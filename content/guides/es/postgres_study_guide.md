## Guía de estudio de PostgreSQL

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de PostgreSQL: unas 200 preguntas](../../images/postgres_study_guide_title_img.png)

Unas 200 preguntas sobre PostgreSQL y SQL para entrevistas de ingeniería de datos: arquitectura, tipos de datos, consultas, funciones de ventana, índices, transacciones y MVCC, optimización del rendimiento, modelado de datos, administración y funciones avanzadas como JSONB y el particionado. Los ejemplos usan PostgreSQL 16 y 17. Abre una pregunta para ver su respuesta, o usa el filtro para buscar en toda la guía.

<!-- QA -->

### Fundamentos y arquitectura

#### ¿Qué es PostgreSQL?

Un sistema de bases de datos objeto-relacional de código abierto, conocido por su respeto de los estándares, su fiabilidad y su extensibilidad. Admite transacciones ACID, MVCC, tipos de datos ricos (JSONB, arrays, rangos), SQL avanzado (funciones de ventana, CTE), extensiones y varios tipos de índices.

#### ¿Qué significa ACID?

Las propiedades que deben tener las transacciones de una base de datos, esenciales en los sistemas OLTP, para que los datos sigan siendo válidos pese a errores y fallos:

- **Atomicidad:** una transacción es una unidad que o se completa entera o no tiene ningún efecto.
- **Consistencia:** una transacción lleva la base de datos de un estado válido a otro, respetando las restricciones.
- **Aislamiento:** las transacciones concurrentes no interfieren entre sí: el resultado es como si se hubieran ejecutado en algún orden, según el nivel de aislamiento.
- **Durabilidad:** una vez confirmada, una transacción sobrevive a las caídas (en PostgreSQL, gracias al write-ahead log).

#### ¿Cómo es la arquitectura de procesos de PostgreSQL?

Un proceso postmaster acepta las conexiones y crea un proceso backend por cada conexión de cliente. Varios procesos en segundo plano se encargan de la escritura (background writer, checkpointer), del escritor del WAL, de autovacuum, de las estadísticas y de la replicación. Todos comparten memoria, como `shared_buffers`.

#### ¿Por qué importa el modelo de un proceso por conexión?

Cada conexión cuesta memoria y un proceso, así que miles de conexiones directas perjudican el rendimiento. Las aplicaciones usan un pool de conexiones como PgBouncer o el pool del propio driver.

#### ¿Qué es el write-ahead log (WAL)?

Un registro donde se anota cada cambio antes de modificar los archivos de datos. Tras una caída, PostgreSQL reproduce el WAL para recuperar un estado coherente. El WAL también alimenta la replicación y la recuperación a un momento dado.

#### ¿Qué es un checkpoint?

El momento en que todas las páginas modificadas en memoria se escriben en los archivos de datos, de modo que el WAL anterior deja de ser necesario para la recuperación ante caídas. Su frecuencia la controlan `checkpoint_timeout` y `max_wal_size`.

#### ¿Qué diferencia hay entre una base de datos, un esquema y una tabla?

Un clúster (instancia) contiene bases de datos. Una base de datos contiene esquemas (espacios de nombres como `public`). Un esquema contiene tablas, vistas, funciones y otros objetos. Una conexión se hace a una base de datos y puede consultar varios de sus esquemas.

#### ¿Cómo se crea una base de datos nueva en PostgreSQL?

```sql
CREATE DATABASE my_database OWNER app_owner ENCODING 'UTF8';
```

Desde la terminal, `createdb my_database` hace lo mismo.

#### ¿Cómo se crea una tabla en PostgreSQL?

```sql
CREATE TABLE company (
    company_id   bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    country_code char(2)      NOT NULL,
    business_id  text         NOT NULL,
    name         text,
    created_on   date,
    employees    integer CHECK (employees >= 0),
    UNIQUE (country_code, business_id)
);
```

#### ¿Qué es una clave primaria en Postgres?

Una restricción que identifica de forma única cada fila: sus columnas son `NOT NULL` y únicas, y PostgreSQL crea un índice B-tree único para aplicarla. Una tabla tiene como mucho una clave primaria, que puede abarcar varias columnas.

#### ¿Qué es psql?

El cliente interactivo de línea de comandos de PostgreSQL. Metacomandos útiles: `\l` lista las bases de datos, `\c` se conecta, `\dt` lista las tablas, `\d table` describe una, `\di` lista los índices, `\x` activa la salida expandida y `\timing` muestra la duración de las consultas.

#### ¿Qué es el search path?

La lista ordenada de esquemas en los que PostgreSQL busca los nombres de objetos no cualificados (`SHOW search_path`). Por defecto, `"$user", public`.

#### ¿Qué diferencia hay entre `DELETE`, `TRUNCATE` y `DROP`?

`DELETE` borra las filas una a una, admite una cláusula `WHERE`, dispara triggers y deja tuplas muertas para vacuum. `TRUNCATE` vacía toda la tabla rápidamente sustituyendo sus archivos. `DROP` elimina la propia tabla. En PostgreSQL, los tres son transaccionales.

#### ¿Qué es una secuencia?

Un objeto de la base de datos que genera números crecientes, usado para las claves subrogadas. Las columnas `GENERATED ... AS IDENTITY` (estándar SQL) y los antiguos tipos `serial` usan secuencias. Las secuencias no son transaccionales: las inserciones deshechas dejan huecos.

#### ¿Qué diferencia hay entre `serial` y las columnas identity?

Ambas generan enteros automáticamente a partir de una secuencia. Las columnas identity son SQL estándar, ligan la secuencia a la columna de forma más limpia y, con `GENERATED ALWAYS`, impiden valores manuales accidentales. Son las preferidas para tablas nuevas.

#### ¿Qué es una vista?

Una consulta guardada que se puede consultar como una tabla. No contiene datos y su consulta se ejecuta en cada acceso. Las vistas sencillas pueden ser actualizables.

#### ¿Qué es una vista materializada?

Una vista cuyo resultado se guarda en disco y se refresca explícitamente con `REFRESH MATERIALIZED VIEW`. Con un índice único, `REFRESH ... CONCURRENTLY` la refresca sin bloquear a los lectores.

#### ¿Qué es TOAST?

The Oversized-Attribute Storage Technique: los valores grandes (de más de unos 2 kB) se comprimen y/o se guardan fuera de la fila en una tabla aparte, de forma transparente para las consultas.

#### ¿Qué es un tablespace?

Un directorio del disco donde PostgreSQL puede guardar objetos, lo que permite poner algunas tablas o índices en otro almacenamiento.

#### ¿Qué es el catálogo del sistema?

Las tablas de `pg_catalog` (como `pg_class`, `pg_attribute`, `pg_index`) que describen todos los objetos, más las vistas estándar de `information_schema`.

### Tipos de datos y DDL

#### ¿Qué tipos numéricos ofrece PostgreSQL y cuándo se usa cada uno?

`smallint`, `integer` y `bigint` para números enteros. `numeric(p, s)` para decimales exactos, como importes. `real` y `double precision` para valores de coma flotante aproximados. Evita los float para el dinero.

#### ¿Qué diferencia hay entre `char(n)`, `varchar(n)` y `text`?

`char(n)` rellena con espacios hasta una longitud fija. `varchar(n)` limita la longitud. `text` no tiene límite. En PostgreSQL rinden igual, así que `text` (con una restricción `CHECK` si necesitas un límite) es la opción habitual.

#### ¿Cuáles son los tipos de fecha y hora?

`date`, `time`, `timestamp` (sin zona horaria), `timestamptz` (con zona horaria) e `interval`. `timestamptz` guarda un instante absoluto en UTC y lo convierte al mostrarlo según la `TimeZone` de la sesión.

#### ¿Conviene usar `timestamp` o `timestamptz`?

`timestamptz` para los eventos que ocurrieron en un momento dado: evita ambigüedades entre zonas horarias y cambios de horario. `timestamp` solo para valores de "hora local" no ligados a una zona.

#### ¿Qué es el tipo `boolean`?

`true`, `false` o `NULL`, y acepta como entrada `'t'`, `'yes'`, `'1'`, `'on'` y sus contrarios.

#### ¿Qué es el tipo `uuid` y cómo se generan UUID?

Un tipo de identificador de 128 bits. `gen_random_uuid()` está integrado y genera UUID de versión 4. PostgreSQL 18 añade `uuidv7()` para UUID ordenados en el tiempo, que se indexan mejor.

#### ¿Qué son los arrays en PostgreSQL?

Cualquier tipo puede ser un array: `text[]`, `integer[]`. Se consultan con `ANY`, `@>` (contiene) y `unnest()` para convertirlos en filas, y se indexan con GIN.

#### ¿Qué son los tipos de rango?

Tipos que representan un rango de valores, como `daterange`, `tstzrange` o `int4range`, con operadores de solapamiento (`&&`) y de contención (`@>`). Son útiles para periodos de validez y reservas.

#### ¿Qué es un tipo enum?

Un tipo con una lista fija y ordenada de valores: `CREATE TYPE status AS ENUM ('active', 'closed')`. Añadir valores es fácil, pero quitarlos no, así que las tablas de referencia suelen ser más flexibles.

#### ¿Cuáles son los principales tipos de restricciones?

`NOT NULL`, `UNIQUE`, `PRIMARY KEY`, `FOREIGN KEY`, `CHECK` y `EXCLUDE` (por ejemplo, que no haya dos reservas solapadas de la misma sala).

#### ¿Qué es una clave foránea y qué hacen las opciones `ON DELETE`?

Una restricción que exige que los valores de una columna existan en la clave de una tabla referenciada. `ON DELETE CASCADE` borra las filas hijas con el padre, `SET NULL` vacía la referencia, y `RESTRICT` o `NO ACTION` impiden el borrado.

#### ¿Se indexan automáticamente las columnas de clave foránea?

No. PostgreSQL indexa la clave referenciada (la del padre), pero no la columna que referencia. Indexa las columnas de clave foránea que se usan en joins o que se comprueban al borrar en el padre.

#### ¿Qué es una columna generada?

Una columna calculada a partir de otras: `total numeric GENERATED ALWAYS AS (price * qty) STORED`. PostgreSQL la calcula al escribir.

#### ¿Qué es un dominio?

Un tipo de datos con restricciones, reutilizable en varias tablas: `CREATE DOMAIN postcode_fr AS text CHECK (VALUE ~ '^\d{5}$')`.

#### ¿Cómo se añade una columna a una tabla grande de forma segura?

`ALTER TABLE t ADD COLUMN c type` es instantáneo, incluso con un valor por defecto constante (desde PostgreSQL 11). Los valores por defecto volátiles, los cambios de tipo que reescriben la tabla y añadir `NOT NULL` con una pasada de validación requieren más cuidado y planificación.

#### ¿Cómo se añade una restricción sin bloquear la tabla mucho tiempo?

Añádela como `NOT VALID` (se aplica solo a las filas nuevas) y luego ejecuta `ALTER TABLE ... VALIDATE CONSTRAINT`, que toma un bloqueo más débil mientras comprueba las filas existentes.

#### ¿Qué es una tabla temporal?

Una tabla visible solo para la sesión actual y que se elimina al terminarla (o al confirmar, con `ON COMMIT DROP`). Útil para resultados intermedios.

#### ¿Qué es una tabla unlogged?

Una tabla cuyos cambios no se escriben en el WAL. Las escrituras son mucho más rápidas, pero la tabla se vacía tras una caída y no se replica. Útil para datos de staging que se pueden volver a cargar.

#### ¿Qué significa `NULL` y cómo se comporta en las comparaciones?

Un valor desconocido o ausente. Cualquier comparación con `NULL` devuelve `NULL` (no verdadero), así que hay que usar `IS NULL` / `IS NOT NULL`, e `IS DISTINCT FROM` para comparaciones seguras con nulos.

#### ¿Qué hace `COALESCE`?

Devuelve el primer argumento que no sea nulo: `COALESCE(nickname, first_name, 'unknown')`.

#### ¿Qué es `NULLIF`?

`NULLIF(a, b)` devuelve `NULL` si `a = b`, y `a` en caso contrario. Es útil para evitar divisiones por cero: `x / NULLIF(y, 0)`.

### Consultas: joins, subconsultas y CTE

#### ¿Cuáles son los distintos tipos de join?

`INNER JOIN` (solo las filas que coinciden), `LEFT JOIN` (todas las filas de la izquierda más las coincidencias), `RIGHT JOIN`, `FULL OUTER JOIN` (todas las filas de ambos lados) y `CROSS JOIN` (todas las combinaciones). También existen los self-joins y los joins `LATERAL`.

#### ¿Qué diferencia hay entre `WHERE` y `ON` en un left join?

Una condición en `ON` decide qué filas del lado derecho coinciden, y las filas de la izquierda se conservan igualmente. La misma condición en `WHERE` filtra el resultado del join, lo que puede eliminar filas de la izquierda y convertir en la práctica el left join en un inner join.

#### ¿Qué son un semi-join y un anti-join?

Un semi-join devuelve las filas de A que tienen coincidencia en B (`WHERE EXISTS (...)`) sin duplicar A. Un anti-join devuelve las filas de A sin coincidencia en B (`WHERE NOT EXISTS (...)` o un left join con `IS NULL`).

#### ¿Por qué preferir `NOT EXISTS` a `NOT IN` con una subconsulta?

Si la subconsulta devuelve algún `NULL`, `NOT IN` no devuelve ninguna fila, porque la comparación con `NULL` es desconocida. `NOT EXISTS` se comporta como se espera y se planifica bien como anti-join.

#### ¿Qué es un CTE?

Una Common Table Expression, introducida con `WITH`, da nombre a una subconsulta para mejorar la legibilidad y reutilizarla dentro de una sentencia. Desde PostgreSQL 12, los CTE no recursivos se integran en la consulta cuando es posible. `MATERIALIZED` y `NOT MATERIALIZED` fuerzan la decisión.

#### ¿Qué es un CTE recursivo?

Un CTE que se referencia a sí mismo para recorrer jerarquías o generar series:

```sql
WITH RECURSIVE tree AS (
    SELECT id, parent_id, name, 1 AS depth FROM category WHERE parent_id IS NULL
    UNION ALL
    SELECT c.id, c.parent_id, c.name, t.depth + 1
    FROM category c JOIN tree t ON c.parent_id = t.id
)
SELECT * FROM tree;
```

#### ¿Qué es una subconsulta correlacionada?

Una subconsulta que referencia columnas de la consulta exterior, así que lógicamente se evalúa por cada fila exterior. El planificador a menudo puede convertirla en un join.

#### ¿Qué es un join `LATERAL`?

Un join en el que la subconsulta de la derecha puede referenciar columnas de las tablas de su izquierda. Se usa para el "top N por grupo":

```sql
SELECT c.name, o.*
FROM customer c
CROSS JOIN LATERAL (
    SELECT * FROM orders o WHERE o.customer_id = c.id ORDER BY created_at DESC LIMIT 3
) o;
```

#### ¿Qué diferencia hay entre `UNION` y `UNION ALL`?

`UNION` elimina los duplicados, lo que requiere una ordenación o un hash. `UNION ALL` conserva todas las filas y es más rápido. Usa `UNION ALL` salvo que necesites deduplicar.

#### ¿Qué hacen `INTERSECT` y `EXCEPT`?

`INTERSECT` devuelve las filas presentes en las dos consultas, y `EXCEPT` las de la primera que no están en la segunda, ambas sin duplicados salvo que se use `ALL`.

#### ¿Cuál es el orden lógico de ejecución de un SELECT?

`FROM` y los joins, `WHERE`, `GROUP BY`, `HAVING`, las funciones de ventana, `SELECT`, `DISTINCT`, `ORDER BY` y `LIMIT`/`OFFSET`. Por eso los alias definidos en el `SELECT` no se pueden usar en el `WHERE`.

#### ¿Qué diferencia hay entre `WHERE` y `HAVING`?

`WHERE` filtra las filas antes de agrupar. `HAVING` filtra los grupos después de agregar, así que puede usar resultados de agregados como `HAVING count(*) > 10`.

#### ¿Qué hace `DISTINCT ON`?

Una extensión de PostgreSQL que conserva la primera fila de cada grupo, según el `ORDER BY`:

```sql
SELECT DISTINCT ON (customer_id) customer_id, order_id, created_at
FROM orders
ORDER BY customer_id, created_at DESC;   -- último pedido de cada cliente
```

#### ¿Qué es un upsert en PostgreSQL?

`INSERT ... ON CONFLICT` inserta una fila o, si viola una restricción única, la actualiza (o no hace nada):

```sql
INSERT INTO company (country_code, business_id, name)
VALUES ('FR', '732829320', 'ACME')
ON CONFLICT (country_code, business_id) DO UPDATE SET name = EXCLUDED.name;
```

#### ¿Qué es la sentencia `MERGE`?

Una sentencia SQL estándar (PostgreSQL 15+) que inserta, actualiza o borra filas de un destino según un join con un origen, en una sola sentencia. PostgreSQL 17 añade `RETURNING` y `WHEN NOT MATCHED BY SOURCE`.

#### ¿Qué hace `RETURNING`?

Devuelve columnas de las filas afectadas por `INSERT`, `UPDATE` o `DELETE`, lo que evita una segunda consulta: `INSERT ... RETURNING id`.

#### ¿Cómo se pagina de forma eficiente?

`OFFSET` es cada vez más lento a medida que crece el desplazamiento, porque las filas saltadas se siguen leyendo. La paginación por clave (keyset) es más rápida: `WHERE (created_at, id) < ($1, $2) ORDER BY created_at DESC, id DESC LIMIT 50`, con un índice sobre esas columnas.

#### ¿Cómo se encuentran filas duplicadas?

```sql
SELECT country_code, business_id, count(*)
FROM company
GROUP BY country_code, business_id
HAVING count(*) > 1;
```

#### ¿Cómo se borran los duplicados conservando una fila por clave?

```sql
DELETE FROM company c
USING (
    SELECT ctid, row_number() OVER (PARTITION BY country_code, business_id ORDER BY company_id) AS rn
    FROM company
) d
WHERE c.ctid = d.ctid AND d.rn > 1;
```

#### ¿Qué es `generate_series`?

Una función que devuelve un conjunto de filas con una serie de números o marcas de tiempo, usada para construir calendarios y rellenar huecos: `SELECT generate_series('2026-01-01'::date, '2026-12-31', interval '1 day')`.

### Agregación y funciones de ventana

#### ¿Cuáles son las funciones de agregación más usadas?

`count`, `sum`, `avg`, `min`, `max`, `string_agg`, `array_agg`, `bool_and`, `bool_or`, `json_agg`, y estadísticas como `stddev` y `percentile_cont`.

#### ¿Qué diferencia hay entre `count(*)`, `count(col)` y `count(DISTINCT col)`?

`count(*)` cuenta filas. `count(col)` cuenta los valores no nulos de `col`. `count(DISTINCT col)` cuenta los valores distintos no nulos.

#### ¿Qué hace la cláusula `FILTER`?

Limita las filas que ve un agregado, una alternativa más limpia a poner `CASE` dentro de los agregados:

```sql
SELECT country_code,
       count(*) AS total,
       count(*) FILTER (WHERE status = 'ACTIVE') AS active
FROM company GROUP BY country_code;
```

#### ¿Qué son `GROUPING SETS`, `ROLLUP` y `CUBE`?

Formas de calcular varias agrupaciones en una sola consulta. `ROLLUP (country, city)` produce totales por ciudad, por país y el total general. `CUBE` produce todas las combinaciones. `GROUPING SETS` lista exactamente las agrupaciones que quieres.

#### ¿Qué es una función de ventana?

Una función que se calcula sobre un conjunto de filas relacionadas con la fila actual (su ventana), sin colapsar las filas como `GROUP BY`:

```sql
SELECT country_code, name, revenue,
       rank() OVER (PARTITION BY country_code ORDER BY revenue DESC) AS rank_in_country
FROM company;
```

#### ¿Qué diferencia hay entre `row_number`, `rank` y `dense_rank`?

En los empates: `row_number` da números únicos (1, 2, 3), `rank` da el mismo puesto y luego salta (1, 1, 3), y `dense_rank` da el mismo puesto sin huecos (1, 1, 2).

#### ¿Cómo se obtienen las N primeras filas de cada grupo?

Numerando las filas por grupo y filtrando en una consulta exterior (las funciones de ventana no se pueden usar en el `WHERE`):

```sql
SELECT * FROM (
    SELECT *, row_number() OVER (PARTITION BY country_code ORDER BY employees DESC) AS rn
    FROM company
) t WHERE rn <= 3;
```

#### ¿Qué hacen `lag` y `lead`?

Devuelven un valor de una fila anterior o siguiente dentro de la ventana, por ejemplo para calcular la variación respecto al mes anterior: `revenue - lag(revenue) OVER (ORDER BY month)`.

#### ¿Cómo se calcula un total acumulado?

```sql
SELECT day, amount,
       sum(amount) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM sales;
```

#### ¿Qué es el marco de una ventana y qué diferencia hay entre `ROWS` y `RANGE`?

El subconjunto de la partición que se usa en el cálculo de cada fila. `ROWS` cuenta filas físicas (por ejemplo, las tres filas anteriores). `RANGE` usa distancias de valor en la columna del `ORDER BY`, así que las filas con valores iguales se incluyen juntas. El marco por defecto con `ORDER BY` es `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`.

#### ¿Cómo se calcula un promedio móvil de 7 días?

```sql
SELECT day,
       avg(amount) OVER (ORDER BY day RANGE BETWEEN interval '6 days' PRECEDING AND CURRENT ROW) AS avg_7d
FROM daily_sales;
```

#### ¿Qué hacen `first_value`, `last_value` y `nth_value`?

Devuelven el primer, el último o el enésimo valor del marco. `last_value` suele sorprender porque el marco por defecto termina en la fila actual: especifica `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.

#### ¿Qué hacen `ntile` y `percent_rank`?

`ntile(4)` reparte las filas ordenadas en 4 grupos (cuartiles). `percent_rank()` da a cada fila su posición relativa entre 0 y 1.

#### ¿Cómo se calcula un porcentaje del total con una función de ventana?

```sql
SELECT country_code, count(*) AS n,
       round(100.0 * count(*) / sum(count(*)) OVER (), 1) AS pct
FROM company GROUP BY country_code;
```

#### ¿Cómo se calcula una mediana en PostgreSQL?

Con el agregado de conjunto ordenado `percentile_cont(0.5) WITHIN GROUP (ORDER BY value)`. `percentile_disc` devuelve un valor real del conjunto.

#### ¿Qué es el problema de "huecos e islas" y cómo se resuelve?

Encontrar tramos consecutivos (islas) en una secuencia. Un método clásico resta un `row_number()` al valor ordenado: las filas de una misma isla comparten la diferencia, por la que luego se agrupa.

```sql
SELECT user_id, min(day) AS start_day, max(day) AS end_day
FROM (
    SELECT user_id, day, day - (row_number() OVER (PARTITION BY user_id ORDER BY day))::int AS grp
    FROM logins
) t
GROUP BY user_id, grp;
```

#### ¿Cómo se pasan filas a columnas (pivotar)?

Con agregación condicional:

```sql
SELECT country_code,
       sum(amount) FILTER (WHERE year = 2025) AS y2025,
       sum(amount) FILTER (WHERE year = 2026) AS y2026
FROM revenue GROUP BY country_code;
```

La función `crosstab` de la extensión `tablefunc` es una alternativa.

#### ¿Qué hace `string_agg`?

Concatena valores con un separador, opcionalmente ordenados: `string_agg(name, ', ' ORDER BY name)`.

#### ¿Qué es la cláusula `WINDOW`?

Una forma de dar nombre a una definición de ventana y reutilizarla en varias funciones: `... OVER w ... WINDOW w AS (PARTITION BY country ORDER BY day)`.

#### ¿Cómo se calcula el crecimiento interanual?

```sql
SELECT year, revenue,
       round(100.0 * (revenue - lag(revenue) OVER (ORDER BY year)) / lag(revenue) OVER (ORDER BY year), 1) AS yoy_pct
FROM yearly_revenue;
```

### Índices

#### ¿Qué tipos de índices hay en PostgreSQL y cuándo usar cada uno?

- **B-tree** (por defecto): búsquedas por igualdad y por rango (`=`, `<`, `>`, `BETWEEN`, `ORDER BY`, `LIKE 'abc%'` con prefijo) sobre datos ordenables.
- **Hash:** solo igualdad. Rara vez mejor que un B-tree, pero pequeño para valores largos.
- **GIN** (índice invertido generalizado): valores que contienen varios componentes, como arrays, JSONB y vectores de búsqueda de texto completo, para consultas de "contiene".
- **GiST** (árbol de búsqueda generalizado): datos geométricos, rangos, búsqueda de texto completo y búsquedas del vecino más cercano (con PostGIS, por ejemplo).
- **SP-GiST:** datos particionados en el espacio, como quadtrees, direcciones IP o números de teléfono.
- **BRIN** (índice por rangos de bloques): tablas muy grandes cuyos valores siguen el orden físico, como una columna de marca de tiempo en una tabla de solo inserción. Diminuto y barato de mantener.

#### ¿Cómo funciona un índice B-tree?

Es un árbol equilibrado de claves ordenadas con punteros a las filas de la tabla. Las búsquedas leen unas pocas páginas (tiempo logarítmico), y el orden hace eficientes los recorridos por rango y el `ORDER BY`.

#### ¿Qué es un índice compuesto (de varias columnas) y importa el orden de las columnas?

Un índice sobre varias columnas. El orden importa: un índice sobre `(country_code, created_on)` sirve para filtros sobre `country_code` solo, o sobre ambas, pero no de forma eficiente para `created_on` solo. Pon primero las columnas de igualdad y después la de rango u ordenación.

#### ¿Qué es un índice parcial?

Un índice sobre un subconjunto de filas, definido con una cláusula `WHERE`. Es más pequeño y más rápido cuando las consultas apuntan a ese subconjunto:

```sql
CREATE INDEX ON company (country_code) WHERE status = 'ACTIVE';
```

#### ¿Qué es un índice de expresión?

Un índice sobre el resultado de una expresión, que se usa cuando las consultas filtran por esa misma expresión:

```sql
CREATE INDEX ON customer (lower(email));
SELECT * FROM customer WHERE lower(email) = 'a@b.com';
```

#### ¿Qué es un índice que cubre la consulta y qué hace `INCLUDE`?

Un índice que contiene todas las columnas que necesita una consulta, de modo que puede responder con un index-only scan sin leer la tabla. `INCLUDE (col)` añade columnas que no son clave al índice con ese fin.

#### ¿Qué es un index-only scan y qué necesita?

Un recorrido que responde a una consulta solo con el índice. Necesita un índice que cubra la consulta y páginas marcadas como visibles en el visibility map, que mantiene vacuum.

#### ¿Qué cuestan los índices?

Ocupan espacio en disco y ralentizan `INSERT`, `UPDATE` y `DELETE`, porque hay que mantener cada índice. Los índices no usados son puro costo: encuéntralos con `pg_stat_user_indexes` (`idx_scan = 0`).

#### ¿Por qué PostgreSQL podría no usar un índice?

La consulta devuelve una gran parte de la tabla (un recorrido secuencial es más barato), las estadísticas están desactualizadas, se aplica una función o una conversión de tipo a la columna indexada, el filtro empieza por un comodín (`LIKE '%abc'`), el orden de las columnas no coincide con un índice compuesto, o la tabla es pequeña.

#### ¿Cómo se crea un índice sin bloquear las escrituras?

Con `CREATE INDEX CONCURRENTLY`, que construye el índice sin un bloqueo que impida inserciones y actualizaciones. Tarda más y no se puede ejecutar dentro de un bloque de transacción. Si falla, deja un índice inválido que hay que borrar.

#### ¿Qué es un índice único y cómo se relaciona con una restricción única?

Un índice que rechaza claves duplicadas. Una restricción `UNIQUE` se implementa con un índice único. Por defecto se permiten varios `NULL`, salvo que el índice se declare `NULLS NOT DISTINCT` (PostgreSQL 15+).

#### ¿Cómo se indexa una columna JSONB?

Con un índice GIN sobre toda la columna para las consultas de contención y de existencia de claves (`@>`, `?`), con `jsonb_path_ops` para un índice más pequeño que solo admite `@>`, o con un índice de expresión B-tree sobre una clave extraída:

```sql
CREATE INDEX ON events USING gin (payload jsonb_path_ops);
CREATE INDEX ON events ((payload->>'user_id'));
```

#### ¿Cómo se aceleran las búsquedas `LIKE '%text%'`?

Con un índice de trigramas de la extensión `pg_trgm`: `CREATE INDEX ON company USING gin (name gin_trgm_ops)`. También acelera las búsquedas por similitud.

#### ¿Qué es el bloat de los índices y cómo se corrige?

Los índices acumulan espacio vacío tras muchas actualizaciones y borrados. `REINDEX CONCURRENTLY` los reconstruye en línea. La deduplicación de los B-tree (PostgreSQL 13+) reduce el bloat causado por los duplicados.

#### ¿Cuándo es un índice BRIN la elección correcta?

En tablas muy grandes en las que una columna sigue el orden físico, como una marca de tiempo en un registro de solo inserción. Un índice BRIN guarda el mínimo y el máximo por rango de bloques, así que es diminuto y permite a las consultas saltarse la mayoría de los bloques.

#### ¿Qué diferencia hay entre un índice agrupado (clustered) de otras bases de datos y `CLUSTER` en PostgreSQL?

PostgreSQL no tiene tablas agrupadas de forma permanente. `CLUSTER` reordena físicamente una tabla una vez según un índice, pero las filas nuevas no se mantienen en orden, así que hay que repetirlo.

#### ¿Cómo se detectan los índices que faltan?

Buscando recorridos secuenciales grandes en `pg_stat_user_tables` (`seq_scan`, `seq_tup_read`), consultas lentas en `pg_stat_statements` y recorridos secuenciales con filtros selectivos en los planes de `EXPLAIN`.

#### ¿Un índice sobre `(a, b)` hace redundante un índice sobre `(a)`?

Casi siempre: el índice compuesto sirve para las consultas sobre `a` sola. Un índice aparte sobre `a` puede ser algo más pequeño y rápido, pero no suele compensar su costo de mantenimiento.

#### ¿Qué son el `fastupdate` y las listas pendientes de los índices GIN?

Los índices GIN acumulan las entradas nuevas en una lista pendiente para acelerar las inserciones, y las integran en el índice principal más tarde, con vacuum o cuando la lista se llena. Las listas pendientes grandes pueden ralentizar las búsquedas.

#### ¿Cómo se ve el tamaño de una tabla y de sus índices?

```sql
SELECT pg_size_pretty(pg_total_relation_size('company')) AS total,
       pg_size_pretty(pg_relation_size('company'))       AS table_only,
       pg_size_pretty(pg_indexes_size('company'))        AS indexes;
```

### Transacciones, MVCC y concurrencia

#### ¿Qué es una transacción en PostgreSQL?

Un grupo de sentencias entre `BEGIN` y `COMMIT` (o `ROLLBACK`) que se ejecutan de forma atómica. Cada sentencia fuera de una transacción explícita se ejecuta en su propia transacción (autocommit).

#### ¿Qué es MVCC?

El control de concurrencia multiversión: un `UPDATE` escribe una versión nueva de la fila en lugar de sobrescribirla, y cada transacción ve una instantánea de los datos confirmados. Los lectores no bloquean a los escritores y los escritores no bloquean a los lectores.

#### ¿Qué son las tuplas muertas?

Versiones antiguas de filas que dejan las actualizaciones y los borrados y que ya ninguna transacción puede ver. Ocupan espacio hasta que `VACUUM` lo recupera.

#### ¿Cuáles son los niveles de aislamiento de las transacciones en PostgreSQL?

- **Read Committed** (por defecto): cada sentencia ve los datos confirmados antes de que empezara.
- **Repeatable Read:** toda la transacción ve una única instantánea, tomada en su primera sentencia. Las actualizaciones concurrentes en conflicto provocan errores de serialización.
- **Serializable:** como Repeatable Read, más la detección de anomalías (aislamiento de instantánea serializable), de modo que el resultado equivale a algún orden secuencial. Las aplicaciones deben reintentar cuando hay fallos de serialización.

Read Uncommitted se acepta, pero se comporta como Read Committed.

#### ¿Qué anomalías evitan los niveles de aislamiento?

Las lecturas sucias (imposibles en PostgreSQL), las lecturas no repetibles (evitadas a partir de Repeatable Read), las lecturas fantasma (evitadas también por el Repeatable Read de PostgreSQL) y las anomalías de serialización como el write skew (evitadas solo por Serializable).

#### ¿Qué es un interbloqueo (deadlock) y cómo lo gestiona PostgreSQL?

Dos transacciones esperan cada una un bloqueo que tiene la otra. PostgreSQL lo detecta pasado `deadlock_timeout` y cancela una de las transacciones con un error. Se evitan bloqueando las filas en un orden coherente y manteniendo las transacciones cortas.

#### ¿Qué es `SELECT ... FOR UPDATE`?

Bloquea las filas seleccionadas frente a actualizaciones o borrados concurrentes hasta que termina la transacción, para poder leerlas y luego modificarlas con seguridad. `FOR SHARE` permite que otros lectores también las bloqueen.

#### ¿Qué hace `SKIP LOCKED` y para qué se usa?

Se salta las filas ya bloqueadas por otros en lugar de esperar, lo que facilita construir colas de trabajos:

```sql
SELECT id FROM jobs WHERE status = 'pending'
ORDER BY id LIMIT 10 FOR UPDATE SKIP LOCKED;
```

#### ¿Qué son los bloqueos consultivos (advisory locks)?

Bloqueos definidos por la aplicación sobre números arbitrarios (`pg_advisory_lock(42)`), gestionados por PostgreSQL pero no ligados a filas. Se usan para garantizar que solo un trabajador ejecuta una tarea a la vez.

#### ¿Qué es un savepoint?

Un punto dentro de una transacción al que se puede volver sin abortar toda la transacción: `SAVEPOINT s1; ... ROLLBACK TO SAVEPOINT s1;`.

#### ¿Por qué son dañinas las transacciones de larga duración?

Mantienen una instantánea, así que vacuum no puede eliminar las tuplas muertas más recientes que ella, lo que genera bloat. También pueden mantener bloqueos que impiden el DDL y otras escrituras. Las sesiones "idle in transaction" son un culpable habitual, que se limita con `idle_in_transaction_session_timeout`.

#### ¿Qué es el problema de la actualización perdida y cómo se evita?

Dos transacciones leen un valor, lo modifican, y la segunda escritura sobrescribe la primera. Se evita con una actualización atómica (`SET qty = qty - 1`), con `SELECT ... FOR UPDATE`, con bloqueo optimista mediante una columna de versión, o con Repeatable Read y reintentos.

#### ¿Qué es el bloqueo optimista?

Detectar los conflictos al escribir en lugar de bloquear: cada fila tiene una versión y una actualización solo tiene éxito si la versión no ha cambiado (`UPDATE ... SET ..., version = version + 1 WHERE id = $1 AND version = $2`).

#### ¿Qué bloqueos toma el DDL y por qué un `ALTER TABLE` puede bloquearlo todo?

Muchas formas de `ALTER TABLE` toman un bloqueo `ACCESS EXCLUSIVE`, que entra en conflicto con todos los demás, incluidas las lecturas. Si espera detrás de una consulta larga, todas las consultas nuevas se ponen en cola detrás de él. Usa `lock_timeout` y reintenta.

#### ¿Qué es el desbordamiento (wraparound) de los identificadores de transacción?

Los identificadores de transacción son de 32 bits y dan la vuelta. Vacuum debe "congelar" las filas antiguas antes de que eso ocurra; si no, PostgreSQL deja de aceptar escrituras para proteger los datos. Autovacuum ejecuta automáticamente vacuums anti-wraparound, y vigilar `age(datfrozenxid)` detecta los problemas pronto.

#### ¿Qué hace `VACUUM` y en qué se diferencia de `VACUUM FULL`?

`VACUUM` marca como reutilizable el espacio de las tuplas muertas, actualiza el visibility map y congela las filas antiguas, sin bloquear lecturas ni escrituras. `VACUUM FULL` reescribe la tabla para devolver espacio al sistema operativo, pero toma un bloqueo exclusivo. `pg_repack` hace lo mismo en línea.

#### ¿Qué es autovacuum?

Un proceso en segundo plano que ejecuta `VACUUM` y `ANALYZE` sobre las tablas cuando han cambiado suficientes filas, según umbrales y factores de escala que se pueden ajustar por tabla.

#### ¿Qué hace `ANALYZE`?

Toma muestras de las tablas y actualiza las estadísticas (`pg_statistic`) que usa el planificador para estimar el número de filas y elegir los planes.

#### ¿Qué es una actualización HOT (heap-only tuple)?

Una optimización por la que una actualización que no cambia columnas indexadas, y que cabe en la misma página, crea la versión nueva sin actualizar los índices. Un `fillfactor` más bajo deja sitio para las actualizaciones HOT en tablas con muchas actualizaciones.

#### ¿Qué diferencia hay entre `COMMIT` y `synchronous_commit = off`?

Por defecto, `COMMIT` espera a que el WAL se escriba en disco, lo que garantiza la durabilidad. Con `synchronous_commit = off`, los commits vuelven antes y una caída puede perder las últimas transacciones, sin corromper los datos.

### Rendimiento y planificación de consultas

#### ¿Qué muestra `EXPLAIN` y en qué se diferencia `EXPLAIN ANALYZE`?

`EXPLAIN` muestra el plan elegido por el planificador, con costos y número de filas estimados. `EXPLAIN ANALYZE` ejecuta la consulta y añade los tiempos y el número de filas reales. Añade `BUFFERS` para ver las páginas leídas de la caché o del disco.

```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM company WHERE country_code = 'FR';
```

#### ¿Qué hay que buscar en un plan de ejecución?

Grandes diferencias entre las filas estimadas y las reales (estadísticas malas), recorridos secuenciales sobre tablas grandes con filtros selectivos, bucles anidados sobre muchas filas, ordenaciones o hashes que se vuelcan a disco, y los nodos donde se va la mayor parte del tiempo.

#### ¿Cuáles son los principales tipos de recorrido?

Recorrido secuencial (lee toda la tabla), index scan (sigue el índice y luego lee las filas de la tabla), index-only scan (solo con el índice) y bitmap index/heap scan (reúne las ubicaciones coincidentes de uno o varios índices y luego lee las páginas en orden físico).

#### ¿Cuáles son los tres algoritmos de join?

- **Nested loop:** por cada fila exterior, busca las filas interiores. Bueno cuando un lado es pequeño y el otro está indexado.
- **Hash join:** construye una tabla hash con la entrada más pequeña. Bueno para joins de igualdad grandes y sin ordenar.
- **Merge join:** ambas entradas ordenadas por la clave del join. Bueno para entradas grandes ya ordenadas o indexadas.

#### ¿Qué es `work_mem` y por qué importa?

La memoria que puede usar cada operación de ordenación o de hash antes de volcarse a disco. Si es demasiado baja, las ordenaciones en disco son lentas. Si es demasiado alta, hay riesgo de quedarse sin memoria, porque una sola consulta puede usar varias veces ese valor.

#### ¿Cuáles son los principales parámetros de memoria que se ajustan?

`shared_buffers` (la caché de PostgreSQL, a menudo en torno al 25 % de la RAM), `effective_cache_size` (indicación al planificador de la caché total, a menudo entre el 50 y el 75 % de la RAM), `work_mem` (por operación) y `maintenance_work_mem` (vacuum, creación de índices).

#### ¿Qué es `pg_stat_statements`?

Una extensión que registra las estadísticas de ejecución de cada consulta normalizada: llamadas, tiempo total y medio, filas, aciertos de búfer. Es el primer sitio donde buscar las consultas lentas o frecuentes.

#### ¿Cómo se encuentran las consultas lentas que se están ejecutando?

```sql
SELECT pid, now() - query_start AS duration, state, wait_event_type, query
FROM pg_stat_activity
WHERE state <> 'idle'
ORDER BY duration DESC;
```

#### ¿Cómo se detiene una consulta descontrolada?

`SELECT pg_cancel_backend(pid)` cancela la consulta en curso. `pg_terminate_backend(pid)` cierra toda la conexión. `statement_timeout` evita de entrada las consultas descontroladas.

#### ¿Por qué una función sobre una columna indexada puede impedir el uso del índice?

El índice guarda los valores en bruto de la columna, así que `WHERE date(created_at) = '2026-10-15'` no puede usar un índice sobre `created_at`. Reescríbelo como un rango (`created_at >= '2026-10-15' AND created_at < '2026-10-16'`) o crea un índice de expresión.

#### ¿Qué son las estadísticas extendidas?

`CREATE STATISTICS` permite al planificador conocer las correlaciones entre columnas (dependencias, número de valores distintos, combinaciones de valores más frecuentes), lo que mejora las estimaciones de los filtros sobre varias columnas correlacionadas, como ciudad y código postal.

#### ¿Qué controla `default_statistics_target`?

Cuántos valores de muestra y tramos de histograma guarda `ANALYZE` por columna. Aumentarlo en las columnas con distribuciones sesgadas mejora las estimaciones a costa del tiempo de planificación.

#### ¿Cómo se cargan grandes volúmenes de datos rápidamente?

Usando `COPY` en lugar de inserciones fila a fila, cargando dentro de una sola transacción, creando los índices y las claves foráneas después de la carga, considerando tablas de staging unlogged, aumentando `maintenance_work_mem` para la creación de índices y ejecutando `ANALYZE` después.

#### ¿Qué es el comando `COPY`?

La forma más rápida de cargar o exportar datos en bloque entre tablas y archivos o flujos: `COPY company FROM '/data/company.csv' WITH (FORMAT csv, HEADER)`. Desde un cliente, usa el `\copy` de psql o el soporte de COPY del driver. PostgreSQL 17 puede saltarse las filas mal formadas con `ON_ERROR ignore`.

#### ¿Qué es un pool de conexiones y por qué se usa PgBouncer?

Reutilizar un número pequeño de conexiones a la base de datos para muchos clientes. PgBouncer se sitúa entre las aplicaciones y PostgreSQL, en modo sesión, transacción o sentencia, y reduce el costo de cada conexión.

#### ¿Qué es la consulta paralela?

PostgreSQL puede repartir los recorridos secuenciales, los joins y las agregaciones entre varios procesos trabajadores, según `max_parallel_workers_per_gather` y el tamaño de la tabla.

#### ¿Qué es la compilación JIT en PostgreSQL?

La compilación en tiempo de ejecución (con LLVM) de las expresiones de consultas analíticas largas. Acelera los cálculos pesados, pero añade sobrecosto a las consultas cortas. La controlan `jit` y unos umbrales de costo.

#### ¿Cómo interactúa `LIMIT` con `ORDER BY` y los índices?

Con un índice que coincida con el `ORDER BY`, PostgreSQL solo lee las primeras filas que necesita. Sin él, tiene que ordenarlo todo (con un heapsort de top N) antes de aplicar el límite.

#### ¿Qué es el bloat de las tablas y cómo se detecta?

Espacio desperdiciado por tuplas muertas que vacuum no ha recuperado o que el sistema operativo no ha recibido de vuelta. Se detecta con `pgstattuple`, con consultas de estimación del bloat, o viendo tablas que crecen más deprisa que su número de filas.

#### ¿Qué revisarías primero cuando una consulta se vuelve lenta de repente?

Su plan (`EXPLAIN ANALYZE`) comparado con el de antes, la actualidad de las estadísticas (último analyze), los cambios de volumen de datos, los bloqueos y esperas en `pg_stat_activity`, el bloat, y si los parámetros o un índice nuevo han cambiado el plan.

### Modelado de datos, normalización y OLAP

#### Nombra las tres formas normales principales.

- **Primera forma normal (1FN):** cada columna contiene valores atómicos, sin grupos repetidos ni listas en una columna, y cada fila es única.
- **Segunda forma normal (2FN):** 1FN, y cada columna que no es clave depende de toda la clave primaria, no solo de una parte de una clave compuesta.
- **Tercera forma normal (3FN):** 2FN, y las columnas que no son clave dependen solo de la clave, no de otras columnas que no son clave (sin dependencias transitivas).

#### ¿Qué es la FNBC?

La forma normal de Boyce-Codd, una 3FN más estricta: todo determinante (un conjunto de columnas que determina otra columna) debe ser una clave candidata.

#### ¿Qué es la desnormalización y cuándo está justificada?

Añadir redundancia a propósito (columnas duplicadas, tablas pre-unidas o pre-agregadas) para acelerar las lecturas, en analítica y reporting, donde dominan las consultas y los datos se cargan por lotes controlados.

#### ¿Qué diferencia hay entre OLTP y OLAP?

OLTP (procesamiento de transacciones en línea) gestiona muchas lecturas y escrituras cortas sobre datos actuales, con esquemas normalizados y almacenamiento por filas. OLAP (procesamiento analítico en línea) ejecuta consultas complejas sobre grandes volúmenes de datos históricos, con esquemas desnormalizados (en estrella) y almacenamiento por columnas.

#### ¿Cuáles son las principales operaciones OLAP en un sistema OLAP?

Las operaciones OLAP trabajan sobre un modelo multidimensional en el que los datos se representan como cubos. Hay cinco operaciones analíticas básicas:

- **Drill down (profundizar):** bajar a un nivel más detallado de una jerarquía, por ejemplo año → trimestre → mes.
- **Roll up (agregar):** lo contrario del drill down, agregar a un nivel superior, por ejemplo ciudad → país o mes → trimestre.
- **Slice (cortar):** fijar una dimensión en un único valor para obtener un subcubo con una dimensión menos, por ejemplo solo el T1.
- **Dice (trocear):** filtrar sobre dos o más dimensiones para obtener un subcubo más pequeño, por ejemplo ubicación = Bogotá y producto = café.
- **Pivot (rotar):** girar el cubo para intercambiar las dimensiones de los ejes y ver los datos desde otro ángulo.

#### ¿Qué es un esquema en estrella?

Un modelo dimensional con una tabla de hechos central (medidas y claves foráneas) rodeada de tablas de dimensiones (atributos descriptivos). Es sencillo de consultar y rápido para la analítica.

#### ¿Qué es un esquema en copo de nieve?

Un esquema en estrella cuyas dimensiones están normalizadas en varias tablas relacionadas (producto → categoría → departamento). Ahorra espacio, pero requiere más joins.

#### ¿Qué es la granularidad de una tabla de hechos?

Lo que representa exactamente una fila (una línea de pedido, un saldo diario por cuenta). Declararla primero es el paso más importante del diseño dimensional.

#### ¿Qué tipos de tablas de hechos existen?

Hechos transaccionales (una fila por evento), instantáneas periódicas (una fila por entidad y periodo, como los saldos de fin de mes) e instantáneas acumulativas (una fila por instancia de un proceso, actualizada a medida que avanza por sus hitos).

#### ¿Qué son las dimensiones de cambio lento (SCD)?

Formas de gestionar los cambios en los atributos de las dimensiones. El tipo 1 sobrescribe, así que no se guarda historial. El tipo 2 añade una fila nueva por versión, con fechas de validez y un indicador de vigencia. El tipo 3 guarda el valor anterior en una columna adicional. Los tipos 4 y 6 combinan enfoques.

#### ¿Cómo se implementa una SCD de tipo 2 en PostgreSQL?

Cerrando la versión vigente e insertando la nueva en una sola transacción:

```sql
BEGIN;
UPDATE dim_customer SET valid_to = now(), is_current = false
WHERE customer_id = $1 AND is_current AND row_hash <> $2;
INSERT INTO dim_customer (customer_id, name, city, row_hash, valid_from, valid_to, is_current)
SELECT $1, $3, $4, $2, now(), NULL, true
WHERE NOT EXISTS (SELECT 1 FROM dim_customer WHERE customer_id = $1 AND is_current);
COMMIT;
```

#### ¿Qué es una clave subrogada y por qué usarla en un almacén de datos?

Una clave generada sin significado (identity o hash) en lugar de la clave natural del origen. Aísla el almacén de los cambios de clave del origen, permite varias versiones de un registro (SCD2) y hace eficientes los joins.

#### ¿Qué es una clave natural?

Una clave que tiene significado en el negocio o en el sistema de origen, como un SIRET o una dirección de correo. Debe conservarse como atributo aunque se use una clave subrogada.

#### ¿Qué es una dimensión basura (junk dimension)?

Una dimensión que agrupa varios indicadores y marcas de baja cardinalidad (tipo de pago, is_promo) en una tabla, en lugar de llenar con ellos la tabla de hechos.

#### ¿Qué es una dimensión degenerada?

Una clave de dimensión guardada en la tabla de hechos sin tabla de dimensión propia, como un número de factura.

#### ¿Qué es una dimensión conformada?

Una dimensión compartida, con el mismo significado y las mismas claves, entre varias tablas de hechos o data marts (fecha, cliente), para poder combinar los resultados.

#### ¿Qué es una dimensión de fecha y por qué construirla?

Una tabla con una fila por día y atributos (día de la semana, mes, trimestre, festivos, periodos fiscales). Hace que los filtros y agrupaciones de calendario sean sencillos y coherentes:

```sql
SELECT d::date AS day, extract(isodow FROM d) AS weekday, extract(quarter FROM d) AS quarter
FROM generate_series('2020-01-01'::date, '2030-12-31', interval '1 day') AS d;
```

#### ¿Qué es el modelado Data Vault?

Un método de modelado para integrar muchas fuentes con el historial completo: hubs (claves de negocio), links (relaciones) y satélites (atributos descriptivos con fechas de carga). Favorece la auditabilidad y la carga en paralelo, y suele alimentar esquemas en estrella para el reporting.

#### ¿Cuándo no usarías PostgreSQL para analítica?

Cuando los datos llegan a muchos terabytes o las consultas recorren habitualmente volúmenes enormes: los almacenes en columnas o los lakehouses (Redshift, BigQuery, Snowflake, Databricks) escalan mejor. Extensiones como Citus o el almacenamiento en columnas, o DuckDB para el análisis local, pueden ampliar antes el alcance de PostgreSQL.

#### ¿Qué es la arquitectura medallion y qué papel tiene en ella una base de datos relacional?

Una organización en capas de un lakehouse: bronze (en bruto), silver (limpio y conformado) y gold (agregados y modelos de negocio). Una base de datos relacional como PostgreSQL suele ser un sistema de origen, o una capa de servicio para los datos gold que usan las aplicaciones.

### Administración, seguridad, copias de seguridad y replicación

#### ¿Qué son los roles en PostgreSQL?

Los roles son a la vez usuarios y grupos: un rol con `LOGIN` es un usuario, y los roles se pueden conceder a otros roles para que hereden sus privilegios.

#### ¿Cómo se concede acceso de solo lectura a un esquema?

```sql
CREATE ROLE reporting NOLOGIN;
GRANT USAGE ON SCHEMA analytics TO reporting;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO reporting;
ALTER DEFAULT PRIVILEGES IN SCHEMA analytics GRANT SELECT ON TABLES TO reporting;
GRANT reporting TO alice;
```

PostgreSQL 14+ tiene también el rol predefinido `pg_read_all_data`.

#### ¿Qué es la seguridad a nivel de fila (RLS)?

Políticas que restringen qué filas puede ver o modificar cada rol:

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders USING (tenant_id = current_setting('app.tenant_id')::int);
```

#### ¿Qué es `pg_hba.conf`?

El archivo de autenticación basada en host: reglas que indican qué usuarios pueden conectarse a qué bases de datos, desde qué direcciones y con qué método (`scram-sha-256`, `cert`, `peer`). `trust` no debe usarse nunca fuera de pruebas locales.

#### ¿Cómo deben guardarse y comprobarse las contraseñas?

Con `scram-sha-256` (el valor por defecto desde PostgreSQL 14) en lugar de md5, conexiones cifradas con TLS y credenciales de las aplicaciones guardadas en un gestor de secretos.

#### ¿Cómo se evita la inyección SQL?

Usando consultas parametrizadas (marcadores que vincula el driver) en lugar de concatenar cadenas. En el SQL dinámico dentro de funciones, usa `format()` con `%I` para los identificadores y `%L` para los literales, o `EXECUTE ... USING`.

#### ¿Qué diferencia hay entre las copias de seguridad lógicas y físicas?

Las copias lógicas (`pg_dump`, `pg_dumpall`) exportan archivos SQL o de archivo con los objetos y los datos. Son portables entre versiones y se pueden restaurar de forma selectiva, pero son lentas en bases de datos grandes. Las copias físicas (`pg_basebackup`, pgBackRest) copian los archivos de datos y el WAL. Son rápidas en bases grandes y permiten la recuperación a un momento dado.

#### ¿Cómo se hace y se restaura una copia de una sola base de datos con pg_dump?

```bash
pg_dump -Fc -d mydb -f mydb.dump          # formato custom, comprimido
pg_restore -d newdb -j 4 mydb.dump        # restauración en paralelo
```

#### ¿Qué es la recuperación a un momento dado (PITR)?

Restaurar una copia base y reproducir el WAL archivado hasta un instante elegido, por ejemplo justo antes de un `DELETE` accidental.

#### ¿Qué es la replicación en streaming?

Un servidor en espera recibe y reproduce continuamente el WAL del primario, manteniendo una copia idéntica byte a byte. Puede atender consultas de solo lectura (hot standby) y promocionarse si el primario falla.

#### ¿Qué diferencia hay entre la replicación síncrona y la asíncrona?

Con la replicación asíncrona, los commits no esperan a las réplicas, así que una conmutación puede perder las últimas transacciones. Con la síncrona, los commits esperan la confirmación de una o varias réplicas, así que no se pierden datos, a costa de la latencia de los commits.

#### ¿Qué es la replicación lógica?

La replicación de los cambios de filas por tabla mediante publicaciones y suscripciones. Funciona entre versiones mayores y permite replicar un subconjunto de tablas, lo que es útil para actualizaciones, consolidaciones y captura de cambios.

#### ¿Qué es la captura de datos de cambios (CDC) con PostgreSQL?

Transmitir en streaming los cambios a nivel de fila desde el WAL mediante la decodificación lógica, a menudo con Debezium y Kafka, para que los sistemas de destino (data lakes, índices de búsqueda) reciban inserciones, actualizaciones y borrados casi en tiempo real.

#### ¿Qué es un slot de replicación y qué riesgo tiene?

Un slot hace que el primario conserve el WAL hasta que lo recibe un consumidor. Si el consumidor se detiene, el WAL se acumula y puede llenar el disco, así que hay que vigilar `pg_replication_slots`.

#### ¿Cómo se actualiza PostgreSQL a una nueva versión mayor?

Con `pg_upgrade` (rápido, en el sitio, con `--link` o `--clone`), con un volcado y una restauración (sencillo pero lento), o con replicación lógica hacia un clúster nuevo para un tiempo de inactividad casi nulo.

#### ¿Con qué se suele construir la alta disponibilidad de PostgreSQL?

Con replicación en streaming más un gestor de conmutación como Patroni (con etcd o Consul), o con un servicio gestionado (Amazon RDS o Aurora, Cloud SQL, Azure Database for PostgreSQL) que se encarga de la conmutación.

#### ¿Qué hay que monitorizar en un servidor PostgreSQL?

Las conexiones, la tasa de transacciones, la tasa de aciertos de caché, las consultas lentas (`pg_stat_statements`), los bloqueos y las esperas, el retraso de replicación, la actividad de autovacuum y el bloat, la edad de los identificadores de transacción, el espacio en disco y el crecimiento del WAL, los checkpoints y la E/S.

#### ¿Qué es la tasa de aciertos de caché y cómo se calcula?

La proporción de lecturas de bloques servidas desde `shared_buffers`. En cargas OLTP suele tener que estar por encima del 99 %:

```sql
SELECT round(100.0 * sum(blks_hit) / nullif(sum(blks_hit) + sum(blks_read), 0), 2)
FROM pg_stat_database;
```

#### ¿Qué es `statement_timeout` y dónde conviene fijarlo?

El tiempo máximo que puede durar una sentencia antes de cancelarse. Fíjalo por rol o por aplicación (por ejemplo 30 segundos para una aplicación web) para proteger el servidor de las consultas descontroladas.

#### ¿Qué gestiona Amazon RDS for PostgreSQL por ti?

El aprovisionamiento, las copias de seguridad automáticas y la PITR, los parches de versiones menores, la conmutación Multi-AZ, las réplicas de lectura, la monitorización y el crecimiento del almacenamiento. Tú sigues siendo responsable del esquema, las consultas, los usuarios, los parámetros y el acceso de red, y no tienes acceso de superusuario ni al sistema operativo.

### Funciones avanzadas

#### ¿Qué diferencia hay entre `json` y `jsonb`?

`json` guarda el texto de entrada exacto y lo analiza en cada acceso. `jsonb` guarda una forma binaria descompuesta, elimina los espacios y las claves duplicadas, es más rápido de consultar y se puede indexar. `jsonb` es la opción habitual.

#### ¿Cuáles son los principales operadores de JSONB?

`->` devuelve un valor JSON, `->>` devuelve texto, `#>` y `#>>` siguen una ruta, `@>` comprueba la contención, `?` comprueba la existencia de una clave, `||` concatena y `-` elimina una clave.

```sql
SELECT payload->>'user_id' AS user_id
FROM events
WHERE payload @> '{"type": "click"}';
```

#### ¿Qué es SQL/JSON path en PostgreSQL?

Un lenguaje de consulta para JSON (`jsonb_path_query`, `@?`, `@@`). PostgreSQL 17 añade las funciones estándar `JSON_TABLE`, `JSON_VALUE` y `JSON_QUERY` para convertir JSON en filas relacionales.

#### ¿Cómo se convierte un array JSON en filas?

```sql
SELECT e.id, item->>'sku' AS sku, (item->>'qty')::int AS qty
FROM orders e, jsonb_array_elements(e.payload->'items') AS item;
```

#### ¿Cuándo conviene guardar datos como JSONB en lugar de en columnas?

Para atributos semiestructurados o dispersos que varían entre filas, o para cargas útiles en bruto que se guardan como referencia. Las columnas son mejores para los campos por los que filtras, unes o agregas a menudo, porque tienen tipos, restricciones y estadísticas propios.

#### ¿Qué es la búsqueda de texto completo en PostgreSQL?

Buscar en documentos con `tsvector` (lexemas normalizados) y `tsquery`, con stemming según el idioma, ordenación por relevancia (`ts_rank`) e índices GIN:

```sql
SELECT * FROM article
WHERE to_tsvector('english', body) @@ websearch_to_tsquery('english', 'data pipeline');
```

#### ¿Qué es una función PL/pgSQL?

Una función escrita en el lenguaje procedimental de PostgreSQL, con variables, bucles, condiciones y gestión de excepciones, que se ejecuta dentro del servidor.

#### ¿Qué diferencia hay entre una función y un procedimiento?

Las funciones devuelven un valor, se llaman dentro de consultas y se ejecutan en la transacción de quien las llama. Los procedimientos (PostgreSQL 11+) se invocan con `CALL`, no devuelven nada (o parámetros de salida) y pueden hacer `COMMIT` y `ROLLBACK` dentro, lo que encaja con los trabajos de mantenimiento por lotes.

#### ¿Qué son las categorías de volatilidad de las funciones?

`IMMUTABLE` (mismo resultado para los mismos argumentos siempre, necesario para los índices de expresión), `STABLE` (constante dentro de una sentencia) y `VOLATILE` (puede cambiar en cada llamada, el valor por defecto). Marcarlas bien permite optimizar al planificador.

#### ¿Qué es un trigger?

Una función que se ejecuta automáticamente antes o después de un `INSERT`, `UPDATE`, `DELETE` o `TRUNCATE`, por fila o por sentencia. Se usa para registros de auditoría, para mantener columnas derivadas o para imponer reglas complejas. Los triggers esconden lógica, así que úsalos con moderación.

#### ¿Cómo se mantiene al día una columna `updated_at` con un trigger?

```sql
CREATE FUNCTION touch_updated_at() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at := now();
    RETURN NEW;
END $$;

CREATE TRIGGER company_touch BEFORE UPDATE ON company
FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
```

#### ¿Qué son las extensiones? Nombra algunas útiles.

Paquetes que añaden funciones con `CREATE EXTENSION`: `pg_stat_statements` (estadísticas de consultas), `pg_trgm` (similitud e índices de trigramas), `postgis` (geoespacial), `pgcrypto`, `uuid-ossp`, `postgres_fdw`, `pg_partman` (gestión de particiones), `pgvector` (búsqueda por similitud de vectores), `timescaledb` (series temporales), `citus` (distribución).

#### ¿Qué es el particionado de tablas?

Dividir una tabla grande en particiones por `RANGE`, `LIST` o `HASH` de una clave, detrás de una tabla padre. Las consultas que filtran por la clave solo leen las particiones relevantes (poda de particiones), y los datos antiguos se pueden eliminar al instante separando o borrando una partición.

```sql
CREATE TABLE events (id bigint, created_at timestamptz NOT NULL, payload jsonb)
PARTITION BY RANGE (created_at);
CREATE TABLE events_2026_10 PARTITION OF events
FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
```

#### ¿Cuándo compensa particionar?

En tablas muy grandes con una clave natural para la poda (normalmente el tiempo) y un ciclo de vida que elimina o archiva los datos antiguos. Añade complejidad: las claves primarias deben incluir la clave de partición, y demasiadas particiones ralentizan la planificación.

#### ¿Qué es PostGIS?

La extensión espacial de PostgreSQL: tipos geometry y geography, funciones espaciales (distancia, intersección, áreas de influencia), índices GiST y transformaciones de sistemas de coordenadas. Es la base de datos espacial de código abierto de referencia.

#### ¿Qué es un foreign data wrapper (FDW)?

Una extensión que permite a PostgreSQL consultar fuentes de datos externas como si fueran tablas locales: `postgres_fdw` (otros servidores PostgreSQL), `file_fdw` (archivos) y otras para MySQL, Oracle, S3 o Parquet.

#### ¿Qué es pgvector?

Una extensión que añade un tipo `vector` y la búsqueda por similitud (coseno, L2, producto escalar) con índices HNSW e IVFFlat. Se usa para guardar embeddings para la búsqueda semántica y la generación aumentada por recuperación.

#### ¿Qué hace `LISTEN` / `NOTIFY`?

Un mecanismo integrado de publicación/suscripción: una sesión envía `NOTIFY channel, 'payload'` y todas las sesiones que han ejecutado `LISTEN channel` lo reciben tras el commit. Es útil para invalidar cachés de forma ligera o despertar trabajos.

#### ¿Cuáles son las funciones de fecha más habituales?

`now()` y `current_date`, `date_trunc('month', ts)`, `extract(year FROM ts)`, `age(a, b)`, la aritmética de intervalos (`ts + interval '7 days'`), `to_char(ts, 'YYYY-MM')` y `make_date(y, m, d)`.

#### ¿Cómo se generan datos de prueba rápidamente en PostgreSQL?

Con `generate_series` y funciones aleatorias:

```sql
INSERT INTO company (country_code, business_id, name, employees)
SELECT (ARRAY['FR','GB','IE','NO'])[1 + floor(random() * 4)::int],
       lpad(i::text, 9, '0'),
       'Company ' || i,
       floor(random() * 500)::int
FROM generate_series(1, 1000000) AS i;
```
