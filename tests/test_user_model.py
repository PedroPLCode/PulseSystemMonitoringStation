import pytest
from datetime import datetime
from app.models import db
from app.models import User


@pytest.fixture
def new_user():
    user = User(username="testuser", email="test@example.com")
    user.set_password("securepassword")
    return user


def test_set_and_check_password(new_user):
    assert new_user.check_password("securepassword")
    assert not new_user.check_password("wrongpassword")


def test_update_last_login(app, new_user):
    with app.app_context():
        db.session.add(new_user)
        db.session.commit()
        new_user.update_last_login()
        assert isinstance(new_user.last_login, datetime)


def test_update_last_alert_time(app, new_user):
    with app.app_context():
        db.session.add(new_user)
        db.session.commit()
        new_user.update_last_alert_time()
        assert isinstance(new_user.last_alert_time, datetime)


def test_increment_login_error(app, new_user):
    with app.app_context():
        db.session.add(new_user)
        db.session.commit()
        initial = new_user.login_errors or 0
        new_user.increment_login_error()
        assert new_user.login_errors == initial + 1


def test_suspend_user(app, new_user):
    with app.app_context():
        db.session.add(new_user)
        db.session.commit()
        assert new_user.is_suspended is not True
        new_user.suspend_user()
        assert new_user.is_suspended is True
