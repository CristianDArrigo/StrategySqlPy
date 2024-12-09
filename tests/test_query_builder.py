import unittest
from querykit.core.query_builder import QueryBuilder
from querykit.core.query_strategy import StandardQueryStrategy
from querykit.core.sql_query import SQLQuery

class TestQueryBuilder(unittest.TestCase):

    def setUp(self):
        self.strategy = StandardQueryStrategy()
        self.builder = QueryBuilder(self.strategy)

    def test_from_table(self):
        query = self.builder.select(['name', 'age']).from_table('users').build()
        self.assertIn('FROM users', query.parse())

    def test_where(self):
        query = self.builder.select(['name', 'age']).from_table('users').where('age > 30').build()
        self.assertIn('WHERE age > 30', query.parse())

    def test_select_with_subquery(self):
        subquery = SQLQuery(self.strategy)
        subquery.set_select(['*'])
        subquery.set_from('users')
        query = self.builder.select_with_subquery(subquery, 'sub_alias').build()
        self.assertIn('(SELECT * FROM users) AS sub_alias', query.parse())

    def test_from_with_subquery(self):
        from querykit.core.query_components import Where
        subquery = SQLQuery(self.strategy)
        subquery.set_select(['*'])
        subquery.set_from('users')
        subquery.add_component(Where('age > 30'))
        query = self.builder.select(['name', 'age']).from_with_subquery(subquery, 'sub_alias').build()
        self.assertIn('FROM (SELECT * FROM users WHERE age > 30) AS sub_alias', query.parse())

    def test_group_by(self):
        query = self.builder.select(['name', 'age']).from_table('users').group_by(['age']).build()
        self.assertIn('GROUP BY age', query.parse())

    def test_order_by(self):
        query = self.builder.select(['name', 'age']).from_table('users').order_by(['age'], 'DESC').build()
        self.assertIn('ORDER BY age DESC', query.parse())

    def test_join(self):
        query = self.builder.select(['users.name', 'orders.id']).from_table('users').join('orders', 'users.id = orders.user_id').build()
        self.assertIn('JOIN orders ON users.id = orders.user_id', query.parse())

    def test_delete(self):
        query = self.builder.delete('users').build()
        self.assertIn('DELETE FROM users', query.parse())

if __name__ == '__main__':
    unittest.main()