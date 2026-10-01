#!/usr/bin/python3
"""Tests for FileStorage.all(cls) and FileStorage.delete(obj)"""
import os
import unittest
from models import storage
from models.state import State
from models.city import City


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', "FileStorage only")
class TestAllAndDelete(unittest.TestCase):
    """all(cls) filtering and delete(obj)"""

    def setUp(self):
        self.state = State()
        self.state.name = "California"
        storage.new(self.state)
        self.city = City()
        self.city.name = "Fremont"
        storage.new(self.city)
        self.key = "State." + self.state.id

    def tearDown(self):
        storage.delete(self.state)
        storage.delete(self.city)

    def test_all_class_filter(self):
        states = storage.all(State)
        self.assertIn(self.key, states)
        for obj in states.values():
            self.assertIsInstance(obj, State)

    def test_all_str_filter(self):
        states = storage.all("State")
        self.assertIn(self.key, states)
        self.assertNotIn("City." + self.city.id, states)

    def test_all_no_arg_has_everything(self):
        everything = storage.all()
        self.assertIn(self.key, everything)
        self.assertIn("City." + self.city.id, everything)

    def test_delete_removes_object(self):
        storage.delete(self.state)
        self.assertNotIn(self.key, storage.all())

    def test_delete_none_is_noop(self):
        before = len(storage.all())
        storage.delete(None)
        self.assertEqual(len(storage.all()), before)

    def test_delete_missing_is_noop(self):
        storage.delete(self.state)
        storage.delete(self.state)
        self.assertNotIn(self.key, storage.all())


if __name__ == "__main__":
    unittest.main()
