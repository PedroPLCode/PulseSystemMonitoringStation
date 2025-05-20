import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.forms import RegisterForm


@pytest.fixture
def valid_form_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "StrongPass1!",
        "confirm_password": "StrongPass1!",
        "g-recaptcha-response": "PASSED",
    }


def test_valid_form(app, valid_form_data):
    with app.app_context():
        form = RegisterForm(data=valid_form_data)
        assert form.validate() is True


@pytest.mark.parametrize(
    "password", ["weakpass", "NoNumber!", "nonumber1!", "NOLOWER1!", "NoSpecial1"]
)
def test_password_complexity_fail(app, password, valid_form_data):
    with app.app_context():
        valid_form_data["password"] = password
        valid_form_data["confirm_password"] = password
        form = RegisterForm(data=valid_form_data)
        assert not form.validate()
        assert "password" in form.errors


def test_mismatched_passwords(app, valid_form_data):
    with app.app_context():
        valid_form_data["confirm_password"] = "DifferentPass1!"
        form = RegisterForm(data=valid_form_data)
        assert not form.validate()
        assert "confirm_password" in form.errors


def test_invalid_email(app, valid_form_data):
    with app.app_context():
        valid_form_data["email"] = "invalidemail"
        form = RegisterForm(data=valid_form_data)
        assert not form.validate()
        assert "email" in form.errors


def test_missing_username(app, valid_form_data):
    with app.app_context():
        valid_form_data["username"] = ""
        form = RegisterForm(data=valid_form_data)
        assert not form.validate()
        assert "username" in form.errors


def test_short_password(app, valid_form_data):
    with app.app_context():
        valid_form_data["password"] = "Aa1!"
        valid_form_data["confirm_password"] = "Aa1!"
        form = RegisterForm(data=valid_form_data)
        assert not form.validate()
        assert "password" in form.errors
