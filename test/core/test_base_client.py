import unittest
from unittest.mock import patch, Mock
from alioth.core.base_client import *

class TestBaseClient(unittest.TestCase):
    """Testing base client"""

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def setUp(self):
        self.client = Mock(spec=BaseClient)
        self.client.__class__.__name__ = "MockClient"
        self.client.check_connection = BaseClient.check_connection.__get__(self.client)

    def test_check_connection_calls_abstract_method(self):
        with patch.object(self.client, '_check_connection', return_value=True) as mock_check_connection:
            result = self.client.check_connection()
            mock_check_connection.assert_called_once()
            self.assertTrue(result)