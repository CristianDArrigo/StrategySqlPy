from abc import ABC, abstractmethod
import sqlite3  # Example of a database module that can be used with this interface


class DBInterface(ABC):
    @abstractmethod
    def connect(self):
        """Establish connection to the database."""
        pass

    @abstractmethod
    def execute_query(self, query: str):
        """Execute a query on the database."""
        pass

    @abstractmethod
    def disconnect(self):
        """Close the database connection."""
        pass


class SQLiteInterface(DBInterface):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        print("Connected to SQLite database.")

    def execute_query(self, query: str):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            self.connection.commit()
            return results
        except Exception as e:
            print(f"Error executing query: {e}")
            raise

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from SQLite database.")
