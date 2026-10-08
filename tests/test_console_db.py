#!/usr/bin/python3
"""Console create tests against a real MySQL database (DBStorage only)"""
import os
import unittest
from io import StringIO
from unittest.mock import patch

DB_MODE = os.getenv('HBNB_TYPE_STORAGE') == 'db'

if DB_MODE:
    import MySQLdb
    from console import HBNBCommand


def query(sql, args=()):
    """Runs a query through MySQLdb (not SQLAlchemy), returns all rows"""
    conn = MySQLdb.connect(host=os.getenv('HBNB_MYSQL_HOST'),
                           user=os.getenv('HBNB_MYSQL_USER'),
                           passwd=os.getenv('HBNB_MYSQL_PWD'),
                           db=os.getenv('HBNB_MYSQL_DB'))
    cur = conn.cursor()
    cur.execute(sql, args)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def count(table):
    """Number of rows currently in a table"""
    return query("SELECT COUNT(*) FROM {}".format(table))[0][0]


def run(line):
    """Runs one console command and returns what it printed"""
    with patch('sys.stdout', new=StringIO()) as out:
        HBNBCommand().onecmd(line)
        return out.getvalue().strip()


@unittest.skipUnless(DB_MODE, "DBStorage only")
class TestCreateDB(unittest.TestCase):
    """create <Class> key=value against MySQL"""

    def test_create_state_adds_one_row(self):
        before = count('states')
        run('create State name="California"')
        self.assertEqual(count('states'), before + 1)

    def test_create_state_and_city_add_rows(self):
        states = count('states')
        cities = count('cities')
        state_id = run('create State name="California"')
        run('create City state_id="{}" name="Fremont"'.format(state_id))
        self.assertEqual(count('states'), states + 1)
        self.assertEqual(count('cities'), cities + 1)

    def test_space_translated_in_db(self):
        state_id = run('create State name="California"')
        city_id = run(
            'create City state_id="{}" name="San_Francisco"'.format(state_id))
        rows = query("SELECT name FROM cities WHERE id = %s", (city_id,))
        self.assertEqual(rows[0][0], "San Francisco")

    def test_city_with_unknown_state_adds_nothing(self):
        before = count('cities')
        run('create City state_id="nope" name="Fremont"')
        self.assertEqual(count('cities'), before)


if __name__ == "__main__":
    unittest.main()
