## AWS Glue Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![AWS Glue study guide: about 200 questions](../../images/aws_glue_study_guide_title_img.png)

About 200 interview-style questions on AWS Glue: the Data Catalog, crawlers, Spark ETL jobs, DynamicFrames, job bookmarks, workers and cost, streaming, data quality, orchestration, security with Lake Formation, and performance tuning. The answers reflect the service as of 2026.

The guide follows a learning path in four stages. Each section is split into short units: learning goals, a concept explanation and a worked example, then questions (recall first, then application), a practical challenge and key takeaways. To **learn**, read each unit top to bottom. To **review**, switch to review mode or use "Skip to questions", mark answers you want to see again, and try a mixed review across sections.

<!-- QA -->
<!-- stage: Foundations -->

### Fundamentals

<!-- unit: What Glue is -->

<!-- goals -->

- Explain what AWS Glue does and which components it has.
- Place Glue in an AWS data lake, for ETL and ELT.

<!-- concept -->

A data lake needs two things besides storage: a shared description of what the data is, and jobs that turn raw files into usable tables. Glue provides both. Its catalog is the inventory that Athena, Redshift and EMR read; its crawlers fill that inventory; its serverless Spark jobs do the transformation.

"Serverless" here means you pick a size and pay per second of use, with no cluster to keep running. That fits batch work that runs a few times a day and sits idle in between.

<!-- example -->

```text
sources ─► S3 raw ─► Glue job (Spark) ─► S3 curated (Parquet/Iceberg)
                │                               │
                └──────► Glue Data Catalog ◄────┘ ◄── Athena, Redshift, EMR
```

#### What is AWS Glue?

A serverless data integration service on AWS for discovering, preparing, moving and integrating data. Its main parts are the Glue Data Catalog (a central metadata repository), crawlers (schema discovery), ETL jobs (Apache Spark or Python), Glue Studio (visual authoring), Data Quality, DataBrew (visual data preparation) and workflows for orchestration.

#### What does "serverless" mean for Glue?

You don't provision or manage clusters: you choose a worker type and number (or let auto scaling decide), Glue starts the environment for the job run, and you pay only for the time the job runs, per second.

#### What are the main use cases for Glue?

Building data lakes on S3 (cataloging and transforming raw data into Parquet or Iceberg), ETL into Redshift or other databases, preparing data for Athena and machine learning, CDC and streaming ingestion, and providing a shared metadata catalog for Athena, EMR, Redshift Spectrum and Lake Formation.

#### What are the main components of AWS Glue, in one sentence each?

The Data Catalog stores metadata; crawlers discover schemas; ETL jobs transform data with Spark or Python; triggers and workflows orchestrate; Glue Studio provides visual authoring; Data Quality validates data; DataBrew prepares data visually; the Schema Registry governs streaming schemas.

#### How does Glue fit into the AWS data lake architecture?

Data lands in S3 (from DMS, Kinesis, AppFlow, uploads), crawlers or jobs register it in the Data Catalog, Glue jobs clean and convert it into curated zones (Parquet or Iceberg), Lake Formation governs access, and Athena, Redshift, EMR, QuickSight and SageMaker consume it.

#### What is ETL versus ELT in the context of Glue?

With ETL, Glue jobs transform data before loading it into the target (for example cleaning and converting to Parquet before Redshift). With ELT, raw data is loaded first and transformed inside the target (Redshift SQL, dbt on Athena). Glue is often used for the "E" and "L" of ELT, or as the "T" in a lakehouse.

#### How would you explain AWS Glue to a non-technical stakeholder?

It's AWS's service for keeping an inventory of the company's data and for cleaning and moving that data into shape for reports and analysis, without having to run servers.

<!-- challenge -->

A team writes Python scripts on an EC2 instance that convert CSVs to Parquet each night. What would Glue add, and what would they still need to design?

<!-- solution -->

Glue would remove the server, scale the conversion with Spark, register tables in the catalog and track runs. The team still decides partitioning, file sizes, incremental logic, schedules and data quality rules.

<!-- takeaways -->

- Glue combines a catalog, crawlers and serverless Spark jobs.
- The catalog is shared by Athena, Redshift and EMR.
- Serverless suits batch work with idle time between runs.

<!-- unit: Glue among AWS services -->

<!-- goals -->

- Compare Glue with EMR, Lambda, DataBrew and other platforms.
- Choose a processing service for a given workload.

<!-- concept -->

AWS has several ways to run transformations, and they mostly differ in how much you manage and how big the job is. Lambda handles small, event-driven files. Glue handles batch Spark ETL without clusters. EMR handles workloads that need full control or many open-source engines. DataBrew gives analysts a visual tool.

The Glue catalog sits underneath most of them, which is why the choice of engine can change without moving metadata.

<!-- example -->

| Workload | Good fit |
|---|---|
| Transform each 2 MB file on arrival | Lambda |
| Nightly 500 GB CSV to Parquet | Glue |
| Long-running Spark with custom configs and Hudi tuning | EMR |
| Analyst cleans a spreadsheet-like dataset visually | DataBrew |

#### How does Glue compare with Amazon EMR?

Glue is serverless and focused on ETL with Spark, with built-in catalog, bookmarks and quality features; you trade control for simplicity. EMR (on EC2, EKS or Serverless) gives full control of Spark, Hadoop, Hive, Trino and other frameworks, versions and tuning, and is often cheaper for large, steady workloads.

#### How does Glue compare with AWS Lambda for ETL?

Lambda suits small, event-driven transformations (a file of a few MB) with a 15-minute limit and limited memory. Glue suits larger, distributed processing with Spark, longer runtimes and big volumes.

#### What is AWS Glue DataBrew?

A visual data preparation tool with 250+ built-in transformations, used by analysts to clean and normalize data without code. Transformations are saved as recipes and run as jobs on S3 data, with data profiling.

#### What is the relationship between Glue and SageMaker Lakehouse/Unified Studio?

The Glue Data Catalog is the metadata foundation of SageMaker Lakehouse, and Glue's data integration features (ETL jobs, visual ETL, connections, zero-ETL) are available inside SageMaker Unified Studio, AWS's combined environment for data, analytics and AI.

#### How do you choose between Glue, EMR Serverless and Databricks for a new data platform on AWS?

Glue for serverless ETL tightly integrated with the AWS catalog and Lake Formation; EMR Serverless for open-source Spark/Hive with more control and often lower cost at scale; Databricks for a unified lakehouse platform with collaborative notebooks, Delta, Unity Catalog and ML. Team skills, governance requirements and cost models decide.

<!-- challenge -->

A Lambda function that converts uploaded files started timing out because some files are now 3 GB. What do you recommend?

<!-- solution -->

Move large-file processing to a Glue job (triggered by EventBridge or a schedule), which has no 15-minute limit and scales with Spark. Keep Lambda only for small files or for starting the Glue job.

<!-- takeaways -->

- Lambda for small events; Glue for batch Spark ETL; EMR for control.
- DataBrew serves analysts visually.
- The Glue catalog is shared across engines.

<!-- unit: Billing, versions and limits -->

<!-- goals -->

- Explain DPUs and estimate how Glue bills jobs.
- Choose Glue versions and know the main quotas.

<!-- concept -->

Glue's price is simple: capacity times time. A DPU is a fixed amount of CPU and memory, and you pay for DPUs per second while a job runs. So cost depends on choosing the right size and finishing quickly, not on data volume directly.

Each Glue version bundles a Spark and Python version, which affects speed, start-up time and available features. Regional catalogs, service quotas and the tools for development complete the operating picture.

<!-- example -->

```text
10 G.1X workers × 1 DPU × 0.25 h × 0.44 USD/DPU-hour ≈ 1.10 USD per run
same job on Glue 5.0, 40% faster          ≈ 0.66 USD per run
```

#### What is a DPU?

A Data Processing Unit: 4 vCPU and 16 GB of memory. Glue bills ETL jobs, crawlers and interactive sessions in DPU-hours, per second.

#### How is a Glue job billed?

Per DPU-hour, per second, with a 1-minute minimum for Spark jobs on Glue 2.0 and later. The cost is number of DPUs × duration × price per DPU-hour (about 0.44 USD in many regions, Flex cheaper). Python shell jobs bill 1/16 or 1 DPU.

#### What are the Glue versions, and why do they matter?

Each Glue version bundles a Spark, Python and Java version and connectors: for example Glue 4.0 runs Spark 3.3 and Python 3.10, and Glue 5.0 runs Spark 3.5 and Python 3.11. Newer versions start faster, run faster and support newer table formats. Older versions reach end of support, so upgrades are part of maintenance.

#### What are Glue service quotas you should know?

Limits on concurrent job runs per account, maximum DPUs per job, number of jobs, triggers, crawlers, databases, tables and partitions per table. Most are adjustable through Service Quotas; large data lakes hit partition and concurrency limits first.

#### In which regions is Glue available, and is the catalog regional?

Glue is available in most AWS regions, and the Data Catalog is regional: each region has its own catalog per account. Cross-region access needs replication of metadata or resource links in Lake Formation.

#### What is Glue Studio?

The console experience for creating, running and monitoring Glue jobs: a visual editor where you build ETL as a graph of sources, transforms and targets (which generates PySpark code), a script editor, a notebook editor, and job monitoring dashboards.

#### What is a development endpoint, and what replaced it?

A legacy, always-on environment for developing Glue scripts from notebooks, billed while running. Interactive sessions and Glue Studio notebooks replaced it with on-demand, per-second billing and idle timeouts.

<!-- challenge -->

A job on Glue 2.0 runs 40 minutes on 20 G.1X workers every hour. Name two changes likely to cut its cost.

<!-- solution -->

Upgrade to the latest Glue version (newer Spark, faster runtime and start-up), and enable auto scaling so workers drop when stages need fewer. Then check whether hourly runs could process incrementally.

<!-- takeaways -->

- You pay DPUs × time, billed per second.
- Newer Glue versions are usually faster and cheaper.
- The catalog is regional; quotas limit concurrency.

### Data Catalog

<!-- unit: Databases and tables -->

<!-- goals -->

- Describe what the Data Catalog stores and how tables get into it.
- Use table properties and know what "external" means.

<!-- concept -->

The Data Catalog is a metastore: it stores descriptions of data, never the data. Databases group tables, and tables record a location, a schema, a format and properties that tell engines how to read files. Because every analytics service reads the same entries, one wrong property breaks queries everywhere.

Tables can be created by crawlers, by DDL, by jobs or by infrastructure as code. In pipelines you own, explicit definitions are more predictable than discovery.

<!-- example -->

```python
glue.create_table(DatabaseName="curated", TableInput={
    "Name": "orders",
    "StorageDescriptor": {
        "Columns": [{"Name": "order_id", "Type": "bigint"}, {"Name": "amount", "Type": "decimal(12,2)"}],
        "Location": "s3://lake/curated/orders/",
        "InputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
        "SerdeInfo": {"SerializationLibrary": "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"}},
    "PartitionKeys": [{"Name": "dt", "Type": "string"}],
    "Parameters": {"classification": "parquet"}})
```

#### What is the Glue Data Catalog?

A managed, Hive-metastore-compatible metadata repository per account and region. It stores databases, tables (schema, location, format, partitions, statistics), connections and user-defined functions. Athena, EMR, Redshift Spectrum, Glue jobs and many other services use it to know where data is and how to read it.

#### What is a Glue database?

A logical container for tables in the Data Catalog. It doesn't store data itself; it groups table definitions, and permissions can be granted at the database level with Lake Formation.

#### What is a Glue table?

Metadata that describes data: column names and types, the S3 location (or a JDBC source), the format (SerDe and input/output formats), partition keys and table properties. The data itself stays in S3 or in the source database.

#### How do tables get into the Data Catalog?

By running crawlers, by creating tables manually (console, `CREATE EXTERNAL TABLE` in Athena, CloudFormation, Terraform, the API), from Glue jobs that create or update tables when writing (`enableUpdateCatalog`), or from services such as Lake Formation blueprints and zero-ETL integrations.

#### What is the difference between an external table and a governed table?

In the Data Catalog all S3-based tables are external (the catalog only holds metadata, dropping it doesn't delete data). Governed tables were a Lake Formation table type with ACID transactions, now retired in favor of Apache Iceberg tables.

#### What are table properties like `classification` and `compressionType` used for?

They tell engines and Glue how to interpret the data: `classification` (csv, json, parquet) is set by crawlers and used by Glue jobs, while SerDe parameters and compression settings tell Athena or Hive how to parse the files.

#### What is a user-defined function in the Data Catalog?

Metadata for a Hive UDF (class name and JAR location) stored in the catalog so engines like EMR Hive can use it, mostly relevant for Hive-compatible workloads.

<!-- challenge -->

Someone drops a catalog table to "clean up" and Athena queries fail. Is the data lost? How do you restore the table?

<!-- solution -->

No, S3 tables are external, so the files remain. Recreate the table from its definition in infrastructure as code (or from a catalog version or Athena DDL), then re-register partitions or rerun the crawler.

<!-- takeaways -->

- The catalog stores metadata; data stays in S3.
- All engines read the same table entries.
- Define pipeline tables explicitly, as code.

<!-- unit: Partitions and statistics -->

<!-- goals -->

- Register partitions and keep them consistent with the table.
- Speed up planning with partition indexes and column statistics.

<!-- concept -->

Partitions are catalog entries too, one per folder, each with its own location and schema. That has two consequences. Engines can skip partitions only if they're registered, and partitions can drift from the table when something updates one but not the other.

As partition counts grow, even listing them becomes slow. Partition indexes let the catalog filter partitions on the server, and column statistics help optimizers plan joins.

<!-- example -->

```python
glue.batch_create_partition(DatabaseName="curated", TableName="orders",
    PartitionInputList=[{"Values": ["2026-10-17"],
        "StorageDescriptor": {**table_sd, "Location": "s3://lake/curated/orders/dt=2026-10-17/"}}])
```

#### What is a partition in the Data Catalog?

A subset of a table's data defined by partition key values (for example `year=2026/month=10/day=15`), each with its own S3 location. Query engines read only the partitions matching filters, which cuts cost and time.

#### How are new partitions registered?

By a crawler, by `MSCK REPAIR TABLE` or `ALTER TABLE ADD PARTITION` in Athena, by the `BatchCreatePartition` API, by Glue jobs writing with catalog updates, or avoided entirely with Athena partition projection.

#### What are partition indexes?

Indexes on partition keys of catalog tables with many partitions, so `GetPartitions` calls with filters return quickly instead of scanning all partitions. They speed up query planning in Athena and Glue on tables with tens of thousands of partitions.

#### What are column statistics in the Data Catalog?

Statistics (number of distinct values, nulls, min/max, average length) computed by Glue for table columns and stored in the catalog, which Athena and Redshift Spectrum use for cost-based optimization such as join reordering.

#### Athena queries on the Glue table fail with `HIVE_PARTITION_SCHEMA_MISMATCH`. Why?

Some partitions were registered with a different schema than the table (a crawler updated one partition after a source change). Make partitions inherit the table schema (crawler setting "update all new and existing partitions with metadata from the table"), fix or rewrite the odd partitions, and stabilize the source schema.

<!-- challenge -->

A table with 300,000 partitions takes 40 seconds to plan in Athena, even for one day. What do you add?

<!-- solution -->

A partition index on the date key, so `GetPartitions` filters on the server, or switch the table to partition projection. Also consider whether partition granularity is finer than queries need.

<!-- takeaways -->

- Partitions are catalog entries with their own schema.
- Mismatched partition schemas break queries.
- Partition indexes and statistics speed up planning.

<!-- unit: Formats, connections and schemas -->

<!-- goals -->

- Know which table formats and connections the catalog supports.
- Version schemas for tables and streams.

<!-- concept -->

The catalog describes more than folders of files. It registers open table formats like Iceberg, whose own metadata tracks files, and can maintain them by compacting files automatically. It stores connections to databases so jobs and crawlers don't embed URLs and credentials.

Schemas change, so the catalog keeps table versions, and the Schema Registry versions schemas for streaming data with compatibility rules that stop breaking changes.

<!-- example -->

```python
# connection referencing a secret instead of a password
glue.create_connection(ConnectionInput={
    "Name": "orders_pg", "ConnectionType": "JDBC",
    "ConnectionProperties": {"JDBC_CONNECTION_URL": "jdbc:postgresql://db:5432/shop",
                             "SECRET_ID": "prod/orders_pg"}})
```

#### What table formats does the Data Catalog support?

Hive-style tables in Parquet, ORC, Avro, JSON, CSV and other formats, and open table formats Apache Iceberg, Apache Hudi and Delta Lake. Iceberg is the most deeply integrated across AWS services.

#### What are catalog optimizations for Iceberg tables?

Managed table maintenance for Iceberg tables in the Data Catalog: automatic compaction of small files, snapshot retention (expiring old snapshots) and orphan file deletion, configured per table and run by Glue without your own jobs.

#### What is a Glue connection?

A catalog object that stores connection properties for a data store: JDBC URL, credentials (preferably a Secrets Manager secret), VPC, subnet and security groups, or properties for Kafka, MongoDB, Snowflake, BigQuery and other native connectors. Jobs and crawlers reference it.

#### What is the Glue Schema Registry?

A service to store, version and validate schemas (Avro, JSON Schema, Protobuf) for streaming data, with compatibility rules (backward, forward, full). Producers and consumers using Kafka, MSK, Kinesis or Lambda serialize and validate records against registered schemas.

#### How do you version table schemas in the Data Catalog?

The catalog keeps table versions automatically when a table is updated (up to a limit), so you can see and compare earlier schemas with `GetTableVersions`. Iceberg tables also keep schema history in their own metadata.

<!-- challenge -->

A Kafka producer changed a field from `int` to `string` and broke three consumers. Which Glue feature would have prevented it?

<!-- solution -->

The Glue Schema Registry with a compatibility mode such as `BACKWARD`: the producer's serializer would have rejected the incompatible schema version before any message was sent.

<!-- takeaways -->

- The catalog registers Hive-style and open table formats.
- Connections keep URLs and secrets out of code.
- Table versions and the Schema Registry track schema changes.

<!-- unit: Sharing and managing the catalog -->

<!-- goals -->

- Share catalogs across accounts and query them programmatically.
- Keep a catalog clean and understand its cost.

<!-- concept -->

In multi-account setups, one catalog often serves many teams. Sharing works through Lake Formation and resource links, which make remote tables appear local without copying metadata, and every API call can name the catalog it targets.

A shared catalog needs housekeeping: naming conventions per layer, tables defined as code, and removal of tables that crawlers or experiments left behind. Billing is rarely the issue; confusion is.

<!-- example -->

```python
paginator = boto3.client("glue").get_paginator("get_tables")
for page in paginator.paginate(CatalogId="111122223333", DatabaseName="curated"):
    for t in page["TableList"]:
        print(t["Name"], t["StorageDescriptor"]["Location"])
```

#### Can several AWS accounts share one Data Catalog?

Yes. Access can be granted across accounts with resource policies on the catalog or, more commonly, with Lake Formation cross-account grants (often through AWS RAM), so a central governance account shares databases and tables with consumer accounts.

#### What is the catalog ID?

The AWS account ID that owns a Data Catalog. APIs and queries can reference another account's catalog by its ID when cross-account access is granted.

#### What is a resource link?

A Lake Formation object that points to a shared database or table from another account or region, so users can query it as if it were local in their own catalog.

#### How do you query the Data Catalog programmatically?

With the Glue API (`GetDatabases`, `GetTables`, `GetPartitions`, `SearchTables`) through boto3 or the CLI, or with SQL through Athena's `information_schema` views.

#### How is the Data Catalog billed?

The first million objects stored and the first million requests per month are free; beyond that you pay per 100,000 objects and per million requests. Statistics computation and Iceberg optimizations are billed separately in DPU-hours.

#### How do you keep a Data Catalog clean?

Define naming conventions per layer (`raw_`, `curated_`), manage tables as code, remove tables created by accidental crawls, document tables and columns with descriptions, apply LF-Tags for classification, and monitor for unused tables.

<!-- challenge -->

The `raw` database has 2,000 tables, half created by crawlers on test folders. Analysts can't find anything. What do you do?

<!-- solution -->

Inventory tables with the API (location, last update), delete those pointing to test or missing locations, restrict crawler scopes, adopt naming conventions per layer, and manage curated tables as code with descriptions.

<!-- takeaways -->

- Share catalogs through Lake Formation and resource links.
- Catalog IDs let APIs target other accounts.
- Clean catalogs need conventions and ownership.

### Crawlers

<!-- unit: How crawlers work -->

<!-- goals -->

- Explain how crawlers infer schemas and group files into tables.
- Know what crawlers can read, from CSV to JDBC and Iceberg.

<!-- concept -->

A crawler looks at a sample of data and guesses. Classifiers recognize the format and schema, folder structure suggests tables and partitions, and the result is written to the catalog. Good guesses need consistent data: same format, same columns, predictable folders.

Text formats are where guessing fails most often, since types and headers must be inferred from values. Self-describing sources (Parquet, Iceberg, database schemas) give much more reliable results.

<!-- example -->

```text
s3://landing/orders/dt=2026-10-16/part-0.csv   ┐
s3://landing/orders/dt=2026-10-17/part-0.csv   ┘─► table "orders", partition key "dt"
s3://landing/orders/backup_old/orders.json      ─► a second table: different format
```

#### What is a crawler?

A Glue component that connects to a data store (S3, JDBC databases, DynamoDB, MongoDB, Delta, Iceberg, Hudi), samples the data, infers schemas and partitions with classifiers, and creates or updates tables in the Data Catalog. It can run on demand or on a schedule.

#### What is a classifier?

The logic that recognizes a data format and its schema. Glue has built-in classifiers (CSV, JSON, Parquet, Avro, ORC, XML, logs and more), and you can add custom classifiers with grok patterns, XML tags, JSON paths or CSV settings.

#### How does a crawler decide how many tables to create?

It groups files with compatible schemas under a common prefix into one table, using folder structure to detect partitions. If schemas differ too much, it creates several tables. The "create a single schema for each S3 path" option forces one table per include path.

#### How do crawlers infer types from CSV files?

By sampling the first rows and choosing types that fit; if a column has mixed values (like numbers with a few blanks or text), the crawler may choose `string`, or pick a type that later rows break. Define CSV tables explicitly for predictable types.

#### How do crawlers handle headers in CSV?

The built-in CSV classifier guesses whether the first row is a header by checking whether it looks different from the data rows. When guessing fails, a custom CSV classifier with an explicit header setting fixes it.

#### Can crawlers create Iceberg or Delta tables?

Yes. Crawlers can register existing Delta Lake, Iceberg and Hudi tables from S3 by reading their metadata, creating catalog tables that point to the table format (natively or via manifests, depending on configuration).

#### Can a crawler crawl a JDBC database?

Yes. Through a Glue connection, it reads table definitions from databases such as MySQL, PostgreSQL, Oracle and SQL Server using an include path like `mydb/%` and creates catalog tables that jobs can read.

<!-- challenge -->

A crawler typed a `zip_code` column as `bigint`, dropping leading zeros. How do you fix it for good?

<!-- solution -->

Set the schema yourself: define the table as code with `zip_code` as `string` and set the crawler to not update schemas (or stop using it for this table). A custom classifier with explicit types is another option.

<!-- takeaways -->

- Crawlers infer schemas by sampling; consistent data helps.
- Text formats produce the most wrong guesses.
- Self-describing formats crawl reliably.

<!-- unit: Configuring crawlers -->

<!-- goals -->

- Configure schema change, recrawl and scope settings.
- Make crawls incremental and event-driven.

<!-- concept -->

A crawler that rescans everything and rewrites schemas on each run is slow, expensive and risky. Its settings control three things: what it looks at (paths, exclusions, table level, sample size), how often it rereads old folders (recrawl policy, S3 events), and what it may change (schema change policy).

The safest configuration reads only new data and logs schema changes instead of applying them.

<!-- example -->

```json
{
  "Targets": {"S3Targets": [{"Path": "s3://landing/orders/", "Exclusions": ["**/_temporary/**", "**.crc"]}]},
  "RecrawlPolicy": {"RecrawlBehavior": "CRAWL_NEW_FOLDERS_ONLY"},
  "SchemaChangePolicy": {"UpdateBehavior": "LOG", "DeleteBehavior": "LOG"},
  "Configuration": "{\"Version\":1.0,\"Grouping\":{\"TableLevelConfiguration\":3}}"
}
```

#### What is the schema change policy of a crawler?

Settings for what to do when the schema changes or objects are deleted: update the table or only log changes, and delete, deprecate or ignore removed tables and partitions. Production teams often log changes rather than update automatically, to avoid surprises.

#### What are incremental crawls?

Crawls that only process folders added since the last run (and with S3 event mode, only changed objects from an SQS queue), which is much faster and cheaper for large, growing data lakes.

#### What is S3 event mode for crawlers?

A mode where the crawler reads S3 event notifications from an SQS queue to know exactly which objects changed, instead of listing the whole prefix.

#### What is the "recrawl policy"?

The setting that decides whether to crawl all folders again on each run or only new folders since the last crawl (incremental), or use S3 events.

#### What are exclude patterns?

Glob patterns that tell a crawler to skip files or folders, such as `**/_temporary/**`, `**.crc` or `**/_SUCCESS`, which avoids junk tables and saves time.

#### How do you limit the scope of a crawler?

With precise include paths, exclude patterns, a sample size per folder (for S3), table level settings (at which folder depth tables are created) and separate crawlers per source.

#### What does "table level" mean in crawler configuration?

The folder depth at which the crawler creates tables. Setting it avoids crawlers making tables at the wrong level, for example treating each partition folder as a separate table.

<!-- challenge -->

A crawler on a 5-year-old bucket runs for an hour every night to find one new folder. What do you change?

<!-- solution -->

Set the recrawl policy to new folders only, or switch to S3 event mode with an SQS queue so it reads only changed objects. Better still, register the daily partition from the load job and drop the crawler.

<!-- takeaways -->

- Scope settings control what a crawler reads.
- Incremental and event modes avoid full rescans.
- Log schema changes instead of applying them blindly.

<!-- unit: When to crawl -->

<!-- goals -->

- Recognize common crawler problems and their causes.
- Decide when to use crawlers and when to define tables yourself.

<!-- concept -->

Crawlers are a discovery tool. They shine for data you don't control and want to explore quickly. In pipelines you own, you already know the schema and the partitions, so letting a crawler guess them adds cost, delay and the risk of a wrong guess changing production tables.

Most crawler problems trace back to inconsistent inputs: mixed formats or schemas under one prefix, stray files, or unexpected folder depth.

<!-- example -->

| Situation | Use |
|---|---|
| Explore a vendor's S3 bucket | Crawler |
| Your Glue job writes daily partitions | Job updates the catalog |
| Iceberg table written by Spark | Catalog via the writer, no crawler |

#### What are common problems with crawlers?

Too many tables created because of inconsistent schemas or folder structures, wrong types inferred from CSV samples, `HIVE_PARTITION_SCHEMA_MISMATCH` errors when partitions have different schemas, cost and time on huge prefixes, and silent schema changes breaking downstream queries.

#### Should you always use crawlers?

No. Crawlers are convenient for discovery and for sources you don't control. For pipelines you own, defining tables explicitly (infrastructure as code) and registering partitions from jobs, or using partition projection, gives predictable schemas and no crawler cost.

#### How are crawlers billed?

Per DPU-hour for the time they run, per second with a minimum duration per run. Crawling millions of small files can be expensive; use include/exclude patterns, sampling and incremental crawls.

#### A crawler keeps creating dozens of tables instead of one. What's wrong?

Files under the prefix have inconsistent schemas or folder structures (extra columns, different formats, stray files). Fix the source layout, add exclude patterns, use "create a single schema for each S3 path", or define the table explicitly instead of crawling.

<!-- challenge -->

Your Glue job writes Parquet to S3 and a crawler runs after it to update the table. Sometimes queries break after the crawler changes a type. What do you propose?

<!-- solution -->

Remove the crawler from the pipeline: have the job write with catalog updates enabled (or call `BatchCreatePartition`) against a table defined as code. Schema changes then happen deliberately, through code review.

<!-- takeaways -->

- Crawlers are for discovery, not owned pipelines.
- Inconsistent inputs create too many tables.
- Let jobs register their own output.

<!-- stage: Building jobs -->

### Glue ETL jobs

<!-- unit: Anatomy of a Glue job -->

<!-- goals -->

- Read and write the structure of a Glue PySpark job.
- Follow a job run through its states, IDs and logs.

<!-- concept -->

A Glue Spark job is a Spark application with a thin Glue layer around it. The Glue context adds catalog-aware readers and writers; the job object tracks state between runs, which is what bookmarks rely on. Everything else is ordinary PySpark.

Each run gets an ID and goes through states you can watch and react to. Logs and metrics land in CloudWatch, organized by run.

<!-- example -->

```python
import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

args = getResolvedOptions(sys.argv, ["JOB_NAME", "process_date"])
glue = GlueContext(SparkContext.getOrCreate())
job = Job(glue); job.init(args["JOB_NAME"], args)
df = glue.spark_session.read.parquet(f"s3://lake/raw/orders/dt={args['process_date']}/")
df.write.mode("overwrite").parquet(f"s3://lake/curated/orders/dt={args['process_date']}/")
job.commit()
```

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

#### What are job run states?

`STARTING`, `RUNNING`, `STOPPING`, `STOPPED`, `SUCCEEDED`, `FAILED`, `TIMEOUT`, `ERROR` and `WAITING`. EventBridge receives state change events for alerts and orchestration.

#### What is the Glue job run ID used for?

It identifies a run for monitoring, logs, bookmark rewinds and retries, and can be passed into outputs (for example as a column) for lineage.

#### What happens to logs of a Glue job?

Driver and executor logs go to CloudWatch Logs (`/aws-glue/jobs/output` and `/aws-glue/jobs/error`); continuous logging streams them during the run. Use `glue.get_logger()` for structured messages.

<!-- challenge -->

A job forgets to call `job.commit()`. Bookmarks are enabled. What happens on the next run?

<!-- solution -->

The bookmark never advances, so every run reprocesses the same data as if it were new, which can create duplicates downstream. Add `job.commit()` at the end of successful processing.

<!-- takeaways -->

- A Glue job is Spark plus a Glue context and job state.
- `job.commit()` saves bookmark state after success.
- Run IDs tie together states, logs and metrics.

<!-- unit: Parameters, libraries and catalog access -->

<!-- goals -->

- Pass arguments and add Python or Java dependencies to jobs.
- Use Spark SQL against the Glue catalog.

<!-- concept -->

The same script should run for any date or environment, so everything variable comes in as job arguments. Dependencies arrive the same way: Python packages and JARs are named in job parameters and installed when the job starts, which keeps scripts portable but adds start-up time for large installs.

Enabling the catalog as Spark's metastore lets jobs use plain SQL on catalog tables, which many teams find clearer than Glue-specific APIs.

<!-- example -->

```text
--process_date                 2026-10-17
--additional-python-modules    pydantic==2.9.2,s3://artifacts/libs/etl_lib-1.4.0-py3-none-any.whl
--extra-jars                   s3://artifacts/jars/postgresql-42.7.4.jar
--enable-glue-datacatalog      true
```

#### How do you pass parameters to a Glue job?

As job arguments (`--target_path s3://...`) set in the job definition or overridden at run start, read with `getResolvedOptions`. Special arguments configure Glue itself, such as `--job-bookmark-option`, `--enable-metrics`, `--additional-python-modules` or `--conf`.

#### How do you add Python libraries to a Glue job?

With `--additional-python-modules` (installs from PyPI or wheels in S3 at start-up), `--extra-py-files` (zip or py files in S3), or by packaging dependencies in a wheel. For jobs without internet access, host wheels in S3 or use a private repository through a VPC endpoint.

#### How do you add JAR dependencies?

With `--extra-jars` pointing to JAR files in S3, used for JDBC drivers or Spark libraries not included in the Glue version.

#### What does `--enable-glue-datacatalog` do?

It configures Spark in the job to use the Glue Data Catalog as its Hive metastore, so `spark.sql("SELECT * FROM raw.orders")` and `saveAsTable` work against catalog tables.

#### How do you use Spark SQL inside a Glue job?

Convert to a DataFrame, register a temporary view, and run `spark.sql()`. With the Data Catalog enabled as the Hive metastore (`--enable-glue-datacatalog`), you can query catalog tables directly by `database.table`.

<!-- challenge -->

A job installs 15 PyPI packages at start-up and sometimes fails when PyPI is slow. How do you make it reliable?

<!-- solution -->

Build a wheel (or a bundle of wheels) with pinned versions in CI, store it in S3, and reference it in `--additional-python-modules`. Start-up no longer depends on PyPI, and versions stay fixed.

<!-- takeaways -->

- Job arguments make one script work for every run.
- Dependencies come from job parameters at start-up.
- The catalog can act as Spark's metastore.

<!-- unit: Execution options -->

<!-- goals -->

- Choose between Spark, Python shell, Flex and auto scaling.
- Set timeouts, retries and concurrency deliberately.

<!-- concept -->

Not every job needs a Spark cluster, and not every Spark job needs to start immediately. Python shell jobs handle light tasks cheaply; Flex runs non-urgent Spark on spare capacity at a discount; auto scaling sizes the cluster per stage.

Defaults are risky. A 48-hour timeout lets a stuck job burn money for two days, and retries on a non-idempotent job duplicate data. Set both on purpose, along with how many runs may overlap.

<!-- example -->

```python
glue.create_job(Name="orders_daily", Role=ROLE, GlueVersion="5.0",
    Command={"Name": "glueetl", "ScriptLocation": "s3://artifacts/jobs/orders_daily.py"},
    WorkerType="G.1X", NumberOfWorkers=10, ExecutionClass="FLEX",
    Timeout=60, MaxRetries=1, ExecutionProperty={"MaxConcurrentRuns": 1},
    DefaultArguments={"--enable-auto-scaling": "true", "--TempDir": "s3://glue-temp/orders/"})
```

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

#### What is the temporary directory (`--TempDir`) used for?

An S3 location where Glue writes intermediate data, for example when loading into Redshift or for shuffle in some configurations. It should have a lifecycle rule to delete old files.

<!-- challenge -->

A nightly report job only needs to finish by 08:00 and runs 30 minutes. How can you cut its cost without code changes?

<!-- solution -->

Run it with the Flex execution class, which uses spare capacity at a lower price; the possibly slower start doesn't matter given the deadline. Also set a sensible timeout and enable auto scaling.

<!-- takeaways -->

- Python shell for light tasks; Flex for non-urgent Spark.
- Never keep the 48-hour default timeout.
- Retry only idempotent jobs; limit concurrent runs.

<!-- unit: Developing jobs -->

<!-- goals -->

- Develop Glue jobs interactively and locally.
- Choose between the visual editor and scripts.

<!-- concept -->

Waiting a minute for each test run kills productivity. Interactive sessions give you a Spark session in a notebook or IDE, billed only while open; the Glue Docker images let you run jobs and tests on your laptop with the same libraries.

The visual editor speeds up simple jobs and helps non-programmers, but complex logic, reuse and testing are easier in scripts kept in Git.

<!-- example -->

```bash
docker run -it -v ~/.aws:/home/hadoop/.aws -v $PWD:/home/hadoop/workspace \
  public.ecr.aws/glue/aws-glue-libs:5 \
  spark-submit workspace/jobs/orders_daily.py --JOB_NAME local --process_date 2026-10-17
```

#### What are Glue interactive sessions?

On-demand Spark sessions you use from Jupyter notebooks, Glue Studio notebooks or your IDE to develop and debug Glue code interactively, billed per second with an idle timeout.

#### How do you develop Glue jobs locally?

With the official Glue Docker images (which include the Glue libraries and Spark of a given Glue version), running scripts and pytest locally, or with interactive sessions from a local notebook. Pure PySpark logic can also be tested with a local SparkSession.

#### What is the difference between the Spark script editor and the visual editor?

The visual editor builds jobs as a graph of nodes and generates code; it's quick for standard ETL and accessible to analysts. The script editor gives full control over PySpark or Scala code. Many teams start visually, then switch to code managed in Git.

<!-- challenge -->

A team builds every job in the visual editor and now has 40 jobs with copied logic. What do you propose?

<!-- solution -->

Move shared logic into a Python package with tests, write new jobs as scripts that import it, and keep the visual editor for prototypes. Store scripts and job definitions in Git and deploy them as code.

<!-- takeaways -->

- Interactive sessions give fast feedback in notebooks.
- Glue Docker images run jobs and tests locally.
- Scripts in Git scale better than visual jobs.

<!-- unit: Sources and sinks -->

<!-- goals -->

- Read databases in parallel and write to warehouses and table formats.
- Handle nested JSON and bad records on read.

<!-- concept -->

Most job problems start at the edges. A database read without partitioning runs on one executor no matter how many workers you pay for. A warehouse write goes through S3 staging and needs permissions on both. Open table formats must be enabled explicitly.

Files bring their own issues: nested structures to flatten and malformed records to quarantine instead of letting them fail the job or vanish.

<!-- example -->

```python
df = (spark.read.format("jdbc")
      .option("url", url).option("dbtable", "public.orders")
      .option("partitionColumn", "order_id").option("lowerBound", 1)
      .option("upperBound", 50_000_000).option("numPartitions", 16)
      .load())                               # 16 parallel reads instead of 1
```

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

#### How do you read from DynamoDB in Glue?

With the DynamoDB connector: either directly (consumes read capacity, controlled by `dynamodb.throughput.read.percent`) or through DynamoDB export to S3 (`dynamodb.export`), which doesn't consume table capacity and is preferred for large tables.

#### How do Glue jobs connect to Snowflake, BigQuery or other non-AWS sources?

Through native Glue connectors for many sources (Snowflake, BigQuery, Teradata, SAP HANA, MongoDB and SaaS applications), through AWS Marketplace connectors, or through JDBC with a custom driver and Glue connection.

#### How do you read JSON with nested structures in Glue?

Read it as a DynamicFrame or DataFrame (schema inferred or declared), then flatten with `select` of nested fields, `explode` for arrays, or Glue's `Relationalize` for a fully relational output.

#### How do you handle bad records when reading files?

For Spark readers, use `mode` (`PERMISSIVE` with a corrupt record column, `DROPMALFORMED`, `FAILFAST`) or `badRecordsPath` where supported; for DynamicFrames, errors are captured per record and can be inspected with `errorsAsDynamicFrame()` and thresholds set with `stageThreshold` and `totalThreshold`.

<!-- challenge -->

A job reading a 200 GB PostgreSQL table uses 20 workers but takes 3 hours, and only one executor is busy. What is wrong?

<!-- solution -->

The JDBC read isn't partitioned, so one connection reads everything. Add `partitionColumn`, bounds and `numPartitions` (or `hashfield`/`hashpartitions` for DynamicFrames) on an indexed numeric column, within what the database can handle.

<!-- takeaways -->

- Partition JDBC reads or they run on one executor.
- Enable table formats with `--datalake-formats`.
- Quarantine bad records instead of losing them.

### DynamicFrames and transforms

<!-- unit: DynamicFrames and DataFrames -->

<!-- goals -->

- Explain what DynamicFrames add and when to switch to DataFrames.
- Write DynamicFrames with catalog updates and bookmarks.

<!-- concept -->

DynamicFrames were built for messy sources: each record carries its own schema, so inconsistent types don't stop the read. DataFrames assume one schema and get the full Spark optimizer in return. Most jobs use both: DynamicFrames at the edges, where catalog integration and bookmarks matter, and DataFrames for the transformation logic in between.

The `transformation_ctx` names connect each step to bookmark state, so they must be stable and unique.

<!-- example -->

```python
dyf = glue.create_dynamic_frame.from_catalog(database="raw", table_name="orders",
                                             transformation_ctx="src_orders")
df = dyf.toDF().where("status = 'paid'")            # DataFrame logic
out = DynamicFrame.fromDF(df, glue, "out_orders")
sink = glue.getSink(connection_type="s3", path="s3://lake/curated/orders/",
                    enableUpdateCatalog=True, partitionKeys=["dt"])
sink.setFormat("glueparquet"); sink.setCatalogInfo("curated", "orders"); sink.writeFrame(out)
```

#### What is a DynamicFrame?

Glue's distributed data structure, similar to a Spark DataFrame but where each record is self-describing, so it doesn't need a fixed schema upfront. It handles inconsistent and messy data (a field that is sometimes a string and sometimes an int) with "choice" types.

#### What is the difference between a DynamicFrame and a DataFrame?

A DataFrame has one schema for the whole dataset and the full Spark SQL optimizer and API. A DynamicFrame computes schema per record, supports choice types and Glue-specific transforms, bookmarks and catalog integration. You convert with `toDF()` and `DynamicFrame.fromDF()`, and most teams use DataFrames for transformations.

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

<!-- challenge -->

Bookmarks stopped working after a refactor, and each run reads everything again. The reads look unchanged. What do you check?

<!-- solution -->

Whether the `transformation_ctx` values changed or were removed: bookmark state is stored per context name. Restore the original names (or reset the bookmark deliberately), and make sure `job.commit()` still runs.

<!-- takeaways -->

- DynamicFrames tolerate inconsistent schemas.
- DataFrames give the optimizer and a richer API.
- Stable `transformation_ctx` names keep bookmarks working.

<!-- unit: Schema-flexible transforms -->

<!-- goals -->

- Resolve mixed types and map columns with Glue transforms.
- Flatten nested data and survive new source columns.

<!-- concept -->

Sources rarely keep their promises. A column that was numbers yesterday has text today; a JSON field that was flat becomes nested; a vendor adds columns without warning. Glue's schema-flexible transforms handle this at the boundary: decide what to do with mixed types, map and cast columns explicitly, and flatten nesting into tables.

The principle is to absorb change in the raw-to-clean step and keep the curated schema stable and explicit.

<!-- example -->

```python
dyf = dyf.resolveChoice(specs=[("price", "cast:double")])
dyf = ApplyMapping.apply(frame=dyf, mappings=[
    ("id", "string", "order_id", "bigint"),
    ("price", "double", "amount", "decimal(12,2)"),
    ("ts", "string", "created_at", "timestamp")])
```

#### What is a choice type, and how does `ResolveChoice` work?

When a column has values of different types, a DynamicFrame keeps a choice type (for example `choice<int,string>`). `ResolveChoice` resolves it with `cast:long`, `make_cols` (split into `col_int` and `col_string`), `make_struct` or `project:string`.

```python
resolved = dyf.resolveChoice(specs=[("amount", "cast:double"), ("id", "cast:long")])
```

#### What does `ApplyMapping` do?

It renames columns, casts types and selects fields in one step, from a list of `(source, source_type, target, target_type)` tuples, which is how Glue Studio's mapping node works.

#### What does `Relationalize` do?

It flattens nested JSON into a set of relational tables: nested structs become columns and arrays become separate tables linked by generated keys, ready to load into a relational database.

#### What does `Unbox` do?

It parses a string column containing JSON (or CSV) into a struct, so nested fields become accessible columns.

#### A source system adds new columns without warning. How do you keep the Glue pipeline running?

Read with schema evolution in mind: use DynamicFrames or permissive schemas in raw, select columns explicitly in curated outputs, alert on new columns (crawler log-only mode or a schema check), and use Iceberg schema evolution to add columns intentionally.

<!-- challenge -->

A source sends `amount` as a number, but some days as a string with a currency symbol. The curated table must stay `decimal`. What do you do?

<!-- solution -->

Resolve the choice by casting to string first, strip non-numeric characters, cast to decimal with `try_cast` semantics, and route rows that still fail to a quarantine location with an alert.

<!-- takeaways -->

- Choice types record mixed types; `ResolveChoice` decides.
- `ApplyMapping` renames, casts and selects in one step.
- Absorb source changes in raw-to-clean; keep curated stable.

<!-- unit: Built-in transforms -->

<!-- goals -->

- Use built-in transforms for filtering, joining and splitting.
- Deduplicate and add audit columns.

<!-- concept -->

Glue ships transforms that mirror common SQL operations, mainly for the visual editor and DynamicFrame-only jobs. In code, the equivalent DataFrame operations are usually clearer and faster, so the built-ins matter most when you read generated jobs.

Two habits apply whatever API you use: deduplicate on a business key with a clear rule for which row wins, and stamp every row with where and when it came from.

<!-- example -->

```python
from pyspark.sql import functions as F, Window
w = Window.partitionBy("order_id").orderBy(F.col("updated_at").desc())
clean = (df.withColumn("rn", F.row_number().over(w)).where("rn = 1").drop("rn")
           .withColumn("ingested_at", F.current_timestamp())
           .withColumn("source_file", F.input_file_name()))
```

#### What are other built-in Glue transforms?

`DropFields`, `SelectFields`, `RenameField`, `Filter`, `Map`, `Join`, `SplitFields`, `SplitRows`, `Unbox` (parse JSON strings), `DropNullFields`, `FillMissingValues`, `FindMatches` (ML deduplication) and, in Glue Studio, transforms such as `Aggregate`, `Pivot`, `Derived column`, `Identify sensitive data` and `Evaluate data quality`.

#### How do you filter a DynamicFrame?

With `Filter.apply(frame=dyf, f=lambda row: row["status"] == "paid")` or `dyf.filter(...)`, though converting to a DataFrame and using `filter("status = 'paid'")` is usually faster because Spark can optimize it.

#### How do you join DynamicFrames?

With `Join.apply(dyf1, dyf2, "key1", "key2")`, which performs an equality join; for other join types or conditions, convert to DataFrames.

#### What does `SplitFields` do?

It splits a DynamicFrame into two collections by columns, for example separating PII columns from the rest to write them to different locations.

#### How do you deduplicate in a Glue job?

Convert to a DataFrame and use `dropDuplicates(["key"])` or a window function with `row_number()` ordered by an update timestamp, keeping the latest record per key.

#### How do you add audit columns in a Glue job?

Add columns such as `ingested_at` (`current_timestamp()`), `source_file` (`input_file_name()` or file metadata), `job_run_id` and `process_date`, so every row can be traced to the run and file that produced it.

<!-- challenge -->

A downstream team asks which file each curated row came from, after a bad file corrupted a report. What do you add, and where?

<!-- solution -->

Add `source_file` (from `input_file_name()` or file metadata), `ingested_at` and the job run ID as columns in the raw-to-clean step, and carry them into curated tables. Bad rows can then be traced and removed by file.

<!-- takeaways -->

- Built-ins mirror SQL; DataFrame code is often clearer.
- Deduplicate on a key with an explicit "winner" rule.
- Audit columns make data traceable to its source.

<!-- unit: Matching records with ML -->

<!-- goals -->

- Explain what FindMatches does and when it fits.
- Train and use it to deduplicate records without a shared key.

<!-- concept -->

Exact deduplication needs a key. When records describe the same customer differently across systems (different spellings, missing fields, swapped names), rules become endless. FindMatches learns what "the same" means from examples you label, then groups records into matches.

Its quality depends on the labels: a few hundred well-chosen pairs teach it more than thousands of easy ones.

<!-- example -->

```text
1. Create a FindMatches transform on customers (primary key: source_id)
2. Generate a labeling file, mark pairs as match / no match, upload it
3. Check estimated precision/recall; tune toward precision or recall
4. Use the transform in a job: output adds match_id per group
```

#### What is FindMatches?

A machine learning transform that identifies duplicate or matching records that don't share a common key (for example the same customer with different spellings), trained with labeled examples.

#### You need to deduplicate customer records with no common key across two systems. What Glue tool can help?

The FindMatches ML transform: label examples of matching and non-matching pairs, train the transform, and run it in a job to assign match IDs, then merge records per match ID with business rules.

<!-- challenge -->

After applying FindMatches, sales notice two different customers merged into one. Which setting do you adjust, and what else?

<!-- solution -->

Tune the transform toward precision rather than recall, so it merges only confident matches. Add labeled examples of similar-but-different customers, retrain, and review a sample of merged groups before publishing.

<!-- takeaways -->

- FindMatches learns matching from labeled pairs.
- Label hard cases, not easy ones.
- Trade precision against recall for the use case.

### Job bookmarks and incremental processing

<!-- unit: How job bookmarks work -->

<!-- goals -->

- Enable, pause, reset and rewind job bookmarks.
- Know the limits of bookmarks for files, JDBC and Iceberg.

<!-- concept -->

Bookmarks let a job remember what it already processed. For files, the state is based on paths and modification times; for databases, on key columns you choose. The state advances only when a run commits successfully, so failures never skip data.

Bookmarks are convenient but implicit: overwritten files, renamed contexts or a shared source can confuse them, and they don't apply to Iceberg sources. Know how to reset them before you need to.

<!-- example -->

```bash
aws glue start-job-run --job-name orders_daily \
  --arguments '{"--job-bookmark-option": "job-bookmark-enable"}'
aws glue reset-job-bookmark --job-name orders_daily --run-id jr_0a1b2c   # rewind to a run
```

#### What are job bookmarks?

A Glue feature that stores state between job runs so each run processes only new data: for S3 sources, which files (by modification time) were processed; for JDBC sources, the highest values of bookmark key columns.

#### How do you enable and control job bookmarks?

With `--job-bookmark-option`: `job-bookmark-enable`, `job-bookmark-disable` or `job-bookmark-pause` (process from the last bookmark without updating it). The source needs a `transformation_ctx` and the script must call `job.commit()`.

#### How do you reset or rewind a bookmark?

With the console or the `ResetJobBookmark` API, which makes the next run reprocess everything; you can also rewind to a previous run ID to reprocess from that point.

#### What happens to bookmarks if a job fails?

Bookmarks are only updated on `job.commit()` after success, so a failed run leaves the bookmark where it was and the next run processes the same data again. That's why writes must be idempotent.

#### Can two different jobs share a bookmark?

No. Bookmarks are per job (and per `transformation_ctx`). Two jobs reading the same source keep independent state.

#### How do JDBC bookmarks work?

You specify `jobBookmarkKeys` (columns such as an increasing ID or `updated_at`) and a sort order; the job reads rows with values greater than the last stored maximum. Updates to rows with old key values are missed, so it fits append-only tables or monotonic timestamps.

#### What are the limits of job bookmarks?

They track files by modification time, so overwritten files with the same name may be missed or reprocessed; JDBC bookmarks need monotonically increasing key columns and don't see updates to old rows; they only work with certain sources and formats; and they don't make writes idempotent, so a failure after writing and before `commit` reprocesses data.

#### Do job bookmarks work with Iceberg tables as sources?

Not in the same way; for Iceberg sources you process incrementally with Iceberg's own features, such as reading changes between snapshots (incremental reads or changelog views) and storing the last processed snapshot ID.

<!-- challenge -->

A bug corrupted the last three runs' output. Bookmarks are on. How do you reprocess just those runs?

<!-- solution -->

Fix the code, delete or overwrite the three runs' output, then rewind the bookmark to the run before the first bad one with `ResetJobBookmark` and a run ID. The next run reprocesses everything since.

<!-- takeaways -->

- Bookmarks track processed files or keys per job.
- They advance only on successful commit.
- Know their limits: overwritten files, Iceberg, renamed contexts.

<!-- unit: Incremental without bookmarks -->

<!-- goals -->

- Process explicit date ranges with predicates.
- Make jobs idempotent and handle late data.

<!-- concept -->

Many teams prefer explicit increments over bookmarks: the orchestrator passes a date, the job reads that partition with a pushdown predicate, and it overwrites that partition's output. The run becomes a pure function of its argument, which makes reruns, backfills and late data simple to reason about.

Predicates matter for performance too: pushed to the catalog, they stop the job from listing partitions it will never read.

<!-- example -->

```python
dyf = glue.create_dynamic_frame.from_catalog(
    database="raw", table_name="orders",
    push_down_predicate=f"dt = '{args['process_date']}'",
    additional_options={"catalogPartitionPredicate": f"dt = '{args['process_date']}'"})
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
dyf.toDF().write.mode("overwrite").partitionBy("dt").parquet("s3://lake/curated/orders/")
```

#### How do you make a Glue job idempotent?

Write output for the processed partition with overwrite (dynamic partition overwrite) or use `MERGE` on an Iceberg table, rather than appending blindly; base the processed period on a parameter; and keep bookmarks as an optimization, not the only guarantee.

#### What is pushdown predicate in Glue?

A filter on partition columns passed when reading from the catalog (`push_down_predicate="order_date >= '2026-10-01'"`) so Glue lists and reads only matching partitions instead of the whole table.

#### What is `catalogPartitionPredicate`?

A server-side partition filter evaluated by the Data Catalog using partition indexes, which reduces the number of partitions Glue has to fetch from the catalog for tables with very many partitions. It can be combined with `push_down_predicate`.

#### How do you process only yesterday's data without bookmarks?

Pass the date as a job argument (from the scheduler), read with a pushdown predicate on the date partition, and overwrite that date's output partition. This is explicit, reproducible and makes backfills easy.

#### How do you implement a "late data" correction in a daily Glue pipeline?

Process a rolling window (for example the last three days) each run with partition overwrite or `MERGE`, so late records update the right partitions, and keep the window parameterized for larger corrections.

<!-- challenge -->

A job overwrites the whole curated table each run with only today's data, wiping history. Which setting is missing?

<!-- solution -->

Dynamic partition overwrite: set `spark.sql.sources.partitionOverwriteMode=dynamic` (and write with `partitionBy`) so only the partitions in the output are replaced, or write directly to the partition path.

<!-- takeaways -->

- Pass dates explicitly; read with pushdown predicates.
- Overwrite only the partitions a run owns.
- Rolling windows absorb late data.

### Streaming ETL

<!-- unit: Glue streaming jobs -->

<!-- goals -->

- Describe Glue streaming jobs, their sources and schemas.
- Choose between Glue streaming, Firehose and Flink.

<!-- concept -->

A streaming job is a Spark job that never ends: it reads a stream in micro-batches and writes each batch somewhere, usually S3 or a table format. Because it runs continuously, you pay for every hour, so it's worth it only when freshness truly matters and transformations need Spark.

Simpler delivery fits Firehose; complex event processing with low latency fits Flink. Glue streaming sits in between.

<!-- example -->

| Need | Choice |
|---|---|
| Deliver events to S3 as Parquet, no logic | Firehose |
| Join stream with lake data, write Iceberg every minute | Glue streaming |
| Sub-second windows, complex state | Managed Service for Apache Flink |

#### What are Glue streaming jobs?

Long-running Spark Structured Streaming jobs that read from Kinesis Data Streams, Amazon MSK or self-managed Kafka, transform records in micro-batches and write to S3, data lakes formats, databases or other streams.

#### What sources can Glue streaming read?

Amazon Kinesis Data Streams, Amazon MSK, self-managed Apache Kafka, and (through connectors) other streaming systems. Outputs include S3, Iceberg/Hudi/Delta tables, JDBC databases and other streams.

#### How does a Glue streaming job handle schemas?

From a Data Catalog table describing the stream, from the Glue Schema Registry, or by inferring the schema from the data. Records that don't fit can be handled with choice types or routed to an error path.

#### When would you choose Glue streaming over Kinesis Data Firehose or Managed Service for Apache Flink?

Firehose for simple delivery to S3, Redshift or OpenSearch with light transformation and no code. Managed Flink for low-latency, stateful stream processing with complex event-time logic. Glue streaming when the team already uses Spark, needs micro-batch ETL to a data lake and wants shared code with batch jobs.

#### How are Glue streaming jobs billed?

Per DPU-hour for as long as they run, since they run continuously; G.025X workers reduce cost for low-volume streams. Auto scaling helps with variable traffic.

<!-- challenge -->

A team runs a Glue streaming job 24/7 just to write raw Kinesis events to S3 as Parquet. What would you suggest?

<!-- solution -->

Use Kinesis Data Firehose with Parquet conversion and dynamic partitioning: no code, no cluster running all day, and lower cost. Keep Glue for later batch transformations.

<!-- takeaways -->

- Streaming jobs are always-on Spark micro-batches.
- You pay for every hour they run.
- Firehose for simple delivery; Flink for complex low latency.

<!-- unit: Running streams reliably -->

<!-- goals -->

- Tune windows and checkpoints for reliable streaming.
- Handle small files, code updates and late events.

<!-- concept -->

Reliability in streaming comes from the checkpoint: it records what was read and what state exists, so a restarted job continues exactly where it stopped. Everything else follows from protecting it. Code changes must stay compatible with it, and output must tolerate a batch being written twice.

Window size is the main trade-off: shorter means fresher data but more, smaller files, which then need compaction.

<!-- example -->

```python
glue.forEachBatch(frame=stream_df,
    batch_function=write_batch,
    options={"windowSize": "120 seconds",
             "checkpointLocation": "s3://glue-checkpoints/orders_stream/"})
```

#### What is the window size in Glue streaming?

The interval of each micro-batch (`windowSize`, for example 100 seconds) in `forEachBatch`. Larger windows reduce small files and overhead; smaller ones reduce latency.

#### Where does a streaming job keep its progress?

In a checkpoint location in S3, which stores offsets and state so the job resumes from where it stopped after a restart or update.

#### How do you avoid small files from streaming jobs?

Use larger windows, write to Iceberg or Hudi tables and compact them (or rely on catalog compaction for Iceberg), or run a separate compaction job.

#### How do you update a running streaming job's code?

Stop the job and start the new version with the same checkpoint location, as long as the changes are compatible with the stored state; incompatible changes need a new checkpoint and a plan for replaying or skipping data.

#### How do you handle late events in Glue streaming?

With Spark Structured Streaming's event-time windows and watermarks for aggregations, or by writing events to partitions by event date and letting downstream jobs reprocess recent partitions.

<!-- challenge -->

After a deployment, a streaming job starts reading from the beginning of the stream and duplicates a day of data. What happened?

<!-- solution -->

The new version used a different (or empty) checkpoint location, so it had no record of progress. Deploy with the same checkpoint path, and make the sink idempotent (for example `MERGE` into Iceberg on event ID) so replays don't duplicate.

<!-- takeaways -->

- The checkpoint holds progress; never lose it.
- Larger windows and compaction fight small files.
- Make sinks idempotent so replays are safe.

<!-- stage: Running in production -->

### Workers, performance and cost

<!-- unit: Sizing workers -->

<!-- goals -->

- Choose worker types and counts for a job.
- Estimate a job's cost before running it.

<!-- concept -->

Sizing is a choice between more workers and bigger workers. More workers add parallelism, which helps when the data splits evenly. Bigger or memory-optimized workers help when single tasks need memory, as in large joins or wide rows. Auto scaling handles jobs whose stages need different amounts.

Since cost is workers times time, a bigger cluster that finishes much faster can cost the same or less.

<!-- example -->

```text
G.1X × 20 workers × 0.5 h = 10 DPU-h  ≈ 4.40 USD
G.2X × 10 workers × 0.3 h =  6 DPU-h  ≈ 2.64 USD   (no spill, faster)
```

#### What worker types does Glue offer?

G.1X (1 DPU: 4 vCPU, 16 GB), G.2X (2 DPU), G.4X (4 DPU), G.8X (8 DPU), and larger types on recent versions, G.025X (0.25 DPU, for low-volume streaming), and memory-optimized R types for memory-heavy jobs. Bigger workers suit memory-intensive transforms; more workers suit parallel work.

#### How do you choose the number of workers?

Start from data volume and complexity, enable auto scaling with a sensible maximum, and look at job metrics: if executors are idle, reduce; if stages spill or tasks queue, increase or use bigger workers. Measure cost per run.

#### When should you use G.2X or larger workers instead of more G.1X workers?

When executors run out of memory (large joins, wide rows, big aggregations, ML transforms) or spill heavily. If tasks are small and numerous, more smaller workers give the same parallelism at the same price.

#### What are R-type (memory-optimized) workers?

Worker types with a higher memory-to-CPU ratio, for jobs that are memory-bound rather than CPU-bound, such as large broadcast joins or caching.

#### What does `--enable-auto-scaling` require?

Glue 3.0 or later, a maximum number of workers, and a workload that varies across stages. Glue then adjusts executors based on pending tasks.

#### How do you estimate the cost of a Glue job?

Workers × DPU per worker × runtime in hours × price per DPU-hour. For example 10 G.1X workers for 15 minutes is 10 × 1 × 0.25 = 2.5 DPU-hours, about 1.10 USD at 0.44 USD per DPU-hour. With auto scaling, check actual DPU-seconds in job run details.

<!-- challenge -->

Executors of a join-heavy job keep dying with out-of-memory errors on 40 G.1X workers. Adding workers didn't help. What do you try?

<!-- solution -->

Switch to G.2X (or R-type) workers so each executor has more memory, with fewer of them. Also check for skewed keys and whether a small side can be broadcast, since one hot key fails no matter the count.

<!-- takeaways -->

- More workers add parallelism; bigger workers add memory.
- Auto scaling fits jobs with uneven stages.
- Cost is workers × DPU × time; faster can be cheaper.

<!-- unit: Diagnosing slow jobs -->

<!-- goals -->

- Use the Spark UI and observability metrics to find bottlenecks.
- Investigate a job that suddenly became slow.

<!-- concept -->

A slow Glue job is a slow Spark job, so the tools are the same: find the slowest stage, then ask whether it reads too much, shuffles too much, spills, or waits on one task. Glue adds metrics per job and executor and a Spark UI built from event logs.

When a job slows down suddenly, compare runs before reading code: input size, file counts, skipped predicates and changed configuration explain most regressions.

<!-- example -->

```text
--enable-metrics                 true
--enable-observability-metrics   true
--enable-spark-ui                true
--spark-event-logs-path          s3://glue-sparkui/orders_daily/
```

#### How do you troubleshoot a slow Glue job?

Enable job metrics, observability metrics and the Spark UI (event logs to S3), then look at stage durations, skewed tasks, shuffle sizes and spill, executor utilization, and the number of input files. Job run insights point to the failing line and common causes.

#### What is the Glue Spark UI?

A Spark history server view of a job run's event logs (enabled with `--enable-spark-ui` and an S3 log path), available in the Glue console, to analyze stages, tasks, storage and SQL plans.

#### What are Glue observability metrics?

CloudWatch metrics at job, stage and executor level (CPU, memory, disk, shuffle, skewness, worker utilization, throughput) that help detect bottlenecks and size jobs.

#### A Glue job that used to take 10 minutes now takes 2 hours. How do you investigate?

Compare input volume and number of files, check whether the pushdown predicate or bookmarks stopped working (reprocessing everything), look at the Spark UI for skew or spill, check worker count and auto scaling, and check for a changed join or a lost broadcast.

<!-- challenge -->

The Spark UI shows one task of 200 in a stage running 50 minutes while the others take 20 seconds. What is it, and what do you try?

<!-- solution -->

Data skew: one key holds most rows. Check the key distribution, rely on AQE skew join handling, broadcast the smaller side if possible, or salt the hot key. Filtering junk keys like `NULL` often fixes it.

<!-- takeaways -->

- Find the slowest stage, then the cause.
- Compare runs: input size, files, predicates, configs.
- One long task in a stage usually means skew.

<!-- unit: Shuffles, skew and memory -->

<!-- goals -->

- Use AQE and Spark settings to reduce shuffle problems.
- Fix disk and memory errors caused by shuffles.

<!-- concept -->

Shuffles move data between workers for joins and aggregations, and they cause most memory and disk failures. Adaptive Query Execution fixes many problems at runtime by merging small partitions, switching to broadcast joins and splitting skewed ones.

When a shuffle is simply larger than the workers' disks, you either give it more room (bigger workers, shuffle to S3) or make it smaller (filter early, select fewer columns, pre-aggregate).

<!-- example -->

```text
--conf spark.sql.adaptive.enabled=true
--conf spark.sql.shuffle.partitions=400
--write-shuffle-files-to-s3 true
```

#### How does Spark's Adaptive Query Execution help in Glue?

Enabled by default on Glue 4.0+, it coalesces small shuffle partitions, converts joins to broadcast when one side is small and splits skewed partitions, which improves performance without manual tuning.

#### How do you handle data skew in a Glue job?

Same as in Spark: rely on Adaptive Query Execution (enabled on recent Glue versions), broadcast small tables, isolate hot keys or salt them, and check the Spark UI for stragglers.

#### How do you pass Spark configuration to a Glue job?

With the `--conf` job parameter (for example `--conf spark.sql.shuffle.partitions=400`), keeping in mind that some settings are managed by Glue and can't be changed.

#### What is the S3 shuffle option in Glue?

An option (`--write-shuffle-files-to-s3`) that writes Spark shuffle data to S3 instead of local disk, avoiding "no space left on device" failures on shuffle-heavy jobs, at the cost of some speed.

#### Your Glue job fails with "No space left on device". What do you do?

The job is spilling or shuffling more than local disk can hold. Use bigger workers (more disk per executor), enable the S3 shuffle option, reduce data before shuffles (filter and select earlier), fix skew, and increase partitions so each task handles less data.

<!-- challenge -->

A job aggregates 2 TB but only needs 5 of 80 columns. It fails with disk errors. What two changes come first?

<!-- solution -->

Select the 5 columns and apply filters before the aggregation, so the shuffle carries far less data. If it still spills, use larger workers or enable S3 shuffle.

<!-- takeaways -->

- AQE handles partition sizing, broadcast and skew at runtime.
- Shrink shuffles first: filter and select early.
- Bigger workers or S3 shuffle give shuffles more room.

<!-- unit: Output layout -->

<!-- goals -->

- Write files and partitions that downstream engines read cheaply.
- Fix small-file problems in Glue output.

<!-- concept -->

A Glue job's output is someone else's input. Athena bills per byte scanned and plans per file and partition, so the way a job writes decides query cost for months. Columnar formats, sensible partitions and files of a few hundred megabytes are the target.

Spark tends to produce one file per task per partition, so without a repartition step, output can explode into thousands of tiny files.

<!-- example -->

```python
(df.repartition("dt")                       # one task per date → few files per partition
   .write.mode("overwrite")
   .option("compression", "zstd")
   .partitionBy("dt")
   .parquet("s3://lake/curated/events/"))
```

#### What is the small-files problem in Glue, and how do you handle it?

Reading many small files creates many tasks and S3 requests and slows jobs. Glue can group files at read time (`groupFiles: inPartition`, `groupSize`), and you should write fewer, larger files (repartition before writing, around 128 MB–1 GB per file) or compact Iceberg tables.

```python
dyf = glue.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://lake/raw/clicks/"], "recurse": True,
                        "groupFiles": "inPartition", "groupSize": "134217728"},
    format="json")
```

#### How do you write output with a controlled number of files?

Repartition or coalesce before writing (`df.repartition(20, "order_date")`), or set `spark.sql.files.maxRecordsPerFile`, so each partition gets a few large files instead of hundreds of small ones.

#### Why convert raw CSV or JSON to Parquet?

Parquet is columnar and compressed: Athena, Redshift Spectrum and Spark read only needed columns, skip row groups with statistics, and scan far less data, which reduces both time and cost.

#### What makes Parquet files efficient for later queries?

Columnar layout, compression (Snappy or ZSTD), row group statistics for skipping, reasonable file sizes (hundreds of MB), and sorting or partitioning by common filter columns.

#### How does partitioning strategy affect Glue and Athena?

Partition by columns used in most filters (usually date), with a moderate number of partitions each holding enough data; too fine (by hour and customer) creates millions of tiny partitions and slow planning, too coarse forces large scans.

#### A Glue job writes thousands of tiny Parquet files per day. How do you fix it?

Repartition by the partition column before writing so each partition gets a few files, increase the batch size (process a day rather than every few minutes), and if using Iceberg enable catalog compaction or run `rewrite_data_files`.

#### Analysts complain Athena queries on Glue tables are expensive. What changes do you make in the Glue jobs?

Write Parquet or Iceberg instead of CSV/JSON, compress, partition by common filters, produce fewer larger files, compute column statistics, and maybe create aggregated tables for frequent dashboards.

<!-- challenge -->

A job writes a table partitioned by `dt` and `customer_id`, producing 400,000 files a day. What do you change?

<!-- solution -->

Partition by `dt` only, repartition by `dt` before writing so each day gets a few large files, and sort or bucket by `customer_id` inside. Compact existing data once.

<!-- takeaways -->

- Output layout decides downstream query cost.
- Repartition before writing to control file counts.
- Partition by common filters, not high-cardinality keys.

<!-- unit: Cost and start-up -->

<!-- goals -->

- Apply the main levers for lowering Glue costs.
- Reduce job start-up time.

<!-- concept -->

Glue cost reduction is mostly about not paying for idle or waste: run on the newest version, let auto scaling drop unused workers, use Flex where deadlines allow, process increments instead of full reloads, and cap runaway jobs with timeouts.

Start-up time matters for frequent small jobs, where waiting can exceed the work itself. Newer versions start faster, and heavy dependency installs slow every run.

<!-- example -->

| Lever | Typical effect |
|---|---|
| Upgrade to latest Glue version | Faster start and runtime |
| Auto scaling | Fewer idle workers |
| Flex execution | Lower price for non-urgent jobs |
| Incremental instead of full reload | Less data processed |

#### How do you reduce Glue costs?

Use the latest Glue version (faster start and runtime), enable auto scaling, use Flex for non-urgent jobs, right-size workers, set timeouts, process incrementally with partitions or bookmarks, read only needed partitions and columns, avoid crawlers where tables can be defined in code, and turn off development endpoints and idle sessions.

#### Why do Glue jobs take time to start, and how do you reduce it?

Glue provisions the environment at each run. Glue 2.0 and later start in seconds to about a minute; Flex can take longer. Reduce start time with newer versions, fewer extra modules installed at start-up (prebuild wheels), and avoid many tiny jobs that could be one.

<!-- challenge -->

A job runs every 5 minutes for 40 seconds of work and costs more than expected. Why, and what do you change?

<!-- solution -->

Each run pays a minimum and start-up time, so overhead dominates. Batch work into fewer runs (for example every 30 minutes), use a Python shell job if Spark isn't needed, or switch to a streaming or Lambda design.

<!-- takeaways -->

- Pay for work, not idle: auto scaling, Flex, timeouts.
- Process increments, not full reloads.
- Frequent tiny jobs waste money on start-up.

### Data quality and sensitive data

<!-- unit: Data Quality rules -->

<!-- goals -->

- Write DQDL rules, including composite and referential ones.
- Get rule recommendations from data profiles.

<!-- concept -->

Glue Data Quality turns expectations about data into rules you can run on every load: counts, completeness, uniqueness, allowed values, relationships. Writing them in DQDL keeps them declarative and reviewable, like code.

Starting from scratch is hard, so recommendations profile a table and propose rules. Treat them as a draft: keep the ones that express real business expectations, and tighten thresholds over time.

<!-- example -->

```text
Rules = [
  RowCount > 1000,
  IsComplete "order_id", IsUnique "order_id",
  ColumnValues "status" in ["paid", "refunded", "cancelled"],
  (ColumnValues "amount" > 0) or (ColumnValues "status" = "refunded"),
  ReferentialIntegrity "customer_id" "customers.customer_id" = 1.0
]
```

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

#### What are composite rules in DQDL?

Rules combined with `and` and `or`, for example `(ColumnValues "status" = "paid") and (ColumnValues "amount" > 0)`, to express conditions involving several columns.

#### How do you check referential integrity in Glue Data Quality?

With rules like `ReferentialIntegrity` that compare a column with another dataset's key column, or `DatasetMatch` to compare two datasets, passing the reference dataset as an additional source.

#### How do you get rule recommendations in Glue Data Quality?

Run a recommendation task on a catalog table: Glue profiles the data and proposes DQDL rules (completeness, uniqueness, value ranges, allowed values) that you review and edit before using.

<!-- challenge -->

A recommendation suggests `ColumnValues "country" in [...]` with today's 12 countries. Should you accept it as is?

<!-- solution -->

Not blindly: a new market would fail the job. Confirm the list with the business, or replace it with a reference-table check, and decide whether a new value should fail the load or only warn.

<!-- takeaways -->

- DQDL rules declare expectations as code.
- Composite and referential rules express business logic.
- Recommendations are a starting draft.

<!-- unit: Acting on quality and sensitive data -->

<!-- goals -->

- Route, store and alert on data quality results.
- Detect and handle sensitive data in pipelines.

<!-- concept -->

A rule that fails silently is decoration. Quality results need consequences: rows that fail go to quarantine, runs that fail stop publishing, and owners get notified. Anomaly detection adds checks no one wrote, by flagging values that drift from history.

Sensitive data is a related problem: before data spreads to curated layers, detection can find PII and mask, hash or remove it.

<!-- example -->

```python
dq = EvaluateDataQuality().process_rows(frame=orders, ruleset=RULES,
        publishing_options={"dataQualityEvaluationContext": "orders_dq",
                            "enableDataQualityCloudWatchMetrics": True})
rows = SelectFromCollection.apply(dfc=dq, key="rowLevelOutcomes")
passed = rows.filter(lambda r: r["DataQualityEvaluationResult"] == "Passed")
failed = rows.filter(lambda r: r["DataQualityEvaluationResult"] == "Failed")   # → quarantine
```

#### How do you act on data quality results in a job?

Use the Evaluate Data Quality transform, then route rows: keep passing rows, write failing rows to a quarantine location, and fail the job or send an EventBridge alert when the overall score drops below a threshold.

#### What is data quality anomaly detection?

Glue learns statistics over runs (row counts, distinct values, distributions) and flags unusual values even without explicit thresholds, which catches problems like a sudden drop in volume.

#### How do you get alerts for data quality failures?

Glue publishes data quality results to EventBridge and CloudWatch; rules can send notifications through SNS or trigger remediation workflows.

#### Where are data quality results stored?

In the Glue console history, in CloudWatch metrics, as EventBridge events and, optionally, written to S3 by the job, where they can be queried with Athena for trends.

#### What is sensitive data detection in Glue?

A transform that scans data for PII such as names, emails, phone numbers, credit cards and national IDs (with country-specific detectors), and can redact, hash or report the findings, helping comply with GDPR or similar laws.

<!-- challenge -->

Daily row counts dropped 60% one day, but no rule failed because the threshold was `RowCount > 1000`. What do you add?

<!-- solution -->

Enable anomaly detection on row count (or a rule comparing with the recent average), and alert through EventBridge to the owners. Static minimums miss large relative drops.

<!-- takeaways -->

- Quarantine failing rows; stop bad publishes.
- Anomaly detection catches drift static rules miss.
- Detect and mask PII before curated layers.

### Orchestration

<!-- unit: Triggers and workflows -->

<!-- goals -->

- Build pipelines with Glue triggers and workflows.
- Share state across a workflow and resume failures.

<!-- concept -->

Glue has its own lightweight orchestration. Triggers start jobs and crawlers on a schedule, on demand, or when others finish; workflows group them into a graph with a shared run and properties. For pipelines that live entirely inside Glue, this avoids another service.

The limits show when pipelines grow: branching, retries across services and backfills are easier in a general orchestrator.

<!-- example -->

```text
workflow orders_daily
  scheduled trigger 05:00 ─► job extract_orders
  conditional trigger (extract SUCCEEDED AND ...) ─► job build_curated
  conditional trigger (build SUCCEEDED) ─► job publish_marts
```

#### What are Glue triggers?

Objects that start jobs and crawlers: scheduled (cron), conditional (when other jobs or crawlers reach a state such as `SUCCEEDED`), on-demand, or EventBridge-based events (for example batches of S3 events).

#### What is a Glue workflow?

A container for a graph of triggers, crawlers and jobs that represents an ETL pipeline, with a visual view of runs, shared run properties (key-value parameters) and the ability to resume from a failed step.

#### What is a conditional trigger's predicate?

The list of jobs or crawlers and states it watches, with logic `AND` (all conditions) or `ANY` (one condition), for example "start job B when job A succeeded and crawler C succeeded".

#### What are workflow run properties?

Key-value pairs shared by all jobs in a workflow run, read and updated with `get_workflow_run_properties` and `put_workflow_run_properties`, to pass values like a processing date between steps.

#### How do you resume a failed workflow?

In the Glue console or API (`ResumeWorkflowRun`), selecting the failed nodes to rerun after fixing the problem; completed nodes aren't rerun.

<!-- challenge -->

A workflow failed at its third job after the first two took two hours. How do you continue without rerunning them?

<!-- solution -->

Fix the cause, then resume the workflow run (`ResumeWorkflowRun`) selecting the failed node, so only it and its downstream nodes run with the same run properties.

<!-- takeaways -->

- Triggers start jobs on schedules, demand or conditions.
- Workflows group triggers and share run properties.
- Resume failed nodes instead of rerunning everything.

<!-- unit: External orchestrators and events -->

<!-- goals -->

- Run Glue jobs from Step Functions, Airflow and EventBridge.
- Pass processing dates from the orchestrator.

<!-- concept -->

Most production platforms orchestrate more than Glue: Lambda, EMR, Athena, dbt, notifications. A general orchestrator starts Glue jobs, waits for them and decides what's next, while the job only needs its arguments.

Event-driven starts complete the picture: a file landing in S3 can start a workflow or job through EventBridge, so pipelines react to data instead of a clock.

<!-- example -->

```json
{
  "Type": "Task",
  "Resource": "arn:aws:states:::glue:startJobRun.sync",
  "Parameters": {"JobName": "orders_daily",
                 "Arguments": {"--process_date.$": "$.process_date"}},
  "Retry": [{"ErrorEquals": ["Glue.ConcurrentRunsExceededException"], "MaxAttempts": 3}],
  "Next": "PublishMarts"
}
```

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

#### Can EventBridge start a Glue job directly?

EventBridge can target Glue workflows natively; for a single job, the common pattern is EventBridge to Step Functions or to a Lambda function that calls `StartJobRun`.

#### How do you pass the processing date from an orchestrator to a Glue job?

As a job argument in `StartJobRun` (`--process_date=2026-10-16`), computed by the orchestrator from the schedule's logical date, never from the job's own clock.

<!-- challenge -->

A pipeline needs Glue, then an Athena query, then a Lambda notification, with a different path on failure. Glue workflow or Step Functions?

<!-- solution -->

Step Functions: it calls Glue (`.sync`), Athena and Lambda natively, with retries and catch branches for the failure path. Glue workflows only orchestrate Glue jobs and crawlers.

<!-- takeaways -->

- Use a general orchestrator when pipelines span services.
- `.sync` integrations wait for Glue jobs to finish.
- Pass dates as job arguments from the orchestrator.

### Security and governance

<!-- unit: Job identity and network access -->

<!-- goals -->

- Give Glue jobs least-privilege roles and safe credentials.
- Reach private databases without exposing jobs to the internet.

<!-- concept -->

A Glue job acts with the permissions of its IAM role, so the role is the security boundary. It should reach only the buckets, keys and secrets the job needs. Database credentials belong in Secrets Manager, referenced by connections.

Network access is the second boundary. Jobs that read private databases run inside your VPC through a connection, and without a NAT gateway they can't reach the internet at all, with endpoints for the AWS services they use.

<!-- example -->

```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": ["arn:aws:s3:::lake/raw/orders/*", "arn:aws:s3:::lake/curated/orders/*"]
}
```

#### What IAM permissions does a Glue job need?

A job runs with an IAM role that Glue assumes. It needs the `AWSGlueServiceRole` permissions (or equivalent), access to the S3 paths it reads and writes, the script location, the temporary directory, KMS keys, Secrets Manager secrets for connections and CloudWatch Logs.

#### How do you restrict a Glue job to specific S3 prefixes?

Give its IAM role a policy allowing only the needed bucket prefixes and KMS keys, and with Lake Formation, grant only the needed tables; avoid broad `s3:*` permissions.

#### How do you avoid hard-coding credentials in Glue scripts?

Store credentials in AWS Secrets Manager and reference the secret in the Glue connection, or read it in the script with boto3; use IAM roles for AWS resources.

#### How do Glue jobs access databases in a VPC?

Through a Glue connection with VPC, subnet and security group settings: Glue creates elastic network interfaces in the subnet. The subnet needs routes to the database and, for S3 access, an S3 gateway endpoint (or NAT for internet).

#### How do you prevent Glue jobs from reaching the internet?

Run them with a VPC connection in private subnets without a NAT gateway, use VPC endpoints for S3, Glue, CloudWatch, KMS and Secrets Manager, and host Python dependencies in S3 or a private repository.

<!-- challenge -->

A Glue job fails to connect to an RDS database in a private subnet with a timeout. What do you check?

<!-- solution -->

That the job uses a Glue connection with the right VPC, subnet and security group; that the security group allows itself (self-referencing) and the database allows it on the port; and that the subnet has endpoints or NAT for S3 and Secrets Manager.

<!-- takeaways -->

- The job role is the security boundary; keep it narrow.
- Keep credentials in Secrets Manager.
- VPC connections reach private databases; no NAT means no internet.

<!-- unit: Lake Formation and fine-grained access -->

<!-- goals -->

- Explain how Lake Formation governs Glue catalog tables.
- Use LF-Tags and fine-grained access in Spark jobs.

<!-- concept -->

IAM policies on S3 control files, not tables. Lake Formation adds table, column, row and cell permissions on catalog objects, and hands engines temporary credentials for exactly what's allowed. LF-Tags make this scale: classify tables and columns once, and grant by tag.

With recent Glue versions, Spark jobs enforce the same fine-grained permissions, so governance doesn't stop at SQL engines.

<!-- example -->

```text
LF-Tag classification=pii on columns customers.email, customers.phone
Grant  analysts: SELECT on tables tagged domain=sales, excluding classification=pii
Grant  etl-role: SELECT, INSERT on domain=sales (all columns)
```

#### How does Lake Formation work with Glue?

Lake Formation adds fine-grained permissions (database, table, column, row and cell level, and tag-based access control with LF-Tags) on top of the Data Catalog. Services such as Athena, Redshift Spectrum, EMR and Glue (5.0+) enforce these permissions when reading data.

#### What are LF-Tags?

Lake Formation tags (key-value pairs such as `domain=sales`, `classification=pii`) attached to databases, tables and columns; permissions are granted on tag expressions, which scales better than granting table by table.

#### What is fine-grained access control for Glue Spark jobs?

With Glue 5.0 and Lake Formation, Spark jobs can enforce table, column, row and cell-level permissions defined in Lake Formation, so the job's role sees only the data it's allowed to.

<!-- challenge -->

A new table with customer emails is added every month, and each time someone forgets to restrict the email column. How do you make it automatic?

<!-- solution -->

Use LF-Tags: grant analysts by `domain` tag excluding `classification=pii`, and tag new tables and PII columns at creation (in the table-as-code template). New tables then inherit the right access.

<!-- takeaways -->

- Lake Formation governs tables, columns, rows and cells.
- LF-Tags grant by classification at scale.
- Recent Glue Spark jobs enforce fine-grained permissions.

<!-- unit: Encryption and audit -->

<!-- goals -->

- Encrypt job output, logs and bookmarks with security configurations.
- Audit Glue and catalog activity.

<!-- concept -->

Glue writes in several places besides your output: logs, bookmarks, temporary files. A security configuration encrypts all of them consistently with your KMS keys, so encryption doesn't depend on each developer remembering.

Audit answers "who changed or read what": CloudTrail records API calls on jobs and the catalog, and Lake Formation logs data access.

<!-- example -->

```python
glue.create_security_configuration(Name="lake-kms", EncryptionConfiguration={
    "S3Encryption": [{"S3EncryptionMode": "SSE-KMS", "KmsKeyArn": KEY}],
    "CloudWatchEncryption": {"CloudWatchEncryptionMode": "SSE-KMS", "KmsKeyArn": KEY},
    "JobBookmarksEncryption": {"JobBookmarksEncryptionMode": "CSE-KMS", "KmsKeyArn": KEY}})
```

#### How do you encrypt data with Glue?

With security configurations that enable encryption for S3 output (SSE-S3 or SSE-KMS), CloudWatch Logs and job bookmarks; catalog encryption with KMS; and connection passwords stored in Secrets Manager or encrypted in the catalog.

#### What is a Glue security configuration?

A named set of encryption settings (S3 encryption mode and KMS key, CloudWatch Logs encryption, job bookmark encryption) attached to jobs, crawlers and development endpoints.

#### How do you audit Glue activity?

CloudTrail logs Glue API calls (job and catalog changes), CloudWatch Logs holds job output, Lake Formation provides data access audit trails, and AWS Config can track resource configuration.

<!-- challenge -->

An auditor asks who changed the schema of the `payments` table last month. Where do you look?

<!-- solution -->

CloudTrail events for `UpdateTable` on that table (user or role and time), and the catalog's table versions to see what changed. If it was a crawler, its logs show the run.

<!-- takeaways -->

- Security configurations encrypt output, logs and bookmarks.
- CloudTrail records job and catalog changes.
- Table versions show how a schema changed.

### Operations, CI/CD and integration

<!-- unit: Jobs as code -->

<!-- goals -->

- Structure, test, version and deploy Glue jobs as code.
- Run one job across dev, staging and prod.

<!-- concept -->

A Glue job is a script plus a definition: role, workers, arguments. Treating both as code makes environments reproducible: the same script runs everywhere with different parameters, and infrastructure tools create the jobs.

Testing follows the usual pattern: logic in functions that take and return DataFrames, tested locally with pytest, while the job script only wires inputs and outputs. Versioned script paths make rollbacks trivial.

<!-- example -->

```text
repo/
  jobs/orders_daily.py          # thin entry script
  src/etl_lib/transforms.py     # logic, built as a wheel
  tests/test_transforms.py
  infra/glue_jobs.tf            # job definitions per environment
```

#### How do you deploy Glue jobs as code?

Store scripts and job definitions in Git, deploy with CloudFormation, CDK, Terraform or SAM: upload scripts to S3 and create jobs, triggers, crawlers, connections and catalog tables. A CI pipeline runs tests, packages libraries as wheels and deploys to each environment.

#### How do you structure a Glue project repository?

Separate job entry scripts, a shared Python package with transformation logic (built as a wheel), tests, infrastructure as code (CDK, Terraform or CloudFormation), data quality rulesets and configuration per environment.

#### How do you version Glue scripts?

Keep them in Git and deploy versioned copies to S3 (for example with the commit SHA in the path), so each job definition points to a known script version and rollback means pointing back.

#### How do you test Glue job logic?

Put transformation logic in functions that take and return DataFrames, test them with pytest on a local SparkSession or the Glue Docker image, test the job end to end on sample data in a dev account, and add data quality rules for runtime checks.

#### How do you upgrade a Glue job to a newer version?

Change the Glue version in a dev copy, run tests and compare outputs and durations, review migration notes (Spark, Python and library changes), check connectors and JARs, then promote through CI.

#### How do you run the same Glue job for dev, staging and prod?

One script with parameters for paths, databases and connections, deployed by infrastructure as code per environment (separate accounts ideally), with environment-specific job arguments and IAM roles, promoted through CI after tests.

<!-- challenge -->

A developer edited a production job's script in the console to fix a bug. A week later, a deploy overwrote the fix. How do you prevent this?

<!-- solution -->

Make Git and CI the only path to production: deploy scripts and definitions with infrastructure as code, remove console edit rights in prod, and add the fix to the repository with a test.

<!-- takeaways -->

- Scripts and job definitions both belong in Git.
- One parameterized script serves every environment.
- Test logic as plain DataFrame functions.

<!-- unit: Monitoring and failures -->

<!-- goals -->

- Monitor job health and duration in production.
- Handle failures with retries, alerts and reruns.

<!-- concept -->

In production, the important signals are simple: did the job fail, did it time out, did it run much longer than usual? Job state events flow to EventBridge, and metrics to CloudWatch, which together cover alerting and dashboards.

Handling failures depends on idempotency. When a job can rerun safely, retries and reruns are routine; when it can't, every failure becomes manual cleanup.

<!-- example -->

```json
{
  "source": ["aws.glue"],
  "detail-type": ["Glue Job State Change"],
  "detail": {"state": ["FAILED", "TIMEOUT", "ERROR"]}
}
```

#### How do you monitor Glue jobs in production?

CloudWatch metrics and alarms (job failures, duration, DPU usage), EventBridge events for job state changes routed to SNS or Slack, job run insights for errors, and dashboards of job durations and costs over time.

#### How do you handle job failures?

Retries for transient errors (only with idempotent jobs), alerts on `FAILED` and `TIMEOUT` states, a rerun procedure using parameters for the failed period, and dead-letter or quarantine paths for bad data.

#### How do you alert on long-running Glue jobs?

Set the job timeout, add a CloudWatch alarm on elapsed time or on the `glue.driver.aggregate.elapsedTime` metric, or have the orchestrator alert when a step exceeds its expected duration.

<!-- challenge -->

A job that usually runs 20 minutes ran for 9 hours before someone noticed. What two controls were missing?

<!-- solution -->

A realistic job timeout (for example 60 minutes) so it fails instead of running on, and an alarm on elapsed time or an EventBridge rule on `TIMEOUT` that pages the owner.

<!-- takeaways -->

- EventBridge state events drive failure alerts.
- Set timeouts and alarm on unusual duration.
- Idempotent jobs make retries and reruns safe.

<!-- unit: Glue in the AWS ecosystem -->

<!-- goals -->

- Connect Glue with Athena, DMS, Redshift and EMR.
- Know when zero-ETL, SaaS connectors or Amazon Q help.

<!-- concept -->

Glue rarely works alone. DMS brings database changes into S3, Glue applies them to lake tables, Athena and Redshift query the result, and EMR reads the same catalog. Managed integrations increasingly remove whole steps: zero-ETL replicates sources without jobs, and SaaS connectors pull from business applications.

Knowing these connections is often the answer to "should we build a job for this?"

<!-- example -->

```sql
-- Redshift reading Glue catalog tables directly
CREATE EXTERNAL SCHEMA lake FROM DATA CATALOG
DATABASE 'curated' IAM_ROLE 'arn:aws:iam::123456789012:role/redshift-spectrum';
SELECT count(*) FROM lake.orders WHERE dt = '2026-10-17';
```

#### How do Glue and Athena work together?

Glue catalogs and transforms data; Athena queries the catalog tables with SQL. Glue jobs often convert raw data to partitioned Parquet or Iceberg so Athena queries are fast and cheap.

#### How do Glue and AWS DMS work together?

DMS replicates databases (full load and CDC) into S3 as files with operation flags; Glue jobs then apply the changes to curated tables, typically with `MERGE` on Iceberg or Hudi tables.

#### How do you share Glue tables with Amazon Redshift?

Create an external schema in Redshift pointing to a Glue database (`CREATE EXTERNAL SCHEMA ... FROM DATA CATALOG`), then query the tables with Redshift Spectrum, or use Redshift's auto-mounted Data Catalog access.

#### How does EMR use the Glue Data Catalog?

EMR clusters and EMR Serverless can be configured to use the Glue Data Catalog as their Hive metastore, so Spark, Hive, Presto and Trino on EMR share the same table definitions as Athena and Glue.

#### What is zero-ETL in the Glue context?

Managed integrations that replicate data from sources (SaaS applications such as Salesforce, SAP or ServiceNow, and AWS databases such as DynamoDB) into targets like SageMaker Lakehouse tables or Redshift without building ETL pipelines, keeping them in sync.

#### What is AWS Glue for SAP or other SaaS connectors used for?

Extracting data from enterprise applications (SAP OData, Salesforce, ServiceNow, Zendesk and others) through managed connectors into Glue jobs or zero-ETL integrations, without writing API code.

#### What is Amazon Q data integration in Glue?

A generative AI assistant that creates Glue ETL jobs and transforms from natural-language descriptions and helps troubleshoot jobs; there is also AI-assisted upgrade of Spark scripts to newer Glue versions.

<!-- challenge -->

A team plans a custom Glue job to copy Salesforce objects into S3 nightly. What would you check first?

<!-- solution -->

Whether a managed path exists: the Glue Salesforce connector or a zero-ETL integration can replicate objects without custom extraction code, handling pagination, API limits and incremental changes.

<!-- takeaways -->

- DMS replicates; Glue applies; Athena and Redshift query.
- One catalog serves Athena, Redshift and EMR.
- Check zero-ETL and connectors before building jobs.

<!-- stage: Putting it together -->

### Scenarios

<!-- unit: Designing lake pipelines -->

<!-- goals -->

- Design batch and CDC pipelines on Glue end to end.
- Explain each design choice in an interview answer.

<!-- concept -->

Design questions test whether you can connect the sections: how data lands, how it's registered, how jobs process only what's new, how output is laid out for queries, how quality is checked and how it's orchestrated. Follow the data and name one choice per step, then say what happens on rerun. For CDC, add how changes are applied, which is where table formats like Iceberg earn their place.

<!-- example -->

```text
RDS ─► DMS (full load + CDC, Parquet with op column) ─► S3 raw
     ─► Glue job: dedupe per key, MERGE INTO Iceberg ─► curated.customers
     ─► Data Quality ruleset ─► Athena / Redshift
```

#### Design a pipeline that turns daily CSV drops in S3 into a queryable, partitioned dataset.

Land CSVs under a dated raw prefix, run a Glue Spark job (triggered by EventBridge or a schedule) that reads the day's files with a defined schema, cleans and casts types, writes Parquet or Iceberg partitioned by date to a curated prefix, updates the catalog, and runs data quality rules. Athena or Redshift Spectrum query the curated table; Lake Formation controls access.

#### How would you load CDC data from an RDS PostgreSQL database into a lakehouse with Glue?

Use DMS for full load plus CDC into S3 (Parquet with an operation column), or a zero-ETL integration where available. A Glue job reads new change files (bookmarks or date partitions), deduplicates per key keeping the latest change, and runs `MERGE INTO` on an Iceberg table registered in the Data Catalog. Compaction and snapshot expiry keep it healthy.

<!-- challenge -->

In the CDC design, DMS sometimes delivers the same change twice. How does your pipeline stay correct?

<!-- solution -->

Deduplicate each batch on primary key plus change sequence (or timestamp), keep the latest change per key, and apply it with `MERGE` so repeating an already-applied change doesn't alter the table.

<!-- takeaways -->

- Follow the data: land, register, process, lay out, check, orchestrate.
- Make each step idempotent.
- CDC needs ordered, deduplicated changes and `MERGE`.

<!-- unit: Migrating legacy ETL -->

<!-- goals -->

- Plan a migration from SSIS or Informatica to Glue.
- Validate migrated jobs before switching consumers.

<!-- concept -->

Legacy ETL tools hide a lot of logic in visual mappings, lookups and scheduler dependencies. A migration succeeds when that logic is made explicit: inventory jobs and dependencies, rebuild sources as connections, rewrite transformations in Spark with tests, and replace the scheduler. Running old and new in parallel and comparing outputs is what earns the trust to switch.

<!-- example -->

| Legacy | Glue equivalent |
|---|---|
| Connection manager | Glue connection + Secrets Manager |
| Data flow with lookups | Spark job with joins |
| SQL Agent / Informatica scheduler | Step Functions, Airflow or Glue workflows |
| Package variables | Job arguments |

#### How would you migrate on-premises SSIS or Informatica jobs to Glue?

Inventory jobs and their dependencies, rebuild sources as Glue connections, rewrite transformations as PySpark (or visual jobs), store reference data in S3 or the catalog, orchestrate with Step Functions or Airflow, and validate outputs side by side before switching.

<!-- challenge -->

Parallel runs show the new job produces 0.5% fewer rows than the SSIS package. How do you find out why?

<!-- solution -->

Diff the outputs by key to find the missing rows, then trace them back: typical causes are inner instead of left joins on lookups, case or whitespace differences in keys, `NULL` handling and different date filters.

<!-- takeaways -->

- Make hidden legacy logic explicit and tested.
- Replace schedulers and connections deliberately.
- Run in parallel and compare outputs before cutover.
