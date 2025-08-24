import unittest
import sys
import logging

from unittest.mock import patch, Mock
from alioth.core.decorators import *

class TestTryCatchDecorator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def test_try_catch_decorator_successfully_returns(self):
        """Test try_catch decorator returns the result of the wrapped function when no exception is raised."""
        @try_catch()
        def test_func():
            return 'test_result'

        result = test_func()
        self.assertEqual(result, 'test_result')

    @patch('sys.exit')
    def test_try_catch_decorator_catches_exception_and_exits(self, mock_exit):
        """Test try_catch decorator exits the program when an exception is raised and exit_on_error is True."""
        @try_catch(exit_on_error = True)
        def test_func():
            raise Exception('test_exception')
        test_func()
        mock_exit.assert_called_once_with(1)

    def test_try_catch_decorator_returns_default_value(self):
        """Test try_catch decorator returns a default value when an exception is raised and exit_on_error is False."""
        @try_catch(exit_on_error = False, default_return = 'test_default')
        def test_func():
            raise Exception('test_exception')

        result = test_func()
        self.assertEqual(result, 'test_default')

    def test_try_catch_decorator_raises_unspecified_exception(self):
        """Test try_catch decorator raises an exception when an exception is raised and catch_exceptions is not specified."""
        @try_catch(catch_exceptions =ValueError)
        def test_func():
            raise TypeError('test_error')

        with self.assertRaises(TypeError):
            test_func()

    @patch('sys.exit')
    def test_try_catch_decorator_catches_multiple_exceptions(self, mock_exit):
        """Test try_catch decorator catches multiple specified exception types."""
        @try_catch(exit_code = 1, catch_exceptions = (ValueError, TypeError))
        def test_func():
            raise TypeError('test_error')

        test_func()
        mock_exit.assert_called_once_with(1)


