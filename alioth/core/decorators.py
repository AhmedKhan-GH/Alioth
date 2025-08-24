import logging
from functools import wraps
import sys
import os
import inspect
from typing import Union, Type, Tuple

# log at info level, visible at the second-lowest level of logging, this serves
# to outline program execution flow without cluttering the logs with validation
def try_catch(exit_code=1, exit_on_error=True, default_return=None, catch_exceptions: type = BaseException):
    """Decorator to catch exceptions and exit with a specific exit code.

    Args:
        exit_code (int): Exit code to use when exiting the program, passed to the operating system
        exit_on_error (bool): Whether to exit the program on error or just continue
        default_return: Value of a desired type to return if an exception is raised and exit_on_error is False
        catch_exceptions (Exception): Exception types to catch and handle, others are raised up the call stack
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log = logging.getLogger(func.__module__)

            log.info(f"Starting {func.__name__}")
            try:
                result = func(*args, **kwargs)
                log.info(f"Completed {func.__name__}")
                return result

            # only catch specified exception types
            except catch_exceptions as e:
                log.error(f"Failed {func.__name__}: {e}")
                if exit_on_error:
                    sys.exit(exit_code)
                else:
                    return default_return
        return wrapper
    return decorator
