## dbt Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![dbt study guide: about 200 questions](../../images/dbt_study_guide_title_img.png)

About 200 interview-style questions on dbt (data build tool), from the basics to incremental models, snapshots, testing, deployment and performance. The answers follow current dbt: v2, the Rust engine installed by default, and the YAML conventions shared with dbt v1.10 and later. Where dbt v1 behaves differently, the answer says so.

The guide follows a learning path in four stages. Each section is split into short units: learning goals, a concept explanation and a worked example, then questions (recall first, then application), a practical challenge and key takeaways. To **learn**, read each unit top to bottom. To **review**, switch to review mode or use "Skip to questions", mark answers you want to see again, and try a mixed review across sections.

<!-- QA -->
<!-- stage: Foundations -->

### Fundamentals

<!-- unit: What dbt is -->

<!-- goals -->

- Explain what dbt does and where it fits in ELT.
- Compare dbt with ETL tools and stored procedures, including its limits.

<!-- concept -->

Once raw data is loaded into a warehouse, someone has to turn it into clean, trustworthy tables. For years that meant stored procedures and scripts run in a fixed order that only their author understood. dbt replaces them with a framework: each transformation is a `SELECT` in a file, dependencies are declared in the code, and dbt builds everything in the right order inside the warehouse.

Software practices come with it: version control, tests, documentation and reviews. What dbt doesn't do is move data in or schedule itself.

<!-- example -->

```sql
-- models/marts/fct_orders.sql
select
    o.order_id,
    o.customer_id,
    o.ordered_at,
    sum(p.amount) as amount
from {{ ref('stg_shop__orders') }} o
left join {{ ref('stg_shop__payments') }} p using (order_id)
group by 1, 2, 3
```

#### What is dbt?

dbt (data build tool) is a transformation framework: you write `SELECT` statements as models, and dbt compiles them with Jinja, works out their dependencies and runs them in your data warehouse as tables or views. It brings software engineering practices (version control, testing, documentation, modularity, CI/CD) to SQL transformations. dbt is the "T" in ELT.

#### What are common use cases for dbt?

Building a data warehouse or lakehouse layer by layer (staging, intermediate, marts), cleaning and standardizing raw data, building dimensional models for BI, historizing slowly changing data with snapshots, testing data quality, documenting datasets with lineage, and defining shared business metrics in the semantic layer.

#### How does dbt differ from traditional ETL tools?

Traditional ETL tools extract, transform in their own engine, then load, often through a GUI. dbt only transforms, inside the warehouse that already holds the loaded data (ELT), using SQL in plain text files. Everything is code: versioned in Git, reviewed, tested and deployed like software. Extraction and loading are left to other tools (Fivetran, Airbyte, custom pipelines).

#### What does ELT mean, and why does dbt fit it?

Extract, Load, Transform: raw data is loaded into the warehouse first and transformed there. Modern warehouses are cheap to store in and powerful to compute in, so transforming in SQL where the data already sits is simpler and scalable. dbt provides the structure for that transform step.

#### What problems does dbt solve compared with stored procedures and scripts?

Dependencies are explicit and resolved automatically, code is modular and reusable through `ref` and macros, tests and documentation live next to the code, environments are switched through configuration rather than edits, and everything is version-controlled and reviewable.

#### What are the challenges with dbt?

It only covers transformation, so you need other tools for ingestion and orchestration. Large projects can become slow to compile and hard to navigate without conventions. Incremental models and snapshots need careful design. Jinja can make SQL hard to read when overused. Performance still depends on the warehouse and the SQL you write, and costs can grow if full refreshes run too often.

<!-- challenge -->

A team has 80 stored procedures run by a scheduler in a hand-maintained order. Name two concrete improvements dbt would bring and one thing they'd still need.

<!-- solution -->

dbt would derive the run order from `ref()` dependencies and add tests and documentation next to the code in Git. They'd still need ingestion into the warehouse and an orchestrator or scheduler to run dbt.

<!-- takeaways -->

- dbt turns `SELECT` statements into managed tables and views.
- Dependencies, tests and docs live with the code.
- Ingestion and orchestration stay outside dbt.

<!-- unit: dbt in the ecosystem -->

<!-- goals -->

- Compare dbt with Spark and distinguish self-hosted dbt from the dbt platform.
- Explain adapters, dbt v1 and v2, static analysis and the Semantic Layer.

<!-- concept -->

dbt is not a query engine. It generates SQL (or Python) and sends it to a data platform through an adapter, so the warehouse does the work. That's why it pairs with Spark-based platforms rather than competing with them.

You can run dbt yourself from the command line or use the managed dbt platform, which adds an IDE, scheduling and hosted features. The dbt engine itself comes in two generations: v1, the original Python CLI, and v2, a Rust rewrite (first known as dbt Fusion) that is now the default install. v2 runs the same project code but also understands the SQL it compiles.

<!-- example -->

| Piece | Role |
|---|---|
| dbt v2 | Default engine, written in Rust: fast parsing, SQL comprehension, `dbt lint` |
| dbt v1 | Original Python engine (formerly dbt Core), still maintained |
| dbt platform (formerly dbt Cloud) | Studio IDE, jobs, CI, Catalog, Semantic Layer APIs |
| Adapter | Talks to Snowflake, BigQuery, Databricks, Redshift... |

#### How does dbt compare to Apache Spark?

Spark is a distributed processing engine that you program in Python, Scala or SQL, and you manage its jobs and clusters. dbt is not an engine: it generates SQL and sends it to an engine (Snowflake, BigQuery, Redshift, Databricks, Postgres, and Spark itself through the dbt-spark or dbt-databricks adapters). They are complementary: dbt can orchestrate SQL transformations that Spark executes, while complex non-SQL processing stays in Spark code.

#### What is the difference between self-hosted dbt and the dbt platform?

Self-hosted dbt is the command-line tool you install (`pip install dbt` or a native installer), run and orchestrate yourself; this is what used to be called dbt Core. The dbt platform (formerly dbt Cloud) is the managed commercial service: Studio IDE, job scheduler, CI jobs, Catalog for documentation and lineage, the Semantic Layer APIs, alerts and access control. Both run the same project code, and the platform supports both engine versions.

#### What are dbt v1 and dbt v2?

The two generations of the dbt engine. dbt v1 is the original Python implementation (the 1.x releases of dbt Core). dbt v2 is a rewrite in Rust, first released as dbt Fusion, and is now what `pip install dbt` installs. Projects carry over, but v2 is stricter: misspelled configs, unknown YAML keys, missing macros and undefined variables fail at parse time instead of being ignored or failing later. In return, v2 parses much faster and adds static analysis, column-level lineage, a built-in linter (`dbt lint`), project checks (`dbt check`) and a language server for the VS Code extension. Both generations produce compatible artifacts, so they can run side by side during a migration.

#### What is static analysis in dbt v2?

After rendering the Jinja, v2 parses each model's SQL into a logical plan without querying the warehouse. That lets it catch SQL errors before anything runs. The `static_analysis` config controls how strict this is. `baseline`, the default, reports problems as warnings. `strict` resolves column types across the whole DAG and fails before execution; it's required for column-level lineage. dbt v1 only renders templates, so SQL errors appear when the warehouse runs the query.

#### What is a dbt adapter?

A plugin that lets dbt talk to a specific data platform, translating dbt's generic operations into that platform's SQL dialect: Snowflake, BigQuery, Databricks, Redshift, Postgres, Spark and many community adapters. In dbt v1 they are Python packages (`dbt-snowflake`, `dbt-bigquery`...). In dbt v2 they connect through ADBC drivers that dbt downloads on first use, so dbt ships as a single binary.

#### What is the dbt Semantic Layer?

A layer, built on MetricFlow, where metrics (revenue, active users) are defined once in YAML on top of dbt models, then queried consistently by BI and other tools through APIs, so every tool computes the metric the same way.

<!-- challenge -->

A team on Databricks asks whether to use dbt or Spark for transformations. What do you answer?

<!-- solution -->

Both: dbt can run SQL (and Python) models on Databricks through the adapter, with Spark executing them. Use dbt for SQL-friendly modeling with tests and lineage; use Spark jobs directly for complex code-heavy processing.

<!-- takeaways -->

- dbt generates code; the platform executes it.
- dbt v2 (Rust) is the default engine; v1 is the original Python one.
- The dbt platform adds managed features on top of either engine.

<!-- unit: Models and the DAG -->

<!-- goals -->

- Describe dbt models and the DAG built from their references.
- Choose between SQL and Python models and design modular layers.

<!-- concept -->

A model is one file with one `SELECT`. When it references another model with `ref()`, dbt records an edge, and the edges together form a DAG that decides build order and what can run in parallel.

That makes modularity cheap: small models with one responsibility each, reused by many downstream models. Python models fit the few transformations SQL handles badly, while still sitting in the same DAG.

<!-- example -->

```python
# models/ml/customer_features.py
def model(dbt, session):
    orders = dbt.ref("fct_orders").to_pandas()
    feats = orders.groupby("customer_id").agg(orders=("order_id", "count"), spend=("amount", "sum"))
    return feats.reset_index()
```

#### What is a dbt model?

A `.sql` file in the `models/` folder containing one `SELECT` statement. dbt wraps it in the DDL needed to create a view, table or other object named after the file. Python models (`.py`) are also supported on some platforms.

#### What is the DAG in the context of dbt?

The Directed Acyclic Graph of dependencies between models, sources, seeds and snapshots, built from `ref()` and `source()` calls. dbt uses it to run nodes in the right order (and in parallel when possible), to select parts of the project, and to draw lineage in the docs.

#### What does "modular data modeling" mean in dbt?

Splitting transformations into small, reusable models with one responsibility each (staging per source, intermediate logic, final marts), connected with `ref`, instead of large monolithic queries.

#### Which languages can you write dbt models in?

SQL (with Jinja) everywhere, and Python on Snowflake (Snowpark), Databricks (PySpark) and BigQuery (BigQuery DataFrames or Dataproc). The Python code runs on the data platform, not on the machine running dbt. Python models return a DataFrame and are useful for logic that is awkward in SQL.

#### What is a Python model in dbt?

A `.py` file defining `model(dbt, session)` that returns a DataFrame. It can reference other models with `dbt.ref()` and is materialized as a table or incremental model; views and ephemeral models aren't possible in Python, and Python models can't reference ephemeral models.

```python
def model(dbt, session):
    dbt.config(materialized="table")
    orders = dbt.ref("stg_orders")
    return orders.groupBy("customer_id").count()
```

<!-- challenge -->

Five mart models each repeat the same 40-line join between orders and payments. How do you restructure them?

<!-- solution -->

Extract the join into one intermediate model (for example `int_orders_with_payments`) and have the five marts `ref()` it. The logic lives once, and the DAG shows the shared dependency.

<!-- takeaways -->

- A model is one `SELECT` in one file.
- `ref()` builds the DAG and the run order.
- Small, single-purpose models are easy to reuse.

<!-- unit: Core commands -->

<!-- goals -->

- Use the most common dbt commands.
- Explain what `dbt build`, `dbt debug` and `dbt compile` do.

<!-- concept -->

A handful of commands cover daily work. Running builds models; testing checks them; building does both, plus seeds and snapshots, in DAG order and skips what depends on a failure. Compiling renders the SQL without running it, which is how you see what dbt will actually send. Debugging checks the setup and connection.

Knowing which command to use saves time and avoids building on top of broken data.

<!-- example -->

```bash
dbt debug                           # config and connection OK?
dbt compile --select fct_orders     # see rendered SQL in target/compiled
dbt build --select +fct_orders      # build and test fct_orders and its parents
```

#### Which commands are the most common in dbt?

`dbt run` (build models), `dbt test` (run tests), `dbt build` (seeds, models, snapshots and tests in DAG order), `dbt seed`, `dbt snapshot`, `dbt compile`, `dbt show`, `dbt retry`, `dbt docs generate` / `dbt docs serve`, `dbt debug`, `dbt deps`, `dbt clean`, `dbt ls`, `dbt run-operation` and `dbt source freshness`. dbt v2 adds `dbt freshness` (sources and models), `dbt check` (project standards) and `dbt lint` (SQL style).

#### What does `dbt build` do?

It runs seeds, models, snapshots and their tests in DAG order, testing each node right after building it. If a test with `error` severity fails, the nodes downstream are skipped, so bad data doesn't propagate. In dbt v2, `dbt build` also runs all unit tests first and evaluates project checks before any warehouse work.

#### What is `dbt debug` used for?

It checks the installation, `dbt_project.yml`, `profiles.yml`, required dependencies such as `git`, and the connection to the warehouse. It is the first thing to run when nothing works.

#### What is the difference between `dbt run` and `dbt compile`?

`dbt compile` renders the Jinja and writes the resulting SQL to `target/compiled/` without building anything. It still connects to the warehouse when models need introspection (for example `run_query`). `dbt run` compiles and executes, writing the executed statements (with DDL) to `target/run/`.

<!-- challenge -->

A production job runs `dbt run` then `dbt test`. A broken staging model produced duplicates, and every downstream model was rebuilt on them before tests failed. What do you change?

<!-- solution -->

Use `dbt build`, which tests each node right after building it and skips its children when a test fails, so bad data doesn't propagate.

<!-- takeaways -->

- `build` = run + test + seed + snapshot in DAG order.
- `compile` shows the SQL without running it.
- `debug` checks configuration and connection.

### Projects and configuration

<!-- unit: Project and connection files -->

<!-- goals -->

- Describe `dbt_project.yml`, `profiles.yml`, targets and threads.
- Keep credentials in environment variables.

<!-- concept -->

A dbt project has two kinds of configuration. The project file travels with the code: name, paths, default configs per folder. The profile stays with the person or machine running dbt: which platform, which credentials, which target such as `dev` or `prod`.

That split is what lets one codebase build into many environments. Environment variables complete it, keeping secrets out of every file.

<!-- example -->

```yaml
# profiles.yml
shop:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('DBT_USER') }}"
      password: "{{ env_var('DBT_PASSWORD') }}"
      database: analytics_dev
      schema: "dbt_{{ env_var('USER') }}"
      threads: 8
```

#### What is a dbt project?

A directory containing a `dbt_project.yml` file plus models, tests, macros, seeds, snapshots, analyses and documentation. It's the unit that dbt compiles and runs, usually one Git repository.

#### What goes in `dbt_project.yml`?

The project name, version, `profile` to use, paths (models, seeds, macros…), `vars`, and default configurations per folder, such as `+materialized: table` for all marts or `+schema: staging`.

#### What is `profiles.yml`?

The file holding connection details per profile and target: adapter type, host, database, schema, credentials and threads. dbt looks for it in the directory given by `--profiles-dir` or `DBT_PROFILES_DIR`, then in the project directory, then in `~/.dbt/`. It contains connection secrets, so either keep it out of the repository or commit a version that reads every secret with `env_var()`.

#### What is a target in dbt?

A named connection configuration within a profile, such as `dev` and `prod`. You choose it with `--target`, and models can branch on `target.name`.

#### What are threads in dbt?

The maximum number of nodes dbt builds at the same time. Independent branches of the DAG run in parallel up to that limit. dbt v2 manages parallelism itself on Snowflake and Databricks, where `threads` only acts as a cap, and treats `threads: 0` (or no value) as "optimize automatically" on BigQuery and Redshift.

#### How do you use environment variables in dbt?

With `{{ env_var('DBT_PASSWORD') }}`, optionally with a default value: `{{ env_var('DBT_SCHEMA', 'dbt_dev') }}`. They're commonly used in `profiles.yml` for credentials. Variables prefixed `DBT_ENV_SECRET_` are scrubbed from logs and can only be used in `profiles.yml` and `packages.yml`, not in models.

<!-- challenge -->

A developer committed `profiles.yml` with a production password. What do you change?

<!-- solution -->

Rotate the password, remove it from the repository history, and rewrite the profile to read credentials with `env_var()`. In CI and production, inject them from a secrets manager.

<!-- takeaways -->

- `dbt_project.yml` travels with the code.
- `profiles.yml` holds connections and targets per environment.
- Credentials come from environment variables.

<!-- unit: Configuring nodes -->

<!-- goals -->

- Configure models at file, YAML and project level.
- Select nodes with tags, selectors and variables.

<!-- concept -->

Configuration flows from general to specific: project-level defaults per folder, overridden in YAML, overridden again in the model file. Configs change how dbt builds something; properties describe it. Keeping that distinction clear avoids most "why didn't my setting apply?" questions.

Selection lets you act on part of the DAG: by name, path, tag, state or graph operators. Variables make the same code behave differently per run.

<!-- example -->

```bash
dbt build --select tag:daily
dbt build --select +fct_orders+          # parents, the model, children
dbt run --select path:models/marts --exclude tag:deprecated
dbt run --vars '{start_date: "2026-10-01"}'
```

#### How do you configure a model?

In three places, from most to least specific: a `{{ config(...) }}` block in the model file, a `config:` block in the model's YAML properties, and folder-level settings in `dbt_project.yml`. The most specific wins.

```sql
{{ config(materialized='table', schema='marts', tags=['daily']) }}
select * from {{ ref('int_orders') }}
```

#### What is the difference between configs and properties?

Configs control how dbt builds and manages a node (materialization, schema, tags, meta, hooks, access). Properties describe it (description, columns, tests, docs). Properties live in YAML files; configs can live in YAML under a `config:` key, in the model file or in `dbt_project.yml`, and cascade from general to specific. Since dbt v1.10, configs such as `tags`, `meta` and `access` belong under `config:` in YAML, and dbt v2 rejects them at the top level. Only configs can be used in selection, with `--select config.materialized:incremental`.

#### What are tags used for?

Labels on nodes to select them in commands, for example `dbt run --select tag:daily`, or to group them in jobs.

#### How does node selection work?

With `--select` and `--exclude`, using names, paths, tags, `source:`, `state:`, `resource_type:` and graph operators: `+model` selects the model and its parents, `model+` the model and its children, `@model` the model, its children and their parents.

```bash
dbt build --select +fct_orders          # fct_orders and everything upstream
dbt run --select staging.stripe         # a folder
dbt test --select source:stripe+        # tests on a source and everything downstream
```

#### What are variables (`vars`) in dbt?

Values defined in `dbt_project.yml` or passed on the command line (`--vars '{start_date: 2026-01-01}'`) and read with `{{ var('start_date') }}`, optionally with a default: `{{ var('start_date', '2020-01-01') }}`. Command-line values override the project file. A variable with no value and no default is an error (at parse time in dbt v2).

<!-- challenge -->

All marts should be tables, except one large model that must be incremental. Where do you set each config?

<!-- solution -->

Set `+materialized: table` for the marts folder in `dbt_project.yml`, and override with `{{ config(materialized='incremental', unique_key=...) }}` in the large model's file, which takes precedence.

<!-- takeaways -->

- Configs cascade from project to YAML to file.
- Configs change builds; properties describe nodes.
- Selection targets parts of the DAG.

<!-- unit: Structure and schemas -->

<!-- goals -->

- Organize a project into folders and layers.
- Control schema names with `generate_schema_name`.

<!-- concept -->

A consistent folder structure tells everyone where things belong: staging per source, intermediate for shared logic, marts per business area. Folder-level configs then apply materializations and schemas to whole layers.

By default dbt appends a custom schema to the target schema, which protects developers from writing into production schemas. Teams often override the macro so production gets clean names while development stays isolated. Analyses and cleanup commands round out the project layout.

<!-- example -->

```sql
-- macros/generate_schema_name.sql
{% macro generate_schema_name(custom_schema_name, node) -%}
  {%- if target.name == 'prod' and custom_schema_name is not none -%}
    {{ custom_schema_name | trim }}
  {%- else -%}
    {{ target.schema }}{% if custom_schema_name %}_{{ custom_schema_name | trim }}{% endif %}
  {%- endif -%}
{%- endmacro %}
```

#### How is a dbt project usually structured?

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
functions/    user-defined functions (UDFs)
checks/       project standards checked by dbt check (dbt v2)
```

#### How does dbt decide which schema a model is built in?

By the `generate_schema_name` macro. By default, a custom schema is appended to the target schema (`dbt_alice_marts` in dev, `analytics_marts` in prod). Many projects override the macro to use the custom schema as-is in production.

#### What is the `generate_schema_name` macro, and why override it?

It computes the schema for each node. Overriding it lets you, for example, use exact schema names in production while keeping a personal prefix in development, so developers don't overwrite each other.

#### What are analyses in dbt?

SQL files in `analyses/` that are compiled (Jinja and `ref` resolved) but never executed by `dbt run`. They are useful for ad hoc queries that benefit from dbt's references.

#### What does `dbt clean` do?

It deletes the folders listed in `clean-targets` (usually `target/` and `dbt_packages/`). dbt v2 refuses to delete anything outside the project directory or inside resource paths such as `models/`.

<!-- challenge -->

Production models land in schemas like `analytics_marts` instead of `marts`, and analysts find the names confusing. What do you change without affecting developers?

<!-- solution -->

Override `generate_schema_name` so that in the prod target the custom schema is used as is (`marts`), while other targets keep the prefixed form (`dbt_ana_marts`) to stay isolated.

<!-- takeaways -->

- Organize by layer: staging, intermediate, marts.
- dbt appends custom schemas to the target schema by default.
- Override schema naming for clean production names.

<!-- unit: Packages and governance -->

<!-- goals -->

- Install and use packages such as `dbt_utils`.
- Govern public models with access, groups and versions.

<!-- concept -->

Packages are dbt projects you import: tests, macros and models other people already wrote and tested. Most projects start with `dbt_utils` for common tests and helpers.

As projects grow and serve other teams, models become interfaces. Access levels and groups decide who may reference what, and versions let a breaking change ship as a new version while consumers move at their own pace.

<!-- example -->

```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: [">=1.3.0", "<2.0.0"]
# models/marts/_marts.yml
models:
  - name: fct_orders
    config:
      access: public
      group: finance
    latest_version: 2
    versions: [{v: 1}, {v: 2}]
```

#### What are packages, and how do you install them?

Reusable dbt projects (macros, models, tests) such as `dbt_utils`, `dbt_expectations` or `codegen`. You list them in `packages.yml` and run `dbt deps`, which installs them into `dbt_packages/` and pins the resolved versions in `package-lock.yml`. `dependencies.yml` can hold both packages and cross-project dependencies (dbt Mesh), but dbt v1 doesn't render Jinja in it, so private packages that need a token from an environment variable stay in `packages.yml`.

#### What is `dbt_utils`?

The most used package, with generic tests (`unique_combination_of_columns`, `expression_is_true`, `accepted_range`) and macros (`generate_surrogate_key`, `star`, `date_spine`, `pivot`, `union_relations`).

#### What are model access and groups?

Governance features. A model's `access` config can be `private` (only referenced within its group), `protected` (within the project or when installed as a package; the default) or `public` (also by other projects). Groups gather related models under one owner. dbt Labs recommends `private` for new models that aren't designed for sharing.

#### What are model versions?

A way to publish a breaking change to a public model as a new version while consumers keep using the old one until they migrate. Each version lives in its own file (`fct_orders_v1.sql`, `fct_orders_v2.sql`). `ref('fct_orders', v=1)` pins a version, and a plain `ref('fct_orders')` resolves to `latest_version`. Old versions can get a `deprecation_date` so consumers are warned.

<!-- challenge -->

Another team references your intermediate models directly, and each refactor breaks them. How do you set boundaries?

<!-- solution -->

Put your models in a group, mark intermediate models `private` (or `protected`) and expose only the marts they need as `public` with contracts. Breaking changes then go through model versions.

<!-- takeaways -->

- Packages bring ready-made tests and macros.
- Access and groups define model interfaces.
- Versions let breaking changes coexist.

<!-- stage: Building models -->

### Sources and seeds

<!-- unit: Sources and freshness -->

<!-- goals -->

- Declare sources and reference them with `source()`.
- Test sources and check their freshness.

<!-- concept -->

Raw tables loaded by other tools are dbt's inputs. Declaring them as sources puts their location in one place, starts lineage at the right point and lets you test and check them before anything is built on top.

Freshness checks answer a question that tests don't: did new data arrive at all? Running them first in production stops models from quietly rebuilding on stale data.

<!-- example -->

```yaml
sources:
  - name: shop
    database: raw
    schema: shop
    config:
      loaded_at_field: _loaded_at
      freshness:
        warn_after: {count: 6, period: hour}
        error_after: {count: 24, period: hour}
    tables:
      - name: orders
        columns:
          - name: id
            data_tests: [unique, not_null]
```

#### What are sources in dbt?

Declarations, in YAML, of the raw tables that were loaded into the warehouse by other tools. Models select from them with `{{ source('stripe', 'payments') }}` instead of hard-coded table names, which records lineage, allows tests and documentation on raw data, and enables freshness checks.

```yaml
sources:
  - name: stripe
    database: raw
    schema: stripe
    tables:
      - name: payments
        config:
          loaded_at_field: _loaded_at
          freshness:
            warn_after: {count: 12, period: hour}
            error_after: {count: 24, period: hour}
```

#### Why use `source()` rather than writing the table name?

The table location is defined in one place, lineage starts from the source in the DAG, sources can be selected (`source:stripe+`), and `dbt source freshness` can check them.

#### What is source freshness?

A check that compares the most recent load time of a source with the current time and warns or errors when data is older than the `warn_after` and `error_after` thresholds. dbt reads the maximum of `loaded_at_field` (or the result of a custom `loaded_at_query`), or uses warehouse metadata when neither is set and the platform supports it. Since dbt v1.10, `freshness` and `loaded_at_field` go under `config:`, at source level as defaults or per table as overrides.

#### Can you test sources?

Yes, generic tests can be declared on source columns exactly as on models, catching problems in raw data before they reach your models.

#### What is `dbt source freshness` used for in production?

To detect broken or late ingestion before models run on stale data, often as the first step of a scheduled job. Its results go to `target/sources.json`.

#### What is model freshness, and what does `dbt freshness` do?

dbt v2 extends freshness to models: you set `warn_after` and `error_after` (and a `loaded_at_field` or `loaded_at_query`) in a model's config, and `dbt freshness` checks every source and model with freshness configured in one command, writing `target/freshness.json`. `dbt source freshness` still works but only checks sources. Model freshness is useful on models that consumers query directly, where "the job succeeded" doesn't prove the data is recent.

#### What is the difference between `ref()` and `source()`?

`ref()` points to another dbt node (model, seed, snapshot) and creates a dependency the DAG uses to order runs. `source()` points to raw data loaded outside dbt. Both resolve to the fully qualified table name for the current target.

<!-- challenge -->

An ingestion job failed for two days, and dashboards showed flat numbers without anyone noticing. Which dbt feature would have caught it?

<!-- solution -->

Source freshness on the raw tables with `error_after` thresholds, run as the first step of the production job (and alerting on failure), so the job stops and the team is notified.

<!-- takeaways -->

- Sources declare raw inputs in one place.
- `source()` for raw tables; `ref()` for dbt nodes.
- Freshness checks catch late or broken ingestion.

<!-- unit: Staging and layering -->

<!-- goals -->

- Write staging models as the only consumers of sources.
- Explain staging, intermediate and marts layers across environments.

<!-- concept -->

Staging models are the clean entry point: one per source table, with renames, casts and light cleanup, no joins or business logic. If only staging models read sources, a source change touches one file.

Layers build on that: intermediate models hold reusable joins and logic, marts serve consumers. Because `ref()` resolves to the current target, the same layers build into a developer's schema or production without code changes.

<!-- example -->

```sql
-- models/staging/shop/stg_shop__orders.sql
select
    id::bigint            as order_id,
    customer_id::bigint   as customer_id,
    lower(status)         as status,
    created_at::timestamp as ordered_at
from {{ source('shop', 'orders') }}
```

#### What is a staging model?

The first layer on top of a source: one model per source table, doing only light transformations (renaming, casting, basic cleaning, deduplication). Everything downstream references staging models, not sources directly.

#### Why should only staging models reference sources?

So each raw table is cleaned once, in one place. If the source changes, only its staging model needs updating.

#### What is a "staging, intermediate, marts" layering?

A common structure: staging cleans each source, intermediate holds reusable joins and business logic, marts are the final fact and dimension tables (or wide tables) consumed by BI and analysts.

#### What does `ref()` resolve to in different environments?

To the relation in the current target's database and schema, so the same code builds into a developer's schema in dev and into production schemas in prod.

#### Can dbt work with different data sources and data warehouses?

dbt runs against one data platform per target, through its adapter, and transforms data that is already in that platform. It doesn't extract from source systems. Platforms that can query external data (Snowflake external tables, BigQuery federated queries, Databricks and Trino catalogs) let dbt transform data from several origins through the warehouse.

<!-- challenge -->

A source renames `created_at` to `created_ts`, and nine models break. How would layering have limited the damage?

<!-- solution -->

If only `stg_shop__orders` read the source, the fix would be one line there (`created_ts as ordered_at`); all downstream models use the staging column name and stay unchanged.

<!-- takeaways -->

- Staging: one model per source table, light cleanup only.
- Only staging reads sources.
- `ref()` resolves per target, so layers work in every environment.

<!-- unit: Seeds -->

<!-- goals -->

- Decide when seeds fit and when they don't.
- Set seed column types and reload changed seeds.

<!-- concept -->

Seeds load small CSV files from the repository into the warehouse. They're ideal for static reference data that belongs in version control, such as country codes or mapping tables, and reviewed like code.

They're the wrong tool for anything large, sensitive or changing often; that data belongs in ingestion. Types should be set explicitly, since inference guesses, and changes to columns need a full refresh.

<!-- example -->

```yaml
seeds:
  shop:
    country_codes:
      +column_types:
        iso_code: varchar(2)
        dial_code: varchar(6)
```
```bash
dbt seed --select country_codes --full-refresh
```

#### What is a seed?

A CSV file in the `seeds/` folder that `dbt seed` loads into the warehouse as a table. Models reference it with `ref()` like any model.

#### When should you use seeds, and when not?

For small, static reference data that changes rarely and belongs in version control: country codes, mapping tables, test fixtures. Not for large or frequently changing data, or data that should come from a source system.

#### How do you set column types for a seed?

With the `column_types` config, in `dbt_project.yml` or in the seed's YAML properties; otherwise dbt infers each type from the values:

```yaml
seeds:
  my_project:
    country_codes:
      +column_types:
        code: varchar(2)
```

#### How do you reload a seed whose columns changed?

With `dbt seed --full-refresh`, which drops and recreates the table instead of truncating and inserting.

<!-- challenge -->

A team loads a 300 MB daily export of product prices as a seed. What do you suggest?

<!-- solution -->

Move it to the ingestion layer (a loader or connector into a raw table declared as a source). Seeds are for small, static reference data versioned in Git, not daily data feeds.

<!-- takeaways -->

- Seeds load small, static CSVs from Git.
- Set column types explicitly.
- Changed columns need `--full-refresh`.

### Models and materializations

<!-- unit: Building models and materializations -->

<!-- goals -->

- Create models and let `ref()` manage dependencies.
- Choose between view, table, ephemeral and incremental materializations.

<!-- concept -->

Writing a model is writing a query; the materialization decides what dbt does with it. A view stores nothing and recomputes on every read. A table stores results and recomputes on each build. Ephemeral models are inlined as CTEs into their children. Incremental models add only new data each run.

The choice trades build cost against query cost and freshness, and a project usually uses all of them by layer. When none fits, custom materializations are possible but rarely needed.

<!-- example -->

| Layer | Typical materialization | Why |
|---|---|---|
| Staging | View | Cheap, always current |
| Intermediate | Ephemeral or view | Reused logic, no extra objects |
| Marts | Table | Fast for BI |
| Large facts | Incremental | Process only new rows |

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
- **materialized_view**: a database materialized view that the platform refreshes itself, where supported. Snowflake's equivalent is the adapter-specific `dynamic_table` materialization.

Snapshots and seeds are separate resource types with their own behavior.

#### When should you use a view versus a table?

Views are cheap to build and always current, so they fit staging models and light transformations. Tables are faster to query, so they fit marts used by BI and models that are expensive to compute or queried often.

#### When should you use an ephemeral model?

For light, reusable logic that you don't want as a separate object in the warehouse. Overusing them makes debugging harder because they can't be queried directly.

#### How would you create a custom materialization in dbt?

With a `{% materialization name, adapter='default' %}` block in a macro file. It typically gets the target relation, runs pre-hooks, builds the SQL with `{% call statement('main') %}`, handles existing relations, runs post-hooks and returns `{'relations': [target_relation]}`. Custom materializations are rare: most needs are covered by built-ins and incremental strategies.

<!-- challenge -->

A dashboard queries a mart built as a view on top of four other views, and each refresh takes two minutes. What do you change?

<!-- solution -->

Materialize the mart as a table (and perhaps one expensive intermediate model), so the work happens once per build instead of on every dashboard query.

<!-- takeaways -->

- Materializations decide how a model is stored.
- Views are cheap to build; tables are cheap to read.
- Pick materializations by layer and usage.

<!-- unit: Marts, naming and grain -->

<!-- goals -->

- Design fact and dimension marts with a declared grain.
- Apply naming conventions, surrogate keys, aliases and disabled models.

<!-- concept -->

Marts are the models people use, so they follow dimensional design: facts at a declared grain, dimensions for context. Stating the grain in the description and testing it with a uniqueness test catches the most common modeling bug, a join that multiplies rows.

Conventions make a project navigable: prefixes by layer, surrogate keys generated consistently, aliases when warehouse names must differ from file names, and disabled models for code that shouldn't run on a platform.

<!-- example -->

```sql
-- models/marts/fct_order_lines.sql   grain: one row per order line
select
    {{ dbt_utils.generate_surrogate_key(['order_id', 'line_number']) }} as order_line_key,
    order_id, line_number, product_id, quantity, net_amount
from {{ ref('int_order_lines_enriched') }}
```

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

#### What is the `alias` config?

It sets the name of the relation in the warehouse independently of the model file name.

#### What is a disabled model?

A model with `enabled: false`. dbt ignores it, which is useful for platform-specific or work-in-progress models.

<!-- challenge -->

`fct_orders` suddenly has more rows than there are orders. What test would have caught it, and what usually causes it?

<!-- solution -->

A `unique` test on `order_id` (the declared grain). The usual cause is a join to a table with several rows per order, such as payments or shipments, without aggregating it first.

<!-- takeaways -->

- Marts are facts and dimensions at a declared grain.
- Test the grain with a uniqueness test.
- Consistent names and keys make projects navigable.

<!-- unit: Hooks, contracts and constraints -->

<!-- goals -->

- Run SQL around models with hooks and `{{ this }}`.
- Enforce schemas with model contracts and constraints.

<!-- concept -->

Hooks run extra SQL before or after a model or a whole run: grants, audit inserts, maintenance commands. `{{ this }}` refers to the model's own relation, which hooks and incremental logic need.

Contracts go the other way: instead of adding actions, they add guarantees. With a contract enforced, the model's columns and types must match what's declared, so a refactor can't silently change the interface consumers rely on. Constraints add database-level rules where the platform supports them.

<!-- example -->

```yaml
models:
  - name: dim_customer
    config:
      contract: {enforced: true}
      post_hook: "grant select on {{ this }} to role reporting"
    columns:
      - name: customer_id
        data_type: bigint
        constraints: [{type: not_null}, {type: primary_key}]
      - name: segment
        data_type: varchar
```

#### What are hooks?

SQL executed at given moments: `pre-hook` and `post-hook` around a model, and `on-run-start` / `on-run-end` around the whole invocation. Uses include granting privileges, creating indexes or logging runs.

#### What are pre-hooks and post-hooks?

A `pre-hook` runs SQL just before a model is built, and a `post-hook` just after, inside the same run. For example:

```sql
{{ config(post_hook="grant select on {{ this }} to role reporter") }}
```

#### What does `{{ this }}` refer to?

The relation (database.schema.table) of the model being built. It is used in hooks and in incremental models to query the existing table.

#### What are model contracts?

A `contract: {enforced: true}` config with every column's name and data type declared (and constraints where supported). Before building, dbt runs a preflight check that the model's query returns exactly those columns and types, in any order, and fails the build if not. That protects downstream consumers from schema changes. Contracts apply to SQL models materialized as tables, views (names and types only, no constraints) or incremental models with `on_schema_change` set to `append_new_columns` or `fail`.

#### What are constraints in dbt?

Declarations such as `not_null`, `unique`, `primary_key`, `foreign_key` and `check` on contracted models. dbt adds them to the `create table` DDL where the platform supports them. Support differs: most analytical platforms enforce `not_null`, but they record primary keys, foreign keys and `unique` only as metadata (Snowflake's `primary_key`, for example), so tests are still needed for uniqueness and relationships.

<!-- challenge -->

A developer changes a column from `bigint` to `varchar` in a public model, and a downstream application breaks a week later. What would have stopped this at build time?

<!-- solution -->

An enforced model contract declaring `bigint` for that column: the build fails when the produced type doesn't match, before anything reaches production.

<!-- takeaways -->

- Hooks run SQL before or after models and runs.
- `{{ this }}` is the model's own relation.
- Contracts make column names and types an enforced interface.

<!-- unit: Running and troubleshooting models -->

<!-- goals -->

- Use full refresh, defer, clone, show and retry.
- Fix "relation does not exist" and plan data refreshes.

<!-- concept -->

Day-to-day work needs more than `run`. Full refreshes rebuild incremental models from scratch. Defer and clone let you build only what you changed while reading everything else from production. Show previews results without building; retry reruns only what failed.

Many errors come from environments rather than SQL: a parent never built in your schema, a typo in a source, missing permissions. Knowing the tools above usually resolves them in minutes.

<!-- example -->

```bash
dbt build --select state:modified+ --defer --state prod-artifacts/   # build only my changes
dbt show --select fct_orders --limit 10                              # preview
dbt retry                                                            # rerun failed nodes only
```

#### What is the difference between `dbt run --full-refresh` and a normal run?

`--full-refresh` rebuilds incremental models from scratch and drops and reloads seeds, instead of processing only new data. Models with `full_refresh: false` ignore it, and snapshots always ignore it and run as normal.

#### What does the `--defer` flag do?

With `--state` pointing to production artifacts, it makes `ref()` resolve to production relations for models you haven't built in your environment, so you can run one model in dev without rebuilding all its parents.

#### What is `dbt clone`?

A command that copies selected nodes from a saved state (for example production artifacts given with `--state`) into the current target. On platforms with zero-copy cloning (Snowflake, Databricks, BigQuery) it creates clones of tables; elsewhere it creates views pointing at the original. It speeds up development and CI setups and supports blue-green deployments.

#### What is `dbt show`?

A command that compiles one model, test or analysis (or an inline query with `--inline`), runs it and prints a preview of the results without materializing anything: `dbt show --select stg_orders --limit 10`.

#### What is `dbt retry`?

It re-executes the previous invocation from the point of failure: the nodes that failed or were skipped, with the same flags. If the previous command failed before any node ran (for example on a connection error), there is nothing to retry.

#### How do you deal with the error "relation does not exist" in dbt?

Common causes: a referenced table was never built in the current target (run the parent, or use `--defer`), the table name is hard-coded instead of using `ref`/`source` (so the dependency isn't known and order is wrong), the source definition points to the wrong database or schema, the user lacks permission to see the object, or the identifier has quoting or case problems. Running `dbt compile` and checking the SQL in `target/compiled/` usually shows which name is wrong.

#### What is a data refresh?

Updating the warehouse tables so they reflect the latest source data: a scheduled `dbt build` that rebuilds tables, processes new rows in incremental models and captures changes in snapshots. Its frequency depends on how fresh consumers need the data and how often sources load.

<!-- challenge -->

A developer changes one mart and runs `dbt run --select my_mart` in their dev schema. It fails with "relation does not exist" for a parent model. What are two ways to fix it?

<!-- solution -->

Build the parents too (`--select +my_mart`), or use `--defer --state` with production artifacts so unbuilt parents resolve to production relations (or `dbt clone` them into dev).

<!-- takeaways -->

- Full refresh rebuilds incremental models.
- Defer and clone reuse production for unchanged parents.
- Show previews; retry reruns failures.

### Jinja and macros

<!-- unit: Jinja basics -->

<!-- goals -->

- Use Jinja expressions, statements, variables and filters in models.
- Adapt SQL to the target and keep compiled SQL tidy.

<!-- concept -->

Jinja turns SQL files into templates. Expressions insert values, statements add loops and conditions, and comments disappear on compilation. With variables and filters, repetitive SQL, like one column per payment method, becomes a loop over a list.

The `target` variable lets code adapt to environments, for example sampling data in development. Whitespace control keeps the compiled SQL readable, which matters because that's what you debug.

<!-- example -->

```sql
{% set methods = ['card', 'paypal', 'bank_transfer'] %}
select
    order_id,
    {%- for m in methods %}
    sum(case when method = '{{ m }}' then amount end) as {{ m }}_amount{{ "," if not loop.last }}
    {%- endfor %}
from {{ ref('stg_shop__payments') }}
{% if target.name == 'dev' %} where created_at >= current_date - 30 {% endif %}
group by 1
```

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

#### What is the difference between `{{ }}`, `{% %}` and `{# #}`?

`{{ }}` outputs an expression, `{% %}` runs a statement (if, for, set, macro, call), and `{# #}` is a comment that doesn't appear in the compiled SQL.

#### What does the `-` in `{%-` or `-%}` do?

It trims whitespace before or after the tag, keeping the compiled SQL tidy.

#### How do you set a variable inside a model?

With `{% set %}`, for example `{% set payment_methods = ['card', 'paypal'] %}`, then use it in loops or expressions.

#### What are Jinja filters? Give examples.

Functions applied with `|`, such as `{{ name | upper }}`, `{{ columns | join(', ') }}` or `{{ value | default('n/a') }}`.

#### What is the `target` variable in Jinja?

Information about the current connection: `target.name`, `target.schema`, `target.type`, `target.threads`. It is often used to limit data in development:

```sql
{% if target.name == 'dev' %} where created_at >= dateadd(day, -3, current_date) {% endif %}
```

<!-- challenge -->

A model has 12 nearly identical `case when` lines, one per country, and a new country means editing SQL. How do you make it data-driven?

<!-- solution -->

Read the list of countries from a variable, seed or `run_query` and loop over it with `{% for %}` to generate the columns. New countries then only change the list.

<!-- takeaways -->

- Jinja adds loops, conditions and variables to SQL.
- `target` adapts code to the environment.
- Whitespace control keeps compiled SQL readable.

<!-- unit: Writing macros -->

<!-- goals -->

- Write macros with arguments, defaults and return values.
- Run macros as operations, debug them with `log()` and know when a UDF fits better.

<!-- concept -->

Macros are functions for SQL: logic you write once and call from many models. They take arguments with defaults, can read a model's config, and can return values instead of text when another macro needs data rather than SQL.

Some macros never run during a build. Run-operations call them directly for admin tasks like granting permissions or cleaning up old schemas, and logging helps trace what they do. When logic should also be callable outside dbt, a user-defined function that dbt creates in the warehouse is the better tool.

<!-- example -->

```sql
-- macros/cents_to_currency.sql
{% macro cents_to_currency(column, scale=2) %}
    round({{ column }} / 100.0, {{ scale }})
{% endmacro %}

-- usage in a model
select order_id, {{ cents_to_currency('amount_cents') }} as amount from {{ ref('stg_shop__payments') }}
```

#### What are macros in dbt and how can you run them?

Reusable pieces of Jinja (often generating SQL) defined with `{% macro name(args) %}...{% endmacro %}` in the `macros/` folder. They are called inside models, tests or hooks with `{{ name(args) }}`, or executed directly with `dbt run-operation name --args '{...}'`.

#### How do you write a macro with a default argument?

```sql
{% macro cents_to_euros(column, scale=2) %}
    round({{ column }} / 100.0, {{ scale }})
{% endmacro %}
```

Called as `{{ cents_to_euros('amount') }}`.

#### What does `return()` do in a macro?

It returns a Python object (list, dict, number) instead of rendered text, so another macro can use the value.

#### What is `log()` used for in macros?

To print messages to the console or log file during compilation, for debugging: `{{ log("value: " ~ my_var, info=true) }}`.

#### What is the `config` object in Jinja?

It reads a model's configuration inside macros and materializations: `config.get('unique_key')` returns a value or a default, and `config.require('unique_key')` fails if it's missing. Custom keys stored under `meta` are read with `config.meta_get('owner')` or `config.meta_require('owner')`, not with `config.get`.

#### What is `dbt run-operation` used for?

Running a macro outside the build, for administration tasks: granting permissions, dropping old schemas, loading data, or generating code with the `codegen` package.

#### When should you use a user-defined function (UDF) instead of a macro?

A macro generates SQL text at compile time and only exists inside dbt. A UDF, defined as a SQL or Python file in `functions/` and called with `{{ function('name') }}`, is created as a real function in the warehouse before the models that use it, so BI tools and notebooks can call it too. Use a UDF for reusable row-level logic that should be shared outside dbt; use a macro to generate SQL, adapt it per platform or produce DDL. UDFs need dbt v1.11+ or v2 on platforms such as Snowflake, BigQuery, Databricks and Redshift.

<!-- challenge -->

Every month someone manually drops development schemas older than 30 days. How do you automate it with dbt?

<!-- solution -->

Write a macro that queries the information schema for dev schemas, filters by age or naming pattern, and drops them, then schedule `dbt run-operation drop_old_dev_schemas` in the orchestrator.

<!-- takeaways -->

- Macros are reusable SQL-generating functions.
- `return()` passes data between macros.
- `run-operation` runs macros outside builds.

<!-- unit: Compile-time introspection -->

<!-- goals -->

- Query the warehouse and the project graph during compilation.
- Write adapter-specific macros and override built-ins.

<!-- concept -->

Some SQL can't be written until you know something: the distinct values in a column, the columns of a table, the platform you're on. dbt can query the warehouse while compiling and read its own project graph, but only when it's actually executing, not while parsing the project.

Dispatch picks a macro implementation per platform, which is how packages work everywhere, and any built-in macro can be overridden by defining one with the same name.

<!-- example -->

```sql
{% set statuses_query %}select distinct status from {{ ref('stg_shop__orders') }}{% endset %}
{% if execute %}
  {% set statuses = run_query(statuses_query).columns[0].values() %}
{% else %}
  {% set statuses = [] %}
{% endif %}
```

#### What does `run_query` do?

It executes a query during compilation and returns the result as an agate table, for example to build a list of distinct values used in a loop. It only returns data at execution time, so it is usually guarded with `{% if execute %}`.

#### What is the `execute` variable?

A boolean that is false while dbt parses the project and true when it compiles or runs nodes. Code that depends on query results must be wrapped in `{% if execute %}`, because during parsing queries return nothing and referenced relations may not exist yet.

#### What are `graph` and `model` context variables?

`graph` exposes the parsed project (all nodes and their metadata), and `model` the current node, which macros can inspect, for example to generate documentation or audits.

#### What is `adapter.dispatch`?

A mechanism to implement a macro differently per database, so packages work across adapters: dbt picks `snowflake__my_macro`, `bigquery__my_macro` or `default__my_macro` depending on the adapter.

#### How do you override a built-in dbt macro?

Define a macro with the same name in your project, for example `generate_schema_name` or `generate_alias_name`. The project's version takes precedence over the one shipped with dbt.

<!-- challenge -->

A model using `run_query` fails during `dbt parse` with an error about a missing relation. Why, and what is the fix?

<!-- solution -->

The Jinja is rendered during parsing too, when relations may not exist and query results aren't available. Wrap the `run_query` in `{% if execute %}` and provide a default otherwise.

<!-- takeaways -->

- `run_query` reads the warehouse at compile time.
- Guard queries with `execute`.
- Dispatch and overrides adapt macros per platform.

<!-- unit: Packages and restraint -->

<!-- goals -->

- Use helper macros like `codegen` and `dbt_utils.star`.
- Avoid over-engineering with Jinja.

<!-- concept -->

Ready-made macros remove a lot of typing: generating source YAML and staging models, listing columns except a few. They're worth knowing before writing your own.

The opposite risk is real too. Heavily templated SQL is hard to read, review and debug, since the code you see isn't the code that runs. Plain SQL first, a macro only when logic truly repeats or must vary by platform, keeps a project maintainable.

<!-- example -->

```bash
dbt run-operation generate_source --args '{"schema_name": "shop", "generate_columns": true}'
```
```sql
select {{ dbt_utils.star(from=ref('stg_shop__customers'), except=['_loaded_at', 'raw_payload']) }}
from {{ ref('stg_shop__customers') }}
```

#### What is the `codegen` package?

A package with macros that generate boilerplate YAML and SQL, such as source definitions from a schema or a staging model from a source table.

#### What is the `star` macro from dbt_utils?

`{{ dbt_utils.star(ref('model'), except=['col']) }}` generates the list of a relation's columns, minus some, to avoid `select *` while not typing every column.

#### How do you avoid over-engineering with Jinja?

Write plain SQL first, extract a macro only when logic repeats or must vary by adapter, document macro arguments, and check the compiled SQL is readable.

<!-- challenge -->

A teammate built a macro that generates entire models from YAML metadata, and nobody else can debug them. What do you suggest?

<!-- solution -->

Keep generation for truly repetitive, mechanical models (if at all), and write business logic as plain SQL models. Document any remaining generator and make compiled SQL easy to inspect.

<!-- takeaways -->

- `codegen` writes boilerplate; `star` lists columns.
- Prefer plain SQL; macro only repeated logic.
- Readable compiled SQL matters for debugging.

<!-- stage: Quality and history -->

### Testing and data quality

<!-- unit: Data tests -->

<!-- goals -->

- Use generic, singular and custom generic data tests.
- Test uniqueness across column combinations.

<!-- concept -->

A data test is a query that returns rows breaking a rule; no rows means pass. Generic tests are reusable rules applied in YAML, such as uniqueness or accepted values. Singular tests are one-off SQL files for rules too specific to reuse. When a rule appears in several places, a custom generic test turns it into a reusable one.

Because tests run on real data in the warehouse, they catch problems in sources as well as in code.

<!-- example -->

```yaml
models:
  - name: fct_order_lines
    data_tests:
      - dbt_utils.unique_combination_of_columns:
          arguments:
            combination_of_columns: [order_id, line_number]
    columns:
      - name: status
        data_tests:
          - accepted_values:
              arguments: {values: [placed, shipped, returned]}
      - name: customer_id
        data_tests:
          - relationships:
              arguments: {to: ref('dim_customer'), field: customer_id}
```

#### What are the two types of tests in dbt?

**Data tests** check the data in the warehouse: generic tests (reusable, parameterized, declared in YAML) and singular tests (one-off SQL queries in `tests/`). **Unit tests**, added in dbt 1.8, check a model's SQL logic against small mocked inputs before it runs on real data.

#### What types of tests can you run in dbt?

The four built-in generic tests (`unique`, `not_null`, `accepted_values`, `relationships`), generic tests from packages (`dbt_utils`, `dbt_expectations`) or your own, singular SQL tests and unit tests. Related safeguards are source and model freshness, model contracts and, in dbt v2, checks on project metadata.

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
              arguments:
                values: ['placed', 'shipped', 'returned']
      - name: customer_id
        data_tests:
          - relationships:
              arguments:
                to: ref('dim_customers')
                field: customer_id
```

dbt turns each into a query that returns failing rows. The test passes when the query returns no rows. Test inputs go under `arguments:` and options such as `severity` under `config:`; older projects put the inputs directly under the test name, which is deprecated since dbt v1.10.

#### What is a singular test?

A `.sql` file in `tests/` that selects rows violating a rule. It fails if it returns any row:

```sql
-- tests/assert_no_negative_amounts.sql
select * from {{ ref('fct_orders') }} where amount < 0
```

#### How do you write a custom generic test?

With a `{% test name(model, column_name) %}` block, usually in `tests/generic/` or `macros/`, that returns failing rows. Extra parameters become arguments in YAML, where you use the test like a built-in one:

```sql
{% test is_positive(model, column_name) %}
select * from {{ model }} where {{ column_name }} <= 0
{% endtest %}
```

#### How do you test that a combination of columns is unique?

With `dbt_utils.unique_combination_of_columns`:

```yaml
data_tests:
  - dbt_utils.unique_combination_of_columns:
      arguments:
        combination_of_columns: [order_id, line_number]
```

<!-- challenge -->

Several models need the rule "amount must be non-negative unless the row is a refund". How do you avoid copying a singular test five times?

<!-- solution -->

Write a custom generic test (for example `non_negative_unless_refund(model, column_name)`) that returns violating rows, and apply it in YAML to each model's amount column.

<!-- takeaways -->

- Data tests return the rows that break a rule.
- Generic tests are reusable; singular tests are specific.
- Repeated rules become custom generic tests.

<!-- unit: Unit tests and test packages -->

<!-- goals -->

- Write unit tests and distinguish them from data tests.
- Use package tests for ranges, recency and row counts.

<!-- concept -->

Data tests check the data that happens to exist; unit tests check the logic against inputs you choose. A unit test gives fixed rows for a model's parents and the expected output, so edge cases like refunds or nulls are tested before the model ever runs on real data.

Packages extend data tests with common checks: values in a range, recent data, matching row counts between models. They cover most needs without custom SQL.

<!-- example -->

```yaml
unit_tests:
  - name: refunds_reduce_net_amount
    model: fct_order_lines
    given:
      - input: ref('int_order_lines_enriched')
        rows:
          - {order_id: 1, line_number: 1, type: sale,   amount: 100}
          - {order_id: 1, line_number: 2, type: refund, amount: 30}
    expect:
      rows:
        - {order_id: 1, line_number: 1, net_amount: 100}
        - {order_id: 1, line_number: 2, net_amount: -30}
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

Rows can be written as `dict` (the default), `csv` or `sql`, inline or in fixture files, and only the columns relevant to the test need values. `overrides` can fix macros and vars, for example `is_incremental: true` to test the incremental branch.

#### What is the difference between a unit test and a data test?

A unit test checks code against fixed inputs and runs before the model is built. Because its inputs never change, dbt Labs recommends running unit tests only in development and CI, and excluding them from production jobs. A data test checks real data after the model is built, on every run. Unit tests currently support SQL models only, and every `ref` or `source` the model uses must be given as an input.

#### What is `dbt_expectations`?

A package of generic tests inspired by Great Expectations: value ranges, regular expressions, row counts, distributions, column types and more.

#### How do you test a model's row count against another?

With a package test such as `dbt_utils.equal_rowcount` or `dbt_expectations.expect_table_row_count_to_equal_other_table`, or a singular test comparing counts.

#### How can you check that a value falls within a range?

With `dbt_utils.accepted_range` (`min_value`, `max_value`) or `dbt_expectations.expect_column_values_to_be_between`.

#### What is a recency test?

A test such as `dbt_utils.recency` that fails when the most recent timestamp in a model is older than a threshold, detecting models that stopped receiving data.

<!-- challenge -->

A complex discount calculation passes all data tests, but a rare combination of coupons is computed wrong in production. Which test type would have caught it?

<!-- solution -->

A unit test with mock input rows covering that coupon combination and the expected discount. Data tests only see combinations present in the data at test time.

<!-- takeaways -->

- Unit tests check logic on chosen inputs.
- Data tests check real data.
- Packages add range, recency and row-count tests.

<!-- unit: Configuring tests -->

<!-- goals -->

- Set severity, thresholds and filters on tests.
- Store failures and avoid alert fatigue.

<!-- concept -->

Not every failed test means the same thing. Severity and thresholds separate "stop everything" from "worth a look": a handful of bad rows might warn while a thousand errors. A `where` filter limits a test to recent data, which keeps it fast and relevant.

Storing failures turns a red test into something you can investigate. Without these settings, teams drown in alerts and start ignoring them, which is worse than having fewer tests.

<!-- example -->

```yaml
columns:
  - name: email
    data_tests:
      - not_null:
          config:
            severity: error
            warn_if: ">0"
            error_if: ">100"
            where: "created_at >= current_date - 7"
            store_failures: true
```

#### What is test severity?

A config setting `severity: warn` or `error` (default). With `warn_if` and `error_if` thresholds such as `">10"`, a test can warn on a few failures and only fail beyond a limit.

#### How do you store test failures?

With `--store-failures` or `store_failures: true`, dbt saves the failing rows of each test in a table in an audit schema (by default the target schema with the suffix `_dbt_test__audit`), so you can inspect them after the run. `store_failures_as` chooses `table`, `view` or `ephemeral` (don't store).

#### What does the `where` config on a test do?

It limits the test to a subset of rows, for example only recent data: `config: {where: "order_date >= current_date - 7"}`.

#### How do you avoid alert fatigue with dbt tests?

Use `warn` severity and thresholds for non-critical checks, test what matters to consumers, remove tests that never catch anything meaningful, and route errors to owners.

<!-- challenge -->

A team gets 40 test warnings every morning and has stopped reading them. What do you do?

<!-- solution -->

Review each test: fix real issues, delete tests that don't protect consumers, set thresholds so warnings mean something, make critical tests errors that block, and route alerts to owners.

<!-- takeaways -->

- Severity and thresholds grade failures.
- `where` keeps tests focused and fast.
- Fewer, meaningful alerts beat many ignored ones.

<!-- unit: A testing strategy -->

<!-- goals -->

- Define the minimum tests every model needs.
- Test at the source, use `dbt build` to stop bad data and enforce project standards with checks.

<!-- concept -->

A good strategy puts tests where they protect most. At the entrance, tests on sources and staging catch raw data problems before they spread. On every model, primary keys are unique and not null, and important foreign keys exist. On public models, contracts protect consumers.

`dbt build` ties it together: each model is tested right after it's built, and children of a failing model are skipped. In dbt v2, checks add a layer above the data, enforcing standards such as descriptions and owners before anything runs.

<!-- example -->

| Layer | Minimum |
|---|---|
| Sources | Freshness, key not null, unique where expected |
| Staging | Primary key unique + not null |
| Marts | Grain uniqueness, relationships, accepted values, contracts |

#### What should you test at minimum on every model?

The primary key with `unique` and `not_null`, foreign keys with `relationships` on important joins, and categorical columns with `accepted_values`. Add business rules where errors would be costly.

#### What does "testing at the source" mean?

Putting tests on sources and staging models, so problems in raw data are caught at the entrance rather than discovered in a dashboard.

#### How does dbt ensure data quality across the pipeline?

Through tests at each layer, source freshness, contracts on public models, `dbt build` skipping downstream models when a test fails, and CI that runs modified models and their tests before merging.

#### What is the difference between `dbt test` and `dbt build` regarding tests?

`dbt test` runs tests on already-built models. `dbt build` interleaves building and testing in DAG order, so a failing test stops its children from being built.

#### What are checks in dbt v2?

Rules about the project itself rather than the data: every model has a description, every public model has an owner, names follow conventions. A check is a SQL file in `checks/`, written in DuckDB SQL against the dbt Information Schema (`{{ info_schema('models') }}`), and it fails when it returns rows, like a data test. Checks run locally without a warehouse connection, on demand with `dbt check` and automatically at the start of every `dbt build`.

```sql
-- checks/all_models_have_descriptions.sql
select unique_id from {{ info_schema('models') }} where description = ''
```

<!-- challenge -->

Duplicates from a source reached three marts before anyone noticed. Where should the first test have been?

<!-- solution -->

On the source or its staging model: a uniqueness test on the source key would fail at the entrance, and with `dbt build` the marts would be skipped instead of rebuilt on duplicates.

<!-- takeaways -->

- Test keys on every model.
- Catch raw problems at sources and staging.
- `dbt build` stops bad data from propagating.

### Incremental models

<!-- unit: How incremental models work -->

<!-- goals -->

- Build incremental models with `is_incremental()` and `unique_key`.
- Know when to use them and how they read their own table.

<!-- concept -->

Rebuilding a billion-row table every run wastes time and money when only today's rows are new. An incremental model builds the full table once, then on later runs processes only new or changed rows and adds them to the existing table.

The model decides what's new by filtering inside an `is_incremental()` block, usually against the maximum timestamp already in `{{ this }}`. A `unique_key` turns inserts into upserts.

<!-- example -->

```sql
{{ config(materialized='incremental', unique_key='event_id') }}
select event_id, user_id, event_type, occurred_at
from {{ ref('stg_app__events') }}
{% if is_incremental() %}
where occurred_at > (select max(occurred_at) from {{ this }})
{% endif %}
```

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

True only when the model is materialized as incremental, the target table already exists, and the run is not a full refresh. The model's SQL must be valid whether it returns true or false.

#### What is `unique_key` in an incremental model?

The column (or list of columns) identifying a row. With it, rows that already exist are updated instead of duplicated, depending on the strategy.

#### How does dbt handle incremental loading of data from source systems?

dbt doesn't extract from source systems: it processes data already loaded into the warehouse. Incremental models select only rows newer than the latest already processed (using a timestamp or ID), and merge or append them. Loaders like Fivetran or Airbyte bring the data in incrementally, and dbt transforms it incrementally.

#### Can an incremental model reference itself?

Yes, through `{{ this }}` inside the `is_incremental()` block, typically to read the current maximum timestamp.

#### What is an "append-only" incremental model?

One using the `append` strategy, or a model without `unique_key`: new rows are inserted and existing rows are never updated. It suits immutable event logs where records never change, and it's the cheapest strategy, but a rerun over the same rows creates duplicates.

<!-- challenge -->

An incremental model has no `unique_key`, and the source sometimes resends updated orders. What happens, and what do you change?

<!-- solution -->

Updated orders are appended again, creating duplicates. Add `unique_key='order_id'` (with a merge or delete+insert strategy) so existing rows are updated instead.

<!-- takeaways -->

- Incremental models process only new rows after the first build.
- `is_incremental()` guards the filter.
- `unique_key` turns appends into upserts.

<!-- unit: Incremental strategies -->

<!-- goals -->

- Choose between append, merge, delete+insert, insert_overwrite and microbatch.
- Speed up merges with predicates and partitioning.

<!-- concept -->

How new rows are combined with the table is the strategy. Append just inserts. Merge upserts on the key. Delete+insert removes matching rows first, sometimes faster on large batches. Insert_overwrite replaces whole partitions on platforms such as BigQuery and Databricks, which is very efficient when data arrives by day. Microbatch splits work into independent time batches that can be retried and backfilled one by one, with no filter to write.

Large targets need help: predicates and partitioning limit how much of the existing table each merge scans.

<!-- example -->

```sql
{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='order_id',
    incremental_predicates=["DBT_INTERNAL_DEST.ordered_at >= dateadd(day, -7, current_date)"],
    cluster_by=['ordered_at']
) }}
```

#### What incremental strategies exist?

Depending on the adapter: `append` (insert only), `merge` (upsert on `unique_key`), `delete+insert` (delete matching keys then insert), `insert_overwrite` (replace whole partitions on BigQuery, Spark, Databricks and Athena) and `microbatch` (process time-based batches). Some adapters add their own, such as `replace_where` on Databricks. BigQuery doesn't support `append` or `delete+insert`.

#### What is the difference between `merge` and `delete+insert`?

`merge` updates matching rows and inserts new ones in one statement. `delete+insert` deletes existing rows with the same keys and inserts the new batch. It is useful where merge is slow or unsupported.

#### What is `insert_overwrite`, and when is it efficient?

It replaces entire partitions (for example the days present in the new batch) instead of merging row by row. It is efficient on partitioned tables in BigQuery, Spark and Databricks when data arrives by partition. On Snowflake, which has no partitions, `insert_overwrite` replaces the whole table.

#### What does `incremental_predicates` do?

It adds extra conditions to the merge, for example limiting the target scan to recent partitions, which reduces cost on large tables.

#### What is the microbatch strategy?

Added in dbt 1.9, it processes data in independent time batches based on an `event_time` column. You don't write an `is_incremental()` filter: dbt filters each parent that also declares `event_time` to the batch's time range. `batch_size` sets the granularity (`hour`, `day`, `month` or `year`), `begin` the start date for the first or full build, and `lookback` how many earlier batches to reprocess for late data. Batches can be retried individually, run in parallel or backfilled with `--event-time-start` and `--event-time-end`.

```sql
{{ config(materialized='incremental', incremental_strategy='microbatch',
          event_time='occurred_at', begin='2024-01-01', batch_size='day', lookback=3) }}
select * from {{ ref('stg_app__events') }}   -- filtered per batch automatically
```

#### How does partitioning or clustering interact with incremental models?

Partitioning or clustering the target on the filter column (usually a date) makes both the incremental filter and the merge read less data, which is where most of the savings come from.

<!-- challenge -->

A daily-partitioned BigQuery table receives a full day of events each run. Merge is slow and expensive. Which strategy fits better?

<!-- solution -->

`insert_overwrite` with the table partitioned by date: each run replaces the affected day partitions instead of merging row by row, which is cheaper and naturally idempotent.

<!-- takeaways -->

- Strategies: append, merge, delete+insert, insert_overwrite, microbatch.
- Partition-level overwrite is efficient for daily data.
- Predicates and partitioning limit merge scans.

<!-- unit: Keeping incremental models correct -->

<!-- goals -->

- Handle late data, schema changes and full refreshes.
- Test and backfill incremental models.

<!-- concept -->

Incremental models trade simplicity for speed, and the trade shows in edge cases. A strict "newer than max" filter misses late rows; a lookback window reprocesses recent days to catch them. Column changes need a policy. Logic changes need a full refresh or a backfill, because existing rows were built with the old logic.

Testing matters more than for tables: duplicate keys are the classic bug, and comparing with a full rebuild occasionally proves the increments still add up.

<!-- example -->

```sql
{% if is_incremental() %}
-- 3-day lookback catches late events; unique_key de-duplicates the overlap
where occurred_at >= (select dateadd(day, -3, max(occurred_at)) from {{ this }})
{% endif %}
```

#### How do you handle late-arriving data in incremental models?

Use a lookback window rather than a strict "greater than max": reprocess the last few days, and rely on `unique_key` with `merge` to update rows already loaded.

```sql
{% if is_incremental() %}
where event_time >= (select dateadd(day, -3, max(event_time)) from {{ this }})
{% endif %}
```

#### What does `on_schema_change` do?

It defines what happens when an incremental model's columns change: `ignore` (default: new columns are not added), `fail`, `append_new_columns` (add new columns, keep removed ones) or `sync_all_columns` (add new columns, drop removed ones, including type changes). None of them backfills values for old rows in new columns; that needs a full refresh. Only top-level columns are tracked, not nested fields.

#### When should you do a full refresh of an incremental model?

When the logic changes in a way that affects historical rows, when columns change in ways `on_schema_change` doesn't handle, or to repair data. Some tables are protected with `full_refresh: false` because rebuilding them is too costly.

#### What are the risks of incremental models?

Duplicates if `unique_key` is missing or wrong, missed rows if the filter misses late data, divergence from a full rebuild if logic changes, and complexity for testing. A periodic full refresh in a lower environment helps detect drift.

#### How do you test an incremental model properly?

Test the primary key for uniqueness (duplicates are the usual bug), compare with a full refresh in a lower environment, and write unit tests that override `is_incremental` to true and false.

#### How do you backfill an incremental model?

With `--full-refresh`, or for microbatch models with `--event-time-start` and `--event-time-end` to reprocess a period, or by running with a var that changes the filter window.

<!-- challenge -->

You change how `net_amount` is calculated in an incremental model. New rows are right, but last year's rows still use the old formula. What do you do?

<!-- solution -->

Rebuild history: run with `--full-refresh` (or a microbatch backfill over the affected range). Incremental runs never revisit old rows, so logic changes require reprocessing them.

<!-- takeaways -->

- Use lookback windows for late data.
- Logic changes need full refreshes or backfills.
- Test keys for duplicates; compare with full rebuilds.

<!-- unit: Incremental models over time -->

<!-- goals -->

- Explain why incremental models slow down and how to fix it.
- Choose between incremental models and snapshots.

<!-- concept -->

An incremental model that was fast at launch can become slow a year later, because each merge scans an ever-growing target. Limiting the scan with predicates, partitioning or clustering keeps cost proportional to new data.

Incremental models and snapshots both "add over time" but answer different questions. Incremental models keep the latest state or the stream of events using your logic; snapshots record how mutable source rows changed.

<!-- example -->

| Need | Use |
|---|---|
| Append click events efficiently | Incremental (append) |
| Keep current orders, updated in place | Incremental (merge) |
| History of each customer's plan changes | Snapshot |

#### Why might an incremental model become slower over time?

The merge has to scan an ever-growing target table. Incremental predicates, partition pruning, clustering, or the `insert_overwrite` and `microbatch` strategies keep each run bounded.

#### What is the difference between an incremental model and a snapshot?

An incremental model keeps the latest state (or appends events) and its logic is yours. A snapshot keeps the full history of changes to mutable records, as SCD Type 2 rows with validity dates. They combine well: an incremental staging model keeps runs cheap, and a snapshot on the source records history when the business needs to know what a row looked like in the past.

<!-- challenge -->

A merge-based incremental model's runtime grew from 2 to 25 minutes in a year, though daily volume is stable. What do you do?

<!-- solution -->

Limit the target scan: add `incremental_predicates` on a recent date range and partition or cluster the table on that date, so the merge only touches recent data.

<!-- takeaways -->

- Unbounded merges slow down as tables grow.
- Predicates and clustering keep merges cheap.
- Incremental keeps state; snapshots keep history.

### Snapshots

<!-- unit: Capturing history with snapshots -->

<!-- goals -->

- Define snapshots with timestamp or check strategies.
- Explain the columns dbt adds and how snapshots implement SCD2.

<!-- concept -->

Source tables often overwrite rows: a customer's plan changes, and the old value is gone. Snapshots record those changes. Each run compares the source with the latest recorded version and, when something changed, closes the old version and inserts a new one, which is exactly a type 2 slowly changing dimension.

Detecting change is the strategy: a reliable updated-at column is cheapest; without one, comparing selected or all columns works at a higher cost.

<!-- example -->

```yaml
# snapshots/customers_snapshot.yml
snapshots:
  - name: customers_snapshot
    relation: source('crm', 'customers')
    config:
      unique_key: customer_id
      strategy: timestamp
      updated_at: updated_at
      hard_deletes: invalidate
```

#### What is a snapshot?

A dbt resource that records changes to a mutable table over time (Slowly Changing Dimension Type 2). Each run compares the current source rows with the snapshot table, closes changed rows by setting `dbt_valid_to`, and inserts their new version with `dbt_valid_from`.

#### How do you define a snapshot?

Since dbt 1.9, in a YAML file that names the relation to snapshot and its config (older projects use a `{% snapshot %}` block with a `select` in `snapshots/`, which still works but is the legacy form):

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

`timestamp` (recommended): a row changed if its `updated_at` column is newer. It is reliable and efficient when the source keeps such a column. `check`: a row changed if any of the listed `check_cols` (or all columns) differ. It is used when there is no trustworthy timestamp.

#### Which columns does dbt add to a snapshot?

`dbt_scd_id` (a unique key per version), `dbt_updated_at`, `dbt_valid_from` and `dbt_valid_to` (NULL for the current version, unless `dbt_valid_to_current` sets a value such as `9999-12-31`). With `hard_deletes: new_record`, dbt also adds `dbt_is_deleted`. The names can be changed with `snapshot_meta_column_names`.

#### When would you use the `check` strategy with `check_cols: all`?

When the source has no reliable `updated_at` and any column change matters. It is more expensive because every column is compared, and new source columns change what counts as a change. The docs recommend listing the columns that matter explicitly, or comparing a single hash column built from them.

#### What is an SCD Type 2, and how do dbt snapshots implement it?

A slowly changing dimension that keeps a new row for each version of a record, with validity dates. dbt snapshots are exactly that: one row per version, `dbt_valid_from` and `dbt_valid_to` bounding its validity.

<!-- challenge -->

A source table has no `updated_at` column, but changes to `plan` and `status` matter. How do you configure the snapshot?

<!-- solution -->

Use the `check` strategy with `check_cols: ['plan', 'status']`, so dbt compares those columns each run and records a new version when they change.

<!-- takeaways -->

- Snapshots record changes to mutable rows (SCD2).
- Timestamp strategy is cheapest; check works without timestamps.
- dbt adds validity and ID columns.

<!-- unit: Running snapshots safely -->

<!-- goals -->

- Handle deletes, key problems and run frequency.
- Explain why snapshots can't be rebuilt and how they differ from time travel.

<!-- concept -->

Snapshots are the one part of a dbt project that can't be regenerated: if a change wasn't captured, it's gone. That shapes every rule about them. Read raw sources so history reflects reality, not your current logic. Run often enough to catch changes that revert. Make sure the key is unique, or versions get scrambled.

Deletes need explicit handling, and warehouse time travel is no substitute, since its retention is short and it's meant for recovery, not history.

<!-- example -->

| Rule | Why |
|---|---|
| Snapshot sources, not marts | Logic changes would rewrite history |
| Test the source key's uniqueness | Duplicates corrupt versions |
| Run at least as often as changes matter | Missed changes are lost |
| Never drop the snapshot table | Full refresh doesn't apply; history can't be rebuilt |

#### How do snapshots handle deleted source rows?

By default (`hard_deletes: ignore`) they don't: the last version of a deleted row stays current. With `hard_deletes: invalidate` (formerly `invalidate_hard_deletes: true`), deleted rows get their `dbt_valid_to` set. With `hard_deletes: new_record`, dbt inserts a new row with `dbt_is_deleted = True`, and a row that reappears gets a new version with `dbt_is_deleted = False`.

#### Why should snapshots read from sources rather than transformed models?

Snapshots capture history that can't be recreated later. Snapshotting raw data with minimal logic means a bug in transformation code doesn't corrupt the history, and transformations can be re-run on top of it.

#### How often should snapshots run?

As often as changes need to be captured: changes that happen and revert between two runs are lost. Many teams run them hourly or daily, before the models that use them.

#### What happens if the `unique_key` isn't unique in the source?

The snapshot produces duplicate or inconsistent versions. Test uniqueness on the source and deduplicate upstream if needed.

#### Can you full-refresh a snapshot?

No. Snapshots ignore both the `--full-refresh` flag and the `full_refresh` config: a `dbt build --full-refresh` runs them as normal, because dropping the table would lose history that can't be recreated. To change one, you migrate the table manually or start a new snapshot.

#### How are snapshots different from Delta Lake time travel or warehouse time travel?

Warehouse time travel keeps past table versions for a limited retention period and is meant for recovery. Snapshots build a permanent, queryable history table at row level, designed for analysis.

<!-- challenge -->

A snapshot runs daily, but customers sometimes change plan and change back within hours. The business wants to see those changes. What do you change?

<!-- solution -->

Run the snapshot more often (for example hourly), or capture changes upstream with CDC. A daily snapshot only sees the state at run time, so short-lived changes are missed.

<!-- takeaways -->

- Snapshots can't be rebuilt; protect them.
- Snapshot raw sources with unique keys.
- Handle deletes explicitly; time travel isn't history.

<!-- unit: Querying snapshots -->

<!-- goals -->

- Query current and point-in-time versions from a snapshot.
- Build a historized dimension on top of a snapshot.

<!-- concept -->

A snapshot is raw history, and like other raw data it's best consumed through a model. Current versions are the rows whose validity hasn't ended; a point-in-time view picks the version whose range contains a date.

A dimension model on top renames the validity columns, adds a current flag and a surrogate key, and gives facts something clean to join to.

<!-- example -->

```sql
-- models/marts/dim_customer.sql
select
    {{ dbt_utils.generate_surrogate_key(['customer_id', 'dbt_valid_from']) }} as customer_key,
    customer_id, plan, status,
    dbt_valid_from as valid_from,
    coalesce(dbt_valid_to, '9999-12-31'::timestamp) as valid_to,
    dbt_valid_to is null as is_current
from {{ ref('customers_snapshot') }}
```

#### How do you query the current version of each record in a snapshot?

`where dbt_valid_to is null` (or the configured current value).

#### How do you get the state of a record at a given date?

```sql
select * from {{ ref('customers_snapshot') }}
where '2026-06-30' >= dbt_valid_from
  and ('2026-06-30' < dbt_valid_to or dbt_valid_to is null)
```

#### How do you build a dimension with history from a snapshot?

Select from the snapshot in a model, rename `dbt_valid_from` and `dbt_valid_to` to friendlier names, add a surrogate key per version and an `is_current` flag, and join facts on the natural key and the fact's date within the validity range.

<!-- challenge -->

Finance asks for each customer's plan as of 30 June. Write the filter.

<!-- solution -->

`where '2026-06-30' >= dbt_valid_from and ('2026-06-30' < dbt_valid_to or dbt_valid_to is null)` on the snapshot (or the equivalent on `valid_from`/`valid_to` in the dimension).

<!-- takeaways -->

- Current rows have no end of validity.
- Point-in-time queries filter by validity range.
- Build dimensions on top of snapshots.

<!-- stage: Production -->

### Documentation, lineage and the semantic layer

<!-- unit: Documenting projects -->

<!-- goals -->

- Write descriptions and generate the documentation site.
- Use persist_docs, meta fields and exposures.

<!-- concept -->

dbt documentation lives next to the code: descriptions in YAML for models and columns, longer text in doc blocks. Generating the docs site combines them with the DAG and tests, so readers see what a table means and where it comes from.

Documentation reaches further when it leaves dbt: persisting descriptions into the warehouse shows them in BI tools, meta fields record owners and sensitivity, and exposures declare which dashboards depend on which models.

<!-- example -->

```yaml
exposures:
  - name: revenue_dashboard
    type: dashboard
    owner: {name: Finance Data, email: finance-data@example.com}
    depends_on: [ref('fct_revenue'), ref('dim_customer')]
models:
  - name: fct_revenue
    description: "One row per invoice line. Net of refunds and discounts, in EUR."
    config:
      meta: {owner: finance-data, contains_pii: false}
      persist_docs: {relation: true, columns: true}
```

#### How does dbt generate documentation?

`dbt docs generate` builds a static site from the project (descriptions, columns, tests, SQL) and from warehouse metadata (column types, row counts), and `dbt docs serve` serves it locally, with an interactive lineage graph. In dbt v2, docs v2 stores the metadata as Parquet files that the browser queries with DuckDB-WASM, so the site scales to large projects, can be hosted on any static host and shows column-level lineage when built with `--static-analysis strict`. On the dbt platform, jobs keep Catalog up to date instead.

#### Where do you write descriptions?

In YAML properties files next to models (`description:` on models and columns), or in `{% docs %}` blocks in `.md` files referenced with `{{ doc('name') }}` for longer text.

#### What is `persist_docs`?

A config that writes model and column descriptions into the warehouse as table and column comments, so they are visible in other tools.

#### How do you document a test or a macro?

Macros are documented in YAML under a `macros:` key, with a description and their arguments. Data tests accept a `description` where they're applied, and singular tests can be documented in a properties file under `data_tests:`. These descriptions appear in the generated docs.

#### What are meta fields?

A free-form `meta` dictionary, set under `config:` on nodes and columns, for example to record owners, PII flags or SLAs. External tools read it from the manifest, and macros read it with `config.meta_get()`.

#### What are exposures?

YAML declarations of downstream uses of dbt models (dashboards, ML models, applications) with owners, so lineage shows what depends on each model.

<!-- challenge -->

Before changing `fct_revenue`, an engineer wants to know which dashboards will be affected. How does the project answer that?

<!-- solution -->

With exposures declared for the dashboards: the DAG shows which exposures depend on `fct_revenue`, with their owners, and `dbt ls --select fct_revenue+` lists them.

<!-- takeaways -->

- Descriptions live in YAML next to models.
- `persist_docs` pushes them into the warehouse.
- Exposures link models to their consumers.

<!-- unit: Artifacts and lineage -->

<!-- goals -->

- Use dbt artifacts for lineage, monitoring and selection checks.
- Explain column-level lineage.

<!-- concept -->

Every dbt invocation writes artifacts: a manifest describing the whole project and run results with the outcome and timing of each node. Many tools are built on them: CI state comparison, observability dashboards, catalogs and lineage graphs.

Lineage at model level shows which tables depend on which; column-level lineage goes further, tracing each column back to its sources, which answers "what breaks if I drop this column?" precisely.

<!-- example -->

```bash
dbt ls --select state:modified+ --state prod-artifacts/    # check a selection before running
jq '.results[] | {node: .unique_id, s: .execution_time}' target/run_results.json | head
```

#### What does `dbt ls` do?

It lists the nodes matching a selection without running them, which is useful to check selectors.

#### What is the `manifest.json` artifact?

A JSON file in `target/` describing the whole project (nodes, configurations, dependencies). It is used for state comparison (`state:modified`), documentation and external tools.

#### What is `run_results.json`?

An artifact with the result, timing and status of each node in the last invocation, used for monitoring and `dbt retry`.

#### What are dbt artifacts used for in observability?

Tools parse `manifest.json` and `run_results.json` to track run duration, test failures and freshness over time, and the `dbt_artifacts` package loads them into the warehouse for analysis. dbt v2 can also write the dbt Information Schema (`--generate-info-schema`): versioned Parquet tables describing every resource, which checks and `dbt show --info` query directly.

#### What is column-level lineage?

Lineage that shows which upstream columns feed each column, not just which models depend on which, so you can see exactly what a column rename or removal affects. dbt Catalog on the dbt platform shows it, and dbt v2 computes it locally when you compile or build with `--static-analysis strict`.

<!-- challenge -->

You want a weekly report of the ten slowest models and the tests that failed most often. Where does the data come from?

<!-- solution -->

From `run_results.json` of each production run (execution time and status per node), joined with `manifest.json` for model metadata, loaded into a table and aggregated weekly.

<!-- takeaways -->

- `manifest.json` describes the project; `run_results.json` the run.
- Artifacts power CI, observability and catalogs.
- Column-level lineage traces each column's origins.

<!-- unit: The semantic layer -->

<!-- goals -->

- Describe semantic models, entities, dimensions and metric types.
- Explain why metrics belong in dbt rather than BI tools.

<!-- concept -->

When each BI tool defines "revenue" itself, numbers drift. The semantic layer defines metrics once in dbt, on top of models: a semantic model marks a model's columns as entities for joining and dimensions for slicing, simple metrics aggregate a column, and other metric types combine metrics into business definitions.

Tools then query the metric by name, and MetricFlow generates correct SQL with the right joins, grain and filters, so every consumer gets the same answer.

<!-- example -->

```yaml
models:
  - name: fct_orders
    semantic_model: {enabled: true}
    agg_time_dimension: ordered_at
    columns:
      - name: order_id
        entity: {type: primary, name: order}
      - name: customer_id
        entity: {type: foreign, name: customer}
      - name: ordered_at
        granularity: day
        dimension: {type: time}
    metrics:
      - name: revenue
        type: simple
        agg: sum
        expr: net_amount
```

#### What is the semantic layer architecture of dbt?

Semantic models are declared on top of dbt models, marking entities (join keys) and dimensions. Metrics are defined on top of them. MetricFlow turns a metric request (metrics, dimensions, filters, grain) into SQL for the warehouse, using the entities to find joins, and the dbt platform exposes it through APIs (JDBC, GraphQL, Python SDK) and integrations to BI tools and spreadsheets.

#### What is a semantic model?

Metadata attached to one dbt model that tells MetricFlow how to join and aggregate it. In the current spec (dbt v1.12+ and v2) it is enabled inside the model's YAML with `semantic_model:`, entities and dimensions are set on columns, and simple metrics are listed next to them. Older projects use a separate top-level `semantic_models:` block with `measures`, which are deprecated in favor of simple metrics.

#### What types of metrics exist in the semantic layer?

Simple (an aggregation of a column, such as `sum` or `count_distinct`), ratio (one metric divided by another), cumulative (running totals or windows), derived (an expression over other metrics) and conversion (the rate at which an entity moves from one event to another). Simple metrics live with their semantic model; the others are defined under a top-level `metrics:` key.

#### Why define metrics in dbt rather than in the BI tool?

So the definition lives once, in version control, with tests and review, and every tool returns the same number for "revenue" or "active users".

<!-- challenge -->

Marketing's BI tool and finance's spreadsheet show different "average order value". How would the semantic layer fix it?

<!-- solution -->

Define AOV once as a ratio metric (numerator `revenue`, denominator `orders`) in dbt, reviewed in Git, and have both tools query the metric through the semantic layer API instead of computing it themselves.

<!-- takeaways -->

- Semantic models declare entities and dimensions; simple metrics aggregate columns.
- Metrics are defined once, in version control.
- Every tool queries the same definitions.

### Deployment, environments, CI/CD and orchestration

<!-- unit: Environments, version control and CI -->

<!-- goals -->

- Manage dev, staging and production with one codebase.
- Run Slim CI with `state:modified`, deploy safely and explain what dbt State adds.

<!-- concept -->

dbt makes environments cheap: one codebase, several targets, each writing to its own schemas. Developers build into personal schemas, CI into a schema per pull request, production into production.

Slim CI compares the project with production artifacts and builds only modified models and their children, deferring to production for the rest. dbt State takes the same idea further, deciding per node and per run whether anything really needs rebuilding. For high-stakes changes, building a full new version alongside the old and swapping atomically gives blue-green deployment.

<!-- example -->

```bash
# CI for a pull request
dbt deps
dbt build --select state:modified+ --defer --state prod-artifacts/ --target ci
```

#### How would you manage dbt deployments across multiple environments (dev, staging, production)?

Use one codebase and several targets (or dbt platform environments) pointing to separate schemas or databases: each developer builds into a personal dev schema, CI builds into a temporary schema, and scheduled jobs build production. Environment differences come from `profiles.yml`, environment variables and `target.name`, never from code edits. Changes reach production only through pull requests and CI.

#### How do you handle version control on dbt when working with multiple team members?

Git with feature branches and pull requests, code review, CI that builds and tests modified models on every pull request, a style guide and linter (SQLFluff), clear model ownership, small focused changes, and a personal dev schema per developer so nobody overwrites anyone else's tables.

#### What is Slim CI?

Running only modified models and their dependents in CI, by comparing with production artifacts: `dbt build --select state:modified+ --defer --state prod-artifacts/`. Unchanged parents are read from production instead of rebuilt. CI jobs on the dbt platform do this automatically and build into a temporary schema per pull request.

#### What does `state:modified` select?

Nodes whose SQL, configuration or properties differ from the manifest given with `--state`. Combined with `+` it includes their children. Sub-selectors narrow it, such as `state:modified.body` or `state:modified.configs`, and `state:new` selects only nodes that don't exist in the comparison manifest.

#### What is dbt State?

A managed service from dbt Labs (it requires a dbt platform login and is billed by usage) that decides, node by node, whether a build is needed. It compares each node's logic and upstream data with earlier builds in every environment, then skips the node if nothing changed, clones an identical up-to-date object from another schema, or builds it normally while deferring unselected parents. It works with dbt v1, v2 and external orchestrators, ignores changes that don't affect logic such as comments and whitespace, and uses `lag_tolerance` to stop rebuilding a model more often than needed. `dbt state explain` shows why each node was skipped, cloned or built. It replaces the platform's earlier state-aware orchestration.

#### What is blue-green deployment with dbt?

Building production into a new schema or database, testing it, then swapping it in atomically (renaming schemas or swapping views), so consumers never see partially built data.

<!-- challenge -->

CI builds the whole 600-model project on every pull request and takes 50 minutes. What do you change?

<!-- solution -->

Switch to Slim CI: download the production manifest, build `state:modified+` with `--defer`, and use a per-PR schema. Typical PRs then build a handful of models in minutes.

<!-- takeaways -->

- One codebase, many targets and schemas.
- Slim CI builds only what changed.
- Blue-green swaps a fully tested build into place.

<!-- unit: Orchestrating dbt -->

<!-- goals -->

- Schedule self-hosted dbt with an orchestrator or use the dbt platform.
- Design a production job that runs after ingestion.

<!-- concept -->

dbt doesn't schedule itself. When you host dbt yourself, an orchestrator runs it, ideally as part of a larger pipeline: wait for ingestion, check freshness, build and test, then notify downstream. The dbt platform offers jobs and triggers built in, with APIs for orchestrators.

A typical production job follows the same steps everywhere, and running dbt in a container makes it reproducible wherever it runs.

<!-- example -->

```bash
# typical production job
dbt deps
dbt source freshness
dbt build --target prod
dbt docs generate
# then: upload artifacts, alert on failure, trigger downstream
```

#### Name three advantages of integrating dbt with Airflow.

1. dbt runs are orchestrated with the rest of the pipeline (wait for ingestion, then transform, then refresh dashboards or train models).
2. Retries, alerts, SLAs, backfills and scheduling come from Airflow.
3. With tools like Astronomer Cosmos, each dbt model becomes an Airflow task, giving fine-grained visibility and the ability to retry only failed models.

#### How do you schedule self-hosted dbt in production?

With an orchestrator (Airflow, Dagster, Prefect, cron, GitHub Actions, Databricks Lakeflow Jobs) that runs `dbt build` (or selected commands) in a container or virtual environment with production credentials.

#### What does a typical production job look like?

`dbt deps`, `dbt source freshness` (or `dbt freshness` in dbt v2), `dbt build` (seeds, snapshots, models and tests in order), then `dbt docs generate`, with alerts on failure and artifacts saved for the next CI comparison.

#### How do you deploy dbt on the dbt platform?

Create deployment environments with their credentials and dbt version (release track), then define jobs: deploy jobs with commands, a schedule or triggers and selected models; CI jobs that run on each pull request; and merge jobs that run after a pull request is merged. Use job chaining or the Administrative API to start dbt after ingestion.

#### How do you trigger dbt after ingestion finishes?

Through the orchestrator (a task dependency or sensor), dbt platform API triggers or job chaining, or the ingestion tool's integration (for example Fivetran triggering a dbt job).

#### How do you run dbt in a Docker container?

Use an image with dbt installed (with dbt v1, plus the adapter package; dbt v2 is a single binary that downloads its adapter driver on first run, so cache or bake it into the image), mount or copy the project, pass credentials via environment variables, and run commands such as `dbt build --target prod`.

<!-- challenge -->

dbt runs at 06:00 by cron, but ingestion sometimes finishes at 06:30, so marts are built on yesterday's data. What do you change?

<!-- solution -->

Trigger dbt from the orchestrator after ingestion completes (task dependency, sensor or API call), and keep source freshness as the first step so a late load fails loudly instead of building stale data.

<!-- takeaways -->

- An orchestrator or the dbt platform runs dbt.
- Start dbt when ingestion finishes, not at a fixed time.
- Production jobs: deps, freshness, build, docs.

<!-- unit: Security -->

<!-- goals -->

- Run dbt with least-privilege credentials.
- Apply grants as code.

<!-- concept -->

dbt adds no data access of its own: it runs SQL with whatever permissions its credentials have, inside the warehouse. Security therefore comes down to those credentials, a dedicated service user per environment with only the privileges it needs, and to keeping secrets out of the repository.

Grants can live with the models, so permissions are reviewed and applied on every build instead of being clicked by hand.

<!-- example -->

```yaml
models:
  shop:
    marts:
      +grants:
        select: ['reporting', 'analyst']
    staging:
      +grants:
        select: []          # no direct access for consumers
```

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

<!-- challenge -->

The production dbt job runs with a personal admin account. What do you change?

<!-- solution -->

Create a service user for production with privileges only on the needed databases and schemas, store its credentials in the orchestrator's secrets manager, and manage consumer access with `grants` in the project.

<!-- takeaways -->

- dbt has exactly the access of its credentials.
- Use least-privilege service users per environment.
- Declare grants as code with `grants`.

<!-- unit: Debugging, tooling and adoption -->

<!-- goals -->

- Debug models and understand how dbt compiles queries.
- Introduce dbt into existing pipelines and scale with dbt Mesh.

<!-- concept -->

Most dbt debugging starts with the compiled SQL: what dbt actually sent to the warehouse, which you can run directly. Logs, artifacts and the warehouse's query history fill in the rest. Linting with SQLFluff keeps the code consistent enough to read quickly.

Adopting dbt rarely starts from zero: existing tables become sources, existing transformations are rebuilt model by model and compared. At larger scale, several projects reference each other's public models through dbt Mesh.

<!-- example -->

```bash
dbt compile --select fct_orders && cat target/compiled/shop/models/marts/fct_orders.sql
dbt --debug run --select fct_orders        # verbose logs
sqlfluff lint models/marts/fct_orders.sql
```

#### How do you monitor and troubleshoot issues in dbt?

Check the console output and `logs/dbt.log`, read the compiled SQL in `target/compiled` and `target/run`, inspect `run_results.json` for failures and timings, store test failures, use `dbt retry` after fixing, and track run history and durations in the orchestrator or dbt platform. Alerts on job failures and source freshness catch problems early.

#### How can you debug your dbt models?

Run `dbt compile` and execute the compiled SQL directly in the warehouse, preview with `dbt show`, isolate CTEs step by step, use `{{ log() }}` in Jinja, run with `--debug` for full logs, and check upstream data with tests.

#### How does dbt compile queries?

dbt parses the project and builds the DAG, then for each node renders the Jinja: it resolves `ref`, `source`, `var`, `config` and macro calls into plain SQL for the current target. The compiled `SELECT` is written to `target/compiled/`. dbt v2 then adds static analysis, parsing that SQL into a logical plan to catch errors and track column lineage without querying the warehouse. At run time the materialization wraps the query in DDL/DML (`create table as`, `merge`) and sends it to the warehouse through the adapter.

#### What is SQLFluff, and what does `dbt lint` do?

SQLFluff is a SQL linter and formatter with a dbt templater, used in CI and pre-commit hooks to enforce a consistent SQL style. dbt v2 includes `dbt lint`, a much faster built-in linter that reads the same `.sqlfluff` configuration and rule codes and can fix violations with `--fix`. Results can differ slightly from SQLFluff's.

#### How would you implement dbt in an existing data pipeline?

Start by declaring the existing raw tables as sources, then reproduce current transformations as staging and mart models one domain at a time, comparing outputs with the legacy tables (for example with `audit_helper`). Add tests and documentation, run dbt from the existing orchestrator after ingestion, switch consumers to the new tables, and retire legacy scripts gradually.

#### What is dbt Mesh?

A pattern for large organizations where several dbt projects reference each other's public models with a cross-project `ref('project', 'model')`, with groups, contracts, versions and access controls, so domains own their projects independently. Cross-project references are a dbt platform Enterprise feature, and Catalog shows lineage across the projects.

<!-- challenge -->

A model returns wrong totals, and the Jinja makes it hard to see why. What is your first step?

<!-- solution -->

Compile it and run the compiled SQL directly in the warehouse, then query each CTE separately to find where the numbers diverge. Fix the logic, and add a unit test for the case.

<!-- takeaways -->

- Debug the compiled SQL, not the template.
- Adopt dbt by wrapping existing tables as sources.
- dbt Mesh connects several projects through public models.

### Performance, warehouses and troubleshooting

<!-- unit: Faster, cheaper runs -->

<!-- goals -->

- Speed up dbt projects with materializations, threads and incremental models.
- Find slow models and cut costs, including on Snowflake.

<!-- concept -->

A dbt project's runtime is the sum of its queries, so performance work is mostly warehouse work. Materialize what's queried often, make big facts incremental, avoid long chains of views that recompute everything, and run independent models in parallel with enough threads.

Measure before changing: run timings show the slowest models, and the cost model of views, tables and incremental models explains where the money goes. Development can be cheaper still by working on samples and deferring to production.

<!-- example -->

| Materialization | Build cost | Query cost |
|---|---|---|
| View | ~0 | Full query every read |
| Table | Full query every build | Cheap |
| Incremental | New data only | Cheap |

#### How can you optimize the performance of dbt transformations on large datasets?

Materialize expensive models as tables and use incremental models for large fact tables, filter and aggregate early, avoid `select *` and unnecessary joins, partition and cluster big tables on filter columns, use the warehouse's native features (clustering keys, sort keys), limit data in development, and look at query profiles and `run_results.json` timings to find the slowest models.

#### Which optimization techniques help when running dbt on Snowflake?

Use transient tables for intermediate models (no Fail-safe storage cost), cluster very large tables on common filter columns, size warehouses per job (and use separate warehouses for dbt and BI), use `merge` or `delete+insert` with incremental predicates, rely on zero-copy cloning for dev and CI (`dbt clone`), set `query_tag` to attribute costs, and auto-suspend warehouses.

#### How do you make dbt runs faster overall?

Increase `threads` within warehouse limits (dbt v2 tunes parallelism itself on most platforms), remove unnecessary models, convert rarely queried tables to views (or the reverse for heavy views), use incremental models, run only what changed (`state:modified+`) in CI, and split jobs by freshness needs.

#### How do you find the slowest models?

From `run_results.json` timings, the dbt platform's model timing view, or the warehouse query history filtered by the dbt `query_tag`.

#### What is the cost impact of views vs tables vs incremental models?

Views cost compute every time they are queried. Tables cost compute at each build plus storage. Incremental models cost little per run but need care to stay correct.

#### Why can a long chain of views be slow?

Each query on the final view executes the whole chain of underlying SQL. Materializing key intermediate models as tables stops repeated computation.

#### How do you limit data in development to save time and cost?

Filter by date with `target.name == 'dev'`, use `--defer` to reuse production parents, or use zero-copy clones. dbt also has two built-in flags for `run` and `build`: `--sample="3 days"` filters every `ref` and `source` that has an `event_time` to a recent time window, and `--empty` limits them to zero rows, which checks that the SQL runs and creates the right columns at almost no cost (useful in CI).

#### How would you compare dbt and BigQuery?

They aren't alternatives: BigQuery is a serverless data warehouse that stores and processes data, while dbt is a transformation framework that generates SQL and runs it in BigQuery (through dbt-bigquery). BigQuery's own scheduled queries or Dataform cover similar ground to dbt, but dbt adds portability across platforms, a large package ecosystem and a broad community. On BigQuery, dbt supports partitioning, clustering and `insert_overwrite`.

<!-- challenge -->

A nightly run takes 3 hours, but the warehouse shows long idle gaps between queries. What setting do you check first?

<!-- solution -->

`threads`: with too few, independent models wait in line. Raise threads within the warehouse's concurrency limits, then look at the critical path of the DAG for slow models.

<!-- takeaways -->

- Materialize hot models; make large facts incremental.
- Measure with run timings before optimizing.
- Develop on samples and defer to production.

<!-- unit: Correctness problems -->

<!-- goals -->

- Catch fan-out, duplicates and cycles in dbt models.
- Handle source schema changes.

<!-- concept -->

Some problems produce wrong numbers rather than errors. Joins on keys that aren't unique multiply rows; sources that resend records create duplicates; source columns that change break models or silently drop data. Uniqueness tests and explicit column lists catch most of them early.

Cycles are the one problem dbt refuses outright: if two models need each other, the shared logic belongs in a third model upstream of both.

<!-- example -->

```sql
-- staging: keep the latest row per key
select * from {{ source('shop', 'orders') }}
qualify row_number() over (partition by id order by _loaded_at desc) = 1
```

#### What causes "fan-out" in dbt models, and how do you catch it?

Joining on a key that isn't unique on one side multiplies rows, inflating sums. Uniqueness tests on join keys and on each model's grain catch it.

#### How do you handle model dependencies that form a cycle?

dbt refuses cycles. Restructure the logic, usually by extracting the shared part into an upstream model that both models reference.

#### How do you deal with duplicate rows coming from a source?

Deduplicate in the staging model, usually with a window function keeping the latest row per key, and test uniqueness afterwards:

```sql
select *
from {{ source('crm', 'customers') }}
qualify row_number() over (partition by customer_id order by updated_at desc) = 1
```

#### How do you handle schema changes in sources?

Detect them with tests and contracts, use explicit column lists in staging rather than `select *`, configure `on_schema_change` for incremental models, and adapt staging models in one place.

<!-- challenge -->

Model A refs model B for customer segments, and B now needs A's order totals. dbt reports a cycle. How do you restructure?

<!-- solution -->

Move the shared logic into a new upstream model (for example `int_customer_orders` with order totals per customer) that both A and B reference, removing the mutual dependency.

<!-- takeaways -->

- Fan-out comes from non-unique join keys.
- Deduplicate sources in staging.
- Break cycles with a shared upstream model.

<!-- unit: Production troubleshooting -->

<!-- goals -->

- Understand what happens when a model fails mid-run.
- Monitor production runs and investigate slowdowns.

<!-- concept -->

In production, failures are contained by the DAG: a failing model skips its children while independent branches finish. Retrying only the failed part after a fix avoids rebuilding everything.

Monitoring turns runs into trends: failures, test results and durations over time. When a job suddenly takes twice as long, the cause is usually data growth, a lost incremental filter, changed materialization or warehouse contention, and comparing runs points to which.

<!-- example -->

```text
run 2026-10-16: 41 min   run 2026-10-17: 88 min
slowest node change: fct_events 6 min → 52 min
manifest diff: fct_events materialized 'incremental' → 'table' (PR #212)
```

#### What happens when a model fails in the middle of a run?

Its downstream models are skipped, independent branches continue, and the run reports the failure. Fix it and run `dbt retry`, or rerun the failed model and its children with `model+`.

#### How do you monitor and troubleshoot issues with dbt in production?

Alert on job failures and test errors, track test failure trends and run durations, check source freshness before running, keep artifacts for comparison, and document an on-call procedure (inspect logs and compiled SQL, rerun with `dbt retry`, communicate data incidents to consumers).

#### What would you check when a dbt job suddenly takes twice as long?

Data volume growth in sources, a model that changed materialization or lost its incremental filter, a full refresh triggered by mistake, warehouse size or queuing, a new join that fans out, and missing partition pruning.

<!-- challenge -->

A production run failed on one mart at 05:00. After fixing the SQL, how do you complete the run quickly?

<!-- solution -->

Deploy the fix and run `dbt retry` (or `dbt build --select <failed_model>+`), which rebuilds the failed model and its skipped children without rerunning everything that succeeded.

<!-- takeaways -->

- Failures skip children; independent branches continue.
- `dbt retry` resumes from failures.
- Compare run timings to explain slowdowns.
