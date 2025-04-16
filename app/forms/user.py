from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Optional


class UserForm(FlaskForm):
    """
    A form for managing user details.

    Fields:
        username (StringField): The username of the user (required).
        email (StringField): The email address of the user (optional).
        is_admin (BooleanField): Indicates if the user has admin privileges.
        email_alerts_receiver (BooleanField): Indicates if the user should receive email alerts.
        telegram_alerts_receiver (BooleanField): Indicates if the user should receive Telegram alerts.
        telegram_chat_id (StringField): Telegram chat ID for sending alerts (optional).
        date_created (DateTimeField): The date and time the user account was created (optional).
        last_login (DateTimeField): The date and time of the user's last login (optional).
        login_errors (IntegerField): The number of failed login attempts (optional).
        is_suspended (BooleanField): Indicates if the user account is suspended.
    """

    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[Optional()])
    is_admin = BooleanField("is_admin")
    email_alerts_receiver = BooleanField("email_alerts_receiver")
    telegram_alerts_receiver = BooleanField("telegram_alerts_receiver")
    telegram_chat_id = StringField("telegram_chat_id", validators=[Optional()])
    date_created = DateTimeField("date_created", validators=[Optional()])
    last_login = DateTimeField("last_login", validators=[Optional()])
    last_alert_time = DateTimeField("last_alert_time", validators=[Optional()])
    login_errors = IntegerField("login_errors", validators=[Optional()])
    is_suspended = BooleanField("is_suspended")
