## Guía de estudio de Hadoop

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de Hadoop: unas 200 preguntas](../../images/hadoop_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre Apache Hadoop y su ecosistema: HDFS, YARN, MapReduce, formatos de archivo, Hive, HBase, ZooKeeper, herramientas de ingesta, seguridad, operación y el paso al almacenamiento de objetos en la nube. Hadoop ya no es la opción por defecto para las plataformas nuevas, pero muchas empresas todavía lo usan, y sus ideas (localidad de datos, almacenamiento distribuido, gestión de recursos) son la base de Spark y del lakehouse. Abre una pregunta para ver su respuesta, o usa el filtro para buscar en toda la guía.

<!-- QA -->

### Fundamentos

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

#### ¿Por qué Hadoop prioriza el rendimiento total sobre la latencia?

Se diseñó para recorrer grandes conjuntos de datos en batch, donde importa más el tiempo total de procesamiento que el tiempo de respuesta de cada solicitud; HDFS lee bloques grandes de forma secuencial y los jobs de MapReduce tardan segundos en arrancar.

### Arquitectura de HDFS

#### ¿Qué es HDFS?

El Hadoop Distributed File System: un sistema de archivos distribuido y tolerante a fallos que divide los archivos en bloques grandes y guarda réplicas de cada bloque en máquinas distintas, dando un acceso de alto rendimiento a conjuntos de datos grandes.

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

#### ¿Por qué el NameNode es un cuello de botella para escalar?

Todos los metadatos viven en su memoria: unos 150 bytes por archivo, directorio y bloque. Cientos de millones de objetos necesitan mucho heap, y cada operación de metadatos pasa por él. La federación, los observer NameNodes y evitar los archivos pequeños ayudan.

#### ¿Qué es el erasure coding en HDFS?

Una política de almacenamiento de Hadoop 3 que guarda los datos con paridad (por ejemplo Reed-Solomon 6+3) en lugar de tres copias completas, dando una tolerancia a fallos parecida con un 50 % de sobrecosto de almacenamiento en lugar del 200 %. Las lecturas y la reconstrucción cuestan más CPU y red, así que sirve para datos fríos.

#### ¿Qué son los archivos `fsimage` y `edits`?

`fsimage` es un checkpoint de todo el espacio de nombres en un momento dado; `edits` es el log de todos los cambios desde ese checkpoint. Al arrancar, el NameNode carga el `fsimage` y reproduce los edits.

#### ¿Qué son los JournalNodes?

Un pequeño quórum de demonios (normalmente tres o cinco) que guardan el log de edits compartido de los NameNodes en HA; el NameNode activo escribe en la mayoría, y los standby leen de ellos para mantenerse sincronizados.

#### ¿Qué es el fencing en la HA del NameNode?

Mecanismos que garantizan que un NameNode que era activo ya no pueda modificar el espacio de nombres tras el failover (por ejemplo matando su proceso o haciendo que los JournalNodes solo acepten escrituras de una época de escritor), evitando el split brain.

#### ¿Cómo maneja HDFS un archivo más pequeño que un bloque?

Usa solo el disco que el archivo necesita; un archivo de 1 MB no consume 128 MB. Pero sigue costando un objeto de metadatos completo en el NameNode, que es el verdadero problema de los archivos pequeños.

#### ¿Qué es el espacio de nombres de HDFS?

La jerarquía de directorios y archivos, con permisos, propietarios, cuotas y fechas de modificación, que mantiene el NameNode, parecida al árbol de un sistema de archivos tradicional.

### Operación de HDFS

#### ¿Cómo funciona una escritura en HDFS?

El cliente le pide al NameNode crear el archivo; para cada bloque, el NameNode devuelve una lista de DataNodes. El cliente envía los datos en paquetes al primer DataNode, que los reenvía al segundo, que los reenvía al tercero (un pipeline). Las confirmaciones vuelven en sentido contrario, y el archivo es visible cuando se cierra.

#### ¿Cómo funciona una lectura en HDFS?

El cliente le pide al NameNode la ubicación de los bloques del archivo, y luego lee cada bloque directamente del DataNode más cercano que tiene una réplica, verificando los checksums; si un DataNode falla, cambia a otra réplica.

#### ¿Cómo detecta HDFS los datos corruptos?

Cada bloque tiene checksums calculados al escribir; los clientes los verifican al leer, y los DataNodes ejecutan un escáner de bloques en segundo plano. Las réplicas corruptas se reportan al NameNode, que vuelve a replicar desde una copia sana.

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

#### ¿Qué muestra `hdfs dfs -count`?

El número de directorios, archivos y bytes bajo una ruta y, con `-q`, las cuotas de nombres y de espacio, útil para encontrar directorios con demasiados archivos pequeños.

#### ¿Qué es WebHDFS?

Una API REST de HDFS sobre HTTP que permite a clientes en cualquier lenguaje leer, escribir y administrar archivos sin las librerías de Hadoop; HttpFS ofrece una versión tipo gateway.

### YARN

#### ¿Qué es YARN?

Yet Another Resource Negotiator: el gestor de recursos del cluster Hadoop. Asigna CPU y memoria en contenedores a las aplicaciones (MapReduce, Spark, Tez, Flink), separando la gestión de recursos del motor de procesamiento.

#### ¿Cuáles son los componentes principales de YARN?

El ResourceManager (programador y gestor de aplicaciones de todo el cluster), los NodeManagers (agentes por nodo que lanzan y vigilan los contenedores), los ApplicationMasters (uno por aplicación, que negocian recursos y coordinan las tareas) y los contenedores (paquetes asignados de memoria y vcores).

#### ¿Qué pasa cuando envías una aplicación a YARN?

El cliente la envía al ResourceManager, que arranca el ApplicationMaster en un contenedor en algún nodo. El ApplicationMaster pide contenedores para las tareas, teniendo en cuenta la localidad de los datos; los NodeManagers los lanzan; el ApplicationMaster vigila el avance e informa la finalización.

#### ¿Qué programadores ofrece YARN?

El programador FIFO (el primero que llega, primero atendido), el Capacity Scheduler (colas jerárquicas con capacidades garantizadas y elasticidad, el predeterminado en la mayoría de las distribuciones) y el Fair Scheduler (reparte los recursos de forma justa entre aplicaciones y colas en ejecución).

#### ¿Cómo funciona el Capacity Scheduler?

Las colas se configuran con porcentajes garantizados de la capacidad del cluster (por ejemplo `etl` 50 %, `analytics` 30 %, `adhoc` 20 %), pueden tomar prestada capacidad ociosa hasta un máximo, tienen límites por usuario y pueden expropiar contenedores para devolver la capacidad garantizada.

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

#### ¿Cómo se limita que un usuario use todo el cluster?

Con límites de las colas del programador: capacidad máxima por cola, factores de límite por usuario, máximo de aplicaciones por usuario y por cola, y listas de control de acceso en las colas.

### MapReduce

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

### Formatos de archivo y compresión

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

#### ¿Cómo eliges entre Avro y Parquet?

Avro para escrituras por filas, streaming y mensajes donde se leen registros completos y los esquemas evolucionan seguido; Parquet para analítica donde las consultas leen pocas columnas de muchas filas.

### Hive

#### ¿Qué es Apache Hive?

Un sistema de data warehouse sobre Hadoop que permite consultar datos en HDFS (y en almacenamiento de objetos) con un dialecto SQL (HiveQL). Las consultas se compilan en jobs de MapReduce, Tez o Spark, y los metadatos de las tablas se guardan en el Hive Metastore.

#### ¿Qué es el Hive Metastore?

Un servicio respaldado por una base relacional (MySQL, PostgreSQL) que guarda las definiciones de las tablas, columnas, particiones, ubicaciones y formatos. Lo usan Hive, Spark, Impala, Presto/Trino y otros, y el AWS Glue Data Catalog es compatible con él.

#### ¿Qué diferencia hay entre tablas administradas y externas en Hive?

Hive es dueño de los datos de las tablas administradas: borrar la tabla borra los archivos. Las tablas externas apuntan a datos administrados en otro lugar: borrarlas solo elimina los metadatos. Las tablas externas son comunes en los data lakes compartidos.

#### ¿Qué son las particiones en Hive?

Subdirectorios por valores de columna (`/sales/dt=2026-10-15/`); las consultas que filtran por las columnas de partición solo leen los directorios que coinciden. El particionado dinámico crea particiones a partir de los resultados de una consulta.

#### ¿Qué es el bucketing en Hive?

Dividir los datos de una tabla o partición en un número fijo de archivos según el hash de una columna, lo que permite muestreos eficientes y bucket map joins cuando las tablas están agrupadas por la clave del join.

#### ¿Qué motores de ejecución puede usar Hive?

MapReduce (histórico, obsoleto), Apache Tez (basado en DAG, el predeterminado habitual en Hive 2/3) y Spark (Hive on Spark). Hive LLAP añade demonios de larga duración con caché para las consultas interactivas.

#### ¿Qué son las tablas ACID de Hive?

Tablas ORC transaccionales (las tablas administradas de Hive 3) que admiten `INSERT`, `UPDATE`, `DELETE` y `MERGE` con aislamiento por snapshots, usando archivos delta que se fusionan con compactaciones (menores y mayores).

#### ¿Qué es el optimizador basado en costos de Hive?

Una optimización basada en Apache Calcite que usa estadísticas de tablas y columnas (`ANALYZE TABLE … COMPUTE STATISTICS`) para elegir el orden y la estrategia de los joins; sin estadísticas, los planes pueden ser malos.

#### ¿Qué es un map join en Hive?

Un join en el que la tabla pequeña se carga en memoria en cada mapper (broadcast), evitando el shuffle; Hive convierte los joins automáticamente cuando la tabla pequeña está por debajo de un umbral de tamaño (`hive.auto.convert.join`).

#### ¿Cómo se cargan datos en tablas de Hive?

Con `LOAD DATA INPATH` (mueve archivos a la ubicación de la tabla), `INSERT INTO/OVERWRITE … SELECT`, `CREATE TABLE AS SELECT`, o escribiendo archivos directamente en la ubicación de una tabla externa y añadiendo las particiones.

#### ¿Qué es `MSCK REPAIR TABLE`?

Un comando que recorre la ubicación de la tabla buscando directorios de partición no registrados en el metastore y los añade.

#### ¿Qué son los SerDe en Hive?

Serializadores/deserializadores que definen cómo se leen y escriben las filas en los archivos: `LazySimpleSerDe` para texto delimitado, `OpenCSVSerde`, SerDe JSON, `RegexSerDe`, y soporte integrado para ORC, Parquet y Avro.

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

#### ¿Cómo se calculan estadísticas en Hive?

Con `ANALYZE TABLE t PARTITION (dt) COMPUTE STATISTICS` para las estadísticas de tabla y partición, y `… FOR COLUMNS` para las de columnas, que usa el optimizador basado en costos; `hive.stats.autogather` recoge las estadísticas básicas al insertar.

#### ¿Qué es la inserción con particiones dinámicas y qué hay que vigilar?

`INSERT OVERWRITE TABLE t PARTITION (dt) SELECT …, dt FROM src` crea particiones a partir de los valores de los datos. Existen límites (`hive.exec.max.dynamic.partitions`) para evitar crear miles de particiones por accidente, y muchas particiones con pocas filas generan archivos pequeños.

### HBase

#### ¿Qué es HBase?

Una base de datos NoSQL distribuida por familias de columnas, inspirada en Google Bigtable, que corre sobre HDFS. Ofrece acceso aleatorio de lectura y escritura en tiempo real a miles de millones de filas por clave de fila, con consistencia fuerte por fila.

#### ¿Cuál es el modelo de datos de HBase?

Tablas de filas ordenadas por clave de fila; cada fila tiene familias de columnas (definidas al crear la tabla), cada familia tiene cualquier número de columnas (qualifiers), y cada celda guarda versiones identificadas por marcas de tiempo. Las columnas dispersas no cuestan nada.

#### ¿Cuáles son los componentes principales de HBase?

El HMaster (asigna regiones, maneja los cambios de esquema y el balanceo de carga), los RegionServers (atienden las lecturas y escrituras de las regiones), las regiones (rangos contiguos de claves de fila de una tabla) y ZooKeeper (coordinación y localización de la tabla meta).

#### ¿Cómo funciona una escritura en HBase?

El RegionServer añade la edición al write-ahead log (WAL) en HDFS para la durabilidad, y luego la escribe en la MemStore en memoria. Cuando la MemStore se llena, se vuelca a un HFile inmutable en HDFS.

#### ¿Qué son las compactaciones en HBase?

Procesos en segundo plano que fusionan HFiles: las compactaciones menores fusionan unos pocos archivos pequeños; las mayores reescriben todos los archivos de un store en uno, eliminando las celdas borradas y vencidas. Las mayores usan mucha E/S y suelen programarse fuera de las horas pico.

#### ¿Por qué es tan importante el diseño de la clave de fila en HBase?

Todo acceso es por clave de fila, y las filas se ordenan y dividen en regiones por clave. Las claves que siempre crecen (marcas de tiempo, secuencias) envían todas las escrituras a una región (hotspotting). Usa salting, hashing o inversión de campos, y diseña las claves según los patrones de acceso principales.

#### ¿Cuándo elegirías HBase en lugar de Hive?

HBase para lecturas y escrituras aleatorias de baja latencia por clave (perfiles de usuario, búsquedas en series de tiempo, contadores); Hive para analítica SQL batch sobre lecturas grandes.

#### ¿Qué es Apache Phoenix?

Una capa SQL sobre HBase que compila SQL en scans de HBase, con índices secundarios y acceso JDBC.

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

### Otras herramientas del ecosistema

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

#### ¿Qué es Apache Ozone?

Un almacén de objetos distribuido y escalable para Hadoop con una API compatible con S3, diseñado para superar los límites de HDFS con los archivos pequeños y el espacio de nombres, manteniéndose compatible con las aplicaciones Hadoop.

### Seguridad y gobierno

#### ¿Cómo se hace la autenticación en Hadoop?

Con Kerberos: usuarios y servicios obtienen tickets de un Key Distribution Center y los servicios de Hadoop los verifican. Sin Kerberos (modo "simple"), Hadoop confía en el nombre de usuario que declara el cliente, lo que es inseguro.

#### ¿Qué son los delegation tokens?

Tokens emitidos por los servicios (NameNode, ResourceManager) tras la autenticación Kerberos, que se pasan a las tareas del cluster para que accedan a HDFS sin tener credenciales Kerberos propias.

#### ¿Cómo se administran los permisos de HDFS?

Con permisos tipo POSIX de propietario/grupo/otros sobre archivos y directorios, más ACL para un control más fino. Las políticas detalladas y centralizadas suelen administrarse con Apache Ranger.

#### ¿Qué es Apache Ranger?

Un framework de seguridad centralizado para Hadoop que define y audita políticas de acceso (rutas de HDFS, bases, tablas y columnas de Hive, filtros de filas y enmascaramiento, HBase, Kafka) con plugins que las aplican en cada servicio.

#### ¿Qué es Apache Atlas?

Un servicio de metadatos y gobierno que ofrece catálogo de datos, linaje, clasificación (etiquetas como PII) e integración con Ranger para políticas basadas en etiquetas.

#### ¿Qué es Apache Knox?

Un gateway que ofrece un único punto de entrada seguro (APIs REST, interfaces) a los servicios de Hadoop para usuarios fuera del cluster, encargándose de la autenticación y SSL.

#### ¿Cómo se cifran los datos en Hadoop?

En tránsito con cifrado de RPC, TLS en las interfaces web y cifrado de la transferencia de datos; en reposo con el cifrado transparente de HDFS mediante zonas de cifrado cuyas claves administra el Hadoop Key Management Server (KMS).

#### ¿Qué es un keytab?

Un archivo con las claves de un principal de Kerberos, usado por servicios y jobs batch para autenticarse sin contraseña; los keytabs se deben proteger como contraseñas.

#### ¿Qué es la suplantación (proxy users) en Hadoop?

Una configuración que permite a un servicio de confianza (HiveServer2, Livy, Oozie) actuar en nombre de los usuarios finales, para que los permisos y las auditorías reflejen al usuario real y no a la cuenta de servicio.

#### ¿Cómo se audita el acceso en Hadoop?

Los logs de auditoría de HDFS en el NameNode registran cada acceso a archivos; Ranger recoge los eventos de auditoría de todos sus plugins en Solr o HDFS, y Atlas registra el linaje.

### Operación y rendimiento

#### ¿Cómo se dimensiona un cluster Hadoop?

A partir del volumen de datos (tamaño en bruto × factor de replicación × crecimiento, más espacio temporal), las necesidades de procesamiento (CPU y memoria para los jobs concurrentes) y los objetivos de rendimiento; dejando margen para fallos y rebalanceo (a menudo se mantienen los discos por debajo del 70–80 %).

#### ¿Cuáles son las causas comunes de jobs lentos en Hadoop?

Data skew (unos pocos reducers con la mayoría de las claves), demasiados archivos pequeños, paralelismo insuficiente o excesivo, derrames a disco por buffers de memoria pequeños, entradas comprimidas no divisibles, falta de localidad de datos y contención en las colas de YARN.

#### ¿Cómo se ajusta la memoria de MapReduce?

Definiendo `mapreduce.map.memory.mb` y `mapreduce.reduce.memory.mb` para el tamaño de los contenedores y `-Xmx` en `mapreduce.map.java.opts` en torno al 80 % del contenedor, y ajustando `mapreduce.task.io.sort.mb` para reducir los derrames.

#### ¿Cómo se maneja el data skew en los jobs de Hadoop?

Con combiners, partitioners propios, salting de las claves calientes, joins del lado del map para las tablas pequeñas, las optimizaciones de skew join de Hive (`hive.optimize.skewjoin`) o preagregación.

#### ¿Cómo se monitorea un cluster Hadoop?

Con las interfaces web del NameNode y del ResourceManager, las métricas JMX, Cloudera Manager (o históricamente Ambari), exportadores de Prometheus y Grafana, y alertas sobre la capacidad de HDFS, los nodos muertos o lentos, los bloques subreplicados, el heap del NameNode, la latencia de RPC y el uso de las colas.

#### ¿Cómo se actualiza un cluster Hadoop?

Planificando con las notas de la versión y revisiones de compatibilidad, respaldando los metadatos del NameNode, usando actualizaciones progresivas (rolling) cuando se admiten (NameNodes en HA, DataNodes uno a uno), probando los jobs en un cluster de staging y conservando la posibilidad de revertir hasta finalizar.

#### ¿Cómo se respalda HDFS?

Con snapshots para los errores de los usuarios, `distcp` hacia otro cluster o almacenamiento de objetos para la recuperación ante desastres, y respaldos de los metadatos del NameNode (`fsimage` y edits). La replicación dentro del cluster no es un respaldo.

#### ¿Qué impacto tiene el garbage collection de la JVM en los servicios de Hadoop?

Las pausas largas de GC en el NameNode o los RegionServers los dejan sin responder, causando timeouts, failovers o heartbeats perdidos. Dimensiona bien los heaps, usa recolectores modernos (G1) y vigila los logs de GC.

#### ¿Cómo se encuentran los jobs que más recursos del cluster usan?

Con la interfaz y las APIs del ResourceManager de YARN (memoria-segundos y vcore-segundos por aplicación), las métricas de las colas, los history servers de Spark y MapReduce y los informes de uso de las herramientas de administración.

#### ¿Cómo se limpia un cluster que se queda sin espacio?

Buscando los directorios grandes y viejos (`hdfs dfs -du -h`), vaciando la papelera, borrando datos temporales obsoletos y snapshots viejos, reduciendo la replicación de los datos fríos o aplicando erasure coding, comprimiendo o convirtiendo a formatos columnares, y añadiendo capacidad si hace falta.

#### ¿Para qué sirve `mapreduce.job.reduce.slowstart.completedmaps`?

Define la fracción de maps que deben terminar antes de que los reducers empiecen a traer la salida; arrancar los reducers demasiado pronto desperdicia slots esperando, demasiado tarde retrasa el shuffle.

### Hadoop y la nube

#### ¿Cómo se compara HDFS con Amazon S3?

HDFS acopla almacenamiento y cómputo en los mismos nodos, da localidad de datos y consistencia fuerte, y requiere administrar un cluster. S3 es almacenamiento de objetos administrado, escalable de forma independiente, más barato y muy durable, al que se accede por la red; hoy también tiene consistencia fuerte. La mayoría de los data lakes en la nube usan almacenamiento de objetos en lugar de HDFS.

#### ¿Qué es el conector S3A?

El conector de sistema de archivos de Hadoop (`s3a://`) que permite a Hadoop, Hive y Spark leer y escribir en S3 como si fuera un sistema de archivos, con optimizaciones para cargas multiparte, committers que evitan los renombrados lentos y proveedores de credenciales.

#### ¿Por qué los renombrados son un problema en el almacenamiento de objetos?

Los almacenes de objetos no tienen directorios reales; un "renombrado" es una copia más un borrado de cada objeto, lo que es lento y no atómico. Los committers de salida de Hadoop que dependen de renombrar son lentos o inseguros en S3, así que se usan los committers de S3A (magic, staging) o formatos de tabla (Iceberg, Delta).

#### ¿Qué es Amazon EMR?

Una plataforma administrada de big data en AWS que ejecuta Hadoop, Spark, Hive, HBase, Presto/Trino, Flink y otros sobre EC2, EKS o serverless, usando S3 (EMRFS/S3A) como almacenamiento principal y el Glue Data Catalog como metastore, con clusters transitorios o de larga duración.

#### ¿Qué es un cluster transitorio?

Un cluster creado para un job o pipeline y terminado después, con los datos guardados en almacenamiento de objetos. Evita pagar clusters ociosos y hace reproducibles los entornos.

#### ¿Cómo migrarías un data lake Hadoop a la nube?

Inventariando los datos, los jobs y las dependencias; copiando los datos al almacenamiento de objetos con `distcp` o servicios de transferencia; convirtiendo las tablas a formatos abiertos (Parquet y luego Iceberg o Delta); pasando el metastore a un catálogo administrado (Glue, Unity Catalog); portando los jobs de Hive y MapReduce a Spark o motores SQL; reemplazando Oozie por Airflow; recreando la seguridad con el IAM de la nube y los permisos del catálogo; y validando los resultados en paralelo antes de dar de baja el cluster.

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

#### ¿En qué difieren los costos entre Hadoop on-premises y los data lakes en la nube?

Los clusters on-premises tienen costos fijos altos (hardware, centros de datos, personal) y se dimensionan para los picos; los lakes en la nube tienen almacenamiento y cómputo de pago por uso que pueden bajar a cero, pero requieren gobierno de costos para evitar un uso descontrolado.

### Spark sobre Hadoop

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

#### ¿Qué es la asignación dinámica de Spark en YARN?

Una función en la que Spark pide y libera executors según las tareas pendientes, para que los executors ociosos devuelvan sus recursos a YARN; necesita el servicio de shuffle externo (o el seguimiento del shuffle) para que los archivos del shuffle sobrevivan a la eliminación de los executors.

#### ¿Qué es el servicio de shuffle externo?

Un servicio que corre en cada NodeManager y sirve los archivos de shuffle escritos por los executors, para que estos se puedan eliminar (asignación dinámica) o fallar sin perder su salida del shuffle.

#### ¿Cómo se eligen los tamaños de los executors en YARN?

Equilibrando cores y memoria: unos 4–5 cores por executor para un buen rendimiento con HDFS, memoria por core según la carga, overhead para las necesidades fuera del heap, y dejando recursos para el NodeManager y el sistema operativo en cada nodo.

### Escenarios

#### El NameNode se queda sin memoria heap. ¿Qué haces?

A corto plazo, aumento el heap y reinicio en una ventana de mantenimiento (con HA, hago failover). A largo plazo, reduzco los objetos: encuentro y compacto los archivos pequeños, borro datos sin uso y snapshots viejos, uso archivos HAR y considero la federación o los observer NameNodes.

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

#### Un job escribe 50.000 archivos pequeños por día en HDFS. ¿Cuál es tu solución?

Hago repartition o coalesce antes de escribir para producir archivos cercanos al tamaño de bloque, ejecuto jobs periódicos de compactación sobre las particiones viejas, considero escribir en un formato de tabla que compacte y pongo alertas sobre el número de archivos por directorio.

#### Los usuarios se quejan de que el cluster de Hive va lento todas las mañanas a las 9. ¿Qué revisas?

La configuración y la contención de las colas (ETL que sigue corriendo en horario laboral), consultas ad hoc grandes sin filtros de partición, la carga de HiveServer2 y del metastore, estadísticas faltantes, y si hace falta LLAP o más capacidad para los usuarios interactivos.

#### HDFS está al 90 % y sigue creciendo. ¿Qué haces a corto y a largo plazo?

A corto plazo: borro datos temporales y la papelera, reduzco la replicación de los datos fríos y aplico cuotas. A largo plazo: escalono los datos (erasure coding, almacenamiento de archivo), muevo los datos fríos a almacenamiento de objetos, comprimo y convierto a formatos columnares, aplico políticas de retención y planifico la capacidad.

#### Debes migrar 500 tablas de Hive a un lakehouse en la nube. ¿Cómo lo planificas?

Clasifico las tablas por tamaño, uso y dependencias; copio los datos con `distcp` al almacenamiento de objetos; convierto a Iceberg o Delta (procedimientos de migración en su lugar o `CTAS`); las registro en el nuevo catálogo; traduzco los jobs de HiveQL a Spark SQL o dbt; migro por olas y por dominio, validando conteos y checksums, y mantengo el cluster viejo en solo lectura hasta que los consumidores cambien.

#### Ocurre un failover del NameNode y algunos jobs fallan. ¿Por qué y cómo lo evitas?

Los clientes configurados con la dirección de un solo NameNode en lugar del nameservice de HA fallan; los jobs que estaban en medio de operaciones de metadatos pueden recibir errores. Usa el nameservice lógico (`hdfs://nameservice1`) con proxies de failover en el cliente, y reintentos en las aplicaciones.
