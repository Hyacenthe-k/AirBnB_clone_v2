#!/usr/bin/python3
"""Unit tests for the User class."""
import os
import time
import unittest
from models import storage
from models.base_model import BaseModel
from models.user import User

DB_MODE = os.getenv('HBNB_TYPE_STORAGE') == 'db'
ATTRS = [
    ('email', ''),
    ('password', ''),
    ('first_name', ''),
    ('last_name', '')
]
SAMPLES = {str: "sample", int: 7, float: 1.5, list: ["a1", "a2"]}


class TestUserAttributes(unittest.TestCase):
    """Class attributes of User"""

    def test_inherits_basemodel(self):
        """User inherits from BaseModel."""
        self.assertTrue(issubclass(User, BaseModel))


@unittest.skipIf(DB_MODE, "FileStorage behavior")
class TestUserBehavior(unittest.TestCase):
    """Behavior of User instances"""

    def test_instance_type(self):
        """Creating User gives a User instance."""
        self.assertIs(type(User()), User)

    def test_unique_ids(self):
        """Two instances never share an id."""
        self.assertNotEqual(User().id, User().id)

    def test_str_representation(self):
        """__str__ starts with the class name and the id."""
        obj = User()
        self.assertIn("[User] ({})".format(obj.id), str(obj))

    def test_saved_instance_in_storage(self):
        """A saved instance is found in storage under User.<id>."""
        obj = User()
        obj.save()
        key = "User.{}".format(obj.id)
        self.assertIs(storage.all()[key], obj)
        storage.delete(obj)
        storage.save()

    def test_to_dict_class_name(self):
        """to_dict() reports the right class name."""
        self.assertEqual(User().to_dict()["__class__"], "User")

    def test_to_dict_roundtrip_keeps_attributes(self):
        """Attributes survive to_dict() then User(**dict)."""
        obj = User()
        for name, default in ATTRS:
            setattr(obj, name, SAMPLES[type(default)])
        clone = User(**obj.to_dict())
        self.assertIsNot(clone, obj)
        self.assertEqual(clone.id, obj.id)
        for name, default in ATTRS:
            self.assertEqual(getattr(clone, name), SAMPLES[type(default)])

    def test_save_updates_updated_at(self):
        """save() moves updated_at forward."""
        obj = User()
        before = obj.updated_at
        time.sleep(0.01)
        obj.save()
        self.assertLess(before, obj.updated_at)
        storage.delete(obj)
        storage.save()


if __name__ == '__main__':
    unittest.main()
