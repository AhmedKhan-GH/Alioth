import logging
from alioth.core.decorators import *

log = logging.getLogger(__name__)

@try_catch()
def run_application():
    """Main Alioth application logic."""
    print("Welcome to Alioth, the Intelligence Augmentation platform from the Sternbild Organization.")