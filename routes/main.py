from flask import render_template, Response
from app import app
from utils.exception_handler import exception_handler


@exception_handler()
@app.route("/")
def dashboard() -> Response:
    """
    Renders the main dashboard page.

    Returns:
        Response: Rendered HTML page for the dashboard.
    """
    return render_template("dashboard/dashboard.html")
