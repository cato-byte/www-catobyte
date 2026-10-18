## Guía de estudio de Amazon Athena

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de Amazon Athena: unas 200 preguntas](../../images/aws_athena_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre Amazon Athena: cómo funciona el SQL serverless sobre S3, las tablas y los SerDe, las particiones y la proyección de particiones, los formatos de archivo, las tablas Iceberg, `CTAS` y `UNLOAD`, los workgroups y el control de costos, la optimización del rendimiento, las consultas federadas, la seguridad y la resolución de problemas. Las respuestas reflejan el servicio en 2026.

La guía sigue una ruta de aprendizaje en cinco etapas. Cada sección se divide en unidades cortas: objetivos de aprendizaje, una explicación del concepto y un ejemplo resuelto, luego preguntas (primero de memoria, después de aplicación), un reto práctico e ideas clave. Para **aprender**, lee cada unidad de principio a fin. Para **repasar**, cambia al modo repaso o usa "Ir a las preguntas", marca las respuestas que quieras volver a ver y prueba un repaso mixto entre secciones.

<!-- QA -->
<!-- stage: Fundamentos -->

### Fundamentos

<!-- unit: SQL serverless sobre S3 -->

<!-- goals -->

- Explicar qué es Athena, qué motor usa y para qué sirve.
- Describir schema on read y qué te quita de encima el modelo serverless.

<!-- concept -->

La mayoría de empresas ya guarda sus datos crudos como archivos en S3. Athena permite consultarlos con SQL sin cargarlos antes en ningún lado. Dos ideas lo hacen posible. Schema on read: una tabla es solo una descripción sobre archivos, aplicada al consultar, así cualquier herramienta puede escribirlos. Serverless: AWS opera un motor compartido basado en Trino, sin cluster que dimensionar ni mantener ocioso.

La contrapartida es que el motor solo puede ser tan eficiente como los archivos que le das.

<!-- example -->

```sql
-- files written by Firehose; no load step, just a table definition
SELECT status, count(*) AS requests
FROM logs.alb_access
WHERE day = '2026-10-17'
GROUP BY status
ORDER BY requests DESC;
```

#### ¿Qué es Amazon Athena?

Un servicio de consultas interactivas serverless que permite analizar datos directamente en Amazon S3 (y en otros orígenes mediante conectores) con SQL estándar. No hay infraestructura que administrar: defines tablas sobre tus datos, ejecutas consultas y pagas por los datos escaneados o por capacidad reservada.

#### ¿Qué motor usa Athena?

La versión 3 del motor SQL de Athena se basa en Trino (antes PrestoSQL) con mejoras propias de AWS, y el DDL usa una sintaxis compatible con Hive. Athena también ofrece Apache Spark mediante los notebooks de Athena para cargas PySpark.

#### ¿Cuáles son los casos de uso típicos de Athena?

Análisis ad hoc de data lakes, consulta de logs (CloudTrail, VPC Flow Logs, ALB, CloudFront, logs de acceso de S3), ELT ligero con `CTAS` e `INSERT INTO`, alimentar herramientas de BI como QuickSight, explorar datos antes de construir pipelines y consultar tablas Iceberg en un lakehouse.

#### ¿Qué significa "serverless" en Athena?

No hay clusters que dimensionar, arrancar o parchar: AWS opera un motor de consultas compartido y multiinquilino, asigna recursos por consulta y pagas por consulta (o por capacidad reservada). No hay nada corriendo cuando no consultas.

#### ¿Qué significa "esquema al leer" (schema on read) en Athena?

El esquema se aplica cuando se leen los datos, no cuando se escriben: los archivos de S3 los puede escribir cualquier herramienta, y la definición de la tabla le dice a Athena cómo interpretarlos al consultar. Es flexible, pero los archivos defectuosos solo aparecen como errores o `NULL` al consultarlos.

#### ¿Qué servicios de AWS suelen alimentar de datos a Athena?

Kinesis Data Firehose (flujos hacia S3), AWS Glue (ETL y catálogo), AWS DMS (replicación de bases de datos a S3), los servicios de AWS que escriben logs en S3, S3 Inventory y las aplicaciones que escriben archivos directamente.

#### ¿Cómo le explicarías Athena a una persona de negocio?

Permite al equipo hacer preguntas en SQL directamente sobre los archivos que la empresa ya guarda en S3, sin montar ni pagar servidores, pagando solo por los datos que lee cada pregunta.

<!-- challenge -->

Un equipo pregunta si Athena puede reemplazar su job nocturno que carga logs de S3 en una base de datos solo para unas pocas consultas semanales. ¿Qué respondes?

<!-- solution -->

Probablemente sí: define una tabla sobre los logs y consúltalos en su sitio, pagando solo cuando corren las consultas. Convierte los logs a Parquet particionado si las consultas semanales escanean mucho, para mantener bajo el costo.

<!-- takeaways -->

- Athena consulta archivos en S3 directamente con SQL.
- Schema on read: las tablas describen archivos; no se carga nada.
- Serverless significa sin clusters, pero la organización de archivos sigue importando.

<!-- unit: Precios y ejecución de consultas -->

<!-- goals -->

- Explicar cómo se factura Athena y por qué el formato decide el costo.
- Seguir una consulta desde su envío hasta los resultados y conocer los límites.

<!-- concept -->

El precio por defecto de Athena es por byte escaneado, lo que liga el costo a cuánto de cada archivo debe leer una consulta. Los formatos que permiten saltar columnas y grupos de filas reducen costo y tiempo. Cada consulta sigue el mismo camino: cola, planificación con los metadatos del catálogo, escaneo en paralelo y resultados escritos en S3.

Las cuotas de concurrencia y un timeout acotan ese camino, así que consultas muy grandes o muy numerosas necesitan otro diseño, no solo paciencia.

<!-- example -->

| Los mismos 100 GB de eventos | Bytes escaneados para 3 columnas | Costo aprox. a 5 USD/TB |
|---|---|---|
| CSV sin comprimir | 100 GB | 0,50 USD |
| Parquet + Snappy | ~4 GB | 0,02 USD |

#### ¿Cómo se cobra Athena?

Por defecto, por terabyte de datos escaneados (unos 5 USD por TB en muchas regiones), con un mínimo de 10 MB por consulta, redondeado al megabyte. Las sentencias DDL y las consultas fallidas no se cobran. Las reservas de capacidad ofrecen en cambio un precio fijo por DPU-hora. El almacenamiento y las solicitudes de S3 y el uso del Glue Data Catalog se facturan aparte.

#### ¿Por qué importa tanto el formato de los datos para el costo de Athena?

Porque pagas por byte escaneado. Los formatos columnares y comprimidos (Parquet, ORC) permiten que Athena lea solo las columnas que necesita la consulta y salte bloques con las estadísticas, lo que suele reducir los datos escaneados un 90 % o más frente a CSV o JSON sin comprimir.

#### ¿Adónde van los resultados de las consultas?

A una ubicación de resultados en S3 (definida por workgroup o por consulta) como un archivo CSV más un archivo de metadatos, o al almacenamiento administrado de resultados que Athena conserva por un tiempo limitado. Los resultados se pueden cifrar y conviene una regla de ciclo de vida que borre los archivos viejos.

#### ¿Cuál es el ciclo de vida de una consulta en Athena?

La consulta se envía (`QUEUED`), se planifica con los metadatos del catálogo y el descarte de particiones, se ejecuta en paralelo en el cómputo administrado de Athena leyendo de S3 (`RUNNING`) y termina como `SUCCEEDED`, `FAILED` o `CANCELLED`, con los resultados escritos en la ubicación de resultados.

#### ¿Qué límites de Athena conviene conocer?

Cuotas por cuenta de consultas DML y DDL activas a la vez, un timeout de consulta (30 minutos por defecto para DML, ajustable), la longitud del texto de la consulta, el número de particiones que puede añadir una sola consulta, y las tasas de solicitudes de S3 por prefijo, que pueden frenar las lecturas muy paralelas.

<!-- challenge -->

Un dashboard corre una consulta cada minuto sobre una tabla CSV de 2 TB. Estima el costo mensual de escaneo y nombra el primer arreglo.

<!-- solution -->

Unos 2 TB × 43.200 consultas ≈ 86 PB escaneados, cerca de 430.000 USD al mes. Convertir a Parquet particionado y filtrar por fecha para que cada consulta escanee megabytes; luego cachear resultados o pre-agregar.

<!-- takeaways -->

- Pagas por byte escaneado, así que la organización es costo.
- Las consultas hacen cola, se planifican, escanean en paralelo y escriben en S3.
- Cuotas y timeouts limitan lo que puede hacer una consulta.

<!-- unit: Athena entre los servicios analíticos de AWS -->

<!-- goals -->

- Comparar Athena con Redshift, Redshift Spectrum y EMR.
- Elegir el motor adecuado para una carga.

<!-- concept -->

AWS ofrece varias formas de correr SQL sobre el mismo lake, y difieren en quién posee el cómputo y qué tan estable es la carga. Athena encaja con consultas intermitentes, ad hoc y exploratorias porque solo pagas al consultar. Un warehouse encaja con BI estable y de alta concurrencia porque su cómputo siempre está listo y afinado. Los clusters propios encajan con equipos que necesitan control total de motores y configuración.

Muchas arquitecturas usan más de uno sobre un catálogo compartido.

<!-- example -->

| Carga | Buena opción |
|---|---|
| Analistas exploran logs unas veces al día | Athena |
| 300 usuarios de dashboards todo el día, sub-segundo | Redshift |
| Unir tablas del warehouse con historia en S3 | Redshift Spectrum |
| Jobs Spark propios con configuraciones afinadas | EMR |

#### ¿Cómo se compara Athena con Amazon Redshift?

Athena es serverless y consulta los datos en su lugar en S3, ideal para cargas ad hoc, intermitentes o exploratorias, pagando por consulta. Redshift es un data warehouse (aprovisionado o serverless) optimizado para analítica compleja, frecuente y de alta concurrencia sobre datos cargados en su almacenamiento administrado, con funciones como vistas materializadas y gestión de cargas. Muchas arquitecturas usan ambos.

#### ¿Cómo se compara Athena con Redshift Spectrum?

Ambos consultan datos de S3 a través del Glue Data Catalog. Spectrum se ejecuta desde un cluster de Redshift y permite unir datos de S3 con tablas de Redshift; Athena es independiente y serverless. Spectrum es útil cuando el warehouse ya existe.

#### ¿Cómo se compara Athena con ejecutar Trino o Spark en EMR?

Athena elimina la administración de clusters y cobra por consulta o capacidad, pero da menos control sobre la configuración y los recursos. EMR sirve para cargas muy grandes y estables, configuraciones a medida o herramientas más allá de SQL.

<!-- challenge -->

Una empresa usa Athena para todo, incluida una herramienta de BI con 200 usuarios concurrentes, y choca a diario con los límites de concurrencia. ¿Qué propones?

<!-- solution -->

Mover la carga estable de BI a un warehouse (Redshift) o a reservas de capacidad de Athena, y dejar Athena on-demand para el trabajo ad hoc y exploratorio. Las tablas pre-agregadas ayudan en ambos casos.

<!-- takeaways -->

- Athena encaja con consultas intermitentes y ad hoc sobre S3.
- Los warehouses encajan con BI estable y de alta concurrencia.
- EMR encaja con equipos que necesitan control total.

<!-- unit: Trabajar con Athena -->

<!-- goals -->

- Usar workgroups, interfaces y consultas guardadas en el día a día.
- Saber dónde viven los metadatos y qué puede escribir Athena.

<!-- concept -->

Athena casi no guarda nada. Las definiciones de tablas viven en el Glue Data Catalog, datos y resultados en S3 y la configuración en workgroups. Eso explica su comportamiento: borrar una tabla deja los archivos, dos motores pueden compartir un catálogo y un workgroup decide dónde van los resultados y quién paga.

Se puede escribir, pero en tablas estilo Hive solo se agregan archivos. Transacciones, updates y deletes requieren un formato de tabla como Iceberg.

<!-- example -->

```bash
aws athena start-query-execution \
  --work-group analytics \
  --query-string "SELECT count(*) FROM logs.alb_access WHERE day = '2026-10-17'"
```

#### ¿Qué es un workgroup?

Una forma de separar usuarios, equipos o aplicaciones: cada workgroup tiene su propia ubicación de resultados, ajustes de cifrado, versión del motor, límites de uso de datos, métricas de CloudWatch e historial de consultas, e IAM puede controlar quién usa cada workgroup.

#### ¿Cuáles son las principales interfaces de Athena?

El editor de consultas de la consola, la AWS CLI y los SDK (`StartQueryExecution`, `GetQueryExecution`, `GetQueryResults`), los drivers JDBC y ODBC para herramientas de BI y SQL, los notebooks de Athena para Spark, y las integraciones con QuickSight, Glue, Step Functions y Airflow.

#### ¿Qué son las consultas guardadas del editor de Athena?

Consultas con nombre guardadas por workgroup que los usuarios pueden reutilizar y compartir, útiles para análisis recurrentes, aunque para el SQL de producción es mejor el control de versiones en Git.

#### ¿Qué son las versiones del motor de Athena y cómo se actualizan?

Athena hace evolucionar su motor por versiones (la v3 es la actual); los workgroups pueden elegir las actualizaciones automáticas o una versión concreta. Las actualizaciones pueden cambiar el comportamiento de funciones o el manejo de tipos, así que prueba las consultas críticas antes de cambiar.

#### ¿Dónde guarda Athena las definiciones de las tablas?

En el AWS Glue Data Catalog (por defecto), en un Hive metastore externo o en otros catálogos registrados como orígenes de datos (conectores federados, Redshift, catálogos de S3 Tables).

#### ¿Athena es ACID?

En las tablas al estilo Hive, no: las consultas leen los archivos que existan, y las escrituras añaden archivos sin transacciones. En las tablas Apache Iceberg, sí: Athena admite `INSERT`, `UPDATE`, `DELETE` y `MERGE` ACID con aislamiento por snapshots y viaje en el tiempo.

#### ¿Puede Athena escribir datos?

Sí: `CTAS`, `INSERT INTO`, `UNLOAD` y DML completo (`UPDATE`, `DELETE`, `MERGE`) sobre tablas Iceberg. Sobre las tablas al estilo Hive solo puede añadir archivos nuevos.

<!-- challenge -->

Un usuario borra una tabla por error y entra en pánico. ¿Qué pasó con los datos y cómo restauras la tabla?

<!-- solution -->

Los datos siguen en S3, porque las tablas de Athena son externas. Recrea la tabla desde su DDL (por ejemplo desde el control de versiones o un `SHOW CREATE TABLE` en otro entorno) y vuelve a agregar las particiones.

<!-- takeaways -->

- Metadatos en Glue, datos y resultados en S3, configuración en workgroups.
- Borrar una tabla externa deja los archivos.
- Las escrituras ACID necesitan tablas Iceberg.

### Tablas, DDL y SerDe

<!-- unit: Tablas externas y el catálogo -->

<!-- goals -->

- Crear e inspeccionar tablas externas y vistas.
- Elegir tipos de datos y cambiar columnas con seguridad.

<!-- concept -->

Una tabla de Athena es un contrato entre una ubicación en S3 y un esquema. Crearla escribe solo metadatos; los archivos pueden existir ya o llegar después. Esa separación hace las tablas baratas de crear y recrear, y vuelve el DDL tu herramienta principal para corregir desajustes.

Las vistas agregan una capa de lógica sin guardar datos, útil para definiciones compartidas, pero cada consulta paga el escaneo completo de las tablas de abajo.

<!-- example -->

```sql
CREATE EXTERNAL TABLE sales.orders (
  order_id bigint, customer_id bigint, amount decimal(12,2), created_at timestamp
)
PARTITIONED BY (dt string)
STORED AS PARQUET
LOCATION 's3://lake/sales/orders/';
```

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

#### ¿Qué hace `SHOW CREATE TABLE`?

Muestra el DDL de una tabla, útil para copiar definiciones entre entornos o revisar el SerDe y las propiedades.

#### ¿Qué es una vista en Athena?

Una consulta guardada (`CREATE VIEW`) en el catálogo que se consulta como una tabla. No guarda datos, así que cada consulta lee las tablas subyacentes y se factura en consecuencia.

#### ¿Qué tipos de datos admite Athena?

`boolean`, `tinyint`, `smallint`, `int`, `bigint`, `double`, `float`, `decimal(p,s)`, `char`, `varchar`, `string`, `binary`, `date`, `timestamp`, y los tipos complejos `array`, `map` y `struct`.

#### ¿Cómo se cambian las columnas de una tabla?

Con `ALTER TABLE … ADD COLUMNS`, `REPLACE COLUMNS` o `CHANGE COLUMN` (el comportamiento depende del formato), o recreando la tabla. En Iceberg, `ALTER TABLE … ADD COLUMNS`, `DROP COLUMN` y `RENAME COLUMN` son operaciones seguras sobre los metadatos.

<!-- challenge -->

Los montos se guardan como `double` y finanzas ve errores de redondeo en los totales. ¿Qué cambias?

<!-- solution -->

Guardar el dinero como `decimal(p,s)` en vez de `double`. Recrear la tabla (o escribir una versión nueva en Parquet con CTAS casteando a decimal), porque cambiar tipos in situ sobre archivos existentes no es confiable.

<!-- takeaways -->

- Las tablas son metadatos sobre ubicaciones de S3.
- Las vistas comparten lógica pero no guardan nada.
- Usa `decimal` para el dinero.

<!-- unit: Leer formatos de texto con SerDes -->

<!-- goals -->

- Elegir el SerDe adecuado para CSV, archivos delimitados y logs.
- Configurar encabezados, delimitadores y parseo con regex.

<!-- concept -->

Los archivos de texto no traen esquema, así que Athena necesita instrucciones para separarlos en columnas. Un SerDe es ese conjunto de instrucciones. El predeterminado maneja texto delimitado simple rápido; otros manejan CSV con comillas, expresiones regulares y formatos de logs específicos. Elegir mal rara vez falla con ruido: los valores se corren o quedan en `NULL`.

Para los logs de servicios de AWS, AWS publica DDL listo, que suele ser el camino más rápido.

<!-- example -->

```sql
CREATE EXTERNAL TABLE raw.partners (id string, name string, city string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES ('separatorChar' = ',', 'quoteChar' = '"')
LOCATION 's3://landing/partners/'
TBLPROPERTIES ('skip.header.line.count' = '1');
```

#### ¿Qué es un SerDe?

Un serializador/deserializador que le dice a Athena cómo leer y escribir un formato: `LazySimpleSerDe` para texto delimitado, `OpenCSVSerDe` para CSV con comillas, `JsonSerDe` (Hive u OpenX) para JSON, `RegexSerDe` y `GrokSerDe` para logs, y lectores nativos para Parquet, ORC y Avro.

#### ¿Cuándo usar `OpenCSVSerDe` en lugar de `LazySimpleSerDe`?

Cuando los campos del CSV van entre comillas y pueden contener comas. `OpenCSVSerDe` maneja las comillas, pero trata todas las columnas como texto salvo que se conviertan los tipos, y tiene limitaciones con algunos tipos; `LazySimpleSerDe` es más rápido para archivos delimitados sencillos.

#### ¿Cómo se omite la fila de encabezado en archivos CSV?

Con la propiedad de tabla `'skip.header.line.count'='1'`.

#### ¿Cómo se leen archivos con un delimitador propio?

Con `ROW FORMAT DELIMITED FIELDS TERMINATED BY '|'` (o `\t` para TSV), con las opciones `ESCAPED BY` y `LINES TERMINATED BY` cuando haga falta.

#### ¿Cómo se consultan datos usando una expresión regular?

Definiendo una tabla con `RegexSerDe` y una propiedad `input.regex` con grupos de captura para cada columna, útil para logs de formato fijo; para análisis puntuales, usa `regexp_extract` sobre una sola columna de texto.

#### ¿Cómo se consultan los logs de servicios de AWS con Athena?

Creando tablas con el DDL documentado para cada tipo de log (CloudTrail, VPC Flow Logs, ALB, CloudFront, logs de acceso de S3), idealmente con proyección de particiones por fecha y región, y consultándolas con SQL para investigar eventos de seguridad, tráfico y errores.

<!-- challenge -->

Un CSV tiene nombres como `"Pérez, Ana"` y la columna de ciudad muestra `" Ana"`. ¿Qué está mal y qué cambias?

<!-- solution -->

La tabla usa `LazySimpleSerDe`, que corta en cada coma, incluidas las que van entre comillas. Usa `OpenCSVSerDe` con el carácter de comillas configurado y luego castea las columnas no texto, porque lee todo como string.

<!-- takeaways -->

- Un SerDe le dice a Athena cómo parsear un formato.
- El CSV con comillas necesita `OpenCSVSerDe`.
- Un SerDe equivocado corre los valores en silencio.

<!-- unit: JSON y datos anidados -->

<!-- goals -->

- Leer archivos JSON y JSON guardado como texto en Athena.
- Aplanar arreglos anidados con `UNNEST`.

<!-- concept -->

Los datos semiestructurados llegan de dos formas: archivos con un objeto JSON por línea y JSON guardado como string dentro de otra columna. El primero se mapea con un SerDe a columnas, incluidos arreglos y structs. El segundo queda como string del que extraes al consultar.

Los arreglos convierten una fila en muchas. `UNNEST` lo hace explícito, lo que importa para conteos correctos: un pedido con tres ítems se vuelve tres filas.

<!-- example -->

```sql
SELECT o.order_id, i.sku, i.qty
FROM raw.orders o
CROSS JOIN UNNEST(o.items) AS t(i)
WHERE json_extract_scalar(o.metadata, '$.channel') = 'web';
```

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

<!-- challenge -->

Tras un `UNNEST` de ítems, el ingreso total se duplica. ¿Qué salió mal?

<!-- solution -->

El monto del pedido se repite en cada fila de ítem, así que sumarlo tras el unnest lo multiplica. Suma valores a nivel de ítem (precio × cantidad), o agrega los montos del pedido antes de expandir.

<!-- takeaways -->

- Los SerDes de JSON mapean objetos a columnas y structs.
- El JSON en strings se consulta con funciones JSON.
- `UNNEST` multiplica filas; agrega en consecuencia.

<!-- unit: Schema on read en la práctica -->

<!-- goals -->

- Diagnosticar desajustes entre archivos y esquemas de tabla.
- Usar pseudocolumnas para inspeccionar los archivos de origen.

<!-- concept -->

Como el esquema se aplica al leer, tabla y archivos pueden distanciarse sin que nadie lo note hasta que una consulta devuelve `NULL` o falla. Cómo empareja columnas Athena define qué tan tolerante es: Parquet empareja por nombre y los formatos de texto por posición, así que agregar una columna en medio rompe las tablas de texto pero no las de Parquet.

Cuando algo se ve raro, las pseudocolumnas te dicen de qué archivo vino cada fila.

<!-- example -->

```sql
SELECT "$path", count(*) AS bad_rows
FROM raw.events
WHERE user_id IS NULL
GROUP BY "$path"
ORDER BY bad_rows DESC;
```

#### ¿Qué pasa si los datos no coinciden con el esquema de la tabla?

Athena aplica el esquema al leer: los valores que no encajan suelen convertirse en `NULL` o causan errores como `HIVE_BAD_DATA` (por ejemplo un texto en una columna entera, o un tipo de columna Parquet distinto del tipo de la tabla).

#### ¿Puede Athena manejar la evolución del esquema?

En Parquet, añadir columnas al final y leer por nombre funciona; renombrar o cambiar tipos es riesgoso. En CSV las columnas son posicionales, así que solo es seguro añadir columnas al final. Las tablas Iceberg admiten una evolución de esquema correcta (añadir, borrar, renombrar, reordenar, ampliar tipos).

#### ¿Cómo mapea Athena las columnas de Parquet: por nombre o por posición?

Por nombre, por defecto, en Parquet, así que el orden de las columnas de la tabla no tiene que coincidir con el de los archivos. CSV y otros formatos de texto mapean por posición.

#### ¿Cómo se consultan solo ciertos archivos de una ubicación?

Usando la pseudocolumna `"$path"` (la ruta S3 del archivo de cada fila) en un `WHERE`, que también ayuda a depurar qué archivo contiene datos malos.

```sql
SELECT "$path", count(*) FROM raw.app_events_csv GROUP BY 1 ORDER BY 2 DESC;
```

#### ¿Qué otras pseudocolumnas existen?

`"$path"`, `"$file_size"` y `"$file_modified_time"` describen el archivo de origen de cada fila, útiles para el linaje, la depuración y el procesamiento incremental.

<!-- challenge -->

Un productor agregó una columna en medio de su exportación CSV. Desde entonces varias columnas tienen valores equivocados. ¿Qué haces?

<!-- solution -->

CSV empareja por posición, así que todas las columnas posteriores a la nueva se corrieron. Actualiza la definición con el nuevo orden para los archivos nuevos y separa archivos viejos y nuevos en tablas o particiones distintas con sus esquemas, o convierte ambos a Parquet.

<!-- takeaways -->

- Los desajustes de esquema aparecen como `NULL` o errores de parseo.
- Parquet empareja por nombre; los formatos de texto por posición.
- `"$path"` encuentra los archivos detrás de filas sospechosas.

<!-- stage: Organización de los datos -->

### Particiones y proyección de particiones

<!-- unit: Particionado y pruning -->

<!-- goals -->

- Elegir columnas y granularidad de partición.
- Escribir filtros que realmente poden particiones.

<!-- concept -->

Particionar reparte los archivos de una tabla en carpetas según el valor de una columna, así una consulta que filtra por esa columna lee solo las carpetas que coinciden. Es la mayor palanca sobre el tamaño del escaneo, pero solo si las consultas filtran directamente por la columna de partición y las particiones no son ni muy pequeñas ni demasiadas.

Demasiadas particiones diminutas trasladan el costo del escaneo a la planificación y el listado. El bucketing es el complemento: organiza los archivos dentro de una partición por una columna de alta cardinalidad.

<!-- example -->

```sql
-- prunes: compares the partition column directly
SELECT count(*) FROM logs.events WHERE dt BETWEEN '2026-10-01' AND '2026-10-07';
-- does not prune: function applied to the partition column
SELECT count(*) FROM logs.events WHERE date(dt) >= date '2026-10-01';
```

#### ¿Qué es particionar en Athena?

Organizar los datos en S3 según los valores de una o más columnas (`s3://bucket/tabla/dt=2026-10-15/`) y declararlas como columnas de partición, para que las consultas que filtran por ellas solo lean las carpetas que coinciden.

#### ¿Qué es el descarte de particiones (partition pruning)?

El motor usa los filtros sobre las columnas de partición para saltarse las particiones que no pueden coincidir, lo que reduce los datos escaneados. Solo funciona cuando el filtro está sobre la propia columna de partición, sin funciones que impidan evaluarlo al planificar.

#### ¿Cuál es una buena estrategia de particionado?

Particionar por las columnas por las que filtran la mayoría de las consultas (normalmente la fecha), con una granularidad que deje cada partición razonablemente grande (al menos decenas de MB, idealmente más), y evitar claves de partición de alta cardinalidad que crean millones de particiones diminutas.

#### ¿Por qué demasiadas particiones pueden empeorar el rendimiento?

La planificación tiene que traer y evaluar los metadatos de las particiones, y cada partición suele implicar listados de S3 y archivos pequeños aparte. Los índices de partición de Glue o la proyección de particiones reducen el costo de planificación.

#### ¿Qué es el bucketing en Athena?

Repartir los datos dentro de las particiones en un número fijo de archivos según el hash de una columna (`CLUSTERED BY (user_id) INTO 32 BUCKETS`), lo que ayuda a las consultas que filtran por esa columna a saltarse archivos. Se usa sobre todo con `CTAS`.

#### ¿Cómo se particiona por fecha cuando los datos traen timestamps?

Derivando al escribir una fecha en texto (o año/mes/día) y guardándola como columna de partición; con Iceberg, usando el particionado oculto `day(event_ts)` para que las consultas filtren directamente por el timestamp.

#### ¿Por qué una consulta puede no descartar particiones aunque filtre por fecha?

El filtro puede aplicar una función a la columna de partición (por ejemplo `date(dt) = …` sobre una columna de texto), comparar con un tipo que obliga a convertir, o filtrar por una columna distinta de la clave de partición. Filtra por la columna de partición con literales del mismo tipo.

<!-- challenge -->

Una tabla está particionada por `customer_id` (2 millones de valores) y `dt`. Las consultas son lentas incluso con filtros. ¿Qué cambias?

<!-- solution -->

Quitar `customer_id` como columna de partición: crea millones de particiones diminutas. Particionar solo por fecha y hacer bucketing u ordenar por `customer_id` dentro de las particiones para que las estadísticas de los archivos sigan saltando datos.

<!-- takeaways -->

- Particiona por las columnas que más filtran las consultas, normalmente la fecha.
- Filtra la columna de partición directamente para podar.
- Demasiadas particiones dañan la planificación; usa bucketing para alta cardinalidad.

<!-- unit: Registrar particiones -->

<!-- goals -->

- Agregar, listar y quitar particiones en el catálogo.
- Saber cuándo funciona `MSCK REPAIR TABLE` y cuándo no.

<!-- concept -->

Las tablas clásicas solo ven las particiones que conoce el catálogo. Las carpetas nuevas en S3 son invisibles hasta que alguien las registra, la razón más común de "los datos están ahí pero la consulta no devuelve nada".

Cómo registrar depende de los nombres de las carpetas. Las rutas estilo Hive `key=value` se descubren automáticamente; cualquier otra cosa necesita ubicaciones explícitas. Quitar una partición también es solo metadatos, así que los archivos se quedan en S3.

<!-- example -->

```sql
ALTER TABLE logs.events ADD IF NOT EXISTS
  PARTITION (dt = '2026-10-17') LOCATION 's3://lake/events/dt=2026-10-17/';
SHOW PARTITIONS logs.events;
```

#### ¿Cómo se añaden particiones?

`ALTER TABLE t ADD PARTITION (dt='2026-10-15') LOCATION 's3://.../dt=2026-10-15/'`, `MSCK REPAIR TABLE` para carpetas al estilo Hive, un crawler de Glue, la API de Glue o la proyección de particiones (sin registro).

#### ¿Qué hace `MSCK REPAIR TABLE`?

Recorre la ubicación de la tabla en S3 buscando carpetas de partición al estilo Hive (`clave=valor`) y añade al catálogo las particiones que faltan. Es lento en tablas con muchas particiones; es mejor añadir las particiones de forma explícita o usar la proyección de particiones.

#### ¿Qué diferencia hay entre rutas de partición al estilo Hive y no Hive?

Las rutas al estilo Hive contienen `clave=valor` (`dt=2026-10-15/`), que entienden `MSCK REPAIR` y los crawlers. Las rutas no Hive (`2026/10/15/`) requieren añadir las particiones de forma explícita con un `LOCATION`, o usar proyección de particiones con una plantilla de ubicación.

#### ¿Cómo se ve qué particiones tiene una tabla?

`SHOW PARTITIONS tabla` lista las particiones registradas (no las proyectadas), y la consola o la API de Glue muestran las ubicaciones y esquemas de las particiones.

#### ¿Cómo se eliminan particiones?

`ALTER TABLE t DROP PARTITION (dt='2026-10-01')` elimina solo los metadatos del catálogo; borra los objetos de S3 por separado si también deben irse los datos.

<!-- challenge -->

Un job nocturno corre `MSCK REPAIR TABLE` sobre una tabla de 50.000 particiones y ahora tarda 40 minutos. ¿Qué sugieres?

<!-- solution -->

Dejar de escanear toda la ubicación: agregar la partición de cada día explícitamente con `ALTER TABLE ADD PARTITION` en el job de carga, o pasar a partition projection para no necesitar registro.

<!-- takeaways -->

- Las particiones no registradas son invisibles para las consultas.
- `MSCK REPAIR` solo entiende rutas estilo Hive y lo escanea todo.
- Quitar particiones borra metadatos, no archivos.

<!-- unit: Partition projection -->

<!-- goals -->

- Configurar partition projection para particiones predecibles.
- Reconocer dónde no encaja la projection.

<!-- concept -->

Registrar particiones es una tarea de mantenimiento y un costo de planificación. Partition projection elimina ambos: en vez de buscar particiones en el catálogo, Athena las calcula a partir de reglas en las propiedades de la tabla, como un rango de fechas y una plantilla de ruta. Los datos nuevos se pueden consultar en cuanto llegan.

Las reglas deben describir la realidad. La projection funciona con valores predecibles como fechas y enumeraciones conocidas, y reemplaza por completo las particiones del catálogo para esa tabla.

<!-- example -->

```sql
ALTER TABLE logs.events SET TBLPROPERTIES (
  'projection.enabled' = 'true',
  'projection.dt.type' = 'date',
  'projection.dt.format' = 'yyyy-MM-dd',
  'projection.dt.range' = '2024-01-01,NOW',
  'storage.location.template' = 's3://lake/events/dt=${dt}/'
);
```

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

#### ¿Se pueden mezclar la proyección de particiones y las particiones del catálogo?

Cuando la proyección está activada, Athena ignora las particiones registradas en el catálogo para esa tabla y solo usa las reglas de proyección. Los otros motores siguen viendo las particiones del catálogo.

<!-- challenge -->

Tras activar la projection, las consultas sobre datos del año pasado no devuelven nada, aunque antes sí. ¿Qué revisas?

<!-- solution -->

Que el rango de projection cubra el año pasado y que la plantilla de ubicación y el formato coincidan con las rutas reales. Con projection activa se ignoran las particiones del catálogo, así que cualquier desajuste oculta datos.

<!-- takeaways -->

- La projection calcula particiones con reglas; no hace falta registrarlas.
- Encaja con valores predecibles como fechas.
- Con projection activa, se ignoran las particiones del catálogo.

### Formatos de archivo y organización de los datos

<!-- unit: Formatos columnares -->

<!-- goals -->

- Explicar por qué Parquet y ORC hacen a Athena más rápido y barato.
- Convertir formatos crudos a columnares con el propio Athena.

<!-- concept -->

Los formatos de filas como CSV y JSON obligan al motor a leer cada byte para encontrar unas pocas columnas. Los formatos columnares guardan cada columna por separado con estadísticas, así una consulta lee solo las columnas que selecciona y salta bloques cuyas estadísticas no coinciden. Por eso la misma consulta puede escanear una cincuentava parte de los bytes.

Convertir es una consulta puntual, y la ganancia se nota en cada consulta posterior, siempre que la gente deje de escribir `SELECT *`.

<!-- example -->

```sql
CREATE TABLE curated.events
WITH (format = 'PARQUET', write_compression = 'ZSTD',
      external_location = 's3://lake/curated/events/', partitioned_by = ARRAY['dt'])
AS SELECT event_id, user_id, event_type, ts, dt FROM raw.events_json;
```

#### ¿Qué formatos de archivo admite Athena?

CSV/TSV y otros textos delimitados, JSON, Parquet, ORC, Avro, Ion, logs con los SerDe Regex o Grok, y los formatos de tabla abiertos Iceberg, Hudi (lectura) y Delta Lake (lectura).

#### ¿Por qué se recomiendan Parquet y ORC?

Son columnares (solo se leen las columnas necesarias), se comprimen por columna y guardan estadísticas (mínimo y máximo por grupo de filas o stripe) que permiten a Athena saltar datos. También admiten predicate pushdown, lo que acelera las consultas y baja el costo.

#### ¿Qué diferencia hay entre Parquet y ORC para Athena?

Ambos son columnares, con estadísticas y compresión, y funcionan bien. Parquet es la opción más común en el ecosistema (Spark, valores por defecto de Iceberg); ORC fue históricamente el favorito de Hive. Elige según los escritores y los otros motores que uses.

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

<!-- challenge -->

Los analistas se quejan de que una tabla Parquet "sigue siendo cara". La consulta principal es `SELECT * FROM events WHERE dt = ...` sobre una tabla de 200 columnas. ¿Qué sugieres?

<!-- solution -->

Seleccionar solo las columnas necesarias; con Parquet el costo baja con cada columna quitada. Ofrecer vistas o tablas curadas más angostas para el uso común y mantener el filtro de fecha para el pruning.

<!-- takeaways -->

- Los formatos columnares leen solo las columnas seleccionadas.
- Las estadísticas permiten saltar bloques.
- `SELECT *` devuelve la mayor parte del ahorro.

<!-- unit: Compresión -->

<!-- goals -->

- Elegir códecs de compresión para archivos columnares y de texto.
- Manejar archivos grandes no divisibles.

<!-- concept -->

Athena factura los bytes comprimidos, así que comprimir es un descuento directo. El códec también afecta el paralelismo: dentro de Parquet u ORC cualquier códec sirve porque el formato divide el archivo en bloques, pero un solo archivo de texto gzip solo puede leerlo un worker de principio a fin.

Por eso conviene columnar con Snappy o ZSTD y, para texto, archivos de tamaño moderado.

<!-- example -->

| Archivo | ¿Divisible para Athena? |
|---|---|
| Parquet con ZSTD | Sí (row groups) |
| `.csv.gz` de 20 GB | No: lo lee un solo worker |
| 200 × `.csv.gz` de 100 MB | En paralelo entre archivos |

#### ¿Qué códecs de compresión funcionan bien?

Snappy y ZSTD para Parquet y ORC (rápidos, divisibles dentro del formato). Para archivos de texto, gzip es común pero no divisible, así que un archivo gzip grande lo lee un solo worker; bzip2 es divisible pero lento.

#### ¿La compresión reduce los costos de Athena?

Sí. Athena cobra sobre los bytes comprimidos escaneados, así que los archivos comprimidos (y la codificación columnar) reducen directamente el costo, además de reducir el almacenamiento en S3.

#### ¿Cómo se maneja un dato que llega como un único archivo gzip enorme?

Como gzip no es divisible, lo lee un solo worker. Divide el archivo antes o durante la ingesta, vuelve a comprimirlo como bzip2 o, mejor, conviértelo a Parquet con un `CTAS` o un job de Glue.

<!-- challenge -->

Un socio envía un `.json.gz` de 30 GB por día y la consulta sobre él supera el timeout. ¿Qué haces?

<!-- solution -->

Gzip no es divisible, así que lo lee un worker. Agregar un paso de ingesta (Glue, Lambda o Firehose) que lo divida y convierta a Parquet particionado con Snappy o ZSTD, y consultar la tabla convertida.

<!-- takeaways -->

- La compresión baja los bytes que pagas.
- Los formatos columnares dividen archivos comprimidos; el gzip de texto no.
- Prefiere Snappy o ZSTD dentro de Parquet u ORC.

<!-- unit: Tamaño y organización de archivos -->

<!-- goals -->

- Mantener los archivos en el rango de tamaño correcto y resolver los archivos pequeños.
- Usar orden y estadísticas para que el motor salte datos.

<!-- concept -->

Cada archivo tiene un costo fijo de apertura, listado y planificación, así que miles de archivos diminutos desperdician casi todo el tiempo de una consulta. Los archivos muy grandes limitan el paralelismo. El rango sano es de unos 128 MB a 1 GB, lo que suele implicar escribir por lotes o compactar después.

Dentro de los archivos, el orden importa. Si los datos están ordenados por una columna filtrada, las estadísticas mín/máx de cada bloque quedan estrechas y el predicate pushdown salta la mayoría de bloques.

<!-- example -->

```sql
-- compact one day of small files into a few sorted Parquet files
INSERT INTO curated.events
SELECT * FROM raw.events WHERE dt = '2026-10-17'
ORDER BY user_id;
```

#### ¿Cuál es el tamaño de archivo ideal para Athena?

Más o menos de 128 MB a 1 GB por archivo. Muchos archivos pequeños (de pocos KB) añaden sobrecarga por archivo y costos de solicitudes a S3; los archivos enormes no divisibles limitan el paralelismo.

#### ¿Cómo se arregla una tabla formada por muchos archivos pequeños?

Compactándolos: ejecutando un `CTAS` o `INSERT INTO` que reescriba los datos en menos archivos y más grandes (con bucketing o un particionado controlado), usando `OPTIMIZE` en las tablas Iceberg, o corrigiendo al productor (lotes más grandes, buffering de Firehose).

#### ¿Cómo ayuda a Athena ordenar los datos?

Cuando los datos están ordenados (o agrupados) por una columna de filtro habitual dentro de los archivos, las estadísticas de Parquet y ORC tienen rangos mínimo/máximo estrechos y se pueden saltar más grupos de filas.

#### ¿Qué es el predicate pushdown en Athena?

Los filtros se empujan al lector de archivos, que usa las estadísticas de Parquet/ORC para saltar grupos de filas o stripes cuyo mínimo/máximo no puede coincidir, así que se leen y descomprimen menos datos.

#### ¿Qué tamaño de grupo de filas es bueno para Parquet?

Normalmente de 128 MB a 512 MB; los grupos grandes comprimen bien y reducen la sobrecarga, pero los muy grandes reducen la eficacia del salto de datos. Escritores como Spark tienen valores por defecto razonables.

#### Una tabla recibe 2 millones de archivos JSON pequeños por día. ¿Qué recomiendas?

Corregir el productor para que agrupe los registros (buffering de Firehose, escrituras más grandes), añadir un paso de compactación que convierta cada día en unos pocos archivos Parquet (job de Glue o `CTAS`) y consultar la tabla compactada; conservar el JSON en bruto solo como archivo histórico.

<!-- challenge -->

Una Lambda escribe un archivo diminuto por evento en S3. Las consultas van lentas y crecen los costos de S3. ¿Qué dos cambios haces?

<!-- solution -->

Agrupar en el productor: enviar los eventos a Firehose con un buffer (por ejemplo 128 MB o 5 minutos) y conversión a Parquet. Luego compactar una vez los datos viejos en archivos grandes y borrar los pequeños.

<!-- takeaways -->

- Apunta a archivos de 128 MB a 1 GB aproximadamente.
- Escribe por lotes o compacta los archivos pequeños.
- Los datos ordenados hacen efectivos estadísticas y pushdown.

### Tablas Iceberg en Athena

<!-- unit: Iceberg en Athena -->

<!-- goals -->

- Explicar qué agrega Iceberg sobre los archivos Parquet.
- Elegir entre tablas Iceberg y tablas estilo Hive.

<!-- concept -->

Las tablas estilo Hive son carpetas de archivos: simples, pero sin transacciones, sin cambios de filas y sin escrituras concurrentes seguras. Iceberg agrega una capa de metadatos que registra exactamente qué archivos forman cada versión de la tabla. Cada escritura se vuelve un commit atómico, y de ahí salen funciones como updates, time travel y cambios de esquema.

Como el formato es abierto, la misma tabla funciona en Spark, Trino, Snowflake y otros, lo que hace de Iceberg la opción por defecto para tablas nuevas del lake que cambian.

<!-- example -->

```sql
CREATE TABLE lake.customers (
  customer_id bigint, email string, country string, updated_at timestamp
)
PARTITIONED BY (country)
LOCATION 's3://lake/iceberg/customers/'
TBLPROPERTIES ('table_type' = 'ICEBERG', 'format' = 'parquet');
```

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

#### Iceberg o tablas al estilo Hive en Athena: ¿cómo eliges?

Iceberg cuando necesitas actualizaciones, borrados, upserts (CDC, borrados por GDPR o habeas data), evolución del esquema, escritores concurrentes o viaje en el tiempo. El Parquet al estilo Hive es más sencillo para datos inmutables de solo inserción escritos por otras herramientas. Los diseños nuevos de lakehouse suelen elegir Iceberg.

#### ¿Pueden otros motores usar las mismas tablas Iceberg?

Sí. Spark en EMR o Glue, Trino, Flink, Snowflake, Databricks y otros pueden leer y escribir las mismas tablas Iceberg mediante el Glue Data Catalog o un catálogo REST de Iceberg, lo que evita quedar atado a un motor.

#### ¿Qué son las S3 Tables?

Table buckets de S3 que guardan tablas Iceberg con mantenimiento integrado (compactación, gestión de snapshots) y una integración de catálogo, que Athena puede consultar y escribir como cualquier otra tabla Iceberg.

#### ¿Qué propiedades de tabla importan para Iceberg en Athena?

`format` (parquet, orc, avro), `write_compression`, `optimize_rewrite_delete_file_threshold`, `vacuum_max_snapshot_age_seconds`, `vacuum_min_snapshots_to_keep` y `vacuum_max_metadata_files_to_keep`, que controlan la organización de los archivos y la retención.

<!-- challenge -->

Una tabla de logs solo de append la lee únicamente Athena y nunca cambia. ¿Deberías pasarla a Iceberg?

<!-- solution -->

No necesariamente. Una tabla Parquet particionada con projection ya funciona bien. Iceberg aporta cuando necesitas cambios de filas, escritores concurrentes, evolución de esquema o particiones, o time travel. Elígelo si esas necesidades son probables pronto.

<!-- takeaways -->

- Iceberg convierte cada escritura en un commit atómico y versionado.
- Habilita updates, deletes, time travel y evolución.
- Parquet simple basta para datos sencillos solo de append.

<!-- unit: Cambiar datos en Iceberg -->

<!-- goals -->

- Aplicar `UPDATE`, `DELETE` y `MERGE` a tablas Iceberg.
- Manejar CDC y borrados por GDPR con escritores concurrentes.

<!-- concept -->

Con Iceberg, los cambios a nivel de fila se vuelven SQL corriente. Athena escribe pequeños archivos de borrado que marcan filas eliminadas en vez de reescribir los de datos, lo que mantiene rápidas las escrituras pero vuelve más lentas las lecturas hasta que una compactación los fusiona.

La concurrencia es optimista: los escritores no bloquean, verifican al hacer commit y reintentan si hay conflicto. Eso sirve para la mayoría de pipelines, siempre que dos jobs no reescriban las mismas particiones a la vez.

<!-- example -->

```sql
MERGE INTO lake.customers t
USING staging.customer_changes s
ON t.customer_id = s.customer_id
WHEN MATCHED AND s.op = 'D' THEN DELETE
WHEN MATCHED THEN UPDATE SET email = s.email, country = s.country, updated_at = s.updated_at
WHEN NOT MATCHED AND s.op <> 'D' THEN INSERT VALUES (s.customer_id, s.email, s.country, s.updated_at);
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

#### ¿Cómo funcionan los borrados a nivel de fila de Iceberg en Athena?

Athena escribe archivos de borrado por posición (merge-on-read) que marcan las filas borradas en lugar de reescribir los archivos de datos. Las lecturas los combinan al vuelo, así que las tablas con muchos borrados necesitan `OPTIMIZE` regularmente para seguir siendo rápidas.

#### ¿Pueden varios escritores modificar una tabla Iceberg a la vez?

Sí, con concurrencia optimista: cada commit comprueba la versión actual de la tabla, y los commits en conflicto fallan y deben reintentarse. Evita muchos escritores concurrentes actualizando las mismas particiones.

#### Los analistas necesitan borrar los datos de clientes concretos por GDPR o habeas data. ¿Cómo lo soportas en Athena?

Guardando los datos en tablas Iceberg, ejecutando `DELETE FROM … WHERE customer_id = …` en las tablas afectadas, y luego `OPTIMIZE` y `VACUUM` para eliminar físicamente los archivos viejos tras el periodo de retención de los snapshots. Con tablas Hive habría que reescribir particiones completas.

#### ¿Cómo consultas el estado más reciente de una tabla que recibe registros de CDC?

O mantengo una tabla Iceberg con `MERGE` que aplica los cambios (lo más limpio), o, sobre una tabla de cambios de solo inserción, uso `ROW_NUMBER()` por clave ordenado por la marca del cambio y me quedo con la última fila no borrada en una vista.

```sql
SELECT * FROM (
  SELECT *, row_number() OVER (PARTITION BY customer_id ORDER BY change_ts DESC) AS rn
  FROM raw.customer_changes
) WHERE rn = 1 AND op <> 'D';
```

<!-- challenge -->

Tras un `DELETE` por GDPR, los datos de la persona siguen en archivos de S3. ¿Por qué y qué completa el borrado?

<!-- solution -->

Los archivos de borrado solo marcan filas; los archivos de datos viejos y los snapshots aún las contienen. Corre `OPTIMIZE` para reescribir los archivos sin esas filas y luego `VACUUM` para expirar snapshots viejos y quitar archivos no referenciados.

<!-- takeaways -->

- Iceberg soporta `UPDATE`, `DELETE` y `MERGE` en Athena.
- Los deletes escriben archivos de borrado; la compactación los aplica.
- Los commits concurrentes se verifican de forma optimista.

<!-- unit: Evolución, time travel y mantenimiento -->

<!-- goals -->

- Evolucionar esquemas y particionado sin reescribir datos.
- Usar time travel, rollbacks y comandos de mantenimiento.

<!-- concept -->

Como Iceberg rastrea las columnas por ID y las particiones como transformaciones de columnas, la forma de la tabla puede cambiar sin tocar los archivos viejos. Las consultas filtran por la columna real y las particiones correctas se podan por detrás.

Cada commit deja un snapshot, lo que da time travel y rollback gratis hasta que el mantenimiento los expira. Ese es el equilibrio a manejar: snapshots y archivos pequeños se acumulan, así que hay que programar compactación y vacuum.

<!-- example -->

```sql
SELECT count(*) FROM lake.customers FOR TIMESTAMP AS OF TIMESTAMP '2026-10-15 08:00:00 UTC';
OPTIMIZE lake.customers REWRITE DATA USING BIN_PACK;
VACUUM lake.customers;
```

#### ¿Qué es el particionado oculto de Iceberg?

Particiones definidas como transformaciones de columnas (`day(event_ts)`, `bucket(16, user_id)`, `truncate(10, sku)`), de modo que las consultas filtran por la columna original (`event_ts`) e Iceberg descarta las particiones automáticamente; los usuarios no necesitan conocer las columnas de partición.

#### ¿Se puede cambiar el particionado de una tabla Iceberg?

Sí. Puedes cambiar la especificación de particiones (por ejemplo de mensual a diaria) sin reescribir los datos viejos; los archivos antiguos conservan la especificación vieja, los datos nuevos usan la nueva y las consultas manejan ambas.

#### ¿Cómo se añade una columna a una tabla Iceberg?

`ALTER TABLE lake.customers ADD COLUMNS (segment string)`. Los archivos existentes no se reescriben; las filas viejas devuelven `NULL` en la nueva columna.

#### ¿Cómo funciona el viaje en el tiempo de Iceberg en Athena?

```sql
SELECT * FROM lake.customers FOR TIMESTAMP AS OF TIMESTAMP '2026-10-15 08:00:00 UTC';
SELECT * FROM lake.customers FOR VERSION AS OF 949530903748831860;
```

También se pueden revisar las tablas de metadatos como `"customers$snapshots"`, `"customers$history"`, `"customers$files"` y `"customers$partitions"`.

#### ¿Cómo se revierte una tabla Iceberg en Athena?

Leyendo la versión anterior con viaje en el tiempo y reescribiéndola (por ejemplo con un `CTAS` desde `FOR VERSION AS OF`), o usando un motor con procedimientos de reversión (`rollback_to_snapshot` de Spark) sobre la misma tabla.

#### ¿Qué hacen `OPTIMIZE` y `VACUUM` en las tablas Iceberg?

`OPTIMIZE tabla REWRITE DATA USING BIN_PACK` compacta los archivos pequeños y fusiona los archivos de borrado con los de datos. `VACUUM` expira los snapshots antiguos y elimina los archivos que ya no se referencian (según las propiedades de retención), liberando almacenamiento.

<!-- challenge -->

Un job malo sobrescribió la mitad de una tabla de clientes a las 09:12. ¿Cómo la restauras con Athena?

<!-- solution -->

Consulta la tabla `FOR TIMESTAMP AS OF` las 09:10 para confirmar el estado bueno y reconstrúyela desde esa versión (por ejemplo CTAS a una tabla nueva y luego intercambiar, o reinsertar las filas viejas). Hazlo antes de que `VACUUM` expire el snapshot.

<!-- takeaways -->

- Particionado oculto e IDs de columna hacen segura la evolución.
- Los snapshots dan time travel y rollback.
- Programa `OPTIMIZE` y `VACUUM` para controlar el crecimiento.

<!-- stage: Construir y consultar -->

### CTAS, INSERT y UNLOAD

<!-- unit: Escribir tablas con CTAS -->

<!-- goals -->

- Crear tablas desde consultas con CTAS en el formato y la organización correctos.
- Trabajar dentro de los límites de CTAS en particiones, archivos y ubicaciones.

<!-- concept -->

CTAS es la principal herramienta de transformación de Athena: una sentencia corre una consulta y escribe el resultado como tabla nueva, eligiendo formato, compresión, particionado y bucketing. Así conviertes archivos crudos en tablas curadas sin otro servicio.

Sus límites moldean los pipelines. Una consulta solo puede escribir un número limitado de particiones y rechaza ubicaciones no vacías, así que los backfills grandes van por lotes y cada ejecución necesita una ubicación nueva o limpia.

<!-- example -->

```sql
CREATE TABLE curated.daily_sales
WITH (format = 'PARQUET', external_location = 's3://lake/curated/daily_sales/v2/',
      partitioned_by = ARRAY['dt'], bucketed_by = ARRAY['store_id'], bucket_count = 8)
AS SELECT store_id, sum(amount) AS revenue, dt
   FROM sales.orders GROUP BY store_id, dt;
```

#### ¿Qué es `CTAS`?

`CREATE TABLE AS SELECT`: crea una tabla nueva a partir de los resultados de una consulta, escribiendo en S3 archivos con el formato, la compresión, el particionado y el bucketing elegidos. Se usa para convertir formatos, construir agregados y materializar transformaciones.

#### ¿Cuáles son los límites de `CTAS` e `INSERT INTO`?

Una sola consulta puede crear o insertar en un número limitado de particiones (100 por consulta en las tablas Hive), así que los backfills grandes necesitan varias sentencias o bucles por rangos de particiones. Las tablas Iceberg no tienen ese límite en particular.

#### ¿Cómo se controla el número de archivos de salida en `CTAS`?

Con `bucketed_by` y `bucket_count`, que fijan el número de archivos por partición, o reduciendo el paralelismo del stage final; si no, Athena escribe tantos archivos como produzcan los workers.

#### ¿Puede un `CTAS` escribir en una ubicación de S3 que ya existe?

No. El `external_location` debe estar vacío, lo que evita sobrescribir datos por error. Borra la ubicación o usa una nueva para las reejecuciones.

#### ¿Cómo se crea una copia vacía del esquema de una tabla?

`CREATE TABLE nueva_t WITH (...) AS SELECT * FROM t WITH NO DATA`, que crea la definición de la tabla sin escribir filas.

<!-- challenge -->

Un CTAS sobre tres años de datos diarios falla porque escribe demasiadas particiones. ¿Cómo lo cargas?

<!-- solution -->

Crear la tabla con CTAS para un primer lote de menos de 100 particiones (por ejemplo tres meses) y agregar el resto con `INSERT INTO ... SELECT` en lotes del mismo tamaño, idealmente con un script.

<!-- takeaways -->

- CTAS escribe resultados de consultas como tabla nueva con formato.
- Los límites de particiones obligan a cargar por lotes.
- CTAS necesita una ubicación de destino vacía.

<!-- unit: ELT idempotente en Athena -->

<!-- goals -->

- Construir pipelines seguros de re-ejecutar con `INSERT INTO`, CTAS o dbt.
- Programar consultas de Athena con servicios de AWS o Airflow.

<!-- concept -->

En tablas estilo Hive, `INSERT INTO` solo agrega archivos, así que correrlo dos veces duplica los datos. Los pipelines son seguros de re-ejecutar cuando cada ejecución es dueña de un tramo, normalmente una partición de fecha, y lo limpia primero. Iceberg elimina el problema con `MERGE` y sobrescrituras, por eso muchos ELT en Athena usan Iceberg para las capas curadas.

La orquestación es solo llamar la API con un calendario, pero dbt agrega pruebas y dependencias encima.

<!-- example -->

```bash
# rerun-safe daily load for a Hive-style table
aws s3 rm --recursive s3://lake/curated/orders/dt=2026-10-17/
aws athena start-query-execution --work-group etl --query-string \
 "INSERT INTO curated.orders SELECT ..., dt FROM raw.orders WHERE dt = '2026-10-17'"
```

#### ¿Qué hace `INSERT INTO` en una tabla al estilo Hive?

Añade archivos nuevos en la ubicación de la tabla (y registra las particiones nuevas). Nunca modifica los archivos existentes, así que volver a ejecutarlo duplica los datos salvo que antes borres los archivos de la partición destino.

#### ¿Cómo se hace idempotente un ELT con Athena?

En las tablas Hive, escribiendo la salida de cada ejecución en una partición y borrando o sobrescribiendo esa partición antes de volver a ejecutar (a menudo escribiendo en una ubicación nueva y cambiando la ubicación de la partición). En las tablas Iceberg, usando `MERGE` o `DELETE` más `INSERT` en la misma lógica, o patrones de sobrescritura con Iceberg.

#### ¿Cómo se programan consultas de Athena?

Con EventBridge Scheduler o Step Functions llamando a `StartQueryExecution`, el `AthenaOperator` de Airflow, dbt con el adaptador dbt-athena, o una función Lambda programada.

#### ¿Se puede usar dbt con Athena?

Sí, con el adaptador dbt-athena: los modelos se materializan como vistas, tablas (`CTAS`), modelos incrementales (`insert_overwrite` por partición, `append` o `merge` sobre Iceberg) y tablas Iceberg, con Glue como catálogo.

#### ¿Cómo construirías un pequeño pipeline ELT solo con Athena?

Tablas raw sobre los archivos de aterrizaje, `CTAS` o `INSERT INTO` (o modelos de dbt-athena) para construir tablas limpias en Iceberg o Parquet, `MERGE` para los upserts, controles de calidad como consultas SQL que hacen fallar el pipeline cuando devuelven filas, y Step Functions o Airflow para programar y ordenar las sentencias.

<!-- challenge -->

Un modelo incremental de dbt-athena agrega filas en cada ejecución y las re-ejecuciones crean duplicados. ¿A qué estrategia cambias?

<!-- solution -->

Usar `insert_overwrite` sobre una partición de fecha (tablas Hive) o `merge` con `unique_key` en tablas Iceberg. Ambas reemplazan los datos afectados al re-ejecutar en vez de agregar.

<!-- takeaways -->

- `INSERT INTO` agrega; re-ejecutar duplica.
- Que cada ejecución sea dueña de un tramo, o usa `MERGE` de Iceberg.
- dbt-athena agrega pruebas y dependencias al ELT en Athena.

<!-- unit: Exportar y parametrizar -->

<!-- goals -->

- Exportar resultados de consultas en formatos útiles.
- Usar consultas parametrizadas con seguridad en aplicaciones.

<!-- concept -->

No todo resultado debe ser una tabla. A veces otro sistema necesita archivos, y `UNLOAD` escribe resultados en el formato elegido sin registrar nada. A veces una persona necesita un único CSV, que la ubicación de resultados ya ofrece.

Las aplicaciones que arman consultas con entradas de usuarios nunca deben concatenar strings; los parámetros mantienen los valores separados del SQL y evitan la inyección.

<!-- example -->

```sql
UNLOAD (SELECT * FROM curated.daily_sales WHERE dt = '2026-10-17')
TO 's3://exports/partner_x/2026-10-17/'
WITH (format = 'PARQUET', compression = 'SNAPPY');

PREPARE sales_by_store FROM SELECT * FROM curated.daily_sales WHERE store_id = ?;
EXECUTE sales_by_store USING 42;
```

#### ¿Qué hace `UNLOAD`?

Escribe los resultados de una consulta en S3 con el formato elegido (Parquet, ORC, Avro, JSON, texto), con particionado y compresión opcionales, sin crear una tabla, lo que es útil para exportar a otros sistemas.

```sql
UNLOAD (SELECT * FROM curated.app_events WHERE dt = '2026-10-15')
TO 's3://exports/app_events/dt=2026-10-15/'
WITH (format = 'PARQUET', compression = 'SNAPPY');
```

#### ¿Cómo se exportan los resultados de una consulta como un solo CSV?

Ejecutando la consulta y descargando el archivo de resultados de la ubicación de resultados (Athena escribe un CSV por consulta), o usando `UNLOAD` con un formato de texto; los resultados muy grandes pueden quedar divididos en varios archivos con `UNLOAD`.

#### ¿Qué son las sentencias preparadas y las consultas parametrizadas?

Sentencias creadas con `PREPARE` (o enviadas con `ExecutionParameters`) que contienen marcadores `?` que se llenan al ejecutar, lo que evita la inyección SQL y permite a las aplicaciones reutilizar el texto de la consulta.

```sql
PREPARE events_by_day FROM
SELECT event_type, count(*) FROM curated.app_events WHERE dt = ? GROUP BY 1;

EXECUTE events_by_day USING '2026-10-15';
```

<!-- challenge -->

Una app interna arma el SQL de Athena concatenando el nombre de tienda que escribe el usuario. ¿Qué riesgo hay y cuál es el arreglo?

<!-- solution -->

Inyección SQL: un nombre manipulado podría cambiar la consulta. Usar consultas parametrizadas (`ExecutionParameters` o prepared statements) y un workgroup y rol IAM limitados a las tablas que la app necesita.

<!-- takeaways -->

- `UNLOAD` exporta resultados como archivos sin tabla.
- Cada consulta también escribe un CSV en la ubicación de resultados.
- Parametriza las consultas construidas con entradas de usuarios.

### Funciones SQL y patrones

<!-- unit: Tipos, fechas y NULL -->

<!-- goals -->

- Manejar fechas, conversiones y `NULL` correctamente.
- Seudonimizar identificadores con hashing.

<!-- concept -->

Muchas respuestas equivocadas en SQL vienen de tres lugares: fechas con el tipo o la zona horaria incorrectos, casts que fallan con valores sucios y `NULL` que desaparecen en silencio de las comparaciones. Los datos del lake suelen estar sucios porque nunca se validaron al escribir, así que las funciones defensivas importan más en Athena que en un warehouse.

El hashing también entra aquí: un hash determinista permite unir por un identificador sin exponerlo.

<!-- example -->

```sql
SELECT
  date_trunc('month', TRY_CAST(order_ts AS timestamp)) AS month,
  count(*) FILTER (WHERE TRY_CAST(amount AS decimal(12,2)) IS NULL) AS bad_amounts,
  to_hex(hmac_sha256(to_utf8(email), to_utf8('salt-from-secrets'))) AS email_key
FROM raw.orders
GROUP BY 1, 3;
```

#### ¿Cómo se trabaja con fechas y horas en Athena?

Con funciones como `current_date`, `date_add('day', -1, current_date)`, `date_diff('day', a, b)`, `date_trunc('month', ts)`, `date_format(ts, '%Y-%m-%d')`, `from_iso8601_timestamp(s)`, `parse_datetime(s, 'yyyy-MM-dd HH:mm')` y `ts AT TIME ZONE 'America/Bogota'`.

#### ¿Cómo se convierten tipos de forma segura?

`TRY_CAST(x AS integer)` devuelve `NULL` en lugar de fallar con valores malos, y `try()` envuelve expresiones que pueden dar error. Úsalos sobre datos de texto en bruto.

#### ¿Cómo se manejan los valores `NULL` en agregaciones y comparaciones?

Las agregaciones ignoran los `NULL` (salvo `count(*)`); las comparaciones con `NULL` devuelven `NULL`, así que usa `IS NULL`, `coalesce`, `IS DISTINCT FROM` para comparar sin problemas con nulos, y ten cuidado con `NOT IN` sobre columnas que contienen nulos.

#### ¿Cómo se hashean valores para seudonimizar?

Con `to_hex(sha256(to_utf8(email)))` (preferiblemente con una sal secreta o un HMAC con `hmac_sha256`), lo que produce seudónimos estables que se pueden seguir uniendo.

<!-- challenge -->

Una consulta `WHERE discount <> 10` pierde las filas donde falta el descuento. ¿Por qué y cómo lo arreglas?

<!-- solution -->

Las comparaciones con `NULL` devuelven `NULL`, así que esas filas se excluyen. Usa `WHERE discount IS NULL OR discount <> 10`, o `coalesce(discount, 0) <> 10` si faltante significa cero.

<!-- takeaways -->

- Usa `TRY_CAST` sobre datos sucios del lake.
- Las comparaciones con `NULL` descartan filas en silencio.
- Los hashes con sal seudonimizan identificadores.

<!-- unit: Patrones analíticos -->

<!-- goals -->

- Deduplicar, rankear y calcular métricas acumuladas con window functions.
- Pivotar datos y comparar tablas.

<!-- concept -->

Unos pocos patrones cubren la mayoría de preguntas analíticas. Las window functions responden preguntas "por grupo" sin colapsar filas: último registro por clave, top N por categoría, totales acumulados. La agregación condicional reemplaza el `PIVOT` que falta. Las operaciones de conjuntos comparan dos versiones de una tabla.

Conocer el patrón importa más que la sintaxis, porque la misma forma se repite entre motores.

<!-- example -->

```sql
WITH ranked AS (
  SELECT *, row_number() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) AS rn
  FROM raw.customer_changes
)
SELECT * FROM ranked WHERE rn = 1;      -- latest version per customer
```

#### ¿Cómo se deduplican filas en Athena?

Con `row_number()` por clave ordenado por una marca de tiempo, quedándose con la primera fila por clave, en una subconsulta o CTE, ya que Athena no admite `QUALIFY`.

#### ¿Cómo se obtienen las N primeras filas por grupo?

Usando `row_number()` o `rank()` por grupo ordenado por la métrica en una subconsulta y filtrando por el rango en la consulta externa; `max_by(x, y)` da el valor de `x` en el máximo de `y` por grupo.

#### ¿Cómo se calcula un total acumulado o un promedio móvil?

Con funciones de ventana: `sum(amount) OVER (PARTITION BY customer ORDER BY dt ROWS UNBOUNDED PRECEDING)` para los totales acumulados y `avg(amount) OVER (ORDER BY dt ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)` para un promedio móvil de 7 filas.

#### ¿Para qué sirven `max_by` y `min_by`?

Para devolver el valor de una columna en la fila donde otra columna es máxima o mínima, por ejemplo el último estado de cada pedido: `max_by(status, updated_at)`, sin una función de ventana.

#### ¿Cómo se pivotan datos en Athena?

Con agregación condicional, porque no existe la palabra `PIVOT`: `sum(CASE WHEN month = 1 THEN amount END) AS ene`, o `map_agg` para construir un mapa clave-valor.

#### ¿Cómo se comparan dos tablas para encontrar diferencias?

Con `EXCEPT` en ambos sentidos (`SELECT * FROM a EXCEPT SELECT * FROM b`) para las diferencias de filas, o un full outer join por clave comparando columnas, útil para validar migraciones.

<!-- challenge -->

Necesitas el país más reciente de cada cliente y su gasto total en una consulta. Escribe su núcleo.

<!-- solution -->

`SELECT customer_id, max_by(country, updated_at) AS country, sum(amount) AS spend FROM orders GROUP BY customer_id`. `max_by` evita un paso de ventana aparte para el último valor.

<!-- takeaways -->

- `row_number()` resuelve deduplicación y top N por grupo.
- La agregación condicional pivota datos.
- `EXCEPT` en ambos sentidos encuentra diferencias entre tablas.

<!-- unit: Arreglos, series y funciones especializadas -->

<!-- goals -->

- Usar funciones de arreglos, mapas y secuencias.
- Aplicar patrones geoespaciales, de muestreo y de reutilización.

<!-- concept -->

La librería de funciones de Trino va mucho más allá del SQL estándar, y los datos del lake la necesitan a menudo: arreglos y mapas desde JSON, calendarios con huecos, coordenadas de apps. Generar una serie de fechas es un truco común para mostrar días sin actividad en vez de omitirlos.

La reutilización completa el kit: las vistas comparten lógica entre consultas y los CTE la organizan dentro de una.

<!-- example -->

```sql
SELECT d AS day, coalesce(count(o.order_id), 0) AS orders
FROM UNNEST(sequence(date '2026-10-01', date '2026-10-31', interval '1' day)) AS t(d)
LEFT JOIN sales.orders o ON date(o.created_at) = d
GROUP BY d ORDER BY d;
```

#### ¿Qué funciones de arreglos y mapas son útiles?

`cardinality`, `contains`, `element_at`, `array_join`, `array_agg`, `filter`, `transform`, `reduce`, `map_keys`, `map_values` y `map_agg`, que permiten trabajar con datos anidados sin desplegarlos.

#### ¿Cómo se genera una serie de fechas en Athena?

Con `sequence` y `UNNEST`: `SELECT d FROM UNNEST(sequence(date '2026-01-01', date '2026-12-31', interval '1' day)) AS t(d)`, útil para llenar huecos en series de tiempo.

#### ¿Cómo se hacen consultas geoespaciales en Athena?

Con funciones geoespaciales como `ST_Point`, `ST_Contains`, `ST_Distance`, `ST_Within`, `ST_GeometryFromText` y `great_circle_distance`, por ejemplo para contar eventos dentro de polígonos.

#### ¿Cómo se toman muestras de datos en Athena?

`TABLESAMPLE BERNOULLI (1)` lee las filas con un 1 % de probabilidad (pero escanea todos los datos), y `TABLESAMPLE SYSTEM (1)` muestrea a nivel de archivo o split, lo que puede reducir los datos escaneados.

#### ¿Cómo se escribe lógica SQL reutilizable en Athena?

Con vistas para la lógica compartida, CTE (`WITH`) para la legibilidad dentro de una consulta, y macros de dbt cuando se usa dbt-athena.

<!-- challenge -->

Un compañero usa `TABLESAMPLE BERNOULLI (1)` para abaratar una consulta exploratoria. ¿Funciona?

<!-- solution -->

Devuelve cerca del 1 % de las filas pero igual escanea todos los datos, así que el costo no baja. Filtra por particiones (por ejemplo un día) o usa `TABLESAMPLE SYSTEM` si aceptas un muestreo aproximado por archivos.

<!-- takeaways -->

- Funciones de arreglos, mapas y JSON manejan los datos anidados del lake.
- `sequence` y `UNNEST` rellenan huecos en series de fechas.
- El muestreo no baja el costo salvo que salte archivos.

### Spark en Athena y notebooks

<!-- unit: Spark serverless en Athena -->

<!-- goals -->

- Explicar qué ofrece Athena para Apache Spark.
- Elegir entre Athena SQL y Athena Spark.

<!-- concept -->

Parte del trabajo no cabe en una sentencia SQL: exploración iterativa, librerías de Python, preparación para machine learning. Athena para Apache Spark da la misma experiencia serverless para PySpark en notebooks, arrancando en segundos sin cluster.

SQL sigue siendo mejor para consultas y reportes; Spark es para lógica que necesita un lenguaje de programación.

<!-- example -->

```python
df = spark.read.table("lake.orders").where("dt >= '2026-10-01'")
features = df.groupBy("customer_id").agg(F.count("*").alias("orders"), F.sum("amount").alias("spend"))
features.write.mode("overwrite").saveAsTable("ml.customer_features")
```

#### ¿Qué es Amazon Athena for Apache Spark?

Una oferta de Spark serverless en Athena en la que ejecutas PySpark y Spark SQL en notebooks o mediante APIs, con un arranque rápido y facturación por DPU-hora, para cargas que necesitan más que SQL.

#### ¿Cuándo usarías Athena Spark en lugar de Athena SQL?

Para transformaciones complejas en Python, preparación para machine learning, exploración iterativa con DataFrames o lógica incómoda en SQL; el SQL sigue siendo más simple y barato para la mayoría de la analítica.

#### ¿Qué lenguajes admiten los notebooks de Athena?

PySpark y Spark SQL (con comandos mágicos), con librerías Python comunes disponibles y la posibilidad de añadir otras a la sesión.

<!-- challenge -->

Una científica de datos quiere preparar features con lógica tipo pandas sobre 300 GB de Parquet. ¿Athena SQL o Athena Spark?

<!-- solution -->

Athena Spark: la lógica es más fácil en PySpark y los datos son demasiado grandes para pandas en una máquina. Los resultados pueden escribirse de vuelta como tablas del catálogo que consulta Athena SQL.

<!-- takeaways -->

- Athena Spark corre PySpark serverless en notebooks.
- SQL para consultas; Spark para lógica programática.
- Ambos comparten el catálogo de Glue.

<!-- unit: Sesiones, facturación y catálogo -->

<!-- goals -->

- Entender cómo se facturan y terminan las sesiones de Spark.
- Leer y escribir tablas del catálogo desde sesiones de Spark.

<!-- concept -->

Una sesión de Spark retiene cómputo mientras está abierta, así que el costo sigue al tiempo de sesión y no a los bytes escaneados. Los timeouts por inactividad terminan las sesiones automáticamente, lo que importa porque los notebooks se quedan abiertos con facilidad.

Las sesiones usan el mismo Glue Data Catalog que SQL, así las tablas escritas desde Spark aparecen en Athena SQL y ambos estilos comparten un lake.

<!-- example -->

| Modelo de facturación | Athena SQL | Athena Spark |
|---|---|---|
| Unidad | Bytes escaneados (o DPU reservadas) | DPU-hora de la sesión |
| Qué mueve el costo | Datos leídos | Duración y tamaño de la sesión |

#### ¿Cómo se facturan las sesiones de Athena Spark?

Por DPU-hora del cómputo de la sesión, con escalado automático de los executors y timeouts de inactividad que terminan la sesión.

#### ¿Cómo accede Athena Spark al Data Catalog?

Las sesiones Spark de Athena usan por defecto el Glue Data Catalog, así que puedes leer y escribir tablas del catálogo (incluidas Iceberg) con Spark SQL o DataFrames.

<!-- challenge -->

El costo mensual de Athena Spark es alto, aunque los notebooks se usan solo unas horas al día. ¿Qué revisas?

<!-- solution -->

Los timeouts de inactividad de las sesiones y si los usuarios las dejan corriendo, además del tamaño en DPU por sesión. Baja el timeout y enseña a los usuarios a cerrar sesiones al terminar.

<!-- takeaways -->

- Las sesiones de Spark se facturan por DPU-hora.
- Los timeouts de inactividad limitan las sesiones olvidadas.
- Spark y SQL comparten el catálogo de Glue.

<!-- stage: Operar Athena -->

### Optimización del rendimiento

<!-- unit: Medir una consulta -->

<!-- goals -->

- Medir los datos escaneados y leer planes de consulta.
- Conocer las palancas que mejoran velocidad y costo.

<!-- concept -->

El tuning empieza midiendo. Cada ejecución registra bytes escaneados y tiempo en cola, planificación y ejecución, y `EXPLAIN ANALYZE` muestra dónde se fue el tiempo. Casi todas las mejoras salen de la misma lista corta: leer menos (columnas, particiones, formatos), mover menos entre workers y evitar pasos de un solo worker.

Un `LIMIT` no es por sí solo un control de costo; solo lo es leer menos datos.

<!-- example -->

```sql
EXPLAIN ANALYZE
SELECT store_id, sum(amount) FROM sales.orders
WHERE dt = '2026-10-17' GROUP BY store_id;
-- check: input bytes per stage, pruned partitions, time per operator
```

#### ¿Cuáles son las principales formas de hacer más rápidas y baratas las consultas de Athena?

Usar formatos columnares con compresión, particionar por los filtros habituales (o con proyección), mantener archivos de 128 MB a 1 GB, seleccionar solo las columnas necesarias, filtrar por las columnas de partición, ordenar o hacer bucketing por los filtros habituales, usar Iceberg con compactación, calcular estadísticas de las tablas y reutilizar resultados.

#### ¿Cómo se ve cuántos datos escaneó una consulta?

En la consola después de ejecutarla, en las estadísticas de `GetQueryExecution` (`DataScannedInBytes`), en las métricas de CloudWatch del workgroup y en la salida de `EXPLAIN ANALYZE` por stage.

#### ¿Qué muestran `EXPLAIN` y `EXPLAIN ANALYZE`?

`EXPLAIN` muestra el plan distribuido o lógico sin ejecutar la consulta: lecturas, filtros empujados, joins y su distribución. `EXPLAIN ANALYZE` ejecuta la consulta e informa las filas, los datos leídos y el tiempo reales por stage, lo que muestra dónde se va el tiempo.

#### ¿Cómo afecta `LIMIT` al costo?

En las tablas al estilo Hive, un `LIMIT` sin filtros puede detenerse antes pero aun así escanear muchos archivos; no garantiza un costo bajo. Los filtros de partición son la forma confiable de limitar lo escaneado.

<!-- challenge -->

Una consulta escanea 800 GB aunque filtra un día. ¿Qué buscas en `EXPLAIN`?

<!-- solution -->

Si el filtro de partición aparece en el escaneo (pruning), o si se aplica después del escaneo por una función o un desajuste de tipo sobre la columna de partición. Revisa también si la tabla está particionada o proyectada.

<!-- takeaways -->

- Mide primero bytes escaneados y tiempos de cada etapa.
- `EXPLAIN ANALYZE` muestra adónde van tiempo y datos.
- `LIMIT` no garantiza escanear menos.

<!-- unit: Joins y distribución de datos -->

<!-- goals -->

- Escribir joins que el optimizador pueda ejecutar con eficiencia.
- Manejar el skew y la falta de estadísticas.

<!-- concept -->

Los joins distribuidos o bien hacen broadcast de una tabla pequeña a cada worker o bien redistribuyen ambos lados por clave. El optimizador elige según estadísticas; sin ellas, se apoya en el orden en que escribiste, así que la tabla más grande va primero y la más pequeña al final.

El skew rompe ambas estrategias: cuando unas pocas claves concentran casi todas las filas, unos pocos workers reciben casi todo el trabajo. Filtrar o separar las claves calientes suele ayudar más que cualquier ajuste.

<!-- example -->

```sql
-- largest table first, small dimension last (broadcast-friendly)
SELECT f.order_id, d.region
FROM sales.orders f
JOIN ref.stores d ON f.store_id = d.store_id
WHERE f.dt = '2026-10-17';
```

#### ¿En qué orden se deben poner las tablas en un join?

El motor v3 tiene un optimizador basado en costos que puede reordenar los joins cuando hay estadísticas de las tablas en el catálogo de Glue. Sin estadísticas, pon la tabla más grande primero (a la izquierda) y las más pequeñas a la derecha, porque el lado derecho se construye en memoria y se distribuye a los workers.

#### ¿Qué tipos de distribución de join existen?

Los broadcast joins envían la tabla pequeña del lado derecho a todos los workers (rápido si es pequeña); los joins particionados reparten ambos lados por hash entre los workers (necesario con dos tablas grandes). El optimizador elige según las estadísticas.

#### ¿Cómo ayudan a Athena las estadísticas de las tablas?

Las estadísticas de columnas guardadas en el catálogo de Glue (calculadas por Glue) permiten que el optimizador basado en costos elija el orden y la distribución de los joins, mejorando las consultas complejas sin cambiar el código.

#### ¿Qué impacto tiene el data skew en los joins y agregaciones de Athena?

Unas pocas claves con la mayoría de las filas sobrecargan a workers individuales y pueden causar errores de "exhausted resources". Filtra las claves calientes (a menudo los nulos), trátalas aparte o usa agregaciones aproximadas.

<!-- challenge -->

Un join por `customer_id` falla con "exhausted resources", y el 30 % de las filas tiene `customer_id = 0` (invitados). ¿Qué haces?

<!-- solution -->

Trata la clave caliente aparte: saca `customer_id = 0` del join y maneja a los invitados en otra rama, luego une los resultados con `UNION ALL`. Genera además estadísticas de tabla para que el optimizador elija el tipo de join correcto.

<!-- takeaways -->

- Pon primero las tablas grandes cuando faltan estadísticas.
- Broadcast para tablas pequeñas; redistribución para las grandes.
- Las claves con skew necesitan manejo especial.

<!-- unit: Operaciones que consumen memoria -->

<!-- goals -->

- Reconocer operaciones que concentran el trabajo en un solo worker.
- Reemplazar cálculos exactos por aproximados cuando se acepte.

<!-- concept -->

Algunas operaciones SQL necesitan ver todas las filas a la vez: ordenamientos globales, conteos distintos exactos, ventanas sin particiones, deduplicación en una unión. En un motor distribuido, esos pasos embudan los datos hacia pocos workers, y de ahí vienen los errores "exhausted resources".

Los remedios son agregar estructura (particionar ventanas, limitar ordenamientos), aceptar aproximaciones donde el negocio pueda y evitar deduplicaciones innecesarias.

<!-- example -->

```sql
SELECT dt,
       approx_distinct(user_id) AS users,            -- ~2% error, small memory
       approx_percentile(latency_ms, 0.95) AS p95
FROM logs.requests
WHERE dt >= '2026-10-01'
GROUP BY dt;
```

#### ¿Por qué un `ORDER BY` sin `LIMIT` empeora el rendimiento?

Un orden global requiere enviar todas las filas a un solo worker para el orden final, lo que es lento y puede fallar con "exceeded resources". Añade un `LIMIT` (el top-N es eficiente) u ordena solo lo necesario.

#### ¿Qué es "Query exhausted resources at this scale factor"?

Un error cuando una consulta necesita más memoria de la disponible para una operación (joins enormes, `GROUP BY` con muchos grupos, `DISTINCT` sobre muchas columnas, `ORDER BY` de todo, arreglos muy grandes). Soluciones: filtrar antes, reducir columnas, funciones aproximadas, dividir la consulta, materializar pasos intermedios con `CTAS` o usar reservas de capacidad.

#### ¿Cuándo conviene usar funciones aproximadas?

`approx_distinct`, `approx_percentile` y `approx_most_frequent` devuelven estimaciones con errores pequeños usando mucha menos memoria que `count(DISTINCT)` o los percentiles exactos, lo que sirve para dashboards y exploración.

#### ¿Por qué `count(DISTINCT x)` sobre una tabla enorme falla o es lento?

Requiere mantener todos los valores distintos en memoria entre los workers. Usa `approx_distinct(x)` para estimaciones, o preagrega conteos distintos por partición y combínalos.

#### ¿Cómo afectan las funciones de ventana al rendimiento de Athena?

Las funciones de ventana particionan y ordenan los datos; una ventana sobre toda la tabla (sin `PARTITION BY`) obliga a usar un solo worker. Particiona siempre las ventanas por una clave y filtra los datos antes.

#### ¿Qué efecto tiene `UNION` frente a `UNION ALL`?

`UNION` elimina duplicados, lo que requiere un paso extra de agregación; `UNION ALL` solo concatena. Usa `UNION ALL` cuando los duplicados son imposibles o aceptables.

#### ¿Cómo se aceleran las búsquedas con `LIKE` sobre columnas de texto grandes?

Filtrando primero por particiones, usando `regexp_like` solo cuando haga falta, y extrayendo durante el ETL los campos buscables en columnas aparte, o usando un servicio de búsqueda como OpenSearch para necesidades de texto completo.

<!-- challenge -->

Un reporte diario calcula usuarios distintos exactos sobre 90 días y suele fallar. El equipo de producto solo necesita una tendencia. ¿Qué cambias?

<!-- solution -->

Usar `approx_distinct(user_id)` por día, que necesita poca memoria y tiene cerca de 2 % de error. Si algún día se necesitan cifras exactas, precalcular los conjuntos distintos diarios en una tabla resumen.

<!-- takeaways -->

- Ordenamientos globales, distintos exactos y ventanas sin particiones son caros.
- Las funciones aproximadas cambian un error pequeño por escala.
- Prefiere `UNION ALL` salvo que necesites deduplicar.

<!-- unit: Reutilizar y precalcular resultados -->

<!-- goals -->

- Reutilizar resultados recientes y precalcular agregados frecuentes.
- Acelerar dashboards que consultan Athena.

<!-- concept -->

La consulta más barata es la que no corres. Los dashboards suelen enviar las mismas consultas una y otra vez, así que cachear resultados recientes y precalcular agregados comunes ahorra costo y espera. La reutilización de resultados cubre consultas idénticas; las tablas resumen cubren la misma pregunta hecha de formas ligeramente distintas.

La pregunta de diseño es la frescura: ¿qué tan vieja puede ser una respuesta?

<!-- example -->

```sql
-- summary table refreshed hourly; the dashboard reads it instead of raw events
INSERT INTO marts.sales_hourly
SELECT date_trunc('hour', created_at) AS hour, store_id, sum(amount) AS revenue
FROM sales.orders WHERE dt = '2026-10-17'
GROUP BY 1, 2;
```

#### ¿Qué es la reutilización de resultados de consultas?

Una función en la que Athena devuelve los resultados de una consulta anterior si la misma consulta se ejecutó hace poco (dentro de una antigüedad máxima que defines, de hasta 7 días) y los datos no cambiaron (en las tablas compatibles), sin volver a escanear datos.

#### ¿Cómo se optimizan las consultas sobre una combinación grande de dimensiones muy consultada?

Precalculando agregados en una tabla resumen (`CTAS` o `INSERT` programado), particionada por fecha, y apuntando los dashboards a ella en lugar de a la tabla en bruto.

#### Un dashboard de QuickSight sobre Athena es lento y caro. ¿Qué cambias?

Preagrego en una tabla resumen que se refresca de forma programada, uso SPICE de QuickSight para tener los datos en caché, me aseguro de que el dashboard aplique filtros de partición, convierto las tablas de origen a Parquet o Iceberg con compactación y considero reservas de capacidad para una concurrencia predecible.

<!-- challenge -->

Un dashboard con 10 gráficos corre sobre eventos crudos y tarda 40 segundos en cargar. Los datos solo cambian cada hora. ¿Qué propones?

<!-- solution -->

Construir tablas resumen horarias para los gráficos, refrescarlas con un calendario y apuntar el dashboard a ellas; activar la reutilización de resultados o la caché de la herramienta de BI (SPICE) con frescura de una hora.

<!-- takeaways -->

- La reutilización devuelve respuestas cacheadas a consultas idénticas.
- Las tablas resumen sirven agregaciones repetidas con bajo costo.
- Decide primero la frescura y luego la caché.

<!-- unit: Capacidad y límites de S3 -->

<!-- goals -->

- Decidir cuándo compensan las reservas de capacidad.
- Reconocer el throttling de S3 como límite de rendimiento.

<!-- concept -->

Athena on-demand comparte capacidad con otros clientes y factura por escaneo. Las reservas de capacidad compran procesamiento dedicado para cargas estables, cambiando el pago por consulta por un costo y una concurrencia predecibles.

Debajo del motor está S3, que tiene sus propios límites por prefijo. Las consultas sobre millones de archivos pequeños pueden sufrir throttling sin importar cuánto cómputo haya, así que la organización de archivos también es un tema de rendimiento.

<!-- example -->

| Situación | Mejor opción |
|---|---|
| Unas pocas consultas ad hoc al día | On-demand |
| BI todo el día, cientos de usuarios | Reserva de capacidad |
| Errores `SlowDown` con muchos archivos diminutos | Compactar archivos, repartir prefijos |

#### ¿Qué son las reservas de capacidad?

Capacidad dedicada de procesamiento de consultas comprada en DPU (por una duración mínima y luego por minuto) y asignada a workgroups. Las consultas de esos workgroups corren sobre la capacidad reservada, facturadas por DPU-hora en lugar de por TB escaneado, con costo y concurrencia predecibles.

#### ¿Cuándo valen la pena las reservas de capacidad?

Cuando el volumen de consultas es alto y estable (dashboards de BI intensivos, muchos usuarios concurrentes), cuando necesitas concurrencia garantizada para cargas críticas, o cuando el costo por TB supera el precio de la capacidad reservada.

#### ¿Por qué el throttling de S3 puede ralentizar las consultas de Athena?

S3 admite altas tasas de solicitudes por prefijo, pero las consultas sobre millones de archivos pequeños en un mismo prefijo pueden recibir errores `SlowDown` (503). Menos archivos y más grandes, y repartir los datos entre prefijos (particiones), lo evitan.

<!-- challenge -->

Tu factura on-demand es de 30.000 USD al mes, sobre todo por consultas de BI que corren 8 horas al día. ¿Cómo evalúas una reserva de capacidad?

<!-- solution -->

Estimar las DPU necesarias para la concurrencia pico a partir del volumen actual, cotizarlas para las horas de trabajo y comparar con el gasto on-demand. Asignar solo el workgroup de BI a la reserva y dejar lo ad hoc on-demand.

<!-- takeaways -->

- Las reservas dan capacidad dedicada y costo predecible.
- Compensan con cargas estables y de alto volumen.
- Muchos archivos diminutos pueden topar con los límites de peticiones de S3.

### Workgroups, control de costos y monitoreo

<!-- unit: Workgroups como barandas -->

<!-- goals -->

- Fijar límites por consulta y por workgroup.
- Imponer configuraciones y asignar costos por equipo.

<!-- concept -->

En un servicio que cobra por escaneo, una consulta descuidada puede costar más que un mes de uso normal. Los workgroups ponen barandas a ese riesgo: cada equipo o aplicación tiene su configuración, ubicación de resultados y cifrado impuestos, y límites que cancelan o alertan ante escaneos grandes.

Los workgroups también hacen visibles los costos, porque los tags y métricas atan cada consulta a su dueño.

<!-- example -->

```bash
aws athena update-work-group --work-group analysts \
  --configuration-updates 'EnforceWorkGroupConfiguration=true,BytesScannedCutoffPerQuery=107374182400'
# cancels any query scanning more than 100 GB
```

#### ¿Cómo se limitan los costos por equipo?

Creando un workgroup por equipo o aplicación con un límite de uso de datos por consulta (cancela las consultas que escanean más de un umbral) y límites por periodo para todo el workgroup que disparan alarmas, imponiendo la configuración del workgroup para que los usuarios no la sobrescriban y etiquetando los workgroups para la asignación de costos.

#### ¿Qué significa "override client-side settings" en un workgroup?

Cuando se activa, la ubicación de resultados, el cifrado y otros ajustes del workgroup se aplican a todas las consultas, ignorando lo que indiquen los clientes, lo que impone el gobierno.

#### ¿Qué diferencia hay entre un límite por consulta y uno de todo el workgroup?

Un control por consulta cancela cualquier consulta que escanee más del umbral. Los controles de todo el workgroup miden el total escaneado en un periodo y disparan alarmas de CloudWatch o notificaciones de SNS, pero no cancelan consultas.

#### ¿Cómo se evitan las consultas descontroladas?

Con límites de datos por consulta en los workgroups, timeouts de consulta, formación sobre los filtros de partición, vistas que exigen filtros de partición y reservas de capacidad para las cargas predecibles.

#### ¿Cómo se asignan los costos de Athena a los equipos?

Con workgroups separados por equipo, etiquetados con etiquetas de asignación de costos, y analizando los costos en Cost Explorer por etiqueta; con reservas de capacidad, asignando los workgroups a reservas por equipo.

<!-- challenge -->

La consulta de un practicante escaneó 40 TB durante un fin de semana. ¿Qué barandas agregas?

<!-- solution -->

Poner a practicantes y analistas en un workgroup con límite por consulta (por ejemplo 1 TB) y una alerta diaria del workgroup, imponer su configuración y exigir filtros de partición mediante vistas o formación.

<!-- takeaways -->

- Los límites por consulta cancelan escaneos grandes.
- La configuración impuesta del workgroup se sobrepone a los clientes.
- Los workgroups con tags atribuyen costos a equipos.

<!-- unit: Monitorear uso y fallos -->

<!-- goals -->

- Monitorear escaneos, duraciones y fallos en el tiempo.
- Investigar aumentos de costo de forma sistemática.

<!-- concept -->

Athena guarda el historial de consultas 45 días y los workgroups publican métricas, pero ninguno responde por sí solo "¿por qué cambiaron los costos?". Exportar los detalles de las consultas permite encontrar las caras y su tendencia.

Recuerda también los costos ocultos: las peticiones a S3 se facturan aparte, así que las tablas con muchos archivos pequeños cuestan más de lo que muestra la factura de Athena.

<!-- example -->

```sql
-- after exporting query executions to a table
SELECT workgroup, query_hash, sum(data_scanned_bytes) / 1e12 AS tb
FROM ops.athena_queries
WHERE day >= current_date - interval '7' day
GROUP BY 1, 2 ORDER BY tb DESC LIMIT 20;
```

#### ¿Cómo se monitorea el uso de Athena?

Con métricas de CloudWatch por workgroup (datos escaneados, duración, tiempo en cola, consultas fallidas), el historial de consultas (`ListQueryExecutions`, consola), CloudTrail para las llamadas a la API e informes de costos con etiquetas.

#### ¿Cuánto tiempo se guarda el historial de consultas?

Athena guarda el historial durante 45 días. Para conservarlo más o analizarlo, exporta los detalles de ejecución (por ejemplo con eventos de EventBridge o un job programado que llame a `GetQueryExecution`) a S3.

#### ¿Cómo encuentras las consultas más caras?

En el historial o en los datos de ejecución exportados, ordenando por `DataScannedInBytes`; luego revisas si filtran por particiones, leen CSV o JSON, o seleccionan demasiadas columnas.

#### ¿Cómo afectan las solicitudes de S3 a los costos de Athena?

El precio por TB de Athena no incluye las solicitudes GET y LIST de S3, que factura S3. Las tablas con enormes cantidades de archivos pequeños pueden generar costos de solicitudes importantes además del cobro de Athena.

#### ¿Cómo se siguen los fallos de las consultas?

Con las métricas de CloudWatch de consultas fallidas por workgroup, los eventos "Athena Query State Change" de EventBridge enviados a alertas y el historial de consultas con los mensajes de error.

#### Tu factura de Athena se duplicó. ¿Cómo lo investigas?

Reviso en CloudWatch los datos escaneados por workgroup, busco en el historial las consultas con más bytes escaneados, y busco dashboards nuevos con consultas sin filtrar, `SELECT *` sobre tablas anchas, tablas en CSV o JSON, y filtros de partición que dejaron de funcionar (por ejemplo una función sobre la columna de partición). Luego corrijo formatos y filtros y añado límites por consulta.

<!-- challenge -->

Los costos subieron un 40 % este mes y no llegó ningún equipo nuevo. Nombra las tres primeras cosas que revisas.

<!-- solution -->

Las consultas con más bytes escaneados este mes contra el anterior, consultas programadas nuevas o cambiadas (a menudo la frecuencia de refresco de un dashboard) y tablas cuyos filtros de partición dejaron de podar tras un cambio de esquema u organización.

<!-- takeaways -->

- Exporta el historial de consultas para analizarlo a largo plazo.
- Ordena por bytes escaneados para encontrar consultas caras.
- Los costos de peticiones a S3 están fuera de la factura de Athena.

### Consultas federadas y conectores

<!-- unit: Consultar más allá de S3 -->

<!-- goals -->

- Explicar cómo las consultas federadas llegan a bases de datos y otras fuentes.
- Sopesar su comodidad frente al rendimiento y la carga.

<!-- concept -->

Las consultas federadas permiten que una sentencia SQL una datos del lake con datos vivos en bases de datos u otros servicios. Un conector Lambda traduce parte de la consulta para la fuente, empuja filtros cuando puede y devuelve filas a Athena.

La comodidad tiene costos: la fuente hace trabajo real, la Lambda tiene límites y los escaneos analíticos pueden dañar una base operativa. La federación sirve para búsquedas pequeñas y joins ocasionales, no para escaneos pesados frecuentes.

<!-- example -->

```sql
SELECT o.order_id, o.amount, c.segment
FROM lake.orders o
JOIN rds_pg.public.customers c ON o.customer_id = c.id
WHERE o.dt = '2026-10-17';
```

#### ¿Qué es Athena Federated Query?

Una función que permite a Athena consultar datos fuera de S3, como DynamoDB, RDS y Aurora (MySQL, PostgreSQL), Redshift, DocumentDB, OpenSearch, CloudWatch Logs, Snowflake, BigQuery y muchos más, mediante conectores de orígenes de datos que corren como funciones AWS Lambda (o como conexiones administradas de Glue).

#### ¿Cómo funcionan los conectores federados?

La Lambda del conector recibe parte del plan de la consulta, lee los datos del origen (empujando los filtros y las proyecciones cuando se puede) y los devuelve a Athena en formato Apache Arrow, que luego los une y agrega con otros datos.

#### ¿Cuáles son las desventajas de las consultas federadas?

El rendimiento depende del origen y de la Lambda (timeouts, memoria, concurrencia), las consultas pueden cargar las bases operativas, el pushdown es limitado en algunos orígenes y pagas Lambda más los datos escaneados. Para un uso frecuente e intensivo, replica los datos en S3.

#### ¿Cómo se une un dato de S3 con una tabla de RDS?

Registrando el conector de RDS como origen de datos (por ejemplo `rds_pg`) y consultando `SELECT … FROM lake.orders o JOIN rds_pg.public.customers c ON o.customer_id = c.id`, manteniendo pequeño el lado de RDS con filtros.

#### ¿Cómo se consulta DynamoDB con Athena?

Con el conector de DynamoDB, que escanea o consulta la tabla (consumiendo capacidad de lectura); para consultas analíticas grandes, exporta la tabla a S3 (exportación de DynamoDB) y consulta la exportación.

<!-- challenge -->

Un reporte diario une una tabla de 2 TB del lake con un escaneo completo de una tabla DynamoDB de producción, y la app se pone lenta a esa hora. ¿Qué cambias?

<!-- solution -->

Dejar de escanear DynamoDB en vivo: exportarla a S3 (export de DynamoDB a S3 en Parquet o un job diario) y unir con la copia exportada. Dejar la federación para búsquedas pequeñas y filtradas.

<!-- takeaways -->

- Los conectores corren en Lambda y empujan filtros.
- La federación es cómoda pero carga la fuente.
- Exporta las fuentes grandes a S3 para analítica regular.

<!-- unit: Conectores y funciones externas -->

<!-- goals -->

- Desplegar y operar conectores federados.
- Llamar UDF en Lambda y modelos de SageMaker desde SQL.

<!-- concept -->

Conectores y funciones extienden Athena con código que tú corres. Ambos son funciones Lambda, así que heredan sus límites: tamaño de respuesta (de ahí el spill bucket), timeouts y concurrencia. Trátalos como cualquier servicio: despliégalos como código, con roles de mínimo privilegio, y monitorízalos.

Las funciones externas llevan al SQL lógica que el motor no tiene, del descifrado a la puntuación de modelos, pero cada fila cruza una llamada de red.

<!-- example -->

```sql
USING EXTERNAL FUNCTION predict_churn(tenure int, spend double)
  RETURNS double SAGEMAKER 'churn-endpoint'
SELECT customer_id, predict_churn(tenure, spend) AS churn_score
FROM marts.customers WHERE dt = '2026-10-17';
```

#### ¿Cómo se despliega un conector federado?

Desde la consola de Athena (creando un origen de datos), que despliega la Lambda del conector desde el AWS Serverless Application Repository o usa conexiones de Glue, con un bucket de spill en S3 para los resultados grandes y la configuración de IAM y VPC adecuada.

#### ¿Para qué sirve el bucket de spill?

Una ubicación de S3 donde el conector escribe los datos que superan los límites de tamaño de respuesta de Lambda, y que Athena luego lee. Debe estar cifrado y tener una regla de ciclo de vida.

#### ¿Se puede escribir un conector propio?

Sí, con el Athena Query Federation SDK (Java), implementando los manejadores de metadatos y de registros para tu origen, desplegado como función Lambda.

#### ¿Qué son las funciones definidas por el usuario en Athena?

Funciones escalares implementadas en una función Lambda (Java) y llamadas con `USING EXTERNAL FUNCTION`, usadas para lógica que no existe en SQL, como llamar a un servicio interno o un descifrado propio.

#### ¿Puede Athena llamar a modelos de machine learning?

Sí, con `USING EXTERNAL FUNCTION … SAGEMAKER 'nombre-endpoint'`, que envía filas a un endpoint de SageMaker para hacer inferencia dentro de una consulta.

<!-- challenge -->

Una consulta federada falla con un error de tamaño de respuesta de Lambda en resultados grandes. ¿Qué falta?

<!-- solution -->

Un spill bucket, o uno en el que el conector pueda escribir. Configura una ubicación de spill en S3 con una regla de ciclo de vida para borrar objetos viejos y da acceso a ella al rol del conector.

<!-- takeaways -->

- Conectores y UDF son funciones Lambda con los límites de Lambda.
- El spill bucket maneja respuestas grandes del conector.
- Las funciones externas agregan lógica por fila con costo de red.

### Seguridad y gobierno

<!-- unit: Control de acceso con IAM y Lake Formation -->

<!-- goals -->

- Controlar quién consulta qué tablas, columnas y filas.
- Enmascarar o excluir datos sensibles.

<!-- concept -->

Con solo IAM, el acceso a tablas es en realidad acceso a S3: quien pueda leer los archivos puede leer cualquier tabla encima. Lake Formation sube el control a tablas, columnas y filas, y entrega a Athena credenciales temporales para exactamente lo que el usuario puede ver. Eso hace posibles reglas finas como "los analistas de la UE ven filas de la UE sin email".

El enmascarado agrega otra capa, mediante columnas excluidas, vistas que ocultan o copias enmascaradas.

<!-- example -->

```sql
-- Lake Formation data filter (defined in LF): row filter + excluded columns
--   table: lake.customers  row filter: country IN ('DE','FR','ES')  exclude: email, phone
SELECT customer_id, country, segment FROM lake.customers;   -- analyst sees only allowed data
```

#### ¿Cómo se controla el acceso a Athena?

Con políticas IAM sobre las acciones de Athena y los workgroups, permisos de S3 sobre los datos y las ubicaciones de resultados, permisos del Glue Data Catalog (bases, tablas) y, para un control detallado, permisos de Lake Formation sobre bases de datos, tablas, columnas, filas y celdas.

#### ¿Cómo funciona Lake Formation con Athena?

Athena comprueba los permisos de Lake Formation de quien consulta y solo devuelve las columnas y filas permitidas, usando credenciales temporales que entrega Lake Formation para leer S3, así que los usuarios no necesitan acceso directo a S3 sobre los datos.

#### ¿Cómo se restringe qué datos de S3 puede consultar un usuario?

Concediendo el acceso a las tablas mediante Lake Formation (sin permisos directos de S3), o con IAM limitando el acceso de S3 a prefijos concretos y el acceso de Glue a bases y tablas concretas.

#### ¿Qué es un data filter de Lake Formation?

Una definición de seguridad a nivel de fila y de celda para una tabla (una expresión de filtro de filas más las columnas incluidas o excluidas) que se concede a principals; Athena la aplica al consultar.

#### ¿Cómo se enmascaran columnas sensibles en Athena?

Excluyéndolas con permisos de columna de Lake Formation, ofreciendo vistas que las hashean u ocultan, o guardando copias enmascaradas en una tabla curada aparte para el acceso general.

<!-- challenge -->

Los analistas deben consultar una tabla de clientes sin ver emails, y los analistas alemanes solo clientes alemanes. ¿Cómo lo configuras?

<!-- solution -->

Registrar la ubicación en Lake Formation, crear un data filter que excluya `email` con filtro de filas `country = 'DE'` y otorgarlo al rol de los analistas alemanes. Quitarles el acceso directo a S3 sobre la ubicación de la tabla.

<!-- takeaways -->

- Solo IAM implica acceso a nivel de archivos.
- Lake Formation otorga tablas, columnas y filas.
- Los data filters combinan seguridad de filas y columnas.

<!-- unit: Cifrado, redes y auditoría -->

<!-- goals -->

- Cifrar datos y resultados y mantener privado el tráfico.
- Compartir datos entre cuentas y auditar el uso.

<!-- concept -->

La seguridad también cubre el camino alrededor de las consultas. Datos y resultados deben cifrarse con claves que controles. El tráfico puede quedarse dentro de tu red con VPC endpoints. El acceso entre cuentas funciona con catálogos compartidos en vez de copiar datos.

La auditoría cierra el círculo: CloudTrail registra quién corrió qué, lo que importa cuando hay tablas sensibles de por medio.

<!-- example -->

```bash
aws athena update-work-group --work-group finance --configuration-updates \
 'ResultConfigurationUpdates={OutputLocation=s3://athena-results-finance/,EncryptionConfiguration={EncryptionOption=SSE_KMS,KmsKey=alias/finance}}'
```

#### ¿Cómo se cifran los datos de Athena?

Los datos en S3 se pueden cifrar con SSE-S3, SSE-KMS o KMS del lado del cliente; Athena lee los datos cifrados de forma transparente con los permisos de KMS adecuados. Los resultados de las consultas se pueden cifrar (SSE-S3, SSE-KMS, CSE-KMS) por workgroup, y los datos en tránsito usan TLS.

#### ¿Cómo se consultan datos de otra cuenta de AWS?

Con el uso compartido entre cuentas de Lake Formation (resource links), el acceso entre cuentas al catálogo de Glue registrado como origen de datos, o políticas de bucket que dan al rol que consulta acceso a los datos y a su clave KMS.

#### ¿Cómo se audita el uso de Athena?

CloudTrail registra las llamadas a la API (quién lanzó qué consulta, con su texto), Lake Formation registra el acceso a los datos, y los logs de acceso del servidor de S3 o los eventos de datos de CloudTrail registran las lecturas de objetos.

#### ¿Cómo se usa Athena desde una red privada?

Mediante endpoints de interfaz de VPC para Athena (y para Glue, S3 y KMS según haga falta), para que el tráfico no pase por internet; las políticas del endpoint pueden restringir el uso.

#### ¿Cómo se da acceso seguro a Athena a una herramienta de BI?

Creando un rol o usuario IAM dedicado (preferiblemente federado con IAM Identity Center u OAuth para el driver), limitado a un workgroup, a las tablas necesarias vía Lake Formation y a la ubicación de resultados, y conectando con el driver JDBC/ODBC.

<!-- challenge -->

Una herramienta de BI se conecta con un usuario IAM cuyas claves nunca expiran y tienen permisos de administrador. ¿Cómo lo arreglas?

<!-- solution -->

Crear un rol dedicado (o identidad federada desde el driver) limitado a un workgroup y a las tablas necesarias vía Lake Formation, usar credenciales temporales y borrar las claves de larga vida.

<!-- takeaways -->

- Cifra datos y resultados con KMS.
- Comparte entre cuentas mediante catálogos, no copias.
- CloudTrail registra quién corrió cada consulta.

### Resolución de problemas

<!-- unit: Resultados faltantes o equivocados -->

<!-- goals -->

- Diagnosticar consultas que no devuelven filas, devuelven `NULL` o duplican.
- Arreglar problemas de registro de particiones y de timestamps.

<!-- concept -->

Cuando los resultados se ven mal en Athena, la causa suele ser el contrato entre tabla y archivos, no el SQL. Particiones no registradas, una ubicación levemente equivocada, un SerDe que no parsea los valores o archivos escritos dos veces producen respuestas plausibles pero falsas.

Trabaja desde los archivos hacia arriba: lista la ubicación, revisa las particiones, mira los valores crudos con `"$path"` y luego corrige la definición o el pipeline.

<!-- example -->

```sql
SHOW PARTITIONS sales.orders;                 -- is today's partition there?
SELECT "$path", count(*) FROM sales.orders WHERE dt = '2026-10-17' GROUP BY 1;  -- duplicate files?
```

#### Una consulta devuelve cero filas pero los archivos existen. ¿Qué revisas?

Si las particiones están registradas (o si la proyección está bien configurada), si el `LOCATION` y la plantilla de ubicación coinciden con las rutas reales, si el SerDe y las columnas corresponden al formato, y si los archivos están en subcarpetas que la tabla no incluye.

#### ¿Por qué `MSCK REPAIR TABLE` no añade ninguna partición?

Las carpetas no están al estilo Hive (`clave=valor`), los nombres de las claves no coinciden con los de las columnas de partición (importan las mayúsculas), la ubicación está mal o la tabla tiene activada la proyección de particiones.

#### ¿Por qué los números salen como `NULL` desde una tabla CSV?

Los valores contienen caracteres que no se pueden interpretar (separadores de miles, símbolos de moneda, comillas con `LazySimpleSerDe`, cadenas vacías), o las columnas están corridas porque un campo contiene el delimitador. Usa `OpenCSVSerDe`, limpia los datos, o lee como texto y aplica `TRY_CAST`.

#### ¿Por qué una consulta sobre fechas y horas devuelve resultados incorrectos?

Marcas de tiempo guardadas como texto en formatos distintos, confusión de zonas horarias (los timestamps sin zona se interpretan como UTC en muchos casos) o codificaciones de timestamp de Parquet que difieren entre escritores. Interpreta de forma explícita con `from_iso8601_timestamp` o `parse_datetime` y convierte las zonas con `AT TIME ZONE`.

#### Los resultados tienen duplicados tras reejecutar un pipeline. ¿Por qué?

El pipeline usó `INSERT INTO` sobre una tabla Hive sin eliminar la salida anterior, o se escribieron archivos dos veces en la misma ubicación. Haz idempotentes las escrituras (sobrescribir particiones, `MERGE` de Iceberg) y deduplica las particiones afectadas.

<!-- challenge -->

Los datos de ayer están en S3 en `s3://lake/orders/2026/10/17/`, pero `WHERE dt = '2026-10-17'` no devuelve nada. ¿Cuál es la causa probable y el arreglo?

<!-- solution -->

La ruta no es estilo Hive, así que ni `MSCK REPAIR` ni el catálogo conocen la partición. Agrégala con `ALTER TABLE ADD PARTITION ... LOCATION`, o configura projection con una plantilla de ubicación que coincida con `${year}/${month}/${day}`.

<!-- takeaways -->

- Revisa particiones y ubicaciones antes que el SQL.
- Los errores de parseo se vuelven `NULL` en silencio.
- Los duplicados suelen indicar escrituras no idempotentes.

<!-- unit: Leer errores de Hive -->

<!-- goals -->

- Interpretar los errores `HIVE_*` y de permisos más comunes.
- Ubicar el archivo u objeto que los causa.

<!-- concept -->

Los mensajes de error de Athena nombran la capa que falló. Los errores de desajuste de esquema apuntan al catálogo, los de cursor y datos malos a los archivos, y el acceso denegado puede venir de cualquiera de cinco capas de permisos. Leer el error primero ahorra adivinar.

La mayoría de errores a nivel de archivo se resuelven encontrando el archivo culpable con `"$path"` y moviéndolo o corrigiéndolo.

<!-- example -->

| Error | Mira |
|---|---|
| `HIVE_PARTITION_SCHEMA_MISMATCH` | esquema de partición vs tabla en el catálogo |
| `HIVE_CURSOR_ERROR` | archivo corrupto o de formato equivocado |
| `HIVE_BAD_DATA` | un valor que no encaja en el tipo |
| `Access Denied` | S3, bucket de resultados, KMS, Glue, Lake Formation |

#### ¿Qué significa `HIVE_PARTITION_SCHEMA_MISMATCH`?

El esquema de una partición en el catálogo difiere del de la tabla (tipos o columnas). Haz que las particiones hereden el esquema de la tabla (ajuste del crawler o recreando las particiones) y estabiliza el origen.

#### ¿Qué suele indicar `HIVE_CURSOR_ERROR`?

Un problema al leer un archivo: archivos corruptos o truncados, un formato distinto al de la definición de la tabla, un archivo comprimido ilegible, o problemas de permisos o de KMS en algunos objetos.

#### ¿Qué significa `HIVE_BAD_DATA`?

Un valor no se puede interpretar con el tipo declarado, por ejemplo texto en una columna numérica, un registro JSON mal formado o un tipo de Parquet que no coincide. Corrige los datos, los tipos de la tabla, o usa `TRY_CAST` sobre columnas de texto.

#### ¿Por qué aparece `Access Denied` en una consulta?

Faltan permisos sobre los datos de S3, la ubicación de resultados, la clave KMS, los objetos del catálogo de Glue, los permisos de Lake Formation o el workgroup. El mensaje de error suele nombrar el recurso.

<!-- challenge -->

Un usuario recibe `Access Denied` aunque tiene lectura completa en S3 sobre los datos. Enumera otros tres lugares a revisar.

<!-- solution -->

Permiso de escritura en la ubicación de resultados, permiso de descifrado en la clave KMS que usan datos o resultados, y permisos del catálogo de Glue (o Lake Formation) sobre la base y la tabla.

<!-- takeaways -->

- El error nombra la capa que falló.
- Usa `"$path"` para encontrar archivos malos.
- El acceso necesita S3, resultados, KMS, Glue y Lake Formation.

<!-- unit: Consultas lentas y que fallan -->

<!-- goals -->

- Diagnosticar consultas lentas que escanean poco.
- Resolver timeouts, throttling y la lentitud de Iceberg.

<!-- concept -->

No toda la lentitud viene del escaneo. Planificar muchas particiones, abrir muchos archivos pequeños, esperar por throttling de S3 o por una fuente federada lenta consumen tiempo que las métricas de bytes no muestran. Las estadísticas de ejecución dividen el tiempo en cola, planificación y ejecución, lo que señala al culpable.

Las tablas Iceberg se ralentizan por una razón parecida: las escrituras frecuentes dejan archivos pequeños y archivos de borrado hasta que el mantenimiento los limpia.

<!-- example -->

```text
QueryQueueTime:      0.2 s
QueryPlanningTime:  48.7 s   ← partition metadata, not data
EngineExecutionTime: 3.1 s
DataScannedInBytes:  120 MB
```

#### Una consulta es lenta pero escanea pocos datos. ¿Qué puede causarlo?

El tiempo de planificación en tablas con muchas particiones (usa proyección o índices de partición), muchos archivos diminutos (sobrecarga por archivo), un origen federado, la espera por límites de concurrencia, o una operación costosa como un join grande o un orden global.

#### ¿Por qué aparece "Query timeout"?

La consulta superó el timeout del workgroup: escanea demasiados datos, un join u orden pesado, o un origen federado lento. Optimiza la consulta o la organización de los datos, materializa pasos intermedios o sube la cuota del timeout.

#### ¿Por qué hay errores de "too many open files" o `SlowDown` de S3?

Las tablas con una cantidad enorme de archivos pequeños provocan muchísimas solicitudes concurrentes a S3. Compacta los archivos y repártelos entre particiones.

#### ¿Por qué una consulta sobre Iceberg se vuelve más lenta con el tiempo?

Se acumulan muchos archivos pequeños y archivos de borrado con las escrituras frecuentes y los cambios a nivel de fila. Programa `OPTIMIZE` y `VACUUM` (o usa la compactación automática del catálogo de Glue o de S3 Tables).

<!-- challenge -->

Una tabla Iceberg actualizada cada 5 minutos es ahora diez veces más lenta de consultar que el mes pasado. ¿Qué programas?

<!-- solution -->

`OPTIMIZE ... REWRITE DATA USING BIN_PACK` periódico para compactar archivos pequeños y de borrado, y `VACUUM` para expirar snapshots viejos, por ejemplo a diario. Considera agrupar las actualizaciones con menos frecuencia si la frescura lo permite.

<!-- takeaways -->

- Revisa por separado cola, planificación y ejecución.
- Muchas particiones o archivos ralentizan la planificación, no el escaneo.
- Las tablas Iceberg necesitan compactación regular.

<!-- stage: Integrarlo todo -->

### Escenarios

<!-- unit: Diseñar analítica de logs y eventos -->

<!-- goals -->

- Diseñar un camino barato y rápido desde los eventos hasta las consultas.
- Equilibrar frescura frente a costo y tamaño de archivos.

<!-- concept -->

Los diseños con Athena triunfan o fracasan en el camino de escritura. Las consultas son baratas y rápidas cuando los datos llegan en archivos columnares de buen tamaño, particionados por los filtros que usa la gente y registrados sin pasos manuales. Una buena respuesta sigue a los datos desde el productor hasta la consulta, nombra una decisión en cada paso y explica el equilibrio entre frescura y costo: buffers más cortos dan datos más frescos pero archivos más pequeños.

<!-- example -->

```text
apps ─► Firehose (buffer 5 min, convert to Parquet, dt/hour prefixes)
     ─► S3 lake ─► table with partition projection
     ─► workgroup with limits ─► dashboards on hourly summary tables
```

#### Diseña una solución barata de analítica de logs con Athena.

Envío los logs a S3 con Firehose (con buffer, convertidos a Parquet, particionados por fecha), defino una tabla con proyección de particiones por fecha, creo vistas para las preguntas frecuentes, configuro un workgroup con límites de datos y doy acceso a los analistas mediante Lake Formation. Añado reglas de ciclo de vida para mover los logs viejos a clases de almacenamiento más baratas.

#### ¿Cómo construirías dashboards casi en tiempo real sobre Athena?

Envío los eventos con Firehose a S3 en Parquet con buffers cortos, particiono por fecha y hora con proyección, construyo cada pocos minutos tablas agregadas pequeñas con `INSERT INTO` programado o `MERGE` sobre Iceberg, y apunto los dashboards a esos agregados; para latencias por debajo del minuto, uso otro almacén como OpenSearch o una base de datos de streaming.

<!-- challenge -->

El negocio quiere dashboards actualizados cada minuto en vez de cada 15. ¿Qué cambia y cuánto cuesta?

<!-- solution -->

Acortar el buffer de Firehose y refrescar más seguido, lo que crea muchos más archivos pequeños y más consultas. Agregar compactación (o Iceberg con `OPTIMIZE`) y consultar tablas resumen; si de verdad se necesita latencia de un minuto, considerar un almacén de streaming en vez de Athena.

<!-- takeaways -->

- Diseña el camino de escritura: formato, tamaño, particiones, registro.
- La frescura cuesta tamaño de archivo y volumen de consultas.
- Sirve los dashboards desde resúmenes, no desde eventos crudos.

<!-- unit: Migraciones y autoservicio gobernado -->

<!-- goals -->

- Planear la migración de reportes a Athena.
- Montar acceso gobernado y con control de presupuesto a un lake grande.

<!-- concept -->

Llevar gente a Athena tiene tanto de control como de SQL. Una migración necesita datos en buenos formatos, consultas traducidas y validación en paralelo. El autoservicio necesita barandas para que la libertad no termine en costos descontrolados o fugas de datos: permisos por dominio, workgroups con límites, tablas curadas y monitoreo. Ambas preguntas prueban si ves Athena como parte de una plataforma y no como una herramienta suelta.

<!-- example -->

| Preocupación | Control |
|---|---|
| Quién ve qué | Permisos de Lake Formation por dominio |
| Cuánto gastan | Workgroup por equipo, límite por consulta |
| Qué tan rápidas y baratas son las consultas | Parquet particionado o Iceberg, resúmenes |
| Qué pasó | CloudTrail, exportación del historial de consultas |

#### ¿Cómo migras reportes de un SQL Server on-premises a Athena?

Exporto las tablas a S3 como Parquet (DMS o exportaciones), defino tablas de Glue o Iceberg, traduzco el T-SQL a SQL de Trino (funciones, manejo de fechas, `TOP` a `LIMIT`, sin `PIVOT`), recreo las vistas, valido los resultados comparando agregados y conecto la herramienta de BI con el driver.

#### Un equipo necesita acceso SQL ad hoc a un data lake de 50 TB con un control de presupuesto estricto. ¿Qué montas?

Permisos de Lake Formation por dominio, un workgroup por equipo con límites por consulta, tablas Parquet o Iceberg particionadas por fecha, vistas que imponen filtros de partición, reutilización de resultados, documentación de las tablas e informes mensuales de bytes escaneados por equipo.

<!-- challenge -->

Tras migrar los reportes, los totales difieren levemente de SQL Server en algunos días. ¿Cómo encuentras la causa?

<!-- solution -->

Compara por día y por clave para ubicar la diferencia y luego inspecciona las filas. Causas típicas: zonas horarias en timestamps, `double` contra `decimal`, manejo de `NULL` en joins y funciones de T-SQL traducidas con otra semántica.

<!-- takeaways -->

- Las migraciones necesitan formatos, traducción y validación.
- El autoservicio necesita permisos, límites y datos curados.
- Valida comparando agregados por clave y por día.
