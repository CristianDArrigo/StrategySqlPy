# SQL Query Library

A flexible and extensible Python library for building SQL queries programmatically. This library utilizes modern software design patterns to ensure modularity, maintainability, and ease of use. It is database-agnostic, focusing purely on query generation while leaving execution up to user-defined strategies.

## Features

### 1. **Component-Based Query Construction**
The library provides abstractions for SQL components such as `SELECT`, `WHERE`, `ORDER BY`, `INSERT`, and more. Each component is represented as a class that converts its attributes into SQL syntax.

### 2. **Strategy Pattern for Query Construction**
The library uses the [Strategy Pattern](https://en.wikipedia.org/wiki/Strategy_pattern) to define different methods for assembling query components. For example, the `SimpleQueryStrategy` concatenates components linearly, ensuring a clean and structured query output.

### 3. **Builder Pattern for Fluent Query Creation**
The [Builder Pattern](https://en.wikipedia.org/wiki/Builder_pattern) is implemented to provide a fluent interface for query creation. This enables users to chain method calls to define queries in an intuitive and readable manner.

### 4. **Execution Strategies**
The library introduces an `ExecutionStrategy` base class to allow custom execution logic for queries. Examples include:
- `PrintExecutionStrategy` for printing queries.
- `MockExecutionStrategy` for simulating query execution.

### 5. **Validation Mechanism**
Queries are validated before execution to ensure logical consistency, such as verifying that a `SELECT` query includes a `FROM` clause or that an `UPDATE` query includes a `SET` clause.

---

## Installation

Simply clone the repository and include the `querykit.py` in your project.

```bash
git clone https://github.com/CristianDArrigo/StrategySqlPy.git
cd StrategySqlPy
```

---

## Usage

### **1. Building Queries with the Builder Pattern**

```python
from querykit import QueryBuilder, SimpleQueryStrategy, PrintExecutionStrategy

strategy = SimpleQueryStrategy()
builder = QueryBuilder(strategy)

query = (
    builder
    .select(["id", "name", "age"])
    .from_table("users")
    .where("age > 30")
    .join("addresses", "users.id = addresses.user_id")
    .group_by(["age"])
    .order_by(["name"], "DESC")
    .build()
)

execution_strategy = PrintExecutionStrategy()
execution_strategy.execute(query)
```

### **2. Mock Query Execution**

```python
from querykit import MockExecutionStrategy

mock_strategy = MockExecutionStrategy()
result = mock_strategy.execute(query)
print(result)
```

### **3. Update Query Example**

```python
update_query = QueryBuilder(strategy)
update_query.query.add_component(Update(table="users"))
update_query.query.add_component(Set(updates=["name = 'John'", "age = 25"]))
update_query.query.add_component(Where(condition="id = 1"))

execution_strategy.execute(update_query.query)
```

---

## Design Patterns in Use

### 1. **Strategy Pattern**
- Defines how query components are assembled.
- `SimpleQueryStrategy`: A straightforward concatenation of components.

Read more about the Strategy Pattern on [Wikipedia](https://en.wikipedia.org/wiki/Strategy_pattern).

### 2. **Builder Pattern**
- Provides a fluent interface for building queries.
- Eliminates the need to manually create and manage query components.

Learn more about the Builder Pattern on [Wikipedia](https://en.wikipedia.org/wiki/Builder_pattern).

### 3. **Execution Strategy**
- Introduces a standardized way to execute or simulate SQL queries.
- Easily extendable to support database connections or other execution behaviors.

### 4. **Validation**
- Ensures the logical structure of queries before execution, reducing runtime errors.

---

## Advantages

1. **Database-Agnostic**: Generates SQL strings that can be executed on any relational database.
2. **Extensible**: Easily add new SQL components or strategies.
3. **Fluent Interface**: The Builder Pattern ensures clean and readable query definitions.
4. **Custom Execution**: User-defined execution strategies allow flexibility in running or testing queries.

---

## Example Output

### **SELECT Query**
```sql
SELECT id, name, age FROM users JOIN addresses ON users.id = addresses.user_id WHERE age > 30 GROUP BY age ORDER BY name DESC
```

### **UPDATE Query**
```sql
UPDATE users SET name = 'John', age = 25 WHERE id = 1
```

---

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests to improve functionality, add features, or fix bugs.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
