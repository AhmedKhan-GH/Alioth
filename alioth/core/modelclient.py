
import logging

from alioth.core.decorators import try_catch

log = logging.getLogger(__name__)
from abc import ABC, abstractmethod
from typing import Any, Optional, Union, Type
from pydantic import BaseModel

class ModelClient(ABC):
    """Base class for all AI client providers."""

    def __init__(self, model: str = ""):        # we initialize our initial state
        self._model = model

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
    def _generate_text(self, prompt: str = "", system="",
                       schema: Optional[Type[BaseModel]] = None) -> Union[str, BaseModel]:
        pass


    # logging tested
    # success and failure tested
    @try_catch(exit_on_error=False, default_return = False, catch_exceptions=ConnectionError)
    def _initialize_connection(self) -> Any:
        # if connection does not return false we can create a client
        if not self._check_connection():
            raise ConnectionError(f"{self.__class__.__name__} connection check failed")
        self._client = self._create_client()
        log.info(f"{self.__class__.__name__} connection check successful")
        # if connection fails then we never set _client away from None

        # if client does not return null object we are connected
        if self._client is None:
            raise ConnectionError(f"{self.__class__.__name__} client creation failed")
        self._connected = True
        log.info(f"{self.__class__.__name__} client creation successful")

        self._model_list = self._list_models()
        # if client creation fails then we never set _connected = true

        # if all code is successful then only do we change our state to
        # _connected = True and _client = a client object

# == ABSTRACTED INTERFACE ==

    # logging tested
    @try_catch(exit_on_error=False, default_return=False, catch_exceptions=ConnectionError)
    def check_connection(self) -> bool:
        log.info(f"{self.__class__.__name__} connection check started")
        result = self._check_connection()
        log.info(f"{self.__class__.__name__} connection check completed: {'OK' if result else 'FAILED'}")
        return result

    @try_catch(exit_on_error=False, default_return=None, catch_exceptions=(ConnectionError, ValueError))
    def set_model(self, new_model: str = ""):
        self._system_check()
        self._model_check(new_model)

        if self._model == new_model:
            log.info(f"{self.__class__.__name__} model is already set to {self._model}")

        log.info(f"{self.__class__.__name__} setting model to {new_model}")
        self._model = new_model
        log.info(f"{self.__class__.__name__} model set to {new_model}")

    # logging tested
    # success and failure tested
    @try_catch(exit_on_error=False, default_return="", catch_exceptions=(ValueError, ConnectionError))
    def generate_text(self, prompt: str = "", system="",
                      schema: Optional[Type[BaseModel]] = None) -> Union[str, BaseModel]:
        self._system_check()
        self._model_check()

        if prompt == "":
            raise ValueError(f"{self.__class__.__name__} prompt is missing")

        log.info(f"{self.__class__.__name__} attempting to generate text")
        result = self._generate_text(prompt, system, schema=schema)
        log.info(f"{self.__class__.__name__} generated text: {len(str(result))}")
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
    def _model_check(self, model: str = None):
        # method defaults to internal check if not given an external specification
        if model is None:
            model = self._model

        if model == "":
            raise ValueError(f"{self.__class__.__name__} model is not set")
        #log.info(f"{self.__class__.__name__} model is set to {self._model}")

        #log.info(f"{self.__class__.__name__} checking model {model} is available")
        if model not in self._model_list:
            raise ValueError(f"{self.__class__.__name__} model {self._model} not available")
        #log.info(f"{self.__class__.__name__} model {self._model} is available")
        return

