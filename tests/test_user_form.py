import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.forms import UserForm


@pytest.mark.usefixtures("app")
class TestUserForm:
    def test_valid_data(self, app):
        with app.app_context():
            form = UserForm(
                data={
                    "username": "john_doe",
                    "email": "john@example.com",
                    "is_admin": True,
                    "email_alerts_receiver": True,
                    "telegram_alerts_receiver": True,
                    "telegram_chat_id": "123456789",
                    "date_created": "2023-01-01 12:00:00",
                    "last_login": "2023-01-02 15:00:00",
                    "last_alert_time": "2023-01-03 18:00:00",
                    "login_errors": 2,
                    "is_suspended": False,
                }
            )
            assert form.validate() is True

    def test_missing_required_username(self, app):
        with app.app_context():
            form = UserForm(data={"email": "john@example.com"})
            assert form.validate() is False
            assert "username" in form.errors

    def test_optional_fields_can_be_empty(self, app):
        with app.app_context():
            form = UserForm(data={"username": "jane_doe"})
            assert form.validate() is True
