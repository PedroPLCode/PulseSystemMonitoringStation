import pytest
from unittest import mock
from flask import Flask
from app import app, load_user, run_job_with_context, start_scheduler
from app.models import User


def test_load_user_returns_user(monkeypatch):
    test_user = User(id=1, login="testuser")
    monkeypatch.setattr(
        "app.db.session.get", lambda model, user_id: test_user if user_id == 1 else None
    )

    user = load_user("1")
    assert user is test_user

    user_none = load_user("999")
    assert user_none is None


def test_run_job_with_context_success(monkeypatch):
    def test_func(x, y):
        return x + y

    monkeypatch.setattr("app.logger", mock.Mock())

    result = run_job_with_context(test_func, 2, 3)
    assert result == 5
    assert app.logger.info.called


def test_run_job_with_context_failure(monkeypatch):
    def fail_func():
        raise ValueError("fail")

    monkeypatch.setattr("app.logger", mock.Mock())

    monkeypatch.setattr("app.utils.email_utils.send_admin_email", mock.Mock())

    with pytest.raises(ValueError):
        run_job_with_context(fail_func)

    assert app.logger.error.called
    from app.utils.email_utils import send_admin_email

    assert send_admin_email.called


def test_start_scheduler(monkeypatch):
    mock_scheduler = mock.Mock()
    mock_scheduler.add_job = mock.Mock()
    mock_scheduler.start = mock.Mock()

    monkeypatch.setattr("app.BackgroundScheduler", lambda: mock_scheduler)
    monkeypatch.setattr("app.logger", mock.Mock())

    monkeypatch.setattr("app.utils.system_monitor.check_resources", mock.Mock())
    monkeypatch.setattr(
        "app.utils.logs_utils.send_logs_via_email_and_clear_logs", mock.Mock()
    )
    monkeypatch.setattr("app.utils.db_utils.backup_database", mock.Mock())

    start_scheduler()

    assert mock_scheduler.add_job.call_count == 3
    assert mock_scheduler.start.called
    assert app.logger.info.called


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    rv = client.get("/")
    assert rv.status_code in (200, 404)
