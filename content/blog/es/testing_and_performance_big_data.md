## Pruebas y rendimiento en pipelines de big data

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Pruebas y rendimiento en pipelines de big data](../../images/testing_and_performance_big_data_title_img.png)

*Artículo técnico*

## Dos preguntas que todo pipeline debe responder

Un pipeline de datos tiene que responder dos preguntas antes de que alguien deba confiar en él en producción. ¿Es **correcto**: produce los datos correctos, cada vez, incluso con las entradas extrañas que envían las fuentes reales? ¿Y es **lo bastante rápido y barato**: termina dentro de su ventana, con un costo que el negocio acepta, a medida que crecen los datos?

Los equipos suelen tratarlas por separado: la corrección es problema de los analistas, el rendimiento es problema del equipo de plataforma. Están conectadas. Optimizar un pipeline sin pruebas es apostar, porque cada cambio de rendimiento (una nueva estrategia de join, otro particionado, una carga incremental en lugar de una reconstrucción completa) es una oportunidad de cambiar los resultados en silencio. Y las pruebas que no corren rápido en un computador portátil no se van a ejecutar nunca.

Este artículo cubre cómo abordo ambas cosas, con ejemplos en PySpark y Delta Lake. Varios vienen de mi [lakehouse de registros mercantiles europeos](../projects/eu-company-registry.html), que tiene unas 200 pruebas y corre de punta a punta en un portátil antes de que nada llegue a Databricks.

## Parte 1: demostrar que el pipeline es correcto

### Por qué probar big data es distinto

Probar una API web y probar un pipeline de datos comparten principios, pero los datos añaden cuatro complicaciones:

- **La entrada es la mitad del programa.** Un código correcto puede producir datos malos a partir de una fuente que cambió su formato, corrió una columna o envió medio archivo. Las pruebas de código no bastan; también hacen falta pruebas de los datos.
- **El estado importa.** Los pipelines escriben tablas con historial. Un error no se corrige volviendo a desplegar; también hay que reparar los datos que escribió.
- **La escala esconde problemas.** Un join que funciona con 1.000 filas puede explotar con 50 millones por una sola clave caliente. Algunos fallos solo aparecen con volumen.
- **Ejecutar de verdad es caro.** "Desplegar y ver qué pasa" en un cluster cuesta dinero y minutos en cada intento, así que el ciclo de retroalimentación tiene que ser local.

Por eso una buena estrategia tiene varias capas, y cada una detecta un tipo distinto de problema.

| Capa | Qué detecta | Dónde corre |
|---|---|---|
| Controles estáticos | Antipatrones, APIs no admitidas, secretos | Pre-commit y CI, segundos |
| Pruebas unitarias | Lógica equivocada en el parseo, la limpieza, las reglas de negocio | Portátil y CI, segundos |
| Pruebas de extremo a extremo con datos sintéticos | Errores de conexión entre etapas, idempotencia, historial | Portátil y CI, minutos |
| Controles de calidad de datos | Datos reales malos o inesperados | Producción, en cada ejecución |
| Regresión y conciliación | Cambios no buscados en los resultados, cargas incompletas | CI con muestras, producción tras las cargas |
| Controles de rendimiento | Planes y tiempos que se degradan | CI (controles del plan), benchmarks periódicos |

### Diseñar para poder probar

El hábito más útil es **separar las transformaciones de la E/S**. Una función que recibe un DataFrame y devuelve un DataFrame se puede probar con diez filas; una celda de notebook que lee de S3, transforma y escribe una tabla solo se puede probar ejecutándolo todo.

```python
from pyspark.sql import DataFrame, functions as F
from pyspark.sql.window import Window

def latest_per_key(df: DataFrame, key: str, order_col: str) -> DataFrame:
    """Conserva la fila más reciente por clave."""
    w = Window.partitionBy(key).orderBy(F.col(order_col).desc())
    return df.withColumn("_rn", F.row_number().over(w)).filter("_rn = 1").drop("_rn")
```

Los puntos de entrada (jobs, notebooks, handlers de Lambda) quedan delgados: leen la configuración, llaman a estas funciones y escriben los resultados. Las rutas, fechas y nombres de tablas son parámetros, nunca constantes enterradas en el código.

### Pruebas unitarias con una SparkSession local

Un fixture con alcance de sesión da a todas las pruebas la misma instancia pequeña de Spark, lo que mantiene rápida la suite:

```python
import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark():
    session = (SparkSession.builder.master("local[2]")
               .config("spark.sql.shuffle.partitions", "2")
               .config("spark.sql.ansi.enabled", "true")   # mismo comportamiento que producción
               .getOrCreate())
    yield session
    session.stop()

def test_latest_per_key_keeps_newest(spark):
    from pyspark.testing import assertDataFrameEqual
    df = spark.createDataFrame(
        [(1, "old", "2026-10-01"), (1, "new", "2026-10-02"), (2, "only", "2026-10-01")],
        ["id", "value", "updated_at"])
    expected = spark.createDataFrame(
        [(1, "new", "2026-10-02"), (2, "only", "2026-10-01")],
        ["id", "value", "updated_at"])
    assertDataFrameEqual(latest_per_key(df, "id", "updated_at"), expected)
```

Hay dos detalles importantes. Configura la sesión local como producción (aquí el modo ANSI, que hace fallar las conversiones inválidas en lugar de devolver nulo en silencio), o las pruebas pasarán en local y fallarán en el cluster. Y mantén bajas las particiones del shuffle; el valor por defecto de 200 vuelve lentas las pruebas pequeñas.

Para las funciones a nivel de columna (parsear fechas, limpiar códigos postales, validar identificadores) uso un helper que evalúa una expresión de columna sobre una lista de entradas **en un solo job de Spark**, para que una prueba con cincuenta casos no lance cincuenta jobs:

```python
def eval_col(spark, fn, values):
    """eval_col(spark, parse_int, ["5.0", "x"]) -> [5, None]"""
    df = spark.createDataFrame([(v,) for v in values], "value string")
    return [row[0] for row in df.select(fn(F.col("value"))).collect()]

def test_parse_postcode(spark):
    assert eval_col(spark, clean_postcode, [" 75001", "75-001", "", None]) == ["75001", "75001", None, None]
```

### Pruebas basadas en propiedades para los parsers

Los ejemplos escritos a mano cubren los casos en los que pensaste. Las pruebas basadas en propiedades (con Hypothesis) generan cientos de entradas y verifican propiedades que siempre deben cumplirse: una salida deduplicada tiene claves únicas; un identificador limpio es válido o nulo, nunca algo intermedio; parsear y luego formatear un valor devuelve el mismo valor. Son especialmente buenas para encontrar casos límite en los parsers de texto desordenado.

### Datos sintéticos que se parecen a los reales

Los datos reales no pueden ir a un repositorio público, y tampoco deberían ir a CI. La respuesta son **datos de prueba sintéticos que reproducen las rarezas de los archivos reales**: los mismos nombres y orden de columnas, las mismas codificaciones y separadores, las mismas particularidades (fechas en tres formatos, identificadores con espacios, filas con campos faltantes, un arreglo JSON en lugar de NDJSON). En el proyecto de registros, los datos de prueba se generan a partir de la forma de los archivos reales con identificadores nuevos que siguen pasando sus dígitos de control, así la lógica de validación se ejercita de forma realista.

### Pruebas de extremo a extremo: todo el pipeline en un portátil

La prueba que más valoro ejecuta todas las etapas, desde los archivos de aterrizaje hasta la salida publicada, sobre esos datos de prueba:

```python
@pytest.mark.e2e
def test_pipeline_end_to_end(spark, tmp_path):
    settings = Settings(landing_root=copy_fixtures(tmp_path), snapshot_date=date(2026, 7, 31),
                        publish_root=tmp_path / "publish")
    run_bronze(spark, settings)
    run_silver(spark, settings)
    run_gold(spark, settings)
    run_publish(spark, settings)

    silver = spark.table("silver.companies")
    assert silver.filter("is_current").groupBy("company_key").count().filter("count > 1").count() == 0
    assert (tmp_path / "publish" / "summary.json").exists()
```

Tarda unos minutos y no cuesta nada. Detecta los errores que las pruebas unitarias no pueden: una etapa que lee una columna que la etapa anterior renombró, una tabla escrita en el esquema equivocado, una condición de merge que duplica las filas vigentes. En mi proyecto es literalmente "la prueba que reemplaza ejecutarlo en Databricks y ver qué pasa".

### Probar explícitamente la idempotencia y el historial

Los pipelines se vuelven a ejecutar todo el tiempo: reintentos tras fallos, backfills, disparos dobles por accidente. Un pipeline que añade a ciegas duplicará los datos en cada reejecución. Haz de la idempotencia una prueba, no una esperanza:

```python
def test_rerun_on_same_input_changes_nothing(spark, settings):
    run_silver(spark, settings)
    version_before = spark.sql("DESCRIBE HISTORY silver.companies").first()["version"]
    run_silver(spark, settings)   # mismos archivos de entrada
    version_after = spark.sql("DESCRIBE HISTORY silver.companies").first()["version"]
    assert version_after == version_before   # no se escribió una nueva versión de la tabla
```

En las tablas con historial (SCD tipo 2), prueba el ciclo de vida: una entidad nueva tiene una fila abierta; un cambio cierra la versión vieja y abre una nueva; una entidad que desaparece se cierra; una foto más vieja se rechaza en lugar de reescribir el historial hacia atrás.

### Controles de calidad de datos en producción

Las pruebas con datos de prueba demuestran el código; no pueden demostrar que el archivo del mes que viene sea sensato. Ese es el trabajo de los controles de calidad que corren sobre datos reales en cada ejecución. Un diseño simple y eficaz da a cada regla una **gravedad**:

- **Advertencia:** se conserva la fila, se cuenta y se informa.
- **Error:** la fila va a una tabla de cuarentena con las reglas que falló, y se sigue con el resto.
- **Umbral de aborto:** si demasiadas filas fallan una regla, se detiene la ejecución. Cuando el 1 % de los identificadores falla de repente su dígito de control, el problema es estructural (columnas corridas, un formato nuevo), y cargar el resto sería peor que detenerse.

Todas las reglas se pueden evaluar en una sola pasada sobre los datos:

```python
RULES = {
    # nombre: (gravedad, condición que debe cumplirse)
    "id_present":    ("error",   F.col("company_id").isNotNull()),
    "known_country": ("error",   F.col("country_code").isin("FR", "IE", "GB", "NO", "EE", "ES")),
    "has_postcode":  ("warning", F.col("postcode").isNotNull()),
}

failures = df.select(
    F.count("*").alias("rows"),
    *[F.sum(F.when(F.coalesce(cond, F.lit(False)), 0).otherwise(1)).alias(name)
      for name, (_, cond) in RULES.items()],
).first()
```

Añade también controles de volumen. En el pipeline de registros, una foto con menos del 80 % de las filas de la anterior detiene la ejecución: así se ve una descarga truncada, y es mucho más barato detenerse que publicar un mapa al que le falta una quinta parte de un país.

Las restricciones a nivel de tabla son la última línea de defensa. Las restricciones `CHECK` de Delta Lake (estados válidos, `valid_to >= valid_from`, filas vigentes con fecha de fin abierta) hacen imposible que una regresión del código escriba un estado inválido, porque la propia escritura falla.

### Regresión y conciliación

Cuando cambias la lógica, compara las salidas. Con los datos de prueba en CI, compara los resultados de la nueva versión con los de la anterior (conteos de filas, agregados clave, diferencias fila a fila sobre una muestra). En producción, concilia con las fuentes tras cada carga: filas por foto, claves distintas, sumas de montos. La conciliación convierte "creo que la carga está completa" en una evidencia.

## Parte 2: hacerlo rápido y asequible

### Medir antes de optimizar

La mayoría de los pipelines lentos lo son por una o dos razones, y adivinar hace perder días. Mira:

- **La Spark UI:** qué stage se lleva el tiempo, cómo se distribuyen las duraciones de sus tareas (una cola larga significa skew), el tamaño de lectura y escritura del shuffle, y el spill a disco.
- **El plan físico** (`df.explain(mode="formatted")`): ¿se empujan los filtros hasta la lectura, se descartan archivos, qué estrategia de join se eligió, aparece un `CartesianProduct` inesperado o una evaluación en Python?
- **El costo por ejecución**, no solo la duración. En Databricks, `system.billing.usage` da los DBU reales de cada ejecución; en mi proyecto, una pequeña tarea `cost_report` los registra tras cada ejecución para poder calibrar las estimaciones contra la realidad.

### Dónde se suele ir el tiempo

En mi experiencia, más o menos en este orden:

1. **Leer demasiados datos.** Lecturas completas en lugar de lecturas podadas, CSV o JSON en lugar de un formato columnar, miles de archivos pequeños.
2. **Shuffles.** Joins y agregaciones que mueven grandes cantidades de datos por la red.
3. **Skew.** Unas pocas claves (a menudo `null` o un valor por defecto) con la mayoría de las filas, así que unas pocas tareas corren una hora mientras el resto termina en segundos.
4. **Spill.** Particiones demasiado grandes para la memoria del executor, escritas en disco y vueltas a leer.
5. **Python a nivel de fila.** UDF que serializan cada fila entre la JVM y Python.
6. **Cuellos de botella en el driver.** `collect()` o `toPandas()` sobre muchos datos, o planes de consulta gigantes.

### Organización de los datos: leer menos

El byte más barato es el que nunca lees.

- Los **formatos columnares** (Parquet, o Delta e Iceberg encima de él) permiten a los motores leer solo las columnas necesarias y saltar grupos de filas con las estadísticas de mínimo y máximo.
- Los **tamaños de archivo** de unos 128 MB a 1 GB mantienen baja la sobrecarga por archivo. El streaming y los appends pequeños y frecuentes crean archivos pequeños; la compactación (`OPTIMIZE`) los corrige.
- **Particionar o agrupar** por las columnas con las que filtran la mayoría de las consultas. En Delta, el liquid clustering (`CLUSTER BY`) ha reemplazado en gran medida el particionado manual y el Z-ordering; particiona solo las tablas muy grandes, por una columna de baja cardinalidad que usen casi todas las consultas, o recrearás el problema de los archivos pequeños.
- **Filtros que podan.** Un filtro solo poda si se aplica directamente a la columna guardada. `WHERE to_date(event_ts) = '2026-10-15'` puede leerlo todo; `WHERE event_date = '2026-10-15'` sobre una columna agrupada o particionada no.

### Joins: broadcast de lo pequeño, manejar el skew

Cuando un lado de un join es pequeño (una dimensión, una tabla de búsqueda), haz broadcast para no hacer shuffle del lado grande:

```python
from pyspark.sql.functions import broadcast
enriched = facts.join(broadcast(dim_country), "country_code", "left")
```

La Adaptive Query Execution (activada por defecto en el Spark reciente) convierte los joins en broadcast cuando un lado resulta pequeño en ejecución, fusiona las particiones pequeñas del shuffle y divide las que tienen skew. Déjala trabajar y mantén activados sus ajustes.

Para el skew que AQE no puede corregir, trata aparte las claves calientes o aplícales **salting**: reparte una clave caliente en varias subclaves artificiales del lado grande y replica en consecuencia el lado pequeño.

```python
SALTS = 16
big = big.withColumn("salt", (F.rand() * SALTS).cast("int"))
small = small.crossJoin(spark.range(SALTS).withColumnRenamed("id", "salt"))  # solo el lado pequeño
joined = big.join(small, ["key", "salt"])
```

Muchas veces la verdadera solución está antes: una clave de join `null` que debía filtrarse o mapearse a un miembro "desconocido" antes del join.

### Patrones que conviene prohibir en el código

Algunos antipatrones son tan comunes y tan costosos que vale la pena detectarlos automáticamente y no en la revisión de código. En el proyecto de registros, un pequeño linter basado en el AST corre en pre-commit, en CI y en la suite de pruebas, y señala, entre otros:

| Patrón | Por qué duele |
|---|---|
| `collect()` / `toPandas()` sobre datos sin acotar | Trae todo al driver |
| UDF de Python | Serialización fila por fila, invisible para el optimizador; casi siempre existen funciones integradas |
| `withColumn` dentro de un bucle | El plan crece de forma cuadrática; usa `withColumns` o un solo `select` |
| `crossJoin` | Producto cartesiano, casi siempre un error |
| `repartition(1)` / `coalesce(1)` | Hace pasar todos los datos por una sola tarea |
| `inferSchema` | Lectura completa extra, tipos inestables; declara los esquemas |
| `cache()` / `persist()` en serverless | No se admite allí; escribe una tabla intermedia |

Cada hallazgo se puede suprimir en una línea con una justificación escrita, lo que mantiene estrictas las reglas sin bloquear las excepciones legítimas.

### Probar el plan, no solo el resultado

No puedes ejecutar benchmarks con volumen de producción en cada pull request, pero sí puedes revisar la **forma del plan de consulta** sobre los datos de prueba, de forma barata y determinista:

```python
import contextlib, io

def plan_of(df) -> str:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        df.explain(mode="formatted")
    return buffer.getvalue()

def test_gold_plan_is_safe(spark, silver_fixture):
    plan = plan_of(build_gold(silver_fixture))
    assert "BatchEvalPython" not in plan and "ArrowEvalPython" not in plan   # sin UDF de Python
    assert "CartesianProduct" not in plan                                     # sin productos cartesianos accidentales
    assert len(plan.splitlines()) < 400                                       # el tamaño del plan sigue acotado
```

Estas pruebas detectan una regresión de rendimiento en el momento en que se escribe, mucho antes de que alguien note que un job tarda el doble.

### Procesar solo lo que cambió

Los mayores ahorros rara vez vienen de ajustar un join. Vienen de **no hacer el trabajo**:

- Cargar de forma incremental (Auto Loader, `COPY INTO`, CDC, marcas de agua) en lugar de volver a leer todos los archivos.
- Escribir con `MERGE` o `replaceWhere` sobre el periodo afectado en lugar de reconstruir tablas completas.
- Saltar las etapas cuyas entradas no cambiaron. La primera tarea del job de registros compara los archivos de aterrizaje más recientes, el nomenclátor geográfico y los resultados de geocodificación con lo último procesado; si nada cambió, una tarea de condición termina la ejecución de inmediato, y si solo cambió Francia, solo se reprocesa Francia. Una prueba verifica que reejecutar sobre los mismos archivos no escribe ninguna nueva versión de tabla ni ningún archivo publicado.

### Dimensionar bien el cómputo

Ajusta el cómputo a la carga: serverless o clusters de job para los pipelines programados (nunca clusters interactivos), autoescalado dentro de límites razonables, instancias spot para los workers batch tolerantes a fallos y autoterminación en todas partes. Más grande no siempre es más caro: si un job se paraleliza bien, duplicar el cluster reduce a la mitad el tiempo al mismo costo. Si no, estás pagando núcleos ociosos, y la línea de tiempo de los executors en la Spark UI lo mostrará.

### Seguir el rendimiento en el tiempo

El rendimiento se degrada poco a poco a medida que crecen los datos. Guarda un historial de la duración, el tamaño de entrada, el volumen de shuffle y el costo por ejecución, y crea alertas cuando una ejecución tarda mucho más que su promedio reciente. En los jobs de Databricks, una alerta de duración por debajo del timeout duro te avisa antes de que el job falle.

## Una lista de control para cada pipeline

**Corrección**

- Las transformaciones son funciones puras con pruebas unitarias, ejecutadas en una sesión local configurada como producción.
- Los datos de prueba sintéticos reproducen las rarezas de las fuentes reales; no hay datos personales reales en el repositorio.
- Una prueba de extremo a extremo ejecuta todo el pipeline con los datos de prueba en minutos.
- Se prueba que las reejecuciones sean idempotentes; la lógica de historial (SCD2) se prueba a lo largo de su ciclo de vida.
- Las reglas de calidad tienen gravedades, cuarentena y umbrales de aborto; las caídas de volumen detienen la ejecución.
- Las restricciones de las tablas imponen invariantes; los resultados se concilian con las fuentes.

**Rendimiento y costo**

- Formatos columnares, tamaños de archivo sanos, clustering por los filtros habituales, filtros que podan.
- Broadcast de las tablas pequeñas, skew manejado, AQE activada.
- Antipatrones bloqueados por un linter; planes de consulta revisados en las pruebas.
- Solo se procesan los datos que cambiaron; se saltan las etapas sin cambios.
- El cómputo se ajusta a la carga; el costo por ejecución se mide y se sigue en el tiempo.

Las pruebas y el rendimiento son la misma disciplina vista desde dos lados: saber exactamente qué hace tu pipeline, para poder cambiarlo con confianza. Una suite que corre en minutos en un portátil es lo que hace seguro optimizar; las mediciones son las que te dicen dónde vale la pena hacerlo.
