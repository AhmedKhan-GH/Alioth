import unittest
from unittest.mock import patch, Mock
from alioth.clients.databaseclient import *

class MockDatabaseClient(DatabaseClient):
    def _check_connection(self):
        return True

    def _create_client(self):
        return Mock()

class TestLogging(unittest.TestCase):

    def test_check_connection_logging(self):
        client = MockDatabaseClient()
        with self.assertLogs("alioth.core.clientmixin", level="INFO") as cm:
            client.check_connection()
            self.assertGreater(len(cm.records), 0)


class TestCheckConnection(unittest.TestCase):
    def test_check_connection_success(self):
        client = MockDatabaseClient()
        self.assertTrue(client.check_connection())

    def test_check_connection_failure(self):
        client = MockDatabaseClient()
        with patch.object(client, '_check_connection', return_value=False):
            self.assertFalse(client.check_connection())