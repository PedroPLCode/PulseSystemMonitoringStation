import pytest
from flask import url_for


def test_404_handler(client):
    response = client.get("/nonexistentpage", follow_redirects=True)
    assert response.status_code == 200
    assert b"dashboard" in response.data or b"Dashboard" in response.data
    assert b"You have no access" not in response.data


def test_429_handler(app, client):
    with app.test_request_context():
        from app import app

        response = app.handle_http_exception(
            type(
                "429error",
                (Exception,),
                {"code": 429, "description": "Too Many Requests"},
            )()
        )
        assert response.status_code == 200
        assert b"limiter" in response.data or b"Too Many Requests" in response.data


def test_unauthorized_handler(client):
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert (
        b"Please log in to access this page" in response.data
        or b"login" in response.data
    )
