## Snowflake Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Snowflake study guide: about 200 questions](../../images/snowflake_study_guide_title_img.png)

About 200 interview-style questions on Snowflake, from its architecture to virtual warehouses, micro-partitions, loading, semi-structured data, streams and tasks, dynamic tables, security, data sharing, performance and cost control. The answers reflect the platform as of 2026. Open a question to see its answer, or use the filter to search the whole guide.

<!-- QA -->

### Architecture

#### What is Snowflake?

A cloud data platform delivered as a fully managed service on AWS, Azure and Google Cloud. It started as a SQL data warehouse and now also covers data lakes (Iceberg tables), data engineering, data sharing, applications and AI. There is no hardware or software to install, tune or patch.

#### What are the three layers of Snowflake's architecture?

Database storage (data stored in compressed, columnar micro-partitions in cloud object storage), query processing (virtual warehouses: independent compute clusters), and cloud services (authentication, metadata, query optimization, access control, transactions and infrastructure management).

#### What does "separation of storage and compute" mean in Snowflake?

Data is stored once in central storage, and any number of virtual warehouses can read it independently. You scale and pay for compute and storage separately, and workloads (loading, BI, data science) don't compete for the same resources.

#### Why is Snowflake called a hybrid of shared-disk and shared-nothing?

Like shared-disk, all compute nodes see one central copy of the data. Like shared-nothing (MPP), each warehouse processes its part of the data on its own nodes with local caching, which gives scalable performance.

#### What is a virtual warehouse?

A named cluster of compute resources that executes queries and DML and loads data. It has a size, can be suspended and resumed, and consumes credits only while running.

#### What does the cloud services layer do?

It coordinates everything: authentication and access control, the metadata store (tables, micro-partition statistics, history), query parsing and optimization, transaction management, result caching and security. It is billed only if its usage exceeds 10% of the daily warehouse compute.

#### What is a Snowflake account and an organization?

An account is one Snowflake deployment in one cloud region, with its own users, databases and warehouses, reached through a URL. An organization groups several accounts of the same customer for billing, replication and account management (by ORGADMIN).

#### What is the object hierarchy in Snowflake?

Organization → account → database → schema → objects (tables, views, stages, file formats, sequences, streams, tasks, pipes, functions, procedures). Warehouses, users, roles, resource monitors and integrations are account-level objects.

#### What editions does Snowflake offer?

Standard; Enterprise (adds multi-cluster warehouses, Time Travel up to 90 days, materialized views, masking and row access policies, search optimization); Business Critical (adds stronger security and compliance such as HIPAA and PCI support, Tri-Secret Secure, private connectivity, failover); and Virtual Private Snowflake (a fully isolated environment).

#### What is a credit?

The unit for billing compute. A warehouse consumes credits per second (with a 60-second minimum each time it resumes) according to its size. Serverless features (Snowpipe, automatic clustering, search optimization, serverless tasks) also consume credits. Storage is billed separately per TB per month.

#### How do warehouse sizes relate to credits?

Each size step doubles the compute and the credit rate: X-Small uses 1 credit per hour, Small 2, Medium 4, Large 8, and so on up to 6X-Large. A query that parallelizes well runs about twice as fast on the next size, so the cost can stay similar while latency drops.

#### Which cloud providers and regions can you use?

AWS, Azure and Google Cloud, in many regions. An account lives in one region of one cloud; replication and data sharing across regions and clouds connect accounts.

#### How do you connect to Snowflake?

Through Snowsight (the web UI), the Snowflake CLI and SnowSQL, drivers (JDBC, ODBC, Python connector, Go, Node.js, .NET, Spark and Kafka connectors), the SQL REST API, and partner tools (BI, ETL, dbt).

#### What is Snowsight?

Snowflake's web interface for writing SQL and Python worksheets, notebooks, dashboards, exploring data, monitoring queries and costs, and administering the account.

#### What is Snowflake Horizon?

Snowflake's built-in governance and catalog capabilities: access control, classification of sensitive data, masking and row access policies, tags, lineage, data quality monitoring, auditing and discovery, applied across tables, Iceberg tables and shared data.

#### What is the difference between Snowflake and a traditional MPP warehouse such as Teradata or Redshift (provisioned)?

Traditional MPP warehouses couple storage and compute on the same nodes, so scaling means redistributing data, and all workloads share one cluster. Snowflake keeps storage central and lets you start independent warehouses in seconds, with no indexes, distribution keys or vacuuming to manage.

#### What is the role of the account URL and locator?

The account identifier (organization name plus account name, or the legacy locator with region) forms the URL that clients connect to, for example `myorg-myaccount.snowflakecomputing.com`.

#### What are contexts in a Snowflake session?

The current role, warehouse, database and schema of a session (`USE ROLE`, `USE WAREHOUSE`, `USE DATABASE`, `USE SCHEMA`). Queries run with the current role's privileges on the current warehouse, and unqualified names resolve against the current database and schema.

### Storage and micro-partitions

#### What is a micro-partition?

The physical storage unit of a Snowflake table: an immutable file of 50 to 500 MB of uncompressed data (much smaller compressed), stored in columnar format. Snowflake creates them automatically as data is loaded, in the order it arrives.

#### What metadata does Snowflake keep per micro-partition?

The range of values (min and max) of each column, the number of distinct values, null counts and other statistics. The optimizer uses them to skip micro-partitions that can't contain matching rows.

#### What is pruning?

Skipping micro-partitions during a scan because their metadata shows they can't match the filter. Good pruning is the main reason queries on huge tables can be fast. It appears in the query profile as "partitions scanned" versus "partitions total".

#### Why are micro-partitions immutable, and what does an update do?

Immutability makes concurrency, Time Travel and cloning simple. An `UPDATE` or `DELETE` writes new micro-partitions containing the changed rows and marks the old ones as no longer current; the old ones are kept for Time Travel and Fail-safe.

#### What is data clustering in Snowflake?

How well rows with similar values of a column are co-located in the same micro-partitions. Data loaded in date order is naturally well clustered by date. Clustering degrades when DML scatters values over many partitions.

#### What is a clustering key?

One or more columns or expressions declared on a large table (`CLUSTER BY (event_date, customer_id)`) so that the Automatic Clustering service reorganizes micro-partitions in the background to keep similar values together, improving pruning for filters on those columns.

#### When should you define a clustering key?

On very large tables (multi-terabyte) where queries filter on columns that are not naturally clustered and the query profile shows poor pruning. Clustering costs credits for reclustering, so it isn't worth it for small or frequently fully rewritten tables.

#### How do you check how well a table is clustered?

With `SYSTEM$CLUSTERING_INFORMATION('table', '(col)')`, which reports the average depth and overlap of micro-partitions. Lower depth means better clustering.

#### How is data compressed in Snowflake?

Automatically, per column, with the best encoding for the data. You don't choose compression; storage is billed on the compressed size.

#### What are the table types in Snowflake?

Permanent tables (Time Travel and 7-day Fail-safe), transient tables (Time Travel of 0 or 1 day, no Fail-safe, cheaper for data that can be rebuilt), temporary tables (exist only for the session), external tables (read files in a stage), Iceberg tables, hybrid tables (row-oriented, for transactional workloads) and dynamic tables.

#### What are Iceberg tables in Snowflake?

Tables stored in Apache Iceberg format in your own cloud storage (an external volume). With Snowflake as the catalog they behave almost like native tables; with an external catalog (AWS Glue, Snowflake Open Catalog/Apache Polaris and others) Snowflake can read and, in some cases, write them. Other engines (Spark, Trino) can work on the same data.

#### What are hybrid tables?

Tables optimized for low-latency, high-concurrency single-row reads and writes, with enforced primary keys and indexes, that can be joined with analytic tables in the same query. They target light transactional workloads (Unistore).

#### What is an external table?

A read-only table whose data stays in files in an external stage (S3, GCS, Azure). Snowflake stores file-level metadata, and you query the files with SQL. It's slower than native tables; Iceberg tables are usually preferred now.

#### How is storage billed?

On the average compressed bytes per month across tables, Time Travel and Fail-safe data, and staged files, at a rate per TB depending on capacity or on-demand pricing and region.

#### What does `ALTER TABLE … SUSPEND RECLUSTER` do?

It pauses automatic clustering on a table, stopping reclustering costs, for example during a large backfill; `RESUME RECLUSTER` turns it back on.

#### What is the difference between a column's natural clustering and a clustering key?

Natural clustering comes from the order in which data was loaded and costs nothing; a clustering key asks Snowflake to maintain an order through background reclustering, which costs credits but keeps pruning good despite DML.

#### How can you see how much storage Time Travel and Fail-safe use?

In `ACCOUNT_USAGE.TABLE_STORAGE_METRICS`, which reports active bytes, Time Travel bytes, Fail-safe bytes and bytes retained for clones per table.

### Virtual warehouses and compute

#### What happens when a warehouse is suspended?

It stops consuming credits and its local cache is dropped. With auto-resume, the next query starts it again in a second or two.

#### What are auto-suspend and auto-resume?

Settings that suspend a warehouse after a number of seconds of inactivity and resume it automatically when a query arrives. A short auto-suspend (for example 60 seconds) saves credits on intermittent workloads; a longer one keeps the cache warm for BI.

#### What is a multi-cluster warehouse?

An Enterprise feature where a warehouse can run several clusters of the same size, between a minimum and maximum, to absorb concurrency. Extra clusters start when queries queue and stop when load drops.

#### What is the difference between scaling up and scaling out?

Scaling up (a bigger warehouse) makes individual complex queries faster and reduces spilling. Scaling out (more clusters in a multi-cluster warehouse) serves more concurrent users without queuing; it doesn't make a single query faster.

#### What are the multi-cluster scaling policies?

Standard (starts clusters quickly to avoid queuing, favoring performance) and Economy (starts a cluster only if there's enough load to keep it busy for several minutes, favoring cost).

#### How do you separate workloads in Snowflake?

With different warehouses per workload (ingestion, transformation, BI, data science, ad hoc), each sized and suspended appropriately, so they never compete for compute and their costs are visible separately.

#### What is query queuing, and how do you reduce it?

Queries wait when a warehouse is at its concurrency limit (`MAX_CONCURRENCY_LEVEL`, 8 by default). Fixes: multi-cluster warehouses, separate warehouses for different workloads, faster queries, or a larger warehouse.

#### What is a Snowpark-optimized warehouse?

A warehouse with much more memory per node, for memory-heavy Snowpark workloads such as ML training or large UDF processing.

#### What is the Query Acceleration Service?

A serverless feature that offloads parts of large scans and filters in eligible queries to shared compute, so outlier queries finish faster without resizing the whole warehouse. It's enabled per warehouse with a scale factor limit.

#### What are Gen2 standard warehouses?

A newer generation of standard warehouses with faster hardware and engine improvements, especially for DML and large scans, billed at a somewhat higher credit rate. They can be chosen per warehouse.

#### What is the statement timeout?

`STATEMENT_TIMEOUT_IN_SECONDS`, set on a warehouse, user or session, cancels queries running longer than the limit. Setting it prevents runaway queries from burning credits for hours.

#### Can a running query use a warehouse that was resized?

Resizing affects new queries; running queries finish on the existing resources. Scaling up provisions new resources in the background, so queued and new queries benefit once they're ready.

#### What does `MAX_CONCURRENCY_LEVEL` control?

The number of concurrent SQL statements a warehouse cluster runs before queuing more. Lowering it gives each query more resources; raising it allows more parallel queries at the risk of slowing each one.

#### How do you choose an initial warehouse size?

Start small (X-Small or Small) for development and simple loads, test representative queries, and size up only when queries spill, run too long, or don't meet the target time. Measure cost per run, not just duration.

### Caching

#### What caches does Snowflake have?

The result cache (in the cloud services layer: query results reused for 24 hours if the query and data haven't changed), the warehouse (local disk) cache (micro-partition data cached on the warehouse's SSD while it runs), and the metadata cache (statistics that answer some queries like `COUNT(*)` or `MIN` without a warehouse).

#### When is the result cache used?

When the same query text runs again, the underlying data hasn't changed, the user has the required privileges, and the query doesn't use non-deterministic functions such as `CURRENT_TIMESTAMP()`. Each reuse extends retention, up to 31 days. It costs no compute.

#### How does the warehouse cache affect auto-suspend decisions?

Suspending drops the local cache, so the next queries read from remote storage and are slower. For dashboards that query the same data repeatedly, a longer auto-suspend can be faster and not much more expensive.

#### How do you disable the result cache for testing?

`ALTER SESSION SET USE_CACHED_RESULT = FALSE;` so benchmark queries actually run.

#### Does the result cache work across users?

Yes, if the other user's role has the required privileges on the underlying objects and the query text is identical; results are not tied to the original user.

#### Why might a repeated query not hit the result cache?

The data changed, the query text differs (even by whitespace or case in some cases), it uses non-deterministic functions, it queries external functions or some table functions, the result is older than its retention, or caching is disabled for the session.

### Loading data

#### What are the ways to load data into Snowflake?

Bulk loading with `COPY INTO` from stages, continuous loading with Snowpipe (files) and Snowpipe Streaming (rows), the Kafka connector, Openflow and partner ETL/ELT tools, `INSERT` statements, external and Iceberg tables for querying in place, and data sharing for data from other accounts.

#### What is a stage?

A location for files to load or unload. Internal stages are inside Snowflake: user stages (`@~`), table stages (`@%table`) and named stages. External stages point to S3, GCS or Azure containers, usually through a storage integration.

#### What is a storage integration?

An account object that holds a cloud identity (for AWS, an IAM role that Snowflake assumes) and the allowed storage locations, so external stages access buckets without storing credentials in SQL.

```sql
CREATE STORAGE INTEGRATION s3_lake
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/snowflake-lake'
  STORAGE_ALLOWED_LOCATIONS = ('s3://my-lake/raw/');

CREATE STAGE raw_stage URL = 's3://my-lake/raw/' STORAGE_INTEGRATION = s3_lake;
```

#### What is a file format object?

A named definition of how to parse files: type (CSV, JSON, Avro, ORC, Parquet, XML), delimiters, header handling, null strings, compression, date formats. Stages and `COPY` statements reference it.

#### How does `COPY INTO <table>` work?

It loads files from a stage into a table in parallel, using a file format, with options for error handling and transformations in a `SELECT`. It keeps 64 days of load metadata per table, so files already loaded are skipped by default.

```sql
COPY INTO raw.orders
FROM @raw_stage/orders/
FILE_FORMAT = (TYPE = 'PARQUET')
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
ON_ERROR = 'ABORT_STATEMENT';
```

#### What `ON_ERROR` options exist for `COPY`?

`ABORT_STATEMENT` (default for bulk loads), `CONTINUE` (skip bad rows), `SKIP_FILE`, `SKIP_FILE_<n>` or `SKIP_FILE_<n>%` (skip a file with too many errors). Use `VALIDATION_MODE = RETURN_ERRORS` to test a load without loading, and the `VALIDATE` function to see errors from a previous load.

#### What is the ideal file size for loading?

Roughly 100–250 MB compressed per file. Many tiny files add overhead; a single huge file can't be loaded in parallel. Split large files and batch small ones.

#### What is Snowpipe?

A serverless service that loads files continuously as they arrive in a stage, using a `COPY` statement defined in a pipe. With auto-ingest, cloud event notifications (S3 events via SQS, Event Grid, Pub/Sub) trigger it; otherwise you call its REST API. Latency is typically around a minute.

```sql
CREATE PIPE raw.orders_pipe AUTO_INGEST = TRUE AS
COPY INTO raw.orders FROM @raw_stage/orders/ FILE_FORMAT = (TYPE = 'JSON');
```

#### How is Snowpipe billed, and why do file sizes matter?

On serverless compute plus a small per-file overhead (in recent pricing, a fixed amount per GB ingested). Very small files make the overhead dominate, so producers should batch data into files of reasonable size, ideally sent every minute or so rather than per event.

#### What is Snowpipe Streaming?

An API (through the Java or Python SDK, the Kafka connector or Openflow) that writes rows directly into tables with seconds of latency, without staging files. It suits event streams; its high-performance architecture bills by data volume.

#### How do you unload data from Snowflake?

With `COPY INTO @stage/path/ FROM (SELECT ...)`, writing CSV, JSON or Parquet files to an internal or external stage, with options for partitioning (`PARTITION BY`), file size and headers. Then `GET` downloads files from internal stages.

#### What are `PUT` and `GET`?

Client commands (SnowSQL, CLI, drivers) to upload local files to an internal stage (`PUT`, which compresses and encrypts them) and download files from it (`GET`).

#### What is schema detection with `INFER_SCHEMA`?

A function that reads staged Parquet, Avro, ORC, JSON or CSV files and returns column names and types; combined with `CREATE TABLE … USING TEMPLATE`, it creates a table from files' structure. Tables can also enable schema evolution so new columns are added during loads.

#### What is the `FORCE` option of `COPY`?

`FORCE = TRUE` loads files again even if the load metadata says they were already loaded, which can create duplicates; it's used deliberately for reloads after truncating a table.

#### How does `COPY` handle files older than 64 days?

Load metadata expires after 64 days, so for older files Snowflake may not know whether they were loaded. `LOAD_UNCERTAIN_FILES = TRUE` loads them anyway; to avoid ambiguity, move or delete files once loaded, or use Snowpipe, which keeps 14 days of history per pipe.

#### How can you transform data during `COPY`?

With a `SELECT` over the staged files in the `COPY` statement: reorder or omit columns, cast types, use `$1`, `$2` positions or `$1:field` for semi-structured data, and add `METADATA$FILENAME` or `METADATA$FILE_ROW_NUMBER` for lineage.

#### How do you query staged files without loading them?

`SELECT $1, $2, METADATA$FILENAME FROM @stage/path (FILE_FORMAT => 'my_csv')`, which is useful to inspect files before loading.

#### What is Openflow?

Snowflake's managed data integration service, based on Apache NiFi, with connectors for databases, SaaS apps and streams, deployed in Snowflake or in your own cloud (bring your own cloud), to ingest structured and unstructured data.

#### How do you load from a relational database with CDC into Snowflake?

With a CDC tool (Openflow connectors, Debezium with Kafka and the Snowflake Kafka connector, Fivetran, AWS DMS writing to S3 plus Snowpipe) landing change events in raw tables, then a `MERGE` from a stream or a dynamic table to apply them to the current-state table.

### Semi-structured data

#### What is the `VARIANT` data type?

A type that can hold any JSON-like value (object, array, string, number, boolean, null) up to a size limit. Snowflake stores frequently present keys in columnar form internally, so queries on them can still prune and run fast.

#### How do you query JSON stored in a `VARIANT`?

With path notation and casts:

```sql
SELECT payload:customer.id::NUMBER       AS customer_id,
       payload:items[0]:sku::STRING       AS first_sku
FROM raw.events
WHERE payload:type::STRING = 'purchase';
```

#### What does `FLATTEN` do?

A table function that expands an array or object into one row per element, used with `LATERAL` to unnest nested data.

```sql
SELECT e.payload:order_id::STRING AS order_id, i.value:sku::STRING AS sku
FROM raw.events e, LATERAL FLATTEN(input => e.payload:items) i;
```

#### What are `OBJECT` and `ARRAY` types?

Semi-structured types for key-value objects and arrays. Functions like `OBJECT_CONSTRUCT`, `ARRAY_AGG`, `ARRAY_CONTAINS` and `PARSE_JSON` build and inspect them. Structured versions (`OBJECT(name STRING, age NUMBER)`, `ARRAY(NUMBER)`) enforce element types.

#### Should you keep JSON as `VARIANT` or flatten it into columns?

Keep raw JSON in `VARIANT` in the landing layer for flexibility and auditability, then extract the fields that are queried often into typed columns in clean layers: typed columns are easier to use, document and govern, and they prune predictably.

#### How do you handle a JSON field that sometimes is a string and sometimes a number?

Cast defensively with `TRY_CAST` or `TRY_TO_NUMBER`, which return `NULL` instead of failing, and check the type with `TYPEOF()` to quarantine unexpected values.

#### How do you convert relational rows into JSON?

With `OBJECT_CONSTRUCT(*)` or `OBJECT_CONSTRUCT('id', id, 'name', name)` for each row, and `ARRAY_AGG` to group rows into arrays, useful for exporting nested documents or feeding APIs.

#### How is a missing key different from a JSON null?

A missing key returns SQL `NULL`; a JSON `null` value is a `VARIANT` null, which is not the same as SQL `NULL` (`IS_NULL_VALUE()` tests it). Casting with `::STRING` turns JSON null into SQL `NULL`.

#### How do you load Parquet columns directly into table columns?

With `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE` in `COPY`, which maps file columns to table columns by name, or by selecting `$1:column_name::type` explicitly.

### SQL features

#### What is `QUALIFY`?

A clause that filters on window function results, like `HAVING` for aggregates. It's the idiomatic way to deduplicate:

```sql
SELECT *
FROM raw.customers
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1;
```

#### What does `MERGE` do in Snowflake?

It inserts, updates or deletes rows in a target table based on a join with a source, in one atomic statement, typically used for upserts and CDC.

```sql
MERGE INTO dw.customers t
USING staging.customers s ON t.customer_id = s.customer_id
WHEN MATCHED AND s.is_deleted THEN DELETE
WHEN MATCHED THEN UPDATE SET t.email = s.email, t.updated_at = s.updated_at
WHEN NOT MATCHED THEN INSERT (customer_id, email, updated_at)
  VALUES (s.customer_id, s.email, s.updated_at);
```

#### Does Snowflake enforce primary and foreign keys?

On standard tables, only `NOT NULL` is enforced. Primary, unique and foreign key constraints are informational: they document the model and can help BI tools and the optimizer (with `RELY`), but they don't prevent duplicates. Hybrid tables do enforce them.

#### What are sequences and identity columns?

Sequences generate unique numbers (`seq.NEXTVAL`), not necessarily gap-free. `AUTOINCREMENT`/`IDENTITY` columns use a sequence internally. Many warehouse designs prefer hash-based surrogate keys, which are deterministic across loads.

#### What is `SAMPLE` used for?

Reading a random fraction of a table (`SELECT * FROM t SAMPLE (1)` for 1% of rows, or `SAMPLE BLOCK` for micro-partitions), which is useful for quick exploration and testing on big tables.

#### What are user-defined functions in Snowflake?

Scalar or table functions written in SQL, JavaScript, Python, Java or Scala. Python UDFs run in a secure sandbox with packages from Anaconda or uploaded files. Vectorized Python UDFs process batches with pandas for better performance.

#### What are stored procedures in Snowflake?

Procedures written in Snowflake Scripting (SQL), JavaScript, Python, Java or Scala, used for procedural logic and administration. They run with owner's rights (default) or caller's rights.

#### What is Snowflake Scripting?

A procedural SQL extension with variables, `IF`, loops, cursors, exception handling and `RETURN`, usable in stored procedures and anonymous blocks.

#### What are transactions like in Snowflake?

ACID with the read committed isolation level. Each statement autocommits unless inside an explicit `BEGIN … COMMIT`. DDL commits implicitly. Concurrent DML on the same table can be blocked by locks until the other transaction finishes.

#### What does `UNDROP` do?

It restores a recently dropped table, schema or database from Time Travel, as long as it is within the retention period.

#### What does `SWAP WITH` do?

`ALTER TABLE a SWAP WITH b` exchanges two tables' names atomically, a common way to publish a rebuilt table without downtime for readers.

#### What is `CREATE OR ALTER`?

A statement that creates an object if it doesn't exist or alters it to match the definition if it does, keeping data and grants, useful for declarative deployments of tables and other objects.

#### What are `PIVOT` and `UNPIVOT` used for?

Rotating rows into columns (for example months into columns) and columns back into rows. `PIVOT` supports dynamic value lists with `ANY` in recent versions.

#### What does `MATCH_RECOGNIZE` do?

Pattern matching over ordered rows (for example a sequence of events in a session, such as view → cart → purchase), returning matches with measures, without writing complex self-joins.

### Time Travel, Fail-safe and cloning

#### What is Time Travel?

Access to historical data that was changed or deleted, for a retention period: 1 day by default, configurable up to 90 days on Enterprise for permanent tables. You can query, clone or restore data as of a time, an offset or a statement.

```sql
SELECT * FROM orders AT (OFFSET => -3600);
SELECT * FROM orders BEFORE (STATEMENT => '01b2c3d4-...');
CREATE TABLE orders_restored CLONE orders AT (TIMESTAMP => '2026-10-15 08:00'::TIMESTAMP_LTZ);
```

#### What is Fail-safe?

A 7-day period after Time Travel during which Snowflake can recover permanent table data for disaster recovery. Only Snowflake support can access it; you can't query it. It costs storage, which is why transient tables (no Fail-safe) are cheaper.

#### How do you set Time Travel retention?

With `DATA_RETENTION_TIME_IN_DAYS` at the account, database, schema or table level. Long retention on tables with frequent updates increases storage costs considerably.

#### What is zero-copy cloning?

Creating a copy of a table, schema or database instantly with `CLONE`, without copying data: the clone shares the original's micro-partitions and only new changes consume storage. It's used for dev and test environments, backups before risky changes, and point-in-time snapshots.

#### What does a clone inherit?

The data and structure, and for databases and schemas the child objects. Privileges on the source object itself are not copied unless you use `COPY GRANTS`; privileges on child objects are cloned. Pipes referencing internal stages, and some other objects, are not cloned.

#### How would you give a developer a full copy of production data cheaply?

Clone the production database into a dev database (instantly, with no extra storage until changes are made), apply masking policies or a secure view layer if the data is sensitive, and give the developer a role on the clone.

#### What happens to Time Travel when you drop and recreate a table with the same name?

The new table is separate; the dropped one stays in Time Travel and can be restored with `UNDROP` only after renaming the new table, since names must be unique.

#### Can you clone from a point in time?

Yes: `CREATE TABLE t_clone CLONE t AT (TIMESTAMP => ...)` or `BEFORE (STATEMENT => ...)`, as long as it's within the retention period. It is a common way to recover from a bad change while keeping the current table for comparison.

### Streams, tasks and dynamic tables

#### What is a stream?

An object that records the changes (inserts, updates, deletes) made to a table, view or external table since the stream was last consumed, exposing them with the columns `METADATA$ACTION`, `METADATA$ISUPDATE` and `METADATA$ROW_ID`. Consuming it in a DML transaction advances its offset.

#### What types of streams exist?

Standard (all changes, net of each other), append-only (only inserts, cheaper, for tables with insert-only loads), and insert-only for external and Iceberg tables.

#### What is a task?

A scheduled or triggered unit that runs a SQL statement, a stored procedure call or Snowflake Scripting, using a warehouse or serverless compute. Tasks can be chained into DAGs with `AFTER` and can run only when a stream has data with `WHEN SYSTEM$STREAM_HAS_DATA(...)`.

```sql
CREATE TASK load_orders
  WAREHOUSE = transform_wh
  SCHEDULE = '15 MINUTE'
  WHEN SYSTEM$STREAM_HAS_DATA('raw.orders_stream')
AS
  INSERT INTO dw.orders SELECT * FROM raw.orders_stream WHERE METADATA$ACTION = 'INSERT';

ALTER TASK load_orders RESUME;
```

#### What is a serverless task?

A task with no warehouse specified, where Snowflake manages compute size based on previous runs. It suits small, frequent tasks, because there is no warehouse minimum billing.

#### What is a triggered task?

A task with no schedule that runs when its stream has new data, reacting quickly to changes without polling on a fixed interval.

#### What is a dynamic table?

A table defined by a query and a target lag (`TARGET_LAG = '10 minutes'`), which Snowflake keeps refreshed automatically, incrementally when possible. It replaces many stream-and-task pipelines with declarative SQL.

```sql
CREATE DYNAMIC TABLE dw.daily_sales
  TARGET_LAG = '30 minutes'
  WAREHOUSE = transform_wh
AS
SELECT order_date, SUM(amount) AS sales FROM dw.orders GROUP BY order_date;
```

#### Dynamic tables, materialized views or streams and tasks: how do you choose?

Dynamic tables for declarative pipelines with joins and aggregations at a chosen freshness. Materialized views for speeding up repeated queries on a single table (no joins), always current. Streams and tasks for procedural logic, custom `MERGE` handling or side effects.

#### What is the difference between incremental and full refresh in dynamic tables?

Incremental refresh processes only changes in sources since the last refresh; full refresh recomputes the whole query. Snowflake chooses incremental when the query supports it; some constructs (certain non-deterministic functions, some window patterns) force full refreshes, which cost more.

#### What is a materialized view in Snowflake?

A precomputed result of a query on one table, maintained automatically and transparently by a background service (Enterprise). The optimizer can use it even when you query the base table. Maintenance costs credits, so use it for expensive, frequent queries on slowly changing tables.

#### What happens to a stream if it isn't consumed for a long time?

It can become stale when its offset falls outside the source table's data retention period (Snowflake extends retention up to 14 days to prevent this for tables with streams). A stale stream must be recreated, and changes may need a full reload.

#### How do you monitor tasks?

With `TASK_HISTORY` (information schema table function and account usage view), the task graph view in Snowsight, error notifications through a notification integration, and `SYSTEM$TASK_DEPENDENTS_ENABLE` to resume whole graphs.

#### What is a finalizer task?

A task attached to the root of a task graph that runs after all other tasks finish, whether they succeeded or failed, for cleanup or notifications.

#### Can dynamic tables be chained?

Yes. A dynamic table can read other dynamic tables, forming a pipeline; `TARGET_LAG = DOWNSTREAM` means a table refreshes only as needed by the tables that depend on it.

### Security and access control

#### How does access control work in Snowflake?

Through role-based access control (RBAC) combined with discretionary access control: privileges are granted to roles, roles are granted to users and other roles, and each object has an owner role that controls it.

#### What are the system-defined roles?

ORGADMIN (organization), ACCOUNTADMIN (top account role; use sparingly), SECURITYADMIN (manages grants and can manage users and roles), USERADMIN (creates users and roles), SYSADMIN (creates warehouses and databases; custom roles should roll up to it) and PUBLIC (granted to everyone).

#### What is a good role hierarchy?

Access roles holding privileges on objects (for example `SALES_READ`, `SALES_WRITE`), functional roles representing jobs or teams (`ANALYST`, `DATA_ENGINEER`) that are granted access roles, and functional roles rolled up to SYSADMIN so administrators can manage everything. Service accounts get their own functional roles.

#### What are future grants?

Grants that apply automatically to objects created later in a schema or database: `GRANT SELECT ON FUTURE TABLES IN SCHEMA sales.marts TO ROLE sales_read;`. They avoid missing grants on new tables.

#### What are database roles?

Roles scoped to a database, used to manage access inside it and especially to share fine-grained access through data sharing.

#### What are managed access schemas?

Schemas where only the schema owner (or roles with `MANAGE GRANTS`) can grant privileges on objects, not the object owners, which centralizes access control.

#### What is a masking policy?

A schema-level object that rewrites a column's value at query time depending on the context, typically the role: analysts see `***@***` while a privileged role sees the real email. It's attached to columns directly or via tags (Enterprise).

```sql
CREATE MASKING POLICY mask_email AS (val STRING) RETURNS STRING ->
  CASE WHEN IS_ROLE_IN_SESSION('PII_READER') THEN val ELSE '***MASKED***' END;

ALTER TABLE crm.customers MODIFY COLUMN email SET MASKING POLICY mask_email;
```

#### What is a row access policy?

A policy that returns whether a row is visible for the current context, attached to a table or view, often using a mapping table of roles to allowed regions. It filters rows transparently for every query.

#### What is tag-based masking?

Attaching a masking policy to a tag, so every column with that tag (for example `pii = 'email'`) is masked automatically, including new columns as soon as they are tagged.

#### What is data classification?

A feature that analyzes columns to detect sensitive data (emails, names, phone numbers, national IDs) and suggests or applies system tags, which can then drive masking policies.

#### How do users authenticate to Snowflake?

With passwords plus MFA (which Snowflake is making mandatory for password sign-ins), SSO through SAML 2.0 identity providers (Okta, Entra ID), OAuth (Snowflake or external), key-pair authentication for services, workload identity federation, and programmatic access tokens. Service users should use key pairs or OAuth, not passwords.

#### What are network policies?

Rules that allow or block client IP addresses (and network rules for private endpoints) at account or user level, so only corporate networks or specific services can connect.

#### How is data encrypted in Snowflake?

Always at rest (AES-256) and in transit (TLS), with a hierarchical key model and automatic key rotation. Business Critical adds Tri-Secret Secure, combining a customer-managed key with Snowflake's key.

#### What are secure views and secure UDFs?

Views and functions whose definition is hidden from non-owners and that disable some optimizations that could leak data through query behavior. They are required for objects in data shares.

#### What is the access history view used for?

`SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY` records which columns each query read and wrote, which helps auditing, lineage and finding unused data.

#### What is the difference between `OWNERSHIP` and other privileges?

The role owning an object has full control, including granting privileges on it and dropping it. Other privileges (`SELECT`, `INSERT`, `USAGE`, `MONITOR`, `OPERATE`) allow specific actions. Ownership can be transferred with `GRANT OWNERSHIP`.

#### Why shouldn't ACCOUNTADMIN be the default role for anyone?

It has unrestricted power, so mistakes or compromised sessions are catastrophic. Grant it to a few administrators with MFA, never use it for daily work or service accounts, and create objects with SYSADMIN or custom roles.

#### What are secondary roles?

`USE SECONDARY ROLES ALL` lets a session use the privileges of all granted roles for queries (the primary role still owns created objects), which simplifies work for users with several roles.

#### What are external access integrations?

Objects that allow UDFs and procedures to call external network endpoints, controlled by network rules listing allowed hosts and secrets objects for credentials.

### Data sharing and collaboration

#### What is Secure Data Sharing?

Sharing live, read-only data from one account with another without copying it: the provider creates a share containing databases, schemas, tables and secure views, and the consumer creates a database from it. The consumer pays for the compute it uses; the provider pays for storage.

#### Can you share with someone who doesn't have a Snowflake account?

Yes, through a reader account that the provider creates and pays for, with limited capabilities.

#### How does sharing work across regions or clouds?

Data must be replicated to an account in the consumer's region, or shared through listings with cross-cloud auto-fulfillment, which replicates the data automatically.

#### What is the Snowflake Marketplace?

A catalog of listings where providers publish free or paid datasets, data services and Native Apps that consumers can get into their accounts directly.

#### What are data clean rooms?

Environments where several parties combine data for analysis (for example audience overlap) under policies that allow only approved queries and aggregated outputs, without exposing raw records to each other.

#### What is a Native App?

An application packaged with code and data that a provider distributes through the Marketplace and that runs inside the consumer's account, so the consumer's data doesn't leave it.

#### What can't you do with shared data as a consumer?

You can't modify it, clone it or re-share it (except through specific provider settings), and Time Travel isn't available on shared objects. You can query it, join it with your data and create views over it.

#### What is a listing?

A packaged offering of a share or Native App with metadata, terms and usage analytics, published privately to chosen accounts or publicly on the Marketplace.

### Snowpark, Python and AI

#### What is Snowpark?

A set of libraries and runtimes for processing data in Snowflake with Python, Java or Scala. DataFrame operations are translated to SQL and executed in a warehouse, so data doesn't leave Snowflake.

```python
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, sum as sum_

session = Session.builder.configs(connection_params).create()
daily = (session.table("dw.orders")
         .filter(col("status") == "paid")
         .group_by("order_date")
         .agg(sum_("amount").alias("sales")))
daily.write.save_as_table("dw.daily_sales", mode="overwrite")
```

#### What is the pandas on Snowflake API?

A pandas-compatible API (Snowpark pandas, through Modin) that runs pandas code on Snowflake compute, so familiar pandas syntax scales to large tables.

#### What are Snowflake Notebooks?

Notebooks in Snowsight that mix SQL, Python and Markdown cells and run on a warehouse or on container compute, for exploration, data engineering and ML.

#### What is Snowpark Container Services?

A managed container runtime in Snowflake for running any containerized app, service or ML model (including GPUs) next to the data, governed by Snowflake's security.

#### What is Snowflake Cortex?

Snowflake's AI layer: LLM functions callable from SQL (`AI_COMPLETE`, `AI_CLASSIFY`, `AI_EXTRACT`, `AI_SENTIMENT`, summarization, translation), Cortex Search for retrieval, Cortex Analyst for natural-language questions over semantic models, and agents.

#### What is Streamlit in Snowflake?

A way to build and host Streamlit data apps directly in Snowflake, running with the account's governance and sharing them through roles.

#### What is the Snowflake ML ecosystem?

Snowflake ML includes a feature store, model registry, distributed training and inference on warehouses or containers, and ML observability, so models are built and served where the data is.

#### When would you use Snowpark instead of SQL?

For logic that's easier in Python (complex string or business rules, ML feature engineering, reuse of Python libraries), for unit-testable transformation code, or for teams more comfortable with DataFrames. For straightforward transformations, SQL is often simpler and as fast.

#### How do Python packages get into Snowflake?

From the Snowflake Anaconda channel (listed in `PACKAGES`), from wheels or zip files uploaded to a stage (`IMPORTS`), or through artifact repositories that pull from PyPI.

### Performance

#### How do you find out why a query is slow?

Open the Query Profile: look at the most expensive operators, partitions scanned versus total (pruning), bytes spilled to local and remote storage, exploding joins (output rows much greater than input), and queuing time. `GET_QUERY_OPERATOR_STATS` gives the same data in SQL.

#### What is spilling, and how do you fix it?

When a warehouse doesn't have enough memory for an operation, it spills to local disk and then to remote storage, which is much slower. Fix it with a larger warehouse, by processing less data (better filters, pre-aggregation), or by splitting the query.

#### What causes an "exploding join"?

A join on a non-unique key, or missing join conditions, so each row matches many rows and the output multiplies. Check join keys for uniqueness and that every join has the full condition.

#### How do you improve pruning?

Filter on columns that correlate with load order (dates), add a clustering key on large tables filtered by other columns, avoid wrapping filter columns in functions that prevent pruning, and filter as early as possible.

#### What is the Search Optimization Service?

An Enterprise feature that builds a persistent search access path for a table so point lookups and selective filters (equality, `IN`, substring and regex searches, `VARIANT` fields, geo) can skip most micro-partitions. It costs storage and maintenance credits.

#### Why avoid `SELECT *` in Snowflake?

Storage is columnar, so reading only needed columns scans far less data. `SELECT *` on wide tables reads every column and slows queries and BI extracts.

#### How do you make many small `INSERT` statements faster?

Don't: Snowflake is optimized for set-based operations. Batch rows into files and use `COPY`, use Snowpipe Streaming for continuous rows, or insert in large multi-row statements.

#### Is `ORDER BY` in a `CREATE TABLE AS` useful?

Yes, on initial loads of big tables: sorting by the main filter columns produces well-clustered micro-partitions from the start, improving pruning without paying for automatic clustering.

#### What are common mistakes that make Snowflake slow?

Single-row DML in loops, `SELECT *`, functions on filter columns, joins on mismatched types, huge `IN` lists, too-small warehouses that spill, too-large warehouses for trivial queries (cost), and complex views stacked many levels deep.

#### What does `EXPLAIN` show in Snowflake?

The logical plan of a query without running it: operators, join order and partitions to be scanned (from metadata), useful to check pruning before running an expensive query.

#### How do you speed up a query using `DISTINCT` on huge data?

Check if deduplication is really needed (often a join fanned out), deduplicate earlier on fewer columns, use `APPROX_COUNT_DISTINCT` (HyperLogLog) when an estimate is enough, and use a larger warehouse if it spills.

#### What are approximate functions useful for?

`APPROX_COUNT_DISTINCT`, `APPROX_PERCENTILE` and `APPROX_TOP_K` give estimates with small error using far less memory and time, which suits dashboards and exploration on very large tables.

### Cost management

#### What drives Snowflake costs?

Warehouse compute (by far the largest for most customers), serverless features (Snowpipe, clustering, materialized views, search optimization, tasks, AI functions), storage (including Time Travel and Fail-safe), cloud services above 10% of compute, and data transfer out of the region.

#### What is a resource monitor?

An object that tracks credit usage for warehouses or the account over a period and can notify, suspend after running queries finish, or suspend immediately when thresholds are reached.

```sql
CREATE RESOURCE MONITOR monthly_bi WITH CREDIT_QUOTA = 500
  FREQUENCY = MONTHLY START_TIMESTAMP = IMMEDIATELY
  TRIGGERS ON 80 PERCENT DO NOTIFY
           ON 100 PERCENT DO SUSPEND;
ALTER WAREHOUSE bi_wh SET RESOURCE_MONITOR = monthly_bi;
```

#### How do you see where credits go?

With `SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY`, `QUERY_HISTORY` (with `QUERY_ATTRIBUTION_HISTORY` for per-query cost), `METERING_DAILY_HISTORY` for serverless features, the cost management pages in Snowsight, budgets, and object tags or query tags for attribution.

#### What are query tags?

A session parameter (`ALTER SESSION SET QUERY_TAG = 'dbt:daily_sales'`) stored with each query in the history, used to attribute costs and find queries by job, tool or team.

#### What are budgets in Snowflake?

Spending limits for the account or for groups of objects, with notifications when projected spend exceeds the limit, helping teams keep track of serverless and warehouse costs.

#### How do you reduce warehouse costs?

Right-size warehouses per workload, use short auto-suspend, avoid always-on warehouses, consolidate small jobs onto shared warehouses, use multi-cluster with the Economy policy where queuing is acceptable, set statement timeouts, optimize the most expensive queries, and use resource monitors.

#### How do you reduce storage costs?

Use transient tables for staging and rebuildable data, shorten Time Travel on high-churn tables, drop unused tables and clones that diverged, clean old stage files, and avoid keeping many full copies instead of clones.

#### Is a bigger warehouse always more expensive?

Not necessarily. If a query parallelizes well, doubling the size halves the runtime at double the rate, so the cost is similar and the result arrives sooner. It's more expensive when queries are small or don't parallelize.

#### Why is a warehouse that runs a one-second query every minute expensive?

Each resume bills at least 60 seconds, and auto-suspend keeps it running for the configured idle time after each query. A query every minute can keep the warehouse running permanently. Batch such queries, use serverless tasks, or use a single small shared warehouse.

#### How does the cloud services adjustment work?

Cloud services usage is free up to 10% of the day's warehouse compute; only the excess is billed. Heavy metadata operations (many tiny queries, `SHOW` commands, frequent clones) can exceed it.

### Operations and data protection

#### What is the difference between `ACCOUNT_USAGE` and `INFORMATION_SCHEMA`?

`SNOWFLAKE.ACCOUNT_USAGE` views cover the whole account, keep one year of history and include dropped objects, but have latency (minutes to a few hours). `INFORMATION_SCHEMA` views and table functions are per database, real-time and keep shorter history (7–14 days for query history).

#### What is database replication?

Copying databases (and with replication groups, other objects such as users, roles, warehouses and integrations) to accounts in other regions or clouds, refreshed on a schedule, for disaster recovery, data sharing or migration.

#### What are failover groups and client redirect?

Failover groups (Business Critical) let a secondary account be promoted to primary for replicated objects during an outage. Client redirect uses a connection URL that can be switched to the new primary, so applications reconnect without config changes.

#### How do you manage Snowflake objects as code?

With Terraform (the Snowflake provider) for account objects such as warehouses, roles, grants, databases and integrations; dbt or schemachange for schema and transformation changes; and the Snowflake CLI or `EXECUTE IMMEDIATE FROM` with Git repositories in Snowflake for deploying SQL files.

#### What is a Git repository object in Snowflake?

An integration that clones a Git repository into Snowflake so you can run SQL and Python files from it, reference them in notebooks and procedures, and deploy from a branch or tag.

#### How do you alert on data issues inside Snowflake?

With alerts (scheduled conditions that run an action such as sending an email or a webhook notification), data metric functions (Horizon data quality monitoring: null counts, duplicates, freshness, custom metrics), and failure notifications on tasks.

#### What are data metric functions?

Functions (system ones like `NULL_COUNT`, `DUPLICATE_COUNT`, `FRESHNESS`, or custom ones) attached to tables and run on a schedule, with results stored for monitoring data quality over time.

#### What is the event table?

A special table that collects logs, traces and metrics emitted by UDFs, procedures, Native Apps and Snowpark Container Services, so application code inside Snowflake can be monitored.

#### How do you back up Snowflake data?

Time Travel and Fail-safe cover recent mistakes and disasters; for longer protection use zero-copy clones on a schedule, backups (immutable point-in-time backup sets, where available), replication to another region, or unloading to cloud storage.

#### How do you run SQL deployments safely?

Version SQL in Git, deploy through CI with a service user (key pair or OAuth), use `CREATE OR ALTER` or migration tools (schemachange, dbt, Terraform), test on a cloned database first, and keep rollback scripts or rely on Time Travel and clones.

### Modeling and integration

#### Is star schema modeling still useful in Snowflake?

Yes. Snowflake handles joins well and storage is cheap, but star schemas still make analytics simpler, consistent and fast for BI tools. Many teams use a layered approach: raw, staging, intermediate and marts with facts and dimensions, often built with dbt.

#### Should you normalize or denormalize in Snowflake?

Normalize where data integrity and reuse matter (core entities), denormalize for consumption (wide marts, one big table for specific dashboards). Columnar storage makes wide tables cheap to query when only some columns are read.

#### How does dbt work with Snowflake?

dbt compiles models to SQL and runs them on a Snowflake warehouse through the dbt-snowflake adapter, supporting tables, views, incremental models (`merge`, `delete+insert`, `append`, `microbatch`), dynamic tables, transient tables, query tags and clustering configs.

#### How do Spark and Snowflake integrate?

Through the Spark connector, which reads and writes Snowflake tables with query pushdown, or by sharing Iceberg tables through a catalog so Spark and Snowflake both work on the same files.

#### How do you implement SCD Type 2 in Snowflake?

With a `MERGE` that closes changed current rows and inserts new versions (often two statements or a union trick), with streams and tasks for incremental processing, or with dbt snapshots, which handle it automatically.

#### What is the "one big table" approach, and when does it fit?

A wide denormalized table with everything a use case needs, which is fast to query in a columnar engine and simple for BI. It fits stable, specific use cases; for general analytics, star schemas stay more flexible and consistent.

#### How do you model slowly changing reference data shared by many marts?

As conformed dimensions owned by one model, with surrogate keys and SCD history as needed, referenced by all marts so every report uses the same definitions.

### Scenarios

#### Design an ingestion pipeline from S3 events into Snowflake reporting tables.

Create a storage integration and external stage on the S3 prefix, a Snowpipe with auto-ingest from S3 event notifications into a raw `VARIANT` or typed table, a stream on the raw table, and dynamic tables (or tasks with `MERGE`) building cleaned and aggregated tables at the needed freshness. Add data metric functions, alerts and resource monitors, and manage everything as code.

#### A dashboard warehouse queues every Monday at 9 a.m. What do you do?

Make it a multi-cluster warehouse with enough maximum clusters (Standard policy for interactive users), check whether the slow queries can be optimized or served from aggregates, and separate other workloads that hit the same warehouse at that time.

#### A query scans 98% of a 5 TB table's partitions although it filters on `customer_id`. How do you fix it?

The table isn't clustered by `customer_id`. For point lookups, enable search optimization on that column; for range filters used often, add a clustering key (possibly combined with date); otherwise reconsider the query or create a pre-aggregated table.

#### Someone ran `DELETE FROM orders` without a `WHERE` an hour ago. How do you recover?

Use Time Travel: insert back the rows from `orders AT (OFFSET => -3600)` or `BEFORE (STATEMENT => '<query id>')`, or clone the table at that point and swap it in with `ALTER TABLE … SWAP WITH`. Then restrict delete rights on production tables.

#### Costs jumped 40% this month. How do you investigate?

Compare `WAREHOUSE_METERING_HISTORY` and serverless metering by service and warehouse, find the warehouses and query tags that grew, look at `QUERY_ATTRIBUTION_HISTORY` for the costliest queries, and check for warehouses no longer auto-suspending, new dynamic tables with tight lag, reclustering on high-churn tables, or full refreshes.

#### You must give analysts in each country access only to their rows and hide emails. How?

A row access policy on the tables using a mapping table of roles to countries, and a masking policy (or tag-based masking) on email columns that reveals values only to a privileged role. Grant analysts functional roles mapped to their countries.

#### How would you migrate from an on-premises data warehouse to Snowflake?

Inventory objects, workloads and dependencies; translate DDL and SQL (SnowConvert helps); move historical data through cloud storage and `COPY`; set up incremental loading; rebuild transformations (often in dbt); re-create security with roles and policies; validate with row counts, checksums and report comparisons; run both in parallel before cutover; then tune warehouses and costs.

#### A team wants to process 2 TB of JSON logs daily. How do you load and model it?

Land compressed files of ~100–250 MB in S3, load with Snowpipe or scheduled `COPY` into a `VARIANT` column in a transient raw table, extract commonly used fields into typed columns in a cleaned table clustered by event date, and aggregate into marts. Keep raw data short-lived if it can be reloaded from S3.

#### How do you explain Snowflake's value to a business stakeholder?

One governed place for the company's data that scales instantly for any number of users, costs nothing when idle, and lets teams share and analyze the same numbers without managing servers.

#### A nightly `MERGE` into a 3 TB table takes hours. What do you check?

Whether the target is pruned (add a date or key range filter in the `ON` clause, cluster by the merge key), whether the source has duplicates or is far larger than the changes, the warehouse size and spilling, and whether an incremental approach (streams, `delete+insert` on recent partitions) fits better.

#### A Snowpipe loads duplicate rows sometimes. Why, and what do you do?

The same data arrived in different files (producer retries, renamed files), or files were reloaded with `FORCE`. Make producers write deterministic file names, deduplicate downstream on a business key with `QUALIFY`, and keep the raw layer append-only with file metadata for tracing.

#### How do you give a partner access to a curated dataset without copying it?

Create secure views on the curated tables, put them in a share (or a private listing), and add the partner's account as a consumer; if they have no Snowflake account, create a reader account. Use row access policies or separate views to limit what they see.
