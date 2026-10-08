#!/usr/bin/python3
"""Unit tests for the Review class."""
import os
import time
import unittest
from models import storage
from models.base_model import BaseModel
from models.review import Review

DB_MODE = os.getenv('HBNB_TYPE_STORAGE') == 'db'
ATTRS = [
    ('place_id', ''),
    ('user_id', ''),
    ('text', '')
]
SAMPLES = {str: "sample", int: 7, float: 1.5, list: ["a1", "a2"]}


@unittest.skipIf(DB_MODE, "class defaults are FileStorage-only")
class TestReviewAttributes(unittest.TestCase):
    """Class attributes of Review"""

    def test_inherits_basemodel(self):
        """Review inherits from BaseModel."""
        self.assertTrue(issubclass(Review, BaseModel))

    def test_place_id_class_default(self):
        """Review.place_id is a public class attribute, default ''."""
        self.assertIn("place_id", Review.__dict__)
        self.assertEqual(Review.place_id, '')
        self.assertIs(type(Review.place_id), str)

    def test_place_id_instance_default(self):
        """A new Review starts with place_id equal to ''."""
        obj = Review()
        self.assertEqual(obj.place_id, '')
        self.assertIs(type(obj.place_id), str)

    def test_user_id_class_default(self):
        """Review.user_id is a public class attribute, default ''."""
        self.assertIn("user_id", Review.__dict__)
        self.assertEqual(Review.user_id, '')
        self.assertIs(type(Review.user_id), str)

    def test_user_id_instance_default(self):
        """A new Review starts with user_id equal to ''."""
        obj = Review()
        self.assertEqual(obj.user_id, '')
        self.assertIs(type(obj.user_id), str)

    def test_text_class_default(self):
        """Review.text is a public class attribute, default ''."""
        self.assertIn("text", Review.__dict__)
        self.assertEqual(Review.text, '')
        self.assertIs(type(Review.text), str)

    def test_text_instance_default(self):
        """A new Review starts with text equal to ''."""
        obj = Review()
        self.assertEqual(obj.text, '')
        self.assertIs(type(obj.text), str)


@unittest.skipIf(DB_MODE, "FileStorage behavior")
class TestReviewBehavior(unittest.TestCase):
    """Behavior of Review instances"""

    def test_instance_type(self):
        """Creating Review gives a Review instance."""
        self.assertIs(type(Review()), Review)

    def test_unique_ids(self):
        """Two instances never share an id."""
        self.assertNotEqual(Review().id, Review().id)

    def test_str_representation(self):
        """__str__ starts with the class name and the id."""
        obj = Review()
        self.assertIn("[Review] ({})".format(obj.id), str(obj))

    def test_saved_instance_in_storage(self):
        """A saved instance is found in storage under Review.<id>."""
        obj = Review()
        obj.save()
        key = "Review.{}".format(obj.id)
        self.assertIs(storage.all()[key], obj)
        storage.delete(obj)
        storage.save()

    def test_to_dict_class_name(self):
        """to_dict() reports the right class name."""
        self.assertEqual(Review().to_dict()["__class__"], "Review")

    def test_to_dict_roundtrip_keeps_attributes(self):
        """Attributes survive to_dict() then Review(**dict)."""
        obj = Review()
        for name, default in ATTRS:
            setattr(obj, name, SAMPLES[type(default)])
        clone = Review(**obj.to_dict())
        self.assertIsNot(clone, obj)
        self.assertEqual(clone.id, obj.id)
        for name, default in ATTRS:
            self.assertEqual(getattr(clone, name), SAMPLES[type(default)])

    def test_save_updates_updated_at(self):
        """save() moves updated_at forward."""
        obj = Review()
        before = obj.updated_at
        time.sleep(0.01)
        obj.save()
        self.assertLess(before, obj.updated_at)
        storage.delete(obj)
        storage.save()


if __name__ == '__main__':
    unittest.main()
