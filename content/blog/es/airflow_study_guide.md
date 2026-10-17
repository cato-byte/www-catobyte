## Guía de estudio de Apache Airflow

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de Apache Airflow: unas 200 preguntas](../../images/airflow_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre Apache Airflow, desde los DAG y los operadores hasta la programación, los sensores, los assets, los executors, las pruebas, el despliegue y la resolución de problemas. Las respuestas siguen Airflow 3 y señalan lo que cambió respecto a Airflow 2, ya que muchas empresas todavía usan ambas versiones. Abre una pregunta para ver su respuesta, o usa el filtro para buscar en toda la guía.

<!-- QA -->

### Fundamentos

#### ¿Qué es Apache Airflow?

Una plataforma de código abierto para escribir, programar y monitorear flujos de trabajo como código. Los flujos son DAG de tareas definidos en Python; Airflow los ejecuta según una programación o ante eventos, en el orden de sus dependencias, con reintentos, logs, alertas y una interfaz web. Nació en Airbnb en 2014 y es un proyecto de primer nivel de Apache.

#### ¿Para qué sirve Airflow y para qué no?

Sirve para orquestar flujos batch: ETL/ELT, lanzar jobs en otros sistemas (Spark, dbt, Databricks, Snowflake, Glue), pipelines de ML, reportes y mantenimiento. No es un motor de procesamiento de datos (el cálculo pesado debe ocurrir en los sistemas que lanza), ni un motor de streaming, ni está pensado para programaciones de altísima frecuencia por debajo del segundo.

#### ¿Qué es un DAG?

Un grafo acíclico dirigido (Directed Acyclic Graph): un conjunto de tareas con dependencias y sin ciclos. En Airflow, un DAG también lleva su programación, su fecha de inicio, sus argumentos por defecto, sus etiquetas y otros ajustes. Cada vez que se ejecuta, crea un DAG run.

#### ¿Qué es una tarea?

La unidad básica de ejecución de un DAG: una instancia de un operador, una función Python decorada (`@task`) o un sensor. Cada tarea en cada DAG run se convierte en una task instance con su propio estado, logs y reintentos.

#### ¿Qué es un operador?

Una plantilla para una unidad de trabajo, como `BashOperator`, `PythonOperator`, `SQLExecuteQueryOperator`, `DatabricksRunNowOperator` o `S3ToRedshiftOperator`. Se instancia con parámetros dentro de un DAG para crear una tarea.

#### ¿Qué es una task instance?

Una ejecución concreta de una tarea para un DAG run concreto (y un índice de mapeo, en las tareas mapeadas). Tiene un estado (`scheduled`, `queued`, `running`, `success`, `failed`, `up_for_retry`, `skipped`, `upstream_failed` y otros), un número de intento y logs.

#### ¿Qué es un DAG run?

Una ejecución de un DAG, identificada por un run ID y una fecha lógica, creada por la programación, un disparo manual, un evento de asset o un backfill. Las ejecuciones programadas tienen un intervalo de datos.

#### ¿Qué aporta escribir los flujos como código?

Control de versiones, revisión de código, pruebas, generación dinámica de tareas, reutilización mediante funciones y librerías Python, y la posibilidad de desplegar los flujos con CI/CD como cualquier otro software.

#### ¿Cuáles son los componentes principales de un despliegue de Airflow?

El scheduler (decide qué se ejecuta y cuándo), el DAG processor (analiza los archivos de DAG), el API server (sirve la interfaz y la API REST; en Airflow 2 era el webserver), el executor y sus workers (ejecutan las tareas), el triggerer (ejecuta las tareas diferidas) y la base de datos de metadatos (guarda el estado).

#### ¿Qué es la base de datos de metadatos?

Una base de datos relacional (PostgreSQL o MySQL en producción; SQLite solo para pruebas) que guarda los DAG runs, las task instances, las conexiones, las variables, los XCom, los usuarios y los DAG serializados. Es la fuente de verdad del estado de Airflow, así que hay que respaldarla y mantenerla.

#### ¿Cuáles son los mayores cambios de Airflow 3?

Una nueva interfaz en React, el versionado de los DAG (cada ejecución queda ligada a la versión del DAG con la que corrió), el Task SDK y una Task Execution API para que los workers ya no hablen directamente con la base de metadatos, `airflow api-server` en lugar del webserver, los datasets renombrados como assets con programación por eventos, los backfills gestionados por el scheduler, la eliminación de los SubDAG y los SLA, y `schedule` en lugar de `schedule_interval`.

#### ¿Qué es el Task SDK?

La interfaz pública y estable para escribir DAG en Airflow 3 (`from airflow.sdk import dag, task, DAG, Asset, Variable`). Desacopla el código de los DAG de los detalles internos de Airflow y permite ejecutar tareas de forma remota mediante la Task Execution API, e incluso en otros lenguajes en el futuro.

#### ¿Qué es un provider de Airflow?

Un paquete con versión propia que añade operadores, hooks, sensores y conexiones para un sistema externo: `apache-airflow-providers-amazon`, `-google`, `-databricks`, `-snowflake`, `-postgres`, `-standard` (los operadores básicos como `BashOperator` y `PythonOperator` en Airflow 3) y muchos más.

#### ¿Qué es un hook?

Una clase que encapsula la conexión a un sistema externo y ofrece métodos de ayuda, como `S3Hook.load_file()` o `PostgresHook.get_records()`. Los operadores usan hooks internamente; también puedes usarlos en tus propias tareas Python.

#### ¿Qué es una conexión?

Un conjunto guardado de credenciales y parámetros de un sistema externo (host, usuario, contraseña, esquema, puerto, JSON extra), referenciado por un `conn_id`. Puede guardarse en la base de metadatos, en variables de entorno (`AIRFLOW_CONN_<ID>`) o en un secrets backend.

#### ¿Qué son las Variables de Airflow?

Valores de configuración clave-valor guardados en Airflow (base de metadatos, variables de entorno `AIRFLOW_VAR_<NOMBRE>` o un secrets backend) y leídos con `Variable.get()`. Leerlos en el nivel superior de un archivo de DAG provoca una llamada a la base o al backend en cada análisis, así que hay que leerlos dentro de las tareas o con plantillas.

#### ¿Qué diferencia hay entre Airflow y cron?

Cron solo lanza comandos a ciertas horas. Airflow añade dependencias entre tareas, reintentos, backfills, historial, logs centralizados, alertas, parametrización, una interfaz e integración con sistemas externos.

#### ¿Cómo se compara Airflow con Dagster y Prefect?

Los tres orquestan flujos en Python. Airflow es el más desplegado y tiene el ecosistema de providers más grande. Dagster está centrado en assets (declaras los activos de datos y su linaje), con tipado fuerte y pruebas locales. Prefect se enfoca en flujos Python dinámicos con poco código repetitivo. Airflow 3 se acercó a las ideas de Dagster con los assets y el versionado.

#### ¿Qué servicios administrados de Airflow existen?

Amazon MWAA (Managed Workflows for Apache Airflow), Google Cloud Composer, Astronomer (Astro) y la oferta de Airflow de Azure en Data Factory/Fabric. Administran el scheduler, los workers, la base de datos y las actualizaciones.

#### ¿Qué significa "orquestación", frente a "procesamiento"?

La orquestación decide qué se ejecuta, cuándo, en qué orden y qué pasa ante un fallo. El procesamiento es el cálculo real sobre los datos. Airflow orquesta; Spark, los motores SQL y dbt procesan.

#### ¿Para qué se usa la CLI `airflow`?

Para administrar y depurar Airflow: `airflow dags list|trigger|pause|test`, `airflow tasks test|clear`, `airflow db migrate|clean`, los comandos `airflow connections` y `variables`, `airflow config get-value`, y para iniciar los componentes (`scheduler`, `api-server`, `dag-processor`, `triggerer`, `celery worker`).

#### ¿Qué ofrece la API REST?

Una API estable y versionada (servida por el API server) para disparar y administrar DAG runs, leer estados y logs de las task instances, administrar conexiones, variables y pools, y limpiar tareas. Los pipelines de CI y otros sistemas la usan para integrarse con Airflow.

#### ¿Qué hace pausar un DAG?

Un DAG pausado no crea nuevas ejecuciones programadas; las tareas en curso terminan. Los DAG nuevos están pausados por defecto (`dags_are_paused_at_creation`) para que no empiecen a correr apenas se despliegan.

#### ¿Qué estados puede tener un DAG run?

`queued`, `running`, `success` y `failed`. El estado de un DAG run se deduce de sus tareas finales: tiene éxito si todas terminan bien o se omiten.

#### ¿Qué significa `upstream_failed`?

Que la tarea no se ejecutó porque una tarea anterior falló y no se pudo cumplir su trigger rule (por defecto `all_success`).

### Escribir DAG

#### ¿Cómo se define un DAG?

Con el decorador `@dag` sobre una función, o con un gestor de contexto `DAG`. Las tareas creadas dentro pertenecen al DAG.

```python
from datetime import datetime
from airflow.sdk import dag, task

@dag(schedule="@daily", start_date=datetime(2026, 1, 1), catchup=False, tags=["sales"])
def daily_sales():
    @task
    def extract() -> list[dict]:
        return [{"id": 1, "amount": 10}]

    @task
    def load(rows: list[dict]) -> None:
        print(f"cargando {len(rows)} filas")

    load(extract())

daily_sales()
```

#### ¿Qué es la TaskFlow API?

La forma de escribir tareas con decoradores (`@task`, `@task.bash`, `@task.virtualenv`, `@task.docker`, `@task.kubernetes` y otros), en la que los valores devueltos pasan automáticamente a las tareas siguientes por XCom y las dependencias se deducen de las llamadas entre funciones.

#### ¿Cómo se definen las dependencias entre tareas?

Con los operadores de desplazamiento de bits (`extract >> transform >> load`), listas para abrir y cerrar ramas (`start >> [a, b] >> end`), las funciones `chain()` y `cross_downstream()`, o de forma implícita al pasar las salidas de TaskFlow como argumentos.

#### ¿Qué son los `default_args`?

Un diccionario de argumentos aplicado a todas las tareas de un DAG, como `owner`, `retries`, `retry_delay`, `email_on_failure` o `execution_timeout`. Las tareas pueden sobrescribirlos.

#### ¿Qué significa `start_date`?

La fecha a partir de la cual se puede programar el DAG. Debe ser una fecha fija en el pasado, nunca `datetime.now()`, que cambiaría en cada análisis e impediría crear ejecuciones.

#### ¿Qué es `catchup`?

Si el scheduler crea ejecuciones para todos los intervalos perdidos entre `start_date` (o la última ejecución) y ahora. En Airflow 3 el valor por defecto es `False`; en Airflow 2 era `True`. Dejar catchup activo en un DAG con una fecha de inicio antigua puede lanzar cientos de ejecuciones a la vez.

#### ¿Para qué sirven las etiquetas y `doc_md`?

Las etiquetas agrupan y filtran los DAG en la interfaz. `doc_md` añade documentación en Markdown al DAG o a una tarea, visible en la interfaz, lo que ayuda a la persona de guardia a entender qué hace un DAG.

#### ¿Por qué el nivel superior de los archivos de DAG debe ser ligero?

El DAG processor analiza cada archivo de DAG una y otra vez (cada 30 segundos por defecto para los archivos modificados). El código de nivel superior, como consultas a bases de datos, llamadas a APIs, `Variable.get()` o imports pesados, se ejecuta en cada análisis, ralentiza todo el scheduler y golpea los sistemas externos. Ese trabajo va dentro de las tareas.

#### ¿Cómo se generan DAG o tareas de forma dinámica?

Con un bucle en Python sobre una configuración (una lista, un YAML leído del disco) para crear tareas o varios DAG al analizar el archivo, o con el mapeo dinámico de tareas para abrir ramas en tiempo de ejecución. Mantén la configuración estática y barata de leer para que el análisis siga siendo rápido y determinista.

#### ¿Qué es un task group?

Una forma de agrupar tareas visual y lógicamente en la interfaz (`@task_group` o `TaskGroup`), con un prefijo común para los IDs de las tareas y argumentos por defecto compartidos. Reemplazó a los SubDAG, que se eliminaron en Airflow 3.

#### ¿Qué son las trigger rules?

Reglas que deciden cuándo se ejecuta una tarea según el estado de las anteriores. Por defecto es `all_success`. Otras: `all_failed`, `all_done`, `one_success`, `one_failed`, `none_failed`, `none_failed_min_one_success`, `none_skipped` y `always`. Por ejemplo, una tarea de limpieza usa `all_done`.

#### ¿Cómo se crean ramas condicionales en un DAG?

Con `@task.branch` (o `BranchPythonOperator`), que devuelve el ID o los IDs de las tareas que se deben seguir; las demás se omiten. Una tarea de unión posterior necesita una trigger rule como `none_failed_min_one_success` para que no se omita también.

```python
@task.branch
def choose(**context):
    return "full_load" if context["logical_date"].day == 1 else "incremental_load"
```

#### ¿Qué es `ShortCircuitOperator`?

Un operador (o `@task.short_circuit`) que omite todas las tareas siguientes cuando su función devuelve un valor falso, por ejemplo cuando no hay datos nuevos.

#### ¿Qué es `LatestOnlyOperator`?

Un operador que omite las tareas siguientes salvo que la ejecución sea la programada más reciente, útil para tareas como enviar un reporte, que no tienen sentido durante un backfill.

#### ¿Cómo se ejecuta una tarea en un entorno Python aislado?

Con `@task.virtualenv` (crea un virtualenv con los requisitos indicados), `@task.external_python` (usa un intérprete existente), `@task.docker` o `@task.kubernetes` (se ejecuta en un contenedor). Así se evitan conflictos de dependencias con el propio Airflow.

#### ¿Cómo se pasan parámetros a un DAG run?

Con `params` declarados en el DAG (con valores por defecto y validación opcional con JSON Schema), que aparecen como un formulario al disparar manualmente y se leen con `{{ params.nombre }}` o desde el contexto.

#### ¿Para qué se usa el `BashOperator` y cuál es el riesgo?

Para ejecutar comandos o scripts de shell. El riesgo es meter en el comando entradas no confiables mediante plantillas (inyección) y esconder lógica compleja en shell, donde es difícil de probar.

#### ¿Cómo se define un timeout en una tarea?

Con `execution_timeout` (un `timedelta`); la tarea falla cuando dura más. Un `dagrun_timeout` a nivel de DAG hace fallar toda la ejecución tras cierta duración.

#### ¿Qué hace `max_active_runs`?

Limita cuántas ejecuciones de un DAG pueden estar activas a la vez. Ponerlo en 1 garantiza que las ejecuciones sean secuenciales, algo importante en los pipelines que dependen de la salida de la ejecución anterior.

#### ¿Qué es `depends_on_past`?

Un argumento de tarea: si es `True`, una task instance solo se ejecuta si la misma tarea tuvo éxito (o se omitió) en el DAG run anterior. Impone un procesamiento secuencial a nivel de tarea.

#### ¿Qué diferencia hay entre `@task` y `PythonOperator`?

Ambos ejecutan una función Python. `@task` (TaskFlow) es más conciso, pasa los valores devueltos por XCom automáticamente y deduce las dependencias. `PythonOperator` es la forma clásica; el XCom y las dependencias se conectan a mano. Se pueden mezclar en un DAG.

#### ¿Cómo se mezclan tareas TaskFlow y operadores clásicos?

Los operadores clásicos exponen `.output` (un `XComArg`) que se puede pasar a funciones TaskFlow, y las salidas de TaskFlow se pueden pasar a los campos con plantilla de los operadores clásicos. Las dependencias se deducen de esos vínculos.

#### ¿Qué es `@task.sensor`?

Un decorador que convierte una función Python en un sensor: devuelve `True` (o un `PokeReturnValue`) cuando se cumple la condición, con las opciones habituales `poke_interval`, `timeout` y `mode`.

#### ¿Qué son `@setup` y `@teardown`?

Decoradores que marcan las tareas que crean y limpian recursos (un cluster, una tabla temporal). Un teardown se ejecuta aunque falle el trabajo intermedio, y limpiar una tarea también vuelve a ejecutar su setup y su teardown.

#### ¿Cómo se define un owner y por qué importa?

Con `owner` en `default_args`. Aparece en la interfaz y en las alertas, así que se contacta al equipo correcto cuando el DAG falla.

#### ¿Qué es `email_on_failure`?

Un argumento de tarea que envía un correo cuando la tarea falla, usando la configuración SMTP. La mayoría de los equipos prefiere callbacks o notifiers hacia Slack o PagerDuty, con alertas más completas y enrutables.

#### ¿Qué pasa cuando cambias el nombre de una tarea o de un DAG?

Airflow lo trata como una tarea o un DAG nuevo: el historial queda bajo el nombre antiguo. En Airflow 3 el versionado de DAG muestra el cambio, pero renombrar sigue rompiendo la continuidad de las métricas y de `depends_on_past`.

### Programación y tiempo

#### ¿Cómo se programa un DAG?

Con el argumento `schedule`: una expresión cron (`"0 6 * * *"`), un preset (`"@daily"`, `"@hourly"`), un `timedelta`, un timetable, una lista de assets (por eventos) o `None` para los DAG manuales o disparados desde fuera.

#### ¿Qué es la fecha lógica?

La fecha que identifica el lugar de una ejecución en la programación (antes `execution_date`). En las programaciones por intervalos es el inicio del intervalo de datos, así que una ejecución diaria del 2026-10-15 empieza cuando termina ese día, el 2026-10-16. En Airflow 3, las ejecuciones manuales pueden no tener fecha lógica.

#### ¿Qué es un intervalo de datos?

El periodo de datos del que es responsable una ejecución programada, de `data_interval_start` a `data_interval_end`. Usarlo en las consultas (en lugar de "ahora") hace que las ejecuciones sean reproducibles y los backfills correctos.

```sql
SELECT * FROM orders
WHERE created_at >= '{{ data_interval_start }}' AND created_at < '{{ data_interval_end }}'
```

#### ¿Por qué un DAG diario se ejecuta "con un día de retraso"?

Porque con la programación por intervalos una ejecución empieza al final de su intervalo: procesa un día completo, así que solo puede empezar cuando ese día terminó. En Airflow 3 las programaciones cron usan por defecto `CronTriggerTimetable`, que ejecuta a la hora del cron sin semántica de intervalo, así que esto sorprende menos.

#### ¿Qué es un timetable?

Una clase que define una programación personalizada cuando cron no basta: solo días hábiles, varias horas distintas según el día, calendarios fiscales. Los incluidos son `CronDataIntervalTimetable`, `CronTriggerTimetable`, `DeltaDataIntervalTimetable` y `MultipleCronTriggerTimetable`.

#### ¿Cómo maneja Airflow las zonas horarias?

Internamente todo se guarda en UTC. Puedes dar a un DAG un `start_date` con zona horaria (con `pendulum`), y las programaciones cron siguen esa zona, incluidos los cambios de horario de verano. La interfaz puede mostrar la hora local.

#### ¿Qué es un backfill?

Ejecutar un DAG para intervalos pasados, por ejemplo tras añadir un DAG o corregir un error. En Airflow 3 los backfills se crean desde la interfaz, la API o `airflow backfill create` y los ejecuta el scheduler, con opciones de reprocesamiento y concurrencia.

#### ¿Qué diferencia hay entre catchup y un backfill?

Catchup es automático: el scheduler crea las ejecuciones perdidas desde la última. Un backfill es una petición explícita para un rango de fechas, que además puede volver a ejecutar intervalos que ya tuvieron éxito.

#### ¿Cómo se limpian y se vuelven a ejecutar tareas?

En la interfaz o la CLI, limpiar (clear) una task instance reinicia su estado para que el scheduler la vuelva a ejecutar, opcionalmente con las instancias siguientes, anteriores, pasadas o futuras. Es la forma habitual de reprocesar tras una corrección.

#### ¿Qué es un disparo manual y cómo se hace?

Iniciar un DAG run fuera de su programación desde la interfaz, la CLI (`airflow dags trigger`) o la API REST, opcionalmente con una configuración o parámetros.

#### ¿Qué significa "tarea idempotente" en Airflow?

Una tarea que produce el mismo resultado se ejecute una o varias veces para el mismo intervalo. Se logra procesando el intervalo de datos y no "lo último", escribiendo con sobrescritura de una partición o `MERGE` en lugar de append, y usando nombres de archivo deterministas.

#### ¿Por qué las tareas no deben usar `datetime.now()`?

Porque las reejecuciones y los backfills procesarían el periodo equivocado. Usa la fecha lógica o el intervalo de datos del contexto o de las plantillas.

#### ¿Cómo se ejecuta un DAG solo los días hábiles?

Con una expresión cron como `0 6 * * 1-5`, o con un timetable propio si importan los festivos. Una tarea de rama o de cortocircuito también puede omitir el procesamiento en festivos según una tabla de calendario.

#### ¿Qué es el preset `@once`?

Una programación que crea una sola ejecución, útil para DAG puntuales como migraciones.

#### ¿Qué pasa si una ejecución dura más que el intervalo de programación?

La siguiente ejecución empieza a su hora si `max_active_runs` lo permite, así que las ejecuciones pueden solaparse. Usa `max_active_runs=1` (y posiblemente `depends_on_past=True`) cuando no deban solaparse.

#### ¿Cómo se pasa a una tarea la fecha de la última ejecución exitosa?

Con las variables de plantilla `prev_data_interval_start_success` y `prev_data_interval_end_success` (o `prev_start_date_success`), útiles en cargas incrementales que deben continuar desde el último punto exitoso.

#### ¿Cómo afectan los cambios de horario de verano a las programaciones?

Con una fecha de inicio con zona horaria, un cron diario a las 02:30 puede omitirse o ejecutarse dos veces en los días de cambio, según el reloj local. Programa los jobs críticos fuera de la franja de 01:00 a 03:00 o en UTC. (En Colombia no hay horario de verano, pero sí en muchas zonas de origen de los datos.)

### Operadores, sensores y tareas diferibles

#### ¿Qué es un sensor?

Un operador especial que espera una condición: un archivo en S3 (`S3KeySensor`), una partición, una tarea externa, una consulta SQL que devuelve filas, un endpoint HTTP, una hora. Comprueba periódicamente hasta que la condición se cumple o vence el timeout.

#### ¿Qué diferencia hay entre los modos `poke` y `reschedule`?

En modo `poke` el sensor ocupa un slot de worker durante toda la espera, durmiendo entre comprobaciones. En modo `reschedule` libera el slot entre comprobaciones y se vuelve a programar más tarde, lo que es mejor para esperas largas. El modo diferible es todavía mejor.

#### ¿Qué son los operadores diferibles?

Operadores que, mientras esperan algo externo (un job, un archivo, una hora), se suspenden y delegan la espera a un trigger asíncrono que corre en el proceso triggerer, liberando el slot del worker. Cuando el trigger se activa, la tarea continúa en un worker. Muchos operadores de providers tienen `deferrable=True`.

#### ¿Qué es el triggerer?

Un componente que ejecuta los triggers basados en asyncio de las tareas diferidas. Un solo triggerer puede atender miles de esperas a la vez con pocos recursos.

#### ¿Qué es `ExternalTaskSensor`?

Un sensor que espera a que una tarea o un DAG run de otro DAG llegue a un estado, por defecto para la misma fecha lógica. Crea dependencias entre DAG, pero acopla las programaciones; los assets suelen ser una alternativa más limpia.

#### ¿Qué es `TriggerDagRunOperator`?

Un operador que dispara otro DAG, opcionalmente pasándole una configuración y esperando a que termine. Es una dependencia de tipo "empujar", frente al `ExternalTaskSensor`, que "jala".

#### ¿Qué es el timeout de un sensor y por qué definirlo?

El tiempo máximo que espera un sensor antes de fallar (`timeout`, siete días por defecto). Ponle un valor realista para que la falta de un archivo de origen se note rápido en lugar de bloquear recursos durante días. `soft_fail=True` marca el sensor como omitido en lugar de fallido.

#### ¿Cómo se escribe un operador propio?

Heredando de `BaseOperator`, declarando los parámetros en `__init__`, listando los campos con plantilla en `template_fields` e implementando `execute(self, context)`, con hooks para las conexiones externas. Mantén `__init__` ligero, porque se ejecuta al analizar el DAG.

```python
from airflow.sdk import BaseOperator

class RowCountCheckOperator(BaseOperator):
    template_fields = ("table",)

    def __init__(self, *, table: str, conn_id: str, min_rows: int = 1, **kwargs):
        super().__init__(**kwargs)
        self.table, self.conn_id, self.min_rows = table, conn_id, min_rows

    def execute(self, context):
        from airflow.providers.postgres.hooks.postgres import PostgresHook
        count = PostgresHook(self.conn_id).get_first(f"SELECT count(*) FROM {self.table}")[0]
        if count < self.min_rows:
            raise ValueError(f"{self.table} tiene {count} filas")
        return count
```

#### ¿Para qué se usa `EmptyOperator`?

Una tarea que no hace nada, usada como marca de inicio o fin o como punto de unión en el grafo para que las dependencias sean más claras.

#### ¿Cómo se llama a una base de datos SQL desde Airflow?

Con `SQLExecuteQueryOperator` (provider common SQL) y una conexión, o con el hook específico del provider en una tarea Python. Guarda el SQL en archivos `.sql` aparte, referenciados mediante plantillas.

#### ¿Cómo se lanza un job de Databricks desde Airflow?

Con `DatabricksRunNowOperator` (ejecuta un job existente por su ID, con parámetros) o `DatabricksSubmitRunOperator` (envía una ejecución puntual), del provider de Databricks, normalmente en modo diferible para que la espera no ocupe un worker. `DatabricksWorkflowTaskGroup` puede definir un job de Databricks desde Airflow.

#### ¿Cómo se ejecuta dbt desde Airflow?

Con un `BashOperator` que llama a `dbt build`, con un operador de dbt Cloud (`DbtCloudRunJobOperator`) o con Astronomer Cosmos, que convierte cada modelo de dbt en una tarea de Airflow con las dependencias del grafo de dbt.

#### ¿Cómo se ejecuta trabajo en Kubernetes desde Airflow?

Con `KubernetesPodOperator` o `@task.kubernetes`, que inician un pod con una imagen, un comando, unos recursos y unos secretos dados para cada tarea. Cada tarea tiene sus propias dependencias y recursos.

#### ¿Para qué se usa `PythonVirtualenvOperator`?

Para ejecutar una función con dependencias que chocan con las de Airflow, en un virtualenv nuevo en cada ejecución (más lento) o en uno en caché. La función debe ser autocontenida porque se ejecuta en otro intérprete.

#### ¿Qué son los operadores de transferencia?

Operadores que mueven datos entre dos sistemas en una sola tarea, como `S3ToRedshiftOperator`, `GCSToBigQueryOperator`, `SqlToS3Operator` o `S3ToSnowflakeOperator`. Por lo general delegan el trabajo al sistema destino (por ejemplo con un comando `COPY`).

#### ¿Para qué se usa `HttpOperator`?

Para llamar a APIs HTTP con una conexión que define la URL base y las credenciales, con comprobaciones de la respuesta y paginación opcionales. `HttpSensor` espera a que un endpoint devuelva una condición.

#### ¿Cómo se ejecuta un job de AWS Glue desde Airflow?

Con `GlueJobOperator` del provider de Amazon, pasando el nombre del job y los argumentos del script, preferiblemente con `deferrable=True` o con `wait_for_completion` y un `GlueJobSensor`.

#### ¿Cómo se ejecuta una consulta de Athena desde Airflow?

Con `AthenaOperator`, que envía la consulta, espera a que termine y escribe los resultados en la ubicación de salida de S3 configurada. Usa fechas con plantilla en la consulta para procesar el intervalo de datos.

#### ¿Qué es `on_execute_callback`?

Un callback que se llama justo antes de ejecutar una tarea, usado para logs o notificaciones. Como los demás callbacks, debe ser rápido y no debe hacer fallar la tarea.

### XCom y paso de datos

#### ¿Qué es XCom?

"Cross-communication": un mecanismo para pasar valores pequeños entre tareas. Una tarea publica un valor (los valores devueltos con TaskFlow se publican automáticamente) y las tareas siguientes lo leen. Por defecto, los valores se guardan en la base de metadatos.

#### ¿Por qué no pasar muchos datos por XCom?

El backend por defecto guarda los valores en la base de metadatos, que no está pensada para cargas grandes, y los valores serializados tienen límites de tamaño. Pasa referencias (una ruta de S3, un nombre de tabla, una partición) y deja los datos en el almacenamiento.

#### ¿Qué es un backend de XCom personalizado?

Un backend intercambiable que guarda los valores de XCom en otro lugar (S3, GCS, Azure Blob) y solo deja una referencia en la base de datos. El provider Common IO ofrece un backend de almacenamiento de objetos con un umbral de tamaño.

#### ¿Cómo se lee un XCom en una plantilla?

```jinja2
{{ ti.xcom_pull(task_ids='extract', key='return_value') }}
```

Con TaskFlow, basta con pasar la salida de una función de tarea como argumento de otra.

#### ¿Qué es el contexto de la tarea?

Un diccionario con información de ejecución disponible para las tareas: `ti` (task instance), `dag_run`, `logical_date`, `data_interval_start`, `data_interval_end`, `params`, `run_id` y más. En TaskFlow se obtiene con `get_current_context()` o declarando `**context`.

#### ¿Qué son las plantillas Jinja en Airflow?

Muchos campos de los operadores (listados en `template_fields`) se procesan con Jinja justo antes de ejecutarse, con variables de contexto como `{{ ds }}`, `{{ data_interval_start }}`, `{{ params.x }}`, macros como `{{ macros.ds_add(ds, -1) }}` y Variables (`{{ var.value.nombre }}`). Los valores resultantes se ven en la interfaz.

#### ¿Qué es `ds`?

Una variable de plantilla con la fecha lógica en formato `YYYY-MM-DD`. `ds_nodash` da `YYYYMMDD`. Son prácticas para nombres de particiones y rutas de archivos.

#### ¿Qué es el mapeo dinámico de tareas?

Crear un número variable de task instances en tiempo de ejecución a partir de la salida de una tarea anterior, con `.expand()`. Por ejemplo, una tarea por cada archivo encontrado en un bucket. `.partial()` fija los argumentos comunes a todas las instancias.

```python
@task
def list_files() -> list[str]:
    return ["a.csv", "b.csv", "c.csv"]

@task
def process(path: str) -> int:
    return len(path)

process.expand(path=list_files())
```

#### ¿Cómo se limita el paralelismo de las tareas mapeadas?

Con `max_active_tis_per_dag` o `max_active_tis_per_dagrun` en la tarea mapeada, o asignándola a un pool con pocos slots.

#### ¿Qué hace `multiple_outputs=True`?

En un `@task` que devuelve un diccionario, publica cada clave como un XCom aparte, para que las tareas siguientes puedan usar `result["clave"]` por separado.

#### ¿Se borran los XCom después de una ejecución?

Se quedan en la base de datos (y se limpian cuando una tarea se limpia y se vuelve a ejecutar) hasta que los purgas con `airflow db clean` o una política de retención. Es otra razón para que sean pequeños.

#### ¿Qué es `XComArg`?

El objeto que se obtiene al llamar a una función TaskFlow o al acceder a `.output` de un operador. Representa un valor futuro y lleva la dependencia, así que pasarlo a otra tarea vincula las dos.

#### ¿Cómo se evitan los errores de serialización con XCom?

Devolviendo valores serializables en JSON (o tipos que Airflow sabe serializar, como dataclasses y DataFrames de pandas con el serializador adecuado); evita conexiones abiertas, generadores u objetos grandes. Devuelve rutas o IDs.

### Assets y programación por eventos

#### ¿Qué es un asset (antes dataset)?

Una referencia lógica a un conjunto de datos, identificada por una URI (por ejemplo `s3://bucket/sales/`), declarada como salida (outlet) de una tarea productora. Cuando la tarea termina bien, Airflow registra un evento del asset y se disparan los DAG programados sobre ese asset.

```python
from airflow.sdk import Asset, dag, task

sales = Asset("s3://lake/silver/sales/")

@dag(schedule="@daily", start_date=datetime(2026, 1, 1))
def produce():
    @task(outlets=[sales])
    def build_sales(): ...
    build_sales()

@dag(schedule=[sales], start_date=datetime(2026, 1, 1))
def consume():
    @task
    def report(): ...
    report()
```

#### ¿Por qué usar assets en lugar de `ExternalTaskSensor`?

Los assets expresan directamente las dependencias de datos ("ejecutar cuando se actualice sales") sin alinear programaciones ni ocupar slots con sensores, y la interfaz muestra el linaje entre los DAG productores y consumidores.

#### ¿Puede un DAG depender de varios assets?

Sí. Una lista significa que todos deben haberse actualizado desde la última ejecución; también se pueden combinar assets con expresiones `&` (y) y `|` (o). `AssetOrTimeSchedule` combina una programación por tiempo con disparos por assets.

#### ¿Qué son los asset watchers?

Una función de Airflow 3 para programar por eventos de sistemas externos: un `AssetWatcher` asocia un trigger (por ejemplo sobre una cola de mensajes como SQS o Kafka) a un asset, para que un DAG se ejecute cuando llega un evento externo, no solo cuando otra tarea de Airflow actualiza el asset.

#### ¿Qué es el decorador `@asset`?

Un atajo de Airflow 3 que define un asset junto con el DAG de una sola tarea que lo materializa, para escribir de forma centrada en los assets, al estilo de Dagster.

#### ¿Saben los assets si los datos cambiaron de verdad?

No. Airflow solo sabe que una tarea productora terminó bien; no inspecciona los datos. Si una tarea puede terminar bien sin escribir nada, no debería emitir el evento, o el consumidor debe comprobarlo.

#### ¿Se pueden añadir metadatos a un evento de asset?

Sí. Una tarea productora puede añadir información extra (por ejemplo el número de filas o la partición escrita) al evento del asset mediante los outlet events, y los consumidores pueden leerla desde los eventos que los dispararon, en su contexto.

#### ¿Cómo se ve el linaje de los assets en la interfaz?

La vista de assets muestra cada asset con sus DAG productores y consumidores y el historial de eventos, lo que hace visibles las dependencias entre DAG.

#### ¿Qué es un asset alias?

Un marcador que se usa cuando la URI exacta del asset solo se conoce en tiempo de ejecución: la tarea emite eventos para un alias y le asocia el asset concreto, y los consumidores pueden programarse sobre el alias.

#### ¿Puede dispararse un DAG por programación y por assets a la vez?

Sí, con `AssetOrTimeSchedule`, que ejecuta según un timetable y además cada vez que se cumple la condición de los assets.

### Executors y arquitectura

#### ¿Qué es un executor?

El componente que decide cómo y dónde se ejecutan las task instances. El scheduler envía las tareas en cola al executor, que las ejecuta en local o las reparte entre workers.

#### ¿Qué executors hay disponibles?

`LocalExecutor` (procesos en paralelo en la máquina del scheduler), `CeleryExecutor` (un conjunto de workers alimentados por un broker de mensajes como Redis o RabbitMQ), `KubernetesExecutor` (un pod por tarea) y executors de providers como los de AWS ECS y Batch y el Edge executor para workers remotos. Desde Airflow 2.10 se pueden usar varios executors a la vez.

#### ¿Cuándo elegirías el CeleryExecutor?

Para muchas tareas cortas con una carga estable: los workers de larga duración inician las tareas rápido. Hay que operar un broker y escalar los workers por tu cuenta (o con KEDA).

#### ¿Cuándo elegirías el KubernetesExecutor?

Cuando las tareas necesitan recursos o imágenes distintos, importa el aislamiento y la carga es irregular: cada tarea corre en su propio pod y los recursos se liberan después. El arranque del pod añade segundos de latencia por tarea.

#### ¿Qué hace el scheduler?

Lee los DAG serializados, crea los DAG runs cuando corresponde, comprueba qué task instances tienen sus dependencias cumplidas, respeta los límites de concurrencia y los pools, y envía las tareas al executor. Pueden correr varios schedulers a la vez para tener alta disponibilidad.

#### ¿Qué hace el DAG processor?

Analiza los archivos de DAG y guarda los DAG serializados en la base de datos. En Airflow 3 es un componente aparte, así que el código de los usuarios nunca se ejecuta dentro del scheduler.

#### ¿Qué ajustes de concurrencia existen?

`parallelism` (máximo de tareas en ejecución por scheduler), `max_active_tasks_per_dag`, `max_active_runs_per_dag`, los slots de los pools, `max_active_tis_per_dag` por tarea y ajustes propios de cada executor, como la concurrencia de los workers de Celery.

#### ¿Qué es un pool?

Un límite con nombre sobre los slots de tareas concurrentes, usado para proteger un recurso compartido: por ejemplo un pool de 4 slots para las tareas que consultan una base de datos de producción. Las tareas se asignan a un pool y pueden consumir varios slots.

#### ¿Qué es el priority weight?

Un número que decide qué tareas en cola se ejecutan primero cuando faltan slots. La regla de peso (`downstream`, `upstream`, `absolute`) controla cómo se acumula a lo largo del grafo.

#### ¿Qué son las colas en el CeleryExecutor?

Colas con nombre a las que se suscriben los workers. Asignar tareas a una cola (`queue="gpu"`) las envía a workers con los recursos adecuados.

#### ¿Cómo obtienen credenciales los workers en Airflow 3?

A través de la Task Execution API: las tareas piden conexiones, variables y XCom al API server en lugar de leer la base de metadatos, lo que mejora la seguridad y permite workers remotos.

#### ¿Qué papel cumple el broker de mensajes con Celery?

Redis o RabbitMQ guarda la cola de tareas que envía el scheduler; los workers de Celery la consumen. Un backend de resultados (normalmente la base de datos) guarda los estados de las tareas.

#### ¿Qué es el `pod_template_file`?

Una especificación de pod de Kubernetes que el KubernetesExecutor (y el KubernetesPodOperator) usa como base de los pods de las tareas: imagen, recursos, volúmenes, selectores de nodo, service account. Las tareas pueden sobrescribir partes con `executor_config`.

#### ¿Se pueden usar varios executors a la vez?

Sí, desde Airflow 2.10: se configura una lista de executors y se asigna cada tarea a uno con el argumento `executor`, por ejemplo la mayoría de las tareas en Celery y las pesadas y aisladas en Kubernetes.

#### ¿Qué es el Edge executor?

Un executor (del provider Edge3) que ejecuta tareas en workers remotos conectados a la API de Airflow por HTTP, por ejemplo en otra red o en otro centro de datos, sin acceso directo a la base de datos.

#### ¿Cómo se logra alta disponibilidad del scheduler?

Ejecutando dos o más schedulers contra la misma base PostgreSQL o MySQL; se coordinan con bloqueos a nivel de fila. Se ejecutan varios API servers detrás de un balanceador y varios triggerers.

### Configuración, seguridad y secretos

#### ¿Cómo se configura Airflow?

Con `airflow.cfg`, sobrescrito por variables de entorno con el formato `AIRFLOW__SECCION__CLAVE` (por ejemplo `AIRFLOW__CORE__PARALLELISM`). Las variables de entorno son lo habitual en contenedores.

#### ¿Qué es un secrets backend?

Una integración que lee conexiones y variables de un gestor de secretos externo: AWS Secrets Manager o SSM Parameter Store, HashiCorp Vault, Google Secret Manager, Azure Key Vault. Así los secretos no tienen que guardarse en la base de metadatos.

#### ¿Cómo evita Airflow mostrar secretos en los logs y la interfaz?

Enmascara las contraseñas de las conexiones, las variables cuyo nombre contiene palabras como `password`, `secret` o `token`, y los valores registrados con `mask_secret()`. El enmascarado no es infalible, así que no imprimas secretos.

#### ¿Qué es la clave Fernet?

La clave usada para cifrar las contraseñas de las conexiones y los valores de las variables en la base de metadatos. Debe estar definida, mantenerse en secreto y ser idéntica en todos los componentes; rotarla exige volver a cifrar.

#### ¿Cómo se controla el acceso a la interfaz?

Con un auth manager. Airflow 3 trae un auth manager simple para desarrollo; el auth manager FAB ofrece control de acceso basado en roles (Admin, Op, User, Viewer y roles propios), y los servicios administrados se integran con el IAM de la nube.

#### ¿Cómo debe acceder el código de los DAG a los recursos de la nube?

Con la identidad del worker (IAM roles for service accounts en Kubernetes, el rol de ejecución de MWAA, workload identity) siempre que se pueda, en lugar de claves de larga duración guardadas en conexiones.

#### ¿Cómo se definen conexiones como variables de entorno?

Con `AIRFLOW_CONN_<CONN_ID>` igual a una URI o un JSON, por ejemplo `AIRFLOW_CONN_WAREHOUSE='postgresql://user:pass@host:5432/db'`. No aparecen en la interfaz y tienen prioridad sobre una conexión con el mismo ID en la base de datos (aunque un secrets backend configurado se consulta primero).

#### ¿Cómo se restringe quién puede disparar un DAG?

Con control de acceso basado en roles: se dan permisos a los roles sobre DAG concretos (por ID de DAG o con `access_control` en el DAG), para que cada equipo solo pueda disparar y limpiar sus propios DAG.

#### ¿Por qué es riesgoso que muchas personas editen el código de los DAG?

El código de los DAG se ejecuta con los permisos de los workers y puede leer las conexiones, así que quien puede desplegar DAG tiene en la práctica acceso a todas las conexiones. La revisión de código y los controles de CI en el repositorio de DAG son parte de la seguridad.

### Pruebas y calidad del código

#### ¿Cómo se prueba que los DAG cargan correctamente?

Con una prueba de integridad que carga todos los archivos de DAG con `DagBag` y comprueba que no hay errores de importación, además de controles de convenciones (etiquetas, owners, reintentos, sin ciclos).

```python
from airflow.models import DagBag

def test_no_import_errors():
    bag = DagBag(dag_folder="dags/", include_examples=False)
    assert not bag.import_errors, bag.import_errors

def test_every_dag_has_retries():
    bag = DagBag(dag_folder="dags/", include_examples=False)
    for dag_id, dag in bag.dags.items():
        assert dag.default_args.get("retries", 0) >= 1, dag_id
```

#### ¿Cómo se hacen pruebas unitarias de la lógica de las tareas?

Manteniendo la lógica de negocio en funciones o módulos Python normales fuera del archivo del DAG, probándolos con pytest sin Airflow, y dejando las tareas como envoltorios finos. Para los operadores, se prueba `execute()` con hooks simulados (mocks).

#### ¿Qué hace `dag.test()`?

Ejecuta un DAG run completo en un solo proceso Python sin scheduler, útil para depurar en local desde un IDE con puntos de interrupción.

#### ¿Qué hace `airflow tasks test`?

Ejecuta una task instance para una fecha dada sin registrar su estado en la base de datos ni comprobar dependencias. Sirve para revisar rápido las plantillas y la lógica.

#### ¿Cómo se ejecuta Airflow en local para desarrollar?

Con el Docker Compose oficial, `airflow standalone`, la CLI de Astro (`astro dev start`) o Breeze para contribuir a Airflow. Usa la misma imagen y los mismos providers que en producción.

#### ¿Qué linting es útil para el código de los DAG?

Ruff con las reglas de Airflow (las reglas `AIR` señalan imports obsoletos y problemas de migración a Airflow 3), verificación de tipos y controles propios para el código de nivel superior, la falta de owners o etiquetas y las credenciales escritas en el código.

#### ¿Cómo se prueban los DAG contra sistemas reales?

En un Airflow de staging que apunta a almacenes de datos de staging: despliega desde una rama, dispara ejecuciones con parámetros para un rango de fechas corto y verifica las salidas con pruebas de calidad de datos. Evita ejecutar pruebas contra los almacenes de producción.

#### ¿Cómo se prueban los operadores propios que usan sistemas externos?

Simulando el hook en las pruebas unitarias para verificar la lógica y los parámetros del operador, y ejecutando pruebas de integración contra contenedores locales (Postgres, LocalStack para AWS, MinIO para S3) en CI.

#### ¿Cómo se comprueba que los campos con plantilla se generan bien?

Generándolos para un contexto dado en una prueba (`ti.render_templates()`), o ejecutando `airflow tasks render dag_id task_id fecha`, y revisando el SQL o el comando resultante.

#### ¿Qué debe ejecutar un pipeline de CI para un repositorio de Airflow?

Linting (Ruff con reglas `AIR`), pruebas unitarias de la lógica de negocio, pruebas de integridad de los DAG (errores de importación del `DagBag`, convenciones, ciclos), controles del tiempo de análisis, construcción de la imagen y despliegue en staging, con el despliegue a producción tras el merge o una aprobación.

#### ¿Cómo se prueba que un DAG tiene la estructura correcta?

Cargándolo desde un `DagBag` y comprobando los IDs de las tareas, las dependencias (`task.downstream_task_ids`), las programaciones y los ajustes, para detectar cambios accidentales en el grafo.

### Despliegue y operación

#### ¿Cómo se despliegan los DAG?

La mayoría de los equipos construye una imagen Docker con Airflow, los providers, las dependencias y el código de los DAG, y la despliega con CI/CD en Kubernetes (chart de Helm) o en un servicio administrado. Alternativas: sincronizar los DAG desde Git con git-sync o en un bucket de S3 (MWAA). Los DAG bundles de Airflow 3 pueden leer los DAG directamente desde Git con versionado.

#### ¿Qué es un DAG bundle?

Un concepto de Airflow 3 para un conjunto de archivos de DAG provenientes de un origen como una carpeta local o un repositorio Git, que permite a Airflow seguir las versiones del código y ejecutar cada DAG run con la versión con la que empezó.

#### ¿Cómo se actualiza Airflow de forma segura?

Leyendo las notas de la versión, actualizando primero en un entorno de pruebas, usando los archivos de constraints para fijar dependencias compatibles, ejecutando `airflow db migrate`, revisando los DAG en busca de elementos obsoletos (reglas `AIR` de Ruff para Airflow 3) y respaldando la base de metadatos antes de migrar producción.

#### ¿Qué son los archivos de constraints?

Listas de dependencias fijadas que se publican para cada versión de Airflow y de Python, usadas con `pip install "apache-airflow==X" --constraint <url>` para obtener un conjunto de paquetes que se sabe que funciona.

#### ¿Cómo se mantiene sana la base de metadatos?

Usando un PostgreSQL administrado con copias de respaldo, vigilando su tamaño y ejecutando `airflow db clean` periódicamente para purgar task instances, metadatos de logs y XCom antiguos. Una base enorme ralentiza el scheduler y la interfaz.

#### ¿Dónde van los logs de las tareas?

Por defecto a archivos locales en los workers, visibles en la interfaz. En producción se configura el logging remoto en S3, GCS, Azure Blob, Elasticsearch o CloudWatch para que los logs sobrevivan a los reinicios de los pods.

#### ¿Cómo se monitorea Airflow?

Con métricas StatsD u OpenTelemetry (heartbeat del scheduler, tiempo de análisis de los DAG, tareas en cola y en ejecución, duraciones, uso de los pools) en Prometheus/Grafana o Datadog, endpoints de salud y alertas sobre los fallos y las ejecuciones demasiado largas.

#### ¿Cómo recibes alertas cuando falla una tarea?

Con callbacks (`on_failure_callback`, `on_retry_callback`, `on_success_callback`) que envían a Slack, correo o PagerDuty, las clases notifier de los providers o la configuración de correo. Alerta a nivel de DAG para tener mensajes accionables y sin duplicados.

#### ¿Qué reemplazó a los SLA en Airflow 3?

Los SLA (`sla` y `sla_miss_callback`) se eliminaron porque no eran confiables. Airflow 3.1 introdujo las deadline alerts, que lanzan un callback cuando un DAG run no terminó antes de un plazo relativo a una hora de referencia. Hasta entonces, los equipos usaban `execution_timeout`, `dagrun_timeout` y monitoreo externo.

#### ¿Cuáles son las causas comunes de tareas atascadas en `queued`?

No hay slots libres (límites de parallelism, de pool o de concurrencia del DAG), los workers están caídos o no consumen la cola, el executor no logra arrancar pods (cuotas, errores al descargar la imagen) o hay un problema con el scheduler. Revisa los pools, los logs de los workers y los eventos del executor.

#### ¿Qué son las tareas zombie?

Task instances marcadas como en ejecución cuyo proceso murió sin avisar (caída del worker, OOM kill, desalojo del pod). El scheduler detecta la falta de heartbeats y las marca como fallidas o las reintenta.

#### ¿Cómo se escala Airflow?

Con varios schedulers, escalando los workers (autoescalado de los workers de Celery con KEDA, o el executor de Kubernetes), usando operadores diferibles para liberar slots, reduciendo el tiempo de análisis de los DAG, ajustando `parallelism` y los pools, y dejando el cálculo pesado fuera de Airflow.

#### ¿Por qué importa el tiempo de análisis de los DAG?

Un análisis lento retrasa la programación de todos los DAG y consume CPU. Se mide con `airflow dags report`; se corrige eliminando el trabajo de nivel superior, evitando imports pesados a nivel de módulo y dividiendo los archivos gigantes de DAG generados.

#### ¿Qué es el chart oficial de Helm?

El chart de Helm de Apache Airflow, que despliega todos los componentes en Kubernetes con opciones para los executors, git-sync, PgBouncer, el autoescalado con KEDA, los logs y los secretos. Es el despliegue estándar autoalojado en Kubernetes.

#### ¿Por qué usar PgBouncer con Airflow?

Cada tarea y componente abre conexiones a la base de datos; muchas tareas concurrentes pueden agotar el límite de conexiones de PostgreSQL. PgBouncer las agrupa. En Airflow 3 la Task Execution API reduce las conexiones directas desde los workers.

#### ¿Cómo se despliega en Amazon MWAA?

Subiendo los DAG al bucket de S3 del entorno (normalmente desde CI con `aws s3 sync`) y administrando `requirements.txt`, los plugins y un script de arranque en S3; la versión de Airflow y el tamaño del entorno se definen en su configuración. El rol de ejecución da el acceso a AWS.

#### ¿Qué debe contener un runbook para un DAG que falla?

Qué hace el DAG y quién es el responsable, las dependencias de origen, cómo revisar los logs y las entradas, qué tareas se pueden limpiar y reejecutar sin riesgo, cómo hacer un backfill, a quién avisar y los fallos conocidos con su solución.

#### ¿Cómo se revierte un despliegue de DAG defectuoso?

Volviendo a desplegar la imagen o el commit de Git anterior con CI. Con el versionado de DAG de Airflow 3, las ejecuciones existentes conservan su versión. Después se limpian las ejecuciones fallidas si hace falta.

### Buenas prácticas

#### ¿Debe Airflow hacer el procesamiento de datos?

No. Airflow debe orquestar: lanzar Spark, motores SQL, dbt, Databricks o contenedores que hacen el procesamiento, y pasar referencias. El trabajo pesado con pandas en los workers de Airflow compite con otras tareas y escala mal.

#### ¿Cuál es una buena granularidad de tareas?

Cada tarea debería ser una unidad con sentido y reintentable (extraer un origen, cargar una tabla, ejecutar un grupo de modelos). Demasiado gruesa obliga a reintentar mucho trabajo; demasiado fina añade sobrecarga de programación y vuelve ilegible el grafo.

#### ¿Cómo se hacen seguros los reintentos?

Haciendo las tareas idempotentes, definiendo `retries` y `retry_delay` (con `retry_exponential_backoff`) para los errores transitorios, y fallando rápido (sin reintentos) ante errores que reintentar no arregla, como credenciales incorrectas o un fallo de calidad de datos.

#### ¿Dónde debe vivir la configuración?

En el código (versionado) para la estructura, en variables de entorno o Variables para los valores propios de cada entorno, y en un secrets backend para las credenciales. Evita leer muchas Variables al analizar los DAG.

#### ¿Cómo se nombran los DAG y las tareas?

De forma coherente y descriptiva: `dominio__proposito` para los DAG (`sales__daily_load`), verbos para las tareas (`extract_orders`, `load_orders`), con owners y etiquetas para los equipos y los dominios de datos.

#### ¿Cómo se maneja el código compartido entre DAG?

Poniéndolo en un paquete Python (en la carpeta `include/` o `plugins/` del repositorio, o instalado en la imagen) con sus propias pruebas, en lugar de copiar código entre archivos de DAG.

#### ¿Para qué sirven los plugins en Airflow?

Para extender Airflow con vistas propias en la interfaz, enlaces de menú, macros, listeners, timetables y, en Airflow 3, apps FastAPI y vistas React. Los operadores y hooks propios no necesitan ser plugins; basta con módulos Python normales.

#### ¿Qué son los listeners?

Ganchos sobre los eventos de Airflow (inicio o fin de un DAG run, cambios de estado de las task instances) implementados con pluggy, usados para linaje (OpenLineage), auditoría o notificaciones propias.

#### ¿Qué es OpenLineage en Airflow?

Un estándar de metadatos de linaje. El provider de OpenLineage emite eventos que describen las entradas y salidas de las tareas hacia un backend como Marquez o un catálogo de datos, para ver qué jobs leen y escriben qué datasets.

#### ¿Cómo se hacen controles de calidad de datos en Airflow?

Con los operadores de control SQL (`SQLColumnCheckOperator`, `SQLTableCheckOperator`, `SQLCheckOperator`), los operadores de Great Expectations o Soda, o las pruebas de dbt, ubicados después de las cargas para detener las tareas siguientes cuando los datos están mal.

#### ¿Por qué los DAG no deben depender de archivos locales entre tareas?

Las tareas pueden correr en workers o pods distintos, así que un archivo escrito por una tarea puede no existir para la siguiente. Usa almacenamiento de objetos, un volumen compartido o una base de datos.

#### ¿En cuántos DAG se debe dividir un pipeline?

Un DAG por cada programación y frontera de responsabilidad independientes. Divide cuando las partes tienen programaciones, responsables o dominios de fallo distintos, y conéctalas con assets; mantén en un solo DAG los pasos muy acoplados.

#### ¿Cómo se mantiene legible un DAG?

Con tareas pequeñas y bien nombradas, task groups para los bloques lógicos, nada de lógica de negocio en el archivo del DAG, documentación con `doc_md`, un uso coherente de TaskFlow u operadores y poca generación dinámica.

#### ¿Por qué fijar las versiones de los providers y las dependencias?

Las actualizaciones sin fijar pueden cambiar el comportamiento de los operadores o romper imports sin avisar. Fija las versiones con el archivo de constraints y actualiza de forma deliberada y con pruebas.

### Escenarios

#### Un DAG diario debe cargar los archivos de ayer desde S3 en Snowflake y luego ejecutar dbt. Diséñalo.

Un DAG diario con `catchup=False` (o true si importa el historial), un `S3KeySensor` diferible sobre el prefijo esperado del intervalo de datos, un `CopyFromExternalStageToSnowflakeOperator` o una tarea SQL que ejecute `COPY INTO`, luego dbt con Cosmos o un operador de dbt Cloud, controles de calidad de datos y callbacks de fallo hacia Slack. Todas las rutas y filtros salen del intervalo de datos.

#### Cientos de DAG tardan en programarse. ¿Qué investigas?

Los tiempos de análisis de los DAG (`airflow dags report`), el código y los imports de nivel superior, el número de archivos de DAG, la CPU del scheduler y el rendimiento de la base de datos, el número de task instances en la base (ejecuta `db clean`), y si el scheduler y el DAG processor tienen suficientes recursos o réplicas.

#### Un sensor espera un archivo que a veces nunca llega. ¿Cómo lo manejas?

Hago el sensor diferible o uso el modo `reschedule`, le pongo un timeout realista, decido si la ausencia debe fallar (avisar a alguien) u omitirse (`soft_fail`) y notifico al responsable del origen. Documento la hora de llegada esperada.

#### Una tarea falla al azar por el límite de solicitudes de una API. ¿Qué haces?

Añado reintentos con espera exponencial, pongo las llamadas a la API en un pool que limite la concurrencia, respeto `Retry-After` en el hook y reduzco las llamadas (agrupación, extracción incremental).

#### Hay que reprocesar seis meses de datos tras corregir un error. ¿Cómo?

Me aseguro de que las tareas sean idempotentes y usen el intervalo de datos, y luego creo un backfill para el rango de fechas con concurrencia limitada (`max_active_runs`) para no dejar sin recursos a la producción, o limpio los DAG runs afectados. Después monitoreo y valido las salidas.

#### Dos DAG escriben en la misma tabla y a veces entran en conflicto. ¿Cómo lo corriges?

Serializándolos: un pool de un solo slot para las escrituras en esa tabla, o fusionándolos en un solo DAG con un orden explícito, o haciendo que uno dependa del otro mediante un asset. Mejor todavía, dar a cada tabla un único proceso responsable.

#### ¿Cómo migrarías de Airflow 2 a Airflow 3?

Primero actualizo a la última 2.x y corrijo los avisos de obsolescencia, ejecuto las reglas `AIR3` de Ruff para encontrar el código que hay que cambiar (imports a `airflow.sdk`, `schedule_interval` a `schedule`, `execution_date` a `logical_date`, SubDAG y SLA eliminados, sin acceso directo a la base desde las tareas), pruebo en staging, migro la base de datos y actualizo el despliegue para el API server y el DAG processor.

#### ¿Cómo orquestarías un pipeline que combina AWS Glue, Databricks y un proyecto dbt?

Con un DAG (o varios DAG enlazados por assets) que use `GlueJobOperator` del provider de Amazon, `DatabricksRunNowOperator` del provider de Databricks y Cosmos o el operador de dbt Cloud, todos en modo diferible, pasando nombres de tablas o rutas, con controles de calidad entre los pasos y una sola configuración de alertas.

#### Tu persona de guardia recibe cada noche una alerta por la misma tarea inestable. ¿Qué cambias?

Busco la causa raíz en los logs (timeouts, límites de recursos, retrasos del origen), añado reintentos con espera solo para los errores transitorios, añado un sensor o una dependencia por asset si empieza antes de que su entrada esté lista, subo los recursos o la paso a un pool dedicado, y cambio las alertas para que solo salten cuando se agotan los reintentos.

#### Un DAG funciona en local pero en producción las tareas fallan con "module not found". ¿Por qué?

A la imagen o los workers de producción les falta la dependencia, o el módulo no está en la ruta (por ejemplo código fuera de la carpeta de DAG o de plugins). Añádelo a los requisitos de la imagen o a un paquete, y construye local y producción a partir de la misma imagen.

#### Las tareas suelen morir sin ningún error en los logs. ¿Qué sospechas?

Cierres por falta de memoria (OOM) del worker o del pod, desalojos o timeouts. Revisa los eventos de los pods y las métricas de los workers, sube los límites de memoria y saca el procesamiento pesado de Airflow.

#### Tu backfill creó duplicados en la tabla destino. ¿Qué salió mal?

Las tareas no eran idempotentes: añadían datos o usaban "ahora" en lugar del intervalo de datos. Reescribe la carga para sobrescribir la partición del intervalo o hacer `MERGE` por clave, borra los duplicados y vuelve a ejecutar.

#### Una persona de negocio quiere recibir un reporte por correo solo si las ventas de ayer están completas. ¿Cómo?

Programo el DAG del reporte sobre el asset de ventas (o con un sensor sobre la carga), añado un control de calidad (número de filas y completitud frente a los orígenes esperados), corto el envío del correo si los controles fallan y, en ese caso, alerto al equipo de datos.

#### ¿Cómo se dispara un DAG de Airflow cuando llega un archivo a S3, sin sondeo?

Con un asset watcher sobre una cola SQS que recibe las notificaciones de eventos de S3 (Airflow 3), o con un evento de S3 que lanza una función Lambda que llama a la API REST de Airflow para disparar el DAG con la ruta del archivo como configuración.

#### La CPU de tu scheduler está al 100 %. ¿Cuáles son las soluciones habituales?

Reducir la carga de análisis de los DAG (archivos más ligeros y menos numerosos, un `min_file_process_interval` más largo, un DAG processor separado), abandonar los sensores en modo poke, limpiar la base de datos, añadir réplicas del scheduler y revisar los DAG con cantidades enormes de tareas mapeadas.

#### ¿Cómo le explicarías Airflow a una persona no técnica?

Es el programador y controlador de tráfico de los procesos de datos de la empresa: arranca cada paso a la hora correcta y en el orden correcto, lo reintenta cuando algo falla momentáneamente y avisa al equipo cuando algo necesita a una persona.
