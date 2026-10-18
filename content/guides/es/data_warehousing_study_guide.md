## Guía de estudio de Data Warehousing

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de data warehousing: unas 200 preguntas](../../images/data_warehousing_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre data warehousing: conceptos clave, modelado dimensional con hechos y dimensiones, dimensiones lentamente cambiantes, patrones de carga, calidad de datos, arquitecturas y motores de warehouse, rendimiento, warehouses en la nube, BI y capa semántica, con ejemplos en SQL. Las respuestas son independientes de la herramienta cuando es posible, con notas para Snowflake, Redshift, BigQuery y Databricks.

La guía sigue una ruta de aprendizaje en seis etapas. Cada sección se divide en unidades cortas: objetivos de aprendizaje, una explicación del concepto y un ejemplo resuelto, luego preguntas (primero de memoria, después de aplicación), un reto práctico e ideas clave. Para **aprender**, lee cada unidad de principio a fin. Para **repasar**, cambia al modo repaso o usa "Ir a las preguntas", marca las respuestas que quieras volver a ver y prueba un repaso mixto entre secciones.

<!-- QA -->
<!-- stage: Fundamentos -->

### Conceptos clave

<!-- unit: Qué es un warehouse -->

<!-- goals -->

- Explicar qué es un data warehouse y en qué se diferencia de una base operativa.
- Describir quién usa un warehouse y por qué la analítica necesita su propio sistema.

<!-- concept -->

Los sistemas operativos están hechos para mover el negocio: tomar una orden, actualizar inventario, registrar un pago, miles de veces por minuto. Preguntarles "¿cómo cambiaron las ventas por región en tres años?" es lento para ellos e incómodo para ti, porque los datos están repartidos entre sistemas, se sobrescriben al cambiar y están modelados para escribir, no para leer.
Un warehouse resuelve ese desajuste: un lugar donde los datos de muchos sistemas se integran, conservan su historia y se organizan por temas de negocio para un análisis rápido y consistente.

<!-- example -->

| Pregunta | Base OLTP | Data warehouse |
|---|---|---|
| Consulta típica | Traer la orden 98123 | Ingresos por mes y región, 3 años |
| Datos | Estado actual, un sistema | Historia, muchos sistemas integrados |
| Modelo | Normalizado para escrituras | Dimensional para lecturas |
| Usuarios | Aplicaciones | Analistas, BI, ciencia de datos |

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

<!-- challenge -->

Una empresa corre sus reportes mensuales directamente sobre la base del ERP de noche. Nombra dos problemas que resolvería un warehouse.

<!-- solution -->

Los reportes dejarían de competir con el ERP por recursos y de necesitar ventanas nocturnas, y se conservaría la historia (el ERP sobrescribe cambios como la región del cliente). Un warehouse además integra el CRM y otras fuentes que el ERP no tiene.

<!-- takeaways -->

- Los warehouses integran datos de muchos sistemas con historia.
- OLTP mueve el negocio; OLAP lo analiza.
- La analítica necesita su propio sistema y modelo.

<!-- unit: Capas y componentes -->

<!-- goals -->

- Describir las capas de un warehouse y el papel del staging.
- Comparar ETL y ELT y explicar los metadatos del warehouse.

<!-- concept -->

Los datos pasan por un warehouse en etapas, cada una con su tarea. Staging conserva los extractos de la fuente casi como llegaron, para reiniciar y auditar las cargas. Una capa de integración limpia, conforma y guarda la historia. Los marts de presentación dan forma a los datos para los consumidores.
Que la transformación ocurra antes de cargar (ETL) o dentro del warehouse (ELT) depende sobre todo de dónde es más barato el cómputo; los warehouses en la nube volvieron estándar el ELT. Los metadatos unen las capas registrando qué significa cada tabla y de dónde vino.

<!-- example -->

```text
sources ─► staging (raw extracts, load metadata)
        ─► core / integration (clean, conformed, historized)
        ─► marts (stars per business process) ─► BI, data science
```

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

<!-- challenge -->

Un equipo transforma los datos dentro del script de extracción y carga solo las tablas finales. Aparece un bug de transformación. ¿Por qué es difícil recuperarse y qué capa falta?

<!-- solution -->

Sin capa de staging no se guardan los extractos crudos, así que la lógica corregida no se puede volver a correr sobre los datos originales; las fuentes pueden haber cambiado. Conserva los datos de la fuente en staging (o un persistent staging area) y transforma desde ahí.

<!-- takeaways -->

- Staging, integración y marts tienen cada uno su tarea.
- ELT transforma dentro del warehouse; ETL antes.
- Los metadatos explican significado y origen.

<!-- unit: Marts, ODS, lagos y appliances -->

<!-- goals -->

- Distinguir data marts, ODS, data lakes y lakehouses.
- Conocer marts dependientes e independientes y los appliances de warehouse.

<!-- concept -->

Alrededor del warehouse hay almacenes relacionados con tareas distintas. Los data marts se enfocan en un área o proceso; construidos desde un warehouse compartido coinciden entre sí, construidos por separado se distancian. Un ODS integra datos operativos actuales para uso casi en tiempo real. Un data lake guarda datos crudos de cualquier formato a bajo costo; un lakehouse le agrega funciones de warehouse.
Los appliances eran la forma on premises de correr warehouses, hoy reemplazados casi del todo por servicios en la nube.

<!-- example -->

| Almacén | Propósito | Datos |
|---|---|---|
| Data mart | Análisis de ventas | Modelados, un tema |
| ODS | Pantallas de servicio al cliente | Actuales, integrados |
| Data lake | Datos crudos y de ML | Cualquier formato, historia |
| Lakehouse | BI y ML sobre una copia | Tablas abiertas con ACID |

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

<!-- challenge -->

Marketing y finanzas construyeron cada uno su mart independiente desde los sistemas fuente, y sus conteos de clientes nunca coinciden. ¿Qué propones?

<!-- solution -->

Construir ambos marts desde una capa de integración compartida con una dimensión de cliente conformada y una sola definición de "cliente", volviéndolos marts dependientes que coinciden por construcción.

<!-- takeaways -->

- Los marts sirven un tema; los dependientes coinciden.
- Un ODS sirve necesidades operativas actuales.
- Lagos y lakehouses complementan o reemplazan a los warehouses.

<!-- unit: Confianza y oportunidad -->

<!-- goals -->

- Explicar una fuente única de verdad y cómo lograrla.
- Definir expectativas de latencia y SLAs del warehouse.

<!-- concept -->

Un warehouse solo vale si la gente confía en él, lo que significa una definición y una fuente por métrica, entregada cuando se necesita. Las cifras contradictorias suelen venir de definiciones distintas más que de bugs: bruto contra neto, fecha de reserva contra fecha de envío.
La oportunidad es la otra mitad de la confianza. La latencia es cuánto tarda un evento en aparecer en los reportes; los SLAs lo hacen explícito para que los consumidores sepan cuándo los datos están completos.

<!-- example -->

| Métrica | Definición (acordada) | SLA |
|---|---|---|
| Ingreso neto | Bruto − devoluciones − descuentos, por fecha de orden, EUR | Actualizado antes de las 07:00 hora local, días hábiles |
| Cliente activo | Orden en los últimos 90 días | Diario |

#### ¿Qué es la latencia en el contexto de un warehouse?

La demora entre un evento en un sistema de origen y su disponibilidad en los reportes: batch diario (horas), micro-lotes (minutos) o streaming (segundos). La latencia adecuada depende de las decisiones de negocio, no de la tecnología.

#### ¿Qué son los SLA de un data warehouse?

Compromisos como "el mart de ventas se actualiza antes de las 7 a. m. hora local en días hábiles" o "el 99 % de las cargas termina bien", con monitoreo y comunicación cuando se incumplen. Convierten los pipelines en productos en los que los consumidores pueden confiar.

#### ¿Qué es el modelado dimensional?

La técnica de Ralph Kimball para diseñar esquemas analíticos alrededor de los procesos de negocio: hechos (mediciones de eventos) rodeados de dimensiones (contexto descriptivo). Prioriza la comprensión y el rendimiento de las consultas sobre la normalización.

#### ¿Cuáles son los cuatro pasos del diseño dimensional de Kimball?

1) Elegir el proceso de negocio (por ejemplo la toma de pedidos). 2) Declarar el grano (qué representa una fila de hechos). 3) Identificar las dimensiones (quién, qué, dónde, cuándo, por qué, cómo). 4) Identificar los hechos (mediciones numéricas a ese grano).

<!-- challenge -->

Ventas reporta ingresos por fecha de reserva y finanzas por fecha de factura, y ambos tienen razón para su propósito. ¿Cómo mantienes una fuente única de verdad?

<!-- solution -->

Define ambas métricas explícitamente con nombres distintos (ingreso reservado, ingreso facturado), documéntalas en el glosario, calcula cada una una vez en modelos certificados y muestra ambas donde aplique.

<!-- takeaways -->

- Los conflictos suelen venir de definiciones, no de bugs.
- Una definición y una fuente por métrica.
- Los SLAs hacen explícitas las expectativas de frescura.

### Fundamentos del modelado dimensional

<!-- unit: Inmon y Kimball -->

<!-- goals -->

- Comparar los enfoques de Inmon y Kimball.
- Describir arquitecturas hub-and-spoke y federadas.

<!-- concept -->

Las dos escuelas clásicas difieren en dónde ocurre la integración. Inmon construye primero un warehouse empresarial normalizado y de ahí deriva los marts: integración fuerte, arranque lento. Kimball construye marts dimensionales por proceso de negocio y los integra con dimensiones conformadas: valor más rápido, pero exige disciplina.
La forma organizacional sigue: hub-and-spoke pone un warehouse central en el medio; las federadas dejan a las unidades de negocio conservar los suyos, unidos por estándares compartidos.

<!-- example -->

```text
Inmon:   sources ─► EDW (3NF) ─► marts (sales, finance, HR)
Kimball: sources ─► staging ─► star schemas per process, sharing dim_customer, dim_date
```

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

<!-- challenge -->

Una empresa necesita dashboards de ventas en dos meses y más áreas después. ¿Con qué enfoque arrancas y qué disciplina protege el futuro?

<!-- solution -->

Kimball: entrega rápido la estrella de ventas, pero construye las dimensiones (cliente, producto, fecha) conformadas desde el primer día y planea con una bus matrix, para que los marts siguientes las reutilicen.

<!-- takeaways -->

- Inmon integra primero; Kimball entrega marts primero.
- Las dimensiones conformadas mantienen integrados los marts de Kimball.
- La organización define hub-and-spoke o diseños federados.

<!-- unit: Data Vault -->

<!-- goals -->

- Describir hubs, links, satellites y capas del vault en Data Vault.
- Decidir cuándo encaja Data Vault, incluso con adquisiciones frecuentes.

<!-- concept -->

Data Vault está pensado para el cambio. Separa llaves de negocio (hubs), relaciones (links) e historia descriptiva (satellites), así una fuente nueva agrega satellites nuevos en lugar de reestructurar las tablas existentes. Todo es solo de inserción con metadatos de carga, lo que da historia de auditoría completa.
El precio es la complejidad: muchas tablas y joins, así que hacen falta marts y tablas auxiliares como las PIT para el consumo. Paga con muchas fuentes cambiantes y requisitos estrictos de auditoría.

<!-- example -->

```text
raw vault:      hub_customer, sat_customer_crm, sat_customer_billing, link_customer_order
business vault: sat_customer_segment (derived rules)
helpers:        pit_customer (keys of latest satellite rows per snapshot date)
marts:          dim_customer, fct_orders
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

<!-- challenge -->

Tras cada adquisición, hay que rediseñar el modelo central para encajar los datos de clientes de la nueva empresa. ¿Cómo cambiaría eso Data Vault?

<!-- solution -->

Las fuentes nuevas cargan en satellites (y links) nuevos atados al hub de clientes existente mediante llaves de negocio o mapeo; las tablas existentes no se tocan. Luego los marts combinan los satellites con reglas de negocio acordadas.

<!-- takeaways -->

- Hubs, links y satellites separan llaves, relaciones e historia.
- Las fuentes nuevas agregan tablas en vez de reestructurar las viejas.
- Marts y tablas PIT hacen usables los vaults.

<!-- unit: Consumo y arquitecturas alternativas -->

<!-- goals -->

- Ubicar la arquitectura medallion y las capas semánticas en el warehousing.
- Conocer cubos OLAP, virtualización y warehouses en tiempo real.

<!-- concept -->

Las plataformas modernas conservan las ideas del warehouse cambiando la tecnología. Las capas medallion de un lakehouse corresponden a staging, integración y marts. Las capas semánticas definen las métricas una vez para todas las herramientas de BI, haciendo lo que hacían los cubos OLAP con agregados precalculados.
Dos alternativas cambian almacenamiento por otras cosas: la virtualización consulta las fuentes en sitio sin copiar, y los warehouses en tiempo real ingestan continuamente para que los reportes tengan minutos y no un día.

<!-- example -->

| Clásico | Equivalente moderno |
|---|---|
| Staging | Bronze |
| Capa de integración | Silver |
| Data marts | Gold |
| Cubo OLAP | Capa semántica + motor columnar |

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

<!-- challenge -->

Tres herramientas de BI calculan el "margen bruto" de tres formas distintas. ¿Qué pieza de arquitectura lo arregla?

<!-- solution -->

Una capa semántica (o de métricas) que defina el margen bruto una vez, con su fórmula y dimensiones, consumida por las tres herramientas, para que cada reporte use el mismo cálculo.

<!-- takeaways -->

- Las capas medallion reflejan las capas clásicas del warehouse.
- Las capas semánticas definen métricas una vez para todas las herramientas.
- Virtualización y streaming cambian copias por frescura.

<!-- stage: Modelado dimensional -->

### Hechos en detalle

<!-- unit: Diseñar un modelo dimensional -->

<!-- goals -->

- Aplicar los cuatro pasos de diseño de Kimball.
- Declarar el grano y elegir dimensiones a partir de preguntas de negocio.

<!-- concept -->

El diseño dimensional parte de un proceso de negocio, no de las tablas fuente. Elegido el proceso, la decisión más importante es el grano: exactamente qué significa una fila. Todo lo demás se desprende de ahí. Las dimensiones son el quién, qué, dónde y cuándo que describen cada fila; los hechos son los números medidos a ese grano.
Elegir el grano más atómico mantiene útil el modelo para preguntas que nadie ha hecho todavía, porque desde el detalle se arma cualquier resumen, pero no al revés.

<!-- example -->

```text
1. Process:    order taking
2. Grain:      one row per order line
3. Dimensions: date, customer, product, store, promotion
4. Facts:      quantity, gross_amount, discount_amount, net_amount
```

#### ¿Por qué no se deben unir directamente dos tablas de hechos?

Sus granos suelen ser distintos, y los joins directos producen fan-outs y doble conteo. Agrega primero cada hecho al grano dimensional común y luego combínalos.

#### ¿Qué es una dimensión de hora del día?

Una dimensión aparte con una fila por minuto o segundo del día (hora, minuto, franja horaria), usada cuando importa el análisis por hora del día, manteniendo pequeña la dimensión de fecha.

#### ¿Cómo se nombran las tablas y columnas en un modelo dimensional?

De forma coherente y en lenguaje de negocio: prefijos `fct_` y `dim_` (o `fact_`/`dim_`), sustantivos en singular, `_key` para las claves sustitutas, `_id` para las naturales, unidades explícitas (`amount_cop`) y sin jerga de los sistemas de origen en las capas de presentación.

#### ¿Cuáles son los tres tipos de tablas de hechos?

Hechos transaccionales (una fila por evento, como una línea de pedido), de foto periódica (una fila por entidad por periodo, como el saldo de una cuenta por día) y de foto acumulativa (una fila por instancia de un proceso, actualizada a medida que avanza por sus hitos, como un pedido desde su creación hasta la entrega).

#### ¿Cuándo se usa una tabla de hechos de foto periódica?

Para medir niveles o estados a intervalos regulares (inventario, saldos, suscripciones activas por mes), cuando sumar las transacciones sería costoso o el estado no se puede derivar de los eventos.

<!-- challenge -->

Un interesado pide una tabla de "ventas diarias por tienda". ¿Qué grano construyes y por qué?

<!-- solution -->

El grano atómico, una fila por línea de orden, con lo diario por tienda como agregado o vista encima. La tabla atómica también responde las preguntas de producto, cliente y promoción que vendrán.

<!-- takeaways -->

- Parte de un proceso de negocio.
- Declara el grano antes que todo.
- El grano atómico responde preguntas futuras.

<!-- unit: Hechos, dimensiones y esquemas -->

<!-- goals -->

- Distinguir tablas de hechos y de dimensiones.
- Comparar esquemas estrella y copo de nieve y nombrar bien los objetos.

<!-- concept -->

Un modelo dimensional tiene dos tipos de tablas. Las de hechos son largas y angostas: llaves más mediciones, una fila por evento al grano. Las de dimensiones son anchas y cortas: atributos descriptivos para filtrar y agrupar.
Poner las dimensiones directamente alrededor del hecho da una estrella, simple para los usuarios y rápida en motores columnares. Normalizar las dimensiones en subtablas da un copo de nieve, que ahorra poco espacio y agrega joins. Nombres claros de negocio completan un modelo que la gente usa sin ayuda.

<!-- example -->

```text
             dim_date
                │
dim_customer ─ fct_order_lines ─ dim_product
                │
             dim_store
```

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

<!-- challenge -->

Una dimensión de producto se normalizó en tablas de producto, subcategoría, categoría y departamento. Los analistas se quejan de los joins. ¿Qué haces?

<!-- solution -->

Aplanar la jerarquía dentro de la dimensión de producto (categoría y departamento como columnas). El costo de almacenamiento es despreciable en motores columnares, y las consultas necesitan un join en lugar de cuatro.

<!-- takeaways -->

- Los hechos guardan mediciones; las dimensiones, contexto.
- Las estrellas son más simples y suelen ser más rápidas que los copos de nieve.
- Los nombres de negocio hacen usables los modelos.

<!-- unit: Llaves -->

<!-- goals -->

- Explicar llaves sustitutas y naturales y por qué los hechos usan sustitutas.
- Decidir cómo garantizar la integridad referencial.

<!-- concept -->

Los sistemas fuente identifican las cosas con llaves naturales, que pueden cambiar, reutilizarse o chocar cuando se fusionan fuentes. El warehouse emite sus propias llaves sustitutas para las filas de dimensión, lo que además permite que una llave natural tenga varias versiones históricas.
Los hechos apuntan a las dimensiones con esas llaves sustitutas. Cada hecho debe referenciar una fila de dimensión existente, así que las cargas buscan las llaves y recurren a un miembro desconocido en vez de dejar huérfanos.

<!-- example -->

```text
dim_customer
customer_key | customer_number | segment | valid_from | valid_to
1001         | C-552           | SMB     | 2024-01-01 | 2026-03-31
1874         | C-552           | Mid     | 2026-04-01 | 9999-12-31
fct_orders.customer_key → 1001 for 2025 orders, 1874 for 2026 orders
```

#### ¿Cómo se manejan hechos con granos distintos?

Poniéndolos en tablas de hechos separadas; mezclar granos (montos del encabezado del pedido y de las líneas en una tabla) causa doble conteo. Asigna los valores del encabezado a las líneas solo si una regla de negocio lo respalda.

#### ¿Cuál es la clave primaria de una tabla de hechos?

A menudo la combinación de sus claves de dimensión más las dimensiones degeneradas al grano declarado, o una clave sustituta del hecho por comodidad. Es esencial comprobar con una prueba la unicidad al grano.

#### ¿Qué son las tablas de hechos agregadas?

Versiones resumidas de los hechos atómicos a un grano más grueso (ventas por mes y categoría) que aceleran las consultas comunes. Deben mantenerse coherentes con la tabla atómica, y las herramientas de BI o las capas semánticas pueden enrutar las consultas hacia ellas.

#### ¿Qué es una tabla de hechos consolidada?

Una tabla de hechos que combina hechos de varios procesos al mismo grano (montos reales y presupuestados por mes, cuenta y centro de costos), práctica para comparaciones como real frente a presupuesto.

<!-- challenge -->

Dos empresas adquiridas tienen un cliente `C-100` cada una, personas distintas. Los hechos con llave por número de cliente ahora las mezclan. ¿Qué cambias?

<!-- solution -->

Emite llaves sustitutas en la dimensión de cliente y conserva la llave natural junto con una columna de sistema fuente (`source`, `customer_number`) como llave de negocio. Los hechos referencian la sustituta.

<!-- takeaways -->

- Las llaves sustitutas son estables e independientes de la fuente.
- Las llaves naturales quedan como atributos con su fuente.
- Los hechos siempre deben referenciar una fila de dimensión.

<!-- unit: Dimensiones compartidas y de tiempo -->

<!-- goals -->

- Construir dimensiones conformadas y planear con una bus matrix.
- Diseñar dimensiones de fecha y de hora del día.

<!-- concept -->

En un warehouse Kimball, la integración ocurre con dimensiones conformadas: las mismas tablas de cliente, producto y fecha compartidas por todos los hechos. La bus matrix lo planea listando los procesos de negocio contra las dimensiones que usan, y muestra qué dimensiones construir primero.
La dimensión de fecha es la más compartida de todas. Lleva atributos de calendario y fiscales para que ningún reporte los recalcule. La hora del día, cuando hace falta, es una dimensión pequeña aparte.

<!-- example -->

| Proceso \ Dimensión | Fecha | Cliente | Producto | Tienda | Empleado |
|---|---|---|---|---|---|
| Órdenes | X | X | X | X | |
| Devoluciones | X | X | X | X | |
| Inventario | X | | X | X | |
| Nómina | X | | | X | X |

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

<!-- challenge -->

Cada reporte calcula los trimestres fiscales con su propio CASE, y dos no coinciden. ¿Qué agregas?

<!-- solution -->

Atributos fiscales (año, trimestre y semana fiscal) en la dimensión de fecha, calculados una vez y unidos por todos los hechos, para que los reportes usen el mismo calendario.

<!-- takeaways -->

- Las dimensiones conformadas integran los marts.
- La bus matrix planea las dimensiones compartidas.
- La dimensión de fecha centraliza la lógica de calendario.

<!-- unit: Combinar hechos -->

<!-- goals -->

- Combinar correctamente medidas de varias tablas de hechos.
- Explicar por qué los joins directos entre hechos cuentan doble.

<!-- concept -->

Procesos distintos producen tablas de hechos distintas, a menudo con granos distintos: órdenes por línea, devoluciones por línea de devolución, metas por mes. Cruzarlas directamente multiplica filas donde las llaves se repiten e infla los totales.
El método seguro es drill-across: agregar cada hecho primero a un conjunto común de dimensiones conformadas y luego combinar los resultados. Las dimensiones conformadas son las que lo hacen posible.

<!-- example -->

```sql
WITH s AS (SELECT date_key, product_key, SUM(net_amount) AS sales   FROM fct_order_lines GROUP BY 1, 2),
     r AS (SELECT date_key, product_key, SUM(refund_amount) AS returns FROM fct_returns     GROUP BY 1, 2)
SELECT COALESCE(s.date_key, r.date_key) AS date_key, COALESCE(s.product_key, r.product_key) AS product_key,
       s.sales, r.returns
FROM s FULL OUTER JOIN r ON s.date_key = r.date_key AND s.product_key = r.product_key;
```

#### ¿Cuándo usar una foto periódica en lugar de derivar el estado de las transacciones?

Cuando calcular el estado a partir de todas las transacciones históricas es costoso o complejo (saldos, niveles de inventario, tickets abiertos), o cuando los sistemas de origen dan los estados pero no historiales completos de eventos.

#### ¿Qué es una dimensión de rol (role-playing)?

Una dimensión física usada varias veces en una tabla de hechos con significados distintos, típicamente la dimensión de fecha como fecha de pedido, de envío y de entrega, expuesta mediante vistas o alias.

<!-- challenge -->

Un reporte cruza `fct_orders` con `fct_shipments` por `order_id`, y los ingresos salen 40 % por encima de finanzas. ¿Por qué?

<!-- solution -->

Las órdenes con varios envíos repiten su ingreso una vez por fila de envío. Agrega primero cada hecho a la orden (o a dimensiones compartidas) y luego cruza los resultados agregados.

<!-- takeaways -->

- Hechos con granos distintos se multiplican al cruzarlos.
- Drill-across agrega primero y combina después.
- Las dimensiones conformadas hacen posible el drill-across.

### Dimensiones en detalle

<!-- unit: Tipos de tablas de hechos -->

<!-- goals -->

- Elegir entre hechos transaccionales, periodic snapshot y accumulating snapshot.
- Usar factless facts y decidir cuándo un snapshot gana a la derivación.

<!-- concept -->

Los procesos de negocio miden cosas distintas. Los eventos (una línea de orden) encajan en hechos transaccionales, una fila por evento. Los niveles y estados (inventario, saldo de una cuenta) encajan en periodic snapshots, una fila por periodo. Los procesos con hitos (orden creada, pagada, enviada, entregada) encajan en accumulating snapshots, una fila por instancia que se actualiza a medida que avanza.
Algunos hechos no tienen ninguna medida: solo registran que algo pasó o pudo pasar.

<!-- example -->

| Proceso | Tipo de hecho | Grano |
|---|---|---|
| Ventas | Transaccional | Línea de orden |
| Inventario | Periodic snapshot | Producto × tienda × día |
| Cumplimiento de órdenes | Accumulating snapshot | Orden, con fechas de hitos |
| Asistencia a clases | Factless | Estudiante × clase × fecha |

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

<!-- challenge -->

El negocio pregunta "¿cuánto tarda cada paso del cumplimiento de órdenes y dónde se atascan?". ¿Qué tipo de hecho encaja?

<!-- solution -->

Un accumulating snapshot con una fila por orden, una llave de fecha por hito (creada, pagada, enviada, entregada) y medidas de demora entre ellos, actualizado a medida que ocurre cada hito.

<!-- takeaways -->

- Eventos: hechos transaccionales. Niveles: periodic snapshots.
- Procesos con hitos: accumulating snapshots.
- Los factless facts registran ocurrencias o cobertura.

<!-- unit: Medidas y aditividad -->

<!-- goals -->

- Clasificar hechos como aditivos, semiaditivos o no aditivos.
- Guardar bien ratios, monedas, cancelaciones y devoluciones.

<!-- concept -->

Cómo se puede sumar una medida decide cómo se guarda. Los montos suman en todo; los saldos suman entre cuentas pero no entre días; los ratios y porcentajes no suman. Guardar los componentes aditivos y calcular los ratios al consultar mantiene correcta cada agregación.
Dos casos de negocio comunes siguen la misma lógica: las monedas, que necesitan el monto original y el convertido, y las cancelaciones y devoluciones, que deben restar de los totales de una forma que siga sumando.

<!-- example -->

```sql
-- margin % computed from additive parts, correct at any level
SELECT category, SUM(revenue) AS revenue, SUM(cost) AS cost,
       (SUM(revenue) - SUM(cost)) / NULLIF(SUM(revenue), 0) AS margin_pct
FROM fct_sales JOIN dim_product USING (product_key)
GROUP BY category;
```

#### ¿Qué es la fila de "miembro desconocido"?

Una fila especial de la dimensión (a menudo con clave sustituta `-1` o `0`) que se usa cuando falta la dimensión de un hecho o aún no se conoce, para que los hechos no se pierdan en los inner joins y el problema sea visible en los reportes.

#### ¿Qué es una dimensión reducida (shrunken)?

Un subconjunto de las filas o columnas de una dimensión usado para hechos agregados a un grano mayor, como una dimensión de mes derivada de la de fecha o una de categoría derivada de la de productos.

#### ¿Qué es una dimensión lentamente cambiante?

Una dimensión cuyos atributos cambian con el tiempo de forma impredecible (un cliente se muda, un producto cambia de categoría), lo que exige una política sobre si conservar el historial y cómo.

#### ¿Qué es una dimensión estática?

Una dimensión cuyo contenido no viene de una fuente y casi no cambia, como la dimensión de fecha, las tablas de códigos de estado o las monedas, generada una vez o mantenida a mano.

<!-- challenge -->

Un dashboard promedia una columna guardada `margin_pct` entre productos y muestra un margen que el CFO discute. ¿Qué está mal?

<!-- solution -->

El porcentaje de margen no es aditivo; promediar ratios ignora el peso de los ingresos. Guarda ingreso y costo, y calcula el margen a partir de sus sumas en el nivel elegido.

<!-- takeaways -->

- La aditividad decide cómo se agregan las medidas.
- Guarda componentes; calcula ratios al consultar.
- Conserva montos en moneda original y convertida.

<!-- unit: Grano, llaves y dimensiones degeneradas -->

<!-- goals -->

- Mantener un grano por tabla de hechos y definir su llave.
- Usar dimensiones degeneradas y de auditoría, y cargar hechos tardíos.

<!-- concept -->

El grano de una tabla de hechos es una promesa que cada fila debe cumplir. Mezclar montos de encabezado de orden con montos de línea en una misma tabla rompe las sumas. Identificadores como el número de orden se quedan en el hecho como dimensiones degeneradas, sin tabla propia, y junto con las llaves de dimensión forman la llave del hecho.
Los hechos también deben explicarse: las columnas de auditoría registran cómo se cargó cada fila, y los hechos tardíos deben caer en el periodo correcto con las versiones de dimensión vigentes cuando ocurrieron.

<!-- example -->

```text
fct_order_lines
  order_number (degenerate), line_number, date_key, customer_key, product_key,
  quantity, net_amount,
  batch_id, loaded_at, source_system          ← audit
key: (order_number, line_number)
```

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

<!-- challenge -->

El costo de envío se conoce por orden, pero la tabla de hechos es por línea de orden. Los analistas lo suman y obtienen totales inflados. ¿Qué opciones tienes?

<!-- solution -->

Dejar el envío en un hecho aparte con grano de orden, o repartirlo entre las líneas (por ejemplo según el monto de la línea) para que sume bien al grano de línea. Nunca repetir el valor de la orden en cada línea.

<!-- takeaways -->

- Un grano por tabla de hechos.
- Las dimensiones degeneradas dejan los IDs de transacción en el hecho.
- Columnas de auditoría y manejo de hechos tardíos los hacen confiables.

<!-- unit: Hechos grandes y agregados -->

<!-- goals -->

- Manejar tablas de hechos con miles de millones de filas.
- Usar tablas de hechos agregadas y consolidadas.

<!-- concept -->

Las tablas de hechos crecen sin fin. Particionar por fecha y hacer clustering sobre filtros comunes mantiene las consultas leyendo una parte pequeña, y las cargas incrementales hacen que el procesamiento sea proporcional a los datos nuevos.
Los agregados cambian almacenamiento por velocidad: una copia resumida a un grano más grueso responde rápido las preguntas frecuentes, siempre que se reconstruya desde los hechos atómicos. Los hechos consolidados van en sentido contrario y combinan procesos a un grano compartido, como real y presupuesto por mes, para facilitar la comparación.

<!-- example -->

```sql
CREATE TABLE agg_sales_month_category AS
SELECT d.year_month, p.category, SUM(f.net_amount) AS net_amount, SUM(f.quantity) AS quantity
FROM fct_order_lines f
JOIN dim_date d USING (date_key) JOIN dim_product p USING (product_key)
GROUP BY 1, 2;
```

#### ¿Qué es una "vista actual" de una dimensión SCD2?

Una vista que filtra `is_current = true` y da una fila por clave natural con los atributos de hoy, usada por los analistas que no necesitan el historial y para reportes de estilo tipo 1.

#### ¿Cuáles son los tipos de SCD?

Tipo 0: nunca cambia (se conserva el original). Tipo 1: sobrescribir, sin historial. Tipo 2: una fila nueva por cambio con fechas de vigencia. Tipo 3: una columna con el "valor anterior". Tipo 4: el historial en una tabla aparte (minidimensión o tabla de historial). Tipo 6: híbrido de 1, 2 y 3 (columnas de valor actual en todas las filas más filas de historial). Tipo 7: doble clave para unir con las filas actuales o las históricas.

#### ¿Cómo funciona la SCD tipo 2?

Cuando cambia un atributo seguido, se cierra la fila vigente (se llena la fecha de fin y el indicador de vigencia pasa a falso) y se inserta una fila nueva con una nueva clave sustituta, los valores nuevos, una fecha de inicio y una fecha de fin abierta. Los hechos referencian la clave sustituta vigente cuando ocurrieron.

| customer_key | customer_id | city     | valid_from | valid_to   | is_current |
|---|---|---|---|---|---|
| 101 | C-42 | Bogotá   | 2024-01-01 | 2026-03-31 | false |
| 187 | C-42 | Medellín | 2026-04-01 | 9999-12-31 | true  |

<!-- challenge -->

Finanzas compara las ventas reales mensuales con el presupuesto, que solo existe por mes y categoría. ¿Cómo lo modelas?

<!-- solution -->

Un hecho consolidado al grano mes × categoría con columnas de real (agregado desde las ventas atómicas) y presupuesto, usando dimensiones conformadas de fecha y producto (una dimensión de producto reducida al nivel de categoría).

<!-- takeaways -->

- Particiona y agrupa los hechos grandes; carga incremental.
- Los agregados aceleran las preguntas frecuentes.
- Los hechos consolidados comparan procesos a un grano compartido.

### Dimensiones lentamente cambiantes

<!-- unit: Dimensiones especializadas -->

<!-- goals -->

- Usar dimensiones role-playing, junk, mini, outrigger, reducidas y estáticas.
- Separar atributos que cambian rápido de los que cambian lento.

<!-- concept -->

Los modelos reales necesitan algunos patrones de dimensión más allá de la tabla básica. Una dimensión de fecha puede cumplir varios roles en un hecho. Los flags sueltos se agrupan en una junk dimension en vez de llenar el hecho. Los atributos que cambian demasiado rápido para historiarlos en una dimensión grande pasan a una mini-dimensión. Algunas dimensiones referencian a otras, son versiones reducidas para agregados o se generan en lugar de cargarse.
Cada patrón existe para mantener angosto el hecho y manejables las dimensiones.

<!-- example -->

```text
fct_orders: order_date_key, ship_date_key, delivery_date_key → dim_date (role-playing)
            order_flags_key → dim_order_flags (gift_wrap, express, coupon_used) (junk)
            customer_key → dim_customer (SCD2: segment)
            customer_profile_key → dim_customer_profile (age band, income band) (mini)
```

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

<!-- challenge -->

Una tabla de hechos tiene 12 columnas de flags sí/no que los analistas casi no usan y que inflan la tabla. ¿Qué haces?

<!-- solution -->

Crea una junk dimension con una fila por cada combinación de flags observada, reemplaza las 12 columnas por una llave y deja los flags disponibles como atributos descriptivos.

<!-- takeaways -->

- Role-playing reutiliza una dimensión para varios significados.
- Las junk dimensions absorben flags misceláneos.
- Las mini-dimensiones aíslan atributos que cambian rápido.

<!-- unit: Jerarquías y muchos a muchos -->

<!-- goals -->

- Modelar jerarquías fijas e irregulares.
- Resolver relaciones muchos a muchos con tablas puente.

<!-- concept -->

Las dimensiones suelen contener jerarquías. Las fijas, con niveles conocidos, se aplanan en columnas. Las irregulares o recursivas, como los organigramas, necesitan más estructura, a menudo un puente que lista cada par ancestro-descendiente.
Las relaciones muchos a muchos, como cuentas con varios titulares o clientes con varios intereses, también necesitan puentes. Los pesos en las filas del puente permiten repartir las medidas sin contar doble.

<!-- example -->

```text
bridge_account_holder (account_key, customer_key, weight)
  A1, C1, 0.5
  A1, C2, 0.5
fct_balances.account_key → bridge → dim_customer   (SUM(balance * weight) per customer)
```

#### ¿Cómo se maneja un cambio de dimensión que llega tarde?

Si hoy te enteras de que un cambio ocurrió el mes pasado, insertas la versión con su fecha de inicio real, ajustas la fecha de fin de la fila anterior y, posiblemente, reasignas a la nueva clave sustituta los hechos ocurridos después del cambio; por eso algunos equipos prefieren hacer los joins por fecha al consultar.

#### ¿Qué es un hash diff y por qué usarlo?

Un hash (MD5, SHA) de los atributos seguidos concatenados, guardado en cada fila, para que detectar cambios sea una sola comparación en lugar de comparar muchas columnas, incluido el manejo seguro de los nulos.

#### ¿Cómo implementan la SCD2 los snapshots de dbt?

La configuración del snapshot define la clave única y una estrategia (`timestamp`, con una columna de fecha de actualización, o `check`, comparando columnas); cada ejecución compara el origen con la tabla de snapshot y cierra e inserta filas, añadiendo `dbt_valid_from` y `dbt_valid_to`.

<!-- challenge -->

Las cuentas conjuntas tienen dos titulares, y el saldo por cliente cuenta dos veces cada saldo conjunto. ¿Cómo reportas bien?

<!-- solution -->

Usa un puente con pesos de reparto (0,5 cada uno, o según participación) y suma saldo × peso por cliente. Muestra totales sin ponderar solo en reportes que pidan explícitamente "exposición por titular".

<!-- takeaways -->

- Aplana las jerarquías fijas; usa puentes para las irregulares.
- Los puentes resuelven relaciones muchos a muchos.
- Los pesos evitan contar doble.

<!-- unit: Integrar y conformar dimensiones -->

<!-- goals -->

- Fusionar datos de clientes de varios sistemas en una dimensión.
- Usar miembros desconocidos, MDM y atributos conformados.

<!-- concept -->

Una dimensión de cliente construida desde CRM, facturación y soporte debe decidir qué registros describen al mismo cliente y qué valores ganan. La gestión de datos maestros aporta el emparejamiento y un registro dorado; sin ella, el warehouse hace una versión más simple por su cuenta.
Dos convenciones pequeñas mantienen usable el resultado: una fila de miembro desconocido para hechos sin dimensión, para que nada se pierda en los joins, y atributos conformados que significan lo mismo en todas partes.

<!-- example -->

```text
dim_customer
customer_key | master_id | crm_id | billing_id | segment | country
-1           | -1        | n/a    | n/a        | Unknown | Unknown   ← unknown member
1874         | M-552     | C-552  | B-9917     | Mid     | ES
```

#### ¿Cómo se prueba una dimensión SCD2?

Comprobando que cada clave natural tenga exactamente una fila vigente, que los rangos de vigencia no se solapen ni dejen huecos, que `valid_from < valid_to`, que las claves sustitutas sean únicas y que las claves sustitutas de los hechos existan en la dimensión.

#### ¿Qué es una SCD2 con marca de tiempo frente a granularidad diaria?

Algunas dimensiones siguen los cambios con precisión de marca de tiempo (varios cambios al día), otras a nivel de día (el último valor del día). Elige según cómo se emparejan los hechos; la granularidad diaria es más simple y suele bastar.

#### ¿Se pueden reasignar los hechos a nuevas versiones de la dimensión?

Normalmente no: los hechos conservan la versión vigente cuando ocurrieron. Para reportar "a la fecha de hoy", une por la clave natural con la fila vigente o usa las columnas de valor actual del tipo 6.

#### ¿Qué es una carga completa frente a una incremental?

Una carga completa vuelve a cargar todos los datos en cada ejecución (simple, costosa, adecuada para tablas pequeñas). Una carga incremental procesa solo los datos nuevos o modificados desde la última ejecución (por fecha, secuencia o CDC), lo que es necesario en tablas grandes.

<!-- challenge -->

El 5 % de las ventas no tiene cliente asociado porque la sincronización del CRM va atrasada. Los reportes por cliente pierden esas ventas en silencio. Arréglalo.

<!-- solution -->

Asigna los hechos sin pareja al miembro desconocido (o crea inferred members con la llave natural) para que los totales queden completos, y actualiza la llave cuando llegue el cliente. Monitorea la proporción de llaves desconocidas.

<!-- takeaways -->

- Fusiona las fuentes en una dimensión de cliente conformada.
- Los miembros desconocidos evitan que los hechos desaparezcan.
- Los atributos conformados significan lo mismo en todas partes.

### Carga del warehouse

<!-- unit: Tipos de SCD -->

<!-- goals -->

- Explicar los SCD tipo 0, 1, 2, 3 y 6.
- Elegir una política de cambio por atributo.

<!-- concept -->

Los atributos de dimensión cambian: los clientes se mudan, los productos se recategorizan. Cada atributo necesita una decisión: ¿los reportes deben ver la historia o solo el valor actual? El tipo 1 sobrescribe, así toda la historia sigue el valor de hoy. El tipo 2 guarda versiones, así los hechos quedan atados a lo que era cierto cuando ocurrieron. El tipo 3 guarda un valor anterior; el tipo 6 combina historia con columnas actuales.
La decisión es por atributo, así que la mayoría de dimensiones mezcla políticas.

<!-- example -->

| Atributo | Política | Por qué |
|---|---|---|
| Corrección de ortografía del nombre | Tipo 1 | Corrección, no hace falta historia |
| Segmento del cliente | Tipo 2 | Las ventas deben quedar con el segmento anterior |
| Región anterior (reorganización puntual) | Tipo 3 | Comparar vieja vs nueva |
| Fecha de nacimiento | Tipo 0 | Nunca cambia |

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

<!-- challenge -->

Los gerentes de ventas quieren las ventas del año pasado por la región en que estaba el cliente en ese momento, pero también por la región de hoy. ¿Qué enfoque de SCD soporta ambas?

<!-- solution -->

Tipo 2 en la región para las versiones históricas, más una columna tipo 1 `current_region` en cada versión (tipo 6), para que los reportes agrupen por cualquiera de las dos.

<!-- takeaways -->

- Elige una política de cambio por atributo.
- El tipo 2 conserva la historia; el tipo 1 sobrescribe.
- El tipo 6 ofrece la vista histórica y la actual juntas.

<!-- unit: Implementar el tipo 2 -->

<!-- goals -->

- Implementar SCD2 con SQL, hash diffs y dbt snapshots.
- Elegir fechas de vigencia, flags de actual y granularidad.

<!-- concept -->

Una carga SCD2 compara los registros entrantes con las versiones actuales. Cuando cambian atributos seguidos, cierra la fila actual e inserta una nueva con una llave sustituta nueva. Hacer hash de los atributos seguidos convierte la detección de cambios en una sola comparación en lugar de muchas.
Las convenciones simplifican las consultas: una fecha de fin lejana en el futuro en lugar de `NULL`, un flag de actual y una vista de filas actuales. Si la vigencia se sigue por día o por timestamp depende de qué tan seguido ocurren los cambios.

<!-- example -->

```sql
-- close changed current rows
UPDATE dim_customer d SET valid_to = s.change_date - 1, is_current = false
FROM stg_customer s
WHERE d.customer_number = s.customer_number AND d.is_current AND d.hash_diff <> s.hash_diff;
-- insert new versions
INSERT INTO dim_customer (customer_number, segment, region, hash_diff, valid_from, valid_to, is_current)
SELECT s.customer_number, s.segment, s.region, s.hash_diff, s.change_date, DATE '9999-12-31', true
FROM stg_customer s
LEFT JOIN dim_customer d ON d.customer_number = s.customer_number AND d.is_current
WHERE d.customer_number IS NULL OR d.hash_diff <> s.hash_diff;
```

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

<!-- challenge -->

Una dimensión SCD2 crea una versión nueva cada día para la mayoría de clientes, aunque nada visible cambia. ¿Cuál es la causa probable?

<!-- solution -->

El hash incluye un atributo que cambia a diario (un `last_login` o timestamp de carga) o valores sin normalizar (espacios finales, mayúsculas). Haz hash solo de los atributos de negocio seguidos, normalizados; pasa los volátiles a tipo 1 o a una tabla aparte.

<!-- takeaways -->

- SCD2 cierra filas viejas e inserta versiones nuevas.
- Los hash diffs abaratan la detección de cambios.
- Fechas de fin lejanas y flags de actual simplifican las consultas.

<!-- unit: Usar y mantener SCD2 -->

<!-- goals -->

- Buscar la versión correcta de la dimensión al cargar hechos.
- Manejar cambios tardíos, dimensiones grandes y pruebas.

<!-- concept -->

La historia solo sirve si los hechos apuntan a la versión correcta. Las cargas de hechos buscan la versión cuyo rango de vigencia contiene la fecha del evento; reportar "a hoy" pasa por la vista actual en vez de reescribir hechos.
Con el tiempo SCD2 trae sus propios problemas: cambios que llegan tarde y deben insertarse en el pasado, dimensiones que crecen demasiado rápido y errores sutiles como rangos superpuestos. Las pruebas sobre la estructura de la dimensión atrapan la mayoría.

<!-- example -->

```sql
-- each natural key: exactly one current row, no overlapping ranges
SELECT customer_number FROM dim_customer GROUP BY 1 HAVING SUM(CASE WHEN is_current THEN 1 ELSE 0 END) <> 1;
SELECT a.customer_number FROM dim_customer a JOIN dim_customer b
  ON a.customer_number = b.customer_number AND a.customer_key < b.customer_key
 AND a.valid_from <= b.valid_to AND b.valid_from <= a.valid_to;
```

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

<!-- challenge -->

Hoy te enteras de que un cliente cambió de segmento el 1 de marzo, pero ya cargaste las ventas de marzo contra la versión vieja. ¿Qué haces?

<!-- solution -->

Inserta la versión nueva con valid_from 1 de marzo, cierra la vieja el 28 de febrero y redirige los hechos de marzo de ese cliente a la nueva llave sustituta. Deja registrada la corrección.

<!-- takeaways -->

- Los hechos se unen a la versión vigente en la fecha del evento.
- Los cambios tardíos pueden exigir redirigir hechos.
- Prueba que haya una fila actual y ninguna superposición.

<!-- stage: Construir el warehouse -->

### Calidad de datos

<!-- unit: Cargas completas, incrementales y CDC -->

<!-- goals -->

- Elegir entre extracción completa, incremental y CDC.
- Seguir el progreso con watermarks y tablas de control.

<!-- concept -->

Recargar todo cada noche es simple hasta que deja de serlo: los volúmenes crecen y las ventanas se achican. Las cargas incrementales toman solo lo que cambió desde la última vez, seguido con un watermark guardado en una tabla de control. La extracción por timestamp depende de que las fuentes actualicen sus timestamps; el CDC basado en logs lee cada cambio, borrados incluidos, sin tocar las tablas.
Quién inicia la transferencia, el warehouse que jala o la fuente que empuja, decide dónde viven la programación y el manejo de fallas.

<!-- example -->

```sql
SELECT * FROM src.orders
WHERE updated_at > (SELECT last_watermark FROM etl_control WHERE pipeline = 'orders')
  AND updated_at <= :run_started_at;
UPDATE etl_control SET last_watermark = :run_started_at WHERE pipeline = 'orders';
```

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

<!-- challenge -->

Una carga incremental por `updated_at` nunca elimina las órdenes borradas en la fuente. ¿Qué opciones tienes?

<!-- solution -->

Pasar a CDC basado en logs para recibir eventos de borrado, o comparar periódicamente la lista completa de llaves con la fuente para detectar las faltantes y marcarlas como borradas (soft delete) en el warehouse.

<!-- takeaways -->

- Las cargas incrementales escalan; las completas son simples.
- Watermarks y tablas de control siguen el progreso.
- El CDC basado en logs captura también los borrados.

<!-- unit: Cargar dimensiones y hechos -->

<!-- goals -->

- Cargar dimensiones y hechos en el orden correcto con búsqueda de llaves.
- Manejar inferred members y borrados en la fuente.

<!-- concept -->

El orden importa: las dimensiones cargan primero para que los hechos encuentren sus llaves sustitutas. Las cargas de dimensiones limpian y deduplican por llave natural y luego aplican las políticas de cambio. Las cargas de hechos buscan las llaves de cada dimensión, en la versión vigente en la fecha del evento.
Cuando un hecho referencia un cliente que el warehouse no ha visto, un inferred member deja cargado el hecho y se completa después. Los borrados en las fuentes también necesitan una política: eliminación física o un flag de borrado.

<!-- example -->

```text
1. load dim_date (static), dim_product, dim_customer (SCD2)
2. load fct_order_lines:
   customer_key ← lookup(customer_number, order_date)  or inferred member if missing
   product_key  ← lookup(sku, order_date)              or -1 (unknown)
```

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

<!-- challenge -->

Llegan órdenes de clientes nuevos unas horas antes de que el CRM mande sus datos, y esas órdenes quedan para siempre con la llave desconocida. ¿Qué cambias?

<!-- solution -->

Crea inferred members: inserta una fila de cliente provisional con la llave natural cuando un hecho referencia un cliente desconocido, y actualízala (tipo 1) cuando lleguen los datos del CRM. Los hechos tienen la llave correcta desde el inicio.

<!-- takeaways -->

- Carga las dimensiones antes que los hechos.
- Busca las llaves en la fecha del evento.
- Los inferred members manejan hechos que llegan antes.

<!-- unit: Cargas idempotentes y repetibles -->

<!-- goals -->

- Hacer idempotentes las cargas con MERGE o delete-insert.
- Correr backfills y conciliar los resultados con las fuentes.

<!-- concept -->

Toda carga se va a volver a correr algún día: tras una falla, un arreglo o datos tardíos. Una carga es segura de repetir solo si correrla dos veces da el mismo resultado, lo que significa reemplazar su porción de datos en lugar de anexar. `MERGE` sobre la llave del grano o borrar y reinsertar la ventana de carga lo logra.
Los backfills reutilizan la misma lógica sobre periodos pasados, y los chequeos de conciliación comparan totales con la fuente para demostrar el resultado.

<!-- example -->

```sql
MERGE INTO fct_order_lines t
USING stg_order_lines s
ON t.order_number = s.order_number AND t.line_number = s.line_number
WHEN MATCHED THEN UPDATE SET quantity = s.quantity, net_amount = s.net_amount, loaded_at = s.loaded_at
WHEN NOT MATCHED THEN INSERT (order_number, line_number, date_key, customer_key, product_key, quantity, net_amount, loaded_at)
VALUES (s.order_number, s.line_number, s.date_key, s.customer_key, s.product_key, s.quantity, s.net_amount, s.loaded_at);
```

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

<!-- challenge -->

Tras un backfill de marzo, los ingresos de marzo en el warehouse están 0,4 % por debajo del sistema fuente. ¿Cómo encuentras la diferencia?

<!-- solution -->

Concilia por día y luego por llave: compara conteos y sumas diarias con la fuente, y en los días que difieren busca las llaves de la fuente que faltan en el warehouse (filtros, búsquedas de llave fallidas, registros tardíos).

<!-- takeaways -->

- Las cargas idempotentes reemplazan su porción de datos.
- Los backfills reutilizan la misma lógica sobre el pasado.
- Concilia conteos y sumas con las fuentes.

<!-- unit: Fuentes y herramientas -->

<!-- goals -->

- Cargar datos de SaaS y usar dbt para las transformaciones.
- Manejar cambios de esquema en las fuentes y cargas en micro-batch.

<!-- concept -->

La mayoría de warehouses carga hoy desde decenas de herramientas SaaS y bases de datos. Los conectores administrados manejan APIs y paginación; dbt maneja las transformaciones como SQL versionado con pruebas y dependencias. Juntos cubren la mayor parte del ELT.
Las fuentes igual cambian por debajo: aparecen columnas, cambian tipos. Aterrizar los datos crudos con flexibilidad, detectar cambios de esquema y alertar convierte esas sorpresas en trabajo planeado. Los micro-batches bajan la latencia a minutos cuando lo diario no basta.

<!-- example -->

```text
Fivetran/Airbyte ─► raw schema (auto-added columns, alerts on change)
dbt: staging models (rename, cast) ─► core ─► marts, tests on each
schedule: every 15 minutes for orders, daily for finance
```

#### ¿Qué relación tiene la arquitectura medallion con el warehousing?

Es un patrón de lakehouse por capas (bronze en bruto, silver limpio y homogeneizado, gold listo para el negocio) que corresponde a las capas de staging, integración y presentación; gold suele contener esquemas en estrella de Kimball.

#### ¿Qué es una capa semántica?

Una capa que define una sola vez las métricas, dimensiones y relaciones de negocio (en la capa semántica de dbt, LookML, Cube, los modelos semánticos de Power BI, AtScale, las metric views) para que todas las herramientas calculen "ingresos" de la misma forma.

#### ¿Qué es un cubo OLAP?

Una estructura multidimensional que precalcula agregados entre dimensiones para cortar y rebanar rápido. MOLAP guarda los cubos en un almacenamiento especializado (SSAS), ROLAP consulta tablas relacionales y HOLAP mezcla ambos. Los warehouses columnares en la nube redujeron la necesidad de cubos físicos.

#### ¿Qué es un data warehouse virtual o la virtualización de datos?

Consultar datos de varias fuentes en su lugar mediante una capa de virtualización (Denodo, Trino, consultas federadas) sin consolidarlos físicamente. Es rápido para integrar, pero el rendimiento y el historial son limitados.

<!-- challenge -->

Un conector agrega solo una columna nueva a la tabla cruda, y un modelo aguas abajo con `SELECT *` rompe la herramienta de BI. ¿Cómo haces resiliente el pipeline?

<!-- solution -->

Selecciona columnas explícitas en los modelos de staging en lugar de `SELECT *`, impón contratos en los marts y alerta ante cambios de esquema en lo crudo, para que las columnas nuevas se agreguen a propósito.

<!-- takeaways -->

- Los conectores cargan datos de SaaS; dbt los transforma.
- Aterriza con flexibilidad, selecciona explícitamente.
- Los micro-batches bajan la latencia a minutos.

### Arquitecturas de warehouse

<!-- unit: Definir y probar la calidad -->

<!-- goals -->

- Nombrar las dimensiones de la calidad de datos y las pruebas que necesita toda tabla.
- Decidir dónde corren los chequeos y qué pasa cuando fallan.

<!-- concept -->

La calidad tiene varias dimensiones (completitud, exactitud, consistencia, oportunidad, validez, unicidad), y cada tabla necesita pruebas para las que le importan. Algunas aplican en todas partes: unicidad de la llave al grano, llaves no nulas, integridad referencial de hechos a dimensiones.
Dónde corren los chequeos decide qué atrapan: en la ingesta el formato, tras la transformación las reglas, antes de publicar como compuerta. La severidad decide la respuesta, de bloquear y alertar a advertir y registrar.

<!-- example -->

```yaml
models:
  - name: fct_order_lines
    tests:
      - dbt_utils.unique_combination_of_columns: {combination_of_columns: [order_number, line_number]}
    columns:
      - name: customer_key
        tests: [not_null, {relationships: {to: ref('dim_customer'), field: customer_key}}]
      - name: net_amount
        tests: [{dbt_utils.accepted_range: {min_value: -100000, max_value: 100000}}]
```

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

<!-- challenge -->

Una prueba de unicidad en una tabla de hechos falla a las 06:00. Los dashboards se refrescan a las 07:00. ¿Qué debe hacer el pipeline?

<!-- solution -->

Bloquear la publicación del mart afectado (dejando visibles los datos de ayer), alertar al dueño con las llaves que fallan y marcar los dashboards como desactualizados. Publicar duplicados confundiría a los usuarios.

<!-- takeaways -->

- Prueba llaves, nulos y relaciones en cada tabla.
- Revisa en la ingesta, la transformación y la publicación.
- La severidad decide bloquear, poner en cuarentena o advertir.

<!-- unit: Monitoreo y responsables -->

<!-- goals -->

- Monitorear la calidad con observabilidad, detección de anomalías y SLAs.
- Asignar responsables con contratos y stewards.

<!-- concept -->

Las pruebas atrapan lo que alguien anticipó; el monitoreo atrapa el resto. La observabilidad vigila frescura, volumen, esquema y distribuciones, y la detección de anomalías compara hoy con el histórico para señalar cambios bruscos que ninguna regla describía.
La calidad también es un acuerdo entre personas. Los contratos fijan lo que prometen los productores, los SLAs ponen metas medibles, los stewards son dueños de definiciones y arreglos, y cuantificar el costo de los datos malos justifica el esfuerzo.

<!-- example -->

| Señal | Chequeo |
|---|---|
| Frescura | `max(loaded_at)` a menos de 2 h de lo programado |
| Volumen | Conteo de filas a ±20 % del promedio de 7 días |
| Distribución | Tasa de nulos de `customer_key` < 0,1 % |
| Esquema | Columna agregada/quitada en la fuente → alerta |

#### ¿Qué son las tablas point-in-time (PIT) en Data Vault?

Tablas auxiliares que guardan, para cada clave de hub y fecha de foto, las fechas de carga de los satellites correspondientes, lo que agiliza armar el estado de una entidad en un momento dado para las dimensiones.

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

<!-- challenge -->

Todas las pruebas pasan, pero las ventas de ayer son la mitad de lo usual porque el feed de una tienda falló en silencio. ¿Qué chequeo lo habría atrapado?

<!-- solution -->

Un chequeo de anomalías sobre volumen o ingresos por tienda (o por fuente) frente al histórico reciente, que alerte cuando un segmento cae fuerte aunque los totales sigan pareciendo plausibles.

<!-- takeaways -->

- La observabilidad atrapa lo que las pruebas no anticiparon.
- Contratos y SLAs vuelven la calidad un acuerdo.
- Los stewards son dueños de definiciones y arreglos.

### Motores y almacenamiento

<!-- unit: Funciones de ventana -->

<!-- goals -->

- Usar funciones de ventana para totales acumulados, rankings y deduplicación.
- Calcular el crecimiento periodo contra periodo.

<!-- concept -->

Las funciones de ventana calculan sobre filas relacionadas sin colapsarlas, y por eso están en todas partes del warehousing. La partición define el grupo, el orden define la secuencia y el frame define qué filas cuentan. Con ellas, totales acumulados, rankings, selección de la última fila y comparaciones con el periodo anterior se vuelven una sola expresión.
Las funciones de ranking solo difieren en los empates, un detalle que cambia los resultados cuando se repiten valores.

<!-- example -->

```sql
WITH monthly AS (
  SELECT d.year_month, SUM(f.net_amount) AS revenue
  FROM fct_order_lines f JOIN dim_date d USING (date_key)
  GROUP BY 1
)
SELECT year_month, revenue,
       revenue / NULLIF(LAG(revenue) OVER (ORDER BY year_month), 0) - 1 AS mom_growth
FROM monthly;
```

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

<!-- challenge -->

Necesitas los 3 productos con más ingresos de cada categoría, incluidos los empates en el tercer puesto. ¿Qué función usas?

<!-- solution -->

`RANK()` o `DENSE_RANK()` sobre los ingresos con partición por categoría, filtrando rank ≤ 3. `ROW_NUMBER()` cortaría los empates arbitrariamente.

<!-- takeaways -->

- Las ventanas calculan sobre filas relacionadas sin agruparlas.
- `LAG` y los frames dan crecimiento y totales acumulados.
- Las funciones de ranking difieren en cómo tratan los empates.

<!-- unit: Patrones analíticos -->

<!-- goals -->

- Escribir consultas de cohortes, retención y actividad consecutiva.
- Calcular percentiles, agregados multinivel y pivots.

<!-- concept -->

La mayoría de solicitudes analíticas son variantes de unos pocos patrones. Las cohortes agrupan clientes por cuándo empezaron y los siguen en el tiempo. Las preguntas de actividad consecutiva comparan cada periodo con el anterior. Los percentiles describen distribuciones mejor que los promedios. Los agregados multinivel y los pivots dan forma a los resultados para reportes.
Reconocer el patrón detrás de una pregunta es la mayor parte del trabajo; el SQL viene después.

<!-- example -->

```sql
WITH firsts AS (
  SELECT customer_key, MIN(order_month) AS cohort FROM customer_months GROUP BY 1
)
SELECT f.cohort, m.order_month, COUNT(DISTINCT m.customer_key) AS active
FROM customer_months m JOIN firsts f USING (customer_key)
GROUP BY 1, 2 ORDER BY 1, 2;
```

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

<!-- challenge -->

Un reporte necesita ingresos por año, por año y trimestre, y un total general en un solo resultado. ¿Cómo lo escribes sin tres consultas?

<!-- solution -->

`GROUP BY ROLLUP(year, quarter)`, que devuelve subtotales por año, filas por trimestre y un total general; usa `GROUPING()` para etiquetar las filas de subtotal.

<!-- takeaways -->

- Las cohortes siguen a los clientes desde su primera actividad.
- Los percentiles describen datos sesgados mejor que los promedios.
- `ROLLUP`, `CUBE` y los pivots dan forma a las salidas de reportes.

<!-- unit: Escribir SQL correcto -->

<!-- goals -->

- Estructurar consultas con CTEs y filtrar en el lugar correcto.
- Evitar errores por división entre cero y NULLs.

<!-- concept -->

Las cifras erróneas en los reportes suelen venir de pequeños errores de SQL, no de lógica compleja. Filtrar después de agregar en lugar de antes, dividir entre cero u olvidar que `NULL` nunca es igual a nada cambian los resultados en silencio.
Una estructura legible es la mejor defensa: los CTEs nombran cada paso para que los revisores sigan la lógica, y manejar explícitamente `NULL` y el cero convierte supuestos ocultos en decisiones visibles.

<!-- example -->

```sql
WITH paid AS (
  SELECT customer_key, net_amount FROM fct_order_lines WHERE status = 'paid'   -- row filter: WHERE
)
SELECT customer_key, SUM(net_amount) AS revenue,
       SUM(net_amount) / NULLIF(COUNT(*), 0) AS avg_line
FROM paid
GROUP BY customer_key
HAVING SUM(net_amount) > 1000;                                               -- group filter: HAVING
```

#### ¿Cómo se hace rápida una consulta sobre un esquema en estrella?

Filtrando por columnas particionadas o agrupadas (la fecha), uniendo los hechos con dimensiones pequeñas (broadcast), seleccionando solo las columnas necesarias, preagregando las consultas comunes, manteniendo al día las estadísticas y evitando funciones sobre las columnas de filtro.

#### ¿Qué causa el "fan-out" o doble conteo en los joins?

Unir un hecho con una tabla que tiene varias filas por clave (muchos a muchos o un grano equivocado), de modo que cada fila de hecho se duplica y las sumas se inflan. Revisa la cardinalidad de los joins y exige la unicidad de las claves de las dimensiones.

#### ¿Cómo se acelera `COUNT(DISTINCT)` sobre muchos datos?

Usando funciones aproximadas (HyperLogLog: `APPROX_COUNT_DISTINCT`), preagregando los conjuntos distintos por periodo, o manteniendo los conteos distintos en tablas agregadas cuando se necesitan valores exactos.

#### ¿Por qué las tablas anchas desnormalizadas pueden ser rápidas en motores columnares?

Porque solo se leen las columnas que referencia la consulta, así que una tabla ancha no cuesta más que una angosta con las mismas filas, y evita joins. Los costos son el almacenamiento, el mantenimiento y la posible incoherencia.

<!-- challenge -->

Un join por `promotion_id` deja por fuera todas las ventas sin promoción, y los ingresos se ven bajos. ¿Qué pasó y cómo lo arreglas en el modelo?

<!-- solution -->

Las ventas tienen IDs de promoción `NULL`, y `NULL` nunca empareja en un join, así que un inner join las elimina. Asigna las promociones faltantes a un miembro desconocido/sin promoción en el hecho (o usa un left join).

<!-- takeaways -->

- Los CTEs hacen legible cada paso.
- `NULLIF` evita la división entre cero.
- Las llaves `NULL` no se unen; usa miembros desconocidos.

<!-- stage: Plataformas y rendimiento -->

### Rendimiento

<!-- unit: MPP y almacenamiento columnar -->

<!-- goals -->

- Explicar MPP y por qué los motores analíticos guardan los datos por columna.
- Describir codificaciones de compresión y ejecución vectorizada.

<!-- concept -->

Los motores analíticos están hechos para un tipo de trabajo: escanear muchas filas pero pocas columnas. Guardar cada columna junta hace que una consulta lea solo lo que usa, y los valores parecidos lado a lado se comprimen muchísimo. Procesar valores en lotes con ciclos amigables para la CPU acelera cada escaneo.
El procesamiento masivamente paralelo agrega escala: los datos se reparten entre nodos que trabajan su parte al mismo tiempo, así que agregar nodos agrega velocidad.

<!-- example -->

| Organización | Leer `SUM(amount)` sobre 1.000 M filas × 50 columnas |
|---|---|
| Almacén por filas | Lee las 50 columnas |
| Almacén columnar | Lee 1 columna, comprimida ~10× |

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

<!-- challenge -->

Un equipo guarda una columna de estado como cadenas largas tipo "ORDER_STATUS_SHIPPED". ¿Importa en un warehouse columnar?

<!-- solution -->

Menos que en un almacén por filas, porque la codificación por diccionario comprime bien los valores repetidos. Aun así, códigos cortos o enteros pequeños reducen memoria y costo de comparación; deja las descripciones en una dimensión.

<!-- takeaways -->

- El almacenamiento columnar lee solo las columnas necesarias.
- Las codificaciones comprimen mucho los valores repetidos.
- MPP reparte el trabajo entre nodos.

<!-- unit: Organización de los datos -->

<!-- goals -->

- Usar llaves de distribución, sort keys, clustering y particionamiento.
- Explicar cómo los zone maps y las estadísticas ayudan al optimizador.

<!-- concept -->

Cómo se ubican los datos decide cuánto debe leer y mover una consulta. Particionar y ordenar permite al motor saltarse bloques cuyos valores mínimo y máximo no pueden cumplir un filtro. La distribución decide qué nodo guarda qué filas, así los joins por la llave de distribución ocurren sin mover datos.
Las estadísticas le dicen al optimizador qué tan grandes son las tablas y cómo se reparten los valores, lo que guía el orden y la estrategia de los joins. Estadísticas viejas producen malos planes sobre buenos datos.

<!-- example -->

```sql
-- Redshift
CREATE TABLE fct_order_lines (...)
DISTKEY (customer_key)
SORTKEY (date_key);
-- Snowflake / BigQuery equivalent idea: CLUSTER BY (date_key)
```

#### ¿Cómo se evitan los `SELECT DISTINCT` costosos en los modelos?

Buscando por qué aparecen los duplicados (un join con el grano equivocado) y corrigiendo el join en lugar de ocultarlo con `DISTINCT`, que es costoso y esconde problemas de datos.

#### ¿Cómo se prueba el rendimiento del warehouse antes de salir a producción?

Reproduciendo consultas representativas y la concurrencia sobre datos del tamaño de producción, midiendo la latencia y el costo por consulta, revisando los planes en cuanto a pruning y joins, y ajustando la organización, los agregados y el tamaño del warehouse.

#### ¿Cómo pueden los modelos incrementales reducir los costos del warehouse?

Transformando en cada ejecución solo los datos nuevos o modificados en lugar de reconstruir tablas completas, lo que reduce drásticamente el cómputo en los hechos grandes; requieren un manejo cuidadoso de los datos tardíos y de los backfills.

#### ¿Cuáles son los principales warehouses en la nube?

Snowflake, Google BigQuery, Amazon Redshift (aprovisionado y Serverless), los warehouses de Azure Synapse y Microsoft Fabric, y Databricks SQL sobre el lakehouse. Se diferencian en arquitectura, modelos de precios e integración con el ecosistema.

#### ¿Cómo funciona BigQuery y cómo se cobra?

BigQuery es serverless: el almacenamiento está en un formato columnar (Capacitor) sobre Colossus y el cómputo se asigna como slots de Dremel. Se cobra bajo demanda por TB escaneado o por capacidad (ediciones con slots reservados o con autoescalado), más el almacenamiento.

<!-- challenge -->

Una consulta que filtra un día de una tabla de hechos de 3 años lee el 80 % de sus bloques. ¿Qué revisas?

<!-- solution -->

Si la tabla está ordenada, con clustering o particionada por fecha, y si el filtro aplica directamente sobre esa columna (no a través de una función). Revisa la profundidad de clustering o el estado de vacuum/sort si los datos se cargaron desordenados.

<!-- takeaways -->

- Ordenar y particionar permite saltarse bloques.
- Las llaves de distribución colocan juntos los datos que se cruzan.
- Las estadísticas frescas producen buenos planes.

<!-- unit: Cómputo y concurrencia -->

<!-- goals -->

- Separar almacenamiento y cómputo y manejar cargas de trabajo.
- Usar vistas materializadas, caché de resultados y opciones de escalado.

<!-- concept -->

Los warehouses en la nube separan almacenamiento y cómputo, así que varios clústeres independientes pueden leer los mismos datos. Eso cambia el manejo de la carga: cómputo separado por carga evita que el ETL frene los dashboards, escalar hacia afuera atiende más usuarios y escalar hacia arriba acelera consultas individuales.
La caché y el precálculo reducen aún más el trabajo: la caché de resultados responde al instante consultas repetidas y las vistas materializadas mantienen listos resultados costosos.

<!-- example -->

| Problema | Palanca |
|---|---|
| El ETL frena los dashboards a las 08:00 | Cómputo separado por carga |
| Una consulta pesada es lenta | Escalar hacia arriba |
| 200 usuarios en fila a las 09:00 | Escalar hacia afuera (multi-cluster) |
| La misma consulta de dashboard 500 veces al día | Caché de resultados / vista materializada |

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

<!-- challenge -->

Los dashboards de la mañana hacen fila detrás del ETL nocturno, que termina tarde. El warehouse es un solo clúster. ¿Qué propones?

<!-- solution -->

Dar cómputo separado al ETL y a BI (warehouses o colas con workload management), para que BI nunca espere al ETL. Luego arreglar aparte el retraso del ETL.

<!-- takeaways -->

- Separar almacenamiento y cómputo permite aislar cargas.
- Escala hacia arriba para velocidad; hacia afuera para concurrencia.
- Caché y vistas materializadas evitan repetir trabajo.

### Warehouses en la nube

<!-- unit: Consultas estrella rápidas -->

<!-- goals -->

- Hacer que las consultas sobre estrellas poden y crucen con eficiencia.
- Elegir tipos de datos y tablas anchas por velocidad.

<!-- concept -->

Las consultas estrella rápidas comparten un perfil: filtran por columnas particionadas o con clustering, cruzan un hecho grande con dimensiones pequeñas y leen pocas columnas. Revisar la poda en el perfil de la consulta es el primer paso cuando algo va lento.
En motores columnares, las tablas anchas desnormalizadas pueden ser rápidas porque las columnas sin usar no cuestan nada. Los tipos de datos compactos ayudan siempre: llaves y fechas más pequeñas se escanean, cruzan y comprimen mejor.

<!-- example -->

```text
Query profile: fct_order_lines
  partitions scanned: 31 of 1,826   ✔ pruning on date_key
  bytes scanned: 4.2 GB
  join: broadcast dim_product (12 MB) ✔
```

#### ¿Cómo maneja BigQuery el particionado y el clustering?

Las tablas se pueden particionar por una columna de fecha/marca de tiempo, por tiempo de ingesta o por rango de enteros, y agrupar por hasta cuatro columnas; las consultas que filtran por ellas leen menos bytes, lo que reduce directamente el costo bajo demanda.

#### ¿Qué es Redshift Spectrum?

Una función que permite a Redshift consultar datos en S3 mediante tablas externas del Glue Data Catalog, uniendo datos del lake con tablas del warehouse, facturada por bytes escaneados.

#### ¿Qué es el warehouse de Microsoft Fabric?

Una plataforma analítica SaaS en la que los warehouses y lakehouses guardan los datos en formato Delta en OneLake, se consultan con T-SQL y Spark, y se sirven a Power BI con el modo Direct Lake.

#### ¿Qué es Databricks SQL como warehouse?

SQL warehouses sobre el lakehouse de Databricks que consultan tablas Delta gobernadas por Unity Catalog, con Photon, cómputo serverless y conectores de BI, que ofrecen funciones de warehouse sobre almacenamiento abierto.

#### ¿Qué hace que un modelo de datos sea fácil para BI?

Esquemas en estrella con nombres claros, definiciones de negocio documentadas, dimensiones conformadas, granos correctos, claves sustitutas ocultas para los usuarios, un manejo coherente de las fechas y una capa semántica para las métricas.

<!-- challenge -->

Las llaves de join son UUIDs de 36 caracteres, y los joins sobre un hecho de 2.000 millones de filas son lentos. ¿Qué cambias?

<!-- solution -->

Usa llaves sustitutas enteras en hechos y dimensiones (conserva el UUID como atributo de llave natural). Los joins y comparaciones de enteros son mucho más baratos y comprimen mejor.

<!-- takeaways -->

- Revisa primero la poda cuando una consulta va lenta.
- Cruza hechos grandes con dimensiones pequeñas.
- Los tipos compactos abaratan escaneos y joins.

<!-- unit: Joins y conteos distintos -->

<!-- goals -->

- Reconocer y corregir el fan-out y los DISTINCT innecesarios.
- Acelerar conteos distintos y dimensiones muy grandes.

<!-- concept -->

Dos hábitos vuelven las consultas lentas y erradas a la vez. Cruzar al grano equivocado multiplica filas, y agregar `DISTINCT` para esconder los duplicados duplica el costo y deja la causa raíz. Corregir el join es la solución real.
Los conteos distintos sobre datos enormes son caros por naturaleza; las funciones aproximadas o los conjuntos preagregados los vuelven asequibles. Las dimensiones muy grandes necesitan el mismo cuidado que los hechos: clustering, menos versiones y joins sobre llaves compactas.

<!-- example -->

```sql
SELECT date_key, APPROX_COUNT_DISTINCT(customer_key) AS customers   -- HyperLogLog, ~1–2% error
FROM fct_page_views
WHERE date_key BETWEEN 20261001 AND 20261031
GROUP BY date_key;
```

#### ¿Qué diferencia hay entre un reporte y un dashboard?

Un reporte presenta datos detallados, a menudo en tablas y paginados, para análisis o fines regulatorios. Un dashboard resume visualmente las métricas clave para monitorear de un vistazo, con desglose.

#### ¿Qué es el BI de autoservicio y cuáles son sus riesgos?

Usuarios de negocio que construyen sus propios análisis a partir de datasets gobernados. Riesgos: definiciones de métricas inconsistentes, lógica duplicada, extracciones y costos sin control. Una capa semántica, datasets certificados y formación los reducen.

#### ¿Qué es la seguridad a nivel de fila en BI y en los warehouses?

Restringir qué filas ve cada usuario según su identidad (región, departamento), implementada en el warehouse (row access policies, vistas seguras) o en la capa de BI, para que un dataset sirva con seguridad a muchas audiencias.

#### ¿Cómo se documenta un warehouse?

Con descripciones de tablas y columnas en el catálogo (dbt docs, Unity Catalog, Glue, DataHub), un glosario de negocio para las métricas, grafos de linaje, responsables y SLA, y ejemplos de consultas correctas.

<!-- challenge -->

Un modelo termina con `SELECT DISTINCT *` "para quitar duplicados" y tarda 40 minutos. ¿Qué haces?

<!-- solution -->

Encuentra qué join introduce duplicados (una tabla con varias filas por llave), corrige el grano del join (agrega o filtra esa tabla antes), agrega una prueba de unicidad sobre la llave de salida y quita el `DISTINCT`.

<!-- takeaways -->

- El fan-out viene de cruzar al grano equivocado.
- Corrige los joins en vez de taparlos con `DISTINCT`.
- Los conteos distintos aproximados escalan a datos enormes.

<!-- unit: Dashboards y costo -->

<!-- goals -->

- Acelerar dashboards lentos con agregados y tablas de cobertura.
- Probar el rendimiento antes de salir en vivo y bajar costos con modelos incrementales.

<!-- concept -->

Los dashboards repiten las mismas preguntas, así que su trabajo de rendimiento consiste en no recalcular respuestas: agregados o vistas materializadas al grano que necesitan las gráficas, tablas de cobertura con exactamente las columnas que usa una consulta frecuente.
Costo y velocidad suelen ir juntos. Los modelos incrementales transforman solo los datos nuevos, y probar con volúmenes y concurrencia realistas antes del lanzamiento evita descubrir los límites frente a los usuarios.

<!-- example -->

```text
dashboard "Sales overview": 9 charts
  before: each chart scans fct_order_lines (1.4 B rows) → 25 s
  after:  agg_sales_day_store_category (3 M rows), refreshed hourly → 1.5 s
```

#### ¿Qué es un dataset certificado?

Un dataset marcado como confiable tras una revisión (definiciones, pruebas, responsable), destacado en las herramientas de BI y los catálogos para que los usuarios lo prefieran frente a copias personales o experimentales.

#### ¿Qué es el reverse ETL?

Enviar datos del warehouse (segmentos, puntajes, métricas) de vuelta a herramientas operativas como CRM, plataformas de marketing o de soporte, para que los equipos de negocio actúen sobre datos modelados (Hightouch, Census, jobs propios).

#### ¿Cómo se decide entre consultas en vivo y extracciones en las herramientas de BI?

Las consultas en vivo dan datos frescos y seguridad centralizada pero dependen del rendimiento y el costo del warehouse; las extracciones (extracts de Tableau, import de Power BI, SPICE) son rápidas y baratas por consulta pero quedan desactualizadas y duplicadas. Se elige por dashboard según la necesidad de frescura y el uso.

#### ¿Cómo se asegura un data warehouse?

Con roles de mínimo privilegio (roles de acceso concedidos a roles funcionales), SSO y MFA, restricciones de red, cifrado en reposo y en tránsito, enmascaramiento de las columnas sensibles, seguridad a nivel de fila, auditoría de los accesos y entornos separados para desarrollo y producción.

<!-- challenge -->

Un proyecto dbt reconstruye sus 300 modelos cada hora, y los costos del warehouse se triplicaron. ¿Qué cambias primero?

<!-- solution -->

Vuelve incrementales los modelos de hechos grandes (procesar solo filas nuevas o cambiadas), reconstruye los modelos pequeños con menos frecuencia y corre cada hora solo los modelos que los dashboards necesitan cada hora.

<!-- takeaways -->

- Precalcula lo que los dashboards preguntan una y otra vez.
- Prueba con datos y concurrencia realistas.
- Los modelos incrementales bajan costo y tiempo.

### BI y consumo

<!-- unit: El panorama de warehouses en la nube -->

<!-- goals -->

- Describir los principales warehouses en la nube y cómo funcionan.
- Comparar BigQuery, Redshift, Fabric y Databricks SQL.

<!-- concept -->

Los warehouses en la nube comparten las mismas ideas de base, almacenamiento columnar, MPP y cómputo separado, pero difieren en cuánto administras tú y en cómo pagas. BigQuery es completamente serverless. Redshift ofrece clústeres y un modo serverless. Fabric y Databricks SQL construyen warehouses sobre formatos de lago abiertos.
Conocer la arquitectura detrás de cada uno explica sus palancas de ajuste y su precio.

<!-- example -->

| Warehouse | Modelo de cómputo | Almacenamiento |
|---|---|---|
| Snowflake | Virtual warehouses (créditos) | Administrado, micro-particiones |
| BigQuery | Slots (on-demand o reservados) | Columnar administrado |
| Redshift | Clústeres RA3 o RPUs serverless | Almacenamiento administrado + S3 |
| Fabric | Unidades de capacidad | Delta en OneLake |
| Databricks SQL | SQL warehouses (DBUs) | Delta / Iceberg vía Unity Catalog |

#### ¿Cómo se manejan los datos personales en un warehouse?

Clasificándolos y etiquetándolos, minimizando lo que se carga, seudonimizando o tokenizando los identificadores desde el principio, enmascarando para la mayoría de los usuarios, restringiendo el acceso en bruto, aplicando políticas de retención y atendiendo las solicitudes de supresión (RGPD, Ley 1581 de 2012 de habeas data en Colombia) con procesos documentados.

#### ¿Qué es el linaje de datos y por qué importa?

El registro de dónde vienen los datos y cómo se transforman, a nivel de tabla y de columna. Sirve para analizar el impacto antes de los cambios, depurar cifras erróneas, las auditorías y la confianza.

#### ¿Qué es un catálogo de datos?

Un inventario consultable de datasets con descripciones, responsables, esquemas, etiquetas, linaje, estado de calidad y uso, que ayuda a encontrar y entender los datos (DataHub, Collibra, Alation, Unity Catalog, Glue Data Catalog).

#### ¿Qué son las políticas de retención de datos?

Reglas sobre cuánto tiempo se conserva cada dataset (por razones legales, de negocio y de costo), implementadas con el borrado de particiones, reglas de ciclo de vida, ajustes de Time Travel y archivado, y documentadas para el cumplimiento.

#### ¿Qué son las funciones de ventana y por qué son esenciales en el warehousing?

Funciones que calculan valores sobre un conjunto de filas relacionadas con la fila actual sin colapsarlas (`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`, `SUM() OVER`). Sirven para deduplicar, calcular totales acumulados, comparar periodos y armar sesiones.

<!-- challenge -->

Un equipo que pasa de Redshift a BigQuery pregunta dónde se configuran las llaves de distribución y de ordenamiento. ¿Qué le dices?

<!-- solution -->

BigQuery no tiene llaves de distribución; administra la ubicación. Los equivalentes son el particionamiento (normalmente por fecha) y el clustering sobre columnas de filtro comunes, además de controlar los bytes escaneados, ya que el precio on-demand cobra por datos leídos.

<!-- takeaways -->

- Todos comparten almacenamiento columnar y MPP.
- Difieren en administración y modelo de precio.
- Las palancas de ajuste siguen a cada arquitectura.

<!-- unit: Elegir y pagar un warehouse -->

<!-- goals -->

- Entender los costos de los warehouses en la nube y elegir plataforma.
- Usar el particionamiento de BigQuery y Redshift Spectrum, y planear migraciones.

<!-- concept -->

El cómputo domina la factura del warehouse, y cada plataforma lo mide distinto: créditos, slots, RPUs o DBUs. Los costos siguen más a los hábitos que a los precios: clústeres ociosos, reconstrucciones completas y escaneos sin filtro.
Elegir plataforma parte del contexto: la nube en la que estás, la forma de las cargas, las habilidades, el ecosistema y el gobierno. Migrar a ella es un proyecto de inventario, traducción y validación, no una copia.

<!-- example -->

```sql
-- BigQuery: partition and cluster to cut bytes scanned
CREATE TABLE sales.fct_order_lines
PARTITION BY order_date
CLUSTER BY customer_key, product_key
AS SELECT * FROM staging.order_lines;
```

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

<!-- challenge -->

Tras migrar a la nube, la factura mensual es el doble de lo estimado. Nombra tres causas probables.

<!-- solution -->

Cómputo encendido sin uso (sin auto-suspend), jobs que reconstruyen tablas completas en vez de cargas incrementales y consultas que escanean tablas sin particionar ni clustering. Una cuarta: consultas en vivo de BI sin caché.

<!-- takeaways -->

- El cómputo domina; los hábitos mueven el costo.
- Elige por contexto, cargas y habilidades.
- Las migraciones necesitan inventario, traducción y validación.

<!-- unit: Datos abiertos y compartición -->

<!-- goals -->

- Compartir datos en vivo sin copias.
- Explicar qué significan los formatos de tabla abiertos para los warehouses.

<!-- concept -->

Copiar datos para compartirlos crea duplicados desactualizados y huecos de seguridad. La compartición zero-copy da a otras cuentas o empresas acceso en vivo y de solo lectura a los mismos datos, gobernado por el dueño.
Los formatos de tabla abiertos llevan la idea más lejos: warehouses, Spark y otros motores leen y escriben las mismas tablas Iceberg o Delta en tu almacenamiento, así el warehouse se vuelve un motor entre varios y no un almacén cerrado.

<!-- example -->

```text
producer account: share sales.daily_revenue → partner account (read-only, live)
open tables: Iceberg in S3 ◄── Snowflake, Spark, Trino all read the same files
```

#### ¿Qué es una consulta de análisis de cohortes?

Asignar cada cliente a una cohorte (mes de primera compra) y luego contar los clientes activos o los ingresos por cohorte y meses desde la primera compra, a menudo pivotado en un triángulo de retención.

#### ¿Cómo se calcula una mediana o un percentil?

Con `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x)` en muchos motores, `MEDIAN()` en Snowflake, o `APPROX_PERCENTILE`/`APPROX_QUANTILES` para muchos datos.

<!-- challenge -->

Un socio recibe cada noche una exportación CSV de 20 tablas, a menudo con un día de retraso y a veces incompleta. ¿Qué propones?

<!-- solution -->

Comparte las tablas curadas con la compartición zero-copy del warehouse (o Delta Sharing / Iceberg vía un catálogo), para que el socio consulte datos en vivo con permisos que tú controlas y sin transferencia de archivos.

<!-- takeaways -->

- La compartición zero-copy reemplaza las exportaciones.
- Los formatos de tabla abiertos dejan que muchos motores compartan tablas.
- El warehouse se vuelve un motor entre varios.

<!-- stage: Servir y gobernar -->

### Gobierno y seguridad

<!-- unit: Modelos listos para BI -->

<!-- goals -->

- Hacer los modelos de datos amigables para herramientas y usuarios de BI.
- Elegir entre reportes, dashboards, consultas en vivo y extractos.

<!-- concept -->

Un modelo está listo para BI cuando un usuario de negocio puede armar una gráfica correcta sin preguntarle a nadie: nombres claros, medidas documentadas, dimensiones conformadas y relaciones correctas. Los esquemas estrella encajan de forma natural en las herramientas de BI.
También importa cómo llegan los datos a la herramienta. Las consultas en vivo mantienen frescos los datos y centralizada la seguridad; los extractos dan velocidad y alivian el warehouse. Reportes y dashboards sirven necesidades distintas, y el reverse ETL empuja resultados a las herramientas operativas donde la gente ya trabaja.

<!-- example -->

| Necesidad | Elección |
|---|---|
| Listado regulatorio mensual | Reporte paginado |
| Monitoreo diario de KPIs | Dashboard |
| Datos que cambian cada pocos minutos | Consulta en vivo |
| 500 lectores, datos que cambian a diario | Extracto / caché |
| Los vendedores necesitan scores en el CRM | Reverse ETL |

#### ¿Qué son `GROUPING SETS`, `ROLLUP` y `CUBE`?

Extensiones de `GROUP BY` que calculan varios niveles de agregación en una consulta: `ROLLUP(year, month)` da totales por mes, por año y general; `CUBE` da todas las combinaciones; `GROUPING SETS` enumera las combinaciones exactas.

#### ¿Qué es una CTE y cuándo usarla?

Una common table expression (`WITH nombre AS (...)`) le da nombre a una subconsulta para la legibilidad y la reutilización dentro de una consulta; las CTE recursivas recorren jerarquías. Facilitan la revisión del SQL complejo del warehouse.

#### ¿Cómo se evitan los errores de división por cero?

Con `NULLIF(denominador, 0)` para que el resultado sea `NULL` en lugar de un error, o con funciones de división segura (`SAFE_DIVIDE` en BigQuery, `DIV0` en Snowflake).

#### ¿Qué diferencia hay entre `WHERE` y `HAVING`?

`WHERE` filtra las filas antes de agregar; `HAVING` filtra los grupos después de agregar. Filtrar temprano con `WHERE` es más barato.

<!-- challenge -->

Un dashboard con 400 lectores diarios corre consultas en vivo contra el warehouse cada vez que alguien lo abre, aunque los datos se actualizan una vez al día. ¿Qué cambias?

<!-- solution -->

Usa un extracto o dataset en caché refrescado tras la carga diaria, para que los lectores consulten la caché y el warehouse corra las consultas una sola vez.

<!-- takeaways -->

- Nombres claros y estrellas hacen los modelos amigables para BI.
- Consultas en vivo por frescura; extractos por velocidad.
- El reverse ETL lleva los datos a las herramientas operativas.

<!-- unit: Autoservicio con barandas -->

<!-- goals -->

- Habilitar BI de autoservicio manteniendo consistentes las cifras.
- Proteger filas, documentar modelos y certificar datasets.

<!-- concept -->

El autoservicio deja que los usuarios de negocio respondan sus propias preguntas, lo que escala mucho mejor que una fila de solicitudes. Sin barandas, produce métricas contradictorias y datos expuestos. Las barandas son datasets gobernados y certificados con definiciones documentadas, seguridad por fila que sigue al usuario y documentación donde la gente mira.
La certificación es la señal que necesitan los usuarios: este dataset está revisado, probado y tiene dueño.

<!-- example -->

```sql
-- row-level security (Snowflake row access policy)
CREATE ROW ACCESS POLICY region_rls AS (region STRING) RETURNS BOOLEAN ->
  EXISTS (SELECT 1 FROM security.user_regions u
          WHERE u.user_name = CURRENT_USER() AND u.region = region);
ALTER TABLE marts.fct_sales ADD ROW ACCESS POLICY region_rls ON (region);
```

#### ¿Cómo se manejan los NULL en joins y agregaciones?

`NULL` nunca es igual a nada, así que las filas con claves `NULL` no se unen (usa miembros desconocidos o `IS NOT DISTINCT FROM`); las agregaciones ignoran los `NULL` salvo `COUNT(*)`; usa `COALESCE` para los valores por defecto al mostrar.

#### ¿Cómo se pivotan filas en columnas con SQL?

Con agregación condicional (`SUM(CASE WHEN channel = 'web' THEN amount END) AS web_amount`), portable entre motores, o con `PIVOT` donde se admita (Snowflake, SQL Server, BigQuery, Databricks).

#### Diseña un data mart de ventas para una empresa de comercio electrónico.

Proceso de negocio: líneas de pedido. Grano: una fila por línea de pedido. Dimensiones: fecha (pedido, envío), cliente (SCD2 sobre segmento y región), producto (SCD2 sobre categoría), tienda o canal, promoción y una junk dimension para los indicadores; dimensión degenerada el número de pedido. Hechos: cantidad, monto bruto, descuento, monto neto, costo, impuestos. Después se añaden un hecho de devoluciones y una foto diaria de inventario que comparten las dimensiones conformadas.

#### Finanzas y ventas reportan cifras de ingresos distintas. ¿Cómo lo resuelves?

Busco la definición de cada equipo (bruto o neto, fecha de reserva o de envío, conversión de moneda, reembolsos, cancelaciones), sigo ambas cifras con el linaje hasta las fuentes, acuerdo una sola definición con los responsables de negocio, la implemento una vez en la capa semántica o en un hecho conformado y retiro la lógica divergente.

<!-- challenge -->

Los gerentes regionales deben ver solo las ventas de su región en todas las herramientas, no solo en un dashboard. ¿Dónde lo implementas?

<!-- solution -->

En el warehouse, con una row access policy (o vistas seguras) basada en un mapeo de usuario a región, para que toda herramienta que consulte los datos reciba la misma restricción. Los filtros de la herramienta por sí solos se saltan fácil.

<!-- takeaways -->

- El autoservicio necesita datasets gobernados y certificados.
- La seguridad por fila va en el warehouse.
- Documenta las definiciones donde los usuarios miran.

### SQL para analítica

<!-- unit: Proteger los datos del warehouse -->

<!-- goals -->

- Proteger un warehouse con roles, controles de red y cifrado.
- Manejar datos personales y fijar políticas de retención.

<!-- concept -->

La seguridad del warehouse sigue el mínimo privilegio: los roles de acceso tienen privilegios sobre objetos, los roles funcionales los agrupan por cargo y los usuarios reciben roles funcionales vía SSO. Las restricciones de red y el cifrado agregan capas alrededor.
Los datos personales necesitan su propio tratamiento: clasificarlos y etiquetarlos, cargar solo lo necesario, seudonimizar temprano y enmascararlos para la mayoría de usuarios. Las políticas de retención deciden cuánto tiempo se queda cada dataset, por razones legales y de costo.

<!-- example -->

```text
access roles:     sales_read, sales_write, pii_read
functional roles: analyst_sales = sales_read
                  data_engineer = sales_read + sales_write
users ← functional roles via SSO groups; pii_read only for a few
```

#### La carga diaria de una tabla de hechos a veces crea duplicados. ¿Cómo lo corriges?

Hago idempotente la carga (`MERGE` sobre la clave del grano o delete-insert de la ventana de carga), deduplico staging por clave natural, añado una prueba de unicidad al grano que bloquee la publicación y reviso si la extracción del origen tiene ventanas solapadas.

#### Una dimensión debe conservar el historial de los cambios de segmento del cliente, pero la dirección cambia a diario. ¿Qué haces?

Sigo el segmento como SCD2 en la dimensión de cliente; pongo la dirección en una dimensión o minidimensión aparte, o la mantengo como tipo 1 si su historial no se necesita para el análisis, para evitar la explosión diaria de filas.

#### ¿Cómo migrarías un warehouse on-premises a la nube?

Inventariando las fuentes, los jobs de ETL, los reportes y los usuarios; eligiendo la plataforma y la arquitectura destino; migrando el historial de forma masiva; reconstruyendo los pipelines como ELT (a menudo con dbt) en lugar de un simple "lift-and-shift" cuando aporte valor; redefiniendo la seguridad y el gobierno; validando con reportes de conciliación; ejecutando en paralelo; cambiando los reportes por olas; y dando de baja el sistema viejo.

<!-- challenge -->

Cualquier analista puede consultar los correos y teléfonos crudos de los clientes. ¿Qué cambias sin romper su trabajo?

<!-- solution -->

Aplica políticas de enmascaramiento a las columnas PII (visibles solo para un rol privilegiado), ofrece llaves seudonimizadas para joins y conteos, y revisa quién necesita de verdad los valores crudos.

<!-- takeaways -->

- Mínimo privilegio con roles de acceso y funcionales.
- Clasifica, minimiza y enmascara los datos personales.
- Las políticas de retención limitan el riesgo legal y el costo.

<!-- unit: Linaje y descubrimiento -->

<!-- goals -->

- Usar linaje y catálogos para que los datos se entiendan.
- Ayudar a los analistas a encontrar las tablas correctas.

<!-- concept -->

Cuando un warehouse crece, encontrar la tabla correcta se vuelve el cuello de botella. Un catálogo hace buscables los datasets, con descripciones, dueños y señales de calidad; el linaje muestra de dónde viene cada tabla y qué depende de ella, lo que genera confianza y apoya el análisis de impacto.
La organización ayuda tanto como las herramientas: esquemas por capa y dominio, datasets certificados y menos tablas casi duplicadas.

<!-- example -->

```text
search "revenue" →
  marts.fct_revenue        ✔ certified · owner: finance-data · refreshed 06:40 · used by 34 dashboards
  sandbox.revenue_test_v2  ✘ uncertified · owner: a.lopez · last used 4 months ago
```

#### Las consultas sobre una tabla de hechos de 5 años se volvieron lentas a medida que crecieron los datos. ¿Qué revisas?

Si las consultas filtran por la columna de partición o de clustering, la degradación de la organización de los datos (profundidad de clustering, archivos pequeños), estadísticas faltantes, joins nuevos que multiplican filas, consultas de BI sin filtro de fecha, y si tablas agregadas o vistas materializadas servirían los patrones comunes.

#### ¿Cómo le explicas un data warehouse a una persona de negocio?

Es la historia confiable y ordenada de los datos de la empresa: la información de todos los sistemas reunida, limpiada y descrita una sola vez, para que todos respondan las preguntas de negocio con las mismas cifras.

#### ¿Cómo modelarías las suscripciones de una empresa SaaS?

Una dimensión de suscripción (plan, periodo de facturación, estado en SCD2), un hecho transaccional para los eventos de suscripción (alta, mejora, reducción, cancelación) y un hecho de foto periódica mensual con el MRR por cliente y plan, que permite analizar churn, expansión y cohortes.

<!-- challenge -->

Los analistas siguen usando una tabla de ingresos vieja y sin mantenimiento porque aparece primero en la búsqueda. ¿Qué haces?

<!-- solution -->

Certifica la tabla mantenida y marca la vieja como deprecada en el catálogo, redirígela o reemplázala por una vista sobre la nueva, avisa a sus usuarios encontrados en los logs de consultas y luego elimínala.

<!-- takeaways -->

- Los catálogos hacen los datos encontrables y confiables.
- El linaje apoya la confianza y el análisis de impacto.
- Certifica las tablas correctas; depreca el resto.

<!-- stage: Juntarlo todo -->

### Escenarios

<!-- unit: Diseñar un mart de ventas -->

<!-- goals -->

- Diseñar un mart dimensional de ventas de punta a punta.
- Justificar las decisiones de grano, hechos, dimensiones y SCD.

<!-- concept -->

Una pregunta de diseño de data mart evalúa si sabes aplicar el método bajo presión. Empieza por el proceso de negocio y el grano, lista las dimensiones con sus políticas de cambio, define los hechos y su aditividad, y luego cubre la carga, la calidad y cómo lo consultarán los usuarios. Decir qué harías con devoluciones, monedas y datos tardíos muestra experiencia más allá del libro.

<!-- example -->

```text
process: order taking   grain: order line
dims: date (order, ship roles), customer (SCD2 segment), product (SCD2 category),
      store, promotion, junk flags
facts: quantity, gross, discount, net (additive), returns as negative lines
load: incremental MERGE on (order_number, line_number); tests on keys and relationships
```

#### Los analistas se quejan de que no encuentran las tablas correctas. ¿Qué haces?

Organizo los esquemas por capa y dominio, documento los modelos y las columnas, certifico los datasets clave, publico un catálogo con búsqueda y linaje, marco como obsoletas y elimino las tablas heredadas, y ofrezco una capa semántica con métricas con nombres de negocio.

<!-- challenge -->

El negocio agrega: "también queremos saber qué productos vieron los clientes sin comprarlos". ¿Cómo cambia tu diseño?

<!-- solution -->

Agrega un hecho aparte para las vistas de producto (una fila por evento de vista, factless o con tiempo de permanencia), que comparta las dimensiones conformadas de cliente, producto y fecha, y compáralo con las ventas por drill-across.

<!-- takeaways -->

- Parte del proceso y el grano; luego dimensiones y hechos.
- Aborda explícitamente devoluciones, monedas y datos tardíos.
- Los procesos nuevos llevan hechos nuevos sobre dimensiones conformadas.

<!-- unit: Modelar suscripciones -->

<!-- goals -->

- Modelar un negocio de suscripciones con los tipos de hechos adecuados.
- Calcular ingreso recurrente y churn desde el modelo.

<!-- concept -->

Las suscripciones mezclan eventos y estados. Altas, upgrades y cancelaciones son eventos; el ingreso recurrente mensual y el estado activo son estados en un momento dado. Un buen modelo captura ambos: hechos transaccionales para los cambios y un periodic snapshot para el estado mensual, con la suscripción como dimensión de cambio lento. Así métricas como MRR, churn y expansión se vuelven consultas simples en lugar de reconstrucciones complejas.

<!-- example -->

```text
dim_subscription (plan, billing_period, status; SCD2)
fct_subscription_events (date, subscription, event_type, mrr_delta)
fct_subscription_monthly (month, subscription, customer, mrr, is_active)   ← periodic snapshot
churned MRR(month) = SUM(mrr) last month for subscriptions inactive this month
```

#### ¿Cómo diseñarías el warehouse de una empresa que adquiere otras empresas con frecuencia?

Una capa de integración resiliente a fuentes nuevas (Data Vault o un núcleo bien estructurado con tablas de mapeo de fuentes), dimensiones conformadas con emparejamiento de datos maestros entre empresas, códigos del sistema de origen en cada fila, y marts que puedan incluir o excluir las entidades adquiridas.

<!-- challenge -->

Finanzas quiere el MRR tal como se reportó en cada cierre de mes, aunque correcciones posteriores cambien la historia. ¿Cómo lo soportas?

<!-- solution -->

Mantén inmutable el snapshot mensual una vez cerrado el mes (agrega una versión corregida del snapshot en lugar de sobrescribir), para tener disponibles el MRR "según se reportó" y "según se corrigió".

<!-- takeaways -->

- Eventos en hechos transaccionales; estados en snapshots.
- MRR y churn salen directo del snapshot.
- Congela los periodos cerrados cuando importan las cifras reportadas.
