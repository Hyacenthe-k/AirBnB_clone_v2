#!/usr/bin/python3
"""Tests for the DBStorage module"""
import unittest
from models.engine import db_storage


class TestDBStorageModule(unittest.TestCase):
    """Basic checks on the db_storage module"""

    def test_class_exists(self):
        self.assertTrue(hasattr(db_storage, "DBStorage"))

    def test_class_has_docstring(self):
        self.assertTrue(len(db_storage.DBStorage.__doc__) > 0)


if __name__ == "__main__":
    unittest.main()
