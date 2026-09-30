#!/usr/bin/python3
"""Unit tests for the BaseModel class."""
import unittest
import time
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModelInstantiation(unittest.TestCase):
    """Tests for how a BaseModel instance is created."""

    def test_no_args_instantiates(self):
        """A BaseModel can be created with no arguments."""
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        """A newly created instance is registered with storage."""
        self.assertIn(BaseModel(), models_all_values())

    def test_id_is_public_str(self):
        """id is a public string attribute."""
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        """created_at is a public datetime attribute."""
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        """updated_at is a public datetime attribute."""
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_have_unique_ids(self):
        """Two different instances must never share an id."""
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.assertNotEqual(bm1.id, bm2.id)

    def test_two_models_different_created_at(self):
        """Two instances created apart in time have different created_at."""
        bm1 = BaseModel()
        time.sleep(0.01)
        bm2 = BaseModel()
        self.assertLess(bm1.created_at, bm2.created_at)

    def test_two_models_different_updated_at(self):
        """Two instances created apart in time have different updated_at."""
        bm1 = BaseModel()
        time.sleep(0.01)
        bm2 = BaseModel()
        self.assertLess(bm1.updated_at, bm2.updated_at)

    def test_str_representation(self):
        """__str__ prints as [<class name>] (<id>) <__dict__>."""
        bm = BaseModel()
        string = str(bm)
        self.assertIn("[BaseModel] ({})".format(bm.id), string)
        self.assertIn("'id': '{}'".format(bm.id), string)

    def test_args_unused(self):
        """Positional arguments passed to __init__ are ignored."""
        bm = BaseModel(None)
        self.assertNotIn(None, bm.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """A BaseModel can be recreated from a kwargs dictionary."""
        dt = datetime.now()
        dt_iso = dt.isoformat()
        bm = BaseModel(id="123", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "123")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """Passing only None-valued kwargs still yields default fields."""
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)


class TestBaseModelSave(unittest.TestCase):
    """Tests for the save() method."""

    def test_save_updates_updated_at(self):
        """Calling save() moves updated_at forward in time."""
        bm = BaseModel()
        old_updated_at = bm.updated_at
        time.sleep(0.01)
        bm.save()
        self.assertLess(old_updated_at, bm.updated_at)

    def test_save_does_not_change_created_at(self):
        """Calling save() does not modify created_at."""
        bm = BaseModel()
        old_created_at = bm.created_at
        bm.save()
        self.assertEqual(old_created_at, bm.created_at)


class TestBaseModelToDict(unittest.TestCase):
    """Tests for the to_dict() method."""

    def test_to_dict_returns_dict(self):
        """to_dict() returns a dict instance."""
        self.assertEqual(dict, type(BaseModel().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """to_dict() output includes id, created_at, updated_at, __class__."""
        bm = BaseModel()
        d = bm.to_dict()
        for key in ("id", "created_at", "updated_at", "__class__"):
            self.assertIn(key, d)

    def test_to_dict_datetimes_are_strings(self):
        """created_at and updated_at are ISO-format strings in to_dict()."""
        bm = BaseModel()
        d = bm.to_dict()
        self.assertEqual(str, type(d["created_at"]))
        self.assertEqual(str, type(d["updated_at"]))

    def test_to_dict_class_name(self):
        """__class__ matches the instance's class name."""
        bm = BaseModel()
        self.assertEqual(bm.to_dict()["__class__"], "BaseModel")

    def test_to_dict_output_matches_expected(self):
        """to_dict() output exactly matches a hand-built expected dict."""
        bm = BaseModel()
        expected = {
            "id": bm.id,
            "__class__": "BaseModel",
            "created_at": bm.created_at.isoformat(),
            "updated_at": bm.updated_at.isoformat(),
        }
        self.assertDictEqual(bm.to_dict(), expected)

    def test_to_dict_then_recreate_roundtrip(self):
        """to_dict() -> BaseModel(**d) recreates an equivalent instance."""
        bm = BaseModel()
        bm.name = "Holberton"
        bm.number = 89
        d = bm.to_dict()
        bm2 = BaseModel(**d)
        self.assertEqual(bm.id, bm2.id)
        self.assertEqual(bm.created_at, bm2.created_at)
        self.assertEqual(bm.updated_at, bm2.updated_at)
        self.assertEqual(bm.name, bm2.name)
        self.assertEqual(bm.number, bm2.number)
        self.assertIsNot(bm, bm2)


def models_all_values():
    """Return the current storage objects as a list, avoids top-level
    circular import ordering issues in this test module."""
    from models import storage
    return list(storage.all().values())


if __name__ == "__main__":
    unittest.main()
