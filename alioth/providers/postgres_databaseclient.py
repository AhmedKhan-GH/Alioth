from alioth.clients.databaseclient import DatabaseClient
import psycopg2
from psycopg2 import OperationalError

from alioth.core.decorators import try_catch


class PostgresDatabaseClient(DatabaseClient):
    def __init__(self):
        self._client = None
        self._connected = False

        self._initialize_connection()

    def __exit__(self):
        self._client.close()

    @try_catch(exit_on_error=False, default_return=False, catch_exceptions = OperationalError)
    def _check_connection(self):
        conn = psycopg2.connect(dbname = "postgres",
                                user = "ahmed",
                                host = "localhost",
                                port = "5432")
        cur = conn.cursor()
        cur.execute("SELECT version();")
        result = cur.fetchone()
        cur.close()
        _client = conn
        if result: return True
        return False

    def _initialize_connection(self):
        pass