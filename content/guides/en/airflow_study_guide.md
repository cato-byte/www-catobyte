## Apache Airflow Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Apache Airflow study guide: about 200 questions](../../images/airflow_study_guide_title_img.png)

About 200 interview-style questions on Apache Airflow, from DAGs and operators to scheduling, sensors, assets, executors, testing, deployment and troubleshooting. The answers follow Airflow 3 and point out what changed from Airflow 2, since many companies still run both.

The guide follows a learning path in five stages. Each section is split into short units: learning goals, a concept explanation and a worked example, then questions (recall first, then application), a practical challenge and key takeaways. To **learn**, read each unit top to bottom. To **review**, switch to review mode or use "Skip to questions", mark answers you want to see again, and try a mixed review across sections.

<!-- QA -->
<!-- stage: Foundations -->

### Fundamentals

<!-- unit: What Airflow is for -->

<!-- goals -->

- Explain what an orchestrator does and what it leaves to other systems.
- Compare Airflow with cron, Dagster, Prefect and managed services.

<!-- concept -->

A data platform has many jobs that depend on each other: extract before load, load before transform, transform before report. Something has to start each job at the right time, in the right order, and react when one fails. That is orchestration, and it is separate from processing, which is the heavy computation that engines like Spark or a warehouse do.

Airflow is an orchestrator. Because pipelines are written as Python code, they get the same review, testing and deployment habits as any software. Its alternatives differ mostly in philosophy and in who runs the servers.

<!-- example -->

| Need | cron | Airflow |
|---|---|---|
| Start a command at 06:00 | Yes | Yes |
| Run load only after extract succeeds | No | Yes |
| Retry, alert, show history and logs | No | Yes |
| Rerun last March for one table | Manual | Backfill |

#### What is Apache Airflow?

An open-source platform to author, schedule and monitor workflows as code. Workflows are Python-defined DAGs of tasks; Airflow runs them on a schedule or on events, in dependency order, with retries, logging, alerting and a web UI. It started at Airbnb in 2014 and is an Apache top-level project.

#### What is Airflow good for, and what is it not for?

It is good for orchestrating batch workflows: ETL/ELT, triggering jobs in other systems (Spark, dbt, Databricks, Snowflake, Glue), ML pipelines, reports and maintenance. It is not a data processing engine (heavy computation should happen in the systems it triggers), not a streaming engine, and not designed for sub-second, very high-frequency scheduling.

#### What does "orchestration" mean, as opposed to "processing"?

Orchestration decides what runs, when, in which order and what happens on failure. Processing is the actual computation on data. Airflow orchestrates; Spark, SQL engines and dbt process.

#### What does "workflows as code" give you?

Version control, code review, testing, dynamic generation of tasks, reuse through Python functions and libraries, and the ability to deploy workflows through CI/CD like any other software.

#### What is the difference between Airflow and cron?

Cron only starts commands at times. Airflow adds dependencies between tasks, retries, backfills, history, logs in one place, alerting, parameterization, a UI, and integration with external systems.

#### How does Airflow compare with Dagster and Prefect?

All three orchestrate Python workflows. Airflow is the most widely deployed with the largest ecosystem of providers. Dagster is asset-centric (you declare data assets and their lineage) with strong typing and local testing. Prefect focuses on dynamic Python flows with little boilerplate. Airflow 3 moved towards Dagster's ideas with assets and versioning.

#### What managed Airflow services exist?

Amazon MWAA (Managed Workflows for Apache Airflow), Google Cloud Composer, Astronomer (Astro) and Azure's Airflow offering in Data Factory/Fabric. They manage the scheduler, workers, database and upgrades.

#### How would you explain Airflow to a non-technical stakeholder?

It's the scheduler and traffic controller for the company's data jobs: it starts each step at the right time and in the right order, retries when something hiccups, and alerts the team when something needs a human.

<!-- challenge -->

A team runs 30 cron jobs on one VM, and each script sleeps 20 minutes "to be sure" the previous one finished. Name two problems Airflow would solve and one thing it would not.

<!-- solution -->

Airflow would replace the sleeps with real dependencies, so jobs start as soon as their inputs are ready, and it would add retries, alerts and a history of runs. It would not make the scripts faster: heavy processing still belongs in the engines the tasks call.

<!-- takeaways -->

- Orchestration decides what runs and when; processing does the work.
- Workflows as code bring review, testing and CI/CD to pipelines.
- Airflow has the largest ecosystem; alternatives differ in style and hosting.

<!-- unit: DAGs, tasks and runs -->

<!-- goals -->

- Tell apart DAGs, tasks, operators, task instances and DAG runs.
- Read run and task states, including `upstream_failed`.

<!-- concept -->

Airflow separates definition from execution. In code you define a DAG: tasks and the dependencies between them. Every time the DAG is scheduled, Airflow creates a DAG run, and inside it one task instance per task. States live on these runtime objects, not on the code, which is why the same task can be green yesterday and red today.

Dependencies drive the states: a task only starts when its upstream tasks are in the states its trigger rule expects. A failure upstream therefore shows up downstream as `upstream_failed`, and a DAG run's final state is derived from its last tasks.

<!-- example -->

```text
DAG daily_sales (code)         DAG run 2026-10-17 (runtime)
 extract >> transform >> load   extract    success
                                transform  failed
                                load       upstream_failed  → run: failed
```

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

#### What states can a DAG run have?

`queued`, `running`, `success` and `failed`. A DAG run's state is derived from its leaf tasks: it succeeds if they all succeed or are skipped.

#### What does `upstream_failed` mean?

The task didn't run because an upstream task failed and its trigger rule (by default `all_success`) couldn't be met.

#### What does pausing a DAG do?

A paused DAG creates no new scheduled runs; running tasks finish. New DAGs are paused by default (`dags_are_paused_at_creation`) so they don't start running as soon as they are deployed.

<!-- challenge -->

You deploy a new DAG with a daily schedule, but no runs appear the next morning. What is the most likely reason, and what do you check?

<!-- solution -->

New DAGs are paused by default, so the scheduler creates no runs. Unpause it in the UI or with `airflow dags unpause`. Also check the DAG has no import errors and that its `start_date` is in the past.

<!-- takeaways -->

- A DAG is code; DAG runs and task instances are its executions.
- States belong to task instances and DAG runs, not to tasks.
- `upstream_failed` points you to a failure earlier in the graph.

<!-- unit: Architecture and Airflow 3 -->

<!-- goals -->

- Describe the components of an Airflow deployment and what each stores or runs.
- Summarize what Airflow 3 changed for DAG authors and operators.

<!-- concept -->

Airflow is a set of cooperating services around one database. The DAG processor turns files into serialized DAGs, the scheduler decides what is due, executors and workers run tasks, the triggerer handles waiting, and the API server serves the UI and REST API. The metadata database is the shared memory: if it is lost, so is all state.

Airflow 3 tightened these boundaries. Workers no longer touch the database directly; they go through an API, and DAG authors import from one stable SDK. That makes upgrades safer and remote execution possible.

<!-- example -->

```python
# Airflow 3: import everything from the stable Task SDK
from airflow.sdk import dag, task, Asset, Variable
```
```bash
airflow dags list-import-errors     # CLI for debugging
curl -X POST "$AIRFLOW/api/v2/dags/daily_sales/dagRuns" -d '{"logical_date": null}'
```

#### What are the main components of an Airflow deployment?

The scheduler (decides what runs when), the DAG processor (parses DAG files), the API server (serves the UI and REST API; in Airflow 2 this was the webserver), the executor and its workers (run tasks), the triggerer (runs deferred tasks), and the metadata database (stores state).

#### What is the metadata database?

A relational database (PostgreSQL or MySQL in production; SQLite only for testing) that stores DAG runs, task instances, connections, variables, XComs, users and serialized DAGs. It is the source of truth for Airflow's state, so it must be backed up and maintained.

#### What are the biggest changes in Airflow 3?

A new React UI, DAG versioning (each run is tied to the DAG version it ran with), the Task SDK and a Task Execution API so workers no longer talk to the metadata database directly, the `airflow api-server` replacing the webserver, datasets renamed to assets with event-driven scheduling, backfills managed by the scheduler, removal of SubDAGs and SLAs, and `schedule` replacing `schedule_interval`.

#### What is the Task SDK?

The stable, public interface for DAG authors in Airflow 3 (`from airflow.sdk import dag, task, DAG, Asset, Variable`). It decouples DAG code from Airflow's internals and lets tasks run remotely through the Task Execution API, even in other languages in the future.

#### What is the `airflow` CLI used for?

Managing and debugging Airflow: `airflow dags list|trigger|pause|test`, `airflow tasks test|clear`, `airflow db migrate|clean`, `airflow connections` and `variables` commands, `airflow config get-value`, and starting components (`scheduler`, `api-server`, `dag-processor`, `triggerer`, `celery worker`).

#### What does the REST API offer?

A stable, versioned API (served by the API server) to trigger and manage DAG runs, read task instance states and logs, manage connections, variables and pools, and clear tasks. CI pipelines and other systems use it to integrate with Airflow.

<!-- challenge -->

A team wants an external system to start a DAG run after it finishes a nightly export. Which interface do you suggest, and what must the caller have?

<!-- solution -->

Use the REST API to create a DAG run, passing parameters in the request body. The caller needs credentials with permission to trigger that DAG, ideally a dedicated service account, and network access to the API server.

<!-- takeaways -->

- The metadata database holds all state; back it up.
- Airflow 3 isolates workers behind an API and exposes a stable Task SDK.
- Use the CLI for debugging and the REST API for integrations.

<!-- unit: Connecting to other systems -->

<!-- goals -->

- Explain how providers, hooks and connections fit together.
- Decide when to use Variables and when not to.

<!-- concept -->

Airflow talks to the outside world in layers. A provider package brings everything for one system. Inside it, hooks know how to open a session and call the system, and operators use hooks to do one unit of work. Hooks get their host and credentials from connections, looked up by `conn_id`, so code never contains secrets and the same DAG works in every environment.

Variables cover the rest of the configuration. They are convenient but each read can hit the database, so they belong inside tasks, not at the top of DAG files.

<!-- example -->

```python
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

@task
def list_new_files(prefix: str) -> list[str]:
    hook = S3Hook(aws_conn_id="aws_data")       # credentials come from the connection
    return hook.list_keys(bucket_name="landing", prefix=prefix)
```

#### What is an Airflow provider?

A separately versioned package that adds operators, hooks, sensors and connections for an external system: `apache-airflow-providers-amazon`, `-google`, `-databricks`, `-snowflake`, `-postgres`, `-standard` (core operators such as `BashOperator` and `PythonOperator` in Airflow 3) and many more.

#### What is a hook?

A class that wraps the connection to an external system and exposes helper methods, such as `S3Hook.load_file()` or `PostgresHook.get_records()`. Operators use hooks internally; you can also use them in your own Python tasks.

#### What is a connection?

A stored set of credentials and parameters for an external system (host, login, password, schema, port, extra JSON), referenced by `conn_id`. It can be stored in the metadata database, environment variables (`AIRFLOW_CONN_<ID>`) or a secrets backend.

#### What are Airflow Variables?

Key-value configuration values stored in Airflow (metadata database, environment variables `AIRFLOW_VAR_<NAME>` or a secrets backend), read with `Variable.get()`. Reading them at the top level of a DAG file causes a database or backend call on every parse, so read them inside tasks or with templates.

<!-- challenge -->

A DAG hard-codes a Postgres password and reads five Variables at the top of the file. What do you change?

<!-- solution -->

Move the password into a connection (stored in a secrets backend) and use the Postgres hook with its `conn_id`. Read the Variables inside the tasks that need them, or pass them through templates, so parsing doesn't query the database.

<!-- takeaways -->

- Providers package hooks, operators and sensors for one system.
- Connections keep credentials out of code; hooks use them.
- Read Variables at runtime, not at parse time.

### Writing DAGs

<!-- unit: Defining DAGs and tasks -->

<!-- goals -->

- Write a DAG with TaskFlow tasks and classic operators.
- Express dependencies, fan-out and grouping.

<!-- concept -->

There are two ways to create tasks, and they mix freely. Classic operators are configured objects; TaskFlow functions are plain Python decorated with `@task`. With TaskFlow, passing one task's return value to another both moves the data and creates the dependency, so the graph follows the code. Where there is no data to pass, you draw the edges yourself with `>>`.

Task groups keep large graphs readable without changing how tasks run.

<!-- example -->

```python
from airflow.sdk import dag, task
from airflow.providers.standard.operators.bash import BashOperator

@dag(schedule="@daily", start_date=datetime(2026, 1, 1), catchup=False)
def daily_sales():
    @task
    def extract() -> list[dict]: ...
    @task
    def load(rows: list[dict]): ...
    notify = BashOperator(task_id="notify", bash_command="echo done")
    load(extract()) >> notify       # data edge + explicit edge

daily_sales()
```

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

#### What is the difference between `@task` and `PythonOperator`?

Both run a Python callable. `@task` (TaskFlow) is more concise, passes return values through XCom automatically and infers dependencies. `PythonOperator` is the classic form; you wire XCom and dependencies by hand. They can be mixed in a DAG.

#### How do you mix TaskFlow tasks and classic operators?

Classic operators expose `.output` (an `XComArg`) that can be passed into TaskFlow functions, and TaskFlow outputs can be passed into templated fields of classic operators. Dependencies are inferred from these links.

#### How do you set dependencies between tasks?

With bitshift operators (`extract >> transform >> load`), lists for fan-out and fan-in (`start >> [a, b] >> end`), `chain()` and `cross_downstream()` helpers, or implicitly by passing TaskFlow outputs as arguments.

#### What is a task group?

A way to group tasks visually and logically in the UI (`@task_group` or `TaskGroup`), with a shared prefix for task IDs and shared default arguments. It replaced SubDAGs, which were removed in Airflow 3.

<!-- challenge -->

Ten tables are loaded by identical extract-then-load pairs, and all must finish before a summary task. Sketch the dependencies.

<!-- solution -->

Create one task group per table (extract >> load), then `[group_1, ..., group_10] >> summary`. Generating the groups in a loop over the table list keeps it to a few lines.

<!-- takeaways -->

- TaskFlow passes data and dependencies in one call.
- Use `>>`, lists and `chain()` when there is no data to pass.
- Task groups organize the graph; they don't change execution.

<!-- unit: DAG-level settings -->

<!-- goals -->

- Set defaults, ownership and documentation for every task.
- Choose `start_date`, `catchup` and parameters correctly.

<!-- concept -->

Most settings are the same for every task in a DAG, so they go in one place. `default_args` holds retries, owner and alerting; the DAG itself holds schedule, start date and catchup. These choices decide how a DAG behaves on its first deploy: a start date in the past combined with catchup can launch hundreds of runs at once.

Ownership, tags and documentation cost nothing and pay off during incidents, when someone who didn't write the DAG needs to know what it does and who to call. Params make manual runs safe by validating input.

<!-- example -->

```python
default_args = {"owner": "sales-data", "retries": 2, "retry_delay": timedelta(minutes=5)}

@dag(schedule="0 6 * * *", start_date=datetime(2026, 1, 1), catchup=False,
     default_args=default_args, tags=["sales"], doc_md=__doc__,
     params={"full_refresh": Param(False, type="boolean")})
def sales_load(): ...
```

#### What are `default_args`?

A dictionary of arguments applied to every task of a DAG, such as `owner`, `retries`, `retry_delay`, `email_on_failure` or `execution_timeout`. Tasks can override them.

#### How do you define an owner and why does it matter?

With `owner` in `default_args`. It appears in the UI and alerts, so the right team is contacted when the DAG fails.

#### What is `email_on_failure`?

A task argument that sends an email when the task fails, using the SMTP settings. Most teams prefer callbacks or notifiers to Slack or PagerDuty for richer, routable alerts.

#### What are tags and `doc_md` for?

Tags group and filter DAGs in the UI. `doc_md` attaches Markdown documentation to the DAG or a task, shown in the UI, which helps on-call engineers understand what a DAG does.

#### What does `start_date` mean?

The date from which the DAG can be scheduled. It should be a fixed date in the past, never `datetime.now()`, which would change on each parse and prevent runs from being created.

#### What is `catchup`?

Whether the scheduler creates runs for all missed intervals between `start_date` (or the last run) and now. In Airflow 3 the default is `False`; in Airflow 2 it was `True`. Leaving catchup on for a DAG with an old start date can trigger hundreds of runs at once.

#### How do you pass parameters to a DAG run?

With `params` declared on the DAG (with defaults and optional JSON-schema validation), shown as a form when triggering manually, and read with `{{ params.name }}` or from the context.

<!-- challenge -->

A DAG uses `start_date=datetime.now()`. Runs never appear, or appear at odd times. Why, and what is the fix?

<!-- solution -->

The start date changes on every parse, so the scheduler never sees a complete interval after it. Use a fixed date in the past, set `catchup=False` unless history is needed, and let the schedule decide when runs happen.

<!-- takeaways -->

- Put shared task settings in `default_args`.
- Use a fixed past `start_date`; decide on `catchup` deliberately.
- Owners, tags, docs and params make DAGs easier to operate.

<!-- unit: Controlling the flow -->

<!-- goals -->

- Use trigger rules, branches and short-circuits to control what runs.
- Guarantee cleanup with setup and teardown tasks.

<!-- concept -->

By default a task runs only when everything upstream succeeded. Real pipelines need more: skip work when there is no data, choose one path out of several, run a cleanup even after failure. Each tool changes either which tasks are skipped or which upstream states a task accepts.

The trap is that skips propagate. After a branch, the join task must use a trigger rule that tolerates skipped parents, or it will be skipped too. Setup and teardown pairs make cleanup explicit, so a failed run doesn't leave clusters running.

<!-- example -->

```python
@task.branch
def choose(**context):
    return "full_load" if context["params"]["full_refresh"] else "incremental_load"

join = EmptyOperator(task_id="join", trigger_rule="none_failed_min_one_success")
choose() >> [full_load, incremental_load] >> join
```

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

#### What is `@setup` and `@teardown`?

Decorators marking tasks that create and clean up resources (a cluster, a temporary table). A teardown runs even if the work in between fails, and clearing a task also reruns its setup and teardown.

<!-- challenge -->

A DAG creates a temporary cluster, runs three jobs on it and deletes it. When a job fails, the cluster stays up. Fix it.

<!-- solution -->

Mark the create task with `@setup` and the delete task with `@teardown`, linked to it. The teardown then runs whatever happens to the jobs, and the DAG run still reports the job failure.

<!-- takeaways -->

- Trigger rules decide which upstream states let a task run.
- Joins after branches need a rule that tolerates skips.
- Setup and teardown guarantee cleanup.

<!-- unit: Runtime limits and isolation -->

<!-- goals -->

- Bound how long and how often tasks and runs execute.
- Isolate dependencies and avoid unsafe shell commands.

<!-- concept -->

A task that hangs, overlaps with yesterday's run or clashes with Airflow's own libraries can do more damage than one that fails. Timeouts turn hangs into clear failures. Run limits and `depends_on_past` stop runs that modify the same data from overlapping. Isolated environments let a task use libraries Airflow can't install.

Shell commands are the easiest place to introduce injection and hidden logic, so keep them short and never template untrusted input into them.

<!-- example -->

```python
@task.virtualenv(requirements=["pandas==2.2.3"], system_site_packages=False,
                 execution_timeout=timedelta(minutes=30))
def score(path: str):
    import pandas as pd       # imports inside the function
    ...
```

#### How do you set a timeout on a task?

With `execution_timeout` (a `timedelta`); the task fails when it runs longer. A DAG-level `dagrun_timeout` fails the whole run after a duration.

#### What does `max_active_runs` do?

It limits how many runs of a DAG can be active at once. Setting it to 1 ensures runs happen sequentially, which matters for pipelines that depend on the previous run's output.

#### What is `depends_on_past`?

A task argument: if `True`, a task instance runs only if the same task succeeded (or was skipped) in the previous DAG run. It enforces sequential processing at task level.

#### How do you run a task in an isolated Python environment?

With `@task.virtualenv` (creates a virtualenv with given requirements), `@task.external_python` (uses an existing interpreter), `@task.docker` or `@task.kubernetes` (runs in a container). This avoids dependency conflicts with Airflow itself.

#### What is the `BashOperator` used for, and what is the risk?

Running shell commands or scripts. The risk is templating untrusted input into the command (injection), and hiding complex logic in shell where it's hard to test.

<!-- challenge -->

A daily DAG updates running totals from the previous day. Yesterday's run was slow, today's started anyway, and totals are now wrong. What two settings prevent this?

<!-- solution -->

Set `max_active_runs=1` so runs never overlap, and `depends_on_past=True` on the update task so it waits for the previous day's instance to succeed. Add `execution_timeout` so a hang fails loudly instead of blocking forever.

<!-- takeaways -->

- Timeouts turn silent hangs into visible failures.
- `max_active_runs` and `depends_on_past` enforce order between runs.
- Isolate conflicting dependencies; keep shell commands short.

<!-- unit: Keeping DAG files healthy -->

<!-- goals -->

- Keep DAG parsing fast and predictable.
- Generate DAGs and tasks dynamically without surprises.

<!-- concept -->

Airflow re-reads DAG files constantly, so a DAG file is code that runs far more often than its tasks. Anything at the top level (a database query, an API call, a heavy import) runs on every parse and slows scheduling for everyone.

Dynamic generation is powerful as long as the inputs are cheap and stable, such as a YAML file in the repository. Stability matters because IDs are identity: a renamed task or DAG starts a new history.

<!-- example -->

```python
# tables.yaml lives next to the DAG: cheap to read at parse time
for table in yaml.safe_load(open(CONFIG))["tables"]:
    @task(task_id=f"load_{table}")
    def load(name=table): ...
    load()
```

#### Why should DAG files be lightweight at the top level?

The DAG processor parses every DAG file repeatedly (every 30 seconds by default for changed files). Top-level code such as database queries, API calls, `Variable.get()` or heavy imports runs on every parse, slowing the whole scheduler and hitting external systems. Put such work inside tasks.

#### How do you generate DAGs or tasks dynamically?

Loop in Python over a configuration (a list, a YAML file read from disk) to create tasks or several DAGs at parse time, or use dynamic task mapping for runtime fan-out. Keep the configuration static and cheap to read so parsing remains fast and deterministic.

#### What happens when you rename a task or a DAG?

Airflow treats it as a new task or DAG: history stays under the old name. In Airflow 3, DAG versioning shows the change, but renaming still breaks continuity for metrics and `depends_on_past`.

<!-- challenge -->

A DAG file builds its task list by querying the warehouse for all tables at the top level. Scheduling became slow. What do you change?

<!-- solution -->

Move the query out of parse time: write the table list to a config file during CI or a separate task, read that file at parse time, or use dynamic task mapping so a task fetches the list at runtime.

<!-- takeaways -->

- Top-level code runs on every parse; keep it trivial.
- Generate tasks from cheap, versioned configuration.
- Task and DAG IDs are identity; renaming starts a new history.

<!-- stage: Scheduling and data flow -->

### Scheduling and time

<!-- unit: Schedules and timetables -->

<!-- goals -->

- Express schedules with cron, presets, timedeltas and timetables.
- Handle time zones and daylight saving changes.

<!-- concept -->

A schedule answers one question: when should a new run be created? Cron strings and presets cover most cases. When the rule depends on a calendar (business days, holidays, fiscal months), a timetable expresses it in Python instead of a run that starts and then skips itself.

Time zones add a subtlety. Airflow stores everything in UTC, but people think in local time. A DAG with a local time zone follows the local clock, which means some local times happen twice or not at all on daylight saving days.

<!-- example -->

```python
import pendulum
@dag(schedule="0 6 * * 1-5",                     # 06:00 Monday to Friday
     start_date=pendulum.datetime(2026, 1, 1, tz="America/Bogota"),
     catchup=False)
def weekday_report(): ...
```

#### How do you schedule a DAG?

With the `schedule` argument: a cron expression (`"0 6 * * *"`), a preset (`"@daily"`, `"@hourly"`), a `timedelta`, a timetable, a list of assets (event-driven), or `None` for manual or externally triggered DAGs.

#### What is the `@once` preset?

A schedule that creates a single run, useful for one-off DAGs such as migrations.

#### How do you run a DAG only on business days?

Use a cron expression such as `0 6 * * 1-5`, or a custom timetable if holidays matter. A branch or short-circuit task can also skip processing on holidays from a calendar table.

#### What is a timetable?

A class that defines a custom schedule when cron isn't enough: business days only, several times on different days, fiscal calendars. Built-ins include `CronDataIntervalTimetable`, `CronTriggerTimetable`, `DeltaDataIntervalTimetable` and `MultipleCronTriggerTimetable`.

#### How does Airflow handle time zones?

Internally everything is stored in UTC. You can give a DAG a time-zone-aware `start_date` (with `pendulum`), and cron schedules then follow that time zone, including daylight saving changes. The UI can display local time.

#### How do daylight saving time changes affect schedules?

With a time-zone-aware start date, a daily cron at 02:30 can be skipped or run twice on transition days, depending on the local clock. Schedule critical jobs outside the 01:00–03:00 window or in UTC.

<!-- challenge -->

A European team schedules a report at 02:30 local time. Twice a year it misbehaves. What happens, and what do you suggest?

<!-- solution -->

On the spring change 02:30 doesn't exist, and in autumn it happens twice, so the run is skipped or duplicated depending on the clock. Schedule outside the transition window (for example 04:00) or in UTC if the business accepts it.

<!-- takeaways -->

- Cron and presets cover most schedules; timetables cover calendars.
- Airflow stores UTC; time-zone-aware start dates follow local time.
- Avoid scheduling inside daylight saving transition hours.

<!-- unit: Logical dates and data intervals -->

<!-- goals -->

- Explain why a daily run starts after the day it processes.
- Use the data interval instead of the current time in tasks.

<!-- concept -->

Scheduled runs are about data periods, not wall-clock moments. A daily run covers one complete day, so it can only start once that day is over, which is why it looks "one day late". The run's logical date and data interval tell a task which period it owns.

That design is what makes reruns correct: a task that reads its interval from the context processes the same data whenever it runs. A task that asks for the current time processes a different period on every retry or backfill.

<!-- example -->

```sql
-- templated SQL: always the run's own day
DELETE FROM sales_daily WHERE sale_date = '{{ ds }}';
INSERT INTO sales_daily
SELECT * FROM raw_sales
WHERE sold_at >= '{{ data_interval_start }}' AND sold_at < '{{ data_interval_end }}';
```

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

#### Why shouldn't tasks use `datetime.now()`?

Because reruns and backfills would process the wrong period. Use the logical date or data interval from the context or templates.

#### How do you pass the previous successful run's date into a task?

Use the template variables `prev_data_interval_start_success` and `prev_data_interval_end_success` (or `prev_start_date_success`), useful for incremental loads that should continue from the last successful point.

#### What happens if a run takes longer than the schedule interval?

The next run starts when it's due if `max_active_runs` allows it, so runs can overlap. Set `max_active_runs=1` (and possibly `depends_on_past=True`) when runs must not overlap.

<!-- challenge -->

An hourly DAG filters `WHERE updated_at > now() - interval '1 hour'`. After an outage, reruns load nothing. Rewrite the filter's logic.

<!-- solution -->

Filter on the run's interval: `updated_at >= data_interval_start AND updated_at < data_interval_end`, passed through templates. Each rerun then reloads exactly its own hour, regardless of when it runs.

<!-- takeaways -->

- A run processes its data interval, after the interval ends.
- Read dates from the context, never from the clock.
- Long runs can overlap; limit active runs when that matters.

<!-- unit: Backfills, reruns and idempotency -->

<!-- goals -->

- Choose between catchup, backfills, clearing and manual triggers.
- Make tasks idempotent so reprocessing is safe.

<!-- concept -->

Pipelines are rerun all the time: after bugs, outages, late data or logic changes. Airflow offers several ways to rerun, from clearing a single task to backfilling months, but all of them assume the same thing: running a task twice for the same interval leaves the same result.

That property, idempotency, comes from how you write the load, not from Airflow. Overwrite or merge the interval's slice instead of appending, and use the interval instead of the clock. Then reprocessing becomes a routine operation instead of a cleanup project.

<!-- example -->

```bash
# reprocess Q1 with at most 4 concurrent runs
airflow backfill create --dag-id sales_load \
  --from-date 2026-01-01 --to-date 2026-03-31 --max-active-runs 4
```

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

#### You need to reprocess six months of data after a bug fix. How?

Make sure tasks are idempotent and use the data interval, then create a backfill for the date range with limited concurrency (`max_active_runs`) so production isn't starved, or clear the affected DAG runs. Monitor and validate outputs afterwards.

#### Your backfill runs created duplicates in the target table. What went wrong?

Tasks weren't idempotent: they appended data or used "now" instead of the data interval. Rewrite the load to overwrite the interval's partition or `MERGE` on keys, delete the duplicates, and rerun.

<!-- challenge -->

A task appends each day's orders to a table with `INSERT INTO`. You must rerun last week. What do you change first?

<!-- solution -->

Make the load idempotent: delete the interval's rows and insert in one transaction, use `MERGE` on the order key, or overwrite the date partition. Then backfill the week with limited concurrency.

<!-- takeaways -->

- Catchup is automatic; backfills and clears are explicit.
- Idempotency comes from overwrite or merge by interval.
- Make loads idempotent before you backfill.

### Operators, sensors and deferrable tasks

<!-- unit: Sensors and cross-DAG waits -->

<!-- goals -->

- Configure sensors with the right mode and timeout.
- Choose between pull-style and push-style dependencies across DAGs.

<!-- concept -->

Pipelines often wait for things outside their control: a file, a partition, another team's DAG. Sensors turn that wait into a task with a success condition. The cost is a worker slot for as long as the wait lasts, unless the sensor releases it between checks.

Across DAGs you can wait (a sensor in the downstream DAG pulls) or trigger (an operator in the upstream DAG pushes). Pulling keeps teams independent but couples schedules; pushing removes the wait but makes the upstream DAG know its consumers.

<!-- example -->

```python
wait = S3KeySensor(
    task_id="wait_for_orders",
    bucket_key="s3://landing/orders/{{ ds }}/_SUCCESS",
    mode="reschedule", poke_interval=300, timeout=6 * 3600,
)
```

#### What is a sensor?

A special operator that waits for a condition: a file in S3 (`S3KeySensor`), a partition, an external task, a SQL query returning rows, an HTTP endpoint, a time. It checks periodically until the condition is true or the timeout expires.

#### What is the difference between `poke` and `reschedule` modes?

In `poke` mode the sensor holds a worker slot for its whole wait, sleeping between checks. In `reschedule` mode it releases the slot between checks and is rescheduled later, which is better for long waits. Deferrable mode is better still.

#### What is a sensor timeout, and why set it?

The maximum time a sensor waits before failing (`timeout`, default seven days). Set it to something realistic so a missing upstream file is noticed quickly instead of blocking resources for days. `soft_fail=True` marks the sensor skipped instead of failed.

#### What is `@task.sensor`?

A decorator that turns a Python function into a sensor: it returns `True` (or a `PokeReturnValue`) when the condition is met, with the usual `poke_interval`, `timeout` and `mode` options.

#### What is `ExternalTaskSensor`?

A sensor that waits for a task or DAG run in another DAG to reach a state, for the same logical date by default. It creates cross-DAG dependencies but couples schedules; assets are often a cleaner alternative.

#### What is `TriggerDagRunOperator`?

An operator that triggers another DAG, optionally passing configuration and waiting for it to finish. It is a push-style dependency, as opposed to the pull-style `ExternalTaskSensor`.

<!-- challenge -->

Twenty sensors in `poke` mode wait up to seven days each for partner files. Workers are often full. What do you change?

<!-- solution -->

Switch the sensors to deferrable mode, or `reschedule` at least, so they release worker slots while waiting. Lower the timeout to a realistic window, such as six hours, and alert when it expires.

<!-- takeaways -->

- Sensors wait for conditions; their mode decides the slot cost.
- Always set a realistic timeout.
- Cross-DAG links can pull (sensor) or push (trigger).

<!-- unit: Deferring instead of waiting -->

<!-- goals -->

- Explain how deferrable operators free worker slots.
- Handle inputs that may never arrive.

<!-- concept -->

Most waiting needs no CPU: checking a job status every minute is cheap, but holding a worker process for it is not. Deferrable operators hand the wait to the triggerer, an asynchronous service that can watch thousands of conditions at once, and resume on a worker only when something happened.

Deferring fixes cost, not semantics. You still decide what absence means: fail and alert, or skip because no data is a valid outcome.

<!-- example -->

```python
run = DatabricksRunNowOperator(
    task_id="run_job", job_id=1234,
    deferrable=True,          # waits in the triggerer, not on a worker
)
```

#### What are deferrable operators?

Operators that, while waiting for something external (a job, a file, a time), suspend themselves and hand the wait to an asynchronous trigger running in the triggerer process, freeing the worker slot. When the trigger fires, the task resumes on a worker. Many provider operators have `deferrable=True`.

#### What is the triggerer?

A component that runs asyncio-based triggers for deferred tasks. One triggerer can handle thousands of waits concurrently with little resource use.

#### A sensor waits for a file that sometimes never arrives. How do you handle it?

Make the sensor deferrable or use `reschedule` mode, give it a realistic timeout, decide whether the absence should fail (alert someone) or skip (`soft_fail`), and notify the source owner. Document the expected arrival time.

<!-- challenge -->

Deferrable tasks stay in the `deferred` state forever after an upgrade. Which component do you check first?

<!-- solution -->

The triggerer. Deferred tasks resume only when a running triggerer fires their trigger, so check that the triggerer service is deployed, healthy and has the providers installed, then look at its logs.

<!-- takeaways -->

- Deferring moves waits from workers to the triggerer.
- The triggerer must run for deferred tasks to resume.
- Decide explicitly whether missing input fails or skips.

<!-- unit: Data and API operators -->

<!-- goals -->

- Run SQL and HTTP calls from Airflow with connections.
- Know when transfer operators help and when they hurt.

<!-- concept -->

Many tasks are thin wrappers around a call to another system: run this SQL, call that API, copy this file. Provider operators do the call and reuse a connection for credentials, so the task needs only parameters, often templated with the run's dates.

The risk is pulling data through the worker. Transfer operators are fine for modest volumes, but large moves should run inside the systems themselves, such as `COPY` in the warehouse or an Athena `UNLOAD`.

<!-- example -->

```python
SQLExecuteQueryOperator(
    task_id="build_daily",
    conn_id="warehouse",
    sql="sql/build_daily.sql",                 # templated with {{ ds }}
)
```

#### How do you call a SQL database from Airflow?

With `SQLExecuteQueryOperator` (common SQL provider) and a connection, or with the provider-specific hook in a Python task. Keep SQL in separate `.sql` files referenced through templates.

#### What are transfer operators?

Operators that move data between two systems in one task, such as `S3ToRedshiftOperator`, `GCSToBigQueryOperator`, `SqlToS3Operator` or `S3ToSnowflakeOperator`. They usually delegate the work to the target system (for example a `COPY` command).

#### What is `HttpOperator` used for?

Calling HTTP APIs with a connection for the base URL and credentials, with optional response checks and pagination. `HttpSensor` waits for an endpoint to return a condition.

#### How do you run an Athena query from Airflow?

With `AthenaOperator`, which submits the query, waits for completion and writes results to the configured S3 output location. Use templated dates in the query to process the data interval.

<!-- challenge -->

A `SqlToS3Operator` exports a 200 GB table every night and the worker runs out of memory. What do you change?

<!-- solution -->

Let the database do the export: use its native unload or export command (for example `UNLOAD` in Redshift or a `COPY INTO` location in Snowflake) from a SQL operator. The worker then only issues the command and waits.

<!-- takeaways -->

- Operators plus connections keep tasks to parameters.
- Keep SQL in versioned, templated files.
- Large data moves belong inside the data systems.

<!-- unit: Triggering external engines -->

<!-- goals -->

- Trigger Databricks, dbt, Glue and Kubernetes work from Airflow.
- Combine several engines in one pipeline.

<!-- concept -->

Airflow is strongest as the conductor of other engines. Each engine has an operator that submits work, waits (ideally deferred) and reports success or failure, so the DAG reads like a plan while the computation happens elsewhere.

When the work has dependencies that Airflow's environment can't hold, running it in a container (a pod or a virtualenv) isolates it. The design question is always the same: what is the unit of retry, and where do the logs live?

<!-- example -->

```python
glue = GlueJobOperator(task_id="ingest", job_name="orders_ingest", deferrable=True)
spark = DatabricksRunNowOperator(task_id="enrich", job_id=1234, deferrable=True)
dbt = DbtTaskGroup(group_id="marts", project_config=ProjectConfig(DBT_DIR))  # Cosmos
glue >> spark >> dbt
```

#### How do you trigger a Databricks job from Airflow?

With `DatabricksRunNowOperator` (run an existing job by ID, passing parameters) or `DatabricksSubmitRunOperator` (submit a one-off run), from the Databricks provider, usually in deferrable mode so the wait doesn't hold a worker. `DatabricksWorkflowTaskGroup` can define a Databricks job from Airflow.

#### How do you run dbt from Airflow?

With a `BashOperator` calling `dbt build`, with a dbt Cloud operator (`DbtCloudRunJobOperator`), or with Astronomer Cosmos, which turns each dbt model into an Airflow task with dependencies from the dbt graph.

#### How do you run an AWS Glue job from Airflow?

With `GlueJobOperator` from the Amazon provider, passing the job name and script arguments, preferably with `deferrable=True` or `wait_for_completion` with a `GlueJobSensor`.

#### How do you run work on Kubernetes from Airflow?

With `KubernetesPodOperator` or `@task.kubernetes`, which start a pod with a given image, command, resources and secrets for each task. Each task gets its own dependencies and resources.

#### What is `PythonVirtualenvOperator` used for?

Running a function with dependencies that conflict with Airflow's, in a fresh virtualenv per run (slower) or a cached one. The function must be self-contained because it runs in another interpreter.

#### How would you orchestrate a pipeline across AWS Glue, Databricks and a dbt project?

One DAG (or asset-linked DAGs) using the Amazon provider's `GlueJobOperator`, the Databricks provider's `DatabricksRunNowOperator` and Cosmos or the dbt Cloud operator, all in deferrable mode, passing table names or paths, with data quality checks between steps and a single alerting setup.

<!-- challenge -->

A dbt project runs as one `BashOperator` calling `dbt build`. One failed model forces a two-hour rerun. What do you suggest?

<!-- solution -->

Run dbt with Cosmos, which turns models into tasks, or split `dbt build` by selectors into several tasks. A failure then retries only the affected models and their descendants, and each model's logs appear on its own task.

<!-- takeaways -->

- Engine operators submit, wait and report; Airflow doesn't compute.
- Use deferrable mode for long external jobs.
- Choose task granularity so retries stay small.

<!-- unit: Writing your own operators -->

<!-- goals -->

- Write a custom operator with templated fields.
- Use helper tasks and callbacks without side effects.

<!-- concept -->

When the same pattern appears in many DAGs, a custom operator packages it: parameters in the constructor, work in `execute`, and a list of fields Airflow renders with Jinja. Anything that touches external systems belongs in `execute`, not the constructor, because constructors run at parse time.

Smaller tools complete the picture. Empty tasks make graphs readable, and callbacks add logging or notifications around execution, as long as they stay fast and never decide the task's outcome.

<!-- example -->

```python
class PartitionCheckOperator(BaseOperator):
    template_fields = ("table", "partition")

    def __init__(self, table: str, partition: str, **kwargs):
        super().__init__(**kwargs)
        self.table, self.partition = table, partition

    def execute(self, context):
        rows = WarehouseHook().count(self.table, self.partition)
        if rows == 0:
            raise AirflowException(f"{self.table}/{self.partition} is empty")
```

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

#### What is `on_execute_callback`?

A callback called just before a task executes, used for logging or notifications. Like the other callbacks, it should be quick and must not fail the task.

<!-- challenge -->

A custom operator opens a database connection in `__init__`. The scheduler slows down and the database shows hundreds of idle connections. Why?

<!-- solution -->

`__init__` runs every time the DAG file is parsed, so each parse opens a connection. Move the connection into `execute`, through a hook, so it opens only when the task actually runs.

<!-- takeaways -->

- Put external calls in `execute`, never in `__init__`.
- List templatable parameters in `template_fields`.
- Keep callbacks fast and free of business logic.

### XCom and passing data

<!-- unit: Passing values with XCom -->

<!-- goals -->

- Pass small values between tasks with XCom and TaskFlow.
- Read XComs in templates and split dictionary outputs.

<!-- concept -->

Tasks often need a small piece of information from an earlier task: a file path, a row count, a job ID. XCom stores that value with the task instance so later tasks can read it. TaskFlow hides the mechanics: calling a task function returns a placeholder for its future value, and passing it on wires both the data and the dependency.

Classic operators read the same values through templates, so both styles share one mechanism.

<!-- example -->

```python
@task(multiple_outputs=True)
def extract() -> dict:
    return {"path": "s3://lake/orders/2026-10-17.parquet", "rows": 18233}

out = extract()
load(out["path"])                                   # TaskFlow
SQLExecuteQueryOperator(task_id="log", conn_id="wh",
    sql="INSERT INTO audit VALUES ({{ ti.xcom_pull(task_ids='extract', key='rows') }})")
```

#### What is XCom?

"Cross-communication": a mechanism to pass small values between tasks. A task pushes a value (TaskFlow return values are pushed automatically) and downstream tasks pull it. Values are stored in the metadata database by default.

#### What is `XComArg`?

The object returned when you call a TaskFlow function or access `.output` on an operator. It represents a future value and carries the dependency, so passing it to another task links the two.

#### How do you pull an XCom in a template?

```jinja2
{{ ti.xcom_pull(task_ids='extract', key='return_value') }}
```

With TaskFlow, you simply pass the output of one task function as an argument to another.

#### What does `multiple_outputs=True` do?

On a `@task` returning a dictionary, it pushes each key as a separate XCom, so downstream tasks can use `result["key"]` individually.

<!-- challenge -->

A task returns a list of 2 million IDs and the next task reads it. The UI is slow and the database grows fast. What do you change?

<!-- solution -->

Write the IDs to object storage or a staging table and return only its path or table name through XCom. The next task reads the data from there.

<!-- takeaways -->

- XCom carries small values between tasks.
- TaskFlow passes XComs and dependencies in one call.
- Templates read the same values for classic operators.

<!-- unit: XCom limits and backends -->

<!-- goals -->

- Keep large data out of the metadata database.
- Avoid serialization and retention problems.

<!-- concept -->

The default XCom backend is the metadata database, which is built for state, not data. Large values slow the scheduler and UI and eventually hit size limits. A custom backend moves values to object storage and keeps only a reference, which helps, but the healthier habit is to pass references yourself.

Values must also survive serialization, and they stay around until someone cleans them, so retention is part of database hygiene.

<!-- example -->

```ini
# airflow.cfg: store XCom values above 1 MB in S3, keep a reference in the database
[common.io]
xcom_objectstorage_path = s3://airflow-xcom/
xcom_objectstorage_threshold = 1048576
```

#### Why shouldn't you pass large data through XCom?

The default backend stores values in the metadata database, which isn't designed for large payloads, and serialized values have size limits. Pass references instead (an S3 path, a table name, a partition) and keep the data in storage.

#### What is a custom XCom backend?

A pluggable backend that stores XCom values elsewhere (S3, GCS, Azure Blob) and keeps only a reference in the database. The Common IO provider offers an object storage backend with a size threshold.

#### How do you avoid serialization errors with XCom?

Return JSON-serializable values (or types Airflow serializes, like dataclasses and pandas DataFrames with the right serializer); avoid open connections, generators or large objects. Return paths or IDs instead.

#### Are XComs deleted after a run?

They stay in the database (and are cleared when a task is cleared and rerun) until you purge them with `airflow db clean` or a retention policy. That's another reason to keep them small.

<!-- challenge -->

A task returns a database cursor and fails with a serialization error. What should it return instead?

<!-- solution -->

Fetch the results inside the task and return JSON-serializable data, such as a list of dicts if small. If large, write it to storage and return the path. Open handles like cursors can't cross tasks.

<!-- takeaways -->

- The metadata database is not a data store.
- Pass references (paths, table names) for large data.
- Return serializable values and clean old XComs.

<!-- unit: Context, templates and mapping -->

<!-- goals -->

- Use the task context and Jinja templates for run-specific values.
- Create tasks at runtime with dynamic task mapping.

<!-- concept -->

Every task instance knows where it stands: its run, its interval, its try number. That knowledge reaches your code through the context in Python and through Jinja templates in operator fields, rendered just before execution.

Dynamic task mapping uses the same idea for the shape of the graph. Instead of fixing the number of tasks at parse time, a mapped task expands over a list produced at runtime, such as the files that arrived today, and each element becomes its own retryable instance.

<!-- example -->

```python
@task
def list_files(ds=None) -> list[str]:
    return S3Hook().list_keys("landing", prefix=f"orders/{ds}/")

@task(max_active_tis_per_dagrun=5)
def load(key: str): ...

load.expand(key=list_files())
```

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

<!-- challenge -->

A mapped task over 300 files overloads the target database. How do you keep the mapping but protect the database?

<!-- solution -->

Cap concurrency with `max_active_tis_per_dagrun`, or assign the mapped task to a pool with a few slots. Each file still gets its own task instance and retries.

<!-- takeaways -->

- The context and templates give tasks their run's dates and IDs.
- Mapping sizes the graph at runtime with `.expand()`.
- Limit mapped concurrency with task limits or pools.

### Assets and event-driven scheduling

<!-- unit: Data-aware scheduling -->

<!-- goals -->

- Schedule DAGs on asset updates instead of times.
- Combine assets and timetables in one schedule.

<!-- concept -->

Time-based schedules guess when data will be ready. Assets remove the guess: a producing task declares that it updates a piece of data, and consuming DAGs run when that happens. Dependencies then describe data, not clocks, and the UI shows who feeds whom.

Conditions can combine several assets with and/or logic, or mix assets with a timetable when consumers need both freshness and a guaranteed daily run.

<!-- example -->

```python
orders = Asset("s3://lake/silver/orders/")

@task(outlets=[orders])
def build_orders(): ...

@dag(schedule=[orders])                 # runs after each successful build
def orders_report(): ...
```

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

#### Can a DAG be triggered both on a schedule and by assets?

Yes, with `AssetOrTimeSchedule`, which runs on a timetable and also whenever the asset condition is met.

#### What is the `@asset` decorator?

An Airflow 3 shortcut that defines an asset together with the single-task DAG that materializes it, for asset-centric authoring similar to Dagster.

<!-- challenge -->

A report DAG runs at 07:00 and uses an `ExternalTaskSensor` on the 06:00 load DAG. Loads sometimes move to 06:30. How do you decouple them?

<!-- solution -->

Declare the load task's table as an asset outlet and schedule the report on that asset. The report runs whenever the load succeeds, with no schedule alignment and no sensor holding a slot.

<!-- takeaways -->

- Assets schedule consumers on data updates.
- Conditions combine assets with and/or, or with a timetable.
- The assets view makes cross-DAG lineage visible.

<!-- unit: Asset events and external triggers -->

<!-- goals -->

- Understand what an asset event does and doesn't guarantee.
- Trigger DAGs from external events without polling.

<!-- concept -->

An asset event means a producing task succeeded, nothing more. Airflow never looks at the data, so a task that can succeed without writing must avoid emitting the event, and events can carry metadata such as the partition written so consumers know what changed.

Events can also come from outside Airflow. Asset watchers attach a trigger to a message queue, so a file landing in storage can start a DAG within seconds and without a sensor in sight.

<!-- example -->

```python
queue = MessageQueueTrigger(queue="https://sqs.eu-west-1.amazonaws.com/123/landing-events")
landing = Asset("s3://landing/orders/", watchers=[AssetWatcher(name="sqs", trigger=queue)])

@dag(schedule=[landing])
def ingest_orders(): ...
```

#### Do assets know whether the data actually changed?

No. Airflow only knows that a producing task succeeded; it doesn't inspect the data. If a task can succeed without writing anything, it should not emit the event, or the consumer must check.

#### Can you attach metadata to an asset event?

Yes. A producing task can add extra information (for example the row count or the partition written) to the asset event through outlet events, and consumers can read it from the triggering events in their context.

#### How do you see asset lineage in the UI?

The assets view shows each asset with its producing and consuming DAGs and the history of events, making cross-DAG dependencies visible.

#### What is an asset alias?

A placeholder used when the exact asset URI is only known at runtime: the task emits events for an alias and attaches the concrete asset, and consumers can schedule on the alias.

#### What are asset watchers?

An Airflow 3 feature for event-driven scheduling from external systems: an `AssetWatcher` attaches a trigger (for example on a message queue such as SQS or Kafka) to an asset, so a DAG runs when an external event arrives, not only when another Airflow task updates the asset.

#### How do you trigger an Airflow DAG when a file lands in S3, with no polling?

Use an asset watcher on an SQS queue that receives S3 event notifications (Airflow 3), or an S3 event that triggers a Lambda function calling the Airflow REST API to trigger the DAG with the file path as configuration.

<!-- challenge -->

A producing task succeeds even when its source is empty, and downstream DAGs rerun for nothing. How do you stop it?

<!-- solution -->

Check the row count in the task and skip it (raise a skip exception) when there is nothing new, so no asset event is emitted. Optionally attach the row count to events for consumers.

<!-- takeaways -->

- An asset event only means the producer succeeded.
- Event metadata tells consumers what changed.
- Watchers trigger DAGs from queues without polling.

<!-- stage: Running Airflow -->

### Executors and architecture

<!-- unit: Choosing an executor -->

<!-- goals -->

- Compare Local, Celery, Kubernetes and Edge executors.
- Match an executor to workload shape and team skills.

<!-- concept -->

The executor decides where task code physically runs. The choice is a trade-off between start-up speed and isolation. Long-lived workers start tasks quickly but share an environment and must be sized for peak load. One pod per task starts slower but gives each task its own image and resources, and costs nothing when idle.

Since you can combine executors, the choice is no longer all-or-nothing: most tasks on fast workers, special ones in pods or on remote edge workers.

<!-- example -->

```ini
[core]
executor = CeleryExecutor,KubernetesExecutor
```
```python
@task(executor="KubernetesExecutor")      # this task alone runs in its own pod
def train_model(): ...
```

#### What is an executor?

The component that decides how and where task instances run. The scheduler sends queued tasks to the executor, which runs them locally or dispatches them to workers.

#### What executors are available?

`LocalExecutor` (parallel processes on the scheduler machine), `CeleryExecutor` (a pool of workers fed by a message broker such as Redis or RabbitMQ), `KubernetesExecutor` (one pod per task), and provider executors such as the AWS ECS and Batch executors and the Edge executor for remote workers. Airflow 2.10+ can use several executors at once.

#### When would you choose the CeleryExecutor?

For many short tasks with steady load: long-running workers start tasks quickly. You need to operate a broker and scale workers yourself (or with KEDA).

#### When would you choose the KubernetesExecutor?

When tasks need different resources or images, isolation matters, and load is spiky: each task runs in its own pod and resources are released afterwards. Pod start-up adds seconds of latency per task.

#### What is the role of the message broker with Celery?

Redis or RabbitMQ holds the queue of tasks sent by the scheduler; Celery workers consume from it. A result backend (usually the database) stores task states.

#### What is the `pod_template_file`?

A Kubernetes pod specification used by the KubernetesExecutor (and KubernetesPodOperator) as the base for task pods: image, resources, volumes, node selectors, service account. Tasks can override parts with `executor_config`.

#### Can you use several executors at once?

Yes, since Airflow 2.10: configure a list of executors and assign tasks to one with the `executor` argument, for example most tasks on Celery and heavy, isolated ones on Kubernetes.

#### What is the Edge executor?

An executor (from the Edge3 provider) that runs tasks on remote workers that connect to the Airflow API over HTTP, for example in another network or data center, without direct database access.

<!-- challenge -->

Your platform runs 5,000 short SQL tasks a day and a few GPU training jobs each week. Which executor setup do you propose?

<!-- solution -->

CeleryExecutor for the short SQL tasks, so they start fast on warm workers, plus KubernetesExecutor for the training tasks, assigned per task, so GPU nodes are used only when needed.

<!-- takeaways -->

- Workers start fast; pods isolate and scale to zero.
- Celery needs a broker; Kubernetes needs pod templates.
- Multiple executors let each task run where it fits.

<!-- unit: Scheduler and DAG processor -->

<!-- goals -->

- Describe what the scheduler and DAG processor do in each loop.
- Make the scheduling layer highly available and secure.

<!-- concept -->

Scheduling is a loop over the database: find runs that are due, find task instances whose dependencies are met, and hand them to the executor within the limits. Parsing user code is a separate job, done by the DAG processor, so a slow or broken DAG file can't stall scheduling.

Because state lives in the database, high availability is simple: run several schedulers and they coordinate with row locks. In Airflow 3, workers also stop reading the database and ask the API server for what they need, which narrows what a task can see.

<!-- example -->

```text
DAG files ─► DAG processor ─► serialized DAGs ─┐
                                               ▼
 scheduler ×2 ─ row locks ─► metadata DB ◄─ API server ◄─ workers (Task Execution API)
```

#### What does the scheduler do?

It reads serialized DAGs, creates DAG runs when due, checks which task instances have their dependencies met, respects concurrency limits and pools, and sends tasks to the executor. Several schedulers can run at once for high availability.

#### What does the DAG processor do?

It parses DAG files and stores serialized DAGs in the database. In Airflow 3 it is a separate component, so user code never runs inside the scheduler.

#### How do you make the scheduler highly available?

Run two or more schedulers against the same PostgreSQL or MySQL database; they coordinate with row-level locks. Run several API servers behind a load balancer and several triggerers.

#### How do workers get credentials in Airflow 3?

Through the Task Execution API: tasks request connections, variables and XComs from the API server instead of reading the metadata database, which improves security and allows remote workers.

<!-- challenge -->

A single scheduler VM failed overnight and nothing ran until morning. What do you propose so this doesn't happen again?

<!-- solution -->

Run at least two schedulers (on different nodes) against a managed PostgreSQL with backups, and alert on the scheduler heartbeat metric. Run the DAG processor separately so parsing problems don't take the schedulers down.

<!-- takeaways -->

- The scheduler loops over the database; the DAG processor parses code.
- Several schedulers give high availability through row locks.
- Airflow 3 workers talk to the API server, not the database.

<!-- unit: Concurrency, pools and priorities -->

<!-- goals -->

- Use concurrency settings, pools and priorities to share capacity.
- Protect shared systems from overload and conflicting writes.

<!-- concept -->

Capacity is limited at several levels: the whole installation, each DAG, each task, and each pool. When tasks compete, priority weights decide who goes first. These knobs don't just tune speed; they express rules about the systems tasks touch.

A pool with few slots is the simplest way to say "no more than four queries against production at once", and a pool with one slot serializes writers that must never overlap.

<!-- example -->

```python
# pool "orders_table" created with 1 slot: writers take turns
MERGE_A = SQLExecuteQueryOperator(task_id="merge_a", pool="orders_table", ...)
MERGE_B = SQLExecuteQueryOperator(task_id="merge_b", pool="orders_table", ...)
```

#### What concurrency settings exist?

`parallelism` (max running tasks per scheduler), `max_active_tasks_per_dag`, `max_active_runs_per_dag`, pool slots, per-task `max_active_tis_per_dag`, and executor-specific settings such as Celery worker concurrency.

#### What is a pool?

A named limit on concurrent task slots, used to protect a shared resource: for example a pool of 4 slots for tasks that query a production database. Tasks are assigned to a pool and can consume several slots.

#### What is priority weight?

A number that decides which queued tasks run first when slots are limited. The weight rule (`downstream`, `upstream`, `absolute`) controls how it accumulates across the graph.

#### What are queues in the CeleryExecutor?

Named queues that workers subscribe to. Assigning tasks to a queue (`queue="gpu"`) routes them to workers with suitable resources.

#### Two DAGs write to the same table and sometimes conflict. How do you fix it?

Serialize them: one pool with one slot for writes to that table, or merge them into one DAG with explicit order, or make one depend on the other through an asset. Better still, give each table one owner process.

<!-- challenge -->

A nightly batch of 200 tasks delays the morning's critical finance DAG. How do you make sure finance runs first?

<!-- solution -->

Give the finance tasks a higher `priority_weight` (with an `absolute` weight rule) so they win slots when queued, and put the batch in a pool with a slot limit so it can't take all workers.

<!-- takeaways -->

- Limits exist per installation, DAG, task and pool.
- Pools protect shared systems and serialize conflicting writes.
- Priority weights decide who gets scarce slots.

### Configuration, security and secrets

<!-- unit: Configuration and secrets -->

<!-- goals -->

- Configure Airflow with files and environment variables.
- Keep credentials in a secrets backend, encrypted and masked.

<!-- concept -->

Airflow's configuration has layers: the config file, environment variables that override it, and secrets that should never live in either. Connections and variables can come from the database, environment variables or a secrets manager; Airflow checks those sources in order, so production can keep secrets in a vault while development uses local variables.

Defense goes further: values stored in the database are encrypted with the Fernet key, and logs and the UI mask anything that looks like a secret.

<!-- example -->

```bash
export AIRFLOW__CORE__PARALLELISM=64
export AIRFLOW__SECRETS__BACKEND=airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend
export AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "airflow/connections"}'
```

#### How is Airflow configured?

Through `airflow.cfg`, overridden by environment variables named `AIRFLOW__SECTION__KEY` (for example `AIRFLOW__CORE__PARALLELISM`). Environment variables are the usual approach in containers.

#### How do you define connections as environment variables?

With `AIRFLOW_CONN_<CONN_ID>` set to a URI or JSON, for example `AIRFLOW_CONN_WAREHOUSE='postgresql://user:pass@host:5432/db'`. They don't appear in the UI, and they take precedence over a connection with the same ID in the database (a configured secrets backend is checked first).

#### What is a secrets backend?

An integration that reads connections and variables from an external secrets manager: AWS Secrets Manager or SSM Parameter Store, HashiCorp Vault, Google Secret Manager, Azure Key Vault. Secrets don't have to be stored in the metadata database.

#### What is the Fernet key?

The key used to encrypt connection passwords and variable values in the metadata database. It must be set, kept secret and identical on all components; rotating it requires re-encrypting.

#### How does Airflow avoid showing secrets in logs and the UI?

It masks values of connection passwords, variables whose names contain words like `password`, `secret` or `token`, and values registered with `mask_secret()`. Masking is best-effort, so don't print secrets.

<!-- challenge -->

A connection password appears in plain text in a task log because the task printed a URL containing it. How do you prevent this?

<!-- solution -->

Stop printing the URL, register the value with Airflow's secret masker if it's built at runtime, and rotate the leaked password. Prefer secrets backends so values aren't copied into variables with names the masker doesn't recognize.

<!-- takeaways -->

- Environment variables override `airflow.cfg`.
- Secrets backends keep credentials in a vault.
- Encryption and masking protect, but code can still leak.

<!-- unit: Access and identity -->

<!-- goals -->

- Control who can see and trigger which DAGs.
- Give tasks cloud access without long-lived keys.

<!-- concept -->

Two identities matter in Airflow: the people using the UI and the code running on workers. People get roles that limit which DAGs they can see or trigger. Code runs with the workers' permissions, which is the harder problem, because anyone who can deploy a DAG can make it read any connection.

So control access at deployment (reviews, separate deployments per team) and give workers short-lived cloud identities instead of stored keys.

<!-- example -->

```python
@dag(access_control={"finance-ops": {"DAGs": {"can_read", "can_edit"}}},
     schedule="@daily", start_date=datetime(2026, 1, 1))
def finance_close(): ...
```

#### How is access to the UI controlled?

Through an auth manager. Airflow 3 ships a simple auth manager for development; the FAB auth manager provides role-based access control (Admin, Op, User, Viewer and custom roles), and managed services integrate with cloud IAM.

#### How do you restrict who can trigger a DAG?

With role-based access control: give roles permissions on specific DAGs (by DAG ID or via `access_control` in the DAG), so a team can trigger and clear its own DAGs only.

#### How should DAG code access cloud resources?

Through the worker's identity (IAM role for service accounts on Kubernetes, MWAA execution role, workload identity) wherever possible, rather than long-lived keys stored in connections.

#### Why is it risky to let many users edit DAG code?

DAG code runs with the workers' permissions and can read connections, so anyone who can deploy DAGs effectively has access to every connection. Code review and CI gates on the DAG repository are part of security.

<!-- challenge -->

Ten teams share one Airflow deployment, and one team's DAGs need access to payroll data. What do you propose?

<!-- solution -->

Give payroll its own deployment (or at least its own workers with a separate cloud role and secrets path), restrict its DAGs with RBAC, and require code review on that repository. Shared workers would expose payroll credentials to every team's code.

<!-- takeaways -->

- RBAC controls people; worker identity controls code.
- Deploying DAG code means access to its connections.
- Prefer workload identities over stored cloud keys.

<!-- stage: Production -->

### Testing and code quality

<!-- unit: Testing DAGs and task logic -->

<!-- goals -->

- Write integrity and structure tests for DAGs.
- Unit test business logic and operators without a full Airflow.

<!-- concept -->

A DAG can fail in three places: at import, in its structure, or in the logic of its tasks. Each needs a different test. Import and structure tests load the DAGs and assert they parse and have the expected shape. Logic tests treat task code like any Python module, which is easy only if the logic lives outside the DAG file.

Operators that call external systems are tested twice: with mocked hooks for their logic, and against local containers for real behavior.

<!-- example -->

```python
def test_dags_import():
    bag = DagBag(include_examples=False)
    assert bag.import_errors == {}

def test_sales_structure():
    dag = DagBag().get_dag("sales_load")
    assert dag.get_task("extract").downstream_task_ids == {"transform"}
```

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

#### How do you test that a DAG has the right structure?

Load it from a `DagBag` and assert task IDs, dependencies (`task.downstream_task_ids`), schedules and settings, so accidental changes to the graph are caught.

#### How do you unit test task logic?

Keep business logic in plain Python functions or modules outside the DAG file, test them with pytest without Airflow, and keep tasks as thin wrappers. For operators, test `execute()` with mocked hooks.

#### How do you check templated fields render correctly?

Render them for a given context in a test (`ti.render_templates()`), or run `airflow tasks render dag_id task_id date`, and check the rendered SQL or command.

#### How do you test custom operators with external systems?

Mock the hook in unit tests to check the operator's logic and parameters, and run integration tests against local containers (Postgres, LocalStack for AWS, MinIO for S3) in CI.

<!-- challenge -->

All the transformation logic of a DAG is written inline in five `@task` functions, and nobody tests it. How do you make it testable?

<!-- solution -->

Move the logic into a module of plain functions that take and return data, test those with pytest, and keep the tasks as thin wrappers that read inputs, call the functions and write outputs.

<!-- takeaways -->

- Test imports, structure and logic separately.
- Logic outside DAG files is easy to unit test.
- Mock hooks for unit tests; use containers for integration.

<!-- unit: Local runs and CI -->

<!-- goals -->

- Run DAGs and single tasks locally for debugging.
- Assemble a CI pipeline for an Airflow repository.

<!-- concept -->

Fast feedback comes from running small pieces locally: a whole DAG in one process with a debugger, or one task for one date. Local environments should match production images, or "works on my machine" problems reappear in deployment.

CI then automates the same checks on every change, from linting to integrity tests, and a staging environment runs real data for a small date range before production.

<!-- example -->

```yaml
# CI steps for an Airflow repository
- run: ruff check dags/ --select AIR
- run: pytest tests/unit tests/dags
- run: docker build -t airflow:${{ github.sha }} .
```

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

#### What should a CI pipeline for an Airflow repository run?

Linting (Ruff with `AIR` rules), unit tests for business logic, DAG integrity tests (`DagBag` import errors, conventions, cycles), parse-time checks, image build, and deployment to staging, with production deployment after merge or approval.

<!-- challenge -->

A broken import reached production and the DAG disappeared from the UI. Which CI check would have caught it, and how cheap is it?

<!-- solution -->

A DAG integrity test that loads every file with `DagBag` and asserts no import errors. It runs in seconds in CI, inside the same image as production so missing packages are caught too.

<!-- takeaways -->

- `dag.test()` and `airflow tasks test` give fast local feedback.
- Ruff `AIR` rules catch deprecated and Airflow 3 issues.
- CI runs lint, unit and integrity tests on every change.

### Deployment and operations

<!-- unit: Shipping DAGs -->

<!-- goals -->

- Deploy DAG code and dependencies reproducibly.
- Roll back a bad deployment quickly.

<!-- concept -->

A deployment has two parts that must match: the environment (Airflow, providers, Python packages) and the DAG code. Building both into one image makes every environment identical. Shipping DAGs separately, through git-sync, bundles or an S3 bucket, is faster but invites mismatches between code and installed packages.

Whatever the method, deployments should come from CI and be reversible by redeploying the previous version.

<!-- example -->

```dockerfile
FROM apache/airflow:3.1.0-python3.12
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.1.0/constraints-3.12.txt"
COPY dags/ /opt/airflow/dags/
```

#### How do you deploy DAGs?

Most teams build a Docker image with Airflow, providers, dependencies and DAG code, and deploy it through CI/CD to Kubernetes (Helm chart) or a managed service. Alternatives: syncing DAGs from Git with git-sync or to an S3 bucket (MWAA). DAG bundles in Airflow 3 can read DAGs directly from Git with versioning.

#### What is a DAG bundle?

An Airflow 3 concept for a collection of DAG files from a source such as a local folder or a Git repository, which lets Airflow track versions of DAG code and run a DAG run with the code version it started with.

#### What is the official Helm chart?

The Apache Airflow Helm chart, which deploys all components on Kubernetes with options for executors, git-sync, PgBouncer, KEDA autoscaling, logging and secrets. It's the standard self-hosted Kubernetes deployment.

#### How do you deploy to Amazon MWAA?

Upload DAGs to the environment's S3 bucket (usually via CI with `aws s3 sync`), and manage `requirements.txt`, plugins and a startup script in S3; the environment's Airflow version and size are set in its configuration. The execution role grants AWS access.

#### How do you roll back a bad DAG deployment?

Redeploy the previous image or Git commit through CI. With DAG versioning in Airflow 3, existing runs keep their version. Then clear failed runs if needed.

#### A DAG works locally but tasks fail in production with "module not found". Why?

The production image or workers lack the dependency, or the module isn't on the path (for example code outside the DAGs or plugins folder). Add it to the image's requirements or package, and build local and production from the same image.

<!-- challenge -->

A deploy broke three DAGs at 02:00. Write the first three steps of your rollback.

<!-- solution -->

Redeploy the previous image or commit through CI. Check the import errors list is empty and the DAGs are back. Then clear the failed task instances so they rerun on the old code, and open a fix-forward ticket.

<!-- takeaways -->

- Ship code and dependencies together when possible.
- Deploy from CI; roll back by redeploying the previous version.
- "Module not found" usually means the image and code diverged.

<!-- unit: Upgrades and dependencies -->

<!-- goals -->

- Upgrade Airflow versions safely, including 2 to 3.
- Pin dependencies with constraints files.

<!-- concept -->

Airflow sits on hundreds of Python packages, and a small change in one provider can change operator behavior. Constraints files pin a known-good set for each Airflow and Python version, so upgrades become deliberate events instead of side effects of a rebuild.

Major upgrades add database migrations and API changes. The safe path is incremental: reach the last minor version, fix warnings, test in staging with a database backup, then move.

<!-- example -->

```bash
pip install "apache-airflow[amazon,databricks]==3.1.0" \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.1.0/constraints-3.12.txt"
ruff check dags/ --select AIR3     # find Airflow 3 incompatibilities
airflow db migrate
```

#### How do you upgrade Airflow safely?

Read the release notes, upgrade in a test environment first, use the constraints files to pin compatible dependencies, run `airflow db migrate`, check DAGs for deprecations (Ruff `AIR` rules for Airflow 3), and back up the metadata database before migrating production.

#### What are constraints files?

Pinned dependency lists published for each Airflow and Python version, used with `pip install "apache-airflow==X" --constraint <url>` to get a known-good set of packages.

#### Why pin provider and dependency versions?

Unpinned upgrades can change operator behavior or break imports silently. Pin versions with the constraints file and upgrade deliberately with tests.

#### How would you migrate from Airflow 2 to Airflow 3?

Upgrade to the latest 2.x first and fix deprecation warnings, run Ruff's `AIR3` rules to find code to change (imports to `airflow.sdk`, `schedule_interval` to `schedule`, `execution_date` to `logical_date`, removed SubDAGs and SLAs, no direct database access in tasks), test in a staging environment, migrate the database, and update deployment for the API server and DAG processor.

<!-- challenge -->

A rebuild of the image without changes made a provider upgrade itself, and an operator now behaves differently. How do you prevent it?

<!-- solution -->

Pin Airflow and all providers in `requirements.txt` and install with the matching constraints file, so rebuilds are reproducible. Upgrade providers deliberately in a branch, with tests and release notes reviewed.

<!-- takeaways -->

- Constraints files make installs reproducible.
- Pin providers; upgrade them on purpose.
- For majors: last minor first, fix warnings, test, back up, migrate.

<!-- unit: Monitoring and alerting -->

<!-- goals -->

- Collect logs and metrics from Airflow and its tasks.
- Design alerts that reach the right people with the right context.

<!-- concept -->

Two kinds of signals matter. Platform signals (scheduler heartbeat, queue sizes, parse times) say whether Airflow works. Pipeline signals (task failures, late runs) say whether data arrives. Each needs a different audience: the platform team and the data owners.

Good alerts carry context and point to a runbook. Alerts that fire every night for known flaky tasks train people to ignore them, so fixing root causes is part of alerting, not separate from it.

<!-- example -->

```python
def notify_failure(context):
    ti = context["ti"]
    send_slack(f":red_circle: {ti.dag_id}.{ti.task_id} failed ({context['ds']}) "
               f"owner={ti.task.owner} log={ti.log_url}")

default_args = {"on_failure_callback": notify_failure}
```

#### Where do task logs go?

By default to local files on workers, shown in the UI. In production, configure remote logging to S3, GCS, Azure Blob, Elasticsearch or CloudWatch so logs survive pod restarts.

#### How do you monitor Airflow?

With StatsD or OpenTelemetry metrics (scheduler heartbeat, DAG parse time, queued and running tasks, task durations, pool usage) in Prometheus/Grafana or Datadog, health endpoints, and alerts on failures and on runs that take too long.

#### How do you get alerted on task failures?

With callbacks (`on_failure_callback`, `on_retry_callback`, `on_success_callback`) that send to Slack, email or PagerDuty, the notifier classes from providers, or email settings. Alert on the DAG level for actionable, non-duplicated messages.

#### What replaced SLAs in Airflow 3?

SLAs (`sla` and `sla_miss_callback`) were removed because they were unreliable. Airflow 3.1 introduced deadline alerts, which trigger a callback when a DAG run hasn't finished by a deadline relative to a reference time. Until then, teams used `execution_timeout`, `dagrun_timeout` and external monitoring.

#### What should a runbook for a failed DAG contain?

What the DAG does and who owns it, upstream dependencies, how to check logs and inputs, which tasks are safe to clear and rerun, how to backfill, who to notify, and known failure modes with fixes.

#### Your on-call engineer is paged every night for the same flaky task. What do you change?

Find the root cause in logs (timeouts, resource limits, upstream lateness), add appropriate retries with backoff only for transient errors, add a sensor or asset dependency if it starts before its input is ready, raise resources or move it to a dedicated pool, and change alerts to fire only after retries are exhausted.

<!-- challenge -->

A finance DAG must finish by 08:00, but nobody notices when it runs late without failing. What do you set up?

<!-- solution -->

Add a deadline alert (Airflow 3.1+) on the DAG run for 08:00 that notifies the owners, or a separate check that alerts if the run hasn't succeeded by then. Include the run link and runbook in the message.

<!-- takeaways -->

- Ship logs remotely; export metrics to a monitoring system.
- Alert owners with context and a runbook link.
- Fix flaky tasks so alerts stay meaningful.

<!-- unit: Troubleshooting stuck and dying tasks -->

<!-- goals -->

- Diagnose tasks stuck in `queued` and zombie tasks.
- Find the cause when tasks die without an error.

<!-- concept -->

When a task never starts or dies silently, the problem is usually below your code. A queued task waits for a slot that some limit or a missing worker never provides. A task that disappears without a traceback was usually killed from outside, often for memory, and the scheduler later notices the missing heartbeat.

So debugging starts with the platform: limits, workers, pod events and memory metrics, before the task code.

<!-- example -->

```bash
kubectl get events -n airflow --field-selector reason=OOMKilling
kubectl describe pod sales-load-transform-abc12 | grep -A3 "Last State"
#   Last State: Terminated  Reason: OOMKilled  Exit Code: 137
```

#### What are common causes of tasks stuck in `queued`?

No free slots (parallelism, pool or DAG concurrency limits), workers down or not consuming the queue, the executor not able to start pods (quota, image pull errors), or a scheduler problem. Check pools, worker logs and executor events.

#### What are zombie tasks?

Task instances marked as running whose process died without reporting (worker crash, OOM kill, pod eviction). The scheduler detects missing heartbeats and fails or retries them.

#### Tasks are often killed with no error in the logs. What do you suspect?

Out-of-memory kills (OOM) of the worker or pod, evictions, or timeouts. Check pod events and worker metrics, raise memory limits, and move heavy processing out of Airflow.

<!-- challenge -->

After a release, many tasks stay `queued` while workers look idle. List three things to check.

<!-- solution -->

Check whether workers consume the right queue (a renamed queue strands tasks), whether a pool or DAG concurrency limit is full, and whether the executor can start pods (quotas, image pull errors). Scheduler logs usually name the limit.

<!-- takeaways -->

- `queued` means a limit or worker problem, not code.
- Zombies come from processes that died without reporting.
- Exit code 137 or no traceback: suspect memory.

<!-- unit: Scaling and database health -->

<!-- goals -->

- Scale schedulers, workers and the database as DAG count grows.
- Keep parse times and database size under control.

<!-- concept -->

Airflow's limits usually appear in this order: parsing, then the database, then workers. Parse time grows with every DAG file and every heavy import. The database grows with every run and XCom, and every task opens connections to it. Workers are the easiest part to scale, so fix the first two before adding machines.

Most scaling work is hygiene: light DAG files, pooled database connections, periodic cleanup and deferrable waits.

<!-- example -->

```bash
airflow dags report                                # parse time per file
airflow db clean --clean-before-timestamp "$(date -d '-90 days' +%F)" --yes
```

#### How do you scale Airflow?

Run several schedulers, scale workers (autoscaling Celery workers with KEDA, or Kubernetes executor), use deferrable operators to free slots, reduce DAG parse time, tune `parallelism` and pools, and keep heavy computation outside Airflow.

#### Why is DAG parse time important?

Slow parsing delays scheduling for all DAGs and consumes CPU. Measure it with `airflow dags report`; fix it by removing top-level work, avoiding heavy imports at module level, and splitting giant generated DAG files.

#### How do you keep the metadata database healthy?

Use a managed PostgreSQL with backups, monitor its size, and run `airflow db clean` periodically to purge old task instances, logs metadata and XComs. A huge database slows the scheduler and UI.

#### Why use PgBouncer with Airflow?

Each task and component opens database connections; many concurrent tasks can exhaust PostgreSQL's connection limit. PgBouncer pools them. In Airflow 3 the Task Execution API reduces direct connections from workers.

#### Hundreds of DAGs are slow to schedule. What do you investigate?

DAG parse times (`airflow dags report`), top-level code and imports, the number of DAG files, scheduler CPU and database performance, the number of task instances in the database (run `db clean`), and whether the scheduler and DAG processor have enough resources or replicas.

#### Your scheduler's CPU is at 100%. What are typical fixes?

Reduce DAG parsing load (fewer, lighter files, longer `min_file_process_interval`, separate DAG processor), move away from sensors in poke mode, clean the database, add scheduler replicas, and check for DAGs with huge numbers of mapped tasks.

<!-- challenge -->

The metadata database reached 400 GB and the UI takes 30 seconds to load. What do you do first, and what do you schedule?

<!-- solution -->

Back up, then run `airflow db clean` to purge old task instances, XComs and logs metadata beyond your retention. Schedule the same cleanup weekly (as a maintenance DAG) and check for large XComs that should be references.

<!-- takeaways -->

- Fix parsing and the database before adding workers.
- PgBouncer pools the many connections tasks open.
- Clean old metadata on a schedule.

### Best practices

<!-- unit: Orchestrate, don't process -->

<!-- goals -->

- Size tasks so they are meaningful and cheap to retry.
- Split pipelines into DAGs along schedules and ownership.

<!-- concept -->

Airflow works best as a thin layer of control over systems that do the work. Tasks that process data on the worker compete for memory with everything else and can't scale. The right size for a task is a unit you'd want to retry on its own, and the right size for a DAG is one schedule and one owner.

Because tasks may run on different machines, anything passed between them must live in shared storage, not on local disk.

<!-- example -->

| Too coarse | Right size | Too fine |
|---|---|---|
| `run_everything` (2 h, retries all) | `load_orders`, `build_orders_mart` | one task per SQL statement |

#### Should Airflow do the data processing itself?

No. Airflow should orchestrate: trigger Spark, SQL engines, dbt, Databricks or containers that do the processing, and pass references. Heavy pandas work on Airflow workers competes with other tasks and is hard to scale.

#### What makes a good task granularity?

Each task should be a meaningful, retryable unit (extract one source, load one table, run one model group). Too coarse means retrying lots of work; too fine adds scheduling overhead and makes the graph unreadable.

#### Why should DAGs avoid relying on local files between tasks?

Tasks can run on different workers or pods, so a file written by one task may not exist for the next. Use object storage, a shared volume or a database instead.

#### How many DAGs should a pipeline be split into?

One DAG per independent schedule and ownership boundary. Split when parts have different schedules, owners or failure domains, and connect them with assets; keep tightly coupled steps in one DAG.

<!-- challenge -->

One DAG loads marketing, finance and product data at 06:00, owned by three teams. Failures in one block the others. How do you restructure it?

<!-- solution -->

Split it into one DAG per domain, each owned and alerted separately. Where one domain needs another's data, connect the DAGs with assets so they run when the data is ready.

<!-- takeaways -->

- Airflow orchestrates; engines process.
- A task is a retryable unit; a DAG is a schedule and an owner.
- Share data through storage, not worker disks.

<!-- unit: Safe retries and data checks -->

<!-- goals -->

- Configure retries that help transient errors without hiding bugs.
- Add data quality checks as gates in a DAG.

<!-- concept -->

Retries are cheap insurance against flaky networks and busy APIs, but only when tasks are idempotent and errors are transient. Retrying a bug three times only delays the alert. Backoff and pools turn retries from a stampede into polite waiting.

Data checks are the other half of reliability: a task can succeed and still produce wrong data. Checks placed between load and publish stop bad data before consumers see it.

<!-- example -->

```python
SQLColumnCheckOperator(
    task_id="check_orders", conn_id="warehouse", table="silver.orders",
    column_mapping={"order_id": {"null_check": {"equal_to": 0}, "unique_check": {"equal_to": 0}}},
)
```

#### How do you make retries safe?

Make tasks idempotent, set `retries` and `retry_delay` (with `retry_exponential_backoff`) for transient errors, and fail fast (no retries) for errors that retrying can't fix, such as bad credentials or a data quality failure.

#### A task fails randomly on an API's rate limit. What do you do?

Add retries with exponential backoff, put the API calls in a pool limiting concurrency, respect `Retry-After` in the hook, and reduce calls (batching, incremental extraction).

#### How do you handle data quality checks in Airflow?

With SQL check operators (`SQLColumnCheckOperator`, `SQLTableCheckOperator`, `SQLCheckOperator`), Great Expectations or Soda operators, or dbt tests, placed after loads to stop downstream tasks when data is wrong.

<!-- challenge -->

A load task retries five times on a schema mismatch and finally fails two hours later. What do you change?

<!-- solution -->

Fail fast on non-transient errors: catch schema errors and raise a failure that skips retries, keeping retries with backoff only for timeouts and throttling. Add a schema check before the load.

<!-- takeaways -->

- Retry transient errors with backoff; fail fast on bugs.
- Pools and backoff protect rate-limited systems.
- Gate publishing with data quality checks.

<!-- unit: Organizing code and configuration -->

<!-- goals -->

- Organize shared code, configuration and naming across DAGs.
- Keep DAGs readable for the next person on call.

<!-- concept -->

A repository with fifty DAGs needs the same structure as any codebase. Shared logic lives in a tested package, not copied between files. Configuration splits by how often it changes: structure in code, per-environment values in variables, credentials in secrets.

Readability is an operational concern. The person reading a DAG at 3 a.m. didn't write it, so consistent names, small tasks and documentation decide how fast they can act.

<!-- example -->

```text
dags/
  sales__daily_load.py      # thin: schedule, tasks, dependencies
  finance__month_close.py
include/
  common/warehouse.py       # shared, tested code
tests/
```

#### Where should configuration live?

In code (versioned) for structure, in environment variables or Variables for environment-specific values, and in a secrets backend for credentials. Avoid many Variables read at parse time.

#### How do you name DAGs and tasks?

Consistently and descriptively: `domain__purpose` for DAGs (`sales__daily_load`), verbs for tasks (`extract_orders`, `load_orders`), with owners and tags for teams and data domains.

#### How do you handle shared code between DAGs?

Put it in a Python package (in the repository's `include/` or `plugins/` path, or installed into the image) with its own tests, rather than copying code between DAG files.

#### How do you keep a DAG readable?

Small tasks with clear names, task groups for logical blocks, no business logic in the DAG file, documentation with `doc_md`, consistent use of TaskFlow or operators, and limited dynamic generation.

<!-- challenge -->

Five DAGs each contain a copy of the same 80-line function to load files into the warehouse, with small differences. What do you do?

<!-- solution -->

Extract one parameterized function (or custom operator) into a shared package with tests, replace the copies, and capture the differences as parameters. Future fixes then happen once.

<!-- takeaways -->

- Shared code goes in a tested package.
- Structure in code, environment values in variables, credentials in secrets.
- Consistent names and docs speed up incident response.

<!-- unit: Extending Airflow and lineage -->

<!-- goals -->

- Know what plugins and listeners can add to Airflow.
- Emit lineage with OpenLineage.

<!-- concept -->

Airflow has extension points for what operators can't do. Plugins add UI views, macros or timetables. Listeners react to events such as a task finishing, which makes them the natural place for cross-cutting concerns like lineage, audit or custom metrics.

OpenLineage builds on listeners: providers describe each task's inputs and outputs, and a backend assembles a lineage graph across tools, not just inside Airflow.

<!-- example -->

```bash
pip install apache-airflow-providers-openlineage
export AIRFLOW__OPENLINEAGE__TRANSPORT='{"type": "http", "url": "http://marquez:5000"}'
```

#### What are plugins used for in Airflow?

Extending Airflow with custom UI views, menu links, macros, listeners, timetables and, in Airflow 3, FastAPI apps and React views. Custom operators and hooks don't need to be plugins; regular Python modules work.

#### What are listeners?

Hooks into Airflow events (DAG run started or finished, task instance state changes) implemented with pluggy, used for lineage (OpenLineage), auditing or custom notifications.

#### What is OpenLineage in Airflow?

A standard for lineage metadata. The OpenLineage provider emits events describing inputs and outputs of tasks to a backend such as Marquez or a data catalog, so you can see which jobs read and write which datasets.

<!-- challenge -->

Compliance asks which dashboards depend on a customer table loaded by Airflow. How could lineage answer this automatically?

<!-- solution -->

Enable the OpenLineage provider so tasks emit input and output datasets, send events to a lineage backend that also receives events from dbt and BI tools, and query the downstream graph of the customer table.

<!-- takeaways -->

- Plugins extend the UI and scheduling; listeners react to events.
- OpenLineage emits task inputs and outputs automatically.
- Lineage answers impact questions across tools.

<!-- stage: Putting it together -->

### Scenarios

<!-- unit: Designing a daily ELT DAG -->

<!-- goals -->

- Combine sensors, loads, dbt and checks into one daily DAG.
- Justify each choice in an interview answer.

<!-- concept -->

Design questions test whether you can connect the pieces: when the data is ready, how it gets loaded idempotently, how transformations run, how failures surface. A strong answer follows the data and names one tool per step, then explains what happens on rerun and who gets alerted. Mentioning deferrable waits, interval-based loads and per-model dbt tasks shows you know the production pitfalls.

<!-- example -->

```text
wait_for_files (deferrable S3KeySensor, timeout 6h)
  ─► copy_into_snowflake (interval's prefix, idempotent)
  ─► dbt models (Cosmos task group)
  ─► data checks ─► asset event: marts.sales
```

#### A daily DAG must load yesterday's files from S3 into Snowflake, then run dbt. Design it.

A DAG scheduled daily with `catchup=False` (or true if history matters), a deferrable `S3KeySensor` on the expected prefix for the data interval, a `CopyFromExternalStageToSnowflakeOperator` or SQL task running `COPY INTO`, then dbt through Cosmos or a dbt Cloud operator, data quality checks, and failure callbacks to Slack. All paths and filters come from the data interval.

<!-- challenge -->

The source team says files may be corrected and re-sent up to three days later. Adjust the design.

<!-- solution -->

Process the last three intervals each run, or trigger reruns on new files with asset watchers. Make the Snowflake load replace each day's slice (delete and insert, or `MERGE`) so corrections overwrite, and let dbt rebuild the affected days.

<!-- takeaways -->

- Follow the data from arrival to consumers, one tool per step.
- Idempotent, interval-based loads make reruns safe.
- Finish with checks, alerts and what consumers get.

<!-- unit: Gating a report on data quality -->

<!-- goals -->

- Trigger a report only when its inputs are complete and correct.
- Decide what happens when the gate fails.

<!-- concept -->

Business users care about a report being right more than it being on time. A good design makes completeness explicit: the report depends on the data, not on a clock, and a check compares what arrived with what was expected before anything is sent. When the check fails, the right behavior is to tell someone and not send, rather than to email a wrong number.

<!-- example -->

```python
@dag(schedule=[Asset("snowflake://analytics/sales_daily")])
def sales_report():
    check = SQLCheckOperator(task_id="complete",
        conn_id="warehouse",
        sql="SELECT count(*) >= 0.95 * expected FROM sales_completeness WHERE day = '{{ ds }}'")
    check >> send_report()
```

#### A business user wants a report emailed only if yesterday's sales are complete. How?

Schedule the report DAG on the sales asset (or a sensor on the load), add a data quality check (row count and completeness compared with expected sources), short-circuit the email if checks fail, and alert the data team instead.

<!-- challenge -->

The check fails one morning because a single store didn't send data. The business still wants the report, labeled. What do you change?

<!-- solution -->

Make the check return which stores are missing, and branch: send the report with a "partial data" banner listing them, and alert the data owners. Keep a hard stop only when completeness falls below an agreed threshold.

<!-- takeaways -->

- Schedule reports on data, not on the clock.
- Check completeness before sending.
- Agree with users what partial data should produce.
