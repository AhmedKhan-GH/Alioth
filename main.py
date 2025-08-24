# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
from dotenv import load_dotenv

from test import test_main

load_dotenv()
import test.test_main

def has_openai_key():
    """Check if OPENAI_API_KEY exists in environment."""
    return 'OPENAI_API_KEY' in os.environ

def main():
    if not has_openai_key():
        raise EnvironmentError('OPENAI_API_KEY not found')

if __name__ == '__main__':
    main()