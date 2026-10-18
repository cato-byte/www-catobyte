## Amazon Athena Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Amazon Athena study guide: about 200 questions](../../images/aws_athena_study_guide_title_img.png)

About 200 interview-style questions on Amazon Athena: how serverless SQL on S3 works, tables and SerDes, partitions and partition projection, file formats, Iceberg tables, CTAS and `UNLOAD`, workgroups and cost control, performance tuning, federated queries, security and troubleshooting. The answers reflect the service as of 2026. Open a question to see its answer, or use the filter to search the whole guide.

<!-- QA -->

### Fundamentals

#### What is Amazon Athena?

A serverless, interactive query service that lets you analyze data directly in Amazon S3 (and other sources through connectors) with standard SQL. There is no infrastructure to manage: you define tables over your data, run queries and pay for the data scanned or for reserved capacity.

#### What engine does Athena use?

Athena's SQL engine version 3 is based on Trino (formerly PrestoSQL) with AWS-specific improvements, and DDL uses Hive-compatible syntax. Athena also offers Apache Spark through Athena notebooks for PySpark workloads.

#### What are typical use cases for Athena?

Ad hoc analysis of data lakes, querying logs (CloudTrail, VPC Flow Logs, ALB, CloudFront, S3 access logs), building lightweight ELT with `CTAS` and `INSERT INTO`, serving BI tools such as QuickSight, exploring data before building pipelines, and querying Iceberg tables in a lakehouse.

#### How is Athena priced?

By default, per terabyte of data scanned (about 5 USD per TB in many regions), with a 10 MB minimum per query, rounded up to the nearest megabyte. DDL statements and failed queries aren't charged. Capacity reservations offer a fixed price per DPU-hour instead. S3 storage, requests and Glue Data Catalog usage are billed separately.

#### Why does data format matter so much for Athena's cost?

Because you pay per byte scanned. Columnar, compressed formats (Parquet, ORC) let Athena read only the columns a query needs and skip blocks using statistics, often reducing scanned data by 90% or more compared with uncompressed CSV or JSON.

#### Where does Athena store table definitions?

In the AWS Glue Data Catalog (by default), or in an external Hive metastore, or in other catalogs registered as data sources (federated connectors, Redshift, S3 Tables catalogs).

#### Where do query results go?

To a query result location in S3 (set per workgroup or per query) as a CSV file plus a metadata file, or to managed query results storage that Athena keeps for you for a limited time. Results can be encrypted and should have a lifecycle rule to expire old files.

#### How does Athena compare with Amazon Redshift?

Athena is serverless and queries data in place on S3, ideal for ad hoc, intermittent or exploratory workloads, paying per query. Redshift is a data warehouse (provisioned or serverless) optimized for complex, frequent, high-concurrency analytics on data loaded into its managed storage, with features such as materialized views and workload management. Many architectures use both.

#### How does Athena compare with Redshift Spectrum?

Both query S3 data through the Glue Data Catalog. Spectrum runs from a Redshift cluster and lets you join S3 data with Redshift tables; Athena is standalone and serverless. Spectrum is useful when the warehouse already exists.

#### How does Athena compare with running Trino or Spark on EMR?

Athena removes cluster management and bills per query or capacity, but gives less control over configuration and resources. EMR suits very large, steady workloads, custom configurations or tools beyond SQL.

#### What is a workgroup?

A way to separate users, teams or applications: each workgroup has its own query result location, encryption settings, engine version, data usage limits, CloudWatch metrics and query history, and IAM can control who uses which workgroup.

#### What are the main Athena interfaces?

The console query editor, the AWS CLI and SDKs (`StartQueryExecution`, `GetQueryExecution`, `GetQueryResults`), JDBC and ODBC drivers for BI and SQL tools, Athena notebooks for Spark, and integrations with QuickSight, Glue, Step Functions and Airflow.

#### Is Athena ACID?

For Hive-style tables, no: queries read whatever files exist, and writes add files without transactions. For Apache Iceberg tables, yes: Athena supports ACID `INSERT`, `UPDATE`, `DELETE` and `MERGE` with snapshot isolation and time travel.

#### What is the query lifecycle in Athena?

The query is submitted (`QUEUED`), planned using catalog metadata and partition pruning, executed in parallel across Athena's managed compute reading from S3 (`RUNNING`), and finishes as `SUCCEEDED`, `FAILED` or `CANCELLED`, with results written to the result location.

#### What limits should you know about Athena?

Account-level quotas on concurrent active DML and DDL queries, a query timeout (30 minutes by default for DML, adjustable), query string length, the number of partitions a single query can add, and S3 request rates per prefix that can throttle very parallel scans.

#### What does "schema on read" mean in Athena?

The schema is applied when data is read, not when it's written: files in S3 can be written by any tool, and the table definition tells Athena how to interpret them at query time. It's flexible but means bad files only show up as errors or `NULL`s when queried.

#### What does "serverless" mean for Athena?

There are no clusters to size, start or patch: AWS runs a shared, multi-tenant query engine, allocates resources per query, and you pay per query (or per reserved capacity). There is nothing running when you aren't querying.

#### Which AWS services commonly feed data to Athena?

Kinesis Data Firehose (streams to S3), AWS Glue (ETL and catalog), AWS DMS (database replication to S3), AWS services writing logs to S3, S3 Inventory, and applications that write files directly.

#### Can Athena write data?

Yes: `CTAS`, `INSERT INTO`, `UNLOAD`, and full DML (`UPDATE`, `DELETE`, `MERGE`) on Iceberg tables. On Hive-style tables it can only add new files.

#### What are Athena engine versions, and how are they upgraded?

Athena evolves its engine in versions (v3 is current); workgroups can choose automatic upgrades or a specific version. Upgrades can change function behavior or type handling, so test critical queries before switching.

#### What is the Athena query editor's "saved query" feature?

Named queries stored per workgroup that users can reuse and share, which is useful for recurring analyses, though version control in Git is better for production SQL.

### Tables, DDL and SerDes

#### How do you create a table in Athena?

With `CREATE EXTERNAL TABLE`, giving columns, the S3 location, the format or SerDe, partition columns and table properties:

```sql
CREATE EXTERNAL TABLE logs.app_events (
  event_id   string,
  user_id    bigint,
  event_type string,
  payload    string,
  event_ts   timestamp
)
PARTITIONED BY (dt string)
STORED AS PARQUET
LOCATION 's3://my-lake/curated/app_events/'
TBLPROPERTIES ('parquet.compression' = 'SNAPPY');
```

#### Why are Athena tables "external"?

Athena only stores metadata; data stays in S3. Dropping an external table removes the definition but not the files (Iceberg tables are different: dropping them can delete data).

#### What is a SerDe?

A serializer/deserializer that tells Athena how to read and write a format: `LazySimpleSerDe` for delimited text, `OpenCSVSerDe` for quoted CSV, `JsonSerDe` (Hive or OpenX) for JSON, `RegexSerDe` and `GrokSerDe` for logs, and native readers for Parquet, ORC and Avro.

#### When do you use `OpenCSVSerDe` instead of `LazySimpleSerDe`?

When CSV fields are enclosed in quotes and may contain commas. `OpenCSVSerDe` handles quotes but treats every column as a string unless types are cast, and it has limitations with some types; `LazySimpleSerDe` is faster for simple delimited files.

#### How do you skip a header row in CSV files?

With the table property `'skip.header.line.count'='1'`.

#### How do you read JSON in Athena?

With a JSON SerDe, one JSON object per line. The OpenX SerDe offers options such as `ignore.malformed.json` and case-insensitive mapping. Nested objects map to `struct` and arrays to `array` types.

```sql
CREATE EXTERNAL TABLE raw.orders_json (
  order_id string,
  customer struct<id:bigint, country:string>,
  items array<struct<sku:string, qty:int, price:double>>
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES ('ignore.malformed.json' = 'true')
LOCATION 's3://my-lake/raw/orders/';
```

#### How do you query nested arrays?

With `UNNEST` in a `CROSS JOIN`, which produces one row per array element:

```sql
SELECT o.order_id, i.sku, i.qty
FROM raw.orders_json o
CROSS JOIN UNNEST(o.items) AS t(i);
```

#### How do you parse JSON stored as a string column?

With JSON functions such as `json_extract_scalar(payload, '$.customer.id')`, `json_extract`, `json_parse` and `CAST(json_parse(payload) AS map(varchar, json))`.

#### What happens if the data doesn't match the table schema?

Athena applies schema on read: mismatched values usually become `NULL` or cause errors such as `HIVE_BAD_DATA` (for example a string in an integer column, or a Parquet column type that doesn't match the table type).

#### Can Athena handle schema evolution?

For Parquet, adding columns at the end and reading by name works; renaming or changing types is risky. For CSV, columns are positional, so only appending columns at the end is safe. Iceberg tables support proper schema evolution (add, drop, rename, reorder, widen types).

#### What is a view in Athena?

A saved query (`CREATE VIEW`) stored in the catalog that you query like a table. It doesn't store data, so each query reads the underlying tables and is billed accordingly.

#### What does `MSCK REPAIR TABLE` do?

It scans the table's S3 location for Hive-style partition folders (`key=value`) and adds missing partitions to the catalog. It's slow on tables with many partitions; adding partitions explicitly or using partition projection is better.

#### What does `SHOW CREATE TABLE` do?

It prints the DDL of a table, useful to copy definitions between environments or to check SerDe and properties.

#### How do you query AWS service logs with Athena?

Create tables with the documented DDL for each log type (CloudTrail, VPC Flow Logs, ALB, CloudFront, S3 access logs), ideally with partition projection on date and region, then query them with SQL to investigate security events, traffic and errors.

#### How do you change a table's columns?

With `ALTER TABLE … ADD COLUMNS`, `REPLACE COLUMNS` or `CHANGE COLUMN` (behavior depends on the format), or by recreating the table. For Iceberg, `ALTER TABLE … ADD COLUMNS`, `DROP COLUMN` and `RENAME COLUMN` are safe metadata operations.

#### How does Athena map Parquet columns: by name or by position?

By name by default for Parquet, so column order in the table doesn't need to match the files. CSV and other text formats map by position.

#### What data types does Athena support?

`boolean`, `tinyint`, `smallint`, `int`, `bigint`, `double`, `float`, `decimal(p,s)`, `char`, `varchar`, `string`, `binary`, `date`, `timestamp`, and complex types `array`, `map` and `struct`.

#### How do you read files with a custom delimiter?

`ROW FORMAT DELIMITED FIELDS TERMINATED BY '|'` (or `\t` for TSV), with `ESCAPED BY` and `LINES TERMINATED BY` options when needed.

#### How do you query data using a regular expression?

Define a table with `RegexSerDe` and an `input.regex` property capturing groups for each column, useful for fixed-format logs; for ad hoc parsing, use `regexp_extract` on a single string column.

#### How do you query only certain files in a location?

Use the pseudo-column `"$path"` (the S3 path of each row's file) in a `WHERE` clause, which also helps debugging which file contains bad data.

```sql
SELECT "$path", count(*) FROM raw.app_events_csv GROUP BY 1 ORDER BY 2 DESC;
```

#### What other pseudo-columns exist?

`"$path"`, `"$file_size"` and `"$file_modified_time"` describe the source file of each row, useful for lineage, debugging and incremental processing.

### Partitions and partition projection

#### What is partitioning in Athena?

Organizing data in S3 by the values of one or more columns (`s3://bucket/table/dt=2026-10-15/`) and declaring them as partition columns, so queries filtering on them read only matching folders.

#### What is partition pruning?

The engine uses filters on partition columns to skip partitions that can't match, reducing data scanned. It only works when the filter is on the partition column itself, without functions that prevent evaluation at planning time.

#### How do you add partitions?

`ALTER TABLE t ADD PARTITION (dt='2026-10-15') LOCATION 's3://.../dt=2026-10-15/'`, `MSCK REPAIR TABLE` for Hive-style folders, a Glue crawler, the Glue API, or partition projection (no registration).

#### What is partition projection?

A table configuration where Athena computes partition values and locations from rules in table properties (ranges of dates or integers, enums, injected values) instead of reading them from the catalog. New partitions need no registration, and planning is faster for highly partitioned tables.

```sql
ALTER TABLE logs.app_events SET TBLPROPERTIES (
  'projection.enabled' = 'true',
  'projection.dt.type' = 'date',
  'projection.dt.range' = '2024-01-01,NOW',
  'projection.dt.format' = 'yyyy-MM-dd',
  'storage.location.template' = 's3://my-lake/curated/app_events/dt=${dt}/'
);
```

#### When is partition projection a bad fit?

When partition values are unpredictable (for example arbitrary customer IDs not known in advance, unless using `injected` type with mandatory filters), when other engines (EMR, Spark) also need partitions in the catalog, or when most projected partitions don't exist (Athena would probe many empty prefixes).

#### What is an injected projection type?

A projection type where the partition value must be provided in the query's `WHERE` clause (for example `customer_id = '123'`); Athena uses it to build the location. It suits high-cardinality keys always used as filters.

#### What is a good partitioning strategy?

Partition by the columns most queries filter on (usually date), at a granularity that keeps each partition reasonably large (at least tens of MB, ideally more), and avoid high-cardinality partition keys that create millions of tiny partitions.

#### What is the difference between Hive-style and non-Hive-style partition paths?

Hive-style paths contain `key=value` (`dt=2026-10-15/`), which `MSCK REPAIR` and crawlers understand. Non-Hive paths (`2026/10/15/`) need partitions added explicitly with a `LOCATION`, or partition projection with a storage location template.

#### What is bucketing in Athena?

Distributing data within partitions into a fixed number of files by hashing a column (`CLUSTERED BY (user_id) INTO 32 BUCKETS`), which helps queries that filter on that column skip files. It's mainly used with `CTAS`.

#### Why can too many partitions hurt performance?

Query planning has to fetch and evaluate partition metadata, and each partition usually means separate S3 listings and small files. Partition indexes in Glue or partition projection reduce the planning cost.

#### How do you check which partitions a table has?

`SHOW PARTITIONS table` lists registered partitions (not projected ones), and the Glue console or API shows partition locations and schemas.

#### How do you remove partitions?

`ALTER TABLE t DROP PARTITION (dt='2026-10-01')` removes catalog metadata only; delete the S3 objects separately if the data should go too.

#### Can you mix partition projection and catalog partitions?

When projection is enabled, Athena ignores partitions registered in the catalog for that table and only uses the projection rules. Other engines still see the catalog partitions.

#### How do you partition by date when the data contains timestamps?

Derive a date string (or year/month/day) at write time and store it as a partition column; with Iceberg, use hidden partitioning `day(event_ts)` so queries filter on the timestamp directly.

#### Why might a query not prune partitions even though it filters on the date?

The filter might apply a function to the partition column (for example `date(dt) = …` on a string column), compare with a type that requires casting, or filter on a different column than the partition key. Filter on the partition column with literal values of the same type.

### File formats and data layout

#### Which file formats does Athena support?

CSV/TSV and other delimited text, JSON, Parquet, ORC, Avro, Ion, logs via Regex or Grok SerDes, and open table formats Iceberg, Hudi (read) and Delta Lake (read).

#### Why are Parquet and ORC recommended?

They are columnar (read only needed columns), compressed per column, and store statistics (min/max per row group or stripe) that let Athena skip data. They also support predicate pushdown, which speeds up queries and cuts cost.

#### Which compression codecs work well?

Snappy and ZSTD for Parquet and ORC (fast, splittable within the format). For text files, gzip is common but not splittable, so one large gzip file is read by a single worker; bzip2 is splittable but slow.

#### What is the ideal file size for Athena?

Roughly 128 MB to 1 GB per file. Many small files (a few KB) add per-file overhead and S3 request costs; very large unsplittable files limit parallelism.

#### How do you fix a table made of many small files?

Compact them: run a `CTAS` or `INSERT INTO` that rewrites data into fewer larger files (with bucketing or a controlled partitioning), use `OPTIMIZE` on Iceberg tables, or fix the producer (larger batches, Firehose buffering).

#### How does sorting data help Athena?

When data is sorted (or clustered) by a commonly filtered column within files, Parquet and ORC statistics have tight min/max ranges, so more row groups can be skipped.

#### What does columnar projection mean for `SELECT *`?

With Parquet or ORC, selecting fewer columns scans fewer bytes, so `SELECT *` on a wide table costs much more than selecting the columns you need.

#### How do you convert CSV data to Parquet with Athena?

With `CTAS`:

```sql
CREATE TABLE curated.app_events
WITH (
  format = 'PARQUET',
  write_compression = 'ZSTD',
  external_location = 's3://my-lake/curated/app_events/',
  partitioned_by = ARRAY['dt']
) AS
SELECT event_id, user_id, event_type, event_ts, dt
FROM raw.app_events_csv;
```

#### Does Athena support S3 Express One Zone or S3 Tables?

Yes. Athena can query data in S3 Express One Zone directory buckets for lower latency, and can query and manage Iceberg tables in S3 Tables (table buckets) through their catalog integration.

#### What is predicate pushdown in Athena?

Filters are pushed to the file reader, which uses Parquet/ORC statistics to skip row groups or stripes whose min/max can't match, so less data is read and decompressed.

#### What row group size is good for Parquet?

Typically 128 MB to 512 MB row groups; larger row groups compress well and reduce overhead, but very large ones reduce the effectiveness of skipping. Writers such as Spark have sensible defaults.

#### Does compression reduce Athena costs?

Yes. Athena bills on compressed bytes scanned, so compressed files (and columnar encoding) directly reduce cost, besides reducing S3 storage.

#### What is the difference between Parquet and ORC for Athena?

Both are columnar with statistics and compression and work well. Parquet is the more common choice across the ecosystem (Spark, Iceberg defaults); ORC was historically favored by Hive. Choose based on the writers and other engines you use.

#### How do you handle data that arrives as one huge gzip file?

Since gzip isn't splittable, a single worker reads it. Split the file before or during ingestion, recompress as bzip2 or, better, convert to Parquet with a `CTAS` or a Glue job.

### Iceberg tables in Athena

#### What is Apache Iceberg, and why use it with Athena?

An open table format that adds a metadata layer (snapshots, manifests) on top of Parquet files, giving ACID transactions, schema and partition evolution, hidden partitioning, time travel and efficient row-level changes. Athena can create, read and write Iceberg tables registered in the Glue Data Catalog.

#### How do you create an Iceberg table in Athena?

```sql
CREATE TABLE lake.customers (
  customer_id bigint,
  email       string,
  country     string,
  updated_at  timestamp
)
PARTITIONED BY (country)
LOCATION 's3://my-lake/iceberg/customers/'
TBLPROPERTIES ('table_type' = 'ICEBERG', 'format' = 'parquet');
```

#### Which DML statements does Athena support on Iceberg?

`INSERT INTO`, `UPDATE`, `DELETE` and `MERGE INTO`, plus `CREATE TABLE AS SELECT` into Iceberg, `OPTIMIZE … REWRITE DATA` and `VACUUM` for maintenance.

```sql
MERGE INTO lake.customers t
USING staging.customer_changes s ON t.customer_id = s.customer_id
WHEN MATCHED AND s.op = 'D' THEN DELETE
WHEN MATCHED THEN UPDATE SET email = s.email, country = s.country, updated_at = s.updated_at
WHEN NOT MATCHED THEN INSERT (customer_id, email, country, updated_at)
  VALUES (s.customer_id, s.email, s.country, s.updated_at);
```

#### What is hidden partitioning in Iceberg?

Partitions defined as transforms of columns (`day(event_ts)`, `bucket(16, user_id)`, `truncate(10, sku)`), so queries filter on the original column (`event_ts`) and Iceberg prunes partitions automatically; users don't need to know about partition columns.

#### How does time travel work for Iceberg in Athena?

```sql
SELECT * FROM lake.customers FOR TIMESTAMP AS OF TIMESTAMP '2026-10-15 08:00:00 UTC';
SELECT * FROM lake.customers FOR VERSION AS OF 949530903748831860;
```

You can also inspect metadata tables such as `"customers$snapshots"`, `"customers$history"`, `"customers$files"` and `"customers$partitions"`.

#### What do `OPTIMIZE` and `VACUUM` do on Iceberg tables?

`OPTIMIZE table REWRITE DATA USING BIN_PACK` compacts small files and merges delete files into data files. `VACUUM` expires old snapshots and removes files no longer referenced (according to retention properties), freeing storage.

#### How do row-level deletes work in Iceberg on Athena?

Athena writes position delete files (merge-on-read) that mark deleted rows instead of rewriting data files. Reads merge them on the fly, so tables with many deletes need regular `OPTIMIZE` to stay fast.

#### Can you evolve an Iceberg table's partitioning?

Yes. You can change the partition spec (for example from monthly to daily) without rewriting old data; old files keep the old spec and new data uses the new one, and queries handle both.

#### Iceberg or Hive-style tables in Athena: how do you choose?

Iceberg when you need updates, deletes, upserts (CDC, GDPR deletions), schema evolution, concurrent writers, or time travel. Hive-style Parquet is simpler for immutable append-only data written by other tools. New lakehouse designs usually choose Iceberg.

#### Can other engines use the same Iceberg tables?

Yes. Spark on EMR or Glue, Trino, Flink, Snowflake, Databricks and others can read and write the same Iceberg tables through the Glue Data Catalog or an Iceberg REST catalog, which avoids engine lock-in.

#### What table properties matter for Iceberg in Athena?

`format` (parquet, orc, avro), `write_compression`, `optimize_rewrite_delete_file_threshold`, `vacuum_max_snapshot_age_seconds`, `vacuum_min_snapshots_to_keep` and `vacuum_max_metadata_files_to_keep`, which control file layout and retention.

#### Can multiple writers modify an Iceberg table at the same time?

Yes, with optimistic concurrency: each commit checks the table's current version, and conflicting commits fail and must retry. Avoid many concurrent writers updating the same partitions.

#### How do you add a column to an Iceberg table?

`ALTER TABLE lake.customers ADD COLUMNS (segment string)`. Existing files aren't rewritten; old rows return `NULL` for the new column.

#### How do you roll back an Iceberg table in Athena?

Read the previous version with time travel and rewrite it (for example `CTAS` from `FOR VERSION AS OF`), or use an engine with rollback procedures (Spark's `rollback_to_snapshot`) on the same table.

#### What are S3 Tables?

S3 table buckets that store Iceberg tables with built-in maintenance (compaction, snapshot management) and a catalog integration, which Athena can query and write like other Iceberg tables.

### CTAS, INSERT and UNLOAD

#### What is `CTAS`?

`CREATE TABLE AS SELECT`: creates a new table from a query's results, writing files in the chosen format, compression, partitioning and bucketing to S3. It's used to convert formats, build aggregates and materialize transformations.

#### What are the limits of `CTAS` and `INSERT INTO`?

A single query can create or insert into a limited number of partitions (100 per query for Hive tables), so large backfills need several statements or loops by partition ranges. Iceberg tables don't have this specific limit.

#### What does `INSERT INTO` do on a Hive-style table?

It appends new files to the table's location (and registers new partitions). It never modifies existing files, so rerunning it duplicates data unless you first delete the target partition's files.

#### How do you make Athena ELT idempotent?

For Hive tables, write each run's output to a partition and delete or overwrite that partition before rerunning (often by writing to a new location and swapping the partition location). For Iceberg tables, use `MERGE` or `DELETE` plus `INSERT` in the same logic, or `INSERT OVERWRITE`-style patterns with Iceberg.

#### What does `UNLOAD` do?

It writes query results to S3 in a chosen format (Parquet, ORC, Avro, JSON, text) with optional partitioning and compression, without creating a table, which is useful for exports to other systems.

```sql
UNLOAD (SELECT * FROM curated.app_events WHERE dt = '2026-10-15')
TO 's3://exports/app_events/dt=2026-10-15/'
WITH (format = 'PARQUET', compression = 'SNAPPY');
```

#### How do you schedule Athena queries?

With EventBridge Scheduler or Step Functions calling `StartQueryExecution`, Airflow's `AthenaOperator`, dbt with the dbt-athena adapter, or a Lambda function on a schedule.

#### Can you use dbt with Athena?

Yes, with the dbt-athena adapter: models materialize as views, tables (`CTAS`), incremental models (`insert_overwrite` by partition, `append`, or `merge` on Iceberg) and Iceberg tables, with Glue as the catalog.

#### What are prepared statements and parameterized queries?

Statements created with `PREPARE` (or passed with `ExecutionParameters`) that contain `?` placeholders filled at execution, which avoids SQL injection and lets applications reuse query text.

```sql
PREPARE events_by_day FROM
SELECT event_type, count(*) FROM curated.app_events WHERE dt = ? GROUP BY 1;

EXECUTE events_by_day USING '2026-10-15';
```

#### How do you create an empty copy of a table's schema?

`CREATE TABLE new_t WITH (...) AS SELECT * FROM t WITH NO DATA`, which creates the table definition without writing rows.

#### How do you control the number of output files in `CTAS`?

With `bucketed_by` and `bucket_count`, which fix the number of files per partition, or by reducing parallelism of the final stage; otherwise Athena writes as many files as workers produce.

#### Can a `CTAS` write to an existing S3 location?

No. The `external_location` must be empty, which prevents overwriting data by mistake. Delete or use a new location for reruns.

#### How do you export query results as a single CSV?

Run the query and download the result file from the result location (Athena writes one CSV per query), or use `UNLOAD` with a text format; very large results may be split across files with `UNLOAD`.

### Performance tuning

#### What are the main ways to make Athena queries faster and cheaper?

Use columnar formats with compression, partition by common filters (or partition projection), keep files 128 MB–1 GB, select only needed columns, filter on partition columns, sort or bucket by common filters, use Iceberg with compaction, compute table statistics, and reuse query results.

#### How do you see how much data a query scanned?

In the console after running, in `GetQueryExecution` statistics (`DataScannedInBytes`), in CloudWatch workgroup metrics, and in `EXPLAIN ANALYZE` output per stage.

#### What do `EXPLAIN` and `EXPLAIN ANALYZE` show?

`EXPLAIN` shows the distributed or logical plan without running the query: scans, filters pushed down, joins and their distribution. `EXPLAIN ANALYZE` runs the query and reports actual rows, data read and time per stage, which shows where time goes.

#### How should you order tables in a join?

Engine v3 has a cost-based optimizer that can reorder joins when table statistics exist in the Glue catalog. Without statistics, put the largest table first (left) and smaller tables on the right, since the right side is built into memory and distributed to workers.

#### What are join distribution types?

Broadcast joins send the small right-side table to all workers (fast if it's small); partitioned joins hash both sides across workers (needed for two large tables). The optimizer chooses based on statistics.

#### Why does `ORDER BY` without `LIMIT` hurt performance?

A global sort requires sending all rows to a single worker for the final ordering, which is slow and can fail with "exceeded resources". Add a `LIMIT` (top-N is efficient) or sort only what's needed.

#### What is "Query exhausted resources at this scale factor"?

An error when a query needs more memory than available for an operation (huge joins, `GROUP BY` with many groups, `DISTINCT` on many columns, `ORDER BY` of everything, very large arrays). Fixes: filter earlier, reduce columns, approximate functions, split the query, use `CTAS` to materialize intermediate steps, or use capacity reservations.

#### When should you use approximate functions?

`approx_distinct`, `approx_percentile` and `approx_most_frequent` return estimates with small errors using much less memory than exact `count(DISTINCT)` or percentiles, which suits dashboards and exploration.

#### What is query result reuse?

A feature where Athena returns a previous query's results if the same query was run recently (within a maximum age you set, up to 7 days) and the underlying data hasn't changed (for supported tables), without scanning data again.

#### How do table statistics help Athena?

Column statistics stored in the Glue catalog (computed by Glue) let the cost-based optimizer choose join order and distribution, improving complex queries without code changes.

#### How do you speed up `LIKE` searches on large text columns?

Filter on partitions first, use `regexp_like` only when needed, and consider pre-extracting searchable fields into separate columns during ETL, or a search service such as OpenSearch for full-text needs.

#### Why can S3 throttling slow Athena queries?

S3 supports high request rates per prefix, but queries over millions of small files in one prefix can hit `SlowDown` (503) errors. Fewer, larger files and spreading data across prefixes (partitions) avoid it.

#### What are capacity reservations?

Dedicated query processing capacity bought in DPUs (for a minimum duration, then per minute) and assigned to workgroups. Queries in those workgroups run on the reserved capacity, billed per DPU-hour instead of per TB scanned, with predictable cost and concurrency.

#### When are capacity reservations worth it?

When query volume is high and steady (heavy BI dashboards, many concurrent users), when you need guaranteed concurrency for critical workloads, or when per-TB costs exceed the reserved capacity price.

#### Why does `count(DISTINCT x)` on a huge table fail or run slowly?

It requires keeping all distinct values in memory across workers. Use `approx_distinct(x)` for estimates, or pre-aggregate distinct counts by partition and combine.

#### How do window functions affect Athena performance?

Window functions partition and sort data; a window over the whole table (no `PARTITION BY`) forces a single worker. Always partition windows by a key and filter data first.

#### What is the effect of `UNION` versus `UNION ALL`?

`UNION` removes duplicates, which needs an extra aggregation step; `UNION ALL` just concatenates. Use `UNION ALL` when duplicates are impossible or acceptable.

#### How do you optimize queries on a large, frequently queried dimension combination?

Precompute aggregates in a summary table (`CTAS` or scheduled `INSERT`), keep it partitioned by date, and point dashboards to it instead of the raw table.

#### How does `LIMIT` affect cost?

On Hive-style tables a `LIMIT` without filters may stop early but can still scan many files; it doesn't guarantee low cost. Partition filters are the reliable way to limit scanning.

#### What is the impact of data skew on Athena joins and aggregations?

A few keys holding most rows overload single workers and can cause "exhausted resources" errors. Filter out hot keys (often nulls), handle them separately, or use approximate aggregations.

### Workgroups, cost control and monitoring

#### How do you limit costs per team?

Create a workgroup per team or application with a per-query data usage limit (cancels queries scanning more than a threshold) and workgroup-wide limits per period that trigger alarms, enforce workgroup settings so users can't override them, and tag workgroups for cost allocation.

#### What does "override client-side settings" mean for a workgroup?

When enabled, the workgroup's result location, encryption and other settings apply to every query, ignoring what clients specify, which enforces governance.

#### How do you monitor Athena usage?

With CloudWatch metrics per workgroup (data scanned, query duration, queued time, failed queries), query history (`ListQueryExecutions`, console), CloudTrail for API calls, and cost reports with tags.

#### How long is query history kept?

Athena keeps query history for 45 days. For longer retention or analysis, export execution details (for example with EventBridge events or a scheduled job calling `GetQueryExecution`) to S3.

#### How do you find the most expensive queries?

From query history or exported execution data, sort by `DataScannedInBytes`; then check whether they filter on partitions, read CSV or JSON, or select too many columns.

#### How do you prevent runaway queries?

Per-query data usage limits in workgroups, query timeouts, education on partition filters, views that require partition filters, and capacity reservations for predictable workloads.

#### How are Athena costs affected by S3 requests?

Athena's per-TB price doesn't include S3 GET and LIST requests, which are billed by S3. Tables with huge numbers of small files can generate significant request costs on top of Athena charges.

#### What is the difference between a per-query limit and a workgroup-wide limit?

A per-query control cancels any query scanning more than the threshold. Workgroup-wide controls measure total data scanned over a period and trigger CloudWatch alarms or SNS notifications, but don't cancel queries.

#### How do you allocate Athena costs to teams?

Use separate workgroups per team, tag them with cost allocation tags, and analyze costs in Cost Explorer by tag; for capacity reservations, assign workgroups to reservations per team.

#### How do you track query failures?

CloudWatch metrics for failed queries per workgroup, EventBridge "Athena Query State Change" events routed to alerts, and query history with error messages.

### Federated queries and connectors

#### What is Athena Federated Query?

A feature that lets Athena query data outside S3, such as DynamoDB, RDS and Aurora (MySQL, PostgreSQL), Redshift, DocumentDB, OpenSearch, CloudWatch Logs, Snowflake, BigQuery and many others, through data source connectors that run as AWS Lambda functions (or as managed Glue connections).

#### How do federated connectors work?

The connector Lambda receives part of the query plan, reads data from the source (with filters and projections pushed down when possible) and returns it in Apache Arrow format to Athena, which then joins and aggregates it with other data.

#### What are the downsides of federated queries?

Performance depends on the source and the Lambda (timeouts, memory, concurrency), queries can load operational databases, pushdown is limited for some sources, and you pay for Lambda plus data scanned. For frequent heavy use, replicate the data to S3.

#### How do you join S3 data with an RDS table?

Register the RDS connector as a data source (for example `rds_pg`), then query `SELECT … FROM lake.orders o JOIN rds_pg.public.customers c ON o.customer_id = c.id`, keeping the RDS side small with filters.

#### What are user-defined functions in Athena?

Scalar functions implemented in a Lambda function (Java) and called with `USING EXTERNAL FUNCTION`, used for logic not available in SQL, such as calling an internal service or custom decryption.

#### Can Athena call machine learning models?

Yes, with `USING EXTERNAL FUNCTION … SAGEMAKER 'endpoint-name'`, which sends rows to a SageMaker endpoint for inference within a query.

#### How do you deploy a federated connector?

From the Athena console (creating a data source), which deploys the connector Lambda from the AWS Serverless Application Repository or uses Glue connections, with a spill bucket in S3 for large results and the right IAM and VPC settings.

#### What is the spill bucket for?

An S3 location where the connector writes data that exceeds Lambda's response size limits, which Athena then reads. It should be encrypted and have a lifecycle rule.

#### How do you query DynamoDB with Athena?

With the DynamoDB connector, which scans or queries the table (consuming read capacity); for large analytical queries, export the table to S3 (DynamoDB export) and query the export instead.

#### Can you write a custom connector?

Yes, with the Athena Query Federation SDK (Java), implementing metadata and record handlers for your source, deployed as a Lambda function.

### Security and governance

#### How do you control access to Athena?

IAM policies on Athena actions and workgroups, S3 permissions on data and result locations, Glue Data Catalog permissions (databases, tables), and, for fine-grained control, Lake Formation permissions on databases, tables, columns, rows and cells.

#### How does Lake Formation work with Athena?

Athena checks Lake Formation permissions for the caller and only returns allowed columns and rows, using temporary credentials vended by Lake Formation to read S3, so users don't need direct S3 access to the data.

#### How do you encrypt Athena data?

Data in S3 can be encrypted with SSE-S3, SSE-KMS or client-side KMS; Athena reads encrypted data transparently with the right KMS permissions. Query results can be encrypted (SSE-S3, SSE-KMS, CSE-KMS) per workgroup, and data in transit uses TLS.

#### How do you restrict which S3 data a user can query?

Grant table access through Lake Formation (no direct S3 permissions needed), or with IAM limit S3 access to specific prefixes and Glue access to specific databases and tables.

#### How do you query data in another AWS account?

Through Lake Formation cross-account sharing (resource links), cross-account Glue catalog access registered as a data source, or bucket policies granting the querying role access to the data and its KMS key.

#### How do you audit Athena usage?

CloudTrail records API calls (who started which query, with the query text), Lake Formation logs data access, and S3 server access logs or CloudTrail data events record object reads.

#### How do you use Athena from a private network?

Through VPC interface endpoints for Athena (and for Glue, S3 and KMS as needed), so traffic doesn't traverse the internet; endpoint policies can restrict usage.

#### What is Lake Formation's data filter?

A definition of row and cell-level security for a table (a row filter expression plus included or excluded columns) granted to principals; Athena enforces it at query time.

#### How do you give a BI tool access to Athena securely?

Create a dedicated IAM role or user (preferably federated with IAM Identity Center or OAuth for the driver), limited to one workgroup, the needed tables via Lake Formation, and the result location, and connect through the JDBC/ODBC driver.

#### How do you mask sensitive columns in Athena?

Exclude them through Lake Formation column permissions, provide views that hash or redact them, or store masked copies in a separate curated table for broad access.

### Spark in Athena and notebooks

#### What is Amazon Athena for Apache Spark?

A serverless Spark offering in Athena where you run PySpark and Spark SQL in notebooks or through APIs, with fast start-up and billing per DPU-hour, for workloads that need more than SQL.

#### When would you use Athena Spark instead of Athena SQL?

For complex transformations in Python, machine learning preparation, iterative exploration with DataFrames, or logic that's awkward in SQL; SQL remains simpler and cheaper for most analytics.

#### How do Athena Spark sessions bill?

Per DPU-hour of the session's compute, with automatic scaling of executors and idle timeouts that end the session.

#### How does Athena Spark access the Data Catalog?

Spark sessions in Athena use the Glue Data Catalog by default, so you can read and write catalog tables (including Iceberg) with Spark SQL or DataFrames.

#### What languages are supported in Athena notebooks?

PySpark and Spark SQL (with magics), with common Python libraries available and the ability to add others to the session.

### Troubleshooting

#### A query returns zero rows but the files exist. What do you check?

Whether partitions are registered (or projection is configured correctly), whether the `LOCATION` and storage location template match the real paths, whether the SerDe and columns match the format, and whether files are in subfolders that the table doesn't include.

#### What does `HIVE_PARTITION_SCHEMA_MISMATCH` mean?

A partition's schema in the catalog differs from the table's schema (types or columns). Make partitions inherit the table schema (crawler setting or recreating partitions) and stabilize the source.

#### What does `HIVE_CURSOR_ERROR` usually indicate?

A problem reading a file: corrupted or truncated files, a format different from the table definition, an unreadable compressed file, or permissions or KMS issues on some objects.

#### What does `HIVE_BAD_DATA` mean?

A value can't be parsed as the declared type, for example text in a numeric column, a malformed JSON record, or a Parquet type mismatch. Fix the data, the table types, or use `TRY_CAST` over string columns.

#### Why do you get `Access Denied` on a query?

Missing permissions on the S3 data, the query result location, the KMS key, the Glue catalog objects, Lake Formation grants, or the workgroup. The error message usually names the resource.

#### Why does a query on timestamps return wrong results?

Timestamps stored as strings in different formats, time zone confusion (Athena timestamps without time zone are interpreted as UTC in many cases), or Parquet timestamp encodings that differ between writers. Parse explicitly with `from_iso8601_timestamp` or `parse_datetime` and convert time zones with `AT TIME ZONE`.

#### A query is slow but scans little data. What could cause it?

Planning time on tables with many partitions (use projection or partition indexes), many tiny files (per-file overhead), a federated source, queuing behind concurrency limits, or an expensive operation such as a large join or global sort.

#### Results contain duplicates after a pipeline rerun. Why?

The pipeline used `INSERT INTO` on a Hive table without removing the previous output, or files were written twice to the same location. Make writes idempotent (overwrite partitions, use Iceberg `MERGE`) and deduplicate the affected partitions.

#### Why does `MSCK REPAIR TABLE` add no partitions?

The folders aren't Hive-style (`key=value`), the key names don't match the partition column names (case matters), the location is wrong, or partition projection is enabled for the table.

#### Why do numbers show up as `NULL` from a CSV table?

Values contain characters that don't parse (thousand separators, currency symbols, quotes with `LazySimpleSerDe`, empty strings), or columns are shifted because a field contains the delimiter. Use `OpenCSVSerDe`, clean the data, or read as strings and `TRY_CAST`.

#### Why do you get "Query timeout"?

The query exceeded the workgroup's timeout: scanning too much data, a heavy join or sort, or a slow federated source. Optimize the query or data layout, materialize intermediate steps, or raise the timeout quota.

#### Why are there "too many open files" or S3 `SlowDown` errors?

Tables with an enormous number of small files cause many concurrent S3 requests. Compact the files and spread them across partitions.

#### Why does an Iceberg query get slower over time?

Many small files and delete files accumulate with frequent writes and row-level changes. Schedule `OPTIMIZE` and `VACUUM` (or use automatic compaction in the Glue catalog or S3 Tables).

### SQL functions and patterns

#### How do you work with dates and times in Athena?

With functions like `current_date`, `date_add('day', -1, current_date)`, `date_diff('day', a, b)`, `date_trunc('month', ts)`, `date_format(ts, '%Y-%m-%d')`, `from_iso8601_timestamp(s)`, `parse_datetime(s, 'yyyy-MM-dd HH:mm')` and `ts AT TIME ZONE 'America/Bogota'`.

#### How do you safely convert types?

`TRY_CAST(x AS integer)` returns `NULL` instead of failing on bad values, and `try()` wraps expressions that may error. Use them on raw string data.

#### How do you deduplicate rows in Athena?

With `row_number()` over the key ordered by a timestamp, keeping the first row per key, in a subquery or CTE, since Athena doesn't support `QUALIFY`.

#### How do you pivot data in Athena?

With conditional aggregation, since there's no `PIVOT` keyword: `sum(CASE WHEN month = 1 THEN amount END) AS jan`, or `map_agg` to build a key-value map.

#### What are useful array and map functions?

`cardinality`, `contains`, `element_at`, `array_join`, `array_agg`, `filter`, `transform`, `reduce`, `map_keys`, `map_values` and `map_agg`, which let you work with nested data without exploding it.

#### How do you compute a running total or moving average?

With window functions: `sum(amount) OVER (PARTITION BY customer ORDER BY dt ROWS UNBOUNDED PRECEDING)` for running totals and `avg(amount) OVER (ORDER BY dt ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)` for a 7-row moving average.

#### How do you generate a date series in Athena?

With `sequence` and `UNNEST`: `SELECT d FROM UNNEST(sequence(date '2026-01-01', date '2026-12-31', interval '1' day)) AS t(d)`, useful for filling gaps in time series.

#### How do you get the top N rows per group?

Use `row_number()` or `rank()` over the group ordered by the metric in a subquery, and filter on the rank in the outer query; `max_by(x, y)` gives the value of `x` at the maximum `y` per group.

#### What are `max_by` and `min_by` useful for?

Returning the value of one column at the row where another column is maximal or minimal, for example the latest status per order: `max_by(status, updated_at)`, without a window function.

#### How do you do geospatial queries in Athena?

With geospatial functions such as `ST_Point`, `ST_Contains`, `ST_Distance`, `ST_Within`, `ST_GeometryFromText` and `great_circle_distance`, for example to count events inside polygons.

#### How do you hash values for pseudonymization?

With `to_hex(sha256(to_utf8(email)))` (preferably with a secret salt or HMAC via `hmac_sha256`), producing stable pseudonyms that can still be joined.

#### How do you write reusable SQL logic in Athena?

With views for shared logic, CTEs (`WITH`) for readability within a query, SQL UDF-like patterns through views, and dbt macros when using dbt-athena.

#### How do you compare two tables to find differences?

With `EXCEPT` in both directions (`SELECT * FROM a EXCEPT SELECT * FROM b`) for row differences, or a full outer join on the key comparing columns, useful for validating migrations.

#### How do you sample data in Athena?

`TABLESAMPLE BERNOULLI (1)` reads rows with 1% probability (but still scans all data), and `TABLESAMPLE SYSTEM (1)` samples at file or split level, which can reduce data scanned.

#### How do you handle `NULL` values in aggregations and comparisons?

Aggregations ignore `NULL`s (except `count(*)`); comparisons with `NULL` return `NULL`, so use `IS NULL`, `coalesce`, `IS DISTINCT FROM` for null-safe comparison, and be careful with `NOT IN` on columns that contain nulls.

### Scenarios

#### Design a cheap log analytics solution with Athena.

Deliver logs to S3 with Firehose (buffered, converted to Parquet, partitioned by date), define a table with partition projection on date, create views for common questions, set up a workgroup with data limits, and give analysts access via Lake Formation. Add lifecycle rules to move old logs to cheaper storage classes.

#### Your Athena bill doubled. How do you investigate?

Check CloudWatch data scanned per workgroup, find top queries by bytes scanned in query history, look for new dashboards running unfiltered queries, `SELECT *` on wide tables, tables in CSV or JSON, and partition filters that stopped working (for example a function on the partition column). Then fix formats and filters and add per-query limits.

#### Analysts need to delete individual customers' data for GDPR. How do you support it on Athena?

Store the data in Iceberg tables, run `DELETE FROM … WHERE customer_id = …` across affected tables, then `OPTIMIZE` and `VACUUM` to physically remove old files after the snapshot retention period. With Hive tables, you'd have to rewrite whole partitions.

#### How would you build a small ELT pipeline only with Athena?

Raw tables over landing files, `CTAS` or `INSERT INTO` (or dbt-athena models) to build cleaned Iceberg or Parquet tables, `MERGE` for upserts, data quality checks as SQL queries that fail the pipeline when they return rows, and Step Functions or Airflow to schedule and order the statements.

#### A QuickSight dashboard on Athena is slow and expensive. What do you change?

Pre-aggregate into a summary table refreshed on a schedule, use QuickSight SPICE to cache data, ensure partition filters are applied by the dashboard, convert source tables to Parquet or Iceberg with compaction, and consider capacity reservations for predictable concurrency.

#### A table has 2 million small JSON files per day. What do you recommend?

Fix the producer to batch records (Firehose buffering, larger writes), add a compaction step that converts each day to a handful of Parquet files (Glue job or `CTAS`), and query the compacted table; keep the raw JSON only as an archive.

#### How do you query the latest state of a table that receives CDC records?

Either maintain an Iceberg table with `MERGE` applying the changes (the cleanest), or, on an append-only change table, use `ROW_NUMBER()` over each key ordered by change timestamp and keep the latest non-deleted row in a view.

```sql
SELECT * FROM (
  SELECT *, row_number() OVER (PARTITION BY customer_id ORDER BY change_ts DESC) AS rn
  FROM raw.customer_changes
) WHERE rn = 1 AND op <> 'D';
```

#### How would you explain Athena to a business stakeholder?

It lets the team ask questions in SQL directly of the files the company already stores in S3, without setting up or paying for servers, paying only for the data each question reads.

#### How do you migrate reports from an on-premises SQL Server to Athena?

Export tables to S3 as Parquet (DMS or exports), define Glue tables or Iceberg tables, translate T-SQL to Trino SQL (functions, date handling, `TOP` to `LIMIT`, no `PIVOT`), recreate views, validate results by comparing aggregates, and connect the BI tool via the driver.

#### A team needs ad hoc SQL access to a 50 TB data lake with tight budget control. What do you set up?

Lake Formation permissions by domain, a workgroup per team with per-query limits, Parquet or Iceberg tables partitioned by date, views that enforce partition filters, query result reuse, documentation of tables, and monthly reports of bytes scanned per team.

#### How would you build near-real-time dashboards on Athena?

Stream events with Firehose to S3 in Parquet with short buffers, partition by date and hour with projection, build small aggregate tables every few minutes with scheduled `INSERT INTO` or `MERGE` into Iceberg, and point dashboards to the aggregates; for sub-minute latency, use a different store such as OpenSearch or a streaming database.
