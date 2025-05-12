from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .monitor import Monitor
from .settings import Settings
from .admin import MyUserModelView, MyModelView
