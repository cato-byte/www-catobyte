## Guía de estudio de Amazon RDS

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de Amazon RDS: unas 200 preguntas](../../images/aws_rds_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre Amazon RDS y Aurora: motores, elección de instancia y almacenamiento, alta disponibilidad con Multi-AZ, réplicas de lectura, backups y restauraciones, seguridad, monitoreo, rendimiento, escalado, costos, migraciones, y cómo los ingenieros de datos extraen datos de RDS con CDC, exportaciones y zero-ETL. Las respuestas reflejan el servicio en 2026.

La guía sigue una ruta de aprendizaje en seis etapas. Cada sección se divide en unidades cortas: objetivos de aprendizaje, una explicación del concepto y un ejemplo resuelto, luego preguntas (primero de memoria, después de aplicación), un reto práctico e ideas clave. Para **aprender**, lee cada unidad de principio a fin. Para **repasar**, cambia al modo repaso o usa "Ir a las preguntas", marca las respuestas que quieras volver a ver y prueba un repaso mixto entre secciones.

<!-- QA -->
<!-- stage: Fundamentos -->

### Fundamentos

<!-- unit: Qué gestiona RDS -->

<!-- goals -->

- Explicar qué es Amazon RDS y qué motores ejecuta.
- Repartir las responsabilidades entre AWS y tú.

<!-- concept -->

Operar bien una base de datos exige trabajo rutinario constante: instalar, parchear, respaldar, reemplazar hardware dañado, montar standbys. RDS convierte esa rutina en configuraciones. Eliges un motor y un tamaño, y AWS opera el servidor de abajo.

Lo que queda de tu lado es todo lo que depende de tus datos y tu aplicación: diseño del esquema, consultas, índices, usuarios y permisos, acceso de red y las decisiones sobre backups y disponibilidad. Gestionado no significa afinado ni seguro por defecto.

<!-- example -->

| Tarea | Autogestionado en EC2 | RDS |
|---|---|---|
| Parches del sistema y del motor | Tú | AWS (en tu ventana de mantenimiento) |
| Backups y restauración a un punto en el tiempo | Tú | AWS (tú fijas la retención) |
| Standby y failover | Tú | AWS (si es Multi-AZ) |
| Esquema, índices, consultas, usuarios | Tú | Tú |

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

<!-- challenge -->

Un equipo se pasó a RDS y dejó de pensar en la base. Seis meses después las consultas van lentas y alguien borró una tabla por error. ¿Cuál de estas cosas era su responsabilidad?

<!-- solution -->

Ambas. El rendimiento de las consultas (índices, diseño de consultas) y proteger los datos de errores humanos (permisos, deletion protection, retención de backups y restauraciones probadas) son responsabilidad del cliente en RDS.

<!-- takeaways -->

- RDS automatiza infraestructura, parches, backups y failover.
- Esquema, consultas, usuarios y acceso siguen siendo tuyos.
- Gestionado no es lo mismo que afinado o asegurado.

<!-- unit: RDS, EC2 y variantes -->

<!-- goals -->

- Decidir cuándo RDS es la opción correcta y cuándo no.
- Conocer RDS Custom y RDS on Outposts.

<!-- concept -->

RDS cambia control por menos trabajo. No puedes entrar al servidor, instalar extensiones arbitrarias ni usar versiones raras. Para la mayoría de aplicaciones es un buen cambio; para algunas bases heredadas o especializadas no lo es.

AWS cubre los huecos intermedios: RDS Custom da acceso al sistema operativo para Oracle y SQL Server manteniendo la automatización, y RDS on Outposts corre el servicio en tu propio centro de datos. Correr la base tú mismo en EC2 sigue siendo la opción de control total, con todo el trabajo que implica.

<!-- example -->

| Requisito | Opción |
|---|---|
| App PostgreSQL estándar | RDS |
| Oracle con un agente del proveedor en el sistema | RDS Custom |
| Base de baja latencia en una fábrica | RDS on Outposts |
| Motor no soportado o configuración exótica | EC2, autogestionado |

#### ¿Cuándo RDS no es la opción correcta?

Cuando necesitas acceso al sistema operativo o extensiones no admitidas (considera RDS Custom o EC2), un motor que RDS no ofrece, una escala extrema más allá de un solo escritor (considera Aurora DSQL, DynamoDB o sharding), o cargas analíticas sobre terabytes que encajan mejor en un data warehouse o un lakehouse.

#### ¿Qué diferencia hay entre RDS y ejecutar una base de datos en EC2?

En EC2 tienes control total (sistema operativo, cualquier versión, cualquier configuración) pero lo administras todo: instalación, parches, backups, replicación, failover y monitoreo. RDS elimina ese trabajo operativo a cambio de algunas restricciones (sin acceso al sistema operativo, privilegios de superusuario limitados, solo parámetros admitidos).

#### ¿Qué es RDS Custom?

Una variante de RDS para Oracle y SQL Server que da acceso al sistema operativo y permite personalizar la base de datos (para aplicaciones heredadas que necesitan parches o software concretos), mientras AWS sigue automatizando los backups y parte de la administración.

#### ¿Qué es un DB subnet group?

Un conjunto de subredes (en al menos dos zonas de disponibilidad) de una VPC donde RDS puede ubicar las instancias. Es necesario para crear una instancia en una VPC y para admitir Multi-AZ.

<!-- challenge -->

La aplicación SQL Server de un proveedor exige instalar un agente de monitoreo en el sistema operativo del servidor de base de datos. ¿Qué opción encaja y qué sigues recibiendo de AWS?

<!-- solution -->

RDS Custom for SQL Server: permite acceso al sistema para el agente y AWS sigue automatizando backups, monitoreo y parte del mantenimiento. El RDS normal no permite acceso al sistema operativo.

<!-- takeaways -->

- RDS cambia acceso al sistema por automatización.
- RDS Custom agrega acceso al sistema para Oracle y SQL Server.
- EC2 da control total y responsabilidad total.

<!-- unit: Instancias y clases -->

<!-- goals -->

- Describir las instancias de base de datos y elegir una clase.
- Usar con seguridad la detención, la deletion protection y los tags.

<!-- concept -->

Una DB instance es la unidad que pagas y operas: cómputo de una clase de instancia más el almacenamiento conectado. Las clases vienen en familias, de burstables para carga liviana o variable a optimizadas en memoria para la mayoría de bases de producción, donde que los datos quepan en memoria decide el rendimiento.

Alrededor de la instancia, unas pocas configuraciones evitan accidentes y costos comunes: deletion protection, detener instancias de desarrollo ociosas (con un límite de tiempo) y tags para responsables y costos.

<!-- example -->

```bash
aws rds create-db-instance --db-instance-identifier orders-prod \
  --engine postgres --db-instance-class db.r7g.large --allocated-storage 200 \
  --storage-type gp3 --multi-az --deletion-protection \
  --tags Key=team,Value=orders Key=env,Value=prod
```

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

<!-- challenge -->

Las bases de desarrollo se detienen el viernes para ahorrar, pero el sábado de la semana siguiente vuelven a estar encendidas. ¿Por qué y qué haces?

<!-- solution -->

RDS vuelve a arrancar las instancias detenidas tras 7 días. Programa el stop/start diario (EventBridge Scheduler o Instance Scheduler) por tag, o usa Aurora Serverless v2 o snapshots para entornos que se usan poco.

<!-- takeaways -->

- Una instancia es una clase más almacenamiento.
- Las clases optimizadas en memoria sirven a casi toda base de producción.
- Deletion protection y tags evitan accidentes y costos desconocidos.

<!-- unit: Configuración y mantenimiento -->

<!-- goals -->

- Configurar los motores con parameter groups y option groups.
- Planear el mantenimiento y crear instancias como código.

<!-- concept -->

En RDS no puedes editar archivos de configuración, así que los ajustes del motor viven en parameter groups y las funciones opcionales en option groups. Usar grupos propios desde el primer día importa, porque los grupos por defecto no se pueden cambiar y cambiarlos después puede exigir un reinicio.

El mantenimiento se programa en una ventana semanal que eliges. Definir instancias, grupos y ventanas como código hace consistentes los entornos y revisables los cambios.

<!-- example -->

```bash
aws rds create-db-parameter-group --db-parameter-group-name pg16-orders \
  --db-parameter-group-family postgres16 --description "orders prod"
aws rds modify-db-parameter-group --db-parameter-group-name pg16-orders \
  --parameters "ParameterName=log_min_duration_statement,ParameterValue=500,ApplyMethod=immediate"
```

#### ¿Qué es la protección contra borrado?

Un ajuste que impide borrar una instancia o un cluster hasta que se desactive, protegiendo las bases de producción de un borrado accidental.

#### ¿Qué es el modelo de responsabilidad compartida en RDS?

AWS se encarga de la infraestructura, el sistema operativo, los parches del software de base de datos, los backups y los mecanismos de replicación. Tú te encargas del acceso de red (grupos de seguridad), las decisiones de cifrado, los usuarios y privilegios de la base, el diseño del esquema y de las consultas, los parámetros y la protección de las credenciales.

#### ¿Cómo te conectas desde tu computador a una instancia de RDS en una subred privada?

Mediante un bastión o, mejor, el reenvío de puertos de AWS Systems Manager Session Manager hacia una instancia en la VPC, una VPN de cliente, o un EC2 dentro de la VPC; nunca haciendo pública la base de datos.

#### ¿Qué significa "publicly accessible" en una instancia de RDS?

La instancia recibe una IP pública y su endpoint la resuelve desde fuera de la VPC, así que es accesible desde internet si los grupos de seguridad lo permiten. Las bases de producción deben tenerlo desactivado.

<!-- challenge -->

Debes cambiar un parámetro estático (`shared_buffers`) en una instancia de producción que usa el parameter group por defecto. ¿Qué pasos implica?

<!-- solution -->

Crear un parameter group propio, fijar ahí el valor, asociar el grupo a la instancia y reiniciar (de preferencia en la ventana de mantenimiento), porque los parámetros estáticos solo se aplican tras un reinicio.

<!-- takeaways -->

- Los parameter groups guardan ajustes del motor; los option groups, funciones.
- Usa grupos propios desde el inicio.
- Elige una ventana de mantenimiento y gestiona todo como código.

<!-- unit: Red y conectividad -->

<!-- goals -->

- Ubicar RDS en una VPC con subnet groups y endpoints.
- Conectarte con seguridad a instancias privadas.

<!-- concept -->

Una instancia RDS vive en tu VPC, en subredes que eliges mediante un subnet group que abarca al menos dos zonas. Las aplicaciones se conectan por un endpoint, un nombre DNS que sigue funcionando cuando RDS mueve la instancia en un failover.

Las bases de producción van en subredes privadas sin acceso público. Quien necesite conectarse pasa por port forwarding de Session Manager o un bastión, en vez de abrir la base a internet.

<!-- example -->

```bash
aws ssm start-session --target i-0bastion123 \
  --document-name AWS-StartPortForwardingSessionToRemoteHost \
  --parameters '{"host":["orders-prod.abc123.eu-west-1.rds.amazonaws.com"],"portNumber":["5432"],"localPortNumber":["5432"]}'
psql -h localhost -U analyst orders
```

#### ¿Cómo se crean instancias de RDS de forma repetible?

Con infraestructura como código (CloudFormation, CDK, Terraform), definiendo los subnet groups, parameter groups, grupos de seguridad, claves KMS, secretos y la instancia, para que los entornos sean coherentes y los cambios se revisen.

#### ¿Para qué sirven las etiquetas en RDS?

Para la asignación de costos, el control de acceso (condiciones IAM sobre etiquetas), la automatización (por ejemplo detener de noche las instancias con `env=dev`) y la información de responsables.

#### ¿Qué es RDS on Outposts?

RDS ejecutándose sobre hardware AWS Outposts en tu propio centro de datos, para cargas que necesitan baja latencia hacia sistemas on-premises o residencia de los datos, administrado con las mismas APIs.

#### ¿Qué tipos de almacenamiento ofrece RDS?

SSD de propósito general gp3 (base de 3.000 IOPS y 125 MiB/s, con IOPS y rendimiento configurables independientemente del tamaño), gp2 (IOPS ligadas al tamaño con créditos de ráfaga), IOPS aprovisionadas io1 e io2 Block Express (IOPS altas y constantes y baja latencia) y el almacenamiento magnético heredado.

<!-- challenge -->

Una aplicación se conecta a RDS usando la IP de la instancia y se rompe tras cada failover. ¿Qué debería usar?

<!-- solution -->

El nombre DNS del endpoint de RDS. Durante el failover RDS apunta el endpoint al nuevo primario; las IPs cambian. Mantén además corto el caché de DNS en la aplicación.

<!-- takeaways -->

- Los subnet groups abarcan al menos dos zonas.
- Conéctate siempre por el endpoint, nunca por IP.
- Mantén privadas las bases de producción; usa túneles para acceder.

### Almacenamiento

<!-- unit: Tipos de almacenamiento e IOPS -->

<!-- goals -->

- Elegir entre almacenamiento gp3, gp2 e io1/io2.
- Leer métricas de IOPS y de cola para dimensionar el almacenamiento.

<!-- concept -->

Las bases de datos suelen estar limitadas por la velocidad de lectura y escritura de bloques, no por la CPU. Los tipos de almacenamiento de RDS difieren en cómo se fija esa velocidad: gp3 da una base que puedes subir aparte del tamaño, el viejo gp2 ata la velocidad al tamaño con créditos de ráfaga, e io1/io2 garantizan IOPS con baja latencia para cargas exigentes.

Las métricas te dicen en qué caso estás: una cola y una latencia altas significan que el disco no da abasto.

<!-- example -->

```text
ReadIOPS + WriteIOPS at peak:  5,200
gp3 baseline:                  3,000  → raise gp3 IOPS to ~6,000
DiskQueueDepth:                 35    (was 2)  → storage is the bottleneck
```

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

<!-- challenge -->

Una base gp2 de 100 GB va rápida en la mañana y lenta cada tarde durante las cargas batch. ¿Qué pasa y qué cambias?

<!-- solution -->

La base de gp2 es de 300 IOPS para 100 GB; las cargas batch agotan los créditos de ráfaga y el rendimiento cae a la base. Pasar a gp3 (base de 3.000 IOPS, ajustable) o a io2 si la latencia debe ser constante.

<!-- takeaways -->

- gp3 desacopla IOPS del tamaño; gp2 depende de ráfagas.
- io1/io2 garantizan IOPS para cargas exigentes.
- Una cola alta indica que el almacenamiento es el cuello de botella.

<!-- unit: Crecer y cambiar el almacenamiento -->

<!-- goals -->

- Evitar quedarte sin espacio con storage autoscaling.
- Saber qué pueden y qué no pueden hacer los cambios de almacenamiento.

<!-- concept -->

Quedarse sin espacio detiene las escrituras, así que RDS ofrece storage autoscaling hasta un máximo que fijas. Crecer es fácil; reducir no: el almacenamiento asignado solo puede subir, y bajarlo implica mover los datos a una instancia nueva.

Los cambios de tamaño o tipo suelen hacerse en línea, pero la instancia entra en una fase de optimización y hay un periodo de espera antes del siguiente cambio. Planea los cambios de almacenamiento en vez de hacerlos en medio de un incidente.

<!-- example -->

```bash
aws rds modify-db-instance --db-instance-identifier orders-prod \
  --max-allocated-storage 1000 --apply-immediately     # enable autoscaling up to 1 TB
```

#### ¿Cómo se compara gp3 con io2 en RDS?

gp3 ofrece una base de 3.000 IOPS y 125 MiB/s, configurable hasta límites mayores con costo extra, a un precio por GB más bajo. io2 Block Express ofrece IOPS más altas y constantes y menor latencia con mejor durabilidad, para las cargas más exigentes.

#### ¿Qué indica `DiskQueueDepth`?

El número de solicitudes de E/S pendientes esperando al disco. Una cola alta y constante con latencia alta significa que el almacenamiento no da abasto; considera más IOPS, mejores consultas o caché.

#### ¿Qué impacto tiene modificar el almacenamiento de una instancia en marcha?

Aumentar el almacenamiento o cambiar el tipo suele hacerse en línea, pero la instancia puede quedar horas en estado "storage-optimization", durante el cual no se permiten más cambios de almacenamiento; el rendimiento puede verse algo afectado.

#### ¿Cómo se estiman las IOPS necesarias?

A partir de las métricas actuales (`ReadIOPS` + `WriteIOPS` en el pico) o, para cargas nuevas, de las transacciones por segundo esperadas y la E/S por transacción, con margen; luego se prueba con carga antes de producción.

#### ¿Qué es un despliegue Multi-AZ de instancia?

RDS mantiene una réplica standby síncrona de la primaria en otra zona de disponibilidad. Si la primaria falla (hardware, caída de la AZ, fallo de almacenamiento) o durante ciertos mantenimientos, RDS hace failover automático a la standby, normalmente en uno o dos minutos. La standby no atiende lecturas.

<!-- challenge -->

Un equipo asignó 4 TB "por si acaso" a una base que usa 300 GB. ¿Pueden reducirlo y cómo?

<!-- solution -->

No en el sitio. Crear una instancia nueva con menos almacenamiento y autoscaling activado, migrar los datos (dump y restore, DMS o replicación), cambiar la aplicación y luego borrar la instancia vieja.

<!-- takeaways -->

- Storage autoscaling evita caídas por "storage-full".
- El almacenamiento asignado puede crecer pero no reducirse.
- Los cambios disparan optimización y periodos de espera.

<!-- stage: Disponibilidad y protección de datos -->

### Alta disponibilidad y Multi-AZ

<!-- unit: Despliegues Multi-AZ -->

<!-- goals -->

- Explicar los despliegues Multi-AZ de instancia y de cluster.
- Describir cómo funciona el failover y qué RPO y RTO da.

<!-- concept -->

Multi-AZ protege contra la pérdida de un servidor o de toda una zona de disponibilidad. RDS mantiene un standby en otra zona con replicación síncrona, así cada escritura confirmada existe en ambos lugares. Cuando falla el primario, el standby se promueve y el endpoint apunta a él.

En la variante de instancia el standby es invisible y solo espera. La variante de cluster tiene dos standbys legibles y conmuta más rápido. En ambos casos el RPO es prácticamente cero y la recuperación toma uno o dos minutos.

<!-- example -->

```text
AZ a: primary  ── synchronous replication ──►  AZ b: standby
         ▲
endpoint orders-prod.xxxx.rds.amazonaws.com  (DNS flips to b on failover)
```

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

<!-- challenge -->

El negocio pide "cero pérdida de datos y menos de 5 minutos de caída" si falla una zona. ¿Lo cumple Multi-AZ?

<!-- solution -->

Sí. La replicación síncrona da un RPO prácticamente cero, y el failover suele completarse en uno o dos minutos (más rápido con Multi-AZ DB clusters), dentro de los 5 minutos.

<!-- takeaways -->

- Multi-AZ mantiene un standby síncrono en otra zona.
- El failover promueve el standby y cambia el endpoint.
- RPO ≈ 0; RTO de unos 1–2 minutos.

<!-- unit: Convivir con el failover -->

<!-- goals -->

- Preparar las aplicaciones para el failover y probarlo.
- Saber de qué no protege Multi-AZ.

<!-- concept -->

El failover es solo la mitad de la historia; la aplicación tiene que reconectarse. Clientes que cachean DNS mucho tiempo, mantienen conexiones sin reintentos o tienen IPs escritas convierten un failover de un minuto en una caída larga. Probar con un failover forzado lo revela antes de que importe.

Multi-AZ también tiene límites claros. En el esquema clásico el standby no sirve lecturas, así que no es escalado, y replica fielmente los errores, así que no es un backup. Los desastres regionales necesitan un plan de recuperación aparte.

<!-- example -->

```bash
aws rds reboot-db-instance --db-instance-identifier orders-prod --force-failover
# then watch: app errors, reconnect time, connection pool behavior
```

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

#### ¿Qué es una réplica de lectura?

Una copia de una instancia origen mantenida al día con replicación asíncrona, usada para descargar el tráfico de lectura (reportes, analítica, APIs con muchas lecturas). Tiene su propio endpoint y puede estar en la misma región o en otra.

<!-- challenge -->

Tras un failover de prueba la base vuelve en 60 segundos, pero la aplicación Java sigue fallando 15 minutos. ¿Cuál es la causa probable?

<!-- solution -->

La JVM cachea el DNS (a veces sin límite), así que la app sigue conectándose a la IP del primario viejo. Fija un TTL de DNS corto en la JVM, agrega reintentos y considera el AWS Advanced JDBC Wrapper para detectar antes el failover.

<!-- takeaways -->

- Las aplicaciones deben reconectarse rápido; pruébalo.
- Multi-AZ no es escalado de lecturas ni un backup.
- Alta disponibilidad no es recuperación ante desastres.

### Réplicas de lectura

<!-- unit: Réplicas y lag -->

<!-- goals -->

- Explicar las réplicas de lectura, el lag y las lecturas desactualizadas.
- Enrutar lecturas a réplicas con seguridad.

<!-- concept -->

Las réplicas de lectura copian los cambios del primario de forma asíncrona, lo que les permite servir lecturas sin frenar las escrituras. El precio es el lag: una réplica siempre va un poco atrás, a veces mucho, así que leer tu propia escritura justo después puede fallar.

Eso define cómo las usan las aplicaciones. Las consultas pesadas en lectura que toleran algo de atraso van a réplicas; todo lo que debe ver la última escritura va al primario.

<!-- example -->

```python
WRITER = "orders-prod.xxxx.rds.amazonaws.com"
READER = "orders-replica-1.xxxx.rds.amazonaws.com"

def get_order_after_payment(order_id):
    return query(WRITER, "SELECT * FROM orders WHERE id = %s", order_id)  # must be fresh

def list_catalog():
    return query(READER, "SELECT * FROM products WHERE active")             # lag is fine
```

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

<!-- challenge -->

Tras mover las lecturas a una réplica, a veces los usuarios no ven el comentario que acaban de publicar. ¿Cómo lo arreglas sin abandonar las réplicas?

<!-- solution -->

Enviar al primario las lecturas que siguen a una escritura del propio usuario (read-your-writes), por ejemplo durante unos segundos tras escribir o para la sesión de ese usuario, y dejar las demás lecturas en la réplica.

<!-- takeaways -->

- Las réplicas replican de forma asíncrona y tienen lag.
- Enruta al primario las lecturas que necesitan frescura.
- Las réplicas necesitan backups automáticos en el origen.

<!-- unit: Topologías de réplicas -->

<!-- goals -->

- Usar réplicas entre regiones, con Multi-AZ y como copias con retraso.
- Promover réplicas y saber cómo se comportan en un failover.

<!-- concept -->

Las réplicas hacen más que escalar lecturas. En otra región acercan los datos a los usuarios y dan una copia de recuperación que puedes promover. Con Multi-AZ propio sobreviven a caídas de zona. Con retraso, conservan una ventana en la que los errores del primario aún no llegaron.

La promoción es una puerta de un solo sentido: la réplica se vuelve una base independiente y la replicación se detiene.

<!-- example -->

```bash
aws rds create-db-instance-read-replica --db-instance-identifier orders-dr \
  --source-db-instance-identifier arn:aws:rds:eu-west-1:123456789012:db:orders-prod \
  --region eu-central-1 --kms-key-id alias/rds-dr
# during a regional disaster:
aws rds promote-read-replica --db-instance-identifier orders-dr --region eu-central-1
```

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

<!-- challenge -->

Alguien corrió un `UPDATE` sin `WHERE` en MySQL hace 10 minutos. Existe una réplica con una hora de retraso. ¿Cómo puede ayudar?

<!-- solution -->

Detener la replicación en la réplica retrasada antes de que aplique la sentencia mala, aplicar los cambios hasta justo antes, y copiar las filas correctas de vuelta al primario (o promover la réplica si hace falta).

<!-- takeaways -->

- Las réplicas entre regiones sirven lecturas lejanas y DR.
- La promoción independiza la réplica; la replicación termina.
- Las réplicas retrasadas dan una ventana para recuperarse de errores.

<!-- unit: Réplicas para analítica -->

<!-- goals -->

- Descargar reportes y extracciones en réplicas.
- Manejar el lag causado por escrituras pesadas en el primario.

<!-- concept -->

La analítica y las transacciones compiten por la misma CPU, memoria e I/O. Una réplica dimensionada para reportes saca las consultas pesadas del primario para que los clientes no las sientan.

Pero las réplicas comparten la carga de escritura del primario: cada cambio debe re-aplicarse. Escrituras batch grandes o transacciones largas en el primario aparecen como lag en la réplica, y las consultas largas en la réplica pueden retrasar aún más la aplicación de cambios.

<!-- example -->

```sql
-- on the primary: break one huge update into batches
UPDATE orders SET status = 'archived'
WHERE id IN (SELECT id FROM orders WHERE created_at < '2024-01-01' AND status <> 'archived' LIMIT 10000);
-- repeat until 0 rows; replicas apply each small transaction quickly
```

#### ¿Qué son los backups automáticos?

Snapshots diarios de la instancia más los logs de transacciones capturados cada pocos minutos, conservados durante un periodo configurable (de 1 a 35 días; 0 los desactiva), que permiten la recuperación a un punto en el tiempo dentro de la ventana de retención.

#### ¿Qué es la recuperación a un punto en el tiempo (PITR)?

Restaurar la base a cualquier segundo dentro del periodo de retención (hasta unos cinco minutos atrás), lo que crea una instancia nueva con un endpoint nuevo. Es la herramienta principal para recuperarse de cambios accidentales.

#### ¿Qué son los snapshots manuales?

Snapshots iniciados por el usuario que se conservan hasta que los borres, independientes de la retención de los backups automáticos. Se usan antes de cambios riesgosos, para retención a largo plazo y para copiar o compartir bases de datos.

<!-- challenge -->

Los analistas necesitan los datos de ayer a las 07:00, pero el lag de la réplica llega a tres horas durante el batch nocturno. Enumera dos cambios.

<!-- solution -->

Dividir las transacciones grandes del batch en otras más pequeñas (y programarlas antes), y dar a la réplica I/O y CPU suficientes para aplicar los cambios. Si los analistas no necesitan frescura al minuto, una exportación diaria de snapshot a S3 evita el problema.

<!-- takeaways -->

- Las réplicas sacan la analítica del primario.
- Las transacciones grandes del primario causan lag.
- Para analítica diaria pueden encajar mejor exportaciones o un lake.

### Backups y restauración

<!-- unit: Backups automáticos y recuperación a un punto en el tiempo -->

<!-- goals -->

- Explicar los backups automáticos y la recuperación a un punto en el tiempo.
- Recuperarte de borrados accidentales y saber cómo se comportan las restauraciones.

<!-- concept -->

Los backups automáticos combinan un snapshot diario con logs de transacciones guardados cada pocos minutos, lo que permite a RDS reconstruir la base en cualquier segundo del periodo de retención. Es la protección principal contra errores humanos, ya que las réplicas también copian los errores.

Las restauraciones nunca sobrescriben: crean una instancia nueva, que arranca rápido pero carga los datos perezosamente desde S3, así las primeras consultas van lentas. Recuperar unas pocas filas significa restaurar junto a producción y copiarlas de vuelta.

<!-- example -->

```bash
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier orders-prod \
  --target-db-instance-identifier orders-restore-0930 \
  --restore-time 2026-10-17T09:29:00Z
pg_dump -h orders-restore-0930... -t public.invoices --data-only | psql -h orders-prod...
```

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

<!-- challenge -->

Una instancia restaurada para una prueba de desastre responde muy lento la primera hora. ¿Hay algún problema?

<!-- solution -->

No, es lazy loading: los bloques se traen de S3 en el primer acceso. Caliéntala leyendo las tablas importantes (por ejemplo escaneos completos o `pg_prewarm`) antes de enviar tráfico real.

<!-- takeaways -->

- Los backups automáticos permiten restaurar cualquier segundo de la retención.
- Las restauraciones crean instancias nuevas.
- El almacenamiento restaurado carga perezosamente; caliéntalo.

<!-- unit: Snapshots y retención -->

<!-- goals -->

- Gestionar snapshots manuales, copias y retención de largo plazo.
- Proteger los backups entre regiones y cuentas.

<!-- concept -->

Los backups automáticos expiran con su retención; los snapshots manuales quedan hasta que los borras. Las necesidades de largo plazo y cumplimiento dependen por eso de snapshots, idealmente gestionados con AWS Backup y sus políticas, bóvedas y bloqueos que impiden borrarlos.

Un backup en la misma cuenta y región comparte su suerte, así que copias a otra región o cuenta protegen contra caídas regionales y cuentas comprometidas. Borrar una instancia es el momento de decidir qué conservar.

<!-- example -->

```bash
aws rds copy-db-snapshot \
  --source-db-snapshot-identifier arn:aws:rds:eu-west-1:123456789012:snapshot:orders-2026-10 \
  --target-db-snapshot-identifier orders-2026-10-dr --kms-key-id alias/rds-dr \
  --region eu-central-1
```

#### ¿Qué es la carga diferida (lazy loading) tras una restauración?

Cuando una instancia se restaura desde un snapshot, sus bloques de almacenamiento se traen de S3 en el primer acceso, así que las lecturas iniciales tienen más latencia. Ejecutar lecturas completas de las tablas tras la restauración calienta el almacenamiento.

#### ¿Cómo se conservan backups durante siete años por cumplimiento?

Con AWS Backup y un plan de retención largo con vault lock, o copiando snapshots manuales periódicamente; los backups automáticos llegan a 35 días como máximo. Exportar a S3 con reglas de ciclo de vida también sirve para el archivo.

#### ¿Se puede restaurar una sola tabla desde un backup?

No directamente. Restaura toda la instancia en una nueva (a un punto en el tiempo), luego haz un dump de la tabla necesaria e impórtala en producción.

#### ¿Qué es la replicación entre regiones de los backups automáticos?

Una función que copia los backups automáticos y los logs de transacciones a otra región, para poder hacer recuperación a un punto en el tiempo en la región de DR.

#### ¿Cómo se controla el acceso de red a RDS?

Ubicando las instancias en subredes privadas, desactivando el acceso público y usando grupos de seguridad de la VPC que solo permitan los grupos de seguridad de la aplicación o rangos CIDR concretos en el puerto de la base. El acceso desde on-premises pasa por VPN o Direct Connect.

#### ¿Cómo se cifran los datos en reposo en RDS?

Con claves de AWS KMS (administradas por AWS o por el cliente), que cubren el almacenamiento, los backups automáticos, los snapshots, las réplicas de lectura y los logs. El cifrado se elige al crear la instancia.

#### ¿Cómo se cifra una instancia de RDS existente sin cifrar?

Tomando un snapshot, copiándolo con cifrado activado con una clave KMS y restaurando una instancia nueva desde la copia cifrada; luego se cambian las aplicaciones a ella. Las réplicas de una instancia sin cifrar no se pueden cifrar directamente.

<!-- challenge -->

Un ransomware borró la instancia y sus snapshots usando una cuenta de administrador comprometida. ¿Qué diseño habría salvado los datos?

<!-- solution -->

Copias de los backups en una cuenta aparte (y otra región) con vault lock de AWS Backup, para que ni un administrador de la cuenta de producción pueda borrarlas. Combinarlo con mínimo privilegio y MFA en los roles de administración.

<!-- takeaways -->

- Los snapshots manuales y AWS Backup sirven a la retención larga.
- Copia los backups a otra región y cuenta.
- Los vault locks protegen los backups del borrado.

### Seguridad

<!-- unit: Acceso de red -->

<!-- goals -->

- Restringir el acceso de red a RDS con subredes y security groups.
- Conectar Lambda y corregir instancias accesibles públicamente.

<!-- concept -->

La primera capa de seguridad es el alcance. Las bases en subredes privadas sin acceso público solo son alcanzables desde dentro de la red, y los security groups lo acotan aún más a grupos de aplicaciones concretos en vez de rangos de IP.

Referenciar security groups en vez de direcciones mantiene correctas las reglas a medida que instancias y funciones escalan y cambian de IP.

<!-- example -->

```text
sg-app     (attached to ECS tasks and Lambda)
sg-db      inbound: TCP 5432 from sg-app   ← no CIDR ranges, no 0.0.0.0/0
RDS:       private subnets, PubliclyAccessible = false
```

#### ¿Cómo se cifran los datos en tránsito?

Con conexiones SSL/TLS que usan el paquete de autoridades certificadoras de RDS. Se puede obligar TLS con parámetros como `rds.force_ssl` (PostgreSQL, SQL Server) o `require_secure_transport` (MySQL). Hay que rotar los certificados cuando RDS rota sus CA.

#### ¿Qué es la autenticación de base de datos con IAM?

En MySQL, MariaDB y PostgreSQL (y Aurora), los usuarios se autentican con un token de corta duración generado a partir de credenciales IAM en lugar de una contraseña, de modo que el acceso se controla con políticas IAM y no se guardan contraseñas de base de datos en las aplicaciones.

#### ¿Cómo se deben administrar las contraseñas de la base de datos?

Con Secrets Manager, idealmente con contraseñas del usuario maestro administradas por RDS (RDS crea y rota el secreto), rotando automáticamente los secretos de los usuarios de aplicación y sin escribir nunca credenciales en el código.

<!-- challenge -->

El security group de una base permite `0.0.0.0/0` en el puerto 3306 "temporalmente" para un contratista. ¿Con qué lo reemplazas?

<!-- solution -->

Quitar la regla, mantener privada la instancia y dar acceso al contratista mediante port forwarding de Session Manager (o una client VPN) con una identidad IAM, para que el acceso quede autenticado y registrado.

<!-- takeaways -->

- Primero subredes privadas y sin acceso público.
- Los security groups deben referenciar otros security groups.
- Da acceso a las personas por túneles, no por puertos abiertos.

<!-- unit: Cifrado -->

<!-- goals -->

- Cifrar los datos de RDS en reposo y en tránsito.
- Cifrar instancias existentes e imponer el cifrado por política.

<!-- concept -->

El cifrado en reposo con KMS cubre almacenamiento, backups, snapshots y réplicas, y solo se elige al crear una instancia. Cifrar una base existente implica copiar un snapshot con cifrado y restaurarlo.

El cifrado en tránsito se apoya en TLS, que puedes exigir con parámetros. Las políticas vuelven obligatorio el cifrado, y hacen falta claves gestionadas por el cliente para compartir snapshots cifrados entre cuentas.

<!-- example -->

```bash
aws rds copy-db-snapshot --source-db-snapshot-identifier orders-plain \
  --target-db-snapshot-identifier orders-encrypted --kms-key-id alias/rds-prod
aws rds restore-db-instance-from-db-snapshot --db-instance-identifier orders-prod-enc \
  --db-snapshot-identifier orders-encrypted
# PostgreSQL: rds.force_ssl = 1 in the parameter group
```

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

<!-- challenge -->

Debes compartir un snapshot cifrado con una cuenta de analítica, pero la copia falla. ¿Qué está mal?

<!-- solution -->

El snapshot está cifrado con la clave gestionada por AWS para RDS, que no se puede compartir. Cópialo con una clave KMS gestionada por el cliente, da a la otra cuenta permiso sobre esa clave y comparte el snapshot.

<!-- takeaways -->

- El cifrado en reposo se elige al crear; copia para cambiarlo.
- Exige TLS con parámetros del motor.
- Los snapshots cifrados compartidos necesitan claves del cliente.

<!-- unit: Autenticación y usuarios de base de datos -->

<!-- goals -->

- Elegir entre contraseñas, autenticación IAM y Kerberos.
- Diseñar usuarios de base con mínimo privilegio.

<!-- concept -->

Quién se conecta a la base importa tanto como desde dónde. Las contraseñas deben vivir en Secrets Manager con rotación, idealmente gestionada por el propio RDS. La autenticación IAM reemplaza las contraseñas por tokens de corta vida atados a roles IAM; Kerberos enlaza los inicios de sesión con un directorio corporativo.

Dentro de la base, el usuario maestro es solo para administración. Cada aplicación recibe su propio usuario con los privilegios justos, lo que limita el daño y da sentido a los logs de auditoría.

<!-- example -->

```sql
CREATE ROLE orders_app LOGIN;
GRANT CONNECT ON DATABASE shop TO orders_app;
GRANT USAGE ON SCHEMA orders TO orders_app;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA orders TO orders_app;
GRANT rds_iam TO orders_app;           -- PostgreSQL: allow IAM token authentication
```

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

<!-- challenge -->

Tres servicios y cinco analistas usan todos el usuario maestro. ¿Qué cambias primero?

<!-- solution -->

Crear un usuario por servicio y por grupo de analistas con solo los privilegios necesarios (solo lectura para analistas), guardar credenciales en Secrets Manager o usar autenticación IAM, y luego rotar la contraseña maestra y restringir quién la usa.

<!-- takeaways -->

- Guarda y rota contraseñas con Secrets Manager.
- IAM y Kerberos reemplazan las contraseñas estáticas.
- Un usuario de mínimo privilegio por aplicación.

<!-- unit: Auditoría y barandas -->

<!-- goals -->

- Auditar la actividad de la base y los cambios por API.
- Evitar cambios riesgosos en los recursos de RDS.

<!-- concept -->

Hay dos tipos de actividad que vigilar. Dentro del motor, los logs de auditoría y los activity streams registran quién consultó o cambió datos. Alrededor, CloudTrail registra quién modificó instancias, snapshots y configuraciones.

Las barandas frenan los errores antes de tener que investigarlos: políticas IAM que limitan quién puede modificar o borrar bases de producción, deletion protection y roles o cuentas separados para producción.

<!-- example -->

```json
{
  "Effect": "Deny",
  "Action": ["rds:DeleteDBInstance", "rds:ModifyDBInstance"],
  "Resource": "arn:aws:rds:*:*:db:*",
  "Condition": {"StringEquals": {"aws:ResourceTag/env": "prod"},
                "StringNotEquals": {"aws:PrincipalTag/role": "dba"}}
}
```

#### ¿Qué métricas de CloudWatch son las más importantes en RDS?

`CPUUtilization`, `FreeableMemory`, `FreeStorageSpace`, `ReadIOPS`/`WriteIOPS`, `ReadLatency`/`WriteLatency`, `DiskQueueDepth`, `DatabaseConnections`, `ReplicaLag`, `SwapUsage` y, en las clases ampliables, `CPUCreditBalance`.

#### ¿Qué es Enhanced Monitoring?

Métricas a nivel de sistema operativo (CPU y memoria por proceso, sistema de archivos, swap, E/S de disco) recogidas por un agente a intervalos de hasta un segundo y enviadas a CloudWatch Logs, que ayudan a encontrar causas que las métricas estándar no muestran.

#### ¿Qué es Performance Insights / Database Insights?

Una herramienta de rendimiento que muestra la carga de la base (sesiones activas promedio) desglosada por eventos de espera, sentencias SQL, usuarios y hosts, para ver qué consultas causan carga y por qué. Hoy forma parte de CloudWatch Database Insights, que en su modo avanzado añade vistas de toda la flota y más retención.

#### ¿Cómo se encuentran las consultas lentas en RDS?

Activando los logs de consultas lentas (`slow_query_log` y `long_query_time` en MySQL, `log_min_duration_statement` en PostgreSQL), usando `pg_stat_statements` o Performance Schema, y analizando el top SQL de Database Insights; después se ejecuta `EXPLAIN` para corregir planes e índices.

<!-- challenge -->

Un desarrollador cambió el tamaño de una base de producción en horario laboral y causó una caída. ¿Qué controles lo evitan?

<!-- solution -->

Una política IAM que niegue `rds:ModifyDBInstance` sobre instancias con tag de prod salvo para un rol de DBA, cambios desplegados por IaC con revisión, y modificaciones programadas en la ventana de mantenimiento en vez de aplicadas de inmediato.

<!-- takeaways -->

- Los logs de auditoría y activity streams rastrean el acceso a datos.
- CloudTrail rastrea los cambios en recursos de RDS.
- Las barandas IAM y la IaC evitan cambios riesgosos.

<!-- stage: Operar RDS -->

### Monitoreo y rendimiento

<!-- unit: Métricas, logs y eventos -->

<!-- goals -->

- Saber qué métricas, herramientas y logs vigilar en RDS.
- Configurar alertas y notificaciones de eventos.

<!-- concept -->

RDS da tres niveles de visibilidad. Las métricas de CloudWatch muestran los signos vitales de la instancia. Enhanced Monitoring muestra el sistema operativo de abajo, por proceso. Performance Insights muestra en qué está ocupada la base, desglosado por esperas y consultas, que es donde suele estar la respuesta.

Logs y eventos completan el cuadro: los slow query logs muestran sentencias costosas y las notificaciones de eventos avisan de failovers, reinicios y alertas de almacenamiento cuando pasan.

<!-- example -->

| Métrica | Preocúpate cuando |
|---|---|
| `CPUUtilization` | sostenida > 80 % |
| `FreeableMemory` | baja y `SwapUsage` subiendo |
| `FreeStorageSpace` | por debajo del 15 % |
| `DatabaseConnections` | cerca de `max_connections` |
| `ReadLatency` / `WriteLatency` | sube junto con `DiskQueueDepth` |
| `ReplicaLag` | por encima de lo que toleran los lectores |

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

<!-- challenge -->

La CPU de una base está al 95 % y el equipo planea duplicar el tamaño de la instancia. ¿Qué revisas primero?

<!-- solution -->

Performance Insights: qué consultas y eventos de espera forman la carga. A menudo unas pocas consultas sin índices o con malos planes dominan; arreglarlas sale más barato que una instancia más grande.

<!-- takeaways -->

- Métricas para signos vitales, Enhanced Monitoring para el sistema, Insights para la carga.
- Los slow query logs encuentran sentencias costosas.
- Alerta sobre CPU, memoria, almacenamiento, conexiones, latencia y lag.

<!-- unit: Diagnosticar la carga -->

<!-- goals -->

- Encontrar las causas de CPU alta y poca memoria.
- Ubicar consultas lentas y esperas por locks.

<!-- concept -->

La carga de una base tiene pocas causas de fondo: consultas que hacen demasiado trabajo, demasiadas sesiones a la vez, memoria insuficiente para el conjunto de trabajo y sesiones esperándose entre sí. Las herramientas señalan cuál aplica. Performance Insights muestra las consultas y esperas principales; los slow logs y las estadísticas de consultas muestran qué sentencias cuestan más; las métricas de memoria muestran si la caché alcanza.

Arreglar la causa, normalmente una consulta o un índice, es mejor que agregar hardware.

<!-- example -->

```sql
-- PostgreSQL: top statements by total time
SELECT left(query, 80) AS query, calls, round(total_exec_time) AS total_ms, round(mean_exec_time) AS mean_ms
FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 10;
```

#### ¿Cómo se ajusta MySQL en RDS?

Dimensionando `innodb_buffer_pool_size` (por defecto alrededor del 75 % de la memoria), revisando `max_connections`, usando índices y planes adecuados, vigilando el log de consultas lentas y evitando transacciones largas que hacen crecer los undo logs.

#### ¿Por qué importa el autovacuum en RDS PostgreSQL?

El MVCC de PostgreSQL deja tuplas muertas tras los updates y deletes; el autovacuum las recupera y evita el wraparound del ID de transacción. Si se atrasa, las tablas se inflan y, en el peor caso, la base deja de aceptar escrituras para evitar el wraparound. Ajústalo para las tablas grandes y activas.

#### ¿Qué es `FreeableMemory` y cuándo debe preocuparte?

La RAM disponible en la instancia. Poca memoria libre con un `SwapUsage` en aumento significa que la carga no cabe (buffer pool, conexiones, ordenamientos); escala o reduce el consumo de memoria.

#### ¿Cómo aparecen los bloqueos en las herramientas de rendimiento de RDS?

Como eventos de espera (por ejemplo `Lock:transactionid` o `Lock:relation` en PostgreSQL, `synch/cond/innodb/row_lock_wait` en MySQL) en Database Insights; consultas sobre `pg_locks` con `pg_stat_activity` muestran quién bloquea a quién.

<!-- challenge -->

Performance Insights muestra casi toda la carga como esperas `Lock:transactionid` en PostgreSQL. ¿Qué significa y qué buscas?

<!-- solution -->

Las sesiones esperan a que otras transacciones hagan commit o rollback, normalmente sobre las mismas filas. Busca sesiones largas o idle in transaction que retengan locks (`pg_stat_activity`, `pg_locks`) y acorta o reordena las transacciones involucradas.

<!-- takeaways -->

- La mayoría de la carga viene de consultas costosas o demasiadas sesiones.
- `pg_stat_statements` y los slow logs ordenan las consultas costosas.
- Las esperas por locks apuntan a transacciones largas o en conflicto.

<!-- unit: Conexiones y RDS Proxy -->

<!-- goals -->

- Diagnosticar el agotamiento de conexiones.
- Usar RDS Proxy para muchos clientes de vida corta.

<!-- concept -->

Cada conexión a la base cuesta memoria, y los motores tienen un máximo. Las aplicaciones sin pool, y sobre todo las funciones serverless que escalan a cientos de copias, pueden agotarlo en segundos durante un pico.

RDS Proxy se ubica entre los clientes y la base y comparte un pool pequeño de conexiones entre muchos clientes. Además acelera el failover y se integra con IAM y Secrets Manager, lo que lo vuelve el arreglo por defecto en arquitecturas con mucho Lambda.

<!-- example -->

```text
800 Lambda invocations ─► RDS Proxy (pool: 80 connections) ─► RDS (max_connections 200)
without proxy:          800 direct connections ─► "too many connections"
```

#### ¿Cómo se encuentran los índices sin uso en PostgreSQL en RDS?

Consultando `pg_stat_user_indexes` para los índices con `idx_scan = 0` durante un periodo largo (excluyendo los de restricciones) y borrándolos tras verificar, porque cuestan rendimiento de escritura y almacenamiento.

#### ¿Cómo se identifican las transacciones largas en PostgreSQL?

Consultando `pg_stat_activity` para las sesiones con un `xact_start` antiguo, sobre todo `idle in transaction`; bloquean el vacuum y causan bloat. Define `idle_in_transaction_session_timeout` para proteger la base.

#### ¿Qué logs puede publicar RDS en CloudWatch Logs?

Logs de errores, de consultas lentas, generales (MySQL), los logs de PostgreSQL (incluida la salida de `log_min_duration_statement` y de `pgaudit`), logs de auditoría, de actualización y del agente, según el motor y la configuración.

#### ¿Cómo se generan alertas sobre problemas de RDS?

Con alarmas de CloudWatch sobre CPU, almacenamiento libre, memoria libre, conexiones, retraso de réplica, latencias de lectura y escritura y saldo de ráfaga; reglas de EventBridge sobre los eventos de RDS (failover, almacenamiento lleno, mantenimiento); y la detección de anomalías de Database Insights.

#### ¿Cómo se escala verticalmente una instancia de RDS?

Modificando la clase de instancia (por ejemplo de `db.r6g.large` a `db.r6g.2xlarge`), de inmediato o en la ventana de mantenimiento. Requiere una breve interrupción, que Multi-AZ acorta (se modifica primero la standby y luego hay failover).

<!-- challenge -->

Subir `max_connections` de 500 a 5.000 detuvo los errores, pero la base se volvió más lenta. ¿Por qué?

<!-- solution -->

Cada conexión consume memoria y CPU para su planificación, así que miles de conexiones aprietan la caché y suman contención. Mantén un límite moderado y usa pools de conexiones (en la app o con RDS Proxy).

<!-- takeaways -->

- Los clientes sin pool y serverless agotan las conexiones.
- RDS Proxy agrupa y comparte conexiones.
- Subir `max_connections` no es un arreglo.

<!-- unit: Afinar el motor -->

<!-- goals -->

- Afinar parámetros de PostgreSQL y MySQL en RDS.
- Mantener sano PostgreSQL: autovacuum, índices y transacciones.

<!-- concept -->

Los valores por defecto son suposiciones seguras, no ajustes afinados. Los parámetros de memoria deciden cuánto de los datos queda en caché; los de logging, qué puedes ver; y en PostgreSQL, el autovacuum decide si las filas muertas se limpian antes de que las tablas se inflen.

Muchos problemas de PostgreSQL vienen de lo que frena esa limpieza: transacciones largas o inactivas, replication slots abandonados e índices sin uso que ralentizan cada escritura. Revisarlos con regularidad es parte de operar el motor.

<!-- example -->

```sql
-- sessions holding back vacuum and locks
SELECT pid, state, now() - xact_start AS age, left(query, 60)
FROM pg_stat_activity
WHERE xact_start < now() - interval '15 minutes'
ORDER BY xact_start;
```

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

<!-- challenge -->

Una tabla de PostgreSQL muy actualizada creció de 5 GB a 60 GB aunque el número de filas es estable. ¿Qué revisas y cambias?

<!-- solution -->

Bloat por tuplas muertas: revisa `n_dead_tup` y la actividad del autovacuum, busca transacciones largas o slots inactivos que bloqueen la limpieza, afina el autovacuum de esa tabla (scale factor más bajo) y reconstrúyela una vez (por ejemplo `pg_repack`).

<!-- takeaways -->

- Afina memoria y logging en grupos de parámetros propios.
- El autovacuum debe seguir el ritmo de updates y deletes.
- Las transacciones largas y los slots viejos bloquean la limpieza.

### Escalado

<!-- unit: Escalar hacia arriba y hacia afuera -->

<!-- goals -->

- Escalar RDS verticalmente y escalar lecturas horizontalmente.
- Reconocer cuándo las escrituras necesitan otro diseño.

<!-- concept -->

Las bases relacionales escalan lecturas más fácil que escrituras. Las lecturas se reparten entre réplicas y cachés; todas las escrituras pasan por un primario. Así que el primer paso ante presión de escrituras es una instancia más grande, luego abaratar las escrituras y solo después cambios estructurales como dividir la base por dominio o pasar a un motor que escale escrituras horizontalmente.

Dividir es tanto una decisión organizacional como técnica: bases separadas encajan con responsables y cargas separadas.

<!-- example -->

| Presión | Primer paso | Siguiente |
|---|---|---|
| CPU por lecturas | Réplicas de lectura, caché | Afinar consultas |
| CPU por escrituras | Clase de instancia más grande | Escrituras por lotes, menos índices, dividir por dominio |
| Una tabla enorme | Particionado | Archivar datos viejos |

#### ¿Cómo ayuda la caché a una base de datos RDS?

ElastiCache (Redis o Memcached) o las cachés de la aplicación sirven desde memoria las lecturas repetidas (sesiones, catálogos de productos, resultados calculados), reduciendo la carga y la latencia de la base. La estrategia de invalidación es la parte difícil.

#### ¿Cuándo conviene dividir una base de datos en varias?

Cuando distintos dominios o servicios tienen cargas, necesidades de escalado o responsables independientes, cuando los picos de una carga afectan a otras, o por el principio de microservicios de una base de datos por servicio.

#### ¿Qué es Amazon Aurora?

Una base de datos relacional compatible con MySQL y PostgreSQL construida para la nube, con una capa de almacenamiento distribuida y tolerante a fallos compartida por el escritor y las réplicas. Ofrece más rendimiento que los motores estándar, un failover más rápido y un almacenamiento que crece automáticamente.

#### ¿Cómo funciona el almacenamiento de Aurora?

Los datos se guardan en un volumen de cluster replicado seis veces en tres zonas de disponibilidad, en segmentos de 10 GB. Las escrituras necesitan cuatro de seis copias y las lecturas tres de seis, así que el cluster tolera perder una AZ más otra copia. El almacenamiento escala solo hasta 128 TiB.

<!-- challenge -->

Las escrituras de una base se duplicaron tras una nueva función, y la clase de instancia más grande está cerca de su límite. ¿Qué opciones quedan?

<!-- solution -->

Abaratar las escrituras (inserts por lotes, quitar índices sin uso, evitar amplificación de escrituras), mover los datos de la función a su propia base o a un almacén específico como DynamoDB, o pasar a un motor con escalado horizontal de escrituras (por ejemplo Aurora Limitless).

<!-- takeaways -->

- Las lecturas escalan hacia afuera; las escrituras pasan por un primario.
- Primero escala hacia arriba, luego abarata las escrituras.
- Divide las bases según dominios y responsables.

<!-- unit: Límites ocultos y alivios -->

<!-- goals -->

- Reconocer límites por CPU burstable y por topes de I/O de la instancia.
- Aliviar la presión con caché, particionado y cambios de almacenamiento.

<!-- concept -->

Algunas lentitudes vienen de límites poco evidentes. Las instancias burstable van rápido hasta que se les acaban los créditos de CPU. Cada clase de instancia tiene un tope de I/O, así que un almacenamiento con más IOPS de las que permite la clase no da ningún beneficio.

Otros alivios no tocan la instancia: las cachés absorben lecturas repetidas, y particionar tablas grandes deja que consultas y mantenimiento trabajen sobre piezas más pequeñas.

<!-- example -->

```sql
-- PostgreSQL declarative partitioning by month
CREATE TABLE events (id bigint, created_at timestamptz NOT NULL, payload jsonb)
PARTITION BY RANGE (created_at);
CREATE TABLE events_2026_10 PARTITION OF events
  FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
```

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

<!-- challenge -->

Una `db.t3.medium` va bien durante semanas y luego se vuelve muy lenta cada día desde las 14:00. La CPU marca 20 %. ¿Qué pasa?

<!-- solution -->

La instancia agotó sus créditos de CPU y quedó limitada a su base, cerca del 20 % para esta clase. Pasar a una clase no burstable (por ejemplo `db.m7g`) o activar el modo unlimited, si la carga sostenida es la esperada.

<!-- takeaways -->

- Las clases burstable se limitan cuando se agotan los créditos.
- Las clases de instancia ponen tope al I/O sin importar el almacenamiento.
- Cachés y particionado alivian la carga sin instancias más grandes.

### Aurora

<!-- unit: Qué cuesta RDS -->

<!-- goals -->

- Identificar los factores de costo de un despliegue RDS.
- Tener en cuenta Multi-AZ, backups y transferencia de datos.

<!-- concept -->

Una factura de RDS tiene pocas líneas: horas de instancia, almacenamiento y su rendimiento, backups por encima de lo gratuito y transferencia de datos. Las decisiones de disponibilidad multiplican la línea de cómputo: Multi-AZ corre una segunda instancia y cada réplica es otra instancia.

La transferencia es fácil de olvidar. La replicación dentro de Multi-AZ es gratis, pero las aplicaciones que hablan con una base en otra zona pagan el tráfico entre zonas.

<!-- example -->

```text
db.r7g.large single-AZ        ~ 1 × instance price
db.r7g.large Multi-AZ         ~ 2 × instance price
+ 2 read replicas             ~ 4 × instance price
+ gp3 storage, extra IOPS, backups beyond DB size, cross-AZ app traffic
```

#### ¿Qué es Aurora Backtrack?

Una función de Aurora MySQL que retrocede el cluster en su lugar a un momento anterior dentro de una ventana configurada, sin restaurar desde un backup, útil para deshacer errores rápidamente.

#### ¿Qué son Aurora Standard y Aurora I/O-Optimized?

Dos configuraciones de almacenamiento: Standard factura las solicitudes de E/S aparte (más barato con poca E/S), I/O-Optimized incluye la E/S en un precio mayor de almacenamiento e instancia (más barato cuando la E/S supera aproximadamente un cuarto del costo de la base).

#### ¿Qué es la integración zero-ETL de Aurora con Redshift?

Una integración administrada que replica los datos de Aurora (y de algunos motores de RDS) en Amazon Redshift casi en tiempo real sin construir pipelines, para hacer analítica en Redshift con datos operativos frescos.

#### ¿Qué es Babelfish for Aurora PostgreSQL?

Una capacidad que permite a Aurora PostgreSQL entender el T-SQL y el protocolo TDS de SQL Server, para que las aplicaciones escritas para SQL Server funcionen con menos cambios de código.

<!-- challenge -->

La factura de RDS muestra costos altos de almacenamiento de backups para una base de 500 GB. ¿Cuáles son las causas probables?

<!-- solution -->

Retención larga con muchos cambios (logs y snapshots diarios suman), muchos snapshots manuales nunca borrados y copias guardadas en otras regiones. Revisar la retención, borrar snapshots manuales obsoletos y pasar las copias de largo plazo a AWS Backup con reglas de ciclo de vida.

<!-- takeaways -->

- Cómputo, almacenamiento, backups y transferencia mueven el costo.
- Multi-AZ duplica aproximadamente el cómputo.
- El tráfico de aplicaciones entre zonas se factura.

<!-- unit: Ahorrar en RDS -->

<!-- goals -->

- Ajustar el tamaño de las instancias y comprometer con Reserved Instances.
- Recortar costos en bases de desarrollo e inactivas.

<!-- concept -->

El ahorro viene de tres movimientos: usar el tamaño correcto, pagar menos por lo que corre todo el tiempo y dejar de pagar lo que no necesita correr. Las métricas de varias semanas muestran instancias sobredimensionadas; las Reserved Instances descuentan las de producción estables; las clases Graviton cuestan menos por el mismo trabajo.

Las bases de desarrollo son la ganancia fácil: más pequeñas, single-AZ, detenidas fuera del horario laboral o reemplazadas por capacidad serverless.

<!-- example -->

| Base | Cambio | Efecto |
|---|---|---|
| Prod, 24/7, estable | Reserved Instance a 3 años, Graviton | Gran descuento |
| Prod, CPU al 10 % durante meses | Un tamaño menos | La mitad de cómputo |
| Dev | Single-AZ, detenida noches y fines de semana | ~70 % menos |

#### ¿Qué es la Data API de Aurora?

Una API HTTP para ejecutar SQL sobre Aurora (Serverless v2 y aprovisionado) sin administrar conexiones ni drivers, cómoda para Lambda y otras aplicaciones serverless.

#### ¿Qué es Aurora DSQL?

Una base de datos SQL distribuida y serverless compatible con PostgreSQL, diseñada para aplicaciones activo-activo multirregión, que escala lecturas y escrituras horizontalmente con consistencia fuerte. Es distinta del Aurora estándar y tiene algunas limitaciones de funciones de PostgreSQL.

#### ¿Cuándo elegirías Aurora en lugar de RDS para PostgreSQL o MySQL?

Cuando necesitas más rendimiento, un failover más rápido, muchas réplicas con poco retraso, replicación global, clonado rápido o escalado serverless. El RDS estándar puede ser más barato para cargas pequeñas o estables y a veces admite antes ciertas funciones o versiones del motor.

#### ¿Qué son los endpoints personalizados de Aurora?

Endpoints que apuntan a un subconjunto elegido de las instancias de un cluster, por ejemplo réplicas más grandes para consultas analíticas y más pequeñas para las lecturas de la aplicación.

<!-- challenge -->

Diez bases de desarrollo corren Multi-AZ 24/7 con la misma clase que producción. Estima las principales palancas de ahorro.

<!-- solution -->

Pasarlas a single-AZ (cerca de la mitad), a clases más pequeñas o burstable, y programar el stop/start solo en horario laboral (cerca de 70 % menos de tiempo). Juntas, ahorros por encima del 80 % son realistas.

<!-- takeaways -->

- Ajusta el tamaño con semanas de métricas.
- Reserva las instancias estables; prefiere Graviton.
- Bases de dev: pequeñas, single-AZ, programadas.

<!-- stage: Motores y funciones -->

### Motores y funciones

<!-- unit: Arquitectura de Aurora -->

<!-- goals -->

- Explicar cómo el almacenamiento compartido de Aurora cambia la disponibilidad.
- Describir clusters, niveles de failover y backups.

<!-- concept -->

Aurora separa cómputo de almacenamiento. Las instancias no tienen discos propios; comparten un volumen de cluster que guarda seis copias en tres zonas y se repara solo. Las réplicas leen el mismo almacenamiento, así su lag es de milisegundos y pueden tomar el control sin copiar datos.

Como el almacenamiento se encarga de la durabilidad, el failover es más rápido que en Multi-AZ clásico, los backups corren de forma continua sin afectar el rendimiento y decides qué réplica se promueve primero con los niveles de failover.

<!-- example -->

```text
writer (AZ a)   reader tier-0 (AZ b)   reader tier-1 (AZ c)
      │                 │                     │
      └──────── shared cluster volume: 6 copies across 3 AZs ────────┘
```

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

<!-- challenge -->

Un cluster Aurora tiene un lector grande para analítica y uno pequeño. Tras un failover, el pequeño quedó como escritor y producción se volvió lenta. ¿Cómo lo evitas?

<!-- solution -->

Fijar niveles de failover: dar nivel 0 a un lector del tamaño del escritor para que se promueva primero, y poner los lectores de analítica o pequeños en niveles de menor prioridad.

<!-- takeaways -->

- Las instancias de Aurora comparten un volumen replicado seis veces.
- Las réplicas tienen lag de milisegundos y conmutan rápido.
- Los niveles de failover deciden qué réplica será el escritor.

<!-- unit: Endpoints y escalado de lecturas -->

<!-- goals -->

- Enrutar tráfico con endpoints de cluster, de lectura y personalizados.
- Acelerar lecturas con parallel query y Optimized Reads.

<!-- concept -->

Un cluster Aurora expone varios endpoints. El de cluster sigue al escritor; el de lectura reparte las conexiones nuevas entre réplicas; los personalizados apuntan a instancias elegidas, por ejemplo lectores grandes para reportes.

El balanceo ocurre por conexión mediante DNS, no por consulta, así que los pools de larga vida pueden quedarse pegados a una réplica. Funciones como parallel query y Optimized Reads llevan algunas cargas más allá de lo que dan las réplicas simples.

<!-- example -->

```bash
aws rds create-db-cluster-endpoint --db-cluster-identifier orders-aurora \
  --db-cluster-endpoint-identifier reporting --endpoint-type READER \
  --static-members orders-reader-xl-1 orders-reader-xl-2
```

#### ¿Se pueden mezclar Aurora Serverless v2 e instancias aprovisionadas?

Sí. Un cluster puede tener un escritor aprovisionado y lectores Serverless v2 (o al revés), lo que es útil con tráfico de lectura variable.

#### ¿Qué extensiones de PostgreSQL son útiles en RDS?

`pg_stat_statements` (estadísticas de consultas), `PostGIS` (geoespacial), `pgvector` (búsqueda vectorial), `pg_partman` (gestión de particiones), `pg_cron` (jobs programados), `aws_s3` (importar/exportar con S3), `pgaudit`, `pg_repack` y `postgres_fdw`. Solo se pueden instalar las extensiones admitidas.

#### ¿Cómo se cargan datos desde S3 en RDS PostgreSQL?

Con la extensión `aws_s3`: `SELECT aws_s3.table_import_from_s3('tabla', 'col1,col2', '(format csv, header true)', aws_commons.create_s3_uri('bucket', 'archivo.csv', 'eu-west-1'));`, con un rol IAM asociado a la instancia.

#### ¿Qué es un despliegue Blue/Green?

Una función (MySQL, MariaDB, PostgreSQL, Aurora) que crea una copia de staging (green) sincronizada con producción (blue) mediante replicación lógica, te deja actualizarla o cambiarla y luego hace el cambio en alrededor de un minuto con salvaguardas, conservando los mismos endpoints.

<!-- challenge -->

Existen tres réplicas, pero una recibe casi todo el tráfico de lectura. La app usa un pool de conexiones abierto al arrancar. ¿Por qué?

<!-- solution -->

El endpoint de lectura balancea al conectar mediante DNS, así que las conexiones del pool cayeron casi todas en una réplica y ahí se quedan. Recicla las conexiones periódicamente, usa un wrapper de driver que balancee entre lectores o usa endpoints personalizados.

<!-- takeaways -->

- Los endpoints de cluster, lectura y personalizados enrutan el tráfico.
- El balanceo de lectura es por conexión, no por consulta.
- Parallel query y Optimized Reads ayudan a cargas concretas.

<!-- unit: Opciones de capacidad y almacenamiento -->

<!-- goals -->

- Elegir entre clusters aprovisionados, Serverless v2 y mixtos.
- Elegir almacenamiento Standard o I/O-Optimized, y conocer Limitless y DSQL.

<!-- concept -->

Aurora ofrece varias formas de pagar la capacidad. Las instancias aprovisionadas encajan con carga estable; Serverless v2 escala la capacidad en pasos pequeños con la demanda, y ambos pueden mezclarse en un cluster. El almacenamiento tiene dos modos de facturación: pagar por I/O, o pagar más por almacenamiento sin cargos de I/O, lo que gana en cargas intensivas en I/O.

Para escalar escrituras más allá de una instancia, Limitless reparte tablas de PostgreSQL en shards, y DSQL ofrece una base SQL distribuida y serverless entre regiones.

<!-- example -->

| Carga | Opción |
|---|---|
| OLTP estable, 24/7 | Aprovisionado |
| Con picos o dev/test | Serverless v2 |
| Costo de I/O > ~25 % de la factura | I/O-Optimized |
| Escrituras más allá de una instancia | Limitless Database |

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

<!-- challenge -->

El 60 % de la factura de un cluster Aurora son cargos de I/O. ¿Qué cambias y cómo confirmas el beneficio?

<!-- solution -->

Pasar el cluster a Aurora I/O-Optimized, que elimina los cargos por I/O a cambio de un precio mayor de instancia y almacenamiento. Compara los costos de I/O, instancia y almacenamiento de los últimos meses con los precios de I/O-Optimized antes de cambiar; compensa cuando domina el I/O.

<!-- takeaways -->

- Aprovisionado para carga estable; Serverless v2 para carga variable.
- I/O-Optimized gana cuando el I/O domina la factura.
- Limitless y DSQL atacan el escalado de escrituras y el multi-región.

<!-- unit: Bases globales, clonación y Backtrack -->

<!-- goals -->

- Usar Aurora Global Database para lecturas entre regiones y DR.
- Crear clones rápidos y rebobinar con Backtrack.

<!-- concept -->

La capa de almacenamiento de Aurora abarata cosas que en otros motores son caras. Global Database replica a nivel de almacenamiento hacia otras regiones con cerca de un segundo de lag, así una región remota puede servir lecturas y tomar el control en un desastre.

La clonación crea un cluster nuevo que comparte páginas con el origen hasta que cambian, así una copia completa aparece en minutos y cuesta poco. Backtrack, en Aurora MySQL, rebobina un cluster en el sitio a un momento anterior.

<!-- example -->

```bash
aws rds restore-db-cluster-to-point-in-time --source-db-cluster-identifier orders-aurora \
  --db-cluster-identifier orders-clone-qa --restore-type copy-on-write --use-latest-restorable-time
```

#### ¿Qué opciones de licenciamiento hay para Oracle y SQL Server en RDS?

License Included (la licencia va en el precio por hora) o Bring Your Own License para Oracle; SQL Server suele ser License Included, eligiendo la edición (Express, Web, Standard, Enterprise).

#### ¿Cómo se usa `pgvector` en RDS PostgreSQL?

Instalando la extensión, creando columnas `vector` para los embeddings e indexándolas con índices HNSW o IVFFlat para búsquedas por similitud, lo que permite hacer generación aumentada por recuperación sin una base vectorial aparte.

#### ¿Para qué se usa la replicación lógica en RDS PostgreSQL?

Para replicar tablas seleccionadas a otra base PostgreSQL (actualizaciones, migraciones, dividir bases o alimentar analítica), CDC hacia sistemas externos y los despliegues Blue/Green.

<!-- challenge -->

QA necesita cada mañana una copia completa de una base de producción de 3 TB, pero las restauraciones tardan horas. ¿Qué usas?

<!-- solution -->

Clonación rápida de Aurora (copy-on-write): el clon está listo en minutos y solo guarda las páginas que cambian. Bórralo y recréalo cada mañana, y enmascara los datos sensibles si QA no debe verlos.

<!-- takeaways -->

- Global Database replica entre regiones con ~1 s de lag.
- Los clones comparten almacenamiento hasta que las páginas cambian.
- Backtrack rebobina Aurora MySQL en el sitio.

<!-- unit: Integraciones y cuándo elegir Aurora -->

<!-- goals -->

- Usar zero-ETL, Babelfish y la Data API.
- Decidir cuándo vale la pena Aurora frente a RDS.

<!-- concept -->

Aurora agrega integraciones que eliminan piezas enteras de fontanería. Zero-ETL replica datos a Redshift de forma continua sin pipelines. Babelfish permite que aplicaciones SQL Server hablen con PostgreSQL. La Data API corre SQL por HTTP sin gestionar conexiones.

Elegir Aurora frente a RDS estándar depende de la necesidad: failover más rápido, muchas réplicas con poco lag, replicación global, clonación o estas integraciones. Para bases pequeñas y estables, RDS estándar suele salir más barato.

<!-- example -->

| Necesidad | Función de Aurora |
|---|---|
| Analítica en Redshift sin ETL | Integración zero-ETL |
| Pasar gradualmente una app SQL Server a PostgreSQL | Babelfish |
| Consultar desde Lambda sin pools de conexiones | Data API |

#### ¿Qué ventajas tienen las funciones de MySQL 8.0+ en RDS para el trabajo con datos?

Funciones de ventana, CTE (incluidas las recursivas), funciones JSON, índices invisibles, `ADD COLUMN` instantáneo en muchos cambios y mejores estadísticas del optimizador, que facilitan las consultas analíticas y los cambios de esquema.

#### ¿Cómo se ejecutan migraciones de esquema seguras sobre tablas grandes?

Usando operaciones compatibles con el trabajo en línea (DDL instantáneo en MySQL 8, `CREATE INDEX CONCURRENTLY` en PostgreSQL), herramientas como `gh-ost` o `pt-online-schema-change` para MySQL, despliegues Blue/Green, y midiendo el tiempo de la migración sobre un clon.

#### ¿Qué impulsa los costos de RDS?

Las horas de instancia (por clase; Multi-AZ duplica el cómputo), el almacenamiento (por tipo y tamaño, más las IOPS aprovisionadas), el almacenamiento de backups por encima del gratuito, la transferencia de datos de salida y entre AZ o regiones, las tarifas de Extended Support, y funciones como RDS Proxy y el modo avanzado de Database Insights.

#### ¿Cómo se reducen los costos de RDS?

Dimensionando bien las instancias según las métricas, usando clases Graviton, comprando Reserved Instances para las cargas estables, usando gp3 en lugar de io1 sobreaprovisionado, deteniendo de noche las instancias que no son de producción, limpiando los snapshots viejos, usando Aurora Serverless v2 o I/O-Optimized donde encajen y descargando lecturas en cachés.

<!-- challenge -->

Un equipo corre una base PostgreSQL de 50 GB con poco tráfico y pide pasarse a Aurora "porque es mejor". ¿Qué preguntas antes de aceptar?

<!-- solution -->

Qué problema resuelve: tiempo de failover, réplicas, lecturas globales, clonación o integraciones. Si nada de eso importa, RDS for PostgreSQL estándar probablemente es más barato y simple; si importa, compara costos incluido el I/O.

<!-- takeaways -->

- Zero-ETL alimenta Redshift sin pipelines.
- Babelfish y la Data API facilitan la integración.
- Elige Aurora por necesidades concretas, no por defecto.

### Costos

<!-- unit: Extensiones de PostgreSQL -->

<!-- goals -->

- Usar extensiones comunes de PostgreSQL en RDS.
- Cargar desde S3, programar jobs y replicar tablas lógicamente.

<!-- concept -->

Las extensiones de PostgreSQL lo vuelven una plataforma: estadísticas de consultas, datos geoespaciales, búsqueda vectorial, jobs programados e importación directa desde S3. RDS soporta una lista curada, que cubre casi todas las necesidades sin acceso al sistema.

La replicación lógica es la otra pieza: transmite los cambios de tablas elegidas a otra base, en lo que se apoyan actualizaciones, migraciones y CDC.

<!-- example -->

```sql
CREATE EXTENSION IF NOT EXISTS aws_s3 CASCADE;
SELECT aws_s3.table_import_from_s3('staging.orders', '', '(format csv, header true)',
       aws_commons.create_s3_uri('landing-bucket', 'orders/2026-10-17.csv', 'eu-west-1'));
CREATE EXTENSION IF NOT EXISTS pg_cron;
SELECT cron.schedule('refresh-mv', '0 * * * *', 'REFRESH MATERIALIZED VIEW CONCURRENTLY marts.sales_hourly');
```

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

<!-- challenge -->

Una app necesita búsqueda por similitud sobre 2 millones de embeddings de productos y ya usa RDS PostgreSQL. ¿Necesitas una base vectorial aparte?

<!-- solution -->

Probablemente no a ese tamaño: instala `pgvector`, guarda los embeddings en una columna `vector` y crea un índice HNSW. Considera un almacén vectorial aparte solo si los requisitos de latencia o escala superan a PostgreSQL.

<!-- takeaways -->

- Las extensiones agregan estadísticas, geoespacial, vectores y programación.
- `aws_s3` carga archivos directamente desde S3.
- La replicación lógica transmite tablas seleccionadas.

<!-- unit: Actualizaciones y cambios seguros -->

<!-- goals -->

- Planear actualizaciones de versión menor y mayor del motor.
- Usar despliegues Blue/Green y cambios de esquema en línea.

<!-- concept -->

Los motores envejecen: las versiones llegan al fin de soporte, y quedarse en ellas cuesta tarifas de Extended Support o arriesga actualizaciones forzadas. Las versiones menores pueden aplicarse solas; las mayores necesitan pruebas porque cambian extensiones, parámetros y planes de consulta.

Los despliegues Blue/Green hacen más seguros las actualizaciones y los cambios grandes: una copia sincronizada se cambia y se prueba mientras producción sigue corriendo, y el switchover toma cerca de un minuto. Los cambios de esquema en tablas grandes necesitan operaciones en línea por la misma razón.

<!-- example -->

```bash
aws rds create-blue-green-deployment --blue-green-deployment-name orders-pg16 \
  --source arn:aws:rds:eu-west-1:123456789012:db:orders-prod \
  --target-engine-version 16.4 --target-db-parameter-group-name pg16-orders
# test green, then:
aws rds switchover-blue-green-deployment --blue-green-deployment-identifier bgd-abc123
```

#### ¿Cómo se ahorra en las bases de desarrollo?

Usando instancias pequeñas o ampliables, single-AZ, programando que se detengan fuera del horario laboral, usando Aurora Serverless v2 con un mínimo bajo, restaurando desde snapshots compartidos en lugar de mantener muchas copias y borrando los entornos sin uso.

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

<!-- challenge -->

Agregar un índice a una tabla PostgreSQL de 400 GB bloqueó las escrituras 20 minutos en producción. ¿Cómo debió hacerse?

<!-- solution -->

Con `CREATE INDEX CONCURRENTLY`, que construye sin bloquear escrituras (más lento, y no puede ir dentro de una transacción). Probar antes la duración en un clon y correrlo con poco tráfico.

<!-- takeaways -->

- Planea las versiones mayores; prueba sobre una copia restaurada.
- Blue/Green hace el switchover en cerca de un minuto.
- Usa DDL en línea para tablas grandes.

<!-- unit: Motores comerciales y MySQL -->

<!-- goals -->

- Conocer los límites y el licenciamiento de SQL Server y Oracle en RDS.
- Usar funciones modernas de MySQL para trabajo con datos.

<!-- concept -->

Los motores comerciales en RDS traen dos consideraciones extra. Algunos privilegios y funciones están restringidos porque AWS gestiona el servidor, así que ciertas tareas de administración usan procedimientos propios de RDS. La licencia puede venir incluida en el precio por hora o traerse desde acuerdos existentes, lo que cambia mucho el costo.

MySQL 8 cerró muchas brechas del SQL analítico, con window functions, CTEs y soporte JSON, algo que importa cuando los equipos de datos lo consultan directamente.

<!-- example -->

```sql
-- MySQL 8: latest order per customer with a window function
SELECT * FROM (
  SELECT o.*, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC) AS rn
  FROM orders o
) t WHERE rn = 1;
```

#### ¿Cómo se extraen tablas grandes de RDS sin afectar la producción?

Leyendo de una réplica o de un clon o restauración reciente, exportando snapshots a S3 como Parquet, extrayendo de forma incremental por una columna updated-at o con CDC en lugar de extracciones completas, en paralelo por rangos de clave con límites, y fuera de las horas pico.

#### ¿Qué es la exportación de snapshots a S3?

Una función de RDS que exporta los datos de un snapshot a S3 en formato Parquet, particionados por tabla, sin afectar la base en marcha, listos para catalogarse con Glue y consultarse con Athena.

#### ¿Cómo leen los jobs de Glue desde RDS?

Mediante una conexión JDBC de Glue en la VPC de la base (con acceso de subred y grupo de seguridad), leyendo las tablas en paralelo con opciones de particionado y guardando las credenciales en Secrets Manager; los bookmarks o una columna de marca de agua dan las cargas incrementales.

<!-- challenge -->

Un equipo que migra SQL Server a RDS depende de `sysadmin` para sus scripts de mantenimiento. ¿Qué les dices?

<!-- solution -->

RDS no otorga `sysadmin`. Reescribe los scripts usando los privilegios del usuario maestro y los procedimientos de RDS (por ejemplo `rds_backup_database` para backups nativos), o considera RDS Custom si el control a nivel de sistema es imprescindible.

<!-- takeaways -->

- Los motores comerciales tienen privilegios restringidos en RDS.
- License Included frente a BYOL cambia el costo.
- MySQL 8 agrega window functions, CTEs y JSON.

<!-- stage: Ingeniería de datos sobre RDS -->

### Migración e ingeniería de datos

<!-- unit: Claves y normalización -->

<!-- goals -->

- Elegir claves primarias para tablas OLTP.
- Explicar por qué importa la normalización para datos transaccionales.

<!-- concept -->

Las bases transaccionales están optimizadas para muchos cambios pequeños y correctos. La normalización lo apoya guardando cada hecho una sola vez, así un update toca una fila. Las claves primarias dan a cada fila una identidad estable, de la que dependen joins, replicación y herramientas de CDC.

Diseñar claves es un equilibrio: las subrogadas son estables y compactas, las naturales tienen significado, y los enteros indexan mejor que los UUID aleatorios, aunque los UUID se generan más fácil en cualquier lado.

<!-- example -->

```sql
CREATE TABLE customers (
  customer_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,   -- surrogate
  email       text NOT NULL UNIQUE,                               -- natural key, enforced
  created_at  timestamptz NOT NULL DEFAULT now(),
  updated_at  timestamptz NOT NULL DEFAULT now()
);
```

#### ¿Cómo se cargan datos en RDS de forma eficiente?

Con carga masiva (`COPY` en PostgreSQL, `LOAD DATA` en MySQL, la extensión `aws_s3`), inserciones por lotes, desactivando o aplazando la creación de índices secundarios en las cargas iniciales, subiendo temporalmente `maintenance_work_mem` y evitando las inserciones fila por fila por la red.

#### ¿Conviene ejecutar analítica directamente en la instancia RDS de producción?

En general no. Las consultas analíticas compiten con el tráfico OLTP por CPU, memoria y E/S. Usa una réplica de lectura para reportes ligeros y, para analítica más pesada, mueve los datos a un warehouse o lakehouse con CDC, exportaciones o zero-ETL.

#### ¿Qué diferencia hay entre OLTP y OLAP, y dónde encaja RDS?

OLTP maneja muchas transacciones pequeñas (inserciones, actualizaciones, búsquedas puntuales) con consistencia fuerte; OLAP maneja lecturas grandes y agregaciones sobre el historial. RDS está hecho para OLTP; el OLAP va en Redshift, Snowflake, Databricks o Athena sobre un data lake.

#### ¿Qué es DMS Schema Conversion?

Una función administrada de DMS (sucesora del Schema Conversion Tool de escritorio en muchos casos) que evalúa y convierte esquemas y código entre motores, e informa los elementos que requieren trabajo manual.

<!-- challenge -->

Una tabla heredada no tiene clave primaria, y el CDC de DMS no puede aplicar updates en el destino. ¿Qué haces?

<!-- solution -->

Agregar una clave primaria (una columna única existente o una nueva columna identity) y reiniciar la tarea. Sin clave, las herramientas de CDC no pueden identificar a qué fila se refiere un update o delete.

<!-- takeaways -->

- Toda tabla necesita clave primaria.
- Las claves subrogadas son estables; impón las naturales con restricciones únicas.
- La normalización mantiene pequeños y consistentes los updates OLTP.

<!-- unit: Índices y concurrencia -->

<!-- goals -->

- Diseñar índices, incluidos los compuestos, y sopesar su costo.
- Entender los niveles de aislamiento y evitar deadlocks.

<!-- concept -->

Los índices cambian costo de escritura y almacenamiento por lecturas más rápidas. Un índice compuesto ayuda a las consultas que filtran por sus columnas iniciales, así el orden de columnas sigue cómo filtran las consultas. Demasiados índices ralentizan cada insert y update.

La concurrencia agrega otra capa: los niveles de aislamiento deciden qué ve una transacción de los cambios de otras, y órdenes de bloqueo en conflicto causan deadlocks. Transacciones cortas y un orden de acceso consistente evitan casi todos los problemas.

<!-- example -->

```sql
CREATE INDEX idx_orders_customer_created ON orders (customer_id, created_at);
-- uses the index:      WHERE customer_id = 42 AND created_at >= '2026-10-01'
-- uses it partially:   WHERE customer_id = 42
-- cannot use it well:  WHERE created_at >= '2026-10-01'
```

#### ¿Cómo maneja DMS las tablas grandes en la carga completa?

Con carga paralela por particiones o rangos de una columna, ajustes para los objetos grandes (LOB) y mapeos de tablas para seleccionar y transformar; las migraciones muy grandes pueden combinar una exportación masiva nativa con el CDC de DMS desde una posición conocida.

#### ¿Cómo se valida una migración?

Con la validación de datos de DMS (comparación fila por fila), conteos de filas y checksums por tabla, comparación de agregados (sumas, mínimos/máximos por rangos de clave), pruebas de la aplicación contra el destino y un periodo de funcionamiento en paralelo.

#### ¿Cuáles son las trampas comunes del CDC desde bases relacionales?

Tablas sin clave primaria (no se pueden aplicar updates), retención de logs insuficiente, transacciones grandes que generan retraso, cambios de esquema que no se propagan, diferencias de tipos (timestamps, decimales) y borrados que no se manejan después.

#### ¿Cómo se envían los cambios de RDS a Kafka?

Con Debezium sobre Kafka Connect (o Amazon MSK Connect) leyendo el binlog o la replicación lógica, produciendo un topic por tabla con los eventos de cambio, o con DMS apuntando a Kinesis o MSK.

<!-- challenge -->

Dos jobs actualizan la misma tabla de cuentas y a veces caen en deadlock. Uno actualiza en orden de ID y el otro en orden de nombre. ¿Qué cambias?

<!-- solution -->

Que ambos actualicen las filas en el mismo orden (por ejemplo por clave primaria), mantener cortas las transacciones y agregar lógica de reintento para el deadlock raro que aún ocurra.

<!-- takeaways -->

- Los índices aceleran lecturas y ralentizan escrituras.
- El orden del índice compuesto sigue los filtros de las consultas.
- Un orden de bloqueo consistente y transacciones cortas evitan deadlocks.

<!-- unit: Tablas amigables con los pipelines -->

<!-- goals -->

- Diseñar tablas que soporten extracción incremental y auditoría.
- Hacer visibles los borrados para los sistemas de abajo.

<!-- concept -->

Las tablas las lee más que la aplicación. Los pipelines de datos necesitan saber qué cambió desde la última vez, y la auditoría cuándo. Las columnas de timestamp mantenidas en cada cambio hacen posible la extracción incremental.

Los borrados son el caso difícil: una fila borrada simplemente desaparece, y un pipeline que lee cambios por timestamp nunca la ve. Los soft deletes, o el CDC, hacen visibles los borrados.

<!-- example -->

```sql
ALTER TABLE orders ADD COLUMN deleted_at timestamptz;
-- trigger keeps updated_at current on every UPDATE
CREATE TRIGGER orders_touch BEFORE UPDATE ON orders
FOR EACH ROW EXECUTE FUNCTION set_updated_at();
```

#### ¿Cómo se llevan los datos de RDS a un data lake?

Cargas completas con la exportación de snapshots a S3 o la carga completa de DMS, y luego los cambios incrementales con el CDC de DMS hacia S3 (Parquet con columnas de operación) o zero-ETL; los cambios se aplican a tablas Iceberg/Delta con `MERGE` y todo se cataloga en Glue.

#### ¿Qué es una extracción incremental por marca de agua y qué riesgos tiene?

Seleccionar las filas cuyo `updated_at` supera el último valor extraído. No ve los borrados, las filas actualizadas sin cambiar la marca de tiempo ni las filas confirmadas tarde con una marca anterior; usa una ventana de solapamiento y conciliaciones periódicas, o CDC.

<!-- challenge -->

Un pipeline incremental usa `updated_at` para copiar cambios, pero el warehouse sigue mostrando pedidos que se borraron en la app. ¿Por qué y cuáles son dos arreglos?

<!-- solution -->

Los hard deletes no dejan fila que extraer. O usar soft deletes (`deleted_at`) para que los borrados sean updates, o capturar cambios con CDC (DMS o Debezium) para recibir eventos de borrado.

<!-- takeaways -->

- `created_at` y `updated_at` permiten cargas incrementales.
- Los hard deletes son invisibles para la extracción por timestamp.
- Los soft deletes o el CDC propagan los borrados.

### SQL y diseño de bases de datos en RDS

<!-- unit: Migrar a RDS -->

<!-- goals -->

- Elegir un método de migración para motores iguales y distintos.
- Usar DMS y Schema Conversion, y validar el resultado.

<!-- concept -->

Cómo migras depende de dos preguntas: ¿es el mismo motor y cuánta inactividad se acepta? Mismo motor y una ventana de mantenimiento permiten dump y restore nativos. Inactividad mínima exige replicación continua: una carga completa seguida de captura de cambios hasta el corte.

Cambiar de motor suma conversión de esquema y código, que las herramientas automatizan solo en parte. Toda migración termina con validación, porque "corrió" no es lo mismo que "los datos coinciden".

<!-- example -->

```text
1. Schema Conversion: Oracle schema → PostgreSQL (review stored procedures by hand)
2. DMS full load (parallel by table partitions) + CDC
3. DMS data validation, row counts, checksums per table
4. Cutover: stop writes, wait for CDC lag 0, switch connection strings
```

#### ¿Cómo se evita bloquear tablas de producción al extraer?

Usando snapshots o réplicas, leyendo con aislamiento de snapshot consistente sin bloqueos (MVCC de PostgreSQL, lecturas consistentes de InnoDB), evitando `SELECT … FOR UPDATE` y las transacciones largas, y paginando por clave.

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

<!-- challenge -->

La validación muestra pequeñas diferencias numéricas entre Oracle y PostgreSQL en algunas columnas. ¿Cuál es la causa probable?

<!-- solution -->

El mapeo de tipos: un `NUMBER` de Oracle sin precisión se mapeó a un tipo de punto flotante, o hay diferencias de redondeo en funciones convertidas. Mapea esas columnas a `numeric` con la precisión correcta y vuelve a cargarlas.

<!-- takeaways -->

- Mismo motor: herramientas nativas; inactividad mínima: replicación.
- Cambiar de motor exige convertir esquema y código.
- Valida siempre los datos tras migrar.

<!-- unit: Captura de cambios -->

<!-- goals -->

- Activar CDC en RDS MySQL y PostgreSQL.
- Evitar las trampas comunes del CDC, incluidos los replication slots.

<!-- concept -->

El CDC lee el propio log de cambios de la base, que registra cada insert, update y delete sin consultar las tablas. Cada motor lo expone distinto: MySQL con el binlog, PostgreSQL con replication slots lógicos. Ambos necesitan configuración y retención suficiente del log.

El riesgo es la dependencia que crea. Si un consumidor se detiene, PostgreSQL guarda WAL para su slot hasta llenar el disco, y la falta de claves o las transacciones enormes rompen los pipelines. El CDC necesita monitoreo como cualquier sistema de producción.

<!-- example -->

```text
MySQL:      binlog_format = ROW, binlog_row_image = FULL,
            CALL mysql.rds_set_configuration('binlog retention hours', 24);
PostgreSQL: rds.logical_replication = 1, then a slot per consumer
            alert on: pg_replication_slots.active = false, retained WAL size
```

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

<!-- challenge -->

Un conector de Debezium estuvo detenido una semana por mantenimiento y el disco de PostgreSQL se llenó. ¿Qué pasó y cómo lo evitas?

<!-- solution -->

El replication slot del conector siguió reteniendo WAL mientras estaba inactivo. Alerta sobre slots inactivos y el tamaño de WAL retenido, borra los slots que ya no se usan y, en versiones recientes de PostgreSQL, fija `max_slot_wal_keep_size` como límite de seguridad.

<!-- takeaways -->

- El CDC lee el binlog o el WAL, no las tablas.
- Los slots inactivos de PostgreSQL retienen WAL hasta llenar el disco.
- Claves, retención y monitoreo hacen confiable el CDC.

<!-- unit: Extraer para analítica -->

<!-- goals -->

- Mantener la analítica fuera del primario de producción.
- Extraer datos sin locks, con snapshots, réplicas o exportaciones.

<!-- concept -->

Las bases OLTP atienden clientes; la analítica no debe competir con ellas. La extracción más segura lee en otro lado que el primario: una réplica, un clon o un snapshot exportado a S3 como Parquet. Cuando no queda más que leer el primario, las lecturas con snapshot consistente evitan bloquear a los escritores.

La extracción incremental por timestamp es simple pero tiene huecos: no ve los borrados ni las filas cuyo timestamp no se actualiza, y los commits tardíos pueden pasar por detrás del watermark.

<!-- example -->

```bash
aws rds start-export-task --export-task-identifier orders-2026-10-17 \
  --source-arn arn:aws:rds:eu-west-1:123456789012:snapshot:rds:orders-prod-2026-10-17-03-10 \
  --s3-bucket-name lake-raw --s3-prefix rds/orders/ \
  --iam-role-arn arn:aws:iam::123456789012:role/rds-export --kms-key-id alias/lake
```

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

<!-- challenge -->

Un job de extracción selecciona `WHERE updated_at > last_watermark` y a veces pierde filas. Nombra dos causas y un enfoque más robusto.

<!-- solution -->

Transacciones que hacen commit después de tomar el watermark pero llevan un `updated_at` anterior, y updates que no tocan `updated_at` (o hard deletes). Usar una ventana de solape con deduplicación, o pasar a CDC.

<!-- takeaways -->

- Extrae de réplicas, clones o exportaciones de snapshot.
- Las exportaciones de snapshot escriben Parquet en S3 sin cargar la base.
- Los watermarks pierden borrados y commits tardíos.

<!-- unit: Mover datos hacia y desde el lake -->

<!-- goals -->

- Leer RDS desde Glue y cargar datos en RDS de forma eficiente.
- Llevar datos de RDS a un data lake con cargas completas e incrementales.

<!-- concept -->

Los datos se mueven en ambos sentidos entre RDS y el lake. Desde RDS, una carga completa siembra el lake y el CDC lo mantiene al día, con Glue o Spark aplicando los cambios a las tablas del lake. Hacia RDS, la carga masiva supera por órdenes de magnitud a los inserts fila por fila.

Los jobs de Glue llegan a RDS mediante connections en la VPC, y las lecturas en paralelo importan en tablas grandes.

<!-- example -->

```sql
-- PostgreSQL bulk load: far faster than INSERT per row
COPY staging.products (sku, name, price) FROM STDIN WITH (FORMAT csv, HEADER true);
-- then upsert into the final table
INSERT INTO products SELECT * FROM staging.products
ON CONFLICT (sku) DO UPDATE SET name = EXCLUDED.name, price = EXCLUDED.price;
```

#### ¿Cómo le explicarías RDS a una persona no técnica?

Es AWS operando nuestras bases de datos por nosotros: las mantiene actualizadas, respaldadas y disponibles aunque falle un servidor, para que el equipo se concentre en los datos y en la aplicación en lugar de mantener máquinas.

#### Una API basada en Lambda satura de conexiones la base durante los picos de tráfico. ¿Cuál es tu solución?

Pongo RDS Proxy entre Lambda y la base con autenticación IAM, defino concurrencia reservada en la función para limitar el paralelismo, reutilizo las conexiones entre invocaciones y considero cachear las lecturas más frecuentes.

#### El retraso de una réplica de reportes llega a horas durante los batches nocturnos. ¿Qué haces?

Busco las escrituras pesadas en la primaria (jobs batch, transacciones grandes) y las divido en transacciones más pequeñas, subo la clase de instancia y las IOPS de la réplica, evito en la réplica consultas largas que choquen con la reproducción (`max_standby_streaming_delay` en PostgreSQL) y considero una copia analítica aparte.

<!-- challenge -->

Un job nocturno inserta 5 millones de filas en RDS una por una y tarda 6 horas. ¿Qué cambias?

<!-- solution -->

Carga masiva: escribir un archivo y usar `COPY` (o `aws_s3.table_import_from_s3` / `LOAD DATA`) a una tabla de staging y luego un solo upsert por conjuntos. Quitar o aplazar los índices no esenciales durante la carga si hace falta.

<!-- takeaways -->

- Carga completa más CDC mantienen al día el lake.
- Glue lee RDS mediante connections de VPC.
- La carga masiva supera a los inserts fila por fila.

<!-- stage: Integrarlo todo -->

### Escenarios

<!-- unit: Diseñar para disponibilidad y recuperación -->

<!-- goals -->

- Diseñar una base de producción para disponibilidad, seguridad y recuperación.
- Agregar un plan de recuperación ante desastres entre regiones.

<!-- concept -->

Las preguntas de diseño prueban si sabes combinar las piezas. Una respuesta sólida cubre ubicación (subredes privadas entre zonas), disponibilidad (Multi-AZ), protección (backups con restauraciones probadas, cifrado, deletion protection), acceso (usuarios de mínimo privilegio, secretos), observabilidad (métricas, logs, alarmas) y crecimiento. Luego separa la alta disponibilidad de la recuperación ante desastres y da RTO y RPO para cada una.

<!-- example -->

| Capa | Opción |
|---|---|
| Disponibilidad | Multi-AZ DB cluster (o Aurora) |
| Protección | PITR de 14 días, copias de AWS Backup en otra cuenta y región |
| Acceso | Subredes privadas, SG desde el SG de la app, Secrets Manager, RDS Proxy |
| Observabilidad | Database Insights, alarmas, notificaciones de eventos |
| DR | Réplica entre regiones (o Aurora Global Database), runbook |

#### Tu equipo debe pasar de PostgreSQL 13 a 16 con una interrupción mínima. ¿Cómo lo planificas?

Reviso la compatibilidad de extensiones y parámetros, pruebo la actualización sobre un snapshot restaurado y ejecuto las pruebas de la aplicación, y luego uso un despliegue Blue/Green: creo el entorno green, lo actualizo, dejo que se sincronice, valido y hago el cambio en una ventana corta, conservando el blue como reversión hasta estar seguro.

#### Una revisión de seguridad encuentra una instancia de RDS accesible públicamente. ¿Qué cambias?

Desactivo el acceso público, la paso a subredes privadas, restrinjo los grupos de seguridad a los orígenes de la aplicación, obligo TLS, roto las credenciales, reviso los logs en busca de accesos sospechosos y añado barreras (regla de Config, SCP) para que no se repita.

<!-- challenge -->

El negocio fija un RTO de 1 hora y un RPO de 5 minutos ante un desastre regional. ¿Lo cumple una réplica de lectura entre regiones y qué más necesitas?

<!-- solution -->

Normalmente sí: el lag de la réplica suele ser de segundos y la promoción toma minutos. También necesitas un runbook probado, infraestructura lista en la región de DR (app, secretos, failover de DNS) y simulacros periódicos.

<!-- takeaways -->

- Combina ubicación, disponibilidad, protección, acceso y observabilidad.
- Da RTO y RPO por separado para HA y DR.
- La DR solo cuenta si está probada.

<!-- unit: Datos frescos de producción para analítica -->

<!-- goals -->

- Dar a los analistas copias frescas de los datos de producción con seguridad.
- Equilibrar frescura, costo, aislamiento y privacidad.

<!-- concept -->

Los analistas quieren datos de producción, y producción quiere que la dejen tranquila. La pregunta de diseño es cómo darles una copia reciente aislada de los clientes, asequible y segura. Las opciones van de réplicas (frescas, pero cargan la replicación del primario) a clones o restauraciones diarias (aisladas, con un día de antigüedad) a exportaciones al lake (baratas, consultables con otros motores). La privacidad decide si el enmascarado forma parte de la copia.

<!-- example -->

| Opción | Frescura | Aislamiento | Notas |
|---|---|---|---|
| Réplica de lectura | Segundos | Comparte replicación | Buena para dashboards en vivo |
| Clon diario de Aurora | Diaria | Total | Rápido de crear, pagas los cambios |
| Exportación de snapshot a S3 | Diaria | Total | Parquet para Athena o Spark |

#### ¿Cómo montas un plan de recuperación ante desastres entre regiones para una base RDS MySQL?

Creo una réplica de lectura en otra región (o Aurora Global Database si es Aurora), replico los backups automáticos o copio los snapshots a la región de DR, automatizo con scripts la promoción y los cambios de DNS, mantengo lista la infraestructura de la aplicación en la región de DR y pruebo el failover periódicamente contra el RPO y el RTO.

<!-- challenge -->

La copia contiene correos y teléfonos de clientes que los analistas no deben ver. ¿En qué punto de tu diseño los quitas?

<!-- solution -->

Enmascararlos al construir la copia: correr un paso de enmascarado sobre el clon antes de dar acceso, o excluir y hashear esas columnas al exportar al lake (con permisos de columna de Lake Formation como segunda capa).

<!-- takeaways -->

- Ajusta frescura y aislamiento a la necesidad analítica.
- Clones y exportaciones aíslan la analítica de producción.
- Enmascara los datos personales antes de dar acceso.
