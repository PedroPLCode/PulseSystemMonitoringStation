from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from typing import Optional
from app.models import db


class User(db.Model, UserMixin):
    """
    A database model representing a system user.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The user's login name.
        password_hash (str): The hashed password.
        is_admin (bool): Indicates whether the user has admin privileges.
        email_alerts_receiver (Optional[bool]): If True, the user receives email alerts.
        email (str): The user's email address.
        telegram_alerts_receiver (Optional[bool]): If True, the user receives Telegram alerts.
        telegram_chat_id (Optional[str]): The Telegram chat ID for alerts.
        date_created (Optional[datetime]): The timestamp of user account creation.
        last_login (Optional[datetime]): The timestamp of the user's last login.
        login_errors (Optional[int]): Number of failed login attempts.
        is_suspended (Optional[bool]): If True, the account is suspended.
    """

    id: int = db.Column(db.Integer, primary_key=True, nullable=False)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    password_hash: str = db.Column(db.String(128), nullable=False)
    is_admin: bool = db.Column(db.Boolean, default=False, nullable=False)
    email_alerts_receiver: Optional[bool] = db.Column(
        db.Boolean, default=False, nullable=True
    )
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    telegram_alerts_receiver: Optional[bool] = db.Column(
        db.Boolean, default=False, nullable=True
    )
    telegram_chat_id: Optional[str] = db.Column(
        db.String(120), unique=False, nullable=True
    )
    date_created: Optional[datetime] = db.Column(
        db.DateTime, default=datetime.now, nullable=True
    )
    last_login: Optional[datetime] = db.Column(db.DateTime, nullable=True)
    last_alert_time: Optional[datetime] = db.Column(db.DateTime, nullable=True)
    login_errors: Optional[int] = db.Column(db.Integer, default=0, nullable=True)
    is_suspended: Optional[bool] = db.Column(db.Boolean, default=False, nullable=True)

    def set_password(self, password: str) -> None:
        """
        Sets the user's password by generating a secure hash.

        Args:
            password (str): The plain-text password to be hashed.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Verifies if the given password matches the stored hashed password.

        Args:
            password (str): The plain-text password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def update_last_login(self) -> None:
        """
        Updates the user's last login timestamp to the current UTC time and commits the change.
        """
        self.last_login = datetime.now()
        db.session.commit()

    def update_last_alert_time(self) -> None:
        """
        Updates the user's last alert timestamp to the current UTC time and commits the change.
        """
        self.last_alert_time = datetime.now()
        db.session.commit()

    def increment_login_error(self) -> None:
        """
        Increments the user's failed login attempt counter and commits the change.
        """
        self.login_errors += 1
        db.session.commit()

    def suspend_user(self) -> None:
        """
        Suspends the user account by setting the 'is_suspended' flag and committing the change.
        """
        self.is_suspended = True
        db.session.commit()
