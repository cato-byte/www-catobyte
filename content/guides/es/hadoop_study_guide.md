## Guía de estudio de Hadoop

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de Hadoop: unas 200 preguntas](../../images/hadoop_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre Apache Hadoop y su ecosistema: HDFS, YARN, MapReduce, formatos de archivo, Hive, HBase, ZooKeeper, herramientas de ingesta, seguridad, operación y el paso al almacenamiento de objetos en la nube. Hadoop ya no es la opción por defecto para las plataformas nuevas, pero muchas empresas todavía lo usan, y sus ideas (localidad de datos, almacenamiento distribuido, gestión de recursos) son la base de Spark y del lakehouse.

La guía sigue una ruta de aprendizaje en seis etapas. Cada sección se divide en unidades cortas: objetivos de aprendizaje, una explicación del concepto y un ejemplo resuelto, luego preguntas (primero de memoria, después de aplicación), un reto práctico e ideas clave. Para **aprender**, lee cada unidad de principio a fin. Para **repasar**, cambia al modo repaso o usa "Ir a las preguntas", marca las respuestas que quieras volver a ver y prueba un repaso mixto entre secciones.

<!-- QA -->
<!-- stage: Fundamentos -->

### Fundamentos

<!-- unit: Por qué existe Hadoop -->

<!-- goals -->

- Explicar el problema que resolvió Hadoop y de dónde salió.
- Describir sus principios de diseño: localidad de datos, hardware común, throughput.

<!-- concept -->

A inicios de los 2000, las empresas web tenían más datos de los que cualquier máquina podía guardar o procesar, y los grandes servidores especializados eran demasiado caros. La respuesta de Google, descrita en dos papers, fue repartir datos y cómputo entre muchas máquinas baratas y dejar que el software manejara las fallas que inevitablemente ocurrirían.
Hadoop es la versión open source de esa idea. Su truco central es llevar el cómputo adonde ya están los datos, porque enviar código es barato y enviar terabytes no. Optimiza para terminar enormes jobs batch, no para responder consultas rápidas.

<!-- example -->

```text
Classic approach:  data ──network──► one big server ──► result
Hadoop:            code ──► node 1 (block A)  node 2 (block B)  node 3 (block C)
                            process locally, in parallel, combine results
```

#### ¿Qué es Apache Hadoop?

Un framework de código abierto para guardar y procesar conjuntos de datos muy grandes en clusters de máquinas comunes. Sus módulos centrales son HDFS (almacenamiento distribuido), YARN (gestión de recursos), MapReduce (un modelo de procesamiento batch) y Hadoop Common (librerías compartidas).

#### ¿Qué problema resolvió Hadoop?

Guardar y procesar datos demasiado grandes para una sola máquina, de forma barata, repartiendo los datos y el cálculo entre muchos servidores económicos y tolerando los fallos de hardware por software, en lugar de comprar hardware especializado y caro.

#### ¿De dónde viene Hadoop?

De los artículos de Google sobre el Google File System (2003) y MapReduce (2004). Doug Cutting y Mike Cafarella implementaron esas ideas para el proyecto de búsqueda Nutch; Yahoo! invirtió fuerte, y Hadoop pasó a ser un proyecto de primer nivel de Apache en 2008.

#### ¿Cuáles son los principios de diseño de Hadoop?

Llevar el cálculo a los datos (localidad de datos), asumir que el hardware falla y manejarlo por software (replicación, reintentos de tareas), escalar horizontalmente con máquinas comunes, priorizar el rendimiento total sobre la baja latencia, y guardar los datos con el modelo "escribir una vez, leer muchas".

#### ¿Qué es la localidad de datos?

Programar las tareas en los nodos (o racks) que ya tienen los bloques de datos que leen, para que los datos no viajen por la red. Era crucial cuando la red era el cuello de botella.

#### ¿Cuáles son los archivos de configuración principales de Hadoop?

`core-site.xml` (ajustes comunes como el sistema de archivos por defecto `fs.defaultFS`), `hdfs-site.xml` (ajustes de HDFS como la replicación y los directorios del NameNode), `yarn-site.xml` (ajustes del ResourceManager y los NodeManager) y `mapred-site.xml` (ajustes de MapReduce).

#### ¿Qué diferencia hay entre Hadoop 1, 2 y 3?

Hadoop 1 combinaba la gestión de recursos y MapReduce en el modelo JobTracker/TaskTracker. Hadoop 2 introdujo YARN, que separó la gestión de recursos para que pudieran correr otros motores, y la alta disponibilidad del NameNode. Hadoop 3 añadió erasure coding, más de dos NameNodes, el requisito de Java 8+, YARN timeline service v2 y otras mejoras.

#### ¿Cuáles son las principales distribuciones de Hadoop?

Históricamente Cloudera, Hortonworks (fusionada con Cloudera en 2019) y MapR (comprada por HPE). Hoy Cloudera Data Platform es la principal distribución comercial, y los servicios en la nube (Amazon EMR, Google Dataproc, Azure HDInsight) ofrecen ecosistemas Hadoop administrados.

<!-- challenge -->

Un gerente pregunta por qué una consulta en Hadoop tarda 40 segundos en contar 10 filas cuando la base de datos responde al instante. ¿Qué le explicas?

<!-- solution -->

Hadoop está hecho para throughput sobre datasets enormes: cada job paga costos de programación y arranque que dominan en consultas diminutas. Es eficiente escaneando terabytes, no en búsquedas interactivas pequeñas, que debe servir una base de datos o un motor de baja latencia.

<!-- takeaways -->

- Hadoop reparte datos y trabajo entre muchas máquinas baratas.
- Lleva el cómputo a los datos.
- Optimiza el throughput batch, no la latencia.

<!-- unit: Versiones, distribuciones y ecosistema -->

<!-- goals -->

- Distinguir Hadoop 1, 2 y 3 y las principales distribuciones.
- Describir Hadoop Common, la abstracción FileSystem y los archivos de configuración principales.

<!-- concept -->

Hadoop pasó de ser un sistema MapReduce de un solo propósito a una plataforma. La versión 2 separó la gestión de recursos (YARN) del procesamiento, para que motores como Spark y Tez compartieran un clúster; la versión 3 agregó erasure coding y más NameNodes. Los proveedores lo empaquetaron en distribuciones con herramientas de gestión, y decenas de proyectos crecieron a su alrededor.
Por debajo, librerías compartidas y una abstracción de sistema de archivos permiten que el mismo código lea HDFS, discos locales o almacenamiento de objetos, configurado con unos pocos archivos XML.

<!-- example -->

```xml
<!-- core-site.xml -->
<property>
  <name>fs.defaultFS</name>
  <value>hdfs://prod-nameservice</value>
</property>
<!-- hdfs-site.xml -->
<property>
  <name>dfs.replication</name>
  <value>3</value>
</property>
```

#### ¿Qué es el ecosistema Hadoop?

El conjunto de proyectos construidos alrededor de Hadoop: Hive (SQL), HBase (NoSQL), Pig (scripting), Spark (procesamiento rápido), Kafka (streaming), ZooKeeper (coordinación), Oozie (flujos de trabajo), Sqoop y Flume (ingesta), Ranger y Atlas (seguridad y gobierno), Impala y Presto/Trino (SQL interactivo), entre otros.

#### ¿Por qué Hadoop es menos popular hoy para proyectos nuevos?

El almacenamiento de objetos en la nube (S3, ADLS, GCS) separa almacenamiento y cómputo de forma más barata y elástica, Spark reemplazó a MapReduce para el procesamiento, y los warehouses y lakehouses administrados (Snowflake, Databricks, BigQuery) eliminan la operación de clusters. Los clusters Hadoop son complejos de operar y ajustar.

#### ¿Sigue siendo relevante aprender Hadoop?

Sí, para mantener y migrar clusters existentes (frecuentes en bancos, telecomunicaciones y grandes empresas), y porque sus conceptos —sistemas de archivos distribuidos, bloques, replicación, localidad de datos, gestores de recursos, particionado, shuffle— explican cómo funcionan Spark, Hive y los lakehouses modernos.

#### ¿Qué es un cluster de hardware común (commodity)?

Un cluster de servidores estándar y relativamente baratos con discos locales, frente a máquinas especializadas de gama alta o SAN. Hadoop espera que los nodos individuales fallen y lo compensa.

#### ¿Qué significa "escribir una vez, leer muchas" en HDFS?

Los archivos se escriben una vez y luego sobre todo se leen; HDFS admite añadir al final (append) pero no actualizaciones aleatorias en medio de los archivos. Esto simplifica la consistencia y favorece la analítica batch.

#### ¿Cómo escala Hadoop?

Horizontalmente: se añaden DataNodes para más almacenamiento y NodeManagers para más cómputo; HDFS rebalancea los datos y YARN usa la capacidad nueva. La memoria del NameNode limita el número de archivos, lo que resuelve la federación.

<!-- challenge -->

Un equipo en Hadoop 1 quiere correr Spark en el mismo clúster. ¿Qué debe cambiar y por qué?

<!-- solution -->

Necesita Hadoop 2 o superior: YARN separa la gestión de recursos de MapReduce, así Spark puede pedir contenedores junto a otros motores. El JobTracker de Hadoop 1 solo corre MapReduce.

<!-- takeaways -->

- Hadoop 2 introdujo YARN; Hadoop 3 agregó erasure coding.
- El ecosistema creció alrededor de un clúster compartido.
- La API FileSystem abstrae HDFS, local y almacenamiento de objetos.

<!-- unit: Cómo se usa Hadoop -->

<!-- goals -->

- Describir el modelo write-once de HDFS, el schema on read y el escalado horizontal.
- Conocer las cargas típicas y el papel de los edge nodes.

<!-- concept -->

Los clústeres Hadoop se usaban como el data lake de la empresa: los archivos llegan una vez, los leen muchas veces jobs batch y reciben un esquema solo cuando un job o una tabla los interpreta. Ese modelo sirve para logs, ETL y analítica tipo warehouse, y escala agregando más nodos comunes.
Los usuarios no entran a los nodos worker. Trabajan desde edge nodes que tienen las herramientas cliente y la configuración, así el clúster se mantiene limpio y seguro.

<!-- example -->

```text
edge node (hdfs, hive, spark-submit clients)
   │ submits jobs / reads files
   ▼
master nodes: NameNode, ResourceManager
worker nodes: DataNode + NodeManager on every machine (storage and compute together)
```

#### ¿Qué es Hadoop Common?

Las librerías y utilidades compartidas que usan los demás módulos de Hadoop: abstracciones de sistema de archivos, RPC, serialización, configuración, seguridad y herramientas de línea de comandos.

#### ¿Qué es la abstracción `FileSystem` de Hadoop?

Una API Java que permite a las aplicaciones Hadoop trabajar con distintos sistemas de almacenamiento a través de una sola interfaz, con implementaciones para HDFS (`hdfs://`), archivos locales (`file://`), S3 (`s3a://`), Azure (`abfs://`), Google Cloud Storage (`gs://`) y otros.

#### ¿Qué cargas típicas corren en los clusters Hadoop?

ETL batch, procesamiento de logs, data warehousing con Hive, preparación de features de machine learning con Spark, indexación para búsqueda y almacenamiento de datos en bruto en un data lake central.

#### ¿Qué significa "esquema al leer" en Hadoop?

Los datos se guardan como archivos sin imponer un esquema al escribir; el esquema (por ejemplo una definición de tabla de Hive) se aplica al leer. Hace flexible la ingesta pero traslada la validación a los consumidores.

#### ¿Qué son los edge nodes?

Máquinas de acceso con las librerías cliente y la configuración de Hadoop pero sin los roles de DataNode ni NodeManager, desde las que los usuarios envían jobs, usan herramientas de línea de comandos y alojan aplicaciones cliente sin tocar los nodos trabajadores.

<!-- challenge -->

Una aplicación necesita actualizar registros individuales de un archivo muchas veces al día. ¿HDFS encaja bien?

<!-- solution -->

No. HDFS es write once, read many: soporta anexar pero no actualizaciones aleatorias. Usa una base de datos (o HBase para acceso por llave a gran escala), o reescribe los datos en lotes.

<!-- takeaways -->

- Los archivos de HDFS se escriben una vez y se leen muchas.
- El esquema se aplica al leer los datos.
- Los clústeres escalan agregando nodos; los usuarios trabajan desde edge nodes.

<!-- unit: Hadoop hoy -->

<!-- goals -->

- Explicar por qué los proyectos nuevos casi nunca eligen Hadoop.
- Explicar por qué conocer Hadoop sigue siendo valioso.

<!-- concept -->

El almacenamiento de objetos en la nube cambió la economía. Almacenamiento y cómputo ya no tienen que estar en las mismas máquinas, así que cada uno escala y se paga por separado, y los servicios administrados eliminan la operación de clústeres que Hadoop exige. La mayoría de plataformas nuevas arranca ahí.
Aun así, muchos bancos, telcos y grandes empresas siguen operando clústeres Hadoop enormes, y las herramientas modernas heredaron sus ideas: Spark, el metastore de Hive, Parquet y el particionamiento vienen de ese mundo. Conocer Hadoop ayuda a operar, migrar y entender lo que lo reemplazó.

<!-- example -->

| Pieza de Hadoop | Sucesor moderno |
|---|---|
| HDFS | S3, ADLS, GCS |
| YARN | Kubernetes, cómputo serverless |
| MapReduce | Spark, Flink |
| Tablas Hive | Tablas Iceberg / Delta |

#### ¿Por qué Hadoop prioriza el rendimiento total sobre la latencia?

Se diseñó para recorrer grandes conjuntos de datos en batch, donde importa más el tiempo total de procesamiento que el tiempo de respuesta de cada solicitud; HDFS lee bloques grandes de forma secuencial y los jobs de MapReduce tardan segundos en arrancar.

#### ¿Qué es HDFS?

El Hadoop Distributed File System: un sistema de archivos distribuido y tolerante a fallos que divide los archivos en bloques grandes y guarda réplicas de cada bloque en máquinas distintas, dando un acceso de alto rendimiento a conjuntos de datos grandes.

<!-- challenge -->

En una entrevista te preguntan por qué aprenderías Hadoop en 2026. Da una respuesta de dos frases.

<!-- solution -->

Muchas empresas grandes siguen operando clústeres Hadoop que necesitan mantenimiento y migración, y los conceptos detrás (almacenamiento distribuido, localidad de datos, particionamiento, el metastore) son la base de los lakehouses y de Spark actuales.

<!-- takeaways -->

- La nube separó almacenamiento y cómputo.
- Muchos clústeres aún necesitan operarse y migrarse.
- Las herramientas modernas heredan las ideas de Hadoop.

<!-- stage: Almacenamiento distribuido -->

### Arquitectura de HDFS

<!-- unit: NameNode y DataNodes -->

<!-- goals -->

- Describir los componentes de HDFS y qué guarda cada uno.
- Explicar heartbeats, block reports y safe mode.

<!-- concept -->

HDFS separa saber de guardar. El NameNode sabe: el árbol de directorios, los permisos, qué bloques forman cada archivo y dónde viven, todo en memoria. Los DataNodes guardan: bloques como archivos comunes en discos locales, sirviendo lecturas y escrituras directamente a los clientes.
Ambos lados se mantienen sincronizados con mensajes constantes. Los heartbeats muestran que un DataNode está vivo; los block reports le dicen al NameNode qué tiene. Al arrancar, el NameNode espera en un safe mode de solo lectura hasta que se reportan suficientes bloques.

<!-- example -->

```text
NameNode (memory):  /data/orders/part-0.parquet → blocks b1, b2
                    b1 → dn1, dn4, dn7     b2 → dn2, dn4, dn9
DataNode dn4 disk:  /hadoop/dfs/data/current/.../blk_b1, blk_b2
```

#### ¿Cuáles son los componentes principales de HDFS?

El NameNode (maestro que guarda el espacio de nombres y la ubicación de los bloques), los DataNodes (trabajadores que guardan los bloques en discos locales) y, en las configuraciones de alta disponibilidad, un NameNode standby, los JournalNodes y los ZooKeeper Failover Controllers.

#### ¿Qué guarda el NameNode?

El espacio de nombres del sistema de archivos (directorios, archivos, permisos, qué bloques forman cada archivo) en memoria, persistido como un checkpoint `fsimage` más un log `edits`. La ubicación de los bloques no se persiste; llega en los block reports de los DataNodes.

#### ¿Qué hace un DataNode?

Guarda los bloques como archivos en discos locales, atiende las solicitudes de lectura y escritura de los clientes, envía heartbeats y block reports al NameNode, y replica bloques hacia otros DataNodes cuando se le ordena.

#### ¿Cuál es el tamaño de bloque por defecto y por qué es tan grande?

128 MB en Hadoop 2 y 3 (64 MB en Hadoop 1). Los bloques grandes reducen los metadatos del NameNode, minimizan el tiempo de búsqueda frente al de transferencia y dan a cada tarea map una cantidad de datos razonable.

#### ¿Qué es el factor de replicación?

El número de copias de cada bloque, 3 por defecto (`dfs.replication`), configurable por archivo. Más réplicas significan más durabilidad y paralelismo de lectura, pero más almacenamiento.

#### ¿Qué es el rack awareness?

El NameNode sabe en qué rack está cada DataNode (con un script de topología) y ubica las réplicas para sobrevivir a la caída de un rack: por defecto la primera réplica en el nodo del escritor, la segunda en un nodo de otro rack y la tercera en otro nodo de ese segundo rack.

#### ¿Qué es el Secondary NameNode?

Un ayudante que fusiona periódicamente el log `edits` con el `fsimage` (checkpointing) para que el log no crezca sin fin y los reinicios del NameNode sean más rápidos. A pesar del nombre, no es un standby y no puede tomar el control si el NameNode falla.

<!-- challenge -->

Tras reiniciar el NameNode, las escrituras fallan 10 minutos con un error de "safe mode". ¿Hay algo roto?

<!-- solution -->

Probablemente no. El NameNode se queda en safe mode hasta que suficientes DataNodes reportan sus bloques; los clústeres grandes tardan minutos. Revisa `hdfs dfsadmin -safemode get` y el porcentaje de bloques reportados; fuerza la salida solo si de verdad faltan bloques.

<!-- takeaways -->

- El NameNode guarda metadatos; los DataNodes, bloques.
- Heartbeats y block reports los mantienen sincronizados.
- Safe mode protege los datos mientras se reportan los bloques.

<!-- unit: Bloques y replicación -->

<!-- goals -->

- Explicar los bloques grandes, la replicación y la ubicación consciente del rack.
- Comparar la replicación con el erasure coding.

<!-- concept -->

HDFS corta los archivos en bloques grandes, típicamente de 128 MB, para que el NameNode siga pocos objetos y los discos lean en secuencias largas y eficientes. Cada bloque se copia, tres veces por defecto, y la ubicación es consciente del rack: las copias se reparten entre racks para que la caída de uno no pierda datos.
Tres copias implican pagar tres veces el almacenamiento. El erasure coding guarda los datos con paridad, parecido a RAID, y baja el sobrecosto a cerca de la mitad, a cambio de más CPU y red al leer o reconstruir. Sirve para datos fríos.

<!-- example -->

| Esquema | Sobrecosto de almacenamiento | Sobrevive a |
|---|---|---|
| Replicación ×3 | 200 % | 2 copias perdidas |
| Erasure coding RS-6-3 | 50 % | 3 celdas perdidas de 9 |

#### ¿Cómo funciona la alta disponibilidad del NameNode?

Corren dos (o más, en Hadoop 3) NameNodes: uno activo y los demás en standby. Comparten el log de edits mediante un quórum de JournalNodes; los DataNodes reportan a todos. Los ZooKeeper Failover Controllers vigilan la salud y disparan el failover automático, con fencing para evitar dos NameNodes activos (split brain).

#### ¿Qué es la federación de HDFS?

Varios NameNodes independientes, cada uno con una parte del espacio de nombres (por ejemplo `/user` y `/data`), que comparten los mismos DataNodes. Escala el espacio de nombres más allá de la memoria de un NameNode y aísla las cargas. ViewFs o la federación basada en Router ofrecen una vista unificada.

#### ¿Qué es el Observer NameNode?

Un NameNode de solo lectura (Hadoop 3) que atiende lecturas con un estado consistente, descargando al NameNode activo en clusters con mucho tráfico de lectura de metadatos.

#### ¿Qué son los heartbeats y los block reports?

Los DataNodes envían un heartbeat cada pocos segundos para mostrar que están vivos, y periódicamente un block report completo con sus bloques. Si los heartbeats se detienen unos diez minutos, el NameNode marca el nodo como muerto y vuelve a replicar sus bloques.

#### ¿Qué es el safe mode?

Un estado de solo lectura en el que entra el NameNode al arrancar mientras carga el espacio de nombres y espera a que los DataNodes reporten suficientes réplicas de bloques. Sale solo cuando se alcanza un umbral de bloques, o un administrador puede sacarlo a mano.

<!-- challenge -->

Un clúster guarda 2 PB de logs de más de un año que se leen unas pocas veces por trimestre. ¿Cómo bajas su costo de almacenamiento?

<!-- solution -->

Aplica una política de erasure coding (por ejemplo RS-6-3) a los directorios de logs viejos, bajando el sobrecosto de 200 % a 50 %. Deja replicados los datos calientes por rendimiento de lectura.

<!-- takeaways -->

- Los bloques grandes mantienen pequeños los metadatos y eficientes las lecturas.
- Las réplicas se reparten entre racks por seguridad.
- El erasure coding ahorra espacio en datos fríos.

<!-- unit: Durabilidad de los metadatos -->

<!-- goals -->

- Explicar el fsimage y el edits log.
- Describir los papeles del Secondary NameNode y los JournalNodes.

<!-- concept -->

El NameNode guarda los metadatos en memoria por velocidad, así que necesita un registro durable en disco. Usa dos archivos: un checkpoint completo del namespace (fsimage) y un log de cada cambio desde entonces (edits). Al reiniciar, carga el checkpoint y reproduce el log.
Si el log crece sin fin, los reinicios tardan sin fin. Un ayudante fusiona periódicamente el log en el checkpoint. En montajes de alta disponibilidad, un pequeño quórum de JournalNodes guarda el log compartido, para que un NameNode standby siga cada cambio.

<!-- example -->

```text
fsimage_0000000000041000      (namespace at transaction 41000)
edits_0000000000041001-...    (every change since)
checkpoint: fsimage + edits → new fsimage, edits truncated
```

#### ¿Por qué el NameNode es un cuello de botella para escalar?

Todos los metadatos viven en su memoria: unos 150 bytes por archivo, directorio y bloque. Cientos de millones de objetos necesitan mucho heap, y cada operación de metadatos pasa por él. La federación, los observer NameNodes y evitar los archivos pequeños ayudan.

#### ¿Qué es el erasure coding en HDFS?

Una política de almacenamiento de Hadoop 3 que guarda los datos con paridad (por ejemplo Reed-Solomon 6+3) en lugar de tres copias completas, dando una tolerancia a fallos parecida con un 50 % de sobrecosto de almacenamiento en lugar del 200 %. Las lecturas y la reconstrucción cuestan más CPU y red, así que sirve para datos fríos.

#### ¿Qué son los archivos `fsimage` y `edits`?

`fsimage` es un checkpoint de todo el espacio de nombres en un momento dado; `edits` es el log de todos los cambios desde ese checkpoint. Al arrancar, el NameNode carga el `fsimage` y reproduce los edits.

<!-- challenge -->

Un reinicio del NameNode tarda dos horas. Los logs muestran que está reproduciendo un archivo de edits enorme. ¿Qué salió mal?

<!-- solution -->

Se detuvo el checkpointing: el Secondary o Standby NameNode no estaba fusionando los edits en el fsimage. Arregla el proceso de checkpoint y monitorea el tiempo desde el último checkpoint.

<!-- takeaways -->

- fsimage es un checkpoint; edits registra los cambios desde entonces.
- Los checkpoints mantienen rápidos los reinicios.
- Los JournalNodes comparten el edits log en montajes HA.

<!-- unit: Alta disponibilidad y escalado del NameNode -->

<!-- goals -->

- Explicar NameNode HA, fencing, observers y federación.
- Reconocer y manejar los límites de memoria del NameNode.

<!-- concept -->

El NameNode era el punto único de falla de Hadoop y su límite de escala. La alta disponibilidad agrega NameNodes standby que siguen el edits log compartido y toman el control cuando falla el activo; el fencing garantiza que el viejo activo no siga escribiendo. Los clientes deben hablar con el nameservice lógico, no con un host.
La escala es un problema de memoria: cada archivo y bloque cuesta heap del NameNode. La federación reparte el namespace entre varios NameNodes, los observers toman carga de lectura, y menos archivos más grandes reducen la presión.

<!-- example -->

```xml
<property><name>dfs.nameservices</name><value>prod-nameservice</value></property>
<property><name>dfs.ha.namenodes.prod-nameservice</name><value>nn1,nn2</value></property>
<!-- clients use hdfs://prod-nameservice/... never hdfs://nn1-host:8020/... -->
```

#### ¿Qué son los JournalNodes?

Un pequeño quórum de demonios (normalmente tres o cinco) que guardan el log de edits compartido de los NameNodes en HA; el NameNode activo escribe en la mayoría, y los standby leen de ellos para mantenerse sincronizados.

#### ¿Qué es el fencing en la HA del NameNode?

Mecanismos que garantizan que un NameNode que era activo ya no pueda modificar el espacio de nombres tras el failover (por ejemplo matando su proceso o haciendo que los JournalNodes solo acepten escrituras de una época de escritor), evitando el split brain.

#### ¿Cómo maneja HDFS un archivo más pequeño que un bloque?

Usa solo el disco que el archivo necesita; un archivo de 1 MB no consume 128 MB. Pero sigue costando un objeto de metadatos completo en el NameNode, que es el verdadero problema de los archivos pequeños.

#### ¿Qué es el espacio de nombres de HDFS?

La jerarquía de directorios y archivos, con permisos, propietarios, cuotas y fechas de modificación, que mantiene el NameNode, parecida al árbol de un sistema de archivos tradicional.

#### ¿Cómo funciona una escritura en HDFS?

El cliente le pide al NameNode crear el archivo; para cada bloque, el NameNode devuelve una lista de DataNodes. El cliente envía los datos en paquetes al primer DataNode, que los reenvía al segundo, que los reenvía al tercero (un pipeline). Las confirmaciones vuelven en sentido contrario, y el archivo es visible cuando se cierra.

#### ¿Cómo funciona una lectura en HDFS?

El cliente le pide al NameNode la ubicación de los bloques del archivo, y luego lee cada bloque directamente del DataNode más cercano que tiene una réplica, verificando los checksums; si un DataNode falla, cambia a otra réplica.

#### ¿Cómo detecta HDFS los datos corruptos?

Cada bloque tiene checksums calculados al escribir; los clientes los verifican al leer, y los DataNodes ejecutan un escáner de bloques en segundo plano. Las réplicas corruptas se reportan al NameNode, que vuelve a replicar desde una copia sana.

<!-- challenge -->

El uso de heap del NameNode crece 5 % al mes, sobre todo por millones de archivos diminutos. Además de agregar memoria, ¿qué haces?

<!-- solution -->

Ataca la cantidad de archivos: compacta archivos pequeños en grandes (o archívalos), arregla los jobs que los producen, pon cuotas de nombres en los directorios y considera la federación si el namespace sigue creciendo.

<!-- takeaways -->

- Los NameNodes standby y el fencing dan HA.
- Los clientes deben usar el nameservice HA.
- La memoria del NameNode crece con la cantidad de archivos y bloques.

### Operación de HDFS

<!-- unit: Lecturas, escrituras e integridad -->

<!-- goals -->

- Describir cómo lee y escribe datos HDFS.
- Explicar checksums, short-circuit reads y WebHDFS.

<!-- concept -->

Los datos nunca pasan por el NameNode. Para escribir, un cliente le pregunta dónde poner un bloque y luego manda los datos a un pipeline de DataNodes que se los pasan y confirman. Para leer, el cliente obtiene las ubicaciones de los bloques y lee directamente del DataNode más cercano.
La integridad se revisa en todas partes: los checksums se calculan al escribir y se verifican al leer, así la corrupción se detecta y se sirve desde otra réplica. Los lectores locales pueden saltarse la red por completo, y los clientes remotos pueden usar una API REST.

<!-- example -->

```text
write: client ──► dn1 ──► dn4 ──► dn7   (pipeline, acks flow back)
read:  client ──► NameNode: "where is b1?" ──► dn4 (closest) ──► data
```

#### ¿Qué pasa cuando muere un DataNode?

El NameNode deja de recibir heartbeats, lo marca como muerto tras un timeout y programa la re-replicación de sus bloques desde las réplicas restantes para recuperar el factor de replicación.

#### ¿Qué es el balancer de HDFS?

Una herramienta que mueve bloques entre DataNodes para que el uso del disco quede parejo en el cluster, normalmente tras añadir nodos. El disk balancer empareja el uso entre los discos de un mismo DataNode.

#### ¿Cómo se retira (decommission) un DataNode?

Añadiéndolo al archivo de exclusión y refrescando el NameNode (`hdfs dfsadmin -refreshNodes`); el NameNode vuelve a replicar sus bloques en otros nodos y, cuando termina, el nodo se puede quitar con seguridad.

#### ¿Cuáles son los comandos `hdfs dfs` más comunes?

```bash
hdfs dfs -ls /data/raw
hdfs dfs -mkdir -p /data/raw/orders/dt=2026-10-15
hdfs dfs -put orders.csv /data/raw/orders/dt=2026-10-15/
hdfs dfs -get /data/curated/report.parquet .
hdfs dfs -du -h /data
hdfs dfs -rm -r -skipTrash /tmp/old
hdfs dfs -setrep -w 2 /data/archive
```

#### ¿Qué hace `hdfs fsck`?

Revisa la salud de los archivos y bloques: bloques faltantes, corruptos, subreplicados o mal replicados, y puede listar la ubicación de los bloques (`hdfs fsck /ruta -files -blocks -locations`). Solo lee metadatos y no corrige los problemas por sí mismo.

<!-- challenge -->

Un disco corrompe en silencio unos pocos bloques. ¿Los usuarios reciben datos errados? ¿Qué pasa?

<!-- solution -->

No. Los checksums fallan al leer, así que el cliente lee otra réplica y reporta la corrupta; el NameNode programa una nueva copia sana. Los block scanners de los DataNodes también encuentran la corrupción de forma proactiva.

<!-- takeaways -->

- Los datos fluyen directamente entre clientes y DataNodes.
- Las escrituras usan un pipeline de replicación.
- Los checksums detectan la corrupción y la esquivan.

<!-- unit: Comandos de HDFS del día a día -->

<!-- goals -->

- Mover e inspeccionar datos con los comandos `hdfs dfs`.
- Revisar salud y capacidad con `fsck` y `dfsadmin`.

<!-- concept -->

La mayor parte del trabajo diario en HDFS son unos pocos comandos que se parecen a los de Unix: listar, copiar, mover, contar tamaños. La administración agrega chequeos de salud: `fsck` reporta bloques faltantes, corruptos o sub-replicados por ruta, y `dfsadmin` muestra la capacidad y el estado de los nodos en todo el clúster.
Cambiar la replicación de datos existentes también es un comando, útil para subir la protección de datos críticos o bajarla en espacio temporal.

<!-- example -->

```bash
hdfs dfs -mkdir -p /data/raw/orders/dt=2026-10-17
hdfs dfs -put orders.csv /data/raw/orders/dt=2026-10-17/
hdfs dfs -du -h /data/raw | sort -h | tail
hdfs dfs -count -q /data/raw/orders
hdfs fsck /data/raw/orders -files -blocks | tail
hdfs dfsadmin -report | head -20
```

#### ¿Qué muestra `hdfs dfsadmin -report`?

La capacidad del cluster, el espacio usado y libre, y el estado de cada DataNode (vivo, muerto, retirándose), útil para una revisión rápida de salud.

#### ¿Qué es la papelera (trash) de HDFS?

Cuando está activa (`fs.trash.interval`), los archivos borrados van a una carpeta `.Trash` en el directorio del usuario y se eliminan definitivamente tras el intervalo, lo que protege contra borrados accidentales. `-skipTrash` la omite.

#### ¿Qué son los snapshots de HDFS?

Copias de solo lectura de un directorio en un momento dado (activadas por directorio por un administrador), baratas porque solo registran los cambios; se usan para recuperarse de errores de los usuarios y para respaldos consistentes.

#### ¿Qué son las cuotas de HDFS?

Cuotas de nombres (número máximo de archivos y directorios) y de espacio (bytes máximos, incluidas las réplicas) definidas por directorio, para evitar que un equipo agote el cluster.

#### ¿Qué es `distcp`?

Una herramienta que copia grandes cantidades de datos entre clusters HDFS o entre HDFS y el almacenamiento de objetos, usando MapReduce para copiar en paralelo, con opciones de actualización incremental y conservación de atributos.

#### ¿Qué son las políticas de almacenamiento de HDFS?

Reglas que ubican las réplicas de los bloques en distintos tipos de almacenamiento (DISK, SSD, ARCHIVE, RAM_DISK) según la "temperatura": Hot, Warm, Cold, All_SSD, One_SSD y Lazy_Persist. La herramienta mover reubica los datos existentes según la política.

<!-- challenge -->

Un usuario dice que un dataset crítico "podría estar dañado". ¿Qué comandos corres y qué buscas?

<!-- solution -->

`hdfs fsck <path> -files -blocks -locations` para bloques faltantes, corruptos o sub-replicados, y `hdfs dfsadmin -report` para DataNodes caídos. Si faltan bloques sin réplica viva, restaura desde un snapshot o backup.

<!-- takeaways -->

- `hdfs dfs` cubre las operaciones de archivos.
- `fsck` revisa la salud de los bloques por ruta.
- `dfsadmin -report` muestra capacidad y nodos del clúster.

<!-- unit: Fallas de nodos y mantenimiento -->

<!-- goals -->

- Explicar qué pasa cuando falla un DataNode.
- Balancear, dar de baja y tolerar fallas de disco con seguridad.

<!-- concept -->

En un clúster grande siempre hay algún disco o nodo fallando. Cuando un DataNode deja de mandar heartbeats, el NameNode re-replica sus bloques desde las copias que sobreviven; tener bloques sub-replicados por un rato es normal. Los nodos también pueden tolerar unos pocos discos fallidos en vez de apagarse.
El trabajo planeado usa los mismos mecanismos con suavidad: dar de baja un nodo copia sus bloques a otro lado antes de retirarlo, y el balancer empareja el uso de disco tras agregar nodos.

<!-- example -->

```bash
echo "dn12.prod" >> /etc/hadoop/conf/dfs.exclude
hdfs dfsadmin -refreshNodes          # dn12 → "Decommission in progress"
hdfs dfsadmin -report | grep -A3 dn12
hdfs balancer -threshold 10          # after adding new nodes
```

#### ¿Qué es la lectura local short-circuit?

Cuando el cliente corre en el mismo nodo que el DataNode que tiene un bloque, lee el archivo directamente del disco local mediante un descriptor de archivo compartido, sin pasar por la red del DataNode, lo que acelera las lecturas.

#### ¿Qué es el problema de los archivos pequeños en HDFS?

Millones de archivos mucho más pequeños que el tamaño de bloque consumen memoria del NameNode (cada archivo y bloque es un objeto), vuelven lentos los listados y crean muchas tareas diminutas. Soluciones: compactar archivos (`INSERT OVERWRITE` de Hive, repartition en Spark), usar formatos contenedores (SequenceFile, Parquet, ORC) o archivar con archivos HAR.

#### ¿Cómo se cambia el factor de replicación de datos existentes?

Con `hdfs dfs -setrep -w <n> <ruta>`, que cambia la replicación de los archivos y espera hasta que se añadan o quiten las réplicas.

#### ¿Qué controla `dfs.datanode.failed.volumes.tolerated`?

Cuántos fallos de disco tolera un DataNode antes de apagarse; por defecto cero, pero los nodos grandes con muchos discos suelen configurarse para seguir funcionando con uno o dos discos fallidos.

#### ¿Cómo se mueven datos entre HDFS y el sistema de archivos local?

`hdfs dfs -put`/`-copyFromLocal` para subir, `hdfs dfs -get`/`-copyToLocal` para descargar, y `hdfs dfs -getmerge` para concatenar un directorio de archivos de partes en un solo archivo local.

<!-- challenge -->

Necesitas retirar tres DataNodes para reemplazar hardware sin arriesgar datos. ¿Qué pasos sigues?

<!-- solution -->

Dalos de baja con el archivo de exclusión y `-refreshNodes`, espera a que aparezcan como "Decommissioned" (todos los bloques copiados a otro lado) y luego apágalos. Corre el balancer cuando entre el hardware nuevo.

<!-- takeaways -->

- El NameNode re-replica los bloques de los nodos caídos.
- Da de baja los nodos antes de retirarlos.
- El balancer empareja el uso de disco.

<!-- unit: Proteger y organizar los datos -->

<!-- goals -->

- Usar trash, snapshots y cuotas para proteger los datos.
- Ubicar datos con storage policies y copiarlos con `distcp`.

<!-- concept -->

HDFS ofrece varias redes de seguridad contra errores. La papelera guarda un tiempo los archivos borrados; los snapshots guardan vistas de solo lectura de directorios en un momento dado casi sin costo; las cuotas evitan que un equipo llene el clúster.
Las storage policies ponen los datos en el medio correcto, como SSD para datos calientes o discos de archivo para fríos, y `distcp` copia datasets grandes entre clústeres o hacia almacenamiento de objetos con un job paralelo.

<!-- example -->

```bash
hdfs dfsadmin -allowSnapshot /data/finance
hdfs dfs -createSnapshot /data/finance before-reload-2026-10-17
hdfs dfsadmin -setSpaceQuota 50t /data/marketing
hadoop distcp -update hdfs://prod/data/finance s3a://backup-bucket/finance
```

#### ¿Qué muestra `hdfs dfs -count`?

El número de directorios, archivos y bytes bajo una ruta y, con `-q`, las cuotas de nombres y de espacio, útil para encontrar directorios con demasiados archivos pequeños.

#### ¿Qué es WebHDFS?

Una API REST de HDFS sobre HTTP que permite a clientes en cualquier lenguaje leer, escribir y administrar archivos sin las librerías de Hadoop; HttpFS ofrece una versión tipo gateway.

#### ¿Qué es YARN?

Yet Another Resource Negotiator: el gestor de recursos del cluster Hadoop. Asigna CPU y memoria en contenedores a las aplicaciones (MapReduce, Spark, Tez, Flink), separando la gestión de recursos del motor de procesamiento.

#### ¿Cuáles son los componentes principales de YARN?

El ResourceManager (programador y gestor de aplicaciones de todo el cluster), los NodeManagers (agentes por nodo que lanzan y vigilan los contenedores), los ApplicationMasters (uno por aplicación, que negocian recursos y coordinan las tareas) y los contenedores (paquetes asignados de memoria y vcores).

#### ¿Qué pasa cuando envías una aplicación a YARN?

El cliente la envía al ResourceManager, que arranca el ApplicationMaster en un contenedor en algún nodo. El ApplicationMaster pide contenedores para las tareas, teniendo en cuenta la localidad de los datos; los NodeManagers los lanzan; el ApplicationMaster vigila el avance e informa la finalización.

<!-- challenge -->

Antes de una recarga riesgosa de un directorio de finanzas, ¿cómo te aseguras de poder revertir en minutos?

<!-- solution -->

Toma un snapshot de HDFS del directorio antes de la recarga. Si sale mal, copia los archivos de vuelta desde la ruta `.snapshot` (los snapshots son baratos e instantáneos de crear).

<!-- takeaways -->

- Trash y snapshots protegen contra errores.
- Las cuotas protegen la capacidad compartida.
- `distcp` copia datos grandes en paralelo.

<!-- unit: El problema de los archivos pequeños -->

<!-- goals -->

- Explicar por qué los archivos pequeños dañan a HDFS y a los jobs que lo leen.
- Arreglar y prevenir el crecimiento de archivos pequeños.

<!-- concept -->

Cada archivo, por diminuto que sea, cuesta memoria del NameNode y normalmente una tarea aparte al leerlo. Millones de archivos pequeños agotan entonces el NameNode y hacen que los jobs pasen más tiempo arrancando tareas que procesando datos.
Suelen venir de jobs de streaming o con demasiado paralelismo que escriben un archivo por tarea. La cura está en la fuente, escribir menos archivos y más grandes, más una compactación periódica de lo que ya existe.

<!-- example -->

```text
50,000 files × 200 KB  = 10 GB  → 50,000 NameNode objects, 50,000 map tasks
80 files × 128 MB      = 10 GB  → 80 objects, 80 tasks
```

#### ¿Qué programadores ofrece YARN?

El programador FIFO (el primero que llega, primero atendido), el Capacity Scheduler (colas jerárquicas con capacidades garantizadas y elasticidad, el predeterminado en la mayoría de las distribuciones) y el Fair Scheduler (reparte los recursos de forma justa entre aplicaciones y colas en ejecución).

#### ¿Cómo funciona el Capacity Scheduler?

Las colas se configuran con porcentajes garantizados de la capacidad del cluster (por ejemplo `etl` 50 %, `analytics` 30 %, `adhoc` 20 %), pueden tomar prestada capacidad ociosa hasta un máximo, tienen límites por usuario y pueden expropiar contenedores para devolver la capacidad garantizada.

<!-- challenge -->

Un job de streaming escribe un archivo por partición cada minuto. ¿Cómo frenas el crecimiento sin perder frescura?

<!-- solution -->

Deja los archivos por minuto en un área de landing y corre una compactación cada hora o cada día que los reescriba en pocos archivos grandes (o usa un formato de tabla con compactación), y luego borra los originales.

<!-- takeaways -->

- Los archivos pequeños cuestan memoria del NameNode y sobrecarga de tareas.
- Escribe menos archivos y más grandes en la fuente.
- Compacta lo que ya existe.

### YARN

<!-- unit: Elegir un formato de archivo -->

<!-- goals -->

- Comparar texto, SequenceFile, Avro, Parquet y ORC.
- Explicar la divisibilidad y cuándo usar Avro o Parquet.

<!-- concept -->

Los formatos de archivo deciden cuánto trabaja un job antes de calcular nada. El texto es universal pero voluminoso y sin tipos. SequenceFiles y Avro guardan filas en binario, y Avro lleva su esquema para evolucionar con seguridad, lo que sirve para mensajes e ingesta. Los formatos columnares sirven para analítica.
La divisibilidad decide el paralelismo: un formato que se puede leer en trozos independientes deja que muchas tareas compartan un archivo grande. Existen soluciones para archivos pequeños como los archives, pero no reemplazan escribir mejor.

<!-- example -->

| Necesidad | Formato |
|---|---|
| Ingestar eventos de Kafka con esquema cambiante | Avro |
| Tablas analíticas consultadas por columna | Parquet u ORC |
| Datos clave-valor intermedios de MapReduce | SequenceFile |
| Archivar millones de archivos diminutos | HAR |

#### ¿Qué es la expropiación (preemption) en YARN?

Cuando una cola está por debajo de su parte garantizada y otras usan más, el programador puede matar contenedores de las aplicaciones que usan de más para liberar recursos y cumplir las garantías.

#### ¿Cómo se configuran los tamaños de los contenedores?

Con `yarn.nodemanager.resource.memory-mb` y `.cpu-vcores` (recursos que ofrece un nodo), `yarn.scheduler.minimum-allocation-mb` y `maximum-allocation-mb` (tamaños de contenedor permitidos), y las solicitudes de cada aplicación (por ejemplo `mapreduce.map.memory.mb` o la memoria de los executors de Spark más el overhead).

#### ¿Qué pasa cuando un contenedor supera su memoria?

El NodeManager lo mata ("Container killed by YARN for exceeding memory limits") y la tarea se reintenta. Se corrige aumentando la memoria o el overhead del contenedor, o reduciendo el uso de memoria por tarea (más particiones, menos caché).

#### ¿Qué son las node labels en YARN?

Etiquetas que dividen los nodos (por ejemplo `gpu` o `high-memory`), para que las colas y aplicaciones se limiten a grupos de nodos concretos.

#### ¿Cómo funciona la alta disponibilidad del ResourceManager?

Un ResourceManager activo y uno standby se coordinan mediante ZooKeeper; el estado se guarda en un state store para que el standby tome el control y las aplicaciones en curso puedan continuar (reinicio que conserva el trabajo).

#### ¿Qué es el YARN Timeline Service?

Un servicio que guarda y sirve el historial de las aplicaciones y sus tareas (horas de inicio, duraciones, contadores) para monitorear y depurar después de que terminan. Spark tiene su propio History Server.

<!-- challenge -->

Los eventos crudos llegan en Avro, y los analistas consultan tres columnas de un dataset de 200. ¿Qué organización sugieres?

<!-- solution -->

Mantén Avro para la ingesta cruda (evolución de esquema, registros completos) y convierte a Parquet u ORC particionado para las tablas analíticas, para que las consultas lean solo las columnas que necesitan.

<!-- takeaways -->

- Avro para filas y evolución de esquema; columnar para analítica.
- Los formatos divisibles permiten lecturas en paralelo.
- Los archives ayudan con archivos pequeños pero no arreglan su origen.

<!-- unit: Formatos columnares y compresión -->

<!-- goals -->

- Describir cómo organizan los datos Parquet y ORC.
- Elegir codecs de compresión, también para la salida intermedia.

<!-- concept -->

Parquet y ORC agrupan las filas en trozos grandes (row groups o stripes) y guardan cada columna por separado dentro de ellos, con estadísticas que permiten saltarse trozos. ORC creció con Hive y agrega índices livianos; Parquet es el más soportado entre motores.
La compresión multiplica el beneficio, pero el codec importa: los rápidos como Snappy sirven para datos calientes y salida intermedia, los más fuertes ahorran más espacio, y los codecs no divisibles sobre texto plano limitan el paralelismo.

<!-- example -->

```properties
# compress map output to cut shuffle I/O
mapreduce.map.output.compress=true
mapreduce.map.output.compress.codec=org.apache.hadoop.io.compress.SnappyCodec
```

#### ¿Cómo se inspeccionan y matan aplicaciones de YARN?

```bash
yarn application -list -appStates RUNNING
yarn application -status application_1729000000000_0042
yarn logs -applicationId application_1729000000000_0042 | less
yarn application -kill application_1729000000000_0042
```

#### ¿Qué diferencia hay entre los modos client y cluster de Spark en YARN?

En modo client, el driver de Spark corre en la máquina que envió el job (un edge node), útil para el trabajo interactivo; en modo cluster, el driver corre dentro del contenedor del ApplicationMaster en el cluster, mejor para los jobs de producción que deben sobrevivir a la desconexión del cliente.

#### ¿Qué son los vcores?

Núcleos de CPU virtuales que anuncian los NodeManagers, una unidad abstracta que YARN usa para programar CPU; qué tan estrictamente se aplica depende del calculador de recursos y de la configuración de cgroups.

#### ¿Qué es el DominantResourceCalculator?

Un calculador de recursos de YARN que tiene en cuenta memoria y CPU al programar (el recurso dominante de cada solicitud), en lugar del predeterminado, que solo mira la memoria.

#### ¿Qué es el shared cache de YARN?

Una función que guarda en caché los recursos de las aplicaciones (JAR, archivos) en los nodos entre aplicaciones, reduciendo el tiempo y el ancho de banda de localizar una y otra vez las mismas dependencias.

<!-- challenge -->

Un job lee un único archivo `.csv.gz` de 40 GB y usa una sola tarea map. ¿Por qué y cómo lo arreglas?

<!-- solution -->

Gzip no es divisible, así que una sola tarea debe leer todo el archivo. Divide la entrada antes de comprimir, usa un codec divisible (bzip2) o, mejor, convierte a Parquet u ORC con Snappy o ZSTD.

<!-- takeaways -->

- Parquet y ORC guardan columnas en trozos con estadísticas.
- Codecs rápidos para datos calientes e intermedios.
- El texto comprimido no divisible limita el paralelismo.

<!-- stage: Cómputo en el clúster -->

### MapReduce

<!-- unit: Arquitectura de YARN -->

<!-- goals -->

- Describir los componentes de YARN y el ciclo de vida de una aplicación.
- Inspeccionar, gestionar y dar alta disponibilidad al ResourceManager.

<!-- concept -->

YARN convirtió Hadoop en una plataforma compartida. El ResourceManager es dueño de la capacidad del clúster; los NodeManagers ofrecen la CPU y memoria de cada nodo como contenedores; cada aplicación tiene su propio ApplicationMaster que negocia contenedores y sigue sus tareas. MapReduce, Spark y Tez corren así lado a lado.
Como el ResourceManager es central, corre con un standby, y un timeline service conserva la historia cuando las aplicaciones terminan.

<!-- example -->

```bash
yarn application -list -appStates RUNNING
yarn application -status application_1729150000000_0042
yarn logs -applicationId application_1729150000000_0042 | less
yarn application -kill application_1729150000000_0042
```

#### ¿Cómo se limita que un usuario use todo el cluster?

Con límites de las colas del programador: capacidad máxima por cola, factores de límite por usuario, máximo de aplicaciones por usuario y por cola, y listas de control de acceso en las colas.

#### ¿Qué es MapReduce?

Un modelo de programación y motor de ejecución para procesamiento batch: una función map procesa los registros de entrada en pares clave-valor intermedios, el framework agrupa todos los valores por clave (shuffle y sort), y una función reduce agrega los valores de cada clave en resultados.

#### Explica el conteo de palabras en MapReduce.

El mapper lee líneas y emite `(palabra, 1)` por cada palabra. El shuffle agrupa los pares por palabra. El reducer recibe `(palabra, [1, 1, 1, …])` y emite `(palabra, suma)`. Un combiner puede sumar localmente después del map para reducir los datos del shuffle.

#### ¿Qué es un InputSplit?

Un trozo lógico de la entrada asignado a una tarea map, normalmente correspondiente a un bloque de HDFS. El número de splits determina el número de tareas map.

#### ¿Qué es un RecordReader?

El componente que lee un InputSplit y lo convierte en registros clave-valor para el mapper; por ejemplo `LineRecordReader` da (desplazamiento en bytes, línea).

#### ¿Qué pasa durante el shuffle y el sort?

Las salidas del map se particionan por clave, se ordenan y se derraman al disco local; los reducers traen sus particiones de todos los mappers por la red, las fusionan ordenadas y entregan las claves agrupadas a la función reduce. Suele ser la fase más costosa.

<!-- challenge -->

Una consulta de Hive descontrolada está acaparando casi todo el clúster. ¿Cómo la encuentras y la detienes desde la línea de comandos?

<!-- solution -->

Lista las aplicaciones en curso con `yarn application -list`, identifícala por usuario, cola y recursos, revísala con `-status` y detenla con `yarn application -kill <id>`. Luego revisa los límites de las colas.

<!-- takeaways -->

- El ResourceManager asigna; los NodeManagers corren contenedores.
- Cada aplicación tiene su propio ApplicationMaster.
- El ResourceManager corre con un standby para HA.

<!-- unit: Schedulers y colas -->

<!-- goals -->

- Comparar los schedulers de YARN y configurar colas de capacidad.
- Usar preemption, node labels y límites por usuario.

<!-- concept -->

Un clúster compartido necesita reglas sobre quién recibe qué. El Capacity Scheduler divide el clúster en colas con participaciones garantizadas que pueden tomar prestada la capacidad ociosa. Cuando una cola necesita recuperar su garantía, la preemption reclama contenedores a quienes la tomaron prestada.
Otros controles afinan las reglas: los node labels dirigen trabajo a hardware especial y los límites por usuario evitan que una persona se quede con una cola entera.

<!-- example -->

```xml
<property><name>yarn.scheduler.capacity.root.queues</name><value>etl,analytics,adhoc</value></property>
<property><name>yarn.scheduler.capacity.root.etl.capacity</name><value>50</value></property>
<property><name>yarn.scheduler.capacity.root.analytics.capacity</name><value>35</value></property>
<property><name>yarn.scheduler.capacity.root.adhoc.capacity</name><value>15</value></property>
<property><name>yarn.scheduler.capacity.root.adhoc.maximum-capacity</name><value>30</value></property>
```

#### ¿Qué es un combiner?

Un "mini-reducer" opcional que corre sobre la salida del map antes del shuffle para preagregar los valores por clave, reduciendo la transferencia por la red. Debe ser seguro aplicarlo cero, una o varias veces (operaciones asociativas y conmutativas como suma o máximo).

#### ¿Qué es un partitioner?

La función que decide qué reducer recibe cada clave, por defecto `hash(clave) % numReducers`. Los partitioners propios controlan la distribución de los datos, por ejemplo para evitar el skew o agrupar claves relacionadas.

#### ¿Cómo se elige el número de reducers?

Suficientes para paralelizar el trabajo de reduce y mantener razonable la entrada de cada reducer, típicamente alrededor de 0,95 o 1,75 veces los slots de reduce o según el tamaño de la salida; cero reducers dan un job solo de map.

#### ¿Qué es la ejecución especulativa?

Cuando algunas tareas van mucho más lento que las demás (rezagadas), el framework lanza intentos duplicados en otros nodos y usa el que termine primero. Ayuda con hardware lento pero desperdicia recursos y debe desactivarse si hay efectos secundarios no idempotentes.

#### ¿Qué son los contadores (counters)?

Números con nombre que las tareas incrementan (los integrados, como registros leídos, bytes escritos o registros derramados, y los propios, como "filas inválidas"), agregados en todo el job para monitorear y validar.

<!-- challenge -->

Las consultas ad hoc toman prestada toda la capacidad ociosa de noche, y el ETL de las 05:00 las espera. ¿Qué configuras?

<!-- solution -->

Activa la preemption para que la cola de ETL recupere su participación garantizada, y limita la capacidad máxima de la cola ad hoc y los límites por usuario.

<!-- takeaways -->

- Las colas garantizan participaciones y toman prestada capacidad ociosa.
- La preemption devuelve las garantías.
- Labels y límites por usuario afinan la asignación.

<!-- unit: Contenedores y recursos -->

<!-- goals -->

- Configurar los tamaños de contenedor y entender los kills por memoria.
- Explicar vcores, el DominantResourceCalculator y el shared cache.

<!-- concept -->

Cada tarea corre en un contenedor con un tamaño de memoria y CPU. Los nodos anuncian lo que ofrecen, el scheduler impone mínimos y máximos, y el NodeManager mata cualquier contenedor que se pase de memoria. La mayoría de errores "killed by YARN" significan que el contenedor era muy pequeño para el heap más las necesidades fuera del heap.
Por defecto solo cuenta la memoria al acomodar contenedores; el dominant resource calculator agrega la CPU para que los jobs pesados en CPU no sobrecarguen los nodos. Cachear archivos de aplicación entre jobs acelera el arranque.

<!-- example -->

```properties
yarn.nodemanager.resource.memory-mb=114688      # 112 GB offered per node
yarn.nodemanager.resource.cpu-vcores=30
yarn.scheduler.minimum-allocation-mb=1024
yarn.scheduler.maximum-allocation-mb=32768
```

#### ¿Qué es el distributed cache?

Un mecanismo para enviar archivos de solo lectura (tablas de búsqueda, JAR, configuración) a cada nodo que ejecuta tareas de un job, para que las tareas los lean en local.

#### ¿Cómo se hace un join en MapReduce?

Un join del lado del reduce etiqueta los registros de ambos conjuntos, los emite por la clave del join y los une en el reducer (general, pero hace shuffle de todo). Un join del lado del map carga el conjunto pequeño en memoria con el distributed cache y une en el mapper (rápido, pero un lado debe caber en memoria).

#### ¿Por qué Spark reemplazó a MapReduce en la mayoría de las cargas?

MapReduce escribe los resultados intermedios en disco entre cada etapa y expresa los pipelines complejos como cadenas de jobs, lo que es lento y verboso. Spark mantiene los datos en memoria entre etapas, optimiza DAG completos y ofrece APIs de alto nivel (SQL, DataFrames) en varios lenguajes.

#### ¿Qué es Hadoop Streaming?

Una utilidad que permite escribir mappers y reducers en cualquier lenguaje que lea stdin y escriba stdout (Python, bash), mientras Hadoop maneja la distribución; fue popular antes de PySpark.

#### ¿Para qué sirve un job solo de map?

Para transformaciones que no necesitan agrupar, como filtrar, convertir formatos o interpretar logs, con cero reducers para que la salida del mapper se escriba directamente.

<!-- challenge -->

Los nodos muestran 90 % de memoria asignada pero 300 % de carga de CPU, y los jobs van lentísimo. ¿Qué ajuste revisas?

<!-- solution -->

El resource calculator: con el de por defecto solo se considera la memoria, así que demasiados contenedores ávidos de CPU caen en un nodo. Cambia al DominantResourceCalculator y fija vcores realistas por contenedor.

<!-- takeaways -->

- Los contenedores tienen tamaños de memoria y CPU con límites.
- Pasarse de memoria hace que maten el contenedor.
- El DominantResourceCalculator también programa la CPU.

### Formatos de archivo y compresión

<!-- unit: El modelo MapReduce -->

<!-- goals -->

- Explicar map, shuffle y reduce con el conteo de palabras.
- Escribir jobs en Java u otros lenguajes y saber por qué Spark reemplazó a MapReduce.

<!-- concept -->

MapReduce divide un cálculo en dos funciones simples. Map convierte cada registro de entrada en pares clave-valor; el framework agrupa todos los valores por clave; reduce combina los valores de cada clave en un resultado. Como ambas funciones trabajan sobre piezas independientes, el framework puede correr miles en paralelo y reintentar cualquiera que falle.
La debilidad del modelo es que cada etapa escribe a disco, así que los pipelines de varios pasos se vuelven cadenas de jobs lentos. Spark conservó la idea y mantuvo los datos en memoria entre etapas.

<!-- example -->

```text
input:  "to be or not to be"
map:    (to,1) (be,1) (or,1) (not,1) (to,1) (be,1)
shuffle: be→[1,1]  not→[1]  or→[1]  to→[1,1]
reduce: (be,2) (not,1) (or,1) (to,2)
```

#### ¿Cuáles son las clases principales de un job MapReduce en Java?

Una subclase de `Mapper` con un método `map()`, una subclase de `Reducer` con `reduce()`, y un driver que configura el `Job` (formatos y rutas de entrada y salida, tipos de clave y valor, número de reducers) y lo envía.

#### ¿Qué son InputFormat y OutputFormat?

`InputFormat` define cómo se divide y lee la entrada (`TextInputFormat`, `SequenceFileInputFormat`, `KeyValueTextInputFormat`, `CombineFileInputFormat` para muchos archivos pequeños); `OutputFormat` define cómo se escriben los resultados (`TextOutputFormat`, `SequenceFileOutputFormat`).

#### ¿Para qué sirve `CombineFileInputFormat`?

Para agrupar muchos archivos pequeños en menos splits, de modo que un job sobre miles de archivos pequeños no lance miles de tareas map diminutas.

#### ¿Qué papel cumple el OutputCommitter?

Hace que la salida del job aparezca de forma atómica: las tareas escriben en directorios temporales y el committer mueve los resultados a la ubicación final cuando el job termina bien, para que los intentos fallidos o especulativos no dejen salidas parciales.

#### ¿Qué es un secondary sort?

Una técnica para que los valores lleguen al reducer ordenados por un campo secundario, usando una clave compuesta, un partitioner propio sobre la clave natural y un comparador de agrupamiento.

#### ¿Por qué las tareas map deberían durar al menos un minuto o algo así?

Arrancar una tarea tiene un costo (lanzar la JVM, programarla); las tareas muy cortas pasan más tiempo arrancando que procesando. Splits más grandes o archivos pequeños agrupados hacen eficientes las tareas.

<!-- challenge -->

Un pipeline de cinco jobs MapReduce corre tres horas, casi todo escribiendo y leyendo datos intermedios. ¿Qué cambiaría pasarlo a Spark?

<!-- solution -->

Spark corre los cinco pasos como una aplicación con un DAG de etapas, manteniendo los datos intermedios en memoria (o en disco local solo en los shuffles) en vez de escribir a HDFS entre jobs, lo que suele reducir mucho el tiempo.

<!-- takeaways -->

- Map emite pares clave-valor; reduce combina por clave.
- El paralelismo y los reintentos vienen de tareas independientes.
- El disco entre etapas volvió lento a MapReduce para pipelines.

<!-- unit: Entradas y salidas -->

<!-- goals -->

- Explicar InputSplits, RecordReaders y formatos de entrada y salida.
- Manejar muchas entradas pequeñas y commits atómicos de salida.

<!-- concept -->

Antes de que un mapper vea un registro, el framework decide cómo dividir la entrada (splits, normalmente uno por bloque) y cómo convertir bytes en registros (un RecordReader del formato de entrada). A la salida, un formato de salida escribe los resultados y un committer los hace aparecer de una vez, para que los lectores nunca vean media salida de un job.
Muchos archivos de entrada pequeños implicarían muchos splits diminutos; combinarlos en menos splits mantiene razonable la cantidad de tareas.

<!-- example -->

```java
job.setInputFormatClass(CombineTextInputFormat.class);
CombineTextInputFormat.setMaxInputSplitSize(job, 256L * 1024 * 1024);   // pack small files
job.setOutputFormatClass(TextOutputFormat.class);
```

#### ¿Qué formatos de archivo son comunes en Hadoop?

Texto (CSV, JSON), SequenceFile (clave-valor binario), Avro (por filas con el esquema embebido, bueno para ingesta y evolución del esquema), Parquet y ORC (columnares, comprimidos, con estadísticas, los mejores para analítica).

#### ¿Qué es un formato de archivo divisible (splittable) y por qué importa?

Uno que pueden leer en trozos independientes tareas distintas. El texto plano, SequenceFile, Avro, Parquet y ORC son divisibles; un archivo de texto comprimido con gzip no lo es, así que una sola tarea debe leerlo completo, lo que limita el paralelismo.

#### ¿Qué códecs de compresión se usan en Hadoop?

Snappy y LZ4 (rápidos, compresión moderada), gzip/Deflate (mejor compresión, más lentos, no divisibles para texto), bzip2 (divisible, lento), LZO (divisible con un índice) y ZSTD (buena relación y velocidad). Dentro de Parquet y ORC la compresión es por bloque, así que los archivos siguen siendo divisibles.

#### ¿Por qué ORC se asocia con Hive?

ORC (Optimized Row Columnar) se creó para Hive: almacenamiento columnar con índices ligeros, estadísticas y filtros bloom, y admite las tablas ACID de Hive. Parquet es más común en los demás motores.

#### ¿Qué ventaja tiene Avro en los pipelines de datos?

El esquema se guarda con los datos y admite evolución (añadir campos con valores por defecto, renombrar con alias), y su formato compacto por filas sirve para streaming e ingesta, a menudo con un schema registry en Kafka.

<!-- challenge -->

Un job sobre 20.000 archivos de 100 KB lanza 20.000 tareas map y corre lento. ¿Qué cambias?

<!-- solution -->

Usa `CombineFileInputFormat` (o `CombineTextInputFormat`) para empacar los archivos pequeños en splits de unos cientos de MB, así unas pocas decenas de tareas hacen el trabajo. A largo plazo, compacta los archivos.

<!-- takeaways -->

- Los splits dividen la entrada; los RecordReaders producen registros.
- Combina archivos pequeños en splits más grandes.
- Los committers hacen aparecer la salida de forma atómica.

<!-- unit: Shuffle, combiners y partitioners -->

<!-- goals -->

- Explicar shuffle y sort y cómo los combiners lo reducen.
- Controlar el particionamiento, la cantidad de reducers y los secondary sorts.

<!-- concept -->

El shuffle es donde MapReduce gasta la mayor parte de su esfuerzo: la salida de map se particiona por clave, se ordena, se escribe a disco y los reducers la traen por la red. Todo lo que lo achique ayuda. Un combiner preagrega del lado map, así viajan muchos menos datos.
El particionamiento decide qué reducer recibe cada clave, y la cantidad de reducers decide el paralelismo. Los partitioners personalizados reparten claves sesgadas; un secondary sort entrega los valores al reducer ya ordenados.

<!-- example -->

```java
job.setMapperClass(WordMapper.class);
job.setCombinerClass(SumReducer.class);   // safe: sum is associative and commutative
job.setReducerClass(SumReducer.class);
job.setNumReduceTasks(40);
```

#### ¿Qué es un SequenceFile?

Un archivo binario plano de pares clave-valor, divisible y comprimible, usado como salida intermedia de MapReduce y para empaquetar muchos archivos pequeños en un contenedor.

#### ¿Qué son los archivos HAR?

Hadoop Archives: una forma de empaquetar muchos archivos pequeños en un solo archivo (un índice más archivos de partes) para reducir los objetos del NameNode, manteniendo los archivos accesibles con una ruta `har://`.

#### ¿Cómo organiza Parquet los datos?

Los archivos contienen grupos de filas; cada grupo guarda fragmentos por columna, divididos en páginas con codificación y compresión; el pie del archivo contiene el esquema y las estadísticas (mínimo/máximo, nulos) por grupo y columna, lo que permite podar columnas y empujar predicados.

#### ¿Cómo organiza ORC los datos?

Los archivos se dividen en stripes (normalmente de 64–256 MB) con flujos por columna, índices ligeros cada 10.000 filas (mínimo/máximo), filtros bloom opcionales y un pie con estadísticas por stripe, lo que permite a los motores saltar stripes y grupos de filas.

#### ¿Conviene comprimir la salida intermedia de MapReduce?

Normalmente sí, con un códec rápido como Snappy o LZ4 (`mapreduce.map.output.compress`), porque reduce la E/S de disco y de red durante el shuffle con un costo pequeño de CPU.

<!-- challenge -->

Un job calcula un promedio por clave y alguien agrega el reducer como combiner. Los resultados salen mal. ¿Por qué?

<!-- solution -->

Los promedios no son asociativos: promediar promedios parciales ignora los conteos. Emite (suma, conteo) desde el combiner y calcula suma/conteo en el reducer.

<!-- takeaways -->

- El shuffle domina el costo de MapReduce.
- Los combiners achican la salida de map cuando la función es asociativa.
- Partitioners y cantidad de reducers controlan el paralelismo.

<!-- unit: Correr bien los jobs -->

<!-- goals -->

- Usar counters, el distributed cache y la ejecución especulativa.
- Cruzar datasets y dimensionar bien las tareas.

<!-- concept -->

Unas pocas herramientas hacen los jobs observables y eficientes. Los counters reportan qué pasó, como registros malformados o bytes derramados a disco. El distributed cache envía archivos de búsqueda pequeños a cada tarea, lo que permite joins del lado map con tablas pequeñas; los datasets grandes necesitan joins del lado reduce.
La ejecución especulativa combate los nodos lentos corriendo duplicados de las tareas rezagadas. El tamaño de las tareas también importa: las que terminan en segundos pasan casi todo su tiempo arrancando.

<!-- example -->

```java
context.getCounter("quality", "MALFORMED_RECORDS").increment(1);
job.addCacheFile(new URI("/ref/country_codes.csv#countries"));  // map-side join lookup
```

#### ¿Cómo eliges entre Avro y Parquet?

Avro para escrituras por filas, streaming y mensajes donde se leen registros completos y los esquemas evolucionan seguido; Parquet para analítica donde las consultas leen pocas columnas de muchas filas.

#### ¿Qué es Apache Hive?

Un sistema de data warehouse sobre Hadoop que permite consultar datos en HDFS (y en almacenamiento de objetos) con un dialecto SQL (HiveQL). Las consultas se compilan en jobs de MapReduce, Tez o Spark, y los metadatos de las tablas se guardan en el Hive Metastore.

#### ¿Qué es el Hive Metastore?

Un servicio respaldado por una base relacional (MySQL, PostgreSQL) que guarda las definiciones de las tablas, columnas, particiones, ubicaciones y formatos. Lo usan Hive, Spark, Impala, Presto/Trino y otros, y el AWS Glue Data Catalog es compatible con él.

#### ¿Qué diferencia hay entre tablas administradas y externas en Hive?

Hive es dueño de los datos de las tablas administradas: borrar la tabla borra los archivos. Las tablas externas apuntan a datos administrados en otro lugar: borrarlas solo elimina los metadatos. Las tablas externas son comunes en los data lakes compartidos.

#### ¿Qué son las particiones en Hive?

Subdirectorios por valores de columna (`/sales/dt=2026-10-15/`); las consultas que filtran por las columnas de partición solo leen los directorios que coinciden. El particionado dinámico crea particiones a partir de los resultados de una consulta.

<!-- challenge -->

Un job cruza 2 TB de transacciones con una tabla de países de 20 MB usando un join del lado reduce, y el shuffle es enorme. ¿Qué cambias?

<!-- solution -->

Usa un join del lado map: envía la tabla de países por el distributed cache, cárgala en memoria en cada mapper y cruza ahí, así los 2 TB nunca pasan por el shuffle.

<!-- takeaways -->

- Los counters hacen observables los jobs.
- Las tablas pequeñas se cruzan del lado map vía el cache.
- La ejecución especulativa y el tamaño de tareas combaten la lentitud.

### Hive

<!-- unit: Spark sobre YARN -->

<!-- goals -->

- Correr Spark sobre YARN con datos de HDFS y el Hive Metastore.
- Elegir entre los modos de despliegue client y cluster.

<!-- concept -->

Spark corre en los clústeres Hadoop como una aplicación YARN más: los executors son contenedores, los datos vienen de HDFS a través de la API de sistema de archivos de Hadoop y las definiciones de tablas vienen del Hive Metastore. Esa reutilización explica por qué Spark se apropió tan fácil de los clústeres Hadoop.
Dónde corre el driver es la decisión principal. En modo client corre en la máquina que envía el job, cómodo para trabajo interactivo; en modo cluster corre dentro de YARN, que es lo que necesitan los jobs de producción.

<!-- example -->

```bash
spark-submit \
  --master yarn --deploy-mode cluster --queue etl \
  --num-executors 20 --executor-cores 4 --executor-memory 12g \
  --conf spark.executor.memoryOverhead=2g \
  daily_orders.py --date 2026-10-17
```

#### ¿Qué es el bucketing en Hive?

Dividir los datos de una tabla o partición en un número fijo de archivos según el hash de una columna, lo que permite muestreos eficientes y bucket map joins cuando las tablas están agrupadas por la clave del join.

#### ¿Qué motores de ejecución puede usar Hive?

MapReduce (histórico, obsoleto), Apache Tez (basado en DAG, el predeterminado habitual en Hive 2/3) y Spark (Hive on Spark). Hive LLAP añade demonios de larga duración con caché para las consultas interactivas.

#### ¿Qué son las tablas ACID de Hive?

Tablas ORC transaccionales (las tablas administradas de Hive 3) que admiten `INSERT`, `UPDATE`, `DELETE` y `MERGE` con aislamiento por snapshots, usando archivos delta que se fusionan con compactaciones (menores y mayores).

#### ¿Qué es el optimizador basado en costos de Hive?

Una optimización basada en Apache Calcite que usa estadísticas de tablas y columnas (`ANALYZE TABLE … COMPUTE STATISTICS`) para elegir el orden y la estrategia de los joins; sin estadísticas, los planes pueden ser malos.

<!-- challenge -->

Un job nocturno de Spark enviado desde un edge node falla cada vez que alguien reinicia ese edge node. ¿Por qué y qué cambias?

<!-- solution -->

Corre en modo client, así que el driver vive en el edge node y muere con él. Envíalo en modo cluster para que el driver corra en un contenedor de YARN, independiente de la máquina cliente.

<!-- takeaways -->

- Spark sobre YARN reutiliza HDFS y el Hive Metastore.
- Modo client para trabajo interactivo; cluster para producción.
- Los executors son contenedores de YARN.

<!-- unit: Dimensionar Spark sobre YARN -->

<!-- goals -->

- Dimensionar executors y usar dynamic allocation con el external shuffle service.
- Arreglar contenedores que matan por pasarse de memoria.

<!-- concept -->

Dimensionar executors equilibra paralelismo y memoria. Unos cuatro o cinco cores por executor mantienen bueno el throughput de HDFS; la memoria debe cubrir el heap más el overhead de workers de Python, buffers y datos fuera del heap, o YARN mata el contenedor.
Dynamic allocation deja que los jobs crezcan y achiquen sus executors según la carga, lo que solo funciona si los archivos de shuffle sobreviven a la eliminación de executors, tarea del external shuffle service en cada NodeManager.

<!-- example -->

```properties
spark.dynamicAllocation.enabled=true
spark.shuffle.service.enabled=true
spark.dynamicAllocation.minExecutors=2
spark.dynamicAllocation.maxExecutors=60
spark.executor.memoryOverhead=3g      # PySpark UDFs need off-heap room
```

#### ¿Qué es un map join en Hive?

Un join en el que la tabla pequeña se carga en memoria en cada mapper (broadcast), evitando el shuffle; Hive convierte los joins automáticamente cuando la tabla pequeña está por debajo de un umbral de tamaño (`hive.auto.convert.join`).

#### ¿Cómo se cargan datos en tablas de Hive?

Con `LOAD DATA INPATH` (mueve archivos a la ubicación de la tabla), `INSERT INTO/OVERWRITE … SELECT`, `CREATE TABLE AS SELECT`, o escribiendo archivos directamente en la ubicación de una tabla externa y añadiendo las particiones.

#### ¿Qué es `MSCK REPAIR TABLE`?

Un comando que recorre la ubicación de la tabla buscando directorios de partición no registrados en el metastore y los añade.

#### ¿Qué son los SerDe en Hive?

Serializadores/deserializadores que definen cómo se leen y escriben las filas en los archivos: `LazySimpleSerDe` para texto delimitado, `OpenCSVSerde`, SerDe JSON, `RegexSerDe`, y soporte integrado para ORC, Parquet y Avro.

<!-- challenge -->

Un job de PySpark con UDFs de Python sigue perdiendo executors con "killed by YARN for exceeding memory limits", aunque el heap de la JVM se ve bien. ¿Qué cambias?

<!-- solution -->

Sube `spark.executor.memoryOverhead` (los workers de Python corren fuera del heap) o baja los cores por executor para que menos workers de Python lo compartan; reemplaza las UDFs por funciones incorporadas donde se pueda.

<!-- takeaways -->

- ~4–5 cores por executor; dimensiona heap más overhead.
- Dynamic allocation necesita el external shuffle service.
- El uso fuera del heap causa la mayoría de kills de memoria en YARN.

<!-- stage: El ecosistema -->

### HBase

<!-- unit: Hive y su metastore -->

<!-- goals -->

- Explicar qué es Hive, su metastore y sus motores de ejecución.
- Conectarse con HiveServer2 y Beeline, y saber en qué difiere HiveQL de SQL.

<!-- concept -->

Hive hizo usable Hadoop para cualquiera que supiera SQL. Las consultas se traducen en jobs sobre un motor de ejecución, antes MapReduce, hoy Tez o Spark, y corren sobre archivos en HDFS. El metastore guarda lo que convierte archivos en tablas: esquemas, ubicaciones, particiones y formatos.
Ese metastore sobrevivió al propio motor de Hive: Spark, Trino e Impala lo usan. Los clientes se conectan por HiveServer2, normalmente con Beeline o herramientas JDBC.

<!-- example -->

```bash
beeline -u "jdbc:hive2://hs2.prod:10000/default;principal=hive/_HOST@CORP.COM" \
  -e "SELECT dt, count(*) FROM sales.orders WHERE dt >= '2026-10-01' GROUP BY dt"
```

#### ¿En qué se diferencian HiveQL y el SQL estándar?

HiveQL es casi SQL, pero con funciones propias de Hadoop (particiones, buckets, `LATERAL VIEW explode`, SerDe, `INSERT OVERWRITE DIRECTORY`), con transacciones y subconsultas históricamente limitadas y semántica de esquema al leer.

#### ¿Qué es HiveServer2?

El servicio que acepta las conexiones de los clientes (JDBC/ODBC, Beeline) y ejecuta consultas HiveQL con autenticación, concurrencia y seguridad, reemplazando a la antigua CLI de Hive para el acceso multiusuario.

#### ¿Qué es Beeline?

El cliente JDBC de línea de comandos para HiveServer2, usado para ejecutar consultas y scripts en Hive con la autenticación adecuada.

#### ¿Qué es `LATERAL VIEW explode`?

Una construcción de Hive para convertir columnas de tipo arreglo o mapa en varias filas, parecida a `UNNEST` en otros dialectos SQL.

```sql
SELECT o.order_id, item
FROM orders o
LATERAL VIEW explode(o.items) t AS item;
```

#### ¿Qué diferencia hay entre `ORDER BY`, `SORT BY`, `DISTRIBUTE BY` y `CLUSTER BY` en Hive?

`ORDER BY` produce un orden total con un solo reducer; `SORT BY` ordena dentro de cada reducer; `DISTRIBUTE BY` controla qué reducer recibe cada clave; `CLUSTER BY` es `DISTRIBUTE BY` más `SORT BY` sobre las mismas columnas.

#### ¿Qué es la vectorización de Hive?

Procesar lotes de filas (normalmente 1.024) a la vez con operaciones columnares en lugar de fila por fila, lo que acelera las lecturas, los filtros y las agregaciones sobre datos ORC.

<!-- challenge -->

Un equipo quiere que Spark y Trino vean las mismas tablas que Hive. ¿Qué comparten?

<!-- solution -->

El Hive Metastore: configura Spark (`enableHiveSupport` / ajustes de catálogo) y el conector Hive de Trino para usar el mismo metastore, así todos los motores ven las mismas definiciones de tablas y particiones.

<!-- takeaways -->

- Hive traduce SQL en jobs distribuidos.
- El metastore convierte archivos en tablas para muchos motores.
- HiveServer2 y Beeline son los puntos de entrada de los clientes.

<!-- unit: Tablas, particiones y buckets -->

<!-- goals -->

- Distinguir tablas managed y external.
- Usar bien particiones, buckets e inserts con particiones dinámicas.

<!-- concept -->

Las tablas de Hive son directorios, y su organización define el rendimiento. Las tablas managed pertenecen a Hive, así que borrarlas borra los datos; las external solo apuntan a datos de otros. Las particiones son subdirectorios por valor de columna, que permiten a las consultas saltarse todo salvo las carpetas relevantes, siempre que los filtros apliquen directamente sobre la columna de partición.
Los buckets dividen los datos dentro de las particiones en un número fijo de archivos por hash, lo que ayuda a joins y muestreo. Los inserts con particiones dinámicas las crean desde los datos y necesitan límites.

<!-- example -->

```sql
SET hive.exec.dynamic.partition.mode=nonstrict;
INSERT OVERWRITE TABLE sales.orders PARTITION (dt)
SELECT order_id, customer_id, amount, to_date(created_at) AS dt
FROM staging.orders_raw
WHERE created_at >= '2026-10-15';
```

#### ¿Cómo se calculan estadísticas en Hive?

Con `ANALYZE TABLE t PARTITION (dt) COMPUTE STATISTICS` para las estadísticas de tabla y partición, y `… FOR COLUMNS` para las de columnas, que usa el optimizador basado en costos; `hive.stats.autogather` recoge las estadísticas básicas al insertar.

#### ¿Qué es la inserción con particiones dinámicas y qué hay que vigilar?

`INSERT OVERWRITE TABLE t PARTITION (dt) SELECT …, dt FROM src` crea particiones a partir de los valores de los datos. Existen límites (`hive.exec.max.dynamic.partitions`) para evitar crear miles de particiones por accidente, y muchas particiones con pocas filas generan archivos pequeños.

#### ¿Qué es HBase?

Una base de datos NoSQL distribuida por familias de columnas, inspirada en Google Bigtable, que corre sobre HDFS. Ofrece acceso aleatorio de lectura y escritura en tiempo real a miles de millones de filas por clave de fila, con consistencia fuerte por fila.

#### ¿Cuál es el modelo de datos de HBase?

Tablas de filas ordenadas por clave de fila; cada fila tiene familias de columnas (definidas al crear la tabla), cada familia tiene cualquier número de columnas (qualifiers), y cada celda guarda versiones identificadas por marcas de tiempo. Las columnas dispersas no cuestan nada.

#### ¿Cuáles son los componentes principales de HBase?

El HMaster (asigna regiones, maneja los cambios de esquema y el balanceo de carga), los RegionServers (atienden las lecturas y escrituras de las regiones), las regiones (rangos contiguos de claves de fila de una tabla) y ZooKeeper (coordinación y localización de la tabla meta).

#### ¿Cómo funciona una escritura en HBase?

El RegionServer añade la edición al write-ahead log (WAL) en HDFS para la durabilidad, y luego la escribe en la MemStore en memoria. Cuando la MemStore se llena, se vuelca a un HFile inmutable en HDFS.

<!-- challenge -->

Alguien borra una tabla managed de Hive creyendo que solo quita la definición. ¿Qué pasó con los datos y cómo deberían definirse los datos compartidos?

<!-- solution -->

Los archivos de datos se borraron con la tabla (salvo que los salve la papelera o un snapshot). Los datos compartidos con otras herramientas o equipos deben estar en tablas external, para que borrar la definición deje los archivos intactos.

<!-- takeaways -->

- Las tablas managed son dueñas de los datos; las external apuntan a ellos.
- Las particiones podan solo cuando el filtro aplica directo sobre la columna.
- Limita las particiones dinámicas para evitar explosiones.

<!-- unit: Cargar y leer datos -->

<!-- goals -->

- Cargar datos en tablas Hive y leer formatos con SerDes.
- Usar LATERAL VIEW explode y las cláusulas de ordenamiento de Hive.

<!-- concept -->

Los datos entran a Hive de pocas formas: moviendo archivos al directorio de una tabla, insertando resultados de consultas o definiendo una tabla external sobre archivos que ya existen. Los SerDes deciden cómo los bytes se vuelven columnas, de texto delimitado a JSON u ORC.
HiveQL también tiene vocabulario propio para datos distribuidos: explotar arrays en filas y cuatro cláusulas de orden que difieren en si el orden es global, por reducer o solo sobre qué reducer recibe qué filas.

<!-- example -->

```sql
SELECT o.order_id, item.sku, item.qty
FROM sales.orders o
LATERAL VIEW explode(o.items) t AS item
WHERE o.dt = '2026-10-17'
DISTRIBUTE BY o.order_id SORT BY o.order_id;
```

#### ¿Qué son las compactaciones en HBase?

Procesos en segundo plano que fusionan HFiles: las compactaciones menores fusionan unos pocos archivos pequeños; las mayores reescriben todos los archivos de un store en uno, eliminando las celdas borradas y vencidas. Las mayores usan mucha E/S y suelen programarse fuera de las horas pico.

#### ¿Por qué es tan importante el diseño de la clave de fila en HBase?

Todo acceso es por clave de fila, y las filas se ordenan y dividen en regiones por clave. Las claves que siempre crecen (marcas de tiempo, secuencias) envían todas las escrituras a una región (hotspotting). Usa salting, hashing o inversión de campos, y diseña las claves según los patrones de acceso principales.

#### ¿Cuándo elegirías HBase en lugar de Hive?

HBase para lecturas y escrituras aleatorias de baja latencia por clave (perfiles de usuario, búsquedas en series de tiempo, contadores); Hive para analítica SQL batch sobre lecturas grandes.

#### ¿Qué es Apache Phoenix?

Una capa SQL sobre HBase que compila SQL en scans de HBase, con índices secundarios y acceso JDBC.

<!-- challenge -->

Una consulta con `ORDER BY` sobre mil millones de filas corre horas en un solo reducer. La salida solo necesita estar ordenada dentro de cada cliente. ¿Qué usas?

<!-- solution -->

`DISTRIBUTE BY customer_id SORT BY customer_id, event_time`: las filas de cada cliente van al mismo reducer y se ordenan ahí, en paralelo, sin un ordenamiento global en un solo reducer.

<!-- takeaways -->

- Carga moviendo archivos, insertando resultados o con tablas external.
- Los SerDes mapean el contenido de los archivos a columnas.
- `ORDER BY` es global; `SORT BY` y `DISTRIBUTE BY` escalan.

<!-- unit: Rendimiento y ACID en Hive -->

<!-- goals -->

- Acelerar Hive con estadísticas, el CBO, map joins y vectorización.
- Explicar las tablas ACID de Hive.

<!-- concept -->

El optimizador de Hive necesita conocer tamaños de tablas y distribuciones de valores para planear bien los joins, así que las estadísticas son la base del rendimiento. Con ellas, las tablas pequeñas se vuelven map joins difundidos a cada tarea, evitando shuffles. La vectorización procesa filas por lotes y usa la CPU con mucha más eficiencia.
Las tablas ACID agregaron updates y deletes a Hive mediante archivos delta y compactación, el primer paso hacia lo que formatos de tabla como Iceberg ofrecen hoy en todas partes.

<!-- example -->

```sql
ANALYZE TABLE sales.orders PARTITION (dt) COMPUTE STATISTICS;
ANALYZE TABLE sales.orders PARTITION (dt) COMPUTE STATISTICS FOR COLUMNS;
SET hive.cbo.enable=true;
SET hive.auto.convert.join=true;
SET hive.vectorized.execution.enabled=true;
```

#### ¿Qué es la división de una región (region split)?

Cuando una región supera un tamaño configurado, el RegionServer la divide en dos regiones por una clave de fila intermedia, y el HMaster puede moverlas para balancear la carga. Predividir las tablas evita los hotspots iniciales.

#### ¿Qué es una familia de columnas y por qué conviene tener pocas?

Un grupo de columnas guardadas juntas en los mismos archivos con ajustes compartidos (compresión, versiones, TTL). Cada familia tiene su propia MemStore y sus archivos, así que muchas familias multiplican los volcados y las compactaciones; lo típico son dos o tres.

#### ¿Cómo se lee de HBase de forma eficiente?

Usando `Get` para filas sueltas por clave y `Scan` con claves de inicio y fin para los rangos, añadiendo filtros para reducir los datos devueltos, configurando caching y batching en los scans y evitando los scans completos en las rutas sensibles a la latencia.

#### ¿Qué es un filtro bloom en HBase?

Una estructura por archivo de store que indica si una fila (o fila y columna) podría existir en el archivo, permitiendo que las lecturas salten los archivos que seguro no la contienen, lo que reduce las lecturas de disco en los gets aleatorios.

#### ¿Qué es un TTL en HBase?

Un tiempo de vida definido por familia de columnas; las celdas más viejas que el TTL se eliminan durante las compactaciones, útil para series de tiempo y cachés.

<!-- challenge -->

Un join entre un hecho grande y una dimensión de 50 MB hace shuffle de ambos lados. Nunca se calcularon estadísticas. ¿Qué haces?

<!-- solution -->

Calcula estadísticas de tablas y columnas para que el optimizador sepa que la dimensión es pequeña, y activa la conversión automática a map join; la dimensión se difunde y el hecho no pasa por el shuffle.

<!-- takeaways -->

- Las estadísticas alimentan el optimizador basado en costos.
- Los map joins difunden las tablas pequeñas.
- Las tablas ACID agregan updates y deletes con deltas.

### Otras herramientas del ecosistema

<!-- unit: El modelo de datos de HBase -->

<!-- goals -->

- Describir el modelo de datos de HBase y las column families.
- Elegir entre HBase y Hive, y conocer Apache Phoenix.

<!-- concept -->

HBase responde otra pregunta que Hive: no "escanea todo" sino "dame esta fila ya". Sus tablas son mapas ordenados de row key a column families a celdas versionadas, hechos para lecturas y escrituras rápidas por clave a escala enorme.
Las column families se guardan por separado, así que deben ser pocas y agrupar datos que se leen juntos. Phoenix agrega SQL encima para equipos que quieren consultas e índices secundarios sin la API cruda.

<!-- example -->

```text
row key: user#00042
  cf "profile": name="Ana", city="Bogotá"
  cf "activity": last_login@t3="2026-10-17T09:01", last_login@t2="2026-10-16T21:40"
```

#### ¿Qué es ZooKeeper?

Un servicio de coordinación centralizado que ofrece un almacén clave-valor jerárquico (znodes), watches y consenso (protocolo ZAB). Los componentes de Hadoop lo usan para elegir líder (HA del NameNode y del ResourceManager), configuración y descubrimiento de servicios; las versiones antiguas de Kafka también lo usaban.

#### ¿Qué era Apache Pig?

Un lenguaje de flujo de datos de alto nivel (Pig Latin) que compilaba scripts a jobs de MapReduce o Tez, popular para ETL antes de que Spark y Hive maduraran; casi no se usa para trabajo nuevo.

#### ¿Qué era Apache Sqoop?

Una herramienta para transferir datos entre bases relacionales y Hadoop (importar a HDFS/Hive y exportar de vuelta) con tareas MapReduce en paralelo. Se retiró al Apache Attic en 2021; la reemplazaron Spark JDBC, herramientas tipo DMS y herramientas de CDC.

#### ¿Qué es Apache Flume?

Un servicio para recolectar, agregar y mover grandes cantidades de logs desde muchos orígenes hacia HDFS o HBase, con sources, channels y sinks. Kafka lo ha reemplazado en gran medida.

#### ¿Qué es Apache Oozie?

Un programador de flujos de trabajo para jobs de Hadoop (MapReduce, Hive, Pig, Sqoop, shell) definidos en XML, con coordinadores para disparadores por tiempo y por datos. La mayoría de los equipos se ha pasado a Airflow u otros orquestadores.

<!-- challenge -->

Una app necesita el perfil más reciente de cualquiera de 500 millones de usuarios en menos de 10 ms, mientras los analistas necesitan agregados semanales. ¿Qué almacén sirve cada necesidad?

<!-- solution -->

HBase (row key = ID de usuario) para búsquedas de baja latencia por clave; Hive (o Spark sobre Parquet) para los agregados semanales, alimentados desde los mismos datos.

<!-- takeaways -->

- HBase es un almacén ordenado por clave con celdas versionadas.
- Mantén pocas column families.
- HBase para acceso por clave; Hive para escaneos.

<!-- unit: Internos de HBase -->

<!-- goals -->

- Describir los componentes de HBase y su camino de escritura.
- Explicar compactaciones, división de regiones, bloom filters y TTLs.

<!-- concept -->

HBase escribe rápido porque nunca reescribe archivos en sitio. Una escritura va a un log por durabilidad y a memoria; la memoria se vuelca en archivos inmutables. Con el tiempo esos archivos se acumulan, así que las compactaciones los fusionan y descartan los datos borrados o vencidos.
Las tablas se dividen en regiones por rango de claves, servidas por RegionServers y divididas de nuevo al crecer. Los bloom filters permiten a las lecturas saltarse archivos que no pueden contener una fila, y los TTLs vencen las celdas viejas automáticamente.

<!-- example -->

```text
put(row) → WAL on HDFS → MemStore (memory) → flush → HFile
minor compaction: merge a few HFiles
major compaction: rewrite all HFiles of a store, drop deletes and expired cells
```

#### ¿Qué son Impala y Presto/Trino?

Motores SQL MPP que consultan directamente datos en HDFS y en almacenamiento de objetos con demonios de larga duración, con latencia interactiva frente a Hive sobre MapReduce. Trino (antes PrestoSQL) se usa mucho y es la base de Amazon Athena.

#### ¿Cómo corre Spark en un cluster Hadoop?

Spark corre sobre YARN (driver en modo cliente o cluster, executors en contenedores de YARN), lee y escribe en HDFS, usa el Hive Metastore para las tablas y aprovecha la localidad de los datos.

#### ¿Qué papel cumple Kafka en las arquitecturas Hadoop?

Un log de mensajes durable y escalable que ingiere flujos (eventos, CDC) y desacopla productores de consumidores; luego los datos se escriben en HDFS o en almacenamiento de objetos con Kafka Connect, Spark Streaming o Flink.

#### ¿Qué es Apache Tez?

Un framework de ejecución por DAG sobre YARN que ejecuta los jobs de Hive y Pig como un solo grafo de tareas, evitando las escrituras a disco por etapa y los costos de arranque de MapReduce.

#### ¿Qué es Apache Ambari?

Una herramienta web para aprovisionar, administrar y monitorear clusters Hadoop (instalar servicios, configuración, alertas), usada sobre todo con las distribuciones de Hortonworks; Cloudera Manager cumple el mismo papel en Cloudera.

#### ¿Qué es Apache Livy?

Un servicio REST para enviar jobs y sesiones interactivas de Spark a un cluster, usado por notebooks y aplicaciones que no pueden ejecutar un driver de Spark por sí mismas.

<!-- challenge -->

La latencia de lectura se dispara cada domingo a las 02:00 en un clúster HBase. ¿Cuál es una causa probable y su solución?

<!-- solution -->

Las major compactions programadas reescriben todos los store files y compiten con las lecturas. Desactiva las major compactions por tiempo y córrelas a mano o con límite de velocidad en ventanas tranquilas, por tabla.

<!-- takeaways -->

- Las escrituras van al WAL y al MemStore, luego a HFiles.
- Las compactaciones fusionan archivos y descartan datos viejos.
- Las regiones se dividen por rango de claves al crecer.

<!-- unit: Diseñar para el acceso -->

<!-- goals -->

- Diseñar row keys que eviten hotspots.
- Leer HBase con eficiencia con gets, scans y filtros.

<!-- concept -->

En HBase, la row key es a la vez el índice, el particionamiento y el orden. Una clave que crece con el tiempo, como un timestamp, manda todas las escrituras a la última región: un hotspot. Agregar sal, hashear o invertir las claves reparte las escrituras, a costa de rangos de escaneo más difíciles.
Las lecturas siguen la misma lógica: trae filas individuales por clave, escanea rangos con claves de inicio y fin, y limita columnas y versiones a lo necesario.

<!-- example -->

```text
bad:  20261017T090112#sensor42      → all writes hit the newest region
good: 7#sensor42#20261017T090112    → salt (hash(sensor) % 16) spreads writes
scan: start=7#sensor42#20261017  stop=7#sensor42#20261018
```

#### ¿Qué es Apache Ozone?

Un almacén de objetos distribuido y escalable para Hadoop con una API compatible con S3, diseñado para superar los límites de HDFS con los archivos pequeños y el espacio de nombres, manteniéndose compatible con las aplicaciones Hadoop.

#### ¿Cómo se hace la autenticación en Hadoop?

Con Kerberos: usuarios y servicios obtienen tickets de un Key Distribution Center y los servicios de Hadoop los verifican. Sin Kerberos (modo "simple"), Hadoop confía en el nombre de usuario que declara el cliente, lo que es inseguro.

<!-- challenge -->

Una tabla IoT con clave por timestamp maneja las escrituras en un solo RegionServer mientras los demás están ociosos. Rediseña la clave.

<!-- solution -->

Ponle a la clave un prefijo de sal o el ID del dispositivo (por ejemplo `hash(device) % N # device # timestamp`), para que las escrituras se repartan entre regiones y los escaneos de un dispositivo sigan siendo por rango.

<!-- takeaways -->

- La row key decide la distribución y el acceso.
- Las claves monótonas crean hotspots de escritura.
- Usa gets y scans acotados con filtros.

### Seguridad y gobierno

<!-- unit: Coordinación y orquestación -->

<!-- goals -->

- Explicar el papel de ZooKeeper en la coordinación de servicios de Hadoop.
- Describir Oozie, Ambari y Livy.

<!-- concept -->

Los servicios distribuidos necesitan ponerse de acuerdo: quién es el master activo, qué nodos están vivos, cuál es la configuración actual. ZooKeeper da ese estado compartido pequeño y confiable, y muchos componentes de Hadoop dependen de él para el failover.
Alrededor del clúster, otras herramientas manejan el trabajo y la operación: Oozie programa workflows de jobs de Hadoop, Ambari instala y monitorea servicios, y Livy permite a las aplicaciones enviar jobs de Spark por REST.

<!-- example -->

```text
ZooKeeper ensemble (3 or 5 nodes)
 ├─ NameNode HA: ZKFC elects the active NameNode
 ├─ ResourceManager HA leader election
 └─ HBase: active HMaster, RegionServer membership
```

#### ¿Qué son los delegation tokens?

Tokens emitidos por los servicios (NameNode, ResourceManager) tras la autenticación Kerberos, que se pasan a las tareas del cluster para que accedan a HDFS sin tener credenciales Kerberos propias.

#### ¿Cómo se administran los permisos de HDFS?

Con permisos tipo POSIX de propietario/grupo/otros sobre archivos y directorios, más ACL para un control más fino. Las políticas detalladas y centralizadas suelen administrarse con Apache Ranger.

#### ¿Qué es Apache Ranger?

Un framework de seguridad centralizado para Hadoop que define y audita políticas de acceso (rutas de HDFS, bases, tablas y columnas de Hive, filtros de filas y enmascaramiento, HBase, Kafka) con plugins que las aplican en cada servicio.

#### ¿Qué es Apache Atlas?

Un servicio de metadatos y gobierno que ofrece catálogo de datos, linaje, clasificación (etiquetas como PII) e integración con Ranger para políticas basadas en etiquetas.

<!-- challenge -->

¿Por qué un ensemble de ZooKeeper tiene tres o cinco nodos, nunca dos o cuatro?

<!-- solution -->

Necesita una mayoría (quórum) para operar. Tres nodos toleran una falla y cinco toleran dos; cuatro tolera solo una, igual que tres, y dos no tolera ninguna, así que los números pares suman costo sin resiliencia.

<!-- takeaways -->

- ZooKeeper da coordinación y elección de líder.
- Oozie programa workflows de Hadoop.
- Ambari gestiona clústeres; Livy envía Spark por REST.

<!-- unit: Herramientas de ingesta -->

<!-- goals -->

- Describir el papel de Sqoop, Flume y Kafka en las arquitecturas Hadoop.
- Elegir un camino de ingesta para bases de datos, logs y eventos.

<!-- concept -->

Los datos llegaban a Hadoop con herramientas especializadas. Sqoop movía tablas entre bases relacionales y HDFS con jobs paralelos. Flume recogía líneas de log de muchos servidores y las entregaba por lotes. Kafka se volvió el buffer durable entre productores y todo lo que viene después.
Sqoop y Flume están retirados o casi no se eligen hoy, reemplazados por Spark JDBC, herramientas de CDC y conectores de Kafka, pero sus patrones siguen.

<!-- example -->

| Fuente | Herramienta clásica | Equivalente moderno |
|---|---|---|
| Tablas de bases relacionales | Sqoop | Spark JDBC, CDC (Debezium) |
| Archivos de log de servidores | Flume | Kafka + conectores, Fluent Bit |
| Streams de eventos | Kafka | Kafka |

#### ¿Qué es Apache Knox?

Un gateway que ofrece un único punto de entrada seguro (APIs REST, interfaces) a los servicios de Hadoop para usuarios fuera del cluster, encargándose de la autenticación y SSL.

#### ¿Cómo se cifran los datos en Hadoop?

En tránsito con cifrado de RPC, TLS en las interfaces web y cifrado de la transferencia de datos; en reposo con el cifrado transparente de HDFS mediante zonas de cifrado cuyas claves administra el Hadoop Key Management Server (KMS).

#### ¿Qué es un keytab?

Un archivo con las claves de un principal de Kerberos, usado por servicios y jobs batch para autenticarse sin contraseña; los keytabs se deben proteger como contraseñas.

<!-- challenge -->

Un clúster sigue importando una base cada noche con Sqoop, que ya no tiene mantenimiento. ¿Con qué lo reemplazas?

<!-- solution -->

Un job de Spark JDBC que lea en paralelo por rangos de claves (o una herramienta de CDC para cambios incrementales), escribiendo particiones Parquet u ORC, programado por el orquestador existente.

<!-- takeaways -->

- Sqoop movía bases de datos; Flume movía logs.
- Kafka desacopla productores y consumidores.
- Los stacks modernos usan Spark JDBC, CDC y conectores.

<!-- unit: Motores de procesamiento y consulta -->

<!-- goals -->

- Comparar Pig, Tez, Impala y Trino con Spark.
- Describir cómo encajan Spark y Ozone en los clústeres Hadoop.

<!-- concept -->

Los motores sobre Hadoop evolucionaron para recortar la sobrecarga de MapReduce. Pig ofrecía un lenguaje de scripts que compilaba a jobs. Tez corría una consulta completa como un grafo en vez de jobs encadenados. Impala y Trino usaban daemons de larga vida para SQL interactivo sin arranque de jobs. Spark generalizó todo con procesamiento en memoria.
El almacenamiento también evolucionó: Ozone lleva a los clústeres Hadoop un almacén de objetos con API S3, aliviando los límites de archivos pequeños y del NameNode.

<!-- example -->

| Motor | Estilo | Uso típico |
|---|---|---|
| Pig (retirado) | Scripts de flujo de datos | ETL heredado |
| Hive sobre Tez | SQL como DAG | SQL batch |
| Impala / Trino | Daemons MPP | SQL interactivo |
| Spark | DAG, en memoria | ETL, ML, SQL |

#### ¿Qué es la suplantación (proxy users) en Hadoop?

Una configuración que permite a un servicio de confianza (HiveServer2, Livy, Oozie) actuar en nombre de los usuarios finales, para que los permisos y las auditorías reflejen al usuario real y no a la cuenta de servicio.

#### ¿Cómo se audita el acceso en Hadoop?

Los logs de auditoría de HDFS en el NameNode registran cada acceso a archivos; Ranger recoge los eventos de auditoría de todos sus plugins en Solr o HDFS, y Atlas registra el linaje.

#### ¿Cómo se dimensiona un cluster Hadoop?

A partir del volumen de datos (tamaño en bruto × factor de replicación × crecimiento, más espacio temporal), las necesidades de procesamiento (CPU y memoria para los jobs concurrentes) y los objetivos de rendimiento; dejando margen para fallos y rebalanceo (a menudo se mantienen los discos por debajo del 70–80 %).

#### ¿Cuáles son las causas comunes de jobs lentos en Hadoop?

Data skew (unos pocos reducers con la mayoría de las claves), demasiados archivos pequeños, paralelismo insuficiente o excesivo, derrames a disco por buffers de memoria pequeños, entradas comprimidas no divisibles, falta de localidad de datos y contención en las colas de YARN.

#### ¿Cómo se ajusta la memoria de MapReduce?

Definiendo `mapreduce.map.memory.mb` y `mapreduce.reduce.memory.mb` para el tamaño de los contenedores y `-Xmx` en `mapreduce.map.java.opts` en torno al 80 % del contenedor, y ajustando `mapreduce.task.io.sort.mb` para reducir los derrames.

<!-- challenge -->

Los analistas se quejan de que cada consulta de Hive tarda 30 segundos en arrancar, aun las simples. ¿Qué les ofreces?

<!-- solution -->

Un motor interactivo con daemons de larga vida (Impala o Trino) sobre el mismo metastore y archivos, para consultas ad hoc; deja Hive sobre Tez o Spark para los jobs batch pesados.

<!-- takeaways -->

- Tez corre las consultas como un solo DAG.
- Impala y Trino sirven SQL interactivo.
- Ozone agrega almacenamiento de objetos tipo S3 a Hadoop.

<!-- stage: Operar Hadoop -->

### Operación y rendimiento

<!-- unit: Autenticación con Kerberos -->

<!-- goals -->

- Explicar la autenticación con Kerberos, los keytabs y los delegation tokens.
- Configurar la suplantación para servicios confiables.

<!-- concept -->

Por defecto Hadoop confía en el nombre de usuario que diga el cliente, lo que no es seguridad en absoluto. Kerberos lo arregla: usuarios y servicios prueban su identidad con tickets de una autoridad central. Los jobs batch se autentican con archivos keytab en lugar de contraseñas.
Los jobs distribuidos agregan un giro: miles de tareas no pueden contactar cada una al servidor Kerberos, así que los servicios entregan delegation tokens tras la primera autenticación. Servicios confiables como HiveServer2 actúan en nombre de los usuarios mediante suplantación.

<!-- example -->

```bash
kinit -kt /etc/security/keytabs/etl.keytab etl@CORP.COM
klist
hdfs dfs -ls /data/finance
```

#### ¿Cómo se maneja el data skew en los jobs de Hadoop?

Con combiners, partitioners propios, salting de las claves calientes, joins del lado del map para las tablas pequeñas, las optimizaciones de skew join de Hive (`hive.optimize.skewjoin`) o preagregación.

#### ¿Cómo se monitorea un cluster Hadoop?

Con las interfaces web del NameNode y del ResourceManager, las métricas JMX, Cloudera Manager (o históricamente Ambari), exportadores de Prometheus y Grafana, y alertas sobre la capacidad de HDFS, los nodos muertos o lentos, los bloques subreplicados, el heap del NameNode, la latencia de RPC y el uso de las colas.

#### ¿Cómo se actualiza un cluster Hadoop?

Planificando con las notas de la versión y revisiones de compatibilidad, respaldando los metadatos del NameNode, usando actualizaciones progresivas (rolling) cuando se admiten (NameNodes en HA, DataNodes uno a uno), probando los jobs en un cluster de staging y conservando la posibilidad de revertir hasta finalizar.

#### ¿Cómo se respalda HDFS?

Con snapshots para los errores de los usuarios, `distcp` hacia otro cluster o almacenamiento de objetos para la recuperación ante desastres, y respaldos de los metadatos del NameNode (`fsimage` y edits). La replicación dentro del cluster no es un respaldo.

<!-- challenge -->

Un job nocturno falla tras meses funcionando bien, con "GSS initiate failed". ¿Qué revisas?

<!-- solution -->

Las credenciales de Kerberos: si el keytab sigue siendo válido (cambió la contraseña o la versión de la clave), si el ticket venció antes de renovarse y el desfase de reloj entre el nodo y el KDC.

<!-- takeaways -->

- Kerberos prueba identidades con tickets.
- Los keytabs autentican jobs batch y servicios.
- Delegation tokens y proxy users escalan la autenticación.

<!-- unit: Autorización, cifrado y auditoría -->

<!-- goals -->

- Manejar permisos con ACLs de HDFS y Ranger.
- Cifrar datos y auditar el acceso con Atlas, Knox y logs de auditoría.

<!-- concept -->

Una vez conocidas las identidades, hay que decidir el acceso. Los permisos y ACLs de HDFS funcionan por archivo y directorio; Ranger centraliza políticas para HDFS, Hive, HBase y más, incluido enmascaramiento de columnas y filtrado de filas, con auditoría de cada decisión.
Alrededor hay cifrado de datos en tránsito y en reposo, un gateway que oculta los endpoints del clúster a los usuarios y un catálogo de gobierno con linaje y clasificaciones que pueden guiar las políticas.

<!-- example -->

```text
Ranger policy "finance_read":
  resource: Hive db=finance, table=*, column=*
  allow: group finance-analysts → SELECT
  mask: column=iban → partial mask (show last 4)
Atlas tag PII on finance.customers.iban → tag-based policy applies everywhere
```

#### ¿Qué impacto tiene el garbage collection de la JVM en los servicios de Hadoop?

Las pausas largas de GC en el NameNode o los RegionServers los dejan sin responder, causando timeouts, failovers o heartbeats perdidos. Dimensiona bien los heaps, usa recolectores modernos (G1) y vigila los logs de GC.

#### ¿Cómo se encuentran los jobs que más recursos del cluster usan?

Con la interfaz y las APIs del ResourceManager de YARN (memoria-segundos y vcore-segundos por aplicación), las métricas de las colas, los history servers de Spark y MapReduce y los informes de uso de las herramientas de administración.

#### ¿Cómo se limpia un cluster que se queda sin espacio?

Buscando los directorios grandes y viejos (`hdfs dfs -du -h`), vaciando la papelera, borrando datos temporales obsoletos y snapshots viejos, reduciendo la replicación de los datos fríos o aplicando erasure coding, comprimiendo o convirtiendo a formatos columnares, y añadiendo capacidad si hace falta.

#### ¿Para qué sirve `mapreduce.job.reduce.slowstart.completedmaps`?

Define la fracción de maps que deben terminar antes de que los reducers empiecen a traer la salida; arrancar los reducers demasiado pronto desperdicia slots esperando, demasiado tarde retrasa el shuffle.

#### ¿Cómo se compara HDFS con Amazon S3?

HDFS acopla almacenamiento y cómputo en los mismos nodos, da localidad de datos y consistencia fuerte, y requiere administrar un cluster. S3 es almacenamiento de objetos administrado, escalable de forma independiente, más barato y muy durable, al que se accede por la red; hoy también tiene consistencia fuerte. La mayoría de los data lakes en la nube usan almacenamiento de objetos en lugar de HDFS.

#### ¿Qué es el conector S3A?

El conector de sistema de archivos de Hadoop (`s3a://`) que permite a Hadoop, Hive y Spark leer y escribir en S3 como si fuera un sistema de archivos, con optimizaciones para cargas multiparte, committers que evitan los renombrados lentos y proveedores de credenciales.

<!-- challenge -->

Los auditores preguntan quién leyó una tabla sensible de Hive en los últimos 90 días. ¿De dónde sale la respuesta?

<!-- solution -->

De los logs de auditoría de Ranger para la tabla de Hive (usuario, hora, acción, decisión de política), más los logs de auditoría del NameNode de HDFS para lecturas directas de archivos en su ubicación.

<!-- takeaways -->

- Ranger centraliza políticas, enmascaramiento y auditoría.
- Atlas clasifica datos y sigue el linaje.
- Cifra en tránsito y en reposo; Knox va delante del clúster.

### Hadoop y la nube

<!-- unit: Dimensionamiento y monitoreo -->

<!-- goals -->

- Dimensionar un clúster Hadoop a partir de los datos y la carga.
- Monitorear servicios, jobs y salud de la JVM.

<!-- concept -->

El dimensionamiento parte de los datos: volumen crudo por replicación por crecimiento, más espacio para datos temporales. El cómputo sale de las cargas y sus plazos. Los clústeres cortos fallan por capacidad; los sobrados desperdician dinero, y on premises el hardware tarda meses en llegar.
El monitoreo cubre ambas capas: servicios, como heap del NameNode, bloques faltantes y pausas de garbage collection, y jobs, como uso de recursos por cola y aplicación.

<!-- example -->

```text
raw data 400 TB × 3 replicas = 1.2 PB
+ 25% temporary/shuffle space    = 1.5 PB
+ 30% yearly growth, 2 years     ≈ 2.5 PB raw disk
```

#### ¿Por qué los renombrados son un problema en el almacenamiento de objetos?

Los almacenes de objetos no tienen directorios reales; un "renombrado" es una copia más un borrado de cada objeto, lo que es lento y no atómico. Los committers de salida de Hadoop que dependen de renombrar son lentos o inseguros en S3, así que se usan los committers de S3A (magic, staging) o formatos de tabla (Iceberg, Delta).

#### ¿Qué es Amazon EMR?

Una plataforma administrada de big data en AWS que ejecuta Hadoop, Spark, Hive, HBase, Presto/Trino, Flink y otros sobre EC2, EKS o serverless, usando S3 (EMRFS/S3A) como almacenamiento principal y el Glue Data Catalog como metastore, con clusters transitorios o de larga duración.

#### ¿Qué es un cluster transitorio?

Un cluster creado para un job o pipeline y terminado después, con los datos guardados en almacenamiento de objetos. Evita pagar clusters ociosos y hace reproducibles los entornos.

#### ¿Cómo migrarías un data lake Hadoop a la nube?

Inventariando los datos, los jobs y las dependencias; copiando los datos al almacenamiento de objetos con `distcp` o servicios de transferencia; convirtiendo las tablas a formatos abiertos (Parquet y luego Iceberg o Delta); pasando el metastore a un catálogo administrado (Glue, Unity Catalog); portando los jobs de Hive y MapReduce a Spark o motores SQL; reemplazando Oozie por Airflow; recreando la seguridad con el IAM de la nube y los permisos del catálogo; y validando los resultados en paralelo antes de dar de baja el cluster.

<!-- challenge -->

El NameNode deja de responder 30 segundos varias veces al día, y luego vienen failovers. ¿Qué miras?

<!-- solution -->

Los logs de garbage collection de la JVM y el uso de heap: largas pausas de full GC en un heap grande. Ajusta el collector y el tamaño del heap, reduce metadatos (menos archivos pequeños) y monitorea los tiempos de pausa de GC.

<!-- takeaways -->

- Dimensiona con datos × replicación × crecimiento.
- Monitorea servicios y jobs por separado.
- Las pausas largas de GC desestabilizan los servicios master.

<!-- unit: Jobs lentos y sesgo -->

<!-- goals -->

- Diagnosticar jobs lentos de Hadoop y ajustar la memoria de MapReduce.
- Manejar el sesgo de datos y el momento de arranque de los reducers.

<!-- concept -->

Los jobs lentos suelen venir de pocas causas: claves sesgadas que sobrecargan reducers individuales, demasiados archivos pequeños, ajustes de memoria equivocados o contención con otras cargas en las mismas colas. Comparar los tiempos de las tareas muestra cuál: una tarea larga es sesgo, miles de tareas diminutas son archivos pequeños, tareas matadas son memoria.
Cuándo arrancan los reducers también importa: arrancarlos temprano solapa trabajo, pero puede dejar contenedores ociosos mientras terminan los maps.

<!-- example -->

```properties
mapreduce.map.memory.mb=4096
mapreduce.map.java.opts=-Xmx3276m          # ~80% of the container
mapreduce.reduce.memory.mb=8192
mapreduce.reduce.java.opts=-Xmx6553m
mapreduce.job.reduce.slowstart.completedmaps=0.80
```

#### ¿Qué reemplazó a los componentes de Hadoop en los stacks modernos?

HDFS → almacenamiento de objetos (S3, ADLS, GCS); YARN → Kubernetes o cómputo serverless administrado; MapReduce → Spark, Flink, motores SQL; Hive Metastore → Glue, Unity Catalog, Polaris y otros catálogos; tablas Hive → Iceberg, Delta, Hudi; Oozie → Airflow, Dagster; Ranger/Atlas → gobierno nativo de la nube (Lake Formation, Unity Catalog).

#### ¿Qué son los formatos de tabla abiertos y qué relación tienen con las tablas Hive?

Iceberg, Delta Lake y Hudi añaden una capa de metadatos transaccional sobre archivos Parquet, resolviendo los problemas de las tablas Hive (sin ACID sobre almacenamiento de objetos, listado lento de particiones, escrituras concurrentes inseguras, evolución de esquema dolorosa). Son los sucesores modernos de las tablas al estilo Hive.

#### ¿Qué es EMRFS?

La implementación de Amazon EMR del sistema de archivos de Hadoop para S3, con funciones como la vista consistente (históricamente), el cifrado y el mapeo de roles IAM; las versiones recientes de EMR también admiten S3A.

#### ¿Se puede ejecutar Hadoop en Kubernetes?

En parte, sí: Spark y Flink corren de forma nativa en Kubernetes, el Hive Metastore y Trino corren como servicios, y el almacenamiento pasa a almacenes de objetos. Ejecutar HDFS y YARN en Kubernetes es posible pero rara vez compensa la complejidad.

#### ¿Qué son Google Dataproc y Azure HDInsight?

Servicios administrados de Hadoop y Spark en Google Cloud y Azure, parecidos a EMR, que crean clusters en minutos con almacenamiento de objetos (GCS, ADLS) como almacenamiento principal. Azure ha ido orientando a los usuarios hacia Fabric y Databricks para el trabajo nuevo.

<!-- challenge -->

199 reducers de un job terminan en 5 minutos y uno corre 2 horas. ¿Qué está pasando y cuáles son dos soluciones?

<!-- solution -->

Sesgo de datos: una clave concentra la mayoría de registros. Usa un combiner para achicarla, agrega sal a la clave caliente para repartirla entre varios reducers y fusiona después, o maneja la clave caliente aparte (por ejemplo con un join del lado map para ella).

<!-- takeaways -->

- Una tarea larga es sesgo; muchas diminutas, archivos pequeños.
- Dimensiona el heap en cerca del 80 % del contenedor.
- Slowstart equilibra reducers tempranos contra contenedores ociosos.

<!-- unit: Capacidad, backups y actualizaciones -->

<!-- goals -->

- Liberar espacio y proteger los datos de HDFS con backups.
- Planear actualizaciones seguras del clúster.

<!-- concept -->

Quedarse sin espacio es una emergencia lenta: las escrituras empiezan a fallar en todo el clúster. Las soluciones son limpiar ya (papelera, datos temporales, replicación de datos fríos) y fijar políticas después (cuotas, retención, archivado en almacenamiento más barato).
Los backups siguen la misma división de siempre: snapshots para errores de usuario, copias a otro clúster o a almacenamiento de objetos para desastres. Las actualizaciones se planean como migraciones, con backups de metadatos, rolling upgrades donde se soporten y un camino de reversión probado.

<!-- example -->

```bash
hdfs dfs -du -h / | sort -h | tail -20          # biggest directories
hdfs dfs -expunge                               # empty trash
hdfs dfs -setrep -w 2 /data/archive/2023        # less replication on cold data
hadoop distcp /data/finance s3a://dr-bucket/finance   # disaster copy
```

#### ¿En qué difieren los costos entre Hadoop on-premises y los data lakes en la nube?

Los clusters on-premises tienen costos fijos altos (hardware, centros de datos, personal) y se dimensionan para los picos; los lakes en la nube tienen almacenamiento y cómputo de pago por uso que pueden bajar a cero, pero requieren gobierno de costos para evitar un uso descontrolado.

#### ¿Cómo lee Spark datos de HDFS?

Mediante la API `FileSystem` de Hadoop y los input formats: cada bloque de HDFS (o rango de grupos de filas de Parquet) se convierte en una partición, y YARN programa los executors con preferencias de localidad cerca de los bloques.

#### ¿Cómo usa Spark el Hive Metastore?

Con `enableHiveSupport()` (o la configuración del catálogo), Spark lee del metastore las definiciones de tablas, particiones y ubicaciones, así que `spark.table("db.tabla")` y Spark SQL funcionan sobre tablas de Hive, y Spark puede crear tablas visibles para Hive.

#### ¿Cómo se envía un job de Spark a YARN?

```bash
spark-submit \
  --master yarn --deploy-mode cluster \
  --queue etl \
  --num-executors 20 --executor-cores 4 --executor-memory 8g \
  --conf spark.executor.memoryOverhead=1g \
  --conf spark.sql.shuffle.partitions=400 \
  jobs/curate_orders.py --date 2026-10-15
```

<!-- challenge -->

Un administrador borró por error un directorio de producción con `-skipTrash`. ¿Qué protecciones podrían haberlo salvado?

<!-- solution -->

Un snapshot de HDFS del directorio (restaurar desde `.snapshot`) o un backup reciente con `distcp` en otro lugar. Además, restringe el uso de `-skipTrash` y el acceso de escritura en producción a cuentas de servicio.

<!-- takeaways -->

- Limpia ya; impón cuotas y retención después.
- Snapshots para errores; copias para desastres.
- Actualiza con backups y un plan de reversión.

### Spark sobre Hadoop

<!-- unit: HDFS frente al almacenamiento de objetos -->

<!-- goals -->

- Comparar HDFS con S3 y explicar el conector S3A y EMRFS.
- Explicar por qué los renombres son un problema en el almacenamiento de objetos.

<!-- concept -->

HDFS acopla almacenamiento y cómputo: la localidad de datos es rápida, pero escalas ambos juntos y pagas capacidad ociosa. El almacenamiento de objetos los separa: prácticamente ilimitado, barato y durable, accesible por red desde cualquier número de clústeres.
Las herramientas de Hadoop llegan a él con conectores, pero los almacenes de objetos no son sistemas de archivos. Renombrar un directorio, que los jobs de Hadoop usan para hacer commit de la salida, se vuelve una copia y borrado lentos de cada objeto, así que se necesitan committers pensados para almacenamiento de objetos.

<!-- example -->

| | HDFS | S3 |
|---|---|---|
| Escalado | Almacenamiento + cómputo juntos | Independiente |
| Renombre | Cambio atómico de metadatos | Copia + borrado por objeto |
| Durabilidad | Replicación ×3 | 11 nueves, administrada |
| Modelo de costo | Hardware, siempre encendido | Por GB-mes |

#### ¿Qué es la asignación dinámica de Spark en YARN?

Una función en la que Spark pide y libera executors según las tareas pendientes, para que los executors ociosos devuelvan sus recursos a YARN; necesita el servicio de shuffle externo (o el seguimiento del shuffle) para que los archivos del shuffle sobrevivan a la eliminación de los executors.

#### ¿Qué es el servicio de shuffle externo?

Un servicio que corre en cada NodeManager y sirve los archivos de shuffle escritos por los executors, para que estos se puedan eliminar (asignación dinámica) o fallar sin perder su salida del shuffle.

#### ¿Cómo se eligen los tamaños de los executors en YARN?

Equilibrando cores y memoria: unos 4–5 cores por executor para un buen rendimiento con HDFS, memoria por core según la carga, overhead para las necesidades fuera del heap, y dejando recursos para el NodeManager y el sistema operativo en cada nodo.

#### El NameNode se queda sin memoria heap. ¿Qué haces?

A corto plazo, aumento el heap y reinicio en una ventana de mantenimiento (con HA, hago failover). A largo plazo, reduzco los objetos: encuentro y compacto los archivos pequeños, borro datos sin uso y snapshots viejos, uso archivos HAR y considero la federación o los observer NameNodes.

<!-- challenge -->

Un job de Spark que escribe en S3 pasa 20 minutos en "committing" después de que terminan las tareas. ¿Por qué y qué cambias?

<!-- solution -->

El file output committer por defecto renombra la salida temporal, lo que en S3 es copia más borrado por archivo. Usa un committer optimizado para S3 (los committers magic/directory de S3A o el committer optimizado de EMR), o escribe en un formato de tabla.

<!-- takeaways -->

- El almacenamiento de objetos separa almacenamiento y cómputo.
- S3A y EMRFS conectan las herramientas de Hadoop con S3.
- Los renombres son lentos en almacenes de objetos; usa committers especiales.

<!-- unit: Clústeres administrados y transitorios -->

<!-- goals -->

- Describir EMR, Dataproc y HDInsight y los clústeres transitorios.
- Comparar costos con Hadoop on premises y Hadoop sobre Kubernetes.

<!-- concept -->

Los servicios administrados corren por ti el ecosistema Hadoop en máquinas de nube, y cambian la forma de usar los clústeres. En lugar de un clúster de larga vida dimensionado para el pico, puedes arrancar un clúster para un job, leer y escribir en almacenamiento de objetos y apagarlo, pagando solo mientras corre.
Eso pasa los costos de hardware fijo a uso. Algunas piezas corren ahora sobre Kubernetes, sobre todo Spark, Trino y el metastore.

<!-- example -->

```bash
aws emr create-cluster --name nightly-etl --release-label emr-7.3.0 \
  --applications Name=Spark Name=Hive --instance-type m7g.2xlarge --instance-count 10 \
  --steps Type=Spark,Name=etl,Args=[s3://code/etl.py,--date,2026-10-17] \
  --auto-terminate
```

#### Una consulta de Hive sobre una tabla particionada lee toda la tabla. ¿Por qué?

El filtro no está sobre la columna de partición, la envuelve en una función, la compara con otro tipo, o las particiones no se registraron y la consulta recurre a la ubicación de la tabla. Reviso el plan con `EXPLAIN` y corrijo los filtros o las particiones.

#### Un job de Spark en YARN falla una y otra vez con contenedores matados por exceso de memoria. ¿Cómo lo corriges?

Aumento `spark.executor.memoryOverhead` (memoria fuera del heap para los workers de Python y los buffers), reduzco los cores por executor, aumento las particiones para reducir los datos por tarea, evito collects grandes y el caché, y reviso si hay skew.

#### Aparecen muchos bloques subreplicados tras la caída de un nodo. ¿Es un problema?

De forma temporal es lo esperado: el NameNode está volviendo a replicar los bloques del nodo muerto. Vigilo el avance; si persiste, reviso falta de capacidad, restricciones de racks, problemas de retiro de nodos o limitación de la red (`dfs.namenode.replication.max-streams`).

#### ¿Cómo ingerirías una extracción diaria de una base relacional en un data lake Hadoop?

Extraigo con Spark JDBC (en paralelo por rangos de clave) o una herramienta de CDC, escribo Parquet u ORC en un directorio de aterrizaje por fecha, registro las particiones en el metastore, transformo hacia tablas curadas con Hive o Spark, ejecuto controles de calidad de datos y orquesto con Airflow u Oozie.

#### ¿Cómo le explicarías Hadoop a una persona no técnica?

Es una forma de guardar y procesar cantidades enormes de datos repartiéndolos entre muchos computadores comunes que trabajan juntos, de modo que el sistema sigue funcionando aunque algunas máquinas fallen.

<!-- challenge -->

Un clúster en la nube corre 24/7 pero procesa jobs solo 4 horas cada noche. ¿Cómo bajas los costos?

<!-- solution -->

Deja los datos en almacenamiento de objetos y pasa a clústeres transitorios arrancados para los jobs nocturnos y terminados después (o autoescalado casi a cero), con instancias spot para los nodos de tareas.

<!-- takeaways -->

- Los servicios administrados corren las herramientas de Hadoop en la nube.
- Los clústeres transitorios solo cobran mientras corren los jobs.
- Los costos pasan de hardware fijo a uso.

<!-- unit: Más allá de Hadoop -->

<!-- goals -->

- Relacionar los componentes de Hadoop con sus reemplazos modernos.
- Explicar cómo los formatos de tabla abiertos mejoran las tablas Hive.

<!-- concept -->

La mayoría de piezas de Hadoop tienen sucesores de la era de la nube: almacenamiento de objetos para HDFS, Kubernetes o serverless para YARN, Spark para MapReduce. Las tablas Hive evolucionan a formatos de tabla abiertos que agregan transacciones, evolución de esquema y time travel sobre los mismos archivos Parquet, y arreglan los problemas de listado de particiones y consistencia de Hive.
Migrar un lago Hadoop es entonces menos copiar archivos y más elegir cuál de esos sucesores encaja en cada carga.

<!-- example -->

```sql
-- Spark: migrate a Hive Parquet table to Iceberg in place
CALL spark_catalog.system.migrate('sales.orders');
-- or snapshot it first to test without touching the original
CALL spark_catalog.system.snapshot('sales.orders', 'sales.orders_iceberg_test');
```

#### Un job escribe 50.000 archivos pequeños por día en HDFS. ¿Cuál es tu solución?

Hago repartition o coalesce antes de escribir para producir archivos cercanos al tamaño de bloque, ejecuto jobs periódicos de compactación sobre las particiones viejas, considero escribir en un formato de tabla que compacte y pongo alertas sobre el número de archivos por directorio.

#### Los usuarios se quejan de que el cluster de Hive va lento todas las mañanas a las 9. ¿Qué revisas?

La configuración y la contención de las colas (ETL que sigue corriendo en horario laboral), consultas ad hoc grandes sin filtros de partición, la carga de HiveServer2 y del metastore, estadísticas faltantes, y si hace falta LLAP o más capacidad para los usuarios interactivos.

#### HDFS está al 90 % y sigue creciendo. ¿Qué haces a corto y a largo plazo?

A corto plazo: borro datos temporales y la papelera, reduzco la replicación de los datos fríos y aplico cuotas. A largo plazo: escalono los datos (erasure coding, almacenamiento de archivo), muevo los datos fríos a almacenamiento de objetos, comprimo y convierto a formatos columnares, aplico políticas de retención y planifico la capacidad.

<!-- challenge -->

Una tabla Hive tiene 200.000 particiones, y planear las consultas tarda minutos listándolas. ¿Cómo ayudaría un formato de tabla abierto?

<!-- solution -->

Iceberg (o Delta) guarda los metadatos de archivos y particiones en sus propios manifests con estadísticas, así la planeación lee archivos de metadatos en vez de listar directorios y el metastore, y poda archivos por estadísticas.

<!-- takeaways -->

- Almacenamiento de objetos, Kubernetes y Spark reemplazan a HDFS, YARN y MapReduce.
- Los formatos de tabla abiertos mejoran las tablas Hive.
- Migrar significa elegir sucesores por carga.

<!-- stage: Juntarlo todo -->

### Escenarios

<!-- unit: Ingestar una base de datos al lago -->

<!-- goals -->

- Diseñar una ingesta relacional diaria hacia un lago Hadoop.
- Combinar extracción paralela, formatos, particiones y tablas.

<!-- concept -->

Las preguntas de ingesta evalúan si sabes conectar almacenamiento, cómputo y metadatos. Una buena respuesta extrae con eficiencia sin dañar la fuente, escribe archivos columnares de buen tamaño en particiones por fecha, los registra como tablas y hace seguras las re-ejecuciones. Luego cubre chequeos y programación, y si CDC sería mejor que las extracciones completas.

<!-- example -->

```text
Spark JDBC (16 parallel reads by id range) ─► Parquet, dt=2026-10-17, ~256 MB files
  ─► INSERT OVERWRITE partition (idempotent) ─► Hive Metastore table
  ─► row-count check vs source ─► Oozie/Airflow schedule, alerts
```

#### Debes migrar 500 tablas de Hive a un lakehouse en la nube. ¿Cómo lo planificas?

Clasifico las tablas por tamaño, uso y dependencias; copio los datos con `distcp` al almacenamiento de objetos; convierto a Iceberg o Delta (procedimientos de migración en su lugar o `CTAS`); las registro en el nuevo catálogo; traduzco los jobs de HiveQL a Spark SQL o dbt; migro por olas y por dominio, validando conteos y checksums, y mantengo el cluster viejo en solo lectura hasta que los consumidores cambien.

<!-- challenge -->

La tabla fuente crece a 2.000 millones de filas y la extracción diaria completa ya no cabe en la ventana. ¿Qué cambias?

<!-- solution -->

Pasa a extracción incremental: CDC desde el log de la base (o extracciones por `updated_at` con solapamiento), aplicando los cambios a un formato de tabla con `MERGE`, más una conciliación completa periódica.

<!-- takeaways -->

- Extrae en paralelo sin sobrecargar la fuente.
- Escribe archivos columnares de buen tamaño en particiones.
- Haz idempotentes las cargas; considera CDC al crecer los volúmenes.

<!-- unit: Migrar tablas Hive a un lakehouse -->

<!-- goals -->

- Planear la migración de cientos de tablas Hive a la nube.
- Ordenar copia, conversión, validación y corte.

<!-- concept -->

Migrar un parque Hive es un programa, no un job de copia. Las tablas difieren en tamaño, uso y dependencias, así que el plan las clasifica, mueve los datos por oleadas, convierte al formato y catálogo destino, porta los jobs y valida los resultados antes de cambiar a los consumidores. Retirar en el camino las tablas sin uso reduce el trabajo.

<!-- example -->

| Oleada | Tablas | Enfoque |
|---|---|---|
| 0 | Sin uso (sin lecturas en 90 días) | Archivar, no migrar |
| 1 | Pequeñas, pocos consumidores | Copiar + convertir, validación rápida |
| 2 | Grandes, críticas | distcp, Iceberg/Delta, ejecución en paralelo |
| 3 | Dependencias complejas | Portar jobs, cortar juntas |

#### Ocurre un failover del NameNode y algunos jobs fallan. ¿Por qué y cómo lo evitas?

Los clientes configurados con la dirección de un solo NameNode en lugar del nameservice de HA fallan; los jobs que estaban en medio de operaciones de metadatos pueden recibir errores. Usa el nameservice lógico (`hdfs://nameservice1`) con proxies de failover en el cliente, y reintentos en las aplicaciones.

<!-- challenge -->

Durante la ejecución en paralelo, una tabla migrada muestra 0,1 % menos filas que Hive en algunas particiones. ¿Cómo encuentras la causa?

<!-- solution -->

Compara por partición y luego por clave para encontrar las filas faltantes; causas típicas son archivos escritos después de la copia (resincronizar con `distcp -update`), diferencias de zona horaria en los valores de partición y registros que rechaza el parseo del job nuevo.

<!-- takeaways -->

- Clasifica las tablas; migra por oleadas.
- Retira las tablas sin uso en lugar de moverlas.
- Corre en paralelo y concilia antes del corte.
