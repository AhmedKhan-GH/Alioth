import unittest
import logging
from ctypes.macholib.dyld import dyld_default_search
from io import StringIO
from alioth.core.bootstrap import *
from unittest.mock import Mock, patch

class TestLoggingSetup(unittest.TestCase):
    """Testing logging configuration"""

    def test_setup_logging_with_custom_handlers(self):
        """Test logging setup with custom handlers configures correctly."""
        stream = StringIO()
        custom_handler = logging.StreamHandler(stream)

        # Clear any existing handlers to ensure clean test
        logging.getLogger().handlers.clear()

        setup_logging(level=logging.INFO, handlers=[custom_handler])

        # Check that the custom handler is actually configured
        root_logger = logging.getLogger()
        self.assertIs(root_logger.handlers[0], custom_handler)
        self.assertEqual(root_logger.level, logging.INFO)

        # Clean up
        logging.getLogger().handlers.clear()

    def test_setup_logging_with_default_handlers(self):
        """Test logging setup uses default handler when none provided."""
        setup_logging()
        self.assertTrue(logging.getLogger().hasHandlers())

if __name__ == '__main__':
    unittest.main()