import logging
from abc import ABC, abstractmethod

log = logging.getLogger(__name__)

class DatabaseClient(ABC):

    @abstractmethod
    def _check_connection(self):
        pass

    def check_connection(self) -> bool:
        log.info(f"{self.__class__.__name__} connection check started")
        result = self._check_connection()
        log.info(f"{self.__class__.__name__} connection check completed: {'OK' if result else 'FAILED'}")
        return result

    # need to create a method that initializes our central database
    # if it does not already exist, but use it if it already does
    # there needs to be some mechanism to ensure that the database
    # was one that we explicitly created before instead of it being
    # user created and potentially harboring a malicious payload
