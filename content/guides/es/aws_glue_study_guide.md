## Guía de estudio de AWS Glue

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de AWS Glue: unas 200 preguntas](../../images/aws_glue_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre AWS Glue: el Data Catalog, los crawlers, los jobs ETL con Spark, los DynamicFrames, los job bookmarks, los workers y los costos, el streaming, la calidad de datos, la orquestación, la seguridad con Lake Formation y la optimización del rendimiento. Las respuestas reflejan el servicio en 2026. Abre una pregunta para ver su respuesta, o usa el filtro para buscar en toda la guía.

<!-- QA -->

### Fundamentos

#### ¿Qué es AWS Glue?

Un servicio serverless de integración de datos de AWS para descubrir, preparar, mover e integrar datos. Sus partes principales son el Glue Data Catalog (un repositorio central de metadatos), los crawlers (descubrimiento de esquemas), los jobs ETL (Apache Spark o Python), Glue Studio (creación visual), Data Quality, DataBrew (preparación visual de datos) y los workflows para la orquestación.

#### ¿Qué significa "serverless" en Glue?

No aprovisionas ni administras clusters: eliges un tipo y un número de workers (o dejas que el autoescalado decida), Glue arranca el entorno para la ejecución del job y solo pagas el tiempo que corre el job, por segundo.

#### ¿Cuáles son los principales casos de uso de Glue?

Construir data lakes en S3 (catalogar y transformar los datos en bruto a Parquet o Iceberg), ETL hacia Redshift u otras bases de datos, preparar datos para Athena y machine learning, ingesta CDC y streaming, y ofrecer un catálogo de metadatos compartido para Athena, EMR, Redshift Spectrum y Lake Formation.

#### ¿Qué es el Glue Data Catalog?

Un repositorio de metadatos administrado y compatible con el Hive metastore, por cuenta y región. Guarda bases de datos, tablas (esquema, ubicación, formato, particiones, estadísticas), conexiones y funciones definidas por el usuario. Athena, EMR, Redshift Spectrum, los jobs de Glue y muchos otros servicios lo usan para saber dónde están los datos y cómo leerlos.

#### ¿Qué es una base de datos de Glue?

Un contenedor lógico de tablas en el Data Catalog. No guarda datos; agrupa definiciones de tablas, y con Lake Formation se pueden conceder permisos a nivel de base de datos.

#### ¿Qué es una tabla de Glue?

Metadatos que describen datos: nombres y tipos de las columnas, la ubicación en S3 (o un origen JDBC), el formato (SerDe y formatos de entrada y salida), las claves de partición y las propiedades de la tabla. Los datos se quedan en S3 o en la base de origen.

#### ¿Cómo se compara Glue con Amazon EMR?

Glue es serverless y está enfocado en ETL con Spark, con catálogo, bookmarks y calidad de datos integrados; cambias control por sencillez. EMR (sobre EC2, EKS o Serverless) da control total de Spark, Hadoop, Hive, Trino y otros frameworks, sus versiones y su ajuste, y suele ser más barato para cargas grandes y estables.

#### ¿Cómo se compara Glue con AWS Lambda para ETL?

Lambda sirve para transformaciones pequeñas disparadas por eventos (un archivo de pocos MB), con un límite de 15 minutos y memoria limitada. Glue sirve para procesamiento distribuido más grande con Spark, ejecuciones largas y grandes volúmenes.

#### ¿Qué es un DPU?

Una Data Processing Unit: 4 vCPU y 16 GB de memoria. Glue factura los jobs ETL, los crawlers y las sesiones interactivas en DPU-hora, por segundo.

#### ¿Cómo se factura un job de Glue?

Por DPU-hora, por segundo, con un mínimo de 1 minuto para los jobs Spark desde Glue 2.0. El costo es número de DPU × duración × precio por DPU-hora (unos 0,44 USD en muchas regiones, menos con Flex). Los jobs Python shell facturan 1/16 o 1 DPU.

#### ¿Qué son las versiones de Glue y por qué importan?

Cada versión de Glue empaqueta una versión de Spark, Python y Java y unos conectores: por ejemplo Glue 4.0 corre Spark 3.3 y Python 3.10, y Glue 5.0 corre Spark 3.5 y Python 3.11. Las versiones nuevas arrancan más rápido, corren más rápido y admiten formatos de tabla más nuevos. Las versiones viejas pierden soporte, así que actualizar es parte del mantenimiento.

#### ¿Qué es Glue Studio?

La experiencia de consola para crear, ejecutar y monitorear jobs de Glue: un editor visual en el que armas el ETL como un grafo de orígenes, transformaciones y destinos (que genera código PySpark), un editor de scripts, un editor de notebooks y dashboards de monitoreo de jobs.

#### ¿Qué es AWS Glue DataBrew?

Una herramienta visual de preparación de datos con más de 250 transformaciones integradas, usada por analistas para limpiar y normalizar datos sin código. Las transformaciones se guardan como recetas y se ejecutan como jobs sobre datos en S3, con perfilado de datos.

#### ¿Cómo encaja Glue en la arquitectura de data lake de AWS?

Los datos llegan a S3 (desde DMS, Kinesis, AppFlow, cargas manuales), los crawlers o los jobs los registran en el Data Catalog, los jobs de Glue los limpian y convierten en zonas curadas (Parquet o Iceberg), Lake Formation gobierna el acceso, y Athena, Redshift, EMR, QuickSight y SageMaker los consumen.

#### ¿Qué relación hay entre Glue y SageMaker Lakehouse/Unified Studio?

El Glue Data Catalog es la base de metadatos de SageMaker Lakehouse, y las funciones de integración de datos de Glue (jobs ETL, ETL visual, conexiones, zero-ETL) están disponibles dentro de SageMaker Unified Studio, el entorno unificado de AWS para datos, analítica e IA.

#### ¿Cuáles son los componentes principales de AWS Glue, en una frase cada uno?

El Data Catalog guarda los metadatos; los crawlers descubren esquemas; los jobs ETL transforman datos con Spark o Python; los triggers y workflows orquestan; Glue Studio ofrece creación visual; Data Quality valida los datos; DataBrew prepara datos de forma visual; el Schema Registry gobierna los esquemas de streaming.

#### ¿Qué es ETL frente a ELT en el contexto de Glue?

Con ETL, los jobs de Glue transforman los datos antes de cargarlos en el destino (por ejemplo, limpiar y convertir a Parquet antes de Redshift). Con ELT, los datos en bruto se cargan primero y se transforman dentro del destino (SQL de Redshift, dbt sobre Athena). Glue se usa a menudo para la "E" y la "L" del ELT, o como la "T" en un lakehouse.

#### ¿Qué cuotas de servicio de Glue conviene conocer?

Límites de ejecuciones concurrentes de jobs por cuenta, DPU máximos por job, número de jobs, triggers, crawlers, bases de datos, tablas y particiones por tabla. La mayoría se puede ampliar en Service Quotas; los data lakes grandes chocan primero con los límites de particiones y de concurrencia.

#### ¿En qué regiones está Glue y el catálogo es regional?

Glue está disponible en la mayoría de las regiones de AWS, y el Data Catalog es regional: cada región tiene su propio catálogo por cuenta. El acceso entre regiones requiere replicar los metadatos o usar resource links de Lake Formation.

#### ¿Qué es un development endpoint y qué lo reemplazó?

Un entorno heredado, siempre encendido, para desarrollar scripts de Glue desde notebooks, facturado mientras corría. Lo reemplazaron las sesiones interactivas y los notebooks de Glue Studio, bajo demanda, con facturación por segundo y timeouts de inactividad.

### Data Catalog

#### ¿Cómo llegan las tablas al Data Catalog?

Ejecutando crawlers, creando tablas a mano (consola, `CREATE EXTERNAL TABLE` en Athena, CloudFormation, Terraform, la API), desde jobs de Glue que crean o actualizan tablas al escribir (`enableUpdateCatalog`), o desde servicios como los blueprints de Lake Formation y las integraciones zero-ETL.

#### ¿Qué es una partición en el Data Catalog?

Un subconjunto de los datos de una tabla definido por valores de las claves de partición (por ejemplo `year=2026/month=10/day=15`), cada uno con su propia ubicación en S3. Los motores de consulta solo leen las particiones que cumplen los filtros, lo que reduce costo y tiempo.

#### ¿Cómo se registran las particiones nuevas?

Con un crawler, con `MSCK REPAIR TABLE` o `ALTER TABLE ADD PARTITION` en Athena, con la API `BatchCreatePartition`, con jobs de Glue que escriben actualizando el catálogo, o evitándolo por completo con la proyección de particiones de Athena.

#### ¿Qué son los índices de partición?

Índices sobre las claves de partición de las tablas del catálogo con muchas particiones, para que las llamadas `GetPartitions` con filtros respondan rápido en lugar de recorrer todas las particiones. Aceleran la planificación de consultas en Athena y Glue sobre tablas con decenas de miles de particiones.

#### ¿Qué son las estadísticas de columnas en el Data Catalog?

Estadísticas (número de valores distintos, nulos, mínimo/máximo, longitud media) que Glue calcula para las columnas de las tablas y guarda en el catálogo, y que Athena y Redshift Spectrum usan para la optimización basada en costos, como reordenar los joins.

#### ¿Qué es una conexión de Glue?

Un objeto del catálogo que guarda las propiedades de conexión a un almacén de datos: URL JDBC, credenciales (preferiblemente un secreto de Secrets Manager), VPC, subred y grupos de seguridad, o propiedades para Kafka, MongoDB, Snowflake, BigQuery y otros conectores nativos. Los jobs y crawlers la referencian.

#### ¿Qué formatos de tabla admite el Data Catalog?

Tablas al estilo Hive en Parquet, ORC, Avro, JSON, CSV y otros formatos, y los formatos de tabla abiertos Apache Iceberg, Apache Hudi y Delta Lake. Iceberg es el más integrado en los servicios de AWS.

#### ¿Qué son las optimizaciones del catálogo para tablas Iceberg?

Mantenimiento administrado de las tablas Iceberg del Data Catalog: compactación automática de archivos pequeños, retención de snapshots (expiración de los antiguos) y borrado de archivos huérfanos, configurado por tabla y ejecutado por Glue sin jobs propios.

#### ¿Pueden varias cuentas de AWS compartir un Data Catalog?

Sí. El acceso se puede conceder entre cuentas con políticas de recursos sobre el catálogo o, más a menudo, con permisos entre cuentas de Lake Formation (muchas veces mediante AWS RAM), de modo que una cuenta central de gobierno comparte bases de datos y tablas con las cuentas consumidoras.

#### ¿Qué es el catalog ID?

El ID de la cuenta de AWS dueña de un Data Catalog. Las APIs y las consultas pueden referenciar el catálogo de otra cuenta por su ID cuando se concedió acceso entre cuentas.

#### ¿Cómo se versionan los esquemas de las tablas en el Data Catalog?

El catálogo guarda versiones de una tabla automáticamente cuando se actualiza (hasta un límite), así que puedes ver y comparar esquemas anteriores con `GetTableVersions`. Las tablas Iceberg también guardan el historial del esquema en sus propios metadatos.

#### ¿Qué es el Glue Schema Registry?

Un servicio para guardar, versionar y validar esquemas (Avro, JSON Schema, Protobuf) de datos en streaming, con reglas de compatibilidad (backward, forward, full). Los productores y consumidores que usan Kafka, MSK, Kinesis o Lambda serializan y validan los registros con los esquemas registrados.

#### ¿Qué es un resource link?

Un objeto de Lake Formation que apunta a una base de datos o tabla compartida desde otra cuenta o región, para que los usuarios la consulten como si fuera local en su propio catálogo.

#### ¿Qué diferencia hay entre una tabla externa y una governed table?

En el Data Catalog todas las tablas basadas en S3 son externas (el catálogo solo guarda metadatos; borrar la tabla no borra los datos). Las governed tables eran un tipo de tabla de Lake Formation con transacciones ACID, hoy retiradas en favor de las tablas Apache Iceberg.

#### ¿Cómo se consulta el Data Catalog de forma programática?

Con la API de Glue (`GetDatabases`, `GetTables`, `GetPartitions`, `SearchTables`) mediante boto3 o la CLI, o con SQL a través de las vistas `information_schema` de Athena.

#### ¿Cómo se factura el Data Catalog?

El primer millón de objetos guardados y el primer millón de solicitudes al mes son gratis; después se paga por cada 100.000 objetos y por millón de solicitudes. El cálculo de estadísticas y las optimizaciones de Iceberg se facturan aparte en DPU-hora.

#### ¿Para qué sirven propiedades de tabla como `classification` y `compressionType`?

Indican a los motores y a Glue cómo interpretar los datos: `classification` (csv, json, parquet) la definen los crawlers y la usan los jobs de Glue, mientras que los parámetros del SerDe y la compresión le dicen a Athena o Hive cómo leer los archivos.

#### ¿Qué es una función definida por el usuario en el Data Catalog?

Metadatos de una UDF de Hive (nombre de clase y ubicación del JAR) guardados en el catálogo para que motores como Hive en EMR puedan usarla; importa sobre todo en cargas compatibles con Hive.

#### ¿Cómo se mantiene ordenado un Data Catalog?

Definiendo convenciones de nombres por capa (`raw_`, `curated_`), administrando las tablas como código, eliminando las tablas creadas por crawls accidentales, documentando tablas y columnas con descripciones, aplicando LF-Tags para clasificar y vigilando las tablas sin uso.

### Crawlers

#### ¿Qué es un crawler?

Un componente de Glue que se conecta a un almacén de datos (S3, bases JDBC, DynamoDB, MongoDB, Delta, Iceberg, Hudi), toma muestras de los datos, infiere esquemas y particiones con clasificadores, y crea o actualiza tablas en el Data Catalog. Puede ejecutarse bajo demanda o de forma programada.

#### ¿Qué es un clasificador?

La lógica que reconoce un formato de datos y su esquema. Glue trae clasificadores integrados (CSV, JSON, Parquet, Avro, ORC, XML, logs y más), y puedes añadir clasificadores propios con patrones grok, etiquetas XML, rutas JSON o ajustes de CSV.

#### ¿Cómo decide un crawler cuántas tablas crear?

Agrupa en una tabla los archivos con esquemas compatibles bajo un prefijo común, usando la estructura de carpetas para detectar particiones. Si los esquemas difieren demasiado, crea varias tablas. La opción "create a single schema for each S3 path" fuerza una tabla por ruta incluida.

#### ¿Qué es la política de cambios de esquema de un crawler?

Los ajustes de qué hacer cuando cambia el esquema o se borran objetos: actualizar la tabla o solo registrar los cambios, y borrar, marcar como obsoletas o ignorar las tablas y particiones eliminadas. Los equipos de producción suelen registrar los cambios en lugar de actualizar automáticamente, para evitar sorpresas.

#### ¿Qué son los crawls incrementales?

Ejecuciones que solo procesan las carpetas añadidas desde la última (y, con el modo de eventos de S3, solo los objetos modificados según una cola SQS), lo que es mucho más rápido y barato en data lakes grandes y en crecimiento.

#### ¿Qué es el modo de eventos de S3 para crawlers?

Un modo en el que el crawler lee notificaciones de eventos de S3 desde una cola SQS para saber exactamente qué objetos cambiaron, en lugar de listar todo el prefijo.

#### ¿Cuáles son los problemas comunes de los crawlers?

Demasiadas tablas creadas por esquemas o estructuras de carpetas incoherentes, tipos mal inferidos a partir de muestras de CSV, errores `HIVE_PARTITION_SCHEMA_MISMATCH` cuando las particiones tienen esquemas distintos, costo y tiempo sobre prefijos enormes, y cambios de esquema silenciosos que rompen las consultas posteriores.

#### ¿Hay que usar siempre crawlers?

No. Los crawlers son prácticos para descubrir datos y para orígenes que no controlas. En los pipelines propios, definir las tablas de forma explícita (infraestructura como código) y registrar las particiones desde los jobs, o usar proyección de particiones, da esquemas predecibles y ningún costo de crawler.

#### ¿Cómo se facturan los crawlers?

Por DPU-hora durante el tiempo que corren, por segundo con una duración mínima por ejecución. Recorrer millones de archivos pequeños puede salir caro; usa patrones de inclusión y exclusión, muestreo y crawls incrementales.

#### ¿Qué son los patrones de exclusión?

Patrones glob que le indican a un crawler qué archivos o carpetas saltar, como `**/_temporary/**`, `**.crc` o `**/_SUCCESS`, lo que evita tablas basura y ahorra tiempo.

#### ¿Puede un crawler recorrer una base de datos JDBC?

Sí. Con una conexión de Glue lee las definiciones de las tablas de bases como MySQL, PostgreSQL, Oracle y SQL Server con una ruta de inclusión como `mydb/%`, y crea tablas en el catálogo que los jobs pueden leer.

#### ¿Cómo infieren los crawlers los tipos en archivos CSV?

Tomando una muestra de las primeras filas y eligiendo tipos que encajen; si una columna tiene valores mezclados (números con algunos vacíos o textos), el crawler puede elegir `string`, o un tipo que las filas siguientes rompen. Define las tablas CSV de forma explícita para tener tipos predecibles.

#### ¿Cómo manejan los crawlers los encabezados de CSV?

El clasificador CSV integrado adivina si la primera fila es un encabezado comprobando si se ve distinta de las filas de datos. Cuando falla, un clasificador CSV propio con el encabezado explícito lo resuelve.

#### ¿Pueden los crawlers crear tablas Iceberg o Delta?

Sí. Los crawlers pueden registrar tablas Delta Lake, Iceberg y Hudi existentes en S3 leyendo sus metadatos y crear tablas del catálogo que apuntan al formato de tabla (de forma nativa o mediante manifiestos, según la configuración).

#### ¿Qué es la "recrawl policy"?

El ajuste que decide si en cada ejecución se recorren de nuevo todas las carpetas o solo las nuevas desde el último crawl (incremental), o si se usan eventos de S3.

#### ¿Cómo se limita el alcance de un crawler?

Con rutas de inclusión precisas, patrones de exclusión, un tamaño de muestra por carpeta (en S3), el ajuste de nivel de tabla (a qué profundidad de carpeta se crean las tablas) y crawlers separados por origen.

#### ¿Qué significa "table level" en la configuración del crawler?

La profundidad de carpeta a la que el crawler crea las tablas. Definirla evita que el crawler cree tablas en el nivel equivocado, por ejemplo tratando cada carpeta de partición como una tabla aparte.

### Jobs ETL de Glue

#### ¿Qué tipos de job ofrece Glue?

Jobs Spark (ETL batch con PySpark o Scala), jobs Spark streaming (procesamiento continuo desde Kinesis, Kafka o MSK) y jobs Python shell (scripts Python de un solo nodo para tareas pequeñas).

#### ¿Cómo es un job básico de Glue en PySpark?

```python
import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

args = getResolvedOptions(sys.argv, ["JOB_NAME", "target_path"])
glue = GlueContext(SparkContext.getOrCreate())
spark = glue.spark_session
job = Job(glue)
job.init(args["JOB_NAME"], args)

orders = glue.create_dynamic_frame.from_catalog(
    database="raw", table_name="orders", transformation_ctx="orders")
df = orders.toDF().filter("status = 'paid'")
df.write.mode("append").partitionBy("order_date").parquet(args["target_path"])

job.commit()
```

#### ¿Qué es `GlueContext`?

Un envoltorio del `SparkContext` que añade las funciones de Glue: leer y escribir DynamicFrames desde el catálogo, S3 y las conexiones, los job bookmarks y opciones propias de Glue.

#### ¿Qué hacen `job.init()` y `job.commit()`?

`init` inicia el estado del job, y `commit` guarda el estado de los job bookmarks al final de una ejecución exitosa. Sin `commit`, los bookmarks no avanzan y la siguiente ejecución vuelve a procesar los mismos datos.

#### ¿Cómo se pasan parámetros a un job de Glue?

Como argumentos del job (`--target_path s3://...`) definidos en el job o sobrescritos al iniciar la ejecución, leídos con `getResolvedOptions`. Algunos argumentos especiales configuran el propio Glue, como `--job-bookmark-option`, `--enable-metrics`, `--additional-python-modules` o `--conf`.

#### ¿Cómo se añaden librerías Python a un job de Glue?

Con `--additional-python-modules` (instala desde PyPI o wheels en S3 al arrancar), `--extra-py-files` (archivos zip o py en S3) o empaquetando las dependencias en un wheel. Para jobs sin acceso a internet, aloja los wheels en S3 o usa un repositorio privado mediante un endpoint de VPC.

#### ¿Cómo se añaden dependencias JAR?

Con `--extra-jars` apuntando a archivos JAR en S3, para drivers JDBC o librerías de Spark que no trae la versión de Glue.

#### ¿Para qué sirve un job Python shell?

Para tareas ligeras que no necesitan Spark: llamar a APIs, ejecutar SQL en Redshift o Athena, mover archivos pequeños, lanzar otros servicios. Corre en 1/16 o 1 DPU con Python y librerías comunes como pandas y boto3.

#### ¿Qué es la ejecución Flex de Glue?

Una clase de ejecución que corre sobre capacidad sobrante a un precio menor, con arranques posiblemente más largos y sin garantía de inicio inmediato. Sirve para cargas no urgentes como el batch nocturno, las pruebas y los backfills.

#### ¿Qué es el autoescalado de los jobs de Glue?

Con el autoescalado activado (Glue 3.0+), Glue añade y quita workers durante la ejecución según la carga, hasta el máximo que definas, para no pagar workers ociosos en las etapas con poco paralelismo.

#### ¿Qué son los timeouts y reintentos de un job?

`Timeout` detiene un job tras cierto número de minutos (48 horas por defecto en los jobs batch, lo cual es riesgoso; pon un valor realista). `MaxRetries` vuelve a ejecutar automáticamente los jobs fallidos; úsalo solo si el job es idempotente.

#### ¿Qué es la concurrencia máxima de un job?

El número de ejecuciones del mismo job permitidas a la vez (1 por defecto). Si una ejecución sigue activa, las nuevas peticiones de inicio fallan con `ConcurrentRunsExceededException` salvo que la aumentes.

#### ¿Cómo se escribe en Redshift desde un job de Glue?

Con una conexión de Redshift, escribiendo un DynamicFrame con `glue.write_dynamic_frame.from_jdbc_conf` (Glue deja los datos en S3 y ejecuta `COPY`), o con el conector de Spark para Redshift. `preactions` y `postactions` ejecutan SQL antes y después, por ejemplo para hacer `TRUNCATE` de una tabla de staging y luego `MERGE` en el destino.

#### ¿Cómo se lee una base JDBC en paralelo?

Con las opciones `hashfield`/`hashpartitions` de los DynamicFrames, o con `partitionColumn`, `lowerBound`, `upperBound` y `numPartitions` en el lector JDBC de Spark, para que varias tareas lean rangos a la vez en lugar de una sola conexión que lo lee todo.

#### ¿Pueden los jobs de Glue escribir tablas Iceberg, Hudi o Delta?

Sí. Define `--datalake-formats` como `iceberg`, `hudi` o `delta` (con la configuración de Spark correspondiente) y usa Spark SQL o las APIs de DataFrame, incluido `MERGE INTO`, con el Glue Data Catalog como catálogo.

```python
spark.sql("""
MERGE INTO glue_catalog.curated.customers t
USING updates s ON t.customer_id = s.customer_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
""")
```

#### ¿Para qué sirve el directorio temporal (`--TempDir`)?

Una ubicación de S3 donde Glue escribe datos intermedios, por ejemplo al cargar en Redshift o para el shuffle en algunas configuraciones. Debe tener una regla de ciclo de vida que borre los archivos viejos.

#### ¿Qué son las sesiones interactivas de Glue?

Sesiones Spark bajo demanda que usas desde notebooks Jupyter, los notebooks de Glue Studio o tu IDE para desarrollar y depurar código de Glue de forma interactiva, facturadas por segundo con un timeout de inactividad.

#### ¿Cómo se desarrollan jobs de Glue en local?

Con las imágenes Docker oficiales de Glue (que traen las librerías de Glue y el Spark de una versión dada), ejecutando scripts y pytest en local, o con sesiones interactivas desde un notebook local. La lógica PySpark pura también se puede probar con una SparkSession local.

#### ¿Qué diferencia hay entre el editor de scripts de Spark y el editor visual?

El editor visual arma los jobs como un grafo de nodos y genera el código; es rápido para el ETL estándar y accesible para analistas. El editor de scripts da control total sobre el código PySpark o Scala. Muchos equipos empiezan en visual y luego pasan al código administrado en Git.

#### ¿Cómo se usa Spark SQL dentro de un job de Glue?

Convirtiendo a DataFrame, registrando una vista temporal y ejecutando `spark.sql()`. Con el Data Catalog activado como Hive metastore (`--enable-glue-datacatalog`), puedes consultar directamente las tablas del catálogo por `base.tabla`.

#### ¿Qué hace `--enable-glue-datacatalog`?

Configura Spark en el job para usar el Glue Data Catalog como su Hive metastore, de modo que `spark.sql("SELECT * FROM raw.orders")` y `saveAsTable` funcionen sobre las tablas del catálogo.

#### ¿Cómo se lee JSON con estructuras anidadas en Glue?

Leyéndolo como DynamicFrame o DataFrame (con esquema inferido o declarado) y aplanándolo con `select` de los campos anidados, `explode` para los arreglos, o `Relationalize` de Glue para una salida totalmente relacional.

#### ¿Cómo se manejan los registros defectuosos al leer archivos?

En los lectores de Spark, con `mode` (`PERMISSIVE` con una columna de registros corruptos, `DROPMALFORMED`, `FAILFAST`) o `badRecordsPath` donde se admite; en los DynamicFrames, los errores se capturan por registro y se pueden revisar con `errorsAsDynamicFrame()`, con umbrales definidos por `stageThreshold` y `totalThreshold`.

#### ¿Cómo se escribe la salida con un número controlado de archivos?

Con repartition o coalesce antes de escribir (`df.repartition(20, "order_date")`), o con `spark.sql.files.maxRecordsPerFile`, para que cada partición tenga unos pocos archivos grandes en lugar de cientos de pequeños.

#### ¿Para qué sirve el ID de ejecución de un job de Glue?

Identifica una ejecución para el monitoreo, los logs, el retroceso de bookmarks y los reintentos, y se puede pasar a las salidas (por ejemplo como columna) para el linaje.

#### ¿Cómo se lee DynamoDB en Glue?

Con el conector de DynamoDB: directamente (consume capacidad de lectura, controlada con `dynamodb.throughput.read.percent`) o mediante la exportación de DynamoDB a S3 (`dynamodb.export`), que no consume capacidad de la tabla y es preferible para tablas grandes.

#### ¿Cómo se conectan los jobs de Glue a Snowflake, BigQuery u otros orígenes fuera de AWS?

Con los conectores nativos de Glue para muchos orígenes (Snowflake, BigQuery, Teradata, SAP HANA, MongoDB y aplicaciones SaaS), con conectores del AWS Marketplace o por JDBC con un driver propio y una conexión de Glue.

#### ¿Cuáles son los estados de ejecución de un job?

`STARTING`, `RUNNING`, `STOPPING`, `STOPPED`, `SUCCEEDED`, `FAILED`, `TIMEOUT`, `ERROR` y `WAITING`. EventBridge recibe los eventos de cambio de estado para alertas y orquestación.

#### ¿Qué pasa con los logs de un job de Glue?

Los logs del driver y de los executors van a CloudWatch Logs (`/aws-glue/jobs/output` y `/aws-glue/jobs/error`); el logging continuo los envía durante la ejecución. Usa `glue.get_logger()` para mensajes estructurados.

### DynamicFrames y transformaciones

#### ¿Qué es un DynamicFrame?

La estructura de datos distribuida de Glue, parecida a un DataFrame de Spark pero en la que cada registro se describe a sí mismo, así que no necesita un esquema fijo de antemano. Maneja datos inconsistentes y desordenados (un campo que a veces es texto y a veces entero) con tipos "choice".

#### ¿Qué diferencia hay entre un DynamicFrame y un DataFrame?

Un DataFrame tiene un esquema para todo el conjunto y todo el optimizador y la API de Spark SQL. Un DynamicFrame calcula el esquema por registro, admite tipos choice y transformaciones propias de Glue, bookmarks e integración con el catálogo. Se convierte con `toDF()` y `DynamicFrame.fromDF()`, y la mayoría de los equipos usa DataFrames para transformar.

#### ¿Qué es un tipo choice y cómo funciona `ResolveChoice`?

Cuando una columna tiene valores de tipos distintos, un DynamicFrame guarda un tipo choice (por ejemplo `choice<int,string>`). `ResolveChoice` lo resuelve con `cast:long`, `make_cols` (divide en `col_int` y `col_string`), `make_struct` o `project:string`.

```python
resolved = dyf.resolveChoice(specs=[("amount", "cast:double"), ("id", "cast:long")])
```

#### ¿Qué hace `ApplyMapping`?

Renombra columnas, convierte tipos y selecciona campos en un solo paso, a partir de una lista de tuplas `(origen, tipo_origen, destino, tipo_destino)`, que es como funciona el nodo de mapeo de Glue Studio.

#### ¿Qué hace `Relationalize`?

Aplana JSON anidado en un conjunto de tablas relacionales: las estructuras anidadas pasan a columnas y los arreglos a tablas aparte enlazadas por claves generadas, listas para cargar en una base relacional.

#### ¿Qué otras transformaciones integradas tiene Glue?

`DropFields`, `SelectFields`, `RenameField`, `Filter`, `Map`, `Join`, `SplitFields`, `SplitRows`, `Unbox` (interpretar cadenas JSON), `DropNullFields`, `FillMissingValues`, `FindMatches` (deduplicación con ML) y, en Glue Studio, transformaciones como `Aggregate`, `Pivot`, `Derived column`, `Identify sensitive data` y `Evaluate data quality`.

#### ¿Qué es FindMatches?

Una transformación de machine learning que identifica registros duplicados o coincidentes que no comparten una clave común (por ejemplo el mismo cliente escrito de formas distintas), entrenada con ejemplos etiquetados.

#### ¿Por qué muchos equipos convierten pronto los DynamicFrames a DataFrames?

Los DataFrames tienen una API más rica, el optimizador Catalyst, mejor rendimiento en la mayoría de las transformaciones y son portables a otros entornos Spark. Los DynamicFrames son útiles sobre todo al leer (catálogo, bookmarks, resolución de choices) y al escribir (actualización del catálogo, conectores).

#### ¿Cómo se escribe un DynamicFrame actualizando el catálogo?

```python
sink = glue.getSink(connection_type="s3", path="s3://lake/curated/orders/",
                    enableUpdateCatalog=True, updateBehavior="UPDATE_IN_DATABASE",
                    partitionKeys=["order_date"])
sink.setFormat("glueparquet")
sink.setCatalogInfo(catalogDatabase="curated", catalogTableName="orders")
sink.writeFrame(dyf)
```

#### ¿Qué es el formato `glueparquet`?

Un escritor de Parquet optimizado por Glue para DynamicFrames que calcula el esquema mientras escribe, evitando una pasada extra sobre los datos, lo que acelera la escritura de conjuntos grandes.

#### ¿Qué es `transformation_ctx`?

Un nombre único para cada origen y transformación de un job, que los job bookmarks usan para guardar el estado. Sin él en un origen, los bookmarks no funcionan para ese origen.

#### ¿Cómo se filtra un DynamicFrame?

Con `Filter.apply(frame=dyf, f=lambda row: row["status"] == "paid")` o `dyf.filter(...)`, aunque convertir a DataFrame y usar `filter("status = 'paid'")` suele ser más rápido porque Spark lo puede optimizar.

#### ¿Cómo se unen DynamicFrames?

Con `Join.apply(dyf1, dyf2, "key1", "key2")`, que hace un join por igualdad; para otros tipos de join o condiciones, convierte a DataFrames.

#### ¿Qué hace `Unbox`?

Interpreta una columna de texto que contiene JSON (o CSV) como una estructura, para que los campos anidados sean columnas accesibles.

#### ¿Qué hace `SplitFields`?

Divide un DynamicFrame en dos colecciones por columnas, por ejemplo para separar las columnas con datos personales del resto y escribirlas en ubicaciones distintas.

#### ¿Cómo se deduplica en un job de Glue?

Convirtiendo a DataFrame y usando `dropDuplicates(["key"])` o una función de ventana con `row_number()` ordenada por una marca de actualización, quedándose con el registro más reciente por clave.

#### ¿Cómo se añaden columnas de auditoría en un job de Glue?

Añadiendo columnas como `ingested_at` (`current_timestamp()`), `source_file` (`input_file_name()` o los metadatos del archivo), `job_run_id` y `process_date`, para que cada fila se pueda rastrear hasta la ejecución y el archivo que la produjeron.

### Job bookmarks y procesamiento incremental

#### ¿Qué son los job bookmarks?

Una función de Glue que guarda estado entre ejecuciones para que cada una procese solo los datos nuevos: en orígenes S3, qué archivos (por fecha de modificación) se procesaron; en orígenes JDBC, los valores más altos de las columnas clave del bookmark.

#### ¿Cómo se activan y controlan los job bookmarks?

Con `--job-bookmark-option`: `job-bookmark-enable`, `job-bookmark-disable` o `job-bookmark-pause` (procesa desde el último bookmark sin actualizarlo). El origen necesita un `transformation_ctx` y el script debe llamar a `job.commit()`.

#### ¿Cómo se reinicia o se retrocede un bookmark?

Con la consola o la API `ResetJobBookmark`, que hace que la siguiente ejecución lo reprocese todo; también se puede retroceder al ID de una ejecución anterior para reprocesar desde ese punto.

#### ¿Cuáles son los límites de los job bookmarks?

Siguen los archivos por fecha de modificación, así que los archivos sobrescritos con el mismo nombre pueden perderse o reprocesarse; los bookmarks JDBC necesitan columnas clave que siempre crecen y no ven las actualizaciones de filas viejas; solo funcionan con ciertos orígenes y formatos; y no hacen idempotentes las escrituras, así que un fallo después de escribir y antes del `commit` reprocesa datos.

#### ¿Cómo se hace idempotente un job de Glue?

Escribiendo la salida de la partición procesada con sobrescritura (sobrescritura dinámica de particiones) o usando `MERGE` sobre una tabla Iceberg, en lugar de añadir a ciegas; tomando el periodo procesado de un parámetro; y usando los bookmarks como optimización, no como única garantía.

#### ¿Qué es el pushdown predicate en Glue?

Un filtro sobre las columnas de partición que se pasa al leer desde el catálogo (`push_down_predicate="order_date >= '2026-10-01'"`) para que Glue liste y lea solo las particiones que coinciden en lugar de toda la tabla.

#### ¿Qué es `catalogPartitionPredicate`?

Un filtro de particiones del lado del servidor que evalúa el Data Catalog con los índices de partición, lo que reduce el número de particiones que Glue tiene que traer del catálogo en tablas con muchísimas particiones. Se puede combinar con `push_down_predicate`.

#### ¿Cómo procesas solo los datos de ayer sin bookmarks?

Paso la fecha como argumento del job (desde el orquestador), leo con un pushdown predicate sobre la partición de fecha y sobrescribo la partición de salida de esa fecha. Es explícito, reproducible y facilita los backfills.

#### ¿Funcionan los job bookmarks con tablas Iceberg como origen?

No de la misma forma; para orígenes Iceberg se procesa de forma incremental con las funciones propias de Iceberg, como leer los cambios entre snapshots (lecturas incrementales o vistas de changelog) y guardar el ID del último snapshot procesado.

#### ¿Qué pasa con los bookmarks si un job falla?

Los bookmarks solo se actualizan con `job.commit()` tras un éxito, así que una ejecución fallida deja el bookmark donde estaba y la siguiente vuelve a procesar los mismos datos. Por eso las escrituras deben ser idempotentes.

#### ¿Pueden dos jobs distintos compartir un bookmark?

No. Los bookmarks son por job (y por `transformation_ctx`). Dos jobs que leen el mismo origen mantienen estados independientes.

#### ¿Cómo funcionan los bookmarks JDBC?

Defines `jobBookmarkKeys` (columnas como un ID creciente o `updated_at`) y un orden; el job lee las filas con valores mayores al último máximo guardado. Las actualizaciones de filas con claves viejas se pierden, así que encaja con tablas de solo inserción o marcas de tiempo monótonas.

### Workers, rendimiento y costos

#### ¿Qué tipos de worker ofrece Glue?

G.1X (1 DPU: 4 vCPU, 16 GB), G.2X (2 DPU), G.4X (4 DPU), G.8X (8 DPU) y tipos más grandes en las versiones recientes, G.025X (0,25 DPU, para streaming de poco volumen) y los tipos R optimizados para memoria. Los workers más grandes sirven para transformaciones que usan mucha memoria; más workers sirven para el trabajo en paralelo.

#### ¿Cómo se elige el número de workers?

Partiendo del volumen y la complejidad de los datos, activando el autoescalado con un máximo razonable y mirando las métricas del job: si los executors están ociosos, reduce; si los stages derraman o las tareas hacen cola, aumenta o usa workers más grandes. Mide el costo por ejecución.

#### ¿Cómo se diagnostica un job de Glue lento?

Activando las métricas del job, las métricas de observabilidad y la Spark UI (event logs en S3), y revisando la duración de los stages, las tareas con skew, el tamaño de los shuffles y el spill, el uso de los executors y el número de archivos de entrada. Job run insights señala la línea que falla y las causas comunes.

#### ¿Qué es el problema de los archivos pequeños en Glue y cómo se maneja?

Leer muchos archivos pequeños crea muchas tareas y solicitudes a S3 y ralentiza los jobs. Glue puede agrupar archivos al leer (`groupFiles: inPartition`, `groupSize`), y conviene escribir menos archivos y más grandes (repartition antes de escribir, entre 128 MB y 1 GB por archivo) o compactar las tablas Iceberg.

```python
dyf = glue.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://lake/raw/clicks/"], "recurse": True,
                        "groupFiles": "inPartition", "groupSize": "134217728"},
    format="json")
```

#### ¿Por qué convertir CSV o JSON en bruto a Parquet?

Parquet es columnar y comprimido: Athena, Redshift Spectrum y Spark leen solo las columnas necesarias, saltan grupos de filas con las estadísticas y escanean muchos menos datos, lo que reduce el tiempo y el costo.

#### ¿Cómo se maneja el data skew en un job de Glue?

Igual que en Spark: apoyándose en Adaptive Query Execution (activada en las versiones recientes de Glue), haciendo broadcast de las tablas pequeñas, aislando o aplicando salting a las claves calientes y revisando en la Spark UI las tareas rezagadas.

#### ¿Cómo se reducen los costos de Glue?

Usando la última versión de Glue (arranque y ejecución más rápidos), activando el autoescalado, usando Flex para los jobs no urgentes, dimensionando bien los workers, definiendo timeouts, procesando de forma incremental con particiones o bookmarks, leyendo solo las particiones y columnas necesarias, evitando los crawlers cuando las tablas se pueden definir en código y apagando los endpoints de desarrollo y las sesiones ociosas.

#### ¿Qué es la Spark UI de Glue?

Una vista del Spark history server sobre los event logs de una ejecución (activada con `--enable-spark-ui` y una ruta de logs en S3), disponible en la consola de Glue, para analizar stages, tareas, almacenamiento y planes SQL.

#### ¿Qué son las métricas de observabilidad de Glue?

Métricas de CloudWatch a nivel de job, stage y executor (CPU, memoria, disco, shuffle, skew, uso de workers, rendimiento) que ayudan a detectar cuellos de botella y dimensionar los jobs.

#### ¿Qué requiere `--enable-auto-scaling`?

Glue 3.0 o posterior, un número máximo de workers y una carga que varíe entre stages. Glue ajusta entonces los executors según las tareas pendientes.

#### ¿Qué es la opción de shuffle en S3 de Glue?

Una opción (`--write-shuffle-files-to-s3`) que escribe los datos del shuffle de Spark en S3 en lugar del disco local, evitando fallos de "no space left on device" en jobs con mucho shuffle, a costa de algo de velocidad.

#### ¿Cuándo conviene usar workers G.2X o más grandes en lugar de más workers G.1X?

Cuando los executors se quedan sin memoria (joins grandes, filas anchas, agregaciones grandes, transformaciones de ML) o derraman mucho. Si las tareas son pequeñas y numerosas, más workers pequeños dan el mismo paralelismo al mismo precio.

#### ¿Qué son los workers de tipo R (optimizados para memoria)?

Tipos de worker con más memoria por CPU, para jobs limitados por la memoria más que por la CPU, como los broadcast joins grandes o el uso de caché.

#### ¿Cómo se estima el costo de un job de Glue?

Workers × DPU por worker × duración en horas × precio por DPU-hora. Por ejemplo, 10 workers G.1X durante 15 minutos son 10 × 1 × 0,25 = 2,5 DPU-hora, alrededor de 1,10 USD a 0,44 USD por DPU-hora. Con autoescalado, revisa los DPU-segundos reales en los detalles de la ejecución.

#### ¿Por qué los jobs de Glue tardan en arrancar y cómo se reduce?

Glue aprovisiona el entorno en cada ejecución. Desde Glue 2.0 el arranque toma de segundos a un minuto; Flex puede tardar más. Se reduce con versiones más nuevas, menos módulos extra instalados al arrancar (wheels preconstruidos) y evitando muchos jobs diminutos que podrían ser uno.

#### ¿Cómo ayuda la Adaptive Query Execution de Spark en Glue?

Activada por defecto desde Glue 4.0, fusiona las particiones pequeñas del shuffle, convierte los joins a broadcast cuando un lado es pequeño y divide las particiones con skew, lo que mejora el rendimiento sin ajustes manuales.

#### ¿Cómo se pasa configuración de Spark a un job de Glue?

Con el parámetro `--conf` (por ejemplo `--conf spark.sql.shuffle.partitions=400`), teniendo en cuenta que Glue administra algunos ajustes que no se pueden cambiar.

#### ¿Qué hace eficientes a los archivos Parquet para las consultas posteriores?

La organización columnar, la compresión (Snappy o ZSTD), las estadísticas por grupo de filas para saltarlas, tamaños de archivo razonables (cientos de MB) y el orden o particionado por las columnas de filtro habituales.

#### ¿Cómo afecta la estrategia de particionado a Glue y Athena?

Particiona por las columnas usadas en la mayoría de los filtros (normalmente la fecha), con un número moderado de particiones que tengan datos suficientes cada una; demasiado fino (por hora y cliente) crea millones de particiones diminutas y una planificación lenta, demasiado grueso obliga a lecturas grandes.

### ETL en streaming

#### ¿Qué son los jobs de streaming de Glue?

Jobs de Spark Structured Streaming de larga duración que leen de Kinesis Data Streams, Amazon MSK o Kafka autoadministrado, transforman los registros en micro-lotes y escriben en S3, formatos de data lake, bases de datos u otros flujos.

#### ¿Cómo maneja los esquemas un job de streaming de Glue?

Desde una tabla del Data Catalog que describe el flujo, desde el Glue Schema Registry o infiriendo el esquema a partir de los datos. Los registros que no encajan se pueden manejar con tipos choice o enviar a una ruta de errores.

#### ¿Qué es el tamaño de ventana en el streaming de Glue?

El intervalo de cada micro-lote (`windowSize`, por ejemplo 100 segundos) en `forEachBatch`. Las ventanas más grandes reducen los archivos pequeños y la sobrecarga; las más pequeñas reducen la latencia.

#### ¿Dónde guarda su avance un job de streaming?

En una ubicación de checkpoint en S3, que guarda los offsets y el estado para que el job continúe donde se detuvo tras un reinicio o una actualización.

#### ¿Cuándo elegirías el streaming de Glue frente a Kinesis Data Firehose o Managed Service for Apache Flink?

Firehose para una entrega sencilla a S3, Redshift u OpenSearch con poca transformación y sin código. Managed Flink para procesamiento de flujos con estado y baja latencia, con lógica compleja por tiempo del evento. El streaming de Glue cuando el equipo ya usa Spark, necesita ETL en micro-lotes hacia un data lake y quiere compartir código con los jobs batch.

#### ¿Cómo se evitan los archivos pequeños en los jobs de streaming?

Usando ventanas más grandes, escribiendo en tablas Iceberg o Hudi y compactándolas (o apoyándose en la compactación del catálogo para Iceberg), o ejecutando un job de compactación aparte.

#### ¿Qué orígenes puede leer el streaming de Glue?

Amazon Kinesis Data Streams, Amazon MSK, Apache Kafka autoadministrado y (con conectores) otros sistemas de streaming. Las salidas incluyen S3, tablas Iceberg/Hudi/Delta, bases JDBC y otros flujos.

#### ¿Cómo se facturan los jobs de streaming de Glue?

Por DPU-hora mientras corren, que es todo el tiempo; los workers G.025X reducen el costo en flujos de poco volumen. El autoescalado ayuda con tráfico variable.

#### ¿Cómo se actualiza el código de un job de streaming en marcha?

Se detiene el job y se inicia la versión nueva con la misma ubicación de checkpoint, siempre que los cambios sean compatibles con el estado guardado; los cambios incompatibles necesitan un checkpoint nuevo y un plan para reprocesar u omitir datos.

#### ¿Cómo se manejan los eventos tardíos en el streaming de Glue?

Con ventanas por tiempo del evento y watermarks de Spark Structured Streaming para las agregaciones, o escribiendo los eventos en particiones por fecha del evento y dejando que los jobs posteriores reprocesen las particiones recientes.

### Calidad de datos y datos sensibles

#### ¿Qué es AWS Glue Data Quality?

Una función basada en la librería de código abierto Deequ para medir y monitorear la calidad de los datos con reglas escritas en DQDL (Data Quality Definition Language), que se ejecutan en jobs de Glue o sobre tablas del catálogo, con recomendaciones, puntajes, detección de anomalías y alertas.

#### ¿Cómo es un conjunto de reglas DQDL?

```
Rules = [
    RowCount > 1000,
    IsComplete "order_id",
    IsUnique "order_id",
    ColumnValues "status" in ["paid", "refunded", "cancelled"],
    ColumnValues "amount" >= 0,
    Freshness "updated_at" <= 24 hours
]
```

#### ¿Cómo se actúa sobre los resultados de calidad en un job?

Usando la transformación Evaluate Data Quality y luego enrutando las filas: conservar las que pasan, escribir las que fallan en una ubicación de cuarentena, y hacer fallar el job o enviar una alerta por EventBridge cuando el puntaje total baja de un umbral.

#### ¿Qué es la detección de anomalías de calidad de datos?

Glue aprende estadísticas a lo largo de las ejecuciones (número de filas, valores distintos, distribuciones) y señala valores inusuales incluso sin umbrales explícitos, lo que detecta problemas como una caída repentina del volumen.

#### ¿Qué es la detección de datos sensibles en Glue?

Una transformación que busca datos personales como nombres, correos, teléfonos, tarjetas de crédito y documentos de identidad (con detectores por país), y puede ocultar, hashear o informar los hallazgos, lo que ayuda a cumplir el RGPD o leyes similares, como la ley de protección de datos personales de Colombia.

#### ¿Cómo recibes alertas de fallos de calidad de datos?

Glue publica los resultados de calidad en EventBridge y CloudWatch; las reglas pueden enviar notificaciones por SNS o lanzar flujos de corrección.

#### ¿Cómo se obtienen recomendaciones de reglas en Glue Data Quality?

Ejecutando una tarea de recomendación sobre una tabla del catálogo: Glue perfila los datos y propone reglas DQDL (completitud, unicidad, rangos de valores, valores permitidos) que revisas y editas antes de usarlas.

#### ¿Qué son las reglas compuestas en DQDL?

Reglas combinadas con `and` y `or`, por ejemplo `(ColumnValues "status" = "paid") and (ColumnValues "amount" > 0)`, para expresar condiciones sobre varias columnas.

#### ¿Dónde se guardan los resultados de calidad de datos?

En el historial de la consola de Glue, en métricas de CloudWatch, como eventos de EventBridge y, opcionalmente, escritos en S3 por el job, donde se pueden consultar con Athena para ver tendencias.

#### ¿Cómo se comprueba la integridad referencial en Glue Data Quality?

Con reglas como `ReferentialIntegrity`, que compara una columna con la columna clave de otro dataset, o `DatasetMatch` para comparar dos datasets, pasando el dataset de referencia como origen adicional.

### Orquestación

#### ¿Qué son los triggers de Glue?

Objetos que inician jobs y crawlers: programados (cron), condicionales (cuando otros jobs o crawlers llegan a un estado como `SUCCEEDED`), bajo demanda o basados en eventos de EventBridge (por ejemplo lotes de eventos de S3).

#### ¿Qué es un workflow de Glue?

Un contenedor para un grafo de triggers, crawlers y jobs que representa un pipeline ETL, con una vista visual de las ejecuciones, propiedades de ejecución compartidas (parámetros clave-valor) y la posibilidad de retomar desde un paso fallido.

#### ¿Cuándo usarías Step Functions o Airflow en lugar de los workflows de Glue?

Cuando el pipeline involucra muchos servicios de AWS (Lambda, EMR, Athena, SageMaker), necesita ramificaciones complejas, reintentos y manejo de errores, o abarca otros sistemas. Step Functions se integra de forma nativa con Glue (`startJobRun.sync`); Airflow (o MWAA) tiene operadores para Glue.

#### ¿Cómo se lanza un job de Glue cuando llega un archivo a S3?

Con una regla de EventBridge sobre los eventos "Object Created" de S3 que apunta a un workflow de Glue (con agrupación por número de eventos o ventana de tiempo), con notificaciones de S3 hacia una Lambda que llama a `StartJobRun`, o con una regla de EventBridge que inicia una máquina de estados de Step Functions.

#### ¿Cómo se inicia un job de Glue desde Step Functions y se espera a que termine?

```json
{
  "Type": "Task",
  "Resource": "arn:aws:states:::glue:startJobRun.sync",
  "Parameters": {
    "JobName": "curate-orders",
    "Arguments": { "--process_date.$": "$.date" }
  },
  "Retry": [{ "ErrorEquals": ["States.ALL"], "MaxAttempts": 2, "BackoffRate": 2 }],
  "Next": "RunAthenaChecks"
}
```

#### ¿Qué son las propiedades de ejecución de un workflow?

Pares clave-valor compartidos por todos los jobs de una ejecución del workflow, leídos y actualizados con `get_workflow_run_properties` y `put_workflow_run_properties`, para pasar valores como una fecha de procesamiento entre pasos.

#### ¿Qué es el predicado de un trigger condicional?

La lista de jobs o crawlers y estados que vigila, con lógica `AND` (todas las condiciones) o `ANY` (una condición), por ejemplo "iniciar el job B cuando el job A y el crawler C hayan terminado bien".

#### ¿Puede EventBridge iniciar directamente un job de Glue?

EventBridge puede apuntar de forma nativa a workflows de Glue; para un job suelto, el patrón común es EventBridge hacia Step Functions o hacia una Lambda que llama a `StartJobRun`.

#### ¿Cómo se retoma un workflow fallido?

En la consola o la API de Glue (`ResumeWorkflowRun`), seleccionando los nodos fallidos para volver a ejecutarlos tras corregir el problema; los nodos completados no se vuelven a ejecutar.

#### ¿Cómo se pasa la fecha de procesamiento desde un orquestador a un job de Glue?

Como argumento del job en `StartJobRun` (`--process_date=2026-10-16`), calculado por el orquestador a partir de la fecha lógica de la programación, nunca del reloj del propio job.

### Seguridad y gobierno

#### ¿Qué permisos de IAM necesita un job de Glue?

Un job corre con un rol IAM que Glue asume. Necesita los permisos de `AWSGlueServiceRole` (o equivalentes), acceso a las rutas de S3 que lee y escribe, a la ubicación del script, al directorio temporal, a las claves KMS, a los secretos de Secrets Manager de las conexiones y a CloudWatch Logs.

#### ¿Cómo funciona Lake Formation con Glue?

Lake Formation añade permisos detallados (a nivel de base de datos, tabla, columna, fila y celda, y control de acceso por etiquetas con LF-Tags) sobre el Data Catalog. Servicios como Athena, Redshift Spectrum, EMR y Glue (5.0+) aplican esos permisos al leer los datos.

#### ¿Qué son las LF-Tags?

Etiquetas de Lake Formation (pares clave-valor como `domain=sales`, `classification=pii`) asociadas a bases de datos, tablas y columnas; los permisos se conceden sobre expresiones de etiquetas, lo que escala mejor que conceder tabla por tabla.

#### ¿Cómo acceden los jobs de Glue a bases de datos dentro de una VPC?

Mediante una conexión de Glue con VPC, subred y grupos de seguridad: Glue crea interfaces de red elásticas en la subred. La subred necesita rutas hacia la base y, para acceder a S3, un endpoint de gateway de S3 (o un NAT para internet).

#### ¿Cómo se cifran los datos con Glue?

Con configuraciones de seguridad que activan el cifrado de la salida a S3 (SSE-S3 o SSE-KMS), de CloudWatch Logs y de los job bookmarks; el cifrado del catálogo con KMS; y las contraseñas de las conexiones guardadas en Secrets Manager o cifradas en el catálogo.

#### ¿Cómo se evita poner credenciales en el código de los scripts de Glue?

Guardando las credenciales en AWS Secrets Manager y referenciando el secreto en la conexión de Glue, o leyéndolo en el script con boto3; y usando roles IAM para los recursos de AWS.

#### ¿Cómo se audita la actividad de Glue?

CloudTrail registra las llamadas a la API de Glue (cambios de jobs y del catálogo), CloudWatch Logs guarda la salida de los jobs, Lake Formation ofrece registros de auditoría del acceso a los datos y AWS Config puede seguir la configuración de los recursos.

#### ¿Qué es una configuración de seguridad de Glue?

Un conjunto con nombre de ajustes de cifrado (modo de cifrado de S3 y clave KMS, cifrado de CloudWatch Logs, cifrado de los job bookmarks) que se asocia a jobs, crawlers y endpoints de desarrollo.

#### ¿Cómo se restringe un job de Glue a prefijos concretos de S3?

Dándole a su rol IAM una política que solo permita los prefijos de bucket y las claves KMS necesarios y, con Lake Formation, concediendo solo las tablas necesarias; evita permisos amplios como `s3:*`.

#### ¿Cómo se impide que los jobs de Glue salgan a internet?

Ejecutándolos con una conexión de VPC en subredes privadas sin NAT gateway, usando endpoints de VPC para S3, Glue, CloudWatch, KMS y Secrets Manager, y alojando las dependencias Python en S3 o en un repositorio privado.

#### ¿Qué es el control de acceso detallado para los jobs Spark de Glue?

Con Glue 5.0 y Lake Formation, los jobs Spark pueden aplicar los permisos a nivel de tabla, columna, fila y celda definidos en Lake Formation, para que el rol del job solo vea los datos permitidos.

### Operación, CI/CD e integración

#### ¿Cómo se despliegan los jobs de Glue como código?

Guardando los scripts y las definiciones de los jobs en Git y desplegándolos con CloudFormation, CDK, Terraform o SAM: se suben los scripts a S3 y se crean los jobs, triggers, crawlers, conexiones y tablas del catálogo. Un pipeline de CI ejecuta las pruebas, empaqueta las librerías como wheels y despliega en cada entorno.

#### ¿Cómo se prueba la lógica de los jobs de Glue?

Poniendo la lógica de transformación en funciones que reciben y devuelven DataFrames, probándolas con pytest sobre una SparkSession local o la imagen Docker de Glue, probando el job de extremo a extremo con datos de muestra en una cuenta de desarrollo y añadiendo reglas de calidad de datos para los controles en ejecución.

#### ¿Cómo se monitorean los jobs de Glue en producción?

Con métricas y alarmas de CloudWatch (fallos de jobs, duración, uso de DPU), eventos de EventBridge sobre los cambios de estado enviados a SNS o Slack, job run insights para los errores, y dashboards de duración y costo de los jobs en el tiempo.

#### ¿Cómo se manejan los fallos de los jobs?

Con reintentos para los errores transitorios (solo con jobs idempotentes), alertas sobre los estados `FAILED` y `TIMEOUT`, un procedimiento de reejecución con parámetros para el periodo fallido y rutas de cuarentena o dead-letter para los datos defectuosos.

#### ¿Qué es zero-ETL en el contexto de Glue?

Integraciones administradas que replican datos desde orígenes (aplicaciones SaaS como Salesforce, SAP o ServiceNow, y bases de datos de AWS como DynamoDB) hacia destinos como tablas de SageMaker Lakehouse o Redshift sin construir pipelines ETL, manteniéndolos sincronizados.

#### ¿Qué es Amazon Q data integration en Glue?

Un asistente de IA generativa que crea jobs y transformaciones ETL de Glue a partir de descripciones en lenguaje natural y ayuda a diagnosticar jobs; también existe la actualización asistida por IA de scripts Spark a versiones más nuevas de Glue.

#### ¿Cómo trabajan juntos Glue y Athena?

Glue cataloga y transforma los datos; Athena consulta con SQL las tablas del catálogo. Los jobs de Glue suelen convertir los datos en bruto a Parquet o Iceberg particionado para que las consultas de Athena sean rápidas y baratas.

#### ¿Cómo trabajan juntos Glue y AWS DMS?

DMS replica bases de datos (carga completa y CDC) en S3 como archivos con indicadores de operación; luego los jobs de Glue aplican los cambios a las tablas curadas, típicamente con `MERGE` sobre tablas Iceberg o Hudi.

#### ¿Cómo se actualiza un job de Glue a una versión más nueva?

Cambiando la versión de Glue en una copia de desarrollo, ejecutando las pruebas y comparando salidas y duraciones, revisando las notas de migración (cambios de Spark, Python y librerías), verificando conectores y JAR, y promoviéndolo con CI.

#### ¿Cómo se estructura el repositorio de un proyecto de Glue?

Separando los scripts de entrada de los jobs, un paquete Python compartido con la lógica de transformación (construido como wheel), las pruebas, la infraestructura como código (CDK, Terraform o CloudFormation), los conjuntos de reglas de calidad y la configuración por entorno.

#### ¿Cómo se versionan los scripts de Glue?

Guardándolos en Git y desplegando copias versionadas en S3 (por ejemplo con el SHA del commit en la ruta), para que cada definición de job apunte a una versión conocida del script y revertir sea volver a apuntar a la anterior.

#### ¿Cómo se generan alertas sobre jobs de Glue que tardan demasiado?

Definiendo el timeout del job, añadiendo una alarma de CloudWatch sobre el tiempo transcurrido o la métrica `glue.driver.aggregate.elapsedTime`, o haciendo que el orquestador alerte cuando un paso supera su duración esperada.

#### ¿Cómo se comparten tablas de Glue con Amazon Redshift?

Creando en Redshift un esquema externo que apunte a una base de Glue (`CREATE EXTERNAL SCHEMA ... FROM DATA CATALOG`) y consultando las tablas con Redshift Spectrum, o usando el acceso al Data Catalog montado automáticamente en Redshift.

#### ¿Cómo usa EMR el Glue Data Catalog?

Los clusters de EMR y EMR Serverless se pueden configurar para usar el Glue Data Catalog como su Hive metastore, de modo que Spark, Hive, Presto y Trino en EMR comparten las mismas definiciones de tablas que Athena y Glue.

#### ¿Para qué sirven AWS Glue for SAP u otros conectores SaaS?

Para extraer datos de aplicaciones empresariales (SAP OData, Salesforce, ServiceNow, Zendesk y otras) mediante conectores administrados hacia jobs de Glue o integraciones zero-ETL, sin escribir código de APIs.

### Escenarios

#### Diseña un pipeline que convierta archivos CSV diarios en S3 en un dataset particionado y consultable.

Dejo los CSV bajo un prefijo raw por fecha, ejecuto un job Spark de Glue (disparado por EventBridge o por programación) que lee los archivos del día con un esquema definido, limpia y convierte tipos, escribe Parquet o Iceberg particionado por fecha en un prefijo curado, actualiza el catálogo y ejecuta reglas de calidad de datos. Athena o Redshift Spectrum consultan la tabla curada; Lake Formation controla el acceso.

#### Un crawler crea docenas de tablas en lugar de una. ¿Qué pasa?

Los archivos bajo el prefijo tienen esquemas o estructuras de carpetas incoherentes (columnas extra, formatos distintos, archivos sueltos). Corrijo la organización del origen, añado patrones de exclusión, uso "create a single schema for each S3 path" o defino la tabla de forma explícita en lugar de usar el crawler.

#### Un job de Glue que tardaba 10 minutos ahora tarda 2 horas. ¿Cómo lo investigas?

Comparo el volumen y el número de archivos de entrada, compruebo si el pushdown predicate o los bookmarks dejaron de funcionar (reprocesa todo), miro en la Spark UI el skew o el spill, reviso el número de workers y el autoescalado, y busco un join que cambió o un broadcast que se perdió.

#### Tu job de Glue falla con "No space left on device". ¿Qué haces?

El job derrama o hace shuffle de más datos de los que caben en el disco local. Uso workers más grandes (más disco por executor), activo la opción de shuffle en S3, reduzco los datos antes de los shuffles (filtrar y seleccionar antes), corrijo el skew y aumento las particiones para que cada tarea maneje menos datos.

#### Las consultas de Athena sobre la tabla de Glue fallan con `HIVE_PARTITION_SCHEMA_MISMATCH`. ¿Por qué?

Algunas particiones se registraron con un esquema distinto al de la tabla (un crawler actualizó una partición tras un cambio en el origen). Hago que las particiones hereden el esquema de la tabla (ajuste del crawler "update all new and existing partitions with metadata from the table"), corrijo o reescribo las particiones raras y estabilizo el esquema del origen.

#### ¿Cómo cargarías el CDC de una base RDS PostgreSQL en un lakehouse con Glue?

Con DMS para la carga completa más el CDC hacia S3 (Parquet con una columna de operación), o con una integración zero-ETL si existe. Un job de Glue lee los archivos de cambios nuevos (bookmarks o particiones por fecha), deduplica por clave quedándose con el último cambio y ejecuta `MERGE INTO` sobre una tabla Iceberg registrada en el Data Catalog. La compactación y la expiración de snapshots la mantienen sana.

#### ¿Cómo ejecutas el mismo job de Glue en dev, staging y prod?

Un solo script con parámetros para las rutas, las bases de datos y las conexiones, desplegado con infraestructura como código por entorno (idealmente en cuentas separadas), con argumentos de job y roles IAM propios de cada entorno, y promovido con CI tras las pruebas.

#### ¿Cómo le explicarías AWS Glue a una persona no técnica?

Es el servicio de AWS que mantiene un inventario de los datos de la empresa y que limpia y mueve esos datos para dejarlos listos para reportes y análisis, sin tener que administrar servidores.

#### Necesitas deduplicar registros de clientes sin una clave común entre dos sistemas. ¿Qué herramienta de Glue ayuda?

La transformación de ML FindMatches: etiquetas ejemplos de pares que coinciden y que no, entrenas la transformación y la ejecutas en un job para asignar IDs de coincidencia; luego fusionas los registros por ID de coincidencia con reglas de negocio.

#### Un job de Glue escribe miles de archivos Parquet diminutos por día. ¿Cómo lo corriges?

Hago repartition por la columna de partición antes de escribir para que cada partición tenga pocos archivos, aumento el tamaño del lote (procesar un día en lugar de cada pocos minutos) y, si uso Iceberg, activo la compactación del catálogo o ejecuto `rewrite_data_files`.

#### ¿Cómo migrarías jobs on-premises de SSIS o Informatica a Glue?

Inventariando los jobs y sus dependencias, reconstruyendo los orígenes como conexiones de Glue, reescribiendo las transformaciones en PySpark (o jobs visuales), guardando los datos de referencia en S3 o en el catálogo, orquestando con Step Functions o Airflow y validando las salidas lado a lado antes de cambiar.

#### Los analistas se quejan de que las consultas de Athena sobre tablas de Glue son caras. ¿Qué cambias en los jobs de Glue?

Escribir Parquet o Iceberg en lugar de CSV/JSON, comprimir, particionar por los filtros habituales, producir menos archivos y más grandes, calcular estadísticas de columnas y quizá crear tablas agregadas para los dashboards frecuentes.

#### Un sistema de origen añade columnas nuevas sin avisar. ¿Cómo mantienes funcionando el pipeline de Glue?

Leyendo con la evolución del esquema en mente: DynamicFrames o esquemas permisivos en raw, selección explícita de columnas en las salidas curadas, alertas ante columnas nuevas (modo de solo registro del crawler o un control de esquema) y evolución de esquema de Iceberg para añadir columnas de forma intencionada.

#### ¿Cómo implementas una corrección de "datos tardíos" en un pipeline diario de Glue?

Procesando una ventana móvil (por ejemplo los últimos tres días) en cada ejecución con sobrescritura de particiones o `MERGE`, para que los registros tardíos actualicen las particiones correctas, y manteniendo la ventana parametrizada para correcciones mayores.

#### ¿Cómo eliges entre Glue, EMR Serverless y Databricks para una nueva plataforma de datos en AWS?

Glue para ETL serverless muy integrado con el catálogo de AWS y Lake Formation; EMR Serverless para Spark/Hive de código abierto con más control y a menudo menor costo a escala; Databricks para una plataforma lakehouse unificada con notebooks colaborativos, Delta, Unity Catalog y ML. Deciden las habilidades del equipo, los requisitos de gobierno y los modelos de costo.
