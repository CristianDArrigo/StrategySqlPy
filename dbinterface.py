from abc import ABC, abstractmethod
import sqlite3  # Example of a database module that can be used with this interface


def cursor_manager(func):
        def wrapper(self, query: str, params: tuple = ()):
            cursor = None
            try:
                cursor = self.connection.cursor()  # Crea il cursore
                result = func(self, cursor, query, params)  # Esegue la funzione originale
                self.connection.commit()  # Effettua il commit per operazioni non-SELECT
                return result
            except Exception as e:
                if self.connection:
                    self.connection.rollback()  # Rollback in caso di errore
                raise RuntimeError(f"Error executing query: {e}")
            finally:
                if cursor:
                    cursor.close()  # Chiude sempre il cursore
        return wrapper


class DBInterface(ABC):
    @abstractmethod
    def connect(self):
        """Establish connection to the database."""
        pass

    @abstractmethod
    @cursor_manager
    def execute_query(self, query: str, params: tuple = ()):
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

    
    @cursor_manager
    def execute_query(self, query: str, params: tuple = ()):
        cursor.execute(query, params)
        if query.upper().startswith("SELECT"):
            return cursor.fetchall()

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from SQLite database.")
