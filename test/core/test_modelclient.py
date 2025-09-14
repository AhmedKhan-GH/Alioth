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
        return ["test_model1", "test_model2"]

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
        client = MockModelClient(model = "test_model1")
        with self.assertLogs("alioth.core.modelclient", level="INFO") as cm:
            client.list_models()
            self.assertGreater(len(cm.records), 0)

    def test_check_connection_logging(self):
        client = MockModelClient(model = "test_model1")
        with self.assertLogs("alioth.core.modelclient", level="INFO") as cm:
            client.check_connection()
            self.assertGreater(len(cm.records), 0)

    def test_initialize_connection_logging(self):
        client = MockModelClient(model = "test_model1")
        with self.assertLogs("alioth.core.modelclient", level="INFO") as cm:
            client._initialize_connection()
            self.assertGreater(len(cm.records), 0)

class TestModelClientInitialization(unittest.TestCase):
    def test_initialize_connection_success(self):
        client = MockModelClient(model = "test_model1")
        self.assertTrue(client._connected)
        self.assertIsNotNone(client._client)

    def test_initialize_connection_failure(self):
        with patch.object(MockModelClient,'_check_connection', return_value=False):
            client = MockModelClient(model = "test_model1")
            self.assertFalse(client._connected)
            self.assertIsNone(client._client)

    def test_client_creation_failure(self):
        with patch.object(MockModelClient,'_create_client', return_value=None):
            client = MockModelClient(model = "test_model1")
            self.assertFalse(client._connected)
            self.assertIsNone(client._client)

class TestModelClientGenerateText(unittest.TestCase):
    def test_generate_text_success(self):
        client = MockModelClient(model = "test_model1")
        result = client.generate_text("test prompt")
        self.assertEqual(result, "generated text")

    def test_generate_text_no_model(self):
        client = MockModelClient(model = "")
        result = client.generate_text("test prompt")
        self.assertEqual(result, "")

    def test_generate_text_missing_model(self):
        client = MockModelClient(model = "missing_model")
        result = client.generate_text("test prompt")
        self.assertEqual(result, "")

    def test_generate_text_missing_prompt(self):
        client = MockModelClient(model = "test_model1")
        result = client.generate_text("")
        self.assertEqual(result, "")

class TestModelClientListModels(unittest.TestCase):
    def test_list_models_success(self):
        client = MockModelClient(model = "test_model1")
        result = client.list_models()
        self.assertEqual(result, ["test_model1", "test_model2"])

    def test_list_models_no_model(self):
        with patch.object(MockModelClient,'_list_models', return_value=[]):
            client = MockModelClient(model = "test_model1")
            result = client.list_models()
            self.assertEqual(result, [])

class TestModelClientHealthCheck(unittest.TestCase):
    def test_system_check_success(self):
        client = MockModelClient(model = "test_model1")
        client._system_check()

    def test_system_check_connection_failure(self):
        with patch.object(MockModelClient,'_check_connection', return_value=False):
            client = MockModelClient(model = "test_model1")
            with self.assertRaises(ConnectionError):
                client._system_check()

    def test_system_check_client_failure(self):
        with patch.object(MockModelClient,'_create_client', return_value=None):
            client = MockModelClient(model = "test_model1")
            with self.assertRaises(ConnectionError):
                client._system_check()

class TestModelClientModelCheck(unittest.TestCase):
    def test_model_check_success(self):
        client = MockModelClient(model = "test_model1")
        client._model_check()

    def test_model_check_missing_model(self):
        client = MockModelClient(model = "missing_model")
        with self.assertRaises(ValueError):
            client._model_check()

    def test_model_check_no_model(self):
        client = MockModelClient()
        with self.assertRaises(ValueError):
            client._model_check()

class TestModelClientSetModel(unittest.TestCase):
    def test_set_model_success(self):
        client = MockModelClient(model = "test_model1")
        client.set_model("test_model2")
        self.assertEqual(client._model, "test_model2")

    def test_set_model_no_model(self):
        client = MockModelClient(model = "test_model1")
        client.set_model("")
        self.assertEqual(client._model, "test_model1")

    def test_set_model_missing_model(self):
        client = MockModelClient(model = "test_model1")
        client.set_model("missing_model")
        self.assertEqual(client._model, "test_model1")

    def test_set_model_same_model(self):
        client = MockModelClient(model = "test_model1")
        client.set_model("test_model1")
        self.assertEqual(client._model, "test_model1")

