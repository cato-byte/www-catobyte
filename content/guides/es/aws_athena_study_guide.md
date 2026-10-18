## Guía de estudio de Amazon Athena

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de Amazon Athena: unas 200 preguntas](../../images/aws_athena_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre Amazon Athena: cómo funciona el SQL serverless sobre S3, las tablas y los SerDe, las particiones y la proyección de particiones, los formatos de archivo, las tablas Iceberg, `CTAS` y `UNLOAD`, los workgroups y el control de costos, la optimización del rendimiento, las consultas federadas, la seguridad y la resolución de problemas. Las respuestas reflejan el servicio en 2026. Abre una pregunta para ver su respuesta, o usa el filtro para buscar en toda la guía.

<!-- QA -->

### Fundamentos

#### ¿Qué es Amazon Athena?

Un servicio de consultas interactivas serverless que permite analizar datos directamente en Amazon S3 (y en otros orígenes mediante conectores) con SQL estándar. No hay infraestructura que administrar: defines tablas sobre tus datos, ejecutas consultas y pagas por los datos escaneados o por capacidad reservada.

#### ¿Qué motor usa Athena?

La versión 3 del motor SQL de Athena se basa en Trino (antes PrestoSQL) con mejoras propias de AWS, y el DDL usa una sintaxis compatible con Hive. Athena también ofrece Apache Spark mediante los notebooks de Athena para cargas PySpark.

#### ¿Cuáles son los casos de uso típicos de Athena?

Análisis ad hoc de data lakes, consulta de logs (CloudTrail, VPC Flow Logs, ALB, CloudFront, logs de acceso de S3), ELT ligero con `CTAS` e `INSERT INTO`, alimentar herramientas de BI como QuickSight, explorar datos antes de construir pipelines y consultar tablas Iceberg en un lakehouse.

#### ¿Cómo se cobra Athena?

Por defecto, por terabyte de datos escaneados (unos 5 USD por TB en muchas regiones), con un mínimo de 10 MB por consulta, redondeado al megabyte. Las sentencias DDL y las consultas fallidas no se cobran. Las reservas de capacidad ofrecen en cambio un precio fijo por DPU-hora. El almacenamiento y las solicitudes de S3 y el uso del Glue Data Catalog se facturan aparte.

#### ¿Por qué importa tanto el formato de los datos para el costo de Athena?

Porque pagas por byte escaneado. Los formatos columnares y comprimidos (Parquet, ORC) permiten que Athena lea solo las columnas que necesita la consulta y salte bloques con las estadísticas, lo que suele reducir los datos escaneados un 90 % o más frente a CSV o JSON sin comprimir.

#### ¿Dónde guarda Athena las definiciones de las tablas?

En el AWS Glue Data Catalog (por defecto), en un Hive metastore externo o en otros catálogos registrados como orígenes de datos (conectores federados, Redshift, catálogos de S3 Tables).

#### ¿Adónde van los resultados de las consultas?

A una ubicación de resultados en S3 (definida por workgroup o por consulta) como un archivo CSV más un archivo de metadatos, o al almacenamiento administrado de resultados que Athena conserva por un tiempo limitado. Los resultados se pueden cifrar y conviene una regla de ciclo de vida que borre los archivos viejos.

#### ¿Cómo se compara Athena con Amazon Redshift?

Athena es serverless y consulta los datos en su lugar en S3, ideal para cargas ad hoc, intermitentes o exploratorias, pagando por consulta. Redshift es un data warehouse (aprovisionado o serverless) optimizado para analítica compleja, frecuente y de alta concurrencia sobre datos cargados en su almacenamiento administrado, con funciones como vistas materializadas y gestión de cargas. Muchas arquitecturas usan ambos.

#### ¿Cómo se compara Athena con Redshift Spectrum?

Ambos consultan datos de S3 a través del Glue Data Catalog. Spectrum se ejecuta desde un cluster de Redshift y permite unir datos de S3 con tablas de Redshift; Athena es independiente y serverless. Spectrum es útil cuando el warehouse ya existe.

#### ¿Cómo se compara Athena con ejecutar Trino o Spark en EMR?

Athena elimina la administración de clusters y cobra por consulta o capacidad, pero da menos control sobre la configuración y los recursos. EMR sirve para cargas muy grandes y estables, configuraciones a medida o herramientas más allá de SQL.

#### ¿Qué es un workgroup?

Una forma de separar usuarios, equipos o aplicaciones: cada workgroup tiene su propia ubicación de resultados, ajustes de cifrado, versión del motor, límites de uso de datos, métricas de CloudWatch e historial de consultas, e IAM puede controlar quién usa cada workgroup.

#### ¿Cuáles son las principales interfaces de Athena?

El editor de consultas de la consola, la AWS CLI y los SDK (`StartQueryExecution`, `GetQueryExecution`, `GetQueryResults`), los drivers JDBC y ODBC para herramientas de BI y SQL, los notebooks de Athena para Spark, y las integraciones con QuickSight, Glue, Step Functions y Airflow.

#### ¿Athena es ACID?

En las tablas al estilo Hive, no: las consultas leen los archivos que existan, y las escrituras añaden archivos sin transacciones. En las tablas Apache Iceberg, sí: Athena admite `INSERT`, `UPDATE`, `DELETE` y `MERGE` ACID con aislamiento por snapshots y viaje en el tiempo.

#### ¿Cuál es el ciclo de vida de una consulta en Athena?

La consulta se envía (`QUEUED`), se planifica con los metadatos del catálogo y el descarte de particiones, se ejecuta en paralelo en el cómputo administrado de Athena leyendo de S3 (`RUNNING`) y termina como `SUCCEEDED`, `FAILED` o `CANCELLED`, con los resultados escritos en la ubicación de resultados.

#### ¿Qué límites de Athena conviene conocer?

Cuotas por cuenta de consultas DML y DDL activas a la vez, un timeout de consulta (30 minutos por defecto para DML, ajustable), la longitud del texto de la consulta, el número de particiones que puede añadir una sola consulta, y las tasas de solicitudes de S3 por prefijo, que pueden frenar las lecturas muy paralelas.

#### ¿Qué significa "esquema al leer" (schema on read) en Athena?

El esquema se aplica cuando se leen los datos, no cuando se escriben: los archivos de S3 los puede escribir cualquier herramienta, y la definición de la tabla le dice a Athena cómo interpretarlos al consultar. Es flexible, pero los archivos defectuosos solo aparecen como errores o `NULL` al consultarlos.

#### ¿Qué significa "serverless" en Athena?

No hay clusters que dimensionar, arrancar o parchar: AWS opera un motor de consultas compartido y multiinquilino, asigna recursos por consulta y pagas por consulta (o por capacidad reservada). No hay nada corriendo cuando no consultas.

#### ¿Qué servicios de AWS suelen alimentar de datos a Athena?

Kinesis Data Firehose (flujos hacia S3), AWS Glue (ETL y catálogo), AWS DMS (replicación de bases de datos a S3), los servicios de AWS que escriben logs en S3, S3 Inventory y las aplicaciones que escriben archivos directamente.

#### ¿Puede Athena escribir datos?

Sí: `CTAS`, `INSERT INTO`, `UNLOAD` y DML completo (`UPDATE`, `DELETE`, `MERGE`) sobre tablas Iceberg. Sobre las tablas al estilo Hive solo puede añadir archivos nuevos.

#### ¿Qué son las versiones del motor de Athena y cómo se actualizan?

Athena hace evolucionar su motor por versiones (la v3 es la actual); los workgroups pueden elegir las actualizaciones automáticas o una versión concreta. Las actualizaciones pueden cambiar el comportamiento de funciones o el manejo de tipos, así que prueba las consultas críticas antes de cambiar.

#### ¿Qué son las consultas guardadas del editor de Athena?

Consultas con nombre guardadas por workgroup que los usuarios pueden reutilizar y compartir, útiles para análisis recurrentes, aunque para el SQL de producción es mejor el control de versiones en Git.

### Tablas, DDL y SerDe

#### ¿Cómo se crea una tabla en Athena?

Con `CREATE EXTERNAL TABLE`, indicando las columnas, la ubicación en S3, el formato o SerDe, las columnas de partición y las propiedades de la tabla:

```sql
CREATE EXTERNAL TABLE logs.app_events (
  event_id   string,
  user_id    bigint,
  event_type string,
  payload    string,
  event_ts   timestamp
)
PARTITIONED BY (dt string)
STORED AS PARQUET
LOCATION 's3://my-lake/curated/app_events/'
TBLPROPERTIES ('parquet.compression' = 'SNAPPY');
```

#### ¿Por qué las tablas de Athena son "externas"?

Athena solo guarda metadatos; los datos se quedan en S3. Borrar una tabla externa elimina la definición pero no los archivos (las tablas Iceberg son distintas: borrarlas puede eliminar los datos).

#### ¿Qué es un SerDe?

Un serializador/deserializador que le dice a Athena cómo leer y escribir un formato: `LazySimpleSerDe` para texto delimitado, `OpenCSVSerDe` para CSV con comillas, `JsonSerDe` (Hive u OpenX) para JSON, `RegexSerDe` y `GrokSerDe` para logs, y lectores nativos para Parquet, ORC y Avro.

#### ¿Cuándo usar `OpenCSVSerDe` en lugar de `LazySimpleSerDe`?

Cuando los campos del CSV van entre comillas y pueden contener comas. `OpenCSVSerDe` maneja las comillas, pero trata todas las columnas como texto salvo que se conviertan los tipos, y tiene limitaciones con algunos tipos; `LazySimpleSerDe` es más rápido para archivos delimitados sencillos.

#### ¿Cómo se omite la fila de encabezado en archivos CSV?

Con la propiedad de tabla `'skip.header.line.count'='1'`.

#### ¿Cómo se lee JSON en Athena?

Con un SerDe JSON, un objeto JSON por línea. El SerDe de OpenX ofrece opciones como `ignore.malformed.json` y el mapeo sin distinguir mayúsculas. Los objetos anidados se mapean a tipos `struct` y los arreglos a `array`.

```sql
CREATE EXTERNAL TABLE raw.orders_json (
  order_id string,
  customer struct<id:bigint, country:string>,
  items array<struct<sku:string, qty:int, price:double>>
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES ('ignore.malformed.json' = 'true')
LOCATION 's3://my-lake/raw/orders/';
```

#### ¿Cómo se consultan arreglos anidados?

Con `UNNEST` en un `CROSS JOIN`, que produce una fila por elemento del arreglo:

```sql
SELECT o.order_id, i.sku, i.qty
FROM raw.orders_json o
CROSS JOIN UNNEST(o.items) AS t(i);
```

#### ¿Cómo se interpreta un JSON guardado en una columna de texto?

Con funciones JSON como `json_extract_scalar(payload, '$.customer.id')`, `json_extract`, `json_parse` y `CAST(json_parse(payload) AS map(varchar, json))`.

#### ¿Qué pasa si los datos no coinciden con el esquema de la tabla?

Athena aplica el esquema al leer: los valores que no encajan suelen convertirse en `NULL` o causan errores como `HIVE_BAD_DATA` (por ejemplo un texto en una columna entera, o un tipo de columna Parquet distinto del tipo de la tabla).

#### ¿Puede Athena manejar la evolución del esquema?

En Parquet, añadir columnas al final y leer por nombre funciona; renombrar o cambiar tipos es riesgoso. En CSV las columnas son posicionales, así que solo es seguro añadir columnas al final. Las tablas Iceberg admiten una evolución de esquema correcta (añadir, borrar, renombrar, reordenar, ampliar tipos).

#### ¿Qué es una vista en Athena?

Una consulta guardada (`CREATE VIEW`) en el catálogo que se consulta como una tabla. No guarda datos, así que cada consulta lee las tablas subyacentes y se factura en consecuencia.

#### ¿Qué hace `MSCK REPAIR TABLE`?

Recorre la ubicación de la tabla en S3 buscando carpetas de partición al estilo Hive (`clave=valor`) y añade al catálogo las particiones que faltan. Es lento en tablas con muchas particiones; es mejor añadir las particiones de forma explícita o usar la proyección de particiones.

#### ¿Qué hace `SHOW CREATE TABLE`?

Muestra el DDL de una tabla, útil para copiar definiciones entre entornos o revisar el SerDe y las propiedades.

#### ¿Cómo se consultan los logs de servicios de AWS con Athena?

Creando tablas con el DDL documentado para cada tipo de log (CloudTrail, VPC Flow Logs, ALB, CloudFront, logs de acceso de S3), idealmente con proyección de particiones por fecha y región, y consultándolas con SQL para investigar eventos de seguridad, tráfico y errores.

#### ¿Cómo se cambian las columnas de una tabla?

Con `ALTER TABLE … ADD COLUMNS`, `REPLACE COLUMNS` o `CHANGE COLUMN` (el comportamiento depende del formato), o recreando la tabla. En Iceberg, `ALTER TABLE … ADD COLUMNS`, `DROP COLUMN` y `RENAME COLUMN` son operaciones seguras sobre los metadatos.

#### ¿Cómo mapea Athena las columnas de Parquet: por nombre o por posición?

Por nombre, por defecto, en Parquet, así que el orden de las columnas de la tabla no tiene que coincidir con el de los archivos. CSV y otros formatos de texto mapean por posición.

#### ¿Qué tipos de datos admite Athena?

`boolean`, `tinyint`, `smallint`, `int`, `bigint`, `double`, `float`, `decimal(p,s)`, `char`, `varchar`, `string`, `binary`, `date`, `timestamp`, y los tipos complejos `array`, `map` y `struct`.

#### ¿Cómo se leen archivos con un delimitador propio?

Con `ROW FORMAT DELIMITED FIELDS TERMINATED BY '|'` (o `\t` para TSV), con las opciones `ESCAPED BY` y `LINES TERMINATED BY` cuando haga falta.

#### ¿Cómo se consultan datos usando una expresión regular?

Definiendo una tabla con `RegexSerDe` y una propiedad `input.regex` con grupos de captura para cada columna, útil para logs de formato fijo; para análisis puntuales, usa `regexp_extract` sobre una sola columna de texto.

#### ¿Cómo se consultan solo ciertos archivos de una ubicación?

Usando la pseudocolumna `"$path"` (la ruta S3 del archivo de cada fila) en un `WHERE`, que también ayuda a depurar qué archivo contiene datos malos.

```sql
SELECT "$path", count(*) FROM raw.app_events_csv GROUP BY 1 ORDER BY 2 DESC;
```

#### ¿Qué otras pseudocolumnas existen?

`"$path"`, `"$file_size"` y `"$file_modified_time"` describen el archivo de origen de cada fila, útiles para el linaje, la depuración y el procesamiento incremental.

### Particiones y proyección de particiones

#### ¿Qué es particionar en Athena?

Organizar los datos en S3 según los valores de una o más columnas (`s3://bucket/tabla/dt=2026-10-15/`) y declararlas como columnas de partición, para que las consultas que filtran por ellas solo lean las carpetas que coinciden.

#### ¿Qué es el descarte de particiones (partition pruning)?

El motor usa los filtros sobre las columnas de partición para saltarse las particiones que no pueden coincidir, lo que reduce los datos escaneados. Solo funciona cuando el filtro está sobre la propia columna de partición, sin funciones que impidan evaluarlo al planificar.

#### ¿Cómo se añaden particiones?

`ALTER TABLE t ADD PARTITION (dt='2026-10-15') LOCATION 's3://.../dt=2026-10-15/'`, `MSCK REPAIR TABLE` para carpetas al estilo Hive, un crawler de Glue, la API de Glue o la proyección de particiones (sin registro).

#### ¿Qué es la proyección de particiones?

Una configuración de tabla en la que Athena calcula los valores y ubicaciones de las particiones a partir de reglas en las propiedades de la tabla (rangos de fechas o enteros, enumeraciones, valores inyectados) en lugar de leerlas del catálogo. Las particiones nuevas no necesitan registro y la planificación es más rápida en tablas muy particionadas.

```sql
ALTER TABLE logs.app_events SET TBLPROPERTIES (
  'projection.enabled' = 'true',
  'projection.dt.type' = 'date',
  'projection.dt.range' = '2024-01-01,NOW',
  'projection.dt.format' = 'yyyy-MM-dd',
  'storage.location.template' = 's3://my-lake/curated/app_events/dt=${dt}/'
);
```

#### ¿Cuándo no encaja la proyección de particiones?

Cuando los valores de partición son impredecibles (por ejemplo IDs de clientes arbitrarios no conocidos de antemano, salvo que uses el tipo `injected` con filtros obligatorios), cuando otros motores (EMR, Spark) también necesitan las particiones en el catálogo, o cuando la mayoría de las particiones proyectadas no existen (Athena revisaría muchos prefijos vacíos).

#### ¿Qué es el tipo de proyección injected?

Un tipo de proyección en el que el valor de la partición debe venir en la cláusula `WHERE` de la consulta (por ejemplo `customer_id = '123'`); Athena lo usa para construir la ubicación. Sirve para claves de alta cardinalidad que siempre se usan como filtro.

#### ¿Cuál es una buena estrategia de particionado?

Particionar por las columnas por las que filtran la mayoría de las consultas (normalmente la fecha), con una granularidad que deje cada partición razonablemente grande (al menos decenas de MB, idealmente más), y evitar claves de partición de alta cardinalidad que crean millones de particiones diminutas.

#### ¿Qué diferencia hay entre rutas de partición al estilo Hive y no Hive?

Las rutas al estilo Hive contienen `clave=valor` (`dt=2026-10-15/`), que entienden `MSCK REPAIR` y los crawlers. Las rutas no Hive (`2026/10/15/`) requieren añadir las particiones de forma explícita con un `LOCATION`, o usar proyección de particiones con una plantilla de ubicación.

#### ¿Qué es el bucketing en Athena?

Repartir los datos dentro de las particiones en un número fijo de archivos según el hash de una columna (`CLUSTERED BY (user_id) INTO 32 BUCKETS`), lo que ayuda a las consultas que filtran por esa columna a saltarse archivos. Se usa sobre todo con `CTAS`.

#### ¿Por qué demasiadas particiones pueden empeorar el rendimiento?

La planificación tiene que traer y evaluar los metadatos de las particiones, y cada partición suele implicar listados de S3 y archivos pequeños aparte. Los índices de partición de Glue o la proyección de particiones reducen el costo de planificación.

#### ¿Cómo se ve qué particiones tiene una tabla?

`SHOW PARTITIONS tabla` lista las particiones registradas (no las proyectadas), y la consola o la API de Glue muestran las ubicaciones y esquemas de las particiones.

#### ¿Cómo se eliminan particiones?

`ALTER TABLE t DROP PARTITION (dt='2026-10-01')` elimina solo los metadatos del catálogo; borra los objetos de S3 por separado si también deben irse los datos.

#### ¿Se pueden mezclar la proyección de particiones y las particiones del catálogo?

Cuando la proyección está activada, Athena ignora las particiones registradas en el catálogo para esa tabla y solo usa las reglas de proyección. Los otros motores siguen viendo las particiones del catálogo.

#### ¿Cómo se particiona por fecha cuando los datos traen timestamps?

Derivando al escribir una fecha en texto (o año/mes/día) y guardándola como columna de partición; con Iceberg, usando el particionado oculto `day(event_ts)` para que las consultas filtren directamente por el timestamp.

#### ¿Por qué una consulta puede no descartar particiones aunque filtre por fecha?

El filtro puede aplicar una función a la columna de partición (por ejemplo `date(dt) = …` sobre una columna de texto), comparar con un tipo que obliga a convertir, o filtrar por una columna distinta de la clave de partición. Filtra por la columna de partición con literales del mismo tipo.

### Formatos de archivo y organización de los datos

#### ¿Qué formatos de archivo admite Athena?

CSV/TSV y otros textos delimitados, JSON, Parquet, ORC, Avro, Ion, logs con los SerDe Regex o Grok, y los formatos de tabla abiertos Iceberg, Hudi (lectura) y Delta Lake (lectura).

#### ¿Por qué se recomiendan Parquet y ORC?

Son columnares (solo se leen las columnas necesarias), se comprimen por columna y guardan estadísticas (mínimo y máximo por grupo de filas o stripe) que permiten a Athena saltar datos. También admiten predicate pushdown, lo que acelera las consultas y baja el costo.

#### ¿Qué códecs de compresión funcionan bien?

Snappy y ZSTD para Parquet y ORC (rápidos, divisibles dentro del formato). Para archivos de texto, gzip es común pero no divisible, así que un archivo gzip grande lo lee un solo worker; bzip2 es divisible pero lento.

#### ¿Cuál es el tamaño de archivo ideal para Athena?

Más o menos de 128 MB a 1 GB por archivo. Muchos archivos pequeños (de pocos KB) añaden sobrecarga por archivo y costos de solicitudes a S3; los archivos enormes no divisibles limitan el paralelismo.

#### ¿Cómo se arregla una tabla formada por muchos archivos pequeños?

Compactándolos: ejecutando un `CTAS` o `INSERT INTO` que reescriba los datos en menos archivos y más grandes (con bucketing o un particionado controlado), usando `OPTIMIZE` en las tablas Iceberg, o corrigiendo al productor (lotes más grandes, buffering de Firehose).

#### ¿Cómo ayuda a Athena ordenar los datos?

Cuando los datos están ordenados (o agrupados) por una columna de filtro habitual dentro de los archivos, las estadísticas de Parquet y ORC tienen rangos mínimo/máximo estrechos y se pueden saltar más grupos de filas.

#### ¿Qué significa la proyección columnar para `SELECT *`?

Con Parquet u ORC, seleccionar menos columnas escanea menos bytes, así que `SELECT *` sobre una tabla ancha cuesta mucho más que seleccionar solo las columnas necesarias.

#### ¿Cómo se convierten datos CSV a Parquet con Athena?

Con `CTAS`:

```sql
CREATE TABLE curated.app_events
WITH (
  format = 'PARQUET',
  write_compression = 'ZSTD',
  external_location = 's3://my-lake/curated/app_events/',
  partitioned_by = ARRAY['dt']
) AS
SELECT event_id, user_id, event_type, event_ts, dt
FROM raw.app_events_csv;
```

#### ¿Athena admite S3 Express One Zone o S3 Tables?

Sí. Athena puede consultar datos en directory buckets de S3 Express One Zone para menor latencia, y puede consultar y administrar tablas Iceberg en S3 Tables (table buckets) mediante su integración de catálogo.

#### ¿Qué es el predicate pushdown en Athena?

Los filtros se empujan al lector de archivos, que usa las estadísticas de Parquet/ORC para saltar grupos de filas o stripes cuyo mínimo/máximo no puede coincidir, así que se leen y descomprimen menos datos.

#### ¿Qué tamaño de grupo de filas es bueno para Parquet?

Normalmente de 128 MB a 512 MB; los grupos grandes comprimen bien y reducen la sobrecarga, pero los muy grandes reducen la eficacia del salto de datos. Escritores como Spark tienen valores por defecto razonables.

#### ¿La compresión reduce los costos de Athena?

Sí. Athena cobra sobre los bytes comprimidos escaneados, así que los archivos comprimidos (y la codificación columnar) reducen directamente el costo, además de reducir el almacenamiento en S3.

#### ¿Qué diferencia hay entre Parquet y ORC para Athena?

Ambos son columnares, con estadísticas y compresión, y funcionan bien. Parquet es la opción más común en el ecosistema (Spark, valores por defecto de Iceberg); ORC fue históricamente el favorito de Hive. Elige según los escritores y los otros motores que uses.

#### ¿Cómo se maneja un dato que llega como un único archivo gzip enorme?

Como gzip no es divisible, lo lee un solo worker. Divide el archivo antes o durante la ingesta, vuelve a comprimirlo como bzip2 o, mejor, conviértelo a Parquet con un `CTAS` o un job de Glue.

### Tablas Iceberg en Athena

#### ¿Qué es Apache Iceberg y por qué usarlo con Athena?

Un formato de tabla abierto que añade una capa de metadatos (snapshots, manifiestos) sobre archivos Parquet y ofrece transacciones ACID, evolución del esquema y de las particiones, particionado oculto, viaje en el tiempo y cambios a nivel de fila eficientes. Athena puede crear, leer y escribir tablas Iceberg registradas en el Glue Data Catalog.

#### ¿Cómo se crea una tabla Iceberg en Athena?

```sql
CREATE TABLE lake.customers (
  customer_id bigint,
  email       string,
  country     string,
  updated_at  timestamp
)
PARTITIONED BY (country)
LOCATION 's3://my-lake/iceberg/customers/'
TBLPROPERTIES ('table_type' = 'ICEBERG', 'format' = 'parquet');
```

#### ¿Qué sentencias DML admite Athena sobre Iceberg?

`INSERT INTO`, `UPDATE`, `DELETE` y `MERGE INTO`, además de `CREATE TABLE AS SELECT` hacia Iceberg, y `OPTIMIZE … REWRITE DATA` y `VACUUM` para el mantenimiento.

```sql
MERGE INTO lake.customers t
USING staging.customer_changes s ON t.customer_id = s.customer_id
WHEN MATCHED AND s.op = 'D' THEN DELETE
WHEN MATCHED THEN UPDATE SET email = s.email, country = s.country, updated_at = s.updated_at
WHEN NOT MATCHED THEN INSERT (customer_id, email, country, updated_at)
  VALUES (s.customer_id, s.email, s.country, s.updated_at);
```

#### ¿Qué es el particionado oculto de Iceberg?

Particiones definidas como transformaciones de columnas (`day(event_ts)`, `bucket(16, user_id)`, `truncate(10, sku)`), de modo que las consultas filtran por la columna original (`event_ts`) e Iceberg descarta las particiones automáticamente; los usuarios no necesitan conocer las columnas de partición.

#### ¿Cómo funciona el viaje en el tiempo de Iceberg en Athena?

```sql
SELECT * FROM lake.customers FOR TIMESTAMP AS OF TIMESTAMP '2026-10-15 08:00:00 UTC';
SELECT * FROM lake.customers FOR VERSION AS OF 949530903748831860;
```

También se pueden revisar las tablas de metadatos como `"customers$snapshots"`, `"customers$history"`, `"customers$files"` y `"customers$partitions"`.

#### ¿Qué hacen `OPTIMIZE` y `VACUUM` en las tablas Iceberg?

`OPTIMIZE tabla REWRITE DATA USING BIN_PACK` compacta los archivos pequeños y fusiona los archivos de borrado con los de datos. `VACUUM` expira los snapshots antiguos y elimina los archivos que ya no se referencian (según las propiedades de retención), liberando almacenamiento.

#### ¿Cómo funcionan los borrados a nivel de fila de Iceberg en Athena?

Athena escribe archivos de borrado por posición (merge-on-read) que marcan las filas borradas en lugar de reescribir los archivos de datos. Las lecturas los combinan al vuelo, así que las tablas con muchos borrados necesitan `OPTIMIZE` regularmente para seguir siendo rápidas.

#### ¿Se puede cambiar el particionado de una tabla Iceberg?

Sí. Puedes cambiar la especificación de particiones (por ejemplo de mensual a diaria) sin reescribir los datos viejos; los archivos antiguos conservan la especificación vieja, los datos nuevos usan la nueva y las consultas manejan ambas.

#### Iceberg o tablas al estilo Hive en Athena: ¿cómo eliges?

Iceberg cuando necesitas actualizaciones, borrados, upserts (CDC, borrados por GDPR o habeas data), evolución del esquema, escritores concurrentes o viaje en el tiempo. El Parquet al estilo Hive es más sencillo para datos inmutables de solo inserción escritos por otras herramientas. Los diseños nuevos de lakehouse suelen elegir Iceberg.

#### ¿Pueden otros motores usar las mismas tablas Iceberg?

Sí. Spark en EMR o Glue, Trino, Flink, Snowflake, Databricks y otros pueden leer y escribir las mismas tablas Iceberg mediante el Glue Data Catalog o un catálogo REST de Iceberg, lo que evita quedar atado a un motor.

#### ¿Qué propiedades de tabla importan para Iceberg en Athena?

`format` (parquet, orc, avro), `write_compression`, `optimize_rewrite_delete_file_threshold`, `vacuum_max_snapshot_age_seconds`, `vacuum_min_snapshots_to_keep` y `vacuum_max_metadata_files_to_keep`, que controlan la organización de los archivos y la retención.

#### ¿Pueden varios escritores modificar una tabla Iceberg a la vez?

Sí, con concurrencia optimista: cada commit comprueba la versión actual de la tabla, y los commits en conflicto fallan y deben reintentarse. Evita muchos escritores concurrentes actualizando las mismas particiones.

#### ¿Cómo se añade una columna a una tabla Iceberg?

`ALTER TABLE lake.customers ADD COLUMNS (segment string)`. Los archivos existentes no se reescriben; las filas viejas devuelven `NULL` en la nueva columna.

#### ¿Cómo se revierte una tabla Iceberg en Athena?

Leyendo la versión anterior con viaje en el tiempo y reescribiéndola (por ejemplo con un `CTAS` desde `FOR VERSION AS OF`), o usando un motor con procedimientos de reversión (`rollback_to_snapshot` de Spark) sobre la misma tabla.

#### ¿Qué son las S3 Tables?

Table buckets de S3 que guardan tablas Iceberg con mantenimiento integrado (compactación, gestión de snapshots) y una integración de catálogo, que Athena puede consultar y escribir como cualquier otra tabla Iceberg.

### CTAS, INSERT y UNLOAD

#### ¿Qué es `CTAS`?

`CREATE TABLE AS SELECT`: crea una tabla nueva a partir de los resultados de una consulta, escribiendo en S3 archivos con el formato, la compresión, el particionado y el bucketing elegidos. Se usa para convertir formatos, construir agregados y materializar transformaciones.

#### ¿Cuáles son los límites de `CTAS` e `INSERT INTO`?

Una sola consulta puede crear o insertar en un número limitado de particiones (100 por consulta en las tablas Hive), así que los backfills grandes necesitan varias sentencias o bucles por rangos de particiones. Las tablas Iceberg no tienen ese límite en particular.

#### ¿Qué hace `INSERT INTO` en una tabla al estilo Hive?

Añade archivos nuevos en la ubicación de la tabla (y registra las particiones nuevas). Nunca modifica los archivos existentes, así que volver a ejecutarlo duplica los datos salvo que antes borres los archivos de la partición destino.

#### ¿Cómo se hace idempotente un ELT con Athena?

En las tablas Hive, escribiendo la salida de cada ejecución en una partición y borrando o sobrescribiendo esa partición antes de volver a ejecutar (a menudo escribiendo en una ubicación nueva y cambiando la ubicación de la partición). En las tablas Iceberg, usando `MERGE` o `DELETE` más `INSERT` en la misma lógica, o patrones de sobrescritura con Iceberg.

#### ¿Qué hace `UNLOAD`?

Escribe los resultados de una consulta en S3 con el formato elegido (Parquet, ORC, Avro, JSON, texto), con particionado y compresión opcionales, sin crear una tabla, lo que es útil para exportar a otros sistemas.

```sql
UNLOAD (SELECT * FROM curated.app_events WHERE dt = '2026-10-15')
TO 's3://exports/app_events/dt=2026-10-15/'
WITH (format = 'PARQUET', compression = 'SNAPPY');
```

#### ¿Cómo se programan consultas de Athena?

Con EventBridge Scheduler o Step Functions llamando a `StartQueryExecution`, el `AthenaOperator` de Airflow, dbt con el adaptador dbt-athena, o una función Lambda programada.

#### ¿Se puede usar dbt con Athena?

Sí, con el adaptador dbt-athena: los modelos se materializan como vistas, tablas (`CTAS`), modelos incrementales (`insert_overwrite` por partición, `append` o `merge` sobre Iceberg) y tablas Iceberg, con Glue como catálogo.

#### ¿Qué son las sentencias preparadas y las consultas parametrizadas?

Sentencias creadas con `PREPARE` (o enviadas con `ExecutionParameters`) que contienen marcadores `?` que se llenan al ejecutar, lo que evita la inyección SQL y permite a las aplicaciones reutilizar el texto de la consulta.

```sql
PREPARE events_by_day FROM
SELECT event_type, count(*) FROM curated.app_events WHERE dt = ? GROUP BY 1;

EXECUTE events_by_day USING '2026-10-15';
```

#### ¿Cómo se crea una copia vacía del esquema de una tabla?

`CREATE TABLE nueva_t WITH (...) AS SELECT * FROM t WITH NO DATA`, que crea la definición de la tabla sin escribir filas.

#### ¿Cómo se controla el número de archivos de salida en `CTAS`?

Con `bucketed_by` y `bucket_count`, que fijan el número de archivos por partición, o reduciendo el paralelismo del stage final; si no, Athena escribe tantos archivos como produzcan los workers.

#### ¿Puede un `CTAS` escribir en una ubicación de S3 que ya existe?

No. El `external_location` debe estar vacío, lo que evita sobrescribir datos por error. Borra la ubicación o usa una nueva para las reejecuciones.

#### ¿Cómo se exportan los resultados de una consulta como un solo CSV?

Ejecutando la consulta y descargando el archivo de resultados de la ubicación de resultados (Athena escribe un CSV por consulta), o usando `UNLOAD` con un formato de texto; los resultados muy grandes pueden quedar divididos en varios archivos con `UNLOAD`.

### Optimización del rendimiento

#### ¿Cuáles son las principales formas de hacer más rápidas y baratas las consultas de Athena?

Usar formatos columnares con compresión, particionar por los filtros habituales (o con proyección), mantener archivos de 128 MB a 1 GB, seleccionar solo las columnas necesarias, filtrar por las columnas de partición, ordenar o hacer bucketing por los filtros habituales, usar Iceberg con compactación, calcular estadísticas de las tablas y reutilizar resultados.

#### ¿Cómo se ve cuántos datos escaneó una consulta?

En la consola después de ejecutarla, en las estadísticas de `GetQueryExecution` (`DataScannedInBytes`), en las métricas de CloudWatch del workgroup y en la salida de `EXPLAIN ANALYZE` por stage.

#### ¿Qué muestran `EXPLAIN` y `EXPLAIN ANALYZE`?

`EXPLAIN` muestra el plan distribuido o lógico sin ejecutar la consulta: lecturas, filtros empujados, joins y su distribución. `EXPLAIN ANALYZE` ejecuta la consulta e informa las filas, los datos leídos y el tiempo reales por stage, lo que muestra dónde se va el tiempo.

#### ¿En qué orden se deben poner las tablas en un join?

El motor v3 tiene un optimizador basado en costos que puede reordenar los joins cuando hay estadísticas de las tablas en el catálogo de Glue. Sin estadísticas, pon la tabla más grande primero (a la izquierda) y las más pequeñas a la derecha, porque el lado derecho se construye en memoria y se distribuye a los workers.

#### ¿Qué tipos de distribución de join existen?

Los broadcast joins envían la tabla pequeña del lado derecho a todos los workers (rápido si es pequeña); los joins particionados reparten ambos lados por hash entre los workers (necesario con dos tablas grandes). El optimizador elige según las estadísticas.

#### ¿Por qué un `ORDER BY` sin `LIMIT` empeora el rendimiento?

Un orden global requiere enviar todas las filas a un solo worker para el orden final, lo que es lento y puede fallar con "exceeded resources". Añade un `LIMIT` (el top-N es eficiente) u ordena solo lo necesario.

#### ¿Qué es "Query exhausted resources at this scale factor"?

Un error cuando una consulta necesita más memoria de la disponible para una operación (joins enormes, `GROUP BY` con muchos grupos, `DISTINCT` sobre muchas columnas, `ORDER BY` de todo, arreglos muy grandes). Soluciones: filtrar antes, reducir columnas, funciones aproximadas, dividir la consulta, materializar pasos intermedios con `CTAS` o usar reservas de capacidad.

#### ¿Cuándo conviene usar funciones aproximadas?

`approx_distinct`, `approx_percentile` y `approx_most_frequent` devuelven estimaciones con errores pequeños usando mucha menos memoria que `count(DISTINCT)` o los percentiles exactos, lo que sirve para dashboards y exploración.

#### ¿Qué es la reutilización de resultados de consultas?

Una función en la que Athena devuelve los resultados de una consulta anterior si la misma consulta se ejecutó hace poco (dentro de una antigüedad máxima que defines, de hasta 7 días) y los datos no cambiaron (en las tablas compatibles), sin volver a escanear datos.

#### ¿Cómo ayudan a Athena las estadísticas de las tablas?

Las estadísticas de columnas guardadas en el catálogo de Glue (calculadas por Glue) permiten que el optimizador basado en costos elija el orden y la distribución de los joins, mejorando las consultas complejas sin cambiar el código.

#### ¿Cómo se aceleran las búsquedas con `LIKE` sobre columnas de texto grandes?

Filtrando primero por particiones, usando `regexp_like` solo cuando haga falta, y extrayendo durante el ETL los campos buscables en columnas aparte, o usando un servicio de búsqueda como OpenSearch para necesidades de texto completo.

#### ¿Por qué el throttling de S3 puede ralentizar las consultas de Athena?

S3 admite altas tasas de solicitudes por prefijo, pero las consultas sobre millones de archivos pequeños en un mismo prefijo pueden recibir errores `SlowDown` (503). Menos archivos y más grandes, y repartir los datos entre prefijos (particiones), lo evitan.

#### ¿Qué son las reservas de capacidad?

Capacidad dedicada de procesamiento de consultas comprada en DPU (por una duración mínima y luego por minuto) y asignada a workgroups. Las consultas de esos workgroups corren sobre la capacidad reservada, facturadas por DPU-hora en lugar de por TB escaneado, con costo y concurrencia predecibles.

#### ¿Cuándo valen la pena las reservas de capacidad?

Cuando el volumen de consultas es alto y estable (dashboards de BI intensivos, muchos usuarios concurrentes), cuando necesitas concurrencia garantizada para cargas críticas, o cuando el costo por TB supera el precio de la capacidad reservada.

#### ¿Por qué `count(DISTINCT x)` sobre una tabla enorme falla o es lento?

Requiere mantener todos los valores distintos en memoria entre los workers. Usa `approx_distinct(x)` para estimaciones, o preagrega conteos distintos por partición y combínalos.

#### ¿Cómo afectan las funciones de ventana al rendimiento de Athena?

Las funciones de ventana particionan y ordenan los datos; una ventana sobre toda la tabla (sin `PARTITION BY`) obliga a usar un solo worker. Particiona siempre las ventanas por una clave y filtra los datos antes.

#### ¿Qué efecto tiene `UNION` frente a `UNION ALL`?

`UNION` elimina duplicados, lo que requiere un paso extra de agregación; `UNION ALL` solo concatena. Usa `UNION ALL` cuando los duplicados son imposibles o aceptables.

#### ¿Cómo se optimizan las consultas sobre una combinación grande de dimensiones muy consultada?

Precalculando agregados en una tabla resumen (`CTAS` o `INSERT` programado), particionada por fecha, y apuntando los dashboards a ella en lugar de a la tabla en bruto.

#### ¿Cómo afecta `LIMIT` al costo?

En las tablas al estilo Hive, un `LIMIT` sin filtros puede detenerse antes pero aun así escanear muchos archivos; no garantiza un costo bajo. Los filtros de partición son la forma confiable de limitar lo escaneado.

#### ¿Qué impacto tiene el data skew en los joins y agregaciones de Athena?

Unas pocas claves con la mayoría de las filas sobrecargan a workers individuales y pueden causar errores de "exhausted resources". Filtra las claves calientes (a menudo los nulos), trátalas aparte o usa agregaciones aproximadas.

### Workgroups, control de costos y monitoreo

#### ¿Cómo se limitan los costos por equipo?

Creando un workgroup por equipo o aplicación con un límite de uso de datos por consulta (cancela las consultas que escanean más de un umbral) y límites por periodo para todo el workgroup que disparan alarmas, imponiendo la configuración del workgroup para que los usuarios no la sobrescriban y etiquetando los workgroups para la asignación de costos.

#### ¿Qué significa "override client-side settings" en un workgroup?

Cuando se activa, la ubicación de resultados, el cifrado y otros ajustes del workgroup se aplican a todas las consultas, ignorando lo que indiquen los clientes, lo que impone el gobierno.

#### ¿Cómo se monitorea el uso de Athena?

Con métricas de CloudWatch por workgroup (datos escaneados, duración, tiempo en cola, consultas fallidas), el historial de consultas (`ListQueryExecutions`, consola), CloudTrail para las llamadas a la API e informes de costos con etiquetas.

#### ¿Cuánto tiempo se guarda el historial de consultas?

Athena guarda el historial durante 45 días. Para conservarlo más o analizarlo, exporta los detalles de ejecución (por ejemplo con eventos de EventBridge o un job programado que llame a `GetQueryExecution`) a S3.

#### ¿Cómo encuentras las consultas más caras?

En el historial o en los datos de ejecución exportados, ordenando por `DataScannedInBytes`; luego revisas si filtran por particiones, leen CSV o JSON, o seleccionan demasiadas columnas.

#### ¿Cómo se evitan las consultas descontroladas?

Con límites de datos por consulta en los workgroups, timeouts de consulta, formación sobre los filtros de partición, vistas que exigen filtros de partición y reservas de capacidad para las cargas predecibles.

#### ¿Cómo afectan las solicitudes de S3 a los costos de Athena?

El precio por TB de Athena no incluye las solicitudes GET y LIST de S3, que factura S3. Las tablas con enormes cantidades de archivos pequeños pueden generar costos de solicitudes importantes además del cobro de Athena.

#### ¿Qué diferencia hay entre un límite por consulta y uno de todo el workgroup?

Un control por consulta cancela cualquier consulta que escanee más del umbral. Los controles de todo el workgroup miden el total escaneado en un periodo y disparan alarmas de CloudWatch o notificaciones de SNS, pero no cancelan consultas.

#### ¿Cómo se asignan los costos de Athena a los equipos?

Con workgroups separados por equipo, etiquetados con etiquetas de asignación de costos, y analizando los costos en Cost Explorer por etiqueta; con reservas de capacidad, asignando los workgroups a reservas por equipo.

#### ¿Cómo se siguen los fallos de las consultas?

Con las métricas de CloudWatch de consultas fallidas por workgroup, los eventos "Athena Query State Change" de EventBridge enviados a alertas y el historial de consultas con los mensajes de error.

### Consultas federadas y conectores

#### ¿Qué es Athena Federated Query?

Una función que permite a Athena consultar datos fuera de S3, como DynamoDB, RDS y Aurora (MySQL, PostgreSQL), Redshift, DocumentDB, OpenSearch, CloudWatch Logs, Snowflake, BigQuery y muchos más, mediante conectores de orígenes de datos que corren como funciones AWS Lambda (o como conexiones administradas de Glue).

#### ¿Cómo funcionan los conectores federados?

La Lambda del conector recibe parte del plan de la consulta, lee los datos del origen (empujando los filtros y las proyecciones cuando se puede) y los devuelve a Athena en formato Apache Arrow, que luego los une y agrega con otros datos.

#### ¿Cuáles son las desventajas de las consultas federadas?

El rendimiento depende del origen y de la Lambda (timeouts, memoria, concurrencia), las consultas pueden cargar las bases operativas, el pushdown es limitado en algunos orígenes y pagas Lambda más los datos escaneados. Para un uso frecuente e intensivo, replica los datos en S3.

#### ¿Cómo se une un dato de S3 con una tabla de RDS?

Registrando el conector de RDS como origen de datos (por ejemplo `rds_pg`) y consultando `SELECT … FROM lake.orders o JOIN rds_pg.public.customers c ON o.customer_id = c.id`, manteniendo pequeño el lado de RDS con filtros.

#### ¿Qué son las funciones definidas por el usuario en Athena?

Funciones escalares implementadas en una función Lambda (Java) y llamadas con `USING EXTERNAL FUNCTION`, usadas para lógica que no existe en SQL, como llamar a un servicio interno o un descifrado propio.

#### ¿Puede Athena llamar a modelos de machine learning?

Sí, con `USING EXTERNAL FUNCTION … SAGEMAKER 'nombre-endpoint'`, que envía filas a un endpoint de SageMaker para hacer inferencia dentro de una consulta.

#### ¿Cómo se despliega un conector federado?

Desde la consola de Athena (creando un origen de datos), que despliega la Lambda del conector desde el AWS Serverless Application Repository o usa conexiones de Glue, con un bucket de spill en S3 para los resultados grandes y la configuración de IAM y VPC adecuada.

#### ¿Para qué sirve el bucket de spill?

Una ubicación de S3 donde el conector escribe los datos que superan los límites de tamaño de respuesta de Lambda, y que Athena luego lee. Debe estar cifrado y tener una regla de ciclo de vida.

#### ¿Cómo se consulta DynamoDB con Athena?

Con el conector de DynamoDB, que escanea o consulta la tabla (consumiendo capacidad de lectura); para consultas analíticas grandes, exporta la tabla a S3 (exportación de DynamoDB) y consulta la exportación.

#### ¿Se puede escribir un conector propio?

Sí, con el Athena Query Federation SDK (Java), implementando los manejadores de metadatos y de registros para tu origen, desplegado como función Lambda.

### Seguridad y gobierno

#### ¿Cómo se controla el acceso a Athena?

Con políticas IAM sobre las acciones de Athena y los workgroups, permisos de S3 sobre los datos y las ubicaciones de resultados, permisos del Glue Data Catalog (bases, tablas) y, para un control detallado, permisos de Lake Formation sobre bases de datos, tablas, columnas, filas y celdas.

#### ¿Cómo funciona Lake Formation con Athena?

Athena comprueba los permisos de Lake Formation de quien consulta y solo devuelve las columnas y filas permitidas, usando credenciales temporales que entrega Lake Formation para leer S3, así que los usuarios no necesitan acceso directo a S3 sobre los datos.

#### ¿Cómo se cifran los datos de Athena?

Los datos en S3 se pueden cifrar con SSE-S3, SSE-KMS o KMS del lado del cliente; Athena lee los datos cifrados de forma transparente con los permisos de KMS adecuados. Los resultados de las consultas se pueden cifrar (SSE-S3, SSE-KMS, CSE-KMS) por workgroup, y los datos en tránsito usan TLS.

#### ¿Cómo se restringe qué datos de S3 puede consultar un usuario?

Concediendo el acceso a las tablas mediante Lake Formation (sin permisos directos de S3), o con IAM limitando el acceso de S3 a prefijos concretos y el acceso de Glue a bases y tablas concretas.

#### ¿Cómo se consultan datos de otra cuenta de AWS?

Con el uso compartido entre cuentas de Lake Formation (resource links), el acceso entre cuentas al catálogo de Glue registrado como origen de datos, o políticas de bucket que dan al rol que consulta acceso a los datos y a su clave KMS.

#### ¿Cómo se audita el uso de Athena?

CloudTrail registra las llamadas a la API (quién lanzó qué consulta, con su texto), Lake Formation registra el acceso a los datos, y los logs de acceso del servidor de S3 o los eventos de datos de CloudTrail registran las lecturas de objetos.

#### ¿Cómo se usa Athena desde una red privada?

Mediante endpoints de interfaz de VPC para Athena (y para Glue, S3 y KMS según haga falta), para que el tráfico no pase por internet; las políticas del endpoint pueden restringir el uso.

#### ¿Qué es un data filter de Lake Formation?

Una definición de seguridad a nivel de fila y de celda para una tabla (una expresión de filtro de filas más las columnas incluidas o excluidas) que se concede a principals; Athena la aplica al consultar.

#### ¿Cómo se da acceso seguro a Athena a una herramienta de BI?

Creando un rol o usuario IAM dedicado (preferiblemente federado con IAM Identity Center u OAuth para el driver), limitado a un workgroup, a las tablas necesarias vía Lake Formation y a la ubicación de resultados, y conectando con el driver JDBC/ODBC.

#### ¿Cómo se enmascaran columnas sensibles en Athena?

Excluyéndolas con permisos de columna de Lake Formation, ofreciendo vistas que las hashean u ocultan, o guardando copias enmascaradas en una tabla curada aparte para el acceso general.

### Spark en Athena y notebooks

#### ¿Qué es Amazon Athena for Apache Spark?

Una oferta de Spark serverless en Athena en la que ejecutas PySpark y Spark SQL en notebooks o mediante APIs, con un arranque rápido y facturación por DPU-hora, para cargas que necesitan más que SQL.

#### ¿Cuándo usarías Athena Spark en lugar de Athena SQL?

Para transformaciones complejas en Python, preparación para machine learning, exploración iterativa con DataFrames o lógica incómoda en SQL; el SQL sigue siendo más simple y barato para la mayoría de la analítica.

#### ¿Cómo se facturan las sesiones de Athena Spark?

Por DPU-hora del cómputo de la sesión, con escalado automático de los executors y timeouts de inactividad que terminan la sesión.

#### ¿Cómo accede Athena Spark al Data Catalog?

Las sesiones Spark de Athena usan por defecto el Glue Data Catalog, así que puedes leer y escribir tablas del catálogo (incluidas Iceberg) con Spark SQL o DataFrames.

#### ¿Qué lenguajes admiten los notebooks de Athena?

PySpark y Spark SQL (con comandos mágicos), con librerías Python comunes disponibles y la posibilidad de añadir otras a la sesión.

### Resolución de problemas

#### Una consulta devuelve cero filas pero los archivos existen. ¿Qué revisas?

Si las particiones están registradas (o si la proyección está bien configurada), si el `LOCATION` y la plantilla de ubicación coinciden con las rutas reales, si el SerDe y las columnas corresponden al formato, y si los archivos están en subcarpetas que la tabla no incluye.

#### ¿Qué significa `HIVE_PARTITION_SCHEMA_MISMATCH`?

El esquema de una partición en el catálogo difiere del de la tabla (tipos o columnas). Haz que las particiones hereden el esquema de la tabla (ajuste del crawler o recreando las particiones) y estabiliza el origen.

#### ¿Qué suele indicar `HIVE_CURSOR_ERROR`?

Un problema al leer un archivo: archivos corruptos o truncados, un formato distinto al de la definición de la tabla, un archivo comprimido ilegible, o problemas de permisos o de KMS en algunos objetos.

#### ¿Qué significa `HIVE_BAD_DATA`?

Un valor no se puede interpretar con el tipo declarado, por ejemplo texto en una columna numérica, un registro JSON mal formado o un tipo de Parquet que no coincide. Corrige los datos, los tipos de la tabla, o usa `TRY_CAST` sobre columnas de texto.

#### ¿Por qué aparece `Access Denied` en una consulta?

Faltan permisos sobre los datos de S3, la ubicación de resultados, la clave KMS, los objetos del catálogo de Glue, los permisos de Lake Formation o el workgroup. El mensaje de error suele nombrar el recurso.

#### ¿Por qué una consulta sobre fechas y horas devuelve resultados incorrectos?

Marcas de tiempo guardadas como texto en formatos distintos, confusión de zonas horarias (los timestamps sin zona se interpretan como UTC en muchos casos) o codificaciones de timestamp de Parquet que difieren entre escritores. Interpreta de forma explícita con `from_iso8601_timestamp` o `parse_datetime` y convierte las zonas con `AT TIME ZONE`.

#### Una consulta es lenta pero escanea pocos datos. ¿Qué puede causarlo?

El tiempo de planificación en tablas con muchas particiones (usa proyección o índices de partición), muchos archivos diminutos (sobrecarga por archivo), un origen federado, la espera por límites de concurrencia, o una operación costosa como un join grande o un orden global.

#### Los resultados tienen duplicados tras reejecutar un pipeline. ¿Por qué?

El pipeline usó `INSERT INTO` sobre una tabla Hive sin eliminar la salida anterior, o se escribieron archivos dos veces en la misma ubicación. Haz idempotentes las escrituras (sobrescribir particiones, `MERGE` de Iceberg) y deduplica las particiones afectadas.

#### ¿Por qué `MSCK REPAIR TABLE` no añade ninguna partición?

Las carpetas no están al estilo Hive (`clave=valor`), los nombres de las claves no coinciden con los de las columnas de partición (importan las mayúsculas), la ubicación está mal o la tabla tiene activada la proyección de particiones.

#### ¿Por qué los números salen como `NULL` desde una tabla CSV?

Los valores contienen caracteres que no se pueden interpretar (separadores de miles, símbolos de moneda, comillas con `LazySimpleSerDe`, cadenas vacías), o las columnas están corridas porque un campo contiene el delimitador. Usa `OpenCSVSerDe`, limpia los datos, o lee como texto y aplica `TRY_CAST`.

#### ¿Por qué aparece "Query timeout"?

La consulta superó el timeout del workgroup: escanea demasiados datos, un join u orden pesado, o un origen federado lento. Optimiza la consulta o la organización de los datos, materializa pasos intermedios o sube la cuota del timeout.

#### ¿Por qué hay errores de "too many open files" o `SlowDown` de S3?

Las tablas con una cantidad enorme de archivos pequeños provocan muchísimas solicitudes concurrentes a S3. Compacta los archivos y repártelos entre particiones.

#### ¿Por qué una consulta sobre Iceberg se vuelve más lenta con el tiempo?

Se acumulan muchos archivos pequeños y archivos de borrado con las escrituras frecuentes y los cambios a nivel de fila. Programa `OPTIMIZE` y `VACUUM` (o usa la compactación automática del catálogo de Glue o de S3 Tables).

### Funciones SQL y patrones

#### ¿Cómo se trabaja con fechas y horas en Athena?

Con funciones como `current_date`, `date_add('day', -1, current_date)`, `date_diff('day', a, b)`, `date_trunc('month', ts)`, `date_format(ts, '%Y-%m-%d')`, `from_iso8601_timestamp(s)`, `parse_datetime(s, 'yyyy-MM-dd HH:mm')` y `ts AT TIME ZONE 'America/Bogota'`.

#### ¿Cómo se convierten tipos de forma segura?

`TRY_CAST(x AS integer)` devuelve `NULL` en lugar de fallar con valores malos, y `try()` envuelve expresiones que pueden dar error. Úsalos sobre datos de texto en bruto.

#### ¿Cómo se deduplican filas en Athena?

Con `row_number()` por clave ordenado por una marca de tiempo, quedándose con la primera fila por clave, en una subconsulta o CTE, ya que Athena no admite `QUALIFY`.

#### ¿Cómo se pivotan datos en Athena?

Con agregación condicional, porque no existe la palabra `PIVOT`: `sum(CASE WHEN month = 1 THEN amount END) AS ene`, o `map_agg` para construir un mapa clave-valor.

#### ¿Qué funciones de arreglos y mapas son útiles?

`cardinality`, `contains`, `element_at`, `array_join`, `array_agg`, `filter`, `transform`, `reduce`, `map_keys`, `map_values` y `map_agg`, que permiten trabajar con datos anidados sin desplegarlos.

#### ¿Cómo se calcula un total acumulado o un promedio móvil?

Con funciones de ventana: `sum(amount) OVER (PARTITION BY customer ORDER BY dt ROWS UNBOUNDED PRECEDING)` para los totales acumulados y `avg(amount) OVER (ORDER BY dt ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)` para un promedio móvil de 7 filas.

#### ¿Cómo se genera una serie de fechas en Athena?

Con `sequence` y `UNNEST`: `SELECT d FROM UNNEST(sequence(date '2026-01-01', date '2026-12-31', interval '1' day)) AS t(d)`, útil para llenar huecos en series de tiempo.

#### ¿Cómo se obtienen las N primeras filas por grupo?

Usando `row_number()` o `rank()` por grupo ordenado por la métrica en una subconsulta y filtrando por el rango en la consulta externa; `max_by(x, y)` da el valor de `x` en el máximo de `y` por grupo.

#### ¿Para qué sirven `max_by` y `min_by`?

Para devolver el valor de una columna en la fila donde otra columna es máxima o mínima, por ejemplo el último estado de cada pedido: `max_by(status, updated_at)`, sin una función de ventana.

#### ¿Cómo se hacen consultas geoespaciales en Athena?

Con funciones geoespaciales como `ST_Point`, `ST_Contains`, `ST_Distance`, `ST_Within`, `ST_GeometryFromText` y `great_circle_distance`, por ejemplo para contar eventos dentro de polígonos.

#### ¿Cómo se hashean valores para seudonimizar?

Con `to_hex(sha256(to_utf8(email)))` (preferiblemente con una sal secreta o un HMAC con `hmac_sha256`), lo que produce seudónimos estables que se pueden seguir uniendo.

#### ¿Cómo se escribe lógica SQL reutilizable en Athena?

Con vistas para la lógica compartida, CTE (`WITH`) para la legibilidad dentro de una consulta, y macros de dbt cuando se usa dbt-athena.

#### ¿Cómo se comparan dos tablas para encontrar diferencias?

Con `EXCEPT` en ambos sentidos (`SELECT * FROM a EXCEPT SELECT * FROM b`) para las diferencias de filas, o un full outer join por clave comparando columnas, útil para validar migraciones.

#### ¿Cómo se toman muestras de datos en Athena?

`TABLESAMPLE BERNOULLI (1)` lee las filas con un 1 % de probabilidad (pero escanea todos los datos), y `TABLESAMPLE SYSTEM (1)` muestrea a nivel de archivo o split, lo que puede reducir los datos escaneados.

#### ¿Cómo se manejan los valores `NULL` en agregaciones y comparaciones?

Las agregaciones ignoran los `NULL` (salvo `count(*)`); las comparaciones con `NULL` devuelven `NULL`, así que usa `IS NULL`, `coalesce`, `IS DISTINCT FROM` para comparar sin problemas con nulos, y ten cuidado con `NOT IN` sobre columnas que contienen nulos.

### Escenarios

#### Diseña una solución barata de analítica de logs con Athena.

Envío los logs a S3 con Firehose (con buffer, convertidos a Parquet, particionados por fecha), defino una tabla con proyección de particiones por fecha, creo vistas para las preguntas frecuentes, configuro un workgroup con límites de datos y doy acceso a los analistas mediante Lake Formation. Añado reglas de ciclo de vida para mover los logs viejos a clases de almacenamiento más baratas.

#### Tu factura de Athena se duplicó. ¿Cómo lo investigas?

Reviso en CloudWatch los datos escaneados por workgroup, busco en el historial las consultas con más bytes escaneados, y busco dashboards nuevos con consultas sin filtrar, `SELECT *` sobre tablas anchas, tablas en CSV o JSON, y filtros de partición que dejaron de funcionar (por ejemplo una función sobre la columna de partición). Luego corrijo formatos y filtros y añado límites por consulta.

#### Los analistas necesitan borrar los datos de clientes concretos por GDPR o habeas data. ¿Cómo lo soportas en Athena?

Guardando los datos en tablas Iceberg, ejecutando `DELETE FROM … WHERE customer_id = …` en las tablas afectadas, y luego `OPTIMIZE` y `VACUUM` para eliminar físicamente los archivos viejos tras el periodo de retención de los snapshots. Con tablas Hive habría que reescribir particiones completas.

#### ¿Cómo construirías un pequeño pipeline ELT solo con Athena?

Tablas raw sobre los archivos de aterrizaje, `CTAS` o `INSERT INTO` (o modelos de dbt-athena) para construir tablas limpias en Iceberg o Parquet, `MERGE` para los upserts, controles de calidad como consultas SQL que hacen fallar el pipeline cuando devuelven filas, y Step Functions o Airflow para programar y ordenar las sentencias.

#### Un dashboard de QuickSight sobre Athena es lento y caro. ¿Qué cambias?

Preagrego en una tabla resumen que se refresca de forma programada, uso SPICE de QuickSight para tener los datos en caché, me aseguro de que el dashboard aplique filtros de partición, convierto las tablas de origen a Parquet o Iceberg con compactación y considero reservas de capacidad para una concurrencia predecible.

#### Una tabla recibe 2 millones de archivos JSON pequeños por día. ¿Qué recomiendas?

Corregir el productor para que agrupe los registros (buffering de Firehose, escrituras más grandes), añadir un paso de compactación que convierta cada día en unos pocos archivos Parquet (job de Glue o `CTAS`) y consultar la tabla compactada; conservar el JSON en bruto solo como archivo histórico.

#### ¿Cómo consultas el estado más reciente de una tabla que recibe registros de CDC?

O mantengo una tabla Iceberg con `MERGE` que aplica los cambios (lo más limpio), o, sobre una tabla de cambios de solo inserción, uso `ROW_NUMBER()` por clave ordenado por la marca del cambio y me quedo con la última fila no borrada en una vista.

```sql
SELECT * FROM (
  SELECT *, row_number() OVER (PARTITION BY customer_id ORDER BY change_ts DESC) AS rn
  FROM raw.customer_changes
) WHERE rn = 1 AND op <> 'D';
```

#### ¿Cómo le explicarías Athena a una persona de negocio?

Permite al equipo hacer preguntas en SQL directamente sobre los archivos que la empresa ya guarda en S3, sin montar ni pagar servidores, pagando solo por los datos que lee cada pregunta.

#### ¿Cómo migras reportes de un SQL Server on-premises a Athena?

Exporto las tablas a S3 como Parquet (DMS o exportaciones), defino tablas de Glue o Iceberg, traduzco el T-SQL a SQL de Trino (funciones, manejo de fechas, `TOP` a `LIMIT`, sin `PIVOT`), recreo las vistas, valido los resultados comparando agregados y conecto la herramienta de BI con el driver.

#### Un equipo necesita acceso SQL ad hoc a un data lake de 50 TB con un control de presupuesto estricto. ¿Qué montas?

Permisos de Lake Formation por dominio, un workgroup por equipo con límites por consulta, tablas Parquet o Iceberg particionadas por fecha, vistas que imponen filtros de partición, reutilización de resultados, documentación de las tablas e informes mensuales de bytes escaneados por equipo.

#### ¿Cómo construirías dashboards casi en tiempo real sobre Athena?

Envío los eventos con Firehose a S3 en Parquet con buffers cortos, particiono por fecha y hora con proyección, construyo cada pocos minutos tablas agregadas pequeñas con `INSERT INTO` programado o `MERGE` sobre Iceberg, y apunto los dashboards a esos agregados; para latencias por debajo del minuto, uso otro almacén como OpenSearch o una base de datos de streaming.
