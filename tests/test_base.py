import sys
import os
import unittest

# append the parent folder to sys.paths.
parent_folder = os.path.dirname(__file__)
sys.path.append(os.path.dirname(parent_folder))


class TestBase(unittest.TestCase):
    @classmethod
    def get_test_resource(cls, *args):
        return os.path.join(
            os.path.dirname(__file__),
            "resources",
            *args
        )