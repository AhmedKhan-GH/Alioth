
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

    @try_catch(exit_on_error=False, default_return=None)
    @abstractmethod
    def _check_connection(self) -> bool:
        pass


    @try_catch(exit_on_error=False, default_return=None)
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

    def check_connection(self) -> bool:
        log.info(f"{self.__class__.__name__} connection check started")
        result = self._check_connection()
        log.info(f"{self.__class__.__name__} connection check completed: {'OK' if result else 'FAILED'}")
        return result




