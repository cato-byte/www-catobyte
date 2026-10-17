## Patrones de arquitectura de datos: Kimball, microservicios, medallion y más

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Patrones de arquitectura de datos: de Kimball al lakehouse](../../images/data_architecture_patterns_title_img.png)

*Artículo técnico*

## No existe la mejor arquitectura

Cada pocos años se anuncia una nueva arquitectura de datos como la que reemplaza a todas las demás. Inmon fue reemplazado por Kimball, el warehouse por el data lake, el lake por el lakehouse, el equipo central por el data mesh. En la práctica, ninguno desapareció. La mayoría de las plataformas que he visto mezclan tres o cuatro de estas ideas, a veces a propósito y muchas veces por accidente.

La forma útil de pensarlas es como respuestas a preguntas concretas. ¿Cómo integro veinte sistemas que describen al mismo cliente de forma distinta? ¿Cómo hago que las cifras sean fáciles para los analistas? ¿Cómo conservo un registro de auditoría de cada cambio? ¿Cómo saco los datos de treinta microservicios sin acoplarme a sus bases de datos? ¿Cómo atiendo a la vez un reporte nocturno y un modelo de fraude que necesita una respuesta en 200 milisegundos? Cada patrón de este artículo es una buena respuesta a una de estas preguntas y una mala respuesta a otras.

Voy a recorrer los patrones que encuentro con más frecuencia, qué optimiza cada uno, dónde falla y cómo se combinan. Usaré mi [lakehouse de registros mercantiles europeos](../projects/eu-company-registry.html) como ejemplo concreto cuando ayude, incluida una decisión que revertí.

## Inmon: integrar primero

La Corporate Information Factory de Bill Inmon pone en el centro un **data warehouse empresarial en tercera forma normal**. Todas las fuentes se integran en un único modelo normalizado y orientado a temas (cliente, cuenta, producto) que es la versión única de la verdad. Después se derivan de él los data marts de cada departamento.

```
fuentes ──► staging ──► warehouse empresarial (3FN, integrado, historizado) ──► data marts dependientes ──► BI
```

**Qué optimiza:** la coherencia. Como todos los marts salen del mismo núcleo integrado, finanzas y ventas no pueden discrepar sobre qué es un cliente.

**Dónde duele:** el tiempo hasta entregar valor. Diseñar un modelo normalizado para toda la empresa toma meses antes del primer reporte, y cada fuente nueva obliga a cambiar un modelo central del que dependen muchos equipos. Además, los modelos normalizados son difíciles de consultar directamente para los analistas.

Todavía se ven núcleos al estilo Inmon en bancos y aseguradoras, y su idea central sobrevive en toda arquitectura que tenga una capa de "integración" o "silver".

## Kimball: modelar para las preguntas

Ralph Kimball tomó el camino contrario: partir de los **procesos de negocio** (toma de pedidos, facturación, envíos) y construir **modelos dimensionales** que los analistas puedan entender. Una tabla de hechos registra mediciones a un grano declarado, rodeada de tablas de dimensión con el contexto descriptivo. Ese es el esquema en estrella.

```sql
-- Una fila por línea de pedido (el grano), unida a dimensiones conformadas
SELECT d.year_month, c.segment, p.category, SUM(f.net_amount) AS revenue
FROM fct_order_lines f
JOIN dim_date d     ON f.order_date_key = d.date_key
JOIN dim_customer c ON f.customer_key   = c.customer_key
JOIN dim_product p  ON f.product_key    = p.product_key
WHERE d.year = 2026
GROUP BY d.year_month, c.segment, p.category;
```

Los marts se integran mediante **dimensiones conformadas**: un solo `dim_customer` y un solo `dim_date` compartidos por todas las tablas de hechos, planificados con la bus matrix. El historial vive en las **dimensiones lentamente cambiantes**, normalmente de tipo 2: cuando un cliente cambia de segmento, se cierra la fila vieja y se inserta una versión nueva, así las ventas del año pasado siguen atribuidas al segmento del año pasado.

**Qué optimiza:** la facilidad de uso y el rendimiento de las consultas. Los esquemas en estrella son fáciles de explicar, las herramientas de BI los entienden y los motores columnares los ejecutan rápido.

**Dónde duele:** la integración de fuentes desordenadas y solapadas. Kimball supone que puedes conformar las dimensiones; cuando veinte sistemas no se ponen de acuerdo sobre los clientes, ese trabajo de conformación tiene que ocurrir en algún lado, y el modelo dimensional no es el mejor lugar para guardar el historial en bruto y auditable de cada fuente.

Kimball no está pasado de moda. Casi todas las capas "gold" que he visto en un lakehouse son conjuntos de esquemas en estrella, aunque nadie los llame así. La capa gold de mi proyecto de registros es una estrella de Kimball: una dimensión de empresas, una dimensión de sectores y tablas agregadas, con la cobertura por país explícita.

## Data Vault: integrar y auditar a escala

El Data Vault de Dan Linstedt apunta a la capa de integración cuando hay muchas fuentes que cambian y requisitos fuertes de auditoría. Divide el modelo en tres tipos de tablas:

- Los **hubs** guardan las claves de negocio únicas (un número de cliente) con la fecha de carga y la fuente del registro.
- Los **links** guardan las relaciones entre hubs (cliente hizo pedido).
- Los **satellites** guardan los atributos descriptivos y su historial, un satellite por fuente o por velocidad de cambio.

Todo es de solo inserción, con claves hash para que las cargas corran en paralelo, y completamente trazable hasta la fuente. Encima se construyen los marts para el consumo, a menudo estrellas de Kimball, a veces con tablas auxiliares point-in-time y bridge.

**Qué optimiza:** la agilidad y la auditabilidad. Añadir una fuente significa añadir satellites, no rediseñar tablas. Los reguladores pueden ver exactamente qué dijo cada sistema y cuándo.

**Dónde duele:** la complejidad y el costo de las consultas. Una pregunta simple se convierte en un join entre hubs, links y varios satellites, así que nadie consulta el vault directamente; siempre se necesita una capa de presentación. Sin automatización (paquetes de dbt, generadores de código), el número de tablas crece rápido.

Trabajé en una plataforma Data Vault en Corum L'Épargne, y la primera versión de mi lakehouse de registros también fue un modelo Data Vault 2.0. Lo reemplacé a propósito, y el razonamiento es un buen ejemplo de elegir un patrón a partir del problema y no de la costumbre:

> Data Vault compensa cuando muchos sistemas describen las mismas claves de negocio. En el proyecto de registros ninguna clave se comparte nunca: un SIRET francés y un número de empresa británico nunca se refieren a la misma empresa. Cada hub era una copia renombrada de la columna de ID de un registro, y cada consulta se convertía en un join de cinco o seis tablas, cada shuffle facturado en cómputo serverless. Los registros publican fotos completas, así que el historial es exactamente lo que produce un merge SCD tipo 2, y Delta Lake ya da un registro de auditoría (viaje en el tiempo, `RESTORE`, Change Data Feed).

Conservé las ideas de Data Vault que se ganaron su lugar: claves hash, un `hash_diff` para detectar cambios, columnas de fuente del registro y de linaje, e historial en bruto de solo inserción en bronze. Ese suele ser el resultado correcto: tomar las técnicas y saltarse la metodología completa cuando su principal ventaja no aplica.

## Data lakes y el lakehouse

El data lake respondía a otra pregunta: ¿dónde ponemos todo, de forma barata, incluidos los datos que todavía no entendemos? El almacenamiento de objetos (S3, ADLS, GCS) guarda archivos en bruto de cualquier formato a una fracción del costo de un warehouse, con el esquema aplicado al leer.

Los lakes trajeron almacenamiento barato y flexibilidad, y también muchos **pantanos de datos**: sin transacciones (los lectores veían datos a medio escribir), sin control de esquema, consultas lentas sobre millones de archivos pequeños, sin actualizaciones ni borrados confiables (un problema real para el RGPD o el habeas data) y un gobierno débil.

El **lakehouse** lo resuelve con formatos de tabla abiertos, **Delta Lake, Apache Iceberg y Apache Hudi**, que añaden un registro de transacciones encima de archivos Parquet: escrituras ACID, control y evolución del esquema, viaje en el tiempo, `MERGE`, `UPDATE` y `DELETE`. Un catálogo (Unity Catalog, AWS Glue con Lake Formation, Polaris) convierte los archivos en tablas gobernadas, y varios motores (Spark, Databricks SQL, Snowflake, Athena, Trino) pueden leer los mismos datos.

**Qué optimiza:** una sola copia de los datos para BI, ciencia de datos y machine learning, en formatos abiertos, con garantías parecidas a las de un warehouse.

**Dónde duele:** sigue siendo necesario diseñar las capas, mantener las tablas (compactación, vacuum, clustering) y gobernar el acceso. Un lakehouse sin disciplina de modelado es solo un pantano más rápido.

## Medallion: capas de refinamiento

La arquitectura medallion es la convención de capas del lakehouse:

| Capa | Contiene | Reglas típicas |
|---|---|---|
| **Bronze** | Los datos en bruto tal como llegan, más metadatos de carga | Solo inserción, transformación mínima, todo reproducible |
| **Silver** | Entidades limpias, tipadas, deduplicadas, homogeneizadas e historizadas | Controles de calidad, cuarentena, SCD tipo 2, una versión confiable de cada entidad |
| **Gold** | Modelos listos para el negocio: esquemas en estrella, agregados, tablas de features | Definiciones de negocio aplicadas, optimizado para la lectura |

Es importante ver qué es medallion y qué no. Es una **convención de capas de refinamiento**, no una técnica de modelado. Silver puede ser normalizado, Data Vault o simplemente tablas de entidades limpias; gold suele ser Kimball. Medallion te dice dónde va cada cosa, no cómo modelarla.

En mi lakehouse de registros, las capas se ven así:

```
landing (S3, archivos en bruto por ingest_date)
   │  control de deriva del esquema contra un contrato
   ▼
bronze  todas las columnas como STRING + linaje, solo inserción, una tabla por registro
   │  parseo por fuente, reglas de calidad, cuarentena
   ▼
silver  un modelo canónico de empresas, MERGE SCD tipo 2 por país y foto
   │  modelado dimensional
   ▼
gold    estrella de Kimball (dimensiones de empresas y sectores) + tablas agregadas
```

Vale la pena copiar dos decisiones. Bronze guarda todas las columnas como texto, así un valor malo nunca puede hacer fallar una carga y silver siempre se puede volver a ejecutar con un mejor parseo. Y silver impone sus propias invariantes con restricciones (estados válidos, `valid_to >= valid_from`, filas vigentes abiertas), así una regresión del código no puede escribir un estado inválido.

Los errores que más veo con medallion: tratar las tres capas como copias obligatorias aunque una capa no aporte nada; dejar que los dashboards lean bronze o silver directamente; meter lógica de negocio en bronze; copiar tablas completas entre capas en cada ejecución en lugar de procesar de forma incremental; y no tener un contrato explícito de lo que garantiza cada capa.

## Microservicios y datos

Los microservicios cambiaron la arquitectura de datos desde el otro lado. Cada servicio es dueño de su base de datos (**una base por servicio**) y expone sus datos mediante APIs y eventos, nunca mediante tablas compartidas. Eso es bueno para la autonomía y la velocidad de despliegue. Es un reto para la analítica, porque los datos que el negocio quiere analizar quedan repartidos entre decenas de bases privadas.

El atajo tentador es apuntar el warehouse a la base de cada servicio y leer sus tablas. Funciona un mes; luego un equipo renombra una columna y se rompe el pipeline nocturno. Los esquemas internos son detalles de implementación; leerlos acopla la plataforma de datos al interior de cada servicio.

Los patrones que funcionan:

- La **captura de cambios (CDC)** lee el log de transacciones de cada base (con Debezium, AWS DMS o un conector administrado) y transmite las inserciones, actualizaciones y borrados a Kafka o al lakehouse, sin tocar el código del servicio. Es la forma más rápida de sacar datos de sistemas existentes, pero sigue exponiendo los esquemas internos salvo que se acuerde un contrato.
- Los **eventos de integración** son hechos de negocio (`OrderPlaced`, `PaymentFailed`) que los servicios publican a propósito como contratos versionados, separados de su modelo de dominio interno. Son más estables que el CDC y llevan significado de negocio.
- El **transactional outbox** resuelve el problema de la doble escritura: si un servicio escribe en su base y luego publica un evento, una cosa puede salir bien y la otra fallar. En su lugar, el servicio escribe el evento en una tabla outbox dentro de la misma transacción, y el CDC publica las filas del outbox en el broker.

```
┌──────────── servicio de pedidos ────────────┐
│  BEGIN                                      │
│    INSERT INTO orders ...                   │
│    INSERT INTO outbox (event: OrderPlaced)  │
│  COMMIT                                     │
└───────────────────┬─────────────────────────┘
                    │ el CDC lee las filas del outbox
                    ▼
              topic de Kafka: orders.events ──► otros servicios
                    │
                    ▼
              lakehouse bronze ──► silver ──► gold
```

En los sistemas orientados a eventos aparecen dos patrones relacionados. El **event sourcing** guarda una entidad como la secuencia de eventos que la modificaron y reconstruye el estado reproduciéndolos, lo que da un registro de auditoría perfecto pero complica las consultas. **CQRS** separa el modelo de escritura de los modelos de lectura, que se actualizan de forma asíncrona a partir de los eventos, para escalar lecturas y escrituras de forma independiente. Para las transacciones que abarcan varios servicios, las **sagas** reemplazan los commits distribuidos en dos fases por una secuencia de transacciones locales con acciones compensatorias.

Para un ingeniero de datos, la regla práctica es sencilla: **consumir contratos publicados (eventos o vistas de CDC curadas), no tablas internas**, y validar esos contratos en el CI de los productores para que los cambios que rompen fallen antes de publicarse.

## Lambda y Kappa: batch y streaming

Cuando llegó la necesidad de baja latencia, compitieron dos arquitecturas.

La **arquitectura Lambda** tiene dos caminos: una capa batch que recalcula vistas exactas a partir de todo el historial, y una capa de velocidad que procesa los eventos recientes en tiempo real, con una capa de servicio que combina ambas. Da exactitud y frescura, a costa de escribir y mantener la misma lógica dos veces.

La **arquitectura Kappa** mantiene un solo camino: todo es un flujo, guardado en un log durable y reproducible (Kafka). Para corregir un error o cambiar la lógica, se reproduce el log con una nueva versión del job. Una sola base de código, pero necesitas un procesamiento de streaming sólido y una retención larga.

Hoy la Lambda pura es rara. Los motores unificados (Spark Structured Streaming, Flink, Apache Beam) y los formatos de tabla que aceptan escrituras de streaming y batch sobre las mismas tablas hacen práctico un diseño tipo Kappa, con backfills batch desde el lakehouse cuando hace falta. Antes de elegir cualquiera de los dos, hazte la pregunta que más dinero ahorra: **¿qué decisiones cambian de verdad si los datos tienen segundos de antigüedad en lugar de horas?** La detección de fraude y las alertas operativas, sí. La mayoría de los dashboards, no.

## Data mesh y data fabric

El **data mesh**, propuesto por Zhamak Dehghani, es sobre todo una respuesta organizacional. Los equipos de datos centrales se vuelven cuellos de botella entre muchos dominios de origen y muchos consumidores, así que el mesh traslada la propiedad a los dominios, con cuatro principios: propiedad por dominio, **datos como producto** (con responsable, documentados, con garantías de calidad y SLA), una **plataforma de autoservicio** y un **gobierno computacional federado** (reglas globales aplicadas automáticamente por la plataforma).

Funciona cuando los dominios tienen la capacidad y la motivación para hacerse cargo de productos de datos y cuando hay una plataforma real debajo. Sin eso, el mesh produce datos fragmentados e inconsistentes con un nombre de moda. Muchas organizaciones adoptan la parte más útil, productos de datos con responsables y contratos, sin descentralizar del todo.

El **data fabric** es la contraparte tecnológica: metadatos activos, grafos de conocimiento, automatización y virtualización para integrar datos distribuidos detrás de una capa de acceso gobernada. El mesh pregunta "¿quién es dueño de esto?"; el fabric pregunta "¿cómo lo conectamos todo de forma automática?". Pueden convivir.

## Cómo encajan los patrones

En una plataforma moderna estos patrones son capas de un mismo diseño, no competidores. Una combinación típica se ve así:

```
 fuentes operativas            ingesta                   lakehouse (medallion)                  consumo
 ───────────────────   ─────────────────────────   ─────────────────────────────────   ─────────────────────
 bases de microserv. ──► CDC / eventos outbox ─┐
 aplicaciones SaaS   ──► conectores admin. ────┼──►  bronze  en bruto, solo inserción
 archivos y APIs     ──► extracciones batch ───┘         │
                                                         ▼
                                                 silver  integrado e historizado   ──► features de ML
                                                         │  (normalizado, Data Vault
                                                         │   o entidades SCD2 limpias)
                                                         ▼
                                                 gold    estrellas Kimball, agregados ──► BI, capa semántica,
                                                                                         reverse ETL, APIs
          gobierno en todas las capas: catálogo, linaje, contratos, controles de calidad, políticas de acceso
```

Los patrones de microservicios gobiernan cómo salen los datos de las aplicaciones. Medallion organiza el lakehouse. La idea de integración de Inmon o el Data Vault viven en silver. Kimball vive en gold. Los caminos de streaming alimentan bronze de forma continua cuando la latencia importa. El mesh decide quién es dueño de cada producto de datos a lo largo del camino.

## Cómo elegir

Empieza por las restricciones, no por el diagrama más nuevo. Estas preguntas reducen las opciones rápido:

| Si tu situación es… | Inclínate por… |
|---|---|
| Pocas fuentes y los analistas necesitan cifras pronto | Marts de Kimball sobre un warehouse en la nube o un lakehouse; sáltate las capas de integración pesadas |
| Muchas fuentes solapadas, necesidades fuertes de auditoría o regulatorias | Data Vault (o un núcleo normalizado) en silver, Kimball en gold |
| Datos estructurados, semiestructurados y no estructurados, ML y BI sobre los mismos datos | Lakehouse con formatos de tabla abiertos y capas medallion |
| Los datos vienen de microservicios que no controlas | Eventos de integración y outbox donde se pueda, CDC en el resto, contratos en el CI |
| Las decisiones pierden valor en segundos | Un camino de streaming (Kafka más Flink o Spark streaming) que alimente las mismas tablas que el batch |
| Un equipo central es el cuello de botella y los dominios están maduros | Productos de datos con responsables y contratos; mesh completo solo con una plataforma real |
| Equipo pequeño y presupuesto limitado | El stack administrado más simple que funcione: warehouse, dbt, un orquestador, pruebas |

Algunos principios valen elijas lo que elijas:

- **Mantén inmutables los datos en bruto** para poder reprocesar cuando cambien la lógica o se corrijan errores.
- **Modela las capas de consumo para las preguntas que hace la gente**, al grano más atómico que puedas permitirte.
- **Haz explícitos los contratos** entre productores, capas y consumidores.
- **Escribe la decisión.** Un registro de decisión de arquitectura de una página, con el contexto, las opciones y por qué elegiste una, es lo que permite revertir una decisión con calma más adelante, como hice yo con Data Vault.

La mejor arquitectura es la que tu equipo puede explicar, operar y cambiar. Los patrones son herramientas; la habilidad está en saber qué problema resuelve cada uno.
