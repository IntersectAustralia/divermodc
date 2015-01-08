import unittest
import sys, os

PROJECT_ROOT = os.path.dirname(__file__) + '/../'
sys.path.insert(0, PROJECT_ROOT)

import diver.config as config
import diver.hiev as hiev

# To run all tests from project directory:
# python -m unittest discover -s tests/ -p 'test_*.py' -v
    