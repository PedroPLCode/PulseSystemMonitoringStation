from flask import render_template, Response
from app import app
from app.models import Monitor, Settings
from app.utils.exception_handler import exception_handler


@exception_handler()
@app.route("/")
def dashboard() -> Response:
    """
    Renders the main dashboard page.

    Returns:
        Response: Rendered HTML page for the dashboard.
    """
    settings = Settings.query.first()
    last_record = Monitor.query.order_by(Monitor.timestamp.desc()).first()

    return render_template(
        "dashboard/dashboard.html", 
        settings=settings,
        last_record=last_record
        )
