## PostgresStudy Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Downloaded. 10 December 2025 ](../../images/postgres_study_guide_title_img.png)

### What are the different type of indexes available in postgres and when to use each one?

PostgreSQL provides different indexes for different purposes

B-Tree index: Are good for equality and range search in ordered columns. 
Hash index: 32 bit hash code derived from the value. Handle simple equality operations. 

GIN index: Inverted indexes appropriate for columns that contain multi component values such as arrays. An inverted index contains an entry for each value. Can handle queries that test for the presence of specific components. 

gist index: Good for text search. They also allow to optimize for nearest neighbor searches. 

BRIN index: Date-based range queries. 

### What does ACID stand for?

Acid are properties of database transactions should have very used in OLTP systems. Their objective is to provide data validity despite errors or failures. 

Atomicity: Guarantees that each transaction is treated as a single unit that either succeds or fails.
Consistency: Ensures that a transaction can only bring the database from a consistent state to another. 
Isolation: Transactions are executed concurrently 
Durability: Ensures that a transaction once commited will state commited even if the system fails.

### How to create a new database in postgresql

```sql
CREATE DATABASE my_database;
```

### How to create a table in postgresql


### What's a primary key in postgres?


### Which are the main OLAP operations in an OLAP system?

Olap operations are based on a multidimensional model where data is represented in the form of cubes. 

There are five basic analysitcal operations.

- Drill Down: moves to a more detailed level in the hierarchy. It moves from a summary level to a lower level for example: Year -> Quarter -> Month
- Roll up: Is the opposite of Drill down it aggregates data into a higher level of hierarchy. Ex: city -> country, month -> quarter
- Slice: Selects a single dimension from the cube creating sub cube with reduce dimensionality. Focus on one dimension for example: slice Q1
- Dice operation: Apply filters to two or more dimmensions to get a subcube. ex: location -> Bogota, Product -> Coffee
- Pivot: invert the order of the dimensions to analyze data differently

### Name the three main normal forms


