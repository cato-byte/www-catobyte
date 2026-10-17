## AWS Glue Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![AWS Glue study guide: about 200 questions](../../images/aws_glue_study_guide_title_img.png)

About 200 interview-style questions on AWS Glue: the Data Catalog, crawlers, Spark ETL jobs, DynamicFrames, job bookmarks, workers and cost, streaming, data quality, orchestration, security with Lake Formation, and performance tuning. The answers reflect the service as of 2026. Open a question to see its answer, or use the filter to search the whole guide.

<!-- QA -->

### Fundamentals

#### What is AWS Glue?

A serverless data integration service on AWS for discovering, preparing, moving and integrating data. Its main parts are the Glue Data Catalog (a central metadata repository), crawlers (schema discovery), ETL jobs (Apache Spark or Python), Glue Studio (visual authoring), Data Quality, DataBrew (visual data preparation) and workflows for orchestration.

#### What does "serverless" mean for Glue?

You don't provision or manage clusters: you choose a worker type and number (or let auto scaling decide), Glue starts the environment for the job run, and you pay only for the time the job runs, per second.

#### What are the main use cases for Glue?

Building data lakes on S3 (cataloging and transforming raw data into Parquet or Iceberg), ETL into Redshift or other databases, preparing data for Athena and machine learning, CDC and streaming ingestion, and providing a shared metadata catalog for Athena, EMR, Redshift Spectrum and Lake Formation.

#### What is the Glue Data Catalog?

A managed, Hive-metastore-compatible metadata repository per account and region. It stores databases, tables (schema, location, format, partitions, statistics), connections and user-defined functions. Athena, EMR, Redshift Spectrum, Glue jobs and many other services use it to know where data is and how to read it.

#### What is a Glue database?

A logical container for tables in the Data Catalog. It doesn't store data itself; it groups table definitions, and permissions can be granted at the database level with Lake Formation.

#### What is a Glue table?

Metadata that describes data: column names and types, the S3 location (or a JDBC source), the format (SerDe and input/output formats), partition keys and table properties. The data itself stays in S3 or in the source database.

#### How does Glue compare with Amazon EMR?

Glue is serverless and focused on ETL with Spark, with built-in catalog, bookmarks and quality features; you trade control for simplicity. EMR (on EC2, EKS or Serverless) gives full control of Spark, Hadoop, Hive, Trino and other frameworks, versions and tuning, and is often cheaper for large, steady workloads.

#### How does Glue compare with AWS Lambda for ETL?

Lambda suits small, event-driven transformations (a file of a few MB) with a 15-minute limit and limited memory. Glue suits larger, distributed processing with Spark, longer runtimes and big volumes.

#### What is a DPU?

A Data Processing Unit: 4 vCPU and 16 GB of memory. Glue bills ETL jobs, crawlers and interactive sessions in DPU-hours, per second.

#### How is a Glue job billed?

Per DPU-hour, per second, with a 1-minute minimum for Spark jobs on Glue 2.0 and later. The cost is number of DPUs × duration × price per DPU-hour (about 0.44 USD in many regions, Flex cheaper). Python shell jobs bill 1/16 or 1 DPU.

#### What are the Glue versions, and why do they matter?

Each Glue version bundles a Spark, Python and Java version and connectors: for example Glue 4.0 runs Spark 3.3 and Python 3.10, and Glue 5.0 runs Spark 3.5 and Python 3.11. Newer versions start faster, run faster and support newer table formats. Older versions reach end of support, so upgrades are part of maintenance.

#### What is Glue Studio?

The console experience for creating, running and monitoring Glue jobs: a visual editor where you build ETL as a graph of sources, transforms and targets (which generates PySpark code), a script editor, a notebook editor, and job monitoring dashboards.

#### What is AWS Glue DataBrew?

A visual data preparation tool with 250+ built-in transformations, used by analysts to clean and normalize data without code. Transformations are saved as recipes and run as jobs on S3 data, with data profiling.

#### How does Glue fit into the AWS data lake architecture?

Data lands in S3 (from DMS, Kinesis, AppFlow, uploads), crawlers or jobs register it in the Data Catalog, Glue jobs clean and convert it into curated zones (Parquet or Iceberg), Lake Formation governs access, and Athena, Redshift, EMR, QuickSight and SageMaker consume it.

#### What is the relationship between Glue and SageMaker Lakehouse/Unified Studio?

The Glue Data Catalog is the metadata foundation of SageMaker Lakehouse, and Glue's data integration features (ETL jobs, visual ETL, connections, zero-ETL) are available inside SageMaker Unified Studio, AWS's combined environment for data, analytics and AI.

#### What are the main components of AWS Glue, in one sentence each?

The Data Catalog stores metadata; crawlers discover schemas; ETL jobs transform data with Spark or Python; triggers and workflows orchestrate; Glue Studio provides visual authoring; Data Quality validates data; DataBrew prepares data visually; the Schema Registry governs streaming schemas.

#### What is ETL versus ELT in the context of Glue?

With ETL, Glue jobs transform data before loading it into the target (for example cleaning and converting to Parquet before Redshift). With ELT, raw data is loaded first and transformed inside the target (Redshift SQL, dbt on Athena). Glue is often used for the "E" and "L" of ELT, or as the "T" in a lakehouse.

#### What are Glue service quotas you should know?

Limits on concurrent job runs per account, maximum DPUs per job, number of jobs, triggers, crawlers, databases, tables and partitions per table. Most are adjustable through Service Quotas; large data lakes hit partition and concurrency limits first.

#### In which regions is Glue available, and is the catalog regional?

Glue is available in most AWS regions, and the Data Catalog is regional: each region has its own catalog per account. Cross-region access needs replication of metadata or resource links in Lake Formation.

#### What is a development endpoint, and what replaced it?

A legacy, always-on environment for developing Glue scripts from notebooks, billed while running. Interactive sessions and Glue Studio notebooks replaced it with on-demand, per-second billing and idle timeouts.

### Data Catalog

#### How do tables get into the Data Catalog?

By running crawlers, by creating tables manually (console, `CREATE EXTERNAL TABLE` in Athena, CloudFormation, Terraform, the API), from Glue jobs that create or update tables when writing (`enableUpdateCatalog`), or from services such as Lake Formation blueprints and zero-ETL integrations.

#### What is a partition in the Data Catalog?

A subset of a table's data defined by partition key values (for example `year=2026/month=10/day=15`), each with its own S3 location. Query engines read only the partitions matching filters, which cuts cost and time.

#### How are new partitions registered?

By a crawler, by `MSCK REPAIR TABLE` or `ALTER TABLE ADD PARTITION` in Athena, by the `BatchCreatePartition` API, by Glue jobs writing with catalog updates, or avoided entirely with Athena partition projection.

#### What are partition indexes?

Indexes on partition keys of catalog tables with many partitions, so `GetPartitions` calls with filters return quickly instead of scanning all partitions. They speed up query planning in Athena and Glue on tables with tens of thousands of partitions.

#### What are column statistics in the Data Catalog?

Statistics (number of distinct values, nulls, min/max, average length) computed by Glue for table columns and stored in the catalog, which Athena and Redshift Spectrum use for cost-based optimization such as join reordering.

#### What is a Glue connection?

A catalog object that stores connection properties for a data store: JDBC URL, credentials (preferably a Secrets Manager secret), VPC, subnet and security groups, or properties for Kafka, MongoDB, Snowflake, BigQuery and other native connectors. Jobs and crawlers reference it.

#### What table formats does the Data Catalog support?

Hive-style tables in Parquet, ORC, Avro, JSON, CSV and other formats, and open table formats Apache Iceberg, Apache Hudi and Delta Lake. Iceberg is the most deeply integrated across AWS services.

#### What are catalog optimizations for Iceberg tables?

Managed table maintenance for Iceberg tables in the Data Catalog: automatic compaction of small files, snapshot retention (expiring old snapshots) and orphan file deletion, configured per table and run by Glue without your own jobs.

#### Can several AWS accounts share one Data Catalog?

Yes. Access can be granted across accounts with resource policies on the catalog or, more commonly, with Lake Formation cross-account grants (often through AWS RAM), so a central governance account shares databases and tables with consumer accounts.

#### What is the catalog ID?

The AWS account ID that owns a Data Catalog. APIs and queries can reference another account's catalog by its ID when cross-account access is granted.

#### How do you version table schemas in the Data Catalog?

The catalog keeps table versions automatically when a table is updated (up to a limit), so you can see and compare earlier schemas with `GetTableVersions`. Iceberg tables also keep schema history in their own metadata.

#### What is the Glue Schema Registry?

A service to store, version and validate schemas (Avro, JSON Schema, Protobuf) for streaming data, with compatibility rules (backward, forward, full). Producers and consumers using Kafka, MSK, Kinesis or Lambda serialize and validate records against registered schemas.

#### What is a resource link?

A Lake Formation object that points to a shared database or table from another account or region, so users can query it as if it were local in their own catalog.

#### What is the difference between an external table and a governed table?

In the Data Catalog all S3-based tables are external (the catalog only holds metadata, dropping it doesn't delete data). Governed tables were a Lake Formation table type with ACID transactions, now retired in favor of Apache Iceberg tables.

#### How do you query the Data Catalog programmatically?

With the Glue API (`GetDatabases`, `GetTables`, `GetPartitions`, `SearchTables`) through boto3 or the CLI, or with SQL through Athena's `information_schema` views.

#### How is the Data Catalog billed?

The first million objects stored and the first million requests per month are free; beyond that you pay per 100,000 objects and per million requests. Statistics computation and Iceberg optimizations are billed separately in DPU-hours.

#### What are table properties like `classification` and `compressionType` used for?

They tell engines and Glue how to interpret the data: `classification` (csv, json, parquet) is set by crawlers and used by Glue jobs, while SerDe parameters and compression settings tell Athena or Hive how to parse the files.

#### What is a user-defined function in the Data Catalog?

Metadata for a Hive UDF (class name and JAR location) stored in the catalog so engines like EMR Hive can use it, mostly relevant for Hive-compatible workloads.

#### How do you keep a Data Catalog clean?

Define naming conventions per layer (`raw_`, `curated_`), manage tables as code, remove tables created by accidental crawls, document tables and columns with descriptions, apply LF-Tags for classification, and monitor for unused tables.

### Crawlers

#### What is a crawler?

A Glue component that connects to a data store (S3, JDBC databases, DynamoDB, MongoDB, Delta, Iceberg, Hudi), samples the data, infers schemas and partitions with classifiers, and creates or updates tables in the Data Catalog. It can run on demand or on a schedule.

#### What is a classifier?

The logic that recognizes a data format and its schema. Glue has built-in classifiers (CSV, JSON, Parquet, Avro, ORC, XML, logs and more), and you can add custom classifiers with grok patterns, XML tags, JSON paths or CSV settings.

#### How does a crawler decide how many tables to create?

It groups files with compatible schemas under a common prefix into one table, using folder structure to detect partitions. If schemas differ too much, it creates several tables. The "create a single schema for each S3 path" option forces one table per include path.

#### What is the schema change policy of a crawler?

Settings for what to do when the schema changes or objects are deleted: update the table or only log changes, and delete, deprecate or ignore removed tables and partitions. Production teams often log changes rather than update automatically, to avoid surprises.

#### What are incremental crawls?

Crawls that only process folders added since the last run (and with S3 event mode, only changed objects from an SQS queue), which is much faster and cheaper for large, growing data lakes.

#### What is S3 event mode for crawlers?

A mode where the crawler reads S3 event notifications from an SQS queue to know exactly which objects changed, instead of listing the whole prefix.

#### What are common problems with crawlers?

Too many tables created because of inconsistent schemas or folder structures, wrong types inferred from CSV samples, `HIVE_PARTITION_SCHEMA_MISMATCH` errors when partitions have different schemas, cost and time on huge prefixes, and silent schema changes breaking downstream queries.

#### Should you always use crawlers?

No. Crawlers are convenient for discovery and for sources you don't control. For pipelines you own, defining tables explicitly (infrastructure as code) and registering partitions from jobs, or using partition projection, gives predictable schemas and no crawler cost.

#### How are crawlers billed?

Per DPU-hour for the time they run, per second with a minimum duration per run. Crawling millions of small files can be expensive; use include/exclude patterns, sampling and incremental crawls.

#### What are exclude patterns?

Glob patterns that tell a crawler to skip files or folders, such as `**/_temporary/**`, `**.crc` or `**/_SUCCESS`, which avoids junk tables and saves time.

#### Can a crawler crawl a JDBC database?

Yes. Through a Glue connection, it reads table definitions from databases such as MySQL, PostgreSQL, Oracle and SQL Server using an include path like `mydb/%` and creates catalog tables that jobs can read.

#### How do crawlers infer types from CSV files?

By sampling the first rows and choosing types that fit; if a column has mixed values (like numbers with a few blanks or text), the crawler may choose `string`, or pick a type that later rows break. Define CSV tables explicitly for predictable types.

#### How do crawlers handle headers in CSV?

The built-in CSV classifier guesses whether the first row is a header by checking whether it looks different from the data rows. When guessing fails, a custom CSV classifier with an explicit header setting fixes it.

#### Can crawlers create Iceberg or Delta tables?

Yes. Crawlers can register existing Delta Lake, Iceberg and Hudi tables from S3 by reading their metadata, creating catalog tables that point to the table format (natively or via manifests, depending on configuration).

#### What is the "recrawl policy"?

The setting that decides whether to crawl all folders again on each run or only new folders since the last crawl (incremental), or use S3 events.

#### How do you limit the scope of a crawler?

With precise include paths, exclude patterns, a sample size per folder (for S3), table level settings (at which folder depth tables are created) and separate crawlers per source.

#### What does "table level" mean in crawler configuration?

The folder depth at which the crawler creates tables. Setting it avoids crawlers making tables at the wrong level, for example treating each partition folder as a separate table.

### Glue ETL jobs

#### What job types does Glue offer?

Spark jobs (batch ETL with PySpark or Scala), Spark streaming jobs (continuous processing from Kinesis, Kafka or MSK), and Python shell jobs (single-node Python scripts for small tasks).

#### What does a basic Glue PySpark job look like?

```python
import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

args = getResolvedOptions(sys.argv, ["JOB_NAME", "target_path"])
glue = GlueContext(SparkContext.getOrCreate())
spark = glue.spark_session
job = Job(glue)
job.init(args["JOB_NAME"], args)

orders = glue.create_dynamic_frame.from_catalog(
    database="raw", table_name="orders", transformation_ctx="orders")
df = orders.toDF().filter("status = 'paid'")
df.write.mode("append").partitionBy("order_date").parquet(args["target_path"])

job.commit()
```

#### What is `GlueContext`?

A wrapper around the `SparkContext` that adds Glue functionality: reading and writing DynamicFrames from the catalog, S3 and connections, job bookmarks, and Glue-specific options.

#### What do `job.init()` and `job.commit()` do?

`init` starts the job state, and `commit` saves job bookmark state at the end of a successful run. Without `commit`, bookmarks don't advance and the next run reprocesses the same data.

#### How do you pass parameters to a Glue job?

As job arguments (`--target_path s3://...`) set in the job definition or overridden at run start, read with `getResolvedOptions`. Special arguments configure Glue itself, such as `--job-bookmark-option`, `--enable-metrics`, `--additional-python-modules` or `--conf`.

#### How do you add Python libraries to a Glue job?

With `--additional-python-modules` (installs from PyPI or wheels in S3 at start-up), `--extra-py-files` (zip or py files in S3), or by packaging dependencies in a wheel. For jobs without internet access, host wheels in S3 or use a private repository through a VPC endpoint.

#### How do you add JAR dependencies?

With `--extra-jars` pointing to JAR files in S3, used for JDBC drivers or Spark libraries not included in the Glue version.

#### What is a Python shell job good for?

Lightweight tasks that don't need Spark: calling APIs, running SQL on Redshift or Athena, moving small files, triggering other services. It runs on 1/16 or 1 DPU with Python and common libraries such as pandas and boto3.

#### What is Glue Flex execution?

A job execution class that runs on spare capacity at a lower price, with possibly longer start times and no guarantee of immediate start. It suits non-urgent workloads such as nightly batch, tests and backfills.

#### What is auto scaling for Glue jobs?

With auto scaling enabled (Glue 3.0+), Glue adds and removes workers during a run according to the workload, up to the maximum you set, so you don't pay for idle workers in stages with little parallelism.

#### What are job timeouts and retries?

`Timeout` stops a job after a number of minutes (default 48 hours for batch jobs, which is risky; set a realistic value). `MaxRetries` reruns failed jobs automatically; only use it when the job is idempotent.

#### What is maximum concurrency of a job?

The number of runs of the same job allowed at once (default 1). If a run is still active, new start requests fail with `ConcurrentRunsExceededException` unless you raise it.

#### How do you write to Redshift from a Glue job?

Through a Redshift connection, writing a DynamicFrame with `glue.write_dynamic_frame.from_jdbc_conf` (Glue stages the data in S3 and runs `COPY`), or with the Spark Redshift connector. `preactions` and `postactions` run SQL before and after, for example to `TRUNCATE` a staging table and then `MERGE` into the target.

#### How do you read from a JDBC database in parallel?

With `hashfield`/`hashpartitions` options on DynamicFrames, or `partitionColumn`, `lowerBound`, `upperBound` and `numPartitions` on Spark's JDBC reader, so several tasks read ranges concurrently instead of one connection reading everything.

#### Can Glue jobs write Iceberg, Hudi or Delta tables?

Yes. Set `--datalake-formats` to `iceberg`, `hudi` or `delta` (with the matching Spark configs) and use Spark SQL or DataFrame APIs, including `MERGE INTO`, with the Glue Data Catalog as the catalog.

```python
spark.sql("""
MERGE INTO glue_catalog.curated.customers t
USING updates s ON t.customer_id = s.customer_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
""")
```

#### What is the temporary directory (`--TempDir`) used for?

An S3 location where Glue writes intermediate data, for example when loading into Redshift or for shuffle in some configurations. It should have a lifecycle rule to delete old files.

#### What are Glue interactive sessions?

On-demand Spark sessions you use from Jupyter notebooks, Glue Studio notebooks or your IDE to develop and debug Glue code interactively, billed per second with an idle timeout.

#### How do you develop Glue jobs locally?

With the official Glue Docker images (which include the Glue libraries and Spark of a given Glue version), running scripts and pytest locally, or with interactive sessions from a local notebook. Pure PySpark logic can also be tested with a local SparkSession.

#### What is the difference between the Spark script editor and the visual editor?

The visual editor builds jobs as a graph of nodes and generates code; it's quick for standard ETL and accessible to analysts. The script editor gives full control over PySpark or Scala code. Many teams start visually, then switch to code managed in Git.

#### How do you use Spark SQL inside a Glue job?

Convert to a DataFrame, register a temporary view, and run `spark.sql()`. With the Data Catalog enabled as the Hive metastore (`--enable-glue-datacatalog`), you can query catalog tables directly by `database.table`.

#### What does `--enable-glue-datacatalog` do?

It configures Spark in the job to use the Glue Data Catalog as its Hive metastore, so `spark.sql("SELECT * FROM raw.orders")` and `saveAsTable` work against catalog tables.

#### How do you read JSON with nested structures in Glue?

Read it as a DynamicFrame or DataFrame (schema inferred or declared), then flatten with `select` of nested fields, `explode` for arrays, or Glue's `Relationalize` for a fully relational output.

#### How do you handle bad records when reading files?

For Spark readers, use `mode` (`PERMISSIVE` with a corrupt record column, `DROPMALFORMED`, `FAILFAST`) or `badRecordsPath` where supported; for DynamicFrames, errors are captured per record and can be inspected with `errorsAsDynamicFrame()` and thresholds set with `stageThreshold` and `totalThreshold`.

#### How do you write output with a controlled number of files?

Repartition or coalesce before writing (`df.repartition(20, "order_date")`), or set `spark.sql.files.maxRecordsPerFile`, so each partition gets a few large files instead of hundreds of small ones.

#### What is the Glue job run ID used for?

It identifies a run for monitoring, logs, bookmark rewinds and retries, and can be passed into outputs (for example as a column) for lineage.

#### How do you read from DynamoDB in Glue?

With the DynamoDB connector: either directly (consumes read capacity, controlled by `dynamodb.throughput.read.percent`) or through DynamoDB export to S3 (`dynamodb.export`), which doesn't consume table capacity and is preferred for large tables.

#### How do Glue jobs connect to Snowflake, BigQuery or other non-AWS sources?

Through native Glue connectors for many sources (Snowflake, BigQuery, Teradata, SAP HANA, MongoDB and SaaS applications), through AWS Marketplace connectors, or through JDBC with a custom driver and Glue connection.

#### What are job run states?

`STARTING`, `RUNNING`, `STOPPING`, `STOPPED`, `SUCCEEDED`, `FAILED`, `TIMEOUT`, `ERROR` and `WAITING`. EventBridge receives state change events for alerts and orchestration.

#### What happens to logs of a Glue job?

Driver and executor logs go to CloudWatch Logs (`/aws-glue/jobs/output` and `/aws-glue/jobs/error`); continuous logging streams them during the run. Use `glue.get_logger()` for structured messages.

### DynamicFrames and transforms

#### What is a DynamicFrame?

Glue's distributed data structure, similar to a Spark DataFrame but where each record is self-describing, so it doesn't need a fixed schema upfront. It handles inconsistent and messy data (a field that is sometimes a string and sometimes an int) with "choice" types.

#### What is the difference between a DynamicFrame and a DataFrame?

A DataFrame has one schema for the whole dataset and the full Spark SQL optimizer and API. A DynamicFrame computes schema per record, supports choice types and Glue-specific transforms, bookmarks and catalog integration. You convert with `toDF()` and `DynamicFrame.fromDF()`, and most teams use DataFrames for transformations.

#### What is a choice type, and how does `ResolveChoice` work?

When a column has values of different types, a DynamicFrame keeps a choice type (for example `choice<int,string>`). `ResolveChoice` resolves it with `cast:long`, `make_cols` (split into `col_int` and `col_string`), `make_struct` or `project:string`.

```python
resolved = dyf.resolveChoice(specs=[("amount", "cast:double"), ("id", "cast:long")])
```

#### What does `ApplyMapping` do?

It renames columns, casts types and selects fields in one step, from a list of `(source, source_type, target, target_type)` tuples, which is how Glue Studio's mapping node works.

#### What does `Relationalize` do?

It flattens nested JSON into a set of relational tables: nested structs become columns and arrays become separate tables linked by generated keys, ready to load into a relational database.

#### What are other built-in Glue transforms?

`DropFields`, `SelectFields`, `RenameField`, `Filter`, `Map`, `Join`, `SplitFields`, `SplitRows`, `Unbox` (parse JSON strings), `DropNullFields`, `FillMissingValues`, `FindMatches` (ML deduplication) and, in Glue Studio, transforms such as `Aggregate`, `Pivot`, `Derived column`, `Identify sensitive data` and `Evaluate data quality`.

#### What is FindMatches?

A machine learning transform that identifies duplicate or matching records that don't share a common key (for example the same customer with different spellings), trained with labeled examples.

#### Why do many teams convert DynamicFrames to DataFrames early?

DataFrames have a richer API, the Catalyst optimizer, better performance for most transformations and are portable to other Spark environments. DynamicFrames are mainly useful at read time (catalog, bookmarks, choice resolution) and write time (catalog updates, connectors).

#### How do you write a DynamicFrame and update the catalog?

```python
sink = glue.getSink(connection_type="s3", path="s3://lake/curated/orders/",
                    enableUpdateCatalog=True, updateBehavior="UPDATE_IN_DATABASE",
                    partitionKeys=["order_date"])
sink.setFormat("glueparquet")
sink.setCatalogInfo(catalogDatabase="curated", catalogTableName="orders")
sink.writeFrame(dyf)
```

#### What is the `glueparquet` format?

A Glue-optimized Parquet writer for DynamicFrames that computes the schema while writing, avoiding an extra pass over the data, which speeds up writes of large datasets.

#### What is `transformation_ctx`?

A unique name for each source and transform in a job, used by job bookmarks to store state. Without it on a source, bookmarks don't work for that source.

#### How do you filter a DynamicFrame?

With `Filter.apply(frame=dyf, f=lambda row: row["status"] == "paid")` or `dyf.filter(...)`, though converting to a DataFrame and using `filter("status = 'paid'")` is usually faster because Spark can optimize it.

#### How do you join DynamicFrames?

With `Join.apply(dyf1, dyf2, "key1", "key2")`, which performs an equality join; for other join types or conditions, convert to DataFrames.

#### What does `Unbox` do?

It parses a string column containing JSON (or CSV) into a struct, so nested fields become accessible columns.

#### What does `SplitFields` do?

It splits a DynamicFrame into two collections by columns, for example separating PII columns from the rest to write them to different locations.

#### How do you deduplicate in a Glue job?

Convert to a DataFrame and use `dropDuplicates(["key"])` or a window function with `row_number()` ordered by an update timestamp, keeping the latest record per key.

#### How do you add audit columns in a Glue job?

Add columns such as `ingested_at` (`current_timestamp()`), `source_file` (`input_file_name()` or file metadata), `job_run_id` and `process_date`, so every row can be traced to the run and file that produced it.

### Job bookmarks and incremental processing

#### What are job bookmarks?

A Glue feature that stores state between job runs so each run processes only new data: for S3 sources, which files (by modification time) were processed; for JDBC sources, the highest values of bookmark key columns.

#### How do you enable and control job bookmarks?

With `--job-bookmark-option`: `job-bookmark-enable`, `job-bookmark-disable` or `job-bookmark-pause` (process from the last bookmark without updating it). The source needs a `transformation_ctx` and the script must call `job.commit()`.

#### How do you reset or rewind a bookmark?

With the console or the `ResetJobBookmark` API, which makes the next run reprocess everything; you can also rewind to a previous run ID to reprocess from that point.

#### What are the limits of job bookmarks?

They track files by modification time, so overwritten files with the same name may be missed or reprocessed; JDBC bookmarks need monotonically increasing key columns and don't see updates to old rows; they only work with certain sources and formats; and they don't make writes idempotent, so a failure after writing and before `commit` reprocesses data.

#### How do you make a Glue job idempotent?

Write output for the processed partition with overwrite (dynamic partition overwrite) or use `MERGE` on an Iceberg table, rather than appending blindly; base the processed period on a parameter; and keep bookmarks as an optimization, not the only guarantee.

#### What is pushdown predicate in Glue?

A filter on partition columns passed when reading from the catalog (`push_down_predicate="order_date >= '2026-10-01'"`) so Glue lists and reads only matching partitions instead of the whole table.

#### What is `catalogPartitionPredicate`?

A server-side partition filter evaluated by the Data Catalog using partition indexes, which reduces the number of partitions Glue has to fetch from the catalog for tables with very many partitions. It can be combined with `push_down_predicate`.

#### How do you process only yesterday's data without bookmarks?

Pass the date as a job argument (from the scheduler), read with a pushdown predicate on the date partition, and overwrite that date's output partition. This is explicit, reproducible and makes backfills easy.

#### Do job bookmarks work with Iceberg tables as sources?

Not in the same way; for Iceberg sources you process incrementally with Iceberg's own features, such as reading changes between snapshots (incremental reads or changelog views) and storing the last processed snapshot ID.

#### What happens to bookmarks if a job fails?

Bookmarks are only updated on `job.commit()` after success, so a failed run leaves the bookmark where it was and the next run processes the same data again. That's why writes must be idempotent.

#### Can two different jobs share a bookmark?

No. Bookmarks are per job (and per `transformation_ctx`). Two jobs reading the same source keep independent state.

#### How do JDBC bookmarks work?

You specify `jobBookmarkKeys` (columns such as an increasing ID or `updated_at`) and a sort order; the job reads rows with values greater than the last stored maximum. Updates to rows with old key values are missed, so it fits append-only tables or monotonic timestamps.

### Workers, performance and cost

#### What worker types does Glue offer?

G.1X (1 DPU: 4 vCPU, 16 GB), G.2X (2 DPU), G.4X (4 DPU), G.8X (8 DPU), and larger types on recent versions, G.025X (0.25 DPU, for low-volume streaming), and memory-optimized R types for memory-heavy jobs. Bigger workers suit memory-intensive transforms; more workers suit parallel work.

#### How do you choose the number of workers?

Start from data volume and complexity, enable auto scaling with a sensible maximum, and look at job metrics: if executors are idle, reduce; if stages spill or tasks queue, increase or use bigger workers. Measure cost per run.

#### How do you troubleshoot a slow Glue job?

Enable job metrics, observability metrics and the Spark UI (event logs to S3), then look at stage durations, skewed tasks, shuffle sizes and spill, executor utilization, and the number of input files. Job run insights point to the failing line and common causes.

#### What is the small-files problem in Glue, and how do you handle it?

Reading many small files creates many tasks and S3 requests and slows jobs. Glue can group files at read time (`groupFiles: inPartition`, `groupSize`), and you should write fewer, larger files (repartition before writing, around 128 MB–1 GB per file) or compact Iceberg tables.

```python
dyf = glue.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://lake/raw/clicks/"], "recurse": True,
                        "groupFiles": "inPartition", "groupSize": "134217728"},
    format="json")
```

#### Why convert raw CSV or JSON to Parquet?

Parquet is columnar and compressed: Athena, Redshift Spectrum and Spark read only needed columns, skip row groups with statistics, and scan far less data, which reduces both time and cost.

#### How do you handle data skew in a Glue job?

Same as in Spark: rely on Adaptive Query Execution (enabled on recent Glue versions), broadcast small tables, isolate hot keys or salt them, and check the Spark UI for stragglers.

#### How do you reduce Glue costs?

Use the latest Glue version (faster start and runtime), enable auto scaling, use Flex for non-urgent jobs, right-size workers, set timeouts, process incrementally with partitions or bookmarks, read only needed partitions and columns, avoid crawlers where tables can be defined in code, and turn off development endpoints and idle sessions.

#### What is the Glue Spark UI?

A Spark history server view of a job run's event logs (enabled with `--enable-spark-ui` and an S3 log path), available in the Glue console, to analyze stages, tasks, storage and SQL plans.

#### What are Glue observability metrics?

CloudWatch metrics at job, stage and executor level (CPU, memory, disk, shuffle, skewness, worker utilization, throughput) that help detect bottlenecks and size jobs.

#### What does `--enable-auto-scaling` require?

Glue 3.0 or later, a maximum number of workers, and a workload that varies across stages. Glue then adjusts executors based on pending tasks.

#### What is the S3 shuffle option in Glue?

An option (`--write-shuffle-files-to-s3`) that writes Spark shuffle data to S3 instead of local disk, avoiding "no space left on device" failures on shuffle-heavy jobs, at the cost of some speed.

#### When should you use G.2X or larger workers instead of more G.1X workers?

When executors run out of memory (large joins, wide rows, big aggregations, ML transforms) or spill heavily. If tasks are small and numerous, more smaller workers give the same parallelism at the same price.

#### What are R-type (memory-optimized) workers?

Worker types with a higher memory-to-CPU ratio, for jobs that are memory-bound rather than CPU-bound, such as large broadcast joins or caching.

#### How do you estimate the cost of a Glue job?

Workers × DPU per worker × runtime in hours × price per DPU-hour. For example 10 G.1X workers for 15 minutes is 10 × 1 × 0.25 = 2.5 DPU-hours, about 1.10 USD at 0.44 USD per DPU-hour. With auto scaling, check actual DPU-seconds in job run details.

#### Why do Glue jobs take time to start, and how do you reduce it?

Glue provisions the environment at each run. Glue 2.0 and later start in seconds to about a minute; Flex can take longer. Reduce start time with newer versions, fewer extra modules installed at start-up (prebuild wheels), and avoid many tiny jobs that could be one.

#### How does Spark's Adaptive Query Execution help in Glue?

Enabled by default on Glue 4.0+, it coalesces small shuffle partitions, converts joins to broadcast when one side is small and splits skewed partitions, which improves performance without manual tuning.

#### How do you pass Spark configuration to a Glue job?

With the `--conf` job parameter (for example `--conf spark.sql.shuffle.partitions=400`), keeping in mind that some settings are managed by Glue and can't be changed.

#### What makes Parquet files efficient for later queries?

Columnar layout, compression (Snappy or ZSTD), row group statistics for skipping, reasonable file sizes (hundreds of MB), and sorting or partitioning by common filter columns.

#### How does partitioning strategy affect Glue and Athena?

Partition by columns used in most filters (usually date), with a moderate number of partitions each holding enough data; too fine (by hour and customer) creates millions of tiny partitions and slow planning, too coarse forces large scans.

### Streaming ETL

#### What are Glue streaming jobs?

Long-running Spark Structured Streaming jobs that read from Kinesis Data Streams, Amazon MSK or self-managed Kafka, transform records in micro-batches and write to S3, data lakes formats, databases or other streams.

#### How does a Glue streaming job handle schemas?

From a Data Catalog table describing the stream, from the Glue Schema Registry, or by inferring the schema from the data. Records that don't fit can be handled with choice types or routed to an error path.

#### What is the window size in Glue streaming?

The interval of each micro-batch (`windowSize`, for example 100 seconds) in `forEachBatch`. Larger windows reduce small files and overhead; smaller ones reduce latency.

#### Where does a streaming job keep its progress?

In a checkpoint location in S3, which stores offsets and state so the job resumes from where it stopped after a restart or update.

#### When would you choose Glue streaming over Kinesis Data Firehose or Managed Service for Apache Flink?

Firehose for simple delivery to S3, Redshift or OpenSearch with light transformation and no code. Managed Flink for low-latency, stateful stream processing with complex event-time logic. Glue streaming when the team already uses Spark, needs micro-batch ETL to a data lake and wants shared code with batch jobs.

#### How do you avoid small files from streaming jobs?

Use larger windows, write to Iceberg or Hudi tables and compact them (or rely on catalog compaction for Iceberg), or run a separate compaction job.

#### What sources can Glue streaming read?

Amazon Kinesis Data Streams, Amazon MSK, self-managed Apache Kafka, and (through connectors) other streaming systems. Outputs include S3, Iceberg/Hudi/Delta tables, JDBC databases and other streams.

#### How are Glue streaming jobs billed?

Per DPU-hour for as long as they run, since they run continuously; G.025X workers reduce cost for low-volume streams. Auto scaling helps with variable traffic.

#### How do you update a running streaming job's code?

Stop the job and start the new version with the same checkpoint location, as long as the changes are compatible with the stored state; incompatible changes need a new checkpoint and a plan for replaying or skipping data.

#### How do you handle late events in Glue streaming?

With Spark Structured Streaming's event-time windows and watermarks for aggregations, or by writing events to partitions by event date and letting downstream jobs reprocess recent partitions.

### Data quality and sensitive data

#### What is AWS Glue Data Quality?

A feature built on the open-source Deequ library to measure and monitor data quality with rules written in DQDL (Data Quality Definition Language), run in Glue jobs or against catalog tables, with recommendations, scores, anomaly detection and alerts.

#### What does a DQDL ruleset look like?

```
Rules = [
    RowCount > 1000,
    IsComplete "order_id",
    IsUnique "order_id",
    ColumnValues "status" in ["paid", "refunded", "cancelled"],
    ColumnValues "amount" >= 0,
    Freshness "updated_at" <= 24 hours
]
```

#### How do you act on data quality results in a job?

Use the Evaluate Data Quality transform, then route rows: keep passing rows, write failing rows to a quarantine location, and fail the job or send an EventBridge alert when the overall score drops below a threshold.

#### What is data quality anomaly detection?

Glue learns statistics over runs (row counts, distinct values, distributions) and flags unusual values even without explicit thresholds, which catches problems like a sudden drop in volume.

#### What is sensitive data detection in Glue?

A transform that scans data for PII such as names, emails, phone numbers, credit cards and national IDs (with country-specific detectors), and can redact, hash or report the findings, helping comply with GDPR or similar laws.

#### How do you get alerts for data quality failures?

Glue publishes data quality results to EventBridge and CloudWatch; rules can send notifications through SNS or trigger remediation workflows.

#### How do you get rule recommendations in Glue Data Quality?

Run a recommendation task on a catalog table: Glue profiles the data and proposes DQDL rules (completeness, uniqueness, value ranges, allowed values) that you review and edit before using.

#### What are composite rules in DQDL?

Rules combined with `and` and `or`, for example `(ColumnValues "status" = "paid") and (ColumnValues "amount" > 0)`, to express conditions involving several columns.

#### Where are data quality results stored?

In the Glue console history, in CloudWatch metrics, as EventBridge events and, optionally, written to S3 by the job, where they can be queried with Athena for trends.

#### How do you check referential integrity in Glue Data Quality?

With rules like `ReferentialIntegrity` that compare a column with another dataset's key column, or `DatasetMatch` to compare two datasets, passing the reference dataset as an additional source.

### Orchestration

#### What are Glue triggers?

Objects that start jobs and crawlers: scheduled (cron), conditional (when other jobs or crawlers reach a state such as `SUCCEEDED`), on-demand, or EventBridge-based events (for example batches of S3 events).

#### What is a Glue workflow?

A container for a graph of triggers, crawlers and jobs that represents an ETL pipeline, with a visual view of runs, shared run properties (key-value parameters) and the ability to resume from a failed step.

#### When would you use Step Functions or Airflow instead of Glue workflows?

When the pipeline involves many AWS services (Lambda, EMR, Athena, SageMaker), needs complex branching, retries and error handling, or spans other systems. Step Functions integrates natively with Glue (`startJobRun.sync`); Airflow (or MWAA) has Glue operators.

#### How do you trigger a Glue job when a file arrives in S3?

With an EventBridge rule on S3 "Object Created" events targeting a Glue workflow (with batching by number of events or time window), or with S3 notifications to Lambda that calls `StartJobRun`, or with an EventBridge rule that starts a Step Functions state machine.

#### How do you start a Glue job from Step Functions and wait?

```json
{
  "Type": "Task",
  "Resource": "arn:aws:states:::glue:startJobRun.sync",
  "Parameters": {
    "JobName": "curate-orders",
    "Arguments": { "--process_date.$": "$.date" }
  },
  "Retry": [{ "ErrorEquals": ["States.ALL"], "MaxAttempts": 2, "BackoffRate": 2 }],
  "Next": "RunAthenaChecks"
}
```

#### What are workflow run properties?

Key-value pairs shared by all jobs in a workflow run, read and updated with `get_workflow_run_properties` and `put_workflow_run_properties`, to pass values like a processing date between steps.

#### What is a conditional trigger's predicate?

The list of jobs or crawlers and states it watches, with logic `AND` (all conditions) or `ANY` (one condition), for example "start job B when job A succeeded and crawler C succeeded".

#### Can EventBridge start a Glue job directly?

EventBridge can target Glue workflows natively; for a single job, the common pattern is EventBridge to Step Functions or to a Lambda function that calls `StartJobRun`.

#### How do you resume a failed workflow?

In the Glue console or API (`ResumeWorkflowRun`), selecting the failed nodes to rerun after fixing the problem; completed nodes aren't rerun.

#### How do you pass the processing date from an orchestrator to a Glue job?

As a job argument in `StartJobRun` (`--process_date=2026-10-16`), computed by the orchestrator from the schedule's logical date, never from the job's own clock.

### Security and governance

#### What IAM permissions does a Glue job need?

A job runs with an IAM role that Glue assumes. It needs the `AWSGlueServiceRole` permissions (or equivalent), access to the S3 paths it reads and writes, the script location, the temporary directory, KMS keys, Secrets Manager secrets for connections and CloudWatch Logs.

#### How does Lake Formation work with Glue?

Lake Formation adds fine-grained permissions (database, table, column, row and cell level, and tag-based access control with LF-Tags) on top of the Data Catalog. Services such as Athena, Redshift Spectrum, EMR and Glue (5.0+) enforce these permissions when reading data.

#### What are LF-Tags?

Lake Formation tags (key-value pairs such as `domain=sales`, `classification=pii`) attached to databases, tables and columns; permissions are granted on tag expressions, which scales better than granting table by table.

#### How do Glue jobs access databases in a VPC?

Through a Glue connection with VPC, subnet and security group settings: Glue creates elastic network interfaces in the subnet. The subnet needs routes to the database and, for S3 access, an S3 gateway endpoint (or NAT for internet).

#### How do you encrypt data with Glue?

With security configurations that enable encryption for S3 output (SSE-S3 or SSE-KMS), CloudWatch Logs and job bookmarks; catalog encryption with KMS; and connection passwords stored in Secrets Manager or encrypted in the catalog.

#### How do you avoid hard-coding credentials in Glue scripts?

Store credentials in AWS Secrets Manager and reference the secret in the Glue connection, or read it in the script with boto3; use IAM roles for AWS resources.

#### How do you audit Glue activity?

CloudTrail logs Glue API calls (job and catalog changes), CloudWatch Logs holds job output, Lake Formation provides data access audit trails, and AWS Config can track resource configuration.

#### What is a Glue security configuration?

A named set of encryption settings (S3 encryption mode and KMS key, CloudWatch Logs encryption, job bookmark encryption) attached to jobs, crawlers and development endpoints.

#### How do you restrict a Glue job to specific S3 prefixes?

Give its IAM role a policy allowing only the needed bucket prefixes and KMS keys, and with Lake Formation, grant only the needed tables; avoid broad `s3:*` permissions.

#### How do you prevent Glue jobs from reaching the internet?

Run them with a VPC connection in private subnets without a NAT gateway, use VPC endpoints for S3, Glue, CloudWatch, KMS and Secrets Manager, and host Python dependencies in S3 or a private repository.

#### What is fine-grained access control for Glue Spark jobs?

With Glue 5.0 and Lake Formation, Spark jobs can enforce table, column, row and cell-level permissions defined in Lake Formation, so the job's role sees only the data it's allowed to.

### Operations, CI/CD and integration

#### How do you deploy Glue jobs as code?

Store scripts and job definitions in Git, deploy with CloudFormation, CDK, Terraform or SAM: upload scripts to S3 and create jobs, triggers, crawlers, connections and catalog tables. A CI pipeline runs tests, packages libraries as wheels and deploys to each environment.

#### How do you test Glue job logic?

Put transformation logic in functions that take and return DataFrames, test them with pytest on a local SparkSession or the Glue Docker image, test the job end to end on sample data in a dev account, and add data quality rules for runtime checks.

#### How do you monitor Glue jobs in production?

CloudWatch metrics and alarms (job failures, duration, DPU usage), EventBridge events for job state changes routed to SNS or Slack, job run insights for errors, and dashboards of job durations and costs over time.

#### How do you handle job failures?

Retries for transient errors (only with idempotent jobs), alerts on `FAILED` and `TIMEOUT` states, a rerun procedure using parameters for the failed period, and dead-letter or quarantine paths for bad data.

#### What is zero-ETL in the Glue context?

Managed integrations that replicate data from sources (SaaS applications such as Salesforce, SAP or ServiceNow, and AWS databases such as DynamoDB) into targets like SageMaker Lakehouse tables or Redshift without building ETL pipelines, keeping them in sync.

#### What is Amazon Q data integration in Glue?

A generative AI assistant that creates Glue ETL jobs and transforms from natural-language descriptions and helps troubleshoot jobs; there is also AI-assisted upgrade of Spark scripts to newer Glue versions.

#### How do Glue and Athena work together?

Glue catalogs and transforms data; Athena queries the catalog tables with SQL. Glue jobs often convert raw data to partitioned Parquet or Iceberg so Athena queries are fast and cheap.

#### How do Glue and AWS DMS work together?

DMS replicates databases (full load and CDC) into S3 as files with operation flags; Glue jobs then apply the changes to curated tables, typically with `MERGE` on Iceberg or Hudi tables.

#### How do you upgrade a Glue job to a newer version?

Change the Glue version in a dev copy, run tests and compare outputs and durations, review migration notes (Spark, Python and library changes), check connectors and JARs, then promote through CI.

#### How do you structure a Glue project repository?

Separate job entry scripts, a shared Python package with transformation logic (built as a wheel), tests, infrastructure as code (CDK, Terraform or CloudFormation), data quality rulesets and configuration per environment.

#### How do you version Glue scripts?

Keep them in Git and deploy versioned copies to S3 (for example with the commit SHA in the path), so each job definition points to a known script version and rollback means pointing back.

#### How do you alert on long-running Glue jobs?

Set the job timeout, add a CloudWatch alarm on elapsed time or on the `glue.driver.aggregate.elapsedTime` metric, or have the orchestrator alert when a step exceeds its expected duration.

#### How do you share Glue tables with Amazon Redshift?

Create an external schema in Redshift pointing to a Glue database (`CREATE EXTERNAL SCHEMA ... FROM DATA CATALOG`), then query the tables with Redshift Spectrum, or use Redshift's auto-mounted Data Catalog access.

#### How does EMR use the Glue Data Catalog?

EMR clusters and EMR Serverless can be configured to use the Glue Data Catalog as their Hive metastore, so Spark, Hive, Presto and Trino on EMR share the same table definitions as Athena and Glue.

#### What is AWS Glue for SAP or other SaaS connectors used for?

Extracting data from enterprise applications (SAP OData, Salesforce, ServiceNow, Zendesk and others) through managed connectors into Glue jobs or zero-ETL integrations, without writing API code.

### Scenarios

#### Design a pipeline that turns daily CSV drops in S3 into a queryable, partitioned dataset.

Land CSVs under a dated raw prefix, run a Glue Spark job (triggered by EventBridge or a schedule) that reads the day's files with a defined schema, cleans and casts types, writes Parquet or Iceberg partitioned by date to a curated prefix, updates the catalog, and runs data quality rules. Athena or Redshift Spectrum query the curated table; Lake Formation controls access.

#### A crawler keeps creating dozens of tables instead of one. What's wrong?

Files under the prefix have inconsistent schemas or folder structures (extra columns, different formats, stray files). Fix the source layout, add exclude patterns, use "create a single schema for each S3 path", or define the table explicitly instead of crawling.

#### A Glue job that used to take 10 minutes now takes 2 hours. How do you investigate?

Compare input volume and number of files, check whether the pushdown predicate or bookmarks stopped working (reprocessing everything), look at the Spark UI for skew or spill, check worker count and auto scaling, and check for a changed join or a lost broadcast.

#### Your Glue job fails with "No space left on device". What do you do?

The job is spilling or shuffling more than local disk can hold. Use bigger workers (more disk per executor), enable the S3 shuffle option, reduce data before shuffles (filter and select earlier), fix skew, and increase partitions so each task handles less data.

#### Athena queries on the Glue table fail with `HIVE_PARTITION_SCHEMA_MISMATCH`. Why?

Some partitions were registered with a different schema than the table (a crawler updated one partition after a source change). Make partitions inherit the table schema (crawler setting "update all new and existing partitions with metadata from the table"), fix or rewrite the odd partitions, and stabilize the source schema.

#### How would you load CDC data from an RDS PostgreSQL database into a lakehouse with Glue?

Use DMS for full load plus CDC into S3 (Parquet with an operation column), or a zero-ETL integration where available. A Glue job reads new change files (bookmarks or date partitions), deduplicates per key keeping the latest change, and runs `MERGE INTO` on an Iceberg table registered in the Data Catalog. Compaction and snapshot expiry keep it healthy.

#### How do you run the same Glue job for dev, staging and prod?

One script with parameters for paths, databases and connections, deployed by infrastructure as code per environment (separate accounts ideally), with environment-specific job arguments and IAM roles, promoted through CI after tests.

#### How would you explain AWS Glue to a non-technical stakeholder?

It's AWS's service for keeping an inventory of the company's data and for cleaning and moving that data into shape for reports and analysis, without having to run servers.

#### You need to deduplicate customer records with no common key across two systems. What Glue tool can help?

The FindMatches ML transform: label examples of matching and non-matching pairs, train the transform, and run it in a job to assign match IDs, then merge records per match ID with business rules.

#### A Glue job writes thousands of tiny Parquet files per day. How do you fix it?

Repartition by the partition column before writing so each partition gets a few files, increase the batch size (process a day rather than every few minutes), and if using Iceberg enable catalog compaction or run `rewrite_data_files`.

#### How would you migrate on-premises SSIS or Informatica jobs to Glue?

Inventory jobs and their dependencies, rebuild sources as Glue connections, rewrite transformations as PySpark (or visual jobs), store reference data in S3 or the catalog, orchestrate with Step Functions or Airflow, and validate outputs side by side before switching.

#### Analysts complain Athena queries on Glue tables are expensive. What changes do you make in the Glue jobs?

Write Parquet or Iceberg instead of CSV/JSON, compress, partition by common filters, produce fewer larger files, compute column statistics, and maybe create aggregated tables for frequent dashboards.

#### A source system adds new columns without warning. How do you keep the Glue pipeline running?

Read with schema evolution in mind: use DynamicFrames or permissive schemas in raw, select columns explicitly in curated outputs, alert on new columns (crawler log-only mode or a schema check), and use Iceberg schema evolution to add columns intentionally.

#### How do you implement a "late data" correction in a daily Glue pipeline?

Process a rolling window (for example the last three days) each run with partition overwrite or `MERGE`, so late records update the right partitions, and keep the window parameterized for larger corrections.

#### How do you choose between Glue, EMR Serverless and Databricks for a new data platform on AWS?

Glue for serverless ETL tightly integrated with the AWS catalog and Lake Formation; EMR Serverless for open-source Spark/Hive with more control and often lower cost at scale; Databricks for a unified lakehouse platform with collaborative notebooks, Delta, Unity Catalog and ML. Team skills, governance requirements and cost models decide.
