## Databricks Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Databricks study guide: about 200 questions](../../images/databricks_study_guide_title_img.png)

About 200 interview-style questions on Databricks, from the lakehouse idea to Delta Lake, Unity Catalog, ingestion, Lakeflow pipelines and jobs, performance tuning, security and cost. The answers reflect the platform as of 2026; Databricks renames products often, so former names are given where they are still common. Open a question to see its answer, or use the filter to search the whole guide.

<!-- QA -->

### Platform fundamentals

#### What is Databricks?

A cloud data and AI platform, founded by the creators of Apache Spark, that runs on AWS, Azure and Google Cloud. It combines data engineering, SQL analytics, streaming, machine learning and governance on one copy of the data stored in open formats (Delta Lake, Apache Iceberg) in your own cloud storage.

#### What is a lakehouse?

An architecture that stores data in cheap object storage like a data lake, but adds warehouse features on top: ACID transactions, schemas, indexing-like optimizations, fine-grained governance and fast SQL. It avoids keeping one copy of the data in a lake for data science and a second copy in a warehouse for BI.

#### What problems of the classic data lake does the lakehouse solve?

Data lakes had no transactions (readers saw half-written data), no schema enforcement (garbage accumulated), slow queries over many small files, no easy updates or deletes (a problem for GDPR), and weak governance. Delta Lake and Unity Catalog address each of these.

#### What is the control plane versus the compute plane?

The control plane is managed by Databricks in its own account: the web application, notebooks, job scheduler, cluster manager and Unity Catalog metadata. The compute plane is where data is processed. With classic compute it runs in your cloud account (your VPC); with serverless compute it runs in Databricks' account, in the same region. Data at rest stays in your storage in both cases.

#### What is a Databricks workspace?

The environment where users work: notebooks, files, Git folders, jobs, pipelines, SQL queries, dashboards, clusters and experiments. A company usually has several workspaces (for example dev, staging and prod), attached to one Unity Catalog metastore per region.

#### What is a DBU?

A Databricks Unit, the unit of processing capacity that Databricks bills per second. The DBU rate depends on the compute type (jobs, all-purpose, SQL, serverless) and the plan. With classic compute you also pay the cloud provider for the VMs; with serverless, the DBU price includes the infrastructure.

#### Why is jobs compute cheaper than all-purpose compute?

Jobs compute is billed at a lower DBU rate because it runs scheduled, non-interactive workloads and terminates when the job ends. All-purpose clusters are for interactive development and are shared and long-lived, so Databricks charges more for them. Running production work on all-purpose clusters is a classic cost mistake.

#### What languages can you use in Databricks?

Python, SQL, Scala and R in notebooks, plus Java and Scala in JAR jobs. You can mix languages in a notebook with magic commands such as `%sql`, `%python`, `%scala`, `%md` (Markdown) and `%sh` (shell on the driver).

#### What is a Databricks notebook?

A web document of cells that run code against attached compute, with results, charts, comments, version history and real-time co-editing. Notebooks can be scheduled as job tasks, parameterized with widgets and stored as source files in Git.

#### What are Git folders (formerly Repos)?

Workspace folders linked to a Git repository (GitHub, GitLab, Azure DevOps, Bitbucket). They let you clone, branch, commit, pull and push from the workspace, so notebooks and Python files are versioned and reviewed like any other code.

#### What is DBFS, and why is it discouraged now?

The Databricks File System, a legacy abstraction that mounted cloud storage under `dbfs:/` paths, including a workspace root bucket. It has no fine-grained governance, so Databricks now recommends Unity Catalog volumes for files and tables for data, and disables DBFS root and mounts in new setups.

#### What is `dbutils`?

A utility library available in notebooks and jobs: `dbutils.fs` for files, `dbutils.secrets` for secrets, `dbutils.widgets` for parameters, `dbutils.notebook.run` and `dbutils.notebook.exit` to chain notebooks, and `dbutils.jobs.taskValues` to pass small values between job tasks.

#### What are widgets?

Input parameters for notebooks (text, dropdown, combobox, multiselect). In jobs, task parameters fill them. In SQL, parameters are referenced with the `:name` syntax.

```python
dbutils.widgets.text("snapshot_date", "2026-10-01")
snapshot = dbutils.widgets.get("snapshot_date")
```

#### What is the Databricks Runtime?

The versioned software image that clusters run: Apache Spark plus Delta Lake, Photon, libraries, connectors and performance improvements. LTS (long-term support) versions are supported for about three years. The ML runtime adds machine learning libraries.

#### What is Photon?

A vectorized query engine written in C++ that executes Spark SQL and DataFrame operations natively, instead of in the JVM. It speeds up scans, joins, aggregations and writes, especially on Delta and Parquet. It is enabled by default on SQL warehouses and serverless, and optional (at a higher DBU rate) on clusters.

#### What is Spark Connect, and why does it matter on Databricks?

A client-server protocol where the client builds an unresolved logical plan and sends it to a remote Spark server. Serverless compute and shared (standard access mode) clusters use it, so code that touches the `SparkContext`, RDDs or the JVM directly does not work there. DataFrame and SQL code works unchanged.

#### What is the Databricks CLI?

A command-line tool to manage workspaces from a terminal or CI: files, jobs, clusters, secrets, Unity Catalog objects and, above all, Databricks Asset Bundles (`databricks bundle validate|deploy|run`). It authenticates with OAuth (user or service principal) or tokens.

#### What is Databricks Connect?

A library that lets you run Spark code from your IDE or a local Python process against Databricks compute, through Spark Connect. You develop and debug locally while the DataFrame operations execute on the cluster or serverless.

#### What is Lakeflow?

The umbrella name, since 2025, for Databricks' data engineering products: Lakeflow Connect (managed ingestion connectors), Lakeflow Declarative Pipelines (formerly Delta Live Tables) and Lakeflow Jobs (formerly Workflows).

#### What is Mosaic AI?

Databricks' set of AI and ML features: model training and fine-tuning, Model Serving, Vector Search, AI Gateway, agent frameworks and evaluation, all governed through Unity Catalog.

### Delta Lake

#### What is Delta Lake?

An open-source storage format that adds a transaction log to Parquet files. It provides ACID transactions, schema enforcement and evolution, time travel, `MERGE`, `UPDATE` and `DELETE`, and streaming reads and writes. It is the default table format on Databricks.

#### How does the Delta transaction log work?

Each table has a `_delta_log/` folder of ordered JSON commit files (`000…0.json`, `000…1.json`) listing the data files added and removed by each transaction, plus schema and metadata changes. Periodically a Parquet checkpoint summarizes the state so readers don't replay every commit. A table version is the set of files valid after a given commit.

#### How does Delta provide ACID guarantees on object storage?

Writers create new Parquet files, then try to commit by atomically writing the next numbered log entry. If two writers race, only one succeeds; the other checks for conflicts and retries or fails. Readers only see files referenced by committed log entries, so they never see partial writes.

#### What concurrency control does Delta use?

Optimistic concurrency control: transactions don't lock, they check at commit time whether a concurrent commit touched the same data. Appends rarely conflict; concurrent `UPDATE`/`MERGE` on the same files can raise `ConcurrentModificationException`. Partitioning, liquid clustering and row-level concurrency (with deletion vectors) reduce conflicts.

#### What is schema enforcement?

Delta rejects writes whose columns or types don't match the table schema, instead of silently corrupting the table. It protects downstream consumers from bad loads.

#### How does schema evolution work in Delta?

You allow it explicitly: `.option("mergeSchema", "true")` on a write adds new columns, and `ALTER TABLE` changes the schema. For `MERGE`, `WITH SCHEMA EVOLUTION` (or the automatic merge setting) lets new source columns be added. Type widening allows some type changes, such as `int` to `bigint`, without rewriting data.

#### What is time travel?

Querying a previous version of a table by version number or timestamp, using the transaction log:

```sql
SELECT * FROM sales VERSION AS OF 42;
SELECT * FROM sales TIMESTAMP AS OF '2026-10-01';
DESCRIBE HISTORY sales;
```

It is useful for audits, reproducing a report, comparing versions and recovering from bad writes. It only works while old files have not been vacuumed.

#### How do you undo a bad write in Delta?

`RESTORE TABLE sales TO VERSION AS OF 41` (or `TIMESTAMP AS OF`). It creates a new commit pointing back to the old files, so the history is preserved.

#### What does `VACUUM` do?

It deletes data files that are no longer referenced by the current table version and are older than the retention threshold (7 days by default). It saves storage but limits time travel to the retention period. Lowering the threshold below the longest-running read or write can break concurrent queries.

#### What does `OPTIMIZE` do?

It compacts small files into larger ones (around 1 GB by default), which speeds up reads. With Z-ordering or liquid clustering, it also rewrites data so related values sit in the same files.

#### What is the small-files problem?

Many tiny files make reads slow (each file has open and metadata overhead, and statistics are less useful) and slow down the transaction log. Streaming and frequent small appends cause it. Fixes: `OPTIMIZE`, auto compaction and optimized writes, and fewer, larger batches.

#### What are optimized writes and auto compaction?

Optimized writes shuffle data before writing so each partition produces fewer, larger files. Auto compaction runs a small `OPTIMIZE` after a write when a table has many small files. Both are enabled by default for many operations on recent runtimes and on serverless.

#### What is data skipping?

Delta stores min/max values and null counts for the first columns of each file (32 by default). When a query filters on those columns, files whose ranges can't match are skipped without being read. It works best when data is clustered by the filter columns.

#### What is Z-ordering?

A multi-dimensional clustering technique run with `OPTIMIZE table ZORDER BY (col1, col2)`. It co-locates similar values of several columns in the same files to improve data skipping. It has to be rerun as data arrives and is being replaced by liquid clustering.

#### What is liquid clustering?

A clustering method declared on the table with `CLUSTER BY (cols)` that replaces both partitioning and Z-ordering. It clusters data incrementally during `OPTIMIZE`, keys can be changed without rewriting the table, and `CLUSTER BY AUTO` lets Databricks choose keys from the query history. It is the recommended layout for new tables.

```sql
CREATE TABLE events (event_date DATE, user_id BIGINT, payload STRING)
CLUSTER BY (event_date, user_id);
```

#### When should you still partition a Delta table?

Rarely, now that liquid clustering exists. Partitioning only helps for very large tables (roughly over 1 TB) on a low-cardinality column that almost every query filters on, with at least about 1 GB per partition. Over-partitioning creates the small-files problem.

#### What are deletion vectors?

A storage optimization where `DELETE`, `UPDATE` and `MERGE` mark rows as deleted in a small side file instead of rewriting whole Parquet files. Writes become much faster; the files are physically rewritten later by `OPTIMIZE` or `REORG TABLE … APPLY (PURGE)`.

#### What is Change Data Feed?

A table option (`delta.enableChangeDataFeed = true`) that records row-level changes (insert, update_preimage, update_postimage, delete) with the commit version and timestamp. Downstream jobs read only what changed:

```sql
SELECT * FROM table_changes('silver.customers', 120);
```

#### How does `MERGE` work in Delta?

`MERGE INTO` upserts a source into a target by a join condition, with clauses for matched and not-matched rows. It is the basis for CDC, deduplication and SCD logic.

```sql
MERGE INTO silver.customers t
USING updates s ON t.customer_id = s.customer_id
WHEN MATCHED AND s.op = 'DELETE' THEN DELETE
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

#### Why does `MERGE` fail with "multiple source rows matched"?

Because two or more source rows match the same target row, so the result would be ambiguous. Deduplicate the source first, for example keeping the latest row per key with `ROW_NUMBER()`.

#### How do you speed up a slow `MERGE`?

Add filters that let Delta prune target files (for example a date range in the `ON` clause), cluster the target by the merge key, deduplicate and shrink the source, enable deletion vectors, and avoid merging the full history when only recent data changes.

#### What is the difference between a deep clone and a shallow clone?

A deep clone copies the data files and metadata into an independent table. A shallow clone copies only the metadata and points to the source's files, so it is instant and cheap, which is useful for testing changes on production-sized data. Both have their own history from the clone point.

#### What constraints does Delta support?

`NOT NULL` and `CHECK` constraints, which are enforced: a write that violates them fails. Primary and foreign keys can be declared in Unity Catalog, but they are informational (not enforced), used by tools and the optimizer.

#### What are generated and identity columns?

A generated column is computed from other columns (`GENERATED ALWAYS AS (CAST(ts AS DATE))`). An identity column (`GENERATED ALWAYS AS IDENTITY`) assigns unique, increasing (not necessarily consecutive) numbers, which is useful for surrogate keys.

#### What is UniForm?

Universal Format: a Delta table option that also writes Iceberg (and Hudi) metadata, so engines that read Iceberg can read the same files without copying data.

#### What is the difference between a managed and an external table?

A managed table's data lives in storage controlled by Unity Catalog; dropping the table deletes the data (after a retention period), and Databricks can optimize it automatically. An external table points to a path you manage in your own storage location; dropping it removes only the metadata.

#### What does `DESCRIBE DETAIL` show?

The table's format, location, number of files, size in bytes, partition or clustering columns, and properties. It is a quick check for the small-files problem.

#### What is the difference between `overwrite` mode and `replaceWhere`?

`mode("overwrite")` replaces the whole table (as a new version, so time travel still works). `replaceWhere` replaces only the rows matching a predicate. Dynamic partition overwrite (`partitionOverwriteMode=dynamic`) replaces only the partitions present in the new data.

#### How does Delta handle `UPDATE` and `DELETE` without deletion vectors?

It finds the files containing matching rows, rewrites those files without the deleted rows (or with updated values), and commits a transaction that removes the old files and adds the new ones. That is copy-on-write: cheap reads, expensive writes on large files.

#### What is `CONVERT TO DELTA`?

A command that turns an existing Parquet directory into a Delta table in place by writing a transaction log over the existing files, without copying data.

#### What are table properties used for in Delta?

Settings stored with the table, such as `delta.enableChangeDataFeed`, `delta.logRetentionDuration`, `delta.deletedFileRetentionDuration`, `delta.enableDeletionVectors` or `delta.appendOnly`, plus custom key-value metadata. They are set with `TBLPROPERTIES` and shown by `SHOW TBLPROPERTIES`.

#### What is the difference between log retention and deleted-file retention?

`delta.logRetentionDuration` (30 days by default) controls how long commit history is kept; `delta.deletedFileRetentionDuration` (7 days by default) controls how long `VACUUM` keeps unreferenced data files. Time travel needs both the log entries and the data files.

### Unity Catalog and governance

#### What is Unity Catalog?

Databricks' unified governance layer for data and AI assets across workspaces: one place to define access control, auditing, lineage, data discovery and sharing for tables, views, volumes, functions and models. It has also been released as open source.

#### What is the Unity Catalog object hierarchy?

Metastore (one per region) → catalog → schema (database) → tables, views, materialized views, volumes, functions and models. Objects are addressed with a three-level name: `catalog.schema.table`.

#### What is a volume?

A Unity Catalog object that governs access to non-tabular files (CSV, JSON, images, PDFs, wheels) in cloud storage, addressed as `/Volumes/catalog/schema/volume/path`. Managed volumes live in Unity Catalog-managed storage; external volumes map to an existing storage path.

#### What are storage credentials and external locations?

A storage credential wraps a cloud identity (an AWS IAM role, an Azure managed identity) that can access storage. An external location combines a storage path with a credential, and grants on it control who can create external tables or volumes there.

#### How do you grant permissions in Unity Catalog?

With SQL or the UI, to users, groups or service principals. Privileges are inherited down the hierarchy, and a user needs `USE CATALOG` and `USE SCHEMA` on the parents to reach an object.

```sql
GRANT USE CATALOG ON CATALOG prod TO `analysts`;
GRANT USE SCHEMA, SELECT ON SCHEMA prod.gold TO `analysts`;
```

#### What are row filters and column masks?

Functions attached to a table that are evaluated at query time. A row filter returns which rows a user may see (for example only their country); a column mask returns the value or a masked version depending on the user's group membership. Data stays in one table instead of in many filtered copies.

#### What are dynamic views?

Views that use functions like `current_user()` or `is_account_group_member()` to filter rows or redact columns. They were the usual approach before row filters and column masks existed.

#### What lineage does Unity Catalog capture?

Table- and column-level lineage for queries run on Databricks compute, across notebooks, jobs, pipelines and dashboards, shown in Catalog Explorer and queryable from system tables. It answers "what breaks if I change this column?" and "where does this number come from?".

#### What are system tables?

Read-only tables in the `system` catalog with operational data: billing usage (`system.billing.usage`), audit logs, table lineage, job runs, cluster events, query history and more. They are the basis for cost dashboards and auditing.

#### What is the legacy Hive metastore, and how do you migrate from it?

The per-workspace metastore that predates Unity Catalog, with workspace-local permissions. Migration consists of creating a Unity Catalog metastore, upgrading tables (`SYNC` for external tables, `CREATE TABLE … AS SELECT` or deep clone for managed ones) and updating code to three-level names. The UCX tool automates much of the assessment and migration.

#### What is Delta Sharing?

An open protocol for sharing live data securely across organizations and platforms without copying it. The provider creates a share of tables, views or volumes; recipients read it from Databricks or from open-source clients (pandas, Spark, BI tools). Databricks-to-Databricks sharing uses Unity Catalog identities.

#### What is Lakehouse Federation?

Query federation that lets Unity Catalog register external databases (PostgreSQL, MySQL, SQL Server, Snowflake, Redshift, BigQuery and others) as foreign catalogs, so you can query them in place with governance and lineage, without first ingesting the data.

#### What are tags and comments used for in Unity Catalog?

Comments document tables and columns (and power AI-generated descriptions and search); tags (key-value pairs) classify objects, for example `pii=true`, which can drive policies, discovery and audits.

#### What is a service principal, and why use one for production jobs?

A non-human identity for automation. Production jobs and CI/CD deployments should run as a service principal so they don't depend on a person's account and permissions, and so access is limited to what the pipeline needs.

#### How do you manage secrets in Databricks?

In secret scopes (Databricks-backed or backed by Azure Key Vault), read with `dbutils.secrets.get(scope, key)`. Secret values are redacted in notebook output. For cloud resources, prefer identity-based access (instance profiles, storage credentials) over secrets.

#### What is the difference between account-level and workspace-level administration?

Account admins manage identities (users, groups, service principals, often synced from an identity provider through SCIM), metastores, workspaces and account-wide settings. Workspace admins manage settings, compute policies and access within one workspace.

#### What is the difference between ownership and privileges?

The owner of an object (a user, group or service principal) can grant privileges on it and manage it. Privileges such as `SELECT`, `MODIFY`, `CREATE TABLE` or `READ VOLUME` grant specific actions. Making a group the owner of production objects avoids depending on one person.

#### What is workspace-catalog binding?

A setting that limits which workspaces can access a catalog, for example so that a production catalog is only reachable from the production workspace, even if users have grants on it.

#### What is the information schema in Unity Catalog?

A set of standard SQL views in each catalog (`information_schema.tables`, `columns`, `table_privileges` and others) describing the objects and permissions, useful for documentation and audits.

#### How do you discover data in Unity Catalog?

Through Catalog Explorer and search, which use names, comments, tags and lineage, plus popularity signals such as frequent users and queries. Good comments and tags make discovery much better.

### Compute

#### What types of compute does Databricks offer?

All-purpose clusters for interactive work, jobs compute created for one job run, SQL warehouses for SQL and BI, serverless compute for notebooks, jobs and pipelines, and instance pools to speed up classic cluster start-up.

#### What is serverless compute?

Compute that Databricks provisions and manages in its own account: it starts in seconds, scales automatically, is always on a current runtime with Photon, and is billed only while it works. You give up control of instance types and Spark configs, and code must be Spark Connect compatible.

#### What is the anatomy of a classic cluster?

One driver node that runs the main program, plans the work and collects results, plus worker nodes that run executors that process partitions. A single-node cluster runs everything on the driver, which is enough for small data and ML on one machine.

#### What are access modes?

Settings that control isolation and governance on classic compute. Standard (formerly shared) lets several users share a cluster with Unity Catalog isolation, using Spark Connect. Dedicated (formerly single user) assigns the cluster to one user or group and supports more APIs, such as RDDs and some ML libraries.

#### How does autoscaling work?

You set a minimum and maximum number of workers; Databricks adds workers when tasks are queued and removes them when they are idle. Autoscaling suits interactive and variable workloads; fixed-size clusters can be more predictable for steady batch jobs. Streaming workloads should use enhanced autoscaling in pipelines.

#### What is auto-termination?

A cluster setting that shuts down an idle all-purpose cluster after a number of minutes. Leaving it off is one of the most common causes of wasted spend.

#### What are instance pools?

A set of idle, ready-to-use VMs that clusters draw from, to cut start time from minutes to seconds. Idle pool instances incur cloud costs but no DBUs.

#### Should you use spot instances?

For workers of fault-tolerant batch jobs, yes: they are much cheaper and Spark retries tasks if one is reclaimed. Keep the driver on-demand, since losing it kills the job, and allow a fallback to on-demand.

#### What are cluster policies?

Admin-defined rules that limit how users create clusters: allowed instance types, maximum size, mandatory tags, auto-termination, runtime versions. They control cost and standardize configurations.

#### What is a SQL warehouse?

Compute dedicated to SQL queries for Databricks SQL, BI tools and dashboards. Types: serverless (fast start, recommended), pro and classic. It scales out by adding clusters to absorb concurrency and uses Photon and intelligent workload management.

#### How do you size a SQL warehouse?

Pick a T-shirt size from query complexity and data volume (bigger means faster single queries), and set the maximum number of clusters for concurrency (more users at once). Watch query queuing and spilling in query history, and set auto-stop.

#### How do you install libraries on a cluster?

As compute-scoped libraries (PyPI, Maven, wheels from volumes or workspace files), notebook-scoped with `%pip install`, or as job task dependencies. On serverless, you declare dependencies in the environment configuration. Pin versions for reproducibility.

#### What are init scripts?

Shell scripts that run on each node at start-up, used to install system packages or configure the environment. They should be stored in volumes or workspace files, not DBFS, and kept to a minimum because they slow start-up and complicate debugging.

#### What happens when the driver runs out of memory?

The notebook or job fails or restarts. Common causes: `collect()` or `toPandas()` on large data, broadcasting a table that is too large, large Python objects on the driver, or too many tasks tracked at once. Keep data in Spark, write results to tables, and size the driver appropriately.

#### Where do you look when a cluster is slow?

The Spark UI (jobs, stages, task durations, shuffle sizes, spill, skew), cluster metrics (CPU, memory, disk), driver logs, and the query profile for SQL. Compare the median and maximum task times in a stage to detect skew.

#### What is a single-node cluster good for?

Small data processing, pandas and scikit-learn work, and lightweight development. It has no workers, so Spark runs in local mode on the driver, which is cheap but doesn't scale.

#### What are GPU clusters used for?

Deep learning training and inference, and some GPU-accelerated libraries. They need an ML runtime with GPU drivers and are expensive, so they should auto-terminate quickly.

#### What does the "standard" versus "dedicated" choice mean for ML workloads?

ML libraries that need direct access to the JVM or the `SparkContext`, or GPU training, usually require dedicated access mode or serverless with the right environment. Standard mode is better for shared SQL and DataFrame work.

### Ingestion

#### What options exist for loading data into Databricks?

Auto Loader for files arriving in cloud storage, `COPY INTO` for idempotent batch file loads, Lakeflow Connect managed connectors (Salesforce, Workday, SQL Server, Google Analytics and others), Structured Streaming from Kafka, Kinesis or Event Hubs, Lakehouse Federation for querying in place, partner tools (Fivetran and others) and file uploads to volumes.

#### What is Auto Loader?

A Structured Streaming source (`cloudFiles`) that incrementally and efficiently processes new files as they land in cloud storage. It tracks which files have been processed in its checkpoint, so each file is loaded exactly once, and it can infer and evolve the schema.

```python
(spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/Volumes/raw/_schemas/orders")
    .load("/Volumes/raw/landing/orders/")
  .writeStream
    .option("checkpointLocation", "/Volumes/raw/_checkpoints/orders")
    .trigger(availableNow=True)
    .toTable("bronze.orders"))
```

#### What are Auto Loader's file detection modes?

Directory listing, which lists the input path to find new files (simple, fine for moderate volumes), and file notification, which subscribes to storage events through a queue (SQS/SNS, Event Grid) and scales to millions of files. Newer setups can use managed file events on external locations.

#### How does Auto Loader handle schema changes?

It stores the inferred schema in the schema location. With the default `addNewColumns` mode, a new column stops the stream, updates the schema and the stream continues after a restart. Data that doesn't fit the schema (wrong type, unexpected column) goes into the `_rescued_data` column instead of being lost.

#### What is the rescued data column?

A JSON string column (`_rescued_data`) where Auto Loader puts values that couldn't be parsed into the schema. Monitoring it reveals upstream format changes.

#### What is `COPY INTO`?

A SQL command that loads files from a path into a Delta table and is idempotent: files already loaded are skipped. It suits scheduled batch loads of thousands of files; Auto Loader is preferred for millions of files or continuous ingestion.

```sql
COPY INTO bronze.customers
FROM '/Volumes/raw/landing/customers/'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');
```

#### What does `trigger(availableNow=True)` do?

It makes a streaming query process everything available at start (in several batches respecting rate limits), then stop. It gives the incremental bookkeeping of streaming with the cost profile of a scheduled batch job.

#### What is a streaming checkpoint?

A storage location where a streaming query records its progress (offsets or processed files) and state. It gives exactly-once processing across restarts. Each query needs its own checkpoint, and deleting it makes the query start over.

#### How do you ingest from Kafka?

With the Structured Streaming Kafka source, which reads `key`, `value`, `topic`, `partition`, `offset` and `timestamp`. Parse `value` (JSON, Avro with a schema registry, Protobuf), write raw records to bronze, and keep the checkpoint per query.

#### What is the `_metadata` column?

A hidden column available when reading files, with `file_path`, `file_name`, `file_size` and `file_modification_time`. It replaces `input_file_name()` (not supported in Unity Catalog) to record the source file of each row.

#### Why should you avoid `inferSchema` in production?

Inference requires an extra pass over the data, can infer different types from different files, and silently changes when the source changes. Declare schemas (data contracts) for production loads, or let Auto Loader manage inference with schema hints.

#### What is Lakeflow Connect?

Managed, serverless ingestion connectors for SaaS applications and databases. They handle incremental extraction (often CDC) and land the data in Unity Catalog tables through a pipeline, without writing extraction code.

#### How do you load data from a relational database without Lakeflow Connect?

With the Spark JDBC reader, partitioning the read with `partitionColumn`, `lowerBound`, `upperBound` and `numPartitions` so it runs in parallel, and loading incrementally by a watermark column (for example `updated_at`). Store credentials in secrets.

#### How do you handle late-arriving files?

Auto Loader picks up any new file whenever it arrives, regardless of its date, so the load itself is safe. Downstream, use `MERGE` keyed on business keys, or reprocess the affected dates with `replaceWhere`, so late data corrects earlier results.

#### What are schema hints in Auto Loader?

Explicit types for some columns (`cloudFiles.schemaHints = "amount DECIMAL(18,2), event_ts TIMESTAMP"`) that override inference while the rest of the schema is still inferred.

#### What is `read_files`?

A SQL table-valued function that reads files (CSV, JSON, Parquet, Avro, XML, text) from a path or volume with schema inference. With `STREAM read_files(...)` in a streaming table, it uses Auto Loader underneath.

### Lakeflow Declarative Pipelines

#### What are Lakeflow Declarative Pipelines (formerly Delta Live Tables)?

A declarative framework where you define tables and the queries that produce them, in SQL or Python, and Databricks works out the dependencies, orchestrates the execution, manages the infrastructure, retries failures and applies data quality expectations. The engine was contributed to Apache Spark as Spark Declarative Pipelines.

#### What is the difference between a streaming table and a materialized view?

A streaming table processes each input row once, appending or upserting incrementally, which suits ingestion and append-only data. A materialized view stores the result of a query and is refreshed (incrementally when possible) so it always reflects its sources, which suits aggregations and joins over changing data.

```sql
CREATE OR REFRESH STREAMING TABLE bronze_orders
AS SELECT * FROM STREAM read_files('/Volumes/raw/landing/orders/', format => 'json');

CREATE OR REFRESH MATERIALIZED VIEW gold_daily_sales
AS SELECT order_date, sum(amount) AS sales FROM silver_orders GROUP BY order_date;
```

#### What are expectations?

Data quality rules declared on a pipeline table. Each row is checked, and the policy decides what happens on a violation: keep and record it (`EXPECT`), drop the row (`ON VIOLATION DROP ROW`) or fail the update (`ON VIOLATION FAIL UPDATE`). Metrics are visible in the pipeline UI and event log.

```sql
CONSTRAINT valid_amount EXPECT (amount >= 0) ON VIOLATION DROP ROW
```

#### How do you handle CDC in declarative pipelines?

With `AUTO CDC` (formerly `APPLY CHANGES INTO`), which applies a change feed to a target table using a key and a sequencing column, handles out-of-order events and deletes, and can keep history as SCD Type 1 or Type 2 without writing `MERGE` logic.

#### What is the difference between triggered and continuous pipeline mode?

Triggered mode processes the available data and stops (cheaper, for batch schedules). Continuous mode keeps the pipeline running to process data with low latency.

#### What is development mode in a pipeline?

A mode that reuses the cluster between updates and disables retries, so you iterate quickly and see errors at once. Production mode restarts the cluster on recoverable errors and retries.

#### What is the pipeline event log?

A Delta table recording every event of a pipeline: updates, flow progress, data quality metrics, lineage and errors. You query it to build monitoring and data quality dashboards.

#### When would you not use declarative pipelines?

When you need fine-grained control over every step, logic that doesn't fit the declarative model (complex procedural code, calls to external systems per batch), or portability to plain Spark jobs. Many teams use plain jobs with Delta and `MERGE` and get the same results with more code.

#### What is a full refresh of a pipeline table?

Truncating the table and reprocessing all source data from the beginning, including resetting streaming checkpoints. It is needed after logic changes that must apply to history, but can be costly and can lose data if the source retention is shorter than the history.

#### How do you write a declarative pipeline in Python?

With the `pipelines` module (formerly `dlt`): decorated functions return DataFrames, and the decorators declare tables and expectations.

```python
from pyspark import pipelines as dp

@dp.table(comment="Cleaned orders")
@dp.expect_or_drop("valid_amount", "amount >= 0")
def silver_orders():
    return spark.readStream.table("bronze_orders").dropDuplicates(["order_id"])
```

#### Where do pipeline tables live?

In the Unity Catalog catalog and schema configured for the pipeline (and other schemas if fully qualified names are used). They are ordinary Delta tables for readers, but only the pipeline should write to them.

#### What is a flow in a declarative pipeline?

A unit of processing that writes into a target table. A streaming table can have several append flows (for example one per source region), which lets you add sources without a full refresh.

#### How is a declarative pipeline billed?

Through pipeline compute (serverless or classic) at the pipeline product tier (Core, Pro, Advanced), with higher tiers adding CDC and expectations. Serverless pipelines are billed per use and are the default.

### Jobs and orchestration

#### What are Lakeflow Jobs (formerly Workflows)?

Databricks' built-in orchestrator. A job is a DAG of tasks (notebooks, Python scripts, wheels, SQL, dbt, pipelines, JARs, other jobs) with dependencies, schedules or triggers, parameters, retries, timeouts, notifications and compute settings.

#### What task types can a job have?

Notebook, Python script, Python wheel, SQL (query, file, dashboard or alert), dbt, pipeline, JAR, Spark Submit, Run Job (another job), If/else condition and For each (loop over values).

#### What triggers can start a job?

A cron schedule, a file arrival in a storage location, a table update (when a source table changes), continuous mode (restart as soon as it ends), the API or CLI, or a manual run.

#### How do you pass values between tasks?

Small values with task values (`dbutils.jobs.taskValues.set` in one task and `get` in a later one, or dynamic references like `{{tasks.ingest.values.row_count}}` in task parameters). Data itself should be passed through tables, not task values.

#### What are job parameters and dynamic value references?

Parameters defined at job level and passed to every task, overridable at run time. Dynamic value references such as `{{job.start_time.iso_date}}` or `{{job.run_id}}` inject run context, which is useful for idempotent, date-driven processing.

#### How do you make a Databricks job idempotent?

Write with `MERGE` or `replaceWhere`/dynamic partition overwrite for the processed date instead of blind appends, base the processing date on a parameter rather than the wall clock, use streaming checkpoints for incremental ingestion, and make side effects (notifications, exports) safe to repeat.

#### How do you rerun only the failed part of a job?

With "Repair run", which reruns the failed tasks and their downstream dependencies, reusing successful upstream results, optionally with new parameters.

#### What is the difference between job compute and running tasks on a shared cluster?

Each task can use its own job cluster, share a job cluster with other tasks of the same run, use serverless compute, or use an existing all-purpose cluster. Shared job clusters avoid repeated start-up; serverless removes start-up altogether.

#### How do you get alerted when a job fails or is slow?

Configure notifications (email, Slack, Teams, PagerDuty, webhooks) on start, success, failure and duration thresholds, and set a timeout and maximum concurrent runs. System tables on job runs let you build longer-term reliability dashboards.

#### Should you orchestrate Databricks with Airflow or with Jobs?

Jobs is enough when the workflow lives mainly in Databricks, and it is cheaper and simpler. Airflow (or Dagster, Prefect) makes sense when the DAG spans many systems, when the company already standardizes on it, or for complex cross-team dependencies. Airflow's Databricks provider can trigger jobs and wait for them.

#### What does the For each task do?

It runs a nested task once per item of a list (for example a list of countries or dates), with a configurable concurrency, so you don't have to define one task per item.

#### What is the If/else condition task used for?

Branching a job based on a value, such as a task value or parameter: for example, skip the publish step when a data quality task reports zero valid rows.

#### How do you limit concurrent runs of a job?

With the maximum concurrent runs setting (usually 1 for jobs that write the same tables) and the queueing option, so a new trigger waits instead of being skipped or running in parallel.

#### How do you run a job for a backfill of many dates?

Parameterize the job by date and trigger it per date (through the API, CLI or a For each task over a list of dates), keeping writes idempotent, and limit concurrency so the backfill doesn't starve production workloads.

### Spark and performance on Databricks

#### How do you read a Spark query plan?

With `df.explain(mode="formatted")` or the SQL tab of the Spark UI. Read it bottom-up: scans (check pushed filters and pruned files), exchanges (shuffles), join strategies (broadcast, sort-merge), and aggregations. The query profile in Databricks SQL shows the same with timings.

#### What is Adaptive Query Execution?

A Spark feature, on by default, that re-optimizes a query at stage boundaries using runtime statistics: it coalesces small shuffle partitions, switches sort-merge joins to broadcast joins when a side turns out small, and splits skewed partitions.

#### What is a broadcast join, and when does it help?

Spark sends a copy of the small table to every executor, so the large table is joined without being shuffled. It helps when one side is small enough (tens of MB by default, more with hints). Broadcasting a table that is too big causes driver or executor out-of-memory errors.

#### What is data skew, and how do you fix it?

Some keys hold far more rows than others, so a few tasks take much longer than the rest. Fixes: let AQE split skewed partitions, broadcast the small side, filter out or handle hot keys (often nulls) separately, or salt the key to spread it across partitions.

#### What is spill, and why is it slow?

When a task's data doesn't fit in execution memory, Spark writes it to local disk and reads it back. It shows up in the Spark UI as spill (memory) and spill (disk). Fix it with more, smaller partitions, larger or memory-optimized workers, or less data per task.

#### How do you choose the number of shuffle partitions?

`spark.sql.shuffle.partitions` defaults to 200. With AQE, set a generous number (or `auto` on Databricks) and let AQE coalesce. Aim for partitions of roughly 100–200 MB after shuffle; too few causes spill, too many causes overhead.

#### Why are Python UDFs slow, and what are the alternatives?

Each row is serialized between the JVM and a Python worker, and the optimizer can't see inside the function. Use built-in functions first, then pandas (vectorized) UDFs with Arrow, or SQL UDFs. Photon can't accelerate Python UDFs either.

#### Should you use `cache()` on Databricks?

Sparingly. Caching helps when the same DataFrame is reused several times in one interactive session, but it uses memory and is not supported on serverless. The disk cache (automatic SSD caching of remote Parquet files on some instance types) often gives the benefit without code changes. For reuse across jobs, write a table.

#### What is the disk cache?

An automatic cache, formerly called the Delta cache, that stores copies of remote Parquet and Delta files on the workers' local SSDs, so repeated reads of the same data are faster. It is managed transparently.

#### Why is `withColumn` in a loop a problem?

Each call adds a projection to the logical plan, and analyzing a very deep plan becomes slow (it can take minutes before any data is processed). Use one `select` or `withColumns` with a dictionary instead.

#### What is predictive optimization?

A Unity Catalog feature that automatically runs `OPTIMIZE`, `VACUUM` and statistics collection on managed tables when it predicts a benefit, so you don't have to schedule maintenance jobs.

#### How do you reduce the cost of a heavy Databricks job?

Use jobs or serverless compute instead of all-purpose clusters, enable Photon where it pays off, process incrementally instead of full recomputes, prune reads with clustering and filters, right-size and autoscale clusters, use spot workers, avoid unnecessary shuffles and Python UDFs, and monitor with `system.billing.usage`.

#### What is `replaceWhere`?

A write option that atomically replaces only the rows matching a predicate, typically one date range, leaving the rest of the table untouched. It makes reprocessing a period idempotent.

```python
(df.write.format("delta").mode("overwrite")
   .option("replaceWhere", "event_date = '2026-10-15'")
   .saveAsTable("silver.events"))
```

#### How would you troubleshoot a job that suddenly got slower?

Compare the slow run with a normal one: input sizes, number of files (small files, missing `OPTIMIZE`), plan changes (a broadcast became a sort-merge join), skew in one stage, spill, cluster size or spot losses, and code or data changes since the last good run.

#### What is the difference between narrow and wide transformations?

Narrow transformations (`filter`, `select`, `withColumn`) compute each output partition from one input partition, with no data movement. Wide transformations (`groupBy`, `join`, `distinct`, `orderBy`) need a shuffle across the network. Performance work is mostly about shuffles.

#### What is the difference between `repartition` and `coalesce`?

`repartition(n)` does a full shuffle and can increase or decrease the number of partitions, optionally by columns. `coalesce(n)` only merges partitions without a full shuffle, so it's cheaper but can only decrease them and can leave uneven partitions. `coalesce(1)` funnels everything through one task.

#### Why does `count()` before every step slow a job down?

Each action triggers a full execution of the plan up to that point. Counting for logging after every transformation recomputes the data repeatedly. Get metrics from the Delta commit (`numOutputRows` in the history) or compute them once.

#### What are column statistics and why compute them?

`ANALYZE TABLE … COMPUTE STATISTICS FOR ALL COLUMNS` stores row counts and column statistics that the cost-based optimizer uses to choose join orders and strategies. Predictive optimization can maintain them automatically.

#### How does file pruning differ from partition pruning?

Partition pruning skips whole directories based on partition columns. File pruning (data skipping) skips individual files using the min/max statistics in the Delta log, so it works on any column with statistics and benefits from clustering.

### Databricks SQL and analytics

#### What is Databricks SQL?

The SQL warehousing part of the platform: SQL warehouses, a SQL editor, query history and profiles, alerts, dashboards and connectors for BI tools (Power BI, Tableau, Looker) through JDBC/ODBC.

#### What are AI/BI dashboards and Genie?

AI/BI dashboards are the current Databricks dashboards, built on SQL warehouses with AI-assisted authoring. Genie is a natural-language interface where business users ask questions of curated tables and get SQL-backed answers.

#### What is a materialized view in Databricks SQL?

A view whose results are stored and refreshed (on a schedule or on demand, incrementally when possible). It speeds up expensive aggregations for dashboards. It is created with `CREATE MATERIALIZED VIEW` and runs on serverless pipelines.

#### What are SQL alerts?

Scheduled queries that compare a result with a threshold and notify (email, Slack, webhook) when the condition is met, for example when a data quality check returns rows.

#### What is query federation used for in analytics?

Joining Databricks tables with tables still in an operational database or another warehouse, for exploration or migration, without building an ingestion first. For heavy repeated use, ingesting the data is faster and cheaper.

#### What is the difference between a view, a temporary view and a materialized view?

A view stores only the query and runs it on each read. A temporary view exists only in the current session. A materialized view stores precomputed results and must be refreshed.

#### How do BI tools connect to Databricks?

Through JDBC/ODBC drivers or native connectors (Power BI, Tableau, Looker, Excel) pointing at a SQL warehouse, authenticating with OAuth or tokens. Permissions are enforced by Unity Catalog for the connecting identity.

#### What is the result cache in Databricks SQL?

A cache of query results on SQL warehouses: when the same query runs again and the underlying tables haven't changed, the result is returned without recomputation.

#### What is a metric view?

A Unity Catalog object that defines business metrics (measures and dimensions) once in YAML on top of a table, so dashboards, Genie and SQL users compute them consistently.

### Medallion architecture and modeling

#### What is the medallion architecture?

A layered way to organize lakehouse data: bronze holds raw data as received (append-only, with load metadata), silver holds cleaned, conformed, deduplicated and validated data, and gold holds business-level aggregates and dimensional models ready for BI and ML. Quality and structure increase layer by layer.

#### Why keep a raw bronze layer?

So you can reprocess history when logic changes or bugs are found, audit what the source actually sent, and decouple ingestion from transformation. Bronze should be cheap to keep and faithful to the source.

#### What belongs in silver?

Typed and renamed columns, deduplication, standardized values (dates, codes, addresses), joins to reference data, data quality checks with quarantine of bad rows, and history (SCD Type 2) when needed. Silver is the single trusted version of each entity.

#### What belongs in gold?

Data shaped for consumption: star schemas (facts and dimensions), aggregates, feature tables and data products, with business definitions applied. Gold tables are usually smaller and optimized for read performance.

#### How do you implement SCD Type 2 on Delta?

With `MERGE`: close the current row (set `valid_to` and `is_current = false`) when tracked attributes change, and insert the new version. A common trick is to merge a union of the updates with a null merge key for changed rows, so one `MERGE` both closes and inserts. Declarative pipelines do it with `AUTO CDC … STORED AS SCD TYPE 2`.

#### How do you quarantine bad records?

Validate rows against rules in silver, write failing rows with the reasons to a quarantine table, and continue with the valid ones. Monitor the quarantine rate and alert on spikes. Expectations with `DROP ROW` plus a separate inverse query achieve the same in declarative pipelines.

#### Should you use one catalog per environment or per layer?

A common pattern is one catalog per environment (`dev`, `staging`, `prod`) with schemas per layer (`bronze`, `silver`, `gold`), because environments need different permissions and storage. Some teams prefer catalogs per domain or business unit. Consistency matters more than the choice.

#### What is a data product in the Databricks context?

A curated, documented and governed set of tables (usually gold) owned by a team, with quality checks, a clear interface and access granted through Unity Catalog, possibly shared through Delta Sharing.

#### Is the medallion architecture always three layers?

No. It is a convention, not a rule. Small projects may merge silver and gold; others add a landing zone before bronze or a platinum/serving layer after gold. What matters is that each layer has a clear contract.

#### Should bronze be a Delta table or raw files?

Usually raw files stay in a landing zone (or volume) and bronze is a Delta table loaded from them with minimal changes plus load metadata. Delta in bronze gives transactions, schema tracking and fast reprocessing; keeping the original files gives an exact copy for audits.

#### How do you model gold for both BI and ML?

Star schemas (facts at a declared grain with conformed dimensions) for BI, and feature tables keyed by entity and time for ML, both built from the same silver tables so numbers agree.

### Machine learning and AI

#### What is MLflow?

An open-source platform, created by Databricks, for the ML lifecycle: experiment tracking (parameters, metrics, artifacts), model packaging, a model registry with versions and aliases, evaluation, and tracing for generative AI applications. On Databricks it is managed and integrated with Unity Catalog.

#### What does it mean to register a model in Unity Catalog?

Models are stored as Unity Catalog objects (`catalog.schema.model`) with versions and aliases such as `champion`, governed by the same permissions and lineage as tables, and usable across workspaces.

#### What is a feature table?

A Delta table with a primary key used to store ML features in Unity Catalog. Training sets are built by joining feature tables to labels (with point-in-time correctness for time series), and the same features can be served online for inference.

#### What is Model Serving?

A serverless service that exposes models (custom MLflow models, foundation models, external models) as REST endpoints with autoscaling, monitoring and access control.

#### What is Vector Search?

A managed vector database that indexes embeddings of a Delta table and keeps the index in sync, used for retrieval-augmented generation (RAG) and similarity search.

#### What are AI functions in Databricks SQL?

SQL functions such as `ai_query`, `ai_classify`, `ai_extract`, `ai_summarize` and `ai_translate` that call models from SQL, so you can enrich tables with LLM output in batch.

### Security, cost and operations

#### How does Databricks access data in AWS S3 securely?

Through IAM roles: in Unity Catalog, a storage credential wraps an IAM role that trusts Databricks, and external locations grant access to paths. Legacy setups used instance profiles attached to clusters. Access keys in code should be avoided.

#### What network security options exist?

Deploying classic compute in your own VPC/VNet, private connectivity between the control and compute planes (PrivateLink, Private Link), IP access lists, no public IPs on cluster nodes, serverless network policies for egress control, and customer-managed keys for encryption.

#### How do you audit who accessed what?

With audit logs (available in the `system.access.audit` table), Unity Catalog lineage and query history. They record logins, permission changes, data access and job actions.

#### How do you monitor and control Databricks spend?

Tag clusters, jobs and warehouses with cost centers, query `system.billing.usage` joined with list prices, set budgets and alerts, enforce cluster policies (instance types, auto-termination, maximum workers), use serverless or jobs compute for production, and review the most expensive jobs regularly.

#### What are Databricks Asset Bundles?

A way to describe Databricks resources (jobs, pipelines, dashboards, models, permissions) as YAML next to the code in Git, with targets for each environment. The CLI validates, deploys and runs them, which makes Databricks projects deployable through CI/CD.

```yaml
bundle:
  name: sales_pipeline
targets:
  dev:
    mode: development
    default: true
  prod:
    mode: production
resources:
  jobs:
    daily_sales:
      name: daily_sales
      tasks:
        - task_key: build
          notebook_task:
            notebook_path: ./src/build_sales.py
```

#### What does `mode: development` change in a bundle target?

It prefixes deployed resources with the user's name, pauses schedules and triggers, and deploys to a per-user folder, so several developers can deploy the same bundle without clashing. `mode: production` checks that the deployment runs as a service principal (or a set identity) and doesn't use these shortcuts.

#### How do you set up CI/CD for Databricks?

Keep code and bundle definitions in Git, run unit tests (with local Spark or Databricks Connect) and linting on pull requests, validate the bundle, deploy to a staging target and run integration tests, then deploy to production after approval, all as a service principal authenticated through OAuth or workload identity federation.

#### How do you test PySpark code for Databricks?

Factor transformations into pure functions that take and return DataFrames, test them with pytest on a local SparkSession and small fixtures (comparing with `assertDataFrameEqual`), add end-to-end tests on synthetic data, and run data quality checks (expectations, constraints) in the pipeline itself.

#### What are Databricks Apps?

A way to build and host data and AI applications (Streamlit, Dash, Gradio, Flask and others) directly in the workspace, with authentication and access to governed data through Unity Catalog.

#### What is Lakebase?

A managed PostgreSQL-compatible operational database inside Databricks, based on serverless Postgres, meant for low-latency transactional workloads (apps, feature serving) that sync with lakehouse tables.

### Scenarios

#### Design a pipeline that ingests daily CSV files from S3 into a reporting table.

Land files in S3, read them with Auto Loader (`availableNow` trigger) into a bronze Delta table with a declared schema and `_metadata` columns, clean, deduplicate and validate into silver with `MERGE`, build gold aggregates or a star schema, schedule it as a job with retries and alerts, govern it with Unity Catalog, and deploy it with a bundle.

#### A daily job writes duplicates every time it's rerun. What do you change?

Replace the append with an idempotent write: a `MERGE` on the business key, or `replaceWhere` on the processing date. Derive the date from a job parameter, and add a uniqueness check on the target.

#### Your Delta table has 500,000 small files. What do you do?

Run `OPTIMIZE` (with liquid clustering on the main filter columns), enable optimized writes and auto compaction or predictive optimization, then fix the cause: batch micro-appends, avoid over-partitioning, and use `availableNow` triggers rather than very frequent tiny streams. Run `VACUUM` afterwards to remove the old files.

#### A join between a 2 TB fact table and a 50 MB dimension is slow. What do you check?

Whether it's being broadcast (check the plan; add a broadcast hint or raise the threshold), whether the fact scan is pruning files (filters on clustered columns), skew on the join key, and spill. A 50 MB dimension should almost always be broadcast.

#### A streaming query fails after a schema change in the source. How do you handle it?

With Auto Loader in `addNewColumns` mode, restart the stream so it picks up the new schema. For incompatible changes, update the target schema (or use the rescued data column), and if the logic changed, start a new checkpoint with a clear backfill plan. Add alerting on rescued data.

#### Analysts must see only their country's rows in a shared table. How do you implement it?

Attach a Unity Catalog row filter function to the table that checks the user's group membership against the country column. Grant `SELECT` to the analyst groups. Use column masks for sensitive columns.

#### How would you migrate a Hive-based on-premises pipeline to Databricks?

Inventory jobs, tables and dependencies; copy data to cloud storage and convert to Delta (`CONVERT TO DELTA` for Parquet); port HiveQL to Spark SQL (mostly compatible); replace Oozie or cron with Lakeflow Jobs or Airflow; put tables in Unity Catalog; validate results side by side (row counts, checksums, aggregates) before switching consumers.

#### Someone dropped columns from a gold table by mistake an hour ago. How do you recover?

Check `DESCRIBE HISTORY` for the version before the change and `RESTORE TABLE … TO VERSION AS OF` that version, or `SELECT` from it to rebuild. Then review permissions so that only the pipeline's service principal can modify gold tables.

#### How do you make development cheaper for a team of ten engineers?

Use small or single-node clusters with policies and short auto-termination, serverless notebooks, shared dev data samples or shallow clones instead of full copies, local unit tests for most logic, development-mode bundles, and a budget alert per team.

#### How do you explain the lakehouse to a business stakeholder?

One place for all the company's data, stored once in open formats in the company's own cloud account, where reporting, data science and AI work on the same trusted numbers, with permissions and audit trails managed centrally.

#### A notebook works on your cluster but fails as a serverless job. Why?

Probably because it uses something unsupported on serverless (Spark Connect): RDDs, `sparkContext`, `cache()`, most `spark.conf.set` calls, init scripts or libraries that need the JVM. Rewrite with DataFrame APIs, declare dependencies in the environment, and test on serverless before deploying.

#### How do you share gold tables with a partner company that doesn't use Databricks?

With open Delta Sharing: create a share with the tables, create a recipient with a token-based credential, and the partner reads it from pandas, Spark or a BI tool. Access can be revoked at any time and is audited.

#### The monthly Databricks bill doubled. How do you investigate?

Query `system.billing.usage` by SKU, workspace, job, warehouse and tag, and compare months. Look for all-purpose clusters without auto-termination, jobs moved to all-purpose compute, warehouses that never stop, full refreshes, new serverless workloads and runaway retries.

#### How do you deliver a GDPR deletion request on a Delta lakehouse?

Delete the person's rows with `DELETE` or `MERGE` in every layer (bronze included), then run `VACUUM` so the old files containing them are physically removed after the retention period. Pseudonymizing identifiers early in the pipeline limits how many tables hold personal data.
