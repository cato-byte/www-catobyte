## Guía de estudio de PostgreSQL

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de PostgreSQL: unas 200 preguntas](../../images/postgres_study_guide_title_img.png)

Unas 200 preguntas sobre PostgreSQL y SQL para entrevistas de ingeniería de datos: arquitectura, tipos de datos, consultas, funciones de ventana, índices, transacciones y MVCC, optimización del rendimiento, modelado de datos, administración y funciones avanzadas como JSONB y el particionado. Los ejemplos usan PostgreSQL 16 y 17.

La guía sigue una ruta de aprendizaje en cuatro etapas. Cada sección se divide en unidades cortas: objetivos de aprendizaje, una explicación del concepto y un ejemplo resuelto, luego preguntas (primero de memoria, después de aplicación), un reto práctico e ideas clave. Para **aprender**, lee cada unidad de principio a fin. Para **repasar**, cambia al modo repaso o usa "Ir a las preguntas", marca las respuestas que quieras volver a ver y prueba un repaso mixto entre secciones.

<!-- QA -->
<!-- stage: Fundamentos -->

### Fundamentos y arquitectura

<!-- unit: Arquitectura de PostgreSQL -->

<!-- goals -->

- Describir el modelo de procesos, el WAL y los checkpoints de PostgreSQL.
- Explicar ACID y por qué las conexiones son costosas.

<!-- concept -->

El diseño de PostgreSQL explica buena parte de su comportamiento. Cada conexión de cliente recibe su propio proceso del sistema operativo, lo que es robusto pero cuesta memoria, así que miles de conexiones directas hacen daño y el pooling se vuelve necesario.
La durabilidad viene del write-ahead log: cada cambio se escribe primero en el log y después en los archivos de datos. Tras una caída, reproducir el log restaura el trabajo confirmado. Los checkpoints vuelcan periódicamente las páginas cambiadas para que el log necesario en la recuperación sea corto. Juntos dan las garantías ACID.

<!-- example -->

```text
client ──► postmaster ──fork──► backend process (one per connection)
UPDATE ──► WAL record (fsync on COMMIT) ──► shared_buffers page (dirty)
checkpoint ──► dirty pages flushed to data files ──► old WAL recyclable
```

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

<!-- challenge -->

Un servidor pierde la energía a mitad de una transacción. Al reiniciar, ¿están las transacciones confirmadas y desaparecieron las no confirmadas? ¿Por qué?

<!-- solution -->

Sí. Las transacciones confirmadas tenían su WAL volcado a disco antes de que `COMMIT` respondiera, así que la recuperación las reproduce; los cambios sin confirmar no tienen registro de commit y se descartan.

<!-- takeaways -->

- Un proceso por conexión: usa pooling.
- WAL primero y archivos de datos después garantizan la durabilidad.
- Los checkpoints acotan el tiempo de recuperación.

<!-- unit: Bases de datos, esquemas y tablas -->

<!-- goals -->

- Navegar clústeres, bases, esquemas y tablas con psql.
- Crear bases y tablas con llaves primarias y entender el search path.

<!-- concept -->

PostgreSQL organiza los objetos en capas. Una instancia de servidor contiene bases de datos, aisladas entre sí; cada base contiene esquemas, espacios de nombres para tablas y otros objetos. Los nombres sin calificar se resuelven con el search path, lo que explica muchas sorpresas de "tabla no encontrada".
Todo sobre esos objetos, incluidas tablas, columnas, índices y permisos, se guarda a su vez en tablas del catálogo del sistema que puedes consultar. psql es la herramienta diaria para explorarlo todo.

<!-- example -->

```sql
CREATE DATABASE shop OWNER app_owner ENCODING 'UTF8';
\c shop
CREATE SCHEMA sales;
CREATE TABLE sales.company (
  company_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  country_code char(2) NOT NULL,
  business_id text NOT NULL,
  UNIQUE (country_code, business_id)
);
\dt sales.*
```

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

<!-- challenge -->

`SELECT * FROM orders` falla con "relation does not exist", pero la tabla se ve en una herramienta gráfica. ¿Qué revisas?

<!-- solution -->

El esquema y el search path: la tabla probablemente vive en otro esquema (por ejemplo `sales.orders`) que no está en `search_path`, o en otra base. Califica el nombre o ajusta el search path.

<!-- takeaways -->

- Las instancias contienen bases; las bases, esquemas.
- El search path resuelve los nombres sin calificar.
- El catálogo del sistema describe cada objeto.

<!-- unit: Objetos más allá de las tablas -->

<!-- goals -->

- Usar secuencias, columnas identity, vistas y vistas materializadas.
- Elegir entre DELETE, TRUNCATE y DROP.

<!-- concept -->

Las tablas están rodeadas de objetos auxiliares. Las secuencias generan números para llaves, y las columnas identity son la forma moderna y estándar de asociarlas. Las vistas guardan consultas, recalculadas en cada lectura; las vistas materializadas guardan resultados, refrescados cuando tú lo indicas.
Quitar datos tiene tres herramientas con efectos muy distintos: borrar filas una a una, truncar toda la tabla al instante o eliminar la tabla por completo.

<!-- example -->

| Operación | Quita | Velocidad | ¿WHERE? | Deja tuplas muertas |
|---|---|---|---|---|
| `DELETE` | Filas seleccionadas | Fila por fila | Sí | Sí |
| `TRUNCATE` | Todas las filas | Instantánea | No | No |
| `DROP TABLE` | La tabla misma | Instantánea | No | n/a |

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

<!-- challenge -->

Un job nocturno vacía una tabla de staging de 50 millones de filas con `DELETE FROM staging`, y la tabla sigue creciendo en disco. ¿Qué cambias?

<!-- solution -->

Usa `TRUNCATE staging`, que quita todas las filas al instante sin dejar tuplas muertas. `DELETE` marca las filas como muertas y depende de vacuum para recuperar el espacio.

<!-- takeaways -->

- Las columnas identity son la forma estándar de generar llaves.
- Las vistas recalculan; las materializadas guardan resultados.
- TRUNCATE vacía tablas sin tuplas muertas.

<!-- unit: Almacenamiento físico -->

<!-- goals -->

- Explicar cómo guarda PostgreSQL valores grandes con TOAST.
- Usar tablespaces para poner datos en discos distintos.

<!-- concept -->

Las filas viven en páginas de tamaño fijo, así que los valores muy grandes necesitan un manejo especial. TOAST los comprime y, si siguen siendo grandes, los mueve a una tabla aparte, manteniendo la tabla principal compacta y rápida de escanear cuando no se leen esas columnas.
Los tablespaces asocian objetos a directorios en disco y permiten poner ciertas tablas o índices en almacenamiento más rápido o más grande. En servicios administrados casi no hacen falta.

<!-- example -->

```sql
SELECT pg_size_pretty(pg_relation_size('documents'))        AS main,
       pg_size_pretty(pg_total_relation_size('documents'))  AS total;   -- includes TOAST and indexes
CREATE TABLESPACE fast_ssd LOCATION '/mnt/nvme/pg';
ALTER INDEX orders_created_idx SET TABLESPACE fast_ssd;
```

#### ¿Qué es un tablespace?

Un directorio del disco donde PostgreSQL puede guardar objetos, lo que permite poner algunas tablas o índices en otro almacenamiento.

#### ¿Qué es el catálogo del sistema?

Las tablas de `pg_catalog` (como `pg_class`, `pg_attribute`, `pg_index`) que describen todos los objetos, más las vistas estándar de `information_schema`.

<!-- challenge -->

Una tabla `documents` es pequeña en disco, pero `pg_total_relation_size` muestra 400 GB. ¿Dónde está el espacio y frena las consultas que no leen el contenido?

<!-- solution -->

Sobre todo en la tabla TOAST que guarda los valores grandes de `content`. Las consultas que no seleccionan esa columna no leen TOAST, así que siguen siendo rápidas.

<!-- takeaways -->

- TOAST comprime y saca de línea los valores grandes.
- Las consultas que no leen esas columnas se saltan TOAST.
- Los tablespaces ubican objetos en el almacenamiento elegido.

### Tipos de datos y DDL

<!-- unit: Elegir tipos de datos -->

<!-- goals -->

- Elegir bien tipos numéricos, de texto, fecha y hora.
- Decidir entre timestamp y timestamptz, y generar UUIDs.

<!-- concept -->

Los tipos son reglas: deciden qué valores son válidos, cómo se comparan y cuánto espacio ocupan. Decimales exactos para dinero, enteros para conteos y llaves, texto sin límites arbitrarios. El tiempo es la trampa clásica: `timestamptz` registra un instante, mientras que `timestamp` registra una lectura de reloj sin zona, que se vuelve ambigua en cuanto los sistemas cruzan zonas horarias.
Los UUIDs sirven cuando las llaves deben generarse fuera de la base.

<!-- example -->

```sql
CREATE TABLE payment (
  payment_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  amount numeric(12,2) NOT NULL,          -- exact money
  currency char(3) NOT NULL,
  paid_at timestamptz NOT NULL,           -- an instant
  is_refund boolean NOT NULL DEFAULT false,
  note text
);
```

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

<!-- challenge -->

Los totales de montos en `double precision` salen con un centavo de diferencia en los reportes de finanzas. ¿Qué tipo deberían usar y por qué?

<!-- solution -->

`numeric(p, s)`, que guarda decimales exactos. Los tipos de punto flotante aproximan los valores en binario, así que las sumas de muchos montos acumulan errores de redondeo.

<!-- takeaways -->

- `numeric` para dinero; enteros para llaves y conteos.
- `timestamptz` para instantes.
- `text` está bien; limita la longitud solo cuando sea una regla.

<!-- unit: Tipos enriquecidos -->

<!-- goals -->

- Usar arrays, rangos, enums y dominios.
- Calcular valores con columnas generadas.

<!-- concept -->

Los tipos de PostgreSQL van más allá de lo básico de SQL. Los arrays guardan listas en una columna; los rangos representan intervalos y pueden impedir solapamientos; los enums fijan un conjunto de valores; los dominios atan restricciones a un tipo reutilizable. Las columnas generadas calculan valores a partir de otras columnas automáticamente.
Cada uno ahorra código en otro lado, pero cada uno también sacrifica flexibilidad: los enums son difíciles de achicar, y los arrays no reemplazan tablas relacionadas cuando los elementos necesitan atributos propios.

<!-- example -->

```sql
CREATE DOMAIN email AS text CHECK (VALUE ~* '^[^@\s]+@[^@\s]+$');
CREATE TABLE booking (
  room_id int,
  during tstzrange NOT NULL,
  tags text[] DEFAULT '{}',
  guest_email email,
  nights int GENERATED ALWAYS AS (upper(during)::date - lower(during)::date) STORED,
  EXCLUDE USING gist (room_id WITH =, during WITH &&)   -- no double bookings (btree_gist)
);
```

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

<!-- challenge -->

Las categorías de producto se guardan como enum, y el negocio renombra y elimina categorías cada trimestre. ¿Es buena elección un enum?

<!-- solution -->

No. Los valores de un enum son fáciles de agregar pero incómodos de renombrar, reordenar o quitar. Usa una tabla de referencia con llave foránea, que admite cambios, descripciones e historia.

<!-- takeaways -->

- Arrays, rangos, enums y dominios codifican reglas en tipos.
- Los exclusion constraints sobre rangos impiden solapamientos.
- Usa tablas de referencia para valores que cambian.

<!-- unit: Restricciones y llaves -->

<!-- goals -->

- Usar los principales tipos de restricciones, incluidas las llaves foráneas.
- Elegir el comportamiento ON DELETE e indexar las llaves foráneas.

<!-- concept -->

Las restricciones permiten que la base rechace datos malos en vez de confiar en que cada aplicación los revise. Llaves y unicidad evitan duplicados, los checks imponen reglas, las exclusiones impiden solapamientos y las llaves foráneas garantizan que las referencias existan.
Las llaves foráneas necesitan dos decisiones: qué pasa con los hijos al borrar un padre y un índice sobre la columna que referencia, que PostgreSQL no crea por ti. Sin él, los borrados en el padre escanean la tabla hija.

<!-- example -->

```sql
CREATE TABLE order_line (
  order_id bigint NOT NULL REFERENCES orders (order_id) ON DELETE CASCADE,
  line_no int NOT NULL,
  qty int NOT NULL CHECK (qty > 0),
  PRIMARY KEY (order_id, line_no)
);
CREATE INDEX ON order_line (order_id);   -- often covered by the PK; needed if it doesn't lead
```

#### ¿Se indexan automáticamente las columnas de clave foránea?

No. PostgreSQL indexa la clave referenciada (la del padre), pero no la columna que referencia. Indexa las columnas de clave foránea que se usan en joins o que se comprueban al borrar en el padre.

#### ¿Qué es una columna generada?

Una columna calculada a partir de otras: `total numeric GENERATED ALWAYS AS (price * qty) STORED`. PostgreSQL la calcula al escribir.

#### ¿Qué es un dominio?

Un tipo de datos con restricciones, reutilizable en varias tablas: `CREATE DOMAIN postcode_fr AS text CHECK (VALUE ~ '^\d{5}$')`.

<!-- challenge -->

Borrar un cliente tarda 30 segundos. La tabla `orders` referencia a customers con una llave foránea. ¿Cuál es la causa probable?

<!-- solution -->

`orders.customer_id` no está indexada, así que cada borrado escanea toda la tabla de órdenes buscando referencias. Crea un índice sobre la columna de la llave foránea.

<!-- takeaways -->

- Las restricciones imponen reglas en la base.
- Elige el comportamiento ON DELETE a propósito.
- Indexa tú mismo las columnas de llaves foráneas.

<!-- unit: Cambiar tablas con seguridad -->

<!-- goals -->

- Agregar columnas y restricciones a tablas grandes sin bloqueos largos.
- Usar bien tablas temporales y unlogged.

<!-- concept -->

En una tabla con mucho uso, cómo cambias el esquema importa tanto como qué cambias. Algunos cambios son instantáneos; otros reescriben la tabla o la escanean con un bloqueo que frena a todos. Agregar una columna con un default constante hoy es instantáneo, y las restricciones se pueden agregar sin validar y luego validarse sin bloquear las escrituras.
Las tablas temporales y unlogged cambian durabilidad por velocidad, lo que sirve para datos de trabajo y de staging.

<!-- example -->

```sql
ALTER TABLE orders ADD COLUMN channel text DEFAULT 'web';          -- instant
ALTER TABLE orders ADD CONSTRAINT orders_amount_pos CHECK (amount >= 0) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT orders_amount_pos;          -- scans without blocking writes
CREATE UNLOGGED TABLE staging_orders (LIKE orders);                -- fast, not crash-safe
```

#### ¿Cómo se añade una columna a una tabla grande de forma segura?

`ALTER TABLE t ADD COLUMN c type` es instantáneo, incluso con un valor por defecto constante (desde PostgreSQL 11). Los valores por defecto volátiles, los cambios de tipo que reescriben la tabla y añadir `NOT NULL` con una pasada de validación requieren más cuidado y planificación.

#### ¿Cómo se añade una restricción sin bloquear la tabla mucho tiempo?

Añádela como `NOT VALID` (se aplica solo a las filas nuevas) y luego ejecuta `ALTER TABLE ... VALIDATE CONSTRAINT`, que toma un bloqueo más débil mientras comprueba las filas existentes.

#### ¿Qué es una tabla temporal?

Una tabla visible solo para la sesión actual y que se elimina al terminarla (o al confirmar, con `ON COMMIT DROP`). Útil para resultados intermedios.

#### ¿Qué es una tabla unlogged?

Una tabla cuyos cambios no se escriben en el WAL. Las escrituras son mucho más rápidas, pero la tabla se vacía tras una caída y no se replica. Útil para datos de staging que se pueden volver a cargar.

<!-- challenge -->

Una migración agrega una llave foránea a una tabla de 500 millones de filas y bloquea las escrituras 20 minutos. ¿Cómo debió escribirse?

<!-- solution -->

Agrega la llave foránea con `NOT VALID` (rápido, se aplica a filas nuevas) y luego corre `VALIDATE CONSTRAINT` aparte, que revisa las filas existentes con un bloqueo más débil que no frena las escrituras.

<!-- takeaways -->

- Algo de DDL es instantáneo; otro reescribe o bloquea.
- Usa `NOT VALID` y luego `VALIDATE` para restricciones.
- Las tablas unlogged son rápidas pero no sobreviven a caídas.

<!-- unit: Trabajar con NULL -->

<!-- goals -->

- Explicar cómo se comporta NULL en las comparaciones.
- Usar COALESCE y NULLIF.

<!-- concept -->

`NULL` significa desconocido, y lo desconocido se propaga: comparar cualquier cosa con `NULL` da desconocido, que los filtros tratan como falso. Por eso `= NULL` nunca coincide y por eso las filas desaparecen en silencio de los `WHERE` que lo olvidan.
Dos funciones cubren la mayoría de casos: una reemplaza valores faltantes por valores por defecto y la otra convierte un valor específico en `NULL`, lo que evita errores como la división entre cero.

<!-- example -->

```sql
SELECT count(*) FROM customer WHERE phone = NULL;     -- always 0
SELECT count(*) FROM customer WHERE phone IS NULL;    -- correct
SELECT COALESCE(nickname, first_name, 'unknown') AS display_name FROM customer;
SELECT revenue / NULLIF(orders, 0) AS avg_order FROM daily_stats;
```

#### ¿Qué significa `NULL` y cómo se comporta en las comparaciones?

Un valor desconocido o ausente. Cualquier comparación con `NULL` devuelve `NULL` (no verdadero), así que hay que usar `IS NULL` / `IS NOT NULL`, e `IS DISTINCT FROM` para comparaciones seguras con nulos.

#### ¿Qué hace `COALESCE`?

Devuelve el primer argumento que no sea nulo: `COALESCE(nickname, first_name, 'unknown')`.

#### ¿Qué es `NULLIF`?

`NULLIF(a, b)` devuelve `NULL` si `a = b`, y `a` en caso contrario. Es útil para evitar divisiones por cero: `x / NULLIF(y, 0)`.

<!-- challenge -->

`WHERE status <> 'cancelled'` devuelve menos filas de lo esperado. Algunas filas tienen `status` NULL. ¿Cómo las incluyes?

<!-- solution -->

`WHERE status IS DISTINCT FROM 'cancelled'` (o `status <> 'cancelled' OR status IS NULL`), porque `NULL <> 'cancelled'` es desconocido y se filtra.

<!-- takeaways -->

- Las comparaciones con NULL son desconocidas.
- Usa `IS NULL` e `IS DISTINCT FROM`.
- `COALESCE` da valores por defecto; `NULLIF` evita dividir entre cero.

<!-- stage: Consultas -->

### Consultas: joins, subconsultas y CTE

<!-- unit: Joins -->

<!-- goals -->

- Elegir el tipo de join correcto y ubicar bien las condiciones.
- Escribir semi-joins, anti-joins y joins LATERAL.

<!-- concept -->

Los joins combinan tablas, y los detalles pequeños cambian los resultados. En un left join, una condición en `ON` decide qué filas de la derecha coinciden y conserva todas las de la izquierda; la misma condición en `WHERE` filtra filas después y convierte en silencio el join en un inner join.
Las preguntas de "tiene coincidencia" y "no tiene coincidencia" son semi y anti-joins, que se escriben mejor con `EXISTS` y `NOT EXISTS`. LATERAL deja que una subconsulta use columnas de tablas anteriores, como traer las tres últimas órdenes por cliente.

<!-- example -->

```sql
-- customers with no orders in 2026 (anti-join)
SELECT c.*
FROM customer c
WHERE NOT EXISTS (
  SELECT 1 FROM orders o
  WHERE o.customer_id = c.customer_id AND o.ordered_at >= '2026-01-01'
);
```

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

<!-- challenge -->

`SELECT * FROM customer WHERE customer_id NOT IN (SELECT customer_id FROM orders)` no devuelve filas, aunque algunos clientes no tienen órdenes. ¿Por qué?

<!-- solution -->

`orders.customer_id` contiene un `NULL`, así que `NOT IN` compara contra un desconocido y no devuelve nada. Usa `NOT EXISTS`, que no se ve afectado por los NULLs.

<!-- takeaways -->

- Las condiciones en `ON` emparejan; las de `WHERE` filtran.
- Usa `EXISTS` / `NOT EXISTS` para semi y anti-joins.
- Las subconsultas LATERAL pueden usar columnas de tablas anteriores.

<!-- unit: Subconsultas, CTEs y operaciones de conjuntos -->

<!-- goals -->

- Estructurar consultas con CTEs, incluidas las recursivas.
- Usar bien subconsultas correlacionadas y operaciones de conjuntos.

<!-- concept -->

Las preguntas complejas se leen mejor por pasos. Los CTEs nombran cada paso; los CTEs recursivos recorren jerarquías como organigramas o generan secuencias. Las subconsultas correlacionadas se refieren a la fila exterior, y el planner a menudo las reescribe como joins.
Las operaciones de conjuntos combinan resultados verticalmente: union quita duplicados con un costo, union all solo anexa, e intersect y except comparan dos resultados, útil para revisar diferencias.

<!-- example -->

```sql
WITH RECURSIVE chain AS (
  SELECT employee_id, manager_id, name, 1 AS depth FROM employee WHERE employee_id = 42
  UNION ALL
  SELECT e.employee_id, e.manager_id, e.name, c.depth + 1
  FROM employee e JOIN chain c ON e.employee_id = c.manager_id
)
SELECT * FROM chain;            -- employee 42 and every manager above
```

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

<!-- challenge -->

¿Cómo verificas si una consulta reescrita devuelve exactamente las mismas filas que la vieja?

<!-- solution -->

Corre `(old EXCEPT new)` y `(new EXCEPT old)`; ambas deben quedar vacías. Para duplicados, compara con `EXCEPT ALL` o con conteos por fila.

<!-- takeaways -->

- Los CTEs hacen legibles los pasos; los recursivos recorren jerarquías.
- `UNION ALL` salvo que necesites deduplicar.
- `EXCEPT` en ambos sentidos compara resultados.

<!-- unit: Cómo corre un SELECT -->

<!-- goals -->

- Explicar el orden lógico de un SELECT.
- Usar HAVING, DISTINCT ON, paginación por keyset y generate_series.

<!-- concept -->

SQL se escribe de arriba abajo pero se evalúa en otro orden: se reúnen y filtran filas, se agrupan, se filtran de nuevo, se calculan ventanas, se proyectan, se deduplican, se ordenan y se limitan. Ese orden explica por qué los alias no se pueden usar en `WHERE` y por qué las funciones de ventana no se pueden filtrar sin una subconsulta.
Algunas funciones de PostgreSQL se apoyan en eso: `DISTINCT ON` conserva una fila por grupo según el orden, la paginación por keyset evita leer las filas saltadas y `generate_series` rellena fechas faltantes.

<!-- example -->

```sql
-- latest order per customer
SELECT DISTINCT ON (customer_id) customer_id, order_id, ordered_at
FROM orders
ORDER BY customer_id, ordered_at DESC;

-- next page after the last seen row (keyset)
SELECT * FROM orders WHERE (ordered_at, order_id) < ('2026-10-17 09:00', 98123)
ORDER BY ordered_at DESC, order_id DESC LIMIT 50;
```

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

<!-- challenge -->

Una API pagina las órdenes con `OFFSET 200000 LIMIT 50` y las páginas profundas dan timeout. ¿Qué cambias?

<!-- solution -->

Pasa a paginación por keyset: recuerda la llave de orden de la última fila (por ejemplo `ordered_at, order_id`) y filtra `WHERE (ordered_at, order_id) < (...)` con un índice que coincida, así cada página lee solo 50 filas.

<!-- takeaways -->

- Orden de evaluación: FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY.
- `DISTINCT ON` conserva una fila por grupo.
- La paginación por keyset sigue rápida en páginas profundas.

<!-- unit: Escribir datos -->

<!-- goals -->

- Hacer upserts con ON CONFLICT y MERGE, y devolver las filas afectadas.
- Encontrar y quitar filas duplicadas.

<!-- concept -->

Las escrituras suelen depender de lo que ya existe. `INSERT ... ON CONFLICT` inserta o actualiza en una sentencia atómica, usando una restricción única para detectar conflictos. `MERGE` maneja casos más ricos, incluidos borrados, a partir de una fuente de cambios. `RETURNING` devuelve las filas afectadas y ahorra otra consulta.
Los duplicados son el problema opuesto: encuéntralos agrupando por la llave prevista, borra todos menos uno por grupo y agrega la restricción única que debió evitarlos.

<!-- example -->

```sql
INSERT INTO company (country_code, business_id, name)
VALUES ('FR', '123456789', 'Acme')
ON CONFLICT (country_code, business_id)
DO UPDATE SET name = EXCLUDED.name
RETURNING company_id, (xmax = 0) AS inserted;
```

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

<!-- challenge -->

Un upsert con `ON CONFLICT (email)` falla con "there is no unique or exclusion constraint matching". ¿Qué falta?

<!-- solution -->

Una restricción única o un índice único sobre `email`. `ON CONFLICT` necesita uno para detectar conflictos; créalo (tras quitar los duplicados existentes).

<!-- takeaways -->

- `ON CONFLICT` hace upsert atómico sobre una llave única.
- `MERGE` aplica inserts, updates y deletes desde una fuente.
- Quita los duplicados y luego agrega la restricción faltante.

### Agregación y funciones de ventana

<!-- unit: Agregados -->

<!-- goals -->

- Usar los agregados comunes y la cláusula FILTER.
- Producir totales multinivel y pivots.

<!-- concept -->

La agregación colapsa filas en resúmenes, y unos pocos detalles deciden si el resumen es correcto. Contar filas, valores no nulos y valores distintos da tres números diferentes. Los filtros dentro de un agregado calculan varios totales condicionales en una sola pasada.
Los grouping sets producen subtotales y totales generales en una consulta, y la agregación condicional pivotea filas en columnas, la forma usual de armar resultados con forma de reporte en SQL.

<!-- example -->

```sql
SELECT country_code,
       count(*)                                  AS orders,
       count(DISTINCT customer_id)               AS customers,
       sum(amount) FILTER (WHERE status = 'paid') AS paid_amount,
       string_agg(DISTINCT channel, ', ' ORDER BY channel) AS channels
FROM orders
GROUP BY ROLLUP (country_code);
```

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

<!-- challenge -->

Un reporte necesita los ingresos por país de 2024, 2025 y 2026 en tres columnas. Escribe el núcleo.

<!-- solution -->

`SELECT country_code, sum(amount) FILTER (WHERE extract(year FROM ordered_at) = 2024) AS y2024, ... 2025 ..., ... 2026 ... FROM orders GROUP BY country_code`.

<!-- takeaways -->

- `count(*)`, `count(col)` y `count(DISTINCT col)` difieren.
- `FILTER` da agregados condicionales.
- `ROLLUP` agrega subtotales; `FILTER` pivotea.

<!-- unit: Bases de las funciones de ventana -->

<!-- goals -->

- Explicar las funciones de ventana y de ranking.
- Obtener el top N por grupo y comparar con filas anteriores.

<!-- concept -->

Las funciones de ventana calculan sobre filas relacionadas conservando cada fila en el resultado. La ventana se define con una partición (qué filas van juntas) y un orden (su secuencia). Con eso, rankear dentro de grupos, comparar con la fila anterior o numerar filas se vuelve una sola expresión.
Como las ventanas se calculan después del `WHERE`, filtrar por sus resultados necesita una consulta externa. Las ventanas con nombre evitan repetir definiciones largas.

<!-- example -->

```sql
SELECT * FROM (
  SELECT product_id, category, revenue,
         rank() OVER w AS rnk,
         revenue - lag(revenue) OVER w AS diff_to_previous
  FROM product_revenue
  WINDOW w AS (PARTITION BY category ORDER BY revenue DESC)
) t
WHERE rnk <= 3;
```

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

<!-- challenge -->

Alguien escribe `WHERE row_number() OVER (...) = 1` y obtiene un error. ¿Cómo lo arreglas?

<!-- solution -->

Las funciones de ventana corren después del `WHERE`, así que calcula el número de fila en una subconsulta o CTE y filtra en la consulta externa (o usa `DISTINCT ON` para la primera fila por grupo).

<!-- takeaways -->

- Las ventanas calculan sobre particiones sin colapsar filas.
- Las funciones de ranking difieren en los empates.
- Filtra los resultados de ventana en una consulta externa.

<!-- unit: Frames y cálculos acumulados -->

<!-- goals -->

- Definir frames de ventana con ROWS y RANGE.
- Calcular totales acumulados, promedios móviles y crecimiento por periodo.

<!-- concept -->

Las ventanas ordenadas tienen un frame: las filas alrededor de la actual que ve la función. El frame por defecto va del inicio hasta la fila actual, lo que hace funcionar los totales acumulados pero también explica por qué `last_value` sorprende.
Elegir entre contar filas y cubrir un rango de valores importa con huecos o empates: un frame de siete filas y uno de siete días difieren cada vez que faltan días.

<!-- example -->

```sql
SELECT day, amount,
       sum(amount) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
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

<!-- challenge -->

`last_value(price) OVER (PARTITION BY product ORDER BY changed_at)` devuelve el precio de cada fila en lugar del último. ¿Por qué y cómo se arregla?

<!-- solution -->

El frame por defecto termina en la fila actual, así que el "último" valor es el actual. Usa `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`, o `first_value` con orden descendente.

<!-- takeaways -->

- Los frames definen qué filas ve una función de ventana.
- `ROWS` cuenta filas; `RANGE` cubre rangos de valores.
- El frame por defecto termina en la fila actual.

<!-- unit: Distribuciones y secuencias -->

<!-- goals -->

- Calcular percentiles, buckets y participaciones en el total.
- Resolver problemas de gaps and islands.

<!-- concept -->

Los promedios esconden las distribuciones. Medianas y percentiles describen con honestidad los datos sesgados, los buckets dividen las filas en cuartiles o deciles, y una ventana sobre todo el resultado convierte conteos en participaciones del total.
Las secuencias de eventos plantean otro clásico: encontrar rachas consecutivas, como los días seguidos que un usuario estuvo activo. Restar un número de fila a la fecha da a cada racha una llave constante, el núcleo de la técnica gaps and islands.

<!-- example -->

```sql
WITH d AS (
  SELECT user_id, day, day - (row_number() OVER (PARTITION BY user_id ORDER BY day))::int AS grp
  FROM (SELECT DISTINCT user_id, day FROM activity) a
)
SELECT user_id, min(day) AS start_day, max(day) AS end_day, count(*) AS streak
FROM d GROUP BY user_id, grp
ORDER BY streak DESC;
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

<!-- challenge -->

El valor promedio de orden es 120, pero la mayoría de órdenes rondan los 40. ¿Cómo describes mejor las órdenes típicas en una consulta?

<!-- solution -->

Usa `percentile_cont(0.5) WITHIN GROUP (ORDER BY amount)` para la mediana, más p90 y p99, que revelan que unas pocas órdenes grandes inflan la media.

<!-- takeaways -->

- Medianas y percentiles describen datos sesgados.
- `sum(...) OVER ()` da participaciones del total.
- Gaps and islands: fecha menos número de fila agrupa rachas.

<!-- stage: Rendimiento -->

### Índices

<!-- unit: Tipos de índice -->

<!-- goals -->

- Elegir entre índices B-tree, hash, GIN, GiST, BRIN y únicos.
- Explicar cómo funcionan los B-trees y qué hace CLUSTER.

<!-- concept -->

Un índice es una estructura aparte que deja a PostgreSQL encontrar filas sin leer toda la tabla. Cada tipo sirve a un tipo de pregunta: B-trees para igualdad, rangos y ordenamiento; GIN para preguntas de "contiene" sobre arrays, JSON y texto; GiST para datos geométricos y de rangos; BRIN para tablas enormes cuyos valores siguen el orden físico.
Los índices únicos además imponen reglas. PostgreSQL nunca mantiene las tablas ordenadas físicamente; `CLUSTER` reordena una vez y el orden se degrada.

<!-- example -->

| Consulta | Índice |
|---|---|
| `WHERE email = ?`, `ORDER BY created_at` | B-tree |
| `WHERE tags @> '{sale}'`, JSONB `@>` | GIN |
| `WHERE during && tstzrange(...)` | GiST |
| `WHERE logged_at > now() - interval '1 day'` sobre 5 TB solo de anexado | BRIN |

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

<!-- challenge -->

Una tabla de logs de 3 TB solo de anexado se consulta por rango de tiempo. Un B-tree sobre `logged_at` pesa 90 GB. ¿Qué alternativa consideras?

<!-- solution -->

Un índice BRIN sobre `logged_at`: como las filas se anexan en orden de tiempo, BRIN guarda mínimo y máximo por rango de bloques y ocupa unos pocos MB mientras poda la mayor parte de la tabla.

<!-- takeaways -->

- Elige el tipo de índice según la forma de la consulta.
- B-tree es el estándar; GIN y GiST para tipos complejos.
- BRIN es diminuto para tablas enormes ordenadas de forma natural.

<!-- unit: Diseñar índices -->

<!-- goals -->

- Diseñar índices compuestos, parciales, de expresión y de cobertura.
- Lograr index-only scans y evitar índices redundantes.

<!-- concept -->

Los buenos índices coinciden con cómo filtran y ordenan las consultas. En un índice compuesto las columnas se usan de izquierda a derecha, así que las de igualdad van primero y las de rango al final; un índice compuesto suele volver redundante uno sobre su primera columna.
Los índices pueden ser más angostos o más ricos que una columna: los parciales cubren solo las filas que piden las consultas, los de expresión cubren valores calculados y las columnas incluidas dejan que el índice responda solo una consulta, si el visibility map lo permite.

<!-- example -->

```sql
CREATE INDEX ON orders (customer_id, ordered_at);                     -- composite
CREATE INDEX ON orders (ordered_at) WHERE status = 'pending';         -- partial
CREATE INDEX ON customer (lower(email));                              -- expression
CREATE INDEX ON orders (customer_id) INCLUDE (amount);                -- covering
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

<!-- challenge -->

Las consultas filtran `WHERE status = 'pending' AND ordered_at > now() - interval '1 day'`; el 99 % de las órdenes no están pendientes. ¿Qué índice encaja mejor?

<!-- solution -->

Un índice parcial `ON orders (ordered_at) WHERE status = 'pending'`: contiene solo las filas pendientes, así que es pequeño y coincide exactamente con la consulta.

<!-- takeaways -->

- Orden compuesto: igualdad primero, rangos al final.
- Los índices parciales y de expresión encajan con consultas puntuales.
- Los índices de cobertura permiten index-only scans.

<!-- unit: Índices para datos especiales -->

<!-- goals -->

- Indexar documentos JSONB y búsquedas de subcadenas.
- Entender las pending lists de GIN.

<!-- concept -->

Algunas consultas no pueden usar B-trees comunes. Buscar dentro de documentos JSON, probar contención o encontrar texto en cualquier parte de una cadena necesita índices invertidos. GIN indexa cada clave o trigrama para que esas búsquedas se vuelvan index scans.
GIN es costoso de actualizar, así que guarda las entradas nuevas en una pending list y las fusiona después. Eso acelera las escrituras pero puede volver irregulares las lecturas hasta que ocurre la fusión.

<!-- example -->

```sql
CREATE INDEX ON events USING gin (payload jsonb_path_ops);    -- payload @> '{"type":"click"}'
CREATE INDEX ON events ((payload->>'user_id'));               -- equality on one key
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX ON company USING gin (name gin_trgm_ops);        -- name ILIKE '%acme%'
```

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

<!-- challenge -->

Las búsquedas con `name ILIKE '%dupont%'` sobre 20 millones de empresas tardan 8 segundos. ¿Qué agregas?

<!-- solution -->

Un índice GIN de trigramas (`pg_trgm`, `gin_trgm_ops`) sobre `name`, que soporta `LIKE`/`ILIKE` con comodín al inicio.

<!-- takeaways -->

- GIN indexa claves y trigramas para contención y subcadenas.
- Los índices de expresión cubren claves JSON individuales.
- GIN guarda las escrituras en una pending list.

<!-- unit: Costo y mantenimiento de índices -->

<!-- goals -->

- Sopesar el costo de los índices y entender por qué se ignoran.
- Crear, reconstruir, encontrar y medir índices con seguridad.

<!-- concept -->

Los índices no son gratis: cada uno frena cada escritura y ocupa espacio, y los que no se usan son puro costo. El planner además ignora índices cuando un escaneo es más barato, cuando las estadísticas lo engañan o cuando la consulta envuelve la columna en una función.
El mantenimiento sale de ahí: construir índices sin bloquear escrituras, reconstruir de la misma forma los inflados, buscar índices faltantes en las estadísticas de escaneo y las consultas lentas, y borrar los que nadie usa.

<!-- example -->

```sql
CREATE INDEX CONCURRENTLY orders_customer_idx ON orders (customer_id);
REINDEX INDEX CONCURRENTLY orders_customer_idx;
SELECT relname, seq_scan, seq_tup_read, idx_scan FROM pg_stat_user_tables ORDER BY seq_tup_read DESC LIMIT 10;
SELECT pg_size_pretty(pg_indexes_size('orders'));
```

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

<!-- challenge -->

Una tabla tiene 14 índices y los inserts se volvieron lentos. ¿Cómo decides cuáles borrar?

<!-- solution -->

Revisa `pg_stat_user_indexes.idx_scan` durante un periodo representativo (excluyendo índices únicos y de restricciones), busca duplicados y prefijos de índices compuestos, y borra los que no se usan, anotando cómo recrearlos si hace falta.

<!-- takeaways -->

- Cada índice frena las escrituras y ocupa espacio.
- Construye y reconstruye índices de forma concurrente.
- Encuentra índices faltantes y sin uso con las estadísticas.

### Transacciones, MVCC y concurrencia

<!-- unit: Transacciones y MVCC -->

<!-- goals -->

- Explicar transacciones, MVCC y tuplas muertas.
- Usar bien savepoints, HOT updates y commit asíncrono.

<!-- concept -->

PostgreSQL deja trabajar a lectores y escritores al mismo tiempo guardando varias versiones de las filas. Un update escribe una versión nueva; las transacciones ven la versión que corresponde a su snapshot. Nadie espera a los lectores, pero las versiones viejas se acumulan como tuplas muertas hasta que vacuum las quita.
Algunas optimizaciones bajan ese costo: los updates que no tocan columnas indexadas pueden quedarse en la misma página sin cambiar los índices. Los savepoints permiten rollback parcial, y relajar la durabilidad del commit cambia una pequeña ventana de pérdida por velocidad.

<!-- example -->

```sql
BEGIN;
UPDATE account SET balance = balance - 100 WHERE account_id = 1;
SAVEPOINT before_fee;
UPDATE account SET balance = balance - 2 WHERE account_id = 1;
ROLLBACK TO before_fee;         -- undo only the fee
COMMIT;
```

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

<!-- challenge -->

Una tabla que se actualiza constantemente sigue creciendo, y sus índices también, aunque la cantidad de filas no cambia. ¿Qué detalle de MVCC puedes usar para reducir el crecimiento de los índices?

<!-- solution -->

Habilita los HOT updates: evita indexar columnas que se actualizan seguido y fija un `fillfactor` más bajo para que las versiones nuevas quepan en la misma página, así los updates se saltan los cambios de índice.

<!-- takeaways -->

- MVCC guarda versiones para que los lectores no bloqueen a los escritores.
- Las tuplas muertas necesitan vacuum.
- Los HOT updates evitan cambios de índice.

<!-- unit: Aislamiento y anomalías -->

<!-- goals -->

- Comparar los niveles de aislamiento de PostgreSQL y las anomalías que evitan.
- Evitar actualizaciones perdidas con bloqueos o chequeos optimistas.

<!-- concept -->

El aislamiento decide qué ve una transacción de otras que corren al mismo tiempo. Read Committed, el nivel por defecto, da a cada sentencia un snapshot nuevo. Repeatable Read conserva un snapshot para toda la transacción. Serializable hace que las transacciones concurrentes se comporten como si corrieran una tras otra, abortando las que no pueden.
El bug clásico en el nivel por defecto es la actualización perdida: dos sesiones leen, modifican y escriben el mismo valor. Los updates atómicos, los bloqueos de fila o los chequeos de versión la evitan.

<!-- example -->

```sql
-- optimistic locking: fail if someone else changed the row
UPDATE product SET price = 19.90, version = version + 1
WHERE product_id = 7 AND version = 12;
-- 0 rows updated → reload and retry
```

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

<!-- challenge -->

Dos agentes de soporte editan la misma nota de cliente a la vez, y una edición desaparece. ¿Qué enfoque eliges para una app web?

<!-- solution -->

Bloqueo optimista: guarda una columna `version`, actualiza con `WHERE version = :read_version` y muestra un mensaje de conflicto si no se actualizó ninguna fila, en lugar de mantener bloqueos mientras el usuario piensa.

<!-- takeaways -->

- Read Committed por defecto; Serializable para corrección estricta.
- Las actualizaciones perdidas ocurren con leer-modificar-escribir.
- Usa updates atómicos, bloqueos de fila o chequeos de versión.

<!-- unit: Bloqueos -->

<!-- goals -->

- Usar bloqueos de fila, SKIP LOCKED y advisory locks.
- Entender los deadlocks y los conflictos de bloqueo del DDL.

<!-- concept -->

La mayor parte de la concurrencia en PostgreSQL no necesita bloqueos explícitos, pero algunos patrones sí. Bloquear filas seleccionadas las reserva hasta el commit; saltarse filas ya bloqueadas deja que muchos workers saquen trabajos de una misma tabla de cola; los advisory locks coordinan tareas de la aplicación.
Los bloqueos traen dos riesgos: los deadlocks, cuando las transacciones se esperan entre sí, y el DDL que toma bloqueos exclusivos y pone en fila detrás a todas las demás consultas.

<!-- example -->

```sql
-- job queue worker
BEGIN;
SELECT job_id, payload FROM job
WHERE status = 'ready'
ORDER BY created_at
LIMIT 1
FOR UPDATE SKIP LOCKED;
-- process, then
UPDATE job SET status = 'done' WHERE job_id = :id;
COMMIT;
```

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

<!-- challenge -->

Una migración corre `ALTER TABLE orders ADD COLUMN ...` y toda la app se congela, aunque el cambio en sí es instantáneo. ¿Por qué?

<!-- solution -->

El `ALTER` espera un bloqueo `ACCESS EXCLUSIVE` detrás de una consulta larga, y cada consulta nueva hace fila detrás del `ALTER`. Fija `lock_timeout` en las migraciones y reintenta, y evita correrlas durante transacciones largas.

<!-- takeaways -->

- `FOR UPDATE SKIP LOCKED` sirve para colas de trabajos.
- PostgreSQL detecta y rompe los deadlocks.
- Un DDL esperando bloqueo pone todo en fila; usa `lock_timeout`.

<!-- unit: Vacuum y mantenimiento -->

<!-- goals -->

- Explicar VACUUM, VACUUM FULL, autovacuum y ANALYZE.
- Evitar el bloat por transacciones largas y el wraparound de IDs de transacción.

<!-- concept -->

Los restos de MVCC necesitan limpieza. Vacuum vuelve reutilizable el espacio de las tuplas muertas, actualiza el visibility map y congela filas viejas; autovacuum lo hace automáticamente a medida que cambian las tablas, además de analizar estadísticas. El vacuum full reescribe la tabla para achicarla, con un bloqueo exclusivo.
Dos cosas derrotan a vacuum: las transacciones largas, cuyos snapshots viejos mantienen vivas las tuplas muertas, y las tablas descuidadas que se acercan al wraparound de IDs de transacción, lo que fuerza un vacuum de emergencia.

<!-- example -->

```sql
SELECT relname, n_dead_tup, last_autovacuum, last_autoanalyze
FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 10;
ALTER TABLE events SET (autovacuum_vacuum_scale_factor = 0.02);   -- vacuum big tables more often
SELECT datname, age(datfrozenxid) FROM pg_database ORDER BY 2 DESC;
```

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

<!-- challenge -->

Una tabla grande se infla aunque autovacuum corre. `pg_stat_activity` muestra una sesión "idle in transaction" desde hace dos días. ¿Cuál es la relación?

<!-- solution -->

La transacción abierta conserva un snapshot viejo, así que vacuum no puede quitar tuplas muertas más nuevas que él. Termina la sesión, fija `idle_in_transaction_session_timeout` y arregla la aplicación.

<!-- takeaways -->

- Vacuum recupera espacio; vacuum full achica con bloqueo.
- Ajusta autovacuum por tabla con mucho movimiento.
- Las transacciones largas bloquean la limpieza y arriesgan el wraparound.

### Rendimiento y planificación de consultas

<!-- unit: Leer planes de ejecución -->

<!-- goals -->

- Leer la salida de EXPLAIN y EXPLAIN ANALYZE.
- Reconocer tipos de scan, algoritmos de join y el comportamiento de LIMIT.

<!-- concept -->

El planner convierte cada consulta en un árbol de operaciones y elige el más barato según sus estimaciones. `EXPLAIN` muestra ese árbol; `EXPLAIN ANALYZE` lo ejecuta y agrega filas y tiempos reales. Comparar filas estimadas contra reales es el hábito más útil: brechas grandes significan malas estadísticas y casi siempre malos planes.
Los tipos de nodo cuentan la historia: cómo se leen las tablas, cómo se cruzan y si un `LIMIT` deja parar temprano la consulta gracias a un índice que coincide.

<!-- example -->

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT o.* FROM orders o JOIN customer c USING (customer_id)
WHERE c.country_code = 'FR' AND o.ordered_at >= '2026-10-01';
-- look for: rows=estimated vs actual, Seq Scan on big tables, Sort spilling, loops
```

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

<!-- challenge -->

Un plan estima 10 filas para un filtro pero obtiene 2 millones, y elige un nested loop que corre minutos. ¿Qué haces?

<!-- solution -->

Corrige la estimación: corre `ANALYZE`, sube las estadísticas de columnas sesgadas o agrega estadísticas extendidas para columnas correlacionadas, para que el planner elija un hash join. Luego revisa de nuevo el plan.

<!-- takeaways -->

- `EXPLAIN ANALYZE` muestra filas y tiempos reales.
- Las brechas de estimación apuntan a problemas de estadísticas.
- Los joins son nested loop, hash o merge.

<!-- unit: Estadísticas y estimaciones -->

<!-- goals -->

- Mantener precisas las estadísticas del planner, incluidas las extendidas.
- Diagnosticar consultas que de pronto se vuelven lentas.

<!-- concept -->

El planner vale lo que sabe. Las estadísticas muestrean los valores de cada columna; cuando están viejas, son muy gruesas para datos sesgados o no ven correlaciones entre columnas, las estimaciones fallan y los planes también. Envolver columnas indexadas en funciones también las oculta tanto del índice como de las estadísticas.
Cuando una consulta que era rápida se vuelve lenta, la causa suele ser una de estas: un plan cambiado, estadísticas viejas, más datos, bloat o nueva contención.

<!-- example -->

```sql
-- correlated columns: city implies country
CREATE STATISTICS addr_stats (dependencies) ON country_code, city FROM address;
ALTER TABLE orders ALTER COLUMN status SET STATISTICS 1000;
ANALYZE address; ANALYZE orders;
-- sargable rewrite:
-- WHERE date(created_at) = '2026-10-15'  →  WHERE created_at >= '2026-10-15' AND created_at < '2026-10-16'
```

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

<!-- challenge -->

Una consulta que filtra `WHERE country_code = 'FR' AND city = 'Paris'` estima 50 filas pero devuelve 400.000. ¿Por qué y cómo se arregla?

<!-- solution -->

El planner multiplica las dos selectividades como si fueran independientes, pero la ciudad implica el país. Crea estadísticas extendidas (dependencies) sobre las dos columnas y analiza.

<!-- takeaways -->

- Las estadísticas guían las estimaciones; mantenlas frescas.
- Las estadísticas extendidas capturan correlaciones entre columnas.
- Mantén los filtros sargables: sin funciones sobre columnas indexadas.

<!-- unit: Memoria, paralelismo y JIT -->

<!-- goals -->

- Ajustar work_mem y los principales parámetros de memoria.
- Entender las consultas paralelas y la compilación JIT.

<!-- concept -->

Los parámetros de memoria deciden cuánto trabajo se queda en RAM. `shared_buffers` es la caché propia de PostgreSQL; `work_mem` es por operación, así que una consulta compleja con muchos ordenamientos en muchas conexiones puede multiplicarlo muchas veces. Muy bajo y los ordenamientos se derraman a disco; muy alto y el servidor se queda sin memoria.
Para consultas analíticas grandes, los workers paralelos reparten escaneos y joins, y JIT compila expresiones a código máquina, lo que ayuda a las consultas largas y perjudica a las cortas.

<!-- example -->

```text
shared_buffers = 16GB            # ~25% of 64 GB RAM
effective_cache_size = 48GB      # planner hint: OS cache + shared_buffers
work_mem = 32MB                  # per sort/hash node, per connection
maintenance_work_mem = 2GB       # VACUUM, CREATE INDEX
max_parallel_workers_per_gather = 4
```

#### ¿Por qué una función sobre una columna indexada puede impedir el uso del índice?

El índice guarda los valores en bruto de la columna, así que `WHERE date(created_at) = '2026-10-15'` no puede usar un índice sobre `created_at`. Reescríbelo como un rango (`created_at >= '2026-10-15' AND created_at < '2026-10-16'`) o crea un índice de expresión.

#### ¿Qué son las estadísticas extendidas?

`CREATE STATISTICS` permite al planificador conocer las correlaciones entre columnas (dependencias, número de valores distintos, combinaciones de valores más frecuentes), lo que mejora las estimaciones de los filtros sobre varias columnas correlacionadas, como ciudad y código postal.

#### ¿Qué controla `default_statistics_target`?

Cuántos valores de muestra y tramos de histograma guarda `ANALYZE` por columna. Aumentarlo en las columnas con distribuciones sesgadas mejora las estimaciones a costa del tiempo de planificación.

#### ¿Cómo se cargan grandes volúmenes de datos rápidamente?

Usando `COPY` en lugar de inserciones fila a fila, cargando dentro de una sola transacción, creando los índices y las claves foráneas después de la carga, considerando tablas de staging unlogged, aumentando `maintenance_work_mem` para la creación de índices y ejecutando `ANALYZE` después.

<!-- challenge -->

`EXPLAIN ANALYZE` muestra "Sort Method: external merge Disk: 2GB" en un reporte nocturno. ¿Qué cambias?

<!-- solution -->

Sube `work_mem` para esa sesión o rol (`SET work_mem = '512MB'` antes del reporte), no globalmente, para que el ordenamiento quepa en memoria sin arriesgar el consumo de todas las conexiones.

<!-- takeaways -->

- `shared_buffers` es caché; `work_mem` es por operación.
- Sube `work_mem` por sesión para ordenamientos grandes.
- Las consultas paralelas y JIT ayudan a las consultas analíticas largas.

<!-- unit: Encontrar y detener consultas lentas -->

<!-- goals -->

- Encontrar consultas costosas y en curso con pg_stat_statements y pg_stat_activity.
- Detener consultas descontroladas y detectar el bloat de las tablas.

<!-- concept -->

Dos vistas responden la mayoría de preguntas de rendimiento. `pg_stat_statements` agrega la historia por forma de consulta y muestra qué consultas cuestan más tiempo en total. `pg_stat_activity` muestra qué está corriendo ahora, cuánto lleva y qué espera.
Cuando algo se atasca, puedes cancelar la consulta o terminar la sesión. El bloat, espacio retenido por tuplas muertas, es el problema lento detrás de escaneos cada vez más lentos.

<!-- example -->

```sql
SELECT pid, now() - query_start AS duration, state, wait_event_type, left(query, 80)
FROM pg_stat_activity
WHERE state <> 'idle' ORDER BY duration DESC;
SELECT pg_cancel_backend(12345);     -- cancel the query
SELECT pg_terminate_backend(12345);  -- close the connection
```

#### ¿Qué es el comando `COPY`?

La forma más rápida de cargar o exportar datos en bloque entre tablas y archivos o flujos: `COPY company FROM '/data/company.csv' WITH (FORMAT csv, HEADER)`. Desde un cliente, usa el `\copy` de psql o el soporte de COPY del driver. PostgreSQL 17 puede saltarse las filas mal formadas con `ON_ERROR ignore`.

#### ¿Qué es un pool de conexiones y por qué se usa PgBouncer?

Reutilizar un número pequeño de conexiones a la base de datos para muchos clientes. PgBouncer se sitúa entre las aplicaciones y PostgreSQL, en modo sesión, transacción o sentencia, y reduce el costo de cada conexión.

#### ¿Qué es la consulta paralela?

PostgreSQL puede repartir los recorridos secuenciales, los joins y las agregaciones entre varios procesos trabajadores, según `max_parallel_workers_per_gather` y el tamaño de la tabla.

#### ¿Qué es la compilación JIT en PostgreSQL?

La compilación en tiempo de ejecución (con LLVM) de las expresiones de consultas analíticas largas. Acelera los cálculos pesados, pero añade sobrecosto a las consultas cortas. La controlan `jit` y unos umbrales de costo.

<!-- challenge -->

La base está lenta, pero ninguna consulta individual parece larga. ¿Dónde buscas la causa?

<!-- solution -->

En `pg_stat_statements` ordenado por tiempo total de ejecución: a menudo una consulta rápida llamada millones de veces domina la carga. Optimízala o ponla en caché, o reduce cuántas veces se llama.

<!-- takeaways -->

- `pg_stat_statements` ordena las consultas por costo total.
- `pg_stat_activity` muestra lo que corre ahora.
- Cancela consultas primero; termina sesiones si hace falta.

<!-- unit: Conexiones y carga masiva -->

<!-- goals -->

- Hacer pooling de conexiones con PgBouncer.
- Cargar grandes volúmenes rápido con COPY.

<!-- concept -->

Dos problemas de rendimiento comunes están fuera de los planes de consulta. Demasiadas conexiones gastan memoria y CPU en administrar procesos, así que un pooler como PgBouncer deja que miles de clientes compartan unas pocas decenas de conexiones al servidor.
Cargar datos fila por fila desperdicia viajes de red y costo por sentencia. `COPY` envía los datos en bloque, y cargar antes de crear los índices, dentro de una transacción, es todavía más rápido.

<!-- example -->

```bash
psql -c "\copy staging.orders (order_id, customer_id, amount, ordered_at) FROM 'orders.csv' WITH (FORMAT csv, HEADER true)"
```
```ini
; pgbouncer.ini
pool_mode = transaction
default_pool_size = 40
max_client_conn = 2000
```

#### ¿Cómo interactúa `LIMIT` con `ORDER BY` y los índices?

Con un índice que coincida con el `ORDER BY`, PostgreSQL solo lee las primeras filas que necesita. Sin él, tiene que ordenarlo todo (con un heapsort de top N) antes de aplicar el límite.

#### ¿Qué es el bloat de las tablas y cómo se detecta?

Espacio desperdiciado por tuplas muertas que vacuum no ha recuperado o que el sistema operativo no ha recibido de vuelta. Se detecta con `pgstattuple`, con consultas de estimación del bloat, o viendo tablas que crecen más deprisa que su número de filas.

#### ¿Qué revisarías primero cuando una consulta se vuelve lenta de repente?

Su plan (`EXPLAIN ANALYZE`) comparado con el de antes, la actualidad de las estadísticas (último analyze), los cambios de volumen de datos, los bloqueos y esperas en `pg_stat_activity`, el bloat, y si los parámetros o un índice nuevo han cambiado el plan.

<!-- challenge -->

Un script de Python inserta 10 millones de filas con un `INSERT` por fila y tarda 3 horas. ¿Qué cambias?

<!-- solution -->

Usa `COPY` (por ejemplo `cursor.copy_expert` o el `copy` de psycopg) hacia una tabla de staging, dentro de una transacción, y luego haz upsert al destino en una sentencia por conjuntos. Espera minutos en lugar de horas.

<!-- takeaways -->

- Haz pooling; no abras miles de conexiones directas.
- `COPY` es el camino rápido para cargas masivas.
- Carga primero, indexa después, en una transacción.

<!-- stage: Diseño y operación -->

### Modelado de datos, normalización y OLAP

<!-- unit: Normalización -->

<!-- goals -->

- Explicar 1NF, 2NF, 3NF y BCNF.
- Decidir cuándo se justifica desnormalizar, OLTP frente a OLAP.

<!-- concept -->

La normalización guarda cada hecho una vez para que las actualizaciones no dejen contradicciones: sin grupos repetidos, sin atributos que dependan de parte de una llave, sin atributos que dependan de otros atributos no llave. Es la forma correcta para sistemas transaccionales, donde importa sobre todo la corrección de muchas escrituras pequeñas.
La analítica invierte las prioridades: dominan las lecturas, así que la redundancia deliberada, como tablas precruzadas o preagregadas, hace las consultas más simples y rápidas.

<!-- example -->

```text
Not 3NF: orders(order_id, customer_id, customer_city, amount)   ← city depends on customer
3NF:     orders(order_id, customer_id, amount)
         customer(customer_id, city)
```

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

<!-- challenge -->

Una tabla guarda la ciudad del cliente en cada orden, y tras una mudanza las órdenes viejas y nuevas muestran ciudades distintas. ¿Es un bug?

<!-- solution -->

En un modelo OLTP, sí: la ciudad depende del cliente, así que va en la tabla de clientes (3NF). En un modelo analítico, guardar la ciudad al momento de la orden puede ser historia intencional, pero entonces debe ser explícito.

<!-- takeaways -->

- Las formas normales eliminan redundancia y anomalías de actualización.
- OLTP favorece la normalización; OLAP tolera la redundancia.
- Desnormaliza a propósito, para las lecturas.

<!-- unit: Bases dimensionales -->

<!-- goals -->

- Describir las operaciones OLAP y los esquemas estrella y copo de nieve.
- Declarar el grano y el tipo de una tabla de hechos.

<!-- concept -->

Los modelos analíticos se organizan alrededor de preguntas: los hechos guardan mediciones y las dimensiones el contexto por el que segmentas. Las operaciones OLAP, drill down, roll up, slice y pivot, son formas de moverse por esa estructura.
Una estrella mantiene las dimensiones planas alrededor del hecho; un copo de nieve las normaliza. La decisión más importante es el grano, qué significa una fila de hechos, que luego decide el tipo de hecho: eventos, snapshots periódicos o procesos acumulativos.

<!-- example -->

```text
fct_sales (grain: one order line)
  date_key, customer_key, product_key, store_key, quantity, net_amount
dim_date, dim_customer, dim_product, dim_store  (star)
```

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

<!-- challenge -->

Un equipo necesita los saldos de cuentas al cierre de cada mes. ¿Debe sumar hechos de transacciones al vuelo o guardar otra cosa?

<!-- solution -->

Guardar un hecho de periodic snapshot (una fila por cuenta por mes con el saldo). Los saldos son semiaditivos y costosos de reconstruir desde todas las transacciones históricas.

<!-- takeaways -->

- Los hechos miden; las dimensiones describen.
- Las estrellas son más simples que los copos de nieve.
- El grano decide el tipo de hecho.

<!-- unit: Llaves y dimensiones -->

<!-- goals -->

- Usar llaves sustitutas y naturales en un warehouse.
- Construir dimensiones junk, degeneradas, conformadas y de fecha.

<!-- concept -->

Los warehouses emiten sus propias llaves sustitutas para las filas de dimensión y conservan las llaves naturales de las fuentes como atributos. Eso aísla el modelo de los cambios en las fuentes y deja que una entidad tenga versiones históricas.
Algunos patrones de dimensión se repiten: junk dimensions para los flags sueltos, dimensiones degeneradas para identificadores que se quedan en el hecho, dimensiones conformadas compartidas entre marts y una dimensión de fecha que guarda la lógica de calendario una sola vez.

<!-- example -->

```sql
INSERT INTO dim_date (date_key, day, month, quarter, is_weekend)
SELECT to_char(d, 'YYYYMMDD')::int, d::date, extract(month FROM d), extract(quarter FROM d),
       extract(isodow FROM d) IN (6, 7)
FROM generate_series('2020-01-01'::date, '2030-12-31', interval '1 day') AS d;
```

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

<!-- challenge -->

Los reportes agrupan por trimestre usando `extract(quarter ...)` en todas partes, pero el año fiscal de la empresa empieza en abril. ¿Cómo lo arreglas una sola vez?

<!-- solution -->

Agrega atributos fiscales (año fiscal, trimestre fiscal) a la dimensión de fecha, calculados una vez, y haz que los reportes la crucen en lugar de calcular los trimestres por su cuenta.

<!-- takeaways -->

- Las llaves sustitutas aíslan el warehouse de las fuentes.
- Las dimensiones junk, degeneradas y conformadas resuelven necesidades recurrentes.
- Una dimensión de fecha centraliza la lógica de calendario.

<!-- unit: Historia y arquitecturas -->

<!-- goals -->

- Implementar dimensiones de cambio lento en PostgreSQL.
- Ubicar PostgreSQL frente a Data Vault, medallion y motores analíticos.

<!-- concept -->

Las dimensiones cambian, y las de cambio lento tipo 2 guardan la historia cerrando la versión actual e insertando una nueva, idealmente en una sola transacción para que los lectores nunca vean un hueco.
PostgreSQL funciona bien como warehouse pequeño o capa de consumo, pero no es columnar: con muchos terabytes de escaneos, encajan mejor warehouses dedicados o lakehouses. Metodologías como Data Vault y las capas medallion aplican en ambos casos.

<!-- example -->

```sql
BEGIN;
UPDATE dim_customer SET valid_to = now(), is_current = false
WHERE customer_id = 552 AND is_current;
INSERT INTO dim_customer (customer_id, segment, valid_from, valid_to, is_current)
VALUES (552, 'Mid', now(), 'infinity', true);
COMMIT;
```

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

<!-- challenge -->

Una base de reportes en PostgreSQL ya tiene 6 TB y los dashboards que escanean meses de datos tardan minutos. ¿Qué sugieres?

<!-- solution -->

A corto plazo, particiona y preagrega, pero planea llevar la analítica de escaneos grandes a un warehouse columnar o un lakehouse, dejando PostgreSQL para cargas operativas y de consumo pequeñas.

<!-- takeaways -->

- SCD2 cierra e inserta versiones en una transacción.
- PostgreSQL sirve para warehouses pequeños y capas de consumo.
- Los escaneos grandes van en motores columnares.

### Administración, seguridad, copias de seguridad y replicación

<!-- unit: Roles y acceso -->

<!-- goals -->

- Manejar roles, acceso de solo lectura y seguridad por fila.
- Configurar la autenticación y evitar la inyección SQL.

<!-- concept -->

En PostgreSQL, usuarios y grupos son roles, y los privilegios fluyen por la pertenencia a roles. El acceso de lectura a un esquema necesita usage sobre el esquema, select sobre las tablas y privilegios por defecto para las tablas creadas después. La seguridad por fila restringe aún más el acceso, fila a fila.
Quién puede conectarse lo deciden las reglas por host y un hashing fuerte de contraseñas. Dentro de las aplicaciones, las consultas parametrizadas evitan que la entrada del usuario se vuelva SQL.

<!-- example -->

```sql
CREATE ROLE reporting NOLOGIN;
GRANT USAGE ON SCHEMA analytics TO reporting;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO reporting;
ALTER DEFAULT PRIVILEGES IN SCHEMA analytics GRANT SELECT ON TABLES TO reporting;
CREATE ROLE ana LOGIN PASSWORD '...' IN ROLE reporting;
```

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

<!-- challenge -->

Un rol de solo lectura funciona con las tablas existentes, pero los analistas pierden acceso a cada tabla nueva. ¿Qué falta?

<!-- solution -->

Privilegios por defecto: `ALTER DEFAULT PRIVILEGES ... GRANT SELECT ON TABLES TO reporting` para el rol que crea las tablas, así las tablas futuras se otorgan automáticamente.

<!-- takeaways -->

- Los roles son usuarios y grupos; otorga por pertenencia.
- Los privilegios por defecto cubren tablas futuras.
- RLS restringe filas; los parámetros evitan la inyección.

<!-- unit: Backups y recuperación -->

<!-- goals -->

- Comparar backups lógicos y físicos.
- Hacer backup con pg_dump y recuperar a un punto en el tiempo.

<!-- concept -->

Hay dos tipos de backup. Los lógicos exportan objetos y datos como SQL o archivos: portables entre versiones y selectivos, pero lentos para bases grandes. Los físicos copian los archivos de datos y, con el WAL archivado, permiten reproducir los cambios hasta cualquier momento.
Esa segunda capacidad, la recuperación a un punto en el tiempo, es la que te salva de errores como un mal borrado a las 10:42: restauras el backup base y detienes la reproducción a las 10:41.

<!-- example -->

```bash
pg_dump -Fc -d shop -f shop.dump
pg_restore -d shop_restore -j 4 shop.dump
# PITR: restore base backup, then in postgresql.conf
#   restore_command = 'cp /archive/%f %p'
#   recovery_target_time = '2026-10-17 10:41:00+02'
```

#### ¿Qué diferencia hay entre las copias de seguridad lógicas y físicas?

Las copias lógicas (`pg_dump`, `pg_dumpall`) exportan archivos SQL o de archivo con los objetos y los datos. Son portables entre versiones y se pueden restaurar de forma selectiva, pero son lentas en bases de datos grandes. Las copias físicas (`pg_basebackup`, pgBackRest) copian los archivos de datos y el WAL. Son rápidas en bases grandes y permiten la recuperación a un momento dado.

#### ¿Cómo se hace y se restaura una copia de una sola base de datos con pg_dump?

```bash
pg_dump -Fc -d mydb -f mydb.dump          # formato custom, comprimido
pg_restore -d newdb -j 4 mydb.dump        # restauración en paralelo
```

#### ¿Qué es la recuperación a un momento dado (PITR)?

Restaurar una copia base y reproducir el WAL archivado hasta un instante elegido, por ejemplo justo antes de un `DELETE` accidental.

<!-- challenge -->

Una base de 4 TB se respalda cada noche con `pg_dump`, que tarda 9 horas, y restaurar tardaría más. ¿Qué cambias?

<!-- solution -->

Pasa a backups físicos (pgBackRest o los snapshots del servicio administrado) con archivado continuo del WAL, lo que permite restauraciones rápidas y recuperación a un punto en el tiempo; deja `pg_dump` para exportaciones selectivas.

<!-- takeaways -->

- Los backups lógicos son portables; los físicos, rápidos.
- El archivado del WAL permite recuperar a un punto en el tiempo.
- Prueba las restauraciones, no solo los backups.

<!-- unit: Replicación y CDC -->

<!-- goals -->

- Comparar replicación streaming y lógica, síncrona y asíncrona.
- Usar CDC y replication slots con seguridad, y construir alta disponibilidad.

<!-- concept -->

La replicación streaming envía el WAL a standbys que lo reproducen y mantienen copias exactas para failover y escalar lecturas. Las réplicas asíncronas pueden ir atrasadas; las síncronas hacen que los commits esperen confirmación, cambiando latencia por cero pérdida de datos.
La replicación lógica funciona por tabla y entre versiones, y las herramientas de CDC usan la misma decodificación para enviar cambios a Kafka o a un lago. Los replication slots guardan el WAL hasta que los consumidores lo leen, lo que llena los discos si un consumidor desaparece. La HA agrega encima un gestor de failover.

<!-- example -->

```sql
-- publisher
CREATE PUBLICATION orders_pub FOR TABLE orders, order_line;
-- subscriber
CREATE SUBSCRIPTION orders_sub CONNECTION 'host=primary dbname=shop user=repl' PUBLICATION orders_pub;
-- watch slots
SELECT slot_name, active, pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS retained
FROM pg_replication_slots;
```

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

<!-- challenge -->

Tras un failover a un standby asíncrono, faltan los últimos segundos de órdenes. ¿Cómo pudiste evitarlo y a qué costo?

<!-- solution -->

Replicación síncrona hacia al menos un standby (`synchronous_standby_names`), para que los commits esperen la confirmación del standby. El costo es mayor latencia de commit y depender de la disponibilidad del standby.

<!-- takeaways -->

- La replicación streaming copia todo; la lógica copia tablas.
- La replicación síncrona evita pérdidas a costa de latencia.
- Monitorea los slots; los inactivos retienen WAL.

<!-- unit: Operar un servidor -->

<!-- goals -->

- Actualizar versiones mayores y monitorear un servidor PostgreSQL.
- Usar el cache hit ratio, statement_timeout y servicios administrados.

<!-- concept -->

Operar PostgreSQL significa vigilar unas pocas señales y planear unos pocos eventos. Señales: conexiones, tasa de transacciones, cache hit ratio, consultas lentas, bloqueos, retraso de replicación, bloat y edad hacia el wraparound. Eventos: las actualizaciones mayores, que necesitan pruebas y un método acorde al tamaño y al tiempo de inactividad permitido.
Barandas como los statement timeouts detienen consultas descontroladas por rol. Los servicios administrados asumen buena parte de la rutina, pero el ajuste y el diseño siguen siendo tuyos.

<!-- example -->

```sql
SELECT round(100.0 * sum(blks_hit) / nullif(sum(blks_hit) + sum(blks_read), 0), 2) AS cache_hit_pct
FROM pg_stat_database;
ALTER ROLE reporting SET statement_timeout = '5min';
```

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

<!-- challenge -->

Las consultas ad hoc de los analistas a veces corren horas y frenan la aplicación. ¿Qué baranda agregas sin afectar a la app?

<!-- solution -->

Fija `statement_timeout` en el rol de los analistas (por ejemplo 5 minutos), no globalmente, y dirígelos a una réplica de lectura si necesitan consultas más largas.

<!-- takeaways -->

- Monitorea conexiones, caché, consultas lentas, bloqueos y retraso.
- Planea las actualizaciones mayores con pruebas.
- Fija timeouts por rol.

### Funciones avanzadas

<!-- unit: JSON en PostgreSQL -->

<!-- goals -->

- Elegir entre json y jsonb y consultar documentos.
- Decidir cuándo guardar JSONB en lugar de columnas.

<!-- concept -->

PostgreSQL guarda documentos de forma nativa. `jsonb` parsea una vez a una forma binaria que se puede indexar y consultar con eficiencia; `json` conserva el texto exacto. Los operadores extraen valores, prueban contención y siguen rutas, y las funciones que devuelven conjuntos convierten arrays en filas para cruzarlas.
JSONB es ideal para atributos dispersos o variables y payloads crudos. Los campos sobre los que toda consulta filtra, cruza o agrega suelen merecer columnas reales, con tipos y restricciones.

<!-- example -->

```sql
SELECT e.event_id,
       e.payload->>'type'                 AS type,
       (item->>'qty')::int                AS qty
FROM events e,
     jsonb_array_elements(e.payload->'items') AS item
WHERE e.payload @> '{"channel": "web"}';
```

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

<!-- challenge -->

Todos los reportes filtran y agregan sobre `payload->>'country'`, guardado en una columna JSONB, y las consultas son lentas. ¿Qué cambias?

<!-- solution -->

Promueve `country` a una columna real (generada desde el JSON o llenada al escribir) con un índice, ya que la usa toda consulta; deja el resto en JSONB.

<!-- takeaways -->

- Usa `jsonb` para indexar y consultar rápido.
- Los operadores extraen, prueban contención y siguen rutas.
- Promueve a columnas los campos de uso frecuente.

<!-- unit: Código en el servidor -->

<!-- goals -->

- Escribir funciones, procedimientos y triggers en PL/pgSQL.
- Elegir la volatilidad de las funciones y usar LISTEN/NOTIFY.

<!-- concept -->

Hay lógica que va junto a los datos: mantener al día `updated_at`, imponer reglas complejas, avisar de cambios a quienes escuchan. Las funciones y triggers en PL/pgSQL lo hacen. Las funciones devuelven valores y corren dentro de la transacción de quien las llama; los procedimientos pueden manejar transacciones ellos mismos.
Las etiquetas de volatilidad le dicen al planner qué puede hacer una función, lo que afecta la caché y si puede respaldar un índice. LISTEN/NOTIFY ofrece mensajería liviana entre sesiones.

<!-- example -->

```sql
CREATE FUNCTION touch_updated_at() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at := now();
  RETURN NEW;
END $$;
CREATE TRIGGER orders_touch BEFORE UPDATE ON orders
FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
```

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

<!-- challenge -->

Un índice de expresión sobre `my_normalize(name)` falla con "functions in index expression must be marked IMMUTABLE". ¿Qué significa?

<!-- solution -->

Los valores del índice nunca deben cambiar para la misma entrada, así que la función debe declararse `IMMUTABLE`. Márcala así solo si de verdad lo es (sin depender de parámetros, hora ni tablas); si no, usa una columna generada.

<!-- takeaways -->

- Las funciones devuelven valores; los procedimientos pueden hacer commit.
- Los triggers corren lógica cuando cambian filas.
- Las etiquetas de volatilidad deben ser veraces.

<!-- unit: Particionamiento -->

<!-- goals -->

- Particionar tablas por rango, lista o hash.
- Decidir cuándo vale la pena particionar.

<!-- concept -->

El particionamiento divide una tabla lógica en muchas físicas según una llave, normalmente el tiempo. Las consultas que filtran por la llave tocan solo las particiones relevantes, y los datos viejos se pueden eliminar al instante separando una partición en lugar de borrar millones de filas.
Agrega costo de planeación y reglas para llaves e índices, así que paga en tablas grandes con una llave natural de poda y un ciclo de vida, no en toda tabla grande.

<!-- example -->

```sql
CREATE TABLE events (event_id bigint, occurred_at timestamptz NOT NULL, payload jsonb)
PARTITION BY RANGE (occurred_at);
CREATE TABLE events_2026_10 PARTITION OF events
  FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
ALTER TABLE events DETACH PARTITION events_2024_10;   -- then DROP: instant retention
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

<!-- challenge -->

Una tabla de eventos de 2.000 millones de filas necesita 13 meses de retención, y el `DELETE` nocturno de filas viejas tarda horas e infla la tabla. ¿Qué propones?

<!-- solution -->

Particiona por mes sobre `occurred_at` y elimina (o separa y archiva) la partición más vieja cada mes, lo que es instantáneo y no deja tuplas muertas.

<!-- takeaways -->

- Las particiones podan por llave y simplifican la retención.
- Eliminar particiones reemplaza los borrados masivos.
- Particiona solo las tablas que se benefician.

<!-- unit: Extensiones -->

<!-- goals -->

- Usar extensiones comunes como pg_stat_statements, PostGIS y pgvector.
- Consultar datos externos con foreign data wrappers y buscar texto.

<!-- concept -->

Las extensiones son la forma en que crece PostgreSQL: un comando agrega tipos, funciones, índices o integraciones nuevos. Algunas son casi estándar, como las estadísticas de consultas; otras convierten PostgreSQL en una base geoespacial, un almacén vectorial o una puerta a otros sistemas.
La búsqueda de texto completo viene incorporada, con stemming según idioma y ranking, a menudo suficiente para evitar un motor de búsqueda aparte en necesidades moderadas.

<!-- example -->

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE doc_chunk (id bigint PRIMARY KEY, body text, embedding vector(1536));
CREATE INDEX ON doc_chunk USING hnsw (embedding vector_cosine_ops);
SELECT id, body FROM doc_chunk ORDER BY embedding <=> :query_embedding LIMIT 5;
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

<!-- challenge -->

Una app de soporte necesita "buscar artículos por palabras, con ranking, en español", y el equipo planea agregar Elasticsearch. ¿Qué puede ofrecer PostgreSQL primero?

<!-- solution -->

La búsqueda de texto completo incorporada: una columna `tsvector` con la configuración `spanish`, un índice GIN y orden por `ts_rank`. Pasa a un motor de búsqueda solo si el ajuste de relevancia o la escala lo superan.

<!-- takeaways -->

- Las extensiones agregan tipos, índices e integraciones.
- PostGIS, pgvector y los FDWs cubren necesidades especializadas.
- La búsqueda de texto incorporada cubre muchas necesidades.

<!-- unit: Funciones prácticas -->

<!-- goals -->

- Usar las funciones comunes de fecha y hora.
- Generar datos de prueba rápido en SQL.

<!-- concept -->

Un pequeño conjunto de funciones cubre casi todo el trabajo con fechas: hora actual, truncar a periodos, extraer partes, sumar intervalos y calcular edades. Usarlas en la base mantiene consistente la lógica de zonas horarias y calendario.
El mismo kit genera datos de prueba realistas: series de números o fechas combinadas con funciones aleatorias producen millones de filas en segundos, ideal para probar consultas e índices.

<!-- example -->

```sql
INSERT INTO orders (customer_id, amount, ordered_at)
SELECT (random() * 10000)::int + 1,
       round((random() * 200)::numeric, 2),
       now() - random() * interval '365 days'
FROM generate_series(1, 1000000);
SELECT date_trunc('month', ordered_at) AS month, count(*) FROM orders GROUP BY 1 ORDER BY 1;
```

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

<!-- challenge -->

Necesitas verificar si un índice nuevo ayuda a una consulta sobre 10 millones de órdenes, pero dev tiene 500 filas. ¿Cómo pruebas de forma realista en minutos?

<!-- solution -->

Genera 10 millones de filas con `generate_series` y valores aleatorios con distribuciones realistas, corre `ANALYZE` y compara `EXPLAIN ANALYZE` con y sin el índice.

<!-- takeaways -->

- `date_trunc`, `extract`, intervalos y `age` cubren casi todo con fechas.
- `generate_series` más `random()` crea datos de prueba rápido.
- Prueba el rendimiento con volúmenes realistas.
