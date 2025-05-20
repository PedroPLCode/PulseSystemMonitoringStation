import sys
import pytest
from unittest import mock
from app.utils.exception_handler import exception_handler


class DummyBotSettings:
    def __init__(self, id, bot_running):
        self.id = id
        self.bot_running = bot_running


def dummy_func_no_error(x):
    return x * 2


def dummy_func_raises(exc):
    raise exc("Test error")


@pytest.mark.parametrize(
    "exc",
    [
        IndexError,
        ConnectionError,
        TimeoutError,
        ValueError,
        TypeError,
        FileNotFoundError,
        Exception,
    ],
)
def test_exception_handler_logs_and_sends_email(exc):
    with mock.patch("yourmodule.logger") as mock_logger, mock.patch(
        "yourmodule.send_admin_email"
    ) as mock_send_email, mock.patch(
        "yourmodule.db.session.rollback"
    ) as mock_db_rollback:

        decorated = exception_handler()(dummy_func_raises)
        result = decorated(exc)

        assert mock_logger.error.called
        assert mock_send_email.called
        mock_db_rollback.rollback.assert_not_called()
        assert result is None


def test_exception_handler_db_rollback_and_default_return():
    with mock.patch("yourmodule.logger") as mock_logger, mock.patch(
        "yourmodule.send_admin_email"
    ) as mock_send_email, mock.patch(
        "yourmodule.db.session.rollback"
    ) as mock_db_rollback:

        decorated = exception_handler(default_return=42, db_rollback=True)(
            dummy_func_raises
        )
        result = decorated(ValueError)

        mock_db_rollback.rollback.assert_called_once()
        assert result == 42


def test_exception_handler_default_return_callable():
    with mock.patch("yourmodule.logger"), mock.patch(
        "yourmodule.send_admin_email"
    ), mock.patch("yourmodule.db.session.rollback"):

        decorated = exception_handler(default_return=lambda: "hello")(dummy_func_raises)
        result = decorated(ValueError)

        assert result == "hello"


def test_exception_handler_default_return_exit():
    with mock.patch("yourmodule.logger"), mock.patch(
        "yourmodule.send_admin_email"
    ), mock.patch("yourmodule.db.session.rollback"), mock.patch(
        "sys.exit"
    ) as mock_exit:

        decorated = exception_handler(default_return=exit)(dummy_func_raises)
        decorated(ValueError)

        mock_exit.assert_called_once_with(1)


def test_exception_handler_passes_bot_id(monkeypatch):
    called_args = {}

    def fake_send_admin_email(subject, msg):
        called_args["subject"] = subject
        called_args["msg"] = msg

    monkeypatch.setattr("yourmodule.send_admin_email", fake_send_admin_email)
    monkeypatch.setattr("yourmodule.logger", mock.MagicMock())

    @exception_handler()
    def func(bot_settings=None, bot_id=None):
        raise ValueError("test error")

    bot_settings = DummyBotSettings(id=123, bot_running=True)
    func(bot_settings=bot_settings)

    assert "Bot 123" in called_args["subject"]
    assert "Bot 123" in called_args["msg"]

    called_args.clear()
    try:
        func(bot_id=456)
    except Exception:
        pass

    assert "Bot 456" in called_args["subject"]
    assert "Bot 456" in called_args["msg"]


def test_decorator_passes_through_without_exception():
    decorated = exception_handler()(dummy_func_no_error)
    result = decorated(3)
    assert result == 6
