
import logging

from openai.types import embedding_model

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
    """Base class for all AI client providers."""

    def __init__(self,
                 language_model: Optional[str] = None,
                 embedding_model: Optional[str] = None):        # we initialize our initial state
        self._language_model = language_model
        self._embedding_model = embedding_model

        self._client = None
        self._connected = False

        self._model_list = []

        # we attempt to change our state
        self._initialize_connection()

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
    def _generate_text(self,
                       prompt: Optional[str] = None,
                       system: Optional[str] = None,
                       schema: Optional[Type[BaseModel]] = None
                       ) -> Union[str, BaseModel]:
        pass

    @try_catch(exit_on_error=False, default_return=None)
    @abstractmethod
    def _embed_text(self, prompt: Union[str, list[str]]) -> Union[list[float], list[list[float]]]:
        pass


    # logging tested
    # success and failure tested
    @try_catch(exit_on_error=False, default_return = False, catch_exceptions=ConnectionError)
    def _initialize_connection(self) -> Any:

        # connection check guard clause
        if self._check_connection():
            log.info(f"{self.__class__.__name__} connection check successful")
        else:
            raise ConnectionError(f"{self.__class__.__name__} connection check failed")

        self._client = self._create_client()

        # if client does not return null object we are connected
        if self._client:
            log.info(f"{self.__class__.__name__} client creation successful")
        else:
            raise ConnectionError(f"{self.__class__.__name__} client creation failed")

        self._connected = True

        # given we have created a client and connected we can capture a model list
        self._model_list = self._list_models()

        # if all code is successful then only do we change our state to
        # _connected = True and _client = a client object and they are
        # tightly coupled

# == ABSTRACTED INTERFACE ==

    def check_connection(self) -> bool:
        log.info(f"{self.__class__.__name__} connection check started")
        result = self._check_connection()
        log.info(f"{self.__class__.__name__} connection check completed: {'OK' if result else 'FAILED'}")
        return result

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
    def generate_text(self, prompt: str = "", system = "",
                      schema: Optional[Type[BaseModel]] = None) -> Union[str, BaseModel]:

        self._system_check()
        self._check_language_model()

        if prompt == "":
            raise ValueError(f"{self.__class__.__name__} prompt is missing")

        log.info(f"{self.__class__.__name__} attempting to generate {"structured" if schema else "simple"} text")
        result = self._generate_text(prompt=prompt, system=system, schema=schema)
        log.info(f"{self.__class__.__name__} generated {"structured" if schema else "simple"} text "
                 f"{len(str(result))} characters long")
        return result

    @try_catch(exit_on_error=False, default_return=[], catch_exceptions=(ValueError, ConnectionError))
    def embed_text(self, text: Union[str, list[str]]) -> Union[list[float], list[list[float]]]:
        self._system_check()
        self._check_embedding_model()

        if text == "":
            raise ValueError(f"{self.__class__.__name__} text is missing")

        log.info(f"{self.__class__.__name__} attempting to embed text")
        result = self._embed_text(prompt=text)
        log.info(f"{self.__class__.__name__} successfully embedded text")
        return result

    # logging tested
    def list_models(self) -> list:
        log.info(f"{self.__class__.__name__} retrieving list of models")
        models = self._list_models()
        log.info(f"{self.__class__.__name__} found {len(models)} models")
        return models

# === INTERNAL HELPER FUNCTIONS ==

    # functionality tested
    def _system_check(self):
        if not self._connected:
            raise ConnectionError(f"{self.__class__.__name__} is not connected")
        #log.info(f"{self.__class__.__name__} is connected")
        if self._client is None:
            return ConnectionError(f"{self.__class__.__name__} client is not initialized")
        #log.info(f"{self.__class__.__name__} client is initialized")
        return None

    def _type_check(self, type: ModelType):
        if type is None:
            raise ValueError(f"{self.__class__.__name__} model type is missing")
        if type not in ModelType:
            raise ValueError(f"{self.__class__.__name__} model type {type} not supported")

    def _model_check(self, model: Optional[str] = None,
                     type: Optional[ModelType] = None):

        self._type_check(type)
        # if given no parameter default to internal parameter

        if model is None:
            if type == ModelType.EMBEDDING:
                model = self._embedding_model
            elif type == ModelType.LANGUAGE:
                model = self._language_model

        if model is None or model == "":
            raise ValueError(f"{self.__class__.__name__} model is missing")
        # if it is still empty string or none then we raise an error

        if model not in self._model_list:
            raise ValueError(f"{self.__class__.__name__} model {model} not available")
        # if we have specified a model that is missing also raise an error

    def _set_model(self, candidate: Optional[str] = None,
                   type: ModelType = None):

        self._type_check(type)

        self._model_check(model = candidate, type = type)

        if type == ModelType.EMBEDDING:
            self._embedding_model = candidate
        elif type == ModelType.LANGUAGE:
            self._language_model = candidate

    def _check_embedding_model(self, embedding_model: Optional[str] = None):
        log.info(f"{self.__class__.__name__} checking embedding model {embedding_model}")
        self._model_check(embedding_model, ModelType.EMBEDDING)
        log.info(f"{self.__class__.__name__} embedding model {embedding_model} is available")

    def _check_language_model(self, language_model: Optional[str] = None):
        log.info(f"{self.__class__.__name__} checking language model {language_model}")
        self._model_check(language_model, ModelType.LANGUAGE)
        log.info(f"{self.__class__.__name__} language model {language_model} is available")
