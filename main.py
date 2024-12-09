# example where we connect to a MySQL database and execute a query

from querykit.core.db_interface import MySQLInterface
from querykit.core.execution_strategy import DBExecutionStrategy
from querykit.core.query_builder import QueryBuilder
from querykit.core.query_strategy import StandardQueryStrategy

# Connect to MySQL database
db_interface = MySQLInterface(
    host="localhost", user="user", password="password", db="database"
)
db_interface.connect()

# Create a query builder with a strategy
query_builder = QueryBuilder(strategy=StandardQueryStrategy())

# Build a query
query = query_builder.select(["*"]).from_table("users").where("id = %s").build()

# Execute the query
execution_strategy = DBExecutionStrategy(db_interface)
result = execution_strategy.execute(query, params=(1,))

# Print the result
print(result)
