## Databricks Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Databricks study guide: about 200 questions](../../images/databricks_study_guide_title_img.png)

About 200 interview-style questions on Databricks, from the lakehouse idea to Delta Lake, Unity Catalog, ingestion, Lakeflow pipelines and jobs, performance tuning, security and cost. The answers reflect the platform as of 2026; Databricks renames products often, so former names are given where they are still common.

The guide follows a learning path in six stages. Each section is split into short units: learning goals, a concept explanation and a worked example, then questions (recall first, then application), a practical challenge and key takeaways. To **learn**, read each unit top to bottom. To **review**, switch to review mode or use "Skip to questions", mark answers you want to see again, and try a mixed review across sections.

<!-- QA -->
<!-- stage: Foundations -->

### Platform fundamentals

<!-- unit: The lakehouse idea -->

<!-- goals -->

- Explain what a lakehouse is and which data lake problems it fixes.
- Place Databricks' product families (Lakeflow, Mosaic AI) on that picture.

<!-- concept -->

Companies used to keep two copies of their data: a cheap data lake of files for data science, and an expensive warehouse for BI. The lake had no transactions, schemas or easy updates; the warehouse locked data in a proprietary format. A lakehouse keeps one copy in open formats on object storage and adds warehouse features on top: Delta Lake brings transactions, Unity Catalog governance, and Spark, Photon and SQL warehouses speed.

Databricks sells that platform. Its products group into families: Lakeflow for data engineering (ingest, transform, orchestrate), Databricks SQL for analytics, and Mosaic AI for machine learning.

<!-- example -->

| Need | Classic lake | Warehouse | Lakehouse |
|---|---|---|---|
| Cheap storage, open format | Yes | No | Yes |
| ACID transactions, `UPDATE`/`DELETE` | No | Yes | Yes (Delta) |
| Fine-grained permissions | Weak | Yes | Yes (Unity Catalog) |
| One copy for BI and ML | No | No | Yes |

#### What is Databricks?

A cloud data and AI platform, founded by the creators of Apache Spark, that runs on AWS, Azure and Google Cloud. It combines data engineering, SQL analytics, streaming, machine learning and governance on one copy of the data stored in open formats (Delta Lake, Apache Iceberg) in your own cloud storage.

#### What is a lakehouse?

An architecture that stores data in cheap object storage like a data lake, but adds warehouse features on top: ACID transactions, schemas, indexing-like optimizations, fine-grained governance and fast SQL. It avoids keeping one copy of the data in a lake for data science and a second copy in a warehouse for BI.

#### What problems of the classic data lake does the lakehouse solve?

Data lakes had no transactions (readers saw half-written data), no schema enforcement (garbage accumulated), slow queries over many small files, no easy updates or deletes (a problem for GDPR), and weak governance. Delta Lake and Unity Catalog address each of these.

#### What is Lakeflow?

The umbrella name, since 2025, for Databricks' data engineering products: Lakeflow Connect (managed ingestion connectors), Lakeflow Declarative Pipelines (formerly Delta Live Tables) and Lakeflow Jobs (formerly Workflows).

#### What is Mosaic AI?

Databricks' set of AI and ML features: model training and fine-tuning, Model Serving, Vector Search, AI Gateway, agent frameworks and evaluation, all governed through Unity Catalog.

#### How do you explain the lakehouse to a business stakeholder?

One place for all the company's data, stored once in open formats in the company's own cloud account, where reporting, data science and AI work on the same trusted numbers, with permissions and audit trails managed centrally.

<!-- challenge -->

Your manager asks why the team should stop exporting nightly CSVs from the lake into a separate warehouse. Write three sentences for them: what changes, what they gain, and one risk.

<!-- solution -->

Reports and models would read the same Delta tables, so the nightly copy and its delays disappear. Numbers agree across BI and data science, and permissions and audits live in one place. The risk is migration effort: existing reports must be repointed and validated against the old warehouse before it is switched off.

<!-- takeaways -->

- A lakehouse is one copy of data in open formats, with warehouse features added on top.
- Delta Lake fixes transactions and schemas; Unity Catalog fixes governance.
- Lakeflow (engineering), Databricks SQL (analytics) and Mosaic AI (ML) are the product families.

<!-- unit: Control plane, workspaces and billing -->

<!-- goals -->

- Say where Databricks runs your code and where your data stays.
- Explain how DBUs make jobs compute cheaper than all-purpose compute.

<!-- concept -->

Databricks splits into two planes. The control plane, in Databricks' account, hosts the web app, notebooks, scheduler and catalog metadata. The compute plane is where data is processed: in your cloud account for classic clusters, in Databricks' account for serverless. Either way the data at rest stays in your storage.

You work inside workspaces, usually one per environment. Processing is billed in DBUs per second, and the rate depends on the compute type: interactive all-purpose clusters cost more than jobs compute, which only lives for one run.

<!-- example -->

```text
 Control plane (Databricks)        Compute plane
 ┌──────────────────────────┐      ┌─────────────────────────────┐
 │ web app, notebooks, jobs │ ───► │ classic: VMs in YOUR account│
 │ scheduler, UC metadata   │      │ serverless: Databricks acct │
 └──────────────────────────┘      └──────────────┬──────────────┘
                                                  ▼
                                   your S3 / ADLS / GCS storage
```

#### What is the control plane versus the compute plane?

The control plane is managed by Databricks in its own account: the web application, notebooks, job scheduler, cluster manager and Unity Catalog metadata. The compute plane is where data is processed. With classic compute it runs in your cloud account (your VPC); with serverless compute it runs in Databricks' account, in the same region. Data at rest stays in your storage in both cases.

#### What is a Databricks workspace?

The environment where users work: notebooks, files, Git folders, jobs, pipelines, SQL queries, dashboards, clusters and experiments. A company usually has several workspaces (for example dev, staging and prod), attached to one Unity Catalog metastore per region.

#### What is a DBU?

A Databricks Unit, the unit of processing capacity that Databricks bills per second. The DBU rate depends on the compute type (jobs, all-purpose, SQL, serverless) and the plan. With classic compute you also pay the cloud provider for the VMs; with serverless, the DBU price includes the infrastructure.

#### Why is jobs compute cheaper than all-purpose compute?

Jobs compute is billed at a lower DBU rate because it runs scheduled, non-interactive workloads and terminates when the job ends. All-purpose clusters are for interactive development and are shared and long-lived, so Databricks charges more for them. Running production work on all-purpose clusters is a classic cost mistake.

<!-- challenge -->

A nightly production job runs on the team's shared all-purpose cluster and takes one hour. List two changes that reduce its cost without touching the code.

<!-- solution -->

Run it on jobs compute (or serverless jobs) instead of the all-purpose cluster, which lowers the DBU rate and ends billing when the run ends. Then right-size the job cluster (or use spot workers) based on the run's metrics.

<!-- takeaways -->

- The control plane is Databricks'; data at rest always stays in your storage.
- DBUs are billed per second at a rate that depends on the compute type.
- Production work belongs on jobs or serverless compute, not all-purpose clusters.

<!-- unit: Working in the workspace -->

<!-- goals -->

- Use notebooks, widgets and `dbutils` for everyday development.
- Explain why Git folders and volumes replace older patterns.

<!-- concept -->

Most development happens in notebooks: cells in Python, SQL, Scala or R that run on attached compute. Widgets turn a notebook into a parameterized job task, and `dbutils` gives access to files, secrets, parameters and task values.

Two older habits are being replaced. Code should live in Git folders, so it is reviewed and versioned like any other repository. Files should live in Unity Catalog volumes rather than DBFS, because DBFS paths have no fine-grained permissions.

<!-- example -->

A notebook that works both interactively and as a scheduled task:
```python
dbutils.widgets.text("snapshot_date", "2026-10-01")    # default for interactive runs
snapshot = dbutils.widgets.get("snapshot_date")          # the job overrides it
df = spark.read.json(f"/Volumes/raw/landing/orders/{snapshot}/")
```

#### What languages can you use in Databricks?

Python, SQL, Scala and R in notebooks, plus Java and Scala in JAR jobs. You can mix languages in a notebook with magic commands such as `%sql`, `%python`, `%scala`, `%md` (Markdown) and `%sh` (shell on the driver).

#### What is a Databricks notebook?

A web document of cells that run code against attached compute, with results, charts, comments, version history and real-time co-editing. Notebooks can be scheduled as job tasks, parameterized with widgets and stored as source files in Git.

#### What are widgets?

Input parameters for notebooks (text, dropdown, combobox, multiselect). In jobs, task parameters fill them. In SQL, parameters are referenced with the `:name` syntax.

```python
dbutils.widgets.text("snapshot_date", "2026-10-01")
snapshot = dbutils.widgets.get("snapshot_date")
```

#### What is `dbutils`?

A utility library available in notebooks and jobs: `dbutils.fs` for files, `dbutils.secrets` for secrets, `dbutils.widgets` for parameters, `dbutils.notebook.run` and `dbutils.notebook.exit` to chain notebooks, and `dbutils.jobs.taskValues` to pass small values between job tasks.

#### What are Git folders (formerly Repos)?

Workspace folders linked to a Git repository (GitHub, GitLab, Azure DevOps, Bitbucket). They let you clone, branch, commit, pull and push from the workspace, so notebooks and Python files are versioned and reviewed like any other code.

#### What is DBFS, and why is it discouraged now?

The Databricks File System, a legacy abstraction that mounted cloud storage under `dbfs:/` paths, including a workspace root bucket. It has no fine-grained governance, so Databricks now recommends Unity Catalog volumes for files and tables for data, and disables DBFS root and mounts in new setups.

<!-- challenge -->

A teammate keeps credentials in a notebook cell and reads files from `dbfs:/mnt/raw`. Which two changes do you suggest?

<!-- solution -->

Move the credentials into a secret scope read with `dbutils.secrets.get` (or better, use a storage credential so no secret is needed), and replace the mount with a Unity Catalog volume path under `/Volumes/...`, so access is governed and audited.

<!-- takeaways -->

- Widgets make the same notebook usable interactively and as a job task.
- Keep code in Git folders and files in volumes, not DBFS.
- `dbutils` covers files, secrets, widgets and task values.

<!-- unit: Runtime, Photon and remote development -->

<!-- goals -->

- Describe what a Databricks Runtime contains and what Photon accelerates.
- Explain why Spark Connect limits some APIs, and how you develop from an IDE.

<!-- concept -->

Every cluster runs a Databricks Runtime: Spark plus Delta, connectors and optimizations, in LTS versions you can pin. Photon, a C++ vectorized engine, speeds up SQL and DataFrame work underneath.

Newer compute talks to Spark through Spark Connect: the client sends a logical plan to a remote server. That makes serverless and IDE development possible (Databricks Connect, the CLI), but code that reaches into the JVM, RDDs or `SparkContext` no longer works there.

<!-- example -->

```python
# Works everywhere, including serverless (plain DataFrame API):
df.groupBy("country").count()

# Fails on Spark Connect (serverless, standard access mode):
spark.sparkContext.parallelize([1, 2, 3])
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

<!-- challenge -->

You want to step through a transformation in your IDE debugger while the data stays in Databricks. What do you set up?

<!-- solution -->

Install Databricks Connect matching the cluster's runtime (or use serverless), authenticate with the CLI (`databricks auth login`), and run the code locally: DataFrame operations execute remotely through Spark Connect, while the Python code runs in your debugger.

<!-- takeaways -->

- The runtime is the versioned image: pin an LTS version for production.
- Photon accelerates SQL and DataFrame work, not Python UDFs.
- Spark Connect enables serverless and IDE work but forbids RDD and JVM access.

### Compute

<!-- unit: Compute types and serverless -->

<!-- goals -->

- Choose between all-purpose, jobs, SQL warehouse and serverless compute.
- Explain what you give up with serverless.

<!-- concept -->

Databricks matches compute to the workload. All-purpose clusters serve interactive development, jobs compute lives for one run, and SQL warehouses serve SQL and BI. Serverless versions of all three start in seconds and bill only while working.

Serverless trades control for convenience: you can't pick instance types or most Spark configs, and code must be Spark Connect compatible. SQL warehouses are sized differently from clusters: the T-shirt size sets the speed of a single query, and the cluster count sets how many users can query at once.

<!-- example -->

| Workload | Good fit |
|---|---|
| Exploring data in a notebook | All-purpose (with auto-termination) or serverless notebook |
| Nightly ETL job | Jobs compute or serverless jobs |
| Dashboards and BI tools | Serverless SQL warehouse |
| Library that needs the JVM | Classic cluster, dedicated access mode |

#### What types of compute does Databricks offer?

All-purpose clusters for interactive work, jobs compute created for one job run, SQL warehouses for SQL and BI, serverless compute for notebooks, jobs and pipelines, and instance pools to speed up classic cluster start-up.

#### What is serverless compute?

Compute that Databricks provisions and manages in its own account: it starts in seconds, scales automatically, is always on a current runtime with Photon, and is billed only while it works. You give up control of instance types and Spark configs, and code must be Spark Connect compatible.

#### What is a SQL warehouse?

Compute dedicated to SQL queries for Databricks SQL, BI tools and dashboards. Types: serverless (fast start, recommended), pro and classic. It scales out by adding clusters to absorb concurrency and uses Photon and intelligent workload management.

#### How do you size a SQL warehouse?

Pick a T-shirt size from query complexity and data volume (bigger means faster single queries), and set the maximum number of clusters for concurrency (more users at once). Watch query queuing and spilling in query history, and set auto-stop.

#### A notebook works on your cluster but fails as a serverless job. Why?

Probably because it uses something unsupported on serverless (Spark Connect): RDDs, `sparkContext`, `cache()`, most `spark.conf.set` calls, init scripts or libraries that need the JVM. Rewrite with DataFrame APIs, declare dependencies in the environment, and test on serverless before deploying.

<!-- challenge -->

Monday mornings, a dashboard is slow because 40 analysts open it at once; each query alone is fast. Which warehouse setting do you change?

<!-- solution -->

Raise the maximum number of clusters (scaling out for concurrency), not the T-shirt size, since single queries are already fast. Check query history for queuing to confirm.

<!-- takeaways -->

- Match compute to the workload: interactive, scheduled or SQL.
- Serverless starts fast and bills per use, but requires Spark Connect compatible code.
- Warehouse size is per-query speed; cluster count is concurrency.

<!-- unit: Classic clusters and access modes -->

<!-- goals -->

- Describe the driver and workers of a classic cluster.
- Choose standard or dedicated access mode for a workload.

<!-- concept -->

A classic cluster has one driver, which runs your program and plans the work, and workers whose executors process partitions in parallel. A single-node cluster puts everything on the driver, enough for small data or pandas work.

The access mode decides how a cluster is shared. Standard mode lets several users share it safely under Unity Catalog, at the cost of Spark Connect restrictions. Dedicated mode belongs to one user or group and supports more APIs, which some ML libraries and GPU work require.

<!-- example -->

```text
 driver  ── plans stages, collects results (keep big data off it)
   ├── worker 1: executor ── tasks on partitions 1..n
   ├── worker 2: executor ── tasks on partitions n+1..m
   └── worker 3: executor ── ...
```

#### What is the anatomy of a classic cluster?

One driver node that runs the main program, plans the work and collects results, plus worker nodes that run executors that process partitions. A single-node cluster runs everything on the driver, which is enough for small data and ML on one machine.

#### What is a single-node cluster good for?

Small data processing, pandas and scikit-learn work, and lightweight development. It has no workers, so Spark runs in local mode on the driver, which is cheap but doesn't scale.

#### What are access modes?

Settings that control isolation and governance on classic compute. Standard (formerly shared) lets several users share a cluster with Unity Catalog isolation, using Spark Connect. Dedicated (formerly single user) assigns the cluster to one user or group and supports more APIs, such as RDDs and some ML libraries.

#### What does the "standard" versus "dedicated" choice mean for ML workloads?

ML libraries that need direct access to the JVM or the `SparkContext`, or GPU training, usually require dedicated access mode or serverless with the right environment. Standard mode is better for shared SQL and DataFrame work.

#### What are GPU clusters used for?

Deep learning training and inference, and some GPU-accelerated libraries. They need an ML runtime with GPU drivers and are expensive, so they should auto-terminate quickly.

<!-- challenge -->

A data scientist's training script calls `spark.sparkContext` and fails on the team's shared cluster. What do you propose?

<!-- solution -->

Give them a dedicated (single user) cluster, or a serverless environment that supports their library, for the training work. The shared standard-mode cluster stays for SQL and DataFrame work.

<!-- takeaways -->

- The driver plans and collects; workers do the processing.
- Standard mode is for sharing under Unity Catalog; dedicated mode supports more APIs.
- Single-node clusters are cheap for small data; GPU clusters must terminate quickly.

<!-- unit: Scaling and cost controls -->

<!-- goals -->

- Configure autoscaling, auto-termination, pools and spot instances sensibly.
- Use cluster policies to keep a team's compute under control.

<!-- concept -->

Most wasted compute money comes from clusters that are too big or never stop. Autoscaling adds and removes workers with the load, auto-termination stops idle clusters, and pools keep warm VMs to cut start-up time. Spot instances make fault-tolerant workers much cheaper, as long as the driver stays on-demand.

Cluster policies make these choices the default: admins limit instance types and sizes, force auto-termination and require cost tags, so individual users can't forget them.

<!-- example -->

A policy fragment that every development cluster must follow:
```json
{
  "autotermination_minutes": {"type": "range", "maxValue": 30, "defaultValue": 20},
  "num_workers": {"type": "range", "maxValue": 4},
  "custom_tags.team": {"type": "fixed", "value": "data-eng"}
}
```

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

#### How do you make development cheaper for a team of ten engineers?

Use small or single-node clusters with policies and short auto-termination, serverless notebooks, shared dev data samples or shallow clones instead of full copies, local unit tests for most logic, development-mode bundles, and a budget alert per team.

<!-- challenge -->

A team's development spend doubled after five new engineers joined. Name three controls you put in place this week.

<!-- solution -->

A cluster policy with small maximum sizes and 20–30 minute auto-termination, serverless notebooks or a shared pool for quick starts, and a budget alert on the team's cost tag. Longer term, move most logic tests to local unit tests.

<!-- takeaways -->

- Idle and oversized clusters are the main waste; auto-termination fixes the first.
- Spot for workers, on-demand for the driver.
- Policies turn good settings into defaults for everyone.

<!-- unit: Libraries and troubleshooting -->

<!-- goals -->

- Install dependencies reproducibly on clusters and serverless.
- Find the cause of a slow or failing cluster.

<!-- concept -->

Dependencies can be attached to the cluster, installed per notebook with `%pip`, or declared per job task; serverless uses an environment specification. Pin versions so a rerun next month behaves the same. Init scripts run at start-up for system-level setup, but they slow start-up and are hard to debug.

When something goes wrong, the driver is the usual suspect for crashes (it runs out of memory when data is pulled onto it), and the Spark UI is the place to look for slowness: stage durations, skewed tasks, shuffle sizes and spill.

<!-- example -->

```python
# Pulls 50 million rows into driver memory: likely out-of-memory
pdf = spark.table("silver.events").toPandas()

# Keeps the work distributed and the result small
spark.table("silver.events").groupBy("event_date").count().toPandas()
```

#### How do you install libraries on a cluster?

As compute-scoped libraries (PyPI, Maven, wheels from volumes or workspace files), notebook-scoped with `%pip install`, or as job task dependencies. On serverless, you declare dependencies in the environment configuration. Pin versions for reproducibility.

#### What are init scripts?

Shell scripts that run on each node at start-up, used to install system packages or configure the environment. They should be stored in volumes or workspace files, not DBFS, and kept to a minimum because they slow start-up and complicate debugging.

#### What happens when the driver runs out of memory?

The notebook or job fails or restarts. Common causes: `collect()` or `toPandas()` on large data, broadcasting a table that is too large, large Python objects on the driver, or too many tasks tracked at once. Keep data in Spark, write results to tables, and size the driver appropriately.

#### Where do you look when a cluster is slow?

The Spark UI (jobs, stages, task durations, shuffle sizes, spill, skew), cluster metrics (CPU, memory, disk), driver logs, and the query profile for SQL. Compare the median and maximum task times in a stage to detect skew.

<!-- challenge -->

A job fails every few days with "driver not responding". The last cell calls `collect()` on the result to send it by email. What do you change?

<!-- solution -->

Write the result to a table (or a file in a volume) and email a link or a small summary instead of collecting all rows. If a summary is needed, aggregate in Spark first so only a few rows reach the driver.

<!-- takeaways -->

- Pin library versions; keep init scripts to a minimum.
- `collect()` and `toPandas()` on large data are the usual driver killers.
- Use the Spark UI to compare median and maximum task times.

### Delta Lake

<!-- unit: Transaction log and ACID -->

<!-- goals -->

- Explain how a folder of Parquet files plus a log becomes a transactional table.
- Distinguish managed and external tables.

<!-- concept -->

A Delta table is Parquet data files plus a `_delta_log/` folder. Each commit is a numbered JSON file listing the files it added and removed; the table at version N is the set of files valid after commit N. Writers write new files first and then race to create the next log entry, which is atomic, so readers never see half-written data.

There are no locks: concurrency is optimistic, and conflicts are detected at commit time. Whether Unity Catalog or you own the storage location decides if a table is managed or external.

<!-- example -->

```text
sales/
├── part-0001.parquet   added in v0
├── part-0002.parquet   added in v1
├── part-0003.parquet   added in v2 (replaces 0001)
└── _delta_log/
    ├── 00000000000000000000.json   add 0001
    ├── 00000000000000000001.json   add 0002
    └── 00000000000000000002.json   remove 0001, add 0003
Version 2 = {0002, 0003}
```

#### What is Delta Lake?

An open-source storage format that adds a transaction log to Parquet files. It provides ACID transactions, schema enforcement and evolution, time travel, `MERGE`, `UPDATE` and `DELETE`, and streaming reads and writes. It is the default table format on Databricks.

#### How does the Delta transaction log work?

Each table has a `_delta_log/` folder of ordered JSON commit files (`000…0.json`, `000…1.json`) listing the data files added and removed by each transaction, plus schema and metadata changes. Periodically a Parquet checkpoint summarizes the state so readers don't replay every commit. A table version is the set of files valid after a given commit.

#### How does Delta provide ACID guarantees on object storage?

Writers create new Parquet files, then try to commit by atomically writing the next numbered log entry. If two writers race, only one succeeds; the other checks for conflicts and retries or fails. Readers only see files referenced by committed log entries, so they never see partial writes.

#### What concurrency control does Delta use?

Optimistic concurrency control: transactions don't lock, they check at commit time whether a concurrent commit touched the same data. Appends rarely conflict; concurrent `UPDATE`/`MERGE` on the same files can raise `ConcurrentModificationException`. Partitioning, liquid clustering and row-level concurrency (with deletion vectors) reduce conflicts.

#### What is the difference between a managed and an external table?

A managed table's data lives in storage controlled by Unity Catalog; dropping the table deletes the data (after a retention period), and Databricks can optimize it automatically. An external table points to a path you manage in your own storage location; dropping it removes only the metadata.

#### What does `DESCRIBE DETAIL` show?

The table's format, location, number of files, size in bytes, partition or clustering columns, and properties. It is a quick check for the small-files problem.

#### What is `CONVERT TO DELTA`?

A command that turns an existing Parquet directory into a Delta table in place by writing a transaction log over the existing files, without copying data.

<!-- challenge -->

Two jobs run `MERGE` into the same table at the same time and one fails with `ConcurrentModificationException`. Give two ways to prevent it.

<!-- solution -->

Serialize the writers (one job, or max concurrent runs of 1 with queueing), or make them touch different files: cluster or partition by the column that separates their data and include it in the `MERGE` condition. Deletion vectors also enable row-level concurrency.

<!-- takeaways -->

- A Delta version is the set of files listed by the log up to that commit.
- The atomic log commit gives ACID on object storage.
- Concurrency is optimistic: conflicts appear at commit, not as locks.

<!-- unit: Schemas and constraints -->

<!-- goals -->

- Explain schema enforcement and how to allow evolution deliberately.
- Use constraints, generated and identity columns and table properties.

<!-- concept -->

Delta rejects writes that don't match the table schema; that is enforcement, and it protects downstream readers. When the schema should change, you allow it explicitly: `mergeSchema` on a write, `ALTER TABLE`, or schema evolution in `MERGE`.

Beyond types, tables can carry rules and metadata: `NOT NULL` and `CHECK` constraints (enforced), generated and identity columns, and table properties that switch on features like Change Data Feed. UniForm adds Iceberg metadata so other engines can read the same files.

<!-- example -->

```sql
CREATE TABLE silver.orders (
  order_id   BIGINT GENERATED ALWAYS AS IDENTITY,
  ordered_at TIMESTAMP NOT NULL,
  order_date DATE GENERATED ALWAYS AS (CAST(ordered_at AS DATE)),
  amount     DECIMAL(18,2),
  CONSTRAINT positive_amount CHECK (amount >= 0)
) TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true');
```

#### What is schema enforcement?

Delta rejects writes whose columns or types don't match the table schema, instead of silently corrupting the table. It protects downstream consumers from bad loads.

#### How does schema evolution work in Delta?

You allow it explicitly: `.option("mergeSchema", "true")` on a write adds new columns, and `ALTER TABLE` changes the schema. For `MERGE`, `WITH SCHEMA EVOLUTION` (or the automatic merge setting) lets new source columns be added. Type widening allows some type changes, such as `int` to `bigint`, without rewriting data.

#### What constraints does Delta support?

`NOT NULL` and `CHECK` constraints, which are enforced: a write that violates them fails. Primary and foreign keys can be declared in Unity Catalog, but they are informational (not enforced), used by tools and the optimizer.

#### What are generated and identity columns?

A generated column is computed from other columns (`GENERATED ALWAYS AS (CAST(ts AS DATE))`). An identity column (`GENERATED ALWAYS AS IDENTITY`) assigns unique, increasing (not necessarily consecutive) numbers, which is useful for surrogate keys.

#### What are table properties used for in Delta?

Settings stored with the table, such as `delta.enableChangeDataFeed`, `delta.logRetentionDuration`, `delta.deletedFileRetentionDuration`, `delta.enableDeletionVectors` or `delta.appendOnly`, plus custom key-value metadata. They are set with `TBLPROPERTIES` and shown by `SHOW TBLPROPERTIES`.

#### What is UniForm?

Universal Format: a Delta table option that also writes Iceberg (and Hudi) metadata, so engines that read Iceberg can read the same files without copying data.

<!-- challenge -->

A source adds a `discount` column, and the nightly append into `silver.orders` now fails. Should you turn on `mergeSchema` permanently?

<!-- solution -->

Not blindly. Add the column on purpose (`ALTER TABLE ... ADD COLUMN discount ...` or a one-off `mergeSchema` write) after checking its meaning and type. Permanent automatic evolution lets any upstream mistake reshape a trusted silver table.

<!-- takeaways -->

- Enforcement is the default; evolution should be a deliberate choice.
- `CHECK` and `NOT NULL` are enforced; primary and foreign keys are informational.
- Table properties switch features like CDF and retention on and off.

<!-- unit: Time travel, restore and retention -->

<!-- goals -->

- Query and restore earlier versions of a table.
- Explain how `VACUUM` and retention settings limit time travel.

<!-- concept -->

Because old files stay in storage until removed, every Delta version can be read again: that is time travel, and `RESTORE` makes an old version current with a new commit. Clones copy a table at a point in time, either fully (deep) or as metadata only (shallow).

Time travel isn't free storage forever. `VACUUM` deletes unreferenced files older than the retention (7 days by default), and the log keeps 30 days of history. Once files are vacuumed, versions that needed them can no longer be read.

<!-- example -->

```sql
DESCRIBE HISTORY gold.revenue;                 -- find the bad commit, say v57
SELECT * FROM gold.revenue VERSION AS OF 56;   -- check the good version
RESTORE TABLE gold.revenue TO VERSION AS OF 56;
```

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

#### What is the difference between log retention and deleted-file retention?

`delta.logRetentionDuration` (30 days by default) controls how long commit history is kept; `delta.deletedFileRetentionDuration` (7 days by default) controls how long `VACUUM` keeps unreferenced data files. Time travel needs both the log entries and the data files.

#### What is the difference between a deep clone and a shallow clone?

A deep clone copies the data files and metadata into an independent table. A shallow clone copies only the metadata and points to the source's files, so it is instant and cheap, which is useful for testing changes on production-sized data. Both have their own history from the clone point.

#### Someone dropped columns from a gold table by mistake an hour ago. How do you recover?

Check `DESCRIBE HISTORY` for the version before the change and `RESTORE TABLE … TO VERSION AS OF` that version, or `SELECT` from it to rebuild. Then review permissions so that only the pipeline's service principal can modify gold tables.

<!-- challenge -->

Audit asks you to reproduce a report exactly as it was 60 days ago. With default settings, can you? What would you change for the future?

<!-- solution -->

Probably not: deleted files are vacuumed after 7 days and the log keeps 30 days. For the future, raise `delta.logRetentionDuration` and `delta.deletedFileRetentionDuration` on that table, or snapshot the report data (for example a deep clone or a dated table) at each publication.

<!-- takeaways -->

- Time travel reads old versions; `RESTORE` makes one current again.
- `VACUUM` plus retention settings define how far back you can go.
- Shallow clones are instant copies for testing on real data.

<!-- unit: Changing data: MERGE, UPDATE and DELETE -->

<!-- goals -->

- Write a correct `MERGE` and fix its common errors.
- Explain copy-on-write, deletion vectors and Change Data Feed.

<!-- concept -->

Parquet files are immutable, so changing a row means writing new files. Without deletion vectors, `UPDATE`, `DELETE` and `MERGE` rewrite every file containing a touched row (copy-on-write). Deletion vectors instead mark rows as deleted in a small side file and rewrite later.

`MERGE` is the workhorse for upserts, CDC and deduplication. Its two usual problems are ambiguous sources (several rows per key) and slow scans of the whole target. For replacing a whole slice, `replaceWhere` is simpler than `MERGE`. Change Data Feed lets downstream jobs read only the rows that changed.

<!-- example -->

Deduplicate the source, then merge:
```sql
MERGE INTO silver.customers t
USING (
  SELECT * FROM updates
  QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1
) s
ON t.customer_id = s.customer_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

#### How does Delta handle `UPDATE` and `DELETE` without deletion vectors?

It finds the files containing matching rows, rewrites those files without the deleted rows (or with updated values), and commits a transaction that removes the old files and adds the new ones. That is copy-on-write: cheap reads, expensive writes on large files.

#### What are deletion vectors?

A storage optimization where `DELETE`, `UPDATE` and `MERGE` mark rows as deleted in a small side file instead of rewriting whole Parquet files. Writes become much faster; the files are physically rewritten later by `OPTIMIZE` or `REORG TABLE … APPLY (PURGE)`.

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

#### What is the difference between `overwrite` mode and `replaceWhere`?

`mode("overwrite")` replaces the whole table (as a new version, so time travel still works). `replaceWhere` replaces only the rows matching a predicate. Dynamic partition overwrite (`partitionOverwriteMode=dynamic`) replaces only the partitions present in the new data.

#### What is Change Data Feed?

A table option (`delta.enableChangeDataFeed = true`) that records row-level changes (insert, update_preimage, update_postimage, delete) with the commit version and timestamp. Downstream jobs read only what changed:

```sql
SELECT * FROM table_changes('silver.customers', 120);
```

#### How do you deliver a GDPR deletion request on a Delta lakehouse?

Delete the person's rows with `DELETE` or `MERGE` in every layer (bronze included), then run `VACUUM` so the old files containing them are physically removed after the retention period. Pseudonymizing identifiers early in the pipeline limits how many tables hold personal data.

<!-- challenge -->

A daily `MERGE` of 50,000 changed rows into a 3-billion-row table takes 40 minutes. The changes are always from the last 3 days. What do you try first?

<!-- solution -->

Add the date range to the `ON` condition (for example `t.event_date >= current_date() - 3`) so Delta prunes most target files, and cluster the table by the date and key. Enable deletion vectors so matched files aren't fully rewritten.

<!-- takeaways -->

- Without deletion vectors, any row change rewrites whole files.
- Deduplicate the `MERGE` source; prune the target with extra conditions.
- CDF gives downstream jobs only the changed rows.

<!-- unit: File layout and data skipping -->

<!-- goals -->

- Diagnose and fix the small-files problem.
- Choose liquid clustering over partitioning and Z-ordering for new tables.

<!-- concept -->

Read speed depends on how many files a query opens and how many it can skip. Many small files add overhead, so `OPTIMIZE`, optimized writes and auto compaction combine them. Delta keeps min/max statistics per file, so a filter can skip files whose range can't match; that only works well if similar values sit in the same files.

Clustering puts them there. Partitioning splits by directory and suits only huge tables on low-cardinality columns. Z-ordering clusters several columns but must be rerun. Liquid clustering (`CLUSTER BY`) clusters incrementally, lets you change keys, and is the default choice now.

<!-- example -->

```sql
DESCRIBE DETAIL silver.events;            -- numFiles: 480000, sizeInBytes: 200 GB → ~400 KB per file
ALTER TABLE silver.events CLUSTER BY (event_date, user_id);
OPTIMIZE silver.events;                   -- compacts and clusters
```

#### What is the small-files problem?

Many tiny files make reads slow (each file has open and metadata overhead, and statistics are less useful) and slow down the transaction log. Streaming and frequent small appends cause it. Fixes: `OPTIMIZE`, auto compaction and optimized writes, and fewer, larger batches.

#### What does `OPTIMIZE` do?

It compacts small files into larger ones (around 1 GB by default), which speeds up reads. With Z-ordering or liquid clustering, it also rewrites data so related values sit in the same files.

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

#### Your Delta table has 500,000 small files. What do you do?

Run `OPTIMIZE` (with liquid clustering on the main filter columns), enable optimized writes and auto compaction or predictive optimization, then fix the cause: batch micro-appends, avoid over-partitioning, and use `availableNow` triggers rather than very frequent tiny streams. Run `VACUUM` afterwards to remove the old files.

<!-- challenge -->

A table partitioned by `customer_id` (200,000 customers) is slow for every query. What happened, and what do you do?

<!-- solution -->

High-cardinality partitioning created hundreds of thousands of tiny directories and files. Recreate the table without partitions, with `CLUSTER BY (customer_id)` (plus the date if queries filter on it), run `OPTIMIZE`, then `VACUUM` the old files.

<!-- takeaways -->

- Aim for few, large files; `DESCRIBE DETAIL` shows the file count.
- Data skipping needs clustered data to be effective.
- Use liquid clustering for new tables; partition only huge tables on low-cardinality columns.

<!-- stage: Building pipelines -->

### Ingestion

<!-- unit: Choosing an ingestion path -->

<!-- goals -->

- Pick the right tool for files, databases, SaaS sources and streams.
- Load a relational table in parallel and incrementally.

<!-- concept -->

How data arrives decides the tool. Files landing in storage go through Auto Loader (or `COPY INTO` for modest batch loads, or `read_files` in SQL). SaaS apps and databases can use Lakeflow Connect's managed connectors; otherwise a JDBC read does the job. Event streams come from Kafka or similar through Structured Streaming.

Whatever the source, the pattern is the same: land the data raw in bronze, incrementally, with enough metadata to know where each row came from.

<!-- example -->

| Source | First choice |
|---|---|
| Files in S3 / ADLS / volumes | Auto Loader (`cloudFiles`) |
| A few thousand batch files, SQL only | `COPY INTO` |
| Salesforce, SQL Server, Workday... | Lakeflow Connect |
| PostgreSQL without a connector | Spark JDBC, partitioned, by watermark |
| Kafka, Kinesis, Event Hubs | Structured Streaming |

#### What options exist for loading data into Databricks?

Auto Loader for files arriving in cloud storage, `COPY INTO` for idempotent batch file loads, Lakeflow Connect managed connectors (Salesforce, Workday, SQL Server, Google Analytics and others), Structured Streaming from Kafka, Kinesis or Event Hubs, Lakehouse Federation for querying in place, partner tools (Fivetran and others) and file uploads to volumes.

#### What is Lakeflow Connect?

Managed, serverless ingestion connectors for SaaS applications and databases. They handle incremental extraction (often CDC) and land the data in Unity Catalog tables through a pipeline, without writing extraction code.

#### How do you load data from a relational database without Lakeflow Connect?

With the Spark JDBC reader, partitioning the read with `partitionColumn`, `lowerBound`, `upperBound` and `numPartitions` so it runs in parallel, and loading incrementally by a watermark column (for example `updated_at`). Store credentials in secrets.

#### How do you ingest from Kafka?

With the Structured Streaming Kafka source, which reads `key`, `value`, `topic`, `partition`, `offset` and `timestamp`. Parse `value` (JSON, Avro with a schema registry, Protobuf), write raw records to bronze, and keep the checkpoint per query.

#### What is `COPY INTO`?

A SQL command that loads files from a path into a Delta table and is idempotent: files already loaded are skipped. It suits scheduled batch loads of thousands of files; Auto Loader is preferred for millions of files or continuous ingestion.

```sql
COPY INTO bronze.customers
FROM '/Volumes/raw/landing/customers/'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');
```

#### What is `read_files`?

A SQL table-valued function that reads files (CSV, JSON, Parquet, Avro, XML, text) from a path or volume with schema inference. With `STREAM read_files(...)` in a streaming table, it uses Auto Loader underneath.

<!-- challenge -->

You must load a 400-million-row PostgreSQL table every night, but only about 1% of rows change. Sketch the read.

<!-- solution -->

Read only rows with `updated_at` greater than the last loaded watermark (stored in a control table or derived from the target's maximum), with a JDBC read partitioned on a numeric key (`partitionColumn`, bounds, `numPartitions`). `MERGE` the result into the target by primary key. Deletes need a separate approach, such as CDC or a periodic key comparison.

<!-- takeaways -->

- Choose the tool by how data arrives: files, databases, SaaS or streams.
- Load incrementally; full reloads don't scale.
- Bronze keeps raw data plus where it came from.

<!-- unit: Auto Loader and streaming bookkeeping -->

<!-- goals -->

- Explain how Auto Loader loads each file exactly once.
- Run streaming ingestion on a batch schedule with `availableNow`.

<!-- concept -->

Auto Loader is a streaming source that discovers new files, by listing the directory or through storage notifications. It records processed files in the stream's checkpoint, so restarts never load a file twice and late files are still picked up.

Streaming doesn't mean always-on. With `trigger(availableNow=True)` the query processes everything new and stops, which gives the bookkeeping of streaming at the cost of a scheduled job. The hidden `_metadata` column records which file each row came from.

<!-- example -->

```python
(spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("cloudFiles.schemaLocation", "/Volumes/raw/_schemas/orders")
    .load("/Volumes/raw/landing/orders/")
    .select("*", "_metadata.file_path", "_metadata.file_modification_time")
  .writeStream
    .option("checkpointLocation", "/Volumes/raw/_checkpoints/orders")
    .trigger(availableNow=True)          # run as a daily batch
    .toTable("bronze.orders"))
```

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

#### What is a streaming checkpoint?

A storage location where a streaming query records its progress (offsets or processed files) and state. It gives exactly-once processing across restarts. Each query needs its own checkpoint, and deleting it makes the query start over.

#### What does `trigger(availableNow=True)` do?

It makes a streaming query process everything available at start (in several batches respecting rate limits), then stop. It gives the incremental bookkeeping of streaming with the cost profile of a scheduled batch job.

#### What is the `_metadata` column?

A hidden column available when reading files, with `file_path`, `file_name`, `file_size` and `file_modification_time`. It replaces `input_file_name()` (not supported in Unity Catalog) to record the source file of each row.

#### How do you handle late-arriving files?

Auto Loader picks up any new file whenever it arrives, regardless of its date, so the load itself is safe. Downstream, use `MERGE` keyed on business keys, or reprocess the affected dates with `replaceWhere`, so late data corrects earlier results.

<!-- challenge -->

Someone deletes the checkpoint folder of a bronze ingestion stream "to clean up". What happens on the next run, and how do you recover?

<!-- solution -->

The stream starts over and reloads every file in the landing path, duplicating bronze. Recover by restoring the bronze table to the version before the run (or deduplicating by file path), then let the new checkpoint continue. Protect checkpoints with permissions.

<!-- takeaways -->

- The checkpoint is what makes ingestion exactly-once; never share or delete it.
- `availableNow` gives streaming bookkeeping on a batch schedule.
- Record `_metadata.file_path` for traceability.

<!-- unit: Schema inference and drift -->

<!-- goals -->

- Control schema inference in production loads.
- Handle new or malformed columns without losing data.

<!-- concept -->

Sources change without warning. Inferring the schema each run is slow and unstable, so production loads either declare a schema or let Auto Loader manage it: it stores the inferred schema, stops when a new column appears, and continues with the evolved schema after a restart.

Schema hints pin the types that matter, and values that don't fit go to `_rescued_data` instead of being dropped. Watching that column is an early warning that the source changed.

<!-- example -->

```python
.option("cloudFiles.schemaHints", "amount DECIMAL(18,2), event_ts TIMESTAMP")
.option("cloudFiles.schemaEvolutionMode", "addNewColumns")
# Later: SELECT count(*) FROM bronze.orders WHERE _rescued_data IS NOT NULL
```

#### Why should you avoid `inferSchema` in production?

Inference requires an extra pass over the data, can infer different types from different files, and silently changes when the source changes. Declare schemas (data contracts) for production loads, or let Auto Loader manage inference with schema hints.

#### How does Auto Loader handle schema changes?

It stores the inferred schema in the schema location. With the default `addNewColumns` mode, a new column stops the stream, updates the schema and the stream continues after a restart. Data that doesn't fit the schema (wrong type, unexpected column) goes into the `_rescued_data` column instead of being lost.

#### What is the rescued data column?

A JSON string column (`_rescued_data`) where Auto Loader puts values that couldn't be parsed into the schema. Monitoring it reveals upstream format changes.

#### What are schema hints in Auto Loader?

Explicit types for some columns (`cloudFiles.schemaHints = "amount DECIMAL(18,2), event_ts TIMESTAMP"`) that override inference while the rest of the schema is still inferred.

#### A streaming query fails after a schema change in the source. How do you handle it?

With Auto Loader in `addNewColumns` mode, restart the stream so it picks up the new schema. For incompatible changes, update the target schema (or use the rescued data column), and if the logic changed, start a new checkpoint with a clear backfill plan. Add alerting on rescued data.

<!-- challenge -->

After a vendor update, `amount` arrives as `"12,50"` (comma decimal) in some files. What happens with a hinted `DECIMAL` type, and how do you notice?

<!-- solution -->

Those values don't parse, so `amount` is null and the raw value goes into `_rescued_data`. An alert on the share of rows with rescued data catches it; then fix the parsing in silver (replace the comma, cast) and reprocess the affected files.

<!-- takeaways -->

- Declare or hint the important types; don't rely on fresh inference.
- `addNewColumns` stops, evolves and continues after restart.
- Monitor `_rescued_data` to catch upstream changes.

### Medallion architecture and modeling

<!-- unit: Layers and their contracts -->

<!-- goals -->

- Describe what belongs in bronze, silver and gold.
- Justify keeping a raw layer, and adapt the layers to the project.

<!-- concept -->

The medallion architecture organizes a lakehouse in layers of increasing quality. Bronze keeps what the source sent, so you can reprocess and audit. Silver is the cleaned, deduplicated, validated version of each entity, the one everyone trusts. Gold shapes data for consumption: star schemas, aggregates and features.

The value is in the contracts between layers, not in the number three. Small projects merge layers; others add a landing zone or a serving layer.

<!-- example -->

| Layer | Example table | Contract |
|---|---|---|
| Bronze | `bronze.orders` | Raw rows + `file_path`, load time; append-only |
| Silver | `silver.orders` | Typed, one row per `order_id`, bad rows quarantined |
| Gold | `gold.fct_daily_sales` | Grain: one row per day and store; business definitions applied |

#### What is the medallion architecture?

A layered way to organize lakehouse data: bronze holds raw data as received (append-only, with load metadata), silver holds cleaned, conformed, deduplicated and validated data, and gold holds business-level aggregates and dimensional models ready for BI and ML. Quality and structure increase layer by layer.

#### Why keep a raw bronze layer?

So you can reprocess history when logic changes or bugs are found, audit what the source actually sent, and decouple ingestion from transformation. Bronze should be cheap to keep and faithful to the source.

#### Should bronze be a Delta table or raw files?

Usually raw files stay in a landing zone (or volume) and bronze is a Delta table loaded from them with minimal changes plus load metadata. Delta in bronze gives transactions, schema tracking and fast reprocessing; keeping the original files gives an exact copy for audits.

#### What belongs in silver?

Typed and renamed columns, deduplication, standardized values (dates, codes, addresses), joins to reference data, data quality checks with quarantine of bad rows, and history (SCD Type 2) when needed. Silver is the single trusted version of each entity.

#### What belongs in gold?

Data shaped for consumption: star schemas (facts and dimensions), aggregates, feature tables and data products, with business definitions applied. Gold tables are usually smaller and optimized for read performance.

#### Is the medallion architecture always three layers?

No. It is a convention, not a rule. Small projects may merge silver and gold; others add a landing zone before bronze or a platinum/serving layer after gold. What matters is that each layer has a clear contract.

<!-- challenge -->

A colleague proposes cleaning data as it is loaded and skipping bronze "to save storage". What do you lose?

<!-- solution -->

The ability to reprocess history when the cleaning logic changes or has a bug, and the evidence of what the source actually sent. Bronze storage is cheap compared with re-extracting data that the source may no longer have.

<!-- takeaways -->

- Bronze is faithful, silver is trusted, gold is shaped for use.
- Each layer is a contract about grain, quality and ownership.
- Adapt the number of layers; keep the contracts.

<!-- unit: Modeling patterns -->

<!-- goals -->

- Implement SCD Type 2 and record quarantine on Delta.
- Organize catalogs and gold tables for BI and ML.

<!-- concept -->

Silver is where history and quality are handled. SCD Type 2 keeps every version of an entity with validity dates, which a single `MERGE` can maintain. Quarantine sends failing rows, with their reasons, to a side table so the pipeline continues and someone can fix the source.

Gold then serves two audiences from the same silver data: star schemas for BI and feature tables for ML. Catalogs usually separate environments, and schemas separate layers, so permissions follow the environment.

<!-- example -->

SCD Type 2 rows for one customer:
| customer_id | city | valid_from | valid_to | is_current |
|---|---|---|---|---|
| 42 | Bogotá | 2024-01-10 | 2026-03-02 | false |
| 42 | Medellín | 2026-03-02 | null | true |

#### How do you implement SCD Type 2 on Delta?

With `MERGE`: close the current row (set `valid_to` and `is_current = false`) when tracked attributes change, and insert the new version. A common trick is to merge a union of the updates with a null merge key for changed rows, so one `MERGE` both closes and inserts. Declarative pipelines do it with `AUTO CDC … STORED AS SCD TYPE 2`.

#### How do you quarantine bad records?

Validate rows against rules in silver, write failing rows with the reasons to a quarantine table, and continue with the valid ones. Monitor the quarantine rate and alert on spikes. Expectations with `DROP ROW` plus a separate inverse query achieve the same in declarative pipelines.

#### Should you use one catalog per environment or per layer?

A common pattern is one catalog per environment (`dev`, `staging`, `prod`) with schemas per layer (`bronze`, `silver`, `gold`), because environments need different permissions and storage. Some teams prefer catalogs per domain or business unit. Consistency matters more than the choice.

#### What is a data product in the Databricks context?

A curated, documented and governed set of tables (usually gold) owned by a team, with quality checks, a clear interface and access granted through Unity Catalog, possibly shared through Delta Sharing.

#### How do you model gold for both BI and ML?

Star schemas (facts at a declared grain with conformed dimensions) for BI, and feature tables keyed by entity and time for ML, both built from the same silver tables so numbers agree.

<!-- challenge -->

Finance reports revenue by customer region and wants last year's numbers to stay as they were when customers move. Which dimension type do you use, and how does the fact table join to it?

<!-- solution -->

SCD Type 2 on the customer dimension, with a surrogate key per version. The fact table stores the surrogate key valid at the time of the sale (or joins on the natural key with `sale_date BETWEEN valid_from AND valid_to`), so old sales keep their old region.

<!-- takeaways -->

- SCD2 keeps history with validity ranges; one `MERGE` can maintain it.
- Quarantine bad rows with reasons instead of failing or silently dropping.
- Build BI and ML gold from the same silver so numbers agree.

### Lakeflow Declarative Pipelines

<!-- unit: The declarative model -->

<!-- goals -->

- Explain what a declarative pipeline manages for you.
- Choose between a streaming table and a materialized view.

<!-- concept -->

In a declarative pipeline you define the tables you want and the queries that produce them; the engine works out the order, runs them, retries failures and manages compute. You stop writing orchestration and checkpoint code.

Two kinds of datasets cover most needs. A streaming table processes each new input row once, which suits ingestion and append-only data. A materialized view recomputes (incrementally when possible) so it always matches its sources, which suits joins and aggregations. Flows let several sources feed one table.

<!-- example -->

```sql
CREATE OR REFRESH STREAMING TABLE silver_orders
AS SELECT * FROM STREAM bronze_orders WHERE order_id IS NOT NULL;

CREATE OR REFRESH MATERIALIZED VIEW gold_sales_by_day
AS SELECT order_date, sum(amount) AS sales FROM silver_orders GROUP BY order_date;
```

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

#### How do you write a declarative pipeline in Python?

With the `pipelines` module (formerly `dlt`): decorated functions return DataFrames, and the decorators declare tables and expectations.

```python
from pyspark import pipelines as dp

@dp.table(comment="Cleaned orders")
@dp.expect_or_drop("valid_amount", "amount >= 0")
def silver_orders():
    return spark.readStream.table("bronze_orders").dropDuplicates(["order_id"])
```

#### What is a flow in a declarative pipeline?

A unit of processing that writes into a target table. A streaming table can have several append flows (for example one per source region), which lets you add sources without a full refresh.

#### Where do pipeline tables live?

In the Unity Catalog catalog and schema configured for the pipeline (and other schemas if fully qualified names are used). They are ordinary Delta tables for readers, but only the pipeline should write to them.

#### When would you not use declarative pipelines?

When you need fine-grained control over every step, logic that doesn't fit the declarative model (complex procedural code, calls to external systems per batch), or portability to plain Spark jobs. Many teams use plain jobs with Delta and `MERGE` and get the same results with more code.

<!-- challenge -->

Orders arrive append-only; refunds update old orders. You need daily revenue net of refunds. Which tables are streaming tables, and which is a materialized view?

<!-- solution -->

Ingest orders and refunds as streaming tables (each event processed once). Compute net daily revenue as a materialized view joining both, because a refund changes the result for a past day, which a materialized view recomputes and a streaming table would not.

<!-- takeaways -->

- Declare tables and queries; the engine handles order, retries and compute.
- Streaming tables process each row once; materialized views stay correct as sources change.
- Use flows to add sources to a table without a full refresh.

<!-- unit: Quality, CDC and running pipelines -->

<!-- goals -->

- Add expectations and CDC handling to a pipeline.
- Run, monitor and refresh a pipeline safely.

<!-- concept -->

Expectations declare quality rules on a table, with a policy for violations: record them, drop the row or fail the update. `AUTO CDC` applies a change feed with keys and sequencing, handling out-of-order events and SCD Type 2 history without `MERGE` code.

Operationally, triggered mode runs and stops; continuous mode stays up. Development mode iterates quickly, the event log records everything, and a full refresh rebuilds a table from scratch, which is powerful but costly and risky when the source no longer keeps its history.

<!-- example -->

```sql
CREATE OR REFRESH STREAMING TABLE silver_customers;

CREATE FLOW customers_cdc AS AUTO CDC INTO silver_customers
FROM STREAM bronze_customer_changes
KEYS (customer_id)
SEQUENCE BY change_ts
APPLY AS DELETE WHEN op = 'D'
STORED AS SCD TYPE 2;
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

#### What is a full refresh of a pipeline table?

Truncating the table and reprocessing all source data from the beginning, including resetting streaming checkpoints. It is needed after logic changes that must apply to history, but can be costly and can lose data if the source retention is shorter than the history.

#### How is a declarative pipeline billed?

Through pipeline compute (serverless or classic) at the pipeline product tier (Core, Pro, Advanced), with higher tiers adding CDC and expectations. Serverless pipelines are billed per use and are the default.

<!-- challenge -->

A teammate wants to run a full refresh on the bronze table because of a parsing fix. The source Kafka topic keeps 7 days of data. What do you warn them about?

<!-- solution -->

A full refresh truncates the table and replays the source from the start, but Kafka only has 7 days: older history would be lost. Fix the parsing in silver instead, or reprocess only recent data, and keep bronze (or the raw files) as the long-term copy.

<!-- takeaways -->

- Expectations make quality rules visible and enforceable.
- `AUTO CDC` replaces hand-written `MERGE` for change feeds.
- Full refreshes replay sources; check source retention first.

### Jobs and orchestration

<!-- unit: Jobs, tasks and triggers -->

<!-- goals -->

- Build a job as a DAG of tasks with the right compute and trigger.
- Decide when Lakeflow Jobs is enough and when to use Airflow.

<!-- concept -->

A job is a DAG of tasks: notebooks, scripts, SQL, dbt, pipelines or other jobs, each with dependencies, compute, retries and timeouts. Triggers start it on a schedule, when files arrive or when a source table updates. Control-flow tasks add loops (For each) and branches (If/else).

If the workflow lives mostly in Databricks, Jobs is simpler and cheaper than an external orchestrator. Airflow earns its place when the DAG spans many systems.

<!-- example -->

```text
ingest_orders ─┐
               ├─► build_silver ─► check_quality ─► if rows > 0 ─► publish_gold
ingest_stores ─┘                                      └── else ──► notify
```

#### What are Lakeflow Jobs (formerly Workflows)?

Databricks' built-in orchestrator. A job is a DAG of tasks (notebooks, Python scripts, wheels, SQL, dbt, pipelines, JARs, other jobs) with dependencies, schedules or triggers, parameters, retries, timeouts, notifications and compute settings.

#### What task types can a job have?

Notebook, Python script, Python wheel, SQL (query, file, dashboard or alert), dbt, pipeline, JAR, Spark Submit, Run Job (another job), If/else condition and For each (loop over values).

#### What triggers can start a job?

A cron schedule, a file arrival in a storage location, a table update (when a source table changes), continuous mode (restart as soon as it ends), the API or CLI, or a manual run.

#### What is the difference between job compute and running tasks on a shared cluster?

Each task can use its own job cluster, share a job cluster with other tasks of the same run, use serverless compute, or use an existing all-purpose cluster. Shared job clusters avoid repeated start-up; serverless removes start-up altogether.

#### What does the For each task do?

It runs a nested task once per item of a list (for example a list of countries or dates), with a configurable concurrency, so you don't have to define one task per item.

#### What is the If/else condition task used for?

Branching a job based on a value, such as a task value or parameter: for example, skip the publish step when a data quality task reports zero valid rows.

#### Should you orchestrate Databricks with Airflow or with Jobs?

Jobs is enough when the workflow lives mainly in Databricks, and it is cheaper and simpler. Airflow (or Dagster, Prefect) makes sense when the DAG spans many systems, when the company already standardizes on it, or for complex cross-team dependencies. Airflow's Databricks provider can trigger jobs and wait for them.

<!-- challenge -->

A job should run whenever the upstream team's `silver.orders` table changes, but not more than once every 30 minutes. How do you trigger it?

<!-- solution -->

Use a table update trigger on `silver.orders` with a minimum time between triggers of 30 minutes (or wait-after-last-change), and set maximum concurrent runs to 1 with queueing.

<!-- takeaways -->

- A job is a DAG of tasks with their own compute, retries and timeouts.
- Trigger on schedules, file arrival or table updates.
- Use Jobs for Databricks-centric workflows; Airflow for cross-system ones.

<!-- unit: Reliable runs: parameters, idempotency and backfills -->

<!-- goals -->

- Make a job safe to rerun and to backfill.
- Pass parameters and small values between tasks.

<!-- concept -->

A reliable job gives the same result whether it runs once or three times. That means writes that replace or merge instead of appending, and a processing date that comes from a parameter rather than the clock. Dynamic references such as `{{job.start_time.iso_date}}` supply that context.

With idempotent tasks, recovery is easy: repair a run to rerun only the failed tasks, limit concurrency so runs don't overlap, and backfill by looping over dates.

<!-- example -->

```python
# Task parameter: process_date = {{job.start_time.iso_date}}
process_date = dbutils.widgets.get("process_date")
(daily_df.write.mode("overwrite")
   .option("replaceWhere", f"event_date = '{process_date}'")   # rerun-safe
   .saveAsTable("silver.events"))
dbutils.jobs.taskValues.set("row_count", daily_df.count())
```

#### What are job parameters and dynamic value references?

Parameters defined at job level and passed to every task, overridable at run time. Dynamic value references such as `{{job.start_time.iso_date}}` or `{{job.run_id}}` inject run context, which is useful for idempotent, date-driven processing.

#### How do you pass values between tasks?

Small values with task values (`dbutils.jobs.taskValues.set` in one task and `get` in a later one, or dynamic references like `{{tasks.ingest.values.row_count}}` in task parameters). Data itself should be passed through tables, not task values.

#### How do you make a Databricks job idempotent?

Write with `MERGE` or `replaceWhere`/dynamic partition overwrite for the processed date instead of blind appends, base the processing date on a parameter rather than the wall clock, use streaming checkpoints for incremental ingestion, and make side effects (notifications, exports) safe to repeat.

#### How do you rerun only the failed part of a job?

With "Repair run", which reruns the failed tasks and their downstream dependencies, reusing successful upstream results, optionally with new parameters.

#### How do you limit concurrent runs of a job?

With the maximum concurrent runs setting (usually 1 for jobs that write the same tables) and the queueing option, so a new trigger waits instead of being skipped or running in parallel.

#### How do you get alerted when a job fails or is slow?

Configure notifications (email, Slack, Teams, PagerDuty, webhooks) on start, success, failure and duration thresholds, and set a timeout and maximum concurrent runs. System tables on job runs let you build longer-term reliability dashboards.

#### How do you run a job for a backfill of many dates?

Parameterize the job by date and trigger it per date (through the API, CLI or a For each task over a list of dates), keeping writes idempotent, and limit concurrency so the backfill doesn't starve production workloads.

#### A daily job writes duplicates every time it's rerun. What do you change?

Replace the append with an idempotent write: a `MERGE` on the business key, or `replaceWhere` on the processing date. Derive the date from a job parameter, and add a uniqueness check on the target.

<!-- challenge -->

You must backfill 2 years of daily data through a job that normally processes one day. How do you run it without disturbing production?

<!-- solution -->

Make sure the job is idempotent by date, then run a For each task (or API calls) over the 730 dates with limited concurrency, on separate job compute, possibly outside business hours. Check row counts per date afterwards.

<!-- takeaways -->

- Idempotent writes (`MERGE`, `replaceWhere`) make reruns safe.
- Take the processing date from a parameter, never the wall clock.
- Repair runs rerun only what failed.

<!-- stage: Governing data -->

### Unity Catalog and governance

<!-- unit: Object model and storage -->

<!-- goals -->

- Name the Unity Catalog hierarchy and address objects with three-level names.
- Explain how storage credentials, external locations and volumes govern files.

<!-- concept -->

Unity Catalog is one governance layer for all workspaces in a region. Everything sits in a hierarchy: metastore, catalog, schema, then tables, views, volumes, functions and models, addressed as `catalog.schema.object`.

Access to cloud storage is governed too. A storage credential wraps a cloud identity, an external location ties it to a path, and volumes expose files under governed paths. Older workspaces still have a Hive metastore, which you migrate into Unity Catalog.

<!-- example -->

```text
metastore (eu-west-1)
└── catalog: prod
    ├── schema: bronze ── table: orders
    ├── schema: gold   ── table: fct_sales, view: v_sales_eu
    └── schema: raw    ── volume: landing  → /Volumes/prod/raw/landing/
```

#### What is Unity Catalog?

Databricks' unified governance layer for data and AI assets across workspaces: one place to define access control, auditing, lineage, data discovery and sharing for tables, views, volumes, functions and models. It has also been released as open source.

#### What is the Unity Catalog object hierarchy?

Metastore (one per region) → catalog → schema (database) → tables, views, materialized views, volumes, functions and models. Objects are addressed with a three-level name: `catalog.schema.table`.

#### What is a volume?

A Unity Catalog object that governs access to non-tabular files (CSV, JSON, images, PDFs, wheels) in cloud storage, addressed as `/Volumes/catalog/schema/volume/path`. Managed volumes live in Unity Catalog-managed storage; external volumes map to an existing storage path.

#### What are storage credentials and external locations?

A storage credential wraps a cloud identity (an AWS IAM role, an Azure managed identity) that can access storage. An external location combines a storage path with a credential, and grants on it control who can create external tables or volumes there.

#### What is the information schema in Unity Catalog?

A set of standard SQL views in each catalog (`information_schema.tables`, `columns`, `table_privileges` and others) describing the objects and permissions, useful for documentation and audits.

#### What is the legacy Hive metastore, and how do you migrate from it?

The per-workspace metastore that predates Unity Catalog, with workspace-local permissions. Migration consists of creating a Unity Catalog metastore, upgrading tables (`SYNC` for external tables, `CREATE TABLE … AS SELECT` or deep clone for managed ones) and updating code to three-level names. The UCX tool automates much of the assessment and migration.

<!-- challenge -->

A notebook reads `hive_metastore.sales.orders` and writes files to `dbfs:/mnt/exports`. List the migration steps for it.

<!-- solution -->

Upgrade the table into Unity Catalog (`SYNC` if external, deep clone or CTAS if managed), change the code to the three-level name such as `prod.sales.orders`, replace the mount with a volume backed by an external location, and grant the needed privileges to the job's service principal.

<!-- takeaways -->

- Every object has a three-level name: `catalog.schema.object`.
- Storage credentials and external locations govern access to paths.
- Volumes replace DBFS mounts for files.

<!-- unit: Identities and permissions -->

<!-- goals -->

- Grant privileges with inheritance and ownership in mind.
- Run production work under service principals with secrets handled safely.

<!-- concept -->

Privileges are granted to users, groups or service principals and flow down the hierarchy, but a user also needs `USE CATALOG` and `USE SCHEMA` on the parents. Owners can grant and manage; production objects should be owned by groups, not people.

Automation should run as service principals, so jobs don't break when someone leaves. Secrets live in secret scopes, though identity-based access to storage is better still. Account admins manage identities and metastores; workspace admins manage one workspace; catalog binding limits which workspaces see a catalog.

<!-- example -->

```sql
GRANT USE CATALOG ON CATALOG prod TO `analysts`;
GRANT USE SCHEMA, SELECT ON SCHEMA prod.gold TO `analysts`;
ALTER TABLE prod.gold.fct_sales OWNER TO `data-platform`;
```

#### How do you grant permissions in Unity Catalog?

With SQL or the UI, to users, groups or service principals. Privileges are inherited down the hierarchy, and a user needs `USE CATALOG` and `USE SCHEMA` on the parents to reach an object.

```sql
GRANT USE CATALOG ON CATALOG prod TO `analysts`;
GRANT USE SCHEMA, SELECT ON SCHEMA prod.gold TO `analysts`;
```

#### What is the difference between ownership and privileges?

The owner of an object (a user, group or service principal) can grant privileges on it and manage it. Privileges such as `SELECT`, `MODIFY`, `CREATE TABLE` or `READ VOLUME` grant specific actions. Making a group the owner of production objects avoids depending on one person.

#### What is the difference between account-level and workspace-level administration?

Account admins manage identities (users, groups, service principals, often synced from an identity provider through SCIM), metastores, workspaces and account-wide settings. Workspace admins manage settings, compute policies and access within one workspace.

#### What is a service principal, and why use one for production jobs?

A non-human identity for automation. Production jobs and CI/CD deployments should run as a service principal so they don't depend on a person's account and permissions, and so access is limited to what the pipeline needs.

#### How do you manage secrets in Databricks?

In secret scopes (Databricks-backed or backed by Azure Key Vault), read with `dbutils.secrets.get(scope, key)`. Secret values are redacted in notebook output. For cloud resources, prefer identity-based access (instance profiles, storage credentials) over secrets.

#### What is workspace-catalog binding?

A setting that limits which workspaces can access a catalog, for example so that a production catalog is only reachable from the production workspace, even if users have grants on it.

<!-- challenge -->

An analyst has `SELECT` on `prod.gold.fct_sales` but gets "permission denied". What is the likely cause?

<!-- solution -->

They are missing `USE CATALOG` on `prod` or `USE SCHEMA` on `prod.gold`; `SELECT` alone isn't enough. Another possibility is that the catalog is bound to other workspaces only.

<!-- takeaways -->

- Grants flow down, but `USE CATALOG` and `USE SCHEMA` are always needed.
- Groups own production objects; service principals run production jobs.
- Prefer identity-based access over secrets.

<!-- unit: Fine-grained access -->

<!-- goals -->

- Restrict rows and columns without copying tables.
- Compare row filters and column masks with dynamic views.

<!-- concept -->

Table-level grants are often too coarse: a team may see only its country, or only masked emails. Row filters and column masks are functions attached to the table and evaluated at query time for the current user, so there is one table and many views of it. Dynamic views achieve the same with `current_user()` or group checks, and were the usual approach before.

<!-- example -->

```sql
CREATE FUNCTION gov.country_filter(country STRING)
RETURN is_account_group_member('admins')
    OR is_account_group_member(concat('analysts_', lower(country)));

ALTER TABLE prod.gold.sales SET ROW FILTER gov.country_filter ON (country);
```

#### What are row filters and column masks?

Functions attached to a table that are evaluated at query time. A row filter returns which rows a user may see (for example only their country); a column mask returns the value or a masked version depending on the user's group membership. Data stays in one table instead of in many filtered copies.

#### What are dynamic views?

Views that use functions like `current_user()` or `is_account_group_member()` to filter rows or redact columns. They were the usual approach before row filters and column masks existed.

#### Analysts must see only their country's rows in a shared table. How do you implement it?

Attach a Unity Catalog row filter function to the table that checks the user's group membership against the country column. Grant `SELECT` to the analyst groups. Use column masks for sensitive columns.

<!-- challenge -->

Support agents must see customer rows but only the last four digits of the phone number; the fraud team must see full numbers. Write the idea of the mask.

<!-- solution -->

A column mask function on `phone`: if the user is in the fraud group, return the value; otherwise return `concat('***', right(phone, 4))`. Attach it with `ALTER TABLE ... ALTER COLUMN phone SET MASK`.

<!-- takeaways -->

- Row filters and column masks run at query time per user.
- One table with policies beats many filtered copies.
- Base policies on groups, not individual users.

<!-- unit: Discovery, lineage and sharing -->

<!-- goals -->

- Use lineage, system tables, tags and comments to understand data.
- Share or query data across organizations and systems without copying it.

<!-- concept -->

Governance also means knowing what exists and how it connects. Unity Catalog records table- and column-level lineage automatically, system tables expose usage, audits and billing as SQL, and comments and tags make data searchable and classifiable.

Data often has to cross boundaries. Delta Sharing gives other organizations live, read-only access without copies; Lakehouse Federation lets you query external databases in place.

<!-- example -->

```sql
-- Who reads the table we want to change?
SELECT DISTINCT entity_type, entity_id, created_by
FROM system.access.table_lineage
WHERE source_table_full_name = 'prod.silver.customers'
  AND event_date >= current_date() - 30;
```

#### What lineage does Unity Catalog capture?

Table- and column-level lineage for queries run on Databricks compute, across notebooks, jobs, pipelines and dashboards, shown in Catalog Explorer and queryable from system tables. It answers "what breaks if I change this column?" and "where does this number come from?".

#### What are system tables?

Read-only tables in the `system` catalog with operational data: billing usage (`system.billing.usage`), audit logs, table lineage, job runs, cluster events, query history and more. They are the basis for cost dashboards and auditing.

#### What are tags and comments used for in Unity Catalog?

Comments document tables and columns (and power AI-generated descriptions and search); tags (key-value pairs) classify objects, for example `pii=true`, which can drive policies, discovery and audits.

#### How do you discover data in Unity Catalog?

Through Catalog Explorer and search, which use names, comments, tags and lineage, plus popularity signals such as frequent users and queries. Good comments and tags make discovery much better.

#### What is Delta Sharing?

An open protocol for sharing live data securely across organizations and platforms without copying it. The provider creates a share of tables, views or volumes; recipients read it from Databricks or from open-source clients (pandas, Spark, BI tools). Databricks-to-Databricks sharing uses Unity Catalog identities.

#### What is Lakehouse Federation?

Query federation that lets Unity Catalog register external databases (PostgreSQL, MySQL, SQL Server, Snowflake, Redshift, BigQuery and others) as foreign catalogs, so you can query them in place with governance and lineage, without first ingesting the data.

#### How do you share gold tables with a partner company that doesn't use Databricks?

With open Delta Sharing: create a share with the tables, create a recipient with a token-based credential, and the partner reads it from pandas, Spark or a BI tool. Access can be revoked at any time and is audited.

<!-- challenge -->

You plan to rename a column in `silver.customers`. How do you find out what will break and who to warn?

<!-- solution -->

Check column-level lineage in Catalog Explorer (or `system.access.column_lineage`) for downstream tables, jobs, dashboards and notebooks, and the query history or audit logs for direct readers. Warn the owners, and consider keeping the old name in a view during the transition.

<!-- takeaways -->

- Lineage answers "what breaks if I change this?".
- System tables turn usage, audits and billing into SQL.
- Delta Sharing shares without copies; Federation queries without ingesting.

<!-- stage: Operating effectively -->

### Spark and performance on Databricks

<!-- unit: Plans and shuffles -->

<!-- goals -->

- Read a query plan and spot the expensive steps.
- Explain shuffles, AQE and partition counts.

<!-- concept -->

Spark turns your code into a plan of stages separated by shuffles, the moments when data moves across the network for a join, `groupBy` or `distinct`. Narrow steps are cheap; shuffles dominate the cost. So performance work starts by reading the plan, bottom-up: what is scanned, what is pushed down, where the exchanges are and which join strategy is used.

Adaptive Query Execution adjusts the plan at runtime, merging small partitions and switching joins. You still pick sensible partition counts and know the difference between `repartition` and `coalesce`.

<!-- example -->

```text
== Physical Plan (simplified, read bottom-up) ==
HashAggregate(keys=[country])
+- Exchange hashpartitioning(country, 200)          ← shuffle
   +- HashAggregate(keys=[country])                 ← partial aggregation
      +- Scan delta silver.orders
         PushedFilters: [order_date >= 2026-10-01]   ← pruning works
```

#### What is the difference between narrow and wide transformations?

Narrow transformations (`filter`, `select`, `withColumn`) compute each output partition from one input partition, with no data movement. Wide transformations (`groupBy`, `join`, `distinct`, `orderBy`) need a shuffle across the network. Performance work is mostly about shuffles.

#### How do you read a Spark query plan?

With `df.explain(mode="formatted")` or the SQL tab of the Spark UI. Read it bottom-up: scans (check pushed filters and pruned files), exchanges (shuffles), join strategies (broadcast, sort-merge), and aggregations. The query profile in Databricks SQL shows the same with timings.

#### What is Adaptive Query Execution?

A Spark feature, on by default, that re-optimizes a query at stage boundaries using runtime statistics: it coalesces small shuffle partitions, switches sort-merge joins to broadcast joins when a side turns out small, and splits skewed partitions.

#### How do you choose the number of shuffle partitions?

`spark.sql.shuffle.partitions` defaults to 200. With AQE, set a generous number (or `auto` on Databricks) and let AQE coalesce. Aim for partitions of roughly 100–200 MB after shuffle; too few causes spill, too many causes overhead.

#### What is the difference between `repartition` and `coalesce`?

`repartition(n)` does a full shuffle and can increase or decrease the number of partitions, optionally by columns. `coalesce(n)` only merges partitions without a full shuffle, so it's cheaper but can only decrease them and can leave uneven partitions. `coalesce(1)` funnels everything through one task.

<!-- challenge -->

A job ends with `.coalesce(1).write...` to produce one file, and the last stage takes 25 minutes on a 40-node cluster. Why, and what do you do?

<!-- solution -->

`coalesce(1)` funnels the whole final computation through one task, so 39 nodes sit idle. Write normally and let consumers read the table, or, if one file is truly required, write a small aggregated result or use `repartition(1)` only after the heavy work so the earlier stages stay parallel.

<!-- takeaways -->

- Shuffles are the main cost; read the plan for exchanges.
- AQE adjusts partitions and joins at runtime.
- `coalesce` merges without a shuffle but can kill parallelism.

<!-- unit: Joins, skew and spill -->

<!-- goals -->

- Choose broadcast joins and fix skew.
- Recognize spill and its remedies.

<!-- concept -->

Joins are where most slow jobs hurt. When one side is small, broadcasting it avoids shuffling the big side entirely. When keys are unevenly distributed, a few tasks get most of the data (skew) and the stage waits for them. When a task's data doesn't fit in memory, Spark spills it to disk.

All three show up in the Spark UI: look at the join strategy in the plan, compare median and maximum task durations, and check spill columns.

<!-- example -->

```python
from pyspark.sql.functions import broadcast
facts.join(broadcast(dim_store), "store_id")      # 50 MB dimension: no shuffle of facts
```
Stage summary that signals skew: median task 8 s, max task 14 min.

#### What is a broadcast join, and when does it help?

Spark sends a copy of the small table to every executor, so the large table is joined without being shuffled. It helps when one side is small enough (tens of MB by default, more with hints). Broadcasting a table that is too big causes driver or executor out-of-memory errors.

#### What is data skew, and how do you fix it?

Some keys hold far more rows than others, so a few tasks take much longer than the rest. Fixes: let AQE split skewed partitions, broadcast the small side, filter out or handle hot keys (often nulls) separately, or salt the key to spread it across partitions.

#### What is spill, and why is it slow?

When a task's data doesn't fit in execution memory, Spark writes it to local disk and reads it back. It shows up in the Spark UI as spill (memory) and spill (disk). Fix it with more, smaller partitions, larger or memory-optimized workers, or less data per task.

#### A join between a 2 TB fact table and a 50 MB dimension is slow. What do you check?

Whether it's being broadcast (check the plan; add a broadcast hint or raise the threshold), whether the fact scan is pruning files (filters on clustered columns), skew on the join key, and spill. A 50 MB dimension should almost always be broadcast.

#### How would you troubleshoot a job that suddenly got slower?

Compare the slow run with a normal one: input sizes, number of files (small files, missing `OPTIMIZE`), plan changes (a broadcast became a sort-merge join), skew in one stage, spill, cluster size or spot losses, and code or data changes since the last good run.

<!-- challenge -->

A join on `customer_id` has one task running for 20 minutes while the others finish in seconds. The key with most rows is `NULL`. What do you do?

<!-- solution -->

Rows with null keys can never match in an inner join, so filter them out before the join (or handle them separately for an outer join). If other hot keys remain, rely on AQE skew handling or salt those keys.

<!-- takeaways -->

- Broadcast small dimensions; check the plan to confirm it happens.
- Skew shows as a long tail of task times; nulls are a common hot key.
- Spill means too much data per task: more partitions or more memory.

<!-- unit: Writing efficient code -->

<!-- goals -->

- Avoid code patterns that make Spark slow.
- Use caching only where it helps.

<!-- concept -->

Some slowness comes from code, not data. Python UDFs move every row between the JVM and Python and hide logic from the optimizer; built-in functions are much faster. Building a plan with `withColumn` in a loop makes analysis slow, and calling `count()` after each step recomputes everything each time.

Caching is not a general fix: on Databricks the disk cache already speeds up repeated reads, serverless doesn't support `cache()`, and reuse across jobs belongs in a table.

<!-- example -->

```python
# Slow: Python UDF, row by row
@udf("string")
def clean(s): return s.strip().upper()
df.withColumn("code", clean("code"))

# Fast: built-in functions, optimized and Photon-friendly
from pyspark.sql import functions as F
df.withColumn("code", F.upper(F.trim("code")))
```

#### Why are Python UDFs slow, and what are the alternatives?

Each row is serialized between the JVM and a Python worker, and the optimizer can't see inside the function. Use built-in functions first, then pandas (vectorized) UDFs with Arrow, or SQL UDFs. Photon can't accelerate Python UDFs either.

#### Why is `withColumn` in a loop a problem?

Each call adds a projection to the logical plan, and analyzing a very deep plan becomes slow (it can take minutes before any data is processed). Use one `select` or `withColumns` with a dictionary instead.

#### Why does `count()` before every step slow a job down?

Each action triggers a full execution of the plan up to that point. Counting for logging after every transformation recomputes the data repeatedly. Get metrics from the Delta commit (`numOutputRows` in the history) or compute them once.

#### Should you use `cache()` on Databricks?

Sparingly. Caching helps when the same DataFrame is reused several times in one interactive session, but it uses memory and is not supported on serverless. The disk cache (automatic SSD caching of remote Parquet files on some instance types) often gives the benefit without code changes. For reuse across jobs, write a table.

#### What is the disk cache?

An automatic cache, formerly called the Delta cache, that stores copies of remote Parquet and Delta files on the workers' local SSDs, so repeated reads of the same data are faster. It is managed transparently.

<!-- challenge -->

A notebook renames 300 columns with a `for` loop of `withColumnRenamed` and takes 6 minutes before any job starts. Fix it.

<!-- solution -->

Build all the expressions at once and apply one `select`: `df.select([F.col(c).alias(new_names[c]) for c in df.columns])`, or use `withColumnsRenamed` with a dictionary. The plan stays shallow and analysis takes seconds.

<!-- takeaways -->

- Prefer built-in functions to Python UDFs.
- Build wide transformations in one `select`, not loops.
- Cache rarely; write tables for reuse across jobs.

<!-- unit: Pruning, statistics and job cost -->

<!-- goals -->

- Make queries read less data with pruning and statistics.
- Cut the cost of a heavy job.

<!-- concept -->

The cheapest data is the data you never read. Partition pruning skips directories and file pruning skips files using Delta statistics; both depend on filters that match the table's layout. Column statistics help the optimizer choose join strategies, and predictive optimization maintains layout and statistics on managed tables automatically.

Cost follows from that: incremental processing instead of full recomputes, pruned reads, the right compute type and size, and monitoring from billing system tables.

<!-- example -->

```sql
-- Prunes files: filter on the clustering column
SELECT sum(amount) FROM silver.events WHERE event_date = '2026-10-15';
-- Can't prune: function applied to the column
SELECT sum(amount) FROM silver.events WHERE date_format(event_date, 'yyyy-MM') = '2026-10';
```

#### How does file pruning differ from partition pruning?

Partition pruning skips whole directories based on partition columns. File pruning (data skipping) skips individual files using the min/max statistics in the Delta log, so it works on any column with statistics and benefits from clustering.

#### What are column statistics and why compute them?

`ANALYZE TABLE … COMPUTE STATISTICS FOR ALL COLUMNS` stores row counts and column statistics that the cost-based optimizer uses to choose join orders and strategies. Predictive optimization can maintain them automatically.

#### What is predictive optimization?

A Unity Catalog feature that automatically runs `OPTIMIZE`, `VACUUM` and statistics collection on managed tables when it predicts a benefit, so you don't have to schedule maintenance jobs.

#### What is `replaceWhere`?

A write option that atomically replaces only the rows matching a predicate, typically one date range, leaving the rest of the table untouched. It makes reprocessing a period idempotent.

```python
(df.write.format("delta").mode("overwrite")
   .option("replaceWhere", "event_date = '2026-10-15'")
   .saveAsTable("silver.events"))
```

#### How do you reduce the cost of a heavy Databricks job?

Use jobs or serverless compute instead of all-purpose clusters, enable Photon where it pays off, process incrementally instead of full recomputes, prune reads with clustering and filters, right-size and autoscale clusters, use spot workers, avoid unnecessary shuffles and Python UDFs, and monitor with `system.billing.usage`.

<!-- challenge -->

A daily job recomputes three years of sales into a gold table every night, though only yesterday's data changes. Outline a cheaper design.

<!-- solution -->

Process only the changed range: read new silver rows (CDF or a date filter), recompute the affected days, and write with `replaceWhere` on those dates (or a `MERGE`). Run it on jobs or serverless compute, and keep the gold table clustered by date.

<!-- takeaways -->

- Filters must match the layout, without functions on the column, to prune.
- Predictive optimization maintains managed tables for you.
- Incremental processing is the biggest cost lever.

### Security, cost and operations

<!-- unit: Security and auditing -->

<!-- goals -->

- Describe secure access to cloud storage and network options.
- Find who accessed what.

<!-- concept -->

Security on Databricks rests on identities rather than keys. Storage access goes through IAM roles wrapped in storage credentials, never access keys in code. Networks can be locked down with your own VPC, private connectivity, IP access lists and egress policies for serverless.

Everything is recorded: audit logs in `system.access.audit`, query history and lineage answer who did what and when.

<!-- example -->

```sql
SELECT event_time, user_identity.email, action_name, request_params.full_name_arg
FROM system.access.audit
WHERE service_name = 'unityCatalog'
  AND request_params.full_name_arg = 'prod.silver.customers'
  AND event_date >= current_date() - 7;
```

#### How does Databricks access data in AWS S3 securely?

Through IAM roles: in Unity Catalog, a storage credential wraps an IAM role that trusts Databricks, and external locations grant access to paths. Legacy setups used instance profiles attached to clusters. Access keys in code should be avoided.

#### What network security options exist?

Deploying classic compute in your own VPC/VNet, private connectivity between the control and compute planes (PrivateLink, Private Link), IP access lists, no public IPs on cluster nodes, serverless network policies for egress control, and customer-managed keys for encryption.

#### How do you audit who accessed what?

With audit logs (available in the `system.access.audit` table), Unity Catalog lineage and query history. They record logins, permission changes, data access and job actions.

<!-- challenge -->

A security review finds an AWS access key hard-coded in a notebook. What do you replace it with, and what else do you do?

<!-- solution -->

Replace it with a Unity Catalog storage credential (IAM role) and an external location or volume for the path, so no key is needed. Rotate (deactivate) the exposed key, check the audit and CloudTrail logs for misuse, and scan other notebooks and repos for keys.

<!-- takeaways -->

- Access storage through roles and storage credentials, never keys in code.
- Private networking and egress controls limit exposure.
- Audit logs live in system tables and can be queried.

<!-- unit: Watching the bill -->

<!-- goals -->

- Break down Databricks spend and find its drivers.
- Attribute costs to teams with tags and system tables.

<!-- concept -->

Spend is visible in `system.billing.usage`: DBUs by SKU, workspace, job, warehouse and tag, which you join with list prices. Tags on compute make the data attributable to teams. The usual culprits are always the same: clusters that never stop, production on all-purpose compute, full recomputes and runaway retries.

<!-- example -->

```sql
SELECT usage_metadata.job_id, sku_name, sum(usage_quantity) AS dbus
FROM system.billing.usage
WHERE usage_date >= date_trunc('month', current_date())
GROUP BY ALL ORDER BY dbus DESC LIMIT 10;
```

#### How do you monitor and control Databricks spend?

Tag clusters, jobs and warehouses with cost centers, query `system.billing.usage` joined with list prices, set budgets and alerts, enforce cluster policies (instance types, auto-termination, maximum workers), use serverless or jobs compute for production, and review the most expensive jobs regularly.

#### The monthly Databricks bill doubled. How do you investigate?

Query `system.billing.usage` by SKU, workspace, job, warehouse and tag, and compare months. Look for all-purpose clusters without auto-termination, jobs moved to all-purpose compute, warehouses that never stop, full refreshes, new serverless workloads and runaway retries.

<!-- challenge -->

Write the first two queries you run when finance asks why last month was 40% more expensive.

<!-- solution -->

First, DBUs (or cost) per SKU for this month versus last month, to see which product grew. Second, within the growing SKU, the top jobs, warehouses or clusters by usage, comparing the two months, to find the specific workload that changed.

<!-- takeaways -->

- `system.billing.usage` is the source of truth for spend.
- Tags make costs attributable to teams and projects.
- Compare by SKU first, then by workload.

<!-- unit: Deploying with bundles and CI/CD -->

<!-- goals -->

- Describe a Databricks project as code with Asset Bundles.
- Set up testing and deployment through CI/CD.

<!-- concept -->

Production pipelines should be deployed, not clicked together. Databricks Asset Bundles describe jobs, pipelines and their settings in YAML next to the code, with one target per environment. Development targets prefix resources per user and pause schedules; production targets run as a service principal.

A CI pipeline then validates the bundle, runs unit tests on pure transformation functions, deploys to staging for integration tests and promotes to production after approval.

<!-- example -->

```text
pull request ──► lint + pytest (local Spark) ──► bundle validate
merge to main ──► deploy -t staging ──► integration run ──► approval ──► deploy -t prod
```

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

<!-- challenge -->

Two developers deploy the same bundle to the dev workspace and overwrite each other's job. What is missing?

<!-- solution -->

The dev target should use `mode: development`, which prefixes resources with each user's name and deploys to a per-user folder, so their copies don't collide.

<!-- takeaways -->

- Bundles keep jobs and pipelines as code, per environment.
- Development mode isolates each developer's deployment.
- Test pure functions locally; deploy to staging before production.

<!-- stage: Serving and applying -->

### Databricks SQL and analytics

<!-- unit: Warehousing and BI -->

<!-- goals -->

- Explain how BI tools query Databricks and what speeds them up.
- Choose between views, materialized views and federation.

<!-- concept -->

Databricks SQL turns the lakehouse into a warehouse for analysts: SQL warehouses run queries from the editor, dashboards and BI tools over JDBC/ODBC, with Unity Catalog permissions for each user. Repeated queries benefit from the result cache.

How you expose data affects cost: a view reruns its query each time, a materialized view stores results and refreshes, and federation queries an external database in place, which is fine for exploration but slow for heavy use.

<!-- example -->

```sql
CREATE MATERIALIZED VIEW gold.mv_sales_by_month
SCHEDULE CRON '0 0 6 * * ?'
AS SELECT date_trunc('month', order_date) AS month, region, sum(amount) AS sales
FROM silver.orders GROUP BY ALL;
```

#### What is Databricks SQL?

The SQL warehousing part of the platform: SQL warehouses, a SQL editor, query history and profiles, alerts, dashboards and connectors for BI tools (Power BI, Tableau, Looker) through JDBC/ODBC.

#### How do BI tools connect to Databricks?

Through JDBC/ODBC drivers or native connectors (Power BI, Tableau, Looker, Excel) pointing at a SQL warehouse, authenticating with OAuth or tokens. Permissions are enforced by Unity Catalog for the connecting identity.

#### What is the result cache in Databricks SQL?

A cache of query results on SQL warehouses: when the same query runs again and the underlying tables haven't changed, the result is returned without recomputation.

#### What is the difference between a view, a temporary view and a materialized view?

A view stores only the query and runs it on each read. A temporary view exists only in the current session. A materialized view stores precomputed results and must be refreshed.

#### What is a materialized view in Databricks SQL?

A view whose results are stored and refreshed (on a schedule or on demand, incrementally when possible). It speeds up expensive aggregations for dashboards. It is created with `CREATE MATERIALIZED VIEW` and runs on serverless pipelines.

#### What is query federation used for in analytics?

Joining Databricks tables with tables still in an operational database or another warehouse, for exploration or migration, without building an ingestion first. For heavy repeated use, ingesting the data is faster and cheaper.

<!-- challenge -->

A Power BI report runs a heavy aggregation over 2 billion rows each time someone opens it; data changes once a day. What do you change?

<!-- solution -->

Precompute the aggregation as a materialized view (or a gold table) refreshed after the daily load, and point the report at it. Queries then read a small table, and the result cache helps repeated opens.

<!-- takeaways -->

- BI tools connect to SQL warehouses, with Unity Catalog permissions per user.
- Materialized views precompute expensive aggregations.
- Federation is for exploration; ingest for heavy repeated use.

<!-- unit: Dashboards, metrics and applications -->

<!-- goals -->

- Describe dashboards, Genie, metric views and alerts.
- Know when Databricks Apps and Lakebase fit.

<!-- concept -->

On top of warehouses, Databricks offers AI/BI dashboards, Genie for natural-language questions, and SQL alerts that notify on conditions. Metric views define measures once so every tool computes "revenue" the same way.

For interactive applications, Databricks Apps hosts web apps inside the workspace, and Lakebase provides a Postgres-compatible database for low-latency transactional needs that the analytical tables don't serve well.

<!-- example -->

A data quality alert: schedule this query hourly and notify when `bad_rows > 0`.
```sql
SELECT count(*) AS bad_rows FROM silver.orders
WHERE amount < 0 AND order_date = current_date();
```

#### What are AI/BI dashboards and Genie?

AI/BI dashboards are the current Databricks dashboards, built on SQL warehouses with AI-assisted authoring. Genie is a natural-language interface where business users ask questions of curated tables and get SQL-backed answers.

#### What is a metric view?

A Unity Catalog object that defines business metrics (measures and dimensions) once in YAML on top of a table, so dashboards, Genie and SQL users compute them consistently.

#### What are SQL alerts?

Scheduled queries that compare a result with a threshold and notify (email, Slack, webhook) when the condition is met, for example when a data quality check returns rows.

#### What are Databricks Apps?

A way to build and host data and AI applications (Streamlit, Dash, Gradio, Flask and others) directly in the workspace, with authentication and access to governed data through Unity Catalog.

#### What is Lakebase?

A managed PostgreSQL-compatible operational database inside Databricks, based on serverless Postgres, meant for low-latency transactional workloads (apps, feature serving) that sync with lakehouse tables.

<!-- challenge -->

Three dashboards show three different "active customers" numbers. How do you fix it for good?

<!-- solution -->

Agree on one definition with the business owners, define it once as a metric view (or a documented gold table), and rebuild the dashboards on it, so the definition can't drift per dashboard.

<!-- takeaways -->

- Define business metrics once, in a metric view.
- SQL alerts turn queries into monitoring.
- Apps and Lakebase serve interactive and transactional needs.

### Machine learning and AI

<!-- unit: Models and features -->

<!-- goals -->

- Describe the ML lifecycle on Databricks with MLflow and Unity Catalog.
- Explain why feature tables keep training and inference consistent.

<!-- concept -->

A model is only as trustworthy as its history. MLflow records each training run (parameters, metrics, artifacts) so you can compare runs and package the best one. Registering it in Unity Catalog turns it into a governed object with versions, aliases like `champion`, permissions and lineage back to the tables it was trained on.

Features need the same discipline. A feature table keyed by entity and time is computed once and reused, so training sets and live predictions read the same definitions instead of two copies of the logic.

<!-- example -->

```python
import mlflow
mlflow.set_registry_uri("databricks-uc")
with mlflow.start_run():
    model = train(features_df)
    mlflow.sklearn.log_model(model, "model", registered_model_name="ml.churn.churn_model")
```

#### What is MLflow?

An open-source platform, created by Databricks, for the ML lifecycle: experiment tracking (parameters, metrics, artifacts), model packaging, a model registry with versions and aliases, evaluation, and tracing for generative AI applications. On Databricks it is managed and integrated with Unity Catalog.

#### What does it mean to register a model in Unity Catalog?

Models are stored as Unity Catalog objects (`catalog.schema.model`) with versions and aliases such as `champion`, governed by the same permissions and lineage as tables, and usable across workspaces.

#### What is a feature table?

A Delta table with a primary key used to store ML features in Unity Catalog. Training sets are built by joining feature tables to labels (with point-in-time correctness for time series), and the same features can be served online for inference.

<!-- challenge -->

A model trained last quarter performs worse in production than in testing. Its features are computed by separate code for training and serving. What do you change?

<!-- solution -->

Move the features into feature tables built once from silver data, use point-in-time joins for training sets, and serve the same features online, so training and inference can't drift apart. Then retrain and compare versions in MLflow.

<!-- takeaways -->

- MLflow tracks runs; Unity Catalog versions and governs the models.
- Aliases such as `champion` decouple consumers from version numbers.
- Feature tables keep training and serving on one definition.

<!-- unit: Serving and AI in SQL -->

<!-- goals -->

- Choose between Model Serving, Vector Search and AI functions.
- Match each option to online, retrieval or batch workloads.

<!-- concept -->

Once a model is registered, the question is how it meets data. Online applications need low-latency answers, so the model sits behind a REST endpoint. Retrieval-augmented apps need to find relevant documents first, so an index over a Delta table keeps embeddings in sync with the source. Batch enrichment needs neither: analysts call a model inside a SQL query and the warehouse handles scale. All three stay under Unity Catalog permissions.

<!-- example -->

```sql
SELECT ticket_id,
       ai_classify(body, ARRAY('billing', 'bug', 'feature request')) AS category
FROM silver.support_tickets
WHERE created_date = current_date();
```

#### What is Model Serving?

A serverless service that exposes models (custom MLflow models, foundation models, external models) as REST endpoints with autoscaling, monitoring and access control.

#### What is Vector Search?

A managed vector database that indexes embeddings of a Delta table and keeps the index in sync, used for retrieval-augmented generation (RAG) and similarity search.

#### What are AI functions in Databricks SQL?

SQL functions such as `ai_query`, `ai_classify`, `ai_extract`, `ai_summarize` and `ai_translate` that call models from SQL, so you can enrich tables with LLM output in batch.

<!-- challenge -->

Support wants every new ticket tagged by category each morning and a chatbot that answers from the help-center articles. Which option fits each need?

<!-- solution -->

Tagging is batch work: a scheduled SQL query with `ai_classify` over new tickets. The chatbot needs retrieval: a Vector Search index over the articles table, with the LLM behind a Model Serving endpoint that uses retrieved passages as context.

<!-- takeaways -->

- Model Serving answers online requests through REST endpoints.
- Vector Search indexes Delta tables for retrieval.
- AI functions bring models into batch SQL.

<!-- stage: Putting it together -->

### Scenarios

<!-- unit: Designing an end-to-end pipeline -->

<!-- goals -->

- Combine ingestion, medallion layers, jobs and governance into one design.
- Explain each design choice in an interview answer.

<!-- concept -->

Design questions test whether you can connect the sections, not recite them. A good answer follows the data: how files arrive, how they become a trusted table, how they are refreshed, who may read them, and how the code reaches production. Name one tool per step and say why it fits, such as incremental reads for growing landing folders or `MERGE` for late corrections. Close with failure handling: retries, alerts and what a rerun does.

<!-- example -->

```text
S3 landing ─► Auto Loader ─► bronze (raw + _metadata)
                                │ dedupe, validate, MERGE
                                ▼
                             silver ─► gold aggregates ─► dashboard
 job: daily trigger, retries, alerts · UC grants · bundle deploys dev → prod
```

#### Design a pipeline that ingests daily CSV files from S3 into a reporting table.

Land files in S3, read them with Auto Loader (`availableNow` trigger) into a bronze Delta table with a declared schema and `_metadata` columns, clean, deduplicate and validate into silver with `MERGE`, build gold aggregates or a star schema, schedule it as a job with retries and alerts, govern it with Unity Catalog, and deploy it with a bundle.

<!-- challenge -->

The same pipeline must now also accept corrected files for past days. What changes in your design?

<!-- solution -->

Auto Loader still picks up the new files once. Silver uses `MERGE` on the business key with the newest `updated_at` winning, so corrections replace old rows instead of duplicating them. Gold aggregates for affected dates are recomputed, for example with `replaceWhere` on those dates.

<!-- takeaways -->

- Follow the data from landing to consumers, one tool per step.
- Make every layer idempotent so reruns and corrections are safe.
- Finish with scheduling, monitoring, governance and deployment.

<!-- unit: Migrating to Databricks -->

<!-- goals -->

- Plan a migration from an on-premises Hive stack.
- Validate results before switching consumers.

<!-- concept -->

Migrations fail less on technology than on sequencing. Start with an inventory, because hidden dependencies (a cron script, a report reading a raw table) break cutovers. Data and code move separately: tables convert to Delta, queries port to Spark SQL, and schedulers are replaced. Running old and new side by side and comparing outputs builds the trust needed to switch consumers and retire the old system.

<!-- example -->

```sql
-- Parquet table copied to cloud storage: convert in place
CONVERT TO DELTA parquet.`s3://lake/legacy/orders` PARTITIONED BY (order_date DATE);
-- then compare with the legacy output
SELECT count(*), sum(amount) FROM main.sales.orders WHERE order_date = '2026-09-30';
```

#### How would you migrate a Hive-based on-premises pipeline to Databricks?

Inventory jobs, tables and dependencies; copy data to cloud storage and convert to Delta (`CONVERT TO DELTA` for Parquet); port HiveQL to Spark SQL (mostly compatible); replace Oozie or cron with Lakeflow Jobs or Airflow; put tables in Unity Catalog; validate results side by side (row counts, checksums, aggregates) before switching consumers.

<!-- challenge -->

Row counts match between the old and new pipelines, but revenue totals differ by 0.3%. How do you find the cause?

<!-- solution -->

Compare aggregates per day and per key to localize the difference, then diff the affected rows. Usual causes are decimal versus double types, time-zone handling of timestamps, NULL handling in joins, and duplicates resolved differently. Fix the rule, rerun, and compare again.

<!-- takeaways -->

- Inventory jobs, tables and consumers before moving anything.
- Convert data to Delta, port HiveQL, replace the scheduler.
- Run side by side and compare results before cutover.
