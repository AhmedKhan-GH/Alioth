import unittest
import logging
from io import StringIO
from alioth.core.bootstrap import *

class TestLoggingSetup(unittest.TestCase):
    """Testing logging configuration"""

    def test_setup_logging_with_custom_handlers(self):
        """Test logging setup uses a custom handler when one provided."""
        stream = StringIO()
        setup_logging(level = logging.INFO, handlers = [logging.StreamHandler(stream)])

        logger = logging.getLogger('test')
        logger.info('Test message')

        self.assertIn('INFO', stream.getvalue())
        self.assertIn('Test message', stream.getvalue())


    def test_setup_logging_with_default_handlers(self):
        """Test logging setup uses default handler when none provided."""
        setup_logging()
        self.assertTrue(logging.getLogger().hasHandlers())

if __name__ == '__main__':
    unittest.main()