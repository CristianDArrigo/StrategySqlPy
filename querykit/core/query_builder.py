from typing import List
from querykit.core.query_components import *
from querykit.core.query_strategy import QueryStrategy
from querykit.core.sql_query import SQLQuery


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
