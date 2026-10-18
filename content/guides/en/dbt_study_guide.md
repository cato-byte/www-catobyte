## dbt Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![dbt study guide: about 200 questions](../../images/dbt_study_guide_title_img.png)

About 200 interview-style questions on dbt (data build tool), from the basics to incremental models, snapshots, testing, deployment and performance. The answers refer to dbt Core 1.x conventions. Open a question to see its answer, or use the filter to search the whole guide.

<!-- QA -->

### Fundamentals

#### What is dbt?

dbt (data build tool) is a transformation framework: you write `SELECT` statements as models, and dbt compiles them with Jinja, works out their dependencies and runs them in your data warehouse as tables or views. It brings software engineering practices (version control, testing, documentation, modularity, CI/CD) to SQL transformations. dbt is the "T" in ELT.

#### What are common use cases for dbt?

Building a data warehouse or lakehouse layer by layer (staging, intermediate, marts), cleaning and standardizing raw data, building dimensional models for BI, historizing slowly changing data with snapshots, testing data quality, documenting datasets with lineage, and defining shared business metrics in the semantic layer.

#### How does dbt differ from traditional ETL tools?

Traditional ETL tools extract, transform in their own engine, then load, often through a GUI. dbt only transforms, inside the warehouse that already holds the loaded data (ELT), using SQL in plain text files. Everything is code: versioned in Git, reviewed, tested and deployed like software. Extraction and loading are left to other tools (Fivetran, Airbyte, custom pipelines).

#### How does dbt compare to Apache Spark?

Spark is a distributed processing engine that you program in Python, Scala or SQL, and you manage its jobs and clusters. dbt is not an engine: it generates SQL and sends it to an engine (Snowflake, BigQuery, Redshift, Databricks, Postgres, and Spark itself through the dbt-spark or dbt-databricks adapters). They are complementary: dbt can orchestrate SQL transformations that Spark executes, while complex non-SQL processing stays in Spark code.

#### What does ELT mean, and why does dbt fit it?

Extract, Load, Transform: raw data is loaded into the warehouse first and transformed there. Modern warehouses are cheap to store in and powerful to compute in, so transforming in SQL where the data already sits is simpler and scalable. dbt provides the structure for that transform step.

#### What is the difference between dbt Core and dbt Cloud?

dbt Core is the open-source command-line tool (Apache 2.0): you install it, run it and orchestrate it yourself. dbt Cloud (now part of the dbt platform) is the managed commercial service: a web IDE, job scheduler, CI, hosted documentation, the semantic layer, alerts, and access control. Both run the same project code.

#### What is a dbt adapter?

A plugin that lets dbt talk to a specific data platform, translating dbt's generic operations into that platform's SQL dialect: dbt-postgres, dbt-snowflake, dbt-bigquery, dbt-redshift, dbt-databricks, dbt-spark and many community adapters.

#### What is a dbt model?

A `.sql` file in the `models/` folder containing one `SELECT` statement. dbt wraps it in the DDL needed to create a view, table or other object named after the file. Python models (`.py`) are also supported on some platforms.

#### What is the DAG in the context of dbt?

The Directed Acyclic Graph of dependencies between models, sources, seeds and snapshots, built from `ref()` and `source()` calls. dbt uses it to run nodes in the right order (and in parallel when possible), to select parts of the project, and to draw lineage in the docs.

#### What are the challenges with dbt?

It only covers transformation, so you need other tools for ingestion and orchestration. Large projects can become slow to compile and hard to navigate without conventions. Incremental models and snapshots need careful design. Jinja can make SQL hard to read when overused. Performance still depends on the warehouse and the SQL you write, and costs can grow if full refreshes run too often.

#### What problems does dbt solve compared with stored procedures and scripts?

Dependencies are explicit and resolved automatically, code is modular and reusable through `ref` and macros, tests and documentation live next to the code, environments are switched through configuration rather than edits, and everything is version-controlled and reviewable.

#### Which commands are the most common in dbt?

`dbt run` (build models), `dbt test` (run tests), `dbt build` (run, test, snapshot and seed in DAG order), `dbt seed`, `dbt snapshot`, `dbt compile`, `dbt docs generate` / `dbt docs serve`, `dbt debug`, `dbt deps`, `dbt clean`, `dbt ls`, `dbt source freshness` and `dbt run-operation`.

#### What does `dbt build` do?

It runs seeds, models, snapshots and tests in DAG order. If a test fails on a node, the nodes downstream of it are skipped, so bad data doesn't propagate.

#### What is `dbt debug` used for?

It checks the installation, `dbt_project.yml`, `profiles.yml` and the connection to the warehouse. It is the first thing to run when nothing works.

#### What is the difference between `dbt run` and `dbt compile`?

`dbt compile` renders the Jinja and writes the resulting SQL to `target/compiled/` without executing anything. `dbt run` compiles and executes, writing the executed statements (with DDL) to `target/run/`.

#### Which languages can you write dbt models in?

SQL (with Jinja) everywhere, and Python on Snowflake (Snowpark), Databricks and BigQuery (Dataproc). Python models return a DataFrame and are useful for logic that is awkward in SQL.

#### What is a Python model in dbt?

A `.py` file defining `model(dbt, session)` that returns a DataFrame. It can reference other models with `dbt.ref()` and is materialized as a table or incremental model.

```python
def model(dbt, session):
    dbt.config(materialized="table")
    orders = dbt.ref("stg_orders")
    return orders.groupBy("customer_id").count()
```

#### What is dbt Fusion?

A new dbt engine written in Rust, introduced in 2025, that parses and compiles projects much faster and understands SQL semantically (column-level lineage, catching errors before they reach the warehouse). It powers the dbt VS Code extension and the dbt platform.

#### What is the dbt Semantic Layer?

A layer, built on MetricFlow, where metrics (revenue, active users) are defined once in YAML on top of semantic models, then queried consistently by BI and other tools through APIs, so every tool computes the metric the same way.

#### What does "modular data modeling" mean in dbt?

Splitting transformations into small, reusable models with one responsibility each (staging per source, intermediate logic, final marts), connected with `ref`, instead of large monolithic queries.

### Projects and configuration

#### What is a dbt project?

A directory containing a `dbt_project.yml` file plus models, tests, macros, seeds, snapshots, analyses and documentation. It's the unit that dbt compiles and runs, usually one Git repository.

#### What is project structure?

The recommended layout:

```
dbt_project.yml
models/
  staging/<source>/      stg_ models: one per source table, light cleaning
  intermediate/          int_ models: joins and business logic
  marts/                 fct_ and dim_ models consumed by users
seeds/        small CSV reference data
snapshots/    SCD Type 2 history
macros/       reusable Jinja
tests/        singular data tests
analyses/     SQL that is compiled but not run
```

#### What goes in `dbt_project.yml`?

The project name, version, `profile` to use, paths (models, seeds, macros…), `vars`, and default configurations per folder, such as `+materialized: table` for all marts or `+schema: staging`.

#### What is `profiles.yml`?

The file (by default in `~/.dbt/`) holding connection details per profile and target: adapter type, host, database, schema, credentials and threads. It is kept out of the project repository because it contains secrets. Values can come from environment variables with `env_var()`.

#### What is a target in dbt?

A named connection configuration within a profile, such as `dev` and `prod`. You choose it with `--target`, and models can branch on `target.name`.

#### What are threads in dbt?

The maximum number of models dbt runs at the same time. Independent branches of the DAG run in parallel up to that limit.

#### How do you configure a model?

In three places, from most to least specific: a `{{ config(...) }}` block in the model file, a `config:` block in the model's YAML properties, and folder-level settings in `dbt_project.yml`. The most specific wins.

```sql
{{ config(materialized='table', schema='marts', tags=['daily']) }}
select * from {{ ref('int_orders') }}
```

#### What is the difference between configs and properties?

Configs control how dbt builds a node (materialization, schema, tags, hooks). Properties describe it (description, columns, tests, docs). Properties live in YAML files; configs can live in YAML, the model file or `dbt_project.yml`.

#### What are tags used for?

Labels on nodes to select them in commands, for example `dbt run --select tag:daily`, or to group them in jobs.

#### How does node selection work?

With `--select` and `--exclude`, using names, paths, tags, `source:`, `state:`, `resource_type:` and graph operators: `+model` selects the model and its parents, `model+` the model and its children, `@model` the model, its children and their parents.

```bash
dbt build --select +fct_orders          # fct_orders and everything upstream
dbt run --select staging.stripe         # a folder
dbt test --select source:stripe+        # tests on a source and everything downstream
```

#### What are packages, and how do you install them?

Reusable dbt projects (macros, models, tests) such as `dbt_utils`, `dbt_expectations` or `codegen`. You list them in `packages.yml` (or `dependencies.yml`) and run `dbt deps`.

#### What is `dbt_utils`?

The most used package, with generic tests (`unique_combination_of_columns`, `expression_is_true`, `accepted_range`) and macros (`generate_surrogate_key`, `star`, `date_spine`, `pivot`, `union_relations`).

#### What are variables (`vars`) in dbt?

Values defined in `dbt_project.yml` or passed on the command line (`--vars '{start_date: 2026-01-01}'`) and read with `{{ var('start_date') }}`.

#### How do you use environment variables in dbt?

With `{{ env_var('DBT_PASSWORD') }}`, optionally with a default value. They're commonly used in `profiles.yml` for credentials, and variables prefixed `DBT_ENV_SECRET_` are masked in logs.

#### How does dbt decide which schema a model is built in?

By the `generate_schema_name` macro. By default, a custom schema is appended to the target schema (`dbt_alice_marts` in dev, `analytics_marts` in prod). Many projects override the macro to use the custom schema as-is in production.

#### What is the `generate_schema_name` macro, and why override it?

It computes the schema for each node. Overriding it lets you, for example, use exact schema names in production while keeping a personal prefix in development, so developers don't overwrite each other.

#### What are analyses in dbt?

SQL files in `analyses/` that are compiled (Jinja and `ref` resolved) but never executed by `dbt run`. They are useful for ad hoc queries that benefit from dbt's references.

#### What does `dbt clean` do?

It deletes the folders listed in `clean-targets` (usually `target/` and `dbt_packages/`).

#### What are model access and groups?

Governance features. A model's `access` can be `private` (only referenced within its group), `protected` (within the project, the default) or `public` (by other projects). Groups assign ownership to a set of models.

#### What are model versions?

A way to publish a new version of a public model (`fct_orders_v2`) while consumers keep using the old one until they migrate, with `ref('fct_orders', v=1)`.

### Sources and seeds

#### What are sources in dbt?

Declarations, in YAML, of the raw tables that were loaded into the warehouse by other tools. Models select from them with `{{ source('stripe', 'payments') }}` instead of hard-coded table names, which records lineage, allows tests and documentation on raw data, and enables freshness checks.

```yaml
sources:
  - name: stripe
    database: raw
    schema: stripe
    tables:
      - name: payments
        loaded_at_field: _loaded_at
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
```

#### Why use `source()` rather than writing the table name?

The table location is defined in one place, lineage starts from the source in the DAG, sources can be selected (`source:stripe+`), and `dbt source freshness` can check them.

#### What is source freshness?

A check, run with `dbt source freshness`, that compares the maximum of the `loaded_at_field` with the current time and warns or errors when data is older than the configured thresholds.

#### Can you test sources?

Yes, generic tests can be declared on source columns exactly as on models, catching problems in raw data before they reach your models.

#### What is a staging model?

The first layer on top of a source: one model per source table, doing only light transformations (renaming, casting, basic cleaning, deduplication). Everything downstream references staging models, not sources directly.

#### Why should only staging models reference sources?

So each raw table is cleaned once, in one place. If the source changes, only its staging model needs updating.

#### What is seed?

A CSV file in the `seeds/` folder that `dbt seed` loads into the warehouse as a table. Models reference it with `ref()` like any model.

#### When should you use seeds, and when not?

For small, static reference data that changes rarely and belongs in version control: country codes, mapping tables, test fixtures. Not for large or frequently changing data, or data that should come from a source system.

#### How do you set column types for a seed?

With `column_types` in the seed's configuration, otherwise dbt infers them:

```yaml
seeds:
  my_project:
    country_codes:
      +column_types:
        code: varchar(2)
```

#### How do you reload a seed whose columns changed?

With `dbt seed --full-refresh`, which drops and recreates the table instead of truncating and inserting.

#### Can dbt work with different data sources and data warehouses?

dbt runs against one data platform per target, through its adapter, and transforms data that is already in that platform. It doesn't extract from source systems. Platforms that can query external data (Snowflake external tables, BigQuery federated queries, Databricks and Trino catalogs) let dbt transform data from several origins through the warehouse.

#### What is the difference between `ref()` and `source()`?

`ref()` points to another dbt node (model, seed, snapshot) and creates a dependency the DAG uses to order runs. `source()` points to raw data loaded outside dbt. Both resolve to the fully qualified table name for the current target.

#### What does `ref()` resolve to in different environments?

To the relation in the current target's database and schema, so the same code builds into a developer's schema in dev and into production schemas in prod.

#### What is a "staging, intermediate, marts" layering?

A common structure: staging cleans each source, intermediate holds reusable joins and business logic, marts are the final fact and dimension tables (or wide tables) consumed by BI and analysts.

#### What is `dbt source freshness` used for in production?

To detect broken or late ingestion before models run on stale data, often as the first step of a scheduled job.

### Models and materializations

#### How do you create a dbt model?

Create a `.sql` file under `models/` containing a `SELECT` that references upstream nodes with `ref` or `source`, optionally add a `config` block and a YAML entry with description and tests, then run `dbt run --select my_model`.

```sql
-- models/staging/stripe/stg_stripe__payments.sql
select
    id as payment_id,
    order_id,
    amount / 100.0 as amount_eur,
    created::date as payment_date
from {{ source('stripe', 'payments') }}
where status = 'succeeded'
```

#### How does dbt handle dependencies between models?

Through `ref()`. When a model calls `{{ ref('stg_orders') }}`, dbt records the edge in the DAG, builds `stg_orders` first, and replaces the call with the right table name. You never declare the order of execution yourself.

#### What are the types of materialization in dbt?

- **view** (default): a view is created, so nothing is stored and the query runs on read.
- **table**: the result is stored and rebuilt on each run.
- **incremental**: on later runs, only new or changed rows are inserted or merged.
- **ephemeral**: not built at all, inlined as a CTE into downstream models.
- **materialized_view**: a database materialized view, where supported.
Snapshots and seeds are separate resource types with their own behavior.

#### When should you use a view versus a table?

Views are cheap to build and always current, so they fit staging models and light transformations. Tables are faster to query, so they fit marts used by BI and models that are expensive to compute or queried often.

#### When should you use an ephemeral model?

For light, reusable logic that you don't want as a separate object in the warehouse. Overusing them makes debugging harder because they can't be queried directly.

#### How would you create custom materialization in dbt?

With a `{% materialization name, adapter='default' %}` block in a macro file. It typically gets the target relation, runs pre-hooks, builds the SQL with `{% call statement('main') %}`, handles existing relations, runs post-hooks and returns `{'relations': [target_relation]}`. Custom materializations are rare: most needs are covered by built-ins and incremental strategies.

#### What is a mart model?

A final model built for consumers, usually a fact (`fct_orders`) or dimension (`dim_customers`) table, or a wide denormalized table for a specific team.

#### What naming conventions are common in dbt?

`stg_<source>__<table>` for staging, `int_<entity>_<verb>` for intermediate, `fct_` and `dim_` for marts, plural entity names, snake_case, and one model per file with the same name as the relation.

#### What is the difference between a fact and a dimension model?

A fact model holds events or measurements at a declared grain (orders, payments) with foreign keys and numeric measures. A dimension holds descriptive attributes of entities (customers, products) used to filter and group facts.

#### How do you generate a surrogate key in dbt?

With `dbt_utils.generate_surrogate_key`, which hashes the concatenation of columns (handling NULLs consistently):

```sql
select
    {{ dbt_utils.generate_surrogate_key(['order_id', 'line_number']) }} as order_line_key,
    *
from {{ ref('stg_order_lines') }}
```

#### What is the grain of a model, and why does it matter?

What one row represents (one order, one order line, one customer per day). Stating it, and testing it with a uniqueness test, prevents duplicate rows and wrong aggregations downstream.

#### What are hooks?

SQL executed at given moments: `pre-hook` and `post-hook` around a model, and `on-run-start` / `on-run-end` around the whole invocation. Uses include granting privileges, creating indexes or logging runs.

#### What is Pre Hook and Post Hook?

A `pre-hook` runs SQL just before a model is built, and a `post-hook` just after, inside the same run. For example:

```sql
{{ config(post_hook="grant select on {{ this }} to role reporter") }}
```

#### What does `{{ this }}` refer to?

The relation (database.schema.table) of the model being built. It is used in hooks and in incremental models to query the existing table.

#### What are model contracts?

A `contract: {enforced: true}` config with declared column names and data types (and constraints where supported). dbt checks that the model's output matches before building it, protecting downstream consumers from schema changes.

#### What are constraints in dbt?

Declarations such as `not_null`, `unique`, `primary_key`, `foreign_key` and `check` on contracted models. dbt adds them to the DDL when the platform enforces them. Many warehouses only record some as metadata, so tests are still needed.

#### What is the difference between `dbt run --full-refresh` and a normal run?

`--full-refresh` drops and rebuilds incremental models and reloads seeds from scratch, instead of processing only new data.

#### What does the `--defer` flag do?

With `--state` pointing to production artifacts, it makes `ref()` resolve to production relations for models you haven't built in your environment, so you can run one model in dev without rebuilding all its parents.

#### What is `dbt clone`?

A command that creates copies (zero-copy clones where supported, otherwise views) of production models in another environment, from production state. It speeds up CI and development setups.

#### What is `dbt show`?

A command to preview the results of a model or inline query without materializing it: `dbt show --select stg_orders --limit 10`.

#### What is `dbt retry`?

It reruns only the nodes that failed or were skipped in the previous invocation.

#### How do you deal with the error "relation does not exist" on dbt?

Common causes: a referenced table was never built in the current target (run the parent, or use `--defer`), the table name is hard-coded instead of using `ref`/`source` (so the dependency isn't known and order is wrong), the source definition points to the wrong database or schema, the user lacks permission to see the object, or the identifier has quoting or case problems. Running `dbt compile` and checking the SQL in `target/compiled/` usually shows which name is wrong.

#### What is data refresh?

Updating the warehouse tables so they reflect the latest source data: a scheduled `dbt build` that rebuilds tables, processes new rows in incremental models and captures changes in snapshots. Its frequency depends on how fresh consumers need the data and how often sources load.

#### What is a disabled model?

A model with `enabled: false`. dbt ignores it, which is useful for platform-specific or work-in-progress models.

#### What is the `alias` config?

It sets the name of the relation in the warehouse independently of the model file name.

### Jinja and macros

#### How do you use Jinja to improve your SQL code?

Jinja adds control flow and reuse: loops to generate repetitive columns, `if` blocks for environment-specific logic, variables for configurable values, and macros to share logic across models. Keep it readable: when Jinja dominates a model, a macro or a different design is usually better.

```sql
select
    order_id,
    {% for method in ['card', 'paypal', 'transfer'] %}
    sum(case when payment_method = '{{ method }}' then amount else 0 end) as {{ method }}_amount
    {%- if not loop.last %},{% endif %}
    {% endfor %}
from {{ ref('stg_payments') }}
group by 1
```

#### What are macros in dbt and how can you run them?

Reusable pieces of Jinja (often generating SQL) defined with `{% macro name(args) %}...{% endmacro %}` in the `macros/` folder. They are called inside models, tests or hooks with `{{ name(args) }}`, or executed directly with `dbt run-operation name --args '{...}'`.

#### What is the difference between `{{ }}`, `{% %}` and `{# #}`?

`{{ }}` outputs an expression, `{% %}` runs a statement (if, for, set, macro, call), and `{# #}` is a comment that doesn't appear in the compiled SQL.

#### What does the `-` in `{%-` or `-%}` do?

It trims whitespace before or after the tag, keeping the compiled SQL tidy.

#### How do you write a macro with a default argument?

```sql
{% macro cents_to_euros(column, scale=2) %}
    round({{ column }} / 100.0, {{ scale }})
{% endmacro %}
```

Called as `{{ cents_to_euros('amount') }}`.

#### What does `run_query` do?

It executes a query during compilation and returns the result as an agate table, for example to build a list of distinct values used in a loop. It only returns data at execution time, so it is usually guarded with `{% if execute %}`.

#### What is the `execute` variable?

A boolean that is false during parsing and true when dbt actually runs nodes. Code that queries the database must be wrapped in `{% if execute %}` because the database isn't queried while parsing.

#### What is `adapter.dispatch`?

A mechanism to implement a macro differently per database, so packages work across adapters: dbt picks `snowflake__my_macro`, `bigquery__my_macro` or `default__my_macro` depending on the adapter.

#### What is the `target` variable in Jinja?

Information about the current connection: `target.name`, `target.schema`, `target.type`, `target.threads`. It is often used to limit data in development:

```sql
{% if target.name == 'dev' %} where created_at >= dateadd(day, -3, current_date) {% endif %}
```

#### How do you set a variable inside a model?

With `{% set %}`, for example `{% set payment_methods = ['card', 'paypal'] %}`, then use it in loops or expressions.

#### What is `log()` used for in macros?

To print messages to the console or log file during compilation, for debugging: `{{ log("value: " ~ my_var, info=true) }}`.

#### What is the `config` object in Jinja?

It reads a model's configuration inside macros, for example `config.get('unique_key')`.

#### What are `graph` and `model` context variables?

`graph` exposes the parsed project (all nodes and their metadata), and `model` the current node, which macros can inspect, for example to generate documentation or audits.

#### What is `dbt run-operation` used for?

Running a macro outside the build, for administration tasks: granting permissions, dropping old schemas, loading data, or generating code with the `codegen` package.

#### What is the `codegen` package?

A package with macros that generate boilerplate YAML and SQL, such as source definitions from a schema or a staging model from a source table.

#### How do you override a built-in dbt macro?

Define a macro with the same name in your project, for example `generate_schema_name` or `generate_alias_name`. The project's version takes precedence over the one shipped with dbt.

#### What does `return()` do in a macro?

It returns a Python object (list, dict, number) instead of rendered text, so another macro can use the value.

#### What are Jinja filters, and give examples?

Functions applied with `|`, such as `{{ name | upper }}`, `{{ columns | join(', ') }}` or `{{ value | default('n/a') }}`.

#### How do you avoid over-engineering with Jinja?

Write plain SQL first, extract a macro only when logic repeats or must vary by adapter, document macro arguments, and check the compiled SQL is readable.

#### What is the `star` macro from dbt_utils?

`{{ dbt_utils.star(ref('model'), except=['col']) }}` generates the list of a relation's columns, minus some, to avoid `select *` while not typing every column.

### Testing and data quality

#### What are the two types of tests in dbt?

**Data tests** check the data in the warehouse: generic tests (reusable, parameterized, declared in YAML) and singular tests (one-off SQL queries in `tests/`). **Unit tests**, added in dbt 1.8, check a model's SQL logic against small mocked inputs before it runs on real data.

#### What types of tests can you run in dbt?

The four built-in generic tests (`unique`, `not_null`, `accepted_values`, `relationships`), generic tests from packages (`dbt_utils`, `dbt_expectations`) or your own, singular SQL tests, unit tests, source freshness checks and model contracts.

#### How do the built-in generic tests work?

```yaml
models:
  - name: fct_orders
    columns:
      - name: order_id
        data_tests: [unique, not_null]
      - name: status
        data_tests:
          - accepted_values:
              values: ['placed', 'shipped', 'returned']
      - name: customer_id
        data_tests:
          - relationships:
              to: ref('dim_customers')
              field: customer_id
```

dbt turns each into a query that returns failing rows. The test passes when the query returns no rows.

#### What is a singular test?

A `.sql` file in `tests/` that selects rows violating a rule. It fails if it returns any row:

```sql
-- tests/assert_no_negative_amounts.sql
select * from {{ ref('fct_orders') }} where amount < 0
```

#### How do you write a custom generic test?

With a `{% test name(model, column_name) %}` block that returns failing rows, then use it in YAML like a built-in test:

```sql
{% test is_positive(model, column_name) %}
select * from {{ model }} where {{ column_name }} <= 0
{% endtest %}
```

#### What is a unit test in dbt?

A YAML definition that gives fixed input rows for a model's parents and the expected output, so dbt can check the transformation logic (edge cases, case statements, window functions) without real data:

```yaml
unit_tests:
  - name: test_is_valid_email
    model: dim_customers
    given:
      - input: ref('stg_customers')
        rows:
          - {customer_id: 1, email: a@b.com}
          - {customer_id: 2, email: not-an-email}
    expect:
      rows:
        - {customer_id: 1, is_valid_email: true}
        - {customer_id: 2, is_valid_email: false}
```

#### What is the difference between a unit test and a data test?

A unit test checks code against fixed inputs and runs before the model is built, typically in CI. A data test checks real data after the model is built, every run.

#### What is test severity?

A config setting `severity: warn` or `error` (default). With `warn_if` and `error_if` thresholds such as `">10"`, a test can warn on a few failures and only fail beyond a limit.

#### How do you store test failures?

With `--store-failures` or `store_failures: true`, dbt saves failing rows in a table in an audit schema, so you can inspect them after the run.

#### What does the `where` config on a test do?

It limits the test to a subset of rows, for example only recent data: `config: {where: "order_date >= current_date - 7"}`.

#### What is `dbt_expectations`?

A package of generic tests inspired by Great Expectations: value ranges, regular expressions, row counts, distributions, column types and more.

#### How do you test that a combination of columns is unique?

With `dbt_utils.unique_combination_of_columns`:

```yaml
data_tests:
  - dbt_utils.unique_combination_of_columns:
      combination_of_columns: [order_id, line_number]
```

#### What should you test at minimum on every model?

The primary key with `unique` and `not_null`, foreign keys with `relationships` on important joins, and categorical columns with `accepted_values`. Add business rules where errors would be costly.

#### What does "testing at the source" mean?

Putting tests on sources and staging models, so problems in raw data are caught at the entrance rather than discovered in a dashboard.

#### How do you avoid alert fatigue with dbt tests?

Use `warn` severity and thresholds for non-critical checks, test what matters to consumers, remove tests that never catch anything meaningful, and route errors to owners.

#### How does dbt ensure data quality across the pipeline?

Through tests at each layer, source freshness, contracts on public models, `dbt build` skipping downstream models when a test fails, and CI that runs modified models and their tests before merging.

#### What is the difference between `dbt test` and `dbt build` regarding tests?

`dbt test` runs tests on already-built models. `dbt build` interleaves building and testing in DAG order, so a failing test stops its children from being built.

#### How do you test a model's row count against another?

With a package test such as `dbt_utils.equal_rowcount` or `dbt_expectations.expect_table_row_count_to_equal_other_table`, or a singular test comparing counts.

#### How can you check that a value falls within a range?

With `dbt_utils.accepted_range` (`min_value`, `max_value`) or `dbt_expectations.expect_column_values_to_be_between`.

#### What is a recency test?

A test such as `dbt_utils.recency` that fails when the most recent timestamp in a model is older than a threshold, detecting models that stopped receiving data.

### Incremental models

#### How can you make incremental models in dbt and when would you use them?

Set `materialized='incremental'` and filter new rows with `is_incremental()`. The first run builds the whole table, later runs only process rows newer than what is already there. Use them for large, append-heavy tables (events, logs, transactions) where rebuilding everything each run is too slow or expensive.

```sql
{{ config(materialized='incremental', unique_key='event_id') }}

select * from {{ ref('stg_events') }}
{% if is_incremental() %}
where event_time > (select max(event_time) from {{ this }})
{% endif %}
```

#### What does `is_incremental()` return?

True only when the model is incremental, the target table already exists, and the run is not a `--full-refresh`.

#### What is `unique_key` in an incremental model?

The column (or list of columns) identifying a row. With it, rows that already exist are updated instead of duplicated, depending on the strategy.

#### What incremental strategies exist?

Depending on the adapter: `append` (insert only), `merge` (upsert on `unique_key`), `delete+insert` (delete matching keys then insert), `insert_overwrite` (replace whole partitions, BigQuery and Spark), and `microbatch` (process time-based batches).

#### How does dbt handle incremental loading of data from source systems?

dbt doesn't extract from source systems: it processes data already loaded into the warehouse. Incremental models select only rows newer than the latest already processed (using a timestamp or ID), and merge or append them. Loaders like Fivetran or Airbyte bring the data in incrementally, and dbt transforms it incrementally.

#### What is the microbatch strategy?

Added in dbt 1.9, it processes data in independent time batches (for example one per day) based on an `event_time` column, so batches can be retried, run in parallel or backfilled with `--event-time-start` and `--event-time-end`.

#### How do you handle late-arriving data in incremental models?

Use a lookback window rather than a strict "greater than max": reprocess the last few days, and rely on `unique_key` with `merge` to update rows already loaded.

```sql
{% if is_incremental() %}
where event_time >= (select dateadd(day, -3, max(event_time)) from {{ this }})
{% endif %}
```

#### What does `on_schema_change` do?

It defines what happens when an incremental model's columns change: `ignore` (default), `fail`, `append_new_columns`, or `sync_all_columns`.

#### When should you do a full refresh of an incremental model?

When the logic changes in a way that affects historical rows, when columns change in ways `on_schema_change` doesn't handle, or to repair data. Some tables are protected with `full_refresh: false` because rebuilding them is too costly.

#### What are the risks of incremental models?

Duplicates if `unique_key` is missing or wrong, missed rows if the filter misses late data, divergence from a full rebuild if logic changes, and complexity for testing. A periodic full refresh in a lower environment helps detect drift.

#### What is the difference between `merge` and `delete+insert`?

`merge` updates matching rows and inserts new ones in one statement. `delete+insert` deletes existing rows with the same keys and inserts the new batch. It is useful where merge is slow or unsupported.

#### What is `insert_overwrite`, and when is it efficient?

It replaces entire partitions (for example the days present in the new batch) instead of merging row by row. It is efficient on partitioned tables in BigQuery, Spark and Databricks when data arrives by partition.

#### What does `incremental_predicates` do?

It adds extra conditions to the merge, for example limiting the target scan to recent partitions, which reduces cost on large tables.

#### Can an incremental model reference itself?

Yes, through `{{ this }}` inside the `is_incremental()` block, typically to read the current maximum timestamp.

#### How do you test an incremental model properly?

Test the primary key for uniqueness (duplicates are the usual bug), compare with a full refresh in a lower environment, and write unit tests that override `is_incremental` to true and false.

#### What is an "append-only" incremental model?

One with the `append` strategy and no `unique_key`: rows are only inserted. It suits immutable event logs where records never change.

#### How does partitioning or clustering interact with incremental models?

Partitioning or clustering the target on the filter column (usually a date) makes both the incremental filter and the merge read less data, which is where most of the savings come from.

#### Why might an incremental model become slower over time?

The merge has to scan an ever-growing target table. Incremental predicates, partition pruning, clustering, or the `insert_overwrite` and `microbatch` strategies keep each run bounded.

#### How do you backfill an incremental model?

With `--full-refresh`, or for microbatch models with `--event-time-start` and `--event-time-end` to reprocess a period, or by running with a var that changes the filter window.

#### What is the difference between an incremental model and a snapshot?

An incremental model keeps the latest state (or appends events) and its logic is yours. A snapshot keeps the full history of changes to mutable records, as SCD Type 2 rows with validity dates.

### Snapshots

#### What is snapshot?

A dbt resource that records changes to a mutable table over time (Slowly Changing Dimension Type 2). Each run compares the current source rows with the snapshot table, closes changed rows by setting `dbt_valid_to`, and inserts their new version with `dbt_valid_from`.

#### How do you define a snapshot?

In recent dbt versions, in YAML (older projects use a `{% snapshot %}` block in `snapshots/`):

```yaml
snapshots:
  - name: customers_snapshot
    relation: source('crm', 'customers')
    config:
      schema: snapshots
      unique_key: customer_id
      strategy: timestamp
      updated_at: updated_at
```

#### What snapshot strategies exist?

`timestamp`: a row changed if its `updated_at` column is newer. It is reliable and efficient when the source keeps such a column. `check`: a row changed if any of the listed `check_cols` (or all columns) differ. It is used when there is no trustworthy timestamp.

#### Which columns does dbt add to a snapshot?

`dbt_scd_id`, `dbt_updated_at`, `dbt_valid_from` and `dbt_valid_to` (NULL for the current version, unless `dbt_valid_to_current` is configured).

#### How do snapshots handle deleted source rows?

By default they don't. With `hard_deletes: invalidate` (formerly `invalidate_hard_deletes`), deleted rows get their `dbt_valid_to` set. With `hard_deletes: new_record`, a new row marks the deletion explicitly.

#### Why should snapshots read from sources rather than transformed models?

Snapshots capture history that can't be recreated later. Snapshotting raw data with minimal logic means a bug in transformation code doesn't corrupt the history, and transformations can be re-run on top of it.

#### How often should snapshots run?

As often as changes need to be captured: changes that happen and revert between two runs are lost. Many teams run them hourly or daily, before the models that use them.

#### How do you query the current version of each record in a snapshot?

`where dbt_valid_to is null` (or the configured current value).

#### How do you get the state of a record at a given date?

```sql
select * from {{ ref('customers_snapshot') }}
where '2026-06-30' >= dbt_valid_from
  and ('2026-06-30' < dbt_valid_to or dbt_valid_to is null)
```

#### Can you full-refresh a snapshot?

No. Snapshots are never rebuilt by dbt, because history would be lost. To change one, you migrate the table manually or start a new snapshot.

#### What happens if the `unique_key` isn't unique in the source?

The snapshot produces duplicate or inconsistent versions. Test uniqueness on the source and deduplicate upstream if needed.

#### When would you use the `check` strategy with `check_cols: all`?

When the source has no reliable `updated_at` and any column change matters. It is more expensive because every column is compared.

#### How are snapshots different from Delta Lake time travel or warehouse time travel?

Warehouse time travel keeps past table versions for a limited retention period and is meant for recovery. Snapshots build a permanent, queryable history table at row level, designed for analysis.

#### What is an SCD Type 2, and how do dbt snapshots implement it?

A slowly changing dimension that keeps a new row for each version of a record, with validity dates. dbt snapshots are exactly that: one row per version, `dbt_valid_from` and `dbt_valid_to` bounding its validity.

#### How do you build a dimension with history from a snapshot?

Select from the snapshot in a model, rename `dbt_valid_from` and `dbt_valid_to` to friendlier names, add a surrogate key per version and an `is_current` flag, and join facts on the natural key and the fact's date within the validity range.

### Documentation, lineage and the semantic layer

#### How does dbt generate documentation?

`dbt docs generate` builds a static site from the project (descriptions, columns, tests, SQL) and from warehouse metadata (column types, row counts). `dbt docs serve` serves it locally. It includes an interactive lineage graph.

#### Where do you write descriptions?

In YAML properties files next to models (`description:` on models and columns), or in `{% docs %}` blocks in `.md` files referenced with `{{ doc('name') }}` for longer text.

#### What is `persist_docs`?

A config that writes model and column descriptions into the warehouse as table and column comments, so they are visible in other tools.

#### What are exposures?

YAML declarations of downstream uses of dbt models (dashboards, ML models, applications) with owners, so lineage shows what depends on each model.

#### What does `dbt ls` do?

It lists the nodes matching a selection without running them, which is useful to check selectors.

#### What is the `manifest.json` artifact?

A JSON file in `target/` describing the whole project (nodes, configurations, dependencies). It is used for state comparison (`state:modified`), documentation and external tools.

#### What is `run_results.json`?

An artifact with the result, timing and status of each node in the last invocation, used for monitoring and `dbt retry`.

#### What is the semantic layer architecture of dbt?

Semantic models are defined in YAML on top of dbt models, declaring entities (join keys), dimensions and measures. Metrics are defined on those measures. MetricFlow turns a metric request (metric, dimensions, filters, grain) into optimized SQL for the warehouse, and the dbt platform exposes it through APIs and integrations to BI tools.

#### What is a semantic model?

A YAML definition tied to one dbt model that describes its entities, dimensions and measures, so MetricFlow knows how to aggregate and join it.

#### What types of metrics exist in the semantic layer?

Simple (one measure), ratio, cumulative (running totals or windows), derived (expressions over other metrics) and conversion metrics.

#### Why define metrics in dbt rather than in the BI tool?

So the definition lives once, in version control, with tests and review, and every tool returns the same number for "revenue" or "active users".

#### What is column-level lineage?

Lineage that shows which upstream columns feed each column, not just which models depend on which. The dbt platform and dbt Fusion provide it.

#### What are dbt artifacts used for in observability?

Tools parse `manifest.json` and `run_results.json` to track run duration, test failures and freshness over time, and the `dbt_artifacts` package loads them into the warehouse for analysis.

#### What are meta fields?

A free `meta:` dictionary on nodes and columns, for example to record owners, PII flags or SLAs, which tools and macros can read.

#### How do you document a test or a macro?

Tests and macros can have `description` properties in YAML, which appear in the generated docs.

### Deployment, environments, CI/CD and orchestration

#### How would you manage dbt deployments across multiple environments (dev, staging, production)?

Use one codebase and several targets (or dbt platform environments) pointing to separate schemas or databases: each developer builds into a personal dev schema, CI builds into a temporary schema, and scheduled jobs build production. Environment differences come from `profiles.yml`, environment variables and `target.name`, never from code edits. Changes reach production only through pull requests and CI.

#### How do you handle version control on dbt when working with multiple team members?

Git with feature branches and pull requests, code review, CI that builds and tests modified models on every pull request, a style guide and linter (SQLFluff), clear model ownership, small focused changes, and a personal dev schema per developer so nobody overwrites anyone else's tables.

#### What is Slim CI?

Running only modified models and their dependants in CI, by comparing with production artifacts: `dbt build --select state:modified+ --defer --state prod-artifacts/`. Unchanged parents are read from production instead of rebuilt.

#### What does `state:modified` select?

Nodes whose SQL, configuration or properties differ from the manifest given with `--state`. Combined with `+` it includes their children.

#### Name three advantages of integrating dbt with Airflow.

1. dbt runs are orchestrated with the rest of the pipeline (wait for ingestion, then transform, then refresh dashboards or train models).
2. Retries, alerts, SLAs, backfills and scheduling come from Airflow.
3. With tools like Astronomer Cosmos, each dbt model becomes an Airflow task, giving fine-grained visibility and the ability to retry only failed models.

#### How would you implement dbt in an existing data pipeline?

Start by declaring the existing raw tables as sources, then reproduce current transformations as staging and mart models one domain at a time, comparing outputs with the legacy tables (for example with `audit_helper`). Add tests and documentation, run dbt from the existing orchestrator after ingestion, switch consumers to the new tables, and retire legacy scripts gradually.

#### How do you schedule dbt in production with dbt Core?

With an orchestrator (Airflow, Dagster, Prefect, cron, GitHub Actions, Databricks Workflows) that runs `dbt build` (or selected commands) in a container or virtual environment with production credentials.

#### What does a typical production job look like?

`dbt deps`, `dbt source freshness`, `dbt build` (seeds, snapshots, models and tests in order), then `dbt docs generate`, with alerts on failure and artifacts saved for the next CI comparison.

#### How do you deploy dbt in the dbt platform (dbt Cloud)?

Create deployment environments with their credentials, define jobs (commands, schedule or triggers, selected models), enable CI jobs on pull requests, and use job chaining or API triggers to start dbt after ingestion.

#### What security measures does dbt support for data access and transformation?

dbt runs with the warehouse permissions of the credentials it uses, so least-privilege service accounts per environment are the main control. It also offers `grants` configs to manage privileges on built objects, secrets kept in environment variables (masked when prefixed `DBT_ENV_SECRET_`), model access levels and contracts. The dbt platform adds SSO, role-based access control, audit logs and IP restrictions.

#### How does dbt ensure data security?

dbt never stores or moves the data itself: transformations run inside the warehouse, so data stays under the warehouse's access controls, encryption and governance. dbt holds only connection credentials, which should be secrets with minimal privileges.

#### What does the `grants` config do?

It declares privileges, and dbt applies them after building a model:

```yaml
models:
  +grants:
    select: ['reporter', 'analyst']
```

#### How do you monitor and troubleshoot issues in dbt?

Check the console output and `logs/dbt.log`, read the compiled SQL in `target/compiled` and `target/run`, inspect `run_results.json` for failures and timings, store test failures, use `dbt retry` after fixing, and track run history and durations in the orchestrator or dbt platform. Alerts on job failures and source freshness catch problems early.

#### How can you debug your dbt models?

Run `dbt compile` and execute the compiled SQL directly in the warehouse, preview with `dbt show`, isolate CTEs step by step, use `{{ log() }}` in Jinja, run with `--debug` for full logs, and check upstream data with tests.

#### How does dbt compile queries?

dbt parses the project and builds the DAG, then for each node renders the Jinja: it resolves `ref`, `source`, `var`, `config` and macro calls into plain SQL for the current target. The compiled `SELECT` is written to `target/compiled/`. At run time the materialization wraps it in DDL/DML (`create table as`, `merge`) and sends it to the warehouse through the adapter.

#### What is SQLFluff?

A SQL linter and formatter with a dbt templater, used in CI and pre-commit hooks to enforce a consistent SQL style.

#### How do you run dbt in a Docker container?

Use an image with dbt Core and the adapter installed, mount or copy the project, pass credentials via environment variables, and run commands such as `dbt build --target prod`.

#### What is dbt Mesh?

A pattern for large organizations where several dbt projects reference each other's public models (cross-project `ref`), with contracts, versions and access controls, so domains own their projects independently.

#### How do you trigger dbt after ingestion finishes?

Through the orchestrator (a task dependency or sensor), dbt platform API triggers or job chaining, or the ingestion tool's integration (for example Fivetran triggering a dbt job).

#### What is blue-green deployment with dbt?

Building production into a new schema or database, testing it, then swapping it in atomically (renaming schemas or swapping views), so consumers never see partially built data.

### Performance, warehouses and troubleshooting

#### How can you optimize the performance of dbt transformations on large datasets?

Materialize expensive models as tables and use incremental models for large fact tables, filter and aggregate early, avoid `select *` and unnecessary joins, partition and cluster big tables on filter columns, use the warehouse's native features (clustering keys, sort keys), limit data in development, and look at query profiles and `run_results.json` timings to find the slowest models.

#### Name some optimization techniques for dbt when run in Snowflake.

Use transient tables for intermediate models (no Fail-safe storage cost), cluster very large tables on common filter columns, size warehouses per job (and use separate warehouses for dbt and BI), use `merge` or `delete+insert` with incremental predicates, rely on zero-copy cloning for dev and CI (`dbt clone`), set `query_tag` to attribute costs, and auto-suspend warehouses.

#### How would you compare dbt and BigQuery?

They aren't alternatives: BigQuery is a serverless data warehouse that stores and processes data, while dbt is a transformation framework that generates SQL and runs it in BigQuery (through dbt-bigquery). BigQuery's own scheduled queries or Dataform cover similar ground to dbt, but dbt adds portability across platforms, a large package ecosystem and a broad community. On BigQuery, dbt supports partitioning, clustering and `insert_overwrite`.

#### How do you make dbt runs faster overall?

Increase `threads` within warehouse limits, remove unnecessary models, convert rarely queried tables to views (or the reverse for heavy views), use incremental models, run only what changed (`state:modified+`) in CI, and split jobs by freshness needs.

#### Why can a long chain of views be slow?

Each query on the final view executes the whole chain of underlying SQL. Materializing key intermediate models as tables stops repeated computation.

#### How do you find the slowest models?

From `run_results.json` timings, the dbt platform's model timing view, or the warehouse query history filtered by the dbt `query_tag`.

#### What is the cost impact of views vs tables vs incremental models?

Views cost compute every time they are queried. Tables cost compute at each build plus storage. Incremental models cost little per run but need care to stay correct.

#### What causes "fan-out" in dbt models, and how do you catch it?

Joining on a key that isn't unique on one side multiplies rows, inflating sums. Uniqueness tests on join keys and on each model's grain catch it.

#### How do you limit data in development to save time and cost?

Filter by date or sample with `target.name == 'dev'`, use `--defer` to reuse production parents, or use zero-copy clones.

#### How do you handle model dependencies that form a cycle?

dbt refuses cycles. Restructure the logic, usually by extracting the shared part into an upstream model that both models reference.

#### What happens when a model fails in the middle of a run?

Its downstream models are skipped, independent branches continue, and the run reports the failure. Fix it and run `dbt retry`, or rerun the failed model and its children with `model+`.

#### How do you handle schema changes in sources?

Detect them with tests and contracts, use explicit column lists in staging rather than `select *`, configure `on_schema_change` for incremental models, and adapt staging models in one place.

#### How do you deal with duplicate rows coming from a source?

Deduplicate in the staging model, usually with a window function keeping the latest row per key, and test uniqueness afterwards:

```sql
select *
from {{ source('crm', 'customers') }}
qualify row_number() over (partition by customer_id order by updated_at desc) = 1
```

#### How do you monitor and troubleshoot issues with dbt in production?

Alert on job failures and test errors, track test failure trends and run durations, check source freshness before running, keep artifacts for comparison, and document an on-call procedure (inspect logs and compiled SQL, rerun with `dbt retry`, communicate data incidents to consumers).

#### What would you check when a dbt job suddenly takes twice as long?

Data volume growth in sources, a model that changed materialization or lost its incremental filter, a full refresh triggered by mistake, warehouse size or queuing, a new join that fans out, and missing partition pruning.
