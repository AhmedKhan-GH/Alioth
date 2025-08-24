import logging
import sys

def setup_logging(level = logging.INFO, handlers = None):
    """Configure application logging."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers = handlers
    )
