import unittest
from unittest.mock import patch, Mock
import logging
from alioth.core.connection import *

class TestUrlConnection(unittest.TestCase):
    """Testing connection validation"""

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    @patch('requests.get')
    def test_check_url_connection_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        headers = {'Authorization': 'Bearer test-key'}
        result = check_url_connection('https://example.com', headers, timeout=5)
        self.assertTrue(result)
        mock_get.assert_called_once_with('https://example.com', headers=headers, timeout=5)

    @patch('requests.get')
    def test_check_url_connection_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError()


        headers = {'Authorization': 'Bearer test-key'}
        result = check_url_connection('https://example.com', headers, timeout=5)
        self.assertFalse(result)
        mock_get.assert_called_once_with('https://example.com', headers=headers, timeout=5)


class TestPortConnection(unittest.TestCase):
    """Testing connection validation"""

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    @patch('socket.socket')
    def test_check_port_connection_success(self, mock_socket):
        mock_sock_instance = Mock()
        mock_sock_instance.connect_ex.return_value = 0
        mock_socket.return_value = mock_sock_instance

        result = check_port_connection('localhost', 8080)
        self.assertTrue(result)
        mock_sock_instance.close.assert_called_once()

    @patch('socket.socket')
    def test_check_port_connection_failure(self, mock_socket):
        mock_sock_instance = Mock()
        mock_sock_instance.connect_ex.return_value = 1
        mock_socket.return_value = mock_sock_instance


        result = check_port_connection('localhost', 8080)
        self.assertFalse(result)
        mock_sock_instance.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()