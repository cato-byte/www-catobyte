## Guía de estudio de Databricks

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de Databricks: unas 200 preguntas](../../images/databricks_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre Databricks, desde la idea del lakehouse hasta Delta Lake, Unity Catalog, la ingesta, los pipelines y jobs de Lakeflow, la optimización del rendimiento, la seguridad y los costos. Las respuestas reflejan la plataforma en 2026; Databricks cambia a menudo el nombre de sus productos, así que se indican los nombres anteriores cuando todavía son comunes. Abre una pregunta para ver su respuesta, o usa el filtro para buscar en toda la guía.

<!-- QA -->

### Fundamentos de la plataforma

#### ¿Qué es Databricks?

Una plataforma de datos e IA en la nube, fundada por los creadores de Apache Spark, que funciona en AWS, Azure y Google Cloud. Reúne ingeniería de datos, analítica SQL, streaming, machine learning y gobierno sobre una sola copia de los datos, guardada en formatos abiertos (Delta Lake, Apache Iceberg) en tu propio almacenamiento en la nube.

#### ¿Qué es un lakehouse?

Una arquitectura que guarda los datos en almacenamiento de objetos barato, como un data lake, pero le añade funciones de data warehouse: transacciones ACID, esquemas, optimizaciones parecidas a los índices, gobierno detallado y SQL rápido. Evita tener una copia de los datos en un lake para ciencia de datos y otra en un warehouse para BI.

#### ¿Qué problemas del data lake clásico resuelve el lakehouse?

Los data lakes no tenían transacciones (los lectores veían datos a medio escribir), ni control de esquema (se acumulaba basura), las consultas sobre muchos archivos pequeños eran lentas, no era fácil actualizar ni borrar (un problema para el RGPD/GDPR) y el gobierno era débil. Delta Lake y Unity Catalog resuelven cada uno de estos puntos.

#### ¿Qué diferencia hay entre el plano de control y el plano de cómputo?

El plano de control lo administra Databricks en su propia cuenta: la aplicación web, los notebooks, el programador de jobs, el gestor de clusters y los metadatos de Unity Catalog. El plano de cómputo es donde se procesan los datos. Con cómputo clásico corre en tu cuenta de nube (tu VPC); con cómputo serverless corre en la cuenta de Databricks, en la misma región. En ambos casos los datos en reposo se quedan en tu almacenamiento.

#### ¿Qué es un workspace de Databricks?

El entorno donde trabajan los usuarios: notebooks, archivos, carpetas Git, jobs, pipelines, consultas SQL, dashboards, clusters y experimentos. Una empresa suele tener varios workspaces (por ejemplo dev, staging y prod), conectados a un metastore de Unity Catalog por región.

#### ¿Qué es un DBU?

Una Databricks Unit, la unidad de capacidad de procesamiento que Databricks factura por segundo. La tarifa por DBU depende del tipo de cómputo (jobs, all-purpose, SQL, serverless) y del plan. Con cómputo clásico también le pagas al proveedor de nube por las máquinas virtuales; con serverless, el precio del DBU incluye la infraestructura.

#### ¿Por qué el cómputo de jobs es más barato que el all-purpose?

El cómputo de jobs se factura a una tarifa de DBU más baja porque ejecuta cargas programadas y no interactivas, y se apaga cuando termina el job. Los clusters all-purpose son para el desarrollo interactivo, compartidos y de larga duración, así que Databricks cobra más por ellos. Correr la producción en clusters all-purpose es un error de costos clásico.

#### ¿Qué lenguajes se pueden usar en Databricks?

Python, SQL, Scala y R en los notebooks, además de Java y Scala en jobs JAR. Puedes mezclar lenguajes en un notebook con comandos mágicos como `%sql`, `%python`, `%scala`, `%md` (Markdown) y `%sh` (shell en el driver).

#### ¿Qué es un notebook de Databricks?

Un documento web formado por celdas que ejecutan código sobre el cómputo conectado, con resultados, gráficos, comentarios, historial de versiones y edición simultánea. Los notebooks se pueden programar como tareas de un job, parametrizar con widgets y guardar como archivos fuente en Git.

#### ¿Qué son las carpetas Git (antes Repos)?

Carpetas del workspace vinculadas a un repositorio Git (GitHub, GitLab, Azure DevOps, Bitbucket). Permiten clonar, crear ramas, hacer commit, pull y push desde el workspace, de modo que los notebooks y los archivos Python se versionan y se revisan como cualquier otro código.

#### ¿Qué es DBFS y por qué ya no se recomienda?

El Databricks File System, una abstracción heredada que montaba el almacenamiento en la nube bajo rutas `dbfs:/`, incluido un bucket raíz del workspace. No tiene gobierno detallado, así que Databricks recomienda ahora los volúmenes de Unity Catalog para los archivos y las tablas para los datos, y desactiva la raíz de DBFS y los montajes en las instalaciones nuevas.

#### ¿Qué es `dbutils`?

Una librería de utilidades disponible en notebooks y jobs: `dbutils.fs` para archivos, `dbutils.secrets` para secretos, `dbutils.widgets` para parámetros, `dbutils.notebook.run` y `dbutils.notebook.exit` para encadenar notebooks, y `dbutils.jobs.taskValues` para pasar valores pequeños entre tareas de un job.

#### ¿Qué son los widgets?

Parámetros de entrada de los notebooks (texto, lista desplegable, combobox, selección múltiple). En los jobs, los parámetros de la tarea los llenan. En SQL, los parámetros se referencian con la sintaxis `:nombre`.

```python
dbutils.widgets.text("snapshot_date", "2026-10-01")
snapshot = dbutils.widgets.get("snapshot_date")
```

#### ¿Qué es el Databricks Runtime?

La imagen de software versionada que ejecutan los clusters: Apache Spark más Delta Lake, Photon, librerías, conectores y mejoras de rendimiento. Las versiones LTS (soporte a largo plazo) tienen soporte durante unos tres años. El runtime ML añade librerías de machine learning.

#### ¿Qué es Photon?

Un motor de consultas vectorizado escrito en C++ que ejecuta de forma nativa las operaciones de Spark SQL y DataFrame, en lugar de hacerlo en la JVM. Acelera lecturas, joins, agregaciones y escrituras, sobre todo en Delta y Parquet. Viene activado por defecto en los SQL warehouses y en serverless, y es opcional (con una tarifa de DBU más alta) en los clusters.

#### ¿Qué es Spark Connect y por qué importa en Databricks?

Un protocolo cliente-servidor en el que el cliente construye un plan lógico sin resolver y lo envía a un servidor Spark remoto. El cómputo serverless y los clusters compartidos (modo de acceso estándar) lo usan, así que el código que toca directamente el `SparkContext`, los RDD o la JVM no funciona allí. El código DataFrame y SQL funciona sin cambios.

#### ¿Qué es la CLI de Databricks?

Una herramienta de línea de comandos para administrar workspaces desde una terminal o desde CI: archivos, jobs, clusters, secretos, objetos de Unity Catalog y, sobre todo, Databricks Asset Bundles (`databricks bundle validate|deploy|run`). Se autentica con OAuth (usuario o service principal) o con tokens.

#### ¿Qué es Databricks Connect?

Una librería que permite ejecutar código Spark desde tu IDE o un proceso Python local contra el cómputo de Databricks, a través de Spark Connect. Desarrollas y depuras en local mientras las operaciones DataFrame se ejecutan en el cluster o en serverless.

#### ¿Qué es Lakeflow?

El nombre general, desde 2025, de los productos de ingeniería de datos de Databricks: Lakeflow Connect (conectores de ingesta administrados), Lakeflow Declarative Pipelines (antes Delta Live Tables) y Lakeflow Jobs (antes Workflows).

#### ¿Qué es Mosaic AI?

El conjunto de funciones de IA y ML de Databricks: entrenamiento y ajuste fino de modelos, Model Serving, Vector Search, AI Gateway, frameworks y evaluación de agentes, todo gobernado con Unity Catalog.

### Delta Lake

#### ¿Qué es Delta Lake?

Un formato de almacenamiento de código abierto que añade un registro de transacciones a archivos Parquet. Ofrece transacciones ACID, control y evolución del esquema, viaje en el tiempo, `MERGE`, `UPDATE` y `DELETE`, y lecturas y escrituras en streaming. Es el formato de tabla por defecto en Databricks.

#### ¿Cómo funciona el registro de transacciones de Delta?

Cada tabla tiene una carpeta `_delta_log/` con archivos JSON de commit ordenados (`000…0.json`, `000…1.json`) que listan los archivos de datos añadidos y eliminados por cada transacción, además de los cambios de esquema y metadatos. Cada cierto tiempo un checkpoint en Parquet resume el estado para que los lectores no tengan que repetir todos los commits. Una versión de la tabla es el conjunto de archivos válidos después de un commit dado.

#### ¿Cómo garantiza Delta las propiedades ACID sobre almacenamiento de objetos?

Los escritores crean archivos Parquet nuevos y luego intentan hacer commit escribiendo de forma atómica la siguiente entrada numerada del registro. Si dos escritores compiten, solo uno lo logra; el otro comprueba si hay conflictos y reintenta o falla. Los lectores solo ven los archivos referenciados por entradas confirmadas, así que nunca ven escrituras parciales.

#### ¿Qué control de concurrencia usa Delta?

Control de concurrencia optimista: las transacciones no bloquean, sino que comprueban al hacer commit si otro commit concurrente tocó los mismos datos. Los appends casi nunca entran en conflicto; los `UPDATE`/`MERGE` concurrentes sobre los mismos archivos pueden lanzar `ConcurrentModificationException`. El particionamiento, el liquid clustering y la concurrencia a nivel de fila (con deletion vectors) reducen los conflictos.

#### ¿Qué es el control del esquema (schema enforcement)?

Delta rechaza las escrituras cuyas columnas o tipos no coinciden con el esquema de la tabla, en lugar de corromperla en silencio. Protege a los consumidores de cargas defectuosas.

#### ¿Cómo funciona la evolución del esquema en Delta?

Hay que permitirla de forma explícita: `.option("mergeSchema", "true")` en una escritura añade columnas nuevas, y `ALTER TABLE` cambia el esquema. Para `MERGE`, `WITH SCHEMA EVOLUTION` (o la configuración de merge automático) permite añadir columnas nuevas del origen. El type widening permite algunos cambios de tipo, como de `int` a `bigint`, sin reescribir los datos.

#### ¿Qué es el viaje en el tiempo (time travel)?

Consultar una versión anterior de una tabla por número de versión o por fecha, usando el registro de transacciones:

```sql
SELECT * FROM sales VERSION AS OF 42;
SELECT * FROM sales TIMESTAMP AS OF '2026-10-01';
DESCRIBE HISTORY sales;
```

Sirve para auditorías, reproducir un informe, comparar versiones y recuperarse de escrituras erróneas. Solo funciona mientras los archivos antiguos no hayan sido eliminados con `VACUUM`.

#### ¿Cómo se deshace una escritura errónea en Delta?

`RESTORE TABLE sales TO VERSION AS OF 41` (o `TIMESTAMP AS OF`). Crea un nuevo commit que vuelve a apuntar a los archivos antiguos, así que se conserva el historial.

#### ¿Qué hace `VACUUM`?

Borra los archivos de datos que ya no están referenciados por la versión actual de la tabla y que son más antiguos que el umbral de retención (7 días por defecto). Ahorra almacenamiento, pero limita el viaje en el tiempo al periodo de retención. Bajar el umbral por debajo de la lectura o escritura más larga puede romper consultas concurrentes.

#### ¿Qué hace `OPTIMIZE`?

Compacta archivos pequeños en archivos más grandes (alrededor de 1 GB por defecto), lo que acelera las lecturas. Con Z-ordering o liquid clustering, además reescribe los datos para que los valores relacionados queden en los mismos archivos.

#### ¿Qué es el problema de los archivos pequeños?

Muchos archivos diminutos hacen lentas las lecturas (cada archivo tiene un costo de apertura y de metadatos, y las estadísticas sirven menos) y ralentizan el registro de transacciones. Lo causan el streaming y los appends pequeños y frecuentes. Soluciones: `OPTIMIZE`, la auto compactación y las escrituras optimizadas, y lotes menos numerosos y más grandes.

#### ¿Qué son las escrituras optimizadas y la auto compactación?

Las escrituras optimizadas reorganizan los datos antes de escribir para que cada partición produzca menos archivos y más grandes. La auto compactación ejecuta un pequeño `OPTIMIZE` después de una escritura cuando una tabla tiene muchos archivos pequeños. Ambas vienen activadas por defecto en muchas operaciones en los runtimes recientes y en serverless.

#### ¿Qué es el data skipping?

Delta guarda los valores mínimo y máximo y el número de nulos de las primeras columnas de cada archivo (32 por defecto). Cuando una consulta filtra por esas columnas, se saltan sin leerlos los archivos cuyos rangos no pueden coincidir. Funciona mejor cuando los datos están agrupados por las columnas del filtro.

#### ¿Qué es el Z-ordering?

Una técnica de agrupamiento multidimensional que se ejecuta con `OPTIMIZE tabla ZORDER BY (col1, col2)`. Coloca juntos en los mismos archivos los valores similares de varias columnas para mejorar el data skipping. Hay que repetirlo a medida que llegan datos, y lo está reemplazando el liquid clustering.

#### ¿Qué es el liquid clustering?

Un método de agrupamiento declarado en la tabla con `CLUSTER BY (cols)` que reemplaza tanto el particionamiento como el Z-ordering. Agrupa los datos de forma incremental durante `OPTIMIZE`, las claves se pueden cambiar sin reescribir la tabla, y `CLUSTER BY AUTO` deja que Databricks elija las claves según el historial de consultas. Es la organización recomendada para las tablas nuevas.

```sql
CREATE TABLE events (event_date DATE, user_id BIGINT, payload STRING)
CLUSTER BY (event_date, user_id);
```

#### ¿Cuándo conviene todavía particionar una tabla Delta?

Rara vez, ahora que existe el liquid clustering. El particionamiento solo ayuda en tablas muy grandes (más de 1 TB, aproximadamente) sobre una columna de baja cardinalidad por la que filtran casi todas las consultas, con al menos 1 GB por partición. Particionar en exceso crea el problema de los archivos pequeños.

#### ¿Qué son los deletion vectors?

Una optimización del almacenamiento en la que `DELETE`, `UPDATE` y `MERGE` marcan las filas como borradas en un pequeño archivo auxiliar en lugar de reescribir archivos Parquet completos. Las escrituras se vuelven mucho más rápidas; los archivos se reescriben físicamente más tarde con `OPTIMIZE` o `REORG TABLE … APPLY (PURGE)`.

#### ¿Qué es el Change Data Feed?

Una opción de tabla (`delta.enableChangeDataFeed = true`) que registra los cambios a nivel de fila (insert, update_preimage, update_postimage, delete) con la versión y la fecha del commit. Los jobs posteriores leen solo lo que cambió:

```sql
SELECT * FROM table_changes('silver.customers', 120);
```

#### ¿Cómo funciona `MERGE` en Delta?

`MERGE INTO` hace un upsert de un origen en un destino según una condición de unión, con cláusulas para las filas que coinciden y las que no. Es la base de la CDC, la deduplicación y la lógica de SCD.

```sql
MERGE INTO silver.customers t
USING updates s ON t.customer_id = s.customer_id
WHEN MATCHED AND s.op = 'DELETE' THEN DELETE
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

#### ¿Por qué falla `MERGE` con "multiple source rows matched"?

Porque dos o más filas del origen coinciden con la misma fila del destino, así que el resultado sería ambiguo. Primero hay que deduplicar el origen, por ejemplo quedándose con la fila más reciente por clave con `ROW_NUMBER()`.

#### ¿Cómo se acelera un `MERGE` lento?

Añadiendo filtros que permitan a Delta descartar archivos del destino (por ejemplo un rango de fechas en la cláusula `ON`), agrupando el destino por la clave del merge, deduplicando y reduciendo el origen, activando los deletion vectors y evitando hacer merge de todo el historial cuando solo cambian los datos recientes.

#### ¿Qué diferencia hay entre un deep clone y un shallow clone?

Un deep clone copia los archivos de datos y los metadatos en una tabla independiente. Un shallow clone copia solo los metadatos y apunta a los archivos del origen, así que es instantáneo y barato, útil para probar cambios sobre datos del tamaño de producción. Ambos tienen su propio historial desde el momento del clon.

#### ¿Qué restricciones admite Delta?

Restricciones `NOT NULL` y `CHECK`, que se aplican: una escritura que las viola falla. Las claves primarias y foráneas se pueden declarar en Unity Catalog, pero son informativas (no se aplican) y las usan las herramientas y el optimizador.

#### ¿Qué son las columnas generadas y las columnas de identidad?

Una columna generada se calcula a partir de otras columnas (`GENERATED ALWAYS AS (CAST(ts AS DATE))`). Una columna de identidad (`GENERATED ALWAYS AS IDENTITY`) asigna números únicos y crecientes (no necesariamente consecutivos), útiles como claves sustitutas.

#### ¿Qué es UniForm?

Universal Format: una opción de las tablas Delta que también escribe metadatos Iceberg (y Hudi), para que los motores que leen Iceberg puedan leer los mismos archivos sin copiar los datos.

#### ¿Qué diferencia hay entre una tabla administrada y una externa?

Los datos de una tabla administrada (managed) viven en un almacenamiento controlado por Unity Catalog; al borrar la tabla se borran los datos (tras un periodo de retención), y Databricks puede optimizarla automáticamente. Una tabla externa apunta a una ruta que tú administras en tu propia ubicación de almacenamiento; al borrarla solo se eliminan los metadatos.

#### ¿Qué muestra `DESCRIBE DETAIL`?

El formato, la ubicación, el número de archivos, el tamaño en bytes, las columnas de partición o de clustering y las propiedades de la tabla. Es una forma rápida de detectar el problema de los archivos pequeños.

#### ¿Qué diferencia hay entre el modo `overwrite` y `replaceWhere`?

`mode("overwrite")` reemplaza toda la tabla (como una nueva versión, así que el viaje en el tiempo sigue funcionando). `replaceWhere` reemplaza solo las filas que cumplen un predicado. La sobrescritura dinámica de particiones (`partitionOverwriteMode=dynamic`) reemplaza solo las particiones presentes en los datos nuevos.

#### ¿Cómo hace Delta `UPDATE` y `DELETE` sin deletion vectors?

Busca los archivos que contienen filas afectadas, los reescribe sin las filas borradas (o con los valores actualizados) y hace commit de una transacción que elimina los archivos antiguos y añade los nuevos. Es copy-on-write: lecturas baratas y escrituras caras sobre archivos grandes.

#### ¿Qué es `CONVERT TO DELTA`?

Un comando que convierte en su lugar un directorio Parquet existente en una tabla Delta, escribiendo un registro de transacciones sobre los archivos existentes, sin copiar datos.

#### ¿Para qué sirven las propiedades de tabla en Delta?

Son ajustes guardados con la tabla, como `delta.enableChangeDataFeed`, `delta.logRetentionDuration`, `delta.deletedFileRetentionDuration`, `delta.enableDeletionVectors` o `delta.appendOnly`, además de metadatos clave-valor propios. Se definen con `TBLPROPERTIES` y se ven con `SHOW TBLPROPERTIES`.

#### ¿Qué diferencia hay entre la retención del log y la de los archivos borrados?

`delta.logRetentionDuration` (30 días por defecto) controla cuánto tiempo se conserva el historial de commits; `delta.deletedFileRetentionDuration` (7 días por defecto) controla cuánto tiempo conserva `VACUUM` los archivos de datos sin referencia. El viaje en el tiempo necesita las dos cosas: las entradas del log y los archivos de datos.

### Unity Catalog y gobierno

#### ¿Qué es Unity Catalog?

La capa de gobierno unificada de Databricks para los activos de datos e IA de todos los workspaces: un solo lugar para definir el control de acceso, la auditoría, el linaje, el descubrimiento de datos y el uso compartido de tablas, vistas, volúmenes, funciones y modelos. También se publicó como código abierto.

#### ¿Cuál es la jerarquía de objetos de Unity Catalog?

Metastore (uno por región) → catálogo → esquema (base de datos) → tablas, vistas, vistas materializadas, volúmenes, funciones y modelos. Los objetos se nombran con tres niveles: `catalogo.esquema.tabla`.

#### ¿Qué es un volumen?

Un objeto de Unity Catalog que gobierna el acceso a archivos no tabulares (CSV, JSON, imágenes, PDF, wheels) en el almacenamiento en la nube, con rutas del tipo `/Volumes/catalogo/esquema/volumen/ruta`. Los volúmenes administrados viven en el almacenamiento administrado por Unity Catalog; los externos apuntan a una ruta de almacenamiento existente.

#### ¿Qué son las storage credentials y las external locations?

Una storage credential encapsula una identidad de nube (un rol IAM de AWS, una identidad administrada de Azure) con acceso al almacenamiento. Una external location combina una ruta de almacenamiento con una credencial, y los permisos sobre ella controlan quién puede crear allí tablas o volúmenes externos.

#### ¿Cómo se conceden permisos en Unity Catalog?

Con SQL o desde la interfaz, a usuarios, grupos o service principals. Los privilegios se heredan hacia abajo en la jerarquía, y un usuario necesita `USE CATALOG` y `USE SCHEMA` en los niveles superiores para llegar a un objeto.

```sql
GRANT USE CATALOG ON CATALOG prod TO `analysts`;
GRANT USE SCHEMA, SELECT ON SCHEMA prod.gold TO `analysts`;
```

#### ¿Qué son los row filters y las column masks?

Funciones asociadas a una tabla que se evalúan en el momento de la consulta. Un row filter decide qué filas puede ver un usuario (por ejemplo solo las de su país); una column mask devuelve el valor o una versión enmascarada según los grupos del usuario. Los datos quedan en una sola tabla en lugar de en muchas copias filtradas.

#### ¿Qué son las vistas dinámicas?

Vistas que usan funciones como `current_user()` o `is_account_group_member()` para filtrar filas u ocultar columnas. Eran el enfoque habitual antes de que existieran los row filters y las column masks.

#### ¿Qué linaje registra Unity Catalog?

Linaje a nivel de tabla y de columna de las consultas ejecutadas en el cómputo de Databricks, a través de notebooks, jobs, pipelines y dashboards, visible en Catalog Explorer y consultable en las tablas del sistema. Responde a "¿qué se rompe si cambio esta columna?" y "¿de dónde sale este número?".

#### ¿Qué son las tablas del sistema?

Tablas de solo lectura del catálogo `system` con datos operativos: consumo facturado (`system.billing.usage`), logs de auditoría, linaje de tablas, ejecuciones de jobs, eventos de clusters, historial de consultas y más. Son la base de los dashboards de costos y de la auditoría.

#### ¿Qué es el Hive metastore heredado y cómo se migra desde él?

El metastore por workspace anterior a Unity Catalog, con permisos locales al workspace. La migración consiste en crear un metastore de Unity Catalog, actualizar las tablas (`SYNC` para las externas, `CREATE TABLE … AS SELECT` o deep clone para las administradas) y cambiar el código a nombres de tres niveles. La herramienta UCX automatiza gran parte de la evaluación y la migración.

#### ¿Qué es Delta Sharing?

Un protocolo abierto para compartir datos vivos de forma segura entre organizaciones y plataformas sin copiarlos. El proveedor crea un share con tablas, vistas o volúmenes; los destinatarios lo leen desde Databricks o desde clientes de código abierto (pandas, Spark, herramientas de BI). El uso compartido entre Databricks usa las identidades de Unity Catalog.

#### ¿Qué es Lakehouse Federation?

Federación de consultas que permite a Unity Catalog registrar bases de datos externas (PostgreSQL, MySQL, SQL Server, Snowflake, Redshift, BigQuery y otras) como catálogos foráneos, para consultarlas en su lugar con gobierno y linaje, sin ingerir primero los datos.

#### ¿Para qué sirven las etiquetas y los comentarios en Unity Catalog?

Los comentarios documentan tablas y columnas (y alimentan las descripciones generadas por IA y la búsqueda); las etiquetas (pares clave-valor) clasifican objetos, por ejemplo `pii=true`, lo que puede guiar políticas, descubrimiento y auditorías.

#### ¿Qué es un service principal y por qué usarlo en los jobs de producción?

Una identidad no humana para la automatización. Los jobs de producción y los despliegues de CI/CD deberían ejecutarse como service principal para no depender de la cuenta y los permisos de una persona, y para limitar el acceso a lo que necesita el pipeline.

#### ¿Cómo se administran los secretos en Databricks?

En secret scopes (respaldados por Databricks o por Azure Key Vault), leídos con `dbutils.secrets.get(scope, key)`. Los valores secretos se ocultan en la salida de los notebooks. Para los recursos de la nube, es preferible el acceso basado en identidad (instance profiles, storage credentials) a los secretos.

#### ¿Qué diferencia hay entre la administración a nivel de cuenta y a nivel de workspace?

Los administradores de la cuenta gestionan las identidades (usuarios, grupos, service principals, a menudo sincronizados desde un proveedor de identidad por SCIM), los metastores, los workspaces y la configuración general. Los administradores de un workspace gestionan la configuración, las políticas de cómputo y el acceso dentro de ese workspace.

#### ¿Qué diferencia hay entre la propiedad y los privilegios?

El propietario de un objeto (un usuario, grupo o service principal) puede conceder privilegios sobre él y administrarlo. Los privilegios como `SELECT`, `MODIFY`, `CREATE TABLE` o `READ VOLUME` permiten acciones concretas. Hacer que un grupo sea el propietario de los objetos de producción evita depender de una sola persona.

#### ¿Qué es la vinculación entre workspaces y catálogos?

Un ajuste que limita qué workspaces pueden acceder a un catálogo, por ejemplo para que un catálogo de producción solo sea accesible desde el workspace de producción, aunque los usuarios tengan permisos sobre él.

#### ¿Qué es el information schema en Unity Catalog?

Un conjunto de vistas SQL estándar en cada catálogo (`information_schema.tables`, `columns`, `table_privileges` y otras) que describen los objetos y los permisos, útiles para la documentación y las auditorías.

#### ¿Cómo se descubren datos en Unity Catalog?

Con Catalog Explorer y la búsqueda, que usan nombres, comentarios, etiquetas y linaje, además de señales de popularidad como los usuarios y las consultas frecuentes. Unos buenos comentarios y etiquetas mejoran mucho el descubrimiento.

### Cómputo

#### ¿Qué tipos de cómputo ofrece Databricks?

Clusters all-purpose para el trabajo interactivo, cómputo de jobs creado para una ejecución, SQL warehouses para SQL y BI, cómputo serverless para notebooks, jobs y pipelines, e instance pools para acelerar el arranque de los clusters clásicos.

#### ¿Qué es el cómputo serverless?

Cómputo que Databricks aprovisiona y administra en su propia cuenta: arranca en segundos, escala automáticamente, siempre usa un runtime actual con Photon y solo se factura mientras trabaja. Renuncias al control de los tipos de instancia y de la configuración de Spark, y el código debe ser compatible con Spark Connect.

#### ¿Cómo está compuesto un cluster clásico?

Un nodo driver que ejecuta el programa principal, planifica el trabajo y recoge los resultados, y nodos worker con executors que procesan las particiones. Un cluster de un solo nodo lo ejecuta todo en el driver, lo cual basta para datos pequeños y para ML en una sola máquina.

#### ¿Qué son los modos de acceso?

Ajustes que controlan el aislamiento y el gobierno en el cómputo clásico. El modo estándar (antes shared) permite que varios usuarios compartan un cluster con aislamiento de Unity Catalog, usando Spark Connect. El modo dedicado (antes single user) asigna el cluster a un usuario o grupo y admite más APIs, como los RDD y algunas librerías de ML.

#### ¿Cómo funciona el autoescalado?

Defines un número mínimo y máximo de workers; Databricks añade workers cuando hay tareas en cola y los quita cuando están inactivos. El autoescalado sirve para cargas interactivas y variables; los clusters de tamaño fijo pueden ser más predecibles para jobs batch estables. Las cargas de streaming deberían usar el autoescalado mejorado de los pipelines.

#### ¿Qué es la autoterminación?

Un ajuste del cluster que apaga un cluster all-purpose inactivo tras cierto número de minutos. Dejarla desactivada es una de las causas más comunes de gasto desperdiciado.

#### ¿Qué son los instance pools?

Un conjunto de máquinas virtuales inactivas y listas para usar del que toman los clusters, para reducir el arranque de minutos a segundos. Las instancias inactivas del pool generan costos de nube, pero no DBU.

#### ¿Conviene usar instancias spot?

Para los workers de jobs batch tolerantes a fallos, sí: son mucho más baratas y Spark reintenta las tareas si se pierde una instancia. Mantén el driver bajo demanda, porque perderlo mata el job, y permite volver a instancias bajo demanda si no hay spot.

#### ¿Qué son las políticas de cluster?

Reglas definidas por los administradores que limitan cómo crean clusters los usuarios: tipos de instancia permitidos, tamaño máximo, etiquetas obligatorias, autoterminación, versiones del runtime. Controlan los costos y estandarizan las configuraciones.

#### ¿Qué es un SQL warehouse?

Cómputo dedicado a las consultas SQL de Databricks SQL, las herramientas de BI y los dashboards. Tipos: serverless (arranque rápido, recomendado), pro y classic. Escala añadiendo clusters para absorber la concurrencia, y usa Photon y una gestión inteligente de la carga.

#### ¿Cómo se dimensiona un SQL warehouse?

Elige una talla (T-shirt size) según la complejidad de las consultas y el volumen de datos (más grande significa consultas individuales más rápidas), y define el número máximo de clusters para la concurrencia (más usuarios a la vez). Vigila las colas y el spill en el historial de consultas, y configura el auto-stop.

#### ¿Cómo se instalan librerías en un cluster?

Como librerías del cómputo (PyPI, Maven, wheels desde volúmenes o archivos del workspace), con alcance de notebook con `%pip install`, o como dependencias de una tarea de job. En serverless, las dependencias se declaran en la configuración del entorno. Fija las versiones para que sea reproducible.

#### ¿Qué son los init scripts?

Scripts de shell que se ejecutan en cada nodo al arrancar, para instalar paquetes del sistema o configurar el entorno. Deben guardarse en volúmenes o archivos del workspace, no en DBFS, y reducirse al mínimo porque ralentizan el arranque y complican la depuración.

#### ¿Qué pasa cuando el driver se queda sin memoria?

El notebook o el job falla o se reinicia. Causas comunes: `collect()` o `toPandas()` sobre muchos datos, hacer broadcast de una tabla demasiado grande, objetos Python grandes en el driver o demasiadas tareas seguidas a la vez. Mantén los datos en Spark, escribe los resultados en tablas y dimensiona bien el driver.

#### ¿Dónde se mira cuando un cluster va lento?

En la Spark UI (jobs, stages, duración de las tareas, tamaños del shuffle, spill, skew), las métricas del cluster (CPU, memoria, disco), los logs del driver y el perfil de la consulta en SQL. Compara la mediana y el máximo de la duración de las tareas de un stage para detectar skew.

#### ¿Para qué sirve un cluster de un solo nodo?

Para procesar datos pequeños, trabajar con pandas y scikit-learn y desarrollar cosas ligeras. No tiene workers, así que Spark corre en modo local en el driver: es barato, pero no escala.

#### ¿Para qué se usan los clusters con GPU?

Para entrenar e inferir modelos de deep learning y para algunas librerías aceleradas por GPU. Necesitan un runtime ML con drivers de GPU y son caros, así que deben autoterminarse pronto.

#### ¿Qué implica elegir entre modo estándar y dedicado para cargas de ML?

Las librerías de ML que necesitan acceso directo a la JVM o al `SparkContext`, o el entrenamiento con GPU, suelen requerir el modo de acceso dedicado o serverless con el entorno adecuado. El modo estándar es mejor para el trabajo compartido con SQL y DataFrames.

### Ingesta

#### ¿Qué opciones hay para cargar datos en Databricks?

Auto Loader para los archivos que llegan al almacenamiento en la nube, `COPY INTO` para cargas batch idempotentes de archivos, los conectores administrados de Lakeflow Connect (Salesforce, Workday, SQL Server, Google Analytics y otros), Structured Streaming desde Kafka, Kinesis o Event Hubs, Lakehouse Federation para consultar en su lugar, herramientas de socios (Fivetran y otras) y la subida de archivos a volúmenes.

#### ¿Qué es Auto Loader?

Una fuente de Structured Streaming (`cloudFiles`) que procesa de forma incremental y eficiente los archivos nuevos a medida que llegan al almacenamiento en la nube. Registra en su checkpoint qué archivos ya se procesaron, así que cada archivo se carga exactamente una vez, y puede inferir y hacer evolucionar el esquema.

```python
(spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/Volumes/raw/_schemas/orders")
    .load("/Volumes/raw/landing/orders/")
  .writeStream
    .option("checkpointLocation", "/Volumes/raw/_checkpoints/orders")
    .trigger(availableNow=True)
    .toTable("bronze.orders"))
```

#### ¿Cuáles son los modos de detección de archivos de Auto Loader?

El listado de directorios, que lista la ruta de entrada para encontrar archivos nuevos (sencillo, suficiente para volúmenes moderados), y la notificación de archivos, que se suscribe a los eventos del almacenamiento a través de una cola (SQS/SNS, Event Grid) y escala a millones de archivos. Las instalaciones nuevas pueden usar los managed file events de las external locations.

#### ¿Cómo maneja Auto Loader los cambios de esquema?

Guarda el esquema inferido en la ubicación del esquema. Con el modo por defecto `addNewColumns`, una columna nueva detiene el stream, actualiza el esquema y el stream continúa tras reiniciarse. Los datos que no encajan en el esquema (tipo incorrecto, columna inesperada) van a la columna `_rescued_data` en lugar de perderse.

#### ¿Qué es la columna de datos rescatados?

Una columna de texto JSON (`_rescued_data`) donde Auto Loader pone los valores que no pudo convertir al esquema. Vigilarla revela los cambios de formato en el origen.

#### ¿Qué es `COPY INTO`?

Un comando SQL que carga archivos de una ruta en una tabla Delta y es idempotente: los archivos ya cargados se omiten. Sirve para cargas batch programadas de miles de archivos; para millones de archivos o ingesta continua es preferible Auto Loader.

```sql
COPY INTO bronze.customers
FROM '/Volumes/raw/landing/customers/'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');
```

#### ¿Qué hace `trigger(availableNow=True)`?

Hace que una consulta de streaming procese todo lo disponible al arrancar (en varios lotes, respetando los límites de velocidad) y luego se detenga. Da el seguimiento incremental del streaming con el perfil de costos de un job batch programado.

#### ¿Qué es un checkpoint de streaming?

Una ubicación de almacenamiento donde una consulta de streaming registra su avance (offsets o archivos procesados) y su estado. Garantiza un procesamiento exactly-once entre reinicios. Cada consulta necesita su propio checkpoint, y borrarlo hace que la consulta empiece de cero.

#### ¿Cómo se ingiere desde Kafka?

Con la fuente Kafka de Structured Streaming, que lee `key`, `value`, `topic`, `partition`, `offset` y `timestamp`. Se interpreta `value` (JSON, Avro con un schema registry, Protobuf), se escriben los registros en bruto en bronze y se mantiene un checkpoint por consulta.

#### ¿Qué es la columna `_metadata`?

Una columna oculta disponible al leer archivos, con `file_path`, `file_name`, `file_size` y `file_modification_time`. Reemplaza a `input_file_name()` (no admitida en Unity Catalog) para registrar el archivo de origen de cada fila.

#### ¿Por qué evitar `inferSchema` en producción?

La inferencia requiere una pasada extra sobre los datos, puede inferir tipos distintos en archivos distintos y cambia en silencio cuando cambia el origen. Declara los esquemas (contratos de datos) en las cargas de producción, o deja que Auto Loader gestione la inferencia con schema hints.

#### ¿Qué es Lakeflow Connect?

Conectores de ingesta administrados y serverless para aplicaciones SaaS y bases de datos. Se encargan de la extracción incremental (a menudo con CDC) y dejan los datos en tablas de Unity Catalog a través de un pipeline, sin escribir código de extracción.

#### ¿Cómo se cargan datos de una base de datos relacional sin Lakeflow Connect?

Con el lector JDBC de Spark, particionando la lectura con `partitionColumn`, `lowerBound`, `upperBound` y `numPartitions` para que se ejecute en paralelo, y cargando de forma incremental según una columna marca de agua (por ejemplo `updated_at`). Guarda las credenciales en secretos.

#### ¿Cómo se manejan los archivos que llegan tarde?

Auto Loader toma cualquier archivo nuevo cuando llega, sin importar su fecha, así que la carga en sí es segura. Más adelante, usa `MERGE` sobre las claves de negocio o reprocesa las fechas afectadas con `replaceWhere`, para que los datos tardíos corrijan los resultados anteriores.

#### ¿Qué son los schema hints de Auto Loader?

Tipos explícitos para algunas columnas (`cloudFiles.schemaHints = "amount DECIMAL(18,2), event_ts TIMESTAMP"`) que se imponen a la inferencia, mientras el resto del esquema se sigue infiriendo.

#### ¿Qué es `read_files`?

Una función SQL de tabla que lee archivos (CSV, JSON, Parquet, Avro, XML, texto) de una ruta o un volumen con inferencia de esquema. Con `STREAM read_files(...)` en una streaming table, usa Auto Loader por debajo.

### Lakeflow Declarative Pipelines

#### ¿Qué son las Lakeflow Declarative Pipelines (antes Delta Live Tables)?

Un framework declarativo en el que defines las tablas y las consultas que las producen, en SQL o Python, y Databricks deduce las dependencias, orquesta la ejecución, administra la infraestructura, reintenta los fallos y aplica las expectativas de calidad de datos. El motor se donó a Apache Spark como Spark Declarative Pipelines.

#### ¿Qué diferencia hay entre una streaming table y una vista materializada?

Una streaming table procesa cada fila de entrada una sola vez, añadiendo o actualizando de forma incremental, lo que sirve para la ingesta y los datos que solo crecen. Una vista materializada guarda el resultado de una consulta y se refresca (de forma incremental cuando se puede) para reflejar siempre sus fuentes, lo que sirve para agregaciones y joins sobre datos que cambian.

```sql
CREATE OR REFRESH STREAMING TABLE bronze_orders
AS SELECT * FROM STREAM read_files('/Volumes/raw/landing/orders/', format => 'json');

CREATE OR REFRESH MATERIALIZED VIEW gold_daily_sales
AS SELECT order_date, sum(amount) AS sales FROM silver_orders GROUP BY order_date;
```

#### ¿Qué son las expectativas (expectations)?

Reglas de calidad de datos declaradas sobre una tabla del pipeline. Se comprueba cada fila, y la política decide qué pasa ante una infracción: conservarla y registrarla (`EXPECT`), descartar la fila (`ON VIOLATION DROP ROW`) o hacer fallar la actualización (`ON VIOLATION FAIL UPDATE`). Las métricas se ven en la interfaz del pipeline y en el event log.

```sql
CONSTRAINT valid_amount EXPECT (amount >= 0) ON VIOLATION DROP ROW
```

#### ¿Cómo se maneja la CDC en los pipelines declarativos?

Con `AUTO CDC` (antes `APPLY CHANGES INTO`), que aplica un flujo de cambios a una tabla destino usando una clave y una columna de secuencia, maneja eventos desordenados y borrados, y puede conservar el historial como SCD tipo 1 o tipo 2 sin escribir lógica de `MERGE`.

#### ¿Qué diferencia hay entre el modo triggered y el modo continuo de un pipeline?

El modo triggered procesa los datos disponibles y se detiene (más barato, para programaciones batch). El modo continuo mantiene el pipeline en marcha para procesar los datos con baja latencia.

#### ¿Qué es el modo de desarrollo de un pipeline?

Un modo que reutiliza el cluster entre actualizaciones y desactiva los reintentos, para iterar rápido y ver los errores de inmediato. El modo de producción reinicia el cluster ante errores recuperables y reintenta.

#### ¿Qué es el event log del pipeline?

Una tabla Delta que registra todos los eventos de un pipeline: actualizaciones, avance de los flujos, métricas de calidad de datos, linaje y errores. Se consulta para construir dashboards de monitoreo y de calidad de datos.

#### ¿Cuándo no usarías pipelines declarativos?

Cuando necesitas un control detallado de cada paso, lógica que no encaja en el modelo declarativo (código procedural complejo, llamadas a sistemas externos en cada lote) o portabilidad a jobs Spark sencillos. Muchos equipos usan jobs normales con Delta y `MERGE` y obtienen los mismos resultados con más código.

#### ¿Qué es un full refresh de una tabla del pipeline?

Vaciar la tabla y reprocesar todos los datos de origen desde el principio, incluido el reinicio de los checkpoints de streaming. Hace falta tras cambios de lógica que deben aplicarse al historial, pero puede ser costoso y puede perder datos si la retención del origen es más corta que el historial.

#### ¿Cómo se escribe un pipeline declarativo en Python?

Con el módulo `pipelines` (antes `dlt`): funciones decoradas que devuelven DataFrames, y los decoradores declaran las tablas y las expectativas.

```python
from pyspark import pipelines as dp

@dp.table(comment="Pedidos limpios")
@dp.expect_or_drop("valid_amount", "amount >= 0")
def silver_orders():
    return spark.readStream.table("bronze_orders").dropDuplicates(["order_id"])
```

#### ¿Dónde viven las tablas de un pipeline?

En el catálogo y el esquema de Unity Catalog configurados para el pipeline (y en otros esquemas si se usan nombres completos). Para los lectores son tablas Delta normales, pero solo el pipeline debería escribir en ellas.

#### ¿Qué es un flow en un pipeline declarativo?

Una unidad de procesamiento que escribe en una tabla destino. Una streaming table puede tener varios append flows (por ejemplo uno por región de origen), lo que permite añadir fuentes sin un full refresh.

#### ¿Cómo se factura un pipeline declarativo?

Por el cómputo del pipeline (serverless o clásico) según la edición del producto (Core, Pro, Advanced); las ediciones superiores añaden CDC y expectativas. Los pipelines serverless se facturan por uso y son la opción por defecto.

### Jobs y orquestación

#### ¿Qué son los Lakeflow Jobs (antes Workflows)?

El orquestador integrado de Databricks. Un job es un DAG de tareas (notebooks, scripts Python, wheels, SQL, dbt, pipelines, JAR, otros jobs) con dependencias, programaciones o disparadores, parámetros, reintentos, timeouts, notificaciones y configuración de cómputo.

#### ¿Qué tipos de tarea puede tener un job?

Notebook, script Python, wheel Python, SQL (consulta, archivo, dashboard o alerta), dbt, pipeline, JAR, Spark Submit, Run Job (otro job), condición If/else y For each (bucle sobre valores).

#### ¿Qué disparadores pueden iniciar un job?

Una programación cron, la llegada de un archivo a una ubicación de almacenamiento, la actualización de una tabla (cuando cambia una tabla de origen), el modo continuo (reiniciar en cuanto termina), la API o la CLI, o una ejecución manual.

#### ¿Cómo se pasan valores entre tareas?

Los valores pequeños con task values (`dbutils.jobs.taskValues.set` en una tarea y `get` en otra posterior, o referencias dinámicas como `{{tasks.ingest.values.row_count}}` en los parámetros de la tarea). Los datos en sí deben pasar por tablas, no por task values.

#### ¿Qué son los parámetros de job y las referencias a valores dinámicos?

Parámetros definidos a nivel de job que se pasan a todas las tareas y se pueden sobrescribir en cada ejecución. Las referencias dinámicas como `{{job.start_time.iso_date}}` o `{{job.run_id}}` inyectan el contexto de la ejecución, útil para un procesamiento idempotente basado en fechas.

#### ¿Cómo se hace idempotente un job de Databricks?

Escribiendo con `MERGE` o con `replaceWhere`/sobrescritura dinámica de particiones para la fecha procesada en lugar de appends a ciegas, tomando la fecha de procesamiento de un parámetro y no del reloj, usando checkpoints de streaming para la ingesta incremental y haciendo que los efectos secundarios (notificaciones, exportaciones) se puedan repetir sin problema.

#### ¿Cómo se vuelve a ejecutar solo la parte fallida de un job?

Con "Repair run", que vuelve a ejecutar las tareas fallidas y sus dependientes, reutilizando los resultados correctos de las tareas anteriores, opcionalmente con parámetros nuevos.

#### ¿Qué diferencia hay entre el cómputo de jobs y ejecutar tareas en un cluster compartido?

Cada tarea puede usar su propio cluster de job, compartir un cluster de job con otras tareas de la misma ejecución, usar cómputo serverless o usar un cluster all-purpose existente. Los clusters de job compartidos evitan arranques repetidos; serverless elimina el arranque por completo.

#### ¿Cómo te enteras cuando un job falla o va lento?

Configurando notificaciones (correo, Slack, Teams, PagerDuty, webhooks) al iniciar, al terminar con éxito, al fallar y al superar umbrales de duración, y definiendo un timeout y un máximo de ejecuciones concurrentes. Las tablas del sistema sobre ejecuciones de jobs permiten construir dashboards de confiabilidad a más largo plazo.

#### ¿Conviene orquestar Databricks con Airflow o con Jobs?

Jobs basta cuando el flujo vive principalmente en Databricks, y es más barato y más simple. Airflow (o Dagster, Prefect) tiene sentido cuando el DAG abarca muchos sistemas, cuando la empresa ya lo tiene como estándar o para dependencias complejas entre equipos. El provider de Databricks para Airflow puede lanzar jobs y esperar a que terminen.

#### ¿Qué hace la tarea For each?

Ejecuta una tarea anidada una vez por cada elemento de una lista (por ejemplo una lista de países o de fechas), con una concurrencia configurable, para no tener que definir una tarea por elemento.

#### ¿Para qué sirve la tarea de condición If/else?

Para ramificar un job según un valor, como un task value o un parámetro: por ejemplo, saltarse el paso de publicación cuando una tarea de calidad de datos informa cero filas válidas.

#### ¿Cómo se limitan las ejecuciones concurrentes de un job?

Con el ajuste de máximo de ejecuciones concurrentes (normalmente 1 para los jobs que escriben en las mismas tablas) y la opción de cola, para que un nuevo disparo espere en lugar de omitirse o ejecutarse en paralelo.

#### ¿Cómo se ejecuta un job para hacer el backfill de muchas fechas?

Parametrizando el job por fecha y lanzándolo por cada fecha (con la API, la CLI o una tarea For each sobre una lista de fechas), manteniendo las escrituras idempotentes y limitando la concurrencia para que el backfill no deje sin recursos a la producción.

### Spark y rendimiento en Databricks

#### ¿Cómo se lee un plan de consulta de Spark?

Con `df.explain(mode="formatted")` o en la pestaña SQL de la Spark UI. Se lee de abajo hacia arriba: lecturas (revisa los filtros empujados y los archivos descartados), exchanges (shuffles), estrategias de join (broadcast, sort-merge) y agregaciones. El perfil de consulta de Databricks SQL muestra lo mismo con los tiempos.

#### ¿Qué es la Adaptive Query Execution?

Una función de Spark, activada por defecto, que vuelve a optimizar una consulta entre stages con estadísticas de ejecución: fusiona las particiones pequeñas del shuffle, cambia los joins sort-merge por joins broadcast cuando un lado resulta pequeño y divide las particiones con skew.

#### ¿Qué es un broadcast join y cuándo ayuda?

Spark envía una copia de la tabla pequeña a cada executor, de modo que la tabla grande se une sin hacer shuffle. Ayuda cuando un lado es lo bastante pequeño (decenas de MB por defecto, más con hints). Hacer broadcast de una tabla demasiado grande provoca errores de memoria en el driver o en los executors.

#### ¿Qué es el data skew y cómo se corrige?

Algunas claves tienen muchas más filas que otras, así que unas pocas tareas tardan mucho más que el resto. Soluciones: dejar que AQE divida las particiones con skew, hacer broadcast del lado pequeño, filtrar o tratar aparte las claves calientes (a menudo los nulos) o aplicar salting a la clave para repartirla entre particiones.

#### ¿Qué es el spill y por qué es lento?

Cuando los datos de una tarea no caben en la memoria de ejecución, Spark los escribe en el disco local y los vuelve a leer. Aparece en la Spark UI como spill (memory) y spill (disk). Se corrige con más particiones y más pequeñas, workers más grandes u optimizados para memoria, o menos datos por tarea.

#### ¿Cómo se elige el número de particiones del shuffle?

`spark.sql.shuffle.partitions` vale 200 por defecto. Con AQE, define un número generoso (o `auto` en Databricks) y deja que AQE las fusione. Apunta a particiones de unos 100–200 MB después del shuffle; muy pocas causan spill, demasiadas causan sobrecarga.

#### ¿Por qué las UDF de Python son lentas y qué alternativas hay?

Cada fila se serializa entre la JVM y un worker de Python, y el optimizador no puede ver dentro de la función. Usa primero las funciones integradas, luego las UDF de pandas (vectorizadas) con Arrow, o UDF SQL. Photon tampoco puede acelerar las UDF de Python.

#### ¿Conviene usar `cache()` en Databricks?

Con moderación. El caché ayuda cuando el mismo DataFrame se reutiliza varias veces en una sesión interactiva, pero consume memoria y no está disponible en serverless. El disk cache (caché automático en SSD de los archivos Parquet remotos en algunos tipos de instancia) suele dar el beneficio sin cambiar el código. Para reutilizar entre jobs, escribe una tabla.

#### ¿Qué es el disk cache?

Un caché automático, antes llamado Delta cache, que guarda copias de los archivos Parquet y Delta remotos en los SSD locales de los workers, para que las lecturas repetidas de los mismos datos sean más rápidas. Se administra de forma transparente.

#### ¿Por qué es un problema `withColumn` dentro de un bucle?

Cada llamada añade una proyección al plan lógico, y analizar un plan muy profundo se vuelve lento (puede tardar minutos antes de procesar ningún dato). Usa un solo `select` o `withColumns` con un diccionario.

#### ¿Qué es la optimización predictiva?

Una función de Unity Catalog que ejecuta automáticamente `OPTIMIZE`, `VACUUM` y la recolección de estadísticas en las tablas administradas cuando predice un beneficio, para que no tengas que programar jobs de mantenimiento.

#### ¿Cómo se reduce el costo de un job pesado de Databricks?

Usando cómputo de jobs o serverless en lugar de clusters all-purpose, activando Photon donde compense, procesando de forma incremental en lugar de recalcularlo todo, reduciendo las lecturas con clustering y filtros, dimensionando y autoescalando bien los clusters, usando workers spot, evitando shuffles innecesarios y UDF de Python, y monitoreando con `system.billing.usage`.

#### ¿Qué es `replaceWhere`?

Una opción de escritura que reemplaza de forma atómica solo las filas que cumplen un predicado, normalmente un rango de fechas, sin tocar el resto de la tabla. Hace idempotente el reprocesamiento de un periodo.

```python
(df.write.format("delta").mode("overwrite")
   .option("replaceWhere", "event_date = '2026-10-15'")
   .saveAsTable("silver.events"))
```

#### ¿Cómo investigarías un job que de repente se volvió más lento?

Comparando la ejecución lenta con una normal: tamaños de entrada, número de archivos (archivos pequeños, falta de `OPTIMIZE`), cambios de plan (un broadcast que pasó a sort-merge join), skew en un stage, spill, tamaño del cluster o pérdida de instancias spot, y cambios en el código o en los datos desde la última ejecución buena.

#### ¿Qué diferencia hay entre transformaciones narrow y wide?

Las transformaciones narrow (`filter`, `select`, `withColumn`) calculan cada partición de salida a partir de una partición de entrada, sin mover datos. Las wide (`groupBy`, `join`, `distinct`, `orderBy`) necesitan un shuffle por la red. Optimizar el rendimiento consiste sobre todo en controlar los shuffles.

#### ¿Qué diferencia hay entre `repartition` y `coalesce`?

`repartition(n)` hace un shuffle completo y puede aumentar o reducir el número de particiones, opcionalmente por columnas. `coalesce(n)` solo fusiona particiones sin shuffle completo, así que es más barato pero solo puede reducirlas y puede dejarlas desiguales. `coalesce(1)` hace pasar todo por una sola tarea.

#### ¿Por qué un `count()` antes de cada paso ralentiza un job?

Cada acción dispara la ejecución completa del plan hasta ese punto. Contar para los logs después de cada transformación recalcula los datos una y otra vez. Toma las métricas del commit de Delta (`numOutputRows` en el historial) o calcúlalas una sola vez.

#### ¿Qué son las estadísticas de columnas y por qué calcularlas?

`ANALYZE TABLE … COMPUTE STATISTICS FOR ALL COLUMNS` guarda el número de filas y las estadísticas de las columnas que usa el optimizador basado en costos para elegir el orden y la estrategia de los joins. La optimización predictiva puede mantenerlas automáticamente.

#### ¿En qué se diferencia el descarte de archivos del descarte de particiones?

El descarte de particiones (partition pruning) salta directorios enteros según las columnas de partición. El descarte de archivos (data skipping) salta archivos individuales usando las estadísticas mínimo/máximo del log de Delta, así que funciona con cualquier columna con estadísticas y se beneficia del clustering.

### Databricks SQL y analítica

#### ¿Qué es Databricks SQL?

La parte de data warehousing SQL de la plataforma: SQL warehouses, un editor SQL, historial y perfiles de consultas, alertas, dashboards y conectores para herramientas de BI (Power BI, Tableau, Looker) por JDBC/ODBC.

#### ¿Qué son los dashboards AI/BI y Genie?

Los dashboards AI/BI son los dashboards actuales de Databricks, construidos sobre SQL warehouses con ayuda de IA para crearlos. Genie es una interfaz en lenguaje natural donde los usuarios de negocio hacen preguntas sobre tablas seleccionadas y reciben respuestas respaldadas por SQL.

#### ¿Qué es una vista materializada en Databricks SQL?

Una vista cuyos resultados se guardan y se refrescan (de forma programada o bajo demanda, incremental cuando se puede). Acelera las agregaciones costosas de los dashboards. Se crea con `CREATE MATERIALIZED VIEW` y corre sobre pipelines serverless.

#### ¿Qué son las alertas SQL?

Consultas programadas que comparan un resultado con un umbral y notifican (correo, Slack, webhook) cuando se cumple la condición, por ejemplo cuando un control de calidad de datos devuelve filas.

#### ¿Para qué sirve la federación de consultas en analítica?

Para unir tablas de Databricks con tablas que todavía están en una base de datos operativa u otro warehouse, para explorar o migrar, sin construir primero una ingesta. Para un uso intensivo y repetido, ingerir los datos es más rápido y más barato.

#### ¿Qué diferencia hay entre una vista, una vista temporal y una vista materializada?

Una vista guarda solo la consulta y la ejecuta en cada lectura. Una vista temporal solo existe en la sesión actual. Una vista materializada guarda resultados precalculados y hay que refrescarla.

#### ¿Cómo se conectan las herramientas de BI a Databricks?

Con drivers JDBC/ODBC o conectores nativos (Power BI, Tableau, Looker, Excel) que apuntan a un SQL warehouse, autenticándose con OAuth o con tokens. Unity Catalog aplica los permisos de la identidad que se conecta.

#### ¿Qué es el caché de resultados de Databricks SQL?

Un caché de resultados de consultas en los SQL warehouses: cuando la misma consulta se ejecuta de nuevo y las tablas no han cambiado, el resultado se devuelve sin recalcularlo.

#### ¿Qué es una metric view?

Un objeto de Unity Catalog que define las métricas de negocio (medidas y dimensiones) una sola vez en YAML sobre una tabla, para que los dashboards, Genie y los usuarios de SQL las calculen de forma coherente.

### Arquitectura medallion y modelado

#### ¿Qué es la arquitectura medallion?

Una forma de organizar los datos del lakehouse por capas: bronze guarda los datos en bruto tal como llegan (solo añadir, con metadatos de carga), silver guarda los datos limpios, homogeneizados, deduplicados y validados, y gold guarda agregados de negocio y modelos dimensionales listos para BI y ML. La calidad y la estructura aumentan capa por capa.

#### ¿Por qué conservar una capa bronze en bruto?

Para poder reprocesar el historial cuando cambia la lógica o se encuentran errores, auditar lo que el origen envió realmente y desacoplar la ingesta de la transformación. Bronze debe ser barato de conservar y fiel al origen.

#### ¿Qué va en silver?

Columnas tipadas y renombradas, deduplicación, valores estandarizados (fechas, códigos, direcciones), uniones con datos de referencia, controles de calidad con cuarentena de las filas defectuosas e historial (SCD tipo 2) cuando hace falta. Silver es la versión única y confiable de cada entidad.

#### ¿Qué va en gold?

Datos con la forma que necesita el consumo: esquemas en estrella (hechos y dimensiones), agregados, tablas de features y productos de datos, con las definiciones de negocio aplicadas. Las tablas gold suelen ser más pequeñas y están optimizadas para la lectura.

#### ¿Cómo se implementa una SCD tipo 2 en Delta?

Con `MERGE`: se cierra la fila vigente (se llenan `valid_to` e `is_current = false`) cuando cambian los atributos seguidos, y se inserta la nueva versión. Un truco común es hacer merge de una unión de las actualizaciones con una clave de merge nula para las filas modificadas, de modo que un solo `MERGE` cierre e inserte. Los pipelines declarativos lo hacen con `AUTO CDC … STORED AS SCD TYPE 2`.

#### ¿Cómo se ponen en cuarentena los registros defectuosos?

Validando las filas contra reglas en silver, escribiendo las filas que fallan con sus motivos en una tabla de cuarentena y siguiendo con las válidas. Vigila la tasa de cuarentena y genera alertas ante picos. En los pipelines declarativos se logra lo mismo con expectativas `DROP ROW` y una consulta inversa aparte.

#### ¿Conviene usar un catálogo por entorno o por capa?

Un patrón común es un catálogo por entorno (`dev`, `staging`, `prod`) con esquemas por capa (`bronze`, `silver`, `gold`), porque los entornos necesitan permisos y almacenamiento distintos. Algunos equipos prefieren catálogos por dominio o unidad de negocio. Importa más la coherencia que la elección.

#### ¿Qué es un producto de datos en el contexto de Databricks?

Un conjunto de tablas (normalmente gold) seleccionado, documentado y gobernado, del que es responsable un equipo, con controles de calidad, una interfaz clara y acceso concedido mediante Unity Catalog, posiblemente compartido con Delta Sharing.

#### ¿La arquitectura medallion tiene siempre tres capas?

No. Es una convención, no una regla. Los proyectos pequeños pueden fusionar silver y gold; otros añaden una zona de aterrizaje (landing) antes de bronze o una capa de servicio (platinum) después de gold. Lo importante es que cada capa tenga un contrato claro.

#### ¿Bronze debe ser una tabla Delta o archivos en bruto?

Por lo general, los archivos en bruto se quedan en una zona de landing (o un volumen) y bronze es una tabla Delta cargada desde ellos con cambios mínimos y metadatos de carga. Delta en bronze aporta transacciones, seguimiento del esquema y reprocesamiento rápido; conservar los archivos originales da una copia exacta para auditorías.

#### ¿Cómo se modela gold para BI y para ML a la vez?

Con esquemas en estrella (hechos con un grano declarado y dimensiones conformadas) para BI, y tablas de features por entidad y fecha para ML, ambos construidos desde las mismas tablas silver para que las cifras coincidan.

### Machine learning e IA

#### ¿Qué es MLflow?

Una plataforma de código abierto, creada por Databricks, para el ciclo de vida del ML: seguimiento de experimentos (parámetros, métricas, artefactos), empaquetado de modelos, un registro de modelos con versiones y alias, evaluación, y trazas para aplicaciones de IA generativa. En Databricks es un servicio administrado e integrado con Unity Catalog.

#### ¿Qué significa registrar un modelo en Unity Catalog?

Los modelos se guardan como objetos de Unity Catalog (`catalogo.esquema.modelo`) con versiones y alias como `champion`, gobernados con los mismos permisos y el mismo linaje que las tablas, y utilizables desde varios workspaces.

#### ¿Qué es una tabla de features?

Una tabla Delta con clave primaria que sirve para guardar features de ML en Unity Catalog. Los conjuntos de entrenamiento se construyen uniendo tablas de features con las etiquetas (con corrección point-in-time para las series temporales), y las mismas features se pueden servir en línea para la inferencia.

#### ¿Qué es Model Serving?

Un servicio serverless que expone modelos (modelos MLflow propios, modelos fundacionales, modelos externos) como endpoints REST con autoescalado, monitoreo y control de acceso.

#### ¿Qué es Vector Search?

Una base de datos vectorial administrada que indexa embeddings de una tabla Delta y mantiene el índice sincronizado, usada para la generación aumentada por recuperación (RAG) y la búsqueda por similitud.

#### ¿Qué son las funciones de IA en Databricks SQL?

Funciones SQL como `ai_query`, `ai_classify`, `ai_extract`, `ai_summarize` y `ai_translate` que llaman a modelos desde SQL, para enriquecer tablas con la salida de un LLM en batch.

### Seguridad, costos y operación

#### ¿Cómo accede Databricks de forma segura a los datos en AWS S3?

Mediante roles IAM: en Unity Catalog, una storage credential encapsula un rol IAM que confía en Databricks, y las external locations dan acceso a las rutas. Las instalaciones antiguas usaban instance profiles asociados a los clusters. Hay que evitar las claves de acceso en el código.

#### ¿Qué opciones de seguridad de red existen?

Desplegar el cómputo clásico en tu propia VPC/VNet, conectividad privada entre el plano de control y el de cómputo (PrivateLink, Private Link), listas de IP permitidas, nodos sin IP pública, políticas de red serverless para controlar la salida y claves administradas por el cliente para el cifrado.

#### ¿Cómo se audita quién accedió a qué?

Con los logs de auditoría (disponibles en la tabla `system.access.audit`), el linaje de Unity Catalog y el historial de consultas. Registran los inicios de sesión, los cambios de permisos, el acceso a los datos y las acciones sobre los jobs.

#### ¿Cómo se monitorea y controla el gasto en Databricks?

Etiquetando clusters, jobs y warehouses con centros de costo, consultando `system.billing.usage` unido a los precios de lista, definiendo presupuestos y alertas, imponiendo políticas de cluster (tipos de instancia, autoterminación, máximo de workers), usando serverless o cómputo de jobs en producción y revisando con regularidad los jobs más caros.

#### ¿Qué son los Databricks Asset Bundles?

Una forma de describir los recursos de Databricks (jobs, pipelines, dashboards, modelos, permisos) en YAML junto al código en Git, con targets para cada entorno. La CLI los valida, los despliega y los ejecuta, lo que permite desplegar los proyectos de Databricks con CI/CD.

```yaml
bundle:
  name: sales_pipeline
targets:
  dev:
    mode: development
    default: true
  prod:
    mode: production
resources:
  jobs:
    daily_sales:
      name: daily_sales
      tasks:
        - task_key: build
          notebook_task:
            notebook_path: ./src/build_sales.py
```

#### ¿Qué cambia `mode: development` en un target del bundle?

Añade el nombre del usuario como prefijo de los recursos desplegados, pausa las programaciones y los disparadores, y despliega en una carpeta por usuario, para que varios desarrolladores puedan desplegar el mismo bundle sin pisarse. `mode: production` comprueba que el despliegue se haga como service principal (o una identidad fija) y no use esos atajos.

#### ¿Cómo se configura CI/CD para Databricks?

Guardando el código y las definiciones del bundle en Git, ejecutando pruebas unitarias (con Spark local o Databricks Connect) y linting en los pull requests, validando el bundle, desplegando en un target de staging y ejecutando pruebas de integración, y luego desplegando en producción tras una aprobación, todo como service principal autenticado con OAuth o con federación de identidades de carga de trabajo.

#### ¿Cómo se prueba código PySpark para Databricks?

Separando las transformaciones en funciones puras que reciben y devuelven DataFrames, probándolas con pytest sobre una SparkSession local y datos de prueba pequeños (comparando con `assertDataFrameEqual`), añadiendo pruebas de extremo a extremo con datos sintéticos y ejecutando controles de calidad de datos (expectativas, restricciones) dentro del propio pipeline.

#### ¿Qué son las Databricks Apps?

Una forma de construir y alojar aplicaciones de datos e IA (Streamlit, Dash, Gradio, Flask y otras) directamente en el workspace, con autenticación y acceso a datos gobernados mediante Unity Catalog.

#### ¿Qué es Lakebase?

Una base de datos operativa administrada compatible con PostgreSQL dentro de Databricks, basada en Postgres serverless, pensada para cargas transaccionales de baja latencia (aplicaciones, servicio de features) que se sincronizan con las tablas del lakehouse.

### Escenarios

#### Diseña un pipeline que ingiera archivos CSV diarios desde S3 hasta una tabla de reportes.

Deja los archivos en S3, léelos con Auto Loader (trigger `availableNow`) hacia una tabla Delta bronze con un esquema declarado y columnas de `_metadata`, limpia, deduplica y valida hacia silver con `MERGE`, construye agregados gold o un esquema en estrella, prográmalo como job con reintentos y alertas, gobiérnalo con Unity Catalog y despliégalo con un bundle.

#### Un job diario escribe duplicados cada vez que se vuelve a ejecutar. ¿Qué cambias?

Reemplazo el append por una escritura idempotente: un `MERGE` sobre la clave de negocio, o `replaceWhere` sobre la fecha procesada. Tomo la fecha de un parámetro del job y añado un control de unicidad sobre el destino.

#### Tu tabla Delta tiene 500.000 archivos pequeños. ¿Qué haces?

Ejecuto `OPTIMIZE` (con liquid clustering sobre las columnas de filtro principales), activo las escrituras optimizadas y la auto compactación o la optimización predictiva, y luego corrijo la causa: agrupar los microappends, evitar el particionamiento excesivo y usar triggers `availableNow` en lugar de streams diminutos muy frecuentes. Después ejecuto `VACUUM` para borrar los archivos antiguos.

#### Un join entre una tabla de hechos de 2 TB y una dimensión de 50 MB es lento. ¿Qué revisas?

Si se hace broadcast (revisa el plan; añade un hint de broadcast o sube el umbral), si la lectura de los hechos descarta archivos (filtros sobre columnas agrupadas), el skew en la clave del join y el spill. Una dimensión de 50 MB debería ir casi siempre en broadcast.

#### Una consulta de streaming falla tras un cambio de esquema en el origen. ¿Cómo lo manejas?

Con Auto Loader en modo `addNewColumns`, reinicia el stream para que tome el esquema nuevo. Para los cambios incompatibles, actualiza el esquema destino (o usa la columna de datos rescatados) y, si cambió la lógica, empieza un checkpoint nuevo con un plan de backfill claro. Añade alertas sobre los datos rescatados.

#### Los analistas solo deben ver las filas de su país en una tabla compartida. ¿Cómo lo implementas?

Asocio a la tabla una función de row filter de Unity Catalog que compruebe los grupos del usuario contra la columna de país. Concedo `SELECT` a los grupos de analistas. Uso column masks para las columnas sensibles.

#### ¿Cómo migrarías un pipeline on-premises basado en Hive a Databricks?

Inventariando los jobs, las tablas y las dependencias; copiando los datos al almacenamiento en la nube y convirtiéndolos a Delta (`CONVERT TO DELTA` para Parquet); pasando el HiveQL a Spark SQL (casi todo es compatible); reemplazando Oozie o cron por Lakeflow Jobs o Airflow; registrando las tablas en Unity Catalog; y validando los resultados lado a lado (número de filas, checksums, agregados) antes de cambiar a los consumidores.

#### Alguien borró por error columnas de una tabla gold hace una hora. ¿Cómo la recuperas?

Busco en `DESCRIBE HISTORY` la versión anterior al cambio y ejecuto `RESTORE TABLE … TO VERSION AS OF` esa versión, o hago un `SELECT` sobre ella para reconstruirla. Después reviso los permisos para que solo el service principal del pipeline pueda modificar las tablas gold.

#### ¿Cómo abaratas el desarrollo para un equipo de diez ingenieros?

Con clusters pequeños o de un solo nodo, con políticas y autoterminación corta, notebooks serverless, muestras de datos de desarrollo compartidas o shallow clones en lugar de copias completas, pruebas unitarias locales para la mayor parte de la lógica, bundles en modo desarrollo y una alerta de presupuesto por equipo.

#### ¿Cómo le explicas el lakehouse a una persona de negocio?

Un solo lugar para todos los datos de la empresa, guardados una vez en formatos abiertos en la propia cuenta de nube de la empresa, donde los reportes, la ciencia de datos y la IA trabajan sobre las mismas cifras confiables, con permisos y registros de auditoría administrados de forma centralizada.

#### Un notebook funciona en tu cluster pero falla como job serverless. ¿Por qué?

Probablemente porque usa algo no admitido en serverless (Spark Connect): RDD, `sparkContext`, `cache()`, la mayoría de las llamadas a `spark.conf.set`, init scripts o librerías que necesitan la JVM. Reescríbelo con las APIs de DataFrame, declara las dependencias en el entorno y pruébalo en serverless antes de desplegarlo.

#### ¿Cómo compartes tablas gold con una empresa socia que no usa Databricks?

Con Delta Sharing abierto: creo un share con las tablas, creo un destinatario con una credencial basada en token, y el socio lo lee desde pandas, Spark o una herramienta de BI. El acceso se puede revocar en cualquier momento y queda auditado.

#### La factura mensual de Databricks se duplicó. ¿Cómo lo investigas?

Consulto `system.billing.usage` por SKU, workspace, job, warehouse y etiqueta, y comparo los meses. Busco clusters all-purpose sin autoterminación, jobs que pasaron a cómputo all-purpose, warehouses que nunca se detienen, full refreshes, cargas serverless nuevas y reintentos descontrolados.

#### ¿Cómo atiendes una solicitud de borrado del RGPD/GDPR o de habeas data en un lakehouse Delta?

Borro las filas de la persona con `DELETE` o `MERGE` en todas las capas (bronze incluida) y luego ejecuto `VACUUM` para eliminar físicamente los archivos antiguos que las contenían, pasado el periodo de retención. Seudonimizar los identificadores al inicio del pipeline limita el número de tablas con datos personales.
