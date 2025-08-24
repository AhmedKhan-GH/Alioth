import unittest
import os
from unittest.mock import patch
import sys
from alioth.core.environment import *

class TestEnvironmentValidation(unittest.TestCase):
    """Testing environment variable validation"""

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    @patch.dict(os.environ, {'TEST_VAR': 'test_value'}, clear = False)
    def test_check_environment_vars_success(self):
        check_environment_vars(['TEST_VAR'])

    @patch.dict(os.environ, {}, clear = True)
    @patch('sys.exit')
    def test_check_environment_vars_failure(self, mock_exit):
        check_environment_vars(['TEST_VAR'])
        mock_exit.assert_called_once_with(2)

if __name__ == '__main__':
    unittest.main()