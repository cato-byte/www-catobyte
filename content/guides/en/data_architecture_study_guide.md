## Data Architecture Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Data architecture study guide: about 200 questions](../../images/data_architecture_study_guide_title_img.png)

About 200 interview-style questions on data architecture: principles, storage and database choices, distributed systems trade-offs, modeling approaches (Inmon, Kimball, Data Vault), lakes, lakehouses and the medallion pattern, batch and streaming architectures (Lambda, Kappa), microservices and event-driven data, data mesh and data fabric, governance, security, reliability, cost, and architecture for AI. It complements the data warehousing guide, which goes deeper into dimensional modeling. Open a question to see its answer, or use the filter to search the whole guide.

<!-- QA -->

### Principles

#### What is data architecture?

The set of decisions, models, policies and standards that define how data is collected, stored, integrated, processed, governed and consumed across an organization, and the systems that implement them.

#### What does a data architect do?

Translates business needs into data structures and platforms: chooses technologies and patterns, designs models and flows, defines standards for quality, security and governance, documents decisions, and guides teams so systems fit together and evolve without constant rework.

#### What are the main layers of a modern data architecture?

Sources, ingestion (batch, CDC, streaming), storage (lake, warehouse, operational stores), processing and transformation, serving (BI, APIs, ML features, reverse ETL), plus cross-cutting orchestration, governance, security, observability and metadata.

#### What are good data architecture principles?

Treat data as a product with owners; design for change (loose coupling, contracts); keep one source of truth per entity; store raw data immutably and reprocess when logic changes; secure and govern by default; automate everything as code; optimize for the questions people ask; and prefer simple, managed components when they meet requirements.

#### What is the difference between conceptual, logical and physical data models?

Conceptual models show business entities and relationships for stakeholders; logical models add attributes, keys and normalization without technology details; physical models implement them in a specific database with types, indexes, partitions and storage choices.

#### What are functional versus non-functional requirements in data architecture?

Functional: which data, transformations, metrics and outputs are needed. Non-functional: latency, freshness, volume, scalability, availability, durability, security, compliance, cost and maintainability, which often drive the technology choices.

#### What is an architecture decision record (ADR)?

A short document capturing a significant decision: context, options considered, decision, consequences and status. ADRs make reasoning visible and stop teams from relitigating decisions; they're stored with the code.

#### What is technical debt in data platforms?

Shortcuts that make future change costly: undocumented pipelines, duplicated logic, hard-coded configuration, missing tests, unowned tables, quick fixes in production. It accumulates silently and shows up as incidents, slow delivery and distrust of numbers.

#### What does "build versus buy" mean for data platforms?

Choosing between building custom components (more control, more maintenance) and using managed services or vendors (faster, less control, recurring cost, lock-in). Most teams buy commodity capabilities (storage, warehouse, connectors) and build what differentiates them.

#### What is vendor lock-in, and how do you limit it?

Dependence on one vendor's proprietary formats or APIs that makes switching expensive. Limit it with open formats (Parquet, Iceberg, Delta), standard SQL, infrastructure as code, abstraction where it's cheap, and exit plans for critical components, accepting some lock-in where value is high.

#### What is "data as a product"?

Managing datasets like products: a clear owner, documented purpose and schema, quality guarantees and SLAs, discoverability, versioning, and feedback from consumers. It's a core idea of data mesh but useful in any architecture.

#### What are the trade-offs between centralization and decentralization?

Centralized platforms and teams give consistency, economies of scale and strong governance but become bottlenecks. Decentralized domain ownership scales delivery and puts expertise close to data but risks inconsistency and duplicated effort; federated governance balances them.

#### What is the difference between data architecture and data engineering?

Data architecture defines the blueprint: structures, standards, technology choices and how components fit together. Data engineering builds and operates the pipelines and platforms that implement it. In practice the roles overlap, and senior engineers make many architectural decisions.

#### How do you evaluate a new technology for the platform?

Start from requirements, compare a few options against criteria (fit, performance, cost, skills, ecosystem, support, security, lock-in), run a proof of concept on real workloads, consider total cost of ownership and exit costs, and record the decision in an ADR.

#### What is total cost of ownership (TCO)?

The full cost of a solution over time: licenses or cloud usage, infrastructure, people to build and operate it, training, migration, support and the cost of downtime, not just the price per unit of compute.

#### What is "evolutionary architecture"?

Designing systems to change incrementally with guardrails (fitness functions such as tests on latency, cost or coupling), favoring reversible decisions and small steps over big upfront designs.

#### Why should raw data be immutable?

Immutable raw data lets you reprocess history when logic or bugs change, audit what sources sent, and rebuild downstream layers; mutations happen in later layers, keeping the system recoverable.

#### What is the "single responsibility" idea applied to data pipelines?

Each pipeline or model should have one clear purpose (ingest a source, conform an entity, build a metric), which makes it easier to test, own, reuse and change without side effects.

### Storage and databases

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

#### What is the difference between OLTP, OLAP and HTAP?

OLTP handles transactions, OLAP handles analytics, and HTAP (hybrid transactional/analytical processing) systems (TiDB, SingleStore, AlloyDB, Unistore) try to serve both on fresh data, useful for operational analytics with limited scale.

#### How do you choose a primary key strategy at scale?

Consider uniqueness across systems, ordering for index locality, and exposure: auto-increment integers are compact but need central coordination; UUIDv4 are globally unique but random; UUIDv7 and ULIDs are unique and time-ordered; natural keys should stay as attributes.

#### What is an index, and what types matter for data architects?

A structure that speeds up lookups at the cost of writes and storage: B-tree (ranges, equality), hash (equality), GIN/inverted (full text, arrays, JSON), BRIN (huge naturally ordered tables), bitmap (low cardinality in warehouses) and vector indexes (HNSW, IVF) for similarity search.

#### What is a time series database good for?

High-ingest, time-stamped measurements (metrics, IoT, monitoring) with queries over time ranges, downsampling and retention policies; they compress time series efficiently and offer specialized functions.

#### When would you use a search engine like OpenSearch?

For full-text search with relevance scoring, fuzzy matching, faceting and log analytics, usually as a secondary index fed from the system of record rather than as the primary database.

### Distributed systems fundamentals

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

#### What is partitioning (sharding)?

Splitting data across nodes by a key (hash or range) so storage and load scale horizontally. A good key spreads data evenly and keeps related data together; bad keys cause hotspots.

#### What is replication, and what are its types?

Keeping copies of data on several nodes for availability and read scaling. Synchronous replication waits for replicas (stronger consistency, higher latency); asynchronous returns before replicas confirm (lower latency, possible data loss on failover). Topologies include leader-follower, multi-leader and leaderless.

#### What is a consensus algorithm?

A protocol (Raft, Paxos, ZAB) that lets distributed nodes agree on a value or leader despite failures, used for metadata, coordination and replicated logs in systems like Kafka (KRaft), etcd and ZooKeeper.

#### What is idempotency, and why is it vital in data systems?

An operation is idempotent if performing it several times has the same effect as once. Retries are unavoidable in distributed systems, so idempotent writes (upserts, overwrite by partition, deduplication keys) prevent duplicates and corruption.

#### What are delivery semantics in messaging?

At-most-once (may lose messages), at-least-once (may duplicate) and exactly-once (each message's effect happens once). Exactly-once usually means at-least-once delivery plus idempotent or transactional processing.

#### What is backpressure?

A mechanism by which a slower consumer signals producers to slow down (or buffers absorb bursts), preventing overload and memory exhaustion in streaming pipelines.

#### What is the difference between horizontal and vertical scaling?

Vertical scaling adds resources to one machine (simpler, limited); horizontal scaling adds machines (near-unlimited, needs partitioning and coordination). Data platforms rely on horizontal scaling for storage and compute.

#### What is a hotspot, and how do you avoid it?

A partition or node receiving disproportionate load because of a skewed key (a celebrity user, a monotonically increasing timestamp). Avoid it with better keys, salting, hashing or splitting hot keys.

#### What is the two-phase commit protocol, and why is it avoided?

A protocol where a coordinator asks all participants to prepare, then to commit, ensuring atomicity across systems. It's avoided at scale because it blocks on failures, adds latency and couples availability of all participants; sagas and outbox patterns are preferred.

#### What is a quorum?

The minimum number of nodes that must acknowledge a read or write for it to succeed (for example a majority). With read quorum plus write quorum larger than the number of replicas, reads see the latest write.

#### What is clock skew, and why does it matter?

Different machines' clocks disagree, so timestamps from different systems can't be trusted for exact ordering. Use logical clocks, sequence numbers, or source-system log positions for ordering changes.

#### What is the difference between latency and throughput?

Latency is how long one operation takes; throughput is how many operations complete per unit of time. Batch systems optimize throughput; interactive and streaming systems care about latency; improving one can hurt the other.

### Modeling approaches

#### What modeling approaches are used in data architecture?

Normalized (3NF) models for integration and OLTP, dimensional (Kimball) models for analytics, Data Vault for auditable integration layers, wide denormalized tables (one big table) for specific consumption, and anchor or ensemble models in niche cases.

#### What is third normal form, and why use it?

A normalization level where every non-key attribute depends only on the key, avoiding redundancy and update anomalies. It suits transactional systems and Inmon-style integration layers.

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

#### What is the "one big table" (OBT) approach?

A single wide, denormalized table per use case containing everything needed, fast in columnar engines and easy for tools, at the cost of duplicated logic and storage across tables. It's often built on top of dimensional models.

#### How do Kimball, Inmon and Data Vault fit together in practice?

A common modern layering: raw landing, an integration layer (normalized or Data Vault) that historizes and integrates sources, and Kimball star schemas or OBTs for consumption, often mapped to bronze, silver and gold.

#### What is schema-on-write versus schema-on-read?

Schema-on-write validates and structures data when loading (warehouses), catching errors early. Schema-on-read stores raw data and applies structure when querying (lakes), which is flexible but defers problems to consumers. Lakehouses combine both by layer.

#### What is a canonical data model?

A shared, application-independent representation of core entities and events used for integration between systems, so each system maps to the canonical model rather than to every other system.

#### What is anchor modeling?

A highly normalized (6NF) technique where each attribute is stored in its own table with history, allowing non-destructive schema evolution; it's rare in practice but influenced ideas in Data Vault.

#### How do you model semi-structured data in an analytical platform?

Land it raw (JSON, `VARIANT`, struct columns), extract stable, frequently used fields into typed columns in later layers, keep the rest nested for flexibility, and document schemas with contracts or a registry.

#### What is a "conformed" model across domains?

Shared definitions of keys and entities (customer, product, date) used by every domain's data products, so cross-domain analysis works; in a mesh they're often published as reference data products.

#### How do you decide the grain of a data product?

From consumers' questions and the source's atomic events: choose the most atomic grain that's stable and useful, document it explicitly, and provide aggregates as separate products.

### Data lakes, lakehouses and medallion

#### What is a data lake?

A centralized repository in object storage holding raw and processed data of any format at any scale, with cheap storage and schema on read, used for analytics, data science and as a source for warehouses.

#### What is a data swamp?

A data lake that became unusable: undocumented, ungoverned, duplicated data with unknown quality and ownership. Catalogs, ownership, quality checks, zones and lifecycle policies prevent it.

#### What zones does a data lake usually have?

Landing/raw (as received), cleansed/standardized (validated, typed, deduplicated), curated/consumption (business-ready datasets), plus sandbox zones for exploration and archive zones for cold data.

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

#### Lakehouse or warehouse: how do you decide?

A warehouse (Snowflake, BigQuery, Redshift) is simplest for SQL-centric BI with structured data. A lakehouse fits when you need open formats, multiple engines, large semi-structured or unstructured data, ML and streaming on the same data, or want to avoid copies. Many organizations combine them, and the lines are blurring.

#### What is a data catalog's role in a lakehouse?

It's the control plane: table registry, schemas, permissions, lineage, tags and discovery across engines (Unity Catalog, Glue with Lake Formation, Polaris), turning files into governed tables.

#### What is a "landing zone" versus bronze?

The landing zone holds files exactly as delivered (CSV, JSON, exports) for traceability; bronze is the first table representation of that data with minimal changes plus ingestion metadata, queryable and governed.

#### How many layers should a lakehouse have?

As many as provide clear value: typically raw/bronze, cleaned/silver and consumption/gold, sometimes a landing zone before and a serving or semantic layer after. Extra layers without distinct contracts just add cost.

#### What is compaction, and why do lakehouses need it?

Rewriting many small files into fewer larger ones (and merging delete files), which keeps reads fast and metadata small. Streaming and frequent upserts make it necessary; it can be scheduled or automatic.

#### How do you handle schema evolution in a lakehouse?

Allow additive changes (new nullable columns) automatically in bronze, review and apply changes intentionally in silver and gold with table format features (add, rename, widen), and use contracts and alerts for breaking changes.

#### What is "time travel" useful for architecturally?

Reproducing reports as of a date, auditing, debugging what changed, recovering from bad writes and comparing versions, provided retention policies keep enough history.

### Batch and streaming architectures

#### What is the difference between batch and stream processing?

Batch processes bounded datasets at intervals (hourly, daily) with high throughput and simpler logic; stream processing handles unbounded event flows continuously with low latency, requiring state management, event-time handling and fault tolerance.

#### What is the Lambda architecture?

Nathan Marz's architecture with a batch layer (recomputes accurate views from all history), a speed layer (processes recent data in real time) and a serving layer that merges both. It gives accuracy and low latency but duplicates logic in two code paths.

#### What is the Kappa architecture?

Jay Kreps's simplification: a single stream processing path where everything is a stream; reprocessing is done by replaying the log (Kafka) through a new version of the job. It removes duplicated logic but needs a durable, replayable log and robust streaming.

#### Lambda or Kappa: which is used today?

Pure Lambda is rare because maintaining two code bases is costly. Modern platforms use unified engines (Spark Structured Streaming, Flink, Beam) and table formats that support both batch and streaming on the same tables, closer to Kappa with batch backfills when needed.

#### What is event time versus processing time?

Event time is when something happened at the source; processing time is when the system processes it. Correct analytics usually need event time, because events arrive late and out of order.

#### What are windows in stream processing?

Groupings of events in time for aggregation: tumbling (fixed, non-overlapping), sliding or hopping (overlapping), and session windows (gaps of inactivity define sessions).

#### What is a watermark in streaming?

A threshold of event time up to which the system assumes it has seen all events, allowing windows to close and state to be cleaned; events later than the watermark are dropped or handled separately.

#### What is Apache Kafka's role in data architecture?

A distributed, durable, replayable log of events: it decouples producers from consumers, buffers bursts, enables multiple consumers to read the same data at their own pace, and serves as the backbone for streaming, CDC and event-driven systems.

#### What are Kafka topics, partitions and consumer groups?

A topic is a named stream of records; it's split into partitions (ordered, replicated logs) for parallelism; a consumer group shares partitions among its members so each partition is read by one consumer in the group, giving scalable consumption with ordering per partition.

#### How is ordering guaranteed in Kafka?

Only within a partition. Records with the same key go to the same partition, so per-key ordering is preserved; global ordering across partitions isn't guaranteed.

#### What is a schema registry?

A service that stores versioned schemas (Avro, Protobuf, JSON Schema) for topics and enforces compatibility rules, so producers can't publish breaking changes and consumers can deserialize reliably.

#### What stream processing engines exist?

Apache Flink (low-latency, stateful, event-time), Spark Structured Streaming (micro-batch and continuous, integrated with Spark), Kafka Streams and ksqlDB (library and SQL on Kafka), Apache Beam (portable model, run on Dataflow), and managed services (Kinesis Data Analytics/Managed Flink, Confluent, Databricks).

#### When is real-time actually needed?

When decisions or actions lose value within seconds or minutes: fraud detection, operational alerts, personalization, IoT monitoring, dynamic pricing. Many dashboards don't need it; batch or micro-batch is cheaper and simpler.

#### What is a streaming database or real-time OLAP store?

Systems built to ingest streams and serve low-latency analytical queries on fresh data (Apache Druid, Apache Pinot, ClickHouse, Materialize, RisingWave), used for user-facing analytics and operational dashboards.

#### What is micro-batching?

Processing a stream as a sequence of small batches (seconds to minutes), as Spark Structured Streaming does by default. It simplifies fault tolerance and reuses batch logic, with slightly higher latency than true event-at-a-time processing.

#### What is stateful stream processing?

Processing that keeps information across events (counts per window, session state, joins between streams, deduplication), requiring fault-tolerant state stores and checkpoints; Flink and Spark manage state with snapshots.

#### How do you join streams with reference data?

Broadcast slowly changing reference data to stream processors and refresh it periodically, join against a changelog stream (temporal or versioned tables), or look up a fast store (Redis, DynamoDB) with caching.

#### What is exactly-once processing in Kafka?

Idempotent producers plus transactions that atomically write output records and commit consumer offsets, so a read-process-write cycle's effects happen once even with retries, within Kafka-to-Kafka pipelines.

#### How do you reprocess data in a streaming architecture?

Replay from the log (Kafka retention or tiered storage) into a new version of the job writing to new tables, validate, then switch consumers; or backfill from the lakehouse tables with a batch job using the same logic.

#### What are tiered storage and infinite retention in Kafka?

Offloading older log segments to object storage, so topics can keep long histories cheaply, enabling replays and Kappa-style reprocessing without huge broker disks.

### Microservices and event-driven data

#### How do microservices change data architecture?

Each service owns its data and database (database per service), communicating through APIs and events rather than shared tables. This improves autonomy and scaling but scatters data, requiring integration patterns for analytics and cross-service queries.

#### What is the "database per service" pattern?

Each microservice has a private database that only it accesses; other services use its API or its events. It prevents tight coupling through shared schemas.

#### Why is a shared database an anti-pattern in microservices?

Services become coupled through the schema: one team's change breaks others, deployments must be coordinated, and ownership is unclear, losing the main benefit of microservices.

#### How do you do analytics across microservices?

Capture each service's data (CDC from its database or its domain events) into a lake or warehouse, model it centrally or by domain, and serve analytics there, rather than querying services' databases directly.

#### What is event-driven architecture?

Systems that communicate by producing and reacting to events (facts about something that happened: `OrderPlaced`, `PaymentFailed`) through a broker, rather than synchronous calls, giving loose coupling, scalability and natural audit trails.

#### What is the difference between events, commands and messages?

A command asks someone to do something (`ShipOrder`) and can be rejected; an event states that something happened (`OrderShipped`) and is immutable; message is the generic envelope carrying either.

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

#### What are domain events versus integration events?

Domain events are internal to a service's model; integration events are published contracts for other services and analytics, stable and versioned, deliberately decoupled from internal schemas.

#### What is an API gateway's role in data access?

A single entry point for client requests that routes to services, handles authentication, rate limiting and aggregation. For data products, APIs or GraphQL layers expose curated data to applications.

#### How should events be designed?

Named in the past tense, with a clear schema, an event ID, timestamps (event and publish time), the entity key, a version, and enough data for consumers (fat events) or a reference to fetch details (thin events), evolving compatibly.

#### What are thin versus fat events?

Thin events carry only identifiers and the type of change, so consumers call back for details (coupling, load on the producer); fat (event-carried state transfer) events carry the full state needed, enabling autonomous consumers at the cost of larger messages and schema care.

#### How do you version event schemas?

Use a schema registry with compatibility rules, add optional fields instead of changing meanings, introduce new event types or versions for breaking changes, and keep old versions until all consumers migrate.

#### What is choreography versus orchestration?

In choreography, services react to each other's events without a central coordinator (loose coupling, harder to see the whole flow); in orchestration, a coordinator tells services what to do (clear flow, central dependency). Data pipelines usually use orchestration (Airflow); microservice sagas use either.

### Data mesh and data fabric

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

#### When is data mesh a bad fit?

Small organizations, few domains, low data maturity, or no capacity in domains to own data products. Without platform investment and governance, mesh turns into fragmented, inconsistent data.

#### What is a data fabric?

An architecture that uses metadata, knowledge graphs, automation and virtualization to integrate data across distributed sources and present a unified, governed access layer, emphasizing technology (active metadata) over organization.

#### What is the difference between data mesh and data fabric?

Data mesh is primarily organizational (who owns data, product thinking), with decentralization; data fabric is primarily technological (integration through metadata and automation), often centralized. They can be combined.

#### How do you start a data mesh journey?

Pick one or two motivated domains with clear consumers, build a minimal self-serve platform (templates, catalog, access control, quality), define a few global standards, deliver data products end to end, measure adoption, then expand.

#### How do data products stay interoperable in a mesh?

Through global standards: shared identifiers and reference data, naming and metadata conventions, common formats and access methods, quality metrics, and a central catalog for discovery.

#### What metrics show a data mesh is working?

Time to deliver new data products, number of products with active consumers, quality SLO compliance, reduction in central team tickets, reuse across domains, and consumer satisfaction.

#### What is "active metadata"?

Metadata that drives automation rather than just documentation: tags that apply masking, lineage that triggers alerts on upstream changes, usage stats that suggest deprecation, quality metrics that gate publishing.

### Integration and ingestion

#### What are the main data integration patterns?

Batch ETL/ELT, change data capture, event streaming, API-based integration, data virtualization/federation, file transfers, and reverse ETL to push curated data back to operational tools.

#### What is ELT, and why did it become dominant?

Loading raw data into scalable cloud storage or warehouses first and transforming it there with SQL (often dbt). Cheap storage and elastic compute made it simpler and more flexible than transforming before loading.

#### What is data virtualization?

Querying data where it lives through a logical layer (Denodo, Trino, federated queries) without copying it. It's fast to set up and avoids duplication, but performance, history and source load are limitations.

#### What is reverse ETL?

Syncing modeled data from the warehouse into operational systems (CRM, marketing, support tools) so business teams act on analytics, closing the loop between analysis and operations.

#### What should you consider when ingesting from APIs?

Authentication, pagination, rate limits and retries with backoff, incremental extraction (cursors, updated-since), schema drift, idempotency, storing raw responses for reprocessing, and monitoring for silent API changes.

#### What is a data contract in integration?

An explicit, versioned agreement on a dataset or event's schema, semantics, quality and SLAs between producer and consumers, validated in CI and at runtime, making breaking changes visible before they break pipelines.

#### How do you handle late and out-of-order data in integration?

Use event timestamps, allow lateness windows, design upserts and idempotent writes, reprocess recent partitions, and track data completeness so consumers know when a period is final.

#### How do you choose between CDC, batch extracts and events for a source?

CDC for databases you can't change, needing all changes with low latency and low source impact; batch extracts for small or rarely changing data and sources without log access; events when you control the application and want business-level semantics.

#### What are managed connectors, and when do they make sense?

Services like Fivetran, Airbyte Cloud, Lakeflow Connect or AppFlow that extract from SaaS and databases with maintained connectors and schema handling. They save engineering time for standard sources at a per-volume cost; custom code makes sense for unusual sources or huge volumes.

#### How do you design ingestion for many similar sources?

Metadata-driven pipelines: one generic, tested ingestion component configured per source (connection, tables, keys, schedule) from a configuration table or files, rather than one hand-written pipeline per source.

#### What is a landing contract with external data providers?

An agreement on file formats, naming, delivery schedule, completeness signals (manifest or `_SUCCESS` files), encoding, schema changes notice and error handling, which prevents most file ingestion incidents.

### Governance, metadata and quality

#### What is data governance?

The framework of roles, policies, standards and processes that ensures data is accurate, secure, compliant, understood and used appropriately, including ownership, stewardship, classification, access, quality and lifecycle.

#### What are data owners and data stewards?

Data owners are accountable for a data domain (decisions on access, definitions, quality targets); data stewards handle day-to-day definitions, quality issues and metadata, working with engineers who implement controls.

#### What is metadata management?

Collecting and managing technical, business and operational metadata (schemas, definitions, lineage, quality, usage) to enable discovery, impact analysis, governance and automation; "active metadata" uses it to drive actions.

#### What is data lineage, and how is it captured?

The flow of data from sources through transformations to consumers. It's captured by parsing SQL and jobs (dbt, Unity Catalog, OpenLineage events from Airflow and Spark), and shown at table and column level for impact analysis and audits.

#### What is OpenLineage?

An open standard for lineage events emitted by orchestrators and engines (Airflow, Spark, dbt, Flink) describing jobs, runs and input/output datasets, collected by backends like Marquez or catalogs.

#### What is data classification?

Labeling data by sensitivity (public, internal, confidential, restricted) and type (PII, financial, health), often automated by scanners, to drive access policies, masking, retention and compliance.

#### What is master data management (MDM)?

Creating a single, trusted record for core entities (customer, product, supplier) across systems through matching, merging and survivorship rules, distributed to operational and analytical systems.

#### What is reference data?

Relatively static code sets and classifications used across systems (country codes, currencies, industry codes, status values); managing them centrally avoids inconsistent codes.

#### How do you build data quality into an architecture?

Define quality dimensions and SLAs per data product, validate at ingestion (schemas, contracts), test transformations (uniqueness, integrity, business rules), gate publishing, monitor anomalies and freshness, quarantine bad records, and assign owners to resolve issues.

#### How do you measure data governance maturity?

By coverage of ownership, documented definitions, classification of sensitive data, access policies as code, lineage, quality SLOs, incident processes, and how often consumers find and trust data without asking around.

#### What is a business glossary?

A curated list of business terms and their agreed definitions (active customer, net revenue, churn), linked to datasets and metrics in the catalog, which aligns teams on meaning.

#### How do you prevent duplicate datasets?

Make existing datasets discoverable (catalog, search), certify authoritative ones, require ownership and review for new published datasets, monitor usage, and deprecate copies.

### Security and compliance

#### What are the layers of data security?

Identity and access management (authentication, least-privilege authorization), network isolation, encryption at rest and in transit, key management, data masking and tokenization, row and column-level security, auditing and monitoring, and secure development practices.

#### What is the difference between RBAC and ABAC?

Role-based access control grants permissions to roles assigned to users; attribute-based access control evaluates attributes of users, resources and context (department, data classification, location) in policies, scaling better for fine-grained rules (for example tag-based policies).

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

#### What is zero trust in data platforms?

Never trusting by network location: every access is authenticated, authorized with least privilege and audited, with short-lived credentials, workload identities and continuous verification.

#### How do you manage secrets in data platforms?

Store them in a secrets manager (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault, Databricks secret scopes), prefer workload identities and short-lived credentials over static keys, rotate automatically, and never commit them to Git.

#### What is data loss prevention (DLP)?

Tools and policies that detect and block sensitive data from leaving approved boundaries (emails, exports, public buckets), often by scanning content for patterns like card numbers or national IDs.

#### How do you secure data sharing with external partners?

Share curated, minimal datasets through governed mechanisms (Delta Sharing, Snowflake shares, presigned access with expiry) rather than file dumps, apply row and column restrictions, contractually define usage, and audit access.

### Reliability, operations and cost

#### What are SLAs, SLOs and SLIs for data?

SLIs are measured indicators (freshness, completeness, pipeline success rate); SLOs are targets for them (data ready by 7 a.m. 99% of days); SLAs are commitments to consumers with consequences. They make data reliability measurable.

#### What is data observability?

Monitoring freshness, volume, schema, distribution and lineage of data (not just job status) to detect incidents quickly and find their root cause, often with automated anomaly detection.

#### How do you design pipelines for failure?

Assume failures: idempotent and restartable steps, retries with backoff for transient errors, checkpoints for streams, dead-letter queues for bad records, alerts with runbooks, and the ability to backfill specific periods.

#### What is a dead-letter queue?

A place where messages or records that can't be processed (invalid format, failed validation) are sent with error information, so the pipeline continues and the failures can be inspected and replayed later.

#### What are RPO and RTO?

Recovery point objective: how much data loss is acceptable (time between last recoverable state and failure). Recovery time objective: how long recovery can take. They drive backup frequency, replication and disaster recovery design.

#### What is FinOps for data platforms?

The practice of managing cloud data costs collaboratively: visibility (tagging, cost per pipeline and team), optimization (right-sizing, auto-suspend, storage tiers, query tuning, incremental processing) and governance (budgets, alerts, accountability).

#### What are the biggest cost drivers in data platforms?

Compute for transformations and queries (especially always-on clusters and full recomputes), inefficient queries on large data, data duplication across layers and tools, egress and cross-region transfer, and unused data kept forever.

#### How do you make a platform cost-efficient by design?

Incremental processing, partitioning and clustering for pruning, serverless or auto-scaling compute with auto-suspend, tiered storage and retention, avoiding unnecessary copies, choosing latency appropriate to the business need, and making costs visible per team.

#### What is infrastructure as code's role in data architecture?

Defining platforms (storage, compute, permissions, catalogs, jobs) declaratively in code (Terraform, CloudFormation, Bicep, bundles) so environments are reproducible, reviewed and auditable, and drift is detectable.

#### What is a data incident, and how do you manage it?

Any event where data is wrong, late or unavailable for consumers. Manage it like software incidents: detect, assess impact, communicate to consumers, mitigate (pause publishing, roll back), fix the root cause, and write a blameless postmortem with actions.

#### What is capacity planning for data platforms?

Forecasting growth of data volume, users and workloads to ensure storage, compute and concurrency remain adequate and budgets are prepared, using trends from monitoring and business plans.

#### How do you set retention policies architecturally?

Classify datasets by legal and business needs, define retention per layer (raw might be kept longer for reprocessing, or shorter for privacy), implement with lifecycle rules, partition drops and table format retention, and document exceptions.

### AI and ML data architecture

#### What does an ML platform need from the data architecture?

Reliable, versioned training data, point-in-time correct features, feature reuse between training and serving, lineage from data to models, experiment tracking, model registry, and monitoring of data and prediction drift.

#### What is a feature store?

A system that stores, documents and serves ML features consistently for training (offline, historical, point-in-time correct) and inference (online, low latency), avoiding training-serving skew and duplicated feature engineering.

#### What is point-in-time correctness?

When building training data, features must use only information available at the time of each label's event, avoiding leakage of future data; feature stores join features as of each event timestamp.

#### What is training-serving skew?

Differences between how features are computed for training and for inference (different code, data sources or timing), which degrade model performance in production. Shared feature definitions and feature stores reduce it.

#### What is a vector database, and where does it fit?

A store optimized for similarity search over embeddings (pgvector, OpenSearch, Pinecone, Weaviate, Databricks Vector Search), used for semantic search, recommendations and retrieval-augmented generation.

#### What is the data architecture of a RAG application?

Ingest documents, split them into chunks, compute embeddings, store them with metadata in a vector index, retrieve relevant chunks at query time (often combined with keyword search and filters by permissions), and pass them to an LLM, with pipelines to keep the index fresh and governed.

#### How do governance concerns change with AI?

You must track which data trained which models, respect permissions in retrieval (users shouldn't see documents through an LLM they couldn't access directly), manage PII in prompts and training data, and evaluate outputs; catalogs increasingly govern models and features alongside tables.

#### What is MLOps?

Practices and tooling to develop, deploy and operate ML models reliably: versioned data and code, reproducible training pipelines, model registry, automated testing and deployment, monitoring of performance and drift, and retraining.

#### What is data drift versus concept drift?

Data drift is a change in the input data distribution (customers' ages shift); concept drift is a change in the relationship between inputs and the target (what predicts churn changes). Both require monitoring and possibly retraining.

#### How should unstructured data be managed for AI?

Store it in object storage with metadata in a catalog (volumes), track lineage from documents to chunks and embeddings, apply access controls and classification, and build pipelines that update indexes when documents change or are deleted.

### Cloud and reference architectures

#### What does a typical AWS data architecture look like?

Sources ingested with DMS, Kinesis/MSK, AppFlow or Glue into S3; Glue Data Catalog and Lake Formation for governance; processing with Glue, EMR or Databricks; Iceberg or Delta tables; Athena and Redshift for SQL; QuickSight for BI; SageMaker for ML; Step Functions, MWAA or EventBridge for orchestration; all defined with CloudFormation, CDK or Terraform.

#### What does a typical Azure data architecture look like?

Ingestion with Data Factory or Fabric pipelines and Event Hubs into ADLS Gen2/OneLake; processing with Databricks or Fabric Spark; Delta tables; Synapse/Fabric warehouses or Databricks SQL; Power BI; Purview for governance; Entra ID for identity.

#### What does a typical Google Cloud data architecture look like?

Ingestion with Pub/Sub, Datastream (CDC) and Dataflow into Cloud Storage and BigQuery; processing with Dataflow, Dataproc or BigQuery SQL (often with dbt or Dataform); Dataplex for governance; Looker for BI; Vertex AI for ML.

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

### Scenarios

#### Design a data platform for a mid-size e-commerce company.

Ingest the orders database with CDC, web events through a stream (Kafka or Kinesis), and SaaS tools (CRM, marketing) with connectors into object storage; organize medallion layers with Iceberg or Delta tables in a catalog; transform with dbt or Spark into conformed dimensions and facts; serve BI from a warehouse or lakehouse SQL engine with a semantic layer; add reverse ETL for marketing segments; orchestrate with Airflow or native jobs; enforce governance, quality tests, observability and cost tagging; define everything as code with CI/CD.

#### A company has ten departments each building their own reports with conflicting numbers. What do you propose?

Identify the core business processes and metrics, create conformed dimensions and certified facts owned by accountable teams, implement a semantic layer for metric definitions, establish data ownership and stewardship, retire duplicated logic gradually, and communicate a catalog of certified datasets.

#### You must add real-time fraud scoring to a batch-oriented platform. How?

Stream transactions from the source (CDC or events) into a broker, compute features with a stream processor using an online feature store (shared definitions with batch training), call the model for scoring in milliseconds, write decisions back as events, and land everything in the lakehouse for analysis and retraining.

#### Microservices teams complain the data team keeps breaking when they change their databases. What do you change?

Stop reading internal tables directly: agree data contracts, have services publish integration events (via an outbox) or curated CDC views, validate contracts in the services' CI, version breaking changes, and give domains ownership of their published data products.

#### Your data lake has become a swamp. How do you recover it?

Inventory datasets with usage and owners, define zones and naming standards, register valuable data in a catalog with descriptions and tags, add quality checks, convert key datasets to table formats, archive or delete unused data with lifecycle policies, and make ownership mandatory for new datasets.

#### How do you explain data architecture to a non-technical stakeholder?

It's the city plan for the company's data: where data comes from, where it's stored, how it flows and is cleaned, who's responsible for it, and the rules that keep it safe and trustworthy, so teams can build on it without chaos.

#### A startup asks you to design its first data platform. What do you recommend?

Keep it simple and managed: a cloud warehouse or lakehouse service, managed connectors for SaaS sources, CDC or replicas for the product database, dbt for transformations with tests, one orchestrator, a BI tool with a semantic layer, basic governance and cost alerts, all as code. Add streaming, mesh or custom components only when needs appear.

#### Your company acquired another one with a different cloud and platform. How do you integrate data?

Start with the questions leadership needs answered, map key entities and metrics, replicate the necessary data into the primary platform with CDC or exports (or share it via open formats), build conformed dimensions with master data matching, and plan longer-term consolidation of platforms based on cost and capabilities.

#### Leadership wants "real-time everything". How do you respond?

Ask which decisions change with fresher data and what latency each needs, estimate costs and complexity for each tier (seconds, minutes, hours), deliver real time where the business value justifies it, and keep the rest in cheaper batch or micro-batch.
