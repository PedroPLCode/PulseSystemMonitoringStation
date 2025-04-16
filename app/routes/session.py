from flask import render_template, redirect, url_for, flash, session, request, Response
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError
from app import app, limiter
from utils.logging import logger
from utils.app_utils import get_ip_address
from utils.exception_handler import exception_handler
from typing import Optional


@exception_handler()
@limiter.limit("4/min")
@app.route("/register", methods=["GET", "POST"])
def register() -> Response:
    """
    Renders and handles the user registration form.

    If the form is submitted and valid, it attempts to create a new user.
    The first registered user is automatically assigned admin privileges.

    Returns:
        Response: Rendered registration form or a redirect to the login page.
    """
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user_ip = get_ip_address(request)
        try:
            is_first_user = User.query.first() is None

            user = User(
                username=form.username.data,
                email=form.email.data,
                is_admin=is_first_user,
            )
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()

            flash("Registration completed. You can log in now.", "success")
            return redirect(url_for("login"))

        except IntegrityError:
            db.session.rollback()
            flash("User with this username or email already exists.", "danger")

        except Exception as e:
            db.session.rollback()
            flash(f"Unexpected error occurred: {str(e)}", "danger")

    return render_template("user/register.html", form=form)


@exception_handler()
@limiter.limit("4/min")
@app.route("/login", methods=["GET", "POST"])
def login() -> Response:
    """
    Renders and handles the user login form.

    Validates user credentials, logs the user in if valid,
    handles login errors, suspensions, and redirects accordingly.

    Returns:
        Response: Rendered login form or a redirect to the admin dashboard.
    """
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user_ip = get_ip_address(request)
        user = User.query.filter_by(username=form.username.data).first()

        if not user:
            logger.error(f"Bad login attempt. User not found from {user_ip}")
            flash("Error: Login or Password Incorrect.", "danger")
            return render_template("user/login.html", form=form)

        if user.is_suspended:
            logger.error(
                f"User {user.username} suspended trying to log in from {user_ip}"
            )
            flash(f"User {user.username} suspended. Admin will contact you.", "danger")
            return render_template("user/login.html", form=form)

        if not user.check_password(form.password.data):
            handle_failed_login(user, user_ip)
            return render_template("user/login.html", form=form)

        handle_successful_login(user)
        return redirect(url_for("admin.index"))

    return render_template("user/login.html", form=form)


@exception_handler(default_return=False)
def handle_successful_login(user: User) -> bool:
    """
    Handles actions required for a successful user login.

    Logs in the user, updates the last login time, and displays a success message.

    Args:
        user (User): The user object representing the authenticated user.

    Returns:
        bool: True if login handling was successful.
    """
    login_user(user)
    session.permanent = True
    current_user.update_last_login()
    flash(f"Logged in successfully. Welcome back {current_user.username}!", "success")
    return True


@exception_handler(default_return=False)
def handle_failed_login(user: User, user_ip: str) -> bool:
    """
    Handles a failed login attempt for a user.

    Increments the user's login error counter, logs a warning, 
    displays an error message, and suspends the user if necessary.

    Args:
        user (User): The user object attempting to log in.
        user_ip (str): The IP address from which the login attempt was made.

    Returns:
        bool: True after handling the failed login.
    """
    user.increment_login_error()
    logger.warning(
        f"User {user.username} login error number {user.login_errors} from {user_ip}."
    )
    flash(f"User {user.username} login error number {user.login_errors}.", "danger")

    if user.login_errors >= 4:
        user.suspend_user()
        logger.warning(f"User {user.username} suspended from address {user_ip}")
        flash(f"User {user.username} suspended. Admin will contact you.", "danger")

    return True


@exception_handler()
@app.route("/logout")
@login_required
def logout() -> Response:
    """
    Logs out the currently authenticated user.

    Displays a logout message and redirects to the login page.

    Returns:
        Response: A redirect response to the login page.
    """
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("dashboard"))
