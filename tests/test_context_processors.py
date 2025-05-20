import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime as dt
import pytz
from flask import template_rendered, request
from app import app, inject_user, to_datetime


@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    yield recorded
    template_rendered.disconnect(record, app)


def test_inject_user_returns_user(app):
    class DummyUser:
        id = 1

    with app.app_context():
        with patch("app.inject_user.User") as MockUser:
            MockUser.query.get.return_value = DummyUser()
            user = inject_user(1)
            assert user.id == 1


def test_to_datetime():
    timestamp = 1609459200000
    result = to_datetime(timestamp)
    assert result == "2021-01-01 00:00:00"


def test_inject_current_user(client, captured_templates):
    with client:
        with patch("app.current_user", False):
            client.get("/")
            assert any(
                "user" in context or context.get("user") is False
                for _, context in captured_templates
            )


def test_inject_date_and_time(client, captured_templates):
    with client:
        client.get("/")
        assert any("date_and_time" in context for _, context in captured_templates)


def test_inject_date_and_time_isoformat(client, captured_templates):
    with client:
        client.get("/")
        assert any(
            "date_and_time_isoformat" in context for _, context in captured_templates
        )


def test_inject_user_agent(client, captured_templates):
    user_agent = "pytest-agent"
    with client:
        client.get("/", headers={"User-Agent": user_agent})
        assert any(
            context.get("user_agent") == user_agent for _, context in captured_templates
        )


def test_inject_system_info(monkeypatch, client, captured_templates):
    with patch("platform.system", return_value="Linux"), patch(
        "platform.version", return_value="5.4.0-42-generic"
    ), patch("platform.release", return_value="generic-release"):
        with client:
            client.get("/")
            assert any(
                "Linux generic-release 5.4.0-42-generic" in context.get("system_info")
                for _, context in captured_templates
            )


def test_inject_system_uptime(monkeypatch, client, captured_templates):
    with patch(
        "subprocess.check_output",
        return_value=" 10:23:45 up 1 day,  2:34,  2 users,  load average: 0.00, 0.01, 0.05\n",
    ):
        with client:
            client.get("/")
            assert any(
                "10:23:45" in context.get("system_uptime")
                for _, context in captured_templates
            )


def test_inject_python_version(client, captured_templates):
    with client:
        client.get("/")
        assert any("python_version" in context for _, context in captured_templates)


def test_inject_flask_version(client, captured_templates):
    with client:
        client.get("/")
        assert any("flask_version" in context for _, context in captured_templates)


def test_inject_db_info(client, captured_templates):
    with client:
        client.get("/")
        assert any("db_engine" in context for _, context in captured_templates)


def test_shell_context_processor(app):
    ctx = app.shell_context_processor()
    context_dict = ctx()
    expected_keys = {
        "db",
        "User",
        "BotSettings",
        "BotCurrentTrade",
        "TradesHistory",
        "BacktestSettings",
        "BacktestResult",
    }
    assert expected_keys.issubset(context_dict.keys())
