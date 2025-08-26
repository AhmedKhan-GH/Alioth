import unittest
from unittest.mock import patch, Mock
from alioth.core.base_client import *

class MockClient(BaseClient):
    def _check_connection(self):
        pass

    def _create_client(self):
        pass

class TestBaseClient(unittest.TestCase):
    """Testing base client"""

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def setUp(self):
        self.client = MockClient.__new__(MockClient)
        self.client._client = None
        self.client._connected = False

    def test_check_connection_success(self):
        with patch.object(self.client, '_check_connection', return_value=True) as mock_check_connection:
            result = self.client.check_connection()
            mock_check_connection.assert_called_once()
            self.assertTrue(result)

    def test_check_connection_failure(self):
        with patch.object(self.client, '_check_connection', return_value=False) as mock_check_connection:
            result = self.client.check_connection()
            mock_check_connection.assert_called_once()
            self.assertFalse(result)

    def test_initialize_connection_success(self):
        with patch.object(self.client, '_check_connection', return_value=True):
            with patch.object(self.client, '_create_client', return_value="test_client"):
                self.client._initialize_connection()
                self.assertEqual(self.client._client, "test_client")
                self.assertTrue(self.client._connected)

    def test_initialize_connection_failure(self):
        with patch.object(self.client, '_check_connection', return_value=False):
            with patch.object(self.client, '_create_client', return_value=None):
                self.client._initialize_connection()
                self.assertNotEqual(self.client._client, "test_client")
                self.assertFalse(self.client._connected)
