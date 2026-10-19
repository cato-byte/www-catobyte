## Amazon RDS Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Amazon RDS study guide: about 200 questions](../../images/aws_rds_study_guide_title_img.png)

About 200 interview-style questions on Amazon RDS and Aurora: engines, instance and storage choices, high availability with Multi-AZ, read replicas, backups and restores, security, monitoring, performance, scaling, cost, migrations, and how data engineers extract data from RDS with CDC, exports and zero-ETL. The answers reflect the service as of 2026.

The guide follows a learning path in six stages. Each section is split into short units: learning goals, a concept explanation and a worked example, then questions (recall first, then application), a practical challenge and key takeaways. To **learn**, read each unit top to bottom. To **review**, switch to review mode or use "Skip to questions", mark answers you want to see again, and try a mixed review across sections.

<!-- QA -->
<!-- stage: Foundations -->

### Fundamentals

<!-- unit: What RDS manages -->

<!-- goals -->

- Explain what Amazon RDS is and which engines it runs.
- Split responsibilities between AWS and you.

<!-- concept -->

Running a database well takes constant routine work: installing, patching, backing up, replacing failed hardware, setting up standbys. RDS turns that routine into settings. You choose an engine and size, and AWS operates the server underneath.

What stays with you is everything that depends on your data and application: schema design, queries, indexes, users and permissions, network access, and the choices about backups and availability. Managed does not mean tuned or secure by default.

<!-- example -->

| Task | Self-managed on EC2 | RDS |
|---|---|---|
| OS and engine patching | You | AWS (in your maintenance window) |
| Backups and point-in-time restore | You | AWS (you set retention) |
| Standby and failover | You | AWS (if Multi-AZ) |
| Schema, indexes, queries, users | You | You |

#### What is Amazon RDS?

Amazon Relational Database Service: a managed service to run relational databases in AWS. AWS handles provisioning, patching, backups, monitoring, failover and storage management, while you choose the engine, instance size and configuration and manage schemas, queries and users.

#### Which database engines does RDS support?

MySQL, PostgreSQL, MariaDB, Oracle, Microsoft SQL Server and IBM Db2, plus Amazon Aurora (MySQL-compatible and PostgreSQL-compatible), which is part of the RDS family but has its own storage architecture.

#### What does AWS manage for you in RDS, and what do you still manage?

AWS manages hardware, OS installation and patching, database software installation and minor version patching, automated backups, storage, Multi-AZ replication and failover, and monitoring metrics. You manage database design, queries and indexes, users and privileges, parameter tuning, security group rules, capacity choices and application connection handling.

#### What is the shared responsibility model for RDS?

AWS is responsible for the infrastructure, OS, database software patching, backups and replication mechanisms. You are responsible for network access (security groups), encryption choices, database users and privileges, schema and query design, parameter settings and protecting credentials.

#### How would you explain RDS to a non-technical stakeholder?

It's AWS running our databases for us: it keeps them patched, backed up and available even if a server fails, so the team can focus on the data and the application instead of maintaining machines.

<!-- challenge -->

A team moved to RDS and stopped thinking about the database. Six months later, queries are slow and a table was deleted by mistake. Which of these was their responsibility?

<!-- solution -->

Both. Query performance (indexes, query design) and protecting data from user mistakes (permissions, deletion protection, backup retention and tested restores) are customer responsibilities on RDS.

<!-- takeaways -->

- RDS automates infrastructure, patching, backups and failover.
- Schema, queries, users and access stay yours.
- Managed is not the same as tuned or secured.

<!-- unit: RDS, EC2 and variants -->

<!-- goals -->

- Decide when RDS is the right choice and when it isn't.
- Know RDS Custom and RDS on Outposts.

<!-- concept -->

RDS trades control for less work. You can't log into the server, install arbitrary extensions or run unusual versions. For most applications that's a good trade; for some legacy or specialized databases it isn't.

AWS fills the gaps in between: RDS Custom gives OS access for Oracle and SQL Server while keeping automation, and RDS on Outposts runs the service in your own data center. Running the database yourself on EC2 remains the full-control option, with all the work that implies.

<!-- example -->

| Requirement | Option |
|---|---|
| Standard PostgreSQL app | RDS |
| Oracle with a vendor agent on the OS | RDS Custom |
| Low-latency DB in a factory | RDS on Outposts |
| Unsupported engine or exotic setup | EC2, self-managed |

#### What is the difference between RDS and running a database on EC2?

On EC2 you get full control (OS, any version, any configuration) but you manage everything: installation, patching, backups, replication, failover and monitoring. RDS removes that operational work at the cost of some restrictions (no OS access, limited superuser privileges, supported parameters only).

#### When is RDS not the right choice?

When you need OS access or unsupported extensions (consider RDS Custom or EC2), a database engine RDS doesn't offer, extreme scale beyond a single writer (consider Aurora DSQL, DynamoDB or sharding), or analytical workloads on terabytes that suit a data warehouse or lakehouse better.

#### What is RDS Custom?

A variant of RDS for Oracle and SQL Server that gives access to the underlying OS and database customization (for legacy applications that need specific patches or software) while AWS still automates backups and some management.

#### What is RDS on Outposts?

RDS running on AWS Outposts hardware in your own data center, for workloads that need low latency to on-premises systems or data residency, managed with the same APIs.

<!-- challenge -->

A vendor's SQL Server application requires installing a monitoring agent on the database server's OS. Which option fits, and what do you still get from AWS?

<!-- solution -->

RDS Custom for SQL Server: it allows OS access for the agent while AWS still automates backups, monitoring and some maintenance. Plain RDS doesn't allow OS access.

<!-- takeaways -->

- RDS trades OS access for automation.
- RDS Custom adds OS access for Oracle and SQL Server.
- EC2 gives full control and full responsibility.

<!-- unit: Instances and classes -->

<!-- goals -->

- Describe DB instances and choose an instance class.
- Use stop, deletion protection and tags safely.

<!-- concept -->

A DB instance is the unit you pay for and operate: compute from an instance class plus attached storage. Classes come in families, from burstable for light or variable load to memory-optimized for most production databases, where data that fits in memory decides performance.

Around the instance, a few settings prevent common accidents and costs: deletion protection, stopping idle dev instances (with a time limit) and tags for ownership and cost.

<!-- example -->

```bash
aws rds create-db-instance --db-instance-identifier orders-prod \
  --engine postgres --db-instance-class db.r7g.large --allocated-storage 200 \
  --storage-type gp3 --multi-az --deletion-protection \
  --tags Key=team,Value=orders Key=env,Value=prod
```

#### What is a DB instance?

An isolated database environment in the cloud: a compute instance class (CPU and memory) with attached storage running one engine version, reachable through an endpoint (DNS name and port).

#### What is a DB instance class?

The compute and memory capacity of an instance: burstable (`db.t4g`, `db.t3`) for light or variable workloads, general purpose (`db.m*`) and memory-optimized (`db.r*`, `db.x*`) for production databases. Graviton (`g` suffix) classes usually offer better price-performance.

#### Can you stop an RDS instance?

Yes, for up to 7 days at a time; after that AWS starts it again automatically to apply maintenance. While stopped you pay for storage and backups but not instance hours. Aurora clusters can be stopped similarly.

#### What is deletion protection?

A setting that prevents an instance or cluster from being deleted until it's turned off, protecting production databases from accidental deletion.

#### What are RDS tags used for?

Cost allocation, access control (IAM conditions on tags), automation (for example stopping instances tagged `env=dev` at night) and ownership information.

<!-- challenge -->

Dev databases are stopped on Friday to save money, but by Saturday next week they're running again. Why, and what do you do?

<!-- solution -->

RDS restarts stopped instances after 7 days. Schedule stop/start daily (EventBridge Scheduler or Instance Scheduler) by tag, or use Aurora Serverless v2 or snapshots for rarely used environments.

<!-- takeaways -->

- An instance is a class plus storage.
- Memory-optimized classes suit most production databases.
- Deletion protection and tags prevent accidents and unknown costs.

<!-- unit: Configuration and maintenance -->

<!-- goals -->

- Configure engines with parameter and option groups.
- Plan maintenance and create instances as code.

<!-- concept -->

You can't edit configuration files on RDS, so engine settings live in parameter groups and optional features in option groups. Using custom groups from day one matters, because default groups can't be changed and switching later may need a reboot.

Maintenance is scheduled into a weekly window you choose. Defining instances, groups and windows as code makes environments consistent and changes reviewable.

<!-- example -->

```bash
aws rds create-db-parameter-group --db-parameter-group-name pg16-orders \
  --db-parameter-group-family postgres16 --description "orders prod"
aws rds modify-db-parameter-group --db-parameter-group-name pg16-orders \
  --parameters "ParameterName=log_min_duration_statement,ParameterValue=500,ApplyMethod=immediate"
```

#### What are parameter groups?

Containers of engine configuration settings (for example `max_connections`, `work_mem`, `innodb_buffer_pool_size`, `log_min_duration_statement`) applied to instances. Default groups can't be modified; you create custom groups. Dynamic parameters apply immediately, static ones need a reboot.

#### What are option groups?

Containers for optional features of some engines, such as Oracle Transparent Data Encryption, SQL Server native backup to S3, or MySQL's memcached plugin.

#### What is the maintenance window?

A weekly time range during which AWS applies pending maintenance such as OS patches, required minor version upgrades or instance modifications deferred to the window. With Multi-AZ, maintenance is applied to the standby first, then failover, to reduce downtime.

#### How do you create RDS instances repeatably?

With infrastructure as code (CloudFormation, CDK, Terraform), defining subnet groups, parameter groups, security groups, KMS keys, secrets and the instance, so environments are consistent and changes are reviewed.

<!-- challenge -->

You need to change a static parameter (`shared_buffers`) on a production instance that uses the default parameter group. What steps does it take?

<!-- solution -->

Create a custom parameter group, set the value there, attach the group to the instance, and reboot (preferably in the maintenance window), because static parameters apply only after a reboot.

<!-- takeaways -->

- Parameter groups hold engine settings; option groups hold features.
- Use custom groups from the start.
- Choose a maintenance window and manage it all as code.

<!-- unit: Networking and connectivity -->

<!-- goals -->

- Place RDS in a VPC with subnet groups and endpoints.
- Connect safely to private instances.

<!-- concept -->

An RDS instance lives in your VPC, in subnets you choose through a subnet group spanning at least two AZs. Applications connect through an endpoint, a DNS name that keeps working when RDS moves the instance during failover.

Production databases belong in private subnets with no public access. People who need to connect go through Session Manager port forwarding or a bastion rather than opening the database to the internet.

<!-- example -->

```bash
aws ssm start-session --target i-0bastion123 \
  --document-name AWS-StartPortForwardingSessionToRemoteHost \
  --parameters '{"host":["orders-prod.abc123.eu-west-1.rds.amazonaws.com"],"portNumber":["5432"],"localPortNumber":["5432"]}'
psql -h localhost -U analyst orders
```

#### What is a DB subnet group?

A set of subnets (in at least two Availability Zones) in a VPC where RDS can place instances. It's required to create an instance in a VPC and to support Multi-AZ.

#### What is an RDS endpoint?

The DNS name and port that applications use to connect. It stays the same during failover (the DNS record points to the new primary), so applications should always connect through the endpoint, not an IP address.

#### How do you connect to an RDS instance from your laptop if it's in a private subnet?

Through a bastion host or, better, AWS Systems Manager Session Manager port forwarding to an instance in the VPC, a client VPN, or AWS Cloud9/EC2 inside the VPC, never by making the database publicly accessible.

#### What does "publicly accessible" mean for an RDS instance?

The instance gets a public IP and its endpoint resolves to it from outside the VPC, so it's reachable from the internet if security groups allow it. Production databases should keep it disabled.

<!-- challenge -->

An application connects to RDS using the instance's IP address, and it breaks after every failover. What should it use?

<!-- solution -->

The RDS endpoint DNS name. During failover RDS points the endpoint to the new primary; IPs change. Also keep DNS caching short in the application.

<!-- takeaways -->

- Subnet groups span at least two AZs.
- Always connect through the endpoint, never IPs.
- Keep production databases private; tunnel for access.

### Storage

<!-- unit: Storage types and IOPS -->

<!-- goals -->

- Choose between gp3, gp2 and io1/io2 storage.
- Read IOPS and queue metrics to size storage.

<!-- concept -->

Databases are often limited by how fast they can read and write blocks, not by CPU. RDS storage types differ in how that speed is set: gp3 gives a baseline you can raise separately from size, older gp2 ties speed to size with burst credits, and io1/io2 provide guaranteed IOPS at low latency for demanding workloads.

Metrics tell you which case you're in: high queue depth and latency mean the disk can't keep up.

<!-- example -->

```text
ReadIOPS + WriteIOPS at peak:  5,200
gp3 baseline:                  3,000  → raise gp3 IOPS to ~6,000
DiskQueueDepth:                 35    (was 2)  → storage is the bottleneck
```

#### What storage types does RDS offer?

General Purpose SSD gp3 (baseline 3,000 IOPS and 125 MiB/s, with IOPS and throughput configurable independently of size), gp2 (IOPS tied to size with burst credits), Provisioned IOPS io1 and io2 Block Express (consistent high IOPS and low latency), and legacy magnetic storage.

#### When should you choose Provisioned IOPS?

For I/O-intensive production workloads that need consistent low latency and high IOPS (busy OLTP, large write volumes), where gp3's configurable limits aren't enough or predictability matters more than cost.

#### How does gp3 compare with io2 for RDS?

gp3 offers a baseline of 3,000 IOPS and 125 MiB/s, configurable up to higher limits at extra cost, at a lower price per GB. io2 Block Express offers higher, more consistent IOPS and lower latency with better durability, for the most demanding workloads.

#### Why can gp2 performance suddenly drop?

gp2 small volumes rely on burst credits above their baseline IOPS (3 IOPS per GB). When credits run out, performance falls to the baseline. gp3 avoids this by providing a fixed baseline independent of size.

#### How do you estimate the IOPS you need?

From current metrics (`ReadIOPS` + `WriteIOPS` at peak), or for new workloads from expected transactions per second and I/O per transaction, with headroom; then test with load before production.

#### What is `DiskQueueDepth` telling you?

The number of outstanding I/O requests waiting for the disk. A consistently high queue depth with high latency means the storage can't keep up; consider more IOPS, better queries or caching.

<!-- challenge -->

A 100 GB gp2 database is fast in the morning and slow every afternoon during batch loads. What is happening, and what do you change?

<!-- solution -->

gp2's baseline is 300 IOPS for 100 GB; batch loads drain burst credits, then performance drops to baseline. Move to gp3 (3,000 IOPS baseline, adjustable) or io2 if latency must be consistent.

<!-- takeaways -->

- gp3 decouples IOPS from size; gp2 relies on bursts.
- io1/io2 guarantee IOPS for demanding workloads.
- High queue depth means storage is the bottleneck.

<!-- unit: Growing and changing storage -->

<!-- goals -->

- Avoid running out of storage with autoscaling.
- Know what storage changes can and can't do.

<!-- concept -->

Running out of space stops writes, so RDS offers storage autoscaling up to a maximum you set. Growth is easy; shrinking is not: allocated storage can only go up, and reducing it means moving data to a new instance.

Changes to size or type usually happen online, but the instance enters an optimization phase, and there's a cooldown before the next change. Plan storage changes rather than making them during an incident.

<!-- example -->

```bash
aws rds modify-db-instance --db-instance-identifier orders-prod \
  --max-allocated-storage 1000 --apply-immediately     # enable autoscaling up to 1 TB
```

#### What is storage autoscaling?

A setting that automatically increases allocated storage when free space is low, up to a maximum you define, avoiding outages caused by full disks. Storage can't be decreased afterwards.

#### Can you reduce allocated storage in RDS?

Not directly. To shrink, create a new instance with smaller storage and migrate the data (dump and restore, DMS, or logical replication), or use Blue/Green deployments where supported.

#### What is the maximum storage of an RDS instance?

Up to 64 TiB for most engines (lower for some SQL Server configurations). Aurora storage grows automatically up to 128 TiB per cluster.

#### What does "storage-full" status mean?

The instance has run out of storage and stops accepting writes. Enable storage autoscaling, alert on `FreeStorageSpace`, and clean up large tables, logs or temporary files.

#### What is the impact of modifying storage on a running instance?

Increasing storage or changing type usually happens online, but the instance may enter a "storage-optimization" state for hours during which further storage changes aren't possible; performance can be affected slightly.

<!-- challenge -->

A team allocated 4 TB "to be safe" for a database that uses 300 GB. Can they shrink it, and how?

<!-- solution -->

Not in place. Create a new instance with smaller storage and autoscaling enabled, migrate the data (dump and restore, DMS or replication), switch the application, then delete the old instance.

<!-- takeaways -->

- Storage autoscaling prevents "storage-full" outages.
- Allocated storage can grow but not shrink.
- Storage changes trigger optimization and cooldowns.

<!-- stage: Availability and data protection -->

### High availability and Multi-AZ

<!-- unit: Multi-AZ deployments -->

<!-- goals -->

- Explain Multi-AZ instance and cluster deployments.
- Describe how failover works and what RPO and RTO it gives.

<!-- concept -->

Multi-AZ protects against losing a server or a whole Availability Zone. RDS keeps a standby in another AZ with synchronous replication, so every committed write exists in both places. When the primary fails, the standby is promoted and the endpoint points to it.

The instance flavor's standby is invisible and only waits. The cluster flavor has two readable standbys and fails over faster. Either way, RPO is essentially zero and recovery takes about a minute or two.

<!-- example -->

```text
AZ a: primary  ── synchronous replication ──►  AZ b: standby
         ▲
endpoint orders-prod.xxxx.rds.amazonaws.com  (DNS flips to b on failover)
```

#### What is a Multi-AZ instance deployment?

RDS keeps a synchronous standby replica of the primary in another Availability Zone. If the primary fails (hardware, AZ outage, storage failure) or during certain maintenance, RDS fails over automatically to the standby, typically in one to two minutes. The standby doesn't serve reads.

#### What is a Multi-AZ DB cluster deployment?

A deployment (for MySQL and PostgreSQL) with one writer and two readable standby instances in three AZs, using semi-synchronous replication. Failover is faster (typically under 35 seconds) and the standbys can serve read traffic through a reader endpoint.

#### How does Multi-AZ failover work?

RDS detects the failure, promotes the standby, and updates the endpoint's DNS record to point to it. Applications must reconnect; connection pools should handle disconnects and respect DNS TTL.

#### What events trigger an automatic failover?

Loss of the primary instance or its AZ, network or storage failure on the primary, instance type changes, OS patching and some engine maintenance, and manual reboot with failover.

#### Can you choose which AZ the standby goes in?

RDS chooses the standby AZ within the subnet group; you choose the primary AZ. Subnets in at least two (or three for Multi-AZ DB clusters) AZs must exist in the subnet group.

#### What RPO and RTO does Multi-AZ give?

For Multi-AZ instance deployments, RPO is effectively zero (synchronous replication) and RTO is typically one to two minutes; for Multi-AZ DB clusters, RTO is usually under a minute.

<!-- challenge -->

A business asks for "no data loss and under 5 minutes of downtime" if an AZ fails. Does Multi-AZ meet it?

<!-- solution -->

Yes. Synchronous replication gives an RPO of effectively zero, and failover usually completes in one to two minutes (faster with Multi-AZ DB clusters), within the 5-minute target.

<!-- takeaways -->

- Multi-AZ keeps a synchronous standby in another AZ.
- Failover promotes the standby and flips the endpoint.
- RPO ≈ 0; RTO about 1–2 minutes.

<!-- unit: Living with failover -->

<!-- goals -->

- Prepare applications for failover and test it.
- Know what Multi-AZ doesn't protect against.

<!-- concept -->

Failover is only half the story; the application must reconnect. Clients that cache DNS for long, hold connections without retries or hard-code IPs turn a one-minute failover into a long outage. Testing with a forced failover reveals this before it matters.

Multi-AZ also has clear limits. The standby doesn't serve reads in the classic setup, so it isn't scaling, and it faithfully replicates mistakes, so it isn't a backup. Regional disasters need a separate recovery plan.

<!-- example -->

```bash
aws rds reboot-db-instance --db-instance-identifier orders-prod --force-failover
# then watch: app errors, reconnect time, connection pool behavior
```

#### How do you test a failover?

Reboot the instance with the "reboot with failover" option and observe application behavior, reconnection time and errors. Doing this regularly validates the application's resilience.

#### How should applications handle failover?

Use the endpoint (never IPs), set short DNS caching (for example JVM DNS TTL), implement retries with backoff on connection errors, use connection pools that validate connections, and consider RDS Proxy or AWS drivers that speed up failover detection.

#### What are the AWS Advanced JDBC/Python wrappers?

Driver wrappers that understand RDS and Aurora topologies, detect failovers faster than DNS updates, and reconnect to the new writer, reducing downtime perceived by applications.

#### Is Multi-AZ a scaling solution?

No. For Multi-AZ instance deployments the standby can't serve traffic; it's for availability and durability. Use read replicas (or Multi-AZ DB clusters' readable standbys, or Aurora replicas) for read scaling.

#### Does Multi-AZ protect against data corruption or accidental deletes?

No. Replication copies every change, including bad ones, to the standby. Backups, point-in-time recovery and snapshots protect against logical errors.

#### What is the difference between high availability and disaster recovery for RDS?

High availability (Multi-AZ) keeps the database running when an AZ or instance fails within a region. Disaster recovery covers losing a region or data: cross-region read replicas, cross-region snapshot copies, AWS Backup and Aurora Global Database, with defined RPO and RTO.

<!-- challenge -->

After a test failover, the database is back in 60 seconds, but the Java application keeps failing for 15 minutes. What is the likely cause?

<!-- solution -->

The JVM caches DNS (sometimes indefinitely), so the app keeps connecting to the old primary's IP. Set a short DNS TTL in the JVM, add retries, and consider the AWS Advanced JDBC Wrapper for faster failover detection.

<!-- takeaways -->

- Applications must reconnect quickly; test it.
- Multi-AZ isn't read scaling or a backup.
- High availability isn't disaster recovery.

### Read replicas

<!-- unit: Replicas and lag -->

<!-- goals -->

- Explain read replicas, replica lag and stale reads.
- Route reads to replicas safely.

<!-- concept -->

Read replicas copy changes from the primary asynchronously, which lets them serve reads without slowing writes. The price is lag: a replica is always a little behind, sometimes a lot, so reading your own write right after making it may not work.

That shapes how applications use them. Read-heavy, slightly stale-tolerant queries go to replicas; anything that must see the latest write goes to the primary.

<!-- example -->

```python
WRITER = "orders-prod.xxxx.rds.amazonaws.com"
READER = "orders-replica-1.xxxx.rds.amazonaws.com"

def get_order_after_payment(order_id):
    return query(WRITER, "SELECT * FROM orders WHERE id = %s", order_id)  # must be fresh

def list_catalog():
    return query(READER, "SELECT * FROM products WHERE active")             # lag is fine
```

#### What is a read replica?

A copy of a source instance kept up to date with asynchronous replication, used to offload read traffic (reports, analytics, read-heavy APIs). It has its own endpoint and can be in the same region or another region.

#### How many read replicas can you create?

Up to 15 for MySQL, MariaDB and PostgreSQL, and fewer for Oracle and SQL Server; Aurora supports up to 15 Aurora Replicas per cluster. Replicas can also have their own replicas for some engines.

#### What is replica lag?

The delay between a write on the source and its visibility on the replica, monitored with the `ReplicaLag` metric. Heavy writes, long transactions, undersized replicas and network distance (cross-region) increase it.

#### Why might reading from a replica return stale data?

Because replication is asynchronous: a read immediately after a write may not see it. Applications needing read-your-writes consistency should read from the primary for that path.

#### Can you write to a read replica?

Not normally: replicas are read-only. For MySQL you can set `read_only = 0` on a replica for special cases like adding indexes for reporting, but writes can break replication and are discouraged.

#### How do you route reads to replicas?

In the application (separate read and write data sources), through a proxy or driver that supports read/write splitting, or with Aurora's reader endpoint, which load-balances connections across replicas.

#### Do read replicas need automated backups on the source?

Yes. Automated backups must be enabled on the source instance (backup retention greater than zero) to create read replicas for most engines.

<!-- challenge -->

After moving reads to a replica, users sometimes don't see the comment they just posted. How do you fix it without abandoning replicas?

<!-- solution -->

Send reads that follow a user's own write to the primary (read-your-writes), for example for a few seconds after a write or for that user's session, and keep other reads on the replica.

<!-- takeaways -->

- Replicas replicate asynchronously and lag.
- Route freshness-critical reads to the primary.
- Replicas need automated backups on the source.

<!-- unit: Replica topologies -->

<!-- goals -->

- Use replicas across Regions, with Multi-AZ, and as delayed copies.
- Promote replicas and know how they behave during failover.

<!-- concept -->

Replicas do more than scale reads. In another Region they bring data closer to users and give you a disaster-recovery copy you can promote. Made Multi-AZ themselves, they survive AZ failures. With a delay, they keep a window in which mistakes on the primary haven't arrived yet.

Promotion is a one-way door: the replica becomes an independent database, and replication stops.

<!-- example -->

```bash
aws rds create-db-instance-read-replica --db-instance-identifier orders-dr \
  --source-db-instance-identifier arn:aws:rds:eu-west-1:123456789012:db:orders-prod \
  --region eu-central-1 --kms-key-id alias/rds-dr
# during a regional disaster:
aws rds promote-read-replica --db-instance-identifier orders-dr --region eu-central-1
```

#### Can you promote a read replica?

Yes. Promotion turns it into a standalone instance that accepts writes, breaking replication. It's used for disaster recovery, migrations or splitting a database.

#### What are cross-region read replicas used for?

Serving reads close to users in another region, disaster recovery (promote if the primary region fails), and migrating a database to another region.

#### Can a read replica be Multi-AZ?

Yes, for supported engines a read replica can itself be configured as Multi-AZ, which improves the availability of the replica (useful when it may be promoted for DR).

#### What happens to replicas when the source fails over in Multi-AZ?

Replicas automatically follow the new primary after a Multi-AZ failover, because the source endpoint and replication stream continue from the standby.

#### What is a delayed replica?

A replica (MySQL, MariaDB) configured to apply changes with a delay, for example one hour, so you can recover from mistakes by promoting it before the bad change is applied.

<!-- challenge -->

Someone ran a bad `UPDATE` without `WHERE` on MySQL 10 minutes ago. A one-hour delayed replica exists. How can it help?

<!-- solution -->

Stop replication on the delayed replica before the bad statement is applied, apply changes up to just before it, then copy the correct rows back to the primary (or promote the replica if needed).

<!-- takeaways -->

- Cross-Region replicas serve distant reads and DR.
- Promotion makes a replica independent; replication ends.
- Delayed replicas give a window to recover from mistakes.

<!-- unit: Replicas for analytics -->

<!-- goals -->

- Offload reporting and extraction to replicas.
- Handle replica lag caused by heavy primary writes.

<!-- concept -->

Analytics and transactions compete for the same CPU, memory and I/O. A replica sized for reporting moves heavy queries off the primary so customers don't feel them.

Replicas share the primary's write load, though: every change must be replayed. Big batch writes or long transactions on the primary show up as lag on the replica, and long queries on the replica can delay replay further.

<!-- example -->

```sql
-- on the primary: break one huge update into batches
UPDATE orders SET status = 'archived'
WHERE id IN (SELECT id FROM orders WHERE created_at < '2024-01-01' AND status <> 'archived' LIMIT 10000);
-- repeat until 0 rows; replicas apply each small transaction quickly
```

#### How do you use read replicas for analytics without hurting production?

Point reporting and extraction jobs at a replica sized for analytic queries, so long-running reads don't compete with OLTP traffic on the primary; monitor lag so reports know how fresh data is.

#### A nightly report makes the production database slow. How do you fix it?

Move the report to a read replica (or a clone), optimize its queries and indexes, or move the data to an analytical store with CDC. If it must stay, schedule it outside peak hours and limit its resources.

#### Replica lag on a reporting replica reaches hours during nightly batches. What do you do?

Find the heavy writes on the primary (batch jobs, large transactions) and break them into smaller transactions, scale the replica's instance class and storage IOPS, avoid long-running queries on the replica that conflict with replay (PostgreSQL `max_standby_streaming_delay`), and consider a separate analytical copy.

<!-- challenge -->

Analysts need yesterday's data at 07:00, but replica lag reaches three hours during the nightly batch. List two changes.

<!-- solution -->

Break the batch's large transactions into smaller ones (and schedule them earlier), and give the replica enough I/O and CPU to replay changes. If analysts don't need minute freshness, a daily snapshot export to S3 avoids the problem.

<!-- takeaways -->

- Replicas move analytics off the primary.
- Large primary transactions cause replica lag.
- For daily analytics, exports or lakes may fit better.

### Backups and restore

<!-- unit: Automated backups and point-in-time recovery -->

<!-- goals -->

- Explain automated backups and point-in-time recovery.
- Recover from accidental deletes and know how restores behave.

<!-- concept -->

Automated backups combine a daily snapshot with transaction logs saved every few minutes, which lets RDS rebuild the database at any second within the retention period. That's the main protection against human mistakes, since replicas copy mistakes too.

Restores never overwrite: they create a new instance, which starts fast but loads data lazily from S3, so first queries are slow. Recovering a few rows means restoring next to production and copying them back.

<!-- example -->

```bash
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier orders-prod \
  --target-db-instance-identifier orders-restore-0930 \
  --restore-time 2026-10-17T09:29:00Z
pg_dump -h orders-restore-0930... -t public.invoices --data-only | psql -h orders-prod...
```

#### What are automated backups?

Daily snapshots of the instance plus transaction logs captured every few minutes, retained for a configurable period (1 to 35 days; 0 disables them), enabling point-in-time recovery within the retention window.

#### What is point-in-time recovery?

Restoring the database to any second within the backup retention period (up to about the last five minutes), which creates a new instance with a new endpoint. It's the main tool for recovering from accidental changes.

#### Can you restore a snapshot into the existing instance?

No. Restores always create a new instance. You then point applications to the new endpoint (or rename instances to reuse the old endpoint name).

#### How long does a restore take?

It depends on database size and activity: creating the instance from the snapshot is fast, but data loads lazily from S3, so first queries can be slow until blocks are read (initializing or "warming" may be needed for performance-critical restores).

#### What is lazy loading after a restore?

When an instance is restored from a snapshot, its storage blocks are fetched from S3 on first access, so initial reads have higher latency. Running full table scans after the restore warms the storage.

#### Can you restore a single table from a backup?

Not directly. Restore the whole instance to a new one (point-in-time), then dump the needed table and import it into production.

#### Someone deleted rows from an important table 30 minutes ago. How do you recover them?

Use point-in-time recovery to restore a new instance to just before the delete, extract the deleted rows from it, and insert them back into production (or switch over if appropriate). Then review privileges and add safeguards.

<!-- challenge -->

A restored instance for a disaster test answers queries very slowly for the first hour. Is something wrong?

<!-- solution -->

No, that's lazy loading: blocks are fetched from S3 on first access. Warm it up by reading the important tables (for example full scans or `pg_prewarm`) before sending real traffic.

<!-- takeaways -->

- Automated backups enable restore to any second in retention.
- Restores create new instances.
- Restored storage loads lazily; warm it up.

<!-- unit: Snapshots and retention -->

<!-- goals -->

- Manage manual snapshots, copies and long-term retention.
- Protect backups across Regions and accounts.

<!-- concept -->

Automated backups expire with their retention; manual snapshots stay until deleted. Long-term and compliance needs therefore rely on snapshots, ideally managed by AWS Backup with policies, vaults and locks that prevent deletion.

A backup in the same account and Region shares their fate, so copies to another Region or account protect against regional outages and compromised accounts. Deleting an instance is the moment to decide what to keep.

<!-- example -->

```bash
aws rds copy-db-snapshot \
  --source-db-snapshot-identifier arn:aws:rds:eu-west-1:123456789012:snapshot:orders-2026-10 \
  --target-db-snapshot-identifier orders-2026-10-dr --kms-key-id alias/rds-dr \
  --region eu-central-1
```

#### What are manual snapshots?

User-initiated snapshots that are kept until you delete them, independent of the automated backup retention. They're used before risky changes, for long-term retention and to copy or share databases.

#### How do you copy backups to another region or account?

Copy snapshots to another region (cross-region snapshot copy, optionally automated with AWS Backup or cross-region automated backup replication) and share snapshots with other accounts (encrypted snapshots require sharing the KMS key).

#### What is cross-region automated backup replication?

A feature that copies automated backups and transaction logs to another region, so you can do point-in-time recovery in the DR region.

#### What is AWS Backup's role with RDS?

AWS Backup centralizes backup policies across services: schedules, retention, cross-region and cross-account copies, vault locks for immutability, and compliance reports for RDS and Aurora.

#### How do you keep backups for seven years for compliance?

Use AWS Backup with a long retention plan and vault lock, or copy manual snapshots periodically; automated backups max out at 35 days. Exporting to S3 with lifecycle rules can also serve archival needs.

#### What happens to automated backups when you delete an instance?

You can retain them (until their retention expires) and take a final snapshot. Without a final snapshot and retained backups, the data is gone; deletion protection and final snapshots prevent mistakes.

#### Do backups affect performance?

With Multi-AZ, backups are taken from the standby, so the primary isn't impacted. On single-AZ instances, I/O may briefly be suspended during the snapshot, which can affect performance.

<!-- challenge -->

Ransomware deleted the instance and its snapshots using a compromised admin account. What design would have saved the data?

<!-- solution -->

Copies of backups in a separate account (and Region) with an AWS Backup vault lock, so even an admin in the production account can't delete them. Combine with least privilege and MFA on admin roles.

<!-- takeaways -->

- Manual snapshots and AWS Backup serve long retention.
- Copy backups to another Region and account.
- Vault locks protect backups from deletion.

### Security

<!-- unit: Network access -->

<!-- goals -->

- Restrict network access to RDS with subnets and security groups.
- Connect Lambda and fix publicly accessible instances.

<!-- concept -->

The first security layer is reachability. Databases in private subnets without public access can only be reached from inside the network, and security groups narrow that further to specific application groups instead of IP ranges.

Referencing security groups instead of addresses keeps rules correct as instances and functions scale and change IPs.

<!-- example -->

```text
sg-app     (attached to ECS tasks and Lambda)
sg-db      inbound: TCP 5432 from sg-app   ← no CIDR ranges, no 0.0.0.0/0
RDS:       private subnets, PubliclyAccessible = false
```

#### How do you control network access to RDS?

Place instances in private subnets, disable public accessibility, and use VPC security groups to allow only the application's security groups or specific CIDR ranges on the database port. Access from on-premises goes through VPN or Direct Connect.

#### How do you limit network access from Lambda to RDS?

Run Lambda in the VPC with its own security group, allow only that security group on the database port, and use RDS Proxy with IAM authentication to avoid storing passwords in the function.

#### A security review finds a publicly accessible RDS instance. What do you change?

Disable public accessibility, move it to private subnets, restrict security groups to application sources, enforce TLS, rotate credentials, review logs for suspicious access, and add guardrails (Config rule, SCP) to prevent recurrence.

<!-- challenge -->

A database security group allows `0.0.0.0/0` on port 3306 "temporarily" for a contractor. What do you replace it with?

<!-- solution -->

Remove the rule, keep the instance private, and give the contractor access through Session Manager port forwarding (or a client VPN) with an IAM identity, so access is authenticated and logged.

<!-- takeaways -->

- Private subnets and no public access first.
- Security groups should reference other security groups.
- Give people access through tunnels, not open ports.

<!-- unit: Encryption -->

<!-- goals -->

- Encrypt RDS data at rest and in transit.
- Encrypt existing instances and enforce encryption by policy.

<!-- concept -->

Encryption at rest with KMS covers storage, backups, snapshots and replicas, and it can only be chosen when an instance is created. Encrypting an existing database therefore means copying a snapshot with encryption and restoring it.

Encryption in transit relies on TLS, which you can require through parameters. Policies make encryption non-optional, and customer-managed keys are needed to share encrypted snapshots across accounts.

<!-- example -->

```bash
aws rds copy-db-snapshot --source-db-snapshot-identifier orders-plain \
  --target-db-snapshot-identifier orders-encrypted --kms-key-id alias/rds-prod
aws rds restore-db-instance-from-db-snapshot --db-instance-identifier orders-prod-enc \
  --db-snapshot-identifier orders-encrypted
# PostgreSQL: rds.force_ssl = 1 in the parameter group
```

#### How is data encrypted at rest in RDS?

With AWS KMS keys (AWS-managed or customer-managed), covering storage, automated backups, snapshots, read replicas and logs. Encryption must be chosen at creation.

#### How do you encrypt an existing unencrypted RDS instance?

Take a snapshot, copy it with encryption enabled using a KMS key, and restore a new instance from the encrypted copy; then switch applications to it. Read replicas of an unencrypted instance can't be encrypted directly.

#### How is data encrypted in transit?

With SSL/TLS connections using the RDS certificate authority bundle. You can enforce TLS with parameters such as `rds.force_ssl` (PostgreSQL, SQL Server) or `require_secure_transport` (MySQL). Certificates must be rotated when RDS rotates its CAs.

#### How do you share an encrypted snapshot with another account?

Use a customer-managed KMS key (snapshots encrypted with the AWS-managed key can't be shared), grant the other account access to the key, and share the snapshot; the other account copies it with its own key.

#### How do you prevent unencrypted databases from being created?

Use an SCP or IAM condition `rds:StorageEncrypted = true` on create actions, AWS Config rules (`rds-storage-encrypted`) to detect violations, and infrastructure as code defaults.

<!-- challenge -->

You must share an encrypted snapshot with an analytics account, but the copy fails. What is wrong?

<!-- solution -->

The snapshot is encrypted with the AWS-managed RDS key, which can't be shared. Copy it with a customer-managed KMS key, grant the other account use of that key, then share the snapshot.

<!-- takeaways -->

- Encryption at rest is chosen at creation; copy to change it.
- Require TLS with engine parameters.
- Shared encrypted snapshots need customer-managed keys.

<!-- unit: Authentication and database users -->

<!-- goals -->

- Choose between passwords, IAM authentication and Kerberos.
- Design least-privilege database users.

<!-- concept -->

Who connects to the database matters as much as from where. Passwords should live in Secrets Manager with rotation, ideally managed by RDS itself. IAM authentication replaces passwords with short-lived tokens tied to IAM roles; Kerberos links logins to a corporate directory.

Inside the database, the master user is for administration only. Each application gets its own user with just the privileges it needs, which limits damage and makes audit logs meaningful.

<!-- example -->

```sql
CREATE ROLE orders_app LOGIN;
GRANT CONNECT ON DATABASE shop TO orders_app;
GRANT USAGE ON SCHEMA orders TO orders_app;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA orders TO orders_app;
GRANT rds_iam TO orders_app;           -- PostgreSQL: allow IAM token authentication
```

#### What is IAM database authentication?

For MySQL, MariaDB and PostgreSQL (and Aurora), users authenticate with a short-lived token generated from IAM credentials instead of a password, so access is controlled with IAM policies and no database passwords are stored in applications.

#### How should you manage database passwords?

Use Secrets Manager, ideally with RDS-managed master user passwords (RDS creates and rotates the secret), rotate application user secrets automatically, and never hard-code credentials.

#### What privileges does the master user have?

Broad administrative privileges within the engine's limits (for example `rds_superuser` in PostgreSQL), but not full superuser or OS access. Create separate users with least privilege for applications and pipelines.

#### What is Kerberos authentication on RDS?

Integration with AWS Managed Microsoft AD (or self-managed AD through a trust) so users log in to SQL Server, Oracle, PostgreSQL or MySQL with their directory credentials and centralized account management.

#### What is a good practice for application database users?

One user per application or service with only the privileges it needs (often schema-level `SELECT`, `INSERT`, `UPDATE`, `DELETE`, no DDL), separate read-only users for reporting, and DDL handled by migration tooling with a separate user.

<!-- challenge -->

Three services and five analysts all use the master user. What do you change first?

<!-- solution -->

Create one user per service and per analyst group with only the privileges they need (read-only for analysts), store credentials in Secrets Manager or use IAM authentication, then rotate the master password and restrict who can use it.

<!-- takeaways -->

- Store and rotate passwords with Secrets Manager.
- IAM and Kerberos replace static passwords.
- One least-privilege user per application.

<!-- unit: Audit and guardrails -->

<!-- goals -->

- Audit database activity and API changes.
- Prevent risky changes to RDS resources.

<!-- concept -->

Two kinds of activity need watching. Inside the engine, audit logs and activity streams record who queried or changed data. Around it, CloudTrail records who modified instances, snapshots and settings.

Guardrails stop mistakes before they need investigating: IAM policies that limit who can modify or delete production databases, deletion protection, and separate roles or accounts for production.

<!-- example -->

```json
{
  "Effect": "Deny",
  "Action": ["rds:DeleteDBInstance", "rds:ModifyDBInstance"],
  "Resource": "arn:aws:rds:*:*:db:*",
  "Condition": {"StringEquals": {"aws:ResourceTag/env": "prod"},
                "StringNotEquals": {"aws:PrincipalTag/role": "dba"}}
}
```

#### How do you audit database activity?

Engine logs (PostgreSQL `pgaudit`, MySQL audit plugin, SQL Server audit, Oracle unified auditing) published to CloudWatch Logs, CloudTrail for RDS API calls, and Database Activity Streams for near-real-time activity sent to Kinesis (for compliance tools).

#### What are Database Activity Streams?

A feature (for Aurora and some RDS engines) that pushes a real-time stream of database activity to Kinesis Data Streams, encrypted with KMS and separated from DBA control, for monitoring and compliance.

#### How do you protect RDS from accidental changes by humans?

Least-privilege IAM for RDS APIs, deletion protection, separate accounts or roles for production, change management through infrastructure as code, and audits of who can modify instances and parameter groups.

#### How do you restrict which IAM users can create or modify RDS instances?

With IAM policies on RDS actions (`rds:CreateDBInstance`, `rds:ModifyDBInstance`, `rds:DeleteDBInstance`), conditions on tags, and service control policies in AWS Organizations for guardrails such as requiring encryption.

<!-- challenge -->

A developer resized a production database during business hours, causing an outage. Which controls prevent this?

<!-- solution -->

An IAM policy denying `rds:ModifyDBInstance` on prod-tagged instances except for a DBA role, changes deployed through IaC with review, and modifications scheduled for the maintenance window instead of applied immediately.

<!-- takeaways -->

- Engine audit logs and activity streams track data access.
- CloudTrail tracks changes to RDS resources.
- IAM guardrails and IaC prevent risky changes.

<!-- stage: Operating RDS -->

### Monitoring and performance

<!-- unit: Metrics, logs and events -->

<!-- goals -->

- Know which metrics, tools and logs to watch on RDS.
- Set up alerts and event notifications.

<!-- concept -->

RDS gives three levels of visibility. CloudWatch metrics show the instance's vital signs. Enhanced Monitoring shows the operating system underneath, per process. Performance Insights shows what the database is busy doing, broken down by waits and queries, which is usually where the answer is.

Logs and events complete the picture: slow query logs show expensive statements, and event notifications tell you about failovers, reboots and storage warnings as they happen.

<!-- example -->

| Metric | Worry when |
|---|---|
| `CPUUtilization` | sustained > 80% |
| `FreeableMemory` | low and `SwapUsage` rising |
| `FreeStorageSpace` | below 15% |
| `DatabaseConnections` | near `max_connections` |
| `ReadLatency` / `WriteLatency` | rising with `DiskQueueDepth` |
| `ReplicaLag` | above what readers tolerate |

#### Which CloudWatch metrics are most important for RDS?

`CPUUtilization`, `FreeableMemory`, `FreeStorageSpace`, `ReadIOPS`/`WriteIOPS`, `ReadLatency`/`WriteLatency`, `DiskQueueDepth`, `DatabaseConnections`, `ReplicaLag`, `SwapUsage` and, for burstable classes, `CPUCreditBalance`.

#### What is Enhanced Monitoring?

OS-level metrics (per process CPU and memory, file system, swap, disk I/O) collected by an agent at intervals down to one second and sent to CloudWatch Logs, which helps find causes that standard metrics miss.

#### What is Performance Insights / Database Insights?

A database performance tool that shows database load (average active sessions) broken down by wait events, SQL statements, users and hosts, so you can see which queries cause load and why. It is now part of CloudWatch Database Insights, which adds fleet-wide views and longer retention in its advanced mode.

#### What logs can RDS publish to CloudWatch Logs?

Error logs, slow query logs, general logs (MySQL), PostgreSQL logs (including `log_min_duration_statement` output and `pgaudit`), audit logs, upgrade logs and agent logs, depending on engine and settings.

#### What are RDS event notifications?

Notifications sent through EventBridge or SNS for events such as failovers, reboots, low storage, backups, configuration changes and maintenance, used for alerting and automation.

#### How do you alert on RDS problems?

CloudWatch alarms on CPU, free storage, freeable memory, connections, replica lag, read/write latency and burst balance; EventBridge rules on RDS events (failover, storage full, maintenance); and anomaly detection in Database Insights.

<!-- challenge -->

CPU on a database is at 95% and the team plans to double the instance size. What do you check first?

<!-- solution -->

Performance Insights: which queries and wait events make up the load. Often a few queries with missing indexes or bad plans dominate; fixing them is cheaper than a bigger instance.

<!-- takeaways -->

- Metrics for vitals, Enhanced Monitoring for the OS, Insights for load.
- Slow query logs find expensive statements.
- Alert on CPU, memory, storage, connections, latency and lag.

<!-- unit: Diagnosing load -->

<!-- goals -->

- Find the causes of high CPU and low memory.
- Locate slow queries and lock waits.

<!-- concept -->

Database load has few root causes: queries doing too much work, too many sessions at once, not enough memory for the working set, and sessions waiting on each other. The tools point to which one applies. Performance Insights shows top queries and wait events; slow logs and query statistics show which statements cost most; memory metrics show whether the cache fits.

Fixing the cause, usually a query or an index, beats adding hardware.

<!-- example -->

```sql
-- PostgreSQL: top statements by total time
SELECT left(query, 80) AS query, calls, round(total_exec_time) AS total_ms, round(mean_exec_time) AS mean_ms
FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 10;
```

#### What causes high CPU on an RDS instance?

Inefficient queries (missing indexes, full scans, poor plans), too many concurrent connections, heavy reporting on the primary, lock contention or an undersized instance. Find the top SQL first, then tune or scale.

#### What is `FreeableMemory` and when should it worry you?

The RAM available on the instance. Low freeable memory with rising `SwapUsage` means the workload doesn't fit (buffer pool, connections, sorts); scale up or reduce memory consumption.

#### How do you find slow queries in RDS?

Enable slow query logs (MySQL `slow_query_log` and `long_query_time`, PostgreSQL `log_min_duration_statement`), use `pg_stat_statements` or Performance Schema, and analyze Database Insights top SQL; then run `EXPLAIN` to fix plans and indexes.

#### How do locks show up in RDS performance tools?

As wait events (for example `Lock:transactionid` or `Lock:relation` in PostgreSQL, `synch/cond/innodb/row_lock_wait` in MySQL) in Database Insights; queries like `pg_locks` with `pg_stat_activity` show who blocks whom.

<!-- challenge -->

Performance Insights shows most load as `Lock:transactionid` waits in PostgreSQL. What does it mean, and what do you look for?

<!-- solution -->

Sessions are waiting for other transactions to commit or roll back, usually on the same rows. Find long-running or idle-in-transaction sessions holding locks (`pg_stat_activity`, `pg_locks`), and shorten or reorder the transactions involved.

<!-- takeaways -->

- Most load comes from expensive queries or too many sessions.
- `pg_stat_statements` and slow logs rank costly queries.
- Lock waits point to long or conflicting transactions.

<!-- unit: Connections and RDS Proxy -->

<!-- goals -->

- Diagnose connection exhaustion.
- Use RDS Proxy for many short-lived clients.

<!-- concept -->

Each database connection costs memory, and engines have a maximum. Applications without pooling, and especially serverless functions that scale to hundreds of copies, can exhaust it in seconds during a spike.

RDS Proxy sits between clients and the database and shares a small pool of connections among many clients. It also speeds up failover and integrates with IAM and Secrets Manager, which makes it the default fix for Lambda-heavy architectures.

<!-- example -->

```text
800 Lambda invocations ─► RDS Proxy (pool: 80 connections) ─► RDS (max_connections 200)
without proxy:          800 direct connections ─► "too many connections"
```

#### What causes running out of connections?

Applications without pooling opening many connections (serverless functions are a classic case), leaked connections, low `max_connections` for the instance's memory, or a spike in traffic. Use pooling (RDS Proxy, PgBouncer) and fix leaks.

#### What is RDS Proxy?

A managed database proxy that pools and shares connections between applications and RDS or Aurora, reduces connection overhead (especially from Lambda), speeds up failover by keeping client connections and redirecting them, and supports IAM authentication and Secrets Manager.

#### When should you use RDS Proxy?

With Lambda or other highly concurrent, short-lived clients, applications that open many connections, or when you want faster, more transparent failover. It adds cost and a small latency, and some session features (pinning) reduce its benefit.

#### The application team reports intermittent "too many connections" errors. What do you do?

Check `DatabaseConnections` against `max_connections`, find clients opening excessive connections (Lambda without pooling, missing pool limits, leaks), introduce RDS Proxy or an application pool with sensible limits, close idle connections, and size the instance if memory allows more connections.

#### A Lambda-based API overwhelms the database with connections during traffic spikes. What's your fix?

Put RDS Proxy between Lambda and the database with IAM authentication, set reserved concurrency on the function to cap parallelism, reuse connections across invocations, and consider caching hot reads.

<!-- challenge -->

Raising `max_connections` from 500 to 5,000 stopped the errors, but the database got slower. Why?

<!-- solution -->

Each connection consumes memory and CPU for scheduling, so thousands of connections squeeze the cache and add contention. Keep a moderate limit and pool connections (in the app or with RDS Proxy) instead.

<!-- takeaways -->

- Unpooled and serverless clients exhaust connections.
- RDS Proxy pools and shares connections.
- Raising `max_connections` isn't a fix.

<!-- unit: Engine tuning -->

<!-- goals -->

- Tune PostgreSQL and MySQL parameters on RDS.
- Maintain PostgreSQL health: autovacuum, indexes and transactions.

<!-- concept -->

Defaults are safe guesses, not tuned settings. Memory parameters decide how much of the data stays cached; logging parameters decide what you can see; and in PostgreSQL, autovacuum decides whether dead rows are cleaned up before tables bloat.

Many PostgreSQL problems come from things that hold back cleanup: long-running or idle transactions, abandoned replication slots, and unused indexes that slow every write. Checking for them regularly is part of operating the engine.

<!-- example -->

```sql
-- sessions holding back vacuum and locks
SELECT pid, state, now() - xact_start AS age, left(query, 60)
FROM pg_stat_activity
WHERE xact_start < now() - interval '15 minutes'
ORDER BY xact_start;
```

#### How do you tune PostgreSQL on RDS?

Adjust parameters in a custom parameter group (`shared_buffers`, `work_mem`, `maintenance_work_mem`, `effective_cache_size`, autovacuum settings, `max_connections`), keep statistics fresh, add appropriate indexes, monitor bloat and long-running transactions, and use `pg_stat_statements`.

#### How do you tune MySQL on RDS?

Size `innodb_buffer_pool_size` (default is about 75% of memory), review `max_connections`, use proper indexes and query plans, monitor the slow query log, and avoid long transactions that grow undo logs.

#### Why does autovacuum matter on RDS PostgreSQL?

PostgreSQL's MVCC leaves dead tuples after updates and deletes; autovacuum reclaims them and prevents transaction ID wraparound. If it falls behind, tables bloat and, in the worst case, the database stops accepting writes to prevent wraparound. Tune it for large, busy tables.

#### How do you find unused indexes in PostgreSQL on RDS?

Query `pg_stat_user_indexes` for indexes with `idx_scan = 0` over a long period (excluding constraints), and drop them after checking, since they cost write performance and storage.

#### How do you identify long-running transactions in PostgreSQL?

Query `pg_stat_activity` for sessions with old `xact_start`, especially `idle in transaction`; they block vacuum and cause bloat. Set `idle_in_transaction_session_timeout` to protect the database.

#### Disk usage on RDS PostgreSQL keeps growing although the data doesn't. Why?

Possible causes: an inactive logical replication slot retaining WAL, table and index bloat from autovacuum falling behind, large temporary files from heavy queries, or long logs retention. Check `pg_replication_slots`, bloat estimates, `TransactionLogsDiskUsage` and log settings.

<!-- challenge -->

A frequently updated PostgreSQL table grew from 5 GB to 60 GB though row count is stable. What do you check and change?

<!-- solution -->

Bloat from dead tuples: check `n_dead_tup` and autovacuum activity, look for long transactions or inactive replication slots blocking cleanup, tune autovacuum for that table (lower scale factor), and rebuild it once (for example `pg_repack`).

<!-- takeaways -->

- Tune memory and logging parameters in custom groups.
- Autovacuum must keep up with updates and deletes.
- Long transactions and old slots block cleanup.

### Scaling

<!-- unit: Scaling up and out -->

<!-- goals -->

- Scale RDS vertically and scale reads horizontally.
- Recognize when writes need a different design.

<!-- concept -->

Relational databases scale reads more easily than writes. Reads can spread across replicas and caches; writes all go through one primary. So the first step for write pressure is a bigger instance, then making writes cheaper, and only then structural changes like splitting the database by domain or moving to an engine that scales writes horizontally.

Splitting is as much an organizational choice as a technical one: separate databases suit separate owners and workloads.

<!-- example -->

| Pressure | First move | Next |
|---|---|---|
| CPU from reads | Read replicas, caching | Query tuning |
| CPU from writes | Larger instance class | Batch writes, fewer indexes, split by domain |
| One huge table | Partitioning | Archive old data |

#### How do you scale an RDS instance vertically?

Modify the instance class (for example from `db.r6g.large` to `db.r6g.2xlarge`), immediately or in the maintenance window. It requires a brief outage, shortened by Multi-AZ (the standby is modified first, then failover).

#### How do you scale reads?

Add read replicas (or Aurora Replicas) and route read-only traffic to them, cache frequent reads with ElastiCache, and use Multi-AZ DB clusters' readable standbys.

#### How do you scale writes beyond a single instance?

Scale up the instance, optimize write patterns (batching, fewer indexes, partitioning), move parts of the workload to other databases (DynamoDB for key-value access), or shard the data across instances at the application level. Aurora Limitless Database (PostgreSQL) and Aurora DSQL offer managed horizontal scaling options.

#### When should you split one database into several?

When different domains or services have independent workloads, scaling needs or owners, when one workload's peaks affect others, or for the microservices principle of one database per service.

<!-- challenge -->

A database's writes doubled after a new feature, and the largest instance class is near its limit. What options remain?

<!-- solution -->

Reduce write cost (batch inserts, drop unused indexes, avoid write amplification), move the feature's data to its own database or a purpose-built store such as DynamoDB, or move to an engine with horizontal write scaling (for example Aurora Limitless).

<!-- takeaways -->

- Reads scale out; writes go through one primary.
- Scale up first, then make writes cheaper.
- Split databases along domains and owners.

<!-- unit: Hidden limits and relief -->

<!-- goals -->

- Recognize limits from burstable CPU and instance I/O caps.
- Relieve pressure with caching, partitioning and storage changes.

<!-- concept -->

Some slowdowns come from limits that aren't obvious. Burstable instances run fast until their CPU credits run out. Each instance class caps how much I/O it can push, so storage with more IOPS than the class allows gives no benefit.

Other relief doesn't touch the instance at all: caches absorb repeated reads, and partitioning large tables lets queries and maintenance work on smaller pieces.

<!-- example -->

```sql
-- PostgreSQL declarative partitioning by month
CREATE TABLE events (id bigint, created_at timestamptz NOT NULL, payload jsonb)
PARTITION BY RANGE (created_at);
CREATE TABLE events_2026_10 PARTITION OF events
  FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
```

#### How do burstable instances behave under sustained load?

`db.t*` instances accumulate CPU credits when idle and spend them under load; with sustained high CPU, they exhaust credits and either throttle (standard mode) or bill extra (unlimited mode). They're unsuited for steady production workloads.

#### How do you scale storage performance without changing the instance?

With gp3, raise IOPS and throughput independently; with io1/io2, raise provisioned IOPS; check that the instance class's EBS bandwidth isn't the bottleneck.

#### What instance limits can cap I/O performance?

Each instance class has maximum EBS bandwidth and IOPS; a small class can't use very high provisioned IOPS. Choose a class whose limits match the storage configuration.

#### How does caching help an RDS database?

ElastiCache (Redis or Memcached) or application caches serve repeated reads (sessions, product catalogs, computed results) from memory, reducing load and latency on the database. Cache invalidation strategy is the hard part.

#### What is table partitioning and does it help on RDS?

Splitting large tables into partitions (PostgreSQL declarative partitioning, MySQL partitioning) by range or list, which speeds up queries filtering on the partition key and makes archiving old data cheap (drop a partition instead of deleting rows).

<!-- challenge -->

A `db.t3.medium` runs fine for weeks, then becomes very slow every day from 14:00. CPU shows 20%. What is happening?

<!-- solution -->

The instance has used up its CPU credits and is throttled to its baseline, which is about 20% for this class. Move to a non-burstable class (for example `db.m7g`) or enable unlimited mode, if the sustained load is expected.

<!-- takeaways -->

- Burstable classes throttle when credits run out.
- Instance classes cap I/O regardless of storage.
- Caches and partitioning relieve load without bigger instances.

### Cost

<!-- unit: What RDS costs -->

<!-- goals -->

- Identify the cost drivers of an RDS deployment.
- Account for Multi-AZ, backups and data transfer.

<!-- concept -->

An RDS bill has a few lines: instance hours, storage and its performance, backups beyond the free allowance, and data transfer. Availability choices multiply the compute line: Multi-AZ runs a second instance, and every replica is another instance.

Data transfer is easy to miss. Replication within Multi-AZ is free, but applications talking to a database in another AZ pay for cross-AZ traffic.

<!-- example -->

```text
db.r7g.large single-AZ        ~ 1 × instance price
db.r7g.large Multi-AZ         ~ 2 × instance price
+ 2 read replicas             ~ 4 × instance price
+ gp3 storage, extra IOPS, backups beyond DB size, cross-AZ app traffic
```

#### What drives RDS costs?

Instance hours (by class, Multi-AZ doubles the compute), storage (by type and size, plus provisioned IOPS), backup storage beyond the free amount, data transfer out and across AZs or regions, Extended Support fees, and features like RDS Proxy and Database Insights advanced mode.

#### How much does Multi-AZ cost?

Roughly double the instance cost, because a standby instance runs in another AZ, plus replicated storage. It's usually justified for production; non-production environments often run single-AZ.

#### What does backup storage cost?

Backup storage up to the size of the provisioned database storage in a region is included; beyond that, and for manual snapshots kept long, you pay per GB-month. Old manual snapshots are a common hidden cost.

#### How do cross-AZ data transfer costs affect RDS?

Multi-AZ replication traffic isn't charged, but application traffic between an instance in one AZ and clients in another AZ, and cross-region replication, incur data transfer charges.

<!-- challenge -->

The RDS bill shows high backup storage costs for a 500 GB database. What are likely causes?

<!-- solution -->

Long retention with many changes (logs and daily snapshots add up), many manual snapshots never deleted, and copies kept in other Regions. Review retention, delete obsolete manual snapshots, and move long-term copies to AWS Backup with lifecycle rules.

<!-- takeaways -->

- Compute, storage, backups and transfer drive cost.
- Multi-AZ roughly doubles compute.
- Cross-AZ application traffic is billed.

<!-- unit: Saving on RDS -->

<!-- goals -->

- Right-size instances and commit with Reserved Instances.
- Cut costs for development and idle databases.

<!-- concept -->

Savings come from three moves: run the right size, pay less for what runs all the time, and stop paying for what doesn't need to run. Metrics over several weeks show oversized instances; Reserved Instances discount steady production instances; Graviton classes cost less for the same work.

Development databases are the easy win: smaller, single-AZ, stopped outside working hours, or replaced by serverless capacity.

<!-- example -->

| Database | Change | Effect |
|---|---|---|
| Prod, 24/7, steady | 3-year Reserved Instance, Graviton | Large discount |
| Prod, CPU 10% for months | One size smaller | Half the compute |
| Dev | Single-AZ, stop nights and weekends | ~70% less |

#### How do you reduce RDS costs?

Right-size instances using metrics, use Graviton classes, buy Reserved Instances for steady workloads, use gp3 instead of over-provisioned io1, stop non-production instances at night, clean old snapshots, use Aurora Serverless v2 or I/O-Optimized where they fit, and offload reads to caches.

#### What are Reserved Instances for RDS?

A one- or three-year commitment to an instance class family in a region in exchange for a significant discount over on-demand pricing, with size flexibility within a family for most engines.

#### How do you find idle or oversized RDS instances?

CloudWatch metrics (CPU, connections, IOPS) over weeks, AWS Compute Optimizer recommendations for RDS, Trusted Advisor checks for idle instances, and cost reports by tag.

#### How can you save on development databases?

Use small or burstable instances, single-AZ, schedule stop/start outside working hours, use Aurora Serverless v2 with a low minimum, restore from shared snapshots rather than keeping many copies, and delete unused environments.

<!-- challenge -->

Ten dev databases run Multi-AZ 24/7 on the same class as production. Estimate the main savings levers.

<!-- solution -->

Switch them to single-AZ (about half), smaller or burstable classes, and schedule stop/start for working hours only (about 70% less time). Together, savings above 80% are realistic.

<!-- takeaways -->

- Right-size from weeks of metrics.
- Reserve steady instances; prefer Graviton.
- Dev databases: small, single-AZ, scheduled.

<!-- stage: Engines and features -->

### Aurora

<!-- unit: Aurora architecture -->

<!-- goals -->

- Explain how Aurora's shared storage changes availability.
- Describe clusters, failover tiers and backups.

<!-- concept -->

Aurora separates compute from storage. Instances don't own disks; they share a cluster volume that stores six copies across three AZs and heals itself. Replicas read the same storage, so they lag milliseconds and can take over without copying data.

Because storage handles durability, failover is faster than classic Multi-AZ, backups run continuously without affecting performance, and you decide which replica is promoted first with failover tiers.

<!-- example -->

```text
writer (AZ a)   reader tier-0 (AZ b)   reader tier-1 (AZ c)
      │                 │                     │
      └──────── shared cluster volume: 6 copies across 3 AZs ────────┘
```

#### What is Amazon Aurora?

A MySQL- and PostgreSQL-compatible relational database built for the cloud, with a distributed, fault-tolerant storage layer shared by the writer and replicas. It offers higher throughput than standard engines, faster failover and storage that grows automatically.

#### How does Aurora storage work?

Data is stored in a cluster volume replicated six ways across three Availability Zones in 10 GB segments. Writes need four of six copies and reads three of six, so the cluster tolerates losing an AZ plus another copy. Storage scales automatically up to 128 TiB.

#### What is an Aurora cluster?

One writer (primary) instance and up to 15 Aurora Replicas sharing the same cluster volume, with a cluster endpoint (writer), a reader endpoint (load-balanced across replicas) and optional custom endpoints for subsets of instances.

#### How is Aurora failover different from RDS Multi-AZ?

An Aurora Replica can be promoted because it shares the same storage, so there's no data to catch up and failover is typically around 30 seconds or less. Replica lag is usually in milliseconds.

#### How does Aurora handle backups?

Continuously and incrementally to S3 with no performance impact, with point-in-time recovery within the retention period (1–35 days); snapshots are cluster-level.

#### What is Aurora's failover priority (tier)?

A setting (tier 0–15) on each replica that decides which replica is promoted first during failover; equally ranked replicas are chosen by size.

<!-- challenge -->

An Aurora cluster has one large reader for analytics and one small reader. After a failover, the small one became the writer and production slowed. How do you prevent this?

<!-- solution -->

Set failover tiers: give a reader sized like the writer tier 0 so it's promoted first, and put the analytics or small readers in lower-priority tiers.

<!-- takeaways -->

- Aurora instances share a six-way replicated volume.
- Replicas lag milliseconds and fail over quickly.
- Failover tiers decide which replica becomes writer.

<!-- unit: Endpoints and read scaling -->

<!-- goals -->

- Route traffic with cluster, reader and custom endpoints.
- Speed up reads with parallel query and Optimized Reads.

<!-- concept -->

An Aurora cluster exposes several endpoints. The cluster endpoint follows the writer; the reader endpoint spreads new connections across replicas; custom endpoints target chosen instances, for example large readers for reporting.

Balancing happens per connection through DNS, not per query, so long-lived pools can stick to one replica. Features like parallel query and Optimized Reads push some workloads further than plain replicas.

<!-- example -->

```bash
aws rds create-db-cluster-endpoint --db-cluster-identifier orders-aurora \
  --db-cluster-endpoint-identifier reporting --endpoint-type READER \
  --static-members orders-reader-xl-1 orders-reader-xl-2
```

#### What are Aurora custom endpoints?

Endpoints that point to a chosen subset of instances in a cluster, for example larger replicas for analytics queries and smaller ones for application reads.

#### What is the Aurora reader endpoint's limitation?

It load-balances new connections across replicas via DNS, not individual queries; long-lived connections stay on one replica, so load can become uneven. Connection pools with periodic recycling or proxies help.

#### What is Aurora parallel query?

An Aurora MySQL feature that pushes parts of analytic queries (filters, aggregations) down to the storage layer across thousands of nodes, speeding up some analytical queries on large tables without a separate warehouse.

#### What are Aurora Optimized Reads?

A feature on instances with local NVMe storage that uses that storage as a tiered cache and for temporary objects, improving latency for read-heavy workloads whose data exceeds memory and for queries with large temporary tables.

<!-- challenge -->

Three replicas exist, but one receives almost all read traffic. The app uses a connection pool opened at startup. Why?

<!-- solution -->

The reader endpoint balances at connection time through DNS, so the pool's connections landed mostly on one replica and stay there. Recycle connections periodically, use a driver wrapper that balances across readers, or use custom endpoints.

<!-- takeaways -->

- Cluster, reader and custom endpoints route traffic.
- Reader balancing is per connection, not per query.
- Parallel query and Optimized Reads help specific workloads.

<!-- unit: Capacity and storage options -->

<!-- goals -->

- Choose between provisioned, Serverless v2 and mixed clusters.
- Pick Standard or I/O-Optimized storage, and know Limitless and DSQL.

<!-- concept -->

Aurora offers several ways to pay for capacity. Provisioned instances fit steady load; Serverless v2 scales capacity in small steps with demand, and both can be mixed in one cluster. Storage billing has two modes: pay per I/O, or pay more for storage with no I/O charges, which wins for I/O-heavy workloads.

For write scaling beyond one instance, Limitless shards PostgreSQL tables, and DSQL offers a distributed, serverless SQL database across Regions.

<!-- example -->

| Workload | Choice |
|---|---|
| Steady OLTP, 24/7 | Provisioned |
| Spiky or dev/test | Serverless v2 |
| I/O cost > ~25% of the bill | I/O-Optimized |
| Writes beyond one instance | Limitless Database |

#### What is Aurora Serverless v2?

A capacity mode where Aurora instances scale capacity automatically in fine-grained Aurora Capacity Units (ACUs) according to load, within a minimum and maximum, and can scale down to zero for some configurations. It suits variable or unpredictable workloads.

#### Can Aurora Serverless v2 and provisioned instances be mixed?

Yes. A cluster can have a provisioned writer and Serverless v2 readers (or the reverse), which is useful for variable read traffic.

#### What are Aurora Standard and Aurora I/O-Optimized?

Two storage configurations: Standard bills I/O requests separately (cheaper for low I/O), I/O-Optimized includes I/O in a higher storage and instance price (cheaper when I/O exceeds about a quarter of the database cost).

#### What is Aurora Limitless Database?

A capability of Aurora PostgreSQL that scales writes horizontally by sharding tables across multiple instances behind a single endpoint, for workloads beyond one writer's capacity.

#### What is Aurora DSQL?

A serverless, distributed SQL database with PostgreSQL compatibility designed for active-active multi-region applications, scaling reads and writes horizontally with strong consistency. It differs from standard Aurora and has some PostgreSQL feature limitations.

<!-- challenge -->

An Aurora cluster's bill is 60% I/O charges. What do you change, and how do you confirm the benefit?

<!-- solution -->

Switch the cluster to Aurora I/O-Optimized, which removes per-I/O charges for a higher instance and storage price. Compare the last months' I/O, instance and storage costs with I/O-Optimized pricing before switching; it pays off when I/O dominates.

<!-- takeaways -->

- Provisioned for steady load; Serverless v2 for variable load.
- I/O-Optimized wins when I/O dominates the bill.
- Limitless and DSQL address write scaling and multi-Region.

<!-- unit: Global databases, cloning and Backtrack -->

<!-- goals -->

- Use Aurora Global Database for cross-Region reads and DR.
- Create fast clones and rewind with Backtrack.

<!-- concept -->

Aurora's storage layer makes a few things cheap that are expensive elsewhere. Global Database replicates at the storage level to other Regions with about a second of lag, so a remote Region can serve reads and take over in a disaster.

Cloning creates a new cluster that shares pages with the source until they change, so a full copy appears in minutes and costs little. Backtrack, for Aurora MySQL, rewinds a cluster in place to an earlier time.

<!-- example -->

```bash
aws rds restore-db-cluster-to-point-in-time --source-db-cluster-identifier orders-aurora \
  --db-cluster-identifier orders-clone-qa --restore-type copy-on-write --use-latest-restorable-time
```

#### What is Aurora Global Database?

A configuration with a primary region and up to several secondary regions, replicated at the storage level with typically under one second of lag. Secondaries serve local reads and can be promoted in a regional outage (managed failover or switchover).

#### What is Aurora fast cloning?

Creating a new cluster that shares the source's storage pages using copy-on-write, so the clone is created quickly and only changed pages use new storage. It's ideal for testing, analytics on a copy, or pre-production refreshes.

#### What is Aurora Backtrack?

An Aurora MySQL feature that rewinds the cluster in place to a previous point in time within a configured window, without restoring from a backup, useful for quickly undoing mistakes.

<!-- challenge -->

QA needs a full copy of a 3 TB production database every morning, but restores take hours. What do you use?

<!-- solution -->

Aurora fast cloning (copy-on-write): the clone is ready in minutes and only stores pages that change. Delete and recreate it each morning, and mask sensitive data if QA shouldn't see it.

<!-- takeaways -->

- Global Database replicates across Regions with ~1 s lag.
- Clones share storage until pages change.
- Backtrack rewinds Aurora MySQL in place.

<!-- unit: Integrations and choosing Aurora -->

<!-- goals -->

- Use zero-ETL, Babelfish and the Data API.
- Decide when Aurora is worth it over RDS.

<!-- concept -->

Aurora adds integrations that remove whole pieces of plumbing. Zero-ETL replicates data to Redshift continuously without pipelines. Babelfish lets SQL Server applications talk to PostgreSQL. The Data API runs SQL over HTTP without managing connections.

Whether to choose Aurora over standard RDS comes down to need: faster failover, many low-lag replicas, global replication, cloning or these integrations. For small, steady databases, standard RDS is often cheaper.

<!-- example -->

| Need | Aurora feature |
|---|---|
| Analytics in Redshift without ETL | Zero-ETL integration |
| Move a SQL Server app to PostgreSQL gradually | Babelfish |
| Query from Lambda without connection pools | Data API |

#### What is Aurora zero-ETL integration with Redshift?

A managed integration that replicates Aurora (and some RDS) data into Amazon Redshift in near real time without building pipelines, so analytics run on Redshift with fresh operational data.

#### What is Babelfish for Aurora PostgreSQL?

A capability that lets Aurora PostgreSQL understand SQL Server's T-SQL and TDS protocol, so applications written for SQL Server can run with fewer code changes.

#### What is the Aurora Data API?

An HTTP API to run SQL against Aurora (Serverless v2 and provisioned) without managing connections or drivers, convenient for Lambda and other serverless apps.

#### When would you choose Aurora over RDS for PostgreSQL or MySQL?

When you need higher throughput, faster failover, many low-lag replicas, global replication, fast cloning, or serverless scaling. Standard RDS can be cheaper for small or steady workloads and supports some engine features or versions earlier.

<!-- challenge -->

A team runs a 50 GB PostgreSQL database with light traffic and asks to move to Aurora "because it's better". What do you ask before agreeing?

<!-- solution -->

What problem it solves: failover time, replicas, global reads, cloning or integrations. If none matter, standard RDS PostgreSQL is likely cheaper and simpler; otherwise compare costs including I/O.

<!-- takeaways -->

- Zero-ETL feeds Redshift without pipelines.
- Babelfish and the Data API ease integration.
- Choose Aurora for specific needs, not by default.

### Engines and features

<!-- unit: PostgreSQL extensions -->

<!-- goals -->

- Use common PostgreSQL extensions on RDS.
- Load from S3, schedule jobs and replicate tables logically.

<!-- concept -->

PostgreSQL's extensions turn it into a platform: query statistics, geospatial data, vector search, scheduled jobs, and direct import from S3. RDS supports a curated list, which covers most needs without OS access.

Logical replication is the other building block: it streams changes for chosen tables to another database, which underlies upgrades, migrations and CDC.

<!-- example -->

```sql
CREATE EXTENSION IF NOT EXISTS aws_s3 CASCADE;
SELECT aws_s3.table_import_from_s3('staging.orders', '', '(format csv, header true)',
       aws_commons.create_s3_uri('landing-bucket', 'orders/2026-10-17.csv', 'eu-west-1'));
CREATE EXTENSION IF NOT EXISTS pg_cron;
SELECT cron.schedule('refresh-mv', '0 * * * *', 'REFRESH MATERIALIZED VIEW CONCURRENTLY marts.sales_hourly');
```

#### What PostgreSQL extensions are useful on RDS?

`pg_stat_statements` (query stats), `PostGIS` (geospatial), `pgvector` (vector search), `pg_partman` (partition management), `pg_cron` (scheduled jobs), `aws_s3` (import/export with S3), `pgaudit`, `pg_repack` and `postgres_fdw`. Only supported extensions can be installed.

#### How do you load data from S3 into RDS PostgreSQL?

With the `aws_s3` extension: `SELECT aws_s3.table_import_from_s3('table', 'col1,col2', '(format csv, header true)', aws_commons.create_s3_uri('bucket', 'key.csv', 'eu-west-1'));`, with an IAM role attached to the instance.

#### How do you use `pgvector` on RDS PostgreSQL?

Install the extension, create `vector` columns for embeddings, and index them with HNSW or IVFFlat indexes for similarity search, which supports retrieval-augmented generation without a separate vector database.

#### How do you schedule jobs inside RDS PostgreSQL?

With `pg_cron` for SQL jobs inside the database, or externally with EventBridge Scheduler, Lambda or an orchestrator. Heavy batch work is often better outside the OLTP database.

#### What is logical replication used for on RDS PostgreSQL?

Replicating selected tables to another PostgreSQL database (for upgrades, migrations, splitting databases or feeding analytics), CDC to external systems, and Blue/Green deployments.

<!-- challenge -->

An app needs similarity search over 2 million product embeddings and already uses RDS PostgreSQL. Do you need a separate vector database?

<!-- solution -->

Probably not at that size: install `pgvector`, store embeddings in a `vector` column, and create an HNSW index. Keep a separate vector store in mind only if latency or scale requirements outgrow PostgreSQL.

<!-- takeaways -->

- Extensions add stats, geospatial, vectors and scheduling.
- `aws_s3` loads files directly from S3.
- Logical replication streams selected tables.

<!-- unit: Upgrades and safe changes -->

<!-- goals -->

- Plan minor and major engine upgrades.
- Use Blue/Green deployments and online schema changes.

<!-- concept -->

Engines age: versions reach end of support, and staying on them costs Extended Support fees or risks forced upgrades. Minor versions can apply automatically; major versions need testing because extensions, parameters and query plans change.

Blue/Green deployments make upgrades and big changes safer: a synchronized copy is changed and tested while production runs, and switchover takes about a minute. Schema changes on large tables need online-friendly operations for the same reason.

<!-- example -->

```bash
aws rds create-blue-green-deployment --blue-green-deployment-name orders-pg16 \
  --source arn:aws:rds:eu-west-1:123456789012:db:orders-prod \
  --target-engine-version 16.4 --target-db-parameter-group-name pg16-orders
# test green, then:
aws rds switchover-blue-green-deployment --blue-green-deployment-identifier bgd-abc123
```

#### What is a Blue/Green deployment?

A feature (MySQL, MariaDB, PostgreSQL, Aurora) that creates a staging copy (green) synchronized with production (blue) by logical replication, lets you upgrade or change it, then switches over in about a minute with guardrails, keeping the same endpoints.

#### How do you upgrade the major version of an RDS engine?

Test the upgrade on a snapshot restore, check extension and parameter compatibility, then either upgrade in place (downtime) or use Blue/Green deployments for minimal downtime. Take a snapshot before upgrading.

#### What are minor version auto-upgrades?

An option where RDS applies minor engine versions (bug and security fixes) automatically during the maintenance window. Most teams enable it, sometimes after testing in lower environments.

#### What is RDS Extended Support?

A paid offering that keeps receiving critical patches for major engine versions after their community end of life, giving extra time to upgrade. Instances on such versions are enrolled automatically unless upgraded.

#### How do you run schema migrations safely on large tables?

Use online-friendly operations (instant DDL in MySQL 8, `CREATE INDEX CONCURRENTLY` in PostgreSQL), tools like `gh-ost` or `pt-online-schema-change` for MySQL, Blue/Green deployments, and test migration time on a clone.

#### Your team must upgrade from PostgreSQL 13 to 16 with minimal downtime. How do you plan it?

Check extension and parameter compatibility, test the upgrade on a restored snapshot and run application tests, then use a Blue/Green deployment: create the green environment, upgrade it, let it sync, validate, and switch over in a short window, keeping the blue environment as rollback until confident.

<!-- challenge -->

Adding an index to a 400 GB PostgreSQL table locked writes for 20 minutes in production. How should it have been done?

<!-- solution -->

With `CREATE INDEX CONCURRENTLY`, which builds without blocking writes (slower, and it can't run inside a transaction). Test duration on a clone first and run it at low traffic.

<!-- takeaways -->

- Plan major upgrades; test on a restored copy.
- Blue/Green switches over in about a minute.
- Use online DDL for large tables.

<!-- unit: Commercial engines and MySQL -->

<!-- goals -->

- Know the limits and licensing of SQL Server and Oracle on RDS.
- Use modern MySQL features for data work.

<!-- concept -->

Commercial engines on RDS come with two extra considerations. Some privileges and features are restricted because AWS manages the server, so certain admin tasks use RDS-specific procedures. Licensing can be included in the hourly price or brought from existing agreements, which changes cost dramatically.

MySQL 8 closed many gaps for analytical SQL, with window functions, CTEs and JSON support, which matters when data teams query it directly.

<!-- example -->

```sql
-- MySQL 8: latest order per customer with a window function
SELECT * FROM (
  SELECT o.*, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC) AS rn
  FROM orders o
) t WHERE rn = 1;
```

#### What are the restrictions of SQL Server on RDS?

No `sysadmin` role, limited features in some editions, specific procedures for native backup and restore (via S3), limits on the number of databases per instance, and storage size limits; RDS Custom for SQL Server lifts some of them.

#### What licensing options exist for Oracle and SQL Server on RDS?

License Included (license cost in the hourly price) or Bring Your Own License for Oracle; SQL Server is generally License Included, with edition choices (Express, Web, Standard, Enterprise).

#### What are the benefits of MySQL 8.0+ features on RDS for data work?

Window functions, CTEs (including recursive), JSON functions, invisible indexes, instant `ADD COLUMN` for many changes and better optimizer statistics, which make analytics queries and schema changes easier.

<!-- challenge -->

A team migrating SQL Server to RDS relies on `sysadmin` for maintenance scripts. What do you tell them?

<!-- solution -->

RDS doesn't grant `sysadmin`. Rewrite scripts to use the master user's privileges and RDS stored procedures (for example `rds_backup_database` for native backups), or consider RDS Custom if OS-level control is essential.

<!-- takeaways -->

- Commercial engines have restricted privileges on RDS.
- License Included versus BYOL changes cost.
- MySQL 8 adds window functions, CTEs and JSON.

<!-- stage: Data engineering on RDS -->

### SQL and database design on RDS

<!-- unit: Keys and normalization -->

<!-- goals -->

- Choose primary keys for OLTP tables.
- Explain why normalization matters for transactional data.

<!-- concept -->

Transactional databases are optimized for many small, correct changes. Normalization supports that by storing each fact once, so an update touches one row. Primary keys give every row a stable identity, which joins, replication and CDC tools depend on.

Key design is a trade-off: surrogate keys are stable and compact, natural keys carry meaning, and integers index better than random UUIDs, while UUIDs are easier to generate anywhere.

<!-- example -->

```sql
CREATE TABLE customers (
  customer_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,   -- surrogate
  email       text NOT NULL UNIQUE,                               -- natural key, enforced
  created_at  timestamptz NOT NULL DEFAULT now(),
  updated_at  timestamptz NOT NULL DEFAULT now()
);
```

#### Why do primary keys matter so much on RDS tables?

They guarantee row identity, are required by many replication and CDC tools to apply updates and deletes, and in InnoDB define the physical clustering of the table. Every table should have one.

#### Should you use natural keys or surrogate keys?

Surrogate keys (auto-increment, identity or UUIDs) are stable and compact; natural keys (email, national ID) can change and are often sensitive. Use surrogate primary keys with unique constraints on natural keys.

#### UUIDs or integers for primary keys?

Integers are smaller and keep inserts sequential (good for B-tree indexes and InnoDB clustering). Random UUIDs scatter inserts and bloat indexes; time-ordered UUIDs (UUIDv7) keep uniqueness across systems with better locality.

#### What is normalization, and why does it matter for OLTP?

Organizing tables so each fact is stored once (normal forms), which avoids update anomalies and keeps transactions small and consistent. OLTP databases are usually normalized to third normal form; analytics denormalize later.

<!-- challenge -->

A legacy table has no primary key, and DMS CDC can't apply updates to the target. What do you do?

<!-- solution -->

Add a primary key (an existing unique column, or a new identity column), then restart the task. Without a key, CDC tools can't identify which row an update or delete refers to.

<!-- takeaways -->

- Every table needs a primary key.
- Surrogate keys are stable; enforce natural keys with unique constraints.
- Normalization keeps OLTP updates small and consistent.

<!-- unit: Indexes and concurrency -->

<!-- goals -->

- Design indexes, including composite ones, and weigh their cost.
- Understand isolation levels and avoid deadlocks.

<!-- concept -->

Indexes trade write cost and storage for faster reads. A composite index helps queries that filter on its leading columns, so column order follows how queries filter. Too many indexes slow every insert and update.

Concurrency adds another layer: isolation levels decide what a transaction sees of others' changes, and conflicting lock orders cause deadlocks. Short transactions and consistent access order prevent most problems.

<!-- example -->

```sql
CREATE INDEX idx_orders_customer_created ON orders (customer_id, created_at);
-- uses the index:      WHERE customer_id = 42 AND created_at >= '2026-10-01'
-- uses it partially:   WHERE customer_id = 42
-- cannot use it well:  WHERE created_at >= '2026-10-01'
```

#### How do indexes speed up queries, and what do they cost?

B-tree indexes let the database find rows by key without scanning the table and help sorting and joins; each index slows writes and uses storage, so index the columns used in frequent filters, joins and sorts, not everything.

#### What is a composite index, and how does column order matter?

An index on several columns used left to right: an index on `(customer_id, created_at)` helps filters on `customer_id` and on `customer_id` with a range on `created_at`, but not on `created_at` alone.

#### What isolation levels do RDS engines use by default?

PostgreSQL defaults to read committed; MySQL InnoDB defaults to repeatable read. Understanding them matters for consistency of extracts and concurrency behavior.

#### How do you avoid deadlocks?

Access tables and rows in a consistent order, keep transactions short, index foreign keys and filter columns to lock fewer rows, and retry transactions that fail with deadlock errors.

<!-- challenge -->

Two jobs update the same accounts table and occasionally deadlock. One updates in ID order, the other in name order. What do you change?

<!-- solution -->

Make both update rows in the same order (for example by primary key), keep transactions short, and add retry logic for the rare deadlock that still occurs.

<!-- takeaways -->

- Indexes speed reads and slow writes.
- Composite index order follows query filters.
- Consistent lock order and short transactions avoid deadlocks.

<!-- unit: Pipeline-friendly tables -->

<!-- goals -->

- Design tables that support incremental extraction and audit.
- Make deletions visible to downstream systems.

<!-- concept -->

Tables are read by more than the application. Data pipelines need to know what changed since last time, and audit needs to know when. Timestamp columns maintained on every change make incremental extraction possible.

Deletes are the hard case: a deleted row simply disappears, and a pipeline reading changes by timestamp never sees it. Soft deletes, or CDC, make deletions visible.

<!-- example -->

```sql
ALTER TABLE orders ADD COLUMN deleted_at timestamptz;
-- trigger keeps updated_at current on every UPDATE
CREATE TRIGGER orders_touch BEFORE UPDATE ON orders
FOR EACH ROW EXECUTE FUNCTION set_updated_at();
```

#### What are soft deletes, and why do they matter for data pipelines?

Marking rows as deleted (`deleted_at`) instead of removing them. They make deletions visible to incremental extraction, but applications and pipelines must filter them consistently.

#### Why add `created_at` and `updated_at` columns to every table?

They support auditing, incremental extraction, debugging and data quality checks; `updated_at` should be maintained by the application or a trigger on every change.

<!-- challenge -->

An incremental pipeline uses `updated_at` to copy changes, but the warehouse still shows orders that were deleted in the app. Why, and what are two fixes?

<!-- solution -->

Hard deletes leave no row to extract. Either use soft deletes (`deleted_at`) so deletions are updates, or capture changes with CDC (DMS or Debezium) to receive delete events.

<!-- takeaways -->

- `created_at` and `updated_at` enable incremental loads.
- Hard deletes are invisible to timestamp extraction.
- Soft deletes or CDC propagate deletions.

### Migration and data engineering

<!-- unit: Migrating into RDS -->

<!-- goals -->

- Choose a migration method for same and different engines.
- Use DMS and Schema Conversion, and validate the result.

<!-- concept -->

How you migrate depends on two questions: is the engine the same, and how much downtime is acceptable? Same engine and a maintenance window allow native dump and restore. Minimal downtime needs continuous replication: a full load followed by change capture until cutover.

Changing engines adds schema and code conversion, which tools only partly automate. Every migration ends with validation, because "it ran" isn't the same as "the data matches".

<!-- example -->

```text
1. Schema Conversion: Oracle schema → PostgreSQL (review stored procedures by hand)
2. DMS full load (parallel by table partitions) + CDC
3. DMS data validation, row counts, checksums per table
4. Cutover: stop writes, wait for CDC lag 0, switch connection strings
```

#### How do you migrate a database to RDS?

For the same engine: native dump and restore (`pg_dump`/`pg_restore`, `mysqldump`, SQL Server backup to S3 and restore), or replication from the source to RDS for minimal downtime. For different engines or continuous replication: AWS DMS, with the Schema Conversion Tool (or DMS Schema Conversion) for schema translation.

#### What is AWS DMS?

Database Migration Service: replicates data from a source database to a target (another database, S3, Redshift, Kinesis and others) with a full load and ongoing change data capture (CDC), running on replication instances or DMS Serverless.

#### What is DMS Schema Conversion?

A managed feature in DMS (successor to the desktop Schema Conversion Tool for many cases) that assesses and converts schemas and code between engines, reporting items that need manual work.

#### How does DMS handle large tables during full load?

With parallel load by partitions or ranges of a column, LOB settings for large objects, and table mappings to select and transform tables; very large migrations may combine native bulk export with DMS CDC from a known position.

#### How do you validate a migration?

DMS data validation (row-by-row comparison), row counts and checksums per table, comparison of aggregates (sums, min/max by key ranges), application tests against the target, and a period of parallel running.

#### You need to migrate a 2 TB Oracle database to Aurora PostgreSQL with minimal downtime. How?

Assess with the Schema Conversion Tool, convert schema and code (PL/SQL to PL/pgSQL), run DMS full load plus CDC to keep the target in sync, validate data (DMS validation, row counts, checksums) and application behavior, then cut over during a short window by stopping writes, letting CDC catch up and switching connections.

<!-- challenge -->

Validation shows small numeric differences between Oracle and PostgreSQL for a few columns. What is the likely cause?

<!-- solution -->

Type mapping: Oracle `NUMBER` without precision mapped to a floating-point type, or rounding differences in converted functions. Map those columns to `numeric` with the right precision and re-run the load for them.

<!-- takeaways -->

- Same engine: native tools; minimal downtime: replication.
- Engine changes need schema and code conversion.
- Always validate data after migrating.

<!-- unit: Change data capture -->

<!-- goals -->

- Enable CDC on RDS MySQL and PostgreSQL.
- Avoid the common pitfalls of CDC, including replication slots.

<!-- concept -->

CDC reads the database's own change log, which captures every insert, update and delete without querying tables. Each engine exposes it differently: MySQL through the binlog, PostgreSQL through logical replication slots. Both need configuration and enough log retention.

The risk is the dependency it creates. If a consumer stops, PostgreSQL keeps WAL for its slot until disk fills, and missing keys or huge transactions break pipelines. CDC needs monitoring like any production system.

<!-- example -->

```text
MySQL:      binlog_format = ROW, binlog_row_image = FULL,
            CALL mysql.rds_set_configuration('binlog retention hours', 24);
PostgreSQL: rds.logical_replication = 1, then a slot per consumer
            alert on: pg_replication_slots.active = false, retained WAL size
```

#### How do you capture changes (CDC) from RDS MySQL?

Enable binary logging with `binlog_format = ROW` (and full row images), keep enough binlog retention (`mysql.rds_set_configuration('binlog retention hours', 24)`), and read changes with DMS, Debezium or a zero-ETL integration.

#### How do you capture changes from RDS PostgreSQL?

Enable logical replication (`rds.logical_replication = 1`), create a replication slot and publication, and consume with DMS, Debezium (pgoutput plugin) or zero-ETL. Monitor replication slots: an unconsumed slot retains WAL and can fill the disk.

#### Why are replication slots dangerous on PostgreSQL?

A slot makes PostgreSQL keep WAL until the consumer confirms it. If a CDC consumer stops, WAL accumulates (`TransactionLogsDiskUsage` grows) until storage fills and the database stops. Alert on slot lag and drop abandoned slots.

#### What are the common pitfalls of CDC from relational databases?

Missing primary keys (updates can't be matched), insufficient log retention, large transactions that lag, schema changes not propagated, data type mismatches (timestamps, decimals), and deletes not handled downstream.

#### How do you send RDS changes to Kafka?

With Debezium on Kafka Connect (or Amazon MSK Connect) reading the binlog or logical replication, producing one topic per table with change events, or with DMS targeting Kinesis or MSK.

<!-- challenge -->

A Debezium connector was stopped for a week of maintenance, and the PostgreSQL disk filled up. What happened, and how do you prevent it?

<!-- solution -->

The connector's replication slot kept retaining WAL while inactive. Alert on inactive slots and retained WAL size, drop slots that are no longer needed, and, on recent PostgreSQL versions, set `max_slot_wal_keep_size` as a safety limit.

<!-- takeaways -->

- CDC reads the binlog or WAL, not the tables.
- Inactive PostgreSQL slots retain WAL until disk fills.
- Keys, retention and monitoring make CDC reliable.

<!-- unit: Extracting for analytics -->

<!-- goals -->

- Keep analytics off the production primary.
- Extract data without locks, with snapshots, replicas or exports.

<!-- concept -->

OLTP databases serve customers; analytics should not compete with them. The safest extraction reads somewhere other than the primary: a replica, a clone, or a snapshot exported to S3 as Parquet. When reading the primary is unavoidable, consistent snapshot reads avoid blocking writers.

Incremental extraction by timestamp is simple but has gaps: it misses deletes and rows whose timestamp isn't updated, and late commits can slip past the watermark.

<!-- example -->

```bash
aws rds start-export-task --export-task-identifier orders-2026-10-17 \
  --source-arn arn:aws:rds:eu-west-1:123456789012:snapshot:rds:orders-prod-2026-10-17-03-10 \
  --s3-bucket-name lake-raw --s3-prefix rds/orders/ \
  --iam-role-arn arn:aws:iam::123456789012:role/rds-export --kms-key-id alias/lake
```

#### Should you run analytics directly on the production RDS instance?

Generally no. Analytical queries compete with OLTP traffic for CPU, memory and I/O. Use a read replica for light reporting, and for heavier analytics move data to a warehouse or lakehouse through CDC, exports or zero-ETL.

#### What is the difference between OLTP and OLAP, and where does RDS fit?

OLTP handles many small transactions (inserts, updates, point lookups) with strong consistency; OLAP handles large scans and aggregations over history. RDS is built for OLTP; OLAP belongs in Redshift, Snowflake, Databricks or Athena on a data lake.

#### How do you extract large tables from RDS without hurting production?

Read from a read replica or a fresh clone/restore, export snapshots to S3 as Parquet, extract incrementally by an updated-at column or CDC instead of full extracts, run in parallel by key ranges within limits, and schedule outside peak hours.

#### How do you avoid locking production tables when extracting?

Use snapshots or replicas, read with consistent snapshot isolation without locks (PostgreSQL MVCC, InnoDB consistent reads), avoid `SELECT … FOR UPDATE` and long transactions, and paginate by key.

#### What is the snapshot export to S3 feature?

An RDS feature that exports data from a snapshot to S3 in Parquet format, partitioned by table, without impacting the running database, ready to be catalogued with Glue and queried with Athena.

#### How do you export RDS data to S3 for analytics?

Export a snapshot to S3 (RDS writes tables as Parquet files, which Athena or Glue can query), or run your own exports (the `aws_s3` extension in PostgreSQL, `SELECT INTO OUTFILE S3` in Aurora MySQL, or Glue/DMS jobs).

#### What is a watermark-based incremental extraction, and what are its risks?

Selecting rows where `updated_at` is greater than the last extracted value. It misses deletes, rows updated without changing the timestamp, and rows committed late with an older timestamp; use an overlap window and periodic reconciliation, or CDC.

<!-- challenge -->

An extraction job selects `WHERE updated_at > last_watermark` and occasionally misses rows. Name two causes and a sturdier approach.

<!-- solution -->

Transactions that commit after the watermark was taken but carry an earlier `updated_at`, and updates that don't touch `updated_at` (or hard deletes). Use an overlap window with deduplication, or switch to CDC.

<!-- takeaways -->

- Extract from replicas, clones or snapshot exports.
- Snapshot exports write Parquet to S3 without load.
- Watermarks miss deletes and late commits.

<!-- unit: Moving data in and to the lake -->

<!-- goals -->

- Read RDS from Glue and load data into RDS efficiently.
- Land RDS data in a data lake with full and incremental loads.

<!-- concept -->

Data moves both ways between RDS and the lake. Out of RDS, a full load seeds the lake and CDC keeps it current, with Glue or Spark applying changes to lake tables. Into RDS, bulk loading beats row-by-row inserts by orders of magnitude.

Glue jobs reach RDS through connections in the VPC, and parallel reads matter for large tables.

<!-- example -->

```sql
-- PostgreSQL bulk load: far faster than INSERT per row
COPY staging.products (sku, name, price) FROM STDIN WITH (FORMAT csv, HEADER true);
-- then upsert into the final table
INSERT INTO products SELECT * FROM staging.products
ON CONFLICT (sku) DO UPDATE SET name = EXCLUDED.name, price = EXCLUDED.price;
```

#### How do Glue jobs read from RDS?

Through a Glue JDBC connection in the database's VPC (with subnet and security group access), reading tables in parallel with partitioning options and storing credentials in Secrets Manager; bookmarks or a watermark column provide incremental loads.

#### How do you load data into RDS efficiently?

Use bulk loading (`COPY` in PostgreSQL, `LOAD DATA` in MySQL, the `aws_s3` extension), batch inserts, disable or defer secondary index creation for initial loads, increase `maintenance_work_mem` temporarily, and avoid row-by-row inserts over the network.

#### How do you land RDS data in a data lake?

Full loads via snapshot export to S3 or DMS full load, then incremental changes via DMS CDC to S3 (Parquet with operation columns) or zero-ETL; apply changes to Iceberg/Delta tables with `MERGE`, and catalog everything in Glue.

<!-- challenge -->

A nightly job inserts 5 million rows into RDS one at a time and takes 6 hours. What do you change?

<!-- solution -->

Bulk load: write a file and use `COPY` (or `aws_s3.table_import_from_s3` / `LOAD DATA`) into a staging table, then one set-based upsert. Drop or defer non-essential indexes during the load if needed.

<!-- takeaways -->

- Full load plus CDC keeps the lake current.
- Glue reads RDS through VPC connections.
- Bulk loads beat row-by-row inserts.

<!-- stage: Putting it together -->

### Scenarios

<!-- unit: Designing for availability and recovery -->

<!-- goals -->

- Design a production database for availability, security and recovery.
- Add a cross-Region disaster recovery plan.

<!-- concept -->

Design questions test whether you can combine the pieces. A strong answer covers placement (private subnets across AZs), availability (Multi-AZ), protection (backups with tested restores, encryption, deletion protection), access (least-privilege users, secrets), observability (metrics, logs, alarms) and growth. Then it separates high availability from disaster recovery and gives RTO and RPO for each.

<!-- example -->

| Layer | Choice |
|---|---|
| Availability | Multi-AZ DB cluster (or Aurora) |
| Protection | 14-day PITR, AWS Backup copies to another account and Region |
| Access | Private subnets, SG from app SG, Secrets Manager, RDS Proxy |
| Observability | Database Insights, alarms, event notifications |
| DR | Cross-Region replica (or Aurora Global Database), runbook |

#### Design a highly available PostgreSQL database for a production application.

RDS for PostgreSQL (or Aurora PostgreSQL) in private subnets across AZs with Multi-AZ (or a Multi-AZ DB cluster), encryption with a customer-managed KMS key, TLS enforced, RDS-managed secrets with rotation, RDS Proxy for connection pooling, automated backups with 14–35 days retention plus AWS Backup copies to another region, Database Insights, alarms on key metrics and deletion protection, all defined in infrastructure as code.

#### How do you set up a cross-region disaster recovery plan for an RDS MySQL database?

Create a cross-region read replica (or Aurora Global Database for Aurora), replicate automated backups or copy snapshots to the DR region, script promotion and DNS changes, keep application infrastructure ready in the DR region, and test failover periodically against your RPO and RTO.

<!-- challenge -->

The business sets an RTO of 1 hour and an RPO of 5 minutes for a regional disaster. Does a cross-Region read replica meet it, and what else do you need?

<!-- solution -->

Usually yes: replica lag is typically seconds and promotion takes minutes. You also need a tested runbook, infrastructure ready in the DR Region (app, secrets, DNS failover) and regular drills.

<!-- takeaways -->

- Combine placement, availability, protection, access and observability.
- State RTO and RPO for HA and DR separately.
- DR only counts if it's tested.

<!-- unit: Fresh production data for analytics -->

<!-- goals -->

- Give analysts fresh copies of production data safely.
- Balance freshness, cost, isolation and privacy.

<!-- concept -->

Analysts want production data, and production wants to be left alone. The design question is how to give them a recent copy that's isolated from customers, affordable and safe. Options range from replicas (fresh, but load the primary's replication) to daily clones or restores (isolated, a day old) to exports into the lake (cheap, query with other engines). Privacy decides whether masking is part of the copy.

<!-- example -->

| Option | Freshness | Isolation | Notes |
|---|---|---|---|
| Read replica | Seconds | Shares replication | Good for live dashboards |
| Daily Aurora clone | Daily | Full | Fast to create, pay for changes |
| Snapshot export to S3 | Daily | Full | Parquet for Athena or Spark |

#### How do you give the analytics team daily access to fresh copies of production data?

Use Aurora fast cloning or snapshot restores to create a separate copy each day (masked if needed), or export snapshots to S3 as Parquet for Athena, or set up zero-ETL to Redshift for near-real-time analytics without touching production.

<!-- challenge -->

The copy contains customer emails and phone numbers, which analysts must not see. Where in your design do you remove them?

<!-- solution -->

Mask them as part of building the copy: run a masking step on the clone before granting access, or exclude and hash those columns when exporting to the lake (with Lake Formation column permissions as a second layer).

<!-- takeaways -->

- Match freshness and isolation to the analytics need.
- Clones and exports isolate analytics from production.
- Mask personal data before analysts get access.
