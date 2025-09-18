from alioth.core.connection import *
from alioth.core.vectorclient import VectorClient
import chromadb

# later project, find methods that are common to all client
# providing classes such as the external logging check_connection
# that call internal methods, etc, and put that into some Mixin
# class so that I dont have to keep writing those methods over
# and over again for each provider

class ChromaDBVectorClient(VectorClient):

    def _check_connection(self):
        return check_url_connection("http://localhost:8000/api/v2/heartbeat")

    def _create_client(self):
        self._client = chromadb.HttpClient(host = 'localhost', port = 8000)