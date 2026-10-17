## Guía de estudio de Arquitectura de datos

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de arquitectura de datos: unas 200 preguntas](../../images/data_architecture_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre arquitectura de datos: principios, elección de almacenamiento y bases de datos, compromisos de los sistemas distribuidos, enfoques de modelado (Inmon, Kimball, Data Vault), lakes, lakehouses y el patrón medallion, arquitecturas batch y streaming (Lambda, Kappa), microservicios y datos orientados a eventos, data mesh y data fabric, gobierno, seguridad, confiabilidad, costos y arquitectura para IA. Complementa la guía de data warehousing, que profundiza en el modelado dimensional. Abre una pregunta para ver su respuesta, o usa el filtro para buscar en toda la guía.

<!-- QA -->

### Principios

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

#### ¿Qué son los requisitos funcionales y no funcionales en arquitectura de datos?

Funcionales: qué datos, transformaciones, métricas y salidas se necesitan. No funcionales: latencia, frescura, volumen, escalabilidad, disponibilidad, durabilidad, seguridad, cumplimiento, costo y mantenibilidad, que a menudo determinan la elección de tecnologías.

#### ¿Qué es un registro de decisión de arquitectura (ADR)?

Un documento corto que recoge una decisión importante: contexto, opciones consideradas, decisión, consecuencias y estado. Los ADR hacen visible el razonamiento y evitan que los equipos vuelvan a discutir lo ya decidido; se guardan junto al código.

#### ¿Qué es la deuda técnica en las plataformas de datos?

Atajos que encarecen los cambios futuros: pipelines sin documentar, lógica duplicada, configuración escrita en el código, pruebas faltantes, tablas sin responsable, arreglos rápidos en producción. Se acumula en silencio y aparece como incidentes, entregas lentas y desconfianza en las cifras.

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

#### ¿Qué es el costo total de propiedad (TCO)?

El costo completo de una solución en el tiempo: licencias o consumo en la nube, infraestructura, personas para construirla y operarla, formación, migración, soporte y el costo de las caídas, no solo el precio por unidad de cómputo.

#### ¿Qué es la "arquitectura evolutiva"?

Diseñar los sistemas para que cambien de forma incremental con salvaguardas (fitness functions como pruebas sobre latencia, costo o acoplamiento), prefiriendo decisiones reversibles y pasos pequeños frente a grandes diseños iniciales.

#### ¿Por qué los datos en bruto deben ser inmutables?

Los datos en bruto inmutables permiten reprocesar el historial cuando cambian la lógica o se corrigen errores, auditar lo que enviaron las fuentes y reconstruir las capas posteriores; las modificaciones ocurren en las capas siguientes, lo que mantiene el sistema recuperable.

#### ¿Qué es el principio de "responsabilidad única" aplicado a los pipelines de datos?

Cada pipeline o modelo debe tener un propósito claro (ingerir una fuente, homogeneizar una entidad, construir una métrica), lo que facilita probarlo, asignarle un responsable, reutilizarlo y cambiarlo sin efectos secundarios.

### Almacenamiento y bases de datos

#### ¿Qué tipos de bases de datos existen?

Relacionales (PostgreSQL, MySQL, Oracle), clave-valor (DynamoDB, Redis), documentales (MongoDB, Couchbase), de columnas anchas (Cassandra, HBase, Bigtable), de grafos (Neo4j, Neptune), de series de tiempo (TimescaleDB, InfluxDB), de búsqueda (Elasticsearch, OpenSearch), vectoriales (pgvector, Pinecone, vectores de OpenSearch) y almacenes analíticos columnares (warehouses, ClickHouse, Druid).

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

#### ¿Qué diferencias hay entre el almacenamiento en bloques, de archivos y de objetos?

El de bloques da volúmenes en bruto para una máquina (EBS), ideal para bases de datos; el de archivos da sistemas de archivos jerárquicos compartidos (NFS, EFS); el de objetos da objetos planos accesibles por HTTP a enorme escala (S3), ideal para data lakes.

#### ¿Qué son los niveles (tiers) de almacenamiento?

Clases de almacenamiento con distinto costo y velocidad de acceso (caliente, tibio, frío, archivo; S3 Standard, Infrequent Access, Glacier). Las políticas de ciclo de vida mueven los datos que envejecen a niveles más baratos.

#### ¿Qué son los formatos de archivo por filas y columnares?

Los formatos por filas (CSV, JSON, Avro) guardan los registros juntos, buenos para escribir y leer registros completos; los columnares (Parquet, ORC) guardan las columnas juntas con estadísticas, buenos para analítica que lee pocas columnas de muchas filas.

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

#### ¿Cuándo usarías un motor de búsqueda como OpenSearch?

Para búsqueda de texto completo con relevancia, coincidencias aproximadas, facetas y analítica de logs, normalmente como índice secundario alimentado desde el sistema de registro y no como base de datos principal.

### Fundamentos de sistemas distribuidos

#### ¿Qué es el teorema CAP?

En un sistema distribuido que sufre una partición de red, hay que elegir entre consistencia (toda lectura ve la última escritura) y disponibilidad (toda solicitud recibe respuesta). Sin particiones ambas son posibles; CAP trata del comportamiento durante los fallos.

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

#### ¿Qué es un hotspot y cómo se evita?

Una partición o nodo que recibe una carga desproporcionada por una clave sesgada (un usuario muy popular, una marca de tiempo que siempre crece). Se evita con mejores claves, salting, hashing o dividiendo las claves calientes.

#### ¿Qué es el protocolo de commit en dos fases y por qué se evita?

Un protocolo en el que un coordinador pide a todos los participantes que se preparen y luego que confirmen, garantizando la atomicidad entre sistemas. Se evita a escala porque se bloquea ante fallos, añade latencia y acopla la disponibilidad de todos los participantes; se prefieren las sagas y el outbox.

#### ¿Qué es un quórum?

El número mínimo de nodos que deben confirmar una lectura o escritura para que tenga éxito (por ejemplo una mayoría). Si el quórum de lectura más el de escritura supera el número de réplicas, las lecturas ven la última escritura.

#### ¿Qué es el desfase de relojes y por qué importa?

Los relojes de distintas máquinas no coinciden, así que no se puede confiar en las marcas de tiempo de distintos sistemas para un orden exacto. Para ordenar los cambios usa relojes lógicos, números de secuencia o posiciones del log del sistema de origen.

#### ¿Qué diferencia hay entre latencia y rendimiento (throughput)?

La latencia es cuánto tarda una operación; el rendimiento es cuántas operaciones terminan por unidad de tiempo. Los sistemas batch optimizan el rendimiento; los interactivos y de streaming se preocupan por la latencia; mejorar uno puede empeorar el otro.

### Enfoques de modelado

#### ¿Qué enfoques de modelado se usan en arquitectura de datos?

Modelos normalizados (3FN) para la integración y el OLTP, dimensionales (Kimball) para la analítica, Data Vault para capas de integración auditables, tablas anchas desnormalizadas (one big table) para consumos concretos, y modelos anchor o ensemble en casos de nicho.

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

#### ¿Cómo se modelan los datos semiestructurados en una plataforma analítica?

Aterrizándolos en bruto (JSON, `VARIANT`, columnas struct), extrayendo en las capas siguientes los campos estables y muy usados a columnas tipadas, dejando el resto anidado para conservar la flexibilidad y documentando los esquemas con contratos o un registro.

#### ¿Qué es un modelo "conformado" entre dominios?

Definiciones compartidas de claves y entidades (cliente, producto, fecha) que usan los productos de datos de todos los dominios, para que el análisis entre dominios funcione; en un mesh suelen publicarse como productos de datos de referencia.

#### ¿Cómo se decide el grano de un producto de datos?

A partir de las preguntas de los consumidores y de los eventos atómicos del origen: elige el grano más atómico que sea estable y útil, documéntalo de forma explícita y ofrece los agregados como productos aparte.

### Data lakes, lakehouses y medallion

#### ¿Qué es un data lake?

Un repositorio centralizado en almacenamiento de objetos que guarda datos en bruto y procesados de cualquier formato y a cualquier escala, con almacenamiento barato y esquema al leer, usado para analítica, ciencia de datos y como fuente de los warehouses.

#### ¿Qué es un data swamp?

Un data lake que se volvió inutilizable: datos sin documentar, sin gobierno, duplicados, de calidad y propiedad desconocidas. Los catálogos, los responsables, los controles de calidad, las zonas y las políticas de ciclo de vida lo evitan.

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

#### ¿Para qué sirve arquitectónicamente el "viaje en el tiempo"?

Para reproducir reportes a una fecha, auditar, depurar qué cambió, recuperarse de escrituras malas y comparar versiones, siempre que las políticas de retención conserven suficiente historial.

### Arquitecturas batch y streaming

#### ¿Qué diferencia hay entre el procesamiento batch y el de streaming?

El batch procesa conjuntos de datos acotados a intervalos (cada hora, cada día) con mucho rendimiento y lógica más simple; el streaming maneja flujos de eventos sin fin de forma continua con baja latencia, y requiere gestión de estado, manejo del tiempo del evento y tolerancia a fallos.

#### ¿Qué es la arquitectura Lambda?

La arquitectura de Nathan Marz con una capa batch (recalcula vistas exactas a partir de todo el historial), una capa de velocidad (procesa los datos recientes en tiempo real) y una capa de servicio que combina ambas. Da exactitud y baja latencia, pero duplica la lógica en dos caminos de código.

#### ¿Qué es la arquitectura Kappa?

La simplificación de Jay Kreps: un único camino de procesamiento en streaming donde todo es un flujo; el reprocesamiento se hace reproduciendo el log (Kafka) con una nueva versión del job. Elimina la lógica duplicada, pero necesita un log durable y reproducible y un streaming robusto.

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

### Microservicios y datos orientados a eventos

#### ¿Cómo cambian los microservicios la arquitectura de datos?

Cada servicio es dueño de sus datos y de su base (una base por servicio) y se comunica mediante APIs y eventos en lugar de tablas compartidas. Esto mejora la autonomía y el escalado, pero dispersa los datos y exige patrones de integración para la analítica y las consultas entre servicios.

#### ¿Qué es el patrón de "una base de datos por servicio"?

Cada microservicio tiene una base privada a la que solo él accede; los demás servicios usan su API o sus eventos. Evita el acoplamiento fuerte a través de esquemas compartidos.

#### ¿Por qué una base compartida es un antipatrón en microservicios?

Los servicios quedan acoplados por el esquema: el cambio de un equipo rompe a otros, los despliegues deben coordinarse y la propiedad es confusa, con lo que se pierde el principal beneficio de los microservicios.

#### ¿Cómo se hace analítica entre microservicios?

Capturando los datos de cada servicio (CDC de su base o sus eventos de dominio) en un lake o un warehouse, modelándolos de forma central o por dominio, y sirviendo la analítica desde allí, en lugar de consultar directamente las bases de los servicios.

#### ¿Qué es la arquitectura orientada a eventos?

Sistemas que se comunican produciendo eventos y reaccionando a ellos (hechos sobre algo que ocurrió: `OrderPlaced`, `PaymentFailed`) a través de un broker, en lugar de llamadas síncronas, lo que da bajo acoplamiento, escalabilidad y registros de auditoría naturales.

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

#### ¿Qué es la coreografía frente a la orquestación?

En la coreografía, los servicios reaccionan a los eventos de los demás sin un coordinador central (bajo acoplamiento, más difícil ver el flujo completo); en la orquestación, un coordinador les dice a los servicios qué hacer (flujo claro, dependencia central). Los pipelines de datos suelen usar orquestación (Airflow); las sagas de microservicios usan cualquiera de las dos.

### Data mesh y data fabric

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

#### ¿Qué son los "metadatos activos"?

Metadatos que disparan automatizaciones en lugar de solo documentar: etiquetas que aplican enmascaramiento, linaje que lanza alertas ante cambios en el origen, estadísticas de uso que sugieren retirar datasets, métricas de calidad que bloquean la publicación.

### Integración e ingesta

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

#### ¿Qué es un contrato de aterrizaje con proveedores de datos externos?

Un acuerdo sobre los formatos de archivo, los nombres, el calendario de entrega, las señales de completitud (manifiestos o archivos `_SUCCESS`), la codificación, el aviso de cambios de esquema y el manejo de errores, que evita la mayoría de los incidentes de ingesta de archivos.

### Gobierno, metadatos y calidad

#### ¿Qué es el gobierno de datos?

El marco de roles, políticas, estándares y procesos que garantiza que los datos sean exactos, seguros, conformes, comprensibles y se usen de forma apropiada, incluidos la propiedad, la custodia (stewardship), la clasificación, el acceso, la calidad y el ciclo de vida.

#### ¿Qué son los data owners y los data stewards?

Los data owners responden por un dominio de datos (decisiones sobre acceso, definiciones, metas de calidad); los data stewards manejan en el día a día las definiciones, los problemas de calidad y los metadatos, junto con los ingenieros que implementan los controles.

#### ¿Qué es la gestión de metadatos?

Recoger y administrar metadatos técnicos, de negocio y operativos (esquemas, definiciones, linaje, calidad, uso) para facilitar el descubrimiento, el análisis de impacto, el gobierno y la automatización; los "metadatos activos" los usan para disparar acciones.

#### ¿Qué es el linaje de datos y cómo se captura?

El flujo de los datos desde las fuentes, a través de las transformaciones, hasta los consumidores. Se captura analizando el SQL y los jobs (dbt, Unity Catalog, eventos OpenLineage de Airflow y Spark) y se muestra a nivel de tabla y de columna para el análisis de impacto y las auditorías.

#### ¿Qué es OpenLineage?

Un estándar abierto para los eventos de linaje que emiten los orquestadores y motores (Airflow, Spark, dbt, Flink), que describen los jobs, las ejecuciones y los datasets de entrada y salida, y que recogen backends como Marquez o los catálogos.

#### ¿Qué es la clasificación de datos?

Etiquetar los datos por sensibilidad (público, interno, confidencial, restringido) y tipo (datos personales, financieros, de salud), a menudo de forma automática con escáneres, para guiar las políticas de acceso, el enmascaramiento, la retención y el cumplimiento.

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

#### ¿Cómo se evitan los datasets duplicados?

Haciendo descubribles los datasets existentes (catálogo, búsqueda), certificando los autorizados, exigiendo un responsable y una revisión para los nuevos datasets publicados, monitoreando el uso y retirando las copias.

### Seguridad y cumplimiento

#### ¿Cuáles son las capas de la seguridad de datos?

La gestión de identidades y accesos (autenticación, autorización de mínimo privilegio), el aislamiento de red, el cifrado en reposo y en tránsito, la gestión de claves, el enmascaramiento y la tokenización, la seguridad a nivel de fila y columna, la auditoría y el monitoreo, y las prácticas de desarrollo seguro.

#### ¿Qué diferencia hay entre RBAC y ABAC?

El control de acceso basado en roles concede permisos a roles asignados a usuarios; el basado en atributos evalúa en las políticas atributos de los usuarios, los recursos y el contexto (departamento, clasificación de los datos, ubicación), lo que escala mejor para reglas detalladas (por ejemplo, políticas por etiquetas).

#### ¿Qué es la seudonimización frente a la anonimización?

La seudonimización reemplaza los identificadores por tokens o hashes que se pueden volver a vincular con información adicional (siguen siendo datos personales según el RGPD); la anonimización impide de forma irreversible la identificación (dejan de ser datos personales), algo difícil de lograr en la práctica.

#### ¿Qué es la tokenización?

Reemplazar valores sensibles (números de tarjeta, documentos de identidad) por tokens no sensibles, guardando la correspondencia en una bóveda segura, para que la mayoría de los sistemas nunca maneje los valores reales.

#### ¿Cómo afectan el RGPD y las leyes de protección de datos a la arquitectura de datos?

Exigen una base legal y limitación de la finalidad, minimización de los datos, límites de retención, seguridad, registros del tratamiento y atender los derechos de los titulares (acceso, rectificación, supresión), lo que implica saber dónde están los datos personales (linaje, catálogo) y poder borrarlos de todas las capas. En Colombia, la Ley 1581 de 2012 de habeas data plantea obligaciones similares.

#### ¿Cómo se implementa el derecho de supresión en un lakehouse?

Rastreando dónde están los datos de cada persona, usando formatos de tabla que admiten borrados (Delta, Iceberg), borrando en todas las capas, haciendo vacuum de los archivos viejos tras la retención, evitando copiar ampliamente los identificadores en bruto (seudonimizar pronto) y documentando el proceso y sus plazos.

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

### Confiabilidad, operación y costos

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

#### ¿Cuáles son los mayores impulsores de costo en las plataformas de datos?

El cómputo de las transformaciones y las consultas (sobre todo clusters siempre encendidos y recálculos completos), las consultas ineficientes sobre muchos datos, la duplicación de datos entre capas y herramientas, la salida de datos y la transferencia entre regiones, y los datos sin uso guardados para siempre.

#### ¿Cómo se hace una plataforma eficiente en costos desde el diseño?

Con procesamiento incremental, particionado y clustering para el pruning, cómputo serverless o con autoescalado y auto-suspend, almacenamiento por niveles y retención, evitando copias innecesarias, eligiendo la latencia adecuada a la necesidad de negocio y haciendo visibles los costos por equipo.

#### ¿Qué papel cumple la infraestructura como código en la arquitectura de datos?

Definir las plataformas (almacenamiento, cómputo, permisos, catálogos, jobs) de forma declarativa en código (Terraform, CloudFormation, Bicep, bundles) para que los entornos sean reproducibles, revisados y auditables, y se pueda detectar la deriva.

#### ¿Qué es un incidente de datos y cómo se gestiona?

Cualquier evento en el que los datos están mal, llegan tarde o no están disponibles para los consumidores. Se gestiona como un incidente de software: detectar, evaluar el impacto, comunicar a los consumidores, mitigar (pausar la publicación, revertir), corregir la causa raíz y escribir un postmortem sin culpables con acciones.

#### ¿Qué es la planificación de capacidad en las plataformas de datos?

Prever el crecimiento del volumen de datos, de los usuarios y de las cargas para que el almacenamiento, el cómputo y la concurrencia sigan siendo suficientes y los presupuestos estén preparados, usando las tendencias del monitoreo y los planes de negocio.

#### ¿Cómo se definen arquitectónicamente las políticas de retención?

Clasificando los datasets según las necesidades legales y de negocio, definiendo la retención por capa (el raw puede guardarse más tiempo para reprocesar, o menos por privacidad), implementándola con reglas de ciclo de vida, borrado de particiones y la retención del formato de tabla, y documentando las excepciones.

### Arquitectura de datos para IA y ML

#### ¿Qué necesita una plataforma de ML de la arquitectura de datos?

Datos de entrenamiento confiables y versionados, features correctas en el tiempo (point-in-time), reutilización de las features entre entrenamiento y servicio, linaje de los datos a los modelos, seguimiento de experimentos, registro de modelos y monitoreo de la deriva de los datos y de las predicciones.

#### ¿Qué es un feature store?

Un sistema que guarda, documenta y sirve features de ML de forma coherente para el entrenamiento (offline, histórico, correcto en el tiempo) y la inferencia (online, baja latencia), evitando el desfase entre entrenamiento y servicio y la ingeniería de features duplicada.

#### ¿Qué es la corrección en el tiempo (point-in-time)?

Al construir los datos de entrenamiento, las features solo deben usar la información disponible en el momento del evento de cada etiqueta, evitando filtrar datos del futuro; los feature stores unen las features a la fecha de cada evento.

#### ¿Qué es el desfase entre entrenamiento y servicio (training-serving skew)?

Diferencias en cómo se calculan las features para el entrenamiento y para la inferencia (distinto código, fuentes o momento), que degradan el rendimiento del modelo en producción. Las definiciones de features compartidas y los feature stores lo reducen.

#### ¿Qué es una base de datos vectorial y dónde encaja?

Un almacén optimizado para búsquedas por similitud sobre embeddings (pgvector, OpenSearch, Pinecone, Weaviate, Databricks Vector Search), usado para búsqueda semántica, recomendaciones y generación aumentada por recuperación.

#### ¿Cuál es la arquitectura de datos de una aplicación RAG?

Ingerir documentos, dividirlos en fragmentos, calcular embeddings, guardarlos con metadatos en un índice vectorial, recuperar los fragmentos relevantes al consultar (a menudo combinando búsqueda por palabras clave y filtros por permisos) y pasarlos a un LLM, con pipelines que mantengan el índice fresco y gobernado.

#### ¿Cómo cambian las preocupaciones de gobierno con la IA?

Hay que rastrear qué datos entrenaron qué modelos, respetar los permisos en la recuperación (los usuarios no deberían ver mediante un LLM documentos a los que no podrían acceder directamente), manejar los datos personales en los prompts y los datos de entrenamiento, y evaluar las respuestas; los catálogos gobiernan cada vez más los modelos y las features junto a las tablas.

#### ¿Qué es MLOps?

Prácticas y herramientas para desarrollar, desplegar y operar modelos de ML de forma confiable: datos y código versionados, pipelines de entrenamiento reproducibles, registro de modelos, pruebas y despliegue automatizados, monitoreo del rendimiento y la deriva, y reentrenamiento.

#### ¿Qué es la deriva de datos frente a la deriva de concepto?

La deriva de datos es un cambio en la distribución de los datos de entrada (cambian las edades de los clientes); la de concepto es un cambio en la relación entre las entradas y el objetivo (cambia lo que predice el churn). Ambas requieren monitoreo y posiblemente reentrenar.

#### ¿Cómo se deben gestionar los datos no estructurados para la IA?

Guardándolos en almacenamiento de objetos con metadatos en un catálogo (volúmenes), rastreando el linaje de los documentos a los fragmentos y embeddings, aplicando controles de acceso y clasificación, y construyendo pipelines que actualicen los índices cuando los documentos cambian o se borran.

### Nube y arquitecturas de referencia

#### ¿Cómo es una arquitectura de datos típica en AWS?

Fuentes ingeridas con DMS, Kinesis/MSK, AppFlow o Glue hacia S3; Glue Data Catalog y Lake Formation para el gobierno; procesamiento con Glue, EMR o Databricks; tablas Iceberg o Delta; Athena y Redshift para SQL; QuickSight para BI; SageMaker para ML; Step Functions, MWAA o EventBridge para orquestar; todo definido con CloudFormation, CDK o Terraform.

#### ¿Cómo es una arquitectura de datos típica en Azure?

Ingesta con Data Factory o pipelines de Fabric y Event Hubs hacia ADLS Gen2/OneLake; procesamiento con Databricks o Spark de Fabric; tablas Delta; warehouses de Synapse/Fabric o Databricks SQL; Power BI; Purview para el gobierno; Entra ID para la identidad.

#### ¿Cómo es una arquitectura de datos típica en Google Cloud?

Ingesta con Pub/Sub, Datastream (CDC) y Dataflow hacia Cloud Storage y BigQuery; procesamiento con Dataflow, Dataproc o SQL de BigQuery (a menudo con dbt o Dataform); Dataplex para el gobierno; Looker para BI; Vertex AI para ML.

#### ¿Qué es el multinube y cuándo vale la pena?

Usar varios proveedores de nube. Puede reducir la dependencia, cumplir requisitos de clientes o regulatorios, o usar los mejores servicios de cada uno, pero multiplica las habilidades, las herramientas, la red y los costos de salida. La mayoría de las organizaciones gana más con una nube principal y formatos portables.

#### ¿Qué es una arquitectura híbrida?

Combinar sistemas on-premises con servicios en la nube, común durante las migraciones o para datos regulados; necesita conectividad segura (VPN, Direct Connect, ExpressRoute), identidad y gobierno coherentes, y un movimiento de datos cuidadoso.

#### ¿Qué estrategias de migración existen para las plataformas de datos?

Rehost (lift and shift), replatform (pasar a equivalentes administrados con pocos cambios), refactor (rediseñar para servicios nativos de la nube y ELT), retirar los activos sin uso y retener lo que debe quedarse. Las migraciones de datos suelen combinarlas, avanzando por olas y por dominio con validación en paralelo.

#### ¿Qué es una landing zone en la arquitectura de nube?

Un entorno multicuenta (o multisuscripción) preconfigurado y seguro, con identidad, red, logs, barreras de seguridad y estructura de cuentas, sobre el que se despliegan de forma coherente las plataformas de datos.

#### ¿Cómo se organizan las cuentas o proyectos de una plataforma de datos?

Separando los entornos (dev, staging, prod) y a menudo los dominios en cuentas o proyectos distintos para aislar el impacto de los fallos, ver los costos y aplicar el mínimo privilegio, con los servicios compartidos (catálogo, red, logs) administrados de forma central.

### Escenarios

#### Diseña una plataforma de datos para una empresa de comercio electrónico mediana.

Ingiero la base de pedidos con CDC, los eventos web con un stream (Kafka o Kinesis) y las herramientas SaaS (CRM, marketing) con conectores hacia almacenamiento de objetos; organizo capas medallion con tablas Iceberg o Delta en un catálogo; transformo con dbt o Spark hacia dimensiones conformadas y hechos; sirvo BI desde un warehouse o un motor SQL de lakehouse con una capa semántica; añado reverse ETL para los segmentos de marketing; orquesto con Airflow o jobs nativos; aplico gobierno, pruebas de calidad, observabilidad y etiquetas de costo; y lo defino todo como código con CI/CD.

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

#### Una startup te pide diseñar su primera plataforma de datos. ¿Qué recomiendas?

Mantenerla simple y administrada: un servicio de warehouse o lakehouse en la nube, conectores administrados para las fuentes SaaS, CDC o réplicas para la base del producto, dbt para las transformaciones con pruebas, un solo orquestador, una herramienta de BI con capa semántica, un gobierno básico y alertas de costo, todo como código. Añadir streaming, mesh o componentes propios solo cuando aparezca la necesidad.

#### Tu empresa compró otra con una nube y una plataforma distintas. ¿Cómo integras los datos?

Empiezo por las preguntas que necesita responder la dirección, mapeo las entidades y métricas clave, replico los datos necesarios en la plataforma principal con CDC o exportaciones (o los comparto con formatos abiertos), construyo dimensiones conformadas con emparejamiento de datos maestros, y planifico a más largo plazo la consolidación de las plataformas según costo y capacidades.

#### La dirección quiere "todo en tiempo real". ¿Cómo respondes?

Pregunto qué decisiones cambian con datos más frescos y qué latencia necesita cada una, estimo los costos y la complejidad de cada nivel (segundos, minutos, horas), entrego tiempo real donde el valor de negocio lo justifica y mantengo el resto en batch o micro-lotes, que son más baratos.
