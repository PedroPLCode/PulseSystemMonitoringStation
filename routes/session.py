from flask import render_template, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError
from app import app
from utils.exception_handler import exception_handler


@exception_handler()
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
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

            flash("Registration completed. You can log in now", "success")
            return redirect(url_for("login"))

        except IntegrityError:
            db.session.rollback()
            flash("User with this username or email already exists.", "danger")

        except Exception as e:
            db.session.rollback()
            flash(f"Unexpecter error occured: {str(e)}", "danger")

    return render_template("user/register.html", form=form)


@exception_handler()
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            session.permanent = True
            current_user.update_last_login()
            flash(
                f"Logged in succefully. Welcome back {current_user.username}", "success"
            )
            return redirect(url_for("admin.index"))
        flash("Wrong usermane or password.", "danger")
    return render_template("user/login.html", form=form)


@exception_handler()
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out succefully.", "success")
    return redirect(url_for("login"))
