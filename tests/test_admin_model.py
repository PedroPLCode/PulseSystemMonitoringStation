from flask import url_for
from flask_login import AnonymousUserMixin
from app.models import AdminProtectedModelView, MyUserModelView, MyModelView
from types import SimpleNamespace


class FakeUser:
    def __init__(self, authenticated=False, is_admin=False):
        self.is_authenticated = authenticated
        self.is_admin = is_admin


def test_is_accessible_authenticated_admin_user(mocker):
    mocker.patch("app.admin.current_user", FakeUser(authenticated=True, is_admin=True))
    view = AdminProtectedModelView()
    assert view.is_accessible() is True


def test_is_accessible_authenticated_non_admin_user(mocker):
    mocker.patch("app.admin.current_user", FakeUser(authenticated=True, is_admin=False))
    view = AdminProtectedModelView()
    assert view.is_accessible() is False


def test_is_accessible_unauthenticated_user(mocker):
    mocker.patch(
        "app.admin.current_user", FakeUser(authenticated=False, is_admin=False)
    )
    view = AdminProtectedModelView()
    assert view.is_accessible() is False


def test_inaccessible_callback_redirects(mocker, app):
    with app.test_request_context():
        mocker.patch("app.admin.flash")
        view = AdminProtectedModelView()
        response = view.inaccessible_callback(name="admin")
        assert response.status_code == 302
        assert response.location == url_for("login")


def test_my_user_model_view_has_custom_form():
    view = MyUserModelView()
    from app.forms import UserForm

    assert view.form == UserForm
    assert "password_hash" in view.form_excluded_columns
    assert "password_hash" in view.column_exclude_list


def test_my_model_view_is_instance():
    view = MyModelView()
    assert isinstance(view, AdminProtectedModelView)
