from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from flask_login import LoginManager
from flask_admin import Admin
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import db, User, Monitor, AdminModelView
from utils.logging import logger
from typing import Optional

app: Flask = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate: Migrate = Migrate(app, db)

limiter: Limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["500 per day", "100 per hour"],
    storage_uri="memory://",
)

mail: Mail = Mail(app)

login_manager: LoginManager = LoginManager(app)
login_manager.login_view = "login"

admin: Admin = Admin(
    app,
    name="PulseSystemMonitoringStation",
    template_mode="bootstrap4",
    base_template="admin/base.html",
)
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Monitor, db.session))


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    """
    Loads a user from the database by their user ID.

    Args:
        user_id (str): The ID of the user to load.

    Returns:
        Optional[User]: The User object if found, otherwise None.
    """
    return db.session.get(User, int(user_id))


def start_scheduler() -> None:
    """
    Starts the background scheduler that periodically checks system resources.
    """
    from utils.system_monitor import check_resources

    scheduler: BackgroundScheduler = BackgroundScheduler()
    scheduler.add_job(func=check_resources, trigger="interval", minutes=1)
    scheduler.start()
    logger.info("scheduler.start()")

start_scheduler()

from routes import api, session, main

def create_db() -> None:
    """
    Creates all database tables within the current application context.
    """
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    create_db()
    app.run(debug=True, host="0.0.0.0", port=8000, use_reloader=True)
