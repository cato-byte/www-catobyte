## Data Architecture Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Data architecture study guide: about 200 questions](../../images/data_architecture_study_guide_title_img.png)

About 200 interview-style questions on data architecture: principles, storage and database choices, distributed systems trade-offs, modeling approaches (Inmon, Kimball, Data Vault), lakes, lakehouses and the medallion pattern, batch and streaming architectures (Lambda, Kappa), microservices and event-driven data, data mesh and data fabric, governance, security, reliability, cost, and architecture for AI. It complements the data warehousing guide, which goes deeper into dimensional modeling.

The guide follows a learning path in six stages. Each section is split into short units: learning goals, a concept explanation and a worked example, then questions (recall first, then application), a practical challenge and key takeaways. To **learn**, read each unit top to bottom. To **review**, switch to review mode or use "Skip to questions", mark answers you want to see again, and try a mixed review across sections.

<!-- QA -->
<!-- stage: Foundations -->

### Principles

<!-- unit: What data architecture is -->

<!-- goals -->

- Explain what data architecture covers and what a data architect does.
- Name the layers of a modern data platform.

<!-- concept -->

Every company already has a data architecture, designed or not: data comes from somewhere, is stored somewhere, changes shape and reaches people. Data architecture is the deliberate version of that, a blueprint of structures, standards and technology choices that lets many teams build without contradicting each other.

Engineers build pipelines inside that blueprint; architects decide its shape, weighing requirements, cost and change over years rather than sprints.

<!-- example -->

```text
sources ─► ingestion (batch, CDC, streams) ─► storage (lake, warehouse)
        ─► processing (transform, model) ─► serving (BI, APIs, ML, reverse ETL)
        across all layers: governance, security, metadata, observability
```

#### What is data architecture?

The set of decisions, models, policies and standards that define how data is collected, stored, integrated, processed, governed and consumed across an organization, and the systems that implement them.

#### What does a data architect do?

Translates business needs into data structures and platforms: chooses technologies and patterns, designs models and flows, defines standards for quality, security and governance, documents decisions, and guides teams so systems fit together and evolve without constant rework.

#### What is the difference between data architecture and data engineering?

Data architecture defines the blueprint: structures, standards, technology choices and how components fit together. Data engineering builds and operates the pipelines and platforms that implement it. In practice the roles overlap, and senior engineers make many architectural decisions.

#### What are the main layers of a modern data architecture?

Sources, ingestion (batch, CDC, streaming), storage (lake, warehouse, operational stores), processing and transformation, serving (BI, APIs, ML features, reverse ETL), plus cross-cutting orchestration, governance, security, observability and metadata.

#### How do you explain data architecture to a non-technical stakeholder?

It's the city plan for the company's data: where data comes from, where it's stored, how it flows and is cleaned, who's responsible for it, and the rules that keep it safe and trustworthy, so teams can build on it without chaos.

<!-- challenge -->

A manager asks why the company needs a data architect when it already has five data engineers. Give two answers in business terms.

<!-- solution -->

Without a shared blueprint, each engineer solves problems differently, so costs, duplicate data and conflicting numbers grow. An architect sets standards and makes the long-term technology decisions so the platform stays affordable and trustworthy as it grows.

<!-- takeaways -->

- Data architecture is the blueprint; engineering builds within it.
- Layers: sources, ingestion, storage, processing, serving.
- Governance, security and metadata cut across all layers.

<!-- unit: Requirements and models -->

<!-- goals -->

- Gather functional and non-functional requirements.
- Use conceptual, logical and physical models, and record decisions in ADRs.

<!-- concept -->

Good architecture starts from questions, not tools. Functional requirements say what data and outputs are needed; non-functional ones (freshness, volume, availability, cost, compliance) usually decide the design, because two systems producing the same report can differ a hundredfold in cost.

Models translate requirements in layers, from business entities for stakeholders to exact tables for engineers. Decision records keep the reasoning, so the next team knows why, not just what.

<!-- example -->

```markdown
# ADR-014: Use Iceberg for curated lake tables
Context: Athena, Spark and Snowflake must read the same tables.
Options: Delta, Iceberg, plain Parquet.
Decision: Iceberg (broadest multi-engine support, catalog integration).
Consequences: compaction jobs required; team training on Iceberg maintenance.
```

#### What is the difference between conceptual, logical and physical data models?

Conceptual models show business entities and relationships for stakeholders; logical models add attributes, keys and normalization without technology details; physical models implement them in a specific database with types, indexes, partitions and storage choices.

#### What are functional versus non-functional requirements in data architecture?

Functional: which data, transformations, metrics and outputs are needed. Non-functional: latency, freshness, volume, scalability, availability, durability, security, compliance, cost and maintainability, which often drive the technology choices.

#### What is an architecture decision record (ADR)?

A short document capturing a significant decision: context, options considered, decision, consequences and status. ADRs make reasoning visible and stop teams from relitigating decisions; they're stored with the code.

<!-- challenge -->

Stakeholders ask for "real-time sales dashboards". Which non-functional questions do you ask before designing anything?

<!-- solution -->

How fresh is fresh enough (seconds, minutes, hourly), how many users, which decisions change with fresher data, acceptable cost, and availability needs. The answers decide between streaming and frequent batch.

<!-- takeaways -->

- Non-functional requirements usually drive design and cost.
- Conceptual, logical and physical models serve different readers.
- ADRs preserve the reasoning behind decisions.

<!-- unit: Design principles -->

<!-- goals -->

- Apply core principles: data as a product, immutable raw data, single responsibility.
- Design for change and manage technical debt.

<!-- concept -->

A few principles make platforms last. Datasets with owners and guarantees are trusted and reused. Raw data kept unchanged lets you reprocess when logic or bugs change. Pipelines with one job each are easier to test and replace.

The thread running through them is change: requirements, sources and tools will all change. Architectures that assume this, with loose coupling, contracts and automated checks, absorb change; those that don't accumulate debt that slows every future project.

<!-- example -->

| Principle | Practice |
|---|---|
| Data as a product | Owner, schema, SLA, docs for each dataset |
| Immutable raw | Append-only landing; never edit source files |
| Single responsibility | One pipeline per source; one model per concept |
| Evolutionary | Contracts and tests as fitness functions |

#### What are good data architecture principles?

Treat data as a product with owners; design for change (loose coupling, contracts); keep one source of truth per entity; store raw data immutably and reprocess when logic changes; secure and govern by default; automate everything as code; optimize for the questions people ask; and prefer simple, managed components when they meet requirements.

#### What is "data as a product"?

Managing datasets like products: a clear owner, documented purpose and schema, quality guarantees and SLAs, discoverability, versioning, and feedback from consumers. It's a core idea of data mesh but useful in any architecture.

#### Why should raw data be immutable?

Immutable raw data lets you reprocess history when logic or bugs change, audit what sources sent, and rebuild downstream layers; mutations happen in later layers, keeping the system recoverable.

#### What is the "single responsibility" idea applied to data pipelines?

Each pipeline or model should have one clear purpose (ingest a source, conform an entity, build a metric), which makes it easier to test, own, reuse and change without side effects.

#### What is "evolutionary architecture"?

Designing systems to change incrementally with guardrails (fitness functions such as tests on latency, cost or coupling), favoring reversible decisions and small steps over big upfront designs.

#### What is technical debt in data platforms?

Shortcuts that make future change costly: undocumented pipelines, duplicated logic, hard-coded configuration, missing tests, unowned tables, quick fixes in production. It accumulates silently and shows up as incidents, slow delivery and distrust of numbers.

<!-- challenge -->

A team overwrites raw source files after cleaning them to save storage. Six months later a bug in the cleaning logic is found. What is the consequence, and the fix?

<!-- solution -->

History can't be reprocessed, because the original inputs are gone. Keep raw data immutable (cheap with storage tiers and lifecycle rules) and write cleaned data to a separate layer.

<!-- takeaways -->

- Datasets need owners and guarantees.
- Immutable raw data enables reprocessing and audit.
- Design for change; track and repay debt.

<!-- unit: Choosing technology -->

<!-- goals -->

- Decide between building and buying, and limit lock-in.
- Evaluate technologies by fit and total cost of ownership.

<!-- concept -->

Technology choices are long-term bets. Managed services trade control for speed; open formats and standard interfaces keep the option to switch later. Centralizing gives consistency, decentralizing gives speed, and most organizations need some of both.

Comparing options by license price alone misleads. Total cost includes people to run it, migrations and the cost of being stuck, so evaluations should test real workloads against explicit criteria.

<!-- example -->

| Criterion | Option A (managed) | Option B (self-hosted OSS) |
|---|---|---|
| Time to first value | Weeks | Months |
| Run cost (people) | Low | High |
| Lock-in | Medium (open formats help) | Low |
| 3-year TCO | ... | ... |

#### What does "build versus buy" mean for data platforms?

Choosing between building custom components (more control, more maintenance) and using managed services or vendors (faster, less control, recurring cost, lock-in). Most teams buy commodity capabilities (storage, warehouse, connectors) and build what differentiates them.

#### What is vendor lock-in, and how do you limit it?

Dependence on one vendor's proprietary formats or APIs that makes switching expensive. Limit it with open formats (Parquet, Iceberg, Delta), standard SQL, infrastructure as code, abstraction where it's cheap, and exit plans for critical components, accepting some lock-in where value is high.

#### What are the trade-offs between centralization and decentralization?

Centralized platforms and teams give consistency, economies of scale and strong governance but become bottlenecks. Decentralized domain ownership scales delivery and puts expertise close to data but risks inconsistency and duplicated effort; federated governance balances them.

#### How do you evaluate a new technology for the platform?

Start from requirements, compare a few options against criteria (fit, performance, cost, skills, ecosystem, support, security, lock-in), run a proof of concept on real workloads, consider total cost of ownership and exit costs, and record the decision in an ADR.

#### What is total cost of ownership (TCO)?

The full cost of a solution over time: licenses or cloud usage, infrastructure, people to build and operate it, training, migration, support and the cost of downtime, not just the price per unit of compute.

<!-- challenge -->

A team wants to self-host an open-source streaming platform because "it's free". What do you ask them to include in the comparison?

<!-- solution -->

The people cost of running it 24/7 (upgrades, scaling, on-call), infrastructure, security and support, compared with a managed service's price over three years. Include the opportunity cost of engineers not building data products.

<!-- takeaways -->

- Buy for speed, build for differentiation.
- Open formats and standards limit lock-in.
- Compare total cost of ownership, not license prices.

### Storage and databases

<!-- unit: Choosing a database -->

<!-- goals -->

- Match relational, document, key-value, wide-column and graph stores to workloads.
- Explain polyglot persistence and its cost.

<!-- concept -->

Databases differ in the questions they answer cheaply. Relational systems handle flexible queries over related data with transactions. Document stores keep self-contained, nested records together. Key-value stores answer "give me this key" at enormous scale. Wide-column stores absorb massive writes by partition. Graphs follow relationships.

Choosing by access pattern rather than habit leads to several stores in one system, which works, as long as someone owns the integration and consistency between them.

<!-- example -->

| Access pattern | Store |
|---|---|
| Orders with joins and transactions | PostgreSQL |
| Product catalog with nested attributes | MongoDB / DynamoDB documents |
| Session lookup by ID, millions/s | Redis / DynamoDB |
| Sensor writes by device and time | Cassandra |
| "Friends of friends" or fraud rings | Neo4j / Neptune |

#### What types of databases are there?

Relational (PostgreSQL, MySQL, Oracle), key-value (DynamoDB, Redis), document (MongoDB, Couchbase), wide-column (Cassandra, HBase, Bigtable), graph (Neo4j, Neptune), time series (TimescaleDB, InfluxDB), search (Elasticsearch, OpenSearch), vector (pgvector, Pinecone, OpenSearch vectors) and analytical columnar stores (warehouses, ClickHouse, Druid).

#### When do you choose a relational database?

When data is structured with relationships, needs ACID transactions, flexible querying with joins, and strong consistency: orders, payments, accounts, inventories. It's the default for most operational systems.

#### When do you choose a document database?

When records are self-contained, nested and schema-flexible (product catalogs, content, user profiles), accessed mostly by key or simple queries, and teams want to evolve the schema quickly.

#### When do you choose a key-value store?

For very fast lookups by key at scale (sessions, caches, user preferences, shopping carts), with simple access patterns and predictable latency.

#### When do you choose a wide-column store?

For massive write volumes and large datasets accessed by partition key with known query patterns, like time series, IoT, messaging and event logs (Cassandra, Bigtable, HBase).

#### When do you choose a graph database?

When relationships are the main object of analysis: fraud rings, social networks, recommendations, network topologies, knowledge graphs, where queries traverse many hops.

#### What is polyglot persistence?

Using different storage technologies for different needs within one system (PostgreSQL for orders, Redis for sessions, Elasticsearch for search, S3 for files), accepting more operational complexity for fitness to each use case.

<!-- challenge -->

A team stores user profiles, orders and payments in MongoDB and now struggles with reports joining them and with consistency. What do you suggest?

<!-- solution -->

Keep MongoDB where documents fit (profiles), move orders and payments, which need joins and transactions, to a relational database, and replicate all of them into the analytics platform for reporting.

<!-- takeaways -->

- Choose stores by access pattern.
- Relational for joins and transactions; others for specific shapes.
- Polyglot persistence needs owned integration.

<!-- unit: Specialized stores -->

<!-- goals -->

- Know when time series and search engines fit.
- Distinguish OLTP, OLAP and HTAP.

<!-- concept -->

Some workloads are so common they have their own engines. Time series stores handle high-rate timestamped measurements and queries over time ranges. Search engines rank text by relevance and handle fuzzy matching and facets.

The broadest split is between transactions and analysis: OLTP serves many small reads and writes, OLAP serves large scans and aggregations. HTAP systems try to do both in one engine, which helps for operational analytics but rarely replaces a dedicated analytical platform.

<!-- example -->

| Workload | Engine type |
|---|---|
| CPU metrics every 10 s from 5,000 hosts | Time series |
| Product search with typos and filters | Search engine |
| Checkout and inventory updates | OLTP |
| Monthly revenue by region and channel | OLAP |

#### What is a time series database good for?

High-ingest, time-stamped measurements (metrics, IoT, monitoring) with queries over time ranges, downsampling and retention policies; they compress time series efficiently and offer specialized functions.

#### When would you use a search engine like OpenSearch?

For full-text search with relevance scoring, fuzzy matching, faceting and log analytics, usually as a secondary index fed from the system of record rather than as the primary database.

#### What is the difference between OLTP, OLAP and HTAP?

OLTP handles transactions, OLAP handles analytics, and HTAP (hybrid transactional/analytical processing) systems (TiDB, SingleStore, AlloyDB, Unistore) try to serve both on fresh data, useful for operational analytics with limited scale.

<!-- challenge -->

An e-commerce team implements product search with `LIKE '%term%'` on PostgreSQL and it's slow and misses typos. What do you propose?

<!-- solution -->

Index products in a search engine (OpenSearch or Elasticsearch) fed from the database through CDC or events, and serve search there with relevance, fuzzy matching and facets. PostgreSQL remains the source of truth.

<!-- takeaways -->

- Time series stores handle timestamped measurements.
- Search engines rank and match text.
- OLTP and OLAP need different engines; HTAP blends them.

<!-- unit: Storage layers and formats -->

<!-- goals -->

- Explain object storage, storage tiers and file formats.
- Compare open table formats and the catalog's role.

<!-- concept -->

Modern data platforms rest on object storage: cheap, durable, nearly unlimited and readable by any engine. On top of it, file formats decide how efficiently data is read; columnar formats let analytical queries skip what they don't need.

Open table formats add the missing database features, transactions, schema evolution and time travel, as metadata over those files. A catalog then tells engines which tables exist and who may read them, which is what turns files into a shared platform.

<!-- example -->

```text
catalog (Unity / Glue / Polaris)  ─ tables, schemas, permissions
table format (Iceberg / Delta)    ─ snapshots, transactions, schema
file format (Parquet)             ─ columnar, compressed, statistics
object storage (S3 / ADLS / GCS)  ─ cheap, durable, tiered
```

#### What is object storage, and why is it central to modern data platforms?

Storage of immutable objects in buckets accessed by key over HTTP (S3, ADLS, GCS): virtually unlimited, very durable, cheap and decoupled from compute. Data lakes and lakehouses build on it, with table formats adding database features.

#### What are the differences between block, file and object storage?

Block storage gives raw volumes for one machine (EBS), ideal for databases; file storage gives shared hierarchical file systems (NFS, EFS); object storage gives flat, HTTP-accessible objects at huge scale (S3), ideal for data lakes.

#### What are storage tiers?

Classes of storage with different cost and access speed (hot, warm, cold, archive; S3 Standard, Infrequent Access, Glacier). Lifecycle policies move aging data to cheaper tiers.

#### What are row-oriented versus columnar file formats?

Row formats (CSV, JSON, Avro) store records together, good for writing and reading whole records; columnar formats (Parquet, ORC) store columns together with statistics, good for analytics reading few columns of many rows.

#### What are open table formats?

Specifications (Apache Iceberg, Delta Lake, Apache Hudi) that add a transactional metadata layer over Parquet files in object storage, providing ACID writes, schema evolution, time travel, partition evolution and efficient updates, readable by many engines.

#### Iceberg, Delta or Hudi: how do you choose?

Delta is native to Databricks and widely used in Spark; Iceberg has the broadest multi-engine support (Snowflake, Athena, Trino, Spark, Flink) and an open REST catalog; Hudi focuses on streaming upserts and incremental processing. Choose based on your engines, catalog and governance; interoperability features (UniForm, XTable) narrow the differences.

#### What is a data catalog's role in storage architecture?

It records which tables exist, where their files are, their schemas and permissions, so engines can find and govern data: Hive Metastore, AWS Glue, Unity Catalog, Polaris and Iceberg REST catalogs.

<!-- challenge -->

Three engines (Spark, Trino and a warehouse) must read and write the same tables. Which storage choices keep that possible?

<!-- solution -->

Object storage with Parquet files, an open table format with broad multi-engine support (often Iceberg), and a shared catalog that all three engines use for metadata and permissions.

<!-- takeaways -->

- Object storage is the platform's foundation.
- Columnar formats make analytics cheap.
- Table formats add transactions; catalogs make tables shareable.

<!-- unit: Keys and indexes -->

<!-- goals -->

- Choose a primary key strategy for scale and integration.
- Know which index types matter.

<!-- concept -->

Keys outlive the systems that create them. A key that is unique only inside one database collides when data is merged from several; a key that exposes meaning or sequence leaks information. At scale, ordering also matters, because sequential keys keep indexes compact while random ones scatter writes.

Indexes are the other half: each type suits a query shape, and every index makes writes slower.

<!-- example -->

| Need | Choice |
|---|---|
| Unique across services, generated anywhere | UUIDv7 (time-ordered) |
| Compact, single database | bigint identity |
| Range and equality queries | B-tree index |
| JSON or array contains | GIN index |
| Huge append-only tables by time | BRIN / clustering |

#### How do you choose a primary key strategy at scale?

Consider uniqueness across systems, ordering for index locality, and exposure: auto-increment integers are compact but need central coordination; UUIDv4 are globally unique but random; UUIDv7 and ULIDs are unique and time-ordered; natural keys should stay as attributes.

#### What is an index, and what types matter for data architects?

A structure that speeds up lookups at the cost of writes and storage: B-tree (ranges, equality), hash (equality), GIN/inverted (full text, arrays, JSON), BRIN (huge naturally ordered tables), bitmap (low cardinality in warehouses) and vector indexes (HNSW, IVF) for similarity search.

<!-- challenge -->

After merging two companies' customer tables, IDs collide because both used auto-increment integers. How do you avoid this for the future?

<!-- solution -->

Introduce a global key (for example a UUIDv7 or a source-prefixed surrogate) in the integrated model, keep the original IDs as source attributes, and map them through a key-mapping table.

<!-- takeaways -->

- Keys must be unique across systems that will merge.
- Ordered keys keep indexes efficient.
- Index types fit query shapes; each costs writes.

### Distributed systems fundamentals

<!-- unit: Trade-offs under failure -->

<!-- goals -->

- Explain CAP, PACELC, ACID and BASE.
- Compare consistency models from strong to eventual.

<!-- concept -->

Once data lives on several machines, networks fail and machines disagree. CAP says that during a partition a system must choose between answering and answering correctly; PACELC adds that even without failures there's a choice between speed and consistency.

ACID and BASE describe two attitudes to that choice: strict transactions or availability with eventual agreement. Between them sit useful middle grounds, like guaranteeing users see their own writes, which often satisfy the product without the cost of full consistency.

<!-- example -->

| Use case | Acceptable model |
|---|---|
| Bank transfer | Strong consistency (ACID) |
| Like counter on a post | Eventual consistency |
| User edits a profile and reloads | Read-your-writes |
| Comments thread | Causal consistency |

#### What is the CAP theorem?

In a distributed system facing a network partition, you must choose between consistency (every read sees the latest write) and availability (every request gets a response). Without partitions both are possible; CAP is about behavior during failures.

#### What is PACELC?

An extension of CAP: if there's a Partition, choose Availability or Consistency; Else (normal operation), choose Latency or Consistency. It explains why many systems trade consistency for lower latency even without failures.

#### What is ACID?

Atomicity (all or nothing), Consistency (constraints are preserved), Isolation (concurrent transactions don't interfere) and Durability (committed data survives failures): the guarantees of relational transactions.

#### What is BASE?

Basically Available, Soft state, Eventual consistency: a model favored by some distributed NoSQL systems that prioritize availability and partition tolerance, with data converging to consistency over time.

#### What is eventual consistency?

If no new updates are made, all replicas eventually return the same value; in the meantime, reads may return stale data. Applications must tolerate temporary differences.

#### What consistency models exist besides strong and eventual?

Read-your-writes (a client sees its own writes), monotonic reads (no going back in time), causal consistency (causally related operations are seen in order), bounded staleness (reads at most X seconds behind) and session consistency.

<!-- challenge -->

A shopping cart service must stay available during network issues between regions. Which consistency model fits, and what must the design handle?

<!-- solution -->

Availability with eventual consistency (often per-user read-your-writes). The design must merge conflicting cart updates, for example by keeping item additions as a set and resolving removals with timestamps or version vectors.

<!-- takeaways -->

- During partitions, choose availability or consistency.
- PACELC adds the latency trade-off in normal operation.
- Middle-ground models often meet product needs cheaply.

<!-- unit: Partitioning and replication -->

<!-- goals -->

- Explain partitioning, replication, consensus and quorums.
- Avoid hotspots and distributed transactions.

<!-- concept -->

Distributed databases scale by splitting data across nodes (partitioning) and survive failures by copying it (replication). Each brings its own problem. Partitioning by a skewed key sends most traffic to one node. Replication raises the question of which copy is right, answered by consensus protocols and quorums.

Coordinating a transaction across many nodes or systems with two-phase commit is possible but slow and fragile, which is why modern designs prefer local transactions plus asynchronous coordination.

<!-- example -->

```text
N = 3 replicas, W = 2 write acks, R = 2 read acks
W + R > N  →  every read overlaps the latest write (strongly consistent reads)
hot key "celebrity_123" → add a suffix 0–9 and spread it over 10 partitions
```

#### What is partitioning (sharding)?

Splitting data across nodes by a key (hash or range) so storage and load scale horizontally. A good key spreads data evenly and keeps related data together; bad keys cause hotspots.

#### What is replication, and what are its types?

Keeping copies of data on several nodes for availability and read scaling. Synchronous replication waits for replicas (stronger consistency, higher latency); asynchronous returns before replicas confirm (lower latency, possible data loss on failover). Topologies include leader-follower, multi-leader and leaderless.

#### What is a consensus algorithm?

A protocol (Raft, Paxos, ZAB) that lets distributed nodes agree on a value or leader despite failures, used for metadata, coordination and replicated logs in systems like Kafka (KRaft), etcd and ZooKeeper.

#### What is a quorum?

The minimum number of nodes that must acknowledge a read or write for it to succeed (for example a majority). With read quorum plus write quorum larger than the number of replicas, reads see the latest write.

#### What is the two-phase commit protocol, and why is it avoided?

A protocol where a coordinator asks all participants to prepare, then to commit, ensuring atomicity across systems. It's avoided at scale because it blocks on failures, adds latency and couples availability of all participants; sagas and outbox patterns are preferred.

#### What is a hotspot, and how do you avoid it?

A partition or node receiving disproportionate load because of a skewed key (a celebrity user, a monotonically increasing timestamp). Avoid it with better keys, salting, hashing or splitting hot keys.

<!-- challenge -->

A table partitioned by `country` has one partition with 70% of the load. What do you change?

<!-- solution -->

Partition by a higher-cardinality key (for example `customer_id` hash), or composite keys that split the big country further, so load spreads evenly. Keep `country` as a filter or secondary index.

<!-- takeaways -->

- Partitioning scales; replication protects.
- Quorums and consensus decide which copy wins.
- Avoid skewed keys and distributed transactions.

<!-- unit: Reliable data movement -->

<!-- goals -->

- Make data movement safe with idempotency and delivery semantics.
- Handle backpressure and clock skew.

<!-- concept -->

Moving data between systems means retries, and retries mean duplicates. Most messaging guarantees at-least-once delivery, so correctness comes from idempotent consumers that produce the same result when a message arrives twice.

Two more realities shape designs: consumers can be slower than producers, so systems need backpressure or buffers, and clocks on different machines disagree, so ordering by timestamps across systems needs care.

<!-- example -->

```sql
-- idempotent sink: replaying an event changes nothing
MERGE INTO payments t
USING incoming s ON t.event_id = s.event_id
WHEN NOT MATCHED THEN INSERT *;
```

#### What is idempotency, and why is it vital in data systems?

An operation is idempotent if performing it several times has the same effect as once. Retries are unavoidable in distributed systems, so idempotent writes (upserts, overwrite by partition, deduplication keys) prevent duplicates and corruption.

#### What are delivery semantics in messaging?

At-most-once (may lose messages), at-least-once (may duplicate) and exactly-once (each message's effect happens once). Exactly-once usually means at-least-once delivery plus idempotent or transactional processing.

#### What is backpressure?

A mechanism by which a slower consumer signals producers to slow down (or buffers absorb bursts), preventing overload and memory exhaustion in streaming pipelines.

#### What is clock skew, and why does it matter?

Different machines' clocks disagree, so timestamps from different systems can't be trusted for exact ordering. Use logical clocks, sequence numbers, or source-system log positions for ordering changes.

<!-- challenge -->

A consumer processes payment events with at-least-once delivery and sometimes double-counts revenue. Fix it without changing the broker.

<!-- solution -->

Give each event a unique ID and make the sink idempotent: upsert or `MERGE` on the event ID (or keep a processed-IDs table) so redelivered events don't create new rows.

<!-- takeaways -->

- At-least-once delivery requires idempotent consumers.
- Backpressure stops fast producers overwhelming consumers.
- Don't order events across machines by wall-clock time alone.

<!-- unit: Scaling and performance -->

<!-- goals -->

- Choose between vertical and horizontal scaling.
- Distinguish latency from throughput.

<!-- concept -->

Scaling up a single machine is the simplest move until it hits a ceiling or a price cliff. Scaling out across many machines removes the ceiling but brings the distributed problems of partitioning, replication and coordination.

Performance has two axes that pull in different directions: latency is how fast one request completes, throughput is how many complete per second. Batching raises throughput and latency together; real-time systems sacrifice throughput for latency.

<!-- example -->

| Design | Latency | Throughput |
|---|---|---|
| Insert row by row | Low per row | Low |
| Batch 10,000 rows | Higher per row | High |
| Stream with 1 s micro-batches | Seconds | Medium |

#### What is the difference between horizontal and vertical scaling?

Vertical scaling adds resources to one machine (simpler, limited); horizontal scaling adds machines (near-unlimited, needs partitioning and coordination). Data platforms rely on horizontal scaling for storage and compute.

#### What is the difference between latency and throughput?

Latency is how long one operation takes; throughput is how many operations complete per unit of time. Batch systems optimize throughput; interactive and streaming systems care about latency; improving one can hurt the other.

<!-- challenge -->

A nightly job loading 100 million rows one at a time takes 9 hours. Which trade-off do you change?

<!-- solution -->

Favor throughput over per-row latency: load in large batches or with bulk commands (`COPY`), in parallel by partition. Total time drops dramatically because per-row overhead disappears.

<!-- takeaways -->

- Scale up for simplicity; scale out past limits.
- Latency and throughput trade against each other.
- Batching raises throughput.

<!-- stage: Modeling and storage patterns -->

### Modeling approaches

<!-- unit: Modeling approaches -->

<!-- goals -->

- Compare normalized, dimensional and other modeling approaches.
- Choose between schema-on-write and schema-on-read.

<!-- concept -->

Models encode what the data means. Normalized models store each fact once and suit integration and transactions; dimensional models arrange facts and context for fast, understandable analysis. Canonical models give systems a shared language; highly normalized techniques like anchor modeling favor change over simplicity.

When the schema is enforced matters too: on write catches errors early, on read keeps flexibility for raw and exploratory data. Most platforms do both, at different layers.

<!-- example -->

| Layer | Approach |
|---|---|
| Raw | Schema-on-read, as delivered |
| Integration | 3NF or Data Vault |
| Consumption | Dimensional (star schemas) or wide tables |

#### What modeling approaches are used in data architecture?

Normalized (3NF) models for integration and OLTP, dimensional (Kimball) models for analytics, Data Vault for auditable integration layers, wide denormalized tables (one big table) for specific consumption, and anchor or ensemble models in niche cases.

#### What is third normal form, and why use it?

A normalization level where every non-key attribute depends only on the key, avoiding redundancy and update anomalies. It suits transactional systems and Inmon-style integration layers.

#### What is schema-on-write versus schema-on-read?

Schema-on-write validates and structures data when loading (warehouses), catching errors early. Schema-on-read stores raw data and applies structure when querying (lakes), which is flexible but defers problems to consumers. Lakehouses combine both by layer.

#### What is a canonical data model?

A shared, application-independent representation of core entities and events used for integration between systems, so each system maps to the canonical model rather than to every other system.

#### What is anchor modeling?

A highly normalized (6NF) technique where each attribute is stored in its own table with history, allowing non-destructive schema evolution; it's rare in practice but influenced ideas in Data Vault.

<!-- challenge -->

Analysts query a 3NF integration model directly and write 12-table joins for every report. What do you add?

<!-- solution -->

A dimensional consumption layer: fact tables per business process with conformed dimensions (or wide tables for specific uses), built from the integration model, so reports need few, predictable joins.

<!-- takeaways -->

- Normalized for integration; dimensional for analysis.
- Enforce schema on write where errors are costly.
- Different layers can use different approaches.

<!-- unit: Inmon, Kimball and Data Vault -->

<!-- goals -->

- Describe the Inmon, Kimball and Data Vault methodologies.
- Combine them in a modern layered platform.

<!-- concept -->

The classic debates are about where integration happens. Inmon integrates first into a normalized enterprise warehouse and builds marts from it. Kimball integrates through shared dimensions across process-specific marts. Data Vault separates keys, relationships and history into hubs, links and satellites, so new sources can be added without remodeling.

In practice they're layers rather than rivals: a vault or normalized layer for integration and audit, dimensional marts for consumption.

<!-- example -->

```text
hub_customer       (customer_hk, customer_number, load_ts, source)
link_order_customer (link_hk, order_hk, customer_hk, load_ts, source)
sat_customer_details (customer_hk, load_ts, name, segment, hash_diff)
      └─► dim_customer (Kimball, SCD2) ─► fct_orders
```

#### What is the Inmon architecture?

Bill Inmon's Corporate Information Factory: an enterprise data warehouse in 3NF as the integrated, subject-oriented single version of the truth, feeding dependent data marts for departments. Top-down, integration-first.

#### What is the Kimball architecture?

Ralph Kimball's bus architecture: dimensional data marts per business process, integrated through conformed dimensions and the bus matrix, built incrementally. Bottom-up, business-value-first.

#### What is Data Vault 2.0?

A methodology for the integration layer with hubs (unique business keys), links (relationships) and satellites (descriptive attributes over time), plus hash keys for parallel loading, insert-only history, and standards for business vault and information marts. Designed for agility and auditability with many changing sources.

#### What are hubs, links and satellites?

Hubs store business keys (customer number) with load metadata; links store relationships between hubs (customer-order); satellites store attributes and their history for a hub or link, split by source or change rate.

#### When is Data Vault a good choice?

For enterprises with many sources that change often, strong audit requirements (finance, insurance, regulated industries) and a need to load in parallel and keep full history. It's overkill for small or single-source platforms.

#### How do Kimball, Inmon and Data Vault fit together in practice?

A common modern layering: raw landing, an integration layer (normalized or Data Vault) that historizes and integrates sources, and Kimball star schemas or OBTs for consumption, often mapped to bronze, silver and gold.

<!-- challenge -->

A 20-person company with three sources considers Data Vault "for best practice". What do you advise?

<!-- solution -->

Probably not: Data Vault pays off with many changing sources and strict audit needs. With three sources, a staging layer plus dimensional marts is simpler and faster to deliver; revisit if sources multiply.

<!-- takeaways -->

- Inmon integrates first; Kimball integrates through conformed dimensions.
- Data Vault separates keys, relationships and history.
- Combine them as layers when needed.

<!-- unit: Shaping analytical models -->

<!-- goals -->

- Choose the grain and shape of analytical datasets.
- Model semi-structured data and conform definitions across domains.

<!-- concept -->

Two decisions shape every analytical dataset. Grain, what one row represents, decides what questions it can answer; choosing the most atomic grain consumers need keeps options open. Shape decides how easy it is to use: star schemas for flexibility, one wide table for a specific use.

Across domains, consistency matters more than shape. Conformed keys and definitions are what make "revenue" mean the same thing in every department's report.

<!-- example -->

```text
grain: one row per order line
fct_order_lines(order_line_id, order_id, product_id, customer_id, date_id, quantity, net_amount)
conformed: dim_customer, dim_product, dim_date shared by sales, finance and marketing
```

#### What is the "one big table" (OBT) approach?

A single wide, denormalized table per use case containing everything needed, fast in columnar engines and easy for tools, at the cost of duplicated logic and storage across tables. It's often built on top of dimensional models.

#### What is a "conformed" model across domains?

Shared definitions of keys and entities (customer, product, date) used by every domain's data products, so cross-domain analysis works; in a mesh they're often published as reference data products.

#### How do you decide the grain of a data product?

From consumers' questions and the source's atomic events: choose the most atomic grain that's stable and useful, document it explicitly, and provide aggregates as separate products.

#### How do you model semi-structured data in an analytical platform?

Land it raw (JSON, `VARIANT`, struct columns), extract stable, frequently used fields into typed columns in later layers, keep the rest nested for flexibility, and document schemas with contracts or a registry.

#### A company has ten departments each building their own reports with conflicting numbers. What do you propose?

Identify the core business processes and metrics, create conformed dimensions and certified facts owned by accountable teams, implement a semantic layer for metric definitions, establish data ownership and stewardship, retire duplicated logic gradually, and communicate a catalog of certified datasets.

<!-- challenge -->

A team builds a daily summary table as the only source for revenue. Now finance needs revenue by order line. What went wrong, and the fix?

<!-- solution -->

The grain was chosen too coarse. Build the fact at the atomic grain (order line) and derive the daily summary from it, so new questions can be answered without going back to sources.

<!-- takeaways -->

- Choose the most atomic grain consumers need.
- Wide tables for specific uses; stars for flexibility.
- Conformed definitions make numbers agree.

### Data lakes, lakehouses and medallion

<!-- unit: Lakes, zones and swamps -->

<!-- goals -->

- Describe data lakes and their zones.
- Prevent and recover from a data swamp.

<!-- concept -->

A data lake keeps data of any format cheaply in object storage, usually in zones from raw to curated. Its flexibility is also its risk: without owners, catalogs and standards, it fills with undocumented copies until nobody trusts anything, a swamp.

The fixes are organizational as much as technical: inventory, ownership, zones with clear rules, a catalog and lifecycle policies that remove what nobody uses.

<!-- example -->

```text
s3://lake/landing/   files as delivered (immutable, short retention after processing)
s3://lake/raw/       standardized format, all history
s3://lake/curated/   validated, modeled, owned and documented
s3://lake/sandbox/   per-user experiments, auto-expire after 30 days
```

#### What is a data lake?

A centralized repository in object storage holding raw and processed data of any format at any scale, with cheap storage and schema on read, used for analytics, data science and as a source for warehouses.

#### What is a data swamp?

A data lake that became unusable: undocumented, ungoverned, duplicated data with unknown quality and ownership. Catalogs, ownership, quality checks, zones and lifecycle policies prevent it.

#### What zones does a data lake usually have?

Landing/raw (as received), cleansed/standardized (validated, typed, deduplicated), curated/consumption (business-ready datasets), plus sandbox zones for exploration and archive zones for cold data.

#### What is a "landing zone" versus bronze?

The landing zone holds files exactly as delivered (CSV, JSON, exports) for traceability; bronze is the first table representation of that data with minimal changes plus ingestion metadata, queryable and governed.

#### Your data lake has become a swamp. How do you recover it?

Inventory datasets with usage and owners, define zones and naming standards, register valuable data in a catalog with descriptions and tags, add quality checks, convert key datasets to table formats, archive or delete unused data with lifecycle policies, and make ownership mandatory for new datasets.

<!-- challenge -->

The lake has 8,000 folders and nobody knows which are used. Give the first three steps of a cleanup.

<!-- solution -->

Use access logs and catalog metadata to find what's read and by whom, assign owners to used datasets and register them in the catalog, then archive or delete unused data after announcing a deadline.

<!-- takeaways -->

- Lakes store anything cheaply; zones give structure.
- Swamps come from missing ownership and metadata.
- Recover with inventory, owners, catalog and lifecycle rules.

<!-- unit: Lakehouse and medallion -->

<!-- goals -->

- Explain the lakehouse and the medallion layers.
- Decide between a lakehouse and a warehouse, and avoid common medallion mistakes.

<!-- concept -->

A lakehouse adds warehouse features (transactions, schemas, governance) to a lake through table formats and a catalog, so BI and ML share one copy of the data. Medallion is its usual layering: bronze as received, silver cleaned and conformed, gold ready for consumption.

Layers are a means, not a rule. Copying data through layers that add nothing wastes money, and putting business logic in bronze defeats its purpose. Whether a lakehouse or a warehouse fits depends on workloads, skills and formats.

<!-- example -->

| Layer | Contract |
|---|---|
| Bronze | Append-only, source schema, ingestion metadata |
| Silver | Typed, deduplicated, conformed keys |
| Gold | Business-ready facts, dimensions, aggregates |

#### What is a lakehouse?

An architecture that brings warehouse features (ACID transactions, schema enforcement, governance, performance) to lake storage through open table formats and catalogs, so one copy of data serves BI, ML and data engineering with multiple engines.

#### What is the medallion architecture?

A lakehouse layering pattern: bronze stores raw data as ingested (append-only, with metadata), silver stores cleaned, conformed, deduplicated and historized data, and gold stores business-level aggregates and dimensional models ready for consumption.

#### What are the benefits of the medallion architecture?

Clear responsibilities per layer, the ability to reprocess from raw data, incremental improvement of quality, easier debugging (inspect each layer), and a natural place for quality gates between layers.

#### What are common mistakes with the medallion architecture?

Treating layers as mandatory copies even when they add nothing, mixing business logic into bronze, letting consumers read bronze or silver directly, unclear contracts between layers, and copying data between layers without incremental processing (cost).

#### How does medallion relate to Kimball and Data Vault?

They're complementary: medallion describes layers of refinement; Data Vault can be the modeling technique in silver; Kimball star schemas are typical in gold. Medallion is a layering convention, not a modeling method.

#### How many layers should a lakehouse have?

As many as provide clear value: typically raw/bronze, cleaned/silver and consumption/gold, sometimes a landing zone before and a serving or semantic layer after. Extra layers without distinct contracts just add cost.

#### Lakehouse or warehouse: how do you decide?

A warehouse (Snowflake, BigQuery, Redshift) is simplest for SQL-centric BI with structured data. A lakehouse fits when you need open formats, multiple engines, large semi-structured or unstructured data, ML and streaming on the same data, or want to avoid copies. Many organizations combine them, and the lines are blurring.

<!-- challenge -->

A team creates bronze, silver and gold copies of a small reference table that never changes. Is that good practice?

<!-- solution -->

No. Layers should add value; a static reference table can be loaded once into silver (or gold) and used directly. Keep the raw file for traceability.

<!-- takeaways -->

- Lakehouses add warehouse features to the lake.
- Bronze, silver, gold have different contracts.
- Use layers where they add value.

<!-- unit: Running a lakehouse -->

<!-- goals -->

- Use the catalog as the lakehouse's control plane.
- Plan compaction, schema evolution and time travel.

<!-- concept -->

A lakehouse is only as good as its upkeep. The catalog registers tables, permissions and lineage, so it becomes the control plane. Frequent writes create small files and delete files, so compaction is routine maintenance. Schemas evolve, so each layer needs a policy: permissive in bronze, reviewed in silver and gold.

Time travel turns the table history into a tool for audits, reproductions and recovery, within retention limits that maintenance sets.

<!-- example -->

```sql
OPTIMIZE silver.orders;                                 -- compaction (Delta)
SELECT * FROM gold.revenue TIMESTAMP AS OF '2026-09-30'; -- reproduce month-end report
ALTER TABLE bronze.events ADD COLUMNS (device_type STRING); -- additive change
```

#### What is a data catalog's role in a lakehouse?

It's the control plane: table registry, schemas, permissions, lineage, tags and discovery across engines (Unity Catalog, Glue with Lake Formation, Polaris), turning files into governed tables.

#### What is compaction, and why do lakehouses need it?

Rewriting many small files into fewer larger ones (and merging delete files), which keeps reads fast and metadata small. Streaming and frequent upserts make it necessary; it can be scheduled or automatic.

#### How do you handle schema evolution in a lakehouse?

Allow additive changes (new nullable columns) automatically in bronze, review and apply changes intentionally in silver and gold with table format features (add, rename, widen), and use contracts and alerts for breaking changes.

#### What is "time travel" useful for architecturally?

Reproducing reports as of a date, auditing, debugging what changed, recovering from bad writes and comparing versions, provided retention policies keep enough history.

<!-- challenge -->

An auditor asks for the exact revenue figure the company reported on 30 September, though data was corrected since. How does the architecture help?

<!-- solution -->

With time travel on the gold table (retention covering that date), query it as of the reporting timestamp. For long-term needs, snapshot reported figures into an immutable table, since time travel retention is limited.

<!-- takeaways -->

- The catalog is the lakehouse's control plane.
- Compaction keeps reads fast.
- Time travel helps audits within its retention.

<!-- stage: Moving data -->

### Batch and streaming architectures

<!-- unit: Batch, streaming and their architectures -->

<!-- goals -->

- Compare batch, micro-batch and streaming processing.
- Explain Lambda and Kappa and decide when real-time is needed.

<!-- concept -->

Batch and streaming differ in when results are computed, not in what. Batch processes bounded data on a schedule, simply and cheaply. Streaming processes events as they arrive, for decisions that lose value in minutes.

Lambda ran both paths side by side; Kappa used streams for everything. Modern engines blur the line, running the same code as batch or stream. The real question is business latency: most dashboards are fine hourly, and real-time costs more to build and run.

<!-- example -->

| Use case | Needed latency | Approach |
|---|---|---|
| Fraud check on a card payment | < 1 s | Streaming |
| Inventory on the website | Minutes | Micro-batch or streaming |
| Executive revenue dashboard | Hours | Batch |

#### What is the difference between batch and stream processing?

Batch processes bounded datasets at intervals (hourly, daily) with high throughput and simpler logic; stream processing handles unbounded event flows continuously with low latency, requiring state management, event-time handling and fault tolerance.

#### What is the Lambda architecture?

Nathan Marz's architecture with a batch layer (recomputes accurate views from all history), a speed layer (processes recent data in real time) and a serving layer that merges both. It gives accuracy and low latency but duplicates logic in two code paths.

#### What is the Kappa architecture?

Jay Kreps's simplification: a single stream processing path where everything is a stream; reprocessing is done by replaying the log (Kafka) through a new version of the job. It removes duplicated logic but needs a durable, replayable log and robust streaming.

#### Lambda or Kappa: which is used today?

Pure Lambda is rare because maintaining two code bases is costly. Modern platforms use unified engines (Spark Structured Streaming, Flink, Beam) and table formats that support both batch and streaming on the same tables, closer to Kappa with batch backfills when needed.

#### What is micro-batching?

Processing a stream as a sequence of small batches (seconds to minutes), as Spark Structured Streaming does by default. It simplifies fault tolerance and reuses batch logic, with slightly higher latency than true event-at-a-time processing.

#### When is real-time actually needed?

When decisions or actions lose value within seconds or minutes: fraud detection, operational alerts, personalization, IoT monitoring, dynamic pricing. Many dashboards don't need it; batch or micro-batch is cheaper and simpler.

#### Leadership wants "real-time everything". How do you respond?

Ask which decisions change with fresher data and what latency each needs, estimate costs and complexity for each tier (seconds, minutes, hours), deliver real time where the business value justifies it, and keep the rest in cheaper batch or micro-batch.

<!-- challenge -->

A product manager asks for a real-time dashboard of weekly active users. What do you propose?

<!-- solution -->

Ask which decision depends on it. Weekly active users change slowly, so an hourly or daily batch is enough and much cheaper. Offer streaming only for metrics that drive immediate action.

<!-- takeaways -->

- Batch is simple and cheap; streaming serves urgent decisions.
- Unified engines replace separate Lambda paths.
- Match latency to business value.

<!-- unit: Time in streams -->

<!-- goals -->

- Distinguish event time from processing time.
- Use windows, watermarks and state correctly.

<!-- concept -->

Events arrive late and out of order, so a stream processor must decide which clock to trust. Event time, when something happened, gives correct results; processing time, when it arrived, is simpler but wrong whenever delays vary.

Windows group events in event time, watermarks decide how long to wait for stragglers, and state remembers partial results in between. Joining with reference data adds another time question: which version of the reference applied when the event happened.

<!-- example -->

```python
(events
 .withWatermark("event_time", "10 minutes")           # wait up to 10 min for late events
 .groupBy(F.window("event_time", "5 minutes"), "store_id")
 .agg(F.sum("amount").alias("revenue")))
```

#### What is event time versus processing time?

Event time is when something happened at the source; processing time is when the system processes it. Correct analytics usually need event time, because events arrive late and out of order.

#### What are windows in stream processing?

Groupings of events in time for aggregation: tumbling (fixed, non-overlapping), sliding or hopping (overlapping), and session windows (gaps of inactivity define sessions).

#### What is a watermark in streaming?

A threshold of event time up to which the system assumes it has seen all events, allowing windows to close and state to be cleaned; events later than the watermark are dropped or handled separately.

#### What is stateful stream processing?

Processing that keeps information across events (counts per window, session state, joins between streams, deduplication), requiring fault-tolerant state stores and checkpoints; Flink and Spark manage state with snapshots.

#### How do you join streams with reference data?

Broadcast slowly changing reference data to stream processors and refresh it periodically, join against a changelog stream (temporal or versioned tables), or look up a fast store (Redis, DynamoDB) with caching.

<!-- challenge -->

Mobile app events can arrive hours late when phones are offline. Revenue per 5-minute window keeps changing in the dashboard. How do you design for this?

<!-- solution -->

Aggregate by event time with a watermark that bounds lateness for the live view, and recompute final figures in a batch job (or with upserts) that includes late events. Label recent windows as provisional.

<!-- takeaways -->

- Use event time for correct results.
- Watermarks bound how long to wait for late data.
- State holds partial results; reference joins need versions.

<!-- unit: Kafka as the backbone -->

<!-- goals -->

- Explain Kafka topics, partitions, consumer groups and ordering.
- Use schema registries, exactly-once processing and replay.

<!-- concept -->

Kafka is a durable, replayable log. Producers append events; any number of consumer groups read at their own pace; data stays for a retention period, or indefinitely with tiered storage. That decoupling is why it often becomes the backbone between systems.

Its guarantees are specific: order only within a partition, so keys choose partitions; exactly-once only within Kafka's transactions; and compatibility only if schemas are enforced. Replay from the log is the standard way to reprocess.

<!-- example -->

```text
topic orders (6 partitions, key = customer_id)
  → all events of one customer in order, on one partition
consumer group "billing"   reads every event once (split across its consumers)
consumer group "analytics" reads every event independently
```

#### What is Apache Kafka's role in data architecture?

A distributed, durable, replayable log of events: it decouples producers from consumers, buffers bursts, enables multiple consumers to read the same data at their own pace, and serves as the backbone for streaming, CDC and event-driven systems.

#### What are Kafka topics, partitions and consumer groups?

A topic is a named stream of records; it's split into partitions (ordered, replicated logs) for parallelism; a consumer group shares partitions among its members so each partition is read by one consumer in the group, giving scalable consumption with ordering per partition.

#### How is ordering guaranteed in Kafka?

Only within a partition. Records with the same key go to the same partition, so per-key ordering is preserved; global ordering across partitions isn't guaranteed.

#### What is a schema registry?

A service that stores versioned schemas (Avro, Protobuf, JSON Schema) for topics and enforces compatibility rules, so producers can't publish breaking changes and consumers can deserialize reliably.

#### What is exactly-once processing in Kafka?

Idempotent producers plus transactions that atomically write output records and commit consumer offsets, so a read-process-write cycle's effects happen once even with retries, within Kafka-to-Kafka pipelines.

#### What are tiered storage and infinite retention in Kafka?

Offloading older log segments to object storage, so topics can keep long histories cheaply, enabling replays and Kappa-style reprocessing without huge broker disks.

#### How do you reprocess data in a streaming architecture?

Replay from the log (Kafka retention or tiered storage) into a new version of the job writing to new tables, validate, then switch consumers; or backfill from the lakehouse tables with a batch job using the same logic.

<!-- challenge -->

Order status events (created, paid, shipped) sometimes arrive out of order at a consumer. The topic has 12 partitions and no key. What do you change?

<!-- solution -->

Produce with `order_id` as the key so all events of an order go to the same partition and stay ordered. Consumers should also tolerate duplicates and use a sequence number for safety.

<!-- takeaways -->

- Kafka is a durable, replayable log.
- Order holds per partition; keys pick partitions.
- Schema registries and replay keep streams evolvable.

<!-- unit: Stream engines and serving -->

<!-- goals -->

- Compare stream processing engines and real-time serving stores.
- Add real-time scoring to a batch platform.

<!-- concept -->

Processing and serving are separate choices. Engines like Flink, Spark Structured Streaming and Kafka Streams compute on streams, differing mostly in latency, state handling and the skills they need. Serving fresh results to users needs a store built for low-latency queries on recent data, which ordinary warehouses aren't.

Adding real-time to a batch platform usually means a parallel path for the few use cases that need it, reusing the same definitions.

<!-- example -->

```text
payments ─► Kafka ─► Flink: features (txn count 5 min, amount vs avg)
                         └─► model endpoint ─► decision < 200 ms
                         └─► feature log ─► lake (training, audit)
```

#### What stream processing engines exist?

Apache Flink (low-latency, stateful, event-time), Spark Structured Streaming (micro-batch and continuous, integrated with Spark), Kafka Streams and ksqlDB (library and SQL on Kafka), Apache Beam (portable model, run on Dataflow), and managed services (Kinesis Data Analytics/Managed Flink, Confluent, Databricks).

#### What is a streaming database or real-time OLAP store?

Systems built to ingest streams and serve low-latency analytical queries on fresh data (Apache Druid, Apache Pinot, ClickHouse, Materialize, RisingWave), used for user-facing analytics and operational dashboards.

#### You must add real-time fraud scoring to a batch-oriented platform. How?

Stream transactions from the source (CDC or events) into a broker, compute features with a stream processor using an online feature store (shared definitions with batch training), call the model for scoring in milliseconds, write decisions back as events, and land everything in the lakehouse for analysis and retraining.

<!-- challenge -->

Fraud features in real time and in model training are computed by different code and disagree. How do you fix it?

<!-- solution -->

Compute features once (same definitions) and log the values used for each decision to the lake; train on those logged features or use a feature store that serves the same definitions online and offline.

<!-- takeaways -->

- Engines differ in latency, state and skills.
- Real-time serving needs low-latency stores.
- Add real-time paths only where needed, sharing definitions.

### Microservices and event-driven data

<!-- unit: Data ownership in microservices -->

<!-- goals -->

- Explain database-per-service and why shared databases fail.
- Run analytics across services without coupling to their internals.

<!-- concept -->

Microservices split systems so teams can change independently, and that only works if each service owns its data. A shared database couples everyone to one schema; a change by one team breaks others.

The same logic applies to analytics. Reading services' internal tables makes the data team a hidden consumer of every schema change. Contracts, published events or CDC streams with agreed shapes let services evolve while analytics keeps working.

<!-- example -->

```text
orders-service ─ its own DB ─► publishes OrderPlaced v2 (contract) ─► Kafka ─► lake
payments-service ─ its own DB ─► CDC on the outbox table only     ─► Kafka ─► lake
data team reads contracts, not internal tables
```

#### How do microservices change data architecture?

Each service owns its data and database (database per service), communicating through APIs and events rather than shared tables. This improves autonomy and scaling but scatters data, requiring integration patterns for analytics and cross-service queries.

#### What is the "database per service" pattern?

Each microservice has a private database that only it accesses; other services use its API or its events. It prevents tight coupling through shared schemas.

#### Why is a shared database an anti-pattern in microservices?

Services become coupled through the schema: one team's change breaks others, deployments must be coordinated, and ownership is unclear, losing the main benefit of microservices.

#### How do you do analytics across microservices?

Capture each service's data (CDC from its database or its domain events) into a lake or warehouse, model it centrally or by domain, and serve analytics there, rather than querying services' databases directly.

#### What is an API gateway's role in data access?

A single entry point for client requests that routes to services, handles authentication, rate limiting and aggregation. For data products, APIs or GraphQL layers expose curated data to applications.

#### Microservices teams complain the data team keeps breaking when they change their databases. What do you change?

Stop reading internal tables directly: agree data contracts, have services publish integration events (via an outbox) or curated CDC views, validate contracts in the services' CI, version breaking changes, and give domains ownership of their published data products.

<!-- challenge -->

The data team's pipelines break every time a service renames a column. What agreement do you propose with service teams?

<!-- solution -->

Each service publishes integration events or a CDC-exposed view with a versioned contract, registered in a schema registry with compatibility checks. Internal tables can change freely; contract changes go through versioning.

<!-- takeaways -->

- Each service owns its data.
- Shared databases couple teams.
- Analytics should consume contracts, not internals.

<!-- unit: Events and commands -->

<!-- goals -->

- Distinguish events, commands and messages.
- Design and version events that others can depend on.

<!-- concept -->

Event-driven systems communicate facts. A command asks a service to do something and can be refused; an event states that something already happened and can't be argued with. Facts make good integration because consumers can be added without changing the producer.

That makes events public interfaces. They need clear names, IDs, timestamps and schemas, a choice between carrying data and carrying references, and versioning rules that keep old consumers working.

<!-- example -->

```json
{
  "event_id": "0192f0c3-7a1e-7b3c-9d4e-5f6a7b8c9d0e",
  "event_type": "OrderPlaced",
  "schema_version": 2,
  "occurred_at": "2026-10-17T09:41:12Z",
  "order_id": 98123,
  "customer_id": 552,
  "total_amount": "129.90",
  "currency": "EUR"
}
```

#### What is event-driven architecture?

Systems that communicate by producing and reacting to events (facts about something that happened: `OrderPlaced`, `PaymentFailed`) through a broker, rather than synchronous calls, giving loose coupling, scalability and natural audit trails.

#### What is the difference between events, commands and messages?

A command asks someone to do something (`ShipOrder`) and can be rejected; an event states that something happened (`OrderShipped`) and is immutable; message is the generic envelope carrying either.

#### What are domain events versus integration events?

Domain events are internal to a service's model; integration events are published contracts for other services and analytics, stable and versioned, deliberately decoupled from internal schemas.

#### How should events be designed?

Named in the past tense, with a clear schema, an event ID, timestamps (event and publish time), the entity key, a version, and enough data for consumers (fat events) or a reference to fetch details (thin events), evolving compatibly.

#### What are thin versus fat events?

Thin events carry only identifiers and the type of change, so consumers call back for details (coupling, load on the producer); fat (event-carried state transfer) events carry the full state needed, enabling autonomous consumers at the cost of larger messages and schema care.

#### How do you version event schemas?

Use a schema registry with compatibility rules, add optional fields instead of changing meanings, introduce new event types or versions for breaking changes, and keep old versions until all consumers migrate.

<!-- challenge -->

A team wants to rename `total` to `total_amount` in an event consumed by six services. How do they do it safely?

<!-- solution -->

Add `total_amount` as a new optional field while still sending `total`, register the backward-compatible schema, migrate consumers, then remove `total` in a new major version after a deprecation period.

<!-- takeaways -->

- Commands request; events state facts.
- Integration events are public contracts.
- Version events with compatibility rules.

<!-- unit: Consistency across services -->

<!-- goals -->

- Avoid the dual-write problem with the outbox pattern and CDC.
- Coordinate multi-service processes with sagas, event sourcing and CQRS.

<!-- concept -->

Without shared transactions, keeping services consistent becomes a design problem. Writing to a database and publishing an event separately can lose one of them; the outbox pattern writes both in one local transaction and publishes afterwards, often through CDC.

Longer processes become sagas of local steps with compensations. Event sourcing stores state as its history of events, and CQRS separates write and read models, both useful when audit or read performance justify their complexity.

<!-- example -->

```sql
BEGIN;
UPDATE orders SET status = 'paid' WHERE order_id = 98123;
INSERT INTO outbox (event_id, type, payload) VALUES (gen_random_uuid(), 'OrderPaid', '{"order_id":98123}');
COMMIT;
-- CDC (Debezium) publishes outbox rows to Kafka
```

#### What is event sourcing?

Storing the state of an entity as the sequence of events that changed it, rather than the current state; current state is rebuilt by replaying events. It gives a complete audit log and time travel but complicates queries and schema evolution.

#### What is CQRS?

Command Query Responsibility Segregation: separating the write model (commands, validation) from read models (queries optimized views), often updated asynchronously from events. It scales reads and writes independently and fits event sourcing.

#### What is the transactional outbox pattern?

A service writes its business change and an event record to an outbox table in the same database transaction; a separate process (often CDC) publishes outbox records to the broker. It avoids the dual-write problem of updating the database and publishing an event separately.

#### What is the dual-write problem?

When a service writes to its database and publishes an event as two separate operations, one can succeed and the other fail, leaving systems inconsistent. Outbox or CDC-based publishing solves it.

#### What is the saga pattern?

A way to run business transactions spanning several services as a sequence of local transactions with compensating actions on failure, coordinated by choreography (events) or orchestration (a coordinator), instead of distributed two-phase commits.

#### What is change data capture's role in microservices data integration?

CDC reads each service's database log and publishes changes as events without modifying services, feeding analytics and other services; it's simpler than adding events to legacy code, but exposes internal schemas unless an outbox or contract is used.

#### What is choreography versus orchestration?

In choreography, services react to each other's events without a central coordinator (loose coupling, harder to see the whole flow); in orchestration, a coordinator tells services what to do (clear flow, central dependency). Data pipelines usually use orchestration (Airflow); microservice sagas use either.

<!-- challenge -->

An order service updates its database, then publishes an event to Kafka. Sometimes the event is missing after a crash. What pattern fixes it?

<!-- solution -->

The transactional outbox: write the event to an outbox table in the same transaction as the order update, and publish it from the outbox (with CDC or a relay), so both happen or neither does.

<!-- takeaways -->

- Separate writes to DB and broker can diverge.
- The outbox pattern makes them atomic.
- Sagas coordinate; event sourcing and CQRS fit specific needs.

### Integration and ingestion

<!-- unit: Integration patterns -->

<!-- goals -->

- Compare ETL, ELT, CDC, events, virtualization and reverse ETL.
- Choose an integration pattern per source.

<!-- concept -->

There are only a handful of ways to move data, and each source deserves the right one. Batch extracts suit sources that change little or can't offer more. CDC captures every change from databases with little impact. Events suit systems that already publish facts. Virtualization avoids copying when queries are rare. Reverse ETL sends modeled data back into operational tools.

ELT became the default because cloud storage and engines made it cheap to load first and transform where the data lands.

<!-- example -->

| Source | Pattern |
|---|---|
| Production PostgreSQL | CDC |
| SaaS CRM | Managed connector, incremental |
| Partner CSV drop | Batch file ingestion |
| Microservice with domain events | Event stream |
| Customer scores back to the CRM | Reverse ETL |

#### What are the main data integration patterns?

Batch ETL/ELT, change data capture, event streaming, API-based integration, data virtualization/federation, file transfers, and reverse ETL to push curated data back to operational tools.

#### What is ELT, and why did it become dominant?

Loading raw data into scalable cloud storage or warehouses first and transforming it there with SQL (often dbt). Cheap storage and elastic compute made it simpler and more flexible than transforming before loading.

#### What is data virtualization?

Querying data where it lives through a logical layer (Denodo, Trino, federated queries) without copying it. It's fast to set up and avoids duplication, but performance, history and source load are limitations.

#### What is reverse ETL?

Syncing modeled data from the warehouse into operational systems (CRM, marketing, support tools) so business teams act on analytics, closing the loop between analysis and operations.

#### How do you choose between CDC, batch extracts and events for a source?

CDC for databases you can't change, needing all changes with low latency and low source impact; batch extracts for small or rarely changing data and sources without log access; events when you control the application and want business-level semantics.

<!-- challenge -->

A team runs a nightly full export of a 2 TB production database that takes 6 hours and slows the app. What do you propose?

<!-- solution -->

Switch to CDC: an initial snapshot followed by change capture from the database log, which loads only changes with low impact on the source and gives fresher data.

<!-- takeaways -->

- Choose the integration pattern per source.
- ELT loads first and transforms in the platform.
- Reverse ETL closes the loop to operational tools.

<!-- unit: Ingesting reliably -->

<!-- goals -->

- Ingest from APIs, files and providers with contracts.
- Handle late data and scale ingestion with metadata-driven designs.

<!-- concept -->

Ingestion is where external systems' problems become yours: rate limits, missing files, changed schemas, late records. Contracts set expectations in advance, covering schemas, delivery schedules, completeness signals and who to call. Idempotent, upsert-based loads absorb late and repeated data.

When sources multiply, building one pipeline per source stops scaling. A generic, tested component configured by metadata ingests each new source with a configuration entry instead of new code.

<!-- example -->

```yaml
# sources.yaml driving one generic ingestion job
- name: crm_accounts
  type: api
  endpoint: /v2/accounts
  incremental_key: updated_at
  primary_key: id
  schedule: hourly
- name: partner_sales
  type: s3_files
  path: s3://landing/partner/sales/
  format: csv
  completeness_marker: _SUCCESS
```

#### What should you consider when ingesting from APIs?

Authentication, pagination, rate limits and retries with backoff, incremental extraction (cursors, updated-since), schema drift, idempotency, storing raw responses for reprocessing, and monitoring for silent API changes.

#### What is a data contract in integration?

An explicit, versioned agreement on a dataset or event's schema, semantics, quality and SLAs between producer and consumers, validated in CI and at runtime, making breaking changes visible before they break pipelines.

#### How do you handle late and out-of-order data in integration?

Use event timestamps, allow lateness windows, design upserts and idempotent writes, reprocess recent partitions, and track data completeness so consumers know when a period is final.

#### What are managed connectors, and when do they make sense?

Services like Fivetran, Airbyte Cloud, Lakeflow Connect or AppFlow that extract from SaaS and databases with maintained connectors and schema handling. They save engineering time for standard sources at a per-volume cost; custom code makes sense for unusual sources or huge volumes.

#### How do you design ingestion for many similar sources?

Metadata-driven pipelines: one generic, tested ingestion component configured per source (connection, tables, keys, schedule) from a configuration table or files, rather than one hand-written pipeline per source.

#### What is a landing contract with external data providers?

An agreement on file formats, naming, delivery schedule, completeness signals (manifest or `_SUCCESS` files), encoding, schema changes notice and error handling, which prevents most file ingestion incidents.

<!-- challenge -->

A partner sometimes uploads half a file, and the pipeline loads it before the rest arrives. What do you agree with them and change?

<!-- solution -->

Agree on a completeness signal in the landing contract (a manifest or `_SUCCESS` file written last, with row counts), and make the pipeline start only when it's present and the counts match.

<!-- takeaways -->

- Contracts set expectations with producers.
- Idempotent upserts absorb late and repeated data.
- Metadata-driven ingestion scales to many sources.

<!-- stage: Organizing and governing -->

### Data mesh and data fabric

<!-- unit: Data mesh principles -->

<!-- goals -->

- Explain data mesh's four principles and the problem it addresses.
- Describe data products, federated governance and the platform team.

<!-- concept -->

Central data teams become bottlenecks when many domains produce data and many consumers need it. Data mesh moves ownership to the domains that know the data, asks them to publish it as products with guarantees, gives them a self-serve platform so they don't each build infrastructure, and keeps global standards through federated governance.

It's more an organizational change than a technical one: the hard part is giving domains the skills, incentives and capacity to own data.

<!-- example -->

| Principle | In practice |
|---|---|
| Domain ownership | Payments team owns payments data |
| Data as a product | `payments.transactions` with SLA, docs, owner |
| Self-serve platform | Templates for pipelines, catalog, access |
| Federated governance | Global rules on IDs, PII, quality metrics |

#### What is data mesh?

Zhamak Dehghani's socio-technical approach with four principles: domain-oriented ownership of data, data as a product, a self-serve data platform, and federated computational governance. It decentralizes data ownership to the domains that know the data.

#### What problem does data mesh try to solve?

Central data teams becoming bottlenecks between many source domains and many consumers, losing domain context and scaling poorly as organizations grow.

#### What is a data product in data mesh?

A domain's dataset exposed for consumption with an owner, interface (tables, APIs, events), documentation, quality and SLA guarantees, discoverability, security and versioning, built on the shared platform.

#### What is federated computational governance?

Governance where global standards (interoperability, security, privacy, quality metrics) are agreed by a federation of domain and platform representatives and enforced automatically by the platform (policies as code), while domains decide locally within those rules.

#### What is the role of the platform team in a data mesh?

Providing self-serve infrastructure (storage, compute, pipelines, catalog, access control, observability, templates) so domain teams can build data products without deep platform expertise.

<!-- challenge -->

A company announces "we're doing data mesh" by renaming tables to `<domain>_*`. What is missing?

<!-- solution -->

Ownership and capacity in domains, product guarantees (SLAs, documentation, quality), a self-serve platform, and global standards enforced automatically. Renaming changes nothing about who is accountable.

<!-- takeaways -->

- Mesh moves ownership to domains.
- Data products carry owners and guarantees.
- A platform and federated governance make it workable.

<!-- unit: Adopting a data mesh -->

<!-- goals -->

- Decide whether data mesh fits an organization.
- Start small and measure whether it works.

<!-- concept -->

Data mesh solves a problem of scale and organization, so small companies or immature domains usually get its costs without its benefits. Where it fits, starting small works best: one or two motivated domains with real consumers, a minimal platform, and standards that grow from experience.

Interoperability is what keeps a mesh from becoming many silos: shared identifiers, conventions and contracts. Metrics show whether it's working, in delivery speed, consumer adoption and quality.

<!-- example -->

| Metric | Signal |
|---|---|
| Lead time for a new data product | Falling from months to weeks |
| Products with active consumers | Growing |
| Quality SLOs met | Above 95% |
| Requests to the central team | Falling |

#### When is data mesh a bad fit?

Small organizations, few domains, low data maturity, or no capacity in domains to own data products. Without platform investment and governance, mesh turns into fragmented, inconsistent data.

#### How do you start a data mesh journey?

Pick one or two motivated domains with clear consumers, build a minimal self-serve platform (templates, catalog, access control, quality), define a few global standards, deliver data products end to end, measure adoption, then expand.

#### How do data products stay interoperable in a mesh?

Through global standards: shared identifiers and reference data, naming and metadata conventions, common formats and access methods, quality metrics, and a central catalog for discovery.

#### What metrics show a data mesh is working?

Time to deliver new data products, number of products with active consumers, quality SLO compliance, reduction in central team tickets, reuse across domains, and consumer satisfaction.

<!-- challenge -->

Two domains publish customer data with different IDs, and joining them is impossible. Which mesh principle failed, and how do you fix it?

<!-- solution -->

Federated governance on interoperability: define a global customer identifier (or mapping service) as a standard every product must expose, enforced by platform checks.

<!-- takeaways -->

- Mesh fits large, multi-domain organizations.
- Start with a few domains and real consumers.
- Global identifiers keep products interoperable.

<!-- unit: Data fabric and active metadata -->

<!-- goals -->

- Explain data fabric and how it differs from data mesh.
- Use active metadata to automate governance.

<!-- concept -->

Data fabric approaches the same integration problem from the technology side: rich metadata, automation and virtualization connect data where it lives, with less emphasis on who owns it. Mesh asks who is accountable; fabric asks how to make data findable and usable automatically. They can coexist.

The common thread is active metadata: tags and lineage that don't just document but act, applying masking, routing alerts or recommending datasets.

<!-- example -->

```text
column customers.email tagged pii=true
  → masking policy applied automatically for non-privileged roles
  → lineage propagates the tag to downstream copies
  → quality alert routed to the owner listed in the catalog
```

#### What is a data fabric?

An architecture that uses metadata, knowledge graphs, automation and virtualization to integrate data across distributed sources and present a unified, governed access layer, emphasizing technology (active metadata) over organization.

#### What is the difference between data mesh and data fabric?

Data mesh is primarily organizational (who owns data, product thinking), with decentralization; data fabric is primarily technological (integration through metadata and automation), often centralized. They can be combined.

#### What is "active metadata"?

Metadata that drives automation rather than just documentation: tags that apply masking, lineage that triggers alerts on upstream changes, usage stats that suggest deprecation, quality metrics that gate publishing.

<!-- challenge -->

New tables with personal data keep appearing without masking. How can active metadata help?

<!-- solution -->

Classify columns automatically (scanners or naming rules) and attach tags, then bind masking and access policies to the tags, so any new tagged column is protected without manual work. Propagate tags through lineage.

<!-- takeaways -->

- Fabric automates integration through metadata.
- Mesh is organizational; fabric is technological.
- Active metadata turns tags into enforced policies.

### Governance, metadata and quality

<!-- unit: Roles, policies and definitions -->

<!-- goals -->

- Define governance roles, policies and maturity.
- Use a business glossary and prevent duplicate datasets.

<!-- concept -->

Governance answers "who decides?" for data: who may access it, what terms mean, what quality is acceptable. Owners are accountable, stewards maintain definitions and quality day to day. Without these roles, every question becomes a meeting.

Agreed definitions prevent the most visible failure, two reports with different numbers for the same metric. A glossary records them, and certified, discoverable datasets stop teams from building their own copies.

<!-- example -->

| Term | Definition | Owner |
|---|---|---|
| Active customer | Placed an order in the last 90 days | Sales ops |
| Net revenue | Gross minus refunds, discounts and taxes | Finance |

#### What is data governance?

The framework of roles, policies, standards and processes that ensures data is accurate, secure, compliant, understood and used appropriately, including ownership, stewardship, classification, access, quality and lifecycle.

#### What are data owners and data stewards?

Data owners are accountable for a data domain (decisions on access, definitions, quality targets); data stewards handle day-to-day definitions, quality issues and metadata, working with engineers who implement controls.

#### How do you measure data governance maturity?

By coverage of ownership, documented definitions, classification of sensitive data, access policies as code, lineage, quality SLOs, incident processes, and how often consumers find and trust data without asking around.

#### What is a business glossary?

A curated list of business terms and their agreed definitions (active customer, net revenue, churn), linked to datasets and metrics in the catalog, which aligns teams on meaning.

#### How do you prevent duplicate datasets?

Make existing datasets discoverable (catalog, search), certify authoritative ones, require ownership and review for new published datasets, monitor usage, and deprecate copies.

<!-- challenge -->

Marketing and finance report different "active customer" counts to the board. What governance step resolves it?

<!-- solution -->

Have the business owners agree on one definition in the glossary, implement it once in a certified model, point both reports to it, and label any variant with a distinct name.

<!-- takeaways -->

- Governance assigns decisions to owners and stewards.
- A glossary fixes shared definitions.
- Certified, discoverable datasets prevent copies.

<!-- unit: Metadata and lineage -->

<!-- goals -->

- Manage technical, business and operational metadata.
- Capture lineage and classify data.

<!-- concept -->

Metadata turns a pile of tables into something people can use: what exists, what it means, who owns it, how fresh it is and where it came from. Lineage, the map from sources through transformations to consumers, answers impact questions before changes and root-cause questions after incidents.

Lineage is best captured automatically from the tools that move data. Classification adds sensitivity labels, which drive access policies.

<!-- example -->

```text
crm.accounts ─► bronze.accounts ─► silver.customers ─► gold.dim_customer
                                                    └► gold.churn_features ─► churn model
change silver.customers.segment → impact: 2 gold tables, 1 model, 4 dashboards
```

#### What is metadata management?

Collecting and managing technical, business and operational metadata (schemas, definitions, lineage, quality, usage) to enable discovery, impact analysis, governance and automation; "active metadata" uses it to drive actions.

#### What is data lineage, and how is it captured?

The flow of data from sources through transformations to consumers. It's captured by parsing SQL and jobs (dbt, Unity Catalog, OpenLineage events from Airflow and Spark), and shown at table and column level for impact analysis and audits.

#### What is OpenLineage?

An open standard for lineage events emitted by orchestrators and engines (Airflow, Spark, dbt, Flink) describing jobs, runs and input/output datasets, collected by backends like Marquez or catalogs.

#### What is data classification?

Labeling data by sensitivity (public, internal, confidential, restricted) and type (PII, financial, health), often automated by scanners, to drive access policies, masking, retention and compliance.

<!-- challenge -->

Before removing a column in silver, an engineer asks what might break. How does the architecture answer?

<!-- solution -->

Column-level lineage in the catalog (captured automatically through OpenLineage or query parsing) lists downstream tables, models and dashboards that use it, with owners to notify.

<!-- takeaways -->

- Metadata makes data findable and understandable.
- Lineage answers impact and root-cause questions.
- Classification drives access and protection.

<!-- unit: Master data and quality -->

<!-- goals -->

- Manage master and reference data.
- Build data quality into the architecture.

<!-- concept -->

Core entities like customer and product appear in many systems, each with its own version. Master data management creates one trusted record and maps the others to it; reference data, such as country or currency codes, needs the same single source.

Quality works the same way at every layer: define what "good" means per data product, validate early at ingestion, test transformations, monitor outputs and quarantine what fails instead of publishing it.

<!-- example -->

| Layer | Quality check |
|---|---|
| Ingestion | Schema and contract validation |
| Silver | Uniqueness, nulls, referential integrity |
| Gold | Business rules, reconciliation with source totals |
| Monitoring | Freshness, volume, distribution changes |

#### What is master data management (MDM)?

Creating a single, trusted record for core entities (customer, product, supplier) across systems through matching, merging and survivorship rules, distributed to operational and analytical systems.

#### What is reference data?

Relatively static code sets and classifications used across systems (country codes, currencies, industry codes, status values); managing them centrally avoids inconsistent codes.

#### How do you build data quality into an architecture?

Define quality dimensions and SLAs per data product, validate at ingestion (schemas, contracts), test transformations (uniqueness, integrity, business rules), gate publishing, monitor anomalies and freshness, quarantine bad records, and assign owners to resolve issues.

<!-- challenge -->

The same customer appears three times with slightly different names across CRM, billing and support. How do you give analytics one customer?

<!-- solution -->

Create a master customer with matching rules (or ML matching) across sources, assign a golden ID, keep a cross-reference table to source IDs, and build `dim_customer` from the master record.

<!-- takeaways -->

- MDM creates one trusted record per entity.
- Reference data needs a single source.
- Validate at every layer; quarantine failures.

### Security and compliance

<!-- unit: Access and protection -->

<!-- goals -->

- Layer data security from identity to monitoring.
- Choose between RBAC and ABAC and apply zero trust.

<!-- concept -->

Data security works in layers, so one failure doesn't expose everything: identity and least privilege, network isolation, encryption, fine-grained access to rows and columns, secrets management and monitoring. Each layer assumes the others might fail.

As platforms grow, role-based access becomes a jungle of roles. Attribute-based access grants by tags and user attributes instead, which scales better. Zero trust drops network location as a reason to trust anything.

<!-- example -->

```text
RBAC: role finance_analyst → SELECT on finance.*
ABAC: allow SELECT where table.domain IN user.domains
      AND (column.pii = false OR user.clearance = 'pii')
```

#### What are the layers of data security?

Identity and access management (authentication, least-privilege authorization), network isolation, encryption at rest and in transit, key management, data masking and tokenization, row and column-level security, auditing and monitoring, and secure development practices.

#### What is the difference between RBAC and ABAC?

Role-based access control grants permissions to roles assigned to users; attribute-based access control evaluates attributes of users, resources and context (department, data classification, location) in policies, scaling better for fine-grained rules (for example tag-based policies).

#### What is zero trust in data platforms?

Never trusting by network location: every access is authenticated, authorized with least privilege and audited, with short-lived credentials, workload identities and continuous verification.

#### How do you manage secrets in data platforms?

Store them in a secrets manager (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault, Databricks secret scopes), prefer workload identities and short-lived credentials over static keys, rotate automatically, and never commit them to Git.

#### What is data loss prevention (DLP)?

Tools and policies that detect and block sensitive data from leaving approved boundaries (emails, exports, public buckets), often by scanning content for patterns like card numbers or national IDs.

<!-- challenge -->

The warehouse has 400 roles, many overlapping, and access reviews take weeks. What do you propose?

<!-- solution -->

Move to attribute-based access: tag tables and columns (domain, sensitivity), give users attributes (team, clearance), and write a few policies over tags. Keep a small set of functional roles.

<!-- takeaways -->

- Layer identity, network, encryption, access and monitoring.
- ABAC scales better than many roles.
- Zero trust authenticates every access.

<!-- unit: Privacy and compliance -->

<!-- goals -->

- Apply pseudonymization, anonymization and tokenization.
- Design for GDPR, erasure, residency and secure sharing.

<!-- concept -->

Privacy law shapes architecture. Collect only what's needed, keep it only as long as needed, and know where every person's data lives. Pseudonymization reduces exposure but stays personal data; only true anonymization escapes regulation, and it's harder than it looks.

Rights like erasure need technical support: table formats that delete rows, a map of where identifiers live, and processes that also clean backups and copies. Residency and external sharing add rules about where data may go.

<!-- example -->

```sql
-- erasure request on a lakehouse (Delta/Iceberg)
DELETE FROM silver.customers WHERE customer_id = 552;
DELETE FROM silver.orders    WHERE customer_id = 552;
-- then remove old file versions after retention
VACUUM silver.customers; VACUUM silver.orders;
```

#### What is pseudonymization versus anonymization?

Pseudonymization replaces identifiers with tokens or hashes that can be re-linked with additional information (still personal data under GDPR); anonymization irreversibly prevents identification (no longer personal data), which is hard to achieve in practice.

#### What is tokenization?

Replacing sensitive values (card numbers, national IDs) with non-sensitive tokens, with the mapping kept in a secure vault, so most systems never handle real values.

#### How does GDPR affect data architecture?

It requires lawful basis and purpose limitation, data minimization, retention limits, security, records of processing, and supporting data subject rights (access, rectification, erasure), which means knowing where personal data lives (lineage, catalog) and being able to delete it from all layers, including backups policies and immutable storage designs.

#### How do you implement the right to erasure in a lakehouse?

Track where each person's data lives, use table formats that support deletes (Delta, Iceberg), delete across all layers, vacuum old files after retention, avoid copying raw identifiers widely (pseudonymize early), and document the process and timelines.

#### What is data residency?

Requirements that certain data be stored and processed in specific jurisdictions, which affects region choices, replication, backup locations and which services can be used.

#### How do you secure data sharing with external partners?

Share curated, minimal datasets through governed mechanisms (Delta Sharing, Snowflake shares, presigned access with expiry) rather than file dumps, apply row and column restrictions, contractually define usage, and audit access.

<!-- challenge -->

Analytics tables store customer emails in 40 places. Each erasure request takes a week. How do you redesign?

<!-- solution -->

Pseudonymize early: replace emails with a token in silver, keep the mapping in one protected table, and let downstream tables use the token. Erasure then deletes the mapping and the few raw sources, making tokens unlinkable.

<!-- takeaways -->

- Pseudonymized data is still personal data.
- Erasure needs deletable formats and a map of identifiers.
- Residency and sharing rules constrain data flows.

<!-- stage: Running and evolving -->

### Reliability, operations and cost

<!-- unit: Service levels and observability -->

<!-- goals -->

- Define SLIs, SLOs and SLAs for data products.
- Monitor data with observability and handle incidents.

<!-- concept -->

Users don't care whether a job succeeded; they care whether the data is fresh, complete and right. Service levels make that measurable: indicators like freshness, objectives that set targets, and agreements that promise them to consumers.

Data observability watches the data itself, catching silent failures that green jobs hide. When something goes wrong, incident management, with severity, communication and postmortems, treats data like any production service.

<!-- example -->

| SLI | SLO |
|---|---|
| Freshness of `gold.revenue` | Updated by 07:00 on 99% of days |
| Completeness | Row count within 5% of 7-day average |
| Pipeline success | 99.5% of daily runs |

#### What are SLAs, SLOs and SLIs for data?

SLIs are measured indicators (freshness, completeness, pipeline success rate); SLOs are targets for them (data ready by 7 a.m. 99% of days); SLAs are commitments to consumers with consequences. They make data reliability measurable.

#### What is data observability?

Monitoring freshness, volume, schema, distribution and lineage of data (not just job status) to detect incidents quickly and find their root cause, often with automated anomaly detection.

#### What is a data incident, and how do you manage it?

Any event where data is wrong, late or unavailable for consumers. Manage it like software incidents: detect, assess impact, communicate to consumers, mitigate (pause publishing, roll back), fix the root cause, and write a blameless postmortem with actions.

#### What are RPO and RTO?

Recovery point objective: how much data loss is acceptable (time between last recoverable state and failure). Recovery time objective: how long recovery can take. They drive backup frequency, replication and disaster recovery design.

<!-- challenge -->

All jobs are green, yet a dashboard showed zero sales for one region all morning. Which observability check would have caught it?

<!-- solution -->

A volume or distribution check on the output (rows per region compared with history), alerting when a segment drops to zero, regardless of job status.

<!-- takeaways -->

- Measure what users feel: freshness, completeness, correctness.
- Observability watches data, not just jobs.
- Handle data incidents like software incidents.

<!-- unit: Designing for failure -->

<!-- goals -->

- Design pipelines that fail safely and recover.
- Use dead-letter queues, IaC and capacity planning.

<!-- concept -->

Failures will happen; the design decides whether they're routine or crises. Steps that are idempotent and restartable can simply be retried. Bad records go to a dead-letter queue instead of stopping everything. Infrastructure in code can be recreated. Capacity planning keeps growth from becoming an outage.

The goal is that no single bad file, node or deploy takes the platform down or loses data.

<!-- example -->

```text
stream ─► parse/validate ─┬─► valid  ─► silver
                          └─► invalid ─► dead-letter topic (with error, source, offset)
                                         └─► alert + reprocess after fix
```

#### How do you design pipelines for failure?

Assume failures: idempotent and restartable steps, retries with backoff for transient errors, checkpoints for streams, dead-letter queues for bad records, alerts with runbooks, and the ability to backfill specific periods.

#### What is a dead-letter queue?

A place where messages or records that can't be processed (invalid format, failed validation) are sent with error information, so the pipeline continues and the failures can be inspected and replayed later.

#### What is infrastructure as code's role in data architecture?

Defining platforms (storage, compute, permissions, catalogs, jobs) declaratively in code (Terraform, CloudFormation, Bicep, bundles) so environments are reproducible, reviewed and auditable, and drift is detectable.

#### What is capacity planning for data platforms?

Forecasting growth of data volume, users and workloads to ensure storage, compute and concurrency remain adequate and budgets are prepared, using trends from monitoring and business plans.

<!-- challenge -->

One malformed record in a daily file makes the entire load fail, blocking all reports. How do you redesign it?

<!-- solution -->

Validate per record: send invalid rows to a quarantine table or dead-letter location with the error, load the valid ones, and alert if invalid rows exceed a threshold. Reprocess quarantined rows after fixing.

<!-- takeaways -->

- Idempotent, restartable steps make retries safe.
- Dead-letter queues isolate bad records.
- IaC and capacity planning prevent self-made outages.

<!-- unit: Cost and retention -->

<!-- goals -->

- Identify cost drivers and design cost-efficient platforms.
- Apply FinOps and retention policies.

<!-- concept -->

Data platforms spend most on compute: always-on clusters, full recomputes and inefficient queries. Storage is cheap per byte but grows forever unless retention says otherwise. Cost-efficient designs process incrementally, prune with partitioning, scale to zero when idle and keep data only as long as it's useful or legally required.

FinOps makes cost visible to the teams who cause it, so efficiency becomes a shared habit rather than a yearly cleanup.

<!-- example -->

| Layer | Retention |
|---|---|
| Landing files | 30 days after processing |
| Bronze | 7 years (legal), cold tier after 1 year |
| Gold aggregates | As long as used |
| Sandbox | 30 days, auto-delete |

#### What is FinOps for data platforms?

The practice of managing cloud data costs collaboratively: visibility (tagging, cost per pipeline and team), optimization (right-sizing, auto-suspend, storage tiers, query tuning, incremental processing) and governance (budgets, alerts, accountability).

#### What are the biggest cost drivers in data platforms?

Compute for transformations and queries (especially always-on clusters and full recomputes), inefficient queries on large data, data duplication across layers and tools, egress and cross-region transfer, and unused data kept forever.

#### How do you make a platform cost-efficient by design?

Incremental processing, partitioning and clustering for pruning, serverless or auto-scaling compute with auto-suspend, tiered storage and retention, avoiding unnecessary copies, choosing latency appropriate to the business need, and making costs visible per team.

#### How do you set retention policies architecturally?

Classify datasets by legal and business needs, define retention per layer (raw might be kept longer for reprocessing, or shorter for privacy), implement with lifecycle rules, partition drops and table format retention, and document exceptions.

<!-- challenge -->

Cloud costs grew 60% in a year, mostly from a few pipelines that rebuild full tables nightly. What do you change?

<!-- solution -->

Make them incremental (process only new or changed partitions with `MERGE`), add partition pruning, right-size or autoscale the compute, and show each team its cost per data product.

<!-- takeaways -->

- Compute dominates cost; incremental beats full rebuilds.
- Design for pruning and scale to zero.
- Retention policies control storage growth.

### AI and ML data architecture

<!-- unit: Data for machine learning -->

<!-- goals -->

- Describe what ML platforms need: features, point-in-time data and MLOps.
- Prevent training-serving skew and monitor drift.

<!-- concept -->

Models are only as good as their training data, and ML adds requirements that BI doesn't have. Training sets must use only information available at prediction time, or models look great in testing and fail in production. Features must be computed the same way for training and serving.

A feature store addresses both, and MLOps wraps the lifecycle: versioned data and models, automated retraining, and monitoring for when inputs or relationships drift.

<!-- example -->

```text
label: churned on 2026-06-01
features must come from data known on 2026-05-31:
  orders_last_90d   ✔ computed from orders before 2026-05-31
  support_tickets   ✘ includes the cancellation ticket of 2026-06-02 → leakage
```

#### What does an ML platform need from the data architecture?

Reliable, versioned training data, point-in-time correct features, feature reuse between training and serving, lineage from data to models, experiment tracking, model registry, and monitoring of data and prediction drift.

#### What is a feature store?

A system that stores, documents and serves ML features consistently for training (offline, historical, point-in-time correct) and inference (online, low latency), avoiding training-serving skew and duplicated feature engineering.

#### What is point-in-time correctness?

When building training data, features must use only information available at the time of each label's event, avoiding leakage of future data; feature stores join features as of each event timestamp.

#### What is training-serving skew?

Differences between how features are computed for training and for inference (different code, data sources or timing), which degrade model performance in production. Shared feature definitions and feature stores reduce it.

#### What is MLOps?

Practices and tooling to develop, deploy and operate ML models reliably: versioned data and code, reproducible training pipelines, model registry, automated testing and deployment, monitoring of performance and drift, and retraining.

#### What is data drift versus concept drift?

Data drift is a change in the input data distribution (customers' ages shift); concept drift is a change in the relationship between inputs and the target (what predicts churn changes). Both require monitoring and possibly retraining.

<!-- challenge -->

A churn model has 97% accuracy in testing and 70% in production. What do you suspect first?

<!-- solution -->

Leakage from training data that isn't point-in-time correct (features using information from after the prediction date), or training-serving skew in feature computation. Rebuild the training set with point-in-time joins and compare feature values.

<!-- takeaways -->

- Training data must be point-in-time correct.
- Compute features once for training and serving.
- Monitor data and concept drift.

<!-- unit: Data for generative AI -->

<!-- goals -->

- Place vector databases and RAG pipelines in the architecture.
- Govern unstructured data used by AI.

<!-- concept -->

Generative AI applications retrieve relevant documents and hand them to a model. That turns unstructured files into data products: they need ingestion, chunking, embeddings, metadata and a vector index that stays in sync with the source.

Governance follows the data. A retrieval system must respect the same permissions as the documents, and teams must know which data fed which model or answer.

<!-- example -->

```text
docs (S3 / SharePoint) ─► parse + chunk ─► embeddings ─► vector index (with ACL metadata)
user question ─► retrieve top-k allowed chunks ─► LLM ─► answer with sources
lineage: answer → chunks → documents → owners
```

#### What is a vector database, and where does it fit?

A store optimized for similarity search over embeddings (pgvector, OpenSearch, Pinecone, Weaviate, Databricks Vector Search), used for semantic search, recommendations and retrieval-augmented generation.

#### What is the data architecture of a RAG application?

Ingest documents, split them into chunks, compute embeddings, store them with metadata in a vector index, retrieve relevant chunks at query time (often combined with keyword search and filters by permissions), and pass them to an LLM, with pipelines to keep the index fresh and governed.

#### How do governance concerns change with AI?

You must track which data trained which models, respect permissions in retrieval (users shouldn't see documents through an LLM they couldn't access directly), manage PII in prompts and training data, and evaluate outputs; catalogs increasingly govern models and features alongside tables.

#### How should unstructured data be managed for AI?

Store it in object storage with metadata in a catalog (volumes), track lineage from documents to chunks and embeddings, apply access controls and classification, and build pipelines that update indexes when documents change or are deleted.

<!-- challenge -->

An internal assistant answers employees' questions from company documents, and someone gets an answer quoting HR files they can't open. What went wrong?

<!-- solution -->

Retrieval ignored document permissions. Store access-control metadata with each chunk and filter retrieval by the user's identity, so the model only sees chunks the user may read.

<!-- takeaways -->

- RAG turns documents into governed data products.
- Keep vector indexes in sync with sources.
- Retrieval must enforce source permissions.

### Cloud and reference architectures

<!-- unit: Reference architectures -->

<!-- goals -->

- Sketch typical data architectures on AWS, Azure and Google Cloud.
- Map equivalent services across clouds.

<!-- concept -->

The three major clouds offer the same building blocks under different names: ingestion services, object storage, a catalog, processing engines, a warehouse and BI. Knowing the pattern matters more than the product list, because the shape repeats: land data in object storage or a warehouse, catalog and govern it, transform it, serve it.

Differences lie in integration depth and defaults, such as how tightly the warehouse and lake are combined.

<!-- example -->

| Layer | AWS | Azure | Google Cloud |
|---|---|---|---|
| Ingestion | DMS, Kinesis, Glue | Data Factory, Event Hubs | Datastream, Pub/Sub |
| Storage | S3 | ADLS / OneLake | Cloud Storage |
| Catalog | Glue + Lake Formation | Purview / Unity | Dataplex |
| Warehouse | Redshift | Fabric / Synapse | BigQuery |

#### What does a typical AWS data architecture look like?

Sources ingested with DMS, Kinesis/MSK, AppFlow or Glue into S3; Glue Data Catalog and Lake Formation for governance; processing with Glue, EMR or Databricks; Iceberg or Delta tables; Athena and Redshift for SQL; QuickSight for BI; SageMaker for ML; Step Functions, MWAA or EventBridge for orchestration; all defined with CloudFormation, CDK or Terraform.

#### What does a typical Azure data architecture look like?

Ingestion with Data Factory or Fabric pipelines and Event Hubs into ADLS Gen2/OneLake; processing with Databricks or Fabric Spark; Delta tables; Synapse/Fabric warehouses or Databricks SQL; Power BI; Purview for governance; Entra ID for identity.

#### What does a typical Google Cloud data architecture look like?

Ingestion with Pub/Sub, Datastream (CDC) and Dataflow into Cloud Storage and BigQuery; processing with Dataflow, Dataproc or BigQuery SQL (often with dbt or Dataform); Dataplex for governance; Looker for BI; Vertex AI for ML.

<!-- challenge -->

An interviewer asks you to design on a cloud you've never used. How do you answer convincingly?

<!-- solution -->

Describe the layers and requirements first (ingestion, storage, catalog, processing, serving, governance), then map each to the cloud's equivalent service, saying where you'd check details. The pattern shows judgment more than product names.

<!-- takeaways -->

- All clouds offer the same layers.
- Learn the pattern, then map the services.
- Integration depth differs between clouds.

<!-- unit: Multi-cloud, hybrid and migration -->

<!-- goals -->

- Decide when multi-cloud or hybrid architectures are worth it.
- Plan migrations and organize cloud accounts for a data platform.

<!-- concept -->

Multi-cloud sounds like freedom but doubles skills, tooling and integration work; it pays off for specific reasons such as regulation, acquisitions or customer demands. Hybrid setups are common during migrations and for systems that must stay on premises.

Migrations follow the familiar spectrum from rehosting to rebuilding. Underneath, a landing zone with separate accounts per environment and domain gives security and cost boundaries from day one.

<!-- example -->

```text
organization
 ├─ security (logs, audit)
 ├─ shared-network
 ├─ data-dev / data-staging / data-prod
 └─ domain-payments-prod, domain-marketing-prod (mesh-style)
```

#### What is multi-cloud, and when is it worth it?

Using several cloud providers. It can reduce dependency, meet customer or regulatory requirements, or use best-of-breed services, but it multiplies skills, tooling, networking and egress costs. Most organizations benefit more from one primary cloud with portable formats.

#### What is a hybrid architecture?

Combining on-premises systems with cloud services, common during migrations or for regulated data; it needs secure connectivity (VPN, Direct Connect, ExpressRoute), consistent identity and governance, and careful data movement.

#### What are migration strategies for data platforms?

Rehost (lift and shift), replatform (move to managed equivalents with small changes), refactor (redesign for cloud-native services and ELT), retire unused assets and retain what must stay. Data migrations usually combine them, moving in waves by domain with parallel validation.

#### What is a landing zone in cloud architecture?

A preconfigured, secure multi-account (or subscription) environment with identity, networking, logging, security guardrails and account structure, on which data platforms are deployed consistently.

#### How should accounts or projects be organized for a data platform?

Separate environments (dev, staging, prod) and often domains into different accounts or projects for blast-radius isolation, cost visibility and least privilege, with shared services (catalog, networking, logging) managed centrally.

<!-- challenge -->

Leadership wants to run every workload on two clouds "to avoid lock-in". What do you advise?

<!-- solution -->

Explain the cost: duplicate skills, tooling and integration, and lowest-common-denominator services. Limit lock-in with open formats and portable tools instead, and use a second cloud only where a concrete requirement justifies it.

<!-- takeaways -->

- Multi-cloud has real costs; use it for concrete reasons.
- Hybrid is common during migrations.
- A landing zone sets account boundaries early.

<!-- stage: Putting it together -->

### Scenarios

<!-- unit: Designing a platform from scratch -->

<!-- goals -->

- Design a data platform end to end for a given company.
- Scale the design to the company's size and maturity.

<!-- concept -->

Design questions test judgment, not tool lists. A strong answer starts from the business questions and constraints, then walks the layers: how each source is ingested, where data is stored and in what formats, how it's modeled, how it's served, and how it's governed, secured and monitored. Then it scales the design to the company: a startup needs managed simplicity, a mid-size company needs structure, and both need a path to grow.

<!-- example -->

| Layer | Startup | Mid-size e-commerce |
|---|---|---|
| Ingestion | Managed connectors | CDC, event stream, connectors |
| Storage | Cloud warehouse | Lakehouse or warehouse + lake |
| Modeling | dbt, a few marts | Medallion + dimensional marts |
| Governance | Basic roles, docs | Catalog, owners, classification |

#### Design a data platform for a mid-size e-commerce company.

Ingest the orders database with CDC, web events through a stream (Kafka or Kinesis), and SaaS tools (CRM, marketing) with connectors into object storage; organize medallion layers with Iceberg or Delta tables in a catalog; transform with dbt or Spark into conformed dimensions and facts; serve BI from a warehouse or lakehouse SQL engine with a semantic layer; add reverse ETL for marketing segments; orchestrate with Airflow or native jobs; enforce governance, quality tests, observability and cost tagging; define everything as code with CI/CD.

#### A startup asks you to design its first data platform. What do you recommend?

Keep it simple and managed: a cloud warehouse or lakehouse service, managed connectors for SaaS sources, CDC or replicas for the product database, dbt for transformations with tests, one orchestrator, a BI tool with a semantic layer, basic governance and cost alerts, all as code. Add streaming, mesh or custom components only when needs appear.

<!-- challenge -->

The startup from your design doubles every year. What would you change in year three, and what would you keep?

<!-- solution -->

Keep the warehouse, dbt and managed connectors. Add a catalog with owners, data contracts with product teams, CDC for the main database, cost monitoring, and possibly a lake for raw and ML data as volumes grow.

<!-- takeaways -->

- Start from questions and constraints, then walk the layers.
- Scale the design to company size and maturity.
- Leave a path to grow without rebuilding.

<!-- unit: Integrating after an acquisition -->

<!-- goals -->

- Plan data integration between two companies' platforms.
- Prioritize business questions over platform consolidation.

<!-- concept -->

After an acquisition, leadership wants combined numbers long before platforms can merge. The practical path is to start from the questions that need answering, map the key entities and metrics between the companies, and replicate the needed data into one platform. Platform consolidation follows later, once definitions are aligned and the business sees results.

<!-- example -->

```text
week 1–4:  agree on 10 key metrics and their definitions; map customer, product, revenue
week 4–8:  replicate needed tables from company B into A's platform; build combined marts
month 3+:  plan migration of B's pipelines; retire duplicate tools
```

#### Your company acquired another one with a different cloud and platform. How do you integrate data?

Start with the questions leadership needs answered, map key entities and metrics, replicate the necessary data into the primary platform with CDC or exports (or share it via open formats), build conformed dimensions with master data matching, and plan longer-term consolidation of platforms based on cost and capabilities.

<!-- challenge -->

Both companies define "customer" differently: one counts accounts, the other counts people. How do you produce a combined customer count?

<!-- solution -->

Agree on one definition with business owners (or report both clearly labeled), map each company's records to it through a key-mapping table, and document the rule in the glossary before publishing combined numbers.

<!-- takeaways -->

- Start from the questions leadership needs answered.
- Map entities and metrics before moving platforms.
- Consolidate platforms after definitions align.
