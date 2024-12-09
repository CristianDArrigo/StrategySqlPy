from typing import List
from querykit.core.query_components import *
from querykit.core.query_strategy import QueryStrategy


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
        if any(isinstance(c, Update) for c in self.components) and not any(
            isinstance(c, Set) for c in self.components
        ):
            raise ValueError("UPDATE query requires a SET clause.")
        if any(isinstance(c, Delete) for c in self.components) and self.from_component:
            raise ValueError("DELETE query should not have a FROM clause explicitly.")

        # Ensure subqueries are properly validated
        for component in self.components:
            if isinstance(component, Subquery):
                component.query.validate()

    def parse(self) -> str:
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


class Subquery(SQLQueryComponent):
    """
    Represents a subquery that can be used in various SQL clauses.
    """

    def __init__(self, query: SQLQuery):
        """
        Initializes a Subquery with an SQLQuery instance.

        Parameters:
        query (SQLQuery): The subquery to embed.
        """
        self.query = query

    def to_sql(self) -> str:
        """
        Converts the subquery to a string representation wrapped in parentheses.
        """
        return f"({self.query.parse()})"