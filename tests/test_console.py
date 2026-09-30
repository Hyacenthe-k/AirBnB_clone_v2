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


if __name__ == "__main__":
    unittest.main()
