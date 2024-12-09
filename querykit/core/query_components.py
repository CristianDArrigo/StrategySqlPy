from typing import List, Optional


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
