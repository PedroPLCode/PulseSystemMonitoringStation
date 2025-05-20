import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from app.utils.email_utils import (
    send_email,
    send_admin_email,
    filter_users_and_send_alert_email,
)
from app.models import User, Settings


@pytest.fixture
def app_context(app):
    """Użyj fixture z kontekstem aplikacji Flask"""
    with app.app_context():
        yield


@patch("app.utils.email_utils.mail")
@patch("app.utils.email_utils.logger")
def test_send_email_success(mock_logger, mock_mail, app_context):
    mock_mail.send = MagicMock()
    result = send_email("test@example.com", "Subject", "Body")
    assert result is True
    mock_mail.send.assert_called_once()
    mock_logger.info.assert_called_once()


@patch("app.utils.email_utils.mail")
@patch("app.utils.email_utils.logger")
def test_send_email_exception(mock_logger, mock_mail, app_context):
    mock_mail.send.side_effect = Exception("Fail to send")
    result = send_email("test@example.com", "Subject", "Body")
    assert result is False
    mock_logger.info.assert_not_called()


@patch("app.utils.email_utils.send_email")
@patch("app.utils.email_utils.User")
@patch("app.utils.email_utils.logger")
def test_send_admin_email_success(mock_logger, mock_user, mock_send_email, app_context):
    admin_user = MagicMock()
    admin_user.email = "admin@example.com"
    mock_user.query.filter_by.return_value.all.return_value = [admin_user]

    mock_send_email.return_value = True
    send_admin_email("Admin Subject", "Admin Body")
    mock_send_email.assert_called_once_with(
        "admin@example.com", "Admin Subject", "Admin Body"
    )
    mock_logger.error.assert_not_called()


@patch("app.utils.email_utils.send_email")
@patch("app.utils.email_utils.User")
@patch("app.utils.email_utils.logger")
def test_send_admin_email_failure(mock_logger, mock_user, mock_send_email, app_context):
    admin_user = MagicMock()
    admin_user.email = "admin@example.com"
    mock_user.query.filter_by.return_value.all.return_value = [admin_user]

    mock_send_email.return_value = False
    send_admin_email("Admin Subject", "Admin Body")
    mock_logger.error.assert_called_once()


@patch("app.utils.email_utils.send_email")
@patch("app.utils.email_utils.send_admin_email")
@patch("app.utils.email_utils.User")
@patch("app.utils.email_utils.Settings")
@patch("app.utils.email_utils.logger")
def test_filter_users_and_send_alert_email(
    mock_logger,
    mock_settings,
    mock_user,
    mock_send_admin_email,
    mock_send_email,
    app_context,
):
    mock_settings.query.first.return_value = MagicMock(alerts_frequency_hrs=1)

    user1 = MagicMock()
    user1.email = "user1@example.com"
    user1.last_alert_time = None
    user1.update_last_alert_time = MagicMock()

    user2 = MagicMock()
    user2.email = "user2@example.com"
    user2.last_alert_time = datetime.now() - timedelta(minutes=30)
    user2.update_last_alert_time = MagicMock()

    mock_user.query.filter_by.return_value.all.return_value = [user1, user2]

    mock_send_email.side_effect = [True]

    filter_users_and_send_alert_email("Alert Subject", "Alert Body")

    mock_send_email.assert_called_once_with(
        "user1@example.com", "Alert Subject", "Alert Body"
    )
    user1.update_last_alert_time.assert_called_once()

    mock_logger.warning.assert_called_once()


@patch("app.utils.email_utils.send_email")
@patch("app.utils.email_utils.send_admin_email")
@patch("app.utils.email_utils.User")
@patch("app.utils.email_utils.Settings")
@patch("app.utils.email_utils.logger")
def test_filter_users_and_send_alert_email_send_failure(
    mock_logger,
    mock_settings,
    mock_user,
    mock_send_admin_email,
    mock_send_email,
    app_context,
):
    mock_settings.query.first.return_value = MagicMock(alerts_frequency_hrs=1)

    user = MagicMock()
    user.email = "user@example.com"
    user.last_alert_time = None
    user.update_last_alert_time = MagicMock()

    mock_user.query.filter_by.return_value.all.return_value = [user]
    mock_send_email.return_value = False

    filter_users_and_send_alert_email("Alert Subject", "Alert Body")

    mock_logger.error.assert_called_once()
    mock_send_admin_email.assert_called_once()
    user.update_last_alert_time.assert_not_called()
