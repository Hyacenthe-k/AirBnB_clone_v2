#!/usr/bin/python3
"""Unit tests for the FileStorage class."""
import unittest
import os
import json
from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorageInstantiation(unittest.TestCase):
    """Tests for how FileStorage is created and structured."""

    def test_file_path_is_private_str(self):
        """__file_path is a private class attribute of type str."""
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_objects_is_private_dict(self):
        """__objects is a private class attribute of type dict."""
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(self):
        """The models package exposes a single FileStorage instance."""
        self.assertEqual(FileStorage, type(storage))


class TestFileStorageMethods(unittest.TestCase):
    """Tests for all(), new(), save(), and reload()."""

    def setUp(self):
        """Keep a reference to the storage file path used in tests."""
        self.file_path = FileStorage._FileStorage__file_path

    def tearDown(self):
        """Remove any JSON file created during a test."""
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass

    def test_all_returns_dict(self):
        """all() returns the __objects dictionary."""
        self.assertEqual(dict, type(storage.all()))

    def test_new_adds_object(self):
        """new() registers an object under <class>.<id> in __objects."""
        bm = BaseModel()
        storage.new(bm)
        key = "BaseModel.{}".format(bm.id)
        self.assertIn(key, storage.all())
        self.assertIs(storage.all()[key], bm)

    def test_save_creates_file(self):
        """save() writes a JSON file to disk at __file_path."""
        BaseModel()
        storage.save()
        self.assertTrue(os.path.exists(self.file_path))

    def test_save_content_is_valid_json(self):
        """The file written by save() is parseable, valid JSON."""
        bm = BaseModel()
        storage.save()
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        key = "BaseModel.{}".format(bm.id)
        self.assertIn(key, data)
        self.assertEqual(data[key]["__class__"], "BaseModel")

    def test_reload_restores_objects(self):
        """reload() repopulates __objects from a previously saved file."""
        bm = BaseModel()
        bm_id = bm.id
        storage.save()
        FileStorage._FileStorage__objects = {}
        storage.reload()
        key = "BaseModel.{}".format(bm_id)
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].id, bm_id)

    def test_reload_no_file_does_not_raise(self):
        """reload() silently does nothing if the JSON file is missing."""
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass
        try:
            storage.reload()
        except Exception as exc:
            self.fail("reload() raised {} with no file present".format(exc))


if __name__ == "__main__":
    unittest.main()
