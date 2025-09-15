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

    def _embed_text(self, prompt: str) -> list[float]:
        return [1.1]

    def _generate_text(self,
                       prompt: str = "", system = "",
                       schema: Type[Optional[BaseModel]] = None
                       ) -> Union[BaseModel, str]:

        class Test(BaseModel):
            test_field: str

        output = "generated text"
        if not system == "":
            output = system + "\n" + output

        if schema:
            return Test(test_field = output)

        return output

class TestModelClientLogging(unittest.TestCase):
    """Testing base client"""

    def test_generate_text_logging(self):
        client = MockModelClient(language_model = "test_model1")
        with self.assertLogs("alioth.core.modelclient", level="INFO") as cm:
            client.generate_text("test prompt")
            self.assertGreater(len(cm.records), 0)

    def test_list_models_logging(self):
        client = MockModelClient(language_model = "test_model1")
        with self.assertLogs("alioth.core.modelclient", level="INFO") as cm:
            client.list_models()
            self.assertGreater(len(cm.records), 0)

    def test_check_connection_logging(self):
        client = MockModelClient(language_model = "test_model1")
        with self.assertLogs("alioth.core.modelclient", level="INFO") as cm:
            client.check_connection()
            self.assertGreater(len(cm.records), 0)

    def test_initialize_connection_logging(self):
        client = MockModelClient(language_model = "test_model1")
        with self.assertLogs("alioth.core.modelclient", level="INFO") as cm:
            client._initialize_connection()
            self.assertGreater(len(cm.records), 0)

class TestModelClientInitialization(unittest.TestCase):
    def test_initialize_connection_success(self):
        client = MockModelClient(language_model = "test_model1")
        self.assertTrue(client._connected)
        self.assertIsNotNone(client._client)

    def test_initialize_connection_failure(self):
        with patch.object(MockModelClient,'_check_connection', return_value=False):
            client = MockModelClient(language_model = "test_model1")
            self.assertFalse(client._connected)
            self.assertIsNone(client._client)

    def test_client_creation_failure(self):
        with patch.object(MockModelClient,'_create_client', return_value=None):
            client = MockModelClient(language_model = "test_model1")
            self.assertFalse(client._connected)
            self.assertIsNone(client._client)

class TestModelClientGenerateText(unittest.TestCase):
    def test_generate_text_success(self):
        client = MockModelClient(language_model = "test_model1")
        result = client.generate_text("test prompt")
        self.assertEqual(result, "generated text")

    def test_generate_text_no_language_model(self):
        client = MockModelClient(language_model = "")
        result = client.generate_text("test prompt")
        self.assertEqual(result, "")

    def test_generate_text_missing_language_model(self):
        client = MockModelClient(language_model = "missing_model")
        result = client.generate_text("test prompt")
        self.assertEqual(result, "")

    def test_generate_text_missing_prompt(self):
        client = MockModelClient(language_model = "test_model1")
        result = client.generate_text("")
        self.assertEqual(result, "")

    def test_generate_text_structured(self):
        class Test(BaseModel):
            test_field: str

        client = MockModelClient(language_model = "test_model1")
        result = client.generate_text("test prompt", schema=Test)

        self.assertIsInstance(result.test_field, str)

    def test_generate_text_system_prompt(self):
        client = MockModelClient(language_model = "test_model1")
        result = client.generate_text(prompt ="test prompt", system="test system prompt")
        self.assertEqual(result, "test system prompt\ngenerated text")

class TestModelClientListModels(unittest.TestCase):
    def test_list_models_success(self):
        client = MockModelClient(language_model = "test_model1")
        result = client.list_models()
        self.assertEqual(result, ["test_model1", "test_model2"])

    def test_list_models_no_model(self):
        with patch.object(MockModelClient,'_list_models', return_value=[]):
            client = MockModelClient(language_model = "test_model1")
            result = client.list_models()
            self.assertEqual(result, [])

class TestModelClientHealthCheck(unittest.TestCase):
    def test_system_check_success(self):
        client = MockModelClient(language_model = "test_model1")
        client._system_check()

    def test_system_check_connection_failure(self):
        with patch.object(MockModelClient,'_check_connection', return_value=False):
            client = MockModelClient(language_model = "test_model1")
            with self.assertRaises(ConnectionError):
                client._system_check()

    def test_system_check_client_failure(self):
        with patch.object(MockModelClient,'_create_client', return_value=None):
            client = MockModelClient(language_model = "test_model1")
            with self.assertRaises(ConnectionError):
                client._system_check()

class TestModelClientModelCheck(unittest.TestCase):
    def test_model_check_language_model_success(self):
        client = MockModelClient(language_model = "test_model1")
        client._model_check(type = ModelType.LANGUAGE)

    def test_model_check_missing_language_model(self):
        client = MockModelClient(language_model = "missing_model")
        with self.assertRaises(ValueError):
            client._model_check(type = ModelType.LANGUAGE)

    def test_model_check_missing_embedding_model(self):
        client = MockModelClient(embedding_model = "missing_model")
        with self.assertRaises(ValueError):
            client._model_check(type = ModelType.EMBEDDING)

    def test_model_check_embedding_model_success(self):
        client = MockModelClient(embedding_model = "test_model1")
        client._model_check(type = ModelType.EMBEDDING)

    def test_model_check_no_model(self):
        client = MockModelClient()
        with self.assertRaises(ValueError):
            client._model_check()

class TestModelClientSetLanguageModel(unittest.TestCase):
    def test_set_language_model_success(self):
        client = MockModelClient(language_model = "test_model1")
        client.set_language_model("test_model2")
        self.assertEqual("test_model2", client._language_model)

    def test_set_language_model_no_model(self):
        client = MockModelClient(language_model = "test_model1")
        client.set_language_model("")
        self.assertEqual("test_model1", client._language_model)

    def test_set_language_model_missing_model(self):
        client = MockModelClient(language_model = "test_model1")
        client.set_language_model("missing_model")
        self.assertEqual("test_model1", client._language_model)

    def test_set_language_model_same_model(self):
        client = MockModelClient(language_model = "test_model1")
        client.set_language_model("test_model1")
        self.assertEqual("test_model1", client._language_model)

class TestModelClientSetEmbeddingModel(unittest.TestCase):
    def test_set_embedding_model_success(self):
        client = MockModelClient(embedding_model = "test_model1")
        client.set_embedding_model("test_model2")
        self.assertEqual("test_model2", client._embedding_model)

    def test_set_embedding_model_no_model(self):
        client = MockModelClient(embedding_model = "test_model1")
        client.set_embedding_model("")
        self.assertEqual("test_model1", client._embedding_model)

    def test_set_embedding_model_missing_model(self):
        client = MockModelClient(embedding_model = "test_model1")
        client.set_embedding_model("missing_model")
        self.assertEqual("test_model1", client._embedding_model)

    def test_set_embedding_model_same_model(self):
        client = MockModelClient(embedding_model = "test_model1")
        client.set_embedding_model("test_model1")
        self.assertEqual("test_model1", client._embedding_model)

class TestModelClientEmbedText(unittest.TestCase):
    def test_embed_text_success(self):
        client = MockModelClient(embedding_model = "test_model1")
        result = client.embed_text("test prompt")
        self.assertEqual([1.1], result)

    def test_embed_text_no_embedding_model(self):
        client = MockModelClient()
        result = client.embed_text("test prompt")
        self.assertEqual(result, [])

    def test_embed_text_missing_embedding_model(self):
        client = MockModelClient(embedding_model = "missing_model")
        result = client.embed_text("test prompt")
        self.assertEqual(result, [])

    def test_embed_text_no_prompt(self):
        client = MockModelClient(embedding_model = "test_model1")
        result = client.embed_text("")
        self.assertEqual(result, [])

