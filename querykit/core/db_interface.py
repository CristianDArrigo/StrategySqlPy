from abc import ABC, abstractmethod
import sqlite3
import mysql.connector


class DBInterface(ABC):
    """
    DBInterface is an abstract base class that defines the interface for database operations.

    Methods
    -------
    connect():
        Establishes a connection to the database.

    execute_query(query: str, params: tuple = ()):
        Executes a query on the database with optional parameters.

    disconnect():
        Closes the database connection.
    """

    @abstractmethod
    def connect(self):
        """Establish connection to the database."""
        pass

    @abstractmethod
    def execute_query(self, query: str, params: tuple = ()):
        """Execute a query on the database."""
        pass

    @abstractmethod
    def disconnect(self):
        """Close the database connection."""
        pass


class SQLiteInterface(DBInterface):
    """
    A class to interface with an SQLite database.

    Attributes:
    -------
    db_path (str): The file path to the SQLite database.
    connection (sqlite3.Connection | None): The connection object to the SQLite database.

    Methods:
    -------
    __init__(db_path: str):
        Initializes the SQLiteInterface with the given database path.

    connect():
        Establishes a connection to the SQLite database.

    execute_query(query: str, params: tuple = ()):
        Executes the given SQL query with optional parameters.
        If the query is a SELECT statement, returns the fetched results.
        Rolls back the transaction and raises a RuntimeError if an error occurs.

    disconnect():
        Closes the connection to the SQLite database if it is open.
    """

    def __init__(self, db_path: str, verbose: bool = False):
        self.db_path = db_path
        self.connection: sqlite3.Connection | None = None
        self.verbose = verbose

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        if self.verbose:
            print(f"[+] Connected to SQLite database: {self.db_path}")

    def execute_query(self, query: str, params: tuple = ()):
        assert self.connection, "Database connection not established."
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
        except Exception as e:
            self.connection.rollback()
            raise RuntimeError(f"Error executing query: {e}")
        finally:
            cursor.close()

    def disconnect(self):
        if self.connection:
            self.connection.close()
            if self.verbose:
                print(f"[-] Disconnected from SQLite database: {self.db_path}")


class MySQLInterface(DBInterface):
    """MySQLInterface is a class that provides an interface to interact with a MySQL database.

    Attributes:
    -------
    connection: The MySQL database connection object.
    host: The host address of the MySQL
    user: The username to connect to the MySQL database
    password: The password to connect to the MySQL database
    db: The database name to connect

    Methods:
    -------
    __init__(host: str, user: str, password: str, db: str):
        Initializes the MySQLInterface with the given connection parameters.

    connect():
        Establishes a connection to the MySQL database using the provided credentials.

    execute_query(query: str, params: tuple = ()):
        Executes the given SQL query with optional parameters. If the query is a SELECT statement, returns the fetched results.

    disconnect():
        Closes the connection to the MySQL database if it is open."""

    def __init__(
        self, host: str, user: str, password: str, db: str, verbose: bool = False
    ):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.connection = None
        self.verbose = verbose

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host, user=self.user, password=self.password, database=self.db
        )
        if self.verbose:
            print(f"[+] Connected to MySQL DB @{self.host}")

    def execute_query(self, query: str, params: tuple = ()):
        assert self.connection, "Database connection not established."
        with self.connection.cursor() as cursor:
            try:
                print(query, params)
                cursor.execute(query, params)
                if query.strip().upper().startswith("SELECT"):
                    return cursor.fetchall()
            except Exception as e:
                self.connection.rollback()
                raise RuntimeError(f"Error executing query: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            if self.verbose:
                print(f"[-] Disconnected from MySQL DB @{self.host}")
