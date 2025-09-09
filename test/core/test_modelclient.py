import unittest
from abc import ABC
from unittest.mock import patch, Mock
from alioth.core.modelclient import *

class MockClient(ModelClient):
    def _check_connection(self):
        pass

    def _create_client(self):
        pass

    def _list_models(self):
        pass

    def _generate_text(self, prompt) -> str:
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

    def test_list_models(self):
        with patch.object(self.client, '_list_models', return_value=["test_model1", "test_model2"]):
            models = self.client.list_models()
            self.assertEqual(models, ["test_model1", "test_model2"])