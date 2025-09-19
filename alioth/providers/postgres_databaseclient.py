from alioth.clients.databaseclient import DatabaseClient
from peewee import PostgresqlDatabase
from alioth.core.environment import get_environment_variable

from alioth.core.decorators import try_catch

class PostgresDatabaseClient(DatabaseClient):

    @try_catch(exit_on_error=False, default_return=False)
    def _check_connection(self):
        postgres_user = get_environment_variable('POSTGRES_USER', required=True)
        self.temp_client = PostgresqlDatabase(database="postgres", user=postgres_user, host="localhost", port=5432)
        self.temp_client.connect(reuse_if_open=True)
        result = not self.temp_client.is_closed()
        self.temp_client.close()
        return result

    def _create_client(self):
        postgres_user = get_environment_variable('POSTGRES_USER', required=True)
        return PostgresqlDatabase(database="postgres", user=postgres_user, host="localhost", port=5432)


