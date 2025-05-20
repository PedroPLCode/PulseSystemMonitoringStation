import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from app.utils.telegram_utils import (
    init_telegram_bot,
    send_telegram,
    filter_users_and_send_alert_telegram,
)
from app.models import User, Settings


@pytest.fixture
def app_context(app):
    """Flask app context fixture"""
    with app.app_context():
        yield


@patch("app.utils.telegram_utils.os.environ", {"TELEGRAM_API_SECRET": "fake_token"})
@patch("app.utils.telegram_utils.TelegramBot")
def test_init_telegram_bot_success(mock_bot_class):
    mock_bot_class.return_value = "bot_instance"
    bot = init_telegram_bot()
    assert bot == "bot_instance"
    mock_bot_class.assert_called_once_with(token="fake_token")


@patch("app.utils.telegram_utils.os.environ", {})
@patch("app.utils.telegram_utils.logger")
def test_init_telegram_bot_missing_env_var(mock_logger):
    bot = init_telegram_bot()
    assert bot is False or bot is None
    mock_logger.error.assert_called()


@patch("app.utils.telegram_utils.init_telegram_bot")
@patch("app.utils.telegram_utils.asyncio")
@patch("app.utils.telegram_utils.logger")
def test_send_telegram_success(mock_logger, mock_asyncio, mock_init_bot):
    mock_bot = MagicMock()
    mock_init_bot.return_value = mock_bot

    mock_asyncio.run = MagicMock()

    result = send_telegram("chat_id_123", "Hello Telegram")
    assert result is True
    mock_asyncio.run.assert_called_once()
    mock_logger.info.assert_called()


@patch("app.utils.telegram_utils.init_telegram_bot")
def test_send_telegram_no_bot(mock_init_bot):
    mock_init_bot.return_value = None
    result = send_telegram("chat_id_123", "Hello Telegram")
    assert result is False


@patch("app.utils.telegram_utils.send_telegram")
@patch("app.utils.telegram_utils.send_admin_email")
@patch("app.utils.telegram_utils.User")
@patch("app.utils.telegram_utils.Settings")
@patch("app.utils.telegram_utils.logger")
def test_filter_users_and_send_alert_telegram(
    mock_logger,
    mock_settings,
    mock_user,
    mock_send_admin_email,
    mock_send_telegram,
    app_context,
):
    mock_settings.query.first.return_value = MagicMock(alerts_frequency_hrs=1)

    user1 = MagicMock()
    user1.email = "user1@example.com"
    user1.telegram_chat_id = "chat1"
    user1.last_alert_time = None
    user1.update_last_alert_time = MagicMock()

    user2 = MagicMock()
    user2.email = "user2@example.com"
    user2.telegram_chat_id = "chat2"
    user2.last_alert_time = datetime.now() - timedelta(minutes=30)
    user2.update_last_alert_time = MagicMock()

    mock_user.query.filter_by.return_value.all.return_value = [user1, user2]

    mock_send_telegram.side_effect = [True]

    filter_users_and_send_alert_telegram("Trade alert")

    mock_send_telegram.assert_called_once_with(chat_id="chat1", msg="Trade alert")
    user1.update_last_alert_time.assert_called_once()
    mock_logger.warning.assert_called_once()


@patch("app.utils.telegram_utils.send_telegram")
@patch("app.utils.telegram_utils.send_admin_email")
@patch("app.utils.telegram_utils.User")
@patch("app.utils.telegram_utils.Settings")
@patch("app.utils.telegram_utils.logger")
def test_filter_users_and_send_alert_telegram_send_failure(
    mock_logger,
    mock_settings,
    mock_user,
    mock_send_admin_email,
    mock_send_telegram,
    app_context,
):
    mock_settings.query.first.return_value = MagicMock(alerts_frequency_hrs=1)

    user = MagicMock()
    user.email = "user@example.com"
    user.telegram_chat_id = "chat_id"
    user.last_alert_time = None
    user.update_last_alert_time = MagicMock()

    mock_user.query.filter_by.return_value.all.return_value = [user]
    mock_send_telegram.return_value = False

    filter_users_and_send_alert_telegram("Trade alert")

    mock_logger.error.assert_called_once()
    mock_send_admin_email.assert_called_once()
    user.update_last_alert_time.assert_not_called()
