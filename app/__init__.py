from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from flask_login import LoginManager
from flask_admin import Admin
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config
from functools import partial
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.models import db, User, Monitor, AdminModelView
from app.utils.logging import logger
from typing import Optional

app: Flask = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate: Migrate = Migrate(app, db)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["500 per day", "100 per hour"],
    storage_uri="memory://",
)
limiter.init_app(app)

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


def run_job_with_context(func, *args, **kwargs):
    logger.info(f"Running job: {func.__name__} with args: {args} and kwargs: {kwargs}")
    with app.app_context():
        try:
            result = func(*args, **kwargs)
            logger.info(f"Job {func.__name__} executed successfully. Result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in run_job_with_context: job {func.__name__}: {e}")
            with app.app_context():
                from .utils.email_utils import send_admin_email

                send_admin_email("Error in run_job_with_context", str(e))
            raise


def start_scheduler() -> None:
    """
    Starts the background scheduler that periodically checks system resources.
    """
    try:
        from app.utils.system_monitor import check_resources
        from app.utils.logs_utils import send_logs_via_email_and_clear_logs
        from app.utils.db_utils import backup_database

        scheduler: BackgroundScheduler = BackgroundScheduler()
        scheduler.add_job(
            func=partial(run_job_with_context, check_resources),
            trigger="interval",
            minutes=1,
        )
        scheduler.add_job(
            func=partial(run_job_with_context, send_logs_via_email_and_clear_logs),
            trigger="interval",
            hours=24,
        )
        scheduler.add_job(
            func=partial(run_job_with_context, backup_database),
            trigger="interval",
            hours=24,
        )
        scheduler.start()
        logger.info("scheduler.start()")
    
    except Exception as e:
        logger.error(f"Error in start_scheduler: {e}")
        with app.app_context():
            from app.utils.email_utils import send_admin_email
            send_admin_email("Error in start_scheduler", str(e))


from app.routes import api, session, main


def create_db() -> None:
    """
    Creates all database tables within the current application context.
    """
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    create_db()
    app.run(debug=True, host="0.0.0.0", port=8003, use_reloader=True)
