# QueryKit

QueryKit is a flexible and extensible Python library for programmatically building and executing SQL queries. Designed with modern software engineering practices, QueryKit leverages design patterns like the Builder Pattern, Strategy Pattern, and interfaces to offer a modular, maintainable, and database-agnostic solution for query generation and execution.

---

## Features

### 1. **Component-Based Query Construction**
QueryKit allows you to build SQL queries using modular components, such as:
- `SELECT`, `FROM`, `WHERE`
- `JOIN`, `GROUP BY`, `ORDER BY`
- `INSERT`, `UPDATE`, `DELETE`
- `LIMIT`

Each component encapsulates its own logic and is responsible for converting itself into SQL syntax.

### 2. **Builder Pattern for Fluent Query Creation**
The Builder Pattern simplifies query creation with a readable and intuitive API:
```python
query = (
    QueryBuilder(StandardQueryStrategy())
    .select(["id", "name", "email"])
    .from_table("users")
    .where("age > 18")
    .order_by(["name"], "ASC")
    .build()
)
```

### 3. **Strategy Pattern for Query Assembly**
The library uses the [Strategy Pattern](https://en.wikipedia.org/wiki/Strategy_pattern) to define customizable methods for assembling query components. 

- `StandardQueryStrategy`: A default implementation that concatenates components linearly.

### 4. **Database-Agnostic Execution**
QueryKit includes interfaces (`DBInterface`) for interacting with multiple database systems. Supported databases include:
- SQLite
- MySQL

### 5. **Validation Mechanism**
Queries are validated before execution to ensure logical consistency, such as:
- `SELECT` queries must include a `FROM` clause.
- `UPDATE` queries require a `SET` clause.
- `DELETE` queries should not include an explicit `FROM` clause.

### 6. **Extensibility**
Users can:
- Add custom SQL components.
- Define new query strategies.
- Implement custom database interfaces by extending `DBInterface`.

---

## Installation

Clone the repository and install the dependencies:
```bash
git clone https://github.com/CristianDArrigo/StrategySqlPy.git
cd StrategySqlPy
pip install -r requirements.txt
```

---

## Usage

### **1. Basic Query Building and Execution**

#### Building a SELECT Query:
```python
from querykit.core.query_builder import QueryBuilder
from querykit.core.query_strategy import StandardQueryStrategy
from querykit.core.db_interface import SQLiteInterface
from querykit.core.execution_strategy import DBExecutionStrategy

# Configure the database
db_interface = SQLiteInterface("example.db")
db_interface.connect()
execution_strategy = DBExecutionStrategy(db_interface)

# Build a SELECT query
query = (
    QueryBuilder(StandardQueryStrategy())
    .select(["id", "name", "email"])
    .from_table("users")
    .where("age > 18")
    .order_by(["name"], "ASC")
    .build()
)

# Execute the query
results = execution_strategy.execute(query)
print(results)

db_interface.disconnect()
```

#### Output:
If the `users` table contains:
| id | name      | email              | age |
|----|-----------|--------------------|-----|
| 1  | Alice     | alice@example.com  | 25  |
| 2  | Bob       | bob@example.com    | 20  |
| 3  | Charlie   | charlie@example.com| 17  |

The output will be:
```
[(1, 'Alice', 'alice@example.com'), (2, 'Bob', 'bob@example.com')]
```

### **2. Custom Database Interface**

#### Example: MySQL Interface
```python
from querykit.core.db_interface import MySQLInterface
from querykit.core.execution_strategy import DBExecutionStrategy
from querykit.core.query_builder import QueryBuilder
from querykit.core.query_strategy import StandardQueryStrategy

# Configure the MySQL database
mysql_interface = MySQLInterface(host="localhost", user="root", password="root", db="example_db", verbose=True)
mysql_interface.connect()
execution_strategy = DBExecutionStrategy(mysql_interface)

# Build a query
query = (
    QueryBuilder(StandardQueryStrategy())
    .select(["id", "name"])
    .from_table("users")
    .where("age < 30")
    .build()
)

# Execute the query
results = execution_strategy.execute(query)
print(results)

mysql_interface.disconnect()
```

---

## Architecture Overview

### **Key Components**

#### 1. **SQLQuery**
- Represents the context for a SQL query.
- Manages components and validates logical consistency.

#### 2. **Query Components**
- Encapsulate SQL clauses like `SELECT`, `WHERE`, `ORDER BY`, etc.
- Located in `querykit/core/query_components.py`.

#### 3. **Query Strategies**
- Define how query components are assembled.
- Located in `querykit/core/query_strategy.py`.

#### 4. **Execution Strategies**
- Handle query execution logic.
- Includes `PrintExecutionStrategy` (for debugging) and `DBExecutionStrategy` (for real databases).

#### 5. **Database Interfaces**
- Provide a standardized interface for interacting with different databases.
- Includes `SQLiteInterface` and `MySQLInterface`.

---

## Contribution

Contributions are welcome! Feel free to open issues or submit pull requests to:
- Add support for new databases.
- Extend the validation logic.
- Introduce advanced SQL features.

### Development Setup
```bash
# Clone the repository
git https://github.com/CristianDArrigo/StrategySqlPy.git
cd StrategySqlPy

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest
```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Roadmap

1. Add support for PostgreSQL and other databases.
2. Enhance validation for more complex queries.
3. Introduce advanced features like subqueries and transactions.
4. Implement a CLI tool for generating and executing queries.

---

## Contact

For questions or feedback, feel free to reach out at [cristiandarrigo0@gmail.com].
