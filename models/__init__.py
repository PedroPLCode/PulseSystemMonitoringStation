from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .monitor import Monitor
from .admin import AdminModelView
