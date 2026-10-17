## Data Architecture Patterns: Kimball, Microservices, Medallion and More

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Data architecture patterns: from Kimball to the lakehouse](../../images/data_architecture_patterns_title_img.png)

*Technical article*

## There is no best architecture

Every few years a new data architecture is announced as the one that replaces all the others. Inmon was replaced by Kimball, the warehouse by the data lake, the lake by the lakehouse, the central team by the data mesh. In practice, none of them disappeared. Most platforms I've seen mix three or four of these ideas, sometimes on purpose, often by accident.

The useful way to think about them is as answers to specific questions. How do I integrate twenty systems that describe the same customer differently? How do I make numbers easy for analysts? How do I keep an audit trail of every change? How do I get data out of thirty microservices without coupling to their databases? How do I serve both a nightly report and a fraud model that needs an answer in 200 milliseconds? Each pattern below is a good answer to one of these questions and a poor answer to others.

This article walks through the patterns I meet most often, what each one optimizes, where it breaks down, and how they combine. I'll use my own [EU company registry lakehouse](../projects/eu-company-registry.html) as a concrete example where it helps, including one decision I reversed.

## Inmon: integrate first

Bill Inmon's Corporate Information Factory puts an **enterprise data warehouse in third normal form** at the center. Every source is integrated into one normalized, subject-oriented model (customer, account, product) that is the single version of the truth. Departmental data marts are then derived from it.

```
sources ──► staging ──► enterprise warehouse (3NF, integrated, historized) ──► dependent data marts ──► BI
```

**What it optimizes:** consistency. Because every mart comes from the same integrated core, finance and sales can't disagree about what a customer is.

**Where it hurts:** time to value. Designing an enterprise-wide normalized model takes months before the first report ships, and every new source means changing a central model that many teams depend on. Normalized models are also hard for analysts to query directly.

You still see Inmon-style cores in banks and insurers, and its central idea survives in every architecture that has an "integration" or "silver" layer.

## Kimball: model for the questions

Ralph Kimball took the opposite route: start from **business processes** (order taking, invoicing, shipments) and build **dimensional models** that analysts can understand. A fact table records measurements at a declared grain, surrounded by dimension tables with descriptive context. That's the star schema.

```sql
-- One row per order line (the grain), joined to conformed dimensions
SELECT d.year_month, c.segment, p.category, SUM(f.net_amount) AS revenue
FROM fct_order_lines f
JOIN dim_date d     ON f.order_date_key = d.date_key
JOIN dim_customer c ON f.customer_key   = c.customer_key
JOIN dim_product p  ON f.product_key    = p.product_key
WHERE d.year = 2026
GROUP BY d.year_month, c.segment, p.category;
```

The marts are integrated through **conformed dimensions**: one `dim_customer` and one `dim_date` shared by every fact table, planned with the bus matrix. History lives in **slowly changing dimensions**, usually Type 2: when a customer changes segment, the old row is closed and a new version inserted, so last year's sales stay attributed to last year's segment.

**What it optimizes:** usability and query performance. Star schemas are easy to explain, BI tools understand them, and columnar engines run them fast.

**Where it hurts:** integration of messy, overlapping sources. Kimball assumes you can conform dimensions; when twenty systems disagree about customers, that conformance work has to happen somewhere, and the dimensional model isn't the best place to keep the raw, auditable history of every source.

Kimball is not outdated. Almost every "gold" layer I've seen in a lakehouse is a set of star schemas, even when nobody calls them that. My registry project's gold layer is a Kimball star: a company dimension, an industry dimension and aggregate tables, with explicit country coverage.

## Data Vault: integrate and audit at scale

Dan Linstedt's Data Vault targets the integration layer when there are many changing sources and strong audit requirements. It splits the model into three kinds of tables:

- **Hubs** store unique business keys (a customer number) with load date and record source.
- **Links** store relationships between hubs (customer placed order).
- **Satellites** store descriptive attributes and their history, one satellite per source or rate of change.

Everything is insert-only, keyed by hashes so loads can run in parallel, and fully traceable to the source. Marts for consumption are built on top, often as Kimball stars, sometimes with helper point-in-time and bridge tables.

**What it optimizes:** agility and auditability. Adding a source means adding satellites, not redesigning tables. Regulators can see exactly what each system said and when.

**Where it hurts:** query complexity and cost. A simple question becomes a join across hubs, links and several satellites, so nobody queries the vault directly; you always need a presentation layer. Without automation (dbt packages, code generators) the number of tables grows quickly.

I worked on a Data Vault platform at Corum L'Épargne, and the first version of my registry lakehouse was a Data Vault 2.0 model too. I replaced it on purpose, and the reasoning is a good example of choosing a pattern from the problem rather than from habit:

> Data Vault pays off when many systems describe the same business keys. In the registry project no key is ever shared: a French SIRET and a UK company number never refer to the same company. Every hub was a renamed copy of one register's ID column, and every query became a five or six-way join, each shuffle billed on serverless compute. The registers publish full snapshots, so history is exactly what an SCD Type 2 merge produces, and Delta Lake already gives an audit trail (time travel, `RESTORE`, Change Data Feed).

I kept the Data Vault ideas that earned their place: hash keys, a `hash_diff` for change detection, record source and lineage columns, and insert-only raw history in bronze. That's often the right outcome: borrow the techniques, skip the full methodology when its main benefit doesn't apply.

## Data lakes and the lakehouse

The data lake answered a different question: where do we put everything, cheaply, including data we don't understand yet? Object storage (S3, ADLS, GCS) holds raw files of any format at a fraction of warehouse cost, with schema applied on read.

Lakes delivered cheap storage and flexibility, and also a lot of **data swamps**: no transactions (readers saw half-written data), no schema enforcement, slow queries over millions of small files, no reliable updates or deletes (a real problem for GDPR), and weak governance.

The **lakehouse** fixes this with open table formats, **Delta Lake, Apache Iceberg and Apache Hudi**, which add a transaction log on top of Parquet files: ACID writes, schema enforcement and evolution, time travel, `MERGE`, `UPDATE` and `DELETE`. A catalog (Unity Catalog, AWS Glue with Lake Formation, Polaris) turns files into governed tables, and several engines (Spark, Databricks SQL, Snowflake, Athena, Trino) can read the same data.

**What it optimizes:** one copy of the data for BI, data science and machine learning, in open formats, with warehouse-like guarantees.

**Where it hurts:** you still need to design the layers, maintain tables (compaction, vacuum, clustering) and govern access. A lakehouse without modeling discipline is just a faster swamp.

## Medallion: layers of refinement

The medallion architecture is the lakehouse's layering convention:

| Layer | Contains | Typical rules |
|---|---|---|
| **Bronze** | Raw data as received, plus load metadata | Append-only, minimal transformation, keep everything replayable |
| **Silver** | Cleaned, typed, deduplicated, conformed and historized entities | Data quality checks, quarantine, SCD Type 2, one trusted version of each entity |
| **Gold** | Business-ready models: star schemas, aggregates, feature tables | Business definitions applied, optimized for reading |

It's important to see what medallion is and isn't. It's a **convention for layers of refinement**, not a modeling technique. Silver can be normalized, Data Vault or just clean entity tables; gold is usually Kimball. Medallion tells you where things go, not how to model them.

In my registry lakehouse the layers look like this:

```
landing (S3, raw files by ingest_date)
   │  schema-drift check against a contract
   ▼
bronze  every column as STRING + lineage, append-only, one table per register
   │  per-source parsing, data-quality rules, quarantine
   ▼
silver  one canonical company model, SCD Type 2 MERGE per country and snapshot
   │  dimensional modeling
   ▼
gold    Kimball star (company and industry dimensions) + aggregate insight tables
```

Two choices are worth copying. Bronze stores every column as text, so a bad value can never fail a load and silver can always be rerun with better parsing. And silver enforces its own invariants with constraints (valid statuses, `valid_to >= valid_from`, current rows open), so a code regression can't write an invalid state.

The mistakes I see most often with medallion: treating three layers as mandatory copies even when a layer adds nothing; letting dashboards read bronze or silver directly; putting business logic in bronze; copying entire tables between layers on every run instead of processing incrementally; and having no explicit contract for what each layer guarantees.

## Microservices and data

Microservices changed data architecture from the other side. Each service owns its database (**database per service**) and exposes data through APIs and events, never through shared tables. That's good for autonomy and deployment speed. It's a challenge for analytics, because the data the business wants to analyze is now spread across dozens of private databases.

The tempting shortcut is to point the warehouse at each service's database and read its tables. It works for a month, then a team renames a column and the nightly pipeline breaks. Internal schemas are implementation details; reading them couples the data platform to every service's internals.

The patterns that work:

- **Change data capture (CDC)** reads each database's transaction log (with Debezium, AWS DMS or a managed connector) and streams inserts, updates and deletes into Kafka or the lakehouse, without touching the service's code. It's the fastest way to get data out of existing systems, but it still exposes internal schemas unless a contract is agreed.
- **Integration events** are business facts (`OrderPlaced`, `PaymentFailed`) that services publish deliberately as versioned contracts, separate from their internal domain model. They're more stable than CDC and carry business meaning.
- The **transactional outbox** solves the dual-write problem: if a service writes to its database and then publishes an event, one can succeed and the other fail. Instead, the service writes the event into an outbox table in the same transaction, and CDC publishes the outbox rows to the broker.

```
┌─────────────── order service ───────────────┐
│  BEGIN                                      │
│    INSERT INTO orders ...                   │
│    INSERT INTO outbox (event: OrderPlaced)  │
│  COMMIT                                     │
└───────────────────┬─────────────────────────┘
                    │ CDC reads outbox rows
                    ▼
              Kafka topic: orders.events ──► other services
                    │
                    ▼
              lakehouse bronze ──► silver ──► gold
```

Two related patterns appear in event-driven systems. **Event sourcing** stores an entity as the sequence of events that changed it and rebuilds state by replaying them, which gives a perfect audit log but makes queries harder. **CQRS** separates the write model from read models that are updated asynchronously from events, so reads and writes scale independently. For transactions spanning several services, **sagas** replace distributed two-phase commits with a sequence of local transactions and compensating actions.

For a data engineer, the practical rule is simple: **consume published contracts (events or curated CDC views), not internal tables**, and validate those contracts in the producers' CI so breaking changes fail before they ship.

## Lambda and Kappa: batch and streaming

When low latency entered the picture, two architectures competed.

The **Lambda architecture** runs two paths: a batch layer that recomputes accurate views from all history, and a speed layer that processes recent events in real time, with a serving layer merging both. It gives accuracy and freshness, at the cost of writing and maintaining the same logic twice.

The **Kappa architecture** keeps one path: everything is a stream, stored in a durable, replayable log (Kafka). To fix a bug or change logic, you replay the log through a new version of the job. One codebase, but you need solid stream processing and long retention.

Today pure Lambda is rare. Unified engines (Spark Structured Streaming, Flink, Apache Beam) and table formats that accept both streaming and batch writes on the same tables make a Kappa-like design practical, with batch backfills from the lakehouse when needed. Before choosing either, ask the question that saves the most money: **which decisions actually change if the data is seconds old instead of hours old?** Fraud detection and operational alerts, yes. Most dashboards, no.

## Data mesh and data fabric

**Data mesh**, proposed by Zhamak Dehghani, is mainly an organizational answer. Central data teams become bottlenecks between many source domains and many consumers, so mesh moves ownership to the domains, with four principles: domain ownership, **data as a product** (owned, documented, with quality guarantees and SLAs), a **self-serve platform**, and **federated computational governance** (global rules enforced automatically by the platform).

It works when domains have the capacity and motivation to own data products and when there's a real platform underneath. Without that, mesh produces fragmented, inconsistent data with a fashionable name. Many organizations adopt the most useful parts, data products with owners and contracts, without full decentralization.

**Data fabric** is the technological counterpart: active metadata, knowledge graphs, automation and virtualization to integrate distributed data behind a governed access layer. Mesh asks "who owns this?"; fabric asks "how do we connect it all automatically?". They can coexist.

## How the patterns fit together

In a modern platform these patterns are layers of one design, not competitors. A typical combination looks like this:

```
 operational sources          ingestion                 lakehouse (medallion)                 consumption
 ───────────────────   ─────────────────────────   ─────────────────────────────────   ─────────────────────
 microservices DBs ──► CDC / outbox events ─┐
 SaaS applications ──► managed connectors ──┼──►  bronze  raw, append-only
 files and APIs   ──► batch extracts ───────┘         │
                                                      ▼
                                              silver  integrated & historized   ──► ML features
                                                      │  (normalized, Data Vault
                                                      │   or clean SCD2 entities)
                                                      ▼
                                              gold    Kimball stars, aggregates ──► BI, semantic layer,
                                                                                    reverse ETL, APIs
          governance across all layers: catalog, lineage, contracts, quality checks, access policies
```

Microservice patterns govern how data leaves the applications. Medallion organizes the lakehouse. Inmon's integration idea or Data Vault lives in silver. Kimball lives in gold. Streaming paths feed bronze continuously when latency matters. Mesh decides who owns each data product along the way.

## How to choose

Start from constraints, not from the newest diagram. These questions narrow the options quickly:

| If your situation is… | Lean towards… |
|---|---|
| Few sources, analysts need numbers soon | Kimball marts on a cloud warehouse or lakehouse; skip heavy integration layers |
| Many overlapping sources, strong audit or regulatory needs | Data Vault (or a normalized core) in silver, Kimball in gold |
| Mixed structured, semi-structured and unstructured data, ML and BI on the same data | Lakehouse with open table formats and medallion layers |
| Data comes from microservices you don't control | Integration events and outbox where possible, CDC elsewhere, contracts in CI |
| Decisions lose value within seconds | A streaming path (Kafka plus Flink or Spark streaming) feeding the same tables as batch |
| A central team is the bottleneck and domains are mature | Data products with owners and contracts; full mesh only with a real platform |
| Small team, limited budget | The simplest managed stack that works: warehouse, dbt, one orchestrator, tests |

A few principles hold whatever you choose:

- **Keep raw data immutable** so you can reprocess when logic or bugs change.
- **Model consumption layers for the questions people ask**, at the most atomic grain you can afford.
- **Make contracts explicit** between producers, layers and consumers.
- **Write the decision down.** A one-page architecture decision record with the context, the options and why you chose one is what lets you reverse a decision calmly later, as I did with Data Vault.

The best architecture is the one your team can explain, operate and change. Patterns are tools; the skill is knowing which problem each one solves.
