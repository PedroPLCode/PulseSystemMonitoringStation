import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app as flask_app


@pytest.fixture(scope="module")
def app():
    flask_app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SECRET_KEY="testsecret",
        WTF_I18N_ENABLED=False,
        RECAPTCHA_PUBLIC_KEY="test",
        RECAPTCHA_PRIVATE_KEY="test",
    )
    return flask_app
