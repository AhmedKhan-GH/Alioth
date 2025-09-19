import logging
from abc import ABC, abstractmethod
from alioth.core.decorators import try_catch
from alioth.core.clientmixin import ClientMixin

log = logging.getLogger(__name__)

class DatabaseClient(ClientMixin):

    @abstractmethod
    def _check_connection(self):
        pass

    @abstractmethod
    def _create_client(self):
        pass


    def __init__(self):
        self._client = None
        self._connected = False

        self._initialize_connection()

    def __exit__(self):
        self._client.close()

     # need to create a method that initializes our central database
    # if it does not already exist, but use it if it already does
    # there needs to be some mechanism to ensure that the database
    # was one that we explicitly created before instead of it being
    # user created and potentially harboring a malicious payload
