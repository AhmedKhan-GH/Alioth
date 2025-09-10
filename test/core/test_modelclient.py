import unittest
from abc import ABC
from io import StringIO
from unittest.mock import patch, Mock
from alioth.core.modelclient import *

class MockModelClient(ModelClient):
    def _check_connection(self):
        return True

    def _create_client(self):
        return Mock()

    def _list_models(self):
        return ["model1", "model2",]

    def _generate_text(self, prompt) -> str:
        return "generated text"

class TestModelClientLogging(unittest.TestCase):
    """Testing base client"""

    def test_generate_text_logging(self):
        client = MockModelClient()
        with self.assertLogs("alioth.core.modelclient", level="INFO") as cm:
            client.generate_text("test prompt")
            self.assertGreater(len(cm.records), 0)

    def test_list_models_logging(self):
        client = MockModelClient()
        with self.assertLogs("alioth.core.modelclient", level="INFO") as cm:
            client.list_models()
            self.assertGreater(len(cm.records), 0)

    def test_check_connection_logging(self):
        client = MockModelClient()
        with self.assertLogs("alioth.core.modelclient", level="INFO") as cm:
            client.check_connection()
            self.assertGreater(len(cm.records), 0)

"""

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

    def test_list_models_populated(self):
        with patch.object(self.client, '_list_models', return_value=["test_model1", "test_model2"]):
            models = self.client.list_models()
            self.assertEqual(models, ["test_model1", "test_model2"])

    def test_list_models_empty(self):
        with patch.object(self.client, '_list_models', return_value=[]):
            self.assertEqual(self.client.list_models(), [])

    def test_create_client_success(self):
        Test successful client creation during initialization
        mock_client_object = Mock()  # Create a mock client object

        with patch.object(self.client, '_check_connection', return_value=True):
            with patch.object(self.client, '_create_client', return_value=mock_client_object):
                # Call the method that actually uses _create_client
                self.client._initialize_connection()

                # Verify the client was properly set and connected
                self.assertEqual(self.client._client, mock_client_object)
                self.assertTrue(self.client._connected)

    def test_create_client_failure(self):
        Test client creation failure (returns None) during initialization
        with patch.object(self.client, '_check_connection', return_value=True):
            with patch.object(self.client, '_create_client', return_value=None):
                # This should fail because _create_client returns None
                self.client._initialize_connection()

                # Verify the client was NOT set and connection failed
                self.assertIsNone(self.client._client)
                self.assertFalse(self.client._connected)
    """