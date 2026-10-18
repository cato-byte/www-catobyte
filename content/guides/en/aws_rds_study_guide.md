## Amazon RDS Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Amazon RDS study guide: about 200 questions](../../images/aws_rds_study_guide_title_img.png)

About 200 interview-style questions on Amazon RDS and Aurora: engines, instance and storage choices, high availability with Multi-AZ, read replicas, backups and restores, security, monitoring, performance, scaling, cost, migrations, and how data engineers extract data from RDS with CDC, exports and zero-ETL. The answers reflect the service as of 2026. Open a question to see its answer, or use the filter to search the whole guide.

<!-- QA -->

### Fundamentals

#### What is Amazon RDS?

Amazon Relational Database Service: a managed service to run relational databases in AWS. AWS handles provisioning, patching, backups, monitoring, failover and storage management, while you choose the engine, instance size and configuration and manage schemas, queries and users.

#### Which database engines does RDS support?

MySQL, PostgreSQL, MariaDB, Oracle, Microsoft SQL Server and IBM Db2, plus Amazon Aurora (MySQL-compatible and PostgreSQL-compatible), which is part of the RDS family but has its own storage architecture.

#### What does AWS manage for you in RDS, and what do you still manage?

AWS manages hardware, OS installation and patching, database software installation and minor version patching, automated backups, storage, Multi-AZ replication and failover, and monitoring metrics. You manage database design, queries and indexes, users and privileges, parameter tuning, security group rules, capacity choices and application connection handling.

#### What is a DB instance?

An isolated database environment in the cloud: a compute instance class (CPU and memory) with attached storage running one engine version, reachable through an endpoint (DNS name and port).

#### What is a DB instance class?

The compute and memory capacity of an instance: burstable (`db.t4g`, `db.t3`) for light or variable workloads, general purpose (`db.m*`) and memory-optimized (`db.r*`, `db.x*`) for production databases. Graviton (`g` suffix) classes usually offer better price-performance.

#### When is RDS not the right choice?

When you need OS access or unsupported extensions (consider RDS Custom or EC2), a database engine RDS doesn't offer, extreme scale beyond a single writer (consider Aurora DSQL, DynamoDB or sharding), or analytical workloads on terabytes that suit a data warehouse or lakehouse better.

#### What is the difference between RDS and running a database on EC2?

On EC2 you get full control (OS, any version, any configuration) but you manage everything: installation, patching, backups, replication, failover and monitoring. RDS removes that operational work at the cost of some restrictions (no OS access, limited superuser privileges, supported parameters only).

#### What is RDS Custom?

A variant of RDS for Oracle and SQL Server that gives access to the underlying OS and database customization (for legacy applications that need specific patches or software) while AWS still automates backups and some management.

#### What is a DB subnet group?

A set of subnets (in at least two Availability Zones) in a VPC where RDS can place instances. It's required to create an instance in a VPC and to support Multi-AZ.

#### What is an RDS endpoint?

The DNS name and port that applications use to connect. It stays the same during failover (the DNS record points to the new primary), so applications should always connect through the endpoint, not an IP address.

#### What are parameter groups?

Containers of engine configuration settings (for example `max_connections`, `work_mem`, `innodb_buffer_pool_size`, `log_min_duration_statement`) applied to instances. Default groups can't be modified; you create custom groups. Dynamic parameters apply immediately, static ones need a reboot.

#### What are option groups?

Containers for optional features of some engines, such as Oracle Transparent Data Encryption, SQL Server native backup to S3, or MySQL's memcached plugin.

#### What is the maintenance window?

A weekly time range during which AWS applies pending maintenance such as OS patches, required minor version upgrades or instance modifications deferred to the window. With Multi-AZ, maintenance is applied to the standby first, then failover, to reduce downtime.

#### Can you stop an RDS instance?

Yes, for up to 7 days at a time; after that AWS starts it again automatically to apply maintenance. While stopped you pay for storage and backups but not instance hours. Aurora clusters can be stopped similarly.

#### What is deletion protection?

A setting that prevents an instance or cluster from being deleted until it's turned off, protecting production databases from accidental deletion.

#### What is the shared responsibility model for RDS?

AWS is responsible for the infrastructure, OS, database software patching, backups and replication mechanisms. You are responsible for network access (security groups), encryption choices, database users and privileges, schema and query design, parameter settings and protecting credentials.

#### How do you connect to an RDS instance from your laptop if it's in a private subnet?

Through a bastion host or, better, AWS Systems Manager Session Manager port forwarding to an instance in the VPC, a client VPN, or AWS Cloud9/EC2 inside the VPC, never by making the database publicly accessible.

#### What does "publicly accessible" mean for an RDS instance?

The instance gets a public IP and its endpoint resolves to it from outside the VPC, so it's reachable from the internet if security groups allow it. Production databases should keep it disabled.

#### How do you create RDS instances repeatably?

With infrastructure as code (CloudFormation, CDK, Terraform), defining subnet groups, parameter groups, security groups, KMS keys, secrets and the instance, so environments are consistent and changes are reviewed.

#### What are RDS tags used for?

Cost allocation, access control (IAM conditions on tags), automation (for example stopping instances tagged `env=dev` at night) and ownership information.

#### What is RDS on Outposts?

RDS running on AWS Outposts hardware in your own data center, for workloads that need low latency to on-premises systems or data residency, managed with the same APIs.

### Storage

#### What storage types does RDS offer?

General Purpose SSD gp3 (baseline 3,000 IOPS and 125 MiB/s, with IOPS and throughput configurable independently of size), gp2 (IOPS tied to size with burst credits), Provisioned IOPS io1 and io2 Block Express (consistent high IOPS and low latency), and legacy magnetic storage.

#### When should you choose Provisioned IOPS?

For I/O-intensive production workloads that need consistent low latency and high IOPS (busy OLTP, large write volumes), where gp3's configurable limits aren't enough or predictability matters more than cost.

#### What is storage autoscaling?

A setting that automatically increases allocated storage when free space is low, up to a maximum you define, avoiding outages caused by full disks. Storage can't be decreased afterwards.

#### Can you reduce allocated storage in RDS?

Not directly. To shrink, create a new instance with smaller storage and migrate the data (dump and restore, DMS, or logical replication), or use Blue/Green deployments where supported.

#### Why can gp2 performance suddenly drop?

gp2 small volumes rely on burst credits above their baseline IOPS (3 IOPS per GB). When credits run out, performance falls to the baseline. gp3 avoids this by providing a fixed baseline independent of size.

#### What is the maximum storage of an RDS instance?

Up to 64 TiB for most engines (lower for some SQL Server configurations). Aurora storage grows automatically up to 128 TiB per cluster.

#### What does "storage-full" status mean?

The instance has run out of storage and stops accepting writes. Enable storage autoscaling, alert on `FreeStorageSpace`, and clean up large tables, logs or temporary files.

#### How does gp3 compare with io2 for RDS?

gp3 offers a baseline of 3,000 IOPS and 125 MiB/s, configurable up to higher limits at extra cost, at a lower price per GB. io2 Block Express offers higher, more consistent IOPS and lower latency with better durability, for the most demanding workloads.

#### What is `DiskQueueDepth` telling you?

The number of outstanding I/O requests waiting for the disk. A consistently high queue depth with high latency means the storage can't keep up; consider more IOPS, better queries or caching.

#### What is the impact of modifying storage on a running instance?

Increasing storage or changing type usually happens online, but the instance may enter a "storage-optimization" state for hours during which further storage changes aren't possible; performance can be affected slightly.

#### How do you estimate the IOPS you need?

From current metrics (`ReadIOPS` + `WriteIOPS` at peak), or for new workloads from expected transactions per second and I/O per transaction, with headroom; then test with load before production.

### High availability and Multi-AZ

#### What is a Multi-AZ instance deployment?

RDS keeps a synchronous standby replica of the primary in another Availability Zone. If the primary fails (hardware, AZ outage, storage failure) or during certain maintenance, RDS fails over automatically to the standby, typically in one to two minutes. The standby doesn't serve reads.

#### What is a Multi-AZ DB cluster deployment?

A deployment (for MySQL and PostgreSQL) with one writer and two readable standby instances in three AZs, using semi-synchronous replication. Failover is faster (typically under 35 seconds) and the standbys can serve read traffic through a reader endpoint.

#### How does Multi-AZ failover work?

RDS detects the failure, promotes the standby, and updates the endpoint's DNS record to point to it. Applications must reconnect; connection pools should handle disconnects and respect DNS TTL.

#### What events trigger an automatic failover?

Loss of the primary instance or its AZ, network or storage failure on the primary, instance type changes, OS patching and some engine maintenance, and manual reboot with failover.

#### Is Multi-AZ a scaling solution?

No. For Multi-AZ instance deployments the standby can't serve traffic; it's for availability and durability. Use read replicas (or Multi-AZ DB clusters' readable standbys, or Aurora replicas) for read scaling.

#### How do you test a failover?

Reboot the instance with the "reboot with failover" option and observe application behavior, reconnection time and errors. Doing this regularly validates the application's resilience.

#### Does Multi-AZ protect against data corruption or accidental deletes?

No. Replication copies every change, including bad ones, to the standby. Backups, point-in-time recovery and snapshots protect against logical errors.

#### What is the difference between high availability and disaster recovery for RDS?

High availability (Multi-AZ) keeps the database running when an AZ or instance fails within a region. Disaster recovery covers losing a region or data: cross-region read replicas, cross-region snapshot copies, AWS Backup and Aurora Global Database, with defined RPO and RTO.

#### How should applications handle failover?

Use the endpoint (never IPs), set short DNS caching (for example JVM DNS TTL), implement retries with backoff on connection errors, use connection pools that validate connections, and consider RDS Proxy or AWS drivers that speed up failover detection.

#### What are the AWS Advanced JDBC/Python wrappers?

Driver wrappers that understand RDS and Aurora topologies, detect failovers faster than DNS updates, and reconnect to the new writer, reducing downtime perceived by applications.

#### Can you choose which AZ the standby goes in?

RDS chooses the standby AZ within the subnet group; you choose the primary AZ. Subnets in at least two (or three for Multi-AZ DB clusters) AZs must exist in the subnet group.

#### What RPO and RTO does Multi-AZ give?

For Multi-AZ instance deployments, RPO is effectively zero (synchronous replication) and RTO is typically one to two minutes; for Multi-AZ DB clusters, RTO is usually under a minute.

### Read replicas

#### What is a read replica?

A copy of a source instance kept up to date with asynchronous replication, used to offload read traffic (reports, analytics, read-heavy APIs). It has its own endpoint and can be in the same region or another region.

#### How many read replicas can you create?

Up to 15 for MySQL, MariaDB and PostgreSQL, and fewer for Oracle and SQL Server; Aurora supports up to 15 Aurora Replicas per cluster. Replicas can also have their own replicas for some engines.

#### What is replica lag?

The delay between a write on the source and its visibility on the replica, monitored with the `ReplicaLag` metric. Heavy writes, long transactions, undersized replicas and network distance (cross-region) increase it.

#### Why might reading from a replica return stale data?

Because replication is asynchronous: a read immediately after a write may not see it. Applications needing read-your-writes consistency should read from the primary for that path.

#### Can you promote a read replica?

Yes. Promotion turns it into a standalone instance that accepts writes, breaking replication. It's used for disaster recovery, migrations or splitting a database.

#### What are cross-region read replicas used for?

Serving reads close to users in another region, disaster recovery (promote if the primary region fails), and migrating a database to another region.

#### Can a read replica be Multi-AZ?

Yes, for supported engines a read replica can itself be configured as Multi-AZ, which improves the availability of the replica (useful when it may be promoted for DR).

#### Do read replicas need automated backups on the source?

Yes. Automated backups must be enabled on the source instance (backup retention greater than zero) to create read replicas for most engines.

#### How do you use read replicas for analytics without hurting production?

Point reporting and extraction jobs at a replica sized for analytic queries, so long-running reads don't compete with OLTP traffic on the primary; monitor lag so reports know how fresh data is.

#### Can you write to a read replica?

Not normally: replicas are read-only. For MySQL you can set `read_only = 0` on a replica for special cases like adding indexes for reporting, but writes can break replication and are discouraged.

#### How do you route reads to replicas?

In the application (separate read and write data sources), through a proxy or driver that supports read/write splitting, or with Aurora's reader endpoint, which load-balances connections across replicas.

#### What happens to replicas when the source fails over in Multi-AZ?

Replicas automatically follow the new primary after a Multi-AZ failover, because the source endpoint and replication stream continue from the standby.

#### What is a delayed replica?

A replica (MySQL, MariaDB) configured to apply changes with a delay, for example one hour, so you can recover from mistakes by promoting it before the bad change is applied.

### Backups and restore

#### What are automated backups?

Daily snapshots of the instance plus transaction logs captured every few minutes, retained for a configurable period (1 to 35 days; 0 disables them), enabling point-in-time recovery within the retention window.

#### What is point-in-time recovery?

Restoring the database to any second within the backup retention period (up to about the last five minutes), which creates a new instance with a new endpoint. It's the main tool for recovering from accidental changes.

#### What are manual snapshots?

User-initiated snapshots that are kept until you delete them, independent of the automated backup retention. They're used before risky changes, for long-term retention and to copy or share databases.

#### Can you restore a snapshot into the existing instance?

No. Restores always create a new instance. You then point applications to the new endpoint (or rename instances to reuse the old endpoint name).

#### How do you copy backups to another region or account?

Copy snapshots to another region (cross-region snapshot copy, optionally automated with AWS Backup or cross-region automated backup replication) and share snapshots with other accounts (encrypted snapshots require sharing the KMS key).

#### What is AWS Backup's role with RDS?

AWS Backup centralizes backup policies across services: schedules, retention, cross-region and cross-account copies, vault locks for immutability, and compliance reports for RDS and Aurora.

#### What happens to automated backups when you delete an instance?

You can retain them (until their retention expires) and take a final snapshot. Without a final snapshot and retained backups, the data is gone; deletion protection and final snapshots prevent mistakes.

#### Do backups affect performance?

With Multi-AZ, backups are taken from the standby, so the primary isn't impacted. On single-AZ instances, I/O may briefly be suspended during the snapshot, which can affect performance.

#### How do you export RDS data to S3 for analytics?

Export a snapshot to S3 (RDS writes tables as Parquet files, which Athena or Glue can query), or run your own exports (the `aws_s3` extension in PostgreSQL, `SELECT INTO OUTFILE S3` in Aurora MySQL, or Glue/DMS jobs).

#### How long does a restore take?

It depends on database size and activity: creating the instance from the snapshot is fast, but data loads lazily from S3, so first queries can be slow until blocks are read (initializing or "warming" may be needed for performance-critical restores).

#### What is lazy loading after a restore?

When an instance is restored from a snapshot, its storage blocks are fetched from S3 on first access, so initial reads have higher latency. Running full table scans after the restore warms the storage.

#### How do you keep backups for seven years for compliance?

Use AWS Backup with a long retention plan and vault lock, or copy manual snapshots periodically; automated backups max out at 35 days. Exporting to S3 with lifecycle rules can also serve archival needs.

#### Can you restore a single table from a backup?

Not directly. Restore the whole instance to a new one (point-in-time), then dump the needed table and import it into production.

#### What is cross-region automated backup replication?

A feature that copies automated backups and transaction logs to another region, so you can do point-in-time recovery in the DR region.

### Security

#### How do you control network access to RDS?

Place instances in private subnets, disable public accessibility, and use VPC security groups to allow only the application's security groups or specific CIDR ranges on the database port. Access from on-premises goes through VPN or Direct Connect.

#### How is data encrypted at rest in RDS?

With AWS KMS keys (AWS-managed or customer-managed), covering storage, automated backups, snapshots, read replicas and logs. Encryption must be chosen at creation.

#### How do you encrypt an existing unencrypted RDS instance?

Take a snapshot, copy it with encryption enabled using a KMS key, and restore a new instance from the encrypted copy; then switch applications to it. Read replicas of an unencrypted instance can't be encrypted directly.

#### How is data encrypted in transit?

With SSL/TLS connections using the RDS certificate authority bundle. You can enforce TLS with parameters such as `rds.force_ssl` (PostgreSQL, SQL Server) or `require_secure_transport` (MySQL). Certificates must be rotated when RDS rotates its CAs.

#### What is IAM database authentication?

For MySQL, MariaDB and PostgreSQL (and Aurora), users authenticate with a short-lived token generated from IAM credentials instead of a password, so access is controlled with IAM policies and no database passwords are stored in applications.

#### How should you manage database passwords?

Use Secrets Manager, ideally with RDS-managed master user passwords (RDS creates and rotates the secret), rotate application user secrets automatically, and never hard-code credentials.

#### What privileges does the master user have?

Broad administrative privileges within the engine's limits (for example `rds_superuser` in PostgreSQL), but not full superuser or OS access. Create separate users with least privilege for applications and pipelines.

#### How do you audit database activity?

Engine logs (PostgreSQL `pgaudit`, MySQL audit plugin, SQL Server audit, Oracle unified auditing) published to CloudWatch Logs, CloudTrail for RDS API calls, and Database Activity Streams for near-real-time activity sent to Kinesis (for compliance tools).

#### What are Database Activity Streams?

A feature (for Aurora and some RDS engines) that pushes a real-time stream of database activity to Kinesis Data Streams, encrypted with KMS and separated from DBA control, for monitoring and compliance.

#### How do you protect RDS from accidental changes by humans?

Least-privilege IAM for RDS APIs, deletion protection, separate accounts or roles for production, change management through infrastructure as code, and audits of who can modify instances and parameter groups.

#### How do you restrict which IAM users can create or modify RDS instances?

With IAM policies on RDS actions (`rds:CreateDBInstance`, `rds:ModifyDBInstance`, `rds:DeleteDBInstance`), conditions on tags, and service control policies in AWS Organizations for guardrails such as requiring encryption.

#### How do you prevent unencrypted databases from being created?

Use an SCP or IAM condition `rds:StorageEncrypted = true` on create actions, AWS Config rules (`rds-storage-encrypted`) to detect violations, and infrastructure as code defaults.

#### What is Kerberos authentication on RDS?

Integration with AWS Managed Microsoft AD (or self-managed AD through a trust) so users log in to SQL Server, Oracle, PostgreSQL or MySQL with their directory credentials and centralized account management.

#### How do you limit network access from Lambda to RDS?

Run Lambda in the VPC with its own security group, allow only that security group on the database port, and use RDS Proxy with IAM authentication to avoid storing passwords in the function.

#### How do you share an encrypted snapshot with another account?

Use a customer-managed KMS key (snapshots encrypted with the AWS-managed key can't be shared), grant the other account access to the key, and share the snapshot; the other account copies it with its own key.

#### What is a good practice for application database users?

One user per application or service with only the privileges it needs (often schema-level `SELECT`, `INSERT`, `UPDATE`, `DELETE`, no DDL), separate read-only users for reporting, and DDL handled by migration tooling with a separate user.

### Monitoring and performance

#### Which CloudWatch metrics are most important for RDS?

`CPUUtilization`, `FreeableMemory`, `FreeStorageSpace`, `ReadIOPS`/`WriteIOPS`, `ReadLatency`/`WriteLatency`, `DiskQueueDepth`, `DatabaseConnections`, `ReplicaLag`, `SwapUsage` and, for burstable classes, `CPUCreditBalance`.

#### What is Enhanced Monitoring?

OS-level metrics (per process CPU and memory, file system, swap, disk I/O) collected by an agent at intervals down to one second and sent to CloudWatch Logs, which helps find causes that standard metrics miss.

#### What is Performance Insights / Database Insights?

A database performance tool that shows database load (average active sessions) broken down by wait events, SQL statements, users and hosts, so you can see which queries cause load and why. It is now part of CloudWatch Database Insights, which adds fleet-wide views and longer retention in its advanced mode.

#### How do you find slow queries in RDS?

Enable slow query logs (MySQL `slow_query_log` and `long_query_time`, PostgreSQL `log_min_duration_statement`), use `pg_stat_statements` or Performance Schema, and analyze Database Insights top SQL; then run `EXPLAIN` to fix plans and indexes.

#### What are RDS event notifications?

Notifications sent through EventBridge or SNS for events such as failovers, reboots, low storage, backups, configuration changes and maintenance, used for alerting and automation.

#### What causes high CPU on an RDS instance?

Inefficient queries (missing indexes, full scans, poor plans), too many concurrent connections, heavy reporting on the primary, lock contention or an undersized instance. Find the top SQL first, then tune or scale.

#### What causes running out of connections?

Applications without pooling opening many connections (serverless functions are a classic case), leaked connections, low `max_connections` for the instance's memory, or a spike in traffic. Use pooling (RDS Proxy, PgBouncer) and fix leaks.

#### What is RDS Proxy?

A managed database proxy that pools and shares connections between applications and RDS or Aurora, reduces connection overhead (especially from Lambda), speeds up failover by keeping client connections and redirecting them, and supports IAM authentication and Secrets Manager.

#### When should you use RDS Proxy?

With Lambda or other highly concurrent, short-lived clients, applications that open many connections, or when you want faster, more transparent failover. It adds cost and a small latency, and some session features (pinning) reduce its benefit.

#### How do you tune PostgreSQL on RDS?

Adjust parameters in a custom parameter group (`shared_buffers`, `work_mem`, `maintenance_work_mem`, `effective_cache_size`, autovacuum settings, `max_connections`), keep statistics fresh, add appropriate indexes, monitor bloat and long-running transactions, and use `pg_stat_statements`.

#### How do you tune MySQL on RDS?

Size `innodb_buffer_pool_size` (default is about 75% of memory), review `max_connections`, use proper indexes and query plans, monitor the slow query log, and avoid long transactions that grow undo logs.

#### Why does autovacuum matter on RDS PostgreSQL?

PostgreSQL's MVCC leaves dead tuples after updates and deletes; autovacuum reclaims them and prevents transaction ID wraparound. If it falls behind, tables bloat and, in the worst case, the database stops accepting writes to prevent wraparound. Tune it for large, busy tables.

#### What is `FreeableMemory` and when should it worry you?

The RAM available on the instance. Low freeable memory with rising `SwapUsage` means the workload doesn't fit (buffer pool, connections, sorts); scale up or reduce memory consumption.

#### How do locks show up in RDS performance tools?

As wait events (for example `Lock:transactionid` or `Lock:relation` in PostgreSQL, `synch/cond/innodb/row_lock_wait` in MySQL) in Database Insights; queries like `pg_locks` with `pg_stat_activity` show who blocks whom.

#### How do you find unused indexes in PostgreSQL on RDS?

Query `pg_stat_user_indexes` for indexes with `idx_scan = 0` over a long period (excluding constraints), and drop them after checking, since they cost write performance and storage.

#### How do you identify long-running transactions in PostgreSQL?

Query `pg_stat_activity` for sessions with old `xact_start`, especially `idle in transaction`; they block vacuum and cause bloat. Set `idle_in_transaction_session_timeout` to protect the database.

#### What logs can RDS publish to CloudWatch Logs?

Error logs, slow query logs, general logs (MySQL), PostgreSQL logs (including `log_min_duration_statement` output and `pgaudit`), audit logs, upgrade logs and agent logs, depending on engine and settings.

#### How do you alert on RDS problems?

CloudWatch alarms on CPU, free storage, freeable memory, connections, replica lag, read/write latency and burst balance; EventBridge rules on RDS events (failover, storage full, maintenance); and anomaly detection in Database Insights.

### Scaling

#### How do you scale an RDS instance vertically?

Modify the instance class (for example from `db.r6g.large` to `db.r6g.2xlarge`), immediately or in the maintenance window. It requires a brief outage, shortened by Multi-AZ (the standby is modified first, then failover).

#### How do you scale reads?

Add read replicas (or Aurora Replicas) and route read-only traffic to them, cache frequent reads with ElastiCache, and use Multi-AZ DB clusters' readable standbys.

#### How do you scale writes beyond a single instance?

Scale up the instance, optimize write patterns (batching, fewer indexes, partitioning), move parts of the workload to other databases (DynamoDB for key-value access), or shard the data across instances at the application level. Aurora Limitless Database (PostgreSQL) and Aurora DSQL offer managed horizontal scaling options.

#### What is table partitioning and does it help on RDS?

Splitting large tables into partitions (PostgreSQL declarative partitioning, MySQL partitioning) by range or list, which speeds up queries filtering on the partition key and makes archiving old data cheap (drop a partition instead of deleting rows).

#### How do burstable instances behave under sustained load?

`db.t*` instances accumulate CPU credits when idle and spend them under load; with sustained high CPU, they exhaust credits and either throttle (standard mode) or bill extra (unlimited mode). They're unsuited for steady production workloads.

#### How do you scale storage performance without changing the instance?

With gp3, raise IOPS and throughput independently; with io1/io2, raise provisioned IOPS; check that the instance class's EBS bandwidth isn't the bottleneck.

#### What instance limits can cap I/O performance?

Each instance class has maximum EBS bandwidth and IOPS; a small class can't use very high provisioned IOPS. Choose a class whose limits match the storage configuration.

#### How does caching help an RDS database?

ElastiCache (Redis or Memcached) or application caches serve repeated reads (sessions, product catalogs, computed results) from memory, reducing load and latency on the database. Cache invalidation strategy is the hard part.

#### When should you split one database into several?

When different domains or services have independent workloads, scaling needs or owners, when one workload's peaks affect others, or for the microservices principle of one database per service.

### Aurora

#### What is Amazon Aurora?

A MySQL- and PostgreSQL-compatible relational database built for the cloud, with a distributed, fault-tolerant storage layer shared by the writer and replicas. It offers higher throughput than standard engines, faster failover and storage that grows automatically.

#### How does Aurora storage work?

Data is stored in a cluster volume replicated six ways across three Availability Zones in 10 GB segments. Writes need four of six copies and reads three of six, so the cluster tolerates losing an AZ plus another copy. Storage scales automatically up to 128 TiB.

#### What is an Aurora cluster?

One writer (primary) instance and up to 15 Aurora Replicas sharing the same cluster volume, with a cluster endpoint (writer), a reader endpoint (load-balanced across replicas) and optional custom endpoints for subsets of instances.

#### How is Aurora failover different from RDS Multi-AZ?

An Aurora Replica can be promoted because it shares the same storage, so there's no data to catch up and failover is typically around 30 seconds or less. Replica lag is usually in milliseconds.

#### What is Aurora Serverless v2?

A capacity mode where Aurora instances scale capacity automatically in fine-grained Aurora Capacity Units (ACUs) according to load, within a minimum and maximum, and can scale down to zero for some configurations. It suits variable or unpredictable workloads.

#### What is Aurora Global Database?

A configuration with a primary region and up to several secondary regions, replicated at the storage level with typically under one second of lag. Secondaries serve local reads and can be promoted in a regional outage (managed failover or switchover).

#### What is Aurora fast cloning?

Creating a new cluster that shares the source's storage pages using copy-on-write, so the clone is created quickly and only changed pages use new storage. It's ideal for testing, analytics on a copy, or pre-production refreshes.

#### What is Aurora Backtrack?

An Aurora MySQL feature that rewinds the cluster in place to a previous point in time within a configured window, without restoring from a backup, useful for quickly undoing mistakes.

#### What are Aurora Standard and Aurora I/O-Optimized?

Two storage configurations: Standard bills I/O requests separately (cheaper for low I/O), I/O-Optimized includes I/O in a higher storage and instance price (cheaper when I/O exceeds about a quarter of the database cost).

#### What is Aurora zero-ETL integration with Redshift?

A managed integration that replicates Aurora (and some RDS) data into Amazon Redshift in near real time without building pipelines, so analytics run on Redshift with fresh operational data.

#### What is Babelfish for Aurora PostgreSQL?

A capability that lets Aurora PostgreSQL understand SQL Server's T-SQL and TDS protocol, so applications written for SQL Server can run with fewer code changes.

#### What is the Aurora Data API?

An HTTP API to run SQL against Aurora (Serverless v2 and provisioned) without managing connections or drivers, convenient for Lambda and other serverless apps.

#### What is Aurora DSQL?

A serverless, distributed SQL database with PostgreSQL compatibility designed for active-active multi-region applications, scaling reads and writes horizontally with strong consistency. It differs from standard Aurora and has some PostgreSQL feature limitations.

#### When would you choose Aurora over RDS for PostgreSQL or MySQL?

When you need higher throughput, faster failover, many low-lag replicas, global replication, fast cloning, or serverless scaling. Standard RDS can be cheaper for small or steady workloads and supports some engine features or versions earlier.

#### What are Aurora custom endpoints?

Endpoints that point to a chosen subset of instances in a cluster, for example larger replicas for analytics queries and smaller ones for application reads.

#### What is the Aurora reader endpoint's limitation?

It load-balances new connections across replicas via DNS, not individual queries; long-lived connections stay on one replica, so load can become uneven. Connection pools with periodic recycling or proxies help.

#### What is Aurora parallel query?

An Aurora MySQL feature that pushes parts of analytic queries (filters, aggregations) down to the storage layer across thousands of nodes, speeding up some analytical queries on large tables without a separate warehouse.

#### What are Aurora Optimized Reads?

A feature on instances with local NVMe storage that uses that storage as a tiered cache and for temporary objects, improving latency for read-heavy workloads whose data exceeds memory and for queries with large temporary tables.

#### How does Aurora handle backups?

Continuously and incrementally to S3 with no performance impact, with point-in-time recovery within the retention period (1–35 days); snapshots are cluster-level.

#### What is Aurora Limitless Database?

A capability of Aurora PostgreSQL that scales writes horizontally by sharding tables across multiple instances behind a single endpoint, for workloads beyond one writer's capacity.

#### What is Aurora's failover priority (tier)?

A setting (tier 0–15) on each replica that decides which replica is promoted first during failover; equally ranked replicas are chosen by size.

#### Can Aurora Serverless v2 and provisioned instances be mixed?

Yes. A cluster can have a provisioned writer and Serverless v2 readers (or the reverse), which is useful for variable read traffic.

### Engines and features

#### What PostgreSQL extensions are useful on RDS?

`pg_stat_statements` (query stats), `PostGIS` (geospatial), `pgvector` (vector search), `pg_partman` (partition management), `pg_cron` (scheduled jobs), `aws_s3` (import/export with S3), `pgaudit`, `pg_repack` and `postgres_fdw`. Only supported extensions can be installed.

#### How do you load data from S3 into RDS PostgreSQL?

With the `aws_s3` extension: `SELECT aws_s3.table_import_from_s3('table', 'col1,col2', '(format csv, header true)', aws_commons.create_s3_uri('bucket', 'key.csv', 'eu-west-1'));`, with an IAM role attached to the instance.

#### What is a Blue/Green deployment?

A feature (MySQL, MariaDB, PostgreSQL, Aurora) that creates a staging copy (green) synchronized with production (blue) by logical replication, lets you upgrade or change it, then switches over in about a minute with guardrails, keeping the same endpoints.

#### How do you upgrade the major version of an RDS engine?

Test the upgrade on a snapshot restore, check extension and parameter compatibility, then either upgrade in place (downtime) or use Blue/Green deployments for minimal downtime. Take a snapshot before upgrading.

#### What are minor version auto-upgrades?

An option where RDS applies minor engine versions (bug and security fixes) automatically during the maintenance window. Most teams enable it, sometimes after testing in lower environments.

#### What is RDS Extended Support?

A paid offering that keeps receiving critical patches for major engine versions after their community end of life, giving extra time to upgrade. Instances on such versions are enrolled automatically unless upgraded.

#### How do you schedule jobs inside RDS PostgreSQL?

With `pg_cron` for SQL jobs inside the database, or externally with EventBridge Scheduler, Lambda or an orchestrator. Heavy batch work is often better outside the OLTP database.

#### What are the restrictions of SQL Server on RDS?

No `sysadmin` role, limited features in some editions, specific procedures for native backup and restore (via S3), limits on the number of databases per instance, and storage size limits; RDS Custom for SQL Server lifts some of them.

#### What licensing options exist for Oracle and SQL Server on RDS?

License Included (license cost in the hourly price) or Bring Your Own License for Oracle; SQL Server is generally License Included, with edition choices (Express, Web, Standard, Enterprise).

#### How do you use `pgvector` on RDS PostgreSQL?

Install the extension, create `vector` columns for embeddings, and index them with HNSW or IVFFlat indexes for similarity search, which supports retrieval-augmented generation without a separate vector database.

#### What is logical replication used for on RDS PostgreSQL?

Replicating selected tables to another PostgreSQL database (for upgrades, migrations, splitting databases or feeding analytics), CDC to external systems, and Blue/Green deployments.

#### What are the benefits of MySQL 8.0+ features on RDS for data work?

Window functions, CTEs (including recursive), JSON functions, invisible indexes, instant `ADD COLUMN` for many changes and better optimizer statistics, which make analytics queries and schema changes easier.

#### How do you run schema migrations safely on large tables?

Use online-friendly operations (instant DDL in MySQL 8, `CREATE INDEX CONCURRENTLY` in PostgreSQL), tools like `gh-ost` or `pt-online-schema-change` for MySQL, Blue/Green deployments, and test migration time on a clone.

### Cost

#### What drives RDS costs?

Instance hours (by class, Multi-AZ doubles the compute), storage (by type and size, plus provisioned IOPS), backup storage beyond the free amount, data transfer out and across AZs or regions, Extended Support fees, and features like RDS Proxy and Database Insights advanced mode.

#### How do you reduce RDS costs?

Right-size instances using metrics, use Graviton classes, buy Reserved Instances for steady workloads, use gp3 instead of over-provisioned io1, stop non-production instances at night, clean old snapshots, use Aurora Serverless v2 or I/O-Optimized where they fit, and offload reads to caches.

#### How much does Multi-AZ cost?

Roughly double the instance cost, because a standby instance runs in another AZ, plus replicated storage. It's usually justified for production; non-production environments often run single-AZ.

#### What are Reserved Instances for RDS?

A one- or three-year commitment to an instance class family in a region in exchange for a significant discount over on-demand pricing, with size flexibility within a family for most engines.

#### How do you find idle or oversized RDS instances?

CloudWatch metrics (CPU, connections, IOPS) over weeks, AWS Compute Optimizer recommendations for RDS, Trusted Advisor checks for idle instances, and cost reports by tag.

#### What does backup storage cost?

Backup storage up to the size of the provisioned database storage in a region is included; beyond that, and for manual snapshots kept long, you pay per GB-month. Old manual snapshots are a common hidden cost.

#### How do cross-AZ data transfer costs affect RDS?

Multi-AZ replication traffic isn't charged, but application traffic between an instance in one AZ and clients in another AZ, and cross-region replication, incur data transfer charges.

#### How can you save on development databases?

Use small or burstable instances, single-AZ, schedule stop/start outside working hours, use Aurora Serverless v2 with a low minimum, restore from shared snapshots rather than keeping many copies, and delete unused environments.

### Migration and data engineering

#### How do you migrate a database to RDS?

For the same engine: native dump and restore (`pg_dump`/`pg_restore`, `mysqldump`, SQL Server backup to S3 and restore), or replication from the source to RDS for minimal downtime. For different engines or continuous replication: AWS DMS, with the Schema Conversion Tool (or DMS Schema Conversion) for schema translation.

#### What is AWS DMS?

Database Migration Service: replicates data from a source database to a target (another database, S3, Redshift, Kinesis and others) with a full load and ongoing change data capture (CDC), running on replication instances or DMS Serverless.

#### How do you capture changes (CDC) from RDS MySQL?

Enable binary logging with `binlog_format = ROW` (and full row images), keep enough binlog retention (`mysql.rds_set_configuration('binlog retention hours', 24)`), and read changes with DMS, Debezium or a zero-ETL integration.

#### How do you capture changes from RDS PostgreSQL?

Enable logical replication (`rds.logical_replication = 1`), create a replication slot and publication, and consume with DMS, Debezium (pgoutput plugin) or zero-ETL. Monitor replication slots: an unconsumed slot retains WAL and can fill the disk.

#### Why are replication slots dangerous on PostgreSQL?

A slot makes PostgreSQL keep WAL until the consumer confirms it. If a CDC consumer stops, WAL accumulates (`TransactionLogsDiskUsage` grows) until storage fills and the database stops. Alert on slot lag and drop abandoned slots.

#### How do you extract large tables from RDS without hurting production?

Read from a read replica or a fresh clone/restore, export snapshots to S3 as Parquet, extract incrementally by an updated-at column or CDC instead of full extracts, run in parallel by key ranges within limits, and schedule outside peak hours.

#### What is the snapshot export to S3 feature?

An RDS feature that exports data from a snapshot to S3 in Parquet format, partitioned by table, without impacting the running database, ready to be catalogued with Glue and queried with Athena.

#### How do Glue jobs read from RDS?

Through a Glue JDBC connection in the database's VPC (with subnet and security group access), reading tables in parallel with partitioning options and storing credentials in Secrets Manager; bookmarks or a watermark column provide incremental loads.

#### How do you load data into RDS efficiently?

Use bulk loading (`COPY` in PostgreSQL, `LOAD DATA` in MySQL, the `aws_s3` extension), batch inserts, disable or defer secondary index creation for initial loads, increase `maintenance_work_mem` temporarily, and avoid row-by-row inserts over the network.

#### Should you run analytics directly on the production RDS instance?

Generally no. Analytical queries compete with OLTP traffic for CPU, memory and I/O. Use a read replica for light reporting, and for heavier analytics move data to a warehouse or lakehouse through CDC, exports or zero-ETL.

#### What is the difference between OLTP and OLAP, and where does RDS fit?

OLTP handles many small transactions (inserts, updates, point lookups) with strong consistency; OLAP handles large scans and aggregations over history. RDS is built for OLTP; OLAP belongs in Redshift, Snowflake, Databricks or Athena on a data lake.

#### What is DMS Schema Conversion?

A managed feature in DMS (successor to the desktop Schema Conversion Tool for many cases) that assesses and converts schemas and code between engines, reporting items that need manual work.

#### How does DMS handle large tables during full load?

With parallel load by partitions or ranges of a column, LOB settings for large objects, and table mappings to select and transform tables; very large migrations may combine native bulk export with DMS CDC from a known position.

#### How do you validate a migration?

DMS data validation (row-by-row comparison), row counts and checksums per table, comparison of aggregates (sums, min/max by key ranges), application tests against the target, and a period of parallel running.

#### What are the common pitfalls of CDC from relational databases?

Missing primary keys (updates can't be matched), insufficient log retention, large transactions that lag, schema changes not propagated, data type mismatches (timestamps, decimals), and deletes not handled downstream.

#### How do you send RDS changes to Kafka?

With Debezium on Kafka Connect (or Amazon MSK Connect) reading the binlog or logical replication, producing one topic per table with change events, or with DMS targeting Kinesis or MSK.

#### How do you land RDS data in a data lake?

Full loads via snapshot export to S3 or DMS full load, then incremental changes via DMS CDC to S3 (Parquet with operation columns) or zero-ETL; apply changes to Iceberg/Delta tables with `MERGE`, and catalog everything in Glue.

#### What is a watermark-based incremental extraction, and what are its risks?

Selecting rows where `updated_at` is greater than the last extracted value. It misses deletes, rows updated without changing the timestamp, and rows committed late with an older timestamp; use an overlap window and periodic reconciliation, or CDC.

#### How do you avoid locking production tables when extracting?

Use snapshots or replicas, read with consistent snapshot isolation without locks (PostgreSQL MVCC, InnoDB consistent reads), avoid `SELECT … FOR UPDATE` and long transactions, and paginate by key.

### SQL and database design on RDS

#### Why do primary keys matter so much on RDS tables?

They guarantee row identity, are required by many replication and CDC tools to apply updates and deletes, and in InnoDB define the physical clustering of the table. Every table should have one.

#### Should you use natural keys or surrogate keys?

Surrogate keys (auto-increment, identity or UUIDs) are stable and compact; natural keys (email, national ID) can change and are often sensitive. Use surrogate primary keys with unique constraints on natural keys.

#### UUIDs or integers for primary keys?

Integers are smaller and keep inserts sequential (good for B-tree indexes and InnoDB clustering). Random UUIDs scatter inserts and bloat indexes; time-ordered UUIDs (UUIDv7) keep uniqueness across systems with better locality.

#### What is normalization, and why does it matter for OLTP?

Organizing tables so each fact is stored once (normal forms), which avoids update anomalies and keeps transactions small and consistent. OLTP databases are usually normalized to third normal form; analytics denormalize later.

#### How do indexes speed up queries, and what do they cost?

B-tree indexes let the database find rows by key without scanning the table and help sorting and joins; each index slows writes and uses storage, so index the columns used in frequent filters, joins and sorts, not everything.

#### What is a composite index, and how does column order matter?

An index on several columns used left to right: an index on `(customer_id, created_at)` helps filters on `customer_id` and on `customer_id` with a range on `created_at`, but not on `created_at` alone.

#### What isolation levels do RDS engines use by default?

PostgreSQL defaults to read committed; MySQL InnoDB defaults to repeatable read. Understanding them matters for consistency of extracts and concurrency behavior.

#### How do you avoid deadlocks?

Access tables and rows in a consistent order, keep transactions short, index foreign keys and filter columns to lock fewer rows, and retry transactions that fail with deadlock errors.

#### What are soft deletes, and why do they matter for data pipelines?

Marking rows as deleted (`deleted_at`) instead of removing them. They make deletions visible to incremental extraction, but applications and pipelines must filter them consistently.

#### Why add `created_at` and `updated_at` columns to every table?

They support auditing, incremental extraction, debugging and data quality checks; `updated_at` should be maintained by the application or a trigger on every change.

### Scenarios

#### Design a highly available PostgreSQL database for a production application.

RDS for PostgreSQL (or Aurora PostgreSQL) in private subnets across AZs with Multi-AZ (or a Multi-AZ DB cluster), encryption with a customer-managed KMS key, TLS enforced, RDS-managed secrets with rotation, RDS Proxy for connection pooling, automated backups with 14–35 days retention plus AWS Backup copies to another region, Database Insights, alarms on key metrics and deletion protection, all defined in infrastructure as code.

#### The application team reports intermittent "too many connections" errors. What do you do?

Check `DatabaseConnections` against `max_connections`, find clients opening excessive connections (Lambda without pooling, missing pool limits, leaks), introduce RDS Proxy or an application pool with sensible limits, close idle connections, and size the instance if memory allows more connections.

#### A nightly report makes the production database slow. How do you fix it?

Move the report to a read replica (or a clone), optimize its queries and indexes, or move the data to an analytical store with CDC. If it must stay, schedule it outside peak hours and limit its resources.

#### Someone deleted rows from an important table 30 minutes ago. How do you recover them?

Use point-in-time recovery to restore a new instance to just before the delete, extract the deleted rows from it, and insert them back into production (or switch over if appropriate). Then review privileges and add safeguards.

#### You need to migrate a 2 TB Oracle database to Aurora PostgreSQL with minimal downtime. How?

Assess with the Schema Conversion Tool, convert schema and code (PL/SQL to PL/pgSQL), run DMS full load plus CDC to keep the target in sync, validate data (DMS validation, row counts, checksums) and application behavior, then cut over during a short window by stopping writes, letting CDC catch up and switching connections.

#### Disk usage on RDS PostgreSQL keeps growing although the data doesn't. Why?

Possible causes: an inactive logical replication slot retaining WAL, table and index bloat from autovacuum falling behind, large temporary files from heavy queries, or long logs retention. Check `pg_replication_slots`, bloat estimates, `TransactionLogsDiskUsage` and log settings.

#### How do you give the analytics team daily access to fresh copies of production data?

Use Aurora fast cloning or snapshot restores to create a separate copy each day (masked if needed), or export snapshots to S3 as Parquet for Athena, or set up zero-ETL to Redshift for near-real-time analytics without touching production.

#### How would you explain RDS to a non-technical stakeholder?

It's AWS running our databases for us: it keeps them patched, backed up and available even if a server fails, so the team can focus on the data and the application instead of maintaining machines.

#### A Lambda-based API overwhelms the database with connections during traffic spikes. What's your fix?

Put RDS Proxy between Lambda and the database with IAM authentication, set reserved concurrency on the function to cap parallelism, reuse connections across invocations, and consider caching hot reads.

#### Replica lag on a reporting replica reaches hours during nightly batches. What do you do?

Find the heavy writes on the primary (batch jobs, large transactions) and break them into smaller transactions, scale the replica's instance class and storage IOPS, avoid long-running queries on the replica that conflict with replay (PostgreSQL `max_standby_streaming_delay`), and consider a separate analytical copy.

#### Your team must upgrade from PostgreSQL 13 to 16 with minimal downtime. How do you plan it?

Check extension and parameter compatibility, test the upgrade on a restored snapshot and run application tests, then use a Blue/Green deployment: create the green environment, upgrade it, let it sync, validate, and switch over in a short window, keeping the blue environment as rollback until confident.

#### A security review finds a publicly accessible RDS instance. What do you change?

Disable public accessibility, move it to private subnets, restrict security groups to application sources, enforce TLS, rotate credentials, review logs for suspicious access, and add guardrails (Config rule, SCP) to prevent recurrence.

#### How do you set up a cross-region disaster recovery plan for an RDS MySQL database?

Create a cross-region read replica (or Aurora Global Database for Aurora), replicate automated backups or copy snapshots to the DR region, script promotion and DNS changes, keep application infrastructure ready in the DR region, and test failover periodically against your RPO and RTO.
