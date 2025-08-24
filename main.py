# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os

from dotenv import load_dotenv
import logging
import sys
from functools import wraps

log = logging.getLogger(__name__)

def try_catch(exit_code=1, verbose=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
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

@try_catch(exit_code = 1, verbose=True)
def check_environment_vars(required_vars):
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
            log.warning(f"Missing environment variable: {var}")
        else:
            log.debug(f"Found environment variable: {var}")
    if missing:
        raise Exception(f"Missing environment variables: {missing}")

    log.info("All environment variables found")

def setup_logging(level = logging.INFO, handlers = None):
    """Configure application logging."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers = handlers
    )

def main():
    setup_logging(handlers = [logging.StreamHandler(sys.stdout),
                              logging.FileHandler('app.log', mode='w')])
    log.info("initializing Alioth")
    load_dotenv()
    check_environment_vars(['OPENAI_API_KEY'])

    log.info("terminating Alioth")

if __name__ == '__main__':
    main()