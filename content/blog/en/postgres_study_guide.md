## PostgreSQL Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![PostgreSQL study guide: about 200 questions](../../images/postgres_study_guide_title_img.png)

About 200 questions on PostgreSQL and SQL for data engineering interviews: architecture, data types, querying, window functions, indexes, transactions and MVCC, performance tuning, data modeling, administration and advanced features such as JSONB and partitioning. Examples target PostgreSQL 16 and 17. Open a question to see its answer, or use the filter to search the whole guide.

<!-- QA -->

### Basics and architecture

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

#### What is the difference between `DELETE`, `TRUNCATE` and `DROP`?

`DELETE` removes rows one by one, can have a `WHERE` clause, fires triggers and leaves dead tuples for vacuum. `TRUNCATE` empties the whole table quickly by replacing its files. `DROP` removes the table itself. In PostgreSQL, all three are transactional.

#### What is a sequence?

A database object that generates increasing numbers, used for surrogate keys. `GENERATED ... AS IDENTITY` columns (SQL standard) and the older `serial` types use sequences. Sequences aren't transactional: rolled-back inserts leave gaps.

#### What is the difference between `serial` and identity columns?

Both auto-generate integers from a sequence. Identity columns are standard SQL, tie the sequence to the column more cleanly, and with `GENERATED ALWAYS` prevent accidental manual values. They are preferred for new tables.

#### What is a view?

A stored query that you can select from like a table. It holds no data, and its query runs on each access. Simple views can be updatable.

#### What is a materialized view?

A view whose result is stored on disk and refreshed explicitly with `REFRESH MATERIALIZED VIEW`. With a unique index, `REFRESH ... CONCURRENTLY` refreshes it without blocking readers.

#### What is TOAST?

The Oversized-Attribute Storage Technique: large values (over about 2 kB) are compressed and/or stored out of line in a separate table, transparently to queries.

#### What is a tablespace?

A directory on disk where PostgreSQL can store objects, letting you put some tables or indexes on different storage.

#### What is the system catalog?

Tables in `pg_catalog` (such as `pg_class`, `pg_attribute`, `pg_index`) describing every object, plus the standard `information_schema` views.

### Data types and DDL

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

#### What are arrays in PostgreSQL?

Any type can be an array: `text[]`, `integer[]`. Query them with `ANY`, `@>` (contains), `unnest()` to turn them into rows, and index them with GIN.

#### What are range types?

Types representing a range of values, such as `daterange`, `tstzrange`, `int4range`, with operators for overlap (`&&`) and containment (`@>`). They're useful for validity periods and bookings.

#### What is an enum type?

A type with a fixed, ordered list of values: `CREATE TYPE status AS ENUM ('active', 'closed')`. Adding values is easy, removing them is not, so lookup tables are often more flexible.

#### What are the main constraint types?

`NOT NULL`, `UNIQUE`, `PRIMARY KEY`, `FOREIGN KEY`, `CHECK` and `EXCLUDE` (for example, no two overlapping bookings for the same room).

#### What is a foreign key, and what do `ON DELETE` options do?

A constraint requiring that values in a column exist in a referenced table's key. `ON DELETE CASCADE` deletes child rows with the parent, `SET NULL` clears the reference, `RESTRICT` or `NO ACTION` block the delete.

#### Are foreign key columns indexed automatically?

No. PostgreSQL indexes the referenced (parent) key but not the referencing column. Index foreign key columns that are used in joins or that are checked during deletes on the parent.

#### What is a generated column?

A column computed from other columns: `total numeric GENERATED ALWAYS AS (price * qty) STORED`. PostgreSQL computes it on write.

#### What is a domain?

A data type with constraints attached, reusable across tables: `CREATE DOMAIN postcode_fr AS text CHECK (VALUE ~ '^\d{5}$')`.

#### How do you add a column to a large table safely?

`ALTER TABLE t ADD COLUMN c type` is instant, even with a constant default (since PostgreSQL 11). Volatile defaults, type changes that rewrite the table, and adding `NOT NULL` with a validation scan need more care and planning.

#### How do you add a constraint without locking the table for long?

Add it as `NOT VALID` (enforced for new rows only), then run `ALTER TABLE ... VALIDATE CONSTRAINT`, which takes a weaker lock while it checks existing rows.

#### What is a temporary table?

A table visible only to the current session and dropped at its end (or at commit with `ON COMMIT DROP`). It is useful for intermediate results.

#### What is an unlogged table?

A table whose changes aren't written to the WAL. Writes are much faster, but the table is emptied after a crash and isn't replicated. It is useful for staging data that can be reloaded.

#### What does `NULL` mean, and how does it behave in comparisons?

An unknown or missing value. Any comparison with `NULL` returns `NULL` (not true), so use `IS NULL` / `IS NOT NULL`, and `IS DISTINCT FROM` for null-safe comparisons.

#### What does `COALESCE` do?

It returns the first non-null argument: `COALESCE(nickname, first_name, 'unknown')`.

#### What is `NULLIF`?

`NULLIF(a, b)` returns `NULL` if `a = b`, otherwise `a`. It's handy to avoid division by zero: `x / NULLIF(y, 0)`.

### Querying: joins, subqueries and CTEs

#### What are the different join types?

`INNER JOIN` (matching rows only), `LEFT JOIN` (all left rows plus matches), `RIGHT JOIN`, `FULL OUTER JOIN` (all rows from both sides) and `CROSS JOIN` (every combination). There are also self-joins and `LATERAL` joins.

#### What is the difference between `WHERE` and `ON` in a left join?

A condition in `ON` decides which right-side rows match, and left rows are kept regardless. The same condition in `WHERE` filters the joined result, which can remove left rows and effectively turn the left join into an inner join.

#### What is a semi-join and an anti-join?

A semi-join returns rows of A that have a match in B (`WHERE EXISTS (...)`) without duplicating A. An anti-join returns rows of A with no match in B (`WHERE NOT EXISTS (...)` or a left join with `IS NULL`).

#### Why prefer `NOT EXISTS` over `NOT IN` with a subquery?

If the subquery returns any `NULL`, `NOT IN` returns no rows at all, because the comparison with `NULL` is unknown. `NOT EXISTS` behaves as expected and plans well as an anti-join.

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

#### What is a `LATERAL` join?

A join where the right-hand subquery can reference columns of tables to its left. It is used for "top-N per group":

```sql
SELECT c.name, o.*
FROM customer c
CROSS JOIN LATERAL (
    SELECT * FROM orders o WHERE o.customer_id = c.id ORDER BY created_at DESC LIMIT 3
) o;
```

#### What is the difference between `UNION` and `UNION ALL`?

`UNION` removes duplicates, which requires a sort or hash. `UNION ALL` keeps all rows and is faster. Use `UNION ALL` unless you need deduplication.

#### What do `INTERSECT` and `EXCEPT` do?

`INTERSECT` returns rows present in both queries, `EXCEPT` rows in the first but not the second, both without duplicates unless `ALL` is used.

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

#### How do you paginate efficiently?

`OFFSET` gets slower as the offset grows, because skipped rows are still read. Keyset pagination is faster: `WHERE (created_at, id) < ($1, $2) ORDER BY created_at DESC, id DESC LIMIT 50`, with an index on those columns.

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

#### What is `generate_series`?

A set-returning function that produces a series of numbers or timestamps, used to build calendars and fill gaps: `SELECT generate_series('2026-01-01'::date, '2026-12-31', interval '1 day')`.

### Aggregation and window functions

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

#### How do you pivot rows into columns?

With conditional aggregation:

```sql
SELECT country_code,
       sum(amount) FILTER (WHERE year = 2025) AS y2025,
       sum(amount) FILTER (WHERE year = 2026) AS y2026
FROM revenue GROUP BY country_code;
```

The `tablefunc` extension's `crosstab` is an alternative.

#### What does `string_agg` do?

It concatenates values with a separator, optionally ordered: `string_agg(name, ', ' ORDER BY name)`.

#### What is the `WINDOW` clause?

A way to name a window definition and reuse it in several functions: `... OVER w ... WINDOW w AS (PARTITION BY country ORDER BY day)`.

#### How do you compute year-over-year growth?

```sql
SELECT year, revenue,
       round(100.0 * (revenue - lag(revenue) OVER (ORDER BY year)) / lag(revenue) OVER (ORDER BY year), 1) AS yoy_pct
FROM yearly_revenue;
```

### Indexes

#### What are the different types of indexes available in PostgreSQL and when to use each one?

- **B-tree** (default): equality and range searches (`=`, `<`, `>`, `BETWEEN`, `ORDER BY`, prefix `LIKE 'abc%'`) on sortable data.
- **Hash:** equality only. Rarely better than B-tree, but small for long values.
- **GIN** (generalized inverted index): values that contain several components, such as arrays, JSONB and full-text search vectors, for "contains" queries.
- **GiST** (generalized search tree): geometric data, ranges, full-text search and nearest-neighbor searches (with PostGIS, for example).
- **SP-GiST:** space-partitioned data such as quadtrees, IP addresses or phone numbers.
- **BRIN** (block range index): very large tables whose values follow the physical order, such as an append-only timestamp column. Tiny and cheap to maintain.

#### How does a B-tree index work?

It's a balanced tree of sorted keys with pointers to table rows. Lookups take a few page reads (logarithmic time), and sorted order makes range scans and `ORDER BY` efficient.

#### What is a composite (multi-column) index, and does column order matter?

An index on several columns. Order matters: an index on `(country_code, created_on)` serves filters on `country_code` alone, or on both, but not efficiently on `created_on` alone. Put the equality columns first, then the range or sort column.

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

#### What are the costs of indexes?

They take disk space and slow down `INSERT`, `UPDATE` and `DELETE`, because each index must be maintained. Unused indexes are pure cost: find them with `pg_stat_user_indexes` (`idx_scan = 0`).

#### Why might PostgreSQL not use an index?

The query returns a large share of the table (a sequential scan is cheaper), statistics are outdated, a function or type cast is applied to the indexed column, the filter starts with a wildcard (`LIKE '%abc'`), the column order doesn't match a composite index, or the table is small.

#### How do you create an index without blocking writes?

`CREATE INDEX CONCURRENTLY`, which builds the index without holding a lock that blocks inserts and updates. It takes longer and can't run inside a transaction block. If it fails, it leaves an invalid index to drop.

#### What is a unique index, and how does it relate to a unique constraint?

An index that rejects duplicate keys. A `UNIQUE` constraint is implemented with a unique index. By default, several `NULL`s are allowed, unless the index is declared `NULLS NOT DISTINCT` (PostgreSQL 15+).

#### How do you index a JSONB column?

A GIN index on the whole column for containment and key-existence queries (`@>`, `?`), with `jsonb_path_ops` for a smaller index that only supports `@>`, or a B-tree expression index on one extracted key:

```sql
CREATE INDEX ON events USING gin (payload jsonb_path_ops);
CREATE INDEX ON events ((payload->>'user_id'));
```

#### How do you speed up `LIKE '%text%'` searches?

With a trigram index from the `pg_trgm` extension: `CREATE INDEX ON company USING gin (name gin_trgm_ops)`. It also speeds up similarity searches.

#### What is index bloat, and how do you fix it?

Indexes accumulate empty space after many updates and deletes. `REINDEX CONCURRENTLY` rebuilds them online. B-tree deduplication (PostgreSQL 13+) reduces bloat from duplicates.

#### When is a BRIN index the right choice?

For very large tables where a column correlates with physical order, such as a timestamp in an append-only log. A BRIN index stores min/max values per block range, so it is tiny and lets queries skip most blocks.

#### What is the difference between a clustered index in other databases and `CLUSTER` in PostgreSQL?

PostgreSQL has no permanently clustered tables. `CLUSTER` physically reorders a table once according to an index, but new rows aren't kept in order, so it must be repeated.

#### How do you find missing indexes?

Look for large sequential scans in `pg_stat_user_tables` (`seq_scan`, `seq_tup_read`), slow queries in `pg_stat_statements`, and sequential scans with selective filters in `EXPLAIN` plans.

#### Does an index on `(a, b)` make an index on `(a)` redundant?

Mostly yes: the composite index serves queries on `a` alone. A separate index on `a` may still be smaller and slightly faster, but usually isn't worth its maintenance cost.

#### What are GIN index `fastupdate` and pending lists?

GIN indexes buffer new entries in a pending list for faster inserts, merged into the main index later by vacuum or when the list is full. Large pending lists can slow searches.

#### How do you see the size of a table and its indexes?

```sql
SELECT pg_size_pretty(pg_total_relation_size('company')) AS total,
       pg_size_pretty(pg_relation_size('company'))       AS table_only,
       pg_size_pretty(pg_indexes_size('company'))        AS indexes;
```

### Transactions, MVCC and concurrency

#### What is a transaction in PostgreSQL?

A group of statements between `BEGIN` and `COMMIT` (or `ROLLBACK`) executed atomically. Each statement outside an explicit transaction runs in its own transaction (autocommit).

#### What is MVCC?

Multi-Version Concurrency Control: an `UPDATE` writes a new version of the row instead of overwriting it, and each transaction sees a snapshot of committed data. Readers don't block writers and writers don't block readers.

#### What are dead tuples?

Old row versions left by updates and deletes that no transaction can see any more. They take space until `VACUUM` reclaims it.

#### What are the transaction isolation levels in PostgreSQL?

- **Read Committed** (default): each statement sees data committed before it started.
- **Repeatable Read:** the whole transaction sees one snapshot, taken at its first statement. Concurrent conflicting updates cause serialization errors.
- **Serializable:** like Repeatable Read, plus detection of anomalies (serialisable snapshot isolation), so the result equals some serial order. Applications must retry on serialization failures.

Read Uncommitted is accepted but behaves like Read Committed.

#### What anomalies do isolation levels prevent?

Dirty reads (never possible in PostgreSQL), non-repeatable reads (prevented from Repeatable Read), phantom reads (also prevented by PostgreSQL's Repeatable Read) and serialization anomalies such as write skew (prevented only by Serializable).

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

#### What is a savepoint?

A point within a transaction you can roll back to without aborting the whole transaction: `SAVEPOINT s1; ... ROLLBACK TO SAVEPOINT s1;`.

#### Why are long-running transactions harmful?

They hold a snapshot, so vacuum can't remove dead tuples newer than it, causing bloat. They may also hold locks that block DDL and other writers. "Idle in transaction" sessions are a common culprit, limited with `idle_in_transaction_session_timeout`.

#### What is the lost update problem, and how do you prevent it?

Two transactions read a value, both modify it, and the second write overwrites the first. Prevent it with an atomic update (`SET qty = qty - 1`), `SELECT ... FOR UPDATE`, optimistic locking with a version column, or Repeatable Read with retries.

#### What is optimistic locking?

Detecting conflicts at write time instead of locking: each row has a version, and an update succeeds only if the version is unchanged (`UPDATE ... SET ..., version = version + 1 WHERE id = $1 AND version = $2`).

#### Which locks does DDL take, and why can `ALTER TABLE` block everything?

Many `ALTER TABLE` forms take an `ACCESS EXCLUSIVE` lock, which conflicts with every other lock, including reads. If it waits behind a long query, all new queries queue behind it. Use `lock_timeout` and retry.

#### What is transaction ID wraparound?

Transaction IDs are 32-bit and wrap around. Vacuum must "freeze" old rows before that happens, otherwise PostgreSQL stops accepting writes to protect data. Autovacuum runs anti-wraparound vacuums automatically, and monitoring `age(datfrozenxid)` catches problems early.

#### What does `VACUUM` do, and how is it different from `VACUUM FULL`?

`VACUUM` marks dead tuples' space as reusable, updates the visibility map and freezes old rows, without blocking reads or writes. `VACUUM FULL` rewrites the table to give space back to the operating system, but takes an exclusive lock. `pg_repack` does the same online.

#### What is autovacuum?

A background process that runs `VACUUM` and `ANALYZE` on tables when enough rows have changed, according to thresholds and scale factors that can be tuned per table.

#### What does `ANALYZE` do?

It samples tables and updates the statistics (`pg_statistic`) the planner uses to estimate row counts and choose plans.

#### What is HOT (heap-only tuple) update?

An optimization where an update that doesn't change indexed columns, and fits on the same page, creates the new version without updating indexes. A lower `fillfactor` leaves room for HOT updates on update-heavy tables.

#### What is the difference between `COMMIT` and `synchronous_commit = off`?

By default `COMMIT` waits until the WAL is flushed to disk, guaranteeing durability. With `synchronous_commit = off`, commits return sooner and a crash can lose the last few transactions, without corrupting data.

### Performance and query planning

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

#### What is `work_mem`, and why does it matter?

The memory each sort or hash operation may use before spilling to disk. Too low causes slow disk sorts. Too high risks running out of memory, because a single query can use several multiples of it.

#### What are the main memory settings to tune?

`shared_buffers` (PostgreSQL's cache, often about 25% of RAM), `effective_cache_size` (planner hint of total cache, often 50 to 75% of RAM), `work_mem` (per operation) and `maintenance_work_mem` (vacuum, index builds).

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

#### Why can a function on an indexed column prevent index use?

The index stores the column's raw values, so `WHERE date(created_at) = '2026-10-15'` can't use an index on `created_at`. Rewrite it as a range (`created_at >= '2026-10-15' AND created_at < '2026-10-16'`) or create an expression index.

#### What are extended statistics?

`CREATE STATISTICS` lets the planner learn correlations between columns (dependencies, distinct counts, most common value combinations), improving estimates for filters on several correlated columns such as city and postcode.

#### What does `default_statistics_target` control?

How many sample values and histogram buckets `ANALYZE` keeps per column. Raising it for skewed columns improves estimates at the cost of planning time.

#### How do you load large amounts of data quickly?

Use `COPY` instead of row-by-row inserts, load inside one transaction, create indexes and foreign keys after loading, consider unlogged staging tables, increase `maintenance_work_mem` for index builds, and run `ANALYZE` afterwards.

#### What is the `COPY` command?

The fastest way to bulk load or export data between tables and files or streams: `COPY company FROM '/data/company.csv' WITH (FORMAT csv, HEADER)`. From a client, use psql's `\copy` or the driver's COPY support. PostgreSQL 17 can skip malformed rows with `ON_ERROR ignore`.

#### What is connection pooling, and why is PgBouncer used?

Reusing a small number of database connections for many clients. PgBouncer sits between applications and PostgreSQL, in session, transaction or statement mode, cutting the per-connection overhead.

#### What is parallel query?

PostgreSQL can split sequential scans, joins and aggregations over several worker processes, controlled by `max_parallel_workers_per_gather` and table size.

#### What is JIT compilation in PostgreSQL?

Just-in-time compilation (with LLVM) of expressions in long analytical queries. It speeds up heavy computations but adds overhead to short queries. It is controlled by `jit` and cost thresholds.

#### How does `LIMIT` interact with `ORDER BY` and indexes?

With an index matching the `ORDER BY`, PostgreSQL reads only the first rows it needs. Without one, it must sort everything (a top-N heapsort) before applying the limit.

#### What is table bloat, and how do you detect it?

Wasted space from dead tuples that vacuum hasn't reclaimed or the operating system hasn't got back. Detect it with `pgstattuple`, bloat-estimation queries, or tables growing faster than their row count.

#### What would you check first when a query suddenly becomes slow?

Its plan (`EXPLAIN ANALYZE`) compared with before, statistics freshness (last analyze), data volume changes, locks and waits in `pg_stat_activity`, bloat, and whether parameters or a new index changed the plan.

### Data modeling, normalization and OLAP

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

#### What is Data Vault modeling?

A modeling method for integrating many sources with full history: hubs (business keys), links (relationships) and satellites (descriptive attributes with load dates). It favors auditability and parallel loading, and usually feeds star schemas for reporting.

#### When would you not use PostgreSQL for analytics?

When data reaches many terabytes or queries scan huge volumes routinely: columnar warehouses or lakehouses (Redshift, BigQuery, Snowflake, Databricks) scale better. Extensions such as Citus or columnar storage, or DuckDB for local analysis, can extend PostgreSQL's reach first.

#### What is the medallion architecture, and where does a relational database fit in it?

A lakehouse layering into bronze (raw), silver (cleaned and conformed) and gold (business-level aggregates and models). A relational database such as PostgreSQL is often a source system, or a serving layer for gold data used by applications.

### Administration, security, backup and replication

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

#### What is the difference between logical and physical backups?

Logical backups (`pg_dump`, `pg_dumpall`) export SQL or archive files of objects and data. They are portable across versions and can be restored selectively, but are slow for large databases. Physical backups (`pg_basebackup`, pgBackRest) copy the data files plus WAL. They are fast for large databases and allow point-in-time recovery.

#### How do you back up and restore a single database with pg_dump?

```bash
pg_dump -Fc -d mydb -f mydb.dump          # custom format, compressed
pg_restore -d newdb -j 4 mydb.dump        # parallel restore
```

#### What is point-in-time recovery (PITR)?

Restoring a base backup and replaying archived WAL up to a chosen moment, for example just before an accidental `DELETE`.

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

#### How do you upgrade PostgreSQL to a new major version?

With `pg_upgrade` (fast, in place, with `--link` or `--clone`), dump and restore (simple but slow), or logical replication to a new cluster for near-zero downtime.

#### What is high availability for PostgreSQL usually built with?

Streaming replication plus a failover manager such as Patroni (with etcd or Consul), or a managed service (Amazon RDS or Aurora, Cloud SQL, Azure Database for PostgreSQL) that handles failover.

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

### Advanced features

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

#### What is full-text search in PostgreSQL?

Searching documents with `tsvector` (normalized lexemes) and `tsquery`, with language-specific stemming, ranking (`ts_rank`) and GIN indexes:

```sql
SELECT * FROM article
WHERE to_tsvector('english', body) @@ websearch_to_tsquery('english', 'data pipeline');
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

#### What are extensions, and name some useful ones?

Packages that add features with `CREATE EXTENSION`: `pg_stat_statements` (query statistics), `pg_trgm` (similarity and trigram indexes), `postgis` (geospatial), `pgcrypto`, `uuid-ossp`, `postgres_fdw`, `pg_partman` (partition management), `pgvector` (vector similarity search), `timescaledb` (time series), `citus` (distribution).

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

#### What is PostGIS?

The spatial extension for PostgreSQL: geometry and geography types, spatial functions (distance, intersection, buffers), GiST indexes and coordinate system transformations. It's the standard open-source spatial database.

#### What is a foreign data wrapper (FDW)?

An extension that lets PostgreSQL query external data sources as if they were local tables: `postgres_fdw` (other PostgreSQL servers), `file_fdw` (files), and others for MySQL, Oracle, S3 or Parquet.

#### What is pgvector?

An extension adding a `vector` type and similarity search (cosine, L2, inner product) with HNSW and IVFFlat indexes. It's used to store embeddings for semantic search and retrieval-augmented generation.

#### What does `LISTEN` / `NOTIFY` do?

A built-in publish/subscribe mechanism: a session sends `NOTIFY channel, 'payload'` and every session that ran `LISTEN channel` receives it after commit. It's useful for lightweight cache invalidation or job wake-ups.

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
