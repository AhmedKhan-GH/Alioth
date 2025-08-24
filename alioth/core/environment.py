import os
import logging
from .decorators import *

log = logging.getLogger(__name__)

@try_catch(exit_code = 1, verbose=True)
def check_environment_vars(required_vars):
    """Check if required environment variables are set."""
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
