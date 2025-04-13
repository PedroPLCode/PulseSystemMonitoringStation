from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash
from forms import UserForm


class AdminModelView(ModelView):
    form = UserForm

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        flash("You have no access to Admin Panel.", "danger")
        return redirect(url_for("login"))
