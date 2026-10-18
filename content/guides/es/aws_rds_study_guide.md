## Guía de estudio de Amazon RDS

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de Amazon RDS: unas 200 preguntas](../../images/aws_rds_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre Amazon RDS y Aurora: motores, elección de instancia y almacenamiento, alta disponibilidad con Multi-AZ, réplicas de lectura, backups y restauraciones, seguridad, monitoreo, rendimiento, escalado, costos, migraciones, y cómo los ingenieros de datos extraen datos de RDS con CDC, exportaciones y zero-ETL. Las respuestas reflejan el servicio en 2026. Abre una pregunta para ver su respuesta, o usa el filtro para buscar en toda la guía.

<!-- QA -->

### Fundamentos

#### ¿Qué es Amazon RDS?

Amazon Relational Database Service: un servicio administrado para ejecutar bases de datos relacionales en AWS. AWS se encarga del aprovisionamiento, los parches, los backups, el monitoreo, el failover y el almacenamiento, mientras tú eliges el motor, el tamaño de la instancia y la configuración, y administras los esquemas, las consultas y los usuarios.

#### ¿Qué motores de base de datos admite RDS?

MySQL, PostgreSQL, MariaDB, Oracle, Microsoft SQL Server e IBM Db2, además de Amazon Aurora (compatible con MySQL y con PostgreSQL), que forma parte de la familia RDS pero tiene su propia arquitectura de almacenamiento.

#### ¿Qué administra AWS en RDS y qué sigues administrando tú?

AWS administra el hardware, la instalación y los parches del sistema operativo, la instalación del software de base de datos y sus versiones menores, los backups automáticos, el almacenamiento, la replicación y el failover Multi-AZ, y las métricas de monitoreo. Tú administras el diseño de la base, las consultas y los índices, los usuarios y privilegios, el ajuste de parámetros, las reglas de los grupos de seguridad, las decisiones de capacidad y el manejo de conexiones de la aplicación.

#### ¿Qué es una instancia de base de datos (DB instance)?

Un entorno de base de datos aislado en la nube: una clase de instancia de cómputo (CPU y memoria) con almacenamiento asociado, que ejecuta una versión de un motor y es accesible por un endpoint (nombre DNS y puerto).

#### ¿Qué es una clase de instancia?

La capacidad de cómputo y memoria de una instancia: ampliables (burstable, `db.t4g`, `db.t3`) para cargas ligeras o variables, de propósito general (`db.m*`) y optimizadas para memoria (`db.r*`, `db.x*`) para bases de producción. Las clases Graviton (sufijo `g`) suelen dar mejor relación precio-rendimiento.

#### ¿Cuándo RDS no es la opción correcta?

Cuando necesitas acceso al sistema operativo o extensiones no admitidas (considera RDS Custom o EC2), un motor que RDS no ofrece, una escala extrema más allá de un solo escritor (considera Aurora DSQL, DynamoDB o sharding), o cargas analíticas sobre terabytes que encajan mejor en un data warehouse o un lakehouse.

#### ¿Qué diferencia hay entre RDS y ejecutar una base de datos en EC2?

En EC2 tienes control total (sistema operativo, cualquier versión, cualquier configuración) pero lo administras todo: instalación, parches, backups, replicación, failover y monitoreo. RDS elimina ese trabajo operativo a cambio de algunas restricciones (sin acceso al sistema operativo, privilegios de superusuario limitados, solo parámetros admitidos).

#### ¿Qué es RDS Custom?

Una variante de RDS para Oracle y SQL Server que da acceso al sistema operativo y permite personalizar la base de datos (para aplicaciones heredadas que necesitan parches o software concretos), mientras AWS sigue automatizando los backups y parte de la administración.

#### ¿Qué es un DB subnet group?

Un conjunto de subredes (en al menos dos zonas de disponibilidad) de una VPC donde RDS puede ubicar las instancias. Es necesario para crear una instancia en una VPC y para admitir Multi-AZ.

#### ¿Qué es un endpoint de RDS?

El nombre DNS y el puerto que usan las aplicaciones para conectarse. Se mantiene durante el failover (el registro DNS apunta a la nueva primaria), así que las aplicaciones siempre deben conectarse por el endpoint, no por una dirección IP.

#### ¿Qué son los parameter groups?

Contenedores de ajustes de configuración del motor (por ejemplo `max_connections`, `work_mem`, `innodb_buffer_pool_size`, `log_min_duration_statement`) que se aplican a las instancias. Los grupos por defecto no se pueden modificar; se crean grupos propios. Los parámetros dinámicos se aplican de inmediato, los estáticos necesitan un reinicio.

#### ¿Qué son los option groups?

Contenedores de funciones opcionales de algunos motores, como el Transparent Data Encryption de Oracle, el backup nativo de SQL Server hacia S3 o el plugin memcached de MySQL.

#### ¿Qué es la ventana de mantenimiento?

Un rango de tiempo semanal en el que AWS aplica el mantenimiento pendiente, como parches del sistema operativo, actualizaciones menores obligatorias o modificaciones de instancia aplazadas a la ventana. Con Multi-AZ, el mantenimiento se aplica primero a la standby y luego hay failover, para reducir la interrupción.

#### ¿Se puede detener una instancia de RDS?

Sí, durante un máximo de 7 días seguidos; después AWS la vuelve a encender automáticamente para aplicar mantenimiento. Mientras está detenida pagas el almacenamiento y los backups, pero no las horas de instancia. Los clusters de Aurora se pueden detener de forma parecida.

#### ¿Qué es la protección contra borrado?

Un ajuste que impide borrar una instancia o un cluster hasta que se desactive, protegiendo las bases de producción de un borrado accidental.

#### ¿Qué es el modelo de responsabilidad compartida en RDS?

AWS se encarga de la infraestructura, el sistema operativo, los parches del software de base de datos, los backups y los mecanismos de replicación. Tú te encargas del acceso de red (grupos de seguridad), las decisiones de cifrado, los usuarios y privilegios de la base, el diseño del esquema y de las consultas, los parámetros y la protección de las credenciales.

#### ¿Cómo te conectas desde tu computador a una instancia de RDS en una subred privada?

Mediante un bastión o, mejor, el reenvío de puertos de AWS Systems Manager Session Manager hacia una instancia en la VPC, una VPN de cliente, o un EC2 dentro de la VPC; nunca haciendo pública la base de datos.

#### ¿Qué significa "publicly accessible" en una instancia de RDS?

La instancia recibe una IP pública y su endpoint la resuelve desde fuera de la VPC, así que es accesible desde internet si los grupos de seguridad lo permiten. Las bases de producción deben tenerlo desactivado.

#### ¿Cómo se crean instancias de RDS de forma repetible?

Con infraestructura como código (CloudFormation, CDK, Terraform), definiendo los subnet groups, parameter groups, grupos de seguridad, claves KMS, secretos y la instancia, para que los entornos sean coherentes y los cambios se revisen.

#### ¿Para qué sirven las etiquetas en RDS?

Para la asignación de costos, el control de acceso (condiciones IAM sobre etiquetas), la automatización (por ejemplo detener de noche las instancias con `env=dev`) y la información de responsables.

#### ¿Qué es RDS on Outposts?

RDS ejecutándose sobre hardware AWS Outposts en tu propio centro de datos, para cargas que necesitan baja latencia hacia sistemas on-premises o residencia de los datos, administrado con las mismas APIs.

### Almacenamiento

#### ¿Qué tipos de almacenamiento ofrece RDS?

SSD de propósito general gp3 (base de 3.000 IOPS y 125 MiB/s, con IOPS y rendimiento configurables independientemente del tamaño), gp2 (IOPS ligadas al tamaño con créditos de ráfaga), IOPS aprovisionadas io1 e io2 Block Express (IOPS altas y constantes y baja latencia) y el almacenamiento magnético heredado.

#### ¿Cuándo conviene elegir IOPS aprovisionadas?

Para cargas de producción intensivas en E/S que necesitan una latencia baja y constante e IOPS altas (OLTP muy activo, grandes volúmenes de escritura), cuando los límites configurables de gp3 no alcanzan o la previsibilidad importa más que el costo.

#### ¿Qué es el autoescalado del almacenamiento?

Un ajuste que aumenta automáticamente el almacenamiento asignado cuando queda poco espacio libre, hasta un máximo que defines, evitando caídas por disco lleno. El almacenamiento no se puede reducir después.

#### ¿Se puede reducir el almacenamiento asignado en RDS?

No directamente. Para reducirlo, crea una instancia nueva con menos almacenamiento y migra los datos (dump y restore, DMS o replicación lógica), o usa despliegues Blue/Green donde se admitan.

#### ¿Por qué el rendimiento de gp2 puede caer de repente?

Los volúmenes gp2 pequeños dependen de créditos de ráfaga por encima de sus IOPS base (3 IOPS por GB). Cuando se agotan los créditos, el rendimiento cae a la base. gp3 lo evita con una base fija independiente del tamaño.

#### ¿Cuál es el almacenamiento máximo de una instancia de RDS?

Hasta 64 TiB en la mayoría de los motores (menos en algunas configuraciones de SQL Server). El almacenamiento de Aurora crece automáticamente hasta 128 TiB por cluster.

#### ¿Qué significa el estado "storage-full"?

La instancia se quedó sin almacenamiento y deja de aceptar escrituras. Activa el autoescalado del almacenamiento, crea alertas sobre `FreeStorageSpace` y limpia tablas grandes, logs o archivos temporales.

#### ¿Cómo se compara gp3 con io2 en RDS?

gp3 ofrece una base de 3.000 IOPS y 125 MiB/s, configurable hasta límites mayores con costo extra, a un precio por GB más bajo. io2 Block Express ofrece IOPS más altas y constantes y menor latencia con mejor durabilidad, para las cargas más exigentes.

#### ¿Qué indica `DiskQueueDepth`?

El número de solicitudes de E/S pendientes esperando al disco. Una cola alta y constante con latencia alta significa que el almacenamiento no da abasto; considera más IOPS, mejores consultas o caché.

#### ¿Qué impacto tiene modificar el almacenamiento de una instancia en marcha?

Aumentar el almacenamiento o cambiar el tipo suele hacerse en línea, pero la instancia puede quedar horas en estado "storage-optimization", durante el cual no se permiten más cambios de almacenamiento; el rendimiento puede verse algo afectado.

#### ¿Cómo se estiman las IOPS necesarias?

A partir de las métricas actuales (`ReadIOPS` + `WriteIOPS` en el pico) o, para cargas nuevas, de las transacciones por segundo esperadas y la E/S por transacción, con margen; luego se prueba con carga antes de producción.

### Alta disponibilidad y Multi-AZ

#### ¿Qué es un despliegue Multi-AZ de instancia?

RDS mantiene una réplica standby síncrona de la primaria en otra zona de disponibilidad. Si la primaria falla (hardware, caída de la AZ, fallo de almacenamiento) o durante ciertos mantenimientos, RDS hace failover automático a la standby, normalmente en uno o dos minutos. La standby no atiende lecturas.

#### ¿Qué es un despliegue Multi-AZ de cluster?

Un despliegue (para MySQL y PostgreSQL) con un escritor y dos instancias standby legibles en tres AZ, con replicación semisíncrona. El failover es más rápido (normalmente menos de 35 segundos) y las standby pueden atender lecturas mediante un endpoint de lectura.

#### ¿Cómo funciona el failover Multi-AZ?

RDS detecta el fallo, promueve la standby y actualiza el registro DNS del endpoint para que apunte a ella. Las aplicaciones deben reconectarse; los pools de conexiones deben manejar las desconexiones y respetar el TTL del DNS.

#### ¿Qué eventos disparan un failover automático?

La pérdida de la instancia primaria o de su AZ, un fallo de red o de almacenamiento en la primaria, los cambios de tipo de instancia, los parches del sistema operativo y algunos mantenimientos del motor, y un reinicio manual con failover.

#### ¿Multi-AZ sirve para escalar?

No. En los despliegues Multi-AZ de instancia, la standby no atiende tráfico; sirve para la disponibilidad y la durabilidad. Para escalar lecturas usa réplicas de lectura (o las standby legibles de los clusters Multi-AZ, o las réplicas de Aurora).

#### ¿Cómo se prueba un failover?

Reiniciando la instancia con la opción "reboot with failover" y observando el comportamiento de la aplicación, el tiempo de reconexión y los errores. Hacerlo con regularidad valida la resiliencia de la aplicación.

#### ¿Multi-AZ protege contra datos corruptos o borrados accidentales?

No. La replicación copia todos los cambios a la standby, incluidos los malos. Los backups, la recuperación a un punto en el tiempo y los snapshots protegen contra los errores lógicos.

#### ¿Qué diferencia hay entre alta disponibilidad y recuperación ante desastres en RDS?

La alta disponibilidad (Multi-AZ) mantiene la base funcionando cuando falla una AZ o una instancia dentro de una región. La recuperación ante desastres cubre la pérdida de una región o de datos: réplicas de lectura entre regiones, copias de snapshots entre regiones, AWS Backup y Aurora Global Database, con un RPO y un RTO definidos.

#### ¿Cómo deben manejar las aplicaciones el failover?

Usando el endpoint (nunca IPs), con un caché de DNS corto (por ejemplo el TTL de DNS de la JVM), con reintentos con espera ante errores de conexión, con pools que validan las conexiones, y considerando RDS Proxy o los drivers de AWS que detectan antes el failover.

#### ¿Qué son los AWS Advanced JDBC/Python wrappers?

Envoltorios de drivers que conocen la topología de RDS y Aurora, detectan los failovers más rápido que las actualizaciones de DNS y se reconectan al nuevo escritor, reduciendo la interrupción que perciben las aplicaciones.

#### ¿Se puede elegir en qué AZ va la standby?

RDS elige la AZ de la standby dentro del subnet group; tú eliges la AZ de la primaria. El subnet group debe tener subredes en al menos dos AZ (o tres para los clusters Multi-AZ).

#### ¿Qué RPO y RTO da Multi-AZ?

En los despliegues Multi-AZ de instancia, el RPO es prácticamente cero (replicación síncrona) y el RTO suele ser de uno a dos minutos; en los clusters Multi-AZ, el RTO suele ser de menos de un minuto.

### Réplicas de lectura

#### ¿Qué es una réplica de lectura?

Una copia de una instancia origen mantenida al día con replicación asíncrona, usada para descargar el tráfico de lectura (reportes, analítica, APIs con muchas lecturas). Tiene su propio endpoint y puede estar en la misma región o en otra.

#### ¿Cuántas réplicas de lectura se pueden crear?

Hasta 15 para MySQL, MariaDB y PostgreSQL, y menos para Oracle y SQL Server; Aurora admite hasta 15 Aurora Replicas por cluster. En algunos motores las réplicas también pueden tener sus propias réplicas.

#### ¿Qué es el retraso de réplica (replica lag)?

La demora entre una escritura en el origen y su visibilidad en la réplica, monitoreada con la métrica `ReplicaLag`. Las escrituras pesadas, las transacciones largas, las réplicas pequeñas y la distancia de red (entre regiones) lo aumentan.

#### ¿Por qué leer de una réplica puede devolver datos desactualizados?

Porque la replicación es asíncrona: una lectura justo después de una escritura puede no verla. Las aplicaciones que necesitan leer sus propias escrituras deben leer de la primaria en ese caso.

#### ¿Se puede promover una réplica de lectura?

Sí. La promoción la convierte en una instancia independiente que acepta escrituras y rompe la replicación. Se usa para la recuperación ante desastres, las migraciones o dividir una base de datos.

#### ¿Para qué sirven las réplicas de lectura entre regiones?

Para atender lecturas cerca de los usuarios en otra región, para la recuperación ante desastres (promoverla si cae la región primaria) y para migrar una base de datos a otra región.

#### ¿Puede una réplica de lectura ser Multi-AZ?

Sí, en los motores compatibles una réplica de lectura puede configurarse como Multi-AZ, lo que mejora su disponibilidad (útil cuando puede promoverse para DR).

#### ¿Las réplicas de lectura requieren backups automáticos en el origen?

Sí. En la mayoría de los motores los backups automáticos deben estar activos en la instancia origen (retención mayor que cero) para crear réplicas de lectura.

#### ¿Cómo se usan las réplicas de lectura para analítica sin afectar la producción?

Apuntando los jobs de reportes y extracción a una réplica dimensionada para consultas analíticas, para que las lecturas largas no compitan con el tráfico OLTP de la primaria; se monitorea el retraso para que los reportes sepan qué tan frescos son los datos.

#### ¿Se puede escribir en una réplica de lectura?

Normalmente no: las réplicas son de solo lectura. En MySQL se puede poner `read_only = 0` en una réplica para casos especiales, como añadir índices para reportes, pero las escrituras pueden romper la replicación y se desaconsejan.

#### ¿Cómo se envían las lecturas a las réplicas?

Desde la aplicación (orígenes de datos separados de lectura y escritura), con un proxy o driver que separe lecturas y escrituras, o con el endpoint de lectura de Aurora, que balancea las conexiones entre réplicas.

#### ¿Qué les pasa a las réplicas cuando el origen hace failover Multi-AZ?

Las réplicas siguen automáticamente a la nueva primaria tras un failover Multi-AZ, porque el endpoint del origen y el flujo de replicación continúan desde la standby.

#### ¿Qué es una réplica con retraso (delayed replica)?

Una réplica (MySQL, MariaDB) configurada para aplicar los cambios con retraso, por ejemplo una hora, para poder recuperarse de errores promoviéndola antes de que se aplique el cambio malo.

### Backups y restauración

#### ¿Qué son los backups automáticos?

Snapshots diarios de la instancia más los logs de transacciones capturados cada pocos minutos, conservados durante un periodo configurable (de 1 a 35 días; 0 los desactiva), que permiten la recuperación a un punto en el tiempo dentro de la ventana de retención.

#### ¿Qué es la recuperación a un punto en el tiempo (PITR)?

Restaurar la base a cualquier segundo dentro del periodo de retención (hasta unos cinco minutos atrás), lo que crea una instancia nueva con un endpoint nuevo. Es la herramienta principal para recuperarse de cambios accidentales.

#### ¿Qué son los snapshots manuales?

Snapshots iniciados por el usuario que se conservan hasta que los borres, independientes de la retención de los backups automáticos. Se usan antes de cambios riesgosos, para retención a largo plazo y para copiar o compartir bases de datos.

#### ¿Se puede restaurar un snapshot sobre la instancia existente?

No. Las restauraciones siempre crean una instancia nueva. Luego apuntas las aplicaciones al nuevo endpoint (o renombras las instancias para reutilizar el nombre del endpoint anterior).

#### ¿Cómo se copian los backups a otra región o cuenta?

Copiando snapshots a otra región (copia entre regiones, opcionalmente automatizada con AWS Backup o con la replicación entre regiones de los backups automáticos) y compartiendo snapshots con otras cuentas (los snapshots cifrados requieren compartir la clave KMS).

#### ¿Qué papel cumple AWS Backup con RDS?

AWS Backup centraliza las políticas de backup entre servicios: programaciones, retención, copias entre regiones y cuentas, vault locks para la inmutabilidad e informes de cumplimiento para RDS y Aurora.

#### ¿Qué pasa con los backups automáticos al borrar una instancia?

Puedes conservarlos (hasta que venza su retención) y tomar un snapshot final. Sin snapshot final ni backups conservados, los datos se pierden; la protección contra borrado y los snapshots finales evitan errores.

#### ¿Los backups afectan el rendimiento?

Con Multi-AZ, los backups se toman desde la standby, así que la primaria no se ve afectada. En las instancias single-AZ, la E/S puede suspenderse brevemente durante el snapshot, lo que puede afectar el rendimiento.

#### ¿Cómo se exportan los datos de RDS a S3 para analítica?

Exportando un snapshot a S3 (RDS escribe las tablas como archivos Parquet, que Athena o Glue pueden consultar), o con exportaciones propias (la extensión `aws_s3` de PostgreSQL, `SELECT INTO OUTFILE S3` en Aurora MySQL, o jobs de Glue/DMS).

#### ¿Cuánto tarda una restauración?

Depende del tamaño y la actividad de la base: crear la instancia desde el snapshot es rápido, pero los datos se cargan de forma diferida desde S3, así que las primeras consultas pueden ser lentas hasta que se lean los bloques (puede hacer falta "calentar" las restauraciones críticas en rendimiento).

#### ¿Qué es la carga diferida (lazy loading) tras una restauración?

Cuando una instancia se restaura desde un snapshot, sus bloques de almacenamiento se traen de S3 en el primer acceso, así que las lecturas iniciales tienen más latencia. Ejecutar lecturas completas de las tablas tras la restauración calienta el almacenamiento.

#### ¿Cómo se conservan backups durante siete años por cumplimiento?

Con AWS Backup y un plan de retención largo con vault lock, o copiando snapshots manuales periódicamente; los backups automáticos llegan a 35 días como máximo. Exportar a S3 con reglas de ciclo de vida también sirve para el archivo.

#### ¿Se puede restaurar una sola tabla desde un backup?

No directamente. Restaura toda la instancia en una nueva (a un punto en el tiempo), luego haz un dump de la tabla necesaria e impórtala en producción.

#### ¿Qué es la replicación entre regiones de los backups automáticos?

Una función que copia los backups automáticos y los logs de transacciones a otra región, para poder hacer recuperación a un punto en el tiempo en la región de DR.

### Seguridad

#### ¿Cómo se controla el acceso de red a RDS?

Ubicando las instancias en subredes privadas, desactivando el acceso público y usando grupos de seguridad de la VPC que solo permitan los grupos de seguridad de la aplicación o rangos CIDR concretos en el puerto de la base. El acceso desde on-premises pasa por VPN o Direct Connect.

#### ¿Cómo se cifran los datos en reposo en RDS?

Con claves de AWS KMS (administradas por AWS o por el cliente), que cubren el almacenamiento, los backups automáticos, los snapshots, las réplicas de lectura y los logs. El cifrado se elige al crear la instancia.

#### ¿Cómo se cifra una instancia de RDS existente sin cifrar?

Tomando un snapshot, copiándolo con cifrado activado con una clave KMS y restaurando una instancia nueva desde la copia cifrada; luego se cambian las aplicaciones a ella. Las réplicas de una instancia sin cifrar no se pueden cifrar directamente.

#### ¿Cómo se cifran los datos en tránsito?

Con conexiones SSL/TLS que usan el paquete de autoridades certificadoras de RDS. Se puede obligar TLS con parámetros como `rds.force_ssl` (PostgreSQL, SQL Server) o `require_secure_transport` (MySQL). Hay que rotar los certificados cuando RDS rota sus CA.

#### ¿Qué es la autenticación de base de datos con IAM?

En MySQL, MariaDB y PostgreSQL (y Aurora), los usuarios se autentican con un token de corta duración generado a partir de credenciales IAM en lugar de una contraseña, de modo que el acceso se controla con políticas IAM y no se guardan contraseñas de base de datos en las aplicaciones.

#### ¿Cómo se deben administrar las contraseñas de la base de datos?

Con Secrets Manager, idealmente con contraseñas del usuario maestro administradas por RDS (RDS crea y rota el secreto), rotando automáticamente los secretos de los usuarios de aplicación y sin escribir nunca credenciales en el código.

#### ¿Qué privilegios tiene el usuario maestro?

Privilegios administrativos amplios dentro de los límites del motor (por ejemplo `rds_superuser` en PostgreSQL), pero no superusuario completo ni acceso al sistema operativo. Crea usuarios aparte con el mínimo privilegio para las aplicaciones y los pipelines.

#### ¿Cómo se audita la actividad de la base de datos?

Con los logs del motor (`pgaudit` en PostgreSQL, el plugin de auditoría de MySQL, la auditoría de SQL Server, la auditoría unificada de Oracle) publicados en CloudWatch Logs, CloudTrail para las llamadas a la API de RDS, y Database Activity Streams para la actividad casi en tiempo real enviada a Kinesis (para herramientas de cumplimiento).

#### ¿Qué son los Database Activity Streams?

Una función (para Aurora y algunos motores de RDS) que envía un flujo en tiempo real de la actividad de la base a Kinesis Data Streams, cifrado con KMS y fuera del control de los DBA, para monitoreo y cumplimiento.

#### ¿Cómo se protege RDS de cambios accidentales hechos por personas?

Con IAM de mínimo privilegio sobre las APIs de RDS, protección contra borrado, cuentas o roles separados para producción, gestión de cambios con infraestructura como código y auditorías de quién puede modificar instancias y parameter groups.

#### ¿Cómo se restringe qué usuarios IAM pueden crear o modificar instancias de RDS?

Con políticas IAM sobre las acciones de RDS (`rds:CreateDBInstance`, `rds:ModifyDBInstance`, `rds:DeleteDBInstance`), condiciones sobre etiquetas y service control policies de AWS Organizations como barreras, por ejemplo para exigir cifrado.

#### ¿Cómo se impide crear bases de datos sin cifrar?

Con una SCP o una condición IAM `rds:StorageEncrypted = true` en las acciones de creación, reglas de AWS Config (`rds-storage-encrypted`) para detectar incumplimientos y valores por defecto en la infraestructura como código.

#### ¿Qué es la autenticación Kerberos en RDS?

La integración con AWS Managed Microsoft AD (o un AD propio mediante una relación de confianza) para que los usuarios inicien sesión en SQL Server, Oracle, PostgreSQL o MySQL con sus credenciales del directorio y una gestión centralizada de cuentas.

#### ¿Cómo se limita el acceso de red de Lambda a RDS?

Ejecutando Lambda dentro de la VPC con su propio grupo de seguridad, permitiendo solo ese grupo en el puerto de la base, y usando RDS Proxy con autenticación IAM para no guardar contraseñas en la función.

#### ¿Cómo se comparte un snapshot cifrado con otra cuenta?

Usando una clave KMS administrada por el cliente (los snapshots cifrados con la clave administrada por AWS no se pueden compartir), dándole acceso a la clave a la otra cuenta y compartiendo el snapshot; la otra cuenta lo copia con su propia clave.

#### ¿Cuál es una buena práctica para los usuarios de base de datos de las aplicaciones?

Un usuario por aplicación o servicio con solo los privilegios que necesita (a menudo `SELECT`, `INSERT`, `UPDATE`, `DELETE` a nivel de esquema, sin DDL), usuarios de solo lectura aparte para los reportes, y el DDL a cargo de las herramientas de migración con otro usuario.

### Monitoreo y rendimiento

#### ¿Qué métricas de CloudWatch son las más importantes en RDS?

`CPUUtilization`, `FreeableMemory`, `FreeStorageSpace`, `ReadIOPS`/`WriteIOPS`, `ReadLatency`/`WriteLatency`, `DiskQueueDepth`, `DatabaseConnections`, `ReplicaLag`, `SwapUsage` y, en las clases ampliables, `CPUCreditBalance`.

#### ¿Qué es Enhanced Monitoring?

Métricas a nivel de sistema operativo (CPU y memoria por proceso, sistema de archivos, swap, E/S de disco) recogidas por un agente a intervalos de hasta un segundo y enviadas a CloudWatch Logs, que ayudan a encontrar causas que las métricas estándar no muestran.

#### ¿Qué es Performance Insights / Database Insights?

Una herramienta de rendimiento que muestra la carga de la base (sesiones activas promedio) desglosada por eventos de espera, sentencias SQL, usuarios y hosts, para ver qué consultas causan carga y por qué. Hoy forma parte de CloudWatch Database Insights, que en su modo avanzado añade vistas de toda la flota y más retención.

#### ¿Cómo se encuentran las consultas lentas en RDS?

Activando los logs de consultas lentas (`slow_query_log` y `long_query_time` en MySQL, `log_min_duration_statement` en PostgreSQL), usando `pg_stat_statements` o Performance Schema, y analizando el top SQL de Database Insights; después se ejecuta `EXPLAIN` para corregir planes e índices.

#### ¿Qué son las notificaciones de eventos de RDS?

Notificaciones enviadas por EventBridge o SNS ante eventos como failovers, reinicios, poco almacenamiento, backups, cambios de configuración y mantenimiento, usadas para alertas y automatización.

#### ¿Qué causa una CPU alta en una instancia de RDS?

Consultas ineficientes (índices faltantes, lecturas completas, malos planes), demasiadas conexiones concurrentes, reportes pesados sobre la primaria, contención de bloqueos o una instancia pequeña. Primero encuentra el top SQL, luego ajusta o escala.

#### ¿Qué causa quedarse sin conexiones?

Aplicaciones sin pooling que abren muchas conexiones (las funciones serverless son un caso clásico), conexiones que se filtran, un `max_connections` bajo para la memoria de la instancia o un pico de tráfico. Usa pooling (RDS Proxy, PgBouncer) y corrige las fugas.

#### ¿Qué es RDS Proxy?

Un proxy de base de datos administrado que agrupa y comparte conexiones entre las aplicaciones y RDS o Aurora, reduce el costo de abrir conexiones (sobre todo desde Lambda), acelera el failover manteniendo las conexiones de los clientes y redirigiéndolas, y admite autenticación IAM y Secrets Manager.

#### ¿Cuándo conviene usar RDS Proxy?

Con Lambda u otros clientes muy concurrentes y de vida corta, aplicaciones que abren muchas conexiones, o cuando quieres un failover más rápido y transparente. Añade costo y algo de latencia, y algunas funciones de sesión (pinning) reducen su beneficio.

#### ¿Cómo se ajusta PostgreSQL en RDS?

Ajustando parámetros en un parameter group propio (`shared_buffers`, `work_mem`, `maintenance_work_mem`, `effective_cache_size`, los ajustes de autovacuum, `max_connections`), manteniendo las estadísticas al día, añadiendo los índices adecuados, vigilando el bloat y las transacciones largas, y usando `pg_stat_statements`.

#### ¿Cómo se ajusta MySQL en RDS?

Dimensionando `innodb_buffer_pool_size` (por defecto alrededor del 75 % de la memoria), revisando `max_connections`, usando índices y planes adecuados, vigilando el log de consultas lentas y evitando transacciones largas que hacen crecer los undo logs.

#### ¿Por qué importa el autovacuum en RDS PostgreSQL?

El MVCC de PostgreSQL deja tuplas muertas tras los updates y deletes; el autovacuum las recupera y evita el wraparound del ID de transacción. Si se atrasa, las tablas se inflan y, en el peor caso, la base deja de aceptar escrituras para evitar el wraparound. Ajústalo para las tablas grandes y activas.

#### ¿Qué es `FreeableMemory` y cuándo debe preocuparte?

La RAM disponible en la instancia. Poca memoria libre con un `SwapUsage` en aumento significa que la carga no cabe (buffer pool, conexiones, ordenamientos); escala o reduce el consumo de memoria.

#### ¿Cómo aparecen los bloqueos en las herramientas de rendimiento de RDS?

Como eventos de espera (por ejemplo `Lock:transactionid` o `Lock:relation` en PostgreSQL, `synch/cond/innodb/row_lock_wait` en MySQL) en Database Insights; consultas sobre `pg_locks` con `pg_stat_activity` muestran quién bloquea a quién.

#### ¿Cómo se encuentran los índices sin uso en PostgreSQL en RDS?

Consultando `pg_stat_user_indexes` para los índices con `idx_scan = 0` durante un periodo largo (excluyendo los de restricciones) y borrándolos tras verificar, porque cuestan rendimiento de escritura y almacenamiento.

#### ¿Cómo se identifican las transacciones largas en PostgreSQL?

Consultando `pg_stat_activity` para las sesiones con un `xact_start` antiguo, sobre todo `idle in transaction`; bloquean el vacuum y causan bloat. Define `idle_in_transaction_session_timeout` para proteger la base.

#### ¿Qué logs puede publicar RDS en CloudWatch Logs?

Logs de errores, de consultas lentas, generales (MySQL), los logs de PostgreSQL (incluida la salida de `log_min_duration_statement` y de `pgaudit`), logs de auditoría, de actualización y del agente, según el motor y la configuración.

#### ¿Cómo se generan alertas sobre problemas de RDS?

Con alarmas de CloudWatch sobre CPU, almacenamiento libre, memoria libre, conexiones, retraso de réplica, latencias de lectura y escritura y saldo de ráfaga; reglas de EventBridge sobre los eventos de RDS (failover, almacenamiento lleno, mantenimiento); y la detección de anomalías de Database Insights.

### Escalado

#### ¿Cómo se escala verticalmente una instancia de RDS?

Modificando la clase de instancia (por ejemplo de `db.r6g.large` a `db.r6g.2xlarge`), de inmediato o en la ventana de mantenimiento. Requiere una breve interrupción, que Multi-AZ acorta (se modifica primero la standby y luego hay failover).

#### ¿Cómo se escalan las lecturas?

Añadiendo réplicas de lectura (o Aurora Replicas) y enviándoles el tráfico de solo lectura, cacheando las lecturas frecuentes con ElastiCache y usando las standby legibles de los clusters Multi-AZ.

#### ¿Cómo se escalan las escrituras más allá de una sola instancia?

Escalando la instancia, optimizando los patrones de escritura (lotes, menos índices, particionado), moviendo partes de la carga a otras bases (DynamoDB para accesos clave-valor) o haciendo sharding de los datos entre instancias desde la aplicación. Aurora Limitless Database (PostgreSQL) y Aurora DSQL ofrecen opciones administradas de escalado horizontal.

#### ¿Qué es el particionado de tablas y ayuda en RDS?

Dividir tablas grandes en particiones (particionado declarativo de PostgreSQL, particionado de MySQL) por rango o lista, lo que acelera las consultas que filtran por la clave de partición y abarata archivar los datos viejos (se borra una partición en lugar de filas).

#### ¿Cómo se comportan las instancias ampliables bajo carga sostenida?

Las instancias `db.t*` acumulan créditos de CPU cuando están ociosas y los gastan bajo carga; con una CPU alta sostenida, agotan los créditos y se limitan (modo estándar) o facturan de más (modo ilimitado). No sirven para cargas de producción estables.

#### ¿Cómo se escala el rendimiento del almacenamiento sin cambiar la instancia?

Con gp3, subiendo IOPS y rendimiento de forma independiente; con io1/io2, subiendo las IOPS aprovisionadas; comprobando que el ancho de banda EBS de la clase de instancia no sea el cuello de botella.

#### ¿Qué límites de la instancia pueden frenar la E/S?

Cada clase de instancia tiene un ancho de banda EBS y unas IOPS máximas; una clase pequeña no puede aprovechar IOPS aprovisionadas muy altas. Elige una clase cuyos límites correspondan a la configuración del almacenamiento.

#### ¿Cómo ayuda la caché a una base de datos RDS?

ElastiCache (Redis o Memcached) o las cachés de la aplicación sirven desde memoria las lecturas repetidas (sesiones, catálogos de productos, resultados calculados), reduciendo la carga y la latencia de la base. La estrategia de invalidación es la parte difícil.

#### ¿Cuándo conviene dividir una base de datos en varias?

Cuando distintos dominios o servicios tienen cargas, necesidades de escalado o responsables independientes, cuando los picos de una carga afectan a otras, o por el principio de microservicios de una base de datos por servicio.

### Aurora

#### ¿Qué es Amazon Aurora?

Una base de datos relacional compatible con MySQL y PostgreSQL construida para la nube, con una capa de almacenamiento distribuida y tolerante a fallos compartida por el escritor y las réplicas. Ofrece más rendimiento que los motores estándar, un failover más rápido y un almacenamiento que crece automáticamente.

#### ¿Cómo funciona el almacenamiento de Aurora?

Los datos se guardan en un volumen de cluster replicado seis veces en tres zonas de disponibilidad, en segmentos de 10 GB. Las escrituras necesitan cuatro de seis copias y las lecturas tres de seis, así que el cluster tolera perder una AZ más otra copia. El almacenamiento escala solo hasta 128 TiB.

#### ¿Qué es un cluster de Aurora?

Una instancia escritora (primaria) y hasta 15 Aurora Replicas que comparten el mismo volumen, con un endpoint de cluster (escritor), un endpoint de lectura (balanceado entre réplicas) y endpoints personalizados opcionales para subconjuntos de instancias.

#### ¿En qué se diferencia el failover de Aurora del Multi-AZ de RDS?

Una Aurora Replica se puede promover porque comparte el mismo almacenamiento, así que no hay datos que alcanzar y el failover suele tardar unos 30 segundos o menos. El retraso de las réplicas suele ser de milisegundos.

#### ¿Qué es Aurora Serverless v2?

Un modo de capacidad en el que las instancias de Aurora escalan su capacidad automáticamente, en unidades finas llamadas Aurora Capacity Units (ACU), según la carga, entre un mínimo y un máximo, y en algunas configuraciones pueden bajar a cero. Sirve para cargas variables o impredecibles.

#### ¿Qué es Aurora Global Database?

Una configuración con una región primaria y varias regiones secundarias, replicadas a nivel de almacenamiento con normalmente menos de un segundo de retraso. Las secundarias atienden lecturas locales y se pueden promover ante una caída regional (failover administrado o switchover).

#### ¿Qué es el clonado rápido de Aurora?

Crear un cluster nuevo que comparte las páginas de almacenamiento del origen con copy-on-write, de modo que el clon se crea rápido y solo las páginas modificadas usan almacenamiento nuevo. Es ideal para pruebas, analítica sobre una copia o refrescar preproducción.

#### ¿Qué es Aurora Backtrack?

Una función de Aurora MySQL que retrocede el cluster en su lugar a un momento anterior dentro de una ventana configurada, sin restaurar desde un backup, útil para deshacer errores rápidamente.

#### ¿Qué son Aurora Standard y Aurora I/O-Optimized?

Dos configuraciones de almacenamiento: Standard factura las solicitudes de E/S aparte (más barato con poca E/S), I/O-Optimized incluye la E/S en un precio mayor de almacenamiento e instancia (más barato cuando la E/S supera aproximadamente un cuarto del costo de la base).

#### ¿Qué es la integración zero-ETL de Aurora con Redshift?

Una integración administrada que replica los datos de Aurora (y de algunos motores de RDS) en Amazon Redshift casi en tiempo real sin construir pipelines, para hacer analítica en Redshift con datos operativos frescos.

#### ¿Qué es Babelfish for Aurora PostgreSQL?

Una capacidad que permite a Aurora PostgreSQL entender el T-SQL y el protocolo TDS de SQL Server, para que las aplicaciones escritas para SQL Server funcionen con menos cambios de código.

#### ¿Qué es la Data API de Aurora?

Una API HTTP para ejecutar SQL sobre Aurora (Serverless v2 y aprovisionado) sin administrar conexiones ni drivers, cómoda para Lambda y otras aplicaciones serverless.

#### ¿Qué es Aurora DSQL?

Una base de datos SQL distribuida y serverless compatible con PostgreSQL, diseñada para aplicaciones activo-activo multirregión, que escala lecturas y escrituras horizontalmente con consistencia fuerte. Es distinta del Aurora estándar y tiene algunas limitaciones de funciones de PostgreSQL.

#### ¿Cuándo elegirías Aurora en lugar de RDS para PostgreSQL o MySQL?

Cuando necesitas más rendimiento, un failover más rápido, muchas réplicas con poco retraso, replicación global, clonado rápido o escalado serverless. El RDS estándar puede ser más barato para cargas pequeñas o estables y a veces admite antes ciertas funciones o versiones del motor.

#### ¿Qué son los endpoints personalizados de Aurora?

Endpoints que apuntan a un subconjunto elegido de las instancias de un cluster, por ejemplo réplicas más grandes para consultas analíticas y más pequeñas para las lecturas de la aplicación.

#### ¿Cuál es la limitación del endpoint de lectura de Aurora?

Balancea las conexiones nuevas entre réplicas mediante DNS, no las consultas individuales; las conexiones de larga duración se quedan en una réplica, así que la carga puede quedar desigual. Ayudan los pools que reciclan conexiones periódicamente o los proxies.

#### ¿Qué es Aurora parallel query?

Una función de Aurora MySQL que empuja partes de las consultas analíticas (filtros, agregaciones) a la capa de almacenamiento, sobre miles de nodos, lo que acelera algunas consultas analíticas sobre tablas grandes sin un warehouse aparte.

#### ¿Qué son las Aurora Optimized Reads?

Una función en instancias con almacenamiento NVMe local que lo usa como caché escalonada y para objetos temporales, mejorando la latencia de cargas de lectura cuyos datos superan la memoria y de consultas con tablas temporales grandes.

#### ¿Cómo maneja Aurora los backups?

De forma continua e incremental hacia S3 sin impacto en el rendimiento, con recuperación a un punto en el tiempo dentro del periodo de retención (1–35 días); los snapshots son a nivel de cluster.

#### ¿Qué es Aurora Limitless Database?

Una capacidad de Aurora PostgreSQL que escala las escrituras horizontalmente repartiendo (sharding) las tablas entre varias instancias detrás de un solo endpoint, para cargas que superan la capacidad de un escritor.

#### ¿Qué es la prioridad de failover (tier) de Aurora?

Un ajuste (tier 0–15) en cada réplica que decide qué réplica se promueve primero en un failover; entre réplicas con el mismo rango se elige por tamaño.

#### ¿Se pueden mezclar Aurora Serverless v2 e instancias aprovisionadas?

Sí. Un cluster puede tener un escritor aprovisionado y lectores Serverless v2 (o al revés), lo que es útil con tráfico de lectura variable.

### Motores y funciones

#### ¿Qué extensiones de PostgreSQL son útiles en RDS?

`pg_stat_statements` (estadísticas de consultas), `PostGIS` (geoespacial), `pgvector` (búsqueda vectorial), `pg_partman` (gestión de particiones), `pg_cron` (jobs programados), `aws_s3` (importar/exportar con S3), `pgaudit`, `pg_repack` y `postgres_fdw`. Solo se pueden instalar las extensiones admitidas.

#### ¿Cómo se cargan datos desde S3 en RDS PostgreSQL?

Con la extensión `aws_s3`: `SELECT aws_s3.table_import_from_s3('tabla', 'col1,col2', '(format csv, header true)', aws_commons.create_s3_uri('bucket', 'archivo.csv', 'eu-west-1'));`, con un rol IAM asociado a la instancia.

#### ¿Qué es un despliegue Blue/Green?

Una función (MySQL, MariaDB, PostgreSQL, Aurora) que crea una copia de staging (green) sincronizada con producción (blue) mediante replicación lógica, te deja actualizarla o cambiarla y luego hace el cambio en alrededor de un minuto con salvaguardas, conservando los mismos endpoints.

#### ¿Cómo se actualiza la versión mayor de un motor de RDS?

Probando la actualización sobre una restauración de snapshot, revisando la compatibilidad de extensiones y parámetros, y luego actualizando en su lugar (con interrupción) o usando despliegues Blue/Green para una interrupción mínima. Toma un snapshot antes de actualizar.

#### ¿Qué son las actualizaciones automáticas de versión menor?

Una opción en la que RDS aplica automáticamente las versiones menores del motor (correcciones de errores y de seguridad) durante la ventana de mantenimiento. La mayoría de los equipos la activa, a veces tras probar en entornos inferiores.

#### ¿Qué es RDS Extended Support?

Una oferta de pago que sigue entregando parches críticos para versiones mayores de los motores después de su fin de vida en la comunidad, dando tiempo extra para actualizar. Las instancias en esas versiones se inscriben automáticamente salvo que se actualicen.

#### ¿Cómo se programan jobs dentro de RDS PostgreSQL?

Con `pg_cron` para jobs SQL dentro de la base, o desde fuera con EventBridge Scheduler, Lambda o un orquestador. El trabajo batch pesado suele ir mejor fuera de la base OLTP.

#### ¿Qué restricciones tiene SQL Server en RDS?

Sin rol `sysadmin`, funciones limitadas en algunas ediciones, procedimientos específicos para el backup y restore nativos (vía S3), límites en el número de bases por instancia y límites de tamaño de almacenamiento; RDS Custom for SQL Server levanta algunos.

#### ¿Qué opciones de licenciamiento hay para Oracle y SQL Server en RDS?

License Included (la licencia va en el precio por hora) o Bring Your Own License para Oracle; SQL Server suele ser License Included, eligiendo la edición (Express, Web, Standard, Enterprise).

#### ¿Cómo se usa `pgvector` en RDS PostgreSQL?

Instalando la extensión, creando columnas `vector` para los embeddings e indexándolas con índices HNSW o IVFFlat para búsquedas por similitud, lo que permite hacer generación aumentada por recuperación sin una base vectorial aparte.

#### ¿Para qué se usa la replicación lógica en RDS PostgreSQL?

Para replicar tablas seleccionadas a otra base PostgreSQL (actualizaciones, migraciones, dividir bases o alimentar analítica), CDC hacia sistemas externos y los despliegues Blue/Green.

#### ¿Qué ventajas tienen las funciones de MySQL 8.0+ en RDS para el trabajo con datos?

Funciones de ventana, CTE (incluidas las recursivas), funciones JSON, índices invisibles, `ADD COLUMN` instantáneo en muchos cambios y mejores estadísticas del optimizador, que facilitan las consultas analíticas y los cambios de esquema.

#### ¿Cómo se ejecutan migraciones de esquema seguras sobre tablas grandes?

Usando operaciones compatibles con el trabajo en línea (DDL instantáneo en MySQL 8, `CREATE INDEX CONCURRENTLY` en PostgreSQL), herramientas como `gh-ost` o `pt-online-schema-change` para MySQL, despliegues Blue/Green, y midiendo el tiempo de la migración sobre un clon.

### Costos

#### ¿Qué impulsa los costos de RDS?

Las horas de instancia (por clase; Multi-AZ duplica el cómputo), el almacenamiento (por tipo y tamaño, más las IOPS aprovisionadas), el almacenamiento de backups por encima del gratuito, la transferencia de datos de salida y entre AZ o regiones, las tarifas de Extended Support, y funciones como RDS Proxy y el modo avanzado de Database Insights.

#### ¿Cómo se reducen los costos de RDS?

Dimensionando bien las instancias según las métricas, usando clases Graviton, comprando Reserved Instances para las cargas estables, usando gp3 en lugar de io1 sobreaprovisionado, deteniendo de noche las instancias que no son de producción, limpiando los snapshots viejos, usando Aurora Serverless v2 o I/O-Optimized donde encajen y descargando lecturas en cachés.

#### ¿Cuánto cuesta Multi-AZ?

Aproximadamente el doble del costo de la instancia, porque una instancia standby corre en otra AZ, más el almacenamiento replicado. Suele justificarse en producción; los entornos que no son de producción suelen ir en single-AZ.

#### ¿Qué son las Reserved Instances de RDS?

Un compromiso de uno o tres años con una familia de clases de instancia en una región a cambio de un descuento importante frente al precio bajo demanda, con flexibilidad de tamaño dentro de una familia para la mayoría de los motores.

#### ¿Cómo se encuentran instancias de RDS ociosas o sobredimensionadas?

Con métricas de CloudWatch (CPU, conexiones, IOPS) durante semanas, las recomendaciones de AWS Compute Optimizer para RDS, los controles de Trusted Advisor de instancias ociosas y los informes de costos por etiqueta.

#### ¿Cuánto cuesta el almacenamiento de backups?

El almacenamiento de backups hasta el tamaño del almacenamiento aprovisionado de la región está incluido; por encima de eso, y por los snapshots manuales conservados mucho tiempo, se paga por GB-mes. Los snapshots manuales viejos son un costo oculto frecuente.

#### ¿Cómo afectan a RDS los costos de transferencia entre AZ?

La replicación Multi-AZ no se cobra, pero el tráfico de la aplicación entre una instancia en una AZ y clientes en otra, y la replicación entre regiones, generan cargos de transferencia de datos.

#### ¿Cómo se ahorra en las bases de desarrollo?

Usando instancias pequeñas o ampliables, single-AZ, programando que se detengan fuera del horario laboral, usando Aurora Serverless v2 con un mínimo bajo, restaurando desde snapshots compartidos en lugar de mantener muchas copias y borrando los entornos sin uso.

### Migración e ingeniería de datos

#### ¿Cómo se migra una base de datos a RDS?

Con el mismo motor: dump y restore nativos (`pg_dump`/`pg_restore`, `mysqldump`, backup de SQL Server a S3 y restore), o replicación del origen hacia RDS para una interrupción mínima. Con motores distintos o replicación continua: AWS DMS, con el Schema Conversion Tool (o DMS Schema Conversion) para traducir el esquema.

#### ¿Qué es AWS DMS?

Database Migration Service: replica datos de una base origen a un destino (otra base, S3, Redshift, Kinesis y otros) con una carga completa y captura de cambios continua (CDC), sobre instancias de replicación o DMS Serverless.

#### ¿Cómo se capturan los cambios (CDC) de RDS MySQL?

Activando el binary log con `binlog_format = ROW` (y row image completa), manteniendo suficiente retención del binlog (`mysql.rds_set_configuration('binlog retention hours', 24)`) y leyendo los cambios con DMS, Debezium o una integración zero-ETL.

#### ¿Cómo se capturan los cambios de RDS PostgreSQL?

Activando la replicación lógica (`rds.logical_replication = 1`), creando un slot de replicación y una publicación, y consumiendo con DMS, Debezium (plugin pgoutput) o zero-ETL. Vigila los slots: un slot que nadie consume retiene WAL y puede llenar el disco.

#### ¿Por qué los slots de replicación son peligrosos en PostgreSQL?

Un slot obliga a PostgreSQL a conservar el WAL hasta que el consumidor lo confirme. Si un consumidor de CDC se detiene, el WAL se acumula (`TransactionLogsDiskUsage` crece) hasta llenar el almacenamiento y detener la base. Crea alertas sobre el retraso de los slots y borra los abandonados.

#### ¿Cómo se extraen tablas grandes de RDS sin afectar la producción?

Leyendo de una réplica o de un clon o restauración reciente, exportando snapshots a S3 como Parquet, extrayendo de forma incremental por una columna updated-at o con CDC en lugar de extracciones completas, en paralelo por rangos de clave con límites, y fuera de las horas pico.

#### ¿Qué es la exportación de snapshots a S3?

Una función de RDS que exporta los datos de un snapshot a S3 en formato Parquet, particionados por tabla, sin afectar la base en marcha, listos para catalogarse con Glue y consultarse con Athena.

#### ¿Cómo leen los jobs de Glue desde RDS?

Mediante una conexión JDBC de Glue en la VPC de la base (con acceso de subred y grupo de seguridad), leyendo las tablas en paralelo con opciones de particionado y guardando las credenciales en Secrets Manager; los bookmarks o una columna de marca de agua dan las cargas incrementales.

#### ¿Cómo se cargan datos en RDS de forma eficiente?

Con carga masiva (`COPY` en PostgreSQL, `LOAD DATA` en MySQL, la extensión `aws_s3`), inserciones por lotes, desactivando o aplazando la creación de índices secundarios en las cargas iniciales, subiendo temporalmente `maintenance_work_mem` y evitando las inserciones fila por fila por la red.

#### ¿Conviene ejecutar analítica directamente en la instancia RDS de producción?

En general no. Las consultas analíticas compiten con el tráfico OLTP por CPU, memoria y E/S. Usa una réplica de lectura para reportes ligeros y, para analítica más pesada, mueve los datos a un warehouse o lakehouse con CDC, exportaciones o zero-ETL.

#### ¿Qué diferencia hay entre OLTP y OLAP, y dónde encaja RDS?

OLTP maneja muchas transacciones pequeñas (inserciones, actualizaciones, búsquedas puntuales) con consistencia fuerte; OLAP maneja lecturas grandes y agregaciones sobre el historial. RDS está hecho para OLTP; el OLAP va en Redshift, Snowflake, Databricks o Athena sobre un data lake.

#### ¿Qué es DMS Schema Conversion?

Una función administrada de DMS (sucesora del Schema Conversion Tool de escritorio en muchos casos) que evalúa y convierte esquemas y código entre motores, e informa los elementos que requieren trabajo manual.

#### ¿Cómo maneja DMS las tablas grandes en la carga completa?

Con carga paralela por particiones o rangos de una columna, ajustes para los objetos grandes (LOB) y mapeos de tablas para seleccionar y transformar; las migraciones muy grandes pueden combinar una exportación masiva nativa con el CDC de DMS desde una posición conocida.

#### ¿Cómo se valida una migración?

Con la validación de datos de DMS (comparación fila por fila), conteos de filas y checksums por tabla, comparación de agregados (sumas, mínimos/máximos por rangos de clave), pruebas de la aplicación contra el destino y un periodo de funcionamiento en paralelo.

#### ¿Cuáles son las trampas comunes del CDC desde bases relacionales?

Tablas sin clave primaria (no se pueden aplicar updates), retención de logs insuficiente, transacciones grandes que generan retraso, cambios de esquema que no se propagan, diferencias de tipos (timestamps, decimales) y borrados que no se manejan después.

#### ¿Cómo se envían los cambios de RDS a Kafka?

Con Debezium sobre Kafka Connect (o Amazon MSK Connect) leyendo el binlog o la replicación lógica, produciendo un topic por tabla con los eventos de cambio, o con DMS apuntando a Kinesis o MSK.

#### ¿Cómo se llevan los datos de RDS a un data lake?

Cargas completas con la exportación de snapshots a S3 o la carga completa de DMS, y luego los cambios incrementales con el CDC de DMS hacia S3 (Parquet con columnas de operación) o zero-ETL; los cambios se aplican a tablas Iceberg/Delta con `MERGE` y todo se cataloga en Glue.

#### ¿Qué es una extracción incremental por marca de agua y qué riesgos tiene?

Seleccionar las filas cuyo `updated_at` supera el último valor extraído. No ve los borrados, las filas actualizadas sin cambiar la marca de tiempo ni las filas confirmadas tarde con una marca anterior; usa una ventana de solapamiento y conciliaciones periódicas, o CDC.

#### ¿Cómo se evita bloquear tablas de producción al extraer?

Usando snapshots o réplicas, leyendo con aislamiento de snapshot consistente sin bloqueos (MVCC de PostgreSQL, lecturas consistentes de InnoDB), evitando `SELECT … FOR UPDATE` y las transacciones largas, y paginando por clave.

### SQL y diseño de bases de datos en RDS

#### ¿Por qué importan tanto las claves primarias en las tablas de RDS?

Garantizan la identidad de cada fila, muchas herramientas de replicación y CDC las necesitan para aplicar updates y deletes, y en InnoDB definen el agrupamiento físico de la tabla. Toda tabla debería tener una.

#### ¿Claves naturales o claves sustitutas?

Las claves sustitutas (autoincrementales, identity o UUID) son estables y compactas; las naturales (correo, número de documento) pueden cambiar y a menudo son sensibles. Usa claves primarias sustitutas con restricciones de unicidad sobre las naturales.

#### ¿UUID o enteros como claves primarias?

Los enteros son más pequeños y mantienen las inserciones secuenciales (bueno para los índices B-tree y el agrupamiento de InnoDB). Los UUID aleatorios dispersan las inserciones e inflan los índices; los UUID ordenados por tiempo (UUIDv7) dan unicidad entre sistemas con mejor localidad.

#### ¿Qué es la normalización y por qué importa en OLTP?

Organizar las tablas para que cada hecho se guarde una sola vez (formas normales), lo que evita anomalías de actualización y mantiene las transacciones pequeñas y coherentes. Las bases OLTP suelen normalizarse hasta la tercera forma normal; la analítica desnormaliza después.

#### ¿Cómo aceleran los índices las consultas y qué cuestan?

Los índices B-tree permiten encontrar filas por clave sin leer toda la tabla y ayudan a ordenar y unir; cada índice ralentiza las escrituras y usa almacenamiento, así que indexa las columnas de los filtros, joins y ordenamientos frecuentes, no todo.

#### ¿Qué es un índice compuesto y por qué importa el orden de las columnas?

Un índice sobre varias columnas que se usa de izquierda a derecha: un índice sobre `(customer_id, created_at)` sirve para filtros sobre `customer_id` y sobre `customer_id` con un rango de `created_at`, pero no sobre `created_at` solo.

#### ¿Qué niveles de aislamiento usan por defecto los motores de RDS?

PostgreSQL usa read committed por defecto; InnoDB de MySQL usa repeatable read. Entenderlos importa para la coherencia de las extracciones y el comportamiento ante la concurrencia.

#### ¿Cómo se evitan los deadlocks?

Accediendo a las tablas y filas en un orden coherente, manteniendo cortas las transacciones, indexando las claves foráneas y las columnas de filtro para bloquear menos filas, y reintentando las transacciones que fallan por deadlock.

#### ¿Qué son los borrados lógicos (soft deletes) y por qué importan para los pipelines?

Marcar las filas como borradas (`deleted_at`) en lugar de eliminarlas. Hacen visibles los borrados para la extracción incremental, pero las aplicaciones y los pipelines deben filtrarlos de forma coherente.

#### ¿Por qué añadir columnas `created_at` y `updated_at` a todas las tablas?

Sirven para la auditoría, la extracción incremental, la depuración y los controles de calidad de datos; `updated_at` debe mantenerse en cada cambio desde la aplicación o con un trigger.

### Escenarios

#### Diseña una base PostgreSQL de alta disponibilidad para una aplicación de producción.

RDS for PostgreSQL (o Aurora PostgreSQL) en subredes privadas en varias AZ con Multi-AZ (o un cluster Multi-AZ), cifrado con una clave KMS administrada por el cliente, TLS obligatorio, secretos administrados por RDS con rotación, RDS Proxy para el pooling de conexiones, backups automáticos con 14–35 días de retención más copias con AWS Backup a otra región, Database Insights, alarmas sobre las métricas clave y protección contra borrado, todo definido como infraestructura como código.

#### El equipo de la aplicación reporta errores intermitentes de "too many connections". ¿Qué haces?

Comparo `DatabaseConnections` con `max_connections`, busco los clientes que abren conexiones de más (Lambda sin pooling, pools sin límites, fugas), introduzco RDS Proxy o un pool en la aplicación con límites razonables, cierro las conexiones ociosas y dimensiono la instancia si la memoria permite más conexiones.

#### Un reporte nocturno vuelve lenta la base de producción. ¿Cómo lo corriges?

Llevo el reporte a una réplica de lectura (o a un clon), optimizo sus consultas e índices, o muevo los datos a un almacén analítico con CDC. Si debe quedarse, lo programo fuera de las horas pico y limito sus recursos.

#### Alguien borró filas de una tabla importante hace 30 minutos. ¿Cómo las recuperas?

Uso la recuperación a un punto en el tiempo para restaurar una instancia nueva justo antes del borrado, extraigo de ella las filas borradas y las vuelvo a insertar en producción (o cambio a la nueva instancia si conviene). Después reviso los privilegios y añado salvaguardas.

#### Debes migrar una base Oracle de 2 TB a Aurora PostgreSQL con una interrupción mínima. ¿Cómo?

Evalúo con el Schema Conversion Tool, convierto el esquema y el código (PL/SQL a PL/pgSQL), ejecuto la carga completa de DMS más CDC para mantener el destino sincronizado, valido los datos (validación de DMS, conteos, checksums) y el comportamiento de la aplicación, y hago el corte en una ventana corta: detengo las escrituras, dejo que el CDC se ponga al día y cambio las conexiones.

#### El uso de disco de RDS PostgreSQL no deja de crecer aunque los datos no cambian. ¿Por qué?

Posibles causas: un slot de replicación lógica inactivo que retiene WAL, bloat de tablas e índices por un autovacuum atrasado, archivos temporales grandes de consultas pesadas, o una retención de logs larga. Reviso `pg_replication_slots`, las estimaciones de bloat, `TransactionLogsDiskUsage` y la configuración de los logs.

#### ¿Cómo le das al equipo de analítica acceso diario a copias frescas de los datos de producción?

Con el clonado rápido de Aurora o restauraciones de snapshots para crear una copia aparte cada día (enmascarada si hace falta), exportando snapshots a S3 como Parquet para Athena, o configurando zero-ETL hacia Redshift para analítica casi en tiempo real sin tocar la producción.

#### ¿Cómo le explicarías RDS a una persona no técnica?

Es AWS operando nuestras bases de datos por nosotros: las mantiene actualizadas, respaldadas y disponibles aunque falle un servidor, para que el equipo se concentre en los datos y en la aplicación en lugar de mantener máquinas.

#### Una API basada en Lambda satura de conexiones la base durante los picos de tráfico. ¿Cuál es tu solución?

Pongo RDS Proxy entre Lambda y la base con autenticación IAM, defino concurrencia reservada en la función para limitar el paralelismo, reutilizo las conexiones entre invocaciones y considero cachear las lecturas más frecuentes.

#### El retraso de una réplica de reportes llega a horas durante los batches nocturnos. ¿Qué haces?

Busco las escrituras pesadas en la primaria (jobs batch, transacciones grandes) y las divido en transacciones más pequeñas, subo la clase de instancia y las IOPS de la réplica, evito en la réplica consultas largas que choquen con la reproducción (`max_standby_streaming_delay` en PostgreSQL) y considero una copia analítica aparte.

#### Tu equipo debe pasar de PostgreSQL 13 a 16 con una interrupción mínima. ¿Cómo lo planificas?

Reviso la compatibilidad de extensiones y parámetros, pruebo la actualización sobre un snapshot restaurado y ejecuto las pruebas de la aplicación, y luego uso un despliegue Blue/Green: creo el entorno green, lo actualizo, dejo que se sincronice, valido y hago el cambio en una ventana corta, conservando el blue como reversión hasta estar seguro.

#### Una revisión de seguridad encuentra una instancia de RDS accesible públicamente. ¿Qué cambias?

Desactivo el acceso público, la paso a subredes privadas, restrinjo los grupos de seguridad a los orígenes de la aplicación, obligo TLS, roto las credenciales, reviso los logs en busca de accesos sospechosos y añado barreras (regla de Config, SCP) para que no se repita.

#### ¿Cómo montas un plan de recuperación ante desastres entre regiones para una base RDS MySQL?

Creo una réplica de lectura en otra región (o Aurora Global Database si es Aurora), replico los backups automáticos o copio los snapshots a la región de DR, automatizo con scripts la promoción y los cambios de DNS, mantengo lista la infraestructura de la aplicación en la región de DR y pruebo el failover periódicamente contra el RPO y el RTO.
