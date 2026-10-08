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


@unittest.skipIf(DB_MODE, "class defaults are FileStorage-only")
class TestPlaceAttributes(unittest.TestCase):
    """Class attributes of Place"""

    def test_inherits_basemodel(self):
        """Place inherits from BaseModel."""
        self.assertTrue(issubclass(Place, BaseModel))

    def test_city_id_class_default(self):
        """Place.city_id is a public class attribute, default ''."""
        self.assertIn("city_id", Place.__dict__)
        self.assertEqual(Place.city_id, '')
        self.assertIs(type(Place.city_id), str)

    def test_city_id_instance_default(self):
        """A new Place starts with city_id equal to ''."""
        obj = Place()
        self.assertEqual(obj.city_id, '')
        self.assertIs(type(obj.city_id), str)

    def test_user_id_class_default(self):
        """Place.user_id is a public class attribute, default ''."""
        self.assertIn("user_id", Place.__dict__)
        self.assertEqual(Place.user_id, '')
        self.assertIs(type(Place.user_id), str)

    def test_user_id_instance_default(self):
        """A new Place starts with user_id equal to ''."""
        obj = Place()
        self.assertEqual(obj.user_id, '')
        self.assertIs(type(obj.user_id), str)

    def test_name_class_default(self):
        """Place.name is a public class attribute, default ''."""
        self.assertIn("name", Place.__dict__)
        self.assertEqual(Place.name, '')
        self.assertIs(type(Place.name), str)

    def test_name_instance_default(self):
        """A new Place starts with name equal to ''."""
        obj = Place()
        self.assertEqual(obj.name, '')
        self.assertIs(type(obj.name), str)

    def test_description_class_default(self):
        """Place.description is a public class attribute, default ''."""
        self.assertIn("description", Place.__dict__)
        self.assertEqual(Place.description, '')
        self.assertIs(type(Place.description), str)

    def test_description_instance_default(self):
        """A new Place starts with description equal to ''."""
        obj = Place()
        self.assertEqual(obj.description, '')
        self.assertIs(type(obj.description), str)

    def test_number_rooms_class_default(self):
        """Place.number_rooms is a public class attribute, default 0."""
        self.assertIn("number_rooms", Place.__dict__)
        self.assertEqual(Place.number_rooms, 0)
        self.assertIs(type(Place.number_rooms), int)

    def test_number_rooms_instance_default(self):
        """A new Place starts with number_rooms equal to 0."""
        obj = Place()
        self.assertEqual(obj.number_rooms, 0)
        self.assertIs(type(obj.number_rooms), int)

    def test_number_bathrooms_class_default(self):
        """Place.number_bathrooms is a public class attribute, default 0."""
        self.assertIn("number_bathrooms", Place.__dict__)
        self.assertEqual(Place.number_bathrooms, 0)
        self.assertIs(type(Place.number_bathrooms), int)

    def test_number_bathrooms_instance_default(self):
        """A new Place starts with number_bathrooms equal to 0."""
        obj = Place()
        self.assertEqual(obj.number_bathrooms, 0)
        self.assertIs(type(obj.number_bathrooms), int)

    def test_max_guest_class_default(self):
        """Place.max_guest is a public class attribute, default 0."""
        self.assertIn("max_guest", Place.__dict__)
        self.assertEqual(Place.max_guest, 0)
        self.assertIs(type(Place.max_guest), int)

    def test_max_guest_instance_default(self):
        """A new Place starts with max_guest equal to 0."""
        obj = Place()
        self.assertEqual(obj.max_guest, 0)
        self.assertIs(type(obj.max_guest), int)

    def test_price_by_night_class_default(self):
        """Place.price_by_night is a public class attribute, default 0."""
        self.assertIn("price_by_night", Place.__dict__)
        self.assertEqual(Place.price_by_night, 0)
        self.assertIs(type(Place.price_by_night), int)

    def test_price_by_night_instance_default(self):
        """A new Place starts with price_by_night equal to 0."""
        obj = Place()
        self.assertEqual(obj.price_by_night, 0)
        self.assertIs(type(obj.price_by_night), int)

    def test_latitude_class_default(self):
        """Place.latitude is a public class attribute, default 0.0."""
        self.assertIn("latitude", Place.__dict__)
        self.assertEqual(Place.latitude, 0.0)
        self.assertIs(type(Place.latitude), float)

    def test_latitude_instance_default(self):
        """A new Place starts with latitude equal to 0.0."""
        obj = Place()
        self.assertEqual(obj.latitude, 0.0)
        self.assertIs(type(obj.latitude), float)

    def test_longitude_class_default(self):
        """Place.longitude is a public class attribute, default 0.0."""
        self.assertIn("longitude", Place.__dict__)
        self.assertEqual(Place.longitude, 0.0)
        self.assertIs(type(Place.longitude), float)

    def test_longitude_instance_default(self):
        """A new Place starts with longitude equal to 0.0."""
        obj = Place()
        self.assertEqual(obj.longitude, 0.0)
        self.assertIs(type(obj.longitude), float)

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
