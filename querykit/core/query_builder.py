from typing import List
from querykit.core.query_components import *
from querykit.core.query_strategy import QueryStrategy
from querykit.core.sql_query import SQLQuery, Subquery


# Builder Pattern
class QueryBuilder:
    """
    Builder for creating SQLQuery instances with a fluent interface.

    ! IMPORTANT !
    Each query builder instance should be used to build a single query, as it maintains state.
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
    

    def select_with_subquery(self, subquery: SQLQuery, alias: str):
        """
        Adds a SELECT clause with a subquery.
        E.g. SELECT (SELECT * FROM users) AS sub_alias
        """
        self.query.add_component(Select([f"{Subquery(subquery).to_sql()} AS {alias}"]))
        return self
    
    def from_with_subquery(self, subquery: SQLQuery, alias: str):
        """
        Sets the FROM clause using a subquery.

        Parameters:
        subquery (SQLQuery): The subquery to use in the FROM clause.
        alias (str): The alias for the subquery.

        Returns:
        QueryBuilder: The current instance for method chaining.

        Example:
        SELECT name, age FROM (SELECT * FROM users WHERE age > 30) AS sub_alias
        """
        self.query.set_from(f"({subquery.parse()}) AS {alias}")
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