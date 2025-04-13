from datetime import timedelta
import os
from flask.cli import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = 'tajny_klucz'
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pulse.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=3)

    GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ["GMAIL_USERNAME"]
    MAIL_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
    MAIL_DEFAULT_SENDER = os.environ["GMAIL_USERNAME"]