from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash
from app.forms import UserForm


class UserModelView(ModelView):
    """
    A customized SQLAlchemy admin view that restricts access
    to authenticated admin users only.

    Attributes:
        form (UserForm): The form used for creating and editing users in the admin panel.

    Methods:
        is_accessible() -> bool:
            Checks if the current user is authenticated and has admin privileges.

        inaccessible_callback(name: str, **kwargs) -> Any:
            Redirects unauthorized users to the login page with an error message.
    """

    form = UserForm
    form_excluded_columns = ["password_hash"]
    column_exclude_list = ["password_hash"]

    def is_accessible(self) -> bool:
        """
        Determines whether the current user is allowed to access the admin view.

        Returns:
            bool: True if the user is authenticated and has admin rights, False otherwise.
        """
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name: str, **kwargs) -> str:
        """
        Handles unauthorized access attempts by redirecting to the login page.

        Args:
            name (str): The name of the attempted admin view.
            **kwargs: Additional keyword arguments.

        Returns:
            str: A redirect response to the login page.
        """
        flash("You have no access to Admin Panel.", "danger")
        return redirect(url_for("login"))
