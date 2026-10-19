## PySpark Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![PySpark study guide: about 200 questions](../../images/pyspark_study_guide_title_img.png)

About 200 questions on PySpark for data engineering interviews: Spark's architecture, SparkSession and RDDs, DataFrames and column functions, aggregations, joins, window functions, Spark SQL, reading and writing data, partitioning and shuffles, the Catalyst optimizer and AQE, performance tuning, UDFs and pandas, Structured Streaming, testing, and hands-on practice problems. Examples target Spark 3.5 and 4.x.

The guide follows a learning path in five stages. Each section is split into short units: learning goals, a concept explanation and a worked example, then questions (recall first, then application), a practical challenge and key takeaways. To **learn**, read each unit top to bottom. To **review**, switch to review mode or use "Skip to questions", mark answers you want to see again, and try a mixed review across sections.

<!-- QA -->
<!-- stage: Foundations -->

### Spark fundamentals and architecture

<!-- unit: What Spark is -->

<!-- goals -->

- Explain what Spark and PySpark are and when they pay off.
- Know Spark Connect and what Spark 4.0 changed.

<!-- concept -->

Spark processes data that doesn't fit on one machine by splitting it into partitions and working on them in parallel across a cluster. PySpark lets you describe that work in Python, while the heavy lifting runs in Spark's JVM engine, so Python code mostly builds a plan rather than touching rows.

That split explains when Spark is worth it: large data, batch or streaming pipelines, wide transformations. For a few gigabytes, pandas or DuckDB on one machine is simpler and faster. Recent versions decouple clients from clusters and tighten SQL behavior.

<!-- example -->

```python
from pyspark.sql import SparkSession, functions as F
spark = SparkSession.builder.appName("daily_sales").getOrCreate()
sales = spark.read.parquet("s3://lake/sales/")              # nothing read yet
daily = sales.groupBy("sale_date").agg(F.sum("amount").alias("revenue"))
daily.write.mode("overwrite").parquet("s3://lake/marts/daily_sales/")   # runs now
```

#### What is Apache Spark?

A distributed processing engine for large-scale data. It splits data into partitions and processes them in parallel across a cluster, keeping intermediate results in memory where possible. It offers APIs in Python (PySpark), Scala, Java, R and SQL, and libraries for SQL, streaming and machine learning.

#### What is PySpark?

The Python API for Spark. Your Python code builds a query plan; the actual work runs on the JVM-based Spark engine. Only Python UDFs and pandas functions execute in Python worker processes, which is why built-in functions are faster than Python code.

#### Is PySpark faster than pure Python?

It depends on the size of the data. PySpark is usually faster for large datasets because it distributes the work across many nodes and processes partitions in parallel. For small data that fits comfortably on one machine, plain Python, pandas or Polars is often faster, because Spark adds scheduling, serialization and JVM overhead.

#### When shouldn't you use Spark?

For small datasets (up to a few gigabytes), low-latency single-row lookups, transactional workloads (OLTP) or simple jobs a database can do. A single-node engine such as DuckDB or Polars is often simpler and faster for data that fits on one machine.

#### What is Spark Connect?

A client-server architecture introduced in Spark 3.4. A thin client sends unresolved query plans to a remote Spark server over gRPC, so applications don't need a JVM or to run on the cluster. It's used by Databricks serverless and shared clusters; some low-level APIs, such as RDDs and `SparkContext`, aren't available through it.

#### What changed in Spark 4.0 that matters for PySpark?

ANSI SQL mode is on by default (invalid casts and overflows raise errors instead of returning null), there's a `VARIANT` type for semi-structured data, a Python data source API, improvements to Spark Connect, and Mesos support was removed. Code that relied on silent nulls from bad casts may need changes.

<!-- challenge -->

A team uses a 20-node Spark cluster to process a 2 GB CSV once a day, and jobs take 6 minutes, mostly startup. What do you suggest?

<!-- solution -->

Use a single-machine tool (pandas, Polars or DuckDB) or a small single-node Spark: 2 GB fits in memory, and cluster startup and coordination dominate the runtime. Keep Spark for data that grows past one machine.

<!-- takeaways -->

- Spark parallelizes work over partitions on a cluster.
- PySpark builds plans; the JVM engine executes them.
- Small data is faster on one machine.

<!-- unit: Lazy evaluation and the DAG -->

<!-- goals -->

- Explain transformations, actions and lazy evaluation.
- Distinguish narrow and wide transformations and what partitions are.

<!-- concept -->

Spark waits as long as it can. Transformations only record what you want; actions such as writing or counting trigger execution. Waiting lets Spark see the whole plan and optimize it, for example pushing filters to the source.

The plan is a graph of operations over partitions. Narrow operations like filters work on each partition independently; wide ones like grouping need rows with the same key together, which forces a shuffle across the cluster. Shuffles are where most cost and most tuning live.

<!-- example -->

```python
df = spark.read.parquet("events/")          # transformation (lazy)
clicks = df.filter(F.col("type") == "click") # narrow
by_user = clicks.groupBy("user_id").count()  # wide: shuffle by user_id
by_user.show(5)                              # action: the job runs here
```

#### What are the key Spark concepts every interview starts with?

- **Transformation:** an operation on a DataFrame or RDD that returns a new DataFrame or RDD (`filter`, `select`, `join`). It's lazy.
- **Action:** an operation that returns a value to the driver or writes data (`count`, `collect`, `show`, `write`). It triggers execution.
- **Catalyst optimizer:** the engine that analyzes all the transformations requested and works out the most efficient way to run them together.

#### What is lazy evaluation?

Transformations aren't executed when you call them; Spark only records them in a logical plan. When an action is called, Catalyst analyzes the whole chain of transformations and builds an optimized execution plan. This lets Spark combine steps, push filters down to the source and skip unnecessary columns.

#### What is the DAG?

The directed acyclic graph of operations Spark builds from your transformations. The scheduler uses it to determine stages, dependencies and what can run in parallel, and to recompute lost partitions after a failure.

#### What is the difference between narrow and wide transformations?

**Narrow** transformations compute each output partition from a single input partition, so no data moves between executors: `filter`, `select`, `map`, `union`, `withColumn`. **Wide** transformations need data from many partitions, which requires a shuffle: `groupBy`, `join` (unless broadcast), `distinct`, `orderBy`, `repartition`, `reduceByKey`. Wide transformations are more expensive but often unavoidable.

#### What is a partition?

A chunk of the data that a single task processes. Parallelism equals the number of partitions being processed at once, limited by the total executor cores. Too few partitions waste cores; too many add scheduling overhead and small files.

<!-- challenge -->

A notebook runs five transformations quickly, then `show()` takes four minutes. A colleague thinks `show()` is slow. What is really happening?

<!-- solution -->

The earlier cells only built a plan; `show()` is the first action, so it runs the whole pipeline (reads, filters, shuffles). The time belongs to the transformations, not to `show()` itself.

<!-- takeaways -->

- Transformations are lazy; actions run jobs.
- Narrow operations stay in partitions; wide ones shuffle.
- Laziness lets Spark optimize the whole plan.

<!-- unit: Driver, executors and execution -->

<!-- goals -->

- Describe the driver, executors and cluster manager.
- Follow an action through jobs, stages and tasks, in client or cluster mode.

<!-- concept -->

A Spark application has one driver and many executors. The driver runs your program, turns actions into jobs, splits jobs into stages at shuffle boundaries and stages into tasks, one per partition. Executors run the tasks and keep data for them. A cluster manager such as YARN or Kubernetes provides the machines.

Where the driver runs matters operationally: on the submitting machine in client mode, inside the cluster in cluster mode, which is what production jobs need.

<!-- example -->

```text
action: write()
 └─ job 0
     ├─ stage 0: read + filter + partial agg   → 400 tasks (one per input partition)
     └─ stage 1: final agg + write             → 200 tasks (shuffle partitions)
```

#### What are the driver and the executors?

The **driver** runs your program, builds the plan, splits it into jobs, stages and tasks, and schedules the tasks. **Executors** are JVM processes on worker nodes that run tasks, keep cached data and report back to the driver. A Spark application has one driver and many executors.

#### What is a cluster manager?

The system that allocates resources (CPU, memory) for Spark's executors: Spark standalone, Hadoop YARN or Kubernetes. Mesos support was deprecated and removed in Spark 4.0. Managed platforms (Databricks, EMR, Dataproc, Glue) handle this for you.

#### What is the difference between client and cluster deploy mode?

In **client mode** the driver runs on the machine that submitted the application (useful for interactive work; the application dies if that machine disconnects). In **cluster mode** the driver runs inside the cluster, which is the right choice for production jobs.

#### What are jobs, stages and tasks?

Each action creates a **job**. The job is split into **stages** at shuffle boundaries: operations within a stage can run without moving data between executors. Each stage runs one **task** per partition, and tasks are the unit of work sent to executors.

#### What happens from the moment an action is called?

1. Catalyst turns the transformations into a logical plan, optimizes it and chooses a physical plan.
2. The DAG scheduler walks the plan back from the action to the sources and splits it into stages wherever a shuffle is needed.
3. Each stage becomes a set of tasks, one per partition.
4. The task scheduler sends tasks to executors, preferring executors that already hold the data (data locality).
5. Stages run in order; a stage that depends on a shuffle waits until the previous stage has written its shuffle files.

<!-- challenge -->

The Spark UI shows a job with 3 stages and 1,200 tasks in total. How can you tell where the shuffles are?

<!-- solution -->

Each stage boundary is a shuffle (or broadcast exchange): with 3 stages there are 2 shuffle boundaries. The stage details and the SQL tab's `Exchange` nodes show which operations caused them.

<!-- takeaways -->

- The driver plans; executors run tasks.
- Jobs split into stages at shuffles; stages into tasks.
- Cluster mode keeps the driver inside the cluster.

<!-- unit: Locality, fault tolerance and Tungsten -->

<!-- goals -->

- Explain data locality and lineage-based fault tolerance.
- Describe what the Tungsten engine does.

<!-- concept -->

Spark is fast and resilient for related reasons. It tries to run each task close to its data, ideally in the same executor's memory. When a task or executor fails, Spark doesn't need copies: it knows how each partition was computed and recomputes just the lost ones from lineage.

Underneath, Tungsten stores data in compact binary form outside the JVM's object model and generates code for whole stages, which is why DataFrame operations are far faster than equivalent Python loops.

<!-- example -->

```text
executor 7 dies during stage 2
 → partitions 112–118 lost
 → scheduler reruns their tasks from lineage (stage 1 output or source files)
 → job continues; no full restart
```

#### What is data locality?

Spark tries to run a task where its data already is: in the same executor's memory (`PROCESS_LOCAL`), on the same node (`NODE_LOCAL`), on the same rack, or anywhere. With cloud object storage, data is always remote, so locality matters less than with HDFS.

#### How does Spark achieve fault tolerance?

Through lineage: Spark knows how each partition was computed, so if an executor dies, it recomputes only the lost partitions from their sources or from shuffle files. Failed tasks are retried (`spark.task.maxFailures`, 4 by default) and stages can be resubmitted.

#### What is the Tungsten engine?

Spark's execution layer that manages memory off the JVM heap in a compact binary format and generates JVM bytecode for whole stages of a query (whole-stage code generation). It reduces garbage collection and CPU overhead, and is one reason DataFrames are faster than RDDs.

<!-- challenge -->

A job with a very long lineage (hundreds of iterative steps) takes ages to recover when an executor fails. What can you do?

<!-- solution -->

Cut the lineage: write intermediate results to storage (or `checkpoint()`), so recovery recomputes from the checkpoint instead of replaying hundreds of steps.

<!-- takeaways -->

- Spark schedules tasks near their data.
- Lineage recomputes lost partitions.
- Tungsten's binary format and codegen make DataFrames fast.

### SparkSession, SparkContext and configuration

<!-- unit: Entry points -->

<!-- goals -->

- Distinguish SparkContext, SparkSession and SQLContext.
- Create sessions, use RDDs from them and understand getOrCreate.

<!-- concept -->

Modern PySpark starts with a SparkSession, the single entry point for DataFrames, SQL and configuration. The older SparkContext still exists inside it and is the door to RDDs; SQLContext is a legacy leftover.

Sessions are usually shared: `getOrCreate` returns the active one if it exists, which is how notebooks and libraries avoid creating conflicting sessions.

<!-- example -->

```python
spark = (SparkSession.builder
         .appName("orders_etl")
         .config("spark.sql.shuffle.partitions", "64")
         .getOrCreate())
sc = spark.sparkContext                     # RDD API when needed
rdd = sc.parallelize(range(10))
```

#### What's the difference between SparkContext, SparkSession and SQLContext?

All three are entry points to the engine:

- **SparkContext:** the original entry point. It connects to the cluster and manages RDD operations.
- **SparkSession:** the modern, unified entry point (since Spark 2.0) for DataFrames and Spark SQL. It contains a SparkContext, so RDD operations are still possible through `spark.sparkContext`.
- **SQLContext** (and HiveContext): legacy entry points replaced by SparkSession.

```python
from pyspark import SparkContext

sc = SparkContext("local", "MyApp")
rdd = sc.parallelize(["A", "B", "C", "D"])
print(rdd.map(lambda c: ord(c)).collect())   # [65, 66, 67, 68]
sc.stop()
```

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("MyOtherApp").getOrCreate()
df = spark.createDataFrame(
    [("Rosa María Casas del Campo", 16, "Planeta Rica", "Colombia"),
     ("Hideo Kojima", 63, "Setagaya", "Japón")],
    ["name", "age", "city_of_birth", "country_of_birth"],
)
df.show()
spark.stop()
```

#### How do you create a SparkContext and a SparkSession?

A SparkContext takes a master URL and an app name, or a `SparkConf` for detailed configuration. A SparkSession uses a builder pattern.

```python
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local[*]").setAppName("MiAplicacion")
sc = SparkContext(conf=conf)
print(sc.applicationId)
sc.stop()
```

```python
from pyspark.sql import SparkSession

spark = (SparkSession.builder
         .appName("ProcesadorDeDatos")
         .config("spark.executor.memory", "1g")
         .getOrCreate())
print(spark.sparkContext.applicationId)
spark.stop()
```

`local[*]` uses all local cores, `local[4]` uses four; `local[0]` isn't valid.

#### How do you work with RDDs from a SparkSession?

Through its embedded SparkContext, `spark.sparkContext`. Stop the session, not the context, when you're done.

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("RDDSparkSession").getOrCreate()
sc = spark.sparkContext
rdd = sc.parallelize([1, 2, 3])
print(rdd.collect())
spark.stop()
```

#### Does SparkContext support DataFrames?

No. DataFrames need a SparkSession (or the legacy SQLContext). A SparkContext alone only works with RDDs.

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DataFrames").getOrCreate()
df = spark.createDataFrame([("AWS Redshift", 2013), ("Apache Spark", 2009)],
                           ["product", "year_of_release"])
df.filter(df.year_of_release > 2010).show()
spark.stop()
```

#### What does getOrCreate() do?

It returns the active SparkSession if one exists, or creates a new one. In notebooks and on Databricks a session called `spark` already exists, so `getOrCreate()` returns it and most builder settings are ignored.

<!-- challenge -->

A library function creates its own SparkSession with different settings, and a notebook's configuration seems ignored. What is going on?

<!-- solution -->

`getOrCreate()` returns the already active session, so builder settings that require a new context are ignored. Configure the session once at startup, or set runtime-changeable options with `spark.conf.set`.

<!-- takeaways -->

- SparkSession is the entry point; SparkContext is inside it.
- DataFrames need a session.
- `getOrCreate` reuses the active session.

<!-- unit: Configuring and submitting -->

<!-- goals -->

- Set configuration at build, submit and run time.
- Submit applications with dependencies and control logging.

<!-- concept -->

Configuration can come from three places: the session builder, the `spark-submit` command, and runtime calls. Some settings, such as executor sizes, must be fixed before the application starts; SQL settings can change while it runs.

Python dependencies need special care because executors run their own Python processes: packages must reach them as zipped files, packed environments or container images. Log levels keep output readable.

<!-- example -->

```bash
spark-submit --master yarn --deploy-mode cluster \
  --conf spark.executor.memory=8g --conf spark.executor.cores=4 \
  --archives pyspark_env.tar.gz#environment \
  --conf spark.pyspark.python=./environment/bin/python \
  jobs/orders_etl.py --date 2026-10-17
```

#### How do you set and read configuration?

At build time with `.config(key, value)`, at submit time with `--conf key=value`, or at runtime for SQL settings with `spark.conf.set("spark.sql.shuffle.partitions", "64")`. Read a value with `spark.conf.get(key)`. Cluster-level settings such as executor memory can't be changed once the application has started.

#### What are the most important spark-submit options?

`--master`, `--deploy-mode`, `--executor-memory`, `--executor-cores`, `--num-executors` (or dynamic allocation), `--driver-memory`, `--conf`, `--py-files` (zip or wheel dependencies), `--packages` (Maven coordinates, such as connectors) and `--files`.

```bash
spark-submit --master yarn --deploy-mode cluster \
  --executor-memory 8g --executor-cores 4 \
  --conf spark.sql.shuffle.partitions=400 \
  --py-files deps.zip main.py --date 2026-10-17
```

#### How do you ship Python dependencies to executors?

With `--py-files` (zips, eggs or wheels), by building a packed virtual environment (venv-pack, conda-pack) and passing it with `--archives`, or by installing libraries on the cluster (Databricks libraries, EMR bootstrap actions, a custom Docker image on Kubernetes). Every executor needs the same versions as the driver.

#### How do you change the log level?

`spark.sparkContext.setLogLevel("WARN")` at runtime, or through the log4j2 configuration file for the cluster. Lowering noise makes driver logs easier to read in notebooks.

<!-- challenge -->

A job works in the driver but fails on executors with `ModuleNotFoundError: phonenumbers`. Why, and how do you fix it?

<!-- solution -->

The package exists only on the driver's machine. Ship it to executors: a packed virtual environment with `--archives`, `--py-files` for pure-Python code, or a container image that includes it.

<!-- takeaways -->

- Settings come from builder, submit or runtime.
- Executor sizing must be set before startup.
- Python dependencies must reach every executor.

<!-- unit: Sizing resources -->

<!-- goals -->

- Size executors in cores and memory.
- Use dynamic allocation to match resources to work.

<!-- concept -->

Executor size is a balance. Too few cores per executor wastes memory overhead; too many hurts I/O throughput and garbage collection. Around four or five cores with memory to match is a common starting point, adjusted from metrics.

Workloads vary within a job, so dynamic allocation adds executors when tasks queue and releases idle ones, as long as shuffle data survives their removal.

<!-- example -->

```properties
spark.executor.cores=4
spark.executor.memory=12g
spark.executor.memoryOverhead=2g
spark.dynamicAllocation.enabled=true
spark.dynamicAllocation.minExecutors=2
spark.dynamicAllocation.maxExecutors=50
spark.dynamicAllocation.shuffleTracking.enabled=true
```

#### What is dynamic allocation?

A feature that adds executors when tasks are waiting and removes idle ones (`spark.dynamicAllocation.enabled`). It needs a way to keep shuffle files available when executors are removed: the external shuffle service or shuffle tracking. It saves resources on shared clusters.

#### How do you size executors?

A common starting point is 4 to 5 cores per executor and enough memory for those cores' tasks (for example 4 cores with 16 to 32 GB). Very large executors suffer long garbage collection pauses; very small ones can't hold broadcast tables and waste per-executor overhead. Adjust based on spill and GC time in the Spark UI.

<!-- challenge -->

A job uses 10 executors of 20 cores and 32 GB each, and spends 30% of its time in garbage collection. What do you change?

<!-- solution -->

Use more, smaller executors (for example 40 executors of 5 cores and 8–10 GB), which reduces heap size per JVM and GC pauses, and improves I/O parallelism per core.

<!-- takeaways -->

- Start around 4–5 cores per executor.
- Very large executors suffer GC pauses.
- Dynamic allocation fits resources to workload.

### RDDs and serialization

<!-- unit: RDD operations -->

<!-- goals -->

- Explain RDDs and when to still use them.
- Use map, flatMap, mapPartitions, reduceByKey and conversions to DataFrames.

<!-- concept -->

RDDs are Spark's original abstraction: distributed collections of arbitrary objects, transformed with functions. They give full control but no optimizer, and in Python every element is a Python object shipped between processes, so they're much slower than DataFrames.

They still help for unstructured text, custom partitioning or legacy code. The classic lesson from RDDs applies everywhere: combine values before shuffling, as `reduceByKey` does, instead of shuffling everything and combining afterwards.

<!-- example -->

```python
counts = (sc.textFile("logs/*.txt")
            .flatMap(lambda line: line.lower().split())
            .map(lambda w: (w, 1))
            .reduceByKey(lambda a, b: a + b))      # combines per partition before shuffle
top = counts.toDF(["word", "n"]).orderBy(F.desc("n")).limit(10)
```

#### What is an RDD?

A Resilient Distributed Dataset: an immutable, partitioned collection of objects that can be processed in parallel and rebuilt from its lineage. It's Spark's low-level API; DataFrames are built on top of it.

#### When would you still use RDDs?

Rarely in new code: for fine-grained control over partitioning, for processing unstructured data that doesn't fit a schema, or with legacy code. DataFrames are faster because Catalyst and Tungsten can optimize them, and in Python RDD operations serialize every record between the JVM and Python. RDDs aren't available through Spark Connect.

#### What's the difference between map(), flatMap() and mapPartitions()?

- `map` applies a function to each element and returns one element per input.
- `flatMap` applies a function that returns a sequence for each element and flattens the results.
- `mapPartitions` applies a function to a whole partition (an iterator), which is useful for expensive setup such as opening a connection once per partition.

```python
rdd = sc.parallelize([1, 2, 3, 4])
rdd.map(lambda x: x ** 2).collect()                 # [1, 4, 9, 16]

lines = sc.parallelize(["hello world", "how are you"])
lines.flatMap(lambda line: line.split(" ")).collect()
# ['hello', 'world', 'how', 'are', 'you']

def sum_partition(iterator):
    yield sum(iterator)

sc.parallelize([1, 2, 3, 4], 2).mapPartitions(sum_partition).collect()   # [3, 7]
```

#### What's the difference between reduceByKey and groupByKey?

`reduceByKey` combines values for each key within each partition before the shuffle (a map-side combine), so much less data moves. `groupByKey` shuffles every value and then groups them, which uses more network and memory and can fail on skewed keys. Prefer `reduceByKey` or `aggregateByKey`, or better, DataFrame aggregations.

#### How do you count words with RDDs?

```python
counts = (sc.textFile("path/to/text")
            .flatMap(lambda line: line.lower().split())
            .map(lambda word: (word, 1))
            .reduceByKey(lambda a, b: a + b)
            .sortBy(lambda pair: pair[1], ascending=False))
counts.take(10)
```

#### What is the difference between coalesce and repartition on RDDs?

The same as for DataFrames: `repartition(n)` does a full shuffle and can increase or decrease partitions; `coalesce(n)` merges existing partitions without a full shuffle and can only decrease them.

#### How do you convert between RDDs and DataFrames?

`df.rdd` returns an RDD of `Row` objects; `spark.createDataFrame(rdd, schema)` or `rdd.toDF(["col1", "col2"])` builds a DataFrame. Converting to an RDD in Python serializes every row into Python, so avoid it in hot paths.

<!-- challenge -->

An RDD job uses `groupByKey().mapValues(sum)` and runs out of memory on a few keys. What do you change?

<!-- solution -->

Use `reduceByKey(lambda a, b: a + b)`, which sums within each partition before the shuffle, so far less data moves and no key's full list is held in memory. Better still, use a DataFrame `groupBy().sum()`.

<!-- takeaways -->

- RDDs give control but no optimizer.
- Python RDDs are much slower than DataFrames.
- Combine before shuffling (`reduceByKey`).

<!-- unit: Shared variables -->

<!-- goals -->

- Use broadcast variables for lookup data.
- Use accumulators for counters, knowing their caveats.

<!-- concept -->

Functions sent to executors carry copies of whatever they reference, once per task. A large lookup dictionary referenced in a function is therefore shipped thousands of times; a broadcast variable sends it once per executor instead.

Accumulators go the other way: tasks add to them and the driver reads the total, handy for counting bad records. Because failed or retried tasks may add twice, they're for monitoring, not business logic.

<!-- example -->

```python
country_names = sc.broadcast({"CO": "Colombia", "PE": "Peru", "MX": "Mexico"})
bad = sc.accumulator(0)

def to_name(code):
    if code not in country_names.value:
        bad.add(1)
    return country_names.value.get(code, "unknown")
```

#### What are broadcast variables?

Read-only values sent once to each executor instead of with every task, such as a lookup dictionary. Create them with `sc.broadcast(value)` and read `.value` inside functions. For DataFrame joins, use the `broadcast()` join hint instead.

#### What are accumulators?

Variables that tasks can only add to and only the driver can read, used for counters such as the number of malformed rows. Updates made inside transformations can be applied more than once if a task is retried; only updates inside actions are guaranteed exactly once.

<!-- challenge -->

A team computes a billing total with an accumulator inside a `map`, and the total is sometimes too high. Why?

<!-- solution -->

Accumulator updates inside transformations can be applied more than once when tasks are retried or stages recomputed. Compute business totals with an aggregation (`sum`) and use accumulators only for diagnostics.

<!-- takeaways -->

- Broadcast sends read-only data once per executor.
- Accumulators collect counts at the driver.
- Don't trust accumulators in transformations for exact results.

<!-- unit: Serialization -->

<!-- goals -->

- Explain why Spark serializes data and which serializers it uses.
- Diagnose "Task not serializable" and pickling errors.

<!-- concept -->

Anything that crosses machines or processes must become bytes: tasks shipped to executors, data shuffled between them, cached partitions and Python objects passed to the JVM. The serializer decides how fast and compact that is; Kryo is faster than Java's default for JVM objects, and Python uses pickle.

Errors arise when a function captures something that can't be serialized, such as the SparkSession, a database connection or an open file. The fix is to create those inside the function or per partition.

<!-- example -->

```python
conn = psycopg.connect(DSN)                 # driver-side object
rdd.foreach(lambda r: conn.execute(...))    # ✘ pickling error: connection can't be serialized

def write_partition(rows):                  # ✔ create the connection on the executor
    with psycopg.connect(DSN) as c:
        for r in rows:
            c.execute("INSERT ...", r)
rdd.foreachPartition(write_partition)
```

#### What are serialization and deserialization, and why does Spark need them?

**Serialization** turns an object into a stream of bytes so it can be sent over the network or stored compactly; **deserialization** rebuilds the object from those bytes. Spark needs both to send functions and data from the driver to executors, to move data during shuffles and to cache data in serialized form.

#### What serializers does Spark use?

On the JVM side, Spark uses the **Java serializer** by default for RDDs of JVM objects, and the faster, more compact **Kryo serializer** can be enabled (`spark.serializer=org.apache.spark.serializer.KryoSerializer`), optionally with registered classes. DataFrames don't depend on either for their data: Tungsten stores rows in its own binary format. In PySpark, Python objects and functions are serialized with **pickle** (cloudpickle for functions), and **Apache Arrow** is used to move columnar data between the JVM and pandas.

```python
from pyspark.sql import SparkSession

spark = (SparkSession.builder.appName("Kryo app")
         .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
         .getOrCreate())
```

#### Can you choose the serializer for Python RDDs?

Yes. The default is a batched pickle serializer; `MarshalSerializer` is faster but supports fewer types. Custom classes must be picklable and importable on the executors (defined in a module shipped with `--py-files`, not only in a notebook cell).

```python
from pyspark import SparkContext
from pyspark.serializers import MarshalSerializer

sc = SparkContext("local[*]", "MarshalApp", serializer=MarshalSerializer())
rdd = sc.parallelize([
    {"name": "Daniel Noboa", "home": {"city": "Quito"}},
    {"name": "Nayib Bukele", "home": {"city": "San Salvador"}},
])
print(rdd.map(lambda person: person["home"]["city"]).collect())
sc.stop()
```

#### What does "Task not serializable" or a pickling error mean?

A function sent to executors references something that can't be serialized, such as a SparkSession, a database connection, a lock or an open file. Create such objects inside the function (or per partition with `mapPartitions`/`foreachPartition`) instead of capturing them from the driver.

<!-- challenge -->

A function used in `mapPartitions` references `spark.read`, and the job fails with a pickling error. What is wrong?

<!-- solution -->

The SparkSession exists only on the driver and can't be serialized to executors. Do all reads on the driver; inside executor functions, work only with the rows (and with objects created there).

<!-- takeaways -->

- Tasks and data are serialized to cross machines.
- Kryo for JVM objects; pickle for Python.
- Create connections and sessions where they're used.

<!-- stage: Working with DataFrames -->

### DataFrames and schemas

<!-- unit: DataFrames and schemas -->

<!-- goals -->

- Explain DataFrames, Rows and their relation to Datasets.
- Create DataFrames with explicit schemas instead of inference.

<!-- concept -->

A DataFrame is a distributed table: rows with named, typed columns, immutable and lazily evaluated. Because Spark knows the schema, it can optimize, store data compactly and generate efficient code, which plain Python objects never allow.

Schemas should be declared, not guessed. Inference reads data an extra time and guesses types from samples, which is slow and fragile: a column of numbers today might contain text tomorrow.

<!-- example -->

```python
schema = "order_id BIGINT, customer_id BIGINT, amount DECIMAL(12,2), ordered_at TIMESTAMP"
orders = spark.read.schema(schema).option("header", True).csv("s3://landing/orders/")
small = spark.createDataFrame([(1, "Bogotá"), (2, "Lima")], "id INT, city STRING")
```

#### What is a DataFrame?

A distributed collection of rows with named, typed columns, like a table. It's immutable: every transformation returns a new DataFrame. Because Spark knows the schema and the operations, Catalyst can optimize DataFrame code, unlike opaque RDD functions.

#### What is the difference between a DataFrame and a Dataset?

A Dataset is a typed version of the DataFrame available in Scala and Java. In those languages a DataFrame is `Dataset[Row]`. Python only has DataFrames, because it isn't statically typed.

#### How do you create a DataFrame?

From a list of tuples or `Row` objects with `spark.createDataFrame`, from a pandas DataFrame, from an RDD, from a file or table with `spark.read`, or with SQL through `spark.sql`.

```python
from pyspark.sql import Row

df1 = spark.createDataFrame([(1, "Bogotá"), (2, "Medellín")], ["id", "city"])
df2 = spark.createDataFrame([Row(id=1, city="Cali")])
df3 = spark.range(0, 1000)          # a single "id" column
```

#### How do you define a schema explicitly?

With a `StructType` of `StructField`s, or with a DDL string. Explicit schemas are faster than inference and catch format changes early.

```python
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

schema = StructType([
    StructField("user_id", IntegerType(), nullable=False),
    StructField("city", StringType()),
    StructField("amount", DoubleType()),
])
ddl_schema = "user_id INT, city STRING, amount DOUBLE"
```

#### Why avoid inferSchema in production?

Inference reads the data (all of it for CSV, or a sample) an extra time, which is slow on large files. It can also infer different types on different days (an ID column read as an integer until a value with a letter appears), so jobs break or silently change. Declare the schema.

#### What is a Row?

An object representing one record, with fields accessible by name (`row.city` or `row["city"]`) or position. `collect()` and `take()` return lists of `Row` objects; `row.asDict()` converts one to a dictionary.

<!-- challenge -->

A nightly CSV load with `inferSchema=True` failed after a supplier sent "N/A" in a numeric column, making the column a string. How do you prevent this?

<!-- solution -->

Declare the schema explicitly with the numeric type, read in permissive mode with a corrupt-record column, and route rows that fail to parse to quarantine instead of changing the column type.

<!-- takeaways -->

- DataFrames are typed, immutable, lazy tables.
- Explicit schemas are faster and safer than inference.
- Python's API has DataFrames; Datasets are for Scala/Java.

<!-- unit: Inspecting and moving data to the driver -->

<!-- goals -->

- Inspect schemas and samples safely.
- Choose between collect, take, show and toPandas, and use the pandas API on Spark.

<!-- concept -->

Looking at data is where many jobs accidentally fall over. Some calls inspect metadata only; others pull rows to the driver, and pulling everything from a large DataFrame overwhelms it. Checking emptiness by counting scans all data when one row would do.

Moving to pandas is fine once data is small, and Arrow makes it fast. The pandas API on Spark offers pandas syntax over distributed data for teams migrating code.

<!-- example -->

```python
orders.printSchema()                      # metadata only
orders.show(5, truncate=False)            # 5 rows
if orders.isEmpty(): ...                  # stops after one row
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
summary_pdf = orders.groupBy("country").count().toPandas()   # small result → pandas
```

#### How do you inspect a DataFrame?

`printSchema()` for the schema tree, `df.schema` and `df.dtypes` programmatically, `show(n, truncate=False)` for rows, `df.columns` for names, `describe()` or `summary()` for basic statistics, and `explain()` for the query plan.

#### How do you check whether a DataFrame is empty?

`df.isEmpty()` (Spark 3.3) or `len(df.head(1)) == 0`. Avoid `df.count() == 0`, which scans everything.

#### What is the difference between collect, take, head, show and toPandas?

`collect()` brings all rows to the driver; `take(n)` and `head(n)` bring the first n; `show(n)` prints them; `toPandas()` brings everything into a pandas DataFrame (using Arrow if enabled). Everything except small `take`/`show` calls can run the driver out of memory on large data.

#### How do you convert between Spark and pandas?

`spark.createDataFrame(pandas_df)` and `df.toPandas()`. Enable Arrow (`spark.sql.execution.arrow.pyspark.enabled=true`, the default in recent Databricks runtimes) to make both conversions much faster. Only convert data that fits in the driver's memory.

#### What is the pandas API on Spark?

`pyspark.pandas`, a pandas-compatible API that runs on Spark (formerly Koalas). It helps migrate pandas code to large data, though some operations behave differently (index handling, ordering) and can be slower than native PySpark.

#### How do you sample data?

`df.sample(fraction=0.1, seed=42)` for a random sample (approximate size), `df.limit(n)` for the first rows (not random), and `df.randomSplit([0.8, 0.2], seed=42)` to split for training and testing.

<!-- challenge -->

A notebook calls `df.toPandas()` on a 300 GB table to "look at the data" and the driver crashes. What should it do instead?

<!-- solution -->

Inspect with `printSchema()`, `show(20)`, `limit(1000).toPandas()` or `sample(0.001)`, or aggregate first and convert only the small result.

<!-- takeaways -->

- Metadata calls are cheap; collecting rows isn't.
- Use `isEmpty()` or `head(1)`, not `count()`.
- Convert to pandas only small results, with Arrow.

<!-- unit: Reshaping columns -->

<!-- goals -->

- Rename, add, replace and drop columns efficiently.
- Understand DataFrame immutability in Python code.

<!-- concept -->

DataFrames never change; every operation returns a new one, and reassigning a variable only points it at the newer plan. That makes it safe to build pipelines step by step.

Building many columns one call at a time, especially in loops, grows the plan with one projection per call, which slows analysis. Defining several columns at once keeps plans small and code clearer.

<!-- example -->

```python
clean = (orders
  .withColumnsRenamed({"cust_id": "customer_id", "amt": "amount"})
  .withColumns({
      "amount_eur": F.col("amount") * F.col("fx_rate"),
      "order_date": F.to_date("ordered_at"),
  })
  .drop("fx_rate")
  .dropDuplicates(["order_id"]))
```

#### What is the difference between DataFrame immutability and Python variables?

DataFrames never change; transformations return new ones. Reassigning `df = df.filter(...)` only points the variable to a new plan. That's why calling `df.withColumn(...)` without assigning the result does nothing.

#### How do you rename columns?

`withColumnRenamed(old, new)`, `withColumnsRenamed({old: new})` (Spark 3.4), `select(col(old).alias(new))` or `toDF(*new_names)` to rename all of them at once.

#### How do you add or replace several columns efficiently?

Use one `select` or `withColumns({...})` (Spark 3.3) instead of calling `withColumn` in a loop. Each `withColumn` adds a projection to the plan, and hundreds of them make analysis and optimization very slow.

```python
df = df.withColumns({
    "amount_cop": F.col("amount") * F.col("fx_rate"),
    "load_date": F.current_date(),
})
```

#### How do you drop columns and duplicate rows?

`drop("col1", "col2")` removes columns. `distinct()` removes rows that are duplicates on every column; `dropDuplicates(["id"])` keeps one row per key, but which row survives isn't defined. To keep a specific one (for example the most recent), use a window function.

<!-- challenge -->

Code adds 150 derived columns with `withColumn` in a loop, and the job takes two minutes before any task starts. What do you change?

<!-- solution -->

Build the column expressions in a list or dict and add them in one `select` or `withColumns` call, so the plan has one projection instead of 150 nested ones.

<!-- takeaways -->

- Every operation returns a new DataFrame.
- Add many columns in one `select` or `withColumns`.
- `dropDuplicates` on keys; `distinct` on all columns.

<!-- unit: Nested data -->

<!-- goals -->

- Work with arrays, maps and structs.
- Flatten nested JSON with explode and explode_outer.

<!-- concept -->

Real data is often nested: orders with arrays of items, customers with address structs, attributes as maps. Spark handles these as typed columns, so you can select nested fields with dot notation and keep data nested as long as it's convenient.

Flattening turns each array element into a row. The detail that matters is what happens to empty or missing arrays: one variant drops those rows, the other keeps them with nulls, which changes counts.

<!-- example -->

```python
items = (orders
  .select("order_id", "customer.city", F.explode_outer("items").alias("item"))
  .select("order_id", "city", "item.sku", "item.qty", "item.price"))
```

#### What complex types does Spark support?

`ArrayType`, `MapType` and `StructType` (nested records), which can be nested within each other, plus `VARIANT` in Spark 4 for semi-structured data. Access struct fields with dot notation (`col("address.city")`), arrays with `col("tags")[0]` or `element_at`, and maps with `col("attrs")["key"]`.

#### How do you handle nested JSON?

Read it with a schema, select nested fields with dot notation, flatten arrays with `explode`, and parse JSON strings in a column with `from_json`.

```python
from pyspark.sql import functions as F

orders = spark.read.schema(order_schema).json("path/to/orders")
flat = (orders
        .select("order_id", "customer.name", F.explode("items").alias("item"))
        .select("order_id", "name", "item.sku", "item.qty"))
```

#### What's the difference between explode and explode_outer?

`explode` produces one row per array element and drops rows whose array is null or empty. `explode_outer` keeps those rows with a null element. `posexplode` also returns the element's position.

#### Practice problem 6: flatten nested JSON

Each order is a JSON document with an `order_id`, a `customer` struct (`id`, `city`) and an `items` array of structs (`sku`, `qty`, `price`). Produce one row per item with the order ID, the customer's city and the line total.

```python
order_schema = """
    order_id STRING,
    customer STRUCT<id: STRING, city: STRING>,
    items ARRAY<STRUCT<sku: STRING, qty: INT, price: DOUBLE>>
"""
lines = (spark.read.schema(order_schema).json("path/to/orders")
         .select("order_id", F.col("customer.city").alias("city"), F.explode("items").alias("item"))
         .select("order_id", "city", "item.sku",
                 (F.col("item.qty") * F.col("item.price")).alias("line_total")))
```

Use `explode_outer` if orders without items must still appear.

<!-- challenge -->

After flattening orders with `explode`, the number of distinct orders dropped by 3%. What happened?

<!-- solution -->

Orders with empty or null `items` arrays were dropped by `explode`. Use `explode_outer` to keep them (with null item fields), or count orders before exploding.

<!-- takeaways -->

- Arrays, maps and structs are first-class types.
- Select nested fields with dot notation.
- `explode` drops empty arrays; `explode_outer` keeps them.

### Columns and built-in functions

<!-- unit: Columns and conditions -->

<!-- goals -->

- Reference columns and filter rows correctly.
- Write conditional logic with when, lit and expr.

<!-- concept -->

Most PySpark logic is built from column expressions: references, constants, operators and functions combined into a plan that runs on the JVM. Importing functions as `F` avoids accidentally calling Python's own `sum` or `max` on columns.

Conditions combine with `&`, `|` and `~`, each wrapped in parentheses because Python's operator precedence differs from SQL's. Conditional values use `when` chains; SQL snippets fit in with `expr` when they read better.

<!-- example -->

```python
from pyspark.sql import functions as F
labeled = orders.where((F.col("amount") > 0) & (F.col("status") != "test")).withColumn(
    "size",
    F.when(F.col("amount") >= 1000, "large")
     .when(F.col("amount") >= 100, "medium")
     .otherwise("small"))
taxed = labeled.withColumn("amount_with_tax", F.expr("amount * (1 + tax_rate)"))
```

#### What are the different ways to reference a column?

`F.col("name")`, `df["name"]`, `df.name` and, in many functions, the plain string `"name"`. `df.name` breaks with names that clash with DataFrame methods or contain spaces; `F.col` is the most consistent. Use backticks for names with dots or spaces: ``F.col("`order.id`")``.

#### Why import functions as F?

`from pyspark.sql import functions as F` avoids shadowing Python built-ins such as `sum`, `min`, `max`, `round` and `filter`. Importing `sum` directly from `pyspark.sql.functions` silently replaces Python's `sum`, a classic source of confusing errors.

#### How do you filter rows?

With `filter` or its alias `where`, using column expressions or a SQL string. Combine conditions with `&`, `|` and `~`, wrapping each condition in parentheses.

```python
df.filter((F.col("amount") > 8000) & (F.col("city") == "Bogotá"))
df.where("amount > 8000 AND city = 'Bogotá'")
df.filter(~F.col("city").isin("Cali", "Pasto"))
```

#### How do you write conditional logic?

With `F.when(...).when(...).otherwise(...)`, the equivalent of SQL `CASE WHEN`. Without `otherwise`, unmatched rows get null.

```python
df = df.withColumn(
    "size",
    F.when(F.col("amount") >= 10000, "large")
     .when(F.col("amount") >= 5000, "medium")
     .otherwise("small"),
)
```

#### What does lit() do?

It turns a Python constant into a column expression, for example `F.lit(0)` or `F.lit("COP")`. Many functions accept plain values, but `lit` is needed when a column is expected, such as in `withColumn("currency", F.lit("COP"))`.

#### What does expr() do?

It parses a SQL expression into a column: `F.expr("amount * fx_rate")` or `df.selectExpr("id", "upper(city) AS city")`. It's handy for SQL-only functions and for configuration-driven transformations.

<!-- challenge -->

`df.filter(F.col("a") > 1 & F.col("b") < 5)` raises an error. Why, and what is the fix?

<!-- solution -->

In Python, `&` binds tighter than `>` and `<`, so it tries `1 & F.col("b")`. Wrap each condition: `df.filter((F.col("a") > 1) & (F.col("b") < 5))`.

<!-- takeaways -->

- Build logic from column expressions.
- Import functions as `F`.
- Parenthesize each condition combined with `&` or `|`.

<!-- unit: Nulls, types and ANSI mode -->

<!-- goals -->

- Handle nulls in comparisons and fill them.
- Cast types safely and understand ANSI mode.

<!-- concept -->

Nulls and casts are where silent errors hide. Comparisons with null are neither true nor false, so filters drop those rows unless you test for null explicitly. Filling nulls is a business decision, not a cleanup step.

Casting used to turn invalid values into null without warning. ANSI mode, default in Spark 4, raises errors instead, which is safer but means dirty data must be handled deliberately with try-style casts.

<!-- example -->

```python
df = df.withColumn("amount", F.expr("try_cast(amount_raw AS DECIMAL(12,2))"))  # null on bad input
missing = df.filter(F.col("discount").isNull())
df = df.fillna({"discount": 0, "city": "unknown"})
df = df.withColumn("total", F.round(F.col("amount") * (1 - F.col("discount")), 2))
```

#### How does Spark handle nulls in comparisons?

Comparisons with null return null, which `filter` treats as false. `col == None` doesn't work; use `isNull()`/`isNotNull()`. For null-safe equality (null equals null), use `eqNullSafe` or the SQL operator `<=>`.

#### How do you replace or fill nulls?

`df.na.fill({"city": "unknown", "amount": 0})` or `fillna`, `F.coalesce(col1, col2, F.lit(default))` for the first non-null value, and `df.na.drop(subset=["id"])` to drop rows with nulls in given columns.

#### How do you cast types?

`F.col("amount").cast("double")` or `.cast(DoubleType())`. Without ANSI mode, an invalid cast returns null; with ANSI mode (the default in Spark 4) it raises an error. `try_cast` (Spark 4, and SQL `TRY_CAST`) returns null for invalid values explicitly.

#### What is ANSI mode and why does it matter?

`spark.sql.ansi.enabled` makes Spark follow standard SQL: overflow, division by zero and invalid casts raise errors instead of returning null. It's on by default in Spark 4.0. It catches bad data early, but code written for the old behavior can fail, so test with the same setting as production.

#### How do you round and format numbers?

`round(col, 2)` (half-up), `bround` (banker's rounding), `format_number(col, 2)` for display, and `DecimalType(p, s)` for exact money amounts, because `double` is a floating-point type.

<!-- challenge -->

After upgrading to Spark 4, a job fails with a cast error on a column that "worked fine before". What changed, and how do you fix it properly?

<!-- solution -->

ANSI mode is now on, so invalid casts raise errors instead of silently returning null. Use `try_cast` for columns that may contain bad values, and quarantine or log those rows rather than disabling ANSI mode.

<!-- takeaways -->

- Null comparisons are unknown; test with `isNull`.
- Filling nulls is a business decision.
- ANSI mode raises on bad casts; use `try_cast`.

<!-- unit: Strings, dates and time zones -->

<!-- goals -->

- Clean strings with built-in functions.
- Parse, format and truncate dates, and handle time zones.

<!-- concept -->

Text and time cause most cleaning work, and built-in functions cover nearly all of it: trimming, case, padding, splitting and regular expressions for text; parsing with explicit patterns, formatting and truncating for dates.

Time zones need one rule held firmly: timestamps are instants stored in UTC and shown in the session time zone. Setting that zone explicitly in jobs makes results the same on every cluster.

<!-- example -->

```python
spark.conf.set("spark.sql.session.timeZone", "UTC")
clean = (raw
  .withColumn("email", F.lower(F.trim("email")))
  .withColumn("phone", F.regexp_replace("phone", r"[^0-9+]", ""))
  .withColumn("order_date", F.to_date("order_date_raw", "dd/MM/yyyy"))
  .withColumn("month", F.date_trunc("month", "ordered_at")))
```

#### What are the most useful string functions?

`lower`, `upper`, `trim`, `lpad`/`rpad`, `substring`, `concat`/`concat_ws`, `split`, `regexp_extract`, `regexp_replace`, `like`/`rlike`, `length`, `initcap` and `format_string`.

```python
df = df.withColumn("postcode", F.regexp_replace(F.trim("postcode"), r"[^0-9]", ""))
df = df.withColumn("full_name", F.concat_ws(" ", "first_name", "last_name"))
```

#### How do you parse and format dates?

`to_date(col, "dd/MM/yyyy")`, `to_timestamp`, `date_format(col, "yyyy-MM")`, `date_trunc("month", ts)`, `datediff`, `months_between`, `add_months`, `date_add`, `year`/`month`/`dayofweek`, `current_date` and `current_timestamp`. Patterns follow Java's `DateTimeFormatter` (`yyyy`, `MM`, `dd`, `HH`, `mm`).

#### How does Spark handle time zones?

Timestamps are stored as UTC instants and displayed in the session time zone (`spark.sql.session.timeZone`). Set it explicitly (for example `UTC`) so results don't depend on the cluster's default. Spark 3.4 added `TIMESTAMP_NTZ` for timestamps without a time zone.

<!-- challenge -->

The same job produces daily totals shifted by one day on two clusters. What is the likely cause?

<!-- solution -->

Different session time zones: `to_date` on timestamps uses `spark.sql.session.timeZone`, which defaults to the cluster's zone. Set it explicitly in the job (for example UTC or the business zone).

<!-- takeaways -->

- Built-in functions cover most string cleaning.
- Parse dates with explicit patterns.
- Set the session time zone explicitly.

<!-- unit: Arrays, JSON, IDs and pivots -->

<!-- goals -->

- Work with array and JSON columns.
- Generate IDs and hash keys, and pivot or unpivot data.

<!-- concept -->

Some columns carry structure inside them: arrays of values, JSON strings from APIs. Spark has functions to query and transform both without exploding rows or writing Python.

Keys and reshaping round this out. Generated IDs are unique but not consecutive or stable across runs, so deterministic hashes of business columns are better surrogate keys. Pivoting turns values into columns, best with the list of values given up front.

<!-- example -->

```python
events = events.withColumn("payload", F.from_json("payload_raw", "user_id STRING, tags ARRAY<STRING>"))
tagged = events.where(F.array_contains("payload.tags", "promo"))
keyed = orders.withColumn("order_key", F.xxhash64("source", "order_id"))
wide = sales.groupBy("store").pivot("month", ["2026-08", "2026-09", "2026-10"]).sum("revenue")
```

#### How do you work with arrays?

`array`, `array_contains`, `size`, `element_at`, `array_distinct`, `array_union`, `array_join`, `sort_array`, `explode`, `collect_list` and higher-order functions: `transform`, `filter`, `exists`, `aggregate`.

```python
df.withColumn("prices_with_tax", F.transform("prices", lambda p: p * 1.19))
df.withColumn("big_items", F.filter("items", lambda i: i["qty"] > 10))
```

#### How do you work with JSON strings in a column?

`from_json(col, schema)` parses into a struct or map, `to_json` serializes back, `get_json_object(col, "$.a.b")` extracts one value by path, and `schema_of_json` infers a schema from a sample string.

#### What is monotonically_increasing_id()?

A function that generates unique 64-bit IDs per row. They are increasing within a partition but not consecutive (the partition number is encoded in the upper bits). For consecutive numbers use `row_number()` over a window, which needs a sort.

#### How do you generate a hash or surrogate key?

`F.sha2(F.concat_ws("||", *cols), 256)`, `md5` or `xxhash64`. Hash keys are deterministic, so the same business key always gets the same surrogate key, which is useful for incremental loads and for comparing records to detect changes.

#### How do you pivot and unpivot?

`groupBy("store").pivot("month").sum("revenue")` turns month values into columns; passing the list of values (`pivot("month", ["01", "02"])`) avoids an extra pass to find them. `unpivot` (also called `melt`, Spark 3.4) turns columns back into rows.

<!-- challenge -->

A team uses `monotonically_increasing_id()` as a customer key, and keys change between runs, breaking joins with yesterday's data. What do you use instead?

<!-- solution -->

A deterministic hash of the business key (for example `sha2(concat_ws('||', source, customer_number), 256)` or `xxhash64`), which gives the same key every run for the same customer.

<!-- takeaways -->

- Array and JSON functions avoid Python code.
- Generated IDs aren't stable; hash business keys.
- Pivot with an explicit value list.

### Aggregations and grouping

<!-- unit: Grouping and aggregating -->

<!-- goals -->

- Aggregate with groupBy and agg, and filter aggregated results.
- Choose the right count and collect functions, avoiding unreliable first/last.

<!-- concept -->

Aggregation follows one pattern: group by keys, compute named aggregates, then filter or sort the result. Filtering after aggregation is how PySpark expresses SQL's `HAVING`.

Details decide correctness. Counting rows, non-null values and distinct values differ; collecting values keeps or drops duplicates; and "first" or "last" values depend on partitioning unless you order explicitly, which is why windows or max-by-style functions are safer.

<!-- example -->

```python
per_city = (sales.groupBy("city")
  .agg(F.count("*").alias("orders"),
       F.countDistinct("user_id").alias("buyers"),
       F.sum("amount").alias("revenue"),
       F.max_by("product_id", "amount").alias("top_product"))
  .where(F.col("revenue") > 100000)
  .orderBy(F.desc("revenue")))
```

#### How do you aggregate a DataFrame?

`groupBy(...).agg(...)` with aggregate functions, naming each result with `alias`.

```python
summary = (df.groupBy("city")
             .agg(F.count("*").alias("orders"),
                  F.sum("amount").alias("revenue"),
                  F.avg("amount").alias("avg_amount"),
                  F.countDistinct("user_id").alias("customers")))
```

#### What's the difference between count("*"), count(col) and countDistinct?

`count("*")` counts rows; `count(col)` counts non-null values of a column; `countDistinct(col)` counts distinct non-null values and needs a shuffle by value. On large data, `approx_count_distinct(col, rsd=0.02)` uses HyperLogLog and is much cheaper.

#### What is the difference between collect_list and collect_set?

Both gather values into an array per group: `collect_list` keeps duplicates, `collect_set` removes them. Neither guarantees order. To get an ordered list, collect structs and sort the array, or use a window function.

#### Why are first() and last() unreliable in aggregations?

Without an explicit ordering, the row that's "first" depends on how data was partitioned and shuffled, so results can change between runs. Use `max_by`/`min_by` (Spark 3.3), for example `F.max_by("status", "updated_at")`, or a window with `row_number()`.

#### How do you filter on an aggregate (SQL HAVING)?

Aggregate first, then filter the result.

```python
(df.groupBy("city")
   .agg(F.avg("amount").alias("avg_amount"))
   .filter(F.col("avg_amount") > 8000))
```

#### Practice problem 1: aggregations

Given this CSV file:

```csv
user_id;product_id;amount;city
1;101;12500.0;Bogota
2;102;9000.0;Cartagena
1;103;3000.0;Bogota
4;104;12500.0;Medellin
5;101;6250.0;Bogota
2;102;9000.0;Medellin
```

- Load the CSV into a DataFrame.
- Compute the total amount per user.
- Compute the average transaction amount per city.
- Keep only the cities where the average transaction amount is greater than 8000.
- Return the results as two DataFrames, `total_per_user` and `city_avg`, and cache one of them.

```python
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.getOrCreate()

df_sales = (spark.read
            .schema("user_id INT, product_id INT, amount DOUBLE, city STRING")
            .options(header=True, delimiter=";")
            .csv("path/to/file"))

total_per_user = df_sales.groupBy("user_id").agg(F.sum("amount").alias("total_amount"))

city_avg = (df_sales.groupBy("city")
            .agg(F.avg("amount").alias("avg_amount"))
            .filter(F.col("avg_amount") > 8000))

city_avg.cache()
city_avg.show()     # the first action fills the cache
```

<!-- challenge -->

A report uses `F.first("status")` to get each order's latest status, and results change between runs. What do you use instead?

<!-- solution -->

Pick the latest explicitly: `max_by("status", "updated_at")` in the aggregation, or a window with `row_number()` ordered by `updated_at` descending and keep row 1.

<!-- takeaways -->

- `groupBy().agg()` with aliases; filter afterwards for HAVING.
- Count variants answer different questions.
- `first`/`last` need explicit ordering to be reliable.

<!-- unit: Advanced aggregation -->

<!-- goals -->

- Produce subtotals with rollup and cube, and compute percentiles.
- Explain two-phase aggregation and keep detail rows with group counts.

<!-- concept -->

Spark aggregates in two phases: each partition computes partial results, then a shuffle brings partials for the same key together for the final result. That makes sums and counts cheap, but exact medians and distinct counts expensive, which is why approximate versions exist.

Beyond single groupings, rollups and cubes add subtotals in one pass, and window aggregates attach group-level values to every row without collapsing them.

<!-- example -->

```python
with_share = sales.withColumn(
    "city_revenue", F.sum("amount").over(Window.partitionBy("city"))
).withColumn("share", F.col("amount") / F.col("city_revenue"))
p50 = sales.groupBy("city").agg(F.percentile_approx("amount", 0.5).alias("median_amount"))
totals = sales.rollup("country", "city").agg(F.sum("amount").alias("revenue"))
```

#### What do rollup and cube do?

`rollup("country", "city")` adds subtotals for each level of the hierarchy plus a grand total; `cube` adds subtotals for every combination of the columns. `grouping()` and `grouping_id()` tell real nulls apart from subtotal rows.

#### How do you compute percentiles and medians?

`percentile_approx(col, 0.5)` (also `approx_percentile`) is fast and works on large data; `percentile` and `median` (Spark 3.4) are exact but more expensive.

#### How does Spark perform an aggregation physically?

Usually in two phases: a partial aggregation in each partition (like a map-side combine), a shuffle by grouping key, then a final aggregation. This is why aggregations shuffle much less data than the raw rows, unless almost every key is unique.

#### How do you count rows per group and keep the original columns?

Use a window function: `F.count("*").over(Window.partitionBy("city"))` adds the count to every row, without collapsing the DataFrame as `groupBy` does.

<!-- challenge -->

You need each order's share of its city's revenue. A colleague aggregates per city and joins back. What is a simpler way?

<!-- solution -->

A window aggregate: `F.sum("amount").over(Window.partitionBy("city"))` added to every row, then divide. One pass, no join.

<!-- takeaways -->

- Aggregations run partial, then final after a shuffle.
- Use approximate percentiles on large data.
- Window aggregates keep rows and add group values.

### Joins

<!-- unit: Join types and keys -->

<!-- goals -->

- Use inner, outer, semi and anti joins correctly.
- Handle duplicate columns, null keys and range joins.

<!-- concept -->

The join type decides which rows survive. Inner keeps matches, outer joins keep unmatched rows from one or both sides, semi joins filter by existence without adding columns, and anti joins keep rows with no match, the natural way to find what's missing or what changed.

Keys need care: joining on column names avoids duplicate key columns, null keys never match, and range conditions without an equality key force expensive nested-loop joins.

<!-- example -->

```python
new_or_changed = (this_month.alias("n")
  .join(last_month.alias("o"), on="registry_id", how="left")
  .where(F.col("o.registry_id").isNull() | (F.col("n.row_hash") != F.col("o.row_hash"))))
removed = last_month.join(this_month, on="registry_id", how="left_anti")
```

#### What join types does Spark support?

`inner`, `left` (`left_outer`), `right`, `full` (`outer`), `left_semi` (rows in the left with a match, left columns only), `left_anti` (rows in the left without a match) and `cross`.

```python
orders.join(customers, on="customer_id", how="left")
orders.join(blocked, on="customer_id", how="left_anti")    # orders from non-blocked customers
```

#### How do you avoid duplicate column names after a join?

Join on a column name or list of names (`on="user_id"`), which keeps a single key column. With an expression (`df1.user_id == df2.user_id`) both columns survive, and selecting `user_id` later fails as ambiguous. Alias the DataFrames or drop one side's column.

#### Why do null keys cause problems in joins?

Null never equals null in a join condition, so null keys don't match anything, but they all hash to the same partition during the shuffle, creating skew. Filter them out before the join (and union them back if you need them in a left join) or replace them with an "unknown" member key.

#### What is a semi join and when is it better than an inner join?

A `left_semi` join returns the left rows that have at least one match, without adding right-side columns or duplicating rows when there are several matches. It's the DataFrame version of `WHERE EXISTS` and is more efficient than an inner join followed by `distinct`.

#### How do you do a non-equi or range join?

With a condition such as `events.ts.between(periods.start, periods.end)`. Without an equality condition, Spark uses a broadcast nested loop join or a cartesian product, which is slow on large data. Add an equality condition when possible (for example on a date bucket) or broadcast the small side.

#### Practice problem 2: joins

Given these two files:

```csv
user_id;name
1;Wilmer
2;Jayson
```

```csv
user_id;product_id;amount
1;101;12500.0
1;102;8900.0
2;103;3000.0
2;101;5000.0
```

- Load both DataFrames.
- Join them to get user names and transaction amounts.
- Compute the total spent per user.
- Sort by total amount, descending.

```python
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.getOrCreate()
df_users = spark.read.schema("user_id INT, name STRING").options(header=True, delimiter=";").csv("path/to/users")
df_transactions = (spark.read
                   .schema("user_id INT, product_id INT, amount DOUBLE")
                   .options(header=True, delimiter=";")
                   .csv("path/to/transactions"))

df_total_per_user = (df_users.join(df_transactions, on="user_id", how="inner")
                     .groupBy("user_id", "name")
                     .agg(F.sum("amount").alias("total_amount"))
                     .orderBy(F.col("total_amount").desc()))
```

Joining on `"user_id"` keeps a single key column, and grouping by `user_id` as well as `name` avoids merging two different users with the same name.

#### Practice problem 7: find what changed between two snapshots

You receive a full snapshot of a registry every month. Compare this month's snapshot with last month's (both with `company_id`, `name`, `status`) and label each company as new, removed, changed or unchanged.

```python
cols = ["name", "status"]
prev = previous.withColumn("h_prev", F.sha2(F.concat_ws("||", *cols), 256)).select("company_id", "h_prev")
curr = current.withColumn("h_curr", F.sha2(F.concat_ws("||", *cols), 256)).select("company_id", "h_curr")

changes = (curr.join(prev, "company_id", "full")
           .withColumn("change",
                       F.when(F.col("h_prev").isNull(), "new")
                        .when(F.col("h_curr").isNull(), "removed")
                        .when(F.col("h_prev") != F.col("h_curr"), "changed")
                        .otherwise("unchanged")))
```

`concat_ws` skips nulls, so a change from null to an empty string goes unnoticed. Wrap columns in `coalesce(col, lit("<null>"))` if that distinction matters.

<!-- challenge -->

You need customers who placed an order, but the inner join with orders returns customers several times. Which join fits?

<!-- solution -->

A `left_semi` join of customers with orders on `customer_id`: it keeps each matching customer once and adds no order columns.

<!-- takeaways -->

- Semi and anti joins test existence.
- Join on names to avoid duplicate key columns.
- Null keys never match; range joins need care.

<!-- unit: Join strategies -->

<!-- goals -->

- Explain broadcast, shuffle hash and sort-merge joins.
- Use broadcasts, hints and bucketing safely.

<!-- concept -->

How Spark executes a join matters more than which join you write. If one side is small, Spark broadcasts it to every executor and the big side never moves. Otherwise both sides are shuffled by key and then joined by sorting or hashing.

You can steer the choice with hints and thresholds, but broadcasting something that isn't really small can crash the driver or executors. Bucketing pre-shuffles tables on disk so repeated joins on the same key skip the shuffle.

<!-- example -->

```python
enriched = (orders
  .join(F.broadcast(countries), "country_code")     # small dimension: no shuffle of orders
  .join(customers, "customer_id"))                  # large: sort-merge join
enriched.explain()   # look for BroadcastHashJoin vs SortMergeJoin
```

#### What are the join strategies Spark can choose?

- **Broadcast hash join:** the small side is copied to every executor; no shuffle of the large side.
- **Shuffle hash join:** both sides are shuffled by key and the smaller one is hashed per partition.
- **Sort-merge join:** both sides are shuffled and sorted by key, then merged. It's the default for large tables.
- **Broadcast nested loop join and cartesian product:** for non-equi joins and cross joins. They're expensive.

#### What is a broadcast join and when do you use it?

When one side is small enough to fit in executor memory (a dimension or lookup table), Spark sends a copy to every executor so the large side is joined in place, without a shuffle. Spark does it automatically below `spark.sql.autoBroadcastJoinThreshold` (10 MB by default), and AQE can switch to it at runtime. You can force it with a hint.

```python
from pyspark.sql.functions import broadcast

large_df = spark.createDataFrame([("A", 1000), ("B", 2000), ("C", 3000), ("D", 4000)], ["key", "amount"])
small_df = spark.createDataFrame([("A", "Apple"), ("B", "Banana"), ("C", "Cherry")], ["key", "fruit"])

large_df.join(broadcast(small_df), "key", "inner").show()
```

#### What are the risks of broadcasting?

If the "small" table is actually large, broadcasting can run the driver or executors out of memory, because the table is collected to the driver and copied to every executor. Broadcast timeouts (`spark.sql.broadcastTimeout`) can also occur. Only broadcast tables you know stay small.

#### What do join hints do?

They tell the optimizer which strategy to use: `broadcast`, `merge` (sort-merge), `shuffle_hash` and `shuffle_replicate_nl`, through `df.hint("merge")` or SQL `/*+ BROADCAST(t) */`. Use them when statistics are missing or wrong, and recheck after upgrading Spark.

#### What is bucketing?

Writing a table pre-partitioned into a fixed number of buckets by a key (`bucketBy(64, "customer_id").saveAsTable(...)`). Joins and aggregations between tables bucketed the same way on the key can skip the shuffle. It only works with tables saved in the metastore, and on Delta tables liquid clustering has largely replaced it.

#### How do you join many small DataFrames efficiently?

Broadcast them, join in order from most to least selective, and make sure filters run before the joins. If you're joining the same large table repeatedly in a loop, restructure the logic into a single join or a union.

<!-- challenge -->

A join with a 30 MB lookup table shuffles a 2 TB fact table. Statistics aren't available. What do you do?

<!-- solution -->

Add a `broadcast()` hint on the lookup table (or raise `spark.sql.autoBroadcastJoinThreshold` above its size), so the fact table is joined in place without a shuffle.

<!-- takeaways -->

- Broadcast small sides; shuffle large ones.
- Hints steer strategy; check with `explain()`.
- Bucketing pre-shuffles tables joined repeatedly.

<!-- unit: Skewed joins -->

<!-- goals -->

- Recognize skewed joins in the Spark UI.
- Mitigate skew with AQE, broadcasts, salting and separate handling.

<!-- concept -->

Skew happens when a few keys hold a large share of rows. The tasks for those keys run far longer than the rest, often spilling or running out of memory, while the cluster waits. In the Spark UI, it shows as one or a few tasks with huge input next to many small ones.

Adaptive execution splits skewed partitions automatically in many cases. When it doesn't, broadcasting the other side, salting the hot keys or processing them separately fixes it.

<!-- example -->

```python
SALT = 16
hot = orders.withColumn("salt", (F.rand() * SALT).cast("int"))
dim = customers.crossJoin(spark.range(SALT).withColumnRenamed("id", "salt"))
joined = hot.join(dim, ["customer_id", "salt"]).drop("salt")
```

#### What is a skewed join and what are its symptoms?

A join where a few key values hold a large share of the rows, so the tasks handling those keys get far more data than the rest. Symptoms: a stage where most tasks finish in seconds and a few run for minutes or hours, high spill on those tasks, and out-of-memory errors. The Spark UI's task summary (max duration much larger than the median) shows it.

#### How do you mitigate skew?

- Let AQE split skewed partitions (`spark.sql.adaptive.skewJoin.enabled`, on by default).
- Broadcast the other side if it's small.
- Filter out or handle separately the hot keys, often nulls or default values such as `-1` or `"unknown"`.
- **Salt** the key: add a random suffix on the large side and replicate the small side for every suffix.

```python
from pyspark.sql import functions as F

num_salts = 8
large_salted = large_df.withColumn("salt", (F.rand() * num_salts).cast("int"))
small_salted = small_df.crossJoin(spark.range(num_salts).withColumnRenamed("id", "salt"))
joined = large_salted.join(small_salted, ["key", "salt"]).drop("salt")
```

<!-- challenge -->

A join's last task runs for 40 minutes; its key is `customer_id = 0`, used for guest checkouts. What is the simplest fix?

<!-- solution -->

Handle guest rows separately: filter `customer_id = 0` out of the join (they have no customer details), process them on their own, and `unionByName` the results. The remaining join is balanced.

<!-- takeaways -->

- Skew: a few huge tasks among many small ones.
- AQE splits many skewed partitions automatically.
- Salt or separate hot keys when needed.

### Window functions

<!-- unit: Ranking windows -->

<!-- goals -->

- Rank rows with row_number, rank and dense_rank.
- Keep the latest record per key and the top N per group.

<!-- concept -->

Window functions compute over a group of related rows while keeping every row, which makes them the standard tool for "per key" questions. Partition by the key, order by what decides precedence, number the rows, and filter.

The ranking function decides ties: row numbers are unique, ranks repeat for ties. Adding a tiebreaker column makes "latest record" deterministic when timestamps can be equal.

<!-- example -->

```python
w = Window.partitionBy("customer_id").orderBy(F.desc("updated_at"), F.desc("ingested_at"))
latest = (customers_raw
  .withColumn("rn", F.row_number().over(w))
  .where("rn = 1").drop("rn"))
```

#### What is a window function?

A function that computes a value for each row from a group of related rows (the window) without collapsing them, unlike `groupBy`. A window is defined with `Window.partitionBy(...)`, usually `orderBy(...)`, and optionally a frame.

#### What's the difference between row_number, rank and dense_rank?

For tied values in the ordering: `row_number` gives unique consecutive numbers (ties broken arbitrarily), `rank` gives ties the same number and leaves gaps (1, 1, 3), and `dense_rank` gives ties the same number without gaps (1, 1, 2).

#### How do you keep the latest record per key?

Number rows within each key by descending timestamp and keep the first. Add a tiebreaker column to the ordering so the result is deterministic.

```python
from pyspark.sql import Window, functions as F

w = Window.partitionBy("customer_id").orderBy(F.col("updated_at").desc(), F.col("event_id").desc())
latest = (df.withColumn("rn", F.row_number().over(w))
            .filter("rn = 1")
            .drop("rn"))
```

#### How do you get the top N per group?

The same pattern with `rn <= N`. Use `dense_rank` instead of `row_number` if ties at the boundary should all be included.

#### Practice problem 4: deduplication

A `customers_raw` table receives every change to a customer, with `customer_id`, `email`, `updated_at` and `ingested_at`. Build a table with exactly one row per customer: the most recent version, using `ingested_at` to break ties.

```python
w = Window.partitionBy("customer_id").orderBy(F.col("updated_at").desc(), F.col("ingested_at").desc())
customers = (spark.table("customers_raw")
             .withColumn("rn", F.row_number().over(w))
             .filter("rn = 1")
             .drop("rn"))
```

#### Practice problem 5: top products per city

From the sales data in problem 1, return the two products with the highest revenue in each city, including ties.

```python
revenue = df_sales.groupBy("city", "product_id").agg(F.sum("amount").alias("revenue"))
w = Window.partitionBy("city").orderBy(F.col("revenue").desc())
top2 = revenue.withColumn("rank", F.dense_rank().over(w)).filter("rank <= 2")
```

<!-- challenge -->

Deduplication by latest `updated_at` sometimes keeps a different row for the same customer between reruns. Why, and the fix?

<!-- solution -->

Two rows share the same `updated_at`, so `row_number` breaks the tie arbitrarily. Add a deterministic tiebreaker to the ordering (for example `ingested_at` or a sequence number).

<!-- takeaways -->

- Partition by key, order by precedence, number, filter.
- `row_number` is unique; `rank` repeats ties.
- Add tiebreakers for deterministic results.

<!-- unit: Comparing rows over time -->

<!-- goals -->

- Use lag and lead to compare with previous and next rows.
- Compute running totals, differences and sessions.

<!-- concept -->

Ordered windows answer "compared with before" questions. Looking one row back gives day-over-day differences; a running sum gives cumulative totals; comparing each event's time with the previous one finds gaps, and a running count of gaps assigns session numbers.

All of these need a partition (per store, per user) and an order, or Spark puts every row in one partition on one task.

<!-- example -->

```python
w = Window.partitionBy("user_id").orderBy("event_time")
sessions = (events
  .withColumn("prev_time", F.lag("event_time").over(w))
  .withColumn("new_session",
      (F.col("prev_time").isNull() |
       (F.col("event_time").cast("long") - F.col("prev_time").cast("long") > 1800)).cast("int"))
  .withColumn("session_id", F.sum("new_session").over(w)))
```

#### What do lag and lead do?

They return the value from a previous (`lag`) or following (`lead`) row in the window ordering, with an optional offset and default value. They're used for differences between consecutive rows, detecting changes and building validity ranges.

#### How do you compute a running total and a day-to-day difference?

```python
from pyspark.sql import Window, functions as F

sales_df = spark.createDataFrame([
    ("2024-01-01", "A", 10), ("2024-01-02", "A", 15), ("2024-01-03", "A", 7),
    ("2024-01-01", "B", 20), ("2024-01-02", "B", 5),
], ["date", "store", "revenue"])

w = Window.partitionBy("store").orderBy("date")
result = (sales_df
          .withColumn("running_revenue", F.sum("revenue").over(w))
          .withColumn("day_to_day_diff", F.col("revenue") - F.lag("revenue").over(w)))
result.show()
```

The first row of each store has a null difference, because there's no previous row.

#### How do you detect sessions or gaps between events?

Use `lag` to get the previous event time, flag a new session when the gap exceeds a threshold, and take a running sum of the flags as the session number.

```python
w = Window.partitionBy("user_id").orderBy("event_ts")
sessions = (events
    .withColumn("prev_ts", F.lag("event_ts").over(w))
    .withColumn("new_session",
                (F.col("prev_ts").isNull() |
                 (F.col("event_ts").cast("long") - F.col("prev_ts").cast("long") > 1800)).cast("int"))
    .withColumn("session_id", F.sum("new_session").over(w)))
```

#### Practice problem 3: window functions

Using the `sales_df` DataFrame from the window functions section (date, store, revenue), calculate the cumulative revenue over time for each store and the difference from the previous day.

```python
from pyspark.sql import Window, functions as F

w = Window.partitionBy("store").orderBy("date")
window_revenue = (sales_df
                  .withColumn("cumulative_revenue", F.sum("revenue").over(w))
                  .withColumn("day_to_day_diff", F.col("revenue") - F.lag("revenue").over(w)))
window_revenue.show()
```

<!-- challenge -->

A running total per store is computed with `Window.orderBy("date")` and no partition, and Spark warns about moving all data to a single partition. What is wrong?

<!-- solution -->

Without `partitionBy("store")`, the window covers all rows, so Spark sorts everything in one task and the total runs across stores. Partition by store (and order by date).

<!-- takeaways -->

- `lag`/`lead` compare with neighboring rows.
- Running sums and gap flags build sessions.
- Always partition windows when possible.

<!-- unit: Frames and cost -->

<!-- goals -->

- Define frames with rowsBetween and rangeBetween, and know the default.
- Compute moving averages and buckets, and understand window costs.

<!-- concept -->

An ordered window's frame decides which rows each calculation sees. The default runs from the partition start to the current row, including ties, which is right for running totals and surprising for "last value". Row frames count rows; range frames cover a span of values, which handles missing days in time series correctly.

Every distinct partitioning needs a shuffle and a sort, so many different windows in one query multiply cost.

<!-- example -->

```python
day = F.col("sale_date").cast("timestamp").cast("long") / 86400
w7 = Window.partitionBy("store").orderBy(day).rangeBetween(-6, 0)
smoothed = sales.withColumn("avg_7d", F.avg("revenue").over(w7)) \
                .withColumn("quartile", F.ntile(4).over(Window.partitionBy("store").orderBy("revenue")))
```

#### What is a window frame?

The set of rows, relative to the current one, that an aggregate uses: `rowsBetween(start, end)` counts physical rows, `rangeBetween(start, end)` uses the values of the ordering column. Use `Window.unboundedPreceding`, `Window.currentRow` and `Window.unboundedFollowing` as bounds.

#### What is the default frame, and why does it surprise people?

With `orderBy`, the default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. With ties in the ordering column, all tied rows are included, so a "running" sum can jump. And `last()` over the default frame returns the current row, not the last row of the partition. Without `orderBy`, the frame is the whole partition.

#### How do you compute a 7-day moving average?

Order by a numeric version of the date and use a range frame, so missing days are handled correctly.

```python
w = (Window.partitionBy("store")
           .orderBy(F.col("date").cast("timestamp").cast("long"))
           .rangeBetween(-6 * 86400, 0))
df.withColumn("avg_7d", F.avg("revenue").over(w))
```

#### What do ntile and percent_rank do?

`ntile(n)` splits the ordered rows into n roughly equal buckets (quartiles with 4); `percent_rank` gives each row's relative rank from 0 to 1; `cume_dist` gives the fraction of rows with a value less than or equal to the current one.

#### Why can window functions be expensive?

Each distinct `partitionBy` requires a shuffle and a sort. A window without `partitionBy` moves all the data into a single partition, which is slow and can run out of memory; Spark logs a warning when that happens. Reuse the same window specification for several columns so Spark sorts once.

<!-- challenge -->

A 7-day moving average uses `rowsBetween(-6, 0)`, and on stores closed some days it averages more than 7 calendar days. How do you fix it?

<!-- solution -->

Use a range frame over a numeric day value (`rangeBetween(-6, 0)` on days since epoch), so the frame covers 7 calendar days regardless of missing rows.

<!-- takeaways -->

- Default frame: partition start to current row.
- Row frames count rows; range frames cover values.
- Each distinct window partitioning costs a shuffle.

### Spark SQL and the catalog

<!-- unit: SQL on DataFrames -->

<!-- goals -->

- Run SQL on DataFrames through temporary views.
- Pass parameters safely and reuse logic with CTEs and functions.

<!-- concept -->

DataFrames and SQL are two front ends to the same engine: a temporary view lets SQL query a DataFrame, and SQL results are DataFrames again. Teams mix both freely, choosing whichever reads better for each step.

Two habits keep SQL safe and maintainable: pass values as parameters instead of formatting strings, which avoids injection and quoting bugs, and structure long queries with CTEs or reusable functions.

<!-- example -->

```python
orders.createOrReplaceTempView("orders")
top = spark.sql("""
    WITH paid AS (SELECT * FROM orders WHERE status = 'paid' AND ordered_at >= :since)
    SELECT customer_id, sum(amount) AS revenue FROM paid GROUP BY customer_id
    ORDER BY revenue DESC LIMIT 10
""", args={"since": "2026-10-01"})
```

#### How do you run SQL on a DataFrame?

Register it as a temporary view and query it with `spark.sql`. The result is a DataFrame, so SQL and the DataFrame API can be mixed freely; both compile to the same plan.

```python
df.createOrReplaceTempView("sales")
top = spark.sql("""
    SELECT city, SUM(amount) AS revenue
    FROM sales
    GROUP BY city
    ORDER BY revenue DESC
""")
```

#### What is the difference between a temp view and a global temp view?

A temp view exists only in the SparkSession that created it. A global temp view is shared across sessions in the same application and lives in the `global_temp` database (`SELECT * FROM global_temp.my_view`). Neither persists after the application ends.

#### How do you pass parameters to spark.sql safely?

Use parameterized queries (Spark 3.4+), not string formatting, to avoid SQL injection and quoting bugs.

```python
spark.sql("SELECT * FROM sales WHERE city = :city AND amount > :min",
          args={"city": "Bogotá", "min": 8000})
```

#### What are common table expressions in Spark SQL?

`WITH name AS (...)` blocks that make complex queries readable. Spark inlines them in the plan; a CTE referenced several times may be computed several times unless the optimizer reuses it, so cache or materialize heavy ones if needed.

#### Can you define SQL functions for reuse?

Yes. Register Python functions as UDFs with `spark.udf.register` to call them from SQL, or create SQL functions with `CREATE FUNCTION ... RETURN ...`, which stay inside the engine and are faster than Python UDFs.

<!-- challenge -->

A job builds SQL with an f-string using a user-provided country name, and fails on "Côte d'Ivoire". What do you change?

<!-- solution -->

Use a parameterized query (`spark.sql(query, args={"country": value})`), which handles quoting correctly and prevents SQL injection.

<!-- takeaways -->

- Temp views let SQL query DataFrames.
- Use parameters, not string formatting.
- CTEs and SQL functions keep queries readable.

<!-- unit: Tables and the catalog -->

<!-- goals -->

- Distinguish managed and external tables and use the catalog.
- Write to tables and refresh table metadata.

<!-- concept -->

Paths hold files; tables add names, schemas and permissions through a catalog such as the Hive metastore or Unity Catalog. Writing to tables instead of paths lets other engines and people find the data and lets governance apply.

Ownership matters: dropping a managed table deletes its data, while dropping an external table leaves files in place. When files change outside Spark, cached metadata must be refreshed.

<!-- example -->

```python
(daily.write.mode("overwrite")
      .option("overwriteSchema", "true")
      .saveAsTable("analytics.daily_sales"))          # managed table
spark.sql("REFRESH TABLE raw.partner_files")        # files changed outside Spark
spark.catalog.listTables("analytics")
```

#### What is the difference between managed and external tables?

For a managed table, Spark (or the catalog) controls both metadata and data, and `DROP TABLE` deletes the files. For an external table, you specify a location; dropping it removes only the metadata. With Unity Catalog, managed tables also get automatic maintenance features.

#### What is the catalog?

The metadata layer listing databases (schemas), tables, views and functions: the Hive metastore, AWS Glue Data Catalog or Unity Catalog. In PySpark, `spark.catalog` lets you list tables, check existence (`spark.catalog.tableExists`), cache tables and refresh metadata.

#### How do you write to a table instead of a path?

`df.write.mode("overwrite").saveAsTable("analytics.sales")`, or `insertInto` for an existing table (which matches columns by position, not by name, a common source of bugs). With Delta Lake you can also use SQL `MERGE INTO`.

#### What does REFRESH TABLE do?

It invalidates Spark's cached metadata and file listing for a table, needed when files were changed by another process outside Spark. Without it you may see "file not found" errors or stale data.

<!-- challenge -->

Another process adds files to a table's location, but Spark queries keep returning old results. What do you run?

<!-- solution -->

`REFRESH TABLE <name>` (or `spark.catalog.refreshTable`), which invalidates Spark's cached file listing and metadata so new files are seen.

<!-- takeaways -->

- Tables add names and governance to files.
- Dropping managed tables deletes data.
- Refresh tables changed outside Spark.

<!-- stage: Data in and out -->

### Reading and writing data

<!-- unit: Reading files -->

<!-- goals -->

- Read CSV and JSON with explicit options and read modes.
- Choose formats, track source files and handle schema evolution.

<!-- concept -->

Reading is where bad data enters, so it deserves explicit choices: schema, header, delimiter, date formats, and what to do with malformed rows. Permissive mode keeps going and records broken lines; fail-fast stops at the first problem; drop-malformed hides them.

Format choice decides everything downstream. Columnar Parquet with statistics lets Spark read only needed columns and skip blocks; row formats force full scans. Tracking each row's source file makes debugging possible.

<!-- example -->

```python
df = (spark.read
      .schema("user_id INT, product_id INT, amount DOUBLE, city STRING, _corrupt STRING")
      .option("header", True).option("sep", ";")
      .option("mode", "PERMISSIVE").option("columnNameOfCorruptRecord", "_corrupt")
      .csv("s3://landing/sales/")
      .withColumn("source_file", F.col("_metadata.file_path")))
```

#### How do you read a CSV file correctly?

Declare the schema and the options the file needs.

```python
df = (spark.read
      .schema("user_id INT, product_id INT, amount DOUBLE, city STRING")
      .option("header", True)
      .option("delimiter", ";")
      .option("encoding", "UTF-8")
      .option("mode", "PERMISSIVE")
      .csv("path/to/files/"))
```

Note that the schema goes in `.schema()`, not in `.options()`.

#### What are the CSV/JSON read modes?

`PERMISSIVE` (default) sets malformed fields to null and can keep the raw line in a column named by `columnNameOfCorruptRecord`; `DROPMALFORMED` drops bad rows silently; `FAILFAST` raises an error on the first bad row. In production, prefer permissive with a corrupt-record column and quarantine the bad rows explicitly.

#### What file formats does Spark support?

Built in: Parquet, ORC, JSON, CSV, text, Avro (through a bundled module), binary files and JDBC sources. Table formats such as Delta Lake, Apache Iceberg and Apache Hudi add transactions on top of Parquet. Parquet or a table format should be the default for analytics.

#### Why is Parquet the preferred format?

It's columnar and compressed, stores the schema, and keeps min/max statistics per row group. Spark can read only the needed columns (column pruning) and skip row groups that can't match a filter (predicate pushdown), which reads far less data than CSV or JSON.

#### What does input_file_name() do?

It returns the path of the file each row came from (in Unity Catalog, use the `_metadata.file_path` column instead). It's useful for lineage and debugging, for example to trace a bad row back to the file it came from.

#### What is schema evolution and how is it handled?

Changes to the schema over time, such as new columns. Parquet readers can merge schemas (`mergeSchema`), but it's expensive. Table formats handle it explicitly: Delta adds columns with `mergeSchema` on write or schema evolution in `MERGE`. Renames and type changes need explicit migrations.

<!-- challenge -->

A daily CSV feed occasionally has malformed lines. The business wants the load to continue but nothing silently lost. How do you read it?

<!-- solution -->

Read in `PERMISSIVE` mode with an explicit schema and a corrupt-record column, write rows with `_corrupt` not null (and their source file) to a quarantine table, and alert when their count exceeds a threshold.

<!-- takeaways -->

- Declare schema and options when reading text.
- Permissive mode plus quarantine loses nothing.
- Prefer Parquet; track source files.

<!-- unit: Writing files -->

<!-- goals -->

- Choose save modes and partition outputs.
- Avoid small files and overwrite only the partitions a run owns.

<!-- concept -->

Writing decides how expensive every later read will be. Partitioning by a commonly filtered column lets readers skip folders; file sizes around a hundred megabytes or more keep listing and opening costs low. Spark writes at least one file per task per partition, so without a repartition step, output easily explodes into thousands of tiny files.

Save modes decide what happens to existing data. Dynamic partition overwrite replaces only the partitions in the new output, which makes reruns safe.

<!-- example -->

```python
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
(daily.repartition("sale_date")                 # one task per date → few files per partition
      .write.mode("overwrite")
      .partitionBy("sale_date")
      .parquet("s3://lake/silver/daily_sales/"))
```

#### What are the save modes?

`append` adds data, `overwrite` replaces it, `ignore` does nothing if data exists, and `error`/`errorifexists` (the default) fails if data exists. With `overwrite` on a partitioned table, the overwrite mode setting decides how much is replaced.

#### What is dynamic partition overwrite?

With `spark.sql.sources.partitionOverwriteMode=dynamic`, an overwrite replaces only the partitions present in the DataFrame being written, instead of the whole table. It's the safe way to reprocess one day or one country. On Delta, the equivalent is `replaceWhere`.

```python
(df.write.mode("overwrite")
   .option("partitionOverwriteMode", "dynamic")
   .partitionBy("ingest_date")
   .parquet("s3://bucket/sales/"))
```

#### What does partitionBy do when writing?

It creates one directory per value of the given columns (`country=CO/`, `country=PE/`). Queries filtering on those columns read only the matching directories (partition pruning). Use it on low-cardinality columns filtered in most queries, such as a date; partitioning on a high-cardinality column creates millions of small files.

#### What is the small files problem?

Many small files (well below 128 MB) slow down reads, because each file has overhead for listing, opening and reading metadata, and they create many tiny tasks. Causes include over-partitioning, many partitions written per task and frequent small appends. Fix it by repartitioning before writing, compacting (`OPTIMIZE` in Delta) and choosing better partition columns.

#### How do you control the number and size of output files?

Repartition or coalesce before writing (`df.repartition(16)` or `df.repartition("country")`), set `maxRecordsPerFile`, or let the table format handle it (Delta's optimized writes and auto compaction). With AQE, shuffle partitions are coalesced automatically, which also helps.

<!-- challenge -->

A rerun of yesterday's job with `mode("overwrite")` deleted the whole table's history. What should it have used?

<!-- solution -->

Dynamic partition overwrite (`partitionOverwriteMode=dynamic`) with `partitionBy`, so only yesterday's partition is replaced, or `replaceWhere`/`MERGE` on a Delta table.

<!-- takeaways -->

- Partition by common filters; aim for large files.
- Repartition before writing to control files.
- Overwrite only the partitions a run owns.

<!-- unit: Databases, increments and table formats -->

<!-- goals -->

- Read relational databases in parallel and process new files incrementally.
- Use Delta Lake for transactions and upserts.

<!-- concept -->

Reading a database through JDBC without partitioning options uses one connection and one task, however big the cluster. Splitting on a numeric column spreads the read, within what the database tolerates.

For files, re-reading everything each day wastes time; streaming file sources track which files were processed. Plain Parquet folders also lack transactions, so a failed job can leave half-written data. Table formats like Delta add atomic commits, schema enforcement and `MERGE` for upserts.

<!-- example -->

```python
from delta.tables import DeltaTable
target = DeltaTable.forName(spark, "silver.customers")
(target.alias("t")
   .merge(updates.alias("s"), "t.customer_id = s.customer_id")
   .whenMatchedUpdateAll()
   .whenNotMatchedInsertAll()
   .execute())
```

#### How do you read from a relational database?

With the JDBC source. Set `partitionColumn`, `lowerBound`, `upperBound` and `numPartitions` to read in parallel, otherwise a single task reads the whole table. Push filters to the database with a query (`query` option) and keep credentials in a secret store.

```python
df = (spark.read.format("jdbc")
      .option("url", jdbc_url)
      .option("dbtable", "public.orders")
      .option("user", user).option("password", password)
      .option("partitionColumn", "order_id")
      .option("lowerBound", 1).option("upperBound", 50_000_000)
      .option("numPartitions", 16)
      .load())
```

#### How do you read only new files incrementally?

With Structured Streaming on a file source (or Databricks Auto Loader) and a checkpoint, which tracks processed files; with `trigger(availableNow=True)` it runs like a batch job. Alternatives are keeping a watermark of the last processed date or using a table format's change data feed.

#### Why use a table format such as Delta Lake instead of plain Parquet?

Plain Parquet folders have no transactions: a failed job can leave half-written data, concurrent writers can corrupt results, and updates or deletes mean rewriting files manually. Delta, Iceberg and Hudi add ACID transactions, `MERGE`, time travel, schema enforcement and compaction on top of Parquet.

#### How do you upsert into a Delta table from PySpark?

```python
from delta.tables import DeltaTable

target = DeltaTable.forName(spark, "silver.customers")
(target.alias("t")
   .merge(updates.alias("s"), "t.customer_id = s.customer_id")
   .whenMatchedUpdateAll()
   .whenNotMatchedInsertAll()
   .execute())
```

Deduplicate the source by key first: a `MERGE` fails if several source rows match the same target row.

<!-- challenge -->

A JDBC read of a 300 GB table runs for hours with one busy task. What options do you add?

<!-- solution -->

`partitionColumn` (an indexed numeric or date column), `lowerBound`, `upperBound` and `numPartitions` (for example 16), plus `fetchsize`, so Spark opens several parallel range queries.

<!-- takeaways -->

- Partition JDBC reads or they run as one task.
- Streaming file sources process only new files.
- Delta adds transactions and `MERGE`.

<!-- stage: Performance -->

### Partitioning, shuffles and memory

<!-- unit: Shuffles and partitions -->

<!-- goals -->

- Explain shuffles and reduce them.
- Control partition counts with shuffle settings, repartition and coalesce.

<!-- concept -->

A shuffle moves rows across the network so that rows with the same key meet, writing and reading data from disk along the way. It's the most expensive thing Spark does, so filtering and selecting early, broadcasting small tables and avoiding unnecessary distinct or sort operations pay off quickly.

Partition counts shape every stage: input splits decide read parallelism, the shuffle setting decides post-shuffle parallelism, and repartition or coalesce adjust it explicitly, the first with a shuffle, the second without.

<!-- example -->

```python
spark.conf.set("spark.sql.shuffle.partitions", "400")     # ~150 MB per partition for ~60 GB shuffled
slim = events.select("user_id", "event_type", "event_time").where("event_date = '2026-10-17'")
per_user = slim.groupBy("user_id").count()                 # one shuffle on a small projection
per_user.coalesce(8).write.mode("overwrite").parquet("out/")   # fewer files, no extra shuffle
```

#### What is a shuffle and why is it expensive?

A shuffle redistributes data across the cluster so rows with the same key end up in the same partition. Each task writes its output to local disk in blocks per target partition, and the next stage's tasks fetch those blocks over the network. It costs disk I/O, network transfer, serialization and memory, and in extreme cases it causes job failures. It's usually the most expensive part of a job.

#### How can you reduce shuffles?

- Use narrow transformations where possible and filter and select columns early.
- Broadcast small tables in joins.
- Aggregate before joining when possible.
- Avoid unnecessary `repartition`, `distinct` and `orderBy`.
- Reuse partitioning: bucketed or co-partitioned data can skip shuffles.
- Use `reduceByKey` instead of `groupByKey` with RDDs.

#### What does spark.sql.shuffle.partitions control?

The number of partitions after a shuffle in DataFrame operations (200 by default). Too many for small data creates tiny tasks; too few for large data creates huge partitions that spill. AQE coalesces partitions automatically after the shuffle, so a higher starting value is usually safe.

#### What do repartition and coalesce do?

- **`repartition(n)`** or `repartition(n, "col")` does a full shuffle and produces n roughly even partitions (hash partitioned by the columns if given). It can increase or decrease the number of partitions.
- **`coalesce(n)`** merges existing partitions without a full shuffle, so it can only decrease them. It's cheaper but can leave uneven partitions, and it can reduce the parallelism of the preceding stage.

#### When should you use repartitionByRange?

When you need data sorted into ranges of a column, for example before writing files that should each cover a range of dates or IDs, which improves data skipping. It samples the data to choose range boundaries.

#### How many partitions does a file read produce?

Roughly the total size divided by `spark.sql.files.maxPartitionBytes` (128 MB by default), adjusted by `spark.sql.files.openCostInBytes`, which packs small files together. A non-splittable file (such as a gzip-compressed CSV) always becomes a single partition, however large it is.

<!-- challenge -->

A job writes its final output with `coalesce(1)` to get a single file, and the last stage runs on one task for an hour. What do you change?

<!-- solution -->

`coalesce(1)` pulls the whole computation of that stage onto one task. Use `repartition(1)` (adds a shuffle but keeps upstream parallel), write several files, or avoid single-file output if the consumer can read a folder.

<!-- takeaways -->

- Shuffles are Spark's main cost.
- Filter and select before shuffling.
- Repartition shuffles; coalesce merges without one.

<!-- unit: Memory and failures -->

<!-- goals -->

- Explain how executor memory is divided and what spill is.
- Diagnose driver and executor out-of-memory errors.

<!-- concept -->

Executor memory is shared between execution (shuffles, sorts, joins) and storage (cache), with overhead outside the heap for Python workers and buffers. When execution memory runs short, Spark spills to disk, which is slow but survives. Errors come when even that isn't enough, or when off-heap usage exceeds the container's limit.

The driver fails for different reasons: collecting large results, broadcasting tables that aren't small, or planning enormous queries.

<!-- example -->

| Symptom | Likely cause |
|---|---|
| Driver OOM after `collect()` / `toPandas()` | Too much data pulled to the driver |
| Executor OOM on a few tasks | Skewed partitions |
| "Container killed... exceeding memory limits" | Python/off-heap overhead too small |
| Large "Spill (disk)" in stage metrics | Partitions too big for execution memory |

#### How is executor memory divided?

The JVM heap minus 300 MB of reserved memory is split: `spark.memory.fraction` (0.6) is unified memory shared by execution (shuffles, joins, sorts, aggregations) and storage (cache), where storage can be evicted down to `spark.memory.storageFraction` (0.5). The rest is user memory. Outside the heap there's overhead memory (`spark.executor.memoryOverhead`, 10% or at least 384 MB), which also covers Python worker processes.

#### Why do PySpark jobs sometimes fail with container memory errors when the heap is fine?

Python workers run outside the JVM heap, in the overhead area. Heavy Python UDFs, pandas UDFs with large batches or `toPandas` on executors can exceed it, and YARN or Kubernetes kills the container. Increase `spark.executor.memoryOverhead` or set `spark.executor.pyspark.memory`, and reduce Arrow batch sizes.

#### What is spill?

When execution memory isn't enough for a shuffle, sort or aggregation, Spark writes intermediate data to disk and reads it back later. The Spark UI shows it as "spill (memory)" and "spill (disk)". Spill slows tasks dramatically; reduce it with more, smaller partitions, more memory per core or less data per task.

#### What causes OutOfMemoryError on the driver?

Collecting large results (`collect`, `toPandas`), broadcasting a table that's too large, huge query plans (thousands of columns or `withColumn` calls in loops) and tracking very many tasks or files. Avoid pulling data to the driver and keep plans compact.

#### What causes OutOfMemoryError on executors?

Skewed partitions, too few partitions for the data size, large rows or arrays (huge `collect_list` results), too many cores per executor sharing memory, and memory-hungry Python UDFs. Look at the failing stage's task metrics to see whether it's one task (skew) or all of them (sizing).

<!-- challenge -->

A stage shows 400 GB of spill to disk and runs slowly, but doesn't fail. What two changes do you try?

<!-- solution -->

More shuffle partitions so each task handles less data (or let AQE coalesce from a higher starting number), and check for skew; if partitions are balanced, give executors more memory per core.

<!-- takeaways -->

- Execution and storage share executor memory.
- Spill is slow; OOM means even spill wasn't enough.
- Driver OOMs come from collecting and big broadcasts.

<!-- unit: Caching and checkpoints -->

<!-- goals -->

- Choose between cache and persist and decide when caching pays off.
- Distinguish caching from checkpointing.

<!-- concept -->

Spark recomputes a DataFrame for every action unless told otherwise. Caching keeps the computed result in memory or on disk so later actions reuse it, which helps when an expensive result feeds several outputs, and wastes memory when it's used once.

Caching keeps lineage, so lost partitions are recomputed. Checkpointing writes the data out and cuts the lineage, useful for very long or iterative plans.

<!-- example -->

```python
features = expensive_join(orders, customers).cache()
features.count()                                   # materialize once
features.write.mode("overwrite").parquet("out/features/")
features.groupBy("segment").count().show()         # reuses the cache
features.unpersist()
```

#### What's the difference between cache and persist?

`cache()` stores the data with the default storage level: `MEMORY_ONLY` for RDDs and memory and disk for DataFrames. `persist(level)` lets you choose the level: `MEMORY_ONLY`, `MEMORY_AND_DISK`, `DISK_ONLY`, serialized and replicated variants. Both are lazy: data is cached the first time an action computes it. Release it with `unpersist()`.

#### When is caching worth it?

When the same DataFrame is used by several actions and is expensive to recompute, for example after a costly join used by three different outputs. It isn't worth it for data used once or that's cheap to read, and it takes memory from execution. On Databricks serverless, `cache()` and `persist()` aren't supported; write an intermediate table instead.

#### What's the difference between cache and checkpoint?

Caching keeps the data but also keeps the full lineage, so lost partitions are recomputed. `checkpoint()` writes the data to reliable storage and truncates the lineage, which helps with very long plans (iterative algorithms, loops). `localCheckpoint()` truncates lineage using executor storage, faster but not fault-tolerant.

<!-- challenge -->

A teammate adds `.cache()` after every transformation "to make it faster", and executors start spilling and evicting. What do you advise?

<!-- solution -->

Cache only DataFrames that are expensive and reused by several actions, materialize them once, and `unpersist()` when done. Caching everything wastes memory needed for execution.

<!-- takeaways -->

- Cache results reused by several actions.
- Unpersist when done.
- Checkpoints cut lineage; caches keep it.

### Catalyst, AQE and query plans

<!-- unit: How Catalyst optimizes -->

<!-- goals -->

- Describe Catalyst's role and phases.
- Explain predicate pushdown, column pruning and the cost-based optimizer.

<!-- concept -->

You describe what you want; Catalyst decides how. It resolves names against the catalog, rewrites the logical plan with rules such as pushing filters down and removing unused columns, then chooses physical operators, optionally using table statistics to pick join orders and strategies.

That's why DataFrame code and SQL perform the same, and why opaque Python code can't be optimized. Very long chains of transformations can make planning itself slow.

<!-- example -->

```python
df = (spark.read.parquet("s3://lake/events/")
        .select("user_id", "event_type", "event_date")
        .where("event_date = '2026-10-17'"))
df.explain(mode="formatted")
# FileScan parquet ... PartitionFilters: [event_date = 2026-10-17]
#                      ReadSchema: struct<user_id, event_type, event_date>
```

#### What is the role of the Catalyst optimizer?

Catalyst turns DataFrame and SQL code into an efficient execution plan. It applies rules such as predicate pushdown, column pruning, constant folding and join reordering, then chooses physical operators (for example which join strategy to use). It works on DataFrames, Datasets and SQL, not on RDDs, whose functions are opaque to it.

#### What are the phases of Catalyst?

1. **Analysis:** resolves column and table names and types against the catalog (unresolved logical plan to logical plan).
2. **Logical optimization:** applies rule-based rewrites.
3. **Physical planning:** generates candidate physical plans and picks one, using statistics where available.
4. **Code generation:** whole-stage codegen compiles parts of the plan into JVM bytecode.

#### What are predicate pushdown and column pruning?

**Predicate pushdown** moves filters as close to the data source as possible, so Parquet can skip row groups and JDBC sources can filter in the database. **Column pruning** reads only the columns a query uses. Both happen automatically, unless something blocks them, such as a filter wrapped in a Python UDF.

#### What is the cost-based optimizer?

An optional part of Catalyst that uses table and column statistics (row counts, distinct values, histograms) to choose join order and join strategy. It needs statistics collected with `ANALYZE TABLE ... COMPUTE STATISTICS FOR COLUMNS` and kept up to date.

#### Why can a long chain of transformations make a job slow before it even starts?

Catalyst analyzes and optimizes the entire plan, and very large plans (hundreds of `withColumn` calls, loops that union or join DataFrames repeatedly) can take minutes to optimize or overflow the driver's stack. Combine projections into one `select`, and break long loops with checkpoints or intermediate tables.

<!-- challenge -->

A filter on a Parquet table doesn't appear in `PushedFilters` in the plan, and the job reads everything. What could prevent pushdown?

<!-- solution -->

The filter is applied through a Python UDF, a function on the column, or a type mismatch (for example comparing a date column with a string cast). Rewrite it with built-in functions on the raw column so Catalyst can push it down.

<!-- takeaways -->

- Catalyst analyzes, optimizes and plans queries.
- Pushdown and pruning cut data read.
- Python UDFs and functions on columns block optimization.

<!-- unit: Runtime and physical plans -->

<!-- goals -->

- Explain AQE and dynamic partition pruning.
- Read physical plans, exchanges and whole-stage code generation.

<!-- concept -->

Static plans rely on estimates that may be wrong. Adaptive Query Execution re-plans at runtime using real shuffle statistics: merging tiny partitions, switching joins to broadcast and splitting skewed partitions. Dynamic partition pruning uses a filtered dimension's keys to skip fact partitions.

Reading the physical plan shows what really happens: exchanges mark shuffles or broadcasts, and whole-stage code generation fuses operators into single functions, which is a big part of DataFrame speed.

<!-- example -->

```text
== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=true
+- HashAggregate(keys=[city], functions=[sum(amount)])
   +- AQEShuffleRead coalesced
      +- Exchange hashpartitioning(city, 200)          ← shuffle
         +- *(1) HashAggregate(partial)                ← * = whole-stage codegen
            +- *(1) BroadcastHashJoin [store_id]
               :- *(1) Filter ... FileScan parquet sales
               +- BroadcastExchange                     ← broadcast of stores
```

#### What is Adaptive Query Execution (AQE)?

An optimization layer, on by default since Spark 3.2, that re-plans queries at runtime using actual statistics from completed shuffle stages. It coalesces small shuffle partitions, switches sort-merge joins to broadcast joins when a side turns out to be small, and splits skewed partitions in joins.

#### What is dynamic partition pruning?

When a partitioned fact table is joined with a filtered dimension, Spark uses the dimension's filter result at runtime to prune the fact table's partitions, so it reads only matching partitions. It's on by default and very effective for star-schema queries.

#### How do you read a query plan?

Use `df.explain()` or `df.explain(mode="formatted")` (also `extended`, `cost` and `codegen`). Read the physical plan from the bottom up: scans (look for `PushedFilters`, `PartitionFilters` and `ReadSchema`), `Exchange` nodes (shuffles), join types (`BroadcastHashJoin`, `SortMergeJoin`) and `BatchEvalPython`/`ArrowEvalPython` (Python UDFs).

#### What does an Exchange in the plan mean?

A shuffle (`Exchange hashpartitioning`, `rangepartitioning`) or a broadcast (`BroadcastExchange`). Counting `Exchange` nodes is a quick way to estimate how many shuffles a query does.

#### What is whole-stage code generation?

Tungsten collapses several operators of a stage (scan, filter, project, aggregate) into one generated Java function, removing virtual function calls and intermediate objects. In the plan, operators prefixed with `*` or numbered `WholeStageCodegen` blocks are code-generated.

<!-- challenge -->

A plan shows `Exchange hashpartitioning(customer_id, 2000)`, but the Spark UI shows only 180 tasks in that stage. Is something wrong?

<!-- solution -->

No: AQE coalesced the 2,000 shuffle partitions into 180 based on actual sizes (`AQEShuffleRead coalesced`). It's working as intended.

<!-- takeaways -->

- AQE re-plans with runtime statistics.
- Exchanges are shuffles or broadcasts.
- Whole-stage codegen fuses operators.

### Performance tuning and debugging

<!-- unit: Diagnosing slow jobs -->

<!-- goals -->

- Debug slow jobs from measurements in the Spark UI.
- Map slow stages back to code and explain cold-start effects.

<!-- concept -->

Tuning starts with evidence. The Spark UI shows which stage takes the time, how its tasks are distributed, and whether it shuffles, spills or skews; the SQL tab links plan operators to stages, and named jobs map them to your code.

Most slow jobs share a few causes: reading too much, unnecessary shuffles, skew, spill, small files and Python UDFs. Some slowness is just warm-up: the first run pays for JVM startup, code generation and cold caches.

<!-- example -->

```python
spark.sparkContext.setJobDescription("orders: build daily aggregates")
daily = orders.groupBy("order_date").agg(F.sum("amount").alias("revenue"))
daily.write.mode("overwrite").parquet("out/daily/")
# Spark UI → Jobs: "orders: build daily aggregates" → stages → task summary (max vs median)
```

#### How would you debug a job that takes much longer than expected?

Start with measurements, not guesses:

- Open the Spark UI and find the stage that takes the time.
- Check its task summary: if the maximum duration is far above the median, it's skew; if all tasks are slow, it's sizing or the amount of data.
- Look at shuffle read/write sizes and spill.
- Read the physical plan (`explain`) to see whether filters are pushed down, which join strategies were chosen and whether Python UDFs are involved.
- Fix the biggest problem, measure again, and change one thing at a time.

#### What does the Spark UI show?

The **Jobs** and **Stages** tabs (durations, task summaries, shuffle and spill metrics), **Storage** (cached data), **Environment** (configuration), **Executors** (memory, GC time, failed tasks) and **SQL / DataFrame** (the executed plan with row counts per operator). For finished applications, use the Spark History Server.

#### What are the most common causes of slow Spark jobs?

In rough order: reading too much data (no pruning, CSV/JSON instead of Parquet, many small files), unnecessary or large shuffles, data skew, spill from partitions too large for memory, Python UDFs, collecting data to the driver, and too few or too many partitions.

#### How do you find which part of your code produced a slow stage?

In the SQL / DataFrame tab, the executed plan links operators to stages. Name your jobs with `spark.sparkContext.setJobDescription("load silver companies")` (or `setJobGroup`), so the Jobs tab shows which step each job belongs to.

#### Why is the first run of a job slower than the next ones?

JVM warm-up, class loading, code generation, cluster autoscaling and cold caches (the operating system's file cache and, on Databricks, the disk cache). Measure performance on several runs, and on a realistic data volume.

<!-- challenge -->

A stage's task summary shows median duration 20 s and max 25 min. What does that tell you, and what do you check next?

<!-- solution -->

Skew: one task has far more data. Check the task's input and shuffle read size, find the hot key(s), and apply AQE skew handling, broadcasting or salting.

<!-- takeaways -->

- Measure first: stage, tasks, shuffle, spill.
- Median vs max task time reveals skew.
- Name jobs to map stages to code.

<!-- unit: Anti-patterns and fixes -->

<!-- goals -->

- Recognize common PySpark anti-patterns.
- Avoid unnecessary actions, wide rows and over-processing.

<!-- concept -->

Many slow jobs aren't misconfigured; they do unnecessary work. Collecting data to the driver, using Python UDFs where functions exist, calling `count()` for logging, looping over rows in Python, carrying hundreds of unused columns, or recomputing years of history every day all multiply cost.

The fixes are mostly about doing less: fewer actions, fewer columns, incremental processing and built-in functions.

<!-- example -->

| Anti-pattern | Fix |
|---|---|
| `count()` after every step for logging | Log row counts once, from write metrics |
| Python loop over `collect()` | Column expressions or joins |
| `SELECT *` of 300 columns | Select the 12 you need |
| Rebuild 5 years nightly | Process only new partitions |

#### What PySpark anti-patterns should you avoid?

- `collect()` or `toPandas()` on unbounded data.
- Python UDFs where a built-in function exists.
- `withColumn` in a loop instead of `withColumns` or one `select`.
- Accidental `crossJoin` or joins without a condition.
- `repartition(1)`/`coalesce(1)` on large data, which funnels everything through one task.
- `inferSchema` on large production inputs.
- Calling `count()` just to log a number, which triggers a full extra job.
- Reusing an expensive DataFrame in several actions without caching or materializing it.

#### Why is count() sometimes slow, and when should you avoid it?

`count()` is an action: it runs the whole plan up to that point. Calling it for logging after each step recomputes everything several times. Count once on materialized data, use metrics from the write (table history, Spark UI), or accept approximate counts.

#### What is the effect of too many columns or very wide rows?

Wide rows increase memory per row, shuffle sizes and plan complexity. Select only the needed columns early, avoid carrying large text or binary columns through joins, and split very wide tables if most queries use only a few columns.

#### How do you handle a job that processes much more data than needed?

Process incrementally: read only new files (streaming with `availableNow`, Auto Loader), write only the affected partitions (`replaceWhere`, dynamic overwrite), merge only changed rows, and skip steps whose inputs haven't changed. The cheapest data is the data you don't process.

<!-- challenge -->

A pipeline calls `df.count()` after each of 8 steps to log progress, and runtime doubled. Why, and what do you do?

<!-- solution -->

Each `count()` is an action that recomputes the plan up to that point. Remove them (or cache once if counts are essential), and log counts from the final write or from cheap metrics instead.

<!-- takeaways -->

- Every action recomputes its plan.
- Select fewer columns; avoid Python loops.
- Process incrementally instead of reprocessing history.

<!-- unit: Tuning knobs -->

<!-- goals -->

- Choose shuffle partition counts and use speculation.
- Benefit from data layout and reduce garbage collection.

<!-- concept -->

Once the work itself is lean, a few settings matter. Shuffle partitions should be sized so each holds roughly a hundred to two hundred megabytes, with AQE adjusting from a generous starting point. Speculation reruns tasks stuck on slow machines.

Data layout often beats configuration: tables partitioned or clustered on common filters let Spark skip most data. Garbage collection shrinks with DataFrames instead of Python objects and moderate executor sizes.

<!-- example -->

```properties
spark.sql.adaptive.enabled=true
spark.sql.adaptive.coalescePartitions.enabled=true
spark.sql.shuffle.partitions=2000          # generous start; AQE coalesces
spark.speculation=true
spark.speculation.quantile=0.9
```

#### How do you choose the number of shuffle partitions?

Aim for partitions of roughly 100 to 200 MB after the shuffle and at least two to three times as many partitions as total cores. With AQE on, set a generous starting number (or `spark.sql.adaptive.coalescePartitions.initialPartitionNum`) and let AQE merge small ones.

#### What is speculative execution?

With `spark.speculation=true`, Spark launches backup copies of tasks that run much slower than others in the same stage and uses whichever finishes first. It helps with slow nodes, not with skew, because a skewed task is slow on any node. Outputs must be idempotent.

#### How do you make filters and joins benefit from data layout?

Partition or cluster tables on the columns most queries filter by, and filter directly on the stored columns. A filter such as `to_date(event_ts) = '2026-10-15'` may not prune; `event_date = '2026-10-15'` on a partition or clustering column does. Keep file sizes healthy with compaction.

#### How do you reduce garbage collection time?

Use DataFrames instead of RDDs of Python objects, avoid very large executors (over about 64 GB of heap), use G1GC (the default in recent Java versions), cache in serialized form if caching a lot, and reduce the number of objects created in UDFs. The Executors tab shows the GC time per executor.

<!-- challenge -->

A daily job filters a 10 TB table by `country` and `event_date`, reading 9 TB each time. What layout change helps most?

<!-- solution -->

Partition (or cluster) the table by `event_date`, and cluster or Z-order by `country` within, so the filter prunes partitions and files and reads a small fraction.

<!-- takeaways -->

- Aim for 100–200 MB per shuffle partition.
- Data layout beats most configuration.
- Moderate executors and DataFrames reduce GC.

### UDFs, pandas and Arrow

<!-- unit: Python UDFs and alternatives -->

<!-- goals -->

- Explain why Python UDFs are slow and how to avoid them.
- Write null-safe UDFs and know Python UDTFs.

<!-- concept -->

A Python UDF runs your function row by row in a Python process next to the executor. Every row is serialized out of the JVM and back, and Catalyst can't see inside, so filters can't be pushed through it. That's why built-in functions, including higher-order functions on arrays, should come first.

When a UDF is truly needed, it must handle `None`, since nulls arrive as Python `None`. Python UDTFs extend the idea to functions that return several rows.

<!-- example -->

```python
from pyspark.sql.types import StringType

@F.udf(StringType())
def normalize_phone(p):
    if p is None:
        return None
    digits = "".join(c for c in p if c.isdigit())
    return "+57" + digits[-10:] if len(digits) >= 10 else None

# often no UDF needed:
df = df.withColumn("phone", F.concat(F.lit("+57"), F.substring(F.regexp_replace("phone", r"\D", ""), -10, 10)))
```

#### What is a UDF and why is a Python UDF slow?

A user-defined function applies custom Python code to each row. Each row must be serialized from the JVM to a Python worker, processed by the Python interpreter and serialized back. Catalyst can't see inside it, so it can't optimize or push filters through it. Built-in functions run inside the JVM and are typically many times faster.

```python
from pyspark.sql import functions as F
from pyspark.sql.types import StringType

@F.udf(returnType=StringType())
def clean_city(city):
    return city.strip().title() if city else None

# The built-in version is faster and does the same:
df.withColumn("city", F.initcap(F.trim("city")))
```

#### How do you avoid UDFs?

Search `pyspark.sql.functions` first: string, date, regex, array, map, JSON and higher-order functions cover most needs. Combine them with `when`, `expr` and SQL expressions. Use a pandas UDF if you really need Python libraries, and a row-by-row UDF only as a last resort.

#### Why must UDFs handle None?

Columns can contain nulls, and Python functions receive them as `None`. A UDF that calls `city.strip()` without checking fails the whole job on the first null. Also declare the right return type: a mismatch returns null silently.

#### What is a Python UDTF?

A user-defined table function (Spark 3.5) that returns several rows per input, defined as a Python class with an `eval` method that yields rows. It's useful for parsing or expanding records in ways that `explode` can't express.

<!-- challenge -->

A UDF that uppercases and trims names fails with `AttributeError: 'NoneType' object has no attribute 'strip'`. What are two fixes?

<!-- solution -->

Replace it with built-ins (`F.upper(F.trim("name"))`), which handle nulls; or guard the UDF with `if s is None: return None`.

<!-- takeaways -->

- Python UDFs serialize every row and block optimization.
- Try built-in and higher-order functions first.
- UDFs must handle `None`.

<!-- unit: Vectorized Python with Arrow -->

<!-- goals -->

- Use pandas UDFs, Arrow-optimized UDFs, applyInPandas and mapInPandas.
- Apply ML models in Spark and decide when to switch to pandas.

<!-- concept -->

When Python is unavoidable, process batches instead of rows. Arrow moves data between the JVM and Python in columnar batches, and pandas UDFs receive whole Series or DataFrames, so vectorized pandas and NumPy code runs at near-native speed.

Group-wise functions run arbitrary pandas logic per group, which suits per-entity models or complex transformations. Models are loaded once per batch or partition, not per row. And when data is small after aggregation, plain pandas is simplest.

<!-- example -->

```python
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf("double")
def zscore(v: pd.Series) -> pd.Series:
    return (v - v.mean()) / v.std()

def fit_per_store(pdf: pd.DataFrame) -> pd.DataFrame:
    trend = pdf["revenue"].rolling(7, min_periods=1).mean()
    return pdf.assign(trend=trend)

out = sales.groupBy("store").applyInPandas(fit_per_store, schema="store string, sale_date date, revenue double, trend double")
```

#### What is a pandas UDF?

A vectorized UDF (`@pandas_udf`) that receives pandas Series or DataFrames in batches transferred with Apache Arrow, instead of one row at a time. It's much faster than a row-by-row UDF, and you can use vectorized pandas and NumPy operations inside.

```python
import pandas as pd
from pyspark.sql.functions import pandas_udf

@pandas_udf("double")
def to_cop(amount: pd.Series, rate: pd.Series) -> pd.Series:
    return amount * rate

df.withColumn("amount_cop", to_cop("amount", "fx_rate"))
```

#### What are Arrow-optimized Python UDFs?

Since Spark 3.5, regular Python UDFs can use Arrow for serialization (`@udf(useArrow=True)` or `spark.sql.execution.pythonUDF.arrow.enabled`). The function still processes one row at a time, but data transfer is faster.

#### What do applyInPandas and mapInPandas do?

`groupBy(...).applyInPandas(func, schema)` runs a pandas function on each group as a pandas DataFrame (each group must fit in memory). `mapInPandas(func, schema)` runs a function on an iterator of pandas DataFrames per partition, for example to apply a machine learning model in batches.

#### How do you use a machine learning model in PySpark?

Broadcast the model, or load it once per partition, and apply it with a pandas UDF or `mapInPandas` so predictions are vectorized. MLflow's `spark_udf` wraps a registered model as a Spark UDF.

#### When should you convert to pandas instead?

When the data is already small after aggregation (for example a few thousand rows for a chart or a report) and you need pandas-only functionality. Aggregate in Spark first, then call `toPandas()` on the small result.

<!-- challenge -->

A scikit-learn model is applied with a regular UDF that loads the model inside the function, and scoring 50 million rows takes hours. What do you change?

<!-- solution -->

Use `mapInPandas` (or a pandas UDF) that loads the model once per partition or batch and calls `predict` on whole DataFrames, with the model file broadcast or read from storage once.

<!-- takeaways -->

- Arrow moves data in columnar batches.
- pandas UDFs vectorize Python logic.
- Load models once per partition, not per row.

<!-- stage: Streaming and production -->

### Structured Streaming

<!-- unit: Streaming queries -->

<!-- goals -->

- Describe Structured Streaming's model and components.
- Choose triggers and output modes and explain the checkpoint.

<!-- concept -->

Structured Streaming treats a stream as a table that keeps growing. You write the same DataFrame code as for batch; Spark runs it incrementally on each micro-batch of new data. A query has a source, transformations, a sink, a trigger that decides when batches run, and an output mode that decides what gets written.

The checkpoint stores progress and state, so a restarted query continues exactly where it stopped. Losing it means starting over.

<!-- example -->

```python
q = (spark.readStream.format("kafka")
       .option("kafka.bootstrap.servers", BROKERS).option("subscribe", "orders").load()
       .select(F.from_json(F.col("value").cast("string"), ORDER_SCHEMA).alias("o")).select("o.*")
       .writeStream.format("delta")
       .option("checkpointLocation", "s3://chk/orders_bronze/")
       .trigger(availableNow=True)                 # process what's there, then stop
       .toTable("bronze.orders"))
```

#### What is Structured Streaming?

Spark's stream processing API, which treats a stream as an unbounded table that grows over time. You write the same DataFrame operations as in batch, and Spark runs them incrementally in micro-batches, keeping state and progress in a checkpoint.

#### What are the main components of a streaming query?

A source (`readStream` from Kafka, files, Delta or Auto Loader), transformations, a sink (`writeStream` to Delta, Kafka, files or `foreachBatch`), a trigger, an output mode and a checkpoint location.

```python
query = (spark.readStream.format("kafka")
         .option("kafka.bootstrap.servers", brokers)
         .option("subscribe", "orders")
         .load()
         .select(F.from_json(F.col("value").cast("string"), order_schema).alias("o"))
         .select("o.*")
         .writeStream
         .format("delta")
         .option("checkpointLocation", "s3://bucket/checkpoints/orders")
         .trigger(processingTime="1 minute")
         .toTable("bronze.orders"))
```

#### What triggers are available?

The default runs micro-batches as fast as possible; `processingTime="1 minute"` runs at a fixed interval; `availableNow=True` processes everything available in several batches and stops, which is ideal for scheduled incremental jobs; `once=True` is deprecated in favor of `availableNow`. Continuous mode exists but is experimental and limited.

#### What are the output modes?

`append` writes only new rows (the default; aggregations need a watermark), `update` writes rows that changed since the last trigger, and `complete` rewrites the whole result each time (only for aggregations, and only practical for small results).

#### What is the checkpoint used for?

It stores the offsets processed and the state of stateful operations, so a restarted query continues where it stopped without losing or duplicating data. Each query needs its own checkpoint location, and some query changes (such as changing aggregations) aren't compatible with an existing checkpoint.

<!-- challenge -->

A team runs a streaming job 24/7 although downstream reports refresh once a day. How can they keep the streaming code but cut cost?

<!-- solution -->

Use `trigger(availableNow=True)` and schedule the job daily: it processes all new data incrementally with the same checkpoint, then stops, so the cluster runs only minutes a day.

<!-- takeaways -->

- Streams are unbounded tables processed incrementally.
- Triggers decide when batches run.
- The checkpoint holds progress and state.

<!-- unit: Event time and state -->

<!-- goals -->

- Aggregate by event-time windows with watermarks.
- Deduplicate and join streams with bounded state.

<!-- concept -->

Streaming aggregations need to know when a time window is complete, but events arrive late. A watermark tells Spark how late data may be; windows older than that are finalized, and their state is dropped. Without watermarks, state grows forever.

The same logic applies to deduplication and stream-stream joins: both need state, and both need time bounds so that state can be cleaned. Joining a stream with a static table needs no state at all.

<!-- example -->

```python
per_window = (events
  .withWatermark("event_time", "15 minutes")
  .dropDuplicates(["event_id", "event_time"])
  .groupBy(F.window("event_time", "5 minutes"), "store_id")
  .agg(F.sum("amount").alias("revenue")))
```

#### What is a watermark?

A threshold on event time that tells Spark how late data can arrive (`withWatermark("event_ts", "10 minutes")`). Spark uses it to finalize window aggregations and drop old state. Without a watermark, state for aggregations and stream-stream joins grows forever.

#### How do you aggregate over time windows in a stream?

Group by a `window` (tumbling or sliding) on the event time column, with a watermark.

```python
counts = (events
          .withWatermark("event_ts", "10 minutes")
          .groupBy(F.window("event_ts", "5 minutes"), "store")
          .count())
```

#### How do you deduplicate a stream?

`dropDuplicates(["event_id"])` with a watermark, so the state of seen IDs can be dropped after a while, or `dropDuplicatesWithinWatermark` (Spark 3.5). Without a watermark, the set of seen keys grows without limit.

#### How do you join streams?

Stream-static joins (enriching events with a dimension table) are simple and stateless. Stream-stream joins need watermarks on both sides and a time condition, so Spark knows how long to keep each side's state.

<!-- challenge -->

A streaming deduplication with `dropDuplicates("event_id")` runs fine for weeks, then executors run out of memory. Why?

<!-- solution -->

Without a watermark, Spark keeps every event ID it has ever seen as state. Add a watermark on event time and include the time column in the dedup keys, so old state can be dropped.

<!-- takeaways -->

- Watermarks bound lateness and state.
- Windows group by event time.
- Dedup and stream joins need time bounds.

<!-- unit: Sinks, guarantees and monitoring -->

<!-- goals -->

- Use foreachBatch for batch-style sinks.
- Explain exactly-once guarantees and monitor streaming queries.

<!-- concept -->

Streaming promises exactly-once results when the source can replay data and the sink writes idempotently or transactionally; the checkpoint ties the two together. For sinks without native streaming support, such as `MERGE` into a table or writes to several places, `foreachBatch` hands you each micro-batch as a regular DataFrame.

Running streams need watching: input rates, batch durations and state size show whether a query keeps up or slowly falls behind.

<!-- example -->

```python
def upsert(batch_df, batch_id):
    (DeltaTable.forName(spark, "silver.orders").alias("t")
       .merge(batch_df.alias("s"), "t.order_id = s.order_id")
       .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())

q = stream.writeStream.foreachBatch(upsert).option("checkpointLocation", CHK).start()
print(q.lastProgress["inputRowsPerSecond"], q.lastProgress["batchDuration"])
```

#### What does foreachBatch do?

It gives you each micro-batch as a regular DataFrame plus a batch ID, so you can use batch APIs that streaming sinks don't support: `MERGE` into Delta, writing to several sinks, or calling external systems. Make the function idempotent, for example using the batch ID, because a batch can be re-run after a failure.

```python
def upsert(batch_df, batch_id):
    (DeltaTable.forName(spark, "silver.orders").alias("t")
       .merge(batch_df.alias("s"), "t.order_id = s.order_id")
       .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())

stream.writeStream.foreachBatch(upsert).option("checkpointLocation", ckpt).start()
```

#### What guarantees does Structured Streaming provide?

End-to-end exactly-once processing when the source is replayable (Kafka, files) and the sink is idempotent or transactional (Delta, file sinks, idempotent `foreachBatch`). With non-idempotent sinks (calling an API), you get at-least-once.

#### How do you monitor a streaming query?

`query.status`, `query.lastProgress` and `query.recentProgress` show input rate, processing rate, batch duration and state size. The Structured Streaming tab in the Spark UI charts them, and `StreamingQueryListener` sends the metrics to monitoring systems. Alert when the processing rate stays below the input rate.

<!-- challenge -->

A `foreachBatch` function appends each batch to a table. After a failure and restart, some rows appear twice. Why, and the fix?

<!-- solution -->

On restart, the last batch can be replayed, and a plain append isn't idempotent. Use `MERGE` on a key, or write with the batch ID (for example Delta `txnAppId`/`txnVersion`) so replays are skipped.

<!-- takeaways -->

- Exactly-once needs replayable sources and idempotent sinks.
- `foreachBatch` enables MERGE and multi-sink writes.
- Monitor input rate, batch duration and state.

### Testing and best practices

<!-- unit: Testing PySpark code -->

<!-- goals -->

- Structure transformations so they're unit-testable.
- Write fast tests with pytest and a local SparkSession.

<!-- concept -->

Testable PySpark code separates logic from I/O: functions take DataFrames and return DataFrames, while reading and writing happen at the edges. Then a small local session and tiny in-memory DataFrames are enough to test each transformation.

Speed comes from sharing one session and lowering shuffle partitions so small tests don't create hundreds of empty tasks. Beyond units, an end-to-end run on small synthetic files and a rerun check catch integration problems.

<!-- example -->

```python
@pytest.fixture(scope="session")
def spark():
    return (SparkSession.builder.master("local[2]")
            .config("spark.sql.shuffle.partitions", "2").getOrCreate())

def test_latest_per_customer(spark):
    rows = [(1, "a@x.com", "2026-10-01"), (1, "b@x.com", "2026-10-05")]
    df = spark.createDataFrame(rows, "customer_id INT, email STRING, updated_at STRING")
    assert [r.email for r in latest_per_customer(df).collect()] == ["b@x.com"]
```

#### How do you structure PySpark code to make it testable?

Write transformations as functions that take and return DataFrames, without reading or writing inside them. Keep jobs thin: they read inputs, call the functions and write the results. Paths, dates and table names are parameters, not constants.

```python
def latest_per_key(df, key, order_col):
    w = Window.partitionBy(key).orderBy(F.col(order_col).desc())
    return df.withColumn("_rn", F.row_number().over(w)).filter("_rn = 1").drop("_rn")
```

#### How do you unit test PySpark code?

With pytest and a session-scoped local SparkSession fixture, small in-memory DataFrames and the comparison helpers in `pyspark.testing` (Spark 3.5): `assertDataFrameEqual` and `assertSchemaEqual`.

```python
import pytest
from pyspark.sql import SparkSession
from pyspark.testing import assertDataFrameEqual

@pytest.fixture(scope="session")
def spark():
    session = (SparkSession.builder.master("local[2]")
               .config("spark.sql.shuffle.partitions", "2")
               .getOrCreate())
    yield session
    session.stop()

def test_latest_per_key(spark):
    df = spark.createDataFrame([(1, "old", 1), (1, "new", 2)], ["id", "v", "ts"])
    expected = spark.createDataFrame([(1, "new", 2)], ["id", "v", "ts"])
    assertDataFrameEqual(latest_per_key(df, "id", "ts"), expected)
```

#### Why set spark.sql.shuffle.partitions low in tests?

With the default of 200, every small test that shuffles creates 200 tiny tasks, which makes the test suite slow. Two to four partitions are enough for small data.

#### What else should tests cover beyond unit tests?

An end-to-end run of the whole pipeline on small synthetic files, idempotence (re-running on the same input changes nothing), edge cases such as nulls, empty inputs, duplicates and malformed rows, and data quality checks on real data in production.

<!-- challenge -->

A test suite of 60 tests takes 15 minutes, mostly waiting on tiny shuffles. What two settings change it most?

<!-- solution -->

A session-scoped SparkSession fixture (start Spark once) and `spark.sql.shuffle.partitions` set to 1–4, so tests don't run 200 tasks per shuffle.

<!-- takeaways -->

- DataFrame in, DataFrame out: easy to test.
- One local session; few shuffle partitions.
- Add end-to-end and rerun tests.

<!-- unit: Production habits -->

<!-- goals -->

- Make jobs idempotent and handle bad records.
- Follow coding conventions and log without slowing jobs.

<!-- concept -->

Production jobs will be rerun, fed bad data and read by colleagues at 3 a.m. Idempotent writes, overwriting the partitions a run owns or merging on keys, make reruns safe. Bad records go to quarantine with enough context to fix them.

Readable code and cheap logging complete the picture: consistent imports and naming, explicit schemas, and logs from the driver about parameters and decisions, not actions triggered just to print counts.

<!-- example -->

```python
log.info("run date=%s input=%s", run_date, input_path)
valid = parsed.where(F.col("_corrupt").isNull())
(parsed.where(F.col("_corrupt").isNotNull())
       .withColumn("run_date", F.lit(run_date))
       .write.mode("append").saveAsTable("quarantine.orders"))
valid.write.mode("overwrite").option("replaceWhere", f"order_date = '{run_date}'").saveAsTable("silver.orders")
```

#### How do you make jobs idempotent?

Write with `overwrite` of specific partitions, `replaceWhere` or `MERGE` instead of blind `append`, derive outputs only from inputs (no `current_date()` deciding what to process unless it's a parameter), and use deterministic keys. A re-run after a failure should produce exactly the same result.

#### What are good coding conventions for PySpark?

Import functions as `F`, prefer column expressions over strings when building logic, use explicit schemas, chain transformations inside parentheses instead of backslashes, give aggregations readable aliases, avoid `select("*")` before writing, and keep business rules in named functions with tests.

#### How do you log useful information without slowing the job?

Log at the driver: parameters, input paths, plan decisions and timings. Avoid actions just for logging; use write metrics, table history or a single count of the final output. Use `setJobDescription` so logs and the Spark UI line up.

#### How do you handle bad records in production?

Read in permissive mode with a corrupt-record column, validate rows with explicit rules, route failures to a quarantine table with the reason, and stop the job if the share of bad rows exceeds a threshold. Silent drops (`DROPMALFORMED`) hide problems.

<!-- challenge -->

A job appends each day's data with `mode("append")`, and a rerun after a failure doubled yesterday's revenue. How do you make reruns safe?

<!-- solution -->

Replace only the run's slice: `replaceWhere` on the date (Delta), dynamic partition overwrite, or `MERGE` on the business key, so running twice gives the same result.

<!-- takeaways -->

- Idempotent writes make reruns safe.
- Quarantine bad records with context.
- Log at the driver; avoid actions for logging.
