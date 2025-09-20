from alioth.clients.databaseclient import DatabaseClient
from peewee import PostgresqlDatabase
from alioth.core.environment import get_environment_variable

from alioth.core.decorators import try_catch

# FILES TABLE
# file_uuid: primary key
# file_hash: string, to determine if file is unique from content
# file_name: internal representation
# == extra columns to add ==
# author: string
# publisher: string

# CHUNKS TABLE
# chunks_uuid: primary key
# file_uuid: relates to the files the chunks come from
# text: post-normalization text to be sent to LLMs
# page_number: INT for reference and citation
# bbox_coord: JSON(int, int, int, int) page vis of source
# chunk_hash: string, to id uniqueness when deduplicating for llm

class PostgresDatabaseClient(DatabaseClient):

    @try_catch(exit_on_error=False, default_return=False)
    def _check_connection(self):
        postgres_user = get_environment_variable('POSTGRES_USER', required=True)
        self.temp_client = PostgresqlDatabase(database="postgres", user=postgres_user, host="localhost", port=5432)
        self.temp_client.connect(reuse_if_open=True)
        result = not self.temp_client.is_closed()
        self.temp_client.close()
        return result

    def test_database(self):
        """rewrites test_database on every execution of the program for now"""
        self._client.execute_sql('DROP DATABASE IF EXISTS test_database;')
        self._client.execute_sql('CREATE DATABASE test_database')


    def _create_client(self):
        postgres_user = get_environment_variable('POSTGRES_USER', required=True)
        return PostgresqlDatabase(database="postgres", user=postgres_user, host="localhost", port=5432)


