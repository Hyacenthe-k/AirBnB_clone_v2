#!/usr/bin/python3
"""Unit tests for the State class."""
import os
import time
import unittest
from models import storage
from models.base_model import BaseModel
from models.state import State

DB_MODE = os.getenv('HBNB_TYPE_STORAGE') == 'db'
ATTRS = [
    ('name', '')
]
SAMPLES = {str: "sample", int: 7, float: 1.5, list: ["a1", "a2"]}


class TestStateAttributes(unittest.TestCase):
    """Class attributes of State"""

    def test_inherits_basemodel(self):
        """State inherits from BaseModel."""
        self.assertTrue(issubclass(State, BaseModel))


@unittest.skipIf(DB_MODE, "FileStorage behavior")
class TestStateBehavior(unittest.TestCase):
    """Behavior of State instances"""

    def test_instance_type(self):
        """Creating State gives a State instance."""
        self.assertIs(type(State()), State)

    def test_unique_ids(self):
        """Two instances never share an id."""
        self.assertNotEqual(State().id, State().id)

    def test_str_representation(self):
        """__str__ starts with the class name and the id."""
        obj = State()
        self.assertIn("[State] ({})".format(obj.id), str(obj))

    def test_saved_instance_in_storage(self):
        """A saved instance is found in storage under State.<id>."""
        obj = State()
        obj.save()
        key = "State.{}".format(obj.id)
        self.assertIs(storage.all()[key], obj)
        storage.delete(obj)
        storage.save()

    def test_to_dict_class_name(self):
        """to_dict() reports the right class name."""
        self.assertEqual(State().to_dict()["__class__"], "State")

    def test_to_dict_roundtrip_keeps_attributes(self):
        """Attributes survive to_dict() then State(**dict)."""
        obj = State()
        for name, default in ATTRS:
            setattr(obj, name, SAMPLES[type(default)])
        clone = State(**obj.to_dict())
        self.assertIsNot(clone, obj)
        self.assertEqual(clone.id, obj.id)
        for name, default in ATTRS:
            self.assertEqual(getattr(clone, name), SAMPLES[type(default)])

    def test_save_updates_updated_at(self):
        """save() moves updated_at forward."""
        obj = State()
        before = obj.updated_at
        time.sleep(0.01)
        obj.save()
        self.assertLess(before, obj.updated_at)
        storage.delete(obj)
        storage.save()


if __name__ == '__main__':
    unittest.main()
