
import logging

from alioth.core.decorators import try_catch

log = logging.getLogger(__name__)
from abc import ABC, abstractmethod
from typing import Any, Optional

class ModelClient(ABC):
    """Base class for all AI client providers."""

    def __init__(self, model = None):
        self._model = model

        # we initialize our initial state
        self._client = None
        self._connected = False

        # we attempt to change our state
        self._initialize_connection()

    @try_catch(exit_on_error=False, default_return=None)
    @abstractmethod
    def _check_connection(self) -> bool:
        pass

    @try_catch(exit_on_error=False, default_return=[])
    @abstractmethod
    def _list_models(self) -> list:
        pass

    @try_catch(exit_on_error=False, default_return=None)
    @abstractmethod
    def _create_client(self) -> Any:
        pass

    @try_catch(exit_on_error=False, default_return="")
    @abstractmethod
    def _generate_text(self, prompt) -> str:
        pass


    @try_catch(exit_on_error=False, default_return = False, catch_exceptions=(Exception, ConnectionError))
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
        # if client creation fails then we never set _connected = true

        # if all code is successful then only do we change our state to
        # _connected = True and _client = a client object

    # logging tested
    def check_connection(self) -> bool:
        log.info(f"{self.__class__.__name__} connection check started")
        result = self._check_connection()
        log.info(f"{self.__class__.__name__} connection check completed: {'OK' if result else 'FAILED'}")
        return result

    # logging tested
    @try_catch(exit_on_error=False, default_return=None, catch_exceptions=(ValueError, ConnectionError))
    def generate_text(self, prompt) -> str:
        if not self._connected:
            raise ConnectionError(f"{self.__class__.__name__} is not connected")
        if not self._client:
            raise ConnectionError(f"{self.__class__.__name__} client is not initialized")
        if not self._model:
            raise ValueError(f"{self.__class__.__name__} model is not set")

        log.info(f"{self.__class__.__name__} attempting to generate text")
        result = self._generate_text(prompt)
        log.info(f"{self.__class__.__name__} generated text with {len(result)} characters")
        return result

    # logging tested
    def list_models(self) -> list:
        log.info(f"{self.__class__.__name__} retrieving list of models")
        models = self._list_models()
        log.info(f"{self.__class__.__name__} found {len(models)} models")
        return models



