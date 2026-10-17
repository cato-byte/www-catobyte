## Testing and Performance in Big Data Pipelines

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Testing and performance in big data pipelines](../../images/testing_and_performance_big_data_title_img.png)

*Technical article*

## Two questions every pipeline must answer

A data pipeline has to answer two questions before anyone should trust it in production. Is it **right**: does it produce the correct data, every time, including on the strange inputs real sources send? And is it **fast and cheap enough**: does it finish within its window, at a cost the business accepts, as data grows?

Teams often treat these separately: correctness is the analysts' problem, performance is the platform team's problem. They're connected. Optimizing a pipeline without tests is gambling, because every performance change (a new join strategy, a different partitioning, an incremental load instead of a full rebuild) is a chance to change the results silently. And tests that can't run quickly on a laptop won't be run at all.

This article covers how I approach both, with PySpark and Delta Lake examples. Several of them come from my [EU company registry lakehouse](../projects/eu-company-registry.html), which has about 200 tests and runs end to end on a laptop before anything reaches Databricks.

## Part 1: proving the pipeline is right

### Why testing big data is different

Testing a web API and testing a data pipeline share principles, but data adds four complications:

- **The input is half the program.** Correct code can produce wrong data from a source that changed its format, shifted a column or sent half a file. Tests of code aren't enough; you also need tests of data.
- **State matters.** Pipelines write tables with history. A bug isn't fixed by redeploying; the data it wrote has to be repaired too.
- **Scale hides problems.** A join that works on 1,000 rows can explode on 50 million because of one hot key. Some failures only appear at volume.
- **Running for real is expensive.** "Deploy it and see" on a cluster costs money and minutes per attempt, so the feedback loop must be local.

So a good strategy has several layers, each catching a different class of problem.

| Layer | What it catches | Where it runs |
|---|---|---|
| Static checks | Anti-patterns, unsupported APIs, secrets | Pre-commit and CI, seconds |
| Unit tests | Wrong logic in parsing, cleaning, business rules | Laptop and CI, seconds |
| End-to-end tests on synthetic data | Wiring errors between stages, idempotency, history | Laptop and CI, minutes |
| Data quality checks | Bad or unexpected real data | Production, every run |
| Regression and reconciliation | Unintended changes in results, incomplete loads | CI on samples, production after loads |
| Performance checks | Plans and runtimes that degrade | CI (plan checks), periodic benchmarks |

### Design for testability

The single most useful habit is to **separate transformations from I/O**. A function that takes a DataFrame and returns a DataFrame can be tested with ten rows; a notebook cell that reads S3, transforms and writes a table can only be tested by running the whole thing.

```python
from pyspark.sql import DataFrame, functions as F
from pyspark.sql.window import Window

def latest_per_key(df: DataFrame, key: str, order_col: str) -> DataFrame:
    """Keep the most recent row per key."""
    w = Window.partitionBy(key).orderBy(F.col(order_col).desc())
    return df.withColumn("_rn", F.row_number().over(w)).filter("_rn = 1").drop("_rn")
```

Entry points (jobs, notebooks, Lambda handlers) stay thin: read configuration, call these functions, write results. Paths, dates and table names are parameters, never constants buried in the code.

### Unit tests with a local SparkSession

A session-scoped fixture gives every test the same small Spark instance, which keeps the suite fast:

```python
import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark():
    session = (SparkSession.builder.master("local[2]")
               .config("spark.sql.shuffle.partitions", "2")
               .config("spark.sql.ansi.enabled", "true")   # same behavior as production
               .getOrCreate())
    yield session
    session.stop()

def test_latest_per_key_keeps_newest(spark):
    from pyspark.testing import assertDataFrameEqual
    df = spark.createDataFrame(
        [(1, "old", "2026-10-01"), (1, "new", "2026-10-02"), (2, "only", "2026-10-01")],
        ["id", "value", "updated_at"])
    expected = spark.createDataFrame(
        [(1, "new", "2026-10-02"), (2, "only", "2026-10-01")],
        ["id", "value", "updated_at"])
    assertDataFrameEqual(latest_per_key(df, "id", "updated_at"), expected)
```

Two details matter. Configure the local session like production (here ANSI mode, which makes invalid casts fail instead of silently returning null), or tests will pass locally and fail in the cluster. And keep shuffle partitions low; the default of 200 makes tiny tests slow.

For column-level functions (parsing dates, cleaning postcodes, validating identifiers) I use a helper that evaluates a column expression over a list of inputs **in one Spark job**, so a test with fifty cases doesn't launch fifty jobs:

```python
def eval_col(spark, fn, values):
    """eval_col(spark, parse_int, ["5.0", "x"]) -> [5, None]"""
    df = spark.createDataFrame([(v,) for v in values], "value string")
    return [row[0] for row in df.select(fn(F.col("value"))).collect()]

def test_parse_postcode(spark):
    assert eval_col(spark, clean_postcode, [" 75001", "75-001", "", None]) == ["75001", "75001", None, None]
```

### Property-based tests for parsers

Hand-written examples cover the cases you thought of. Property-based testing (with Hypothesis) generates hundreds of inputs and checks properties that must always hold: a deduplicated output has unique keys; a cleaned identifier is either valid or null, never something in between; parsing then formatting a value returns the same value. It's particularly good at finding edge cases in parsers of messy text.

### Synthetic fixtures that look like the real thing

Real data can't go into a public repository, and shouldn't go into CI anyway. The answer is **synthetic fixtures that reproduce the quirks of the real files**: the same column names and order, the same encodings and separators, the same oddities (dates in three formats, identifiers with spaces, rows with missing fields, a JSON array instead of NDJSON). In the registry project, fixtures are generated from the shapes of the real files with new identifiers that still pass their check digits, so validation logic is exercised realistically.

### End-to-end tests: the whole pipeline on a laptop

The test I value most runs every stage, from landing files to published output, on those fixtures:

```python
@pytest.mark.e2e
def test_pipeline_end_to_end(spark, tmp_path):
    settings = Settings(landing_root=copy_fixtures(tmp_path), snapshot_date=date(2026, 7, 31),
                        publish_root=tmp_path / "publish")
    run_bronze(spark, settings)
    run_silver(spark, settings)
    run_gold(spark, settings)
    run_publish(spark, settings)

    silver = spark.table("silver.companies")
    assert silver.filter("is_current").groupBy("company_key").count().filter("count > 1").count() == 0
    assert (tmp_path / "publish" / "summary.json").exists()
```

It takes a few minutes and costs nothing. It catches the errors unit tests can't: a stage reading a column the previous stage renamed, a table written to the wrong schema, a merge condition that duplicates current rows. In my project it's literally "the test that replaces running it on Databricks and seeing what happens".

### Test idempotency and history explicitly

Pipelines are rerun all the time: retries after failures, backfills, accidental double triggers. A pipeline that appends blindly will duplicate data on every rerun. Make idempotency a test, not a hope:

```python
def test_rerun_on_same_input_changes_nothing(spark, settings):
    run_silver(spark, settings)
    version_before = spark.sql("DESCRIBE HISTORY silver.companies").first()["version"]
    run_silver(spark, settings)   # same input files
    version_after = spark.sql("DESCRIBE HISTORY silver.companies").first()["version"]
    assert version_after == version_before   # no new table version was written
```

For tables with history (SCD Type 2), test the lifecycle: a new entity gets one open row; a change closes the old version and opens a new one; an entity that disappears is closed; an older snapshot is refused rather than rewriting history backwards.

### Data quality checks in production

Tests on fixtures prove the code; they can't prove next month's file is sane. That's the job of data quality checks running on real data during every run. A simple, effective design gives each rule a **severity**:

- **Warning:** keep the row, count it, report it.
- **Error:** send the row to a quarantine table with the failed rules, continue with the rest.
- **Abort threshold:** if too many rows fail a rule, stop the run. When 1% of identifiers suddenly fail their checksum, the problem is structural (shifted columns, a new format), and loading the rest would be worse than stopping.

All rules can be evaluated in a single pass over the data:

```python
RULES = {
    # name: (severity, condition that must hold)
    "id_present":    ("error",   F.col("company_id").isNotNull()),
    "known_country": ("error",   F.col("country_code").isin("FR", "IE", "GB", "NO", "EE", "ES")),
    "has_postcode":  ("warning", F.col("postcode").isNotNull()),
}

failures = df.select(
    F.count("*").alias("rows"),
    *[F.sum(F.when(F.coalesce(cond, F.lit(False)), 0).otherwise(1)).alias(name)
      for name, (_, cond) in RULES.items()],
).first()
```

Add volume checks too. In the registry pipeline, a snapshot with fewer than 80% of the previous row count stops the run: that's what a truncated download looks like, and it's far cheaper to stop than to publish a map missing a fifth of a country.

Constraints at the table level are a last line of defense. Delta Lake `CHECK` constraints (valid statuses, `valid_to >= valid_from`, current rows have an open end date) make it impossible for a code regression to write an invalid state, because the write itself fails.

### Regression and reconciliation

When you change logic, compare outputs. On fixtures in CI, compare the new version's results with the previous version's (row counts, key aggregates, row-level diffs on a sample). In production, reconcile with sources after each load: row counts per snapshot, distinct keys, sums of amounts. Reconciliation turns "I think the load is complete" into evidence.

## Part 2: making it fast and affordable

### Measure before optimizing

Most slow pipelines are slow for one or two reasons, and guessing wastes days. Look at:

- **The Spark UI:** which stage takes the time, how its task durations are distributed (a long tail means skew), shuffle read and write sizes, and spill to disk.
- **The physical plan** (`df.explain(mode="formatted")`): are filters pushed down to the scan, are files pruned, which join strategy was chosen, is there an unexpected `CartesianProduct` or Python evaluation?
- **Cost per run**, not just duration. On Databricks, `system.billing.usage` gives the real DBUs of each run; in my project a small `cost_report` task records them after every run so estimates can be calibrated against reality.

### Where the time usually goes

In my experience, in roughly this order:

1. **Reading too much data.** Full scans instead of pruned reads, CSV or JSON instead of a columnar format, thousands of small files.
2. **Shuffles.** Joins and aggregations that move large amounts of data across the network.
3. **Skew.** A few keys (often `null` or a default value) holding most of the rows, so a few tasks run for an hour while the rest finish in seconds.
4. **Spill.** Partitions too large for executor memory, written to disk and read back.
5. **Python at the row level.** UDFs that serialize every row between the JVM and Python.
6. **Driver bottlenecks.** `collect()` or `toPandas()` on large data, or giant query plans.

### Data layout: read less

The cheapest byte is the one you never read.

- **Columnar formats** (Parquet, or Delta and Iceberg on top of it) let engines read only the needed columns and skip row groups using min/max statistics.
- **File sizes** of roughly 128 MB to 1 GB keep per-file overhead low. Streaming and frequent small appends create small files; compaction (`OPTIMIZE`) fixes them.
- **Partitioning or clustering** by the columns most queries filter on. On Delta, liquid clustering (`CLUSTER BY`) has largely replaced manual partitioning and Z-ordering; partition only very large tables on a low-cardinality column that almost every query uses, or you'll recreate the small-files problem.
- **Filters that prune.** A filter only prunes if it applies to the stored column directly. `WHERE to_date(event_ts) = '2026-10-15'` may scan everything; `WHERE event_date = '2026-10-15'` on a clustered or partitioned column won't.

### Joins: broadcast small, handle skew

When one side of a join is small (a dimension, a lookup table), broadcast it so the large side isn't shuffled:

```python
from pyspark.sql.functions import broadcast
enriched = facts.join(broadcast(dim_country), "country_code", "left")
```

Adaptive Query Execution (on by default in recent Spark) converts joins to broadcast when a side turns out small at runtime, coalesces small shuffle partitions and splits skewed ones. Let it work, and keep its settings enabled.

For skew that AQE can't fix, handle the hot keys separately or **salt** them: spread a hot key over several artificial sub-keys on the large side and replicate the small side accordingly.

```python
SALTS = 16
big = big.withColumn("salt", (F.rand() * SALTS).cast("int"))
small = small.crossJoin(spark.range(SALTS).withColumnRenamed("id", "salt"))  # small side only
joined = big.join(small, ["key", "salt"])
```

Often the real fix is upstream: a `null` join key that should have been filtered or mapped to an "unknown" member before the join.

### Patterns to ban from the codebase

Some anti-patterns are so common and so costly that it's worth catching them automatically rather than in code review. In the registry project a small AST-based linter runs in pre-commit, CI and the test suite, and flags, among others:

| Pattern | Why it hurts |
|---|---|
| `collect()` / `toPandas()` on unbounded data | Pulls everything to the driver |
| Python UDFs | Row-by-row serialization, invisible to the optimizer; built-ins almost always exist |
| `withColumn` inside a loop | Plan grows quadratically; use `withColumns` or one `select` |
| `crossJoin` | Cartesian product, almost always a bug |
| `repartition(1)` / `coalesce(1)` | Funnels all data through one task |
| `inferSchema` | Extra full scan, unstable types; declare schemas |
| `cache()` / `persist()` on serverless | Not supported there; write an intermediate table instead |

Each finding can be suppressed on one line with a written justification, which keeps the rules strict without blocking legitimate exceptions.

### Test the plan, not just the result

You can't run production-volume benchmarks on every pull request, but you can check the **shape of the query plan** on fixtures, cheaply and deterministically:

```python
import contextlib, io

def plan_of(df) -> str:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        df.explain(mode="formatted")
    return buffer.getvalue()

def test_gold_plan_is_safe(spark, silver_fixture):
    plan = plan_of(build_gold(silver_fixture))
    assert "BatchEvalPython" not in plan and "ArrowEvalPython" not in plan   # no Python UDFs
    assert "CartesianProduct" not in plan                                     # no accidental cross joins
    assert len(plan.splitlines()) < 400                                       # plan size stays bounded
```

These tests catch a performance regression the moment it's written, long before anyone notices a job taking twice as long.

### Process only what changed

The biggest savings rarely come from tuning a join. They come from **not doing work at all**:

- Load incrementally (Auto Loader, `COPY INTO`, CDC, watermarks) instead of rereading every file.
- Write with `MERGE` or `replaceWhere` for the affected period instead of rebuilding entire tables.
- Skip stages whose inputs haven't changed. The registry job's first task compares the newest landing files, the gazetteer and the geocoding results with what was last processed; if nothing changed, a condition task ends the run immediately, and if only France changed, only France is reprocessed. A test asserts that a rerun on the same files writes no new table version and no published file.

### Right-size the compute

Match compute to the workload: serverless or job clusters for scheduled pipelines (never interactive clusters), autoscaling within sensible limits, spot instances for fault-tolerant batch workers, auto-termination everywhere. Bigger isn't always more expensive: if a job parallelizes well, doubling the cluster halves the runtime at the same cost. If it doesn't, you're paying for idle cores, and the Spark UI's executor timeline will show it.

### Track performance over time

Performance degrades gradually as data grows. Keep a history of runtime, input size, shuffle volume and cost per run, and alert when a run takes much longer than its recent average. In Databricks jobs, a duration alert below the hard timeout gives you a warning before the job fails.

## A checklist for every pipeline

**Correctness**

- Transformations are pure functions with unit tests, run on a local session configured like production.
- Synthetic fixtures reproduce the real sources' quirks; no real personal data in the repository.
- An end-to-end test runs the whole pipeline on fixtures in minutes.
- Reruns are tested to be idempotent; history logic (SCD2) is tested through its lifecycle.
- Data quality rules have severities, quarantine and abort thresholds; volume drops stop the run.
- Table constraints enforce invariants; results are reconciled with sources.

**Performance and cost**

- Columnar formats, healthy file sizes, clustering on common filters, filters that prune.
- Small tables broadcast, skew handled, AQE enabled.
- Anti-patterns blocked by a linter; query plans checked in tests.
- Only changed data is processed; unchanged stages are skipped.
- Compute matches the workload; cost per run is measured and trended.

Testing and performance are the same discipline seen from two sides: knowing exactly what your pipeline does, so you can change it with confidence. A suite that runs in minutes on a laptop is what makes it safe to optimize; measurements are what tell you where optimizing is worth it.
