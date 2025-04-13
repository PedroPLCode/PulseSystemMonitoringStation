from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .user import User
from .monitor import SystemMonitoringData
from .admin import AdminModelView