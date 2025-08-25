import logging
from alioth.core.decorators import *

log = logging.getLogger(__name__)

@try_catch()
def run_application():
    """Main Alioth application logic."""
    log.info("Activating Alioth")



    log.info("Deactivating Alioth")