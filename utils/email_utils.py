from flask import current_app
from flask_mail import Message
from datetime import datetime
from typing import Any
from models import User
from utils.logging import logger
from utils.exception_handler import exception_handler
from utils.retry_connection import retry_connection


@exception_handler(default_return=False)
@retry_connection()
def send_email(email: str, subject: str, body: str) -> bool:
    """
    Sends an email to a specified recipient.

    This function uses Flask-Mail to send an email with the given subject and body
    to the specified email address. If an exception occurs, it logs the error
    and notifies the admin via email.

    Args:
        email (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The body content of the email.

    Returns:
        bool: True if the email was sent successfully, False otherwise.

    Raises:
        Logs any exceptions encountered and notifies the admin.
    """
    from app import mail

    with current_app.app_context():
        message = Message(subject=subject, recipients=[email])
        message.body = body
        mail.send(message)
        logger.info(f'Email "{subject}" to {email} sent succesfully.')
        return True


def send_admin_email(subject: str, body: str) -> Any:
    """
    Sends an email notification to all users with admin panel access.

    This function retrieves all users who have `admin_panel_access=True`
    and sends them an email with the given subject and body. If an exception
    occurs, it logs the error.

    Args:
        subject (str): The subject of the email.
        body (str): The body content of the email.

    Raises:
        Logs any exceptions encountered.
    """
    try:
        with current_app.app_context():
            users = User.query.filter_by(is_admin=True).all()
            for user in users:
                success = send_email(user.email, subject, body)
                if not success:
                    logger.error(
                        f"Failed to send admin email to {user.email}. {subject} {body}"
                    )
    except Exception as e:
        logger.error(f"Exception in send_admin_email: {str(e)}")


@exception_handler()
def filter_users_and_send_alert_email(subject: str, body: str) -> Any:
    """
    Sends trade-related notifications via email.

    This function retrieves all users who have `email_trades_receiver=True`
    and sends them an email with the given subject and body. If an exception
    occurs, it logs the error.

    Args:
        subject (str): The subject of the email.
        body (str): The body content of the email.

    Raises:
        Logs any exceptions encountered.
    """
    with current_app.app_context():
        email_alerts_receivers = User.query.filter_by(email_alerts_receiver=True).all()

        for user in email_alerts_receivers:
            success = send_email(user.email, subject, body)
            if not success:
                logger.error(
                    f"Failed to send trade info email to {user.email}. {subject} {body}"
                )
                send_admin_email(
                    f"Error in filter_users_and_send_trade_emails",
                    f"Failed to send trade info email to {user.email}",
                )
