## Hadoop Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Hadoop study guide: about 200 questions](../../images/hadoop_study_guide_title_img.png)

About 200 interview-style questions on Apache Hadoop and its ecosystem: HDFS, YARN, MapReduce, file formats, Hive, HBase, ZooKeeper, ingestion tools, security, operations and the move to cloud object storage. Hadoop is no longer the default for new platforms, but many companies still run it, and its ideas (data locality, distributed storage, resource management) underpin Spark and the lakehouse.

The guide follows a learning path in six stages. Each section is split into short units: learning goals, a concept explanation and a worked example, then questions (recall first, then application), a practical challenge and key takeaways. To **learn**, read each unit top to bottom. To **review**, switch to review mode or use "Skip to questions", mark answers you want to see again, and try a mixed review across sections.

<!-- QA -->
<!-- stage: Foundations -->

### Fundamentals

<!-- unit: Why Hadoop exists -->

<!-- goals -->

- Explain the problem Hadoop solved and where it came from.
- Describe its design principles: data locality, commodity hardware, throughput.

<!-- concept -->

In the early 2000s, web companies had more data than any single machine could store or process, and big specialized servers were too expensive. Google's answer, described in two papers, was to spread data and computation over many cheap machines and let software handle the failures that would inevitably happen.

Hadoop is the open-source version of that idea. Its central trick is moving computation to where the data already sits, because shipping code is cheap and shipping terabytes is not. It optimizes for finishing huge batch jobs, not answering quick queries.

<!-- example -->

```text
Classic approach:  data ──network──► one big server ──► result
Hadoop:            code ──► node 1 (block A)  node 2 (block B)  node 3 (block C)
                            process locally, in parallel, combine results
```

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

#### What is a commodity hardware cluster?

A cluster of standard, relatively cheap servers with local disks, as opposed to specialized high-end machines or SANs. Hadoop expects individual nodes to fail and works around it.

#### Why does Hadoop favor throughput over latency?

It was designed for scanning large datasets in batch, where total processing time matters more than the response time of individual requests; HDFS reads large blocks sequentially, and MapReduce jobs have seconds of startup overhead.

#### How would you explain Hadoop to a non-technical stakeholder?

It's a way to store and process huge amounts of data by spreading it across many ordinary computers that work together, so the system keeps working even when some machines fail.

<!-- challenge -->

A manager asks why a Hadoop query takes 40 seconds to count 10 rows when the database answers instantly. What do you explain?

<!-- solution -->

Hadoop is built for throughput on huge datasets: each job pays scheduling and startup costs that dominate for tiny queries. It's efficient when scanning terabytes, not for small interactive lookups, which a database or a low-latency engine should serve.

<!-- takeaways -->

- Hadoop spreads data and work over many cheap machines.
- It moves computation to the data.
- It optimizes for batch throughput, not latency.

<!-- unit: Versions, distributions and the ecosystem -->

<!-- goals -->

- Distinguish Hadoop 1, 2 and 3 and the main distributions.
- Describe Hadoop Common, the FileSystem abstraction and core configuration files.

<!-- concept -->

Hadoop evolved from a single-purpose MapReduce system into a platform. Version 2 separated resource management (YARN) from processing, so engines like Spark and Tez could share a cluster; version 3 added erasure coding and more NameNodes. Vendors packaged it into distributions with management tools, and dozens of projects grew around it.

Underneath, shared libraries and a file system abstraction let the same code read HDFS, local disks or object storage, configured through a few XML files.

<!-- example -->

```xml
<!-- core-site.xml -->
<property>
  <name>fs.defaultFS</name>
  <value>hdfs://prod-nameservice</value>
</property>
<!-- hdfs-site.xml -->
<property>
  <name>dfs.replication</name>
  <value>3</value>
</property>
```

#### What is the difference between Hadoop 1, 2 and 3?

Hadoop 1 combined resource management and MapReduce in the JobTracker/TaskTracker model. Hadoop 2 introduced YARN, separating resource management so other engines could run, and NameNode high availability. Hadoop 3 added erasure coding, support for more than two NameNodes, Java 8+ requirements, YARN timeline service v2, and other improvements.

#### What are the main Hadoop distributions?

Historically Cloudera, Hortonworks (merged with Cloudera in 2019) and MapR (acquired by HPE). Today Cloudera Data Platform is the main commercial distribution, and cloud services (Amazon EMR, Google Dataproc, Azure HDInsight) offer managed Hadoop ecosystems.

#### What is the Hadoop ecosystem?

The set of projects built around Hadoop: Hive (SQL), HBase (NoSQL), Pig (scripting), Spark (fast processing), Kafka (streaming), ZooKeeper (coordination), Oozie (workflows), Sqoop and Flume (ingestion), Ranger and Atlas (security and governance), Impala and Presto/Trino (interactive SQL), and others.

#### What is Hadoop Common?

The shared libraries and utilities used by the other Hadoop modules: file system abstractions, RPC, serialization, configuration, security and command-line tools.

#### What is the Hadoop `FileSystem` abstraction?

A Java API that lets Hadoop applications work with different storage systems through one interface, with implementations for HDFS (`hdfs://`), local files (`file://`), S3 (`s3a://`), Azure (`abfs://`), Google Cloud Storage (`gs://`) and others.

#### What are the core configuration files of Hadoop?

`core-site.xml` (common settings such as the default file system `fs.defaultFS`), `hdfs-site.xml` (HDFS settings like replication and NameNode directories), `yarn-site.xml` (ResourceManager and NodeManager settings) and `mapred-site.xml` (MapReduce settings).

<!-- challenge -->

A team on Hadoop 1 wants to run Spark on the same cluster. What must change, and why?

<!-- solution -->

They need Hadoop 2 or later: YARN separates resource management from MapReduce, so Spark can request containers alongside other engines. Hadoop 1's JobTracker only runs MapReduce.

<!-- takeaways -->

- Hadoop 2 introduced YARN; Hadoop 3 added erasure coding.
- The ecosystem grew around a shared cluster.
- The FileSystem API abstracts HDFS, local and object storage.

<!-- unit: How Hadoop is used -->

<!-- goals -->

- Describe HDFS's write-once model, schema on read and horizontal scaling.
- Know typical workloads and the role of edge nodes.

<!-- concept -->

Hadoop clusters were used as the company's data lake: files land once, are read many times by batch jobs, and gain a schema only when a job or table interprets them. That model suits logs, ETL and warehouse-style analytics, and it scales by adding more ordinary nodes.

Users don't log into the worker nodes. They work from edge nodes that have the client tools and configuration, keeping the cluster itself clean and secure.

<!-- example -->

```text
edge node (hdfs, hive, spark-submit clients)
   │ submits jobs / reads files
   ▼
master nodes: NameNode, ResourceManager
worker nodes: DataNode + NodeManager on every machine (storage and compute together)
```

#### What does "write once, read many" mean in HDFS?

Files are written once and then mostly read; HDFS supports appends but not random updates in the middle of files. This simplifies consistency and favors batch analytics.

#### How does Hadoop scale?

Horizontally: add DataNodes for more storage and NodeManagers for more compute; HDFS rebalances data and YARN uses the new capacity. The NameNode's memory limits the number of files, which federation addresses.

#### What are the typical workloads run on Hadoop clusters?

Batch ETL, log processing, data warehousing with Hive, machine learning feature preparation with Spark, search indexing, and storing raw data in a central data lake.

#### What does "schema on read" mean in Hadoop?

Data is stored as files without enforcing a schema at write time; a schema (for example a Hive table definition) is applied when reading. It makes ingestion flexible but pushes validation to consumers.

#### What are edge nodes?

Gateway machines with Hadoop client libraries and configuration but no DataNode or NodeManager roles, from which users submit jobs, run CLI tools and host client applications without touching the worker nodes.

<!-- challenge -->

An application needs to update individual records in a file many times a day. Is HDFS a good fit?

<!-- solution -->

No. HDFS is write once, read many: it supports appends but not random updates. Use a database (or HBase for large-scale key access), or rewrite data in batches.

<!-- takeaways -->

- HDFS files are written once and read many times.
- Schema is applied when data is read.
- Clusters scale by adding nodes; users work from edge nodes.

<!-- unit: Hadoop today -->

<!-- goals -->

- Explain why new projects rarely choose Hadoop.
- Explain why Hadoop knowledge is still valuable.

<!-- concept -->

Cloud object storage changed the economics. Storage and compute no longer need to sit on the same machines, so each can scale and be paid for separately, and managed services remove the cluster operations Hadoop needs. Most new platforms start there.

Yet many banks, telecoms and enterprises still run large Hadoop clusters, and modern tools inherited its ideas: Spark, Hive's metastore, Parquet and partitioning all came from that world. Knowing Hadoop helps operate, migrate and understand what replaced it.

<!-- example -->

| Hadoop piece | Modern successor |
|---|---|
| HDFS | S3, ADLS, GCS |
| YARN | Kubernetes, serverless compute |
| MapReduce | Spark, Flink |
| Hive tables | Iceberg / Delta tables |

#### Why is Hadoop less popular for new projects today?

Cloud object storage (S3, ADLS, GCS) separates storage from compute more cheaply and elastically, Spark replaced MapReduce for processing, and managed warehouses and lakehouses (Snowflake, Databricks, BigQuery) remove cluster operations. Hadoop clusters are complex to run and tune.

#### Is Hadoop still relevant to learn?

Yes, for maintaining and migrating existing clusters (common in banks, telecoms and large enterprises), and because its concepts — distributed file systems, blocks, replication, data locality, resource managers, partitioning, shuffle — explain how Spark, Hive and modern lakehouses work.

<!-- challenge -->

In an interview, you're asked why you'd learn Hadoop in 2026. Give a two-sentence answer.

<!-- solution -->

Many large companies still run Hadoop clusters that need maintenance and migration, and the concepts behind it (distributed storage, data locality, partitioning, the metastore) underlie today's lakehouses and Spark.

<!-- takeaways -->

- Cloud separated storage from compute.
- Many clusters still need operating and migrating.
- Modern tools inherit Hadoop's ideas.

<!-- stage: Distributed storage -->

### HDFS architecture

<!-- unit: NameNode and DataNodes -->

<!-- goals -->

- Describe HDFS's components and what each stores.
- Explain heartbeats, block reports and safe mode.

<!-- concept -->

HDFS separates knowing from storing. The NameNode knows: the directory tree, permissions, which blocks form each file, and where those blocks live, all in memory. DataNodes store: blocks as plain files on local disks, serving reads and writes directly to clients.

The two sides stay in sync through constant messages. Heartbeats show a DataNode is alive; block reports tell the NameNode what it holds. At startup, the NameNode waits in a read-only safe mode until enough blocks have been reported.

<!-- example -->

```text
NameNode (memory):  /data/orders/part-0.parquet → blocks b1, b2
                    b1 → dn1, dn4, dn7     b2 → dn2, dn4, dn9
DataNode dn4 disk:  /hadoop/dfs/data/current/.../blk_b1, blk_b2
```

#### What is HDFS?

The Hadoop Distributed File System: a distributed, fault-tolerant file system that splits files into large blocks and stores replicas of each block on different machines, providing high-throughput access to large datasets.

#### What are the main components of HDFS?

The NameNode (master holding the namespace and block locations), DataNodes (workers storing blocks on local disks), and in high-availability setups a Standby NameNode, JournalNodes and ZooKeeper Failover Controllers.

#### What does the NameNode store?

The file system namespace (directories, files, permissions, which blocks make up each file) in memory, persisted as an `fsimage` checkpoint plus an `edits` log. Block locations are not persisted; they come from DataNode block reports.

#### What does a DataNode do?

It stores blocks as files on local disks, serves read and write requests from clients, sends heartbeats and block reports to the NameNode, and replicates blocks to other DataNodes when instructed.

#### What is the HDFS namespace?

The hierarchy of directories and files, with permissions, owners, quotas and modification times, maintained by the NameNode, similar to a traditional file system tree.

#### What are heartbeats and block reports?

DataNodes send a heartbeat every few seconds to show they're alive and a full block report periodically listing their blocks. If heartbeats stop for about ten minutes, the NameNode marks the node dead and re-replicates its blocks.

#### What is safe mode?

A read-only state the NameNode enters at startup while it loads the namespace and waits for DataNodes to report enough block replicas. It leaves safe mode automatically once a threshold of blocks is satisfied, or an admin can leave it manually.

<!-- challenge -->

After a NameNode restart, writes fail for 10 minutes with a "safe mode" error. Is something broken?

<!-- solution -->

Probably not. The NameNode stays in safe mode until enough DataNodes report their blocks; large clusters take minutes. Check `hdfs dfsadmin -safemode get` and the reported block percentage; only force exit if blocks are truly missing.

<!-- takeaways -->

- The NameNode holds metadata; DataNodes hold blocks.
- Heartbeats and block reports keep them in sync.
- Safe mode protects data while blocks are reported.

<!-- unit: Blocks and replication -->

<!-- goals -->

- Explain large blocks, replication and rack-aware placement.
- Compare replication with erasure coding.

<!-- concept -->

HDFS cuts files into large blocks, typically 128 MB, so the NameNode tracks few objects and disks read in long, efficient sequences. Each block is copied, three times by default, and placement is rack-aware: copies spread across racks so a rack failure doesn't lose data.

Three copies means paying for three times the storage. Erasure coding stores data with parity instead, much like RAID, cutting overhead to about half, at the cost of more CPU and network when reading or rebuilding. It suits cold data.

<!-- example -->

| Scheme | Storage overhead | Survives |
|---|---|---|
| Replication ×3 | 200% | 2 lost copies |
| Erasure coding RS-6-3 | 50% | 3 lost cells of 9 |

#### What is the default block size and why is it so large?

128 MB in Hadoop 2 and 3 (64 MB in Hadoop 1). Large blocks reduce NameNode metadata, minimize seek time relative to transfer time, and give each map task a meaningful amount of data.

#### What is the replication factor?

The number of copies of each block, 3 by default (`dfs.replication`), configurable per file. More replicas mean more durability and read parallelism but more storage.

#### What is rack awareness?

The NameNode knows which rack each DataNode is in (through a topology script) and places replicas to survive a rack failure: by default the first replica on the writer's node, the second on a node in a different rack, and the third on another node in that second rack.

#### How does HDFS handle a file smaller than a block?

It uses only as much disk as the file needs; a 1 MB file doesn't consume 128 MB. But it still costs a full metadata object in the NameNode, which is the real issue with small files.

#### What is erasure coding in HDFS?

A Hadoop 3 storage policy that stores data with parity (for example Reed-Solomon 6+3) instead of three full copies, giving similar fault tolerance with about 50% storage overhead instead of 200%. Reads and reconstruction cost more CPU and network, so it suits cold data.

<!-- challenge -->

A cluster stores 2 PB of logs older than a year that are read a few times per quarter. How can you cut their storage cost?

<!-- solution -->

Apply an erasure coding policy (for example RS-6-3) to the old log directories, reducing overhead from 200% to 50%. Keep hot data replicated for read performance.

<!-- takeaways -->

- Large blocks keep metadata small and reads efficient.
- Replicas spread across racks for safety.
- Erasure coding saves space for cold data.

<!-- unit: Metadata durability -->

<!-- goals -->

- Explain the fsimage and edits log.
- Describe the roles of the Secondary NameNode and JournalNodes.

<!-- concept -->

The NameNode keeps metadata in memory for speed, so it needs a durable record on disk. It uses two files: a full checkpoint of the namespace (fsimage) and a log of every change since (edits). On restart, it loads the checkpoint and replays the log.

If the log grows forever, restarts take forever. A helper periodically merges log into checkpoint. In high-availability setups, a small quorum of JournalNodes stores the shared log, so a standby NameNode can follow every change.

<!-- example -->

```text
fsimage_0000000000041000      (namespace at transaction 41000)
edits_0000000000041001-...    (every change since)
checkpoint: fsimage + edits → new fsimage, edits truncated
```

#### What are the `fsimage` and `edits` files?

`fsimage` is a checkpoint of the whole namespace at a point in time; `edits` is the log of every change since that checkpoint. On startup, the NameNode loads the `fsimage` and replays the edits.

#### What is the Secondary NameNode?

A helper that periodically merges the `edits` log into the `fsimage` (checkpointing) so the edits log doesn't grow forever and NameNode restarts are faster. Despite its name, it is not a standby and can't take over if the NameNode fails.

#### What are JournalNodes?

A small quorum of daemons (usually three or five) that store the shared edits log for HA NameNodes; the active NameNode writes to a majority, and standbys read from them to stay in sync.

<!-- challenge -->

A NameNode restart takes two hours. Logs show it replaying a huge edits file. What went wrong?

<!-- solution -->

Checkpointing stopped: the Secondary or Standby NameNode wasn't merging edits into the fsimage. Fix the checkpointing process and monitor the time since the last checkpoint.

<!-- takeaways -->

- fsimage is a checkpoint; edits logs changes since.
- Checkpoints keep restarts fast.
- JournalNodes share the edits log in HA setups.

<!-- unit: High availability and scaling the NameNode -->

<!-- goals -->

- Explain NameNode HA, fencing, observers and federation.
- Recognize and handle the NameNode's memory limits.

<!-- concept -->

The NameNode was Hadoop's single point of failure and its scaling limit. High availability adds standby NameNodes that follow the shared edits log and take over when the active one fails; fencing guarantees the old active can't keep writing. Clients must talk to the logical nameservice, not one host.

Scale is a memory problem: every file and block costs NameNode heap. Federation splits the namespace over several NameNodes, observers take read load, and fewer, larger files reduce the pressure.

<!-- example -->

```xml
<property><name>dfs.nameservices</name><value>prod-nameservice</value></property>
<property><name>dfs.ha.namenodes.prod-nameservice</name><value>nn1,nn2</value></property>
<!-- clients use hdfs://prod-nameservice/... never hdfs://nn1-host:8020/... -->
```

#### How does NameNode high availability work?

Two (or more, in Hadoop 3) NameNodes run: one active, the others standby. They share the edits log through a quorum of JournalNodes; DataNodes report to all of them. ZooKeeper Failover Controllers monitor health and trigger automatic failover, with fencing to prevent two active NameNodes (split brain).

#### What is fencing in NameNode HA?

Mechanisms that ensure a former active NameNode can no longer modify the namespace after failover (for example killing its process or relying on JournalNodes accepting writes from only one writer epoch), preventing split brain.

#### What is the Observer NameNode?

A read-only NameNode (Hadoop 3) that serves read requests with consistent state, offloading the active NameNode in clusters with heavy metadata read traffic.

#### What is HDFS federation?

Several independent NameNodes, each managing part of the namespace (for example `/user` and `/data`), sharing the same DataNodes. It scales the namespace beyond one NameNode's memory and isolates workloads. ViewFs or Router-based federation present a unified view.

#### Why is the NameNode a scalability bottleneck?

All metadata lives in its memory: roughly 150 bytes per file, directory and block. Hundreds of millions of objects need a lot of heap, and every metadata operation goes through it. Federation, observer NameNodes and avoiding small files help.

#### The NameNode runs out of heap memory. What do you do?

Short term, increase the heap and restart in a maintenance window (with HA, fail over). Long term, reduce objects: find and compact small files, delete unused data and old snapshots, use HAR files, and consider federation or observer NameNodes.

#### A NameNode failover happens and some jobs fail. Why, and how do you avoid it?

Clients configured with a single NameNode address instead of the HA nameservice fail; jobs in the middle of metadata operations may hit errors. Use the logical nameservice (`hdfs://nameservice1`) with client failover proxies, and retries in applications.

<!-- challenge -->

NameNode heap usage grows 5% a month, mostly from millions of tiny files. Besides adding memory, what do you do?

<!-- solution -->

Attack the file count: compact small files into large ones (or archive them), fix the jobs producing them, set name quotas on directories, and consider federation if the namespace keeps growing.

<!-- takeaways -->

- Standby NameNodes and fencing provide HA.
- Clients must use the HA nameservice.
- NameNode memory scales with file and block counts.

### HDFS operations

<!-- unit: Reads, writes and integrity -->

<!-- goals -->

- Describe how HDFS reads and writes data.
- Explain checksums, short-circuit reads and WebHDFS.

<!-- concept -->

Data never flows through the NameNode. To write, a client asks it where to place a block, then streams data to a pipeline of DataNodes that pass it along and acknowledge. To read, the client gets block locations and reads directly from the nearest DataNode.

Integrity is checked everywhere: checksums are computed on write and verified on read, so corruption is detected and served from another replica. Local readers can skip the network entirely, and remote clients can use a REST API.

<!-- example -->

```text
write: client ──► dn1 ──► dn4 ──► dn7   (pipeline, acks flow back)
read:  client ──► NameNode: "where is b1?" ──► dn4 (closest) ──► data
```

#### How does an HDFS write work?

The client asks the NameNode to create the file; for each block, the NameNode returns a list of DataNodes. The client streams data in packets to the first DataNode, which forwards to the second, which forwards to the third (a pipeline). Acknowledgements flow back, and the file is visible once closed.

#### How does an HDFS read work?

The client asks the NameNode for the block locations of the file, then reads each block directly from the closest DataNode holding a replica, verifying checksums; if a DataNode fails, it switches to another replica.

#### How does HDFS detect corrupted data?

Each block has checksums computed at write time; clients verify them on read, and DataNodes run a background block scanner. Corrupt replicas are reported to the NameNode, which re-replicates from a healthy copy.

#### What is short-circuit local read?

When the client runs on the same node as the DataNode holding a block, it reads the file directly from local disk through a shared file descriptor, bypassing the DataNode's network path, which speeds up reads.

#### What is WebHDFS?

A REST API to HDFS over HTTP, allowing clients in any language to read, write and manage files without Hadoop libraries; HttpFS provides a gateway version.

<!-- challenge -->

A disk silently corrupts a few blocks. Do users get wrong data? What happens?

<!-- solution -->

No. Checksums fail on read, so the client reads another replica and reports the corrupt one; the NameNode schedules a new healthy copy. DataNode block scanners also find corruption proactively.

<!-- takeaways -->

- Data flows directly between clients and DataNodes.
- Writes use a replication pipeline.
- Checksums detect and route around corruption.

<!-- unit: Everyday HDFS commands -->

<!-- goals -->

- Move and inspect data with `hdfs dfs` commands.
- Check health and capacity with `fsck` and `dfsadmin`.

<!-- concept -->

Most daily HDFS work is a small set of commands that look like Unix ones: list, copy, move, count sizes. Administration adds health checks: `fsck` reports missing, corrupt or under-replicated blocks per path, and `dfsadmin` shows capacity and node status across the cluster.

Changing replication for existing data is also a command, useful for raising protection on critical data or lowering it on scratch space.

<!-- example -->

```bash
hdfs dfs -mkdir -p /data/raw/orders/dt=2026-10-17
hdfs dfs -put orders.csv /data/raw/orders/dt=2026-10-17/
hdfs dfs -du -h /data/raw | sort -h | tail
hdfs dfs -count -q /data/raw/orders
hdfs fsck /data/raw/orders -files -blocks | tail
hdfs dfsadmin -report | head -20
```

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

#### How do you move data between HDFS and the local file system?

`hdfs dfs -put`/`-copyFromLocal` to upload, `hdfs dfs -get`/`-copyToLocal` to download, and `hdfs dfs -getmerge` to concatenate a directory of part files into one local file.

#### What does `hdfs dfs -count` show?

The number of directories, files and bytes under a path, and with `-q` the name and space quotas, useful to find directories with too many small files.

#### What does `hdfs fsck` do?

It checks the health of files and blocks: missing, corrupt, under-replicated or mis-replicated blocks, and can list block locations (`hdfs fsck /path -files -blocks -locations`). It reads metadata only and doesn't fix problems itself.

#### What does `hdfs dfsadmin -report` show?

Cluster capacity, used and remaining space, and per-DataNode status (live, dead, decommissioning), useful for a quick health check.

#### How do you change the replication factor of existing data?

With `hdfs dfs -setrep -w <n> <path>`, which changes the replication of the files and waits until replicas are added or removed.

<!-- challenge -->

A user says a critical dataset "might be damaged". Which commands do you run, and what do you look for?

<!-- solution -->

`hdfs fsck <path> -files -blocks -locations` for missing, corrupt or under-replicated blocks, and `hdfs dfsadmin -report` for dead DataNodes. If blocks are missing with no live replica, restore from a snapshot or backup.

<!-- takeaways -->

- `hdfs dfs` covers file operations.
- `fsck` checks block health per path.
- `dfsadmin -report` shows cluster capacity and nodes.

<!-- unit: Node failures and maintenance -->

<!-- goals -->

- Explain what happens when a DataNode fails.
- Balance, decommission and tolerate disk failures safely.

<!-- concept -->

In a large cluster, some disk or node is always failing. When a DataNode stops sending heartbeats, the NameNode re-replicates its blocks from surviving copies; temporarily under-replicated blocks are normal. Nodes can also tolerate a few failed disks rather than shutting down.

Planned work uses the same mechanisms gently: decommissioning copies a node's blocks elsewhere before removal, and the balancer evens out disk usage after nodes are added.

<!-- example -->

```bash
echo "dn12.prod" >> /etc/hadoop/conf/dfs.exclude
hdfs dfsadmin -refreshNodes          # dn12 → "Decommission in progress"
hdfs dfsadmin -report | grep -A3 dn12
hdfs balancer -threshold 10          # after adding new nodes
```

#### What happens when a DataNode dies?

The NameNode stops receiving heartbeats, marks it dead after a timeout, and schedules re-replication of its blocks from remaining replicas to restore the replication factor.

#### What is the HDFS balancer?

A tool that moves blocks between DataNodes so disk usage is even across the cluster, typically run after adding nodes. The disk balancer evens usage across disks within a DataNode.

#### How do you decommission a DataNode?

Add it to the exclude file and refresh the NameNode (`hdfs dfsadmin -refreshNodes`); the NameNode re-replicates its blocks elsewhere, and once decommissioning completes the node can be removed safely.

#### What does `dfs.datanode.failed.volumes.tolerated` control?

How many disk failures a DataNode tolerates before shutting itself down; by default zero, but large nodes with many disks are often configured to keep running with one or two failed disks.

#### Many under-replicated blocks appear after a node failure. Is it a problem?

Temporarily it's expected: the NameNode is re-replicating the dead node's blocks. Monitor progress; if it persists, check for insufficient capacity, rack constraints, decommissioning issues or network throttling (`dfs.namenode.replication.max-streams`).

<!-- challenge -->

You need to remove three DataNodes for hardware replacement without risking data. What steps do you follow?

<!-- solution -->

Decommission them through the exclude file and `-refreshNodes`, wait until they show "Decommissioned" (all blocks copied elsewhere), then stop them. Run the balancer after new hardware joins.

<!-- takeaways -->

- The NameNode re-replicates blocks from dead nodes.
- Decommission before removing nodes.
- The balancer evens out disk usage.

<!-- unit: Protecting and organizing data -->

<!-- goals -->

- Use trash, snapshots and quotas to protect data.
- Place data with storage policies and copy it with `distcp`.

<!-- concept -->

HDFS offers several safety nets against mistakes. Trash keeps deleted files for a while; snapshots keep read-only, point-in-time views of directories at almost no cost; quotas stop one team from filling the cluster.

Storage policies place data on the right media, such as SSD for hot data or archive disks for cold, and `distcp` copies large datasets between clusters or into object storage using a parallel job.

<!-- example -->

```bash
hdfs dfsadmin -allowSnapshot /data/finance
hdfs dfs -createSnapshot /data/finance before-reload-2026-10-17
hdfs dfsadmin -setSpaceQuota 50t /data/marketing
hadoop distcp -update hdfs://prod/data/finance s3a://backup-bucket/finance
```

#### What is the HDFS trash?

When enabled (`fs.trash.interval`), deleted files go to a `.Trash` folder in the user's home directory and are permanently removed after the interval, protecting against accidental deletes. `-skipTrash` bypasses it.

#### What are HDFS snapshots?

Read-only, point-in-time copies of a directory (enabled per directory by an admin) that are cheap because they only record changes; used to recover from user errors and for consistent backups.

#### What are HDFS quotas?

Name quotas (maximum number of files and directories) and space quotas (maximum bytes, including replicas) set per directory, used to prevent one team from exhausting the cluster.

#### What are HDFS storage policies?

Rules that place block replicas on different storage types (DISK, SSD, ARCHIVE, RAM_DISK) according to temperature: Hot, Warm, Cold, All_SSD, One_SSD and Lazy_Persist. The mover tool relocates existing data to match a policy.

#### What is `distcp`?

A tool that copies large amounts of data between HDFS clusters or between HDFS and object storage, using MapReduce to copy in parallel, with options for incremental updates and preserving attributes.

<!-- challenge -->

Before a risky reload of a finance directory, how do you make sure you can roll back in minutes?

<!-- solution -->

Take an HDFS snapshot of the directory before the reload. If the reload goes wrong, copy the files back from the `.snapshot` path (snapshots are cheap and instant to create).

<!-- takeaways -->

- Trash and snapshots protect against mistakes.
- Quotas protect shared capacity.
- `distcp` copies large data in parallel.

<!-- unit: The small-files problem -->

<!-- goals -->

- Explain why small files hurt HDFS and the jobs that read it.
- Fix and prevent small-file growth.

<!-- concept -->

Every file, however tiny, costs NameNode memory and usually a separate task when read. Millions of small files therefore exhaust the NameNode and make jobs spend more time starting tasks than processing data.

They usually come from streaming or over-parallel jobs writing one file per task. The cure is at the source, writing fewer larger files, plus periodic compaction of what already exists.

<!-- example -->

```text
50,000 files × 200 KB  = 10 GB  → 50,000 NameNode objects, 50,000 map tasks
80 files × 128 MB      = 10 GB  → 80 objects, 80 tasks
```

#### What is the small-files problem in HDFS?

Millions of files much smaller than the block size consume NameNode memory (each file and block is an object), make listings slow and create many tiny tasks. Solutions: compact files (Hive `INSERT OVERWRITE`, Spark repartition), use container formats (SequenceFile, Parquet, ORC), or archive with HAR files.

#### A job writes 50,000 small files per day into HDFS. What's your fix?

Repartition or coalesce before writing to produce files close to the block size, run periodic compaction jobs on older partitions, consider writing to a table format that compacts, and set alerts on file counts per directory.

<!-- challenge -->

A streaming job writes one file per partition every minute. How do you stop the growth without losing freshness?

<!-- solution -->

Keep the minute files in a landing area and run an hourly or daily compaction that rewrites them into a few large files (or use a table format with compaction), then delete the originals.

<!-- takeaways -->

- Small files cost NameNode memory and task overhead.
- Write fewer, larger files at the source.
- Compact what already exists.

### File formats and compression

<!-- unit: Choosing a file format -->

<!-- goals -->

- Compare text, SequenceFile, Avro, Parquet and ORC.
- Explain splittability and when to use Avro or Parquet.

<!-- concept -->

File formats decide how much work a job does before computing anything. Text is universal but bulky and untyped. SequenceFiles and Avro store rows in binary, with Avro carrying its schema for safe evolution, which suits messages and ingestion. Columnar formats suit analytics.

Splittability decides parallelism: a format that can be read in independent chunks lets many tasks share one large file. Small-file workarounds like archives exist but don't replace better writing.

<!-- example -->

| Need | Format |
|---|---|
| Ingest Kafka events with evolving schema | Avro |
| Analytical tables queried by column | Parquet or ORC |
| MapReduce intermediate key-value data | SequenceFile |
| Archive millions of tiny files | HAR |

#### Which file formats are common in Hadoop?

Text (CSV, JSON), SequenceFile (binary key-value), Avro (row-based with embedded schema, good for ingestion and schema evolution), Parquet and ORC (columnar, compressed, with statistics, best for analytics).

#### What is a splittable file format, and why does it matter?

One that can be read in independent chunks by different tasks. Plain text, SequenceFile, Avro, Parquet and ORC are splittable; a gzip-compressed text file is not, so one task must read it entirely, limiting parallelism.

#### What is a SequenceFile?

A flat binary file of key-value pairs, splittable and compressible, used as MapReduce intermediate output and to pack many small files into one container.

#### What are HAR files?

Hadoop Archives: a way to pack many small files into a single archive (an index plus part files) to reduce NameNode objects while keeping files accessible through a `har://` path.

#### What is Avro's advantage for data pipelines?

The schema is stored with the data and supports evolution (adding fields with defaults, renaming with aliases), and its compact row format suits streaming and ingestion, often with a schema registry in Kafka.

#### How do you choose between Avro and Parquet?

Avro for row-oriented writes, streaming and messages where whole records are read and schemas evolve frequently; Parquet for analytics where queries read a few columns of many rows.

<!-- challenge -->

Raw events land as Avro, and analysts query three columns of a 200-column dataset. What layout do you suggest?

<!-- solution -->

Keep Avro for raw ingestion (schema evolution, whole records), and convert to partitioned Parquet or ORC for the analytical tables, so queries read only the columns they need.

<!-- takeaways -->

- Avro for rows and schema evolution; columnar for analytics.
- Splittable formats enable parallel reads.
- Archives help small files but don't fix their source.

<!-- unit: Columnar formats and compression -->

<!-- goals -->

- Describe how Parquet and ORC organize data.
- Choose compression codecs, including for intermediate output.

<!-- concept -->

Parquet and ORC both group rows into large chunks (row groups or stripes) and store each column separately inside them, with statistics that let readers skip chunks. ORC grew up with Hive and adds lightweight indexes; Parquet is the most widely supported across engines.

Compression multiplies the benefit, but codec choice matters: fast codecs like Snappy suit hot data and intermediate output, stronger ones save more space, and non-splittable codecs on plain text limit parallelism.

<!-- example -->

```properties
# compress map output to cut shuffle I/O
mapreduce.map.output.compress=true
mapreduce.map.output.compress.codec=org.apache.hadoop.io.compress.SnappyCodec
```

#### Which compression codecs are used in Hadoop?

Snappy and LZ4 (fast, moderate compression), gzip/Deflate (better compression, slower, not splittable for text), bzip2 (splittable, slow), LZO (splittable with an index) and ZSTD (good ratio and speed). Inside Parquet and ORC, compression is per block, so files remain splittable.

#### Why is ORC associated with Hive?

ORC (Optimized Row Columnar) was created for Hive: columnar storage with lightweight indexes, statistics and bloom filters, and it supports Hive ACID tables. Parquet is more common across other engines.

#### How does Parquet organize data?

Files contain row groups; each row group stores column chunks, divided into pages with encoding and compression; the footer holds the schema and statistics (min/max, null counts) per row group and column, enabling column pruning and predicate pushdown.

#### How does ORC organize data?

Files are divided into stripes (typically 64–256 MB) with column streams, lightweight indexes every 10,000 rows (min/max), optional bloom filters, and a footer with stripe statistics, allowing engines to skip stripes and row groups.

#### Should you compress intermediate MapReduce output?

Usually yes, with a fast codec like Snappy or LZ4 (`mapreduce.map.output.compress`), because it reduces disk and network I/O during the shuffle at a small CPU cost.

<!-- challenge -->

A job reads one 40 GB `.csv.gz` file and uses a single map task. Why, and how do you fix it?

<!-- solution -->

Gzip isn't splittable, so one task must read the whole file. Split the input before compressing, use a splittable codec (bzip2) or, better, convert to Parquet or ORC with Snappy or ZSTD.

<!-- takeaways -->

- Parquet and ORC store columns in chunks with statistics.
- Fast codecs for hot and intermediate data.
- Non-splittable compressed text limits parallelism.

<!-- stage: Compute on the cluster -->

### YARN

<!-- unit: YARN architecture -->

<!-- goals -->

- Describe YARN's components and an application's lifecycle.
- Inspect, manage and make the ResourceManager highly available.

<!-- concept -->

YARN turned Hadoop into a shared platform. The ResourceManager owns the cluster's capacity; NodeManagers offer each node's CPU and memory as containers; every application gets its own ApplicationMaster that negotiates containers and tracks its tasks. MapReduce, Spark and Tez all run this way side by side.

Because the ResourceManager is central, it runs with a standby, and a timeline service keeps history after applications finish.

<!-- example -->

```bash
yarn application -list -appStates RUNNING
yarn application -status application_1729150000000_0042
yarn logs -applicationId application_1729150000000_0042 | less
yarn application -kill application_1729150000000_0042
```

#### What is YARN?

Yet Another Resource Negotiator: Hadoop's cluster resource manager. It allocates CPU and memory in containers to applications (MapReduce, Spark, Tez, Flink), separating resource management from the processing engine.

#### What are YARN's main components?

The ResourceManager (cluster-wide scheduler and application manager), NodeManagers (per-node agents that launch and monitor containers), ApplicationMasters (one per application, negotiating resources and coordinating tasks) and containers (allocated bundles of memory and vcores).

#### What happens when you submit an application to YARN?

The client submits to the ResourceManager, which starts the ApplicationMaster in a container on some node. The ApplicationMaster requests containers for tasks, considering data locality; NodeManagers launch them; the ApplicationMaster monitors progress and reports completion.

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

<!-- challenge -->

A runaway Hive query is holding most of the cluster. How do you find and stop it from the command line?

<!-- solution -->

List running applications with `yarn application -list`, identify it by user, queue and resources, check it with `-status`, and stop it with `yarn application -kill <id>`. Then review queue limits.

<!-- takeaways -->

- The ResourceManager allocates; NodeManagers run containers.
- Each application has its own ApplicationMaster.
- The ResourceManager runs with a standby for HA.

<!-- unit: Schedulers and queues -->

<!-- goals -->

- Compare YARN schedulers and configure capacity queues.
- Use preemption, node labels and user limits.

<!-- concept -->

A shared cluster needs rules for who gets what. The Capacity Scheduler divides the cluster into queues with guaranteed shares that can borrow idle capacity. When a queue needs its guarantee back, preemption reclaims containers from borrowers.

Further controls refine the rules: node labels steer work to special hardware, and user limits stop one person from taking a whole queue.

<!-- example -->

```xml
<property><name>yarn.scheduler.capacity.root.queues</name><value>etl,analytics,adhoc</value></property>
<property><name>yarn.scheduler.capacity.root.etl.capacity</name><value>50</value></property>
<property><name>yarn.scheduler.capacity.root.analytics.capacity</name><value>35</value></property>
<property><name>yarn.scheduler.capacity.root.adhoc.capacity</name><value>15</value></property>
<property><name>yarn.scheduler.capacity.root.adhoc.maximum-capacity</name><value>30</value></property>
```

#### What schedulers does YARN offer?

The FIFO scheduler (first come, first served), the Capacity Scheduler (hierarchical queues with guaranteed capacities and elasticity, the default in most distributions) and the Fair Scheduler (shares resources fairly among running applications and queues).

#### How does the Capacity Scheduler work?

Queues are configured with guaranteed percentages of cluster capacity (for example `etl` 50%, `analytics` 30%, `adhoc` 20%), can borrow idle capacity up to a maximum, have user limits, and can preempt containers to give guaranteed capacity back.

#### What is preemption in YARN?

When a queue is below its guaranteed share and others are using more, the scheduler can kill containers of over-using applications to free resources, ensuring guarantees are met.

#### What are node labels in YARN?

Labels that partition nodes (for example `gpu` or `high-memory`), so queues and applications can be restricted to specific node groups.

#### How do you limit a user from using the whole cluster?

With scheduler queue limits: maximum capacity per queue, user limit factors, maximum applications per user and per queue, and access control lists on queues.

<!-- challenge -->

Ad hoc queries borrow all idle capacity at night, and the 05:00 ETL waits for them. What do you configure?

<!-- solution -->

Enable preemption so the ETL queue can reclaim its guaranteed share, and cap the ad hoc queue's maximum capacity and per-user limits.

<!-- takeaways -->

- Queues guarantee shares and borrow idle capacity.
- Preemption gives guarantees back.
- Labels and user limits refine allocation.

<!-- unit: Containers and resources -->

<!-- goals -->

- Configure container sizes and understand memory kills.
- Explain vcores, the DominantResourceCalculator and the shared cache.

<!-- concept -->

Every task runs in a container with a memory and CPU size. Nodes advertise what they offer, the scheduler enforces minimums and maximums, and the NodeManager kills any container that exceeds its memory. Most "killed by YARN" errors mean the container was too small for the heap plus off-heap needs.

By default only memory counts when packing containers; the dominant resource calculator adds CPU so CPU-heavy jobs don't overload nodes. Caching application files across jobs speeds up startup.

<!-- example -->

```properties
yarn.nodemanager.resource.memory-mb=114688      # 112 GB offered per node
yarn.nodemanager.resource.cpu-vcores=30
yarn.scheduler.minimum-allocation-mb=1024
yarn.scheduler.maximum-allocation-mb=32768
```

#### How are container sizes configured?

With `yarn.nodemanager.resource.memory-mb` and `.cpu-vcores` (resources a node offers), `yarn.scheduler.minimum-allocation-mb` and `maximum-allocation-mb` (allowed container sizes), and per-application requests (for example `mapreduce.map.memory.mb` or Spark executor memory plus overhead).

#### What happens when a container exceeds its memory?

The NodeManager kills it ("Container killed by YARN for exceeding memory limits"), and the task is retried. Fix it by increasing container memory or overhead, or reducing memory use per task (more partitions, less caching).

#### What are vcores?

Virtual CPU cores advertised by NodeManagers, an abstract unit YARN uses to schedule CPU; how strictly CPU is enforced depends on the resource calculator and cgroups configuration.

#### What is the DominantResourceCalculator?

A YARN resource calculator that considers both memory and CPU when scheduling (the dominant resource of each request), instead of the default that looks only at memory.

#### What is the YARN shared cache?

A feature that caches application resources (JARs, files) on nodes across applications, reducing the time and bandwidth spent localizing the same dependencies repeatedly.

<!-- challenge -->

Nodes show 90% memory allocated but 300% CPU load, and jobs crawl. What setting do you check?

<!-- solution -->

The resource calculator: with the default, only memory is considered, so too many CPU-hungry containers land on a node. Switch to the DominantResourceCalculator and set realistic vcores per container.

<!-- takeaways -->

- Containers have memory and CPU sizes with limits.
- Exceeding memory gets containers killed.
- DominantResourceCalculator schedules CPU too.

### MapReduce

<!-- unit: The MapReduce model -->

<!-- goals -->

- Explain map, shuffle and reduce with word count.
- Write jobs in Java or other languages and know why Spark replaced MapReduce.

<!-- concept -->

MapReduce splits a computation into two simple functions. Map turns each input record into key-value pairs; the framework groups all values by key; reduce combines each key's values into a result. Because both functions work on independent pieces, the framework can run thousands of them in parallel and retry any that fail.

The model's weakness is that every stage writes to disk, so multi-step pipelines become chains of slow jobs. Spark kept the idea and kept data in memory between stages.

<!-- example -->

```text
input:  "to be or not to be"
map:    (to,1) (be,1) (or,1) (not,1) (to,1) (be,1)
shuffle: be→[1,1]  not→[1]  or→[1]  to→[1,1]
reduce: (be,2) (not,1) (or,1) (to,2)
```

#### What is MapReduce?

A programming model and execution engine for batch processing: a map function processes input records into intermediate key-value pairs, the framework groups all values by key (shuffle and sort), and a reduce function aggregates each key's values into results.

#### Explain word count in MapReduce.

The mapper reads lines and emits `(word, 1)` for each word. The shuffle groups pairs by word. The reducer receives `(word, [1, 1, 1, …])` and emits `(word, sum)`. A combiner can sum locally after the map to reduce shuffled data.

#### What are the main classes of a MapReduce job in Java?

A `Mapper` subclass with a `map()` method, a `Reducer` subclass with `reduce()`, and a driver that configures the `Job` (input and output formats and paths, key and value types, number of reducers) and submits it.

#### What is Hadoop Streaming?

A utility that lets you write mappers and reducers in any language that reads stdin and writes stdout (Python, bash), with Hadoop handling distribution, which was popular before PySpark.

#### What is a map-only job used for?

Transformations that don't need grouping, such as filtering, format conversion or parsing logs, setting the number of reducers to zero so mapper output is written directly.

#### Why was MapReduce replaced by Spark for most workloads?

MapReduce writes intermediate results to disk between every stage and expresses complex pipelines as chains of jobs, which is slow and verbose. Spark keeps data in memory across stages, optimizes whole DAGs, and offers high-level APIs (SQL, DataFrames) in several languages.

<!-- challenge -->

A pipeline of five MapReduce jobs runs for three hours, mostly writing and reading intermediate data. What would moving it to Spark change?

<!-- solution -->

Spark runs the five steps as one application with a DAG of stages, keeping intermediate data in memory (or local disk only at shuffles) instead of writing to HDFS between jobs, typically cutting runtime substantially.

<!-- takeaways -->

- Map emits key-value pairs; reduce combines per key.
- Parallelism and retries come from independent tasks.
- Disk between stages made MapReduce slow for pipelines.

<!-- unit: Inputs and outputs -->

<!-- goals -->

- Explain InputSplits, RecordReaders and input/output formats.
- Handle many small inputs and atomic output commits.

<!-- concept -->

Before a mapper sees a record, the framework decides how to divide the input (splits, usually one per block) and how to turn bytes into records (a RecordReader from the input format). On the way out, an output format writes results, and a committer makes them appear all at once, so readers never see half a job's output.

Many small input files would mean many tiny splits; combining them into fewer splits keeps task counts sane.

<!-- example -->

```java
job.setInputFormatClass(CombineTextInputFormat.class);
CombineTextInputFormat.setMaxInputSplitSize(job, 256L * 1024 * 1024);   // pack small files
job.setOutputFormatClass(TextOutputFormat.class);
```

#### What is an InputSplit?

A logical chunk of input assigned to one map task, usually corresponding to an HDFS block. The number of splits determines the number of map tasks.

#### What is a RecordReader?

The component that reads an InputSplit and turns it into key-value records for the mapper, for example `LineRecordReader` gives (byte offset, line).

#### What are InputFormat and OutputFormat?

`InputFormat` defines how input is split and read (`TextInputFormat`, `SequenceFileInputFormat`, `KeyValueTextInputFormat`, `CombineFileInputFormat` for many small files); `OutputFormat` defines how results are written (`TextOutputFormat`, `SequenceFileOutputFormat`).

#### What is `CombineFileInputFormat` used for?

Packing many small files into fewer splits, so a job over thousands of small files doesn't launch thousands of tiny map tasks.

#### What is the role of the OutputCommitter?

It makes job output appear atomically: tasks write to temporary directories and the committer moves results to the final location when the job succeeds, so failed or speculative attempts don't leave partial output.

<!-- challenge -->

A job over 20,000 files of 100 KB each launches 20,000 map tasks and runs slowly. What do you change?

<!-- solution -->

Use `CombineFileInputFormat` (or `CombineTextInputFormat`) to pack small files into splits of a few hundred MB, so a few dozen tasks do the work. Long term, compact the files.

<!-- takeaways -->

- Splits divide input; RecordReaders produce records.
- Combine small files into larger splits.
- Committers make output appear atomically.

<!-- unit: Shuffle, combiners and partitioners -->

<!-- goals -->

- Explain shuffle and sort and how combiners reduce it.
- Control partitioning, reducer counts and secondary sorts.

<!-- concept -->

The shuffle is where MapReduce spends most of its effort: map output is partitioned by key, sorted, written to disk and fetched by reducers over the network. Anything that shrinks it helps. A combiner pre-aggregates on the map side, so far less data travels.

Partitioning decides which reducer gets each key, and the number of reducers decides parallelism. Custom partitioners spread skewed keys; a secondary sort delivers values to the reducer already ordered.

<!-- example -->

```java
job.setMapperClass(WordMapper.class);
job.setCombinerClass(SumReducer.class);   // safe: sum is associative and commutative
job.setReducerClass(SumReducer.class);
job.setNumReduceTasks(40);
```

#### What happens during shuffle and sort?

Map outputs are partitioned by key, sorted and spilled to local disk; reducers fetch their partitions from all mappers over the network, merge-sort them, and feed grouped keys to the reduce function. It's usually the most expensive phase.

#### What is a combiner?

An optional "mini-reducer" that runs on map output before the shuffle to pre-aggregate values per key, reducing network transfer. It must be safe to apply zero, one or many times (associative and commutative operations like sum, max).

#### What is a partitioner?

The function that decides which reducer receives each key, by default `hash(key) % numReducers`. Custom partitioners control data distribution, for example to avoid skew or to group related keys.

#### How do you choose the number of reducers?

Enough to parallelize the reduce work and keep each reducer's input reasonable, typically around 0.95 or 1.75 times the reduce slots or based on output size; zero reducers make a map-only job.

#### What is a secondary sort?

A technique to have values arrive at the reducer sorted by a secondary field, using a composite key, a custom partitioner on the natural key and a grouping comparator.

<!-- challenge -->

A job computes an average per key and someone adds the reducer as a combiner. Results are wrong. Why?

<!-- solution -->

Averages aren't associative: averaging partial averages ignores counts. Emit (sum, count) from the combiner and compute sum/count in the reducer.

<!-- takeaways -->

- The shuffle dominates MapReduce cost.
- Combiners shrink map output when the function is associative.
- Partitioners and reducer counts control parallelism.

<!-- unit: Running jobs well -->

<!-- goals -->

- Use counters, the distributed cache and speculative execution.
- Join datasets and size tasks sensibly.

<!-- concept -->

A few tools make jobs observable and efficient. Counters report what happened, such as malformed records or bytes spilled. The distributed cache ships small lookup files to every task, enabling map-side joins with small tables; large datasets need reduce-side joins.

Speculative execution fights slow nodes by running duplicates of straggling tasks. Task size matters too: tasks that finish in seconds waste most of their time starting up.

<!-- example -->

```java
context.getCounter("quality", "MALFORMED_RECORDS").increment(1);
job.addCacheFile(new URI("/ref/country_codes.csv#countries"));  // map-side join lookup
```

#### What is speculative execution?

When some tasks run much slower than others (stragglers), the framework launches duplicate attempts on other nodes and uses whichever finishes first. It helps with slow hardware but wastes resources and should be disabled for non-idempotent side effects.

#### What are counters?

Named numbers that tasks increment (built-in ones like records read, bytes written, spilled records, and custom ones like "invalid rows"), aggregated across the job for monitoring and validation.

#### What is the distributed cache?

A mechanism to ship read-only files (lookup tables, JARs, configuration) to every node running tasks of a job, so tasks can read them locally.

#### How do you do a join in MapReduce?

A reduce-side join tags records from both datasets, emits them by join key, and joins in the reducer (general but shuffles everything). A map-side join loads the small dataset into memory through the distributed cache and joins in the mapper (fast, but one side must fit in memory).

#### Why should map tasks run for at least a minute or so?

Task startup has overhead (JVM launch, scheduling); very short tasks spend more time starting than processing. Larger splits or combined small files make tasks efficient.

<!-- challenge -->

A job joins 2 TB of transactions with a 20 MB country table using a reduce-side join, and the shuffle is huge. What do you change?

<!-- solution -->

Use a map-side join: ship the country table through the distributed cache, load it into memory in each mapper and join there, so the 2 TB never shuffles.

<!-- takeaways -->

- Counters make jobs observable.
- Small tables join on the map side via the cache.
- Speculative execution and task sizing fight slowness.

### Spark on Hadoop

<!-- unit: Spark on YARN -->

<!-- goals -->

- Run Spark on YARN with HDFS data and the Hive Metastore.
- Choose between client and cluster deploy modes.

<!-- concept -->

Spark runs on Hadoop clusters as just another YARN application: executors are containers, data comes from HDFS through Hadoop's file system API, and table definitions come from the Hive Metastore. That reuse is why Spark took over Hadoop clusters so easily.

Where the driver runs is the main choice. In client mode it runs on the submitting machine, convenient for interactive work; in cluster mode it runs inside YARN, which is what production jobs need.

<!-- example -->

```bash
spark-submit \
  --master yarn --deploy-mode cluster --queue etl \
  --num-executors 20 --executor-cores 4 --executor-memory 12g \
  --conf spark.executor.memoryOverhead=2g \
  daily_orders.py --date 2026-10-17
```

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

#### What is the difference between client and cluster deploy mode for Spark on YARN?

In client mode, the Spark driver runs on the machine that submitted the job (an edge node), useful for interactive work; in cluster mode, the driver runs inside the ApplicationMaster container on the cluster, better for production jobs that must survive the client disconnecting.

<!-- challenge -->

A nightly Spark job submitted from an edge node fails whenever someone reboots that edge node. Why, and what do you change?

<!-- solution -->

It runs in client mode, so the driver lives on the edge node and dies with it. Submit in cluster mode so the driver runs in a YARN container, independent of the client machine.

<!-- takeaways -->

- Spark on YARN reuses HDFS and the Hive Metastore.
- Client mode for interactive work; cluster mode for production.
- Executors are YARN containers.

<!-- unit: Sizing Spark on YARN -->

<!-- goals -->

- Size executors and use dynamic allocation with the external shuffle service.
- Fix containers killed for exceeding memory.

<!-- concept -->

Executor sizing balances parallelism and memory. Around four or five cores per executor keeps HDFS throughput good; memory must cover the heap plus overhead for Python workers, buffers and off-heap data, or YARN kills the container.

Dynamic allocation lets jobs grow and shrink executors with their workload, which only works if shuffle files survive executor removal, the job of the external shuffle service in each NodeManager.

<!-- example -->

```properties
spark.dynamicAllocation.enabled=true
spark.shuffle.service.enabled=true
spark.dynamicAllocation.minExecutors=2
spark.dynamicAllocation.maxExecutors=60
spark.executor.memoryOverhead=3g      # PySpark UDFs need off-heap room
```

#### What is dynamic allocation for Spark on YARN?

A feature where Spark requests and releases executors according to pending tasks, so idle executors return resources to YARN; it needs the external shuffle service (or shuffle tracking) so shuffle files survive executor removal.

#### What is the external shuffle service?

A service running in each NodeManager that serves shuffle files written by executors, so executors can be removed (dynamic allocation) or fail without losing their shuffle output.

#### How do you choose executor sizes on YARN?

Balance cores and memory: around 4–5 cores per executor for good HDFS throughput, memory per core based on the workload, overhead for off-heap needs, and leave resources for the NodeManager and OS on each node.

#### A Spark job on YARN keeps failing with containers killed for exceeding memory. How do you fix it?

Increase `spark.executor.memoryOverhead` (off-heap memory for Python workers and buffers), reduce executor cores per executor, increase partitions to shrink per-task data, avoid large collects and caching, and check for skew.

<!-- challenge -->

A PySpark job with Python UDFs keeps losing executors with "killed by YARN for exceeding memory limits", though the JVM heap looks fine. What do you change?

<!-- solution -->

Increase `spark.executor.memoryOverhead` (Python workers run outside the heap), or reduce cores per executor so fewer Python workers share it; replace UDFs with built-in functions where possible.

<!-- takeaways -->

- ~4–5 cores per executor; size heap plus overhead.
- Dynamic allocation needs the external shuffle service.
- Off-heap usage causes most YARN memory kills.

<!-- stage: The ecosystem -->

### Hive

<!-- unit: Hive and its metastore -->

<!-- goals -->

- Explain what Hive is, its metastore and its execution engines.
- Connect with HiveServer2 and Beeline, and know how HiveQL differs from SQL.

<!-- concept -->

Hive made Hadoop usable for anyone who knew SQL. Queries are translated into jobs on an execution engine, once MapReduce, now Tez or Spark, and run over files in HDFS. The metastore holds what turns files into tables: schemas, locations, partitions and formats.

That metastore outlived Hive's own engine: Spark, Trino and Impala all use it. Clients connect through HiveServer2, usually with Beeline or JDBC tools.

<!-- example -->

```bash
beeline -u "jdbc:hive2://hs2.prod:10000/default;principal=hive/_HOST@CORP.COM" \
  -e "SELECT dt, count(*) FROM sales.orders WHERE dt >= '2026-10-01' GROUP BY dt"
```

#### What is Apache Hive?

A data warehouse system on Hadoop that lets you query data in HDFS (and object storage) with a SQL dialect (HiveQL). Queries are compiled into jobs on MapReduce, Tez or Spark, and table metadata is stored in the Hive Metastore.

#### What is the Hive Metastore?

A service backed by a relational database (MySQL, PostgreSQL) that stores table definitions, columns, partitions, locations and formats. It's used by Hive, Spark, Impala, Presto/Trino and others, and AWS Glue Data Catalog is compatible with it.

#### What is HiveServer2?

The service that accepts client connections (JDBC/ODBC, Beeline) and executes HiveQL queries with authentication, concurrency and security, replacing the older Hive CLI for multi-user access.

#### What is Beeline?

The command-line JDBC client for HiveServer2, used to run queries and scripts against Hive with proper authentication.

#### What execution engines can Hive use?

MapReduce (historic, deprecated), Apache Tez (DAG-based, the usual default in Hive 2/3) and Spark (Hive on Spark). Hive LLAP adds long-running daemons with caching for interactive queries.

#### How do HiveQL and standard SQL differ?

HiveQL is mostly SQL but with Hadoop-specific features (partitions, buckets, `LATERAL VIEW explode`, SerDes, `INSERT OVERWRITE DIRECTORY`), historically limited transactions and subqueries, and schema-on-read semantics.

<!-- challenge -->

A team wants Spark and Trino to see the same tables as Hive. What do they share?

<!-- solution -->

The Hive Metastore: configure Spark (`enableHiveSupport` / catalog settings) and Trino's Hive connector to use the same metastore, so all engines see the same table definitions and partitions.

<!-- takeaways -->

- Hive translates SQL into distributed jobs.
- The metastore turns files into tables for many engines.
- HiveServer2 and Beeline are the client entry points.

<!-- unit: Tables, partitions and buckets -->

<!-- goals -->

- Distinguish managed and external tables.
- Use partitions, buckets and dynamic partition inserts correctly.

<!-- concept -->

Hive tables are directories, and their layout drives performance. Managed tables belong to Hive, so dropping them deletes data; external tables only point to data others own. Partitions are subdirectories by column value, which let queries skip everything but the relevant folders, as long as filters hit the partition column directly.

Buckets split data within partitions into a fixed number of files by hash, helping joins and sampling. Dynamic partition inserts create partitions from data, which needs limits to avoid accidental explosions.

<!-- example -->

```sql
SET hive.exec.dynamic.partition.mode=nonstrict;
INSERT OVERWRITE TABLE sales.orders PARTITION (dt)
SELECT order_id, customer_id, amount, to_date(created_at) AS dt
FROM staging.orders_raw
WHERE created_at >= '2026-10-15';
```

#### What is the difference between managed and external tables in Hive?

Hive owns managed tables' data: dropping the table deletes the files. External tables point to data managed elsewhere: dropping them only removes metadata. External tables are common for shared data lakes.

#### What are partitions in Hive?

Subdirectories by column values (`/sales/dt=2026-10-15/`); queries filtering on partition columns read only matching directories. Dynamic partitioning creates partitions from query results.

#### What is bucketing in Hive?

Dividing data within a table or partition into a fixed number of files by hashing a column, which enables efficient sampling and bucket map joins when tables are bucketed on the join key.

#### What is `MSCK REPAIR TABLE`?

A command that scans the table location for partition directories not registered in the metastore and adds them.

#### What is dynamic partition insert, and what must you watch for?

`INSERT OVERWRITE TABLE t PARTITION (dt) SELECT …, dt FROM src` creates partitions from data values. Limits (`hive.exec.max.dynamic.partitions`) exist to prevent creating thousands of partitions accidentally, and many partitions with few rows cause small files.

#### A Hive query on a partitioned table scans the whole table. Why?

The filter isn't on the partition column, wraps it in a function, compares with a different type, or partitions weren't registered so the query falls back to the table location. Check the plan with `EXPLAIN` and fix filters or partitions.

<!-- challenge -->

Someone drops a managed Hive table thinking it only removes the definition. What happened to the data, and how should shared data be defined?

<!-- solution -->

The data files were deleted with the table (unless trash or snapshots save them). Data shared with other tools or teams should be in external tables, so dropping the definition leaves files intact.

<!-- takeaways -->

- Managed tables own data; external tables point to it.
- Partitions prune only when filters hit the column directly.
- Limit dynamic partitions to avoid explosions.

<!-- unit: Loading and reading data -->

<!-- goals -->

- Load data into Hive tables and read formats with SerDes.
- Use LATERAL VIEW explode and Hive's ordering clauses.

<!-- concept -->

Data gets into Hive in a few ways: moving files into a table's directory, inserting query results, or defining an external table over files that already exist. SerDes decide how bytes become columns, from delimited text to JSON or ORC.

HiveQL also has its own vocabulary for distributed data: exploding arrays into rows, and four ordering clauses that differ in whether order is global, per reducer, or just about which reducer gets which rows.

<!-- example -->

```sql
SELECT o.order_id, item.sku, item.qty
FROM sales.orders o
LATERAL VIEW explode(o.items) t AS item
WHERE o.dt = '2026-10-17'
DISTRIBUTE BY o.order_id SORT BY o.order_id;
```

#### How do you load data into Hive tables?

`LOAD DATA INPATH` (moves files into the table location), `INSERT INTO/OVERWRITE … SELECT`, `CREATE TABLE AS SELECT`, or by writing files directly to an external table's location and adding partitions.

#### What are SerDes in Hive?

Serializer/deserializers that define how rows are read from and written to files: `LazySimpleSerDe` for delimited text, `OpenCSVSerde`, JSON SerDes, `RegexSerDe`, and built-in support for ORC, Parquet and Avro.

#### What is `LATERAL VIEW explode`?

A Hive construct to turn array or map columns into multiple rows, similar to `UNNEST` in other SQL dialects.

```sql
SELECT o.order_id, item
FROM orders o
LATERAL VIEW explode(o.items) t AS item;
```

#### What is the difference between `ORDER BY`, `SORT BY`, `DISTRIBUTE BY` and `CLUSTER BY` in Hive?

`ORDER BY` produces a total order through a single reducer; `SORT BY` sorts within each reducer; `DISTRIBUTE BY` controls which reducer receives each key; `CLUSTER BY` is `DISTRIBUTE BY` plus `SORT BY` on the same columns.

<!-- challenge -->

A query with `ORDER BY` over a billion rows runs for hours on one reducer. The output only needs to be sorted within each customer. What do you use?

<!-- solution -->

`DISTRIBUTE BY customer_id SORT BY customer_id, event_time`: rows for each customer go to the same reducer and are sorted there, in parallel, without a global single-reducer sort.

<!-- takeaways -->

- Load by moving files, inserting results or external tables.
- SerDes map file contents to columns.
- `ORDER BY` is global; `SORT BY` and `DISTRIBUTE BY` scale.

<!-- unit: Hive performance and ACID -->

<!-- goals -->

- Speed up Hive with statistics, the CBO, map joins and vectorization.
- Explain Hive ACID tables.

<!-- concept -->

Hive's optimizer needs to know table sizes and value distributions to plan joins well, so statistics are the foundation of performance. With them, small tables become map joins broadcast to every task, avoiding shuffles. Vectorization processes rows in batches, using CPUs far more efficiently.

ACID tables added updates and deletes to Hive through delta files and compaction, which was the first step toward what table formats like Iceberg now provide everywhere.

<!-- example -->

```sql
ANALYZE TABLE sales.orders PARTITION (dt) COMPUTE STATISTICS;
ANALYZE TABLE sales.orders PARTITION (dt) COMPUTE STATISTICS FOR COLUMNS;
SET hive.cbo.enable=true;
SET hive.auto.convert.join=true;
SET hive.vectorized.execution.enabled=true;
```

#### What is the Hive cost-based optimizer?

Apache Calcite-based optimization using table and column statistics (`ANALYZE TABLE … COMPUTE STATISTICS`) to choose join orders and strategies; without statistics, plans can be poor.

#### How do you compute statistics in Hive?

`ANALYZE TABLE t PARTITION (dt) COMPUTE STATISTICS` for table and partition stats, and `… FOR COLUMNS` for column stats, which the cost-based optimizer uses; `hive.stats.autogather` gathers basic stats on insert.

#### What is a map join in Hive?

A join where the small table is loaded into memory on each mapper (broadcast), avoiding a shuffle; Hive converts joins automatically when the small table is under a size threshold (`hive.auto.convert.join`).

#### What is Hive vectorization?

Processing batches of rows (typically 1,024) at a time with columnar operations instead of row by row, which speeds up scans, filters and aggregations on ORC data.

#### What are Hive ACID tables?

Transactional ORC tables (Hive 3 managed tables) supporting `INSERT`, `UPDATE`, `DELETE` and `MERGE` with snapshot isolation, using delta files that are merged by compactions (minor and major).

<!-- challenge -->

A join between a large fact and a 50 MB dimension shuffles both sides. Statistics were never computed. What do you do?

<!-- solution -->

Compute table and column statistics so the optimizer knows the dimension is small, and enable automatic map join conversion; the dimension is then broadcast and the fact isn't shuffled.

<!-- takeaways -->

- Statistics drive the cost-based optimizer.
- Map joins broadcast small tables.
- ACID tables add updates and deletes via deltas.

### HBase

<!-- unit: The HBase data model -->

<!-- goals -->

- Describe HBase's data model and column families.
- Choose HBase or Hive, and know Apache Phoenix.

<!-- concept -->

HBase answers a different question than Hive: not "scan everything" but "give me this row now". Its tables are sorted maps from row key to column families to versioned cells, built for fast reads and writes by key at enormous scale.

Column families are stored separately, so they should be few and group data read together. Phoenix adds SQL on top for teams that want queries and secondary indexes without the raw API.

<!-- example -->

```text
row key: user#00042
  cf "profile": name="Ana", city="Bogotá"
  cf "activity": last_login@t3="2026-10-17T09:01", last_login@t2="2026-10-16T21:40"
```

#### What is HBase?

A distributed, column-family NoSQL database modeled on Google Bigtable, running on HDFS. It provides random, real-time read and write access to billions of rows by row key, with strong consistency per row.

#### What is HBase's data model?

Tables of rows sorted by row key; each row has column families (defined at table creation), each family holds any number of columns (qualifiers), and each cell keeps versions identified by timestamps. Sparse columns cost nothing.

#### What is a column family, and why should there be few of them?

A group of columns stored together in the same files with shared settings (compression, versions, TTL). Each family has its own MemStore and store files, so many families multiply flushes and compactions; two or three is typical.

#### When would you choose HBase over Hive?

HBase for low-latency random reads and writes by key (user profiles, time series lookups, counters); Hive for batch SQL analytics over large scans.

#### What is Apache Phoenix?

A SQL layer on HBase that compiles SQL into HBase scans, with secondary indexes and JDBC access.

<!-- challenge -->

An app needs the latest profile of any of 500 million users in under 10 ms, while analysts need weekly aggregates. Which store serves which need?

<!-- solution -->

HBase (row key = user ID) for low-latency lookups by key; Hive (or Spark over Parquet) for the weekly aggregates, fed from the same data.

<!-- takeaways -->

- HBase is a sorted, key-based store with versioned cells.
- Keep column families few.
- HBase for key access; Hive for scans.

<!-- unit: HBase internals -->

<!-- goals -->

- Describe HBase's components and write path.
- Explain compactions, region splits, bloom filters and TTLs.

<!-- concept -->

HBase writes fast because it never rewrites files in place. A write goes to a log for durability and to memory; memory flushes into immutable files. Over time those files pile up, so compactions merge them and drop deleted or expired data.

Tables are split into regions by key range, served by RegionServers and split further as they grow. Bloom filters let reads skip files that can't contain a row, and TTLs expire old cells automatically.

<!-- example -->

```text
put(row) → WAL on HDFS → MemStore (memory) → flush → HFile
minor compaction: merge a few HFiles
major compaction: rewrite all HFiles of a store, drop deletes and expired cells
```

#### What are HBase's main components?

The HMaster (assigns regions, handles schema changes and load balancing), RegionServers (serve reads and writes for regions), regions (contiguous row key ranges of a table), and ZooKeeper (coordination and locating the meta table).

#### How does an HBase write work?

The RegionServer appends the edit to the write-ahead log (WAL) on HDFS for durability, then writes it to the in-memory MemStore. When the MemStore fills, it flushes to an immutable HFile on HDFS.

#### What are compactions in HBase?

Background processes that merge HFiles: minor compactions merge a few small files; major compactions rewrite all files of a store into one, removing deleted and expired cells. Major compactions are I/O heavy and often scheduled off-peak.

#### What is a region split?

When a region grows beyond a configured size, the RegionServer splits it into two regions at a middle row key, and the HMaster may move them to balance load. Pre-splitting tables avoids initial hotspots.

#### What is a bloom filter in HBase?

A per-store-file structure that tells whether a row (or row and column) might exist in the file, letting reads skip files that certainly don't contain the key, reducing disk reads for random gets.

#### What is a TTL in HBase?

A time-to-live set per column family; cells older than the TTL are removed during compactions, which is useful for time series and caches.

<!-- challenge -->

Read latency spikes every Sunday at 02:00 on an HBase cluster. What is a likely cause and fix?

<!-- solution -->

Scheduled major compactions rewriting all store files compete with reads. Disable time-based major compactions and run them manually or throttled during quieter windows, per table.

<!-- takeaways -->

- Writes go to the WAL and MemStore, then HFiles.
- Compactions merge files and drop old data.
- Regions split by key range as they grow.

<!-- unit: Designing for access -->

<!-- goals -->

- Design row keys that avoid hotspots.
- Read HBase efficiently with gets, scans and filters.

<!-- concept -->

In HBase, the row key is the index, the partitioning and the sort order at once. A key that increases over time, like a timestamp, sends all writes to the last region, a hotspot. Salting, hashing or reversing keys spreads writes, at the cost of harder range scans.

Reads follow the same logic: fetch single rows by key, scan ranges with start and stop keys, and limit columns and versions to what's needed.

<!-- example -->

```text
bad:  20261017T090112#sensor42      → all writes hit the newest region
good: 7#sensor42#20261017T090112    → salt (hash(sensor) % 16) spreads writes
scan: start=7#sensor42#20261017  stop=7#sensor42#20261018
```

#### Why is row key design so important in HBase?

All access is by row key, and rows are sorted and split into regions by key. Monotonically increasing keys (timestamps, sequences) send all writes to one region (hotspotting). Use salting, hashing or field reversal, and design keys around the main access patterns.

#### How do you read from HBase efficiently?

Use `Get` for single rows by key and `Scan` with start and stop row keys for ranges, add filters to reduce data returned, set caching and batching for scans, and avoid full table scans in latency-sensitive paths.

<!-- challenge -->

An IoT table keyed by timestamp handles writes on only one RegionServer while others idle. Redesign the key.

<!-- solution -->

Prefix the key with a salt or the device ID (for example `hash(device) % N # device # timestamp`), so writes spread over regions, while scans for one device remain range scans.

<!-- takeaways -->

- The row key decides distribution and access.
- Monotonic keys create write hotspots.
- Use gets and bounded scans with filters.

### Other ecosystem tools

<!-- unit: Coordination and orchestration -->

<!-- goals -->

- Explain ZooKeeper's role in coordinating Hadoop services.
- Describe Oozie, Ambari and Livy.

<!-- concept -->

Distributed services need to agree on things: who is the active master, which nodes are alive, what the current configuration is. ZooKeeper provides that small, reliable shared state, and many Hadoop components depend on it for failover.

Around the cluster, other tools manage work and operations: Oozie schedules workflows of Hadoop jobs, Ambari installs and monitors services, and Livy lets applications submit Spark jobs over REST.

<!-- example -->

```text
ZooKeeper ensemble (3 or 5 nodes)
 ├─ NameNode HA: ZKFC elects the active NameNode
 ├─ ResourceManager HA leader election
 └─ HBase: active HMaster, RegionServer membership
```

#### What is ZooKeeper?

A centralized coordination service providing a hierarchical key-value store (znodes), watches, and consensus (ZAB protocol). Hadoop components use it for leader election (NameNode and ResourceManager HA), configuration and service discovery; older Kafka versions used it too.

#### What is Apache Oozie?

A workflow scheduler for Hadoop jobs (MapReduce, Hive, Pig, Sqoop, shell) defined in XML, with coordinators for time and data triggers. Most teams have moved to Airflow or other orchestrators.

#### What is Apache Ambari?

A web-based tool for provisioning, managing and monitoring Hadoop clusters (installing services, configuration, alerts), mainly used with Hortonworks distributions; Cloudera Manager plays the same role on Cloudera.

#### What is Apache Livy?

A REST service for submitting Spark jobs and interactive sessions to a cluster, used by notebooks and applications that can't run a Spark driver themselves.

<!-- challenge -->

Why does a ZooKeeper ensemble have three or five nodes, never two or four?

<!-- solution -->

It needs a majority (quorum) to operate. Three nodes tolerate one failure and five tolerate two; four tolerates only one, like three, and two tolerates none, so even numbers add cost without resilience.

<!-- takeaways -->

- ZooKeeper provides coordination and leader election.
- Oozie schedules Hadoop workflows.
- Ambari manages clusters; Livy submits Spark over REST.

<!-- unit: Ingestion tools -->

<!-- goals -->

- Describe Sqoop, Flume and Kafka's roles in Hadoop architectures.
- Choose an ingestion path for databases, logs and events.

<!-- concept -->

Data reached Hadoop through specialized tools. Sqoop moved tables between relational databases and HDFS with parallel jobs. Flume collected log lines from many servers and delivered them in batches. Kafka became the durable buffer between producers and everything downstream.

Sqoop and Flume are retired or rarely chosen now, replaced by Spark JDBC, CDC tools and Kafka connectors, but their patterns remain.

<!-- example -->

| Source | Classic tool | Modern equivalent |
|---|---|---|
| Relational DB tables | Sqoop | Spark JDBC, CDC (Debezium) |
| Server log files | Flume | Kafka + connectors, Fluent Bit |
| Event streams | Kafka | Kafka |

#### What was Apache Sqoop?

A tool to transfer data between relational databases and Hadoop (import into HDFS/Hive, export back) using parallel MapReduce tasks. It was retired to the Apache Attic in 2021; Spark JDBC, DMS-like tools and CDC tools replaced it.

#### What is Apache Flume?

A service for collecting, aggregating and moving large amounts of log data from many sources into HDFS or HBase, with sources, channels and sinks. Kafka has largely replaced it.

#### What is Kafka's role in Hadoop architectures?

A durable, scalable message log that ingests streams (events, CDC) and decouples producers from consumers; data is then written to HDFS or object storage by Kafka Connect, Spark Streaming or Flink.

<!-- challenge -->

A cluster still imports a database nightly with Sqoop, which is unmaintained. What do you replace it with?

<!-- solution -->

A Spark JDBC job reading in parallel by key ranges (or a CDC tool for incremental changes), writing Parquet or ORC partitions, scheduled by the existing orchestrator.

<!-- takeaways -->

- Sqoop moved databases; Flume moved logs.
- Kafka decouples producers and consumers.
- Modern stacks use Spark JDBC, CDC and connectors.

<!-- unit: Processing and query engines -->

<!-- goals -->

- Compare Pig, Tez, Impala and Trino with Spark.
- Describe how Spark and Ozone fit on Hadoop clusters.

<!-- concept -->

Engines on Hadoop evolved to cut MapReduce's overhead. Pig offered a scripting language that compiled to jobs. Tez ran a whole query as one graph instead of chained jobs. Impala and Trino used long-running daemons for interactive SQL without job startup. Spark generalized it all with in-memory processing.

Storage evolved too: Ozone brings an object store with an S3 API to Hadoop clusters, easing the small-files and NameNode limits.

<!-- example -->

| Engine | Style | Typical use |
|---|---|---|
| Pig (retired) | Data flow scripts | Legacy ETL |
| Hive on Tez | SQL as DAG | Batch SQL |
| Impala / Trino | MPP daemons | Interactive SQL |
| Spark | DAG, in memory | ETL, ML, SQL |

#### What was Apache Pig?

A high-level data flow language (Pig Latin) that compiled scripts into MapReduce or Tez jobs, popular for ETL before Spark and Hive matured; it's rarely used for new work.

#### What is Apache Tez?

A DAG execution framework on YARN that runs Hive and Pig jobs as a single graph of tasks, avoiding MapReduce's per-stage disk writes and job startup costs.

#### What are Impala and Presto/Trino?

MPP SQL engines that query data in HDFS and object storage directly with long-running daemons, giving interactive latency compared with Hive on MapReduce. Trino (formerly PrestoSQL) is widely used and powers Amazon Athena.

#### How does Spark run on a Hadoop cluster?

Spark runs on YARN (driver in client or cluster mode, executors in YARN containers), reads and writes HDFS, uses the Hive Metastore for tables, and benefits from data locality.

#### What is Apache Ozone?

A scalable, distributed object store for Hadoop with an S3-compatible API, designed to overcome HDFS's small-file and namespace limits while staying compatible with Hadoop applications.

<!-- challenge -->

Analysts complain that every Hive query takes 30 seconds to start, even simple ones. What do you offer them?

<!-- solution -->

An interactive engine with long-running daemons (Impala or Trino) over the same metastore and files, for ad hoc queries; keep Hive on Tez or Spark for heavy batch jobs.

<!-- takeaways -->

- Tez runs queries as one DAG.
- Impala and Trino serve interactive SQL.
- Ozone adds S3-style object storage to Hadoop.

<!-- stage: Operating Hadoop -->

### Security and governance

<!-- unit: Kerberos authentication -->

<!-- goals -->

- Explain Kerberos authentication, keytabs and delegation tokens.
- Configure impersonation for trusted services.

<!-- concept -->

By default Hadoop trusts whatever username a client claims, which is no security at all. Kerberos fixes that: users and services prove their identity with tickets from a central authority. Batch jobs authenticate with keytab files instead of passwords.

Distributed jobs add a twist: thousands of tasks can't each contact the Kerberos server, so services hand out delegation tokens after the first authentication. Trusted services like HiveServer2 act on behalf of users through impersonation.

<!-- example -->

```bash
kinit -kt /etc/security/keytabs/etl.keytab etl@CORP.COM
klist
hdfs dfs -ls /data/finance
```

#### How is authentication done in Hadoop?

With Kerberos: users and services obtain tickets from a Key Distribution Center, and Hadoop services verify them. Without Kerberos ("simple" mode), Hadoop trusts the username the client claims, which is insecure.

#### What is a keytab?

A file containing a Kerberos principal's keys, used by services and batch jobs to authenticate without a password; keytabs must be protected like passwords.

#### What are delegation tokens?

Tokens issued by services (NameNode, ResourceManager) after Kerberos authentication, passed to tasks running on the cluster so they can access HDFS without having Kerberos credentials themselves.

#### What is impersonation (proxy users) in Hadoop?

A configuration allowing a trusted service (HiveServer2, Livy, Oozie) to act on behalf of end users, so permissions and audits reflect the real user rather than the service account.

<!-- challenge -->

A nightly job fails after running fine for months with "GSS initiate failed". What do you check?

<!-- solution -->

The Kerberos credentials: whether the keytab is still valid (password or key version changed), whether the ticket expired before renewal, and clock skew between the node and the KDC.

<!-- takeaways -->

- Kerberos proves identities with tickets.
- Keytabs authenticate batch jobs and services.
- Delegation tokens and proxy users scale authentication.

<!-- unit: Authorization, encryption and audit -->

<!-- goals -->

- Manage permissions with HDFS ACLs and Ranger.
- Encrypt data and audit access with Atlas, Knox and audit logs.

<!-- concept -->

Once identities are known, access must be decided. HDFS permissions and ACLs work per file and directory; Ranger centralizes policies for HDFS, Hive, HBase and more, including column masking and row filtering, with audit of every decision.

Around that sit encryption for data in transit and at rest, a gateway that hides cluster endpoints from users, and a governance catalog with lineage and classifications that can drive policies.

<!-- example -->

```text
Ranger policy "finance_read":
  resource: Hive db=finance, table=*, column=*
  allow: group finance-analysts → SELECT
  mask: column=iban → partial mask (show last 4)
Atlas tag PII on finance.customers.iban → tag-based policy applies everywhere
```

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

#### How do you audit access in Hadoop?

HDFS audit logs on the NameNode record every file access; Ranger collects audit events from all its plugins into Solr or HDFS, and Atlas records lineage.

<!-- challenge -->

Auditors ask who read a sensitive Hive table in the last 90 days. Where does the answer come from?

<!-- solution -->

Ranger audit logs for the Hive table (user, time, action, policy decision), plus HDFS NameNode audit logs for direct file reads of its location.

<!-- takeaways -->

- Ranger centralizes policies, masking and audit.
- Atlas classifies data and tracks lineage.
- Encrypt in transit and at rest; Knox fronts the cluster.

### Operations and performance

<!-- unit: Sizing and monitoring -->

<!-- goals -->

- Size a Hadoop cluster from data and workload.
- Monitor services, jobs and JVM health.

<!-- concept -->

Sizing starts from data: raw volume times replication times growth, plus room for temporary data. Compute follows from workloads and their deadlines. Undersized clusters fail on capacity; oversized ones waste money, and on premises, hardware takes months to arrive.

Monitoring covers both layers: services such as NameNode heap, missing blocks and garbage collection pauses, and jobs such as resource use by queue and application.

<!-- example -->

```text
raw data 400 TB × 3 replicas = 1.2 PB
+ 25% temporary/shuffle space    = 1.5 PB
+ 30% yearly growth, 2 years     ≈ 2.5 PB raw disk
```

#### How do you size a Hadoop cluster?

From data volume (raw size × replication factor × growth, plus temporary space), processing needs (CPU and memory for concurrent jobs), and throughput targets; leave room for failures and rebalancing (often keep disks under 70–80% full).

#### How do you monitor a Hadoop cluster?

With the NameNode and ResourceManager web UIs, JMX metrics, Cloudera Manager (or historically Ambari), Prometheus exporters and Grafana, and alerts on HDFS capacity, dead or slow nodes, under-replicated blocks, NameNode heap and RPC latency, and queue usage.

#### How do you find which jobs use the most cluster resources?

YARN ResourceManager UI and APIs (memory-seconds and vcore-seconds per application), queue metrics, Spark and MapReduce history servers, and cluster management tools' usage reports.

#### What is the impact of JVM garbage collection on Hadoop services?

Long GC pauses on the NameNode or RegionServers make them unresponsive, causing timeouts, failovers or missed heartbeats. Size heaps carefully, use modern collectors (G1), and monitor GC logs.

<!-- challenge -->

The NameNode becomes unresponsive for 30 seconds several times a day, and failovers follow. What do you look at?

<!-- solution -->

JVM garbage collection logs and heap usage: long full GC pauses on a large heap. Tune the collector and heap size, reduce metadata (fewer small files), and monitor GC pause times.

<!-- takeaways -->

- Size from data × replication × growth.
- Monitor services and jobs separately.
- Long GC pauses destabilize master services.

<!-- unit: Slow jobs and skew -->

<!-- goals -->

- Diagnose slow Hadoop jobs and tune MapReduce memory.
- Handle data skew and reducer start timing.

<!-- concept -->

Slow jobs usually come from a few causes: skewed keys that overload single reducers, too many small files, wrong memory settings, or contention with other workloads in the same queues. Comparing task times shows which: one long task means skew, thousands of tiny tasks mean small files, killed tasks mean memory.

When reducers start matters too: starting them early overlaps work but can hold containers idle while maps finish.

<!-- example -->

```properties
mapreduce.map.memory.mb=4096
mapreduce.map.java.opts=-Xmx3276m          # ~80% of the container
mapreduce.reduce.memory.mb=8192
mapreduce.reduce.java.opts=-Xmx6553m
mapreduce.job.reduce.slowstart.completedmaps=0.80
```

#### What are common causes of slow Hadoop jobs?

Data skew (a few reducers with most keys), too many small files, insufficient or excessive parallelism, spills to disk from small memory buffers, non-splittable compressed inputs, lack of data locality, and contention in YARN queues.

#### How do you tune MapReduce memory?

Set `mapreduce.map.memory.mb` and `mapreduce.reduce.memory.mb` for container sizes and `-Xmx` in `mapreduce.map.java.opts` to around 80% of the container, and adjust `mapreduce.task.io.sort.mb` to reduce spills.

#### How do you handle data skew in Hadoop jobs?

Use combiners, custom partitioners, salting of hot keys, map-side joins for small tables, Hive skew join optimizations (`hive.optimize.skewjoin`), or pre-aggregation.

#### What is the purpose of `mapreduce.job.reduce.slowstart.completedmaps`?

It sets the fraction of maps that must finish before reducers start fetching output; starting reducers too early wastes slots waiting, too late delays the shuffle.

#### Users complain the Hive cluster is slow every morning at 9. What do you check?

Queue configuration and contention (ETL still running into business hours), large ad hoc queries without partition filters, HiveServer2 and metastore load, missing statistics, and whether LLAP or more capacity is needed for interactive users.

<!-- challenge -->

A job's 199 reducers finish in 5 minutes and one runs for 2 hours. What is happening, and what are two fixes?

<!-- solution -->

Data skew: one key holds most records. Use a combiner to shrink it, salt the hot key across several reducers and merge afterwards, or handle the hot key separately (for example a map-side join for it).

<!-- takeaways -->

- Long single tasks mean skew; many tiny tasks mean small files.
- Size heaps at about 80% of the container.
- Slowstart balances early reducers against idle containers.

<!-- unit: Capacity, backups and upgrades -->

<!-- goals -->

- Free space and protect HDFS data with backups.
- Plan safe cluster upgrades.

<!-- concept -->

Running out of space is a slow emergency: writes start failing across the cluster. The fixes are cleanup now (trash, temporary data, replication on cold data) and policy later (quotas, retention, archiving to cheaper storage).

Backups follow the same split as elsewhere: snapshots for user mistakes, copies to another cluster or object storage for disasters. Upgrades are planned like migrations, with metadata backups, rolling upgrades where supported, and a tested rollback path.

<!-- example -->

```bash
hdfs dfs -du -h / | sort -h | tail -20          # biggest directories
hdfs dfs -expunge                               # empty trash
hdfs dfs -setrep -w 2 /data/archive/2023        # less replication on cold data
hadoop distcp /data/finance s3a://dr-bucket/finance   # disaster copy
```

#### How do you upgrade a Hadoop cluster?

Plan with release notes and compatibility checks, back up NameNode metadata, use rolling upgrades when supported (HA NameNodes, DataNodes one by one), test jobs in a staging cluster, and keep the ability to roll back until finalized.

#### How do you back up HDFS?

With snapshots for user errors, `distcp` to another cluster or object storage for disaster recovery, and backups of NameNode metadata (`fsimage` and edits). Replication within the cluster isn't a backup.

#### How do you clean up a cluster running out of space?

Find large and old directories (`hdfs dfs -du -h`), empty trash, delete obsolete temporary data and old snapshots, reduce replication for cold data or apply erasure coding, compress or convert data to columnar formats, and add capacity if needed.

#### HDFS is 90% full and growing. What do you do short term and long term?

Short term: delete temporary data and trash, reduce replication on cold data, enforce quotas. Long term: tier data (erasure coding, archive storage), move cold data to object storage, compress and convert to columnar formats, apply retention policies, and plan capacity.

<!-- challenge -->

An admin deleted a production directory by mistake with `-skipTrash`. Which protections could have saved it?

<!-- solution -->

An HDFS snapshot of the directory (restore from `.snapshot`), or a recent `distcp` backup elsewhere. Also restrict `-skipTrash` use and production write access to service accounts.

<!-- takeaways -->

- Clean up now; enforce quotas and retention later.
- Snapshots for mistakes; copies for disasters.
- Upgrade with backups and a rollback plan.

### Hadoop and the cloud

<!-- unit: HDFS versus object storage -->

<!-- goals -->

- Compare HDFS with S3 and explain the S3A connector and EMRFS.
- Explain why renames are a problem on object storage.

<!-- concept -->

HDFS couples storage and compute: data locality is fast, but you scale both together and pay for idle capacity. Object storage separates them: virtually unlimited, cheap and durable, accessed over the network by any number of clusters.

Hadoop tools reach it through connectors, but object stores aren't file systems. A directory rename, which Hadoop jobs use to commit output, becomes a slow copy and delete of every object, so committers designed for object storage are needed.

<!-- example -->

| | HDFS | S3 |
|---|---|---|
| Scaling | Storage + compute together | Independent |
| Rename | Atomic metadata change | Copy + delete per object |
| Durability | Replication ×3 | 11 nines, managed |
| Cost model | Hardware, always on | Per GB-month |

#### How does HDFS compare with Amazon S3?

HDFS couples storage and compute on the same nodes, gives data locality and strong consistency, and requires cluster management. S3 is managed object storage, independently scalable, cheaper and highly durable, accessed over the network; it's now strongly consistent too. Most cloud data lakes use object storage instead of HDFS.

#### What is the S3A connector?

The Hadoop file system connector (`s3a://`) that lets Hadoop, Hive and Spark read and write S3 as if it were a file system, with optimizations for multipart uploads, committers that avoid slow renames, and credentials providers.

#### Why are renames a problem on object storage?

Object stores don't have real directories; a "rename" is a copy plus delete of every object, which is slow and not atomic. Hadoop's output committers that rely on renames are slow or unsafe on S3, so S3A committers (magic, staging) or table formats (Iceberg, Delta) are used.

#### What is EMRFS?

Amazon EMR's implementation of the Hadoop file system for S3, with features like consistent views (historically), encryption and IAM role mapping; recent EMR versions also support S3A.

<!-- challenge -->

A Spark job writing to S3 spends 20 minutes in "committing" after the tasks finish. Why, and what do you change?

<!-- solution -->

The default file output committer renames temporary output, which on S3 is copy plus delete per file. Use an S3-optimized committer (the S3A magic/directory committers or EMR's optimized committer), or write to a table format.

<!-- takeaways -->

- Object storage separates storage from compute.
- S3A and EMRFS connect Hadoop tools to S3.
- Renames are slow on object stores; use special committers.

<!-- unit: Managed and transient clusters -->

<!-- goals -->

- Describe EMR, Dataproc and HDInsight and transient clusters.
- Compare costs with on-premises Hadoop, and Hadoop on Kubernetes.

<!-- concept -->

Managed services run the Hadoop ecosystem for you on cloud machines, and they change how clusters are used. Instead of one long-lived cluster sized for peak, you can start a cluster for a job, read and write object storage, and shut it down, paying only while it runs.

That shifts costs from fixed hardware to usage. Some pieces now run on Kubernetes instead, especially Spark, Trino and the metastore.

<!-- example -->

```bash
aws emr create-cluster --name nightly-etl --release-label emr-7.3.0 \
  --applications Name=Spark Name=Hive --instance-type m7g.2xlarge --instance-count 10 \
  --steps Type=Spark,Name=etl,Args=[s3://code/etl.py,--date,2026-10-17] \
  --auto-terminate
```

#### What is Amazon EMR?

A managed big data platform on AWS that runs Hadoop, Spark, Hive, HBase, Presto/Trino, Flink and others on EC2, EKS or serverless, using S3 (EMRFS/S3A) as primary storage and the Glue Data Catalog as metastore, with transient or long-running clusters.

#### What is a transient cluster?

A cluster created for a job or pipeline and terminated afterwards, with data kept in object storage. It avoids paying for idle clusters and makes environments reproducible.

#### What are Google Dataproc and Azure HDInsight?

Managed Hadoop and Spark services on Google Cloud and Azure, similar to EMR, creating clusters in minutes with object storage (GCS, ADLS) as the main storage. Azure has been steering users towards Fabric and Databricks for new work.

#### How do costs differ between on-premises Hadoop and cloud data lakes?

On-premises clusters have high fixed costs (hardware, data centers, staff) and are sized for peaks; cloud lakes have pay-per-use storage and compute that can scale to zero, but require cost governance to avoid runaway usage.

#### Can you run Hadoop on Kubernetes?

Parts of it, yes: Spark and Flink run natively on Kubernetes, Hive Metastore and Trino run as services, and storage moves to object stores. Running HDFS and YARN on Kubernetes is possible but rarely worth the complexity.

<!-- challenge -->

A cloud cluster runs 24/7 but processes jobs only 4 hours a night. How do you cut costs?

<!-- solution -->

Keep data in object storage and switch to transient clusters started for the nightly jobs and terminated afterwards (or autoscaling to near zero), with spot instances for task nodes.

<!-- takeaways -->

- Managed services run Hadoop tools in the cloud.
- Transient clusters pay only while jobs run.
- Costs move from fixed hardware to usage.

<!-- unit: Moving beyond Hadoop -->

<!-- goals -->

- Map Hadoop components to modern replacements.
- Explain how open table formats improve on Hive tables.

<!-- concept -->

Most Hadoop pieces have cloud-era successors: object storage for HDFS, Kubernetes or serverless for YARN, Spark for MapReduce. Hive tables evolve into open table formats that add transactions, schema evolution and time travel over the same Parquet files, fixing Hive's partition-listing and consistency problems.

Migrating a Hadoop lake is therefore less about copying files and more about choosing which of these successors fits each workload.

<!-- example -->

```sql
-- Spark: migrate a Hive Parquet table to Iceberg in place
CALL spark_catalog.system.migrate('sales.orders');
-- or snapshot it first to test without touching the original
CALL spark_catalog.system.snapshot('sales.orders', 'sales.orders_iceberg_test');
```

#### How would you migrate a Hadoop data lake to the cloud?

Inventory data, jobs and dependencies; copy data to object storage with `distcp` or transfer services; convert tables to open formats (Parquet, then Iceberg or Delta); move the metastore to a managed catalog (Glue, Unity Catalog); port Hive and MapReduce jobs to Spark or SQL engines; replace Oozie with Airflow; re-create security with cloud IAM and catalog permissions; and validate results in parallel before decommissioning.

#### What replaced Hadoop's components in modern stacks?

HDFS → object storage (S3, ADLS, GCS); YARN → Kubernetes or managed serverless compute; MapReduce → Spark, Flink, SQL engines; Hive Metastore → Glue, Unity Catalog, Polaris and other catalogs; Hive tables → Iceberg, Delta, Hudi; Oozie → Airflow, Dagster; Ranger/Atlas → cloud-native governance (Lake Formation, Unity Catalog).

#### What are open table formats, and how do they relate to Hive tables?

Iceberg, Delta Lake and Hudi add a transactional metadata layer over Parquet files, solving Hive tables' problems (no ACID on object storage, slow partition listing, unsafe concurrent writes, painful schema evolution). They are the modern successors of Hive-style tables.

<!-- challenge -->

A Hive table has 200,000 partitions, and query planning takes minutes listing them. How would an open table format help?

<!-- solution -->

Iceberg (or Delta) keeps file and partition metadata in its own manifests with statistics, so planning reads metadata files instead of listing directories and the metastore, and prunes files by statistics.

<!-- takeaways -->

- Object storage, Kubernetes and Spark replace HDFS, YARN and MapReduce.
- Open table formats improve on Hive tables.
- Migration means choosing successors per workload.

<!-- stage: Putting it together -->

### Scenarios

<!-- unit: Ingesting a database into the lake -->

<!-- goals -->

- Design a daily relational ingestion into a Hadoop lake.
- Combine parallel extraction, formats, partitions and tables.

<!-- concept -->

Ingestion questions test whether you can connect storage, compute and metadata. A good answer extracts efficiently without hurting the source, writes columnar files of a healthy size into date partitions, registers them as tables, and makes reruns safe. Then it covers checks and scheduling, and whether CDC would be better than full extracts.

<!-- example -->

```text
Spark JDBC (16 parallel reads by id range) ─► Parquet, dt=2026-10-17, ~256 MB files
  ─► INSERT OVERWRITE partition (idempotent) ─► Hive Metastore table
  ─► row-count check vs source ─► Oozie/Airflow schedule, alerts
```

#### How would you ingest a daily relational database extract into a Hadoop data lake?

Extract with Spark JDBC (parallel by key ranges) or a CDC tool, write Parquet or ORC to a dated landing directory, register partitions in the metastore, transform into curated tables with Hive or Spark, run data quality checks, and orchestrate with Airflow or Oozie.

<!-- challenge -->

The source table grows to 2 billion rows and the full daily extract no longer fits the window. What do you change?

<!-- solution -->

Switch to incremental extraction: CDC from the database log (or extracts by `updated_at` with overlap), applying changes to a table format with `MERGE`, plus a periodic full reconciliation.

<!-- takeaways -->

- Extract in parallel without overloading the source.
- Write right-sized columnar files into partitions.
- Make loads idempotent; consider CDC as volumes grow.

<!-- unit: Migrating Hive tables to a lakehouse -->

<!-- goals -->

- Plan the migration of hundreds of Hive tables to the cloud.
- Sequence copying, conversion, validation and cutover.

<!-- concept -->

Migrating a Hive estate is a program, not a copy job. Tables differ in size, usage and dependencies, so the plan classifies them, moves data in waves, converts to the target format and catalog, ports jobs and validates results before switching consumers. Retiring unused tables along the way reduces the work.

<!-- example -->

| Wave | Tables | Approach |
|---|---|---|
| 0 | Unused (no reads in 90 days) | Archive, don't migrate |
| 1 | Small, few consumers | Copy + convert, quick validation |
| 2 | Large, critical | distcp, Iceberg/Delta, parallel run |
| 3 | Complex dependencies | Port jobs, cut over together |

#### You must migrate 500 Hive tables to a lakehouse in the cloud. How do you plan it?

Classify tables by size, usage and dependencies; copy data with `distcp` to object storage; convert to Iceberg or Delta (in-place migration procedures or `CTAS`); register in the new catalog; translate HiveQL jobs to Spark SQL or dbt; migrate in waves by domain, validating counts and checksums, and keep the old cluster read-only until consumers switch.

<!-- challenge -->

During parallel running, a migrated table shows 0.1% fewer rows than Hive for some partitions. How do you find the cause?

<!-- solution -->

Compare per partition, then by key, to find the missing rows; typical causes are files written after the copy (re-sync with `distcp -update`), timezone differences in partition values, and records the new job's parsing rejects.

<!-- takeaways -->

- Classify tables; migrate in waves.
- Retire unused tables instead of moving them.
- Run in parallel and reconcile before cutover.
