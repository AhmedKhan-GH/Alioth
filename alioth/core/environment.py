import os
import logging
from .decorators import *

log = logging.getLogger(__name__)

@try_catch(exit_code = 2, catch_exceptions = (OSError, IOError))
def check_filesystem_access():
    test_file = "test.txt"
    with open(test_file, "w") as f:
        f.write("test")
    os.remove(test_file)
    log.debug("Filesystem access verified")

# log as debug, only visible on the lowest level of logging
@try_catch(exit_code = 2, catch_exceptions = EnvironmentError)
def check_environment_vars(required_vars):
    """Check if required environment variables are set."""
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
            log.debug(f"Missing environment variable: {var}")
        else:
            log.debug(f"Found environment variable: {var}")

    if missing:
        raise EnvironmentError(f"Missing environment variables: {missing}")

    log.debug("All environment variables found")

