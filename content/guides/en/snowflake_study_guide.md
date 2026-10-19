## Snowflake Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Snowflake study guide: about 200 questions](../../images/snowflake_study_guide_title_img.png)

About 200 interview-style questions on Snowflake, from its architecture to virtual warehouses, micro-partitions, loading, semi-structured data, streams and tasks, dynamic tables, security, data sharing, performance and cost control. The answers reflect the platform as of 2026.

The guide follows a learning path in six stages. Each section is split into short units: learning goals, a concept explanation and a worked example, then questions (recall first, then application), a practical challenge and key takeaways. To **learn**, read each unit top to bottom. To **review**, switch to review mode or use "Skip to questions", mark answers you want to see again, and try a mixed review across sections.

<!-- QA -->
<!-- stage: Foundations -->

### Architecture

<!-- unit: Snowflake's three layers -->

<!-- goals -->

- Describe Snowflake's storage, compute and cloud services layers.
- Explain the separation of storage and compute and how it differs from classic MPP.

<!-- concept -->

Classic warehouses tie data to the machines that process it, so every workload competes for the same cluster and scaling means moving data. Snowflake splits the problem in three. Data lives once in central cloud storage. Independent compute clusters, called virtual warehouses, read it without interfering with each other. A services layer handles everything around queries: security, metadata, optimization and transactions.

The result is a warehouse you don't tune physically: you size compute per workload and pay only while it runs.

<!-- example -->

```text
cloud services: auth · metadata · optimizer · transactions
      │
compute:   WH_LOAD (M)    WH_TRANSFORM (L)    WH_BI (S, multi-cluster)
      │            │                │                 │
storage:   one copy of the data in micro-partitions on S3 / Azure Blob / GCS
```

#### What is Snowflake?

A cloud data platform delivered as a fully managed service on AWS, Azure and Google Cloud. It started as a SQL data warehouse and now also covers data lakes (Iceberg tables), data engineering, data sharing, applications and AI. There is no hardware or software to install, tune or patch.

#### What are the three layers of Snowflake's architecture?

Database storage (data stored in compressed, columnar micro-partitions in cloud object storage), query processing (virtual warehouses: independent compute clusters), and cloud services (authentication, metadata, query optimization, access control, transactions and infrastructure management).

#### What does "separation of storage and compute" mean in Snowflake?

Data is stored once in central storage, and any number of virtual warehouses can read it independently. You scale and pay for compute and storage separately, and workloads (loading, BI, data science) don't compete for the same resources.

#### Why is Snowflake called a hybrid of shared-disk and shared-nothing?

Like shared-disk, all compute nodes see one central copy of the data. Like shared-nothing (MPP), each warehouse processes its part of the data on its own nodes with local caching, which gives scalable performance.

#### What does the cloud services layer do?

It coordinates everything: authentication and access control, the metadata store (tables, micro-partition statistics, history), query parsing and optimization, transaction management, result caching and security. It is billed only if its usage exceeds 10% of the daily warehouse compute.

#### What is the difference between Snowflake and a traditional MPP warehouse such as Teradata or Redshift (provisioned)?

Traditional MPP warehouses couple storage and compute on the same nodes, so scaling means redistributing data, and all workloads share one cluster. Snowflake keeps storage central and lets you start independent warehouses in seconds, with no indexes, distribution keys or vacuuming to manage.

#### How do you explain Snowflake's value to a business stakeholder?

One governed place for the company's data that scales instantly for any number of users, costs nothing when idle, and lets teams share and analyze the same numbers without managing servers.

<!-- challenge -->

Nightly loads slow down morning dashboards on the company's current warehouse. How would Snowflake's architecture address it?

<!-- solution -->

Give loading and BI separate virtual warehouses: both read and write the same storage, but use independent compute, so loads no longer compete with dashboard queries.

<!-- takeaways -->

- Storage, compute and services are separate layers.
- Many warehouses share one copy of the data.
- Compute is sized per workload and billed while running.

<!-- unit: Accounts and objects -->

<!-- goals -->

- Navigate organizations, accounts, databases, schemas and editions.
- Use account identifiers, regions and session contexts.

<!-- concept -->

Everything in Snowflake sits in a hierarchy: an organization holds accounts, each account lives in one cloud region and holds databases, which hold schemas, which hold tables, views, stages and other objects. Warehouses, users and roles live at account level.

Editions decide which features an account gets, and a session always runs in a context: the current role, warehouse, database and schema, which explains most "object does not exist" surprises.

<!-- example -->

```sql
USE ROLE transformer;
USE WAREHOUSE wh_transform;
USE SCHEMA analytics.marts;
SELECT CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_ROLE(), CURRENT_WAREHOUSE();
```

#### What is a Snowflake account and an organization?

An account is one Snowflake deployment in one cloud region, with its own users, databases and warehouses, reached through a URL. An organization groups several accounts of the same customer for billing, replication and account management (by ORGADMIN).

#### What is the object hierarchy in Snowflake?

Organization → account → database → schema → objects (tables, views, stages, file formats, sequences, streams, tasks, pipes, functions, procedures). Warehouses, users, roles, resource monitors and integrations are account-level objects.

#### What editions does Snowflake offer?

Standard; Enterprise (adds multi-cluster warehouses, Time Travel up to 90 days, materialized views, masking and row access policies, search optimization); Business Critical (adds stronger security and compliance such as HIPAA and PCI support, Tri-Secret Secure, private connectivity, failover); and Virtual Private Snowflake (a fully isolated environment).

#### Which cloud providers and regions can you use?

AWS, Azure and Google Cloud, in many regions. An account lives in one region of one cloud; replication and data sharing across regions and clouds connect accounts.

#### What is the role of the account URL and locator?

The account identifier (organization name plus account name, or the legacy locator with region) forms the URL that clients connect to, for example `myorg-myaccount.snowflakecomputing.com`.

#### What are contexts in a Snowflake session?

The current role, warehouse, database and schema of a session (`USE ROLE`, `USE WAREHOUSE`, `USE DATABASE`, `USE SCHEMA`). Queries run with the current role's privileges on the current warehouse, and unqualified names resolve against the current database and schema.

<!-- challenge -->

A query fails with "Object does not exist or not authorized", though a colleague sees the table. What do you check first?

<!-- solution -->

The session context and role: the current role may lack privileges, or the database/schema context differs. Check `CURRENT_ROLE()`, use the fully qualified name, and verify grants.

<!-- takeaways -->

- Organization → account → database → schema → objects.
- Each account lives in one cloud region.
- Role, warehouse, database and schema form the session context.

<!-- unit: Credits and warehouses -->

<!-- goals -->

- Explain virtual warehouses and credits.
- Relate warehouse sizes to credit consumption.

<!-- concept -->

A virtual warehouse is compute you turn on and off. While it runs, it consumes credits, billed per second after a first minute. Each size step doubles both power and credit rate, so the hourly price of a large warehouse is high, but a query that parallelizes well finishes in half the time and costs about the same.

That makes sizing a speed decision more than a cost decision, as long as warehouses suspend when idle.

<!-- example -->

| Size | Credits/hour | Query that parallelizes well |
|---|---|---|
| X-Small | 1 | 16 min → 0.27 credits |
| Small | 2 | 8 min → 0.27 credits |
| Medium | 4 | 4 min → 0.27 credits |
| Large | 8 | 2 min → 0.27 credits |

#### What is a virtual warehouse?

A named cluster of compute resources that executes queries and DML and loads data. It has a size, can be suspended and resumed, and consumes credits only while running.

#### What is a credit?

The unit for billing compute. A warehouse consumes credits per second (with a 60-second minimum each time it resumes) according to its size. Serverless features (Snowpipe, automatic clustering, search optimization, serverless tasks) also consume credits. Storage is billed separately per TB per month.

#### How do warehouse sizes relate to credits?

Each size step doubles the compute and the credit rate: X-Small uses 1 credit per hour, Small 2, Medium 4, Large 8, and so on up to 6X-Large. A query that parallelizes well runs about twice as fast on the next size, so the cost can stay similar while latency drops.

<!-- challenge -->

A transformation takes 40 minutes on a Small warehouse. The team fears a Large would quadruple cost. What do you explain?

<!-- solution -->

If the query parallelizes, a Large (4× the rate) finishes in roughly a quarter of the time, so credits stay similar while results arrive faster. Test it and compare credits in query history.

<!-- takeaways -->

- Warehouses consume credits per second while running.
- Each size doubles power and price.
- Bigger can be faster at similar cost.

<!-- unit: Tools and governance -->

<!-- goals -->

- Connect to Snowflake with Snowsight, CLI and drivers.
- Describe Snowflake Horizon's governance features.

<!-- concept -->

Snowflake is used through many doors: the Snowsight web interface for worksheets, notebooks and dashboards; command-line tools for scripts and deployments; drivers and connectors for applications, BI tools and pipelines.

Governance is built into the platform under the Horizon name: access control, classification, policies, lineage and auditing, so security and discovery don't depend on a separate tool.

<!-- example -->

```bash
snow connection test --connection prod
snow sql -q "SELECT count(*) FROM analytics.marts.fct_orders" --connection prod
```
```python
import snowflake.connector
conn = snowflake.connector.connect(account="myorg-prod", user="etl_svc",
                                   authenticator="SNOWFLAKE_JWT", private_key_file="rsa_key.p8")
```

#### How do you connect to Snowflake?

Through Snowsight (the web UI), the Snowflake CLI and SnowSQL, drivers (JDBC, ODBC, Python connector, Go, Node.js, .NET, Spark and Kafka connectors), the SQL REST API, and partner tools (BI, ETL, dbt).

#### What is Snowsight?

Snowflake's web interface for writing SQL and Python worksheets, notebooks, dashboards, exploring data, monitoring queries and costs, and administering the account.

#### What is Snowflake Horizon?

Snowflake's built-in governance and catalog capabilities: access control, classification of sensitive data, masking and row access policies, tags, lineage, data quality monitoring, auditing and discovery, applied across tables, Iceberg tables and shared data.

<!-- challenge -->

A pipeline connects with a username and password stored in a config file. Which authentication method should a service user use instead?

<!-- solution -->

Key-pair authentication (or OAuth/workload identity), with the private key in a secrets manager, so no password is stored or subject to MFA prompts for automation.

<!-- takeaways -->

- Snowsight, CLI and drivers cover all access paths.
- Service users should use key pairs or OAuth.
- Horizon builds governance into the platform.

### Storage and micro-partitions

<!-- unit: Micro-partitions and pruning -->

<!-- goals -->

- Explain micro-partitions, their metadata and compression.
- Describe pruning and what updates do to immutable storage.

<!-- concept -->

Snowflake stores tables as many small immutable files, micro-partitions, each holding a slice of rows stored by column and compressed automatically. For every one, it records metadata such as the minimum and maximum value of each column.

That metadata is how queries get fast without indexes: a filter on a column lets Snowflake skip every micro-partition whose range can't match. Because files never change, updates and deletes write new micro-partitions, which also makes Time Travel and cloning cheap.

<!-- example -->

```text
orders: 12,000 micro-partitions
WHERE order_date = '2026-10-17'
  micro-partition 0001: order_date 2024-01-01..2024-01-03 → skip
  ...
  micro-partition 11,880: order_date 2026-10-16..2026-10-17 → scan
Query Profile: partitions scanned 14 of 12,000
```

#### What is a micro-partition?

The physical storage unit of a Snowflake table: an immutable file of 50 to 500 MB of uncompressed data (much smaller compressed), stored in columnar format. Snowflake creates them automatically as data is loaded, in the order it arrives.

#### What metadata does Snowflake keep per micro-partition?

The range of values (min and max) of each column, the number of distinct values, null counts and other statistics. The optimizer uses them to skip micro-partitions that can't contain matching rows.

#### What is pruning?

Skipping micro-partitions during a scan because their metadata shows they can't match the filter. Good pruning is the main reason queries on huge tables can be fast. It appears in the query profile as "partitions scanned" versus "partitions total".

#### Why are micro-partitions immutable, and what does an update do?

Immutability makes concurrency, Time Travel and cloning simple. An `UPDATE` or `DELETE` writes new micro-partitions containing the changed rows and marks the old ones as no longer current; the old ones are kept for Time Travel and Fail-safe.

#### How is data compressed in Snowflake?

Automatically, per column, with the best encoding for the data. You don't choose compression; storage is billed on the compressed size.

<!-- challenge -->

A query on a 2 TB table filters on `order_date` and scans 14 of 12,000 partitions. Another filters on `customer_id` and scans 11,500. Why the difference?

<!-- solution -->

Data was loaded in date order, so each micro-partition covers a narrow date range and prunes well; customer IDs are spread across all partitions, so their min/max ranges overlap and almost nothing is skipped.

<!-- takeaways -->

- Tables are immutable, compressed micro-partitions.
- Min/max metadata enables pruning.
- Updates write new micro-partitions.

<!-- unit: Clustering -->

<!-- goals -->

- Explain natural clustering and clustering keys.
- Decide when to cluster, check clustering and control its cost.

<!-- concept -->

Pruning only works when similar values sit together in the same micro-partitions. Data loaded in time order is naturally clustered by date at no cost. For other filter columns on very large tables, a clustering key tells Snowflake to reorganize data in the background, which costs credits as long as the table keeps changing.

So clustering is a trade-off: worth it on multi-terabyte tables with frequent selective filters, wasteful on small or rarely queried ones.

<!-- example -->

```sql
ALTER TABLE events CLUSTER BY (event_date, customer_id);
SELECT SYSTEM$CLUSTERING_INFORMATION('events', '(event_date, customer_id)');
-- average_depth falling toward 1–2 means good clustering
ALTER TABLE events SUSPEND RECLUSTER;   -- pause during a big backfill
```

#### What is data clustering in Snowflake?

How well rows with similar values of a column are co-located in the same micro-partitions. Data loaded in date order is naturally well clustered by date. Clustering degrades when DML scatters values over many partitions.

#### What is a clustering key?

One or more columns or expressions declared on a large table (`CLUSTER BY (event_date, customer_id)`) so that the Automatic Clustering service reorganizes micro-partitions in the background to keep similar values together, improving pruning for filters on those columns.

#### When should you define a clustering key?

On very large tables (multi-terabyte) where queries filter on columns that are not naturally clustered and the query profile shows poor pruning. Clustering costs credits for reclustering, so it isn't worth it for small or frequently fully rewritten tables.

#### How do you check how well a table is clustered?

With `SYSTEM$CLUSTERING_INFORMATION('table', '(col)')`, which reports the average depth and overlap of micro-partitions. Lower depth means better clustering.

#### What does `ALTER TABLE … SUSPEND RECLUSTER` do?

It pauses automatic clustering on a table, stopping reclustering costs, for example during a large backfill; `RESUME RECLUSTER` turns it back on.

#### What is the difference between a column's natural clustering and a clustering key?

Natural clustering comes from the order in which data was loaded and costs nothing; a clustering key asks Snowflake to maintain an order through background reclustering, which costs credits but keeps pruning good despite DML.

<!-- challenge -->

A team adds clustering keys to every table over 1 GB, and automatic clustering credits jump. What do you advise?

<!-- solution -->

Remove keys from small or rarely filtered tables (natural clustering and full scans are cheap there) and keep them only on very large tables with frequent selective filters, checking the benefit in query profiles.

<!-- takeaways -->

- Natural clustering from load order is free.
- Clustering keys reorganize data for a cost.
- Cluster only large, frequently filtered tables.

<!-- unit: Table types and storage cost -->

<!-- goals -->

- Choose among permanent, transient, temporary, Iceberg, hybrid and external tables.
- Understand how storage, Time Travel and Fail-safe are billed.

<!-- concept -->

Table types trade protection, location and workload fit. Permanent tables get Time Travel and Fail-safe; transient and temporary tables skip Fail-safe, which saves storage for data you can rebuild. Iceberg tables keep data in open format in your storage; hybrid tables serve fast row-level operations; external tables read files in place.

Storage is billed on compressed bytes, including history kept for Time Travel and Fail-safe, which can exceed the active data on tables that change constantly.

<!-- example -->

```sql
CREATE TRANSIENT TABLE staging.orders_raw (...) DATA_RETENTION_TIME_IN_DAYS = 0;
SELECT table_name, active_bytes, time_travel_bytes, failsafe_bytes
FROM snowflake.account_usage.table_storage_metrics
ORDER BY failsafe_bytes DESC LIMIT 10;
```

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

#### How can you see how much storage Time Travel and Fail-safe use?

In `ACCOUNT_USAGE.TABLE_STORAGE_METRICS`, which reports active bytes, Time Travel bytes, Fail-safe bytes and bytes retained for clones per table.

<!-- challenge -->

A staging table is fully reloaded every hour, and its Fail-safe storage is ten times its active size. What do you change?

<!-- solution -->

Make it a transient table with short (or zero) Time Travel: it's rebuildable, so it doesn't need Fail-safe, and hourly rewrites stop accumulating historical storage.

<!-- takeaways -->

- Permanent tables carry Time Travel and Fail-safe.
- Transient tables suit rebuildable data.
- Iceberg, hybrid and external tables fit special needs.

### Virtual warehouses and compute

<!-- unit: Warehouse lifecycle -->

<!-- goals -->

- Configure auto-suspend, auto-resume and statement timeouts.
- Choose an initial size and understand resizing.

<!-- concept -->

Warehouses cost money only while running, so their lifecycle settings matter more than their size. Auto-suspend stops one after a short idle period; auto-resume restarts it when a query arrives. Suspending also drops its local cache, so very short timeouts can slow repeated queries.

Sizing is an experiment: start small, measure representative queries and adjust. Resizing affects new queries; running ones finish where they started. Timeouts stop runaway queries before they burn credits.

<!-- example -->

```sql
CREATE WAREHOUSE wh_transform
  WAREHOUSE_SIZE = 'SMALL'
  AUTO_SUSPEND = 60          -- seconds
  AUTO_RESUME = TRUE
  STATEMENT_TIMEOUT_IN_SECONDS = 3600
  INITIALLY_SUSPENDED = TRUE;
```

#### What happens when a warehouse is suspended?

It stops consuming credits and its local cache is dropped. With auto-resume, the next query starts it again in a second or two.

#### What are auto-suspend and auto-resume?

Settings that suspend a warehouse after a number of seconds of inactivity and resume it automatically when a query arrives. A short auto-suspend (for example 60 seconds) saves credits on intermittent workloads; a longer one keeps the cache warm for BI.

#### Can a running query use a warehouse that was resized?

Resizing affects new queries; running queries finish on the existing resources. Scaling up provisions new resources in the background, so queued and new queries benefit once they're ready.

#### How do you choose an initial warehouse size?

Start small (X-Small or Small) for development and simple loads, test representative queries, and size up only when queries spill, run too long, or don't meet the target time. Measure cost per run, not just duration.

#### What is the statement timeout?

`STATEMENT_TIMEOUT_IN_SECONDS`, set on a warehouse, user or session, cancels queries running longer than the limit. Setting it prevents runaway queries from burning credits for hours.

<!-- challenge -->

A development warehouse runs 24/7 with auto-suspend disabled. What do you change, and what is the trade-off?

<!-- solution -->

Enable auto-suspend (for example 60–300 seconds) and auto-resume. The trade-off is a few seconds of resume time and a cold cache after idle periods, far cheaper than paying for idle hours.

<!-- takeaways -->

- Auto-suspend and auto-resume control idle cost.
- Start small, measure, resize.
- Timeouts stop runaway queries.

<!-- unit: Scaling and concurrency -->

<!-- goals -->

- Choose between scaling up and scaling out with multi-cluster warehouses.
- Reduce queuing and separate workloads.

<!-- concept -->

Two problems look alike but need different fixes. A single heavy query that's slow needs a bigger warehouse: more memory, less spilling. Many concurrent queries waiting in line need more clusters of the same size: a multi-cluster warehouse adds them as queues grow and removes them as load drops.

Separate warehouses per workload come first, though, so loads, transformations and dashboards don't compete at all.

<!-- example -->

```sql
ALTER WAREHOUSE wh_bi SET
  WAREHOUSE_SIZE = 'SMALL'
  MIN_CLUSTER_COUNT = 1
  MAX_CLUSTER_COUNT = 4
  SCALING_POLICY = 'STANDARD';   -- start clusters quickly to avoid queuing
```

#### What is a multi-cluster warehouse?

An Enterprise feature where a warehouse can run several clusters of the same size, between a minimum and maximum, to absorb concurrency. Extra clusters start when queries queue and stop when load drops.

#### What is the difference between scaling up and scaling out?

Scaling up (a bigger warehouse) makes individual complex queries faster and reduces spilling. Scaling out (more clusters in a multi-cluster warehouse) serves more concurrent users without queuing; it doesn't make a single query faster.

#### What are the multi-cluster scaling policies?

Standard (starts clusters quickly to avoid queuing, favoring performance) and Economy (starts a cluster only if there's enough load to keep it busy for several minutes, favoring cost).

#### What is query queuing, and how do you reduce it?

Queries wait when a warehouse is at its concurrency limit (`MAX_CONCURRENCY_LEVEL`, 8 by default). Fixes: multi-cluster warehouses, separate warehouses for different workloads, faster queries, or a larger warehouse.

#### What does `MAX_CONCURRENCY_LEVEL` control?

The number of concurrent SQL statements a warehouse cluster runs before queuing more. Lowering it gives each query more resources; raising it allows more parallel queries at the risk of slowing each one.

#### How do you separate workloads in Snowflake?

With different warehouses per workload (ingestion, transformation, BI, data science, ad hoc), each sized and suspended appropriately, so they never compete for compute and their costs are visible separately.

#### A dashboard warehouse queues every Monday at 9 a.m. What do you do?

Make it a multi-cluster warehouse with enough maximum clusters (Standard policy for interactive users), check whether the slow queries can be optimized or served from aggregates, and separate other workloads that hit the same warehouse at that time.

<!-- challenge -->

A BI warehouse shows heavy queuing at peak hours, and someone proposes going from Small to X-Large. Is that the best fix?

<!-- solution -->

Probably not: queuing comes from concurrency, so scale out with a multi-cluster warehouse (Standard policy) at the same size. Scale up only if individual queries are slow or spill.

<!-- takeaways -->

- Scale up for heavy queries; out for concurrency.
- Multi-cluster warehouses add clusters with load.
- Separate warehouses per workload.

<!-- unit: Specialized compute -->

<!-- goals -->

- Know Snowpark-optimized and Gen2 warehouses.
- Use the Query Acceleration Service for spiky large scans.

<!-- concept -->

Standard warehouses fit most SQL, but some workloads need different hardware. Snowpark-optimized warehouses offer much more memory per node for Python and ML work. Newer warehouse generations bring faster hardware and engine improvements, especially for DML-heavy pipelines.

The Query Acceleration Service takes another approach: instead of a bigger warehouse for occasional huge scans, it lends serverless compute to the parts of eligible queries that need it.

<!-- example -->

```sql
CREATE WAREHOUSE wh_ml WAREHOUSE_SIZE = 'MEDIUM' WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED';
ALTER WAREHOUSE wh_adhoc SET ENABLE_QUERY_ACCELERATION = TRUE
                            QUERY_ACCELERATION_MAX_SCALE_FACTOR = 8;
```

#### What is a Snowpark-optimized warehouse?

A warehouse with much more memory per node, for memory-heavy Snowpark workloads such as ML training or large UDF processing.

#### What is the Query Acceleration Service?

A serverless feature that offloads parts of large scans and filters in eligible queries to shared compute, so outlier queries finish faster without resizing the whole warehouse. It's enabled per warehouse with a scale factor limit.

#### What are Gen2 standard warehouses?

A newer generation of standard warehouses with faster hardware and engine improvements, especially for DML and large scans, billed at a somewhat higher credit rate. They can be chosen per warehouse.

<!-- challenge -->

An ad hoc warehouse is Small, but a few analysts' queries scan billions of rows and run for an hour. Resizing for everyone wastes credits. What can help?

<!-- solution -->

Enable the Query Acceleration Service on that warehouse: eligible large scans get extra serverless compute for their heavy parts while normal queries run as usual.

<!-- takeaways -->

- Snowpark-optimized warehouses add memory.
- Gen2 warehouses speed up many pipelines.
- Query acceleration helps occasional huge scans.

### Caching

<!-- unit: Snowflake's caches -->

<!-- goals -->

- Describe Snowflake's result, warehouse and metadata caches.
- Weigh the warehouse cache against auto-suspend.

<!-- concept -->

Three caches make repeated work cheap. The result cache returns identical query results for a day without using a warehouse at all. Each warehouse keeps recently read data on local disk, so repeated scans skip remote storage. The metadata cache answers questions like row counts instantly.

The warehouse cache lives only while the warehouse runs, so suspend timing is a trade-off between cost and warm data for dashboards.

<!-- example -->

| Cache | Where | Lifetime | Needs a warehouse? |
|---|---|---|---|
| Result | Cloud services | 24 h (renewed on reuse, max 31 days) | No |
| Warehouse (local disk) | Compute nodes | Until suspend | Yes |
| Metadata | Cloud services | Always | No (for `COUNT(*)`, min/max) |

#### What caches does Snowflake have?

The result cache (in the cloud services layer: query results reused for 24 hours if the query and data haven't changed), the warehouse (local disk) cache (micro-partition data cached on the warehouse's SSD while it runs), and the metadata cache (statistics that answer some queries like `COUNT(*)` or `MIN` without a warehouse).

#### How does the warehouse cache affect auto-suspend decisions?

Suspending drops the local cache, so the next queries read from remote storage and are slower. For dashboards that query the same data repeatedly, a longer auto-suspend can be faster and not much more expensive.

<!-- challenge -->

A BI warehouse with a 60-second auto-suspend makes the first dashboard of every session slow. What do you consider?

<!-- solution -->

A longer auto-suspend during business hours (for example 5–10 minutes) keeps the local cache warm between users; weigh the extra idle credits against the faster dashboards.

<!-- takeaways -->

- Result, warehouse and metadata caches avoid repeated work.
- The warehouse cache disappears on suspend.
- Tune suspend timing for cache-heavy BI.

<!-- unit: The result cache -->

<!-- goals -->

- Explain when the result cache is used and across which users.
- Disable it for benchmarks and diagnose misses.

<!-- concept -->

The result cache is the cheapest query: zero credits. It applies when the same query text runs again, the data hasn't changed and the role may read it, even for another user. Small differences break it: changed data, different text, non-deterministic functions or some session settings.

Benchmarks must turn it off, or they measure the cache instead of the query.

<!-- example -->

```sql
ALTER SESSION SET USE_CACHED_RESULT = FALSE;   -- benchmark the real query
SELECT region, SUM(amount) FROM sales.fct_orders WHERE order_date >= '2026-10-01' GROUP BY 1;
-- Query Profile shows "QUERY RESULT REUSE" when the cache was hit
```

#### When is the result cache used?

When the same query text runs again, the underlying data hasn't changed, the user has the required privileges, and the query doesn't use non-deterministic functions such as `CURRENT_TIMESTAMP()`. Each reuse extends retention, up to 31 days. It costs no compute.

#### How do you disable the result cache for testing?

`ALTER SESSION SET USE_CACHED_RESULT = FALSE;` so benchmark queries actually run.

#### Does the result cache work across users?

Yes, if the other user's role has the required privileges on the underlying objects and the query text is identical; results are not tied to the original user.

#### Why might a repeated query not hit the result cache?

The data changed, the query text differs (even by whitespace or case in some cases), it uses non-deterministic functions, it queries external functions or some table functions, the result is older than its retention, or caching is disabled for the session.

<!-- challenge -->

A dashboard query using `CURRENT_TIMESTAMP()` in its filter never hits the result cache. Why, and how can you fix it?

<!-- solution -->

Non-deterministic functions make each run different, so results can't be reused. Replace them with a fixed date parameter from the BI tool (for example the report date) so identical runs share results.

<!-- takeaways -->

- Identical query, unchanged data, allowed role: cache hit.
- Non-deterministic functions prevent reuse.
- Disable the cache when benchmarking.

<!-- stage: Getting data in -->

### Loading data

<!-- unit: Stages, integrations and file formats -->

<!-- goals -->

- Set up stages, storage integrations and file formats.
- Upload, inspect and infer schemas of staged files.

<!-- concept -->

Loading starts with where files sit. A stage points to files, either inside Snowflake or in your cloud storage; a storage integration lets Snowflake access that storage through a cloud role instead of keys; a file format says how to parse the files.

Before loading, you can query staged files directly and infer their schema, which makes checking new sources quick.

<!-- example -->

```sql
CREATE STORAGE INTEGRATION s3_lake TYPE = EXTERNAL_STAGE STORAGE_PROVIDER = 'S3'
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/snowflake-lake' ENABLED = TRUE
  STORAGE_ALLOWED_LOCATIONS = ('s3://lake/landing/');
CREATE FILE FORMAT ff_csv TYPE = CSV FIELD_DELIMITER = ';' SKIP_HEADER = 1 NULL_IF = ('', 'NULL');
CREATE STAGE landing URL = 's3://lake/landing/' STORAGE_INTEGRATION = s3_lake FILE_FORMAT = ff_csv;
SELECT $1, $2, METADATA$FILENAME FROM @landing/orders/ LIMIT 10;
```

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

#### What are `PUT` and `GET`?

Client commands (SnowSQL, CLI, drivers) to upload local files to an internal stage (`PUT`, which compresses and encrypts them) and download files from it (`GET`).

#### How do you query staged files without loading them?

`SELECT $1, $2, METADATA$FILENAME FROM @stage/path (FILE_FORMAT => 'my_csv')`, which is useful to inspect files before loading.

#### What is schema detection with `INFER_SCHEMA`?

A function that reads staged Parquet, Avro, ORC, JSON or CSV files and returns column names and types; combined with `CREATE TABLE … USING TEMPLATE`, it creates a table from files' structure. Tables can also enable schema evolution so new columns are added during loads.

<!-- challenge -->

A stage was created with AWS access keys embedded in its definition. What do you replace it with?

<!-- solution -->

A storage integration that uses an IAM role trusted by Snowflake, limited to the allowed locations, and recreate the stage on it; then delete the keys.

<!-- takeaways -->

- Stages point to files; file formats describe them.
- Storage integrations replace embedded keys.
- Query and infer staged files before loading.

<!-- unit: Bulk loading with COPY -->

<!-- goals -->

- Load files with COPY INTO, error handling and transformations.
- Size files correctly, understand load metadata and unload data.

<!-- concept -->

`COPY INTO` loads staged files into a table in parallel, one file per thread, so file size drives speed: many tiny files waste overhead and one huge file can't be split. Snowflake remembers which files it loaded for 64 days, so reruns skip them unless forced.

Errors need a policy: abort, skip rows or skip files. Simple transformations can happen during the load, and the same command in reverse unloads query results to files.

<!-- example -->

```sql
COPY INTO raw.orders (order_id, customer_id, amount, source_file)
FROM (SELECT $1::NUMBER, $2::NUMBER, $3::NUMBER(12,2), METADATA$FILENAME FROM @landing/orders/)
ON_ERROR = 'CONTINUE';
SELECT * FROM TABLE(VALIDATE(raw.orders, JOB_ID => '_last'));   -- rejected rows
COPY INTO @exports/orders/ FROM (SELECT * FROM marts.fct_orders) FILE_FORMAT = (TYPE = PARQUET);
```

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

#### What is the `FORCE` option of `COPY`?

`FORCE = TRUE` loads files again even if the load metadata says they were already loaded, which can create duplicates; it's used deliberately for reloads after truncating a table.

#### How does `COPY` handle files older than 64 days?

Load metadata expires after 64 days, so for older files Snowflake may not know whether they were loaded. `LOAD_UNCERTAIN_FILES = TRUE` loads them anyway; to avoid ambiguity, move or delete files once loaded, or use Snowpipe, which keeps 14 days of history per pipe.

#### How can you transform data during `COPY`?

With a `SELECT` over the staged files in the `COPY` statement: reorder or omit columns, cast types, use `$1`, `$2` positions or `$1:field` for semi-structured data, and add `METADATA$FILENAME` or `METADATA$FILE_ROW_NUMBER` for lineage.

#### How do you unload data from Snowflake?

With `COPY INTO @stage/path/ FROM (SELECT ...)`, writing CSV, JSON or Parquet files to an internal or external stage, with options for partitioning (`PARTITION BY`), file size and headers. Then `GET` downloads files from internal stages.

<!-- challenge -->

A daily `COPY` of one 40 GB gzip file takes an hour even on a Large warehouse. What do you change?

<!-- solution -->

Split the input into files of about 100–250 MB compressed (at the producer or with a pre-processing step), so `COPY` loads many files in parallel across the warehouse's threads.

<!-- takeaways -->

- `COPY` parallelizes by file; size files ~100–250 MB.
- Load metadata skips already-loaded files for 64 days.
- Choose an `ON_ERROR` policy deliberately.

<!-- unit: Continuous loading -->

<!-- goals -->

- Load files continuously with Snowpipe and rows with Snowpipe Streaming.
- Ingest CDC data and avoid duplicate loads.

<!-- concept -->

When data arrives all day, waiting for a nightly `COPY` adds latency. Snowpipe runs the same `COPY` serverlessly as each file lands, notified by cloud events; small files raise its per-file overhead. Snowpipe Streaming skips files entirely, writing rows from Kafka or SDKs with seconds of latency.

Database changes usually arrive through CDC tools into raw tables, then are applied with `MERGE`. Duplicates come from producers resending data, not from Snowpipe itself, so pipelines deduplicate downstream.

<!-- example -->

```sql
CREATE PIPE raw.orders_pipe AUTO_INGEST = TRUE AS
COPY INTO raw.orders FROM @landing/orders/ FILE_FORMAT = ff_csv;
SHOW PIPES;                                      -- notification_channel → configure S3 events to SQS
SELECT SYSTEM$PIPE_STATUS('raw.orders_pipe');
```

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

#### What is Openflow?

Snowflake's managed data integration service, based on Apache NiFi, with connectors for databases, SaaS apps and streams, deployed in Snowflake or in your own cloud (bring your own cloud), to ingest structured and unstructured data.

#### How do you load from a relational database with CDC into Snowflake?

With a CDC tool (Openflow connectors, Debezium with Kafka and the Snowflake Kafka connector, Fivetran, AWS DMS writing to S3 plus Snowpipe) landing change events in raw tables, then a `MERGE` from a stream or a dynamic table to apply them to the current-state table.

#### A Snowpipe loads duplicate rows sometimes. Why, and what do you do?

The same data arrived in different files (producer retries, renamed files), or files were reloaded with `FORCE`. Make producers write deterministic file names, deduplicate downstream on a business key with `QUALIFY`, and keep the raw layer append-only with file metadata for tracing.

<!-- challenge -->

A producer writes one tiny file per event, and Snowpipe costs grow faster than data volume. What do you change?

<!-- solution -->

Batch files at the producer (for example Firehose buffering to ~100 MB or a few minutes), or switch to Snowpipe Streaming for row-level ingestion, avoiding per-file overhead.

<!-- takeaways -->

- Snowpipe loads files as they land.
- Snowpipe Streaming writes rows with low latency.
- Deduplicate downstream; producers resend data.

### Semi-structured data

<!-- unit: VARIANT and path queries -->

<!-- goals -->

- Store JSON in VARIANT and query it with paths and casts.
- Handle mixed types and the difference between missing keys and JSON null.

<!-- concept -->

Semi-structured data lands as it is in `VARIANT` columns, which Snowflake stores in columnar form internally, so queries on common paths stay fast. You navigate with path notation and cast to SQL types as you read.

Two subtleties matter for correctness: a field that arrives sometimes as a number and sometimes as a string needs defensive casting, and a missing key is SQL `NULL` while a JSON `null` is a `VARIANT` null, which behaves differently in comparisons.

<!-- example -->

```sql
SELECT payload:order_id::NUMBER                 AS order_id,
       payload:customer.city::STRING            AS city,
       TRY_TO_NUMBER(payload:amount::STRING)    AS amount,     -- tolerate "12.50" or 12.5
       IS_NULL_VALUE(payload:coupon)            AS coupon_is_json_null
FROM raw.events_json;
```

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

#### What are `OBJECT` and `ARRAY` types?

Semi-structured types for key-value objects and arrays. Functions like `OBJECT_CONSTRUCT`, `ARRAY_AGG`, `ARRAY_CONTAINS` and `PARSE_JSON` build and inspect them. Structured versions (`OBJECT(name STRING, age NUMBER)`, `ARRAY(NUMBER)`) enforce element types.

#### How is a missing key different from a JSON null?

A missing key returns SQL `NULL`; a JSON `null` value is a `VARIANT` null, which is not the same as SQL `NULL` (`IS_NULL_VALUE()` tests it). Casting with `::STRING` turns JSON null into SQL `NULL`.

#### How do you handle a JSON field that sometimes is a string and sometimes a number?

Cast defensively with `TRY_CAST` or `TRY_TO_NUMBER`, which return `NULL` instead of failing, and check the type with `TYPEOF()` to quarantine unexpected values.

<!-- challenge -->

`WHERE payload:discount IS NULL` misses rows where the JSON has `"discount": null`. Why, and how do you include them?

<!-- solution -->

A JSON null is a `VARIANT` null, not SQL `NULL`. Cast first (`payload:discount::NUMBER IS NULL`) or test both with `IS_NULL_VALUE(payload:discount)`.

<!-- takeaways -->

- `VARIANT` stores JSON efficiently.
- Navigate with paths; cast as you read.
- Missing key ≠ JSON null.

<!-- unit: Flattening and modeling JSON -->

<!-- goals -->

- Expand arrays with FLATTEN and build JSON from rows.
- Decide what to keep in VARIANT and what to extract, and load Parquet by column name.

<!-- concept -->

Arrays inside JSON become rows with `FLATTEN`, one per element, joined back to their parent with a lateral join. The opposite direction, building JSON from rows, serves APIs and exports.

The modeling choice is about layers: keep raw JSON in `VARIANT` for flexibility and audit, and extract stable, frequently used fields into typed columns in curated tables, where types, constraints and pruning work best. Columnar files can load straight into matching columns.

<!-- example -->

```sql
SELECT o.payload:order_id::NUMBER AS order_id,
       i.value:sku::STRING        AS sku,
       i.value:qty::NUMBER        AS qty
FROM raw.orders_json o,
     LATERAL FLATTEN(input => o.payload:items) i;

COPY INTO raw.orders FROM @landing/orders_parquet/
FILE_FORMAT = (TYPE = PARQUET) MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
```

#### What does `FLATTEN` do?

A table function that expands an array or object into one row per element, used with `LATERAL` to unnest nested data.

```sql
SELECT e.payload:order_id::STRING AS order_id, i.value:sku::STRING AS sku
FROM raw.events e, LATERAL FLATTEN(input => e.payload:items) i;
```

#### Should you keep JSON as `VARIANT` or flatten it into columns?

Keep raw JSON in `VARIANT` in the landing layer for flexibility and auditability, then extract the fields that are queried often into typed columns in clean layers: typed columns are easier to use, document and govern, and they prune predictably.

#### How do you convert relational rows into JSON?

With `OBJECT_CONSTRUCT(*)` or `OBJECT_CONSTRUCT('id', id, 'name', name)` for each row, and `ARRAY_AGG` to group rows into arrays, useful for exporting nested documents or feeding APIs.

#### How do you load Parquet columns directly into table columns?

With `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE` in `COPY`, which maps file columns to table columns by name, or by selecting `$1:column_name::type` explicitly.

<!-- challenge -->

Every dashboard query extracts the same ten fields from a huge `VARIANT` column. What do you change?

<!-- solution -->

Extract those fields into typed columns in a curated table (or dynamic table) refreshed from raw, so queries read narrow typed columns with better pruning; keep the raw `VARIANT` for audit and new fields.

<!-- takeaways -->

- `FLATTEN` turns arrays into rows.
- Keep raw JSON; extract stable fields to columns.
- `MATCH_BY_COLUMN_NAME` loads columnar files by name.

<!-- stage: Transforming data -->

### SQL features

<!-- unit: Querying and changing data -->

<!-- goals -->

- Use QUALIFY, MERGE, PIVOT, SAMPLE and MATCH_RECOGNIZE.
- Write deduplication and upserts idiomatically.

<!-- concept -->

Snowflake SQL includes shortcuts for patterns analysts write daily. `QUALIFY` filters on window results without a subquery, the cleanest way to keep the latest row per key. `MERGE` applies inserts, updates and deletes from a source in one statement. Pivots rotate data for reports, sampling reads a fraction for exploration, and pattern matching finds sequences of events.

<!-- example -->

```sql
MERGE INTO silver.customers t
USING (
  SELECT * FROM raw.customer_changes
  QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1
) s
ON t.customer_id = s.customer_id
WHEN MATCHED AND s.op = 'D' THEN DELETE
WHEN MATCHED THEN UPDATE SET email = s.email, segment = s.segment, updated_at = s.updated_at
WHEN NOT MATCHED AND s.op <> 'D' THEN INSERT (customer_id, email, segment, updated_at)
  VALUES (s.customer_id, s.email, s.segment, s.updated_at);
```

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

#### What are `PIVOT` and `UNPIVOT` used for?

Rotating rows into columns (for example months into columns) and columns back into rows. `PIVOT` supports dynamic value lists with `ANY` in recent versions.

#### What is `SAMPLE` used for?

Reading a random fraction of a table (`SELECT * FROM t SAMPLE (1)` for 1% of rows, or `SAMPLE BLOCK` for micro-partitions), which is useful for quick exploration and testing on big tables.

#### What does `MATCH_RECOGNIZE` do?

Pattern matching over ordered rows (for example a sequence of events in a session, such as view → cart → purchase), returning matches with measures, without writing complex self-joins.

<!-- challenge -->

A `MERGE` fails with "Duplicate row detected during DML action". What is wrong with the source, and the fix?

<!-- solution -->

Several source rows match the same target row. Deduplicate the source first, keeping one row per key (for example with `QUALIFY ROW_NUMBER() ... = 1`).

<!-- takeaways -->

- `QUALIFY` filters window results.
- `MERGE` upserts and deletes in one statement.
- Deduplicate MERGE sources per key.

<!-- unit: Keys, sequences and transactions -->

<!-- goals -->

- Understand which constraints Snowflake enforces.
- Use sequences, identity columns and transactions correctly.

<!-- concept -->

Snowflake accepts primary, unique and foreign key declarations but enforces only `NOT NULL` on standard tables. The others document intent and help tools and the optimizer, so uniqueness has to be guaranteed by pipelines and tested.

Sequences and identity columns generate unique numbers, not gap-free ones. Statements autocommit unless wrapped in an explicit transaction, which runs at read committed isolation.

<!-- example -->

```sql
CREATE TABLE dim_customer (
  customer_key NUMBER IDENTITY(1,1),
  customer_id NUMBER NOT NULL,          -- enforced
  email STRING,
  PRIMARY KEY (customer_key)            -- declared, not enforced
);
SELECT customer_id, COUNT(*) FROM dim_customer GROUP BY 1 HAVING COUNT(*) > 1;   -- test it yourself
```

#### Does Snowflake enforce primary and foreign keys?

On standard tables, only `NOT NULL` is enforced. Primary, unique and foreign key constraints are informational: they document the model and can help BI tools and the optimizer (with `RELY`), but they don't prevent duplicates. Hybrid tables do enforce them.

#### What are sequences and identity columns?

Sequences generate unique numbers (`seq.NEXTVAL`), not necessarily gap-free. `AUTOINCREMENT`/`IDENTITY` columns use a sequence internally. Many warehouse designs prefer hash-based surrogate keys, which are deterministic across loads.

#### What are transactions like in Snowflake?

ACID with the read committed isolation level. Each statement autocommits unless inside an explicit `BEGIN … COMMIT`. DDL commits implicitly. Concurrent DML on the same table can be blocked by locks until the other transaction finishes.

<!-- challenge -->

A team relies on a declared primary key to prevent duplicates, and duplicates appear after a rerun. What went wrong, and what do you add?

<!-- solution -->

Primary keys aren't enforced on standard tables. Make loads idempotent (`MERGE` on the key or delete-insert per batch) and add a uniqueness test (dbt test or data metric function).

<!-- takeaways -->

- Only `NOT NULL` is enforced on standard tables.
- Sequences are unique, not gap-free.
- Guarantee and test uniqueness in pipelines.

<!-- unit: Procedural code -->

<!-- goals -->

- Write UDFs, stored procedures and Snowflake Scripting.
- Choose languages and use cases for each.

<!-- concept -->

When SQL alone isn't enough, Snowflake runs code next to the data. UDFs return values or tables and are called from queries; stored procedures run sequences of statements with control flow, for administration or multi-step logic. Both can be written in SQL, Python, Java, Scala or JavaScript.

Snowflake Scripting brings variables, loops and error handling to SQL itself, often enough for procedures without another language.

<!-- example -->

```sql
CREATE OR REPLACE PROCEDURE ops.drop_old_dev_schemas(days INT)
RETURNS STRING LANGUAGE SQL AS
$$
DECLARE c CURSOR FOR SELECT schema_name FROM dev.information_schema.schemata
                     WHERE created < DATEADD(day, -:days, CURRENT_TIMESTAMP());
        n INT DEFAULT 0;
BEGIN
  FOR r IN c DO
    EXECUTE IMMEDIATE 'DROP SCHEMA dev.' || r.schema_name; n := n + 1;
  END FOR;
  RETURN n || ' schemas dropped';
END;
$$;
```

#### What are user-defined functions in Snowflake?

Scalar or table functions written in SQL, JavaScript, Python, Java or Scala. Python UDFs run in a secure sandbox with packages from Anaconda or uploaded files. Vectorized Python UDFs process batches with pandas for better performance.

#### What are stored procedures in Snowflake?

Procedures written in Snowflake Scripting (SQL), JavaScript, Python, Java or Scala, used for procedural logic and administration. They run with owner's rights (default) or caller's rights.

#### What is Snowflake Scripting?

A procedural SQL extension with variables, `IF`, loops, cursors, exception handling and `RETURN`, usable in stored procedures and anonymous blocks.

<!-- challenge -->

A Python UDF is called on 2 billion rows to apply a simple tax rule and the query is slow. What do you suggest?

<!-- solution -->

Express the rule in SQL (`CASE` and arithmetic) so it runs natively, or use a vectorized Python UDF if Python is truly needed. Row-by-row Python adds serialization overhead.

<!-- takeaways -->

- UDFs return values; procedures run steps.
- Several languages are supported.
- Prefer SQL when it can express the logic.

<!-- unit: Managing objects -->

<!-- goals -->

- Recover dropped objects with UNDROP and publish atomically with SWAP.
- Keep definitions declarative with CREATE OR ALTER.

<!-- concept -->

A few commands make object management safer. `UNDROP` restores a recently dropped table, schema or database from Time Travel. `SWAP WITH` exchanges two tables atomically, so a rebuilt table can replace the old one without consumers ever seeing a half-loaded state.

`CREATE OR ALTER` brings declarative definitions: describe the object you want, and Snowflake creates or adjusts it without dropping data.

<!-- example -->

```sql
CREATE OR REPLACE TABLE marts.fct_revenue_new AS SELECT ...;
-- validate fct_revenue_new ...
ALTER TABLE marts.fct_revenue SWAP WITH marts.fct_revenue_new;   -- atomic publish
DROP TABLE marts.fct_revenue_new;
UNDROP TABLE marts.fct_revenue_old;                              -- if needed
```

#### What does `UNDROP` do?

It restores a recently dropped table, schema or database from Time Travel, as long as it is within the retention period.

#### What does `SWAP WITH` do?

`ALTER TABLE a SWAP WITH b` exchanges two tables' names atomically, a common way to publish a rebuilt table without downtime for readers.

#### What is `CREATE OR ALTER`?

A statement that creates an object if it doesn't exist or alters it to match the definition if it does, keeping data and grants, useful for declarative deployments of tables and other objects.

<!-- challenge -->

A nightly job rebuilds a large mart in place, and dashboards show empty or partial data for 20 minutes. How do you fix it?

<!-- solution -->

Build the new version into a separate table, validate it, then `ALTER TABLE ... SWAP WITH` to publish atomically; dashboards see either the old or the complete new table.

<!-- takeaways -->

- `UNDROP` restores dropped objects.
- `SWAP WITH` publishes rebuilt tables atomically.
- `CREATE OR ALTER` keeps definitions declarative.

### Streams, tasks and dynamic tables

<!-- unit: Streams -->

<!-- goals -->

- Track table changes with streams.
- Choose stream types and avoid stale streams.

<!-- concept -->

A stream is a bookmark on a table's change history. Querying it returns rows inserted, updated or deleted since it was last consumed, and consuming it in a DML statement moves the bookmark forward. That turns any table into a change feed for incremental processing.

Append-only streams are cheaper when only inserts matter. A stream that isn't consumed for longer than the table's retention becomes stale and must be recreated.

<!-- example -->

```sql
CREATE STREAM raw.orders_changes ON TABLE raw.orders;
INSERT INTO silver.orders_log
SELECT order_id, amount, METADATA$ACTION, METADATA$ISUPDATE, CURRENT_TIMESTAMP()
FROM raw.orders_changes;          -- consuming the stream advances its offset
```

#### What is a stream?

An object that records the changes (inserts, updates, deletes) made to a table, view or external table since the stream was last consumed, exposing them with the columns `METADATA$ACTION`, `METADATA$ISUPDATE` and `METADATA$ROW_ID`. Consuming it in a DML transaction advances its offset.

#### What types of streams exist?

Standard (all changes, net of each other), append-only (only inserts, cheaper, for tables with insert-only loads), and insert-only for external and Iceberg tables.

#### What happens to a stream if it isn't consumed for a long time?

It can become stale when its offset falls outside the source table's data retention period (Snowflake extends retention up to 14 days to prevent this for tables with streams). A stale stream must be recreated, and changes may need a full reload.

<!-- challenge -->

A stream on a staging table wasn't consumed during a two-week holiday, and now it reports as stale. Why, and how do you prevent it?

<!-- solution -->

Its offset fell outside the table's data retention, so changes can't be reconstructed. Recreate it and reload; consume streams regularly (a task with a schedule) or raise retention on tables streams depend on.

<!-- takeaways -->

- Streams return changes since last consumption.
- Consuming in DML advances the offset.
- Unconsumed streams go stale after retention.

<!-- unit: Tasks -->

<!-- goals -->

- Schedule SQL with tasks, serverless tasks and triggered tasks.
- Build and monitor task graphs with finalizers.

<!-- concept -->

Tasks run SQL or procedures on a schedule, after other tasks, or when a stream has new data. Chained into graphs, they form pipelines inside Snowflake without an external orchestrator. Serverless tasks let Snowflake size compute automatically.

Like any pipeline, task graphs need monitoring and cleanup: task history shows runs and failures, and a finalizer task runs at the end whatever happened, for notifications or cleanup.

<!-- example -->

```sql
CREATE TASK silver.apply_orders
  WAREHOUSE = wh_transform
  WHEN SYSTEM$STREAM_HAS_DATA('raw.orders_changes')
AS
  MERGE INTO silver.orders t USING raw.orders_changes s ON t.order_id = s.order_id
  WHEN MATCHED THEN UPDATE SET amount = s.amount
  WHEN NOT MATCHED THEN INSERT (order_id, amount) VALUES (s.order_id, s.amount);
ALTER TASK silver.apply_orders RESUME;
```

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

#### How do you monitor tasks?

With `TASK_HISTORY` (information schema table function and account usage view), the task graph view in Snowsight, error notifications through a notification integration, and `SYSTEM$TASK_DEPENDENTS_ENABLE` to resume whole graphs.

#### What is a finalizer task?

A task attached to the root of a task graph that runs after all other tasks finish, whether they succeeded or failed, for cleanup or notifications.

<!-- challenge -->

A task scheduled every minute checks a stream and usually finds nothing, yet the warehouse rarely suspends. What do you change?

<!-- solution -->

Make it a triggered task (no schedule, runs only when the stream has data) or keep the `WHEN SYSTEM$STREAM_HAS_DATA` condition, which skips runs without resuming the warehouse; consider serverless tasks.

<!-- takeaways -->

- Tasks run on schedules, after others or on new data.
- Serverless tasks size compute automatically.
- Monitor task history; finalizers clean up.

<!-- unit: Dynamic tables and materialized views -->

<!-- goals -->

- Build declarative pipelines with dynamic tables and target lag.
- Choose among dynamic tables, materialized views and streams with tasks.

<!-- concept -->

Dynamic tables turn pipelines into definitions: write the query and a freshness target, and Snowflake keeps the table up to date, incrementally when it can. Chained dynamic tables form a pipeline whose upstream steps refresh as often as downstream ones need.

Materialized views solve a narrower problem, speeding up queries on a single table, transparently. Streams and tasks remain the tool for full control, such as procedural logic or side effects.

<!-- example -->

```sql
CREATE DYNAMIC TABLE marts.daily_revenue
  TARGET_LAG = '15 minutes'
  WAREHOUSE = wh_transform
  REFRESH_MODE = INCREMENTAL
AS
SELECT order_date, region, SUM(amount) AS revenue
FROM silver.orders
GROUP BY order_date, region;
```

#### What is a dynamic table?

A table defined by a query and a target lag (`TARGET_LAG = '10 minutes'`), which Snowflake keeps refreshed automatically, incrementally when possible. It replaces many stream-and-task pipelines with declarative SQL.

```sql
CREATE DYNAMIC TABLE dw.daily_sales
  TARGET_LAG = '30 minutes'
  WAREHOUSE = transform_wh
AS
SELECT order_date, SUM(amount) AS sales FROM dw.orders GROUP BY order_date;
```

#### What is the difference between incremental and full refresh in dynamic tables?

Incremental refresh processes only changes in sources since the last refresh; full refresh recomputes the whole query. Snowflake chooses incremental when the query supports it; some constructs (certain non-deterministic functions, some window patterns) force full refreshes, which cost more.

#### Can dynamic tables be chained?

Yes. A dynamic table can read other dynamic tables, forming a pipeline; `TARGET_LAG = DOWNSTREAM` means a table refreshes only as needed by the tables that depend on it.

#### What is a materialized view in Snowflake?

A precomputed result of a query on one table, maintained automatically and transparently by a background service (Enterprise). The optimizer can use it even when you query the base table. Maintenance costs credits, so use it for expensive, frequent queries on slowly changing tables.

#### Dynamic tables, materialized views or streams and tasks: how do you choose?

Dynamic tables for declarative pipelines with joins and aggregations at a chosen freshness. Materialized views for speeding up repeated queries on a single table (no joins), always current. Streams and tasks for procedural logic, custom `MERGE` handling or side effects.

<!-- challenge -->

A dynamic table always does full refreshes and costs a lot. What do you check?

<!-- solution -->

Whether its query uses constructs that prevent incremental refresh (some non-deterministic functions, certain joins or window patterns); check the refresh mode reported, simplify the query, or split it into chained dynamic tables that can refresh incrementally.

<!-- takeaways -->

- Dynamic tables: query plus target lag.
- Incremental refresh processes only changes.
- Materialized views accelerate one table's queries.

### Snowpark, Python and AI

<!-- unit: Snowpark for code -->

<!-- goals -->

- Process data in Snowflake with Snowpark and pandas on Snowflake.
- Manage Python packages and use notebooks.

<!-- concept -->

Snowpark lets you write DataFrame code in Python, Java or Scala that compiles to SQL and runs in Snowflake, so data never leaves the platform. For logic that's awkward in SQL, such as complex business rules or feature engineering, it's often clearer.

pandas on Snowflake runs familiar pandas code at scale the same way. Packages come from a curated channel or your own uploads, and notebooks mix SQL and Python against the same data.

<!-- example -->

```python
from snowflake.snowpark import Session, functions as F
session = Session.builder.configs(conn_params).create()
orders = session.table("silver.orders")
features = (orders.group_by("customer_id")
                  .agg(F.count("order_id").alias("orders"), F.sum("amount").alias("spend")))
features.write.mode("overwrite").save_as_table("ml.customer_features")
```

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

#### When would you use Snowpark instead of SQL?

For logic that's easier in Python (complex string or business rules, ML feature engineering, reuse of Python libraries), for unit-testable transformation code, or for teams more comfortable with DataFrames. For straightforward transformations, SQL is often simpler and as fast.

#### What is the pandas on Snowflake API?

A pandas-compatible API (Snowpark pandas, through Modin) that runs pandas code on Snowflake compute, so familiar pandas syntax scales to large tables.

#### How do Python packages get into Snowflake?

From the Snowflake Anaconda channel (listed in `PACKAGES`), from wheels or zip files uploaded to a stage (`IMPORTS`), or through artifact repositories that pull from PyPI.

#### What are Snowflake Notebooks?

Notebooks in Snowsight that mix SQL, Python and Markdown cells and run on a warehouse or on container compute, for exploration, data engineering and ML.

<!-- challenge -->

A data scientist exports 200 GB from Snowflake to a laptop to compute features in pandas. What do you suggest?

<!-- solution -->

Run the same logic in Snowflake with Snowpark (or pandas on Snowflake), so computation happens next to the data on a warehouse, and write features back to a table.

<!-- takeaways -->

- Snowpark DataFrames run inside Snowflake.
- pandas on Snowflake scales pandas code.
- Data doesn't need to leave the platform.

<!-- unit: Apps, containers and AI -->

<!-- goals -->

- Describe Snowpark Container Services, Streamlit in Snowflake and Snowflake ML.
- Use Cortex AI functions from SQL.

<!-- concept -->

Snowflake keeps adding ways to run applications where the data is. Container Services host any containerized service or model; Streamlit apps run inside the account with its permissions; Snowflake ML provides features, registry and training tools.

Cortex brings large language models into SQL: classification, extraction, summarization and completion as functions, governed like any query.

<!-- example -->

```sql
SELECT ticket_id,
       AI_CLASSIFY(body, ['billing', 'bug', 'feature request']):labels[0]::STRING AS category,
       AI_COMPLETE('claude-sonnet-4-5', 'Summarize in one sentence: ' || body)  AS summary
FROM support.tickets
WHERE created_at >= DATEADD(day, -1, CURRENT_TIMESTAMP());
```

#### What is Snowpark Container Services?

A managed container runtime in Snowflake for running any containerized app, service or ML model (including GPUs) next to the data, governed by Snowflake's security.

#### What is Snowflake Cortex?

Snowflake's AI layer: LLM functions callable from SQL (`AI_COMPLETE`, `AI_CLASSIFY`, `AI_EXTRACT`, `AI_SENTIMENT`, summarization, translation), Cortex Search for retrieval, Cortex Analyst for natural-language questions over semantic models, and agents.

#### What is Streamlit in Snowflake?

A way to build and host Streamlit data apps directly in Snowflake, running with the account's governance and sharing them through roles.

#### What is the Snowflake ML ecosystem?

Snowflake ML includes a feature store, model registry, distributed training and inference on warehouses or containers, and ML observability, so models are built and served where the data is.

<!-- challenge -->

Support wants each new ticket tagged by topic every hour, and the team plans to build a separate ML service. What could be simpler?

<!-- solution -->

A scheduled task (or dynamic table) that runs a Cortex function like `AI_CLASSIFY` over new tickets in SQL, governed by Snowflake permissions, with no separate service to host.

<!-- takeaways -->

- Container Services host any service in Snowflake.
- Streamlit apps run with account governance.
- Cortex exposes LLMs as SQL functions.

### Modeling and integration

<!-- unit: Modeling in Snowflake -->

<!-- goals -->

- Apply star schemas, normalization and wide tables in Snowflake.
- Implement SCD Type 2 and conformed reference data.

<!-- concept -->

Snowflake's power doesn't make modeling obsolete. Columnar storage and fast joins mean star schemas run well and wide tables cost little for unused columns, but clear models still make data understandable and consistent. Normalize where integrity and reuse matter, denormalize for consumption.

History and shared reference data need the same discipline as anywhere: SCD Type 2 with `MERGE`, and conformed dimensions owned by one model.

<!-- example -->

```sql
MERGE INTO dim_customer d
USING stg_customer s ON d.customer_id = s.customer_id AND d.is_current
WHEN MATCHED AND d.hash_diff <> s.hash_diff
  THEN UPDATE SET valid_to = s.loaded_at, is_current = FALSE;
INSERT INTO dim_customer (customer_id, segment, hash_diff, valid_from, valid_to, is_current)
SELECT s.customer_id, s.segment, s.hash_diff, s.loaded_at, '9999-12-31', TRUE
FROM stg_customer s
LEFT JOIN dim_customer d ON d.customer_id = s.customer_id AND d.is_current
WHERE d.customer_id IS NULL;
```

#### Is star schema modeling still useful in Snowflake?

Yes. Snowflake handles joins well and storage is cheap, but star schemas still make analytics simpler, consistent and fast for BI tools. Many teams use a layered approach: raw, staging, intermediate and marts with facts and dimensions, often built with dbt.

#### Should you normalize or denormalize in Snowflake?

Normalize where data integrity and reuse matter (core entities), denormalize for consumption (wide marts, one big table for specific dashboards). Columnar storage makes wide tables cheap to query when only some columns are read.

#### What is the "one big table" approach, and when does it fit?

A wide denormalized table with everything a use case needs, which is fast to query in a columnar engine and simple for BI. It fits stable, specific use cases; for general analytics, star schemas stay more flexible and consistent.

#### How do you model slowly changing reference data shared by many marts?

As conformed dimensions owned by one model, with surrogate keys and SCD history as needed, referenced by all marts so every report uses the same definitions.

#### How do you implement SCD Type 2 in Snowflake?

With a `MERGE` that closes changed current rows and inserts new versions (often two statements or a union trick), with streams and tasks for incremental processing, or with dbt snapshots, which handle it automatically.

<!-- challenge -->

Each mart team built its own customer table with slightly different segment rules. How do you consolidate?

<!-- solution -->

Create one conformed `dim_customer` owned by a single model (with SCD history if needed and agreed segment rules), have all marts reference its surrogate keys, and deprecate the local copies.

<!-- takeaways -->

- Star schemas still help understanding and consistency.
- Normalize for integrity; denormalize for consumption.
- SCD2 with `MERGE`; conform shared dimensions.

<!-- unit: Tools around Snowflake -->

<!-- goals -->

- Explain how dbt runs on Snowflake.
- Integrate Spark with Snowflake.

<!-- concept -->

Most Snowflake platforms combine it with other tools. dbt is the common transformation layer: models compile to SQL that runs on a Snowflake warehouse, with Snowflake-specific configs for clustering, transient tables and warehouses per model.

Spark integrates through a connector that reads and writes Snowflake tables, pushing filters and queries down, which suits teams that process some data in Spark and serve it from Snowflake.

<!-- example -->

```sql
-- dbt model config for Snowflake
{{ config(materialized='incremental', unique_key='order_id',
          cluster_by=['order_date'], transient=false, snowflake_warehouse='wh_transform_l') }}
select * from {{ ref('stg_orders') }}
{% if is_incremental() %} where order_date >= dateadd(day, -3, current_date) {% endif %}
```

#### How does dbt work with Snowflake?

dbt compiles models to SQL and runs them on a Snowflake warehouse through the dbt-snowflake adapter, supporting tables, views, incremental models (`merge`, `delete+insert`, `append`, `microbatch`), dynamic tables, transient tables, query tags and clustering configs.

#### How do Spark and Snowflake integrate?

Through the Spark connector, which reads and writes Snowflake tables with query pushdown, or by sharing Iceberg tables through a catalog so Spark and Snowflake both work on the same files.

<!-- challenge -->

One heavy dbt model needs a Large warehouse, but the rest run fine on Small. How do you avoid running everything on Large?

<!-- solution -->

Set `snowflake_warehouse` in that model's config to the Large warehouse and keep the project default on Small, so only the heavy model uses the bigger compute.

<!-- takeaways -->

- dbt compiles models to SQL run on Snowflake.
- Snowflake-specific configs tune each model.
- The Spark connector reads and writes with pushdown.

<!-- stage: Protecting and sharing data -->

### Time Travel, Fail-safe and cloning

<!-- unit: Time Travel and Fail-safe -->

<!-- goals -->

- Query and restore past data with Time Travel.
- Explain Fail-safe and set retention periods.

<!-- concept -->

Because micro-partitions are immutable, Snowflake can keep old versions cheaply. Time Travel lets you query a table as it was, restore it, or undrop it within a retention period you set. After that, Fail-safe keeps permanent tables recoverable for another week, but only Snowflake support can use it, for disasters.

Retention is a cost lever: long retention on tables that change constantly multiplies storage.

<!-- example -->

```sql
SELECT COUNT(*) FROM sales.orders AT (OFFSET => -3600);                  -- an hour ago
INSERT INTO sales.orders
SELECT * FROM sales.orders BEFORE (STATEMENT => '01b8a0e3-0002-...');      -- before the bad DELETE
ALTER TABLE sales.orders SET DATA_RETENTION_TIME_IN_DAYS = 14;
```

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

#### What happens to Time Travel when you drop and recreate a table with the same name?

The new table is separate; the dropped one stays in Time Travel and can be restored with `UNDROP` only after renaming the new table, since names must be unique.

#### Someone ran `DELETE FROM orders` without a `WHERE` an hour ago. How do you recover?

Use Time Travel: insert back the rows from `orders AT (OFFSET => -3600)` or `BEFORE (STATEMENT => '<query id>')`, or clone the table at that point and swap it in with `ALTER TABLE … SWAP WITH`. Then restrict delete rights on production tables.

<!-- challenge -->

A table was dropped and recreated with the same name, and now `UNDROP TABLE orders` fails. Why, and how do you restore the old one?

<!-- solution -->

An object with that name exists, so `UNDROP` can't restore over it. Rename the new table first (`ALTER TABLE orders RENAME TO orders_new`), then `UNDROP TABLE orders`.

<!-- takeaways -->

- Time Travel queries and restores past data.
- Fail-safe is a support-only disaster net.
- Retention costs storage on high-churn tables.

<!-- unit: Zero-copy cloning -->

<!-- goals -->

- Clone tables, schemas and databases instantly.
- Understand what clones inherit and clone from points in time.

<!-- concept -->

Cloning creates a full copy by pointing at the same micro-partitions instead of copying them. It's instant and costs no storage until the copy or the original changes. That makes full-size development and test environments cheap and fast.

Clones inherit data and structure, and at database or schema level their child objects, but not all privileges; and combined with Time Travel, they can capture a table as it was before a problem.

<!-- example -->

```sql
CREATE DATABASE analytics_dev CLONE analytics;                                 -- instant
CREATE TABLE sales.orders_before_fix CLONE sales.orders AT (TIMESTAMP => '2026-10-17 08:00:00'::TIMESTAMP_TZ);
GRANT USAGE ON DATABASE analytics_dev TO ROLE developer;
```

#### What is zero-copy cloning?

Creating a copy of a table, schema or database instantly with `CLONE`, without copying data: the clone shares the original's micro-partitions and only new changes consume storage. It's used for dev and test environments, backups before risky changes, and point-in-time snapshots.

#### What does a clone inherit?

The data and structure, and for databases and schemas the child objects. Privileges on the source object itself are not copied unless you use `COPY GRANTS`; privileges on child objects are cloned. Pipes referencing internal stages, and some other objects, are not cloned.

#### How would you give a developer a full copy of production data cheaply?

Clone the production database into a dev database (instantly, with no extra storage until changes are made), apply masking policies or a secure view layer if the data is sensitive, and give the developer a role on the clone.

#### Can you clone from a point in time?

Yes: `CREATE TABLE t_clone CLONE t AT (TIMESTAMP => ...)` or `BEFORE (STATEMENT => ...)`, as long as it's within the retention period. It is a common way to recover from a bad change while keeping the current table for comparison.

<!-- challenge -->

Developers get a weekly clone of production, but it contains customer emails they shouldn't see. What do you add?

<!-- solution -->

Masking policies (ideally tag-based) on PII columns that reveal values only to privileged roles; clones keep the policies, so developers see masked data. Alternatively, mask in a post-clone step.

<!-- takeaways -->

- Clones share micro-partitions; instant and cheap.
- They diverge only as data changes.
- Clone at a timestamp to capture past states.

### Security and access control

<!-- unit: RBAC and role design -->

<!-- goals -->

- Explain Snowflake's role-based access control and system roles.
- Design a role hierarchy and use ownership, ACCOUNTADMIN and secondary roles carefully.

<!-- concept -->

In Snowflake, privileges go to roles, roles go to users, and roles can contain other roles. Every object has an owning role with full control. System roles split administration: one for security, one for users, one for everything. Using the top role daily turns every mistake into a potential disaster.

A clean design separates access roles, which hold privileges on objects, from functional roles, which represent jobs and are granted access roles. Secondary roles let a session use all its roles at once.

<!-- example -->

```sql
CREATE ROLE sales_read;   GRANT USAGE ON DATABASE sales TO ROLE sales_read;
GRANT USAGE ON SCHEMA sales.marts TO ROLE sales_read;
GRANT SELECT ON ALL TABLES IN SCHEMA sales.marts TO ROLE sales_read;
CREATE ROLE analyst_sales; GRANT ROLE sales_read TO ROLE analyst_sales;
GRANT ROLE analyst_sales TO ROLE sysadmin;     -- keep the hierarchy connected
GRANT ROLE analyst_sales TO USER ana;
```

#### How does access control work in Snowflake?

Through role-based access control (RBAC) combined with discretionary access control: privileges are granted to roles, roles are granted to users and other roles, and each object has an owner role that controls it.

#### What are the system-defined roles?

ORGADMIN (organization), ACCOUNTADMIN (top account role; use sparingly), SECURITYADMIN (manages grants and can manage users and roles), USERADMIN (creates users and roles), SYSADMIN (creates warehouses and databases; custom roles should roll up to it) and PUBLIC (granted to everyone).

#### What is a good role hierarchy?

Access roles holding privileges on objects (for example `SALES_READ`, `SALES_WRITE`), functional roles representing jobs or teams (`ANALYST`, `DATA_ENGINEER`) that are granted access roles, and functional roles rolled up to SYSADMIN so administrators can manage everything. Service accounts get their own functional roles.

#### What is the difference between `OWNERSHIP` and other privileges?

The role owning an object has full control, including granting privileges on it and dropping it. Other privileges (`SELECT`, `INSERT`, `USAGE`, `MONITOR`, `OPERATE`) allow specific actions. Ownership can be transferred with `GRANT OWNERSHIP`.

#### Why shouldn't ACCOUNTADMIN be the default role for anyone?

It has unrestricted power, so mistakes or compromised sessions are catastrophic. Grant it to a few administrators with MFA, never use it for daily work or service accounts, and create objects with SYSADMIN or custom roles.

#### What are secondary roles?

`USE SECONDARY ROLES ALL` lets a session use the privileges of all granted roles for queries (the primary role still owns created objects), which simplifies work for users with several roles.

<!-- challenge -->

Ten analysts have ACCOUNTADMIN as their default role "to avoid permission errors". What do you change?

<!-- solution -->

Create functional roles with only the access roles they need, make those the default, restrict ACCOUNTADMIN to two or three admins with MFA, and fix missing grants rather than escalating.

<!-- takeaways -->

- Privileges → roles → users; roles nest.
- Separate access roles from functional roles.
- Keep ACCOUNTADMIN rare and protected.

<!-- unit: Grants at scale -->

<!-- goals -->

- Use future grants and database roles.
- Centralize grant control with managed access schemas.

<!-- concept -->

Granting object by object breaks as soon as new tables appear. Future grants apply privileges automatically to objects created later in a schema or database. Database roles scope access within one database, which is also how fine-grained access travels with shares.

Managed access schemas centralize who can grant: object owners can no longer hand out access themselves, only the schema owner or a role with grant management can.

<!-- example -->

```sql
GRANT SELECT ON FUTURE TABLES IN SCHEMA sales.marts TO ROLE sales_read;
CREATE DATABASE ROLE sales.reader;
GRANT SELECT ON ALL TABLES IN SCHEMA sales.marts TO DATABASE ROLE sales.reader;
CREATE SCHEMA sales.restricted WITH MANAGED ACCESS;
```

#### What are future grants?

Grants that apply automatically to objects created later in a schema or database: `GRANT SELECT ON FUTURE TABLES IN SCHEMA sales.marts TO ROLE sales_read;`. They avoid missing grants on new tables.

#### What are database roles?

Roles scoped to a database, used to manage access inside it and especially to share fine-grained access through data sharing.

#### What are managed access schemas?

Schemas where only the schema owner (or roles with `MANAGE GRANTS`) can grant privileges on objects, not the object owners, which centralizes access control.

<!-- challenge -->

Every new table in a schema requires a ticket to grant analysts access. What do you set up?

<!-- solution -->

Future grants on the schema (`GRANT SELECT ON FUTURE TABLES IN SCHEMA ... TO ROLE ...`), so new tables are readable by the access role automatically, managed as code.

<!-- takeaways -->

- Future grants cover objects created later.
- Database roles scope access inside a database.
- Managed access schemas centralize granting.

<!-- unit: Column and row protection -->

<!-- goals -->

- Protect columns with masking and tag-based policies, and rows with row access policies.
- Classify sensitive data and use secure views.

<!-- concept -->

Table-level grants are too coarse for personal data. Masking policies rewrite column values at query time depending on who asks; row access policies decide which rows each role sees. Attaching masking policies to tags scales protection: tag a column as PII and it's masked everywhere.

Classification finds sensitive columns automatically, and secure views and functions hide their definitions from consumers, which matters when sharing.

<!-- example -->

```sql
CREATE MASKING POLICY gov.mask_email AS (v STRING) RETURNS STRING ->
  CASE WHEN IS_ROLE_IN_SESSION('PII_READER') THEN v ELSE REGEXP_REPLACE(v, '.+@', '***@') END;
ALTER TAG gov.pii SET MASKING POLICY gov.mask_email;
CREATE ROW ACCESS POLICY gov.by_country AS (country STRING) RETURNS BOOLEAN ->
  EXISTS (SELECT 1 FROM gov.role_countries r
          WHERE r.country = country AND IS_ROLE_IN_SESSION(r.role_name));
ALTER TABLE sales.customers ADD ROW ACCESS POLICY gov.by_country ON (country);
```

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

#### What are secure views and secure UDFs?

Views and functions whose definition is hidden from non-owners and that disable some optimizations that could leak data through query behavior. They are required for objects in data shares.

#### You must give analysts in each country access only to their rows and hide emails. How?

A row access policy on the tables using a mapping table of roles to countries, and a masking policy (or tag-based masking) on email columns that reveals values only to a privileged role. Grant analysts functional roles mapped to their countries.

<!-- challenge -->

New tables with emails keep appearing, and each time someone forgets to add a masking policy. How do you make protection automatic?

<!-- solution -->

Use tag-based masking: attach the policy to a `pii` tag, run classification (or tag in table templates) so email columns get the tag, and every tagged column is masked without per-table work.

<!-- takeaways -->

- Masking policies protect columns at query time.
- Row access policies filter rows per role.
- Tags and classification scale protection.

<!-- unit: Authentication, network and audit -->

<!-- goals -->

- Secure sign-in, network access and external calls.
- Explain encryption and audit access with access history.

<!-- concept -->

Around the data, Snowflake secures who gets in and what leaves. Users sign in with MFA, SSO or key pairs; network policies limit where connections come from; external access integrations control which outside endpoints code may call.

Encryption is always on, at rest and in transit. Access history records which columns each query read and wrote, which answers audit and lineage questions precisely.

<!-- example -->

```sql
CREATE NETWORK POLICY corp_only ALLOWED_IP_LIST = ('203.0.113.0/24');
ALTER USER etl_svc SET NETWORK_POLICY = corp_only;
SELECT query_start_time, user_name, direct_objects_accessed
FROM snowflake.account_usage.access_history
WHERE ARRAY_CONTAINS('SALES.PUBLIC.CUSTOMERS'::VARIANT,
      TRANSFORM(base_objects_accessed, o -> o:objectName))
ORDER BY query_start_time DESC LIMIT 20;
```

#### How do users authenticate to Snowflake?

With passwords plus MFA (which Snowflake is making mandatory for password sign-ins), SSO through SAML 2.0 identity providers (Okta, Entra ID), OAuth (Snowflake or external), key-pair authentication for services, workload identity federation, and programmatic access tokens. Service users should use key pairs or OAuth, not passwords.

#### What are network policies?

Rules that allow or block client IP addresses (and network rules for private endpoints) at account or user level, so only corporate networks or specific services can connect.

#### How is data encrypted in Snowflake?

Always at rest (AES-256) and in transit (TLS), with a hierarchical key model and automatic key rotation. Business Critical adds Tri-Secret Secure, combining a customer-managed key with Snowflake's key.

#### What is the access history view used for?

`SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY` records which columns each query read and wrote, which helps auditing, lineage and finding unused data.

#### What are external access integrations?

Objects that allow UDFs and procedures to call external network endpoints, controlled by network rules listing allowed hosts and secrets objects for credentials.

<!-- challenge -->

Auditors ask who read the `customers.national_id` column in the last quarter. Where do you look?

<!-- solution -->

`ACCOUNT_USAGE.ACCESS_HISTORY`, which lists the columns each query accessed (base and direct objects), filtered on that column and date range, joined with query history for details.

<!-- takeaways -->

- MFA, SSO and key pairs for authentication.
- Network policies and integrations control traffic.
- Access history records column-level access.

### Data sharing and collaboration

<!-- unit: Secure Data Sharing -->

<!-- goals -->

- Share live data with other accounts and non-Snowflake users.
- Share across regions and understand consumer limits.

<!-- concept -->

Sharing in Snowflake means granting access, not sending files. The provider adds objects to a share; the consumer mounts it as a read-only database and queries live data with their own compute. No copies, no exports, no stale versions.

Partners without Snowflake can use reader accounts the provider pays for. Consumers in other regions need replication or listings that handle it. Consumers can query but not modify shared data.

<!-- example -->

```sql
CREATE SECURE VIEW share_db.partner.v_sales AS
  SELECT order_date, region, product, revenue FROM marts.fct_sales WHERE partner_id = 42;
CREATE SHARE partner_42;
GRANT USAGE ON DATABASE share_db TO SHARE partner_42;
GRANT USAGE ON SCHEMA share_db.partner TO SHARE partner_42;
GRANT SELECT ON VIEW share_db.partner.v_sales TO SHARE partner_42;
ALTER SHARE partner_42 ADD ACCOUNTS = partnerorg.partner_account;
```

#### What is Secure Data Sharing?

Sharing live, read-only data from one account with another without copying it: the provider creates a share containing databases, schemas, tables and secure views, and the consumer creates a database from it. The consumer pays for the compute it uses; the provider pays for storage.

#### Can you share with someone who doesn't have a Snowflake account?

Yes, through a reader account that the provider creates and pays for, with limited capabilities.

#### How does sharing work across regions or clouds?

Data must be replicated to an account in the consumer's region, or shared through listings with cross-cloud auto-fulfillment, which replicates the data automatically.

#### What can't you do with shared data as a consumer?

You can't modify it, clone it or re-share it (except through specific provider settings), and Time Travel isn't available on shared objects. You can query it, join it with your data and create views over it.

#### How do you give a partner access to a curated dataset without copying it?

Create secure views on the curated tables, put them in a share (or a private listing), and add the partner's account as a consumer; if they have no Snowflake account, create a reader account. Use row access policies or separate views to limit what they see.

<!-- challenge -->

A partner in another cloud region needs your daily sales data. A direct share fails. What do you do?

<!-- solution -->

Replicate the database to an account in the partner's region and share from there, or publish a private listing with cross-cloud auto-fulfillment, which handles the replication.

<!-- takeaways -->

- Shares grant live, read-only access without copies.
- Reader accounts serve partners without Snowflake.
- Cross-region sharing needs replication or listings.

<!-- unit: Marketplace, clean rooms and apps -->

<!-- goals -->

- Describe listings and the Snowflake Marketplace.
- Explain data clean rooms and Native Apps.

<!-- concept -->

Sharing scales into products. Listings package shares with descriptions, terms and usage analytics, published privately or on the Marketplace. Clean rooms let several parties analyze combined data while each keeps control over what can be revealed, such as audience overlaps without exposing customer lists.

Native Apps go furthest, distributing code and data together that runs inside the consumer's account.

<!-- example -->

| Need | Mechanism |
|---|---|
| Offer weather data to any customer | Marketplace listing |
| Share a dataset with one partner, with terms | Private listing |
| Measure audience overlap with an advertiser | Data clean room |
| Ship an analytics app that runs in customers' accounts | Native App |

#### What is the Snowflake Marketplace?

A catalog of listings where providers publish free or paid datasets, data services and Native Apps that consumers can get into their accounts directly.

#### What is a listing?

A packaged offering of a share or Native App with metadata, terms and usage analytics, published privately to chosen accounts or publicly on the Marketplace.

#### What are data clean rooms?

Environments where several parties combine data for analysis (for example audience overlap) under policies that allow only approved queries and aggregated outputs, without exposing raw records to each other.

#### What is a Native App?

An application packaged with code and data that a provider distributes through the Marketplace and that runs inside the consumer's account, so the consumer's data doesn't leave it.

<!-- challenge -->

A retailer and a brand want to know how many customers they share, without either seeing the other's customer list. What fits?

<!-- solution -->

A data clean room: each party contributes hashed identifiers, and only approved aggregate queries (overlap counts above a threshold) can run, so no individual records are revealed.

<!-- takeaways -->

- Listings package shares as products.
- Clean rooms allow joint analysis with control.
- Native Apps ship code and data to consumers.

<!-- stage: Operating Snowflake -->

### Performance

<!-- unit: Reading the Query Profile -->

<!-- goals -->

- Diagnose slow queries with the Query Profile and EXPLAIN.
- Fix spilling, exploding joins and costly DISTINCTs.

<!-- concept -->

The Query Profile shows where a query spends its time and data: the most expensive operators, partitions scanned versus total, bytes spilled, and rows produced at each step. Most problems are visible there at a glance.

Three patterns recur: spilling when memory runs short, exploding joins when a key isn't unique and rows multiply, and `DISTINCT` used to hide duplicates that a bad join created.

<!-- example -->

```text
Query Profile (most expensive nodes)
  Join [id = id]           48%   rows in: 2 M × 3 M   rows out: 1.8 B   ← exploding join
  TableScan ORDERS         31%   partitions 11,500 / 12,000             ← poor pruning
  Aggregate                12%   bytes spilled to local storage: 85 GB ← memory
```

#### How do you find out why a query is slow?

Open the Query Profile: look at the most expensive operators, partitions scanned versus total (pruning), bytes spilled to local and remote storage, exploding joins (output rows much greater than input), and queuing time. `GET_QUERY_OPERATOR_STATS` gives the same data in SQL.

#### What does `EXPLAIN` show in Snowflake?

The logical plan of a query without running it: operators, join order and partitions to be scanned (from metadata), useful to check pruning before running an expensive query.

#### What is spilling, and how do you fix it?

When a warehouse doesn't have enough memory for an operation, it spills to local disk and then to remote storage, which is much slower. Fix it with a larger warehouse, by processing less data (better filters, pre-aggregation), or by splitting the query.

#### What causes an "exploding join"?

A join on a non-unique key, or missing join conditions, so each row matches many rows and the output multiplies. Check join keys for uniqueness and that every join has the full condition.

#### How do you speed up a query using `DISTINCT` on huge data?

Check if deduplication is really needed (often a join fanned out), deduplicate earlier on fewer columns, use `APPROX_COUNT_DISTINCT` (HyperLogLog) when an estimate is enough, and use a larger warehouse if it spills.

<!-- challenge -->

A query's join outputs 600× more rows than its largest input. What do you check, and how do you fix it?

<!-- solution -->

The join keys: one side isn't unique on the key (or a condition is missing), so rows multiply. Fix the join grain (deduplicate or aggregate that side first, add the missing condition) and remove any `DISTINCT` masking it.

<!-- takeaways -->

- Start with the Query Profile's costliest nodes.
- Spilling means more memory or less data.
- Exploding joins come from non-unique keys.

<!-- unit: Pruning and search -->

<!-- goals -->

- Improve pruning with filters, clustering and sorted loads.
- Use the Search Optimization Service for point lookups.

<!-- concept -->

Most Snowflake performance comes from reading less. Filters on columns that follow load order, usually dates, prune well; filters wrapped in functions or on unclustered columns don't. Clustering keys and loading data sorted by the main filter columns improve pruning for large tables.

For needle-in-a-haystack lookups by an ID or string, search optimization builds an access path that finds the few matching micro-partitions without reorganizing the table.

<!-- example -->

```sql
-- prunes poorly: function on the filter column
SELECT * FROM events WHERE TO_DATE(event_ts) = '2026-10-17';
-- prunes well: range on the raw column
SELECT * FROM events WHERE event_ts >= '2026-10-17' AND event_ts < '2026-10-18';
ALTER TABLE events ADD SEARCH OPTIMIZATION ON EQUALITY(customer_id);
```

#### How do you improve pruning?

Filter on columns that correlate with load order (dates), add a clustering key on large tables filtered by other columns, avoid wrapping filter columns in functions that prevent pruning, and filter as early as possible.

#### What is the Search Optimization Service?

An Enterprise feature that builds a persistent search access path for a table so point lookups and selective filters (equality, `IN`, substring and regex searches, `VARIANT` fields, geo) can skip most micro-partitions. It costs storage and maintenance credits.

#### Is `ORDER BY` in a `CREATE TABLE AS` useful?

Yes, on initial loads of big tables: sorting by the main filter columns produces well-clustered micro-partitions from the start, improving pruning without paying for automatic clustering.

#### A query scans 98% of a 5 TB table's partitions although it filters on `customer_id`. How do you fix it?

The table isn't clustered by `customer_id`. For point lookups, enable search optimization on that column; for range filters used often, add a clustering key (possibly combined with date); otherwise reconsider the query or create a pre-aggregated table.

<!-- challenge -->

Support looks up single customers by `email` in a 4 TB events table, and each lookup scans most of it. What do you add?

<!-- solution -->

Search optimization on the `email` column (equality), which lets point lookups skip almost all micro-partitions; clustering by email would be costly and help little for other queries.

<!-- takeaways -->

- Filter raw columns, not functions of them.
- Cluster or sort large tables by main filters.
- Search optimization serves point lookups.

<!-- unit: Writing efficient workloads -->

<!-- goals -->

- Avoid common anti-patterns such as SELECT * and single-row DML.
- Speed up large MERGEs and use approximate functions.

<!-- concept -->

Snowflake rewards set-based work and punishes habits from row-oriented databases. Reading all columns of wide tables wastes the columnar layout; inserting rows one at a time creates many tiny micro-partitions; joining on mismatched types prevents pruning.

Large merges need the same attention: limiting the target with date or key ranges lets Snowflake prune most of the table. Approximate functions trade a tiny error for huge savings on distinct counts and percentiles.

<!-- example -->

```sql
MERGE INTO sales.orders t
USING staging.orders_delta s
ON  t.order_id = s.order_id
AND t.order_date >= DATEADD(day, -7, CURRENT_DATE())     -- prune the 3 TB target
WHEN MATCHED THEN UPDATE SET amount = s.amount
WHEN NOT MATCHED THEN INSERT (order_id, order_date, amount) VALUES (s.order_id, s.order_date, s.amount);
SELECT APPROX_COUNT_DISTINCT(user_id) FROM events WHERE event_date >= '2026-10-01';
```

#### Why avoid `SELECT *` in Snowflake?

Storage is columnar, so reading only needed columns scans far less data. `SELECT *` on wide tables reads every column and slows queries and BI extracts.

#### How do you make many small `INSERT` statements faster?

Don't: Snowflake is optimized for set-based operations. Batch rows into files and use `COPY`, use Snowpipe Streaming for continuous rows, or insert in large multi-row statements.

#### What are common mistakes that make Snowflake slow?

Single-row DML in loops, `SELECT *`, functions on filter columns, joins on mismatched types, huge `IN` lists, too-small warehouses that spill, too-large warehouses for trivial queries (cost), and complex views stacked many levels deep.

#### What are approximate functions useful for?

`APPROX_COUNT_DISTINCT`, `APPROX_PERCENTILE` and `APPROX_TOP_K` give estimates with small error using far less memory and time, which suits dashboards and exploration on very large tables.

#### A nightly `MERGE` into a 3 TB table takes hours. What do you check?

Whether the target is pruned (add a date or key range filter in the `ON` clause, cluster by the merge key), whether the source has duplicates or is far larger than the changes, the warehouse size and spilling, and whether an incremental approach (streams, `delete+insert` on recent partitions) fits better.

<!-- challenge -->

An application inserts 50,000 rows a minute with single-row `INSERT` statements and queries on the table get slower. What do you change?

<!-- solution -->

Batch the rows: write micro-batch files and load with `COPY`/Snowpipe, or use Snowpipe Streaming. Single-row inserts create many tiny micro-partitions and waste compute per statement.

<!-- takeaways -->

- Select only needed columns.
- Batch writes; avoid single-row DML.
- Prune MERGE targets with range conditions.

### Cost management

<!-- unit: What drives cost -->

<!-- goals -->

- Identify Snowflake's main cost drivers.
- Reason about warehouse size, resume minimums and cloud services billing.

<!-- concept -->

For most accounts, warehouse compute is the bill. Serverless features, storage and data transfer follow. Compute cost depends less on size than on time running: a bigger warehouse that finishes faster can cost the same, while a small one kept awake by frequent tiny queries costs far more than its work.

Two billing details explain many surprises: every resume bills at least a minute, and cloud services are free only up to a share of daily compute.

<!-- example -->

```text
query: 1 s, every minute, X-Small, auto-suspend 600 s
→ warehouse never suspends: 24 h × 1 credit/h = 24 credits/day for ~24 min of actual work
fix: batch the checks, use a serverless task, or a shared warehouse already running
```

#### What drives Snowflake costs?

Warehouse compute (by far the largest for most customers), serverless features (Snowpipe, clustering, materialized views, search optimization, tasks, AI functions), storage (including Time Travel and Fail-safe), cloud services above 10% of compute, and data transfer out of the region.

#### Is a bigger warehouse always more expensive?

Not necessarily. If a query parallelizes well, doubling the size halves the runtime at double the rate, so the cost is similar and the result arrives sooner. It's more expensive when queries are small or don't parallelize.

#### Why is a warehouse that runs a one-second query every minute expensive?

Each resume bills at least 60 seconds, and auto-suspend keeps it running for the configured idle time after each query. A query every minute can keep the warehouse running permanently. Batch such queries, use serverless tasks, or use a single small shared warehouse.

#### How does the cloud services adjustment work?

Cloud services usage is free up to 10% of the day's warehouse compute; only the excess is billed. Heavy metadata operations (many tiny queries, `SHOW` commands, frequent clones) can exceed it.

<!-- challenge -->

A monitoring script runs a one-second query every two minutes on its own warehouse. How can you cut its cost?

<!-- solution -->

Run it on an existing warehouse that's already up, lower its frequency, use a serverless task or alert, or set a very short auto-suspend; a dedicated warehouse pays minimums and idle time for seconds of work.

<!-- takeaways -->

- Warehouse time dominates cost.
- Bigger and faster can cost the same.
- Frequent tiny queries keep warehouses awake.

<!-- unit: Monitoring and controlling spend -->

<!-- goals -->

- Track credit usage by warehouse, query and tag.
- Control spend with resource monitors and budgets.

<!-- concept -->

Cost control starts with attribution. Account usage views show credits by warehouse and serverless service; query history, with query tags, ties spend to jobs, teams and tools. Resource monitors and budgets add limits: notify, then suspend warehouses when quotas are reached.

When costs jump, the same data answers why: which warehouse, which service, which queries changed.

<!-- example -->

```sql
ALTER SESSION SET QUERY_TAG = 'dbt:marts_daily';
SELECT warehouse_name, SUM(credits_used) AS credits
FROM snowflake.account_usage.warehouse_metering_history
WHERE start_time >= DATEADD(month, -1, CURRENT_DATE())
GROUP BY 1 ORDER BY 2 DESC;
CREATE RESOURCE MONITOR rm_bi WITH CREDIT_QUOTA = 500
  TRIGGERS ON 80 PERCENT DO NOTIFY ON 100 PERCENT DO SUSPEND;
ALTER WAREHOUSE wh_bi SET RESOURCE_MONITOR = rm_bi;
```

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

#### Costs jumped 40% this month. How do you investigate?

Compare `WAREHOUSE_METERING_HISTORY` and serverless metering by service and warehouse, find the warehouses and query tags that grew, look at `QUERY_ATTRIBUTION_HISTORY` for the costliest queries, and check for warehouses no longer auto-suspending, new dynamic tables with tight lag, reclustering on high-churn tables, or full refreshes.

<!-- challenge -->

Finance wants monthly Snowflake cost per team, but teams share warehouses. How do you attribute it?

<!-- solution -->

Set query tags per team or tool (dbt, BI, notebooks), then allocate warehouse credits by each tag's share of execution time from query history (`QUERY_ATTRIBUTION_HISTORY` where available), plus separate warehouses for the biggest teams.

<!-- takeaways -->

- Attribute credits by warehouse, query and tag.
- Resource monitors and budgets enforce limits.
- Usage views explain cost jumps.

<!-- unit: Reducing costs -->

<!-- goals -->

- Reduce warehouse costs with sizing, suspension and workload design.
- Reduce storage costs with table types and retention.

<!-- concept -->

Compute savings come from not paying for idle or waste: right-size per workload, suspend quickly, consolidate tiny workloads, process incrementally instead of rebuilding, and let caching work.

Storage savings come from history more than data: transient tables for rebuildable data, shorter Time Travel on high-churn tables, and dropping unused tables and old clones that have diverged.

<!-- example -->

| Lever | Typical saving |
|---|---|
| Auto-suspend 60 s on ETL warehouses | Idle hours removed |
| Incremental models instead of full rebuilds | Most of transform compute |
| Transient staging tables | Fail-safe storage |
| Retention 1 day on high-churn tables | Time Travel storage |

#### How do you reduce warehouse costs?

Right-size warehouses per workload, use short auto-suspend, avoid always-on warehouses, consolidate small jobs onto shared warehouses, use multi-cluster with the Economy policy where queuing is acceptable, set statement timeouts, optimize the most expensive queries, and use resource monitors.

#### How do you reduce storage costs?

Use transient tables for staging and rebuildable data, shorten Time Travel on high-churn tables, drop unused tables and clones that diverged, clean old stage files, and avoid keeping many full copies instead of clones.

<!-- challenge -->

Storage costs doubled although active data grew 10%. What do you check?

<!-- solution -->

Time Travel and Fail-safe bytes per table (`TABLE_STORAGE_METRICS`): high-churn tables with long retention, permanent staging tables, and clones whose data diverged. Shorten retention and convert rebuildable tables to transient.

<!-- takeaways -->

- Pay for work, not idle: size, suspend, consolidate.
- Process incrementally.
- History storage often dominates storage cost.

### Operations and data protection

<!-- unit: Monitoring and data quality -->

<!-- goals -->

- Choose between ACCOUNT_USAGE and INFORMATION_SCHEMA.
- Monitor data quality with alerts, data metric functions and the event table.

<!-- concept -->

Two families of views describe an account: `INFORMATION_SCHEMA` per database, real-time but short history; `ACCOUNT_USAGE` for the whole account, a year of history with some delay. Monitoring queries choose based on freshness and scope.

Data quality runs inside Snowflake too: data metric functions measure freshness, nulls or duplicates on a schedule, alerts run conditions and notify, and the event table collects logs from code running in the account.

<!-- example -->

```sql
ALTER TABLE sales.orders SET DATA_METRIC_SCHEDULE = '60 MINUTE';
ALTER TABLE sales.orders ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.DUPLICATE_COUNT ON (order_id);
CREATE ALERT ops.orders_stale
  WAREHOUSE = wh_ops SCHEDULE = '30 MINUTE'
  IF (EXISTS (SELECT 1 FROM sales.orders HAVING MAX(loaded_at) < DATEADD(hour, -2, CURRENT_TIMESTAMP())))
  THEN CALL SYSTEM$SEND_EMAIL('ops_email', 'data@example.com', 'orders stale', 'No load in 2 hours');
```

#### What is the difference between `ACCOUNT_USAGE` and `INFORMATION_SCHEMA`?

`SNOWFLAKE.ACCOUNT_USAGE` views cover the whole account, keep one year of history and include dropped objects, but have latency (minutes to a few hours). `INFORMATION_SCHEMA` views and table functions are per database, real-time and keep shorter history (7–14 days for query history).

#### How do you alert on data issues inside Snowflake?

With alerts (scheduled conditions that run an action such as sending an email or a webhook notification), data metric functions (Horizon data quality monitoring: null counts, duplicates, freshness, custom metrics), and failure notifications on tasks.

#### What are data metric functions?

Functions (system ones like `NULL_COUNT`, `DUPLICATE_COUNT`, `FRESHNESS`, or custom ones) attached to tables and run on a schedule, with results stored for monitoring data quality over time.

#### What is the event table?

A special table that collects logs, traces and metrics emitted by UDFs, procedures, Native Apps and Snowpark Container Services, so application code inside Snowflake can be monitored.

<!-- challenge -->

A cost dashboard built on `ACCOUNT_USAGE` doesn't show the last hour's queries. Is it broken?

<!-- solution -->

No: `ACCOUNT_USAGE` views have latency (often up to a few hours). For near-real-time checks use `INFORMATION_SCHEMA` table functions, accepting their shorter history and per-database scope.

<!-- takeaways -->

- `ACCOUNT_USAGE`: account-wide, long history, delayed.
- `INFORMATION_SCHEMA`: per database, real time.
- DMFs and alerts monitor quality inside Snowflake.

<!-- unit: Replication and backups -->

<!-- goals -->

- Replicate databases and fail over between accounts.
- Plan backups beyond Time Travel and Fail-safe.

<!-- concept -->

Snowflake already protects against hardware and zone failures, and Time Travel covers recent mistakes. Regional outages and longer-term protection need more. Replication copies databases, and with replication groups also users, roles and warehouses, to accounts in other regions or clouds; failover groups and client redirect let applications move to the secondary.

For backups, clones, replicated copies and unloads to your own storage cover what retention periods don't.

<!-- example -->

```sql
CREATE FAILOVER GROUP fg_prod
  OBJECT_TYPES = DATABASES, ROLES, USERS, WAREHOUSES
  ALLOWED_DATABASES = analytics, sales
  ALLOWED_ACCOUNTS = myorg.prod_dr
  REPLICATION_SCHEDULE = '10 MINUTE';
-- in the DR account, during a disaster:
ALTER FAILOVER GROUP fg_prod PRIMARY;
```

#### What is database replication?

Copying databases (and with replication groups, other objects such as users, roles, warehouses and integrations) to accounts in other regions or clouds, refreshed on a schedule, for disaster recovery, data sharing or migration.

#### What are failover groups and client redirect?

Failover groups (Business Critical) let a secondary account be promoted to primary for replicated objects during an outage. Client redirect uses a connection URL that can be switched to the new primary, so applications reconnect without config changes.

#### How do you back up Snowflake data?

Time Travel and Fail-safe cover recent mistakes and disasters; for longer protection use zero-copy clones on a schedule, backups (immutable point-in-time backup sets, where available), replication to another region, or unloading to cloud storage.

<!-- challenge -->

Compliance requires a monthly copy of finance tables kept for 7 years. Time Travel maxes out at 90 days. What do you do?

<!-- solution -->

Keep monthly zero-copy clones (named by month) of the finance schema, or unload monthly snapshots to Parquet in your own storage with object lock; manage retention as code.

<!-- takeaways -->

- Replication copies databases and account objects.
- Failover groups and client redirect enable DR.
- Long-term backups need clones or unloads.

<!-- unit: Objects as code -->

<!-- goals -->

- Manage Snowflake objects with Terraform, Git integration and declarative SQL.
- Deploy SQL changes safely through CI.

<!-- concept -->

Clicking objects into existence doesn't scale or audit well. Account-level objects such as warehouses, roles and grants fit Terraform; database objects fit dbt, migration tools or declarative `CREATE OR ALTER` scripts. A Git repository object lets Snowflake read code straight from your repository.

Deployments then follow software practice: changes reviewed in Git, applied by CI with a service user, tested in a cloned environment before production.

<!-- example -->

```hcl
resource "snowflake_warehouse" "transform" {
  name           = "WH_TRANSFORM"
  warehouse_size = "SMALL"
  auto_suspend   = 60
  auto_resume    = true
}
resource "snowflake_grant_account_role" "analyst_to_sysadmin" {
  role_name        = "ANALYST_SALES"
  parent_role_name = "SYSADMIN"
}
```

#### How do you manage Snowflake objects as code?

With Terraform (the Snowflake provider) for account objects such as warehouses, roles, grants, databases and integrations; dbt or schemachange for schema and transformation changes; and the Snowflake CLI or `EXECUTE IMMEDIATE FROM` with Git repositories in Snowflake for deploying SQL files.

#### What is a Git repository object in Snowflake?

An integration that clones a Git repository into Snowflake so you can run SQL and Python files from it, reference them in notebooks and procedures, and deploy from a branch or tag.

#### How do you run SQL deployments safely?

Version SQL in Git, deploy through CI with a service user (key pair or OAuth), use `CREATE OR ALTER` or migration tools (schemachange, dbt, Terraform), test on a cloned database first, and keep rollback scripts or rely on Time Travel and clones.

<!-- challenge -->

Warehouses and grants differ between dev and prod because people changed them by hand. How do you bring them under control?

<!-- solution -->

Import existing objects into Terraform state, define them as code with per-environment variables, review the plan, and apply only through CI; remove manual change rights for admins outside break-glass.

<!-- takeaways -->

- Terraform for account objects; dbt or migrations for database objects.
- Deploy through CI with service users.
- Test changes on clones first.

<!-- stage: Putting it together -->

### Scenarios

<!-- unit: Designing ingestion pipelines -->

<!-- goals -->

- Design pipelines from cloud storage and logs into reporting tables.
- Combine loading, semi-structured handling, transformation and monitoring.

<!-- concept -->

Ingestion design questions connect the sections. A good answer follows the files: how Snowflake accesses them, how they're loaded and how often, where raw data lands, how it's deduplicated, typed and modeled, how transformations stay incremental, and what's monitored. Naming cost choices, file sizes, warehouse per workload, incremental refreshes, shows production experience.

<!-- example -->

```text
S3 (Firehose, ~128 MB gz) ─► storage integration + stage ─► Snowpipe (auto-ingest)
  ─► raw.events (VARIANT + metadata) ─► dynamic table silver.events (typed, deduped, lag 15 min)
  ─► gold marts (dbt or dynamic tables) ─► BI warehouse (multi-cluster)
  monitoring: pipe status, DMFs freshness/duplicates, alerts, resource monitor
```

#### Design an ingestion pipeline from S3 events into Snowflake reporting tables.

Create a storage integration and external stage on the S3 prefix, a Snowpipe with auto-ingest from S3 event notifications into a raw `VARIANT` or typed table, a stream on the raw table, and dynamic tables (or tasks with `MERGE`) building cleaned and aggregated tables at the needed freshness. Add data metric functions, alerts and resource monitors, and manage everything as code.

#### A team wants to process 2 TB of JSON logs daily. How do you load and model it?

Land compressed files of ~100–250 MB in S3, load with Snowpipe or scheduled `COPY` into a `VARIANT` column in a transient raw table, extract commonly used fields into typed columns in a cleaned table clustered by event date, and aggregate into marts. Keep raw data short-lived if it can be reloaded from S3.

<!-- challenge -->

The source team warns that files may be resent after failures. Where in your design do you handle duplicates?

<!-- solution -->

Keep raw as loaded (with file name and load time), then deduplicate in silver on the event ID, keeping the latest by load time (`QUALIFY ROW_NUMBER() ... = 1`), so resent files don't create duplicate business rows.

<!-- takeaways -->

- Follow the files from storage to reports.
- Raw keeps everything; silver dedupes and types.
- Design for resends, cost and monitoring.

<!-- unit: Migrating to Snowflake -->

<!-- goals -->

- Plan a migration from an on-premises warehouse.
- Sequence translation, data movement, validation and cutover.

<!-- concept -->

Warehouse migrations fail on surprises: forgotten dependencies, SQL that translates with different semantics, consumers nobody listed. A good plan inventories objects, jobs and users, translates DDL and SQL with tools and review, moves history once and changes incrementally, then runs old and new side by side and compares results before switching consumers. Rethinking the design, not just copying it, is where most of the value lies.

<!-- example -->

| Phase | Activities |
|---|---|
| Assess | Inventory tables, jobs, reports, users; usage stats |
| Translate | DDL and SQL (SnowConvert), procedures, data types |
| Move | Historical bulk load via stages; CDC for changes |
| Validate | Row counts, checksums, report comparisons |
| Cut over | Repoint BI and jobs; retire old system |

#### How would you migrate from an on-premises data warehouse to Snowflake?

Inventory objects, workloads and dependencies; translate DDL and SQL (SnowConvert helps); move historical data through cloud storage and `COPY`; set up incremental loading; rebuild transformations (often in dbt); re-create security with roles and policies; validate with row counts, checksums and report comparisons; run both in parallel before cutover; then tune warehouses and costs.

<!-- challenge -->

After migration, a few monthly reports differ from the old system by small amounts. What are likely causes?

<!-- solution -->

Type and rounding differences (number precision, float vs decimal), time zone handling of timestamps, NULL semantics in joins and aggregates, and SQL functions translated with different behavior. Compare per day and key to localize.

<!-- takeaways -->

- Inventory before moving anything.
- Translate and review SQL semantics.
- Validate side by side before cutover.
