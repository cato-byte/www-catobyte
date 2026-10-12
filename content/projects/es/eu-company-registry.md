---
title: Lakehouse de registros mercantiles europeos
summary: Integración de los registros mercantiles abiertos de seis países europeos en un lakehouse Data Vault 2.0 sobre Databricks y AWS, con tablas gold limpias y geocodificadas.
started: 2026-07
updated: 2026-10-12
status: in_progress
stack: [PySpark, Databricks Serverless, Delta Lake, AWS Lambda, Amazon S3, AWS Location Service, Data Vault 2.0]
cover: images/projects/eu-company-registry.png
cover_alt: Seis registros mercantiles nacionales pasando por las capas landing, bronze, staging, vault y gold
repo: https://github.com/cato-byte/eu-company-registry-lakehouse
---

## En resumen

<ul class="stats"><li><strong>6</strong><span>registros nacionales (FR, IE, UK, NO, EE, ES)</span></li><li><strong>5</strong><span>capas del pipeline, de landing a gold</span></li><li><strong>6</strong><span>entidades Data Vault: hubs, link, satélites</span></li><li><strong>2</strong><span>tablas gold para analítica</span></li></ul>

## El problema

Casi todos los países europeos publican su registro mercantil como datos abiertos, pero cada uno lo hace a su manera. Los formatos van del CSV al JSON comprimido y los delimitadores de la coma al punto y coma. Los nombres de columna están en francés, noruego o estonio, y las fechas, formas jurídicas y códigos de estado siguen convenciones propias. Los identificadores solo son únicos dentro de su país.

El objetivo de este proyecto es un único modelo consultable de empresas de seis países. Cualquiera debería poder preguntar «¿cuántas empresas activas hay por sector y país?» o ponerlas en un mapa sin conocer la estructura de cada registro.

## Fuentes de datos

| País | Registro | Publicador | Formato | Clave de negocio |
|---|---|---|---|---|
| Francia | Base SIRENE, establecimientos | INSEE vía data.gouv.fr | CSV (zip) | SIRET, con SIREN como alternativa |
| Irlanda | Registro de empresas | Companies Registration Office (CRO) | CSV | Número de empresa |
| Reino Unido | Basic Company Data | Companies House | CSV (zip) | Número de empresa |
| Noruega | Enhetsregisteret | Brønnøysund Register Centre | JSON (gzip) | Organisasjonsnummer |
| Estonia | Registro mercantil, datos básicos | Centro de Registros y Sistemas de Información (RIK) | CSV (zip, delimitado por `;`) | Código de registro |
| España | Establecimientos de Navarra | Datos abiertos del Gobierno de Navarra | CSV | NIF (DNI/CIF) |

<div class="callout"><p><strong>Una realidad de los datos, no un error:</strong> España no ofrece una descarga masiva gratuita de su registro mercantil nacional, así que la parte española procede del portal regional de datos abiertos de Navarra. Francia y Navarra publican además <em>establecimientos</em> (sedes) en lugar de personas jurídicas, por lo que su granularidad difiere de la de las otras cuatro fuentes. El modelo lo tiene en cuenta en lugar de ocultarlo.</p></div>

## Arquitectura

<ol class="pipeline"><li><strong>Ingesta</strong><span>Una única Lambda genérica descarga cada registro, lo descomprime y deposita los ficheros en S3, particionados por país.</span><span class="tool">AWS Lambda · S3</span></li><li><strong>Bronze</strong><span>Los ficheros se leen con esquemas explícitos y se guardan 1:1 como tablas Delta.</span><span class="tool">PySpark · Delta Lake</span></li><li><strong>Staging</strong><span>Cada fuente se mapea a un modelo canónico, se limpia y recibe sus claves hash de Data Vault.</span><span class="tool">PySpark</span></li><li><strong>Raw Vault</strong><span>Hubs, links y satélites integran los seis países en un solo modelo.</span><span class="tool">Data Vault 2.0 · Delta</span></li><li><strong>Gold</strong><span>Estado más reciente de cada empresa, geocodificación incremental y una dimensión y una tabla de hechos analíticas.</span><span class="tool">PySpark · AWS Location Service</span></li><li><strong>Explotación</strong><span>Mapa y cuadro de mando sobre las tablas gold. Hay un prototipo en desarrollo.</span><span class="tool">Leaflet · JavaScript</span></li></ol>

Todo se ejecuta en **cómputo serverless de Databricks sobre AWS**, leyendo y escribiendo en S3. No hay clústeres que dimensionar ni mantener encendidos para un proceso por lotes que se ejecuta de forma puntual.

## Decisiones clave y por qué

1. **Una sola función de ingesta guiada por configuración.** Una única Lambda sirve para todos los países. Cada fuente es una pequeña petición JSON (URL, país, fichero destino), así que añadir un país es añadir un fichero de configuración, no código. Las descargas se escriben en disco en bloques de 64 KB, de modo que la memoria se mantiene estable incluso con registros de varios gigabytes, y los ZIP se detectan y extraen sobre la marcha.
2. **Esquemas explícitos, guardados junto a los datos.** Cada fuente tiene un esquema `StructType` de Spark en JSON, así que nada depende de `inferSchema`. Se evita una lectura completa extra de ficheros grandes, los tipos son los mismos en cada ejecución y cualquier cambio de esquema hace fallar la capa bronze de forma visible, en lugar de corromper en silencio las tablas posteriores.
3. **Almacenamiento Delta Lake por capas.** Landing conserva los ficheros intactos, y bronze, staging, vault y gold son tablas Delta. Cada capa se puede reconstruir a partir de la anterior, y cuando un valor parece incorrecto puedo localizar la capa exacta en la que cambió.
4. **Un modelo de staging canónico.** Las seis fuentes se mapean a las mismas 14 columnas de negocio (identificador, nombre, forma jurídica, estado, sector, empleados, dirección…) más columnas de linaje (`source_country`, `record_source`, `load_timestamp`). La lógica específica de cada fuente vive en un único `select` por país, y todo lo que viene después de staging es independiente del país.
5. **Claves de negocio con ámbito de país.** Los identificadores nacionales solo son únicos dentro de su registro. Un número de empresa británico puede coincidir con uno irlandés, así que la clave hash de empresa combina el país *y* el identificador.
6. **Data Vault 2.0 para la integración.** Seis fuentes con atributos y ritmos de cambio distintos encajan de forma natural en hubs (claves de negocio), links (relaciones) y satélites (atributos descriptivos con `hash_diff`). Una nueva fuente añade filas, no una migración de esquema.
7. **La geocodificación como satélite incremental.** Llamar a una API de geocodificación es la única parte del pipeline que cuesta dinero por registro. Las direcciones nuevas se detectan con un `left_anti` join contra las coordenadas ya guardadas, se geocodifican con AWS Location Service (con OpenStreetMap como alternativa) y se añaden a un satélite. Ninguna dirección se geocodifica dos veces.

```python
# Claves Data Vault con ámbito de país, generadas en staging
.withColumn("hk_company", md5(concat_ws("||", col("source_country"), col("national_id"))))
.withColumn("hk_location", md5(concat_ws("||",
    coalesce(col("address_line"), lit("")),
    coalesce(col("postal_code"), lit("")),
    col("source_country"),
)))
```

## Limpieza de datos

| Problema en los datos de origen | Ejemplo | Regla aplicada |
|---|---|---|
| Cuatro formatos de fecha distintos | `2024-03-01`, `01/03/2024`, `01.03.2024` | Probar cada patrón con `coalesce(to_date(...))` |
| Basura en los campos de dirección | URLs, correos, teléfonos, coordenadas | Un filtro regex los convierte en `NULL` |
| Empleados publicados como rangos | `de 20 a 49` | Punto medio del rango (34,5), para poder sumarlo |
| Estado publicado como booleanos | `konkurs`, `underAvvikling` en Noruega | Mapeado a `BANKRUPT`, `LIQUIDATION`, `ACTIVE` |
| Campos desplazados por delimitadores | Filas estonias con `;` dentro de la clave | Se separan y se recuperan clave y nombre |
| Claves de negocio vacías o de relleno | vacía, `NONE` | Se descartan *antes* de calcular el hash |
| Mayúsculas y espacios inconsistentes | nombres, ciudades | Se recortan y se pasan a mayúsculas |

## Modelo Data Vault

<div class="vault"><div class="vault-entity vault-hub"><p class="kind">Hub</p><p class="name">hub_company</p><p class="cols">hk_company · national_id · source_country</p></div><div class="vault-entity vault-link"><p class="kind">Link</p><p class="name">link_company_location</p><p class="cols">hk_link · hk_company · hk_location</p></div><div class="vault-entity vault-hub"><p class="kind">Hub</p><p class="name">hub_location</p><p class="cols">hk_location · address_line · postal_code · city</p></div><div class="vault-entity vault-sat"><p class="kind">Satélite</p><p class="name">sat_company_profile</p><p class="cols">nombre · forma jurídica · estado · fecha de registro · IVA</p></div><div class="vault-entity vault-sat"><p class="kind">Satélite</p><p class="name">sat_company_metrics</p><p class="cols">código de sector · descripción · empleados</p></div><div class="vault-entity vault-sat"><p class="kind">Satélite</p><p class="name">sat_location_geocodes</p><p class="cols">latitud · longitud · origen de la geocodificación</p></div></div>

El perfil y las métricas van en satélites separados porque cambian a ritmos distintos. El nombre y el estado de una empresa cambian rara vez, mientras que la plantilla se actualiza cada año.

## Deduplicación

Los duplicados aparecen a varios niveles, y cada uno se resuelve donde se produce:

- **Dentro de un registro:** los hubs se deduplican por su clave hash, así que una empresa aparece una sola vez aunque la fuente la repita.
- **Entre cargas:** los satélites guardan todas las versiones. La capa gold selecciona la más reciente de cada empresa con una ventana point-in-time (`row_number()` sobre `load_timestamp`).
- **Entre empresas con la misma dirección:** `hub_location` usa como clave la dirección normalizada, así que un edificio de oficinas compartido por cincuenta empresas se guarda y geocodifica una sola vez.
- **Multiplicación en los joins:** gold conserva una única ubicación actual por empresa, así que unir dimensiones nunca multiplica filas.

```python
# Point-in-time: registro de satélite más reciente por empresa
latest = Window.partitionBy("hk_company").orderBy(col("load_timestamp").desc())
latest_profile = (
    sat_profile.withColumn("rn", row_number().over(latest))
    .filter(col("rn") == 1)
    .drop("rn")
)
```

## Tablas gold

**`dim_companies`**: una fila por empresa, con su perfil, métricas, dirección y coordenadas actuales.

| Columna | Descripción |
|---|---|
| `company_key` | Clave hash del vault (país + identificador nacional) |
| `national_id`, `source_country`, `record_source` | Identidad y linaje |
| `company_name`, `legal_form_code`, `company_status`, `registration_date` | Perfil más reciente |
| `industry_code`, `employee_count` | Métricas más recientes |
| `address_line`, `postal_code`, `city`, `latitude`, `longitude` | Ubicación actual, geocodificada |

**`fact_country_industry_metrics`**: un agregado por `source_country`, `industry_code` y `company_status`, con `total_companies` y `total_employees`. Está listo para cuadros de mando sin recorrer millones de filas.

<!-- bars: companies_by_country.csv -->

<!-- table: fact_country_industry_metrics_sample.csv -->

## Próximos pasos

- **Cargas que conservan el histórico.** Hoy las tablas del vault se reconstruyen en cada ejecución. El siguiente paso son satélites de solo inserción con un `MERGE` sobre `hash_diff`, para conservar cada cambio de un registro a lo largo del tiempo.
- **Vocabularios comunes.** Mapear los códigos de estado de todas las fuentes a un único conjunto de valores, y agregar los códigos de actividad a secciones NACE Rev. 2. SIC 2007 (Reino Unido), NAF (Francia), SN2007 (Noruega) y CNAE-2009 (España) derivan todos de NACE, así que se pueden alinear.
- **Resolución de entidades entre países.** Identificar el mismo grupo en varios países mediante coincidencia aproximada de nombre y dirección, ya que solo algunos registros publican el número de IVA.
- **Preparación para producción.** Validaciones de calidad de datos en cada capa, orquestación como job de Databricks y la infraestructura de AWS descrita como código con Terraform.
- **Cuadro de mando.** Terminar el mapa Leaflet y los filtros sobre las tablas gold.
