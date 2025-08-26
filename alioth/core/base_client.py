
import logging
log = logging.getLogger(__name__)
from abc import ABC, abstractmethod
from typing import Any, Optional

class BaseClient(ABC):
    """Base class for all AI client providers."""

    def __init(self):
        self._client = None

    @abstractmethod
    def _check_connection(self) -> bool:
        pass

    def check_connection(self) -> bool:
        log.info(f"{self.__class__.__name__} connection check started")
        result = self._check_connection()
        log.info(f"{self.__class__.__name__} connection check completed: {'OK' if result else 'FAILED'}")
        return result


