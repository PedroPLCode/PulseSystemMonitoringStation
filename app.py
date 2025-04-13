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

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["500 per day", "100 per hour"],
    storage_uri="memory://",
)

mail = Mail(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

admin = Admin(
    app, name="PulseSystemMonitoringStation", template_mode="bootstrap4", base_template="admin/base.html"
)
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Monitor, db.session))


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def start_scheduler():
    from utils.system_monitor import check_resources

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_resources, trigger="interval", minutes=1)
    scheduler.start()
    logger.info("scheduler.start()")


start_scheduler()

from routes import api, session, main


def create_db():
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    create_db()
    app.run(debug=True, host="0.0.0.0", port=8000, use_reloader=True)
