import sys
import functools
import logging
from typing import Any, Callable, Optional, TypeVar, Union
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def exception_handler(
    default_return: Optional[Union[Any, Callable[[], Any]]] = None,
    db_rollback: bool = False,
) -> Callable[[F], F]:
    """
    A decorator that catches exceptions, logs the error, optionally rolls back the database session,
    and sends an email notification.

    Args:
        default_return (Any, optional): The value or callable to return if an exception occurs.
                                        If set to `exit`, calls sys.exit(1). Defaults to None.
        db_rollback (bool, optional): If True, rolls back the database session upon an exception.
                                      Defaults to False.

    Returns:
        Callable: A decorator wrapping the target function with exception handling logic.

    Exceptions Caught:
        - IndexError
        - ConnectionError
        - TimeoutError
        - ValueError
        - TypeError
        - FileNotFoundError
        - SQLAlchemyError
        - General Exception (any other unexpected errors)

    Behavior:
        - Logs the exception with the bot ID (if available).
        - Sends an email notification to the administrator.
        - Optionally rolls back the database session if `db_rollback=True`.
        - Returns `default_return` or its result in case of an error.
    """

    def exception_handler_decorator(func: F) -> F:
        @functools.wraps(func)
        def exception_handler_wrapper(*args: Any, **kwargs: Any) -> Any:
            bot_id: Optional[int] = None

            if "bot_settings" in kwargs and hasattr(kwargs["bot_settings"], "id"):
                bot_id = kwargs["bot_settings"].id
            else:
                for arg in args:
                    if hasattr(arg, "id") and hasattr(arg, "bot_running"):
                        bot_id = arg.id
                        break

            if bot_id is None:
                if "bot_id" in kwargs:
                    bot_id = kwargs["bot_id"]
                else:
                    for arg in args:
                        if isinstance(arg, int):
                            bot_id = arg
                            break

            bot_str = f"Bot {bot_id} " if bot_id else ""

            try:
                return func(*args, **kwargs)
            except (
                IndexError,
                ConnectionError,
                TimeoutError,
                ValueError,
                TypeError,
                FileNotFoundError,
                SQLAlchemyError,
            ) as e:
                exception_type = type(e).__name__
                logger.error(f"{bot_str}{exception_type} in {func.__name__}: {str(e)}")
                from .email_utils import send_admin_email

                send_admin_email(
                    f"{bot_str}{exception_type} in {func.__name__}",
                    f"StefanCryptoTradingBot\n{exception_type} in {func.__name__}\n\n{str(e)}",
                )
            except Exception as e:
                exception_type = "Exception"
                logger.error(f"{bot_str}{exception_type} in {func.__name__}: {str(e)}")
                from .email_utils import send_admin_email

                send_admin_email(
                    f"{bot_str}{exception_type} in {func.__name__}",
                    f"StefanCryptoTradingBot\n{exception_type} in {func.__name__}\n\n{str(e)}",
                )

            if db_rollback:
                from ... import db

                db.session.rollback()
                logger.error(
                    f"db.session.rollback() Database transaction rollback executed."
                )

            if default_return is exit:
                logger.error("sys.exit(1) Exiting program due to an error.")
                sys.exit(1)
            elif callable(default_return):
                return default_return()
            return default_return

        return exception_handler_wrapper

    return exception_handler_decorator
