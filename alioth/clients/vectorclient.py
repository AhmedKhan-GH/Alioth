import chromadb

from abc import ABC, abstractmethod
import logging
from alioth.core.clientmixin import (ClientMixin)

log = logging.getLogger(__name__)


class VectorClient(ClientMixin):
    def __init__(self):
        self._client = None
        self._connected = False

        self._initialize_connection()
        pass

    @abstractmethod
    def _check_connection(self):
        pass

