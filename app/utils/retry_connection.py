import time
import requests
import smtplib
from typing import Callable, Any, TypeVar
from app.utils.logging import logger

F = TypeVar("F", bound=Callable[..., Any])


def retry_connection(max_retries: int = 3, delay: float = 1) -> Callable[[F], F]:
    """
    A decorator that retries connecting to the API or other services in case of connection issues.

    Args:
        max_retries (int): Maximum number of retry attempts.
        delay (float): Time in seconds between each retry attempt.

    Returns:
        Callable: A decorator that wraps the target function with retry logic.
    """

    def retry_connection_decorator(func: F) -> F:
        def retry_connection_wrapper(*args: Any, **kwargs: Any) -> Any:
            retries: int = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (
                    ConnectionError,
                    TimeoutError,
                    requests.exceptions.RequestException,
                    smtplib.SMTPException,
                    OSError,
                ) as e:
                    retries += 1
                    logger.warning(
                        f"retry_connection Connection failed (attempt {retries}/{max_retries}). Retrying in {delay} seconds..."
                    )
                    time.sleep(delay)
            error_msg: str = (
                f"retry_connection. Max retries reached. Connection failed. "
                f"max_retries: {max_retries}, delay: {delay}"
            )
            logger.error(error_msg)
            raise Exception(error_msg)

        return retry_connection_wrapper

    return retry_connection_decorator
