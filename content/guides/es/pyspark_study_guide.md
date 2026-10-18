## Guía de estudio de PySpark

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de PySpark: unas 200 preguntas](../../images/pyspark_study_guide_title_img.png)

Unas 200 preguntas sobre PySpark para entrevistas de ingeniería de datos: la arquitectura de Spark, SparkSession y los RDD, DataFrames y funciones de columna, agregaciones, joins, funciones de ventana, Spark SQL, lectura y escritura de datos, particionado y shuffles, el optimizador Catalyst y AQE, optimización del rendimiento, UDF y pandas, Structured Streaming, pruebas y problemas prácticos. Los ejemplos usan Spark 3.5 y 4.x.

La guía sigue una ruta de aprendizaje en cinco etapas. Cada sección se divide en unidades cortas: objetivos de aprendizaje, una explicación del concepto y un ejemplo resuelto, luego preguntas (primero de memoria, después de aplicación), un reto práctico e ideas clave. Para **aprender**, lee cada unidad de principio a fin. Para **repasar**, cambia al modo repaso o usa "Ir a las preguntas", marca las respuestas que quieras volver a ver y prueba un repaso mixto entre secciones.

<!-- QA -->
<!-- stage: Fundamentos -->

### Fundamentos y arquitectura de Spark

<!-- unit: Qué es Spark -->

<!-- goals -->

- Explicar qué son Spark y PySpark y cuándo valen la pena.
- Conocer Spark Connect y lo que cambió Spark 4.0.

<!-- concept -->

Spark procesa datos que no caben en una máquina dividiéndolos en particiones y trabajándolas en paralelo en un clúster. PySpark te deja describir ese trabajo en Python, mientras el trabajo pesado corre en el motor JVM de Spark, así que el código Python sobre todo arma un plan en lugar de tocar filas.
Esa división explica cuándo vale la pena Spark: datos grandes, pipelines batch o streaming, transformaciones amplias. Para unos pocos gigabytes, pandas o DuckDB en una máquina es más simple y rápido. Las versiones recientes desacoplan clientes y clústeres y endurecen el comportamiento del SQL.

<!-- example -->

```python
from pyspark.sql import SparkSession, functions as F
spark = SparkSession.builder.appName("daily_sales").getOrCreate()
sales = spark.read.parquet("s3://lake/sales/")              # nothing read yet
daily = sales.groupBy("sale_date").agg(F.sum("amount").alias("revenue"))
daily.write.mode("overwrite").parquet("s3://lake/marts/daily_sales/")   # runs now
```

#### ¿Qué es Apache Spark?

Un motor de procesamiento distribuido para datos a gran escala. Divide los datos en particiones y las procesa en paralelo en un clúster, manteniendo los resultados intermedios en memoria cuando es posible. Ofrece API en Python (PySpark), Scala, Java, R y SQL, y bibliotecas para SQL, streaming y machine learning.

#### ¿Qué es PySpark?

La API de Python para Spark. Tu código Python construye un plan de consulta; el trabajo real se ejecuta en el motor de Spark, basado en la JVM. Solo las UDF de Python y las funciones de pandas se ejecutan en procesos worker de Python, y por eso las funciones integradas son más rápidas que el código Python.

#### ¿Cuáles son los conceptos clave de Spark con los que empieza toda entrevista?

- **Transformación:** una operación sobre un DataFrame o RDD que devuelve un nuevo DataFrame o RDD (`filter`, `select`, `join`). Es perezosa.
- **Acción:** una operación que devuelve un valor al driver o escribe datos (`count`, `collect`, `show`, `write`). Dispara la ejecución.
- **Optimizador Catalyst:** el componente que analiza todas las transformaciones solicitadas y determina la forma más eficiente de ejecutarlas juntas.

#### ¿Qué es la evaluación perezosa (lazy evaluation)?

Las transformaciones no se ejecutan cuando las llamas; Spark solo las registra en un plan lógico. Cuando se llama una acción, Catalyst analiza toda la cadena de transformaciones y construye un plan de ejecución optimizado. Así Spark puede combinar pasos, llevar los filtros hasta la fuente y omitir columnas innecesarias.

#### ¿Qué son el driver y los executors?

El **driver** ejecuta tu programa, construye el plan, lo divide en jobs, stages y tareas, y planifica las tareas. Los **executors** son procesos JVM en los nodos worker que ejecutan tareas, guardan datos en caché y reportan al driver. Una aplicación Spark tiene un driver y muchos executors.

#### ¿Qué es un gestor de clúster (cluster manager)?

El sistema que asigna recursos (CPU, memoria) a los executors de Spark: Spark standalone, Hadoop YARN o Kubernetes. El soporte de Mesos se declaró obsoleto y se eliminó en Spark 4.0. Las plataformas gestionadas (Databricks, EMR, Dataproc, Glue) se encargan de esto por ti.

<!-- challenge -->

Un equipo usa un clúster Spark de 20 nodos para procesar un CSV de 2 GB una vez al día, y los jobs tardan 6 minutos, casi todo en arranque. ¿Qué sugieres?

<!-- solution -->

Usar una herramienta de una sola máquina (pandas, Polars o DuckDB) o un Spark pequeño de un nodo: 2 GB caben en memoria, y el arranque y la coordinación del clúster dominan el tiempo. Deja Spark para datos que superen una máquina.

<!-- takeaways -->

- Spark paraleliza el trabajo por particiones en un clúster.
- PySpark arma planes; el motor JVM los ejecuta.
- Los datos pequeños van más rápido en una máquina.

<!-- unit: Evaluación perezosa y el DAG -->

<!-- goals -->

- Explicar transformaciones, acciones y evaluación perezosa.
- Distinguir transformaciones narrow y wide y qué son las particiones.

<!-- concept -->

Spark espera todo lo que puede. Las transformaciones solo registran lo que quieres; las acciones, como escribir o contar, disparan la ejecución. Esperar le permite a Spark ver todo el plan y optimizarlo, por ejemplo empujando filtros hacia la fuente.
El plan es un grafo de operaciones sobre particiones. Las operaciones narrow, como los filtros, trabajan cada partición por separado; las wide, como agrupar, necesitan juntas las filas con la misma clave, lo que obliga a un shuffle en el clúster. En los shuffles está la mayor parte del costo y del ajuste.

<!-- example -->

```python
df = spark.read.parquet("events/")          # transformation (lazy)
clicks = df.filter(F.col("type") == "click") # narrow
by_user = clicks.groupBy("user_id").count()  # wide: shuffle by user_id
by_user.show(5)                              # action: the job runs here
```

#### ¿Cuál es la diferencia entre los modos de despliegue client y cluster?

En **modo client** el driver se ejecuta en la máquina que envió la aplicación (útil para trabajo interactivo; la aplicación muere si esa máquina se desconecta). En **modo cluster** el driver se ejecuta dentro del clúster, que es la opción correcta para jobs de producción.

#### ¿Qué son los jobs, stages y tareas?

Cada acción crea un **job**. El job se divide en **stages** en los límites de shuffle: las operaciones dentro de un stage pueden ejecutarse sin mover datos entre executors. Cada stage ejecuta una **tarea** por partición, y las tareas son la unidad de trabajo que se envía a los executors.

#### ¿Qué pasa desde el momento en que se llama una acción?

1. Catalyst convierte las transformaciones en un plan lógico, lo optimiza y elige un plan físico.
2. El DAG scheduler recorre el plan desde la acción hacia las fuentes y lo divide en stages donde se necesita un shuffle.
3. Cada stage se convierte en un conjunto de tareas, una por partición.
4. El task scheduler envía las tareas a los executors, prefiriendo los que ya tienen los datos (localidad de datos).
5. Los stages se ejecutan en orden; un stage que depende de un shuffle espera a que el stage anterior haya escrito sus archivos de shuffle.

#### ¿Qué es el DAG?

El grafo dirigido acíclico de operaciones que Spark construye a partir de tus transformaciones. El scheduler lo usa para determinar los stages, las dependencias y lo que puede ejecutarse en paralelo, y para recalcular particiones perdidas tras una falla.

#### ¿Cuál es la diferencia entre transformaciones narrow y wide?

Las transformaciones **narrow** calculan cada partición de salida a partir de una sola partición de entrada, así que no se mueven datos entre executors: `filter`, `select`, `map`, `union`, `withColumn`. Las transformaciones **wide** necesitan datos de muchas particiones, lo que requiere un shuffle: `groupBy`, `join` (salvo broadcast), `distinct`, `orderBy`, `repartition`, `reduceByKey`. Las wide son más costosas, pero a menudo inevitables.

<!-- challenge -->

Un notebook corre cinco transformaciones rápido y luego `show()` tarda cuatro minutos. Un colega cree que `show()` es lento. ¿Qué pasa en realidad?

<!-- solution -->

Las celdas anteriores solo armaron un plan; `show()` es la primera acción, así que corre todo el pipeline (lecturas, filtros, shuffles). El tiempo pertenece a las transformaciones, no a `show()`.

<!-- takeaways -->

- Las transformaciones son perezosas; las acciones corren jobs.
- Las narrow se quedan en las particiones; las wide hacen shuffle.
- La pereza le permite a Spark optimizar todo el plan.

<!-- unit: Driver, executors y ejecución -->

<!-- goals -->

- Describir el driver, los executors y el cluster manager.
- Seguir una acción por jobs, stages y tareas, en modo client o cluster.

<!-- concept -->

Una aplicación Spark tiene un driver y muchos executors. El driver corre tu programa, convierte las acciones en jobs, divide los jobs en stages en los límites de shuffle y los stages en tareas, una por partición. Los executors corren las tareas y guardan datos para ellas. Un cluster manager como YARN o Kubernetes aporta las máquinas.
Dónde corre el driver importa en la operación: en la máquina que envía el job en modo client, dentro del clúster en modo cluster, que es lo que necesitan los jobs de producción.

<!-- example -->

```text
action: write()
 └─ job 0
     ├─ stage 0: read + filter + partial agg   → 400 tasks (one per input partition)
     └─ stage 1: final agg + write             → 200 tasks (shuffle partitions)
```

#### ¿Qué es una partición?

Un fragmento de los datos que procesa una sola tarea. El paralelismo es igual al número de particiones procesadas a la vez, limitado por el total de núcleos de los executors. Muy pocas particiones desperdician núcleos; demasiadas agregan sobrecosto de planificación y archivos pequeños.

#### ¿Qué es la localidad de datos?

Spark intenta ejecutar una tarea donde ya están sus datos: en la memoria del mismo executor (`PROCESS_LOCAL`), en el mismo nodo (`NODE_LOCAL`), en el mismo rack o en cualquier lugar. Con almacenamiento de objetos en la nube los datos siempre son remotos, así que la localidad importa menos que con HDFS.

#### ¿Cómo logra Spark la tolerancia a fallas?

Con el linaje: Spark sabe cómo se calculó cada partición, así que si un executor muere, recalcula solo las particiones perdidas desde sus fuentes o desde los archivos de shuffle. Las tareas fallidas se reintentan (`spark.task.maxFailures`, 4 por defecto) y los stages pueden volver a enviarse.

#### ¿PySpark es más rápido que Python puro?

Depende del tamaño de los datos. PySpark suele ser más rápido con conjuntos grandes porque distribuye el trabajo entre muchos nodos y procesa las particiones en paralelo. Con datos pequeños que caben cómodamente en una máquina, Python, pandas o Polars suelen ser más rápidos, porque Spark agrega sobrecosto de planificación, serialización y JVM.

#### ¿Cuándo no deberías usar Spark?

Con conjuntos de datos pequeños (hasta unos pocos gigabytes), búsquedas de baja latencia de una sola fila, cargas transaccionales (OLTP) o jobs simples que una base de datos puede hacer. Un motor de un solo nodo como DuckDB o Polars suele ser más simple y rápido para datos que caben en una máquina.

<!-- challenge -->

La Spark UI muestra un job con 3 stages y 1.200 tareas en total. ¿Cómo sabes dónde están los shuffles?

<!-- solution -->

Cada límite entre stages es un shuffle (o un broadcast exchange): con 3 stages hay 2 límites de shuffle. El detalle de los stages y los nodos `Exchange` de la pestaña SQL muestran qué operaciones los causaron.

<!-- takeaways -->

- El driver planea; los executors corren tareas.
- Los jobs se dividen en stages en los shuffles; los stages, en tareas.
- El modo cluster mantiene el driver dentro del clúster.

<!-- unit: Localidad, tolerancia a fallas y Tungsten -->

<!-- goals -->

- Explicar la localidad de datos y la tolerancia a fallas basada en linaje.
- Describir lo que hace el motor Tungsten.

<!-- concept -->

Spark es rápido y resiliente por razones relacionadas. Intenta correr cada tarea cerca de sus datos, idealmente en la memoria del mismo executor. Cuando falla una tarea o un executor, Spark no necesita copias: sabe cómo se calculó cada partición y recalcula solo las perdidas a partir del linaje.
Por debajo, Tungsten guarda los datos en forma binaria compacta fuera del modelo de objetos de la JVM y genera código para stages completos, y por eso las operaciones de DataFrame son mucho más rápidas que bucles equivalentes en Python.

<!-- example -->

```text
executor 7 dies during stage 2
 → partitions 112–118 lost
 → scheduler reruns their tasks from lineage (stage 1 output or source files)
 → job continues; no full restart
```

#### ¿Qué es Spark Connect?

Una arquitectura cliente-servidor introducida en Spark 3.4. Un cliente liviano envía planes de consulta sin resolver a un servidor Spark remoto mediante gRPC, así que las aplicaciones no necesitan una JVM ni ejecutarse en el clúster. Lo usan Databricks serverless y los clústeres compartidos; algunas API de bajo nivel, como los RDD y `SparkContext`, no están disponibles a través de él.

#### ¿Qué cambió en Spark 4.0 que importe para PySpark?

El modo ANSI SQL está activado por defecto (los casts inválidos y los desbordamientos lanzan errores en lugar de devolver null), hay un tipo `VARIANT` para datos semiestructurados, una API de fuentes de datos en Python, mejoras en Spark Connect, y se eliminó el soporte de Mesos. El código que dependía de nulls silenciosos en casts incorrectos puede necesitar cambios.

#### ¿Qué es el motor Tungsten?

La capa de ejecución de Spark que gestiona la memoria fuera del heap de la JVM en un formato binario compacto y genera bytecode JVM para stages completos de una consulta (generación de código whole-stage). Reduce la recolección de basura y el uso de CPU, y es una de las razones por las que los DataFrames son más rápidos que los RDD.

<!-- challenge -->

Un job con un linaje muy largo (cientos de pasos iterativos) tarda muchísimo en recuperarse cuando falla un executor. ¿Qué puedes hacer?

<!-- solution -->

Cortar el linaje: escribe resultados intermedios en almacenamiento (o usa `checkpoint()`), para que la recuperación recalcule desde el checkpoint en lugar de repetir cientos de pasos.

<!-- takeaways -->

- Spark programa las tareas cerca de sus datos.
- El linaje recalcula las particiones perdidas.
- El formato binario y el codegen de Tungsten hacen rápidos los DataFrames.

### SparkSession, SparkContext y configuración

<!-- unit: Puntos de entrada -->

<!-- goals -->

- Distinguir SparkContext, SparkSession y SQLContext.
- Crear sesiones, usar RDDs desde ellas y entender getOrCreate.

<!-- concept -->

PySpark moderno empieza con una SparkSession, el único punto de entrada para DataFrames, SQL y configuración. El viejo SparkContext sigue existiendo dentro de ella y es la puerta a los RDDs; SQLContext es un resto heredado.
Las sesiones suelen compartirse: `getOrCreate` devuelve la activa si existe, y así los notebooks y librerías evitan crear sesiones en conflicto.

<!-- example -->

```python
spark = (SparkSession.builder
         .appName("orders_etl")
         .config("spark.sql.shuffle.partitions", "64")
         .getOrCreate())
sc = spark.sparkContext                     # RDD API when needed
rdd = sc.parallelize(range(10))
```

#### ¿Cuál es la diferencia entre SparkContext, SparkSession y SQLContext?

Los tres son puntos de entrada al motor:

- **SparkContext:** el punto de entrada original. Se conecta al clúster y gestiona las operaciones sobre RDD.
- **SparkSession:** el punto de entrada moderno y unificado (desde Spark 2.0) para DataFrames y Spark SQL. Contiene un SparkContext, así que las operaciones con RDD siguen siendo posibles mediante `spark.sparkContext`.
- **SQLContext** (y HiveContext): puntos de entrada heredados, reemplazados por SparkSession.

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

#### ¿Cómo creas un SparkContext y una SparkSession?

Un SparkContext recibe una URL de master y un nombre de aplicación, o un `SparkConf` para una configuración detallada. Una SparkSession usa el patrón builder.

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

`local[*]` usa todos los núcleos locales, `local[4]` usa cuatro; `local[0]` no es válido.

#### ¿Cómo trabajas con RDD desde una SparkSession?

Con su SparkContext interno, `spark.sparkContext`. Al terminar, detén la sesión, no el contexto.

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("RDDSparkSession").getOrCreate()
sc = spark.sparkContext
rdd = sc.parallelize([1, 2, 3])
print(rdd.collect())
spark.stop()
```

#### ¿SparkContext soporta DataFrames?

No. Los DataFrames necesitan una SparkSession (o el SQLContext heredado). Un SparkContext por sí solo solo trabaja con RDD.

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DataFrames").getOrCreate()
df = spark.createDataFrame([("AWS Redshift", 2013), ("Apache Spark", 2009)],
                           ["product", "year_of_release"])
df.filter(df.year_of_release > 2010).show()
spark.stop()
```

#### ¿Qué hace getOrCreate()?

Devuelve la SparkSession activa si existe, o crea una nueva. En notebooks y en Databricks ya existe una sesión llamada `spark`, así que `getOrCreate()` la devuelve y la mayoría de las opciones del builder se ignoran.

<!-- challenge -->

Una función de una librería crea su propia SparkSession con otra configuración, y la configuración del notebook parece ignorada. ¿Qué pasa?

<!-- solution -->

`getOrCreate()` devuelve la sesión ya activa, así que se ignoran los ajustes del builder que requieren un contexto nuevo. Configura la sesión una vez al arrancar, o fija las opciones cambiables en ejecución con `spark.conf.set`.

<!-- takeaways -->

- SparkSession es el punto de entrada; SparkContext está adentro.
- Los DataFrames necesitan una sesión.
- `getOrCreate` reutiliza la sesión activa.

<!-- unit: Configurar y enviar -->

<!-- goals -->

- Fijar la configuración al construir, al enviar y en ejecución.
- Enviar aplicaciones con dependencias y controlar los logs.

<!-- concept -->

La configuración puede venir de tres lugares: el builder de la sesión, el comando `spark-submit` y las llamadas en ejecución. Algunos ajustes, como el tamaño de los executors, deben fijarse antes de que arranque la aplicación; los ajustes de SQL pueden cambiar mientras corre.
Las dependencias de Python necesitan cuidado especial porque los executors corren sus propios procesos Python: los paquetes deben llegarles como archivos comprimidos, entornos empaquetados o imágenes de contenedor. Los niveles de log mantienen legible la salida.

<!-- example -->

```bash
spark-submit --master yarn --deploy-mode cluster \
  --conf spark.executor.memory=8g --conf spark.executor.cores=4 \
  --archives pyspark_env.tar.gz#environment \
  --conf spark.pyspark.python=./environment/bin/python \
  jobs/orders_etl.py --date 2026-10-17
```

#### ¿Cómo defines y lees la configuración?

Al construir la sesión con `.config(clave, valor)`, al enviar el job con `--conf clave=valor`, o en tiempo de ejecución para las opciones de SQL con `spark.conf.set("spark.sql.shuffle.partitions", "64")`. Lee un valor con `spark.conf.get(clave)`. Las opciones a nivel de clúster, como la memoria de los executors, no se pueden cambiar una vez iniciada la aplicación.

#### ¿Cuáles son las opciones más importantes de spark-submit?

`--master`, `--deploy-mode`, `--executor-memory`, `--executor-cores`, `--num-executors` (o asignación dinámica), `--driver-memory`, `--conf`, `--py-files` (dependencias en zip o wheel), `--packages` (coordenadas Maven, como conectores) y `--files`.

```bash
spark-submit --master yarn --deploy-mode cluster \
  --executor-memory 8g --executor-cores 4 \
  --conf spark.sql.shuffle.partitions=400 \
  --py-files deps.zip main.py --date 2026-10-17
```

#### ¿Cómo envías las dependencias de Python a los executors?

Con `--py-files` (zips, eggs o wheels), construyendo un entorno virtual empaquetado (venv-pack, conda-pack) y pasándolo con `--archives`, o instalando las bibliotecas en el clúster (bibliotecas de Databricks, bootstrap actions de EMR, una imagen Docker propia en Kubernetes). Cada executor necesita las mismas versiones que el driver.

#### ¿Qué es la asignación dinámica (dynamic allocation)?

Una función que agrega executors cuando hay tareas en espera y elimina los inactivos (`spark.dynamicAllocation.enabled`). Necesita una forma de mantener disponibles los archivos de shuffle cuando se eliminan executors: el servicio externo de shuffle o el seguimiento de shuffle. Ahorra recursos en clústeres compartidos.

<!-- challenge -->

Un job funciona en el driver pero falla en los executors con `ModuleNotFoundError: phonenumbers`. ¿Por qué y cómo lo arreglas?

<!-- solution -->

El paquete solo existe en la máquina del driver. Envíalo a los executors: un entorno virtual empaquetado con `--archives`, `--py-files` para código Python puro o una imagen de contenedor que lo incluya.

<!-- takeaways -->

- Los ajustes vienen del builder, del submit o de la ejecución.
- El tamaño de los executors se fija antes del arranque.
- Las dependencias de Python deben llegar a cada executor.

<!-- unit: Dimensionar recursos -->

<!-- goals -->

- Dimensionar los executors en cores y memoria.
- Usar dynamic allocation para ajustar los recursos al trabajo.

<!-- concept -->

El tamaño de los executors es un equilibrio. Muy pocos cores por executor desperdician el overhead de memoria; demasiados afectan el throughput de I/O y la garbage collection. Unos cuatro o cinco cores con la memoria acorde son un punto de partida común, que se ajusta con métricas.
La carga varía dentro de un job, así que dynamic allocation agrega executors cuando las tareas hacen fila y libera los ociosos, siempre que los datos de shuffle sobrevivan a su eliminación.

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

#### ¿Cómo dimensionas los executors?

Un punto de partida habitual es de 4 a 5 núcleos por executor y memoria suficiente para las tareas de esos núcleos (por ejemplo 4 núcleos con 16 a 32 GB). Los executors muy grandes sufren pausas largas de recolección de basura; los muy pequeños no pueden contener tablas broadcast y desperdician el sobrecosto por executor. Ajusta según el spill y el tiempo de GC que muestra la Spark UI.

#### ¿Cómo cambias el nivel de logs?

Con `spark.sparkContext.setLogLevel("WARN")` en tiempo de ejecución, o con el archivo de configuración de log4j2 del clúster. Reducir el ruido hace que los logs del driver sean más fáciles de leer en los notebooks.

<!-- challenge -->

Un job usa 10 executors de 20 cores y 32 GB cada uno, y pasa el 30 % de su tiempo en garbage collection. ¿Qué cambias?

<!-- solution -->

Usa más executors y más pequeños (por ejemplo 40 de 5 cores y 8–10 GB), lo que reduce el heap por JVM y las pausas de GC y mejora el paralelismo de I/O por core.

<!-- takeaways -->

- Empieza con unos 4–5 cores por executor.
- Los executors muy grandes sufren pausas de GC.
- Dynamic allocation ajusta los recursos a la carga.

### RDD y serialización

<!-- unit: Operaciones con RDDs -->

<!-- goals -->

- Explicar los RDDs y cuándo usarlos todavía.
- Usar map, flatMap, mapPartitions, reduceByKey y conversiones a DataFrames.

<!-- concept -->

Los RDDs son la abstracción original de Spark: colecciones distribuidas de objetos arbitrarios, transformadas con funciones. Dan control total pero ningún optimizador, y en Python cada elemento es un objeto Python enviado entre procesos, así que son mucho más lentos que los DataFrames.
Siguen ayudando con texto no estructurado, particionamiento personalizado o código heredado. La lección clásica de los RDDs aplica en todas partes: combina los valores antes del shuffle, como hace `reduceByKey`, en lugar de mover todo y combinar después.

<!-- example -->

```python
counts = (sc.textFile("logs/*.txt")
            .flatMap(lambda line: line.lower().split())
            .map(lambda w: (w, 1))
            .reduceByKey(lambda a, b: a + b))      # combines per partition before shuffle
top = counts.toDF(["word", "n"]).orderBy(F.desc("n")).limit(10)
```

#### ¿Qué es un RDD?

Un Resilient Distributed Dataset: una colección de objetos inmutable y particionada que puede procesarse en paralelo y reconstruirse a partir de su linaje. Es la API de bajo nivel de Spark; los DataFrames se construyen sobre ella.

#### ¿Cuándo usarías todavía RDD?

Rara vez en código nuevo: para un control fino del particionado, para procesar datos no estructurados que no encajan en un esquema, o con código heredado. Los DataFrames son más rápidos porque Catalyst y Tungsten pueden optimizarlos, y en Python las operaciones con RDD serializan cada registro entre la JVM y Python. Los RDD no están disponibles con Spark Connect.

#### ¿Cuál es la diferencia entre map(), flatMap() y mapPartitions()?

- `map` aplica una función a cada elemento y devuelve un elemento por cada entrada.
- `flatMap` aplica una función que devuelve una secuencia por elemento y aplana los resultados.
- `mapPartitions` aplica una función a una partición completa (un iterador), lo que es útil para una preparación costosa, como abrir una conexión una sola vez por partición.

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

#### ¿Cuál es la diferencia entre reduceByKey y groupByKey?

`reduceByKey` combina los valores de cada clave dentro de cada partición antes del shuffle (una combinación del lado map), así que se mueven muchos menos datos. `groupByKey` envía todos los valores por el shuffle y después los agrupa, lo que usa más red y memoria y puede fallar con claves sesgadas. Prefiere `reduceByKey` o `aggregateByKey` o, mejor aún, las agregaciones de DataFrame.

#### ¿Cómo cuentas palabras con RDD?

```python
counts = (sc.textFile("path/to/text")
            .flatMap(lambda line: line.lower().split())
            .map(lambda word: (word, 1))
            .reduceByKey(lambda a, b: a + b)
            .sortBy(lambda pair: pair[1], ascending=False))
counts.take(10)
```

#### ¿Qué son las variables broadcast?

Valores de solo lectura que se envían una vez a cada executor en lugar de con cada tarea, como un diccionario de búsqueda. Se crean con `sc.broadcast(valor)` y se leen con `.value` dentro de las funciones. Para joins de DataFrames, usa en su lugar la pista de join `broadcast()`.

#### ¿Qué son los acumuladores?

Variables a las que las tareas solo pueden sumar y que solo el driver puede leer, usadas como contadores, por ejemplo de filas mal formadas. Las actualizaciones hechas dentro de transformaciones pueden aplicarse más de una vez si se reintenta una tarea; solo las actualizaciones dentro de acciones se garantizan exactamente una vez.

<!-- challenge -->

Un job con RDDs usa `groupByKey().mapValues(sum)` y se queda sin memoria en unas pocas claves. ¿Qué cambias?

<!-- solution -->

Usa `reduceByKey(lambda a, b: a + b)`, que suma dentro de cada partición antes del shuffle, así se mueven muchos menos datos y no se guarda en memoria la lista completa de ninguna clave. Mejor aún, usa un `groupBy().sum()` de DataFrame.

<!-- takeaways -->

- Los RDDs dan control pero no tienen optimizador.
- Los RDDs en Python son mucho más lentos que los DataFrames.
- Combina antes del shuffle (`reduceByKey`).

<!-- unit: Variables compartidas -->

<!-- goals -->

- Usar broadcast variables para datos de búsqueda.
- Usar accumulators para contadores, conociendo sus salvedades.

<!-- concept -->

Las funciones enviadas a los executors llevan copias de todo lo que referencian, una vez por tarea. Un diccionario de búsqueda grande referenciado en una función se envía entonces miles de veces; una broadcast variable lo envía una vez por executor.
Los accumulators van en sentido contrario: las tareas les suman y el driver lee el total, útil para contar registros malos. Como las tareas fallidas o reintentadas pueden sumar dos veces, sirven para monitoreo, no para lógica de negocio.

<!-- example -->

```python
country_names = sc.broadcast({"CO": "Colombia", "PE": "Peru", "MX": "Mexico"})
bad = sc.accumulator(0)

def to_name(code):
    if code not in country_names.value:
        bad.add(1)
    return country_names.value.get(code, "unknown")
```

#### ¿Qué son la serialización y la deserialización, y por qué las necesita Spark?

La **serialización** convierte un objeto en una secuencia de bytes para enviarlo por la red o almacenarlo de forma compacta; la **deserialización** reconstruye el objeto a partir de esos bytes. Spark necesita ambas para enviar funciones y datos del driver a los executors, mover datos durante los shuffles y guardar datos en caché en forma serializada.

#### ¿Qué serializadores usa Spark?

Del lado de la JVM, Spark usa por defecto el **serializador de Java** para los RDD de objetos JVM, y se puede activar el **serializador Kryo**, más rápido y compacto (`spark.serializer=org.apache.spark.serializer.KryoSerializer`), opcionalmente con clases registradas. Los DataFrames no dependen de ninguno de los dos para sus datos: Tungsten guarda las filas en su propio formato binario. En PySpark, los objetos y funciones de Python se serializan con **pickle** (cloudpickle para las funciones), y **Apache Arrow** se usa para mover datos en columnas entre la JVM y pandas.

```python
from pyspark.sql import SparkSession

spark = (SparkSession.builder.appName("Kryo app")
         .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
         .getOrCreate())
```

<!-- challenge -->

Un equipo calcula un total de facturación con un accumulator dentro de un `map`, y el total a veces sale muy alto. ¿Por qué?

<!-- solution -->

Las actualizaciones de accumulators dentro de transformaciones pueden aplicarse más de una vez cuando se reintentan tareas o se recalculan stages. Calcula los totales de negocio con una agregación (`sum`) y usa los accumulators solo para diagnóstico.

<!-- takeaways -->

- Broadcast envía datos de solo lectura una vez por executor.
- Los accumulators juntan conteos en el driver.
- No confíes en accumulators dentro de transformaciones para resultados exactos.

<!-- unit: Serialización -->

<!-- goals -->

- Explicar por qué Spark serializa datos y qué serializadores usa.
- Diagnosticar errores "Task not serializable" y de pickling.

<!-- concept -->

Todo lo que cruza máquinas o procesos debe volverse bytes: tareas enviadas a los executors, datos que se mueven en shuffles, particiones en caché y objetos Python que pasan a la JVM. El serializador decide qué tan rápido y compacto es eso; Kryo es más rápido que el de Java por defecto para objetos JVM, y Python usa pickle.
Los errores aparecen cuando una función captura algo que no se puede serializar, como la SparkSession, una conexión a base de datos o un archivo abierto. La solución es crearlos dentro de la función o por partición.

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

#### ¿Puedes elegir el serializador de los RDD de Python?

Sí. El predeterminado es un serializador pickle por lotes; `MarshalSerializer` es más rápido, pero soporta menos tipos. Las clases propias deben poder serializarse con pickle e importarse en los executors (definidas en un módulo enviado con `--py-files`, no solo en una celda de notebook).

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

#### ¿Qué significa "Task not serializable" o un error de pickle?

Una función enviada a los executors hace referencia a algo que no puede serializarse, como una SparkSession, una conexión a una base de datos, un lock o un archivo abierto. Crea esos objetos dentro de la función (o por partición con `mapPartitions`/`foreachPartition`) en lugar de capturarlos desde el driver.

#### ¿Cuál es la diferencia entre coalesce y repartition en los RDD?

La misma que en los DataFrames: `repartition(n)` hace un shuffle completo y puede aumentar o disminuir las particiones; `coalesce(n)` une particiones existentes sin un shuffle completo y solo puede disminuirlas.

#### ¿Cómo conviertes entre RDD y DataFrames?

`df.rdd` devuelve un RDD de objetos `Row`; `spark.createDataFrame(rdd, schema)` o `rdd.toDF(["col1", "col2"])` construye un DataFrame. Convertir a RDD en Python serializa cada fila hacia Python, así que evítalo en las partes críticas.

<!-- challenge -->

Una función usada en `mapPartitions` referencia `spark.read`, y el job falla con un error de pickling. ¿Qué está mal?

<!-- solution -->

La SparkSession existe solo en el driver y no se puede serializar a los executors. Haz todas las lecturas en el driver; dentro de las funciones de los executors, trabaja solo con las filas (y con objetos creados ahí).

<!-- takeaways -->

- Tareas y datos se serializan para cruzar máquinas.
- Kryo para objetos JVM; pickle para Python.
- Crea conexiones y sesiones donde se usan.

<!-- stage: Trabajar con DataFrames -->

### DataFrames y esquemas

<!-- unit: DataFrames y esquemas -->

<!-- goals -->

- Explicar DataFrames, Rows y su relación con los Datasets.
- Crear DataFrames con esquemas explícitos en lugar de inferirlos.

<!-- concept -->

Un DataFrame es una tabla distribuida: filas con columnas con nombre y tipo, inmutable y evaluada de forma perezosa. Como Spark conoce el esquema, puede optimizar, guardar los datos de forma compacta y generar código eficiente, algo que los objetos Python comunes nunca permiten.
Los esquemas deben declararse, no adivinarse. La inferencia lee los datos una vez extra y adivina los tipos con muestras, lo que es lento y frágil: una columna de números hoy puede traer texto mañana.

<!-- example -->

```python
schema = "order_id BIGINT, customer_id BIGINT, amount DECIMAL(12,2), ordered_at TIMESTAMP"
orders = spark.read.schema(schema).option("header", True).csv("s3://landing/orders/")
small = spark.createDataFrame([(1, "Bogotá"), (2, "Lima")], "id INT, city STRING")
```

#### ¿Qué es un DataFrame?

Una colección distribuida de filas con columnas con nombre y tipo, como una tabla. Es inmutable: cada transformación devuelve un nuevo DataFrame. Como Spark conoce el esquema y las operaciones, Catalyst puede optimizar el código de DataFrames, a diferencia de las funciones opacas de los RDD.

#### ¿Cuál es la diferencia entre un DataFrame y un Dataset?

Un Dataset es una versión tipada del DataFrame disponible en Scala y Java. En esos lenguajes un DataFrame es `Dataset[Row]`. Python solo tiene DataFrames, porque no tiene tipado estático.

#### ¿Cómo creas un DataFrame?

A partir de una lista de tuplas u objetos `Row` con `spark.createDataFrame`, de un DataFrame de pandas, de un RDD, de un archivo o tabla con `spark.read`, o con SQL mediante `spark.sql`.

```python
from pyspark.sql import Row

df1 = spark.createDataFrame([(1, "Bogotá"), (2, "Medellín")], ["id", "city"])
df2 = spark.createDataFrame([Row(id=1, city="Cali")])
df3 = spark.range(0, 1000)          # una sola columna "id"
```

#### ¿Cómo defines un esquema explícito?

Con un `StructType` de `StructField`, o con una cadena DDL. Los esquemas explícitos son más rápidos que la inferencia y detectan pronto los cambios de formato.

```python
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

schema = StructType([
    StructField("user_id", IntegerType(), nullable=False),
    StructField("city", StringType()),
    StructField("amount", DoubleType()),
])
ddl_schema = "user_id INT, city STRING, amount DOUBLE"
```

#### ¿Por qué evitar inferSchema en producción?

La inferencia lee los datos (todos en CSV, o una muestra) una vez más, lo que es lento con archivos grandes. Además puede inferir tipos distintos según el día (una columna de ID leída como entero hasta que aparece un valor con una letra), así que los jobs fallan o cambian sin avisar. Declara el esquema.

#### ¿Cómo inspeccionas un DataFrame?

`printSchema()` para el árbol del esquema, `df.schema` y `df.dtypes` desde el código, `show(n, truncate=False)` para las filas, `df.columns` para los nombres, `describe()` o `summary()` para estadísticas básicas, y `explain()` para el plan de consulta.

<!-- challenge -->

Una carga nocturna de CSV con `inferSchema=True` falló después de que un proveedor mandó "N/A" en una columna numérica, volviéndola string. ¿Cómo lo evitas?

<!-- solution -->

Declara el esquema explícitamente con el tipo numérico, lee en modo permissive con una columna de registros corruptos y manda a cuarentena las filas que no se puedan parsear, en lugar de cambiar el tipo de la columna.

<!-- takeaways -->

- Los DataFrames son tablas tipadas, inmutables y perezosas.
- Los esquemas explícitos son más rápidos y seguros que la inferencia.
- La API de Python tiene DataFrames; los Datasets son para Scala/Java.

<!-- unit: Inspeccionar y traer datos al driver -->

<!-- goals -->

- Inspeccionar esquemas y muestras con seguridad.
- Elegir entre collect, take, show y toPandas, y usar la pandas API on Spark.

<!-- concept -->

Mirar los datos es donde muchos jobs se caen por accidente. Algunas llamadas solo inspeccionan metadatos; otras traen filas al driver, y traer todo de un DataFrame grande lo desborda. Revisar si está vacío contando escanea todos los datos cuando bastaba una fila.
Pasar a pandas está bien cuando los datos ya son pequeños, y Arrow lo hace rápido. La pandas API on Spark ofrece sintaxis de pandas sobre datos distribuidos para equipos que migran código.

<!-- example -->

```python
orders.printSchema()                      # metadata only
orders.show(5, truncate=False)            # 5 rows
if orders.isEmpty(): ...                  # stops after one row
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
summary_pdf = orders.groupBy("country").count().toPandas()   # small result → pandas
```

#### ¿Qué es un Row?

Un objeto que representa un registro, con campos accesibles por nombre (`row.city` o `row["city"]`) o por posición. `collect()` y `take()` devuelven listas de objetos `Row`; `row.asDict()` convierte uno en diccionario.

#### ¿Qué tipos complejos soporta Spark?

`ArrayType`, `MapType` y `StructType` (registros anidados), que pueden anidarse entre sí, además de `VARIANT` en Spark 4 para datos semiestructurados. Accede a los campos de un struct con notación de punto (`col("address.city")`), a los arrays con `col("tags")[0]` o `element_at`, y a los maps con `col("attrs")["key"]`.

#### ¿Cómo manejas JSON anidado?

Léelo con un esquema, selecciona los campos anidados con notación de punto, aplana los arrays con `explode` y convierte las cadenas JSON de una columna con `from_json`.

```python
from pyspark.sql import functions as F

orders = spark.read.schema(order_schema).json("path/to/orders")
flat = (orders
        .select("order_id", "customer.name", F.explode("items").alias("item"))
        .select("order_id", "name", "item.sku", "item.qty"))
```

#### ¿Cuál es la diferencia entre explode y explode_outer?

`explode` produce una fila por elemento del array y descarta las filas cuyo array es null o está vacío. `explode_outer` conserva esas filas con un elemento null. `posexplode` también devuelve la posición del elemento.

#### ¿Qué diferencia hay entre la inmutabilidad de los DataFrames y las variables de Python?

Los DataFrames nunca cambian; las transformaciones devuelven otros nuevos. Reasignar `df = df.filter(...)` solo hace que la variable apunte a un nuevo plan. Por eso llamar `df.withColumn(...)` sin asignar el resultado no hace nada.

#### ¿Cómo renombras columnas?

Con `withColumnRenamed(antiguo, nuevo)`, `withColumnsRenamed({antiguo: nuevo})` (Spark 3.4), `select(col(antiguo).alias(nuevo))` o `toDF(*nuevos_nombres)` para renombrarlas todas a la vez.

<!-- challenge -->

Un notebook llama `df.toPandas()` sobre una tabla de 300 GB para "mirar los datos" y el driver se cae. ¿Qué debería hacer?

<!-- solution -->

Inspeccionar con `printSchema()`, `show(20)`, `limit(1000).toPandas()` o `sample(0.001)`, o agregar primero y convertir solo el resultado pequeño.

<!-- takeaways -->

- Las llamadas de metadatos son baratas; traer filas no.
- Usa `isEmpty()` o `head(1)`, no `count()`.
- Convierte a pandas solo resultados pequeños, con Arrow.

<!-- unit: Dar forma a las columnas -->

<!-- goals -->

- Renombrar, agregar, reemplazar y quitar columnas con eficiencia.
- Entender la inmutabilidad de los DataFrames en el código Python.

<!-- concept -->

Los DataFrames nunca cambian; cada operación devuelve uno nuevo, y reasignar una variable solo la apunta al plan más nuevo. Eso hace seguro construir pipelines paso a paso.
Construir muchas columnas una llamada a la vez, sobre todo en bucles, hace crecer el plan con una proyección por llamada, lo que frena el análisis. Definir varias columnas a la vez mantiene los planes pequeños y el código más claro.

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

#### ¿Cómo agregas o reemplazas varias columnas de forma eficiente?

Usa un solo `select` o `withColumns({...})` (Spark 3.3) en lugar de llamar `withColumn` en un bucle. Cada `withColumn` agrega una proyección al plan, y cientos de ellas hacen muy lentos el análisis y la optimización.

```python
df = df.withColumns({
    "amount_cop": F.col("amount") * F.col("fx_rate"),
    "load_date": F.current_date(),
})
```

#### ¿Cómo eliminas columnas y filas duplicadas?

`drop("col1", "col2")` elimina columnas. `distinct()` elimina filas duplicadas en todas las columnas; `dropDuplicates(["id"])` conserva una fila por clave, pero no se define cuál sobrevive. Para conservar una en particular (por ejemplo la más reciente), usa una función de ventana.

#### ¿Cómo compruebas si un DataFrame está vacío?

Con `df.isEmpty()` (Spark 3.3) o `len(df.head(1)) == 0`. Evita `df.count() == 0`, que recorre todos los datos.

#### ¿Cuál es la diferencia entre collect, take, head, show y toPandas?

`collect()` trae todas las filas al driver; `take(n)` y `head(n)` traen las n primeras; `show(n)` las imprime; `toPandas()` trae todo a un DataFrame de pandas (usando Arrow si está activado). Todo, salvo `take`/`show` pequeños, puede dejar al driver sin memoria con datos grandes.

<!-- challenge -->

Un código agrega 150 columnas derivadas con `withColumn` en un bucle, y el job tarda dos minutos antes de que arranque cualquier tarea. ¿Qué cambias?

<!-- solution -->

Arma las expresiones de columna en una lista o diccionario y agrégalas en una sola llamada `select` o `withColumns`, para que el plan tenga una proyección en lugar de 150 anidadas.

<!-- takeaways -->

- Cada operación devuelve un DataFrame nuevo.
- Agrega muchas columnas en un `select` o `withColumns`.
- `dropDuplicates` sobre claves; `distinct` sobre todas las columnas.

<!-- unit: Datos anidados -->

<!-- goals -->

- Trabajar con arrays, maps y structs.
- Aplanar JSON anidado con explode y explode_outer.

<!-- concept -->

Los datos reales suelen venir anidados: órdenes con arrays de ítems, clientes con structs de dirección, atributos como maps. Spark los maneja como columnas tipadas, así que puedes seleccionar campos anidados con notación de punto y mantener los datos anidados mientras convenga.
Aplanar convierte cada elemento de un array en una fila. El detalle que importa es qué pasa con los arrays vacíos o faltantes: una variante bota esas filas y la otra las conserva con nulos, lo que cambia los conteos.

<!-- example -->

```python
items = (orders
  .select("order_id", "customer.city", F.explode_outer("items").alias("item"))
  .select("order_id", "city", "item.sku", "item.qty", "item.price"))
```

#### ¿Cómo conviertes entre Spark y pandas?

Con `spark.createDataFrame(pandas_df)` y `df.toPandas()`. Activa Arrow (`spark.sql.execution.arrow.pyspark.enabled=true`, el valor por defecto en los runtimes recientes de Databricks) para que ambas conversiones sean mucho más rápidas. Convierte solo datos que quepan en la memoria del driver.

#### ¿Qué es la API de pandas en Spark?

`pyspark.pandas`, una API compatible con pandas que se ejecuta en Spark (antes Koalas). Ayuda a migrar código pandas a datos grandes, aunque algunas operaciones se comportan distinto (el manejo del índice, el orden) y pueden ser más lentas que PySpark nativo.

#### ¿Cómo tomas muestras de los datos?

`df.sample(fraction=0.1, seed=42)` para una muestra aleatoria (de tamaño aproximado), `df.limit(n)` para las primeras filas (no aleatorias) y `df.randomSplit([0.8, 0.2], seed=42)` para dividir en entrenamiento y prueba.

#### ¿De qué formas puedes referenciar una columna?

`F.col("name")`, `df["name"]`, `df.name` y, en muchas funciones, la cadena `"name"`. `df.name` falla con nombres que coinciden con métodos del DataFrame o que contienen espacios; `F.col` es la más consistente. Usa comillas invertidas para nombres con puntos o espacios: ``F.col("`order.id`")``.

<!-- challenge -->

Tras aplanar las órdenes con `explode`, la cantidad de órdenes distintas bajó un 3 %. ¿Qué pasó?

<!-- solution -->

`explode` botó las órdenes con arrays `items` vacíos o nulos. Usa `explode_outer` para conservarlas (con campos de ítem nulos), o cuenta las órdenes antes de explotar.

<!-- takeaways -->

- Arrays, maps y structs son tipos de primera clase.
- Selecciona campos anidados con notación de punto.
- `explode` bota arrays vacíos; `explode_outer` los conserva.

### Columnas y funciones integradas

<!-- unit: Columnas y condiciones -->

<!-- goals -->

- Referenciar columnas y filtrar filas correctamente.
- Escribir lógica condicional con when, lit y expr.

<!-- concept -->

La mayor parte de la lógica en PySpark se construye con expresiones de columna: referencias, constantes, operadores y funciones combinados en un plan que corre en la JVM. Importar las funciones como `F` evita llamar por accidente a `sum` o `max` de Python sobre columnas.
Las condiciones se combinan con `&`, `|` y `~`, cada una entre paréntesis porque la precedencia de operadores de Python difiere de la de SQL. Los valores condicionales usan cadenas de `when`; los fragmentos SQL caben con `expr` cuando se leen mejor.

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

#### ¿Por qué importar las funciones como F?

`from pyspark.sql import functions as F` evita ocultar funciones integradas de Python como `sum`, `min`, `max`, `round` y `filter`. Importar `sum` directamente de `pyspark.sql.functions` reemplaza sin avisar el `sum` de Python, una fuente clásica de errores confusos.

#### ¿Cómo filtras filas?

Con `filter` o su alias `where`, usando expresiones de columna o una cadena SQL. Combina condiciones con `&`, `|` y `~`, poniendo cada condición entre paréntesis.

```python
df.filter((F.col("amount") > 8000) & (F.col("city") == "Bogotá"))
df.where("amount > 8000 AND city = 'Bogotá'")
df.filter(~F.col("city").isin("Cali", "Pasto"))
```

#### ¿Cómo escribes lógica condicional?

Con `F.when(...).when(...).otherwise(...)`, el equivalente de `CASE WHEN` en SQL. Sin `otherwise`, las filas que no cumplen ninguna condición quedan en null.

```python
df = df.withColumn(
    "size",
    F.when(F.col("amount") >= 10000, "large")
     .when(F.col("amount") >= 5000, "medium")
     .otherwise("small"),
)
```

#### ¿Cómo maneja Spark los null en las comparaciones?

Las comparaciones con null devuelven null, que `filter` trata como falso. `col == None` no funciona; usa `isNull()`/`isNotNull()`. Para una igualdad que trate null como igual a null, usa `eqNullSafe` o el operador SQL `<=>`.

#### ¿Cómo reemplazas o rellenas los null?

Con `df.na.fill({"city": "unknown", "amount": 0})` o `fillna`, `F.coalesce(col1, col2, F.lit(valor_por_defecto))` para el primer valor no nulo, y `df.na.drop(subset=["id"])` para eliminar filas con nulls en ciertas columnas.

#### ¿Qué hace lit()?

Convierte una constante de Python en una expresión de columna, por ejemplo `F.lit(0)` o `F.lit("COP")`. Muchas funciones aceptan valores simples, pero `lit` hace falta cuando se espera una columna, como en `withColumn("currency", F.lit("COP"))`.

<!-- challenge -->

`df.filter(F.col("a") > 1 & F.col("b") < 5)` lanza un error. ¿Por qué y cuál es la solución?

<!-- solution -->

En Python, `&` liga más fuerte que `>` y `<`, así que intenta `1 & F.col("b")`. Envuelve cada condición: `df.filter((F.col("a") > 1) & (F.col("b") < 5))`.

<!-- takeaways -->

- Construye la lógica con expresiones de columna.
- Importa las funciones como `F`.
- Pon entre paréntesis cada condición combinada con `&` o `|`.

<!-- unit: Nulos, tipos y modo ANSI -->

<!-- goals -->

- Manejar nulos en comparaciones y rellenarlos.
- Hacer casts seguros y entender el modo ANSI.

<!-- concept -->

Nulos y casts son donde se esconden los errores silenciosos. Las comparaciones con null no son ni verdaderas ni falsas, así que los filtros botan esas filas salvo que revises null explícitamente. Rellenar nulos es una decisión de negocio, no un paso de limpieza.
El cast solía convertir valores inválidos en null sin avisar. El modo ANSI, por defecto en Spark 4, lanza errores en su lugar, lo que es más seguro pero obliga a manejar a propósito los datos sucios con casts del tipo try.

<!-- example -->

```python
df = df.withColumn("amount", F.expr("try_cast(amount_raw AS DECIMAL(12,2))"))  # null on bad input
missing = df.filter(F.col("discount").isNull())
df = df.fillna({"discount": 0, "city": "unknown"})
df = df.withColumn("total", F.round(F.col("amount") * (1 - F.col("discount")), 2))
```

#### ¿Cómo conviertes tipos?

Con `F.col("amount").cast("double")` o `.cast(DoubleType())`. Sin modo ANSI, un cast inválido devuelve null; con modo ANSI (el predeterminado en Spark 4) lanza un error. `try_cast` (Spark 4, y `TRY_CAST` en SQL) devuelve null explícitamente para valores inválidos.

#### ¿Qué es el modo ANSI y por qué importa?

`spark.sql.ansi.enabled` hace que Spark siga el SQL estándar: el desbordamiento, la división por cero y los casts inválidos lanzan errores en lugar de devolver null. Está activado por defecto en Spark 4.0. Detecta pronto los datos incorrectos, pero el código escrito para el comportamiento anterior puede fallar, así que prueba con la misma configuración que producción.

#### ¿Cuáles son las funciones de texto más útiles?

`lower`, `upper`, `trim`, `lpad`/`rpad`, `substring`, `concat`/`concat_ws`, `split`, `regexp_extract`, `regexp_replace`, `like`/`rlike`, `length`, `initcap` y `format_string`.

```python
df = df.withColumn("postcode", F.regexp_replace(F.trim("postcode"), r"[^0-9]", ""))
df = df.withColumn("full_name", F.concat_ws(" ", "first_name", "last_name"))
```

#### ¿Cómo conviertes y formateas fechas?

Con `to_date(col, "dd/MM/yyyy")`, `to_timestamp`, `date_format(col, "yyyy-MM")`, `date_trunc("month", ts)`, `datediff`, `months_between`, `add_months`, `date_add`, `year`/`month`/`dayofweek`, `current_date` y `current_timestamp`. Los patrones siguen el `DateTimeFormatter` de Java (`yyyy`, `MM`, `dd`, `HH`, `mm`).

#### ¿Cómo maneja Spark las zonas horarias?

Los timestamps se guardan como instantes UTC y se muestran en la zona horaria de la sesión (`spark.sql.session.timeZone`). Defínela explícitamente (por ejemplo `UTC`) para que los resultados no dependan de la configuración por defecto del clúster. Spark 3.4 agregó `TIMESTAMP_NTZ` para timestamps sin zona horaria.

<!-- challenge -->

Tras actualizar a Spark 4, un job falla con un error de cast en una columna que "antes funcionaba bien". ¿Qué cambió y cómo lo arreglas bien?

<!-- solution -->

Ahora el modo ANSI está activo, así que los casts inválidos lanzan errores en vez de devolver null en silencio. Usa `try_cast` en las columnas que pueden traer valores malos, y pon en cuarentena o registra esas filas en lugar de desactivar el modo ANSI.

<!-- takeaways -->

- Las comparaciones con null son desconocidas; prueba con `isNull`.
- Rellenar nulos es una decisión de negocio.
- El modo ANSI falla con casts malos; usa `try_cast`.

<!-- unit: Strings, fechas y zonas horarias -->

<!-- goals -->

- Limpiar strings con funciones incorporadas.
- Parsear, formatear y truncar fechas, y manejar zonas horarias.

<!-- concept -->

El texto y el tiempo causan la mayor parte del trabajo de limpieza, y las funciones incorporadas cubren casi todo: recortar, mayúsculas, relleno, dividir y expresiones regulares para texto; parsear con patrones explícitos, formatear y truncar para fechas.
Las zonas horarias necesitan una regla firme: los timestamps son instantes guardados en UTC y mostrados en la zona horaria de la sesión. Fijar esa zona explícitamente en los jobs hace que los resultados sean iguales en cualquier clúster.

<!-- example -->

```python
spark.conf.set("spark.sql.session.timeZone", "UTC")
clean = (raw
  .withColumn("email", F.lower(F.trim("email")))
  .withColumn("phone", F.regexp_replace("phone", r"[^0-9+]", ""))
  .withColumn("order_date", F.to_date("order_date_raw", "dd/MM/yyyy"))
  .withColumn("month", F.date_trunc("month", "ordered_at")))
```

#### ¿Cómo trabajas con arrays?

Con `array`, `array_contains`, `size`, `element_at`, `array_distinct`, `array_union`, `array_join`, `sort_array`, `explode`, `collect_list` y las funciones de orden superior: `transform`, `filter`, `exists`, `aggregate`.

```python
df.withColumn("prices_with_tax", F.transform("prices", lambda p: p * 1.19))
df.withColumn("big_items", F.filter("items", lambda i: i["qty"] > 10))
```

#### ¿Cómo trabajas con cadenas JSON en una columna?

`from_json(col, schema)` las convierte en un struct o un map, `to_json` las vuelve a serializar, `get_json_object(col, "$.a.b")` extrae un valor por ruta, y `schema_of_json` infiere un esquema a partir de una cadena de ejemplo.

#### ¿Qué es monotonically_increasing_id()?

Una función que genera ID únicos de 64 bits por fila. Son crecientes dentro de una partición, pero no consecutivos (el número de partición va en los bits altos). Para números consecutivos usa `row_number()` sobre una ventana, que necesita un ordenamiento.

<!-- challenge -->

El mismo job produce totales diarios corridos un día en dos clústeres. ¿Cuál es la causa probable?

<!-- solution -->

Zonas horarias de sesión distintas: `to_date` sobre timestamps usa `spark.sql.session.timeZone`, que por defecto es la zona del clúster. Fíjala explícitamente en el job (por ejemplo UTC o la zona del negocio).

<!-- takeaways -->

- Las funciones incorporadas cubren casi toda la limpieza de strings.
- Parsea fechas con patrones explícitos.
- Fija explícitamente la zona horaria de la sesión.

<!-- unit: Arrays, JSON, IDs y pivots -->

<!-- goals -->

- Trabajar con columnas de arrays y JSON.
- Generar IDs y llaves hash, y pivotear o despivotear datos.

<!-- concept -->

Algunas columnas llevan estructura adentro: arrays de valores, strings JSON de APIs. Spark tiene funciones para consultar y transformar ambos sin explotar filas ni escribir Python.
Llaves y cambios de forma completan el panorama. Los IDs generados son únicos pero no consecutivos ni estables entre ejecuciones, así que los hashes deterministas de columnas de negocio son mejores llaves sustitutas. Pivotear convierte valores en columnas, mejor si das la lista de valores de antemano.

<!-- example -->

```python
events = events.withColumn("payload", F.from_json("payload_raw", "user_id STRING, tags ARRAY<STRING>"))
tagged = events.where(F.array_contains("payload.tags", "promo"))
keyed = orders.withColumn("order_key", F.xxhash64("source", "order_id"))
wide = sales.groupBy("store").pivot("month", ["2026-08", "2026-09", "2026-10"]).sum("revenue")
```

#### ¿Cómo generas un hash o una clave sustituta?

Con `F.sha2(F.concat_ws("||", *cols), 256)`, `md5` o `xxhash64`. Las claves hash son deterministas, así que la misma clave de negocio siempre recibe la misma clave sustituta, lo que es útil para cargas incrementales y para comparar registros y detectar cambios.

#### ¿Cómo haces pivot y unpivot?

`groupBy("store").pivot("month").sum("revenue")` convierte los valores de mes en columnas; pasar la lista de valores (`pivot("month", ["01", "02"])`) evita una pasada adicional para encontrarlos. `unpivot` (también llamado `melt`, Spark 3.4) vuelve a convertir las columnas en filas.

#### ¿Qué hace expr()?

Convierte una expresión SQL en una columna: `F.expr("amount * fx_rate")` o `df.selectExpr("id", "upper(city) AS city")`. Es útil para funciones que solo existen en SQL y para transformaciones definidas por configuración.

#### ¿Cómo redondeas y formateas números?

Con `round(col, 2)` (redondeo hacia arriba en .5), `bround` (redondeo bancario), `format_number(col, 2)` para mostrar, y `DecimalType(p, s)` para montos de dinero exactos, porque `double` es un tipo de coma flotante.

#### ¿Cómo agregas un DataFrame?

Con `groupBy(...).agg(...)` y funciones de agregación, nombrando cada resultado con `alias`.

```python
summary = (df.groupBy("city")
             .agg(F.count("*").alias("orders"),
                  F.sum("amount").alias("revenue"),
                  F.avg("amount").alias("avg_amount"),
                  F.countDistinct("user_id").alias("customers")))
```

<!-- challenge -->

Un equipo usa `monotonically_increasing_id()` como llave de cliente, y las llaves cambian entre ejecuciones, rompiendo los joins con los datos de ayer. ¿Qué usas en su lugar?

<!-- solution -->

Un hash determinista de la llave de negocio (por ejemplo `sha2(concat_ws('||', source, customer_number), 256)` o `xxhash64`), que da la misma llave en cada ejecución para el mismo cliente.

<!-- takeaways -->

- Las funciones de arrays y JSON evitan código Python.
- Los IDs generados no son estables; haz hash de las llaves de negocio.
- Pivotea con una lista explícita de valores.

### Agregaciones y agrupamiento

<!-- unit: Agrupar y agregar -->

<!-- goals -->

- Agregar con groupBy y agg, y filtrar los resultados agregados.
- Elegir bien las funciones de conteo y collect, evitando first/last poco confiables.

<!-- concept -->

La agregación sigue un patrón: agrupar por claves, calcular agregados con nombre y luego filtrar u ordenar el resultado. Filtrar después de agregar es la forma de expresar en PySpark el `HAVING` de SQL.
Los detalles deciden la corrección. Contar filas, valores no nulos y valores distintos da resultados distintos; recolectar valores conserva o bota duplicados; y los valores "first" o "last" dependen del particionamiento salvo que ordenes explícitamente, por eso las ventanas o las funciones tipo max-by son más seguras.

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

#### ¿Cuál es la diferencia entre count("*"), count(col) y countDistinct?

`count("*")` cuenta filas; `count(col)` cuenta los valores no nulos de una columna; `countDistinct(col)` cuenta los valores distintos no nulos y necesita un shuffle por valor. Con datos grandes, `approx_count_distinct(col, rsd=0.02)` usa HyperLogLog y es mucho más barato.

#### ¿Cuál es la diferencia entre collect_list y collect_set?

Ambas reúnen valores en un array por grupo: `collect_list` conserva los duplicados, `collect_set` los elimina. Ninguna garantiza el orden. Para obtener una lista ordenada, reúne structs y ordena el array, o usa una función de ventana.

#### ¿Por qué first() y last() no son confiables en las agregaciones?

Sin un orden explícito, la fila que queda "primera" depende de cómo se particionaron y se movieron los datos, así que los resultados pueden cambiar entre ejecuciones. Usa `max_by`/`min_by` (Spark 3.3), por ejemplo `F.max_by("status", "updated_at")`, o una ventana con `row_number()`.

#### ¿Cómo filtras sobre un agregado (HAVING en SQL)?

Agrega primero y después filtra el resultado.

```python
(df.groupBy("city")
   .agg(F.avg("amount").alias("avg_amount"))
   .filter(F.col("avg_amount") > 8000))
```

#### ¿Qué hacen rollup y cube?

`rollup("country", "city")` agrega subtotales para cada nivel de la jerarquía más un total general; `cube` agrega subtotales para cada combinación de columnas. `grouping()` y `grouping_id()` distinguen los nulls reales de las filas de subtotal.

#### ¿Cómo calculas percentiles y medianas?

`percentile_approx(col, 0.5)` (también `approx_percentile`) es rápido y funciona con datos grandes; `percentile` y `median` (Spark 3.4) son exactos, pero más costosos.

<!-- challenge -->

Un reporte usa `F.first("status")` para obtener el último estado de cada orden, y los resultados cambian entre ejecuciones. ¿Qué usas en su lugar?

<!-- solution -->

Elige el último explícitamente: `max_by("status", "updated_at")` en la agregación, o una ventana con `row_number()` ordenada por `updated_at` descendente conservando la fila 1.

<!-- takeaways -->

- `groupBy().agg()` con alias; filtra después para el HAVING.
- Cada variante de conteo responde una pregunta distinta.
- `first`/`last` necesitan orden explícito para ser confiables.

<!-- unit: Agregación avanzada -->

<!-- goals -->

- Producir subtotales con rollup y cube, y calcular percentiles.
- Explicar la agregación en dos fases y conservar las filas de detalle con conteos de grupo.

<!-- concept -->

Spark agrega en dos fases: cada partición calcula resultados parciales y luego un shuffle junta los parciales de una misma clave para el resultado final. Eso hace baratos sumas y conteos, pero caros las medianas exactas y los conteos distintos, y por eso existen versiones aproximadas.
Más allá de los agrupamientos simples, rollups y cubes agregan subtotales en una pasada, y los agregados de ventana añaden valores de grupo a cada fila sin colapsarlas.

<!-- example -->

```python
with_share = sales.withColumn(
    "city_revenue", F.sum("amount").over(Window.partitionBy("city"))
).withColumn("share", F.col("amount") / F.col("city_revenue"))
p50 = sales.groupBy("city").agg(F.percentile_approx("amount", 0.5).alias("median_amount"))
totals = sales.rollup("country", "city").agg(F.sum("amount").alias("revenue"))
```

#### ¿Cómo ejecuta Spark físicamente una agregación?

Normalmente en dos fases: una agregación parcial en cada partición (como una combinación del lado map), un shuffle por la clave de agrupamiento y después una agregación final. Por eso las agregaciones mueven muchos menos datos que las filas originales, salvo que casi todas las claves sean únicas.

#### ¿Cómo cuentas filas por grupo conservando las columnas originales?

Con una función de ventana: `F.count("*").over(Window.partitionBy("city"))` agrega el conteo a cada fila sin reducir el DataFrame como hace `groupBy`.

#### ¿Qué tipos de join soporta Spark?

`inner`, `left` (`left_outer`), `right`, `full` (`outer`), `left_semi` (filas de la izquierda que tienen coincidencia, solo con las columnas de la izquierda), `left_anti` (filas de la izquierda sin coincidencia) y `cross`.

```python
orders.join(customers, on="customer_id", how="left")
orders.join(blocked, on="customer_id", how="left_anti")    # pedidos de clientes no bloqueados
```

#### ¿Cómo evitas nombres de columna duplicados después de un join?

Haz el join por nombre de columna o lista de nombres (`on="user_id"`), lo que conserva una sola columna clave. Con una expresión (`df1.user_id == df2.user_id`) sobreviven ambas columnas, y seleccionar `user_id` después falla por ambigüedad. Ponles alias a los DataFrames o elimina la columna de uno de los lados.

<!-- challenge -->

Necesitas la participación de cada orden en los ingresos de su ciudad. Un colega agrega por ciudad y vuelve a cruzar. ¿Cuál es una forma más simple?

<!-- solution -->

Un agregado de ventana: `F.sum("amount").over(Window.partitionBy("city"))` agregado a cada fila, y luego divides. Una pasada, sin join.

<!-- takeaways -->

- Las agregaciones corren parciales y luego finales tras un shuffle.
- Usa percentiles aproximados con datos grandes.
- Los agregados de ventana conservan filas y agregan valores de grupo.

### Joins

<!-- unit: Tipos de join y claves -->

<!-- goals -->

- Usar bien joins inner, outer, semi y anti.
- Manejar columnas duplicadas, claves nulas y joins por rango.

<!-- concept -->

El tipo de join decide qué filas sobreviven. Inner conserva las coincidencias, los outer conservan las filas sin pareja de uno o ambos lados, los semi filtran por existencia sin agregar columnas y los anti conservan las filas sin coincidencia, la forma natural de encontrar lo que falta o lo que cambió.
Las claves necesitan cuidado: cruzar por nombres de columna evita columnas de clave duplicadas, las claves nulas nunca coinciden y las condiciones de rango sin clave de igualdad fuerzan joins nested-loop costosos.

<!-- example -->

```python
new_or_changed = (this_month.alias("n")
  .join(last_month.alias("o"), on="registry_id", how="left")
  .where(F.col("o.registry_id").isNull() | (F.col("n.row_hash") != F.col("o.row_hash"))))
removed = last_month.join(this_month, on="registry_id", how="left_anti")
```

#### ¿Qué estrategias de join puede elegir Spark?

- **Broadcast hash join:** el lado pequeño se copia a cada executor; no hay shuffle del lado grande.
- **Shuffle hash join:** ambos lados pasan por un shuffle por clave y el más pequeño se convierte en tabla hash en cada partición.
- **Sort-merge join:** ambos lados pasan por un shuffle, se ordenan por clave y se combinan. Es la opción por defecto para tablas grandes.
- **Broadcast nested loop join y producto cartesiano:** para joins sin igualdad y joins cruzados. Son costosos.

#### ¿Qué es un broadcast join y cuándo lo usas?

Cuando un lado es lo bastante pequeño para caber en la memoria de un executor (una dimensión o tabla de búsqueda), Spark envía una copia a cada executor y el lado grande se une en su lugar, sin shuffle. Spark lo hace automáticamente por debajo de `spark.sql.autoBroadcastJoinThreshold` (10 MB por defecto), y AQE puede cambiar a esta estrategia en tiempo de ejecución. Puedes forzarlo con una pista.

```python
from pyspark.sql.functions import broadcast

large_df = spark.createDataFrame([("A", 1000), ("B", 2000), ("C", 3000), ("D", 4000)], ["key", "amount"])
small_df = spark.createDataFrame([("A", "Apple"), ("B", "Banana"), ("C", "Cherry")], ["key", "fruit"])

large_df.join(broadcast(small_df), "key", "inner").show()
```

#### ¿Cuáles son los riesgos del broadcast?

Si la tabla "pequeña" en realidad es grande, el broadcast puede dejar sin memoria al driver o a los executors, porque la tabla se reúne en el driver y se copia a cada executor. También puede haber timeouts de broadcast (`spark.sql.broadcastTimeout`). Haz broadcast solo de tablas que sabes que seguirán siendo pequeñas.

#### ¿Qué es un join sesgado (skewed join) y cuáles son sus síntomas?

Un join en el que unos pocos valores de la clave concentran una gran parte de las filas, así que las tareas que procesan esas claves reciben muchos más datos que el resto. Síntomas: un stage en el que la mayoría de las tareas termina en segundos y unas pocas tardan minutos u horas, mucho spill en esas tareas y errores de memoria. El resumen de tareas de la Spark UI (duración máxima muy superior a la mediana) lo muestra.

#### ¿Cómo mitigas el sesgo?

- Deja que AQE divida las particiones sesgadas (`spark.sql.adaptive.skewJoin.enabled`, activado por defecto).
- Haz broadcast del otro lado si es pequeño.
- Filtra o trata por separado las claves calientes, a menudo nulls o valores por defecto como `-1` o `"unknown"`.
- Aplica **salting** a la clave: agrega un sufijo aleatorio en el lado grande y replica el lado pequeño para cada sufijo.

```python
from pyspark.sql import functions as F

num_salts = 8
large_salted = large_df.withColumn("salt", (F.rand() * num_salts).cast("int"))
small_salted = small_df.crossJoin(spark.range(num_salts).withColumnRenamed("id", "salt"))
joined = large_salted.join(small_salted, ["key", "salt"]).drop("salt")
```

#### ¿Por qué las claves null causan problemas en los joins?

Null nunca es igual a null en una condición de join, así que las claves null no coinciden con nada, pero todas van a la misma partición durante el shuffle y crean sesgo. Fíltralas antes del join (y vuelve a unirlas con un union si las necesitas en un left join) o reemplázalas por la clave de un miembro "desconocido".

#### ¿Cómo haces un join sin igualdad o por rango?

Con una condición como `events.ts.between(periods.start, periods.end)`. Sin una condición de igualdad, Spark usa un broadcast nested loop join o un producto cartesiano, que es lento con datos grandes. Agrega una condición de igualdad cuando sea posible (por ejemplo sobre un día) o haz broadcast del lado pequeño.

<!-- challenge -->

Necesitas los clientes que hicieron una orden, pero el inner join con órdenes devuelve clientes varias veces. ¿Qué join encaja?

<!-- solution -->

Un join `left_semi` de clientes con órdenes por `customer_id`: conserva cada cliente que coincide una sola vez y no agrega columnas de órdenes.

<!-- takeaways -->

- Los joins semi y anti prueban existencia.
- Cruza por nombres para evitar columnas de clave duplicadas.
- Las claves nulas nunca coinciden; los joins por rango piden cuidado.

<!-- unit: Estrategias de join -->

<!-- goals -->

- Explicar los joins broadcast, shuffle hash y sort-merge.
- Usar broadcasts, hints y bucketing con seguridad.

<!-- concept -->

Cómo ejecuta Spark un join importa más que qué join escribes. Si un lado es pequeño, Spark lo difunde a cada executor y el lado grande nunca se mueve. Si no, ambos lados se reparten por clave en un shuffle y luego se cruzan ordenando o con hash.
Puedes orientar la elección con hints y umbrales, pero difundir algo que no es realmente pequeño puede tumbar el driver o los executors. El bucketing reparte las tablas en disco de antemano, así los joins repetidos por la misma clave se saltan el shuffle.

<!-- example -->

```python
enriched = (orders
  .join(F.broadcast(countries), "country_code")     # small dimension: no shuffle of orders
  .join(customers, "customer_id"))                  # large: sort-merge join
enriched.explain()   # look for BroadcastHashJoin vs SortMergeJoin
```

#### ¿Qué hacen las pistas (hints) de join?

Le indican al optimizador qué estrategia usar: `broadcast`, `merge` (sort-merge), `shuffle_hash` y `shuffle_replicate_nl`, mediante `df.hint("merge")` o `/*+ BROADCAST(t) */` en SQL. Úsalas cuando faltan estadísticas o son incorrectas, y revísalas después de actualizar Spark.

#### ¿Qué es un semi join y cuándo es mejor que un inner join?

Un join `left_semi` devuelve las filas de la izquierda que tienen al menos una coincidencia, sin agregar columnas de la derecha ni duplicar filas cuando hay varias coincidencias. Es la versión DataFrame de `WHERE EXISTS` y es más eficiente que un inner join seguido de `distinct`.

#### ¿Qué es el bucketing?

Escribir una tabla dividida de antemano en un número fijo de buckets por una clave (`bucketBy(64, "customer_id").saveAsTable(...)`). Los joins y agregaciones entre tablas con el mismo bucketing sobre la clave pueden omitir el shuffle. Solo funciona con tablas guardadas en el metastore, y en las tablas Delta el liquid clustering lo ha reemplazado en gran medida.

#### ¿Cómo unes muchos DataFrames pequeños de forma eficiente?

Haz broadcast de ellos, únelos en orden del más al menos selectivo y asegúrate de que los filtros se apliquen antes de los joins. Si unes la misma tabla grande una y otra vez en un bucle, reestructura la lógica en un solo join o un union.

#### ¿Qué es una función de ventana?

Una función que calcula un valor para cada fila a partir de un grupo de filas relacionadas (la ventana) sin reducirlas, a diferencia de `groupBy`. Una ventana se define con `Window.partitionBy(...)`, normalmente `orderBy(...)` y, opcionalmente, un marco.

#### ¿Cuál es la diferencia entre row_number, rank y dense_rank?

Para valores empatados en el orden: `row_number` da números únicos y consecutivos (los empates se resuelven de forma arbitraria), `rank` da el mismo número a los empates y deja huecos (1, 1, 3), y `dense_rank` da el mismo número a los empates sin huecos (1, 1, 2).

<!-- challenge -->

Un join con una tabla de búsqueda de 30 MB hace shuffle de una tabla de hechos de 2 TB. No hay estadísticas. ¿Qué haces?

<!-- solution -->

Agrega un hint `broadcast()` a la tabla de búsqueda (o sube `spark.sql.autoBroadcastJoinThreshold` por encima de su tamaño), así la tabla de hechos se cruza en sitio sin shuffle.

<!-- takeaways -->

- Difunde los lados pequeños; haz shuffle de los grandes.
- Los hints orientan la estrategia; revisa con `explain()`.
- El bucketing prerreparte las tablas que se cruzan seguido.

<!-- unit: Joins con sesgo -->

<!-- goals -->

- Reconocer joins sesgados en la Spark UI.
- Mitigar el sesgo con AQE, broadcasts, salting y manejo aparte.

<!-- concept -->

El sesgo ocurre cuando unas pocas claves concentran gran parte de las filas. Las tareas de esas claves corren mucho más que las demás, a menudo derramando a disco o quedándose sin memoria, mientras el clúster espera. En la Spark UI se ve como una o pocas tareas con una entrada enorme junto a muchas pequeñas.
La ejecución adaptativa divide automáticamente las particiones sesgadas en muchos casos. Cuando no, difundir el otro lado, agregar sal a las claves calientes o procesarlas aparte lo resuelve.

<!-- example -->

```python
SALT = 16
hot = orders.withColumn("salt", (F.rand() * SALT).cast("int"))
dim = customers.crossJoin(spark.range(SALT).withColumnRenamed("id", "salt"))
joined = hot.join(dim, ["customer_id", "salt"]).drop("salt")
```

#### ¿Cómo conservas el registro más reciente por clave?

Numera las filas dentro de cada clave por timestamp descendente y conserva la primera. Agrega una columna de desempate al orden para que el resultado sea determinista.

```python
from pyspark.sql import Window, functions as F

w = Window.partitionBy("customer_id").orderBy(F.col("updated_at").desc(), F.col("event_id").desc())
latest = (df.withColumn("rn", F.row_number().over(w))
            .filter("rn = 1")
            .drop("rn"))
```

#### ¿Cómo obtienes los N primeros por grupo?

Con el mismo patrón y `rn <= N`. Usa `dense_rank` en lugar de `row_number` si deben incluirse todos los empates en el límite.

<!-- challenge -->

La última tarea de un join corre 40 minutos; su clave es `customer_id = 0`, usada para compras de invitados. ¿Cuál es la solución más simple?

<!-- solution -->

Maneja las filas de invitados aparte: saca `customer_id = 0` del join (no tienen datos de cliente), procésalas por su cuenta y une los resultados con `unionByName`. El join restante queda balanceado.

<!-- takeaways -->

- Sesgo: unas pocas tareas enormes entre muchas pequeñas.
- AQE divide automáticamente muchas particiones sesgadas.
- Agrega sal o separa las claves calientes cuando haga falta.

### Funciones de ventana

<!-- unit: Ventanas de ranking -->

<!-- goals -->

- Rankear filas con row_number, rank y dense_rank.
- Conservar el último registro por clave y el top N por grupo.

<!-- concept -->

Las funciones de ventana calculan sobre un grupo de filas relacionadas conservando cada fila, lo que las vuelve la herramienta estándar para preguntas "por clave". Particiona por la clave, ordena por lo que decide la precedencia, numera las filas y filtra.
La función de ranking decide los empates: los números de fila son únicos, los ranks se repiten en los empates. Agregar una columna de desempate hace determinista el "último registro" cuando los timestamps pueden ser iguales.

<!-- example -->

```python
w = Window.partitionBy("customer_id").orderBy(F.desc("updated_at"), F.desc("ingested_at"))
latest = (customers_raw
  .withColumn("rn", F.row_number().over(w))
  .where("rn = 1").drop("rn"))
```

#### ¿Qué hacen lag y lead?

Devuelven el valor de una fila anterior (`lag`) o siguiente (`lead`) según el orden de la ventana, con un desplazamiento y un valor por defecto opcionales. Se usan para diferencias entre filas consecutivas, para detectar cambios y para construir rangos de validez.

#### ¿Cómo calculas un total acumulado y la diferencia día a día?

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

La primera fila de cada tienda tiene una diferencia null, porque no hay fila anterior.

#### ¿Qué es el marco de una ventana?

El conjunto de filas, relativo a la actual, que usa un agregado: `rowsBetween(inicio, fin)` cuenta filas físicas y `rangeBetween(inicio, fin)` usa los valores de la columna de orden. Usa `Window.unboundedPreceding`, `Window.currentRow` y `Window.unboundedFollowing` como límites.

#### ¿Cuál es el marco por defecto y por qué sorprende?

Con `orderBy`, el marco por defecto es `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. Si hay empates en la columna de orden, se incluyen todas las filas empatadas, así que una suma "acumulada" puede dar saltos. Y `last()` sobre el marco por defecto devuelve la fila actual, no la última de la partición. Sin `orderBy`, el marco es la partición completa.

#### ¿Cómo calculas un promedio móvil de 7 días?

Ordena por una versión numérica de la fecha y usa un marco por rango, para que los días faltantes se manejen correctamente.

```python
w = (Window.partitionBy("store")
           .orderBy(F.col("date").cast("timestamp").cast("long"))
           .rangeBetween(-6 * 86400, 0))
df.withColumn("avg_7d", F.avg("revenue").over(w))
```

#### ¿Qué hacen ntile y percent_rank?

`ntile(n)` divide las filas ordenadas en n grupos de tamaño similar (cuartiles con 4); `percent_rank` da la posición relativa de cada fila entre 0 y 1; `cume_dist` da la fracción de filas con un valor menor o igual al actual.

<!-- challenge -->

La deduplicación por el `updated_at` más reciente a veces conserva una fila distinta del mismo cliente entre re-ejecuciones. ¿Por qué y cómo se arregla?

<!-- solution -->

Dos filas comparten el mismo `updated_at`, así que `row_number` rompe el empate de forma arbitraria. Agrega un desempate determinista al orden (por ejemplo `ingested_at` o un número de secuencia).

<!-- takeaways -->

- Particiona por clave, ordena por precedencia, numera y filtra.
- `row_number` es único; `rank` repite empates.
- Agrega desempates para resultados deterministas.

<!-- unit: Comparar filas en el tiempo -->

<!-- goals -->

- Usar lag y lead para comparar con filas anteriores y siguientes.
- Calcular totales acumulados, diferencias y sesiones.

<!-- concept -->

Las ventanas ordenadas responden preguntas de "comparado con antes". Mirar una fila atrás da diferencias día contra día; una suma acumulada da totales acumulados; comparar la hora de cada evento con la del anterior encuentra huecos, y un conteo acumulado de huecos asigna números de sesión.
Todo esto necesita una partición (por tienda, por usuario) y un orden, o Spark pone todas las filas en una sola partición en una sola tarea.

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

#### ¿Cómo detectas sesiones o intervalos entre eventos?

Usa `lag` para obtener la hora del evento anterior, marca una nueva sesión cuando el intervalo supera un umbral, y calcula la suma acumulada de las marcas como número de sesión.

```python
w = Window.partitionBy("user_id").orderBy("event_ts")
sessions = (events
    .withColumn("prev_ts", F.lag("event_ts").over(w))
    .withColumn("new_session",
                (F.col("prev_ts").isNull() |
                 (F.col("event_ts").cast("long") - F.col("prev_ts").cast("long") > 1800)).cast("int"))
    .withColumn("session_id", F.sum("new_session").over(w)))
```

#### ¿Por qué las funciones de ventana pueden ser costosas?

Cada `partitionBy` distinto requiere un shuffle y un ordenamiento. Una ventana sin `partitionBy` lleva todos los datos a una sola partición, lo que es lento y puede quedarse sin memoria; Spark registra una advertencia cuando ocurre. Reutiliza la misma especificación de ventana para varias columnas para que Spark ordene una sola vez.

#### ¿Cómo ejecutas SQL sobre un DataFrame?

Regístralo como vista temporal y consúltalo con `spark.sql`. El resultado es un DataFrame, así que SQL y la API de DataFrames se pueden mezclar libremente; ambos se compilan al mismo plan.

```python
df.createOrReplaceTempView("sales")
top = spark.sql("""
    SELECT city, SUM(amount) AS revenue
    FROM sales
    GROUP BY city
    ORDER BY revenue DESC
""")
```

#### ¿Cuál es la diferencia entre una vista temporal y una vista temporal global?

Una vista temporal solo existe en la SparkSession que la creó. Una vista temporal global se comparte entre sesiones de la misma aplicación y vive en la base de datos `global_temp` (`SELECT * FROM global_temp.my_view`). Ninguna persiste después de que termina la aplicación.

<!-- challenge -->

Un total acumulado por tienda se calcula con `Window.orderBy("date")` sin partición, y Spark advierte que va a mover todos los datos a una sola partición. ¿Qué está mal?

<!-- solution -->

Sin `partitionBy("store")`, la ventana cubre todas las filas, así que Spark ordena todo en una tarea y el total corre a través de las tiendas. Particiona por tienda (y ordena por fecha).

<!-- takeaways -->

- `lag`/`lead` comparan con filas vecinas.
- Sumas acumuladas y marcas de hueco construyen sesiones.
- Particiona siempre las ventanas cuando se pueda.

<!-- unit: Frames y costo -->

<!-- goals -->

- Definir frames con rowsBetween y rangeBetween, y conocer el de por defecto.
- Calcular promedios móviles y buckets, y entender el costo de las ventanas.

<!-- concept -->

El frame de una ventana ordenada decide qué filas ve cada cálculo. El de por defecto va del inicio de la partición hasta la fila actual, empates incluidos, lo que sirve para totales acumulados y sorprende con "último valor". Los frames de filas cuentan filas; los de rango cubren un intervalo de valores, lo que maneja bien los días faltantes en series de tiempo.
Cada particionamiento distinto necesita un shuffle y un ordenamiento, así que muchas ventanas distintas en una consulta multiplican el costo.

<!-- example -->

```python
day = F.col("sale_date").cast("timestamp").cast("long") / 86400
w7 = Window.partitionBy("store").orderBy(day).rangeBetween(-6, 0)
smoothed = sales.withColumn("avg_7d", F.avg("revenue").over(w7)) \
                .withColumn("quartile", F.ntile(4).over(Window.partitionBy("store").orderBy("revenue")))
```

#### ¿Cómo pasas parámetros a spark.sql de forma segura?

Usa consultas parametrizadas (Spark 3.4+), no formateo de cadenas, para evitar la inyección SQL y los errores de comillas.

```python
spark.sql("SELECT * FROM sales WHERE city = :city AND amount > :min",
          args={"city": "Bogotá", "min": 8000})
```

#### ¿Cuál es la diferencia entre tablas gestionadas y externas?

En una tabla gestionada, Spark (o el catálogo) controla los metadatos y los datos, y `DROP TABLE` borra los archivos. En una tabla externa tú indicas la ubicación, y eliminarla solo borra los metadatos. Con Unity Catalog, las tablas gestionadas también obtienen funciones de mantenimiento automático.

#### ¿Qué es el catálogo?

La capa de metadatos que lista bases de datos (esquemas), tablas, vistas y funciones: el metastore de Hive, el AWS Glue Data Catalog o Unity Catalog. En PySpark, `spark.catalog` permite listar tablas, comprobar si existen (`spark.catalog.tableExists`), guardar tablas en caché y refrescar metadatos.

#### ¿Cómo escribes en una tabla en lugar de una ruta?

Con `df.write.mode("overwrite").saveAsTable("analytics.sales")`, o con `insertInto` para una tabla existente (que asocia las columnas por posición, no por nombre, una fuente frecuente de errores). Con Delta Lake también puedes usar `MERGE INTO` en SQL.

#### ¿Qué hace REFRESH TABLE?

Invalida los metadatos y el listado de archivos que Spark tiene en caché para una tabla, algo necesario cuando otro proceso fuera de Spark cambió los archivos. Sin él puedes ver errores de "archivo no encontrado" o datos desactualizados.

<!-- challenge -->

Un promedio móvil de 7 días usa `rowsBetween(-6, 0)`, y en tiendas cerradas algunos días promedia más de 7 días calendario. ¿Cómo lo arreglas?

<!-- solution -->

Usa un frame de rango sobre un valor numérico de día (`rangeBetween(-6, 0)` sobre días desde epoch), para que el frame cubra 7 días calendario sin importar las filas faltantes.

<!-- takeaways -->

- Frame por defecto: del inicio de la partición a la fila actual.
- Los frames de filas cuentan filas; los de rango cubren valores.
- Cada particionamiento de ventana distinto cuesta un shuffle.

### Spark SQL y el catálogo

<!-- unit: SQL sobre DataFrames -->

<!-- goals -->

- Correr SQL sobre DataFrames con vistas temporales.
- Pasar parámetros con seguridad y reutilizar lógica con CTEs y funciones.

<!-- concept -->

DataFrames y SQL son dos frentes del mismo motor: una vista temporal deja que SQL consulte un DataFrame, y los resultados de SQL vuelven a ser DataFrames. Los equipos mezclan ambos libremente y eligen lo que se lea mejor en cada paso.
Dos hábitos mantienen el SQL seguro y mantenible: pasar los valores como parámetros en lugar de formatear strings, lo que evita inyección y errores de comillas, y estructurar las consultas largas con CTEs o funciones reutilizables.

<!-- example -->

```python
orders.createOrReplaceTempView("orders")
top = spark.sql("""
    WITH paid AS (SELECT * FROM orders WHERE status = 'paid' AND ordered_at >= :since)
    SELECT customer_id, sum(amount) AS revenue FROM paid GROUP BY customer_id
    ORDER BY revenue DESC LIMIT 10
""", args={"since": "2026-10-01"})
```

#### ¿Puedes definir funciones SQL reutilizables?

Sí. Registra funciones de Python como UDF con `spark.udf.register` para llamarlas desde SQL, o crea funciones SQL con `CREATE FUNCTION ... RETURN ...`, que se quedan dentro del motor y son más rápidas que las UDF de Python.

#### ¿Qué son las expresiones de tabla comunes (CTE) en Spark SQL?

Bloques `WITH nombre AS (...)` que hacen legibles las consultas complejas. Spark los integra en el plan; una CTE referenciada varias veces puede calcularse varias veces salvo que el optimizador la reutilice, así que guarda en caché o materializa las más pesadas si hace falta.

#### ¿Cómo lees correctamente un archivo CSV?

Declara el esquema y las opciones que necesita el archivo.

```python
df = (spark.read
      .schema("user_id INT, product_id INT, amount DOUBLE, city STRING")
      .option("header", True)
      .option("delimiter", ";")
      .option("encoding", "UTF-8")
      .option("mode", "PERMISSIVE")
      .csv("path/to/files/"))
```

Ten en cuenta que el esquema va en `.schema()`, no en `.options()`.

#### ¿Cuáles son los modos de lectura de CSV/JSON?

`PERMISSIVE` (por defecto) pone en null los campos mal formados y puede guardar la línea original en la columna indicada por `columnNameOfCorruptRecord`; `DROPMALFORMED` descarta las filas incorrectas sin avisar; `FAILFAST` lanza un error con la primera fila incorrecta. En producción, prefiere el modo permisivo con una columna de registros corruptos y pon en cuarentena explícitamente las filas incorrectas.

#### ¿Qué formatos de archivo soporta Spark?

De forma nativa: Parquet, ORC, JSON, CSV, texto, Avro (con un módulo incluido), archivos binarios y fuentes JDBC. Los formatos de tabla como Delta Lake, Apache Iceberg y Apache Hudi agregan transacciones sobre Parquet. Parquet o un formato de tabla debería ser la opción por defecto para analítica.

<!-- challenge -->

Un job arma SQL con un f-string usando un nombre de país dado por el usuario, y falla con "Côte d'Ivoire". ¿Qué cambias?

<!-- solution -->

Usa una consulta parametrizada (`spark.sql(query, args={"country": value})`), que maneja bien las comillas y evita la inyección SQL.

<!-- takeaways -->

- Las vistas temporales permiten consultar DataFrames con SQL.
- Usa parámetros, no formateo de strings.
- CTEs y funciones SQL mantienen legibles las consultas.

<!-- unit: Tablas y el catálogo -->

<!-- goals -->

- Distinguir tablas managed y external y usar el catálogo.
- Escribir en tablas y refrescar sus metadatos.

<!-- concept -->

Las rutas guardan archivos; las tablas agregan nombres, esquemas y permisos a través de un catálogo como el Hive metastore o Unity Catalog. Escribir en tablas en lugar de rutas deja que otros motores y personas encuentren los datos y que se aplique el gobierno.
La propiedad importa: borrar una tabla managed borra sus datos, mientras que borrar una external deja los archivos en su lugar. Cuando los archivos cambian por fuera de Spark, hay que refrescar los metadatos en caché.

<!-- example -->

```python
(daily.write.mode("overwrite")
      .option("overwriteSchema", "true")
      .saveAsTable("analytics.daily_sales"))          # managed table
spark.sql("REFRESH TABLE raw.partner_files")        # files changed outside Spark
spark.catalog.listTables("analytics")
```

#### ¿Por qué Parquet es el formato preferido?

Es columnar y comprimido, guarda el esquema y mantiene estadísticas mín./máx. por grupo de filas. Spark puede leer solo las columnas necesarias (column pruning) y omitir los grupos de filas que no pueden cumplir un filtro (predicate pushdown), lo que lee muchos menos datos que CSV o JSON.

#### ¿Cuáles son los modos de guardado?

`append` agrega datos, `overwrite` los reemplaza, `ignore` no hace nada si ya existen datos, y `error`/`errorifexists` (por defecto) falla si existen. Con `overwrite` en una tabla particionada, la configuración del modo de sobrescritura decide cuánto se reemplaza.

#### ¿Qué es la sobrescritura dinámica de particiones?

Con `spark.sql.sources.partitionOverwriteMode=dynamic`, un overwrite reemplaza solo las particiones presentes en el DataFrame que se escribe, en lugar de la tabla completa. Es la forma segura de reprocesar un día o un país. En Delta, el equivalente es `replaceWhere`.

```python
(df.write.mode("overwrite")
   .option("partitionOverwriteMode", "dynamic")
   .partitionBy("ingest_date")
   .parquet("s3://bucket/sales/"))
```

#### ¿Qué hace partitionBy al escribir?

Crea un directorio por cada valor de las columnas indicadas (`country=CO/`, `country=PE/`). Las consultas que filtran por esas columnas leen solo los directorios correspondientes (partition pruning). Úsalo en columnas de baja cardinalidad que se filtran en la mayoría de las consultas, como una fecha; particionar por una columna de alta cardinalidad crea millones de archivos pequeños.

<!-- challenge -->

Otro proceso agrega archivos a la ubicación de una tabla, pero las consultas de Spark siguen devolviendo resultados viejos. ¿Qué corres?

<!-- solution -->

`REFRESH TABLE <name>` (o `spark.catalog.refreshTable`), que invalida el listado de archivos y los metadatos en caché de Spark para que se vean los archivos nuevos.

<!-- takeaways -->

- Las tablas agregan nombres y gobierno a los archivos.
- Borrar tablas managed borra los datos.
- Refresca las tablas cambiadas por fuera de Spark.

<!-- stage: Entrada y salida de datos -->

### Lectura y escritura de datos

<!-- unit: Leer archivos -->

<!-- goals -->

- Leer CSV y JSON con opciones y modos de lectura explícitos.
- Elegir formatos, rastrear los archivos fuente y manejar la evolución de esquema.

<!-- concept -->

Leer es por donde entran los datos malos, así que merece decisiones explícitas: esquema, encabezado, delimitador, formatos de fecha y qué hacer con las filas malformadas. El modo permissive sigue adelante y registra las líneas rotas; fail-fast se detiene en el primer problema; drop-malformed las esconde.
La elección de formato lo decide todo aguas abajo. Parquet columnar con estadísticas deja que Spark lea solo las columnas necesarias y se salte bloques; los formatos por filas obligan a escaneos completos. Rastrear el archivo fuente de cada fila hace posible depurar.

<!-- example -->

```python
df = (spark.read
      .schema("user_id INT, product_id INT, amount DOUBLE, city STRING, _corrupt STRING")
      .option("header", True).option("sep", ";")
      .option("mode", "PERMISSIVE").option("columnNameOfCorruptRecord", "_corrupt")
      .csv("s3://landing/sales/")
      .withColumn("source_file", F.col("_metadata.file_path")))
```

#### ¿Qué es el problema de los archivos pequeños?

Muchos archivos pequeños (muy por debajo de 128 MB) hacen lenta la lectura, porque cada archivo tiene un costo de listado, apertura y lectura de metadatos, y generan muchas tareas diminutas. Las causas incluyen el exceso de particionado, muchas particiones escritas por tarea y los appends pequeños y frecuentes. Se corrige reparticionando antes de escribir, compactando (`OPTIMIZE` en Delta) y eligiendo mejores columnas de partición.

#### ¿Cómo controlas el número y el tamaño de los archivos de salida?

Reparticiona o aplica coalesce antes de escribir (`df.repartition(16)` o `df.repartition("country")`), define `maxRecordsPerFile`, o deja que el formato de tabla lo gestione (las escrituras optimizadas y la autocompactación de Delta). Con AQE, las particiones del shuffle se unen automáticamente, lo que también ayuda.

#### ¿Cómo lees solo los archivos nuevos de forma incremental?

Con Structured Streaming sobre una fuente de archivos (o Auto Loader de Databricks) y un checkpoint, que registra los archivos procesados; con `trigger(availableNow=True)` se ejecuta como un job por lotes. Las alternativas son guardar una marca de la última fecha procesada o usar el change data feed de un formato de tabla.

#### ¿Cómo lees desde una base de datos relacional?

Con la fuente JDBC. Define `partitionColumn`, `lowerBound`, `upperBound` y `numPartitions` para leer en paralelo; si no, una sola tarea lee toda la tabla. Lleva los filtros a la base de datos con una consulta (opción `query`) y guarda las credenciales en un gestor de secretos.

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

#### ¿Qué es la evolución del esquema y cómo se maneja?

Los cambios del esquema con el tiempo, como columnas nuevas. Los lectores de Parquet pueden combinar esquemas (`mergeSchema`), pero es costoso. Los formatos de tabla lo manejan explícitamente: Delta agrega columnas con `mergeSchema` al escribir o con la evolución del esquema en `MERGE`. Los cambios de nombre y de tipo necesitan migraciones explícitas.

#### ¿Qué hace input_file_name()?

Devuelve la ruta del archivo del que proviene cada fila (en Unity Catalog, usa en su lugar la columna `_metadata.file_path`). Es útil para el linaje y la depuración, por ejemplo para rastrear una fila incorrecta hasta su archivo de origen.

<!-- challenge -->

Un feed CSV diario a veces trae líneas malformadas. El negocio quiere que la carga siga pero sin perder nada en silencio. ¿Cómo lo lees?

<!-- solution -->

Lee en modo `PERMISSIVE` con un esquema explícito y una columna de registros corruptos, escribe las filas con `_corrupt` no nulo (y su archivo fuente) en una tabla de cuarentena y alerta cuando su cantidad supere un umbral.

<!-- takeaways -->

- Declara esquema y opciones al leer texto.
- Modo permissive más cuarentena no pierde nada.
- Prefiere Parquet; rastrea los archivos fuente.

<!-- unit: Escribir archivos -->

<!-- goals -->

- Elegir los modos de guardado y particionar las salidas.
- Evitar archivos pequeños y sobrescribir solo las particiones que le corresponden a una ejecución.

<!-- concept -->

Escribir decide qué tan caras serán todas las lecturas posteriores. Particionar por una columna filtrada con frecuencia deja que los lectores se salten carpetas; tamaños de archivo de unos cien megabytes o más mantienen bajos los costos de listar y abrir. Spark escribe al menos un archivo por tarea por partición, así que sin un paso de repartition la salida se dispara fácil a miles de archivos diminutos.
Los modos de guardado deciden qué pasa con los datos existentes. La sobrescritura dinámica de particiones reemplaza solo las particiones de la salida nueva, lo que hace seguras las re-ejecuciones.

<!-- example -->

```python
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
(daily.repartition("sale_date")                 # one task per date → few files per partition
      .write.mode("overwrite")
      .partitionBy("sale_date")
      .parquet("s3://lake/silver/daily_sales/"))
```

#### ¿Por qué usar un formato de tabla como Delta Lake en lugar de Parquet simple?

Las carpetas Parquet simples no tienen transacciones: un job que falla puede dejar datos escritos a medias, los escritores concurrentes pueden corromper los resultados, y las actualizaciones o eliminaciones obligan a reescribir archivos a mano. Delta, Iceberg y Hudi agregan transacciones ACID, `MERGE`, viaje en el tiempo, validación del esquema y compactación sobre Parquet.

#### ¿Cómo haces un upsert en una tabla Delta desde PySpark?

```python
from delta.tables import DeltaTable

target = DeltaTable.forName(spark, "silver.customers")
(target.alias("t")
   .merge(updates.alias("s"), "t.customer_id = s.customer_id")
   .whenMatchedUpdateAll()
   .whenNotMatchedInsertAll()
   .execute())
```

Elimina primero los duplicados de la fuente por clave: un `MERGE` falla si varias filas de la fuente coinciden con la misma fila del destino.

#### ¿Qué es un shuffle y por qué es costoso?

Un shuffle redistribuye los datos en el clúster para que las filas con la misma clave terminen en la misma partición. Cada tarea escribe su salida en el disco local en bloques por partición de destino, y las tareas del siguiente stage descargan esos bloques por la red. Cuesta E/S de disco, transferencia por red, serialización y memoria, y en casos extremos hace fallar los jobs. Suele ser la parte más costosa de un job.

#### ¿Cómo reduces los shuffles?

- Usa transformaciones narrow cuando sea posible y filtra y selecciona columnas pronto.
- Haz broadcast de las tablas pequeñas en los joins.
- Agrega antes de hacer joins cuando sea posible.
- Evita `repartition`, `distinct` y `orderBy` innecesarios.
- Reutiliza el particionado: los datos con bucketing o coparticionados pueden omitir shuffles.
- Usa `reduceByKey` en lugar de `groupByKey` con RDD.

#### ¿Qué controla spark.sql.shuffle.partitions?

El número de particiones después de un shuffle en las operaciones con DataFrames (200 por defecto). Demasiadas para datos pequeños crean tareas diminutas; muy pocas para datos grandes crean particiones enormes que hacen spill. AQE une particiones automáticamente después del shuffle, así que un valor inicial más alto suele ser seguro.

<!-- challenge -->

Una re-ejecución del job de ayer con `mode("overwrite")` borró la historia completa de la tabla. ¿Qué debió usar?

<!-- solution -->

Sobrescritura dinámica de particiones (`partitionOverwriteMode=dynamic`) con `partitionBy`, para reemplazar solo la partición de ayer, o `replaceWhere`/`MERGE` sobre una tabla Delta.

<!-- takeaways -->

- Particiona por filtros comunes; apunta a archivos grandes.
- Haz repartition antes de escribir para controlar los archivos.
- Sobrescribe solo las particiones que le tocan a la ejecución.

<!-- unit: Bases de datos, incrementos y formatos de tabla -->

<!-- goals -->

- Leer bases relacionales en paralelo y procesar archivos nuevos de forma incremental.
- Usar Delta Lake para transacciones y upserts.

<!-- concept -->

Leer una base por JDBC sin opciones de particionamiento usa una conexión y una tarea, sin importar el tamaño del clúster. Dividir por una columna numérica reparte la lectura, dentro de lo que tolere la base.
Con archivos, releer todo cada día desperdicia tiempo; las fuentes de archivos en streaming siguen qué archivos ya se procesaron. Las carpetas Parquet simples tampoco tienen transacciones, así que un job fallido puede dejar datos a medio escribir. Formatos de tabla como Delta agregan commits atómicos, imposición de esquema y `MERGE` para upserts.

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

#### ¿Qué hacen repartition y coalesce?

- **`repartition(n)`** o `repartition(n, "col")` hace un shuffle completo y produce n particiones de tamaño similar (por hash de las columnas, si se indican). Puede aumentar o disminuir el número de particiones.
- **`coalesce(n)`** une particiones existentes sin un shuffle completo, así que solo puede disminuirlas. Es más barato, pero puede dejar particiones desiguales y reducir el paralelismo del stage anterior.

#### ¿Cuándo deberías usar repartitionByRange?

Cuando necesitas los datos ordenados en rangos de una columna, por ejemplo antes de escribir archivos que deben cubrir cada uno un rango de fechas o de ID, lo que mejora la omisión de datos. Toma una muestra de los datos para elegir los límites de los rangos.

#### ¿Cuántas particiones produce la lectura de archivos?

Aproximadamente el tamaño total dividido entre `spark.sql.files.maxPartitionBytes` (128 MB por defecto), ajustado por `spark.sql.files.openCostInBytes`, que agrupa archivos pequeños. Un archivo que no se puede dividir (como un CSV comprimido con gzip) siempre se convierte en una sola partición, por grande que sea.

#### ¿Cómo se divide la memoria de un executor?

El heap de la JVM menos 300 MB reservados se reparte así: `spark.memory.fraction` (0.6) es memoria unificada que comparten la ejecución (shuffles, joins, ordenamientos, agregaciones) y el almacenamiento (caché), donde el almacenamiento puede desalojarse hasta `spark.memory.storageFraction` (0.5). El resto es memoria de usuario. Fuera del heap está la memoria de overhead (`spark.executor.memoryOverhead`, 10 % o al menos 384 MB), que también cubre los procesos worker de Python.

<!-- challenge -->

Una lectura JDBC de una tabla de 300 GB corre horas con una sola tarea ocupada. ¿Qué opciones agregas?

<!-- solution -->

`partitionColumn` (una columna numérica o de fecha indexada), `lowerBound`, `upperBound` y `numPartitions` (por ejemplo 16), más `fetchsize`, para que Spark abra varias consultas por rango en paralelo.

<!-- takeaways -->

- Particiona las lecturas JDBC o corren como una tarea.
- Las fuentes de archivos en streaming procesan solo archivos nuevos.
- Delta agrega transacciones y `MERGE`.

<!-- stage: Rendimiento -->

### Particionado, shuffles y memoria

<!-- unit: Shuffles y particiones -->

<!-- goals -->

- Explicar los shuffles y reducirlos.
- Controlar la cantidad de particiones con los ajustes de shuffle, repartition y coalesce.

<!-- concept -->

Un shuffle mueve filas por la red para que se encuentren las de la misma clave, escribiendo y leyendo datos de disco en el camino. Es lo más caro que hace Spark, así que filtrar y seleccionar temprano, difundir las tablas pequeñas y evitar distinct u ordenamientos innecesarios rinde rápido.
La cantidad de particiones da forma a cada stage: los splits de entrada deciden el paralelismo de lectura, el ajuste de shuffle decide el paralelismo tras el shuffle, y repartition o coalesce lo ajustan explícitamente, el primero con shuffle y el segundo sin él.

<!-- example -->

```python
spark.conf.set("spark.sql.shuffle.partitions", "400")     # ~150 MB per partition for ~60 GB shuffled
slim = events.select("user_id", "event_type", "event_time").where("event_date = '2026-10-17'")
per_user = slim.groupBy("user_id").count()                 # one shuffle on a small projection
per_user.coalesce(8).write.mode("overwrite").parquet("out/")   # fewer files, no extra shuffle
```

#### ¿Por qué a veces los jobs de PySpark fallan por memoria del contenedor aunque el heap esté bien?

Los workers de Python se ejecutan fuera del heap de la JVM, en el área de overhead. Las UDF de Python pesadas, las pandas UDF con lotes grandes o `toPandas` en los executors pueden superarla, y YARN o Kubernetes matan el contenedor. Aumenta `spark.executor.memoryOverhead` o define `spark.executor.pyspark.memory`, y reduce el tamaño de los lotes de Arrow.

#### ¿Qué es el spill?

Cuando la memoria de ejecución no alcanza para un shuffle, un ordenamiento o una agregación, Spark escribe datos intermedios en disco y los vuelve a leer después. La Spark UI lo muestra como "spill (memory)" y "spill (disk)". El spill hace mucho más lentas las tareas; redúcelo con más particiones y más pequeñas, más memoria por núcleo o menos datos por tarea.

#### ¿Qué causa un OutOfMemoryError en el driver?

Reunir resultados grandes (`collect`, `toPandas`), hacer broadcast de una tabla demasiado grande, planes de consulta enormes (miles de columnas o llamadas a `withColumn` en bucles) y seguir demasiadas tareas o archivos. Evita traer datos al driver y mantén los planes compactos.

#### ¿Qué causa un OutOfMemoryError en los executors?

Particiones sesgadas, muy pocas particiones para el volumen de datos, filas o arrays grandes (resultados enormes de `collect_list`), demasiados núcleos por executor compartiendo la memoria y UDF de Python que consumen mucha memoria. Mira las métricas de las tareas del stage que falla para saber si es una sola tarea (sesgo) o todas (dimensionamiento).

#### ¿Cuál es la diferencia entre cache y persist?

`cache()` guarda los datos con el nivel de almacenamiento por defecto: `MEMORY_ONLY` para los RDD y memoria y disco para los DataFrames. `persist(nivel)` permite elegir el nivel: `MEMORY_ONLY`, `MEMORY_AND_DISK`, `DISK_ONLY` y variantes serializadas y replicadas. Ambos son perezosos: los datos se guardan en caché la primera vez que una acción los calcula. Libéralos con `unpersist()`.

#### ¿Cuándo vale la pena usar caché?

Cuando el mismo DataFrame se usa en varias acciones y es costoso de recalcular, por ejemplo después de un join costoso que alimenta tres salidas distintas. No vale la pena con datos que se usan una sola vez o que son baratos de leer, y le quita memoria a la ejecución. En Databricks serverless, `cache()` y `persist()` no están soportados; escribe una tabla intermedia en su lugar.

<!-- challenge -->

Un job escribe su salida final con `coalesce(1)` para obtener un solo archivo, y el último stage corre en una tarea durante una hora. ¿Qué cambias?

<!-- solution -->

`coalesce(1)` lleva todo el cálculo de ese stage a una tarea. Usa `repartition(1)` (agrega un shuffle pero mantiene paralelo lo anterior), escribe varios archivos o evita la salida de un solo archivo si el consumidor puede leer una carpeta.

<!-- takeaways -->

- Los shuffles son el principal costo de Spark.
- Filtra y selecciona antes del shuffle.
- Repartition hace shuffle; coalesce une sin él.

<!-- unit: Memoria y fallas -->

<!-- goals -->

- Explicar cómo se reparte la memoria del executor y qué es el spill.
- Diagnosticar errores de memoria en driver y executors.

<!-- concept -->

La memoria del executor se comparte entre ejecución (shuffles, ordenamientos, joins) y almacenamiento (caché), con overhead fuera del heap para workers de Python y buffers. Cuando falta memoria de ejecución, Spark derrama a disco, lo que es lento pero sobrevive. Los errores llegan cuando ni eso alcanza o cuando el uso fuera del heap supera el límite del contenedor.
El driver falla por otras razones: traer resultados grandes, difundir tablas que no son pequeñas o planear consultas enormes.

<!-- example -->

| Síntoma | Causa probable |
|---|---|
| OOM del driver tras `collect()` / `toPandas()` | Demasiados datos traídos al driver |
| OOM de executor en unas pocas tareas | Particiones sesgadas |
| "Container killed... exceeding memory limits" | Overhead de Python/fuera del heap muy pequeño |
| "Spill (disk)" grande en las métricas del stage | Particiones muy grandes para la memoria de ejecución |

#### ¿Cuál es la diferencia entre cache y checkpoint?

La caché guarda los datos, pero también conserva todo el linaje, así que las particiones perdidas se recalculan. `checkpoint()` escribe los datos en un almacenamiento confiable y corta el linaje, lo que ayuda con planes muy largos (algoritmos iterativos, bucles). `localCheckpoint()` corta el linaje usando el almacenamiento de los executors, más rápido pero no tolerante a fallas.

#### ¿Cuál es el papel del optimizador Catalyst?

Catalyst convierte el código de DataFrames y SQL en un plan de ejecución eficiente. Aplica reglas como predicate pushdown, column pruning, constant folding y reordenamiento de joins, y después elige los operadores físicos (por ejemplo qué estrategia de join usar). Funciona con DataFrames, Datasets y SQL, no con RDD, cuyas funciones le resultan opacas.

#### ¿Cuáles son las fases de Catalyst?

1. **Análisis:** resuelve los nombres y tipos de columnas y tablas contra el catálogo (del plan lógico sin resolver al plan lógico).
2. **Optimización lógica:** aplica reescrituras basadas en reglas.
3. **Planificación física:** genera planes físicos candidatos y elige uno, usando estadísticas si están disponibles.
4. **Generación de código:** la generación de código whole-stage compila partes del plan en bytecode JVM.

#### ¿Qué son el predicate pushdown y el column pruning?

El **predicate pushdown** lleva los filtros lo más cerca posible de la fuente de datos, así Parquet puede omitir grupos de filas y las fuentes JDBC pueden filtrar en la base de datos. El **column pruning** lee solo las columnas que usa la consulta. Ambos ocurren automáticamente, salvo que algo los bloquee, como un filtro dentro de una UDF de Python.

#### ¿Qué es Adaptive Query Execution (AQE)?

Una capa de optimización, activada por defecto desde Spark 3.2, que vuelve a planificar las consultas en tiempo de ejecución con estadísticas reales de los stages de shuffle terminados. Une particiones de shuffle pequeñas, cambia sort-merge joins a broadcast joins cuando un lado resulta pequeño, y divide las particiones sesgadas en los joins.

<!-- challenge -->

Un stage muestra 400 GB de spill a disco y corre lento, pero no falla. ¿Qué dos cambios pruebas?

<!-- solution -->

Más particiones de shuffle para que cada tarea maneje menos datos (o deja que AQE las una partiendo de un número más alto), y revisa si hay sesgo; si las particiones están balanceadas, da a los executors más memoria por core.

<!-- takeaways -->

- Ejecución y almacenamiento comparten la memoria del executor.
- El spill es lento; un OOM significa que ni el spill alcanzó.
- Los OOM del driver vienen de traer datos y de broadcasts grandes.

<!-- unit: Caché y checkpoints -->

<!-- goals -->

- Elegir entre cache y persist y decidir cuándo vale la pena cachear.
- Distinguir el caché del checkpointing.

<!-- concept -->

Spark recalcula un DataFrame en cada acción salvo que le digas otra cosa. Cachear guarda el resultado calculado en memoria o en disco para que las acciones siguientes lo reutilicen, lo que ayuda cuando un resultado costoso alimenta varias salidas, y desperdicia memoria cuando se usa una sola vez.
El caché conserva el linaje, así que las particiones perdidas se recalculan. El checkpointing escribe los datos y corta el linaje, útil para planes muy largos o iterativos.

<!-- example -->

```python
features = expensive_join(orders, customers).cache()
features.count()                                   # materialize once
features.write.mode("overwrite").parquet("out/features/")
features.groupBy("segment").count().show()         # reuses the cache
features.unpersist()
```

#### ¿Qué es el dynamic partition pruning?

Cuando una tabla de hechos particionada se une con una dimensión filtrada, Spark usa en tiempo de ejecución el resultado del filtro de la dimensión para podar las particiones de la tabla de hechos, así que lee solo las que coinciden. Está activado por defecto y es muy eficaz en consultas sobre esquemas en estrella.

#### ¿Cómo lees un plan de consulta?

Con `df.explain()` o `df.explain(mode="formatted")` (también `extended`, `cost` y `codegen`). Lee el plan físico de abajo hacia arriba: las lecturas (busca `PushedFilters`, `PartitionFilters` y `ReadSchema`), los nodos `Exchange` (shuffles), los tipos de join (`BroadcastHashJoin`, `SortMergeJoin`) y `BatchEvalPython`/`ArrowEvalPython` (UDF de Python).

#### ¿Qué significa un Exchange en el plan?

Un shuffle (`Exchange hashpartitioning`, `rangepartitioning`) o un broadcast (`BroadcastExchange`). Contar los nodos `Exchange` es una forma rápida de estimar cuántos shuffles hace una consulta.

<!-- challenge -->

Un compañero agrega `.cache()` después de cada transformación "para que vaya más rápido", y los executors empiezan a derramar y desalojar. ¿Qué le aconsejas?

<!-- solution -->

Cachear solo los DataFrames costosos que reutilizan varias acciones, materializarlos una vez y hacer `unpersist()` al terminar. Cachear todo desperdicia la memoria que necesita la ejecución.

<!-- takeaways -->

- Cachea resultados que reutilizan varias acciones.
- Haz unpersist al terminar.
- Los checkpoints cortan el linaje; el caché lo conserva.

### Catalyst, AQE y planes de consulta

<!-- unit: Cómo optimiza Catalyst -->

<!-- goals -->

- Describir el papel y las fases de Catalyst.
- Explicar predicate pushdown, column pruning y el optimizador basado en costos.

<!-- concept -->

Tú describes lo que quieres; Catalyst decide cómo. Resuelve los nombres contra el catálogo, reescribe el plan lógico con reglas como empujar filtros hacia abajo y quitar columnas sin uso, y luego elige los operadores físicos, opcionalmente usando estadísticas de tablas para elegir el orden y la estrategia de los joins.
Por eso el código de DataFrames y el SQL rinden igual, y por eso el código Python opaco no se puede optimizar. Cadenas muy largas de transformaciones pueden volver lenta la planeación misma.

<!-- example -->

```python
df = (spark.read.parquet("s3://lake/events/")
        .select("user_id", "event_type", "event_date")
        .where("event_date = '2026-10-17'"))
df.explain(mode="formatted")
# FileScan parquet ... PartitionFilters: [event_date = 2026-10-17]
#                      ReadSchema: struct<user_id, event_type, event_date>
```

#### ¿Qué es la generación de código whole-stage?

Tungsten agrupa varios operadores de un stage (lectura, filtro, proyección, agregación) en una sola función Java generada, eliminando llamadas virtuales y objetos intermedios. En el plan, los operadores con el prefijo `*` o los bloques numerados `WholeStageCodegen` usan generación de código.

#### ¿Qué es el optimizador basado en costos?

Una parte opcional de Catalyst que usa estadísticas de tablas y columnas (número de filas, valores distintos, histogramas) para elegir el orden y la estrategia de los joins. Necesita estadísticas recopiladas con `ANALYZE TABLE ... COMPUTE STATISTICS FOR COLUMNS` y mantenidas al día.

#### ¿Por qué una cadena larga de transformaciones puede hacer lento un job antes de empezar?

Catalyst analiza y optimiza el plan completo, y los planes muy grandes (cientos de llamadas a `withColumn`, bucles que hacen union o join de DataFrames una y otra vez) pueden tardar minutos en optimizarse o desbordar la pila del driver. Combina las proyecciones en un solo `select`, y corta los bucles largos con checkpoints o tablas intermedias.

#### ¿Cómo depurarías un job que tarda mucho más de lo esperado?

Empieza con mediciones, no con suposiciones:

- Abre la Spark UI y encuentra el stage que consume el tiempo.
- Revisa su resumen de tareas: si la duración máxima está muy por encima de la mediana, es sesgo; si todas las tareas son lentas, es el dimensionamiento o el volumen de datos.
- Mira el tamaño de lectura/escritura del shuffle y el spill.
- Lee el plan físico (`explain`) para ver si los filtros se llevan a la fuente, qué estrategias de join se eligieron y si hay UDF de Python.
- Corrige el problema más grande, vuelve a medir y cambia una sola cosa a la vez.

#### ¿Qué muestra la Spark UI?

Las pestañas **Jobs** y **Stages** (duraciones, resúmenes de tareas, métricas de shuffle y spill), **Storage** (datos en caché), **Environment** (configuración), **Executors** (memoria, tiempo de GC, tareas fallidas) y **SQL / DataFrame** (el plan ejecutado con el número de filas por operador). Para las aplicaciones terminadas, usa el Spark History Server.

<!-- challenge -->

Un filtro sobre una tabla Parquet no aparece en `PushedFilters` en el plan, y el job lee todo. ¿Qué podría impedir el pushdown?

<!-- solution -->

El filtro se aplica a través de una UDF de Python, una función sobre la columna o un desajuste de tipos (por ejemplo comparar una columna de fecha con un cast a string). Reescríbelo con funciones incorporadas sobre la columna cruda para que Catalyst lo empuje.

<!-- takeaways -->

- Catalyst analiza, optimiza y planea las consultas.
- Pushdown y pruning reducen los datos leídos.
- Las UDFs de Python y las funciones sobre columnas bloquean la optimización.

<!-- unit: Planes físicos y en ejecución -->

<!-- goals -->

- Explicar AQE y el dynamic partition pruning.
- Leer planes físicos, exchanges y whole-stage code generation.

<!-- concept -->

Los planes estáticos dependen de estimaciones que pueden estar mal. Adaptive Query Execution vuelve a planear en ejecución con estadísticas reales del shuffle: une particiones diminutas, cambia joins a broadcast y divide particiones sesgadas. El dynamic partition pruning usa las claves de una dimensión filtrada para saltarse particiones del hecho.
Leer el plan físico muestra lo que de verdad pasa: los exchanges marcan shuffles o broadcasts, y el whole-stage code generation fusiona operadores en funciones únicas, gran parte de la velocidad de los DataFrames.

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

#### ¿Cuáles son las causas más comunes de jobs lentos en Spark?

En orden aproximado: leer demasiados datos (sin poda, CSV/JSON en lugar de Parquet, muchos archivos pequeños), shuffles innecesarios o grandes, sesgo de datos, spill por particiones demasiado grandes para la memoria, UDF de Python, traer datos al driver, y muy pocas o demasiadas particiones.

#### ¿Qué malas prácticas de PySpark deberías evitar?

- `collect()` o `toPandas()` sobre datos no acotados.
- UDF de Python cuando existe una función integrada.
- `withColumn` en un bucle en lugar de `withColumns` o un solo `select`.
- `crossJoin` accidentales o joins sin condición.
- `repartition(1)`/`coalesce(1)` con datos grandes, que hace pasar todo por una sola tarea.
- `inferSchema` con entradas grandes de producción.
- Llamar `count()` solo para registrar un número, lo que dispara un job completo adicional.
- Reutilizar un DataFrame costoso en varias acciones sin guardarlo en caché ni materializarlo.

#### ¿Por qué count() a veces es lento y cuándo deberías evitarlo?

`count()` es una acción: ejecuta todo el plan hasta ese punto. Llamarlo para registrar logs después de cada paso recalcula todo varias veces. Cuenta una sola vez sobre datos materializados, usa las métricas de la escritura (el historial de la tabla, la Spark UI) o acepta conteos aproximados.

#### ¿Cómo eliges el número de particiones del shuffle?

Apunta a particiones de unos 100 a 200 MB después del shuffle y al menos dos o tres veces más particiones que núcleos en total. Con AQE activado, define un número inicial generoso (o `spark.sql.adaptive.coalescePartitions.initialPartitionNum`) y deja que AQE una las pequeñas.

#### ¿Qué es la ejecución especulativa?

Con `spark.speculation=true`, Spark lanza copias de respaldo de las tareas que van mucho más lentas que otras del mismo stage y usa la que termine primero. Ayuda con nodos lentos, no con el sesgo, porque una tarea sesgada es lenta en cualquier nodo. Las salidas deben ser idempotentes.

<!-- challenge -->

Un plan muestra `Exchange hashpartitioning(customer_id, 2000)`, pero la Spark UI muestra solo 180 tareas en ese stage. ¿Hay algo mal?

<!-- solution -->

No: AQE unió las 2.000 particiones de shuffle en 180 según los tamaños reales (`AQEShuffleRead coalesced`). Está funcionando como debe.

<!-- takeaways -->

- AQE vuelve a planear con estadísticas de ejecución.
- Los exchanges son shuffles o broadcasts.
- El whole-stage codegen fusiona operadores.

### Optimización del rendimiento y depuración

<!-- unit: Diagnosticar jobs lentos -->

<!-- goals -->

- Depurar jobs lentos a partir de mediciones en la Spark UI.
- Relacionar los stages lentos con el código y explicar los efectos de arranque en frío.

<!-- concept -->

El ajuste empieza con evidencia. La Spark UI muestra qué stage se lleva el tiempo, cómo se reparten sus tareas y si hace shuffle, derrama o tiene sesgo; la pestaña SQL relaciona los operadores del plan con los stages, y los jobs con nombre los conectan con tu código.
La mayoría de jobs lentos comparten pocas causas: leer demasiado, shuffles innecesarios, sesgo, spill, archivos pequeños y UDFs de Python. Parte de la lentitud es solo calentamiento: la primera ejecución paga el arranque de la JVM, la generación de código y cachés en frío.

<!-- example -->

```python
spark.sparkContext.setJobDescription("orders: build daily aggregates")
daily = orders.groupBy("order_date").agg(F.sum("amount").alias("revenue"))
daily.write.mode("overwrite").parquet("out/daily/")
# Spark UI → Jobs: "orders: build daily aggregates" → stages → task summary (max vs median)
```

#### ¿Cómo haces que los filtros y joins aprovechen la organización de los datos?

Particiona o agrupa (clustering) las tablas por las columnas que filtran la mayoría de las consultas, y filtra directamente sobre las columnas almacenadas. Un filtro como `to_date(event_ts) = '2026-10-15'` puede no podar; `event_date = '2026-10-15'` sobre una columna de partición o de clustering sí lo hace. Mantén tamaños de archivo sanos con compactación.

#### ¿Cómo reduces el tiempo de recolección de basura?

Usa DataFrames en lugar de RDD de objetos Python, evita executors muy grandes (más de unos 64 GB de heap), usa G1GC (el predeterminado en las versiones recientes de Java), guarda la caché en forma serializada si guardas mucho, y reduce el número de objetos que se crean en las UDF. La pestaña Executors muestra el tiempo de GC por executor.

#### ¿Qué haces con un job que procesa muchos más datos de los necesarios?

Procesa de forma incremental: lee solo los archivos nuevos (streaming con `availableNow`, Auto Loader), escribe solo las particiones afectadas (`replaceWhere`, sobrescritura dinámica), haz merge solo de las filas que cambiaron, y omite los pasos cuyas entradas no cambiaron. Los datos más baratos son los que no procesas.

#### ¿Qué efecto tienen demasiadas columnas o filas muy anchas?

Las filas anchas aumentan la memoria por fila, el tamaño de los shuffles y la complejidad del plan. Selecciona pronto solo las columnas necesarias, evita arrastrar columnas grandes de texto o binarias a través de los joins, y divide las tablas muy anchas si la mayoría de las consultas usa solo unas pocas columnas.

#### ¿Cómo encuentras qué parte de tu código produjo un stage lento?

En la pestaña SQL / DataFrame, el plan ejecutado vincula los operadores con los stages. Ponles nombre a tus jobs con `spark.sparkContext.setJobDescription("load silver companies")` (o `setJobGroup`), para que la pestaña Jobs muestre a qué paso pertenece cada job.

<!-- challenge -->

El resumen de tareas de un stage muestra una duración mediana de 20 s y una máxima de 25 min. ¿Qué te dice eso y qué revisas después?

<!-- solution -->

Sesgo: una tarea tiene muchísimos más datos. Revisa la entrada y el shuffle read de esa tarea, encuentra la(s) clave(s) caliente(s) y aplica el manejo de sesgo de AQE, broadcast o salting.

<!-- takeaways -->

- Mide primero: stage, tareas, shuffle, spill.
- Mediana contra máximo de las tareas revela el sesgo.
- Ponle nombre a los jobs para ligar stages y código.

<!-- unit: Antipatrones y soluciones -->

<!-- goals -->

- Reconocer antipatrones comunes de PySpark.
- Evitar acciones innecesarias, filas anchas y sobreprocesamiento.

<!-- concept -->

Muchos jobs lentos no están mal configurados; hacen trabajo innecesario. Traer datos al driver, usar UDFs de Python donde existen funciones, llamar `count()` para los logs, recorrer filas en Python, cargar cientos de columnas sin uso o recalcular años de historia cada día multiplican el costo.
Las soluciones consisten sobre todo en hacer menos: menos acciones, menos columnas, procesamiento incremental y funciones incorporadas.

<!-- example -->

| Antipatrón | Solución |
|---|---|
| `count()` tras cada paso para los logs | Registrar conteos una vez, desde las métricas de escritura |
| Bucle de Python sobre `collect()` | Expresiones de columna o joins |
| `SELECT *` de 300 columnas | Seleccionar las 12 necesarias |
| Reconstruir 5 años cada noche | Procesar solo las particiones nuevas |

#### ¿Por qué la primera ejecución de un job es más lenta que las siguientes?

Por el calentamiento de la JVM, la carga de clases, la generación de código, el escalado automático del clúster y las cachés frías (la caché de archivos del sistema operativo y, en Databricks, la caché en disco). Mide el rendimiento en varias ejecuciones y con un volumen de datos realista.

#### ¿Qué es una UDF y por qué una UDF de Python es lenta?

Una función definida por el usuario aplica código Python propio a cada fila. Cada fila debe serializarse de la JVM a un worker de Python, procesarse en el intérprete de Python y serializarse de vuelta. Catalyst no puede ver su interior, así que no puede optimizarla ni llevar filtros a través de ella. Las funciones integradas se ejecutan dentro de la JVM y suelen ser muchas veces más rápidas.

```python
from pyspark.sql import functions as F
from pyspark.sql.types import StringType

@F.udf(returnType=StringType())
def clean_city(city):
    return city.strip().title() if city else None

# La versión integrada es más rápida y hace lo mismo:
df.withColumn("city", F.initcap(F.trim("city")))
```

#### ¿Qué es una pandas UDF?

Una UDF vectorizada (`@pandas_udf`) que recibe Series o DataFrames de pandas por lotes transferidos con Apache Arrow, en lugar de una fila a la vez. Es mucho más rápida que una UDF fila por fila, y dentro puedes usar operaciones vectorizadas de pandas y NumPy.

```python
import pandas as pd
from pyspark.sql.functions import pandas_udf

@pandas_udf("double")
def to_cop(amount: pd.Series, rate: pd.Series) -> pd.Series:
    return amount * rate

df.withColumn("amount_cop", to_cop("amount", "fx_rate"))
```

#### ¿Qué son las UDF de Python optimizadas con Arrow?

Desde Spark 3.5, las UDF de Python normales pueden usar Arrow para la serialización (`@udf(useArrow=True)` o `spark.sql.execution.pythonUDF.arrow.enabled`). La función sigue procesando una fila a la vez, pero la transferencia de datos es más rápida.

<!-- challenge -->

Un pipeline llama `df.count()` después de cada uno de sus 8 pasos para registrar el avance, y el tiempo se duplicó. ¿Por qué y qué haces?

<!-- solution -->

Cada `count()` es una acción que recalcula el plan hasta ese punto. Quítalos (o cachea una vez si los conteos son esenciales) y registra los conteos desde la escritura final o con métricas baratas.

<!-- takeaways -->

- Cada acción recalcula su plan.
- Selecciona menos columnas; evita bucles de Python.
- Procesa de forma incremental en vez de reprocesar la historia.

<!-- unit: Perillas de ajuste -->

<!-- goals -->

- Elegir la cantidad de particiones de shuffle y usar la especulación.
- Aprovechar la organización de los datos y reducir la garbage collection.

<!-- concept -->

Cuando el trabajo ya es liviano, importan unos pocos ajustes. Las particiones de shuffle deben dimensionarse para que cada una tenga entre cien y doscientos megabytes, con AQE ajustando desde un punto de partida generoso. La especulación vuelve a correr las tareas atascadas en máquinas lentas.
La organización de los datos suele ganarle a la configuración: las tablas particionadas o con clustering sobre filtros comunes dejan que Spark se salte la mayoría de los datos. La garbage collection baja con DataFrames en lugar de objetos Python y con executors de tamaño moderado.

<!-- example -->

```properties
spark.sql.adaptive.enabled=true
spark.sql.adaptive.coalescePartitions.enabled=true
spark.sql.shuffle.partitions=2000          # generous start; AQE coalesces
spark.speculation=true
spark.speculation.quantile=0.9
```

#### ¿Qué hacen applyInPandas y mapInPandas?

`groupBy(...).applyInPandas(func, schema)` ejecuta una función de pandas sobre cada grupo como un DataFrame de pandas (cada grupo debe caber en memoria). `mapInPandas(func, schema)` ejecuta una función sobre un iterador de DataFrames de pandas por partición, por ejemplo para aplicar un modelo de machine learning por lotes.

#### ¿Qué es una UDTF de Python?

Una función de tabla definida por el usuario (Spark 3.5) que devuelve varias filas por entrada, definida como una clase Python con un método `eval` que produce filas. Es útil para analizar o expandir registros de formas que `explode` no puede expresar.

#### ¿Cómo evitas las UDF?

Busca primero en `pyspark.sql.functions`: las funciones de texto, fechas, regex, arrays, maps, JSON y de orden superior cubren la mayoría de las necesidades. Combínalas con `when`, `expr` y expresiones SQL. Usa una pandas UDF si de verdad necesitas bibliotecas de Python, y una UDF fila por fila solo como último recurso.

#### ¿Por qué las UDF deben manejar None?

Las columnas pueden contener nulls, y las funciones de Python los reciben como `None`. Una UDF que llama `city.strip()` sin comprobarlo hace fallar todo el job con el primer null. Declara también el tipo de retorno correcto: una discrepancia devuelve null sin avisar.

<!-- challenge -->

Un job diario filtra una tabla de 10 TB por `country` y `event_date`, y lee 9 TB cada vez. ¿Qué cambio de organización ayuda más?

<!-- solution -->

Particiona (o agrupa) la tabla por `event_date`, y haz clustering o Z-order por `country` dentro, para que el filtro pode particiones y archivos y lea una fracción pequeña.

<!-- takeaways -->

- Apunta a 100–200 MB por partición de shuffle.
- La organización de los datos gana a casi toda configuración.
- Executors moderados y DataFrames reducen la GC.

### UDF, pandas y Arrow

<!-- unit: UDFs de Python y alternativas -->

<!-- goals -->

- Explicar por qué las UDFs de Python son lentas y cómo evitarlas.
- Escribir UDFs seguras ante nulos y conocer las Python UDTFs.

<!-- concept -->

Una UDF de Python corre tu función fila por fila en un proceso Python junto al executor. Cada fila se serializa fuera de la JVM y de vuelta, y Catalyst no puede ver adentro, así que los filtros no pueden atravesarla. Por eso las funciones incorporadas, incluidas las de orden superior sobre arrays, deben ir primero.
Cuando una UDF de verdad hace falta, debe manejar `None`, porque los nulos llegan como `None` de Python. Las Python UDTFs extienden la idea a funciones que devuelven varias filas.

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

#### ¿Cómo usas un modelo de machine learning en PySpark?

Haz broadcast del modelo, o cárgalo una vez por partición, y aplícalo con una pandas UDF o `mapInPandas` para que las predicciones sean vectorizadas. `spark_udf` de MLflow envuelve un modelo registrado como una UDF de Spark.

#### ¿Cuándo deberías convertir a pandas?

Cuando los datos ya son pequeños después de la agregación (por ejemplo unos miles de filas para un gráfico o un informe) y necesitas funciones que solo tiene pandas. Agrega primero en Spark y después llama `toPandas()` sobre el resultado pequeño.

#### ¿Qué es Structured Streaming?

La API de procesamiento de flujos de Spark, que trata un flujo como una tabla sin límite que crece con el tiempo. Escribes las mismas operaciones de DataFrame que en batch, y Spark las ejecuta de forma incremental en micro-lotes, guardando el estado y el progreso en un checkpoint.

#### ¿Cuáles son los componentes principales de una consulta de streaming?

Una fuente (`readStream` desde Kafka, archivos, Delta o Auto Loader), transformaciones, un destino (`writeStream` hacia Delta, Kafka, archivos o `foreachBatch`), un trigger, un modo de salida y una ubicación de checkpoint.

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

<!-- challenge -->

Una UDF que pasa a mayúsculas y recorta nombres falla con `AttributeError: 'NoneType' object has no attribute 'strip'`. ¿Cuáles son dos soluciones?

<!-- solution -->

Reemplázala por funciones incorporadas (`F.upper(F.trim("name"))`), que manejan nulos; o protege la UDF con `if s is None: return None`.

<!-- takeaways -->

- Las UDFs de Python serializan cada fila y bloquean la optimización.
- Prueba primero las funciones incorporadas y de orden superior.
- Las UDFs deben manejar `None`.

<!-- unit: Python vectorizado con Arrow -->

<!-- goals -->

- Usar pandas UDFs, UDFs optimizadas con Arrow, applyInPandas y mapInPandas.
- Aplicar modelos de ML en Spark y decidir cuándo pasar a pandas.

<!-- concept -->

Cuando Python es inevitable, procesa lotes en lugar de filas. Arrow mueve los datos entre la JVM y Python en lotes columnares, y las pandas UDFs reciben Series o DataFrames completos, así el código vectorizado de pandas y NumPy corre a una velocidad casi nativa.
Las funciones por grupo corren lógica arbitraria de pandas por grupo, lo que sirve para modelos por entidad o transformaciones complejas. Los modelos se cargan una vez por lote o partición, no por fila. Y cuando los datos son pequeños tras agregar, pandas simple es lo más sencillo.

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

#### ¿Qué triggers hay disponibles?

El predeterminado ejecuta micro-lotes lo más rápido posible; `processingTime="1 minute"` los ejecuta a intervalos fijos; `availableNow=True` procesa todo lo disponible en varios lotes y se detiene, lo que es ideal para jobs incrementales programados; `once=True` está obsoleto en favor de `availableNow`. El modo continuo existe, pero es experimental y limitado.

#### ¿Cuáles son los modos de salida?

`append` escribe solo las filas nuevas (el predeterminado; las agregaciones necesitan un watermark), `update` escribe las filas que cambiaron desde el último trigger, y `complete` reescribe todo el resultado cada vez (solo para agregaciones, y solo práctico con resultados pequeños).

#### ¿Para qué sirve el checkpoint?

Guarda los offsets procesados y el estado de las operaciones con estado, así que una consulta reiniciada continúa donde se detuvo sin perder ni duplicar datos. Cada consulta necesita su propia ubicación de checkpoint, y algunos cambios en la consulta (como cambiar las agregaciones) no son compatibles con un checkpoint existente.

#### ¿Qué es un watermark?

Un umbral sobre el tiempo del evento que le dice a Spark cuánto pueden tardar en llegar los datos (`withWatermark("event_ts", "10 minutes")`). Spark lo usa para cerrar las agregaciones por ventana y descartar el estado antiguo. Sin watermark, el estado de las agregaciones y de los joins entre flujos crece para siempre.

#### ¿Cómo agregas por ventanas de tiempo en un flujo?

Agrupa por un `window` (fijo o deslizante) sobre la columna de tiempo del evento, con un watermark.

```python
counts = (events
          .withWatermark("event_ts", "10 minutes")
          .groupBy(F.window("event_ts", "5 minutes"), "store")
          .count())
```

<!-- challenge -->

Un modelo de scikit-learn se aplica con una UDF común que carga el modelo dentro de la función, y puntuar 50 millones de filas tarda horas. ¿Qué cambias?

<!-- solution -->

Usa `mapInPandas` (o una pandas UDF) que cargue el modelo una vez por partición o lote y llame a `predict` sobre DataFrames completos, con el archivo del modelo difundido o leído una vez del almacenamiento.

<!-- takeaways -->

- Arrow mueve los datos en lotes columnares.
- Las pandas UDFs vectorizan la lógica de Python.
- Carga los modelos una vez por partición, no por fila.

<!-- stage: Streaming y producción -->

### Structured Streaming

<!-- unit: Consultas en streaming -->

<!-- goals -->

- Describir el modelo y los componentes de Structured Streaming.
- Elegir triggers y output modes y explicar el checkpoint.

<!-- concept -->

Structured Streaming trata un stream como una tabla que no deja de crecer. Escribes el mismo código de DataFrames que para batch; Spark lo corre de forma incremental en cada micro-batch de datos nuevos. Una consulta tiene una fuente, transformaciones, un sink, un trigger que decide cuándo corren los lotes y un output mode que decide qué se escribe.
El checkpoint guarda el avance y el estado, así una consulta reiniciada continúa justo donde paró. Perderlo significa empezar de cero.

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

#### ¿Qué hace foreachBatch?

Te entrega cada micro-lote como un DataFrame normal junto con un ID de lote, para que puedas usar API batch que los destinos de streaming no soportan: `MERGE` en Delta, escribir en varios destinos o llamar a sistemas externos. Haz que la función sea idempotente, por ejemplo usando el ID del lote, porque un lote puede volver a ejecutarse tras una falla.

```python
def upsert(batch_df, batch_id):
    (DeltaTable.forName(spark, "silver.orders").alias("t")
       .merge(batch_df.alias("s"), "t.order_id = s.order_id")
       .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())

stream.writeStream.foreachBatch(upsert).option("checkpointLocation", ckpt).start()
```

#### ¿Qué garantías ofrece Structured Streaming?

Procesamiento exactamente una vez de extremo a extremo cuando la fuente se puede releer (Kafka, archivos) y el destino es idempotente o transaccional (Delta, destinos de archivos, `foreachBatch` idempotente). Con destinos no idempotentes (llamar a una API), obtienes al menos una vez.

#### ¿Cómo eliminas duplicados en un flujo?

Con `dropDuplicates(["event_id"])` y un watermark, para que el estado de los ID ya vistos pueda descartarse después de un tiempo, o con `dropDuplicatesWithinWatermark` (Spark 3.5). Sin watermark, el conjunto de claves vistas crece sin límite.

#### ¿Cómo unes flujos?

Los joins entre un flujo y datos estáticos (enriquecer eventos con una tabla de dimensión) son simples y sin estado. Los joins entre dos flujos necesitan watermarks en ambos lados y una condición de tiempo, para que Spark sepa cuánto tiempo conservar el estado de cada lado.

#### ¿Cómo monitoreas una consulta de streaming?

`query.status`, `query.lastProgress` y `query.recentProgress` muestran la tasa de entrada, la tasa de procesamiento, la duración de los lotes y el tamaño del estado. La pestaña Structured Streaming de la Spark UI los grafica, y `StreamingQueryListener` envía las métricas a los sistemas de monitoreo. Configura una alerta cuando la tasa de procesamiento se mantenga por debajo de la de entrada.

<!-- challenge -->

Un equipo corre un job de streaming 24/7 aunque los reportes aguas abajo se refrescan una vez al día. ¿Cómo conservan el código de streaming pero bajan el costo?

<!-- solution -->

Usa `trigger(availableNow=True)` y programa el job a diario: procesa todos los datos nuevos de forma incremental con el mismo checkpoint y luego se detiene, así el clúster corre solo minutos al día.

<!-- takeaways -->

- Los streams son tablas sin fin procesadas de forma incremental.
- Los triggers deciden cuándo corren los lotes.
- El checkpoint guarda el avance y el estado.

<!-- unit: Event time y estado -->

<!-- goals -->

- Agregar por ventanas de event time con watermarks.
- Deduplicar y cruzar streams con estado acotado.

<!-- concept -->

Las agregaciones en streaming necesitan saber cuándo una ventana de tiempo está completa, pero los eventos llegan tarde. Un watermark le dice a Spark qué tan tarde pueden llegar los datos; las ventanas más viejas que eso se cierran y su estado se descarta. Sin watermarks, el estado crece para siempre.
La misma lógica aplica a la deduplicación y a los joins entre streams: ambos necesitan estado y límites de tiempo para poder limpiarlo. Cruzar un stream con una tabla estática no necesita estado.

<!-- example -->

```python
per_window = (events
  .withWatermark("event_time", "15 minutes")
  .dropDuplicates(["event_id", "event_time"])
  .groupBy(F.window("event_time", "5 minutes"), "store_id")
  .agg(F.sum("amount").alias("revenue")))
```

#### ¿Cómo estructuras el código PySpark para que se pueda probar?

Escribe las transformaciones como funciones que reciben y devuelven DataFrames, sin leer ni escribir dentro de ellas. Mantén los jobs livianos: leen las entradas, llaman a las funciones y escriben los resultados. Las rutas, fechas y nombres de tablas son parámetros, no constantes.

```python
def latest_per_key(df, key, order_col):
    w = Window.partitionBy(key).orderBy(F.col(order_col).desc())
    return df.withColumn("_rn", F.row_number().over(w)).filter("_rn = 1").drop("_rn")
```

#### ¿Cómo haces pruebas unitarias de código PySpark?

Con pytest y una fixture de SparkSession local con alcance de sesión, DataFrames pequeños en memoria y las funciones de comparación de `pyspark.testing` (Spark 3.5): `assertDataFrameEqual` y `assertSchemaEqual`.

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

#### ¿Por qué poner un valor bajo en spark.sql.shuffle.partitions en las pruebas?

Con el valor por defecto de 200, cada prueba pequeña que hace un shuffle crea 200 tareas diminutas, lo que hace lenta la suite de pruebas. De dos a cuatro particiones bastan para datos pequeños.

#### ¿Qué más deberían cubrir las pruebas además de las unitarias?

Una ejecución de extremo a extremo de todo el pipeline sobre archivos sintéticos pequeños, la idempotencia (volver a ejecutar con la misma entrada no cambia nada), casos límite como nulls, entradas vacías, duplicados y filas mal formadas, y controles de calidad de datos sobre los datos reales en producción.

<!-- challenge -->

Una deduplicación en streaming con `dropDuplicates("event_id")` corre bien semanas y luego los executors se quedan sin memoria. ¿Por qué?

<!-- solution -->

Sin watermark, Spark guarda como estado cada ID de evento que ha visto. Agrega un watermark sobre el event time e incluye la columna de tiempo en las claves de deduplicación, para que el estado viejo se pueda descartar.

<!-- takeaways -->

- Los watermarks acotan el retraso y el estado.
- Las ventanas agrupan por event time.
- La deduplicación y los joins de streams necesitan límites de tiempo.

<!-- unit: Sinks, garantías y monitoreo -->

<!-- goals -->

- Usar foreachBatch para sinks tipo batch.
- Explicar las garantías exactly-once y monitorear consultas en streaming.

<!-- concept -->

El streaming promete resultados exactly-once cuando la fuente puede repetir datos y el sink escribe de forma idempotente o transaccional; el checkpoint une ambas cosas. Para sinks sin soporte nativo de streaming, como `MERGE` en una tabla o escrituras a varios lugares, `foreachBatch` te entrega cada micro-batch como un DataFrame común.
Los streams en marcha necesitan vigilancia: las tasas de entrada, la duración de los lotes y el tamaño del estado muestran si una consulta se mantiene al día o se va quedando atrás.

<!-- example -->

```python
def upsert(batch_df, batch_id):
    (DeltaTable.forName(spark, "silver.orders").alias("t")
       .merge(batch_df.alias("s"), "t.order_id = s.order_id")
       .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())

q = stream.writeStream.foreachBatch(upsert).option("checkpointLocation", CHK).start()
print(q.lastProgress["inputRowsPerSecond"], q.lastProgress["batchDuration"])
```

#### ¿Cómo haces que los jobs sean idempotentes?

Escribe con `overwrite` de particiones específicas, `replaceWhere` o `MERGE` en lugar de un `append` ciego, deriva las salidas solo de las entradas (sin que `current_date()` decida qué procesar, salvo que sea un parámetro) y usa claves deterministas. Una nueva ejecución después de una falla debe producir exactamente el mismo resultado.

#### ¿Cuáles son buenas convenciones de código para PySpark?

Importa las funciones como `F`, prefiere expresiones de columna en lugar de cadenas al construir la lógica, usa esquemas explícitos, encadena las transformaciones entre paréntesis en lugar de usar barras invertidas, ponles alias legibles a las agregaciones, evita `select("*")` antes de escribir, y mantén las reglas de negocio en funciones con nombre y con pruebas.

#### ¿Cómo registras información útil sin hacer lento el job?

Registra en el driver: los parámetros, las rutas de entrada, las decisiones del plan y los tiempos. Evita acciones solo para los logs; usa las métricas de escritura, el historial de la tabla o un único conteo de la salida final. Usa `setJobDescription` para que los logs y la Spark UI coincidan.

<!-- challenge -->

Una función `foreachBatch` anexa cada lote a una tabla. Tras una falla y un reinicio, algunas filas aparecen dos veces. ¿Por qué y cómo se arregla?

<!-- solution -->

Al reiniciar, el último lote puede repetirse, y un append simple no es idempotente. Usa `MERGE` sobre una clave o escribe con el ID del lote (por ejemplo `txnAppId`/`txnVersion` de Delta) para que se salten las repeticiones.

<!-- takeaways -->

- Exactly-once necesita fuentes repetibles y sinks idempotentes.
- `foreachBatch` permite MERGE y escrituras a varios sinks.
- Monitorea tasa de entrada, duración de lotes y estado.

### Pruebas y buenas prácticas

<!-- unit: Probar código PySpark -->

<!-- goals -->

- Estructurar las transformaciones para que se puedan probar unitariamente.
- Escribir pruebas rápidas con pytest y una SparkSession local.

<!-- concept -->

El código PySpark probable separa la lógica de la I/O: las funciones reciben DataFrames y devuelven DataFrames, mientras la lectura y la escritura ocurren en los bordes. Así bastan una sesión local pequeña y DataFrames diminutos en memoria para probar cada transformación.
La velocidad viene de compartir una sesión y bajar las particiones de shuffle para que las pruebas pequeñas no creen cientos de tareas vacías. Más allá de lo unitario, una ejecución de punta a punta con archivos sintéticos pequeños y una prueba de re-ejecución atrapan problemas de integración.

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

#### ¿Cómo manejas los registros incorrectos en producción?

Lee en modo permisivo con una columna de registros corruptos, valida las filas con reglas explícitas, envía los fallos a una tabla de cuarentena con el motivo, y detén el job si la proporción de filas incorrectas supera un umbral. Los descartes silenciosos (`DROPMALFORMED`) ocultan los problemas.

#### Problema práctico 1: agregaciones

Dado este archivo CSV:

```csv
user_id;product_id;amount;city
1;101;12500.0;Bogota
2;102;9000.0;Cartagena
1;103;3000.0;Bogota
4;104;12500.0;Medellin
5;101;6250.0;Bogota
2;102;9000.0;Medellin
```

- Carga el CSV en un DataFrame.
- Calcula el monto total por usuario.
- Calcula el monto promedio de las transacciones por ciudad.
- Conserva solo las ciudades donde el monto promedio de las transacciones es mayor que 8000.
- Devuelve los resultados como dos DataFrames, `total_per_user` y `city_avg`, y guarda uno de ellos en caché.

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
city_avg.show()     # la primera acción llena la caché
```

#### Problema práctico 2: joins

Dados estos dos archivos:

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

- Carga ambos DataFrames.
- Únelos para obtener los nombres de los usuarios y los montos de las transacciones.
- Calcula el total gastado por usuario.
- Ordena por monto total, de mayor a menor.

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

Hacer el join por `"user_id"` conserva una sola columna clave, y agrupar por `user_id` además de `name` evita juntar a dos usuarios distintos con el mismo nombre.

#### Problema práctico 3: funciones de ventana

Con el DataFrame `sales_df` de la sección de funciones de ventana (date, store, revenue), calcula los ingresos acumulados en el tiempo de cada tienda y la diferencia con el día anterior.

```python
from pyspark.sql import Window, functions as F

w = Window.partitionBy("store").orderBy("date")
window_revenue = (sales_df
                  .withColumn("cumulative_revenue", F.sum("revenue").over(w))
                  .withColumn("day_to_day_diff", F.col("revenue") - F.lag("revenue").over(w)))
window_revenue.show()
```

<!-- challenge -->

Una suite de 60 pruebas tarda 15 minutos, casi todo esperando shuffles diminutos. ¿Qué dos ajustes la cambian más?

<!-- solution -->

Un fixture de SparkSession con scope de sesión (arrancar Spark una vez) y `spark.sql.shuffle.partitions` en 1–4, para que las pruebas no corran 200 tareas por shuffle.

<!-- takeaways -->

- DataFrame que entra, DataFrame que sale: fácil de probar.
- Una sesión local; pocas particiones de shuffle.
- Agrega pruebas de punta a punta y de re-ejecución.

<!-- unit: Hábitos de producción -->

<!-- goals -->

- Hacer idempotentes los jobs y manejar registros malos.
- Seguir convenciones de código y registrar logs sin frenar los jobs.

<!-- concept -->

Los jobs de producción se van a volver a correr, van a recibir datos malos y los van a leer colegas a las 3 a. m. Las escrituras idempotentes, sobrescribiendo las particiones que le tocan a una ejecución o haciendo merge sobre claves, hacen seguras las re-ejecuciones. Los registros malos van a cuarentena con contexto suficiente para corregirlos.
Un código legible y logs baratos completan el cuadro: imports y nombres consistentes, esquemas explícitos y logs desde el driver sobre parámetros y decisiones, no acciones disparadas solo para imprimir conteos.

<!-- example -->

```python
log.info("run date=%s input=%s", run_date, input_path)
valid = parsed.where(F.col("_corrupt").isNull())
(parsed.where(F.col("_corrupt").isNotNull())
       .withColumn("run_date", F.lit(run_date))
       .write.mode("append").saveAsTable("quarantine.orders"))
valid.write.mode("overwrite").option("replaceWhere", f"order_date = '{run_date}'").saveAsTable("silver.orders")
```

#### Problema práctico 4: eliminación de duplicados

Una tabla `customers_raw` recibe cada cambio de un cliente, con `customer_id`, `email`, `updated_at` e `ingested_at`. Construye una tabla con exactamente una fila por cliente: la versión más reciente, usando `ingested_at` para desempatar.

```python
w = Window.partitionBy("customer_id").orderBy(F.col("updated_at").desc(), F.col("ingested_at").desc())
customers = (spark.table("customers_raw")
             .withColumn("rn", F.row_number().over(w))
             .filter("rn = 1")
             .drop("rn"))
```

#### Problema práctico 5: productos principales por ciudad

Con los datos de ventas del problema 1, devuelve los dos productos con más ingresos en cada ciudad, incluidos los empates.

```python
revenue = df_sales.groupBy("city", "product_id").agg(F.sum("amount").alias("revenue"))
w = Window.partitionBy("city").orderBy(F.col("revenue").desc())
top2 = revenue.withColumn("rank", F.dense_rank().over(w)).filter("rank <= 2")
```

#### Problema práctico 6: aplanar JSON anidado

Cada pedido es un documento JSON con un `order_id`, un struct `customer` (`id`, `city`) y un array `items` de structs (`sku`, `qty`, `price`). Produce una fila por artículo con el ID del pedido, la ciudad del cliente y el total de la línea.

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

Usa `explode_outer` si los pedidos sin artículos también deben aparecer.

#### Problema práctico 7: encontrar qué cambió entre dos fotos

Recibes cada mes una foto completa de un registro. Compara la foto de este mes con la del mes anterior (ambas con `company_id`, `name`, `status`) y clasifica cada empresa como nueva, eliminada, modificada o sin cambios.

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

`concat_ws` omite los nulls, así que un cambio de null a cadena vacía pasa desapercibido. Envuelve las columnas en `coalesce(col, lit("<null>"))` si esa distinción importa.

<!-- challenge -->

Un job anexa los datos de cada día con `mode("append")`, y una re-ejecución tras una falla duplicó los ingresos de ayer. ¿Cómo haces seguras las re-ejecuciones?

<!-- solution -->

Reemplaza solo la porción de la ejecución: `replaceWhere` sobre la fecha (Delta), sobrescritura dinámica de particiones o `MERGE` sobre la clave de negocio, para que correr dos veces dé el mismo resultado.

<!-- takeaways -->

- Las escrituras idempotentes hacen seguras las re-ejecuciones.
- Pon en cuarentena los registros malos con contexto.
- Registra desde el driver; evita acciones para los logs.
