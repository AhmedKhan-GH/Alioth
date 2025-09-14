
import logging

from alioth.core.decorators import try_catch

log = logging.getLogger(__name__)
from abc import ABC, abstractmethod
from typing import Any, Optional, Union, Type
from pydantic import BaseModel

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
                       prompt: str = "", system="",
                       schema: Optional[Type[BaseModel]] = None
                       ) -> Union[str, BaseModel]:
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

    # logging tested
    @try_catch(exit_on_error=False, default_return=False, catch_exceptions=ConnectionError)
    def check_connection(self) -> bool:
        log.info(f"{self.__class__.__name__} connection check started")
        result = self._check_connection()
        log.info(f"{self.__class__.__name__} connection check completed: {'OK' if result else 'FAILED'}")
        return result

    @try_catch(exit_on_error=False, default_return=None, catch_exceptions=(ConnectionError, ValueError))
    def set_language_model(self, new_model: str = ""):
        self._system_check()
        self._model_check(new_model)

        if self._language_model == new_model:
            log.info(f"{self.__class__.__name__} language model is already set to {self._language_model}")

        log.info(f"{self.__class__.__name__} setting language model to {new_model}")
        self._language_model = new_model
        log.info(f"{self.__class__.__name__} language model set to {new_model}")

    @try_catch(exit_on_error=False, default_return=None, catch_exceptions=(ConnectionError, ValueError))
    def set_embedding_model(self, new_model: str = ""):
        self._system_check()
        self._model_check(new_model)

        if self._embedding_model == new_model:
            log.info(f"{self.__class__.__name__} embedding model is already set to {self._language_model}")

        log.info(f"{self.__class__.__name__} setting embedding model to {new_model}")
        self._embedding_model = new_model
        log.info(f"{self.__class__.__name__} embedding model set to {new_model}")

    # logging tested
    # success and failure tested
    @try_catch(exit_on_error=False, default_return="", catch_exceptions=(ValueError, ConnectionError))
    def generate_text(self, prompt: str = "", system = "",
                      schema: Optional[Type[BaseModel]] = None) -> Union[str, BaseModel]:
        self._system_check()
        self._model_check()

        if prompt == "":
            raise ValueError(f"{self.__class__.__name__} prompt is missing")

        log.info(f"{self.__class__.__name__} attempting to generate {"structured" if schema else "simple"} text")
        result = self._generate_text(prompt=prompt, system=system, schema=schema)
        log.info(f"{self.__class__.__name__} generated {"structured" if schema else "simple"} text "
                 f"{len(str(result))} characters long")
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

    # functionality tested
    def _model_check(self, model: Optional[str] = None):
        # method defaults to internal check if not given an external specification
        if model is None:
            model = self._language_model

        if model == "":
            raise ValueError(f"{self.__class__.__name__} model is not set")
        #log.info(f"{self.__class__.__name__} model is set to {self._language_model}")

        #log.info(f"{self.__class__.__name__} checking model {model} is available")
        if model not in self._model_list:
            raise ValueError(f"{self.__class__.__name__} model {self._language_model} not available")
        #log.info(f"{self.__class__.__name__} model {self._model} is available")
        return

