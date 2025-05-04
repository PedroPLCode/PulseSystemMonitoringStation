from datetime import timedelta
import os
from flask.cli import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///pulse.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ["APP_SECRET_KEY"]
    WTF_CSRF_SECRET_KEY = os.environ["CSRF_SECRET_KEY"]
    SESSION_COOKIE_SECURE = True  # False if https ssl disabled
    WTF_CSRF_SSL_STRICT = True  # False if https ssl disabled
    WTF_CSRF_ENABLED = True  # False if https ssl disabled

    PERMANENT_SESSION_LIFETIME = timedelta(minutes=3)

    GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ["GMAIL_USERNAME"]
    MAIL_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
    MAIL_DEFAULT_SENDER = os.environ["GMAIL_USERNAME"]

    RECAPTCHA_PUBLIC_KEY = os.environ["RECAPTCHA_PUBLIC_KEY"]
    RECAPTCHA_PRIVATE_KEY = os.environ["RECAPTCHA_PRIVATE_KEY"]
