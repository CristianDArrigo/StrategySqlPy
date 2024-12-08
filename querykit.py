# sql_query_library.py

from typing import List, Optional
import logging
from dbinterface import DBInterface, SQLiteInterface

"""
SQL Query Library

This library provides a flexible and extensible way to build SQL queries using components and strategies.
The library is designed to be independent of any specific database, focusing on query generation.

Features:
- Component-based query construction (SELECT, FROM, WHERE, etc.)
- Strategy pattern for flexible query building
- Support for additional SQL components like UPDATE, DELETE, LIMIT, and INSERT
- Validation of query structure and logical consistency
- Builder Pattern for fluent query creation
- Execution strategies for running queries
"""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base class for all query components
class SQLQueryComponent:
    """
    Abstract base class for query components.
    Each component must implement the `to_sql` method.
    """
    def to_sql(self) -> str:
        raise NotImplementedError("Must be implemented in subclasses")

# Query components
class Select(SQLQueryComponent):
    """
    Represents the SELECT clause of a SQL query.
    """
    def __init__(self, columns: List[str]):
        self.columns = columns

    def to_sql(self) -> str:
        return f"SELECT {', '.join(self.columns)}"

class From(SQLQueryComponent):
    """
    Represents the FROM clause of a SQL query.
    """
    def __init__(self, table: str):
        self.table = table

    def to_sql(self) -> str:
        return f"FROM {self.table}"

class Where(SQLQueryComponent):
    """
    Represents the WHERE clause of a SQL query.
    """
    def __init__(self, condition: str):
        self.condition = condition

    def to_sql(self) -> str:
        return f"WHERE {self.condition}"

class OrderBy(SQLQueryComponent):
    """
    Represents the ORDER BY clause of a SQL query.
    """
    def __init__(self, columns: List[str], order: Optional[str] = "ASC"):
        self.columns = columns
        self.order = order

    def to_sql(self) -> str:
        return f"ORDER BY {', '.join(self.columns)} {self.order}"

class Join(SQLQueryComponent):
    """
    Represents a JOIN clause in a SQL query.
    """
    def __init__(self, table: str, condition: str):
        self.table = table
        self.condition = condition

    def to_sql(self) -> str:
        return f"JOIN {self.table} ON {self.condition}"

class GroupBy(SQLQueryComponent):
    """
    Represents the GROUP BY clause of a SQL query.
    """
    def __init__(self, columns: List[str]):
        self.columns = columns

    def to_sql(self) -> str:
        return f"GROUP BY {', '.join(self.columns)}"

class Update(SQLQueryComponent):
    """
    Represents the UPDATE clause of a SQL query.
    """
    def __init__(self, table: str):
        self.table = table

    def to_sql(self) -> str:
        return f"UPDATE {self.table}"

class Set(SQLQueryComponent):
    """
    Represents the SET clause in an UPDATE statement.
    """
    def __init__(self, updates: List[str]):
        self.updates = updates

    def to_sql(self) -> str:
        return f"SET {', '.join(self.updates)}"

class Delete(SQLQueryComponent):
    """
    Represents a DELETE statement in SQL.
    """
    def __init__(self, table: str):
        self.table = table

    def to_sql(self) -> str:
        return f"DELETE FROM {self.table}"

class Limit(SQLQueryComponent):
    """
    Represents the LIMIT clause of a SQL query.
    """
    def __init__(self, limit: int, offset: Optional[int] = None):
        self.limit = limit
        self.offset = offset

    def to_sql(self) -> str:
        if self.offset is not None:
            return f"LIMIT {self.limit} OFFSET {self.offset}"
        return f"LIMIT {self.limit}"

class Insert(SQLQueryComponent):
    """
    Represents an INSERT INTO statement in SQL.
    """
    def __init__(self, table: str, columns: List[str], values: List[str]):
        self.table = table
        self.columns = columns
        self.values = values

    def to_sql(self) -> str:
        columns = ", ".join(self.columns)
        values = ", ".join(f"'{v}'" for v in self.values)
        return f"INSERT INTO {self.table} ({columns}) VALUES ({values})"

# Strategy interface
class QueryStrategy:
    """
    Interface for query building strategies.
    """
    def build_query(self, components: List[SQLQueryComponent]) -> str:
        raise NotImplementedError("Must be implemented in subclasses")

# Concrete strategies
class SimpleQueryStrategy(QueryStrategy):
    """
    Simple strategy to concatenate components in order.
    """
    def build_query(self, components: List[SQLQueryComponent]) -> str:
        return " ".join(component.to_sql() for component in components)

# Context class
class SQLQuery:
    """
    Context for building and executing SQL queries.
    """
    def __init__(self, strategy: QueryStrategy):
        self.strategy = strategy
        self.components: List[SQLQueryComponent] = []
        self.select_component = None
        self.from_component = None

    def set_select(self, columns: List[str]):
        """
        Set the SELECT clause of the query.
        """
        self.select_component = Select(columns)

    def set_from(self, table: str):
        """
        Set the FROM clause of the query.
        """
        self.from_component = From(table)

    def add_component(self, component: SQLQueryComponent):
        """
        Add a component to the query.
        """
        self.components.append(component)

    def set_strategy(self, strategy: QueryStrategy):
        """
        Set the query building strategy.
        """
        self.strategy = strategy

    def validate(self):
        """
        Validate the structure and logical consistency of the query.
        """
        if self.select_component and not self.from_component:
            raise ValueError("SELECT query requires a FROM clause.")
        if any(isinstance(c, Update) for c in self.components) and not any(isinstance(c, Set) for c in self.components):
            raise ValueError("UPDATE query requires a SET clause.")
        if any(isinstance(c, Delete) for c in self.components) and self.from_component:
            raise ValueError("DELETE query should not have a FROM clause explicitly.")

    def execute(self) -> str:
        """
        Build and return the SQL query string.
        """
        self.validate()

        full_components = []
        if self.select_component:
            full_components.append(self.select_component)
        if self.from_component:
            full_components.append(self.from_component)
        full_components.extend(self.components)

        query = self.strategy.build_query(full_components)
        return query

# Execution Strategy
class ExecutionStrategy:
    """
    Base class for executing SQL queries.
    """
    def execute(self, query: SQLQuery):
        raise NotImplementedError("Must be implemented in subclasses")

class PrintExecutionStrategy(ExecutionStrategy):
    """
    Simple execution strategy that prints the query.
    """
    def execute(self, query: SQLQuery):
        print(query.execute())
        # logger.info(f"Query executed via PrintExecutionStrategy: {query.execute()}")

class MockExecutionStrategy(ExecutionStrategy):
    """
    Mock execution strategy that simulates query execution.
    """
    def execute(self, query: SQLQuery):
        query_string = query.execute()
        return {"status": "success", "query": query_string}
    

class DBExecutionStrategy(ExecutionStrategy):
    def __init__(self, db_interface: DBInterface):
        self.db_interface = db_interface

    def execute(self, query: SQLQuery):
        self.db_interface.connect()
        try:
            query_string = query.execute()
            print(f"Executing query: {query_string}")
            results = self.db_interface.execute_query(query_string)
            print(f"Results: {results}")
            return results
        finally:
            self.db_interface.disconnect()


# Builder Pattern
class QueryBuilder:
    """
    Builder for creating SQLQuery instances with a fluent interface.
    """
    def __init__(self, strategy: QueryStrategy):
        self.query = SQLQuery(strategy)

    def select(self, columns: List[str]):
        self.query.set_select(columns)
        return self

    def from_table(self, table: str):
        self.query.set_from(table)
        return self

    def where(self, condition: str):
        self.query.add_component(Where(condition))
        return self

    def group_by(self, columns: List[str]):
        self.query.add_component(GroupBy(columns))
        return self

    def order_by(self, columns: List[str], order: str = "ASC"):
        self.query.add_component(OrderBy(columns, order))
        return self

    def join(self, table: str, condition: str):
        self.query.add_component(Join(table, condition))
        return self
    
    def delete(self, table: str):
        self.query.add_component(Delete(table))
        return self

    def build(self) -> SQLQuery:
        return self.query

# Example usage
if __name__ == "__main__":
    # Using Builder Pattern
    strategy = SimpleQueryStrategy()
    builder = QueryBuilder(strategy)

    query = (
        builder
        .select(["id", "name", "age"])
        .from_table("users")
        .where("age > 30")
        .join("addresses", "users.id = addresses.user_id")
        .group_by(["age"])
        .order_by(["name"], "DESC")
        .build()
    )

    print_strategy = PrintExecutionStrategy()
    mock_strategy = MockExecutionStrategy()
    db_strategy = DBExecutionStrategy(SQLiteInterface("example.db"))  # Let's suppose we have a SQLite database

    print_strategy.execute(query)

    result = mock_strategy.execute(query)
    print(result)

    # Update query example
    update_query = SQLQuery(strategy)
    update_query.add_component(Update(table="users"))
    update_query.add_component(Set(updates=["name = 'John'", "age = 25"]))
    update_query.add_component(Where(condition="id = 1"))
    print_strategy.execute(update_query)

    # Delete query example
    delete_query = SQLQuery(strategy)
    delete_query.add_component(Delete(table="users"))
    delete_query.add_component(Where(condition="age < 18"))
    
    db_strategy.execute(delete_query)  # Execute the delete query using the DBExecutionStrategy
