#!/usr/bin/python3
"""Unit tests for the Amenity class."""
import os
import time
import unittest
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity

DB_MODE = os.getenv('HBNB_TYPE_STORAGE') == 'db'
ATTRS = [
    ('name', '')
]
SAMPLES = {str: "sample", int: 7, float: 1.5, list: ["a1", "a2"]}


@unittest.skipIf(DB_MODE, "class defaults are FileStorage-only")
class TestAmenityAttributes(unittest.TestCase):
    """Class attributes of Amenity"""

    def test_inherits_basemodel(self):
        """Amenity inherits from BaseModel."""
        self.assertTrue(issubclass(Amenity, BaseModel))

    def test_name_class_default(self):
        """Amenity.name is a public class attribute, default ''."""
        self.assertIn("name", Amenity.__dict__)
        self.assertEqual(Amenity.name, '')
        self.assertIs(type(Amenity.name), str)

    def test_name_instance_default(self):
        """A new Amenity starts with name equal to ''."""
        obj = Amenity()
        self.assertEqual(obj.name, '')
        self.assertIs(type(obj.name), str)


@unittest.skipIf(DB_MODE, "FileStorage behavior")
class TestAmenityBehavior(unittest.TestCase):
    """Behavior of Amenity instances"""

    def test_instance_type(self):
        """Creating Amenity gives a Amenity instance."""
        self.assertIs(type(Amenity()), Amenity)

    def test_unique_ids(self):
        """Two instances never share an id."""
        self.assertNotEqual(Amenity().id, Amenity().id)

    def test_str_representation(self):
        """__str__ starts with the class name and the id."""
        obj = Amenity()
        self.assertIn("[Amenity] ({})".format(obj.id), str(obj))

    def test_saved_instance_in_storage(self):
        """A saved instance is found in storage under Amenity.<id>."""
        obj = Amenity()
        obj.save()
        key = "Amenity.{}".format(obj.id)
        self.assertIs(storage.all()[key], obj)
        storage.delete(obj)
        storage.save()

    def test_to_dict_class_name(self):
        """to_dict() reports the right class name."""
        self.assertEqual(Amenity().to_dict()["__class__"], "Amenity")

    def test_to_dict_roundtrip_keeps_attributes(self):
        """Attributes survive to_dict() then Amenity(**dict)."""
        obj = Amenity()
        for name, default in ATTRS:
            setattr(obj, name, SAMPLES[type(default)])
        clone = Amenity(**obj.to_dict())
        self.assertIsNot(clone, obj)
        self.assertEqual(clone.id, obj.id)
        for name, default in ATTRS:
            self.assertEqual(getattr(clone, name), SAMPLES[type(default)])

    def test_save_updates_updated_at(self):
        """save() moves updated_at forward."""
        obj = Amenity()
        before = obj.updated_at
        time.sleep(0.01)
        obj.save()
        self.assertLess(before, obj.updated_at)
        storage.delete(obj)
        storage.save()


if __name__ == '__main__':
    unittest.main()
