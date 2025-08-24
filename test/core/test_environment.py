import unittest
import os
from unittest.mock import patch
from alioth.core.environment import *

class TestEnvironmentValidation(unittest.TestCase):
    """Testing environment variable validation"""