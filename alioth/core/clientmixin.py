from abc import ABC, abstractmethod
from alioth.core.decorators import try_catch
import logging

log = logging.getLogger(__name__)

class ClientMixin(ABC):

    @try_catch(exit_on_error=False, default_return=False, catch_exceptions=ConnectionError)
    def _initialize_connection(self):
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

    def check_connection(self) -> bool:
        log.info(f"{self.__class__.__name__} connection check started")
        result = self._check_connection()
        log.info(f"{self.__class__.__name__} connection check completed: {'OK' if result else 'FAILED'}")
        return result

    @abstractmethod
    def _check_connection(self):
        pass

    @abstractmethod
    def _create_client(self):
        pass

