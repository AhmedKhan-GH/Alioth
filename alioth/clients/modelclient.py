import logging

from alioth.core.decorators import try_catch

log = logging.getLogger(__name__)
from abc import ABC, abstractmethod
from typing import Any, Optional, Union, Type
from pydantic import BaseModel
from enum import Enum, auto


class ModelType(Enum):
    EMBEDDING = auto(),
    LANGUAGE = auto()


class ModelClient(ABC):
    """Base class for all AI clients providers."""

    # == INITIALIZATION METHODS ==

    def __init__(self, language_model: Optional[str] = None,
                 embedding_model: Optional[str] = None):  # we initialize our initial state
        self._language_model = language_model
        self._embedding_model = embedding_model

        self._client = None
        self._connected = False

        self._model_list = []

        # we attempt to change our state
        self._initialize_connection()

    @try_catch(exit_on_error=False, default_return=False, catch_exceptions=ConnectionError)
    def _initialize_connection(self) -> Any:
        # connection check guard clause
        if self._check_connection():
            log.info(f"{self.__class__.__name__} connection check successful")
        else:
            raise ConnectionError(f"{self.__class__.__name__} connection check failed")

        self._client = self._create_client()

        # if clients does not return null object we are connected
        if self._client:
            log.info(f"{self.__class__.__name__} clients creation successful")
        else:
            raise ConnectionError(f"{self.__class__.__name__} clients creation failed")

        self._connected = True

        # given we have created a clients and connected we can capture a model list
        self._model_list = self._list_models()

        # if all code is successful then only do we change our state to
        # _connected = True and _client = a clients object and they are
        # tightly coupled

    # == ABSTRACT METHODS ==

    @try_catch(exit_on_error=False, default_return=False)
    @abstractmethod
    def _check_connection(self) -> bool:
        pass

    @try_catch(exit_on_error=False, default_return=[])
    @abstractmethod
    def _list_models(self) -> list[str]:
        pass

    @try_catch(exit_on_error=False, default_return=None)
    @abstractmethod
    def _create_client(self) -> Any:
        pass

    @try_catch(exit_on_error=False, default_return="")
    @abstractmethod
    def _generate_text(self, prompt: Optional[str] = None, system: Optional[str] = None,
                       schema: Optional[Type[BaseModel]] = None) -> Union[str, BaseModel]:
        pass

    @try_catch(exit_on_error=False, default_return=None)
    @abstractmethod
    def _embed_text(self, prompt: Union[str, list[str]]) -> Union[list[float], list[list[float]]]:
        pass

    # == PUBLIC INTERFACE ==

    @try_catch(exit_on_error=False, default_return=False)
    def check_connection(self) -> bool:
        log.info(f"{self.__class__.__name__} connection check started")
        result = self._check_connection()
        log.info(f"{self.__class__.__name__} connection check completed: {'OK' if result else 'FAILED'}")
        return result

    @try_catch(exit_on_error=False, default_return=[])
    def list_models(self) -> list:
        log.info(f"{self.__class__.__name__} retrieving list of models")
        models = self._list_models()
        log.info(f"{self.__class__.__name__} found {len(models)} models")
        return models

    @try_catch(exit_on_error=False, default_return=None, catch_exceptions=ValueError)
    def set_embedding_model(self, embedding_model: Optional[str] = None):
        log.info(f"{self.__class__.__name__} setting embedding model to {embedding_model}")
        self._set_model(embedding_model, ModelType.EMBEDDING)
        log.info(f"{self.__class__.__name__} embedding model set to {embedding_model}")

    @try_catch(exit_on_error=False, default_return=None, catch_exceptions=ValueError)
    def set_language_model(self, language_model: Optional[str] = None):
        log.info(f"{self.__class__.__name__} setting language model to {language_model}")
        self._set_model(language_model, ModelType.LANGUAGE)
        log.info(f"{self.__class__.__name__} language model set to {language_model}")

    # logging tested
    # success and failure tested
    @try_catch(exit_on_error=False, default_return="", catch_exceptions=(ValueError, ConnectionError))
    def generate_text(self, prompt: str = "", system="",
                      schema: Optional[Type[BaseModel]] = None) -> Union[str, BaseModel]:

        self._check_system()
        self._check_model(model_type=ModelType.LANGUAGE)

        if prompt == "":
            raise ValueError(f"{self.__class__.__name__} prompt is missing")

        log.info(f"{self.__class__.__name__} attempting to generate {"structured" if schema else "simple"} text")
        result = self._generate_text(prompt=prompt, system=system, schema=schema)
        log.info(f"{self.__class__.__name__} generated {"structured" if schema else "simple"} text "
                 f"{len(str(result))} characters long")
        return result

    @try_catch(exit_on_error=False, default_return=[], catch_exceptions=(ValueError, ConnectionError))
    def embed_text(self, text: Union[str, list[str]]) -> Union[list[float], list[list[float]]]:

        self._check_system()
        self._check_model(model_type=ModelType.EMBEDDING)

        if text == "":
            raise ValueError(f"{self.__class__.__name__} text is missing")

        log.info(f"{self.__class__.__name__} attempting to embed text")
        result = self._embed_text(prompt=text)
        log.info(f"{self.__class__.__name__} successfully embedded text")
        return result

    # == INTERNAL HELPER FUNCTIONS ==
    # no try catch as they are meant to raise errors to their parent functions

    def _check_system(self):
        if not self._connected:
            raise ConnectionError(f"{self.__class__.__name__} is not connected")
        # log.info(f"{self.__class__.__name__} is connected")
        if self._client is None:
            return ConnectionError(f"{self.__class__.__name__} clients is not initialized")
        # log.info(f"{self.__class__.__name__} clients is initialized")
        return None

    def _check_type(self, model_type: ModelType):
        if model_type is None:
            raise ValueError(f"{self.__class__.__name__} model type is missing")
        if model_type not in ModelType:
            raise ValueError(f"{self.__class__.__name__} model type {type} not supported")

    def _check_model(self, model_name: Optional[str] = None, model_type: Optional[ModelType] = None):
        self._check_type(model_type)
        # if given no parameter default to internal parameter
        if model_name is None:
            if model_type == ModelType.EMBEDDING:
                model_name = self._embedding_model
            elif model_type == ModelType.LANGUAGE:
                model_name = self._language_model

        # if internal model is none
        if model_name is None or model_name == "":
            raise ValueError(f"{self.__class__.__name__} model is missing")
        # if it is still empty string or none then we raise an error
        if model_name not in self._model_list:
            raise ValueError(f"{self.__class__.__name__} model {model_name} not available")
        # if we have specified a model that is missing also raise an error
        log.info(f"{self.__class__.__name__} model {model_name} found")

    def _set_model(self, model_name: Optional[str] = None,
                   model_type: ModelType = None):

        self._check_type(model_type)
        self._check_model(model_name=model_name, model_type=model_type)

        if model_type == ModelType.EMBEDDING:
            self._embedding_model = model_name
        elif model_type == ModelType.LANGUAGE:
            self._language_model = model_name
