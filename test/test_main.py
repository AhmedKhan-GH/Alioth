"""Test suite for main.py module functionality."""
# test_{module_name}
# always relates to the python file being tested

# unit test
# test_{what_is_tested}_{expected_outcome}
# always relates to the unit feature being tested

import unittest
import inspect

from dotenv import load_dotenv
import tempfile
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
# classes exist to organize unit test for traceback
# selective execution, and readable documentation
class TestMain(unittest.TestCase):
    """Basic test cases for main functionality"""

    def test_main_fails_without_key(self):
        """Test that the main function fails without key"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(EnvironmentError):
                main.main()

    def test_main_runs_with_key(self):
        """Test that main() executes without raising any exceptions."""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
            try:
                main.main()
            except Exception as e:
                self.fail(f"main() raised an exception: {e}")

    def test_dotenv_loads_env_var(self):
        """Test dotenv loads variables from .env file."""
        # Create temporary .env file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write('OPENAI_API_KEY=test_key\n')
            temp_env_path = f.name
        try:
            with patch.dict(os.environ, {}, clear=True):
                # Load from mock .env file
                load_dotenv(temp_env_path)

                # Check if variable was loaded
                self.assertEqual(os.environ['OPENAI_API_KEY'], 'test_key')
        finally:
            # Clean up temp file
            os.unlink(temp_env_path)

if __name__ == '__main__':
    unittest.main()