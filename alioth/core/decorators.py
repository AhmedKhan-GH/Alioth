import logging
from functools import wraps
import sys

def try_catch(exit_code=1, verbose=False):
    """Decorator to catch exceptions and exit with a specific exit code."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log = logging.getLogger(func.__module__)

            if verbose:
                log.info(f"Starting {func.__name__}")
            try:
                result = func(*args, **kwargs)
                if verbose:
                    log.info(f"Completed {func.__name__}")
                return result
            except Exception as e:
                log.error(f"Failed {func.__name__}: {e}")
                sys.exit(exit_code)
        return wrapper
    return decorator
