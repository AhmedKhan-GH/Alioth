
import logging

from alioth.core.decorators import try_catch

log = logging.getLogger(__name__)
from abc import ABC, abstractmethod
from typing import Any, Optional

class BaseClient(ABC):
    """Base class for all AI client providers."""

    def __init__(self):
        self._client = None
        self._connected = False
        self._initialize_connection()

    # tested
    @abstractmethod
    def _check_connection(self) -> bool:
        pass

    @abstractmethod
    def _create_client(self) -> Any:
        pass

    # tested
    @try_catch(exit_on_error=False, default_return = False, catch_exceptions=(Exception, ConnectionError))
    def _initialize_connection(self) -> Any:
        if not self._check_connection():
            raise ConnectionError(f"{self.__class__.__name__} connection check failed")
        self._client = self._create_client()
        if self._client is None:
            raise ConnectionError(f"{self.__class__.__name__} client creation failed")
        self._connected = True
        return True

    @try_catch(exit_on_error=False, catch_exceptions=(Exception, ConnectionError))
    def _ensure_connection(self):
        """Ensure connection to the client provider during runtime."""
        if not self.check_connection():
            log.warning(f"{self.__class__.__name__} connection lost, attempting to reconnect")
            self.attempt_connection()

    def check_connection(self) -> bool:
        log.info(f"{self.__class__.__name__} connection check started")
        result = self._check_connection()
        log.info(f"{self.__class__.__name__} connection check completed: {'OK' if result else 'FAILED'}")
        return result

    def attempt_connection(self):
        self._connected = False
        self._client = None
        return self._initialize_connection()
"""
    def get_available_models(self) -> list[str]:
        log.info(f"{self.__class__.__name__} getting available models")
        models = self._get_available_models()
        log.info(f"{self.__class__.__name__} found {len(models)} models")
        return models
"""




