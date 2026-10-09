#!/usr/bin/python3
"""Unit tests for the Place class."""
import os
import time
import unittest
from models import storage
from models.base_model import BaseModel
from models.place import Place

DB_MODE = os.getenv('HBNB_TYPE_STORAGE') == 'db'
ATTRS = [
    ('city_id', ''),
    ('user_id', ''),
    ('name', ''),
    ('description', ''),
    ('number_rooms', 0),
    ('number_bathrooms', 0),
    ('max_guest', 0),
    ('price_by_night', 0),
    ('latitude', 0.0),
    ('longitude', 0.0),
    ('amenity_ids', [])
]
SAMPLES = {str: "sample", int: 7, float: 1.5, list: ["a1", "a2"]}


class TestPlaceAttributes(unittest.TestCase):
    """Class attributes of Place"""

    def test_inherits_basemodel(self):
        """Place inherits from BaseModel."""
        self.assertTrue(issubclass(Place, BaseModel))


    def test_amenity_ids_class_default(self):
        """Place.amenity_ids is a public class attribute, default []."""
        self.assertIn("amenity_ids", Place.__dict__)
        self.assertEqual(Place.amenity_ids, [])
        self.assertIs(type(Place.amenity_ids), list)

    def test_amenity_ids_instance_default(self):
        """A new Place starts with amenity_ids equal to []."""
        obj = Place()
        self.assertEqual(obj.amenity_ids, [])
        self.assertIs(type(obj.amenity_ids), list)


@unittest.skipIf(DB_MODE, "FileStorage behavior")
class TestPlaceBehavior(unittest.TestCase):
    """Behavior of Place instances"""

    def test_instance_type(self):
        """Creating Place gives a Place instance."""
        self.assertIs(type(Place()), Place)

    def test_unique_ids(self):
        """Two instances never share an id."""
        self.assertNotEqual(Place().id, Place().id)

    def test_str_representation(self):
        """__str__ starts with the class name and the id."""
        obj = Place()
        self.assertIn("[Place] ({})".format(obj.id), str(obj))

    def test_saved_instance_in_storage(self):
        """A saved instance is found in storage under Place.<id>."""
        obj = Place()
        obj.save()
        key = "Place.{}".format(obj.id)
        self.assertIs(storage.all()[key], obj)
        storage.delete(obj)
        storage.save()

    def test_to_dict_class_name(self):
        """to_dict() reports the right class name."""
        self.assertEqual(Place().to_dict()["__class__"], "Place")

    def test_to_dict_roundtrip_keeps_attributes(self):
        """Attributes survive to_dict() then Place(**dict)."""
        obj = Place()
        for name, default in ATTRS:
            setattr(obj, name, SAMPLES[type(default)])
        clone = Place(**obj.to_dict())
        self.assertIsNot(clone, obj)
        self.assertEqual(clone.id, obj.id)
        for name, default in ATTRS:
            self.assertEqual(getattr(clone, name), SAMPLES[type(default)])

    def test_save_updates_updated_at(self):
        """save() moves updated_at forward."""
        obj = Place()
        before = obj.updated_at
        time.sleep(0.01)
        obj.save()
        self.assertLess(before, obj.updated_at)
        storage.delete(obj)
        storage.save()


if __name__ == '__main__':
    unittest.main()
