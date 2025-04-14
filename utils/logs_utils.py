from datetime import datetime
import os
from .logging import logger
from .exception_handler import exception_handler
from .email_utils import send_admin_email


@exception_handler()
def send_logs_via_email_and_clear_logs() -> None:
    """
    Sends daily log files via email to the admin and then clears the logs.

    This function iterates through all log files listed in `logs`, reads their content,
    and sends an email with the logs attached. If a log file does not exist, a warning is logged.
    After attempting to send all logs, it clears them using `clear_logs()`.

    Exceptions are handled and logged, and in case of an error, an email notification is sent.

    Returns:
        None
    """
    from .logging import logs

    for log in logs:
        log_file_path: str = os.path.join(os.getcwd(), log)
        now: datetime = datetime.now()
        formatted_now: str = now.strftime("%Y-%m-%d %H:%M:%S")
        today: str = now.strftime("%Y-%m-%d")
        subject: str = f"{today} Daily Logs"

        if os.path.exists(log_file_path):
            with open(log_file_path, "r") as log_file:
                log_content: str = log_file.read()

            send_admin_email(
                f"{subject}: {log}",
                f"PulseSystemMonitoringStation\nDaily logs report.\n{formatted_now}\n\n{log}\n\n{log_content}",
            )
            logger.info(f"Successfully sent email with log: {log}")
        else:
            logger.warning(f"Log file does not exist: {log_file_path}")

    clear_logs()


@exception_handler()
def clear_logs() -> None:
    """
    Clears the content of all log files listed in `logs`.

    This function overwrites each log file with a single line indicating that
    the log has been successfully cleared, along with a timestamp.
    If a log file does not exist, a warning is logged.

    Exceptions are handled and logged, and in case of an error, an email notification is sent.

    Returns:
        None
    """
    from ..utils.logging import logs

    for log in logs:
        log_file_path: str = os.path.join(os.getcwd(), log)
        now: datetime = datetime.now()
        timestamp: str = now.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]

        if os.path.exists(log_file_path):
            with open(log_file_path, "w") as log_file:
                log_file.write(
                    f"{timestamp} CLEAN: Log file {log_file_path} cleared successfully.\n"
                )
            logger.info(f"Successfully cleared log file: {log_file_path}")
        else:
            logger.warning(f"Log file does not exist: {log_file_path}")
