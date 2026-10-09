#!/usr/bin/python3
"""Unit tests for the City class."""
import os
import time
import unittest
from models import storage
from models.base_model import BaseModel
from models.city import City

DB_MODE = os.getenv('HBNB_TYPE_STORAGE') == 'db'
ATTRS = [
    ('state_id', ''),
    ('name', '')
]
SAMPLES = {str: "sample", int: 7, float: 1.5, list: ["a1", "a2"]}


class TestCityAttributes(unittest.TestCase):
    """Class attributes of City"""

    def test_inherits_basemodel(self):
        """City inherits from BaseModel."""
        self.assertTrue(issubclass(City, BaseModel))


@unittest.skipIf(DB_MODE, "FileStorage behavior")
class TestCityBehavior(unittest.TestCase):
    """Behavior of City instances"""

    def test_instance_type(self):
        """Creating City gives a City instance."""
        self.assertIs(type(City()), City)

    def test_unique_ids(self):
        """Two instances never share an id."""
        self.assertNotEqual(City().id, City().id)

    def test_str_representation(self):
        """__str__ starts with the class name and the id."""
        obj = City()
        self.assertIn("[City] ({})".format(obj.id), str(obj))

    def test_saved_instance_in_storage(self):
        """A saved instance is found in storage under City.<id>."""
        obj = City()
        obj.save()
        key = "City.{}".format(obj.id)
        self.assertIs(storage.all()[key], obj)
        storage.delete(obj)
        storage.save()

    def test_to_dict_class_name(self):
        """to_dict() reports the right class name."""
        self.assertEqual(City().to_dict()["__class__"], "City")

    def test_to_dict_roundtrip_keeps_attributes(self):
        """Attributes survive to_dict() then City(**dict)."""
        obj = City()
        for name, default in ATTRS:
            setattr(obj, name, SAMPLES[type(default)])
        clone = City(**obj.to_dict())
        self.assertIsNot(clone, obj)
        self.assertEqual(clone.id, obj.id)
        for name, default in ATTRS:
            self.assertEqual(getattr(clone, name), SAMPLES[type(default)])

    def test_save_updates_updated_at(self):
        """save() moves updated_at forward."""
        obj = City()
        before = obj.updated_at
        time.sleep(0.01)
        obj.save()
        self.assertLess(before, obj.updated_at)
        storage.delete(obj)
        storage.save()


if __name__ == '__main__':
    unittest.main()
