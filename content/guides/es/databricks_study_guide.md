## Guía de estudio de Databricks

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de Databricks: unas 250 preguntas](../../images/databricks_study_guide_title_img.png)

Unas 250 preguntas tipo entrevista sobre Databricks, desde la idea del lakehouse hasta Delta Lake, Unity Catalog, la ingesta y el streaming, los pipelines y jobs de Lakeflow, la optimización del rendimiento, la seguridad y los costos. Las respuestas reflejan la plataforma en 2026; Databricks cambia a menudo el nombre de sus productos, así que se indican los nombres anteriores cuando todavía son comunes.

La guía sigue una ruta de aprendizaje en seis etapas. Cada sección se divide en unidades cortas: objetivos de aprendizaje, una explicación del concepto y un ejemplo resuelto, luego preguntas (primero de memoria, después de aplicación), un reto práctico e ideas clave. Para **aprender**, lee cada unidad de principio a fin. Para **repasar**, cambia al modo repaso o usa "Ir a las preguntas", marca las respuestas que quieras volver a ver y prueba un repaso mixto entre secciones.

<!-- QA -->
<!-- stage: Fundamentos -->

### Fundamentos de la plataforma

<!-- unit: La idea del lakehouse -->

<!-- goals -->

- Explicar qué es un lakehouse y qué problemas del data lake resuelve.
- Ubicar las familias de productos de Databricks (Lakeflow, Mosaic AI) en ese panorama.

<!-- concept -->

Las empresas tenían dos copias de sus datos: un data lake barato de archivos para ciencia de datos y un warehouse costoso para BI. El lake no tenía transacciones, esquemas ni actualizaciones fáciles; el warehouse encerraba los datos en un formato propietario. Un lakehouse guarda una sola copia en formatos abiertos sobre almacenamiento de objetos y le suma funciones de warehouse: Delta Lake aporta transacciones, Unity Catalog gobierno, y Spark, Photon y los SQL warehouses velocidad.

Databricks vende esa plataforma. Sus familias: Lakeflow para ingeniería de datos, Databricks SQL para analítica y Mosaic AI para machine learning.

<!-- example -->

| Necesidad | Lake clásico | Warehouse | Lakehouse |
|---|---|---|---|
| Almacenamiento barato, formato abierto | Sí | No | Sí |
| Transacciones ACID, `UPDATE`/`DELETE` | No | Sí | Sí (Delta) |
| Permisos detallados | Débiles | Sí | Sí (Unity Catalog) |
| Una sola copia para BI y ML | No | No | Sí |

#### ¿Qué es Databricks?

Una plataforma de datos e IA en la nube, fundada por los creadores de Apache Spark, que funciona en AWS, Azure y Google Cloud. Reúne ingeniería de datos, analítica SQL, streaming, machine learning y gobierno sobre una sola copia de los datos, guardada en formatos abiertos (Delta Lake, Apache Iceberg) en tu propio almacenamiento en la nube.

#### ¿Qué es un lakehouse?

Una arquitectura que guarda los datos en almacenamiento de objetos barato, como un data lake, pero le añade funciones de data warehouse: transacciones ACID, esquemas, optimizaciones parecidas a los índices, gobierno detallado y SQL rápido. Evita tener una copia de los datos en un lake para ciencia de datos y otra en un warehouse para BI.

#### ¿Qué problemas del data lake clásico resuelve el lakehouse?

Los data lakes no tenían transacciones (los lectores veían datos a medio escribir), ni control de esquema (se acumulaba basura), las consultas sobre muchos archivos pequeños eran lentas, no era fácil actualizar ni borrar (un problema para el RGPD/GDPR) y el gobierno era débil. Delta Lake y Unity Catalog resuelven cada uno de estos puntos.

#### ¿Qué es Lakeflow?

El nombre general, desde 2025, de los productos de ingeniería de datos de Databricks, que ingieren, transforman y orquestan datos. Tiene cuatro partes: Lakeflow Connect (conectores de ingesta), Lakeflow pipelines (pipelines declarativos batch y de streaming, antes Delta Live Tables), Lakeflow Designer (preparación de datos visual y sin código) y Lakeflow Jobs (orquestación, antes Workflows). Todas corren sobre el Databricks Runtime y se gobiernan con Unity Catalog.

#### ¿Qué es Mosaic AI?

El conjunto de funciones de IA y ML de Databricks: entrenamiento y ajuste fino de modelos, Model Serving, Vector Search, AI Gateway, frameworks y evaluación de agentes, todo gobernado con Unity Catalog.

#### ¿Cómo le explicas el lakehouse a una persona de negocio?

Un solo lugar para todos los datos de la empresa, guardados una vez en formatos abiertos en la propia cuenta de nube de la empresa, donde los reportes, la ciencia de datos y la IA trabajan sobre las mismas cifras confiables, con permisos y registros de auditoría administrados de forma centralizada.

<!-- challenge -->

Tu jefe pregunta por qué el equipo debería dejar de exportar CSV cada noche desde el lake a un warehouse aparte. Escríbele tres frases: qué cambia, qué se gana y un riesgo.

<!-- solution -->

Reportes y modelos leerían las mismas tablas Delta, así que la copia nocturna y sus retrasos desaparecen. Las cifras coinciden entre BI y ciencia de datos, y permisos y auditoría quedan en un solo lugar. El riesgo es el esfuerzo de migración: hay que redirigir y validar los reportes antes de apagar el warehouse viejo.

<!-- takeaways -->

- Un lakehouse es una copia de los datos en formatos abiertos con funciones de warehouse encima.
- Delta Lake resuelve transacciones y esquemas; Unity Catalog, el gobierno.
- Lakeflow (ingeniería), Databricks SQL (analítica) y Mosaic AI (ML) son las familias de productos.

<!-- unit: Plano de control, workspaces y facturación -->

<!-- goals -->

- Decir dónde ejecuta Databricks tu código y dónde se quedan tus datos.
- Explicar por qué los DBU hacen que el cómputo de jobs sea más barato que el all-purpose.

<!-- concept -->

Databricks se divide en dos planos. El plano de control, en la cuenta de Databricks, aloja la app web, notebooks, planificador y metadatos del catálogo. El plano de cómputo es donde se procesan los datos: en tu cuenta cloud para clusters clásicos, en la de Databricks para serverless. Los datos en reposo siempre quedan en tu almacenamiento.

Trabajas dentro de workspaces, normalmente uno por entorno. El procesamiento se factura en DBU por segundo, con una tarifa según el tipo de cómputo: los clusters interactivos all-purpose cuestan más que el cómputo de jobs, que vive una sola ejecución.

<!-- example -->

```text
 Control plane (Databricks)        Compute plane
 ┌──────────────────────────┐      ┌─────────────────────────────┐
 │ web app, notebooks, jobs │ ───► │ classic: VMs in YOUR account│
 │ scheduler, UC metadata   │      │ serverless: Databricks acct │
 └──────────────────────────┘      └──────────────┬──────────────┘
                                                  ▼
                                   your S3 / ADLS / GCS storage
```

#### ¿Qué diferencia hay entre el plano de control y el plano de cómputo?

El plano de control lo administra Databricks en su propia cuenta: la aplicación web, los notebooks, el programador de jobs, el gestor de clusters y los metadatos de Unity Catalog. El plano de cómputo es donde se procesan los datos. Con cómputo clásico corre en tu cuenta de nube (tu VPC); con cómputo serverless corre en la cuenta de Databricks, en la misma región. En ambos casos los datos en reposo se quedan en tu almacenamiento.

#### ¿Qué es un workspace de Databricks?

El entorno donde trabajan los usuarios: notebooks, archivos, carpetas Git, jobs, pipelines, consultas SQL, dashboards, clusters y experimentos. Una empresa suele tener varios workspaces (por ejemplo dev, staging y prod), conectados a un metastore de Unity Catalog por región.

#### ¿Qué es un DBU?

Una Databricks Unit, la unidad de capacidad de procesamiento que Databricks factura por segundo. La tarifa por DBU depende del tipo de cómputo (jobs, all-purpose, SQL, serverless) y del plan. Con cómputo clásico también le pagas al proveedor de nube por las máquinas virtuales; con serverless, el precio del DBU incluye la infraestructura.

#### ¿Por qué el cómputo de jobs es más barato que el all-purpose?

El cómputo de jobs se factura a una tarifa de DBU más baja porque ejecuta cargas programadas y no interactivas, y se apaga cuando termina el job. Los clusters all-purpose son para el desarrollo interactivo, compartidos y de larga duración, así que Databricks cobra más por ellos. Correr la producción en clusters all-purpose es un error de costos clásico.

<!-- challenge -->

Un job nocturno de producción corre en el cluster all-purpose compartido del equipo y tarda una hora. Enumera dos cambios que reducen su costo sin tocar el código.

<!-- solution -->

Ejecutarlo en cómputo de jobs (o jobs serverless) en vez del cluster all-purpose, lo que baja la tarifa de DBU y termina la facturación al acabar la ejecución. Luego ajustar el tamaño del cluster del job (o usar workers spot) según sus métricas.

<!-- takeaways -->

- El plano de control es de Databricks; los datos en reposo siempre quedan en tu almacenamiento.
- Los DBU se facturan por segundo con una tarifa que depende del tipo de cómputo.
- La producción va en cómputo de jobs o serverless, no en clusters all-purpose.

<!-- unit: Trabajar en el workspace -->

<!-- goals -->

- Usar notebooks, widgets y `dbutils` en el desarrollo diario.
- Explicar por qué las carpetas Git y los volúmenes reemplazan patrones antiguos.

<!-- concept -->

La mayor parte del desarrollo ocurre en notebooks: celdas en Python, SQL, Scala o R que corren sobre el cómputo conectado. Los widgets convierten un notebook en una tarea de job parametrizada, y `dbutils` da acceso a archivos, secretos, parámetros y valores de tareas.

Dos hábitos antiguos están siendo reemplazados. El código debe vivir en carpetas Git, para revisarlo y versionarlo como cualquier repositorio. Los archivos deben vivir en volúmenes de Unity Catalog y no en DBFS, porque las rutas de DBFS no tienen permisos detallados.

<!-- example -->

Un notebook que funciona tanto de forma interactiva como tarea programada:
```python
dbutils.widgets.text("snapshot_date", "2026-10-01")    # default for interactive runs
snapshot = dbutils.widgets.get("snapshot_date")          # the job overrides it
df = spark.read.json(f"/Volumes/raw/landing/orders/{snapshot}/")
```

#### ¿Qué lenguajes se pueden usar en Databricks?

Python, SQL, Scala y R en los notebooks, además de Java y Scala en jobs JAR. Puedes mezclar lenguajes en un notebook con comandos mágicos como `%sql`, `%python`, `%scala`, `%md` (Markdown) y `%sh` (shell en el driver).

#### ¿Qué es un notebook de Databricks?

Un documento web formado por celdas que ejecutan código sobre el cómputo conectado, con resultados, gráficos, comentarios, historial de versiones y edición simultánea. Los notebooks se pueden programar como tareas de un job, parametrizar con widgets y guardar como archivos fuente en Git.

#### ¿Qué son los widgets?

Parámetros de entrada de los notebooks (texto, lista desplegable, combobox, selección múltiple). En los jobs, los parámetros de la tarea los llenan. En SQL, los parámetros se referencian con la sintaxis `:nombre`.

```python
dbutils.widgets.text("snapshot_date", "2026-10-01")
snapshot = dbutils.widgets.get("snapshot_date")
```

#### ¿Qué es `dbutils`?

Una librería de utilidades disponible en notebooks y jobs: `dbutils.fs` para archivos, `dbutils.secrets` para secretos, `dbutils.widgets` para parámetros, `dbutils.notebook.run` y `dbutils.notebook.exit` para encadenar notebooks, y `dbutils.jobs.taskValues` para pasar valores pequeños entre tareas de un job.

#### ¿Qué son las carpetas Git (antes Repos)?

Carpetas del workspace vinculadas a un repositorio Git (GitHub, GitLab, Azure DevOps, Bitbucket). Permiten clonar, crear ramas, hacer commit, pull y push desde el workspace, de modo que los notebooks y los archivos Python se versionan y se revisan como cualquier otro código.

#### ¿Qué es Genie Code?

El agente de IA integrado en el workspace, que reemplazó a Databricks Assistant en 2026. Escribe y corrige código y explica errores, y en modo agente realiza tareas de varios pasos en notebooks, el editor SQL, pipelines, dashboards y MLflow. Trabaja a partir de los metadatos de Unity Catalog, así que sus sugerencias usan tus tablas, columnas y comentarios reales, y solo ve lo que tú puedes ver.

#### ¿Qué es DBFS y por qué ya no se recomienda?

El Databricks File System, una abstracción heredada que montaba el almacenamiento en la nube bajo rutas `dbfs:/`, incluido un bucket raíz del workspace. No tiene gobierno detallado, así que Databricks recomienda ahora los volúmenes de Unity Catalog para los archivos y las tablas para los datos, y desactiva la raíz de DBFS y los montajes en las instalaciones nuevas.

<!-- challenge -->

Un compañero guarda credenciales en una celda del notebook y lee archivos de `dbfs:/mnt/raw`. ¿Qué dos cambios le sugieres?

<!-- solution -->

Mover las credenciales a un secret scope leído con `dbutils.secrets.get` (o mejor, usar una storage credential para no necesitar secretos) y reemplazar el mount por una ruta de volumen de Unity Catalog en `/Volumes/...`, para que el acceso quede gobernado y auditado.

<!-- takeaways -->

- Los widgets permiten usar el mismo notebook de forma interactiva y como tarea de job.
- El código va en carpetas Git y los archivos en volúmenes, no en DBFS.
- `dbutils` cubre archivos, secretos, widgets y valores de tareas.

<!-- unit: Runtime, Photon y desarrollo remoto -->

<!-- goals -->

- Describir qué contiene un Databricks Runtime y qué acelera Photon.
- Explicar por qué Spark Connect limita algunas APIs y cómo se desarrolla desde un IDE.

<!-- concept -->

Cada cluster corre un Databricks Runtime: Spark más Delta, conectores y optimizaciones, en versiones LTS que puedes fijar. Photon, un motor vectorizado en C++, acelera por debajo el trabajo con SQL y DataFrames.

El cómputo más reciente habla con Spark mediante Spark Connect: el cliente envía un plan lógico a un servidor remoto. Eso hace posible serverless y el desarrollo desde un IDE (Databricks Connect, la CLI), pero el código que accede a la JVM, a los RDD o a `SparkContext` ya no funciona ahí.

<!-- example -->

```python
# Works everywhere, including serverless (plain DataFrame API):
df.groupBy("country").count()

# Fails on Spark Connect (serverless, standard access mode):
spark.sparkContext.parallelize([1, 2, 3])
```

#### ¿Qué es el Databricks Runtime?

La imagen de software versionada que ejecutan los clusters: Apache Spark más Delta Lake, Photon, librerías, conectores y mejoras de rendimiento. Las versiones LTS (soporte a largo plazo) tienen soporte durante unos tres años. El runtime ML añade librerías de machine learning.

#### ¿Qué es Photon?

Un motor de consultas vectorizado escrito en C++ que ejecuta de forma nativa las operaciones de Spark SQL y DataFrame, en lugar de hacerlo en la JVM. Acelera lecturas, joins, agregaciones y escrituras, sobre todo en Delta y Parquet. Viene activado por defecto en los SQL warehouses y en serverless, y es opcional (con una tarifa de DBU más alta) en los clusters.

#### ¿Qué es Spark Connect y por qué importa en Databricks?

Un protocolo cliente-servidor en el que el cliente construye un plan lógico sin resolver y lo envía a un servidor Spark remoto. El cómputo serverless y los clusters compartidos (modo de acceso estándar) lo usan, así que el código que toca directamente el `SparkContext`, los RDD o la JVM no funciona allí. El código DataFrame y SQL funciona sin cambios.

#### ¿Qué es la CLI de Databricks?

Una herramienta de línea de comandos para administrar workspaces desde una terminal o desde CI: archivos, jobs, clusters, secretos, objetos de Unity Catalog y, sobre todo, Declarative Automation Bundles, antes Databricks Asset Bundles (`databricks bundle validate|plan|deploy|run`). Se autentica con OAuth (usuario o service principal) o con tokens.

#### ¿Qué es Databricks Connect?

Una librería que permite ejecutar código Spark desde tu IDE o un proceso Python local contra el cómputo de Databricks, a través de Spark Connect. Desarrollas y depuras en local mientras las operaciones DataFrame se ejecutan en el cluster o en serverless.

<!-- challenge -->

Quieres depurar paso a paso una transformación en tu IDE mientras los datos se quedan en Databricks. ¿Qué configuras?

<!-- solution -->

Instalar Databricks Connect acorde al runtime del cluster (o usar serverless), autenticarte con la CLI (`databricks auth login`) y correr el código localmente: las operaciones de DataFrame se ejecutan en remoto vía Spark Connect, mientras el Python corre en tu depurador.

<!-- takeaways -->

- El runtime es la imagen versionada: fija una versión LTS para producción.
- Photon acelera SQL y DataFrames, no las UDF de Python.
- Spark Connect habilita serverless y el IDE, pero prohíbe RDD y acceso a la JVM.

### Cómputo

<!-- unit: Tipos de cómputo y serverless -->

<!-- goals -->

- Elegir entre cómputo all-purpose, de jobs, SQL warehouse y serverless.
- Explicar a qué renuncias con serverless.

<!-- concept -->

Databricks adapta el cómputo a la carga. Los clusters all-purpose sirven al desarrollo interactivo, el cómputo de jobs vive una ejecución y los SQL warehouses atienden SQL y BI. Las versiones serverless de los tres arrancan en segundos y facturan solo mientras trabajan.

Serverless cambia control por comodidad: no eliges tipos de instancia ni la mayoría de configuraciones de Spark, y el código debe ser compatible con Spark Connect. Los SQL warehouses se dimensionan distinto: la talla define la velocidad de una consulta y el número de clusters cuántos usuarios consultan a la vez.

<!-- example -->

| Carga | Buena opción |
|---|---|
| Explorar datos en un notebook | All-purpose (con auto-terminación) o notebook serverless |
| Job ETL nocturno | Cómputo de jobs o jobs serverless |
| Dashboards y herramientas de BI | SQL warehouse serverless |
| Librería que necesita la JVM | Cluster clásico, modo de acceso dedicado |

#### ¿Qué tipos de cómputo ofrece Databricks?

Clusters all-purpose para el trabajo interactivo, cómputo de jobs creado para una ejecución, SQL warehouses para SQL y BI, cómputo serverless para notebooks, jobs y pipelines, e instance pools para acelerar el arranque de los clusters clásicos.

#### ¿Qué es el cómputo serverless?

Cómputo que Databricks aprovisiona y administra en su propia cuenta: arranca en segundos, escala automáticamente, siempre usa un runtime actual con Photon y solo se factura mientras trabaja. Renuncias al control de los tipos de instancia y de la configuración de Spark, y el código debe ser compatible con Spark Connect.

#### ¿Qué es un SQL warehouse?

Cómputo dedicado a las consultas SQL de Databricks SQL, las herramientas de BI y los dashboards. Tipos: serverless (arranque rápido, recomendado), pro y classic. Escala añadiendo clusters para absorber la concurrencia, y usa Photon y una gestión inteligente de la carga.

#### ¿Cómo se dimensiona un SQL warehouse?

Elige una talla (T-shirt size) según la complejidad de las consultas y el volumen de datos (más grande significa consultas individuales más rápidas), y define el número máximo de clusters para la concurrencia (más usuarios a la vez). Vigila las colas y el spill en el historial de consultas, y configura el auto-stop.

#### Un notebook funciona en tu cluster pero falla como job serverless. ¿Por qué?

Probablemente porque usa algo no admitido en serverless (Spark Connect): RDD, `sparkContext`, `cache()`, la mayoría de las llamadas a `spark.conf.set`, init scripts o librerías que necesitan la JVM. Reescríbelo con las APIs de DataFrame, declara las dependencias en el entorno y pruébalo en serverless antes de desplegarlo.

<!-- challenge -->

Los lunes en la mañana un dashboard va lento porque 40 analistas lo abren a la vez; cada consulta sola es rápida. ¿Qué parámetro del warehouse cambias?

<!-- solution -->

Subir el número máximo de clusters (escalar horizontalmente para la concurrencia), no la talla, porque las consultas individuales ya son rápidas. Revisa el historial de consultas buscando colas para confirmarlo.

<!-- takeaways -->

- Adapta el cómputo a la carga: interactiva, programada o SQL.
- Serverless arranca rápido y cobra por uso, pero exige código compatible con Spark Connect.
- La talla del warehouse es velocidad por consulta; el número de clusters, concurrencia.

<!-- unit: Clusters clásicos y modos de acceso -->

<!-- goals -->

- Describir el driver y los workers de un cluster clásico.
- Elegir el modo de acceso estándar o dedicado para una carga.

<!-- concept -->

Un cluster clásico tiene un driver, que ejecuta tu programa y planifica el trabajo, y workers cuyos executors procesan particiones en paralelo. Un cluster de un solo nodo pone todo en el driver, suficiente para datos pequeños o trabajo con pandas.

El modo de acceso decide cómo se comparte un cluster. El modo estándar permite que varios usuarios lo compartan con seguridad bajo Unity Catalog, a cambio de las restricciones de Spark Connect. El modo dedicado pertenece a un usuario o grupo y admite más APIs, que algunas librerías de ML y el trabajo con GPU requieren.

<!-- example -->

```text
 driver  ── plans stages, collects results (keep big data off it)
   ├── worker 1: executor ── tasks on partitions 1..n
   ├── worker 2: executor ── tasks on partitions n+1..m
   └── worker 3: executor ── ...
```

#### ¿Cómo está compuesto un cluster clásico?

Un nodo driver que ejecuta el programa principal, planifica el trabajo y recoge los resultados, y nodos worker con executors que procesan las particiones. Un cluster de un solo nodo lo ejecuta todo en el driver, lo cual basta para datos pequeños y para ML en una sola máquina.

#### ¿Para qué sirve un cluster de un solo nodo?

Para procesar datos pequeños, trabajar con pandas y scikit-learn y desarrollar cosas ligeras. No tiene workers, así que Spark corre en modo local en el driver: es barato, pero no escala.

#### ¿Qué son los modos de acceso?

Ajustes que controlan el aislamiento y el gobierno en el cómputo clásico. El modo estándar (antes shared) permite que varios usuarios compartan un cluster con aislamiento de Unity Catalog, usando Spark Connect. El modo dedicado (antes single user) asigna el cluster a un usuario o grupo y admite más APIs, como los RDD y algunas librerías de ML.

#### ¿Qué implica elegir entre modo estándar y dedicado para cargas de ML?

Las librerías de ML que necesitan acceso directo a la JVM o al `SparkContext`, o el entrenamiento con GPU, suelen requerir el modo de acceso dedicado o serverless con el entorno adecuado. El modo estándar es mejor para el trabajo compartido con SQL y DataFrames.

#### ¿Para qué se usan los clusters con GPU?

Para entrenar e inferir modelos de deep learning y para algunas librerías aceleradas por GPU. Necesitan un runtime ML con drivers de GPU y son caros, así que deben autoterminarse pronto.

<!-- challenge -->

El script de entrenamiento de una científica de datos llama a `spark.sparkContext` y falla en el cluster compartido del equipo. ¿Qué propones?

<!-- solution -->

Darle un cluster dedicado (usuario único), o un entorno serverless que soporte su librería, para el entrenamiento. El cluster compartido en modo estándar se queda para SQL y DataFrames.

<!-- takeaways -->

- El driver planifica y recolecta; los workers procesan.
- El modo estándar es para compartir bajo Unity Catalog; el dedicado admite más APIs.
- Los clusters de un nodo son baratos para datos pequeños; los de GPU deben terminar pronto.

<!-- unit: Escalado y control de costos -->

<!-- goals -->

- Configurar con criterio autoscaling, auto-terminación, pools e instancias spot.
- Usar políticas de cluster para mantener bajo control el cómputo de un equipo.

<!-- concept -->

La mayor parte del dinero desperdiciado en cómputo viene de clusters demasiado grandes o que nunca se apagan. El autoscaling agrega y quita workers según la carga, la auto-terminación apaga clusters inactivos y los pools mantienen VMs listas para arrancar más rápido. Las instancias spot abaratan mucho los workers tolerantes a fallos, siempre que el driver sea on-demand.

Las políticas de cluster convierten estas decisiones en valores por defecto: los administradores limitan tipos y tamaños, imponen la auto-terminación y exigen etiquetas de costo.

<!-- example -->

Un fragmento de política que todo cluster de desarrollo debe cumplir:
```json
{
  "autotermination_minutes": {"type": "range", "maxValue": 30, "defaultValue": 20},
  "num_workers": {"type": "range", "maxValue": 4},
  "custom_tags.team": {"type": "fixed", "value": "data-eng"}
}
```

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

#### ¿Cómo abaratas el desarrollo para un equipo de diez ingenieros?

Con clusters pequeños o de un solo nodo, con políticas y autoterminación corta, notebooks serverless, muestras de datos de desarrollo compartidas o shallow clones en lugar de copias completas, pruebas unitarias locales para la mayor parte de la lógica, bundles en modo desarrollo y una alerta de presupuesto por equipo.

<!-- challenge -->

El gasto de desarrollo de un equipo se duplicó tras llegar cinco ingenieros nuevos. Nombra tres controles que pones esta semana.

<!-- solution -->

Una política de cluster con tamaños máximos pequeños y auto-terminación de 20–30 minutos, notebooks serverless o un pool compartido para arranques rápidos, y una alerta de presupuesto sobre la etiqueta de costo del equipo. A más largo plazo, llevar las pruebas de lógica a tests unitarios locales.

<!-- takeaways -->

- Los clusters inactivos y sobredimensionados son el principal desperdicio; la auto-terminación resuelve el primero.
- Spot para los workers, on-demand para el driver.
- Las políticas vuelven las buenas configuraciones el valor por defecto.

<!-- unit: Librerías y diagnóstico -->

<!-- goals -->

- Instalar dependencias de forma reproducible en clusters y serverless.
- Encontrar la causa de un cluster lento o que falla.

<!-- concept -->

Las dependencias pueden adjuntarse al cluster, instalarse por notebook con `%pip` o declararse por tarea de job; serverless usa una especificación de entorno. Fija las versiones para que una re-ejecución el mes siguiente se comporte igual. Los init scripts corren al arrancar para configuración de sistema, pero ralentizan el arranque y son difíciles de depurar.

Cuando algo falla, el driver suele ser el sospechoso de los cierres (se queda sin memoria cuando se le traen datos), y la Spark UI es donde buscar la lentitud: duración de stages, tareas desbalanceadas, tamaños de shuffle y spill.

<!-- example -->

```python
# Pulls 50 million rows into driver memory: likely out-of-memory
pdf = spark.table("silver.events").toPandas()

# Keeps the work distributed and the result small
spark.table("silver.events").groupBy("event_date").count().toPandas()
```

#### ¿Cómo se instalan librerías en un cluster?

Como librerías del cómputo (PyPI, Maven, wheels desde volúmenes o archivos del workspace), con alcance de notebook con `%pip install`, o como dependencias de una tarea de job. En serverless, las dependencias se declaran en la configuración del entorno. Fija las versiones para que sea reproducible.

#### ¿Qué son los init scripts?

Scripts de shell que se ejecutan en cada nodo al arrancar, para instalar paquetes del sistema o configurar el entorno. Deben guardarse en volúmenes o archivos del workspace, no en DBFS, y reducirse al mínimo porque ralentizan el arranque y complican la depuración.

#### ¿Qué pasa cuando el driver se queda sin memoria?

El notebook o el job falla o se reinicia. Causas comunes: `collect()` o `toPandas()` sobre muchos datos, hacer broadcast de una tabla demasiado grande, objetos Python grandes en el driver o demasiadas tareas seguidas a la vez. Mantén los datos en Spark, escribe los resultados en tablas y dimensiona bien el driver.

#### ¿Dónde se mira cuando un cluster va lento?

En la Spark UI (jobs, stages, duración de las tareas, tamaños del shuffle, spill, skew), las métricas del cluster (CPU, memoria, disco), los logs del driver y el perfil de la consulta en SQL. Compara la mediana y el máximo de la duración de las tareas de un stage para detectar skew.

<!-- challenge -->

Un job falla cada pocos días con "driver not responding". La última celda llama a `collect()` sobre el resultado para enviarlo por correo. ¿Qué cambias?

<!-- solution -->

Escribir el resultado en una tabla (o un archivo en un volumen) y enviar por correo un enlace o un resumen pequeño en vez de recolectar todas las filas. Si hace falta un resumen, agregarlo antes en Spark para que solo unas pocas filas lleguen al driver.

<!-- takeaways -->

- Fija versiones de librerías; usa init scripts lo mínimo.
- `collect()` y `toPandas()` sobre datos grandes son los asesinos habituales del driver.
- Usa la Spark UI para comparar la mediana y el máximo de duración de tareas.

### Delta Lake

<!-- unit: Log de transacciones y ACID -->

<!-- goals -->

- Explicar cómo una carpeta de archivos Parquet más un log se vuelve una tabla transaccional.
- Distinguir tablas gestionadas y externas.

<!-- concept -->

Una tabla Delta son archivos de datos Parquet más una carpeta `_delta_log/`. Cada commit es un archivo JSON numerado que lista los archivos que agregó y quitó; la tabla en la versión N es el conjunto de archivos válidos tras el commit N. Los escritores crean primero los archivos y luego compiten por la siguiente entrada del log, que es atómica, así que los lectores nunca ven datos a medio escribir.

No hay locks: la concurrencia es optimista y los conflictos se detectan al hacer commit. Quién es dueño de la ubicación decide si la tabla es gestionada o externa.

<!-- example -->

```text
sales/
├── part-0001.parquet   added in v0
├── part-0002.parquet   added in v1
├── part-0003.parquet   added in v2 (replaces 0001)
└── _delta_log/
    ├── 00000000000000000000.json   add 0001
    ├── 00000000000000000001.json   add 0002
    └── 00000000000000000002.json   remove 0001, add 0003
Version 2 = {0002, 0003}
```

#### ¿Qué es Delta Lake?

Un formato de almacenamiento de código abierto que añade un registro de transacciones a archivos Parquet. Ofrece transacciones ACID, control y evolución del esquema, viaje en el tiempo, `MERGE`, `UPDATE` y `DELETE`, y lecturas y escrituras en streaming. Es el formato de tabla por defecto en Databricks.

#### ¿Cómo funciona el registro de transacciones de Delta?

Cada tabla tiene una carpeta `_delta_log/` con archivos JSON de commit ordenados (`000…0.json`, `000…1.json`) que listan los archivos de datos añadidos y eliminados por cada transacción, además de los cambios de esquema y metadatos. Cada cierto tiempo un checkpoint en Parquet resume el estado para que los lectores no tengan que repetir todos los commits. Una versión de la tabla es el conjunto de archivos válidos después de un commit dado.

#### ¿Cómo garantiza Delta las propiedades ACID sobre almacenamiento de objetos?

Los escritores crean archivos Parquet nuevos y luego intentan hacer commit escribiendo de forma atómica la siguiente entrada numerada del registro. Si dos escritores compiten, solo uno lo logra; el otro comprueba si hay conflictos y reintenta o falla. Los lectores solo ven los archivos referenciados por entradas confirmadas, así que nunca ven escrituras parciales.

#### ¿Qué control de concurrencia usa Delta?

Control de concurrencia optimista: las transacciones no bloquean, sino que comprueban al hacer commit si otro commit concurrente tocó los mismos datos. Los appends casi nunca entran en conflicto; los `UPDATE`/`MERGE` concurrentes sobre los mismos archivos pueden lanzar `ConcurrentModificationException`. El particionamiento, el liquid clustering y la concurrencia a nivel de fila (con deletion vectors) reducen los conflictos.

#### ¿Qué diferencia hay entre una tabla administrada y una externa?

Los datos de una tabla administrada (managed) viven en un almacenamiento controlado por Unity Catalog; al borrar la tabla se borran los datos (tras un periodo de retención), y Databricks puede optimizarla automáticamente. Una tabla externa apunta a una ruta que tú administras en tu propia ubicación de almacenamiento; al borrarla solo se eliminan los metadatos.

#### ¿Qué muestra `DESCRIBE DETAIL`?

El formato, la ubicación, el número de archivos, el tamaño en bytes, las columnas de partición o de clustering y las propiedades de la tabla. Es una forma rápida de detectar el problema de los archivos pequeños.

#### ¿Qué es `CONVERT TO DELTA`?

Un comando que convierte en su lugar un directorio Parquet existente en una tabla Delta, escribiendo un registro de transacciones sobre los archivos existentes, sin copiar datos.

<!-- challenge -->

Dos jobs hacen `MERGE` sobre la misma tabla al mismo tiempo y uno falla con `ConcurrentModificationException`. Da dos formas de evitarlo.

<!-- solution -->

Serializar los escritores (un solo job, o máximo una ejecución concurrente con cola), o hacer que toquen archivos distintos: agrupar o particionar por la columna que separa sus datos e incluirla en la condición del `MERGE`. Los deletion vectors también permiten concurrencia a nivel de fila.

<!-- takeaways -->

- Una versión de Delta es el conjunto de archivos que lista el log hasta ese commit.
- El commit atómico del log da ACID sobre almacenamiento de objetos.
- La concurrencia es optimista: los conflictos aparecen al hacer commit, no como locks.

<!-- unit: Esquemas y restricciones -->

<!-- goals -->

- Explicar la aplicación del esquema y cómo permitir su evolución de forma deliberada.
- Usar restricciones, columnas generadas e identity y propiedades de tabla.

<!-- concept -->

Delta rechaza escrituras que no coinciden con el esquema de la tabla; eso es enforcement, y protege a los lectores posteriores. Cuando el esquema debe cambiar, lo permites explícitamente: `mergeSchema` en una escritura, `ALTER TABLE` o la evolución de esquema en `MERGE`.

Más allá de los tipos, las tablas pueden llevar reglas y metadatos: restricciones `NOT NULL` y `CHECK` (aplicadas), columnas generadas e identity, y propiedades que activan funciones como Change Data Feed. UniForm agrega metadatos Iceberg para que otros motores lean los mismos archivos.

<!-- example -->

```sql
CREATE TABLE silver.orders (
  order_id   BIGINT GENERATED ALWAYS AS IDENTITY,
  ordered_at TIMESTAMP NOT NULL,
  order_date DATE GENERATED ALWAYS AS (CAST(ordered_at AS DATE)),
  amount     DECIMAL(18,2),
  CONSTRAINT positive_amount CHECK (amount >= 0)
) TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true');
```

#### ¿Qué es el control del esquema (schema enforcement)?

Delta rechaza las escrituras cuyas columnas o tipos no coinciden con el esquema de la tabla, en lugar de corromperla en silencio. Protege a los consumidores de cargas defectuosas.

#### ¿Cómo funciona la evolución del esquema en Delta?

Hay que permitirla de forma explícita: `.option("mergeSchema", "true")` en una escritura añade columnas nuevas, y `ALTER TABLE` cambia el esquema. Para `MERGE`, `WITH SCHEMA EVOLUTION` (o la configuración de merge automático) permite añadir columnas nuevas del origen. El type widening permite algunos cambios de tipo, como de `int` a `bigint`, sin reescribir los datos.

#### ¿Qué restricciones admite Delta?

Restricciones `NOT NULL` y `CHECK`, que se aplican: una escritura que las viola falla. Las claves primarias y foráneas se pueden declarar en Unity Catalog, pero son informativas (no se aplican) y las usan las herramientas y el optimizador.

#### ¿Qué son las columnas generadas y las columnas de identidad?

Una columna generada se calcula a partir de otras columnas (`GENERATED ALWAYS AS (CAST(ts AS DATE))`). Una columna de identidad (`GENERATED ALWAYS AS IDENTITY`) asigna números únicos y crecientes (no necesariamente consecutivos), útiles como claves sustitutas.

#### ¿Para qué sirven las propiedades de tabla en Delta?

Son ajustes guardados con la tabla, como `delta.enableChangeDataFeed`, `delta.logRetentionDuration`, `delta.deletedFileRetentionDuration`, `delta.enableDeletionVectors` o `delta.appendOnly`, además de metadatos clave-valor propios. Se definen con `TBLPROPERTIES` y se ven con `SHOW TBLPROPERTIES`.

#### ¿Qué es UniForm?

Universal Format: una opción de las tablas Delta que también escribe metadatos Iceberg, para que los motores que leen Iceberg puedan leer los mismos archivos sin copiar los datos.

<!-- challenge -->

Una fuente agrega una columna `discount` y el append nocturno a `silver.orders` ahora falla. ¿Deberías activar `mergeSchema` de forma permanente?

<!-- solution -->

No a ciegas. Agrega la columna a propósito (`ALTER TABLE ... ADD COLUMN discount ...` o una escritura puntual con `mergeSchema`) tras revisar su significado y tipo. La evolución automática permanente deja que cualquier error de origen cambie la forma de una tabla silver de confianza.

<!-- takeaways -->

- El enforcement es lo predeterminado; la evolución debe ser una decisión deliberada.
- `CHECK` y `NOT NULL` se aplican; las claves primarias y foráneas son informativas.
- Las propiedades de tabla activan y desactivan funciones como CDF y la retención.

<!-- unit: Time travel, restore y retención -->

<!-- goals -->

- Consultar y restaurar versiones anteriores de una tabla.
- Explicar cómo `VACUUM` y la retención limitan el time travel.

<!-- concept -->

Como los archivos viejos permanecen en el almacenamiento hasta que se borran, cada versión de Delta puede volver a leerse: eso es time travel, y `RESTORE` vuelve actual una versión antigua con un commit nuevo. Los clones copian una tabla en un punto del tiempo, completa (deep) o solo metadatos (shallow).

El time travel no es almacenamiento gratis para siempre. `VACUUM` borra archivos no referenciados más antiguos que la retención (7 días por defecto), y el log guarda 30 días de historia. Una vez borrados los archivos, las versiones que los necesitaban ya no se pueden leer.

<!-- example -->

```sql
DESCRIBE HISTORY gold.revenue;                 -- find the bad commit, say v57
SELECT * FROM gold.revenue VERSION AS OF 56;   -- check the good version
RESTORE TABLE gold.revenue TO VERSION AS OF 56;
```

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

#### ¿Qué diferencia hay entre la retención del log y la de los archivos borrados?

`delta.logRetentionDuration` (30 días por defecto) controla cuánto tiempo se conserva el historial de commits; `delta.deletedFileRetentionDuration` (7 días por defecto) controla cuánto tiempo conserva `VACUUM` los archivos de datos sin referencia. El viaje en el tiempo necesita las dos cosas: las entradas del log y los archivos de datos.

#### ¿Qué diferencia hay entre un deep clone y un shallow clone?

Un deep clone copia los archivos de datos y los metadatos en una tabla independiente. Un shallow clone copia solo los metadatos y apunta a los archivos del origen, así que es instantáneo y barato, útil para probar cambios sobre datos del tamaño de producción. Ambos tienen su propio historial desde el momento del clon.

#### Alguien borró por error columnas de una tabla gold hace una hora. ¿Cómo la recuperas?

Busco en `DESCRIBE HISTORY` la versión anterior al cambio y ejecuto `RESTORE TABLE … TO VERSION AS OF` esa versión, o hago un `SELECT` sobre ella para reconstruirla. Después reviso los permisos para que solo el service principal del pipeline pueda modificar las tablas gold.

<!-- challenge -->

Auditoría te pide reproducir un reporte exactamente como estaba hace 60 días. Con la configuración por defecto, ¿puedes? ¿Qué cambiarías a futuro?

<!-- solution -->

Probablemente no: los archivos borrados se eliminan tras 7 días y el log guarda 30. A futuro, sube `delta.logRetentionDuration` y `delta.deletedFileRetentionDuration` en esa tabla, o guarda una instantánea de los datos del reporte (un deep clone o una tabla fechada) en cada publicación.

<!-- takeaways -->

- El time travel lee versiones viejas; `RESTORE` vuelve actual una de ellas.
- `VACUUM` más la retención definen hasta dónde puedes volver.
- Los shallow clones son copias instantáneas para probar con datos reales.

<!-- unit: Cambiar datos: MERGE, UPDATE y DELETE -->

<!-- goals -->

- Escribir un `MERGE` correcto y corregir sus errores comunes.
- Explicar copy-on-write, deletion vectors y Change Data Feed.

<!-- concept -->

Los archivos Parquet son inmutables, así que cambiar una fila implica escribir archivos nuevos. Sin deletion vectors, `UPDATE`, `DELETE` y `MERGE` reescriben cada archivo con una fila tocada (copy-on-write). Los deletion vectors, en cambio, marcan filas como borradas en un archivo auxiliar pequeño y reescriben después.

`MERGE` es la herramienta principal para upserts, CDC y deduplicación. Sus dos problemas típicos son fuentes ambiguas (varias filas por clave) y escaneos lentos de todo el destino. Para reemplazar un tramo completo, `replaceWhere` es más simple. Change Data Feed permite a los procesos siguientes leer solo las filas que cambiaron.

<!-- example -->

Deduplica la fuente y luego haz el merge:
```sql
MERGE INTO silver.customers t
USING (
  SELECT * FROM updates
  QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1
) s
ON t.customer_id = s.customer_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

#### ¿Cómo hace Delta `UPDATE` y `DELETE` sin deletion vectors?

Busca los archivos que contienen filas afectadas, los reescribe sin las filas borradas (o con los valores actualizados) y hace commit de una transacción que elimina los archivos antiguos y añade los nuevos. Es copy-on-write: lecturas baratas y escrituras caras sobre archivos grandes.

#### ¿Qué son los deletion vectors?

Una optimización del almacenamiento en la que `DELETE`, `UPDATE` y `MERGE` marcan las filas como borradas en un pequeño archivo auxiliar en lugar de reescribir archivos Parquet completos. Las escrituras se vuelven mucho más rápidas; los archivos se reescriben físicamente más tarde con `OPTIMIZE` o `REORG TABLE … APPLY (PURGE)`.

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

#### ¿Qué diferencia hay entre el modo `overwrite` y `replaceWhere`?

`mode("overwrite")` reemplaza toda la tabla (como una nueva versión, así que el viaje en el tiempo sigue funcionando). `replaceWhere` reemplaza solo las filas que cumplen un predicado. La sobrescritura dinámica de particiones (`partitionOverwriteMode=dynamic`) reemplaza solo las particiones presentes en los datos nuevos.

#### ¿Qué es el Change Data Feed?

Una opción de tabla (`delta.enableChangeDataFeed = true`) que registra los cambios a nivel de fila (insert, update_preimage, update_postimage, delete) con la versión y la fecha del commit. Los jobs posteriores leen solo lo que cambió:

```sql
SELECT * FROM table_changes('silver.customers', 120);
```

#### ¿Cómo atiendes una solicitud de borrado del RGPD/GDPR o de habeas data en un lakehouse Delta?

Borro las filas de la persona con `DELETE` o `MERGE` en todas las capas (bronze incluida) y luego ejecuto `VACUUM` para eliminar físicamente los archivos antiguos que las contenían, pasado el periodo de retención. Seudonimizar los identificadores al inicio del pipeline limita el número de tablas con datos personales.

<!-- challenge -->

Un `MERGE` diario de 50.000 filas cambiadas sobre una tabla de 3.000 millones de filas tarda 40 minutos. Los cambios siempre son de los últimos 3 días. ¿Qué pruebas primero?

<!-- solution -->

Agregar el rango de fechas a la condición `ON` (por ejemplo `t.event_date >= current_date() - 3`) para que Delta descarte la mayoría de archivos del destino, y agrupar la tabla por fecha y clave. Activar deletion vectors para no reescribir completos los archivos afectados.

<!-- takeaways -->

- Sin deletion vectors, cualquier cambio de fila reescribe archivos completos.
- Deduplica la fuente del `MERGE`; poda el destino con condiciones extra.
- CDF entrega a los procesos siguientes solo las filas cambiadas.

<!-- unit: Organización de archivos y data skipping -->

<!-- goals -->

- Diagnosticar y resolver el problema de archivos pequeños.
- Elegir liquid clustering en vez de particionado y Z-ordering para tablas nuevas.

<!-- concept -->

La velocidad de lectura depende de cuántos archivos abre una consulta y cuántos puede saltarse. `OPTIMIZE`, optimized writes y auto compaction combinan los archivos pequeños. Delta guarda estadísticas mín/máx por archivo, de modo que un filtro salta archivos cuyo rango no coincide; eso funciona bien solo si los valores parecidos están en los mismos archivos.

El clustering los pone ahí. El particionado divide por directorio y conviene solo en tablas enormes con columnas de baja cardinalidad. Z-ordering hay que repetirlo. Liquid clustering (`CLUSTER BY`) agrupa de forma incremental, permite cambiar claves y hoy es la opción por defecto.

<!-- example -->

```sql
DESCRIBE DETAIL silver.events;            -- numFiles: 480000, sizeInBytes: 200 GB → ~400 KB per file
ALTER TABLE silver.events CLUSTER BY (event_date, user_id);
OPTIMIZE silver.events;                   -- compacts and clusters
```

#### ¿Qué es el problema de los archivos pequeños?

Muchos archivos diminutos hacen lentas las lecturas (cada archivo tiene un costo de apertura y de metadatos, y las estadísticas sirven menos) y ralentizan el registro de transacciones. Lo causan el streaming y los appends pequeños y frecuentes. Soluciones: `OPTIMIZE`, la auto compactación y las escrituras optimizadas, y lotes menos numerosos y más grandes.

#### ¿Qué hace `OPTIMIZE`?

Compacta archivos pequeños en archivos más grandes (alrededor de 1 GB por defecto), lo que acelera las lecturas. Con Z-ordering o liquid clustering, además reescribe los datos para que los valores relacionados queden en los mismos archivos.

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

#### Tu tabla Delta tiene 500.000 archivos pequeños. ¿Qué haces?

Ejecuto `OPTIMIZE` (con liquid clustering sobre las columnas de filtro principales), activo las escrituras optimizadas y la auto compactación o la optimización predictiva, y luego corrijo la causa: agrupar los microappends, evitar el particionamiento excesivo y usar triggers `availableNow` en lugar de streams diminutos muy frecuentes. Después ejecuto `VACUUM` para borrar los archivos antiguos.

<!-- challenge -->

Una tabla particionada por `customer_id` (200.000 clientes) es lenta en todas las consultas. ¿Qué pasó y qué haces?

<!-- solution -->

El particionado de alta cardinalidad creó cientos de miles de directorios y archivos diminutos. Recrea la tabla sin particiones, con `CLUSTER BY (customer_id)` (más la fecha si las consultas filtran por ella), ejecuta `OPTIMIZE` y luego `VACUUM` sobre los archivos viejos.

<!-- takeaways -->

- Busca pocos archivos grandes; `DESCRIBE DETAIL` muestra el conteo.
- El data skipping necesita datos agrupados para ser efectivo.
- Usa liquid clustering en tablas nuevas; particiona solo tablas enormes en columnas de baja cardinalidad.

<!-- stage: Construir pipelines -->

### Ingesta

<!-- unit: Elegir una vía de ingesta -->

<!-- goals -->

- Elegir la herramienta correcta para archivos, bases de datos, fuentes SaaS y streams.
- Cargar una tabla relacional en paralelo y de forma incremental.

<!-- concept -->

La forma en que llegan los datos decide la herramienta, y Databricks recomienda empezar por la opción más administrada y bajar de nivel solo cuando no sirve. Para apps SaaS y bases de datos, primero los conectores administrados de Lakeflow Connect; si no, una lectura JDBC resuelve. Los archivos que caen en el almacenamiento pasan por Auto Loader (o `COPY INTO` para lotes modestos, o `read_files` en SQL). Los streams de eventos llegan de Kafka o similares con Structured Streaming, y las aplicaciones pueden enviar registros directamente con Zerobus Ingest.

Sea cual sea la fuente, el patrón es el mismo: dejar los datos crudos en bronze, de forma incremental, con metadatos suficientes para saber de dónde vino cada fila.

<!-- example -->

| Fuente | Primera opción |
|---|---|
| Archivos en S3 / ADLS / volúmenes | Auto Loader (`cloudFiles`) |
| Unos miles de archivos por lote, solo SQL | `COPY INTO` |
| Salesforce, Workday, SQL Server, PostgreSQL... | Conector administrado de Lakeflow Connect |
| PostgreSQL sin conector | Spark JDBC, particionado, por watermark |
| Kafka, Kinesis, Event Hubs | Structured Streaming (o un conector de streaming administrado) |
| Eventos de tu propia aplicación | Zerobus Ingest (escritura directa) |

#### ¿Qué opciones hay para cargar datos en Databricks?

Los conectores administrados de Lakeflow Connect para apps SaaS, bases de datos, archivos y buses de mensajes, Auto Loader para los archivos que llegan al almacenamiento en la nube, `COPY INTO` para cargas batch idempotentes de archivos, Structured Streaming desde Kafka, Kinesis o Event Hubs, la API Zerobus Ingest para aplicaciones que escriben registros directamente, conectores comunitarios y propios, herramientas de socios (Fivetran y otras) y la subida de archivos con la interfaz "Add data". Lakehouse Federation y el intercambio de datos son alternativas que leen los datos sin ingerirlos.

#### ¿Qué es Lakeflow Connect?

La capa de ingesta de Databricks. Sus conectores administrados son serverless y totalmente gestionados: bases de datos con CDC (SQL Server, PostgreSQL, MySQL, Oracle), apps SaaS (Salesforce, Workday, HubSpot, Jira y otras), archivos (almacenamiento en la nube, SharePoint, Google Drive) y buses de mensajes (Kafka, Kinesis, Pub/Sub). Se encargan de la extracción incremental y dejan los datos en streaming tables de Unity Catalog, sin código de extracción. Para fuentes sin conector administrado, las API de SQL y Spark (Auto Loader, `read_files`, Structured Streaming) dan más control.

#### ¿Qué es Zerobus Ingest?

Una API de Lakeflow Connect que permite a las aplicaciones escribir registros directamente en una tabla de Unity Catalog, sin un bus de mensajes de por medio. Sirve para eventos y telemetría que de otro modo enviarías a Kafka solo para volver a cargarlos en Databricks.

#### ¿Cuándo conviene ingerir los datos y cuándo federarlos o compartirlos?

Ingiere cuando los volúmenes son altos, las consultas necesitan baja latencia o la fuente tiene límites de API o de carga, aceptando que la copia hay que mantenerla al día. Federa (consulta en su lugar) para exploración, búsquedas pequeñas o un periodo de migración. Comparte cuando otra organización ya publica los datos. Las copias ingeridas pueden quedar desactualizadas; las consultas federadas cargan el sistema de origen.

#### ¿Cómo se cargan datos de una base de datos relacional sin Lakeflow Connect?

Con el lector JDBC de Spark, particionando la lectura con `partitionColumn`, `lowerBound`, `upperBound` y `numPartitions` para que se ejecute en paralelo, y cargando de forma incremental según una columna marca de agua (por ejemplo `updated_at`). Guarda las credenciales en secretos.

#### ¿Cómo se ingiere desde Kafka?

Con la fuente Kafka de Structured Streaming, que lee `key`, `value`, `topic`, `partition`, `offset` y `timestamp`. Se interpreta `value` (JSON, Avro con un schema registry, Protobuf), se escriben los registros en bruto en bronze y se mantiene un checkpoint por consulta.

#### ¿Qué es `COPY INTO`?

Un comando SQL que carga archivos de una ruta en una tabla Delta y es idempotente: los archivos ya cargados se omiten. Sirve para cargas batch programadas de miles de archivos; para millones de archivos o ingesta continua es preferible Auto Loader.

```sql
COPY INTO bronze.customers
FROM '/Volumes/raw/landing/customers/'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');
```

#### ¿Qué es `read_files`?

Una función SQL de tabla que lee archivos (CSV, JSON, Parquet, Avro, XML, texto) de una ruta o un volumen con inferencia de esquema. Con `STREAM read_files(...)` en una streaming table, usa Auto Loader por debajo.

<!-- challenge -->

Debes cargar cada noche una tabla de PostgreSQL de 400 millones de filas, pero solo cambia alrededor del 1 %. Bosqueja la lectura.

<!-- solution -->

Leer solo las filas con `updated_at` mayor que el último watermark cargado (guardado en una tabla de control o tomado del máximo del destino), con una lectura JDBC particionada por una clave numérica (`partitionColumn`, límites, `numPartitions`). Hacer `MERGE` del resultado por clave primaria. Los borrados requieren otra vía, como CDC o una comparación periódica de claves.

<!-- takeaways -->

- Elige la herramienta por cómo llegan los datos: archivos, bases, SaaS o streams.
- Carga de forma incremental; las recargas completas no escalan.
- Bronze guarda los datos crudos y su procedencia.

<!-- unit: Auto Loader y el control del streaming -->

<!-- goals -->

- Explicar cómo Auto Loader carga cada archivo exactamente una vez.
- Ejecutar ingesta en streaming con calendario batch usando `availableNow`.

<!-- concept -->

Auto Loader es una fuente de streaming que descubre archivos nuevos, listando el directorio o mediante notificaciones del almacenamiento. Registra los archivos procesados en el checkpoint del stream, así que los reinicios nunca cargan un archivo dos veces y los archivos tardíos igual se toman.

Streaming no significa siempre encendido. Con `trigger(availableNow=True)` la consulta procesa todo lo nuevo y se detiene, lo que da el control del streaming con el costo de un job programado. La columna oculta `_metadata` registra de qué archivo vino cada fila.

<!-- example -->

```python
(spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("cloudFiles.schemaLocation", "/Volumes/raw/_schemas/orders")
    .load("/Volumes/raw/landing/orders/")
    .select("*", "_metadata.file_path", "_metadata.file_modification_time")
  .writeStream
    .option("checkpointLocation", "/Volumes/raw/_checkpoints/orders")
    .trigger(availableNow=True)          # run as a daily batch
    .toTable("bronze.orders"))
```

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

#### ¿Qué es un checkpoint de streaming?

Una ubicación de almacenamiento donde una consulta de streaming registra su avance (offsets o archivos procesados) y su estado. Garantiza un procesamiento exactly-once entre reinicios. Cada consulta necesita su propio checkpoint, y borrarlo hace que la consulta empiece de cero.

#### ¿Qué hace `trigger(availableNow=True)`?

Hace que una consulta de streaming procese todo lo disponible al arrancar (en varios lotes, respetando los límites de velocidad) y luego se detenga. Da el seguimiento incremental del streaming con el perfil de costos de un job batch programado. En cómputo serverless, `availableNow` y `once` son los únicos triggers soportados.

#### ¿Qué es la columna `_metadata`?

Una columna oculta disponible al leer archivos, con `file_path`, `file_name`, `file_size` y `file_modification_time`. Reemplaza a `input_file_name()` (no admitida en Unity Catalog) para registrar el archivo de origen de cada fila.

#### ¿Cómo se manejan los archivos que llegan tarde?

Auto Loader toma cualquier archivo nuevo cuando llega, sin importar su fecha, así que la carga en sí es segura. Más adelante, usa `MERGE` sobre las claves de negocio o reprocesa las fechas afectadas con `replaceWhere`, para que los datos tardíos corrijan los resultados anteriores.

<!-- challenge -->

Alguien borra la carpeta del checkpoint de un stream de ingesta a bronze "para limpiar". ¿Qué pasa en la siguiente ejecución y cómo te recuperas?

<!-- solution -->

El stream empieza de cero y recarga todos los archivos de la ruta de aterrizaje, duplicando bronze. Recupérate restaurando la tabla bronze a la versión previa a esa ejecución (o deduplicando por ruta de archivo) y deja que el nuevo checkpoint continúe. Protege los checkpoints con permisos.

<!-- takeaways -->

- El checkpoint es lo que hace la ingesta exactly-once; nunca lo compartas ni lo borres.
- `availableNow` da el control del streaming con un calendario batch.
- Registra `_metadata.file_path` para la trazabilidad.

<!-- unit: Inferencia y deriva de esquema -->

<!-- goals -->

- Controlar la inferencia de esquema en cargas de producción.
- Manejar columnas nuevas o mal formadas sin perder datos.

<!-- concept -->

Las fuentes cambian sin avisar. Inferir el esquema en cada ejecución es lento e inestable, así que las cargas de producción declaran un esquema o dejan que Auto Loader lo gestione: guarda el esquema inferido, se detiene cuando aparece una columna nueva y continúa con el esquema evolucionado tras reiniciar.

Los schema hints fijan los tipos que importan, y los valores que no encajan van a `_rescued_data` en vez de perderse. Vigilar esa columna es una alerta temprana de que la fuente cambió.

<!-- example -->

```python
.option("cloudFiles.schemaHints", "amount DECIMAL(18,2), event_ts TIMESTAMP")
.option("cloudFiles.schemaEvolutionMode", "addNewColumns")
# Later: SELECT count(*) FROM bronze.orders WHERE _rescued_data IS NOT NULL
```

#### ¿Por qué evitar `inferSchema` en producción?

La inferencia requiere una pasada extra sobre los datos, puede inferir tipos distintos en archivos distintos y cambia en silencio cuando cambia el origen. Declara los esquemas (contratos de datos) en las cargas de producción, o deja que Auto Loader gestione la inferencia con schema hints.

#### ¿Cómo maneja Auto Loader los cambios de esquema?

Guarda el esquema inferido en la ubicación del esquema. Con el modo por defecto `addNewColumns`, una columna nueva detiene el stream, actualiza el esquema y el stream continúa tras reiniciarse. Los datos que no encajan en el esquema (tipo incorrecto, columna inesperada) van a la columna `_rescued_data` en lugar de perderse.

#### ¿Qué es la columna de datos rescatados?

Una columna de texto JSON (`_rescued_data`) donde Auto Loader pone los valores que no pudo convertir al esquema. Vigilarla revela los cambios de formato en el origen.

#### ¿Qué son los schema hints de Auto Loader?

Tipos explícitos para algunas columnas (`cloudFiles.schemaHints = "amount DECIMAL(18,2), event_ts TIMESTAMP"`) que se imponen a la inferencia, mientras el resto del esquema se sigue infiriendo.

#### Una consulta de streaming falla tras un cambio de esquema en el origen. ¿Cómo lo manejas?

Con Auto Loader en modo `addNewColumns`, reinicia el stream para que tome el esquema nuevo. Para los cambios incompatibles, actualiza el esquema destino (o usa la columna de datos rescatados) y, si cambió la lógica, empieza un checkpoint nuevo con un plan de backfill claro. Añade alertas sobre los datos rescatados.

<!-- challenge -->

Tras una actualización del proveedor, `amount` llega como `"12,50"` (decimal con coma) en algunos archivos. ¿Qué pasa con un tipo `DECIMAL` indicado por hint y cómo lo notas?

<!-- solution -->

Esos valores no se pueden convertir, así que `amount` queda nulo y el valor crudo va a `_rescued_data`. Una alerta sobre la proporción de filas con datos rescatados lo detecta; luego corriges la conversión en silver (reemplazar la coma, castear) y reprocesas los archivos afectados.

<!-- takeaways -->

- Declara o indica los tipos importantes; no dependas de la inferencia.
- `addNewColumns` se detiene, evoluciona y continúa tras reiniciar.
- Vigila `_rescued_data` para detectar cambios en el origen.

<!-- unit: Lo esencial de Structured Streaming -->

<!-- goals -->

- Elegir un trigger y un modo de procesamiento según la latencia requerida.
- Explicar el estado, los watermarks y los modos de salida en las consultas con estado.

<!-- concept -->

En Databricks, un mismo motor sirve para batch y streaming. Structured Streaming trata una fuente (Auto Loader, una tabla Delta, Kafka) como una tabla sin límite y procesa los datos nuevos en micro-batches, con latencias de segundos a minutos. El modo en tiempo real maneja los registros a medida que llegan, con latencia por debajo del segundo, para usos operativos como la detección de fraude.

Las consultas sin estado, como filtros y appends, son simples. Las agregaciones, los joins entre streams y la deduplicación guardan estado entre lotes, y un watermark fija cuánto esperar los datos tardíos antes de descartar ese estado. Sin él, el estado crece hasta que la consulta falla.

<!-- example -->

```python
from pyspark.sql import functions as F

(spark.readStream.table("bronze.clicks")
    .withWatermark("event_ts", "30 minutes")          # acepta datos con hasta 30 min de retraso
    .groupBy(F.window("event_ts", "5 minutes"), "page")
    .count()
  .writeStream
    .outputMode("append")                              # emite una ventana cuando ya es definitiva
    .option("checkpointLocation", "/Volumes/ops/_checkpoints/clicks_5m")
    .trigger(processingTime="1 minute")
    .toTable("silver.clicks_5m"))
```

#### ¿Cómo trata Databricks el batch y el streaming?

Como dos semánticas del mismo motor. Una consulta batch procesa todos los datos de la fuente en cada ejecución y no recuerda qué leyó; una consulta de streaming registra su avance en un checkpoint y procesa solo lo que llegó desde la última ejecución. El streaming no se limita a los buses de mensajes: el almacenamiento en la nube (con Auto Loader) y las tablas Delta también son fuentes de streaming, lo que hace del streaming la forma habitual de procesar datos de forma incremental.

#### ¿Qué triggers puede usar una consulta de streaming?

El de por defecto (un nuevo micro-batch apenas termina el anterior), `processingTime` (un micro-batch a intervalo fijo), `availableNow` (procesa todo lo disponible y se detiene) y `realTime` para el modo en tiempo real. El trigger `continuous` antiguo de Spark no está soportado en Databricks. En serverless solo se permiten `availableNow` y `once`.

#### ¿Qué es el modo en tiempo real (real-time mode)?

Un trigger de Structured Streaming (`.trigger(realTime="5 minutes")`, donde el intervalo fija cuánto dura cada lote de larga duración) que procesa los registros a medida que llegan, con latencia por debajo del segundo, en vez de en micro-batches. Apunta a cargas operativas como la detección de fraude y la personalización. Corre en cómputo de jobs clásico sin autoscaling, Photon ni instancias spot, y Databricks lo recomienda solo cuando la latencia de micro-batch no alcanza.

#### ¿Qué son los modos de salida (output modes)?

Deciden qué escribe una consulta de streaming en cada lote: `append` escribe solo filas nuevas (y, en agregaciones con watermark, solo las ventanas definitivas), `update` escribe las filas que cambiaron desde el último lote y `complete` reescribe todo el resultado. Los sinks de tablas Delta suelen escribirse en modo append; `foreachBatch` con `MERGE` maneja los upserts.

#### ¿Qué es un watermark?

Un umbral sobre el tiempo del evento (`withWatermark("event_ts", "30 minutes")`) que le dice a una consulta con estado cuánto esperar los datos tardíos. Los registros más viejos que el watermark se ignoran y el estado de las ventanas que lo superan se descarta, así que la memoria se mantiene acotada. Sin watermark, las agregaciones y los joins entre streams guardan estado para siempre.

#### ¿Qué es una consulta de streaming con estado y dónde vive su estado?

Una consulta que recuerda datos entre micro-batches: agregaciones, joins entre streams, `dropDuplicates` y operadores con estado arbitrarios. El estado se guarda en un state store en los executors y se persiste en el checkpoint. En Databricks, el state store RocksDB guarda el estado grande en disco local en vez de en la memoria de la JVM, y el checkpointing asíncrono del estado reduce la latencia que añade.

#### ¿Qué es un join stream-static y cuál es su trampa?

Un join entre un DataFrame de streaming y una tabla estática, por ejemplo para enriquecer eventos con una dimensión. Cada micro-batch lee la última versión de la tabla estática, pero las filas ya procesadas no se recalculan cuando la dimensión cambia después. Si los resultados deben reflejar siempre la dimensión actual, usa una vista materializada.

#### ¿Para qué sirve `foreachBatch`?

Ejecuta tu propia función sobre cada micro-batch como un DataFrame normal, para usar operaciones que solo existen en batch: `MERGE` en una tabla Delta, escribir en varios destinos o llamar a un destino sin writer de streaming. Haz la función idempotente, porque un lote se puede reintentar.

#### ¿Qué vigilar al operar streams en producción?

Mantener acotada la tasa de entrada (`maxFilesPerTrigger`, `maxBytesPerTrigger`, `maxOffsetsPerTrigger`) para que el tamaño de los lotes sea predecible, dar a cada consulta su propio checkpoint, vigilar la duración de los lotes frente al intervalo del trigger y las tasas de entrada frente a las de procesamiento (en la interfaz de streaming, con `StreamingQueryListener` o en el event log del pipeline) y ejecutar los streams como jobs con reintentos en vez de en notebooks.

<!-- challenge -->

Un conteo de clics por página cada 5 minutos corre en modo update sin watermark. Después de dos semanas el job se vuelve lento y luego falla por falta de memoria. ¿Por qué, y qué cambias?

<!-- solution -->

Sin watermark, Spark guarda el estado de todas las ventanas desde el inicio, así que el estado crece sin límite. Agrega `withWatermark("event_ts", "30 minutes")` (o el retraso que acepte el negocio) para que las ventanas viejas se cierren y se descarten, usa el state store RocksDB para estados grandes y pasa a modo append si los consumidores solo necesitan ventanas definitivas.

<!-- takeaways -->

- Un solo motor: el streaming es procesamiento incremental, no solo baja latencia.
- El micro-batch cubre de segundos a minutos; el modo en tiempo real es para menos de un segundo.
- Las consultas con estado necesitan un watermark para acotar el estado.

### Arquitectura medallion y modelado

<!-- unit: Capas y sus contratos -->

<!-- goals -->

- Describir qué va en bronze, silver y gold.
- Justificar una capa cruda y adaptar las capas al proyecto.

<!-- concept -->

La arquitectura medallion organiza un lakehouse en capas de calidad creciente. Bronze guarda lo que envió la fuente, para reprocesar y auditar. Silver es la versión limpia, deduplicada y validada de cada entidad, la que todos confían. Gold da forma a los datos para su consumo: esquemas en estrella, agregados y features.

El valor está en los contratos entre capas, no en el número tres. Los proyectos pequeños fusionan capas; otros agregan una zona de aterrizaje o una capa de servicio.

<!-- example -->

| Capa | Tabla de ejemplo | Contrato |
|---|---|---|
| Bronze | `bronze.orders` | Filas crudas + `file_path`, hora de carga; solo append |
| Silver | `silver.orders` | Tipada, una fila por `order_id`, filas malas en cuarentena |
| Gold | `gold.fct_daily_sales` | Grano: una fila por día y tienda; definiciones de negocio aplicadas |

#### ¿Qué es la arquitectura medallion?

Una forma de organizar los datos del lakehouse por capas: bronze guarda los datos en bruto tal como llegan (solo añadir, con metadatos de carga), silver guarda los datos limpios, homogeneizados, deduplicados y validados, y gold guarda agregados de negocio y modelos dimensionales listos para BI y ML. La calidad y la estructura aumentan capa por capa.

#### ¿Por qué conservar una capa bronze en bruto?

Para poder reprocesar el historial cuando cambia la lógica o se encuentran errores, auditar lo que el origen envió realmente y desacoplar la ingesta de la transformación. Bronze debe ser barato de conservar y fiel al origen.

#### ¿Bronze debe ser una tabla Delta o archivos en bruto?

Por lo general, los archivos en bruto se quedan en una zona de landing (o un volumen) y bronze es una tabla Delta cargada desde ellos con cambios mínimos y metadatos de carga. Delta en bronze aporta transacciones, seguimiento del esquema y reprocesamiento rápido; conservar los archivos originales da una copia exacta para auditorías.

#### ¿Qué va en silver?

Columnas tipadas y renombradas, deduplicación, valores estandarizados (fechas, códigos, direcciones), uniones con datos de referencia, controles de calidad con cuarentena de las filas defectuosas e historial (SCD tipo 2) cuando hace falta. Silver es la versión única y confiable de cada entidad.

#### ¿Qué va en gold?

Datos con la forma que necesita el consumo: esquemas en estrella (hechos y dimensiones), agregados, tablas de features y productos de datos, con las definiciones de negocio aplicadas. Las tablas gold suelen ser más pequeñas y están optimizadas para la lectura.

#### ¿La arquitectura medallion tiene siempre tres capas?

No. Es una convención, no una regla. Los proyectos pequeños pueden fusionar silver y gold; otros añaden una zona de aterrizaje (landing) antes de bronze o una capa de servicio (platinum) después de gold. Lo importante es que cada capa tenga un contrato claro.

#### ¿Cada capa medallion debe usar batch o streaming?

La guía de Databricks: bronze suele ser streaming (streaming tables, Auto Loader), porque la ingesta es un append sin estado. Silver y gold usan por defecto semántica batch con refresco incremental, es decir, vistas materializadas, porque unen, agregan y corrigen datos, y una vista materializada sigue correcta cuando cambian las fuentes. Usa streaming en silver solo cuando la latencia importa más que manejar datos tardíos o modificados, y prevé la complejidad del estado.

<!-- challenge -->

Un colega propone limpiar los datos al cargarlos y saltarse bronze "para ahorrar almacenamiento". ¿Qué pierdes?

<!-- solution -->

La capacidad de reprocesar la historia cuando la lógica de limpieza cambia o tiene un error, y la evidencia de lo que la fuente envió realmente. El almacenamiento de bronze es barato comparado con volver a extraer datos que la fuente quizá ya no tenga.

<!-- takeaways -->

- Bronze es fiel, silver es confiable, gold tiene forma para su uso.
- Cada capa es un contrato sobre grano, calidad y responsables.
- Adapta el número de capas; conserva los contratos.

<!-- unit: Patrones de modelado -->

<!-- goals -->

- Implementar SCD tipo 2 y cuarentena de registros sobre Delta.
- Organizar catálogos y tablas gold para BI y ML.

<!-- concept -->

Silver es donde se manejan la historia y la calidad. SCD tipo 2 guarda cada versión de una entidad con fechas de vigencia, y un solo `MERGE` puede mantenerla. La cuarentena envía las filas que fallan, con sus motivos, a una tabla aparte para que el pipeline siga y alguien corrija la fuente.

Gold atiende entonces a dos públicos desde los mismos datos silver: esquemas en estrella para BI y tablas de features para ML. Los catálogos suelen separar entornos y los esquemas separan capas, así los permisos siguen al entorno.

<!-- example -->

Filas SCD tipo 2 de un cliente:
| customer_id | city | valid_from | valid_to | is_current |
|---|---|---|---|---|
| 42 | Bogotá | 2024-01-10 | 2026-03-02 | false |
| 42 | Medellín | 2026-03-02 | null | true |

#### ¿Cómo se implementa una SCD tipo 2 en Delta?

Con `MERGE`: se cierra la fila vigente (se llenan `valid_to` e `is_current = false`) cuando cambian los atributos seguidos, y se inserta la nueva versión. Un truco común es hacer merge de una unión de las actualizaciones con una clave de merge nula para las filas modificadas, de modo que un solo `MERGE` cierre e inserte. Los Lakeflow pipelines lo hacen con `AUTO CDC … STORED AS SCD TYPE 2`.

#### ¿Cómo se ponen en cuarentena los registros defectuosos?

Validando las filas contra reglas en silver, escribiendo las filas que fallan con sus motivos en una tabla de cuarentena y siguiendo con las válidas. Vigila la tasa de cuarentena y genera alertas ante picos. En los Lakeflow pipelines se logra lo mismo con expectativas `DROP ROW` y una consulta inversa aparte.

#### ¿Conviene usar un catálogo por entorno o por capa?

Un patrón común es un catálogo por entorno (`dev`, `staging`, `prod`) con esquemas por capa (`bronze`, `silver`, `gold`), porque los entornos necesitan permisos y almacenamiento distintos. Algunos equipos prefieren catálogos por dominio o unidad de negocio. Importa más la coherencia que la elección.

#### ¿Qué es un producto de datos en el contexto de Databricks?

Un conjunto de tablas (normalmente gold) seleccionado, documentado y gobernado, del que es responsable un equipo, con controles de calidad, una interfaz clara y acceso concedido mediante Unity Catalog, posiblemente compartido con Delta Sharing.

#### ¿Cómo se modela gold para BI y para ML a la vez?

Con esquemas en estrella (hechos con un grano declarado y dimensiones conformadas) para BI, y tablas de features por entidad y fecha para ML, ambos construidos desde las mismas tablas silver para que las cifras coincidan.

<!-- challenge -->

Finanzas reporta ingresos por región del cliente y quiere que las cifras del año pasado se mantengan cuando los clientes se mudan. ¿Qué tipo de dimensión usas y cómo se une la tabla de hechos?

<!-- solution -->

SCD tipo 2 en la dimensión de clientes, con una clave subrogada por versión. La tabla de hechos guarda la clave subrogada vigente al momento de la venta (o une por clave natural con `sale_date BETWEEN valid_from AND valid_to`), así las ventas viejas conservan su región antigua.

<!-- takeaways -->

- SCD2 guarda historia con rangos de vigencia; un `MERGE` puede mantenerla.
- Pon en cuarentena las filas malas con su motivo en vez de fallar o descartarlas en silencio.
- Construye gold de BI y ML desde el mismo silver para que las cifras coincidan.

### Lakeflow pipelines

<!-- unit: Elegir un enfoque de ETL -->

<!-- goals -->

- Contrastar el procesamiento procedural y el declarativo.
- Elegir entre pipelines, dbt, notebooks con jobs, procedimientos almacenados y Designer.

<!-- concept -->

Hay dos formas de describir el procesamiento de datos. El código procedural dice cómo: pasos ordenados, bucles y condiciones, con control total y ajuste manual. Los notebooks Spark orquestados con jobs funcionan así. El código declarativo dice qué: las tablas que quieres y las consultas detrás de ellas. El motor planea el orden, el procesamiento incremental y los reintentos.

Databricks recomienda Lakeflow pipelines, la opción declarativa, para la mayoría del ETL nuevo. Los proyectos dbt existentes corren tal cual, los notebooks y jobs sirven para lógica compleja escrita en código, los procedimientos almacenados empaquetan SQL procedural y Lakeflow Designer permite a quienes no programan construir las mismas transformaciones gobernadas de forma visual.

<!-- example -->

| Situación | Enfoque |
|---|---|
| ETL nuevo, batch o incremental | Lakeflow pipelines |
| El equipo ya mantiene modelos dbt | Tarea dbt en Lakeflow Jobs |
| Lógica compleja, llamadas a APIs externas por lote | Notebooks o scripts Spark + Lakeflow Jobs |
| SQL procedural reutilizable en un warehouse | Procedimientos almacenados (`CREATE PROCEDURE`) |
| Analistas que preparan datos sin código | Lakeflow Designer |

#### ¿Qué diferencia hay entre el procesamiento procedural y el declarativo?

El procesamiento procedural define cómo se procesan los datos, paso a paso, con estructuras de control (bucles, condicionales, funciones) y ajuste manual; da control total a cambio de más código y experiencia. El procesamiento declarativo define qué resultado quieres, y el sistema decide el plan de ejecución, el orden y las optimizaciones. El código de DataFrames Spark orquestado con jobs es sobre todo procedural; SQL y Lakeflow pipelines son declarativos.

#### ¿Cuándo elegir procesamiento procedural en vez de declarativo?

Procedural cuando necesitas un control fino de la ejecución, cuando las reglas de negocio son difíciles de expresar como definiciones de tablas (bucles procedurales, llamadas a sistemas externos por lote) o cuando el rendimiento exige ajuste manual. Declarativo cuando lo que más importa es la mantenibilidad, para transformaciones SQL y pipelines administrados, y cuando quieres procesamiento incremental, reintentos y calidad de datos integrados.

#### ¿Cómo eliges un enfoque de ETL en Databricks?

Empieza con Lakeflow pipelines para el ETL nuevo, batch o incremental, porque el motor maneja las dependencias, el procesamiento incremental y la orquestación. Conserva dbt si el equipo ya mantiene modelos dbt (ejecútalos como tareas dbt en jobs). Usa notebooks o scripts Spark con Lakeflow Jobs para lógica compleja escrita en código. Usa procedimientos almacenados para empaquetar SQL procedural reutilizable que corre en un SQL warehouse.

#### ¿Qué son los procedimientos almacenados y el SQL scripting en Databricks?

El SQL scripting agrega control procedural (variables, `IF`, bucles, manejo de excepciones) a Databricks SQL, y `CREATE PROCEDURE` guarda ese script como un objeto gobernado de Unity Catalog que recibe parámetros y se ejecuta con `CALL`. Sirven a equipos que migran código procedural de un warehouse y para rutinas SQL reutilizables.

#### ¿Qué es Lakeflow Designer?

Una herramienta visual y sin código para preparar datos, integrada en Databricks. Los usuarios construyen "visual data preps" en un lienzo de arrastrar y soltar a partir de operadores integrados (y de operadores propios basados en funciones de Unity Catalog), o describen los cambios en lenguaje natural con Genie Code. Cada visual data prep está respaldado por código listo para producción y gobernado por Unity Catalog, así que puede pasar a producción con Git, jobs y bundles sin que los ingenieros lo reconstruyan.

#### ¿Cuándo no usarías Lakeflow pipelines?

Cuando necesitas un control detallado de cada paso, lógica que no encaja en el modelo declarativo (código procedural complejo, llamadas a sistemas externos en cada lote) o portabilidad a jobs Spark sencillos. Muchos equipos usan jobs normales con Delta y `MERGE` y obtienen los mismos resultados con más código. Ten en cuenta que algunas funciones, como `AUTO CDC` y las expectations, existen en Databricks pero no en Spark Declarative Pipelines de código abierto.

<!-- challenge -->

Un equipo tiene 40 modelos dbt en producción, un conjunto nuevo de fuentes Kafka en streaming por ingerir y un analista que prepara a mano un archivo semanal. ¿Qué enfoque sugieres para cada caso?

<!-- solution -->

Conservar los modelos dbt y ejecutarlos como tareas dbt en un job de Lakeflow, porque reescribirlos no aporta nada. Ingerir Kafka con un Lakeflow pipeline (streaming tables y luego vistas materializadas). Darle Lakeflow Designer al analista, para que la preparación semanal se convierta en un visual data prep gobernado que se puede programar en vez de hacerse a mano.

<!-- takeaways -->

- Lo procedural dice cómo; lo declarativo dice qué y deja que el motor planee.
- Lakeflow pipelines es la opción por defecto para ETL nuevo; conserva dbt donde ya existe.
- Designer trae a quienes no programan a la misma plataforma gobernada.

<!-- unit: El modelo declarativo -->

<!-- goals -->

- Explicar qué gestiona por ti un pipeline y de qué está hecho.
- Elegir entre una streaming table, una vista materializada y una vista.

<!-- concept -->

En un Lakeflow pipeline defines las tablas que quieres y las consultas que las producen, en archivos SQL o Python. El motor resuelve las dependencias, ejecuta el trabajo en el orden correcto y en paralelo, reintenta fallos y gestiona el cómputo. Dejas de escribir código de orquestación y de checkpoints.

Tres tipos de datasets cubren casi todo. Una streaming table procesa cada fila de entrada una vez, ideal para ingesta y datos solo de append. Una vista materializada tiene semántica batch: se refresca, de forma incremental cuando puede, para coincidir siempre con sus fuentes, ideal para joins y agregaciones. Una vista se calcula bajo demanda dentro del pipeline y no guarda nada.

<!-- example -->

```sql
CREATE OR REFRESH STREAMING TABLE silver_orders
AS SELECT * FROM STREAM bronze_orders WHERE order_id IS NOT NULL;

CREATE OR REFRESH MATERIALIZED VIEW gold_sales_by_day
AS SELECT order_date, sum(amount) AS sales FROM silver_orders GROUP BY order_date;
```

#### ¿Qué son los Lakeflow pipelines (antes Delta Live Tables)?

El framework declarativo de Databricks para pipelines batch y de streaming: defines las tablas y las consultas que las producen, en SQL o Python, y Databricks deduce las dependencias, orquesta la ejecución, administra la infraestructura, reintenta los fallos y aplica las expectativas de calidad de datos. El producto se llamó Delta Live Tables (DLT), luego Lakeflow Declarative Pipelines en 2025 y ahora Lakeflow pipelines. Se basa en Apache Spark Declarative Pipelines (SDP), que Databricks donó a Apache Spark 4.1. El código DLT existente sigue funcionando, y los SKU clásicos y los nombres del event log todavía usan `dlt`.

#### ¿De qué está hecho un pipeline?

De archivos fuente (SQL o Python, por defecto en una carpeta `transformations` dentro de la carpeta raíz del pipeline) que definen flows, streaming tables, vistas materializadas, vistas y sinks, más la configuración: cómputo, catálogo y esquema por defecto, modo de disparo, parámetros, identidad run-as y notificaciones. Los archivos pueden ir en cualquier orden, porque el pipeline resuelve solo las dependencias. Se editan en el Lakeflow Pipelines Editor, que puede ejecutar el pipeline completo, un archivo o una tabla.

#### ¿Qué diferencia hay entre una streaming table y una vista materializada?

Una streaming table procesa cada fila de entrada una sola vez, añadiendo o actualizando de forma incremental, lo que sirve para la ingesta y los datos que solo crecen. Una vista materializada guarda el resultado de una consulta y se refresca (de forma incremental cuando se puede) para reflejar siempre sus fuentes, lo que sirve para agregaciones y joins sobre datos que cambian. Cambiar la consulta de una streaming table solo afecta a las filas procesadas después; una vista materializada aplica la nueva consulta a todo en su siguiente refresco.

```sql
CREATE OR REFRESH STREAMING TABLE bronze_orders
AS SELECT * FROM STREAM read_files('/Volumes/raw/landing/orders/', format => 'json');

CREATE OR REFRESH MATERIALIZED VIEW gold_daily_sales
AS SELECT order_date, sum(amount) AS sales FROM silver_orders GROUP BY order_date;
```

#### ¿Cómo se refresca de forma incremental una vista materializada?

En cada actualización, el motor incremental de Databricks (Enzyme) revisa qué cambió en las fuentes y, cuando la consulta lo permite, actualiza solo las filas afectadas. Si no, recalcula todo el resultado. El resultado siempre es correcto; solo cambia el costo. El refresco incremental requiere cómputo serverless, y no toda consulta se puede refrescar de forma incremental (algunas UDF y funciones no deterministas obligan a recalcular todo).

#### ¿Qué es una vista dentro de un pipeline?

Un dataset (`CREATE TEMPORARY VIEW`, o `@dp.temporary_view` en Python) que se evalúa bajo demanda y no se guarda. Divide la lógica compleja en pasos y puede llevar expectations para validar resultados intermedios, pero solo se puede usar dentro del mismo pipeline.

#### ¿Cómo se escribe un pipeline en Python?

Con el módulo `pyspark.pipelines` (antes `dlt`, que sigue funcionando): funciones decoradas que devuelven DataFrames. `@dp.table` define una streaming table a partir de un DataFrame de streaming, `@dp.materialized_view` una vista materializada a partir de un DataFrame batch y `@dp.temporary_view` una vista. Las expectations son otros decoradores.

```python
from pyspark import pipelines as dp

@dp.table(comment="Pedidos limpios")
@dp.expect_or_drop("valid_amount", "amount >= 0")
def silver_orders():
    return spark.readStream.table("bronze_orders").dropDuplicates(["order_id"])

@dp.materialized_view
def gold_sales_by_day():
    return spark.read.table("silver_orders").groupBy("order_date").sum("amount")
```

#### ¿Dónde viven las tablas de un pipeline?

En Unity Catalog, en el catálogo y el esquema por defecto del pipeline (o en otros si se usan nombres completos). Son tablas Delta administradas que cualquiera con permisos puede leer, mantenidas por la optimización predictiva, pero solo el pipeline que las define puede escribir en ellas. Sus tablas internas de respaldo están en un catálogo oculto, `__databricks_internal`.

#### ¿Qué son las streaming tables y vistas materializadas independientes?

Streaming tables y vistas materializadas creadas directamente en Databricks SQL (o en un notebook serverless) en vez de dentro de un pipeline. Databricks crea y administra por detrás un pipeline para cada una (con el tipo `MV/ST` en Jobs & Pipelines), y se refrescan bajo demanda o con `SCHEDULE`. Dan a los analistas tablas incrementales sin montar un pipeline.

#### ¿Qué limitaciones tienen las streaming tables y las vistas materializadas?

Cada una pertenece a un solo pipeline, y otros pipelines o jobs no pueden escribir en ella. No pueden ser origen ni destino de un clon profundo o superficial. Quien no es administrador necesita el privilegio `REFRESH` para ver el pipeline de respaldo. Las streaming tables necesitan streams acotados (o un watermark) para evitar presión de memoria, y sus joins stream-static no se recalculan cuando cambia una dimensión.

<!-- challenge -->

Los pedidos llegan solo como append; los reembolsos actualizan pedidos viejos. Necesitas el ingreso diario neto de reembolsos. ¿Qué tablas son streaming tables y cuál es una vista materializada?

<!-- solution -->

Ingerir pedidos y reembolsos como streaming tables (cada evento se procesa una vez). Calcular el ingreso diario neto como vista materializada que une ambas, porque un reembolso cambia el resultado de un día pasado, lo que una vista materializada recalcula y una streaming table no.

<!-- takeaways -->

- Declara tablas y consultas; el motor maneja orden, reintentos y cómputo.
- Las streaming tables procesan cada fila una vez; las vistas materializadas siguen correctas si cambian las fuentes.
- En Python se usan `@dp.table`, `@dp.materialized_view` y `@dp.temporary_view`.

<!-- unit: Flows, sinks y refrescos focalizados -->

<!-- goals -->

- Usar flows para combinar fuentes, cargar historia y escribir fuera de Databricks.
- Elegir entre un flow REPLACE WHERE y una vista materializada.

<!-- concept -->

Detrás de cada tabla de un pipeline hay al menos un flow: una consulta que lee una fuente y escribe en un destino, en batch o en streaming. Normalmente el flow es implícito y se crea con la tabla. Los flows explícitos permiten que varias fuentes alimenten una tabla (fan-in), agregar una fuente sin full refresh o cargar la historia una sola vez con un flow de backfill.

Los destinos no se limitan a tablas de Unity Catalog. Los sinks escriben un stream en Kafka, Event Hubs, tablas Delta externas o destinos Python propios. Para trabajo batch que reescribe una ventana reciente, un flow REPLACE WHERE refresca solo las filas que cumplen un predicado.

<!-- example -->

```sql
CREATE OR REFRESH STREAMING TABLE all_orders;

CREATE FLOW orders_us AS INSERT INTO all_orders BY NAME SELECT * FROM STREAM us_orders;
CREATE FLOW orders_eu AS INSERT INTO all_orders BY NAME SELECT * FROM STREAM eu_orders;
-- carga única del archivo histórico
CREATE FLOW orders_archive AS INSERT INTO ONCE all_orders BY NAME
SELECT * FROM archive.orders_2020_2024;
```

#### ¿Qué es un flow en un pipeline?

Una consulta más un destino: lee una fuente, aplica la lógica y escribe en una streaming table, una vista materializada o un sink, con semántica batch o de streaming. Definir una tabla con una consulta crea un flow por defecto con el mismo nombre. Los flows explícitos (`CREATE FLOW`, `@dp.append_flow`) se definen aparte del destino, así que varios pueden escribir en una misma tabla.

#### ¿Qué tipos de flows existen?

Append flows (los más comunes: en cada actualización se agregan al destino las filas nuevas de la fuente), flows `AUTO CDC` (aplican datos de cambios a una streaming table), flows de vista materializada (batch, recalculados de forma incremental cuando se puede), update flows (solo Python, en preview: emiten a un sink las filas cambiadas de una agregación en streaming) y flows REPLACE WHERE (reemplazan las filas que cumplen un predicado).

#### ¿Cómo cargas historia (backfill) en una streaming table?

Agregando un append flow con `ONCE` (`INSERT INTO ONCE` en SQL, `once=True` en Python) que lee la fuente histórica como batch. Corre una sola vez y solo vuelve a correr tras un full refresh del destino, mientras los flows de streaming habituales siguen.

#### ¿Por qué usar varios append flows en vez de un `UNION`?

Con un `UNION` en una sola consulta, agregar una fuente cambia la consulta y puede exigir un full refresh. Con un append flow por fuente (fan-in), agregas o quitas una fuente sin tocar las demás ni reprocesar sus datos, y cada flow conserva su propio checkpoint.

#### ¿Qué es un sink en un pipeline?

Un destino de streaming fuera de las tablas administradas por el pipeline: tópicos de Kafka, Azure Event Hubs, tablas Delta externas de Unity Catalog o por ruta, o cualquier destino mediante una fuente de datos Python propia o `foreach_batch_sink`. Se crea con `dp.create_sink` y se escribe con un append flow. Los sinks son solo para Python, solo aceptan flows de streaming de tipo append (o update), no admiten expectations, y un full refresh no limpia los datos ya escritos en ellos.

```python
dp.create_sink("orders_out", "kafka",
               {"kafka.bootstrap.servers": "broker:9092", "topic": "orders_enriched"})

@dp.append_flow(target="orders_out")
def publish_orders():
    return (spark.readStream.table("silver_orders")
            .selectExpr("CAST(order_id AS STRING) AS key", "to_json(struct(*)) AS value"))
```

#### ¿Cuándo usas sinks?

Para reverse ETL y usos operativos: devolver eventos enriquecidos a Kafka para una aplicación, escribir en una tabla Delta fuera del catálogo del pipeline o alimentar un almacén que Databricks no soporta de forma nativa. `foreach_batch_sink` cubre los upserts y la escritura de un lote en varios destinos.

#### ¿Qué es un flow REPLACE WHERE?

Un flow batch que borra las filas del destino que cumplen un predicado y las reemplaza volviendo a ejecutar la consulta de origen solo para ese rango, sin tocar las demás filas. Su costo depende del tamaño del rango, no de la tabla, lo que sirve para ETL que reescribe los últimos días. En 2026 estaba en Beta y necesita serverless para el refresco incremental.

```sql
CREATE STREAMING TABLE orders_enriched
FLOW REPLACE WHERE order_date >= date_add(current_date(), -7) BY NAME
SELECT o.*, p.product_name FROM orders_fct o JOIN product_dim p USING (product_id);
```

#### ¿Cuándo prefieres un flow REPLACE WHERE a una vista materializada?

Cuando el destino debe guardar datos por más tiempo que la fuente, cuando un cambio en una dimensión no debe recalcular toda la historia, cuando el esquema evoluciona sin recalcularlo todo o cuando quieres un costo predecible por refresco. Una vista materializada mantiene correcto todo el resultado pero puede caer en un recálculo completo. Protege la tabla contra full refreshes (`pipelines.reset.allowed = false`), porque un full refresh conserva solo el rango del predicado actual.

<!-- challenge -->

Un pipeline debe cargar una vez 5 años de historia desde una tabla de archivo, luego seguir un tópico de Kafka y además publicar cada pedido limpio en otro tópico de Kafka para la aplicación de seguimiento de pedidos. Esboza los flows.

<!-- solution -->

Una streaming table, `orders`, alimentada por dos append flows: uno de streaming desde el tópico de Kafka y uno de backfill con `ONCE` desde el archivo. Luego un sink creado con `dp.create_sink` para el tópico de salida, escrito por un append flow que lee `orders` como stream y serializa cada fila en JSON.

<!-- takeaways -->

- Cada tabla tiene al menos un flow; los flows explícitos permiten fan-in y backfills.
- Los sinks escriben streams fuera de las tablas del pipeline, solo desde Python.
- Los flows REPLACE WHERE refrescan el rango de un predicado con un costo acotado a ese rango.

<!-- unit: Change data capture con AUTO CDC -->

<!-- goals -->

- Aplicar un feed de cambios o una serie de snapshots a una tabla destino.
- Conservar historia SCD tipo 1 o tipo 2 sin código de `MERGE`.

<!-- concept -->

Las fuentes que modifican filas, y no solo agregan, envían un feed de cambios (una fila por inserción, actualización o borrado) o snapshots completos. Aplicar cualquiera de los dos a mano exige un `MERGE` que maneje eventos desordenados, borrados e historia.

`AUTO CDC` lo hace de forma declarativa. Das las claves y una columna de secuencia, y el flow ordena los eventos por secuencia y no por llegada, aplica borrados y truncados, y guarda el resultado como SCD tipo 1 (último estado) o tipo 2 (una fila por versión). `AUTO CDC FROM SNAPSHOT` compara snapshots consecutivos para deducir los cambios cuando la fuente no tiene feed de cambios.

<!-- example -->

```sql
CREATE OR REFRESH STREAMING TABLE silver_customers;

CREATE FLOW customers_cdc AS AUTO CDC INTO silver_customers
FROM STREAM bronze_customer_changes
KEYS (customer_id)
APPLY AS DELETE WHEN op = 'D'
SEQUENCE BY change_ts
COLUMNS * EXCEPT (op, change_ts)
STORED AS SCD TYPE 2
TRACK HISTORY ON * EXCEPT (last_login);
```

#### ¿Cómo se maneja la CDC en Lakeflow pipelines?

Con `AUTO CDC` (antes `APPLY CHANGES INTO`, con la misma sintaxis), que aplica un flujo de cambios a una streaming table usando claves y una columna de secuencia, maneja eventos desordenados y borrados, y puede conservar el historial como SCD tipo 1 o tipo 2 sin escribir lógica de `MERGE`. Requiere la edición Pro o Advanced (o serverless) y no forma parte de Spark Declarative Pipelines de código abierto.

```python
from pyspark.sql.functions import col, expr

dp.create_streaming_table("silver_customers")
dp.create_auto_cdc_flow(
    target="silver_customers", source="bronze_customer_changes",
    keys=["customer_id"], sequence_by=col("change_ts"),
    apply_as_deletes=expr("op = 'D'"),
    except_column_list=["op", "change_ts"],
    stored_as_scd_type=2)
```

#### ¿Cómo maneja `AUTO CDC` los eventos desordenados?

Ordena los cambios por la columna de `SEQUENCE BY`, no por la hora de llegada. Un evento tardío con un valor de secuencia menor que el ya aplicado no sobrescribe el estado más nuevo (en SCD tipo 2, se ubica en la historia en el punto correcto). Para los empates, secuencia por un struct (`SEQUENCE BY STRUCT(change_ts, change_id)`): los campos se comparan en orden. La columna de secuencia debe ser ordenable y no puede ser nula.

#### ¿Cómo se ve SCD tipo 2 en un destino de `AUTO CDC`?

Cada versión de una clave es una fila con columnas `__START_AT` y `__END_AT`, tomadas de los valores de secuencia; la fila vigente tiene `__END_AT` nulo. `TRACK HISTORY ON` (o `track_history_except_column_list`) elige qué columnas crean una nueva versión; los cambios en las demás actualizan la fila vigente en su lugar.

#### ¿Qué son `APPLY AS DELETE` y `APPLY AS TRUNCATE`?

Condiciones que marcan filas de cambio como borrados (eliminan la clave) o truncados (vacían el destino hasta ese punto de la secuencia). En SCD tipo 2, un borrado cierra la versión vigente en vez de borrar la historia.

#### ¿Qué es `AUTO CDC FROM SNAPSHOT`?

Un flow para fuentes que solo entregan snapshots completos, como un volcado nocturno de una tabla. Compara cada snapshot con el anterior, en orden ascendente de versión, y deduce inserciones, actualizaciones y borrados (las claves que faltan en un snapshot más nuevo se borran). En SQL, `FROM SNAPSHOT (consulta) WITH VERSION (consulta)` define el snapshot y su versión; en Python, `create_auto_cdc_from_snapshot_flow`. No admite expectations.

#### ¿Cómo lees los cambios aguas abajo de una tabla `AUTO CDC`?

No haciendo streaming directo de la tabla, porque recibe actualizaciones y borrados, que una lectura en streaming de una tabla no acepta. Lee en cambio su change data feed, o construye el dataset siguiente como vista materializada.

<!-- challenge -->

Un proveedor envía cada noche una exportación completa de 2 millones de productos, sin marcas de cambio. Necesitas el catálogo actual y la historia de cambios de precio. ¿Qué construyes?

<!-- solution -->

Un flow `AUTO CDC FROM SNAPSHOT` hacia una streaming table con clave `product_id`, con la fecha de exportación como versión del snapshot, guardado como SCD tipo 2 y con historia sobre `price` (y los demás atributos que importen). Los productos que faltan en un snapshot se cierran como borrados. El catálogo actual son las filas con `__END_AT` nulo.

<!-- takeaways -->

- `AUTO CDC` reemplaza el `MERGE` escrito a mano para feeds de cambios.
- La secuencia, no el orden de llegada, decide el estado final.
- Los snapshots sin marcas de cambio también pueden producir CDC y SCD tipo 2.

<!-- unit: Calidad y operación de pipelines -->

<!-- goals -->

- Agregar expectations a un pipeline y actuar según sus métricas.
- Ejecutar, validar, monitorear y refrescar un pipeline con seguridad.

<!-- concept -->

Las expectations declaran reglas de calidad sobre un dataset con una política para las violaciones: conservarlas y registrarlas, descartar la fila o fallar la actualización. Sus métricas quedan en el event log.

En la operación, el modo triggered procesa lo disponible y se detiene; el continuo se queda encendido. Las ejecuciones manuales desde el editor reutilizan el cluster y no reintentan, para que veas los errores de inmediato; las de jobs y de la API reinician y reintentan. Un dry run valida las definiciones sin escribir datos. Un full refresh reconstruye una tabla desde cero, lo cual es potente pero costoso y riesgoso si la fuente ya no guarda su historia.

<!-- example -->

```python
rules = {"valid_id": "order_id IS NOT NULL", "valid_amount": "amount >= 0"}

@dp.table
@dp.expect_all_or_drop(rules)          # descarta las filas que rompan cualquier regla
@dp.expect("recent", "order_date >= '2020-01-01'")   # solo registra las violaciones
def silver_orders():
    return spark.readStream.table("bronze_orders")
```

#### ¿Qué son las expectativas (expectations)?

Reglas de calidad de datos declaradas sobre una streaming table, una vista materializada o una vista. Cada fila se comprueba contra una condición booleana SQL, y la política decide qué pasa ante una infracción: conservarla y registrarla (`EXPECT`, por defecto), descartar la fila (`ON VIOLATION DROP ROW`) o hacer fallar la actualización (`ON VIOLATION FAIL UPDATE`, que revierte la transacción). Las métricas de advertencia y descarte se ven en la interfaz del pipeline y en el event log. Las condiciones no pueden llamar funciones Python ni consultar otras tablas.

```sql
CONSTRAINT valid_amount EXPECT (amount >= 0) ON VIOLATION DROP ROW
```

#### ¿Cómo reutilizas un conjunto de expectations en varias tablas?

En Python, pon las reglas en un diccionario (o cárgalas desde una tabla o un archivo) y aplícalas con `@dp.expect_all`, `@dp.expect_all_or_drop` o `@dp.expect_all_or_fail`. Tener las reglas en un solo lugar las hace revisables y coherentes.

#### ¿Qué diferencia hay entre el modo triggered y el modo continuo de un pipeline?

El modo triggered (por defecto) procesa los datos disponibles al inicio de la actualización y se detiene (más barato, para programaciones batch). El modo continuo mantiene el pipeline en marcha para procesar los datos con baja latencia; en producción, ejecútalo desde un job continuo para que se reinicie si falla.

#### ¿Qué reemplazó al modo de desarrollo en los pipelines?

Ahora el comportamiento depende de cómo arranca la actualización. Las ejecuciones manuales desde la interfaz y el editor usan inicio rápido: el cluster se reutiliza (sigue encendido dos horas por defecto) y los reintentos están desactivados, así que los errores aparecen de inmediato, que es lo que hacía el antiguo modo de desarrollo. Las actualizaciones de jobs, de la API y continuas reinician el cluster ante errores recuperables, reintentan y lo apagan al terminar, como el antiguo modo de producción. "Run now with different settings" lo cambia para una ejecución.

#### ¿Qué es un dry run de un pipeline?

Una actualización de validación que resuelve todas las definiciones de datasets y flows (nombres de tablas, columnas, dependencias, sintaxis) sin materializar ni publicar datos. Detecta errores en segundos en vez de al final de una actualización larga.

#### ¿Se puede refrescar solo una parte de un pipeline?

Sí. Puedes refrescar tablas seleccionadas desde el editor o la interfaz, o usar "Refresh failed tables" para volver a ejecutar solo las tablas que fallaron y sus dependencias aguas abajo. Para los flows de streaming, la API puede reiniciar el checkpoint de flows seleccionados sin borrar sus datos.

#### ¿Qué es el event log del pipeline?

Una tabla Delta que registra todos los eventos de un pipeline: actualizaciones, avance de los flujos, métricas de calidad de datos, linaje y errores. Se consulta para construir dashboards de monitoreo y de calidad de datos.

#### ¿Qué es un full refresh de una tabla del pipeline?

Para una vista materializada, un recálculo completo. Para una streaming table, vaciar sus datos y checkpoints y reprocesar todos los datos de origen desde el principio. Hace falta tras cambios de lógica que deben aplicarse al historial, pero puede ser costoso y puede perder datos si la retención del origen es más corta que el historial. Define `pipelines.reset.allowed = false` en las tablas que nunca deben tener un full refresh.

#### ¿Con qué identidad corre un pipeline?

Por defecto, con la de su propietario. Puedes cambiar la identidad run-as a un service principal (lo recomendado en producción), otro usuario o un grupo; las tablas publicadas pasan a pertenecer a la nueva identidad. Así los pipelines siguen funcionando cuando su creador se va.

#### ¿Cómo se factura un pipeline?

Por el cómputo del pipeline (serverless o clásico) según la edición del producto: Core (ingesta en streaming), Pro (añade CDC) y Advanced (añade expectativas). Los pipelines serverless incluyen todas las funciones, se facturan por uso y son los recomendados para pipelines nuevos; con cómputo clásico, usa el autoscaling mejorado.

<!-- challenge -->

Un compañero quiere hacer un full refresh de la tabla bronze por un arreglo de parsing. El tópico de Kafka de origen guarda 7 días. ¿Sobre qué le adviertes?

<!-- solution -->

Un full refresh trunca la tabla y vuelve a leer la fuente desde el inicio, pero Kafka solo tiene 7 días: se perdería la historia anterior. Mejor corregir el parsing en silver, o reprocesar solo lo reciente, y mantener bronze (o los archivos crudos) como copia de largo plazo, y definir `pipelines.reset.allowed = false` en bronze para que nadie lo haga por accidente.

<!-- takeaways -->

- Las expectations hacen visibles y aplicables las reglas de calidad.
- Las ejecuciones manuales fallan rápido; las de jobs reintentan. Los dry runs validan sin escribir.
- Los full refresh vuelven a leer las fuentes; revisa antes su retención o bloquéalos.

### Jobs y orquestación

<!-- unit: Jobs, tareas y disparadores -->

<!-- goals -->

- Construir un job como DAG de tareas con el cómputo y disparador adecuados.
- Decidir cuándo basta Lakeflow Jobs y cuándo usar Airflow.

<!-- concept -->

Un job es un DAG de tareas: notebooks, scripts, SQL, dbt, pipelines u otros jobs, cada una con dependencias, cómputo, reintentos y timeouts. Los disparadores lo inician por calendario, al llegar archivos o al actualizarse una tabla de origen. Las tareas de control de flujo agregan bucles (For each) y bifurcaciones (If/else), y las condiciones "Run if" deciden qué corre después de un fallo.

Si el flujo vive sobre todo en Databricks, Jobs es más simple y barato que un orquestador externo. Airflow se gana su lugar cuando el DAG abarca muchos sistemas.

<!-- example -->

```text
ingest_orders ─┐
               ├─► build_silver ─► check_quality ─► if rows > 0 ─► publish_gold
ingest_stores ─┘                                      └── else ──► notify
```

#### ¿Qué son los Lakeflow Jobs (antes Workflows)?

El orquestador integrado de Databricks. Un job es un DAG de tareas (notebooks, scripts Python, wheels, SQL, dbt, pipelines, JAR, otros jobs) con dependencias, programaciones o disparadores, parámetros, reintentos, timeouts, notificaciones y configuración de cómputo.

#### ¿Qué tipos de tarea puede tener un job?

Notebook, script Python, wheel Python, SQL (consulta, archivo, dashboard o alerta), dbt, pipeline, JAR, Spark Submit, Run Job (otro job), condición If/else y For each (bucle sobre valores).

#### ¿Qué disparadores pueden iniciar un job?

Una programación cron, la llegada de un archivo a una ubicación de almacenamiento, la actualización de una tabla (cuando cambia una tabla de origen), el modo continuo (reiniciar en cuanto termina), la API o la CLI, o una ejecución manual.

#### ¿Qué diferencia hay entre el cómputo de jobs y ejecutar tareas en un cluster compartido?

Cada tarea puede usar su propio cluster de job, compartir un cluster de job con otras tareas de la misma ejecución, usar cómputo serverless o usar un cluster all-purpose existente. Los clusters de job compartidos evitan arranques repetidos; serverless elimina el arranque por completo.

#### ¿Qué hace la tarea For each?

Ejecuta una tarea anidada una vez por cada elemento de una lista (por ejemplo una lista de países o de fechas), con una concurrencia configurable, para no tener que definir una tarea por elemento.

#### ¿Para qué sirve la tarea de condición If/else?

Para ramificar un job según un valor, como un task value, un parámetro del job o un valor dinámico, comparado con `==`, `!=`, `>`, `>=`, `<` o `<=`: por ejemplo, saltarse el paso de publicación cuando una tarea de calidad de datos informa cero filas válidas.

#### ¿Qué son las dependencias "Run if"?

Un ajuste por tarea que decide cuándo corre según cómo terminaron sus tareas anteriores: todas con éxito (por defecto), al menos una con éxito, ninguna fallida, todas terminadas, al menos una fallida o todas fallidas. "Todas terminadas" sirve para tareas de limpieza, y "al menos una fallida" para una alerta o un rollback propios.

#### ¿Qué hace desactivar una tarea?

La salta en tiempo de ejecución sin borrarla, conservando su configuración y su historial. Las tareas siguientes se evalúan entonces según sus condiciones "Run if". Sirve para pausar un paso, como una exportación, mientras el resto del job sigue corriendo.

#### ¿Cómo se administran los jobs como código?

Con Declarative Automation Bundles (YAML en Git, desplegado con la CLI), o con la CLI de Databricks, los SDK, la API REST de Jobs o Terraform. Las definiciones de jobs también pueden tomar el código de las tareas de una referencia Git. Definir jobs en la interfaz está bien para explorar, pero no para producción.

#### ¿Qué límites conviene conocer en Lakeflow Jobs?

Por workspace: 2.000 ejecuciones de tareas concurrentes (más devuelve HTTP 429), 10.000 jobs creados por hora (incluido runs submit) y 12.000 jobs guardados. Un job puede tener hasta 1.000 tareas. Los DAG muy grandes suelen indicar que conviene dividir el trabajo en varios jobs unidos con tareas Run Job o disparadores por actualización de tabla.

#### ¿Conviene orquestar Databricks con Airflow o con Jobs?

Jobs basta cuando el flujo vive principalmente en Databricks, y es más barato y más simple. Airflow (o Dagster, Prefect) tiene sentido cuando el DAG abarca muchos sistemas, cuando la empresa ya lo tiene como estándar o para dependencias complejas entre equipos. El provider de Databricks para Airflow puede lanzar jobs y esperar a que terminen.

<!-- challenge -->

Un job debe correr cada vez que cambia la tabla `silver.orders` del equipo de origen, pero no más de una vez cada 30 minutos. ¿Cómo lo disparas?

<!-- solution -->

Usar un disparador por actualización de tabla sobre `silver.orders` con un tiempo mínimo entre disparos de 30 minutos (o espera tras el último cambio), y fijar máximo una ejecución concurrente con cola.

<!-- takeaways -->

- Un job es un DAG de tareas con su propio cómputo, reintentos y timeouts.
- Dispara por calendario, llegada de archivos o actualización de tablas.
- Usa Jobs para flujos centrados en Databricks; Airflow para los que cruzan sistemas.

<!-- unit: Ejecuciones confiables: parámetros, idempotencia y backfills -->

<!-- goals -->

- Hacer que un job sea seguro de re-ejecutar y de hacer backfill.
- Pasar parámetros y valores pequeños entre tareas.

<!-- concept -->

Un job confiable da el mismo resultado si corre una vez o tres. Eso exige escrituras que reemplazan o fusionan en vez de agregar, y una fecha de proceso que viene de un parámetro y no del reloj. Referencias dinámicas como `{{job.start_time.iso_date}}` dan ese contexto.

Con tareas idempotentes, recuperarse es fácil: reparar una ejecución para correr solo las tareas que fallaron, limitar la concurrencia para que no se solapen y hacer backfill recorriendo fechas.

<!-- example -->

```python
# Task parameter: process_date = {{job.start_time.iso_date}}
process_date = dbutils.widgets.get("process_date")
(daily_df.write.mode("overwrite")
   .option("replaceWhere", f"event_date = '{process_date}'")   # rerun-safe
   .saveAsTable("silver.events"))
dbutils.jobs.taskValues.set("row_count", daily_df.count())
```

#### ¿Qué son los parámetros de job y las referencias a valores dinámicos?

Parámetros definidos a nivel de job que se pasan a todas las tareas y se pueden sobrescribir en cada ejecución. Las referencias dinámicas como `{{job.start_time.iso_date}}` o `{{job.run_id}}` inyectan el contexto de la ejecución, útil para un procesamiento idempotente basado en fechas.

#### ¿Cómo se pasan valores entre tareas?

Los valores pequeños con task values (`dbutils.jobs.taskValues.set` en una tarea y `get` en otra posterior, o referencias dinámicas como `{{tasks.ingest.values.row_count}}` en los parámetros de la tarea). Los datos en sí deben pasar por tablas, no por task values.

#### ¿Cómo se hace idempotente un job de Databricks?

Escribiendo con `MERGE` o con `replaceWhere`/sobrescritura dinámica de particiones para la fecha procesada en lugar de appends a ciegas, tomando la fecha de procesamiento de un parámetro y no del reloj, usando checkpoints de streaming para la ingesta incremental y haciendo que los efectos secundarios (notificaciones, exportaciones) se puedan repetir sin problema.

#### ¿Cómo se vuelve a ejecutar solo la parte fallida de un job?

Con "Repair run", que vuelve a ejecutar las tareas fallidas y sus dependientes, reutilizando los resultados correctos de las tareas anteriores, opcionalmente con parámetros nuevos.

#### ¿Cómo se limitan las ejecuciones concurrentes de un job?

Con el ajuste de máximo de ejecuciones concurrentes (normalmente 1 para los jobs que escriben en las mismas tablas) y la opción de cola, para que un nuevo disparo espere en lugar de omitirse o ejecutarse en paralelo.

#### ¿Cómo te enteras cuando un job falla o va lento?

Configurando notificaciones (correo, Slack, Teams, PagerDuty, webhooks) al iniciar, al terminar con éxito, al fallar y al superar umbrales de duración, y definiendo un timeout y un máximo de ejecuciones concurrentes. Las tablas del sistema sobre ejecuciones de jobs permiten construir dashboards de confiabilidad a más largo plazo.

#### ¿Cómo observas jobs, pipelines e ingesta en todo un workspace?

Combinando las interfaces de ejecución (logs, métricas y líneas de tiempo por tarea) con las tablas del sistema: el esquema `system.lakeflow` registra jobs, tareas y líneas de tiempo de ejecución en toda la cuenta, `system.billing.usage` agrega el costo por job o pipeline, y el event log de cada pipeline da el avance de los flows, la calidad de datos y los errores. Los dashboards y alertas SQL sobre estas tablas detectan cargas que fallan, van lentas o cuestan demasiado antes de que lo noten los usuarios.

#### ¿Cómo se ejecuta un job para hacer el backfill de muchas fechas?

Parametrizando el job por fecha y lanzándolo por cada fecha (con la API, la CLI o una tarea For each sobre una lista de fechas), manteniendo las escrituras idempotentes y limitando la concurrencia para que el backfill no deje sin recursos a la producción.

#### Un job diario escribe duplicados cada vez que se vuelve a ejecutar. ¿Qué cambias?

Reemplazo el append por una escritura idempotente: un `MERGE` sobre la clave de negocio, o `replaceWhere` sobre la fecha procesada. Tomo la fecha de un parámetro del job y añado un control de unicidad sobre el destino.

<!-- challenge -->

Debes hacer backfill de 2 años de datos diarios con un job que normalmente procesa un día. ¿Cómo lo corres sin afectar producción?

<!-- solution -->

Asegurar que el job sea idempotente por fecha y luego correr una tarea For each (o llamadas a la API) sobre las 730 fechas con concurrencia limitada, en cómputo de jobs aparte, quizá fuera de horario laboral. Revisar después los conteos de filas por fecha.

<!-- takeaways -->

- Las escrituras idempotentes (`MERGE`, `replaceWhere`) hacen seguras las re-ejecuciones.
- Toma la fecha de proceso de un parámetro, nunca del reloj.
- La reparación de ejecuciones re-ejecuta solo lo que falló.

<!-- stage: Gobernar los datos -->

### Unity Catalog y gobierno

<!-- unit: Modelo de objetos y almacenamiento -->

<!-- goals -->

- Nombrar la jerarquía de Unity Catalog y referirse a objetos con nombres de tres niveles.
- Explicar cómo storage credentials, external locations y volúmenes gobiernan los archivos.

<!-- concept -->

Unity Catalog es una sola capa de gobierno para todos los workspaces de una región. Todo está en una jerarquía: metastore, catálogo, esquema y luego tablas, vistas, volúmenes, funciones y modelos, referidos como `catalog.schema.object`.

El acceso al almacenamiento cloud también se gobierna. Una storage credential envuelve una identidad cloud, una external location la asocia a una ruta y los volúmenes exponen archivos en rutas gobernadas. Los workspaces antiguos aún tienen un metastore Hive, que se migra a Unity Catalog.

<!-- example -->

```text
metastore (eu-west-1)
└── catalog: prod
    ├── schema: bronze ── table: orders
    ├── schema: gold   ── table: fct_sales, view: v_sales_eu
    └── schema: raw    ── volume: landing  → /Volumes/prod/raw/landing/
```

#### ¿Qué es Unity Catalog?

La capa de gobierno unificada de Databricks para los activos de datos e IA de todos los workspaces: un solo lugar para definir el control de acceso, la auditoría, el linaje, el descubrimiento de datos y el uso compartido de tablas, vistas, volúmenes, funciones y modelos. También se publicó como código abierto.

#### ¿Cuál es la jerarquía de objetos de Unity Catalog?

Metastore (uno por región) → catálogo → esquema (base de datos) → tablas, vistas, vistas materializadas, volúmenes, funciones y modelos. Los objetos se nombran con tres niveles: `catalogo.esquema.tabla`.

#### ¿Qué es un volumen?

Un objeto de Unity Catalog que gobierna el acceso a archivos no tabulares (CSV, JSON, imágenes, PDF, wheels) en el almacenamiento en la nube, con rutas del tipo `/Volumes/catalogo/esquema/volumen/ruta`. Los volúmenes administrados viven en el almacenamiento administrado por Unity Catalog; los externos apuntan a una ruta de almacenamiento existente.

#### ¿Qué son las storage credentials y las external locations?

Una storage credential encapsula una identidad de nube (un rol IAM de AWS, una identidad administrada de Azure) con acceso al almacenamiento. Una external location combina una ruta de almacenamiento con una credencial, y los permisos sobre ella controlan quién puede crear allí tablas o volúmenes externos.

#### ¿Qué es el information schema en Unity Catalog?

Un conjunto de vistas SQL estándar en cada catálogo (`information_schema.tables`, `columns`, `table_privileges` y otras) que describen los objetos y los permisos, útiles para la documentación y las auditorías.

#### ¿Qué es el Hive metastore heredado y cómo se migra desde él?

El metastore por workspace anterior a Unity Catalog, con permisos locales al workspace. La migración consiste en crear un metastore de Unity Catalog, actualizar las tablas (`SYNC` para las externas, `CREATE TABLE … AS SELECT` o deep clone para las administradas) y cambiar el código a nombres de tres niveles. La herramienta UCX automatiza gran parte de la evaluación y la migración.

<!-- challenge -->

Un notebook lee `hive_metastore.sales.orders` y escribe archivos en `dbfs:/mnt/exports`. Enumera los pasos para migrarlo.

<!-- solution -->

Subir la tabla a Unity Catalog (`SYNC` si es externa, deep clone o CTAS si es gestionada), cambiar el código al nombre de tres niveles como `prod.sales.orders`, reemplazar el mount por un volumen respaldado por una external location y otorgar los privilegios necesarios al service principal del job.

<!-- takeaways -->

- Todo objeto tiene un nombre de tres niveles: `catalog.schema.object`.
- Storage credentials y external locations gobiernan el acceso a rutas.
- Los volúmenes reemplazan los mounts de DBFS para archivos.

<!-- unit: Identidades y permisos -->

<!-- goals -->

- Otorgar privilegios teniendo en cuenta herencia y propiedad.
- Ejecutar producción con service principals y manejar secretos con seguridad.

<!-- concept -->

Los privilegios se otorgan a usuarios, grupos o service principals y bajan por la jerarquía, pero el usuario también necesita `USE CATALOG` y `USE SCHEMA` en los padres. Los dueños pueden otorgar y administrar; los objetos de producción deben pertenecer a grupos, no a personas.

La automatización debe correr como service principal, para que los jobs no fallen cuando alguien se va. Los secretos viven en secret scopes, aunque el acceso al almacenamiento basado en identidad es todavía mejor. Los administradores de cuenta gestionan identidades y metastores; los de workspace, un workspace; el binding limita qué workspaces ven un catálogo.

<!-- example -->

```sql
GRANT USE CATALOG ON CATALOG prod TO `analysts`;
GRANT USE SCHEMA, SELECT ON SCHEMA prod.gold TO `analysts`;
ALTER TABLE prod.gold.fct_sales OWNER TO `data-platform`;
```

#### ¿Cómo se conceden permisos en Unity Catalog?

Con SQL o desde la interfaz, a usuarios, grupos o service principals. Los privilegios se heredan hacia abajo en la jerarquía, y un usuario necesita `USE CATALOG` y `USE SCHEMA` en los niveles superiores para llegar a un objeto.

```sql
GRANT USE CATALOG ON CATALOG prod TO `analysts`;
GRANT USE SCHEMA, SELECT ON SCHEMA prod.gold TO `analysts`;
```

#### ¿Qué diferencia hay entre la propiedad y los privilegios?

El propietario de un objeto (un usuario, grupo o service principal) puede conceder privilegios sobre él y administrarlo. Los privilegios como `SELECT`, `MODIFY`, `CREATE TABLE` o `READ VOLUME` permiten acciones concretas. Hacer que un grupo sea el propietario de los objetos de producción evita depender de una sola persona.

#### ¿Qué diferencia hay entre la administración a nivel de cuenta y a nivel de workspace?

Los administradores de la cuenta gestionan las identidades (usuarios, grupos, service principals, a menudo sincronizados desde un proveedor de identidad por SCIM), los metastores, los workspaces y la configuración general. Los administradores de un workspace gestionan la configuración, las políticas de cómputo y el acceso dentro de ese workspace.

#### ¿Qué es un service principal y por qué usarlo en los jobs de producción?

Una identidad no humana para la automatización. Los jobs de producción y los despliegues de CI/CD deberían ejecutarse como service principal para no depender de la cuenta y los permisos de una persona, y para limitar el acceso a lo que necesita el pipeline.

#### ¿Cómo se administran los secretos en Databricks?

En secret scopes (respaldados por Databricks o por Azure Key Vault), leídos con `dbutils.secrets.get(scope, key)`. Los valores secretos se ocultan en la salida de los notebooks. Para los recursos de la nube, es preferible el acceso basado en identidad (instance profiles, storage credentials) a los secretos.

#### ¿Qué es la vinculación entre workspaces y catálogos?

Un ajuste que limita qué workspaces pueden acceder a un catálogo, por ejemplo para que un catálogo de producción solo sea accesible desde el workspace de producción, aunque los usuarios tengan permisos sobre él.

<!-- challenge -->

Una analista tiene `SELECT` sobre `prod.gold.fct_sales` pero recibe "permission denied". ¿Cuál es la causa probable?

<!-- solution -->

Le falta `USE CATALOG` sobre `prod` o `USE SCHEMA` sobre `prod.gold`; `SELECT` solo no basta. Otra posibilidad es que el catálogo esté vinculado solo a otros workspaces.

<!-- takeaways -->

- Los permisos se heredan, pero siempre hacen falta `USE CATALOG` y `USE SCHEMA`.
- Los grupos son dueños de producción; los service principals ejecutan los jobs.
- Prefiere el acceso por identidad a los secretos.

<!-- unit: Acceso detallado -->

<!-- goals -->

- Restringir filas y columnas sin copiar tablas.
- Comparar row filters y column masks con las vistas dinámicas.

<!-- concept -->

Los permisos a nivel de tabla suelen ser demasiado gruesos: un equipo quizá solo debe ver su país, u otro solo correos enmascarados. Los row filters y column masks son funciones asociadas a la tabla que se evalúan al consultar para el usuario actual, así hay una tabla y muchas vistas de ella. Las vistas dinámicas logran lo mismo con `current_user()` o chequeos de grupo, y eran el enfoque habitual antes.

<!-- example -->

```sql
CREATE FUNCTION gov.country_filter(country STRING)
RETURN is_account_group_member('admins')
    OR is_account_group_member(concat('analysts_', lower(country)));

ALTER TABLE prod.gold.sales SET ROW FILTER gov.country_filter ON (country);
```

#### ¿Qué son los row filters y las column masks?

Funciones asociadas a una tabla que se evalúan en el momento de la consulta. Un row filter decide qué filas puede ver un usuario (por ejemplo solo las de su país); una column mask devuelve el valor o una versión enmascarada según los grupos del usuario. Los datos quedan en una sola tabla en lugar de en muchas copias filtradas.

#### ¿Qué son las vistas dinámicas?

Vistas que usan funciones como `current_user()` o `is_account_group_member()` para filtrar filas u ocultar columnas. Eran el enfoque habitual antes de que existieran los row filters y las column masks.

#### Los analistas solo deben ver las filas de su país en una tabla compartida. ¿Cómo lo implementas?

Asocio a la tabla una función de row filter de Unity Catalog que compruebe los grupos del usuario contra la columna de país. Concedo `SELECT` a los grupos de analistas. Uso column masks para las columnas sensibles.

<!-- challenge -->

Los agentes de soporte deben ver las filas de clientes pero solo los últimos cuatro dígitos del teléfono; el equipo de fraude debe ver el número completo. Escribe la idea de la máscara.

<!-- solution -->

Una función de column mask sobre `phone`: si el usuario está en el grupo de fraude, devuelve el valor; si no, `concat('***', right(phone, 4))`. Se asocia con `ALTER TABLE ... ALTER COLUMN phone SET MASK`.

<!-- takeaways -->

- Row filters y column masks se ejecutan por usuario al consultar.
- Una tabla con políticas es mejor que muchas copias filtradas.
- Basa las políticas en grupos, no en usuarios individuales.

<!-- unit: Descubrimiento, linaje y compartición -->

<!-- goals -->

- Usar linaje, tablas del sistema, tags y comentarios para entender los datos.
- Compartir o consultar datos entre organizaciones y sistemas sin copiarlos.

<!-- concept -->

Gobernar también es saber qué existe y cómo se conecta. Unity Catalog registra automáticamente el linaje a nivel de tabla y columna, las tablas del sistema exponen uso, auditoría y facturación en SQL, y los comentarios y tags hacen los datos buscables y clasificables.

A menudo los datos deben cruzar fronteras. Delta Sharing da a otras organizaciones acceso en vivo y de solo lectura sin copias; Lakehouse Federation permite consultar bases externas en su sitio.

<!-- example -->

```sql
-- Who reads the table we want to change?
SELECT DISTINCT entity_type, entity_id, created_by
FROM system.access.table_lineage
WHERE source_table_full_name = 'prod.silver.customers'
  AND event_date >= current_date() - 30;
```

#### ¿Qué linaje registra Unity Catalog?

Linaje a nivel de tabla y de columna de las consultas ejecutadas en el cómputo de Databricks, a través de notebooks, jobs, pipelines y dashboards, visible en Catalog Explorer y consultable en las tablas del sistema. Responde a "¿qué se rompe si cambio esta columna?" y "¿de dónde sale este número?".

#### ¿Qué son las tablas del sistema?

Tablas de solo lectura del catálogo `system` con datos operativos: consumo facturado (`system.billing.usage`), logs de auditoría, linaje de tablas, ejecuciones de jobs, eventos de clusters, historial de consultas y más. Son la base de los dashboards de costos y de la auditoría.

#### ¿Para qué sirven las etiquetas y los comentarios en Unity Catalog?

Los comentarios documentan tablas y columnas (y alimentan las descripciones generadas por IA y la búsqueda); las etiquetas (pares clave-valor) clasifican objetos, por ejemplo `pii=true`, lo que puede guiar políticas, descubrimiento y auditorías.

#### ¿Cómo se descubren datos en Unity Catalog?

Con Catalog Explorer y la búsqueda, que usan nombres, comentarios, etiquetas y linaje, además de señales de popularidad como los usuarios y las consultas frecuentes. Unos buenos comentarios y etiquetas mejoran mucho el descubrimiento.

#### ¿Qué es Delta Sharing?

Un protocolo abierto para compartir datos vivos de forma segura entre organizaciones y plataformas sin copiarlos. El proveedor crea un share con tablas, vistas o volúmenes; los destinatarios lo leen desde Databricks o desde clientes de código abierto (pandas, Spark, herramientas de BI). El uso compartido entre Databricks usa las identidades de Unity Catalog.

#### ¿Qué es Lakehouse Federation?

Federación de consultas que permite a Unity Catalog registrar bases de datos externas (PostgreSQL, MySQL, SQL Server, Snowflake, Redshift, BigQuery y otras) como catálogos foráneos, para consultarlas en su lugar con gobierno y linaje, sin ingerir primero los datos.

#### ¿Cómo compartes tablas gold con una empresa socia que no usa Databricks?

Con Delta Sharing abierto: creo un share con las tablas, creo un destinatario con una credencial basada en token, y el socio lo lee desde pandas, Spark o una herramienta de BI. El acceso se puede revocar en cualquier momento y queda auditado.

<!-- challenge -->

Planeas renombrar una columna en `silver.customers`. ¿Cómo averiguas qué se rompe y a quién avisar?

<!-- solution -->

Revisa el linaje por columna en Catalog Explorer (o `system.access.column_lineage`) para tablas, jobs, dashboards y notebooks posteriores, y el historial de consultas o la auditoría para lectores directos. Avisa a los dueños y considera mantener el nombre viejo en una vista durante la transición.

<!-- takeaways -->

- El linaje responde "¿qué se rompe si cambio esto?".
- Las tablas del sistema convierten uso, auditoría y facturación en SQL.
- Delta Sharing comparte sin copias; Federation consulta sin ingerir.

<!-- stage: Operar con eficiencia -->

### Spark y rendimiento en Databricks

<!-- unit: Planes y shuffles -->

<!-- goals -->

- Leer un plan de consulta e identificar los pasos costosos.
- Explicar shuffles, AQE y el número de particiones.

<!-- concept -->

Spark convierte tu código en un plan de stages separados por shuffles, cuando los datos viajan por la red para un join, `groupBy` o `distinct`. Los pasos narrow son baratos; los shuffles dominan el costo. Por eso el trabajo de rendimiento empieza leyendo el plan de abajo hacia arriba: qué se escanea, qué se empuja a la fuente, dónde están los exchanges y qué estrategia de join se usa.

Adaptive Query Execution ajusta el plan en ejecución, fusionando particiones pequeñas y cambiando joins. Aun así eliges un número sensato de particiones y conoces la diferencia entre `repartition` y `coalesce`.

<!-- example -->

```text
== Physical Plan (simplified, read bottom-up) ==
HashAggregate(keys=[country])
+- Exchange hashpartitioning(country, 200)          ← shuffle
   +- HashAggregate(keys=[country])                 ← partial aggregation
      +- Scan delta silver.orders
         PushedFilters: [order_date >= 2026-10-01]   ← pruning works
```

#### ¿Qué diferencia hay entre transformaciones narrow y wide?

Las transformaciones narrow (`filter`, `select`, `withColumn`) calculan cada partición de salida a partir de una partición de entrada, sin mover datos. Las wide (`groupBy`, `join`, `distinct`, `orderBy`) necesitan un shuffle por la red. Optimizar el rendimiento consiste sobre todo en controlar los shuffles.

#### ¿Cómo se lee un plan de consulta de Spark?

Con `df.explain(mode="formatted")` o en la pestaña SQL de la Spark UI. Se lee de abajo hacia arriba: lecturas (revisa los filtros empujados y los archivos descartados), exchanges (shuffles), estrategias de join (broadcast, sort-merge) y agregaciones. El perfil de consulta de Databricks SQL muestra lo mismo con los tiempos.

#### ¿Qué es la Adaptive Query Execution?

Una función de Spark, activada por defecto, que vuelve a optimizar una consulta entre stages con estadísticas de ejecución: fusiona las particiones pequeñas del shuffle, cambia los joins sort-merge por joins broadcast cuando un lado resulta pequeño y divide las particiones con skew.

#### ¿Cómo se elige el número de particiones del shuffle?

`spark.sql.shuffle.partitions` vale 200 por defecto. Con AQE, define un número generoso (o `auto` en Databricks) y deja que AQE las fusione. Apunta a particiones de unos 100–200 MB después del shuffle; muy pocas causan spill, demasiadas causan sobrecarga.

#### ¿Qué diferencia hay entre `repartition` y `coalesce`?

`repartition(n)` hace un shuffle completo y puede aumentar o reducir el número de particiones, opcionalmente por columnas. `coalesce(n)` solo fusiona particiones sin shuffle completo, así que es más barato pero solo puede reducirlas y puede dejarlas desiguales. `coalesce(1)` hace pasar todo por una sola tarea.

<!-- challenge -->

Un job termina con `.coalesce(1).write...` para producir un solo archivo, y el último stage tarda 25 minutos en un cluster de 40 nodos. ¿Por qué y qué haces?

<!-- solution -->

`coalesce(1)` canaliza todo el cálculo final por una tarea, así que 39 nodos quedan ociosos. Escribe normalmente y deja que los consumidores lean la tabla, o si de verdad necesitas un archivo, escribe un resultado pequeño agregado o usa `repartition(1)` solo después del trabajo pesado para que los stages previos sigan en paralelo.

<!-- takeaways -->

- Los shuffles son el costo principal; busca los exchanges en el plan.
- AQE ajusta particiones y joins en ejecución.
- `coalesce` fusiona sin shuffle pero puede matar el paralelismo.

<!-- unit: Joins, skew y spill -->

<!-- goals -->

- Elegir broadcast joins y corregir el skew.
- Reconocer el spill y sus remedios.

<!-- concept -->

Los joins son donde más duelen los jobs lentos. Si un lado es pequeño, hacerle broadcast evita mover el lado grande. Si las claves están mal repartidas, unas pocas tareas reciben casi todos los datos (skew) y el stage las espera. Si los datos de una tarea no caben en memoria, Spark los derrama a disco (spill).

Los tres aparecen en la Spark UI: mira la estrategia de join en el plan, compara la mediana y el máximo de duración de tareas y revisa las columnas de spill.

<!-- example -->

```python
from pyspark.sql.functions import broadcast
facts.join(broadcast(dim_store), "store_id")      # 50 MB dimension: no shuffle of facts
```
Resumen de stage que indica skew: tarea mediana 8 s, tarea máxima 14 min.

#### ¿Qué es un broadcast join y cuándo ayuda?

Spark envía una copia de la tabla pequeña a cada executor, de modo que la tabla grande se une sin hacer shuffle. Ayuda cuando un lado es lo bastante pequeño (decenas de MB por defecto, más con hints). Hacer broadcast de una tabla demasiado grande provoca errores de memoria en el driver o en los executors.

#### ¿Qué es el data skew y cómo se corrige?

Algunas claves tienen muchas más filas que otras, así que unas pocas tareas tardan mucho más que el resto. Soluciones: dejar que AQE divida las particiones con skew, hacer broadcast del lado pequeño, filtrar o tratar aparte las claves calientes (a menudo los nulos) o aplicar salting a la clave para repartirla entre particiones.

#### ¿Qué es el spill y por qué es lento?

Cuando los datos de una tarea no caben en la memoria de ejecución, Spark los escribe en el disco local y los vuelve a leer. Aparece en la Spark UI como spill (memory) y spill (disk). Se corrige con más particiones y más pequeñas, workers más grandes u optimizados para memoria, o menos datos por tarea.

#### Un join entre una tabla de hechos de 2 TB y una dimensión de 50 MB es lento. ¿Qué revisas?

Si se hace broadcast (revisa el plan; añade un hint de broadcast o sube el umbral), si la lectura de los hechos descarta archivos (filtros sobre columnas agrupadas), el skew en la clave del join y el spill. Una dimensión de 50 MB debería ir casi siempre en broadcast.

#### ¿Cómo investigarías un job que de repente se volvió más lento?

Comparando la ejecución lenta con una normal: tamaños de entrada, número de archivos (archivos pequeños, falta de `OPTIMIZE`), cambios de plan (un broadcast que pasó a sort-merge join), skew en un stage, spill, tamaño del cluster o pérdida de instancias spot, y cambios en el código o en los datos desde la última ejecución buena.

<!-- challenge -->

Un join por `customer_id` tiene una tarea corriendo 20 minutos mientras las demás terminan en segundos. La clave con más filas es `NULL`. ¿Qué haces?

<!-- solution -->

Las filas con clave nula nunca pueden coincidir en un inner join, así que fíltralas antes del join (o trátalas aparte en un outer join). Si quedan otras claves calientes, apóyate en el manejo de skew de AQE o aplica salting.

<!-- takeaways -->

- Haz broadcast de las dimensiones pequeñas; confírmalo en el plan.
- El skew se ve como una cola larga en la duración de tareas; los nulos son una clave caliente común.
- Spill significa demasiados datos por tarea: más particiones o más memoria.

<!-- unit: Escribir código eficiente -->

<!-- goals -->

- Evitar patrones de código que vuelven lento a Spark.
- Usar caché solo donde ayuda.

<!-- concept -->

Parte de la lentitud viene del código, no de los datos. Las UDF de Python mueven cada fila entre la JVM y Python y le ocultan la lógica al optimizador; las funciones nativas son mucho más rápidas. Construir un plan con `withColumn` en un bucle ralentiza el análisis, y llamar `count()` tras cada paso recalcula todo cada vez.

La caché no es un arreglo general: en Databricks el disk cache ya acelera las lecturas repetidas, serverless no soporta `cache()` y la reutilización entre jobs pertenece a una tabla.

<!-- example -->

```python
# Slow: Python UDF, row by row
@udf("string")
def clean(s): return s.strip().upper()
df.withColumn("code", clean("code"))

# Fast: built-in functions, optimized and Photon-friendly
from pyspark.sql import functions as F
df.withColumn("code", F.upper(F.trim("code")))
```

#### ¿Por qué las UDF de Python son lentas y qué alternativas hay?

Cada fila se serializa entre la JVM y un worker de Python, y el optimizador no puede ver dentro de la función. Usa primero las funciones integradas, luego las UDF de pandas (vectorizadas) con Arrow, o UDF SQL. Photon tampoco puede acelerar las UDF de Python.

#### ¿Por qué es un problema `withColumn` dentro de un bucle?

Cada llamada añade una proyección al plan lógico, y analizar un plan muy profundo se vuelve lento (puede tardar minutos antes de procesar ningún dato). Usa un solo `select` o `withColumns` con un diccionario.

#### ¿Por qué un `count()` antes de cada paso ralentiza un job?

Cada acción dispara la ejecución completa del plan hasta ese punto. Contar para los logs después de cada transformación recalcula los datos una y otra vez. Toma las métricas del commit de Delta (`numOutputRows` en el historial) o calcúlalas una sola vez.

#### ¿Conviene usar `cache()` en Databricks?

Con moderación. El caché ayuda cuando el mismo DataFrame se reutiliza varias veces en una sesión interactiva, pero consume memoria y no está disponible en serverless. El disk cache (caché automático en SSD de los archivos Parquet remotos en algunos tipos de instancia) suele dar el beneficio sin cambiar el código. Para reutilizar entre jobs, escribe una tabla.

#### ¿Qué es el disk cache?

Un caché automático, antes llamado Delta cache, que guarda copias de los archivos Parquet y Delta remotos en los SSD locales de los workers, para que las lecturas repetidas de los mismos datos sean más rápidas. Se administra de forma transparente.

<!-- challenge -->

Un notebook renombra 300 columnas con un bucle `for` de `withColumnRenamed` y tarda 6 minutos antes de que arranque cualquier job. Corrígelo.

<!-- solution -->

Construye todas las expresiones a la vez y aplica un solo `select`: `df.select([F.col(c).alias(new_names[c]) for c in df.columns])`, o usa `withColumnsRenamed` con un diccionario. El plan queda poco profundo y el análisis tarda segundos.

<!-- takeaways -->

- Prefiere funciones nativas a las UDF de Python.
- Construye transformaciones anchas en un `select`, no en bucles.
- Usa caché rara vez; escribe tablas para reutilizar entre jobs.

<!-- unit: Pruning, estadísticas y costo de los jobs -->

<!-- goals -->

- Hacer que las consultas lean menos datos con pruning y estadísticas.
- Reducir el costo de un job pesado.

<!-- concept -->

Los datos más baratos son los que nunca lees. El pruning de particiones salta directorios y el de archivos salta archivos usando las estadísticas de Delta; ambos dependen de filtros que coincidan con la organización de la tabla. Las estadísticas de columna ayudan al optimizador a elegir estrategias de join, y la optimización predictiva mantiene organización y estadísticas en tablas gestionadas.

El costo se deriva de eso: procesamiento incremental en vez de recálculos completos, lecturas podadas, el tipo y tamaño de cómputo correctos y monitoreo con las tablas de facturación.

<!-- example -->

```sql
-- Prunes files: filter on the clustering column
SELECT sum(amount) FROM silver.events WHERE event_date = '2026-10-15';
-- Can't prune: function applied to the column
SELECT sum(amount) FROM silver.events WHERE date_format(event_date, 'yyyy-MM') = '2026-10';
```

#### ¿En qué se diferencia el descarte de archivos del descarte de particiones?

El descarte de particiones (partition pruning) salta directorios enteros según las columnas de partición. El descarte de archivos (data skipping) salta archivos individuales usando las estadísticas mínimo/máximo del log de Delta, así que funciona con cualquier columna con estadísticas y se beneficia del clustering.

#### ¿Qué son las estadísticas de columnas y por qué calcularlas?

`ANALYZE TABLE … COMPUTE STATISTICS FOR ALL COLUMNS` guarda el número de filas y las estadísticas de las columnas que usa el optimizador basado en costos para elegir el orden y la estrategia de los joins. La optimización predictiva puede mantenerlas automáticamente.

#### ¿Qué es la optimización predictiva?

Una función de Unity Catalog que ejecuta automáticamente `OPTIMIZE`, `VACUUM` y la recolección de estadísticas en las tablas administradas cuando predice un beneficio, para que no tengas que programar jobs de mantenimiento.

#### ¿Qué es `replaceWhere`?

Una opción de escritura que reemplaza de forma atómica solo las filas que cumplen un predicado, normalmente un rango de fechas, sin tocar el resto de la tabla. Hace idempotente el reprocesamiento de un periodo.

```python
(df.write.format("delta").mode("overwrite")
   .option("replaceWhere", "event_date = '2026-10-15'")
   .saveAsTable("silver.events"))
```

#### ¿Cómo se reduce el costo de un job pesado de Databricks?

Usando cómputo de jobs o serverless en lugar de clusters all-purpose, activando Photon donde compense, procesando de forma incremental en lugar de recalcularlo todo, reduciendo las lecturas con clustering y filtros, dimensionando y autoescalando bien los clusters, usando workers spot, evitando shuffles innecesarios y UDF de Python, y monitoreando con `system.billing.usage`.

<!-- challenge -->

Un job diario recalcula tres años de ventas en una tabla gold cada noche, aunque solo cambian los datos de ayer. Esboza un diseño más barato.

<!-- solution -->

Procesar solo el rango cambiado: leer las filas nuevas de silver (CDF o un filtro de fecha), recalcular los días afectados y escribir con `replaceWhere` sobre esas fechas (o un `MERGE`). Correrlo en cómputo de jobs o serverless y mantener la tabla gold agrupada por fecha.

<!-- takeaways -->

- Los filtros deben coincidir con la organización, sin funciones sobre la columna, para podar.
- La optimización predictiva mantiene las tablas gestionadas por ti.
- El procesamiento incremental es la mayor palanca de costo.

### Seguridad, costos y operación

<!-- unit: Seguridad y auditoría -->

<!-- goals -->

- Describir el acceso seguro al almacenamiento cloud y las opciones de red.
- Averiguar quién accedió a qué.

<!-- concept -->

La seguridad en Databricks se apoya en identidades, no en claves. El acceso al almacenamiento pasa por roles IAM envueltos en storage credentials, nunca por claves de acceso en el código. La red puede cerrarse con tu propia VPC, conectividad privada, listas de IP y políticas de salida para serverless.

Todo queda registrado: los logs de auditoría en `system.access.audit`, el historial de consultas y el linaje responden quién hizo qué y cuándo.

<!-- example -->

```sql
SELECT event_time, user_identity.email, action_name, request_params.full_name_arg
FROM system.access.audit
WHERE service_name = 'unityCatalog'
  AND request_params.full_name_arg = 'prod.silver.customers'
  AND event_date >= current_date() - 7;
```

#### ¿Cómo accede Databricks de forma segura a los datos en AWS S3?

Mediante roles IAM: en Unity Catalog, una storage credential encapsula un rol IAM que confía en Databricks, y las external locations dan acceso a las rutas. Las instalaciones antiguas usaban instance profiles asociados a los clusters. Hay que evitar las claves de acceso en el código.

#### ¿Qué opciones de seguridad de red existen?

Desplegar el cómputo clásico en tu propia VPC/VNet, conectividad privada entre el plano de control y el de cómputo (PrivateLink, Private Link), listas de IP permitidas, nodos sin IP pública, políticas de red serverless para controlar la salida y claves administradas por el cliente para el cifrado.

#### ¿Cómo se audita quién accedió a qué?

Con los logs de auditoría (disponibles en la tabla `system.access.audit`), el linaje de Unity Catalog y el historial de consultas. Registran los inicios de sesión, los cambios de permisos, el acceso a los datos y las acciones sobre los jobs.

<!-- challenge -->

Una revisión de seguridad encuentra una clave de acceso de AWS escrita en un notebook. ¿Con qué la reemplazas y qué más haces?

<!-- solution -->

Reemplazarla por una storage credential de Unity Catalog (rol IAM) y una external location o volumen para la ruta, para no necesitar claves. Rotar (desactivar) la clave expuesta, revisar la auditoría y CloudTrail buscando abusos, y escanear otros notebooks y repositorios.

<!-- takeaways -->

- Accede al almacenamiento con roles y storage credentials, nunca con claves en el código.
- La red privada y los controles de salida limitan la exposición.
- Los logs de auditoría viven en tablas del sistema y se pueden consultar.

<!-- unit: Vigilar la factura -->

<!-- goals -->

- Desglosar el gasto de Databricks y encontrar sus causas.
- Atribuir costos a equipos con tags y tablas del sistema.

<!-- concept -->

El gasto se ve en `system.billing.usage`: DBU por SKU, workspace, job, warehouse y tag, que se unen con los precios de lista. Los tags en el cómputo permiten atribuir el gasto a equipos. Los culpables suelen ser siempre los mismos: clusters que nunca se apagan, producción en cómputo all-purpose, recálculos completos y reintentos descontrolados.

<!-- example -->

```sql
SELECT usage_metadata.job_id, sku_name, sum(usage_quantity) AS dbus
FROM system.billing.usage
WHERE usage_date >= date_trunc('month', current_date())
GROUP BY ALL ORDER BY dbus DESC LIMIT 10;
```

#### ¿Cómo se monitorea y controla el gasto en Databricks?

Etiquetando clusters, jobs y warehouses con centros de costo, consultando `system.billing.usage` unido a los precios de lista, definiendo presupuestos y alertas, imponiendo políticas de cluster (tipos de instancia, autoterminación, máximo de workers), usando serverless o cómputo de jobs en producción y revisando con regularidad los jobs más caros.

#### La factura mensual de Databricks se duplicó. ¿Cómo lo investigas?

Consulto `system.billing.usage` por SKU, workspace, job, warehouse y etiqueta, y comparo los meses. Busco clusters all-purpose sin autoterminación, jobs que pasaron a cómputo all-purpose, warehouses que nunca se detienen, full refreshes, cargas serverless nuevas y reintentos descontrolados.

<!-- challenge -->

Escribe las dos primeras consultas que harías cuando finanzas pregunta por qué el mes pasado costó un 40 % más.

<!-- solution -->

Primero, DBU (o costo) por SKU este mes contra el anterior, para ver qué producto creció. Segundo, dentro del SKU que creció, los jobs, warehouses o clusters con más uso, comparando ambos meses, para encontrar la carga que cambió.

<!-- takeaways -->

- `system.billing.usage` es la fuente de verdad del gasto.
- Los tags permiten atribuir costos a equipos y proyectos.
- Compara primero por SKU, luego por carga.

<!-- unit: Despliegue con bundles y CI/CD -->

<!-- goals -->

- Describir un proyecto de Databricks como código con Declarative Automation Bundles.
- Montar pruebas y despliegue mediante CI/CD.

<!-- concept -->

Los pipelines de producción se despliegan, no se arman a clics. Los Declarative Automation Bundles (antes Databricks Asset Bundles) describen jobs, pipelines y su configuración en YAML junto al código, con un target por entorno. Los targets de desarrollo anteponen el usuario a los recursos y pausan los calendarios; los de producción corren como service principal.

Un pipeline de CI valida el bundle, corre tests unitarios sobre funciones de transformación puras, despliega a staging para pruebas de integración y promueve a producción tras una aprobación.

<!-- example -->

```text
pull request ──► lint + pytest (local Spark) ──► bundle validate
merge to main ──► deploy -t staging ──► integration run ──► approval ──► deploy -t prod
```

#### ¿Qué son los Declarative Automation Bundles (antes Databricks Asset Bundles)?

Una forma de describir los recursos de Databricks (jobs, pipelines, dashboards, modelos, clusters, permisos) en YAML junto al código en Git, con targets para cada entorno. La CLI los valida, muestra los cambios previstos (`databricks bundle plan`), los despliega y los ejecuta, lo que permite desplegar los proyectos de Databricks con CI/CD. El cambio de nombre de 2026 dejó igual el archivo `databricks.yml` y los comandos `databricks bundle`, y la sigla sigue siendo DABs.

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

<!-- challenge -->

Dos desarrolladores despliegan el mismo bundle en el workspace de desarrollo y se sobrescriben el job. ¿Qué falta?

<!-- solution -->

El target de desarrollo debe usar `mode: development`, que antepone el nombre de cada usuario a los recursos y despliega en una carpeta por usuario, así sus copias no chocan.

<!-- takeaways -->

- Los bundles mantienen jobs y pipelines como código, por entorno.
- El modo de desarrollo aísla el despliegue de cada desarrollador.
- Prueba funciones puras localmente; despliega a staging antes de producción.

<!-- stage: Servir y aplicar -->

### Databricks SQL y analítica

<!-- unit: Warehousing y BI -->

<!-- goals -->

- Explicar cómo consultan las herramientas de BI a Databricks y qué las acelera.
- Elegir entre vistas, vistas materializadas y federación.

<!-- concept -->

Databricks SQL convierte el lakehouse en un warehouse para analistas: los SQL warehouses ejecutan consultas del editor, dashboards y herramientas de BI por JDBC/ODBC, con los permisos de Unity Catalog de cada usuario. Las consultas repetidas aprovechan la caché de resultados.

Cómo expones los datos afecta el costo: una vista vuelve a ejecutar su consulta cada vez, una vista materializada guarda resultados y se refresca, y la federación consulta una base externa en su sitio, bien para explorar pero lenta para uso intensivo.

<!-- example -->

```sql
CREATE MATERIALIZED VIEW gold.mv_sales_by_month
SCHEDULE CRON '0 0 6 * * ?'
AS SELECT date_trunc('month', order_date) AS month, region, sum(amount) AS sales
FROM silver.orders GROUP BY ALL;
```

#### ¿Qué es Databricks SQL?

La parte de data warehousing SQL de la plataforma: SQL warehouses, un editor SQL, historial y perfiles de consultas, alertas, dashboards y conectores para herramientas de BI (Power BI, Tableau, Looker) por JDBC/ODBC.

#### ¿Cómo se conectan las herramientas de BI a Databricks?

Con drivers JDBC/ODBC o conectores nativos (Power BI, Tableau, Looker, Excel) que apuntan a un SQL warehouse, autenticándose con OAuth o con tokens. Unity Catalog aplica los permisos de la identidad que se conecta.

#### ¿Qué es el caché de resultados de Databricks SQL?

Un caché de resultados de consultas en los SQL warehouses: cuando la misma consulta se ejecuta de nuevo y las tablas no han cambiado, el resultado se devuelve sin recalcularlo.

#### ¿Qué diferencia hay entre una vista, una vista temporal y una vista materializada?

Una vista guarda solo la consulta y la ejecuta en cada lectura. Una vista temporal solo existe en la sesión actual. Una vista materializada guarda resultados precalculados y hay que refrescarla.

#### ¿Qué es una vista materializada en Databricks SQL?

Una vista cuyos resultados se guardan y se refrescan (de forma programada o bajo demanda, incremental cuando se puede). Acelera las agregaciones costosas de los dashboards. Se crea con `CREATE MATERIALIZED VIEW` y corre sobre pipelines serverless.

#### ¿Para qué sirve la federación de consultas en analítica?

Para unir tablas de Databricks con tablas que todavía están en una base de datos operativa u otro warehouse, para explorar o migrar, sin construir primero una ingesta. Para un uso intensivo y repetido, ingerir los datos es más rápido y más barato.

<!-- challenge -->

Un reporte de Power BI ejecuta una agregación pesada sobre 2.000 millones de filas cada vez que alguien lo abre; los datos cambian una vez al día. ¿Qué cambias?

<!-- solution -->

Precalcular la agregación como vista materializada (o tabla gold) refrescada tras la carga diaria y apuntar el reporte a ella. Las consultas leen entonces una tabla pequeña y la caché de resultados ayuda en aperturas repetidas.

<!-- takeaways -->

- Las herramientas de BI se conectan a SQL warehouses con permisos de Unity Catalog por usuario.
- Las vistas materializadas precalculan agregaciones costosas.
- La federación es para explorar; ingiere para uso intensivo y repetido.

<!-- unit: Dashboards, métricas y aplicaciones -->

<!-- goals -->

- Describir dashboards, Genie, metric views y alertas.
- Saber cuándo encajan Databricks Apps y Lakebase.

<!-- concept -->

Sobre los warehouses, Databricks ofrece dashboards AI/BI, Genie para preguntas en lenguaje natural y alertas SQL que avisan ante condiciones. Las metric views definen medidas una vez para que todas las herramientas calculen "ingresos" igual.

Para aplicaciones interactivas, Databricks Apps aloja apps web dentro del workspace y Lakebase ofrece una base compatible con Postgres para necesidades transaccionales de baja latencia que las tablas analíticas no atienden bien.

<!-- example -->

Una alerta de calidad: programa esta consulta cada hora y avisa cuando `bad_rows > 0`.
```sql
SELECT count(*) AS bad_rows FROM silver.orders
WHERE amount < 0 AND order_date = current_date();
```

#### ¿Qué son los dashboards AI/BI y Genie?

Los dashboards AI/BI son los dashboards actuales de Databricks, construidos sobre SQL warehouses con ayuda de IA para crearlos. Genie es una interfaz en lenguaje natural donde los usuarios de negocio hacen preguntas sobre tablas seleccionadas y reciben respuestas respaldadas por SQL.

#### ¿Qué es una metric view?

Un objeto de Unity Catalog que define las métricas de negocio (medidas y dimensiones) una sola vez en YAML sobre una tabla, para que los dashboards, Genie y los usuarios de SQL las calculen de forma coherente.

#### ¿Qué son las alertas SQL?

Consultas programadas que comparan un resultado con un umbral y notifican (correo, Slack, webhook) cuando se cumple la condición, por ejemplo cuando un control de calidad de datos devuelve filas.

#### ¿Qué son las Databricks Apps?

Una forma de construir y alojar aplicaciones de datos e IA (Streamlit, Dash, Gradio, Flask y otras) directamente en el workspace, con autenticación y acceso a datos gobernados mediante Unity Catalog.

#### ¿Qué es Lakebase?

Una base de datos operativa administrada compatible con PostgreSQL dentro de Databricks, basada en Postgres serverless, pensada para cargas transaccionales de baja latencia (aplicaciones, servicio de features) que se sincronizan con las tablas del lakehouse.

<!-- challenge -->

Tres dashboards muestran tres cifras distintas de "clientes activos". ¿Cómo lo arreglas para siempre?

<!-- solution -->

Acordar una definición con los responsables de negocio, definirla una vez como metric view (o tabla gold documentada) y reconstruir los dashboards sobre ella, para que la definición no pueda divergir por dashboard.

<!-- takeaways -->

- Define las métricas de negocio una vez, en una metric view.
- Las alertas SQL convierten consultas en monitoreo.
- Apps y Lakebase atienden necesidades interactivas y transaccionales.

### Machine learning e IA

<!-- unit: Modelos y features -->

<!-- goals -->

- Describir el ciclo de vida de ML en Databricks con MLflow y Unity Catalog.
- Explicar por qué las tablas de features mantienen consistentes entrenamiento e inferencia.

<!-- concept -->

Un modelo es tan confiable como su historia. MLflow registra cada ejecución de entrenamiento (parámetros, métricas, artefactos) para comparar ejecuciones y empaquetar la mejor. Registrarlo en Unity Catalog lo convierte en un objeto gobernado con versiones, alias como `champion`, permisos y linaje hasta las tablas con que se entrenó.

Las features necesitan la misma disciplina. Una tabla de features con clave por entidad y tiempo se calcula una vez y se reutiliza, así los sets de entrenamiento y las predicciones en vivo leen las mismas definiciones en vez de dos copias de la lógica.

<!-- example -->

```python
import mlflow
mlflow.set_registry_uri("databricks-uc")
with mlflow.start_run():
    model = train(features_df)
    mlflow.sklearn.log_model(model, "model", registered_model_name="ml.churn.churn_model")
```

#### ¿Qué es MLflow?

Una plataforma de código abierto, creada por Databricks, para el ciclo de vida del ML: seguimiento de experimentos (parámetros, métricas, artefactos), empaquetado de modelos, un registro de modelos con versiones y alias, evaluación, y trazas para aplicaciones de IA generativa. En Databricks es un servicio administrado e integrado con Unity Catalog.

#### ¿Qué significa registrar un modelo en Unity Catalog?

Los modelos se guardan como objetos de Unity Catalog (`catalogo.esquema.modelo`) con versiones y alias como `champion`, gobernados con los mismos permisos y el mismo linaje que las tablas, y utilizables desde varios workspaces.

#### ¿Qué es una tabla de features?

Una tabla Delta con clave primaria que sirve para guardar features de ML en Unity Catalog. Los conjuntos de entrenamiento se construyen uniendo tablas de features con las etiquetas (con corrección point-in-time para las series temporales), y las mismas features se pueden servir en línea para la inferencia.

<!-- challenge -->

Un modelo entrenado el trimestre pasado rinde peor en producción que en pruebas. Sus features se calculan con código separado para entrenamiento y servicio. ¿Qué cambias?

<!-- solution -->

Pasar las features a tablas de features construidas una vez desde silver, usar joins point-in-time para los sets de entrenamiento y servir las mismas features en línea, para que entrenamiento e inferencia no diverjan. Luego reentrenar y comparar versiones en MLflow.

<!-- takeaways -->

- MLflow registra ejecuciones; Unity Catalog versiona y gobierna los modelos.
- Alias como `champion` desacoplan a los consumidores de los números de versión.
- Las tablas de features mantienen entrenamiento y servicio sobre una definición.

<!-- unit: Serving e IA en SQL -->

<!-- goals -->

- Elegir entre Model Serving, Vector Search y AI functions.
- Asociar cada opción a cargas en línea, de recuperación o batch.

<!-- concept -->

Con un modelo registrado, la pregunta es cómo se encuentra con los datos. Las aplicaciones en línea necesitan respuestas de baja latencia, así que el modelo vive detrás de un endpoint REST. Las apps con recuperación aumentada deben encontrar primero los documentos relevantes, así que un índice sobre una tabla Delta mantiene los embeddings sincronizados con la fuente. El enriquecimiento batch no necesita ninguno: los analistas llaman un modelo dentro de una consulta SQL y el warehouse se encarga de la escala. Los tres siguen bajo los permisos de Unity Catalog.

<!-- example -->

```sql
SELECT ticket_id,
       ai_classify(body, ARRAY('billing', 'bug', 'feature request')) AS category
FROM silver.support_tickets
WHERE created_date = current_date();
```

#### ¿Qué es Model Serving?

Un servicio serverless que expone modelos (modelos MLflow propios, modelos fundacionales, modelos externos) como endpoints REST con autoescalado, monitoreo y control de acceso.

#### ¿Qué es Vector Search?

Una base de datos vectorial administrada que indexa embeddings de una tabla Delta y mantiene el índice sincronizado, usada para la generación aumentada por recuperación (RAG) y la búsqueda por similitud.

#### ¿Qué son las funciones de IA en Databricks SQL?

Funciones SQL como `ai_query`, `ai_classify`, `ai_extract`, `ai_summarize` y `ai_translate` que llaman a modelos desde SQL, para enriquecer tablas con la salida de un LLM en batch.

<!-- challenge -->

Soporte quiere que cada ticket nuevo se etiquete por categoría cada mañana y un chatbot que responda con los artículos del centro de ayuda. ¿Qué opción encaja con cada necesidad?

<!-- solution -->

El etiquetado es trabajo batch: una consulta SQL programada con `ai_classify` sobre los tickets nuevos. El chatbot necesita recuperación: un índice de Vector Search sobre la tabla de artículos, con el LLM detrás de un endpoint de Model Serving que usa los fragmentos recuperados como contexto.

<!-- takeaways -->

- Model Serving atiende peticiones en línea mediante endpoints REST.
- Vector Search indexa tablas Delta para recuperación.
- Las AI functions llevan los modelos al SQL batch.

<!-- stage: Integrarlo todo -->

### Escenarios

<!-- unit: Diseñar un pipeline de punta a punta -->

<!-- goals -->

- Combinar ingesta, capas medallion, jobs y gobierno en un diseño.
- Explicar cada decisión de diseño en una respuesta de entrevista.

<!-- concept -->

Las preguntas de diseño prueban si sabes conectar las secciones, no recitarlas. Una buena respuesta sigue a los datos: cómo llegan los archivos, cómo se vuelven una tabla confiable, cómo se refrescan, quién puede leerlos y cómo llega el código a producción. Nombra una herramienta por paso y di por qué encaja, como lecturas incrementales para carpetas que crecen o `MERGE` para correcciones tardías. Cierra con el manejo de fallos: reintentos, alertas y qué hace una re-ejecución.

<!-- example -->

```text
S3 landing ─► Auto Loader ─► bronze (raw + _metadata)
                                │ dedupe, validate, MERGE
                                ▼
                             silver ─► gold aggregates ─► dashboard
 job: daily trigger, retries, alerts · UC grants · bundle deploys dev → prod
```

#### Diseña un pipeline que ingiera archivos CSV diarios desde S3 hasta una tabla de reportes.

Deja los archivos en S3, léelos con Auto Loader (trigger `availableNow`) hacia una tabla Delta bronze con un esquema declarado y columnas de `_metadata`, limpia, deduplica y valida hacia silver con `MERGE`, construye agregados gold o un esquema en estrella, prográmalo como job con reintentos y alertas, gobiérnalo con Unity Catalog y despliégalo con un bundle.

<!-- challenge -->

El mismo pipeline ahora debe aceptar archivos corregidos de días pasados. ¿Qué cambia en tu diseño?

<!-- solution -->

Auto Loader sigue tomando los archivos nuevos una sola vez. Silver usa `MERGE` sobre la clave de negocio y gana el `updated_at` más reciente, así las correcciones reemplazan filas viejas en vez de duplicarlas. Los agregados gold de las fechas afectadas se recalculan, por ejemplo con `replaceWhere` sobre esas fechas.

<!-- takeaways -->

- Sigue a los datos desde el aterrizaje hasta los consumidores, una herramienta por paso.
- Haz cada capa idempotente para que re-ejecuciones y correcciones sean seguras.
- Termina con calendario, monitoreo, gobierno y despliegue.

<!-- unit: Migrar a Databricks -->

<!-- goals -->

- Planear la migración desde un stack Hive on-premises.
- Validar resultados antes de cambiar a los consumidores.

<!-- concept -->

Las migraciones fallan menos por la tecnología que por la secuencia. Empieza con un inventario, porque las dependencias ocultas (un script de cron, un reporte que lee una tabla cruda) rompen los cortes. Datos y código se mueven por separado: las tablas se convierten a Delta, las consultas se portan a Spark SQL y se reemplazan los planificadores. Correr lo viejo y lo nuevo en paralelo y comparar salidas genera la confianza para cambiar a los consumidores y retirar el sistema viejo.

<!-- example -->

```sql
-- Parquet table copied to cloud storage: convert in place
CONVERT TO DELTA parquet.`s3://lake/legacy/orders` PARTITIONED BY (order_date DATE);
-- then compare with the legacy output
SELECT count(*), sum(amount) FROM main.sales.orders WHERE order_date = '2026-09-30';
```

#### ¿Cómo migrarías un pipeline on-premises basado en Hive a Databricks?

Inventariando los jobs, las tablas y las dependencias; copiando los datos al almacenamiento en la nube y convirtiéndolos a Delta (`CONVERT TO DELTA` para Parquet); pasando el HiveQL a Spark SQL (casi todo es compatible); reemplazando Oozie o cron por Lakeflow Jobs o Airflow; registrando las tablas en Unity Catalog; y validando los resultados lado a lado (número de filas, checksums, agregados) antes de cambiar a los consumidores.

<!-- challenge -->

Los conteos de filas coinciden entre el pipeline viejo y el nuevo, pero los totales de ingresos difieren un 0,3 %. ¿Cómo encuentras la causa?

<!-- solution -->

Compara agregados por día y por clave para ubicar la diferencia y luego compara las filas afectadas. Las causas habituales son decimal contra double, el manejo de zonas horarias en timestamps, los NULL en joins y duplicados resueltos de forma distinta. Corrige la regla, re-ejecuta y compara de nuevo.

<!-- takeaways -->

- Inventaría jobs, tablas y consumidores antes de mover nada.
- Convierte los datos a Delta, porta HiveQL y reemplaza el planificador.
- Corre en paralelo y compara resultados antes del corte.
