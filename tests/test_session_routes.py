from app.models import User, db
from flask import session
from werkzeug.security import check_password_hash


def test_register_first_user(client, app):
    with app.app_context():
        response = client.post(
            "/register",
            data={
                "username": "admin",
                "email": "admin@example.com",
                "password": "Test1234",
                "confirm": "Test1234",
            },
            follow_redirects=True,
        )

        user = User.query.filter_by(username="admin").first()

        assert response.status_code == 200
        assert user is not None
        assert user.is_admin is True
        assert check_password_hash(user.password_hash, "Test1234")
        assert b"Registration completed" in response.data


def test_register_duplicate_username(client, app):
    with app.app_context():
        db.session.add(User(username="existing", email="existing@example.com"))
        db.session.commit()

        response = client.post(
            "/register",
            data={
                "username": "existing",
                "email": "new@example.com",
                "password": "Test1234",
                "confirm": "Test1234",
            },
            follow_redirects=True,
        )

        assert b"already exists" in response.data


def test_login_success(client, app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        user.set_password("Test1234")
        db.session.add(user)
        db.session.commit()

        response = client.post(
            "/login",
            data={"username": "testuser", "password": "Test1234"},
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"Logged in successfully" in response.data


def test_login_invalid_password(client, app):
    with app.app_context():
        user = User(username="testuser2", email="test2@example.com")
        user.set_password("CorrectPassword")
        db.session.add(user)
        db.session.commit()

        response = client.post(
            "/login",
            data={"username": "testuser2", "password": "WrongPassword"},
            follow_redirects=True,
        )

        assert b"login error number 1" in response.data
        updated_user = User.query.filter_by(username="testuser2").first()
        assert updated_user.login_errors == 1


def test_login_suspended_user(client, app):
    with app.app_context():
        user = User(
            username="suspended", email="suspended@example.com", is_suspended=True
        )
        user.set_password("Test1234")
        db.session.add(user)
        db.session.commit()

        response = client.post(
            "/login",
            data={"username": "suspended", "password": "Test1234"},
            follow_redirects=True,
        )

        assert b"suspended" in response.data


def test_logout(client, app):
    with app.app_context():
        user = User(username="logoutuser", email="logout@example.com")
        user.set_password("Test1234")
        db.session.add(user)
        db.session.commit()

        client.post(
            "/login",
            data={"username": "logoutuser", "password": "Test1234"},
            follow_redirects=True,
        )

        response = client.get("/logout", follow_redirects=True)

        assert b"Logged out successfully" in response.data
