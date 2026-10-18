## Amazon Athena Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Amazon Athena study guide: about 200 questions](../../images/aws_athena_study_guide_title_img.png)

About 200 interview-style questions on Amazon Athena: how serverless SQL on S3 works, tables and SerDes, partitions and partition projection, file formats, Iceberg tables, CTAS and `UNLOAD`, workgroups and cost control, performance tuning, federated queries, security and troubleshooting. The answers reflect the service as of 2026.

The guide follows a learning path in five stages. Each section is split into short units: learning goals, a concept explanation and a worked example, then questions (recall first, then application), a practical challenge and key takeaways. To **learn**, read each unit top to bottom. To **review**, switch to review mode or use "Skip to questions", mark answers you want to see again, and try a mixed review across sections.

<!-- QA -->
<!-- stage: Foundations -->

### Fundamentals

<!-- unit: Serverless SQL on S3 -->

<!-- goals -->

- Explain what Athena is, what engine it runs and what it is used for.
- Describe schema on read and what "serverless" removes from your work.

<!-- concept -->

Most companies already keep their raw data as files in S3. Athena lets you query those files with SQL without loading them anywhere first. Two ideas make that possible. Schema on read: a table is just a description laid over files, applied when you query, so any tool can write the files. Serverless: AWS runs a shared Trino-based engine, so there is no cluster to size or idle.

The trade-off is that the engine can only be as efficient as the files you give it.

<!-- example -->

```sql
-- files written by Firehose; no load step, just a table definition
SELECT status, count(*) AS requests
FROM logs.alb_access
WHERE day = '2026-10-17'
GROUP BY status
ORDER BY requests DESC;
```

#### What is Amazon Athena?

A serverless, interactive query service that lets you analyze data directly in Amazon S3 (and other sources through connectors) with standard SQL. There is no infrastructure to manage: you define tables over your data, run queries and pay for the data scanned or for reserved capacity.

#### What engine does Athena use?

Athena's SQL engine version 3 is based on Trino (formerly PrestoSQL) with AWS-specific improvements, and DDL uses Hive-compatible syntax. Athena also offers Apache Spark through Athena notebooks for PySpark workloads.

#### What are typical use cases for Athena?

Ad hoc analysis of data lakes, querying logs (CloudTrail, VPC Flow Logs, ALB, CloudFront, S3 access logs), building lightweight ELT with `CTAS` and `INSERT INTO`, serving BI tools such as QuickSight, exploring data before building pipelines, and querying Iceberg tables in a lakehouse.

#### What does "serverless" mean for Athena?

There are no clusters to size, start or patch: AWS runs a shared, multi-tenant query engine, allocates resources per query, and you pay per query (or per reserved capacity). There is nothing running when you aren't querying.

#### What does "schema on read" mean in Athena?

The schema is applied when data is read, not when it's written: files in S3 can be written by any tool, and the table definition tells Athena how to interpret them at query time. It's flexible but means bad files only show up as errors or `NULL`s when queried.

#### Which AWS services commonly feed data to Athena?

Kinesis Data Firehose (streams to S3), AWS Glue (ETL and catalog), AWS DMS (database replication to S3), AWS services writing logs to S3, S3 Inventory, and applications that write files directly.

#### How would you explain Athena to a business stakeholder?

It lets the team ask questions in SQL directly of the files the company already stores in S3, without setting up or paying for servers, paying only for the data each question reads.

<!-- challenge -->

A team asks whether Athena can replace their nightly job that loads S3 logs into a database just to run a few weekly queries. What do you answer?

<!-- solution -->

Probably yes: define a table over the logs and query them in place, paying only when queries run. Convert the logs to partitioned Parquet if the weekly queries scan a lot, so cost stays low.

<!-- takeaways -->

- Athena queries files in S3 directly with SQL.
- Schema on read: tables describe files; nothing is loaded.
- Serverless means no clusters, but file layout still matters.

<!-- unit: Pricing and query execution -->

<!-- goals -->

- Explain how Athena is billed and why file format drives cost.
- Follow a query from submission to results and know the main limits.

<!-- concept -->

Athena's default price is per byte scanned, which links cost directly to how much of each file a query must read. Formats that let the engine skip columns and row groups therefore cut both cost and time. Every query goes through the same path: queue, planning with catalog metadata, parallel scanning, and results written to S3.

Quotas on concurrency and a timeout bound that path, so very large or very many queries need a different design, not just patience.

<!-- example -->

| Same 100 GB of events | Bytes scanned for 3 columns | Approx. cost at 5 USD/TB |
|---|---|---|
| CSV, uncompressed | 100 GB | 0.50 USD |
| Parquet + Snappy | ~4 GB | 0.02 USD |

#### How is Athena priced?

By default, per terabyte of data scanned (about 5 USD per TB in many regions), with a 10 MB minimum per query, rounded up to the nearest megabyte. DDL statements and failed queries aren't charged. Capacity reservations offer a fixed price per DPU-hour instead. S3 storage, requests and Glue Data Catalog usage are billed separately.

#### Why does data format matter so much for Athena's cost?

Because you pay per byte scanned. Columnar, compressed formats (Parquet, ORC) let Athena read only the columns a query needs and skip blocks using statistics, often reducing scanned data by 90% or more compared with uncompressed CSV or JSON.

#### Where do query results go?

To a query result location in S3 (set per workgroup or per query) as a CSV file plus a metadata file, or to managed query results storage that Athena keeps for you for a limited time. Results can be encrypted and should have a lifecycle rule to expire old files.

#### What is the query lifecycle in Athena?

The query is submitted (`QUEUED`), planned using catalog metadata and partition pruning, executed in parallel across Athena's managed compute reading from S3 (`RUNNING`), and finishes as `SUCCEEDED`, `FAILED` or `CANCELLED`, with results written to the result location.

#### What limits should you know about Athena?

Account-level quotas on concurrent active DML and DDL queries, a query timeout (30 minutes by default for DML, adjustable), query string length, the number of partitions a single query can add, and S3 request rates per prefix that can throttle very parallel scans.

<!-- challenge -->

A dashboard runs one query every minute over a 2 TB CSV table. Estimate the monthly scan cost and name the first fix.

<!-- solution -->

About 2 TB × 43,200 queries ≈ 86 PB scanned, roughly 430,000 USD a month. Convert to partitioned Parquet and filter by date so each query scans megabytes; then cache results or pre-aggregate.

<!-- takeaways -->

- You pay per byte scanned, so layout is cost.
- Queries queue, plan, scan in parallel and write results to S3.
- Quotas and timeouts bound what one query can do.

<!-- unit: Athena among AWS analytics -->

<!-- goals -->

- Compare Athena with Redshift, Redshift Spectrum and EMR.
- Choose the right engine for a workload.

<!-- concept -->

AWS offers several ways to run SQL over the same lake, and they differ in who owns the compute and how steady the workload is. Athena fits intermittent, ad hoc and exploratory queries because you pay only when you query. A warehouse fits steady, high-concurrency BI because its compute is always ready and tuned. Clusters you manage yourself fit teams that need full control over engines and configuration.

Many architectures use more than one over a shared catalog.

<!-- example -->

| Workload | Good fit |
|---|---|
| Analysts explore logs a few times a day | Athena |
| 300 dashboard users all day, sub-second | Redshift |
| Join warehouse tables with S3 history | Redshift Spectrum |
| Custom Spark jobs with tuned configs | EMR |

#### How does Athena compare with Amazon Redshift?

Athena is serverless and queries data in place on S3, ideal for ad hoc, intermittent or exploratory workloads, paying per query. Redshift is a data warehouse (provisioned or serverless) optimized for complex, frequent, high-concurrency analytics on data loaded into its managed storage, with features such as materialized views and workload management. Many architectures use both.

#### How does Athena compare with Redshift Spectrum?

Both query S3 data through the Glue Data Catalog. Spectrum runs from a Redshift cluster and lets you join S3 data with Redshift tables; Athena is standalone and serverless. Spectrum is useful when the warehouse already exists.

#### How does Athena compare with running Trino or Spark on EMR?

Athena removes cluster management and bills per query or capacity, but gives less control over configuration and resources. EMR suits very large, steady workloads, custom configurations or tools beyond SQL.

<!-- challenge -->

A company runs Athena for everything, including a BI tool with 200 concurrent users, and hits concurrency limits daily. What do you propose?

<!-- solution -->

Move the steady BI workload to a warehouse (Redshift) or Athena capacity reservations, and keep on-demand Athena for ad hoc and exploratory work. Pre-aggregated tables help either way.

<!-- takeaways -->

- Athena suits intermittent, ad hoc queries on S3.
- Warehouses suit steady, high-concurrency BI.
- EMR suits teams that need full control.

<!-- unit: Working with Athena -->

<!-- goals -->

- Use workgroups, interfaces and saved queries in daily work.
- Know where metadata lives and what Athena can write.

<!-- concept -->

Athena itself stores almost nothing. Table definitions live in the Glue Data Catalog, data and results live in S3, and settings live in workgroups. Knowing this explains its behavior: dropping a table leaves the files, two engines can share one catalog, and a workgroup decides where results go and who pays.

Writes are possible, but on plain Hive-style tables they only add files. Transactions, updates and deletes require a table format such as Iceberg.

<!-- example -->

```bash
aws athena start-query-execution \
  --work-group analytics \
  --query-string "SELECT count(*) FROM logs.alb_access WHERE day = '2026-10-17'"
```

#### What is a workgroup?

A way to separate users, teams or applications: each workgroup has its own query result location, encryption settings, engine version, data usage limits, CloudWatch metrics and query history, and IAM can control who uses which workgroup.

#### What are the main Athena interfaces?

The console query editor, the AWS CLI and SDKs (`StartQueryExecution`, `GetQueryExecution`, `GetQueryResults`), JDBC and ODBC drivers for BI and SQL tools, Athena notebooks for Spark, and integrations with QuickSight, Glue, Step Functions and Airflow.

#### What is the Athena query editor's "saved query" feature?

Named queries stored per workgroup that users can reuse and share, which is useful for recurring analyses, though version control in Git is better for production SQL.

#### What are Athena engine versions, and how are they upgraded?

Athena evolves its engine in versions (v3 is current); workgroups can choose automatic upgrades or a specific version. Upgrades can change function behavior or type handling, so test critical queries before switching.

#### Where does Athena store table definitions?

In the AWS Glue Data Catalog (by default), or in an external Hive metastore, or in other catalogs registered as data sources (federated connectors, Redshift, S3 Tables catalogs).

#### Is Athena ACID?

For Hive-style tables, no: queries read whatever files exist, and writes add files without transactions. For Apache Iceberg tables, yes: Athena supports ACID `INSERT`, `UPDATE`, `DELETE` and `MERGE` with snapshot isolation and time travel.

#### Can Athena write data?

Yes: `CTAS`, `INSERT INTO`, `UNLOAD`, and full DML (`UPDATE`, `DELETE`, `MERGE`) on Iceberg tables. On Hive-style tables it can only add new files.

<!-- challenge -->

A user drops a table by mistake and panics. What happened to the data, and how do you restore the table?

<!-- solution -->

The data is still in S3, because Athena tables are external. Recreate the table from its DDL (for example from version control or `SHOW CREATE TABLE` in another environment) and re-add partitions.

<!-- takeaways -->

- Metadata is in Glue, data and results in S3, settings in workgroups.
- Dropping an external table leaves the files.
- ACID writes need Iceberg tables.

### Tables, DDL and SerDes

<!-- unit: External tables and the catalog -->

<!-- goals -->

- Create and inspect external tables and views.
- Choose data types and change columns safely.

<!-- concept -->

An Athena table is a contract between a location in S3 and a schema. Creating it writes only metadata; the files can already exist or arrive later. That separation makes tables cheap to create and recreate, and makes DDL your main tool for fixing mismatches.

Views add a layer of logic on top without storing data, which is useful for shared definitions but means every query pays the full scan of the underlying tables.

<!-- example -->

```sql
CREATE EXTERNAL TABLE sales.orders (
  order_id bigint, customer_id bigint, amount decimal(12,2), created_at timestamp
)
PARTITIONED BY (dt string)
STORED AS PARQUET
LOCATION 's3://lake/sales/orders/';
```

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

#### What does `SHOW CREATE TABLE` do?

It prints the DDL of a table, useful to copy definitions between environments or to check SerDe and properties.

#### What is a view in Athena?

A saved query (`CREATE VIEW`) stored in the catalog that you query like a table. It doesn't store data, so each query reads the underlying tables and is billed accordingly.

#### What data types does Athena support?

`boolean`, `tinyint`, `smallint`, `int`, `bigint`, `double`, `float`, `decimal(p,s)`, `char`, `varchar`, `string`, `binary`, `date`, `timestamp`, and complex types `array`, `map` and `struct`.

#### How do you change a table's columns?

With `ALTER TABLE … ADD COLUMNS`, `REPLACE COLUMNS` or `CHANGE COLUMN` (behavior depends on the format), or by recreating the table. For Iceberg, `ALTER TABLE … ADD COLUMNS`, `DROP COLUMN` and `RENAME COLUMN` are safe metadata operations.

<!-- challenge -->

Amounts are stored as `double` and finance reports show rounding errors in totals. What do you change?

<!-- solution -->

Store money as `decimal(p,s)` instead of `double`. Recreate the table (or write a new Parquet version with CTAS casting to decimal), since changing types in place over existing files is unreliable.

<!-- takeaways -->

- Tables are metadata over S3 locations.
- Views share logic but store nothing.
- Use `decimal` for money.

<!-- unit: Reading text formats with SerDes -->

<!-- goals -->

- Pick the right SerDe for CSV, delimited and log files.
- Configure headers, delimiters and regex parsing.

<!-- concept -->

Text files carry no schema, so Athena needs instructions to split them into columns. A SerDe is that instruction set. The default handles simple delimited text quickly; others handle quoted CSV, regular expressions and specific log layouts. Choosing wrong rarely fails loudly: values just shift or become `NULL`.

For AWS service logs, AWS publishes ready DDL, which is usually the fastest path.

<!-- example -->

```sql
CREATE EXTERNAL TABLE raw.partners (id string, name string, city string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES ('separatorChar' = ',', 'quoteChar' = '"')
LOCATION 's3://landing/partners/'
TBLPROPERTIES ('skip.header.line.count' = '1');
```

#### What is a SerDe?

A serializer/deserializer that tells Athena how to read and write a format: `LazySimpleSerDe` for delimited text, `OpenCSVSerDe` for quoted CSV, `JsonSerDe` (Hive or OpenX) for JSON, `RegexSerDe` and `GrokSerDe` for logs, and native readers for Parquet, ORC and Avro.

#### When do you use `OpenCSVSerDe` instead of `LazySimpleSerDe`?

When CSV fields are enclosed in quotes and may contain commas. `OpenCSVSerDe` handles quotes but treats every column as a string unless types are cast, and it has limitations with some types; `LazySimpleSerDe` is faster for simple delimited files.

#### How do you skip a header row in CSV files?

With the table property `'skip.header.line.count'='1'`.

#### How do you read files with a custom delimiter?

`ROW FORMAT DELIMITED FIELDS TERMINATED BY '|'` (or `\t` for TSV), with `ESCAPED BY` and `LINES TERMINATED BY` options when needed.

#### How do you query data using a regular expression?

Define a table with `RegexSerDe` and an `input.regex` property capturing groups for each column, useful for fixed-format logs; for ad hoc parsing, use `regexp_extract` on a single string column.

#### How do you query AWS service logs with Athena?

Create tables with the documented DDL for each log type (CloudTrail, VPC Flow Logs, ALB, CloudFront, S3 access logs), ideally with partition projection on date and region, then query them with SQL to investigate security events, traffic and errors.

<!-- challenge -->

A CSV has names like `"Pérez, Ana"` and the city column shows `" Ana"`. What is wrong, and what do you change?

<!-- solution -->

The table uses `LazySimpleSerDe`, which splits on every comma, including those inside quotes. Use `OpenCSVSerDe` with the quote character set, then cast non-string columns, since it reads everything as strings.

<!-- takeaways -->

- A SerDe tells Athena how to parse a format.
- Quoted CSV needs `OpenCSVSerDe`.
- Wrong SerDes shift values silently.

<!-- unit: JSON and nested data -->

<!-- goals -->

- Read JSON files and JSON strings in Athena.
- Flatten nested arrays with `UNNEST`.

<!-- concept -->

Semi-structured data arrives in two shapes: files with one JSON object per line, and JSON stored as a string inside another column. The first is mapped by a SerDe to columns, including arrays and structs. The second stays a string you extract from at query time.

Arrays turn one row into many. `UNNEST` makes that explicit, which matters for correct counts: an order with three items becomes three rows.

<!-- example -->

```sql
SELECT o.order_id, i.sku, i.qty
FROM raw.orders o
CROSS JOIN UNNEST(o.items) AS t(i)
WHERE json_extract_scalar(o.metadata, '$.channel') = 'web';
```

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

<!-- challenge -->

After an `UNNEST` of items, total revenue doubles. What went wrong?

<!-- solution -->

The order-level amount is repeated on every item row, so summing it after the unnest multiplies it. Sum item-level values (price × qty), or aggregate order amounts before unnesting.

<!-- takeaways -->

- JSON SerDes map objects to columns and structs.
- JSON strings are queried with JSON functions.
- `UNNEST` multiplies rows; aggregate accordingly.

<!-- unit: Schema on read in practice -->

<!-- goals -->

- Diagnose mismatches between files and table schemas.
- Use pseudo-columns to inspect source files.

<!-- concept -->

Since the schema is applied at read time, a table and its files can drift apart without anyone noticing until a query returns `NULL`s or fails. How Athena matches columns decides how forgiving it is: Parquet matches by name, text formats by position, so adding a column in the middle breaks text tables but not Parquet ones.

When something looks wrong, pseudo-columns tell you which file each row came from.

<!-- example -->

```sql
SELECT "$path", count(*) AS bad_rows
FROM raw.events
WHERE user_id IS NULL
GROUP BY "$path"
ORDER BY bad_rows DESC;
```

#### What happens if the data doesn't match the table schema?

Athena applies schema on read: mismatched values usually become `NULL` or cause errors such as `HIVE_BAD_DATA` (for example a string in an integer column, or a Parquet column type that doesn't match the table type).

#### Can Athena handle schema evolution?

For Parquet, adding columns at the end and reading by name works; renaming or changing types is risky. For CSV, columns are positional, so only appending columns at the end is safe. Iceberg tables support proper schema evolution (add, drop, rename, reorder, widen types).

#### How does Athena map Parquet columns: by name or by position?

By name by default for Parquet, so column order in the table doesn't need to match the files. CSV and other text formats map by position.

#### How do you query only certain files in a location?

Use the pseudo-column `"$path"` (the S3 path of each row's file) in a `WHERE` clause, which also helps debugging which file contains bad data.

```sql
SELECT "$path", count(*) FROM raw.app_events_csv GROUP BY 1 ORDER BY 2 DESC;
```

#### What other pseudo-columns exist?

`"$path"`, `"$file_size"` and `"$file_modified_time"` describe the source file of each row, useful for lineage, debugging and incremental processing.

<!-- challenge -->

A producer added a column in the middle of its CSV export. Since then, several columns contain wrong values. What do you do?

<!-- solution -->

CSV maps by position, so every column after the new one shifted. Update the table definition to the new order for new files, and separate old and new files into different tables or partitions with their own schemas, or convert both to Parquet.

<!-- takeaways -->

- Schema mismatches show up as `NULL`s or parse errors.
- Parquet maps by name; text formats by position.
- `"$path"` finds the files behind suspicious rows.

<!-- stage: Data layout -->

### Partitions and partition projection

<!-- unit: Partitioning and pruning -->

<!-- goals -->

- Choose partition columns and granularity.
- Write filters that actually prune partitions.

<!-- concept -->

Partitioning splits a table's files into folders by a column's value, so a query that filters on that column reads only the matching folders. It is the single biggest lever on scan size, but only when queries filter directly on the partition column and the partitions are neither too small nor too many.

Too many tiny partitions move the cost from scanning to planning and listing. Bucketing is the complement: it organizes files within a partition by a high-cardinality column.

<!-- example -->

```sql
-- prunes: compares the partition column directly
SELECT count(*) FROM logs.events WHERE dt BETWEEN '2026-10-01' AND '2026-10-07';
-- does not prune: function applied to the partition column
SELECT count(*) FROM logs.events WHERE date(dt) >= date '2026-10-01';
```

#### What is partitioning in Athena?

Organizing data in S3 by the values of one or more columns (`s3://bucket/table/dt=2026-10-15/`) and declaring them as partition columns, so queries filtering on them read only matching folders.

#### What is partition pruning?

The engine uses filters on partition columns to skip partitions that can't match, reducing data scanned. It only works when the filter is on the partition column itself, without functions that prevent evaluation at planning time.

#### What is a good partitioning strategy?

Partition by the columns most queries filter on (usually date), at a granularity that keeps each partition reasonably large (at least tens of MB, ideally more), and avoid high-cardinality partition keys that create millions of tiny partitions.

#### Why can too many partitions hurt performance?

Query planning has to fetch and evaluate partition metadata, and each partition usually means separate S3 listings and small files. Partition indexes in Glue or partition projection reduce the planning cost.

#### What is bucketing in Athena?

Distributing data within partitions into a fixed number of files by hashing a column (`CLUSTERED BY (user_id) INTO 32 BUCKETS`), which helps queries that filter on that column skip files. It's mainly used with `CTAS`.

#### How do you partition by date when the data contains timestamps?

Derive a date string (or year/month/day) at write time and store it as a partition column; with Iceberg, use hidden partitioning `day(event_ts)` so queries filter on the timestamp directly.

#### Why might a query not prune partitions even though it filters on the date?

The filter might apply a function to the partition column (for example `date(dt) = …` on a string column), compare with a type that requires casting, or filter on a different column than the partition key. Filter on the partition column with literal values of the same type.

<!-- challenge -->

A table is partitioned by `customer_id` (2 million values) and `dt`. Queries are slow even with filters. What do you change?

<!-- solution -->

Drop `customer_id` as a partition column: it creates millions of tiny partitions. Partition by date only, and bucket or sort by `customer_id` within partitions so file statistics still skip data.

<!-- takeaways -->

- Partition by the columns most queries filter on, usually date.
- Filter the partition column directly to prune.
- Too many partitions hurt planning; bucket high-cardinality columns.

<!-- unit: Registering partitions -->

<!-- goals -->

- Add, list and remove partitions in the catalog.
- Know when `MSCK REPAIR TABLE` works and when it doesn't.

<!-- concept -->

Classic tables only see partitions the catalog knows about. New folders in S3 are invisible until someone registers them, which is the most common reason for "the data is there but the query returns nothing".

How you register depends on the folder names. Hive-style `key=value` paths can be discovered automatically; anything else needs explicit locations. Removing a partition is also metadata-only, so the files stay in S3.

<!-- example -->

```sql
ALTER TABLE logs.events ADD IF NOT EXISTS
  PARTITION (dt = '2026-10-17') LOCATION 's3://lake/events/dt=2026-10-17/';
SHOW PARTITIONS logs.events;
```

#### How do you add partitions?

`ALTER TABLE t ADD PARTITION (dt='2026-10-15') LOCATION 's3://.../dt=2026-10-15/'`, `MSCK REPAIR TABLE` for Hive-style folders, a Glue crawler, the Glue API, or partition projection (no registration).

#### What does `MSCK REPAIR TABLE` do?

It scans the table's S3 location for Hive-style partition folders (`key=value`) and adds missing partitions to the catalog. It's slow on tables with many partitions; adding partitions explicitly or using partition projection is better.

#### What is the difference between Hive-style and non-Hive-style partition paths?

Hive-style paths contain `key=value` (`dt=2026-10-15/`), which `MSCK REPAIR` and crawlers understand. Non-Hive paths (`2026/10/15/`) need partitions added explicitly with a `LOCATION`, or partition projection with a storage location template.

#### How do you check which partitions a table has?

`SHOW PARTITIONS table` lists registered partitions (not projected ones), and the Glue console or API shows partition locations and schemas.

#### How do you remove partitions?

`ALTER TABLE t DROP PARTITION (dt='2026-10-01')` removes catalog metadata only; delete the S3 objects separately if the data should go too.

<!-- challenge -->

A nightly job runs `MSCK REPAIR TABLE` on a table with 50,000 partitions and it now takes 40 minutes. What do you suggest?

<!-- solution -->

Stop scanning the whole location: add each day's partition explicitly with `ALTER TABLE ADD PARTITION` in the load job, or switch to partition projection so no registration is needed at all.

<!-- takeaways -->

- Unregistered partitions are invisible to queries.
- `MSCK REPAIR` only understands Hive-style paths and scans everything.
- Dropping partitions removes metadata, not files.

<!-- unit: Partition projection -->

<!-- goals -->

- Configure partition projection for predictable partitions.
- Recognize where projection doesn't fit.

<!-- concept -->

Registering partitions is a maintenance chore and a planning cost. Partition projection removes both: instead of looking up partitions in the catalog, Athena computes them from rules in the table properties, such as a date range and a path template. New data becomes queryable the moment it lands.

The rules must describe reality. Projection works for predictable values like dates and known enums, and replaces catalog partitions entirely for that table.

<!-- example -->

```sql
ALTER TABLE logs.events SET TBLPROPERTIES (
  'projection.enabled' = 'true',
  'projection.dt.type' = 'date',
  'projection.dt.format' = 'yyyy-MM-dd',
  'projection.dt.range' = '2024-01-01,NOW',
  'storage.location.template' = 's3://lake/events/dt=${dt}/'
);
```

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

#### Can you mix partition projection and catalog partitions?

When projection is enabled, Athena ignores partitions registered in the catalog for that table and only uses the projection rules. Other engines still see the catalog partitions.

<!-- challenge -->

After enabling projection, queries on last year's data return nothing, though they did before. What do you check?

<!-- solution -->

Check that the projection range covers last year and that the location template and format match the real paths. With projection on, catalog partitions are ignored, so any mismatch hides data.

<!-- takeaways -->

- Projection computes partitions from rules; no registration needed.
- It fits predictable values like dates.
- With projection on, catalog partitions are ignored.

### File formats and data layout

<!-- unit: Columnar formats -->

<!-- goals -->

- Explain why Parquet and ORC make Athena faster and cheaper.
- Convert raw formats to columnar with Athena itself.

<!-- concept -->

Row formats like CSV and JSON force the engine to read every byte to find a few columns. Columnar formats store each column separately with statistics, so a query reads only the columns it selects and skips blocks whose statistics can't match. That is why the same query can scan a fiftieth of the bytes.

Converting is a one-off query, and the gain shows on every query after it, as long as people stop writing `SELECT *`.

<!-- example -->

```sql
CREATE TABLE curated.events
WITH (format = 'PARQUET', write_compression = 'ZSTD',
      external_location = 's3://lake/curated/events/', partitioned_by = ARRAY['dt'])
AS SELECT event_id, user_id, event_type, ts, dt FROM raw.events_json;
```

#### Which file formats does Athena support?

CSV/TSV and other delimited text, JSON, Parquet, ORC, Avro, Ion, logs via Regex or Grok SerDes, and open table formats Iceberg, Hudi (read) and Delta Lake (read).

#### Why are Parquet and ORC recommended?

They are columnar (read only needed columns), compressed per column, and store statistics (min/max per row group or stripe) that let Athena skip data. They also support predicate pushdown, which speeds up queries and cuts cost.

#### What is the difference between Parquet and ORC for Athena?

Both are columnar with statistics and compression and work well. Parquet is the more common choice across the ecosystem (Spark, Iceberg defaults); ORC was historically favored by Hive. Choose based on the writers and other engines you use.

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

<!-- challenge -->

Analysts complain that a Parquet table "is still expensive". The top query is `SELECT * FROM events WHERE dt = ...` on a 200-column table. What do you suggest?

<!-- solution -->

Select only the needed columns; with Parquet the cost drops with every column removed. Offer views or narrower curated tables for common use, and keep the date filter for pruning.

<!-- takeaways -->

- Columnar formats read only selected columns.
- Statistics let the engine skip blocks.
- `SELECT *` gives back most of the savings.

<!-- unit: Compression -->

<!-- goals -->

- Choose compression codecs for columnar and text files.
- Handle large non-splittable files.

<!-- concept -->

Athena bills compressed bytes, so compression is a direct discount. The codec also affects parallelism: inside Parquet or ORC any codec is fine because the format splits the file into blocks, but a single gzip text file can only be read by one worker from start to end.

So prefer columnar plus Snappy or ZSTD, and for text, keep files moderately sized.

<!-- example -->

| File | Splittable for Athena? |
|---|---|
| Parquet with ZSTD | Yes (row groups) |
| 20 GB `.csv.gz` | No: one worker reads it |
| 200 × 100 MB `.csv.gz` | Parallel across files |

#### Which compression codecs work well?

Snappy and ZSTD for Parquet and ORC (fast, splittable within the format). For text files, gzip is common but not splittable, so one large gzip file is read by a single worker; bzip2 is splittable but slow.

#### Does compression reduce Athena costs?

Yes. Athena bills on compressed bytes scanned, so compressed files (and columnar encoding) directly reduce cost, besides reducing S3 storage.

#### How do you handle data that arrives as one huge gzip file?

Since gzip isn't splittable, a single worker reads it. Split the file before or during ingestion, recompress as bzip2 or, better, convert to Parquet with a `CTAS` or a Glue job.

<!-- challenge -->

A partner sends one 30 GB `.json.gz` per day and the query on it times out. What do you do?

<!-- solution -->

Gzip isn't splittable, so one worker reads it. Add an ingestion step (Glue, Lambda or Firehose) that splits and converts it to partitioned Parquet with Snappy or ZSTD, and query the converted table.

<!-- takeaways -->

- Compression lowers the bytes you pay for.
- Columnar formats split compressed files; gzip text doesn't.
- Prefer Snappy or ZSTD inside Parquet or ORC.

<!-- unit: File sizes and layout -->

<!-- goals -->

- Keep files in the right size range and fix small-file problems.
- Use sorting and statistics so the engine skips data.

<!-- concept -->

Every file has a fixed cost to open, list and plan, so thousands of tiny files waste most of a query's time. Very large files limit parallelism. The healthy range is roughly 128 MB to 1 GB, which usually means batching writes or compacting afterwards.

Within files, order matters. When data is sorted by a filtered column, each block's min/max statistics become narrow, and predicate pushdown can skip most blocks.

<!-- example -->

```sql
-- compact one day of small files into a few sorted Parquet files
INSERT INTO curated.events
SELECT * FROM raw.events WHERE dt = '2026-10-17'
ORDER BY user_id;
```

#### What is the ideal file size for Athena?

Roughly 128 MB to 1 GB per file. Many small files (a few KB) add per-file overhead and S3 request costs; very large unsplittable files limit parallelism.

#### How do you fix a table made of many small files?

Compact them: run a `CTAS` or `INSERT INTO` that rewrites data into fewer larger files (with bucketing or a controlled partitioning), use `OPTIMIZE` on Iceberg tables, or fix the producer (larger batches, Firehose buffering).

#### How does sorting data help Athena?

When data is sorted (or clustered) by a commonly filtered column within files, Parquet and ORC statistics have tight min/max ranges, so more row groups can be skipped.

#### What is predicate pushdown in Athena?

Filters are pushed to the file reader, which uses Parquet/ORC statistics to skip row groups or stripes whose min/max can't match, so less data is read and decompressed.

#### What row group size is good for Parquet?

Typically 128 MB to 512 MB row groups; larger row groups compress well and reduce overhead, but very large ones reduce the effectiveness of skipping. Writers such as Spark have sensible defaults.

#### A table has 2 million small JSON files per day. What do you recommend?

Fix the producer to batch records (Firehose buffering, larger writes), add a compaction step that converts each day to a handful of Parquet files (Glue job or `CTAS`), and query the compacted table; keep the raw JSON only as an archive.

<!-- challenge -->

A Lambda writes one tiny file per event to S3. Queries are slow and S3 costs grow. What two changes do you make?

<!-- solution -->

Batch at the producer: send events to Firehose with a buffer (for example 128 MB or 5 minutes) and Parquet conversion. Then compact old data once into large files and delete the small ones.

<!-- takeaways -->

- Aim for files of about 128 MB to 1 GB.
- Batch writes or compact small files.
- Sorted data makes statistics and pushdown effective.

### Iceberg tables in Athena

<!-- unit: Iceberg on Athena -->

<!-- goals -->

- Explain what Iceberg adds on top of Parquet files.
- Choose between Iceberg and Hive-style tables.

<!-- concept -->

Hive-style tables are folders of files: simple, but with no transactions, no row changes and no safe concurrent writes. Iceberg adds a metadata layer that records exactly which files make up each version of a table. Every write becomes an atomic commit, and features like updates, time travel and schema changes follow from that.

Because the format is open, the same table works in Spark, Trino, Snowflake and others, which makes Iceberg the default for new lake tables that change.

<!-- example -->

```sql
CREATE TABLE lake.customers (
  customer_id bigint, email string, country string, updated_at timestamp
)
PARTITIONED BY (country)
LOCATION 's3://lake/iceberg/customers/'
TBLPROPERTIES ('table_type' = 'ICEBERG', 'format' = 'parquet');
```

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

#### Iceberg or Hive-style tables in Athena: how do you choose?

Iceberg when you need updates, deletes, upserts (CDC, GDPR deletions), schema evolution, concurrent writers, or time travel. Hive-style Parquet is simpler for immutable append-only data written by other tools. New lakehouse designs usually choose Iceberg.

#### Can other engines use the same Iceberg tables?

Yes. Spark on EMR or Glue, Trino, Flink, Snowflake, Databricks and others can read and write the same Iceberg tables through the Glue Data Catalog or an Iceberg REST catalog, which avoids engine lock-in.

#### What are S3 Tables?

S3 table buckets that store Iceberg tables with built-in maintenance (compaction, snapshot management) and a catalog integration, which Athena can query and write like other Iceberg tables.

#### What table properties matter for Iceberg in Athena?

`format` (parquet, orc, avro), `write_compression`, `optimize_rewrite_delete_file_threshold`, `vacuum_max_snapshot_age_seconds`, `vacuum_min_snapshots_to_keep` and `vacuum_max_metadata_files_to_keep`, which control file layout and retention.

<!-- challenge -->

An append-only log table is read by Athena only and never changes. Should you move it to Iceberg?

<!-- solution -->

Not necessarily. A partitioned Parquet table with projection already works well. Iceberg adds value when you need row changes, concurrent writers, schema or partition evolution, or time travel. Choose it if those needs are likely soon.

<!-- takeaways -->

- Iceberg makes every write an atomic, versioned commit.
- It enables updates, deletes, time travel and evolution.
- Plain Parquet is fine for simple, append-only data.

<!-- unit: Changing data in Iceberg -->

<!-- goals -->

- Apply `UPDATE`, `DELETE` and `MERGE` to Iceberg tables.
- Handle CDC and GDPR deletions with concurrent writers.

<!-- concept -->

With Iceberg, row-level changes become ordinary SQL. Athena writes small delete files that mark removed rows instead of rewriting data files, which keeps writes fast but makes reads slower until compaction merges them.

Concurrency is optimistic: writers don't lock, they check at commit time and retry on conflict. That suits most pipelines, as long as two jobs don't keep rewriting the same partitions at once.

<!-- example -->

```sql
MERGE INTO lake.customers t
USING staging.customer_changes s
ON t.customer_id = s.customer_id
WHEN MATCHED AND s.op = 'D' THEN DELETE
WHEN MATCHED THEN UPDATE SET email = s.email, country = s.country, updated_at = s.updated_at
WHEN NOT MATCHED AND s.op <> 'D' THEN INSERT VALUES (s.customer_id, s.email, s.country, s.updated_at);
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

#### How do row-level deletes work in Iceberg on Athena?

Athena writes position delete files (merge-on-read) that mark deleted rows instead of rewriting data files. Reads merge them on the fly, so tables with many deletes need regular `OPTIMIZE` to stay fast.

#### Can multiple writers modify an Iceberg table at the same time?

Yes, with optimistic concurrency: each commit checks the table's current version, and conflicting commits fail and must retry. Avoid many concurrent writers updating the same partitions.

#### Analysts need to delete individual customers' data for GDPR. How do you support it on Athena?

Store the data in Iceberg tables, run `DELETE FROM … WHERE customer_id = …` across affected tables, then `OPTIMIZE` and `VACUUM` to physically remove old files after the snapshot retention period. With Hive tables, you'd have to rewrite whole partitions.

#### How do you query the latest state of a table that receives CDC records?

Either maintain an Iceberg table with `MERGE` applying the changes (the cleanest), or, on an append-only change table, use `ROW_NUMBER()` over each key ordered by change timestamp and keep the latest non-deleted row in a view.

```sql
SELECT * FROM (
  SELECT *, row_number() OVER (PARTITION BY customer_id ORDER BY change_ts DESC) AS rn
  FROM raw.customer_changes
) WHERE rn = 1 AND op <> 'D';
```

<!-- challenge -->

After a GDPR `DELETE`, the person's data is still in S3 files. Why, and what completes the deletion?

<!-- solution -->

Delete files only mark rows; old data files and snapshots still contain them. Run `OPTIMIZE` to rewrite files without the rows, then `VACUUM` to expire old snapshots and remove unreferenced files.

<!-- takeaways -->

- Iceberg supports `UPDATE`, `DELETE` and `MERGE` in Athena.
- Deletes write delete files; compaction applies them.
- Concurrent commits are checked optimistically.

<!-- unit: Evolution, time travel and maintenance -->

<!-- goals -->

- Evolve schemas and partitioning without rewriting data.
- Use time travel, rollbacks and maintenance commands.

<!-- concept -->

Because Iceberg tracks columns by ID and partitions as transforms of columns, the table's shape can change without touching old files. Queries filter on the real column, and the right partitions are pruned behind the scenes.

Every commit leaves a snapshot, which gives you time travel and rollback for free, until maintenance expires them. That's the trade-off to manage: snapshots and small files accumulate, so compaction and vacuum must be scheduled.

<!-- example -->

```sql
SELECT count(*) FROM lake.customers FOR TIMESTAMP AS OF TIMESTAMP '2026-10-15 08:00:00 UTC';
OPTIMIZE lake.customers REWRITE DATA USING BIN_PACK;
VACUUM lake.customers;
```

#### What is hidden partitioning in Iceberg?

Partitions defined as transforms of columns (`day(event_ts)`, `bucket(16, user_id)`, `truncate(10, sku)`), so queries filter on the original column (`event_ts`) and Iceberg prunes partitions automatically; users don't need to know about partition columns.

#### Can you evolve an Iceberg table's partitioning?

Yes. You can change the partition spec (for example from monthly to daily) without rewriting old data; old files keep the old spec and new data uses the new one, and queries handle both.

#### How do you add a column to an Iceberg table?

`ALTER TABLE lake.customers ADD COLUMNS (segment string)`. Existing files aren't rewritten; old rows return `NULL` for the new column.

#### How does time travel work for Iceberg in Athena?

```sql
SELECT * FROM lake.customers FOR TIMESTAMP AS OF TIMESTAMP '2026-10-15 08:00:00 UTC';
SELECT * FROM lake.customers FOR VERSION AS OF 949530903748831860;
```

You can also inspect metadata tables such as `"customers$snapshots"`, `"customers$history"`, `"customers$files"` and `"customers$partitions"`.

#### How do you roll back an Iceberg table in Athena?

Read the previous version with time travel and rewrite it (for example `CTAS` from `FOR VERSION AS OF`), or use an engine with rollback procedures (Spark's `rollback_to_snapshot`) on the same table.

#### What do `OPTIMIZE` and `VACUUM` do on Iceberg tables?

`OPTIMIZE table REWRITE DATA USING BIN_PACK` compacts small files and merges delete files into data files. `VACUUM` expires old snapshots and removes files no longer referenced (according to retention properties), freeing storage.

<!-- challenge -->

A bad job overwrote half of a customer table at 09:12. How do you restore it with Athena?

<!-- solution -->

Query the table `FOR TIMESTAMP AS OF` 09:10 to confirm the good state, then rebuild the table from that version (for example CTAS into a new table and swap, or insert the old rows back). Do it before `VACUUM` expires the snapshot.

<!-- takeaways -->

- Hidden partitioning and column IDs make evolution safe.
- Snapshots give time travel and rollback.
- Schedule `OPTIMIZE` and `VACUUM` to control growth.

<!-- stage: Building and querying -->

### CTAS, INSERT and UNLOAD

<!-- unit: Writing tables with CTAS -->

<!-- goals -->

- Create tables from queries with CTAS in the right format and layout.
- Work within CTAS limits on partitions, files and locations.

<!-- concept -->

CTAS is Athena's main transformation tool: one statement runs a query and writes the result as a new table, choosing format, compression, partitioning and bucketing. It's how you turn raw files into curated tables without another service.

Its guardrails shape pipelines. A query can only write a limited number of partitions, and it refuses non-empty locations, so large backfills run in batches and each run needs a fresh or cleaned location.

<!-- example -->

```sql
CREATE TABLE curated.daily_sales
WITH (format = 'PARQUET', external_location = 's3://lake/curated/daily_sales/v2/',
      partitioned_by = ARRAY['dt'], bucketed_by = ARRAY['store_id'], bucket_count = 8)
AS SELECT store_id, sum(amount) AS revenue, dt
   FROM sales.orders GROUP BY store_id, dt;
```

#### What is `CTAS`?

`CREATE TABLE AS SELECT`: creates a new table from a query's results, writing files in the chosen format, compression, partitioning and bucketing to S3. It's used to convert formats, build aggregates and materialize transformations.

#### What are the limits of `CTAS` and `INSERT INTO`?

A single query can create or insert into a limited number of partitions (100 per query for Hive tables), so large backfills need several statements or loops by partition ranges. Iceberg tables don't have this specific limit.

#### How do you control the number of output files in `CTAS`?

With `bucketed_by` and `bucket_count`, which fix the number of files per partition, or by reducing parallelism of the final stage; otherwise Athena writes as many files as workers produce.

#### Can a `CTAS` write to an existing S3 location?

No. The `external_location` must be empty, which prevents overwriting data by mistake. Delete or use a new location for reruns.

#### How do you create an empty copy of a table's schema?

`CREATE TABLE new_t WITH (...) AS SELECT * FROM t WITH NO DATA`, which creates the table definition without writing rows.

<!-- challenge -->

A CTAS over three years of daily data fails because it writes too many partitions. How do you load it?

<!-- solution -->

Create the table with CTAS for the first batch of fewer than 100 partitions (for example three months), then add the rest with `INSERT INTO ... SELECT` in batches of the same size, ideally driven by a script.

<!-- takeaways -->

- CTAS writes query results as a new, formatted table.
- Partition limits require batching large loads.
- CTAS needs an empty target location.

<!-- unit: Idempotent ELT on Athena -->

<!-- goals -->

- Build reruns-safe pipelines with `INSERT INTO`, CTAS or dbt.
- Schedule Athena queries with AWS services or Airflow.

<!-- concept -->

On Hive-style tables, `INSERT INTO` only adds files, so running it twice doubles the data. Pipelines become safe to rerun when each run owns a slice, usually a date partition, and clears it first. Iceberg removes the problem with `MERGE` and overwrites, which is why many Athena ELT setups use Iceberg for curated layers.

Orchestration is just calling the API on a schedule, but dbt adds tests and dependencies on top.

<!-- example -->

```bash
# rerun-safe daily load for a Hive-style table
aws s3 rm --recursive s3://lake/curated/orders/dt=2026-10-17/
aws athena start-query-execution --work-group etl --query-string \
 "INSERT INTO curated.orders SELECT ..., dt FROM raw.orders WHERE dt = '2026-10-17'"
```

#### What does `INSERT INTO` do on a Hive-style table?

It appends new files to the table's location (and registers new partitions). It never modifies existing files, so rerunning it duplicates data unless you first delete the target partition's files.

#### How do you make Athena ELT idempotent?

For Hive tables, write each run's output to a partition and delete or overwrite that partition before rerunning (often by writing to a new location and swapping the partition location). For Iceberg tables, use `MERGE` or `DELETE` plus `INSERT` in the same logic, or `INSERT OVERWRITE`-style patterns with Iceberg.

#### How do you schedule Athena queries?

With EventBridge Scheduler or Step Functions calling `StartQueryExecution`, Airflow's `AthenaOperator`, dbt with the dbt-athena adapter, or a Lambda function on a schedule.

#### Can you use dbt with Athena?

Yes, with the dbt-athena adapter: models materialize as views, tables (`CTAS`), incremental models (`insert_overwrite` by partition, `append`, or `merge` on Iceberg) and Iceberg tables, with Glue as the catalog.

#### How would you build a small ELT pipeline only with Athena?

Raw tables over landing files, `CTAS` or `INSERT INTO` (or dbt-athena models) to build cleaned Iceberg or Parquet tables, `MERGE` for upserts, data quality checks as SQL queries that fail the pipeline when they return rows, and Step Functions or Airflow to schedule and order the statements.

<!-- challenge -->

A dbt-athena incremental model appends rows on each run, and reruns create duplicates. Which strategy do you switch to?

<!-- solution -->

Use `insert_overwrite` on a date partition (Hive tables) or `merge` with a `unique_key` on Iceberg tables. Both replace the affected data on rerun instead of appending.

<!-- takeaways -->

- `INSERT INTO` appends; reruns duplicate.
- Own a slice per run, or use Iceberg `MERGE`.
- dbt-athena adds tests and dependencies to Athena ELT.

<!-- unit: Exporting and parameterizing -->

<!-- goals -->

- Export query results in useful formats.
- Use parameterized queries safely in applications.

<!-- concept -->

Not every result should become a table. Sometimes another system needs files, and `UNLOAD` writes results in a chosen format without registering anything. Sometimes a person needs a single CSV, which the result location already provides.

Applications that build queries from user input should never concatenate strings; parameters keep values separate from SQL and avoid injection.

<!-- example -->

```sql
UNLOAD (SELECT * FROM curated.daily_sales WHERE dt = '2026-10-17')
TO 's3://exports/partner_x/2026-10-17/'
WITH (format = 'PARQUET', compression = 'SNAPPY');

PREPARE sales_by_store FROM SELECT * FROM curated.daily_sales WHERE store_id = ?;
EXECUTE sales_by_store USING 42;
```

#### What does `UNLOAD` do?

It writes query results to S3 in a chosen format (Parquet, ORC, Avro, JSON, text) with optional partitioning and compression, without creating a table, which is useful for exports to other systems.

```sql
UNLOAD (SELECT * FROM curated.app_events WHERE dt = '2026-10-15')
TO 's3://exports/app_events/dt=2026-10-15/'
WITH (format = 'PARQUET', compression = 'SNAPPY');
```

#### How do you export query results as a single CSV?

Run the query and download the result file from the result location (Athena writes one CSV per query), or use `UNLOAD` with a text format; very large results may be split across files with `UNLOAD`.

#### What are prepared statements and parameterized queries?

Statements created with `PREPARE` (or passed with `ExecutionParameters`) that contain `?` placeholders filled at execution, which avoids SQL injection and lets applications reuse query text.

```sql
PREPARE events_by_day FROM
SELECT event_type, count(*) FROM curated.app_events WHERE dt = ? GROUP BY 1;

EXECUTE events_by_day USING '2026-10-15';
```

<!-- challenge -->

An internal app builds Athena SQL by concatenating a user-typed store name. What risk is there, and what is the fix?

<!-- solution -->

SQL injection: a crafted name could change the query. Use parameterized queries (`ExecutionParameters` or prepared statements) and a workgroup and IAM role limited to the tables the app needs.

<!-- takeaways -->

- `UNLOAD` exports results as files without a table.
- Each query also writes a CSV to the result location.
- Parameterize queries built from user input.

### SQL functions and patterns

<!-- unit: Types, dates and NULLs -->

<!-- goals -->

- Handle dates, conversions and `NULL`s correctly.
- Pseudonymize identifiers with hashing.

<!-- concept -->

Many wrong answers in SQL come from three places: dates in the wrong type or time zone, casts that fail on dirty values, and `NULL`s that silently drop out of comparisons. Lake data is often dirty because it was never validated on write, so defensive functions matter more in Athena than in a warehouse.

Hashing belongs here too: a deterministic hash lets you join on an identifier without exposing it.

<!-- example -->

```sql
SELECT
  date_trunc('month', TRY_CAST(order_ts AS timestamp)) AS month,
  count(*) FILTER (WHERE TRY_CAST(amount AS decimal(12,2)) IS NULL) AS bad_amounts,
  to_hex(hmac_sha256(to_utf8(email), to_utf8('salt-from-secrets'))) AS email_key
FROM raw.orders
GROUP BY 1, 3;
```

#### How do you work with dates and times in Athena?

With functions like `current_date`, `date_add('day', -1, current_date)`, `date_diff('day', a, b)`, `date_trunc('month', ts)`, `date_format(ts, '%Y-%m-%d')`, `from_iso8601_timestamp(s)`, `parse_datetime(s, 'yyyy-MM-dd HH:mm')` and `ts AT TIME ZONE 'America/Bogota'`.

#### How do you safely convert types?

`TRY_CAST(x AS integer)` returns `NULL` instead of failing on bad values, and `try()` wraps expressions that may error. Use them on raw string data.

#### How do you handle `NULL` values in aggregations and comparisons?

Aggregations ignore `NULL`s (except `count(*)`); comparisons with `NULL` return `NULL`, so use `IS NULL`, `coalesce`, `IS DISTINCT FROM` for null-safe comparison, and be careful with `NOT IN` on columns that contain nulls.

#### How do you hash values for pseudonymization?

With `to_hex(sha256(to_utf8(email)))` (preferably with a secret salt or HMAC via `hmac_sha256`), producing stable pseudonyms that can still be joined.

<!-- challenge -->

A query `WHERE discount <> 10` misses rows where discount is missing. Why, and how do you fix it?

<!-- solution -->

Comparisons with `NULL` return `NULL`, so those rows are excluded. Use `WHERE discount IS NULL OR discount <> 10`, or `coalesce(discount, 0) <> 10` if missing means zero.

<!-- takeaways -->

- Use `TRY_CAST` on dirty lake data.
- `NULL` comparisons drop rows silently.
- Salted hashes pseudonymize identifiers.

<!-- unit: Analytic patterns -->

<!-- goals -->

- Deduplicate, rank and compute running metrics with window functions.
- Pivot data and compare tables.

<!-- concept -->

A handful of patterns cover most analytic questions. Window functions answer "per group" questions without collapsing rows: latest record per key, top N per category, running totals. Conditional aggregation replaces a missing `PIVOT`. Set operations compare two versions of a table.

Knowing the pattern matters more than the syntax, because the same shape repeats across engines.

<!-- example -->

```sql
WITH ranked AS (
  SELECT *, row_number() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) AS rn
  FROM raw.customer_changes
)
SELECT * FROM ranked WHERE rn = 1;      -- latest version per customer
```

#### How do you deduplicate rows in Athena?

With `row_number()` over the key ordered by a timestamp, keeping the first row per key, in a subquery or CTE, since Athena doesn't support `QUALIFY`.

#### How do you get the top N rows per group?

Use `row_number()` or `rank()` over the group ordered by the metric in a subquery, and filter on the rank in the outer query; `max_by(x, y)` gives the value of `x` at the maximum `y` per group.

#### How do you compute a running total or moving average?

With window functions: `sum(amount) OVER (PARTITION BY customer ORDER BY dt ROWS UNBOUNDED PRECEDING)` for running totals and `avg(amount) OVER (ORDER BY dt ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)` for a 7-row moving average.

#### What are `max_by` and `min_by` useful for?

Returning the value of one column at the row where another column is maximal or minimal, for example the latest status per order: `max_by(status, updated_at)`, without a window function.

#### How do you pivot data in Athena?

With conditional aggregation, since there's no `PIVOT` keyword: `sum(CASE WHEN month = 1 THEN amount END) AS jan`, or `map_agg` to build a key-value map.

#### How do you compare two tables to find differences?

With `EXCEPT` in both directions (`SELECT * FROM a EXCEPT SELECT * FROM b`) for row differences, or a full outer join on the key comparing columns, useful for validating migrations.

<!-- challenge -->

You need each customer's latest country and their total spend in one query. Write the core of it.

<!-- solution -->

`SELECT customer_id, max_by(country, updated_at) AS country, sum(amount) AS spend FROM orders GROUP BY customer_id`. `max_by` avoids a separate window step for the latest value.

<!-- takeaways -->

- `row_number()` handles dedupe and top N per group.
- Conditional aggregation pivots data.
- `EXCEPT` both ways finds differences between tables.

<!-- unit: Arrays, series and specialized functions -->

<!-- goals -->

- Use array, map and sequence functions.
- Apply geospatial, sampling and reuse patterns.

<!-- concept -->

Trino's function library goes well beyond standard SQL, and lake data often needs it: arrays and maps from JSON, calendars that have gaps, coordinates from apps. Generating a date series is a common trick to show days with zero activity instead of missing them.

Reuse completes the toolkit: views share logic across queries and CTEs organize it within one.

<!-- example -->

```sql
SELECT d AS day, coalesce(count(o.order_id), 0) AS orders
FROM UNNEST(sequence(date '2026-10-01', date '2026-10-31', interval '1' day)) AS t(d)
LEFT JOIN sales.orders o ON date(o.created_at) = d
GROUP BY d ORDER BY d;
```

#### What are useful array and map functions?

`cardinality`, `contains`, `element_at`, `array_join`, `array_agg`, `filter`, `transform`, `reduce`, `map_keys`, `map_values` and `map_agg`, which let you work with nested data without exploding it.

#### How do you generate a date series in Athena?

With `sequence` and `UNNEST`: `SELECT d FROM UNNEST(sequence(date '2026-01-01', date '2026-12-31', interval '1' day)) AS t(d)`, useful for filling gaps in time series.

#### How do you do geospatial queries in Athena?

With geospatial functions such as `ST_Point`, `ST_Contains`, `ST_Distance`, `ST_Within`, `ST_GeometryFromText` and `great_circle_distance`, for example to count events inside polygons.

#### How do you sample data in Athena?

`TABLESAMPLE BERNOULLI (1)` reads rows with 1% probability (but still scans all data), and `TABLESAMPLE SYSTEM (1)` samples at file or split level, which can reduce data scanned.

#### How do you write reusable SQL logic in Athena?

With views for shared logic, CTEs (`WITH`) for readability within a query, SQL UDF-like patterns through views, and dbt macros when using dbt-athena.

<!-- challenge -->

A teammate uses `TABLESAMPLE BERNOULLI (1)` to make an exploratory query cheaper. Does it work?

<!-- solution -->

It returns about 1% of rows but still scans all the data, so the cost doesn't drop. Filter on partitions (for example one day), or use `TABLESAMPLE SYSTEM` if approximate file-level sampling is acceptable.

<!-- takeaways -->

- Arrays, maps and JSON functions handle nested lake data.
- `sequence` and `UNNEST` fill gaps in date series.
- Sampling doesn't reduce scan cost unless it skips files.

### Spark in Athena and notebooks

<!-- unit: Serverless Spark in Athena -->

<!-- goals -->

- Explain what Athena for Apache Spark offers.
- Choose between Athena SQL and Athena Spark.

<!-- concept -->

Some work doesn't fit in one SQL statement: iterative exploration, Python libraries, machine learning preparation. Athena for Apache Spark gives the same serverless experience for PySpark in notebooks, starting in seconds without a cluster.

SQL remains the better fit for queries and reports; Spark is for logic that needs a programming language.

<!-- example -->

```python
df = spark.read.table("lake.orders").where("dt >= '2026-10-01'")
features = df.groupBy("customer_id").agg(F.count("*").alias("orders"), F.sum("amount").alias("spend"))
features.write.mode("overwrite").saveAsTable("ml.customer_features")
```

#### What is Amazon Athena for Apache Spark?

A serverless Spark offering in Athena where you run PySpark and Spark SQL in notebooks or through APIs, with fast start-up and billing per DPU-hour, for workloads that need more than SQL.

#### When would you use Athena Spark instead of Athena SQL?

For complex transformations in Python, machine learning preparation, iterative exploration with DataFrames, or logic that's awkward in SQL; SQL remains simpler and cheaper for most analytics.

#### What languages are supported in Athena notebooks?

PySpark and Spark SQL (with magics), with common Python libraries available and the ability to add others to the session.

<!-- challenge -->

A data scientist wants to prepare features with pandas-style logic over 300 GB of Parquet. Athena SQL or Athena Spark?

<!-- solution -->

Athena Spark: the logic is easier in PySpark and the data is too large for pandas on one machine. Results can be written back as catalog tables that Athena SQL queries.

<!-- takeaways -->

- Athena Spark runs PySpark serverlessly in notebooks.
- Use SQL for queries; Spark for programmatic logic.
- Both share the Glue catalog.

<!-- unit: Sessions, billing and catalog -->

<!-- goals -->

- Understand how Spark sessions are billed and ended.
- Read and write catalog tables from Spark sessions.

<!-- concept -->

A Spark session holds compute while it is open, so cost follows session time rather than bytes scanned. Idle timeouts end sessions automatically, which matters because notebooks are easy to leave open.

Sessions use the same Glue Data Catalog as SQL, so tables written from Spark appear in Athena SQL, which lets the two styles share one lake.

<!-- example -->

| Billing model | Athena SQL | Athena Spark |
|---|---|---|
| Unit | Bytes scanned (or reserved DPUs) | DPU-hours of the session |
| Cost driver | Data read | Session duration and size |

#### How do Athena Spark sessions bill?

Per DPU-hour of the session's compute, with automatic scaling of executors and idle timeouts that end the session.

#### How does Athena Spark access the Data Catalog?

Spark sessions in Athena use the Glue Data Catalog by default, so you can read and write catalog tables (including Iceberg) with Spark SQL or DataFrames.

<!-- challenge -->

Monthly Athena Spark costs are high, though notebooks are used only a few hours a day. What do you check?

<!-- solution -->

Check session idle timeouts and whether users leave sessions running, and the DPU sizing per session. Lower the idle timeout and educate users to end sessions after work.

<!-- takeaways -->

- Spark sessions bill per DPU-hour.
- Idle timeouts limit forgotten sessions.
- Spark and SQL share the Glue catalog.

<!-- stage: Operating Athena -->

### Performance tuning

<!-- unit: Measuring a query -->

<!-- goals -->

- Measure data scanned and read query plans.
- Know which levers improve speed and cost.

<!-- concept -->

Tuning starts with measurement. Every execution records bytes scanned and time spent queued, planning and running, and `EXPLAIN ANALYZE` shows where the time went. Most improvements then come from the same short list: read less (columns, partitions, formats), move less between workers, and avoid single-worker steps.

A `LIMIT` is not a cost control on its own; only reading less data is.

<!-- example -->

```sql
EXPLAIN ANALYZE
SELECT store_id, sum(amount) FROM sales.orders
WHERE dt = '2026-10-17' GROUP BY store_id;
-- check: input bytes per stage, pruned partitions, time per operator
```

#### What are the main ways to make Athena queries faster and cheaper?

Use columnar formats with compression, partition by common filters (or partition projection), keep files 128 MB–1 GB, select only needed columns, filter on partition columns, sort or bucket by common filters, use Iceberg with compaction, compute table statistics, and reuse query results.

#### How do you see how much data a query scanned?

In the console after running, in `GetQueryExecution` statistics (`DataScannedInBytes`), in CloudWatch workgroup metrics, and in `EXPLAIN ANALYZE` output per stage.

#### What do `EXPLAIN` and `EXPLAIN ANALYZE` show?

`EXPLAIN` shows the distributed or logical plan without running the query: scans, filters pushed down, joins and their distribution. `EXPLAIN ANALYZE` runs the query and reports actual rows, data read and time per stage, which shows where time goes.

#### How does `LIMIT` affect cost?

On Hive-style tables a `LIMIT` without filters may stop early but can still scan many files; it doesn't guarantee low cost. Partition filters are the reliable way to limit scanning.

<!-- challenge -->

A query scans 800 GB though it filters one day. What do you look for in `EXPLAIN`?

<!-- solution -->

Whether the partition filter appears in the scan (pruning), or whether the filter is applied after the scan because of a function or type mismatch on the partition column. Also check if the table is partitioned or projected at all.

<!-- takeaways -->

- Measure bytes scanned and stage times first.
- `EXPLAIN ANALYZE` shows where time and data go.
- `LIMIT` doesn't guarantee less scanning.

<!-- unit: Joins and data distribution -->

<!-- goals -->

- Write joins the optimizer can execute efficiently.
- Handle skew and missing statistics.

<!-- concept -->

Distributed joins either broadcast a small table to every worker or shuffle both sides by key. The optimizer chooses based on statistics; without them, it relies on the order you wrote, so the largest table should come first and the smallest last.

Skew breaks both strategies: when a few keys hold most rows, single workers receive most of the work. Filtering or splitting hot keys usually helps more than any setting.

<!-- example -->

```sql
-- largest table first, small dimension last (broadcast-friendly)
SELECT f.order_id, d.region
FROM sales.orders f
JOIN ref.stores d ON f.store_id = d.store_id
WHERE f.dt = '2026-10-17';
```

#### How should you order tables in a join?

Engine v3 has a cost-based optimizer that can reorder joins when table statistics exist in the Glue catalog. Without statistics, put the largest table first (left) and smaller tables on the right, since the right side is built into memory and distributed to workers.

#### What are join distribution types?

Broadcast joins send the small right-side table to all workers (fast if it's small); partitioned joins hash both sides across workers (needed for two large tables). The optimizer chooses based on statistics.

#### How do table statistics help Athena?

Column statistics stored in the Glue catalog (computed by Glue) let the cost-based optimizer choose join order and distribution, improving complex queries without code changes.

#### What is the impact of data skew on Athena joins and aggregations?

A few keys holding most rows overload single workers and can cause "exhausted resources" errors. Filter out hot keys (often nulls), handle them separately, or use approximate aggregations.

<!-- challenge -->

A join on `customer_id` fails with "exhausted resources", and 30% of rows have `customer_id = 0` (guest). What do you do?

<!-- solution -->

Treat the hot key separately: filter `customer_id = 0` out of the join and handle guests in a separate branch, then `UNION ALL` the results. Also generate table statistics so the optimizer picks the right join type.

<!-- takeaways -->

- Put large tables first when statistics are missing.
- Broadcast small tables; shuffle large ones.
- Skewed keys need special handling.

<!-- unit: Memory-heavy operations -->

<!-- goals -->

- Recognize operations that concentrate work on a single worker.
- Replace exact computations with approximate ones where acceptable.

<!-- concept -->

Some SQL operations need to see all rows at once: global sorts, exact distinct counts, windows without partitions, deduplication across a union. In a distributed engine, those steps funnel data into few workers, which is where "exhausted resources" errors come from.

The remedies are to add structure (partition windows, limit sorts), to accept approximation where the business can, and to avoid unnecessary deduplication.

<!-- example -->

```sql
SELECT dt,
       approx_distinct(user_id) AS users,            -- ~2% error, small memory
       approx_percentile(latency_ms, 0.95) AS p95
FROM logs.requests
WHERE dt >= '2026-10-01'
GROUP BY dt;
```

#### Why does `ORDER BY` without `LIMIT` hurt performance?

A global sort requires sending all rows to a single worker for the final ordering, which is slow and can fail with "exceeded resources". Add a `LIMIT` (top-N is efficient) or sort only what's needed.

#### What is "Query exhausted resources at this scale factor"?

An error when a query needs more memory than available for an operation (huge joins, `GROUP BY` with many groups, `DISTINCT` on many columns, `ORDER BY` of everything, very large arrays). Fixes: filter earlier, reduce columns, approximate functions, split the query, use `CTAS` to materialize intermediate steps, or use capacity reservations.

#### When should you use approximate functions?

`approx_distinct`, `approx_percentile` and `approx_most_frequent` return estimates with small errors using much less memory than exact `count(DISTINCT)` or percentiles, which suits dashboards and exploration.

#### Why does `count(DISTINCT x)` on a huge table fail or run slowly?

It requires keeping all distinct values in memory across workers. Use `approx_distinct(x)` for estimates, or pre-aggregate distinct counts by partition and combine.

#### How do window functions affect Athena performance?

Window functions partition and sort data; a window over the whole table (no `PARTITION BY`) forces a single worker. Always partition windows by a key and filter data first.

#### What is the effect of `UNION` versus `UNION ALL`?

`UNION` removes duplicates, which needs an extra aggregation step; `UNION ALL` just concatenates. Use `UNION ALL` when duplicates are impossible or acceptable.

#### How do you speed up `LIKE` searches on large text columns?

Filter on partitions first, use `regexp_like` only when needed, and consider pre-extracting searchable fields into separate columns during ETL, or a search service such as OpenSearch for full-text needs.

<!-- challenge -->

A daily report computes exact distinct users over 90 days and often fails. The product team only needs a trend. What do you change?

<!-- solution -->

Use `approx_distinct(user_id)` per day, which needs little memory and has about 2% error. If exact numbers are ever needed, precompute daily distinct sets in a summary table.

<!-- takeaways -->

- Global sorts, exact distincts and unpartitioned windows are expensive.
- Approximate functions trade small errors for scale.
- Prefer `UNION ALL` unless you need deduplication.

<!-- unit: Reusing and precomputing results -->

<!-- goals -->

- Reuse recent results and precompute frequent aggregates.
- Speed up dashboards that query Athena.

<!-- concept -->

The cheapest query is the one you don't run. Dashboards often send the same queries over and over, so caching recent results and precomputing common aggregates save both cost and waiting time. Result reuse handles identical queries; summary tables handle the same question asked in slightly different ways.

The design question is freshness: how old may an answer be?

<!-- example -->

```sql
-- summary table refreshed hourly; the dashboard reads it instead of raw events
INSERT INTO marts.sales_hourly
SELECT date_trunc('hour', created_at) AS hour, store_id, sum(amount) AS revenue
FROM sales.orders WHERE dt = '2026-10-17'
GROUP BY 1, 2;
```

#### What is query result reuse?

A feature where Athena returns a previous query's results if the same query was run recently (within a maximum age you set, up to 7 days) and the underlying data hasn't changed (for supported tables), without scanning data again.

#### How do you optimize queries on a large, frequently queried dimension combination?

Precompute aggregates in a summary table (`CTAS` or scheduled `INSERT`), keep it partitioned by date, and point dashboards to it instead of the raw table.

#### A QuickSight dashboard on Athena is slow and expensive. What do you change?

Pre-aggregate into a summary table refreshed on a schedule, use QuickSight SPICE to cache data, ensure partition filters are applied by the dashboard, convert source tables to Parquet or Iceberg with compaction, and consider capacity reservations for predictable concurrency.

<!-- challenge -->

A dashboard with 10 charts runs on raw events and takes 40 seconds to load. Data only changes hourly. What do you propose?

<!-- solution -->

Build hourly summary tables for the charts, refresh them on a schedule, and point the dashboard at them; enable result reuse or the BI tool's cache (SPICE) with a one-hour freshness.

<!-- takeaways -->

- Result reuse returns cached answers to identical queries.
- Summary tables serve repeated aggregations cheaply.
- Decide freshness first, then choose caching.

<!-- unit: Capacity and S3 limits -->

<!-- goals -->

- Decide when capacity reservations pay off.
- Recognize S3 throttling as a performance limit.

<!-- concept -->

On-demand Athena shares capacity with other customers and bills per scan. Capacity reservations buy dedicated processing for steady workloads, trading pay-per-query for predictable cost and concurrency.

Below the engine sits S3, which has its own limits per prefix. Queries over millions of small files can be throttled no matter how much compute is available, so file layout is also a throughput issue.

<!-- example -->

| Situation | Better choice |
|---|---|
| A few ad hoc queries a day | On-demand |
| BI all day, hundreds of users | Capacity reservation |
| `SlowDown` errors on many tiny files | Compact files, spread prefixes |

#### What are capacity reservations?

Dedicated query processing capacity bought in DPUs (for a minimum duration, then per minute) and assigned to workgroups. Queries in those workgroups run on the reserved capacity, billed per DPU-hour instead of per TB scanned, with predictable cost and concurrency.

#### When are capacity reservations worth it?

When query volume is high and steady (heavy BI dashboards, many concurrent users), when you need guaranteed concurrency for critical workloads, or when per-TB costs exceed the reserved capacity price.

#### Why can S3 throttling slow Athena queries?

S3 supports high request rates per prefix, but queries over millions of small files in one prefix can hit `SlowDown` (503) errors. Fewer, larger files and spreading data across prefixes (partitions) avoid it.

<!-- challenge -->

Your on-demand bill is 30,000 USD a month, mostly from BI queries running 8 hours a day. How do you evaluate a capacity reservation?

<!-- solution -->

Estimate the DPUs needed for peak concurrency from current query volume, price them for the working hours, and compare with on-demand spend. Assign only the BI workgroup to the reservation and keep ad hoc on-demand.

<!-- takeaways -->

- Reservations give dedicated capacity and predictable cost.
- They pay off for steady, high-volume workloads.
- Many tiny files can hit S3 request limits.

### Workgroups, cost control and monitoring

<!-- unit: Workgroups as guardrails -->

<!-- goals -->

- Set per-query and workgroup-wide limits.
- Enforce settings and allocate costs by team.

<!-- concept -->

In a pay-per-scan service, one careless query can cost more than a month of normal use. Workgroups put guardrails around that risk: each team or application gets its own settings, enforced result location and encryption, and limits that cancel or alert on large scans.

Workgroups also make costs visible, because tags and metrics attach every query to its owner.

<!-- example -->

```bash
aws athena update-work-group --work-group analysts \
  --configuration-updates 'EnforceWorkGroupConfiguration=true,BytesScannedCutoffPerQuery=107374182400'
# cancels any query scanning more than 100 GB
```

#### How do you limit costs per team?

Create a workgroup per team or application with a per-query data usage limit (cancels queries scanning more than a threshold) and workgroup-wide limits per period that trigger alarms, enforce workgroup settings so users can't override them, and tag workgroups for cost allocation.

#### What does "override client-side settings" mean for a workgroup?

When enabled, the workgroup's result location, encryption and other settings apply to every query, ignoring what clients specify, which enforces governance.

#### What is the difference between a per-query limit and a workgroup-wide limit?

A per-query control cancels any query scanning more than the threshold. Workgroup-wide controls measure total data scanned over a period and trigger CloudWatch alarms or SNS notifications, but don't cancel queries.

#### How do you prevent runaway queries?

Per-query data usage limits in workgroups, query timeouts, education on partition filters, views that require partition filters, and capacity reservations for predictable workloads.

#### How do you allocate Athena costs to teams?

Use separate workgroups per team, tag them with cost allocation tags, and analyze costs in Cost Explorer by tag; for capacity reservations, assign workgroups to reservations per team.

<!-- challenge -->

An intern's query scanned 40 TB over a weekend. What guardrails do you add?

<!-- solution -->

Put interns and analysts in a workgroup with a per-query limit (for example 1 TB) and a daily workgroup alert, enforce workgroup settings, and require partition filters through views or education.

<!-- takeaways -->

- Per-query limits cancel large scans.
- Enforced workgroup settings override clients.
- Tagged workgroups attribute costs to teams.

<!-- unit: Monitoring usage and failures -->

<!-- goals -->

- Monitor scans, durations and failures over time.
- Investigate cost increases systematically.

<!-- concept -->

Athena keeps query history for 45 days, and workgroups publish metrics, but neither answers "why did costs change?" on its own. Exporting query details lets you find the expensive queries and their trend.

Remember the hidden costs too: S3 requests are billed separately, so tables with many small files cost more than the Athena bill shows.

<!-- example -->

```sql
-- after exporting query executions to a table
SELECT workgroup, query_hash, sum(data_scanned_bytes) / 1e12 AS tb
FROM ops.athena_queries
WHERE day >= current_date - interval '7' day
GROUP BY 1, 2 ORDER BY tb DESC LIMIT 20;
```

#### How do you monitor Athena usage?

With CloudWatch metrics per workgroup (data scanned, query duration, queued time, failed queries), query history (`ListQueryExecutions`, console), CloudTrail for API calls, and cost reports with tags.

#### How long is query history kept?

Athena keeps query history for 45 days. For longer retention or analysis, export execution details (for example with EventBridge events or a scheduled job calling `GetQueryExecution`) to S3.

#### How do you find the most expensive queries?

From query history or exported execution data, sort by `DataScannedInBytes`; then check whether they filter on partitions, read CSV or JSON, or select too many columns.

#### How are Athena costs affected by S3 requests?

Athena's per-TB price doesn't include S3 GET and LIST requests, which are billed by S3. Tables with huge numbers of small files can generate significant request costs on top of Athena charges.

#### How do you track query failures?

CloudWatch metrics for failed queries per workgroup, EventBridge "Athena Query State Change" events routed to alerts, and query history with error messages.

#### Your Athena bill doubled. How do you investigate?

Check CloudWatch data scanned per workgroup, find top queries by bytes scanned in query history, look for new dashboards running unfiltered queries, `SELECT *` on wide tables, tables in CSV or JSON, and partition filters that stopped working (for example a function on the partition column). Then fix formats and filters and add per-query limits.

<!-- challenge -->

Costs rose 40% this month and no new team joined. Name the first three things you check.

<!-- solution -->

The top queries by bytes scanned this month versus last, new or changed scheduled queries (often a dashboard refresh rate), and tables whose partition filters stopped pruning after a schema or layout change.

<!-- takeaways -->

- Export query history for long-term analysis.
- Sort by bytes scanned to find expensive queries.
- S3 request costs sit outside the Athena bill.

### Federated queries and connectors

<!-- unit: Querying beyond S3 -->

<!-- goals -->

- Explain how federated queries reach databases and other sources.
- Weigh their convenience against performance and load.

<!-- concept -->

Federated queries let one SQL statement join lake data with live data in databases or other services. A Lambda connector translates part of the query for the source, pushes filters down when possible, and returns rows to Athena.

The convenience has costs: the source does real work, the Lambda has limits, and analytical scans can hurt an operational database. Federation suits small lookups and occasional joins, not regular heavy scans.

<!-- example -->

```sql
SELECT o.order_id, o.amount, c.segment
FROM lake.orders o
JOIN rds_pg.public.customers c ON o.customer_id = c.id
WHERE o.dt = '2026-10-17';
```

#### What is Athena Federated Query?

A feature that lets Athena query data outside S3, such as DynamoDB, RDS and Aurora (MySQL, PostgreSQL), Redshift, DocumentDB, OpenSearch, CloudWatch Logs, Snowflake, BigQuery and many others, through data source connectors that run as AWS Lambda functions (or as managed Glue connections).

#### How do federated connectors work?

The connector Lambda receives part of the query plan, reads data from the source (with filters and projections pushed down when possible) and returns it in Apache Arrow format to Athena, which then joins and aggregates it with other data.

#### What are the downsides of federated queries?

Performance depends on the source and the Lambda (timeouts, memory, concurrency), queries can load operational databases, pushdown is limited for some sources, and you pay for Lambda plus data scanned. For frequent heavy use, replicate the data to S3.

#### How do you join S3 data with an RDS table?

Register the RDS connector as a data source (for example `rds_pg`), then query `SELECT … FROM lake.orders o JOIN rds_pg.public.customers c ON o.customer_id = c.id`, keeping the RDS side small with filters.

#### How do you query DynamoDB with Athena?

With the DynamoDB connector, which scans or queries the table (consuming read capacity); for large analytical queries, export the table to S3 (DynamoDB export) and query the export instead.

<!-- challenge -->

A daily report joins a 2 TB lake table with a full scan of a production DynamoDB table, and the app slows down at that time. What do you change?

<!-- solution -->

Stop scanning DynamoDB live: export it to S3 (DynamoDB export to S3 in Parquet or a daily job) and join the exported copy. Keep federation for small, filtered lookups.

<!-- takeaways -->

- Connectors run in Lambda and push down filters.
- Federation is convenient but loads the source.
- Export large sources to S3 for regular analytics.

<!-- unit: Connectors and external functions -->

<!-- goals -->

- Deploy and operate federated connectors.
- Call Lambda UDFs and SageMaker models from SQL.

<!-- concept -->

Connectors and functions extend Athena with code you run. Both are Lambda functions, so they inherit Lambda's limits: response sizes (hence the spill bucket), timeouts and concurrency. Treat them like any service: deploy them as code, give them least-privilege roles, and monitor them.

External functions bring logic into SQL that the engine lacks, from decryption to model scoring, but each row crosses a network call.

<!-- example -->

```sql
USING EXTERNAL FUNCTION predict_churn(tenure int, spend double)
  RETURNS double SAGEMAKER 'churn-endpoint'
SELECT customer_id, predict_churn(tenure, spend) AS churn_score
FROM marts.customers WHERE dt = '2026-10-17';
```

#### How do you deploy a federated connector?

From the Athena console (creating a data source), which deploys the connector Lambda from the AWS Serverless Application Repository or uses Glue connections, with a spill bucket in S3 for large results and the right IAM and VPC settings.

#### What is the spill bucket for?

An S3 location where the connector writes data that exceeds Lambda's response size limits, which Athena then reads. It should be encrypted and have a lifecycle rule.

#### Can you write a custom connector?

Yes, with the Athena Query Federation SDK (Java), implementing metadata and record handlers for your source, deployed as a Lambda function.

#### What are user-defined functions in Athena?

Scalar functions implemented in a Lambda function (Java) and called with `USING EXTERNAL FUNCTION`, used for logic not available in SQL, such as calling an internal service or custom decryption.

#### Can Athena call machine learning models?

Yes, with `USING EXTERNAL FUNCTION … SAGEMAKER 'endpoint-name'`, which sends rows to a SageMaker endpoint for inference within a query.

<!-- challenge -->

A federated query fails with a Lambda response size error for large results. What is missing?

<!-- solution -->

A spill bucket, or one the connector can write to. Configure an S3 spill location with a lifecycle rule to delete old objects, and grant the connector role access to it.

<!-- takeaways -->

- Connectors and UDFs are Lambda functions with Lambda limits.
- The spill bucket handles large connector responses.
- External functions add logic per row at a network cost.

### Security and governance

<!-- unit: Access control with IAM and Lake Formation -->

<!-- goals -->

- Control who can query which tables, columns and rows.
- Mask or exclude sensitive data.

<!-- concept -->

With IAM alone, table access is really S3 access: whoever can read the files can read any table over them. Lake Formation moves control up to tables, columns and rows, and hands Athena temporary credentials for exactly what the user may see. That makes fine-grained rules like "EU analysts see EU rows without email" possible.

Masking adds another layer, through excluded columns, redacting views or masked copies.

<!-- example -->

```sql
-- Lake Formation data filter (defined in LF): row filter + excluded columns
--   table: lake.customers  row filter: country IN ('DE','FR','ES')  exclude: email, phone
SELECT customer_id, country, segment FROM lake.customers;   -- analyst sees only allowed data
```

#### How do you control access to Athena?

IAM policies on Athena actions and workgroups, S3 permissions on data and result locations, Glue Data Catalog permissions (databases, tables), and, for fine-grained control, Lake Formation permissions on databases, tables, columns, rows and cells.

#### How does Lake Formation work with Athena?

Athena checks Lake Formation permissions for the caller and only returns allowed columns and rows, using temporary credentials vended by Lake Formation to read S3, so users don't need direct S3 access to the data.

#### How do you restrict which S3 data a user can query?

Grant table access through Lake Formation (no direct S3 permissions needed), or with IAM limit S3 access to specific prefixes and Glue access to specific databases and tables.

#### What is Lake Formation's data filter?

A definition of row and cell-level security for a table (a row filter expression plus included or excluded columns) granted to principals; Athena enforces it at query time.

#### How do you mask sensitive columns in Athena?

Exclude them through Lake Formation column permissions, provide views that hash or redact them, or store masked copies in a separate curated table for broad access.

<!-- challenge -->

Analysts must query a customer table but must not see emails, and German analysts only German customers. How do you set it up?

<!-- solution -->

Register the location in Lake Formation, create a data filter excluding `email` with a row filter `country = 'DE'`, and grant it to the German analysts' role. Remove their direct S3 access to the table location.

<!-- takeaways -->

- IAM alone means file-level access.
- Lake Formation grants tables, columns and rows.
- Data filters combine row and column security.

<!-- unit: Encryption, networks and audit -->

<!-- goals -->

- Encrypt data and results and keep traffic private.
- Share data across accounts and audit usage.

<!-- concept -->

Security also covers the path around queries. Data and results should be encrypted with keys you control. Traffic can stay inside your network with VPC endpoints. Cross-account access works through shared catalogs rather than copying data.

Audit closes the loop: CloudTrail records who ran what, which matters when sensitive tables are involved.

<!-- example -->

```bash
aws athena update-work-group --work-group finance --configuration-updates \
 'ResultConfigurationUpdates={OutputLocation=s3://athena-results-finance/,EncryptionConfiguration={EncryptionOption=SSE_KMS,KmsKey=alias/finance}}'
```

#### How do you encrypt Athena data?

Data in S3 can be encrypted with SSE-S3, SSE-KMS or client-side KMS; Athena reads encrypted data transparently with the right KMS permissions. Query results can be encrypted (SSE-S3, SSE-KMS, CSE-KMS) per workgroup, and data in transit uses TLS.

#### How do you query data in another AWS account?

Through Lake Formation cross-account sharing (resource links), cross-account Glue catalog access registered as a data source, or bucket policies granting the querying role access to the data and its KMS key.

#### How do you audit Athena usage?

CloudTrail records API calls (who started which query, with the query text), Lake Formation logs data access, and S3 server access logs or CloudTrail data events record object reads.

#### How do you use Athena from a private network?

Through VPC interface endpoints for Athena (and for Glue, S3 and KMS as needed), so traffic doesn't traverse the internet; endpoint policies can restrict usage.

#### How do you give a BI tool access to Athena securely?

Create a dedicated IAM role or user (preferably federated with IAM Identity Center or OAuth for the driver), limited to one workgroup, the needed tables via Lake Formation, and the result location, and connect through the JDBC/ODBC driver.

<!-- challenge -->

A BI tool connects with an IAM user whose access keys never expire and have admin rights. How do you fix it?

<!-- solution -->

Create a dedicated role (or federated identity through the driver) limited to one workgroup and the needed tables via Lake Formation, use temporary credentials, and delete the long-lived keys.

<!-- takeaways -->

- Encrypt data and results with KMS.
- Share across accounts through catalogs, not copies.
- CloudTrail records who ran which query.

### Troubleshooting

<!-- unit: Missing or wrong results -->

<!-- goals -->

- Diagnose queries that return no rows, `NULL`s or duplicates.
- Fix partition registration and timestamp problems.

<!-- concept -->

When results look wrong in Athena, the cause is usually the contract between table and files, not the SQL. Partitions that aren't registered, a location that is slightly off, a SerDe that doesn't parse the values, or files written twice all produce plausible but wrong answers.

Work from the files up: list the location, check partitions, look at raw values with `"$path"`, then fix the definition or the pipeline.

<!-- example -->

```sql
SHOW PARTITIONS sales.orders;                 -- is today's partition there?
SELECT "$path", count(*) FROM sales.orders WHERE dt = '2026-10-17' GROUP BY 1;  -- duplicate files?
```

#### A query returns zero rows but the files exist. What do you check?

Whether partitions are registered (or projection is configured correctly), whether the `LOCATION` and storage location template match the real paths, whether the SerDe and columns match the format, and whether files are in subfolders that the table doesn't include.

#### Why does `MSCK REPAIR TABLE` add no partitions?

The folders aren't Hive-style (`key=value`), the key names don't match the partition column names (case matters), the location is wrong, or partition projection is enabled for the table.

#### Why do numbers show up as `NULL` from a CSV table?

Values contain characters that don't parse (thousand separators, currency symbols, quotes with `LazySimpleSerDe`, empty strings), or columns are shifted because a field contains the delimiter. Use `OpenCSVSerDe`, clean the data, or read as strings and `TRY_CAST`.

#### Why does a query on timestamps return wrong results?

Timestamps stored as strings in different formats, time zone confusion (Athena timestamps without time zone are interpreted as UTC in many cases), or Parquet timestamp encodings that differ between writers. Parse explicitly with `from_iso8601_timestamp` or `parse_datetime` and convert time zones with `AT TIME ZONE`.

#### Results contain duplicates after a pipeline rerun. Why?

The pipeline used `INSERT INTO` on a Hive table without removing the previous output, or files were written twice to the same location. Make writes idempotent (overwrite partitions, use Iceberg `MERGE`) and deduplicate the affected partitions.

<!-- challenge -->

Yesterday's data is in S3 at `s3://lake/orders/2026/10/17/`, but `WHERE dt = '2026-10-17'` returns nothing. What is the likely cause and fix?

<!-- solution -->

The path isn't Hive-style, so neither `MSCK REPAIR` nor the catalog knows the partition. Add it with `ALTER TABLE ADD PARTITION ... LOCATION`, or configure projection with a location template matching `${year}/${month}/${day}`.

<!-- takeaways -->

- Check partitions and locations before the SQL.
- Parse errors become `NULL`s silently.
- Duplicates usually mean non-idempotent writes.

<!-- unit: Reading Hive errors -->

<!-- goals -->

- Interpret common `HIVE_*` and permission errors.
- Locate the file or object causing them.

<!-- concept -->

Error messages in Athena name the layer that failed. Schema mismatch errors point to the catalog, cursor and bad-data errors point to the files, and access denied can come from any of five permission layers. Reading the error first saves guessing.

Most file-level errors are fixed by finding the offending file with `"$path"` and moving or fixing it.

<!-- example -->

| Error | Look at |
|---|---|
| `HIVE_PARTITION_SCHEMA_MISMATCH` | partition vs table schema in the catalog |
| `HIVE_CURSOR_ERROR` | corrupt or wrong-format file |
| `HIVE_BAD_DATA` | a value that doesn't fit the type |
| `Access Denied` | S3, results bucket, KMS, Glue, Lake Formation |

#### What does `HIVE_PARTITION_SCHEMA_MISMATCH` mean?

A partition's schema in the catalog differs from the table's schema (types or columns). Make partitions inherit the table schema (crawler setting or recreating partitions) and stabilize the source.

#### What does `HIVE_CURSOR_ERROR` usually indicate?

A problem reading a file: corrupted or truncated files, a format different from the table definition, an unreadable compressed file, or permissions or KMS issues on some objects.

#### What does `HIVE_BAD_DATA` mean?

A value can't be parsed as the declared type, for example text in a numeric column, a malformed JSON record, or a Parquet type mismatch. Fix the data, the table types, or use `TRY_CAST` over string columns.

#### Why do you get `Access Denied` on a query?

Missing permissions on the S3 data, the query result location, the KMS key, the Glue catalog objects, Lake Formation grants, or the workgroup. The error message usually names the resource.

<!-- challenge -->

A user gets `Access Denied` though they have full S3 read access to the data. List three other places to check.

<!-- solution -->

Write access to the query result location, decrypt permission on the KMS key used by the data or results, and Glue catalog (or Lake Formation) permissions on the database and table.

<!-- takeaways -->

- The error names the layer that failed.
- Use `"$path"` to find bad files.
- Access needs S3, results, KMS, Glue and Lake Formation.

<!-- unit: Slow and failing queries -->

<!-- goals -->

- Diagnose slow queries that scan little data.
- Fix timeouts, throttling and Iceberg slowdowns.

<!-- concept -->

Not all slowness comes from scanning. Planning many partitions, opening many small files, waiting on S3 throttling or on a slow federated source all take time that bytes-scanned metrics don't show. The execution statistics split the time into queue, planning and execution, which points to the culprit.

Iceberg tables slow down for a related reason: frequent writes leave small files and delete files until maintenance cleans them.

<!-- example -->

```text
QueryQueueTime:      0.2 s
QueryPlanningTime:  48.7 s   ← partition metadata, not data
EngineExecutionTime: 3.1 s
DataScannedInBytes:  120 MB
```

#### A query is slow but scans little data. What could cause it?

Planning time on tables with many partitions (use projection or partition indexes), many tiny files (per-file overhead), a federated source, queuing behind concurrency limits, or an expensive operation such as a large join or global sort.

#### Why do you get "Query timeout"?

The query exceeded the workgroup's timeout: scanning too much data, a heavy join or sort, or a slow federated source. Optimize the query or data layout, materialize intermediate steps, or raise the timeout quota.

#### Why are there "too many open files" or S3 `SlowDown` errors?

Tables with an enormous number of small files cause many concurrent S3 requests. Compact the files and spread them across partitions.

#### Why does an Iceberg query get slower over time?

Many small files and delete files accumulate with frequent writes and row-level changes. Schedule `OPTIMIZE` and `VACUUM` (or use automatic compaction in the Glue catalog or S3 Tables).

<!-- challenge -->

An Iceberg table updated every 5 minutes is now ten times slower to query than last month. What do you schedule?

<!-- solution -->

Regular `OPTIMIZE ... REWRITE DATA USING BIN_PACK` to compact small and delete files, and `VACUUM` to expire old snapshots, for example daily. Consider batching the updates less frequently if freshness allows.

<!-- takeaways -->

- Check queue, planning and execution time separately.
- Many partitions or files slow planning, not scanning.
- Iceberg tables need regular compaction.

<!-- stage: Putting it together -->

### Scenarios

<!-- unit: Designing log and event analytics -->

<!-- goals -->

- Design a cheap, fast analytics path from events to queries.
- Balance freshness against cost and file sizes.

<!-- concept -->

Athena designs succeed or fail on the write path. Queries are cheap and fast when data lands in columnar files of a good size, partitioned by the filters people use, and registered without manual steps. A good answer follows the data from producer to query and names a choice at each step, then explains the freshness and cost trade-off: shorter buffers mean fresher data but smaller files.

<!-- example -->

```text
apps ─► Firehose (buffer 5 min, convert to Parquet, dt/hour prefixes)
     ─► S3 lake ─► table with partition projection
     ─► workgroup with limits ─► dashboards on hourly summary tables
```

#### Design a cheap log analytics solution with Athena.

Deliver logs to S3 with Firehose (buffered, converted to Parquet, partitioned by date), define a table with partition projection on date, create views for common questions, set up a workgroup with data limits, and give analysts access via Lake Formation. Add lifecycle rules to move old logs to cheaper storage classes.

#### How would you build near-real-time dashboards on Athena?

Stream events with Firehose to S3 in Parquet with short buffers, partition by date and hour with projection, build small aggregate tables every few minutes with scheduled `INSERT INTO` or `MERGE` into Iceberg, and point dashboards to the aggregates; for sub-minute latency, use a different store such as OpenSearch or a streaming database.

<!-- challenge -->

The business wants dashboards updated every minute instead of every 15. What changes, and what does it cost?

<!-- solution -->

Shorten the Firehose buffer and refresh more often, which creates many more small files and more queries. Add compaction (or Iceberg with `OPTIMIZE`) and query summary tables; if one-minute latency is truly needed, consider a streaming store instead of Athena.

<!-- takeaways -->

- Design the write path: format, size, partitions, registration.
- Freshness costs file size and query volume.
- Serve dashboards from summaries, not raw events.

<!-- unit: Migrations and governed self-service -->

<!-- goals -->

- Plan a migration of reports onto Athena.
- Set up governed, budget-controlled access to a large lake.

<!-- concept -->

Moving people onto Athena is as much about control as about SQL. A migration needs data in good formats, translated queries and side-by-side validation. Self-service needs guardrails so that freedom doesn't turn into runaway cost or data leaks: permissions by domain, workgroups with limits, curated tables and monitoring. Both questions test whether you see Athena as part of a platform, not a single tool.

<!-- example -->

| Concern | Control |
|---|---|
| Who sees what | Lake Formation permissions per domain |
| How much they spend | Workgroup per team, per-query limit |
| How fast and cheap queries are | Partitioned Parquet or Iceberg, summaries |
| What happened | CloudTrail, query history export |

#### How do you migrate reports from an on-premises SQL Server to Athena?

Export tables to S3 as Parquet (DMS or exports), define Glue tables or Iceberg tables, translate T-SQL to Trino SQL (functions, date handling, `TOP` to `LIMIT`, no `PIVOT`), recreate views, validate results by comparing aggregates, and connect the BI tool via the driver.

#### A team needs ad hoc SQL access to a 50 TB data lake with tight budget control. What do you set up?

Lake Formation permissions by domain, a workgroup per team with per-query limits, Parquet or Iceberg tables partitioned by date, views that enforce partition filters, query result reuse, documentation of tables, and monthly reports of bytes scanned per team.

<!-- challenge -->

After migrating reports, totals differ slightly from SQL Server for some days. How do you find the cause?

<!-- solution -->

Compare per day and per key to localize the difference, then inspect the rows. Typical causes: time zones on timestamps, `double` versus `decimal`, `NULL` handling in joins, and T-SQL functions translated with different semantics.

<!-- takeaways -->

- Migrations need formats, translation and validation.
- Self-service needs permissions, limits and curated data.
- Validate by comparing aggregates per key and day.
