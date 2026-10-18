## Data Warehousing Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Data warehousing study guide: about 200 questions](../../images/data_warehousing_study_guide_title_img.png)

About 200 interview-style questions on data warehousing: core concepts, dimensional modeling with facts and dimensions, slowly changing dimensions, loading patterns, data quality, warehouse architectures and engines, performance, cloud warehouses, BI and the semantic layer, with SQL examples. The answers are tool-agnostic where possible, with notes for Snowflake, Redshift, BigQuery and Databricks.

The guide follows a learning path in six stages. Each section is split into short units: learning goals, a concept explanation and a worked example, then questions (recall first, then application), a practical challenge and key takeaways. To **learn**, read each unit top to bottom. To **review**, switch to review mode or use "Skip to questions", mark answers you want to see again, and try a mixed review across sections.

<!-- QA -->
<!-- stage: Foundations -->

### Core concepts

<!-- unit: What a warehouse is -->

<!-- goals -->

- Explain what a data warehouse is and how it differs from an operational database.
- Describe who uses a warehouse and why analytics needs its own system.

<!-- concept -->

Operational systems are built to run the business: take an order, update a stock level, record a payment, thousands of times a minute. Asking them "how did sales change by region over three years?" is slow for them and awkward for you, because data is spread across systems, overwritten as it changes, and modeled for writing, not reading.

A warehouse is the answer to that mismatch: one place where data from many systems is integrated, kept with its history and organized around business subjects so analysis is fast and consistent.

<!-- example -->

| Question | OLTP database | Data warehouse |
|---|---|---|
| Typical query | Fetch order 98123 | Revenue by month and region, 3 years |
| Data | Current state, one system | History, many systems integrated |
| Model | Normalized for writes | Dimensional for reads |
| Users | Applications | Analysts, BI, data science |

#### What is a data warehouse?

A central repository of integrated, historical data from many sources, organized for analysis and reporting rather than for transactions. Bill Inmon's classic definition: subject-oriented, integrated, time-variant and non-volatile.

#### What do "subject-oriented, integrated, time-variant and non-volatile" mean?

Subject-oriented: organized around business subjects (customers, sales, products) rather than applications. Integrated: consistent names, codes and units across sources. Time-variant: keeps history so you can analyze change over time. Non-volatile: data is loaded and read, not updated in place by transactions.

#### What is the difference between a data warehouse and a database?

A database is any organized data store; a data warehouse is a specific use of database technology designed for integrated, historical, analytical data, usually with columnar storage and dimensional or layered models.

#### What is the difference between OLTP and OLAP?

OLTP (online transaction processing) systems run the business: many small, concurrent reads and writes, normalized schemas, current state. OLAP (online analytical processing) systems analyze the business: large scans and aggregations over history, denormalized or dimensional schemas, mostly reads.

#### Why not run analytics directly on the operational database?

Analytical queries are heavy and would slow the application; operational schemas are normalized and hard to query; data from different systems must be combined and cleaned; history is often overwritten in OLTP systems; and access control for analysts differs from application access.

#### Who are the main users of a data warehouse?

Business analysts and BI developers (reports, dashboards), data scientists (training data, exploration), finance and operations teams (regulatory and management reporting), executives (KPIs), and increasingly applications and AI agents through APIs and semantic layers.

#### How do you explain a data warehouse to a business stakeholder?

It's the company's trusted, organized history of its data: information from all systems brought together, cleaned and described once, so everyone answers business questions with the same numbers.

<!-- challenge -->

A company runs its monthly reports directly on the ERP database at night. Name two problems a warehouse would solve.

<!-- solution -->

Reports would no longer compete with the ERP for resources or need night windows, and history would be preserved (the ERP overwrites changes like customer regions). A warehouse also integrates CRM and other sources the ERP doesn't have.

<!-- takeaways -->

- Warehouses integrate data from many systems with history.
- OLTP runs the business; OLAP analyzes it.
- Analytics needs its own system and model.

<!-- unit: Layers and components -->

<!-- goals -->

- Describe the layers of a warehouse and the role of staging.
- Compare ETL and ELT and explain warehouse metadata.

<!-- concept -->

Data passes through a warehouse in stages, each with a job. Staging keeps source extracts close to how they arrived, so loads can be restarted and audited. An integration layer cleans, conforms and keeps history. Presentation marts shape the data for consumers.

Whether transformation happens before loading (ETL) or inside the warehouse (ELT) is mostly a matter of where compute is cheapest; cloud warehouses made ELT the default. Metadata ties the layers together by recording what each table means and where it came from.

<!-- example -->

```text
sources ─► staging (raw extracts, load metadata)
        ─► core / integration (clean, conformed, historized)
        ─► marts (stars per business process) ─► BI, data science
```

#### What are the typical layers of a data warehouse?

Staging (raw copies of source data), an integration or core layer (cleaned, conformed, historized data; normalized or Data Vault), and a presentation layer (dimensional marts for BI). Modern stacks call them raw/bronze, staging/silver and marts/gold.

#### What is the role of the staging area?

A landing zone where source extracts are stored with minimal changes, so loads can be restarted, reprocessed and audited without hitting sources again, and transformations don't run against operational systems.

#### What are the main components of a warehouse architecture?

Source systems, ingestion and ETL/ELT tools, storage layers (staging, core, marts), the query engine, a semantic or metrics layer, BI and analytics tools, orchestration, data quality and observability, catalog and governance, and security.

#### What is metadata in a warehouse?

Data about the data: technical metadata (schemas, types, lineage, load times), business metadata (definitions, owners, glossary) and operational metadata (job runs, row counts, errors). It powers catalogs, impact analysis and trust.

#### What is the difference between ETL and ELT?

ETL extracts data, transforms it in a separate engine, then loads it into the warehouse. ELT loads raw data into the warehouse first and transforms it there with SQL (often with dbt), using the warehouse's scalable compute. Cloud warehouses made ELT the default.

<!-- challenge -->

A team transforms data inside the extraction script and loads only final tables. A transformation bug is found. Why is recovery hard, and what layer is missing?

<!-- solution -->

Without a staging layer, raw extracts aren't kept, so the corrected logic can't be rerun on the original data; sources may have changed since. Keep source data in staging (or a persistent staging area) and transform from there.

<!-- takeaways -->

- Staging, integration and marts each have a job.
- ELT transforms inside the warehouse; ETL before it.
- Metadata explains meaning and origin.

<!-- unit: Marts, ODS, lakes and appliances -->

<!-- goals -->

- Distinguish data marts, ODS, data lakes and lakehouses.
- Know dependent versus independent marts and warehouse appliances.

<!-- concept -->

Around the warehouse sit related stores with different jobs. Data marts focus on one department or process; when built from a shared warehouse they agree with each other, when built independently they drift apart. An ODS integrates current operational data for near-real-time use. A data lake stores raw data of any format cheaply; a lakehouse adds warehouse features on top of it.

Appliances were the on-premises way to run warehouses, now mostly replaced by cloud services.

<!-- example -->

| Store | Purpose | Data |
|---|---|---|
| Data mart | Sales analysis | Modeled, one subject |
| ODS | Customer service screens | Current, integrated |
| Data lake | Raw and ML data | Any format, history |
| Lakehouse | BI and ML on one copy | Open tables with ACID |

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

#### What is a data warehouse appliance?

A pre-integrated hardware and software system for warehousing (Teradata, Netezza, Exadata), sold as a box. Cloud warehouses have largely replaced appliances with elastic services.

<!-- challenge -->

Marketing and finance each built their own independent mart from source systems, and their customer counts never match. What do you propose?

<!-- solution -->

Build both marts from a shared integration layer with a conformed customer dimension and one definition of "customer", making them dependent marts that agree by construction.

<!-- takeaways -->

- Marts serve one subject; dependent marts agree.
- An ODS serves current, operational needs.
- Lakes and lakehouses complement or replace warehouses.

<!-- unit: Trust and timeliness -->

<!-- goals -->

- Explain a single source of truth and how to reach it.
- Define latency expectations and warehouse SLAs.

<!-- concept -->

A warehouse is only valuable if people trust it, which means one definition and one source for each metric, delivered when people need it. Conflicting numbers usually come from different definitions rather than bugs: gross versus net, booking versus shipping date.

Timeliness is the other half of trust. Latency is how long until an event shows up in reports; SLAs make that explicit so consumers know when data is complete.

<!-- example -->

| Metric | Definition (agreed) | SLA |
|---|---|---|
| Net revenue | Gross − refunds − discounts, by order date, EUR | Updated by 07:00 local, business days |
| Active customer | Order in last 90 days | Daily |

#### What is a single source of truth?

The goal that each business metric and entity has one agreed definition and one authoritative dataset, so reports across departments agree. Conformed dimensions, a semantic layer and governance support it.

#### What is latency in a warehouse context?

The delay between an event in a source system and its availability in reports: daily batch (hours), micro-batch (minutes) or streaming (seconds). The right latency depends on business decisions, not technology.

#### What are SLAs for a data warehouse?

Commitments such as "sales mart refreshed by 7 a.m. local time on business days" or "99% of loads succeed", with monitoring and communication when breached. They turn pipelines into products consumers can rely on.

#### Finance and sales report different revenue numbers. How do you resolve it?

Find each team's definition (gross vs net, booking vs shipment date, currency conversion, refunds, cancellations), trace both numbers through lineage to the sources, agree a single definition with business owners, implement it once in the semantic layer or a conformed fact, and deprecate the divergent logic.

<!-- challenge -->

Sales reports revenue on booking date, finance on invoice date, and both are right for their purpose. How do you keep a single source of truth?

<!-- solution -->

Define both metrics explicitly with distinct names (booked revenue, invoiced revenue), document them in the glossary, compute each once in certified models, and show both where relevant.

<!-- takeaways -->

- Conflicts usually come from definitions, not bugs.
- One definition, one source per metric.
- SLAs make freshness expectations explicit.

### Warehouse architectures

<!-- unit: Inmon and Kimball -->

<!-- goals -->

- Compare the Inmon and Kimball approaches.
- Describe hub-and-spoke and federated architectures.

<!-- concept -->

The two classic schools differ on where integration happens. Inmon builds a normalized enterprise warehouse first and derives marts from it: strong integration, slower start. Kimball builds dimensional marts per business process and integrates them through conformed dimensions: faster value, discipline required.

Organizational shape follows: hub-and-spoke puts a central warehouse in the middle; federated setups let business units keep their own, joined by shared standards.

<!-- example -->

```text
Inmon:   sources ─► EDW (3NF) ─► marts (sales, finance, HR)
Kimball: sources ─► staging ─► star schemas per process, sharing dim_customer, dim_date
```

#### What is the Inmon approach?

A top-down approach: build a normalized (3NF) enterprise data warehouse as the integrated core (the Corporate Information Factory), then derive dependent data marts for departments. It emphasizes integration and consistency but takes longer to deliver value.

#### What is the Kimball approach?

A bottom-up approach: build dimensional data marts per business process, integrated through conformed dimensions and the bus matrix, delivering value incrementally. The union of the marts is the warehouse.

#### Inmon or Kimball: how do you choose?

Kimball for faster delivery and business-friendly models; Inmon (or Data Vault) for a strongly integrated, auditable core in complex enterprises with many sources. Many organizations combine them: a normalized or Data Vault core with Kimball marts on top.

#### What is a hub-and-spoke architecture?

A central enterprise warehouse (hub) feeding departmental data marts (spokes), the classic Inmon-style topology.

#### What is a federated architecture?

Several warehouses or marts kept by different business units, integrated through shared standards, conformed dimensions or virtualization rather than one central store; it relates to data mesh ideas.

<!-- challenge -->

A company needs sales dashboards in two months, with more departments later. Which approach do you start with, and what discipline protects the future?

<!-- solution -->

Kimball: deliver the sales star quickly, but build dimensions (customer, product, date) as conformed from day one and plan with a bus matrix, so later marts reuse them.

<!-- takeaways -->

- Inmon integrates first; Kimball delivers marts first.
- Conformed dimensions keep Kimball marts integrated.
- Organization shapes hub-and-spoke versus federated designs.

<!-- unit: Data Vault -->

<!-- goals -->

- Describe Data Vault's hubs, links, satellites and vault layers.
- Decide when Data Vault fits, including frequent acquisitions.

<!-- concept -->

Data Vault is designed for change. It separates business keys (hubs), relationships (links) and descriptive history (satellites), so a new source adds new satellites instead of reshaping existing tables. Everything is insert-only with load metadata, which gives full audit history.

The price is complexity: many tables and joins, so marts and helper tables like PIT tables are needed for consumption. It pays off with many changing sources and strict audit needs.

<!-- example -->

```text
raw vault:      hub_customer, sat_customer_crm, sat_customer_billing, link_customer_order
business vault: sat_customer_segment (derived rules)
helpers:        pit_customer (keys of latest satellite rows per snapshot date)
marts:          dim_customer, fct_orders
```

#### What is Data Vault?

A modeling method by Dan Linstedt for the integration layer: hubs (business keys), links (relationships between hubs) and satellites (descriptive attributes with history). It's insert-only, auditable and adapts well to changing sources, with marts built on top for consumption.

#### What are the pros and cons of Data Vault?

Pros: auditability, full history, parallel loading, resilience to source changes, easy to add sources. Cons: many tables and joins, not directly usable by analysts (needs marts), and more complex to implement and query without automation.

#### What is the "raw vault" versus "business vault" in Data Vault?

The raw vault stores source data as-is in hubs, links and satellites; the business vault adds derived structures with business rules (computed satellites, point-in-time and bridge tables) to simplify building marts.

#### What are point-in-time (PIT) tables in Data Vault?

Helper tables that store, for each hub key and snapshot date, the matching satellite load dates, making it fast to assemble the state of an entity at a point in time for dimensions.

#### What is a "persistent staging area"?

A staging layer that keeps all historical extracts (often insert-only with load timestamps) instead of truncating each run, allowing rebuilds of downstream layers without re-extracting from sources.

#### How would you design the warehouse for a company acquiring other companies frequently?

An integration layer resilient to new sources (Data Vault or a well-structured core with source mapping tables), conformed dimensions with master data matching across companies, source system codes on every row, and marts that can include or exclude acquired entities.

<!-- challenge -->

After each acquisition, the core model must be redesigned to fit the new company's customer data. How would Data Vault change that?

<!-- solution -->

New sources load into new satellites (and links) attached to the existing customer hub via business keys or mapping; existing tables stay untouched. Marts then combine satellites with agreed business rules.

<!-- takeaways -->

- Hubs, links and satellites separate keys, relationships and history.
- New sources add tables instead of reshaping old ones.
- Marts and PIT tables make vaults usable.

<!-- unit: Serving and alternative architectures -->

<!-- goals -->

- Place the medallion architecture and semantic layers in warehousing.
- Know OLAP cubes, virtualization and real-time warehouses.

<!-- concept -->

Modern platforms keep the warehouse's ideas while changing the technology. Medallion layers in a lakehouse map onto staging, integration and marts. Semantic layers define metrics once for every BI tool, doing what OLAP cubes did with precomputed aggregates.

Two alternatives trade storage for other things: virtualization queries sources in place without copying, and real-time warehouses ingest continuously so reports are minutes old instead of a day.

<!-- example -->

| Classic | Modern equivalent |
|---|---|
| Staging | Bronze |
| Integration layer | Silver |
| Data marts | Gold |
| OLAP cube | Semantic layer + columnar engine |

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

<!-- challenge -->

Three BI tools compute "gross margin" in three different ways. Which architectural piece fixes it?

<!-- solution -->

A semantic layer (or metrics layer) that defines gross margin once, with its formula and dimensions, consumed by all three tools, so every report uses the same calculation.

<!-- takeaways -->

- Medallion layers mirror classic warehouse layers.
- Semantic layers define metrics once for all tools.
- Virtualization and streaming trade copies for freshness.

<!-- stage: Dimensional modeling -->

### Dimensional modeling basics

<!-- unit: Designing a dimensional model -->

<!-- goals -->

- Apply Kimball's four design steps.
- Declare the grain and choose dimensions from business questions.

<!-- concept -->

Dimensional design starts from a business process, not from source tables. Once the process is chosen, the most important decision is the grain: exactly what one row means. Everything else follows. Dimensions are the who, what, where and when that describe each row; facts are the numbers measured at that grain.

Choosing the most atomic grain keeps the model useful for questions nobody has asked yet, since any summary can be built from detail but not the reverse.

<!-- example -->

```text
1. Process:    order taking
2. Grain:      one row per order line
3. Dimensions: date, customer, product, store, promotion
4. Facts:      quantity, gross_amount, discount_amount, net_amount
```

#### What is dimensional modeling?

Ralph Kimball's technique for designing analytical schemas around business processes: facts (measurements of events) surrounded by dimensions (descriptive context). It favors understandability and query performance over normalization.

#### What are Kimball's four steps of dimensional design?

1) Select the business process (for example order taking). 2) Declare the grain (what one fact row represents). 3) Identify the dimensions (who, what, where, when, why, how). 4) Identify the facts (numeric measurements at that grain).

#### What is the grain of a fact table?

The precise definition of what a single row represents, for example "one row per order line" or "one row per account per day". It must be declared before choosing dimensions and facts, and all rows must share the same grain.

#### Why should you model at the most atomic grain possible?

Atomic data can answer any question by aggregating, including questions not anticipated; aggregated facts can't be broken down. Aggregates can be added later for performance.

#### What questions help identify dimensions?

Who (customer, employee), what (product, service), where (store, region, channel), when (date, time), why (promotion, reason code) and how (payment method, shipping mode), as they appear in the business process's events.

<!-- challenge -->

A stakeholder asks for a table of "daily sales by store". Which grain do you build, and why?

<!-- solution -->

The atomic grain, one row per order line, with daily-by-store as an aggregate or view on top. The atomic table also answers product, customer and promotion questions that will follow.

<!-- takeaways -->

- Start from a business process.
- Declare the grain before anything else.
- Atomic grain answers future questions.

<!-- unit: Facts, dimensions and schemas -->

<!-- goals -->

- Distinguish fact and dimension tables.
- Compare star and snowflake schemas and name objects clearly.

<!-- concept -->

A dimensional model has two kinds of tables. Fact tables are long and narrow: keys plus measurements, one row per event at the grain. Dimension tables are wide and short: descriptive attributes used to filter and group.

Arranging dimensions directly around the fact gives a star, which is simple for users and fast in columnar engines. Normalizing dimensions into sub-tables gives a snowflake, which saves little space and adds joins. Clear business names complete a model people can use without help.

<!-- example -->

```text
             dim_date
                │
dim_customer ─ fct_order_lines ─ dim_product
                │
             dim_store
```

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

#### How do you name tables and columns in a dimensional model?

Consistently and in business language: `fct_` and `dim_` prefixes (or `fact_`/`dim_`), singular nouns, `_key` for surrogate keys, `_id` for natural keys, explicit units (`amount_eur`), and no source system jargon in presentation layers.

<!-- challenge -->

A product dimension was snowflaked into product, subcategory, category and department tables. Analysts complain about joins. What do you do?

<!-- solution -->

Flatten the hierarchy into the product dimension (category and department as columns). Storage cost is negligible in columnar engines, and queries need one join instead of four.

<!-- takeaways -->

- Facts hold measurements; dimensions hold context.
- Stars are simpler and usually faster than snowflakes.
- Business-friendly names make models usable.

<!-- unit: Keys -->

<!-- goals -->

- Explain surrogate and natural keys and why facts use surrogates.
- Decide how to enforce referential integrity.

<!-- concept -->

Source systems identify things with natural keys, which can change, be reused or collide when sources merge. The warehouse issues its own surrogate keys for dimension rows, which also lets one natural key have several historical versions.

Facts point to dimensions through those surrogate keys. Every fact should reference an existing dimension row, so loads look up keys and fall back to an unknown member rather than leaving orphans.

<!-- example -->

```text
dim_customer
customer_key | customer_number | segment | valid_from | valid_to
1001         | C-552           | SMB     | 2024-01-01 | 2026-03-31
1874         | C-552           | Mid     | 2026-04-01 | 9999-12-31
fct_orders.customer_key → 1001 for 2025 orders, 1874 for 2026 orders
```

#### What is a surrogate key?

A meaningless integer (or hash) key generated in the warehouse to identify a dimension row, independent of source system keys. It enables history (several rows per natural key), integration of multiple sources and protection from source key changes.

#### What is a natural (business) key?

The identifier from the source system or business (customer number, SKU, IBAN). It's kept as an attribute in the dimension, alongside the surrogate key, to trace rows back to sources.

#### Why use surrogate keys instead of natural keys in facts?

Natural keys can change, be reused, collide across sources, or be long strings. Surrogate keys support SCD Type 2 history (facts point to the version valid at the time), keep facts compact and allow special rows like "unknown".

#### Should a fact table have foreign key constraints?

Logically yes: every fact must reference an existing dimension row (or the unknown member). Physically, many warehouses don't enforce constraints for load performance, so referential integrity is checked with tests instead.

<!-- challenge -->

Two acquired companies both have a customer `C-100`, different people. Facts keyed by customer number now mix them. What do you change?

<!-- solution -->

Issue surrogate keys in the customer dimension and keep the natural key together with a source system column (`source`, `customer_number`) as the business key. Facts then reference the surrogate.

<!-- takeaways -->

- Surrogate keys are stable and source-independent.
- Natural keys stay as attributes with their source.
- Facts must always reference a dimension row.

<!-- unit: Shared and time dimensions -->

<!-- goals -->

- Build conformed dimensions and plan with a bus matrix.
- Design date and time-of-day dimensions.

<!-- concept -->

Integration in a Kimball warehouse happens through conformed dimensions: the same customer, product and date tables shared by every fact. The bus matrix plans this by listing business processes against the dimensions they use, which shows which dimensions to build first.

The date dimension is the most shared of all. It carries calendar and fiscal attributes so no report recalculates them. Time of day, when needed, is a separate small dimension.

<!-- example -->

| Process \ Dimension | Date | Customer | Product | Store | Employee |
|---|---|---|---|---|---|
| Orders | X | X | X | X | |
| Returns | X | X | X | X | |
| Inventory | X | | X | X | |
| Payroll | X | | | X | X |

#### What is a conformed dimension?

A dimension shared with the same keys, attributes and meaning across several fact tables and marts (one `dim_customer`, one `dim_date`), so metrics from different processes can be compared and combined (drill-across).

#### What is the enterprise data warehouse bus matrix?

A planning grid with business processes as rows and conformed dimensions as columns, marking which dimensions each process uses. It guides incremental development of marts that integrate through conformed dimensions.

#### What is the date dimension, and why is it important?

A dimension with one row per day and attributes like day of week, month, quarter, fiscal periods, holidays and working-day flags. It makes time analysis easy and consistent and avoids complex date logic in every query.

#### Why is the date dimension key often in YYYYMMDD format?

An integer like `20261015` is readable, sorts correctly, makes partition pruning intuitive, and can be derived from a date without a lookup; it's a common exception to meaningless surrogate keys.

#### What is a time-of-day dimension?

A separate dimension with one row per minute or second of the day (hour, minute, day part), used when time-of-day analysis matters, keeping the date dimension small.

<!-- challenge -->

Every report computes fiscal quarters with its own CASE expression, and two disagree. What do you add?

<!-- solution -->

Fiscal attributes (fiscal year, quarter, week) in the date dimension, computed once and joined by every fact, so reports use the same calendar.

<!-- takeaways -->

- Conformed dimensions integrate marts.
- The bus matrix plans shared dimensions.
- The date dimension centralizes calendar logic.

<!-- unit: Combining facts -->

<!-- goals -->

- Combine measures from several fact tables correctly.
- Explain why direct fact-to-fact joins double count.

<!-- concept -->

Different processes produce different fact tables, often at different grains: orders per line, returns per return line, targets per month. Joining them directly multiplies rows wherever keys repeat, inflating totals.

The safe method is drill-across: aggregate each fact to a common set of conformed dimensions first, then combine the results. Conformed dimensions are what make that possible.

<!-- example -->

```sql
WITH s AS (SELECT date_key, product_key, SUM(net_amount) AS sales   FROM fct_order_lines GROUP BY 1, 2),
     r AS (SELECT date_key, product_key, SUM(refund_amount) AS returns FROM fct_returns     GROUP BY 1, 2)
SELECT COALESCE(s.date_key, r.date_key) AS date_key, COALESCE(s.product_key, r.product_key) AS product_key,
       s.sales, r.returns
FROM s FULL OUTER JOIN r ON s.date_key = r.date_key AND s.product_key = r.product_key;
```

#### What is drill-across?

Combining measures from different fact tables (sales and returns) in one report by querying each separately at a common grain of conformed dimensions and joining the results, rather than joining facts directly.

#### Why shouldn't you join two fact tables directly?

Their grains usually differ, and direct joins produce fan-outs and double counting. Aggregate each fact to the common dimensional grain first, then combine.

<!-- challenge -->

A report joins `fct_orders` to `fct_shipments` on `order_id`, and revenue is 40% higher than in finance. Why?

<!-- solution -->

Orders with several shipments repeat their revenue once per shipment row. Aggregate each fact to the order (or to shared dimensions) first, then join the aggregated results.

<!-- takeaways -->

- Facts at different grains multiply when joined.
- Drill-across aggregates first, then combines.
- Conformed dimensions make drill-across possible.

### Facts in depth

<!-- unit: Types of fact tables -->

<!-- goals -->

- Choose between transaction, periodic snapshot and accumulating snapshot facts.
- Use factless facts and decide when snapshots beat derivation.

<!-- concept -->

Business processes measure different things. Events (an order line) suit transaction facts, one row per event. Levels and states (an inventory level, an account balance) suit periodic snapshots, one row per period. Processes with milestones (order placed, paid, shipped, delivered) suit accumulating snapshots, one row per instance updated as it progresses.

Some facts have no measure at all, recording only that something happened or could have.

<!-- example -->

| Process | Fact type | Grain |
|---|---|---|
| Sales | Transaction | Order line |
| Inventory | Periodic snapshot | Product × store × day |
| Order fulfillment | Accumulating snapshot | Order, with milestone dates |
| Class attendance | Factless | Student × class × date |

#### What are the three types of fact tables?

Transaction facts (one row per event, like an order line), periodic snapshot facts (one row per entity per period, like account balance per day) and accumulating snapshot facts (one row per process instance updated as it moves through milestones, like an order from placement to delivery).

#### When do you use a periodic snapshot fact table?

To measure levels or states at regular intervals (inventory, balances, subscriptions active per month), where summing transactions would be expensive or where the state isn't derivable from events.

#### What is an accumulating snapshot fact table?

A fact table with one row per instance of a process with a defined start and end (order fulfillment, loan application, claim), with multiple date keys for milestones and lag measures between them; rows are updated as milestones occur.

#### What is a factless fact table?

A fact table with only dimension keys and no numeric measures, recording that an event happened (student attended class) or coverage (which products were on promotion in which stores), counted with `COUNT(*)`.

#### When should you use a periodic snapshot instead of deriving state from transactions?

When computing state from all historical transactions is expensive or complex (balances, inventory levels, open tickets), or when source systems provide states but not complete event histories.

<!-- challenge -->

The business asks "how long does each step of order fulfillment take, and where do orders get stuck?" Which fact type fits?

<!-- solution -->

An accumulating snapshot with one row per order, a date key per milestone (placed, paid, shipped, delivered) and lag measures between them, updated as each milestone happens.

<!-- takeaways -->

- Events: transaction facts. Levels: periodic snapshots.
- Milestone processes: accumulating snapshots.
- Factless facts record occurrences or coverage.

<!-- unit: Measures and additivity -->

<!-- goals -->

- Classify facts as additive, semi-additive or non-additive.
- Store ratios, currencies, cancellations and returns correctly.

<!-- concept -->

How a measure can be summed decides how it's stored. Amounts add across everything; balances add across accounts but not across days; ratios and percentages don't add at all. Storing the additive components and computing ratios at query time keeps every aggregation correct.

Two common business cases follow the same logic: currencies, which need both original and converted amounts, and cancellations and returns, which must reduce totals in a way that still sums.

<!-- example -->

```sql
-- margin % computed from additive parts, correct at any level
SELECT category, SUM(revenue) AS revenue, SUM(cost) AS cost,
       (SUM(revenue) - SUM(cost)) / NULLIF(SUM(revenue), 0) AS margin_pct
FROM fct_sales JOIN dim_product USING (product_key)
GROUP BY category;
```

#### What are additive, semi-additive and non-additive facts?

Additive facts can be summed across all dimensions (sales amount). Semi-additive facts can be summed across some dimensions but not time (account balance: sum across accounts, average or last over time). Non-additive facts can't be summed (ratios, percentages, unit prices); store their components instead.

#### How should you store ratios like margin percentage?

Store the additive components (revenue and cost) in the fact table and compute the ratio at query time (`SUM(revenue - cost) / SUM(revenue)`), because averaging percentages gives wrong results.

#### How do you model currency in fact tables?

Store amounts in the transaction currency with a currency key, plus converted amounts in a reporting currency using the exchange rate valid on the transaction date (from a rate table), so reports can show both.

#### How do you model cancellations and returns?

Either as negative rows in the same transaction fact (simple sums), or as a separate returns fact with its own grain and reasons; accumulating snapshots can track status changes for orders.

<!-- challenge -->

A dashboard averages a stored `margin_pct` column across products and shows a margin the CFO disputes. What is wrong?

<!-- solution -->

Margin percentage is non-additive; averaging ratios ignores revenue weights. Store revenue and cost, and compute margin from their sums at the chosen level.

<!-- takeaways -->

- Additivity decides how measures aggregate.
- Store components; compute ratios at query time.
- Keep original and converted currency amounts.

<!-- unit: Grain, keys and degenerate dimensions -->

<!-- goals -->

- Keep one grain per fact table and define its key.
- Use degenerate and audit dimensions and load late-arriving facts.

<!-- concept -->

A fact table's grain is a promise every row must keep. Mixing order-header amounts with order-line amounts in one table breaks sums. Identifiers like order numbers stay in the fact as degenerate dimensions, with no table of their own, and together with dimension keys they form the fact's key.

Facts also need to explain themselves: audit columns record how each row was loaded, and late-arriving facts must land in the right period with the dimension versions valid when they happened.

<!-- example -->

```text
fct_order_lines
  order_number (degenerate), line_number, date_key, customer_key, product_key,
  quantity, net_amount,
  batch_id, loaded_at, source_system          ← audit
key: (order_number, line_number)
```

#### What is a degenerate dimension?

A dimension key stored in the fact table without its own dimension table, typically a transaction identifier like an order number or invoice number, used for grouping lines and drill-through.

#### How do you handle facts with different grains?

Put them in separate fact tables; mixing grains (order header amounts and order line amounts in one table) causes double counting. Allocate header-level values to lines only if a business rule supports it.

#### What is a fact table's primary key?

Often the combination of its dimension keys plus degenerate dimensions at the declared grain, or a surrogate fact key for convenience. Enforcing uniqueness at the grain with a test is essential.

#### What is a fact table's "audit dimension"?

A dimension or set of columns describing how each fact row was loaded (batch ID, load timestamp, source file, data quality status), which supports debugging and lineage.

#### What are late-arriving facts?

Fact rows that arrive after their event date (delayed transactions). They must be loaded with the dimension versions that were valid at the event time, not the current ones, by looking up SCD2 rows with the event date.

<!-- challenge -->

Shipping cost is known per order, but the fact table is per order line. Analysts sum it and get inflated totals. What are your options?

<!-- solution -->

Keep shipping in a separate order-grain fact, or allocate it to lines (for example by line amount) so it sums correctly at line grain. Never repeat the order value on every line.

<!-- takeaways -->

- One grain per fact table.
- Degenerate dimensions keep transaction IDs in the fact.
- Audit columns and late-fact handling keep facts trustworthy.

<!-- unit: Large and aggregated facts -->

<!-- goals -->

- Manage fact tables with billions of rows.
- Use aggregate and consolidated fact tables.

<!-- concept -->

Fact tables grow without end. Partitioning by date and clustering on common filters keep queries reading a small part, and incremental loads keep processing proportional to new data.

Aggregates trade storage for speed: a summarized copy at a coarser grain answers frequent questions quickly, as long as it's rebuilt from the atomic facts. Consolidated facts go the other way, combining processes at a shared grain such as actuals and budget by month, to make comparisons easy.

<!-- example -->

```sql
CREATE TABLE agg_sales_month_category AS
SELECT d.year_month, p.category, SUM(f.net_amount) AS net_amount, SUM(f.quantity) AS quantity
FROM fct_order_lines f
JOIN dim_date d USING (date_key) JOIN dim_product p USING (product_key)
GROUP BY 1, 2;
```

#### What are aggregate fact tables?

Pre-summarized versions of atomic facts at a coarser grain (sales by month and category) that speed up common queries. They must be kept consistent with the atomic table, and BI tools or semantic layers can route queries to them.

#### What is a consolidated fact table?

A fact table combining facts from several processes at the same grain (actual and budget amounts by month, account and cost center), convenient for comparisons like actual versus plan.

#### How large can fact tables get, and how do you manage them?

Billions of rows are common. Manage them with partitioning by date, clustering on common filters, compression, incremental loads, retention policies, and aggregates for frequent queries.

<!-- challenge -->

Finance compares monthly actual sales with budget, which exists only by month and category. How do you model it?

<!-- solution -->

A consolidated fact at month × category grain with actual (aggregated from atomic sales) and budget columns, using conformed date and product dimensions (a shrunken product dimension at category level).

<!-- takeaways -->

- Partition and cluster large facts; load incrementally.
- Aggregates speed frequent questions.
- Consolidated facts compare processes at a shared grain.

### Dimensions in depth

<!-- unit: Specialized dimensions -->

<!-- goals -->

- Use role-playing, junk, mini, outrigger, shrunken and static dimensions.
- Separate fast-changing attributes from slowly changing ones.

<!-- concept -->

Real models need a few dimension patterns beyond the basic table. One date dimension can play several roles in a fact. Leftover flags collapse into one junk dimension instead of cluttering the fact. Attributes that change too fast for history in a big dimension move to a mini-dimension. Some dimensions reference others, are shrunken versions for aggregates, or are generated rather than loaded.

Each pattern exists to keep the fact narrow and the dimensions manageable.

<!-- example -->

```text
fct_orders: order_date_key, ship_date_key, delivery_date_key → dim_date (role-playing)
            order_flags_key → dim_order_flags (gift_wrap, express, coupon_used) (junk)
            customer_key → dim_customer (SCD2: segment)
            customer_profile_key → dim_customer_profile (age band, income band) (mini)
```

#### What is a role-playing dimension?

One physical dimension used several times in a fact table with different meanings, typically the date dimension as order date, ship date and delivery date, exposed through views or aliases.

#### What is a junk dimension?

A dimension combining several low-cardinality flags and indicators (payment type, gift wrap flag, channel) into one table of their combinations, avoiding many tiny dimensions or wide fact tables.

#### What is a mini-dimension?

A separate dimension for rapidly changing attributes of a large dimension (customer age band, income band, credit score band), so the main dimension doesn't explode with SCD2 rows; the fact table references both.

#### What is an outrigger dimension?

A dimension referenced by another dimension instead of by the fact table (for example a customer's first purchase date pointing to the date dimension). It's allowed sparingly; too many become snowflaking.

#### What is a shrunken dimension?

A subset of a dimension's rows or columns used for aggregate facts at a higher grain, such as a month dimension derived from the date dimension or a category dimension derived from products.

#### What is a static dimension?

A dimension whose content doesn't come from a source and rarely changes, such as the date dimension, status code lookups or currencies, generated once or maintained manually.

#### A dimension must keep history of customer segment changes but customer address changes daily. What do you do?

Track segment as SCD2 in the customer dimension; put address in a separate dimension or mini-dimension, or keep it type 1 if history isn't needed for analysis, to avoid daily row explosion.

<!-- challenge -->

A fact table has 12 yes/no flag columns that analysts rarely use and that bloat the table. What do you do?

<!-- solution -->

Create a junk dimension with one row per observed flag combination, replace the 12 columns with one key, and keep the flags available as descriptive attributes.

<!-- takeaways -->

- Role-playing reuses one dimension for several meanings.
- Junk dimensions absorb miscellaneous flags.
- Mini-dimensions isolate fast-changing attributes.

<!-- unit: Hierarchies and many-to-many -->

<!-- goals -->

- Model fixed and ragged hierarchies.
- Resolve many-to-many relationships with bridge tables.

<!-- concept -->

Dimensions often contain hierarchies. Fixed ones, with known levels, flatten into columns. Ragged or recursive ones, like org charts, need more structure, often a bridge listing every ancestor-descendant pair.

Many-to-many relationships, such as accounts with several holders or customers with several interests, also need bridges. Weights on bridge rows let measures be allocated without double counting.

<!-- example -->

```text
bridge_account_holder (account_key, customer_key, weight)
  A1, C1, 0.5
  A1, C2, 0.5
fct_balances.account_key → bridge → dim_customer   (SUM(balance * weight) per customer)
```

#### What is a bridge table?

A table resolving many-to-many relationships between facts and dimensions, such as accounts with multiple holders or diagnoses per hospital visit, often with weighting factors so amounts aren't double counted.

#### How do you model hierarchies in dimensions?

Fixed-depth hierarchies (category → subcategory → product) as flattened columns in the dimension. Ragged or variable-depth hierarchies (organization charts, bills of materials) with parent-child keys plus a bridge table of all ancestor-descendant pairs for easy rollups.

#### How do you handle multi-valued attributes like customer interests?

With a bridge table between the dimension and a group or attribute dimension, or by storing an array column where the engine supports it and queries can unnest it; avoid encoding several values in a comma-separated string.

<!-- challenge -->

Joint accounts have two holders, and balance by customer counts each joint balance twice. How do you report correctly?

<!-- solution -->

Use a bridge with allocation weights (0.5 each, or by ownership share) and sum balance × weight per customer. Show unweighted totals only in reports that explicitly want "exposure per holder".

<!-- takeaways -->

- Flatten fixed hierarchies; bridge ragged ones.
- Bridges resolve many-to-many relationships.
- Weights prevent double counting.

<!-- unit: Integrating and conforming dimensions -->

<!-- goals -->

- Merge customer data from several systems into one dimension.
- Use unknown members, MDM and conformed attributes.

<!-- concept -->

A customer dimension built from CRM, billing and support must decide which records describe the same customer and which values win. Master data management supplies matching and a golden record; without it, the warehouse does a simpler version itself.

Two small conventions keep the result usable: an unknown member row for facts whose dimension is missing, so nothing drops out of joins, and conformed attributes that mean the same thing everywhere.

<!-- example -->

```text
dim_customer
customer_key | master_id | crm_id | billing_id | segment | country
-1           | -1        | n/a    | n/a        | Unknown | Unknown   ← unknown member
1874         | M-552     | C-552  | B-9917     | Mid     | ES
```

#### What is the "unknown member" row?

A special dimension row (often surrogate key `-1` or `0`) used when a fact's dimension is missing or not yet known, so facts aren't dropped by inner joins and the issue is visible in reports.

#### How do you handle customer data coming from several systems?

Match and merge records into one conformed customer dimension using a master key (from master data management or matching rules on emails, IDs, names), keep source keys as attributes or in a mapping table, and define survivorship rules for conflicting attributes.

#### What is master data management (MDM)?

Processes and tools that create and maintain a single, authoritative version of core entities (customers, products, suppliers) across systems, which feeds conformed dimensions.

#### What is a "conformed attribute"?

An attribute with the same name, meaning and allowed values everywhere it appears, such as a standard country code or product category list, enabling consistent filtering across marts.

<!-- challenge -->

5% of sales have no matching customer because the CRM sync lags. Reports grouped by customer silently lose those sales. Fix it.

<!-- solution -->

Map unmatched facts to the unknown member (or create inferred members with the natural key) so totals stay complete, and update the key when the customer arrives. Monitor the share of unknown keys.

<!-- takeaways -->

- Merge sources into one conformed customer dimension.
- Unknown members keep facts from disappearing.
- Conformed attributes mean the same everywhere.

### Slowly changing dimensions

<!-- unit: SCD types -->

<!-- goals -->

- Explain SCD types 0, 1, 2, 3 and 6.
- Choose a change policy per attribute.

<!-- concept -->

Dimension attributes change: customers move, products are recategorized. Each attribute needs a decision: should reports see history or only the current value? Type 1 overwrites, so all history follows today's value. Type 2 keeps versions, so facts stay tied to what was true when they happened. Type 3 keeps one previous value; type 6 combines history with current columns.

The choice is per attribute, so most dimensions mix policies.

<!-- example -->

| Attribute | Policy | Why |
|---|---|---|
| Name spelling fix | Type 1 | Correction, no history needed |
| Customer segment | Type 2 | Sales must stay with the old segment |
| Previous region (one-off reorg) | Type 3 | Compare old vs new |
| Birth date | Type 0 | Never changes |

#### What is a slowly changing dimension?

A dimension whose attributes change over time unpredictably (a customer moves, a product changes category), requiring a policy for whether and how to keep history.

#### What are the SCD types?

Type 0: never change (keep original). Type 1: overwrite, no history. Type 2: add a new row per change with validity dates. Type 3: add a "previous value" column. Type 4: history in a separate table (mini-dimension or history table). Type 6: hybrid of 1, 2 and 3 (current value columns on all rows plus history rows). Type 7: dual keys to join to either current or historical rows.

#### What is SCD Type 1, and when is it appropriate?

Overwriting attributes with new values, losing history. Appropriate for corrections (fixing a typo) and attributes where history doesn't matter for analysis.

#### What is SCD Type 3, and why is it rare?

Adding a column for the previous value (`previous_region`) to allow comparisons between current and prior assignments. It keeps only one level of history, so it's limited to specific reorganization analyses.

#### What is SCD Type 6?

A hybrid where the dimension keeps type 2 history rows and also type 1 "current" columns updated on all rows of the same natural key, so you can report facts both as they were and with today's attribute values.

#### What is a dimension's "type 1" attribute in a mixed dimension?

Dimensions can mix policies per attribute: some columns are overwritten (type 1, corrections), others tracked historically (type 2, meaningful changes). Decide per attribute with business users.

<!-- challenge -->

Sales managers want last year's sales by the region the customer was in at the time, but also by today's region. Which SCD approach supports both?

<!-- solution -->

Type 2 on region for historical versions, plus a type 1 `current_region` column on every version (type 6), so reports can group by either.

<!-- takeaways -->

- Choose a change policy per attribute.
- Type 2 preserves history; type 1 overwrites.
- Type 6 offers historical and current views together.

<!-- unit: Implementing Type 2 -->

<!-- goals -->

- Implement SCD2 with SQL, hash diffs and dbt snapshots.
- Choose validity dates, current flags and granularity.

<!-- concept -->

An SCD2 load compares incoming records with current versions. When tracked attributes change, it closes the current row and inserts a new one with a fresh surrogate key. Hashing the tracked attributes makes change detection one comparison instead of many.

Conventions keep queries simple: a far-future end date instead of `NULL`, a current flag, and a view of current rows. Whether validity is tracked by day or timestamp depends on how often changes happen.

<!-- example -->

```sql
-- close changed current rows
UPDATE dim_customer d SET valid_to = s.change_date - 1, is_current = false
FROM stg_customer s
WHERE d.customer_number = s.customer_number AND d.is_current AND d.hash_diff <> s.hash_diff;
-- insert new versions
INSERT INTO dim_customer (customer_number, segment, region, hash_diff, valid_from, valid_to, is_current)
SELECT s.customer_number, s.segment, s.region, s.hash_diff, s.change_date, DATE '9999-12-31', true
FROM stg_customer s
LEFT JOIN dim_customer d ON d.customer_number = s.customer_number AND d.is_current
WHERE d.customer_number IS NULL OR d.hash_diff <> s.hash_diff;
```

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

#### What is a hash diff, and why use it?

A hash (MD5, SHA) of the concatenated tracked attributes, stored on each row, so detecting changes is a single comparison instead of comparing many columns, including null-safe handling.

#### How do dbt snapshots implement SCD2?

A snapshot config defines the unique key and a strategy (`timestamp` using an updated-at column, or `check` comparing columns); each run compares source with the snapshot table and closes and inserts rows, adding `dbt_valid_from` and `dbt_valid_to`.

#### What is a "current view" of an SCD2 dimension?

A view filtering `is_current = true` that gives one row per natural key with today's attributes, used by analysts who don't need history and for type 1 style reporting.

#### What is a "type 2 with effective timestamp" versus date granularity?

Some dimensions track changes at timestamp precision (several changes per day), others at day level (latest value of the day). Choose based on how facts are matched; day granularity is simpler and usually enough.

<!-- challenge -->

An SCD2 dimension creates a new version every day for most customers, though nothing visible changes. What is the likely cause?

<!-- solution -->

The hash includes an attribute that changes daily (a `last_login` or load timestamp) or unnormalized values (trailing spaces, case). Hash only tracked business attributes, normalized; move volatile ones to type 1 or a separate table.

<!-- takeaways -->

- SCD2 closes old rows and inserts new versions.
- Hash diffs make change detection cheap.
- Far-future end dates and current flags simplify queries.

<!-- unit: Using and maintaining SCD2 -->

<!-- goals -->

- Look up the right dimension version when loading facts.
- Handle late changes, large dimensions and testing.

<!-- concept -->

History is only useful if facts point to the right version. Fact loads look up the version whose validity range contains the event date; reporting "as of today" goes through the current view instead of rewriting facts.

Over time SCD2 brings its own problems: changes that arrive late and must be inserted in the past, dimensions that grow too fast, and subtle errors like overlapping ranges. Tests on the dimension's structure catch most of them.

<!-- example -->

```sql
-- each natural key: exactly one current row, no overlapping ranges
SELECT customer_number FROM dim_customer GROUP BY 1 HAVING SUM(CASE WHEN is_current THEN 1 ELSE 0 END) <> 1;
SELECT a.customer_number FROM dim_customer a JOIN dim_customer b
  ON a.customer_number = b.customer_number AND a.customer_key < b.customer_key
 AND a.valid_from <= b.valid_to AND b.valid_from <= a.valid_to;
```

#### How do you join facts to an SCD2 dimension for a point-in-time lookup?

During fact loading, look up the dimension row whose validity range contains the event date: `ON f.customer_id = d.customer_id AND f.event_date >= d.valid_from AND f.event_date < d.valid_to`, and store that surrogate key in the fact.

#### Can facts be reassigned to new dimension versions?

Normally not: facts keep the version valid when they happened. For "as of today" reporting, join through the natural key to the current row or use type 6 current-value columns.

#### How do you handle a late-arriving dimension change?

If you learn today that a change happened last month, insert the version with its real start date, adjust the previous row's end date, and possibly re-point facts that occurred after the change to the new surrogate key, which is why some teams prefer point-in-time joins at query time.

#### What problems does SCD2 cause in large dimensions?

Row explosion when attributes change often, slower joins, and complex point-in-time logic. Mitigations: track only meaningful attributes, move volatile attributes to mini-dimensions, and use hash comparisons for change detection.

#### How do you test an SCD2 dimension?

Check that each natural key has exactly one current row, validity ranges don't overlap or leave gaps, `valid_from < valid_to`, surrogate keys are unique, and facts' surrogate keys exist in the dimension.

<!-- challenge -->

You learn today that a customer changed segment on 1 March, but you already loaded March sales against the old version. What do you do?

<!-- solution -->

Insert the new version with valid_from 1 March, close the old one on 28 February, and re-point March facts for that customer to the new surrogate key. Keep the correction logged.

<!-- takeaways -->

- Facts link to the version valid at event time.
- Late changes may require re-pointing facts.
- Test for one current row and no overlaps.

<!-- stage: Building the warehouse -->

### Loading the warehouse

<!-- unit: Full, incremental and CDC loads -->

<!-- goals -->

- Choose between full, incremental and CDC extraction.
- Track progress with watermarks and control tables.

<!-- concept -->

Reloading everything every night is simple until it isn't: volumes grow and windows shrink. Incremental loads take only what changed since last time, tracked by a watermark stored in a control table. Timestamp-based extraction relies on sources updating their timestamps; log-based CDC reads every change, deletes included, without touching tables.

Who initiates the transfer, the warehouse pulling or the source pushing, decides where scheduling and failure handling live.

<!-- example -->

```sql
SELECT * FROM src.orders
WHERE updated_at > (SELECT last_watermark FROM etl_control WHERE pipeline = 'orders')
  AND updated_at <= :run_started_at;
UPDATE etl_control SET last_watermark = :run_started_at WHERE pipeline = 'orders';
```

#### What is a full load versus an incremental load?

A full load reloads all data every run (simple, expensive, fine for small tables). An incremental load processes only new or changed data since the last run (by timestamp, sequence or CDC), which is necessary for large tables.

#### What is change data capture (CDC)?

Capturing inserts, updates and deletes from a source database, typically by reading its transaction log (binlog, WAL, redo log) with tools like Debezium, DMS, GoldenGate or Fivetran, and applying them to the warehouse.

#### Why is log-based CDC preferred over timestamp-based extraction?

It captures every change including deletes, doesn't depend on applications maintaining `updated_at` correctly, adds little load on the source, and preserves the order of changes.

#### What is a watermark in incremental loading?

The highest timestamp or sequence value processed in the last run, stored in a control table and used to select new rows next time; use an overlap window to catch late-committed rows and deduplicate.

#### What is a control table in ETL?

A table storing metadata for each pipeline run: watermarks, batch IDs, start and end times, row counts, status and errors, used for incremental loading, restarts and monitoring.

#### What is the difference between push and pull ingestion?

Pull: the warehouse side extracts from sources on a schedule (queries, APIs). Push: sources send data as events or files (CDC streams, webhooks, file drops). Push reduces latency and source load; pull is simpler to control.

<!-- challenge -->

An incremental load by `updated_at` never removes orders deleted in the source. What are your options?

<!-- solution -->

Switch to log-based CDC to receive delete events, or periodically compare full key lists with the source to detect missing keys, then mark them deleted (soft delete) in the warehouse.

<!-- takeaways -->

- Incremental loads scale; full loads are simple.
- Watermarks and control tables track progress.
- Log-based CDC captures deletes too.

<!-- unit: Loading dimensions and facts -->

<!-- goals -->

- Load dimensions and facts in the right order with key lookups.
- Handle inferred members and source deletes.

<!-- concept -->

Order matters: dimensions load first so facts can find surrogate keys. Dimension loads clean and deduplicate by natural key, then apply change policies. Fact loads look up keys for every dimension, at the version valid on the event date.

When a fact references a customer the warehouse hasn't seen yet, an inferred member keeps the fact loaded and gets filled in later. Deletes from sources need a policy too: physical removal or a deleted flag.

<!-- example -->

```text
1. load dim_date (static), dim_product, dim_customer (SCD2)
2. load fct_order_lines:
   customer_key ← lookup(customer_number, order_date)  or inferred member if missing
   product_key  ← lookup(sku, order_date)              or -1 (unknown)
```

#### How do you load a dimension?

Extract and clean source records, deduplicate per natural key, generate or look up surrogate keys, apply the SCD policy per attribute, add the unknown member, and run tests on uniqueness of current natural keys.

#### How do you load a fact table?

Extract transactions at the declared grain, look up dimension surrogate keys (point-in-time for SCD2, unknown member when missing), compute derived measures, and insert or merge idempotently into the fact table, usually partitioned by date.

#### What is the order of loading in a warehouse?

Dimensions first, then facts, so facts can find their surrogate keys. Late-arriving dimension members are handled with inferred members or unknown rows and fixed later.

#### What is an inferred member?

A placeholder dimension row created when a fact arrives with a natural key not yet in the dimension, with the natural key and default attributes, updated once the real dimension data arrives.

#### How do you handle deletes from sources?

With CDC delete events or by comparing full extracts to find missing keys; then either physically delete, or soft-delete with an `is_deleted` flag and deletion date to keep history, depending on business and compliance needs.

<!-- challenge -->

Orders arrive for new customers a few hours before the CRM sends their details, and those orders get the unknown key permanently. What do you change?

<!-- solution -->

Create inferred members: insert a placeholder customer row with the natural key when a fact references an unknown customer, and update it (type 1) when CRM details arrive. Facts keep the right key from the start.

<!-- takeaways -->

- Load dimensions before facts.
- Look up keys at the event date.
- Inferred members handle early-arriving facts.

<!-- unit: Idempotent and repeatable loads -->

<!-- goals -->

- Make loads idempotent with MERGE or delete-insert.
- Run backfills and reconcile results with sources.

<!-- concept -->

Every load will be rerun someday: after a failure, a fix or late data. A load is safe to rerun only if running it twice gives the same result, which means replacing its slice of data rather than appending. `MERGE` on the grain key or deleting and reinserting the load window does that.

Backfills reuse the same logic over past periods, and reconciliation checks compare totals with the source to prove the result.

<!-- example -->

```sql
MERGE INTO fct_order_lines t
USING stg_order_lines s
ON t.order_number = s.order_number AND t.line_number = s.line_number
WHEN MATCHED THEN UPDATE SET quantity = s.quantity, net_amount = s.net_amount, loaded_at = s.loaded_at
WHEN NOT MATCHED THEN INSERT (order_number, line_number, date_key, customer_key, product_key, quantity, net_amount, loaded_at)
VALUES (s.order_number, s.line_number, s.date_key, s.customer_key, s.product_key, s.quantity, s.net_amount, s.loaded_at);
```

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

#### What is a backfill?

Reprocessing historical periods, for example after a bug fix or a new column. Pipelines should accept date ranges as parameters and write idempotently so backfills are safe.

#### What are reconciliation checks?

Comparisons between source and warehouse (row counts, sums of amounts, distinct keys per day) to prove that loads are complete and correct, often run automatically after each load.

#### A fact table's daily load sometimes creates duplicates. How do you fix it?

Make the load idempotent (`MERGE` on the grain key or delete-insert of the load window), deduplicate staging by natural key, add a uniqueness test at the grain that blocks publishing, and check source extraction for overlapping windows.

<!-- challenge -->

After a backfill of March, warehouse revenue for March is 0.4% lower than the source system. How do you find the gap?

<!-- solution -->

Reconcile by day, then by key: compare daily counts and sums with the source, and for the days that differ, find source keys missing in the warehouse (filters, failed key lookups, late records).

<!-- takeaways -->

- Idempotent loads replace their slice of data.
- Backfills reuse the same logic over the past.
- Reconcile counts and sums with sources.

<!-- unit: Sources and tools -->

<!-- goals -->

- Load SaaS data and use dbt for transformations.
- Handle source schema changes and micro-batch loading.

<!-- concept -->

Most warehouses now load from dozens of SaaS tools and databases. Managed connectors handle APIs and pagination; dbt handles transformations as versioned SQL with tests and dependencies. Together they cover most ELT.

Sources still change underneath: columns appear, types shift. Landing raw data flexibly, detecting schema changes and alerting turns those surprises into planned work. Micro-batches bring latency down to minutes when daily isn't enough.

<!-- example -->

```text
Fivetran/Airbyte ─► raw schema (auto-added columns, alerts on change)
dbt: staging models (rename, cast) ─► core ─► marts, tests on each
schedule: every 15 minutes for orders, daily for finance
```

#### How do you load data from SaaS applications?

With managed connectors (Fivetran, Airbyte, Lakeflow Connect, AppFlow) or custom API extraction handling pagination, rate limits, incremental cursors and schema changes, landing raw JSON before modeling.

#### What are ELT tools like dbt used for?

Writing transformations as version-controlled SQL models with dependencies, tests, documentation and environments, compiled and run inside the warehouse, bringing software engineering practices to the transformation layer.

#### How do you handle schema changes in sources?

Detect them (schema checks, contracts, alerts), land raw data flexibly (`VARIANT`, JSON, schema evolution), select columns explicitly in staging, decide per change whether to propagate it, and communicate breaking changes.

#### What is micro-batch loading?

Loading small batches every few minutes (instead of daily), balancing latency and efficiency; Snowpipe, Auto Loader, Structured Streaming triggers and scheduled `MERGE` jobs implement it.

<!-- challenge -->

A connector auto-adds a new column to the raw table, and a downstream `SELECT *` model breaks the BI tool. How do you make the pipeline resilient?

<!-- solution -->

Select explicit columns in staging models instead of `SELECT *`, enforce contracts on marts, and alert on raw schema changes so new columns are added deliberately.

<!-- takeaways -->

- Connectors load SaaS data; dbt transforms it.
- Land flexibly, select explicitly.
- Micro-batches lower latency to minutes.

### Data quality

<!-- unit: Defining and testing quality -->

<!-- goals -->

- Name the dimensions of data quality and the tests every table needs.
- Decide where checks run and what happens when they fail.

<!-- concept -->

Quality has several dimensions (completeness, accuracy, consistency, timeliness, validity, uniqueness), and each table needs tests for the ones that matter to it. Some apply everywhere: key uniqueness at the grain, not-null keys, referential integrity from facts to dimensions.

Where checks run decides what they catch: at ingestion for format, after transformation for rules, before publishing as a gate. Severity decides the response, from blocking and alerting to warning and logging.

<!-- example -->

```yaml
models:
  - name: fct_order_lines
    tests:
      - dbt_utils.unique_combination_of_columns: {combination_of_columns: [order_number, line_number]}
    columns:
      - name: customer_key
        tests: [not_null, {relationships: {to: ref('dim_customer'), field: customer_key}}]
      - name: net_amount
        tests: [{dbt_utils.accepted_range: {min_value: -100000, max_value: 100000}}]
```

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

<!-- challenge -->

A uniqueness test on a fact table fails at 06:00. Dashboards refresh at 07:00. What should the pipeline do?

<!-- solution -->

Block publishing the affected mart (keep yesterday's data visible), alert the owner with the failing keys, and mark dashboards as stale. Publishing duplicates would mislead users.

<!-- takeaways -->

- Test keys, nulls and relationships on every table.
- Check at ingestion, transformation and publishing.
- Severity decides block, quarantine or warn.

<!-- unit: Monitoring and ownership -->

<!-- goals -->

- Monitor quality with observability, anomaly detection and SLAs.
- Assign ownership with contracts and stewards.

<!-- concept -->

Tests catch what someone anticipated; monitoring catches the rest. Observability watches freshness, volume, schema and distributions, and anomaly detection compares today with history to flag sudden changes no rule described.

Quality is also an agreement between people. Contracts set what producers promise, SLAs set measurable targets, stewards own definitions and fixes, and quantifying the cost of bad data justifies the effort.

<!-- example -->

| Signal | Check |
|---|---|
| Freshness | `max(loaded_at)` within 2 h of schedule |
| Volume | Row count within ±20% of 7-day average |
| Distribution | Null rate of `customer_key` < 0.1% |
| Schema | Column added/removed in source → alert |

#### What is data observability?

Monitoring data systems for freshness, volume, schema changes, distribution changes and lineage, often with automatic anomaly detection, to find data incidents before users do.

#### What are anomaly detection checks?

Statistical checks comparing today's metrics (row counts, sums, null rates) with historical patterns, flagging unusual deviations even without explicit thresholds.

#### What is a data contract?

An agreement between a data producer and consumers about a dataset's schema, semantics, quality and SLAs, enforced in CI and pipelines so breaking changes are caught early.

#### What is a data quality SLA?

A commitment on measurable quality (for example "fewer than 0.1% of orders without customer", "data no older than 2 hours"), monitored automatically and reported to consumers.

#### How do you quantify the business impact of bad data?

By tracing incidents to decisions affected (wrong invoices, missed targets), time spent fixing, and trust lost; this helps prioritize quality investments on critical datasets.

#### What is the role of a data steward?

A business-side owner responsible for definitions, quality rules and issue resolution for a data domain, working with data engineers who implement the checks.

<!-- challenge -->

All tests pass, but yesterday's sales are half the usual amount because one store's feed failed silently. Which check would have caught it?

<!-- solution -->

An anomaly check on volume or revenue by store (or by source) against recent history, alerting when a segment drops sharply even if totals stay plausible.

<!-- takeaways -->

- Observability catches what tests didn't anticipate.
- Contracts and SLAs make quality an agreement.
- Stewards own definitions and fixes.

### SQL for analytics

<!-- unit: Window functions -->

<!-- goals -->

- Use window functions for running totals, rankings and deduplication.
- Compute period-over-period growth.

<!-- concept -->

Window functions compute across related rows without collapsing them, which is why they're everywhere in warehousing. Partitioning defines the group, ordering defines sequence, and the frame defines which rows count. With them, running totals, rankings, latest-row selection and comparisons with the previous period become single expressions.

The ranking functions differ only in ties, a detail that changes results when values repeat.

<!-- example -->

```sql
WITH monthly AS (
  SELECT d.year_month, SUM(f.net_amount) AS revenue
  FROM fct_order_lines f JOIN dim_date d USING (date_key)
  GROUP BY 1
)
SELECT year_month, revenue,
       revenue / NULLIF(LAG(revenue) OVER (ORDER BY year_month), 0) - 1 AS mom_growth
FROM monthly;
```

#### What are window functions, and why are they essential in warehousing?

Functions that compute values over a set of rows related to the current row without collapsing them (`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`, `SUM() OVER`). They power deduplication, running totals, period comparisons and sessionization.

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

<!-- challenge -->

You need the top 3 products by revenue in each category, including ties at third place. Which function do you use?

<!-- solution -->

`RANK()` or `DENSE_RANK()` over revenue partitioned by category, filtered to rank ≤ 3. `ROW_NUMBER()` would cut ties arbitrarily.

<!-- takeaways -->

- Windows compute over related rows without grouping them.
- `LAG` and frames give growth and running totals.
- Ranking functions differ in how they treat ties.

<!-- unit: Analytical patterns -->

<!-- goals -->

- Write cohort, retention and consecutive-activity queries.
- Compute percentiles, multi-level aggregates and pivots.

<!-- concept -->

Most analytical requests are variations of a few patterns. Cohorts group customers by when they started and follow them over time. Consecutive-activity questions compare each period with the previous one. Percentiles describe distributions better than averages. Multi-level aggregates and pivots shape results for reports.

Recognizing the pattern behind a question is most of the work; the SQL follows.

<!-- example -->

```sql
WITH firsts AS (
  SELECT customer_key, MIN(order_month) AS cohort FROM customer_months GROUP BY 1
)
SELECT f.cohort, m.order_month, COUNT(DISTINCT m.customer_key) AS active
FROM customer_months m JOIN firsts f USING (customer_key)
GROUP BY 1, 2 ORDER BY 1, 2;
```

#### How do you find customers active in consecutive months?

Compute each customer's months of activity, then use `LAG` to compare with the previous month or the "gaps and islands" technique (month index minus row number) to group consecutive streaks.

#### What is a cohort analysis query?

Assign each customer to a cohort (first purchase month), then count active customers or revenue per cohort and months since first purchase, often pivoted into a retention triangle.

#### How do you compute a median or percentile?

With `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x)` in many engines, `MEDIAN()` in Snowflake, or `APPROX_PERCENTILE`/`APPROX_QUANTILES` for large data.

#### What are `GROUPING SETS`, `ROLLUP` and `CUBE`?

Extensions of `GROUP BY` that compute several aggregation levels in one query: `ROLLUP(year, month)` gives month, year and grand totals; `CUBE` gives all combinations; `GROUPING SETS` lists the exact combinations.

#### How do you pivot rows into columns in SQL?

With conditional aggregation (`SUM(CASE WHEN channel = 'web' THEN amount END) AS web_amount`) portable across engines, or `PIVOT` where supported (Snowflake, SQL Server, BigQuery, Databricks).

<!-- challenge -->

A report needs revenue by year, by year and quarter, and a grand total in one result. How do you write it without three queries?

<!-- solution -->

`GROUP BY ROLLUP(year, quarter)`, which returns subtotals per year, rows per quarter and a grand total; use `GROUPING()` to label subtotal rows.

<!-- takeaways -->

- Cohorts follow customers from their first activity.
- Percentiles describe skewed data better than averages.
- `ROLLUP`, `CUBE` and pivots shape report outputs.

<!-- unit: Writing correct SQL -->

<!-- goals -->

- Structure queries with CTEs and filter in the right place.
- Avoid errors from division by zero and NULLs.

<!-- concept -->

Wrong numbers in reports usually come from small SQL mistakes, not complex logic. Filtering after aggregation instead of before, dividing by zero, or forgetting that `NULL` never equals anything silently change results.

Readable structure is the best defense: CTEs name each step so reviewers can follow the logic, and explicit handling of `NULL` and zero turns hidden assumptions into visible decisions.

<!-- example -->

```sql
WITH paid AS (
  SELECT customer_key, net_amount FROM fct_order_lines WHERE status = 'paid'   -- row filter: WHERE
)
SELECT customer_key, SUM(net_amount) AS revenue,
       SUM(net_amount) / NULLIF(COUNT(*), 0) AS avg_line
FROM paid
GROUP BY customer_key
HAVING SUM(net_amount) > 1000;                                               -- group filter: HAVING
```

#### What is a CTE, and when should you use it?

A common table expression (`WITH name AS (...)`) names a subquery for readability and reuse within a query; recursive CTEs traverse hierarchies. They make complex warehouse SQL easier to review.

#### How do you avoid division-by-zero errors?

Use `NULLIF(denominator, 0)` so the result is `NULL` instead of an error, or safe division functions (`SAFE_DIVIDE` in BigQuery, `DIV0` in Snowflake).

#### What is the difference between `WHERE` and `HAVING`?

`WHERE` filters rows before aggregation; `HAVING` filters groups after aggregation. Filtering early with `WHERE` is cheaper.

#### How do you handle NULLs in joins and aggregations?

`NULL` never equals anything, so rows with `NULL` keys don't join (use unknown members or `IS NOT DISTINCT FROM`); aggregates ignore `NULL`s except `COUNT(*)`; use `COALESCE` for display defaults.

<!-- challenge -->

A join on `promotion_id` drops all sales without a promotion, and revenue looks low. What happened, and how do you fix it in the model?

<!-- solution -->

Sales have `NULL` promotion IDs, and `NULL` never matches in a join, so an inner join drops them. Map missing promotions to an unknown/no-promotion member in the fact (or use a left join).

<!-- takeaways -->

- CTEs make each step readable.
- `NULLIF` avoids division by zero.
- `NULL` keys don't join; use unknown members.

<!-- stage: Platforms and performance -->

### Engines and storage

<!-- unit: MPP and columnar storage -->

<!-- goals -->

- Explain MPP and why analytical engines store data by column.
- Describe compression encodings and vectorized execution.

<!-- concept -->

Analytical engines are built for one kind of work: scanning many rows but few columns. Storing each column together means a query reads only what it uses, and similar values side by side compress extremely well. Processing values in batches with CPU-friendly loops makes each scan faster.

Massively parallel processing adds scale: data is split across nodes that work on their share at the same time, so adding nodes adds speed.

<!-- example -->

| Layout | Read `SUM(amount)` over 1 B rows × 50 columns |
|---|---|
| Row store | Reads all 50 columns |
| Column store | Reads 1 column, compressed ~10× |

#### What is MPP?

Massively parallel processing: a database splits data across many nodes, each with its own CPU, memory and storage (or cache), and executes queries in parallel, combining results. Redshift, Teradata, Synapse and Vertica are MPP; Snowflake and BigQuery are cloud variants.

#### Why are analytical databases columnar?

Analytical queries read a few columns of many rows; storing each column contiguously means reading only needed columns, compressing similar values very well, and processing them with vectorized execution.

#### What is the difference between row-oriented and column-oriented storage?

Row storage keeps all columns of a row together, efficient for reading and writing whole records (OLTP). Column storage keeps values of each column together, efficient for scans and aggregations on few columns (OLAP).

#### What is compression encoding in columnar stores?

Techniques such as dictionary, run-length, delta and bit-packing encodings that shrink columns with repeated or ordered values; sorted data compresses better.

#### What is vectorized execution?

Processing batches of column values at once with CPU-efficient loops and SIMD instructions instead of row by row, which greatly speeds up scans, filters and aggregations in columnar engines.

<!-- challenge -->

A team stores a status column as long strings like "ORDER_STATUS_SHIPPED". Does it matter in a columnar warehouse?

<!-- solution -->

Less than in a row store, because dictionary encoding compresses repeated values well. Still, shorter codes or small integers reduce memory and comparison cost; keep descriptions in a dimension.

<!-- takeaways -->

- Columnar storage reads only needed columns.
- Encodings compress repeated values strongly.
- MPP spreads work across nodes.

<!-- unit: Data layout -->

<!-- goals -->

- Use distribution keys, sort keys, clustering and partitioning.
- Explain how zone maps and statistics help the optimizer.

<!-- concept -->

How data is placed decides how much a query must read and move. Partitioning and sorting let the engine skip blocks whose min/max values can't match a filter. Distribution decides which node holds which rows, so joins on the distribution key happen without moving data.

Statistics tell the optimizer how big tables are and how values are spread, which drives join order and strategy. Stale statistics produce bad plans on good data.

<!-- example -->

```sql
-- Redshift
CREATE TABLE fct_order_lines (...)
DISTKEY (customer_key)
SORTKEY (date_key);
-- Snowflake / BigQuery equivalent idea: CLUSTER BY (date_key)
```

#### What is a distribution key (Redshift, Synapse)?

The column used to distribute rows across nodes. Distributing two large tables on their join key co-locates matching rows and avoids redistribution during joins; small dimensions can be replicated (`ALL`) to every node; `EVEN` or `AUTO` spread rows uniformly.

#### What is a sort key (Redshift) or clustering key?

An ordering of data within storage so that range filters can skip blocks using min/max metadata (zone maps). Equivalent concepts: Snowflake clustering keys, BigQuery clustering, Delta liquid clustering or Z-order.

#### What is partitioning in a warehouse?

Splitting a large table by a column (usually date) so queries filtering on it scan only relevant partitions and maintenance (deleting old data, reloading a day) is cheap. BigQuery uses explicit partitioning; Snowflake uses micro-partitions automatically.

#### What are zone maps or min/max statistics?

Metadata storing minimum and maximum values per block or file, used to skip blocks that can't match a filter. Data sorted or clustered by the filter column makes them effective.

#### What is the role of statistics in query optimization?

Row counts, distinct values, min/max and histograms let the optimizer estimate cardinalities and choose join orders and strategies; stale statistics cause bad plans.

<!-- challenge -->

A query filtering one day of a 3-year fact table reads 80% of its blocks. What do you check?

<!-- solution -->

Whether the table is sorted, clustered or partitioned by date, and whether the filter applies directly to that column (not through a function). Check clustering depth or vacuum/sort status if data was loaded out of order.

<!-- takeaways -->

- Sorting and partitioning let engines skip blocks.
- Distribution keys colocate joined data.
- Fresh statistics drive good plans.

<!-- unit: Compute and concurrency -->

<!-- goals -->

- Separate storage and compute and manage workloads.
- Use materialized views, result caches and scaling options.

<!-- concept -->

Cloud warehouses split storage from compute, so several independent clusters can read the same data. That changes how you handle load: separate compute per workload stops ETL from slowing dashboards, and scaling out handles more users while scaling up makes single queries faster.

Caching and precomputation cut work further: result caches answer repeated queries instantly, and materialized views keep expensive results ready.

<!-- example -->

| Problem | Lever |
|---|---|
| ETL slows dashboards at 08:00 | Separate compute per workload |
| One heavy query is slow | Scale up |
| 200 users queue at 09:00 | Scale out (multi-cluster) |
| Same dashboard query 500×/day | Result cache / materialized view |

#### What is a materialized view?

A stored, automatically or periodically refreshed result of a query. It speeds up repeated aggregations or joins; the engine may use it transparently. Maintenance costs compute.

#### What is workload management?

Controlling how queries share resources: queues, priorities, concurrency limits, separate compute clusters or warehouses for ETL and BI, and query timeouts, so heavy jobs don't starve interactive users.

#### What is the separation of storage and compute?

Storing data in shared storage (object storage) and running independent, elastic compute clusters on top, so you scale and pay for each separately and isolate workloads. Snowflake, BigQuery, Databricks and Redshift RA3/Serverless use this model.

#### What are result caches?

Stores of previous query results returned instantly when the same query runs again on unchanged data (Snowflake result cache, BigQuery cached results), saving compute for dashboards.

#### What is the difference between scale up and scale out in warehouses?

Scale up gives a query more resources (bigger warehouse, more slots) to finish faster; scale out adds clusters to serve more concurrent queries. Choose based on whether the problem is single-query latency or concurrency.

<!-- challenge -->

Morning dashboards queue behind nightly ETL that runs late. The warehouse is a single cluster. What do you propose?

<!-- solution -->

Give ETL and BI separate compute (warehouses or queues with workload management), so BI never waits on ETL. Then fix ETL lateness separately.

<!-- takeaways -->

- Storage-compute separation enables isolated workloads.
- Scale up for single-query speed; out for concurrency.
- Caches and materialized views avoid repeated work.

### Performance

<!-- unit: Fast star queries -->

<!-- goals -->

- Make star schema queries prune and join efficiently.
- Choose data types and wide tables for speed.

<!-- concept -->

Fast star queries share a profile: they filter on partitioned or clustered columns, join a large fact to small dimensions, and read few columns. Checking the query profile for pruning is the first step whenever something is slow.

In columnar engines, wide denormalized tables can be fast because unused columns cost nothing. Compact data types help everywhere: smaller keys and dates scan, join and compress better.

<!-- example -->

```text
Query profile: fct_order_lines
  partitions scanned: 31 of 1,826   ✔ pruning on date_key
  bytes scanned: 4.2 GB
  join: broadcast dim_product (12 MB) ✔
```

#### How do you make a star schema query fast?

Filter on partitioned or clustered columns (date), join facts to small dimensions (broadcast), select only needed columns, pre-aggregate common queries, keep statistics current, and avoid functions on filter columns.

#### What is query pruning, and how do you check it?

Skipping partitions, files or blocks that can't match a query's filters. Check it in query profiles or plans (partitions scanned versus total, bytes scanned) and fix filters or data layout when it doesn't happen.

#### What is the impact of data types on warehouse performance?

Smaller types (integers instead of strings for keys, `DATE` instead of `TIMESTAMP` when enough, `DECIMAL` with appropriate precision) compress better and compare faster; joining on mismatched types forces casts and prevents optimizations.

#### Why can wide denormalized tables be fast in columnar engines?

Because only the columns referenced by a query are read, a wide table doesn't cost more to query than a narrow one with the same rows, and it avoids joins. The costs are storage, maintenance and potential inconsistency.

#### Queries on a 5-year fact table got slow as data grew. What do you check?

Whether queries filter on the partition or clustering column, data layout degradation (clustering depth, small files), missing statistics, new joins that fan out, BI queries without date filters, and whether aggregate tables or materialized views would serve common patterns.

<!-- challenge -->

Join keys are 36-character UUID strings, and joins on a 2-billion-row fact are slow. What do you change?

<!-- solution -->

Use integer surrogate keys in facts and dimensions (keep the UUID as a natural key attribute). Integer joins and comparisons are much cheaper and compress better.

<!-- takeaways -->

- Check pruning first when queries are slow.
- Join big facts to small dimensions.
- Compact types make scans and joins cheaper.

<!-- unit: Joins and distinct counts -->

<!-- goals -->

- Recognize and fix fan-out and unnecessary DISTINCT.
- Speed up distinct counts and very large dimensions.

<!-- concept -->

Two habits make queries both slow and wrong. Joining at the wrong grain multiplies rows, and adding `DISTINCT` to hide the duplicates doubles the cost while leaving the root cause. Fixing the join is the real solution.

Distinct counts over huge data are inherently expensive; approximate functions or pre-aggregated sets make them affordable. Very large dimensions need the same care as facts: clustering, fewer versions, and joins on compact keys.

<!-- example -->

```sql
SELECT date_key, APPROX_COUNT_DISTINCT(customer_key) AS customers   -- HyperLogLog, ~1–2% error
FROM fct_page_views
WHERE date_key BETWEEN 20261001 AND 20261031
GROUP BY date_key;
```

#### What causes a "fan-out" or double counting in joins?

Joining a fact to a table that has several rows per key (many-to-many or a wrong grain), so each fact row is duplicated and sums inflate. Check join cardinalities and enforce uniqueness of dimension keys.

#### How do you speed up `COUNT(DISTINCT)` on large data?

Use approximate functions (HyperLogLog: `APPROX_COUNT_DISTINCT`), pre-aggregate distinct sets per period, or maintain distinct counts in aggregate tables when exact values are needed.

#### How do you avoid expensive `SELECT DISTINCT` in models?

Find why duplicates appear (wrong join grain) and fix the join instead of masking it with `DISTINCT`, which is costly and hides data problems.

#### How do you handle very large dimensions (hundreds of millions of rows)?

Partition or cluster by natural key ranges, minimize SCD2 churn with mini-dimensions, avoid unnecessary attributes, use integer surrogate keys, and consider whether the "dimension" is really a fact-like entity.

<!-- challenge -->

A model ends with `SELECT DISTINCT *` "to remove duplicates" and takes 40 minutes. What do you do?

<!-- solution -->

Find which join introduces duplicates (a table with several rows per key), fix the join grain (aggregate or filter that table first), add a uniqueness test on the output key, and remove the `DISTINCT`.

<!-- takeaways -->

- Fan-out comes from joining at the wrong grain.
- Fix joins instead of masking with `DISTINCT`.
- Approximate distincts scale to huge data.

<!-- unit: Dashboards and cost -->

<!-- goals -->

- Speed up slow dashboards with aggregates and covering tables.
- Test performance before go-live and cut costs with incremental models.

<!-- concept -->

Dashboards repeat the same questions, so their performance work is about not recomputing answers: aggregates or materialized views at the grain charts need, covering tables that hold exactly the columns a frequent query uses.

Cost and speed usually move together. Incremental models transform only new data, and testing with realistic volumes and concurrency before launch avoids discovering limits in front of users.

<!-- example -->

```text
dashboard "Sales overview": 9 charts
  before: each chart scans fct_order_lines (1.4 B rows) → 25 s
  after:  agg_sales_day_store_category (3 M rows), refreshed hourly → 1.5 s
```

#### How do you optimize a slow dashboard?

Find the slow queries, check pruning and joins, add aggregates or materialized views for the dashboard's grain, use the BI tool's extracts or caching, limit default date ranges, and remove unnecessary visuals that each fire queries.

#### What is a "covering" aggregate?

An aggregate table containing all the columns a frequent query needs at the right grain, so the query never touches the atomic fact table.

#### How do you test warehouse performance before going live?

Replay representative queries and concurrency on production-sized data, measure latency and cost per query, check plans for pruning and joins, and tune layout, aggregates and warehouse sizing.

#### How can incremental models reduce warehouse costs?

By transforming only new or changed data each run instead of rebuilding entire tables, which cuts compute dramatically for large facts; they need careful handling of late data and backfills.

<!-- challenge -->

A dbt project rebuilds all 300 models every hour, and warehouse costs tripled. What do you change first?

<!-- solution -->

Make large fact models incremental (process only new or changed rows), rebuild small models less often, and run hourly only the models dashboards need hourly.

<!-- takeaways -->

- Precompute what dashboards ask repeatedly.
- Test with realistic data and concurrency.
- Incremental models cut cost and time.

### Cloud data warehouses

<!-- unit: The cloud warehouse landscape -->

<!-- goals -->

- Describe the main cloud warehouses and how they work.
- Compare BigQuery, Redshift, Fabric and Databricks SQL.

<!-- concept -->

Cloud warehouses share the same core ideas, columnar storage, MPP and separated compute, but differ in how much you manage and how you pay. BigQuery is fully serverless. Redshift offers clusters and a serverless mode. Fabric and Databricks SQL build warehouses on open lake formats.

Knowing the architecture behind each explains its tuning levers and pricing.

<!-- example -->

| Warehouse | Compute model | Storage |
|---|---|---|
| Snowflake | Virtual warehouses (credits) | Managed, micro-partitions |
| BigQuery | Slots (on-demand or reserved) | Managed columnar |
| Redshift | RA3 clusters or Serverless RPUs | Managed storage + S3 |
| Fabric | Capacity units | Delta in OneLake |
| Databricks SQL | SQL warehouses (DBUs) | Delta / Iceberg via Unity Catalog |

#### What are the main cloud data warehouses?

Snowflake, Google BigQuery, Amazon Redshift (provisioned and Serverless), Azure Synapse and Microsoft Fabric warehouses, and Databricks SQL on the lakehouse. They differ in architecture, pricing models and ecosystem integration.

#### How does BigQuery work and how is it priced?

BigQuery is serverless: storage in a columnar format (Capacitor) on Colossus, compute allocated as slots by Dremel. Pricing is on-demand per TB scanned or capacity-based (editions with reserved or autoscaled slots), plus storage.

#### How does Amazon Redshift work?

An MPP warehouse with a leader node and compute nodes; RA3 nodes separate managed storage (S3-backed) from compute, Serverless bills per RPU-hour, and features include distribution and sort keys (with automatic tuning), materialized views, Spectrum for S3 data, data sharing and zero-ETL integrations.

#### What is Microsoft Fabric's warehouse?

A SaaS analytics platform where warehouses and lakehouses store data in Delta format in OneLake, queried with T-SQL and Spark and served to Power BI with Direct Lake mode.

#### What is Databricks SQL as a warehouse?

SQL warehouses on the Databricks lakehouse querying Delta tables governed by Unity Catalog, with Photon, serverless compute and BI connectors, offering warehouse functionality on open storage.

<!-- challenge -->

A team moving from Redshift to BigQuery asks where to set distribution and sort keys. What do you tell them?

<!-- solution -->

BigQuery has no distribution keys; it manages placement. The equivalents are partitioning (usually by date) and clustering on common filter columns, plus controlling bytes scanned since on-demand pricing bills by data read.

<!-- takeaways -->

- All share columnar storage and MPP.
- They differ in management and pricing model.
- Tuning levers follow each architecture.

<!-- unit: Choosing and paying for a warehouse -->

<!-- goals -->

- Understand cloud warehouse costs and choose a platform.
- Use BigQuery partitioning, Redshift Spectrum and plan migrations.

<!-- concept -->

Compute dominates warehouse bills, and each platform meters it differently: credits, slots, RPUs or DBUs. Costs follow habits, such as idle clusters, full rebuilds and unfiltered scans, more than prices.

Choosing a platform starts from context: the cloud you're on, workload shapes, skills, ecosystem and governance. Migrating to it is a project of inventory, translation and validation rather than a copy.

<!-- example -->

```sql
-- BigQuery: partition and cluster to cut bytes scanned
CREATE TABLE sales.fct_order_lines
PARTITION BY order_date
CLUSTER BY customer_key, product_key
AS SELECT * FROM staging.order_lines;
```

#### How do cloud warehouses charge, and what drives costs?

Compute (credits, slots, RPUs, DBUs) usually dominates, then storage, data transfer and serverless features. Costs grow with inefficient queries, always-on compute, full refreshes, and many users running unfiltered queries; governance and monitoring are essential.

#### How do you choose a cloud warehouse?

Consider the existing cloud and ecosystem, workload patterns (steady vs spiky, concurrency), skills, governance needs, open formats and lakehouse strategy, pricing model fit, data sharing needs and vendor lock-in tolerance. Prototype with real queries before committing.

#### What is BigQuery's approach to partitioning and clustering?

Tables can be partitioned by a date/timestamp column, ingestion time or integer range, and clustered on up to four columns; queries filtering on them read fewer bytes, which reduces on-demand cost directly.

#### What is Redshift Spectrum?

A feature that lets Redshift query data in S3 through external tables in the Glue Data Catalog, joining lake data with warehouse tables, billed per bytes scanned.

#### How would you migrate an on-premises warehouse to the cloud?

Inventory sources, ETL jobs, reports and users; choose target platform and architecture; migrate history in bulk; rebuild pipelines as ELT (often with dbt) rather than lift-and-shift where valuable; redefine security and governance; validate with reconciliation reports; run in parallel; switch reports in waves; decommission the old system.

<!-- challenge -->

After migrating to the cloud, the monthly bill is twice the estimate. Name three likely causes.

<!-- solution -->

Compute left running (no auto-suspend), jobs rebuilding full tables instead of incremental loads, and queries scanning unpartitioned or unclustered tables. Usage of BI live queries without caching is a fourth.

<!-- takeaways -->

- Compute dominates; habits drive cost.
- Choose by context, workloads and skills.
- Migrations need inventory, translation and validation.

<!-- unit: Open data and sharing -->

<!-- goals -->

- Share live data without copies.
- Explain what open table formats mean for warehouses.

<!-- concept -->

Copying data to share it creates stale duplicates and security gaps. Zero-copy sharing gives other accounts or companies live, read-only access to the same data, governed by the owner.

Open table formats push the same idea further: warehouses, Spark and other engines read and write the same Iceberg or Delta tables in your storage, so the warehouse becomes one engine among several instead of a closed store.

<!-- example -->

```text
producer account: share sales.daily_revenue → partner account (read-only, live)
open tables: Iceberg in S3 ◄── Snowflake, Spark, Trino all read the same files
```

#### What is zero-copy data sharing?

Sharing live data between accounts or organizations without copying it (Snowflake Secure Data Sharing, BigQuery Analytics Hub, Redshift data sharing, Delta Sharing), so consumers query the provider's data with their own compute.

#### What are open table formats' implications for warehouses?

Iceberg and Delta let several engines (warehouse, Spark, Trino) work on the same data in object storage, reducing lock-in and copies. Warehouses increasingly read and write them natively.

<!-- challenge -->

A partner receives a nightly CSV export of 20 tables, often a day late and occasionally incomplete. What do you propose?

<!-- solution -->

Share the curated tables through the warehouse's zero-copy sharing (or Delta Sharing / Iceberg via a catalog), so the partner queries live data with permissions you control and no file transfer.

<!-- takeaways -->

- Zero-copy sharing replaces exports.
- Open table formats let many engines share tables.
- The warehouse becomes one engine among several.

<!-- stage: Serving and governing -->

### BI and consumption

<!-- unit: BI-ready models -->

<!-- goals -->

- Make data models friendly for BI tools and users.
- Choose between reports, dashboards, live queries and extracts.

<!-- concept -->

A model is BI-ready when a business user can build a correct chart without asking anyone: clear names, documented measures, conformed dimensions and correct relationships. Star schemas fit BI tools naturally.

How data reaches the tool matters too. Live queries keep data fresh and security central; extracts give speed and offload the warehouse. Reports and dashboards serve different needs, and reverse ETL pushes results into operational tools where people already work.

<!-- example -->

| Need | Choice |
|---|---|
| Monthly regulatory listing | Paginated report |
| Daily KPI monitoring | Dashboard |
| Data changes every few minutes | Live query |
| 500 viewers, data changes daily | Extract / cache |
| Sales reps need scores in the CRM | Reverse ETL |

#### What makes a data model BI-friendly?

Star schemas with clear names, documented business definitions, conformed dimensions, correct grains, surrogate keys hidden from users, consistent date handling, and a semantic layer for metrics.

#### What is the difference between a report and a dashboard?

A report presents detailed data, often tabular and paginated, for analysis or regulatory purposes. A dashboard summarizes key metrics visually for monitoring at a glance, with drill-down.

#### How do you decide between live queries and extracts in BI tools?

Live queries give fresh data and central security but depend on warehouse performance and cost; extracts (Tableau extracts, Power BI import, SPICE) are fast and cheap per query but stale and duplicated. Choose per dashboard based on freshness needs and usage.

#### What is reverse ETL?

Sending warehouse data (segments, scores, metrics) back into operational tools like CRMs, marketing platforms or support systems, so business teams act on modeled data (Hightouch, Census, custom jobs).

<!-- challenge -->

A dashboard with 400 daily viewers runs live queries against the warehouse every time someone opens it, though data updates once a day. What do you change?

<!-- solution -->

Use an extract or cached dataset refreshed after the daily load, so viewers hit the cache and the warehouse runs the queries once.

<!-- takeaways -->

- Clear names and stars make models BI-friendly.
- Live queries for freshness; extracts for speed.
- Reverse ETL delivers data into operational tools.

<!-- unit: Self-service with guardrails -->

<!-- goals -->

- Enable self-service BI while keeping numbers consistent.
- Secure rows, document models and certify datasets.

<!-- concept -->

Self-service lets business users answer their own questions, which scales far better than a queue of requests. Without guardrails it produces conflicting metrics and exposed data. The guardrails are governed, certified datasets with documented definitions, row-level security that follows the user, and documentation where people look.

Certification is the signal users need: this dataset is reviewed, tested and owned.

<!-- example -->

```sql
-- row-level security (Snowflake row access policy)
CREATE ROW ACCESS POLICY region_rls AS (region STRING) RETURNS BOOLEAN ->
  EXISTS (SELECT 1 FROM security.user_regions u
          WHERE u.user_name = CURRENT_USER() AND u.region = region);
ALTER TABLE marts.fct_sales ADD ROW ACCESS POLICY region_rls ON (region);
```

#### What is self-service BI, and what are its risks?

Business users building their own analyses from governed datasets. Risks: inconsistent metric definitions, duplicated logic, uncontrolled extracts and costs. A semantic layer, certified datasets and training reduce them.

#### What is row-level security in BI and warehouses?

Restricting which rows users see based on their identity (region, department), implemented in the warehouse (row access policies, secure views) or the BI layer, so one dataset serves many audiences safely.

#### How do you document a warehouse?

Table and column descriptions in the catalog (dbt docs, Unity Catalog, Glue, DataHub), a business glossary for metrics, lineage graphs, ownership and SLAs, and examples of correct queries.

#### What is a certified dataset?

A dataset marked as trusted after review (definitions, tests, ownership), promoted in BI tools and catalogs so users prefer it over personal or experimental copies.

<!-- challenge -->

Regional managers must see only their region's sales in every tool, not just in one dashboard. Where do you implement it?

<!-- solution -->

In the warehouse with a row access policy (or secure views) driven by a user-to-region mapping, so every tool querying the data gets the same restriction. Tool-level filters alone are easy to bypass.

<!-- takeaways -->

- Self-service needs governed, certified datasets.
- Row-level security belongs in the warehouse.
- Document definitions where users look.

### Governance and security

<!-- unit: Securing warehouse data -->

<!-- goals -->

- Secure a warehouse with roles, network controls and encryption.
- Handle personal data and set retention policies.

<!-- concept -->

Warehouse security follows least privilege: access roles hold privileges on objects, functional roles group them by job, and users get functional roles through SSO. Network restrictions and encryption add layers around that.

Personal data needs its own treatment: classify and tag it, load only what's needed, pseudonymize early, and mask it for most users. Retention policies decide how long each dataset stays, for legal and cost reasons.

<!-- example -->

```text
access roles:     sales_read, sales_write, pii_read
functional roles: analyst_sales = sales_read
                  data_engineer = sales_read + sales_write
users ← functional roles via SSO groups; pii_read only for a few
```

#### How do you secure a data warehouse?

Least-privilege roles (access roles granted to functional roles), SSO and MFA, network restrictions, encryption at rest and in transit, masking of sensitive columns, row-level security, auditing of access, and separate environments for development and production.

#### How do you handle personal data (PII) in a warehouse?

Classify and tag it, minimize what's loaded, pseudonymize or tokenize identifiers early, mask for most users, restrict raw access, apply retention policies, and support deletion requests (GDPR, Colombia's Law 1581) with documented processes.

#### What are data retention policies?

Rules for how long each dataset is kept (legal, business and cost reasons), implemented with partition drops, lifecycle rules, Time Travel settings and archiving, and documented for compliance.

<!-- challenge -->

Every analyst can query raw customer emails and phone numbers. What do you change without breaking their work?

<!-- solution -->

Apply masking policies to PII columns (shown only to a privileged role), offer pseudonymized keys for joins and counts, and review who truly needs raw values.

<!-- takeaways -->

- Least privilege through access and functional roles.
- Classify, minimize and mask personal data.
- Retention policies limit legal risk and cost.

<!-- unit: Lineage and discovery -->

<!-- goals -->

- Use lineage and catalogs to make data understandable.
- Help analysts find the right tables.

<!-- concept -->

As a warehouse grows, finding the right table becomes the bottleneck. A catalog makes datasets searchable, with descriptions, owners and quality signals; lineage shows where each table comes from and what depends on it, which builds trust and supports impact analysis.

Organization helps as much as tooling: schemas by layer and domain, certified datasets, and fewer near-duplicate tables.

<!-- example -->

```text
search "revenue" →
  marts.fct_revenue        ✔ certified · owner: finance-data · refreshed 06:40 · used by 34 dashboards
  sandbox.revenue_test_v2  ✘ uncertified · owner: a.lopez · last used 4 months ago
```

#### What is data lineage, and why does it matter?

The record of where data comes from and how it's transformed, at table and column level. It supports impact analysis before changes, debugging wrong numbers, audits and trust.

#### What is a data catalog?

A searchable inventory of datasets with descriptions, owners, schemas, tags, lineage, quality status and usage, helping people find and understand data (DataHub, Collibra, Alation, Unity Catalog, Glue Data Catalog).

#### Analysts complain they can't find the right tables. What do you do?

Organize schemas by layer and domain, document models and columns, certify key datasets, publish a catalog with search and lineage, deprecate and remove legacy tables, and offer a semantic layer with business-named metrics.

<!-- challenge -->

Analysts keep using an old, unmaintained revenue table because it appears first in search. What do you do?

<!-- solution -->

Certify the maintained table and mark the old one deprecated in the catalog, redirect or replace it with a view on the new table, notify its users found through query logs, then remove it.

<!-- takeaways -->

- Catalogs make data findable and trusted.
- Lineage supports trust and impact analysis.
- Certify the right tables; deprecate the rest.

<!-- stage: Putting it together -->

### Scenarios

<!-- unit: Designing a sales mart -->

<!-- goals -->

- Design a dimensional sales mart end to end.
- Justify grain, facts, dimensions and SCD choices.

<!-- concept -->

A data mart design question tests whether you can apply the method under pressure. Start with the business process and grain, list the dimensions with their change policies, define facts and their additivity, then cover loading, quality and how users will query it. Naming what you'd do with returns, currencies and late data shows experience beyond the textbook.

<!-- example -->

```text
process: order taking   grain: order line
dims: date (order, ship roles), customer (SCD2 segment), product (SCD2 category),
      store, promotion, junk flags
facts: quantity, gross, discount, net (additive), returns as negative lines
load: incremental MERGE on (order_number, line_number); tests on keys and relationships
```

#### Design a sales data mart for an e-commerce company.

Business process: order lines. Grain: one row per order line. Dimensions: date (order, ship), customer (SCD2 on segment and region), product (SCD2 on category), store or channel, promotion, and a junk dimension for flags; degenerate dimension order number. Facts: quantity, gross amount, discount, net amount, cost, tax. Add a returns fact and daily inventory snapshot later, sharing conformed dimensions.

<!-- challenge -->

The business adds: "we also want to know which products customers viewed but didn't buy." How does your design change?

<!-- solution -->

Add a separate fact for product views (one row per view event, factless or with dwell time), sharing the conformed customer, product and date dimensions, and compare with sales by drill-across.

<!-- takeaways -->

- Start from process and grain, then dimensions and facts.
- Address returns, currencies and late data explicitly.
- New processes get new facts on conformed dimensions.

<!-- unit: Modeling subscriptions -->

<!-- goals -->

- Model a subscription business with the right fact types.
- Compute recurring revenue and churn from the model.

<!-- concept -->

Subscriptions mix events and states. Sign-ups, upgrades and cancellations are events; monthly recurring revenue and active status are states at a point in time. A good model captures both: transaction facts for changes and a periodic snapshot for the monthly state, with the subscription as a slowly changing dimension. Metrics like MRR, churn and expansion then become simple queries instead of complex reconstructions.

<!-- example -->

```text
dim_subscription (plan, billing_period, status; SCD2)
fct_subscription_events (date, subscription, event_type, mrr_delta)
fct_subscription_monthly (month, subscription, customer, mrr, is_active)   ← periodic snapshot
churned MRR(month) = SUM(mrr) last month for subscriptions inactive this month
```

#### How would you model subscriptions for a SaaS company?

A subscription dimension (plan, billing period, status SCD2), a transaction fact for subscription events (start, upgrade, downgrade, cancel), and a monthly periodic snapshot fact with MRR per customer and plan, enabling churn, expansion and cohort analysis.

<!-- challenge -->

Finance wants MRR as it was reported at each month end, even if later corrections change history. How do you support it?

<!-- solution -->

Keep the monthly snapshot immutable once a month closes (append a corrected snapshot version instead of overwriting), so "as reported" and "as corrected" MRR are both available.

<!-- takeaways -->

- Events in transaction facts; states in snapshots.
- MRR and churn come straight from the snapshot.
- Freeze closed periods when reported numbers matter.
