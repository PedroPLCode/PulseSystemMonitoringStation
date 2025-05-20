import pytest
from unittest import mock
from app.utils.retry_connection import retry_connection


def dummy_func_no_error():
    return "success"


def dummy_func_raise_connection_error():
    raise ConnectionError("Connection failed")


def dummy_func_raise_request_exception():
    import requests

    raise requests.exceptions.RequestException("Request failed")


def dummy_func_raise_smtp_exception():
    import smtplib

    raise smtplib.SMTPException("SMTP failed")


@pytest.mark.parametrize(
    "exception_func",
    [
        dummy_func_raise_connection_error,
        dummy_func_raise_request_exception,
        dummy_func_raise_smtp_exception,
    ],
)
def test_retry_success_after_retries(exception_func):
    call_count = {"count": 0}

    @retry_connection(max_retries=3, delay=0)
    def func():
        call_count["count"] += 1
        if call_count["count"] < 2:
            return exception_func()
        return "ok"

    with mock.patch("yourmodule.logger") as mock_logger, mock.patch(
        "time.sleep", return_value=None
    ):

        result = func()
        assert result == "ok"
        assert call_count["count"] == 2
        assert mock_logger.warning.called


def test_retry_raises_after_max_retries():
    @retry_connection(max_retries=3, delay=0)
    def func():
        raise ConnectionError("fail")

    with mock.patch("yourmodule.logger") as mock_logger, mock.patch(
        "time.sleep", return_value=None
    ):

        with pytest.raises(Exception) as excinfo:
            func()

        assert "Max retries reached" in str(excinfo.value)
        assert mock_logger.error.called
        assert mock_logger.warning.call_count == 3


def test_retry_no_exception_returns_value():
    @retry_connection()
    def func():
        return "ok"

    with mock.patch("yourmodule.logger") as mock_logger, mock.patch(
        "time.sleep", return_value=None
    ):
        result = func()
        assert result == "ok"
        mock_logger.warning.assert_not_called()
        mock_logger.error.assert_not_called()
