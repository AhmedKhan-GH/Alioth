"""Test suite for main.py module functionality."""
# test_{module_name}
# always relates to the python file being tested

# unit test
# test_{what_is_tested}_{expected_outcome}
# always relates to the unit feature being tested

import unittest
import main
import os
from unittest.mock import patch

class TestKey(unittest.TestCase):
    """Test environment for key existence verification"""
    def test_openai_key_missing(self):
        """Test that the openai api key is missing"""
        with patch.dict('os.environ', {}, clear = True):
            self.assertFalse(main.has_openai_key())

    def test_openai_key_exists(self):
        """Test that the openai api key exists"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
            self.assertTrue(main.has_openai_key())

# Test{Feature}
# classes exist to organize unit tests for traceback
# selective execution, and readable documentation
class TestMain(unittest.TestCase):
    """Basic test cases for main functionality"""

    def test_main_fails_without_key(self):
        """Test that the main function fails without key"""
        with self.assertRaises(EnvironmentError):
            main.main()

    def test_main_runs_without_failure(self):
        """Test that main() executes without raising any exceptions."""
        try:
            main.main()
        except Exception as e:
            self.fail(f"main() raised an exception: {e}")