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

    def test_check_filesystem_access_success(self):
        check_filesystem_access()

    @patch('tempfile.NamedTemporaryFile', side_effect=OSError())
    @patch('sys.exit')
    def test_check_filesystem_access_failure(self, mock_exit, mock_tempfile):
        check_filesystem_access()
        mock_exit.assert_called_once_with(2)

    @patch('os.remove', side_effect=IOError())
    @patch('sys.exit')
    def check_filesystem_remove_failure(self, mock_exit):
        check_filesystem_access()
        mock_exit.assert_called_once_with(2)

    @patch.dict(os.environ, {'TEST_VAR': 'test_value'}, clear = False)
    def test_get_environment_var_success(self):
        get_environment_variable('TEST_VAR', required = True)


    @patch.dict(os.environ, {}, clear = True)
    @patch('sys.exit')
    def test_get_environment_var_failure(self, mock_exit):
        get_environment_variable('TEST_VAR', required = True)
        mock_exit.assert_called_once_with(2)

if __name__ == '__main__':
    unittest.main()