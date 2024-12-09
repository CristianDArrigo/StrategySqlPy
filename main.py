from querykit.core.execution_strategy import PrintExecutionStrategy
from querykit.core.query_builder import QueryBuilder
from querykit.core.query_strategy import StandardQueryStrategy

# Subquery Builder: SELECT * FROM users WHERE age > 30
subquery_strategy = StandardQueryStrategy()
subquery_builder = QueryBuilder(subquery_strategy)
subquery = subquery_builder.select(["*"]).from_table("users").where("age > 30").build()
print(subquery.parse())

# Main Query Builder: SELECT name, age FROM (SELECT * FROM users WHERE age > 30) AS sub_alias
main_strategy = StandardQueryStrategy()
main_builder = QueryBuilder(main_strategy)
query = main_builder.select(["name", "age"]).from_with_subquery(subquery, "sub_alias").build()

# Execute with PrintExecutionStrategy
execution_strategy = PrintExecutionStrategy()
execution_strategy.execute(query)
