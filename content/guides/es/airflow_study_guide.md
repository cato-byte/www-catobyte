## Guía de estudio de Apache Airflow

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de Apache Airflow: unas 200 preguntas](../../images/airflow_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre Apache Airflow, desde los DAG y los operadores hasta la programación, los sensores, los assets, los executors, las pruebas, el despliegue y la resolución de problemas. Las respuestas siguen Airflow 3 y señalan lo que cambió respecto a Airflow 2, ya que muchas empresas todavía usan ambas versiones.

La guía sigue una ruta de aprendizaje en cinco etapas. Cada sección se divide en unidades cortas: objetivos de aprendizaje, una explicación del concepto y un ejemplo resuelto, luego preguntas (primero de memoria, después de aplicación), un reto práctico e ideas clave. Para **aprender**, lee cada unidad de principio a fin. Para **repasar**, cambia al modo repaso o usa "Ir a las preguntas", marca las respuestas que quieras volver a ver y prueba un repaso mixto entre secciones.

<!-- QA -->
<!-- stage: Fundamentos -->

### Fundamentos

<!-- unit: Para qué sirve Airflow -->

<!-- goals -->

- Explicar qué hace un orquestador y qué deja a otros sistemas.
- Comparar Airflow con cron, Dagster, Prefect y los servicios gestionados.

<!-- concept -->

Una plataforma de datos tiene muchos jobs que dependen entre sí: extraer antes de cargar, cargar antes de transformar, transformar antes de reportar. Algo tiene que arrancar cada job a tiempo, en orden, y reaccionar cuando uno falla. Eso es orquestación, distinta del procesamiento, que es el cálculo pesado que hacen motores como Spark o un warehouse.

Airflow es un orquestador. Como los pipelines se escriben en Python, heredan las prácticas de revisión, pruebas y despliegue de cualquier software. Sus alternativas difieren sobre todo en filosofía y en quién opera los servidores.

<!-- example -->

| Necesidad | cron | Airflow |
|---|---|---|
| Lanzar un comando a las 06:00 | Sí | Sí |
| Cargar solo si la extracción funcionó | No | Sí |
| Reintentar, alertar, ver historial y logs | No | Sí |
| Re-ejecutar marzo pasado para una tabla | Manual | Backfill |

#### ¿Qué es Apache Airflow?

Una plataforma de código abierto para escribir, programar y monitorear flujos de trabajo como código. Los flujos son DAG de tareas definidos en Python; Airflow los ejecuta según una programación o ante eventos, en el orden de sus dependencias, con reintentos, logs, alertas y una interfaz web. Nació en Airbnb en 2014 y es un proyecto de primer nivel de Apache.

#### ¿Para qué sirve Airflow y para qué no?

Sirve para orquestar flujos batch: ETL/ELT, lanzar jobs en otros sistemas (Spark, dbt, Databricks, Snowflake, Glue), pipelines de ML, reportes y mantenimiento. No es un motor de procesamiento de datos (el cálculo pesado debe ocurrir en los sistemas que lanza), ni un motor de streaming, ni está pensado para programaciones de altísima frecuencia por debajo del segundo.

#### ¿Qué significa "orquestación", frente a "procesamiento"?

La orquestación decide qué se ejecuta, cuándo, en qué orden y qué pasa ante un fallo. El procesamiento es el cálculo real sobre los datos. Airflow orquesta; Spark, los motores SQL y dbt procesan.

#### ¿Qué aporta escribir los flujos como código?

Control de versiones, revisión de código, pruebas, generación dinámica de tareas, reutilización mediante funciones y librerías Python, y la posibilidad de desplegar los flujos con CI/CD como cualquier otro software.

#### ¿Qué diferencia hay entre Airflow y cron?

Cron solo lanza comandos a ciertas horas. Airflow añade dependencias entre tareas, reintentos, backfills, historial, logs centralizados, alertas, parametrización, una interfaz e integración con sistemas externos.

#### ¿Cómo se compara Airflow con Dagster y Prefect?

Los tres orquestan flujos en Python. Airflow es el más desplegado y tiene el ecosistema de providers más grande. Dagster está centrado en assets (declaras los activos de datos y su linaje), con tipado fuerte y pruebas locales. Prefect se enfoca en flujos Python dinámicos con poco código repetitivo. Airflow 3 se acercó a las ideas de Dagster con los assets y el versionado.

#### ¿Qué servicios administrados de Airflow existen?

Amazon MWAA (Managed Workflows for Apache Airflow), Google Cloud Composer, Astronomer (Astro) y la oferta de Airflow de Azure en Data Factory/Fabric. Administran el scheduler, los workers, la base de datos y las actualizaciones.

#### ¿Cómo le explicarías Airflow a una persona no técnica?

Es el programador y controlador de tráfico de los procesos de datos de la empresa: arranca cada paso a la hora correcta y en el orden correcto, lo reintenta cuando algo falla momentáneamente y avisa al equipo cuando algo necesita a una persona.

<!-- challenge -->

Un equipo corre 30 jobs de cron en una VM y cada script espera 20 minutos "por si acaso" a que termine el anterior. Nombra dos problemas que Airflow resolvería y uno que no.

<!-- solution -->

Airflow reemplazaría las esperas por dependencias reales, así los jobs arrancan en cuanto sus entradas están listas, y agregaría reintentos, alertas e historial. No haría más rápidos los scripts: el procesamiento pesado sigue perteneciendo a los motores que las tareas invocan.

<!-- takeaways -->

- La orquestación decide qué corre y cuándo; el procesamiento hace el trabajo.
- Workflows como código traen revisión, pruebas y CI/CD a los pipelines.
- Airflow tiene el ecosistema más grande; las alternativas difieren en estilo y hosting.

<!-- unit: DAGs, tareas y ejecuciones -->

<!-- goals -->

- Distinguir DAGs, tareas, operadores, task instances y DAG runs.
- Leer los estados de ejecuciones y tareas, incluido `upstream_failed`.

<!-- concept -->

Airflow separa la definición de la ejecución. En código defines un DAG: tareas y dependencias. Cada vez que se programa, Airflow crea un DAG run y dentro una task instance por tarea. Los estados viven en estos objetos de ejecución, no en el código; por eso la misma tarea puede estar verde ayer y roja hoy.

Las dependencias mandan sobre los estados: una tarea arranca solo cuando sus tareas previas están en los estados que su trigger rule espera. Un fallo arriba aparece abajo como `upstream_failed`, y el estado final del DAG run se deriva de sus últimas tareas.

<!-- example -->

```text
DAG daily_sales (code)         DAG run 2026-10-17 (runtime)
 extract >> transform >> load   extract    success
                                transform  failed
                                load       upstream_failed  → run: failed
```

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

#### ¿Qué estados puede tener un DAG run?

`queued`, `running`, `success` y `failed`. El estado de un DAG run se deduce de sus tareas finales: tiene éxito si todas terminan bien o se omiten.

#### ¿Qué significa `upstream_failed`?

Que la tarea no se ejecutó porque una tarea anterior falló y no se pudo cumplir su trigger rule (por defecto `all_success`).

#### ¿Qué hace pausar un DAG?

Un DAG pausado no crea nuevas ejecuciones programadas; las tareas en curso terminan. Los DAG nuevos están pausados por defecto (`dags_are_paused_at_creation`) para que no empiecen a correr apenas se despliegan.

<!-- challenge -->

Despliegas un DAG nuevo con calendario diario, pero a la mañana siguiente no hay ejecuciones. ¿Cuál es la razón más probable y qué revisas?

<!-- solution -->

Los DAGs nuevos vienen pausados por defecto, así que el scheduler no crea ejecuciones. Reactívalo en la UI o con `airflow dags unpause`. Revisa también que no tenga errores de importación y que su `start_date` esté en el pasado.

<!-- takeaways -->

- Un DAG es código; los DAG runs y task instances son sus ejecuciones.
- Los estados pertenecen a task instances y DAG runs, no a tareas.
- `upstream_failed` te señala un fallo anterior en el grafo.

<!-- unit: Arquitectura y Airflow 3 -->

<!-- goals -->

- Describir los componentes de un despliegue de Airflow y qué guarda o ejecuta cada uno.
- Resumir qué cambió Airflow 3 para autores de DAGs y operadores.

<!-- concept -->

Airflow es un conjunto de servicios alrededor de una base de datos. El DAG processor convierte archivos en DAGs serializados, el scheduler decide qué toca, executors y workers corren tareas, el triggerer maneja esperas y el API server sirve la UI y la API REST. La base de metadatos es la memoria compartida: si se pierde, se pierde todo el estado.

Airflow 3 endureció esas fronteras: los workers ya no tocan la base directamente sino que pasan por una API, y los autores importan desde un SDK estable. Eso hace más seguras las actualizaciones y posible la ejecución remota.

<!-- example -->

```python
# Airflow 3: import everything from the stable Task SDK
from airflow.sdk import dag, task, Asset, Variable
```
```bash
airflow dags list-import-errors     # CLI for debugging
curl -X POST "$AIRFLOW/api/v2/dags/daily_sales/dagRuns" -d '{"logical_date": null}'
```

#### ¿Cuáles son los componentes principales de un despliegue de Airflow?

El scheduler (decide qué se ejecuta y cuándo), el DAG processor (analiza los archivos de DAG), el API server (sirve la interfaz y la API REST; en Airflow 2 era el webserver), el executor y sus workers (ejecutan las tareas), el triggerer (ejecuta las tareas diferidas) y la base de datos de metadatos (guarda el estado).

#### ¿Qué es la base de datos de metadatos?

Una base de datos relacional (PostgreSQL o MySQL en producción; SQLite solo para pruebas) que guarda los DAG runs, las task instances, las conexiones, las variables, los XCom, los usuarios y los DAG serializados. Es la fuente de verdad del estado de Airflow, así que hay que respaldarla y mantenerla.

#### ¿Cuáles son los mayores cambios de Airflow 3?

Una nueva interfaz en React, el versionado de los DAG (cada ejecución queda ligada a la versión del DAG con la que corrió), el Task SDK y una Task Execution API para que los workers ya no hablen directamente con la base de metadatos, `airflow api-server` en lugar del webserver, los datasets renombrados como assets con programación por eventos, los backfills gestionados por el scheduler, la eliminación de los SubDAG y los SLA, y `schedule` en lugar de `schedule_interval`.

#### ¿Qué es el Task SDK?

La interfaz pública y estable para escribir DAG en Airflow 3 (`from airflow.sdk import dag, task, DAG, Asset, Variable`). Desacopla el código de los DAG de los detalles internos de Airflow y permite ejecutar tareas de forma remota mediante la Task Execution API, e incluso en otros lenguajes en el futuro.

#### ¿Para qué se usa la CLI `airflow`?

Para administrar y depurar Airflow: `airflow dags list|trigger|pause|test`, `airflow tasks test|clear`, `airflow db migrate|clean`, los comandos `airflow connections` y `variables`, `airflow config get-value`, y para iniciar los componentes (`scheduler`, `api-server`, `dag-processor`, `triggerer`, `celery worker`).

#### ¿Qué ofrece la API REST?

Una API estable y versionada (servida por el API server) para disparar y administrar DAG runs, leer estados y logs de las task instances, administrar conexiones, variables y pools, y limpiar tareas. Los pipelines de CI y otros sistemas la usan para integrarse con Airflow.

<!-- challenge -->

Un sistema externo debe iniciar un DAG run al terminar una exportación nocturna. ¿Qué interfaz sugieres y qué necesita quien llama?

<!-- solution -->

La API REST para crear un DAG run, pasando parámetros en el cuerpo. Quien llama necesita credenciales con permiso para disparar ese DAG, idealmente una cuenta de servicio dedicada, y acceso de red al API server.

<!-- takeaways -->

- La base de metadatos guarda todo el estado; respáldala.
- Airflow 3 aísla a los workers tras una API y expone un Task SDK estable.
- La CLI para depurar; la API REST para integraciones.

<!-- unit: Conectarse con otros sistemas -->

<!-- goals -->

- Explicar cómo encajan providers, hooks y connections.
- Decidir cuándo usar Variables y cuándo no.

<!-- concept -->

Airflow habla con el mundo por capas. Un provider trae todo lo de un sistema. Dentro, los hooks saben abrir una sesión y llamar al sistema, y los operadores usan hooks para una unidad de trabajo. Los hooks toman host y credenciales de connections, buscadas por `conn_id`, así el código no contiene secretos y el mismo DAG funciona en cada entorno.

Las Variables cubren el resto de la configuración. Son cómodas, pero cada lectura puede ir a la base de datos, así que van dentro de las tareas, no en el nivel superior del archivo del DAG.

<!-- example -->

```python
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

@task
def list_new_files(prefix: str) -> list[str]:
    hook = S3Hook(aws_conn_id="aws_data")       # credentials come from the connection
    return hook.list_keys(bucket_name="landing", prefix=prefix)
```

#### ¿Qué es un provider de Airflow?

Un paquete con versión propia que añade operadores, hooks, sensores y conexiones para un sistema externo: `apache-airflow-providers-amazon`, `-google`, `-databricks`, `-snowflake`, `-postgres`, `-standard` (los operadores básicos como `BashOperator` y `PythonOperator` en Airflow 3) y muchos más.

#### ¿Qué es un hook?

Una clase que encapsula la conexión a un sistema externo y ofrece métodos de ayuda, como `S3Hook.load_file()` o `PostgresHook.get_records()`. Los operadores usan hooks internamente; también puedes usarlos en tus propias tareas Python.

#### ¿Qué es una conexión?

Un conjunto guardado de credenciales y parámetros de un sistema externo (host, usuario, contraseña, esquema, puerto, JSON extra), referenciado por un `conn_id`. Puede guardarse en la base de metadatos, en variables de entorno (`AIRFLOW_CONN_<ID>`) o en un secrets backend.

#### ¿Qué son las Variables de Airflow?

Valores de configuración clave-valor guardados en Airflow (base de metadatos, variables de entorno `AIRFLOW_VAR_<NOMBRE>` o un secrets backend) y leídos con `Variable.get()`. Leerlos en el nivel superior de un archivo de DAG provoca una llamada a la base o al backend en cada análisis, así que hay que leerlos dentro de las tareas o con plantillas.

<!-- challenge -->

Un DAG tiene escrita una contraseña de Postgres y lee cinco Variables en el nivel superior del archivo. ¿Qué cambias?

<!-- solution -->

Pasar la contraseña a una connection (guardada en un secrets backend) y usar el hook de Postgres con su `conn_id`. Leer las Variables dentro de las tareas que las necesitan, o pasarlas por plantillas, para que el parseo no consulte la base.

<!-- takeaways -->

- Los providers empaquetan hooks, operadores y sensores de un sistema.
- Las connections sacan las credenciales del código; los hooks las usan.
- Lee las Variables al ejecutar, no al parsear.

### Escribir DAG

<!-- unit: Definir DAGs y tareas -->

<!-- goals -->

- Escribir un DAG con tareas TaskFlow y operadores clásicos.
- Expresar dependencias, fan-out y agrupaciones.

<!-- concept -->

Hay dos maneras de crear tareas y se combinan libremente. Los operadores clásicos son objetos configurados; las funciones TaskFlow son Python decorado con `@task`. Con TaskFlow, pasar el retorno de una tarea a otra mueve el dato y crea la dependencia, así el grafo sigue al código. Cuando no hay datos que pasar, dibujas las aristas tú con `>>`.

Los task groups mantienen legibles los grafos grandes sin cambiar cómo corren las tareas.

<!-- example -->

```python
from airflow.sdk import dag, task
from airflow.providers.standard.operators.bash import BashOperator

@dag(schedule="@daily", start_date=datetime(2026, 1, 1), catchup=False)
def daily_sales():
    @task
    def extract() -> list[dict]: ...
    @task
    def load(rows: list[dict]): ...
    notify = BashOperator(task_id="notify", bash_command="echo done")
    load(extract()) >> notify       # data edge + explicit edge

daily_sales()
```

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

#### ¿Qué diferencia hay entre `@task` y `PythonOperator`?

Ambos ejecutan una función Python. `@task` (TaskFlow) es más conciso, pasa los valores devueltos por XCom automáticamente y deduce las dependencias. `PythonOperator` es la forma clásica; el XCom y las dependencias se conectan a mano. Se pueden mezclar en un DAG.

#### ¿Cómo se mezclan tareas TaskFlow y operadores clásicos?

Los operadores clásicos exponen `.output` (un `XComArg`) que se puede pasar a funciones TaskFlow, y las salidas de TaskFlow se pueden pasar a los campos con plantilla de los operadores clásicos. Las dependencias se deducen de esos vínculos.

#### ¿Cómo se definen las dependencias entre tareas?

Con los operadores de desplazamiento de bits (`extract >> transform >> load`), listas para abrir y cerrar ramas (`start >> [a, b] >> end`), las funciones `chain()` y `cross_downstream()`, o de forma implícita al pasar las salidas de TaskFlow como argumentos.

#### ¿Qué es un task group?

Una forma de agrupar tareas visual y lógicamente en la interfaz (`@task_group` o `TaskGroup`), con un prefijo común para los IDs de las tareas y argumentos por defecto compartidos. Reemplazó a los SubDAG, que se eliminaron en Airflow 3.

<!-- challenge -->

Diez tablas se cargan con pares idénticos de extraer-luego-cargar, y todas deben terminar antes de una tarea de resumen. Bosqueja las dependencias.

<!-- solution -->

Un task group por tabla (extract >> load) y luego `[group_1, ..., group_10] >> summary`. Generar los grupos en un bucle sobre la lista de tablas lo deja en pocas líneas.

<!-- takeaways -->

- TaskFlow pasa datos y dependencias en una sola llamada.
- Usa `>>`, listas y `chain()` cuando no hay datos que pasar.
- Los task groups organizan el grafo; no cambian la ejecución.

<!-- unit: Configuración a nivel de DAG -->

<!-- goals -->

- Definir valores por defecto, responsables y documentación para todas las tareas.
- Elegir bien `start_date`, `catchup` y los parámetros.

<!-- concept -->

La mayoría de los ajustes son iguales para todas las tareas de un DAG, así que van en un solo lugar. `default_args` guarda reintentos, responsable y alertas; el DAG guarda calendario, fecha de inicio y catchup. Estas decisiones definen el primer despliegue: una fecha de inicio pasada con catchup puede lanzar cientos de ejecuciones de golpe.

Responsable, tags y documentación no cuestan nada y rinden en los incidentes, cuando alguien que no escribió el DAG necesita saber qué hace y a quién llamar. Los params hacen seguras las ejecuciones manuales validando la entrada.

<!-- example -->

```python
default_args = {"owner": "sales-data", "retries": 2, "retry_delay": timedelta(minutes=5)}

@dag(schedule="0 6 * * *", start_date=datetime(2026, 1, 1), catchup=False,
     default_args=default_args, tags=["sales"], doc_md=__doc__,
     params={"full_refresh": Param(False, type="boolean")})
def sales_load(): ...
```

#### ¿Qué son los `default_args`?

Un diccionario de argumentos aplicado a todas las tareas de un DAG, como `owner`, `retries`, `retry_delay`, `email_on_failure` o `execution_timeout`. Las tareas pueden sobrescribirlos.

#### ¿Cómo se define un owner y por qué importa?

Con `owner` en `default_args`. Aparece en la interfaz y en las alertas, así que se contacta al equipo correcto cuando el DAG falla.

#### ¿Qué es `email_on_failure`?

Un argumento de tarea que envía un correo cuando la tarea falla, usando la configuración SMTP. La mayoría de los equipos prefiere callbacks o notifiers hacia Slack o PagerDuty, con alertas más completas y enrutables.

#### ¿Para qué sirven las etiquetas y `doc_md`?

Las etiquetas agrupan y filtran los DAG en la interfaz. `doc_md` añade documentación en Markdown al DAG o a una tarea, visible en la interfaz, lo que ayuda a la persona de guardia a entender qué hace un DAG.

#### ¿Qué significa `start_date`?

La fecha a partir de la cual se puede programar el DAG. Debe ser una fecha fija en el pasado, nunca `datetime.now()`, que cambiaría en cada análisis e impediría crear ejecuciones.

#### ¿Qué es `catchup`?

Si el scheduler crea ejecuciones para todos los intervalos perdidos entre `start_date` (o la última ejecución) y ahora. En Airflow 3 el valor por defecto es `False`; en Airflow 2 era `True`. Dejar catchup activo en un DAG con una fecha de inicio antigua puede lanzar cientos de ejecuciones a la vez.

#### ¿Cómo se pasan parámetros a un DAG run?

Con `params` declarados en el DAG (con valores por defecto y validación opcional con JSON Schema), que aparecen como un formulario al disparar manualmente y se leen con `{{ params.nombre }}` o desde el contexto.

<!-- challenge -->

Un DAG usa `start_date=datetime.now()`. Las ejecuciones nunca aparecen, o aparecen a horas raras. ¿Por qué y cuál es el arreglo?

<!-- solution -->

La fecha de inicio cambia en cada parseo, así que el scheduler nunca ve un intervalo completo después de ella. Usa una fecha fija en el pasado, `catchup=False` salvo que necesites historia, y deja que el calendario decida.

<!-- takeaways -->

- Pon la configuración compartida de tareas en `default_args`.
- Usa un `start_date` fijo en el pasado; decide `catchup` a propósito.
- Responsables, tags, docs y params facilitan operar los DAGs.

<!-- unit: Controlar el flujo -->

<!-- goals -->

- Usar trigger rules, branches y short-circuits para controlar qué corre.
- Garantizar la limpieza con tareas de setup y teardown.

<!-- concept -->

Por defecto una tarea corre solo si todo lo anterior tuvo éxito. Los pipelines reales necesitan más: saltar trabajo si no hay datos, elegir un camino entre varios, limpiar incluso tras un fallo. Cada herramienta cambia qué tareas se saltan o qué estados previos acepta una tarea.

La trampa es que los saltos se propagan. Tras un branch, la tarea de unión necesita una trigger rule que tolere padres saltados, o también se saltará. Los pares setup/teardown hacen explícita la limpieza para que una ejecución fallida no deje clusters encendidos.

<!-- example -->

```python
@task.branch
def choose(**context):
    return "full_load" if context["params"]["full_refresh"] else "incremental_load"

join = EmptyOperator(task_id="join", trigger_rule="none_failed_min_one_success")
choose() >> [full_load, incremental_load] >> join
```

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

#### ¿Qué son `@setup` y `@teardown`?

Decoradores que marcan las tareas que crean y limpian recursos (un cluster, una tabla temporal). Un teardown se ejecuta aunque falle el trabajo intermedio, y limpiar una tarea también vuelve a ejecutar su setup y su teardown.

<!-- challenge -->

Un DAG crea un cluster temporal, corre tres jobs en él y lo borra. Cuando un job falla, el cluster queda encendido. Arréglalo.

<!-- solution -->

Marca la tarea de creación con `@setup` y la de borrado con `@teardown`, enlazadas. El teardown corre pase lo que pase con los jobs, y el DAG run sigue reportando el fallo.

<!-- takeaways -->

- Las trigger rules deciden qué estados previos dejan correr una tarea.
- Las uniones tras un branch necesitan una regla que tolere saltos.
- Setup y teardown garantizan la limpieza.

<!-- unit: Límites de ejecución y aislamiento -->

<!-- goals -->

- Acotar cuánto duran y cuántas veces corren tareas y ejecuciones.
- Aislar dependencias y evitar comandos de shell inseguros.

<!-- concept -->

Una tarea que se cuelga, se solapa con la ejecución de ayer o choca con las librerías de Airflow puede hacer más daño que una que falla. Los timeouts convierten cuelgues en fallos claros. Los límites de ejecuciones y `depends_on_past` evitan que se solapen ejecuciones que modifican los mismos datos. Los entornos aislados permiten librerías que Airflow no puede instalar.

Los comandos de shell son el lugar más fácil para inyecciones y lógica escondida: mantenlos cortos y nunca metas entradas no confiables en ellos.

<!-- example -->

```python
@task.virtualenv(requirements=["pandas==2.2.3"], system_site_packages=False,
                 execution_timeout=timedelta(minutes=30))
def score(path: str):
    import pandas as pd       # imports inside the function
    ...
```

#### ¿Cómo se define un timeout en una tarea?

Con `execution_timeout` (un `timedelta`); la tarea falla cuando dura más. Un `dagrun_timeout` a nivel de DAG hace fallar toda la ejecución tras cierta duración.

#### ¿Qué hace `max_active_runs`?

Limita cuántas ejecuciones de un DAG pueden estar activas a la vez. Ponerlo en 1 garantiza que las ejecuciones sean secuenciales, algo importante en los pipelines que dependen de la salida de la ejecución anterior.

#### ¿Qué es `depends_on_past`?

Un argumento de tarea: si es `True`, una task instance solo se ejecuta si la misma tarea tuvo éxito (o se omitió) en el DAG run anterior. Impone un procesamiento secuencial a nivel de tarea.

#### ¿Cómo se ejecuta una tarea en un entorno Python aislado?

Con `@task.virtualenv` (crea un virtualenv con los requisitos indicados), `@task.external_python` (usa un intérprete existente), `@task.docker` o `@task.kubernetes` (se ejecuta en un contenedor). Así se evitan conflictos de dependencias con el propio Airflow.

#### ¿Para qué se usa el `BashOperator` y cuál es el riesgo?

Para ejecutar comandos o scripts de shell. El riesgo es meter en el comando entradas no confiables mediante plantillas (inyección) y esconder lógica compleja en shell, donde es difícil de probar.

<!-- challenge -->

Un DAG diario actualiza totales acumulados del día anterior. La ejecución de ayer fue lenta, la de hoy arrancó igual y los totales quedaron mal. ¿Qué dos ajustes lo evitan?

<!-- solution -->

`max_active_runs=1` para que las ejecuciones nunca se solapen, y `depends_on_past=True` en la tarea de actualización para que espere a que la instancia del día anterior termine bien. Agrega `execution_timeout` para que un cuelgue falle en vez de bloquear para siempre.

<!-- takeaways -->

- Los timeouts convierten cuelgues silenciosos en fallos visibles.
- `max_active_runs` y `depends_on_past` imponen orden entre ejecuciones.
- Aísla dependencias en conflicto; mantén cortos los comandos de shell.

<!-- unit: Mantener sanos los archivos de DAG -->

<!-- goals -->

- Mantener el parseo de DAGs rápido y predecible.
- Generar DAGs y tareas dinámicamente sin sorpresas.

<!-- concept -->

Airflow relee los archivos de DAG todo el tiempo, así que un archivo de DAG es código que corre mucho más que sus tareas. Todo lo que está en el nivel superior (una consulta, una llamada a una API, un import pesado) se ejecuta en cada parseo y ralentiza el scheduling para todos.

La generación dinámica es potente si las entradas son baratas y estables, como un YAML en el repositorio. La estabilidad importa porque los IDs son identidad: renombrar una tarea o un DAG empieza una historia nueva.

<!-- example -->

```python
# tables.yaml lives next to the DAG: cheap to read at parse time
for table in yaml.safe_load(open(CONFIG))["tables"]:
    @task(task_id=f"load_{table}")
    def load(name=table): ...
    load()
```

#### ¿Por qué el nivel superior de los archivos de DAG debe ser ligero?

El DAG processor analiza cada archivo de DAG una y otra vez (cada 30 segundos por defecto para los archivos modificados). El código de nivel superior, como consultas a bases de datos, llamadas a APIs, `Variable.get()` o imports pesados, se ejecuta en cada análisis, ralentiza todo el scheduler y golpea los sistemas externos. Ese trabajo va dentro de las tareas.

#### ¿Cómo se generan DAG o tareas de forma dinámica?

Con un bucle en Python sobre una configuración (una lista, un YAML leído del disco) para crear tareas o varios DAG al analizar el archivo, o con el mapeo dinámico de tareas para abrir ramas en tiempo de ejecución. Mantén la configuración estática y barata de leer para que el análisis siga siendo rápido y determinista.

#### ¿Qué pasa cuando cambias el nombre de una tarea o de un DAG?

Airflow lo trata como una tarea o un DAG nuevo: el historial queda bajo el nombre antiguo. En Airflow 3 el versionado de DAG muestra el cambio, pero renombrar sigue rompiendo la continuidad de las métricas y de `depends_on_past`.

<!-- challenge -->

Un archivo de DAG arma su lista de tareas consultando el warehouse por todas las tablas en el nivel superior. El scheduling se volvió lento. ¿Qué cambias?

<!-- solution -->

Saca la consulta del parseo: escribe la lista de tablas en un archivo de configuración durante el CI o en una tarea aparte, lee ese archivo al parsear, o usa dynamic task mapping para que una tarea obtenga la lista al ejecutar.

<!-- takeaways -->

- El código de nivel superior corre en cada parseo; mantenlo trivial.
- Genera tareas desde configuración barata y versionada.
- Los IDs de tareas y DAGs son identidad; renombrar empieza otra historia.

<!-- stage: Calendarios y flujo de datos -->

### Programación y tiempo

<!-- unit: Calendarios y timetables -->

<!-- goals -->

- Expresar calendarios con cron, presets, timedeltas y timetables.
- Manejar zonas horarias y cambios de horario de verano.

<!-- concept -->

Un calendario responde una pregunta: ¿cuándo crear una ejecución nueva? Los cron y presets cubren casi todo. Cuando la regla depende de un calendario (días hábiles, festivos, meses fiscales), un timetable la expresa en Python, en vez de una ejecución que arranca y se salta a sí misma.

Las zonas horarias añaden un matiz. Airflow guarda todo en UTC, pero las personas piensan en hora local. Un DAG con zona local sigue el reloj local, lo que significa que algunas horas locales ocurren dos veces o ninguna en los días de cambio de horario.

<!-- example -->

```python
import pendulum
@dag(schedule="0 6 * * 1-5",                     # 06:00 Monday to Friday
     start_date=pendulum.datetime(2026, 1, 1, tz="America/Bogota"),
     catchup=False)
def weekday_report(): ...
```

#### ¿Cómo se programa un DAG?

Con el argumento `schedule`: una expresión cron (`"0 6 * * *"`), un preset (`"@daily"`, `"@hourly"`), un `timedelta`, un timetable, una lista de assets (por eventos) o `None` para los DAG manuales o disparados desde fuera.

#### ¿Qué es el preset `@once`?

Una programación que crea una sola ejecución, útil para DAG puntuales como migraciones.

#### ¿Cómo se ejecuta un DAG solo los días hábiles?

Con una expresión cron como `0 6 * * 1-5`, o con un timetable propio si importan los festivos. Una tarea de rama o de cortocircuito también puede omitir el procesamiento en festivos según una tabla de calendario.

#### ¿Qué es un timetable?

Una clase que define una programación personalizada cuando cron no basta: solo días hábiles, varias horas distintas según el día, calendarios fiscales. Los incluidos son `CronDataIntervalTimetable`, `CronTriggerTimetable`, `DeltaDataIntervalTimetable` y `MultipleCronTriggerTimetable`.

#### ¿Cómo maneja Airflow las zonas horarias?

Internamente todo se guarda en UTC. Puedes dar a un DAG un `start_date` con zona horaria (con `pendulum`), y las programaciones cron siguen esa zona, incluidos los cambios de horario de verano. La interfaz puede mostrar la hora local.

#### ¿Cómo afectan los cambios de horario de verano a las programaciones?

Con una fecha de inicio con zona horaria, un cron diario a las 02:30 puede omitirse o ejecutarse dos veces en los días de cambio, según el reloj local. Programa los jobs críticos fuera de la franja de 01:00 a 03:00 o en UTC. (En Colombia no hay horario de verano, pero sí en muchas zonas de origen de los datos.)

<!-- challenge -->

Un equipo europeo programa un reporte a las 02:30 hora local. Dos veces al año se porta mal. ¿Qué pasa y qué sugieres?

<!-- solution -->

En el cambio de primavera las 02:30 no existen y en otoño ocurren dos veces, así que la ejecución se salta o se duplica según el reloj. Programa fuera de esa ventana (por ejemplo a las 04:00) o en UTC si el negocio lo acepta.

<!-- takeaways -->

- Cron y presets cubren casi todo; los timetables, calendarios especiales.
- Airflow guarda UTC; un start_date con zona sigue la hora local.
- Evita programar dentro de las horas de cambio de horario.

<!-- unit: Fechas lógicas e intervalos de datos -->

<!-- goals -->

- Explicar por qué una ejecución diaria arranca después del día que procesa.
- Usar el intervalo de datos en vez de la hora actual en las tareas.

<!-- concept -->

Las ejecuciones programadas tratan sobre periodos de datos, no momentos del reloj. Una ejecución diaria cubre un día completo, así que solo puede arrancar cuando ese día terminó; por eso parece "un día tarde". La fecha lógica y el intervalo de datos le dicen a la tarea qué periodo le corresponde.

Ese diseño es lo que hace correctas las re-ejecuciones: una tarea que lee su intervalo del contexto procesa los mismos datos cuando sea que corra. Una que pregunta la hora actual procesa un periodo distinto en cada reintento o backfill.

<!-- example -->

```sql
-- templated SQL: always the run's own day
DELETE FROM sales_daily WHERE sale_date = '{{ ds }}';
INSERT INTO sales_daily
SELECT * FROM raw_sales
WHERE sold_at >= '{{ data_interval_start }}' AND sold_at < '{{ data_interval_end }}';
```

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

#### ¿Por qué las tareas no deben usar `datetime.now()`?

Porque las reejecuciones y los backfills procesarían el periodo equivocado. Usa la fecha lógica o el intervalo de datos del contexto o de las plantillas.

#### ¿Cómo se pasa a una tarea la fecha de la última ejecución exitosa?

Con las variables de plantilla `prev_data_interval_start_success` y `prev_data_interval_end_success` (o `prev_start_date_success`), útiles en cargas incrementales que deben continuar desde el último punto exitoso.

#### ¿Qué pasa si una ejecución dura más que el intervalo de programación?

La siguiente ejecución empieza a su hora si `max_active_runs` lo permite, así que las ejecuciones pueden solaparse. Usa `max_active_runs=1` (y posiblemente `depends_on_past=True`) cuando no deban solaparse.

<!-- challenge -->

Un DAG horario filtra `WHERE updated_at > now() - interval '1 hour'`. Tras una caída, las re-ejecuciones no cargan nada. Reescribe la lógica del filtro.

<!-- solution -->

Filtra por el intervalo de la ejecución: `updated_at >= data_interval_start AND updated_at < data_interval_end`, pasado por plantillas. Cada re-ejecución recarga exactamente su hora, sin importar cuándo corra.

<!-- takeaways -->

- Una ejecución procesa su intervalo de datos, cuando este termina.
- Toma las fechas del contexto, nunca del reloj.
- Las ejecuciones largas pueden solaparse; limítalas cuando importa.

<!-- unit: Backfills, re-ejecuciones e idempotencia -->

<!-- goals -->

- Elegir entre catchup, backfills, limpiar tareas y disparos manuales.
- Hacer las tareas idempotentes para que reprocesar sea seguro.

<!-- concept -->

Los pipelines se re-ejecutan todo el tiempo: por bugs, caídas, datos tardíos o cambios de lógica. Airflow ofrece varias formas, desde limpiar una tarea hasta hacer backfill de meses, pero todas asumen lo mismo: correr una tarea dos veces para el mismo intervalo deja el mismo resultado.

Esa propiedad, la idempotencia, sale de cómo escribes la carga, no de Airflow. Sobrescribe o fusiona el tramo del intervalo en vez de agregar, y usa el intervalo en vez del reloj. Así reprocesar se vuelve rutina y no un proyecto de limpieza.

<!-- example -->

```bash
# reprocess Q1 with at most 4 concurrent runs
airflow backfill create --dag-id sales_load \
  --from-date 2026-01-01 --to-date 2026-03-31 --max-active-runs 4
```

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

#### Hay que reprocesar seis meses de datos tras corregir un error. ¿Cómo?

Me aseguro de que las tareas sean idempotentes y usen el intervalo de datos, y luego creo un backfill para el rango de fechas con concurrencia limitada (`max_active_runs`) para no dejar sin recursos a la producción, o limpio los DAG runs afectados. Después monitoreo y valido las salidas.

#### Tu backfill creó duplicados en la tabla destino. ¿Qué salió mal?

Las tareas no eran idempotentes: añadían datos o usaban "ahora" en lugar del intervalo de datos. Reescribe la carga para sobrescribir la partición del intervalo o hacer `MERGE` por clave, borra los duplicados y vuelve a ejecutar.

<!-- challenge -->

Una tarea agrega los pedidos de cada día a una tabla con `INSERT INTO`. Debes re-ejecutar la semana pasada. ¿Qué cambias primero?

<!-- solution -->

Hacer idempotente la carga: borrar las filas del intervalo e insertar en una transacción, usar `MERGE` por la clave del pedido o sobrescribir la partición de la fecha. Luego hacer backfill de la semana con concurrencia limitada.

<!-- takeaways -->

- El catchup es automático; backfills y clears son explícitos.
- La idempotencia viene de sobrescribir o fusionar por intervalo.
- Haz idempotentes las cargas antes de cualquier backfill.

### Operadores, sensores y tareas diferibles

<!-- unit: Sensores y esperas entre DAGs -->

<!-- goals -->

- Configurar sensores con el modo y timeout adecuados.
- Elegir entre dependencias de tipo pull y push entre DAGs.

<!-- concept -->

Los pipelines esperan cosas ajenas: un archivo, una partición, el DAG de otro equipo. Los sensores convierten esa espera en una tarea con una condición de éxito. El costo es un slot de worker mientras dure la espera, salvo que el sensor lo libere entre chequeos.

Entre DAGs puedes esperar (un sensor en el DAG de abajo hace pull) o disparar (un operador en el DAG de arriba hace push). El pull mantiene independientes a los equipos pero acopla calendarios; el push quita la espera pero obliga al DAG de arriba a conocer a sus consumidores.

<!-- example -->

```python
wait = S3KeySensor(
    task_id="wait_for_orders",
    bucket_key="s3://landing/orders/{{ ds }}/_SUCCESS",
    mode="reschedule", poke_interval=300, timeout=6 * 3600,
)
```

#### ¿Qué es un sensor?

Un operador especial que espera una condición: un archivo en S3 (`S3KeySensor`), una partición, una tarea externa, una consulta SQL que devuelve filas, un endpoint HTTP, una hora. Comprueba periódicamente hasta que la condición se cumple o vence el timeout.

#### ¿Qué diferencia hay entre los modos `poke` y `reschedule`?

En modo `poke` el sensor ocupa un slot de worker durante toda la espera, durmiendo entre comprobaciones. En modo `reschedule` libera el slot entre comprobaciones y se vuelve a programar más tarde, lo que es mejor para esperas largas. El modo diferible es todavía mejor.

#### ¿Qué es el timeout de un sensor y por qué definirlo?

El tiempo máximo que espera un sensor antes de fallar (`timeout`, siete días por defecto). Ponle un valor realista para que la falta de un archivo de origen se note rápido en lugar de bloquear recursos durante días. `soft_fail=True` marca el sensor como omitido en lugar de fallido.

#### ¿Qué es `@task.sensor`?

Un decorador que convierte una función Python en un sensor: devuelve `True` (o un `PokeReturnValue`) cuando se cumple la condición, con las opciones habituales `poke_interval`, `timeout` y `mode`.

#### ¿Qué es `ExternalTaskSensor`?

Un sensor que espera a que una tarea o un DAG run de otro DAG llegue a un estado, por defecto para la misma fecha lógica. Crea dependencias entre DAG, pero acopla las programaciones; los assets suelen ser una alternativa más limpia.

#### ¿Qué es `TriggerDagRunOperator`?

Un operador que dispara otro DAG, opcionalmente pasándole una configuración y esperando a que termine. Es una dependencia de tipo "empujar", frente al `ExternalTaskSensor`, que "jala".

<!-- challenge -->

Veinte sensores en modo `poke` esperan hasta siete días cada uno por archivos de socios. Los workers suelen estar llenos. ¿Qué cambias?

<!-- solution -->

Pasar los sensores a modo deferrable, o al menos `reschedule`, para que liberen el slot mientras esperan. Bajar el timeout a una ventana realista, como seis horas, y alertar cuando expire.

<!-- takeaways -->

- Los sensores esperan condiciones; su modo define el costo en slots.
- Pon siempre un timeout realista.
- Los enlaces entre DAGs pueden ser pull (sensor) o push (disparo).

<!-- unit: Diferir en vez de esperar -->

<!-- goals -->

- Explicar cómo los operadores deferrable liberan slots de workers.
- Manejar entradas que quizá nunca lleguen.

<!-- concept -->

La mayoría de las esperas no necesitan CPU: revisar el estado de un job cada minuto es barato, pero ocupar un proceso de worker para eso no. Los operadores deferrable le pasan la espera al triggerer, un servicio asíncrono que vigila miles de condiciones a la vez, y vuelven a un worker solo cuando algo pasó.

Diferir arregla el costo, no la semántica. Tú sigues decidiendo qué significa la ausencia: fallar y alertar, o saltar porque no haber datos es un resultado válido.

<!-- example -->

```python
run = DatabricksRunNowOperator(
    task_id="run_job", job_id=1234,
    deferrable=True,          # waits in the triggerer, not on a worker
)
```

#### ¿Qué son los operadores diferibles?

Operadores que, mientras esperan algo externo (un job, un archivo, una hora), se suspenden y delegan la espera a un trigger asíncrono que corre en el proceso triggerer, liberando el slot del worker. Cuando el trigger se activa, la tarea continúa en un worker. Muchos operadores de providers tienen `deferrable=True`.

#### ¿Qué es el triggerer?

Un componente que ejecuta los triggers basados en asyncio de las tareas diferidas. Un solo triggerer puede atender miles de esperas a la vez con pocos recursos.

#### Un sensor espera un archivo que a veces nunca llega. ¿Cómo lo manejas?

Hago el sensor diferible o uso el modo `reschedule`, le pongo un timeout realista, decido si la ausencia debe fallar (avisar a alguien) u omitirse (`soft_fail`) y notifico al responsable del origen. Documento la hora de llegada esperada.

<!-- challenge -->

Tras una actualización, las tareas deferrable se quedan para siempre en estado `deferred`. ¿Qué componente revisas primero?

<!-- solution -->

El triggerer. Las tareas diferidas solo se reanudan cuando un triggerer en ejecución dispara su trigger, así que revisa que el servicio esté desplegado, sano y con los providers instalados, y mira sus logs.

<!-- takeaways -->

- Diferir lleva las esperas de los workers al triggerer.
- Sin triggerer corriendo, las tareas diferidas no se reanudan.
- Decide explícitamente si la falta de datos falla o salta.

<!-- unit: Operadores de datos y APIs -->

<!-- goals -->

- Ejecutar SQL y llamadas HTTP desde Airflow con connections.
- Saber cuándo ayudan los operadores de transferencia y cuándo estorban.

<!-- concept -->

Muchas tareas son envoltorios finos de una llamada a otro sistema: correr este SQL, llamar esa API, copiar este archivo. Los operadores de los providers hacen la llamada y reutilizan una connection para las credenciales, así la tarea solo necesita parámetros, a menudo con plantillas de las fechas de la ejecución.

El riesgo es pasar los datos por el worker. Los operadores de transferencia sirven para volúmenes modestos, pero los movimientos grandes deben ocurrir dentro de los sistemas, como un `COPY` en el warehouse o un `UNLOAD` de Athena.

<!-- example -->

```python
SQLExecuteQueryOperator(
    task_id="build_daily",
    conn_id="warehouse",
    sql="sql/build_daily.sql",                 # templated with {{ ds }}
)
```

#### ¿Cómo se llama a una base de datos SQL desde Airflow?

Con `SQLExecuteQueryOperator` (provider common SQL) y una conexión, o con el hook específico del provider en una tarea Python. Guarda el SQL en archivos `.sql` aparte, referenciados mediante plantillas.

#### ¿Qué son los operadores de transferencia?

Operadores que mueven datos entre dos sistemas en una sola tarea, como `S3ToRedshiftOperator`, `GCSToBigQueryOperator`, `SqlToS3Operator` o `S3ToSnowflakeOperator`. Por lo general delegan el trabajo al sistema destino (por ejemplo con un comando `COPY`).

#### ¿Para qué se usa `HttpOperator`?

Para llamar a APIs HTTP con una conexión que define la URL base y las credenciales, con comprobaciones de la respuesta y paginación opcionales. `HttpSensor` espera a que un endpoint devuelva una condición.

#### ¿Cómo se ejecuta una consulta de Athena desde Airflow?

Con `AthenaOperator`, que envía la consulta, espera a que termine y escribe los resultados en la ubicación de salida de S3 configurada. Usa fechas con plantilla en la consulta para procesar el intervalo de datos.

<!-- challenge -->

Un `SqlToS3Operator` exporta una tabla de 200 GB cada noche y el worker se queda sin memoria. ¿Qué cambias?

<!-- solution -->

Que la base haga la exportación: usar su comando nativo de unload o export (por ejemplo `UNLOAD` en Redshift o `COPY INTO` una ubicación en Snowflake) desde un operador SQL. El worker solo emite el comando y espera.

<!-- takeaways -->

- Operadores más connections dejan las tareas en parámetros.
- Mantén el SQL en archivos versionados con plantillas.
- Los movimientos grandes de datos van dentro de los sistemas de datos.

<!-- unit: Disparar motores externos -->

<!-- goals -->

- Lanzar trabajo en Databricks, dbt, Glue y Kubernetes desde Airflow.
- Combinar varios motores en un pipeline.

<!-- concept -->

Airflow brilla como director de otros motores. Cada motor tiene un operador que envía el trabajo, espera (idealmente diferido) e informa éxito o fallo, así el DAG se lee como un plan mientras el cálculo ocurre en otro lado.

Cuando el trabajo tiene dependencias que el entorno de Airflow no soporta, correrlo en un contenedor (un pod o un virtualenv) lo aísla. La pregunta de diseño es siempre la misma: ¿cuál es la unidad de reintento y dónde quedan los logs?

<!-- example -->

```python
glue = GlueJobOperator(task_id="ingest", job_name="orders_ingest", deferrable=True)
spark = DatabricksRunNowOperator(task_id="enrich", job_id=1234, deferrable=True)
dbt = DbtTaskGroup(group_id="marts", project_config=ProjectConfig(DBT_DIR))  # Cosmos
glue >> spark >> dbt
```

#### ¿Cómo se lanza un job de Databricks desde Airflow?

Con `DatabricksRunNowOperator` (ejecuta un job existente por su ID, con parámetros) o `DatabricksSubmitRunOperator` (envía una ejecución puntual), del provider de Databricks, normalmente en modo diferible para que la espera no ocupe un worker. `DatabricksWorkflowTaskGroup` puede definir un job de Databricks desde Airflow.

#### ¿Cómo se ejecuta dbt desde Airflow?

Con un `BashOperator` que llama a `dbt build`, con un operador de dbt Cloud (`DbtCloudRunJobOperator`) o con Astronomer Cosmos, que convierte cada modelo de dbt en una tarea de Airflow con las dependencias del grafo de dbt.

#### ¿Cómo se ejecuta un job de AWS Glue desde Airflow?

Con `GlueJobOperator` del provider de Amazon, pasando el nombre del job y los argumentos del script, preferiblemente con `deferrable=True` o con `wait_for_completion` y un `GlueJobSensor`.

#### ¿Cómo se ejecuta trabajo en Kubernetes desde Airflow?

Con `KubernetesPodOperator` o `@task.kubernetes`, que inician un pod con una imagen, un comando, unos recursos y unos secretos dados para cada tarea. Cada tarea tiene sus propias dependencias y recursos.

#### ¿Para qué se usa `PythonVirtualenvOperator`?

Para ejecutar una función con dependencias que chocan con las de Airflow, en un virtualenv nuevo en cada ejecución (más lento) o en uno en caché. La función debe ser autocontenida porque se ejecuta en otro intérprete.

#### ¿Cómo orquestarías un pipeline que combina AWS Glue, Databricks y un proyecto dbt?

Con un DAG (o varios DAG enlazados por assets) que use `GlueJobOperator` del provider de Amazon, `DatabricksRunNowOperator` del provider de Databricks y Cosmos o el operador de dbt Cloud, todos en modo diferible, pasando nombres de tablas o rutas, con controles de calidad entre los pasos y una sola configuración de alertas.

<!-- challenge -->

Un proyecto dbt corre como un solo `BashOperator` que llama a `dbt build`. Un modelo fallido obliga a re-ejecutar dos horas. ¿Qué sugieres?

<!-- solution -->

Correr dbt con Cosmos, que convierte los modelos en tareas, o dividir `dbt build` por selectores en varias tareas. Un fallo reintenta solo los modelos afectados y sus descendientes, y cada modelo tiene sus logs en su tarea.

<!-- takeaways -->

- Los operadores de motores envían, esperan e informan; Airflow no calcula.
- Usa modo deferrable para jobs externos largos.
- Elige la granularidad para que los reintentos sean pequeños.

<!-- unit: Escribir tus propios operadores -->

<!-- goals -->

- Escribir un operador personalizado con campos de plantilla.
- Usar tareas auxiliares y callbacks sin efectos secundarios.

<!-- concept -->

Cuando el mismo patrón aparece en muchos DAGs, un operador personalizado lo empaqueta: parámetros en el constructor, trabajo en `execute` y una lista de campos que Airflow renderiza con Jinja. Todo lo que toca sistemas externos va en `execute`, no en el constructor, porque los constructores corren al parsear.

Piezas menores completan el cuadro: las tareas vacías hacen legibles los grafos y los callbacks agregan logs o notificaciones alrededor de la ejecución, siempre que sean rápidos y nunca decidan el resultado de la tarea.

<!-- example -->

```python
class PartitionCheckOperator(BaseOperator):
    template_fields = ("table", "partition")

    def __init__(self, table: str, partition: str, **kwargs):
        super().__init__(**kwargs)
        self.table, self.partition = table, partition

    def execute(self, context):
        rows = WarehouseHook().count(self.table, self.partition)
        if rows == 0:
            raise AirflowException(f"{self.table}/{self.partition} is empty")
```

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

#### ¿Qué es `on_execute_callback`?

Un callback que se llama justo antes de ejecutar una tarea, usado para logs o notificaciones. Como los demás callbacks, debe ser rápido y no debe hacer fallar la tarea.

<!-- challenge -->

Un operador personalizado abre una conexión a la base de datos en `__init__`. El scheduler se ralentiza y la base muestra cientos de conexiones inactivas. ¿Por qué?

<!-- solution -->

`__init__` corre cada vez que se parsea el archivo del DAG, así que cada parseo abre una conexión. Pasa la conexión a `execute`, mediante un hook, para que se abra solo cuando la tarea corre de verdad.

<!-- takeaways -->

- Las llamadas externas van en `execute`, nunca en `__init__`.
- Lista los parámetros con plantilla en `template_fields`.
- Mantén los callbacks rápidos y sin lógica de negocio.

### XCom y paso de datos

<!-- unit: Pasar valores con XCom -->

<!-- goals -->

- Pasar valores pequeños entre tareas con XCom y TaskFlow.
- Leer XComs en plantillas y separar salidas tipo diccionario.

<!-- concept -->

Las tareas suelen necesitar un dato pequeño de una tarea anterior: una ruta, un conteo, un ID de job. XCom guarda ese valor con la task instance para que tareas posteriores lo lean. TaskFlow oculta la mecánica: llamar a una función de tarea devuelve un marcador de su valor futuro, y pasarlo conecta dato y dependencia.

Los operadores clásicos leen los mismos valores mediante plantillas, así ambos estilos comparten un mecanismo.

<!-- example -->

```python
@task(multiple_outputs=True)
def extract() -> dict:
    return {"path": "s3://lake/orders/2026-10-17.parquet", "rows": 18233}

out = extract()
load(out["path"])                                   # TaskFlow
SQLExecuteQueryOperator(task_id="log", conn_id="wh",
    sql="INSERT INTO audit VALUES ({{ ti.xcom_pull(task_ids='extract', key='rows') }})")
```

#### ¿Qué es XCom?

"Cross-communication": un mecanismo para pasar valores pequeños entre tareas. Una tarea publica un valor (los valores devueltos con TaskFlow se publican automáticamente) y las tareas siguientes lo leen. Por defecto, los valores se guardan en la base de metadatos.

#### ¿Qué es `XComArg`?

El objeto que se obtiene al llamar a una función TaskFlow o al acceder a `.output` de un operador. Representa un valor futuro y lleva la dependencia, así que pasarlo a otra tarea vincula las dos.

#### ¿Cómo se lee un XCom en una plantilla?

```jinja2
{{ ti.xcom_pull(task_ids='extract', key='return_value') }}
```

Con TaskFlow, basta con pasar la salida de una función de tarea como argumento de otra.

#### ¿Qué hace `multiple_outputs=True`?

En un `@task` que devuelve un diccionario, publica cada clave como un XCom aparte, para que las tareas siguientes puedan usar `result["clave"]` por separado.

<!-- challenge -->

Una tarea devuelve una lista de 2 millones de IDs y la siguiente la lee. La UI va lenta y la base crece rápido. ¿Qué cambias?

<!-- solution -->

Escribir los IDs en almacenamiento de objetos o en una tabla de staging y devolver por XCom solo la ruta o el nombre de la tabla. La tarea siguiente lee los datos de ahí.

<!-- takeaways -->

- XCom lleva valores pequeños entre tareas.
- TaskFlow pasa XComs y dependencias en una llamada.
- Las plantillas leen los mismos valores para los operadores clásicos.

<!-- unit: Límites de XCom y backends -->

<!-- goals -->

- Mantener los datos grandes fuera de la base de metadatos.
- Evitar problemas de serialización y retención.

<!-- concept -->

El backend de XCom por defecto es la base de metadatos, hecha para estado, no para datos. Los valores grandes ralentizan scheduler y UI y acaban topando con límites de tamaño. Un backend personalizado mueve los valores a almacenamiento de objetos y guarda solo una referencia, lo que ayuda, pero el hábito más sano es pasar referencias tú mismo.

Los valores también deben sobrevivir a la serialización y permanecen hasta que alguien los limpia, así que la retención es parte de la higiene de la base.

<!-- example -->

```ini
# airflow.cfg: store XCom values above 1 MB in S3, keep a reference in the database
[common.io]
xcom_objectstorage_path = s3://airflow-xcom/
xcom_objectstorage_threshold = 1048576
```

#### ¿Por qué no pasar muchos datos por XCom?

El backend por defecto guarda los valores en la base de metadatos, que no está pensada para cargas grandes, y los valores serializados tienen límites de tamaño. Pasa referencias (una ruta de S3, un nombre de tabla, una partición) y deja los datos en el almacenamiento.

#### ¿Qué es un backend de XCom personalizado?

Un backend intercambiable que guarda los valores de XCom en otro lugar (S3, GCS, Azure Blob) y solo deja una referencia en la base de datos. El provider Common IO ofrece un backend de almacenamiento de objetos con un umbral de tamaño.

#### ¿Cómo se evitan los errores de serialización con XCom?

Devolviendo valores serializables en JSON (o tipos que Airflow sabe serializar, como dataclasses y DataFrames de pandas con el serializador adecuado); evita conexiones abiertas, generadores u objetos grandes. Devuelve rutas o IDs.

#### ¿Se borran los XCom después de una ejecución?

Se quedan en la base de datos (y se limpian cuando una tarea se limpia y se vuelve a ejecutar) hasta que los purgas con `airflow db clean` o una política de retención. Es otra razón para que sean pequeños.

<!-- challenge -->

Una tarea devuelve un cursor de base de datos y falla con un error de serialización. ¿Qué debería devolver?

<!-- solution -->

Leer los resultados dentro de la tarea y devolver datos serializables a JSON, como una lista de dicts si es pequeña. Si es grande, escribirla en almacenamiento y devolver la ruta. Los recursos abiertos como cursores no pueden cruzar tareas.

<!-- takeaways -->

- La base de metadatos no es un almacén de datos.
- Pasa referencias (rutas, nombres de tabla) para datos grandes.
- Devuelve valores serializables y limpia los XComs viejos.

<!-- unit: Contexto, plantillas y mapping -->

<!-- goals -->

- Usar el contexto de la tarea y las plantillas Jinja para valores de la ejecución.
- Crear tareas en tiempo de ejecución con dynamic task mapping.

<!-- concept -->

Cada task instance sabe dónde está: su ejecución, su intervalo, su número de intento. Ese conocimiento llega a tu código por el contexto en Python y por plantillas Jinja en los campos de los operadores, renderizadas justo antes de ejecutar.

Dynamic task mapping aplica la misma idea a la forma del grafo. En vez de fijar el número de tareas al parsear, una tarea mapeada se expande sobre una lista producida al ejecutar, como los archivos que llegaron hoy, y cada elemento se vuelve su propia instancia reintentable.

<!-- example -->

```python
@task
def list_files(ds=None) -> list[str]:
    return S3Hook().list_keys("landing", prefix=f"orders/{ds}/")

@task(max_active_tis_per_dagrun=5)
def load(key: str): ...

load.expand(key=list_files())
```

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

<!-- challenge -->

Una tarea mapeada sobre 300 archivos sobrecarga la base de destino. ¿Cómo conservas el mapping pero proteges la base?

<!-- solution -->

Limitar la concurrencia con `max_active_tis_per_dagrun`, o asignar la tarea mapeada a un pool con pocos slots. Cada archivo sigue teniendo su propia task instance y sus reintentos.

<!-- takeaways -->

- El contexto y las plantillas dan a las tareas las fechas e IDs de su ejecución.
- El mapping dimensiona el grafo al ejecutar con `.expand()`.
- Limita la concurrencia mapeada con límites de tarea o pools.

### Assets y programación por eventos

<!-- unit: Scheduling basado en datos -->

<!-- goals -->

- Programar DAGs por actualizaciones de assets en vez de horarios.
- Combinar assets y timetables en un calendario.

<!-- concept -->

Los calendarios por hora adivinan cuándo estarán listos los datos. Los assets quitan la adivinanza: una tarea productora declara que actualiza un dato, y los DAGs consumidores corren cuando eso pasa. Las dependencias describen datos, no relojes, y la UI muestra quién alimenta a quién.

Las condiciones pueden combinar varios assets con lógica and/or, o mezclar assets con un timetable cuando los consumidores necesitan frescura y además una ejecución diaria garantizada.

<!-- example -->

```python
orders = Asset("s3://lake/silver/orders/")

@task(outlets=[orders])
def build_orders(): ...

@dag(schedule=[orders])                 # runs after each successful build
def orders_report(): ...
```

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

#### ¿Puede dispararse un DAG por programación y por assets a la vez?

Sí, con `AssetOrTimeSchedule`, que ejecuta según un timetable y además cada vez que se cumple la condición de los assets.

#### ¿Qué es el decorador `@asset`?

Un atajo de Airflow 3 que define un asset junto con el DAG de una sola tarea que lo materializa, para escribir de forma centrada en los assets, al estilo de Dagster.

<!-- challenge -->

Un DAG de reporte corre a las 07:00 y usa un `ExternalTaskSensor` sobre el DAG de carga de las 06:00. A veces las cargas se mueven a las 06:30. ¿Cómo los desacoplas?

<!-- solution -->

Declara la tabla de la tarea de carga como outlet de un asset y programa el reporte sobre ese asset. El reporte corre cuando la carga termina bien, sin alinear calendarios ni sensores ocupando slots.

<!-- takeaways -->

- Los assets programan a los consumidores por actualizaciones de datos.
- Las condiciones combinan assets con and/or, o con un timetable.
- La vista de assets hace visible el linaje entre DAGs.

<!-- unit: Eventos de assets y disparadores externos -->

<!-- goals -->

- Entender qué garantiza y qué no un evento de asset.
- Disparar DAGs desde eventos externos sin polling.

<!-- concept -->

Un evento de asset significa que una tarea productora tuvo éxito, nada más. Airflow nunca mira los datos, así que una tarea que puede tener éxito sin escribir debe evitar emitir el evento, y los eventos pueden llevar metadatos como la partición escrita para que los consumidores sepan qué cambió.

Los eventos también pueden venir de fuera de Airflow. Los asset watchers conectan un trigger a una cola de mensajes, así un archivo que llega al almacenamiento puede iniciar un DAG en segundos y sin ningún sensor.

<!-- example -->

```python
queue = MessageQueueTrigger(queue="https://sqs.eu-west-1.amazonaws.com/123/landing-events")
landing = Asset("s3://landing/orders/", watchers=[AssetWatcher(name="sqs", trigger=queue)])

@dag(schedule=[landing])
def ingest_orders(): ...
```

#### ¿Saben los assets si los datos cambiaron de verdad?

No. Airflow solo sabe que una tarea productora terminó bien; no inspecciona los datos. Si una tarea puede terminar bien sin escribir nada, no debería emitir el evento, o el consumidor debe comprobarlo.

#### ¿Se pueden añadir metadatos a un evento de asset?

Sí. Una tarea productora puede añadir información extra (por ejemplo el número de filas o la partición escrita) al evento del asset mediante los outlet events, y los consumidores pueden leerla desde los eventos que los dispararon, en su contexto.

#### ¿Cómo se ve el linaje de los assets en la interfaz?

La vista de assets muestra cada asset con sus DAG productores y consumidores y el historial de eventos, lo que hace visibles las dependencias entre DAG.

#### ¿Qué es un asset alias?

Un marcador que se usa cuando la URI exacta del asset solo se conoce en tiempo de ejecución: la tarea emite eventos para un alias y le asocia el asset concreto, y los consumidores pueden programarse sobre el alias.

#### ¿Qué son los asset watchers?

Una función de Airflow 3 para programar por eventos de sistemas externos: un `AssetWatcher` asocia un trigger (por ejemplo sobre una cola de mensajes como SQS o Kafka) a un asset, para que un DAG se ejecute cuando llega un evento externo, no solo cuando otra tarea de Airflow actualiza el asset.

#### ¿Cómo se dispara un DAG de Airflow cuando llega un archivo a S3, sin sondeo?

Con un asset watcher sobre una cola SQS que recibe las notificaciones de eventos de S3 (Airflow 3), o con un evento de S3 que lanza una función Lambda que llama a la API REST de Airflow para disparar el DAG con la ruta del archivo como configuración.

<!-- challenge -->

Una tarea productora tiene éxito incluso cuando su fuente está vacía, y los DAGs de abajo se re-ejecutan para nada. ¿Cómo lo evitas?

<!-- solution -->

Revisar el conteo de filas en la tarea y saltarla (lanzar una excepción de skip) cuando no hay nada nuevo, para que no se emita evento. Opcionalmente adjuntar el conteo a los eventos para los consumidores.

<!-- takeaways -->

- Un evento de asset solo significa que el productor tuvo éxito.
- Los metadatos del evento dicen a los consumidores qué cambió.
- Los watchers disparan DAGs desde colas sin polling.

<!-- stage: Operar Airflow -->

### Executors y arquitectura

<!-- unit: Elegir un executor -->

<!-- goals -->

- Comparar los executors Local, Celery, Kubernetes y Edge.
- Ajustar el executor a la forma de la carga y a las habilidades del equipo.

<!-- concept -->

El executor decide dónde corre físicamente el código de las tareas. La elección equilibra rapidez de arranque y aislamiento. Los workers de larga vida arrancan tareas rápido pero comparten entorno y deben dimensionarse para el pico. Un pod por tarea arranca más lento pero da a cada tarea su imagen y recursos, y no cuesta nada en reposo.

Como puedes combinar executors, la elección ya no es todo o nada: la mayoría de tareas en workers rápidos, las especiales en pods o en workers remotos edge.

<!-- example -->

```ini
[core]
executor = CeleryExecutor,KubernetesExecutor
```
```python
@task(executor="KubernetesExecutor")      # this task alone runs in its own pod
def train_model(): ...
```

#### ¿Qué es un executor?

El componente que decide cómo y dónde se ejecutan las task instances. El scheduler envía las tareas en cola al executor, que las ejecuta en local o las reparte entre workers.

#### ¿Qué executors hay disponibles?

`LocalExecutor` (procesos en paralelo en la máquina del scheduler), `CeleryExecutor` (un conjunto de workers alimentados por un broker de mensajes como Redis o RabbitMQ), `KubernetesExecutor` (un pod por tarea) y executors de providers como los de AWS ECS y Batch y el Edge executor para workers remotos. Desde Airflow 2.10 se pueden usar varios executors a la vez.

#### ¿Cuándo elegirías el CeleryExecutor?

Para muchas tareas cortas con una carga estable: los workers de larga duración inician las tareas rápido. Hay que operar un broker y escalar los workers por tu cuenta (o con KEDA).

#### ¿Cuándo elegirías el KubernetesExecutor?

Cuando las tareas necesitan recursos o imágenes distintos, importa el aislamiento y la carga es irregular: cada tarea corre en su propio pod y los recursos se liberan después. El arranque del pod añade segundos de latencia por tarea.

#### ¿Qué papel cumple el broker de mensajes con Celery?

Redis o RabbitMQ guarda la cola de tareas que envía el scheduler; los workers de Celery la consumen. Un backend de resultados (normalmente la base de datos) guarda los estados de las tareas.

#### ¿Qué es el `pod_template_file`?

Una especificación de pod de Kubernetes que el KubernetesExecutor (y el KubernetesPodOperator) usa como base de los pods de las tareas: imagen, recursos, volúmenes, selectores de nodo, service account. Las tareas pueden sobrescribir partes con `executor_config`.

#### ¿Se pueden usar varios executors a la vez?

Sí, desde Airflow 2.10: se configura una lista de executors y se asigna cada tarea a uno con el argumento `executor`, por ejemplo la mayoría de las tareas en Celery y las pesadas y aisladas en Kubernetes.

#### ¿Qué es el Edge executor?

Un executor (del provider Edge3) que ejecuta tareas en workers remotos conectados a la API de Airflow por HTTP, por ejemplo en otra red o en otro centro de datos, sin acceso directo a la base de datos.

<!-- challenge -->

Tu plataforma corre 5.000 tareas SQL cortas al día y unos pocos entrenamientos con GPU por semana. ¿Qué configuración de executors propones?

<!-- solution -->

CeleryExecutor para las tareas SQL cortas, que arrancan rápido en workers listos, más KubernetesExecutor asignado por tarea para los entrenamientos, para usar nodos GPU solo cuando hace falta.

<!-- takeaways -->

- Los workers arrancan rápido; los pods aíslan y escalan a cero.
- Celery necesita un broker; Kubernetes, plantillas de pod.
- Varios executors dejan que cada tarea corra donde le conviene.

<!-- unit: Scheduler y DAG processor -->

<!-- goals -->

- Describir qué hacen el scheduler y el DAG processor en cada ciclo.
- Hacer la capa de scheduling altamente disponible y segura.

<!-- concept -->

El scheduling es un ciclo sobre la base de datos: encontrar ejecuciones que tocan, encontrar task instances con dependencias cumplidas y pasarlas al executor dentro de los límites. Parsear el código es otro trabajo, del DAG processor, para que un archivo lento o roto no frene el scheduling.

Como el estado vive en la base, la alta disponibilidad es simple: varios schedulers que se coordinan con bloqueos de fila. En Airflow 3, los workers además dejan de leer la base y piden lo que necesitan al API server, lo que reduce lo que una tarea puede ver.

<!-- example -->

```text
DAG files ─► DAG processor ─► serialized DAGs ─┐
                                               ▼
 scheduler ×2 ─ row locks ─► metadata DB ◄─ API server ◄─ workers (Task Execution API)
```

#### ¿Qué hace el scheduler?

Lee los DAG serializados, crea los DAG runs cuando corresponde, comprueba qué task instances tienen sus dependencias cumplidas, respeta los límites de concurrencia y los pools, y envía las tareas al executor. Pueden correr varios schedulers a la vez para tener alta disponibilidad.

#### ¿Qué hace el DAG processor?

Analiza los archivos de DAG y guarda los DAG serializados en la base de datos. En Airflow 3 es un componente aparte, así que el código de los usuarios nunca se ejecuta dentro del scheduler.

#### ¿Cómo se logra alta disponibilidad del scheduler?

Ejecutando dos o más schedulers contra la misma base PostgreSQL o MySQL; se coordinan con bloqueos a nivel de fila. Se ejecutan varios API servers detrás de un balanceador y varios triggerers.

#### ¿Cómo obtienen credenciales los workers en Airflow 3?

A través de la Task Execution API: las tareas piden conexiones, variables y XCom al API server en lugar de leer la base de metadatos, lo que mejora la seguridad y permite workers remotos.

<!-- challenge -->

Una VM con el único scheduler falló de noche y nada corrió hasta la mañana. ¿Qué propones para que no se repita?

<!-- solution -->

Correr al menos dos schedulers (en nodos distintos) contra un PostgreSQL gestionado con backups, y alertar sobre la métrica de heartbeat del scheduler. Correr el DAG processor aparte para que los problemas de parseo no tumben a los schedulers.

<!-- takeaways -->

- El scheduler recorre la base; el DAG processor parsea el código.
- Varios schedulers dan alta disponibilidad con bloqueos de fila.
- En Airflow 3 los workers hablan con el API server, no con la base.

<!-- unit: Concurrencia, pools y prioridades -->

<!-- goals -->

- Usar ajustes de concurrencia, pools y prioridades para repartir capacidad.
- Proteger sistemas compartidos de sobrecarga y escrituras en conflicto.

<!-- concept -->

La capacidad está limitada en varios niveles: toda la instalación, cada DAG, cada tarea y cada pool. Cuando las tareas compiten, los priority weights deciden quién va primero. Estos controles no solo ajustan la velocidad; expresan reglas sobre los sistemas que tocan las tareas.

Un pool con pocos slots es la forma más simple de decir "no más de cuatro consultas contra producción a la vez", y un pool de un slot serializa escritores que nunca deben solaparse.

<!-- example -->

```python
# pool "orders_table" created with 1 slot: writers take turns
MERGE_A = SQLExecuteQueryOperator(task_id="merge_a", pool="orders_table", ...)
MERGE_B = SQLExecuteQueryOperator(task_id="merge_b", pool="orders_table", ...)
```

#### ¿Qué ajustes de concurrencia existen?

`parallelism` (máximo de tareas en ejecución por scheduler), `max_active_tasks_per_dag`, `max_active_runs_per_dag`, los slots de los pools, `max_active_tis_per_dag` por tarea y ajustes propios de cada executor, como la concurrencia de los workers de Celery.

#### ¿Qué es un pool?

Un límite con nombre sobre los slots de tareas concurrentes, usado para proteger un recurso compartido: por ejemplo un pool de 4 slots para las tareas que consultan una base de datos de producción. Las tareas se asignan a un pool y pueden consumir varios slots.

#### ¿Qué es el priority weight?

Un número que decide qué tareas en cola se ejecutan primero cuando faltan slots. La regla de peso (`downstream`, `upstream`, `absolute`) controla cómo se acumula a lo largo del grafo.

#### ¿Qué son las colas en el CeleryExecutor?

Colas con nombre a las que se suscriben los workers. Asignar tareas a una cola (`queue="gpu"`) las envía a workers con los recursos adecuados.

#### Dos DAG escriben en la misma tabla y a veces entran en conflicto. ¿Cómo lo corriges?

Serializándolos: un pool de un solo slot para las escrituras en esa tabla, o fusionándolos en un solo DAG con un orden explícito, o haciendo que uno dependa del otro mediante un asset. Mejor todavía, dar a cada tabla un único proceso responsable.

<!-- challenge -->

Un lote nocturno de 200 tareas retrasa el DAG crítico de finanzas de la mañana. ¿Cómo garantizas que finanzas corra primero?

<!-- solution -->

Dar a las tareas de finanzas un `priority_weight` más alto (con regla `absolute`) para que ganen slots en cola, y poner el lote en un pool con límite de slots para que no ocupe todos los workers.

<!-- takeaways -->

- Hay límites por instalación, DAG, tarea y pool.
- Los pools protegen sistemas compartidos y serializan escrituras en conflicto.
- Los priority weights deciden quién toma los slots escasos.

### Configuración, seguridad y secretos

<!-- unit: Configuración y secretos -->

<!-- goals -->

- Configurar Airflow con archivos y variables de entorno.
- Guardar credenciales en un secrets backend, cifradas y enmascaradas.

<!-- concept -->

La configuración de Airflow tiene capas: el archivo de configuración, variables de entorno que lo sobrescriben y secretos que no deberían vivir en ninguno de los dos. Connections y variables pueden venir de la base, de variables de entorno o de un gestor de secretos; Airflow revisa esas fuentes en orden, así producción guarda secretos en una bóveda y desarrollo usa variables locales.

La defensa va más allá: los valores guardados en la base se cifran con la Fernet key, y logs y UI enmascaran lo que parezca un secreto.

<!-- example -->

```bash
export AIRFLOW__CORE__PARALLELISM=64
export AIRFLOW__SECRETS__BACKEND=airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend
export AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "airflow/connections"}'
```

#### ¿Cómo se configura Airflow?

Con `airflow.cfg`, sobrescrito por variables de entorno con el formato `AIRFLOW__SECCION__CLAVE` (por ejemplo `AIRFLOW__CORE__PARALLELISM`). Las variables de entorno son lo habitual en contenedores.

#### ¿Cómo se definen conexiones como variables de entorno?

Con `AIRFLOW_CONN_<CONN_ID>` igual a una URI o un JSON, por ejemplo `AIRFLOW_CONN_WAREHOUSE='postgresql://user:pass@host:5432/db'`. No aparecen en la interfaz y tienen prioridad sobre una conexión con el mismo ID en la base de datos (aunque un secrets backend configurado se consulta primero).

#### ¿Qué es un secrets backend?

Una integración que lee conexiones y variables de un gestor de secretos externo: AWS Secrets Manager o SSM Parameter Store, HashiCorp Vault, Google Secret Manager, Azure Key Vault. Así los secretos no tienen que guardarse en la base de metadatos.

#### ¿Qué es la clave Fernet?

La clave usada para cifrar las contraseñas de las conexiones y los valores de las variables en la base de metadatos. Debe estar definida, mantenerse en secreto y ser idéntica en todos los componentes; rotarla exige volver a cifrar.

#### ¿Cómo evita Airflow mostrar secretos en los logs y la interfaz?

Enmascara las contraseñas de las conexiones, las variables cuyo nombre contiene palabras como `password`, `secret` o `token`, y los valores registrados con `mask_secret()`. El enmascarado no es infalible, así que no imprimas secretos.

<!-- challenge -->

La contraseña de una connection aparece en texto plano en el log de una tarea porque la tarea imprimió una URL que la contenía. ¿Cómo lo evitas?

<!-- solution -->

Dejar de imprimir la URL, registrar el valor en el enmascarador de secretos si se construye al ejecutar y rotar la contraseña filtrada. Preferir secrets backends para que los valores no se copien a variables con nombres que el enmascarador no reconoce.

<!-- takeaways -->

- Las variables de entorno sobrescriben `airflow.cfg`.
- Los secrets backends guardan las credenciales en una bóveda.
- Cifrado y enmascarado protegen, pero el código aún puede filtrar.

<!-- unit: Acceso e identidad -->

<!-- goals -->

- Controlar quién puede ver y disparar qué DAGs.
- Dar acceso cloud a las tareas sin claves de larga vida.

<!-- concept -->

En Airflow importan dos identidades: las personas que usan la UI y el código que corre en los workers. Las personas reciben roles que limitan qué DAGs ven o disparan. El código corre con los permisos de los workers, el problema más difícil, porque quien pueda desplegar un DAG puede hacer que lea cualquier connection.

Por eso el acceso se controla en el despliegue (revisiones, despliegues separados por equipo) y los workers reciben identidades cloud de corta vida en vez de claves guardadas.

<!-- example -->

```python
@dag(access_control={"finance-ops": {"DAGs": {"can_read", "can_edit"}}},
     schedule="@daily", start_date=datetime(2026, 1, 1))
def finance_close(): ...
```

#### ¿Cómo se controla el acceso a la interfaz?

Con un auth manager. Airflow 3 trae un auth manager simple para desarrollo; el auth manager FAB ofrece control de acceso basado en roles (Admin, Op, User, Viewer y roles propios), y los servicios administrados se integran con el IAM de la nube.

#### ¿Cómo se restringe quién puede disparar un DAG?

Con control de acceso basado en roles: se dan permisos a los roles sobre DAG concretos (por ID de DAG o con `access_control` en el DAG), para que cada equipo solo pueda disparar y limpiar sus propios DAG.

#### ¿Cómo debe acceder el código de los DAG a los recursos de la nube?

Con la identidad del worker (IAM roles for service accounts en Kubernetes, el rol de ejecución de MWAA, workload identity) siempre que se pueda, en lugar de claves de larga duración guardadas en conexiones.

#### ¿Por qué es riesgoso que muchas personas editen el código de los DAG?

El código de los DAG se ejecuta con los permisos de los workers y puede leer las conexiones, así que quien puede desplegar DAG tiene en la práctica acceso a todas las conexiones. La revisión de código y los controles de CI en el repositorio de DAG son parte de la seguridad.

<!-- challenge -->

Diez equipos comparten un despliegue de Airflow y los DAGs de uno necesitan acceso a datos de nómina. ¿Qué propones?

<!-- solution -->

Dar a nómina su propio despliegue (o al menos workers propios con otro rol cloud y otra ruta de secretos), restringir sus DAGs con RBAC y exigir revisión de código en ese repositorio. Workers compartidos expondrían las credenciales de nómina al código de todos.

<!-- takeaways -->

- RBAC controla a las personas; la identidad del worker, al código.
- Desplegar código de DAG equivale a acceder a sus connections.
- Prefiere identidades de workload a claves cloud guardadas.

<!-- stage: Producción -->

### Pruebas y calidad del código

<!-- unit: Probar DAGs y lógica de tareas -->

<!-- goals -->

- Escribir pruebas de integridad y estructura de DAGs.
- Probar unitariamente la lógica y los operadores sin un Airflow completo.

<!-- concept -->

Un DAG puede fallar en tres lugares: al importar, en su estructura o en la lógica de sus tareas. Cada uno necesita otra prueba. Las pruebas de importación y estructura cargan los DAGs y verifican que parsean y tienen la forma esperada. Las pruebas de lógica tratan el código de las tareas como cualquier módulo de Python, algo fácil solo si la lógica vive fuera del archivo del DAG.

Los operadores que llaman sistemas externos se prueban dos veces: con hooks simulados para su lógica y contra contenedores locales para el comportamiento real.

<!-- example -->

```python
def test_dags_import():
    bag = DagBag(include_examples=False)
    assert bag.import_errors == {}

def test_sales_structure():
    dag = DagBag().get_dag("sales_load")
    assert dag.get_task("extract").downstream_task_ids == {"transform"}
```

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

#### ¿Cómo se prueba que un DAG tiene la estructura correcta?

Cargándolo desde un `DagBag` y comprobando los IDs de las tareas, las dependencias (`task.downstream_task_ids`), las programaciones y los ajustes, para detectar cambios accidentales en el grafo.

#### ¿Cómo se hacen pruebas unitarias de la lógica de las tareas?

Manteniendo la lógica de negocio en funciones o módulos Python normales fuera del archivo del DAG, probándolos con pytest sin Airflow, y dejando las tareas como envoltorios finos. Para los operadores, se prueba `execute()` con hooks simulados (mocks).

#### ¿Cómo se comprueba que los campos con plantilla se generan bien?

Generándolos para un contexto dado en una prueba (`ti.render_templates()`), o ejecutando `airflow tasks render dag_id task_id fecha`, y revisando el SQL o el comando resultante.

#### ¿Cómo se prueban los operadores propios que usan sistemas externos?

Simulando el hook en las pruebas unitarias para verificar la lógica y los parámetros del operador, y ejecutando pruebas de integración contra contenedores locales (Postgres, LocalStack para AWS, MinIO para S3) en CI.

<!-- challenge -->

Toda la lógica de transformación de un DAG está escrita dentro de cinco funciones `@task` y nadie la prueba. ¿Cómo la vuelves testeable?

<!-- solution -->

Mover la lógica a un módulo de funciones puras que reciben y devuelven datos, probarlas con pytest y dejar las tareas como envoltorios delgados que leen entradas, llaman las funciones y escriben salidas.

<!-- takeaways -->

- Prueba importación, estructura y lógica por separado.
- La lógica fuera de los archivos de DAG es fácil de probar.
- Simula hooks en tests unitarios; usa contenedores para integración.

<!-- unit: Ejecuciones locales y CI -->

<!-- goals -->

- Correr DAGs y tareas sueltas localmente para depurar.
- Armar un pipeline de CI para un repositorio de Airflow.

<!-- concept -->

La retroalimentación rápida viene de correr piezas pequeñas en local: un DAG completo en un proceso con depurador, o una tarea para una fecha. Los entornos locales deben parecerse a las imágenes de producción, o los problemas de "en mi máquina funciona" reaparecen al desplegar.

El CI automatiza los mismos chequeos en cada cambio, del linting a las pruebas de integridad, y un entorno de staging corre datos reales en un rango corto de fechas antes de producción.

<!-- example -->

```yaml
# CI steps for an Airflow repository
- run: ruff check dags/ --select AIR
- run: pytest tests/unit tests/dags
- run: docker build -t airflow:${{ github.sha }} .
```

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

#### ¿Qué debe ejecutar un pipeline de CI para un repositorio de Airflow?

Linting (Ruff con reglas `AIR`), pruebas unitarias de la lógica de negocio, pruebas de integridad de los DAG (errores de importación del `DagBag`, convenciones, ciclos), controles del tiempo de análisis, construcción de la imagen y despliegue en staging, con el despliegue a producción tras el merge o una aprobación.

<!-- challenge -->

Un import roto llegó a producción y el DAG desapareció de la UI. ¿Qué chequeo de CI lo habría detectado y cuánto cuesta?

<!-- solution -->

Una prueba de integridad que carga todos los archivos con `DagBag` y verifica que no haya errores de importación. Corre en segundos en el CI, dentro de la misma imagen que producción, así también detecta paquetes faltantes.

<!-- takeaways -->

- `dag.test()` y `airflow tasks test` dan retroalimentación local rápida.
- Las reglas `AIR` de Ruff detectan código obsoleto y problemas de Airflow 3.
- El CI corre lint, pruebas unitarias y de integridad en cada cambio.

### Despliegue y operación

<!-- unit: Desplegar DAGs -->

<!-- goals -->

- Desplegar código de DAGs y dependencias de forma reproducible.
- Revertir rápido un mal despliegue.

<!-- concept -->

Un despliegue tiene dos partes que deben coincidir: el entorno (Airflow, providers, paquetes) y el código de los DAGs. Construir ambos en una sola imagen hace idénticos todos los entornos. Enviar los DAGs aparte, con git-sync, bundles o un bucket de S3, es más rápido pero invita a desajustes entre código y paquetes instalados.

Sea cual sea el método, los despliegues deben salir del CI y poder revertirse volviendo a desplegar la versión anterior.

<!-- example -->

```dockerfile
FROM apache/airflow:3.1.0-python3.12
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.1.0/constraints-3.12.txt"
COPY dags/ /opt/airflow/dags/
```

#### ¿Cómo se despliegan los DAG?

La mayoría de los equipos construye una imagen Docker con Airflow, los providers, las dependencias y el código de los DAG, y la despliega con CI/CD en Kubernetes (chart de Helm) o en un servicio administrado. Alternativas: sincronizar los DAG desde Git con git-sync o en un bucket de S3 (MWAA). Los DAG bundles de Airflow 3 pueden leer los DAG directamente desde Git con versionado.

#### ¿Qué es un DAG bundle?

Un concepto de Airflow 3 para un conjunto de archivos de DAG provenientes de un origen como una carpeta local o un repositorio Git, que permite a Airflow seguir las versiones del código y ejecutar cada DAG run con la versión con la que empezó.

#### ¿Qué es el chart oficial de Helm?

El chart de Helm de Apache Airflow, que despliega todos los componentes en Kubernetes con opciones para los executors, git-sync, PgBouncer, el autoescalado con KEDA, los logs y los secretos. Es el despliegue estándar autoalojado en Kubernetes.

#### ¿Cómo se despliega en Amazon MWAA?

Subiendo los DAG al bucket de S3 del entorno (normalmente desde CI con `aws s3 sync`) y administrando `requirements.txt`, los plugins y un script de arranque en S3; la versión de Airflow y el tamaño del entorno se definen en su configuración. El rol de ejecución da el acceso a AWS.

#### ¿Cómo se revierte un despliegue de DAG defectuoso?

Volviendo a desplegar la imagen o el commit de Git anterior con CI. Con el versionado de DAG de Airflow 3, las ejecuciones existentes conservan su versión. Después se limpian las ejecuciones fallidas si hace falta.

#### Un DAG funciona en local pero en producción las tareas fallan con "module not found". ¿Por qué?

A la imagen o los workers de producción les falta la dependencia, o el módulo no está en la ruta (por ejemplo código fuera de la carpeta de DAG o de plugins). Añádelo a los requisitos de la imagen o a un paquete, y construye local y producción a partir de la misma imagen.

<!-- challenge -->

Un despliegue rompió tres DAGs a las 02:00. Escribe los tres primeros pasos de tu reversión.

<!-- solution -->

Volver a desplegar la imagen o commit anterior por CI. Verificar que la lista de errores de importación esté vacía y los DAGs hayan vuelto. Luego limpiar las task instances fallidas para que corran con el código viejo, y abrir un ticket para corregir.

<!-- takeaways -->

- Despliega código y dependencias juntos cuando puedas.
- Despliega desde el CI; revierte desplegando la versión anterior.
- "Module not found" suele indicar que imagen y código divergieron.

<!-- unit: Actualizaciones y dependencias -->

<!-- goals -->

- Actualizar versiones de Airflow con seguridad, incluso de 2 a 3.
- Fijar dependencias con archivos de constraints.

<!-- concept -->

Airflow descansa sobre cientos de paquetes de Python, y un pequeño cambio en un provider puede cambiar el comportamiento de un operador. Los archivos de constraints fijan un conjunto probado para cada versión de Airflow y de Python, así las actualizaciones se vuelven eventos deliberados y no efectos secundarios de reconstruir la imagen.

Las versiones mayores agregan migraciones de base y cambios de API. El camino seguro es gradual: llegar a la última menor, corregir advertencias, probar en staging con un backup de la base y luego dar el salto.

<!-- example -->

```bash
pip install "apache-airflow[amazon,databricks]==3.1.0" \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.1.0/constraints-3.12.txt"
ruff check dags/ --select AIR3     # find Airflow 3 incompatibilities
airflow db migrate
```

#### ¿Cómo se actualiza Airflow de forma segura?

Leyendo las notas de la versión, actualizando primero en un entorno de pruebas, usando los archivos de constraints para fijar dependencias compatibles, ejecutando `airflow db migrate`, revisando los DAG en busca de elementos obsoletos (reglas `AIR` de Ruff para Airflow 3) y respaldando la base de metadatos antes de migrar producción.

#### ¿Qué son los archivos de constraints?

Listas de dependencias fijadas que se publican para cada versión de Airflow y de Python, usadas con `pip install "apache-airflow==X" --constraint <url>` para obtener un conjunto de paquetes que se sabe que funciona.

#### ¿Por qué fijar las versiones de los providers y las dependencias?

Las actualizaciones sin fijar pueden cambiar el comportamiento de los operadores o romper imports sin avisar. Fija las versiones con el archivo de constraints y actualiza de forma deliberada y con pruebas.

#### ¿Cómo migrarías de Airflow 2 a Airflow 3?

Primero actualizo a la última 2.x y corrijo los avisos de obsolescencia, ejecuto las reglas `AIR3` de Ruff para encontrar el código que hay que cambiar (imports a `airflow.sdk`, `schedule_interval` a `schedule`, `execution_date` a `logical_date`, SubDAG y SLA eliminados, sin acceso directo a la base desde las tareas), pruebo en staging, migro la base de datos y actualizo el despliegue para el API server y el DAG processor.

<!-- challenge -->

Reconstruir la imagen sin cambios actualizó solo un provider, y un operador ahora se comporta distinto. ¿Cómo lo evitas?

<!-- solution -->

Fijar Airflow y todos los providers en `requirements.txt` e instalar con el archivo de constraints correspondiente, para que las reconstrucciones sean reproducibles. Actualizar providers a propósito en una rama, con pruebas y notas de versión revisadas.

<!-- takeaways -->

- Los constraints hacen reproducibles las instalaciones.
- Fija los providers; actualízalos a propósito.
- Para versiones mayores: última menor, advertencias, pruebas, backup, migración.

<!-- unit: Monitoreo y alertas -->

<!-- goals -->

- Recolectar logs y métricas de Airflow y sus tareas.
- Diseñar alertas que lleguen a las personas correctas con el contexto correcto.

<!-- concept -->

Importan dos tipos de señales. Las de plataforma (heartbeat del scheduler, colas, tiempos de parseo) dicen si Airflow funciona. Las de pipeline (fallos de tareas, ejecuciones tardías) dicen si llegan los datos. Cada una tiene su público: el equipo de plataforma y los dueños de los datos.

Las buenas alertas llevan contexto y apuntan a un runbook. Las alertas que suenan cada noche por tareas inestables conocidas enseñan a ignorarlas, así que arreglar las causas raíz es parte de alertar, no algo aparte.

<!-- example -->

```python
def notify_failure(context):
    ti = context["ti"]
    send_slack(f":red_circle: {ti.dag_id}.{ti.task_id} failed ({context['ds']}) "
               f"owner={ti.task.owner} log={ti.log_url}")

default_args = {"on_failure_callback": notify_failure}
```

#### ¿Dónde van los logs de las tareas?

Por defecto a archivos locales en los workers, visibles en la interfaz. En producción se configura el logging remoto en S3, GCS, Azure Blob, Elasticsearch o CloudWatch para que los logs sobrevivan a los reinicios de los pods.

#### ¿Cómo se monitorea Airflow?

Con métricas StatsD u OpenTelemetry (heartbeat del scheduler, tiempo de análisis de los DAG, tareas en cola y en ejecución, duraciones, uso de los pools) en Prometheus/Grafana o Datadog, endpoints de salud y alertas sobre los fallos y las ejecuciones demasiado largas.

#### ¿Cómo recibes alertas cuando falla una tarea?

Con callbacks (`on_failure_callback`, `on_retry_callback`, `on_success_callback`) que envían a Slack, correo o PagerDuty, las clases notifier de los providers o la configuración de correo. Alerta a nivel de DAG para tener mensajes accionables y sin duplicados.

#### ¿Qué reemplazó a los SLA en Airflow 3?

Los SLA (`sla` y `sla_miss_callback`) se eliminaron porque no eran confiables. Airflow 3.1 introdujo las deadline alerts, que lanzan un callback cuando un DAG run no terminó antes de un plazo relativo a una hora de referencia. Hasta entonces, los equipos usaban `execution_timeout`, `dagrun_timeout` y monitoreo externo.

#### ¿Qué debe contener un runbook para un DAG que falla?

Qué hace el DAG y quién es el responsable, las dependencias de origen, cómo revisar los logs y las entradas, qué tareas se pueden limpiar y reejecutar sin riesgo, cómo hacer un backfill, a quién avisar y los fallos conocidos con su solución.

#### Tu persona de guardia recibe cada noche una alerta por la misma tarea inestable. ¿Qué cambias?

Busco la causa raíz en los logs (timeouts, límites de recursos, retrasos del origen), añado reintentos con espera solo para los errores transitorios, añado un sensor o una dependencia por asset si empieza antes de que su entrada esté lista, subo los recursos o la paso a un pool dedicado, y cambio las alertas para que solo salten cuando se agotan los reintentos.

<!-- challenge -->

Un DAG de finanzas debe terminar antes de las 08:00, pero nadie se entera cuando va tarde sin fallar. ¿Qué configuras?

<!-- solution -->

Una deadline alert (Airflow 3.1+) sobre el DAG run para las 08:00 que avise a los responsables, o un chequeo aparte que alerte si la ejecución no ha terminado bien a esa hora. Incluye el enlace a la ejecución y el runbook en el mensaje.

<!-- takeaways -->

- Envía los logs a un almacén remoto; exporta métricas a un sistema de monitoreo.
- Alerta a los responsables con contexto y un enlace al runbook.
- Arregla las tareas inestables para que las alertas sigan significando algo.

<!-- unit: Diagnosticar tareas atascadas y que mueren -->

<!-- goals -->

- Diagnosticar tareas atascadas en `queued` y zombie tasks.
- Encontrar la causa cuando las tareas mueren sin error.

<!-- concept -->

Cuando una tarea nunca arranca o muere en silencio, el problema suele estar debajo de tu código. Una tarea en cola espera un slot que algún límite o un worker ausente nunca da. Una tarea que desaparece sin traceback casi siempre fue matada desde fuera, a menudo por memoria, y el scheduler nota después la falta de heartbeat.

Por eso la depuración empieza por la plataforma: límites, workers, eventos de pods y métricas de memoria, antes del código de la tarea.

<!-- example -->

```bash
kubectl get events -n airflow --field-selector reason=OOMKilling
kubectl describe pod sales-load-transform-abc12 | grep -A3 "Last State"
#   Last State: Terminated  Reason: OOMKilled  Exit Code: 137
```

#### ¿Cuáles son las causas comunes de tareas atascadas en `queued`?

No hay slots libres (límites de parallelism, de pool o de concurrencia del DAG), los workers están caídos o no consumen la cola, el executor no logra arrancar pods (cuotas, errores al descargar la imagen) o hay un problema con el scheduler. Revisa los pools, los logs de los workers y los eventos del executor.

#### ¿Qué son las tareas zombie?

Task instances marcadas como en ejecución cuyo proceso murió sin avisar (caída del worker, OOM kill, desalojo del pod). El scheduler detecta la falta de heartbeats y las marca como fallidas o las reintenta.

#### Las tareas suelen morir sin ningún error en los logs. ¿Qué sospechas?

Cierres por falta de memoria (OOM) del worker o del pod, desalojos o timeouts. Revisa los eventos de los pods y las métricas de los workers, sube los límites de memoria y saca el procesamiento pesado de Airflow.

<!-- challenge -->

Tras un release, muchas tareas quedan en `queued` mientras los workers parecen ociosos. Enumera tres cosas a revisar.

<!-- solution -->

Si los workers consumen la cola correcta (una cola renombrada deja tareas varadas), si un pool o el límite de concurrencia del DAG está lleno, y si el executor puede arrancar pods (cuotas, errores al bajar imágenes). Los logs del scheduler suelen nombrar el límite.

<!-- takeaways -->

- `queued` indica un problema de límites o workers, no de código.
- Los zombies vienen de procesos que murieron sin avisar.
- Exit code 137 o sin traceback: sospecha de memoria.

<!-- unit: Escalado y salud de la base -->

<!-- goals -->

- Escalar schedulers, workers y la base a medida que crecen los DAGs.
- Controlar tiempos de parseo y tamaño de la base.

<!-- concept -->

Los límites de Airflow suelen aparecer en este orden: el parseo, luego la base de datos, luego los workers. El parseo crece con cada archivo de DAG e import pesado. La base crece con cada ejecución y XCom, y cada tarea le abre conexiones. Los workers son lo más fácil de escalar, así que arregla lo primero antes de agregar máquinas.

La mayor parte del escalado es higiene: archivos de DAG livianos, conexiones a la base con pool, limpieza periódica y esperas deferrable.

<!-- example -->

```bash
airflow dags report                                # parse time per file
airflow db clean --clean-before-timestamp "$(date -d '-90 days' +%F)" --yes
```

#### ¿Cómo se escala Airflow?

Con varios schedulers, escalando los workers (autoescalado de los workers de Celery con KEDA, o el executor de Kubernetes), usando operadores diferibles para liberar slots, reduciendo el tiempo de análisis de los DAG, ajustando `parallelism` y los pools, y dejando el cálculo pesado fuera de Airflow.

#### ¿Por qué importa el tiempo de análisis de los DAG?

Un análisis lento retrasa la programación de todos los DAG y consume CPU. Se mide con `airflow dags report`; se corrige eliminando el trabajo de nivel superior, evitando imports pesados a nivel de módulo y dividiendo los archivos gigantes de DAG generados.

#### ¿Cómo se mantiene sana la base de metadatos?

Usando un PostgreSQL administrado con copias de respaldo, vigilando su tamaño y ejecutando `airflow db clean` periódicamente para purgar task instances, metadatos de logs y XCom antiguos. Una base enorme ralentiza el scheduler y la interfaz.

#### ¿Por qué usar PgBouncer con Airflow?

Cada tarea y componente abre conexiones a la base de datos; muchas tareas concurrentes pueden agotar el límite de conexiones de PostgreSQL. PgBouncer las agrupa. En Airflow 3 la Task Execution API reduce las conexiones directas desde los workers.

#### Cientos de DAG tardan en programarse. ¿Qué investigas?

Los tiempos de análisis de los DAG (`airflow dags report`), el código y los imports de nivel superior, el número de archivos de DAG, la CPU del scheduler y el rendimiento de la base de datos, el número de task instances en la base (ejecuta `db clean`), y si el scheduler y el DAG processor tienen suficientes recursos o réplicas.

#### La CPU de tu scheduler está al 100 %. ¿Cuáles son las soluciones habituales?

Reducir la carga de análisis de los DAG (archivos más ligeros y menos numerosos, un `min_file_process_interval` más largo, un DAG processor separado), abandonar los sensores en modo poke, limpiar la base de datos, añadir réplicas del scheduler y revisar los DAG con cantidades enormes de tareas mapeadas.

<!-- challenge -->

La base de metadatos llegó a 400 GB y la UI tarda 30 segundos en cargar. ¿Qué haces primero y qué programas?

<!-- solution -->

Hacer backup y luego `airflow db clean` para purgar task instances, XComs y metadatos de logs más allá de tu retención. Programar la misma limpieza cada semana (como DAG de mantenimiento) y revisar XComs grandes que deberían ser referencias.

<!-- takeaways -->

- Arregla parseo y base antes de agregar workers.
- PgBouncer agrupa las muchas conexiones que abren las tareas.
- Limpia metadatos viejos de forma programada.

### Buenas prácticas

<!-- unit: Orquestar, no procesar -->

<!-- goals -->

- Dimensionar tareas para que sean significativas y baratas de reintentar.
- Dividir los pipelines en DAGs según calendarios y responsables.

<!-- concept -->

Airflow funciona mejor como una capa delgada de control sobre sistemas que hacen el trabajo. Las tareas que procesan datos en el worker compiten por memoria con todo lo demás y no escalan. El tamaño correcto de una tarea es una unidad que querrías reintentar sola, y el de un DAG es un calendario y un responsable.

Como las tareas pueden correr en máquinas distintas, todo lo que pasa entre ellas debe vivir en almacenamiento compartido, no en el disco local.

<!-- example -->

| Demasiado grande | Tamaño correcto | Demasiado fino |
|---|---|---|
| `run_everything` (2 h, reintenta todo) | `load_orders`, `build_orders_mart` | una tarea por sentencia SQL |

#### ¿Debe Airflow hacer el procesamiento de datos?

No. Airflow debe orquestar: lanzar Spark, motores SQL, dbt, Databricks o contenedores que hacen el procesamiento, y pasar referencias. El trabajo pesado con pandas en los workers de Airflow compite con otras tareas y escala mal.

#### ¿Cuál es una buena granularidad de tareas?

Cada tarea debería ser una unidad con sentido y reintentable (extraer un origen, cargar una tabla, ejecutar un grupo de modelos). Demasiado gruesa obliga a reintentar mucho trabajo; demasiado fina añade sobrecarga de programación y vuelve ilegible el grafo.

#### ¿Por qué los DAG no deben depender de archivos locales entre tareas?

Las tareas pueden correr en workers o pods distintos, así que un archivo escrito por una tarea puede no existir para la siguiente. Usa almacenamiento de objetos, un volumen compartido o una base de datos.

#### ¿En cuántos DAG se debe dividir un pipeline?

Un DAG por cada programación y frontera de responsabilidad independientes. Divide cuando las partes tienen programaciones, responsables o dominios de fallo distintos, y conéctalas con assets; mantén en un solo DAG los pasos muy acoplados.

<!-- challenge -->

Un DAG carga datos de marketing, finanzas y producto a las 06:00 y tiene tres equipos dueños. Los fallos de uno bloquean a los otros. ¿Cómo lo reestructuras?

<!-- solution -->

Dividirlo en un DAG por dominio, cada uno con su responsable y sus alertas. Cuando un dominio necesita datos de otro, conectar los DAGs con assets para que corran cuando los datos estén listos.

<!-- takeaways -->

- Airflow orquesta; los motores procesan.
- Una tarea es una unidad reintentable; un DAG, un calendario y un responsable.
- Comparte datos por almacenamiento, no por discos de workers.

<!-- unit: Reintentos seguros y chequeos de datos -->

<!-- goals -->

- Configurar reintentos que ayuden ante errores transitorios sin esconder bugs.
- Agregar chequeos de calidad de datos como compuertas en un DAG.

<!-- concept -->

Los reintentos son un seguro barato contra redes inestables y APIs ocupadas, pero solo cuando las tareas son idempotentes y los errores transitorios. Reintentar un bug tres veces solo retrasa la alerta. El backoff y los pools convierten los reintentos de estampida en espera cortés.

Los chequeos de datos son la otra mitad de la confiabilidad: una tarea puede tener éxito y producir datos malos. Chequeos entre la carga y la publicación frenan los datos malos antes de que los vean los consumidores.

<!-- example -->

```python
SQLColumnCheckOperator(
    task_id="check_orders", conn_id="warehouse", table="silver.orders",
    column_mapping={"order_id": {"null_check": {"equal_to": 0}, "unique_check": {"equal_to": 0}}},
)
```

#### ¿Cómo se hacen seguros los reintentos?

Haciendo las tareas idempotentes, definiendo `retries` y `retry_delay` (con `retry_exponential_backoff`) para los errores transitorios, y fallando rápido (sin reintentos) ante errores que reintentar no arregla, como credenciales incorrectas o un fallo de calidad de datos.

#### Una tarea falla al azar por el límite de solicitudes de una API. ¿Qué haces?

Añado reintentos con espera exponencial, pongo las llamadas a la API en un pool que limite la concurrencia, respeto `Retry-After` en el hook y reduzco las llamadas (agrupación, extracción incremental).

#### ¿Cómo se hacen controles de calidad de datos en Airflow?

Con los operadores de control SQL (`SQLColumnCheckOperator`, `SQLTableCheckOperator`, `SQLCheckOperator`), los operadores de Great Expectations o Soda, o las pruebas de dbt, ubicados después de las cargas para detener las tareas siguientes cuando los datos están mal.

<!-- challenge -->

Una tarea de carga reintenta cinco veces ante un desajuste de esquema y falla finalmente dos horas después. ¿Qué cambias?

<!-- solution -->

Fallar rápido ante errores no transitorios: capturar los errores de esquema y lanzar un fallo que omita los reintentos, dejando reintentos con backoff solo para timeouts y throttling. Agregar un chequeo de esquema antes de la carga.

<!-- takeaways -->

- Reintenta errores transitorios con backoff; falla rápido ante bugs.
- Pools y backoff protegen sistemas con límites de tasa.
- Pon chequeos de calidad antes de publicar.

<!-- unit: Organizar código y configuración -->

<!-- goals -->

- Organizar código compartido, configuración y nombres entre DAGs.
- Mantener los DAGs legibles para la próxima persona de guardia.

<!-- concept -->

Un repositorio con cincuenta DAGs necesita la misma estructura que cualquier código. La lógica compartida vive en un paquete probado, no copiada entre archivos. La configuración se separa según cuánto cambia: la estructura en código, los valores por entorno en variables y las credenciales en secretos.

La legibilidad es una cuestión operativa. Quien lee un DAG a las 3 a. m. no lo escribió, así que nombres consistentes, tareas pequeñas y documentación deciden qué tan rápido puede actuar.

<!-- example -->

```text
dags/
  sales__daily_load.py      # thin: schedule, tasks, dependencies
  finance__month_close.py
include/
  common/warehouse.py       # shared, tested code
tests/
```

#### ¿Dónde debe vivir la configuración?

En el código (versionado) para la estructura, en variables de entorno o Variables para los valores propios de cada entorno, y en un secrets backend para las credenciales. Evita leer muchas Variables al analizar los DAG.

#### ¿Cómo se nombran los DAG y las tareas?

De forma coherente y descriptiva: `dominio__proposito` para los DAG (`sales__daily_load`), verbos para las tareas (`extract_orders`, `load_orders`), con owners y etiquetas para los equipos y los dominios de datos.

#### ¿Cómo se maneja el código compartido entre DAG?

Poniéndolo en un paquete Python (en la carpeta `include/` o `plugins/` del repositorio, o instalado en la imagen) con sus propias pruebas, en lugar de copiar código entre archivos de DAG.

#### ¿Cómo se mantiene legible un DAG?

Con tareas pequeñas y bien nombradas, task groups para los bloques lógicos, nada de lógica de negocio en el archivo del DAG, documentación con `doc_md`, un uso coherente de TaskFlow u operadores y poca generación dinámica.

<!-- challenge -->

Cinco DAGs tienen cada uno una copia de la misma función de 80 líneas para cargar archivos al warehouse, con pequeñas diferencias. ¿Qué haces?

<!-- solution -->

Extraer una función parametrizada (u operador personalizado) a un paquete compartido con pruebas, reemplazar las copias y expresar las diferencias como parámetros. Los arreglos futuros se hacen una sola vez.

<!-- takeaways -->

- El código compartido va en un paquete probado.
- Estructura en código, valores de entorno en variables, credenciales en secretos.
- Nombres y docs consistentes aceleran la respuesta a incidentes.

<!-- unit: Extender Airflow y linaje -->

<!-- goals -->

- Saber qué pueden agregar plugins y listeners a Airflow.
- Emitir linaje con OpenLineage.

<!-- concept -->

Airflow tiene puntos de extensión para lo que los operadores no hacen. Los plugins agregan vistas a la UI, macros o timetables. Los listeners reaccionan a eventos como el fin de una tarea, lo que los hace el lugar natural para temas transversales como linaje, auditoría o métricas propias.

OpenLineage se apoya en los listeners: los providers describen las entradas y salidas de cada tarea y un backend arma un grafo de linaje entre herramientas, no solo dentro de Airflow.

<!-- example -->

```bash
pip install apache-airflow-providers-openlineage
export AIRFLOW__OPENLINEAGE__TRANSPORT='{"type": "http", "url": "http://marquez:5000"}'
```

#### ¿Para qué sirven los plugins en Airflow?

Para extender Airflow con vistas propias en la interfaz, enlaces de menú, macros, listeners, timetables y, en Airflow 3, apps FastAPI y vistas React. Los operadores y hooks propios no necesitan ser plugins; basta con módulos Python normales.

#### ¿Qué son los listeners?

Ganchos sobre los eventos de Airflow (inicio o fin de un DAG run, cambios de estado de las task instances) implementados con pluggy, usados para linaje (OpenLineage), auditoría o notificaciones propias.

#### ¿Qué es OpenLineage en Airflow?

Un estándar de metadatos de linaje. El provider de OpenLineage emite eventos que describen las entradas y salidas de las tareas hacia un backend como Marquez o un catálogo de datos, para ver qué jobs leen y escriben qué datasets.

<!-- challenge -->

Cumplimiento pregunta qué dashboards dependen de una tabla de clientes cargada por Airflow. ¿Cómo podría responderlo el linaje automáticamente?

<!-- solution -->

Activar el provider de OpenLineage para que las tareas emitan sus datasets de entrada y salida, enviar los eventos a un backend de linaje que también reciba eventos de dbt y de las herramientas de BI, y consultar el grafo aguas abajo de la tabla de clientes.

<!-- takeaways -->

- Los plugins extienden la UI y el scheduling; los listeners reaccionan a eventos.
- OpenLineage emite automáticamente entradas y salidas de las tareas.
- El linaje responde preguntas de impacto entre herramientas.

<!-- stage: Integrarlo todo -->

### Escenarios

<!-- unit: Diseñar un DAG ELT diario -->

<!-- goals -->

- Combinar sensores, cargas, dbt y chequeos en un DAG diario.
- Justificar cada elección en una respuesta de entrevista.

<!-- concept -->

Las preguntas de diseño prueban si sabes conectar las piezas: cuándo están listos los datos, cómo se cargan de forma idempotente, cómo corren las transformaciones, cómo afloran los fallos. Una respuesta sólida sigue a los datos, nombra una herramienta por paso y explica qué pasa al re-ejecutar y a quién se alerta. Mencionar esperas deferrable, cargas por intervalo y tareas dbt por modelo muestra que conoces las trampas de producción.

<!-- example -->

```text
wait_for_files (deferrable S3KeySensor, timeout 6h)
  ─► copy_into_snowflake (interval's prefix, idempotent)
  ─► dbt models (Cosmos task group)
  ─► data checks ─► asset event: marts.sales
```

#### Un DAG diario debe cargar los archivos de ayer desde S3 en Snowflake y luego ejecutar dbt. Diséñalo.

Un DAG diario con `catchup=False` (o true si importa el historial), un `S3KeySensor` diferible sobre el prefijo esperado del intervalo de datos, un `CopyFromExternalStageToSnowflakeOperator` o una tarea SQL que ejecute `COPY INTO`, luego dbt con Cosmos o un operador de dbt Cloud, controles de calidad de datos y callbacks de fallo hacia Slack. Todas las rutas y filtros salen del intervalo de datos.

<!-- challenge -->

El equipo de origen avisa que los archivos pueden corregirse y reenviarse hasta tres días después. Ajusta el diseño.

<!-- solution -->

Procesar los últimos tres intervalos en cada ejecución, o disparar re-ejecuciones ante archivos nuevos con asset watchers. Hacer que la carga en Snowflake reemplace el tramo de cada día (delete e insert, o `MERGE`) para que las correcciones sobrescriban, y dejar que dbt reconstruya los días afectados.

<!-- takeaways -->

- Sigue a los datos desde su llegada hasta los consumidores, una herramienta por paso.
- Las cargas idempotentes por intervalo hacen seguras las re-ejecuciones.
- Termina con chequeos, alertas y lo que reciben los consumidores.

<!-- unit: Condicionar un reporte a la calidad de los datos -->

<!-- goals -->

- Disparar un reporte solo cuando sus entradas están completas y correctas.
- Decidir qué pasa cuando la compuerta falla.

<!-- concept -->

A los usuarios de negocio les importa más que un reporte sea correcto que puntual. Un buen diseño hace explícita la completitud: el reporte depende de los datos, no de un reloj, y un chequeo compara lo que llegó con lo esperado antes de enviar nada. Si el chequeo falla, lo correcto es avisar a alguien y no enviar, en vez de mandar por correo una cifra equivocada.

<!-- example -->

```python
@dag(schedule=[Asset("snowflake://analytics/sales_daily")])
def sales_report():
    check = SQLCheckOperator(task_id="complete",
        conn_id="warehouse",
        sql="SELECT count(*) >= 0.95 * expected FROM sales_completeness WHERE day = '{{ ds }}'")
    check >> send_report()
```

#### Una persona de negocio quiere recibir un reporte por correo solo si las ventas de ayer están completas. ¿Cómo?

Programo el DAG del reporte sobre el asset de ventas (o con un sensor sobre la carga), añado un control de calidad (número de filas y completitud frente a los orígenes esperados), corto el envío del correo si los controles fallan y, en ese caso, alerto al equipo de datos.

<!-- challenge -->

Una mañana el chequeo falla porque una sola tienda no envió datos. El negocio igual quiere el reporte, etiquetado. ¿Qué cambias?

<!-- solution -->

Hacer que el chequeo devuelva qué tiendas faltan y bifurcar: enviar el reporte con un aviso de "datos parciales" que las liste y alertar a los responsables. Mantener un freno total solo cuando la completitud cae bajo un umbral acordado.

<!-- takeaways -->

- Programa los reportes por datos, no por reloj.
- Revisa la completitud antes de enviar.
- Acuerda con los usuarios qué deben producir los datos parciales.
