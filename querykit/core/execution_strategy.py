from querykit.core.sql_query import SQLQuery
from querykit.core.db_interface import DBInterface


# Execution Strategy
class ExecutionStrategy:
    """
    Base class for executing SQL queries.
    """

    def execute(self, query: SQLQuery):
        raise NotImplementedError("Must be implemented in subclasses")


class PrintExecutionStrategy(ExecutionStrategy):
    """
    Simple execution strategy that prints the query. (For testing purposes)
    """

    def execute(self, query: SQLQuery):
        print(query.parse())
        # logger.info(f"Query executed via PrintExecutionStrategy: {query.execute()}")


class DBExecutionStrategy(ExecutionStrategy):
    def __init__(self, db_interface: DBInterface):
        self.db_interface = db_interface

    def execute(self, query: SQLQuery, params: tuple = ()):
        query_string = query.parse()
        return self.db_interface.execute_query(query_string, params)
