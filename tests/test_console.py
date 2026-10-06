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


class TestCreateChain(unittest.TestCase):
    """Chained create/show scenarios from the project, FileStorage only"""

    def setUp(self):
        import os
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            self.skipTest("FileStorage only")

    def run_cmd(self, line):
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd(line)
            return out.getvalue().strip()

    def obj(self, key):
        from models import storage
        return storage.all()[key]

    def make_state_and_city(self, city_name):
        state_id = self.run_cmd('create State name="California"')
        city_id = self.run_cmd(
            'create City state_id="{}" name="{}"'.format(state_id, city_name))
        return state_id, city_id

    def test_create_plain_state(self):
        new_id = self.run_cmd('create State')
        self.assertEqual(self.obj("State." + new_id).id, new_id)

    def test_create_city_with_state_id(self):
        state_id, city_id = self.make_state_and_city("Fremont")
        city = self.obj("City." + city_id)
        self.assertEqual(city.state_id, state_id)
        self.assertEqual(city.name, "Fremont")

    def test_space_translated_in_city_name(self):
        state_id, city_id = self.make_state_and_city("San_Francisco")
        self.assertEqual(self.obj("City." + city_id).name, "San Francisco")

    def test_create_place_and_show(self):
        state_id, city_id = self.make_state_and_city("Fremont")
        user_id = self.run_cmd(
            'create User email="my@me.com" password="pwd" '
            'first_name="FN" last_name="LN"')
        place_id = self.run_cmd(
            'create Place city_id="{}" user_id="{}" name="My_house" '
            'description="no_description_yet" number_rooms=4 '
            'number_bathrooms=1 max_guest=3 price_by_night=100 '
            'latitude=120.12 longitude=101.4'.format(city_id, user_id))
        out = self.run_cmd("show Place {}".format(place_id))
        for part in ("'name': 'My house'", "'number_rooms': 4",
                     "'max_guest': 3", "'price_by_night': 100",
                     "'latitude': 120.12", "'longitude': 101.4",
                     "'description': 'no description yet'"):
            self.assertIn(part, out)

    def test_negative_zero_and_long_float(self):
        place_id = self.run_cmd(
            'create Place name="X" number_bathrooms=0 max_guest=-3 '
            'latitude=-120.12 longitude=0.41921928')
        place = self.obj("Place." + place_id)
        self.assertEqual(place.number_bathrooms, 0)
        self.assertEqual(place.max_guest, -3)
        self.assertEqual(place.latitude, -120.12)
        self.assertEqual(place.longitude, 0.41921928)

    def test_escaped_quote_in_string(self):
        new_id = self.run_cmd('create State name="He_said_\\"hi\\""')
        self.assertEqual(self.obj("State." + new_id).name, 'He said "hi"')


if __name__ == "__main__":
    unittest.main()
