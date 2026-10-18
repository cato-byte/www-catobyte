## Guía de estudio de dbt

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de dbt: unas 200 preguntas](../../images/dbt_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre dbt (data build tool), desde lo básico hasta los modelos incrementales, los snapshots, los tests, el despliegue y el rendimiento. Las respuestas siguen las convenciones de dbt Core 1.x. Abre una pregunta para ver su respuesta, o usa el filtro para buscar en toda la guía.

<!-- QA -->

### Fundamentos

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

### Proyectos y configuración

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

#### ¿Qué son los analyses en dbt?

Archivos SQL de `analyses/` que se compilan (con Jinja y `ref` resueltos) pero que `dbt run` nunca ejecuta. Son útiles para consultas puntuales que se benefician de las referencias de dbt.

#### ¿Qué hace `dbt clean`?

Borra las carpetas listadas en `clean-targets` (normalmente `target/` y `dbt_packages/`).

#### ¿Qué son el acceso a modelos y los grupos?

Funciones de gobierno. El `access` de un modelo puede ser `private` (solo referenciable dentro de su grupo), `protected` (dentro del proyecto, el valor por defecto) o `public` (desde otros proyectos). Los grupos asignan la propiedad de un conjunto de modelos.

#### ¿Qué son las versiones de modelos?

Una forma de publicar una nueva versión de un modelo público (`fct_orders_v2`) mientras los consumidores siguen usando la antigua hasta migrar, con `ref('fct_orders', v=1)`.

### Sources y seeds

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

#### ¿Qué diferencia hay entre `ref()` y `source()`?

`ref()` apunta a otro nodo de dbt (modelo, seed, snapshot) y crea una dependencia que el DAG usa para ordenar las ejecuciones. `source()` apunta a datos en bruto cargados fuera de dbt. Ambos se resuelven al nombre completo de la tabla en el target actual.

#### ¿A qué se resuelve `ref()` en entornos distintos?

A la relación en la base de datos y el esquema del target actual, así que el mismo código construye en el esquema de un desarrollador en dev y en los esquemas de producción en prod.

#### ¿Qué es la organización en capas "staging, intermediate, marts"?

Una estructura habitual: staging limpia cada source, intermediate contiene joins y lógica de negocio reutilizables, y los marts son las tablas de hechos y dimensiones finales (o tablas anchas) que consumen BI y los analistas.

#### ¿Para qué se usa `dbt source freshness` en producción?

Para detectar una ingesta rota o retrasada antes de que los modelos se ejecuten sobre datos obsoletos, a menudo como primer paso de un trabajo programado.

### Modelos y materializaciones

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

### Jinja y macros

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

#### ¿Qué son los filtros de Jinja? Da ejemplos.

Funciones que se aplican con `|`, como `{{ name | upper }}`, `{{ columns | join(', ') }}` o `{{ value | default('n/a') }}`.

#### ¿Cómo se evita complicar de más el código con Jinja?

Escribe primero SQL normal, extrae una macro solo cuando la lógica se repite o debe variar según el adaptador, documenta los argumentos de las macros y comprueba que el SQL compilado se lee bien.

#### ¿Qué es la macro `star` de dbt_utils?

`{{ dbt_utils.star(ref('model'), except=['col']) }}` genera la lista de columnas de una relación, menos algunas, para evitar `select *` sin escribir todas las columnas.

### Tests y calidad de datos

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

#### ¿Qué hay que testear como mínimo en cada modelo?

La clave primaria con `unique` y `not_null`, las claves foráneas de los joins importantes con `relationships` y las columnas categóricas con `accepted_values`. Añade reglas de negocio donde un error saldría caro.

#### ¿Qué significa "testear en el origen"?

Poner tests en las sources y en los modelos de staging, para detectar los problemas de los datos en bruto a la entrada en lugar de descubrirlos en un cuadro de mando.

#### ¿Cómo se evita la fatiga de alertas con los tests de dbt?

Usa la severidad `warn` y umbrales para las comprobaciones no críticas, testea lo que importa a los consumidores, elimina los tests que nunca detectan nada relevante y envía los errores a sus responsables.

#### ¿Cómo garantiza dbt la calidad de los datos a lo largo del pipeline?

Con tests en cada capa, frescura de las sources, contratos en los modelos públicos, `dbt build` omitiendo los modelos dependientes cuando un test falla, y CI que ejecuta los modelos modificados y sus tests antes de fusionar.

#### ¿Qué diferencia hay entre `dbt test` y `dbt build` en cuanto a los tests?

`dbt test` ejecuta tests sobre modelos ya construidos. `dbt build` intercala construcción y tests en el orden del DAG, así que un test que falla impide construir sus hijos.

#### ¿Cómo se compara el número de filas de un modelo con el de otro?

Con un test de paquete como `dbt_utils.equal_rowcount` o `dbt_expectations.expect_table_row_count_to_equal_other_table`, o con un test singular que compare los recuentos.

#### ¿Cómo se comprueba que un valor está dentro de un rango?

Con `dbt_utils.accepted_range` (`min_value`, `max_value`) o `dbt_expectations.expect_column_values_to_be_between`.

#### ¿Qué es un test de actualidad (recency)?

Un test como `dbt_utils.recency` que falla cuando la marca de tiempo más reciente de un modelo es más antigua que un umbral, y detecta los modelos que han dejado de recibir datos.

### Modelos incrementales

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

#### ¿Cómo se rellena (backfill) un modelo incremental?

Con `--full-refresh`, o en los modelos microbatch con `--event-time-start` y `--event-time-end` para reprocesar un periodo, o ejecutándolo con una variable que cambie la ventana del filtro.

#### ¿Qué diferencia hay entre un modelo incremental y un snapshot?

Un modelo incremental guarda el último estado (o añade eventos) y su lógica es tuya. Un snapshot guarda el historial completo de los cambios de registros mutables, como filas SCD tipo 2 con fechas de validez.

### Snapshots

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

#### ¿En qué se diferencian los snapshots del time travel de Delta Lake o del almacén?

El time travel del almacén guarda versiones pasadas de la tabla durante un periodo de retención limitado y sirve para recuperar datos. Los snapshots construyen una tabla de historial permanente y consultable a nivel de fila, pensada para el análisis.

#### ¿Qué es una SCD tipo 2 y cómo la implementan los snapshots de dbt?

Una dimensión de cambio lento que guarda una fila nueva por cada versión de un registro, con fechas de validez. Los snapshots de dbt son exactamente eso: una fila por versión, con `dbt_valid_from` y `dbt_valid_to` delimitando su validez.

#### ¿Cómo se construye una dimensión con historial a partir de un snapshot?

Selecciona del snapshot en un modelo, renombra `dbt_valid_from` y `dbt_valid_to` a nombres más claros, añade una clave subrogada por versión y un indicador `is_current`, y une los hechos por la clave natural y la fecha del hecho dentro del rango de validez.

### Documentación, linaje y capa semántica

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

#### ¿Qué es el linaje a nivel de columna?

Un linaje que muestra qué columnas de origen alimentan cada columna, y no solo qué modelos dependen de cuáles. Lo ofrecen la dbt platform y dbt Fusion.

#### ¿Para qué sirven los artefactos de dbt en la observabilidad?

Las herramientas analizan `manifest.json` y `run_results.json` para seguir la duración de las ejecuciones, los fallos de tests y la frescura a lo largo del tiempo, y el paquete `dbt_artifacts` los carga en el almacén para analizarlos.

#### ¿Qué son los campos meta?

Un diccionario libre `meta:` en nodos y columnas, por ejemplo para registrar responsables, marcas de datos personales o acuerdos de nivel de servicio, que pueden leer las herramientas y las macros.

#### ¿Cómo se documenta un test o una macro?

Los tests y las macros pueden tener propiedades `description` en YAML, que aparecen en la documentación generada.

### Despliegue, entornos, CI/CD y orquestación

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

### Rendimiento, almacenes y resolución de problemas

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

#### ¿Cómo se limitan los datos en desarrollo para ahorrar tiempo y dinero?

Filtrando por fecha o con una muestra cuando `target.name == 'dev'`, usando `--defer` para reutilizar los padres de producción, o usando clones sin copia.

#### ¿Qué haces con dependencias entre modelos que forman un ciclo?

dbt rechaza los ciclos. Reestructura la lógica, normalmente extrayendo la parte común a un modelo previo que referencien ambos modelos.

#### ¿Qué pasa cuando un modelo falla a mitad de una ejecución?

Los modelos que dependen de él se omiten, las ramas independientes continúan y la ejecución informa del fallo. Corrígelo y ejecuta `dbt retry`, o vuelve a ejecutar el modelo que falló y sus hijos con `model+`.

#### ¿Cómo se gestionan los cambios de esquema en las sources?

Detectándolos con tests y contratos, usando listas de columnas explícitas en staging en lugar de `select *`, configurando `on_schema_change` en los modelos incrementales y adaptando los modelos de staging en un único sitio.

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
