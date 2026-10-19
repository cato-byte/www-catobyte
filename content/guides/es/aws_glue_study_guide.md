## Guía de estudio de AWS Glue

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de AWS Glue: unas 200 preguntas](../../images/aws_glue_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre AWS Glue: el Data Catalog, los crawlers, los jobs ETL con Spark, los DynamicFrames, los job bookmarks, los workers y los costos, el streaming, la calidad de datos, la orquestación, la seguridad con Lake Formation y la optimización del rendimiento. Las respuestas reflejan el servicio en 2026.

La guía sigue una ruta de aprendizaje en cuatro etapas. Cada sección se divide en unidades cortas: objetivos de aprendizaje, una explicación del concepto y un ejemplo resuelto, luego preguntas (primero de memoria, después de aplicación), un reto práctico e ideas clave. Para **aprender**, lee cada unidad de principio a fin. Para **repasar**, cambia al modo repaso o usa "Ir a las preguntas", marca las respuestas que quieras volver a ver y prueba un repaso mixto entre secciones.

<!-- QA -->
<!-- stage: Fundamentos -->

### Fundamentos

<!-- unit: Qué es Glue -->

<!-- goals -->

- Explicar qué hace AWS Glue y qué componentes tiene.
- Ubicar Glue en un data lake de AWS, para ETL y ELT.

<!-- concept -->

Un data lake necesita dos cosas además del almacenamiento: una descripción compartida de qué son los datos y jobs que conviertan archivos crudos en tablas útiles. Glue aporta ambas. Su catálogo es el inventario que leen Athena, Redshift y EMR; sus crawlers lo llenan; sus jobs Spark serverless hacen la transformación.

"Serverless" aquí significa que eliges un tamaño y pagas por segundo de uso, sin cluster encendido. Encaja con trabajo batch que corre unas veces al día y queda inactivo entre medio.

<!-- example -->

```text
sources ─► S3 raw ─► Glue job (Spark) ─► S3 curated (Parquet/Iceberg)
                │                               │
                └──────► Glue Data Catalog ◄────┘ ◄── Athena, Redshift, EMR
```

#### ¿Qué es AWS Glue?

Un servicio serverless de integración de datos de AWS para descubrir, preparar, mover e integrar datos. Sus partes principales son el Glue Data Catalog (un repositorio central de metadatos), los crawlers (descubrimiento de esquemas), los jobs ETL (Apache Spark o Python), Glue Studio (creación visual), Data Quality, DataBrew (preparación visual de datos) y los workflows para la orquestación.

#### ¿Qué significa "serverless" en Glue?

No aprovisionas ni administras clusters: eliges un tipo y un número de workers (o dejas que el autoescalado decida), Glue arranca el entorno para la ejecución del job y solo pagas el tiempo que corre el job, por segundo.

#### ¿Cuáles son los principales casos de uso de Glue?

Construir data lakes en S3 (catalogar y transformar los datos en bruto a Parquet o Iceberg), ETL hacia Redshift u otras bases de datos, preparar datos para Athena y machine learning, ingesta CDC y streaming, y ofrecer un catálogo de metadatos compartido para Athena, EMR, Redshift Spectrum y Lake Formation.

#### ¿Cuáles son los componentes principales de AWS Glue, en una frase cada uno?

El Data Catalog guarda los metadatos; los crawlers descubren esquemas; los jobs ETL transforman datos con Spark o Python; los triggers y workflows orquestan; Glue Studio ofrece creación visual; Data Quality valida los datos; DataBrew prepara datos de forma visual; el Schema Registry gobierna los esquemas de streaming.

#### ¿Cómo encaja Glue en la arquitectura de data lake de AWS?

Los datos llegan a S3 (desde DMS, Kinesis, AppFlow, cargas manuales), los crawlers o los jobs los registran en el Data Catalog, los jobs de Glue los limpian y convierten en zonas curadas (Parquet o Iceberg), Lake Formation gobierna el acceso, y Athena, Redshift, EMR, QuickSight y SageMaker los consumen.

#### ¿Qué es ETL frente a ELT en el contexto de Glue?

Con ETL, los jobs de Glue transforman los datos antes de cargarlos en el destino (por ejemplo, limpiar y convertir a Parquet antes de Redshift). Con ELT, los datos en bruto se cargan primero y se transforman dentro del destino (SQL de Redshift, dbt sobre Athena). Glue se usa a menudo para la "E" y la "L" del ELT, o como la "T" en un lakehouse.

#### ¿Cómo le explicarías AWS Glue a una persona no técnica?

Es el servicio de AWS que mantiene un inventario de los datos de la empresa y que limpia y mueve esos datos para dejarlos listos para reportes y análisis, sin tener que administrar servidores.

<!-- challenge -->

Un equipo escribe scripts de Python en una instancia EC2 que convierten CSV a Parquet cada noche. ¿Qué aportaría Glue y qué tendrían que seguir diseñando?

<!-- solution -->

Glue quitaría el servidor, escalaría la conversión con Spark, registraría tablas en el catálogo y seguiría las ejecuciones. El equipo aún decide particionado, tamaño de archivos, lógica incremental, calendarios y reglas de calidad.

<!-- takeaways -->

- Glue combina un catálogo, crawlers y jobs Spark serverless.
- Athena, Redshift y EMR comparten el catálogo.
- Serverless encaja con batch que tiene tiempo inactivo entre ejecuciones.

<!-- unit: Glue entre los servicios de AWS -->

<!-- goals -->

- Comparar Glue con EMR, Lambda, DataBrew y otras plataformas.
- Elegir un servicio de procesamiento para una carga.

<!-- concept -->

AWS tiene varias formas de correr transformaciones, y difieren sobre todo en cuánto administras y en el tamaño del trabajo. Lambda maneja archivos pequeños dirigidos por eventos. Glue maneja ETL batch con Spark sin clusters. EMR maneja cargas que necesitan control total o muchos motores open source. DataBrew da a los analistas una herramienta visual.

El catálogo de Glue está debajo de la mayoría, por eso se puede cambiar de motor sin mover los metadatos.

<!-- example -->

| Carga | Buena opción |
|---|---|
| Transformar cada archivo de 2 MB al llegar | Lambda |
| CSV nocturno de 500 GB a Parquet | Glue |
| Spark de larga duración con configs propias y ajuste de Hudi | EMR |
| Un analista limpia visualmente un dataset tipo hoja de cálculo | DataBrew |

#### ¿Cómo se compara Glue con Amazon EMR?

Glue es serverless y está enfocado en ETL con Spark, con catálogo, bookmarks y calidad de datos integrados; cambias control por sencillez. EMR (sobre EC2, EKS o Serverless) da control total de Spark, Hadoop, Hive, Trino y otros frameworks, sus versiones y su ajuste, y suele ser más barato para cargas grandes y estables.

#### ¿Cómo se compara Glue con AWS Lambda para ETL?

Lambda sirve para transformaciones pequeñas disparadas por eventos (un archivo de pocos MB), con un límite de 15 minutos y memoria limitada. Glue sirve para procesamiento distribuido más grande con Spark, ejecuciones largas y grandes volúmenes.

#### ¿Qué es AWS Glue DataBrew?

Una herramienta visual de preparación de datos con más de 250 transformaciones integradas, usada por analistas para limpiar y normalizar datos sin código. Las transformaciones se guardan como recetas y se ejecutan como jobs sobre datos en S3, con perfilado de datos.

#### ¿Qué relación hay entre Glue y SageMaker Lakehouse/Unified Studio?

El Glue Data Catalog es la base de metadatos de SageMaker Lakehouse, y las funciones de integración de datos de Glue (jobs ETL, ETL visual, conexiones, zero-ETL) están disponibles dentro de SageMaker Unified Studio, el entorno unificado de AWS para datos, analítica e IA.

#### ¿Cómo eliges entre Glue, EMR Serverless y Databricks para una nueva plataforma de datos en AWS?

Glue para ETL serverless muy integrado con el catálogo de AWS y Lake Formation; EMR Serverless para Spark/Hive de código abierto con más control y a menudo menor costo a escala; Databricks para una plataforma lakehouse unificada con notebooks colaborativos, Delta, Unity Catalog y ML. Deciden las habilidades del equipo, los requisitos de gobierno y los modelos de costo.

<!-- challenge -->

Una Lambda que convierte archivos subidos empezó a superar el timeout porque algunos archivos ahora pesan 3 GB. ¿Qué recomiendas?

<!-- solution -->

Pasar el procesamiento de archivos grandes a un job de Glue (disparado por EventBridge o un calendario), que no tiene el límite de 15 minutos y escala con Spark. Dejar Lambda solo para archivos pequeños o para lanzar el job de Glue.

<!-- takeaways -->

- Lambda para eventos pequeños; Glue para ETL batch con Spark; EMR para control.
- DataBrew atiende visualmente a los analistas.
- El catálogo de Glue se comparte entre motores.

<!-- unit: Facturación, versiones y límites -->

<!-- goals -->

- Explicar las DPU y estimar cómo factura Glue los jobs.
- Elegir versiones de Glue y conocer las cuotas principales.

<!-- concept -->

El precio de Glue es simple: capacidad por tiempo. Una DPU es una cantidad fija de CPU y memoria, y pagas DPU por segundo mientras corre un job. El costo depende de elegir bien el tamaño y terminar rápido, no del volumen de datos directamente.

Cada versión de Glue empaqueta una versión de Spark y de Python, que afecta velocidad, arranque y funciones disponibles. Catálogos regionales, cuotas de servicio y herramientas de desarrollo completan el panorama operativo.

<!-- example -->

```text
10 G.1X workers × 1 DPU × 0.25 h × 0.44 USD/DPU-hour ≈ 1.10 USD per run
same job on Glue 5.0, 40% faster          ≈ 0.66 USD per run
```

#### ¿Qué es un DPU?

Una Data Processing Unit: 4 vCPU y 16 GB de memoria. Glue factura los jobs ETL, los crawlers y las sesiones interactivas en DPU-hora, por segundo.

#### ¿Cómo se factura un job de Glue?

Por DPU-hora, por segundo, con un mínimo de 1 minuto para los jobs Spark desde Glue 2.0. El costo es número de DPU × duración × precio por DPU-hora (unos 0,44 USD en muchas regiones, menos con Flex). Los jobs Python shell facturan 1/16 o 1 DPU.

#### ¿Qué son las versiones de Glue y por qué importan?

Cada versión de Glue empaqueta una versión de Spark, Python y Java y unos conectores: por ejemplo Glue 4.0 corre Spark 3.3 y Python 3.10, y Glue 5.0 corre Spark 3.5 y Python 3.11. Las versiones nuevas arrancan más rápido, corren más rápido y admiten formatos de tabla más nuevos. Las versiones viejas pierden soporte, así que actualizar es parte del mantenimiento.

#### ¿Qué cuotas de servicio de Glue conviene conocer?

Límites de ejecuciones concurrentes de jobs por cuenta, DPU máximos por job, número de jobs, triggers, crawlers, bases de datos, tablas y particiones por tabla. La mayoría se puede ampliar en Service Quotas; los data lakes grandes chocan primero con los límites de particiones y de concurrencia.

#### ¿En qué regiones está Glue y el catálogo es regional?

Glue está disponible en la mayoría de las regiones de AWS, y el Data Catalog es regional: cada región tiene su propio catálogo por cuenta. El acceso entre regiones requiere replicar los metadatos o usar resource links de Lake Formation.

#### ¿Qué es Glue Studio?

La experiencia de consola para crear, ejecutar y monitorear jobs de Glue: un editor visual en el que armas el ETL como un grafo de orígenes, transformaciones y destinos (que genera código PySpark), un editor de scripts, un editor de notebooks y dashboards de monitoreo de jobs.

#### ¿Qué es un development endpoint y qué lo reemplazó?

Un entorno heredado, siempre encendido, para desarrollar scripts de Glue desde notebooks, facturado mientras corría. Lo reemplazaron las sesiones interactivas y los notebooks de Glue Studio, bajo demanda, con facturación por segundo y timeouts de inactividad.

<!-- challenge -->

Un job en Glue 2.0 corre 40 minutos sobre 20 workers G.1X cada hora. Nombra dos cambios que probablemente bajen su costo.

<!-- solution -->

Actualizar a la última versión de Glue (Spark más nuevo, ejecución y arranque más rápidos) y activar auto scaling para que bajen los workers cuando las etapas necesiten menos. Luego revisar si las ejecuciones horarias podrían procesar de forma incremental.

<!-- takeaways -->

- Pagas DPU × tiempo, facturado por segundo.
- Las versiones nuevas de Glue suelen ser más rápidas y baratas.
- El catálogo es regional; las cuotas limitan la concurrencia.

### Data Catalog

<!-- unit: Bases de datos y tablas -->

<!-- goals -->

- Describir qué guarda el Data Catalog y cómo llegan las tablas a él.
- Usar propiedades de tabla y saber qué significa "externa".

<!-- concept -->

El Data Catalog es un metastore: guarda descripciones de datos, nunca los datos. Las bases agrupan tablas, y las tablas registran una ubicación, un esquema, un formato y propiedades que dicen a los motores cómo leer los archivos. Como todos los servicios analíticos leen las mismas entradas, una propiedad equivocada rompe consultas en todas partes.

Las tablas pueden crearse con crawlers, DDL, jobs o infraestructura como código. En pipelines propios, las definiciones explícitas son más predecibles que el descubrimiento.

<!-- example -->

```python
glue.create_table(DatabaseName="curated", TableInput={
    "Name": "orders",
    "StorageDescriptor": {
        "Columns": [{"Name": "order_id", "Type": "bigint"}, {"Name": "amount", "Type": "decimal(12,2)"}],
        "Location": "s3://lake/curated/orders/",
        "InputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
        "SerdeInfo": {"SerializationLibrary": "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"}},
    "PartitionKeys": [{"Name": "dt", "Type": "string"}],
    "Parameters": {"classification": "parquet"}})
```

#### ¿Qué es el Glue Data Catalog?

Un repositorio de metadatos administrado y compatible con el Hive metastore, por cuenta y región. Guarda bases de datos, tablas (esquema, ubicación, formato, particiones, estadísticas), conexiones y funciones definidas por el usuario. Athena, EMR, Redshift Spectrum, los jobs de Glue y muchos otros servicios lo usan para saber dónde están los datos y cómo leerlos.

#### ¿Qué es una base de datos de Glue?

Un contenedor lógico de tablas en el Data Catalog. No guarda datos; agrupa definiciones de tablas, y con Lake Formation se pueden conceder permisos a nivel de base de datos.

#### ¿Qué es una tabla de Glue?

Metadatos que describen datos: nombres y tipos de las columnas, la ubicación en S3 (o un origen JDBC), el formato (SerDe y formatos de entrada y salida), las claves de partición y las propiedades de la tabla. Los datos se quedan en S3 o en la base de origen.

#### ¿Cómo llegan las tablas al Data Catalog?

Ejecutando crawlers, creando tablas a mano (consola, `CREATE EXTERNAL TABLE` en Athena, CloudFormation, Terraform, la API), desde jobs de Glue que crean o actualizan tablas al escribir (`enableUpdateCatalog`), o desde servicios como los blueprints de Lake Formation y las integraciones zero-ETL.

#### ¿Qué diferencia hay entre una tabla externa y una governed table?

En el Data Catalog todas las tablas basadas en S3 son externas (el catálogo solo guarda metadatos; borrar la tabla no borra los datos). Las governed tables eran un tipo de tabla de Lake Formation con transacciones ACID, hoy retiradas en favor de las tablas Apache Iceberg.

#### ¿Para qué sirven propiedades de tabla como `classification` y `compressionType`?

Indican a los motores y a Glue cómo interpretar los datos: `classification` (csv, json, parquet) la definen los crawlers y la usan los jobs de Glue, mientras que los parámetros del SerDe y la compresión le dicen a Athena o Hive cómo leer los archivos.

#### ¿Qué es una función definida por el usuario en el Data Catalog?

Metadatos de una UDF de Hive (nombre de clase y ubicación del JAR) guardados en el catálogo para que motores como Hive en EMR puedan usarla; importa sobre todo en cargas compatibles con Hive.

<!-- challenge -->

Alguien borra una tabla del catálogo "para limpiar" y fallan las consultas de Athena. ¿Se perdieron los datos? ¿Cómo restauras la tabla?

<!-- solution -->

No, las tablas sobre S3 son externas, así que los archivos siguen ahí. Recrea la tabla desde su definición como código (o desde una versión del catálogo o el DDL de Athena) y vuelve a registrar las particiones o a correr el crawler.

<!-- takeaways -->

- El catálogo guarda metadatos; los datos se quedan en S3.
- Todos los motores leen las mismas entradas de tabla.
- Define las tablas de tus pipelines de forma explícita, como código.

<!-- unit: Particiones y estadísticas -->

<!-- goals -->

- Registrar particiones y mantenerlas coherentes con la tabla.
- Acelerar la planificación con índices de particiones y estadísticas de columnas.

<!-- concept -->

Las particiones también son entradas del catálogo, una por carpeta, cada una con su ubicación y esquema. Eso trae dos consecuencias: los motores solo saltan particiones registradas, y las particiones pueden desviarse de la tabla cuando algo actualiza una pero no la otra.

Cuando crecen las particiones, hasta listarlas se vuelve lento. Los índices de particiones permiten al catálogo filtrarlas en el servidor, y las estadísticas de columnas ayudan a los optimizadores a planear joins.

<!-- example -->

```python
glue.batch_create_partition(DatabaseName="curated", TableName="orders",
    PartitionInputList=[{"Values": ["2026-10-17"],
        "StorageDescriptor": {**table_sd, "Location": "s3://lake/curated/orders/dt=2026-10-17/"}}])
```

#### ¿Qué es una partición en el Data Catalog?

Un subconjunto de los datos de una tabla definido por valores de las claves de partición (por ejemplo `year=2026/month=10/day=15`), cada uno con su propia ubicación en S3. Los motores de consulta solo leen las particiones que cumplen los filtros, lo que reduce costo y tiempo.

#### ¿Cómo se registran las particiones nuevas?

Con un crawler, con `MSCK REPAIR TABLE` o `ALTER TABLE ADD PARTITION` en Athena, con la API `BatchCreatePartition`, con jobs de Glue que escriben actualizando el catálogo, o evitándolo por completo con la proyección de particiones de Athena.

#### ¿Qué son los índices de partición?

Índices sobre las claves de partición de las tablas del catálogo con muchas particiones, para que las llamadas `GetPartitions` con filtros respondan rápido en lugar de recorrer todas las particiones. Aceleran la planificación de consultas en Athena y Glue sobre tablas con decenas de miles de particiones.

#### ¿Qué son las estadísticas de columnas en el Data Catalog?

Estadísticas (número de valores distintos, nulos, mínimo/máximo, longitud media) que Glue calcula para las columnas de las tablas y guarda en el catálogo, y que Athena y Redshift Spectrum usan para la optimización basada en costos, como reordenar los joins.

#### Las consultas de Athena sobre la tabla de Glue fallan con `HIVE_PARTITION_SCHEMA_MISMATCH`. ¿Por qué?

Algunas particiones se registraron con un esquema distinto al de la tabla (un crawler actualizó una partición tras un cambio en el origen). Hago que las particiones hereden el esquema de la tabla (ajuste del crawler "update all new and existing partitions with metadata from the table"), corrijo o reescribo las particiones raras y estabilizo el esquema del origen.

<!-- challenge -->

Una tabla con 300.000 particiones tarda 40 segundos en planificarse en Athena, incluso para un día. ¿Qué agregas?

<!-- solution -->

Un índice de particiones sobre la clave de fecha, para que `GetPartitions` filtre en el servidor, o pasar la tabla a partition projection. Revisa también si la granularidad es más fina de lo que necesitan las consultas.

<!-- takeaways -->

- Las particiones son entradas del catálogo con su propio esquema.
- Esquemas de partición desalineados rompen consultas.
- Índices de particiones y estadísticas aceleran la planificación.

<!-- unit: Formatos, connections y esquemas -->

<!-- goals -->

- Conocer los formatos de tabla y connections que admite el catálogo.
- Versionar esquemas de tablas y de streams.

<!-- concept -->

El catálogo describe más que carpetas. Registra formatos de tabla abiertos como Iceberg, cuyos metadatos rastrean archivos, y puede mantenerlos compactando archivos automáticamente. Guarda connections a bases de datos para que jobs y crawlers no lleven URLs ni credenciales.

Los esquemas cambian, así que el catálogo guarda versiones de tablas, y el Schema Registry versiona esquemas de datos de streaming con reglas de compatibilidad que frenan cambios incompatibles.

<!-- example -->

```python
# connection referencing a secret instead of a password
glue.create_connection(ConnectionInput={
    "Name": "orders_pg", "ConnectionType": "JDBC",
    "ConnectionProperties": {"JDBC_CONNECTION_URL": "jdbc:postgresql://db:5432/shop",
                             "SECRET_ID": "prod/orders_pg"}})
```

#### ¿Qué formatos de tabla admite el Data Catalog?

Tablas al estilo Hive en Parquet, ORC, Avro, JSON, CSV y otros formatos, y los formatos de tabla abiertos Apache Iceberg, Apache Hudi y Delta Lake. Iceberg es el más integrado en los servicios de AWS.

#### ¿Qué son las optimizaciones del catálogo para tablas Iceberg?

Mantenimiento administrado de las tablas Iceberg del Data Catalog: compactación automática de archivos pequeños, retención de snapshots (expiración de los antiguos) y borrado de archivos huérfanos, configurado por tabla y ejecutado por Glue sin jobs propios.

#### ¿Qué es una conexión de Glue?

Un objeto del catálogo que guarda las propiedades de conexión a un almacén de datos: URL JDBC, credenciales (preferiblemente un secreto de Secrets Manager), VPC, subred y grupos de seguridad, o propiedades para Kafka, MongoDB, Snowflake, BigQuery y otros conectores nativos. Los jobs y crawlers la referencian.

#### ¿Qué es el Glue Schema Registry?

Un servicio para guardar, versionar y validar esquemas (Avro, JSON Schema, Protobuf) de datos en streaming, con reglas de compatibilidad (backward, forward, full). Los productores y consumidores que usan Kafka, MSK, Kinesis o Lambda serializan y validan los registros con los esquemas registrados.

#### ¿Cómo se versionan los esquemas de las tablas en el Data Catalog?

El catálogo guarda versiones de una tabla automáticamente cuando se actualiza (hasta un límite), así que puedes ver y comparar esquemas anteriores con `GetTableVersions`. Las tablas Iceberg también guardan el historial del esquema en sus propios metadatos.

<!-- challenge -->

Un productor de Kafka cambió un campo de `int` a `string` y rompió tres consumidores. ¿Qué función de Glue lo habría evitado?

<!-- solution -->

El Glue Schema Registry con un modo de compatibilidad como `BACKWARD`: el serializador del productor habría rechazado la versión incompatible antes de enviar un solo mensaje.

<!-- takeaways -->

- El catálogo registra tablas estilo Hive y formatos abiertos.
- Las connections sacan URLs y secretos del código.
- Versiones de tabla y Schema Registry siguen los cambios de esquema.

<!-- unit: Compartir y administrar el catálogo -->

<!-- goals -->

- Compartir catálogos entre cuentas y consultarlos de forma programática.
- Mantener limpio un catálogo y entender su costo.

<!-- concept -->

En entornos con varias cuentas, un catálogo suele servir a muchos equipos. Se comparte con Lake Formation y resource links, que hacen ver locales las tablas remotas sin copiar metadatos, y cada llamada a la API puede indicar el catálogo destino.

Un catálogo compartido necesita orden: convenciones de nombres por capa, tablas definidas como código y eliminación de las tablas que dejaron crawlers o experimentos. El problema rara vez es la factura; es la confusión.

<!-- example -->

```python
paginator = boto3.client("glue").get_paginator("get_tables")
for page in paginator.paginate(CatalogId="111122223333", DatabaseName="curated"):
    for t in page["TableList"]:
        print(t["Name"], t["StorageDescriptor"]["Location"])
```

#### ¿Pueden varias cuentas de AWS compartir un Data Catalog?

Sí. El acceso se puede conceder entre cuentas con políticas de recursos sobre el catálogo o, más a menudo, con permisos entre cuentas de Lake Formation (muchas veces mediante AWS RAM), de modo que una cuenta central de gobierno comparte bases de datos y tablas con las cuentas consumidoras.

#### ¿Qué es el catalog ID?

El ID de la cuenta de AWS dueña de un Data Catalog. Las APIs y las consultas pueden referenciar el catálogo de otra cuenta por su ID cuando se concedió acceso entre cuentas.

#### ¿Qué es un resource link?

Un objeto de Lake Formation que apunta a una base de datos o tabla compartida desde otra cuenta o región, para que los usuarios la consulten como si fuera local en su propio catálogo.

#### ¿Cómo se consulta el Data Catalog de forma programática?

Con la API de Glue (`GetDatabases`, `GetTables`, `GetPartitions`, `SearchTables`) mediante boto3 o la CLI, o con SQL a través de las vistas `information_schema` de Athena.

#### ¿Cómo se factura el Data Catalog?

El primer millón de objetos guardados y el primer millón de solicitudes al mes son gratis; después se paga por cada 100.000 objetos y por millón de solicitudes. El cálculo de estadísticas y las optimizaciones de Iceberg se facturan aparte en DPU-hora.

#### ¿Cómo se mantiene ordenado un Data Catalog?

Definiendo convenciones de nombres por capa (`raw_`, `curated_`), administrando las tablas como código, eliminando las tablas creadas por crawls accidentales, documentando tablas y columnas con descripciones, aplicando LF-Tags para clasificar y vigilando las tablas sin uso.

<!-- challenge -->

La base `raw` tiene 2.000 tablas, la mitad creadas por crawlers sobre carpetas de prueba. Los analistas no encuentran nada. ¿Qué haces?

<!-- solution -->

Inventariar las tablas con la API (ubicación, última actualización), borrar las que apuntan a pruebas o a ubicaciones inexistentes, acotar los crawlers, adoptar convenciones por capa y gestionar las tablas curadas como código con descripciones.

<!-- takeaways -->

- Comparte catálogos con Lake Formation y resource links.
- El catalog ID permite a las APIs apuntar a otras cuentas.
- Un catálogo limpio necesita convenciones y responsables.

### Crawlers

<!-- unit: Cómo funcionan los crawlers -->

<!-- goals -->

- Explicar cómo los crawlers infieren esquemas y agrupan archivos en tablas.
- Saber qué pueden leer los crawlers, de CSV a JDBC e Iceberg.

<!-- concept -->

Un crawler mira una muestra de los datos y adivina. Los clasificadores reconocen formato y esquema, la estructura de carpetas sugiere tablas y particiones, y el resultado se escribe en el catálogo. Adivinar bien requiere datos consistentes: mismo formato, mismas columnas, carpetas predecibles.

Los formatos de texto son donde más se falla, porque tipos y encabezados se infieren de los valores. Las fuentes autodescriptivas (Parquet, Iceberg, esquemas de bases) dan resultados mucho más confiables.

<!-- example -->

```text
s3://landing/orders/dt=2026-10-16/part-0.csv   ┐
s3://landing/orders/dt=2026-10-17/part-0.csv   ┘─► table "orders", partition key "dt"
s3://landing/orders/backup_old/orders.json      ─► a second table: different format
```

#### ¿Qué es un crawler?

Un componente de Glue que se conecta a un almacén de datos (S3, bases JDBC, DynamoDB, MongoDB, Delta, Iceberg, Hudi), toma muestras de los datos, infiere esquemas y particiones con clasificadores, y crea o actualiza tablas en el Data Catalog. Puede ejecutarse bajo demanda o de forma programada.

#### ¿Qué es un clasificador?

La lógica que reconoce un formato de datos y su esquema. Glue trae clasificadores integrados (CSV, JSON, Parquet, Avro, ORC, XML, logs y más), y puedes añadir clasificadores propios con patrones grok, etiquetas XML, rutas JSON o ajustes de CSV.

#### ¿Cómo decide un crawler cuántas tablas crear?

Agrupa en una tabla los archivos con esquemas compatibles bajo un prefijo común, usando la estructura de carpetas para detectar particiones. Si los esquemas difieren demasiado, crea varias tablas. La opción "create a single schema for each S3 path" fuerza una tabla por ruta incluida.

#### ¿Cómo infieren los crawlers los tipos en archivos CSV?

Tomando una muestra de las primeras filas y eligiendo tipos que encajen; si una columna tiene valores mezclados (números con algunos vacíos o textos), el crawler puede elegir `string`, o un tipo que las filas siguientes rompen. Define las tablas CSV de forma explícita para tener tipos predecibles.

#### ¿Cómo manejan los crawlers los encabezados de CSV?

El clasificador CSV integrado adivina si la primera fila es un encabezado comprobando si se ve distinta de las filas de datos. Cuando falla, un clasificador CSV propio con el encabezado explícito lo resuelve.

#### ¿Pueden los crawlers crear tablas Iceberg o Delta?

Sí. Los crawlers pueden registrar tablas Delta Lake, Iceberg y Hudi existentes en S3 leyendo sus metadatos y crear tablas del catálogo que apuntan al formato de tabla (de forma nativa o mediante manifiestos, según la configuración).

#### ¿Puede un crawler recorrer una base de datos JDBC?

Sí. Con una conexión de Glue lee las definiciones de las tablas de bases como MySQL, PostgreSQL, Oracle y SQL Server con una ruta de inclusión como `mydb/%`, y crea tablas en el catálogo que los jobs pueden leer.

<!-- challenge -->

Un crawler tipó una columna `zip_code` como `bigint` y se perdieron los ceros iniciales. ¿Cómo lo arreglas para siempre?

<!-- solution -->

Fija tú el esquema: define la tabla como código con `zip_code` como `string` y configura el crawler para no actualizar esquemas (o deja de usarlo para esa tabla). Un clasificador personalizado con tipos explícitos es otra opción.

<!-- takeaways -->

- Los crawlers infieren esquemas por muestreo; los datos consistentes ayudan.
- Los formatos de texto dan las peores inferencias.
- Los formatos autodescriptivos se rastrean con fiabilidad.

<!-- unit: Configurar crawlers -->

<!-- goals -->

- Configurar el cambio de esquema, el re-rastreo y el alcance.
- Hacer incrementales los rastreos y dirigirlos por eventos.

<!-- concept -->

Un crawler que vuelve a escanear todo y reescribe esquemas en cada ejecución es lento, caro y riesgoso. Su configuración controla tres cosas: qué mira (rutas, exclusiones, nivel de tabla, tamaño de muestra), cada cuánto relee carpetas viejas (recrawl policy, eventos de S3) y qué puede cambiar (schema change policy).

La configuración más segura lee solo datos nuevos y registra los cambios de esquema en vez de aplicarlos.

<!-- example -->

```json
{
  "Targets": {"S3Targets": [{"Path": "s3://landing/orders/", "Exclusions": ["**/_temporary/**", "**.crc"]}]},
  "RecrawlPolicy": {"RecrawlBehavior": "CRAWL_NEW_FOLDERS_ONLY"},
  "SchemaChangePolicy": {"UpdateBehavior": "LOG", "DeleteBehavior": "LOG"},
  "Configuration": "{\"Version\":1.0,\"Grouping\":{\"TableLevelConfiguration\":3}}"
}
```

#### ¿Qué es la política de cambios de esquema de un crawler?

Los ajustes de qué hacer cuando cambia el esquema o se borran objetos: actualizar la tabla o solo registrar los cambios, y borrar, marcar como obsoletas o ignorar las tablas y particiones eliminadas. Los equipos de producción suelen registrar los cambios en lugar de actualizar automáticamente, para evitar sorpresas.

#### ¿Qué son los crawls incrementales?

Ejecuciones que solo procesan las carpetas añadidas desde la última (y, con el modo de eventos de S3, solo los objetos modificados según una cola SQS), lo que es mucho más rápido y barato en data lakes grandes y en crecimiento.

#### ¿Qué es el modo de eventos de S3 para crawlers?

Un modo en el que el crawler lee notificaciones de eventos de S3 desde una cola SQS para saber exactamente qué objetos cambiaron, en lugar de listar todo el prefijo.

#### ¿Qué es la "recrawl policy"?

El ajuste que decide si en cada ejecución se recorren de nuevo todas las carpetas o solo las nuevas desde el último crawl (incremental), o si se usan eventos de S3.

#### ¿Qué son los patrones de exclusión?

Patrones glob que le indican a un crawler qué archivos o carpetas saltar, como `**/_temporary/**`, `**.crc` o `**/_SUCCESS`, lo que evita tablas basura y ahorra tiempo.

#### ¿Cómo se limita el alcance de un crawler?

Con rutas de inclusión precisas, patrones de exclusión, un tamaño de muestra por carpeta (en S3), el ajuste de nivel de tabla (a qué profundidad de carpeta se crean las tablas) y crawlers separados por origen.

#### ¿Qué significa "table level" en la configuración del crawler?

La profundidad de carpeta a la que el crawler crea las tablas. Definirla evita que el crawler cree tablas en el nivel equivocado, por ejemplo tratando cada carpeta de partición como una tabla aparte.

<!-- challenge -->

Un crawler sobre un bucket de 5 años corre una hora cada noche para encontrar una carpeta nueva. ¿Qué cambias?

<!-- solution -->

Poner la recrawl policy en solo carpetas nuevas, o pasar a S3 event mode con una cola SQS para leer solo objetos cambiados. Mejor aún, registrar la partición diaria desde el job de carga y prescindir del crawler.

<!-- takeaways -->

- La configuración de alcance controla qué lee el crawler.
- Los modos incremental y por eventos evitan re-escaneos completos.
- Registra los cambios de esquema en vez de aplicarlos a ciegas.

<!-- unit: Cuándo usar crawlers -->

<!-- goals -->

- Reconocer los problemas comunes de los crawlers y sus causas.
- Decidir cuándo usar crawlers y cuándo definir las tablas tú.

<!-- concept -->

Los crawlers son una herramienta de descubrimiento. Brillan con datos que no controlas y quieres explorar rápido. En pipelines propios ya conoces esquema y particiones, así que dejar que un crawler los adivine agrega costo, demora y el riesgo de que una mala inferencia cambie tablas de producción.

La mayoría de problemas con crawlers vienen de entradas inconsistentes: formatos o esquemas mezclados bajo un prefijo, archivos sueltos o profundidad de carpetas inesperada.

<!-- example -->

| Situación | Uso |
|---|---|
| Explorar el bucket S3 de un proveedor | Crawler |
| Tu job de Glue escribe particiones diarias | El job actualiza el catálogo |
| Tabla Iceberg escrita por Spark | Catálogo vía el escritor, sin crawler |

#### ¿Cuáles son los problemas comunes de los crawlers?

Demasiadas tablas creadas por esquemas o estructuras de carpetas incoherentes, tipos mal inferidos a partir de muestras de CSV, errores `HIVE_PARTITION_SCHEMA_MISMATCH` cuando las particiones tienen esquemas distintos, costo y tiempo sobre prefijos enormes, y cambios de esquema silenciosos que rompen las consultas posteriores.

#### ¿Hay que usar siempre crawlers?

No. Los crawlers son prácticos para descubrir datos y para orígenes que no controlas. En los pipelines propios, definir las tablas de forma explícita (infraestructura como código) y registrar las particiones desde los jobs, o usar proyección de particiones, da esquemas predecibles y ningún costo de crawler.

#### ¿Cómo se facturan los crawlers?

Por DPU-hora durante el tiempo que corren, por segundo con una duración mínima por ejecución. Recorrer millones de archivos pequeños puede salir caro; usa patrones de inclusión y exclusión, muestreo y crawls incrementales.

#### Un crawler crea docenas de tablas en lugar de una. ¿Qué pasa?

Los archivos bajo el prefijo tienen esquemas o estructuras de carpetas incoherentes (columnas extra, formatos distintos, archivos sueltos). Corrijo la organización del origen, añado patrones de exclusión, uso "create a single schema for each S3 path" o defino la tabla de forma explícita en lugar de usar el crawler.

<!-- challenge -->

Tu job de Glue escribe Parquet en S3 y un crawler corre después para actualizar la tabla. A veces las consultas fallan tras un cambio de tipo del crawler. ¿Qué propones?

<!-- solution -->

Sacar el crawler del pipeline: que el job escriba con actualización del catálogo activada (o llame a `BatchCreatePartition`) sobre una tabla definida como código. Los cambios de esquema pasan a ser deliberados, mediante revisión de código.

<!-- takeaways -->

- Los crawlers son para descubrir, no para pipelines propios.
- Las entradas inconsistentes crean demasiadas tablas.
- Que los jobs registren su propia salida.

<!-- stage: Construir jobs -->

### Jobs ETL de Glue

<!-- unit: Anatomía de un job de Glue -->

<!-- goals -->

- Leer y escribir la estructura de un job PySpark de Glue.
- Seguir una ejecución por sus estados, IDs y logs.

<!-- concept -->

Un job Spark de Glue es una aplicación Spark con una capa fina de Glue alrededor. El contexto de Glue agrega lectores y escritores que conocen el catálogo; el objeto job guarda estado entre ejecuciones, en lo que se apoyan los bookmarks. Todo lo demás es PySpark corriente.

Cada ejecución recibe un ID y pasa por estados que puedes vigilar y a los que puedes reaccionar. Logs y métricas llegan a CloudWatch, organizados por ejecución.

<!-- example -->

```python
import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

args = getResolvedOptions(sys.argv, ["JOB_NAME", "process_date"])
glue = GlueContext(SparkContext.getOrCreate())
job = Job(glue); job.init(args["JOB_NAME"], args)
df = glue.spark_session.read.parquet(f"s3://lake/raw/orders/dt={args['process_date']}/")
df.write.mode("overwrite").parquet(f"s3://lake/curated/orders/dt={args['process_date']}/")
job.commit()
```

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

#### ¿Cuáles son los estados de ejecución de un job?

`STARTING`, `RUNNING`, `STOPPING`, `STOPPED`, `SUCCEEDED`, `FAILED`, `TIMEOUT`, `ERROR` y `WAITING`. EventBridge recibe los eventos de cambio de estado para alertas y orquestación.

#### ¿Para qué sirve el ID de ejecución de un job de Glue?

Identifica una ejecución para el monitoreo, los logs, el retroceso de bookmarks y los reintentos, y se puede pasar a las salidas (por ejemplo como columna) para el linaje.

#### ¿Qué pasa con los logs de un job de Glue?

Los logs del driver y de los executors van a CloudWatch Logs (`/aws-glue/jobs/output` y `/aws-glue/jobs/error`); el logging continuo los envía durante la ejecución. Usa `glue.get_logger()` para mensajes estructurados.

<!-- challenge -->

Un job olvida llamar a `job.commit()`. Los bookmarks están activados. ¿Qué pasa en la siguiente ejecución?

<!-- solution -->

El bookmark nunca avanza, así que cada ejecución reprocesa los mismos datos como si fueran nuevos, lo que puede duplicar datos aguas abajo. Agrega `job.commit()` al final del procesamiento exitoso.

<!-- takeaways -->

- Un job de Glue es Spark más un contexto de Glue y estado del job.
- `job.commit()` guarda el estado del bookmark tras el éxito.
- Los run IDs unen estados, logs y métricas.

<!-- unit: Parámetros, librerías y acceso al catálogo -->

<!-- goals -->

- Pasar argumentos y agregar dependencias de Python o Java a los jobs.
- Usar Spark SQL contra el catálogo de Glue.

<!-- concept -->

El mismo script debe correr para cualquier fecha o entorno, así que todo lo variable entra como argumento del job. Las dependencias llegan igual: paquetes de Python y JARs se nombran en parámetros del job y se instalan al arrancar, lo que mantiene portables los scripts pero suma tiempo de arranque si la instalación es grande.

Activar el catálogo como metastore de Spark permite usar SQL simple sobre las tablas del catálogo, algo que muchos equipos encuentran más claro que las APIs propias de Glue.

<!-- example -->

```text
--process_date                 2026-10-17
--additional-python-modules    pydantic==2.9.2,s3://artifacts/libs/etl_lib-1.4.0-py3-none-any.whl
--extra-jars                   s3://artifacts/jars/postgresql-42.7.4.jar
--enable-glue-datacatalog      true
```

#### ¿Cómo se pasan parámetros a un job de Glue?

Como argumentos del job (`--target_path s3://...`) definidos en el job o sobrescritos al iniciar la ejecución, leídos con `getResolvedOptions`. Algunos argumentos especiales configuran el propio Glue, como `--job-bookmark-option`, `--enable-metrics`, `--additional-python-modules` o `--conf`.

#### ¿Cómo se añaden librerías Python a un job de Glue?

Con `--additional-python-modules` (instala desde PyPI o wheels en S3 al arrancar), `--extra-py-files` (archivos zip o py en S3) o empaquetando las dependencias en un wheel. Para jobs sin acceso a internet, aloja los wheels en S3 o usa un repositorio privado mediante un endpoint de VPC.

#### ¿Cómo se añaden dependencias JAR?

Con `--extra-jars` apuntando a archivos JAR en S3, para drivers JDBC o librerías de Spark que no trae la versión de Glue.

#### ¿Qué hace `--enable-glue-datacatalog`?

Configura Spark en el job para usar el Glue Data Catalog como su Hive metastore, de modo que `spark.sql("SELECT * FROM raw.orders")` y `saveAsTable` funcionen sobre las tablas del catálogo.

#### ¿Cómo se usa Spark SQL dentro de un job de Glue?

Convirtiendo a DataFrame, registrando una vista temporal y ejecutando `spark.sql()`. Con el Data Catalog activado como Hive metastore (`--enable-glue-datacatalog`), puedes consultar directamente las tablas del catálogo por `base.tabla`.

<!-- challenge -->

Un job instala 15 paquetes de PyPI al arrancar y a veces falla cuando PyPI va lento. ¿Cómo lo haces confiable?

<!-- solution -->

Construir en el CI un wheel (o un conjunto de wheels) con versiones fijas, guardarlo en S3 y referenciarlo en `--additional-python-modules`. El arranque deja de depender de PyPI y las versiones quedan fijas.

<!-- takeaways -->

- Los argumentos hacen que un script sirva para cada ejecución.
- Las dependencias llegan por parámetros al arrancar.
- El catálogo puede ser el metastore de Spark.

<!-- unit: Opciones de ejecución -->

<!-- goals -->

- Elegir entre Spark, Python shell, Flex y auto scaling.
- Fijar timeouts, reintentos y concurrencia a propósito.

<!-- concept -->

No todo job necesita un cluster Spark, ni todo job Spark necesita arrancar de inmediato. Los jobs Python shell resuelven tareas livianas a bajo costo; Flex corre Spark no urgente en capacidad sobrante con descuento; auto scaling dimensiona el cluster por etapa.

Los valores por defecto son riesgosos. Un timeout de 48 horas deja que un job colgado queme dinero dos días, y los reintentos de un job no idempotente duplican datos. Fija ambos a propósito, junto con cuántas ejecuciones pueden solaparse.

<!-- example -->

```python
glue.create_job(Name="orders_daily", Role=ROLE, GlueVersion="5.0",
    Command={"Name": "glueetl", "ScriptLocation": "s3://artifacts/jobs/orders_daily.py"},
    WorkerType="G.1X", NumberOfWorkers=10, ExecutionClass="FLEX",
    Timeout=60, MaxRetries=1, ExecutionProperty={"MaxConcurrentRuns": 1},
    DefaultArguments={"--enable-auto-scaling": "true", "--TempDir": "s3://glue-temp/orders/"})
```

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

#### ¿Para qué sirve el directorio temporal (`--TempDir`)?

Una ubicación de S3 donde Glue escribe datos intermedios, por ejemplo al cargar en Redshift o para el shuffle en algunas configuraciones. Debe tener una regla de ciclo de vida que borre los archivos viejos.

<!-- challenge -->

Un job de reporte nocturno solo debe terminar antes de las 08:00 y dura 30 minutos. ¿Cómo bajas su costo sin cambiar código?

<!-- solution -->

Correrlo con la clase de ejecución Flex, que usa capacidad sobrante a menor precio; el arranque posiblemente más lento no importa con ese plazo. Fija además un timeout razonable y activa auto scaling.

<!-- takeaways -->

- Python shell para tareas livianas; Flex para Spark no urgente.
- Nunca dejes el timeout por defecto de 48 horas.
- Reintenta solo jobs idempotentes; limita las ejecuciones concurrentes.

<!-- unit: Desarrollar jobs -->

<!-- goals -->

- Desarrollar jobs de Glue de forma interactiva y local.
- Elegir entre el editor visual y los scripts.

<!-- concept -->

Esperar un minuto por cada prueba mata la productividad. Las sesiones interactivas te dan una sesión Spark en un notebook o IDE, facturada solo mientras está abierta; las imágenes Docker de Glue te dejan correr jobs y pruebas en tu laptop con las mismas librerías.

El editor visual acelera jobs simples y ayuda a quienes no programan, pero la lógica compleja, la reutilización y las pruebas son más fáciles en scripts guardados en Git.

<!-- example -->

```bash
docker run -it -v ~/.aws:/home/hadoop/.aws -v $PWD:/home/hadoop/workspace \
  public.ecr.aws/glue/aws-glue-libs:5 \
  spark-submit workspace/jobs/orders_daily.py --JOB_NAME local --process_date 2026-10-17
```

#### ¿Qué son las sesiones interactivas de Glue?

Sesiones Spark bajo demanda que usas desde notebooks Jupyter, los notebooks de Glue Studio o tu IDE para desarrollar y depurar código de Glue de forma interactiva, facturadas por segundo con un timeout de inactividad.

#### ¿Cómo se desarrollan jobs de Glue en local?

Con las imágenes Docker oficiales de Glue (que traen las librerías de Glue y el Spark de una versión dada), ejecutando scripts y pytest en local, o con sesiones interactivas desde un notebook local. La lógica PySpark pura también se puede probar con una SparkSession local.

#### ¿Qué diferencia hay entre el editor de scripts de Spark y el editor visual?

El editor visual arma los jobs como un grafo de nodos y genera el código; es rápido para el ETL estándar y accesible para analistas. El editor de scripts da control total sobre el código PySpark o Scala. Muchos equipos empiezan en visual y luego pasan al código administrado en Git.

<!-- challenge -->

Un equipo construye todos los jobs en el editor visual y ahora tiene 40 jobs con lógica copiada. ¿Qué propones?

<!-- solution -->

Mover la lógica compartida a un paquete de Python con pruebas, escribir los jobs nuevos como scripts que lo importan y dejar el editor visual para prototipos. Guardar scripts y definiciones en Git y desplegarlos como código.

<!-- takeaways -->

- Las sesiones interactivas dan retroalimentación rápida en notebooks.
- Las imágenes Docker de Glue corren jobs y pruebas en local.
- Los scripts en Git escalan mejor que los jobs visuales.

<!-- unit: Fuentes y destinos -->

<!-- goals -->

- Leer bases de datos en paralelo y escribir en warehouses y formatos de tabla.
- Manejar JSON anidado y registros malos al leer.

<!-- concept -->

La mayoría de problemas de los jobs empiezan en los bordes. Una lectura de base sin particionar corre en un solo executor sin importar cuántos workers pagues. Una escritura a un warehouse pasa por staging en S3 y necesita permisos en ambos lados. Los formatos de tabla abiertos deben activarse explícitamente.

Los archivos traen sus propios problemas: estructuras anidadas que aplanar y registros malformados que poner en cuarentena en vez de dejar que fallen el job o desaparezcan.

<!-- example -->

```python
df = (spark.read.format("jdbc")
      .option("url", url).option("dbtable", "public.orders")
      .option("partitionColumn", "order_id").option("lowerBound", 1)
      .option("upperBound", 50_000_000).option("numPartitions", 16)
      .load())                               # 16 parallel reads instead of 1
```

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

#### ¿Cómo se lee DynamoDB en Glue?

Con el conector de DynamoDB: directamente (consume capacidad de lectura, controlada con `dynamodb.throughput.read.percent`) o mediante la exportación de DynamoDB a S3 (`dynamodb.export`), que no consume capacidad de la tabla y es preferible para tablas grandes.

#### ¿Cómo se conectan los jobs de Glue a Snowflake, BigQuery u otros orígenes fuera de AWS?

Con los conectores nativos de Glue para muchos orígenes (Snowflake, BigQuery, Teradata, SAP HANA, MongoDB y aplicaciones SaaS), con conectores del AWS Marketplace o por JDBC con un driver propio y una conexión de Glue.

#### ¿Cómo se lee JSON con estructuras anidadas en Glue?

Leyéndolo como DynamicFrame o DataFrame (con esquema inferido o declarado) y aplanándolo con `select` de los campos anidados, `explode` para los arreglos, o `Relationalize` de Glue para una salida totalmente relacional.

#### ¿Cómo se manejan los registros defectuosos al leer archivos?

En los lectores de Spark, con `mode` (`PERMISSIVE` con una columna de registros corruptos, `DROPMALFORMED`, `FAILFAST`) o `badRecordsPath` donde se admite; en los DynamicFrames, los errores se capturan por registro y se pueden revisar con `errorsAsDynamicFrame()`, con umbrales definidos por `stageThreshold` y `totalThreshold`.

<!-- challenge -->

Un job que lee una tabla PostgreSQL de 200 GB usa 20 workers pero tarda 3 horas, y solo un executor trabaja. ¿Qué está mal?

<!-- solution -->

La lectura JDBC no está particionada, así que una sola conexión lo lee todo. Agrega `partitionColumn`, límites y `numPartitions` (o `hashfield`/`hashpartitions` en DynamicFrames) sobre una columna numérica indexada, dentro de lo que aguante la base.

<!-- takeaways -->

- Particiona las lecturas JDBC o correrán en un solo executor.
- Activa los formatos de tabla con `--datalake-formats`.
- Pon en cuarentena los registros malos en vez de perderlos.

### DynamicFrames y transformaciones

<!-- unit: DynamicFrames y DataFrames -->

<!-- goals -->

- Explicar qué agregan los DynamicFrames y cuándo pasar a DataFrames.
- Escribir DynamicFrames actualizando el catálogo y con bookmarks.

<!-- concept -->

Los DynamicFrames se hicieron para fuentes desordenadas: cada registro lleva su propio esquema, así que los tipos inconsistentes no detienen la lectura. Los DataFrames asumen un esquema y a cambio obtienen todo el optimizador de Spark. La mayoría de jobs usa ambos: DynamicFrames en los bordes, donde importan catálogo y bookmarks, y DataFrames para la lógica de transformación en medio.

Los nombres `transformation_ctx` conectan cada paso con el estado del bookmark, así que deben ser estables y únicos.

<!-- example -->

```python
dyf = glue.create_dynamic_frame.from_catalog(database="raw", table_name="orders",
                                             transformation_ctx="src_orders")
df = dyf.toDF().where("status = 'paid'")            # DataFrame logic
out = DynamicFrame.fromDF(df, glue, "out_orders")
sink = glue.getSink(connection_type="s3", path="s3://lake/curated/orders/",
                    enableUpdateCatalog=True, partitionKeys=["dt"])
sink.setFormat("glueparquet"); sink.setCatalogInfo("curated", "orders"); sink.writeFrame(out)
```

#### ¿Qué es un DynamicFrame?

La estructura de datos distribuida de Glue, parecida a un DataFrame de Spark pero en la que cada registro se describe a sí mismo, así que no necesita un esquema fijo de antemano. Maneja datos inconsistentes y desordenados (un campo que a veces es texto y a veces entero) con tipos "choice".

#### ¿Qué diferencia hay entre un DynamicFrame y un DataFrame?

Un DataFrame tiene un esquema para todo el conjunto y todo el optimizador y la API de Spark SQL. Un DynamicFrame calcula el esquema por registro, admite tipos choice y transformaciones propias de Glue, bookmarks e integración con el catálogo. Se convierte con `toDF()` y `DynamicFrame.fromDF()`, y la mayoría de los equipos usa DataFrames para transformar.

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

<!-- challenge -->

Los bookmarks dejaron de funcionar tras un refactor y cada ejecución vuelve a leerlo todo. Las lecturas parecen iguales. ¿Qué revisas?

<!-- solution -->

Si los valores de `transformation_ctx` cambiaron o se quitaron: el estado del bookmark se guarda por nombre de contexto. Restaura los nombres originales (o reinicia el bookmark a propósito) y verifica que `job.commit()` siga ejecutándose.

<!-- takeaways -->

- Los DynamicFrames toleran esquemas inconsistentes.
- Los DataFrames dan el optimizador y una API más rica.
- Nombres `transformation_ctx` estables mantienen los bookmarks.

<!-- unit: Transformaciones flexibles de esquema -->

<!-- goals -->

- Resolver tipos mixtos y mapear columnas con transformaciones de Glue.
- Aplanar datos anidados y sobrevivir a columnas nuevas en la fuente.

<!-- concept -->

Las fuentes rara vez cumplen sus promesas. Una columna que ayer era numérica hoy trae texto; un campo JSON plano se vuelve anidado; un proveedor agrega columnas sin avisar. Las transformaciones flexibles de Glue manejan esto en el borde: decidir qué hacer con tipos mixtos, mapear y castear columnas explícitamente y aplanar el anidamiento en tablas.

El principio es absorber el cambio en el paso de crudo a limpio y mantener estable y explícito el esquema curado.

<!-- example -->

```python
dyf = dyf.resolveChoice(specs=[("price", "cast:double")])
dyf = ApplyMapping.apply(frame=dyf, mappings=[
    ("id", "string", "order_id", "bigint"),
    ("price", "double", "amount", "decimal(12,2)"),
    ("ts", "string", "created_at", "timestamp")])
```

#### ¿Qué es un tipo choice y cómo funciona `ResolveChoice`?

Cuando una columna tiene valores de tipos distintos, un DynamicFrame guarda un tipo choice (por ejemplo `choice<int,string>`). `ResolveChoice` lo resuelve con `cast:long`, `make_cols` (divide en `col_int` y `col_string`), `make_struct` o `project:string`.

```python
resolved = dyf.resolveChoice(specs=[("amount", "cast:double"), ("id", "cast:long")])
```

#### ¿Qué hace `ApplyMapping`?

Renombra columnas, convierte tipos y selecciona campos en un solo paso, a partir de una lista de tuplas `(origen, tipo_origen, destino, tipo_destino)`, que es como funciona el nodo de mapeo de Glue Studio.

#### ¿Qué hace `Relationalize`?

Aplana JSON anidado en un conjunto de tablas relacionales: las estructuras anidadas pasan a columnas y los arreglos a tablas aparte enlazadas por claves generadas, listas para cargar en una base relacional.

#### ¿Qué hace `Unbox`?

Interpreta una columna de texto que contiene JSON (o CSV) como una estructura, para que los campos anidados sean columnas accesibles.

#### Un sistema de origen añade columnas nuevas sin avisar. ¿Cómo mantienes funcionando el pipeline de Glue?

Leyendo con la evolución del esquema en mente: DynamicFrames o esquemas permisivos en raw, selección explícita de columnas en las salidas curadas, alertas ante columnas nuevas (modo de solo registro del crawler o un control de esquema) y evolución de esquema de Iceberg para añadir columnas de forma intencionada.

<!-- challenge -->

Una fuente envía `amount` como número, pero algunos días como texto con símbolo de moneda. La tabla curada debe seguir siendo `decimal`. ¿Qué haces?

<!-- solution -->

Resolver la elección casteando primero a string, quitar los caracteres no numéricos, castear a decimal con semántica tipo `try_cast` y enviar las filas que sigan fallando a una ubicación de cuarentena con alerta.

<!-- takeaways -->

- Los choice types registran tipos mixtos; `ResolveChoice` decide.
- `ApplyMapping` renombra, castea y selecciona en un paso.
- Absorbe los cambios en crudo a limpio; mantén estable lo curado.

<!-- unit: Transformaciones integradas -->

<!-- goals -->

- Usar transformaciones integradas para filtrar, unir y dividir.
- Deduplicar y agregar columnas de auditoría.

<!-- concept -->

Glue trae transformaciones que reflejan operaciones SQL comunes, sobre todo para el editor visual y jobs solo con DynamicFrames. En código, las operaciones equivalentes de DataFrame suelen ser más claras y rápidas, así que las integradas importan más al leer jobs generados.

Dos hábitos aplican sea cual sea la API: deduplicar por una clave de negocio con una regla clara de qué fila gana, y marcar cada fila con de dónde y cuándo vino.

<!-- example -->

```python
from pyspark.sql import functions as F, Window
w = Window.partitionBy("order_id").orderBy(F.col("updated_at").desc())
clean = (df.withColumn("rn", F.row_number().over(w)).where("rn = 1").drop("rn")
           .withColumn("ingested_at", F.current_timestamp())
           .withColumn("source_file", F.input_file_name()))
```

#### ¿Qué otras transformaciones integradas tiene Glue?

`DropFields`, `SelectFields`, `RenameField`, `Filter`, `Map`, `Join`, `SplitFields`, `SplitRows`, `Unbox` (interpretar cadenas JSON), `DropNullFields`, `FillMissingValues`, `FindMatches` (deduplicación con ML) y, en Glue Studio, transformaciones como `Aggregate`, `Pivot`, `Derived column`, `Identify sensitive data` y `Evaluate data quality`.

#### ¿Cómo se filtra un DynamicFrame?

Con `Filter.apply(frame=dyf, f=lambda row: row["status"] == "paid")` o `dyf.filter(...)`, aunque convertir a DataFrame y usar `filter("status = 'paid'")` suele ser más rápido porque Spark lo puede optimizar.

#### ¿Cómo se unen DynamicFrames?

Con `Join.apply(dyf1, dyf2, "key1", "key2")`, que hace un join por igualdad; para otros tipos de join o condiciones, convierte a DataFrames.

#### ¿Qué hace `SplitFields`?

Divide un DynamicFrame en dos colecciones por columnas, por ejemplo para separar las columnas con datos personales del resto y escribirlas en ubicaciones distintas.

#### ¿Cómo se deduplica en un job de Glue?

Convirtiendo a DataFrame y usando `dropDuplicates(["key"])` o una función de ventana con `row_number()` ordenada por una marca de actualización, quedándose con el registro más reciente por clave.

#### ¿Cómo se añaden columnas de auditoría en un job de Glue?

Añadiendo columnas como `ingested_at` (`current_timestamp()`), `source_file` (`input_file_name()` o los metadatos del archivo), `job_run_id` y `process_date`, para que cada fila se pueda rastrear hasta la ejecución y el archivo que la produjeron.

<!-- challenge -->

Un equipo de abajo pregunta de qué archivo vino cada fila curada, tras un archivo malo que corrompió un reporte. ¿Qué agregas y dónde?

<!-- solution -->

Agregar como columnas `source_file` (de `input_file_name()` o los metadatos del archivo), `ingested_at` y el run ID del job en el paso de crudo a limpio, y llevarlas a las tablas curadas. Así las filas malas se rastrean y se quitan por archivo.

<!-- takeaways -->

- Las integradas reflejan SQL; el código de DataFrame suele ser más claro.
- Deduplica por una clave con una regla explícita de ganador.
- Las columnas de auditoría rastrean los datos hasta su origen.

<!-- unit: Emparejar registros con ML -->

<!-- goals -->

- Explicar qué hace FindMatches y cuándo encaja.
- Entrenarlo y usarlo para deduplicar registros sin clave compartida.

<!-- concept -->

La deduplicación exacta necesita una clave. Cuando los registros describen al mismo cliente de forma distinta entre sistemas (otra ortografía, campos faltantes, nombres invertidos), las reglas no terminan nunca. FindMatches aprende qué significa "el mismo" a partir de ejemplos que etiquetas y luego agrupa los registros en coincidencias.

Su calidad depende de las etiquetas: unos cientos de pares bien elegidos le enseñan más que miles de casos fáciles.

<!-- example -->

```text
1. Create a FindMatches transform on customers (primary key: source_id)
2. Generate a labeling file, mark pairs as match / no match, upload it
3. Check estimated precision/recall; tune toward precision or recall
4. Use the transform in a job: output adds match_id per group
```

#### ¿Qué es FindMatches?

Una transformación de machine learning que identifica registros duplicados o coincidentes que no comparten una clave común (por ejemplo el mismo cliente escrito de formas distintas), entrenada con ejemplos etiquetados.

#### Necesitas deduplicar registros de clientes sin una clave común entre dos sistemas. ¿Qué herramienta de Glue ayuda?

La transformación de ML FindMatches: etiquetas ejemplos de pares que coinciden y que no, entrenas la transformación y la ejecutas en un job para asignar IDs de coincidencia; luego fusionas los registros por ID de coincidencia con reglas de negocio.

<!-- challenge -->

Tras aplicar FindMatches, ventas nota dos clientes distintos fusionados en uno. ¿Qué ajuste cambias y qué más haces?

<!-- solution -->

Ajustar la transformación hacia precisión en vez de recall, para que fusione solo coincidencias seguras. Agregar ejemplos etiquetados de clientes parecidos pero distintos, reentrenar y revisar una muestra de grupos fusionados antes de publicar.

<!-- takeaways -->

- FindMatches aprende a emparejar con pares etiquetados.
- Etiqueta los casos difíciles, no los fáciles.
- Equilibra precisión y recall según el uso.

### Job bookmarks y procesamiento incremental

<!-- unit: Cómo funcionan los job bookmarks -->

<!-- goals -->

- Activar, pausar, reiniciar y rebobinar bookmarks.
- Conocer sus límites con archivos, JDBC e Iceberg.

<!-- concept -->

Los bookmarks permiten que un job recuerde lo que ya procesó. En archivos, el estado se basa en rutas y fechas de modificación; en bases de datos, en columnas clave que eliges. El estado avanza solo cuando una ejecución hace commit con éxito, así los fallos nunca se saltan datos.

Son cómodos pero implícitos: archivos sobrescritos, contextos renombrados o una fuente compartida pueden confundirlos, y no aplican a fuentes Iceberg. Aprende a reiniciarlos antes de necesitarlo.

<!-- example -->

```bash
aws glue start-job-run --job-name orders_daily \
  --arguments '{"--job-bookmark-option": "job-bookmark-enable"}'
aws glue reset-job-bookmark --job-name orders_daily --run-id jr_0a1b2c   # rewind to a run
```

#### ¿Qué son los job bookmarks?

Una función de Glue que guarda estado entre ejecuciones para que cada una procese solo los datos nuevos: en orígenes S3, qué archivos (por fecha de modificación) se procesaron; en orígenes JDBC, los valores más altos de las columnas clave del bookmark.

#### ¿Cómo se activan y controlan los job bookmarks?

Con `--job-bookmark-option`: `job-bookmark-enable`, `job-bookmark-disable` o `job-bookmark-pause` (procesa desde el último bookmark sin actualizarlo). El origen necesita un `transformation_ctx` y el script debe llamar a `job.commit()`.

#### ¿Cómo se reinicia o se retrocede un bookmark?

Con la consola o la API `ResetJobBookmark`, que hace que la siguiente ejecución lo reprocese todo; también se puede retroceder al ID de una ejecución anterior para reprocesar desde ese punto.

#### ¿Qué pasa con los bookmarks si un job falla?

Los bookmarks solo se actualizan con `job.commit()` tras un éxito, así que una ejecución fallida deja el bookmark donde estaba y la siguiente vuelve a procesar los mismos datos. Por eso las escrituras deben ser idempotentes.

#### ¿Pueden dos jobs distintos compartir un bookmark?

No. Los bookmarks son por job (y por `transformation_ctx`). Dos jobs que leen el mismo origen mantienen estados independientes.

#### ¿Cómo funcionan los bookmarks JDBC?

Defines `jobBookmarkKeys` (columnas como un ID creciente o `updated_at`) y un orden; el job lee las filas con valores mayores al último máximo guardado. Las actualizaciones de filas con claves viejas se pierden, así que encaja con tablas de solo inserción o marcas de tiempo monótonas.

#### ¿Cuáles son los límites de los job bookmarks?

Siguen los archivos por fecha de modificación, así que los archivos sobrescritos con el mismo nombre pueden perderse o reprocesarse; los bookmarks JDBC necesitan columnas clave que siempre crecen y no ven las actualizaciones de filas viejas; solo funcionan con ciertos orígenes y formatos; y no hacen idempotentes las escrituras, así que un fallo después de escribir y antes del `commit` reprocesa datos.

#### ¿Funcionan los job bookmarks con tablas Iceberg como origen?

No de la misma forma; para orígenes Iceberg se procesa de forma incremental con las funciones propias de Iceberg, como leer los cambios entre snapshots (lecturas incrementales o vistas de changelog) y guardar el ID del último snapshot procesado.

<!-- challenge -->

Un bug corrompió la salida de las últimas tres ejecuciones. Los bookmarks están activos. ¿Cómo reprocesas solo esas ejecuciones?

<!-- solution -->

Corregir el código, borrar o sobrescribir la salida de esas tres ejecuciones y rebobinar el bookmark a la ejecución anterior a la primera mala con `ResetJobBookmark` y un run ID. La siguiente ejecución reprocesa todo desde ahí.

<!-- takeaways -->

- Los bookmarks rastrean archivos o claves procesados por job.
- Avanzan solo con un commit exitoso.
- Conoce sus límites: archivos sobrescritos, Iceberg, contextos renombrados.

<!-- unit: Incremental sin bookmarks -->

<!-- goals -->

- Procesar rangos de fechas explícitos con predicados.
- Hacer idempotentes los jobs y manejar datos tardíos.

<!-- concept -->

Muchos equipos prefieren incrementos explícitos a los bookmarks: el orquestador pasa una fecha, el job lee esa partición con un pushdown predicate y sobrescribe la salida de esa partición. La ejecución se vuelve una función pura de su argumento, lo que simplifica re-ejecuciones, backfills y datos tardíos.

Los predicados también importan para el rendimiento: empujados al catálogo, evitan que el job liste particiones que nunca leerá.

<!-- example -->

```python
dyf = glue.create_dynamic_frame.from_catalog(
    database="raw", table_name="orders",
    push_down_predicate=f"dt = '{args['process_date']}'",
    additional_options={"catalogPartitionPredicate": f"dt = '{args['process_date']}'"})
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
dyf.toDF().write.mode("overwrite").partitionBy("dt").parquet("s3://lake/curated/orders/")
```

#### ¿Cómo se hace idempotente un job de Glue?

Escribiendo la salida de la partición procesada con sobrescritura (sobrescritura dinámica de particiones) o usando `MERGE` sobre una tabla Iceberg, en lugar de añadir a ciegas; tomando el periodo procesado de un parámetro; y usando los bookmarks como optimización, no como única garantía.

#### ¿Qué es el pushdown predicate en Glue?

Un filtro sobre las columnas de partición que se pasa al leer desde el catálogo (`push_down_predicate="order_date >= '2026-10-01'"`) para que Glue liste y lea solo las particiones que coinciden en lugar de toda la tabla.

#### ¿Qué es `catalogPartitionPredicate`?

Un filtro de particiones del lado del servidor que evalúa el Data Catalog con los índices de partición, lo que reduce el número de particiones que Glue tiene que traer del catálogo en tablas con muchísimas particiones. Se puede combinar con `push_down_predicate`.

#### ¿Cómo procesas solo los datos de ayer sin bookmarks?

Paso la fecha como argumento del job (desde el orquestador), leo con un pushdown predicate sobre la partición de fecha y sobrescribo la partición de salida de esa fecha. Es explícito, reproducible y facilita los backfills.

#### ¿Cómo implementas una corrección de "datos tardíos" en un pipeline diario de Glue?

Procesando una ventana móvil (por ejemplo los últimos tres días) en cada ejecución con sobrescritura de particiones o `MERGE`, para que los registros tardíos actualicen las particiones correctas, y manteniendo la ventana parametrizada para correcciones mayores.

<!-- challenge -->

Un job sobrescribe toda la tabla curada en cada ejecución con solo los datos de hoy y borra la historia. ¿Qué configuración falta?

<!-- solution -->

La sobrescritura dinámica de particiones: fijar `spark.sql.sources.partitionOverwriteMode=dynamic` (y escribir con `partitionBy`) para reemplazar solo las particiones presentes en la salida, o escribir directamente en la ruta de la partición.

<!-- takeaways -->

- Pasa fechas explícitas; lee con pushdown predicates.
- Sobrescribe solo las particiones de cada ejecución.
- Las ventanas móviles absorben los datos tardíos.

### ETL en streaming

<!-- unit: Jobs de streaming de Glue -->

<!-- goals -->

- Describir los jobs de streaming de Glue, sus fuentes y esquemas.
- Elegir entre Glue streaming, Firehose y Flink.

<!-- concept -->

Un job de streaming es un job Spark que nunca termina: lee un stream en micro-lotes y escribe cada lote en algún lado, normalmente S3 o un formato de tabla. Como corre todo el tiempo, pagas cada hora, así que compensa solo cuando la frescura importa de verdad y las transformaciones necesitan Spark.

La entrega simple encaja con Firehose; el procesamiento de eventos complejo y de baja latencia, con Flink. Glue streaming queda en medio.

<!-- example -->

| Necesidad | Opción |
|---|---|
| Entregar eventos a S3 como Parquet, sin lógica | Firehose |
| Unir el stream con datos del lake, escribir Iceberg cada minuto | Glue streaming |
| Ventanas sub-segundo, estado complejo | Managed Service for Apache Flink |

#### ¿Qué son los jobs de streaming de Glue?

Jobs de Spark Structured Streaming de larga duración que leen de Kinesis Data Streams, Amazon MSK o Kafka autoadministrado, transforman los registros en micro-lotes y escriben en S3, formatos de data lake, bases de datos u otros flujos.

#### ¿Qué orígenes puede leer el streaming de Glue?

Amazon Kinesis Data Streams, Amazon MSK, Apache Kafka autoadministrado y (con conectores) otros sistemas de streaming. Las salidas incluyen S3, tablas Iceberg/Hudi/Delta, bases JDBC y otros flujos.

#### ¿Cómo maneja los esquemas un job de streaming de Glue?

Desde una tabla del Data Catalog que describe el flujo, desde el Glue Schema Registry o infiriendo el esquema a partir de los datos. Los registros que no encajan se pueden manejar con tipos choice o enviar a una ruta de errores.

#### ¿Cuándo elegirías el streaming de Glue frente a Kinesis Data Firehose o Managed Service for Apache Flink?

Firehose para una entrega sencilla a S3, Redshift u OpenSearch con poca transformación y sin código. Managed Flink para procesamiento de flujos con estado y baja latencia, con lógica compleja por tiempo del evento. El streaming de Glue cuando el equipo ya usa Spark, necesita ETL en micro-lotes hacia un data lake y quiere compartir código con los jobs batch.

#### ¿Cómo se facturan los jobs de streaming de Glue?

Por DPU-hora mientras corren, que es todo el tiempo; los workers G.025X reducen el costo en flujos de poco volumen. El autoescalado ayuda con tráfico variable.

<!-- challenge -->

Un equipo corre un job de streaming de Glue 24/7 solo para escribir eventos crudos de Kinesis en S3 como Parquet. ¿Qué sugieres?

<!-- solution -->

Usar Kinesis Data Firehose con conversión a Parquet y particionado dinámico: sin código, sin cluster corriendo todo el día y con menor costo. Dejar Glue para transformaciones batch posteriores.

<!-- takeaways -->

- Los jobs de streaming son micro-lotes de Spark siempre encendidos.
- Pagas cada hora que corren.
- Firehose para entrega simple; Flink para lo complejo y de baja latencia.

<!-- unit: Operar streams de forma confiable -->

<!-- goals -->

- Ajustar ventanas y checkpoints para un streaming confiable.
- Manejar archivos pequeños, actualizaciones de código y eventos tardíos.

<!-- concept -->

La confiabilidad en streaming viene del checkpoint: registra qué se leyó y qué estado existe, así un job reiniciado sigue exactamente donde se detuvo. Todo lo demás se deriva de protegerlo. Los cambios de código deben ser compatibles con él, y la salida debe tolerar que un lote se escriba dos veces.

El tamaño de ventana es el principal equilibrio: más corto significa datos más frescos pero más archivos y más pequeños, que luego requieren compactación.

<!-- example -->

```python
glue.forEachBatch(frame=stream_df,
    batch_function=write_batch,
    options={"windowSize": "120 seconds",
             "checkpointLocation": "s3://glue-checkpoints/orders_stream/"})
```

#### ¿Qué es el tamaño de ventana en el streaming de Glue?

El intervalo de cada micro-lote (`windowSize`, por ejemplo 100 segundos) en `forEachBatch`. Las ventanas más grandes reducen los archivos pequeños y la sobrecarga; las más pequeñas reducen la latencia.

#### ¿Dónde guarda su avance un job de streaming?

En una ubicación de checkpoint en S3, que guarda los offsets y el estado para que el job continúe donde se detuvo tras un reinicio o una actualización.

#### ¿Cómo se evitan los archivos pequeños en los jobs de streaming?

Usando ventanas más grandes, escribiendo en tablas Iceberg o Hudi y compactándolas (o apoyándose en la compactación del catálogo para Iceberg), o ejecutando un job de compactación aparte.

#### ¿Cómo se actualiza el código de un job de streaming en marcha?

Se detiene el job y se inicia la versión nueva con la misma ubicación de checkpoint, siempre que los cambios sean compatibles con el estado guardado; los cambios incompatibles necesitan un checkpoint nuevo y un plan para reprocesar u omitir datos.

#### ¿Cómo se manejan los eventos tardíos en el streaming de Glue?

Con ventanas por tiempo del evento y watermarks de Spark Structured Streaming para las agregaciones, o escribiendo los eventos en particiones por fecha del evento y dejando que los jobs posteriores reprocesen las particiones recientes.

<!-- challenge -->

Tras un despliegue, un job de streaming empieza a leer desde el inicio del stream y duplica un día de datos. ¿Qué pasó?

<!-- solution -->

La nueva versión usó otra ubicación de checkpoint (o una vacía), así que no tenía registro del avance. Despliega con la misma ruta de checkpoint y haz idempotente el destino (por ejemplo `MERGE` en Iceberg por ID de evento) para que las relecturas no dupliquen.

<!-- takeaways -->

- El checkpoint guarda el avance; nunca lo pierdas.
- Ventanas más grandes y compactación combaten los archivos pequeños.
- Destinos idempotentes hacen seguras las relecturas.

<!-- stage: Ejecutar en producción -->

### Workers, rendimiento y costos

<!-- unit: Dimensionar workers -->

<!-- goals -->

- Elegir tipos y cantidad de workers para un job.
- Estimar el costo de un job antes de correrlo.

<!-- concept -->

Dimensionar es elegir entre más workers o workers más grandes. Más workers agregan paralelismo, lo que ayuda cuando los datos se reparten parejo. Workers más grandes o con más memoria ayudan cuando las tareas individuales necesitan memoria, como en joins grandes o filas anchas. Auto scaling maneja jobs cuyas etapas necesitan cantidades distintas.

Como el costo es workers por tiempo, un cluster más grande que termina mucho antes puede costar lo mismo o menos.

<!-- example -->

```text
G.1X × 20 workers × 0.5 h = 10 DPU-h  ≈ 4.40 USD
G.2X × 10 workers × 0.3 h =  6 DPU-h  ≈ 2.64 USD   (no spill, faster)
```

#### ¿Qué tipos de worker ofrece Glue?

G.1X (1 DPU: 4 vCPU, 16 GB), G.2X (2 DPU), G.4X (4 DPU), G.8X (8 DPU) y tipos más grandes en las versiones recientes, G.025X (0,25 DPU, para streaming de poco volumen) y los tipos R optimizados para memoria. Los workers más grandes sirven para transformaciones que usan mucha memoria; más workers sirven para el trabajo en paralelo.

#### ¿Cómo se elige el número de workers?

Partiendo del volumen y la complejidad de los datos, activando el autoescalado con un máximo razonable y mirando las métricas del job: si los executors están ociosos, reduce; si los stages derraman o las tareas hacen cola, aumenta o usa workers más grandes. Mide el costo por ejecución.

#### ¿Cuándo conviene usar workers G.2X o más grandes en lugar de más workers G.1X?

Cuando los executors se quedan sin memoria (joins grandes, filas anchas, agregaciones grandes, transformaciones de ML) o derraman mucho. Si las tareas son pequeñas y numerosas, más workers pequeños dan el mismo paralelismo al mismo precio.

#### ¿Qué son los workers de tipo R (optimizados para memoria)?

Tipos de worker con más memoria por CPU, para jobs limitados por la memoria más que por la CPU, como los broadcast joins grandes o el uso de caché.

#### ¿Qué requiere `--enable-auto-scaling`?

Glue 3.0 o posterior, un número máximo de workers y una carga que varíe entre stages. Glue ajusta entonces los executors según las tareas pendientes.

#### ¿Cómo se estima el costo de un job de Glue?

Workers × DPU por worker × duración en horas × precio por DPU-hora. Por ejemplo, 10 workers G.1X durante 15 minutos son 10 × 1 × 0,25 = 2,5 DPU-hora, alrededor de 1,10 USD a 0,44 USD por DPU-hora. Con autoescalado, revisa los DPU-segundos reales en los detalles de la ejecución.

<!-- challenge -->

Los executors de un job con muchos joins mueren por falta de memoria con 40 workers G.1X. Agregar workers no ayudó. ¿Qué pruebas?

<!-- solution -->

Pasar a workers G.2X (o tipo R) para que cada executor tenga más memoria, con menos workers. Revisar también claves con skew y si un lado pequeño puede hacer broadcast, porque una clave caliente falla sin importar la cantidad.

<!-- takeaways -->

- Más workers dan paralelismo; workers más grandes dan memoria.
- Auto scaling encaja con jobs de etapas desiguales.
- El costo es workers × DPU × tiempo; más rápido puede ser más barato.

<!-- unit: Diagnosticar jobs lentos -->

<!-- goals -->

- Usar la Spark UI y las métricas de observabilidad para hallar cuellos de botella.
- Investigar un job que de repente se volvió lento.

<!-- concept -->

Un job de Glue lento es un job Spark lento, así que las herramientas son las mismas: encuentra la etapa más lenta y pregúntate si lee demasiado, mueve demasiado, hace spill o espera una tarea. Glue agrega métricas por job y executor y una Spark UI construida desde los event logs.

Cuando un job se ralentiza de golpe, compara ejecuciones antes de leer código: tamaño de entrada, cantidad de archivos, predicados que ya no aplican y configuración cambiada explican la mayoría de regresiones.

<!-- example -->

```text
--enable-metrics                 true
--enable-observability-metrics   true
--enable-spark-ui                true
--spark-event-logs-path          s3://glue-sparkui/orders_daily/
```

#### ¿Cómo se diagnostica un job de Glue lento?

Activando las métricas del job, las métricas de observabilidad y la Spark UI (event logs en S3), y revisando la duración de los stages, las tareas con skew, el tamaño de los shuffles y el spill, el uso de los executors y el número de archivos de entrada. Job run insights señala la línea que falla y las causas comunes.

#### ¿Qué es la Spark UI de Glue?

Una vista del Spark history server sobre los event logs de una ejecución (activada con `--enable-spark-ui` y una ruta de logs en S3), disponible en la consola de Glue, para analizar stages, tareas, almacenamiento y planes SQL.

#### ¿Qué son las métricas de observabilidad de Glue?

Métricas de CloudWatch a nivel de job, stage y executor (CPU, memoria, disco, shuffle, skew, uso de workers, rendimiento) que ayudan a detectar cuellos de botella y dimensionar los jobs.

#### Un job de Glue que tardaba 10 minutos ahora tarda 2 horas. ¿Cómo lo investigas?

Comparo el volumen y el número de archivos de entrada, compruebo si el pushdown predicate o los bookmarks dejaron de funcionar (reprocesa todo), miro en la Spark UI el skew o el spill, reviso el número de workers y el autoescalado, y busco un join que cambió o un broadcast que se perdió.

<!-- challenge -->

La Spark UI muestra una tarea de 200 en una etapa corriendo 50 minutos mientras las demás tardan 20 segundos. ¿Qué es y qué pruebas?

<!-- solution -->

Skew de datos: una clave concentra casi todas las filas. Revisa la distribución de la clave, apóyate en el manejo de skew de AQE, haz broadcast del lado pequeño si se puede o aplica salting a la clave caliente. Filtrar claves basura como `NULL` suele resolverlo.

<!-- takeaways -->

- Encuentra la etapa más lenta y luego la causa.
- Compara ejecuciones: entrada, archivos, predicados, configuración.
- Una tarea larga en una etapa casi siempre es skew.

<!-- unit: Shuffles, skew y memoria -->

<!-- goals -->

- Usar AQE y la configuración de Spark para reducir problemas de shuffle.
- Corregir errores de disco y memoria causados por shuffles.

<!-- concept -->

Los shuffles mueven datos entre workers para joins y agregaciones, y causan la mayoría de fallos de memoria y disco. Adaptive Query Execution arregla muchos problemas en ejecución, fusionando particiones pequeñas, cambiando a broadcast joins y dividiendo las que tienen skew.

Cuando un shuffle simplemente es más grande que los discos de los workers, o le das más espacio (workers más grandes, shuffle en S3) o lo achicas (filtrar antes, seleccionar menos columnas, pre-agregar).

<!-- example -->

```text
--conf spark.sql.adaptive.enabled=true
--conf spark.sql.shuffle.partitions=400
--write-shuffle-files-to-s3 true
```

#### ¿Cómo ayuda la Adaptive Query Execution de Spark en Glue?

Activada por defecto desde Glue 4.0, fusiona las particiones pequeñas del shuffle, convierte los joins a broadcast cuando un lado es pequeño y divide las particiones con skew, lo que mejora el rendimiento sin ajustes manuales.

#### ¿Cómo se maneja el data skew en un job de Glue?

Igual que en Spark: apoyándose en Adaptive Query Execution (activada en las versiones recientes de Glue), haciendo broadcast de las tablas pequeñas, aislando o aplicando salting a las claves calientes y revisando en la Spark UI las tareas rezagadas.

#### ¿Cómo se pasa configuración de Spark a un job de Glue?

Con el parámetro `--conf` (por ejemplo `--conf spark.sql.shuffle.partitions=400`), teniendo en cuenta que Glue administra algunos ajustes que no se pueden cambiar.

#### ¿Qué es la opción de shuffle en S3 de Glue?

Una opción (`--write-shuffle-files-to-s3`) que escribe los datos del shuffle de Spark en S3 en lugar del disco local, evitando fallos de "no space left on device" en jobs con mucho shuffle, a costa de algo de velocidad.

#### Tu job de Glue falla con "No space left on device". ¿Qué haces?

El job derrama o hace shuffle de más datos de los que caben en el disco local. Uso workers más grandes (más disco por executor), activo la opción de shuffle en S3, reduzco los datos antes de los shuffles (filtrar y seleccionar antes), corrijo el skew y aumento las particiones para que cada tarea maneje menos datos.

<!-- challenge -->

Un job agrega 2 TB pero solo necesita 5 de 80 columnas. Falla con errores de disco. ¿Qué dos cambios van primero?

<!-- solution -->

Seleccionar las 5 columnas y aplicar filtros antes de la agregación, para que el shuffle lleve muchos menos datos. Si aún hace spill, usar workers más grandes o activar el shuffle en S3.

<!-- takeaways -->

- AQE maneja tamaño de particiones, broadcast y skew en ejecución.
- Achica los shuffles primero: filtra y selecciona temprano.
- Workers más grandes o shuffle en S3 dan más espacio.

<!-- unit: Organización de la salida -->

<!-- goals -->

- Escribir archivos y particiones que los motores de abajo lean a bajo costo.
- Resolver los archivos pequeños en la salida de Glue.

<!-- concept -->

La salida de un job de Glue es la entrada de otro. Athena cobra por byte escaneado y planifica por archivo y partición, así que la forma en que escribe un job decide el costo de las consultas durante meses. El objetivo: formatos columnares, particiones sensatas y archivos de unos cientos de megabytes.

Spark tiende a producir un archivo por tarea por partición, así que sin un paso de repartition la salida puede explotar en miles de archivos diminutos.

<!-- example -->

```python
(df.repartition("dt")                       # one task per date → few files per partition
   .write.mode("overwrite")
   .option("compression", "zstd")
   .partitionBy("dt")
   .parquet("s3://lake/curated/events/"))
```

#### ¿Qué es el problema de los archivos pequeños en Glue y cómo se maneja?

Leer muchos archivos pequeños crea muchas tareas y solicitudes a S3 y ralentiza los jobs. Glue puede agrupar archivos al leer (`groupFiles: inPartition`, `groupSize`), y conviene escribir menos archivos y más grandes (repartition antes de escribir, entre 128 MB y 1 GB por archivo) o compactar las tablas Iceberg.

```python
dyf = glue.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://lake/raw/clicks/"], "recurse": True,
                        "groupFiles": "inPartition", "groupSize": "134217728"},
    format="json")
```

#### ¿Cómo se escribe la salida con un número controlado de archivos?

Con repartition o coalesce antes de escribir (`df.repartition(20, "order_date")`), o con `spark.sql.files.maxRecordsPerFile`, para que cada partición tenga unos pocos archivos grandes en lugar de cientos de pequeños.

#### ¿Por qué convertir CSV o JSON en bruto a Parquet?

Parquet es columnar y comprimido: Athena, Redshift Spectrum y Spark leen solo las columnas necesarias, saltan grupos de filas con las estadísticas y escanean muchos menos datos, lo que reduce el tiempo y el costo.

#### ¿Qué hace eficientes a los archivos Parquet para las consultas posteriores?

La organización columnar, la compresión (Snappy o ZSTD), las estadísticas por grupo de filas para saltarlas, tamaños de archivo razonables (cientos de MB) y el orden o particionado por las columnas de filtro habituales.

#### ¿Cómo afecta la estrategia de particionado a Glue y Athena?

Particiona por las columnas usadas en la mayoría de los filtros (normalmente la fecha), con un número moderado de particiones que tengan datos suficientes cada una; demasiado fino (por hora y cliente) crea millones de particiones diminutas y una planificación lenta, demasiado grueso obliga a lecturas grandes.

#### Un job de Glue escribe miles de archivos Parquet diminutos por día. ¿Cómo lo corriges?

Hago repartition por la columna de partición antes de escribir para que cada partición tenga pocos archivos, aumento el tamaño del lote (procesar un día en lugar de cada pocos minutos) y, si uso Iceberg, activo la compactación del catálogo o ejecuto `rewrite_data_files`.

#### Los analistas se quejan de que las consultas de Athena sobre tablas de Glue son caras. ¿Qué cambias en los jobs de Glue?

Escribir Parquet o Iceberg en lugar de CSV/JSON, comprimir, particionar por los filtros habituales, producir menos archivos y más grandes, calcular estadísticas de columnas y quizá crear tablas agregadas para los dashboards frecuentes.

<!-- challenge -->

Un job escribe una tabla particionada por `dt` y `customer_id` que produce 400.000 archivos al día. ¿Qué cambias?

<!-- solution -->

Particionar solo por `dt`, hacer repartition por `dt` antes de escribir para que cada día tenga pocos archivos grandes, y ordenar o hacer bucketing por `customer_id` dentro. Compactar una vez los datos existentes.

<!-- takeaways -->

- La organización de la salida decide el costo de las consultas.
- Haz repartition antes de escribir para controlar los archivos.
- Particiona por filtros comunes, no por claves de alta cardinalidad.

<!-- unit: Costo y arranque -->

<!-- goals -->

- Aplicar las palancas principales para bajar los costos de Glue.
- Reducir el tiempo de arranque de los jobs.

<!-- concept -->

Bajar costos en Glue es sobre todo dejar de pagar por inactividad o desperdicio: usar la versión más nueva, dejar que auto scaling quite workers sobrantes, usar Flex donde el plazo lo permita, procesar incrementos en vez de recargas completas y frenar jobs descontrolados con timeouts.

El arranque importa para jobs pequeños y frecuentes, donde esperar puede superar el trabajo mismo. Las versiones nuevas arrancan más rápido, y las instalaciones pesadas de dependencias frenan cada ejecución.

<!-- example -->

| Palanca | Efecto típico |
|---|---|
| Actualizar a la última versión de Glue | Arranque y ejecución más rápidos |
| Auto scaling | Menos workers ociosos |
| Ejecución Flex | Menor precio para jobs no urgentes |
| Incremental en vez de recarga completa | Menos datos procesados |

#### ¿Cómo se reducen los costos de Glue?

Usando la última versión de Glue (arranque y ejecución más rápidos), activando el autoescalado, usando Flex para los jobs no urgentes, dimensionando bien los workers, definiendo timeouts, procesando de forma incremental con particiones o bookmarks, leyendo solo las particiones y columnas necesarias, evitando los crawlers cuando las tablas se pueden definir en código y apagando los endpoints de desarrollo y las sesiones ociosas.

#### ¿Por qué los jobs de Glue tardan en arrancar y cómo se reduce?

Glue aprovisiona el entorno en cada ejecución. Desde Glue 2.0 el arranque toma de segundos a un minuto; Flex puede tardar más. Se reduce con versiones más nuevas, menos módulos extra instalados al arrancar (wheels preconstruidos) y evitando muchos jobs diminutos que podrían ser uno.

<!-- challenge -->

Un job corre cada 5 minutos por 40 segundos de trabajo y cuesta más de lo esperado. ¿Por qué y qué cambias?

<!-- solution -->

Cada ejecución paga un mínimo y el tiempo de arranque, así que domina el overhead. Agrupar el trabajo en menos ejecuciones (por ejemplo cada 30 minutos), usar un job Python shell si no hace falta Spark, o pasar a un diseño de streaming o Lambda.

<!-- takeaways -->

- Paga por trabajo, no por inactividad: auto scaling, Flex, timeouts.
- Procesa incrementos, no recargas completas.
- Los jobs diminutos y frecuentes desperdician dinero en el arranque.

### Calidad de datos y datos sensibles

<!-- unit: Reglas de Data Quality -->

<!-- goals -->

- Escribir reglas DQDL, incluidas compuestas y referenciales.
- Obtener recomendaciones de reglas a partir de perfiles de datos.

<!-- concept -->

Glue Data Quality convierte expectativas sobre los datos en reglas que puedes correr en cada carga: conteos, completitud, unicidad, valores permitidos, relaciones. Escribirlas en DQDL las mantiene declarativas y revisables, como código.

Empezar de cero es difícil, así que las recomendaciones perfilan una tabla y proponen reglas. Trátalas como borrador: conserva las que expresan expectativas reales del negocio y ajusta los umbrales con el tiempo.

<!-- example -->

```text
Rules = [
  RowCount > 1000,
  IsComplete "order_id", IsUnique "order_id",
  ColumnValues "status" in ["paid", "refunded", "cancelled"],
  (ColumnValues "amount" > 0) or (ColumnValues "status" = "refunded"),
  ReferentialIntegrity "customer_id" "customers.customer_id" = 1.0
]
```

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

#### ¿Qué son las reglas compuestas en DQDL?

Reglas combinadas con `and` y `or`, por ejemplo `(ColumnValues "status" = "paid") and (ColumnValues "amount" > 0)`, para expresar condiciones sobre varias columnas.

#### ¿Cómo se comprueba la integridad referencial en Glue Data Quality?

Con reglas como `ReferentialIntegrity`, que compara una columna con la columna clave de otro dataset, o `DatasetMatch` para comparar dos datasets, pasando el dataset de referencia como origen adicional.

#### ¿Cómo se obtienen recomendaciones de reglas en Glue Data Quality?

Ejecutando una tarea de recomendación sobre una tabla del catálogo: Glue perfila los datos y propone reglas DQDL (completitud, unicidad, rangos de valores, valores permitidos) que revisas y editas antes de usarlas.

<!-- challenge -->

Una recomendación sugiere `ColumnValues "country" in [...]` con los 12 países de hoy. ¿La aceptas tal cual?

<!-- solution -->

No a ciegas: un mercado nuevo haría fallar el job. Confirma la lista con el negocio o reemplázala por un chequeo contra una tabla de referencia, y decide si un valor nuevo debe fallar la carga o solo advertir.

<!-- takeaways -->

- Las reglas DQDL declaran expectativas como código.
- Las reglas compuestas y referenciales expresan lógica de negocio.
- Las recomendaciones son un borrador inicial.

<!-- unit: Actuar sobre la calidad y los datos sensibles -->

<!-- goals -->

- Enrutar, guardar y alertar sobre los resultados de calidad.
- Detectar y manejar datos sensibles en los pipelines.

<!-- concept -->

Una regla que falla en silencio es decoración. Los resultados de calidad necesitan consecuencias: las filas que fallan van a cuarentena, las ejecuciones que fallan dejan de publicar y se avisa a los responsables. La detección de anomalías agrega chequeos que nadie escribió, marcando valores que se alejan de la historia.

Los datos sensibles son un problema cercano: antes de que lleguen a capas curadas, la detección puede encontrar PII y enmascararla, hashearla o quitarla.

<!-- example -->

```python
dq = EvaluateDataQuality().process_rows(frame=orders, ruleset=RULES,
        publishing_options={"dataQualityEvaluationContext": "orders_dq",
                            "enableDataQualityCloudWatchMetrics": True})
rows = SelectFromCollection.apply(dfc=dq, key="rowLevelOutcomes")
passed = rows.filter(lambda r: r["DataQualityEvaluationResult"] == "Passed")
failed = rows.filter(lambda r: r["DataQualityEvaluationResult"] == "Failed")   # → quarantine
```

#### ¿Cómo se actúa sobre los resultados de calidad en un job?

Usando la transformación Evaluate Data Quality y luego enrutando las filas: conservar las que pasan, escribir las que fallan en una ubicación de cuarentena, y hacer fallar el job o enviar una alerta por EventBridge cuando el puntaje total baja de un umbral.

#### ¿Qué es la detección de anomalías de calidad de datos?

Glue aprende estadísticas a lo largo de las ejecuciones (número de filas, valores distintos, distribuciones) y señala valores inusuales incluso sin umbrales explícitos, lo que detecta problemas como una caída repentina del volumen.

#### ¿Cómo recibes alertas de fallos de calidad de datos?

Glue publica los resultados de calidad en EventBridge y CloudWatch; las reglas pueden enviar notificaciones por SNS o lanzar flujos de corrección.

#### ¿Dónde se guardan los resultados de calidad de datos?

En el historial de la consola de Glue, en métricas de CloudWatch, como eventos de EventBridge y, opcionalmente, escritos en S3 por el job, donde se pueden consultar con Athena para ver tendencias.

#### ¿Qué es la detección de datos sensibles en Glue?

Una transformación que busca datos personales como nombres, correos, teléfonos, tarjetas de crédito y documentos de identidad (con detectores por país), y puede ocultar, hashear o informar los hallazgos, lo que ayuda a cumplir el RGPD o leyes similares, como la ley de protección de datos personales de Colombia.

<!-- challenge -->

Un día los conteos diarios cayeron un 60 %, pero ninguna regla falló porque el umbral era `RowCount > 1000`. ¿Qué agregas?

<!-- solution -->

Activar detección de anomalías sobre el conteo (o una regla que compare con el promedio reciente) y alertar por EventBridge a los responsables. Los mínimos estáticos no detectan caídas relativas grandes.

<!-- takeaways -->

- Pon en cuarentena las filas que fallan; frena las publicaciones malas.
- La detección de anomalías atrapa desvíos que las reglas estáticas no ven.
- Detecta y enmascara PII antes de las capas curadas.

### Orquestación

<!-- unit: Triggers y workflows -->

<!-- goals -->

- Construir pipelines con triggers y workflows de Glue.
- Compartir estado en un workflow y reanudar fallos.

<!-- concept -->

Glue tiene su propia orquestación ligera. Los triggers inician jobs y crawlers por calendario, a demanda o cuando otros terminan; los workflows los agrupan en un grafo con una ejecución y propiedades compartidas. Para pipelines que viven por completo en Glue, evita sumar otro servicio.

Los límites aparecen cuando los pipelines crecen: bifurcaciones, reintentos entre servicios y backfills son más fáciles en un orquestador general.

<!-- example -->

```text
workflow orders_daily
  scheduled trigger 05:00 ─► job extract_orders
  conditional trigger (extract SUCCEEDED AND ...) ─► job build_curated
  conditional trigger (build SUCCEEDED) ─► job publish_marts
```

#### ¿Qué son los triggers de Glue?

Objetos que inician jobs y crawlers: programados (cron), condicionales (cuando otros jobs o crawlers llegan a un estado como `SUCCEEDED`), bajo demanda o basados en eventos de EventBridge (por ejemplo lotes de eventos de S3).

#### ¿Qué es un workflow de Glue?

Un contenedor para un grafo de triggers, crawlers y jobs que representa un pipeline ETL, con una vista visual de las ejecuciones, propiedades de ejecución compartidas (parámetros clave-valor) y la posibilidad de retomar desde un paso fallido.

#### ¿Qué es el predicado de un trigger condicional?

La lista de jobs o crawlers y estados que vigila, con lógica `AND` (todas las condiciones) o `ANY` (una condición), por ejemplo "iniciar el job B cuando el job A y el crawler C hayan terminado bien".

#### ¿Qué son las propiedades de ejecución de un workflow?

Pares clave-valor compartidos por todos los jobs de una ejecución del workflow, leídos y actualizados con `get_workflow_run_properties` y `put_workflow_run_properties`, para pasar valores como una fecha de procesamiento entre pasos.

#### ¿Cómo se retoma un workflow fallido?

En la consola o la API de Glue (`ResumeWorkflowRun`), seleccionando los nodos fallidos para volver a ejecutarlos tras corregir el problema; los nodos completados no se vuelven a ejecutar.

<!-- challenge -->

Un workflow falló en su tercer job después de que los dos primeros tardaran dos horas. ¿Cómo continúas sin re-ejecutarlos?

<!-- solution -->

Corregir la causa y reanudar la ejecución del workflow (`ResumeWorkflowRun`) seleccionando el nodo fallido, para que solo corran él y sus nodos posteriores con las mismas propiedades de ejecución.

<!-- takeaways -->

- Los triggers inician jobs por calendario, demanda o condiciones.
- Los workflows agrupan triggers y comparten propiedades de ejecución.
- Reanuda los nodos fallidos en vez de re-ejecutarlo todo.

<!-- unit: Orquestadores externos y eventos -->

<!-- goals -->

- Correr jobs de Glue desde Step Functions, Airflow y EventBridge.
- Pasar fechas de proceso desde el orquestador.

<!-- concept -->

La mayoría de plataformas orquestan más que Glue: Lambda, EMR, Athena, dbt, notificaciones. Un orquestador general inicia los jobs de Glue, los espera y decide qué sigue, mientras el job solo necesita sus argumentos.

Los inicios por eventos completan el cuadro: un archivo que llega a S3 puede iniciar un workflow o job mediante EventBridge, así los pipelines reaccionan a los datos y no a un reloj.

<!-- example -->

```json
{
  "Type": "Task",
  "Resource": "arn:aws:states:::glue:startJobRun.sync",
  "Parameters": {"JobName": "orders_daily",
                 "Arguments": {"--process_date.$": "$.process_date"}},
  "Retry": [{"ErrorEquals": ["Glue.ConcurrentRunsExceededException"], "MaxAttempts": 3}],
  "Next": "PublishMarts"
}
```

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

#### ¿Puede EventBridge iniciar directamente un job de Glue?

EventBridge puede apuntar de forma nativa a workflows de Glue; para un job suelto, el patrón común es EventBridge hacia Step Functions o hacia una Lambda que llama a `StartJobRun`.

#### ¿Cómo se pasa la fecha de procesamiento desde un orquestador a un job de Glue?

Como argumento del job en `StartJobRun` (`--process_date=2026-10-16`), calculado por el orquestador a partir de la fecha lógica de la programación, nunca del reloj del propio job.

<!-- challenge -->

Un pipeline necesita Glue, luego una consulta de Athena, luego una notificación con Lambda, con otro camino si falla. ¿Workflow de Glue o Step Functions?

<!-- solution -->

Step Functions: llama de forma nativa a Glue (`.sync`), Athena y Lambda, con reintentos y ramas catch para el camino de fallo. Los workflows de Glue solo orquestan jobs y crawlers de Glue.

<!-- takeaways -->

- Usa un orquestador general cuando el pipeline cruza servicios.
- Las integraciones `.sync` esperan a que terminen los jobs de Glue.
- Pasa las fechas como argumentos desde el orquestador.

### Seguridad y gobierno

<!-- unit: Identidad de los jobs y acceso de red -->

<!-- goals -->

- Dar a los jobs de Glue roles de mínimo privilegio y credenciales seguras.
- Llegar a bases privadas sin exponer los jobs a internet.

<!-- concept -->

Un job de Glue actúa con los permisos de su rol IAM, así que el rol es la frontera de seguridad. Debe llegar solo a los buckets, claves y secretos que el job necesita. Las credenciales de bases de datos van en Secrets Manager, referenciadas por connections.

El acceso de red es la segunda frontera. Los jobs que leen bases privadas corren dentro de tu VPC mediante una connection, y sin NAT gateway no pueden salir a internet, con endpoints para los servicios de AWS que usan.

<!-- example -->

```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": ["arn:aws:s3:::lake/raw/orders/*", "arn:aws:s3:::lake/curated/orders/*"]
}
```

#### ¿Qué permisos de IAM necesita un job de Glue?

Un job corre con un rol IAM que Glue asume. Necesita los permisos de `AWSGlueServiceRole` (o equivalentes), acceso a las rutas de S3 que lee y escribe, a la ubicación del script, al directorio temporal, a las claves KMS, a los secretos de Secrets Manager de las conexiones y a CloudWatch Logs.

#### ¿Cómo se restringe un job de Glue a prefijos concretos de S3?

Dándole a su rol IAM una política que solo permita los prefijos de bucket y las claves KMS necesarios y, con Lake Formation, concediendo solo las tablas necesarias; evita permisos amplios como `s3:*`.

#### ¿Cómo se evita poner credenciales en el código de los scripts de Glue?

Guardando las credenciales en AWS Secrets Manager y referenciando el secreto en la conexión de Glue, o leyéndolo en el script con boto3; y usando roles IAM para los recursos de AWS.

#### ¿Cómo acceden los jobs de Glue a bases de datos dentro de una VPC?

Mediante una conexión de Glue con VPC, subred y grupos de seguridad: Glue crea interfaces de red elásticas en la subred. La subred necesita rutas hacia la base y, para acceder a S3, un endpoint de gateway de S3 (o un NAT para internet).

#### ¿Cómo se impide que los jobs de Glue salgan a internet?

Ejecutándolos con una conexión de VPC en subredes privadas sin NAT gateway, usando endpoints de VPC para S3, Glue, CloudWatch, KMS y Secrets Manager, y alojando las dependencias Python en S3 o en un repositorio privado.

<!-- challenge -->

Un job de Glue no logra conectarse a una base RDS en una subred privada y da timeout. ¿Qué revisas?

<!-- solution -->

Que el job use una connection de Glue con la VPC, subred y security group correctos; que el security group se permita a sí mismo (auto-referencia) y que la base lo acepte en el puerto; y que la subred tenga endpoints o NAT hacia S3 y Secrets Manager.

<!-- takeaways -->

- El rol del job es la frontera de seguridad; mantenlo estrecho.
- Guarda las credenciales en Secrets Manager.
- Las connections de VPC llegan a bases privadas; sin NAT no hay internet.

<!-- unit: Lake Formation y acceso detallado -->

<!-- goals -->

- Explicar cómo Lake Formation gobierna las tablas del catálogo de Glue.
- Usar LF-Tags y el acceso detallado en jobs Spark.

<!-- concept -->

Las políticas IAM sobre S3 controlan archivos, no tablas. Lake Formation agrega permisos por tabla, columna, fila y celda sobre los objetos del catálogo, y entrega a los motores credenciales temporales para exactamente lo permitido. Los LF-Tags lo hacen escalar: clasificas tablas y columnas una vez y otorgas por tag.

Con versiones recientes de Glue, los jobs Spark aplican los mismos permisos detallados, así el gobierno no se detiene en los motores SQL.

<!-- example -->

```text
LF-Tag classification=pii on columns customers.email, customers.phone
Grant  analysts: SELECT on tables tagged domain=sales, excluding classification=pii
Grant  etl-role: SELECT, INSERT on domain=sales (all columns)
```

#### ¿Cómo funciona Lake Formation con Glue?

Lake Formation añade permisos detallados (a nivel de base de datos, tabla, columna, fila y celda, y control de acceso por etiquetas con LF-Tags) sobre el Data Catalog. Servicios como Athena, Redshift Spectrum, EMR y Glue (5.0+) aplican esos permisos al leer los datos.

#### ¿Qué son las LF-Tags?

Etiquetas de Lake Formation (pares clave-valor como `domain=sales`, `classification=pii`) asociadas a bases de datos, tablas y columnas; los permisos se conceden sobre expresiones de etiquetas, lo que escala mejor que conceder tabla por tabla.

#### ¿Qué es el control de acceso detallado para los jobs Spark de Glue?

Con Glue 5.0 y Lake Formation, los jobs Spark pueden aplicar los permisos a nivel de tabla, columna, fila y celda definidos en Lake Formation, para que el rol del job solo vea los datos permitidos.

<!-- challenge -->

Cada mes se agrega una tabla nueva con correos de clientes y cada vez alguien olvida restringir la columna de correo. ¿Cómo lo haces automático?

<!-- solution -->

Usar LF-Tags: otorgar a los analistas por tag `domain` excluyendo `classification=pii`, y etiquetar las tablas nuevas y columnas PII al crearlas (en la plantilla de tabla como código). Las tablas nuevas heredan el acceso correcto.

<!-- takeaways -->

- Lake Formation gobierna tablas, columnas, filas y celdas.
- Los LF-Tags otorgan por clasificación a escala.
- Los jobs Spark recientes de Glue aplican permisos detallados.

<!-- unit: Cifrado y auditoría -->

<!-- goals -->

- Cifrar salida, logs y bookmarks con security configurations.
- Auditar la actividad de Glue y del catálogo.

<!-- concept -->

Glue escribe en varios lugares además de tu salida: logs, bookmarks, archivos temporales. Una security configuration los cifra todos de forma consistente con tus claves KMS, así el cifrado no depende de que cada desarrollador lo recuerde.

La auditoría responde "quién cambió o leyó qué": CloudTrail registra las llamadas a la API sobre jobs y catálogo, y Lake Formation registra el acceso a datos.

<!-- example -->

```python
glue.create_security_configuration(Name="lake-kms", EncryptionConfiguration={
    "S3Encryption": [{"S3EncryptionMode": "SSE-KMS", "KmsKeyArn": KEY}],
    "CloudWatchEncryption": {"CloudWatchEncryptionMode": "SSE-KMS", "KmsKeyArn": KEY},
    "JobBookmarksEncryption": {"JobBookmarksEncryptionMode": "CSE-KMS", "KmsKeyArn": KEY}})
```

#### ¿Cómo se cifran los datos con Glue?

Con configuraciones de seguridad que activan el cifrado de la salida a S3 (SSE-S3 o SSE-KMS), de CloudWatch Logs y de los job bookmarks; el cifrado del catálogo con KMS; y las contraseñas de las conexiones guardadas en Secrets Manager o cifradas en el catálogo.

#### ¿Qué es una configuración de seguridad de Glue?

Un conjunto con nombre de ajustes de cifrado (modo de cifrado de S3 y clave KMS, cifrado de CloudWatch Logs, cifrado de los job bookmarks) que se asocia a jobs, crawlers y endpoints de desarrollo.

#### ¿Cómo se audita la actividad de Glue?

CloudTrail registra las llamadas a la API de Glue (cambios de jobs y del catálogo), CloudWatch Logs guarda la salida de los jobs, Lake Formation ofrece registros de auditoría del acceso a los datos y AWS Config puede seguir la configuración de los recursos.

<!-- challenge -->

Un auditor pregunta quién cambió el esquema de la tabla `payments` el mes pasado. ¿Dónde buscas?

<!-- solution -->

En los eventos de CloudTrail de `UpdateTable` sobre esa tabla (usuario o rol y hora) y en las versiones de tabla del catálogo para ver qué cambió. Si fue un crawler, sus logs muestran la ejecución.

<!-- takeaways -->

- Las security configurations cifran salida, logs y bookmarks.
- CloudTrail registra los cambios de jobs y catálogo.
- Las versiones de tabla muestran cómo cambió un esquema.

### Operación, CI/CD e integración

<!-- unit: Jobs como código -->

<!-- goals -->

- Estructurar, probar, versionar y desplegar jobs de Glue como código.
- Correr un mismo job en dev, staging y prod.

<!-- concept -->

Un job de Glue es un script más una definición: rol, workers, argumentos. Tratar ambos como código hace reproducibles los entornos: el mismo script corre en todos lados con distintos parámetros, y las herramientas de infraestructura crean los jobs.

Las pruebas siguen el patrón habitual: lógica en funciones que reciben y devuelven DataFrames, probadas en local con pytest, mientras el script del job solo conecta entradas y salidas. Las rutas versionadas de scripts hacen triviales las reversiones.

<!-- example -->

```text
repo/
  jobs/orders_daily.py          # thin entry script
  src/etl_lib/transforms.py     # logic, built as a wheel
  tests/test_transforms.py
  infra/glue_jobs.tf            # job definitions per environment
```

#### ¿Cómo se despliegan los jobs de Glue como código?

Guardando los scripts y las definiciones de los jobs en Git y desplegándolos con CloudFormation, CDK, Terraform o SAM: se suben los scripts a S3 y se crean los jobs, triggers, crawlers, conexiones y tablas del catálogo. Un pipeline de CI ejecuta las pruebas, empaqueta las librerías como wheels y despliega en cada entorno.

#### ¿Cómo se estructura el repositorio de un proyecto de Glue?

Separando los scripts de entrada de los jobs, un paquete Python compartido con la lógica de transformación (construido como wheel), las pruebas, la infraestructura como código (CDK, Terraform o CloudFormation), los conjuntos de reglas de calidad y la configuración por entorno.

#### ¿Cómo se versionan los scripts de Glue?

Guardándolos en Git y desplegando copias versionadas en S3 (por ejemplo con el SHA del commit en la ruta), para que cada definición de job apunte a una versión conocida del script y revertir sea volver a apuntar a la anterior.

#### ¿Cómo se prueba la lógica de los jobs de Glue?

Poniendo la lógica de transformación en funciones que reciben y devuelven DataFrames, probándolas con pytest sobre una SparkSession local o la imagen Docker de Glue, probando el job de extremo a extremo con datos de muestra en una cuenta de desarrollo y añadiendo reglas de calidad de datos para los controles en ejecución.

#### ¿Cómo se actualiza un job de Glue a una versión más nueva?

Cambiando la versión de Glue en una copia de desarrollo, ejecutando las pruebas y comparando salidas y duraciones, revisando las notas de migración (cambios de Spark, Python y librerías), verificando conectores y JAR, y promoviéndolo con CI.

#### ¿Cómo ejecutas el mismo job de Glue en dev, staging y prod?

Un solo script con parámetros para las rutas, las bases de datos y las conexiones, desplegado con infraestructura como código por entorno (idealmente en cuentas separadas), con argumentos de job y roles IAM propios de cada entorno, y promovido con CI tras las pruebas.

<!-- challenge -->

Un desarrollador editó en la consola el script de un job de producción para arreglar un bug. Una semana después, un despliegue sobrescribió el arreglo. ¿Cómo lo evitas?

<!-- solution -->

Hacer de Git y el CI el único camino a producción: desplegar scripts y definiciones como infraestructura como código, quitar permisos de edición en consola en prod y llevar el arreglo al repositorio con una prueba.

<!-- takeaways -->

- Scripts y definiciones de jobs van ambos en Git.
- Un script parametrizado sirve para todos los entornos.
- Prueba la lógica como funciones simples de DataFrame.

<!-- unit: Monitoreo y fallos -->

<!-- goals -->

- Monitorear la salud y duración de los jobs en producción.
- Manejar fallos con reintentos, alertas y re-ejecuciones.

<!-- concept -->

En producción, las señales importantes son simples: ¿falló el job, superó el timeout, tardó mucho más de lo normal? Los eventos de estado van a EventBridge y las métricas a CloudWatch, que juntos cubren alertas y dashboards.

Manejar fallos depende de la idempotencia. Cuando un job puede re-ejecutarse con seguridad, reintentos y re-ejecuciones son rutina; cuando no, cada fallo se vuelve una limpieza manual.

<!-- example -->

```json
{
  "source": ["aws.glue"],
  "detail-type": ["Glue Job State Change"],
  "detail": {"state": ["FAILED", "TIMEOUT", "ERROR"]}
}
```

#### ¿Cómo se monitorean los jobs de Glue en producción?

Con métricas y alarmas de CloudWatch (fallos de jobs, duración, uso de DPU), eventos de EventBridge sobre los cambios de estado enviados a SNS o Slack, job run insights para los errores, y dashboards de duración y costo de los jobs en el tiempo.

#### ¿Cómo se manejan los fallos de los jobs?

Con reintentos para los errores transitorios (solo con jobs idempotentes), alertas sobre los estados `FAILED` y `TIMEOUT`, un procedimiento de reejecución con parámetros para el periodo fallido y rutas de cuarentena o dead-letter para los datos defectuosos.

#### ¿Cómo se generan alertas sobre jobs de Glue que tardan demasiado?

Definiendo el timeout del job, añadiendo una alarma de CloudWatch sobre el tiempo transcurrido o la métrica `glue.driver.aggregate.elapsedTime`, o haciendo que el orquestador alerte cuando un paso supera su duración esperada.

<!-- challenge -->

Un job que suele durar 20 minutos corrió 9 horas antes de que alguien lo notara. ¿Qué dos controles faltaban?

<!-- solution -->

Un timeout realista (por ejemplo 60 minutos) para que falle en vez de seguir, y una alarma sobre el tiempo transcurrido o una regla de EventBridge sobre `TIMEOUT` que avise al responsable.

<!-- takeaways -->

- Los eventos de estado de EventBridge disparan alertas de fallo.
- Fija timeouts y alarma ante duraciones inusuales.
- Los jobs idempotentes hacen seguros reintentos y re-ejecuciones.

<!-- unit: Glue en el ecosistema de AWS -->

<!-- goals -->

- Conectar Glue con Athena, DMS, Redshift y EMR.
- Saber cuándo ayudan zero-ETL, los conectores SaaS o Amazon Q.

<!-- concept -->

Glue rara vez trabaja solo. DMS lleva los cambios de bases de datos a S3, Glue los aplica a las tablas del lake, Athena y Redshift consultan el resultado y EMR lee el mismo catálogo. Las integraciones gestionadas eliminan cada vez más pasos completos: zero-ETL replica fuentes sin jobs y los conectores SaaS extraen de aplicaciones de negocio.

Conocer estas conexiones suele ser la respuesta a "¿construimos un job para esto?".

<!-- example -->

```sql
-- Redshift reading Glue catalog tables directly
CREATE EXTERNAL SCHEMA lake FROM DATA CATALOG
DATABASE 'curated' IAM_ROLE 'arn:aws:iam::123456789012:role/redshift-spectrum';
SELECT count(*) FROM lake.orders WHERE dt = '2026-10-17';
```

#### ¿Cómo trabajan juntos Glue y Athena?

Glue cataloga y transforma los datos; Athena consulta con SQL las tablas del catálogo. Los jobs de Glue suelen convertir los datos en bruto a Parquet o Iceberg particionado para que las consultas de Athena sean rápidas y baratas.

#### ¿Cómo trabajan juntos Glue y AWS DMS?

DMS replica bases de datos (carga completa y CDC) en S3 como archivos con indicadores de operación; luego los jobs de Glue aplican los cambios a las tablas curadas, típicamente con `MERGE` sobre tablas Iceberg o Hudi.

#### ¿Cómo se comparten tablas de Glue con Amazon Redshift?

Creando en Redshift un esquema externo que apunte a una base de Glue (`CREATE EXTERNAL SCHEMA ... FROM DATA CATALOG`) y consultando las tablas con Redshift Spectrum, o usando el acceso al Data Catalog montado automáticamente en Redshift.

#### ¿Cómo usa EMR el Glue Data Catalog?

Los clusters de EMR y EMR Serverless se pueden configurar para usar el Glue Data Catalog como su Hive metastore, de modo que Spark, Hive, Presto y Trino en EMR comparten las mismas definiciones de tablas que Athena y Glue.

#### ¿Qué es zero-ETL en el contexto de Glue?

Integraciones administradas que replican datos desde orígenes (aplicaciones SaaS como Salesforce, SAP o ServiceNow, y bases de datos de AWS como DynamoDB) hacia destinos como tablas de SageMaker Lakehouse o Redshift sin construir pipelines ETL, manteniéndolos sincronizados.

#### ¿Para qué sirven AWS Glue for SAP u otros conectores SaaS?

Para extraer datos de aplicaciones empresariales (SAP OData, Salesforce, ServiceNow, Zendesk y otras) mediante conectores administrados hacia jobs de Glue o integraciones zero-ETL, sin escribir código de APIs.

#### ¿Qué es Amazon Q data integration en Glue?

Un asistente de IA generativa que crea jobs y transformaciones ETL de Glue a partir de descripciones en lenguaje natural y ayuda a diagnosticar jobs; también existe la actualización asistida por IA de scripts Spark a versiones más nuevas de Glue.

<!-- challenge -->

Un equipo planea un job de Glue personalizado para copiar objetos de Salesforce a S3 cada noche. ¿Qué revisarías primero?

<!-- solution -->

Si existe un camino gestionado: el conector de Salesforce de Glue o una integración zero-ETL pueden replicar los objetos sin código de extracción propio, manejando paginación, límites de API y cambios incrementales.

<!-- takeaways -->

- DMS replica; Glue aplica; Athena y Redshift consultan.
- Un solo catálogo sirve a Athena, Redshift y EMR.
- Revisa zero-ETL y conectores antes de construir jobs.

<!-- stage: Integrarlo todo -->

### Escenarios

<!-- unit: Diseñar pipelines del lake -->

<!-- goals -->

- Diseñar pipelines batch y de CDC en Glue de punta a punta.
- Explicar cada decisión en una respuesta de entrevista.

<!-- concept -->

Las preguntas de diseño prueban si sabes conectar las secciones: cómo llegan los datos, cómo se registran, cómo los jobs procesan solo lo nuevo, cómo se organiza la salida para consultarla, cómo se revisa la calidad y cómo se orquesta. Sigue a los datos y nombra una decisión por paso, luego di qué pasa al re-ejecutar. Para CDC, agrega cómo se aplican los cambios, donde formatos de tabla como Iceberg se ganan su lugar.

<!-- example -->

```text
RDS ─► DMS (full load + CDC, Parquet with op column) ─► S3 raw
     ─► Glue job: dedupe per key, MERGE INTO Iceberg ─► curated.customers
     ─► Data Quality ruleset ─► Athena / Redshift
```

#### Diseña un pipeline que convierta archivos CSV diarios en S3 en un dataset particionado y consultable.

Dejo los CSV bajo un prefijo raw por fecha, ejecuto un job Spark de Glue (disparado por EventBridge o por programación) que lee los archivos del día con un esquema definido, limpia y convierte tipos, escribe Parquet o Iceberg particionado por fecha en un prefijo curado, actualiza el catálogo y ejecuta reglas de calidad de datos. Athena o Redshift Spectrum consultan la tabla curada; Lake Formation controla el acceso.

#### ¿Cómo cargarías el CDC de una base RDS PostgreSQL en un lakehouse con Glue?

Con DMS para la carga completa más el CDC hacia S3 (Parquet con una columna de operación), o con una integración zero-ETL si existe. Un job de Glue lee los archivos de cambios nuevos (bookmarks o particiones por fecha), deduplica por clave quedándose con el último cambio y ejecuta `MERGE INTO` sobre una tabla Iceberg registrada en el Data Catalog. La compactación y la expiración de snapshots la mantienen sana.

<!-- challenge -->

En el diseño de CDC, DMS a veces entrega el mismo cambio dos veces. ¿Cómo se mantiene correcto tu pipeline?

<!-- solution -->

Deduplicar cada lote por clave primaria más la secuencia del cambio (o timestamp), quedarse con el último cambio por clave y aplicarlo con `MERGE`, así repetir un cambio ya aplicado no altera la tabla.

<!-- takeaways -->

- Sigue a los datos: llegar, registrar, procesar, organizar, revisar, orquestar.
- Haz idempotente cada paso.
- CDC necesita cambios ordenados, deduplicados y `MERGE`.

<!-- unit: Migrar ETL heredado -->

<!-- goals -->

- Planear una migración de SSIS o Informatica a Glue.
- Validar los jobs migrados antes de cambiar a los consumidores.

<!-- concept -->

Las herramientas de ETL heredadas esconden mucha lógica en mapeos visuales, lookups y dependencias del planificador. Una migración funciona cuando esa lógica se vuelve explícita: inventariar jobs y dependencias, reconstruir las fuentes como connections, reescribir las transformaciones en Spark con pruebas y reemplazar el planificador. Correr lo viejo y lo nuevo en paralelo y comparar salidas es lo que gana la confianza para el cambio.

<!-- example -->

| Heredado | Equivalente en Glue |
|---|---|
| Connection manager | Connection de Glue + Secrets Manager |
| Data flow con lookups | Job Spark con joins |
| Planificador de SQL Agent / Informatica | Step Functions, Airflow o workflows de Glue |
| Variables del paquete | Argumentos del job |

#### ¿Cómo migrarías jobs on-premises de SSIS o Informatica a Glue?

Inventariando los jobs y sus dependencias, reconstruyendo los orígenes como conexiones de Glue, reescribiendo las transformaciones en PySpark (o jobs visuales), guardando los datos de referencia en S3 o en el catálogo, orquestando con Step Functions o Airflow y validando las salidas lado a lado antes de cambiar.

<!-- challenge -->

En la ejecución en paralelo, el job nuevo produce un 0,5 % menos de filas que el paquete SSIS. ¿Cómo averiguas por qué?

<!-- solution -->

Comparar las salidas por clave para encontrar las filas que faltan y rastrearlas hacia atrás: causas típicas son joins internos en vez de left en los lookups, diferencias de mayúsculas o espacios en claves, manejo de `NULL` y filtros de fecha distintos.

<!-- takeaways -->

- Haz explícita y probada la lógica heredada oculta.
- Reemplaza planificadores y connections a propósito.
- Corre en paralelo y compara salidas antes del corte.
