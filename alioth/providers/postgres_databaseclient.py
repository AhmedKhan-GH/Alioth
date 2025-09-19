from alioth.clients.databaseclient import DatabaseClient
import psycopg2
from psycopg2 import OperationalError
from peewee import PostgresqlDatabase
from alioth.core.environment import get_environment_variable

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
        self._client.connect(reuse_if_open=True)
        return not self._client.is_closed()

    def _initialize_connection(self):
        postgres_user = get_environment_variable('POSTGRES_USER', required=True)
        self._client = PostgresqlDatabase(database="postgres",
                                          user=postgres_user,
                                          host="localhost",
                                          port=5432)
        pass