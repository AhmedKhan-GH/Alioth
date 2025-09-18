import chromadb

from abc import ABC, abstractmethod
import logging

log = logging.getLogger(__name__)

class VectorClient(ABC):
    def __init__(self):
        self.check_connection()
        pass

    @abstractmethod
    def _check_connection(self):
        pass

    def check_connection(self) -> bool:
        log.info(f"{self.__class__.__name__} connection check started")
        result = self._check_connection()
        log.info(f"{self.__class__.__name__} connection check completed: {'OK' if result else 'FAILED'}")
        return result
