## Guía de estudio de Snowflake

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de Snowflake: unas 200 preguntas](../../images/snowflake_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre Snowflake, desde su arquitectura hasta los virtual warehouses, las micro-particiones, la carga de datos, los datos semiestructurados, los streams y tasks, las dynamic tables, la seguridad, el uso compartido de datos, el rendimiento y el control de costos. Las respuestas reflejan la plataforma en 2026. Abre una pregunta para ver su respuesta, o usa el filtro para buscar en toda la guía.

<!-- QA -->

### Arquitectura

#### ¿Qué es Snowflake?

Una plataforma de datos en la nube ofrecida como servicio totalmente administrado en AWS, Azure y Google Cloud. Empezó como data warehouse SQL y hoy cubre también data lakes (tablas Iceberg), ingeniería de datos, uso compartido de datos, aplicaciones e IA. No hay hardware ni software que instalar, ajustar o parchar.

#### ¿Cuáles son las tres capas de la arquitectura de Snowflake?

El almacenamiento (datos guardados en micro-particiones comprimidas y en columnas sobre almacenamiento de objetos en la nube), el procesamiento de consultas (los virtual warehouses: clusters de cómputo independientes) y los servicios en la nube (autenticación, metadatos, optimización de consultas, control de acceso, transacciones y gestión de la infraestructura).

#### ¿Qué significa "separar almacenamiento y cómputo" en Snowflake?

Los datos se guardan una sola vez en un almacenamiento central, y cualquier número de virtual warehouses puede leerlos de forma independiente. Escalas y pagas por separado el cómputo y el almacenamiento, y las cargas de trabajo (carga, BI, ciencia de datos) no compiten por los mismos recursos.

#### ¿Por qué se dice que Snowflake es un híbrido entre shared-disk y shared-nothing?

Como en shared-disk, todos los nodos de cómputo ven una única copia central de los datos. Como en shared-nothing (MPP), cada warehouse procesa su parte de los datos en sus propios nodos con caché local, lo que da un rendimiento escalable.

#### ¿Qué es un virtual warehouse?

Un cluster de cómputo con nombre que ejecuta consultas y DML y carga datos. Tiene un tamaño, se puede suspender y reanudar, y solo consume créditos mientras está encendido.

#### ¿Qué hace la capa de servicios en la nube?

Lo coordina todo: autenticación y control de acceso, el almacén de metadatos (tablas, estadísticas de micro-particiones, historial), el análisis y la optimización de consultas, la gestión de transacciones, el caché de resultados y la seguridad. Solo se factura si su uso supera el 10 % del cómputo diario de los warehouses.

#### ¿Qué son una cuenta y una organización de Snowflake?

Una cuenta es un despliegue de Snowflake en una región de una nube, con sus propios usuarios, bases de datos y warehouses, y una URL de acceso. Una organización agrupa varias cuentas del mismo cliente para la facturación, la replicación y la gestión de cuentas (con ORGADMIN).

#### ¿Cuál es la jerarquía de objetos de Snowflake?

Organización → cuenta → base de datos → esquema → objetos (tablas, vistas, stages, file formats, secuencias, streams, tasks, pipes, funciones, procedimientos). Los warehouses, usuarios, roles, resource monitors e integraciones son objetos a nivel de cuenta.

#### ¿Qué ediciones ofrece Snowflake?

Standard; Enterprise (añade warehouses multi-cluster, Time Travel de hasta 90 días, vistas materializadas, políticas de enmascaramiento y de acceso a filas, search optimization); Business Critical (añade más seguridad y cumplimiento, como soporte para HIPAA y PCI, Tri-Secret Secure, conectividad privada y failover); y Virtual Private Snowflake (un entorno totalmente aislado).

#### ¿Qué es un crédito?

La unidad de facturación del cómputo. Un warehouse consume créditos por segundo (con un mínimo de 60 segundos cada vez que se reanuda) según su tamaño. Las funciones serverless (Snowpipe, clustering automático, search optimization, tasks serverless) también consumen créditos. El almacenamiento se factura aparte por TB al mes.

#### ¿Cómo se relacionan los tamaños de warehouse con los créditos?

Cada escalón de tamaño duplica el cómputo y la tarifa de créditos: X-Small usa 1 crédito por hora, Small 2, Medium 4, Large 8, y así hasta 6X-Large. Una consulta que se paraleliza bien corre más o menos el doble de rápido en el siguiente tamaño, así que el costo puede mantenerse similar mientras baja la latencia.

#### ¿Qué proveedores de nube y regiones se pueden usar?

AWS, Azure y Google Cloud, en muchas regiones. Una cuenta vive en una región de una nube; la replicación y el uso compartido de datos entre regiones y nubes conectan las cuentas.

#### ¿Cómo se conecta uno a Snowflake?

Con Snowsight (la interfaz web), la Snowflake CLI y SnowSQL, los drivers (JDBC, ODBC, conector de Python, Go, Node.js, .NET, conectores de Spark y Kafka), la API REST de SQL y las herramientas de socios (BI, ETL, dbt).

#### ¿Qué es Snowsight?

La interfaz web de Snowflake para escribir worksheets de SQL y Python, notebooks y dashboards, explorar datos, monitorear consultas y costos, y administrar la cuenta.

#### ¿Qué es Snowflake Horizon?

Las capacidades integradas de gobierno y catálogo de Snowflake: control de acceso, clasificación de datos sensibles, políticas de enmascaramiento y de acceso a filas, etiquetas, linaje, monitoreo de la calidad de datos, auditoría y descubrimiento, aplicadas a tablas, tablas Iceberg y datos compartidos.

#### ¿Qué diferencia hay entre Snowflake y un warehouse MPP tradicional como Teradata o Redshift (aprovisionado)?

Los warehouses MPP tradicionales acoplan almacenamiento y cómputo en los mismos nodos, así que escalar implica redistribuir datos, y todas las cargas comparten un cluster. Snowflake mantiene el almacenamiento centralizado y permite arrancar warehouses independientes en segundos, sin índices, claves de distribución ni vacuum que administrar.

#### ¿Qué papel cumplen la URL y el localizador de la cuenta?

El identificador de cuenta (nombre de la organización más nombre de la cuenta, o el antiguo localizador con la región) forma la URL a la que se conectan los clientes, por ejemplo `myorg-myaccount.snowflakecomputing.com`.

#### ¿Qué es el contexto de una sesión de Snowflake?

El rol, el warehouse, la base de datos y el esquema actuales de una sesión (`USE ROLE`, `USE WAREHOUSE`, `USE DATABASE`, `USE SCHEMA`). Las consultas corren con los privilegios del rol actual en el warehouse actual, y los nombres sin calificar se resuelven en la base y el esquema actuales.

### Almacenamiento y micro-particiones

#### ¿Qué es una micro-partición?

La unidad física de almacenamiento de una tabla de Snowflake: un archivo inmutable de 50 a 500 MB de datos sin comprimir (mucho menos comprimido), guardado en formato columnar. Snowflake las crea automáticamente al cargar los datos, en el orden en que llegan.

#### ¿Qué metadatos guarda Snowflake por micro-partición?

El rango de valores (mínimo y máximo) de cada columna, el número de valores distintos, el número de nulos y otras estadísticas. El optimizador los usa para saltarse las micro-particiones que no pueden contener filas que coincidan.

#### ¿Qué es el pruning?

Saltarse micro-particiones durante una lectura porque sus metadatos muestran que no pueden cumplir el filtro. Un buen pruning es la razón principal por la que las consultas sobre tablas enormes pueden ser rápidas. Aparece en el query profile como "partitions scanned" frente a "partitions total".

#### ¿Por qué las micro-particiones son inmutables y qué hace un update?

La inmutabilidad simplifica la concurrencia, el Time Travel y el clonado. Un `UPDATE` o `DELETE` escribe micro-particiones nuevas con las filas modificadas y marca las antiguas como no vigentes; las antiguas se conservan para Time Travel y Fail-safe.

#### ¿Qué es el clustering de datos en Snowflake?

Qué tan juntas quedan, en las mismas micro-particiones, las filas con valores parecidos de una columna. Los datos cargados por orden de fecha quedan naturalmente bien agrupados por fecha. El clustering se degrada cuando el DML dispersa los valores en muchas particiones.

#### ¿Qué es una clustering key?

Una o más columnas o expresiones declaradas en una tabla grande (`CLUSTER BY (event_date, customer_id)`) para que el servicio de Automatic Clustering reorganice las micro-particiones en segundo plano y mantenga juntos los valores parecidos, lo que mejora el pruning en los filtros sobre esas columnas.

#### ¿Cuándo conviene definir una clustering key?

En tablas muy grandes (de varios terabytes) en las que las consultas filtran por columnas que no están naturalmente agrupadas y el query profile muestra un pruning pobre. El clustering cuesta créditos de reagrupamiento, así que no compensa en tablas pequeñas o que se reescriben completas con frecuencia.

#### ¿Cómo se comprueba qué tan bien agrupada está una tabla?

Con `SYSTEM$CLUSTERING_INFORMATION('tabla', '(col)')`, que informa la profundidad media y el solapamiento de las micro-particiones. Menos profundidad significa mejor clustering.

#### ¿Cómo se comprimen los datos en Snowflake?

Automáticamente, por columna, con la mejor codificación para los datos. No eliges la compresión; el almacenamiento se factura sobre el tamaño comprimido.

#### ¿Qué tipos de tabla hay en Snowflake?

Tablas permanentes (Time Travel y 7 días de Fail-safe), transitorias (Time Travel de 0 o 1 día, sin Fail-safe, más baratas para datos que se pueden reconstruir), temporales (solo existen durante la sesión), externas (leen archivos de un stage), tablas Iceberg, tablas híbridas (orientadas a filas, para cargas transaccionales) y dynamic tables.

#### ¿Qué son las tablas Iceberg en Snowflake?

Tablas guardadas en formato Apache Iceberg en tu propio almacenamiento en la nube (un external volume). Con Snowflake como catálogo se comportan casi como tablas nativas; con un catálogo externo (AWS Glue, Snowflake Open Catalog/Apache Polaris y otros) Snowflake puede leerlas y, en algunos casos, escribirlas. Otros motores (Spark, Trino) pueden trabajar sobre los mismos datos.

#### ¿Qué son las tablas híbridas?

Tablas optimizadas para lecturas y escrituras de una sola fila con baja latencia y alta concurrencia, con claves primarias e índices que sí se aplican, y que se pueden unir con tablas analíticas en la misma consulta. Apuntan a cargas transaccionales ligeras (Unistore).

#### ¿Qué es una tabla externa?

Una tabla de solo lectura cuyos datos se quedan en archivos de un stage externo (S3, GCS, Azure). Snowflake guarda los metadatos a nivel de archivo y tú consultas los archivos con SQL. Es más lenta que las tablas nativas; hoy suelen preferirse las tablas Iceberg.

#### ¿Cómo se factura el almacenamiento?

Sobre el promedio mensual de bytes comprimidos de las tablas, los datos de Time Travel y Fail-safe y los archivos en stages, a una tarifa por TB que depende de la modalidad (capacidad o bajo demanda) y de la región.

#### ¿Qué hace `ALTER TABLE … SUSPEND RECLUSTER`?

Pausa el clustering automático de una tabla y detiene los costos de reagrupamiento, por ejemplo durante un backfill grande; `RESUME RECLUSTER` lo vuelve a activar.

#### ¿Qué diferencia hay entre el clustering natural de una columna y una clustering key?

El clustering natural viene del orden en que se cargaron los datos y no cuesta nada; una clustering key le pide a Snowflake mantener un orden mediante reagrupamiento en segundo plano, lo que cuesta créditos pero mantiene un buen pruning a pesar del DML.

#### ¿Cómo se ve cuánto almacenamiento usan Time Travel y Fail-safe?

En `ACCOUNT_USAGE.TABLE_STORAGE_METRICS`, que informa por tabla los bytes activos, los de Time Travel, los de Fail-safe y los retenidos por clones.

### Virtual warehouses y cómputo

#### ¿Qué pasa cuando se suspende un warehouse?

Deja de consumir créditos y se borra su caché local. Con auto-resume, la siguiente consulta lo vuelve a encender en uno o dos segundos.

#### ¿Qué son auto-suspend y auto-resume?

Ajustes que suspenden un warehouse tras cierto número de segundos de inactividad y lo reanudan automáticamente cuando llega una consulta. Un auto-suspend corto (por ejemplo 60 segundos) ahorra créditos en cargas intermitentes; uno más largo mantiene caliente el caché para BI.

#### ¿Qué es un warehouse multi-cluster?

Una función de Enterprise en la que un warehouse puede ejecutar varios clusters del mismo tamaño, entre un mínimo y un máximo, para absorber la concurrencia. Los clusters adicionales arrancan cuando las consultas hacen cola y se detienen cuando baja la carga.

#### ¿Qué diferencia hay entre escalar hacia arriba y hacia afuera?

Escalar hacia arriba (un warehouse más grande) acelera las consultas complejas individuales y reduce el spilling. Escalar hacia afuera (más clusters en un warehouse multi-cluster) atiende a más usuarios concurrentes sin colas; no acelera una consulta individual.

#### ¿Cuáles son las políticas de escalado multi-cluster?

Standard (arranca clusters rápidamente para evitar colas, priorizando el rendimiento) y Economy (solo arranca un cluster si hay carga suficiente para mantenerlo ocupado varios minutos, priorizando el costo).

#### ¿Cómo se separan las cargas de trabajo en Snowflake?

Con warehouses distintos por carga (ingesta, transformación, BI, ciencia de datos, consultas ad hoc), cada uno con su tamaño y su suspensión adecuados, para que nunca compitan por el cómputo y sus costos se vean por separado.

#### ¿Qué son las colas de consultas y cómo se reducen?

Las consultas esperan cuando un warehouse está en su límite de concurrencia (`MAX_CONCURRENCY_LEVEL`, 8 por defecto). Soluciones: warehouses multi-cluster, warehouses separados por carga, consultas más rápidas o un warehouse más grande.

#### ¿Qué es un warehouse optimizado para Snowpark?

Un warehouse con mucha más memoria por nodo, para cargas de Snowpark que usan mucha memoria, como el entrenamiento de ML o el procesamiento con UDF grandes.

#### ¿Qué es el Query Acceleration Service?

Una función serverless que descarga partes de las lecturas y filtros grandes de las consultas elegibles a un cómputo compartido, para que las consultas atípicas terminen antes sin cambiar el tamaño de todo el warehouse. Se activa por warehouse con un límite de factor de escala.

#### ¿Qué son los warehouses estándar Gen2?

Una nueva generación de warehouses estándar con hardware más rápido y mejoras del motor, sobre todo para el DML y las lecturas grandes, facturados a una tarifa de créditos algo más alta. Se pueden elegir por warehouse.

#### ¿Qué es el timeout de sentencias?

`STATEMENT_TIMEOUT_IN_SECONDS`, definido en un warehouse, un usuario o una sesión, cancela las consultas que superan el límite. Definirlo evita que una consulta descontrolada queme créditos durante horas.

#### ¿Una consulta en curso aprovecha un warehouse redimensionado?

El cambio de tamaño afecta a las consultas nuevas; las que están en curso terminan con los recursos actuales. Al escalar hacia arriba se aprovisionan recursos nuevos en segundo plano, y las consultas en cola y nuevas los aprovechan cuando están listos.

#### ¿Qué controla `MAX_CONCURRENCY_LEVEL`?

El número de sentencias SQL concurrentes que ejecuta un cluster de warehouse antes de poner las demás en cola. Bajarlo da más recursos a cada consulta; subirlo permite más consultas en paralelo con el riesgo de ralentizar cada una.

#### ¿Cómo se elige el tamaño inicial de un warehouse?

Empieza pequeño (X-Small o Small) para desarrollo y cargas sencillas, prueba consultas representativas y sube de tamaño solo cuando las consultas derraman, tardan demasiado o no cumplen el tiempo objetivo. Mide el costo por ejecución, no solo la duración.

### Caché

#### ¿Qué cachés tiene Snowflake?

El caché de resultados (en la capa de servicios: los resultados se reutilizan durante 24 horas si la consulta y los datos no cambiaron), el caché del warehouse (datos de micro-particiones en el SSD local del warehouse mientras está encendido) y el caché de metadatos (estadísticas que responden algunas consultas como `COUNT(*)` o `MIN` sin warehouse).

#### ¿Cuándo se usa el caché de resultados?

Cuando el mismo texto de consulta se vuelve a ejecutar, los datos no cambiaron, el usuario tiene los privilegios necesarios y la consulta no usa funciones no deterministas como `CURRENT_TIMESTAMP()`. Cada reutilización extiende la retención, hasta 31 días. No cuesta cómputo.

#### ¿Cómo influye el caché del warehouse en el auto-suspend?

Suspender borra el caché local, así que las consultas siguientes leen del almacenamiento remoto y son más lentas. Para dashboards que consultan los mismos datos una y otra vez, un auto-suspend más largo puede ser más rápido sin costar mucho más.

#### ¿Cómo se desactiva el caché de resultados para hacer pruebas?

`ALTER SESSION SET USE_CACHED_RESULT = FALSE;` para que las consultas de benchmark se ejecuten de verdad.

#### ¿El caché de resultados funciona entre usuarios?

Sí, si el rol del otro usuario tiene los privilegios necesarios sobre los objetos y el texto de la consulta es idéntico; los resultados no están atados al usuario original.

#### ¿Por qué una consulta repetida puede no usar el caché de resultados?

Los datos cambiaron, el texto de la consulta es distinto (incluso por espacios o mayúsculas en algunos casos), usa funciones no deterministas, consulta funciones externas o algunas funciones de tabla, el resultado superó su retención, o el caché está desactivado en la sesión.

### Carga de datos

#### ¿Qué formas hay de cargar datos en Snowflake?

Carga masiva con `COPY INTO` desde stages, carga continua con Snowpipe (archivos) y Snowpipe Streaming (filas), el conector de Kafka, Openflow y herramientas ETL/ELT de socios, sentencias `INSERT`, tablas externas e Iceberg para consultar en su lugar, y el uso compartido de datos para los datos de otras cuentas.

#### ¿Qué es un stage?

Una ubicación para archivos que se cargan o descargan. Los stages internos están dentro de Snowflake: de usuario (`@~`), de tabla (`@%tabla`) y con nombre. Los stages externos apuntan a contenedores de S3, GCS o Azure, normalmente a través de una storage integration.

#### ¿Qué es una storage integration?

Un objeto de cuenta que guarda una identidad de nube (en AWS, un rol IAM que Snowflake asume) y las ubicaciones permitidas, para que los stages externos accedan a los buckets sin guardar credenciales en el SQL.

```sql
CREATE STORAGE INTEGRATION s3_lake
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/snowflake-lake'
  STORAGE_ALLOWED_LOCATIONS = ('s3://my-lake/raw/');

CREATE STAGE raw_stage URL = 's3://my-lake/raw/' STORAGE_INTEGRATION = s3_lake;
```

#### ¿Qué es un objeto file format?

Una definición con nombre de cómo leer los archivos: tipo (CSV, JSON, Avro, ORC, Parquet, XML), delimitadores, manejo del encabezado, cadenas nulas, compresión, formatos de fecha. Los stages y las sentencias `COPY` lo referencian.

#### ¿Cómo funciona `COPY INTO <tabla>`?

Carga en paralelo los archivos de un stage en una tabla, usando un file format, con opciones de manejo de errores y transformaciones en un `SELECT`. Guarda 64 días de metadatos de carga por tabla, así que por defecto omite los archivos ya cargados.

```sql
COPY INTO raw.orders
FROM @raw_stage/orders/
FILE_FORMAT = (TYPE = 'PARQUET')
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
ON_ERROR = 'ABORT_STATEMENT';
```

#### ¿Qué opciones de `ON_ERROR` existen en `COPY`?

`ABORT_STATEMENT` (por defecto en las cargas masivas), `CONTINUE` (omite las filas defectuosas), `SKIP_FILE`, `SKIP_FILE_<n>` o `SKIP_FILE_<n>%` (omite un archivo con demasiados errores). Usa `VALIDATION_MODE = RETURN_ERRORS` para probar una carga sin cargar, y la función `VALIDATE` para ver los errores de una carga anterior.

#### ¿Cuál es el tamaño ideal de archivo para cargar?

Más o menos 100–250 MB comprimidos por archivo. Muchos archivos diminutos añaden sobrecarga; un solo archivo enorme no se puede cargar en paralelo. Divide los archivos grandes y agrupa los pequeños.

#### ¿Qué es Snowpipe?

Un servicio serverless que carga archivos de forma continua a medida que llegan a un stage, con una sentencia `COPY` definida en un pipe. Con auto-ingest, lo disparan las notificaciones de eventos de la nube (eventos de S3 vía SQS, Event Grid, Pub/Sub); si no, se llama a su API REST. La latencia suele ser de alrededor de un minuto.

```sql
CREATE PIPE raw.orders_pipe AUTO_INGEST = TRUE AS
COPY INTO raw.orders FROM @raw_stage/orders/ FILE_FORMAT = (TYPE = 'JSON');
```

#### ¿Cómo se factura Snowpipe y por qué importa el tamaño de los archivos?

Por cómputo serverless más una pequeña sobrecarga por archivo (en la tarifa reciente, un monto fijo por GB ingerido). Con archivos muy pequeños domina la sobrecarga, así que los productores deberían agrupar los datos en archivos de tamaño razonable, idealmente enviados cada minuto más o menos y no por cada evento.

#### ¿Qué es Snowpipe Streaming?

Una API (mediante el SDK de Java o Python, el conector de Kafka u Openflow) que escribe filas directamente en las tablas con segundos de latencia, sin pasar por archivos en stages. Sirve para flujos de eventos; su arquitectura de alto rendimiento se factura por volumen de datos.

#### ¿Cómo se descargan datos de Snowflake?

Con `COPY INTO @stage/ruta/ FROM (SELECT ...)`, que escribe archivos CSV, JSON o Parquet en un stage interno o externo, con opciones de particionado (`PARTITION BY`), tamaño de archivo y encabezados. Luego `GET` descarga los archivos de los stages internos.

#### ¿Qué son `PUT` y `GET`?

Comandos de cliente (SnowSQL, CLI, drivers) para subir archivos locales a un stage interno (`PUT`, que los comprime y cifra) y descargarlos de él (`GET`).

#### ¿Qué es la detección de esquema con `INFER_SCHEMA`?

Una función que lee archivos Parquet, Avro, ORC, JSON o CSV en un stage y devuelve los nombres y tipos de las columnas; combinada con `CREATE TABLE … USING TEMPLATE`, crea una tabla a partir de la estructura de los archivos. Las tablas también pueden activar la evolución de esquema para añadir columnas nuevas durante las cargas.

#### ¿Qué es la opción `FORCE` de `COPY`?

`FORCE = TRUE` vuelve a cargar los archivos aunque los metadatos digan que ya se cargaron, lo que puede crear duplicados; se usa a propósito para recargas tras vaciar una tabla.

#### ¿Cómo maneja `COPY` los archivos de más de 64 días?

Los metadatos de carga vencen a los 64 días, así que para los archivos más viejos Snowflake puede no saber si se cargaron. `LOAD_UNCERTAIN_FILES = TRUE` los carga de todos modos; para evitar la ambigüedad, mueve o borra los archivos una vez cargados, o usa Snowpipe, que guarda 14 días de historial por pipe.

#### ¿Cómo se transforman los datos durante el `COPY`?

Con un `SELECT` sobre los archivos del stage dentro de la sentencia `COPY`: reordenar u omitir columnas, convertir tipos, usar las posiciones `$1`, `$2` o `$1:campo` para datos semiestructurados, y añadir `METADATA$FILENAME` o `METADATA$FILE_ROW_NUMBER` para el linaje.

#### ¿Cómo se consultan archivos en un stage sin cargarlos?

`SELECT $1, $2, METADATA$FILENAME FROM @stage/ruta (FILE_FORMAT => 'my_csv')`, útil para inspeccionar los archivos antes de cargarlos.

#### ¿Qué es Openflow?

El servicio administrado de integración de datos de Snowflake, basado en Apache NiFi, con conectores para bases de datos, aplicaciones SaaS y flujos, desplegado en Snowflake o en tu propia nube (bring your own cloud), para ingerir datos estructurados y no estructurados.

#### ¿Cómo se carga en Snowflake una base relacional con CDC?

Con una herramienta de CDC (conectores de Openflow, Debezium con Kafka y el conector de Kafka para Snowflake, Fivetran, AWS DMS escribiendo en S3 más Snowpipe) que deja los eventos de cambio en tablas raw, y luego un `MERGE` desde un stream o una dynamic table para aplicarlos a la tabla de estado actual.

### Datos semiestructurados

#### ¿Qué es el tipo de dato `VARIANT`?

Un tipo que puede contener cualquier valor de tipo JSON (objeto, arreglo, cadena, número, booleano, nulo) hasta un límite de tamaño. Snowflake guarda internamente en forma columnar las claves que aparecen con frecuencia, así que las consultas sobre ellas pueden hacer pruning y ser rápidas.

#### ¿Cómo se consulta un JSON guardado en un `VARIANT`?

Con la notación de rutas y conversiones de tipo:

```sql
SELECT payload:customer.id::NUMBER       AS customer_id,
       payload:items[0]:sku::STRING       AS first_sku
FROM raw.events
WHERE payload:type::STRING = 'purchase';
```

#### ¿Qué hace `FLATTEN`?

Una función de tabla que expande un arreglo o un objeto en una fila por elemento, usada con `LATERAL` para desanidar datos.

```sql
SELECT e.payload:order_id::STRING AS order_id, i.value:sku::STRING AS sku
FROM raw.events e, LATERAL FLATTEN(input => e.payload:items) i;
```

#### ¿Qué son los tipos `OBJECT` y `ARRAY`?

Tipos semiestructurados para objetos clave-valor y arreglos. Funciones como `OBJECT_CONSTRUCT`, `ARRAY_AGG`, `ARRAY_CONTAINS` y `PARSE_JSON` los construyen e inspeccionan. Las versiones estructuradas (`OBJECT(name STRING, age NUMBER)`, `ARRAY(NUMBER)`) imponen los tipos de los elementos.

#### ¿Conviene guardar el JSON como `VARIANT` o aplanarlo en columnas?

Guarda el JSON en bruto como `VARIANT` en la capa de aterrizaje para tener flexibilidad y trazabilidad, y luego extrae los campos más consultados en columnas tipadas en las capas limpias: las columnas tipadas son más fáciles de usar, documentar y gobernar, y hacen pruning de forma predecible.

#### ¿Cómo se maneja un campo JSON que a veces es texto y a veces número?

Convirtiendo de forma defensiva con `TRY_CAST` o `TRY_TO_NUMBER`, que devuelven `NULL` en lugar de fallar, y revisando el tipo con `TYPEOF()` para poner en cuarentena los valores inesperados.

#### ¿Cómo se convierten filas relacionales en JSON?

Con `OBJECT_CONSTRUCT(*)` o `OBJECT_CONSTRUCT('id', id, 'name', name)` por fila, y `ARRAY_AGG` para agrupar filas en arreglos, útil para exportar documentos anidados o alimentar APIs.

#### ¿En qué se diferencia una clave ausente de un null de JSON?

Una clave ausente devuelve `NULL` de SQL; un valor JSON `null` es un nulo de `VARIANT`, que no es lo mismo que `NULL` de SQL (`IS_NULL_VALUE()` lo comprueba). Al convertir con `::STRING`, el null de JSON pasa a `NULL` de SQL.

#### ¿Cómo se cargan columnas de Parquet directamente en columnas de tabla?

Con `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE` en `COPY`, que asocia las columnas del archivo a las de la tabla por nombre, o seleccionando `$1:nombre_columna::tipo` de forma explícita.

### Funciones SQL

#### ¿Qué es `QUALIFY`?

Una cláusula que filtra sobre los resultados de las funciones de ventana, como `HAVING` para los agregados. Es la forma idiomática de deduplicar:

```sql
SELECT *
FROM raw.customers
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1;
```

#### ¿Qué hace `MERGE` en Snowflake?

Inserta, actualiza o borra filas de una tabla destino según una unión con un origen, en una sola sentencia atómica, típicamente para upserts y CDC.

```sql
MERGE INTO dw.customers t
USING staging.customers s ON t.customer_id = s.customer_id
WHEN MATCHED AND s.is_deleted THEN DELETE
WHEN MATCHED THEN UPDATE SET t.email = s.email, t.updated_at = s.updated_at
WHEN NOT MATCHED THEN INSERT (customer_id, email, updated_at)
  VALUES (s.customer_id, s.email, s.updated_at);
```

#### ¿Snowflake aplica las claves primarias y foráneas?

En las tablas estándar solo se aplica `NOT NULL`. Las restricciones de clave primaria, única y foránea son informativas: documentan el modelo y pueden ayudar a las herramientas de BI y al optimizador (con `RELY`), pero no impiden los duplicados. Las tablas híbridas sí las aplican.

#### ¿Qué son las secuencias y las columnas de identidad?

Las secuencias generan números únicos (`seq.NEXTVAL`), no necesariamente sin huecos. Las columnas `AUTOINCREMENT`/`IDENTITY` usan una secuencia por dentro. Muchos diseños de warehouse prefieren claves sustitutas basadas en hash, que son deterministas entre cargas.

#### ¿Para qué sirve `SAMPLE`?

Para leer una fracción aleatoria de una tabla (`SELECT * FROM t SAMPLE (1)` para el 1 % de las filas, o `SAMPLE BLOCK` por micro-particiones), útil para explorar y probar rápido sobre tablas grandes.

#### ¿Qué son las funciones definidas por el usuario en Snowflake?

Funciones escalares o de tabla escritas en SQL, JavaScript, Python, Java o Scala. Las UDF de Python corren en un sandbox seguro con paquetes de Anaconda o archivos subidos. Las UDF de Python vectorizadas procesan lotes con pandas para rendir mejor.

#### ¿Qué son los procedimientos almacenados en Snowflake?

Procedimientos escritos en Snowflake Scripting (SQL), JavaScript, Python, Java o Scala, usados para lógica procedural y administración. Se ejecutan con los derechos del propietario (por defecto) o con los del que llama.

#### ¿Qué es Snowflake Scripting?

Una extensión procedural de SQL con variables, `IF`, bucles, cursores, manejo de excepciones y `RETURN`, que se usa en procedimientos almacenados y bloques anónimos.

#### ¿Cómo son las transacciones en Snowflake?

ACID con nivel de aislamiento read committed. Cada sentencia hace autocommit salvo que esté dentro de un `BEGIN … COMMIT` explícito. El DDL hace commit implícito. El DML concurrente sobre la misma tabla puede quedar bloqueado hasta que termine la otra transacción.

#### ¿Qué hace `UNDROP`?

Restaura una tabla, esquema o base de datos borrados recientemente desde Time Travel, siempre que esté dentro del periodo de retención.

#### ¿Qué hace `SWAP WITH`?

`ALTER TABLE a SWAP WITH b` intercambia de forma atómica los nombres de dos tablas, una forma común de publicar una tabla reconstruida sin interrumpir a los lectores.

#### ¿Qué es `CREATE OR ALTER`?

Una sentencia que crea un objeto si no existe o lo modifica para que coincida con la definición si ya existe, conservando los datos y los permisos, útil para despliegues declarativos de tablas y otros objetos.

#### ¿Para qué sirven `PIVOT` y `UNPIVOT`?

Para rotar filas en columnas (por ejemplo los meses en columnas) y columnas en filas. `PIVOT` admite listas de valores dinámicas con `ANY` en las versiones recientes.

#### ¿Qué hace `MATCH_RECOGNIZE`?

Busca patrones en filas ordenadas (por ejemplo una secuencia de eventos en una sesión, como vista → carrito → compra) y devuelve las coincidencias con medidas, sin escribir self-joins complejos.

### Time Travel, Fail-safe y clonado

#### ¿Qué es Time Travel?

El acceso a datos históricos que se modificaron o borraron, durante un periodo de retención: 1 día por defecto, configurable hasta 90 días en Enterprise para las tablas permanentes. Puedes consultar, clonar o restaurar los datos a una fecha, un desfase o una sentencia.

```sql
SELECT * FROM orders AT (OFFSET => -3600);
SELECT * FROM orders BEFORE (STATEMENT => '01b2c3d4-...');
CREATE TABLE orders_restored CLONE orders AT (TIMESTAMP => '2026-10-15 08:00'::TIMESTAMP_LTZ);
```

#### ¿Qué es Fail-safe?

Un periodo de 7 días después del Time Travel durante el cual Snowflake puede recuperar los datos de las tablas permanentes en caso de desastre. Solo el soporte de Snowflake accede a él; no se puede consultar. Cuesta almacenamiento, por eso las tablas transitorias (sin Fail-safe) son más baratas.

#### ¿Cómo se define la retención de Time Travel?

Con `DATA_RETENTION_TIME_IN_DAYS` a nivel de cuenta, base de datos, esquema o tabla. Una retención larga en tablas con actualizaciones frecuentes aumenta bastante los costos de almacenamiento.

#### ¿Qué es el clonado zero-copy?

Crear al instante una copia de una tabla, esquema o base de datos con `CLONE`, sin copiar datos: el clon comparte las micro-particiones del original y solo los cambios nuevos consumen almacenamiento. Se usa para entornos de desarrollo y pruebas, respaldos antes de cambios riesgosos y fotos en un momento dado.

#### ¿Qué hereda un clon?

Los datos y la estructura, y en las bases de datos y esquemas, los objetos hijos. Los privilegios sobre el objeto origen no se copian salvo que uses `COPY GRANTS`; los privilegios sobre los objetos hijos sí se clonan. Los pipes que referencian stages internos, y algunos otros objetos, no se clonan.

#### ¿Cómo le das a un desarrollador una copia completa de los datos de producción a bajo costo?

Clonando la base de producción en una base de desarrollo (al instante, sin almacenamiento extra hasta que haya cambios), aplicando políticas de enmascaramiento o una capa de vistas seguras si los datos son sensibles, y dándole al desarrollador un rol sobre el clon.

#### ¿Qué pasa con el Time Travel si borras y vuelves a crear una tabla con el mismo nombre?

La tabla nueva es distinta; la borrada queda en Time Travel y solo se puede restaurar con `UNDROP` tras renombrar la nueva, porque los nombres deben ser únicos.

#### ¿Se puede clonar desde un momento del pasado?

Sí: `CREATE TABLE t_clone CLONE t AT (TIMESTAMP => ...)` o `BEFORE (STATEMENT => ...)`, siempre que esté dentro del periodo de retención. Es una forma común de recuperarse de un cambio erróneo conservando la tabla actual para comparar.

### Streams, tasks y dynamic tables

#### ¿Qué es un stream?

Un objeto que registra los cambios (inserciones, actualizaciones, borrados) hechos en una tabla, vista o tabla externa desde la última vez que se consumió, y los expone con las columnas `METADATA$ACTION`, `METADATA$ISUPDATE` y `METADATA$ROW_ID`. Consumirlo en una transacción DML avanza su offset.

#### ¿Qué tipos de streams existen?

Standard (todos los cambios, compensados entre sí), append-only (solo inserciones, más barato, para tablas con cargas de solo inserción) e insert-only para tablas externas e Iceberg.

#### ¿Qué es un task?

Una unidad programada o disparada que ejecuta una sentencia SQL, una llamada a un procedimiento o Snowflake Scripting, con un warehouse o cómputo serverless. Los tasks se pueden encadenar en DAG con `AFTER` y ejecutarse solo cuando un stream tiene datos con `WHEN SYSTEM$STREAM_HAS_DATA(...)`.

```sql
CREATE TASK load_orders
  WAREHOUSE = transform_wh
  SCHEDULE = '15 MINUTE'
  WHEN SYSTEM$STREAM_HAS_DATA('raw.orders_stream')
AS
  INSERT INTO dw.orders SELECT * FROM raw.orders_stream WHERE METADATA$ACTION = 'INSERT';

ALTER TASK load_orders RESUME;
```

#### ¿Qué es un task serverless?

Un task sin warehouse especificado, en el que Snowflake gestiona el tamaño del cómputo según las ejecuciones anteriores. Sirve para tasks pequeños y frecuentes, porque no aplica la facturación mínima de un warehouse.

#### ¿Qué es un triggered task?

Un task sin programación que se ejecuta cuando su stream tiene datos nuevos, reaccionando rápido a los cambios sin sondear a intervalos fijos.

#### ¿Qué es una dynamic table?

Una tabla definida por una consulta y un retraso objetivo (`TARGET_LAG = '10 minutes'`), que Snowflake mantiene actualizada automáticamente, de forma incremental cuando se puede. Reemplaza muchos pipelines de streams y tasks con SQL declarativo.

```sql
CREATE DYNAMIC TABLE dw.daily_sales
  TARGET_LAG = '30 minutes'
  WAREHOUSE = transform_wh
AS
SELECT order_date, SUM(amount) AS sales FROM dw.orders GROUP BY order_date;
```

#### Dynamic tables, vistas materializadas o streams y tasks: ¿cómo eliges?

Dynamic tables para pipelines declarativos con joins y agregaciones a la frescura elegida. Vistas materializadas para acelerar consultas repetidas sobre una sola tabla (sin joins), siempre al día. Streams y tasks para lógica procedural, un manejo propio del `MERGE` o efectos secundarios.

#### ¿Qué diferencia hay entre el refresco incremental y el completo en las dynamic tables?

El refresco incremental procesa solo los cambios de los orígenes desde el último refresco; el completo recalcula toda la consulta. Snowflake elige el incremental cuando la consulta lo admite; algunas construcciones (ciertas funciones no deterministas, algunos patrones de ventana) obligan a refrescos completos, que cuestan más.

#### ¿Qué es una vista materializada en Snowflake?

El resultado precalculado de una consulta sobre una tabla, mantenido de forma automática y transparente por un servicio en segundo plano (Enterprise). El optimizador puede usarla aunque consultes la tabla base. El mantenimiento cuesta créditos, así que se usa para consultas costosas y frecuentes sobre tablas que cambian poco.

#### ¿Qué le pasa a un stream que no se consume durante mucho tiempo?

Puede volverse obsoleto (stale) cuando su offset queda fuera del periodo de retención de la tabla de origen (Snowflake extiende la retención hasta 14 días para evitarlo en las tablas con streams). Un stream obsoleto se debe recrear, y puede hacer falta una recarga completa de los cambios.

#### ¿Cómo se monitorean los tasks?

Con `TASK_HISTORY` (función de tabla del information schema y vista de account usage), la vista del grafo de tasks en Snowsight, las notificaciones de error mediante una notification integration y `SYSTEM$TASK_DEPENDENTS_ENABLE` para reanudar grafos completos.

#### ¿Qué es un finalizer task?

Un task asociado a la raíz de un grafo de tasks que se ejecuta cuando terminan todos los demás, hayan tenido éxito o no, para limpieza o notificaciones.

#### ¿Se pueden encadenar dynamic tables?

Sí. Una dynamic table puede leer otras dynamic tables y formar un pipeline; `TARGET_LAG = DOWNSTREAM` significa que una tabla solo se refresca cuando lo necesitan las tablas que dependen de ella.

### Seguridad y control de acceso

#### ¿Cómo funciona el control de acceso en Snowflake?

Con control de acceso basado en roles (RBAC) combinado con control discrecional: los privilegios se conceden a roles, los roles se conceden a usuarios y a otros roles, y cada objeto tiene un rol propietario que lo controla.

#### ¿Cuáles son los roles definidos por el sistema?

ORGADMIN (organización), ACCOUNTADMIN (el rol más alto de la cuenta; úsalo con moderación), SECURITYADMIN (administra los permisos y puede administrar usuarios y roles), USERADMIN (crea usuarios y roles), SYSADMIN (crea warehouses y bases de datos; los roles propios deberían colgar de él) y PUBLIC (concedido a todos).

#### ¿Cómo es una buena jerarquía de roles?

Roles de acceso que tienen los privilegios sobre los objetos (por ejemplo `SALES_READ`, `SALES_WRITE`), roles funcionales que representan puestos o equipos (`ANALYST`, `DATA_ENGINEER`) a los que se conceden los roles de acceso, y roles funcionales que cuelgan de SYSADMIN para que los administradores puedan gestionarlo todo. Las cuentas de servicio tienen sus propios roles funcionales.

#### ¿Qué son los future grants?

Permisos que se aplican automáticamente a los objetos que se creen más adelante en un esquema o base de datos: `GRANT SELECT ON FUTURE TABLES IN SCHEMA sales.marts TO ROLE sales_read;`. Evitan que falten permisos en las tablas nuevas.

#### ¿Qué son los roles de base de datos?

Roles con alcance limitado a una base de datos, usados para gestionar el acceso dentro de ella y sobre todo para compartir accesos detallados mediante el uso compartido de datos.

#### ¿Qué son los esquemas de acceso administrado?

Esquemas en los que solo el propietario del esquema (o los roles con `MANAGE GRANTS`) puede conceder privilegios sobre los objetos, no los propietarios de cada objeto, lo que centraliza el control de acceso.

#### ¿Qué es una política de enmascaramiento?

Un objeto a nivel de esquema que reescribe el valor de una columna en el momento de la consulta según el contexto, típicamente el rol: los analistas ven `***@***` mientras un rol privilegiado ve el correo real. Se asocia a las columnas directamente o mediante etiquetas (Enterprise).

```sql
CREATE MASKING POLICY mask_email AS (val STRING) RETURNS STRING ->
  CASE WHEN IS_ROLE_IN_SESSION('PII_READER') THEN val ELSE '***MASKED***' END;

ALTER TABLE crm.customers MODIFY COLUMN email SET MASKING POLICY mask_email;
```

#### ¿Qué es una row access policy?

Una política que decide si una fila es visible para el contexto actual, asociada a una tabla o vista, a menudo con una tabla de correspondencia entre roles y regiones permitidas. Filtra las filas de forma transparente en todas las consultas.

#### ¿Qué es el enmascaramiento basado en etiquetas?

Asociar una política de enmascaramiento a una etiqueta, para que todas las columnas con esa etiqueta (por ejemplo `pii = 'email'`) se enmascaren automáticamente, incluidas las columnas nuevas en cuanto se etiquetan.

#### ¿Qué es la clasificación de datos?

Una función que analiza las columnas para detectar datos sensibles (correos, nombres, teléfonos, documentos de identidad) y sugiere o aplica etiquetas del sistema, que luego pueden guiar las políticas de enmascaramiento.

#### ¿Cómo se autentican los usuarios en Snowflake?

Con contraseñas más MFA (que Snowflake está volviendo obligatorio para el inicio de sesión con contraseña), SSO mediante proveedores de identidad SAML 2.0 (Okta, Entra ID), OAuth (de Snowflake o externo), autenticación con par de claves para los servicios, federación de identidades de carga de trabajo y tokens de acceso programático. Los usuarios de servicio deberían usar pares de claves u OAuth, no contraseñas.

#### ¿Qué son las network policies?

Reglas que permiten o bloquean direcciones IP de clientes (y network rules para endpoints privados) a nivel de cuenta o de usuario, para que solo puedan conectarse las redes corporativas o servicios concretos.

#### ¿Cómo se cifran los datos en Snowflake?

Siempre en reposo (AES-256) y en tránsito (TLS), con un modelo jerárquico de claves y rotación automática. Business Critical añade Tri-Secret Secure, que combina una clave administrada por el cliente con la clave de Snowflake.

#### ¿Qué son las vistas seguras y las UDF seguras?

Vistas y funciones cuya definición queda oculta para quienes no son propietarios y que desactivan algunas optimizaciones que podrían filtrar datos a través del comportamiento de las consultas. Son obligatorias para los objetos de un share.

#### ¿Para qué sirve la vista access history?

`SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY` registra qué columnas leyó y escribió cada consulta, lo que ayuda a la auditoría, al linaje y a encontrar datos sin uso.

#### ¿Qué diferencia hay entre `OWNERSHIP` y los demás privilegios?

El rol propietario de un objeto tiene control total, incluido conceder privilegios sobre él y borrarlo. Los demás privilegios (`SELECT`, `INSERT`, `USAGE`, `MONITOR`, `OPERATE`) permiten acciones concretas. La propiedad se transfiere con `GRANT OWNERSHIP`.

#### ¿Por qué ACCOUNTADMIN no debe ser el rol por defecto de nadie?

Tiene poder ilimitado, así que los errores o las sesiones comprometidas son catastróficos. Concédelo a pocos administradores con MFA, nunca lo uses para el trabajo diario ni para cuentas de servicio, y crea los objetos con SYSADMIN o roles propios.

#### ¿Qué son los roles secundarios?

`USE SECONDARY ROLES ALL` permite que una sesión use para las consultas los privilegios de todos los roles concedidos (el rol primario sigue siendo el propietario de los objetos creados), lo que simplifica el trabajo de quien tiene varios roles.

#### ¿Qué son las external access integrations?

Objetos que permiten a las UDF y procedimientos llamar a endpoints de red externos, controlados por network rules que listan los hosts permitidos y objetos secret para las credenciales.

### Uso compartido de datos y colaboración

#### ¿Qué es Secure Data Sharing?

Compartir datos vivos de solo lectura de una cuenta con otra sin copiarlos: el proveedor crea un share con bases de datos, esquemas, tablas y vistas seguras, y el consumidor crea una base de datos a partir de él. El consumidor paga el cómputo que usa; el proveedor paga el almacenamiento.

#### ¿Se puede compartir con alguien que no tiene cuenta de Snowflake?

Sí, mediante una reader account que el proveedor crea y paga, con capacidades limitadas.

#### ¿Cómo funciona el uso compartido entre regiones o nubes?

Los datos se deben replicar en una cuenta de la región del consumidor, o compartir mediante listings con auto-fulfillment entre nubes, que replica los datos automáticamente.

#### ¿Qué es el Snowflake Marketplace?

Un catálogo de listings donde los proveedores publican datasets gratuitos o de pago, servicios de datos y Native Apps que los consumidores pueden obtener directamente en sus cuentas.

#### ¿Qué son las data clean rooms?

Entornos donde varias partes combinan datos para analizarlos (por ejemplo el solapamiento de audiencias) bajo políticas que solo permiten consultas aprobadas y resultados agregados, sin exponerse los registros en bruto entre sí.

#### ¿Qué es una Native App?

Una aplicación empaquetada con código y datos que un proveedor distribuye por el Marketplace y que se ejecuta dentro de la cuenta del consumidor, de modo que los datos del consumidor no salen de ella.

#### ¿Qué no puedes hacer como consumidor con datos compartidos?

No puedes modificarlos, clonarlos ni volver a compartirlos (salvo con ajustes concretos del proveedor), y el Time Travel no está disponible sobre los objetos compartidos. Puedes consultarlos, unirlos con tus datos y crear vistas encima.

#### ¿Qué es un listing?

Una oferta empaquetada de un share o una Native App con metadatos, condiciones y analítica de uso, publicada de forma privada a cuentas elegidas o de forma pública en el Marketplace.

### Snowpark, Python e IA

#### ¿Qué es Snowpark?

Un conjunto de librerías y entornos de ejecución para procesar datos en Snowflake con Python, Java o Scala. Las operaciones DataFrame se traducen a SQL y se ejecutan en un warehouse, así que los datos no salen de Snowflake.

```python
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, sum as sum_

session = Session.builder.configs(connection_params).create()
daily = (session.table("dw.orders")
         .filter(col("status") == "paid")
         .group_by("order_date")
         .agg(sum_("amount").alias("sales")))
daily.write.save_as_table("dw.daily_sales", mode="overwrite")
```

#### ¿Qué es la API pandas on Snowflake?

Una API compatible con pandas (Snowpark pandas, mediante Modin) que ejecuta código pandas sobre el cómputo de Snowflake, para que la sintaxis conocida de pandas escale a tablas grandes.

#### ¿Qué son los Snowflake Notebooks?

Notebooks en Snowsight que combinan celdas de SQL, Python y Markdown y corren sobre un warehouse o sobre cómputo de contenedores, para exploración, ingeniería de datos y ML.

#### ¿Qué es Snowpark Container Services?

Un entorno administrado de contenedores dentro de Snowflake para ejecutar cualquier aplicación, servicio o modelo de ML en contenedores (incluso con GPU) junto a los datos, gobernado por la seguridad de Snowflake.

#### ¿Qué es Snowflake Cortex?

La capa de IA de Snowflake: funciones de LLM que se llaman desde SQL (`AI_COMPLETE`, `AI_CLASSIFY`, `AI_EXTRACT`, `AI_SENTIMENT`, resumen, traducción), Cortex Search para recuperación, Cortex Analyst para preguntas en lenguaje natural sobre modelos semánticos, y agentes.

#### ¿Qué es Streamlit in Snowflake?

Una forma de construir y alojar aplicaciones de datos de Streamlit directamente en Snowflake, que se ejecutan con el gobierno de la cuenta y se comparten mediante roles.

#### ¿Qué es el ecosistema de ML de Snowflake?

Snowflake ML incluye un feature store, un registro de modelos, entrenamiento e inferencia distribuidos en warehouses o contenedores y observabilidad de ML, para construir y servir los modelos donde están los datos.

#### ¿Cuándo usarías Snowpark en lugar de SQL?

Para lógica que es más fácil en Python (reglas complejas de texto o de negocio, ingeniería de features para ML, reutilizar librerías Python), para código de transformación con pruebas unitarias, o para equipos más cómodos con DataFrames. Para transformaciones sencillas, SQL suele ser más simple e igual de rápido.

#### ¿Cómo llegan los paquetes Python a Snowflake?

Desde el canal Anaconda de Snowflake (listados en `PACKAGES`), desde wheels o zips subidos a un stage (`IMPORTS`), o mediante repositorios de artefactos que traen paquetes de PyPI.

### Rendimiento

#### ¿Cómo averiguas por qué una consulta es lenta?

Abre el Query Profile: mira los operadores más costosos, las particiones leídas frente al total (pruning), los bytes derramados (spill) al almacenamiento local y remoto, los joins que explotan (muchas más filas de salida que de entrada) y el tiempo en cola. `GET_QUERY_OPERATOR_STATS` da los mismos datos en SQL.

#### ¿Qué es el spilling y cómo se corrige?

Cuando un warehouse no tiene memoria suficiente para una operación, derrama datos al disco local y luego al almacenamiento remoto, que es mucho más lento. Se corrige con un warehouse más grande, procesando menos datos (mejores filtros, preagregación) o dividiendo la consulta.

#### ¿Qué causa un "join que explota"?

Un join sobre una clave que no es única, o condiciones de join incompletas, de modo que cada fila coincide con muchas y la salida se multiplica. Verifica la unicidad de las claves y que cada join tenga la condición completa.

#### ¿Cómo se mejora el pruning?

Filtrando por columnas correlacionadas con el orden de carga (fechas), añadiendo una clustering key en las tablas grandes filtradas por otras columnas, evitando envolver las columnas de filtro en funciones que impiden el pruning y filtrando lo antes posible.

#### ¿Qué es el Search Optimization Service?

Una función de Enterprise que construye una ruta de búsqueda persistente para una tabla, de modo que las búsquedas puntuales y los filtros selectivos (igualdad, `IN`, búsquedas de subcadenas y regex, campos `VARIANT`, geo) puedan saltarse la mayoría de las micro-particiones. Cuesta almacenamiento y créditos de mantenimiento.

#### ¿Por qué evitar `SELECT *` en Snowflake?

El almacenamiento es columnar, así que leer solo las columnas necesarias escanea muchos menos datos. `SELECT *` sobre tablas anchas lee todas las columnas y ralentiza las consultas y las extracciones de BI.

#### ¿Cómo se aceleran muchas sentencias `INSERT` pequeñas?

No haciéndolas: Snowflake está optimizado para operaciones por conjuntos. Agrupa las filas en archivos y usa `COPY`, usa Snowpipe Streaming para filas continuas, o inserta en sentencias grandes de varias filas.

#### ¿Sirve un `ORDER BY` en un `CREATE TABLE AS`?

Sí, en las cargas iniciales de tablas grandes: ordenar por las columnas de filtro principales produce micro-particiones bien agrupadas desde el principio, lo que mejora el pruning sin pagar el clustering automático.

#### ¿Qué errores comunes hacen lento a Snowflake?

DML de una fila en bucles, `SELECT *`, funciones sobre las columnas de filtro, joins con tipos distintos, listas `IN` enormes, warehouses demasiado pequeños que derraman, warehouses demasiado grandes para consultas triviales (costo) y vistas complejas apiladas en muchos niveles.

#### ¿Qué muestra `EXPLAIN` en Snowflake?

El plan lógico de una consulta sin ejecutarla: operadores, orden de los joins y particiones a leer (según los metadatos), útil para revisar el pruning antes de lanzar una consulta costosa.

#### ¿Cómo se acelera una consulta con `DISTINCT` sobre datos enormes?

Comprobando si de verdad hace falta deduplicar (a menudo un join multiplicó las filas), deduplicando antes y sobre menos columnas, usando `APPROX_COUNT_DISTINCT` (HyperLogLog) cuando basta una estimación, y usando un warehouse más grande si derrama.

#### ¿Para qué sirven las funciones aproximadas?

`APPROX_COUNT_DISTINCT`, `APPROX_PERCENTILE` y `APPROX_TOP_K` dan estimaciones con un error pequeño usando mucha menos memoria y tiempo, lo que sirve para dashboards y exploración sobre tablas muy grandes.

### Gestión de costos

#### ¿Qué impulsa los costos de Snowflake?

El cómputo de los warehouses (de lejos lo más grande para la mayoría de los clientes), las funciones serverless (Snowpipe, clustering, vistas materializadas, search optimization, tasks, funciones de IA), el almacenamiento (incluidos Time Travel y Fail-safe), los servicios en la nube por encima del 10 % del cómputo y la transferencia de datos fuera de la región.

#### ¿Qué es un resource monitor?

Un objeto que sigue el consumo de créditos de los warehouses o de la cuenta durante un periodo y puede notificar, suspender cuando terminen las consultas en curso o suspender de inmediato al alcanzar umbrales.

```sql
CREATE RESOURCE MONITOR monthly_bi WITH CREDIT_QUOTA = 500
  FREQUENCY = MONTHLY START_TIMESTAMP = IMMEDIATELY
  TRIGGERS ON 80 PERCENT DO NOTIFY
           ON 100 PERCENT DO SUSPEND;
ALTER WAREHOUSE bi_wh SET RESOURCE_MONITOR = monthly_bi;
```

#### ¿Cómo ves en qué se gastan los créditos?

Con `SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY`, `QUERY_HISTORY` (con `QUERY_ATTRIBUTION_HISTORY` para el costo por consulta), `METERING_DAILY_HISTORY` para las funciones serverless, las páginas de gestión de costos de Snowsight, los presupuestos, y las etiquetas de objetos o de consultas para la atribución.

#### ¿Qué son los query tags?

Un parámetro de sesión (`ALTER SESSION SET QUERY_TAG = 'dbt:daily_sales'`) que se guarda con cada consulta en el historial, usado para atribuir costos y encontrar consultas por job, herramienta o equipo.

#### ¿Qué son los presupuestos (budgets) en Snowflake?

Límites de gasto para la cuenta o para grupos de objetos, con notificaciones cuando el gasto proyectado supera el límite, que ayudan a los equipos a seguir los costos serverless y de warehouses.

#### ¿Cómo se reducen los costos de los warehouses?

Dimensionando bien cada warehouse según su carga, usando un auto-suspend corto, evitando los warehouses siempre encendidos, juntando los jobs pequeños en warehouses compartidos, usando multi-cluster con la política Economy donde las colas son aceptables, definiendo timeouts, optimizando las consultas más caras y usando resource monitors.

#### ¿Cómo se reducen los costos de almacenamiento?

Usando tablas transitorias para staging y datos reconstruibles, acortando el Time Travel en las tablas con mucha rotación, borrando tablas sin uso y clones que divergieron, limpiando los archivos viejos de los stages y evitando guardar muchas copias completas en lugar de clones.

#### ¿Un warehouse más grande siempre es más caro?

No necesariamente. Si una consulta se paraleliza bien, duplicar el tamaño reduce a la mitad el tiempo con el doble de tarifa, así que el costo es parecido y el resultado llega antes. Es más caro cuando las consultas son pequeñas o no se paralelizan.

#### ¿Por qué es caro un warehouse que ejecuta una consulta de un segundo cada minuto?

Cada reanudación factura al menos 60 segundos, y el auto-suspend lo mantiene encendido durante el tiempo de inactividad configurado tras cada consulta. Una consulta por minuto puede dejarlo encendido todo el tiempo. Agrupa esas consultas, usa tasks serverless o un único warehouse pequeño compartido.

#### ¿Cómo funciona el ajuste de los servicios en la nube?

El uso de servicios en la nube es gratis hasta el 10 % del cómputo diario de los warehouses; solo se factura el exceso. Las operaciones intensivas en metadatos (muchas consultas diminutas, comandos `SHOW`, clones frecuentes) pueden superarlo.

### Operación y protección de datos

#### ¿Qué diferencia hay entre `ACCOUNT_USAGE` e `INFORMATION_SCHEMA`?

Las vistas de `SNOWFLAKE.ACCOUNT_USAGE` cubren toda la cuenta, guardan un año de historial e incluyen los objetos borrados, pero tienen latencia (de minutos a unas horas). Las vistas y funciones de tabla de `INFORMATION_SCHEMA` son por base de datos, en tiempo real, y guardan menos historial (7–14 días para el historial de consultas).

#### ¿Qué es la replicación de bases de datos?

Copiar bases de datos (y, con los grupos de replicación, otros objetos como usuarios, roles, warehouses e integraciones) a cuentas de otras regiones o nubes, refrescadas según una programación, para recuperación ante desastres, uso compartido de datos o migraciones.

#### ¿Qué son los failover groups y el client redirect?

Los failover groups (Business Critical) permiten promover una cuenta secundaria a primaria para los objetos replicados durante una caída. El client redirect usa una URL de conexión que se puede cambiar a la nueva primaria, para que las aplicaciones se reconecten sin cambiar su configuración.

#### ¿Cómo se administran los objetos de Snowflake como código?

Con Terraform (el provider de Snowflake) para los objetos de cuenta como warehouses, roles, permisos, bases de datos e integraciones; dbt o schemachange para los cambios de esquema y las transformaciones; y la Snowflake CLI o `EXECUTE IMMEDIATE FROM` con repositorios Git en Snowflake para desplegar archivos SQL.

#### ¿Qué es un objeto Git repository en Snowflake?

Una integración que clona un repositorio Git dentro de Snowflake para ejecutar desde él archivos SQL y Python, referenciarlos en notebooks y procedimientos, y desplegar desde una rama o un tag.

#### ¿Cómo se generan alertas sobre problemas de datos dentro de Snowflake?

Con alerts (condiciones programadas que ejecutan una acción, como enviar un correo o una notificación por webhook), las data metric functions (monitoreo de calidad de datos de Horizon: nulos, duplicados, frescura, métricas propias) y las notificaciones de error de los tasks.

#### ¿Qué son las data metric functions?

Funciones (del sistema, como `NULL_COUNT`, `DUPLICATE_COUNT`, `FRESHNESS`, o propias) asociadas a tablas y ejecutadas según una programación, cuyos resultados se guardan para monitorear la calidad de los datos en el tiempo.

#### ¿Qué es la event table?

Una tabla especial que recoge los logs, trazas y métricas emitidos por UDF, procedimientos, Native Apps y Snowpark Container Services, para poder monitorear el código que corre dentro de Snowflake.

#### ¿Cómo se respaldan los datos de Snowflake?

Time Travel y Fail-safe cubren los errores recientes y los desastres; para una protección más larga, usa clones zero-copy programados, backups (conjuntos de copias inmutables en un momento dado, donde estén disponibles), replicación a otra región o descarga a almacenamiento en la nube.

#### ¿Cómo se despliega SQL de forma segura?

Versionando el SQL en Git, desplegando desde CI con un usuario de servicio (par de claves u OAuth), usando `CREATE OR ALTER` o herramientas de migración (schemachange, dbt, Terraform), probando primero sobre una base clonada y conservando scripts de reversión o apoyándose en Time Travel y clones.

### Modelado e integración

#### ¿Sigue siendo útil el modelado en estrella en Snowflake?

Sí. Snowflake maneja bien los joins y el almacenamiento es barato, pero los esquemas en estrella siguen haciendo la analítica más sencilla, coherente y rápida para las herramientas de BI. Muchos equipos usan un enfoque por capas: raw, staging, intermedio y marts con hechos y dimensiones, a menudo construidos con dbt.

#### ¿Conviene normalizar o desnormalizar en Snowflake?

Normaliza donde importan la integridad y la reutilización (las entidades centrales), y desnormaliza para el consumo (marts anchos, una tabla grande para dashboards concretos). El almacenamiento columnar hace que las tablas anchas sean baratas de consultar cuando solo se leen algunas columnas.

#### ¿Cómo funciona dbt con Snowflake?

dbt compila los modelos a SQL y los ejecuta en un warehouse de Snowflake con el adaptador dbt-snowflake, que admite tablas, vistas, modelos incrementales (`merge`, `delete+insert`, `append`, `microbatch`), dynamic tables, tablas transitorias, query tags y configuraciones de clustering.

#### ¿Cómo se integran Spark y Snowflake?

Con el conector de Spark, que lee y escribe tablas de Snowflake con pushdown de consultas, o compartiendo tablas Iceberg a través de un catálogo para que Spark y Snowflake trabajen sobre los mismos archivos.

#### ¿Cómo se implementa una SCD tipo 2 en Snowflake?

Con un `MERGE` que cierra las filas vigentes que cambiaron e inserta las nuevas versiones (a menudo dos sentencias o el truco de la unión), con streams y tasks para el procesamiento incremental, o con los snapshots de dbt, que lo manejan automáticamente.

#### ¿Qué es el enfoque "one big table" y cuándo encaja?

Una tabla ancha y desnormalizada con todo lo que necesita un caso de uso, rápida de consultar en un motor columnar y sencilla para BI. Encaja en casos de uso estables y concretos; para la analítica general, los esquemas en estrella siguen siendo más flexibles y coherentes.

#### ¿Cómo se modelan datos de referencia que cambian lentamente y que usan muchos marts?

Como dimensiones conformadas con un único modelo responsable, con claves sustitutas e historial SCD si hace falta, referenciadas por todos los marts para que todos los reportes usen las mismas definiciones.

### Escenarios

#### Diseña un pipeline de ingesta desde eventos de S3 hasta tablas de reportes en Snowflake.

Creo una storage integration y un stage externo sobre el prefijo de S3, un Snowpipe con auto-ingest a partir de las notificaciones de eventos de S3 hacia una tabla raw tipada o con `VARIANT`, un stream sobre la tabla raw, y dynamic tables (o tasks con `MERGE`) que construyen las tablas limpias y agregadas con la frescura necesaria. Añado data metric functions, alertas y resource monitors, y lo administro todo como código.

#### Un warehouse de dashboards hace cola cada lunes a las 9 a. m. ¿Qué haces?

Lo convierto en un warehouse multi-cluster con suficientes clusters máximos (política Standard para usuarios interactivos), reviso si las consultas lentas se pueden optimizar o servir desde agregados, y separo las otras cargas que usan el mismo warehouse a esa hora.

#### Una consulta lee el 98 % de las particiones de una tabla de 5 TB aunque filtra por `customer_id`. ¿Cómo lo corriges?

La tabla no está agrupada por `customer_id`. Para búsquedas puntuales, activo search optimization en esa columna; para filtros por rango frecuentes, añado una clustering key (quizá combinada con la fecha); si no, replanteo la consulta o creo una tabla preagregada.

#### Alguien ejecutó `DELETE FROM orders` sin `WHERE` hace una hora. ¿Cómo lo recuperas?

Con Time Travel: vuelvo a insertar las filas desde `orders AT (OFFSET => -3600)` o `BEFORE (STATEMENT => '<query id>')`, o clono la tabla en ese momento y la intercambio con `ALTER TABLE … SWAP WITH`. Después restrinjo los permisos de borrado en las tablas de producción.

#### Los costos subieron un 40 % este mes. ¿Cómo lo investigas?

Comparo `WAREHOUSE_METERING_HISTORY` y la medición serverless por servicio y warehouse, encuentro los warehouses y query tags que crecieron, miro `QUERY_ATTRIBUTION_HISTORY` para las consultas más caras, y reviso si hay warehouses que dejaron de suspenderse, dynamic tables nuevas con un lag muy corto, reagrupamiento en tablas con mucha rotación o refrescos completos.

#### Los analistas de cada país solo deben ver sus filas y no deben ver los correos. ¿Cómo?

Una row access policy en las tablas con una tabla de correspondencia entre roles y países, y una política de enmascaramiento (o enmascaramiento por etiquetas) en las columnas de correo que solo revela los valores a un rol privilegiado. Los analistas reciben roles funcionales asociados a su país.

#### ¿Cómo migrarías un data warehouse on-premises a Snowflake?

Inventariando los objetos, las cargas y las dependencias; traduciendo el DDL y el SQL (SnowConvert ayuda); moviendo el histórico por almacenamiento en la nube y `COPY`; montando la carga incremental; reconstruyendo las transformaciones (a menudo en dbt); recreando la seguridad con roles y políticas; validando con conteos de filas, checksums y comparaciones de reportes; ejecutando ambos en paralelo antes del corte; y luego ajustando warehouses y costos.

#### Un equipo quiere procesar 2 TB diarios de logs JSON. ¿Cómo los cargas y modelas?

Dejo en S3 archivos comprimidos de unos 100–250 MB, los cargo con Snowpipe o con `COPY` programado en una columna `VARIANT` de una tabla raw transitoria, extraigo los campos más usados a columnas tipadas en una tabla limpia agrupada por fecha del evento, y agrego en marts. Mantengo los datos raw poco tiempo si se pueden volver a cargar desde S3.

#### ¿Cómo le explicas el valor de Snowflake a una persona de negocio?

Un único lugar gobernado para los datos de la empresa que escala al instante para cualquier número de usuarios, no cuesta nada cuando no se usa y permite que los equipos compartan y analicen las mismas cifras sin administrar servidores.

#### Un `MERGE` nocturno sobre una tabla de 3 TB tarda horas. ¿Qué revisas?

Si el destino se poda (añadir un filtro de fecha o rango de claves en la cláusula `ON`, agrupar por la clave del merge), si el origen tiene duplicados o es mucho más grande que los cambios, el tamaño del warehouse y el spilling, y si encaja mejor un enfoque incremental (streams, `delete+insert` sobre las particiones recientes).

#### Un Snowpipe a veces carga filas duplicadas. ¿Por qué y qué haces?

Los mismos datos llegaron en archivos distintos (reintentos del productor, archivos renombrados), o se recargaron archivos con `FORCE`. Hago que los productores escriban nombres de archivo deterministas, deduplico después por una clave de negocio con `QUALIFY` y mantengo la capa raw como solo inserción, con los metadatos del archivo para rastrear.

#### ¿Cómo le das a un socio acceso a un dataset seleccionado sin copiarlo?

Creo vistas seguras sobre las tablas seleccionadas, las pongo en un share (o en un listing privado) y añado la cuenta del socio como consumidora; si no tiene cuenta de Snowflake, creo una reader account. Uso row access policies o vistas separadas para limitar lo que ve.
