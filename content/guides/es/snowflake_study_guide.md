## Guía de estudio de Snowflake

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de Snowflake: unas 200 preguntas](../../images/snowflake_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre Snowflake, desde su arquitectura hasta los virtual warehouses, las micro-particiones, la carga de datos, los datos semiestructurados, los streams y tasks, las dynamic tables, la seguridad, el uso compartido de datos, el rendimiento y el control de costos. Las respuestas reflejan la plataforma en 2026.

La guía sigue una ruta de aprendizaje en seis etapas. Cada sección se divide en unidades cortas: objetivos de aprendizaje, una explicación del concepto y un ejemplo resuelto, luego preguntas (primero de memoria, después de aplicación), un reto práctico e ideas clave. Para **aprender**, lee cada unidad de principio a fin. Para **repasar**, cambia al modo repaso o usa "Ir a las preguntas", marca las respuestas que quieras volver a ver y prueba un repaso mixto entre secciones.

<!-- QA -->
<!-- stage: Fundamentos -->

### Arquitectura

<!-- unit: Las tres capas de Snowflake -->

<!-- goals -->

- Describir las capas de almacenamiento, cómputo y servicios en la nube de Snowflake.
- Explicar la separación de almacenamiento y cómputo y en qué difiere del MPP clásico.

<!-- concept -->

Los warehouses clásicos atan los datos a las máquinas que los procesan, así que todas las cargas compiten por el mismo clúster y escalar implica mover datos. Snowflake divide el problema en tres. Los datos viven una sola vez en almacenamiento central en la nube. Clústeres de cómputo independientes, llamados virtual warehouses, los leen sin interferir entre sí. Una capa de servicios maneja todo lo que rodea a las consultas: seguridad, metadatos, optimización y transacciones.
El resultado es un warehouse que no ajustas físicamente: dimensionas el cómputo por carga y pagas solo mientras corre.

<!-- example -->

```text
cloud services: auth · metadata · optimizer · transactions
      │
compute:   WH_LOAD (M)    WH_TRANSFORM (L)    WH_BI (S, multi-cluster)
      │            │                │                 │
storage:   one copy of the data in micro-partitions on S3 / Azure Blob / GCS
```

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

<!-- challenge -->

Las cargas nocturnas frenan los dashboards de la mañana en el warehouse actual de la empresa. ¿Cómo lo resolvería la arquitectura de Snowflake?

<!-- solution -->

Dando a la carga y a BI virtual warehouses separados: ambos leen y escriben el mismo almacenamiento, pero usan cómputo independiente, así las cargas dejan de competir con las consultas de los dashboards.

<!-- takeaways -->

- Almacenamiento, cómputo y servicios son capas separadas.
- Muchos warehouses comparten una sola copia de los datos.
- El cómputo se dimensiona por carga y se cobra mientras corre.

<!-- unit: Cuentas y objetos -->

<!-- goals -->

- Navegar organizaciones, cuentas, bases de datos, esquemas y ediciones.
- Usar identificadores de cuenta, regiones y contextos de sesión.

<!-- concept -->

Todo en Snowflake está en una jerarquía: una organización tiene cuentas, cada cuenta vive en una región de nube y tiene bases de datos, que tienen esquemas, que tienen tablas, vistas, stages y otros objetos. Warehouses, usuarios y roles viven a nivel de cuenta.
Las ediciones deciden qué funciones tiene una cuenta, y una sesión siempre corre en un contexto: el rol, el warehouse, la base y el esquema actuales, lo que explica la mayoría de sorpresas de "object does not exist".

<!-- example -->

```sql
USE ROLE transformer;
USE WAREHOUSE wh_transform;
USE SCHEMA analytics.marts;
SELECT CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_ROLE(), CURRENT_WAREHOUSE();
```

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

<!-- challenge -->

Una consulta falla con "Object does not exist or not authorized", aunque un colega ve la tabla. ¿Qué revisas primero?

<!-- solution -->

El contexto de la sesión y el rol: al rol actual pueden faltarle privilegios, o el contexto de base/esquema es otro. Revisa `CURRENT_ROLE()`, usa el nombre completamente calificado y verifica los grants.

<!-- takeaways -->

- Organización → cuenta → base → esquema → objetos.
- Cada cuenta vive en una región de nube.
- Rol, warehouse, base y esquema forman el contexto de la sesión.

<!-- unit: Créditos y warehouses -->

<!-- goals -->

- Explicar los virtual warehouses y los créditos.
- Relacionar los tamaños de warehouse con el consumo de créditos.

<!-- concept -->

Un virtual warehouse es cómputo que enciendes y apagas. Mientras corre consume créditos, cobrados por segundo después de un primer minuto. Cada paso de tamaño duplica la potencia y la tasa de créditos, así que el precio por hora de un warehouse grande es alto, pero una consulta que paraleliza bien termina en la mitad del tiempo y cuesta casi lo mismo.
Eso vuelve el tamaño una decisión de velocidad más que de costo, siempre que los warehouses se suspendan cuando están ociosos.

<!-- example -->

| Tamaño | Créditos/hora | Consulta que paraleliza bien |
|---|---|---|
| X-Small | 1 | 16 min → 0,27 créditos |
| Small | 2 | 8 min → 0,27 créditos |
| Medium | 4 | 4 min → 0,27 créditos |
| Large | 8 | 2 min → 0,27 créditos |

#### ¿Qué es Snowsight?

La interfaz web de Snowflake para escribir worksheets de SQL y Python, notebooks y dashboards, explorar datos, monitorear consultas y costos, y administrar la cuenta.

#### ¿Qué es Snowflake Horizon?

Las capacidades integradas de gobierno y catálogo de Snowflake: control de acceso, clasificación de datos sensibles, políticas de enmascaramiento y de acceso a filas, etiquetas, linaje, monitoreo de la calidad de datos, auditoría y descubrimiento, aplicadas a tablas, tablas Iceberg y datos compartidos.

#### ¿Qué diferencia hay entre Snowflake y un warehouse MPP tradicional como Teradata o Redshift (aprovisionado)?

Los warehouses MPP tradicionales acoplan almacenamiento y cómputo en los mismos nodos, así que escalar implica redistribuir datos, y todas las cargas comparten un cluster. Snowflake mantiene el almacenamiento centralizado y permite arrancar warehouses independientes en segundos, sin índices, claves de distribución ni vacuum que administrar.

<!-- challenge -->

Una transformación tarda 40 minutos en un warehouse Small. El equipo teme que un Large cuadruplique el costo. ¿Qué le explicas?

<!-- solution -->

Si la consulta paraleliza, un Large (4× la tasa) termina en más o menos la cuarta parte del tiempo, así que los créditos quedan parecidos y los resultados llegan antes. Pruébalo y compara los créditos en el historial de consultas.

<!-- takeaways -->

- Los warehouses consumen créditos por segundo mientras corren.
- Cada tamaño duplica potencia y precio.
- Más grande puede ser más rápido a costo similar.

<!-- unit: Herramientas y gobierno -->

<!-- goals -->

- Conectarse a Snowflake con Snowsight, el CLI y drivers.
- Describir las funciones de gobierno de Snowflake Horizon.

<!-- concept -->

Snowflake se usa por muchas puertas: la interfaz web Snowsight para worksheets, notebooks y dashboards; herramientas de línea de comandos para scripts y despliegues; drivers y conectores para aplicaciones, herramientas de BI y pipelines.
El gobierno viene incorporado en la plataforma bajo el nombre Horizon: control de acceso, clasificación, políticas, linaje y auditoría, así la seguridad y el descubrimiento no dependen de una herramienta aparte.

<!-- example -->

```bash
snow connection test --connection prod
snow sql -q "SELECT count(*) FROM analytics.marts.fct_orders" --connection prod
```
```python
import snowflake.connector
conn = snowflake.connector.connect(account="myorg-prod", user="etl_svc",
                                   authenticator="SNOWFLAKE_JWT", private_key_file="rsa_key.p8")
```

#### ¿Qué papel cumplen la URL y el localizador de la cuenta?

El identificador de cuenta (nombre de la organización más nombre de la cuenta, o el antiguo localizador con la región) forma la URL a la que se conectan los clientes, por ejemplo `myorg-myaccount.snowflakecomputing.com`.

#### ¿Qué es el contexto de una sesión de Snowflake?

El rol, el warehouse, la base de datos y el esquema actuales de una sesión (`USE ROLE`, `USE WAREHOUSE`, `USE DATABASE`, `USE SCHEMA`). Las consultas corren con los privilegios del rol actual en el warehouse actual, y los nombres sin calificar se resuelven en la base y el esquema actuales.

#### ¿Qué es una micro-partición?

La unidad física de almacenamiento de una tabla de Snowflake: un archivo inmutable de 50 a 500 MB de datos sin comprimir (mucho menos comprimido), guardado en formato columnar. Snowflake las crea automáticamente al cargar los datos, en el orden en que llegan.

<!-- challenge -->

Un pipeline se conecta con usuario y contraseña guardados en un archivo de configuración. ¿Qué método de autenticación debería usar un usuario de servicio?

<!-- solution -->

Autenticación por key pair (u OAuth/workload identity), con la llave privada en un gestor de secretos, para que no se guarde ninguna contraseña ni aparezcan solicitudes de MFA en la automatización.

<!-- takeaways -->

- Snowsight, CLI y drivers cubren todos los accesos.
- Los usuarios de servicio deben usar key pairs u OAuth.
- Horizon incorpora el gobierno a la plataforma.

### Almacenamiento y micro-particiones

<!-- unit: Micro-particiones y poda -->

<!-- goals -->

- Explicar las micro-particiones, sus metadatos y su compresión.
- Describir la poda y lo que hacen las actualizaciones sobre un almacenamiento inmutable.

<!-- concept -->

Snowflake guarda las tablas como muchos archivos pequeños e inmutables, las micro-particiones, cada una con una porción de filas guardada por columna y comprimida automáticamente. De cada una registra metadatos como el valor mínimo y máximo de cada columna.
Esos metadatos son la forma en que las consultas se vuelven rápidas sin índices: un filtro sobre una columna permite saltarse cada micro-partición cuyo rango no puede coincidir. Como los archivos nunca cambian, updates y deletes escriben micro-particiones nuevas, lo que además abarata el Time Travel y la clonación.

<!-- example -->

```text
orders: 12,000 micro-partitions
WHERE order_date = '2026-10-17'
  micro-partition 0001: order_date 2024-01-01..2024-01-03 → skip
  ...
  micro-partition 11,880: order_date 2026-10-16..2026-10-17 → scan
Query Profile: partitions scanned 14 of 12,000
```

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

<!-- challenge -->

Una consulta sobre una tabla de 2 TB filtra por `order_date` y escanea 14 de 12.000 particiones. Otra filtra por `customer_id` y escanea 11.500. ¿Por qué la diferencia?

<!-- solution -->

Los datos se cargaron en orden de fecha, así que cada micro-partición cubre un rango estrecho de fechas y poda bien; los IDs de cliente están repartidos en todas las particiones, sus rangos de mínimo y máximo se solapan y casi nada se salta.

<!-- takeaways -->

- Las tablas son micro-particiones inmutables y comprimidas.
- Los metadatos de mínimo y máximo permiten la poda.
- Los updates escriben micro-particiones nuevas.

<!-- unit: Clustering -->

<!-- goals -->

- Explicar el clustering natural y las clustering keys.
- Decidir cuándo hacer clustering, revisarlo y controlar su costo.

<!-- concept -->

La poda solo funciona cuando los valores parecidos quedan juntos en las mismas micro-particiones. Los datos cargados en orden de tiempo quedan agrupados naturalmente por fecha sin costo. Para otras columnas de filtro en tablas muy grandes, una clustering key le dice a Snowflake que reorganice los datos en segundo plano, lo que cuesta créditos mientras la tabla siga cambiando.
Así que el clustering es un compromiso: vale la pena en tablas de varios terabytes con filtros selectivos frecuentes, y es un desperdicio en tablas pequeñas o poco consultadas.

<!-- example -->

```sql
ALTER TABLE events CLUSTER BY (event_date, customer_id);
SELECT SYSTEM$CLUSTERING_INFORMATION('events', '(event_date, customer_id)');
-- average_depth falling toward 1–2 means good clustering
ALTER TABLE events SUSPEND RECLUSTER;   -- pause during a big backfill
```

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

<!-- challenge -->

Un equipo agrega clustering keys a todas las tablas de más de 1 GB, y los créditos de automatic clustering se disparan. ¿Qué aconsejas?

<!-- solution -->

Quitar las keys de las tablas pequeñas o poco filtradas (ahí el clustering natural y los escaneos completos son baratos) y conservarlas solo en tablas muy grandes con filtros selectivos frecuentes, revisando el beneficio en los query profiles.

<!-- takeaways -->

- El clustering natural por orden de carga es gratis.
- Las clustering keys reorganizan los datos a un costo.
- Haz clustering solo en tablas grandes y muy filtradas.

<!-- unit: Tipos de tabla y costo de almacenamiento -->

<!-- goals -->

- Elegir entre tablas permanentes, transient, temporales, Iceberg, híbridas y externas.
- Entender cómo se cobran el almacenamiento, el Time Travel y el Fail-safe.

<!-- concept -->

Los tipos de tabla cambian protección, ubicación y encaje con la carga. Las permanentes tienen Time Travel y Fail-safe; las transient y temporales no tienen Fail-safe, lo que ahorra almacenamiento en datos que puedes reconstruir. Las tablas Iceberg guardan los datos en formato abierto en tu almacenamiento; las híbridas sirven operaciones rápidas por fila; las externas leen los archivos en sitio.
El almacenamiento se cobra por bytes comprimidos, incluida la historia guardada para Time Travel y Fail-safe, que puede superar los datos activos en tablas que cambian constantemente.

<!-- example -->

```sql
CREATE TRANSIENT TABLE staging.orders_raw (...) DATA_RETENTION_TIME_IN_DAYS = 0;
SELECT table_name, active_bytes, time_travel_bytes, failsafe_bytes
FROM snowflake.account_usage.table_storage_metrics
ORDER BY failsafe_bytes DESC LIMIT 10;
```

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

#### ¿Qué pasa cuando se suspende un warehouse?

Deja de consumir créditos y se borra su caché local. Con auto-resume, la siguiente consulta lo vuelve a encender en uno o dos segundos.

<!-- challenge -->

Una tabla de staging se recarga completa cada hora, y su almacenamiento de Fail-safe es diez veces su tamaño activo. ¿Qué cambias?

<!-- solution -->

Vuélvela una tabla transient con Time Travel corto (o cero): se puede reconstruir, así que no necesita Fail-safe, y las reescrituras por hora dejan de acumular almacenamiento histórico.

<!-- takeaways -->

- Las tablas permanentes llevan Time Travel y Fail-safe.
- Las transient sirven para datos reconstruibles.
- Iceberg, híbridas y externas cubren necesidades especiales.

### Virtual warehouses y cómputo

<!-- unit: Ciclo de vida de los warehouses -->

<!-- goals -->

- Configurar auto-suspend, auto-resume y statement timeouts.
- Elegir un tamaño inicial y entender el redimensionamiento.

<!-- concept -->

Los warehouses cuestan solo mientras corren, así que sus ajustes de ciclo de vida importan más que su tamaño. Auto-suspend lo detiene tras un periodo corto sin uso; auto-resume lo reinicia cuando llega una consulta. Suspender también borra su caché local, así que timeouts muy cortos pueden frenar las consultas repetidas.
El tamaño es un experimento: empieza pequeño, mide consultas representativas y ajusta. Redimensionar afecta las consultas nuevas; las que están corriendo terminan donde empezaron. Los timeouts detienen las consultas descontroladas antes de quemar créditos.

<!-- example -->

```sql
CREATE WAREHOUSE wh_transform
  WAREHOUSE_SIZE = 'SMALL'
  AUTO_SUSPEND = 60          -- seconds
  AUTO_RESUME = TRUE
  STATEMENT_TIMEOUT_IN_SECONDS = 3600
  INITIALLY_SUSPENDED = TRUE;
```

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

<!-- challenge -->

Un warehouse de desarrollo corre 24/7 con auto-suspend desactivado. ¿Qué cambias y cuál es el compromiso?

<!-- solution -->

Activa auto-suspend (por ejemplo entre 60 y 300 segundos) y auto-resume. El compromiso son unos segundos de reanudación y una caché fría tras los periodos sin uso, mucho más barato que pagar horas ociosas.

<!-- takeaways -->

- Auto-suspend y auto-resume controlan el costo ocioso.
- Empieza pequeño, mide y redimensiona.
- Los timeouts detienen consultas descontroladas.

<!-- unit: Escalado y concurrencia -->

<!-- goals -->

- Elegir entre escalar hacia arriba y hacia afuera con warehouses multi-cluster.
- Reducir las filas de espera y separar las cargas.

<!-- concept -->

Dos problemas se parecen pero necesitan arreglos distintos. Una sola consulta pesada que va lenta necesita un warehouse más grande: más memoria, menos spill. Muchas consultas concurrentes en fila necesitan más clústeres del mismo tamaño: un warehouse multi-cluster los agrega cuando crecen las colas y los quita cuando baja la carga.
Primero van, eso sí, warehouses separados por carga, para que cargas, transformaciones y dashboards no compitan en absoluto.

<!-- example -->

```sql
ALTER WAREHOUSE wh_bi SET
  WAREHOUSE_SIZE = 'SMALL'
  MIN_CLUSTER_COUNT = 1
  MAX_CLUSTER_COUNT = 4
  SCALING_POLICY = 'STANDARD';   -- start clusters quickly to avoid queuing
```

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

<!-- challenge -->

Un warehouse de BI muestra mucha fila de espera en horas pico, y alguien propone pasar de Small a X-Large. ¿Es la mejor solución?

<!-- solution -->

Probablemente no: la fila viene de la concurrencia, así que escala hacia afuera con un warehouse multi-cluster (política Standard) del mismo tamaño. Escala hacia arriba solo si las consultas individuales son lentas o hacen spill.

<!-- takeaways -->

- Escala hacia arriba para consultas pesadas; hacia afuera para concurrencia.
- Los warehouses multi-cluster agregan clústeres con la carga.
- Separa los warehouses por carga.

<!-- unit: Cómputo especializado -->

<!-- goals -->

- Conocer los warehouses Snowpark-optimized y Gen2.
- Usar el Query Acceleration Service para escaneos grandes esporádicos.

<!-- concept -->

Los warehouses estándar sirven para casi todo el SQL, pero algunas cargas necesitan otro hardware. Los Snowpark-optimized ofrecen mucha más memoria por nodo para trabajo de Python y ML. Las generaciones nuevas de warehouses traen hardware más rápido y mejoras del motor, sobre todo para pipelines con mucho DML.
El Query Acceleration Service toma otro camino: en lugar de un warehouse más grande para escaneos enormes ocasionales, presta cómputo serverless a las partes de las consultas elegibles que lo necesitan.

<!-- example -->

```sql
CREATE WAREHOUSE wh_ml WAREHOUSE_SIZE = 'MEDIUM' WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED';
ALTER WAREHOUSE wh_adhoc SET ENABLE_QUERY_ACCELERATION = TRUE
                            QUERY_ACCELERATION_MAX_SCALE_FACTOR = 8;
```

#### ¿Cómo se elige el tamaño inicial de un warehouse?

Empieza pequeño (X-Small o Small) para desarrollo y cargas sencillas, prueba consultas representativas y sube de tamaño solo cuando las consultas derraman, tardan demasiado o no cumplen el tiempo objetivo. Mide el costo por ejecución, no solo la duración.

#### ¿Qué cachés tiene Snowflake?

El caché de resultados (en la capa de servicios: los resultados se reutilizan durante 24 horas si la consulta y los datos no cambiaron), el caché del warehouse (datos de micro-particiones en el SSD local del warehouse mientras está encendido) y el caché de metadatos (estadísticas que responden algunas consultas como `COUNT(*)` o `MIN` sin warehouse).

#### ¿Cuándo se usa el caché de resultados?

Cuando el mismo texto de consulta se vuelve a ejecutar, los datos no cambiaron, el usuario tiene los privilegios necesarios y la consulta no usa funciones no deterministas como `CURRENT_TIMESTAMP()`. Cada reutilización extiende la retención, hasta 31 días. No cuesta cómputo.

<!-- challenge -->

Un warehouse ad hoc es Small, pero las consultas de unos pocos analistas escanean miles de millones de filas y corren una hora. Redimensionar para todos desperdicia créditos. ¿Qué puede ayudar?

<!-- solution -->

Activa el Query Acceleration Service en ese warehouse: los escaneos grandes elegibles reciben cómputo serverless extra para sus partes pesadas mientras las consultas normales corren como siempre.

<!-- takeaways -->

- Los warehouses Snowpark-optimized agregan memoria.
- Los warehouses Gen2 aceleran muchos pipelines.
- La aceleración de consultas ayuda con escaneos enormes ocasionales.

### Caché

<!-- unit: Las cachés de Snowflake -->

<!-- goals -->

- Describir las cachés de resultados, de warehouse y de metadatos.
- Sopesar la caché del warehouse frente al auto-suspend.

<!-- concept -->

Tres cachés abaratan el trabajo repetido. La caché de resultados devuelve durante un día los resultados de consultas idénticas sin usar ningún warehouse. Cada warehouse guarda en disco local los datos leídos recientemente, así los escaneos repetidos se saltan el almacenamiento remoto. La caché de metadatos responde al instante preguntas como el conteo de filas.
La caché del warehouse vive solo mientras corre el warehouse, así que el momento de suspender es un compromiso entre costo y datos calientes para los dashboards.

<!-- example -->

| Caché | Dónde | Duración | ¿Necesita warehouse? |
|---|---|---|---|
| Resultados | Servicios en la nube | 24 h (se renueva al reutilizarse, máx. 31 días) | No |
| Warehouse (disco local) | Nodos de cómputo | Hasta el suspend | Sí |
| Metadatos | Servicios en la nube | Siempre | No (para `COUNT(*)`, mín./máx.) |

#### ¿Cómo influye el caché del warehouse en el auto-suspend?

Suspender borra el caché local, así que las consultas siguientes leen del almacenamiento remoto y son más lentas. Para dashboards que consultan los mismos datos una y otra vez, un auto-suspend más largo puede ser más rápido sin costar mucho más.

#### ¿Cómo se desactiva el caché de resultados para hacer pruebas?

`ALTER SESSION SET USE_CACHED_RESULT = FALSE;` para que las consultas de benchmark se ejecuten de verdad.

<!-- challenge -->

Un warehouse de BI con auto-suspend de 60 segundos hace lento el primer dashboard de cada sesión. ¿Qué consideras?

<!-- solution -->

Un auto-suspend más largo en horario laboral (por ejemplo 5–10 minutos) mantiene caliente la caché local entre usuarios; sopesa los créditos ociosos extra frente a dashboards más rápidos.

<!-- takeaways -->

- Las cachés de resultados, warehouse y metadatos evitan trabajo repetido.
- La caché del warehouse desaparece al suspender.
- Ajusta el suspend para BI que depende de la caché.

<!-- unit: La caché de resultados -->

<!-- goals -->

- Explicar cuándo se usa la caché de resultados y entre qué usuarios.
- Desactivarla para benchmarks y diagnosticar fallos.

<!-- concept -->

La caché de resultados es la consulta más barata: cero créditos. Aplica cuando el mismo texto de consulta se vuelve a correr, los datos no cambiaron y el rol puede leerlos, incluso para otro usuario. Pequeñas diferencias la rompen: datos cambiados, texto distinto, funciones no deterministas o algunos ajustes de sesión.
Los benchmarks deben desactivarla, o miden la caché en lugar de la consulta.

<!-- example -->

```sql
ALTER SESSION SET USE_CACHED_RESULT = FALSE;   -- benchmark the real query
SELECT region, SUM(amount) FROM sales.fct_orders WHERE order_date >= '2026-10-01' GROUP BY 1;
-- Query Profile shows "QUERY RESULT REUSE" when the cache was hit
```

#### ¿El caché de resultados funciona entre usuarios?

Sí, si el rol del otro usuario tiene los privilegios necesarios sobre los objetos y el texto de la consulta es idéntico; los resultados no están atados al usuario original.

#### ¿Por qué una consulta repetida puede no usar el caché de resultados?

Los datos cambiaron, el texto de la consulta es distinto (incluso por espacios o mayúsculas en algunos casos), usa funciones no deterministas, consulta funciones externas o algunas funciones de tabla, el resultado superó su retención, o el caché está desactivado en la sesión.

#### ¿Qué formas hay de cargar datos en Snowflake?

Carga masiva con `COPY INTO` desde stages, carga continua con Snowpipe (archivos) y Snowpipe Streaming (filas), el conector de Kafka, Openflow y herramientas ETL/ELT de socios, sentencias `INSERT`, tablas externas e Iceberg para consultar en su lugar, y el uso compartido de datos para los datos de otras cuentas.

#### ¿Qué es un stage?

Una ubicación para archivos que se cargan o descargan. Los stages internos están dentro de Snowflake: de usuario (`@~`), de tabla (`@%tabla`) y con nombre. Los stages externos apuntan a contenedores de S3, GCS o Azure, normalmente a través de una storage integration.

<!-- challenge -->

Una consulta de dashboard que usa `CURRENT_TIMESTAMP()` en su filtro nunca usa la caché de resultados. ¿Por qué y cómo lo arreglas?

<!-- solution -->

Las funciones no deterministas hacen distinta cada ejecución, así que los resultados no se pueden reutilizar. Reemplázalas por un parámetro de fecha fijo desde la herramienta de BI (por ejemplo la fecha del reporte) para que las ejecuciones idénticas compartan resultados.

<!-- takeaways -->

- Consulta idéntica, datos sin cambios, rol permitido: acierto de caché.
- Las funciones no deterministas impiden reutilizar.
- Desactiva la caché al hacer benchmarks.

<!-- stage: Ingresar datos -->

### Carga de datos

<!-- unit: Stages, integraciones y formatos de archivo -->

<!-- goals -->

- Configurar stages, storage integrations y file formats.
- Subir, inspeccionar e inferir el esquema de archivos en stage.

<!-- concept -->

Cargar empieza por dónde están los archivos. Un stage apunta a archivos, dentro de Snowflake o en tu almacenamiento en la nube; una storage integration permite que Snowflake acceda a ese almacenamiento con un rol de nube en lugar de llaves; un file format dice cómo parsear los archivos.
Antes de cargar puedes consultar directamente los archivos en stage e inferir su esquema, lo que agiliza revisar fuentes nuevas.

<!-- example -->

```sql
CREATE STORAGE INTEGRATION s3_lake TYPE = EXTERNAL_STAGE STORAGE_PROVIDER = 'S3'
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/snowflake-lake' ENABLED = TRUE
  STORAGE_ALLOWED_LOCATIONS = ('s3://lake/landing/');
CREATE FILE FORMAT ff_csv TYPE = CSV FIELD_DELIMITER = ';' SKIP_HEADER = 1 NULL_IF = ('', 'NULL');
CREATE STAGE landing URL = 's3://lake/landing/' STORAGE_INTEGRATION = s3_lake FILE_FORMAT = ff_csv;
SELECT $1, $2, METADATA$FILENAME FROM @landing/orders/ LIMIT 10;
```

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

<!-- challenge -->

Un stage se creó con access keys de AWS incrustadas en su definición. ¿Con qué lo reemplazas?

<!-- solution -->

Con una storage integration que use un rol de IAM en el que confíe Snowflake, limitada a las ubicaciones permitidas, y recrea el stage sobre ella; luego borra las llaves.

<!-- takeaways -->

- Los stages apuntan a archivos; los file formats los describen.
- Las storage integrations reemplazan las llaves incrustadas.
- Consulta e infiere los archivos en stage antes de cargar.

<!-- unit: Carga masiva con COPY -->

<!-- goals -->

- Cargar archivos con COPY INTO, manejo de errores y transformaciones.
- Dimensionar bien los archivos, entender los metadatos de carga y descargar datos.

<!-- concept -->

`COPY INTO` carga en paralelo archivos en stage a una tabla, un archivo por hilo, así que el tamaño de los archivos define la velocidad: muchos archivos diminutos desperdician sobrecarga y un archivo enorme no se puede dividir. Snowflake recuerda qué archivos cargó durante 64 días, así que las re-ejecuciones los saltan salvo que se fuerce.
Los errores necesitan una política: abortar, saltar filas o saltar archivos. Se pueden hacer transformaciones simples durante la carga, y el mismo comando en sentido inverso descarga resultados de consultas a archivos.

<!-- example -->

```sql
COPY INTO raw.orders (order_id, customer_id, amount, source_file)
FROM (SELECT $1::NUMBER, $2::NUMBER, $3::NUMBER(12,2), METADATA$FILENAME FROM @landing/orders/)
ON_ERROR = 'CONTINUE';
SELECT * FROM TABLE(VALIDATE(raw.orders, JOB_ID => '_last'));   -- rejected rows
COPY INTO @exports/orders/ FROM (SELECT * FROM marts.fct_orders) FILE_FORMAT = (TYPE = PARQUET);
```

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

<!-- challenge -->

Un `COPY` diario de un solo archivo gzip de 40 GB tarda una hora incluso en un warehouse Large. ¿Qué cambias?

<!-- solution -->

Divide la entrada en archivos de unos 100–250 MB comprimidos (en el productor o con un paso de preprocesamiento), para que `COPY` cargue muchos archivos en paralelo con los hilos del warehouse.

<!-- takeaways -->

- `COPY` paraleliza por archivo; archivos de ~100–250 MB.
- Los metadatos de carga saltan durante 64 días los archivos ya cargados.
- Elige a propósito una política `ON_ERROR`.

<!-- unit: Carga continua -->

<!-- goals -->

- Cargar archivos de forma continua con Snowpipe y filas con Snowpipe Streaming.
- Ingestar datos de CDC y evitar cargas duplicadas.

<!-- concept -->

Cuando los datos llegan todo el día, esperar un `COPY` nocturno agrega latencia. Snowpipe corre el mismo `COPY` de forma serverless a medida que cae cada archivo, avisado por eventos de la nube; los archivos pequeños suben su sobrecarga por archivo. Snowpipe Streaming se salta los archivos y escribe filas desde Kafka o SDKs con segundos de latencia.
Los cambios de bases de datos suelen llegar por herramientas de CDC a tablas crudas y luego se aplican con `MERGE`. Los duplicados vienen de productores que reenvían datos, no de Snowpipe, así que los pipelines deduplican aguas abajo.

<!-- example -->

```sql
CREATE PIPE raw.orders_pipe AUTO_INGEST = TRUE AS
COPY INTO raw.orders FROM @landing/orders/ FILE_FORMAT = ff_csv;
SHOW PIPES;                                      -- notification_channel → configure S3 events to SQS
SELECT SYSTEM$PIPE_STATUS('raw.orders_pipe');
```

#### ¿Cómo se consultan archivos en un stage sin cargarlos?

`SELECT $1, $2, METADATA$FILENAME FROM @stage/ruta (FILE_FORMAT => 'my_csv')`, útil para inspeccionar los archivos antes de cargarlos.

#### ¿Qué es Openflow?

El servicio administrado de integración de datos de Snowflake, basado en Apache NiFi, con conectores para bases de datos, aplicaciones SaaS y flujos, desplegado en Snowflake o en tu propia nube (bring your own cloud), para ingerir datos estructurados y no estructurados.

#### ¿Cómo se carga en Snowflake una base relacional con CDC?

Con una herramienta de CDC (conectores de Openflow, Debezium con Kafka y el conector de Kafka para Snowflake, Fivetran, AWS DMS escribiendo en S3 más Snowpipe) que deja los eventos de cambio en tablas raw, y luego un `MERGE` desde un stream o una dynamic table para aplicarlos a la tabla de estado actual.

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

<!-- challenge -->

Un productor escribe un archivo diminuto por evento, y los costos de Snowpipe crecen más rápido que el volumen de datos. ¿Qué cambias?

<!-- solution -->

Agrupa los archivos en el productor (por ejemplo con el buffering de Firehose a ~100 MB o unos minutos), o pasa a Snowpipe Streaming para ingesta por filas, evitando la sobrecarga por archivo.

<!-- takeaways -->

- Snowpipe carga los archivos a medida que llegan.
- Snowpipe Streaming escribe filas con baja latencia.
- Deduplica aguas abajo; los productores reenvían datos.

### Datos semiestructurados

<!-- unit: VARIANT y consultas por ruta -->

<!-- goals -->

- Guardar JSON en VARIANT y consultarlo con rutas y casts.
- Manejar tipos mezclados y la diferencia entre claves faltantes y null de JSON.

<!-- concept -->

Los datos semiestructurados llegan tal cual a columnas `VARIANT`, que Snowflake guarda internamente en forma columnar, así las consultas sobre rutas comunes siguen siendo rápidas. Navegas con notación de rutas y haces cast a tipos SQL al leer.
Dos sutilezas importan para la corrección: un campo que llega a veces como número y a veces como string necesita casts defensivos, y una clave faltante es `NULL` de SQL mientras que un `null` de JSON es un null de `VARIANT`, que se comporta distinto en las comparaciones.

<!-- example -->

```sql
SELECT payload:order_id::NUMBER                 AS order_id,
       payload:customer.city::STRING            AS city,
       TRY_TO_NUMBER(payload:amount::STRING)    AS amount,     -- tolerate "12.50" or 12.5
       IS_NULL_VALUE(payload:coupon)            AS coupon_is_json_null
FROM raw.events_json;
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

<!-- challenge -->

`WHERE payload:discount IS NULL` no encuentra las filas donde el JSON tiene `"discount": null`. ¿Por qué y cómo las incluyes?

<!-- solution -->

Un null de JSON es un null de `VARIANT`, no `NULL` de SQL. Haz cast primero (`payload:discount::NUMBER IS NULL`) o prueba ambos con `IS_NULL_VALUE(payload:discount)`.

<!-- takeaways -->

- `VARIANT` guarda JSON con eficiencia.
- Navega con rutas; haz cast al leer.
- Clave faltante ≠ null de JSON.

<!-- unit: Aplanar y modelar JSON -->

<!-- goals -->

- Expandir arrays con FLATTEN y construir JSON a partir de filas.
- Decidir qué dejar en VARIANT y qué extraer, y cargar Parquet por nombre de columna.

<!-- concept -->

Los arrays dentro del JSON se vuelven filas con `FLATTEN`, una por elemento, unidas a su padre con un join lateral. La dirección opuesta, construir JSON a partir de filas, sirve para APIs y exportaciones.
La decisión de modelado es por capas: deja el JSON crudo en `VARIANT` por flexibilidad y auditoría, y extrae los campos estables y de uso frecuente a columnas tipadas en tablas curadas, donde tipos, restricciones y poda funcionan mejor. Los archivos columnares pueden cargar directo a columnas que coincidan.

<!-- example -->

```sql
SELECT o.payload:order_id::NUMBER AS order_id,
       i.value:sku::STRING        AS sku,
       i.value:qty::NUMBER        AS qty
FROM raw.orders_json o,
     LATERAL FLATTEN(input => o.payload:items) i;

COPY INTO raw.orders FROM @landing/orders_parquet/
FILE_FORMAT = (TYPE = PARQUET) MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
```

#### ¿Cómo se cargan columnas de Parquet directamente en columnas de tabla?

Con `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE` en `COPY`, que asocia las columnas del archivo a las de la tabla por nombre, o seleccionando `$1:nombre_columna::tipo` de forma explícita.

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

<!-- challenge -->

Cada consulta de dashboard extrae los mismos diez campos de una columna `VARIANT` enorme. ¿Qué cambias?

<!-- solution -->

Extrae esos campos a columnas tipadas en una tabla curada (o una dynamic table) que se refresque desde lo crudo, así las consultas leen columnas angostas y tipadas con mejor poda; conserva el `VARIANT` crudo para auditoría y campos nuevos.

<!-- takeaways -->

- `FLATTEN` convierte arrays en filas.
- Conserva el JSON crudo; extrae a columnas los campos estables.
- `MATCH_BY_COLUMN_NAME` carga archivos columnares por nombre.

<!-- stage: Transformar datos -->

### Funciones SQL

<!-- unit: Consultar y cambiar datos -->

<!-- goals -->

- Usar QUALIFY, MERGE, PIVOT, SAMPLE y MATCH_RECOGNIZE.
- Escribir deduplicaciones y upserts de forma idiomática.

<!-- concept -->

El SQL de Snowflake incluye atajos para patrones que los analistas escriben a diario. `QUALIFY` filtra sobre resultados de ventana sin subconsulta, la forma más limpia de conservar la última fila por clave. `MERGE` aplica inserts, updates y deletes desde una fuente en una sentencia. Los pivots rotan datos para reportes, el muestreo lee una fracción para explorar y el pattern matching encuentra secuencias de eventos.

<!-- example -->

```sql
MERGE INTO silver.customers t
USING (
  SELECT * FROM raw.customer_changes
  QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1
) s
ON t.customer_id = s.customer_id
WHEN MATCHED AND s.op = 'D' THEN DELETE
WHEN MATCHED THEN UPDATE SET email = s.email, segment = s.segment, updated_at = s.updated_at
WHEN NOT MATCHED AND s.op <> 'D' THEN INSERT (customer_id, email, segment, updated_at)
  VALUES (s.customer_id, s.email, s.segment, s.updated_at);
```

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

<!-- challenge -->

Un `MERGE` falla con "Duplicate row detected during DML action". ¿Qué está mal en la fuente y cómo se arregla?

<!-- solution -->

Varias filas de la fuente coinciden con la misma fila destino. Deduplica primero la fuente conservando una fila por clave (por ejemplo con `QUALIFY ROW_NUMBER() ... = 1`).

<!-- takeaways -->

- `QUALIFY` filtra resultados de ventana.
- `MERGE` hace upserts y deletes en una sentencia.
- Deduplica por clave las fuentes de MERGE.

<!-- unit: Claves, secuencias y transacciones -->

<!-- goals -->

- Entender qué restricciones impone Snowflake.
- Usar bien secuencias, columnas identity y transacciones.

<!-- concept -->

Snowflake acepta declaraciones de primary, unique y foreign key, pero en tablas estándar solo impone `NOT NULL`. Las demás documentan la intención y ayudan a las herramientas y al optimizador, así que la unicidad la deben garantizar y probar los pipelines.
Las secuencias y columnas identity generan números únicos, no sin huecos. Las sentencias hacen autocommit salvo que se envuelvan en una transacción explícita, que corre con aislamiento read committed.

<!-- example -->

```sql
CREATE TABLE dim_customer (
  customer_key NUMBER IDENTITY(1,1),
  customer_id NUMBER NOT NULL,          -- enforced
  email STRING,
  PRIMARY KEY (customer_key)            -- declared, not enforced
);
SELECT customer_id, COUNT(*) FROM dim_customer GROUP BY 1 HAVING COUNT(*) > 1;   -- test it yourself
```

#### ¿Cómo son las transacciones en Snowflake?

ACID con nivel de aislamiento read committed. Cada sentencia hace autocommit salvo que esté dentro de un `BEGIN … COMMIT` explícito. El DDL hace commit implícito. El DML concurrente sobre la misma tabla puede quedar bloqueado hasta que termine la otra transacción.

#### ¿Qué hace `UNDROP`?

Restaura una tabla, esquema o base de datos borrados recientemente desde Time Travel, siempre que esté dentro del periodo de retención.

#### ¿Qué hace `SWAP WITH`?

`ALTER TABLE a SWAP WITH b` intercambia de forma atómica los nombres de dos tablas, una forma común de publicar una tabla reconstruida sin interrumpir a los lectores.

<!-- challenge -->

Un equipo confía en una primary key declarada para evitar duplicados, y tras una re-ejecución aparecen duplicados. ¿Qué salió mal y qué agregas?

<!-- solution -->

Las primary keys no se imponen en tablas estándar. Haz idempotentes las cargas (`MERGE` sobre la clave o delete-insert por lote) y agrega una prueba de unicidad (test de dbt o data metric function).

<!-- takeaways -->

- En tablas estándar solo se impone `NOT NULL`.
- Las secuencias son únicas, no sin huecos.
- Garantiza y prueba la unicidad en los pipelines.

<!-- unit: Código procedural -->

<!-- goals -->

- Escribir UDFs, stored procedures y Snowflake Scripting.
- Elegir lenguajes y casos de uso para cada uno.

<!-- concept -->

Cuando el SQL solo no alcanza, Snowflake corre código junto a los datos. Las UDFs devuelven valores o tablas y se llaman desde consultas; los stored procedures corren secuencias de sentencias con control de flujo, para administración o lógica de varios pasos. Ambos se pueden escribir en SQL, Python, Java, Scala o JavaScript.
Snowflake Scripting lleva variables, ciclos y manejo de errores al propio SQL, a menudo suficiente para procedimientos sin otro lenguaje.

<!-- example -->

```sql
CREATE OR REPLACE PROCEDURE ops.drop_old_dev_schemas(days INT)
RETURNS STRING LANGUAGE SQL AS
$$
DECLARE c CURSOR FOR SELECT schema_name FROM dev.information_schema.schemata
                     WHERE created < DATEADD(day, -:days, CURRENT_TIMESTAMP());
        n INT DEFAULT 0;
BEGIN
  FOR r IN c DO
    EXECUTE IMMEDIATE 'DROP SCHEMA dev.' || r.schema_name; n := n + 1;
  END FOR;
  RETURN n || ' schemas dropped';
END;
$$;
```

#### ¿Qué es `CREATE OR ALTER`?

Una sentencia que crea un objeto si no existe o lo modifica para que coincida con la definición si ya existe, conservando los datos y los permisos, útil para despliegues declarativos de tablas y otros objetos.

#### ¿Para qué sirven `PIVOT` y `UNPIVOT`?

Para rotar filas en columnas (por ejemplo los meses en columnas) y columnas en filas. `PIVOT` admite listas de valores dinámicas con `ANY` en las versiones recientes.

#### ¿Qué hace `MATCH_RECOGNIZE`?

Busca patrones en filas ordenadas (por ejemplo una secuencia de eventos en una sesión, como vista → carrito → compra) y devuelve las coincidencias con medidas, sin escribir self-joins complejos.

<!-- challenge -->

Una UDF de Python se llama sobre 2.000 millones de filas para aplicar una regla de impuestos simple, y la consulta es lenta. ¿Qué sugieres?

<!-- solution -->

Expresa la regla en SQL (`CASE` y aritmética) para que corra de forma nativa, o usa una UDF de Python vectorizada si de verdad hace falta Python. El Python fila por fila agrega sobrecarga de serialización.

<!-- takeaways -->

- Las UDFs devuelven valores; los procedimientos corren pasos.
- Se soportan varios lenguajes.
- Prefiere SQL cuando puede expresar la lógica.

<!-- unit: Manejar objetos -->

<!-- goals -->

- Recuperar objetos borrados con UNDROP y publicar de forma atómica con SWAP.
- Mantener las definiciones declarativas con CREATE OR ALTER.

<!-- concept -->

Unos pocos comandos hacen más segura la gestión de objetos. `UNDROP` restaura desde Time Travel una tabla, esquema o base borrada recientemente. `SWAP WITH` intercambia dos tablas de forma atómica, así una tabla reconstruida puede reemplazar a la vieja sin que los consumidores vean nunca un estado a medio cargar.
`CREATE OR ALTER` trae definiciones declarativas: describes el objeto que quieres y Snowflake lo crea o lo ajusta sin borrar datos.

<!-- example -->

```sql
CREATE OR REPLACE TABLE marts.fct_revenue_new AS SELECT ...;
-- validate fct_revenue_new ...
ALTER TABLE marts.fct_revenue SWAP WITH marts.fct_revenue_new;   -- atomic publish
DROP TABLE marts.fct_revenue_new;
UNDROP TABLE marts.fct_revenue_old;                              -- if needed
```

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

<!-- challenge -->

Un job nocturno reconstruye en sitio un mart grande, y los dashboards muestran datos vacíos o parciales durante 20 minutos. ¿Cómo lo arreglas?

<!-- solution -->

Construye la versión nueva en una tabla aparte, valídala y luego publica de forma atómica con `ALTER TABLE ... SWAP WITH`; los dashboards ven la tabla vieja o la nueva completa.

<!-- takeaways -->

- `UNDROP` restaura objetos borrados.
- `SWAP WITH` publica tablas reconstruidas de forma atómica.
- `CREATE OR ALTER` mantiene declarativas las definiciones.

### Time Travel, Fail-safe y clonado

<!-- unit: Streams -->

<!-- goals -->

- Seguir los cambios de las tablas con streams.
- Elegir tipos de stream y evitar streams vencidos.

<!-- concept -->

Un stream es un marcador sobre el historial de cambios de una tabla. Consultarlo devuelve las filas insertadas, actualizadas o borradas desde la última vez que se consumió, y consumirlo en una sentencia DML adelanta el marcador. Eso convierte cualquier tabla en un feed de cambios para procesamiento incremental.
Los streams append-only son más baratos cuando solo importan los inserts. Un stream que no se consume durante más tiempo que la retención de la tabla se vuelve stale y hay que recrearlo.

<!-- example -->

```sql
CREATE STREAM raw.orders_changes ON TABLE raw.orders;
INSERT INTO silver.orders_log
SELECT order_id, amount, METADATA$ACTION, METADATA$ISUPDATE, CURRENT_TIMESTAMP()
FROM raw.orders_changes;          -- consuming the stream advances its offset
```

#### ¿Qué es el clonado zero-copy?

Crear al instante una copia de una tabla, esquema o base de datos con `CLONE`, sin copiar datos: el clon comparte las micro-particiones del original y solo los cambios nuevos consumen almacenamiento. Se usa para entornos de desarrollo y pruebas, respaldos antes de cambios riesgosos y fotos en un momento dado.

#### ¿Qué hereda un clon?

Los datos y la estructura, y en las bases de datos y esquemas, los objetos hijos. Los privilegios sobre el objeto origen no se copian salvo que uses `COPY GRANTS`; los privilegios sobre los objetos hijos sí se clonan. Los pipes que referencian stages internos, y algunos otros objetos, no se clonan.

#### ¿Cómo le das a un desarrollador una copia completa de los datos de producción a bajo costo?

Clonando la base de producción en una base de desarrollo (al instante, sin almacenamiento extra hasta que haya cambios), aplicando políticas de enmascaramiento o una capa de vistas seguras si los datos son sensibles, y dándole al desarrollador un rol sobre el clon.

<!-- challenge -->

Un stream sobre una tabla de staging no se consumió durante unas vacaciones de dos semanas, y ahora figura como stale. ¿Por qué y cómo lo evitas?

<!-- solution -->

Su offset quedó por fuera de la retención de datos de la tabla, así que los cambios no se pueden reconstruir. Recréalo y recarga; consume los streams con regularidad (una task programada) o sube la retención de las tablas de las que dependen.

<!-- takeaways -->

- Los streams devuelven los cambios desde el último consumo.
- Consumir en DML adelanta el offset.
- Los streams sin consumir vencen tras la retención.

<!-- unit: Tasks -->

<!-- goals -->

- Programar SQL con tasks, serverless tasks y triggered tasks.
- Construir y monitorear grafos de tasks con finalizers.

<!-- concept -->

Las tasks corren SQL o procedimientos según un horario, después de otras tasks o cuando un stream tiene datos nuevos. Encadenadas en grafos, forman pipelines dentro de Snowflake sin un orquestador externo. Las serverless tasks dejan que Snowflake dimensione el cómputo automáticamente.
Como todo pipeline, los grafos de tasks necesitan monitoreo y limpieza: el historial de tasks muestra ejecuciones y fallas, y una finalizer task corre al final pase lo que pase, para avisos o limpieza.

<!-- example -->

```sql
CREATE TASK silver.apply_orders
  WAREHOUSE = wh_transform
  WHEN SYSTEM$STREAM_HAS_DATA('raw.orders_changes')
AS
  MERGE INTO silver.orders t USING raw.orders_changes s ON t.order_id = s.order_id
  WHEN MATCHED THEN UPDATE SET amount = s.amount
  WHEN NOT MATCHED THEN INSERT (order_id, amount) VALUES (s.order_id, s.amount);
ALTER TASK silver.apply_orders RESUME;
```

#### ¿Qué pasa con el Time Travel si borras y vuelves a crear una tabla con el mismo nombre?

La tabla nueva es distinta; la borrada queda en Time Travel y solo se puede restaurar con `UNDROP` tras renombrar la nueva, porque los nombres deben ser únicos.

#### ¿Se puede clonar desde un momento del pasado?

Sí: `CREATE TABLE t_clone CLONE t AT (TIMESTAMP => ...)` o `BEFORE (STATEMENT => ...)`, siempre que esté dentro del periodo de retención. Es una forma común de recuperarse de un cambio erróneo conservando la tabla actual para comparar.

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

<!-- challenge -->

Una task programada cada minuto revisa un stream y casi nunca encuentra nada, y aun así el warehouse rara vez se suspende. ¿Qué cambias?

<!-- solution -->

Vuélvela una triggered task (sin horario, corre solo cuando el stream tiene datos) o conserva la condición `WHEN SYSTEM$STREAM_HAS_DATA`, que se salta las ejecuciones sin reanudar el warehouse; considera las serverless tasks.

<!-- takeaways -->

- Las tasks corren por horario, tras otras o con datos nuevos.
- Las serverless tasks dimensionan el cómputo solas.
- Monitorea el historial; los finalizers limpian.

<!-- unit: Dynamic tables y vistas materializadas -->

<!-- goals -->

- Construir pipelines declarativos con dynamic tables y target lag.
- Elegir entre dynamic tables, vistas materializadas y streams con tasks.

<!-- concept -->

Las dynamic tables convierten los pipelines en definiciones: escribes la consulta y una meta de frescura, y Snowflake mantiene la tabla al día, de forma incremental cuando puede. Varias dynamic tables encadenadas forman un pipeline cuyos pasos de arriba se refrescan tan seguido como lo necesiten los de abajo.
Las vistas materializadas resuelven un problema más estrecho: acelerar de forma transparente las consultas sobre una sola tabla. Streams y tasks siguen siendo la herramienta para control total, como lógica procedural o efectos secundarios.

<!-- example -->

```sql
CREATE DYNAMIC TABLE marts.daily_revenue
  TARGET_LAG = '15 minutes'
  WAREHOUSE = wh_transform
  REFRESH_MODE = INCREMENTAL
AS
SELECT order_date, region, SUM(amount) AS revenue
FROM silver.orders
GROUP BY order_date, region;
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

<!-- challenge -->

Una dynamic table siempre hace refrescos completos y cuesta mucho. ¿Qué revisas?

<!-- solution -->

Si su consulta usa construcciones que impiden el refresco incremental (algunas funciones no deterministas, ciertos joins o patrones de ventana); revisa el refresh mode reportado, simplifica la consulta o divídela en dynamic tables encadenadas que puedan refrescarse de forma incremental.

<!-- takeaways -->

- Dynamic tables: consulta más target lag.
- El refresco incremental procesa solo los cambios.
- Las vistas materializadas aceleran las consultas de una tabla.

### Streams, tasks y dynamic tables

<!-- unit: Snowpark para código -->

<!-- goals -->

- Procesar datos en Snowflake con Snowpark y pandas on Snowflake.
- Manejar paquetes de Python y usar notebooks.

<!-- concept -->

Snowpark te deja escribir código de DataFrames en Python, Java o Scala que se compila a SQL y corre en Snowflake, así los datos nunca salen de la plataforma. Para lógica incómoda en SQL, como reglas de negocio complejas o feature engineering, suele ser más claro.
pandas on Snowflake corre de la misma forma el código pandas conocido a escala. Los paquetes vienen de un canal curado o de tus propias cargas, y los notebooks mezclan SQL y Python sobre los mismos datos.

<!-- example -->

```python
from snowflake.snowpark import Session, functions as F
session = Session.builder.configs(conn_params).create()
orders = session.table("silver.orders")
features = (orders.group_by("customer_id")
                  .agg(F.count("order_id").alias("orders"), F.sum("amount").alias("spend")))
features.write.mode("overwrite").save_as_table("ml.customer_features")
```

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

<!-- challenge -->

Un científico de datos exporta 200 GB de Snowflake a su portátil para calcular features en pandas. ¿Qué sugieres?

<!-- solution -->

Corre la misma lógica en Snowflake con Snowpark (o pandas on Snowflake), para que el cálculo ocurra junto a los datos en un warehouse, y escribe las features de vuelta a una tabla.

<!-- takeaways -->

- Los DataFrames de Snowpark corren dentro de Snowflake.
- pandas on Snowflake escala el código pandas.
- Los datos no tienen que salir de la plataforma.

<!-- unit: Apps, contenedores e IA -->

<!-- goals -->

- Describir Snowpark Container Services, Streamlit in Snowflake y Snowflake ML.
- Usar las funciones de Cortex AI desde SQL.

<!-- concept -->

Snowflake sigue agregando formas de correr aplicaciones donde están los datos. Container Services aloja cualquier servicio o modelo en contenedor; las apps de Streamlit corren dentro de la cuenta con sus permisos; Snowflake ML ofrece features, registro y herramientas de entrenamiento.
Cortex lleva los modelos de lenguaje al SQL: clasificación, extracción, resumen y completado como funciones, gobernadas como cualquier consulta.

<!-- example -->

```sql
SELECT ticket_id,
       AI_CLASSIFY(body, ['billing', 'bug', 'feature request']):labels[0]::STRING AS category,
       AI_COMPLETE('claude-sonnet-4-5', 'Summarize in one sentence: ' || body)  AS summary
FROM support.tickets
WHERE created_at >= DATEADD(day, -1, CURRENT_TIMESTAMP());
```

#### ¿Cómo funciona el control de acceso en Snowflake?

Con control de acceso basado en roles (RBAC) combinado con control discrecional: los privilegios se conceden a roles, los roles se conceden a usuarios y a otros roles, y cada objeto tiene un rol propietario que lo controla.

#### ¿Cuáles son los roles definidos por el sistema?

ORGADMIN (organización), ACCOUNTADMIN (el rol más alto de la cuenta; úsalo con moderación), SECURITYADMIN (administra los permisos y puede administrar usuarios y roles), USERADMIN (crea usuarios y roles), SYSADMIN (crea warehouses y bases de datos; los roles propios deberían colgar de él) y PUBLIC (concedido a todos).

#### ¿Cómo es una buena jerarquía de roles?

Roles de acceso que tienen los privilegios sobre los objetos (por ejemplo `SALES_READ`, `SALES_WRITE`), roles funcionales que representan puestos o equipos (`ANALYST`, `DATA_ENGINEER`) a los que se conceden los roles de acceso, y roles funcionales que cuelgan de SYSADMIN para que los administradores puedan gestionarlo todo. Las cuentas de servicio tienen sus propios roles funcionales.

#### ¿Qué son los future grants?

Permisos que se aplican automáticamente a los objetos que se creen más adelante en un esquema o base de datos: `GRANT SELECT ON FUTURE TABLES IN SCHEMA sales.marts TO ROLE sales_read;`. Evitan que falten permisos en las tablas nuevas.

<!-- challenge -->

Soporte quiere que cada ticket nuevo se etiquete por tema cada hora, y el equipo planea construir un servicio de ML aparte. ¿Qué podría ser más simple?

<!-- solution -->

Una task programada (o una dynamic table) que corra una función de Cortex como `AI_CLASSIFY` sobre los tickets nuevos en SQL, gobernada por los permisos de Snowflake, sin un servicio aparte que alojar.

<!-- takeaways -->

- Container Services aloja cualquier servicio en Snowflake.
- Las apps de Streamlit corren con el gobierno de la cuenta.
- Cortex expone LLMs como funciones SQL.

### Seguridad y control de acceso

<!-- unit: Modelar en Snowflake -->

<!-- goals -->

- Aplicar esquemas estrella, normalización y tablas anchas en Snowflake.
- Implementar SCD tipo 2 y datos de referencia conformados.

<!-- concept -->

La potencia de Snowflake no vuelve obsoleto el modelado. El almacenamiento columnar y los joins rápidos hacen que los esquemas estrella corran bien y que las tablas anchas cuesten poco por las columnas sin usar, pero los modelos claros siguen haciendo los datos comprensibles y consistentes. Normaliza donde importan la integridad y la reutilización, desnormaliza para el consumo.
La historia y los datos de referencia compartidos necesitan la misma disciplina que en cualquier lado: SCD tipo 2 con `MERGE` y dimensiones conformadas con un solo modelo dueño.

<!-- example -->

```sql
MERGE INTO dim_customer d
USING stg_customer s ON d.customer_id = s.customer_id AND d.is_current
WHEN MATCHED AND d.hash_diff <> s.hash_diff
  THEN UPDATE SET valid_to = s.loaded_at, is_current = FALSE;
INSERT INTO dim_customer (customer_id, segment, hash_diff, valid_from, valid_to, is_current)
SELECT s.customer_id, s.segment, s.hash_diff, s.loaded_at, '9999-12-31', TRUE
FROM stg_customer s
LEFT JOIN dim_customer d ON d.customer_id = s.customer_id AND d.is_current
WHERE d.customer_id IS NULL;
```

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

<!-- challenge -->

Cada equipo de mart construyó su propia tabla de clientes con reglas de segmento un poco distintas. ¿Cómo las consolidas?

<!-- solution -->

Crea una `dim_customer` conformada con un solo modelo dueño (con historia SCD si hace falta y reglas de segmento acordadas), haz que todos los marts referencien sus llaves sustitutas y depreca las copias locales.

<!-- takeaways -->

- Los esquemas estrella siguen ayudando a entender y a ser consistentes.
- Normaliza por integridad; desnormaliza para el consumo.
- SCD2 con `MERGE`; conforma las dimensiones compartidas.

<!-- unit: Herramientas alrededor de Snowflake -->

<!-- goals -->

- Explicar cómo corre dbt sobre Snowflake.
- Integrar Spark con Snowflake.

<!-- concept -->

La mayoría de plataformas Snowflake lo combinan con otras herramientas. dbt es la capa de transformación común: los modelos compilan a SQL que corre en un warehouse de Snowflake, con configs propias de Snowflake para clustering, tablas transient y warehouse por modelo.
Spark se integra con un conector que lee y escribe tablas de Snowflake, empujando filtros y consultas hacia abajo, lo que sirve a equipos que procesan parte de los datos en Spark y los sirven desde Snowflake.

<!-- example -->

```sql
-- dbt model config for Snowflake
{{ config(materialized='incremental', unique_key='order_id',
          cluster_by=['order_date'], transient=false, snowflake_warehouse='wh_transform_l') }}
select * from {{ ref('stg_orders') }}
{% if is_incremental() %} where order_date >= dateadd(day, -3, current_date) {% endif %}
```

#### ¿Qué es la clasificación de datos?

Una función que analiza las columnas para detectar datos sensibles (correos, nombres, teléfonos, documentos de identidad) y sugiere o aplica etiquetas del sistema, que luego pueden guiar las políticas de enmascaramiento.

#### ¿Cómo se autentican los usuarios en Snowflake?

Con contraseñas más MFA (que Snowflake está volviendo obligatorio para el inicio de sesión con contraseña), SSO mediante proveedores de identidad SAML 2.0 (Okta, Entra ID), OAuth (de Snowflake o externo), autenticación con par de claves para los servicios, federación de identidades de carga de trabajo y tokens de acceso programático. Los usuarios de servicio deberían usar pares de claves u OAuth, no contraseñas.

<!-- challenge -->

Un modelo dbt pesado necesita un warehouse Large, pero el resto corre bien en Small. ¿Cómo evitas correr todo en Large?

<!-- solution -->

Pon `snowflake_warehouse` en la config de ese modelo apuntando al warehouse Large y deja el default del proyecto en Small, así solo el modelo pesado usa el cómputo más grande.

<!-- takeaways -->

- dbt compila modelos a SQL que corre en Snowflake.
- Las configs propias de Snowflake ajustan cada modelo.
- El conector de Spark lee y escribe con pushdown.

<!-- stage: Proteger y compartir datos -->

### Uso compartido de datos y colaboración

<!-- unit: Time Travel y Fail-safe -->

<!-- goals -->

- Consultar y restaurar datos pasados con Time Travel.
- Explicar el Fail-safe y fijar los periodos de retención.

<!-- concept -->

Como las micro-particiones son inmutables, Snowflake puede guardar versiones viejas a bajo costo. Time Travel te deja consultar una tabla tal como estaba, restaurarla o hacerle undrop dentro de un periodo de retención que tú fijas. Después, el Fail-safe mantiene recuperables las tablas permanentes una semana más, pero solo el soporte de Snowflake puede usarlo, para desastres.
La retención es una palanca de costo: una retención larga en tablas que cambian constantemente multiplica el almacenamiento.

<!-- example -->

```sql
SELECT COUNT(*) FROM sales.orders AT (OFFSET => -3600);                  -- an hour ago
INSERT INTO sales.orders
SELECT * FROM sales.orders BEFORE (STATEMENT => '01b8a0e3-0002-...');      -- before the bad DELETE
ALTER TABLE sales.orders SET DATA_RETENTION_TIME_IN_DAYS = 14;
```

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

<!-- challenge -->

Una tabla se borró y se recreó con el mismo nombre, y ahora `UNDROP TABLE orders` falla. ¿Por qué y cómo restauras la vieja?

<!-- solution -->

Existe un objeto con ese nombre, así que `UNDROP` no puede restaurar encima. Renombra primero la tabla nueva (`ALTER TABLE orders RENAME TO orders_new`) y luego `UNDROP TABLE orders`.

<!-- takeaways -->

- Time Travel consulta y restaura datos pasados.
- El Fail-safe es una red de desastre solo para soporte.
- La retención cuesta almacenamiento en tablas muy cambiantes.

<!-- unit: Clonación zero-copy -->

<!-- goals -->

- Clonar tablas, esquemas y bases al instante.
- Entender qué heredan los clones y clonar desde puntos en el tiempo.

<!-- concept -->

Clonar crea una copia completa apuntando a las mismas micro-particiones en lugar de copiarlas. Es instantáneo y no cuesta almacenamiento hasta que cambian la copia o el original. Eso vuelve baratos y rápidos los ambientes de desarrollo y pruebas de tamaño completo.
Los clones heredan datos y estructura, y a nivel de base o esquema sus objetos hijos, pero no todos los privilegios; y combinados con Time Travel pueden capturar una tabla tal como estaba antes de un problema.

<!-- example -->

```sql
CREATE DATABASE analytics_dev CLONE analytics;                                 -- instant
CREATE TABLE sales.orders_before_fix CLONE sales.orders AT (TIMESTAMP => '2026-10-17 08:00:00'::TIMESTAMP_TZ);
GRANT USAGE ON DATABASE analytics_dev TO ROLE developer;
```

#### ¿Por qué ACCOUNTADMIN no debe ser el rol por defecto de nadie?

Tiene poder ilimitado, así que los errores o las sesiones comprometidas son catastróficos. Concédelo a pocos administradores con MFA, nunca lo uses para el trabajo diario ni para cuentas de servicio, y crea los objetos con SYSADMIN o roles propios.

#### ¿Qué son los roles secundarios?

`USE SECONDARY ROLES ALL` permite que una sesión use para las consultas los privilegios de todos los roles concedidos (el rol primario sigue siendo el propietario de los objetos creados), lo que simplifica el trabajo de quien tiene varios roles.

#### ¿Qué son las external access integrations?

Objetos que permiten a las UDF y procedimientos llamar a endpoints de red externos, controlados por network rules que listan los hosts permitidos y objetos secret para las credenciales.

#### ¿Qué es Secure Data Sharing?

Compartir datos vivos de solo lectura de una cuenta con otra sin copiarlos: el proveedor crea un share con bases de datos, esquemas, tablas y vistas seguras, y el consumidor crea una base de datos a partir de él. El consumidor paga el cómputo que usa; el proveedor paga el almacenamiento.

<!-- challenge -->

Los desarrolladores reciben un clon semanal de producción, pero contiene correos de clientes que no deberían ver. ¿Qué agregas?

<!-- solution -->

Políticas de enmascaramiento (idealmente basadas en tags) sobre las columnas PII, que revelen los valores solo a roles privilegiados; los clones conservan las políticas, así los desarrolladores ven datos enmascarados. Otra opción es enmascarar en un paso posterior al clon.

<!-- takeaways -->

- Los clones comparten micro-particiones; instantáneos y baratos.
- Solo divergen a medida que cambian los datos.
- Clona en un timestamp para capturar estados pasados.

### Snowpark, Python e IA

<!-- unit: RBAC y diseño de roles -->

<!-- goals -->

- Explicar el control de acceso por roles de Snowflake y los roles del sistema.
- Diseñar una jerarquía de roles y usar con cuidado el ownership, ACCOUNTADMIN y los roles secundarios.

<!-- concept -->

En Snowflake los privilegios se otorgan a roles, los roles a usuarios, y los roles pueden contener otros roles. Cada objeto tiene un rol dueño con control total. Los roles del sistema dividen la administración: uno para seguridad, otro para usuarios, otro para todo. Usar el rol más alto a diario vuelve cada error un desastre potencial.
Un diseño limpio separa los roles de acceso, que tienen privilegios sobre objetos, de los roles funcionales, que representan cargos y reciben los roles de acceso. Los roles secundarios dejan que una sesión use todos sus roles a la vez.

<!-- example -->

```sql
CREATE ROLE sales_read;   GRANT USAGE ON DATABASE sales TO ROLE sales_read;
GRANT USAGE ON SCHEMA sales.marts TO ROLE sales_read;
GRANT SELECT ON ALL TABLES IN SCHEMA sales.marts TO ROLE sales_read;
CREATE ROLE analyst_sales; GRANT ROLE sales_read TO ROLE analyst_sales;
GRANT ROLE analyst_sales TO ROLE sysadmin;     -- keep the hierarchy connected
GRANT ROLE analyst_sales TO USER ana;
```

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

<!-- challenge -->

Diez analistas tienen ACCOUNTADMIN como rol por defecto "para evitar errores de permisos". ¿Qué cambias?

<!-- solution -->

Crea roles funcionales con solo los roles de acceso que necesitan, ponlos como rol por defecto, restringe ACCOUNTADMIN a dos o tres administradores con MFA y corrige los grants faltantes en lugar de escalar privilegios.

<!-- takeaways -->

- Privilegios → roles → usuarios; los roles se anidan.
- Separa roles de acceso y roles funcionales.
- Mantén ACCOUNTADMIN escaso y protegido.

<!-- unit: Grants a escala -->

<!-- goals -->

- Usar future grants y database roles.
- Centralizar el control de grants con managed access schemas.

<!-- concept -->

Otorgar objeto por objeto se rompe en cuanto aparecen tablas nuevas. Los future grants aplican privilegios automáticamente a los objetos creados después en un esquema o una base. Los database roles acotan el acceso dentro de una base, y así también viaja el acceso fino con los shares.
Los managed access schemas centralizan quién puede otorgar: los dueños de objetos ya no pueden dar acceso por su cuenta, solo el dueño del esquema o un rol con gestión de grants.

<!-- example -->

```sql
GRANT SELECT ON FUTURE TABLES IN SCHEMA sales.marts TO ROLE sales_read;
CREATE DATABASE ROLE sales.reader;
GRANT SELECT ON ALL TABLES IN SCHEMA sales.marts TO DATABASE ROLE sales.reader;
CREATE SCHEMA sales.restricted WITH MANAGED ACCESS;
```

#### ¿Qué es un listing?

Una oferta empaquetada de un share o una Native App con metadatos, condiciones y analítica de uso, publicada de forma privada a cuentas elegidas o de forma pública en el Marketplace.

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

<!-- challenge -->

Cada tabla nueva en un esquema requiere un ticket para dar acceso a los analistas. ¿Qué configuras?

<!-- solution -->

Future grants sobre el esquema (`GRANT SELECT ON FUTURE TABLES IN SCHEMA ... TO ROLE ...`), para que el rol de acceso pueda leer automáticamente las tablas nuevas, manejado como código.

<!-- takeaways -->

- Los future grants cubren objetos creados después.
- Los database roles acotan el acceso dentro de una base.
- Los managed access schemas centralizan el otorgamiento.

<!-- unit: Protección de columnas y filas -->

<!-- goals -->

- Proteger columnas con políticas de enmascaramiento y basadas en tags, y filas con row access policies.
- Clasificar datos sensibles y usar secure views.

<!-- concept -->

Los grants a nivel de tabla son demasiado gruesos para los datos personales. Las políticas de enmascaramiento reescriben los valores de columna al consultar según quién pregunte; las row access policies deciden qué filas ve cada rol. Atar las políticas de enmascaramiento a tags escala la protección: etiquetas una columna como PII y queda enmascarada en todas partes.
La clasificación encuentra automáticamente las columnas sensibles, y las secure views y funciones ocultan su definición a los consumidores, lo que importa al compartir.

<!-- example -->

```sql
CREATE MASKING POLICY gov.mask_email AS (v STRING) RETURNS STRING ->
  CASE WHEN IS_ROLE_IN_SESSION('PII_READER') THEN v ELSE REGEXP_REPLACE(v, '.+@', '***@') END;
ALTER TAG gov.pii SET MASKING POLICY gov.mask_email;
CREATE ROW ACCESS POLICY gov.by_country AS (country STRING) RETURNS BOOLEAN ->
  EXISTS (SELECT 1 FROM gov.role_countries r
          WHERE r.country = country AND IS_ROLE_IN_SESSION(r.role_name));
ALTER TABLE sales.customers ADD ROW ACCESS POLICY gov.by_country ON (country);
```

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

<!-- challenge -->

Siguen apareciendo tablas nuevas con correos, y cada vez alguien olvida agregar una política de enmascaramiento. ¿Cómo vuelves automática la protección?

<!-- solution -->

Usa enmascaramiento basado en tags: ata la política a un tag `pii`, corre la clasificación (o etiqueta en las plantillas de tablas) para que las columnas de correo reciban el tag, y toda columna etiquetada queda enmascarada sin trabajo por tabla.

<!-- takeaways -->

- Las políticas de enmascaramiento protegen columnas al consultar.
- Las row access policies filtran filas por rol.
- Tags y clasificación escalan la protección.

<!-- unit: Autenticación, red y auditoría -->

<!-- goals -->

- Proteger el inicio de sesión, el acceso de red y las llamadas externas.
- Explicar el cifrado y auditar el acceso con access history.

<!-- concept -->

Alrededor de los datos, Snowflake protege quién entra y qué sale. Los usuarios inician sesión con MFA, SSO o key pairs; las network policies limitan desde dónde llegan las conexiones; las external access integrations controlan a qué endpoints externos puede llamar el código.
El cifrado está siempre activo, en reposo y en tránsito. El access history registra qué columnas leyó y escribió cada consulta, lo que responde con precisión preguntas de auditoría y linaje.

<!-- example -->

```sql
CREATE NETWORK POLICY corp_only ALLOWED_IP_LIST = ('203.0.113.0/24');
ALTER USER etl_svc SET NETWORK_POLICY = corp_only;
SELECT query_start_time, user_name, direct_objects_accessed
FROM snowflake.account_usage.access_history
WHERE ARRAY_CONTAINS('SALES.PUBLIC.CUSTOMERS'::VARIANT,
      TRANSFORM(base_objects_accessed, o -> o:objectName))
ORDER BY query_start_time DESC LIMIT 20;
```

#### ¿Cómo llegan los paquetes Python a Snowflake?

Desde el canal Anaconda de Snowflake (listados en `PACKAGES`), desde wheels o zips subidos a un stage (`IMPORTS`), o mediante repositorios de artefactos que traen paquetes de PyPI.

#### ¿Cómo averiguas por qué una consulta es lenta?

Abre el Query Profile: mira los operadores más costosos, las particiones leídas frente al total (pruning), los bytes derramados (spill) al almacenamiento local y remoto, los joins que explotan (muchas más filas de salida que de entrada) y el tiempo en cola. `GET_QUERY_OPERATOR_STATS` da los mismos datos en SQL.

#### ¿Qué es el spilling y cómo se corrige?

Cuando un warehouse no tiene memoria suficiente para una operación, derrama datos al disco local y luego al almacenamiento remoto, que es mucho más lento. Se corrige con un warehouse más grande, procesando menos datos (mejores filtros, preagregación) o dividiendo la consulta.

#### ¿Qué causa un "join que explota"?

Un join sobre una clave que no es única, o condiciones de join incompletas, de modo que cada fila coincide con muchas y la salida se multiplica. Verifica la unicidad de las claves y que cada join tenga la condición completa.

#### ¿Cómo se mejora el pruning?

Filtrando por columnas correlacionadas con el orden de carga (fechas), añadiendo una clustering key en las tablas grandes filtradas por otras columnas, evitando envolver las columnas de filtro en funciones que impiden el pruning y filtrando lo antes posible.

<!-- challenge -->

Los auditores preguntan quién leyó la columna `customers.national_id` el último trimestre. ¿Dónde buscas?

<!-- solution -->

En `ACCOUNT_USAGE.ACCESS_HISTORY`, que lista las columnas a las que accedió cada consulta (objetos base y directos), filtrado por esa columna y rango de fechas, cruzado con el historial de consultas para los detalles.

<!-- takeaways -->

- MFA, SSO y key pairs para la autenticación.
- Network policies e integraciones controlan el tráfico.
- El access history registra el acceso por columna.

### Rendimiento

<!-- unit: Secure Data Sharing -->

<!-- goals -->

- Compartir datos en vivo con otras cuentas y con usuarios sin Snowflake.
- Compartir entre regiones y entender los límites de los consumidores.

<!-- concept -->

Compartir en Snowflake significa otorgar acceso, no enviar archivos. El proveedor agrega objetos a un share; el consumidor lo monta como una base de solo lectura y consulta datos en vivo con su propio cómputo. Sin copias, sin exportaciones, sin versiones desactualizadas.
Los socios sin Snowflake pueden usar reader accounts que paga el proveedor. Los consumidores en otras regiones necesitan replicación o listings que la manejen. Los consumidores pueden consultar pero no modificar los datos compartidos.

<!-- example -->

```sql
CREATE SECURE VIEW share_db.partner.v_sales AS
  SELECT order_date, region, product, revenue FROM marts.fct_sales WHERE partner_id = 42;
CREATE SHARE partner_42;
GRANT USAGE ON DATABASE share_db TO SHARE partner_42;
GRANT USAGE ON SCHEMA share_db.partner TO SHARE partner_42;
GRANT SELECT ON VIEW share_db.partner.v_sales TO SHARE partner_42;
ALTER SHARE partner_42 ADD ACCOUNTS = partnerorg.partner_account;
```

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

<!-- challenge -->

Un socio en otra región de nube necesita tus datos diarios de ventas. Un share directo falla. ¿Qué haces?

<!-- solution -->

Replica la base a una cuenta en la región del socio y comparte desde ahí, o publica un listing privado con cross-cloud auto-fulfillment, que se encarga de la replicación.

<!-- takeaways -->

- Los shares dan acceso en vivo y de solo lectura sin copias.
- Las reader accounts sirven a socios sin Snowflake.
- Compartir entre regiones necesita replicación o listings.

<!-- unit: Marketplace, clean rooms y apps -->

<!-- goals -->

- Describir los listings y el Snowflake Marketplace.
- Explicar los data clean rooms y las Native Apps.

<!-- concept -->

Compartir escala hasta volverse producto. Los listings empaquetan shares con descripciones, términos y analítica de uso, publicados en privado o en el Marketplace. Los clean rooms dejan que varias partes analicen datos combinados mientras cada una controla lo que se puede revelar, como el solapamiento de audiencias sin exponer listas de clientes.
Las Native Apps van más lejos: distribuyen código y datos juntos, que corren dentro de la cuenta del consumidor.

<!-- example -->

| Necesidad | Mecanismo |
|---|---|
| Ofrecer datos del clima a cualquier cliente | Listing en el Marketplace |
| Compartir un dataset con un socio, con términos | Listing privado |
| Medir el solapamiento de audiencia con un anunciante | Data clean room |
| Entregar una app analítica que corra en las cuentas de los clientes | Native App |

#### ¿Qué muestra `EXPLAIN` en Snowflake?

El plan lógico de una consulta sin ejecutarla: operadores, orden de los joins y particiones a leer (según los metadatos), útil para revisar el pruning antes de lanzar una consulta costosa.

#### ¿Cómo se acelera una consulta con `DISTINCT` sobre datos enormes?

Comprobando si de verdad hace falta deduplicar (a menudo un join multiplicó las filas), deduplicando antes y sobre menos columnas, usando `APPROX_COUNT_DISTINCT` (HyperLogLog) cuando basta una estimación, y usando un warehouse más grande si derrama.

#### ¿Para qué sirven las funciones aproximadas?

`APPROX_COUNT_DISTINCT`, `APPROX_PERCENTILE` y `APPROX_TOP_K` dan estimaciones con un error pequeño usando mucha menos memoria y tiempo, lo que sirve para dashboards y exploración sobre tablas muy grandes.

#### ¿Qué impulsa los costos de Snowflake?

El cómputo de los warehouses (de lejos lo más grande para la mayoría de los clientes), las funciones serverless (Snowpipe, clustering, vistas materializadas, search optimization, tasks, funciones de IA), el almacenamiento (incluidos Time Travel y Fail-safe), los servicios en la nube por encima del 10 % del cómputo y la transferencia de datos fuera de la región.

<!-- challenge -->

Un retailer y una marca quieren saber cuántos clientes comparten, sin que ninguno vea la lista de clientes del otro. ¿Qué encaja?

<!-- solution -->

Un data clean room: cada parte aporta identificadores hasheados y solo pueden correr consultas agregadas aprobadas (conteos de solapamiento por encima de un umbral), así no se revela ningún registro individual.

<!-- takeaways -->

- Los listings empaquetan shares como productos.
- Los clean rooms permiten análisis conjunto con control.
- Las Native Apps llevan código y datos a los consumidores.

<!-- stage: Operar Snowflake -->

### Gestión de costos

<!-- unit: Leer el Query Profile -->

<!-- goals -->

- Diagnosticar consultas lentas con el Query Profile y EXPLAIN.
- Arreglar spills, joins que explotan y DISTINCT costosos.

<!-- concept -->

El Query Profile muestra dónde gasta una consulta su tiempo y sus datos: los operadores más costosos, las particiones escaneadas frente al total, los bytes derramados y las filas producidas en cada paso. La mayoría de problemas se ven ahí de un vistazo.
Tres patrones se repiten: spill cuando falta memoria, joins que explotan cuando una clave no es única y las filas se multiplican, y `DISTINCT` usado para esconder duplicados que creó un mal join.

<!-- example -->

```text
Query Profile (most expensive nodes)
  Join [id = id]           48%   rows in: 2 M × 3 M   rows out: 1.8 B   ← exploding join
  TableScan ORDERS         31%   partitions 11,500 / 12,000             ← poor pruning
  Aggregate                12%   bytes spilled to local storage: 85 GB ← memory
```

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

<!-- challenge -->

El join de una consulta produce 600 veces más filas que su entrada más grande. ¿Qué revisas y cómo lo arreglas?

<!-- solution -->

Las claves del join: un lado no es único en la clave (o falta una condición), así que las filas se multiplican. Corrige el grano del join (deduplica o agrega ese lado antes, agrega la condición faltante) y quita cualquier `DISTINCT` que lo tape.

<!-- takeaways -->

- Empieza por los nodos más costosos del Query Profile.
- El spill pide más memoria o menos datos.
- Los joins que explotan vienen de claves no únicas.

<!-- unit: Poda y búsqueda -->

<!-- goals -->

- Mejorar la poda con filtros, clustering y cargas ordenadas.
- Usar el Search Optimization Service para búsquedas puntuales.

<!-- concept -->

La mayor parte del rendimiento de Snowflake viene de leer menos. Los filtros sobre columnas que siguen el orden de carga, normalmente fechas, podan bien; los filtros envueltos en funciones o sobre columnas sin clustering, no. Las clustering keys y cargar los datos ordenados por las columnas de filtro principales mejoran la poda en tablas grandes.
Para buscar una aguja en un pajar por un ID o un string, search optimization construye un camino de acceso que encuentra las pocas micro-particiones que coinciden sin reorganizar la tabla.

<!-- example -->

```sql
-- prunes poorly: function on the filter column
SELECT * FROM events WHERE TO_DATE(event_ts) = '2026-10-17';
-- prunes well: range on the raw column
SELECT * FROM events WHERE event_ts >= '2026-10-17' AND event_ts < '2026-10-18';
ALTER TABLE events ADD SEARCH OPTIMIZATION ON EQUALITY(customer_id);
```

#### ¿Cómo se reducen los costos de almacenamiento?

Usando tablas transitorias para staging y datos reconstruibles, acortando el Time Travel en las tablas con mucha rotación, borrando tablas sin uso y clones que divergieron, limpiando los archivos viejos de los stages y evitando guardar muchas copias completas en lugar de clones.

#### ¿Un warehouse más grande siempre es más caro?

No necesariamente. Si una consulta se paraleliza bien, duplicar el tamaño reduce a la mitad el tiempo con el doble de tarifa, así que el costo es parecido y el resultado llega antes. Es más caro cuando las consultas son pequeñas o no se paralelizan.

#### ¿Por qué es caro un warehouse que ejecuta una consulta de un segundo cada minuto?

Cada reanudación factura al menos 60 segundos, y el auto-suspend lo mantiene encendido durante el tiempo de inactividad configurado tras cada consulta. Una consulta por minuto puede dejarlo encendido todo el tiempo. Agrupa esas consultas, usa tasks serverless o un único warehouse pequeño compartido.

#### ¿Cómo funciona el ajuste de los servicios en la nube?

El uso de servicios en la nube es gratis hasta el 10 % del cómputo diario de los warehouses; solo se factura el exceso. Las operaciones intensivas en metadatos (muchas consultas diminutas, comandos `SHOW`, clones frecuentes) pueden superarlo.

<!-- challenge -->

Soporte busca clientes individuales por `email` en una tabla de eventos de 4 TB, y cada búsqueda escanea casi toda la tabla. ¿Qué agregas?

<!-- solution -->

Search optimization sobre la columna `email` (igualdad), que permite a las búsquedas puntuales saltarse casi todas las micro-particiones; hacer clustering por email saldría caro y ayudaría poco a otras consultas.

<!-- takeaways -->

- Filtra columnas crudas, no funciones de ellas.
- Agrupa u ordena las tablas grandes por los filtros principales.
- Search optimization sirve búsquedas puntuales.

<!-- unit: Escribir cargas eficientes -->

<!-- goals -->

- Evitar antipatrones comunes como SELECT * y el DML de una sola fila.
- Acelerar los MERGE grandes y usar funciones aproximadas.

<!-- concept -->

Snowflake premia el trabajo por conjuntos y castiga los hábitos de las bases orientadas a filas. Leer todas las columnas de tablas anchas desperdicia la organización columnar; insertar filas una a una crea muchas micro-particiones diminutas; cruzar por tipos que no coinciden impide la poda.
Los merges grandes necesitan la misma atención: limitar el destino con rangos de fechas o claves permite que Snowflake pode la mayor parte de la tabla. Las funciones aproximadas cambian un error mínimo por un ahorro enorme en conteos distintos y percentiles.

<!-- example -->

```sql
MERGE INTO sales.orders t
USING staging.orders_delta s
ON  t.order_id = s.order_id
AND t.order_date >= DATEADD(day, -7, CURRENT_DATE())     -- prune the 3 TB target
WHEN MATCHED THEN UPDATE SET amount = s.amount
WHEN NOT MATCHED THEN INSERT (order_id, order_date, amount) VALUES (s.order_id, s.order_date, s.amount);
SELECT APPROX_COUNT_DISTINCT(user_id) FROM events WHERE event_date >= '2026-10-01';
```

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

<!-- challenge -->

Una aplicación inserta 50.000 filas por minuto con sentencias `INSERT` de una fila, y las consultas sobre la tabla se vuelven más lentas. ¿Qué cambias?

<!-- solution -->

Agrupa las filas: escribe archivos de micro-lote y carga con `COPY`/Snowpipe, o usa Snowpipe Streaming. Los inserts de una fila crean muchas micro-particiones diminutas y desperdician cómputo por sentencia.

<!-- takeaways -->

- Selecciona solo las columnas necesarias.
- Agrupa las escrituras; evita el DML de una fila.
- Poda los destinos de MERGE con condiciones de rango.

### Operación y protección de datos

<!-- unit: Qué mueve el costo -->

<!-- goals -->

- Identificar los principales impulsores de costo de Snowflake.
- Razonar sobre el tamaño de warehouse, los mínimos al reanudar y el cobro de cloud services.

<!-- concept -->

En la mayoría de cuentas, el cómputo de los warehouses es la factura. Le siguen las funciones serverless, el almacenamiento y la transferencia de datos. El costo de cómputo depende menos del tamaño que del tiempo encendido: un warehouse más grande que termina antes puede costar lo mismo, mientras uno pequeño que se mantiene despierto con consultas diminutas frecuentes cuesta mucho más que su trabajo.
Dos detalles de cobro explican muchas sorpresas: cada reanudación cobra al menos un minuto, y los cloud services son gratis solo hasta una proporción del cómputo diario.

<!-- example -->

```text
query: 1 s, every minute, X-Small, auto-suspend 600 s
→ warehouse never suspends: 24 h × 1 credit/h = 24 credits/day for ~24 min of actual work
fix: batch the checks, use a serverless task, or a shared warehouse already running
```

#### ¿Cómo se generan alertas sobre problemas de datos dentro de Snowflake?

Con alerts (condiciones programadas que ejecutan una acción, como enviar un correo o una notificación por webhook), las data metric functions (monitoreo de calidad de datos de Horizon: nulos, duplicados, frescura, métricas propias) y las notificaciones de error de los tasks.

#### ¿Qué son las data metric functions?

Funciones (del sistema, como `NULL_COUNT`, `DUPLICATE_COUNT`, `FRESHNESS`, o propias) asociadas a tablas y ejecutadas según una programación, cuyos resultados se guardan para monitorear la calidad de los datos en el tiempo.

#### ¿Qué es la event table?

Una tabla especial que recoge los logs, trazas y métricas emitidos por UDF, procedimientos, Native Apps y Snowpark Container Services, para poder monitorear el código que corre dentro de Snowflake.

#### ¿Cómo se respaldan los datos de Snowflake?

Time Travel y Fail-safe cubren los errores recientes y los desastres; para una protección más larga, usa clones zero-copy programados, backups (conjuntos de copias inmutables en un momento dado, donde estén disponibles), replicación a otra región o descarga a almacenamiento en la nube.

<!-- challenge -->

Un script de monitoreo corre una consulta de un segundo cada dos minutos en su propio warehouse. ¿Cómo bajas su costo?

<!-- solution -->

Córrelo en un warehouse existente que ya esté encendido, baja su frecuencia, usa una serverless task o una alerta, o fija un auto-suspend muy corto; un warehouse dedicado paga mínimos y tiempo ocioso por segundos de trabajo.

<!-- takeaways -->

- El tiempo de warehouse domina el costo.
- Más grande y más rápido puede costar lo mismo.
- Las consultas diminutas frecuentes mantienen despiertos los warehouses.

<!-- unit: Monitorear y controlar el gasto -->

<!-- goals -->

- Seguir el consumo de créditos por warehouse, consulta y tag.
- Controlar el gasto con resource monitors y budgets.

<!-- concept -->

El control de costos empieza por la atribución. Las vistas de account usage muestran los créditos por warehouse y servicio serverless; el historial de consultas, con query tags, liga el gasto a jobs, equipos y herramientas. Resource monitors y budgets agregan límites: avisan y luego suspenden warehouses cuando se alcanzan las cuotas.
Cuando los costos saltan, los mismos datos responden por qué: qué warehouse, qué servicio, qué consultas cambiaron.

<!-- example -->

```sql
ALTER SESSION SET QUERY_TAG = 'dbt:marts_daily';
SELECT warehouse_name, SUM(credits_used) AS credits
FROM snowflake.account_usage.warehouse_metering_history
WHERE start_time >= DATEADD(month, -1, CURRENT_DATE())
GROUP BY 1 ORDER BY 2 DESC;
CREATE RESOURCE MONITOR rm_bi WITH CREDIT_QUOTA = 500
  TRIGGERS ON 80 PERCENT DO NOTIFY ON 100 PERCENT DO SUSPEND;
ALTER WAREHOUSE wh_bi SET RESOURCE_MONITOR = rm_bi;
```

#### ¿Cómo se despliega SQL de forma segura?

Versionando el SQL en Git, desplegando desde CI con un usuario de servicio (par de claves u OAuth), usando `CREATE OR ALTER` o herramientas de migración (schemachange, dbt, Terraform), probando primero sobre una base clonada y conservando scripts de reversión o apoyándose en Time Travel y clones.

#### ¿Sigue siendo útil el modelado en estrella en Snowflake?

Sí. Snowflake maneja bien los joins y el almacenamiento es barato, pero los esquemas en estrella siguen haciendo la analítica más sencilla, coherente y rápida para las herramientas de BI. Muchos equipos usan un enfoque por capas: raw, staging, intermedio y marts con hechos y dimensiones, a menudo construidos con dbt.

#### ¿Conviene normalizar o desnormalizar en Snowflake?

Normaliza donde importan la integridad y la reutilización (las entidades centrales), y desnormaliza para el consumo (marts anchos, una tabla grande para dashboards concretos). El almacenamiento columnar hace que las tablas anchas sean baratas de consultar cuando solo se leen algunas columnas.

#### ¿Cómo funciona dbt con Snowflake?

dbt compila los modelos a SQL y los ejecuta en un warehouse de Snowflake con el adaptador dbt-snowflake, que admite tablas, vistas, modelos incrementales (`merge`, `delete+insert`, `append`, `microbatch`), dynamic tables, tablas transitorias, query tags y configuraciones de clustering.

#### ¿Cómo se integran Spark y Snowflake?

Con el conector de Spark, que lee y escribe tablas de Snowflake con pushdown de consultas, o compartiendo tablas Iceberg a través de un catálogo para que Spark y Snowflake trabajen sobre los mismos archivos.

<!-- challenge -->

Finanzas quiere el costo mensual de Snowflake por equipo, pero los equipos comparten warehouses. ¿Cómo lo atribuyes?

<!-- solution -->

Fija query tags por equipo o herramienta (dbt, BI, notebooks) y reparte los créditos del warehouse según la participación de cada tag en el tiempo de ejecución del historial de consultas (`QUERY_ATTRIBUTION_HISTORY` donde exista), más warehouses separados para los equipos más grandes.

<!-- takeaways -->

- Atribuye créditos por warehouse, consulta y tag.
- Resource monitors y budgets imponen límites.
- Las vistas de uso explican los saltos de costo.

<!-- unit: Bajar costos -->

<!-- goals -->

- Bajar los costos de warehouse con dimensionamiento, suspensión y diseño de cargas.
- Bajar los costos de almacenamiento con tipos de tabla y retención.

<!-- concept -->

El ahorro en cómputo viene de no pagar tiempo ocioso ni desperdicio: dimensiona por carga, suspende rápido, consolida las cargas diminutas, procesa de forma incremental en lugar de reconstruir y deja trabajar a la caché.
El ahorro en almacenamiento viene más de la historia que de los datos: tablas transient para datos reconstruibles, Time Travel más corto en tablas muy cambiantes y borrar tablas sin uso y clones viejos que ya divergieron.

<!-- example -->

| Palanca | Ahorro típico |
|---|---|
| Auto-suspend de 60 s en warehouses de ETL | Horas ociosas eliminadas |
| Modelos incrementales en vez de reconstrucciones completas | La mayor parte del cómputo de transformación |
| Tablas de staging transient | Almacenamiento de Fail-safe |
| Retención de 1 día en tablas muy cambiantes | Almacenamiento de Time Travel |

#### ¿Cómo se implementa una SCD tipo 2 en Snowflake?

Con un `MERGE` que cierra las filas vigentes que cambiaron e inserta las nuevas versiones (a menudo dos sentencias o el truco de la unión), con streams y tasks para el procesamiento incremental, o con los snapshots de dbt, que lo manejan automáticamente.

#### ¿Qué es el enfoque "one big table" y cuándo encaja?

Una tabla ancha y desnormalizada con todo lo que necesita un caso de uso, rápida de consultar en un motor columnar y sencilla para BI. Encaja en casos de uso estables y concretos; para la analítica general, los esquemas en estrella siguen siendo más flexibles y coherentes.

<!-- challenge -->

Los costos de almacenamiento se duplicaron aunque los datos activos crecieron 10 %. ¿Qué revisas?

<!-- solution -->

Los bytes de Time Travel y Fail-safe por tabla (`TABLE_STORAGE_METRICS`): tablas muy cambiantes con retención larga, tablas de staging permanentes y clones cuyos datos divergieron. Acorta la retención y convierte a transient las tablas reconstruibles.

<!-- takeaways -->

- Paga por trabajo, no por ocio: dimensiona, suspende, consolida.
- Procesa de forma incremental.
- El almacenamiento histórico suele dominar el costo de almacenamiento.

### Modelado e integración

<!-- unit: Monitoreo y calidad de datos -->

<!-- goals -->

- Elegir entre ACCOUNT_USAGE e INFORMATION_SCHEMA.
- Monitorear la calidad de datos con alertas, data metric functions y la event table.

<!-- concept -->

Dos familias de vistas describen una cuenta: `INFORMATION_SCHEMA` por base, en tiempo real pero con poca historia; `ACCOUNT_USAGE` para toda la cuenta, un año de historia con algo de retraso. Las consultas de monitoreo eligen según frescura y alcance.
La calidad de datos también corre dentro de Snowflake: las data metric functions miden frescura, nulos o duplicados según un horario, las alertas evalúan condiciones y avisan, y la event table junta los logs del código que corre en la cuenta.

<!-- example -->

```sql
ALTER TABLE sales.orders SET DATA_METRIC_SCHEDULE = '60 MINUTE';
ALTER TABLE sales.orders ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.DUPLICATE_COUNT ON (order_id);
CREATE ALERT ops.orders_stale
  WAREHOUSE = wh_ops SCHEDULE = '30 MINUTE'
  IF (EXISTS (SELECT 1 FROM sales.orders HAVING MAX(loaded_at) < DATEADD(hour, -2, CURRENT_TIMESTAMP())))
  THEN CALL SYSTEM$SEND_EMAIL('ops_email', 'data@example.com', 'orders stale', 'No load in 2 hours');
```

#### ¿Cómo se modelan datos de referencia que cambian lentamente y que usan muchos marts?

Como dimensiones conformadas con un único modelo responsable, con claves sustitutas e historial SCD si hace falta, referenciadas por todos los marts para que todos los reportes usen las mismas definiciones.

#### Diseña un pipeline de ingesta desde eventos de S3 hasta tablas de reportes en Snowflake.

Creo una storage integration y un stage externo sobre el prefijo de S3, un Snowpipe con auto-ingest a partir de las notificaciones de eventos de S3 hacia una tabla raw tipada o con `VARIANT`, un stream sobre la tabla raw, y dynamic tables (o tasks con `MERGE`) que construyen las tablas limpias y agregadas con la frescura necesaria. Añado data metric functions, alertas y resource monitors, y lo administro todo como código.

#### Un warehouse de dashboards hace cola cada lunes a las 9 a. m. ¿Qué haces?

Lo convierto en un warehouse multi-cluster con suficientes clusters máximos (política Standard para usuarios interactivos), reviso si las consultas lentas se pueden optimizar o servir desde agregados, y separo las otras cargas que usan el mismo warehouse a esa hora.

#### Una consulta lee el 98 % de las particiones de una tabla de 5 TB aunque filtra por `customer_id`. ¿Cómo lo corriges?

La tabla no está agrupada por `customer_id`. Para búsquedas puntuales, activo search optimization en esa columna; para filtros por rango frecuentes, añado una clustering key (quizá combinada con la fecha); si no, replanteo la consulta o creo una tabla preagregada.

<!-- challenge -->

Un dashboard de costos construido sobre `ACCOUNT_USAGE` no muestra las consultas de la última hora. ¿Está roto?

<!-- solution -->

No: las vistas de `ACCOUNT_USAGE` tienen latencia (a menudo de hasta unas horas). Para revisiones casi en tiempo real usa las funciones de tabla de `INFORMATION_SCHEMA`, aceptando su historia más corta y su alcance por base.

<!-- takeaways -->

- `ACCOUNT_USAGE`: toda la cuenta, historia larga, con retraso.
- `INFORMATION_SCHEMA`: por base, en tiempo real.
- DMFs y alertas monitorean la calidad dentro de Snowflake.

<!-- unit: Replicación y backups -->

<!-- goals -->

- Replicar bases y hacer failover entre cuentas.
- Planear backups más allá del Time Travel y el Fail-safe.

<!-- concept -->

Snowflake ya protege contra fallas de hardware y de zona, y el Time Travel cubre los errores recientes. Las caídas regionales y la protección de largo plazo necesitan más. La replicación copia bases, y con replication groups también usuarios, roles y warehouses, a cuentas en otras regiones o nubes; los failover groups y el client redirect permiten que las aplicaciones pasen a la secundaria.
Para backups, los clones, las copias replicadas y las descargas a tu propio almacenamiento cubren lo que no alcanzan los periodos de retención.

<!-- example -->

```sql
CREATE FAILOVER GROUP fg_prod
  OBJECT_TYPES = DATABASES, ROLES, USERS, WAREHOUSES
  ALLOWED_DATABASES = analytics, sales
  ALLOWED_ACCOUNTS = myorg.prod_dr
  REPLICATION_SCHEDULE = '10 MINUTE';
-- in the DR account, during a disaster:
ALTER FAILOVER GROUP fg_prod PRIMARY;
```

#### Alguien ejecutó `DELETE FROM orders` sin `WHERE` hace una hora. ¿Cómo lo recuperas?

Con Time Travel: vuelvo a insertar las filas desde `orders AT (OFFSET => -3600)` o `BEFORE (STATEMENT => '<query id>')`, o clono la tabla en ese momento y la intercambio con `ALTER TABLE … SWAP WITH`. Después restrinjo los permisos de borrado en las tablas de producción.

#### Los costos subieron un 40 % este mes. ¿Cómo lo investigas?

Comparo `WAREHOUSE_METERING_HISTORY` y la medición serverless por servicio y warehouse, encuentro los warehouses y query tags que crecieron, miro `QUERY_ATTRIBUTION_HISTORY` para las consultas más caras, y reviso si hay warehouses que dejaron de suspenderse, dynamic tables nuevas con un lag muy corto, reagrupamiento en tablas con mucha rotación o refrescos completos.

#### Los analistas de cada país solo deben ver sus filas y no deben ver los correos. ¿Cómo?

Una row access policy en las tablas con una tabla de correspondencia entre roles y países, y una política de enmascaramiento (o enmascaramiento por etiquetas) en las columnas de correo que solo revela los valores a un rol privilegiado. Los analistas reciben roles funcionales asociados a su país.

<!-- challenge -->

Cumplimiento exige una copia mensual de las tablas de finanzas guardada 7 años. El Time Travel llega como máximo a 90 días. ¿Qué haces?

<!-- solution -->

Guarda clones zero-copy mensuales (nombrados por mes) del esquema de finanzas, o descarga snapshots mensuales a Parquet en tu propio almacenamiento con object lock; maneja la retención como código.

<!-- takeaways -->

- La replicación copia bases y objetos de cuenta.
- Failover groups y client redirect permiten DR.
- Los backups de largo plazo necesitan clones o descargas.

<!-- unit: Objetos como código -->

<!-- goals -->

- Manejar objetos de Snowflake con Terraform, la integración con Git y SQL declarativo.
- Desplegar cambios de SQL con seguridad mediante CI.

<!-- concept -->

Crear objetos a punta de clics no escala ni se audita bien. Los objetos de nivel de cuenta, como warehouses, roles y grants, encajan en Terraform; los objetos de base de datos, en dbt, herramientas de migración o scripts declarativos `CREATE OR ALTER`. Un objeto Git repository permite que Snowflake lea el código directo de tu repositorio.
Los despliegues siguen entonces la práctica de software: cambios revisados en Git, aplicados por CI con un usuario de servicio y probados en un ambiente clonado antes de producción.

<!-- example -->

```hcl
resource "snowflake_warehouse" "transform" {
  name           = "WH_TRANSFORM"
  warehouse_size = "SMALL"
  auto_suspend   = 60
  auto_resume    = true
}
resource "snowflake_grant_account_role" "analyst_to_sysadmin" {
  role_name        = "ANALYST_SALES"
  parent_role_name = "SYSADMIN"
}
```

#### ¿Cómo migrarías un data warehouse on-premises a Snowflake?

Inventariando los objetos, las cargas y las dependencias; traduciendo el DDL y el SQL (SnowConvert ayuda); moviendo el histórico por almacenamiento en la nube y `COPY`; montando la carga incremental; reconstruyendo las transformaciones (a menudo en dbt); recreando la seguridad con roles y políticas; validando con conteos de filas, checksums y comparaciones de reportes; ejecutando ambos en paralelo antes del corte; y luego ajustando warehouses y costos.

#### Un equipo quiere procesar 2 TB diarios de logs JSON. ¿Cómo los cargas y modelas?

Dejo en S3 archivos comprimidos de unos 100–250 MB, los cargo con Snowpipe o con `COPY` programado en una columna `VARIANT` de una tabla raw transitoria, extraigo los campos más usados a columnas tipadas en una tabla limpia agrupada por fecha del evento, y agrego en marts. Mantengo los datos raw poco tiempo si se pueden volver a cargar desde S3.

#### ¿Cómo le explicas el valor de Snowflake a una persona de negocio?

Un único lugar gobernado para los datos de la empresa que escala al instante para cualquier número de usuarios, no cuesta nada cuando no se usa y permite que los equipos compartan y analicen las mismas cifras sin administrar servidores.

<!-- challenge -->

Warehouses y grants difieren entre dev y prod porque la gente los cambió a mano. ¿Cómo los pones bajo control?

<!-- solution -->

Importa los objetos existentes al state de Terraform, defínelos como código con variables por ambiente, revisa el plan y aplica solo por CI; quita los derechos de cambio manual a los administradores salvo para emergencias.

<!-- takeaways -->

- Terraform para objetos de cuenta; dbt o migraciones para objetos de base.
- Despliega por CI con usuarios de servicio.
- Prueba los cambios primero en clones.

<!-- stage: Juntarlo todo -->

### Escenarios

<!-- unit: Diseñar pipelines de ingesta -->

<!-- goals -->

- Diseñar pipelines desde almacenamiento en la nube y logs hasta tablas de reportes.
- Combinar carga, manejo de semiestructurados, transformación y monitoreo.

<!-- concept -->

Las preguntas de diseño de ingesta conectan las secciones. Una buena respuesta sigue a los archivos: cómo accede Snowflake a ellos, cómo y con qué frecuencia se cargan, dónde aterrizan los datos crudos, cómo se deduplican, tipan y modelan, cómo se mantienen incrementales las transformaciones y qué se monitorea. Nombrar decisiones de costo, tamaño de archivos, warehouse por carga, refrescos incrementales, muestra experiencia de producción.

<!-- example -->

```text
S3 (Firehose, ~128 MB gz) ─► storage integration + stage ─► Snowpipe (auto-ingest)
  ─► raw.events (VARIANT + metadata) ─► dynamic table silver.events (typed, deduped, lag 15 min)
  ─► gold marts (dbt or dynamic tables) ─► BI warehouse (multi-cluster)
  monitoring: pipe status, DMFs freshness/duplicates, alerts, resource monitor
```

#### Un `MERGE` nocturno sobre una tabla de 3 TB tarda horas. ¿Qué revisas?

Si el destino se poda (añadir un filtro de fecha o rango de claves en la cláusula `ON`, agrupar por la clave del merge), si el origen tiene duplicados o es mucho más grande que los cambios, el tamaño del warehouse y el spilling, y si encaja mejor un enfoque incremental (streams, `delete+insert` sobre las particiones recientes).

#### Un Snowpipe a veces carga filas duplicadas. ¿Por qué y qué haces?

Los mismos datos llegaron en archivos distintos (reintentos del productor, archivos renombrados), o se recargaron archivos con `FORCE`. Hago que los productores escriban nombres de archivo deterministas, deduplico después por una clave de negocio con `QUALIFY` y mantengo la capa raw como solo inserción, con los metadatos del archivo para rastrear.

<!-- challenge -->

El equipo de la fuente avisa que los archivos pueden reenviarse tras fallas. ¿En qué punto de tu diseño manejas los duplicados?

<!-- solution -->

Deja lo crudo tal como se cargó (con nombre de archivo y hora de carga) y deduplica en silver por el ID del evento, conservando el más reciente por hora de carga (`QUALIFY ROW_NUMBER() ... = 1`), así los archivos reenviados no crean filas de negocio duplicadas.

<!-- takeaways -->

- Sigue a los archivos desde el almacenamiento hasta los reportes.
- Lo crudo guarda todo; silver deduplica y tipa.
- Diseña para reenvíos, costo y monitoreo.

<!-- unit: Migrar a Snowflake -->

<!-- goals -->

- Planear una migración desde un warehouse on premises.
- Ordenar traducción, movimiento de datos, validación y corte.

<!-- concept -->

Las migraciones de warehouse fallan por sorpresas: dependencias olvidadas, SQL que se traduce con otra semántica, consumidores que nadie listó. Un buen plan inventaría objetos, jobs y usuarios, traduce DDL y SQL con herramientas y revisión, mueve la historia una vez y los cambios de forma incremental, y luego corre el sistema viejo y el nuevo en paralelo comparando resultados antes de cambiar a los consumidores. Repensar el diseño, no solo copiarlo, es donde está la mayor parte del valor.

<!-- example -->

| Fase | Actividades |
|---|---|
| Evaluar | Inventariar tablas, jobs, reportes, usuarios; estadísticas de uso |
| Traducir | DDL y SQL (SnowConvert), procedimientos, tipos de datos |
| Mover | Carga masiva histórica por stages; CDC para los cambios |
| Validar | Conteos de filas, checksums, comparación de reportes |
| Cortar | Reapuntar BI y jobs; retirar el sistema viejo |

#### ¿Cómo le das a un socio acceso a un dataset seleccionado sin copiarlo?

Creo vistas seguras sobre las tablas seleccionadas, las pongo en un share (o en un listing privado) y añado la cuenta del socio como consumidora; si no tiene cuenta de Snowflake, creo una reader account. Uso row access policies o vistas separadas para limitar lo que ve.

<!-- challenge -->

Tras la migración, unos pocos reportes mensuales difieren del sistema viejo por montos pequeños. ¿Cuáles son las causas probables?

<!-- solution -->

Diferencias de tipos y redondeo (precisión numérica, float frente a decimal), manejo de zonas horarias en timestamps, semántica de NULL en joins y agregados, y funciones SQL traducidas con otro comportamiento. Compara por día y por clave para ubicarlas.

<!-- takeaways -->

- Inventaría antes de mover nada.
- Traduce y revisa la semántica del SQL.
- Valida en paralelo antes del corte.
