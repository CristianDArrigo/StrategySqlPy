from typing import List
from querykit.core.query_components import SQLQueryComponent


# Strategy interface
class QueryStrategy:
    """
    Interface for query building strategies.
    """

    def build_query(self, components: List[SQLQueryComponent]) -> str:
        raise NotImplementedError("Must be implemented in subclasses")


# Concrete strategies
class StandardQueryStrategy(QueryStrategy):
    """
    Simple strategy to concatenate components in order.
    """

    def build_query(self, components: List[SQLQueryComponent]) -> str:
        return " ".join(component.to_sql() for component in components)
