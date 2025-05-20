import os
import builtins
from unittest import mock
import pytest
from datetime import datetime

from app.utils.logs_utils import send_logs_via_email_and_clear_logs, clear_logs


@pytest.fixture
def mock_logs():
    return ["log1.log", "log2.log"]


@pytest.fixture(autouse=True)
def patch_dependencies(monkeypatch, mock_logs):
    monkeypatch.setattr("app.utils.logs_utils.logs", mock_logs)
    fixed_datetime = datetime(2025, 5, 20, 15, 30, 45)
    monkeypatch.setattr(
        "app.utils.logs_utils.datetime",
        mock.MagicMock(now=mock.MagicMock(return_value=fixed_datetime)),
    )
    monkeypatch.setattr("app.utils.logs_utils.logger", mock.MagicMock())
    monkeypatch.setattr("app.utils.logs_utils.send_admin_email", mock.MagicMock())
    monkeypatch.setattr("app.utils.logs_utils.clear_logs", mock.MagicMock())


def test_send_logs_via_email_and_clear_logs_files_exist(monkeypatch, mock_logs):
    monkeypatch.setattr(os.path, "exists", lambda path: True)

    mock_file = mock.mock_open(read_data="log file content")
    monkeypatch.setattr(builtins, "open", mock_file)

    send_logs_via_email_and_clear_logs()

    from app.utils.logs_utils import send_admin_email

    assert send_admin_email.call_count == len(mock_logs)

    from app.utils.logs_utils import logger

    assert logger.info.called

    from app.utils.logs_utils import clear_logs

    assert clear_logs.called


def test_send_logs_via_email_and_clear_logs_files_do_not_exist(monkeypatch, mock_logs):
    monkeypatch.setattr(os.path, "exists", lambda path: False)

    send_logs_via_email_and_clear_logs()

    from app.utils.logs_utils import send_admin_email, logger, clear_logs

    assert send_admin_email.call_count == 0
    assert logger.warning.call_count == len(mock_logs)
    assert clear_logs.called


def test_clear_logs_files_exist(monkeypatch, mock_logs):
    monkeypatch.setattr(os.path, "exists", lambda path: True)
    mock_file = mock.mock_open()
    monkeypatch.setattr(builtins, "open", mock_file)

    clear_logs()

    mock_file.assert_called()
    handle = mock_file()
    handle.write.assert_called()

    from app.utils.logs_utils import logger

    assert logger.info.called


def test_clear_logs_files_do_not_exist(monkeypatch, mock_logs):
    monkeypatch.setattr(os.path, "exists", lambda path: False)

    clear_logs()

    from app.utils.logs_utils import logger

    assert logger.warning.call_count == len(mock_logs)
