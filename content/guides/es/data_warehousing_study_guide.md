## Guía de estudio de Data Warehousing

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de data warehousing: unas 200 preguntas](../../images/data_warehousing_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre data warehousing: conceptos clave, modelado dimensional con hechos y dimensiones, dimensiones lentamente cambiantes, patrones de carga, calidad de datos, arquitecturas y motores de warehouse, rendimiento, warehouses en la nube, BI y capa semántica, con ejemplos en SQL. Las respuestas son independientes de la herramienta cuando es posible, con notas para Snowflake, Redshift, BigQuery y Databricks. Abre una pregunta para ver su respuesta, o usa el filtro para buscar en toda la guía.

<!-- QA -->

### Conceptos clave

#### ¿Qué es un data warehouse?

Un repositorio central de datos integrados e históricos provenientes de muchas fuentes, organizado para el análisis y los reportes y no para las transacciones. La definición clásica de Bill Inmon: orientado a temas, integrado, variable en el tiempo y no volátil.

#### ¿Qué significan "orientado a temas, integrado, variable en el tiempo y no volátil"?

Orientado a temas: organizado por temas de negocio (clientes, ventas, productos) y no por aplicaciones. Integrado: nombres, códigos y unidades coherentes entre fuentes. Variable en el tiempo: conserva el historial para analizar los cambios. No volátil: los datos se cargan y se leen, no se actualizan en su lugar por transacciones.

#### ¿Qué diferencia hay entre OLTP y OLAP?

Los sistemas OLTP (procesamiento transaccional en línea) operan el negocio: muchas lecturas y escrituras pequeñas y concurrentes, esquemas normalizados, estado actual. Los sistemas OLAP (procesamiento analítico en línea) analizan el negocio: lecturas grandes y agregaciones sobre el historial, esquemas desnormalizados o dimensionales, sobre todo lecturas.

#### ¿Por qué no hacer analítica directamente sobre la base operativa?

Las consultas analíticas son pesadas y ralentizarían la aplicación; los esquemas operativos están normalizados y son difíciles de consultar; hay que combinar y limpiar datos de distintos sistemas; el historial suele sobrescribirse en los sistemas OLTP; y el control de acceso de los analistas es distinto del de la aplicación.

#### ¿Qué es un data mart?

Un subconjunto del warehouse enfocado en un área de negocio o departamento (ventas, finanzas, marketing), a menudo un conjunto de esquemas en estrella construidos para un grupo concreto de usuarios.

#### ¿Qué diferencia hay entre un data mart dependiente y uno independiente?

Un data mart dependiente se construye desde el warehouse empresarial, así que comparte definiciones con los demás marts. Uno independiente se alimenta directamente de las fuentes, lo que es más rápido de construir pero produce cifras inconsistentes entre departamentos.

#### ¿Qué es un operational data store (ODS)?

Un almacén integrado y casi en tiempo real de los datos operativos actuales de varios sistemas, usado para reportes operativos y como punto intermedio. A diferencia de un warehouse, guarda poco historial y se actualiza con frecuencia.

#### ¿Qué diferencia hay entre un data warehouse y un data lake?

Un warehouse guarda datos estructurados, modelados y curados con un esquema definido al escribir, optimizados para analítica SQL. Un data lake guarda datos en bruto de cualquier formato (estructurados, semiestructurados, no estructurados) de forma barata en almacenamiento de objetos, con esquema al leer, para ciencia de datos y usos futuros.

#### ¿Qué es un lakehouse?

Una arquitectura que añade capacidades de warehouse (transacciones ACID, esquemas, gobierno, SQL rápido) sobre el almacenamiento de un data lake usando formatos de tabla abiertos como Delta Lake e Iceberg, para que una sola copia de los datos sirva a BI, ciencia de datos y ML.

#### ¿Cuáles son las capas típicas de un data warehouse?

Staging (copias en bruto de los datos de origen), una capa de integración o núcleo (datos limpios, homogeneizados e historizados; normalizados o en Data Vault) y una capa de presentación (marts dimensionales para BI). Los stacks modernos las llaman raw/bronze, staging/silver y marts/gold.

#### ¿Qué papel cumple el área de staging?

Una zona de aterrizaje donde las extracciones de origen se guardan con cambios mínimos, para poder reiniciar, reprocesar y auditar las cargas sin volver a consultar las fuentes, y para que las transformaciones no corran contra los sistemas operativos.

#### ¿Qué son los metadatos en un warehouse?

Datos sobre los datos: metadatos técnicos (esquemas, tipos, linaje, horas de carga), de negocio (definiciones, responsables, glosario) y operativos (ejecuciones de jobs, conteos de filas, errores). Alimentan los catálogos, el análisis de impacto y la confianza.

#### ¿Qué es una única fuente de verdad?

El objetivo de que cada métrica y entidad de negocio tenga una sola definición acordada y un solo conjunto de datos autorizado, para que los reportes de los distintos departamentos coincidan. Lo apoyan las dimensiones conformadas, una capa semántica y el gobierno.

#### ¿Qué diferencia hay entre ETL y ELT?

ETL extrae los datos, los transforma en un motor aparte y luego los carga en el warehouse. ELT carga primero los datos en bruto en el warehouse y los transforma allí con SQL (a menudo con dbt), usando el cómputo escalable del warehouse. Los warehouses en la nube hicieron del ELT la opción por defecto.

#### ¿Quiénes son los principales usuarios de un data warehouse?

Analistas de negocio y desarrolladores de BI (reportes, dashboards), científicos de datos (datos de entrenamiento, exploración), equipos de finanzas y operaciones (reportes regulatorios y de gestión), directivos (KPI) y, cada vez más, aplicaciones y agentes de IA mediante APIs y capas semánticas.

#### ¿Qué es un appliance de data warehouse?

Un sistema de hardware y software preintegrado para warehousing (Teradata, Netezza, Exadata), vendido como un equipo. Los warehouses en la nube han reemplazado en gran medida a los appliances con servicios elásticos.

#### ¿Cuáles son los componentes principales de una arquitectura de warehouse?

Los sistemas de origen, las herramientas de ingesta y ETL/ELT, las capas de almacenamiento (staging, núcleo, marts), el motor de consultas, una capa semántica o de métricas, las herramientas de BI y analítica, la orquestación, la calidad y observabilidad de datos, el catálogo y el gobierno, y la seguridad.

#### ¿Qué diferencia hay entre un data warehouse y una base de datos?

Una base de datos es cualquier almacén de datos organizado; un data warehouse es un uso específico de la tecnología de bases de datos pensado para datos analíticos, integrados e históricos, normalmente con almacenamiento columnar y modelos dimensionales o por capas.

#### ¿Qué es la latencia en el contexto de un warehouse?

La demora entre un evento en un sistema de origen y su disponibilidad en los reportes: batch diario (horas), micro-lotes (minutos) o streaming (segundos). La latencia adecuada depende de las decisiones de negocio, no de la tecnología.

#### ¿Qué son los SLA de un data warehouse?

Compromisos como "el mart de ventas se actualiza antes de las 7 a. m. hora local en días hábiles" o "el 99 % de las cargas termina bien", con monitoreo y comunicación cuando se incumplen. Convierten los pipelines en productos en los que los consumidores pueden confiar.

### Fundamentos del modelado dimensional

#### ¿Qué es el modelado dimensional?

La técnica de Ralph Kimball para diseñar esquemas analíticos alrededor de los procesos de negocio: hechos (mediciones de eventos) rodeados de dimensiones (contexto descriptivo). Prioriza la comprensión y el rendimiento de las consultas sobre la normalización.

#### ¿Cuáles son los cuatro pasos del diseño dimensional de Kimball?

1) Elegir el proceso de negocio (por ejemplo la toma de pedidos). 2) Declarar el grano (qué representa una fila de hechos). 3) Identificar las dimensiones (quién, qué, dónde, cuándo, por qué, cómo). 4) Identificar los hechos (mediciones numéricas a ese grano).

#### ¿Qué es el grano de una tabla de hechos?

La definición precisa de lo que representa una sola fila, por ejemplo "una fila por línea de pedido" o "una fila por cuenta por día". Se declara antes de elegir dimensiones y hechos, y todas las filas deben tener el mismo grano.

#### ¿Por qué modelar al grano más atómico posible?

Los datos atómicos pueden responder cualquier pregunta agregando, incluso las no previstas; los hechos agregados no se pueden desglosar. Los agregados se añaden después por rendimiento.

#### ¿Qué es una tabla de hechos?

Una tabla de mediciones de un proceso de negocio, con claves foráneas hacia las dimensiones y hechos numéricos (cantidad, monto, duración). Suele ser angosta y muy larga.

#### ¿Qué es una tabla de dimensión?

Una tabla que describe el contexto de los hechos: atributos para filtrar, agrupar y etiquetar (nombre, segmento y ciudad del cliente; categoría y marca del producto; fecha, mes, indicador de festivo). Suele ser ancha y relativamente corta.

#### ¿Qué es un esquema en estrella?

Una tabla de hechos en el centro unida directamente a tablas de dimensión desnormalizadas, formando una estrella. Es fácil de entender, necesita pocos joins y rinde bien en herramientas de BI y motores columnares.

```sql
SELECT d.year_month, p.category, SUM(f.net_amount) AS revenue
FROM fct_order_lines f
JOIN dim_date d    ON f.order_date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
WHERE d.year = 2026
GROUP BY d.year_month, p.category;
```

#### ¿Qué es un esquema en copo de nieve (snowflake)?

Un esquema en estrella en el que las dimensiones se normalizan en varias tablas relacionadas (producto → subcategoría → categoría). Ahorra algo de almacenamiento y evita redundancia, pero añade joins y complejidad; Kimball suele recomendar aplanar las dimensiones.

#### ¿Qué es una clave sustituta (surrogate key)?

Una clave entera (o hash) sin significado, generada en el warehouse para identificar una fila de dimensión, independiente de las claves de los sistemas de origen. Permite el historial (varias filas por clave natural), la integración de varias fuentes y la protección frente a cambios de las claves de origen.

#### ¿Qué es una clave natural (de negocio)?

El identificador del sistema de origen o del negocio (número de cliente, SKU, número de cuenta). Se guarda como atributo de la dimensión, junto a la clave sustituta, para rastrear las filas hasta las fuentes.

#### ¿Por qué usar claves sustitutas en lugar de naturales en los hechos?

Las claves naturales pueden cambiar, reutilizarse, chocar entre fuentes o ser cadenas largas. Las claves sustitutas admiten el historial SCD tipo 2 (los hechos apuntan a la versión vigente en su momento), mantienen compactos los hechos y permiten filas especiales como "desconocido".

#### ¿Qué es una dimensión conformada?

Una dimensión compartida con las mismas claves, atributos y significado entre varias tablas de hechos y marts (un solo `dim_customer`, un solo `dim_date`), para poder comparar y combinar métricas de distintos procesos (drill-across).

#### ¿Qué es la bus matrix del data warehouse empresarial?

Una cuadrícula de planificación con los procesos de negocio como filas y las dimensiones conformadas como columnas, marcando qué dimensiones usa cada proceso. Guía el desarrollo incremental de marts que se integran mediante dimensiones conformadas.

#### ¿Qué es la dimensión de fecha y por qué es importante?

Una dimensión con una fila por día y atributos como día de la semana, mes, trimestre, periodos fiscales, festivos e indicadores de día hábil. Hace que el análisis temporal sea fácil y coherente y evita lógica de fechas compleja en cada consulta.

#### ¿Por qué la clave de la dimensión de fecha suele tener el formato AAAAMMDD?

Un entero como `20261015` es legible, ordena correctamente, hace intuitivo el descarte de particiones y se puede derivar de una fecha sin búsqueda; es una excepción común a las claves sustitutas sin significado.

#### ¿Qué preguntas ayudan a identificar las dimensiones?

Quién (cliente, empleado), qué (producto, servicio), dónde (tienda, región, canal), cuándo (fecha, hora), por qué (promoción, código de motivo) y cómo (medio de pago, modo de envío), tal como aparecen en los eventos del proceso de negocio.

#### ¿Debe una tabla de hechos tener restricciones de clave foránea?

Lógicamente sí: cada hecho debe referenciar una fila de dimensión existente (o el miembro desconocido). Físicamente, muchos warehouses no aplican las restricciones por rendimiento de carga, así que la integridad referencial se comprueba con pruebas.

#### ¿Qué es el drill-across?

Combinar medidas de distintas tablas de hechos (ventas y devoluciones) en un reporte consultando cada una por separado a un grano común de dimensiones conformadas y uniendo los resultados, en lugar de unir directamente los hechos.

#### ¿Por qué no se deben unir directamente dos tablas de hechos?

Sus granos suelen ser distintos, y los joins directos producen fan-outs y doble conteo. Agrega primero cada hecho al grano dimensional común y luego combínalos.

#### ¿Qué es una dimensión de hora del día?

Una dimensión aparte con una fila por minuto o segundo del día (hora, minuto, franja horaria), usada cuando importa el análisis por hora del día, manteniendo pequeña la dimensión de fecha.

#### ¿Cómo se nombran las tablas y columnas en un modelo dimensional?

De forma coherente y en lenguaje de negocio: prefijos `fct_` y `dim_` (o `fact_`/`dim_`), sustantivos en singular, `_key` para las claves sustitutas, `_id` para las naturales, unidades explícitas (`amount_cop`) y sin jerga de los sistemas de origen en las capas de presentación.

### Hechos en detalle

#### ¿Cuáles son los tres tipos de tablas de hechos?

Hechos transaccionales (una fila por evento, como una línea de pedido), de foto periódica (una fila por entidad por periodo, como el saldo de una cuenta por día) y de foto acumulativa (una fila por instancia de un proceso, actualizada a medida que avanza por sus hitos, como un pedido desde su creación hasta la entrega).

#### ¿Cuándo se usa una tabla de hechos de foto periódica?

Para medir niveles o estados a intervalos regulares (inventario, saldos, suscripciones activas por mes), cuando sumar las transacciones sería costoso o el estado no se puede derivar de los eventos.

#### ¿Qué es una tabla de hechos de foto acumulativa?

Una tabla de hechos con una fila por instancia de un proceso con inicio y fin definidos (preparación de pedidos, solicitud de crédito, reclamación), con varias claves de fecha para los hitos y medidas de tiempo entre ellos; las filas se actualizan a medida que ocurren los hitos.

#### ¿Qué es una tabla de hechos sin hechos (factless)?

Una tabla de hechos con solo claves de dimensión y sin medidas numéricas, que registra que ocurrió un evento (un estudiante asistió a clase) o una cobertura (qué productos estaban en promoción en qué tiendas), contada con `COUNT(*)`.

#### ¿Qué son los hechos aditivos, semiaditivos y no aditivos?

Los aditivos se pueden sumar en todas las dimensiones (monto de venta). Los semiaditivos se pueden sumar en algunas dimensiones pero no en el tiempo (saldo de cuenta: se suma entre cuentas, se promedia o se toma el último en el tiempo). Los no aditivos no se pueden sumar (razones, porcentajes, precios unitarios); guarda sus componentes.

#### ¿Cómo se deben guardar razones como el porcentaje de margen?

Guarda los componentes aditivos (ingreso y costo) en la tabla de hechos y calcula la razón al consultar (`SUM(revenue - cost) / SUM(revenue)`), porque promediar porcentajes da resultados incorrectos.

#### ¿Qué es una dimensión degenerada?

Una clave de dimensión guardada en la tabla de hechos sin tabla de dimensión propia, típicamente un identificador de transacción como el número de pedido o de factura, usado para agrupar líneas y para el drill-through.

#### ¿Cómo se manejan hechos con granos distintos?

Poniéndolos en tablas de hechos separadas; mezclar granos (montos del encabezado del pedido y de las líneas en una tabla) causa doble conteo. Asigna los valores del encabezado a las líneas solo si una regla de negocio lo respalda.

#### ¿Cuál es la clave primaria de una tabla de hechos?

A menudo la combinación de sus claves de dimensión más las dimensiones degeneradas al grano declarado, o una clave sustituta del hecho por comodidad. Es esencial comprobar con una prueba la unicidad al grano.

#### ¿Qué son las tablas de hechos agregadas?

Versiones resumidas de los hechos atómicos a un grano más grueso (ventas por mes y categoría) que aceleran las consultas comunes. Deben mantenerse coherentes con la tabla atómica, y las herramientas de BI o las capas semánticas pueden enrutar las consultas hacia ellas.

#### ¿Qué es una tabla de hechos consolidada?

Una tabla de hechos que combina hechos de varios procesos al mismo grano (montos reales y presupuestados por mes, cuenta y centro de costos), práctica para comparaciones como real frente a presupuesto.

#### ¿Qué son los hechos que llegan tarde?

Filas de hechos que llegan después de su fecha de evento (transacciones demoradas). Se deben cargar con las versiones de dimensión vigentes en el momento del evento, no con las actuales, buscando las filas SCD2 con la fecha del evento.

#### ¿Cómo se modela la moneda en las tablas de hechos?

Guardando los montos en la moneda de la transacción con una clave de moneda, más los montos convertidos a una moneda de reporte con la tasa de cambio vigente en la fecha de la transacción (de una tabla de tasas), para que los reportes muestren ambos.

#### ¿Cómo se modelan las cancelaciones y devoluciones?

Como filas negativas en el mismo hecho transaccional (sumas sencillas), o como un hecho de devoluciones aparte con su propio grano y motivos; las fotos acumulativas pueden seguir los cambios de estado de los pedidos.

#### ¿Qué es la "dimensión de auditoría" de una tabla de hechos?

Una dimensión o un conjunto de columnas que describe cómo se cargó cada fila de hechos (ID de lote, hora de carga, archivo de origen, estado de calidad), útil para la depuración y el linaje.

#### ¿Qué tan grandes pueden ser las tablas de hechos y cómo se manejan?

Miles de millones de filas son comunes. Se manejan con particionado por fecha, clustering por los filtros habituales, compresión, cargas incrementales, políticas de retención y agregados para las consultas frecuentes.

#### ¿Cuándo usar una foto periódica en lugar de derivar el estado de las transacciones?

Cuando calcular el estado a partir de todas las transacciones históricas es costoso o complejo (saldos, niveles de inventario, tickets abiertos), o cuando los sistemas de origen dan los estados pero no historiales completos de eventos.

### Dimensiones en detalle

#### ¿Qué es una dimensión de rol (role-playing)?

Una dimensión física usada varias veces en una tabla de hechos con significados distintos, típicamente la dimensión de fecha como fecha de pedido, de envío y de entrega, expuesta mediante vistas o alias.

#### ¿Qué es una junk dimension?

Una dimensión que combina varios indicadores y banderas de baja cardinalidad (tipo de pago, envoltura de regalo, canal) en una tabla con sus combinaciones, evitando muchas dimensiones diminutas o tablas de hechos demasiado anchas.

#### ¿Qué es una minidimensión?

Una dimensión aparte para los atributos que cambian rápido en una dimensión grande (rango de edad, de ingresos o de puntaje crediticio del cliente), para que la dimensión principal no explote con filas SCD2; la tabla de hechos referencia a ambas.

#### ¿Qué es una dimensión outrigger?

Una dimensión referenciada por otra dimensión en lugar de por la tabla de hechos (por ejemplo la fecha de primera compra de un cliente que apunta a la dimensión de fecha). Se permite con moderación; demasiadas se convierten en copo de nieve.

#### ¿Qué es una tabla puente (bridge)?

Una tabla que resuelve relaciones muchos a muchos entre hechos y dimensiones, como cuentas con varios titulares o varios diagnósticos por consulta médica, a menudo con factores de ponderación para no contar dos veces los montos.

#### ¿Cómo se modelan las jerarquías en las dimensiones?

Las jerarquías de profundidad fija (categoría → subcategoría → producto) como columnas aplanadas de la dimensión. Las jerarquías irregulares o de profundidad variable (organigramas, listas de materiales) con claves padre-hijo más una tabla puente con todos los pares ancestro-descendiente para agregar fácilmente.

#### ¿Qué es la fila de "miembro desconocido"?

Una fila especial de la dimensión (a menudo con clave sustituta `-1` o `0`) que se usa cuando falta la dimensión de un hecho o aún no se conoce, para que los hechos no se pierdan en los inner joins y el problema sea visible en los reportes.

#### ¿Qué es una dimensión reducida (shrunken)?

Un subconjunto de las filas o columnas de una dimensión usado para hechos agregados a un grano mayor, como una dimensión de mes derivada de la de fecha o una de categoría derivada de la de productos.

#### ¿Qué es una dimensión lentamente cambiante?

Una dimensión cuyos atributos cambian con el tiempo de forma impredecible (un cliente se muda, un producto cambia de categoría), lo que exige una política sobre si conservar el historial y cómo.

#### ¿Qué es una dimensión estática?

Una dimensión cuyo contenido no viene de una fuente y casi no cambia, como la dimensión de fecha, las tablas de códigos de estado o las monedas, generada una vez o mantenida a mano.

#### ¿Qué es un atributo "tipo 1" en una dimensión mixta?

Las dimensiones pueden mezclar políticas por atributo: algunas columnas se sobrescriben (tipo 1, correcciones) y otras se historizan (tipo 2, cambios relevantes). Se decide atributo por atributo con los usuarios de negocio.

#### ¿Cómo se manejan los datos de clientes que vienen de varios sistemas?

Emparejando y fusionando los registros en una dimensión de cliente conformada con una clave maestra (de la gestión de datos maestros o de reglas de coincidencia sobre correos, documentos, nombres), conservando las claves de origen como atributos o en una tabla de mapeo, y definiendo reglas de supervivencia para los atributos en conflicto.

#### ¿Qué es la gestión de datos maestros (MDM)?

Procesos y herramientas que crean y mantienen una versión única y autorizada de las entidades principales (clientes, productos, proveedores) entre sistemas, que alimenta las dimensiones conformadas.

#### ¿Qué es un "atributo conformado"?

Un atributo con el mismo nombre, significado y valores permitidos en todos los lugares donde aparece, como un código de país estándar o una lista de categorías de producto, que permite filtrar de forma coherente entre marts.

#### ¿Cómo se manejan los atributos multivaluados como los intereses de un cliente?

Con una tabla puente entre la dimensión y una dimensión de grupo o de atributo, o guardando una columna de arreglo donde el motor lo admita y las consultas puedan desplegarla; evita codificar varios valores en una cadena separada por comas.

#### ¿Qué es una "vista actual" de una dimensión SCD2?

Una vista que filtra `is_current = true` y da una fila por clave natural con los atributos de hoy, usada por los analistas que no necesitan el historial y para reportes de estilo tipo 1.

### Dimensiones lentamente cambiantes

#### ¿Cuáles son los tipos de SCD?

Tipo 0: nunca cambia (se conserva el original). Tipo 1: sobrescribir, sin historial. Tipo 2: una fila nueva por cambio con fechas de vigencia. Tipo 3: una columna con el "valor anterior". Tipo 4: el historial en una tabla aparte (minidimensión o tabla de historial). Tipo 6: híbrido de 1, 2 y 3 (columnas de valor actual en todas las filas más filas de historial). Tipo 7: doble clave para unir con las filas actuales o las históricas.

#### ¿Cómo funciona la SCD tipo 2?

Cuando cambia un atributo seguido, se cierra la fila vigente (se llena la fecha de fin y el indicador de vigencia pasa a falso) y se inserta una fila nueva con una nueva clave sustituta, los valores nuevos, una fecha de inicio y una fecha de fin abierta. Los hechos referencian la clave sustituta vigente cuando ocurrieron.

| customer_key | customer_id | city     | valid_from | valid_to   | is_current |
|---|---|---|---|---|---|
| 101 | C-42 | Bogotá   | 2024-01-01 | 2026-03-31 | false |
| 187 | C-42 | Medellín | 2026-04-01 | 9999-12-31 | true  |

#### ¿Cómo se implementa una SCD tipo 2 con SQL?

Detectando las filas que cambiaron al comparar un hash de los atributos seguidos entre staging y las filas vigentes de la dimensión, cerrando las filas cambiadas e insertando las nuevas versiones (más las claves completamente nuevas). Muchas plataformas lo hacen en un solo `MERGE` con el truco de la unión, o con herramientas como los snapshots de dbt.

```sql
-- 1) cerrar las filas cuyos atributos seguidos cambiaron
UPDATE dim_customer d
SET valid_to = CURRENT_DATE - 1, is_current = false
FROM stg_customer s
WHERE d.customer_id = s.customer_id AND d.is_current
  AND d.attr_hash <> s.attr_hash;

-- 2) insertar las nuevas versiones y los clientes nuevos
INSERT INTO dim_customer (customer_id, city, segment, attr_hash, valid_from, valid_to, is_current)
SELECT s.customer_id, s.city, s.segment, s.attr_hash, CURRENT_DATE, DATE '9999-12-31', true
FROM stg_customer s
LEFT JOIN dim_customer d ON d.customer_id = s.customer_id AND d.is_current
WHERE d.customer_id IS NULL;
```

#### ¿Por qué usar una fecha de fin 9999-12-31 en lugar de NULL?

Simplifica las consultas "vigente en la fecha X" con `BETWEEN` y evita manejar `NULL` en los joins; algunos equipos prefieren `NULL` más un indicador de vigencia. Lo importante es ser coherente.

#### ¿Cómo se unen los hechos a una dimensión SCD2 para una búsqueda en un momento dado?

Al cargar los hechos, se busca la fila de la dimensión cuyo rango de vigencia contiene la fecha del evento: `ON f.customer_id = d.customer_id AND f.event_date >= d.valid_from AND f.event_date < d.valid_to`, y se guarda esa clave sustituta en el hecho.

#### ¿Qué es la SCD tipo 1 y cuándo es apropiada?

Sobrescribir los atributos con los valores nuevos, perdiendo el historial. Es apropiada para correcciones (arreglar un error tipográfico) y para atributos cuyo historial no importa en el análisis.

#### ¿Qué es la SCD tipo 3 y por qué es poco común?

Añadir una columna con el valor anterior (`previous_region`) para comparar la asignación actual con la anterior. Solo guarda un nivel de historial, así que se limita a análisis concretos de reorganizaciones.

#### ¿Qué es la SCD tipo 6?

Un híbrido en el que la dimensión guarda filas de historial tipo 2 y además columnas "actuales" tipo 1 actualizadas en todas las filas de la misma clave natural, para reportar los hechos tanto como eran como con los valores de hoy.

#### ¿Qué problemas causa la SCD2 en dimensiones grandes?

Explosión de filas cuando los atributos cambian seguido, joins más lentos y lógica compleja por fecha. Mitigaciones: seguir solo los atributos relevantes, mover los atributos volátiles a minidimensiones y usar comparaciones por hash para detectar cambios.

#### ¿Cómo se maneja un cambio de dimensión que llega tarde?

Si hoy te enteras de que un cambio ocurrió el mes pasado, insertas la versión con su fecha de inicio real, ajustas la fecha de fin de la fila anterior y, posiblemente, reasignas a la nueva clave sustituta los hechos ocurridos después del cambio; por eso algunos equipos prefieren hacer los joins por fecha al consultar.

#### ¿Qué es un hash diff y por qué usarlo?

Un hash (MD5, SHA) de los atributos seguidos concatenados, guardado en cada fila, para que detectar cambios sea una sola comparación en lugar de comparar muchas columnas, incluido el manejo seguro de los nulos.

#### ¿Cómo implementan la SCD2 los snapshots de dbt?

La configuración del snapshot define la clave única y una estrategia (`timestamp`, con una columna de fecha de actualización, o `check`, comparando columnas); cada ejecución compara el origen con la tabla de snapshot y cierra e inserta filas, añadiendo `dbt_valid_from` y `dbt_valid_to`.

#### ¿Cómo se prueba una dimensión SCD2?

Comprobando que cada clave natural tenga exactamente una fila vigente, que los rangos de vigencia no se solapen ni dejen huecos, que `valid_from < valid_to`, que las claves sustitutas sean únicas y que las claves sustitutas de los hechos existan en la dimensión.

#### ¿Qué es una SCD2 con marca de tiempo frente a granularidad diaria?

Algunas dimensiones siguen los cambios con precisión de marca de tiempo (varios cambios al día), otras a nivel de día (el último valor del día). Elige según cómo se emparejan los hechos; la granularidad diaria es más simple y suele bastar.

#### ¿Se pueden reasignar los hechos a nuevas versiones de la dimensión?

Normalmente no: los hechos conservan la versión vigente cuando ocurrieron. Para reportar "a la fecha de hoy", une por la clave natural con la fila vigente o usa las columnas de valor actual del tipo 6.

### Carga del warehouse

#### ¿Qué es una carga completa frente a una incremental?

Una carga completa vuelve a cargar todos los datos en cada ejecución (simple, costosa, adecuada para tablas pequeñas). Una carga incremental procesa solo los datos nuevos o modificados desde la última ejecución (por fecha, secuencia o CDC), lo que es necesario en tablas grandes.

#### ¿Qué es la captura de cambios (CDC)?

Capturar las inserciones, actualizaciones y borrados de una base de origen, típicamente leyendo su log de transacciones (binlog, WAL, redo log) con herramientas como Debezium, DMS, GoldenGate o Fivetran, y aplicarlos al warehouse.

#### ¿Por qué se prefiere el CDC basado en logs a la extracción por fecha de actualización?

Captura todos los cambios, incluidos los borrados, no depende de que las aplicaciones mantengan bien `updated_at`, carga poco el origen y conserva el orden de los cambios.

#### ¿Cómo se carga una dimensión?

Extrayendo y limpiando los registros de origen, deduplicando por clave natural, generando o buscando las claves sustitutas, aplicando la política SCD por atributo, añadiendo el miembro desconocido y ejecutando pruebas de unicidad de las claves naturales vigentes.

#### ¿Cómo se carga una tabla de hechos?

Extrayendo las transacciones al grano declarado, buscando las claves sustitutas de las dimensiones (por fecha para SCD2, miembro desconocido si falta), calculando las medidas derivadas, e insertando o haciendo merge de forma idempotente en la tabla de hechos, normalmente particionada por fecha.

#### ¿En qué orden se carga un warehouse?

Primero las dimensiones y luego los hechos, para que los hechos encuentren sus claves sustitutas. Los miembros de dimensión que llegan tarde se manejan con miembros inferidos o filas desconocidas y se corrigen después.

#### ¿Qué es un miembro inferido?

Una fila provisional de dimensión creada cuando llega un hecho con una clave natural que aún no existe en la dimensión, con la clave natural y atributos por defecto, que se actualiza cuando llegan los datos reales.

#### ¿Cómo se hacen idempotentes las cargas del warehouse?

Procesando rangos de fechas explícitos, borrando y reinsertando las particiones afectadas o usando `MERGE` por clave, evitando los appends a ciegas, usando claves sustitutas deterministas o búsquedas estables, y diseñando los jobs para que reejecutarlos dé el mismo resultado.

#### ¿Qué es un upsert y cómo se hace?

Insertar las filas nuevas y actualizar las existentes en una sola operación, típicamente con `MERGE` (Snowflake, BigQuery, Databricks, SQL Server, Postgres 15+) o con `INSERT … ON CONFLICT DO UPDATE` (PostgreSQL).

```sql
MERGE INTO fct_orders t
USING stg_orders s ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET status = s.status, amount = s.amount, updated_at = s.updated_at
WHEN NOT MATCHED THEN INSERT (order_id, customer_key, status, amount, updated_at)
  VALUES (s.order_id, s.customer_key, s.status, s.amount, s.updated_at);
```

#### ¿Cómo se manejan los borrados de las fuentes?

Con los eventos de borrado del CDC o comparando extracciones completas para encontrar las claves que faltan; después se borra físicamente, o se hace un borrado lógico con un indicador `is_deleted` y la fecha de borrado para conservar el historial, según las necesidades de negocio y de cumplimiento.

#### ¿Qué es una marca de agua (watermark) en la carga incremental?

El valor más alto de fecha o secuencia procesado en la última ejecución, guardado en una tabla de control y usado para seleccionar las filas nuevas la próxima vez; usa una ventana de solapamiento para captar las filas confirmadas tarde y deduplica.

#### ¿Qué es un backfill?

Reprocesar periodos históricos, por ejemplo tras corregir un error o añadir una columna. Los pipelines deben aceptar rangos de fechas como parámetros y escribir de forma idempotente para que los backfills sean seguros.

#### ¿Qué son los controles de conciliación?

Comparaciones entre el origen y el warehouse (conteos de filas, sumas de montos, claves distintas por día) para demostrar que las cargas están completas y son correctas, a menudo ejecutadas automáticamente después de cada carga.

#### ¿Qué es una tabla de control en ETL?

Una tabla que guarda los metadatos de cada ejecución de un pipeline: marcas de agua, IDs de lote, horas de inicio y fin, conteos de filas, estado y errores, usada para la carga incremental, los reinicios y el monitoreo.

#### ¿Qué diferencia hay entre la ingesta push y pull?

Pull: el lado del warehouse extrae de las fuentes según una programación (consultas, APIs). Push: las fuentes envían los datos como eventos o archivos (flujos de CDC, webhooks, archivos depositados). El push reduce la latencia y la carga sobre las fuentes; el pull es más fácil de controlar.

#### ¿Cómo se cargan datos de aplicaciones SaaS?

Con conectores administrados (Fivetran, Airbyte, Lakeflow Connect, AppFlow) o con extracción propia por API que maneje la paginación, los límites de solicitudes, los cursores incrementales y los cambios de esquema, dejando el JSON en bruto antes de modelar.

#### ¿Para qué se usan herramientas ELT como dbt?

Para escribir las transformaciones como modelos SQL versionados con dependencias, pruebas, documentación y entornos, compilados y ejecutados dentro del warehouse, llevando las prácticas de ingeniería de software a la capa de transformación.

#### ¿Cómo se manejan los cambios de esquema en las fuentes?

Detectándolos (controles de esquema, contratos, alertas), aterrizando los datos en bruto de forma flexible (`VARIANT`, JSON, evolución del esquema), seleccionando columnas explícitamente en staging, decidiendo en cada caso si se propaga el cambio y comunicando los cambios que rompen.

#### ¿Qué es la carga por micro-lotes?

Cargar lotes pequeños cada pocos minutos (en lugar de una vez al día), equilibrando latencia y eficiencia; Snowpipe, Auto Loader, los triggers de Structured Streaming y los jobs de `MERGE` programados la implementan.

### Calidad de datos

#### ¿Cuáles son las dimensiones de la calidad de datos?

Completitud (no faltan datos), exactitud (valores correctos), coherencia (mismos valores entre sistemas), validez (cumple formatos y reglas), unicidad (sin duplicados), oportunidad (lo bastante frescos) e integridad (las relaciones se cumplen).

#### ¿Qué pruebas debería tener toda tabla del warehouse?

Unicidad y no nulidad de la clave primaria al grano, integridad referencial de los hechos hacia las dimensiones, valores aceptados para los códigos de estado, frescura de la última carga, umbrales o anomalías en el número de filas, y conciliación con las fuentes en las tablas críticas.

#### ¿Dónde deben correr los controles de calidad de datos?

En la ingesta (controles de esquema y formato), después de las transformaciones (reglas de negocio e integridad) y antes de publicar a los consumidores (barreras que impiden que los datos malos lleguen a los dashboards), guardando los resultados para analizar tendencias.

#### ¿Qué debe pasar cuando falla un control de calidad?

Depende de la gravedad: bloquear la publicación y alertar al responsable en los controles críticos, poner en cuarentena las filas malas y continuar en los problemas a nivel de fila, o advertir y registrar en los problemas menores. Hay que informar a los consumidores cuando los datos se retrasan o están mal.

#### ¿Qué herramientas se usan para la calidad de datos en el warehouse?

Las pruebas y paquetes de dbt (dbt_utils, dbt_expectations), Great Expectations, Soda, Monte Carlo y otras herramientas de observabilidad, las expectativas de Databricks, las data metric functions de Snowflake y controles SQL propios en los orquestadores.

#### ¿Qué es la observabilidad de datos?

Monitorear los sistemas de datos en cuanto a frescura, volumen, cambios de esquema, cambios de distribución y linaje, a menudo con detección automática de anomalías, para encontrar los incidentes de datos antes que los usuarios.

#### ¿Qué es un contrato de datos?

Un acuerdo entre un productor de datos y sus consumidores sobre el esquema, la semántica, la calidad y los SLA de un dataset, aplicado en CI y en los pipelines para detectar pronto los cambios que rompen.

#### ¿Qué es un SLA de calidad de datos?

Un compromiso sobre una calidad medible (por ejemplo "menos del 0,1 % de pedidos sin cliente", "datos con menos de 2 horas de antigüedad"), monitoreado automáticamente e informado a los consumidores.

#### ¿Cómo se cuantifica el impacto de negocio de los datos malos?

Rastreando los incidentes hasta las decisiones afectadas (facturas erróneas, metas mal medidas), el tiempo dedicado a corregir y la confianza perdida; esto ayuda a priorizar las inversiones en calidad sobre los datasets críticos.

#### ¿Qué son los controles de detección de anomalías?

Controles estadísticos que comparan las métricas de hoy (conteos de filas, sumas, tasas de nulos) con los patrones históricos y señalan las desviaciones inusuales incluso sin umbrales explícitos.

#### ¿Qué papel cumple un data steward?

Un responsable del lado del negocio que se encarga de las definiciones, las reglas de calidad y la resolución de incidencias de un dominio de datos, junto con los ingenieros de datos que implementan los controles.

### Arquitecturas de warehouse

#### ¿Qué es el enfoque de Inmon?

Un enfoque de arriba hacia abajo: construir un warehouse empresarial normalizado (3FN) como núcleo integrado (la Corporate Information Factory) y luego derivar data marts dependientes para los departamentos. Prioriza la integración y la coherencia, pero tarda más en entregar valor.

#### ¿Qué es el enfoque de Kimball?

Un enfoque de abajo hacia arriba: construir data marts dimensionales por proceso de negocio, integrados mediante dimensiones conformadas y la bus matrix, entregando valor de forma incremental. La unión de los marts es el warehouse.

#### Inmon o Kimball: ¿cómo eliges?

Kimball para entregar más rápido con modelos fáciles para el negocio; Inmon (o Data Vault) para un núcleo muy integrado y auditable en empresas complejas con muchas fuentes. Muchas organizaciones los combinan: un núcleo normalizado o en Data Vault con marts de Kimball encima.

#### ¿Qué es Data Vault?

Un método de modelado de Dan Linstedt para la capa de integración: hubs (claves de negocio), links (relaciones entre hubs) y satellites (atributos descriptivos con historial). Es de solo inserción, auditable y se adapta bien a los cambios de las fuentes, con marts construidos encima para el consumo.

#### ¿Cuáles son las ventajas y desventajas de Data Vault?

Ventajas: auditabilidad, historial completo, carga en paralelo, resiliencia a los cambios de las fuentes, facilidad para añadir fuentes. Desventajas: muchas tablas y joins, no lo usan directamente los analistas (necesita marts) y es más complejo de implementar y consultar sin automatización.

#### ¿Qué relación tiene la arquitectura medallion con el warehousing?

Es un patrón de lakehouse por capas (bronze en bruto, silver limpio y homogeneizado, gold listo para el negocio) que corresponde a las capas de staging, integración y presentación; gold suele contener esquemas en estrella de Kimball.

#### ¿Qué es una capa semántica?

Una capa que define una sola vez las métricas, dimensiones y relaciones de negocio (en la capa semántica de dbt, LookML, Cube, los modelos semánticos de Power BI, AtScale, las metric views) para que todas las herramientas calculen "ingresos" de la misma forma.

#### ¿Qué es un cubo OLAP?

Una estructura multidimensional que precalcula agregados entre dimensiones para cortar y rebanar rápido. MOLAP guarda los cubos en un almacenamiento especializado (SSAS), ROLAP consulta tablas relacionales y HOLAP mezcla ambos. Los warehouses columnares en la nube redujeron la necesidad de cubos físicos.

#### ¿Qué es un data warehouse virtual o la virtualización de datos?

Consultar datos de varias fuentes en su lugar mediante una capa de virtualización (Denodo, Trino, consultas federadas) sin consolidarlos físicamente. Es rápido para integrar, pero el rendimiento y el historial son limitados.

#### ¿Qué es un data warehouse en tiempo real o de streaming?

Un warehouse alimentado de forma continua (Snowpipe Streaming, streaming de BigQuery, conectores de Kafka, CDC) con transformaciones de baja latencia (dynamic tables, vistas materializadas, streaming tables), para analítica operativa que necesita datos en segundos o minutos.

#### ¿Qué es una arquitectura hub-and-spoke?

Un warehouse empresarial central (hub) que alimenta data marts departamentales (spokes), la topología clásica de estilo Inmon.

#### ¿Qué es una arquitectura federada?

Varios warehouses o marts mantenidos por distintas unidades de negocio, integrados mediante estándares compartidos, dimensiones conformadas o virtualización en lugar de un único almacén central; se relaciona con las ideas del data mesh.

#### ¿Qué es un "persistent staging area"?

Una capa de staging que conserva todas las extracciones históricas (a menudo de solo inserción con marcas de carga) en lugar de vaciarse en cada ejecución, lo que permite reconstruir las capas posteriores sin volver a extraer de las fuentes.

#### ¿Qué son el "raw vault" y el "business vault" en Data Vault?

El raw vault guarda los datos de origen tal cual en hubs, links y satellites; el business vault añade estructuras derivadas con reglas de negocio (satellites calculados, tablas point-in-time y bridge) para simplificar la construcción de los marts.

#### ¿Qué son las tablas point-in-time (PIT) en Data Vault?

Tablas auxiliares que guardan, para cada clave de hub y fecha de foto, las fechas de carga de los satellites correspondientes, lo que agiliza armar el estado de una entidad en un momento dado para las dimensiones.

### Motores y almacenamiento

#### ¿Qué es MPP?

Massively parallel processing: una base reparte los datos entre muchos nodos, cada uno con su CPU, memoria y almacenamiento (o caché), ejecuta las consultas en paralelo y combina los resultados. Redshift, Teradata, Synapse y Vertica son MPP; Snowflake y BigQuery son variantes en la nube.

#### ¿Por qué las bases analíticas son columnares?

Las consultas analíticas leen pocas columnas de muchas filas; guardar cada columna de forma contigua permite leer solo las columnas necesarias, comprimir muy bien los valores parecidos y procesarlos con ejecución vectorizada.

#### ¿Qué diferencia hay entre el almacenamiento por filas y por columnas?

El almacenamiento por filas guarda juntas todas las columnas de una fila, eficiente para leer y escribir registros completos (OLTP). El columnar guarda juntos los valores de cada columna, eficiente para lecturas y agregaciones sobre pocas columnas (OLAP).

#### ¿Qué es una clave de distribución (Redshift, Synapse)?

La columna usada para repartir las filas entre los nodos. Distribuir dos tablas grandes por su clave de join coloca juntas las filas que coinciden y evita la redistribución en los joins; las dimensiones pequeñas se pueden replicar (`ALL`) en todos los nodos; `EVEN` o `AUTO` reparten las filas de forma uniforme.

#### ¿Qué es una sort key (Redshift) o clave de clustering?

Un orden de los datos dentro del almacenamiento para que los filtros por rango puedan saltar bloques usando los metadatos de mínimo y máximo (zone maps). Conceptos equivalentes: las clustering keys de Snowflake, el clustering de BigQuery, el liquid clustering o Z-order de Delta.

#### ¿Qué es el particionado en un warehouse?

Dividir una tabla grande por una columna (normalmente la fecha) para que las consultas que filtran por ella solo lean las particiones relevantes y el mantenimiento (borrar datos viejos, recargar un día) sea barato. BigQuery usa particionado explícito; Snowflake usa micro-particiones automáticas.

#### ¿Qué son los zone maps o estadísticas de mínimo y máximo?

Metadatos que guardan los valores mínimo y máximo por bloque o archivo, usados para saltar los bloques que no pueden cumplir un filtro. Los datos ordenados o agrupados por la columna del filtro los hacen eficaces.

#### ¿Qué es una vista materializada?

El resultado guardado de una consulta, refrescado automática o periódicamente. Acelera las agregaciones o joins repetidos; el motor puede usarla de forma transparente. Su mantenimiento cuesta cómputo.

#### ¿Qué es la gestión de cargas de trabajo (workload management)?

Controlar cómo comparten recursos las consultas: colas, prioridades, límites de concurrencia, clusters o warehouses separados para ETL y BI, y timeouts, para que los jobs pesados no dejen sin recursos a los usuarios interactivos.

#### ¿Qué es la separación de almacenamiento y cómputo?

Guardar los datos en un almacenamiento compartido (de objetos) y ejecutar encima clusters de cómputo independientes y elásticos, para escalar y pagar cada uno por separado y aislar las cargas. Snowflake, BigQuery, Databricks y Redshift RA3/Serverless usan este modelo.

#### ¿Qué es la ejecución vectorizada?

Procesar lotes de valores de columna a la vez con bucles eficientes para la CPU e instrucciones SIMD, en lugar de fila por fila, lo que acelera mucho las lecturas, los filtros y las agregaciones en los motores columnares.

#### ¿Qué son los cachés de resultados?

Almacenes de resultados de consultas anteriores que se devuelven al instante cuando la misma consulta se ejecuta sobre datos sin cambios (caché de resultados de Snowflake, resultados en caché de BigQuery), ahorrando cómputo en los dashboards.

#### ¿Qué papel cumplen las estadísticas en la optimización de consultas?

Los conteos de filas, valores distintos, mínimos/máximos e histogramas permiten al optimizador estimar cardinalidades y elegir el orden y la estrategia de los joins; las estadísticas desactualizadas causan malos planes.

#### ¿Qué es la codificación de compresión en los almacenes columnares?

Técnicas como la codificación por diccionario, run-length, delta y bit-packing que reducen las columnas con valores repetidos u ordenados; los datos ordenados comprimen mejor.

#### ¿Qué diferencia hay entre escalar hacia arriba y hacia afuera en los warehouses?

Escalar hacia arriba da más recursos a una consulta (warehouse más grande, más slots) para que termine antes; escalar hacia afuera añade clusters para atender más consultas concurrentes. Elige según si el problema es la latencia de una consulta o la concurrencia.

### Rendimiento

#### ¿Cómo se hace rápida una consulta sobre un esquema en estrella?

Filtrando por columnas particionadas o agrupadas (la fecha), uniendo los hechos con dimensiones pequeñas (broadcast), seleccionando solo las columnas necesarias, preagregando las consultas comunes, manteniendo al día las estadísticas y evitando funciones sobre las columnas de filtro.

#### ¿Qué causa el "fan-out" o doble conteo en los joins?

Unir un hecho con una tabla que tiene varias filas por clave (muchos a muchos o un grano equivocado), de modo que cada fila de hecho se duplica y las sumas se inflan. Revisa la cardinalidad de los joins y exige la unicidad de las claves de las dimensiones.

#### ¿Cómo se acelera `COUNT(DISTINCT)` sobre muchos datos?

Usando funciones aproximadas (HyperLogLog: `APPROX_COUNT_DISTINCT`), preagregando los conjuntos distintos por periodo, o manteniendo los conteos distintos en tablas agregadas cuando se necesitan valores exactos.

#### ¿Por qué las tablas anchas desnormalizadas pueden ser rápidas en motores columnares?

Porque solo se leen las columnas que referencia la consulta, así que una tabla ancha no cuesta más que una angosta con las mismas filas, y evita joins. Los costos son el almacenamiento, el mantenimiento y la posible incoherencia.

#### ¿Qué es el descarte (pruning) en las consultas y cómo se comprueba?

Saltarse las particiones, archivos o bloques que no pueden cumplir los filtros de la consulta. Se comprueba en los perfiles o planes de consulta (particiones leídas frente al total, bytes escaneados) y se corrigen los filtros o la organización de los datos cuando no ocurre.

#### ¿Cómo se optimiza un dashboard lento?

Encontrando las consultas lentas, revisando el pruning y los joins, añadiendo agregados o vistas materializadas al grano del dashboard, usando las extracciones o el caché de la herramienta de BI, limitando los rangos de fechas por defecto y quitando visuales innecesarios que lanzan consultas.

#### ¿Qué impacto tienen los tipos de datos en el rendimiento del warehouse?

Los tipos más pequeños (enteros en lugar de cadenas para las claves, `DATE` en lugar de `TIMESTAMP` cuando basta, `DECIMAL` con la precisión adecuada) comprimen mejor y se comparan más rápido; unir por tipos distintos obliga a conversiones e impide optimizaciones.

#### ¿Cómo se manejan dimensiones muy grandes (cientos de millones de filas)?

Particionando o agrupando por rangos de clave natural, minimizando la rotación SCD2 con minidimensiones, evitando atributos innecesarios, usando claves sustitutas enteras y preguntándose si la "dimensión" no es en realidad una entidad parecida a un hecho.

#### ¿Qué es un agregado "que cubre" (covering)?

Una tabla agregada que contiene todas las columnas que necesita una consulta frecuente al grano correcto, para que la consulta nunca toque la tabla de hechos atómica.

#### ¿Cómo se evitan los `SELECT DISTINCT` costosos en los modelos?

Buscando por qué aparecen los duplicados (un join con el grano equivocado) y corrigiendo el join en lugar de ocultarlo con `DISTINCT`, que es costoso y esconde problemas de datos.

#### ¿Cómo se prueba el rendimiento del warehouse antes de salir a producción?

Reproduciendo consultas representativas y la concurrencia sobre datos del tamaño de producción, midiendo la latencia y el costo por consulta, revisando los planes en cuanto a pruning y joins, y ajustando la organización, los agregados y el tamaño del warehouse.

#### ¿Cómo pueden los modelos incrementales reducir los costos del warehouse?

Transformando en cada ejecución solo los datos nuevos o modificados en lugar de reconstruir tablas completas, lo que reduce drásticamente el cómputo en los hechos grandes; requieren un manejo cuidadoso de los datos tardíos y de los backfills.

### Warehouses en la nube

#### ¿Cuáles son los principales warehouses en la nube?

Snowflake, Google BigQuery, Amazon Redshift (aprovisionado y Serverless), los warehouses de Azure Synapse y Microsoft Fabric, y Databricks SQL sobre el lakehouse. Se diferencian en arquitectura, modelos de precios e integración con el ecosistema.

#### ¿Cómo funciona BigQuery y cómo se cobra?

BigQuery es serverless: el almacenamiento está en un formato columnar (Capacitor) sobre Colossus y el cómputo se asigna como slots de Dremel. Se cobra bajo demanda por TB escaneado o por capacidad (ediciones con slots reservados o con autoescalado), más el almacenamiento.

#### ¿Cómo funciona Amazon Redshift?

Un warehouse MPP con un nodo líder y nodos de cómputo; los nodos RA3 separan el almacenamiento administrado (respaldado en S3) del cómputo, Serverless se cobra por RPU-hora, y entre sus funciones están las claves de distribución y de orden (con ajuste automático), las vistas materializadas, Spectrum para datos en S3, el uso compartido de datos y las integraciones zero-ETL.

#### ¿Cómo cobran los warehouses en la nube y qué impulsa los costos?

El cómputo (créditos, slots, RPU, DBU) suele dominar, luego el almacenamiento, la transferencia de datos y las funciones serverless. Los costos crecen con consultas ineficientes, cómputo siempre encendido, refrescos completos y muchos usuarios lanzando consultas sin filtrar; el gobierno y el monitoreo son esenciales.

#### ¿Cómo se elige un warehouse en la nube?

Teniendo en cuenta la nube y el ecosistema existentes, los patrones de carga (estable o irregular, concurrencia), las habilidades del equipo, las necesidades de gobierno, los formatos abiertos y la estrategia de lakehouse, el encaje del modelo de precios, las necesidades de compartir datos y la tolerancia a la dependencia de un proveedor. Prueba con consultas reales antes de comprometerte.

#### ¿Qué es el uso compartido de datos zero-copy?

Compartir datos vivos entre cuentas u organizaciones sin copiarlos (Secure Data Sharing de Snowflake, Analytics Hub de BigQuery, data sharing de Redshift, Delta Sharing), para que los consumidores consulten los datos del proveedor con su propio cómputo.

#### ¿Qué implican los formatos de tabla abiertos para los warehouses?

Iceberg y Delta permiten que varios motores (warehouse, Spark, Trino) trabajen sobre los mismos datos en almacenamiento de objetos, reduciendo la dependencia y las copias. Los warehouses los leen y escriben cada vez más de forma nativa.

#### ¿Cómo maneja BigQuery el particionado y el clustering?

Las tablas se pueden particionar por una columna de fecha/marca de tiempo, por tiempo de ingesta o por rango de enteros, y agrupar por hasta cuatro columnas; las consultas que filtran por ellas leen menos bytes, lo que reduce directamente el costo bajo demanda.

#### ¿Qué es Redshift Spectrum?

Una función que permite a Redshift consultar datos en S3 mediante tablas externas del Glue Data Catalog, uniendo datos del lake con tablas del warehouse, facturada por bytes escaneados.

#### ¿Qué es el warehouse de Microsoft Fabric?

Una plataforma analítica SaaS en la que los warehouses y lakehouses guardan los datos en formato Delta en OneLake, se consultan con T-SQL y Spark, y se sirven a Power BI con el modo Direct Lake.

#### ¿Qué es Databricks SQL como warehouse?

SQL warehouses sobre el lakehouse de Databricks que consultan tablas Delta gobernadas por Unity Catalog, con Photon, cómputo serverless y conectores de BI, que ofrecen funciones de warehouse sobre almacenamiento abierto.

### BI y consumo

#### ¿Qué hace que un modelo de datos sea fácil para BI?

Esquemas en estrella con nombres claros, definiciones de negocio documentadas, dimensiones conformadas, granos correctos, claves sustitutas ocultas para los usuarios, un manejo coherente de las fechas y una capa semántica para las métricas.

#### ¿Qué diferencia hay entre un reporte y un dashboard?

Un reporte presenta datos detallados, a menudo en tablas y paginados, para análisis o fines regulatorios. Un dashboard resume visualmente las métricas clave para monitorear de un vistazo, con desglose.

#### ¿Qué es el BI de autoservicio y cuáles son sus riesgos?

Usuarios de negocio que construyen sus propios análisis a partir de datasets gobernados. Riesgos: definiciones de métricas inconsistentes, lógica duplicada, extracciones y costos sin control. Una capa semántica, datasets certificados y formación los reducen.

#### ¿Qué es la seguridad a nivel de fila en BI y en los warehouses?

Restringir qué filas ve cada usuario según su identidad (región, departamento), implementada en el warehouse (row access policies, vistas seguras) o en la capa de BI, para que un dataset sirva con seguridad a muchas audiencias.

#### ¿Cómo se documenta un warehouse?

Con descripciones de tablas y columnas en el catálogo (dbt docs, Unity Catalog, Glue, DataHub), un glosario de negocio para las métricas, grafos de linaje, responsables y SLA, y ejemplos de consultas correctas.

#### ¿Qué es un dataset certificado?

Un dataset marcado como confiable tras una revisión (definiciones, pruebas, responsable), destacado en las herramientas de BI y los catálogos para que los usuarios lo prefieran frente a copias personales o experimentales.

#### ¿Qué es el reverse ETL?

Enviar datos del warehouse (segmentos, puntajes, métricas) de vuelta a herramientas operativas como CRM, plataformas de marketing o de soporte, para que los equipos de negocio actúen sobre datos modelados (Hightouch, Census, jobs propios).

#### ¿Cómo se decide entre consultas en vivo y extracciones en las herramientas de BI?

Las consultas en vivo dan datos frescos y seguridad centralizada pero dependen del rendimiento y el costo del warehouse; las extracciones (extracts de Tableau, import de Power BI, SPICE) son rápidas y baratas por consulta pero quedan desactualizadas y duplicadas. Se elige por dashboard según la necesidad de frescura y el uso.

### Gobierno y seguridad

#### ¿Cómo se asegura un data warehouse?

Con roles de mínimo privilegio (roles de acceso concedidos a roles funcionales), SSO y MFA, restricciones de red, cifrado en reposo y en tránsito, enmascaramiento de las columnas sensibles, seguridad a nivel de fila, auditoría de los accesos y entornos separados para desarrollo y producción.

#### ¿Cómo se manejan los datos personales en un warehouse?

Clasificándolos y etiquetándolos, minimizando lo que se carga, seudonimizando o tokenizando los identificadores desde el principio, enmascarando para la mayoría de los usuarios, restringiendo el acceso en bruto, aplicando políticas de retención y atendiendo las solicitudes de supresión (RGPD, Ley 1581 de 2012 de habeas data en Colombia) con procesos documentados.

#### ¿Qué es el linaje de datos y por qué importa?

El registro de dónde vienen los datos y cómo se transforman, a nivel de tabla y de columna. Sirve para analizar el impacto antes de los cambios, depurar cifras erróneas, las auditorías y la confianza.

#### ¿Qué es un catálogo de datos?

Un inventario consultable de datasets con descripciones, responsables, esquemas, etiquetas, linaje, estado de calidad y uso, que ayuda a encontrar y entender los datos (DataHub, Collibra, Alation, Unity Catalog, Glue Data Catalog).

#### ¿Qué son las políticas de retención de datos?

Reglas sobre cuánto tiempo se conserva cada dataset (por razones legales, de negocio y de costo), implementadas con el borrado de particiones, reglas de ciclo de vida, ajustes de Time Travel y archivado, y documentadas para el cumplimiento.

### SQL para analítica

#### ¿Qué son las funciones de ventana y por qué son esenciales en el warehousing?

Funciones que calculan valores sobre un conjunto de filas relacionadas con la fila actual sin colapsarlas (`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`, `SUM() OVER`). Sirven para deduplicar, calcular totales acumulados, comparar periodos y armar sesiones.

#### ¿Cómo se calcula el crecimiento mes a mes?

```sql
WITH monthly AS (
  SELECT d.year_month, SUM(f.net_amount) AS revenue
  FROM fct_order_lines f JOIN dim_date d ON f.order_date_key = d.date_key
  GROUP BY d.year_month
)
SELECT year_month, revenue,
       revenue / NULLIF(LAG(revenue) OVER (ORDER BY year_month), 0) - 1 AS mom_growth
FROM monthly;
```

#### ¿Cómo se calcula un total acumulado?

`SUM(amount) OVER (PARTITION BY customer_key ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`.

#### ¿Cómo se deduplica conservando la fila más reciente por clave?

```sql
SELECT * FROM (
  SELECT s.*, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) AS rn
  FROM stg_customers s
) WHERE rn = 1;
```

Los motores con `QUALIFY` (Snowflake, BigQuery, Databricks) permiten filtrar directamente sobre la ventana.

#### ¿Qué diferencia hay entre `RANK`, `DENSE_RANK` y `ROW_NUMBER`?

`ROW_NUMBER` da números secuenciales únicos; `RANK` da el mismo rango a los empates y salta los siguientes (1, 1, 3); `DENSE_RANK` da el mismo rango a los empates sin huecos (1, 1, 2).

#### ¿Cómo se encuentran los clientes activos en meses consecutivos?

Calculando los meses de actividad de cada cliente y usando `LAG` para comparar con el mes anterior, o la técnica de "gaps and islands" (índice del mes menos número de fila) para agrupar las rachas consecutivas.

#### ¿Qué es una consulta de análisis de cohortes?

Asignar cada cliente a una cohorte (mes de primera compra) y luego contar los clientes activos o los ingresos por cohorte y meses desde la primera compra, a menudo pivotado en un triángulo de retención.

#### ¿Cómo se calcula una mediana o un percentil?

Con `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x)` en muchos motores, `MEDIAN()` en Snowflake, o `APPROX_PERCENTILE`/`APPROX_QUANTILES` para muchos datos.

#### ¿Qué son `GROUPING SETS`, `ROLLUP` y `CUBE`?

Extensiones de `GROUP BY` que calculan varios niveles de agregación en una consulta: `ROLLUP(year, month)` da totales por mes, por año y general; `CUBE` da todas las combinaciones; `GROUPING SETS` enumera las combinaciones exactas.

#### ¿Qué es una CTE y cuándo usarla?

Una common table expression (`WITH nombre AS (...)`) le da nombre a una subconsulta para la legibilidad y la reutilización dentro de una consulta; las CTE recursivas recorren jerarquías. Facilitan la revisión del SQL complejo del warehouse.

#### ¿Cómo se evitan los errores de división por cero?

Con `NULLIF(denominador, 0)` para que el resultado sea `NULL` en lugar de un error, o con funciones de división segura (`SAFE_DIVIDE` en BigQuery, `DIV0` en Snowflake).

#### ¿Qué diferencia hay entre `WHERE` y `HAVING`?

`WHERE` filtra las filas antes de agregar; `HAVING` filtra los grupos después de agregar. Filtrar temprano con `WHERE` es más barato.

#### ¿Cómo se manejan los NULL en joins y agregaciones?

`NULL` nunca es igual a nada, así que las filas con claves `NULL` no se unen (usa miembros desconocidos o `IS NOT DISTINCT FROM`); las agregaciones ignoran los `NULL` salvo `COUNT(*)`; usa `COALESCE` para los valores por defecto al mostrar.

#### ¿Cómo se pivotan filas en columnas con SQL?

Con agregación condicional (`SUM(CASE WHEN channel = 'web' THEN amount END) AS web_amount`), portable entre motores, o con `PIVOT` donde se admita (Snowflake, SQL Server, BigQuery, Databricks).

### Escenarios

#### Diseña un data mart de ventas para una empresa de comercio electrónico.

Proceso de negocio: líneas de pedido. Grano: una fila por línea de pedido. Dimensiones: fecha (pedido, envío), cliente (SCD2 sobre segmento y región), producto (SCD2 sobre categoría), tienda o canal, promoción y una junk dimension para los indicadores; dimensión degenerada el número de pedido. Hechos: cantidad, monto bruto, descuento, monto neto, costo, impuestos. Después se añaden un hecho de devoluciones y una foto diaria de inventario que comparten las dimensiones conformadas.

#### Finanzas y ventas reportan cifras de ingresos distintas. ¿Cómo lo resuelves?

Busco la definición de cada equipo (bruto o neto, fecha de reserva o de envío, conversión de moneda, reembolsos, cancelaciones), sigo ambas cifras con el linaje hasta las fuentes, acuerdo una sola definición con los responsables de negocio, la implemento una vez en la capa semántica o en un hecho conformado y retiro la lógica divergente.

#### La carga diaria de una tabla de hechos a veces crea duplicados. ¿Cómo lo corriges?

Hago idempotente la carga (`MERGE` sobre la clave del grano o delete-insert de la ventana de carga), deduplico staging por clave natural, añado una prueba de unicidad al grano que bloquee la publicación y reviso si la extracción del origen tiene ventanas solapadas.

#### Una dimensión debe conservar el historial de los cambios de segmento del cliente, pero la dirección cambia a diario. ¿Qué haces?

Sigo el segmento como SCD2 en la dimensión de cliente; pongo la dirección en una dimensión o minidimensión aparte, o la mantengo como tipo 1 si su historial no se necesita para el análisis, para evitar la explosión diaria de filas.

#### ¿Cómo migrarías un warehouse on-premises a la nube?

Inventariando las fuentes, los jobs de ETL, los reportes y los usuarios; eligiendo la plataforma y la arquitectura destino; migrando el historial de forma masiva; reconstruyendo los pipelines como ELT (a menudo con dbt) en lugar de un simple "lift-and-shift" cuando aporte valor; redefiniendo la seguridad y el gobierno; validando con reportes de conciliación; ejecutando en paralelo; cambiando los reportes por olas; y dando de baja el sistema viejo.

#### Las consultas sobre una tabla de hechos de 5 años se volvieron lentas a medida que crecieron los datos. ¿Qué revisas?

Si las consultas filtran por la columna de partición o de clustering, la degradación de la organización de los datos (profundidad de clustering, archivos pequeños), estadísticas faltantes, joins nuevos que multiplican filas, consultas de BI sin filtro de fecha, y si tablas agregadas o vistas materializadas servirían los patrones comunes.

#### ¿Cómo le explicas un data warehouse a una persona de negocio?

Es la historia confiable y ordenada de los datos de la empresa: la información de todos los sistemas reunida, limpiada y descrita una sola vez, para que todos respondan las preguntas de negocio con las mismas cifras.

#### ¿Cómo modelarías las suscripciones de una empresa SaaS?

Una dimensión de suscripción (plan, periodo de facturación, estado en SCD2), un hecho transaccional para los eventos de suscripción (alta, mejora, reducción, cancelación) y un hecho de foto periódica mensual con el MRR por cliente y plan, que permite analizar churn, expansión y cohortes.

#### Los analistas se quejan de que no encuentran las tablas correctas. ¿Qué haces?

Organizo los esquemas por capa y dominio, documento los modelos y las columnas, certifico los datasets clave, publico un catálogo con búsqueda y linaje, marco como obsoletas y elimino las tablas heredadas, y ofrezco una capa semántica con métricas con nombres de negocio.

#### ¿Cómo diseñarías el warehouse de una empresa que adquiere otras empresas con frecuencia?

Una capa de integración resiliente a fuentes nuevas (Data Vault o un núcleo bien estructurado con tablas de mapeo de fuentes), dimensiones conformadas con emparejamiento de datos maestros entre empresas, códigos del sistema de origen en cada fila, y marts que puedan incluir o excluir las entidades adquiridas.
