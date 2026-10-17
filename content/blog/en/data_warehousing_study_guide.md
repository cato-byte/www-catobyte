## Data Warehousing Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Data warehousing study guide: about 200 questions](../../images/data_warehousing_study_guide_title_img.png)

About 200 interview-style questions on data warehousing: core concepts, dimensional modeling with facts and dimensions, slowly changing dimensions, loading patterns, data quality, warehouse architectures and engines, performance, cloud warehouses, BI and the semantic layer, with SQL examples. The answers are tool-agnostic where possible, with notes for Snowflake, Redshift, BigQuery and Databricks. Open a question to see its answer, or use the filter to search the whole guide.

<!-- QA -->

### Core concepts

#### What is a data warehouse?

A central repository of integrated, historical data from many sources, organized for analysis and reporting rather than for transactions. Bill Inmon's classic definition: subject-oriented, integrated, time-variant and non-volatile.

#### What do "subject-oriented, integrated, time-variant and non-volatile" mean?

Subject-oriented: organized around business subjects (customers, sales, products) rather than applications. Integrated: consistent names, codes and units across sources. Time-variant: keeps history so you can analyze change over time. Non-volatile: data is loaded and read, not updated in place by transactions.

#### What is the difference between OLTP and OLAP?

OLTP (online transaction processing) systems run the business: many small, concurrent reads and writes, normalized schemas, current state. OLAP (online analytical processing) systems analyze the business: large scans and aggregations over history, denormalized or dimensional schemas, mostly reads.

#### Why not run analytics directly on the operational database?

Analytical queries are heavy and would slow the application; operational schemas are normalized and hard to query; data from different systems must be combined and cleaned; history is often overwritten in OLTP systems; and access control for analysts differs from application access.

#### What is a data mart?

A subset of the warehouse focused on one business area or department (sales, finance, marketing), often a set of star schemas built for a specific group of users.

#### What is the difference between a dependent and an independent data mart?

A dependent data mart is built from the enterprise warehouse, so it shares definitions with other marts. An independent mart is fed directly from sources, which is faster to build but leads to inconsistent numbers across departments.

#### What is an operational data store (ODS)?

An integrated, near-real-time store of current operational data from several systems, used for operational reporting and as a staging point. Unlike a warehouse, it holds little history and is updated frequently.

#### What is the difference between a data warehouse and a data lake?

A warehouse stores structured, modeled, curated data with a schema defined on write, optimized for SQL analytics. A data lake stores raw data of any format (structured, semi-structured, unstructured) cheaply in object storage, with schema on read, supporting data science and future uses.

#### What is a lakehouse?

An architecture that adds warehouse capabilities (ACID transactions, schemas, governance, fast SQL) on top of data lake storage using open table formats like Delta Lake and Iceberg, so one copy of data serves BI, data science and ML.

#### What are the typical layers of a data warehouse?

Staging (raw copies of source data), an integration or core layer (cleaned, conformed, historized data; normalized or Data Vault), and a presentation layer (dimensional marts for BI). Modern stacks call them raw/bronze, staging/silver and marts/gold.

#### What is the role of the staging area?

A landing zone where source extracts are stored with minimal changes, so loads can be restarted, reprocessed and audited without hitting sources again, and transformations don't run against operational systems.

#### What is metadata in a warehouse?

Data about the data: technical metadata (schemas, types, lineage, load times), business metadata (definitions, owners, glossary) and operational metadata (job runs, row counts, errors). It powers catalogs, impact analysis and trust.

#### What is a single source of truth?

The goal that each business metric and entity has one agreed definition and one authoritative dataset, so reports across departments agree. Conformed dimensions, a semantic layer and governance support it.

#### What is the difference between ETL and ELT?

ETL extracts data, transforms it in a separate engine, then loads it into the warehouse. ELT loads raw data into the warehouse first and transforms it there with SQL (often with dbt), using the warehouse's scalable compute. Cloud warehouses made ELT the default.

#### Who are the main users of a data warehouse?

Business analysts and BI developers (reports, dashboards), data scientists (training data, exploration), finance and operations teams (regulatory and management reporting), executives (KPIs), and increasingly applications and AI agents through APIs and semantic layers.

#### What is a data warehouse appliance?

A pre-integrated hardware and software system for warehousing (Teradata, Netezza, Exadata), sold as a box. Cloud warehouses have largely replaced appliances with elastic services.

#### What are the main components of a warehouse architecture?

Source systems, ingestion and ETL/ELT tools, storage layers (staging, core, marts), the query engine, a semantic or metrics layer, BI and analytics tools, orchestration, data quality and observability, catalog and governance, and security.

#### What is the difference between a data warehouse and a database?

A database is any organized data store; a data warehouse is a specific use of database technology designed for integrated, historical, analytical data, usually with columnar storage and dimensional or layered models.

#### What is latency in a warehouse context?

The delay between an event in a source system and its availability in reports: daily batch (hours), micro-batch (minutes) or streaming (seconds). The right latency depends on business decisions, not technology.

#### What are SLAs for a data warehouse?

Commitments such as "sales mart refreshed by 7 a.m. local time on business days" or "99% of loads succeed", with monitoring and communication when breached. They turn pipelines into products consumers can rely on.

### Dimensional modeling basics

#### What is dimensional modeling?

Ralph Kimball's technique for designing analytical schemas around business processes: facts (measurements of events) surrounded by dimensions (descriptive context). It favors understandability and query performance over normalization.

#### What are Kimball's four steps of dimensional design?

1) Select the business process (for example order taking). 2) Declare the grain (what one fact row represents). 3) Identify the dimensions (who, what, where, when, why, how). 4) Identify the facts (numeric measurements at that grain).

#### What is the grain of a fact table?

The precise definition of what a single row represents, for example "one row per order line" or "one row per account per day". It must be declared before choosing dimensions and facts, and all rows must share the same grain.

#### Why should you model at the most atomic grain possible?

Atomic data can answer any question by aggregating, including questions not anticipated; aggregated facts can't be broken down. Aggregates can be added later for performance.

#### What is a fact table?

A table of measurements from a business process, with foreign keys to dimensions and numeric facts (quantity, amount, duration). It is usually narrow and very long.

#### What is a dimension table?

A table describing the context of facts: attributes used to filter, group and label (customer name, segment, city; product category, brand; date, month, holiday flag). It is usually wide and relatively short.

#### What is a star schema?

A fact table in the center joined directly to denormalized dimension tables, forming a star. It's simple to understand, needs few joins and performs well in BI tools and columnar engines.

```sql
SELECT d.year_month, p.category, SUM(f.net_amount) AS revenue
FROM fct_order_lines f
JOIN dim_date d    ON f.order_date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
WHERE d.year = 2026
GROUP BY d.year_month, p.category;
```

#### What is a snowflake schema?

A star schema where dimensions are normalized into several related tables (product → subcategory → category). It saves some storage and avoids redundancy but adds joins and complexity; Kimball generally recommends flattening dimensions.

#### What is a surrogate key?

A meaningless integer (or hash) key generated in the warehouse to identify a dimension row, independent of source system keys. It enables history (several rows per natural key), integration of multiple sources and protection from source key changes.

#### What is a natural (business) key?

The identifier from the source system or business (customer number, SKU, IBAN). It's kept as an attribute in the dimension, alongside the surrogate key, to trace rows back to sources.

#### Why use surrogate keys instead of natural keys in facts?

Natural keys can change, be reused, collide across sources, or be long strings. Surrogate keys support SCD Type 2 history (facts point to the version valid at the time), keep facts compact and allow special rows like "unknown".

#### What is a conformed dimension?

A dimension shared with the same keys, attributes and meaning across several fact tables and marts (one `dim_customer`, one `dim_date`), so metrics from different processes can be compared and combined (drill-across).

#### What is the enterprise data warehouse bus matrix?

A planning grid with business processes as rows and conformed dimensions as columns, marking which dimensions each process uses. It guides incremental development of marts that integrate through conformed dimensions.

#### What is the date dimension, and why is it important?

A dimension with one row per day and attributes like day of week, month, quarter, fiscal periods, holidays and working-day flags. It makes time analysis easy and consistent and avoids complex date logic in every query.

#### Why is the date dimension key often in YYYYMMDD format?

An integer like `20261015` is readable, sorts correctly, makes partition pruning intuitive, and can be derived from a date without a lookup; it's a common exception to meaningless surrogate keys.

#### What questions help identify dimensions?

Who (customer, employee), what (product, service), where (store, region, channel), when (date, time), why (promotion, reason code) and how (payment method, shipping mode), as they appear in the business process's events.

#### Should a fact table have foreign key constraints?

Logically yes: every fact must reference an existing dimension row (or the unknown member). Physically, many warehouses don't enforce constraints for load performance, so referential integrity is checked with tests instead.

#### What is drill-across?

Combining measures from different fact tables (sales and returns) in one report by querying each separately at a common grain of conformed dimensions and joining the results, rather than joining facts directly.

#### Why shouldn't you join two fact tables directly?

Their grains usually differ, and direct joins produce fan-outs and double counting. Aggregate each fact to the common dimensional grain first, then combine.

#### What is a time-of-day dimension?

A separate dimension with one row per minute or second of the day (hour, minute, day part), used when time-of-day analysis matters, keeping the date dimension small.

#### How do you name tables and columns in a dimensional model?

Consistently and in business language: `fct_` and `dim_` prefixes (or `fact_`/`dim_`), singular nouns, `_key` for surrogate keys, `_id` for natural keys, explicit units (`amount_eur`), and no source system jargon in presentation layers.

### Facts in depth

#### What are the three types of fact tables?

Transaction facts (one row per event, like an order line), periodic snapshot facts (one row per entity per period, like account balance per day) and accumulating snapshot facts (one row per process instance updated as it moves through milestones, like an order from placement to delivery).

#### When do you use a periodic snapshot fact table?

To measure levels or states at regular intervals (inventory, balances, subscriptions active per month), where summing transactions would be expensive or where the state isn't derivable from events.

#### What is an accumulating snapshot fact table?

A fact table with one row per instance of a process with a defined start and end (order fulfillment, loan application, claim), with multiple date keys for milestones and lag measures between them; rows are updated as milestones occur.

#### What is a factless fact table?

A fact table with only dimension keys and no numeric measures, recording that an event happened (student attended class) or coverage (which products were on promotion in which stores), counted with `COUNT(*)`.

#### What are additive, semi-additive and non-additive facts?

Additive facts can be summed across all dimensions (sales amount). Semi-additive facts can be summed across some dimensions but not time (account balance: sum across accounts, average or last over time). Non-additive facts can't be summed (ratios, percentages, unit prices); store their components instead.

#### How should you store ratios like margin percentage?

Store the additive components (revenue and cost) in the fact table and compute the ratio at query time (`SUM(revenue - cost) / SUM(revenue)`), because averaging percentages gives wrong results.

#### What is a degenerate dimension?

A dimension key stored in the fact table without its own dimension table, typically a transaction identifier like an order number or invoice number, used for grouping lines and drill-through.

#### How do you handle facts with different grains?

Put them in separate fact tables; mixing grains (order header amounts and order line amounts in one table) causes double counting. Allocate header-level values to lines only if a business rule supports it.

#### What is a fact table's primary key?

Often the combination of its dimension keys plus degenerate dimensions at the declared grain, or a surrogate fact key for convenience. Enforcing uniqueness at the grain with a test is essential.

#### What are aggregate fact tables?

Pre-summarized versions of atomic facts at a coarser grain (sales by month and category) that speed up common queries. They must be kept consistent with the atomic table, and BI tools or semantic layers can route queries to them.

#### What is a consolidated fact table?

A fact table combining facts from several processes at the same grain (actual and budget amounts by month, account and cost center), convenient for comparisons like actual versus plan.

#### What are late-arriving facts?

Fact rows that arrive after their event date (delayed transactions). They must be loaded with the dimension versions that were valid at the event time, not the current ones, by looking up SCD2 rows with the event date.

#### How do you model currency in fact tables?

Store amounts in the transaction currency with a currency key, plus converted amounts in a reporting currency using the exchange rate valid on the transaction date (from a rate table), so reports can show both.

#### How do you model cancellations and returns?

Either as negative rows in the same transaction fact (simple sums), or as a separate returns fact with its own grain and reasons; accumulating snapshots can track status changes for orders.

#### What is a fact table's "audit dimension"?

A dimension or set of columns describing how each fact row was loaded (batch ID, load timestamp, source file, data quality status), which supports debugging and lineage.

#### How large can fact tables get, and how do you manage them?

Billions of rows are common. Manage them with partitioning by date, clustering on common filters, compression, incremental loads, retention policies, and aggregates for frequent queries.

#### When should you use a periodic snapshot instead of deriving state from transactions?

When computing state from all historical transactions is expensive or complex (balances, inventory levels, open tickets), or when source systems provide states but not complete event histories.

### Dimensions in depth

#### What is a role-playing dimension?

One physical dimension used several times in a fact table with different meanings, typically the date dimension as order date, ship date and delivery date, exposed through views or aliases.

#### What is a junk dimension?

A dimension combining several low-cardinality flags and indicators (payment type, gift wrap flag, channel) into one table of their combinations, avoiding many tiny dimensions or wide fact tables.

#### What is a mini-dimension?

A separate dimension for rapidly changing attributes of a large dimension (customer age band, income band, credit score band), so the main dimension doesn't explode with SCD2 rows; the fact table references both.

#### What is an outrigger dimension?

A dimension referenced by another dimension instead of by the fact table (for example a customer's first purchase date pointing to the date dimension). It's allowed sparingly; too many become snowflaking.

#### What is a bridge table?

A table resolving many-to-many relationships between facts and dimensions, such as accounts with multiple holders or diagnoses per hospital visit, often with weighting factors so amounts aren't double counted.

#### How do you model hierarchies in dimensions?

Fixed-depth hierarchies (category → subcategory → product) as flattened columns in the dimension. Ragged or variable-depth hierarchies (organization charts, bills of materials) with parent-child keys plus a bridge table of all ancestor-descendant pairs for easy rollups.

#### What is the "unknown member" row?

A special dimension row (often surrogate key `-1` or `0`) used when a fact's dimension is missing or not yet known, so facts aren't dropped by inner joins and the issue is visible in reports.

#### What is a shrunken dimension?

A subset of a dimension's rows or columns used for aggregate facts at a higher grain, such as a month dimension derived from the date dimension or a category dimension derived from products.

#### What is a slowly changing dimension?

A dimension whose attributes change over time unpredictably (a customer moves, a product changes category), requiring a policy for whether and how to keep history.

#### What is a static dimension?

A dimension whose content doesn't come from a source and rarely changes, such as the date dimension, status code lookups or currencies, generated once or maintained manually.

#### What is a dimension's "type 1" attribute in a mixed dimension?

Dimensions can mix policies per attribute: some columns are overwritten (type 1, corrections), others tracked historically (type 2, meaningful changes). Decide per attribute with business users.

#### How do you handle customer data coming from several systems?

Match and merge records into one conformed customer dimension using a master key (from master data management or matching rules on emails, IDs, names), keep source keys as attributes or in a mapping table, and define survivorship rules for conflicting attributes.

#### What is master data management (MDM)?

Processes and tools that create and maintain a single, authoritative version of core entities (customers, products, suppliers) across systems, which feeds conformed dimensions.

#### What is a "conformed attribute"?

An attribute with the same name, meaning and allowed values everywhere it appears, such as a standard country code or product category list, enabling consistent filtering across marts.

#### How do you handle multi-valued attributes like customer interests?

With a bridge table between the dimension and a group or attribute dimension, or by storing an array column where the engine supports it and queries can unnest it; avoid encoding several values in a comma-separated string.

#### What is a "current view" of an SCD2 dimension?

A view filtering `is_current = true` that gives one row per natural key with today's attributes, used by analysts who don't need history and for type 1 style reporting.

### Slowly changing dimensions

#### What are the SCD types?

Type 0: never change (keep original). Type 1: overwrite, no history. Type 2: add a new row per change with validity dates. Type 3: add a "previous value" column. Type 4: history in a separate table (mini-dimension or history table). Type 6: hybrid of 1, 2 and 3 (current value columns on all rows plus history rows). Type 7: dual keys to join to either current or historical rows.

#### How does SCD Type 2 work?

When a tracked attribute changes, the current row is closed (end date set, current flag false) and a new row is inserted with a new surrogate key, the new values, a start date and an open end date. Facts reference the surrogate key valid when they occurred.

| customer_key | customer_id | city     | valid_from | valid_to   | is_current |
|---|---|---|---|---|---|
| 101 | C-42 | Bogotá   | 2024-01-01 | 2026-03-31 | false |
| 187 | C-42 | Medellín | 2026-04-01 | 9999-12-31 | true  |

#### How do you implement SCD Type 2 with SQL?

Detect changed rows by comparing a hash of tracked attributes between staging and current dimension rows, close changed rows, and insert new versions (plus brand-new keys). Many platforms do it in one `MERGE` with a union trick, or with tools like dbt snapshots.

```sql
-- 1) close rows whose tracked attributes changed
UPDATE dim_customer d
SET valid_to = CURRENT_DATE - 1, is_current = false
FROM stg_customer s
WHERE d.customer_id = s.customer_id AND d.is_current
  AND d.attr_hash <> s.attr_hash;

-- 2) insert new versions and new customers
INSERT INTO dim_customer (customer_id, city, segment, attr_hash, valid_from, valid_to, is_current)
SELECT s.customer_id, s.city, s.segment, s.attr_hash, CURRENT_DATE, DATE '9999-12-31', true
FROM stg_customer s
LEFT JOIN dim_customer d ON d.customer_id = s.customer_id AND d.is_current
WHERE d.customer_id IS NULL;
```

#### Why use an end date of 9999-12-31 instead of NULL?

It makes "valid at date X" queries simple with `BETWEEN` and avoids `NULL` handling in joins; some teams prefer `NULL` plus a current flag. Be consistent.

#### How do you join facts to an SCD2 dimension for a point-in-time lookup?

During fact loading, look up the dimension row whose validity range contains the event date: `ON f.customer_id = d.customer_id AND f.event_date >= d.valid_from AND f.event_date < d.valid_to`, and store that surrogate key in the fact.

#### What is SCD Type 1, and when is it appropriate?

Overwriting attributes with new values, losing history. Appropriate for corrections (fixing a typo) and attributes where history doesn't matter for analysis.

#### What is SCD Type 3, and why is it rare?

Adding a column for the previous value (`previous_region`) to allow comparisons between current and prior assignments. It keeps only one level of history, so it's limited to specific reorganization analyses.

#### What is SCD Type 6?

A hybrid where the dimension keeps type 2 history rows and also type 1 "current" columns updated on all rows of the same natural key, so you can report facts both as they were and with today's attribute values.

#### What problems does SCD2 cause in large dimensions?

Row explosion when attributes change often, slower joins, and complex point-in-time logic. Mitigations: track only meaningful attributes, move volatile attributes to mini-dimensions, and use hash comparisons for change detection.

#### How do you handle a late-arriving dimension change?

If you learn today that a change happened last month, insert the version with its real start date, adjust the previous row's end date, and possibly re-point facts that occurred after the change to the new surrogate key, which is why some teams prefer point-in-time joins at query time.

#### What is a hash diff, and why use it?

A hash (MD5, SHA) of the concatenated tracked attributes, stored on each row, so detecting changes is a single comparison instead of comparing many columns, including null-safe handling.

#### How do dbt snapshots implement SCD2?

A snapshot config defines the unique key and a strategy (`timestamp` using an updated-at column, or `check` comparing columns); each run compares source with the snapshot table and closes and inserts rows, adding `dbt_valid_from` and `dbt_valid_to`.

#### How do you test an SCD2 dimension?

Check that each natural key has exactly one current row, validity ranges don't overlap or leave gaps, `valid_from < valid_to`, surrogate keys are unique, and facts' surrogate keys exist in the dimension.

#### What is a "type 2 with effective timestamp" versus date granularity?

Some dimensions track changes at timestamp precision (several changes per day), others at day level (latest value of the day). Choose based on how facts are matched; day granularity is simpler and usually enough.

#### Can facts be reassigned to new dimension versions?

Normally not: facts keep the version valid when they happened. For "as of today" reporting, join through the natural key to the current row or use type 6 current-value columns.

### Loading the warehouse

#### What is a full load versus an incremental load?

A full load reloads all data every run (simple, expensive, fine for small tables). An incremental load processes only new or changed data since the last run (by timestamp, sequence or CDC), which is necessary for large tables.

#### What is change data capture (CDC)?

Capturing inserts, updates and deletes from a source database, typically by reading its transaction log (binlog, WAL, redo log) with tools like Debezium, DMS, GoldenGate or Fivetran, and applying them to the warehouse.

#### Why is log-based CDC preferred over timestamp-based extraction?

It captures every change including deletes, doesn't depend on applications maintaining `updated_at` correctly, adds little load on the source, and preserves the order of changes.

#### How do you load a dimension?

Extract and clean source records, deduplicate per natural key, generate or look up surrogate keys, apply the SCD policy per attribute, add the unknown member, and run tests on uniqueness of current natural keys.

#### How do you load a fact table?

Extract transactions at the declared grain, look up dimension surrogate keys (point-in-time for SCD2, unknown member when missing), compute derived measures, and insert or merge idempotently into the fact table, usually partitioned by date.

#### What is the order of loading in a warehouse?

Dimensions first, then facts, so facts can find their surrogate keys. Late-arriving dimension members are handled with inferred members or unknown rows and fixed later.

#### What is an inferred member?

A placeholder dimension row created when a fact arrives with a natural key not yet in the dimension, with the natural key and default attributes, updated once the real dimension data arrives.

#### How do you make warehouse loads idempotent?

Process explicit date ranges, delete and reinsert the affected partitions or use `MERGE` on keys, avoid blind appends, use deterministic surrogate keys or stable lookups, and design jobs so reruns produce the same result.

#### What is upsert, and how is it done?

Insert new rows and update existing ones in one operation, typically with `MERGE` (Snowflake, BigQuery, Databricks, SQL Server, Postgres 15+) or `INSERT … ON CONFLICT DO UPDATE` (PostgreSQL).

```sql
MERGE INTO fct_orders t
USING stg_orders s ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET status = s.status, amount = s.amount, updated_at = s.updated_at
WHEN NOT MATCHED THEN INSERT (order_id, customer_key, status, amount, updated_at)
  VALUES (s.order_id, s.customer_key, s.status, s.amount, s.updated_at);
```

#### How do you handle deletes from sources?

With CDC delete events or by comparing full extracts to find missing keys; then either physically delete, or soft-delete with an `is_deleted` flag and deletion date to keep history, depending on business and compliance needs.

#### What is a watermark in incremental loading?

The highest timestamp or sequence value processed in the last run, stored in a control table and used to select new rows next time; use an overlap window to catch late-committed rows and deduplicate.

#### What is a backfill?

Reprocessing historical periods, for example after a bug fix or a new column. Pipelines should accept date ranges as parameters and write idempotently so backfills are safe.

#### What are reconciliation checks?

Comparisons between source and warehouse (row counts, sums of amounts, distinct keys per day) to prove that loads are complete and correct, often run automatically after each load.

#### What is a control table in ETL?

A table storing metadata for each pipeline run: watermarks, batch IDs, start and end times, row counts, status and errors, used for incremental loading, restarts and monitoring.

#### What is the difference between push and pull ingestion?

Pull: the warehouse side extracts from sources on a schedule (queries, APIs). Push: sources send data as events or files (CDC streams, webhooks, file drops). Push reduces latency and source load; pull is simpler to control.

#### How do you load data from SaaS applications?

With managed connectors (Fivetran, Airbyte, Lakeflow Connect, AppFlow) or custom API extraction handling pagination, rate limits, incremental cursors and schema changes, landing raw JSON before modeling.

#### What are ELT tools like dbt used for?

Writing transformations as version-controlled SQL models with dependencies, tests, documentation and environments, compiled and run inside the warehouse, bringing software engineering practices to the transformation layer.

#### How do you handle schema changes in sources?

Detect them (schema checks, contracts, alerts), land raw data flexibly (`VARIANT`, JSON, schema evolution), select columns explicitly in staging, decide per change whether to propagate it, and communicate breaking changes.

#### What is micro-batch loading?

Loading small batches every few minutes (instead of daily), balancing latency and efficiency; Snowpipe, Auto Loader, Structured Streaming triggers and scheduled `MERGE` jobs implement it.

### Data quality

#### What are the dimensions of data quality?

Completeness (no missing data), accuracy (correct values), consistency (same values across systems), validity (conforms to formats and rules), uniqueness (no duplicates), timeliness (fresh enough) and integrity (relationships hold).

#### Which tests should every warehouse table have?

Primary key uniqueness and not null at the grain, referential integrity from facts to dimensions, accepted values for status codes, freshness of the latest load, row count thresholds or anomalies, and reconciliation with sources for critical tables.

#### Where should data quality checks run?

At ingestion (schema and format checks), after transformations (business rules and integrity), and before publishing to consumers (gates that stop bad data from reaching dashboards), with results stored for trend analysis.

#### What should happen when a data quality check fails?

Depends on severity: block publishing and alert the owner for critical checks, quarantine bad rows and continue for row-level issues, or warn and record for minor issues. Consumers should be informed when data is delayed or wrong.

#### What tools are used for warehouse data quality?

dbt tests and packages (dbt_utils, dbt_expectations), Great Expectations, Soda, Monte Carlo and other observability tools, Databricks expectations, Snowflake data metric functions, and custom SQL checks in orchestrators.

#### What is data observability?

Monitoring data systems for freshness, volume, schema changes, distribution changes and lineage, often with automatic anomaly detection, to find data incidents before users do.

#### What is a data contract?

An agreement between a data producer and consumers about a dataset's schema, semantics, quality and SLAs, enforced in CI and pipelines so breaking changes are caught early.

#### What is a data quality SLA?

A commitment on measurable quality (for example "fewer than 0.1% of orders without customer", "data no older than 2 hours"), monitored automatically and reported to consumers.

#### How do you quantify the business impact of bad data?

By tracing incidents to decisions affected (wrong invoices, missed targets), time spent fixing, and trust lost; this helps prioritize quality investments on critical datasets.

#### What are anomaly detection checks?

Statistical checks comparing today's metrics (row counts, sums, null rates) with historical patterns, flagging unusual deviations even without explicit thresholds.

#### What is the role of a data steward?

A business-side owner responsible for definitions, quality rules and issue resolution for a data domain, working with data engineers who implement the checks.

### Warehouse architectures

#### What is the Inmon approach?

A top-down approach: build a normalized (3NF) enterprise data warehouse as the integrated core (the Corporate Information Factory), then derive dependent data marts for departments. It emphasizes integration and consistency but takes longer to deliver value.

#### What is the Kimball approach?

A bottom-up approach: build dimensional data marts per business process, integrated through conformed dimensions and the bus matrix, delivering value incrementally. The union of the marts is the warehouse.

#### Inmon or Kimball: how do you choose?

Kimball for faster delivery and business-friendly models; Inmon (or Data Vault) for a strongly integrated, auditable core in complex enterprises with many sources. Many organizations combine them: a normalized or Data Vault core with Kimball marts on top.

#### What is Data Vault?

A modeling method by Dan Linstedt for the integration layer: hubs (business keys), links (relationships between hubs) and satellites (descriptive attributes with history). It's insert-only, auditable and adapts well to changing sources, with marts built on top for consumption.

#### What are the pros and cons of Data Vault?

Pros: auditability, full history, parallel loading, resilience to source changes, easy to add sources. Cons: many tables and joins, not directly usable by analysts (needs marts), and more complex to implement and query without automation.

#### What is the medallion architecture's relation to warehousing?

It's a layered lakehouse pattern (bronze raw, silver cleaned and conformed, gold business-ready) that maps to staging, integration and presentation layers; gold often contains Kimball star schemas.

#### What is a semantic layer?

A layer that defines business metrics, dimensions and relationships once (in dbt's semantic layer, LookML, Cube, Power BI semantic models, AtScale, metric views) so every tool computes "revenue" the same way.

#### What is an OLAP cube?

A multidimensional structure precomputing aggregates across dimensions for fast slicing and dicing. MOLAP stores cubes in specialized storage (SSAS), ROLAP queries relational tables, and HOLAP mixes both. Columnar cloud warehouses reduced the need for physical cubes.

#### What is a virtual data warehouse or data virtualization?

Querying data across sources in place through a virtualization layer (Denodo, Trino, federated queries) without physically consolidating it. It's quick for integration but performance and history are limited.

#### What is a real-time or streaming data warehouse?

A warehouse fed continuously (Snowpipe Streaming, BigQuery streaming, Kafka connectors, CDC) with low-latency transformations (dynamic tables, materialized views, streaming tables), for operational analytics needing data within seconds or minutes.

#### What is a hub-and-spoke architecture?

A central enterprise warehouse (hub) feeding departmental data marts (spokes), the classic Inmon-style topology.

#### What is a federated architecture?

Several warehouses or marts kept by different business units, integrated through shared standards, conformed dimensions or virtualization rather than one central store; it relates to data mesh ideas.

#### What is a "persistent staging area"?

A staging layer that keeps all historical extracts (often insert-only with load timestamps) instead of truncating each run, allowing rebuilds of downstream layers without re-extracting from sources.

#### What is the "raw vault" versus "business vault" in Data Vault?

The raw vault stores source data as-is in hubs, links and satellites; the business vault adds derived structures with business rules (computed satellites, point-in-time and bridge tables) to simplify building marts.

#### What are point-in-time (PIT) tables in Data Vault?

Helper tables that store, for each hub key and snapshot date, the matching satellite load dates, making it fast to assemble the state of an entity at a point in time for dimensions.

### Engines and storage

#### What is MPP?

Massively parallel processing: a database splits data across many nodes, each with its own CPU, memory and storage (or cache), and executes queries in parallel, combining results. Redshift, Teradata, Synapse and Vertica are MPP; Snowflake and BigQuery are cloud variants.

#### Why are analytical databases columnar?

Analytical queries read a few columns of many rows; storing each column contiguously means reading only needed columns, compressing similar values very well, and processing them with vectorized execution.

#### What is the difference between row-oriented and column-oriented storage?

Row storage keeps all columns of a row together, efficient for reading and writing whole records (OLTP). Column storage keeps values of each column together, efficient for scans and aggregations on few columns (OLAP).

#### What is a distribution key (Redshift, Synapse)?

The column used to distribute rows across nodes. Distributing two large tables on their join key co-locates matching rows and avoids redistribution during joins; small dimensions can be replicated (`ALL`) to every node; `EVEN` or `AUTO` spread rows uniformly.

#### What is a sort key (Redshift) or clustering key?

An ordering of data within storage so that range filters can skip blocks using min/max metadata (zone maps). Equivalent concepts: Snowflake clustering keys, BigQuery clustering, Delta liquid clustering or Z-order.

#### What is partitioning in a warehouse?

Splitting a large table by a column (usually date) so queries filtering on it scan only relevant partitions and maintenance (deleting old data, reloading a day) is cheap. BigQuery uses explicit partitioning; Snowflake uses micro-partitions automatically.

#### What are zone maps or min/max statistics?

Metadata storing minimum and maximum values per block or file, used to skip blocks that can't match a filter. Data sorted or clustered by the filter column makes them effective.

#### What is a materialized view?

A stored, automatically or periodically refreshed result of a query. It speeds up repeated aggregations or joins; the engine may use it transparently. Maintenance costs compute.

#### What is workload management?

Controlling how queries share resources: queues, priorities, concurrency limits, separate compute clusters or warehouses for ETL and BI, and query timeouts, so heavy jobs don't starve interactive users.

#### What is the separation of storage and compute?

Storing data in shared storage (object storage) and running independent, elastic compute clusters on top, so you scale and pay for each separately and isolate workloads. Snowflake, BigQuery, Databricks and Redshift RA3/Serverless use this model.

#### What is vectorized execution?

Processing batches of column values at once with CPU-efficient loops and SIMD instructions instead of row by row, which greatly speeds up scans, filters and aggregations in columnar engines.

#### What are result caches?

Stores of previous query results returned instantly when the same query runs again on unchanged data (Snowflake result cache, BigQuery cached results), saving compute for dashboards.

#### What is the role of statistics in query optimization?

Row counts, distinct values, min/max and histograms let the optimizer estimate cardinalities and choose join orders and strategies; stale statistics cause bad plans.

#### What is compression encoding in columnar stores?

Techniques such as dictionary, run-length, delta and bit-packing encodings that shrink columns with repeated or ordered values; sorted data compresses better.

#### What is the difference between scale up and scale out in warehouses?

Scale up gives a query more resources (bigger warehouse, more slots) to finish faster; scale out adds clusters to serve more concurrent queries. Choose based on whether the problem is single-query latency or concurrency.

### Performance

#### How do you make a star schema query fast?

Filter on partitioned or clustered columns (date), join facts to small dimensions (broadcast), select only needed columns, pre-aggregate common queries, keep statistics current, and avoid functions on filter columns.

#### What causes a "fan-out" or double counting in joins?

Joining a fact to a table that has several rows per key (many-to-many or a wrong grain), so each fact row is duplicated and sums inflate. Check join cardinalities and enforce uniqueness of dimension keys.

#### How do you speed up `COUNT(DISTINCT)` on large data?

Use approximate functions (HyperLogLog: `APPROX_COUNT_DISTINCT`), pre-aggregate distinct sets per period, or maintain distinct counts in aggregate tables when exact values are needed.

#### Why can wide denormalized tables be fast in columnar engines?

Because only the columns referenced by a query are read, a wide table doesn't cost more to query than a narrow one with the same rows, and it avoids joins. The costs are storage, maintenance and potential inconsistency.

#### What is query pruning, and how do you check it?

Skipping partitions, files or blocks that can't match a query's filters. Check it in query profiles or plans (partitions scanned versus total, bytes scanned) and fix filters or data layout when it doesn't happen.

#### How do you optimize a slow dashboard?

Find the slow queries, check pruning and joins, add aggregates or materialized views for the dashboard's grain, use the BI tool's extracts or caching, limit default date ranges, and remove unnecessary visuals that each fire queries.

#### What is the impact of data types on warehouse performance?

Smaller types (integers instead of strings for keys, `DATE` instead of `TIMESTAMP` when enough, `DECIMAL` with appropriate precision) compress better and compare faster; joining on mismatched types forces casts and prevents optimizations.

#### How do you handle very large dimensions (hundreds of millions of rows)?

Partition or cluster by natural key ranges, minimize SCD2 churn with mini-dimensions, avoid unnecessary attributes, use integer surrogate keys, and consider whether the "dimension" is really a fact-like entity.

#### What is a "covering" aggregate?

An aggregate table containing all the columns a frequent query needs at the right grain, so the query never touches the atomic fact table.

#### How do you avoid expensive `SELECT DISTINCT` in models?

Find why duplicates appear (wrong join grain) and fix the join instead of masking it with `DISTINCT`, which is costly and hides data problems.

#### How do you test warehouse performance before going live?

Replay representative queries and concurrency on production-sized data, measure latency and cost per query, check plans for pruning and joins, and tune layout, aggregates and warehouse sizing.

#### How can incremental models reduce warehouse costs?

By transforming only new or changed data each run instead of rebuilding entire tables, which cuts compute dramatically for large facts; they need careful handling of late data and backfills.

### Cloud data warehouses

#### What are the main cloud data warehouses?

Snowflake, Google BigQuery, Amazon Redshift (provisioned and Serverless), Azure Synapse and Microsoft Fabric warehouses, and Databricks SQL on the lakehouse. They differ in architecture, pricing models and ecosystem integration.

#### How does BigQuery work and how is it priced?

BigQuery is serverless: storage in a columnar format (Capacitor) on Colossus, compute allocated as slots by Dremel. Pricing is on-demand per TB scanned or capacity-based (editions with reserved or autoscaled slots), plus storage.

#### How does Amazon Redshift work?

An MPP warehouse with a leader node and compute nodes; RA3 nodes separate managed storage (S3-backed) from compute, Serverless bills per RPU-hour, and features include distribution and sort keys (with automatic tuning), materialized views, Spectrum for S3 data, data sharing and zero-ETL integrations.

#### How do cloud warehouses charge, and what drives costs?

Compute (credits, slots, RPUs, DBUs) usually dominates, then storage, data transfer and serverless features. Costs grow with inefficient queries, always-on compute, full refreshes, and many users running unfiltered queries; governance and monitoring are essential.

#### How do you choose a cloud warehouse?

Consider the existing cloud and ecosystem, workload patterns (steady vs spiky, concurrency), skills, governance needs, open formats and lakehouse strategy, pricing model fit, data sharing needs and vendor lock-in tolerance. Prototype with real queries before committing.

#### What is zero-copy data sharing?

Sharing live data between accounts or organizations without copying it (Snowflake Secure Data Sharing, BigQuery Analytics Hub, Redshift data sharing, Delta Sharing), so consumers query the provider's data with their own compute.

#### What are open table formats' implications for warehouses?

Iceberg and Delta let several engines (warehouse, Spark, Trino) work on the same data in object storage, reducing lock-in and copies. Warehouses increasingly read and write them natively.

#### What is BigQuery's approach to partitioning and clustering?

Tables can be partitioned by a date/timestamp column, ingestion time or integer range, and clustered on up to four columns; queries filtering on them read fewer bytes, which reduces on-demand cost directly.

#### What is Redshift Spectrum?

A feature that lets Redshift query data in S3 through external tables in the Glue Data Catalog, joining lake data with warehouse tables, billed per bytes scanned.

#### What is Microsoft Fabric's warehouse?

A SaaS analytics platform where warehouses and lakehouses store data in Delta format in OneLake, queried with T-SQL and Spark and served to Power BI with Direct Lake mode.

#### What is Databricks SQL as a warehouse?

SQL warehouses on the Databricks lakehouse querying Delta tables governed by Unity Catalog, with Photon, serverless compute and BI connectors, offering warehouse functionality on open storage.

### BI and consumption

#### What makes a data model BI-friendly?

Star schemas with clear names, documented business definitions, conformed dimensions, correct grains, surrogate keys hidden from users, consistent date handling, and a semantic layer for metrics.

#### What is the difference between a report and a dashboard?

A report presents detailed data, often tabular and paginated, for analysis or regulatory purposes. A dashboard summarizes key metrics visually for monitoring at a glance, with drill-down.

#### What is self-service BI, and what are its risks?

Business users building their own analyses from governed datasets. Risks: inconsistent metric definitions, duplicated logic, uncontrolled extracts and costs. A semantic layer, certified datasets and training reduce them.

#### What is row-level security in BI and warehouses?

Restricting which rows users see based on their identity (region, department), implemented in the warehouse (row access policies, secure views) or the BI layer, so one dataset serves many audiences safely.

#### How do you document a warehouse?

Table and column descriptions in the catalog (dbt docs, Unity Catalog, Glue, DataHub), a business glossary for metrics, lineage graphs, ownership and SLAs, and examples of correct queries.

#### What is a certified dataset?

A dataset marked as trusted after review (definitions, tests, ownership), promoted in BI tools and catalogs so users prefer it over personal or experimental copies.

#### What is reverse ETL?

Sending warehouse data (segments, scores, metrics) back into operational tools like CRMs, marketing platforms or support systems, so business teams act on modeled data (Hightouch, Census, custom jobs).

#### How do you decide between live queries and extracts in BI tools?

Live queries give fresh data and central security but depend on warehouse performance and cost; extracts (Tableau extracts, Power BI import, SPICE) are fast and cheap per query but stale and duplicated. Choose per dashboard based on freshness needs and usage.

### Governance and security

#### How do you secure a data warehouse?

Least-privilege roles (access roles granted to functional roles), SSO and MFA, network restrictions, encryption at rest and in transit, masking of sensitive columns, row-level security, auditing of access, and separate environments for development and production.

#### How do you handle personal data (PII) in a warehouse?

Classify and tag it, minimize what's loaded, pseudonymize or tokenize identifiers early, mask for most users, restrict raw access, apply retention policies, and support deletion requests (GDPR, Colombia's Law 1581) with documented processes.

#### What is data lineage, and why does it matter?

The record of where data comes from and how it's transformed, at table and column level. It supports impact analysis before changes, debugging wrong numbers, audits and trust.

#### What is a data catalog?

A searchable inventory of datasets with descriptions, owners, schemas, tags, lineage, quality status and usage, helping people find and understand data (DataHub, Collibra, Alation, Unity Catalog, Glue Data Catalog).

#### What are data retention policies?

Rules for how long each dataset is kept (legal, business and cost reasons), implemented with partition drops, lifecycle rules, Time Travel settings and archiving, and documented for compliance.

### SQL for analytics

#### What are window functions, and why are they essential in warehousing?

Functions that compute values over a set of rows related to the current row without collapsing them (`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`, `SUM() OVER`). They power deduplication, running totals, period comparisons and sessionization.

#### How do you compute month-over-month growth?

```sql
WITH monthly AS (
  SELECT d.year_month, SUM(f.net_amount) AS revenue
  FROM fct_order_lines f JOIN dim_date d ON f.order_date_key = d.date_key
  GROUP BY d.year_month
)
SELECT year_month, revenue,
       revenue / NULLIF(LAG(revenue) OVER (ORDER BY year_month), 0) - 1 AS mom_growth
FROM monthly;
```

#### How do you calculate a running total?

`SUM(amount) OVER (PARTITION BY customer_key ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`.

#### How do you deduplicate keeping the latest row per key?

```sql
SELECT * FROM (
  SELECT s.*, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) AS rn
  FROM stg_customers s
) WHERE rn = 1;
```

Engines with `QUALIFY` (Snowflake, BigQuery, Databricks) allow filtering the window directly.

#### What is the difference between `RANK`, `DENSE_RANK` and `ROW_NUMBER`?

`ROW_NUMBER` gives unique sequential numbers; `RANK` gives ties the same rank and skips the next ranks (1, 1, 3); `DENSE_RANK` gives ties the same rank without gaps (1, 1, 2).

#### How do you find customers active in consecutive months?

Compute each customer's months of activity, then use `LAG` to compare with the previous month or the "gaps and islands" technique (month index minus row number) to group consecutive streaks.

#### What is a cohort analysis query?

Assign each customer to a cohort (first purchase month), then count active customers or revenue per cohort and months since first purchase, often pivoted into a retention triangle.

#### How do you compute a median or percentile?

With `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x)` in many engines, `MEDIAN()` in Snowflake, or `APPROX_PERCENTILE`/`APPROX_QUANTILES` for large data.

#### What are `GROUPING SETS`, `ROLLUP` and `CUBE`?

Extensions of `GROUP BY` that compute several aggregation levels in one query: `ROLLUP(year, month)` gives month, year and grand totals; `CUBE` gives all combinations; `GROUPING SETS` lists the exact combinations.

#### What is a CTE, and when should you use it?

A common table expression (`WITH name AS (...)`) names a subquery for readability and reuse within a query; recursive CTEs traverse hierarchies. They make complex warehouse SQL easier to review.

#### How do you avoid division-by-zero errors?

Use `NULLIF(denominator, 0)` so the result is `NULL` instead of an error, or safe division functions (`SAFE_DIVIDE` in BigQuery, `DIV0` in Snowflake).

#### What is the difference between `WHERE` and `HAVING`?

`WHERE` filters rows before aggregation; `HAVING` filters groups after aggregation. Filtering early with `WHERE` is cheaper.

#### How do you handle NULLs in joins and aggregations?

`NULL` never equals anything, so rows with `NULL` keys don't join (use unknown members or `IS NOT DISTINCT FROM`); aggregates ignore `NULL`s except `COUNT(*)`; use `COALESCE` for display defaults.

#### How do you pivot rows into columns in SQL?

With conditional aggregation (`SUM(CASE WHEN channel = 'web' THEN amount END) AS web_amount`) portable across engines, or `PIVOT` where supported (Snowflake, SQL Server, BigQuery, Databricks).

### Scenarios

#### Design a sales data mart for an e-commerce company.

Business process: order lines. Grain: one row per order line. Dimensions: date (order, ship), customer (SCD2 on segment and region), product (SCD2 on category), store or channel, promotion, and a junk dimension for flags; degenerate dimension order number. Facts: quantity, gross amount, discount, net amount, cost, tax. Add a returns fact and daily inventory snapshot later, sharing conformed dimensions.

#### Finance and sales report different revenue numbers. How do you resolve it?

Find each team's definition (gross vs net, booking vs shipment date, currency conversion, refunds, cancellations), trace both numbers through lineage to the sources, agree a single definition with business owners, implement it once in the semantic layer or a conformed fact, and deprecate the divergent logic.

#### A fact table's daily load sometimes creates duplicates. How do you fix it?

Make the load idempotent (`MERGE` on the grain key or delete-insert of the load window), deduplicate staging by natural key, add a uniqueness test at the grain that blocks publishing, and check source extraction for overlapping windows.

#### A dimension must keep history of customer segment changes but customer address changes daily. What do you do?

Track segment as SCD2 in the customer dimension; put address in a separate dimension or mini-dimension, or keep it type 1 if history isn't needed for analysis, to avoid daily row explosion.

#### How would you migrate an on-premises warehouse to the cloud?

Inventory sources, ETL jobs, reports and users; choose target platform and architecture; migrate history in bulk; rebuild pipelines as ELT (often with dbt) rather than lift-and-shift where valuable; redefine security and governance; validate with reconciliation reports; run in parallel; switch reports in waves; decommission the old system.

#### Queries on a 5-year fact table got slow as data grew. What do you check?

Whether queries filter on the partition or clustering column, data layout degradation (clustering depth, small files), missing statistics, new joins that fan out, BI queries without date filters, and whether aggregate tables or materialized views would serve common patterns.

#### How do you explain a data warehouse to a business stakeholder?

It's the company's trusted, organized history of its data: information from all systems brought together, cleaned and described once, so everyone answers business questions with the same numbers.

#### How would you model subscriptions for a SaaS company?

A subscription dimension (plan, billing period, status SCD2), a transaction fact for subscription events (start, upgrade, downgrade, cancel), and a monthly periodic snapshot fact with MRR per customer and plan, enabling churn, expansion and cohort analysis.

#### Analysts complain they can't find the right tables. What do you do?

Organize schemas by layer and domain, document models and columns, certify key datasets, publish a catalog with search and lineage, deprecate and remove legacy tables, and offer a semantic layer with business-named metrics.

#### How would you design the warehouse for a company acquiring other companies frequently?

An integration layer resilient to new sources (Data Vault or a well-structured core with source mapping tables), conformed dimensions with master data matching across companies, source system codes on every row, and marts that can include or exclude acquired entities.
