## PostgreSQL Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![PostgreSQL study guide: about 200 questions](../../images/postgres_study_guide_title_img.png)

About 200 questions on PostgreSQL and SQL for data engineering interviews: architecture, data types, querying, window functions, indexes, transactions and MVCC, performance tuning, data modeling, administration and advanced features such as JSONB and partitioning. Examples target PostgreSQL 16 and 17.

The guide follows a learning path in four stages. Each section is split into short units: learning goals, a concept explanation and a worked example, then questions (recall first, then application), a practical challenge and key takeaways. To **learn**, read each unit top to bottom. To **review**, switch to review mode or use "Skip to questions", mark answers you want to see again, and try a mixed review across sections.

<!-- QA -->
<!-- stage: Foundations -->

### Basics and architecture

<!-- unit: PostgreSQL architecture -->

<!-- goals -->

- Describe PostgreSQL's process model, WAL and checkpoints.
- Explain ACID and why connections are expensive.

<!-- concept -->

PostgreSQL's design explains much of its behavior. Each client connection gets its own operating system process, which is robust but costs memory, so thousands of direct connections hurt and pooling becomes necessary.

Durability comes from the write-ahead log: every change is written to the log first, data files later. After a crash, replaying the log restores committed work. Checkpoints periodically flush changed pages so the log needed for recovery stays short. Together they deliver the ACID guarantees transactional systems rely on.

<!-- example -->

```text
client ──► postmaster ──fork──► backend process (one per connection)
UPDATE ──► WAL record (fsync on COMMIT) ──► shared_buffers page (dirty)
checkpoint ──► dirty pages flushed to data files ──► old WAL recyclable
```

#### What is PostgreSQL?

An open-source, object-relational database system known for standards compliance, reliability and extensibility. It supports ACID transactions, MVCC, rich data types (JSONB, arrays, ranges), advanced SQL (window functions, CTEs), extensions and several index types.

#### What does ACID stand for?

The properties that database transactions should have, essential in OLTP systems, to keep data valid despite errors and failures:

- **Atomicity:** a transaction is a single unit that either fully succeeds or has no effect.
- **Consistency:** a transaction brings the database from one valid state to another, respecting constraints.
- **Isolation:** concurrent transactions don't interfere with each other: the result is as if they ran in some order, depending on the isolation level.
- **Durability:** once committed, a transaction survives crashes (in PostgreSQL, thanks to the write-ahead log).

#### What is the PostgreSQL process architecture?

A postmaster process accepts connections and forks one backend process per client connection. Background processes handle writing (background writer, checkpointer), the WAL writer, autovacuum, statistics and replication. All share memory such as `shared_buffers`.

#### Why does the one-process-per-connection model matter?

Each connection costs memory and a process, so thousands of direct connections hurt performance. Applications use a connection pooler such as PgBouncer or a driver-side pool.

#### What is the write-ahead log (WAL)?

A log where every change is recorded before data files are modified. After a crash, PostgreSQL replays the WAL to restore a consistent state. The WAL also drives replication and point-in-time recovery.

#### What is a checkpoint?

The moment when all dirty pages in memory are flushed to the data files, so older WAL is no longer needed for crash recovery. Checkpoint frequency is controlled by `checkpoint_timeout` and `max_wal_size`.

<!-- challenge -->

A server loses power mid-transaction. On restart, are committed transactions present and uncommitted ones gone? Why?

<!-- solution -->

Yes. Committed transactions had their WAL flushed to disk before `COMMIT` returned, so recovery replays them; uncommitted changes have no commit record and are discarded.

<!-- takeaways -->

- One process per connection: pool connections.
- WAL first, data files later, guarantees durability.
- Checkpoints bound recovery time.

<!-- unit: Databases, schemas and tables -->

<!-- goals -->

- Navigate clusters, databases, schemas and tables with psql.
- Create databases and tables with primary keys and understand the search path.

<!-- concept -->

PostgreSQL organizes objects in layers. A server instance holds databases, which are isolated from each other; each database holds schemas, namespaces for tables and other objects. Unqualified names are resolved through the search path, which explains many "table not found" surprises.

Everything about these objects, including tables, columns, indexes and permissions, is itself stored in system catalog tables you can query. psql is the everyday tool to explore it all.

<!-- example -->

```sql
CREATE DATABASE shop OWNER app_owner ENCODING 'UTF8';
\c shop
CREATE SCHEMA sales;
CREATE TABLE sales.company (
  company_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  country_code char(2) NOT NULL,
  business_id text NOT NULL,
  UNIQUE (country_code, business_id)
);
\dt sales.*
```

#### What is the difference between a database, a schema and a table?

A cluster (instance) contains databases. A database contains schemas (namespaces such as `public`). A schema contains tables, views, functions and other objects. A connection is made to one database, and can query several schemas in it.

#### How do you create a new database in PostgreSQL?

```sql
CREATE DATABASE my_database OWNER app_owner ENCODING 'UTF8';
```

From the shell, `createdb my_database` does the same.

#### How do you create a table in PostgreSQL?

```sql
CREATE TABLE company (
    company_id   bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    country_code char(2)      NOT NULL,
    business_id  text         NOT NULL,
    name         text,
    created_on   date,
    employees    integer CHECK (employees >= 0),
    UNIQUE (country_code, business_id)
);
```

#### What is a primary key in Postgres?

A constraint that uniquely identifies each row: its columns are `NOT NULL` and unique, and PostgreSQL creates a unique B-tree index to enforce it. A table has at most one primary key, which can span several columns.

#### What is psql?

The interactive command-line client for PostgreSQL. Useful meta-commands: `\l` lists databases, `\c` connects, `\dt` lists tables, `\d table` describes one, `\di` lists indexes, `\x` toggles expanded output, `\timing` shows query times.

#### What is the search path?

The ordered list of schemas PostgreSQL looks in for unqualified object names (`SHOW search_path`). By default `"$user", public`.

#### What is the system catalog?

Tables in `pg_catalog` (such as `pg_class`, `pg_attribute`, `pg_index`) describing every object, plus the standard `information_schema` views.

<!-- challenge -->

`SELECT * FROM orders` fails with "relation does not exist", but the table is visible in a GUI tool. What do you check?

<!-- solution -->

The schema and the search path: the table probably lives in another schema (for example `sales.orders`) that isn't in `search_path`, or in another database. Qualify the name or adjust the search path.

<!-- takeaways -->

- Instances hold databases; databases hold schemas.
- The search path resolves unqualified names.
- The system catalog describes every object.

<!-- unit: Objects beyond tables -->

<!-- goals -->

- Use sequences, identity columns, views and materialized views.
- Choose between DELETE, TRUNCATE and DROP.

<!-- concept -->

Tables are surrounded by helper objects. Sequences generate numbers for keys, and identity columns are the modern, standard way to attach them. Views store queries, recomputed on each read; materialized views store results, refreshed when you say so.

Removing data has three tools with very different effects: deleting rows one by one, truncating the whole table instantly, or dropping the table altogether.

<!-- example -->

| Operation | Removes | Speed | WHERE? | Leaves dead tuples |
|---|---|---|---|---|
| `DELETE` | Selected rows | Row by row | Yes | Yes |
| `TRUNCATE` | All rows | Instant | No | No |
| `DROP TABLE` | Table itself | Instant | No | n/a |

#### What is a sequence?

A database object that generates increasing numbers, used for surrogate keys. `GENERATED ... AS IDENTITY` columns (SQL standard) and the older `serial` types use sequences. Sequences aren't transactional: rolled-back inserts leave gaps.

#### What is the difference between `serial` and identity columns?

Both auto-generate integers from a sequence. Identity columns are standard SQL, tie the sequence to the column more cleanly, and with `GENERATED ALWAYS` prevent accidental manual values. They are preferred for new tables.

#### What is a view?

A stored query that you can select from like a table. It holds no data, and its query runs on each access. Simple views can be updatable.

#### What is a materialized view?

A view whose result is stored on disk and refreshed explicitly with `REFRESH MATERIALIZED VIEW`. With a unique index, `REFRESH ... CONCURRENTLY` refreshes it without blocking readers.

#### What is the difference between `DELETE`, `TRUNCATE` and `DROP`?

`DELETE` removes rows one by one, can have a `WHERE` clause, fires triggers and leaves dead tuples for vacuum. `TRUNCATE` empties the whole table quickly by replacing its files. `DROP` removes the table itself. In PostgreSQL, all three are transactional.

<!-- challenge -->

A nightly job empties a 50-million-row staging table with `DELETE FROM staging` and the table keeps growing on disk. What do you change?

<!-- solution -->

Use `TRUNCATE staging`, which removes all rows instantly without leaving dead tuples. `DELETE` marks rows dead and relies on vacuum to reclaim space.

<!-- takeaways -->

- Identity columns are the standard way to generate keys.
- Views recompute; materialized views store results.
- TRUNCATE empties tables without dead tuples.

<!-- unit: Physical storage -->

<!-- goals -->

- Explain how PostgreSQL stores large values with TOAST.
- Use tablespaces to place data on different disks.

<!-- concept -->

Rows live in fixed-size pages, so very large values need special handling. TOAST compresses them and, if still large, moves them to a side table, keeping the main table compact and fast to scan when those columns aren't read.

Tablespaces map objects to directories on disk, letting you put some tables or indexes on faster or larger storage. In managed services, they're rarely needed.

<!-- example -->

```sql
SELECT pg_size_pretty(pg_relation_size('documents'))        AS main,
       pg_size_pretty(pg_total_relation_size('documents'))  AS total;   -- includes TOAST and indexes
CREATE TABLESPACE fast_ssd LOCATION '/mnt/nvme/pg';
ALTER INDEX orders_created_idx SET TABLESPACE fast_ssd;
```

#### What is TOAST?

The Oversized-Attribute Storage Technique: large values (over about 2 kB) are compressed and/or stored out of line in a separate table, transparently to queries.

#### What is a tablespace?

A directory on disk where PostgreSQL can store objects, letting you put some tables or indexes on different storage.

<!-- challenge -->

A `documents` table is small on disk but `pg_total_relation_size` shows 400 GB. Where is the space, and does it slow queries that don't read the content?

<!-- solution -->

Mostly in the TOAST table holding the large `content` values. Queries that don't select that column don't read TOAST, so they stay fast.

<!-- takeaways -->

- TOAST compresses and moves large values out of line.
- Queries not reading those columns skip TOAST.
- Tablespaces place objects on chosen storage.

### Data types and DDL

<!-- unit: Choosing data types -->

<!-- goals -->

- Choose numeric, text, date and time types correctly.
- Decide between timestamp and timestamptz, and generate UUIDs.

<!-- concept -->

Types are rules: they decide what values are valid, how they compare and how much space they take. Exact decimals for money, integers for counts and keys, text without arbitrary limits. Time is the classic trap: `timestamptz` records an instant, while `timestamp` records a wall-clock reading with no zone, which becomes ambiguous as soon as systems span time zones.

UUIDs are useful when keys must be generated outside the database.

<!-- example -->

```sql
CREATE TABLE payment (
  payment_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  amount numeric(12,2) NOT NULL,          -- exact money
  currency char(3) NOT NULL,
  paid_at timestamptz NOT NULL,           -- an instant
  is_refund boolean NOT NULL DEFAULT false,
  note text
);
```

#### Which numeric types does PostgreSQL offer, and when do you use each?

`smallint`, `integer`, `bigint` for whole numbers. `numeric(p, s)` for exact decimals such as money. `real` and `double precision` for approximate floating-point values. Avoid floats for currency.

#### What is the difference between `char(n)`, `varchar(n)` and `text`?

`char(n)` pads with spaces to a fixed length. `varchar(n)` limits the length. `text` has no limit. They perform the same in PostgreSQL, so `text` (with a `CHECK` constraint if you need a limit) is the common choice.

#### What are the date and time types?

`date`, `time`, `timestamp` (without time zone), `timestamptz` (with time zone) and `interval`. `timestamptz` stores an absolute instant in UTC and converts on display using the session `TimeZone`.

#### Should you use `timestamp` or `timestamptz`?

`timestamptz` for events that happened at a point in time. It avoids ambiguity across time zones and daylight-saving changes. `timestamp` only for local "wall clock" values not tied to a zone.

#### What is the `boolean` type?

`true`, `false` or `NULL`, with input accepted as `'t'`, `'yes'`, `'1'`, `'on'` and their opposites.

#### What is the `uuid` type, and how do you generate UUIDs?

A 128-bit identifier type. `gen_random_uuid()` is built in and generates version 4 UUIDs. PostgreSQL 18 adds `uuidv7()` for time-ordered UUIDs, which index better.

<!-- challenge -->

Totals of `double precision` amounts are off by a cent in finance reports. What type should they use, and why?

<!-- solution -->

`numeric(p, s)`, which stores exact decimals. Floating-point types approximate values in binary, so sums of many amounts accumulate rounding errors.

<!-- takeaways -->

- `numeric` for money; integers for keys and counts.
- `timestamptz` for instants.
- `text` is fine; limit length only when it's a rule.

<!-- unit: Rich types -->

<!-- goals -->

- Use arrays, ranges, enums and domains.
- Compute values with generated columns.

<!-- concept -->

PostgreSQL types go beyond the SQL basics. Arrays hold lists in a column; ranges represent intervals and can prevent overlaps; enums fix a set of values; domains attach constraints to a reusable type. Generated columns compute values from other columns automatically.

Each saves code elsewhere, but each also trades flexibility: enums are awkward to shrink, and arrays don't replace related tables when items need their own attributes.

<!-- example -->

```sql
CREATE DOMAIN email AS text CHECK (VALUE ~* '^[^@\s]+@[^@\s]+$');
CREATE TABLE booking (
  room_id int,
  during tstzrange NOT NULL,
  tags text[] DEFAULT '{}',
  guest_email email,
  nights int GENERATED ALWAYS AS (upper(during)::date - lower(during)::date) STORED,
  EXCLUDE USING gist (room_id WITH =, during WITH &&)   -- no double bookings (btree_gist)
);
```

#### What are arrays in PostgreSQL?

Any type can be an array: `text[]`, `integer[]`. Query them with `ANY`, `@>` (contains), `unnest()` to turn them into rows, and index them with GIN.

#### What are range types?

Types representing a range of values, such as `daterange`, `tstzrange`, `int4range`, with operators for overlap (`&&`) and containment (`@>`). They're useful for validity periods and bookings.

#### What is an enum type?

A type with a fixed, ordered list of values: `CREATE TYPE status AS ENUM ('active', 'closed')`. Adding values is easy, removing them is not, so lookup tables are often more flexible.

#### What is a domain?

A data type with constraints attached, reusable across tables: `CREATE DOMAIN postcode_fr AS text CHECK (VALUE ~ '^\d{5}$')`.

#### What is a generated column?

A column computed from other columns: `total numeric GENERATED ALWAYS AS (price * qty) STORED`. PostgreSQL computes it on write.

<!-- challenge -->

Product categories are stored as an enum, and the business renames and removes categories every quarter. Is an enum a good choice?

<!-- solution -->

No. Enum values are easy to add but awkward to rename order or remove. Use a lookup table with a foreign key, which supports changes, descriptions and history.

<!-- takeaways -->

- Arrays, ranges, enums and domains encode rules in types.
- Range exclusion constraints prevent overlaps.
- Use lookup tables for values that change.

<!-- unit: Constraints and keys -->

<!-- goals -->

- Use the main constraint types, including foreign keys.
- Choose ON DELETE behavior and index foreign keys.

<!-- concept -->

Constraints let the database refuse bad data instead of trusting every application to check. Keys and uniqueness prevent duplicates, checks enforce rules, exclusions prevent overlaps, and foreign keys guarantee references exist.

Foreign keys need two decisions: what happens to children when a parent is deleted, and an index on the referencing column, which PostgreSQL doesn't create for you. Without it, deletes on the parent scan the child table.

<!-- example -->

```sql
CREATE TABLE order_line (
  order_id bigint NOT NULL REFERENCES orders (order_id) ON DELETE CASCADE,
  line_no int NOT NULL,
  qty int NOT NULL CHECK (qty > 0),
  PRIMARY KEY (order_id, line_no)
);
CREATE INDEX ON order_line (order_id);   -- often covered by the PK; needed if it doesn't lead
```

#### What are the main constraint types?

`NOT NULL`, `UNIQUE`, `PRIMARY KEY`, `FOREIGN KEY`, `CHECK` and `EXCLUDE` (for example, no two overlapping bookings for the same room).

#### What is a foreign key, and what do `ON DELETE` options do?

A constraint requiring that values in a column exist in a referenced table's key. `ON DELETE CASCADE` deletes child rows with the parent, `SET NULL` clears the reference, `RESTRICT` or `NO ACTION` block the delete.

#### Are foreign key columns indexed automatically?

No. PostgreSQL indexes the referenced (parent) key but not the referencing column. Index foreign key columns that are used in joins or that are checked during deletes on the parent.

<!-- challenge -->

Deleting one customer takes 30 seconds. The `orders` table references customers with a foreign key. What is the likely cause?

<!-- solution -->

`orders.customer_id` isn't indexed, so each delete scans the whole orders table to check for references. Create an index on the foreign key column.

<!-- takeaways -->

- Constraints enforce rules in the database.
- Choose ON DELETE behavior deliberately.
- Index foreign key columns yourself.

<!-- unit: Changing tables safely -->

<!-- goals -->

- Add columns and constraints to large tables without long locks.
- Use temporary and unlogged tables appropriately.

<!-- concept -->

On a busy table, how you change the schema matters as much as what you change. Some changes are instant; others rewrite the table or scan it while holding a lock that blocks everyone. Adding a column with a constant default is now instant, and constraints can be added as not yet validated, then validated without blocking writes.

Temporary and unlogged tables trade durability for speed, which suits scratch and staging data.

<!-- example -->

```sql
ALTER TABLE orders ADD COLUMN channel text DEFAULT 'web';          -- instant
ALTER TABLE orders ADD CONSTRAINT orders_amount_pos CHECK (amount >= 0) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT orders_amount_pos;          -- scans without blocking writes
CREATE UNLOGGED TABLE staging_orders (LIKE orders);                -- fast, not crash-safe
```

#### How do you add a column to a large table safely?

`ALTER TABLE t ADD COLUMN c type` is instant, even with a constant default (since PostgreSQL 11). Volatile defaults, type changes that rewrite the table, and adding `NOT NULL` with a validation scan need more care and planning.

#### How do you add a constraint without locking the table for long?

Add it as `NOT VALID` (enforced for new rows only), then run `ALTER TABLE ... VALIDATE CONSTRAINT`, which takes a weaker lock while it checks existing rows.

#### What is a temporary table?

A table visible only to the current session and dropped at its end (or at commit with `ON COMMIT DROP`). It is useful for intermediate results.

#### What is an unlogged table?

A table whose changes aren't written to the WAL. Writes are much faster, but the table is emptied after a crash and isn't replicated. It is useful for staging data that can be reloaded.

<!-- challenge -->

A migration adds a foreign key to a 500-million-row table and blocks writes for 20 minutes. How should it be written?

<!-- solution -->

Add the foreign key with `NOT VALID` (fast, enforced for new rows), then run `VALIDATE CONSTRAINT` separately, which checks existing rows with a weaker lock that doesn't block writes.

<!-- takeaways -->

- Some DDL is instant; some rewrites or blocks.
- Use `NOT VALID` then `VALIDATE` for constraints.
- Unlogged tables are fast but not crash-safe.

<!-- unit: Working with NULL -->

<!-- goals -->

- Explain how NULL behaves in comparisons.
- Use COALESCE and NULLIF.

<!-- concept -->

`NULL` means unknown, and unknown spreads: comparing anything with `NULL` gives unknown, which filters treat as false. That's why `= NULL` never matches and why rows quietly disappear from `WHERE` clauses that forget them.

Two functions handle most cases: one replaces missing values with defaults, the other turns a specific value into `NULL`, which avoids errors like division by zero.

<!-- example -->

```sql
SELECT count(*) FROM customer WHERE phone = NULL;     -- always 0
SELECT count(*) FROM customer WHERE phone IS NULL;    -- correct
SELECT COALESCE(nickname, first_name, 'unknown') AS display_name FROM customer;
SELECT revenue / NULLIF(orders, 0) AS avg_order FROM daily_stats;
```

#### What does `NULL` mean, and how does it behave in comparisons?

An unknown or missing value. Any comparison with `NULL` returns `NULL` (not true), so use `IS NULL` / `IS NOT NULL`, and `IS DISTINCT FROM` for null-safe comparisons.

#### What does `COALESCE` do?

It returns the first non-null argument: `COALESCE(nickname, first_name, 'unknown')`.

#### What is `NULLIF`?

`NULLIF(a, b)` returns `NULL` if `a = b`, otherwise `a`. It's handy to avoid division by zero: `x / NULLIF(y, 0)`.

<!-- challenge -->

`WHERE status <> 'cancelled'` returns fewer rows than expected. Some rows have `status` NULL. How do you include them?

<!-- solution -->

`WHERE status IS DISTINCT FROM 'cancelled'` (or `status <> 'cancelled' OR status IS NULL`), since `NULL <> 'cancelled'` is unknown and filtered out.

<!-- takeaways -->

- Comparisons with NULL are unknown.
- Use `IS NULL` and `IS DISTINCT FROM`.
- `COALESCE` defaults; `NULLIF` avoids division by zero.

<!-- stage: Querying -->

### Querying: joins, subqueries and CTEs

<!-- unit: Joins -->

<!-- goals -->

- Choose the right join type and place conditions correctly.
- Write semi-joins, anti-joins and LATERAL joins.

<!-- concept -->

Joins combine tables, and small details change results. In a left join, a condition in `ON` decides which right rows match while keeping every left row; the same condition in `WHERE` filters rows afterwards and silently turns the join into an inner join.

"Has a match" and "has no match" questions are semi- and anti-joins, best written with `EXISTS` and `NOT EXISTS`. LATERAL lets a subquery use columns from earlier tables, such as fetching the latest three orders per customer.

<!-- example -->

```sql
-- customers with no orders in 2026 (anti-join)
SELECT c.*
FROM customer c
WHERE NOT EXISTS (
  SELECT 1 FROM orders o
  WHERE o.customer_id = c.customer_id AND o.ordered_at >= '2026-01-01'
);
```

#### What are the different join types?

`INNER JOIN` (matching rows only), `LEFT JOIN` (all left rows plus matches), `RIGHT JOIN`, `FULL OUTER JOIN` (all rows from both sides) and `CROSS JOIN` (every combination). There are also self-joins and `LATERAL` joins.

#### What is the difference between `WHERE` and `ON` in a left join?

A condition in `ON` decides which right-side rows match, and left rows are kept regardless. The same condition in `WHERE` filters the joined result, which can remove left rows and effectively turn the left join into an inner join.

#### What is a semi-join and an anti-join?

A semi-join returns rows of A that have a match in B (`WHERE EXISTS (...)`) without duplicating A. An anti-join returns rows of A with no match in B (`WHERE NOT EXISTS (...)` or a left join with `IS NULL`).

#### Why prefer `NOT EXISTS` over `NOT IN` with a subquery?

If the subquery returns any `NULL`, `NOT IN` returns no rows at all, because the comparison with `NULL` is unknown. `NOT EXISTS` behaves as expected and plans well as an anti-join.

#### What is a `LATERAL` join?

A join where the right-hand subquery can reference columns of tables to its left. It is used for "top-N per group":

```sql
SELECT c.name, o.*
FROM customer c
CROSS JOIN LATERAL (
    SELECT * FROM orders o WHERE o.customer_id = c.id ORDER BY created_at DESC LIMIT 3
) o;
```

<!-- challenge -->

`SELECT * FROM customer WHERE customer_id NOT IN (SELECT customer_id FROM orders)` returns no rows, though some customers have no orders. Why?

<!-- solution -->

`orders.customer_id` contains a `NULL`, so `NOT IN` compares against unknown and returns nothing. Use `NOT EXISTS`, which isn't affected by NULLs.

<!-- takeaways -->

- `ON` conditions match; `WHERE` conditions filter.
- Use `EXISTS` / `NOT EXISTS` for semi- and anti-joins.
- LATERAL subqueries can use earlier tables' columns.

<!-- unit: Subqueries, CTEs and set operations -->

<!-- goals -->

- Structure queries with CTEs, including recursive ones.
- Use correlated subqueries and set operations correctly.

<!-- concept -->

Complex questions are easier to read in steps. CTEs name each step; recursive CTEs walk hierarchies like org charts or generate sequences. Correlated subqueries refer to the outer row and are often rewritten by the planner as joins.

Set operations combine results vertically: union removes duplicates at a cost, union all just appends, and intersect and except compare two result sets, which is handy for checking differences.

<!-- example -->

```sql
WITH RECURSIVE chain AS (
  SELECT employee_id, manager_id, name, 1 AS depth FROM employee WHERE employee_id = 42
  UNION ALL
  SELECT e.employee_id, e.manager_id, e.name, c.depth + 1
  FROM employee e JOIN chain c ON e.employee_id = c.manager_id
)
SELECT * FROM chain;            -- employee 42 and every manager above
```

#### What is a CTE?

A Common Table Expression, introduced with `WITH`, names a subquery for readability and reuse within one statement. Since PostgreSQL 12, non-recursive CTEs are inlined when possible. `MATERIALIZED` and `NOT MATERIALIZED` override that choice.

#### What is a recursive CTE?

A CTE that references itself to walk hierarchies or generate series:

```sql
WITH RECURSIVE tree AS (
    SELECT id, parent_id, name, 1 AS depth FROM category WHERE parent_id IS NULL
    UNION ALL
    SELECT c.id, c.parent_id, c.name, t.depth + 1
    FROM category c JOIN tree t ON c.parent_id = t.id
)
SELECT * FROM tree;
```

#### What is a correlated subquery?

A subquery that references columns of the outer query, so it is logically evaluated per outer row. The planner can often turn it into a join.

#### What is the difference between `UNION` and `UNION ALL`?

`UNION` removes duplicates, which requires a sort or hash. `UNION ALL` keeps all rows and is faster. Use `UNION ALL` unless you need deduplication.

#### What do `INTERSECT` and `EXCEPT` do?

`INTERSECT` returns rows present in both queries, `EXCEPT` rows in the first but not the second, both without duplicates unless `ALL` is used.

<!-- challenge -->

How do you check whether a rewritten query returns exactly the same rows as the old one?

<!-- solution -->

Run `(old EXCEPT new)` and `(new EXCEPT old)`; both must be empty. For duplicates, compare with `EXCEPT ALL` or counts per row.

<!-- takeaways -->

- CTEs make steps readable; recursive CTEs walk hierarchies.
- `UNION ALL` unless you need deduplication.
- `EXCEPT` both ways compares result sets.

<!-- unit: How a SELECT runs -->

<!-- goals -->

- Explain the logical order of a SELECT.
- Use HAVING, DISTINCT ON, keyset pagination and generate_series.

<!-- concept -->

SQL is written top to bottom but evaluated in another order: rows are gathered and filtered, grouped, filtered again, windowed, projected, deduplicated, ordered and limited. That order explains why aliases can't be used in `WHERE` and why window functions can't be filtered without a subquery.

Some PostgreSQL features build on it: `DISTINCT ON` keeps one row per group by ordering, keyset pagination avoids reading skipped rows, and `generate_series` fills in missing dates.

<!-- example -->

```sql
-- latest order per customer
SELECT DISTINCT ON (customer_id) customer_id, order_id, ordered_at
FROM orders
ORDER BY customer_id, ordered_at DESC;

-- next page after the last seen row (keyset)
SELECT * FROM orders WHERE (ordered_at, order_id) < ('2026-10-17 09:00', 98123)
ORDER BY ordered_at DESC, order_id DESC LIMIT 50;
```

#### What is the logical order of execution of a SELECT?

`FROM` and joins, `WHERE`, `GROUP BY`, `HAVING`, window functions, `SELECT`, `DISTINCT`, `ORDER BY`, `LIMIT`/`OFFSET`. This is why aliases defined in `SELECT` can't be used in `WHERE`.

#### What is the difference between `WHERE` and `HAVING`?

`WHERE` filters rows before grouping. `HAVING` filters groups after aggregation, so it can use aggregate results such as `HAVING count(*) > 10`.

#### What does `DISTINCT ON` do?

A PostgreSQL extension that keeps the first row of each group, according to `ORDER BY`:

```sql
SELECT DISTINCT ON (customer_id) customer_id, order_id, created_at
FROM orders
ORDER BY customer_id, created_at DESC;   -- latest order per customer
```

#### How do you paginate efficiently?

`OFFSET` gets slower as the offset grows, because skipped rows are still read. Keyset pagination is faster: `WHERE (created_at, id) < ($1, $2) ORDER BY created_at DESC, id DESC LIMIT 50`, with an index on those columns.

#### What is `generate_series`?

A set-returning function that produces a series of numbers or timestamps, used to build calendars and fill gaps: `SELECT generate_series('2026-01-01'::date, '2026-12-31', interval '1 day')`.

<!-- challenge -->

An API pages through orders with `OFFSET 200000 LIMIT 50` and the deep pages time out. What do you change?

<!-- solution -->

Switch to keyset pagination: remember the last row's sort key (for example `ordered_at, order_id`) and filter `WHERE (ordered_at, order_id) < (...)` with a matching index, so each page reads only 50 rows.

<!-- takeaways -->

- Evaluation order: FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY.
- `DISTINCT ON` keeps one row per group.
- Keyset pagination stays fast on deep pages.

<!-- unit: Writing data -->

<!-- goals -->

- Upsert with ON CONFLICT and MERGE, and return affected rows.
- Find and remove duplicate rows.

<!-- concept -->

Writes often depend on what already exists. `INSERT ... ON CONFLICT` inserts or updates in one atomic statement, using a unique constraint to detect conflicts. `MERGE` handles richer cases, including deletes, from a source of changes. `RETURNING` hands back the affected rows, saving another query.

Duplicates are the opposite problem: find them by grouping on the intended key, then delete all but one per group, and add the unique constraint that should have prevented them.

<!-- example -->

```sql
INSERT INTO company (country_code, business_id, name)
VALUES ('FR', '123456789', 'Acme')
ON CONFLICT (country_code, business_id)
DO UPDATE SET name = EXCLUDED.name
RETURNING company_id, (xmax = 0) AS inserted;
```

#### What is an upsert in PostgreSQL?

`INSERT ... ON CONFLICT` inserts a row or, if it violates a unique constraint, updates it (or does nothing):

```sql
INSERT INTO company (country_code, business_id, name)
VALUES ('FR', '732829320', 'ACME')
ON CONFLICT (country_code, business_id) DO UPDATE SET name = EXCLUDED.name;
```

#### What is the `MERGE` statement?

A standard SQL statement (PostgreSQL 15+) that inserts, updates or deletes rows of a target based on a join with a source, in one statement. PostgreSQL 17 adds `RETURNING` and `WHEN NOT MATCHED BY SOURCE`.

#### What does `RETURNING` do?

It returns columns of the rows affected by `INSERT`, `UPDATE` or `DELETE`, avoiding a second query: `INSERT ... RETURNING id`.

#### How do you find duplicate rows?

```sql
SELECT country_code, business_id, count(*)
FROM company
GROUP BY country_code, business_id
HAVING count(*) > 1;
```

#### How do you delete duplicates and keep one row per key?

```sql
DELETE FROM company c
USING (
    SELECT ctid, row_number() OVER (PARTITION BY country_code, business_id ORDER BY company_id) AS rn
    FROM company
) d
WHERE c.ctid = d.ctid AND d.rn > 1;
```

<!-- challenge -->

An upsert with `ON CONFLICT (email)` fails with "there is no unique or exclusion constraint matching". What is missing?

<!-- solution -->

A unique constraint or unique index on `email`. `ON CONFLICT` needs one to detect conflicts; create it (after removing existing duplicates).

<!-- takeaways -->

- `ON CONFLICT` upserts atomically on a unique key.
- `MERGE` applies inserts, updates and deletes from a source.
- Remove duplicates, then add the missing constraint.

### Aggregation and window functions

<!-- unit: Aggregates -->

<!-- goals -->

- Use common aggregates and the FILTER clause.
- Produce multi-level totals and pivots.

<!-- concept -->

Aggregation collapses rows into summaries, and a few details decide whether the summary is right. Counting rows, non-null values and distinct values gives three different numbers. Filters inside an aggregate compute several conditional totals in one pass.

Grouping sets produce subtotals and grand totals in one query, and conditional aggregation pivots rows into columns, the usual way to build report-shaped results in SQL.

<!-- example -->

```sql
SELECT country_code,
       count(*)                                  AS orders,
       count(DISTINCT customer_id)               AS customers,
       sum(amount) FILTER (WHERE status = 'paid') AS paid_amount,
       string_agg(DISTINCT channel, ', ' ORDER BY channel) AS channels
FROM orders
GROUP BY ROLLUP (country_code);
```

#### What are the most used aggregate functions?

`count`, `sum`, `avg`, `min`, `max`, `string_agg`, `array_agg`, `bool_and`, `bool_or`, `json_agg`, and statistical ones such as `stddev` and `percentile_cont`.

#### What is the difference between `count(*)`, `count(col)` and `count(DISTINCT col)`?

`count(*)` counts rows. `count(col)` counts non-null values of `col`. `count(DISTINCT col)` counts distinct non-null values.

#### What does the `FILTER` clause do?

It restricts the rows an aggregate sees, a cleaner alternative to `CASE` inside aggregates:

```sql
SELECT country_code,
       count(*) AS total,
       count(*) FILTER (WHERE status = 'ACTIVE') AS active
FROM company GROUP BY country_code;
```

#### What are `GROUPING SETS`, `ROLLUP` and `CUBE`?

Ways to compute several groupings in one query. `ROLLUP (country, city)` produces per city, per country and grand totals. `CUBE` produces all combinations. `GROUPING SETS` lists exactly the groupings you want.

#### What does `string_agg` do?

It concatenates values with a separator, optionally ordered: `string_agg(name, ', ' ORDER BY name)`.

#### How do you pivot rows into columns?

With conditional aggregation:

```sql
SELECT country_code,
       sum(amount) FILTER (WHERE year = 2025) AS y2025,
       sum(amount) FILTER (WHERE year = 2026) AS y2026
FROM revenue GROUP BY country_code;
```

The `tablefunc` extension's `crosstab` is an alternative.

<!-- challenge -->

A report needs revenue per country for 2024, 2025 and 2026 as three columns. Write the core of it.

<!-- solution -->

`SELECT country_code, sum(amount) FILTER (WHERE extract(year FROM ordered_at) = 2024) AS y2024, ... 2025 ..., ... 2026 ... FROM orders GROUP BY country_code`.

<!-- takeaways -->

- `count(*)`, `count(col)` and `count(DISTINCT col)` differ.
- `FILTER` gives conditional aggregates.
- `ROLLUP` adds subtotals; `FILTER` pivots.

<!-- unit: Window function basics -->

<!-- goals -->

- Explain window functions and ranking functions.
- Get top N per group and compare with previous rows.

<!-- concept -->

Window functions compute over related rows while keeping every row in the result. The window is defined by a partition (which rows belong together) and an order (their sequence). With that, ranking within groups, comparing with the previous row or numbering rows becomes a single expression.

Because windows are computed after `WHERE`, filtering on their results needs an outer query. Named windows avoid repeating long definitions.

<!-- example -->

```sql
SELECT * FROM (
  SELECT product_id, category, revenue,
         rank() OVER w AS rnk,
         revenue - lag(revenue) OVER w AS diff_to_previous
  FROM product_revenue
  WINDOW w AS (PARTITION BY category ORDER BY revenue DESC)
) t
WHERE rnk <= 3;
```

#### What is a window function?

A function computed over a set of rows related to the current row (its window), without collapsing rows like `GROUP BY`:

```sql
SELECT country_code, name, revenue,
       rank() OVER (PARTITION BY country_code ORDER BY revenue DESC) AS rank_in_country
FROM company;
```

#### What is the difference between `row_number`, `rank` and `dense_rank`?

For ties: `row_number` gives unique numbers (1, 2, 3), `rank` gives the same rank and then skips (1, 1, 3), `dense_rank` gives the same rank without gaps (1, 1, 2).

#### How do you get the top N rows per group?

Number rows per group and filter in an outer query (window functions can't be used in `WHERE`):

```sql
SELECT * FROM (
    SELECT *, row_number() OVER (PARTITION BY country_code ORDER BY employees DESC) AS rn
    FROM company
) t WHERE rn <= 3;
```

#### What do `lag` and `lead` do?

They return a value from a previous or following row in the window, for example to compute the change since the previous month: `revenue - lag(revenue) OVER (ORDER BY month)`.

#### What is the `WINDOW` clause?

A way to name a window definition and reuse it in several functions: `... OVER w ... WINDOW w AS (PARTITION BY country ORDER BY day)`.

<!-- challenge -->

Someone writes `WHERE row_number() OVER (...) = 1` and gets an error. How do you fix it?

<!-- solution -->

Window functions run after `WHERE`, so compute the row number in a subquery or CTE and filter in the outer query (or use `DISTINCT ON` for the first row per group).

<!-- takeaways -->

- Windows compute over partitions without collapsing rows.
- Ranking functions differ in how they treat ties.
- Filter window results in an outer query.

<!-- unit: Frames and running calculations -->

<!-- goals -->

- Define window frames with ROWS and RANGE.
- Compute running totals, moving averages and period growth.

<!-- concept -->

Ordered windows have a frame: the rows around the current one that the function sees. The default frame runs from the start to the current row, which is what makes running totals work but also why `last_value` surprises people.

Choosing between counting rows and covering a value range matters with gaps or ties: a seven-row frame and a seven-day frame differ whenever days are missing.

<!-- example -->

```sql
SELECT day, amount,
       sum(amount) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
       avg(amount) OVER (ORDER BY day RANGE BETWEEN interval '6 days' PRECEDING AND CURRENT ROW) AS avg_7d
FROM daily_sales;
```

#### How do you compute a running total?

```sql
SELECT day, amount,
       sum(amount) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM sales;
```

#### What is a window frame, and what is the difference between `ROWS` and `RANGE`?

The subset of the partition used for each row's calculation. `ROWS` counts physical rows (for example the three preceding rows). `RANGE` uses value distances in the `ORDER BY` column, so peers with equal values are included together. The default frame with `ORDER BY` is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`.

#### How do you compute a 7-day moving average?

```sql
SELECT day,
       avg(amount) OVER (ORDER BY day RANGE BETWEEN interval '6 days' PRECEDING AND CURRENT ROW) AS avg_7d
FROM daily_sales;
```

#### What do `first_value`, `last_value` and `nth_value` do?

They return the first, last or nth value in the frame. `last_value` often surprises because the default frame ends at the current row: specify `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.

#### How do you compute year-over-year growth?

```sql
SELECT year, revenue,
       round(100.0 * (revenue - lag(revenue) OVER (ORDER BY year)) / lag(revenue) OVER (ORDER BY year), 1) AS yoy_pct
FROM yearly_revenue;
```

<!-- challenge -->

`last_value(price) OVER (PARTITION BY product ORDER BY changed_at)` returns each row's own price instead of the latest. Why, and the fix?

<!-- solution -->

The default frame ends at the current row, so the "last" value is the current one. Use `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`, or `first_value` with descending order.

<!-- takeaways -->

- Frames define which rows a window function sees.
- `ROWS` counts rows; `RANGE` covers value ranges.
- The default frame ends at the current row.

<!-- unit: Distributions and sequences -->

<!-- goals -->

- Compute percentiles, buckets and shares of total.
- Solve gaps-and-islands problems.

<!-- concept -->

Averages hide distributions. Medians and percentiles describe skewed data honestly, buckets split rows into quartiles or deciles, and a window over the whole result turns counts into shares of the total.

Sequences of events raise another classic: finding consecutive runs, such as days a user was active in a row. Subtracting a row number from the date gives every run a constant key, the core of the gaps-and-islands technique.

<!-- example -->

```sql
WITH d AS (
  SELECT user_id, day, day - (row_number() OVER (PARTITION BY user_id ORDER BY day))::int AS grp
  FROM (SELECT DISTINCT user_id, day FROM activity) a
)
SELECT user_id, min(day) AS start_day, max(day) AS end_day, count(*) AS streak
FROM d GROUP BY user_id, grp
ORDER BY streak DESC;
```

#### What do `ntile` and `percent_rank` do?

`ntile(4)` splits ordered rows into 4 buckets (quartiles). `percent_rank()` gives each row's relative rank between 0 and 1.

#### How do you compute a percentage of total with a window function?

```sql
SELECT country_code, count(*) AS n,
       round(100.0 * count(*) / sum(count(*)) OVER (), 1) AS pct
FROM company GROUP BY country_code;
```

#### How do you calculate a median in PostgreSQL?

With the ordered-set aggregate `percentile_cont(0.5) WITHIN GROUP (ORDER BY value)`. `percentile_disc` returns an actual value from the set.

#### What is the "gaps and islands" problem, and how do you solve it?

Finding consecutive runs (islands) in a sequence. A classic method subtracts a `row_number()` from the ordered value: rows of the same island share the difference, which you then group by.

```sql
SELECT user_id, min(day) AS start_day, max(day) AS end_day
FROM (
    SELECT user_id, day, day - (row_number() OVER (PARTITION BY user_id ORDER BY day))::int AS grp
    FROM logins
) t
GROUP BY user_id, grp;
```

<!-- challenge -->

The average order value is 120, but most orders are around 40. How do you describe typical orders better in one query?

<!-- solution -->

Use `percentile_cont(0.5) WITHIN GROUP (ORDER BY amount)` for the median, plus p90 and p99, which reveal that a few large orders inflate the mean.

<!-- takeaways -->

- Medians and percentiles describe skewed data.
- `sum(...) OVER ()` gives shares of total.
- Gaps and islands: date minus row number groups runs.

<!-- stage: Performance -->

### Indexes

<!-- unit: Index types -->

<!-- goals -->

- Choose among B-tree, hash, GIN, GiST, BRIN and unique indexes.
- Explain how B-trees work and what CLUSTER does.

<!-- concept -->

An index is a separate structure that lets PostgreSQL find rows without reading the whole table. Each type suits a kind of question: B-trees for equality, ranges and sorting; GIN for "contains" questions on arrays, JSON and text; GiST for geometric and range data; BRIN for huge tables whose values follow physical order.

Unique indexes also enforce rules. PostgreSQL never keeps tables physically sorted; `CLUSTER` reorders once, and the order decays.

<!-- example -->

| Query | Index |
|---|---|
| `WHERE email = ?`, `ORDER BY created_at` | B-tree |
| `WHERE tags @> '{sale}'`, JSONB `@>` | GIN |
| `WHERE during && tstzrange(...)` | GiST |
| `WHERE logged_at > now() - interval '1 day'` on 5 TB append-only | BRIN |

#### What are the different types of indexes available in PostgreSQL and when to use each one?

- **B-tree** (default): equality and range searches (`=`, `<`, `>`, `BETWEEN`, `ORDER BY`, prefix `LIKE 'abc%'`) on sortable data.
- **Hash:** equality only. Rarely better than B-tree, but small for long values.
- **GIN** (generalized inverted index): values that contain several components, such as arrays, JSONB and full-text search vectors, for "contains" queries.
- **GiST** (generalized search tree): geometric data, ranges, full-text search and nearest-neighbor searches (with PostGIS, for example).
- **SP-GiST:** space-partitioned data such as quadtrees, IP addresses or phone numbers.
- **BRIN** (block range index): very large tables whose values follow the physical order, such as an append-only timestamp column. Tiny and cheap to maintain.

#### How does a B-tree index work?

It's a balanced tree of sorted keys with pointers to table rows. Lookups take a few page reads (logarithmic time), and sorted order makes range scans and `ORDER BY` efficient.

#### What is a unique index, and how does it relate to a unique constraint?

An index that rejects duplicate keys. A `UNIQUE` constraint is implemented with a unique index. By default, several `NULL`s are allowed, unless the index is declared `NULLS NOT DISTINCT` (PostgreSQL 15+).

#### When is a BRIN index the right choice?

For very large tables where a column correlates with physical order, such as a timestamp in an append-only log. A BRIN index stores min/max values per block range, so it is tiny and lets queries skip most blocks.

#### What is the difference between a clustered index in other databases and `CLUSTER` in PostgreSQL?

PostgreSQL has no permanently clustered tables. `CLUSTER` physically reorders a table once according to an index, but new rows aren't kept in order, so it must be repeated.

<!-- challenge -->

A 3 TB append-only log table is queried by time range. A B-tree on `logged_at` is 90 GB. What alternative do you consider?

<!-- solution -->

A BRIN index on `logged_at`: since rows are appended in time order, BRIN stores min/max per block range and stays a few MB while pruning most of the table.

<!-- takeaways -->

- Pick index types by query shape.
- B-trees are the default; GIN and GiST for complex types.
- BRIN is tiny for naturally ordered huge tables.

<!-- unit: Designing indexes -->

<!-- goals -->

- Design composite, partial, expression and covering indexes.
- Get index-only scans and avoid redundant indexes.

<!-- concept -->

Good indexes match how queries filter and sort. In a composite index, columns are used left to right, so equality columns come first and range columns last; a composite index usually makes an index on its first column redundant.

Indexes can be narrower or richer than a column: partial indexes cover only the rows queries ask about, expression indexes cover computed values, and included columns let the index answer a query alone, if the visibility map allows it.

<!-- example -->

```sql
CREATE INDEX ON orders (customer_id, ordered_at);                     -- composite
CREATE INDEX ON orders (ordered_at) WHERE status = 'pending';         -- partial
CREATE INDEX ON customer (lower(email));                              -- expression
CREATE INDEX ON orders (customer_id) INCLUDE (amount);                -- covering
```

#### What is a composite (multi-column) index, and does column order matter?

An index on several columns. Order matters: an index on `(country_code, created_on)` serves filters on `country_code` alone, or on both, but not efficiently on `created_on` alone. Put the equality columns first, then the range or sort column.

#### Does an index on `(a, b)` make an index on `(a)` redundant?

Mostly yes: the composite index serves queries on `a` alone. A separate index on `a` may still be smaller and slightly faster, but usually isn't worth its maintenance cost.

#### What is a partial index?

An index over a subset of rows, defined with a `WHERE` clause. It is smaller and faster when queries target that subset:

```sql
CREATE INDEX ON company (country_code) WHERE status = 'ACTIVE';
```

#### What is an expression index?

An index on the result of an expression, used when queries filter on the same expression:

```sql
CREATE INDEX ON customer (lower(email));
SELECT * FROM customer WHERE lower(email) = 'a@b.com';
```

#### What is a covering index, and what does `INCLUDE` do?

An index containing all the columns a query needs, so it can answer with an index-only scan without reading the table. `INCLUDE (col)` adds non-key columns to the index for that purpose.

#### What is an index-only scan, and what does it need?

A scan that answers a query from the index alone. It needs a covering index and pages marked all-visible in the visibility map, which vacuum maintains.

<!-- challenge -->

Queries filter `WHERE status = 'pending' AND ordered_at > now() - interval '1 day'`; 99% of orders aren't pending. Which index fits best?

<!-- solution -->

A partial index `ON orders (ordered_at) WHERE status = 'pending'`: it contains only pending rows, so it's small and matches the query exactly.

<!-- takeaways -->

- Composite order: equality first, ranges last.
- Partial and expression indexes match specific queries.
- Covering indexes enable index-only scans.

<!-- unit: Indexes for special data -->

<!-- goals -->

- Index JSONB documents and substring searches.
- Understand GIN pending lists.

<!-- concept -->

Some queries can't use ordinary B-trees. Searching inside JSON documents, testing containment or matching text anywhere in a string needs inverted indexes. GIN indexes every key or trigram so those lookups become index scans.

GIN is expensive to update, so it buffers new entries in a pending list and merges them later. That speeds writes but can make reads uneven until the merge happens.

<!-- example -->

```sql
CREATE INDEX ON events USING gin (payload jsonb_path_ops);    -- payload @> '{"type":"click"}'
CREATE INDEX ON events ((payload->>'user_id'));               -- equality on one key
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX ON company USING gin (name gin_trgm_ops);        -- name ILIKE '%acme%'
```

#### How do you index a JSONB column?

A GIN index on the whole column for containment and key-existence queries (`@>`, `?`), with `jsonb_path_ops` for a smaller index that only supports `@>`, or a B-tree expression index on one extracted key:

```sql
CREATE INDEX ON events USING gin (payload jsonb_path_ops);
CREATE INDEX ON events ((payload->>'user_id'));
```

#### How do you speed up `LIKE '%text%'` searches?

With a trigram index from the `pg_trgm` extension: `CREATE INDEX ON company USING gin (name gin_trgm_ops)`. It also speeds up similarity searches.

#### What are GIN index `fastupdate` and pending lists?

GIN indexes buffer new entries in a pending list for faster inserts, merged into the main index later by vacuum or when the list is full. Large pending lists can slow searches.

<!-- challenge -->

Searches with `name ILIKE '%dupont%'` on 20 million companies take 8 seconds. What do you add?

<!-- solution -->

A trigram GIN index (`pg_trgm`, `gin_trgm_ops`) on `name`, which supports `LIKE`/`ILIKE` with leading wildcards.

<!-- takeaways -->

- GIN indexes keys and trigrams for containment and substrings.
- Expression indexes cover single JSON keys.
- GIN buffers writes in a pending list.

<!-- unit: Index costs and maintenance -->

<!-- goals -->

- Weigh index costs and understand why indexes are ignored.
- Create, rebuild, find and measure indexes safely.

<!-- concept -->

Indexes aren't free: each one slows every write and takes space, and unused indexes are pure cost. The planner also ignores indexes when a scan is cheaper, when statistics mislead it, or when the query wraps the column in a function.

Maintenance follows from that: build indexes without blocking writes, rebuild bloated ones the same way, look for missing indexes in scan statistics and slow queries, and drop indexes that nobody uses.

<!-- example -->

```sql
CREATE INDEX CONCURRENTLY orders_customer_idx ON orders (customer_id);
REINDEX INDEX CONCURRENTLY orders_customer_idx;
SELECT relname, seq_scan, seq_tup_read, idx_scan FROM pg_stat_user_tables ORDER BY seq_tup_read DESC LIMIT 10;
SELECT pg_size_pretty(pg_indexes_size('orders'));
```

#### What are the costs of indexes?

They take disk space and slow down `INSERT`, `UPDATE` and `DELETE`, because each index must be maintained. Unused indexes are pure cost: find them with `pg_stat_user_indexes` (`idx_scan = 0`).

#### Why might PostgreSQL not use an index?

The query returns a large share of the table (a sequential scan is cheaper), statistics are outdated, a function or type cast is applied to the indexed column, the filter starts with a wildcard (`LIKE '%abc'`), the column order doesn't match a composite index, or the table is small.

#### How do you create an index without blocking writes?

`CREATE INDEX CONCURRENTLY`, which builds the index without holding a lock that blocks inserts and updates. It takes longer and can't run inside a transaction block. If it fails, it leaves an invalid index to drop.

#### What is index bloat, and how do you fix it?

Indexes accumulate empty space after many updates and deletes. `REINDEX CONCURRENTLY` rebuilds them online. B-tree deduplication (PostgreSQL 13+) reduces bloat from duplicates.

#### How do you find missing indexes?

Look for large sequential scans in `pg_stat_user_tables` (`seq_scan`, `seq_tup_read`), slow queries in `pg_stat_statements`, and sequential scans with selective filters in `EXPLAIN` plans.

#### How do you see the size of a table and its indexes?

```sql
SELECT pg_size_pretty(pg_total_relation_size('company')) AS total,
       pg_size_pretty(pg_relation_size('company'))       AS table_only,
       pg_size_pretty(pg_indexes_size('company'))        AS indexes;
```

<!-- challenge -->

A table has 14 indexes, and inserts got slow. How do you decide which to drop?

<!-- solution -->

Check `pg_stat_user_indexes.idx_scan` over a representative period (excluding unique and constraint indexes), find duplicates and prefixes of composite indexes, and drop unused ones, keeping a note to recreate if needed.

<!-- takeaways -->

- Every index slows writes and takes space.
- Build and rebuild indexes concurrently.
- Find missing and unused indexes from statistics.

### Transactions, MVCC and concurrency

<!-- unit: Transactions and MVCC -->

<!-- goals -->

- Explain transactions, MVCC and dead tuples.
- Use savepoints, HOT updates and asynchronous commit appropriately.

<!-- concept -->

PostgreSQL lets readers and writers work at the same time by keeping several versions of rows. An update writes a new version; transactions see the version that matches their snapshot. Nobody waits for readers, but old versions pile up as dead tuples until vacuum removes them.

Some optimizations reduce that cost: updates that don't touch indexed columns can stay on the same page without index changes. Savepoints allow partial rollback, and relaxing commit durability trades a small loss window for speed.

<!-- example -->

```sql
BEGIN;
UPDATE account SET balance = balance - 100 WHERE account_id = 1;
SAVEPOINT before_fee;
UPDATE account SET balance = balance - 2 WHERE account_id = 1;
ROLLBACK TO before_fee;         -- undo only the fee
COMMIT;
```

#### What is a transaction in PostgreSQL?

A group of statements between `BEGIN` and `COMMIT` (or `ROLLBACK`) executed atomically. Each statement outside an explicit transaction runs in its own transaction (autocommit).

#### What is MVCC?

Multi-Version Concurrency Control: an `UPDATE` writes a new version of the row instead of overwriting it, and each transaction sees a snapshot of committed data. Readers don't block writers and writers don't block readers.

#### What are dead tuples?

Old row versions left by updates and deletes that no transaction can see any more. They take space until `VACUUM` reclaims it.

#### What is HOT (heap-only tuple) update?

An optimization where an update that doesn't change indexed columns, and fits on the same page, creates the new version without updating indexes. A lower `fillfactor` leaves room for HOT updates on update-heavy tables.

#### What is a savepoint?

A point within a transaction you can roll back to without aborting the whole transaction: `SAVEPOINT s1; ... ROLLBACK TO SAVEPOINT s1;`.

#### What is the difference between `COMMIT` and `synchronous_commit = off`?

By default `COMMIT` waits until the WAL is flushed to disk, guaranteeing durability. With `synchronous_commit = off`, commits return sooner and a crash can lose the last few transactions, without corrupting data.

<!-- challenge -->

A table updated constantly keeps growing, and indexes grow too, though rows don't change in number. Which MVCC detail can you use to reduce index growth?

<!-- solution -->

Enable HOT updates: avoid indexing frequently updated columns and set a lower `fillfactor` so new versions fit on the same page, letting updates skip index changes.

<!-- takeaways -->

- MVCC keeps versions so readers don't block writers.
- Dead tuples need vacuum.
- HOT updates avoid index changes.

<!-- unit: Isolation and anomalies -->

<!-- goals -->

- Compare PostgreSQL's isolation levels and the anomalies they prevent.
- Prevent lost updates with locking or optimistic checks.

<!-- concept -->

Isolation decides what a transaction sees of others running at the same time. Read Committed, the default, gives each statement a fresh snapshot. Repeatable Read keeps one snapshot for the whole transaction. Serializable makes concurrent transactions behave as if they ran one after another, aborting those that can't.

The classic bug at the default level is the lost update: two sessions read, modify and write the same value. Atomic updates, row locks or version checks prevent it.

<!-- example -->

```sql
-- optimistic locking: fail if someone else changed the row
UPDATE product SET price = 19.90, version = version + 1
WHERE product_id = 7 AND version = 12;
-- 0 rows updated → reload and retry
```

#### What are the transaction isolation levels in PostgreSQL?

- **Read Committed** (default): each statement sees data committed before it started.
- **Repeatable Read:** the whole transaction sees one snapshot, taken at its first statement. Concurrent conflicting updates cause serialization errors.
- **Serializable:** like Repeatable Read, plus detection of anomalies (serialisable snapshot isolation), so the result equals some serial order. Applications must retry on serialization failures.

Read Uncommitted is accepted but behaves like Read Committed.

#### What anomalies do isolation levels prevent?

Dirty reads (never possible in PostgreSQL), non-repeatable reads (prevented from Repeatable Read), phantom reads (also prevented by PostgreSQL's Repeatable Read) and serialization anomalies such as write skew (prevented only by Serializable).

#### What is the lost update problem, and how do you prevent it?

Two transactions read a value, both modify it, and the second write overwrites the first. Prevent it with an atomic update (`SET qty = qty - 1`), `SELECT ... FOR UPDATE`, optimistic locking with a version column, or Repeatable Read with retries.

#### What is optimistic locking?

Detecting conflicts at write time instead of locking: each row has a version, and an update succeeds only if the version is unchanged (`UPDATE ... SET ..., version = version + 1 WHERE id = $1 AND version = $2`).

<!-- challenge -->

Two support agents edit the same customer note at the same time, and one edit disappears. Which approach do you choose for a web app?

<!-- solution -->

Optimistic locking: keep a `version` column, update with `WHERE version = :read_version`, and show a conflict message if no row was updated, rather than holding locks during user think time.

<!-- takeaways -->

- Read Committed by default; Serializable for strict correctness.
- Lost updates happen with read-modify-write.
- Use atomic updates, row locks or version checks.

<!-- unit: Locks -->

<!-- goals -->

- Use row locks, SKIP LOCKED and advisory locks.
- Understand deadlocks and DDL lock conflicts.

<!-- concept -->

Most concurrency in PostgreSQL needs no explicit locks, but some patterns do. Locking selected rows reserves them until commit; skipping already-locked rows lets many workers pull jobs from one queue table; advisory locks coordinate application tasks.

Locks bring two risks: deadlocks, when transactions wait on each other, and DDL that takes exclusive locks and queues every other query behind it.

<!-- example -->

```sql
-- job queue worker
BEGIN;
SELECT job_id, payload FROM job
WHERE status = 'ready'
ORDER BY created_at
LIMIT 1
FOR UPDATE SKIP LOCKED;
-- process, then
UPDATE job SET status = 'done' WHERE job_id = :id;
COMMIT;
```

#### What is a deadlock, and how does PostgreSQL handle it?

Two transactions each wait for a lock the other holds. PostgreSQL detects it after `deadlock_timeout` and cancels one transaction with an error. Avoid deadlocks by locking rows in a consistent order and keeping transactions short.

#### What is `SELECT ... FOR UPDATE`?

It locks the selected rows against concurrent updates or deletes until the transaction ends, so you can read and then modify them safely. `FOR SHARE` allows other readers to lock too.

#### What does `SKIP LOCKED` do, and what is it used for?

It skips rows already locked by others instead of waiting, which makes it easy to build job queues:

```sql
SELECT id FROM jobs WHERE status = 'pending'
ORDER BY id LIMIT 10 FOR UPDATE SKIP LOCKED;
```

#### What are advisory locks?

Application-defined locks on arbitrary numbers (`pg_advisory_lock(42)`), managed by PostgreSQL but not tied to rows. They are used to ensure only one worker runs a task at a time.

#### Which locks does DDL take, and why can `ALTER TABLE` block everything?

Many `ALTER TABLE` forms take an `ACCESS EXCLUSIVE` lock, which conflicts with every other lock, including reads. If it waits behind a long query, all new queries queue behind it. Use `lock_timeout` and retry.

<!-- challenge -->

A migration runs `ALTER TABLE orders ADD COLUMN ...` and the whole app freezes, though the change itself is instant. Why?

<!-- solution -->

The `ALTER` waits for an `ACCESS EXCLUSIVE` lock behind a long-running query, and every new query queues behind the `ALTER`. Set `lock_timeout` in migrations and retry, and avoid running them during long transactions.

<!-- takeaways -->

- `FOR UPDATE SKIP LOCKED` builds job queues.
- PostgreSQL detects and breaks deadlocks.
- Waiting DDL locks queue everything; use `lock_timeout`.

<!-- unit: Vacuum and maintenance -->

<!-- goals -->

- Explain VACUUM, VACUUM FULL, autovacuum and ANALYZE.
- Avoid long-transaction bloat and transaction ID wraparound.

<!-- concept -->

MVCC's leftovers need cleaning. Vacuum makes dead tuples' space reusable, updates the visibility map and freezes old rows; autovacuum does it automatically as tables change, along with analyzing statistics. Full vacuum rewrites the table to shrink it, under an exclusive lock.

Two things defeat vacuum: long transactions, whose old snapshots keep dead tuples alive, and neglected tables that approach transaction ID wraparound, which forces emergency vacuuming.

<!-- example -->

```sql
SELECT relname, n_dead_tup, last_autovacuum, last_autoanalyze
FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 10;
ALTER TABLE events SET (autovacuum_vacuum_scale_factor = 0.02);   -- vacuum big tables more often
SELECT datname, age(datfrozenxid) FROM pg_database ORDER BY 2 DESC;
```

#### What does `VACUUM` do, and how is it different from `VACUUM FULL`?

`VACUUM` marks dead tuples' space as reusable, updates the visibility map and freezes old rows, without blocking reads or writes. `VACUUM FULL` rewrites the table to give space back to the operating system, but takes an exclusive lock. `pg_repack` does the same online.

#### What is autovacuum?

A background process that runs `VACUUM` and `ANALYZE` on tables when enough rows have changed, according to thresholds and scale factors that can be tuned per table.

#### What does `ANALYZE` do?

It samples tables and updates the statistics (`pg_statistic`) the planner uses to estimate row counts and choose plans.

#### Why are long-running transactions harmful?

They hold a snapshot, so vacuum can't remove dead tuples newer than it, causing bloat. They may also hold locks that block DDL and other writers. "Idle in transaction" sessions are a common culprit, limited with `idle_in_transaction_session_timeout`.

#### What is transaction ID wraparound?

Transaction IDs are 32-bit and wrap around. Vacuum must "freeze" old rows before that happens, otherwise PostgreSQL stops accepting writes to protect data. Autovacuum runs anti-wraparound vacuums automatically, and monitoring `age(datfrozenxid)` catches problems early.

<!-- challenge -->

A large table bloats although autovacuum runs. `pg_stat_activity` shows a session "idle in transaction" for two days. What is the link?

<!-- solution -->

The open transaction holds an old snapshot, so vacuum can't remove dead tuples newer than it. Terminate the session, set `idle_in_transaction_session_timeout`, and fix the application.

<!-- takeaways -->

- Vacuum reclaims space; full vacuum shrinks with a lock.
- Tune autovacuum per busy table.
- Long transactions block cleanup and risk wraparound.

### Performance and query planning

<!-- unit: Reading execution plans -->

<!-- goals -->

- Read EXPLAIN and EXPLAIN ANALYZE output.
- Recognize scan types, join algorithms and LIMIT behavior.

<!-- concept -->

The planner turns each query into a tree of operations and picks the cheapest according to its estimates. `EXPLAIN` shows that tree; `EXPLAIN ANALYZE` runs it and adds actual rows and times. Comparing estimated and actual rows is the most useful habit: large gaps mean bad statistics and usually bad plans.

Node types tell the story: how tables are read, how they're joined, and whether a `LIMIT` lets the query stop early thanks to a matching index.

<!-- example -->

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT o.* FROM orders o JOIN customer c USING (customer_id)
WHERE c.country_code = 'FR' AND o.ordered_at >= '2026-10-01';
-- look for: rows=estimated vs actual, Seq Scan on big tables, Sort spilling, loops
```

#### What does `EXPLAIN` show, and how is `EXPLAIN ANALYZE` different?

`EXPLAIN` shows the plan the planner chose, with estimated costs and row counts. `EXPLAIN ANALYZE` executes the query and adds actual times and row counts. Add `BUFFERS` to see pages read from cache or disk.

```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM company WHERE country_code = 'FR';
```

#### What should you look for in an execution plan?

Large differences between estimated and actual rows (bad statistics), sequential scans on big tables with selective filters, nested loops over many rows, sorts or hashes spilling to disk, and the nodes where most time is spent.

#### What are the main scan types?

Sequential scan (reads the whole table), index scan (follows the index, then reads table rows), index-only scan (from the index alone) and bitmap index/heap scan (collects matching locations from one or more indexes, then reads pages in physical order).

#### What are the three join algorithms?

- **Nested loop:** for each outer row, look up inner rows. Good when one side is small and the other is indexed.
- **Hash join:** builds a hash table on the smaller input. Good for large, unsorted equality joins.
- **Merge join:** both inputs sorted on the join key. Good for large inputs already sorted or indexed.

#### How does `LIMIT` interact with `ORDER BY` and indexes?

With an index matching the `ORDER BY`, PostgreSQL reads only the first rows it needs. Without one, it must sort everything (a top-N heapsort) before applying the limit.

<!-- challenge -->

A plan estimates 10 rows for a filter but gets 2 million, and chooses a nested loop that runs for minutes. What do you do?

<!-- solution -->

Fix the estimate: run `ANALYZE`, raise statistics for skewed columns, or add extended statistics for correlated columns, so the planner picks a hash join. Then check the plan again.

<!-- takeaways -->

- `EXPLAIN ANALYZE` shows actual rows and time.
- Estimate gaps point to statistics problems.
- Joins are nested loop, hash or merge.

<!-- unit: Statistics and estimates -->

<!-- goals -->

- Keep planner statistics accurate, including extended statistics.
- Diagnose queries that suddenly become slow.

<!-- concept -->

The planner is only as good as what it knows. Statistics sample each column's values; when they're stale, too coarse for skewed data, or blind to correlations between columns, estimates go wrong and plans follow. Wrapping indexed columns in functions also hides them from both index and statistics.

When a query that was fast becomes slow, the cause is usually one of these: a changed plan, stale statistics, more data, bloat, or new contention.

<!-- example -->

```sql
-- correlated columns: city implies country
CREATE STATISTICS addr_stats (dependencies) ON country_code, city FROM address;
ALTER TABLE orders ALTER COLUMN status SET STATISTICS 1000;
ANALYZE address; ANALYZE orders;
-- sargable rewrite:
-- WHERE date(created_at) = '2026-10-15'  →  WHERE created_at >= '2026-10-15' AND created_at < '2026-10-16'
```

#### Why can a function on an indexed column prevent index use?

The index stores the column's raw values, so `WHERE date(created_at) = '2026-10-15'` can't use an index on `created_at`. Rewrite it as a range (`created_at >= '2026-10-15' AND created_at < '2026-10-16'`) or create an expression index.

#### What are extended statistics?

`CREATE STATISTICS` lets the planner learn correlations between columns (dependencies, distinct counts, most common value combinations), improving estimates for filters on several correlated columns such as city and postcode.

#### What does `default_statistics_target` control?

How many sample values and histogram buckets `ANALYZE` keeps per column. Raising it for skewed columns improves estimates at the cost of planning time.

#### What would you check first when a query suddenly becomes slow?

Its plan (`EXPLAIN ANALYZE`) compared with before, statistics freshness (last analyze), data volume changes, locks and waits in `pg_stat_activity`, bloat, and whether parameters or a new index changed the plan.

<!-- challenge -->

A query filtering `WHERE country_code = 'FR' AND city = 'Paris'` estimates 50 rows but returns 400,000. Why, and the fix?

<!-- solution -->

The planner multiplies the two selectivities as if independent, but city implies country. Create extended statistics (dependencies) on the two columns and analyze.

<!-- takeaways -->

- Statistics drive estimates; keep them fresh.
- Extended statistics capture column correlations.
- Keep filters sargable: no functions on indexed columns.

<!-- unit: Memory, parallelism and JIT -->

<!-- goals -->

- Tune work_mem and the main memory settings.
- Understand parallel query and JIT compilation.

<!-- concept -->

Memory settings decide how much work stays in RAM. `shared_buffers` is PostgreSQL's own cache; `work_mem` is per operation, so a complex query with many sorts across many connections can multiply it many times. Too low and sorts spill to disk; too high and the server runs out of memory.

For large analytical queries, parallel workers split scans and joins, and JIT compiles expressions to machine code, which helps long queries and hurts short ones.

<!-- example -->

```text
shared_buffers = 16GB            # ~25% of 64 GB RAM
effective_cache_size = 48GB      # planner hint: OS cache + shared_buffers
work_mem = 32MB                  # per sort/hash node, per connection
maintenance_work_mem = 2GB       # VACUUM, CREATE INDEX
max_parallel_workers_per_gather = 4
```

#### What is `work_mem`, and why does it matter?

The memory each sort or hash operation may use before spilling to disk. Too low causes slow disk sorts. Too high risks running out of memory, because a single query can use several multiples of it.

#### What are the main memory settings to tune?

`shared_buffers` (PostgreSQL's cache, often about 25% of RAM), `effective_cache_size` (planner hint of total cache, often 50 to 75% of RAM), `work_mem` (per operation) and `maintenance_work_mem` (vacuum, index builds).

#### What is parallel query?

PostgreSQL can split sequential scans, joins and aggregations over several worker processes, controlled by `max_parallel_workers_per_gather` and table size.

#### What is JIT compilation in PostgreSQL?

Just-in-time compilation (with LLVM) of expressions in long analytical queries. It speeds up heavy computations but adds overhead to short queries. It is controlled by `jit` and cost thresholds.

<!-- challenge -->

`EXPLAIN ANALYZE` shows "Sort Method: external merge Disk: 2GB" for a nightly report. What do you change?

<!-- solution -->

Raise `work_mem` for that session or role (`SET work_mem = '512MB'` before the report), not globally, so the sort fits in memory without risking memory use for all connections.

<!-- takeaways -->

- `shared_buffers` caches; `work_mem` is per operation.
- Raise `work_mem` per session for big sorts.
- Parallel query and JIT help long analytical queries.

<!-- unit: Finding and stopping slow queries -->

<!-- goals -->

- Find expensive and running queries with pg_stat_statements and pg_stat_activity.
- Stop runaway queries and detect table bloat.

<!-- concept -->

Two views answer most performance questions. `pg_stat_statements` aggregates history by query shape, showing which queries cost the most time overall. `pg_stat_activity` shows what's running right now, how long, and what it waits on.

When something is stuck, you can cancel the query or terminate the session. Bloat, space held by dead tuples, is the slow-burning problem behind gradually slower scans.

<!-- example -->

```sql
SELECT pid, now() - query_start AS duration, state, wait_event_type, left(query, 80)
FROM pg_stat_activity
WHERE state <> 'idle' ORDER BY duration DESC;
SELECT pg_cancel_backend(12345);     -- cancel the query
SELECT pg_terminate_backend(12345);  -- close the connection
```

#### What is `pg_stat_statements`?

An extension that records execution statistics for every normalized query: calls, total and mean time, rows, buffer hits. It's the first place to look for slow or frequent queries.

#### How do you find currently running slow queries?

```sql
SELECT pid, now() - query_start AS duration, state, wait_event_type, query
FROM pg_stat_activity
WHERE state <> 'idle'
ORDER BY duration DESC;
```

#### How do you stop a runaway query?

`SELECT pg_cancel_backend(pid)` cancels the current query. `pg_terminate_backend(pid)` closes the whole connection. `statement_timeout` prevents runaway queries in the first place.

#### What is table bloat, and how do you detect it?

Wasted space from dead tuples that vacuum hasn't reclaimed or the operating system hasn't got back. Detect it with `pgstattuple`, bloat-estimation queries, or tables growing faster than their row count.

<!-- challenge -->

The database is slow, but no single query looks long-running. Where do you look for the cause?

<!-- solution -->

`pg_stat_statements` ordered by total execution time: often a fast query called millions of times dominates load. Optimize or cache it, or reduce how often it's called.

<!-- takeaways -->

- `pg_stat_statements` ranks queries by total cost.
- `pg_stat_activity` shows what's running now.
- Cancel queries first; terminate sessions if needed.

<!-- unit: Connections and bulk loading -->

<!-- goals -->

- Pool connections with PgBouncer.
- Load large volumes quickly with COPY.

<!-- concept -->

Two common performance problems sit outside query plans. Too many connections waste memory and CPU on process management, so a pooler like PgBouncer lets thousands of clients share a few dozen server connections.

Loading data row by row wastes round trips and per-statement overhead. `COPY` streams data in bulk, and loading before creating indexes, inside one transaction, is faster still.

<!-- example -->

```bash
psql -c "\copy staging.orders (order_id, customer_id, amount, ordered_at) FROM 'orders.csv' WITH (FORMAT csv, HEADER true)"
```
```ini
; pgbouncer.ini
pool_mode = transaction
default_pool_size = 40
max_client_conn = 2000
```

#### What is connection pooling, and why is PgBouncer used?

Reusing a small number of database connections for many clients. PgBouncer sits between applications and PostgreSQL, in session, transaction or statement mode, cutting the per-connection overhead.

#### How do you load large amounts of data quickly?

Use `COPY` instead of row-by-row inserts, load inside one transaction, create indexes and foreign keys after loading, consider unlogged staging tables, increase `maintenance_work_mem` for index builds, and run `ANALYZE` afterwards.

#### What is the `COPY` command?

The fastest way to bulk load or export data between tables and files or streams: `COPY company FROM '/data/company.csv' WITH (FORMAT csv, HEADER)`. From a client, use psql's `\copy` or the driver's COPY support. PostgreSQL 17 can skip malformed rows with `ON_ERROR ignore`.

<!-- challenge -->

A Python script inserts 10 million rows with one `INSERT` per row and takes 3 hours. What do you change?

<!-- solution -->

Use `COPY` (for example `cursor.copy_expert` or psycopg's `copy`) into a staging table, inside one transaction, then upsert into the target in one set-based statement. Expect minutes instead of hours.

<!-- takeaways -->

- Pool connections; don't open thousands directly.
- `COPY` is the fast path for bulk loads.
- Load first, index after, in one transaction.

<!-- stage: Design and operations -->

### Data modeling, normalization and OLAP

<!-- unit: Normalization -->

<!-- goals -->

- Explain 1NF, 2NF, 3NF and BCNF.
- Decide when denormalization is justified, OLTP versus OLAP.

<!-- concept -->

Normalization stores each fact once so updates can't leave contradictions: no repeating groups, no attributes depending on part of a key, no attributes depending on other non-key attributes. That's the right shape for transactional systems, where correctness of many small writes matters most.

Analytics reverses the priorities: reads dominate, so deliberate redundancy, such as pre-joined or pre-aggregated tables, makes queries simpler and faster.

<!-- example -->

```text
Not 3NF: orders(order_id, customer_id, customer_city, amount)   ← city depends on customer
3NF:     orders(order_id, customer_id, amount)
         customer(customer_id, city)
```

#### Name the three main normal forms.

- **First normal form (1NF):** each column holds atomic values, with no repeating groups or lists in a column, and each row is unique.
- **Second normal form (2NF):** 1NF, and every non-key column depends on the whole primary key, not just part of a composite key.
- **Third normal form (3NF):** 2NF, and non-key columns depend only on the key, not on other non-key columns (no transitive dependencies).

#### What is BCNF?

Boyce-Codd normal form, a stricter 3NF: every determinant (a column set that determines another column) must be a candidate key.

#### What is denormalization, and when is it justified?

Deliberately adding redundancy (duplicated columns, pre-joined or pre-aggregated tables) to speed up reads, for analytics and reporting where queries dominate and data is loaded in controlled batches.

#### What is the difference between OLTP and OLAP?

OLTP (online transaction processing) handles many short reads and writes on current data, with normalized schemas and row-oriented storage. OLAP (online analytical processing) runs complex queries over large historical datasets, with denormalized schemas (star schemas) and columnar storage.

<!-- challenge -->

A table stores customer city on every order, and after a move, old and new orders show different cities. Is that a bug?

<!-- solution -->

In an OLTP model, yes: the city depends on the customer, so it belongs in the customer table (3NF). In an analytical model, storing the city at order time may be intended history, but then it should be explicit.

<!-- takeaways -->

- Normal forms remove redundancy and update anomalies.
- OLTP favors normalization; OLAP tolerates redundancy.
- Denormalize deliberately, for reads.

<!-- unit: Dimensional basics -->

<!-- goals -->

- Describe OLAP operations, star and snowflake schemas.
- Declare a fact table's grain and type.

<!-- concept -->

Analytical models are organized around questions: facts hold measurements, dimensions hold the context you slice by. OLAP operations, drilling down, rolling up, slicing and pivoting, are ways of moving through that structure.

A star keeps dimensions flat around the fact, a snowflake normalizes them. The most important decision is the grain, what one fact row means, which then decides the fact type: events, periodic snapshots or accumulating processes.

<!-- example -->

```text
fct_sales (grain: one order line)
  date_key, customer_key, product_key, store_key, quantity, net_amount
dim_date, dim_customer, dim_product, dim_store  (star)
```

#### Which are the main OLAP operations in an OLAP system?

OLAP operations work on a multidimensional model where data is represented as cubes. There are five basic analytical operations:

- **Drill down:** move to a more detailed level of a hierarchy, for example year → quarter → month.
- **Roll up:** the opposite of drill down, aggregating to a higher level, for example city → country or month → quarter.
- **Slice:** fix one dimension to a single value to get a sub-cube with one less dimension, for example only Q1.
- **Dice:** filter on two or more dimensions to get a smaller sub-cube, for example location = Bogotá and product = coffee.
- **Pivot:** rotate the cube to swap dimensions on the axes and see the data from another angle.

#### What is a star schema?

A dimensional model with a central fact table (measures and foreign keys) surrounded by dimension tables (descriptive attributes). It is simple to query and fast for analytics.

#### What is a snowflake schema?

A star schema whose dimensions are normalized into several related tables (product → category → department). It saves space but needs more joins.

#### What is the grain of a fact table?

What exactly one row represents (one order line, one daily balance per account). Declaring it first is the most important step in dimensional design.

#### What are the types of fact tables?

Transaction facts (one row per event), periodic snapshots (one row per entity per period, such as month-end balances) and accumulating snapshots (one row per process instance, updated as it moves through milestones).

<!-- challenge -->

A team needs month-end account balances. Should they sum transaction facts on the fly or store something else?

<!-- solution -->

Store a periodic snapshot fact (one row per account per month with the balance). Balances are semi-additive and expensive to reconstruct from all historical transactions.

<!-- takeaways -->

- Facts measure; dimensions describe.
- Stars are simpler than snowflakes.
- Grain decides the fact type.

<!-- unit: Keys and dimensions -->

<!-- goals -->

- Use surrogate and natural keys in a warehouse.
- Build junk, degenerate, conformed and date dimensions.

<!-- concept -->

Warehouses issue their own surrogate keys for dimension rows, keeping natural keys from sources as attributes. That isolates the model from source changes and lets one entity have historical versions.

A few dimension patterns recur: junk dimensions for leftover flags, degenerate dimensions for identifiers kept in the fact, conformed dimensions shared across marts, and a date dimension that holds calendar logic once.

<!-- example -->

```sql
INSERT INTO dim_date (date_key, day, month, quarter, is_weekend)
SELECT to_char(d, 'YYYYMMDD')::int, d::date, extract(month FROM d), extract(quarter FROM d),
       extract(isodow FROM d) IN (6, 7)
FROM generate_series('2020-01-01'::date, '2030-12-31', interval '1 day') AS d;
```

#### What is a surrogate key, and why use it in a warehouse?

A meaningless generated key (identity or hash) instead of the source's natural key. It isolates the warehouse from source key changes, allows several versions of a record (SCD2), and joins efficiently.

#### What is a natural key?

A key that has meaning in the business or source system, such as a SIRET or an email address. It should be kept as an attribute even when a surrogate key is used.

#### What is a junk dimension?

A dimension that groups several low-cardinality flags and indicators (payment type, is_promo) into one table, instead of cluttering the fact table.

#### What is a degenerate dimension?

A dimension key stored in the fact table with no dimension table of its own, such as an invoice number.

#### What is a conformed dimension?

A dimension shared with the same meaning and keys across several fact tables or data marts (date, customer), so results can be combined.

#### What is a date dimension, and why build one?

A table with one row per day and attributes (weekday, month, quarter, holiday flags, fiscal periods). It makes calendar filters and grouping simple and consistent:

```sql
SELECT d::date AS day, extract(isodow FROM d) AS weekday, extract(quarter FROM d) AS quarter
FROM generate_series('2020-01-01'::date, '2030-12-31', interval '1 day') AS d;
```

<!-- challenge -->

Reports group by quarter using `extract(quarter ...)` everywhere, but the company's fiscal year starts in April. How do you fix it once?

<!-- solution -->

Add fiscal attributes (fiscal year, fiscal quarter) to the date dimension, computed once, and have reports join to it instead of computing quarters themselves.

<!-- takeaways -->

- Surrogate keys isolate the warehouse from sources.
- Junk, degenerate and conformed dimensions solve recurring needs.
- A date dimension centralizes calendar logic.

<!-- unit: History and architectures -->

<!-- goals -->

- Implement slowly changing dimensions in PostgreSQL.
- Place PostgreSQL among Data Vault, medallion and analytical engines.

<!-- concept -->

Dimensions change, and type 2 slowly changing dimensions keep history by closing the current version and inserting a new one, ideally in a single transaction so readers never see a gap.

PostgreSQL works well as a small warehouse or a serving layer, but it isn't columnar: at many terabytes of scans, dedicated warehouses or lakehouses fit better. Methodologies like Data Vault and medallion layers apply either way.

<!-- example -->

```sql
BEGIN;
UPDATE dim_customer SET valid_to = now(), is_current = false
WHERE customer_id = 552 AND is_current;
INSERT INTO dim_customer (customer_id, segment, valid_from, valid_to, is_current)
VALUES (552, 'Mid', now(), 'infinity', true);
COMMIT;
```

#### What are slowly changing dimensions (SCD)?

Ways to handle changes in dimension attributes. Type 1 overwrites, so no history is kept. Type 2 adds a new row per version with validity dates and a current flag. Type 3 keeps the previous value in an extra column. Types 4 and 6 combine approaches.

#### How do you implement an SCD Type 2 in PostgreSQL?

Close the current version and insert the new one in one transaction:

```sql
BEGIN;
UPDATE dim_customer SET valid_to = now(), is_current = false
WHERE customer_id = $1 AND is_current AND row_hash <> $2;
INSERT INTO dim_customer (customer_id, name, city, row_hash, valid_from, valid_to, is_current)
SELECT $1, $3, $4, $2, now(), NULL, true
WHERE NOT EXISTS (SELECT 1 FROM dim_customer WHERE customer_id = $1 AND is_current);
COMMIT;
```

#### What is Data Vault modeling?

A modeling method for integrating many sources with full history: hubs (business keys), links (relationships) and satellites (descriptive attributes with load dates). It favors auditability and parallel loading, and usually feeds star schemas for reporting.

#### When would you not use PostgreSQL for analytics?

When data reaches many terabytes or queries scan huge volumes routinely: columnar warehouses or lakehouses (Redshift, BigQuery, Snowflake, Databricks) scale better. Extensions such as Citus or columnar storage, or DuckDB for local analysis, can extend PostgreSQL's reach first.

#### What is the medallion architecture, and where does a relational database fit in it?

A lakehouse layering into bronze (raw), silver (cleaned and conformed) and gold (business-level aggregates and models). A relational database such as PostgreSQL is often a source system, or a serving layer for gold data used by applications.

<!-- challenge -->

A PostgreSQL reporting database now holds 6 TB and dashboards scanning months of data take minutes. What do you suggest?

<!-- solution -->

Partition and pre-aggregate in the short term, but plan to move large-scan analytics to a columnar warehouse or lakehouse, keeping PostgreSQL for operational and small serving workloads.

<!-- takeaways -->

- SCD2 closes and inserts versions in one transaction.
- PostgreSQL suits small warehouses and serving layers.
- Large scans belong in columnar engines.

### Administration, security, backup and replication

<!-- unit: Roles and access -->

<!-- goals -->

- Manage roles, read-only access and row-level security.
- Configure authentication and prevent SQL injection.

<!-- concept -->

In PostgreSQL, users and groups are both roles, and privileges flow through role membership. Read access to a schema needs usage on the schema, select on tables and default privileges for tables created later. Row-level security narrows access further, per row.

Who can connect at all is decided by host-based rules and strong password hashing. Inside applications, parameterized queries keep user input from becoming SQL.

<!-- example -->

```sql
CREATE ROLE reporting NOLOGIN;
GRANT USAGE ON SCHEMA analytics TO reporting;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO reporting;
ALTER DEFAULT PRIVILEGES IN SCHEMA analytics GRANT SELECT ON TABLES TO reporting;
CREATE ROLE ana LOGIN PASSWORD '...' IN ROLE reporting;
```

#### What are roles in PostgreSQL?

Roles are both users and groups: a role with `LOGIN` is a user, and roles can be granted to other roles to inherit their privileges.

#### How do you grant read-only access to a schema?

```sql
CREATE ROLE reporting NOLOGIN;
GRANT USAGE ON SCHEMA analytics TO reporting;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO reporting;
ALTER DEFAULT PRIVILEGES IN SCHEMA analytics GRANT SELECT ON TABLES TO reporting;
GRANT reporting TO alice;
```

PostgreSQL 14+ also has the predefined role `pg_read_all_data`.

#### What is row-level security (RLS)?

Policies that restrict which rows each role can see or modify:

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders USING (tenant_id = current_setting('app.tenant_id')::int);
```

#### What is `pg_hba.conf`?

The host-based authentication file: rules for which users can connect to which databases from which addresses, with which method (`scram-sha-256`, `cert`, `peer`). `trust` should never be used outside local tests.

#### How should passwords be stored and checked?

With `scram-sha-256` (the default since PostgreSQL 14) rather than md5, connections encrypted with TLS, and application credentials kept in a secrets manager.

#### How do you prevent SQL injection?

Use parameterized queries (placeholders bound by the driver) instead of string concatenation. In dynamic SQL inside functions, use `format()` with `%I` for identifiers and `%L` for literals, or `EXECUTE ... USING`.

<!-- challenge -->

A read-only role works for existing tables, but analysts lose access to every new table. What is missing?

<!-- solution -->

Default privileges: `ALTER DEFAULT PRIVILEGES ... GRANT SELECT ON TABLES TO reporting` for the role that creates tables, so future tables are granted automatically.

<!-- takeaways -->

- Roles are users and groups; grant through membership.
- Default privileges cover future tables.
- RLS restricts rows; parameters prevent injection.

<!-- unit: Backups and recovery -->

<!-- goals -->

- Compare logical and physical backups.
- Back up with pg_dump and recover to a point in time.

<!-- concept -->

Backups come in two kinds. Logical backups export objects and data as SQL or archives: portable across versions, selective, but slow for big databases. Physical backups copy data files and, with archived WAL, allow replaying changes up to any moment.

That second ability, point-in-time recovery, is what saves you from mistakes like a bad delete at 10:42: restore the base backup and stop replay at 10:41.

<!-- example -->

```bash
pg_dump -Fc -d shop -f shop.dump
pg_restore -d shop_restore -j 4 shop.dump
# PITR: restore base backup, then in postgresql.conf
#   restore_command = 'cp /archive/%f %p'
#   recovery_target_time = '2026-10-17 10:41:00+02'
```

#### What is the difference between logical and physical backups?

Logical backups (`pg_dump`, `pg_dumpall`) export SQL or archive files of objects and data. They are portable across versions and can be restored selectively, but are slow for large databases. Physical backups (`pg_basebackup`, pgBackRest) copy the data files plus WAL. They are fast for large databases and allow point-in-time recovery.

#### How do you back up and restore a single database with pg_dump?

```bash
pg_dump -Fc -d mydb -f mydb.dump          # custom format, compressed
pg_restore -d newdb -j 4 mydb.dump        # parallel restore
```

#### What is point-in-time recovery (PITR)?

Restoring a base backup and replaying archived WAL up to a chosen moment, for example just before an accidental `DELETE`.

<!-- challenge -->

A 4 TB database is backed up nightly with `pg_dump`, which takes 9 hours, and restores would take longer. What do you change?

<!-- solution -->

Switch to physical backups (pgBackRest or the managed service's snapshots) with continuous WAL archiving, enabling fast restores and point-in-time recovery; keep `pg_dump` for selective exports.

<!-- takeaways -->

- Logical backups are portable; physical ones are fast.
- WAL archiving enables point-in-time recovery.
- Test restores, not just backups.

<!-- unit: Replication and CDC -->

<!-- goals -->

- Compare streaming and logical replication, synchronous and asynchronous.
- Use CDC and replication slots safely, and build high availability.

<!-- concept -->

Streaming replication ships WAL to standbys that replay it, keeping exact copies for failover and read scaling. Asynchronous replicas may lag; synchronous ones make commits wait for confirmation, trading latency for no data loss.

Logical replication works per table and across versions, and CDC tools build on the same decoding to stream changes to Kafka or a lake. Replication slots keep WAL until consumers read it, which fills disks if a consumer disappears. HA adds a failover manager on top.

<!-- example -->

```sql
-- publisher
CREATE PUBLICATION orders_pub FOR TABLE orders, order_line;
-- subscriber
CREATE SUBSCRIPTION orders_sub CONNECTION 'host=primary dbname=shop user=repl' PUBLICATION orders_pub;
-- watch slots
SELECT slot_name, active, pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS retained
FROM pg_replication_slots;
```

#### What is streaming replication?

A standby server continuously receives and replays WAL from the primary, keeping a byte-for-byte copy. It can serve read-only queries (hot standby) and be promoted if the primary fails.

#### What is the difference between synchronous and asynchronous replication?

With asynchronous replication, commits don't wait for standbys, so a failover can lose the last transactions. With synchronous replication, commits wait for confirmation from one or more standbys, so no data is lost, at the cost of commit latency.

#### What is logical replication?

Replication of row changes per table through publications and subscriptions. It works across major versions and allows replicating a subset of tables, which is useful for upgrades, consolidation and change data capture.

#### What is change data capture (CDC) with PostgreSQL?

Streaming row-level changes from the WAL through logical decoding, often with Debezium and Kafka, so downstream systems (data lakes, search indexes) receive inserts, updates and deletes in near real time.

#### What is a replication slot, and what's the risk?

A slot makes the primary keep WAL until a consumer has received it. If the consumer stops, WAL accumulates and can fill the disk, so monitor `pg_replication_slots`.

#### What is high availability for PostgreSQL usually built with?

Streaming replication plus a failover manager such as Patroni (with etcd or Consul), or a managed service (Amazon RDS or Aurora, Cloud SQL, Azure Database for PostgreSQL) that handles failover.

<!-- challenge -->

After a failover to an asynchronous standby, the last few seconds of orders are missing. How could you have prevented it, and at what cost?

<!-- solution -->

Synchronous replication to at least one standby (`synchronous_standby_names`), so commits wait for the standby to confirm. The cost is higher commit latency and dependence on standby availability.

<!-- takeaways -->

- Streaming replication copies everything; logical replication copies tables.
- Synchronous replication avoids loss at a latency cost.
- Monitor slots; inactive ones retain WAL.

<!-- unit: Running a server -->

<!-- goals -->

- Upgrade major versions and monitor a PostgreSQL server.
- Use cache hit ratio, statement_timeout and managed services.

<!-- concept -->

Operating PostgreSQL means watching a few signals and planning a few events. Signals: connections, transaction rates, cache hit ratio, slow queries, locks, replication lag, bloat and wraparound age. Events: major upgrades, which need testing and a method that fits the size and downtime allowed.

Guardrails like statement timeouts stop runaway queries per role. Managed services take over much of the routine, but tuning and design stay with you.

<!-- example -->

```sql
SELECT round(100.0 * sum(blks_hit) / nullif(sum(blks_hit) + sum(blks_read), 0), 2) AS cache_hit_pct
FROM pg_stat_database;
ALTER ROLE reporting SET statement_timeout = '5min';
```

#### How do you upgrade PostgreSQL to a new major version?

With `pg_upgrade` (fast, in place, with `--link` or `--clone`), dump and restore (simple but slow), or logical replication to a new cluster for near-zero downtime.

#### What should you monitor on a PostgreSQL server?

Connections, transaction rate, cache hit ratio, slow queries (`pg_stat_statements`), locks and waits, replication lag, autovacuum activity and bloat, transaction ID age, disk space and WAL growth, checkpoints and I/O.

#### What is the cache hit ratio, and how do you compute it?

The share of block reads served from `shared_buffers`. For OLTP workloads it should usually be above 99%:

```sql
SELECT round(100.0 * sum(blks_hit) / nullif(sum(blks_hit) + sum(blks_read), 0), 2)
FROM pg_stat_database;
```

#### What is `statement_timeout`, and where should you set it?

The maximum time a statement may run before being canceled. Set it per role or per application (for example 30 seconds for a web application) to protect the server from runaway queries.

#### What does Amazon RDS for PostgreSQL manage for you?

Provisioning, automated backups and PITR, minor version patching, Multi-AZ failover, read replicas, monitoring and storage scaling. You keep responsibility for schema, queries, users, parameters and network access, and you have no superuser or operating-system access.

<!-- challenge -->

Ad hoc analyst queries sometimes run for hours and slow the application. What guardrail do you add without affecting the app?

<!-- solution -->

Set `statement_timeout` on the analysts' role (for example 5 minutes), not globally, and route them to a read replica if they need longer queries.

<!-- takeaways -->

- Monitor connections, cache, slow queries, locks and lag.
- Plan major upgrades with tests.
- Set timeouts per role.

### Advanced features

<!-- unit: JSON in PostgreSQL -->

<!-- goals -->

- Choose between json and jsonb and query documents.
- Decide when to store JSONB instead of columns.

<!-- concept -->

PostgreSQL stores documents natively. `jsonb` parses once into a binary form that can be indexed and queried efficiently; `json` keeps the exact text. Operators extract values, test containment and follow paths, and set-returning functions turn arrays into rows for joining.

JSONB is ideal for sparse or varying attributes and raw payloads. Fields that every query filters, joins or aggregates on usually deserve real columns, with types and constraints.

<!-- example -->

```sql
SELECT e.event_id,
       e.payload->>'type'                 AS type,
       (item->>'qty')::int                AS qty
FROM events e,
     jsonb_array_elements(e.payload->'items') AS item
WHERE e.payload @> '{"channel": "web"}';
```

#### What is the difference between `json` and `jsonb`?

`json` stores the exact input text and parses it on every access. `jsonb` stores a decomposed binary form, removes whitespace and duplicate keys, is faster to query and supports indexing. `jsonb` is the usual choice.

#### What are the main JSONB operators?

`->` returns a JSON value, `->>` returns text, `#>` and `#>>` follow a path, `@>` tests containment, `?` tests key existence, `||` concatenates, and `-` removes a key.

```sql
SELECT payload->>'user_id' AS user_id
FROM events
WHERE payload @> '{"type": "click"}';
```

#### What is SQL/JSON path in PostgreSQL?

A query language for JSON (`jsonb_path_query`, `@?`, `@@`). PostgreSQL 17 adds the standard `JSON_TABLE`, `JSON_VALUE` and `JSON_QUERY` functions to turn JSON into relational rows.

#### How do you turn a JSON array into rows?

```sql
SELECT e.id, item->>'sku' AS sku, (item->>'qty')::int AS qty
FROM orders e, jsonb_array_elements(e.payload->'items') AS item;
```

#### When should you store data as JSONB rather than columns?

For semi-structured or sparse attributes that vary between rows, or raw payloads kept for reference. Columns are better for fields you filter, join or aggregate on regularly, because they have proper types, constraints and statistics.

<!-- challenge -->

Every report filters and aggregates on `payload->>'country'`, stored in a JSONB column, and queries are slow. What do you change?

<!-- solution -->

Promote `country` to a real column (a generated column from the JSON or populated on write) with an index, since it's used by every query; keep the rest in JSONB.

<!-- takeaways -->

- Use `jsonb` for indexing and fast queries.
- Operators extract, test containment and follow paths.
- Promote frequently used fields to columns.

<!-- unit: Server-side code -->

<!-- goals -->

- Write PL/pgSQL functions, procedures and triggers.
- Choose function volatility and use LISTEN/NOTIFY.

<!-- concept -->

Some logic belongs next to the data: keeping `updated_at` current, enforcing complex rules, notifying listeners of changes. PL/pgSQL functions and triggers do that. Functions return values and run inside the caller's transaction; procedures can manage transactions themselves.

Volatility labels tell the planner what a function may do, which affects caching and whether it can back an index. LISTEN/NOTIFY offers lightweight messaging between sessions.

<!-- example -->

```sql
CREATE FUNCTION touch_updated_at() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at := now();
  RETURN NEW;
END $$;
CREATE TRIGGER orders_touch BEFORE UPDATE ON orders
FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
```

#### What is a PL/pgSQL function?

A function written in PostgreSQL's procedural language, with variables, loops, conditions and exception handling, executed inside the server.

#### What is the difference between a function and a procedure?

Functions return a value and are called in queries. They run inside the caller's transaction. Procedures (PostgreSQL 11+) are invoked with `CALL`, return nothing (or output parameters) and can `COMMIT` and `ROLLBACK` inside, which suits batch maintenance jobs.

#### What are function volatility categories?

`IMMUTABLE` (same result for the same arguments forever, required for expression indexes), `STABLE` (constant within one statement) and `VOLATILE` (may change on every call, the default). Marking them correctly lets the planner optimize.

#### What is a trigger?

A function executed automatically before or after `INSERT`, `UPDATE`, `DELETE` or `TRUNCATE`, per row or per statement. It is used for audit logs, maintaining derived columns or enforcing complex rules. Triggers hide logic, so use them sparingly.

#### How do you keep an `updated_at` column current with a trigger?

```sql
CREATE FUNCTION touch_updated_at() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at := now();
    RETURN NEW;
END $$;

CREATE TRIGGER company_touch BEFORE UPDATE ON company
FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
```

#### What does `LISTEN` / `NOTIFY` do?

A built-in publish/subscribe mechanism: a session sends `NOTIFY channel, 'payload'` and every session that ran `LISTEN channel` receives it after commit. It's useful for lightweight cache invalidation or job wake-ups.

<!-- challenge -->

An expression index on `my_normalize(name)` fails with "functions in index expression must be marked IMMUTABLE". What does it mean?

<!-- solution -->

Index values must never change for the same input, so the function must be declared `IMMUTABLE`. Mark it so only if it truly is (no dependence on settings, time or tables); otherwise use a generated column.

<!-- takeaways -->

- Functions return values; procedures can commit.
- Triggers run logic on row changes.
- Volatility labels must be truthful.

<!-- unit: Partitioning -->

<!-- goals -->

- Partition tables by range, list or hash.
- Decide when partitioning is worth it.

<!-- concept -->

Partitioning splits one logical table into many physical ones by a key, usually time. Queries that filter on the key touch only the relevant partitions, and old data can be dropped instantly by detaching a partition instead of deleting millions of rows.

It adds planning overhead and rules for keys and indexes, so it pays off for large tables with a natural pruning key and a lifecycle, not for every big table.

<!-- example -->

```sql
CREATE TABLE events (event_id bigint, occurred_at timestamptz NOT NULL, payload jsonb)
PARTITION BY RANGE (occurred_at);
CREATE TABLE events_2026_10 PARTITION OF events
  FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
ALTER TABLE events DETACH PARTITION events_2024_10;   -- then DROP: instant retention
```

#### What is table partitioning?

Splitting a large table into partitions by `RANGE`, `LIST` or `HASH` of a key, behind one parent table. Queries that filter on the key read only the relevant partitions (partition pruning), and old data can be dropped instantly by detaching or dropping a partition.

```sql
CREATE TABLE events (id bigint, created_at timestamptz NOT NULL, payload jsonb)
PARTITION BY RANGE (created_at);
CREATE TABLE events_2026_10 PARTITION OF events
FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
```

#### When is partitioning worth it?

For very large tables with a natural key for pruning (usually time) and a lifecycle that drops or archives old data. It adds complexity: primary keys must include the partition key, and too many partitions slow planning.

<!-- challenge -->

A 2-billion-row events table needs 13 months of retention, and the nightly `DELETE` of old rows takes hours and bloats the table. What do you propose?

<!-- solution -->

Partition by month on `occurred_at` and drop (or detach and archive) the oldest partition each month, which is instant and leaves no dead tuples.

<!-- takeaways -->

- Partitions prune by key and simplify retention.
- Dropping partitions replaces mass deletes.
- Partition only tables that benefit.

<!-- unit: Extensions -->

<!-- goals -->

- Use common extensions such as pg_stat_statements, PostGIS and pgvector.
- Query external data with foreign data wrappers and search text.

<!-- concept -->

Extensions are how PostgreSQL grows: one command adds new types, functions, indexes or integrations. Some are almost standard, like query statistics; others turn PostgreSQL into a geospatial database, a vector store or a gateway to other systems.

Full-text search is built in, with language-aware stemming and ranking, often enough to avoid a separate search engine for moderate needs.

<!-- example -->

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE doc_chunk (id bigint PRIMARY KEY, body text, embedding vector(1536));
CREATE INDEX ON doc_chunk USING hnsw (embedding vector_cosine_ops);
SELECT id, body FROM doc_chunk ORDER BY embedding <=> :query_embedding LIMIT 5;
```

#### What are extensions, and name some useful ones?

Packages that add features with `CREATE EXTENSION`: `pg_stat_statements` (query statistics), `pg_trgm` (similarity and trigram indexes), `postgis` (geospatial), `pgcrypto`, `uuid-ossp`, `postgres_fdw`, `pg_partman` (partition management), `pgvector` (vector similarity search), `timescaledb` (time series), `citus` (distribution).

#### What is PostGIS?

The spatial extension for PostgreSQL: geometry and geography types, spatial functions (distance, intersection, buffers), GiST indexes and coordinate system transformations. It's the standard open-source spatial database.

#### What is a foreign data wrapper (FDW)?

An extension that lets PostgreSQL query external data sources as if they were local tables: `postgres_fdw` (other PostgreSQL servers), `file_fdw` (files), and others for MySQL, Oracle, S3 or Parquet.

#### What is pgvector?

An extension adding a `vector` type and similarity search (cosine, L2, inner product) with HNSW and IVFFlat indexes. It's used to store embeddings for semantic search and retrieval-augmented generation.

#### What is full-text search in PostgreSQL?

Searching documents with `tsvector` (normalized lexemes) and `tsquery`, with language-specific stemming, ranking (`ts_rank`) and GIN indexes:

```sql
SELECT * FROM article
WHERE to_tsvector('english', body) @@ websearch_to_tsquery('english', 'data pipeline');
```

<!-- challenge -->

A support app needs "search articles by words, ranked, in Spanish" and the team plans to add Elasticsearch. What can PostgreSQL offer first?

<!-- solution -->

Built-in full-text search: a `tsvector` column with the `spanish` configuration, a GIN index, and `ts_rank` ordering. Move to a search engine only if relevance tuning or scale outgrow it.

<!-- takeaways -->

- Extensions add types, indexes and integrations.
- PostGIS, pgvector and FDWs cover specialized needs.
- Built-in full-text search covers many search needs.

<!-- unit: Handy functions -->

<!-- goals -->

- Use common date and time functions.
- Generate test data quickly in SQL.

<!-- concept -->

A small set of functions covers most date work: current time, truncating to periods, extracting parts, adding intervals and computing ages. Using them in the database keeps time-zone and calendar logic consistent.

The same toolkit generates realistic test data: series of numbers or dates combined with random functions produce millions of rows in seconds, which is ideal for testing queries and indexes.

<!-- example -->

```sql
INSERT INTO orders (customer_id, amount, ordered_at)
SELECT (random() * 10000)::int + 1,
       round((random() * 200)::numeric, 2),
       now() - random() * interval '365 days'
FROM generate_series(1, 1000000);
SELECT date_trunc('month', ordered_at) AS month, count(*) FROM orders GROUP BY 1 ORDER BY 1;
```

#### What are common table functions for dates?

`now()` and `current_date`, `date_trunc('month', ts)`, `extract(year FROM ts)`, `age(a, b)`, interval arithmetic (`ts + interval '7 days'`), `to_char(ts, 'YYYY-MM')` and `make_date(y, m, d)`.

#### How do you generate test data quickly in PostgreSQL?

With `generate_series` and random functions:

```sql
INSERT INTO company (country_code, business_id, name, employees)
SELECT (ARRAY['FR','GB','IE','NO'])[1 + floor(random() * 4)::int],
       lpad(i::text, 9, '0'),
       'Company ' || i,
       floor(random() * 500)::int
FROM generate_series(1, 1000000) AS i;
```

<!-- challenge -->

You need to check whether a new index helps a query on 10 million orders, but dev has 500 rows. How do you test realistically in minutes?

<!-- solution -->

Generate 10 million rows with `generate_series` and random values matching realistic distributions, `ANALYZE`, then compare `EXPLAIN ANALYZE` with and without the index.

<!-- takeaways -->

- `date_trunc`, `extract`, intervals and `age` cover most date work.
- `generate_series` plus `random()` creates test data fast.
- Test performance on realistic volumes.
