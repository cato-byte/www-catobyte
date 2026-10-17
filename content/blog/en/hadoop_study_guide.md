## Hadoop Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Hadoop study guide: about 200 questions](../../images/hadoop_study_guide_title_img.png)

About 200 interview-style questions on Apache Hadoop and its ecosystem: HDFS, YARN, MapReduce, file formats, Hive, HBase, ZooKeeper, ingestion tools, security, operations and the move to cloud object storage. Hadoop is no longer the default for new platforms, but many companies still run it, and its ideas (data locality, distributed storage, resource management) underpin Spark and the lakehouse. Open a question to see its answer, or use the filter to search the whole guide.

<!-- QA -->

### Fundamentals

#### What is Apache Hadoop?

An open-source framework for storing and processing very large datasets across clusters of commodity machines. Its core modules are HDFS (distributed storage), YARN (resource management), MapReduce (a batch processing model) and Hadoop Common (shared libraries).

#### What problem did Hadoop solve?

Storing and processing data too large for one machine, cheaply, by spreading data and computation across many inexpensive servers and tolerating hardware failures in software rather than buying specialized, expensive hardware.

#### Where did Hadoop come from?

From Google's papers on the Google File System (2003) and MapReduce (2004). Doug Cutting and Mike Cafarella implemented the ideas for the Nutch search project; Yahoo! invested heavily, and Hadoop became an Apache top-level project in 2008.

#### What are the main design principles of Hadoop?

Move computation to the data (data locality), assume hardware fails and handle it in software (replication, task retries), scale out horizontally with commodity machines, favor high throughput over low latency, and store data write-once, read-many.

#### What is data locality?

Scheduling tasks on the nodes (or racks) that already hold the data blocks they read, so data doesn't travel over the network. It was crucial when networks were the bottleneck.

#### What are the core configuration files of Hadoop?

`core-site.xml` (common settings such as the default file system `fs.defaultFS`), `hdfs-site.xml` (HDFS settings like replication and NameNode directories), `yarn-site.xml` (ResourceManager and NodeManager settings) and `mapred-site.xml` (MapReduce settings).

#### What is the difference between Hadoop 1, 2 and 3?

Hadoop 1 combined resource management and MapReduce in the JobTracker/TaskTracker model. Hadoop 2 introduced YARN, separating resource management so other engines could run, and NameNode high availability. Hadoop 3 added erasure coding, support for more than two NameNodes, Java 8+ requirements, YARN timeline service v2, and other improvements.

#### What are the main Hadoop distributions?

Historically Cloudera, Hortonworks (merged with Cloudera in 2019) and MapR (acquired by HPE). Today Cloudera Data Platform is the main commercial distribution, and cloud services (Amazon EMR, Google Dataproc, Azure HDInsight) offer managed Hadoop ecosystems.

#### What is the Hadoop ecosystem?

The set of projects built around Hadoop: Hive (SQL), HBase (NoSQL), Pig (scripting), Spark (fast processing), Kafka (streaming), ZooKeeper (coordination), Oozie (workflows), Sqoop and Flume (ingestion), Ranger and Atlas (security and governance), Impala and Presto/Trino (interactive SQL), and others.

#### Why is Hadoop less popular for new projects today?

Cloud object storage (S3, ADLS, GCS) separates storage from compute more cheaply and elastically, Spark replaced MapReduce for processing, and managed warehouses and lakehouses (Snowflake, Databricks, BigQuery) remove cluster operations. Hadoop clusters are complex to run and tune.

#### Is Hadoop still relevant to learn?

Yes, for maintaining and migrating existing clusters (common in banks, telecoms and large enterprises), and because its concepts — distributed file systems, blocks, replication, data locality, resource managers, partitioning, shuffle — explain how Spark, Hive and modern lakehouses work.

#### What is a commodity hardware cluster?

A cluster of standard, relatively cheap servers with local disks, as opposed to specialized high-end machines or SANs. Hadoop expects individual nodes to fail and works around it.

#### What does "write once, read many" mean in HDFS?

Files are written once and then mostly read; HDFS supports appends but not random updates in the middle of files. This simplifies consistency and favors batch analytics.

#### How does Hadoop scale?

Horizontally: add DataNodes for more storage and NodeManagers for more compute; HDFS rebalances data and YARN uses the new capacity. The NameNode's memory limits the number of files, which federation addresses.

#### What is Hadoop Common?

The shared libraries and utilities used by the other Hadoop modules: file system abstractions, RPC, serialization, configuration, security and command-line tools.

#### What is the Hadoop `FileSystem` abstraction?

A Java API that lets Hadoop applications work with different storage systems through one interface, with implementations for HDFS (`hdfs://`), local files (`file://`), S3 (`s3a://`), Azure (`abfs://`), Google Cloud Storage (`gs://`) and others.

#### What are the typical workloads run on Hadoop clusters?

Batch ETL, log processing, data warehousing with Hive, machine learning feature preparation with Spark, search indexing, and storing raw data in a central data lake.

#### What does "schema on read" mean in Hadoop?

Data is stored as files without enforcing a schema at write time; a schema (for example a Hive table definition) is applied when reading. It makes ingestion flexible but pushes validation to consumers.

#### What are edge nodes?

Gateway machines with Hadoop client libraries and configuration but no DataNode or NodeManager roles, from which users submit jobs, run CLI tools and host client applications without touching the worker nodes.

#### Why does Hadoop favor throughput over latency?

It was designed for scanning large datasets in batch, where total processing time matters more than the response time of individual requests; HDFS reads large blocks sequentially, and MapReduce jobs have seconds of startup overhead.

### HDFS architecture

#### What is HDFS?

The Hadoop Distributed File System: a distributed, fault-tolerant file system that splits files into large blocks and stores replicas of each block on different machines, providing high-throughput access to large datasets.

#### What are the main components of HDFS?

The NameNode (master holding the namespace and block locations), DataNodes (workers storing blocks on local disks), and in high-availability setups a Standby NameNode, JournalNodes and ZooKeeper Failover Controllers.

#### What does the NameNode store?

The file system namespace (directories, files, permissions, which blocks make up each file) in memory, persisted as an `fsimage` checkpoint plus an `edits` log. Block locations are not persisted; they come from DataNode block reports.

#### What does a DataNode do?

It stores blocks as files on local disks, serves read and write requests from clients, sends heartbeats and block reports to the NameNode, and replicates blocks to other DataNodes when instructed.

#### What is the default block size and why is it so large?

128 MB in Hadoop 2 and 3 (64 MB in Hadoop 1). Large blocks reduce NameNode metadata, minimize seek time relative to transfer time, and give each map task a meaningful amount of data.

#### What is the replication factor?

The number of copies of each block, 3 by default (`dfs.replication`), configurable per file. More replicas mean more durability and read parallelism but more storage.

#### What is rack awareness?

The NameNode knows which rack each DataNode is in (through a topology script) and places replicas to survive a rack failure: by default the first replica on the writer's node, the second on a node in a different rack, and the third on another node in that second rack.

#### What is the Secondary NameNode?

A helper that periodically merges the `edits` log into the `fsimage` (checkpointing) so the edits log doesn't grow forever and NameNode restarts are faster. Despite its name, it is not a standby and can't take over if the NameNode fails.

#### How does NameNode high availability work?

Two (or more, in Hadoop 3) NameNodes run: one active, the others standby. They share the edits log through a quorum of JournalNodes; DataNodes report to all of them. ZooKeeper Failover Controllers monitor health and trigger automatic failover, with fencing to prevent two active NameNodes (split brain).

#### What is HDFS federation?

Several independent NameNodes, each managing part of the namespace (for example `/user` and `/data`), sharing the same DataNodes. It scales the namespace beyond one NameNode's memory and isolates workloads. ViewFs or Router-based federation present a unified view.

#### What is the Observer NameNode?

A read-only NameNode (Hadoop 3) that serves read requests with consistent state, offloading the active NameNode in clusters with heavy metadata read traffic.

#### What are heartbeats and block reports?

DataNodes send a heartbeat every few seconds to show they're alive and a full block report periodically listing their blocks. If heartbeats stop for about ten minutes, the NameNode marks the node dead and re-replicates its blocks.

#### What is safe mode?

A read-only state the NameNode enters at startup while it loads the namespace and waits for DataNodes to report enough block replicas. It leaves safe mode automatically once a threshold of blocks is satisfied, or an admin can leave it manually.

#### Why is the NameNode a scalability bottleneck?

All metadata lives in its memory: roughly 150 bytes per file, directory and block. Hundreds of millions of objects need a lot of heap, and every metadata operation goes through it. Federation, observer NameNodes and avoiding small files help.

#### What is erasure coding in HDFS?

A Hadoop 3 storage policy that stores data with parity (for example Reed-Solomon 6+3) instead of three full copies, giving similar fault tolerance with about 50% storage overhead instead of 200%. Reads and reconstruction cost more CPU and network, so it suits cold data.

#### What are the `fsimage` and `edits` files?

`fsimage` is a checkpoint of the whole namespace at a point in time; `edits` is the log of every change since that checkpoint. On startup, the NameNode loads the `fsimage` and replays the edits.

#### What are JournalNodes?

A small quorum of daemons (usually three or five) that store the shared edits log for HA NameNodes; the active NameNode writes to a majority, and standbys read from them to stay in sync.

#### What is fencing in NameNode HA?

Mechanisms that ensure a former active NameNode can no longer modify the namespace after failover (for example killing its process or relying on JournalNodes accepting writes from only one writer epoch), preventing split brain.

#### How does HDFS handle a file smaller than a block?

It uses only as much disk as the file needs; a 1 MB file doesn't consume 128 MB. But it still costs a full metadata object in the NameNode, which is the real issue with small files.

#### What is the HDFS namespace?

The hierarchy of directories and files, with permissions, owners, quotas and modification times, maintained by the NameNode, similar to a traditional file system tree.

### HDFS operations

#### How does an HDFS write work?

The client asks the NameNode to create the file; for each block, the NameNode returns a list of DataNodes. The client streams data in packets to the first DataNode, which forwards to the second, which forwards to the third (a pipeline). Acknowledgements flow back, and the file is visible once closed.

#### How does an HDFS read work?

The client asks the NameNode for the block locations of the file, then reads each block directly from the closest DataNode holding a replica, verifying checksums; if a DataNode fails, it switches to another replica.

#### How does HDFS detect corrupted data?

Each block has checksums computed at write time; clients verify them on read, and DataNodes run a background block scanner. Corrupt replicas are reported to the NameNode, which re-replicates from a healthy copy.

#### What happens when a DataNode dies?

The NameNode stops receiving heartbeats, marks it dead after a timeout, and schedules re-replication of its blocks from remaining replicas to restore the replication factor.

#### What is the HDFS balancer?

A tool that moves blocks between DataNodes so disk usage is even across the cluster, typically run after adding nodes. The disk balancer evens usage across disks within a DataNode.

#### How do you decommission a DataNode?

Add it to the exclude file and refresh the NameNode (`hdfs dfsadmin -refreshNodes`); the NameNode re-replicates its blocks elsewhere, and once decommissioning completes the node can be removed safely.

#### What are common `hdfs dfs` commands?

```bash
hdfs dfs -ls /data/raw
hdfs dfs -mkdir -p /data/raw/orders/dt=2026-10-15
hdfs dfs -put orders.csv /data/raw/orders/dt=2026-10-15/
hdfs dfs -get /data/curated/report.parquet .
hdfs dfs -du -h /data
hdfs dfs -rm -r -skipTrash /tmp/old
hdfs dfs -setrep -w 2 /data/archive
```

#### What does `hdfs fsck` do?

It checks the health of files and blocks: missing, corrupt, under-replicated or mis-replicated blocks, and can list block locations (`hdfs fsck /path -files -blocks -locations`). It reads metadata only and doesn't fix problems itself.

#### What does `hdfs dfsadmin -report` show?

Cluster capacity, used and remaining space, and per-DataNode status (live, dead, decommissioning), useful for a quick health check.

#### What is the HDFS trash?

When enabled (`fs.trash.interval`), deleted files go to a `.Trash` folder in the user's home directory and are permanently removed after the interval, protecting against accidental deletes. `-skipTrash` bypasses it.

#### What are HDFS snapshots?

Read-only, point-in-time copies of a directory (enabled per directory by an admin) that are cheap because they only record changes; used to recover from user errors and for consistent backups.

#### What are HDFS quotas?

Name quotas (maximum number of files and directories) and space quotas (maximum bytes, including replicas) set per directory, used to prevent one team from exhausting the cluster.

#### What is `distcp`?

A tool that copies large amounts of data between HDFS clusters or between HDFS and object storage, using MapReduce to copy in parallel, with options for incremental updates and preserving attributes.

#### What are HDFS storage policies?

Rules that place block replicas on different storage types (DISK, SSD, ARCHIVE, RAM_DISK) according to temperature: Hot, Warm, Cold, All_SSD, One_SSD and Lazy_Persist. The mover tool relocates existing data to match a policy.

#### What is short-circuit local read?

When the client runs on the same node as the DataNode holding a block, it reads the file directly from local disk through a shared file descriptor, bypassing the DataNode's network path, which speeds up reads.

#### What is the small-files problem in HDFS?

Millions of files much smaller than the block size consume NameNode memory (each file and block is an object), make listings slow and create many tiny tasks. Solutions: compact files (Hive `INSERT OVERWRITE`, Spark repartition), use container formats (SequenceFile, Parquet, ORC), or archive with HAR files.

#### How do you change the replication factor of existing data?

With `hdfs dfs -setrep -w <n> <path>`, which changes the replication of the files and waits until replicas are added or removed.

#### What does `dfs.datanode.failed.volumes.tolerated` control?

How many disk failures a DataNode tolerates before shutting itself down; by default zero, but large nodes with many disks are often configured to keep running with one or two failed disks.

#### How do you move data between HDFS and the local file system?

`hdfs dfs -put`/`-copyFromLocal` to upload, `hdfs dfs -get`/`-copyToLocal` to download, and `hdfs dfs -getmerge` to concatenate a directory of part files into one local file.

#### What does `hdfs dfs -count` show?

The number of directories, files and bytes under a path, and with `-q` the name and space quotas, useful to find directories with too many small files.

#### What is WebHDFS?

A REST API to HDFS over HTTP, allowing clients in any language to read, write and manage files without Hadoop libraries; HttpFS provides a gateway version.

### YARN

#### What is YARN?

Yet Another Resource Negotiator: Hadoop's cluster resource manager. It allocates CPU and memory in containers to applications (MapReduce, Spark, Tez, Flink), separating resource management from the processing engine.

#### What are YARN's main components?

The ResourceManager (cluster-wide scheduler and application manager), NodeManagers (per-node agents that launch and monitor containers), ApplicationMasters (one per application, negotiating resources and coordinating tasks) and containers (allocated bundles of memory and vcores).

#### What happens when you submit an application to YARN?

The client submits to the ResourceManager, which starts the ApplicationMaster in a container on some node. The ApplicationMaster requests containers for tasks, considering data locality; NodeManagers launch them; the ApplicationMaster monitors progress and reports completion.

#### What schedulers does YARN offer?

The FIFO scheduler (first come, first served), the Capacity Scheduler (hierarchical queues with guaranteed capacities and elasticity, the default in most distributions) and the Fair Scheduler (shares resources fairly among running applications and queues).

#### How does the Capacity Scheduler work?

Queues are configured with guaranteed percentages of cluster capacity (for example `etl` 50%, `analytics` 30%, `adhoc` 20%), can borrow idle capacity up to a maximum, have user limits, and can preempt containers to give guaranteed capacity back.

#### What is preemption in YARN?

When a queue is below its guaranteed share and others are using more, the scheduler can kill containers of over-using applications to free resources, ensuring guarantees are met.

#### How are container sizes configured?

With `yarn.nodemanager.resource.memory-mb` and `.cpu-vcores` (resources a node offers), `yarn.scheduler.minimum-allocation-mb` and `maximum-allocation-mb` (allowed container sizes), and per-application requests (for example `mapreduce.map.memory.mb` or Spark executor memory plus overhead).

#### What happens when a container exceeds its memory?

The NodeManager kills it ("Container killed by YARN for exceeding memory limits"), and the task is retried. Fix it by increasing container memory or overhead, or reducing memory use per task (more partitions, less caching).

#### What are node labels in YARN?

Labels that partition nodes (for example `gpu` or `high-memory`), so queues and applications can be restricted to specific node groups.

#### How does ResourceManager high availability work?

An active and a standby ResourceManager coordinate through ZooKeeper; state is stored in a state store so the standby can take over and running applications can continue (work-preserving restart).

#### What is the YARN Timeline Service?

A service that stores and serves history about applications and their tasks (start times, durations, counters) for monitoring and debugging after applications finish. Spark has its own History Server.

#### How do you inspect and kill YARN applications?

```bash
yarn application -list -appStates RUNNING
yarn application -status application_1729000000000_0042
yarn logs -applicationId application_1729000000000_0042 | less
yarn application -kill application_1729000000000_0042
```

#### What is the difference between client and cluster deploy mode for Spark on YARN?

In client mode, the Spark driver runs on the machine that submitted the job (an edge node), useful for interactive work; in cluster mode, the driver runs inside the ApplicationMaster container on the cluster, better for production jobs that must survive the client disconnecting.

#### What are vcores?

Virtual CPU cores advertised by NodeManagers, an abstract unit YARN uses to schedule CPU; how strictly CPU is enforced depends on the resource calculator and cgroups configuration.

#### What is the DominantResourceCalculator?

A YARN resource calculator that considers both memory and CPU when scheduling (the dominant resource of each request), instead of the default that looks only at memory.

#### What is the YARN shared cache?

A feature that caches application resources (JARs, files) on nodes across applications, reducing the time and bandwidth spent localizing the same dependencies repeatedly.

#### How do you limit a user from using the whole cluster?

With scheduler queue limits: maximum capacity per queue, user limit factors, maximum applications per user and per queue, and access control lists on queues.

### MapReduce

#### What is MapReduce?

A programming model and execution engine for batch processing: a map function processes input records into intermediate key-value pairs, the framework groups all values by key (shuffle and sort), and a reduce function aggregates each key's values into results.

#### Explain word count in MapReduce.

The mapper reads lines and emits `(word, 1)` for each word. The shuffle groups pairs by word. The reducer receives `(word, [1, 1, 1, …])` and emits `(word, sum)`. A combiner can sum locally after the map to reduce shuffled data.

#### What is an InputSplit?

A logical chunk of input assigned to one map task, usually corresponding to an HDFS block. The number of splits determines the number of map tasks.

#### What is a RecordReader?

The component that reads an InputSplit and turns it into key-value records for the mapper, for example `LineRecordReader` gives (byte offset, line).

#### What happens during shuffle and sort?

Map outputs are partitioned by key, sorted and spilled to local disk; reducers fetch their partitions from all mappers over the network, merge-sort them, and feed grouped keys to the reduce function. It's usually the most expensive phase.

#### What is a combiner?

An optional "mini-reducer" that runs on map output before the shuffle to pre-aggregate values per key, reducing network transfer. It must be safe to apply zero, one or many times (associative and commutative operations like sum, max).

#### What is a partitioner?

The function that decides which reducer receives each key, by default `hash(key) % numReducers`. Custom partitioners control data distribution, for example to avoid skew or to group related keys.

#### How do you choose the number of reducers?

Enough to parallelize the reduce work and keep each reducer's input reasonable, typically around 0.95 or 1.75 times the reduce slots or based on output size; zero reducers make a map-only job.

#### What is speculative execution?

When some tasks run much slower than others (stragglers), the framework launches duplicate attempts on other nodes and uses whichever finishes first. It helps with slow hardware but wastes resources and should be disabled for non-idempotent side effects.

#### What are counters?

Named numbers that tasks increment (built-in ones like records read, bytes written, spilled records, and custom ones like "invalid rows"), aggregated across the job for monitoring and validation.

#### What is the distributed cache?

A mechanism to ship read-only files (lookup tables, JARs, configuration) to every node running tasks of a job, so tasks can read them locally.

#### How do you do a join in MapReduce?

A reduce-side join tags records from both datasets, emits them by join key, and joins in the reducer (general but shuffles everything). A map-side join loads the small dataset into memory through the distributed cache and joins in the mapper (fast, but one side must fit in memory).

#### Why was MapReduce replaced by Spark for most workloads?

MapReduce writes intermediate results to disk between every stage and expresses complex pipelines as chains of jobs, which is slow and verbose. Spark keeps data in memory across stages, optimizes whole DAGs, and offers high-level APIs (SQL, DataFrames) in several languages.

#### What is Hadoop Streaming?

A utility that lets you write mappers and reducers in any language that reads stdin and writes stdout (Python, bash), with Hadoop handling distribution, which was popular before PySpark.

#### What is a map-only job used for?

Transformations that don't need grouping, such as filtering, format conversion or parsing logs, setting the number of reducers to zero so mapper output is written directly.

#### What are the main classes of a MapReduce job in Java?

A `Mapper` subclass with a `map()` method, a `Reducer` subclass with `reduce()`, and a driver that configures the `Job` (input and output formats and paths, key and value types, number of reducers) and submits it.

#### What are InputFormat and OutputFormat?

`InputFormat` defines how input is split and read (`TextInputFormat`, `SequenceFileInputFormat`, `KeyValueTextInputFormat`, `CombineFileInputFormat` for many small files); `OutputFormat` defines how results are written (`TextOutputFormat`, `SequenceFileOutputFormat`).

#### What is `CombineFileInputFormat` used for?

Packing many small files into fewer splits, so a job over thousands of small files doesn't launch thousands of tiny map tasks.

#### What is the role of the OutputCommitter?

It makes job output appear atomically: tasks write to temporary directories and the committer moves results to the final location when the job succeeds, so failed or speculative attempts don't leave partial output.

#### What is a secondary sort?

A technique to have values arrive at the reducer sorted by a secondary field, using a composite key, a custom partitioner on the natural key and a grouping comparator.

#### Why should map tasks run for at least a minute or so?

Task startup has overhead (JVM launch, scheduling); very short tasks spend more time starting than processing. Larger splits or combined small files make tasks efficient.

### File formats and compression

#### Which file formats are common in Hadoop?

Text (CSV, JSON), SequenceFile (binary key-value), Avro (row-based with embedded schema, good for ingestion and schema evolution), Parquet and ORC (columnar, compressed, with statistics, best for analytics).

#### What is a splittable file format, and why does it matter?

One that can be read in independent chunks by different tasks. Plain text, SequenceFile, Avro, Parquet and ORC are splittable; a gzip-compressed text file is not, so one task must read it entirely, limiting parallelism.

#### Which compression codecs are used in Hadoop?

Snappy and LZ4 (fast, moderate compression), gzip/Deflate (better compression, slower, not splittable for text), bzip2 (splittable, slow), LZO (splittable with an index) and ZSTD (good ratio and speed). Inside Parquet and ORC, compression is per block, so files remain splittable.

#### Why is ORC associated with Hive?

ORC (Optimized Row Columnar) was created for Hive: columnar storage with lightweight indexes, statistics and bloom filters, and it supports Hive ACID tables. Parquet is more common across other engines.

#### What is Avro's advantage for data pipelines?

The schema is stored with the data and supports evolution (adding fields with defaults, renaming with aliases), and its compact row format suits streaming and ingestion, often with a schema registry in Kafka.

#### What is a SequenceFile?

A flat binary file of key-value pairs, splittable and compressible, used as MapReduce intermediate output and to pack many small files into one container.

#### What are HAR files?

Hadoop Archives: a way to pack many small files into a single archive (an index plus part files) to reduce NameNode objects while keeping files accessible through a `har://` path.

#### How does Parquet organize data?

Files contain row groups; each row group stores column chunks, divided into pages with encoding and compression; the footer holds the schema and statistics (min/max, null counts) per row group and column, enabling column pruning and predicate pushdown.

#### How does ORC organize data?

Files are divided into stripes (typically 64–256 MB) with column streams, lightweight indexes every 10,000 rows (min/max), optional bloom filters, and a footer with stripe statistics, allowing engines to skip stripes and row groups.

#### Should you compress intermediate MapReduce output?

Usually yes, with a fast codec like Snappy or LZ4 (`mapreduce.map.output.compress`), because it reduces disk and network I/O during the shuffle at a small CPU cost.

#### How do you choose between Avro and Parquet?

Avro for row-oriented writes, streaming and messages where whole records are read and schemas evolve frequently; Parquet for analytics where queries read a few columns of many rows.

### Hive

#### What is Apache Hive?

A data warehouse system on Hadoop that lets you query data in HDFS (and object storage) with a SQL dialect (HiveQL). Queries are compiled into jobs on MapReduce, Tez or Spark, and table metadata is stored in the Hive Metastore.

#### What is the Hive Metastore?

A service backed by a relational database (MySQL, PostgreSQL) that stores table definitions, columns, partitions, locations and formats. It's used by Hive, Spark, Impala, Presto/Trino and others, and AWS Glue Data Catalog is compatible with it.

#### What is the difference between managed and external tables in Hive?

Hive owns managed tables' data: dropping the table deletes the files. External tables point to data managed elsewhere: dropping them only removes metadata. External tables are common for shared data lakes.

#### What are partitions in Hive?

Subdirectories by column values (`/sales/dt=2026-10-15/`); queries filtering on partition columns read only matching directories. Dynamic partitioning creates partitions from query results.

#### What is bucketing in Hive?

Dividing data within a table or partition into a fixed number of files by hashing a column, which enables efficient sampling and bucket map joins when tables are bucketed on the join key.

#### What execution engines can Hive use?

MapReduce (historic, deprecated), Apache Tez (DAG-based, the usual default in Hive 2/3) and Spark (Hive on Spark). Hive LLAP adds long-running daemons with caching for interactive queries.

#### What are Hive ACID tables?

Transactional ORC tables (Hive 3 managed tables) supporting `INSERT`, `UPDATE`, `DELETE` and `MERGE` with snapshot isolation, using delta files that are merged by compactions (minor and major).

#### What is the Hive cost-based optimizer?

Apache Calcite-based optimization using table and column statistics (`ANALYZE TABLE … COMPUTE STATISTICS`) to choose join orders and strategies; without statistics, plans can be poor.

#### What is a map join in Hive?

A join where the small table is loaded into memory on each mapper (broadcast), avoiding a shuffle; Hive converts joins automatically when the small table is under a size threshold (`hive.auto.convert.join`).

#### How do you load data into Hive tables?

`LOAD DATA INPATH` (moves files into the table location), `INSERT INTO/OVERWRITE … SELECT`, `CREATE TABLE AS SELECT`, or by writing files directly to an external table's location and adding partitions.

#### What is `MSCK REPAIR TABLE`?

A command that scans the table location for partition directories not registered in the metastore and adds them.

#### What are SerDes in Hive?

Serializer/deserializers that define how rows are read from and written to files: `LazySimpleSerDe` for delimited text, `OpenCSVSerde`, JSON SerDes, `RegexSerDe`, and built-in support for ORC, Parquet and Avro.

#### How do HiveQL and standard SQL differ?

HiveQL is mostly SQL but with Hadoop-specific features (partitions, buckets, `LATERAL VIEW explode`, SerDes, `INSERT OVERWRITE DIRECTORY`), historically limited transactions and subqueries, and schema-on-read semantics.

#### What is HiveServer2?

The service that accepts client connections (JDBC/ODBC, Beeline) and executes HiveQL queries with authentication, concurrency and security, replacing the older Hive CLI for multi-user access.

#### What is Beeline?

The command-line JDBC client for HiveServer2, used to run queries and scripts against Hive with proper authentication.

#### What is `LATERAL VIEW explode`?

A Hive construct to turn array or map columns into multiple rows, similar to `UNNEST` in other SQL dialects.

```sql
SELECT o.order_id, item
FROM orders o
LATERAL VIEW explode(o.items) t AS item;
```

#### What is the difference between `ORDER BY`, `SORT BY`, `DISTRIBUTE BY` and `CLUSTER BY` in Hive?

`ORDER BY` produces a total order through a single reducer; `SORT BY` sorts within each reducer; `DISTRIBUTE BY` controls which reducer receives each key; `CLUSTER BY` is `DISTRIBUTE BY` plus `SORT BY` on the same columns.

#### What is Hive vectorization?

Processing batches of rows (typically 1,024) at a time with columnar operations instead of row by row, which speeds up scans, filters and aggregations on ORC data.

#### How do you compute statistics in Hive?

`ANALYZE TABLE t PARTITION (dt) COMPUTE STATISTICS` for table and partition stats, and `… FOR COLUMNS` for column stats, which the cost-based optimizer uses; `hive.stats.autogather` gathers basic stats on insert.

#### What is dynamic partition insert, and what must you watch for?

`INSERT OVERWRITE TABLE t PARTITION (dt) SELECT …, dt FROM src` creates partitions from data values. Limits (`hive.exec.max.dynamic.partitions`) exist to prevent creating thousands of partitions accidentally, and many partitions with few rows cause small files.

### HBase

#### What is HBase?

A distributed, column-family NoSQL database modeled on Google Bigtable, running on HDFS. It provides random, real-time read and write access to billions of rows by row key, with strong consistency per row.

#### What is HBase's data model?

Tables of rows sorted by row key; each row has column families (defined at table creation), each family holds any number of columns (qualifiers), and each cell keeps versions identified by timestamps. Sparse columns cost nothing.

#### What are HBase's main components?

The HMaster (assigns regions, handles schema changes and load balancing), RegionServers (serve reads and writes for regions), regions (contiguous row key ranges of a table), and ZooKeeper (coordination and locating the meta table).

#### How does an HBase write work?

The RegionServer appends the edit to the write-ahead log (WAL) on HDFS for durability, then writes it to the in-memory MemStore. When the MemStore fills, it flushes to an immutable HFile on HDFS.

#### What are compactions in HBase?

Background processes that merge HFiles: minor compactions merge a few small files; major compactions rewrite all files of a store into one, removing deleted and expired cells. Major compactions are I/O heavy and often scheduled off-peak.

#### Why is row key design so important in HBase?

All access is by row key, and rows are sorted and split into regions by key. Monotonically increasing keys (timestamps, sequences) send all writes to one region (hotspotting). Use salting, hashing or field reversal, and design keys around the main access patterns.

#### When would you choose HBase over Hive?

HBase for low-latency random reads and writes by key (user profiles, time series lookups, counters); Hive for batch SQL analytics over large scans.

#### What is Apache Phoenix?

A SQL layer on HBase that compiles SQL into HBase scans, with secondary indexes and JDBC access.

#### What is a region split?

When a region grows beyond a configured size, the RegionServer splits it into two regions at a middle row key, and the HMaster may move them to balance load. Pre-splitting tables avoids initial hotspots.

#### What is a column family, and why should there be few of them?

A group of columns stored together in the same files with shared settings (compression, versions, TTL). Each family has its own MemStore and store files, so many families multiply flushes and compactions; two or three is typical.

#### How do you read from HBase efficiently?

Use `Get` for single rows by key and `Scan` with start and stop row keys for ranges, add filters to reduce data returned, set caching and batching for scans, and avoid full table scans in latency-sensitive paths.

#### What is a bloom filter in HBase?

A per-store-file structure that tells whether a row (or row and column) might exist in the file, letting reads skip files that certainly don't contain the key, reducing disk reads for random gets.

#### What is a TTL in HBase?

A time-to-live set per column family; cells older than the TTL are removed during compactions, which is useful for time series and caches.

### Other ecosystem tools

#### What is ZooKeeper?

A centralized coordination service providing a hierarchical key-value store (znodes), watches, and consensus (ZAB protocol). Hadoop components use it for leader election (NameNode and ResourceManager HA), configuration and service discovery; older Kafka versions used it too.

#### What was Apache Pig?

A high-level data flow language (Pig Latin) that compiled scripts into MapReduce or Tez jobs, popular for ETL before Spark and Hive matured; it's rarely used for new work.

#### What was Apache Sqoop?

A tool to transfer data between relational databases and Hadoop (import into HDFS/Hive, export back) using parallel MapReduce tasks. It was retired to the Apache Attic in 2021; Spark JDBC, DMS-like tools and CDC tools replaced it.

#### What is Apache Flume?

A service for collecting, aggregating and moving large amounts of log data from many sources into HDFS or HBase, with sources, channels and sinks. Kafka has largely replaced it.

#### What is Apache Oozie?

A workflow scheduler for Hadoop jobs (MapReduce, Hive, Pig, Sqoop, shell) defined in XML, with coordinators for time and data triggers. Most teams have moved to Airflow or other orchestrators.

#### What are Impala and Presto/Trino?

MPP SQL engines that query data in HDFS and object storage directly with long-running daemons, giving interactive latency compared with Hive on MapReduce. Trino (formerly PrestoSQL) is widely used and powers Amazon Athena.

#### How does Spark run on a Hadoop cluster?

Spark runs on YARN (driver in client or cluster mode, executors in YARN containers), reads and writes HDFS, uses the Hive Metastore for tables, and benefits from data locality.

#### What is Kafka's role in Hadoop architectures?

A durable, scalable message log that ingests streams (events, CDC) and decouples producers from consumers; data is then written to HDFS or object storage by Kafka Connect, Spark Streaming or Flink.

#### What is Apache Tez?

A DAG execution framework on YARN that runs Hive and Pig jobs as a single graph of tasks, avoiding MapReduce's per-stage disk writes and job startup costs.

#### What is Apache Ambari?

A web-based tool for provisioning, managing and monitoring Hadoop clusters (installing services, configuration, alerts), mainly used with Hortonworks distributions; Cloudera Manager plays the same role on Cloudera.

#### What is Apache Livy?

A REST service for submitting Spark jobs and interactive sessions to a cluster, used by notebooks and applications that can't run a Spark driver themselves.

#### What is Apache Ozone?

A scalable, distributed object store for Hadoop with an S3-compatible API, designed to overcome HDFS's small-file and namespace limits while staying compatible with Hadoop applications.

### Security and governance

#### How is authentication done in Hadoop?

With Kerberos: users and services obtain tickets from a Key Distribution Center, and Hadoop services verify them. Without Kerberos ("simple" mode), Hadoop trusts the username the client claims, which is insecure.

#### What are delegation tokens?

Tokens issued by services (NameNode, ResourceManager) after Kerberos authentication, passed to tasks running on the cluster so they can access HDFS without having Kerberos credentials themselves.

#### How are HDFS permissions managed?

POSIX-like owner/group/other permissions on files and directories, plus ACLs for finer control. Fine-grained, central policies are usually managed with Apache Ranger.

#### What is Apache Ranger?

A centralized security framework for Hadoop that defines and audits access policies (HDFS paths, Hive databases, tables, columns, row filters and masking, HBase, Kafka) with plugins enforcing them in each service.

#### What is Apache Atlas?

A metadata and governance service providing data catalog, lineage, classification (tags like PII) and integration with Ranger for tag-based policies.

#### What is Apache Knox?

A gateway that provides a single, secure entry point (REST APIs, UIs) to Hadoop services for users outside the cluster, handling authentication and SSL.

#### How is data encrypted in Hadoop?

In transit with RPC encryption, TLS for web UIs and data transfer encryption; at rest with HDFS transparent encryption using encryption zones whose keys are managed by the Hadoop Key Management Server (KMS).

#### What is a keytab?

A file containing a Kerberos principal's keys, used by services and batch jobs to authenticate without a password; keytabs must be protected like passwords.

#### What is impersonation (proxy users) in Hadoop?

A configuration allowing a trusted service (HiveServer2, Livy, Oozie) to act on behalf of end users, so permissions and audits reflect the real user rather than the service account.

#### How do you audit access in Hadoop?

HDFS audit logs on the NameNode record every file access; Ranger collects audit events from all its plugins into Solr or HDFS, and Atlas records lineage.

### Operations and performance

#### How do you size a Hadoop cluster?

From data volume (raw size × replication factor × growth, plus temporary space), processing needs (CPU and memory for concurrent jobs), and throughput targets; leave room for failures and rebalancing (often keep disks under 70–80% full).

#### What are common causes of slow Hadoop jobs?

Data skew (a few reducers with most keys), too many small files, insufficient or excessive parallelism, spills to disk from small memory buffers, non-splittable compressed inputs, lack of data locality, and contention in YARN queues.

#### How do you tune MapReduce memory?

Set `mapreduce.map.memory.mb` and `mapreduce.reduce.memory.mb` for container sizes and `-Xmx` in `mapreduce.map.java.opts` to around 80% of the container, and adjust `mapreduce.task.io.sort.mb` to reduce spills.

#### How do you handle data skew in Hadoop jobs?

Use combiners, custom partitioners, salting of hot keys, map-side joins for small tables, Hive skew join optimizations (`hive.optimize.skewjoin`), or pre-aggregation.

#### How do you monitor a Hadoop cluster?

With the NameNode and ResourceManager web UIs, JMX metrics, Cloudera Manager (or historically Ambari), Prometheus exporters and Grafana, and alerts on HDFS capacity, dead or slow nodes, under-replicated blocks, NameNode heap and RPC latency, and queue usage.

#### How do you upgrade a Hadoop cluster?

Plan with release notes and compatibility checks, back up NameNode metadata, use rolling upgrades when supported (HA NameNodes, DataNodes one by one), test jobs in a staging cluster, and keep the ability to roll back until finalized.

#### How do you back up HDFS?

With snapshots for user errors, `distcp` to another cluster or object storage for disaster recovery, and backups of NameNode metadata (`fsimage` and edits). Replication within the cluster isn't a backup.

#### What is the impact of JVM garbage collection on Hadoop services?

Long GC pauses on the NameNode or RegionServers make them unresponsive, causing timeouts, failovers or missed heartbeats. Size heaps carefully, use modern collectors (G1), and monitor GC logs.

#### How do you find which jobs use the most cluster resources?

YARN ResourceManager UI and APIs (memory-seconds and vcore-seconds per application), queue metrics, Spark and MapReduce history servers, and cluster management tools' usage reports.

#### How do you clean up a cluster running out of space?

Find large and old directories (`hdfs dfs -du -h`), empty trash, delete obsolete temporary data and old snapshots, reduce replication for cold data or apply erasure coding, compress or convert data to columnar formats, and add capacity if needed.

#### What is the purpose of `mapreduce.job.reduce.slowstart.completedmaps`?

It sets the fraction of maps that must finish before reducers start fetching output; starting reducers too early wastes slots waiting, too late delays the shuffle.

### Hadoop and the cloud

#### How does HDFS compare with Amazon S3?

HDFS couples storage and compute on the same nodes, gives data locality and strong consistency, and requires cluster management. S3 is managed object storage, independently scalable, cheaper and highly durable, accessed over the network; it's now strongly consistent too. Most cloud data lakes use object storage instead of HDFS.

#### What is the S3A connector?

The Hadoop file system connector (`s3a://`) that lets Hadoop, Hive and Spark read and write S3 as if it were a file system, with optimizations for multipart uploads, committers that avoid slow renames, and credentials providers.

#### Why are renames a problem on object storage?

Object stores don't have real directories; a "rename" is a copy plus delete of every object, which is slow and not atomic. Hadoop's output committers that rely on renames are slow or unsafe on S3, so S3A committers (magic, staging) or table formats (Iceberg, Delta) are used.

#### What is Amazon EMR?

A managed big data platform on AWS that runs Hadoop, Spark, Hive, HBase, Presto/Trino, Flink and others on EC2, EKS or serverless, using S3 (EMRFS/S3A) as primary storage and the Glue Data Catalog as metastore, with transient or long-running clusters.

#### What is a transient cluster?

A cluster created for a job or pipeline and terminated afterwards, with data kept in object storage. It avoids paying for idle clusters and makes environments reproducible.

#### How would you migrate a Hadoop data lake to the cloud?

Inventory data, jobs and dependencies; copy data to object storage with `distcp` or transfer services; convert tables to open formats (Parquet, then Iceberg or Delta); move the metastore to a managed catalog (Glue, Unity Catalog); port Hive and MapReduce jobs to Spark or SQL engines; replace Oozie with Airflow; re-create security with cloud IAM and catalog permissions; and validate results in parallel before decommissioning.

#### What replaced Hadoop's components in modern stacks?

HDFS → object storage (S3, ADLS, GCS); YARN → Kubernetes or managed serverless compute; MapReduce → Spark, Flink, SQL engines; Hive Metastore → Glue, Unity Catalog, Polaris and other catalogs; Hive tables → Iceberg, Delta, Hudi; Oozie → Airflow, Dagster; Ranger/Atlas → cloud-native governance (Lake Formation, Unity Catalog).

#### What are open table formats, and how do they relate to Hive tables?

Iceberg, Delta Lake and Hudi add a transactional metadata layer over Parquet files, solving Hive tables' problems (no ACID on object storage, slow partition listing, unsafe concurrent writes, painful schema evolution). They are the modern successors of Hive-style tables.

#### What is EMRFS?

Amazon EMR's implementation of the Hadoop file system for S3, with features like consistent views (historically), encryption and IAM role mapping; recent EMR versions also support S3A.

#### Can you run Hadoop on Kubernetes?

Parts of it, yes: Spark and Flink run natively on Kubernetes, Hive Metastore and Trino run as services, and storage moves to object stores. Running HDFS and YARN on Kubernetes is possible but rarely worth the complexity.

#### What are Google Dataproc and Azure HDInsight?

Managed Hadoop and Spark services on Google Cloud and Azure, similar to EMR, creating clusters in minutes with object storage (GCS, ADLS) as the main storage. Azure has been steering users towards Fabric and Databricks for new work.

#### How do costs differ between on-premises Hadoop and cloud data lakes?

On-premises clusters have high fixed costs (hardware, data centers, staff) and are sized for peaks; cloud lakes have pay-per-use storage and compute that can scale to zero, but require cost governance to avoid runaway usage.

### Spark on Hadoop

#### How does Spark read data from HDFS?

Through the Hadoop `FileSystem` API and input formats: each HDFS block (or Parquet row group range) becomes a partition, and YARN schedules executors with locality preferences close to the blocks.

#### How does Spark use the Hive Metastore?

With `enableHiveSupport()` (or the catalog configuration), Spark reads table definitions, partitions and locations from the metastore, so `spark.table("db.table")` and Spark SQL work on Hive tables, and Spark can create tables visible to Hive.

#### How do you submit a Spark job to YARN?

```bash
spark-submit \
  --master yarn --deploy-mode cluster \
  --queue etl \
  --num-executors 20 --executor-cores 4 --executor-memory 8g \
  --conf spark.executor.memoryOverhead=1g \
  --conf spark.sql.shuffle.partitions=400 \
  jobs/curate_orders.py --date 2026-10-15
```

#### What is dynamic allocation for Spark on YARN?

A feature where Spark requests and releases executors according to pending tasks, so idle executors return resources to YARN; it needs the external shuffle service (or shuffle tracking) so shuffle files survive executor removal.

#### What is the external shuffle service?

A service running in each NodeManager that serves shuffle files written by executors, so executors can be removed (dynamic allocation) or fail without losing their shuffle output.

#### How do you choose executor sizes on YARN?

Balance cores and memory: around 4–5 cores per executor for good HDFS throughput, memory per core based on the workload, overhead for off-heap needs, and leave resources for the NodeManager and OS on each node.

### Scenarios

#### The NameNode runs out of heap memory. What do you do?

Short term, increase the heap and restart in a maintenance window (with HA, fail over). Long term, reduce objects: find and compact small files, delete unused data and old snapshots, use HAR files, and consider federation or observer NameNodes.

#### A Hive query on a partitioned table scans the whole table. Why?

The filter isn't on the partition column, wraps it in a function, compares with a different type, or partitions weren't registered so the query falls back to the table location. Check the plan with `EXPLAIN` and fix filters or partitions.

#### A Spark job on YARN keeps failing with containers killed for exceeding memory. How do you fix it?

Increase `spark.executor.memoryOverhead` (off-heap memory for Python workers and buffers), reduce executor cores per executor, increase partitions to shrink per-task data, avoid large collects and caching, and check for skew.

#### Many under-replicated blocks appear after a node failure. Is it a problem?

Temporarily it's expected: the NameNode is re-replicating the dead node's blocks. Monitor progress; if it persists, check for insufficient capacity, rack constraints, decommissioning issues or network throttling (`dfs.namenode.replication.max-streams`).

#### How would you ingest a daily relational database extract into a Hadoop data lake?

Extract with Spark JDBC (parallel by key ranges) or a CDC tool, write Parquet or ORC to a dated landing directory, register partitions in the metastore, transform into curated tables with Hive or Spark, run data quality checks, and orchestrate with Airflow or Oozie.

#### How would you explain Hadoop to a non-technical stakeholder?

It's a way to store and process huge amounts of data by spreading it across many ordinary computers that work together, so the system keeps working even when some machines fail.

#### A job writes 50,000 small files per day into HDFS. What's your fix?

Repartition or coalesce before writing to produce files close to the block size, run periodic compaction jobs on older partitions, consider writing to a table format that compacts, and set alerts on file counts per directory.

#### Users complain the Hive cluster is slow every morning at 9. What do you check?

Queue configuration and contention (ETL still running into business hours), large ad hoc queries without partition filters, HiveServer2 and metastore load, missing statistics, and whether LLAP or more capacity is needed for interactive users.

#### HDFS is 90% full and growing. What do you do short term and long term?

Short term: delete temporary data and trash, reduce replication on cold data, enforce quotas. Long term: tier data (erasure coding, archive storage), move cold data to object storage, compress and convert to columnar formats, apply retention policies, and plan capacity.

#### You must migrate 500 Hive tables to a lakehouse in the cloud. How do you plan it?

Classify tables by size, usage and dependencies; copy data with `distcp` to object storage; convert to Iceberg or Delta (in-place migration procedures or `CTAS`); register in the new catalog; translate HiveQL jobs to Spark SQL or dbt; migrate in waves by domain, validating counts and checksums, and keep the old cluster read-only until consumers switch.

#### A NameNode failover happens and some jobs fail. Why, and how do you avoid it?

Clients configured with a single NameNode address instead of the HA nameservice fail; jobs in the middle of metadata operations may hit errors. Use the logical nameservice (`hdfs://nameservice1`) with client failover proxies, and retries in applications.
