from flask import render_template, Response
from app import app
from models import Monitor
from utils.exception_handler import exception_handler

@exception_handler()
@app.route("/")
def dashboard() -> Response:
    """
    Renders the main dashboard page.

    Returns:
        Response: Rendered HTML page for the dashboard.
    """
    last_record = Monitor.query.order_by(Monitor.timestamp.desc()).first()
    
    return render_template("dashboard/dashboard.html", last_record=last_record)
