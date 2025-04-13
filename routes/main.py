from flask import render_template
from app import app
from utils.exception_handler import exception_handler


@exception_handler()
@app.route("/")
def dashboard():
    return render_template("dashboard/dashboard.html")
