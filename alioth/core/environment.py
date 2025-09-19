import os
import logging

from .decorators import *
import tempfile

log = logging.getLogger(__name__)

@try_catch(exit_code = 2, catch_exceptions = (OSError, IOError))
def check_filesystem_access():
    """Verify filesystem access by writing and deleting a test file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test")
        temp_path = f.name
    os.remove(temp_path)
    log.info("Filesystem access verified")

@try_catch(exit_code = 2, catch_exceptions = EnvironmentError)
def get_environment_variable(key, required = False, default_value = None):
    """Lazy check to get an environment variable and raise an exception if it is missing."""
    if not os.getenv(key):
        if required:
            raise EnvironmentError(f"missing required environment variable: {key}")
        else:
            log.warning(f"Missing optional environment variable: {key}")
            if default_value: os.environ[key] = default_value
            return default_value
    log.info(f"Found environment variable: {key}")
    return os.getenv(key)

