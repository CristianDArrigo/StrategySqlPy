import unittest
import sqlite3
from mysql.connector import connect, Error as MySQLError
from querykit.core.db_interface import SQLiteInterface, MySQLInterface

class TestSQLiteInterface(unittest.TestCase):
    def setUp(self):
        self.db_path = ":memory:"
        self.db = SQLiteInterface(self.db_path, verbose=True)
        self.db.connect()

    def tearDown(self):
        self.db.disconnect()

    def test_connect(self):
        self.assertIsNotNone(self.db.connection)

    def test_execute_query_create_table(self):
        create_table_query = "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
        self.db.execute_query(create_table_query)
        result = self.db.execute_query("SELECT name FROM sqlite_master WHERE type='table' AND name='test'")
        self.assertEqual(len(result), 1)

    def test_execute_query_insert_and_select(self):
        self.db.execute_query("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
        self.db.execute_query("INSERT INTO test (name) VALUES (?)", ("Alice",))
        result = self.db.execute_query("SELECT * FROM test WHERE name=?", ("Alice",))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Alice")

    def test_execute_query_error(self):
        with self.assertRaises(RuntimeError):
            self.db.execute_query("SELECT * FROM non_existing_table")


class TestMySQLInterface(unittest.TestCase):
    def setUp(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "password"
        self.db_name = "test_db"
        self.db = MySQLInterface(self.host, self.user, self.password, self.db_name, verbose=True)
        try:
            self.db.connect()
        except MySQLError:
            self.skipTest("MySQL server not available")

    def tearDown(self):
        self.db.disconnect()

    def test_connect(self):
        self.assertIsNotNone(self.db.connection)

    def test_execute_query_create_table(self):
        create_table_query = "CREATE TABLE IF NOT EXISTS test (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255))"
        self.db.execute_query(create_table_query)
        result = self.db.execute_query("SHOW TABLES LIKE 'test'")
        self.assertEqual(len(result), 1)

    def test_execute_query_insert_and_select(self):
        self.db.execute_query("CREATE TABLE IF NOT EXISTS test (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255))")
        self.db.execute_query("INSERT INTO test (name) VALUES (%s)", ("Alice",))
        result = self.db.execute_query("SELECT * FROM test WHERE name=%s", ("Alice",))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Alice")

    def test_execute_query_error(self):
        with self.assertRaises(RuntimeError):
            self.db.execute_query("SELECT * FROM non_existing_table")


if __name__ == "__main__":
    unittest.main()