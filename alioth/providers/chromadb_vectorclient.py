from alioth.core.connection import *
from alioth.clients.vectorclient import VectorClient
import chromadb

#id: chunk_uuid, will refer to the postgres chunks table
#embedding: list[float], will be a vector bound to a certain model
#metadata:
#   file_id: file_uuid, will refer to postgres files table
#   norm_hash: string, a hash of concatenated normalization
#   parameters such as removing newlines, removing headers

class ChromaDBVectorClient(VectorClient):

    def _check_connection(self):
        return check_url_connection("http://localhost:8000/api/v2/heartbeat")

    def _create_client(self):
        self._client = chromadb.HttpClient(host = 'localhost', port = 8000)