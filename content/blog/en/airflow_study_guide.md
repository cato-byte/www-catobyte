## Apache Airflow Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Apache Airflow study guide: about 200 questions](../../images/airflow_study_guide_title_img.png)

About 200 interview-style questions on Apache Airflow, from DAGs and operators to scheduling, sensors, assets, executors, testing, deployment and troubleshooting. The answers follow Airflow 3 and point out what changed from Airflow 2, since many companies still run both. Open a question to see its answer, or use the filter to search the whole guide.

<!-- QA -->

### Fundamentals

#### What is Apache Airflow?

An open-source platform to author, schedule and monitor workflows as code. Workflows are Python-defined DAGs of tasks; Airflow runs them on a schedule or on events, in dependency order, with retries, logging, alerting and a web UI. It started at Airbnb in 2014 and is an Apache top-level project.

#### What is Airflow good for, and what is it not for?

It is good for orchestrating batch workflows: ETL/ELT, triggering jobs in other systems (Spark, dbt, Databricks, Snowflake, Glue), ML pipelines, reports and maintenance. It is not a data processing engine (heavy computation should happen in the systems it triggers), not a streaming engine, and not designed for sub-second, very high-frequency scheduling.

#### What is a DAG?

A Directed Acyclic Graph: a collection of tasks with dependencies and no cycles. In Airflow, a DAG also carries its schedule, start date, default arguments, tags and other settings. Each time it runs, it creates a DAG run.

#### What is a task?

The basic unit of execution in a DAG: an instance of an operator, a decorated Python function (`@task`) or a sensor. Each task in each DAG run becomes a task instance with its own state, logs and retries.

#### What is an operator?

A template for a unit of work, such as `BashOperator`, `PythonOperator`, `SQLExecuteQueryOperator`, `DatabricksRunNowOperator` or `S3ToRedshiftOperator`. You instantiate it with parameters in a DAG to create a task.

#### What is a task instance?

A specific run of a task for a specific DAG run (and map index, for mapped tasks). It has a state (`scheduled`, `queued`, `running`, `success`, `failed`, `up_for_retry`, `skipped`, `upstream_failed` and others), a try number, and logs.

#### What is a DAG run?

One execution of a DAG, identified by a run ID and a logical date, created by the schedule, a manual trigger, an asset event or a backfill. It has a data interval for scheduled runs.

#### What does "workflows as code" give you?

Version control, code review, testing, dynamic generation of tasks, reuse through Python functions and libraries, and the ability to deploy workflows through CI/CD like any other software.

#### What are the main components of an Airflow deployment?

The scheduler (decides what runs when), the DAG processor (parses DAG files), the API server (serves the UI and REST API; in Airflow 2 this was the webserver), the executor and its workers (run tasks), the triggerer (runs deferred tasks), and the metadata database (stores state).

#### What is the metadata database?

A relational database (PostgreSQL or MySQL in production; SQLite only for testing) that stores DAG runs, task instances, connections, variables, XComs, users and serialized DAGs. It is the source of truth for Airflow's state, so it must be backed up and maintained.

#### What are the biggest changes in Airflow 3?

A new React UI, DAG versioning (each run is tied to the DAG version it ran with), the Task SDK and a Task Execution API so workers no longer talk to the metadata database directly, the `airflow api-server` replacing the webserver, datasets renamed to assets with event-driven scheduling, backfills managed by the scheduler, removal of SubDAGs and SLAs, and `schedule` replacing `schedule_interval`.

#### What is the Task SDK?

The stable, public interface for DAG authors in Airflow 3 (`from airflow.sdk import dag, task, DAG, Asset, Variable`). It decouples DAG code from Airflow's internals and lets tasks run remotely through the Task Execution API, even in other languages in the future.

#### What is an Airflow provider?

A separately versioned package that adds operators, hooks, sensors and connections for an external system: `apache-airflow-providers-amazon`, `-google`, `-databricks`, `-snowflake`, `-postgres`, `-standard` (core operators such as `BashOperator` and `PythonOperator` in Airflow 3) and many more.

#### What is a hook?

A class that wraps the connection to an external system and exposes helper methods, such as `S3Hook.load_file()` or `PostgresHook.get_records()`. Operators use hooks internally; you can also use them in your own Python tasks.

#### What is a connection?

A stored set of credentials and parameters for an external system (host, login, password, schema, port, extra JSON), referenced by `conn_id`. It can be stored in the metadata database, environment variables (`AIRFLOW_CONN_<ID>`) or a secrets backend.

#### What are Airflow Variables?

Key-value configuration values stored in Airflow (metadata database, environment variables `AIRFLOW_VAR_<NAME>` or a secrets backend), read with `Variable.get()`. Reading them at the top level of a DAG file causes a database or backend call on every parse, so read them inside tasks or with templates.

#### What is the difference between Airflow and cron?

Cron only starts commands at times. Airflow adds dependencies between tasks, retries, backfills, history, logs in one place, alerting, parameterization, a UI, and integration with external systems.

#### How does Airflow compare with Dagster and Prefect?

All three orchestrate Python workflows. Airflow is the most widely deployed with the largest ecosystem of providers. Dagster is asset-centric (you declare data assets and their lineage) with strong typing and local testing. Prefect focuses on dynamic Python flows with little boilerplate. Airflow 3 moved towards Dagster's ideas with assets and versioning.

#### What managed Airflow services exist?

Amazon MWAA (Managed Workflows for Apache Airflow), Google Cloud Composer, Astronomer (Astro) and Azure's Airflow offering in Data Factory/Fabric. They manage the scheduler, workers, database and upgrades.

#### What does "orchestration" mean, as opposed to "processing"?

Orchestration decides what runs, when, in which order and what happens on failure. Processing is the actual computation on data. Airflow orchestrates; Spark, SQL engines and dbt process.

#### What is the `airflow` CLI used for?

Managing and debugging Airflow: `airflow dags list|trigger|pause|test`, `airflow tasks test|clear`, `airflow db migrate|clean`, `airflow connections` and `variables` commands, `airflow config get-value`, and starting components (`scheduler`, `api-server`, `dag-processor`, `triggerer`, `celery worker`).

#### What does the REST API offer?

A stable, versioned API (served by the API server) to trigger and manage DAG runs, read task instance states and logs, manage connections, variables and pools, and clear tasks. CI pipelines and other systems use it to integrate with Airflow.

#### What does pausing a DAG do?

A paused DAG creates no new scheduled runs; running tasks finish. New DAGs are paused by default (`dags_are_paused_at_creation`) so they don't start running as soon as they are deployed.

#### What states can a DAG run have?

`queued`, `running`, `success` and `failed`. A DAG run's state is derived from its leaf tasks: it succeeds if they all succeed or are skipped.

#### What does `upstream_failed` mean?

The task didn't run because an upstream task failed and its trigger rule (by default `all_success`) couldn't be met.

### Writing DAGs

#### How do you define a DAG?

With the `@dag` decorator on a function, or with a `DAG` context manager. Tasks created inside belong to the DAG.

```python
from datetime import datetime
from airflow.sdk import dag, task

@dag(schedule="@daily", start_date=datetime(2026, 1, 1), catchup=False, tags=["sales"])
def daily_sales():
    @task
    def extract() -> list[dict]:
        return [{"id": 1, "amount": 10}]

    @task
    def load(rows: list[dict]) -> None:
        print(f"loading {len(rows)} rows")

    load(extract())

daily_sales()
```

#### What is the TaskFlow API?

The decorator-based way to write tasks (`@task`, `@task.bash`, `@task.virtualenv`, `@task.docker`, `@task.kubernetes` and others) where return values are passed to downstream tasks automatically through XCom and dependencies are inferred from function calls.

#### How do you set dependencies between tasks?

With bitshift operators (`extract >> transform >> load`), lists for fan-out and fan-in (`start >> [a, b] >> end`), `chain()` and `cross_downstream()` helpers, or implicitly by passing TaskFlow outputs as arguments.

#### What are `default_args`?

A dictionary of arguments applied to every task of a DAG, such as `owner`, `retries`, `retry_delay`, `email_on_failure` or `execution_timeout`. Tasks can override them.

#### What does `start_date` mean?

The date from which the DAG can be scheduled. It should be a fixed date in the past, never `datetime.now()`, which would change on each parse and prevent runs from being created.

#### What is `catchup`?

Whether the scheduler creates runs for all missed intervals between `start_date` (or the last run) and now. In Airflow 3 the default is `False`; in Airflow 2 it was `True`. Leaving catchup on for a DAG with an old start date can trigger hundreds of runs at once.

#### What are tags and `doc_md` for?

Tags group and filter DAGs in the UI. `doc_md` attaches Markdown documentation to the DAG or a task, shown in the UI, which helps on-call engineers understand what a DAG does.

#### Why should DAG files be lightweight at the top level?

The DAG processor parses every DAG file repeatedly (every 30 seconds by default for changed files). Top-level code such as database queries, API calls, `Variable.get()` or heavy imports runs on every parse, slowing the whole scheduler and hitting external systems. Put such work inside tasks.

#### How do you generate DAGs or tasks dynamically?

Loop in Python over a configuration (a list, a YAML file read from disk) to create tasks or several DAGs at parse time, or use dynamic task mapping for runtime fan-out. Keep the configuration static and cheap to read so parsing remains fast and deterministic.

#### What is a task group?

A way to group tasks visually and logically in the UI (`@task_group` or `TaskGroup`), with a shared prefix for task IDs and shared default arguments. It replaced SubDAGs, which were removed in Airflow 3.

#### What are trigger rules?

Rules deciding when a task runs based on its upstream states. The default is `all_success`. Others include `all_failed`, `all_done`, `one_success`, `one_failed`, `none_failed`, `none_failed_min_one_success`, `none_skipped` and `always`. For example a cleanup task uses `all_done`.

#### How do you branch in a DAG?

With `@task.branch` (or `BranchPythonOperator`), which returns the task ID(s) to follow; the others are skipped. A downstream join task needs a trigger rule such as `none_failed_min_one_success` so it isn't skipped too.

```python
@task.branch
def choose(**context):
    return "full_load" if context["logical_date"].day == 1 else "incremental_load"
```

#### What is `ShortCircuitOperator`?

An operator (or `@task.short_circuit`) that skips all downstream tasks when its callable returns a falsy value, for example when there is no new data.

#### What is `LatestOnlyOperator`?

An operator that skips its downstream tasks unless the run is the most recent scheduled one, useful for tasks such as sending a report that make no sense during a backfill.

#### How do you run a task in an isolated Python environment?

With `@task.virtualenv` (creates a virtualenv with given requirements), `@task.external_python` (uses an existing interpreter), `@task.docker` or `@task.kubernetes` (runs in a container). This avoids dependency conflicts with Airflow itself.

#### How do you pass parameters to a DAG run?

With `params` declared on the DAG (with defaults and optional JSON-schema validation), shown as a form when triggering manually, and read with `{{ params.name }}` or from the context.

#### What is the `BashOperator` used for, and what is the risk?

Running shell commands or scripts. The risk is templating untrusted input into the command (injection), and hiding complex logic in shell where it's hard to test.

#### How do you set a timeout on a task?

With `execution_timeout` (a `timedelta`); the task fails when it runs longer. A DAG-level `dagrun_timeout` fails the whole run after a duration.

#### What does `max_active_runs` do?

It limits how many runs of a DAG can be active at once. Setting it to 1 ensures runs happen sequentially, which matters for pipelines that depend on the previous run's output.

#### What is `depends_on_past`?

A task argument: if `True`, a task instance runs only if the same task succeeded (or was skipped) in the previous DAG run. It enforces sequential processing at task level.

#### What is the difference between `@task` and `PythonOperator`?

Both run a Python callable. `@task` (TaskFlow) is more concise, passes return values through XCom automatically and infers dependencies. `PythonOperator` is the classic form; you wire XCom and dependencies by hand. They can be mixed in a DAG.

#### How do you mix TaskFlow tasks and classic operators?

Classic operators expose `.output` (an `XComArg`) that can be passed into TaskFlow functions, and TaskFlow outputs can be passed into templated fields of classic operators. Dependencies are inferred from these links.

#### What is `@task.sensor`?

A decorator that turns a Python function into a sensor: it returns `True` (or a `PokeReturnValue`) when the condition is met, with the usual `poke_interval`, `timeout` and `mode` options.

#### What is `@setup` and `@teardown`?

Decorators marking tasks that create and clean up resources (a cluster, a temporary table). A teardown runs even if the work in between fails, and clearing a task also reruns its setup and teardown.

#### How do you define an owner and why does it matter?

With `owner` in `default_args`. It appears in the UI and alerts, so the right team is contacted when the DAG fails.

#### What is `email_on_failure`?

A task argument that sends an email when the task fails, using the SMTP settings. Most teams prefer callbacks or notifiers to Slack or PagerDuty for richer, routable alerts.

#### What happens when you rename a task or a DAG?

Airflow treats it as a new task or DAG: history stays under the old name. In Airflow 3, DAG versioning shows the change, but renaming still breaks continuity for metrics and `depends_on_past`.

### Scheduling and time

#### How do you schedule a DAG?

With the `schedule` argument: a cron expression (`"0 6 * * *"`), a preset (`"@daily"`, `"@hourly"`), a `timedelta`, a timetable, a list of assets (event-driven), or `None` for manual or externally triggered DAGs.

#### What is the logical date?

The date that identifies a run's place in the schedule (formerly `execution_date`). For interval-based schedules it is the start of the data interval, so a daily run for 2026-10-15 starts after that day ends, on 2026-10-16. In Airflow 3, manually triggered runs can have no logical date.

#### What is a data interval?

The period of data a scheduled run is responsible for, from `data_interval_start` to `data_interval_end`. Using it in queries (rather than "now") makes runs reproducible and backfills correct.

```sql
SELECT * FROM orders
WHERE created_at >= '{{ data_interval_start }}' AND created_at < '{{ data_interval_end }}'
```

#### Why does a daily DAG run "one day late"?

Because with interval-based scheduling a run starts at the end of its interval: it processes a complete day, so it can only start once that day is over. In Airflow 3, cron schedules default to `CronTriggerTimetable`, which runs at the cron time with no interval semantics, so this is less surprising.

#### What is a timetable?

A class that defines a custom schedule when cron isn't enough: business days only, several times on different days, fiscal calendars. Built-ins include `CronDataIntervalTimetable`, `CronTriggerTimetable`, `DeltaDataIntervalTimetable` and `MultipleCronTriggerTimetable`.

#### How does Airflow handle time zones?

Internally everything is stored in UTC. You can give a DAG a time-zone-aware `start_date` (with `pendulum`), and cron schedules then follow that time zone, including daylight saving changes. The UI can display local time.

#### What is a backfill?

Running a DAG for past intervals, for example after adding a DAG or fixing a bug. In Airflow 3 backfills are created through the UI, API or `airflow backfill create` and executed by the scheduler, with options for reprocessing behavior and concurrency.

#### What is the difference between catchup and a backfill?

Catchup is automatic: the scheduler creates missed runs since the last one. A backfill is an explicit request for a date range, which can also rerun intervals that already succeeded.

#### How do you clear and rerun tasks?

In the UI or CLI, clearing a task instance resets its state so the scheduler runs it again, optionally with downstream, upstream, past or future instances. This is the usual way to reprocess after a fix.

#### What is a manual trigger, and how do you do it?

Starting a DAG run outside its schedule from the UI, CLI (`airflow dags trigger`) or REST API, optionally with a configuration or parameters.

#### What does "idempotent task" mean in Airflow?

A task that produces the same result whether it runs once or several times for the same interval. Achieve it by processing the data interval rather than "latest", writing with overwrite of a partition or `MERGE` instead of append, and using deterministic file names.

#### Why shouldn't tasks use `datetime.now()`?

Because reruns and backfills would process the wrong period. Use the logical date or data interval from the context or templates.

#### How do you run a DAG only on business days?

Use a cron expression such as `0 6 * * 1-5`, or a custom timetable if holidays matter. A branch or short-circuit task can also skip processing on holidays from a calendar table.

#### What is the `@once` preset?

A schedule that creates a single run, useful for one-off DAGs such as migrations.

#### What happens if a run takes longer than the schedule interval?

The next run starts when it's due if `max_active_runs` allows it, so runs can overlap. Set `max_active_runs=1` (and possibly `depends_on_past=True`) when runs must not overlap.

#### How do you pass the previous successful run's date into a task?

Use the template variables `prev_data_interval_start_success` and `prev_data_interval_end_success` (or `prev_start_date_success`), useful for incremental loads that should continue from the last successful point.

#### How do daylight saving time changes affect schedules?

With a time-zone-aware start date, a daily cron at 02:30 can be skipped or run twice on transition days, depending on the local clock. Schedule critical jobs outside the 01:00–03:00 window or in UTC.

### Operators, sensors and deferrable tasks

#### What is a sensor?

A special operator that waits for a condition: a file in S3 (`S3KeySensor`), a partition, an external task, a SQL query returning rows, an HTTP endpoint, a time. It checks periodically until the condition is true or the timeout expires.

#### What is the difference between `poke` and `reschedule` modes?

In `poke` mode the sensor holds a worker slot for its whole wait, sleeping between checks. In `reschedule` mode it releases the slot between checks and is rescheduled later, which is better for long waits. Deferrable mode is better still.

#### What are deferrable operators?

Operators that, while waiting for something external (a job, a file, a time), suspend themselves and hand the wait to an asynchronous trigger running in the triggerer process, freeing the worker slot. When the trigger fires, the task resumes on a worker. Many provider operators have `deferrable=True`.

#### What is the triggerer?

A component that runs asyncio-based triggers for deferred tasks. One triggerer can handle thousands of waits concurrently with little resource use.

#### What is `ExternalTaskSensor`?

A sensor that waits for a task or DAG run in another DAG to reach a state, for the same logical date by default. It creates cross-DAG dependencies but couples schedules; assets are often a cleaner alternative.

#### What is `TriggerDagRunOperator`?

An operator that triggers another DAG, optionally passing configuration and waiting for it to finish. It is a push-style dependency, as opposed to the pull-style `ExternalTaskSensor`.

#### What is a sensor timeout, and why set it?

The maximum time a sensor waits before failing (`timeout`, default seven days). Set it to something realistic so a missing upstream file is noticed quickly instead of blocking resources for days. `soft_fail=True` marks the sensor skipped instead of failed.

#### How do you write a custom operator?

Subclass `BaseOperator`, declare parameters in `__init__`, list templatable fields in `template_fields`, and implement `execute(self, context)`, using hooks for external connections. Keep `__init__` cheap because it runs at parse time.

```python
from airflow.sdk import BaseOperator

class RowCountCheckOperator(BaseOperator):
    template_fields = ("table",)

    def __init__(self, *, table: str, conn_id: str, min_rows: int = 1, **kwargs):
        super().__init__(**kwargs)
        self.table, self.conn_id, self.min_rows = table, conn_id, min_rows

    def execute(self, context):
        from airflow.providers.postgres.hooks.postgres import PostgresHook
        count = PostgresHook(self.conn_id).get_first(f"SELECT count(*) FROM {self.table}")[0]
        if count < self.min_rows:
            raise ValueError(f"{self.table} has {count} rows")
        return count
```

#### What is the `EmptyOperator` used for?

A task that does nothing, used as a start or end marker or as a join point in the graph to make dependencies clearer.

#### How do you call a SQL database from Airflow?

With `SQLExecuteQueryOperator` (common SQL provider) and a connection, or with the provider-specific hook in a Python task. Keep SQL in separate `.sql` files referenced through templates.

#### How do you trigger a Databricks job from Airflow?

With `DatabricksRunNowOperator` (run an existing job by ID, passing parameters) or `DatabricksSubmitRunOperator` (submit a one-off run), from the Databricks provider, usually in deferrable mode so the wait doesn't hold a worker. `DatabricksWorkflowTaskGroup` can define a Databricks job from Airflow.

#### How do you run dbt from Airflow?

With a `BashOperator` calling `dbt build`, with a dbt Cloud operator (`DbtCloudRunJobOperator`), or with Astronomer Cosmos, which turns each dbt model into an Airflow task with dependencies from the dbt graph.

#### How do you run work on Kubernetes from Airflow?

With `KubernetesPodOperator` or `@task.kubernetes`, which start a pod with a given image, command, resources and secrets for each task. Each task gets its own dependencies and resources.

#### What is `PythonVirtualenvOperator` used for?

Running a function with dependencies that conflict with Airflow's, in a fresh virtualenv per run (slower) or a cached one. The function must be self-contained because it runs in another interpreter.

#### What are transfer operators?

Operators that move data between two systems in one task, such as `S3ToRedshiftOperator`, `GCSToBigQueryOperator`, `SqlToS3Operator` or `S3ToSnowflakeOperator`. They usually delegate the work to the target system (for example a `COPY` command).

#### What is `HttpOperator` used for?

Calling HTTP APIs with a connection for the base URL and credentials, with optional response checks and pagination. `HttpSensor` waits for an endpoint to return a condition.

#### How do you run an AWS Glue job from Airflow?

With `GlueJobOperator` from the Amazon provider, passing the job name and script arguments, preferably with `deferrable=True` or `wait_for_completion` with a `GlueJobSensor`.

#### How do you run an Athena query from Airflow?

With `AthenaOperator`, which submits the query, waits for completion and writes results to the configured S3 output location. Use templated dates in the query to process the data interval.

#### What is `on_execute_callback`?

A callback called just before a task executes, used for logging or notifications. Like the other callbacks, it should be quick and must not fail the task.

### XCom and passing data

#### What is XCom?

"Cross-communication": a mechanism to pass small values between tasks. A task pushes a value (TaskFlow return values are pushed automatically) and downstream tasks pull it. Values are stored in the metadata database by default.

#### Why shouldn't you pass large data through XCom?

The default backend stores values in the metadata database, which isn't designed for large payloads, and serialized values have size limits. Pass references instead (an S3 path, a table name, a partition) and keep the data in storage.

#### What is a custom XCom backend?

A pluggable backend that stores XCom values elsewhere (S3, GCS, Azure Blob) and keeps only a reference in the database. The Common IO provider offers an object storage backend with a size threshold.

#### How do you pull an XCom in a template?

```jinja2
{{ ti.xcom_pull(task_ids='extract', key='return_value') }}
```

With TaskFlow, you simply pass the output of one task function as an argument to another.

#### What is the task context?

A dictionary of runtime information available to tasks: `ti` (task instance), `dag_run`, `logical_date`, `data_interval_start`, `data_interval_end`, `params`, `run_id` and more. In TaskFlow you get it with `get_current_context()` or by declaring `**context`.

#### What is Jinja templating in Airflow?

Many operator fields (listed in `template_fields`) are rendered with Jinja just before execution, with context variables like `{{ ds }}`, `{{ data_interval_start }}`, `{{ params.x }}`, macros such as `{{ macros.ds_add(ds, -1) }}` and Variables (`{{ var.value.name }}`). The rendered values are visible in the UI.

#### What is `ds`?

A template variable with the logical date as `YYYY-MM-DD`. `ds_nodash` gives `YYYYMMDD`. They are convenient for partition names and file paths.

#### What is dynamic task mapping?

Creating a variable number of task instances at runtime from the output of an upstream task, with `.expand()`. For example, one task per file found in a bucket. `.partial()` sets the arguments shared by all instances.

```python
@task
def list_files() -> list[str]:
    return ["a.csv", "b.csv", "c.csv"]

@task
def process(path: str) -> int:
    return len(path)

process.expand(path=list_files())
```

#### How do you limit the parallelism of mapped tasks?

With `max_active_tis_per_dag` or `max_active_tis_per_dagrun` on the mapped task, or by assigning it to a pool with limited slots.

#### What does `multiple_outputs=True` do?

On a `@task` returning a dictionary, it pushes each key as a separate XCom, so downstream tasks can use `result["key"]` individually.

#### Are XComs deleted after a run?

They stay in the database (and are cleared when a task is cleared and rerun) until you purge them with `airflow db clean` or a retention policy. That's another reason to keep them small.

#### What is `XComArg`?

The object returned when you call a TaskFlow function or access `.output` on an operator. It represents a future value and carries the dependency, so passing it to another task links the two.

#### How do you avoid serialization errors with XCom?

Return JSON-serializable values (or types Airflow serializes, like dataclasses and pandas DataFrames with the right serializer); avoid open connections, generators or large objects. Return paths or IDs instead.

### Assets and event-driven scheduling

#### What is an asset (formerly dataset)?

A logical reference to a piece of data, identified by a URI (for example `s3://bucket/sales/`), declared as an outlet of a producing task. When the task succeeds, Airflow records an asset event, and DAGs scheduled on that asset are triggered.

```python
from airflow.sdk import Asset, dag, task

sales = Asset("s3://lake/silver/sales/")

@dag(schedule="@daily", start_date=datetime(2026, 1, 1))
def produce():
    @task(outlets=[sales])
    def build_sales(): ...
    build_sales()

@dag(schedule=[sales], start_date=datetime(2026, 1, 1))
def consume():
    @task
    def report(): ...
    report()
```

#### Why use assets instead of `ExternalTaskSensor`?

Assets express data dependencies directly ("run when sales is updated") without aligning schedules or holding sensor slots, and the UI shows lineage between producing and consuming DAGs.

#### Can a DAG depend on several assets?

Yes. A list means all must be updated since the last run; you can combine assets with `&` (and) and `|` (or) expressions. `AssetOrTimeSchedule` combines a time schedule with asset triggers.

#### What are asset watchers?

An Airflow 3 feature for event-driven scheduling from external systems: an `AssetWatcher` attaches a trigger (for example on a message queue such as SQS or Kafka) to an asset, so a DAG runs when an external event arrives, not only when another Airflow task updates the asset.

#### What is the `@asset` decorator?

An Airflow 3 shortcut that defines an asset together with the single-task DAG that materializes it, for asset-centric authoring similar to Dagster.

#### Do assets know whether the data actually changed?

No. Airflow only knows that a producing task succeeded; it doesn't inspect the data. If a task can succeed without writing anything, it should not emit the event, or the consumer must check.

#### Can you attach metadata to an asset event?

Yes. A producing task can add extra information (for example the row count or the partition written) to the asset event through outlet events, and consumers can read it from the triggering events in their context.

#### How do you see asset lineage in the UI?

The assets view shows each asset with its producing and consuming DAGs and the history of events, making cross-DAG dependencies visible.

#### What is an asset alias?

A placeholder used when the exact asset URI is only known at runtime: the task emits events for an alias and attaches the concrete asset, and consumers can schedule on the alias.

#### Can a DAG be triggered both on a schedule and by assets?

Yes, with `AssetOrTimeSchedule`, which runs on a timetable and also whenever the asset condition is met.

### Executors and architecture

#### What is an executor?

The component that decides how and where task instances run. The scheduler sends queued tasks to the executor, which runs them locally or dispatches them to workers.

#### What executors are available?

`LocalExecutor` (parallel processes on the scheduler machine), `CeleryExecutor` (a pool of workers fed by a message broker such as Redis or RabbitMQ), `KubernetesExecutor` (one pod per task), and provider executors such as the AWS ECS and Batch executors and the Edge executor for remote workers. Airflow 2.10+ can use several executors at once.

#### When would you choose the CeleryExecutor?

For many short tasks with steady load: long-running workers start tasks quickly. You need to operate a broker and scale workers yourself (or with KEDA).

#### When would you choose the KubernetesExecutor?

When tasks need different resources or images, isolation matters, and load is spiky: each task runs in its own pod and resources are released afterwards. Pod start-up adds seconds of latency per task.

#### What does the scheduler do?

It reads serialized DAGs, creates DAG runs when due, checks which task instances have their dependencies met, respects concurrency limits and pools, and sends tasks to the executor. Several schedulers can run at once for high availability.

#### What does the DAG processor do?

It parses DAG files and stores serialized DAGs in the database. In Airflow 3 it is a separate component, so user code never runs inside the scheduler.

#### What concurrency settings exist?

`parallelism` (max running tasks per scheduler), `max_active_tasks_per_dag`, `max_active_runs_per_dag`, pool slots, per-task `max_active_tis_per_dag`, and executor-specific settings such as Celery worker concurrency.

#### What is a pool?

A named limit on concurrent task slots, used to protect a shared resource: for example a pool of 4 slots for tasks that query a production database. Tasks are assigned to a pool and can consume several slots.

#### What is priority weight?

A number that decides which queued tasks run first when slots are limited. The weight rule (`downstream`, `upstream`, `absolute`) controls how it accumulates across the graph.

#### What are queues in the CeleryExecutor?

Named queues that workers subscribe to. Assigning tasks to a queue (`queue="gpu"`) routes them to workers with suitable resources.

#### How do workers get credentials in Airflow 3?

Through the Task Execution API: tasks request connections, variables and XComs from the API server instead of reading the metadata database, which improves security and allows remote workers.

#### What is the role of the message broker with Celery?

Redis or RabbitMQ holds the queue of tasks sent by the scheduler; Celery workers consume from it. A result backend (usually the database) stores task states.

#### What is the `pod_template_file`?

A Kubernetes pod specification used by the KubernetesExecutor (and KubernetesPodOperator) as the base for task pods: image, resources, volumes, node selectors, service account. Tasks can override parts with `executor_config`.

#### Can you use several executors at once?

Yes, since Airflow 2.10: configure a list of executors and assign tasks to one with the `executor` argument, for example most tasks on Celery and heavy, isolated ones on Kubernetes.

#### What is the Edge executor?

An executor (from the Edge3 provider) that runs tasks on remote workers that connect to the Airflow API over HTTP, for example in another network or data center, without direct database access.

#### How do you make the scheduler highly available?

Run two or more schedulers against the same PostgreSQL or MySQL database; they coordinate with row-level locks. Run several API servers behind a load balancer and several triggerers.

### Configuration, security and secrets

#### How is Airflow configured?

Through `airflow.cfg`, overridden by environment variables named `AIRFLOW__SECTION__KEY` (for example `AIRFLOW__CORE__PARALLELISM`). Environment variables are the usual approach in containers.

#### What is a secrets backend?

An integration that reads connections and variables from an external secrets manager: AWS Secrets Manager or SSM Parameter Store, HashiCorp Vault, Google Secret Manager, Azure Key Vault. Secrets don't have to be stored in the metadata database.

#### How does Airflow avoid showing secrets in logs and the UI?

It masks values of connection passwords, variables whose names contain words like `password`, `secret` or `token`, and values registered with `mask_secret()`. Masking is best-effort, so don't print secrets.

#### What is the Fernet key?

The key used to encrypt connection passwords and variable values in the metadata database. It must be set, kept secret and identical on all components; rotating it requires re-encrypting.

#### How is access to the UI controlled?

Through an auth manager. Airflow 3 ships a simple auth manager for development; the FAB auth manager provides role-based access control (Admin, Op, User, Viewer and custom roles), and managed services integrate with cloud IAM.

#### How should DAG code access cloud resources?

Through the worker's identity (IAM role for service accounts on Kubernetes, MWAA execution role, workload identity) wherever possible, rather than long-lived keys stored in connections.

#### How do you define connections as environment variables?

With `AIRFLOW_CONN_<CONN_ID>` set to a URI or JSON, for example `AIRFLOW_CONN_WAREHOUSE='postgresql://user:pass@host:5432/db'`. They don't appear in the UI, and they take precedence over a connection with the same ID in the database (a configured secrets backend is checked first).

#### How do you restrict who can trigger a DAG?

With role-based access control: give roles permissions on specific DAGs (by DAG ID or via `access_control` in the DAG), so a team can trigger and clear its own DAGs only.

#### Why is it risky to let many users edit DAG code?

DAG code runs with the workers' permissions and can read connections, so anyone who can deploy DAGs effectively has access to every connection. Code review and CI gates on the DAG repository are part of security.

### Testing and code quality

#### How do you test that DAGs load correctly?

With a DAG integrity test that loads all DAG files with `DagBag` and asserts there are no import errors, plus checks on conventions (tags, owners, retries, no cycles).

```python
from airflow.models import DagBag

def test_no_import_errors():
    bag = DagBag(dag_folder="dags/", include_examples=False)
    assert not bag.import_errors, bag.import_errors

def test_every_dag_has_retries():
    bag = DagBag(dag_folder="dags/", include_examples=False)
    for dag_id, dag in bag.dags.items():
        assert dag.default_args.get("retries", 0) >= 1, dag_id
```

#### How do you unit test task logic?

Keep business logic in plain Python functions or modules outside the DAG file, test them with pytest without Airflow, and keep tasks as thin wrappers. For operators, test `execute()` with mocked hooks.

#### What does `dag.test()` do?

It runs a whole DAG run in a single Python process without a scheduler, useful for local debugging in an IDE with breakpoints.

#### What does `airflow tasks test` do?

It runs one task instance for a given date without recording state in the database or checking dependencies. It's handy for quick checks of templating and logic.

#### How do you run Airflow locally for development?

With the official Docker Compose setup, `airflow standalone`, the Astro CLI (`astro dev start`), or Breeze for contributing to Airflow. Use the same image and providers as production.

#### What linting is useful for DAG code?

Ruff with the Airflow rules (`AIR` rules flag deprecated imports and Airflow 3 migration issues), type checking, and custom checks for top-level code, missing owners or tags, and hard-coded credentials.

#### How do you test DAGs against real systems?

In a staging Airflow pointing at staging data stores: deploy from a branch, trigger runs with parameters for a small date range, and check outputs with data quality tests. Avoid running tests against production data stores.

#### How do you test custom operators with external systems?

Mock the hook in unit tests to check the operator's logic and parameters, and run integration tests against local containers (Postgres, LocalStack for AWS, MinIO for S3) in CI.

#### How do you check templated fields render correctly?

Render them for a given context in a test (`ti.render_templates()`), or run `airflow tasks render dag_id task_id date`, and check the rendered SQL or command.

#### What should a CI pipeline for an Airflow repository run?

Linting (Ruff with `AIR` rules), unit tests for business logic, DAG integrity tests (`DagBag` import errors, conventions, cycles), parse-time checks, image build, and deployment to staging, with production deployment after merge or approval.

#### How do you test that a DAG has the right structure?

Load it from a `DagBag` and assert task IDs, dependencies (`task.downstream_task_ids`), schedules and settings, so accidental changes to the graph are caught.

### Deployment and operations

#### How do you deploy DAGs?

Most teams build a Docker image with Airflow, providers, dependencies and DAG code, and deploy it through CI/CD to Kubernetes (Helm chart) or a managed service. Alternatives: syncing DAGs from Git with git-sync or to an S3 bucket (MWAA). DAG bundles in Airflow 3 can read DAGs directly from Git with versioning.

#### What is a DAG bundle?

An Airflow 3 concept for a collection of DAG files from a source such as a local folder or a Git repository, which lets Airflow track versions of DAG code and run a DAG run with the code version it started with.

#### How do you upgrade Airflow safely?

Read the release notes, upgrade in a test environment first, use the constraints files to pin compatible dependencies, run `airflow db migrate`, check DAGs for deprecations (Ruff `AIR` rules for Airflow 3), and back up the metadata database before migrating production.

#### What are constraints files?

Pinned dependency lists published for each Airflow and Python version, used with `pip install "apache-airflow==X" --constraint <url>` to get a known-good set of packages.

#### How do you keep the metadata database healthy?

Use a managed PostgreSQL with backups, monitor its size, and run `airflow db clean` periodically to purge old task instances, logs metadata and XComs. A huge database slows the scheduler and UI.

#### Where do task logs go?

By default to local files on workers, shown in the UI. In production, configure remote logging to S3, GCS, Azure Blob, Elasticsearch or CloudWatch so logs survive pod restarts.

#### How do you monitor Airflow?

With StatsD or OpenTelemetry metrics (scheduler heartbeat, DAG parse time, queued and running tasks, task durations, pool usage) in Prometheus/Grafana or Datadog, health endpoints, and alerts on failures and on runs that take too long.

#### How do you get alerted on task failures?

With callbacks (`on_failure_callback`, `on_retry_callback`, `on_success_callback`) that send to Slack, email or PagerDuty, the notifier classes from providers, or email settings. Alert on the DAG level for actionable, non-duplicated messages.

#### What replaced SLAs in Airflow 3?

SLAs (`sla` and `sla_miss_callback`) were removed because they were unreliable. Airflow 3.1 introduced deadline alerts, which trigger a callback when a DAG run hasn't finished by a deadline relative to a reference time. Until then, teams used `execution_timeout`, `dagrun_timeout` and external monitoring.

#### What are common causes of tasks stuck in `queued`?

No free slots (parallelism, pool or DAG concurrency limits), workers down or not consuming the queue, the executor not able to start pods (quota, image pull errors), or a scheduler problem. Check pools, worker logs and executor events.

#### What are zombie tasks?

Task instances marked as running whose process died without reporting (worker crash, OOM kill, pod eviction). The scheduler detects missing heartbeats and fails or retries them.

#### How do you scale Airflow?

Run several schedulers, scale workers (autoscaling Celery workers with KEDA, or Kubernetes executor), use deferrable operators to free slots, reduce DAG parse time, tune `parallelism` and pools, and keep heavy computation outside Airflow.

#### Why is DAG parse time important?

Slow parsing delays scheduling for all DAGs and consumes CPU. Measure it with `airflow dags report`; fix it by removing top-level work, avoiding heavy imports at module level, and splitting giant generated DAG files.

#### What is the official Helm chart?

The Apache Airflow Helm chart, which deploys all components on Kubernetes with options for executors, git-sync, PgBouncer, KEDA autoscaling, logging and secrets. It's the standard self-hosted Kubernetes deployment.

#### Why use PgBouncer with Airflow?

Each task and component opens database connections; many concurrent tasks can exhaust PostgreSQL's connection limit. PgBouncer pools them. In Airflow 3 the Task Execution API reduces direct connections from workers.

#### How do you deploy to Amazon MWAA?

Upload DAGs to the environment's S3 bucket (usually via CI with `aws s3 sync`), and manage `requirements.txt`, plugins and a startup script in S3; the environment's Airflow version and size are set in its configuration. The execution role grants AWS access.

#### What should a runbook for a failed DAG contain?

What the DAG does and who owns it, upstream dependencies, how to check logs and inputs, which tasks are safe to clear and rerun, how to backfill, who to notify, and known failure modes with fixes.

#### How do you roll back a bad DAG deployment?

Redeploy the previous image or Git commit through CI. With DAG versioning in Airflow 3, existing runs keep their version. Then clear failed runs if needed.

### Best practices

#### Should Airflow do the data processing itself?

No. Airflow should orchestrate: trigger Spark, SQL engines, dbt, Databricks or containers that do the processing, and pass references. Heavy pandas work on Airflow workers competes with other tasks and is hard to scale.

#### What makes a good task granularity?

Each task should be a meaningful, retryable unit (extract one source, load one table, run one model group). Too coarse means retrying lots of work; too fine adds scheduling overhead and makes the graph unreadable.

#### How do you make retries safe?

Make tasks idempotent, set `retries` and `retry_delay` (with `retry_exponential_backoff`) for transient errors, and fail fast (no retries) for errors that retrying can't fix, such as bad credentials or a data quality failure.

#### Where should configuration live?

In code (versioned) for structure, in environment variables or Variables for environment-specific values, and in a secrets backend for credentials. Avoid many Variables read at parse time.

#### How do you name DAGs and tasks?

Consistently and descriptively: `domain__purpose` for DAGs (`sales__daily_load`), verbs for tasks (`extract_orders`, `load_orders`), with owners and tags for teams and data domains.

#### How do you handle shared code between DAGs?

Put it in a Python package (in the repository's `include/` or `plugins/` path, or installed into the image) with its own tests, rather than copying code between DAG files.

#### What are plugins used for in Airflow?

Extending Airflow with custom UI views, menu links, macros, listeners, timetables and, in Airflow 3, FastAPI apps and React views. Custom operators and hooks don't need to be plugins; regular Python modules work.

#### What are listeners?

Hooks into Airflow events (DAG run started or finished, task instance state changes) implemented with pluggy, used for lineage (OpenLineage), auditing or custom notifications.

#### What is OpenLineage in Airflow?

A standard for lineage metadata. The OpenLineage provider emits events describing inputs and outputs of tasks to a backend such as Marquez or a data catalog, so you can see which jobs read and write which datasets.

#### How do you handle data quality checks in Airflow?

With SQL check operators (`SQLColumnCheckOperator`, `SQLTableCheckOperator`, `SQLCheckOperator`), Great Expectations or Soda operators, or dbt tests, placed after loads to stop downstream tasks when data is wrong.

#### Why should DAGs avoid relying on local files between tasks?

Tasks can run on different workers or pods, so a file written by one task may not exist for the next. Use object storage, a shared volume or a database instead.

#### How many DAGs should a pipeline be split into?

One DAG per independent schedule and ownership boundary. Split when parts have different schedules, owners or failure domains, and connect them with assets; keep tightly coupled steps in one DAG.

#### How do you keep a DAG readable?

Small tasks with clear names, task groups for logical blocks, no business logic in the DAG file, documentation with `doc_md`, consistent use of TaskFlow or operators, and limited dynamic generation.

#### Why pin provider and dependency versions?

Unpinned upgrades can change operator behavior or break imports silently. Pin versions with the constraints file and upgrade deliberately with tests.

### Scenarios

#### A daily DAG must load yesterday's files from S3 into Snowflake, then run dbt. Design it.

A DAG scheduled daily with `catchup=False` (or true if history matters), a deferrable `S3KeySensor` on the expected prefix for the data interval, a `CopyFromExternalStageToSnowflakeOperator` or SQL task running `COPY INTO`, then dbt through Cosmos or a dbt Cloud operator, data quality checks, and failure callbacks to Slack. All paths and filters come from the data interval.

#### Hundreds of DAGs are slow to schedule. What do you investigate?

DAG parse times (`airflow dags report`), top-level code and imports, the number of DAG files, scheduler CPU and database performance, the number of task instances in the database (run `db clean`), and whether the scheduler and DAG processor have enough resources or replicas.

#### A sensor waits for a file that sometimes never arrives. How do you handle it?

Make the sensor deferrable or use `reschedule` mode, give it a realistic timeout, decide whether the absence should fail (alert someone) or skip (`soft_fail`), and notify the source owner. Document the expected arrival time.

#### A task fails randomly on an API's rate limit. What do you do?

Add retries with exponential backoff, put the API calls in a pool limiting concurrency, respect `Retry-After` in the hook, and reduce calls (batching, incremental extraction).

#### You need to reprocess six months of data after a bug fix. How?

Make sure tasks are idempotent and use the data interval, then create a backfill for the date range with limited concurrency (`max_active_runs`) so production isn't starved, or clear the affected DAG runs. Monitor and validate outputs afterwards.

#### Two DAGs write to the same table and sometimes conflict. How do you fix it?

Serialize them: one pool with one slot for writes to that table, or merge them into one DAG with explicit order, or make one depend on the other through an asset. Better still, give each table one owner process.

#### How would you migrate from Airflow 2 to Airflow 3?

Upgrade to the latest 2.x first and fix deprecation warnings, run Ruff's `AIR3` rules to find code to change (imports to `airflow.sdk`, `schedule_interval` to `schedule`, `execution_date` to `logical_date`, removed SubDAGs and SLAs, no direct database access in tasks), test in a staging environment, migrate the database, and update deployment for the API server and DAG processor.

#### How would you orchestrate a pipeline across AWS Glue, Databricks and a dbt project?

One DAG (or asset-linked DAGs) using the Amazon provider's `GlueJobOperator`, the Databricks provider's `DatabricksRunNowOperator` and Cosmos or the dbt Cloud operator, all in deferrable mode, passing table names or paths, with data quality checks between steps and a single alerting setup.

#### Your on-call engineer is paged every night for the same flaky task. What do you change?

Find the root cause in logs (timeouts, resource limits, upstream lateness), add appropriate retries with backoff only for transient errors, add a sensor or asset dependency if it starts before its input is ready, raise resources or move it to a dedicated pool, and change alerts to fire only after retries are exhausted.

#### A DAG works locally but tasks fail in production with "module not found". Why?

The production image or workers lack the dependency, or the module isn't on the path (for example code outside the DAGs or plugins folder). Add it to the image's requirements or package, and build local and production from the same image.

#### Tasks are often killed with no error in the logs. What do you suspect?

Out-of-memory kills (OOM) of the worker or pod, evictions, or timeouts. Check pod events and worker metrics, raise memory limits, and move heavy processing out of Airflow.

#### Your backfill runs created duplicates in the target table. What went wrong?

Tasks weren't idempotent: they appended data or used "now" instead of the data interval. Rewrite the load to overwrite the interval's partition or `MERGE` on keys, delete the duplicates, and rerun.

#### A business user wants a report emailed only if yesterday's sales are complete. How?

Schedule the report DAG on the sales asset (or a sensor on the load), add a data quality check (row count and completeness compared with expected sources), short-circuit the email if checks fail, and alert the data team instead.

#### How do you trigger an Airflow DAG when a file lands in S3, with no polling?

Use an asset watcher on an SQS queue that receives S3 event notifications (Airflow 3), or an S3 event that triggers a Lambda function calling the Airflow REST API to trigger the DAG with the file path as configuration.

#### Your scheduler's CPU is at 100%. What are typical fixes?

Reduce DAG parsing load (fewer, lighter files, longer `min_file_process_interval`, separate DAG processor), move away from sensors in poke mode, clean the database, add scheduler replicas, and check for DAGs with huge numbers of mapped tasks.

#### How would you explain Airflow to a non-technical stakeholder?

It's the scheduler and traffic controller for the company's data jobs: it starts each step at the right time and in the right order, retries when something hiccups, and alerts the team when something needs a human.
