## Guía de estudio de dbt

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de dbt: unas 200 preguntas](../../images/dbt_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre dbt (data build tool), desde lo básico hasta los modelos incrementales, los snapshots, los tests, el despliegue y el rendimiento. Las respuestas siguen las convenciones de dbt Core 1.x.

La guía sigue una ruta de aprendizaje en cuatro etapas. Cada sección se divide en unidades cortas: objetivos de aprendizaje, una explicación del concepto y un ejemplo resuelto, luego preguntas (primero de memoria, después de aplicación), un reto práctico e ideas clave. Para **aprender**, lee cada unidad de principio a fin. Para **repasar**, cambia al modo repaso o usa "Ir a las preguntas", marca las respuestas que quieras volver a ver y prueba un repaso mixto entre secciones.

<!-- QA -->
<!-- stage: Fundamentos -->

### Fundamentos

<!-- unit: Qué es dbt -->

<!-- goals -->

- Explicar qué hace dbt y dónde encaja en ELT.
- Comparar dbt con herramientas ETL y stored procedures, incluidos sus límites.

<!-- concept -->

Una vez cargados los datos crudos en un warehouse, alguien tiene que convertirlos en tablas limpias y confiables. Durante años eso significó stored procedures y scripts corridos en un orden fijo que solo entendía su autor. dbt los reemplaza con un framework: cada transformación es un `SELECT` en un archivo, las dependencias se declaran en el código y dbt construye todo en el orden correcto dentro del warehouse.
Con él llegan prácticas de software: control de versiones, pruebas, documentación y revisiones. Lo que dbt no hace es traer datos ni programarse solo.

<!-- example -->

```sql
-- models/marts/fct_orders.sql
select
    o.order_id,
    o.customer_id,
    o.ordered_at,
    sum(p.amount) as amount
from {{ ref('stg_shop__orders') }} o
left join {{ ref('stg_shop__payments') }} p using (order_id)
group by 1, 2, 3
```

#### ¿Qué es dbt?

dbt (data build tool) es un framework de transformación: escribes sentencias `SELECT` como modelos, y dbt las compila con Jinja, deduce sus dependencias y las ejecuta en tu almacén de datos como tablas o vistas. Lleva a las transformaciones SQL las prácticas de la ingeniería de software (control de versiones, tests, documentación, modularidad, CI/CD). dbt es la "T" de ELT.

#### ¿Cuáles son los casos de uso habituales de dbt?

Construir un almacén de datos o lakehouse capa a capa (staging, intermedia, marts), limpiar y normalizar datos en bruto, construir modelos dimensionales para BI, historizar datos que cambian lentamente con snapshots, comprobar la calidad de los datos, documentar los conjuntos de datos con su linaje y definir métricas de negocio compartidas en la capa semántica.

#### ¿En qué se diferencia dbt de las herramientas ETL tradicionales?

Las herramientas ETL tradicionales extraen, transforman en su propio motor y luego cargan, a menudo mediante una interfaz gráfica. dbt solo transforma, dentro del almacén que ya contiene los datos cargados (ELT), con SQL en archivos de texto. Todo es código: versionado en Git, revisado, probado y desplegado como software. La extracción y la carga se dejan a otras herramientas (Fivetran, Airbyte, pipelines propios).

#### ¿Cómo se compara dbt con Apache Spark?

Spark es un motor de procesamiento distribuido que programas en Python, Scala o SQL, y cuyos trabajos y clústeres gestionas. dbt no es un motor: genera SQL y lo envía a un motor (Snowflake, BigQuery, Redshift, Databricks, Postgres, y el propio Spark mediante los adaptadores dbt-spark o dbt-databricks). Son complementarios: dbt puede orquestar transformaciones SQL que ejecuta Spark, mientras que el procesamiento complejo que no es SQL se queda en código Spark.

#### ¿Qué significa ELT y por qué encaja dbt con este enfoque?

Extract, Load, Transform: los datos en bruto se cargan primero en el almacén y se transforman allí. Los almacenes modernos son baratos para guardar y potentes para calcular, así que transformar en SQL donde ya están los datos es más sencillo y escala. dbt aporta la estructura a esa etapa de transformación.

#### ¿Qué diferencia hay entre dbt Core y dbt Cloud?

dbt Core es la herramienta de línea de comandos de código abierto (Apache 2.0): la instalas, la ejecutas y la orquestas tú. dbt Cloud (hoy parte de la dbt platform) es el servicio comercial gestionado: un IDE web, un planificador de trabajos, CI, documentación alojada, la capa semántica, alertas y control de accesos. Los dos ejecutan el mismo código de proyecto.

<!-- challenge -->

Un equipo tiene 80 stored procedures que un scheduler corre en un orden mantenido a mano. Nombra dos mejoras concretas que traería dbt y una cosa que seguirían necesitando.

<!-- solution -->

dbt derivaría el orden de ejecución de las dependencias `ref()` y agregaría pruebas y documentación junto al código en Git. Seguirían necesitando la ingesta al warehouse y un orquestador o scheduler que corra dbt.

<!-- takeaways -->

- dbt convierte sentencias `SELECT` en tablas y vistas administradas.
- Dependencias, pruebas y docs viven con el código.
- La ingesta y la orquestación quedan por fuera de dbt.

<!-- unit: dbt en el ecosistema -->

<!-- goals -->

- Comparar dbt con Spark y distinguir dbt Core de la plataforma dbt.
- Explicar los adapters, dbt Fusion y la Semantic Layer.

<!-- concept -->

dbt no es un motor. Genera SQL (o Python) y lo envía a una plataforma a través de un adapter, así el warehouse hace el trabajo. Por eso se combina con plataformas basadas en Spark en lugar de competir con ellas.
Viene en dos formas: el CLI open source que corres tú mismo y una plataforma administrada que agrega IDE, programación y funciones alojadas. El ecosistema sigue creciendo, con un motor más rápido en Rust y una capa semántica que define las métricas una vez para todas las herramientas.

<!-- example -->

| Pieza | Rol |
|---|---|
| dbt Core | CLI open source: compile, run, test |
| Plataforma dbt (Cloud) | IDE, jobs, CI, docs alojados, API de Semantic Layer |
| Adapter | Habla con Snowflake, BigQuery, Databricks, Postgres... |
| dbt Fusion | Motor en Rust: parseo más rápido, entiende SQL |

#### ¿Qué es un adaptador de dbt?

Un plugin que permite a dbt hablar con una plataforma de datos concreta, traduciendo las operaciones genéricas de dbt al dialecto SQL de esa plataforma: dbt-postgres, dbt-snowflake, dbt-bigquery, dbt-redshift, dbt-databricks, dbt-spark y muchos adaptadores de la comunidad.

#### ¿Qué es un modelo de dbt?

Un archivo `.sql` de la carpeta `models/` que contiene una sentencia `SELECT`. dbt la envuelve en el DDL necesario para crear una vista, tabla u otro objeto con el nombre del archivo. En algunas plataformas también se admiten modelos Python (`.py`).

#### ¿Qué es el DAG en el contexto de dbt?

El grafo acíclico dirigido de dependencias entre modelos, sources, seeds y snapshots, construido a partir de las llamadas a `ref()` y `source()`. dbt lo usa para ejecutar los nodos en el orden correcto (y en paralelo cuando es posible), para seleccionar partes del proyecto y para dibujar el linaje en la documentación.

#### ¿Cuáles son los retos de dbt?

Solo cubre la transformación, así que hacen falta otras herramientas para la ingesta y la orquestación. Los proyectos grandes pueden volverse lentos de compilar y difíciles de recorrer sin convenciones. Los modelos incrementales y los snapshots requieren un diseño cuidadoso. Jinja puede volver ilegible el SQL si se abusa de él. El rendimiento sigue dependiendo del almacén y del SQL que escribas, y los costos pueden dispararse si se hacen full refresh con demasiada frecuencia.

#### ¿Qué problemas resuelve dbt frente a los procedimientos almacenados y los scripts?

Las dependencias son explícitas y se resuelven solas, el código es modular y reutilizable gracias a `ref` y las macros, los tests y la documentación viven junto al código, los entornos se cambian por configuración y no editando, y todo está versionado y se puede revisar.

<!-- challenge -->

Un equipo en Databricks pregunta si usar dbt o Spark para las transformaciones. ¿Qué respondes?

<!-- solution -->

Ambos: dbt puede correr modelos SQL (y Python) en Databricks con el adapter, y Spark los ejecuta. Usa dbt para modelado amigable con SQL, con pruebas y linaje; usa jobs de Spark directamente para procesamiento complejo con mucho código.

<!-- takeaways -->

- dbt genera código; la plataforma lo ejecuta.
- Core es el CLI; la plataforma agrega funciones administradas.
- Los adapters conectan dbt con cada plataforma de datos.

<!-- unit: Modelos y el DAG -->

<!-- goals -->

- Describir los modelos de dbt y el DAG que forman sus referencias.
- Elegir entre modelos SQL y Python y diseñar capas modulares.

<!-- concept -->

Un modelo es un archivo con un `SELECT`. Cuando referencia otro modelo con `ref()`, dbt registra una arista, y todas las aristas forman un DAG que decide el orden de construcción y qué puede correr en paralelo.
Eso abarata la modularidad: modelos pequeños con una sola responsabilidad, reutilizados por muchos modelos aguas abajo. Los modelos Python sirven para las pocas transformaciones que SQL maneja mal, y siguen en el mismo DAG.

<!-- example -->

```python
# models/ml/customer_features.py
def model(dbt, session):
    orders = dbt.ref("fct_orders").to_pandas()
    feats = orders.groupby("customer_id").agg(orders=("order_id", "count"), spend=("amount", "sum"))
    return feats.reset_index()
```

#### ¿Qué comandos de dbt son los más habituales?

`dbt run` (construir modelos), `dbt test` (ejecutar tests), `dbt build` (run, test, snapshot y seed en el orden del DAG), `dbt seed`, `dbt snapshot`, `dbt compile`, `dbt docs generate` / `dbt docs serve`, `dbt debug`, `dbt deps`, `dbt clean`, `dbt ls`, `dbt source freshness` y `dbt run-operation`.

#### ¿Qué hace `dbt build`?

Ejecuta seeds, modelos, snapshots y tests en el orden del DAG. Si un test falla en un nodo, los nodos que dependen de él se omiten, para que los datos erróneos no se propaguen.

#### ¿Para qué sirve `dbt debug`?

Comprueba la instalación, `dbt_project.yml`, `profiles.yml` y la conexión con el almacén. Es lo primero que hay que ejecutar cuando nada funciona.

#### ¿Qué diferencia hay entre `dbt run` y `dbt compile`?

`dbt compile` renderiza el Jinja y escribe el SQL resultante en `target/compiled/` sin ejecutar nada. `dbt run` compila y ejecuta, y escribe las sentencias ejecutadas (con su DDL) en `target/run/`.

#### ¿En qué lenguajes se pueden escribir los modelos de dbt?

En SQL (con Jinja) en todas partes, y en Python en Snowflake (Snowpark), Databricks y BigQuery (Dataproc). Los modelos Python devuelven un DataFrame y son útiles para la lógica que es incómoda en SQL.

<!-- challenge -->

Cinco modelos de mart repiten el mismo join de 40 líneas entre órdenes y pagos. ¿Cómo los reestructuras?

<!-- solution -->

Extrae el join a un modelo intermedio (por ejemplo `int_orders_with_payments`) y haz que los cinco marts lo referencien con `ref()`. La lógica vive una vez y el DAG muestra la dependencia compartida.

<!-- takeaways -->

- Un modelo es un `SELECT` en un archivo.
- `ref()` construye el DAG y el orden de ejecución.
- Los modelos pequeños y de un solo propósito se reutilizan fácil.

<!-- unit: Comandos principales -->

<!-- goals -->

- Usar los comandos de dbt más comunes.
- Explicar qué hacen `dbt build`, `dbt debug` y `dbt compile`.

<!-- concept -->

Un puñado de comandos cubre el trabajo diario. Run construye modelos; test los revisa; build hace ambas cosas, más seeds y snapshots, en orden del DAG y salta lo que depende de una falla. Compile renderiza el SQL sin ejecutarlo, y así ves lo que dbt va a enviar de verdad. Debug revisa la configuración y la conexión.
Saber qué comando usar ahorra tiempo y evita construir encima de datos rotos.

<!-- example -->

```bash
dbt debug                           # config and connection OK?
dbt compile --select fct_orders     # see rendered SQL in target/compiled
dbt build --select +fct_orders      # build and test fct_orders and its parents
```

#### ¿Qué es un modelo Python en dbt?

Un archivo `.py` que define `model(dbt, session)` y devuelve un DataFrame. Puede referenciar otros modelos con `dbt.ref()` y se materializa como tabla o como modelo incremental.

```python
def model(dbt, session):
    dbt.config(materialized="table")
    orders = dbt.ref("stg_orders")
    return orders.groupBy("customer_id").count()
```

#### ¿Qué es dbt Fusion?

Un nuevo motor de dbt escrito en Rust, presentado en 2025, que analiza y compila los proyectos mucho más rápido y entiende el SQL semánticamente (linaje a nivel de columna, detección de errores antes de llegar al almacén). Es la base de la extensión de dbt para VS Code y de la dbt platform.

#### ¿Qué es la capa semántica de dbt?

Una capa, basada en MetricFlow, donde las métricas (ingresos, usuarios activos) se definen una sola vez en YAML sobre modelos semánticos y luego se consultan de forma coherente desde BI y otras herramientas a través de API, para que todas calculen la métrica igual.

#### ¿Qué significa "modelado de datos modular" en dbt?

Dividir las transformaciones en modelos pequeños y reutilizables con una sola responsabilidad (staging por fuente, lógica intermedia, marts finales), conectados con `ref`, en lugar de consultas monolíticas enormes.

<!-- challenge -->

Un job de producción corre `dbt run` y luego `dbt test`. Un modelo de staging roto produjo duplicados, y todos los modelos aguas abajo se reconstruyeron con ellos antes de que fallaran las pruebas. ¿Qué cambias?

<!-- solution -->

Usa `dbt build`, que prueba cada nodo justo después de construirlo y salta a sus hijos cuando falla una prueba, para que los datos malos no se propaguen.

<!-- takeaways -->

- `build` = run + test + seed + snapshot en orden del DAG.
- `compile` muestra el SQL sin ejecutarlo.
- `debug` revisa configuración y conexión.

### Proyectos y configuración

<!-- unit: Archivos de proyecto y conexión -->

<!-- goals -->

- Describir `dbt_project.yml`, `profiles.yml`, targets y threads.
- Guardar las credenciales en variables de ambiente.

<!-- concept -->

Un proyecto dbt tiene dos tipos de configuración. El archivo de proyecto viaja con el código: nombre, rutas, configuraciones por defecto por carpeta. El profile se queda con la persona o la máquina que corre dbt: qué plataforma, qué credenciales, qué target, como `dev` o `prod`.
Esa división permite que un mismo código construya en muchos ambientes. Las variables de ambiente la completan y mantienen los secretos fuera de todos los archivos.

<!-- example -->

```yaml
# profiles.yml
shop:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('DBT_USER') }}"
      password: "{{ env_var('DBT_PASSWORD') }}"
      database: analytics_dev
      schema: "dbt_{{ env_var('USER') }}"
      threads: 8
```

#### ¿Qué es un proyecto de dbt?

Un directorio que contiene un archivo `dbt_project.yml` además de modelos, tests, macros, seeds, snapshots, análisis y documentación. Es la unidad que dbt compila y ejecuta, normalmente un repositorio Git.

#### ¿Cuál es la estructura de un proyecto?

La organización recomendada:

```
dbt_project.yml
models/
  staging/<source>/      modelos stg_: uno por tabla de origen, limpieza ligera
  intermediate/          modelos int_: joins y lógica de negocio
  marts/                 modelos fct_ y dim_ que consumen los usuarios
seeds/        datos de referencia pequeños en CSV
snapshots/    historial SCD tipo 2
macros/       Jinja reutilizable
tests/        tests de datos singulares
analyses/     SQL que se compila pero no se ejecuta
```

#### ¿Qué va en `dbt_project.yml`?

El nombre y la versión del proyecto, el `profile` que se usa, las rutas (models, seeds, macros…), las `vars` y las configuraciones por defecto de cada carpeta, como `+materialized: table` para todos los marts o `+schema: staging`.

#### ¿Qué es `profiles.yml`?

El archivo (por defecto en `~/.dbt/`) que contiene los datos de conexión de cada perfil y target: tipo de adaptador, host, base de datos, esquema, credenciales y threads. Se mantiene fuera del repositorio del proyecto porque contiene secretos. Los valores pueden venir de variables de entorno con `env_var()`.

#### ¿Qué es un target en dbt?

Una configuración de conexión con nombre dentro de un perfil, como `dev` y `prod`. Se elige con `--target`, y los modelos pueden bifurcar según `target.name`.

#### ¿Qué son los threads en dbt?

El número máximo de modelos que dbt ejecuta a la vez. Las ramas independientes del DAG se ejecutan en paralelo hasta ese límite.

<!-- challenge -->

Un desarrollador hizo commit de `profiles.yml` con una contraseña de producción. ¿Qué cambias?

<!-- solution -->

Rota la contraseña, bórrala del historial del repositorio y reescribe el profile para leer las credenciales con `env_var()`. En CI y producción, inyéctalas desde un gestor de secretos.

<!-- takeaways -->

- `dbt_project.yml` viaja con el código.
- `profiles.yml` guarda conexiones y targets por ambiente.
- Las credenciales salen de variables de ambiente.

<!-- unit: Configurar nodos -->

<!-- goals -->

- Configurar modelos a nivel de archivo, YAML y proyecto.
- Seleccionar nodos con tags, selectors y variables.

<!-- concept -->

La configuración va de lo general a lo específico: valores por defecto por carpeta en el proyecto, sobrescritos en YAML y otra vez en el archivo del modelo. Las configs cambian cómo dbt construye algo; las properties lo describen. Tener clara esa distinción evita la mayoría de preguntas del tipo "¿por qué no se aplicó mi ajuste?".
La selección permite actuar sobre parte del DAG: por nombre, ruta, tag, estado u operadores de grafo. Las variables hacen que el mismo código se comporte distinto en cada ejecución.

<!-- example -->

```bash
dbt build --select tag:daily
dbt build --select +fct_orders+          # parents, the model, children
dbt run --select path:models/marts --exclude tag:deprecated
dbt run --vars '{start_date: "2026-10-01"}'
```

#### ¿Cómo se configura un modelo?

En tres sitios, del más al menos específico: un bloque `{{ config(...) }}` en el archivo del modelo, un bloque `config:` en las propiedades YAML del modelo y los ajustes por carpeta en `dbt_project.yml`. Gana el más específico.

```sql
{{ config(materialized='table', schema='marts', tags=['daily']) }}
select * from {{ ref('int_orders') }}
```

#### ¿Qué diferencia hay entre configs y properties?

Las configs controlan cómo construye dbt un nodo (materialización, esquema, etiquetas, hooks). Las properties lo describen (descripción, columnas, tests, documentación). Las properties viven en archivos YAML. Las configs pueden estar en YAML, en el archivo del modelo o en `dbt_project.yml`.

#### ¿Para qué sirven las etiquetas (tags)?

Para marcar nodos y seleccionarlos en los comandos, por ejemplo `dbt run --select tag:daily`, o agruparlos en trabajos.

#### ¿Cómo funciona la selección de nodos?

Con `--select` y `--exclude`, usando nombres, rutas, etiquetas, `source:`, `state:`, `resource_type:` y operadores de grafo: `+model` selecciona el modelo y sus padres, `model+` el modelo y sus hijos, `@model` el modelo, sus hijos y los padres de estos.

```bash
dbt build --select +fct_orders          # fct_orders y todo lo que tiene aguas arriba
dbt run --select staging.stripe         # una carpeta
dbt test --select source:stripe+        # tests de una source y de todo lo que depende de ella
```

#### ¿Qué son los paquetes y cómo se instalan?

Proyectos dbt reutilizables (macros, modelos, tests) como `dbt_utils`, `dbt_expectations` o `codegen`. Se listan en `packages.yml` (o `dependencies.yml`) y se instalan con `dbt deps`.

<!-- challenge -->

Todos los marts deben ser tablas, salvo un modelo grande que debe ser incremental. ¿Dónde pones cada config?

<!-- solution -->

Pon `+materialized: table` para la carpeta de marts en `dbt_project.yml` y sobrescribe con `{{ config(materialized='incremental', unique_key=...) }}` en el archivo del modelo grande, que tiene prioridad.

<!-- takeaways -->

- Las configs bajan en cascada del proyecto al YAML y al archivo.
- Las configs cambian los builds; las properties describen nodos.
- La selección apunta a partes del DAG.

<!-- unit: Estructura y esquemas -->

<!-- goals -->

- Organizar un proyecto en carpetas y capas.
- Controlar los nombres de esquema con `generate_schema_name`.

<!-- concept -->

Una estructura de carpetas consistente le dice a todos dónde va cada cosa: staging por fuente, intermediate para lógica compartida, marts por área de negocio. Las configs por carpeta aplican luego materializaciones y esquemas a capas completas.
Por defecto dbt agrega el esquema personalizado al esquema del target, lo que protege a los desarrolladores de escribir en esquemas de producción. Los equipos suelen sobrescribir la macro para que producción tenga nombres limpios mientras desarrollo sigue aislado. Analyses y comandos de limpieza completan la organización del proyecto.

<!-- example -->

```sql
-- macros/generate_schema_name.sql
{% macro generate_schema_name(custom_schema_name, node) -%}
  {%- if target.name == 'prod' and custom_schema_name is not none -%}
    {{ custom_schema_name | trim }}
  {%- else -%}
    {{ target.schema }}{% if custom_schema_name %}_{{ custom_schema_name | trim }}{% endif %}
  {%- endif -%}
{%- endmacro %}
```

#### ¿Qué es `dbt_utils`?

El paquete más usado, con tests genéricos (`unique_combination_of_columns`, `expression_is_true`, `accepted_range`) y macros (`generate_surrogate_key`, `star`, `date_spine`, `pivot`, `union_relations`).

#### ¿Qué son las variables (`vars`) en dbt?

Valores definidos en `dbt_project.yml` o pasados por la línea de comandos (`--vars '{start_date: 2026-01-01}'`) que se leen con `{{ var('start_date') }}`.

#### ¿Cómo se usan las variables de entorno en dbt?

Con `{{ env_var('DBT_PASSWORD') }}`, opcionalmente con un valor por defecto. Se usan mucho en `profiles.yml` para las credenciales, y las variables con el prefijo `DBT_ENV_SECRET_` se ocultan en los registros.

#### ¿Cómo decide dbt en qué esquema se construye un modelo?

Mediante la macro `generate_schema_name`. Por defecto, un esquema personalizado se añade al esquema del target (`dbt_alice_marts` en dev, `analytics_marts` en prod). Muchos proyectos sobrescriben la macro para usar el esquema personalizado tal cual en producción.

#### ¿Qué es la macro `generate_schema_name` y por qué sobrescribirla?

Calcula el esquema de cada nodo. Sobrescribirla permite, por ejemplo, usar nombres de esquema exactos en producción y mantener un prefijo personal en desarrollo, para que los desarrolladores no se pisen.

<!-- challenge -->

Los modelos de producción caen en esquemas como `analytics_marts` en lugar de `marts`, y a los analistas los nombres les confunden. ¿Qué cambias sin afectar a los desarrolladores?

<!-- solution -->

Sobrescribe `generate_schema_name` para que en el target prod se use el esquema personalizado tal cual (`marts`), mientras los demás targets conservan la forma con prefijo (`dbt_ana_marts`) para seguir aislados.

<!-- takeaways -->

- Organiza por capa: staging, intermediate, marts.
- dbt agrega por defecto los esquemas personalizados al del target.
- Sobrescribe el nombrado de esquemas para nombres limpios en producción.

<!-- unit: Paquetes y gobierno -->

<!-- goals -->

- Instalar y usar paquetes como `dbt_utils`.
- Gobernar modelos públicos con access, groups y versiones.

<!-- concept -->

Los paquetes son proyectos dbt que importas: pruebas, macros y modelos que otros ya escribieron y probaron. La mayoría de proyectos arranca con `dbt_utils` para pruebas y utilidades comunes.
Cuando los proyectos crecen y sirven a otros equipos, los modelos se vuelven interfaces. Los niveles de acceso y los grupos deciden quién puede referenciar qué, y las versiones permiten que un cambio que rompe salga como versión nueva mientras los consumidores migran a su ritmo.

<!-- example -->

```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: [">=1.3.0", "<2.0.0"]
# models/marts/_marts.yml
models:
  - name: fct_orders
    access: public
    group: finance
    latest_version: 2
    versions: [{v: 1}, {v: 2}]
```

#### ¿Qué son los analyses en dbt?

Archivos SQL de `analyses/` que se compilan (con Jinja y `ref` resueltos) pero que `dbt run` nunca ejecuta. Son útiles para consultas puntuales que se benefician de las referencias de dbt.

#### ¿Qué hace `dbt clean`?

Borra las carpetas listadas en `clean-targets` (normalmente `target/` y `dbt_packages/`).

#### ¿Qué son el acceso a modelos y los grupos?

Funciones de gobierno. El `access` de un modelo puede ser `private` (solo referenciable dentro de su grupo), `protected` (dentro del proyecto, el valor por defecto) o `public` (desde otros proyectos). Los grupos asignan la propiedad de un conjunto de modelos.

#### ¿Qué son las versiones de modelos?

Una forma de publicar una nueva versión de un modelo público (`fct_orders_v2`) mientras los consumidores siguen usando la antigua hasta migrar, con `ref('fct_orders', v=1)`.

<!-- challenge -->

Otro equipo referencia directamente tus modelos intermedios, y cada refactor los rompe. ¿Cómo pones límites?

<!-- solution -->

Pon tus modelos en un group, marca los intermedios como `private` (o `protected`) y expón como `public`, con contratos, solo los marts que necesitan. Los cambios que rompen pasan entonces por versiones de modelo.

<!-- takeaways -->

- Los paquetes traen pruebas y macros ya probados.
- Access y groups definen las interfaces de los modelos.
- Las versiones dejan convivir cambios que rompen.

<!-- stage: Construir modelos -->

### Sources y seeds

<!-- unit: Sources y frescura -->

<!-- goals -->

- Declarar sources y referenciarlas con `source()`.
- Probar las sources y revisar su frescura.

<!-- concept -->

Las tablas crudas que cargan otras herramientas son las entradas de dbt. Declararlas como sources pone su ubicación en un solo lugar, arranca el linaje en el punto correcto y permite probarlas y revisarlas antes de construir algo encima.
Los chequeos de frescura responden una pregunta que las pruebas no: ¿llegaron datos nuevos? Correrlos primero en producción evita que los modelos se reconstruyan en silencio sobre datos viejos.

<!-- example -->

```yaml
sources:
  - name: shop
    database: raw
    schema: shop
    loaded_at_field: _loaded_at
    freshness:
      warn_after: {count: 6, period: hour}
      error_after: {count: 24, period: hour}
    tables:
      - name: orders
        columns:
          - name: id
            data_tests: [unique, not_null]
```

#### ¿Qué son las sources en dbt?

Declaraciones, en YAML, de las tablas en bruto que otras herramientas cargaron en el almacén. Los modelos seleccionan de ellas con `{{ source('stripe', 'payments') }}` en lugar de nombres de tabla escritos a mano, lo que registra el linaje, permite tests y documentación sobre los datos en bruto y habilita las comprobaciones de frescura.

```yaml
sources:
  - name: stripe
    database: raw
    schema: stripe
    tables:
      - name: payments
        loaded_at_field: _loaded_at
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
```

#### ¿Por qué usar `source()` en lugar de escribir el nombre de la tabla?

La ubicación de la tabla se define en un solo sitio, el linaje empieza en la source dentro del DAG, las sources se pueden seleccionar (`source:stripe+`) y `dbt source freshness` puede comprobarlas.

#### ¿Qué es la frescura de las sources (source freshness)?

Una comprobación, que se lanza con `dbt source freshness`, que compara el máximo de `loaded_at_field` con la hora actual y avisa o falla cuando los datos son más antiguos que los umbrales configurados.

#### ¿Se pueden testear las sources?

Sí, los tests genéricos se declaran en las columnas de las sources exactamente igual que en los modelos, y detectan problemas en los datos en bruto antes de que lleguen a tus modelos.

#### ¿Qué es un modelo de staging?

La primera capa sobre una source: un modelo por tabla de origen, con transformaciones ligeras (renombrar, convertir tipos, limpieza básica, deduplicación). Todo lo que viene después referencia modelos de staging, no sources directamente.

#### ¿Por qué solo los modelos de staging deben referenciar sources?

Para que cada tabla en bruto se limpie una sola vez, en un único sitio. Si la source cambia, solo hay que actualizar su modelo de staging.

<!-- challenge -->

Un job de ingesta falló dos días y los dashboards mostraron cifras planas sin que nadie lo notara. ¿Qué función de dbt lo habría atrapado?

<!-- solution -->

Source freshness sobre las tablas crudas con umbrales `error_after`, corrida como primer paso del job de producción (y alertando ante fallas), para que el job se detenga y se avise al equipo.

<!-- takeaways -->

- Las sources declaran las entradas crudas en un solo lugar.
- `source()` para tablas crudas; `ref()` para nodos de dbt.
- Los chequeos de frescura atrapan ingestas tardías o rotas.

<!-- unit: Staging y capas -->

<!-- goals -->

- Escribir modelos de staging como únicos consumidores de las sources.
- Explicar las capas staging, intermediate y marts entre ambientes.

<!-- concept -->

Los modelos de staging son la entrada limpia: uno por tabla fuente, con renombres, casts y limpieza ligera, sin joins ni lógica de negocio. Si solo staging lee las sources, un cambio en la fuente toca un archivo.
Las capas se apoyan en eso: los modelos intermedios guardan joins y lógica reutilizable, los marts sirven a los consumidores. Como `ref()` resuelve al target actual, las mismas capas se construyen en el esquema de un desarrollador o en producción sin cambiar código.

<!-- example -->

```sql
-- models/staging/shop/stg_shop__orders.sql
select
    id::bigint            as order_id,
    customer_id::bigint   as customer_id,
    lower(status)         as status,
    created_at::timestamp as ordered_at
from {{ source('shop', 'orders') }}
```

#### ¿Qué es un seed?

Un archivo CSV de la carpeta `seeds/` que `dbt seed` carga en el almacén como tabla. Los modelos lo referencian con `ref()` como a cualquier modelo.

#### ¿Cuándo usar seeds y cuándo no?

Para datos de referencia pequeños y estáticos que cambian poco y deben estar en el control de versiones: códigos de país, tablas de correspondencia, datos de prueba. No para datos grandes o que cambian a menudo, ni para datos que deberían venir de un sistema de origen.

#### ¿Cómo se fijan los tipos de columna de un seed?

Con `column_types` en la configuración del seed. Si no, dbt los infiere:

```yaml
seeds:
  my_project:
    country_codes:
      +column_types:
        code: varchar(2)
```

#### ¿Cómo se recarga un seed cuyas columnas han cambiado?

Con `dbt seed --full-refresh`, que elimina y vuelve a crear la tabla en lugar de vaciarla e insertar.

#### ¿Puede dbt trabajar con distintas fuentes de datos y almacenes?

dbt trabaja con una plataforma de datos por target, a través de su adaptador, y transforma datos que ya están en esa plataforma. No extrae de los sistemas de origen. Las plataformas que pueden consultar datos externos (tablas externas de Snowflake, consultas federadas de BigQuery, catálogos de Databricks y Trino) permiten a dbt transformar datos de varios orígenes a través del almacén.

<!-- challenge -->

Una fuente renombra `created_at` a `created_ts`, y se rompen nueve modelos. ¿Cómo habrían limitado el daño las capas?

<!-- solution -->

Si solo `stg_shop__orders` leyera la fuente, el arreglo sería una línea ahí (`created_ts as ordered_at`); todos los modelos aguas abajo usan el nombre de columna de staging y no cambian.

<!-- takeaways -->

- Staging: un modelo por tabla fuente, solo limpieza ligera.
- Solo staging lee las sources.
- `ref()` resuelve por target, así las capas funcionan en todo ambiente.

<!-- unit: Seeds -->

<!-- goals -->

- Decidir cuándo encajan los seeds y cuándo no.
- Fijar tipos de columnas de los seeds y recargar los que cambian.

<!-- concept -->

Los seeds cargan al warehouse archivos CSV pequeños del repositorio. Son ideales para datos de referencia estáticos que deben estar en control de versiones, como códigos de país o tablas de mapeo, y se revisan como código.
Son la herramienta equivocada para algo grande, sensible o que cambia seguido; eso va en la ingesta. Los tipos deben fijarse explícitamente, porque la inferencia adivina, y los cambios de columnas necesitan un full refresh.

<!-- example -->

```yaml
seeds:
  shop:
    country_codes:
      +column_types:
        iso_code: varchar(2)
        dial_code: varchar(6)
```
```bash
dbt seed --select country_codes --full-refresh
```

#### ¿Qué diferencia hay entre `ref()` y `source()`?

`ref()` apunta a otro nodo de dbt (modelo, seed, snapshot) y crea una dependencia que el DAG usa para ordenar las ejecuciones. `source()` apunta a datos en bruto cargados fuera de dbt. Ambos se resuelven al nombre completo de la tabla en el target actual.

#### ¿A qué se resuelve `ref()` en entornos distintos?

A la relación en la base de datos y el esquema del target actual, así que el mismo código construye en el esquema de un desarrollador en dev y en los esquemas de producción en prod.

#### ¿Qué es la organización en capas "staging, intermediate, marts"?

Una estructura habitual: staging limpia cada source, intermediate contiene joins y lógica de negocio reutilizables, y los marts son las tablas de hechos y dimensiones finales (o tablas anchas) que consumen BI y los analistas.

#### ¿Para qué se usa `dbt source freshness` en producción?

Para detectar una ingesta rota o retrasada antes de que los modelos se ejecuten sobre datos obsoletos, a menudo como primer paso de un trabajo programado.

<!-- challenge -->

Un equipo carga como seed una exportación diaria de 300 MB de precios de productos. ¿Qué sugieres?

<!-- solution -->

Pasarla a la capa de ingesta (un loader o conector hacia una tabla cruda declarada como source). Los seeds son para datos de referencia pequeños y estáticos versionados en Git, no para feeds diarios.

<!-- takeaways -->

- Los seeds cargan CSVs pequeños y estáticos desde Git.
- Fija explícitamente los tipos de columna.
- Las columnas cambiadas necesitan `--full-refresh`.

### Modelos y materializaciones

<!-- unit: Construir modelos y materializaciones -->

<!-- goals -->

- Crear modelos y dejar que `ref()` maneje las dependencias.
- Elegir entre materializaciones view, table, ephemeral e incremental.

<!-- concept -->

Escribir un modelo es escribir una consulta; la materialización decide qué hace dbt con ella. Una vista no guarda nada y recalcula en cada lectura. Una tabla guarda resultados y recalcula en cada build. Los modelos ephemeral se insertan como CTEs en sus hijos. Los incrementales agregan solo datos nuevos en cada ejecución.
La elección cambia costo de build por costo de consulta y frescura, y un proyecto suele usarlas todas según la capa. Cuando ninguna encaja, existen materializaciones personalizadas, aunque rara vez hacen falta.

<!-- example -->

| Capa | Materialización típica | Por qué |
|---|---|---|
| Staging | View | Barata, siempre al día |
| Intermediate | Ephemeral o view | Lógica reutilizada, sin objetos extra |
| Marts | Table | Rápida para BI |
| Hechos grandes | Incremental | Procesa solo filas nuevas |

#### ¿Cómo se crea un modelo de dbt?

Crea un archivo `.sql` en `models/` con un `SELECT` que referencie los nodos de origen con `ref` o `source`, añade si quieres un bloque `config` y una entrada YAML con descripción y tests, y ejecuta `dbt run --select my_model`.

```sql
-- models/staging/stripe/stg_stripe__payments.sql
select
    id as payment_id,
    order_id,
    amount / 100.0 as amount_eur,
    created::date as payment_date
from {{ source('stripe', 'payments') }}
where status = 'succeeded'
```

#### ¿Cómo gestiona dbt las dependencias entre modelos?

Con `ref()`. Cuando un modelo llama a `{{ ref('stg_orders') }}`, dbt registra la arista en el DAG, construye antes `stg_orders` y sustituye la llamada por el nombre de tabla correcto. Nunca declaras tú el orden de ejecución.

#### ¿Qué tipos de materialización existen en dbt?

- **view** (por defecto): se crea una vista, no se guarda nada y la consulta se ejecuta al leer.
- **table**: el resultado se guarda y se reconstruye en cada ejecución.
- **incremental**: en las ejecuciones siguientes solo se insertan o fusionan las filas nuevas o modificadas.
- **ephemeral**: no se construye, se inserta como CTE en los modelos que dependen de él.
- **materialized_view**: una vista materializada de la base de datos, donde se admite.
Los snapshots y los seeds son tipos de recurso aparte, con su propio comportamiento.

#### ¿Cuándo conviene una vista y cuándo una tabla?

Las vistas son baratas de construir y siempre están al día, así que encajan con los modelos de staging y las transformaciones ligeras. Las tablas son más rápidas de consultar, así que encajan con los marts que usa BI y con los modelos costosos de calcular o muy consultados.

#### ¿Cuándo conviene un modelo ephemeral?

Para lógica ligera y reutilizable que no quieres como objeto separado en el almacén. Abusar de ellos complica la depuración, porque no se pueden consultar directamente.

#### ¿Cómo crearías una materialización personalizada en dbt?

Con un bloque `{% materialization name, adapter='default' %}` en un archivo de macros. Normalmente obtiene la relación destino, ejecuta los pre-hooks, construye el SQL con `{% call statement('main') %}`, gestiona las relaciones existentes, ejecuta los post-hooks y devuelve `{'relations': [target_relation]}`. Las materializaciones personalizadas son raras: las integradas y las estrategias incrementales cubren casi todo.

<!-- challenge -->

Un dashboard consulta un mart construido como vista sobre otras cuatro vistas, y cada refresco tarda dos minutos. ¿Qué cambias?

<!-- solution -->

Materializa el mart como tabla (y quizá un modelo intermedio costoso), para que el trabajo ocurra una vez por build y no en cada consulta del dashboard.

<!-- takeaways -->

- Las materializaciones deciden cómo se guarda un modelo.
- Las vistas son baratas de construir; las tablas, de leer.
- Elige la materialización según capa y uso.

<!-- unit: Marts, nombres y grano -->

<!-- goals -->

- Diseñar marts de hechos y dimensiones con un grano declarado.
- Aplicar convenciones de nombres, llaves sustitutas, alias y modelos deshabilitados.

<!-- concept -->

Los marts son los modelos que usa la gente, así que siguen el diseño dimensional: hechos con un grano declarado, dimensiones para el contexto. Declarar el grano en la descripción y probarlo con una prueba de unicidad atrapa el bug de modelado más común, un join que multiplica filas.
Las convenciones hacen navegable un proyecto: prefijos por capa, llaves sustitutas generadas de forma consistente, alias cuando el nombre en el warehouse debe diferir del archivo y modelos deshabilitados para código que no debe correr en una plataforma.

<!-- example -->

```sql
-- models/marts/fct_order_lines.sql   grain: one row per order line
select
    {{ dbt_utils.generate_surrogate_key(['order_id', 'line_number']) }} as order_line_key,
    order_id, line_number, product_id, quantity, net_amount
from {{ ref('int_order_lines_enriched') }}
```

#### ¿Qué es un modelo mart?

Un modelo final construido para los consumidores, normalmente una tabla de hechos (`fct_orders`) o de dimensión (`dim_customers`), o una tabla ancha desnormalizada para un equipo concreto.

#### ¿Qué convenciones de nombres son habituales en dbt?

`stg_<source>__<table>` para staging, `int_<entidad>_<verbo>` para intermediate, `fct_` y `dim_` para los marts, nombres de entidad en plural, snake_case y un modelo por archivo con el mismo nombre que la relación.

#### ¿Qué diferencia hay entre un modelo de hechos y uno de dimensión?

Un modelo de hechos contiene eventos o medidas a una granularidad declarada (pedidos, pagos), con claves foráneas y medidas numéricas. Una dimensión contiene los atributos descriptivos de las entidades (clientes, productos) que sirven para filtrar y agrupar los hechos.

#### ¿Cómo se genera una clave subrogada en dbt?

Con `dbt_utils.generate_surrogate_key`, que calcula el hash de la concatenación de columnas (tratando los NULL de forma coherente):

```sql
select
    {{ dbt_utils.generate_surrogate_key(['order_id', 'line_number']) }} as order_line_key,
    *
from {{ ref('stg_order_lines') }}
```

#### ¿Qué es la granularidad de un modelo y por qué importa?

Lo que representa una fila (un pedido, una línea de pedido, un cliente por día). Declararla, y comprobarla con un test de unicidad, evita filas duplicadas y agregaciones erróneas aguas abajo.

#### ¿Qué son los hooks?

SQL que se ejecuta en momentos concretos: `pre-hook` y `post-hook` alrededor de un modelo, y `on-run-start` / `on-run-end` alrededor de toda la invocación. Sirven, por ejemplo, para conceder privilegios, crear índices o registrar las ejecuciones.

#### ¿Qué son el pre-hook y el post-hook?

Un `pre-hook` ejecuta SQL justo antes de construir un modelo, y un `post-hook` justo después, dentro de la misma ejecución. Por ejemplo:

```sql
{{ config(post_hook="grant select on {{ this }} to role reporter") }}
```

<!-- challenge -->

`fct_orders` de repente tiene más filas que órdenes. ¿Qué prueba lo habría atrapado y qué suele causarlo?

<!-- solution -->

Una prueba `unique` sobre `order_id` (el grano declarado). La causa usual es un join con una tabla que tiene varias filas por orden, como pagos o envíos, sin agregarla antes.

<!-- takeaways -->

- Los marts son hechos y dimensiones con un grano declarado.
- Prueba el grano con una prueba de unicidad.
- Nombres y llaves consistentes hacen navegable el proyecto.

<!-- unit: Hooks, contratos y constraints -->

<!-- goals -->

- Correr SQL alrededor de los modelos con hooks y `{{ this }}`.
- Imponer esquemas con contratos de modelo y constraints.

<!-- concept -->

Los hooks corren SQL extra antes o después de un modelo o de toda una ejecución: grants, inserts de auditoría, comandos de mantenimiento. `{{ this }}` se refiere a la relación del propio modelo, que necesitan los hooks y la lógica incremental.
Los contratos van en sentido contrario: en lugar de agregar acciones, agregan garantías. Con un contrato impuesto, las columnas y tipos del modelo deben coincidir con lo declarado, así un refactor no puede cambiar en silencio la interfaz de la que dependen los consumidores. Los constraints agregan reglas a nivel de base donde la plataforma las soporta.

<!-- example -->

```yaml
models:
  - name: dim_customer
    config:
      contract: {enforced: true}
      post_hook: "grant select on {{ this }} to role reporting"
    columns:
      - name: customer_id
        data_type: bigint
        constraints: [{type: not_null}, {type: primary_key}]
      - name: segment
        data_type: varchar
```

#### ¿A qué se refiere `{{ this }}`?

A la relación (base_de_datos.esquema.tabla) del modelo que se está construyendo. Se usa en los hooks y en los modelos incrementales para consultar la tabla existente.

#### ¿Qué son los contratos de modelo?

Una configuración `contract: {enforced: true}` con nombres y tipos de columna declarados (y restricciones donde se admiten). dbt comprueba que la salida del modelo coincide antes de construirlo, y protege así a los consumidores de cambios de esquema.

#### ¿Qué son las restricciones (constraints) en dbt?

Declaraciones como `not_null`, `unique`, `primary_key`, `foreign_key` y `check` en modelos con contrato. dbt las añade al DDL cuando la plataforma las aplica. Muchos almacenes solo registran algunas como metadatos, así que los tests siguen siendo necesarios.

#### ¿Qué diferencia hay entre `dbt run --full-refresh` y una ejecución normal?

`--full-refresh` elimina y reconstruye desde cero los modelos incrementales y recarga los seeds, en lugar de procesar solo los datos nuevos.

#### ¿Qué hace la opción `--defer`?

Con `--state` apuntando a los artefactos de producción, hace que `ref()` se resuelva a las relaciones de producción de los modelos que no has construido en tu entorno, así que puedes ejecutar un modelo en dev sin reconstruir todos sus padres.

<!-- challenge -->

Un desarrollador cambia una columna de `bigint` a `varchar` en un modelo público, y una aplicación aguas abajo se rompe una semana después. ¿Qué lo habría frenado al construir?

<!-- solution -->

Un contrato de modelo impuesto que declare `bigint` para esa columna: el build falla cuando el tipo producido no coincide, antes de que algo llegue a producción.

<!-- takeaways -->

- Los hooks corren SQL antes o después de modelos y ejecuciones.
- `{{ this }}` es la relación del propio modelo.
- Los contratos vuelven nombres y tipos de columnas una interfaz impuesta.

<!-- unit: Ejecutar modelos y resolver problemas -->

<!-- goals -->

- Usar full refresh, defer, clone, show y retry.
- Arreglar "relation does not exist" y planear refrescos de datos.

<!-- concept -->

El trabajo diario necesita más que `run`. Los full refresh reconstruyen los modelos incrementales desde cero. Defer y clone permiten construir solo lo que cambiaste leyendo todo lo demás de producción. Show previsualiza resultados sin construir; retry vuelve a correr solo lo que falló.
Muchos errores vienen de los ambientes y no del SQL: un padre que nunca se construyó en tu esquema, un error de tipeo en una source, permisos faltantes. Conocer las herramientas anteriores suele resolverlos en minutos.

<!-- example -->

```bash
dbt build --select state:modified+ --defer --state prod-artifacts/   # build only my changes
dbt show --select fct_orders --limit 10                              # preview
dbt retry                                                            # rerun failed nodes only
```

#### ¿Qué es `dbt clone`?

Un comando que crea copias (clones sin copia de datos donde se admite, si no vistas) de los modelos de producción en otro entorno, a partir del estado de producción. Acelera la CI y la preparación de entornos de desarrollo.

#### ¿Qué es `dbt show`?

Un comando para previsualizar los resultados de un modelo o de una consulta en línea sin materializarlo: `dbt show --select stg_orders --limit 10`.

#### ¿Qué es `dbt retry`?

Vuelve a ejecutar solo los nodos que fallaron o se omitieron en la invocación anterior.

#### ¿Cómo se resuelve el error "relation does not exist" en dbt?

Causas habituales: una tabla referenciada nunca se construyó en el target actual (ejecuta el padre o usa `--defer`), el nombre de la tabla está escrito a mano en lugar de usar `ref`/`source` (así que la dependencia no se conoce y el orden es incorrecto), la definición de la source apunta a la base de datos o al esquema equivocados, el usuario no tiene permiso para ver el objeto, o el identificador tiene problemas de comillas o mayúsculas. Ejecutar `dbt compile` y mirar el SQL de `target/compiled/` suele mostrar qué nombre está mal.

#### ¿Qué es el refresco de datos (data refresh)?

Actualizar las tablas del almacén para que reflejen los últimos datos de origen: un `dbt build` programado que reconstruye las tablas, procesa las filas nuevas de los modelos incrementales y captura los cambios en los snapshots. Su frecuencia depende de lo frescos que necesiten los datos los consumidores y de cada cuánto se cargan las sources.

#### ¿Qué es un modelo desactivado?

Un modelo con `enabled: false`. dbt lo ignora, lo que es útil para modelos específicos de una plataforma o en desarrollo.

#### ¿Qué es la configuración `alias`?

Fija el nombre de la relación en el almacén con independencia del nombre del archivo del modelo.

<!-- challenge -->

Un desarrollador cambia un mart y corre `dbt run --select my_mart` en su esquema de desarrollo. Falla con "relation does not exist" para un modelo padre. ¿Cuáles son dos formas de arreglarlo?

<!-- solution -->

Construir también los padres (`--select +my_mart`), o usar `--defer --state` con los artefactos de producción para que los padres sin construir resuelvan a relaciones de producción (o hacer `dbt clone` de ellos en dev).

<!-- takeaways -->

- Full refresh reconstruye los modelos incrementales.
- Defer y clone reutilizan producción para padres sin cambios.
- Show previsualiza; retry repite las fallas.

### Jinja y macros

<!-- unit: Bases de Jinja -->

<!-- goals -->

- Usar expresiones, sentencias, variables y filtros de Jinja en los modelos.
- Adaptar el SQL al target y mantener ordenado el SQL compilado.

<!-- concept -->

Jinja convierte los archivos SQL en plantillas. Las expresiones insertan valores, las sentencias agregan ciclos y condiciones, y los comentarios desaparecen al compilar. Con variables y filtros, el SQL repetitivo, como una columna por método de pago, se vuelve un ciclo sobre una lista.
La variable `target` permite adaptar el código al ambiente, por ejemplo muestreando datos en desarrollo. El control de espacios mantiene legible el SQL compilado, lo que importa porque eso es lo que depuras.

<!-- example -->

```sql
{% set methods = ['card', 'paypal', 'bank_transfer'] %}
select
    order_id,
    {%- for m in methods %}
    sum(case when method = '{{ m }}' then amount end) as {{ m }}_amount{{ "," if not loop.last }}
    {%- endfor %}
from {{ ref('stg_shop__payments') }}
{% if target.name == 'dev' %} where created_at >= current_date - 30 {% endif %}
group by 1
```

#### ¿Cómo se usa Jinja para mejorar el código SQL?

Jinja añade control de flujo y reutilización: bucles para generar columnas repetitivas, bloques `if` para la lógica específica de cada entorno, variables para valores configurables y macros para compartir lógica entre modelos. Mantenlo legible: cuando Jinja domina un modelo, suele ser mejor una macro u otro diseño.

```sql
select
    order_id,
    {% for method in ['card', 'paypal', 'transfer'] %}
    sum(case when payment_method = '{{ method }}' then amount else 0 end) as {{ method }}_amount
    {%- if not loop.last %},{% endif %}
    {% endfor %}
from {{ ref('stg_payments') }}
group by 1
```

#### ¿Qué son las macros en dbt y cómo se ejecutan?

Fragmentos reutilizables de Jinja (que a menudo generan SQL) definidos con `{% macro name(args) %}...{% endmacro %}` en la carpeta `macros/`. Se llaman dentro de modelos, tests o hooks con `{{ name(args) }}`, o se ejecutan directamente con `dbt run-operation name --args '{...}'`.

#### ¿Qué diferencia hay entre `{{ }}`, `{% %}` y `{# #}`?

`{{ }}` muestra una expresión, `{% %}` ejecuta una instrucción (if, for, set, macro, call) y `{# #}` es un comentario que no aparece en el SQL compilado.

#### ¿Qué hace el `-` en `{%-` o `-%}`?

Elimina los espacios en blanco antes o después de la etiqueta, para que el SQL compilado quede limpio.

#### ¿Cómo se escribe una macro con un argumento por defecto?

```sql
{% macro cents_to_euros(column, scale=2) %}
    round({{ column }} / 100.0, {{ scale }})
{% endmacro %}
```

Se llama con `{{ cents_to_euros('amount') }}`.

#### ¿Qué hace `run_query`?

Ejecuta una consulta durante la compilación y devuelve el resultado como una tabla agate, por ejemplo para construir una lista de valores distintos que se usa en un bucle. Solo devuelve datos en tiempo de ejecución, así que se suele proteger con `{% if execute %}`.

<!-- challenge -->

Un modelo tiene 12 líneas `case when` casi idénticas, una por país, y un país nuevo implica editar SQL. ¿Cómo lo vuelves guiado por datos?

<!-- solution -->

Lee la lista de países desde una variable, un seed o `run_query` y recórrela con `{% for %}` para generar las columnas. Así los países nuevos solo cambian la lista.

<!-- takeaways -->

- Jinja agrega ciclos, condiciones y variables al SQL.
- `target` adapta el código al ambiente.
- El control de espacios mantiene legible el SQL compilado.

<!-- unit: Escribir macros -->

<!-- goals -->

- Escribir macros con argumentos, valores por defecto y valores de retorno.
- Correr macros como operaciones y depurarlas con `log()`.

<!-- concept -->

Las macros son funciones para SQL: lógica que escribes una vez y llamas desde muchos modelos. Reciben argumentos con valores por defecto, pueden leer la config de un modelo y pueden devolver valores en lugar de texto cuando otra macro necesita datos y no SQL.
Algunas macros nunca corren durante un build. Run-operation las llama directamente para tareas de administración como otorgar permisos o limpiar esquemas viejos, y el logging ayuda a seguir lo que hacen.

<!-- example -->

```sql
-- macros/cents_to_currency.sql
{% macro cents_to_currency(column, scale=2) %}
    round({{ column }} / 100.0, {{ scale }})
{% endmacro %}

-- usage in a model
select order_id, {{ cents_to_currency('amount_cents') }} as amount from {{ ref('stg_shop__payments') }}
```

#### ¿Qué es la variable `execute`?

Un booleano que vale false durante el análisis del proyecto y true cuando dbt ejecuta realmente los nodos. El código que consulta la base de datos debe ir dentro de `{% if execute %}`, porque la base de datos no se consulta durante el análisis.

#### ¿Qué es `adapter.dispatch`?

Un mecanismo para implementar una macro de forma distinta según la base de datos, de modo que los paquetes funcionen con varios adaptadores: dbt elige `snowflake__my_macro`, `bigquery__my_macro` o `default__my_macro` según el adaptador.

#### ¿Qué es la variable `target` en Jinja?

Información sobre la conexión actual: `target.name`, `target.schema`, `target.type`, `target.threads`. Se usa a menudo para limitar los datos en desarrollo:

```sql
{% if target.name == 'dev' %} where created_at >= dateadd(day, -3, current_date) {% endif %}
```

#### ¿Cómo se define una variable dentro de un modelo?

Con `{% set %}`, por ejemplo `{% set payment_methods = ['card', 'paypal'] %}`, y luego se usa en bucles o expresiones.

#### ¿Para qué sirve `log()` en las macros?

Para mostrar mensajes en la consola o en el archivo de registro durante la compilación, al depurar: `{{ log("value: " ~ my_var, info=true) }}`.

#### ¿Qué es el objeto `config` en Jinja?

Lee la configuración de un modelo dentro de las macros, por ejemplo `config.get('unique_key')`.

<!-- challenge -->

Cada mes alguien borra a mano los esquemas de desarrollo de más de 30 días. ¿Cómo lo automatizas con dbt?

<!-- solution -->

Escribe una macro que consulte el information schema buscando esquemas de dev, filtre por antigüedad o patrón de nombre y los borre, y programa `dbt run-operation drop_old_dev_schemas` en el orquestador.

<!-- takeaways -->

- Las macros son funciones reutilizables que generan SQL.
- `return()` pasa datos entre macros.
- `run-operation` corre macros fuera de los builds.

<!-- unit: Introspección en compilación -->

<!-- goals -->

- Consultar el warehouse y el grafo del proyecto durante la compilación.
- Escribir macros específicas por adapter y sobrescribir las incorporadas.

<!-- concept -->

Hay SQL que no se puede escribir hasta saber algo: los valores distintos de una columna, las columnas de una tabla, la plataforma en la que estás. dbt puede consultar el warehouse mientras compila y leer su propio grafo de proyecto, pero solo cuando de verdad está ejecutando, no mientras parsea el proyecto.
Dispatch elige la implementación de una macro según la plataforma, que es como los paquetes funcionan en todas partes, y cualquier macro incorporada se puede sobrescribir definiendo una con el mismo nombre.

<!-- example -->

```sql
{% set statuses_query %}select distinct status from {{ ref('stg_shop__orders') }}{% endset %}
{% if execute %}
  {% set statuses = run_query(statuses_query).columns[0].values() %}
{% else %}
  {% set statuses = [] %}
{% endif %}
```

#### ¿Qué son las variables de contexto `graph` y `model`?

`graph` expone el proyecto analizado (todos los nodos y sus metadatos), y `model` el nodo actual, que las macros pueden inspeccionar, por ejemplo para generar documentación o auditorías.

#### ¿Para qué se usa `dbt run-operation`?

Para ejecutar una macro fuera de la construcción, en tareas de administración: conceder permisos, borrar esquemas antiguos, cargar datos o generar código con el paquete `codegen`.

#### ¿Qué es el paquete `codegen`?

Un paquete con macros que generan YAML y SQL repetitivos, como las definiciones de sources a partir de un esquema o un modelo de staging a partir de una tabla de origen.

#### ¿Cómo se sobrescribe una macro integrada de dbt?

Definiendo una macro con el mismo nombre en tu proyecto, por ejemplo `generate_schema_name` o `generate_alias_name`. La versión del proyecto tiene prioridad sobre la que trae dbt.

#### ¿Qué hace `return()` en una macro?

Devuelve un objeto Python (lista, diccionario, número) en lugar de texto renderizado, para que otra macro pueda usar el valor.

<!-- challenge -->

Un modelo que usa `run_query` falla durante `dbt parse` con un error de relación faltante. ¿Por qué y cuál es la solución?

<!-- solution -->

Las consultas también corren durante el parseo, cuando las relaciones pueden no existir y los resultados no hacen falta. Envuelve el `run_query` en `{% if execute %}` y da un valor por defecto en el otro caso.

<!-- takeaways -->

- `run_query` lee el warehouse al compilar.
- Protege las consultas con `execute`.
- Dispatch y las sobrescrituras adaptan macros por plataforma.

<!-- unit: Paquetes y mesura -->

<!-- goals -->

- Usar macros de ayuda como `codegen` y `dbt_utils.star`.
- Evitar la sobreingeniería con Jinja.

<!-- concept -->

Las macros ya hechas ahorran mucho tecleo: generar el YAML de sources y los modelos de staging, listar columnas salvo unas pocas. Vale la pena conocerlas antes de escribir las propias.
El riesgo opuesto también es real. El SQL muy templado es difícil de leer, revisar y depurar, porque el código que ves no es el que corre. SQL plano primero, y una macro solo cuando la lógica de verdad se repite o debe variar por plataforma, mantiene mantenible un proyecto.

<!-- example -->

```bash
dbt run-operation generate_source --args '{"schema_name": "shop", "generate_columns": true}'
```
```sql
select {{ dbt_utils.star(from=ref('stg_shop__customers'), except=['_loaded_at', 'raw_payload']) }}
from {{ ref('stg_shop__customers') }}
```

#### ¿Qué son los filtros de Jinja? Da ejemplos.

Funciones que se aplican con `|`, como `{{ name | upper }}`, `{{ columns | join(', ') }}` o `{{ value | default('n/a') }}`.

#### ¿Cómo se evita complicar de más el código con Jinja?

Escribe primero SQL normal, extrae una macro solo cuando la lógica se repite o debe variar según el adaptador, documenta los argumentos de las macros y comprueba que el SQL compilado se lee bien.

#### ¿Qué es la macro `star` de dbt_utils?

`{{ dbt_utils.star(ref('model'), except=['col']) }}` genera la lista de columnas de una relación, menos algunas, para evitar `select *` sin escribir todas las columnas.

<!-- challenge -->

Un compañero construyó una macro que genera modelos completos desde metadatos en YAML, y nadie más puede depurarlos. ¿Qué sugieres?

<!-- solution -->

Reservar la generación para modelos de verdad repetitivos y mecánicos (si acaso) y escribir la lógica de negocio como modelos SQL planos. Documentar cualquier generador que quede y hacer fácil inspeccionar el SQL compilado.

<!-- takeaways -->

- `codegen` escribe el boilerplate; `star` lista columnas.
- Prefiere SQL plano; macros solo para lógica repetida.
- Un SQL compilado legible importa para depurar.

<!-- stage: Calidad e historia -->

### Tests y calidad de datos

<!-- unit: Pruebas de datos -->

<!-- goals -->

- Usar pruebas de datos genéricas, singulares y genéricas personalizadas.
- Probar la unicidad sobre combinaciones de columnas.

<!-- concept -->

Una prueba de datos es una consulta que devuelve las filas que rompen una regla; ninguna fila significa que pasa. Las pruebas genéricas son reglas reutilizables aplicadas en YAML, como unicidad o valores aceptados. Las singulares son archivos SQL puntuales para reglas demasiado específicas para reutilizar. Cuando una regla aparece en varios lugares, una prueba genérica personalizada la vuelve reutilizable.
Como las pruebas corren sobre datos reales en el warehouse, atrapan problemas en las fuentes además de en el código.

<!-- example -->

```yaml
models:
  - name: fct_order_lines
    data_tests:
      - dbt_utils.unique_combination_of_columns:
          combination_of_columns: [order_id, line_number]
    columns:
      - name: status
        data_tests:
          - accepted_values: {values: [placed, shipped, returned]}
      - name: customer_id
        data_tests:
          - relationships: {to: ref('dim_customer'), field: customer_id}
```

#### ¿Cuáles son los dos tipos de tests en dbt?

Los **tests de datos** comprueban los datos del almacén: tests genéricos (reutilizables, parametrizados, declarados en YAML) y tests singulares (consultas SQL puntuales en `tests/`). Los **tests unitarios**, añadidos en dbt 1.8, comprueban la lógica SQL de un modelo con pequeñas entradas simuladas antes de ejecutarlo sobre datos reales.

#### ¿Qué tipos de tests se pueden ejecutar en dbt?

Los cuatro tests genéricos integrados (`unique`, `not_null`, `accepted_values`, `relationships`), tests genéricos de paquetes (`dbt_utils`, `dbt_expectations`) o propios, tests SQL singulares, tests unitarios, comprobaciones de frescura de sources y contratos de modelo.

#### ¿Cómo funcionan los tests genéricos integrados?

```yaml
models:
  - name: fct_orders
    columns:
      - name: order_id
        data_tests: [unique, not_null]
      - name: status
        data_tests:
          - accepted_values:
              values: ['placed', 'shipped', 'returned']
      - name: customer_id
        data_tests:
          - relationships:
              to: ref('dim_customers')
              field: customer_id
```

dbt convierte cada uno en una consulta que devuelve las filas que fallan. El test pasa cuando la consulta no devuelve ninguna fila.

#### ¿Qué es un test singular?

Un archivo `.sql` de `tests/` que selecciona las filas que incumplen una regla. Falla si devuelve alguna fila:

```sql
-- tests/assert_no_negative_amounts.sql
select * from {{ ref('fct_orders') }} where amount < 0
```

#### ¿Cómo se escribe un test genérico propio?

Con un bloque `{% test name(model, column_name) %}` que devuelve las filas que fallan, y luego se usa en YAML como un test integrado:

```sql
{% test is_positive(model, column_name) %}
select * from {{ model }} where {{ column_name }} <= 0
{% endtest %}
```

#### ¿Qué es un test unitario en dbt?

Una definición YAML que da filas de entrada fijas para los padres de un modelo y la salida esperada, para que dbt compruebe la lógica de la transformación (casos límite, sentencias case, funciones de ventana) sin datos reales:

```yaml
unit_tests:
  - name: test_is_valid_email
    model: dim_customers
    given:
      - input: ref('stg_customers')
        rows:
          - {customer_id: 1, email: a@b.com}
          - {customer_id: 2, email: not-an-email}
    expect:
      rows:
        - {customer_id: 1, is_valid_email: true}
        - {customer_id: 2, is_valid_email: false}
```

<!-- challenge -->

Varios modelos necesitan la regla "el monto no puede ser negativo salvo que la fila sea un reembolso". ¿Cómo evitas copiar una prueba singular cinco veces?

<!-- solution -->

Escribe una prueba genérica personalizada (por ejemplo `non_negative_unless_refund(model, column_name)`) que devuelva las filas que la violan, y aplícala en YAML a la columna de monto de cada modelo.

<!-- takeaways -->

- Las pruebas de datos devuelven las filas que rompen una regla.
- Las genéricas se reutilizan; las singulares son específicas.
- Las reglas repetidas se vuelven pruebas genéricas personalizadas.

<!-- unit: Unit tests y paquetes de pruebas -->

<!-- goals -->

- Escribir unit tests y distinguirlos de las pruebas de datos.
- Usar pruebas de paquetes para rangos, recencia y conteos de filas.

<!-- concept -->

Las pruebas de datos revisan los datos que existen en ese momento; los unit tests revisan la lógica contra entradas que tú eliges. Un unit test da filas fijas para los padres del modelo y la salida esperada, así casos borde como reembolsos o nulos se prueban antes de que el modelo corra sobre datos reales.
Los paquetes extienden las pruebas de datos con chequeos comunes: valores en un rango, datos recientes, conteos de filas que coinciden entre modelos. Cubren la mayoría de necesidades sin SQL personalizado.

<!-- example -->

```yaml
unit_tests:
  - name: refunds_reduce_net_amount
    model: fct_order_lines
    given:
      - input: ref('int_order_lines_enriched')
        rows:
          - {order_id: 1, line_number: 1, type: sale,   amount: 100}
          - {order_id: 1, line_number: 2, type: refund, amount: 30}
    expect:
      rows:
        - {order_id: 1, line_number: 1, net_amount: 100}
        - {order_id: 1, line_number: 2, net_amount: -30}
```

#### ¿Qué diferencia hay entre un test unitario y un test de datos?

Un test unitario comprueba el código con entradas fijas y se ejecuta antes de construir el modelo, normalmente en CI. Un test de datos comprueba los datos reales después de construir el modelo, en cada ejecución.

#### ¿Qué es la severidad de un test?

Un ajuste `severity: warn` o `error` (por defecto). Con umbrales `warn_if` y `error_if` como `">10"`, un test puede avisar con pocos fallos y solo fallar por encima de un límite.

#### ¿Cómo se guardan los fallos de los tests?

Con `--store-failures` o `store_failures: true`, dbt guarda las filas que fallan en una tabla de un esquema de auditoría, para poder revisarlas después de la ejecución.

#### ¿Qué hace la configuración `where` de un test?

Limita el test a un subconjunto de filas, por ejemplo solo los datos recientes: `config: {where: "order_date >= current_date - 7"}`.

#### ¿Qué es `dbt_expectations`?

Un paquete de tests genéricos inspirado en Great Expectations: rangos de valores, expresiones regulares, número de filas, distribuciones, tipos de columna y más.

#### ¿Cómo se comprueba que una combinación de columnas es única?

Con `dbt_utils.unique_combination_of_columns`:

```yaml
data_tests:
  - dbt_utils.unique_combination_of_columns:
      combination_of_columns: [order_id, line_number]
```

<!-- challenge -->

Un cálculo complejo de descuentos pasa todas las pruebas de datos, pero una combinación rara de cupones se calcula mal en producción. ¿Qué tipo de prueba lo habría atrapado?

<!-- solution -->

Un unit test con filas de entrada simuladas que cubran esa combinación de cupones y el descuento esperado. Las pruebas de datos solo ven las combinaciones presentes en los datos al momento de probar.

<!-- takeaways -->

- Los unit tests revisan la lógica con entradas elegidas.
- Las pruebas de datos revisan datos reales.
- Los paquetes agregan pruebas de rango, recencia y conteo.

<!-- unit: Configurar pruebas -->

<!-- goals -->

- Fijar severidad, umbrales y filtros en las pruebas.
- Guardar las fallas y evitar la fatiga de alertas.

<!-- concept -->

No toda prueba fallida significa lo mismo. Severidad y umbrales separan "detener todo" de "vale la pena mirar": unas pocas filas malas pueden advertir mientras mil fallan. Un filtro `where` limita la prueba a datos recientes, lo que la mantiene rápida y relevante.
Guardar las fallas convierte una prueba en rojo en algo que puedes investigar. Sin estos ajustes, los equipos se ahogan en alertas y empiezan a ignorarlas, lo que es peor que tener menos pruebas.

<!-- example -->

```yaml
columns:
  - name: email
    data_tests:
      - not_null:
          config:
            severity: error
            warn_if: ">0"
            error_if: ">100"
            where: "created_at >= current_date - 7"
            store_failures: true
```

#### ¿Qué hay que testear como mínimo en cada modelo?

La clave primaria con `unique` y `not_null`, las claves foráneas de los joins importantes con `relationships` y las columnas categóricas con `accepted_values`. Añade reglas de negocio donde un error saldría caro.

#### ¿Qué significa "testear en el origen"?

Poner tests en las sources y en los modelos de staging, para detectar los problemas de los datos en bruto a la entrada en lugar de descubrirlos en un cuadro de mando.

#### ¿Cómo se evita la fatiga de alertas con los tests de dbt?

Usa la severidad `warn` y umbrales para las comprobaciones no críticas, testea lo que importa a los consumidores, elimina los tests que nunca detectan nada relevante y envía los errores a sus responsables.

#### ¿Cómo garantiza dbt la calidad de los datos a lo largo del pipeline?

Con tests en cada capa, frescura de las sources, contratos en los modelos públicos, `dbt build` omitiendo los modelos dependientes cuando un test falla, y CI que ejecuta los modelos modificados y sus tests antes de fusionar.

<!-- challenge -->

Un equipo recibe 40 advertencias de pruebas cada mañana y ya no las lee. ¿Qué haces?

<!-- solution -->

Revisa cada prueba: corrige los problemas reales, borra las pruebas que no protegen a los consumidores, fija umbrales para que las advertencias signifiquen algo, vuelve errores que bloquean las pruebas críticas y dirige las alertas a los dueños.

<!-- takeaways -->

- Severidad y umbrales gradúan las fallas.
- `where` mantiene las pruebas enfocadas y rápidas.
- Pocas alertas con sentido valen más que muchas ignoradas.

<!-- unit: Una estrategia de pruebas -->

<!-- goals -->

- Definir las pruebas mínimas que necesita todo modelo.
- Probar en la fuente y usar `dbt build` para frenar datos malos.

<!-- concept -->

Una buena estrategia pone las pruebas donde más protegen. A la entrada, las pruebas sobre sources y staging atrapan problemas de datos crudos antes de que se propaguen. En cada modelo, las llaves primarias son únicas y no nulas, y las llaves foráneas importantes existen. En los modelos públicos, los contratos protegen a los consumidores.
`dbt build` lo une todo: cada modelo se prueba justo después de construirse, y los hijos de un modelo que falla se saltan.

<!-- example -->

| Capa | Mínimo |
|---|---|
| Sources | Frescura, llave no nula, única donde se espera |
| Staging | Llave primaria única + no nula |
| Marts | Unicidad del grano, relaciones, valores aceptados, contratos |

#### ¿Qué diferencia hay entre `dbt test` y `dbt build` en cuanto a los tests?

`dbt test` ejecuta tests sobre modelos ya construidos. `dbt build` intercala construcción y tests en el orden del DAG, así que un test que falla impide construir sus hijos.

#### ¿Cómo se compara el número de filas de un modelo con el de otro?

Con un test de paquete como `dbt_utils.equal_rowcount` o `dbt_expectations.expect_table_row_count_to_equal_other_table`, o con un test singular que compare los recuentos.

#### ¿Cómo se comprueba que un valor está dentro de un rango?

Con `dbt_utils.accepted_range` (`min_value`, `max_value`) o `dbt_expectations.expect_column_values_to_be_between`.

#### ¿Qué es un test de actualidad (recency)?

Un test como `dbt_utils.recency` que falla cuando la marca de tiempo más reciente de un modelo es más antigua que un umbral, y detecta los modelos que han dejado de recibir datos.

<!-- challenge -->

Duplicados de una fuente llegaron a tres marts antes de que alguien lo notara. ¿Dónde debió estar la primera prueba?

<!-- solution -->

En la source o en su modelo de staging: una prueba de unicidad sobre la llave de la fuente fallaría a la entrada, y con `dbt build` los marts se saltarían en lugar de reconstruirse con duplicados.

<!-- takeaways -->

- Prueba las llaves en cada modelo.
- Atrapa los problemas crudos en sources y staging.
- `dbt build` frena la propagación de datos malos.

### Modelos incrementales

<!-- unit: Cómo funcionan los modelos incrementales -->

<!-- goals -->

- Construir modelos incrementales con `is_incremental()` y `unique_key`.
- Saber cuándo usarlos y cómo leen su propia tabla.

<!-- concept -->

Reconstruir una tabla de mil millones de filas en cada ejecución desperdicia tiempo y dinero cuando solo las filas de hoy son nuevas. Un modelo incremental construye la tabla completa una vez y luego, en las siguientes ejecuciones, procesa solo filas nuevas o cambiadas y las agrega a la tabla existente.
El modelo decide qué es nuevo filtrando dentro de un bloque `is_incremental()`, normalmente contra el timestamp máximo que ya hay en `{{ this }}`. Un `unique_key` convierte los inserts en upserts.

<!-- example -->

```sql
{{ config(materialized='incremental', unique_key='event_id') }}
select event_id, user_id, event_type, occurred_at
from {{ ref('stg_app__events') }}
{% if is_incremental() %}
where occurred_at > (select max(occurred_at) from {{ this }})
{% endif %}
```

#### ¿Cómo se crean modelos incrementales en dbt y cuándo se usan?

Fija `materialized='incremental'` y filtra las filas nuevas con `is_incremental()`. La primera ejecución construye toda la tabla, y las siguientes solo procesan las filas más recientes que las que ya están. Úsalos en tablas grandes con muchas inserciones (eventos, registros, transacciones) donde reconstruirlo todo en cada ejecución es demasiado lento o caro.

```sql
{{ config(materialized='incremental', unique_key='event_id') }}

select * from {{ ref('stg_events') }}
{% if is_incremental() %}
where event_time > (select max(event_time) from {{ this }})
{% endif %}
```

#### ¿Qué devuelve `is_incremental()`?

True solo cuando el modelo es incremental, la tabla destino ya existe y la ejecución no es un `--full-refresh`.

#### ¿Qué es `unique_key` en un modelo incremental?

La columna (o lista de columnas) que identifica una fila. Con ella, las filas que ya existen se actualizan en lugar de duplicarse, según la estrategia.

#### ¿Qué estrategias incrementales existen?

Según el adaptador: `append` (solo inserción), `merge` (upsert por `unique_key`), `delete+insert` (borra las claves coincidentes y luego inserta), `insert_overwrite` (sustituye particiones enteras, en BigQuery y Spark) y `microbatch` (procesa lotes por tiempo).

#### ¿Cómo gestiona dbt la carga incremental de datos de los sistemas de origen?

dbt no extrae de los sistemas de origen: procesa datos ya cargados en el almacén. Los modelos incrementales seleccionan solo las filas más recientes que las ya procesadas (con una marca de tiempo o un ID) y las fusionan o añaden. Herramientas de carga como Fivetran o Airbyte traen los datos de forma incremental, y dbt los transforma de forma incremental.

#### ¿Qué es la estrategia microbatch?

Añadida en dbt 1.9, procesa los datos en lotes de tiempo independientes (por ejemplo uno por día) según una columna `event_time`, de modo que los lotes se pueden reintentar, ejecutar en paralelo o rellenar con `--event-time-start` y `--event-time-end`.

<!-- challenge -->

Un modelo incremental no tiene `unique_key`, y la fuente a veces reenvía órdenes actualizadas. ¿Qué pasa y qué cambias?

<!-- solution -->

Las órdenes actualizadas se vuelven a anexar y crean duplicados. Agrega `unique_key='order_id'` (con estrategia merge o delete+insert) para que las filas existentes se actualicen.

<!-- takeaways -->

- Los incrementales procesan solo filas nuevas tras el primer build.
- `is_incremental()` protege el filtro.
- `unique_key` convierte anexos en upserts.

<!-- unit: Estrategias incrementales -->

<!-- goals -->

- Elegir entre append, merge, delete+insert, insert_overwrite y microbatch.
- Acelerar los merges con predicados y particionamiento.

<!-- concept -->

Cómo se combinan las filas nuevas con la tabla es la estrategia. Append solo inserta. Merge hace upsert sobre la llave. Delete+insert borra primero las filas que coinciden, a veces más rápido en lotes grandes. Insert_overwrite reemplaza particiones completas, muy eficiente cuando los datos llegan por día. Microbatch divide el trabajo en lotes de tiempo independientes que se pueden reintentar y rellenar uno a uno.
Los destinos grandes necesitan ayuda: predicados y particionamiento limitan cuánto de la tabla existente escanea cada merge.

<!-- example -->

```sql
{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='order_id',
    incremental_predicates=["DBT_INTERNAL_DEST.ordered_at >= dateadd(day, -7, current_date)"],
    cluster_by=['ordered_at']
) }}
```

#### ¿Cómo se gestionan los datos que llegan tarde en los modelos incrementales?

Con una ventana de revisión en lugar de un "mayor que" estricto: reprocesa los últimos días y apóyate en `unique_key` con `merge` para actualizar las filas ya cargadas.

```sql
{% if is_incremental() %}
where event_time >= (select dateadd(day, -3, max(event_time)) from {{ this }})
{% endif %}
```

#### ¿Qué hace `on_schema_change`?

Define qué pasa cuando cambian las columnas de un modelo incremental: `ignore` (por defecto), `fail`, `append_new_columns` o `sync_all_columns`.

#### ¿Cuándo hay que hacer un full refresh de un modelo incremental?

Cuando la lógica cambia de una forma que afecta a las filas históricas, cuando las columnas cambian de formas que `on_schema_change` no gestiona, o para reparar datos. Algunas tablas se protegen con `full_refresh: false` porque reconstruirlas es demasiado caro.

#### ¿Qué riesgos tienen los modelos incrementales?

Duplicados si `unique_key` falta o es incorrecta, filas perdidas si el filtro no contempla los datos tardíos, divergencia respecto a una reconstrucción completa si la lógica cambia, y más complejidad para testear. Un full refresh periódico en un entorno inferior ayuda a detectar desviaciones.

#### ¿Qué diferencia hay entre `merge` y `delete+insert`?

`merge` actualiza las filas coincidentes e inserta las nuevas en una sola sentencia. `delete+insert` borra las filas existentes con las mismas claves e inserta el nuevo lote. Es útil donde merge es lento o no se admite.

#### ¿Qué es `insert_overwrite` y cuándo es eficiente?

Sustituye particiones enteras (por ejemplo los días presentes en el nuevo lote) en lugar de fusionar fila a fila. Es eficiente en tablas particionadas de BigQuery, Spark y Databricks cuando los datos llegan por partición.

<!-- challenge -->

Una tabla de BigQuery particionada por día recibe un día completo de eventos en cada ejecución. El merge es lento y caro. ¿Qué estrategia encaja mejor?

<!-- solution -->

`insert_overwrite` con la tabla particionada por fecha: cada ejecución reemplaza las particiones de los días afectados en lugar de hacer merge fila por fila, lo que es más barato y naturalmente idempotente.

<!-- takeaways -->

- Estrategias: append, merge, delete+insert, insert_overwrite, microbatch.
- Sobrescribir por partición es eficiente para datos diarios.
- Predicados y particionamiento limitan el escaneo del merge.

<!-- unit: Mantener correctos los modelos incrementales -->

<!-- goals -->

- Manejar datos tardíos, cambios de esquema y full refreshes.
- Probar y hacer backfill de modelos incrementales.

<!-- concept -->

Los modelos incrementales cambian simplicidad por velocidad, y el cambio se nota en los casos borde. Un filtro estricto de "más nuevo que el máximo" pierde filas tardías; una ventana de lookback reprocesa los días recientes para atraparlas. Los cambios de columnas necesitan una política. Los cambios de lógica necesitan un full refresh o un backfill, porque las filas existentes se construyeron con la lógica vieja.
Las pruebas importan más que en las tablas: las llaves duplicadas son el bug clásico, y comparar de vez en cuando con una reconstrucción completa demuestra que los incrementos siguen cuadrando.

<!-- example -->

```sql
{% if is_incremental() %}
-- 3-day lookback catches late events; unique_key de-duplicates the overlap
where occurred_at >= (select dateadd(day, -3, max(occurred_at)) from {{ this }})
{% endif %}
```

#### ¿Qué hace `incremental_predicates`?

Añade condiciones al merge, por ejemplo limitar la lectura de la tabla destino a las particiones recientes, lo que reduce el costo en tablas grandes.

#### ¿Puede un modelo incremental referenciarse a sí mismo?

Sí, con `{{ this }}` dentro del bloque `is_incremental()`, normalmente para leer la marca de tiempo máxima actual.

#### ¿Cómo se testea bien un modelo incremental?

Comprueba la unicidad de la clave primaria (los duplicados son el error típico), compáralo con un full refresh en un entorno inferior y escribe tests unitarios que fuercen `is_incremental` a true y a false.

#### ¿Qué es un modelo incremental "append-only"?

Uno con la estrategia `append` y sin `unique_key`: las filas solo se insertan. Encaja con registros de eventos inmutables en los que nada cambia.

#### ¿Cómo interactúan el particionado o el clustering con los modelos incrementales?

Particionar o agrupar la tabla destino por la columna del filtro (normalmente una fecha) hace que tanto el filtro incremental como el merge lean menos datos, que es de donde sale la mayor parte del ahorro.

#### ¿Por qué un modelo incremental puede volverse más lento con el tiempo?

El merge tiene que recorrer una tabla destino cada vez mayor. Los incremental predicates, la poda de particiones, el clustering o las estrategias `insert_overwrite` y `microbatch` mantienen cada ejecución acotada.

<!-- challenge -->

Cambias cómo se calcula `net_amount` en un modelo incremental. Las filas nuevas salen bien, pero las del año pasado siguen con la fórmula vieja. ¿Qué haces?

<!-- solution -->

Reconstruye la historia: corre con `--full-refresh` (o un backfill de microbatch sobre el rango afectado). Las ejecuciones incrementales nunca revisitan filas viejas, así que los cambios de lógica exigen reprocesarlas.

<!-- takeaways -->

- Usa ventanas de lookback para datos tardíos.
- Los cambios de lógica necesitan full refresh o backfill.
- Prueba duplicados en las llaves; compara con reconstrucciones completas.

<!-- unit: Modelos incrementales en el tiempo -->

<!-- goals -->

- Explicar por qué los modelos incrementales se vuelven lentos y cómo arreglarlo.
- Elegir entre modelos incrementales y snapshots.

<!-- concept -->

Un modelo incremental rápido al lanzarse puede volverse lento un año después, porque cada merge escanea un destino que crece sin parar. Limitar el escaneo con predicados, particionamiento o clustering mantiene el costo proporcional a los datos nuevos.
Los modelos incrementales y los snapshots "agregan con el tiempo", pero responden preguntas distintas. Los incrementales guardan el último estado o el flujo de eventos según tu lógica; los snapshots registran cómo cambiaron las filas mutables de la fuente.

<!-- example -->

| Necesidad | Usa |
|---|---|
| Anexar eventos de clic con eficiencia | Incremental (append) |
| Mantener las órdenes actuales, actualizadas en sitio | Incremental (merge) |
| Historia de los cambios de plan de cada cliente | Snapshot |

#### ¿Cómo se rellena (backfill) un modelo incremental?

Con `--full-refresh`, o en los modelos microbatch con `--event-time-start` y `--event-time-end` para reprocesar un periodo, o ejecutándolo con una variable que cambie la ventana del filtro.

#### ¿Qué diferencia hay entre un modelo incremental y un snapshot?

Un modelo incremental guarda el último estado (o añade eventos) y su lógica es tuya. Un snapshot guarda el historial completo de los cambios de registros mutables, como filas SCD tipo 2 con fechas de validez.

<!-- challenge -->

El tiempo de ejecución de un modelo incremental con merge pasó de 2 a 25 minutos en un año, aunque el volumen diario es estable. ¿Qué haces?

<!-- solution -->

Limita el escaneo del destino: agrega `incremental_predicates` sobre un rango de fechas reciente y particiona o agrupa la tabla por esa fecha, para que el merge solo toque datos recientes.

<!-- takeaways -->

- Los merges sin límite se vuelven lentos al crecer las tablas.
- Predicados y clustering mantienen baratos los merges.
- Incremental guarda estado; los snapshots guardan historia.

### Snapshots

<!-- unit: Capturar la historia con snapshots -->

<!-- goals -->

- Definir snapshots con estrategia timestamp o check.
- Explicar las columnas que agrega dbt y cómo los snapshots implementan SCD2.

<!-- concept -->

Las tablas fuente suelen sobrescribir filas: cambia el plan de un cliente y el valor viejo desaparece. Los snapshots registran esos cambios. Cada ejecución compara la fuente con la última versión registrada y, si algo cambió, cierra la versión vieja e inserta una nueva, que es exactamente una dimensión de cambio lento tipo 2.
Detectar el cambio es la estrategia: una columna updated-at confiable es lo más barato; sin ella, comparar columnas seleccionadas o todas funciona a mayor costo.

<!-- example -->

```yaml
# snapshots/customers_snapshot.yml
snapshots:
  - name: customers_snapshot
    relation: source('crm', 'customers')
    config:
      unique_key: customer_id
      strategy: timestamp
      updated_at: updated_at
      hard_deletes: invalidate
```

#### ¿Qué es un snapshot?

Un recurso de dbt que registra los cambios de una tabla mutable a lo largo del tiempo (Slowly Changing Dimension tipo 2). Cada ejecución compara las filas actuales de la source con la tabla del snapshot, cierra las filas que cambiaron fijando `dbt_valid_to` e inserta su nueva versión con `dbt_valid_from`.

#### ¿Cómo se define un snapshot?

En las versiones recientes de dbt, en YAML (los proyectos antiguos usan un bloque `{% snapshot %}` en `snapshots/`):

```yaml
snapshots:
  - name: customers_snapshot
    relation: source('crm', 'customers')
    config:
      schema: snapshots
      unique_key: customer_id
      strategy: timestamp
      updated_at: updated_at
```

#### ¿Qué estrategias de snapshot existen?

`timestamp`: una fila cambió si su columna `updated_at` es más reciente. Es fiable y eficiente cuando la source mantiene esa columna. `check`: una fila cambió si alguna de las `check_cols` listadas (o todas las columnas) es distinta. Se usa cuando no hay una marca de tiempo fiable.

#### ¿Qué columnas añade dbt a un snapshot?

`dbt_scd_id`, `dbt_updated_at`, `dbt_valid_from` y `dbt_valid_to` (NULL para la versión actual, salvo que se configure `dbt_valid_to_current`).

#### ¿Cómo gestionan los snapshots las filas borradas en la source?

Por defecto, no las gestionan. Con `hard_deletes: invalidate` (antes `invalidate_hard_deletes`), las filas borradas reciben su `dbt_valid_to`. Con `hard_deletes: new_record`, una nueva fila marca el borrado de forma explícita.

#### ¿Por qué los snapshots deben leer de sources y no de modelos transformados?

Los snapshots capturan un historial que no se puede recrear después. Hacer el snapshot de los datos en bruto con la mínima lógica significa que un error en el código de transformación no corrompe el historial, y que las transformaciones se pueden volver a ejecutar encima.

<!-- challenge -->

Una tabla fuente no tiene columna `updated_at`, pero importan los cambios en `plan` y `status`. ¿Cómo configuras el snapshot?

<!-- solution -->

Usa la estrategia `check` con `check_cols: ['plan', 'status']`, para que dbt compare esas columnas en cada ejecución y registre una versión nueva cuando cambien.

<!-- takeaways -->

- Los snapshots registran cambios de filas mutables (SCD2).
- La estrategia timestamp es la más barata; check funciona sin timestamps.
- dbt agrega columnas de vigencia y de ID.

<!-- unit: Correr snapshots con seguridad -->

<!-- goals -->

- Manejar borrados, problemas de llave y frecuencia de ejecución.
- Explicar por qué los snapshots no se pueden reconstruir y en qué difieren del time travel.

<!-- concept -->

Los snapshots son la única parte de un proyecto dbt que no se puede regenerar: si un cambio no se capturó, se perdió. Eso define todas sus reglas. Lee las fuentes crudas para que la historia refleje la realidad y no tu lógica actual. Córrelos con la frecuencia suficiente para atrapar cambios que se revierten. Asegúrate de que la llave sea única, o las versiones se revuelven.
Los borrados necesitan manejo explícito, y el time travel del warehouse no los reemplaza: su retención es corta y está hecho para recuperar, no para historia.

<!-- example -->

| Regla | Por qué |
|---|---|
| Haz snapshot de sources, no de marts | Los cambios de lógica reescribirían la historia |
| Prueba la unicidad de la llave de la fuente | Los duplicados corrompen las versiones |
| Córrelos al menos tan seguido como importan los cambios | Los cambios no capturados se pierden |
| Nunca borres la tabla del snapshot | No hay full refresh posible |

#### ¿Con qué frecuencia deben ejecutarse los snapshots?

Tan a menudo como haga falta para capturar los cambios: los cambios que ocurren y se deshacen entre dos ejecuciones se pierden. Muchos equipos los ejecutan cada hora o cada día, antes de los modelos que los usan.

#### ¿Cómo se consulta la versión actual de cada registro de un snapshot?

`where dbt_valid_to is null` (o el valor actual configurado).

#### ¿Cómo se obtiene el estado de un registro en una fecha dada?

```sql
select * from {{ ref('customers_snapshot') }}
where '2026-06-30' >= dbt_valid_from
  and ('2026-06-30' < dbt_valid_to or dbt_valid_to is null)
```

#### ¿Se puede hacer un full refresh de un snapshot?

No. dbt nunca reconstruye los snapshots, porque se perdería el historial. Para cambiar uno, se migra la tabla a mano o se empieza un snapshot nuevo.

#### ¿Qué pasa si la `unique_key` no es única en la source?

El snapshot produce versiones duplicadas o incoherentes. Testea la unicidad en la source y deduplica antes si hace falta.

#### ¿Cuándo usarías la estrategia `check` con `check_cols: all`?

Cuando la source no tiene un `updated_at` fiable y cualquier cambio de columna importa. Es más costosa porque compara todas las columnas.

<!-- challenge -->

Un snapshot corre a diario, pero a veces los clientes cambian de plan y vuelven al anterior en pocas horas. El negocio quiere ver esos cambios. ¿Qué cambias?

<!-- solution -->

Corre el snapshot con más frecuencia (por ejemplo cada hora) o captura los cambios aguas arriba con CDC. Un snapshot diario solo ve el estado al momento de correr, así que los cambios de corta duración se pierden.

<!-- takeaways -->

- Los snapshots no se pueden reconstruir; protégelos.
- Haz snapshot de fuentes crudas con llaves únicas.
- Maneja los borrados explícitamente; el time travel no es historia.

<!-- unit: Consultar snapshots -->

<!-- goals -->

- Consultar versiones actuales y en un punto del tiempo desde un snapshot.
- Construir una dimensión historizada sobre un snapshot.

<!-- concept -->

Un snapshot es historia cruda, y como otros datos crudos se consume mejor a través de un modelo. Las versiones actuales son las filas cuya vigencia no ha terminado; una vista en un punto del tiempo elige la versión cuyo rango contiene una fecha.
Un modelo de dimensión encima renombra las columnas de vigencia, agrega un flag de actual y una llave sustituta, y da a los hechos algo limpio con qué cruzarse.

<!-- example -->

```sql
-- models/marts/dim_customer.sql
select
    {{ dbt_utils.generate_surrogate_key(['customer_id', 'dbt_valid_from']) }} as customer_key,
    customer_id, plan, status,
    dbt_valid_from as valid_from,
    coalesce(dbt_valid_to, '9999-12-31'::timestamp) as valid_to,
    dbt_valid_to is null as is_current
from {{ ref('customers_snapshot') }}
```

#### ¿En qué se diferencian los snapshots del time travel de Delta Lake o del almacén?

El time travel del almacén guarda versiones pasadas de la tabla durante un periodo de retención limitado y sirve para recuperar datos. Los snapshots construyen una tabla de historial permanente y consultable a nivel de fila, pensada para el análisis.

#### ¿Qué es una SCD tipo 2 y cómo la implementan los snapshots de dbt?

Una dimensión de cambio lento que guarda una fila nueva por cada versión de un registro, con fechas de validez. Los snapshots de dbt son exactamente eso: una fila por versión, con `dbt_valid_from` y `dbt_valid_to` delimitando su validez.

#### ¿Cómo se construye una dimensión con historial a partir de un snapshot?

Selecciona del snapshot en un modelo, renombra `dbt_valid_from` y `dbt_valid_to` a nombres más claros, añade una clave subrogada por versión y un indicador `is_current`, y une los hechos por la clave natural y la fecha del hecho dentro del rango de validez.

<!-- challenge -->

Finanzas pide el plan de cada cliente al 30 de junio. Escribe el filtro.

<!-- solution -->

`where '2026-06-30' >= dbt_valid_from and ('2026-06-30' < dbt_valid_to or dbt_valid_to is null)` sobre el snapshot (o el equivalente con `valid_from`/`valid_to` en la dimensión).

<!-- takeaways -->

- Las filas actuales no tienen fin de vigencia.
- Las consultas en un punto del tiempo filtran por rango de vigencia.
- Construye dimensiones encima de los snapshots.

<!-- stage: Producción -->

### Documentación, linaje y capa semántica

<!-- unit: Documentar proyectos -->

<!-- goals -->

- Escribir descripciones y generar el sitio de documentación.
- Usar persist_docs, campos meta y exposures.

<!-- concept -->

La documentación de dbt vive junto al código: descripciones en YAML para modelos y columnas, textos más largos en doc blocks. Generar el sitio de docs las combina con el DAG y las pruebas, así el lector ve qué significa una tabla y de dónde viene.
La documentación llega más lejos cuando sale de dbt: persistir las descripciones en el warehouse las muestra en las herramientas de BI, los campos meta registran dueños y sensibilidad, y las exposures declaran qué dashboards dependen de qué modelos.

<!-- example -->

```yaml
exposures:
  - name: revenue_dashboard
    type: dashboard
    owner: {name: Finance Data, email: finance-data@example.com}
    depends_on: [ref('fct_revenue'), ref('dim_customer')]
models:
  - name: fct_revenue
    description: "One row per invoice line. Net of refunds and discounts, in EUR."
    meta: {owner: finance-data, contains_pii: false}
    config: {persist_docs: {relation: true, columns: true}}
```

#### ¿Cómo genera dbt la documentación?

`dbt docs generate` construye un sitio estático a partir del proyecto (descripciones, columnas, tests, SQL) y de los metadatos del almacén (tipos de columna, número de filas). `dbt docs serve` lo sirve en local. Incluye un grafo de linaje interactivo.

#### ¿Dónde se escriben las descripciones?

En archivos de propiedades YAML junto a los modelos (`description:` en modelos y columnas), o en bloques `{% docs %}` de archivos `.md` referenciados con `{{ doc('name') }}` para textos más largos.

#### ¿Qué es `persist_docs`?

Una configuración que escribe las descripciones de modelos y columnas en el almacén como comentarios de tablas y columnas, para que se vean en otras herramientas.

#### ¿Qué son las exposures?

Declaraciones YAML de los usos aguas abajo de los modelos de dbt (cuadros de mando, modelos de ML, aplicaciones) con sus responsables, para que el linaje muestre qué depende de cada modelo.

#### ¿Qué hace `dbt ls`?

Lista los nodos que coinciden con una selección sin ejecutarlos, lo que es útil para comprobar los selectores.

#### ¿Qué es el artefacto `manifest.json`?

Un archivo JSON de `target/` que describe todo el proyecto (nodos, configuraciones, dependencias). Se usa para comparar estados (`state:modified`), para la documentación y en herramientas externas.

<!-- challenge -->

Antes de cambiar `fct_revenue`, un ingeniero quiere saber qué dashboards se verán afectados. ¿Cómo lo responde el proyecto?

<!-- solution -->

Con exposures declaradas para los dashboards: el DAG muestra qué exposures dependen de `fct_revenue`, con sus dueños, y `dbt ls --select fct_revenue+` las lista.

<!-- takeaways -->

- Las descripciones viven en YAML junto a los modelos.
- `persist_docs` las lleva al warehouse.
- Las exposures conectan los modelos con sus consumidores.

<!-- unit: Artefactos y linaje -->

<!-- goals -->

- Usar los artefactos de dbt para linaje, monitoreo y chequeos de selección.
- Explicar el linaje a nivel de columna.

<!-- concept -->

Cada invocación de dbt escribe artefactos: un manifest que describe todo el proyecto y run results con el resultado y la duración de cada nodo. Muchas herramientas se construyen sobre ellos: comparación de estado en CI, dashboards de observabilidad, catálogos y grafos de linaje.
El linaje a nivel de modelo muestra qué tablas dependen de cuáles; el de columna va más allá y rastrea cada columna hasta sus fuentes, lo que responde con precisión "¿qué se rompe si borro esta columna?".

<!-- example -->

```bash
dbt ls --select state:modified+ --state prod-artifacts/    # check a selection before running
jq '.results[] | {node: .unique_id, s: .execution_time}' target/run_results.json | head
```

#### ¿Qué es `run_results.json`?

Un artefacto con el resultado, la duración y el estado de cada nodo de la última invocación, que se usa para la monitorización y para `dbt retry`.

#### ¿Cuál es la arquitectura de la capa semántica de dbt?

Los modelos semánticos se definen en YAML sobre los modelos de dbt, declarando entidades (claves de unión), dimensiones y medidas. Las métricas se definen sobre esas medidas. MetricFlow convierte una solicitud de métrica (métrica, dimensiones, filtros, granularidad) en SQL optimizado para el almacén, y la dbt platform la expone mediante API e integraciones con herramientas de BI.

#### ¿Qué es un modelo semántico?

Una definición YAML ligada a un modelo de dbt que describe sus entidades, dimensiones y medidas, para que MetricFlow sepa cómo agregarlo y unirlo.

#### ¿Qué tipos de métricas existen en la capa semántica?

Simples (una medida), de ratio, acumuladas (totales acumulados o ventanas), derivadas (expresiones sobre otras métricas) y de conversión.

#### ¿Por qué definir las métricas en dbt y no en la herramienta de BI?

Para que la definición exista una sola vez, en el control de versiones, con tests y revisión, y todas las herramientas devuelvan el mismo número para "ingresos" o "usuarios activos".

<!-- challenge -->

Quieres un reporte semanal de los diez modelos más lentos y las pruebas que más fallaron. ¿De dónde salen los datos?

<!-- solution -->

Del `run_results.json` de cada ejecución de producción (tiempo y estado por nodo), cruzado con `manifest.json` para los metadatos de los modelos, cargado en una tabla y agregado por semana.

<!-- takeaways -->

- `manifest.json` describe el proyecto; `run_results.json`, la ejecución.
- Los artefactos alimentan CI, observabilidad y catálogos.
- El linaje de columna rastrea el origen de cada columna.

<!-- unit: La capa semántica -->

<!-- goals -->

- Describir semantic models, measures, dimensions y tipos de métricas.
- Explicar por qué las métricas van en dbt y no en las herramientas de BI.

<!-- concept -->

Cuando cada herramienta de BI define "ingresos" por su cuenta, las cifras se desvían. La capa semántica define las métricas una vez en dbt, sobre los modelos: los semantic models declaran entidades para cruzar, dimensiones para segmentar y medidas para agregar, y las métricas combinan medidas en definiciones de negocio.
Las herramientas consultan la métrica por nombre, y la capa genera el SQL correcto con los joins, el grano y los filtros adecuados, así cada consumidor recibe la misma respuesta.

<!-- example -->

```yaml
semantic_models:
  - name: orders
    model: ref('fct_orders')
    entities: [{name: order_id, type: primary}, {name: customer_id, type: foreign}]
    dimensions: [{name: ordered_at, type: time, type_params: {time_granularity: day}}]
    measures: [{name: revenue, agg: sum, expr: net_amount}]
metrics:
  - name: revenue
    type: simple
    type_params: {measure: revenue}
```

#### ¿Qué es el linaje a nivel de columna?

Un linaje que muestra qué columnas de origen alimentan cada columna, y no solo qué modelos dependen de cuáles. Lo ofrecen la dbt platform y dbt Fusion.

#### ¿Para qué sirven los artefactos de dbt en la observabilidad?

Las herramientas analizan `manifest.json` y `run_results.json` para seguir la duración de las ejecuciones, los fallos de tests y la frescura a lo largo del tiempo, y el paquete `dbt_artifacts` los carga en el almacén para analizarlos.

#### ¿Qué son los campos meta?

Un diccionario libre `meta:` en nodos y columnas, por ejemplo para registrar responsables, marcas de datos personales o acuerdos de nivel de servicio, que pueden leer las herramientas y las macros.

#### ¿Cómo se documenta un test o una macro?

Los tests y las macros pueden tener propiedades `description` en YAML, que aparecen en la documentación generada.

<!-- challenge -->

La herramienta de BI de marketing y la hoja de cálculo de finanzas muestran distinto "valor promedio de orden". ¿Cómo lo arreglaría la capa semántica?

<!-- solution -->

Define el AOV una vez como métrica de ratio (ingresos / órdenes) en dbt, revisada en Git, y haz que ambas herramientas consulten la métrica por la API de la capa semántica en lugar de calcularla por su cuenta.

<!-- takeaways -->

- Los semantic models declaran entidades, dimensiones y medidas.
- Las métricas se definen una vez, en control de versiones.
- Todas las herramientas consultan las mismas definiciones.

### Despliegue, entornos, CI/CD y orquestación

<!-- unit: Ambientes, control de versiones y CI -->

<!-- goals -->

- Manejar dev, staging y producción con un solo código.
- Correr Slim CI con `state:modified` y desplegar con seguridad.

<!-- concept -->

dbt abarata los ambientes: un solo código, varios targets, cada uno escribiendo en sus propios esquemas. Los desarrolladores construyen en esquemas personales, CI en un esquema por pull request, producción en producción.
Slim CI compara el proyecto con los artefactos de producción y construye solo los modelos modificados y sus hijos, haciendo defer a producción para el resto. Para cambios de alto riesgo, construir una versión completa nueva junto a la vieja y cambiarlas de forma atómica da un despliegue blue-green.

<!-- example -->

```bash
# CI for a pull request
dbt deps
dbt build --select state:modified+ --defer --state prod-artifacts/ --target ci
```

#### ¿Cómo gestionarías los despliegues de dbt en varios entornos (dev, staging, producción)?

Con un único código y varios targets (o entornos de la dbt platform) que apuntan a esquemas o bases de datos separados: cada desarrollador construye en un esquema dev personal, la CI construye en un esquema temporal y los trabajos programados construyen producción. Las diferencias entre entornos vienen de `profiles.yml`, de las variables de entorno y de `target.name`, nunca de cambios en el código. Los cambios solo llegan a producción mediante pull requests y CI.

#### ¿Cómo gestionas el control de versiones de dbt cuando trabajan varias personas?

Git con ramas de funcionalidad y pull requests, revisión de código, CI que construye y testea los modelos modificados en cada pull request, una guía de estilo y un linter (SQLFluff), responsables claros de cada modelo, cambios pequeños y acotados, y un esquema dev personal por desarrollador para que nadie pise las tablas de otro.

#### ¿Qué es Slim CI?

Ejecutar en CI solo los modelos modificados y sus dependientes, comparándolos con los artefactos de producción: `dbt build --select state:modified+ --defer --state prod-artifacts/`. Los padres sin cambios se leen de producción en lugar de reconstruirse.

#### ¿Qué selecciona `state:modified`?

Los nodos cuyo SQL, configuración o propiedades difieren del manifest dado con `--state`. Combinado con `+`, incluye a sus hijos.

#### Nombra tres ventajas de integrar dbt con Airflow.

1. Las ejecuciones de dbt se orquestan con el resto del pipeline (esperar a la ingesta, transformar y luego refrescar los cuadros de mando o entrenar modelos).
2. Los reintentos, las alertas, los SLA, los backfills y la planificación vienen de Airflow.
3. Con herramientas como Astronomer Cosmos, cada modelo de dbt se convierte en una tarea de Airflow, lo que da visibilidad detallada y permite reintentar solo los modelos que fallaron.

<!-- challenge -->

CI construye todo el proyecto de 600 modelos en cada pull request y tarda 50 minutos. ¿Qué cambias?

<!-- solution -->

Pasa a Slim CI: descarga el manifest de producción, construye `state:modified+` con `--defer` y usa un esquema por PR. Los PRs típicos construyen entonces unos pocos modelos en minutos.

<!-- takeaways -->

- Un código, muchos targets y esquemas.
- Slim CI construye solo lo que cambió.
- Blue-green pone en su lugar un build completamente probado.

<!-- unit: Orquestar dbt -->

<!-- goals -->

- Programar dbt Core con un orquestador o usar la plataforma dbt.
- Diseñar un job de producción que corra después de la ingesta.

<!-- concept -->

dbt no se programa solo. Con dbt Core, un orquestador lo corre, idealmente como parte de un pipeline mayor: esperar la ingesta, revisar la frescura, construir y probar, y avisar aguas abajo. La plataforma dbt trae jobs y triggers incorporados, con APIs para orquestadores.
Un job típico de producción sigue los mismos pasos en todas partes, y correr dbt en un contenedor lo hace reproducible donde sea que corra.

<!-- example -->

```bash
# typical production job
dbt deps
dbt source freshness
dbt build --target prod
dbt docs generate
# then: upload artifacts, alert on failure, trigger downstream
```

#### ¿Cómo implantarías dbt en un pipeline de datos existente?

Empieza declarando las tablas en bruto existentes como sources, luego reproduce las transformaciones actuales como modelos de staging y marts, un dominio cada vez, comparando las salidas con las tablas heredadas (por ejemplo con `audit_helper`). Añade tests y documentación, ejecuta dbt desde el orquestador existente después de la ingesta, cambia a los consumidores a las nuevas tablas y retira los scripts heredados poco a poco.

#### ¿Cómo se programa dbt en producción con dbt Core?

Con un orquestador (Airflow, Dagster, Prefect, cron, GitHub Actions, Databricks Workflows) que ejecuta `dbt build` (o los comandos seleccionados) en un contenedor o entorno virtual con las credenciales de producción.

#### ¿Cómo es un trabajo de producción típico?

`dbt deps`, `dbt source freshness`, `dbt build` (seeds, snapshots, modelos y tests en orden) y luego `dbt docs generate`, con alertas en caso de fallo y los artefactos guardados para la siguiente comparación de CI.

#### ¿Cómo se despliega dbt en la dbt platform (dbt Cloud)?

Crea entornos de despliegue con sus credenciales, define trabajos (comandos, planificación o disparadores, modelos seleccionados), activa trabajos de CI en las pull requests y usa el encadenamiento de trabajos o disparadores por API para lanzar dbt después de la ingesta.

#### ¿Qué medidas de seguridad ofrece dbt para el acceso a los datos y su transformación?

dbt se ejecuta con los permisos del almacén de las credenciales que usa, así que las cuentas de servicio con mínimo privilegio por entorno son el control principal. También ofrece la configuración `grants` para gestionar los privilegios de los objetos construidos, secretos en variables de entorno (ocultos con el prefijo `DBT_ENV_SECRET_`), niveles de acceso de los modelos y contratos. La dbt platform añade SSO, control de acceso basado en roles, registros de auditoría y restricciones por IP.

#### ¿Cómo garantiza dbt la seguridad de los datos?

dbt nunca guarda ni mueve los datos: las transformaciones se ejecutan dentro del almacén, así que los datos siguen bajo los controles de acceso, el cifrado y la gobernanza del almacén. dbt solo guarda credenciales de conexión, que deben ser secretos con privilegios mínimos.

<!-- challenge -->

dbt corre a las 06:00 por cron, pero la ingesta a veces termina a las 06:30, así que los marts se construyen con datos de ayer. ¿Qué cambias?

<!-- solution -->

Dispara dbt desde el orquestador cuando termine la ingesta (dependencia de tareas, sensor o llamada a API), y deja source freshness como primer paso para que una carga tardía falle de forma visible en vez de construir datos viejos.

<!-- takeaways -->

- Un orquestador o la plataforma dbt corre dbt.
- Arranca dbt cuando termine la ingesta, no a hora fija.
- Jobs de producción: deps, freshness, build, docs.

<!-- unit: Seguridad -->

<!-- goals -->

- Correr dbt con credenciales de mínimo privilegio.
- Aplicar los grants como código.

<!-- concept -->

dbt no agrega ningún acceso a datos propio: corre SQL con los permisos que tengan sus credenciales, dentro del warehouse. La seguridad se reduce entonces a esas credenciales, un usuario de servicio dedicado por ambiente con solo los privilegios que necesita, y a mantener los secretos fuera del repositorio.
Los grants pueden vivir con los modelos, así los permisos se revisan y se aplican en cada build en lugar de darse a mano.

<!-- example -->

```yaml
models:
  shop:
    marts:
      +grants:
        select: ['reporting', 'analyst']
    staging:
      +grants:
        select: []          # no direct access for consumers
```

#### ¿Qué hace la configuración `grants`?

Declara privilegios, y dbt los aplica después de construir un modelo:

```yaml
models:
  +grants:
    select: ['reporter', 'analyst']
```

#### ¿Cómo se monitorizan y diagnostican los problemas en dbt?

Revisa la salida de la consola y `logs/dbt.log`, lee el SQL compilado en `target/compiled` y `target/run`, inspecciona `run_results.json` para ver fallos y duraciones, guarda los fallos de los tests, usa `dbt retry` después de corregir, y sigue el historial y la duración de las ejecuciones en el orquestador o en la dbt platform. Las alertas sobre fallos de trabajos y frescura de sources detectan los problemas pronto.

#### ¿Cómo se depuran los modelos de dbt?

Ejecuta `dbt compile` y lanza el SQL compilado directamente en el almacén, previsualiza con `dbt show`, aísla los CTE paso a paso, usa `{{ log() }}` en Jinja, ejecuta con `--debug` para ver los registros completos y revisa los datos de origen con tests.

<!-- challenge -->

El job de dbt de producción corre con una cuenta personal de administrador. ¿Qué cambias?

<!-- solution -->

Crea un usuario de servicio para producción con privilegios solo sobre las bases y esquemas necesarios, guarda sus credenciales en el gestor de secretos del orquestador y maneja el acceso de los consumidores con `grants` en el proyecto.

<!-- takeaways -->

- dbt tiene exactamente el acceso de sus credenciales.
- Usa usuarios de servicio de mínimo privilegio por ambiente.
- Declara los grants como código con `grants`.

<!-- unit: Depuración, herramientas y adopción -->

<!-- goals -->

- Depurar modelos y entender cómo dbt compila las consultas.
- Introducir dbt en pipelines existentes y escalar con dbt Mesh.

<!-- concept -->

La mayor parte de la depuración en dbt empieza por el SQL compilado: lo que dbt envió de verdad al warehouse, que puedes correr directamente. Logs, artefactos e historial de consultas del warehouse completan el resto. El linting con SQLFluff mantiene el código lo bastante consistente para leerlo rápido.
Adoptar dbt rara vez parte de cero: las tablas existentes se vuelven sources, las transformaciones existentes se reconstruyen modelo a modelo y se comparan. A mayor escala, varios proyectos referencian los modelos públicos de otros con dbt Mesh.

<!-- example -->

```bash
dbt compile --select fct_orders && cat target/compiled/shop/models/marts/fct_orders.sql
dbt --debug run --select fct_orders        # verbose logs
sqlfluff lint models/marts/fct_orders.sql
```

#### ¿Cómo compila dbt las consultas?

dbt analiza el proyecto y construye el DAG, y luego, para cada nodo, renderiza el Jinja: resuelve `ref`, `source`, `var`, `config` y las llamadas a macros en SQL normal para el target actual. El `SELECT` compilado se escribe en `target/compiled/`. En la ejecución, la materialización lo envuelve en DDL/DML (`create table as`, `merge`) y lo envía al almacén a través del adaptador.

#### ¿Qué es SQLFluff?

Un linter y formateador de SQL con un modo para plantillas de dbt, que se usa en CI y en hooks de pre-commit para imponer un estilo SQL coherente.

#### ¿Cómo se ejecuta dbt en un contenedor Docker?

Usa una imagen con dbt Core y el adaptador instalados, monta o copia el proyecto, pasa las credenciales por variables de entorno y ejecuta comandos como `dbt build --target prod`.

#### ¿Qué es dbt Mesh?

Un patrón para organizaciones grandes en el que varios proyectos de dbt referencian los modelos públicos de los demás (`ref` entre proyectos), con contratos, versiones y controles de acceso, para que cada dominio gestione su proyecto de forma independiente.

#### ¿Cómo se lanza dbt cuando termina la ingesta?

Mediante el orquestador (una dependencia entre tareas o un sensor), los disparadores por API o el encadenamiento de trabajos de la dbt platform, o la integración de la herramienta de ingesta (por ejemplo Fivetran lanzando un trabajo de dbt).

#### ¿Qué es un despliegue azul-verde con dbt?

Construir producción en un esquema o base de datos nuevos, testearla y luego intercambiarla de forma atómica (renombrando esquemas o cambiando vistas), para que los consumidores nunca vean datos construidos a medias.

<!-- challenge -->

Un modelo devuelve totales erróneos, y el Jinja hace difícil ver por qué. ¿Cuál es tu primer paso?

<!-- solution -->

Compílalo y corre el SQL compilado directamente en el warehouse, luego consulta cada CTE por separado para encontrar dónde se desvían las cifras. Corrige la lógica y agrega un unit test para el caso.

<!-- takeaways -->

- Depura el SQL compilado, no la plantilla.
- Adopta dbt envolviendo las tablas existentes como sources.
- dbt Mesh conecta varios proyectos con modelos públicos.

### Rendimiento, almacenes y resolución de problemas

<!-- unit: Ejecuciones más rápidas y baratas -->

<!-- goals -->

- Acelerar proyectos dbt con materializaciones, threads y modelos incrementales.
- Encontrar modelos lentos y bajar costos, también en Snowflake.

<!-- concept -->

El tiempo de ejecución de un proyecto dbt es la suma de sus consultas, así que el trabajo de rendimiento es sobre todo trabajo del warehouse. Materializa lo que se consulta seguido, vuelve incrementales los hechos grandes, evita cadenas largas de vistas que lo recalculan todo y corre en paralelo los modelos independientes con suficientes threads.
Mide antes de cambiar: los tiempos de ejecución muestran los modelos más lentos, y el modelo de costo de vistas, tablas e incrementales explica a dónde va el dinero. El desarrollo puede ser aún más barato trabajando con muestras y haciendo defer a producción.

<!-- example -->

| Materialización | Costo de build | Costo de consulta |
|---|---|---|
| View | ~0 | Consulta completa en cada lectura |
| Table | Consulta completa en cada build | Barato |
| Incremental | Solo datos nuevos | Barato |

#### ¿Cómo optimizarías el rendimiento de las transformaciones de dbt sobre grandes volúmenes?

Materializa como tablas los modelos costosos y usa modelos incrementales para las grandes tablas de hechos, filtra y agrega pronto, evita `select *` y los joins innecesarios, particiona y agrupa las tablas grandes por las columnas de filtro, usa las funciones nativas del almacén (claves de clustering, claves de ordenación), limita los datos en desarrollo y revisa los perfiles de las consultas y los tiempos de `run_results.json` para encontrar los modelos más lentos.

#### Nombra algunas técnicas de optimización de dbt en Snowflake.

Usa tablas transitorias para los modelos intermedios (sin costo de almacenamiento Fail-safe), agrupa (clustering) las tablas muy grandes por las columnas de filtro habituales, dimensiona los warehouses por trabajo (y separa los de dbt y los de BI), usa `merge` o `delete+insert` con incremental predicates, apóyate en el clonado sin copia para dev y CI (`dbt clone`), fija `query_tag` para atribuir costos y activa la suspensión automática de los warehouses.

#### ¿Cómo compararías dbt y BigQuery?

No son alternativas: BigQuery es un almacén de datos serverless que guarda y procesa los datos, mientras que dbt es un framework de transformación que genera SQL y lo ejecuta en BigQuery (a través de dbt-bigquery). Las consultas programadas de BigQuery o Dataform cubren un terreno parecido al de dbt, pero dbt añade portabilidad entre plataformas, un gran ecosistema de paquetes y una comunidad amplia. En BigQuery, dbt admite particionado, clustering e `insert_overwrite`.

#### ¿Cómo se aceleran en general las ejecuciones de dbt?

Aumenta los `threads` dentro de los límites del almacén, elimina los modelos innecesarios, convierte en vistas las tablas poco consultadas (o al revés para las vistas pesadas), usa modelos incrementales, ejecuta solo lo que ha cambiado (`state:modified+`) en CI y separa los trabajos según sus necesidades de frescura.

#### ¿Por qué una cadena larga de vistas puede ser lenta?

Cada consulta a la vista final ejecuta toda la cadena de SQL subyacente. Materializar como tablas los modelos intermedios clave evita repetir el cálculo.

#### ¿Cómo se encuentran los modelos más lentos?

Con los tiempos de `run_results.json`, la vista de tiempos de modelos de la dbt platform o el historial de consultas del almacén filtrado por el `query_tag` de dbt.

#### ¿Qué impacto en costos tienen las vistas, las tablas y los modelos incrementales?

Las vistas cuestan cómputo cada vez que se consultan. Las tablas cuestan cómputo en cada construcción, más almacenamiento. Los modelos incrementales cuestan poco por ejecución, pero requieren cuidado para seguir siendo correctos.

#### ¿Qué provoca el "fan-out" en los modelos de dbt y cómo se detecta?

Unir por una clave que no es única en uno de los lados multiplica las filas e infla las sumas. Los tests de unicidad sobre las claves de unión y sobre la granularidad de cada modelo lo detectan.

<!-- challenge -->

Una ejecución nocturna tarda 3 horas, pero el warehouse muestra largos huecos ociosos entre consultas. ¿Qué ajuste revisas primero?

<!-- solution -->

`threads`: con muy pocos, los modelos independientes esperan en fila. Sube los threads dentro de los límites de concurrencia del warehouse y luego revisa el camino crítico del DAG buscando modelos lentos.

<!-- takeaways -->

- Materializa los modelos muy usados; vuelve incrementales los hechos grandes.
- Mide con los tiempos de ejecución antes de optimizar.
- Desarrolla con muestras y haz defer a producción.

<!-- unit: Problemas de corrección -->

<!-- goals -->

- Atrapar fan-out, duplicados y ciclos en los modelos dbt.
- Manejar cambios de esquema en las fuentes.

<!-- concept -->

Algunos problemas producen cifras erróneas en lugar de errores. Los joins sobre llaves que no son únicas multiplican filas; las fuentes que reenvían registros crean duplicados; las columnas de la fuente que cambian rompen modelos o botan datos en silencio. Las pruebas de unicidad y las listas explícitas de columnas atrapan la mayoría temprano.
Los ciclos son el único problema que dbt rechaza de plano: si dos modelos se necesitan entre sí, la lógica compartida va en un tercer modelo aguas arriba de ambos.

<!-- example -->

```sql
-- staging: keep the latest row per key
select * from {{ source('shop', 'orders') }}
qualify row_number() over (partition by id order by _loaded_at desc) = 1
```

#### ¿Cómo se limitan los datos en desarrollo para ahorrar tiempo y dinero?

Filtrando por fecha o con una muestra cuando `target.name == 'dev'`, usando `--defer` para reutilizar los padres de producción, o usando clones sin copia.

#### ¿Qué haces con dependencias entre modelos que forman un ciclo?

dbt rechaza los ciclos. Reestructura la lógica, normalmente extrayendo la parte común a un modelo previo que referencien ambos modelos.

#### ¿Qué pasa cuando un modelo falla a mitad de una ejecución?

Los modelos que dependen de él se omiten, las ramas independientes continúan y la ejecución informa del fallo. Corrígelo y ejecuta `dbt retry`, o vuelve a ejecutar el modelo que falló y sus hijos con `model+`.

#### ¿Cómo se gestionan los cambios de esquema en las sources?

Detectándolos con tests y contratos, usando listas de columnas explícitas en staging en lugar de `select *`, configurando `on_schema_change` en los modelos incrementales y adaptando los modelos de staging en un único sitio.

<!-- challenge -->

El modelo A hace ref al B para los segmentos de clientes, y ahora B necesita los totales de órdenes de A. dbt reporta un ciclo. ¿Cómo reestructuras?

<!-- solution -->

Pasa la lógica compartida a un nuevo modelo aguas arriba (por ejemplo `int_customer_orders` con totales de órdenes por cliente) que referencien tanto A como B, y elimina la dependencia mutua.

<!-- takeaways -->

- El fan-out viene de llaves de join que no son únicas.
- Deduplica las fuentes en staging.
- Rompe los ciclos con un modelo compartido aguas arriba.

<!-- unit: Resolver problemas en producción -->

<!-- goals -->

- Entender qué pasa cuando un modelo falla a mitad de una ejecución.
- Monitorear las ejecuciones de producción e investigar las lentitudes.

<!-- concept -->

En producción, el DAG contiene las fallas: un modelo que falla salta a sus hijos mientras las ramas independientes terminan. Volver a correr solo la parte fallida tras un arreglo evita reconstruirlo todo.
El monitoreo convierte las ejecuciones en tendencias: fallas, resultados de pruebas y duraciones en el tiempo. Cuando un job tarda de pronto el doble, la causa suele ser crecimiento de datos, un filtro incremental perdido, una materialización cambiada o contención en el warehouse, y comparar ejecuciones señala cuál.

<!-- example -->

```text
run 2026-10-16: 41 min   run 2026-10-17: 88 min
slowest node change: fct_events 6 min → 52 min
manifest diff: fct_events materialized 'incremental' → 'table' (PR #212)
```

#### ¿Qué haces con filas duplicadas que vienen de una source?

Deduplicarlas en el modelo de staging, normalmente con una función de ventana que conserve la fila más reciente por clave, y testear la unicidad después:

```sql
select *
from {{ source('crm', 'customers') }}
qualify row_number() over (partition by customer_id order by updated_at desc) = 1
```

#### ¿Cómo monitorizas y diagnosticas los problemas de dbt en producción?

Alertas ante fallos de trabajos y errores de tests, seguimiento de la tendencia de los fallos de tests y de la duración de las ejecuciones, comprobación de la frescura de las sources antes de ejecutar, conservación de los artefactos para comparar, y un procedimiento de guardia documentado (revisar registros y SQL compilado, relanzar con `dbt retry`, comunicar los incidentes de datos a los consumidores).

#### ¿Qué revisarías si un trabajo de dbt pasa de repente a tardar el doble?

El crecimiento del volumen de datos en las sources, un modelo que cambió de materialización o perdió su filtro incremental, un full refresh lanzado por error, el tamaño del warehouse o las colas, un join nuevo que multiplica filas, y la falta de poda de particiones.

<!-- challenge -->

Una ejecución de producción falló en un mart a las 05:00. Tras corregir el SQL, ¿cómo completas la ejecución rápido?

<!-- solution -->

Despliega el arreglo y corre `dbt retry` (o `dbt build --select <failed_model>+`), que reconstruye el modelo fallido y sus hijos saltados sin volver a correr todo lo que salió bien.

<!-- takeaways -->

- Las fallas saltan a los hijos; las ramas independientes siguen.
- `dbt retry` retoma desde las fallas.
- Compara los tiempos de ejecución para explicar las lentitudes.
