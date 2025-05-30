from flask import request, __version__ as flask_version
from flask_login import current_user
from datetime import datetime as dt
import subprocess
import platform
import sys
import pytz
from app import app, db, login_manager


@login_manager.user_loader
def inject_user(user_id: int) -> object:
    """
    Loads a user from the database based on the user_id.

    Args:
        user_id (int): The unique identifier of the user.

    Returns:
        User: The user object if found, else None.
    """
    from app.models import User

    return User.query.get(int(user_id))


@app.template_filter("to_datetime")
def to_datetime(timestamp: int) -> object:
    """
    Converts a timestamp (in milliseconds) to a formatted datetime string.

    Args:
        timestamp (int): The timestamp to be converted.

    Returns:
        str: A formatted datetime string in 'YYYY-MM-DD HH:MM:SS' format.
    """
    return dt.fromtimestamp(timestamp / 1000.0, tz=pytz.utc).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


@app.context_processor
def inject_current_user() -> dict:
    """
    Injects the current logged-in user into the context for use in templates.

    Returns:
        dict: A dictionary with the key 'user' pointing to the current_user object,
              or False if no user is logged in.
    """
    return dict(user=current_user) if current_user else False


@app.context_processor
def inject_date_and_time() -> dict:
    """
    Injects the current date and time into the context for use in templates.

    Returns:
        dict: A dictionary with the key 'date_and_time' pointing to the current date and time.
    """
    return dict(date_and_time=dt.now().strftime("%Y-%m-%d %H:%M:%S"))


@app.context_processor
def inject_date_and_time_isoformat():
    """
    Injects the current date and time ISO format including timezone into the context for use in templates.
    """
    tz = pytz.timezone('Europe/Warsaw')
    current_time = dt.now(tz)
    return dict(date_and_time_isoformat=current_time.isoformat())


@app.context_processor
def inject_user_agent() -> dict:
    """
    Injects the User-Agent header of the request into the context for use in templates.

    Returns:
        dict: A dictionary with the key 'user_agent' containing the value of the User-Agent header,
              or an error message if the header retrieval fails.
    """
    try:
        user_agent = request.headers.get("User-Agent")
    except Exception as e:
        user_agent = f"Error retrieving user agent: {e}"
    return dict(user_agent=user_agent)


@app.context_processor
def inject_system_info() -> dict:
    """
    Injects the system's name, version, and release information into the context for use in templates.

    Returns:
        dict: A dictionary with the key 'system_info' containing the system information string,
              or an error message if the system information retrieval fails.
    """
    try:
        system_name = platform.system()
        system_version = platform.version()
        release = platform.release()
    except Exception as e:
        system_name = f"Error retrieving system info: {e}"
    return dict(system_info=f"{system_name} {release} {system_version}")


@app.context_processor
def inject_system_uptime() -> dict:
    """
    Injects the system's uptime into the context for use in templates.

    Returns:
        dict: A dictionary with the key 'system_uptime' containing the system uptime string,
              or an error message if the uptime retrieval fails.
    """
    try:
        uptime = subprocess.check_output(["/usr/bin/uptime"], text=True).strip()
    except Exception as e:
        uptime = f"Error retrieving system uptime: {e}"
    return dict(system_uptime=uptime)


@app.context_processor
def inject_python_version() -> dict:
    """
    Injects the Python version into the context for use in templates.

    Returns:
        dict: A dictionary with the key 'python_version' containing the Python version string,
              or an error message if the Python version retrieval fails.
    """
    try:
        python_version = sys.version
    except Exception as e:
        python_version = f"Error retrieving python version: {e}"
    return dict(python_version=python_version)


@app.context_processor
def inject_flask_version() -> dict:
    """
    Injects the Flask version into the context for use in templates.

    Returns:
        dict: A dictionary with the key 'flask_version' containing the Flask version string,
              or an error message if the Flask version retrieval fails.
    """
    try:
        flask_info = flask_version
    except Exception as e:
        flask_info = f"Error retrieving flask version: {e}"
    return dict(flask_version=flask_info)


@app.context_processor
def inject_db_info() -> dict:
    """
    Injects the database engine type into the context for use in templates.

    Returns:
        dict: A dictionary with the key 'db_engine' containing the database engine type string,
              or an error message if the database engine retrieval fails.
    """
    try:
        engine = db.get_engine()
        db_dialect = engine.dialect.name
    except Exception as e:
        db_dialect = f"Error retrieving db info: {e}"
    return dict(db_engine=db_dialect)


@app.shell_context_processor
def make_shell_context() -> dict:
    """
    Provides useful objects for use in the Flask shell.

    Returns:
        dict: A dictionary with useful objects such as 'db', 'User', 'BotSettings', etc.
    """
    return {
        "db": db,
        "User": app.models.User,
        "BotSettings": app.models.BotSettings,
        "BotCurrentTrade": app.models.BotCurrentTrade,
        "TradesHistory": app.models.TradesHistory,
        "BacktestSettings": app.models.BacktestSettings,
        "BacktestResult": app.models.BacktestResult,
    }
