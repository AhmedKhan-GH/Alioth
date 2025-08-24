import logging
from alioth.core.decorators import *

log = logging.getLogger(__name__)

@try_catch(exit_code = 1, verbose=True)

def run_application():
    """Main Alioth application logic."""
