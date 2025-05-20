import pytest
from flask import Flask
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.forms import LoginForm


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SECRET_KEY"] = "testsecret"
    return app


def test_login_form_valid(app):
    with app.test_request_context(
        method="POST", data={"username": "testuser", "password": "testpass"}
    ):
        form = LoginForm()
        assert form.validate() is True


def test_login_form_missing_username(app):
    with app.test_request_context(
        method="POST", data={"username": "", "password": "testpass"}
    ):
        form = LoginForm()
        assert form.validate() is False
        assert "This field is required." in form.username.errors


def test_login_form_missing_password(app):
    with app.test_request_context(
        method="POST", data={"username": "testuser", "password": ""}
    ):
        form = LoginForm()
        assert form.validate() is False
        assert "This field is required." in form.password.errors


def test_login_form_empty(app):
    with app.test_request_context(method="POST", data={"username": "", "password": ""}):
        form = LoginForm()
        assert form.validate() is False
        assert "This field is required." in form.username.errors
        assert "This field is required." in form.password.errors
