#!/usr/bin/python3
"""Unit tests for the HBNBCommand console."""
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand


class TestHBNBCommand(unittest.TestCase):
    """Tests for the quit, EOF, and emptyline console commands."""

    def test_quit_exits(self):
        """The quit command returns True, ending the cmdloop."""
        self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(self):
        """The EOF command returns True, ending the cmdloop."""
        self.assertTrue(HBNBCommand().onecmd("EOF"))

    def test_emptyline_outputs_nothing(self):
        """Pressing Enter on a blank line produces no output."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            HBNBCommand().onecmd("")
            self.assertEqual("", fake_out.getvalue())

    def test_help_command_exists(self):
        """The help command lists documented commands without error."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            HBNBCommand().onecmd("help")
            output = fake_out.getvalue()
        self.assertIn("quit", output)


class TestCreateParams(unittest.TestCase):
    """create <Class> key=value, FileStorage only"""

    def setUp(self):
        import os
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            self.skipTest("FileStorage only")

    def run_cmd(self, line):
        from io import StringIO
        from unittest.mock import patch
        from console import HBNBCommand
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd(line)
            return out.getvalue().strip()

    def get(self, key):
        from models import storage
        return storage.all()[key]

    def test_string_param(self):
        new_id = self.run_cmd('create State name="California"')
        self.assertEqual(self.get("State." + new_id).name, "California")

    def test_underscore_to_space(self):
        new_id = self.run_cmd('create State name="San_Francisco"')
        self.assertEqual(self.get("State." + new_id).name, "San Francisco")

    def test_int_and_float(self):
        new_id = self.run_cmd(
            'create Place name="My_house" number_rooms=4 latitude=37.77')
        obj = self.get("Place." + new_id)
        self.assertIsInstance(obj.number_rooms, int)
        self.assertEqual(obj.number_rooms, 4)
        self.assertIsInstance(obj.latitude, float)
        self.assertEqual(obj.latitude, 37.77)

    def test_bad_param_skipped(self):
        new_id = self.run_cmd('create State name="Ok" age=abc nope')
        obj = self.get("State." + new_id)
        self.assertEqual(obj.name, "Ok")
        self.assertFalse(hasattr(obj, "age"))
        self.assertFalse(hasattr(obj, "nope"))

    def test_unknown_class(self):
        out = self.run_cmd('create Nope name="x"')
        self.assertEqual(out, "** class doesn't exist **")


if __name__ == "__main__":
    unittest.main()
