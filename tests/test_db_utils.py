import os
import builtins
import pytest
from unittest.mock import patch, MagicMock
from app.utils import backup_database


@pytest.fixture
def setup_mocks():
    with patch("app.utils.os.path.exists") as mock_exists, patch(
        "app.utils.os.makedirs"
    ) as mock_makedirs, patch("app.utils.shutil.copy2") as mock_copy2, patch(
        "app.utils.logger"
    ) as mock_logger, patch(
        "app.utils.send_admin_email"
    ) as mock_send_email:
        yield mock_exists, mock_makedirs, mock_copy2, mock_logger, mock_send_email


def test_backup_database_success_existing_backup_dir(setup_mocks):
    mock_exists, mock_makedirs, mock_copy2, mock_logger, mock_send_email = setup_mocks
    mock_exists.side_effect = (
        lambda path: path == "instance/pulse.db" or path == "instance/backup"
    )

    result = backup_database()

    assert result == "instance/backup/backup_pulse.db"
    mock_copy2.assert_called_once_with(
        "instance/pulse.db", "instance/backup/backup_pulse.db"
    )
    mock_logger.info.assert_called_once()
    mock_send_email.assert_called_once()


def test_backup_database_success_create_backup_dir(setup_mocks):
    mock_exists, mock_makedirs, mock_copy2, mock_logger, mock_send_email = setup_mocks

    def exists_side_effect(path):
        if path == "instance/pulse.db":
            return True
        if path == "instance/backup":
            return False
        return False

    mock_exists.side_effect = exists_side_effect

    result = backup_database()

    assert result == "instance/backup/backup_pulse.db"
    mock_makedirs.assert_called_once_with("instance/backup")
    mock_copy2.assert_called_once_with(
        "instance/pulse.db", "instance/backup/backup_pulse.db"
    )
    mock_logger.info.assert_called_once()
    mock_send_email.assert_called_once()


def test_backup_database_file_not_found(setup_mocks):
    mock_exists, mock_makedirs, mock_copy2, mock_logger, mock_send_email = setup_mocks
    mock_exists.return_value = False

    with pytest.raises(FileNotFoundError):
        backup_database()
    mock_makedirs.assert_not_called()
    mock_copy2.assert_not_called()
    mock_logger.info.assert_not_called()
    mock_send_email.assert_not_called()
