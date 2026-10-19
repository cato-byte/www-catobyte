## Guía de estudio de Arquitectura de datos

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de arquitectura de datos: unas 200 preguntas](../../images/data_architecture_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre arquitectura de datos: principios, elección de almacenamiento y bases de datos, compromisos de los sistemas distribuidos, enfoques de modelado (Inmon, Kimball, Data Vault), lakes, lakehouses y el patrón medallion, arquitecturas batch y streaming (Lambda, Kappa), microservicios y datos orientados a eventos, data mesh y data fabric, gobierno, seguridad, confiabilidad, costos y arquitectura para IA. Complementa la guía de data warehousing, que profundiza en el modelado dimensional.

La guía sigue una ruta de aprendizaje en seis etapas. Cada sección se divide en unidades cortas: objetivos de aprendizaje, una explicación del concepto y un ejemplo resuelto, luego preguntas (primero de memoria, después de aplicación), un reto práctico e ideas clave. Para **aprender**, lee cada unidad de principio a fin. Para **repasar**, cambia al modo repaso o usa "Ir a las preguntas", marca las respuestas que quieras volver a ver y prueba un repaso mixto entre secciones.

<!-- QA -->
<!-- stage: Fundamentos -->

### Principios

<!-- unit: Qué es la arquitectura de datos -->

<!-- goals -->

- Explicar qué cubre la arquitectura de datos y qué hace un arquitecto de datos.
- Nombrar las capas de una plataforma de datos moderna.

<!-- concept -->

Toda empresa ya tiene una arquitectura de datos, diseñada o no: los datos vienen de algún lado, se guardan en algún lado, cambian de forma y llegan a las personas. La arquitectura de datos es la versión deliberada de eso: un plano de estructuras, estándares y decisiones tecnológicas que permite a muchos equipos construir sin contradecirse.
Los ingenieros construyen pipelines dentro de ese plano; los arquitectos deciden su forma, sopesando requisitos, costo y cambio a lo largo de años, no de sprints.

<!-- example -->

```text
sources ─► ingestion (batch, CDC, streams) ─► storage (lake, warehouse)
        ─► processing (transform, model) ─► serving (BI, APIs, ML, reverse ETL)
        across all layers: governance, security, metadata, observability
```

#### ¿Qué es la arquitectura de datos?

El conjunto de decisiones, modelos, políticas y estándares que definen cómo se recogen, guardan, integran, procesan, gobiernan y consumen los datos en una organización, y los sistemas que los implementan.

#### ¿Qué hace un arquitecto de datos?

Traduce las necesidades del negocio en estructuras y plataformas de datos: elige tecnologías y patrones, diseña modelos y flujos, define estándares de calidad, seguridad y gobierno, documenta las decisiones y orienta a los equipos para que los sistemas encajen y evolucionen sin rehacer todo constantemente.

#### ¿Cuáles son las capas principales de una arquitectura de datos moderna?

Fuentes, ingesta (batch, CDC, streaming), almacenamiento (lake, warehouse, almacenes operativos), procesamiento y transformación, servicio (BI, APIs, features de ML, reverse ETL), y transversalmente orquestación, gobierno, seguridad, observabilidad y metadatos.

#### ¿Cuáles son buenos principios de arquitectura de datos?

Tratar los datos como un producto con responsables; diseñar para el cambio (bajo acoplamiento, contratos); tener una única fuente de verdad por entidad; guardar los datos en bruto de forma inmutable y reprocesar cuando cambia la lógica; asegurar y gobernar por defecto; automatizarlo todo como código; optimizar para las preguntas que la gente hace; y preferir componentes simples y administrados cuando cumplen los requisitos.

#### ¿Qué diferencia hay entre los modelos de datos conceptual, lógico y físico?

Los modelos conceptuales muestran las entidades de negocio y sus relaciones para las partes interesadas; los lógicos añaden atributos, claves y normalización sin detalles tecnológicos; los físicos los implementan en una base concreta con tipos, índices, particiones y decisiones de almacenamiento.

<!-- challenge -->

Un gerente pregunta para qué la empresa necesita un arquitecto de datos si ya tiene cinco ingenieros de datos. Da dos respuestas en términos de negocio.

<!-- solution -->

Sin un plano compartido, cada ingeniero resuelve los problemas a su manera, y crecen los costos, los datos duplicados y las cifras contradictorias. Un arquitecto fija estándares y toma las decisiones tecnológicas de largo plazo para que la plataforma siga siendo asequible y confiable al crecer.

<!-- takeaways -->

- La arquitectura de datos es el plano; la ingeniería construye dentro de él.
- Capas: fuentes, ingesta, almacenamiento, procesamiento, consumo.
- Gobierno, seguridad y metadatos atraviesan todas las capas.

<!-- unit: Requisitos y modelos -->

<!-- goals -->

- Levantar requisitos funcionales y no funcionales.
- Usar modelos conceptuales, lógicos y físicos, y registrar decisiones en ADRs.

<!-- concept -->

Una buena arquitectura empieza por preguntas, no por herramientas. Los requisitos funcionales dicen qué datos y salidas se necesitan; los no funcionales (frescura, volumen, disponibilidad, costo, cumplimiento) suelen decidir el diseño, porque dos sistemas que producen el mismo reporte pueden diferir cien veces en costo.
Los modelos traducen los requisitos en capas, de entidades de negocio para los interesados a tablas exactas para los ingenieros. Los registros de decisiones guardan el razonamiento, para que el siguiente equipo sepa el porqué y no solo el qué.

<!-- example -->

```markdown
# ADR-014: Use Iceberg for curated lake tables
Context: Athena, Spark and Snowflake must read the same tables.
Options: Delta, Iceberg, plain Parquet.
Decision: Iceberg (broadest multi-engine support, catalog integration).
Consequences: compaction jobs required; team training on Iceberg maintenance.
```

#### ¿Qué son los requisitos funcionales y no funcionales en arquitectura de datos?

Funcionales: qué datos, transformaciones, métricas y salidas se necesitan. No funcionales: latencia, frescura, volumen, escalabilidad, disponibilidad, durabilidad, seguridad, cumplimiento, costo y mantenibilidad, que a menudo determinan la elección de tecnologías.

#### ¿Qué es un registro de decisión de arquitectura (ADR)?

Un documento corto que recoge una decisión importante: contexto, opciones consideradas, decisión, consecuencias y estado. Los ADR hacen visible el razonamiento y evitan que los equipos vuelvan a discutir lo ya decidido; se guardan junto al código.

#### ¿Qué es la deuda técnica en las plataformas de datos?

Atajos que encarecen los cambios futuros: pipelines sin documentar, lógica duplicada, configuración escrita en el código, pruebas faltantes, tablas sin responsable, arreglos rápidos en producción. Se acumula en silencio y aparece como incidentes, entregas lentas y desconfianza en las cifras.

<!-- challenge -->

Los interesados piden "dashboards de ventas en tiempo real". ¿Qué preguntas no funcionales haces antes de diseñar nada?

<!-- solution -->

Qué tan fresco es suficiente (segundos, minutos, cada hora), cuántos usuarios, qué decisiones cambian con datos más frescos, costo aceptable y necesidades de disponibilidad. Las respuestas deciden entre streaming y batch frecuente.

<!-- takeaways -->

- Los requisitos no funcionales suelen decidir diseño y costo.
- Modelos conceptuales, lógicos y físicos sirven a lectores distintos.
- Los ADRs preservan el razonamiento de las decisiones.

<!-- unit: Principios de diseño -->

<!-- goals -->

- Aplicar principios clave: datos como producto, datos crudos inmutables, responsabilidad única.
- Diseñar para el cambio y manejar la deuda técnica.

<!-- concept -->

Unos pocos principios hacen que las plataformas duren. Los datasets con dueños y garantías se confían y se reutilizan. Conservar los datos crudos sin cambios permite reprocesar cuando cambian la lógica o aparecen bugs. Los pipelines con una sola tarea son más fáciles de probar y reemplazar.
El hilo común es el cambio: requisitos, fuentes y herramientas van a cambiar. Las arquitecturas que lo asumen, con bajo acoplamiento, contratos y chequeos automáticos, absorben el cambio; las que no, acumulan deuda que frena cada proyecto futuro.

<!-- example -->

| Principio | Práctica |
|---|---|
| Datos como producto | Dueño, esquema, SLA y docs por dataset |
| Crudo inmutable | Landing solo de anexado; nunca editar archivos fuente |
| Responsabilidad única | Un pipeline por fuente; un modelo por concepto |
| Evolutiva | Contratos y pruebas como fitness functions |

#### ¿Qué significa "construir o comprar" en las plataformas de datos?

Elegir entre construir componentes propios (más control, más mantenimiento) y usar servicios administrados o proveedores (más rápido, menos control, costo recurrente, dependencia). La mayoría de los equipos compra las capacidades estándar (almacenamiento, warehouse, conectores) y construye lo que los diferencia.

#### ¿Qué es la dependencia de un proveedor (vendor lock-in) y cómo se limita?

Depender de los formatos o APIs propietarios de un proveedor, lo que encarece cambiar. Se limita con formatos abiertos (Parquet, Iceberg, Delta), SQL estándar, infraestructura como código, abstracciones donde sean baratas y planes de salida para los componentes críticos, aceptando cierta dependencia donde el valor es alto.

#### ¿Qué son los "datos como producto"?

Gestionar los datasets como productos: un responsable claro, propósito y esquema documentados, garantías de calidad y SLA, facilidad para descubrirlos, versionado y retroalimentación de los consumidores. Es una idea central del data mesh, pero útil en cualquier arquitectura.

#### ¿Qué compromisos hay entre centralizar y descentralizar?

Las plataformas y equipos centralizados dan coherencia, economías de escala y un gobierno fuerte, pero se convierten en cuellos de botella. La propiedad descentralizada por dominio escala la entrega y acerca la experiencia a los datos, pero arriesga incoherencias y esfuerzo duplicado; el gobierno federado los equilibra.

#### ¿Qué diferencia hay entre arquitectura de datos e ingeniería de datos?

La arquitectura de datos define el plano: estructuras, estándares, elección de tecnologías y cómo encajan los componentes. La ingeniería de datos construye y opera los pipelines y plataformas que lo implementan. En la práctica los roles se solapan, y los ingenieros sénior toman muchas decisiones de arquitectura.

#### ¿Cómo se evalúa una tecnología nueva para la plataforma?

Partiendo de los requisitos, comparando unas pocas opciones con criterios (encaje, rendimiento, costo, habilidades, ecosistema, soporte, seguridad, dependencia), haciendo una prueba de concepto con cargas reales, considerando el costo total de propiedad y el costo de salida, y registrando la decisión en un ADR.

<!-- challenge -->

Un equipo sobrescribe los archivos fuente crudos después de limpiarlos para ahorrar almacenamiento. Seis meses después se encuentra un bug en la limpieza. ¿Cuál es la consecuencia y la solución?

<!-- solution -->

La historia no se puede reprocesar, porque las entradas originales ya no existen. Mantén los datos crudos inmutables (barato con niveles de almacenamiento y reglas de lifecycle) y escribe los datos limpios en una capa aparte.

<!-- takeaways -->

- Los datasets necesitan dueños y garantías.
- Los datos crudos inmutables permiten reprocesar y auditar.
- Diseña para el cambio; registra y paga la deuda.

<!-- unit: Elegir tecnología -->

<!-- goals -->

- Decidir entre construir y comprar, y limitar el lock-in.
- Evaluar tecnologías por encaje y costo total de propiedad.

<!-- concept -->

Las decisiones tecnológicas son apuestas de largo plazo. Los servicios administrados cambian control por velocidad; los formatos abiertos e interfaces estándar conservan la opción de cambiar después. Centralizar da consistencia, descentralizar da velocidad, y la mayoría de organizaciones necesita algo de ambos.
Comparar opciones solo por precio de licencia engaña. El costo total incluye personas para operarlo, migraciones y el costo de quedar atrapado, así que las evaluaciones deben probar cargas reales contra criterios explícitos.

<!-- example -->

| Criterio | Opción A (administrada) | Opción B (OSS autoalojado) |
|---|---|---|
| Tiempo al primer valor | Semanas | Meses |
| Costo de operación (personas) | Bajo | Alto |
| Lock-in | Medio (los formatos abiertos ayudan) | Bajo |
| TCO a 3 años | ... | ... |

#### ¿Qué es el costo total de propiedad (TCO)?

El costo completo de una solución en el tiempo: licencias o consumo en la nube, infraestructura, personas para construirla y operarla, formación, migración, soporte y el costo de las caídas, no solo el precio por unidad de cómputo.

#### ¿Qué es la "arquitectura evolutiva"?

Diseñar los sistemas para que cambien de forma incremental con salvaguardas (fitness functions como pruebas sobre latencia, costo o acoplamiento), prefiriendo decisiones reversibles y pasos pequeños frente a grandes diseños iniciales.

#### ¿Por qué los datos en bruto deben ser inmutables?

Los datos en bruto inmutables permiten reprocesar el historial cuando cambian la lógica o se corrigen errores, auditar lo que enviaron las fuentes y reconstruir las capas posteriores; las modificaciones ocurren en las capas siguientes, lo que mantiene el sistema recuperable.

#### ¿Qué es el principio de "responsabilidad única" aplicado a los pipelines de datos?

Cada pipeline o modelo debe tener un propósito claro (ingerir una fuente, homogeneizar una entidad, construir una métrica), lo que facilita probarlo, asignarle un responsable, reutilizarlo y cambiarlo sin efectos secundarios.

#### ¿Qué tipos de bases de datos existen?

Relacionales (PostgreSQL, MySQL, Oracle), clave-valor (DynamoDB, Redis), documentales (MongoDB, Couchbase), de columnas anchas (Cassandra, HBase, Bigtable), de grafos (Neo4j, Neptune), de series de tiempo (TimescaleDB, InfluxDB), de búsqueda (Elasticsearch, OpenSearch), vectoriales (pgvector, Pinecone, vectores de OpenSearch) y almacenes analíticos columnares (warehouses, ClickHouse, Druid).

<!-- challenge -->

Un equipo quiere autoalojar una plataforma de streaming open source porque "es gratis". ¿Qué le pides incluir en la comparación?

<!-- solution -->

El costo en personas de operarla 24/7 (actualizaciones, escalado, guardias), infraestructura, seguridad y soporte, comparado con el precio de un servicio administrado a tres años. Incluye el costo de oportunidad de ingenieros que no construyen productos de datos.

<!-- takeaways -->

- Compra por velocidad, construye por diferenciación.
- Formatos abiertos y estándares limitan el lock-in.
- Compara el costo total de propiedad, no precios de licencia.

### Almacenamiento y bases de datos

<!-- unit: Elegir una base de datos -->

<!-- goals -->

- Asociar almacenes relacionales, documentales, clave-valor, wide-column y de grafos a cada carga.
- Explicar la persistencia políglota y su costo.

<!-- concept -->

Las bases de datos difieren en qué preguntas responden barato. Las relacionales manejan consultas flexibles sobre datos relacionados con transacciones. Las documentales guardan juntos registros anidados y autocontenidos. Las clave-valor responden "dame esta llave" a escala enorme. Las wide-column absorben escrituras masivas por partición. Los grafos siguen relaciones.
Elegir por patrón de acceso y no por costumbre lleva a varios almacenes en un mismo sistema, lo cual funciona siempre que alguien sea dueño de la integración y la consistencia entre ellos.

<!-- example -->

| Patrón de acceso | Almacén |
|---|---|
| Órdenes con joins y transacciones | PostgreSQL |
| Catálogo de productos con atributos anidados | Documentos en MongoDB / DynamoDB |
| Búsqueda de sesión por ID, millones/s | Redis / DynamoDB |
| Escrituras de sensores por dispositivo y tiempo | Cassandra |
| "Amigos de amigos" o redes de fraude | Neo4j / Neptune |

#### ¿Cuándo se elige una base relacional?

Cuando los datos son estructurados y tienen relaciones, necesitan transacciones ACID, consultas flexibles con joins y consistencia fuerte: pedidos, pagos, cuentas, inventarios. Es la opción por defecto de la mayoría de los sistemas operativos.

#### ¿Cuándo se elige una base documental?

Cuando los registros son autocontenidos, anidados y con esquema flexible (catálogos de productos, contenidos, perfiles de usuario), se acceden sobre todo por clave o con consultas sencillas, y los equipos quieren hacer evolucionar el esquema rápido.

#### ¿Cuándo se elige un almacén clave-valor?

Para búsquedas muy rápidas por clave a gran escala (sesiones, cachés, preferencias de usuario, carritos de compra), con patrones de acceso simples y latencia predecible.

#### ¿Cuándo se elige un almacén de columnas anchas?

Para volúmenes de escritura masivos y conjuntos de datos grandes accedidos por clave de partición con patrones de consulta conocidos, como series de tiempo, IoT, mensajería y logs de eventos (Cassandra, Bigtable, HBase).

#### ¿Cuándo se elige una base de grafos?

Cuando las relaciones son el objeto principal del análisis: redes de fraude, redes sociales, recomendaciones, topologías de red, grafos de conocimiento, con consultas que recorren muchos saltos.

#### ¿Qué es la persistencia políglota?

Usar distintas tecnologías de almacenamiento para distintas necesidades dentro de un sistema (PostgreSQL para pedidos, Redis para sesiones, Elasticsearch para búsqueda, S3 para archivos), aceptando más complejidad operativa a cambio de ajustarse mejor a cada caso de uso.

#### ¿Qué es el almacenamiento de objetos y por qué es central en las plataformas de datos modernas?

El almacenamiento de objetos inmutables en buckets accedidos por clave mediante HTTP (S3, ADLS, GCS): prácticamente ilimitado, muy durable, barato y desacoplado del cómputo. Los data lakes y lakehouses se construyen sobre él, y los formatos de tabla le añaden funciones de base de datos.

<!-- challenge -->

Un equipo guarda perfiles de usuario, órdenes y pagos en MongoDB y ahora sufre con reportes que los cruzan y con la consistencia. ¿Qué sugieres?

<!-- solution -->

Dejar MongoDB donde encajan los documentos (perfiles), pasar órdenes y pagos, que necesitan joins y transacciones, a una base relacional, y replicar todo a la plataforma analítica para los reportes.

<!-- takeaways -->

- Elige almacenes por patrón de acceso.
- Relacional para joins y transacciones; otros para formas específicas.
- La persistencia políglota necesita una integración con dueño.

<!-- unit: Almacenes especializados -->

<!-- goals -->

- Saber cuándo encajan las series de tiempo y los motores de búsqueda.
- Distinguir OLTP, OLAP y HTAP.

<!-- concept -->

Algunas cargas son tan comunes que tienen motores propios. Los almacenes de series de tiempo manejan mediciones con marca de tiempo a alta frecuencia y consultas por rangos de tiempo. Los motores de búsqueda ordenan texto por relevancia y manejan coincidencias aproximadas y facetas.
La división más amplia es entre transacciones y análisis: OLTP sirve muchas lecturas y escrituras pequeñas, OLAP sirve escaneos grandes y agregaciones. Los sistemas HTAP intentan ambas en un motor, lo que ayuda a la analítica operativa pero rara vez reemplaza una plataforma analítica dedicada.

<!-- example -->

| Carga | Tipo de motor |
|---|---|
| Métricas de CPU cada 10 s de 5.000 hosts | Series de tiempo |
| Búsqueda de productos con errores de tipeo y filtros | Motor de búsqueda |
| Checkout y actualizaciones de inventario | OLTP |
| Ingresos mensuales por región y canal | OLAP |

#### ¿Qué diferencias hay entre el almacenamiento en bloques, de archivos y de objetos?

El de bloques da volúmenes en bruto para una máquina (EBS), ideal para bases de datos; el de archivos da sistemas de archivos jerárquicos compartidos (NFS, EFS); el de objetos da objetos planos accesibles por HTTP a enorme escala (S3), ideal para data lakes.

#### ¿Qué son los niveles (tiers) de almacenamiento?

Clases de almacenamiento con distinto costo y velocidad de acceso (caliente, tibio, frío, archivo; S3 Standard, Infrequent Access, Glacier). Las políticas de ciclo de vida mueven los datos que envejecen a niveles más baratos.

#### ¿Qué son los formatos de archivo por filas y columnares?

Los formatos por filas (CSV, JSON, Avro) guardan los registros juntos, buenos para escribir y leer registros completos; los columnares (Parquet, ORC) guardan las columnas juntas con estadísticas, buenos para analítica que lee pocas columnas de muchas filas.

<!-- challenge -->

Un equipo de e-commerce implementa la búsqueda de productos con `LIKE '%term%'` en PostgreSQL, y es lenta y no tolera errores de tipeo. ¿Qué propones?

<!-- solution -->

Indexar los productos en un motor de búsqueda (OpenSearch o Elasticsearch) alimentado desde la base con CDC o eventos, y servir la búsqueda desde ahí con relevancia, coincidencia aproximada y facetas. PostgreSQL sigue siendo la fuente de verdad.

<!-- takeaways -->

- Las series de tiempo manejan mediciones con marca de tiempo.
- Los motores de búsqueda ordenan y emparejan texto.
- OLTP y OLAP necesitan motores distintos; HTAP los mezcla.

<!-- unit: Capas de almacenamiento y formatos -->

<!-- goals -->

- Explicar el almacenamiento de objetos, sus niveles y los formatos de archivo.
- Comparar formatos de tabla abiertos y el papel del catálogo.

<!-- concept -->

Las plataformas de datos modernas se apoyan en almacenamiento de objetos: barato, durable, casi ilimitado y legible por cualquier motor. Encima, los formatos de archivo deciden qué tan eficiente es la lectura; los columnares permiten a las consultas analíticas saltarse lo que no necesitan.
Los formatos de tabla abiertos agregan las funciones de base de datos que faltan, transacciones, evolución de esquema y time travel, como metadatos sobre esos archivos. Un catálogo dice a los motores qué tablas existen y quién puede leerlas, y eso convierte archivos en una plataforma compartida.

<!-- example -->

```text
catalog (Unity / Glue / Polaris)  ─ tables, schemas, permissions
table format (Iceberg / Delta)    ─ snapshots, transactions, schema
file format (Parquet)             ─ columnar, compressed, statistics
object storage (S3 / ADLS / GCS)  ─ cheap, durable, tiered
```

#### ¿Qué son los formatos de tabla abiertos?

Especificaciones (Apache Iceberg, Delta Lake, Apache Hudi) que añaden una capa de metadatos transaccional sobre archivos Parquet en almacenamiento de objetos, con escrituras ACID, evolución del esquema, viaje en el tiempo, evolución de particiones y actualizaciones eficientes, legibles por muchos motores.

#### Iceberg, Delta o Hudi: ¿cómo eliges?

Delta es nativo de Databricks y muy usado en Spark; Iceberg tiene el soporte multimotor más amplio (Snowflake, Athena, Trino, Spark, Flink) y un catálogo REST abierto; Hudi se enfoca en los upserts de streaming y el procesamiento incremental. Elige según tus motores, tu catálogo y tu gobierno; las funciones de interoperabilidad (UniForm, XTable) reducen las diferencias.

#### ¿Qué papel cumple un catálogo de datos en la arquitectura de almacenamiento?

Registra qué tablas existen, dónde están sus archivos, sus esquemas y permisos, para que los motores encuentren y gobiernen los datos: Hive Metastore, AWS Glue, Unity Catalog, Polaris y los catálogos REST de Iceberg.

#### ¿Qué diferencia hay entre OLTP, OLAP y HTAP?

OLTP maneja transacciones, OLAP maneja analítica, y los sistemas HTAP (procesamiento híbrido transaccional/analítico) (TiDB, SingleStore, AlloyDB, Unistore) intentan atender ambos sobre datos frescos, útiles para analítica operativa a escala limitada.

#### ¿Cómo se elige una estrategia de claves primarias a escala?

Considerando la unicidad entre sistemas, el orden para la localidad de los índices y la exposición: los enteros autoincrementales son compactos pero necesitan coordinación central; los UUIDv4 son únicos en el mundo pero aleatorios; los UUIDv7 y los ULID son únicos y ordenados en el tiempo; las claves naturales deben quedar como atributos.

#### ¿Qué es un índice y qué tipos importan a un arquitecto de datos?

Una estructura que acelera las búsquedas a costa de las escrituras y el almacenamiento: B-tree (rangos, igualdad), hash (igualdad), GIN/invertidos (texto completo, arreglos, JSON), BRIN (tablas enormes ordenadas naturalmente), bitmap (baja cardinalidad en warehouses) e índices vectoriales (HNSW, IVF) para búsqueda por similitud.

#### ¿Para qué sirve una base de series de tiempo?

Para mediciones con marca de tiempo y alta ingesta (métricas, IoT, monitoreo) con consultas por rangos de tiempo, reducción de resolución y políticas de retención; comprimen las series de tiempo de forma eficiente y ofrecen funciones especializadas.

<!-- challenge -->

Tres motores (Spark, Trino y un warehouse) deben leer y escribir las mismas tablas. ¿Qué decisiones de almacenamiento lo hacen posible?

<!-- solution -->

Almacenamiento de objetos con archivos Parquet, un formato de tabla abierto con amplio soporte multimotor (a menudo Iceberg) y un catálogo compartido que los tres motores usan para metadatos y permisos.

<!-- takeaways -->

- El almacenamiento de objetos es la base de la plataforma.
- Los formatos columnares abaratan la analítica.
- Los formatos de tabla agregan transacciones; los catálogos hacen compartibles las tablas.

<!-- unit: Llaves e índices -->

<!-- goals -->

- Elegir una estrategia de llave primaria para escala e integración.
- Saber qué tipos de índice importan.

<!-- concept -->

Las llaves sobreviven a los sistemas que las crean. Una llave única solo dentro de una base choca cuando se fusionan datos de varias; una llave que expone significado o secuencia filtra información. A escala, el orden también importa: las llaves secuenciales mantienen compactos los índices y las aleatorias dispersan las escrituras.
Los índices son la otra mitad: cada tipo sirve a una forma de consulta, y cada índice hace más lentas las escrituras.

<!-- example -->

| Necesidad | Elección |
|---|---|
| Única entre servicios, generada en cualquier parte | UUIDv7 (ordenado por tiempo) |
| Compacta, una sola base | bigint identity |
| Consultas por rango e igualdad | Índice B-tree |
| JSON o array contiene | Índice GIN |
| Tablas enormes solo de anexado por tiempo | BRIN / clustering |

#### ¿Cuándo usarías un motor de búsqueda como OpenSearch?

Para búsqueda de texto completo con relevancia, coincidencias aproximadas, facetas y analítica de logs, normalmente como índice secundario alimentado desde el sistema de registro y no como base de datos principal.

#### ¿Qué es el teorema CAP?

En un sistema distribuido que sufre una partición de red, hay que elegir entre consistencia (toda lectura ve la última escritura) y disponibilidad (toda solicitud recibe respuesta). Sin particiones ambas son posibles; CAP trata del comportamiento durante los fallos.

<!-- challenge -->

Tras fusionar las tablas de clientes de dos empresas, los IDs chocan porque ambas usaban enteros autoincrementales. ¿Cómo lo evitas a futuro?

<!-- solution -->

Introduce una llave global (por ejemplo un UUIDv7 o una llave sustituta con prefijo de fuente) en el modelo integrado, conserva los IDs originales como atributos de la fuente y relaciónalos con una tabla de mapeo de llaves.

<!-- takeaways -->

- Las llaves deben ser únicas entre sistemas que se van a fusionar.
- Las llaves ordenadas mantienen eficientes los índices.
- Cada tipo de índice sirve a una forma de consulta y cuesta en escrituras.

### Fundamentos de sistemas distribuidos

<!-- unit: Compromisos ante fallas -->

<!-- goals -->

- Explicar CAP, PACELC, ACID y BASE.
- Comparar modelos de consistencia de fuerte a eventual.

<!-- concept -->

Cuando los datos viven en varias máquinas, las redes fallan y las máquinas no coinciden. CAP dice que durante una partición un sistema debe elegir entre responder y responder correctamente; PACELC agrega que incluso sin fallas hay que elegir entre velocidad y consistencia.
ACID y BASE describen dos actitudes ante esa elección: transacciones estrictas o disponibilidad con acuerdo eventual. Entre ellas hay puntos medios útiles, como garantizar que cada usuario vea sus propias escrituras, que suelen bastar al producto sin el costo de la consistencia total.

<!-- example -->

| Caso de uso | Modelo aceptable |
|---|---|
| Transferencia bancaria | Consistencia fuerte (ACID) |
| Contador de likes de un post | Consistencia eventual |
| El usuario edita su perfil y recarga | Read-your-writes |
| Hilo de comentarios | Consistencia causal |

#### ¿Qué es PACELC?

Una extensión de CAP: si hay una Partición, elige Disponibilidad o Consistencia; si no (Else, operación normal), elige Latencia o Consistencia. Explica por qué muchos sistemas sacrifican consistencia por menor latencia incluso sin fallos.

#### ¿Qué es ACID?

Atomicidad (todo o nada), Consistencia (se respetan las restricciones), Aislamiento (las transacciones concurrentes no interfieren) y Durabilidad (los datos confirmados sobreviven a los fallos): las garantías de las transacciones relacionales.

#### ¿Qué es BASE?

Basically Available, Soft state, Eventual consistency: un modelo preferido por algunos sistemas NoSQL distribuidos que priorizan la disponibilidad y la tolerancia a particiones, con datos que convergen a la consistencia con el tiempo.

#### ¿Qué es la consistencia eventual?

Si no hay nuevas actualizaciones, todas las réplicas terminan devolviendo el mismo valor; mientras tanto, las lecturas pueden devolver datos desactualizados. Las aplicaciones deben tolerar diferencias temporales.

#### ¿Qué modelos de consistencia existen además de la fuerte y la eventual?

Leer tus propias escrituras (un cliente ve lo que escribió), lecturas monótonas (no se retrocede en el tiempo), consistencia causal (las operaciones relacionadas causalmente se ven en orden), obsolescencia acotada (lecturas con a lo sumo X segundos de retraso) y consistencia de sesión.

#### ¿Qué es el particionado (sharding)?

Repartir los datos entre nodos según una clave (hash o rango) para que el almacenamiento y la carga escalen horizontalmente. Una buena clave reparte los datos de forma pareja y mantiene juntos los datos relacionados; las malas claves causan hotspots.

<!-- challenge -->

Un servicio de carrito de compras debe seguir disponible durante problemas de red entre regiones. ¿Qué modelo de consistencia encaja y qué debe manejar el diseño?

<!-- solution -->

Disponibilidad con consistencia eventual (a menudo read-your-writes por usuario). El diseño debe fusionar actualizaciones conflictivas del carrito, por ejemplo guardando las adiciones como un conjunto y resolviendo las eliminaciones con timestamps o version vectors.

<!-- takeaways -->

- Durante particiones, elige disponibilidad o consistencia.
- PACELC agrega el compromiso de latencia en operación normal.
- Los modelos intermedios suelen cubrir el producto a bajo costo.

<!-- unit: Particionamiento y replicación -->

<!-- goals -->

- Explicar particionamiento, replicación, consenso y quórums.
- Evitar hotspots y transacciones distribuidas.

<!-- concept -->

Las bases distribuidas escalan repartiendo los datos entre nodos (particionamiento) y sobreviven a fallas copiándolos (replicación). Cada una trae su problema. Particionar por una llave sesgada manda la mayoría del tráfico a un nodo. Replicar plantea qué copia es la correcta, lo que resuelven protocolos de consenso y quórums.
Coordinar una transacción entre muchos nodos o sistemas con two-phase commit es posible pero lento y frágil; por eso los diseños modernos prefieren transacciones locales más coordinación asíncrona.

<!-- example -->

```text
N = 3 replicas, W = 2 write acks, R = 2 read acks
W + R > N  →  every read overlaps the latest write (strongly consistent reads)
hot key "celebrity_123" → add a suffix 0–9 and spread it over 10 partitions
```

#### ¿Qué es la replicación y qué tipos hay?

Mantener copias de los datos en varios nodos para la disponibilidad y para escalar lecturas. La replicación síncrona espera a las réplicas (consistencia más fuerte, más latencia); la asíncrona responde antes de que confirmen (menos latencia, posible pérdida de datos en un failover). Las topologías incluyen líder-seguidor, multilíder y sin líder.

#### ¿Qué es un algoritmo de consenso?

Un protocolo (Raft, Paxos, ZAB) que permite a nodos distribuidos ponerse de acuerdo sobre un valor o un líder pese a los fallos, usado para metadatos, coordinación y logs replicados en sistemas como Kafka (KRaft), etcd y ZooKeeper.

#### ¿Qué es la idempotencia y por qué es vital en los sistemas de datos?

Una operación es idempotente si realizarla varias veces tiene el mismo efecto que una vez. Los reintentos son inevitables en los sistemas distribuidos, así que las escrituras idempotentes (upserts, sobrescritura por partición, claves de deduplicación) evitan duplicados y corrupción.

#### ¿Qué son las semánticas de entrega en la mensajería?

At-most-once (puede perder mensajes), at-least-once (puede duplicarlos) y exactly-once (el efecto de cada mensaje ocurre una vez). Exactly-once suele significar entrega at-least-once más procesamiento idempotente o transaccional.

#### ¿Qué es la contrapresión (backpressure)?

Un mecanismo por el cual un consumidor más lento indica a los productores que bajen el ritmo (o los buffers absorben las ráfagas), evitando la sobrecarga y el agotamiento de memoria en los pipelines de streaming.

#### ¿Qué diferencia hay entre escalar horizontal y verticalmente?

Escalar verticalmente añade recursos a una máquina (más simple, limitado); escalar horizontalmente añade máquinas (casi ilimitado, necesita particionado y coordinación). Las plataformas de datos dependen del escalado horizontal para el almacenamiento y el cómputo.

<!-- challenge -->

Una tabla particionada por `country` tiene una partición con el 70 % de la carga. ¿Qué cambias?

<!-- solution -->

Particionar por una llave de mayor cardinalidad (por ejemplo hash de `customer_id`) o llaves compuestas que dividan más el país grande, para repartir la carga. Deja `country` como filtro o índice secundario.

<!-- takeaways -->

- Particionar escala; replicar protege.
- Quórums y consenso deciden qué copia gana.
- Evita llaves sesgadas y transacciones distribuidas.

<!-- unit: Movimiento confiable de datos -->

<!-- goals -->

- Mover datos de forma segura con idempotencia y semánticas de entrega.
- Manejar backpressure y desfase de relojes.

<!-- concept -->

Mover datos entre sistemas implica reintentos, y los reintentos implican duplicados. La mayoría de la mensajería garantiza entrega at-least-once, así que la corrección viene de consumidores idempotentes que producen el mismo resultado si un mensaje llega dos veces.
Dos realidades más moldean el diseño: los consumidores pueden ser más lentos que los productores, así que se necesitan backpressure o buffers, y los relojes de distintas máquinas no coinciden, así que ordenar por timestamps entre sistemas exige cuidado.

<!-- example -->

```sql
-- idempotent sink: replaying an event changes nothing
MERGE INTO payments t
USING incoming s ON t.event_id = s.event_id
WHEN NOT MATCHED THEN INSERT *;
```

#### ¿Qué es un hotspot y cómo se evita?

Una partición o nodo que recibe una carga desproporcionada por una clave sesgada (un usuario muy popular, una marca de tiempo que siempre crece). Se evita con mejores claves, salting, hashing o dividiendo las claves calientes.

#### ¿Qué es el protocolo de commit en dos fases y por qué se evita?

Un protocolo en el que un coordinador pide a todos los participantes que se preparen y luego que confirmen, garantizando la atomicidad entre sistemas. Se evita a escala porque se bloquea ante fallos, añade latencia y acopla la disponibilidad de todos los participantes; se prefieren las sagas y el outbox.

#### ¿Qué es un quórum?

El número mínimo de nodos que deben confirmar una lectura o escritura para que tenga éxito (por ejemplo una mayoría). Si el quórum de lectura más el de escritura supera el número de réplicas, las lecturas ven la última escritura.

#### ¿Qué es el desfase de relojes y por qué importa?

Los relojes de distintas máquinas no coinciden, así que no se puede confiar en las marcas de tiempo de distintos sistemas para un orden exacto. Para ordenar los cambios usa relojes lógicos, números de secuencia o posiciones del log del sistema de origen.

<!-- challenge -->

Un consumidor procesa eventos de pago con entrega at-least-once y a veces cuenta doble los ingresos. Arréglalo sin cambiar el broker.

<!-- solution -->

Da a cada evento un ID único y haz idempotente el destino: upsert o `MERGE` por el ID del evento (o una tabla de IDs procesados), para que los eventos reentregados no creen filas nuevas.

<!-- takeaways -->

- La entrega at-least-once exige consumidores idempotentes.
- El backpressure evita que productores rápidos ahoguen a los consumidores.
- No ordenes eventos entre máquinas solo por la hora del reloj.

<!-- unit: Escalabilidad y rendimiento -->

<!-- goals -->

- Elegir entre escalado vertical y horizontal.
- Distinguir latencia de throughput.

<!-- concept -->

Escalar una sola máquina hacia arriba es lo más simple hasta que choca con un techo o un salto de precio. Escalar hacia afuera en muchas máquinas quita el techo, pero trae los problemas distribuidos de particionamiento, replicación y coordinación.
El rendimiento tiene dos ejes que tiran en direcciones distintas: la latencia es qué tan rápido termina una solicitud, el throughput cuántas terminan por segundo. Agrupar en lotes sube a la vez throughput y latencia; los sistemas en tiempo real sacrifican throughput por latencia.

<!-- example -->

| Diseño | Latencia | Throughput |
|---|---|---|
| Insertar fila por fila | Baja por fila | Bajo |
| Lotes de 10.000 filas | Mayor por fila | Alto |
| Stream con micro-lotes de 1 s | Segundos | Medio |

#### ¿Qué diferencia hay entre latencia y rendimiento (throughput)?

La latencia es cuánto tarda una operación; el rendimiento es cuántas operaciones terminan por unidad de tiempo. Los sistemas batch optimizan el rendimiento; los interactivos y de streaming se preocupan por la latencia; mejorar uno puede empeorar el otro.

#### ¿Qué enfoques de modelado se usan en arquitectura de datos?

Modelos normalizados (3FN) para la integración y el OLTP, dimensionales (Kimball) para la analítica, Data Vault para capas de integración auditables, tablas anchas desnormalizadas (one big table) para consumos concretos, y modelos anchor o ensemble en casos de nicho.

<!-- challenge -->

Un job nocturno que carga 100 millones de filas una por una tarda 9 horas. ¿Qué compromiso cambias?

<!-- solution -->

Prioriza throughput sobre latencia por fila: carga en lotes grandes o con comandos masivos (`COPY`), en paralelo por partición. El tiempo total baja muchísimo porque desaparece el costo por fila.

<!-- takeaways -->

- Escala hacia arriba por simplicidad; hacia afuera al pasar los límites.
- Latencia y throughput compiten entre sí.
- Los lotes suben el throughput.

<!-- stage: Patrones de modelado y almacenamiento -->

### Enfoques de modelado

<!-- unit: Enfoques de modelado -->

<!-- goals -->

- Comparar el modelado normalizado, dimensional y otros enfoques.
- Elegir entre schema-on-write y schema-on-read.

<!-- concept -->

Los modelos codifican qué significan los datos. Los normalizados guardan cada hecho una vez y sirven para integración y transacciones; los dimensionales organizan hechos y contexto para un análisis rápido y comprensible. Los modelos canónicos dan a los sistemas un lenguaje común; técnicas muy normalizadas como anchor modeling favorecen el cambio sobre la simplicidad.
También importa cuándo se impone el esquema: al escribir atrapa errores temprano, al leer conserva flexibilidad para datos crudos y exploratorios. La mayoría de plataformas hace ambas cosas, en capas distintas.

<!-- example -->

| Capa | Enfoque |
|---|---|
| Crudo | Schema-on-read, tal como llega |
| Integración | 3NF o Data Vault |
| Consumo | Dimensional (esquemas estrella) o tablas anchas |

#### ¿Qué es la tercera forma normal y para qué sirve?

Un nivel de normalización en el que cada atributo no clave depende solo de la clave, evitando redundancia y anomalías de actualización. Sirve para los sistemas transaccionales y las capas de integración al estilo Inmon.

#### ¿Qué es la arquitectura de Inmon?

La Corporate Information Factory de Bill Inmon: un data warehouse empresarial en 3FN como versión única, integrada y orientada a temas de la verdad, que alimenta data marts dependientes para los departamentos. De arriba hacia abajo, primero la integración.

#### ¿Qué es la arquitectura de Kimball?

La bus architecture de Ralph Kimball: data marts dimensionales por proceso de negocio, integrados mediante dimensiones conformadas y la bus matrix, construidos de forma incremental. De abajo hacia arriba, primero el valor de negocio.

#### ¿Qué es Data Vault 2.0?

Una metodología para la capa de integración con hubs (claves de negocio únicas), links (relaciones) y satellites (atributos descriptivos en el tiempo), más claves hash para la carga en paralelo, historial de solo inserción y estándares para el business vault y los information marts. Pensada para la agilidad y la auditabilidad con muchas fuentes cambiantes.

#### ¿Qué son los hubs, links y satellites?

Los hubs guardan las claves de negocio (número de cliente) con metadatos de carga; los links guardan las relaciones entre hubs (cliente-pedido); los satellites guardan los atributos y su historial para un hub o un link, separados por fuente o por velocidad de cambio.

<!-- challenge -->

Los analistas consultan directamente un modelo de integración en 3NF y escriben joins de 12 tablas para cada reporte. ¿Qué agregas?

<!-- solution -->

Una capa de consumo dimensional: tablas de hechos por proceso de negocio con dimensiones conformadas (o tablas anchas para usos específicos), construidas desde el modelo de integración, para que los reportes necesiten pocos joins predecibles.

<!-- takeaways -->

- Normalizado para integración; dimensional para análisis.
- Impón el esquema al escribir donde los errores son costosos.
- Cada capa puede usar un enfoque distinto.

<!-- unit: Inmon, Kimball y Data Vault -->

<!-- goals -->

- Describir las metodologías Inmon, Kimball y Data Vault.
- Combinarlas en una plataforma moderna por capas.

<!-- concept -->

Los debates clásicos son sobre dónde ocurre la integración. Inmon integra primero en un warehouse empresarial normalizado y de ahí construye los marts. Kimball integra mediante dimensiones compartidas entre marts por proceso. Data Vault separa llaves, relaciones e historia en hubs, links y satellites, para agregar fuentes nuevas sin remodelar.
En la práctica son capas más que rivales: un vault o una capa normalizada para integración y auditoría, y marts dimensionales para el consumo.

<!-- example -->

```text
hub_customer       (customer_hk, customer_number, load_ts, source)
link_order_customer (link_hk, order_hk, customer_hk, load_ts, source)
sat_customer_details (customer_hk, load_ts, name, segment, hash_diff)
      └─► dim_customer (Kimball, SCD2) ─► fct_orders
```

#### ¿Cuándo es Data Vault una buena opción?

En empresas con muchas fuentes que cambian a menudo, requisitos fuertes de auditoría (finanzas, seguros, sectores regulados) y la necesidad de cargar en paralelo y conservar todo el historial. Es excesivo para plataformas pequeñas o de una sola fuente.

#### ¿Qué es el enfoque "one big table" (OBT)?

Una sola tabla ancha y desnormalizada por caso de uso con todo lo necesario, rápida en los motores columnares y fácil para las herramientas, a costa de lógica y almacenamiento duplicados entre tablas. Suele construirse encima de modelos dimensionales.

#### ¿Cómo encajan Kimball, Inmon y Data Vault en la práctica?

Una organización moderna común: aterrizaje en bruto, una capa de integración (normalizada o Data Vault) que historiza e integra las fuentes, y esquemas en estrella de Kimball u OBT para el consumo, a menudo correspondientes a bronze, silver y gold.

#### ¿Qué es esquema al escribir frente a esquema al leer?

El esquema al escribir valida y estructura los datos al cargarlos (warehouses), detectando los errores pronto. El esquema al leer guarda los datos en bruto y aplica la estructura al consultar (lakes), lo que es flexible pero traslada los problemas a los consumidores. Los lakehouses combinan ambos según la capa.

#### ¿Qué es un modelo de datos canónico?

Una representación compartida e independiente de las aplicaciones de las entidades y eventos principales, usada para integrar sistemas, de modo que cada sistema se mapea al modelo canónico y no a todos los demás sistemas.

#### ¿Qué es el anchor modeling?

Una técnica muy normalizada (6FN) en la que cada atributo se guarda en su propia tabla con historial, lo que permite evolucionar el esquema sin destruir nada; es rara en la práctica pero influyó en ideas de Data Vault.

<!-- challenge -->

Una empresa de 20 personas con tres fuentes considera Data Vault "por buenas prácticas". ¿Qué le aconsejas?

<!-- solution -->

Probablemente no: Data Vault paga con muchas fuentes cambiantes y requisitos estrictos de auditoría. Con tres fuentes, una capa de staging más marts dimensionales es más simple y rápida de entregar; reconsidéralo si las fuentes se multiplican.

<!-- takeaways -->

- Inmon integra primero; Kimball integra con dimensiones conformadas.
- Data Vault separa llaves, relaciones e historia.
- Combínalos como capas cuando haga falta.

<!-- unit: Dar forma a los modelos analíticos -->

<!-- goals -->

- Elegir el grano y la forma de los datasets analíticos.
- Modelar datos semiestructurados y conformar definiciones entre dominios.

<!-- concept -->

Dos decisiones moldean cada dataset analítico. El grano, qué representa una fila, decide qué preguntas puede responder; elegir el grano más atómico que necesitan los consumidores deja opciones abiertas. La forma decide qué tan fácil es usarlo: esquemas estrella para flexibilidad, una tabla ancha para un uso específico.
Entre dominios, la consistencia importa más que la forma. Llaves y definiciones conformadas son lo que hace que "ingresos" signifique lo mismo en el reporte de cada área.

<!-- example -->

```text
grain: one row per order line
fct_order_lines(order_line_id, order_id, product_id, customer_id, date_id, quantity, net_amount)
conformed: dim_customer, dim_product, dim_date shared by sales, finance and marketing
```

#### ¿Cómo se modelan los datos semiestructurados en una plataforma analítica?

Aterrizándolos en bruto (JSON, `VARIANT`, columnas struct), extrayendo en las capas siguientes los campos estables y muy usados a columnas tipadas, dejando el resto anidado para conservar la flexibilidad y documentando los esquemas con contratos o un registro.

#### ¿Qué es un modelo "conformado" entre dominios?

Definiciones compartidas de claves y entidades (cliente, producto, fecha) que usan los productos de datos de todos los dominios, para que el análisis entre dominios funcione; en un mesh suelen publicarse como productos de datos de referencia.

#### ¿Cómo se decide el grano de un producto de datos?

A partir de las preguntas de los consumidores y de los eventos atómicos del origen: elige el grano más atómico que sea estable y útil, documéntalo de forma explícita y ofrece los agregados como productos aparte.

#### ¿Qué es un data lake?

Un repositorio centralizado en almacenamiento de objetos que guarda datos en bruto y procesados de cualquier formato y a cualquier escala, con almacenamiento barato y esquema al leer, usado para analítica, ciencia de datos y como fuente de los warehouses.

#### ¿Qué es un data swamp?

Un data lake que se volvió inutilizable: datos sin documentar, sin gobierno, duplicados, de calidad y propiedad desconocidas. Los catálogos, los responsables, los controles de calidad, las zonas y las políticas de ciclo de vida lo evitan.

<!-- challenge -->

Un equipo construye una tabla de resumen diario como única fuente de ingresos. Ahora finanzas necesita ingresos por línea de orden. ¿Qué salió mal y cómo se arregla?

<!-- solution -->

El grano era demasiado grueso. Construye el hecho al grano atómico (línea de orden) y deriva de él el resumen diario, para responder preguntas nuevas sin volver a las fuentes.

<!-- takeaways -->

- Elige el grano más atómico que necesitan los consumidores.
- Tablas anchas para usos específicos; estrellas para flexibilidad.
- Las definiciones conformadas hacen que las cifras coincidan.

### Data lakes, lakehouses y medallion

<!-- unit: Lagos, zonas y pantanos -->

<!-- goals -->

- Describir los data lakes y sus zonas.
- Prevenir un data swamp y recuperarse de él.

<!-- concept -->

Un data lake guarda datos de cualquier formato a bajo costo en almacenamiento de objetos, usualmente en zonas de crudo a curado. Su flexibilidad es también su riesgo: sin dueños, catálogos ni estándares, se llena de copias sin documentar hasta que nadie confía en nada, un pantano.
Las soluciones son tan organizacionales como técnicas: inventario, dueños, zonas con reglas claras, un catálogo y políticas de lifecycle que eliminen lo que nadie usa.

<!-- example -->

```text
s3://lake/landing/   files as delivered (immutable, short retention after processing)
s3://lake/raw/       standardized format, all history
s3://lake/curated/   validated, modeled, owned and documented
s3://lake/sandbox/   per-user experiments, auto-expire after 30 days
```

#### ¿Qué zonas suele tener un data lake?

Aterrizaje/raw (tal como llega), limpia/estandarizada (validada, tipada, deduplicada), curada/de consumo (datasets listos para el negocio), además de zonas sandbox para explorar y zonas de archivo para los datos fríos.

#### ¿Qué es un lakehouse?

Una arquitectura que lleva las funciones del warehouse (transacciones ACID, control de esquema, gobierno, rendimiento) al almacenamiento del lake mediante formatos de tabla abiertos y catálogos, para que una sola copia de los datos sirva a BI, ML e ingeniería de datos con varios motores.

#### ¿Qué es la arquitectura medallion?

Un patrón de capas del lakehouse: bronze guarda los datos en bruto tal como se ingieren (solo inserción, con metadatos), silver guarda los datos limpios, homogeneizados, deduplicados e historizados, y gold guarda agregados de negocio y modelos dimensionales listos para consumir.

#### ¿Qué ventajas tiene la arquitectura medallion?

Responsabilidades claras por capa, la posibilidad de reprocesar desde los datos en bruto, una mejora incremental de la calidad, una depuración más fácil (se inspecciona cada capa) y un lugar natural para los controles de calidad entre capas.

#### ¿Cuáles son los errores comunes con la arquitectura medallion?

Tratar las capas como copias obligatorias aunque no aporten nada, meter lógica de negocio en bronze, dejar que los consumidores lean bronze o silver directamente, contratos poco claros entre capas, y copiar datos entre capas sin procesamiento incremental (costo).

<!-- challenge -->

El lago tiene 8.000 carpetas y nadie sabe cuáles se usan. Da los tres primeros pasos de una limpieza.

<!-- solution -->

Usa los logs de acceso y los metadatos del catálogo para ver qué se lee y quién lo lee, asigna dueños a los datasets usados y regístralos en el catálogo, y luego archiva o borra los datos sin uso tras anunciar una fecha límite.

<!-- takeaways -->

- Los lagos guardan cualquier cosa barato; las zonas dan estructura.
- Los pantanos vienen de la falta de dueños y metadatos.
- Recupéralos con inventario, dueños, catálogo y reglas de lifecycle.

<!-- unit: Lakehouse y medallion -->

<!-- goals -->

- Explicar el lakehouse y las capas medallion.
- Decidir entre lakehouse y warehouse, y evitar errores comunes de medallion.

<!-- concept -->

Un lakehouse agrega funciones de warehouse (transacciones, esquemas, gobierno) a un lago mediante formatos de tabla y un catálogo, para que BI y ML compartan una sola copia de los datos. Medallion es su organización usual en capas: bronze tal como llega, silver limpio y conformado, gold listo para consumir.
Las capas son un medio, no una regla. Copiar datos por capas que no agregan nada desperdicia dinero, y poner lógica de negocio en bronze anula su propósito. Que encaje un lakehouse o un warehouse depende de cargas, habilidades y formatos.

<!-- example -->

| Capa | Contrato |
|---|---|
| Bronze | Solo anexado, esquema de la fuente, metadatos de ingesta |
| Silver | Tipado, deduplicado, llaves conformadas |
| Gold | Hechos, dimensiones y agregados listos para el negocio |

#### ¿Qué relación tiene medallion con Kimball y Data Vault?

Son complementarios: medallion describe capas de refinamiento; Data Vault puede ser la técnica de modelado en silver; los esquemas en estrella de Kimball son típicos en gold. Medallion es una convención de capas, no un método de modelado.

#### Lakehouse o warehouse: ¿cómo decides?

Un warehouse (Snowflake, BigQuery, Redshift) es lo más sencillo para BI centrado en SQL con datos estructurados. Un lakehouse encaja cuando necesitas formatos abiertos, varios motores, grandes volúmenes semiestructurados o no estructurados, ML y streaming sobre los mismos datos, o evitar copias. Muchas organizaciones combinan ambos, y la frontera se está difuminando.

#### ¿Qué papel cumple un catálogo de datos en un lakehouse?

Es el plano de control: registro de tablas, esquemas, permisos, linaje, etiquetas y descubrimiento entre motores (Unity Catalog, Glue con Lake Formation, Polaris), que convierte archivos en tablas gobernadas.

#### ¿Qué es una "zona de aterrizaje" frente a bronze?

La zona de aterrizaje guarda los archivos exactamente como se entregaron (CSV, JSON, exportaciones) para la trazabilidad; bronze es la primera representación en tabla de esos datos con cambios mínimos más los metadatos de ingesta, consultable y gobernada.

#### ¿Cuántas capas debe tener un lakehouse?

Tantas como aporten un valor claro: típicamente raw/bronze, limpia/silver y de consumo/gold, a veces una zona de aterrizaje antes y una capa de servicio o semántica después. Las capas extra sin contratos propios solo añaden costo.

#### ¿Qué es la compactación y por qué la necesitan los lakehouses?

Reescribir muchos archivos pequeños en menos archivos más grandes (y fusionar los archivos de borrado), lo que mantiene rápidas las lecturas y pequeños los metadatos. El streaming y los upserts frecuentes la hacen necesaria; se puede programar o ser automática.

#### ¿Cómo se maneja la evolución del esquema en un lakehouse?

Permitiendo automáticamente los cambios aditivos (columnas nuevas que admiten nulos) en bronze, revisando y aplicando a propósito los cambios en silver y gold con las funciones del formato de tabla (añadir, renombrar, ampliar) y usando contratos y alertas para los cambios que rompen.

<!-- challenge -->

Un equipo crea copias bronze, silver y gold de una tabla de referencia pequeña que nunca cambia. ¿Es buena práctica?

<!-- solution -->

No. Las capas deben agregar valor; una tabla de referencia estática se puede cargar una vez en silver (o gold) y usar directamente. Conserva el archivo crudo para trazabilidad.

<!-- takeaways -->

- Los lakehouses agregan funciones de warehouse al lago.
- Bronze, silver y gold tienen contratos distintos.
- Usa capas donde agreguen valor.

<!-- unit: Operar un lakehouse -->

<!-- goals -->

- Usar el catálogo como plano de control del lakehouse.
- Planear compactación, evolución de esquema y time travel.

<!-- concept -->

Un lakehouse vale lo que vale su mantenimiento. El catálogo registra tablas, permisos y linaje, así que se vuelve el plano de control. Las escrituras frecuentes crean archivos pequeños y archivos de borrado, así que la compactación es mantenimiento de rutina. Los esquemas evolucionan, así que cada capa necesita una política: permisiva en bronze, revisada en silver y gold.
El time travel convierte el historial de la tabla en una herramienta para auditorías, reproducciones y recuperación, dentro de los límites de retención que fija el mantenimiento.

<!-- example -->

```sql
OPTIMIZE silver.orders;                                 -- compaction (Delta)
SELECT * FROM gold.revenue TIMESTAMP AS OF '2026-09-30'; -- reproduce month-end report
ALTER TABLE bronze.events ADD COLUMNS (device_type STRING); -- additive change
```

#### ¿Para qué sirve arquitectónicamente el "viaje en el tiempo"?

Para reproducir reportes a una fecha, auditar, depurar qué cambió, recuperarse de escrituras malas y comparar versiones, siempre que las políticas de retención conserven suficiente historial.

#### ¿Qué diferencia hay entre el procesamiento batch y el de streaming?

El batch procesa conjuntos de datos acotados a intervalos (cada hora, cada día) con mucho rendimiento y lógica más simple; el streaming maneja flujos de eventos sin fin de forma continua con baja latencia, y requiere gestión de estado, manejo del tiempo del evento y tolerancia a fallos.

#### ¿Qué es la arquitectura Lambda?

La arquitectura de Nathan Marz con una capa batch (recalcula vistas exactas a partir de todo el historial), una capa de velocidad (procesa los datos recientes en tiempo real) y una capa de servicio que combina ambas. Da exactitud y baja latencia, pero duplica la lógica en dos caminos de código.

#### ¿Qué es la arquitectura Kappa?

La simplificación de Jay Kreps: un único camino de procesamiento en streaming donde todo es un flujo; el reprocesamiento se hace reproduciendo el log (Kafka) con una nueva versión del job. Elimina la lógica duplicada, pero necesita un log durable y reproducible y un streaming robusto.

<!-- challenge -->

Un auditor pide la cifra exacta de ingresos que la empresa reportó el 30 de septiembre, aunque los datos se corrigieron desde entonces. ¿Cómo ayuda la arquitectura?

<!-- solution -->

Con time travel sobre la tabla gold (con retención que cubra esa fecha), se consulta tal como estaba en el momento del reporte. Para necesidades de largo plazo, guarda las cifras reportadas en una tabla inmutable, porque la retención del time travel es limitada.

<!-- takeaways -->

- El catálogo es el plano de control del lakehouse.
- La compactación mantiene rápidas las lecturas.
- El time travel ayuda en auditorías dentro de su retención.

<!-- stage: Mover datos -->

### Arquitecturas batch y streaming

<!-- unit: Batch, streaming y sus arquitecturas -->

<!-- goals -->

- Comparar procesamiento batch, micro-batch y streaming.
- Explicar Lambda y Kappa y decidir cuándo hace falta tiempo real.

<!-- concept -->

Batch y streaming difieren en cuándo se calculan los resultados, no en qué. Batch procesa datos acotados según un calendario, de forma simple y barata. Streaming procesa eventos a medida que llegan, para decisiones que pierden valor en minutos.
Lambda corría ambos caminos en paralelo; Kappa usaba streams para todo. Los motores modernos difuminan la línea y corren el mismo código como batch o stream. La pregunta real es la latencia de negocio: a la mayoría de dashboards les basta cada hora, y el tiempo real cuesta más construirlo y operarlo.

<!-- example -->

| Caso de uso | Latencia necesaria | Enfoque |
|---|---|---|
| Chequeo de fraude en un pago con tarjeta | < 1 s | Streaming |
| Inventario en el sitio web | Minutos | Micro-batch o streaming |
| Dashboard ejecutivo de ingresos | Horas | Batch |

#### Lambda o Kappa: ¿cuál se usa hoy?

La Lambda pura es rara porque mantener dos bases de código es costoso. Las plataformas modernas usan motores unificados (Spark Structured Streaming, Flink, Beam) y formatos de tabla que admiten batch y streaming sobre las mismas tablas, más cerca de Kappa, con backfills batch cuando hace falta.

#### ¿Qué es el tiempo del evento frente al tiempo de procesamiento?

El tiempo del evento es cuándo ocurrió algo en el origen; el de procesamiento es cuándo lo procesa el sistema. La analítica correcta suele necesitar el tiempo del evento, porque los eventos llegan tarde y desordenados.

#### ¿Qué son las ventanas en el procesamiento de streaming?

Agrupaciones de eventos en el tiempo para agregarlos: tumbling (fijas, sin solapamiento), sliding o hopping (solapadas) y ventanas de sesión (los periodos de inactividad definen las sesiones).

#### ¿Qué es una watermark en streaming?

Un umbral de tiempo del evento hasta el cual el sistema asume que ya vio todos los eventos, lo que permite cerrar ventanas y limpiar el estado; los eventos más tardíos que la watermark se descartan o se tratan aparte.

#### ¿Qué papel cumple Apache Kafka en la arquitectura de datos?

Un log de eventos distribuido, durable y reproducible: desacopla productores de consumidores, absorbe ráfagas, permite que varios consumidores lean los mismos datos a su ritmo y sirve de columna vertebral para el streaming, el CDC y los sistemas orientados a eventos.

#### ¿Qué son los topics, las particiones y los grupos de consumidores de Kafka?

Un topic es un flujo de registros con nombre; se divide en particiones (logs ordenados y replicados) para el paralelismo; un grupo de consumidores reparte las particiones entre sus miembros, de modo que cada partición la lee un solo consumidor del grupo, lo que da un consumo escalable con orden por partición.

#### ¿Cómo se garantiza el orden en Kafka?

Solo dentro de una partición. Los registros con la misma clave van a la misma partición, así que se conserva el orden por clave; el orden global entre particiones no está garantizado.

<!-- challenge -->

Un product manager pide un dashboard en tiempo real de usuarios activos semanales. ¿Qué propones?

<!-- solution -->

Pregunta qué decisión depende de él. Los usuarios activos semanales cambian despacio, así que un batch cada hora o diario basta y es mucho más barato. Ofrece streaming solo para métricas que impulsan acciones inmediatas.

<!-- takeaways -->

- Batch es simple y barato; streaming sirve decisiones urgentes.
- Los motores unificados reemplazan los caminos separados de Lambda.
- Ajusta la latencia al valor de negocio.

<!-- unit: El tiempo en los streams -->

<!-- goals -->

- Distinguir event time de processing time.
- Usar ventanas, watermarks y estado correctamente.

<!-- concept -->

Los eventos llegan tarde y desordenados, así que un procesador de streams debe decidir en qué reloj confiar. El event time, cuándo ocurrió algo, da resultados correctos; el processing time, cuándo llegó, es más simple pero falla siempre que los retrasos varían.
Las ventanas agrupan eventos por event time, los watermarks deciden cuánto esperar a los rezagados y el estado recuerda resultados parciales entretanto. Cruzar con datos de referencia agrega otra pregunta de tiempo: qué versión de la referencia aplicaba cuando ocurrió el evento.

<!-- example -->

```python
(events
 .withWatermark("event_time", "10 minutes")           # wait up to 10 min for late events
 .groupBy(F.window("event_time", "5 minutes"), "store_id")
 .agg(F.sum("amount").alias("revenue")))
```

#### ¿Qué es un schema registry?

Un servicio que guarda esquemas versionados (Avro, Protobuf, JSON Schema) de los topics y aplica reglas de compatibilidad, para que los productores no publiquen cambios que rompan y los consumidores deserialicen de forma confiable.

#### ¿Qué motores de procesamiento de streaming existen?

Apache Flink (baja latencia, con estado, por tiempo del evento), Spark Structured Streaming (micro-lotes y continuo, integrado con Spark), Kafka Streams y ksqlDB (librería y SQL sobre Kafka), Apache Beam (modelo portable, corre en Dataflow) y servicios administrados (Kinesis Data Analytics/Managed Flink, Confluent, Databricks).

#### ¿Cuándo se necesita de verdad el tiempo real?

Cuando las decisiones o acciones pierden valor en segundos o minutos: detección de fraude, alertas operativas, personalización, monitoreo de IoT, precios dinámicos. Muchos dashboards no lo necesitan; el batch o los micro-lotes son más baratos y simples.

#### ¿Qué es una base de datos de streaming o un almacén OLAP en tiempo real?

Sistemas hechos para ingerir flujos y servir consultas analíticas de baja latencia sobre datos frescos (Apache Druid, Apache Pinot, ClickHouse, Materialize, RisingWave), usados para analítica de cara al usuario y dashboards operativos.

#### ¿Qué son los micro-lotes?

Procesar un flujo como una secuencia de lotes pequeños (de segundos a minutos), como hace por defecto Spark Structured Streaming. Simplifica la tolerancia a fallos y reutiliza la lógica batch, con algo más de latencia que el procesamiento evento por evento.

<!-- challenge -->

Los eventos de una app móvil pueden llegar horas tarde cuando los teléfonos están sin conexión. Los ingresos por ventana de 5 minutos siguen cambiando en el dashboard. ¿Cómo diseñas para esto?

<!-- solution -->

Agrega por event time con un watermark que acote el retraso para la vista en vivo, y recalcula las cifras finales en un job batch (o con upserts) que incluya los eventos tardíos. Marca las ventanas recientes como provisionales.

<!-- takeaways -->

- Usa event time para resultados correctos.
- Los watermarks acotan cuánto esperar a los datos tardíos.
- El estado guarda resultados parciales; los cruces con referencias necesitan versiones.

<!-- unit: Kafka como columna vertebral -->

<!-- goals -->

- Explicar topics, particiones, consumer groups y orden en Kafka.
- Usar schema registries, procesamiento exactly-once y replay.

<!-- concept -->

Kafka es un log durable y re-reproducible. Los productores anexan eventos; cualquier número de consumer groups lee a su propio ritmo; los datos se quedan durante un periodo de retención, o indefinidamente con tiered storage. Ese desacoplamiento es por lo que suele volverse la columna vertebral entre sistemas.
Sus garantías son específicas: orden solo dentro de una partición, así que las llaves eligen la partición; exactly-once solo dentro de las transacciones de Kafka; y compatibilidad solo si se imponen esquemas. Releer desde el log es la forma estándar de reprocesar.

<!-- example -->

```text
topic orders (6 partitions, key = customer_id)
  → all events of one customer in order, on one partition
consumer group "billing"   reads every event once (split across its consumers)
consumer group "analytics" reads every event independently
```

#### ¿Qué es el procesamiento de streaming con estado?

Un procesamiento que conserva información entre eventos (conteos por ventana, estado de sesión, joins entre flujos, deduplicación), que requiere almacenes de estado tolerantes a fallos y checkpoints; Flink y Spark administran el estado con snapshots.

#### ¿Cómo se unen flujos con datos de referencia?

Difundiendo (broadcast) los datos de referencia que cambian poco a los procesadores de streaming y refrescándolos periódicamente, uniendo con un flujo de cambios (tablas temporales o versionadas), o consultando un almacén rápido (Redis, DynamoDB) con caché.

#### ¿Qué es el procesamiento exactly-once en Kafka?

Productores idempotentes más transacciones que escriben de forma atómica los registros de salida y confirman los offsets del consumidor, para que los efectos de un ciclo leer-procesar-escribir ocurran una sola vez aun con reintentos, dentro de pipelines de Kafka a Kafka.

#### ¿Cómo se reprocesan datos en una arquitectura de streaming?

Reproduciendo desde el log (retención o almacenamiento por niveles de Kafka) con una nueva versión del job que escribe en tablas nuevas, validando y luego cambiando a los consumidores; o haciendo backfill desde las tablas del lakehouse con un job batch que use la misma lógica.

#### ¿Qué son el almacenamiento por niveles y la retención infinita en Kafka?

Descargar los segmentos de log más viejos en almacenamiento de objetos, para que los topics conserven historiales largos de forma barata, lo que permite reproducciones y reprocesamientos al estilo Kappa sin discos enormes en los brokers.

#### ¿Cómo cambian los microservicios la arquitectura de datos?

Cada servicio es dueño de sus datos y de su base (una base por servicio) y se comunica mediante APIs y eventos en lugar de tablas compartidas. Esto mejora la autonomía y el escalado, pero dispersa los datos y exige patrones de integración para la analítica y las consultas entre servicios.

#### ¿Qué es el patrón de "una base de datos por servicio"?

Cada microservicio tiene una base privada a la que solo él accede; los demás servicios usan su API o sus eventos. Evita el acoplamiento fuerte a través de esquemas compartidos.

<!-- challenge -->

Los eventos de estado de una orden (creada, pagada, enviada) a veces llegan desordenados a un consumidor. El topic tiene 12 particiones y no usa llave. ¿Qué cambias?

<!-- solution -->

Produce con `order_id` como llave para que todos los eventos de una orden vayan a la misma partición y conserven el orden. Los consumidores también deben tolerar duplicados y usar un número de secuencia por seguridad.

<!-- takeaways -->

- Kafka es un log durable y re-reproducible.
- El orden se mantiene por partición; las llaves eligen la partición.
- Schema registries y replay mantienen los streams evolucionables.

<!-- unit: Motores de streaming y consumo -->

<!-- goals -->

- Comparar motores de procesamiento de streams y almacenes de consumo en tiempo real.
- Agregar scoring en tiempo real a una plataforma batch.

<!-- concept -->

Procesar y servir son decisiones separadas. Motores como Flink, Spark Structured Streaming y Kafka Streams calculan sobre streams y difieren sobre todo en latencia, manejo de estado y habilidades que exigen. Servir resultados frescos a usuarios necesita un almacén hecho para consultas de baja latencia sobre datos recientes, y los warehouses comunes no lo son.
Agregar tiempo real a una plataforma batch suele significar un camino paralelo para los pocos casos que lo necesitan, reutilizando las mismas definiciones.

<!-- example -->

```text
payments ─► Kafka ─► Flink: features (txn count 5 min, amount vs avg)
                         └─► model endpoint ─► decision < 200 ms
                         └─► feature log ─► lake (training, audit)
```

#### ¿Por qué una base compartida es un antipatrón en microservicios?

Los servicios quedan acoplados por el esquema: el cambio de un equipo rompe a otros, los despliegues deben coordinarse y la propiedad es confusa, con lo que se pierde el principal beneficio de los microservicios.

#### ¿Cómo se hace analítica entre microservicios?

Capturando los datos de cada servicio (CDC de su base o sus eventos de dominio) en un lake o un warehouse, modelándolos de forma central o por dominio, y sirviendo la analítica desde allí, en lugar de consultar directamente las bases de los servicios.

#### ¿Qué es la arquitectura orientada a eventos?

Sistemas que se comunican produciendo eventos y reaccionando a ellos (hechos sobre algo que ocurrió: `OrderPlaced`, `PaymentFailed`) a través de un broker, en lugar de llamadas síncronas, lo que da bajo acoplamiento, escalabilidad y registros de auditoría naturales.

<!-- challenge -->

Las features de fraude en tiempo real y las del entrenamiento del modelo se calculan con código distinto y no coinciden. ¿Cómo lo arreglas?

<!-- solution -->

Calcula las features una vez (mismas definiciones) y registra en el lago los valores usados en cada decisión; entrena con esas features registradas o usa un feature store que sirva las mismas definiciones online y offline.

<!-- takeaways -->

- Los motores difieren en latencia, estado y habilidades.
- Servir en tiempo real exige almacenes de baja latencia.
- Agrega caminos en tiempo real solo donde hagan falta, compartiendo definiciones.

### Microservicios y datos orientados a eventos

<!-- unit: Propiedad de datos en microservicios -->

<!-- goals -->

- Explicar database-per-service y por qué fallan las bases compartidas.
- Hacer analítica entre servicios sin acoplarse a sus internos.

<!-- concept -->

Los microservicios dividen los sistemas para que los equipos cambien de forma independiente, y eso solo funciona si cada servicio es dueño de sus datos. Una base compartida acopla a todos a un esquema; el cambio de un equipo rompe a los demás.
La misma lógica aplica a la analítica. Leer las tablas internas de los servicios vuelve al equipo de datos un consumidor oculto de cada cambio de esquema. Contratos, eventos publicados o streams de CDC con formas acordadas dejan evolucionar a los servicios mientras la analítica sigue funcionando.

<!-- example -->

```text
orders-service ─ its own DB ─► publishes OrderPlaced v2 (contract) ─► Kafka ─► lake
payments-service ─ its own DB ─► CDC on the outbox table only     ─► Kafka ─► lake
data team reads contracts, not internal tables
```

#### ¿Qué diferencia hay entre eventos, comandos y mensajes?

Un comando pide a alguien que haga algo (`ShipOrder`) y puede rechazarse; un evento indica que algo ocurrió (`OrderShipped`) y es inmutable; mensaje es el envoltorio genérico que transporta cualquiera de los dos.

#### ¿Qué es event sourcing?

Guardar el estado de una entidad como la secuencia de eventos que lo modificaron, en lugar del estado actual; el estado actual se reconstruye reproduciendo los eventos. Da un log de auditoría completo y viaje en el tiempo, pero complica las consultas y la evolución del esquema.

#### ¿Qué es CQRS?

Command Query Responsibility Segregation: separar el modelo de escritura (comandos, validación) de los modelos de lectura (vistas optimizadas para consultas), a menudo actualizados de forma asíncrona a partir de eventos. Escala lecturas y escrituras de forma independiente y encaja con event sourcing.

#### ¿Qué es el patrón transactional outbox?

Un servicio escribe su cambio de negocio y un registro de evento en una tabla outbox en la misma transacción de base de datos; un proceso aparte (a menudo CDC) publica los registros del outbox en el broker. Evita el problema de la doble escritura de actualizar la base y publicar un evento por separado.

#### ¿Qué es el problema de la doble escritura?

Cuando un servicio escribe en su base y publica un evento como dos operaciones separadas, una puede tener éxito y la otra fallar, dejando los sistemas incoherentes. El outbox o la publicación basada en CDC lo resuelven.

#### ¿Qué es el patrón saga?

Una forma de ejecutar transacciones de negocio que abarcan varios servicios como una secuencia de transacciones locales con acciones compensatorias ante fallos, coordinadas por coreografía (eventos) u orquestación (un coordinador), en lugar de commits distribuidos en dos fases.

<!-- challenge -->

Los pipelines del equipo de datos se rompen cada vez que un servicio renombra una columna. ¿Qué acuerdo propones a los equipos de servicios?

<!-- solution -->

Cada servicio publica eventos de integración o una vista expuesta por CDC con un contrato versionado, registrado en un schema registry con chequeos de compatibilidad. Las tablas internas cambian libremente; los cambios de contrato pasan por versionado.

<!-- takeaways -->

- Cada servicio es dueño de sus datos.
- Las bases compartidas acoplan a los equipos.
- La analítica debe consumir contratos, no internos.

<!-- unit: Eventos y comandos -->

<!-- goals -->

- Distinguir eventos, comandos y mensajes.
- Diseñar y versionar eventos de los que otros puedan depender.

<!-- concept -->

Los sistemas orientados a eventos comunican hechos. Un comando pide a un servicio hacer algo y puede rechazarse; un evento afirma que algo ya pasó y no se discute. Los hechos son buena integración porque se pueden agregar consumidores sin cambiar al productor.
Eso vuelve los eventos interfaces públicas. Necesitan nombres claros, IDs, timestamps y esquemas, una decisión entre llevar datos o referencias, y reglas de versionado que mantengan funcionando a los consumidores viejos.

<!-- example -->

```json
{
  "event_id": "0192f0c3-7a1e-7b3c-9d4e-5f6a7b8c9d0e",
  "event_type": "OrderPlaced",
  "schema_version": 2,
  "occurred_at": "2026-10-17T09:41:12Z",
  "order_id": 98123,
  "customer_id": 552,
  "total_amount": "129.90",
  "currency": "EUR"
}
```

#### ¿Qué papel cumple el CDC en la integración de datos de microservicios?

El CDC lee el log de la base de cada servicio y publica los cambios como eventos sin modificar los servicios, alimentando la analítica y otros servicios; es más simple que añadir eventos a código heredado, pero expone los esquemas internos salvo que se use un outbox o un contrato.

#### ¿Qué son los eventos de dominio frente a los eventos de integración?

Los eventos de dominio son internos al modelo de un servicio; los de integración son contratos publicados para otros servicios y la analítica, estables y versionados, desacoplados a propósito de los esquemas internos.

#### ¿Qué papel cumple un API gateway en el acceso a los datos?

Un punto de entrada único para las solicitudes de los clientes que enruta a los servicios y se encarga de la autenticación, los límites de solicitudes y la agregación. Para los productos de datos, las APIs o capas GraphQL exponen datos curados a las aplicaciones.

#### ¿Cómo se deben diseñar los eventos?

Nombrados en pasado, con un esquema claro, un ID de evento, marcas de tiempo (del evento y de publicación), la clave de la entidad, una versión y suficientes datos para los consumidores (eventos gruesos) o una referencia para buscar los detalles (eventos delgados), evolucionando de forma compatible.

#### ¿Qué son los eventos delgados frente a los gruesos?

Los eventos delgados solo llevan identificadores y el tipo de cambio, así que los consumidores deben consultar los detalles (acoplamiento, carga sobre el productor); los gruesos (event-carried state transfer) llevan todo el estado necesario, lo que permite consumidores autónomos a costa de mensajes más grandes y de cuidar el esquema.

#### ¿Cómo se versionan los esquemas de eventos?

Con un schema registry con reglas de compatibilidad, añadiendo campos opcionales en lugar de cambiar significados, introduciendo tipos o versiones de evento nuevos para los cambios que rompen y conservando las versiones viejas hasta que migren todos los consumidores.

<!-- challenge -->

Un equipo quiere renombrar `total` a `total_amount` en un evento que consumen seis servicios. ¿Cómo lo hace con seguridad?

<!-- solution -->

Agregar `total_amount` como campo opcional nuevo sin dejar de enviar `total`, registrar el esquema compatible hacia atrás, migrar a los consumidores y quitar `total` en una nueva versión major tras un periodo de deprecación.

<!-- takeaways -->

- Los comandos piden; los eventos afirman hechos.
- Los eventos de integración son contratos públicos.
- Versiona los eventos con reglas de compatibilidad.

<!-- unit: Consistencia entre servicios -->

<!-- goals -->

- Evitar el problema de la doble escritura con el patrón outbox y CDC.
- Coordinar procesos entre servicios con sagas, event sourcing y CQRS.

<!-- concept -->

Sin transacciones compartidas, mantener consistentes los servicios se vuelve un problema de diseño. Escribir en una base y publicar un evento por separado puede perder uno de los dos; el patrón outbox escribe ambos en una transacción local y publica después, a menudo con CDC.
Los procesos más largos se vuelven sagas de pasos locales con compensaciones. Event sourcing guarda el estado como su historia de eventos, y CQRS separa los modelos de escritura y lectura; ambos sirven cuando la auditoría o el rendimiento de lectura justifican su complejidad.

<!-- example -->

```sql
BEGIN;
UPDATE orders SET status = 'paid' WHERE order_id = 98123;
INSERT INTO outbox (event_id, type, payload) VALUES (gen_random_uuid(), 'OrderPaid', '{"order_id":98123}');
COMMIT;
-- CDC (Debezium) publishes outbox rows to Kafka
```

#### ¿Qué es la coreografía frente a la orquestación?

En la coreografía, los servicios reaccionan a los eventos de los demás sin un coordinador central (bajo acoplamiento, más difícil ver el flujo completo); en la orquestación, un coordinador les dice a los servicios qué hacer (flujo claro, dependencia central). Los pipelines de datos suelen usar orquestación (Airflow); las sagas de microservicios usan cualquiera de las dos.

#### ¿Qué es el data mesh?

El enfoque sociotécnico de Zhamak Dehghani con cuatro principios: propiedad de los datos orientada al dominio, datos como producto, una plataforma de datos de autoservicio y gobierno computacional federado. Descentraliza la propiedad de los datos hacia los dominios que los conocen.

#### ¿Qué problema intenta resolver el data mesh?

Que los equipos de datos centrales se conviertan en cuellos de botella entre muchos dominios de origen y muchos consumidores, perdiendo el contexto del dominio y escalando mal a medida que crece la organización.

#### ¿Qué es un producto de datos en el data mesh?

Un dataset de un dominio expuesto para su consumo, con un responsable, una interfaz (tablas, APIs, eventos), documentación, garantías de calidad y SLA, facilidad de descubrimiento, seguridad y versionado, construido sobre la plataforma compartida.

#### ¿Qué es el gobierno computacional federado?

Un gobierno en el que los estándares globales (interoperabilidad, seguridad, privacidad, métricas de calidad) los acuerda una federación de representantes de los dominios y la plataforma, y la plataforma los aplica automáticamente (políticas como código), mientras los dominios deciden localmente dentro de esas reglas.

#### ¿Qué papel cumple el equipo de plataforma en un data mesh?

Proveer infraestructura de autoservicio (almacenamiento, cómputo, pipelines, catálogo, control de acceso, observabilidad, plantillas) para que los equipos de dominio construyan productos de datos sin ser expertos en la plataforma.

#### ¿Cuándo no encaja el data mesh?

En organizaciones pequeñas, con pocos dominios, baja madurez de datos o sin capacidad en los dominios para hacerse cargo de productos de datos. Sin inversión en la plataforma y en el gobierno, el mesh se convierte en datos fragmentados e incoherentes.

<!-- challenge -->

Un servicio de órdenes actualiza su base y luego publica un evento en Kafka. A veces, tras una caída, el evento no aparece. ¿Qué patrón lo arregla?

<!-- solution -->

El transactional outbox: escribir el evento en una tabla outbox en la misma transacción que la actualización de la orden, y publicarlo desde el outbox (con CDC o un relay), para que ocurran ambos o ninguno.

<!-- takeaways -->

- Escrituras separadas a la base y al broker pueden divergir.
- El patrón outbox las vuelve atómicas.
- Las sagas coordinan; event sourcing y CQRS encajan en necesidades puntuales.

### Data mesh y data fabric

<!-- unit: Patrones de integración -->

<!-- goals -->

- Comparar ETL, ELT, CDC, eventos, virtualización y reverse ETL.
- Elegir un patrón de integración por fuente.

<!-- concept -->

Hay apenas un puñado de formas de mover datos, y cada fuente merece la adecuada. Las extracciones batch sirven a fuentes que cambian poco o no ofrecen más. CDC captura cada cambio de las bases con poco impacto. Los eventos sirven a sistemas que ya publican hechos. La virtualización evita copiar cuando las consultas son raras. El reverse ETL devuelve datos modelados a las herramientas operativas.
ELT se volvió lo estándar porque el almacenamiento y los motores en la nube abarataron cargar primero y transformar donde caen los datos.

<!-- example -->

| Fuente | Patrón |
|---|---|
| PostgreSQL de producción | CDC |
| CRM SaaS | Conector administrado, incremental |
| CSV que deja un socio | Ingesta batch de archivos |
| Microservicio con eventos de dominio | Stream de eventos |
| Scores de clientes de vuelta al CRM | Reverse ETL |

#### ¿Qué es un data fabric?

Una arquitectura que usa metadatos, grafos de conocimiento, automatización y virtualización para integrar datos de fuentes distribuidas y presentar una capa de acceso unificada y gobernada, poniendo el énfasis en la tecnología (metadatos activos) más que en la organización.

#### ¿Qué diferencia hay entre data mesh y data fabric?

El data mesh es sobre todo organizacional (quién es dueño de los datos, pensamiento de producto), con descentralización; el data fabric es sobre todo tecnológico (integración mediante metadatos y automatización), a menudo centralizado. Se pueden combinar.

#### ¿Cómo se empieza un camino hacia el data mesh?

Eligiendo uno o dos dominios motivados con consumidores claros, construyendo una plataforma de autoservicio mínima (plantillas, catálogo, control de acceso, calidad), definiendo unos pocos estándares globales, entregando productos de datos de punta a punta, midiendo la adopción y luego ampliando.

#### ¿Cómo siguen siendo interoperables los productos de datos en un mesh?

Mediante estándares globales: identificadores y datos de referencia compartidos, convenciones de nombres y metadatos, formatos y métodos de acceso comunes, métricas de calidad y un catálogo central para el descubrimiento.

#### ¿Qué métricas muestran que un data mesh funciona?

El tiempo para entregar nuevos productos de datos, el número de productos con consumidores activos, el cumplimiento de los SLO de calidad, la reducción de las solicitudes al equipo central, la reutilización entre dominios y la satisfacción de los consumidores.

<!-- challenge -->

Un equipo corre cada noche una exportación completa de una base de producción de 2 TB que tarda 6 horas y vuelve lenta la app. ¿Qué propones?

<!-- solution -->

Pasar a CDC: un snapshot inicial seguido de captura de cambios desde el log de la base, que carga solo los cambios con bajo impacto en la fuente y da datos más frescos.

<!-- takeaways -->

- Elige el patrón de integración por fuente.
- ELT carga primero y transforma en la plataforma.
- El reverse ETL cierra el ciclo hacia las herramientas operativas.

<!-- unit: Ingestar con confiabilidad -->

<!-- goals -->

- Ingestar desde APIs, archivos y proveedores con contratos.
- Manejar datos tardíos y escalar la ingesta con diseños guiados por metadatos.

<!-- concept -->

La ingesta es donde los problemas de sistemas externos se vuelven tuyos: límites de tasa, archivos faltantes, esquemas cambiados, registros tardíos. Los contratos fijan expectativas por adelantado: esquemas, horarios de entrega, señales de completitud y a quién llamar. Las cargas idempotentes basadas en upsert absorben datos tardíos y repetidos.
Cuando las fuentes se multiplican, construir un pipeline por fuente deja de escalar. Un componente genérico y probado, configurado por metadatos, ingesta cada fuente nueva con una entrada de configuración en lugar de código nuevo.

<!-- example -->

```yaml
# sources.yaml driving one generic ingestion job
- name: crm_accounts
  type: api
  endpoint: /v2/accounts
  incremental_key: updated_at
  primary_key: id
  schedule: hourly
- name: partner_sales
  type: s3_files
  path: s3://landing/partner/sales/
  format: csv
  completeness_marker: _SUCCESS
```

#### ¿Qué son los "metadatos activos"?

Metadatos que disparan automatizaciones en lugar de solo documentar: etiquetas que aplican enmascaramiento, linaje que lanza alertas ante cambios en el origen, estadísticas de uso que sugieren retirar datasets, métricas de calidad que bloquean la publicación.

#### ¿Cuáles son los principales patrones de integración de datos?

ETL/ELT batch, captura de cambios (CDC), streaming de eventos, integración por APIs, virtualización/federación de datos, transferencia de archivos y reverse ETL para devolver datos curados a las herramientas operativas.

#### ¿Qué es ELT y por qué se volvió dominante?

Cargar primero los datos en bruto en almacenamiento en la nube o en warehouses escalables y transformarlos allí con SQL (a menudo con dbt). El almacenamiento barato y el cómputo elástico lo hicieron más simple y flexible que transformar antes de cargar.

#### ¿Qué es la virtualización de datos?

Consultar los datos donde están mediante una capa lógica (Denodo, Trino, consultas federadas) sin copiarlos. Es rápida de montar y evita duplicados, pero el rendimiento, el historial y la carga sobre las fuentes son limitaciones.

#### ¿Qué es el reverse ETL?

Sincronizar datos modelados del warehouse hacia sistemas operativos (CRM, marketing, herramientas de soporte) para que los equipos de negocio actúen sobre la analítica, cerrando el ciclo entre análisis y operación.

#### ¿Qué hay que tener en cuenta al ingerir desde APIs?

La autenticación, la paginación, los límites de solicitudes y los reintentos con espera, la extracción incremental (cursores, updated-since), la deriva del esquema, la idempotencia, guardar las respuestas en bruto para reprocesar y monitorear los cambios silenciosos de la API.

<!-- challenge -->

Un socio a veces sube medio archivo, y el pipeline lo carga antes de que llegue el resto. ¿Qué acuerdas con él y qué cambias?

<!-- solution -->

Acordar una señal de completitud en el contrato de landing (un manifest o un archivo `_SUCCESS` escrito al final, con conteos de filas), y hacer que el pipeline arranque solo cuando esté presente y los conteos coincidan.

<!-- takeaways -->

- Los contratos fijan expectativas con los productores.
- Los upserts idempotentes absorben datos tardíos y repetidos.
- La ingesta guiada por metadatos escala a muchas fuentes.

<!-- stage: Organizar y gobernar -->

### Integración e ingesta

<!-- unit: Principios del data mesh -->

<!-- goals -->

- Explicar los cuatro principios del data mesh y el problema que aborda.
- Describir productos de datos, gobierno federado y el equipo de plataforma.

<!-- concept -->

Los equipos de datos centrales se vuelven cuello de botella cuando muchos dominios producen datos y muchos consumidores los necesitan. El data mesh pasa la propiedad a los dominios que conocen los datos, les pide publicarlos como productos con garantías, les da una plataforma self-serve para que no construyan infraestructura cada uno y mantiene estándares globales con gobierno federado.
Es más un cambio organizacional que técnico: lo difícil es dar a los dominios las habilidades, los incentivos y la capacidad para ser dueños de datos.

<!-- example -->

| Principio | En la práctica |
|---|---|
| Propiedad por dominio | El equipo de pagos es dueño de los datos de pagos |
| Datos como producto | `payments.transactions` con SLA, docs y dueño |
| Plataforma self-serve | Plantillas para pipelines, catálogo y accesos |
| Gobierno federado | Reglas globales sobre IDs, PII y métricas de calidad |

#### ¿Qué es un contrato de datos en la integración?

Un acuerdo explícito y versionado sobre el esquema, la semántica, la calidad y los SLA de un dataset o un evento entre el productor y los consumidores, validado en CI y en ejecución, que hace visibles los cambios que rompen antes de que rompan los pipelines.

#### ¿Cómo se manejan los datos tardíos y desordenados en la integración?

Usando las marcas de tiempo del evento, permitiendo ventanas de retraso, diseñando upserts y escrituras idempotentes, reprocesando las particiones recientes y midiendo la completitud de los datos para que los consumidores sepan cuándo un periodo es definitivo.

#### ¿Cómo se elige entre CDC, extracciones batch y eventos para una fuente?

CDC para bases que no puedes cambiar y de las que necesitas todos los cambios con baja latencia y poco impacto; extracciones batch para datos pequeños o que cambian poco y fuentes sin acceso al log; eventos cuando controlas la aplicación y quieres semántica de negocio.

#### ¿Qué son los conectores administrados y cuándo tienen sentido?

Servicios como Fivetran, Airbyte Cloud, Lakeflow Connect o AppFlow que extraen de aplicaciones SaaS y bases de datos con conectores mantenidos y manejo del esquema. Ahorran tiempo de ingeniería en las fuentes estándar a un costo por volumen; el código propio tiene sentido para fuentes inusuales o volúmenes enormes.

#### ¿Cómo se diseña la ingesta para muchas fuentes parecidas?

Con pipelines guiados por metadatos: un componente de ingesta genérico y probado, configurado por fuente (conexión, tablas, claves, programación) desde una tabla o archivos de configuración, en lugar de un pipeline escrito a mano para cada fuente.

<!-- challenge -->

Una empresa anuncia "estamos haciendo data mesh" renombrando tablas a `<domain>_*`. ¿Qué falta?

<!-- solution -->

Propiedad y capacidad en los dominios, garantías de producto (SLAs, documentación, calidad), una plataforma self-serve y estándares globales aplicados automáticamente. Renombrar no cambia en nada quién responde.

<!-- takeaways -->

- El mesh pasa la propiedad a los dominios.
- Los productos de datos tienen dueños y garantías.
- Una plataforma y el gobierno federado lo hacen viable.

<!-- unit: Adoptar un data mesh -->

<!-- goals -->

- Decidir si el data mesh encaja en una organización.
- Empezar pequeño y medir si funciona.

<!-- concept -->

El data mesh resuelve un problema de escala y organización, así que las empresas pequeñas o los dominios inmaduros suelen recibir sus costos sin sus beneficios. Donde encaja, empezar pequeño funciona mejor: uno o dos dominios motivados con consumidores reales, una plataforma mínima y estándares que crecen con la experiencia.
La interoperabilidad evita que un mesh se vuelva muchos silos: identificadores, convenciones y contratos compartidos. Las métricas muestran si funciona, en velocidad de entrega, adopción de los consumidores y calidad.

<!-- example -->

| Métrica | Señal |
|---|---|
| Lead time de un nuevo producto de datos | Baja de meses a semanas |
| Productos con consumidores activos | En aumento |
| SLOs de calidad cumplidos | Por encima del 95 % |
| Solicitudes al equipo central | En descenso |

#### ¿Qué es un contrato de aterrizaje con proveedores de datos externos?

Un acuerdo sobre los formatos de archivo, los nombres, el calendario de entrega, las señales de completitud (manifiestos o archivos `_SUCCESS`), la codificación, el aviso de cambios de esquema y el manejo de errores, que evita la mayoría de los incidentes de ingesta de archivos.

#### ¿Qué es el gobierno de datos?

El marco de roles, políticas, estándares y procesos que garantiza que los datos sean exactos, seguros, conformes, comprensibles y se usen de forma apropiada, incluidos la propiedad, la custodia (stewardship), la clasificación, el acceso, la calidad y el ciclo de vida.

#### ¿Qué son los data owners y los data stewards?

Los data owners responden por un dominio de datos (decisiones sobre acceso, definiciones, metas de calidad); los data stewards manejan en el día a día las definiciones, los problemas de calidad y los metadatos, junto con los ingenieros que implementan los controles.

#### ¿Qué es la gestión de metadatos?

Recoger y administrar metadatos técnicos, de negocio y operativos (esquemas, definiciones, linaje, calidad, uso) para facilitar el descubrimiento, el análisis de impacto, el gobierno y la automatización; los "metadatos activos" los usan para disparar acciones.

<!-- challenge -->

Dos dominios publican datos de clientes con IDs distintos y es imposible cruzarlos. ¿Qué principio del mesh falló y cómo lo arreglas?

<!-- solution -->

El gobierno federado en interoperabilidad: define un identificador global de cliente (o un servicio de mapeo) como estándar que todo producto debe exponer, aplicado con chequeos de la plataforma.

<!-- takeaways -->

- El mesh encaja en organizaciones grandes y con muchos dominios.
- Empieza con pocos dominios y consumidores reales.
- Los identificadores globales mantienen interoperables los productos.

<!-- unit: Data fabric y metadatos activos -->

<!-- goals -->

- Explicar el data fabric y en qué se diferencia del data mesh.
- Usar metadatos activos para automatizar el gobierno.

<!-- concept -->

El data fabric aborda el mismo problema de integración desde la tecnología: metadatos ricos, automatización y virtualización conectan los datos donde viven, con menos énfasis en quién es dueño. El mesh pregunta quién responde; el fabric, cómo hacer los datos encontrables y usables automáticamente. Pueden coexistir.
El hilo común son los metadatos activos: etiquetas y linaje que no solo documentan sino que actúan, aplicando enmascaramiento, enrutando alertas o recomendando datasets.

<!-- example -->

```text
column customers.email tagged pii=true
  → masking policy applied automatically for non-privileged roles
  → lineage propagates the tag to downstream copies
  → quality alert routed to the owner listed in the catalog
```

#### ¿Qué es el linaje de datos y cómo se captura?

El flujo de los datos desde las fuentes, a través de las transformaciones, hasta los consumidores. Se captura analizando el SQL y los jobs (dbt, Unity Catalog, eventos OpenLineage de Airflow y Spark) y se muestra a nivel de tabla y de columna para el análisis de impacto y las auditorías.

#### ¿Qué es OpenLineage?

Un estándar abierto para los eventos de linaje que emiten los orquestadores y motores (Airflow, Spark, dbt, Flink), que describen los jobs, las ejecuciones y los datasets de entrada y salida, y que recogen backends como Marquez o los catálogos.

#### ¿Qué es la clasificación de datos?

Etiquetar los datos por sensibilidad (público, interno, confidencial, restringido) y tipo (datos personales, financieros, de salud), a menudo de forma automática con escáneres, para guiar las políticas de acceso, el enmascaramiento, la retención y el cumplimiento.

<!-- challenge -->

Siguen apareciendo tablas nuevas con datos personales sin enmascarar. ¿Cómo ayudan los metadatos activos?

<!-- solution -->

Clasifica las columnas automáticamente (escáneres o reglas de nombres) y asígnales etiquetas, y luego ata las políticas de enmascaramiento y acceso a las etiquetas, para que cualquier columna etiquetada nueva quede protegida sin trabajo manual. Propaga las etiquetas por el linaje.

<!-- takeaways -->

- El fabric automatiza la integración mediante metadatos.
- El mesh es organizacional; el fabric, tecnológico.
- Los metadatos activos convierten etiquetas en políticas aplicadas.

### Gobierno, metadatos y calidad

<!-- unit: Roles, políticas y definiciones -->

<!-- goals -->

- Definir roles, políticas y madurez del gobierno.
- Usar un glosario de negocio y evitar datasets duplicados.

<!-- concept -->

El gobierno responde "¿quién decide?" sobre los datos: quién accede, qué significan los términos, qué calidad es aceptable. Los dueños responden por ellos; los stewards mantienen definiciones y calidad en el día a día. Sin estos roles, cada pregunta se vuelve una reunión.
Las definiciones acordadas evitan la falla más visible: dos reportes con cifras distintas para la misma métrica. Un glosario las registra, y los datasets certificados y fáciles de encontrar evitan que los equipos construyan sus propias copias.

<!-- example -->

| Término | Definición | Dueño |
|---|---|---|
| Cliente activo | Hizo una orden en los últimos 90 días | Sales ops |
| Ingreso neto | Bruto menos devoluciones, descuentos e impuestos | Finanzas |

#### ¿Qué es la gestión de datos maestros (MDM)?

Crear un registro único y confiable de las entidades centrales (cliente, producto, proveedor) entre sistemas mediante reglas de emparejamiento, fusión y supervivencia, distribuido a los sistemas operativos y analíticos.

#### ¿Qué son los datos de referencia?

Conjuntos de códigos y clasificaciones relativamente estáticos usados por muchos sistemas (códigos de país, monedas, códigos de actividad económica, valores de estado); administrarlos de forma central evita códigos inconsistentes.

#### ¿Cómo se incorpora la calidad de datos en una arquitectura?

Definiendo dimensiones de calidad y SLA por producto de datos, validando en la ingesta (esquemas, contratos), probando las transformaciones (unicidad, integridad, reglas de negocio), bloqueando la publicación ante fallos, monitoreando anomalías y frescura, poniendo en cuarentena los registros malos y asignando responsables para resolver los problemas.

#### ¿Cómo se mide la madurez del gobierno de datos?

Por la cobertura de responsables, las definiciones documentadas, la clasificación de los datos sensibles, las políticas de acceso como código, el linaje, los SLO de calidad, los procesos de incidentes y la frecuencia con que los consumidores encuentran datos y confían en ellos sin tener que preguntar.

#### ¿Qué es un glosario de negocio?

Una lista curada de términos de negocio con sus definiciones acordadas (cliente activo, ingreso neto, churn), vinculados a datasets y métricas en el catálogo, que alinea a los equipos sobre el significado.

<!-- challenge -->

Marketing y finanzas reportan a la junta cifras distintas de "clientes activos". ¿Qué paso de gobierno lo resuelve?

<!-- solution -->

Que los dueños de negocio acuerden una definición en el glosario, implementarla una vez en un modelo certificado, apuntar ambos reportes a él y etiquetar cualquier variante con un nombre distinto.

<!-- takeaways -->

- El gobierno asigna decisiones a dueños y stewards.
- Un glosario fija definiciones compartidas.
- Los datasets certificados y encontrables evitan copias.

<!-- unit: Metadatos y linaje -->

<!-- goals -->

- Manejar metadatos técnicos, de negocio y operativos.
- Capturar el linaje y clasificar los datos.

<!-- concept -->

Los metadatos convierten un montón de tablas en algo que la gente puede usar: qué existe, qué significa, quién es dueño, qué tan fresco está y de dónde vino. El linaje, el mapa de las fuentes a los consumidores pasando por las transformaciones, responde preguntas de impacto antes de un cambio y de causa raíz después de un incidente.
Lo mejor es capturar el linaje automáticamente desde las herramientas que mueven datos. La clasificación agrega etiquetas de sensibilidad, que guían las políticas de acceso.

<!-- example -->

```text
crm.accounts ─► bronze.accounts ─► silver.customers ─► gold.dim_customer
                                                    └► gold.churn_features ─► churn model
change silver.customers.segment → impact: 2 gold tables, 1 model, 4 dashboards
```

#### ¿Cómo se evitan los datasets duplicados?

Haciendo descubribles los datasets existentes (catálogo, búsqueda), certificando los autorizados, exigiendo un responsable y una revisión para los nuevos datasets publicados, monitoreando el uso y retirando las copias.

#### ¿Cuáles son las capas de la seguridad de datos?

La gestión de identidades y accesos (autenticación, autorización de mínimo privilegio), el aislamiento de red, el cifrado en reposo y en tránsito, la gestión de claves, el enmascaramiento y la tokenización, la seguridad a nivel de fila y columna, la auditoría y el monitoreo, y las prácticas de desarrollo seguro.

#### ¿Qué diferencia hay entre RBAC y ABAC?

El control de acceso basado en roles concede permisos a roles asignados a usuarios; el basado en atributos evalúa en las políticas atributos de los usuarios, los recursos y el contexto (departamento, clasificación de los datos, ubicación), lo que escala mejor para reglas detalladas (por ejemplo, políticas por etiquetas).

#### ¿Qué es la seudonimización frente a la anonimización?

La seudonimización reemplaza los identificadores por tokens o hashes que se pueden volver a vincular con información adicional (siguen siendo datos personales según el RGPD); la anonimización impide de forma irreversible la identificación (dejan de ser datos personales), algo difícil de lograr en la práctica.

<!-- challenge -->

Antes de quitar una columna en silver, un ingeniero pregunta qué se podría romper. ¿Cómo responde la arquitectura?

<!-- solution -->

El linaje a nivel de columna en el catálogo (capturado automáticamente con OpenLineage o parseo de consultas) lista las tablas, modelos y dashboards aguas abajo que la usan, con los dueños a quienes avisar.

<!-- takeaways -->

- Los metadatos hacen los datos encontrables y comprensibles.
- El linaje responde preguntas de impacto y causa raíz.
- La clasificación guía el acceso y la protección.

<!-- unit: Datos maestros y calidad -->

<!-- goals -->

- Manejar datos maestros y de referencia.
- Incorporar la calidad de datos a la arquitectura.

<!-- concept -->

Entidades clave como cliente y producto aparecen en muchos sistemas, cada uno con su versión. La gestión de datos maestros crea un registro confiable y relaciona los demás con él; los datos de referencia, como códigos de país o moneda, necesitan la misma fuente única.
La calidad funciona igual en cada capa: define qué es "bueno" por producto de datos, valida temprano en la ingesta, prueba las transformaciones, monitorea las salidas y pon en cuarentena lo que falle en vez de publicarlo.

<!-- example -->

| Capa | Chequeo de calidad |
|---|---|
| Ingesta | Validación de esquema y contrato |
| Silver | Unicidad, nulos, integridad referencial |
| Gold | Reglas de negocio, conciliación con totales de la fuente |
| Monitoreo | Frescura, volumen, cambios de distribución |

#### ¿Qué es la tokenización?

Reemplazar valores sensibles (números de tarjeta, documentos de identidad) por tokens no sensibles, guardando la correspondencia en una bóveda segura, para que la mayoría de los sistemas nunca maneje los valores reales.

#### ¿Cómo afectan el RGPD y las leyes de protección de datos a la arquitectura de datos?

Exigen una base legal y limitación de la finalidad, minimización de los datos, límites de retención, seguridad, registros del tratamiento y atender los derechos de los titulares (acceso, rectificación, supresión), lo que implica saber dónde están los datos personales (linaje, catálogo) y poder borrarlos de todas las capas. En Colombia, la Ley 1581 de 2012 de habeas data plantea obligaciones similares.

#### ¿Cómo se implementa el derecho de supresión en un lakehouse?

Rastreando dónde están los datos de cada persona, usando formatos de tabla que admiten borrados (Delta, Iceberg), borrando en todas las capas, haciendo vacuum de los archivos viejos tras la retención, evitando copiar ampliamente los identificadores en bruto (seudonimizar pronto) y documentando el proceso y sus plazos.

<!-- challenge -->

El mismo cliente aparece tres veces con nombres un poco distintos entre CRM, facturación y soporte. ¿Cómo le das a la analítica un solo cliente?

<!-- solution -->

Crea un cliente maestro con reglas de emparejamiento (o matching con ML) entre fuentes, asigna un ID dorado, conserva una tabla de referencias cruzadas con los IDs de origen y construye `dim_customer` desde el registro maestro.

<!-- takeaways -->

- MDM crea un registro confiable por entidad.
- Los datos de referencia necesitan una fuente única.
- Valida en cada capa; pon en cuarentena las fallas.

### Seguridad y cumplimiento

<!-- unit: Acceso y protección -->

<!-- goals -->

- Construir la seguridad de datos por capas, de la identidad al monitoreo.
- Elegir entre RBAC y ABAC y aplicar zero trust.

<!-- concept -->

La seguridad de datos funciona por capas, para que una falla no lo exponga todo: identidad y mínimo privilegio, aislamiento de red, cifrado, acceso fino a filas y columnas, gestión de secretos y monitoreo. Cada capa asume que las otras pueden fallar.
Cuando las plataformas crecen, el acceso por roles se vuelve una selva de roles. El acceso por atributos otorga según etiquetas y atributos del usuario, y escala mejor. Zero trust deja de usar la ubicación en la red como razón para confiar en algo.

<!-- example -->

```text
RBAC: role finance_analyst → SELECT on finance.*
ABAC: allow SELECT where table.domain IN user.domains
      AND (column.pii = false OR user.clearance = 'pii')
```

#### ¿Qué es la residencia de los datos?

Requisitos que obligan a guardar y procesar ciertos datos en jurisdicciones concretas, lo que afecta la elección de regiones, la replicación, la ubicación de los respaldos y los servicios que se pueden usar.

#### ¿Qué es zero trust en las plataformas de datos?

No confiar nunca por la ubicación en la red: todo acceso se autentica, se autoriza con el mínimo privilegio y se audita, con credenciales de corta duración, identidades de carga de trabajo y verificación continua.

#### ¿Cómo se administran los secretos en las plataformas de datos?

Guardándolos en un gestor de secretos (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault, secret scopes de Databricks), prefiriendo las identidades de carga de trabajo y las credenciales de corta duración a las claves estáticas, rotándolos automáticamente y sin subirlos nunca a Git.

#### ¿Qué es la prevención de pérdida de datos (DLP)?

Herramientas y políticas que detectan y bloquean la salida de datos sensibles fuera de los límites aprobados (correos, exportaciones, buckets públicos), a menudo buscando patrones como números de tarjeta o de documentos de identidad.

#### ¿Cómo se comparten datos con socios externos de forma segura?

Compartiendo datasets curados y mínimos con mecanismos gobernados (Delta Sharing, shares de Snowflake, acceso prefirmado con vencimiento) en lugar de volcados de archivos, aplicando restricciones de filas y columnas, definiendo el uso por contrato y auditando el acceso.

<!-- challenge -->

El warehouse tiene 400 roles, muchos superpuestos, y las revisiones de acceso tardan semanas. ¿Qué propones?

<!-- solution -->

Pasar a acceso por atributos: etiquetar tablas y columnas (dominio, sensibilidad), dar atributos a los usuarios (equipo, nivel de autorización) y escribir unas pocas políticas sobre etiquetas. Conservar un conjunto pequeño de roles funcionales.

<!-- takeaways -->

- Combina identidad, red, cifrado, acceso y monitoreo.
- ABAC escala mejor que muchos roles.
- Zero trust autentica cada acceso.

<!-- unit: Privacidad y cumplimiento -->

<!-- goals -->

- Aplicar seudonimización, anonimización y tokenización.
- Diseñar para GDPR, borrado, residencia y compartición segura.

<!-- concept -->

Las leyes de privacidad moldean la arquitectura. Recoge solo lo necesario, consérvalo solo el tiempo necesario y sabe dónde viven los datos de cada persona. La seudonimización reduce la exposición pero sigue siendo dato personal; solo la anonimización real escapa de la regulación, y es más difícil de lo que parece.
Derechos como el borrado necesitan soporte técnico: formatos de tabla que borren filas, un mapa de dónde viven los identificadores y procesos que también limpien backups y copias. La residencia y la compartición externa agregan reglas sobre adónde pueden ir los datos.

<!-- example -->

```sql
-- erasure request on a lakehouse (Delta/Iceberg)
DELETE FROM silver.customers WHERE customer_id = 552;
DELETE FROM silver.orders    WHERE customer_id = 552;
-- then remove old file versions after retention
VACUUM silver.customers; VACUUM silver.orders;
```

#### ¿Qué son los SLA, SLO y SLI de datos?

Los SLI son indicadores medidos (frescura, completitud, tasa de éxito de los pipelines); los SLO son metas para ellos (datos listos a las 7 a. m. el 99 % de los días); los SLA son compromisos con los consumidores con consecuencias. Hacen medible la confiabilidad de los datos.

#### ¿Qué es la observabilidad de datos?

Monitorear la frescura, el volumen, el esquema, la distribución y el linaje de los datos (no solo el estado de los jobs) para detectar rápido los incidentes y encontrar su causa raíz, a menudo con detección automática de anomalías.

#### ¿Cómo se diseñan pipelines para el fallo?

Suponiendo que habrá fallos: pasos idempotentes y reiniciables, reintentos con espera para los errores transitorios, checkpoints para los streams, colas dead-letter para los registros malos, alertas con runbooks y la capacidad de hacer backfill de periodos concretos.

#### ¿Qué es una cola dead-letter?

Un lugar al que se envían, con la información del error, los mensajes o registros que no se pueden procesar (formato inválido, validación fallida), para que el pipeline continúe y los fallos se puedan revisar y reproducir después.

#### ¿Qué son el RPO y el RTO?

Recovery point objective: cuánta pérdida de datos es aceptable (tiempo entre el último estado recuperable y el fallo). Recovery time objective: cuánto puede tardar la recuperación. Determinan la frecuencia de los respaldos, la replicación y el diseño de la recuperación ante desastres.

#### ¿Qué es FinOps para las plataformas de datos?

La práctica de gestionar en colaboración los costos de los datos en la nube: visibilidad (etiquetas, costo por pipeline y equipo), optimización (dimensionamiento, auto-suspend, niveles de almacenamiento, ajuste de consultas, procesamiento incremental) y gobierno (presupuestos, alertas, rendición de cuentas).

<!-- challenge -->

Las tablas analíticas guardan correos de clientes en 40 lugares. Cada solicitud de borrado tarda una semana. ¿Cómo rediseñas?

<!-- solution -->

Seudonimiza temprano: reemplaza los correos por un token en silver, guarda el mapeo en una sola tabla protegida y deja que las tablas aguas abajo usen el token. El borrado elimina entonces el mapeo y las pocas fuentes crudas, y los tokens quedan sin vínculo.

<!-- takeaways -->

- Los datos seudonimizados siguen siendo datos personales.
- El borrado necesita formatos borrables y un mapa de identificadores.
- Las reglas de residencia y compartición limitan los flujos de datos.

<!-- stage: Operar y evolucionar -->

### Confiabilidad, operación y costos

<!-- unit: Niveles de servicio y observabilidad -->

<!-- goals -->

- Definir SLIs, SLOs y SLAs para productos de datos.
- Monitorear los datos con observabilidad y manejar incidentes.

<!-- concept -->

A los usuarios no les importa si un job terminó bien; les importa si los datos están frescos, completos y correctos. Los niveles de servicio lo vuelven medible: indicadores como la frescura, objetivos que fijan metas y acuerdos que las prometen a los consumidores.
La observabilidad de datos vigila los datos mismos y atrapa fallas silenciosas que los jobs en verde esconden. Cuando algo sale mal, la gestión de incidentes, con severidad, comunicación y postmortems, trata los datos como cualquier servicio de producción.

<!-- example -->

| SLI | SLO |
|---|---|
| Frescura de `gold.revenue` | Actualizada antes de las 07:00 el 99 % de los días |
| Completitud | Conteo de filas a ±5 % del promedio de 7 días |
| Éxito del pipeline | 99,5 % de las ejecuciones diarias |

#### ¿Cuáles son los mayores impulsores de costo en las plataformas de datos?

El cómputo de las transformaciones y las consultas (sobre todo clusters siempre encendidos y recálculos completos), las consultas ineficientes sobre muchos datos, la duplicación de datos entre capas y herramientas, la salida de datos y la transferencia entre regiones, y los datos sin uso guardados para siempre.

#### ¿Cómo se hace una plataforma eficiente en costos desde el diseño?

Con procesamiento incremental, particionado y clustering para el pruning, cómputo serverless o con autoescalado y auto-suspend, almacenamiento por niveles y retención, evitando copias innecesarias, eligiendo la latencia adecuada a la necesidad de negocio y haciendo visibles los costos por equipo.

#### ¿Qué papel cumple la infraestructura como código en la arquitectura de datos?

Definir las plataformas (almacenamiento, cómputo, permisos, catálogos, jobs) de forma declarativa en código (Terraform, CloudFormation, Bicep, bundles) para que los entornos sean reproducibles, revisados y auditables, y se pueda detectar la deriva.

#### ¿Qué es un incidente de datos y cómo se gestiona?

Cualquier evento en el que los datos están mal, llegan tarde o no están disponibles para los consumidores. Se gestiona como un incidente de software: detectar, evaluar el impacto, comunicar a los consumidores, mitigar (pausar la publicación, revertir), corregir la causa raíz y escribir un postmortem sin culpables con acciones.

<!-- challenge -->

Todos los jobs están en verde, pero un dashboard mostró cero ventas de una región toda la mañana. ¿Qué chequeo de observabilidad lo habría atrapado?

<!-- solution -->

Un chequeo de volumen o distribución sobre la salida (filas por región frente al histórico), que alerte cuando un segmento cae a cero, sin importar el estado del job.

<!-- takeaways -->

- Mide lo que sienten los usuarios: frescura, completitud, corrección.
- La observabilidad vigila datos, no solo jobs.
- Maneja los incidentes de datos como incidentes de software.

<!-- unit: Diseñar para las fallas -->

<!-- goals -->

- Diseñar pipelines que fallen de forma segura y se recuperen.
- Usar dead-letter queues, IaC y planeación de capacidad.

<!-- concept -->

Las fallas van a ocurrir; el diseño decide si son rutina o crisis. Los pasos idempotentes y reiniciables simplemente se reintentan. Los registros malos van a una dead-letter queue en lugar de detenerlo todo. La infraestructura en código se puede recrear. La planeación de capacidad evita que el crecimiento se vuelva una caída.
El objetivo es que ningún archivo, nodo o despliegue malo tumbe la plataforma o pierda datos.

<!-- example -->

```text
stream ─► parse/validate ─┬─► valid  ─► silver
                          └─► invalid ─► dead-letter topic (with error, source, offset)
                                         └─► alert + reprocess after fix
```

#### ¿Qué es la planificación de capacidad en las plataformas de datos?

Prever el crecimiento del volumen de datos, de los usuarios y de las cargas para que el almacenamiento, el cómputo y la concurrencia sigan siendo suficientes y los presupuestos estén preparados, usando las tendencias del monitoreo y los planes de negocio.

#### ¿Cómo se definen arquitectónicamente las políticas de retención?

Clasificando los datasets según las necesidades legales y de negocio, definiendo la retención por capa (el raw puede guardarse más tiempo para reprocesar, o menos por privacidad), implementándola con reglas de ciclo de vida, borrado de particiones y la retención del formato de tabla, y documentando las excepciones.

#### ¿Qué necesita una plataforma de ML de la arquitectura de datos?

Datos de entrenamiento confiables y versionados, features correctas en el tiempo (point-in-time), reutilización de las features entre entrenamiento y servicio, linaje de los datos a los modelos, seguimiento de experimentos, registro de modelos y monitoreo de la deriva de los datos y de las predicciones.

#### ¿Qué es un feature store?

Un sistema que guarda, documenta y sirve features de ML de forma coherente para el entrenamiento (offline, histórico, correcto en el tiempo) y la inferencia (online, baja latencia), evitando el desfase entre entrenamiento y servicio y la ingeniería de features duplicada.

<!-- challenge -->

Un solo registro malformado en un archivo diario hace fallar toda la carga y bloquea todos los reportes. ¿Cómo lo rediseñas?

<!-- solution -->

Valida por registro: manda las filas inválidas a una tabla de cuarentena o ubicación dead-letter con el error, carga las válidas y alerta si las inválidas superan un umbral. Reprocesa las de cuarentena tras corregir.

<!-- takeaways -->

- Los pasos idempotentes y reiniciables hacen seguros los reintentos.
- Las dead-letter queues aíslan los registros malos.
- IaC y planeación de capacidad evitan caídas autoinfligidas.

<!-- unit: Costo y retención -->

<!-- goals -->

- Identificar qué impulsa los costos y diseñar plataformas eficientes.
- Aplicar FinOps y políticas de retención.

<!-- concept -->

Las plataformas de datos gastan sobre todo en cómputo: clústeres siempre encendidos, recálculos completos y consultas ineficientes. El almacenamiento es barato por byte, pero crece para siempre si la retención no dice lo contrario. Los diseños eficientes procesan de forma incremental, podan con particionamiento, escalan a cero en reposo y guardan los datos solo mientras sirvan o la ley lo exija.
FinOps hace visible el costo para los equipos que lo generan, y la eficiencia se vuelve un hábito compartido en vez de una limpieza anual.

<!-- example -->

| Capa | Retención |
|---|---|
| Archivos de landing | 30 días tras procesarlos |
| Bronze | 7 años (legal), nivel frío después de 1 año |
| Agregados gold | Mientras se usen |
| Sandbox | 30 días, borrado automático |

#### ¿Qué es la corrección en el tiempo (point-in-time)?

Al construir los datos de entrenamiento, las features solo deben usar la información disponible en el momento del evento de cada etiqueta, evitando filtrar datos del futuro; los feature stores unen las features a la fecha de cada evento.

#### ¿Qué es el desfase entre entrenamiento y servicio (training-serving skew)?

Diferencias en cómo se calculan las features para el entrenamiento y para la inferencia (distinto código, fuentes o momento), que degradan el rendimiento del modelo en producción. Las definiciones de features compartidas y los feature stores lo reducen.

#### ¿Qué es una base de datos vectorial y dónde encaja?

Un almacén optimizado para búsquedas por similitud sobre embeddings (pgvector, OpenSearch, Pinecone, Weaviate, Databricks Vector Search), usado para búsqueda semántica, recomendaciones y generación aumentada por recuperación.

#### ¿Cuál es la arquitectura de datos de una aplicación RAG?

Ingerir documentos, dividirlos en fragmentos, calcular embeddings, guardarlos con metadatos en un índice vectorial, recuperar los fragmentos relevantes al consultar (a menudo combinando búsqueda por palabras clave y filtros por permisos) y pasarlos a un LLM, con pipelines que mantengan el índice fresco y gobernado.

<!-- challenge -->

Los costos de nube crecieron 60 % en un año, sobre todo por unos pocos pipelines que reconstruyen tablas completas cada noche. ¿Qué cambias?

<!-- solution -->

Volverlos incrementales (procesar solo particiones nuevas o cambiadas con `MERGE`), agregar poda de particiones, dimensionar bien o autoescalar el cómputo y mostrar a cada equipo su costo por producto de datos.

<!-- takeaways -->

- El cómputo domina el costo; lo incremental gana a reconstruir todo.
- Diseña para la poda y para escalar a cero.
- Las políticas de retención controlan el crecimiento del almacenamiento.

### Arquitectura de datos para IA y ML

<!-- unit: Datos para machine learning -->

<!-- goals -->

- Describir lo que necesitan las plataformas de ML: features, datos point-in-time y MLOps.
- Evitar el training-serving skew y monitorear el drift.

<!-- concept -->

Los modelos valen lo que valen sus datos de entrenamiento, y ML agrega requisitos que BI no tiene. Los sets de entrenamiento deben usar solo información disponible al momento de predecir, o los modelos lucen geniales en pruebas y fallan en producción. Las features deben calcularse igual para entrenar y para servir.
Un feature store atiende ambas cosas, y MLOps envuelve el ciclo de vida: datos y modelos versionados, reentrenamiento automático y monitoreo de cuándo derivan las entradas o las relaciones.

<!-- example -->

```text
label: churned on 2026-06-01
features must come from data known on 2026-05-31:
  orders_last_90d   ✔ computed from orders before 2026-05-31
  support_tickets   ✘ includes the cancellation ticket of 2026-06-02 → leakage
```

#### ¿Cómo cambian las preocupaciones de gobierno con la IA?

Hay que rastrear qué datos entrenaron qué modelos, respetar los permisos en la recuperación (los usuarios no deberían ver mediante un LLM documentos a los que no podrían acceder directamente), manejar los datos personales en los prompts y los datos de entrenamiento, y evaluar las respuestas; los catálogos gobiernan cada vez más los modelos y las features junto a las tablas.

#### ¿Qué es MLOps?

Prácticas y herramientas para desarrollar, desplegar y operar modelos de ML de forma confiable: datos y código versionados, pipelines de entrenamiento reproducibles, registro de modelos, pruebas y despliegue automatizados, monitoreo del rendimiento y la deriva, y reentrenamiento.

#### ¿Qué es la deriva de datos frente a la deriva de concepto?

La deriva de datos es un cambio en la distribución de los datos de entrada (cambian las edades de los clientes); la de concepto es un cambio en la relación entre las entradas y el objetivo (cambia lo que predice el churn). Ambas requieren monitoreo y posiblemente reentrenar.

#### ¿Cómo se deben gestionar los datos no estructurados para la IA?

Guardándolos en almacenamiento de objetos con metadatos en un catálogo (volúmenes), rastreando el linaje de los documentos a los fragmentos y embeddings, aplicando controles de acceso y clasificación, y construyendo pipelines que actualicen los índices cuando los documentos cambian o se borran.

#### ¿Cómo es una arquitectura de datos típica en AWS?

Fuentes ingeridas con DMS, Kinesis/MSK, AppFlow o Glue hacia S3; Glue Data Catalog y Lake Formation para el gobierno; procesamiento con Glue, EMR o Databricks; tablas Iceberg o Delta; Athena y Redshift para SQL; QuickSight para BI; SageMaker para ML; Step Functions, MWAA o EventBridge para orquestar; todo definido con CloudFormation, CDK o Terraform.

#### ¿Cómo es una arquitectura de datos típica en Azure?

Ingesta con Data Factory o pipelines de Fabric y Event Hubs hacia ADLS Gen2/OneLake; procesamiento con Databricks o Spark de Fabric; tablas Delta; warehouses de Synapse/Fabric o Databricks SQL; Power BI; Purview para el gobierno; Entra ID para la identidad.

<!-- challenge -->

Un modelo de churn tiene 97 % de precisión en pruebas y 70 % en producción. ¿Qué sospechas primero?

<!-- solution -->

Fuga de información por datos de entrenamiento no correctos en el tiempo (features que usan información posterior a la fecha de predicción), o training-serving skew en el cálculo de features. Reconstruye el set de entrenamiento con joins point-in-time y compara los valores de las features.

<!-- takeaways -->

- Los datos de entrenamiento deben ser correctos en el tiempo.
- Calcula las features una vez para entrenar y servir.
- Monitorea el drift de datos y de concepto.

<!-- unit: Datos para IA generativa -->

<!-- goals -->

- Ubicar las bases de datos vectoriales y los pipelines RAG en la arquitectura.
- Gobernar los datos no estructurados que usa la IA.

<!-- concept -->

Las aplicaciones de IA generativa recuperan documentos relevantes y se los pasan a un modelo. Eso convierte archivos no estructurados en productos de datos: necesitan ingesta, chunking, embeddings, metadatos y un índice vectorial sincronizado con la fuente.
El gobierno sigue a los datos. Un sistema de recuperación debe respetar los mismos permisos que los documentos, y los equipos deben saber qué datos alimentaron qué modelo o respuesta.

<!-- example -->

```text
docs (S3 / SharePoint) ─► parse + chunk ─► embeddings ─► vector index (with ACL metadata)
user question ─► retrieve top-k allowed chunks ─► LLM ─► answer with sources
lineage: answer → chunks → documents → owners
```

#### ¿Cómo es una arquitectura de datos típica en Google Cloud?

Ingesta con Pub/Sub, Datastream (CDC) y Dataflow hacia Cloud Storage y BigQuery; procesamiento con Dataflow, Dataproc o SQL de BigQuery (a menudo con dbt o Dataform); Dataplex para el gobierno; Looker para BI; Vertex AI para ML.

#### ¿Qué es el multinube y cuándo vale la pena?

Usar varios proveedores de nube. Puede reducir la dependencia, cumplir requisitos de clientes o regulatorios, o usar los mejores servicios de cada uno, pero multiplica las habilidades, las herramientas, la red y los costos de salida. La mayoría de las organizaciones gana más con una nube principal y formatos portables.

#### ¿Qué es una arquitectura híbrida?

Combinar sistemas on-premises con servicios en la nube, común durante las migraciones o para datos regulados; necesita conectividad segura (VPN, Direct Connect, ExpressRoute), identidad y gobierno coherentes, y un movimiento de datos cuidadoso.

#### ¿Qué estrategias de migración existen para las plataformas de datos?

Rehost (lift and shift), replatform (pasar a equivalentes administrados con pocos cambios), refactor (rediseñar para servicios nativos de la nube y ELT), retirar los activos sin uso y retener lo que debe quedarse. Las migraciones de datos suelen combinarlas, avanzando por olas y por dominio con validación en paralelo.

<!-- challenge -->

Un asistente interno responde preguntas de los empleados a partir de documentos de la empresa, y alguien recibe una respuesta que cita archivos de RR. HH. que no puede abrir. ¿Qué salió mal?

<!-- solution -->

La recuperación ignoró los permisos de los documentos. Guarda metadatos de control de acceso con cada chunk y filtra la recuperación por la identidad del usuario, para que el modelo solo vea chunks que el usuario puede leer.

<!-- takeaways -->

- RAG convierte los documentos en productos de datos gobernados.
- Mantén los índices vectoriales sincronizados con las fuentes.
- La recuperación debe respetar los permisos de origen.

### Nube y arquitecturas de referencia

<!-- unit: Arquitecturas de referencia -->

<!-- goals -->

- Esbozar arquitecturas de datos típicas en AWS, Azure y Google Cloud.
- Relacionar servicios equivalentes entre nubes.

<!-- concept -->

Las tres grandes nubes ofrecen las mismas piezas con nombres distintos: servicios de ingesta, almacenamiento de objetos, un catálogo, motores de procesamiento, un warehouse y BI. Conocer el patrón importa más que la lista de productos, porque la forma se repite: aterrizar los datos en almacenamiento de objetos o un warehouse, catalogarlos y gobernarlos, transformarlos y servirlos.
Las diferencias están en la profundidad de la integración y en los valores por defecto, como qué tan unidos están el warehouse y el lago.

<!-- example -->

| Capa | AWS | Azure | Google Cloud |
|---|---|---|---|
| Ingesta | DMS, Kinesis, Glue | Data Factory, Event Hubs | Datastream, Pub/Sub |
| Almacenamiento | S3 | ADLS / OneLake | Cloud Storage |
| Catálogo | Glue + Lake Formation | Purview / Unity | Dataplex |
| Warehouse | Redshift | Fabric / Synapse | BigQuery |

#### ¿Qué es una landing zone en la arquitectura de nube?

Un entorno multicuenta (o multisuscripción) preconfigurado y seguro, con identidad, red, logs, barreras de seguridad y estructura de cuentas, sobre el que se despliegan de forma coherente las plataformas de datos.

#### ¿Cómo se organizan las cuentas o proyectos de una plataforma de datos?

Separando los entornos (dev, staging, prod) y a menudo los dominios en cuentas o proyectos distintos para aislar el impacto de los fallos, ver los costos y aplicar el mínimo privilegio, con los servicios compartidos (catálogo, red, logs) administrados de forma central.

#### Diseña una plataforma de datos para una empresa de comercio electrónico mediana.

Ingiero la base de pedidos con CDC, los eventos web con un stream (Kafka o Kinesis) y las herramientas SaaS (CRM, marketing) con conectores hacia almacenamiento de objetos; organizo capas medallion con tablas Iceberg o Delta en un catálogo; transformo con dbt o Spark hacia dimensiones conformadas y hechos; sirvo BI desde un warehouse o un motor SQL de lakehouse con una capa semántica; añado reverse ETL para los segmentos de marketing; orquesto con Airflow o jobs nativos; aplico gobierno, pruebas de calidad, observabilidad y etiquetas de costo; y lo defino todo como código con CI/CD.

<!-- challenge -->

Un entrevistador te pide diseñar en una nube que nunca has usado. ¿Cómo respondes de forma convincente?

<!-- solution -->

Describe primero las capas y los requisitos (ingesta, almacenamiento, catálogo, procesamiento, consumo, gobierno) y luego relaciona cada una con el servicio equivalente de esa nube, diciendo dónde verificarías detalles. El patrón muestra criterio más que los nombres de productos.

<!-- takeaways -->

- Todas las nubes ofrecen las mismas capas.
- Aprende el patrón y luego relaciona los servicios.
- La profundidad de integración varía entre nubes.

<!-- unit: Multinube, híbrido y migración -->

<!-- goals -->

- Decidir cuándo valen la pena las arquitecturas multinube o híbridas.
- Planear migraciones y organizar las cuentas de nube de una plataforma de datos.

<!-- concept -->

La multinube suena a libertad, pero duplica habilidades, herramientas y trabajo de integración; paga por razones específicas como regulación, adquisiciones o exigencias de clientes. Los montajes híbridos son comunes durante migraciones y para sistemas que deben quedarse on premises.
Las migraciones siguen el espectro conocido de rehosting a reconstrucción. Por debajo, una landing zone con cuentas separadas por ambiente y dominio da límites de seguridad y costo desde el primer día.

<!-- example -->

```text
organization
 ├─ security (logs, audit)
 ├─ shared-network
 ├─ data-dev / data-staging / data-prod
 └─ domain-payments-prod, domain-marketing-prod (mesh-style)
```

#### Una empresa tiene diez departamentos que construyen cada uno sus reportes con cifras contradictorias. ¿Qué propones?

Identificar los procesos de negocio y las métricas centrales, crear dimensiones conformadas y hechos certificados con equipos responsables, implementar una capa semántica para las definiciones de las métricas, establecer la propiedad y la custodia de los datos, retirar poco a poco la lógica duplicada y comunicar un catálogo de datasets certificados.

#### Debes añadir scoring de fraude en tiempo real a una plataforma orientada al batch. ¿Cómo?

Transmito las transacciones desde el origen (CDC o eventos) hacia un broker, calculo las features con un procesador de streaming usando un feature store online (definiciones compartidas con el entrenamiento batch), llamo al modelo para puntuar en milisegundos, escribo las decisiones de vuelta como eventos y llevo todo al lakehouse para el análisis y el reentrenamiento.

#### Los equipos de microservicios se quejan de que el equipo de datos se rompe cada vez que cambian sus bases. ¿Qué cambias?

Dejar de leer directamente las tablas internas: acordar contratos de datos, hacer que los servicios publiquen eventos de integración (mediante un outbox) o vistas de CDC curadas, validar los contratos en el CI de los servicios, versionar los cambios que rompen y dar a los dominios la propiedad de sus productos de datos publicados.

#### Tu data lake se convirtió en un pantano. ¿Cómo lo recuperas?

Inventario los datasets con su uso y sus responsables, defino zonas y estándares de nombres, registro los datos valiosos en un catálogo con descripciones y etiquetas, añado controles de calidad, convierto los datasets clave a formatos de tabla, archivo o borro los datos sin uso con políticas de ciclo de vida y hago obligatoria la propiedad de los datasets nuevos.

#### ¿Cómo le explicas la arquitectura de datos a una persona no técnica?

Es el plan urbanístico de los datos de la empresa: de dónde vienen, dónde se guardan, cómo circulan y se limpian, quién es responsable de ellos y las reglas que los mantienen seguros y confiables, para que los equipos construyan encima sin caos.

<!-- challenge -->

La dirección quiere correr cada carga en dos nubes "para evitar el lock-in". ¿Qué aconsejas?

<!-- solution -->

Explica el costo: habilidades, herramientas e integración duplicadas, y servicios al mínimo común denominador. Limita el lock-in con formatos abiertos y herramientas portables, y usa una segunda nube solo donde un requisito concreto lo justifique.

<!-- takeaways -->

- La multinube tiene costos reales; úsala por razones concretas.
- Lo híbrido es común durante las migraciones.
- Una landing zone fija temprano los límites de las cuentas.

<!-- stage: Juntarlo todo -->

### Escenarios

<!-- unit: Diseñar una plataforma desde cero -->

<!-- goals -->

- Diseñar una plataforma de datos de punta a punta para una empresa dada.
- Ajustar el diseño al tamaño y la madurez de la empresa.

<!-- concept -->

Las preguntas de diseño evalúan criterio, no listas de herramientas. Una respuesta sólida parte de las preguntas de negocio y las restricciones y recorre las capas: cómo se ingesta cada fuente, dónde se guardan los datos y en qué formatos, cómo se modelan, cómo se sirven y cómo se gobiernan, aseguran y monitorean. Luego ajusta el diseño a la empresa: una startup necesita simplicidad administrada, una mediana necesita estructura, y ambas un camino para crecer.

<!-- example -->

| Capa | Startup | E-commerce mediano |
|---|---|---|
| Ingesta | Conectores administrados | CDC, stream de eventos, conectores |
| Almacenamiento | Warehouse en la nube | Lakehouse o warehouse + lago |
| Modelado | dbt, unos pocos marts | Medallion + marts dimensionales |
| Gobierno | Roles básicos, docs | Catálogo, dueños, clasificación |

#### Una startup te pide diseñar su primera plataforma de datos. ¿Qué recomiendas?

Mantenerla simple y administrada: un servicio de warehouse o lakehouse en la nube, conectores administrados para las fuentes SaaS, CDC o réplicas para la base del producto, dbt para las transformaciones con pruebas, un solo orquestador, una herramienta de BI con capa semántica, un gobierno básico y alertas de costo, todo como código. Añadir streaming, mesh o componentes propios solo cuando aparezca la necesidad.

#### Tu empresa compró otra con una nube y una plataforma distintas. ¿Cómo integras los datos?

Empiezo por las preguntas que necesita responder la dirección, mapeo las entidades y métricas clave, replico los datos necesarios en la plataforma principal con CDC o exportaciones (o los comparto con formatos abiertos), construyo dimensiones conformadas con emparejamiento de datos maestros, y planifico a más largo plazo la consolidación de las plataformas según costo y capacidades.

<!-- challenge -->

La startup de tu diseño se duplica cada año. ¿Qué cambiarías en el tercer año y qué conservarías?

<!-- solution -->

Conserva el warehouse, dbt y los conectores administrados. Agrega un catálogo con dueños, contratos de datos con los equipos de producto, CDC para la base principal, monitoreo de costos y quizá un lago para datos crudos y de ML a medida que crecen los volúmenes.

<!-- takeaways -->

- Parte de preguntas y restricciones, luego recorre las capas.
- Ajusta el diseño al tamaño y la madurez de la empresa.
- Deja un camino para crecer sin reconstruir.

<!-- unit: Integrar tras una adquisición -->

<!-- goals -->

- Planear la integración de datos entre las plataformas de dos empresas.
- Priorizar las preguntas de negocio sobre la consolidación de plataformas.

<!-- concept -->

Tras una adquisición, la dirección quiere cifras combinadas mucho antes de que las plataformas se puedan fusionar. El camino práctico es partir de las preguntas que hay que responder, relacionar las entidades y métricas clave entre las empresas y replicar los datos necesarios a una sola plataforma. La consolidación de plataformas viene después, cuando las definiciones estén alineadas y el negocio vea resultados.

<!-- example -->

```text
week 1–4:  agree on 10 key metrics and their definitions; map customer, product, revenue
week 4–8:  replicate needed tables from company B into A's platform; build combined marts
month 3+:  plan migration of B's pipelines; retire duplicate tools
```

#### La dirección quiere "todo en tiempo real". ¿Cómo respondes?

Pregunto qué decisiones cambian con datos más frescos y qué latencia necesita cada una, estimo los costos y la complejidad de cada nivel (segundos, minutos, horas), entrego tiempo real donde el valor de negocio lo justifica y mantengo el resto en batch o micro-lotes, que son más baratos.

<!-- challenge -->

Las dos empresas definen "cliente" distinto: una cuenta cuentas, la otra personas. ¿Cómo produces un conteo combinado de clientes?

<!-- solution -->

Acuerda una definición con los dueños de negocio (o reporta ambas claramente etiquetadas), relaciona los registros de cada empresa con ella mediante una tabla de mapeo de llaves y documenta la regla en el glosario antes de publicar cifras combinadas.

<!-- takeaways -->

- Parte de las preguntas que la dirección necesita responder.
- Relaciona entidades y métricas antes de mover plataformas.
- Consolida las plataformas cuando las definiciones estén alineadas.
