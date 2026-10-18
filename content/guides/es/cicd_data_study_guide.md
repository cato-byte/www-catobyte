## Guía de estudio de CI/CD para datos

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de CI/CD para datos: unas 200 preguntas](../../images/cicd_data_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre CI/CD y automatización para plataformas de datos: flujos de Git, estrategias de pruebas de pipelines y datos, calidad del código, entornos, infraestructura como código, patrones de despliegue, GitHub Actions a fondo, CI/CD para dbt, Databricks, Airflow y warehouses, seguridad de la cadena de entrega y operación. Los ejemplos usan GitHub Actions, con notas sobre GitLab CI y Azure DevOps. Abre una pregunta para ver su respuesta, o usa el filtro para buscar en toda la guía.

<!-- QA -->

### Fundamentos

#### ¿Qué es CI/CD?

La integración continua (CI) consiste en fusionar los cambios de código con frecuencia en una rama compartida, con construcción y pruebas automáticas en cada cambio. La entrega continua (CD) mantiene el código siempre listo para desplegar y automatiza las publicaciones en los entornos; el despliegue continuo va más allá y despliega automáticamente en producción cada cambio que pasa las pruebas.

#### ¿Por qué importa CI/CD a los equipos de datos?

Los pipelines de datos son software: sin automatización, los cambios se despliegan a mano, rompen tablas de producción y son difíciles de revertir. CI/CD detecta los errores antes de que lleguen a los consumidores, hace los despliegues repetibles y auditables, y permite cambiar los pipelines rápido y con seguridad.

#### ¿Qué es DataOps?

Aplicar las prácticas de DevOps y ágiles a los datos: control de versiones, pruebas automáticas (de código y de datos), CI/CD, gestión de entornos, monitoreo y observabilidad, y colaboración entre ingenieros de datos, analistas y operación, con el objetivo de entregar datos confiables rápidamente.

#### ¿En qué se diferencia el CI/CD de datos del de aplicaciones?

Los pipelines de datos tienen estado (tablas, historial, esquemas) que hay que migrar, no solo reemplazar; las pruebas necesitan datos representativos; la corrección depende tanto de los datos como del código; los despliegues pueden disparar recálculos costosos; y revertir datos es más difícil que revertir código.

#### ¿Qué se debe automatizar en un pipeline de CI/CD de datos?

El linting y el formateo, las pruebas unitarias, la construcción de artefactos (wheels, imágenes, manifiestos de dbt), la validación estática (compilación de SQL, validación de bundles o DAG), las pruebas de integración y de datos sobre datos de prueba, los escaneos de seguridad, los cambios de infraestructura, los despliegues en cada entorno, las pruebas de humo tras el despliegue y las notificaciones.

#### ¿Qué diferencia hay entre entrega continua y despliegue continuo?

Con la entrega continua, cada cambio es desplegable y el despliegue a producción está a un clic o una aprobación. Con el despliegue continuo, cada cambio que pasa el pipeline llega a producción automáticamente, sin paso manual.

#### ¿Qué es "todo como código"?

Definir pipelines, transformaciones, infraestructura, permisos, programaciones, reglas de calidad de datos e incluso documentación en archivos versionados, para que cada cambio se revise, se pruebe, sea reproducible y trazable.

#### ¿Qué ventajas tienen los despliegues pequeños y frecuentes?

Cada cambio es más fácil de revisar, probar y entender, los fallos son más fáciles de diagnosticar y revertir, y la retroalimentación de producción llega antes. Las publicaciones grandes y poco frecuentes acumulan muchos riesgos juntos.

#### ¿Qué es un pipeline de despliegue?

La secuencia automatizada que lleva un commit a producción: construir, probar, empaquetar, desplegar en los entornos inferiores, ejecutar controles, aprobar, desplegar en producción, verificar. Es el camino que sigue cada cambio.

#### ¿Qué son las métricas DORA?

Cuatro medidas del desempeño de entrega: frecuencia de despliegue, tiempo de entrega de los cambios, tasa de fallos de los cambios y tiempo para restaurar el servicio. También aplican a los equipos de datos y ayudan a medir si CI/CD mejora la entrega.

#### ¿Qué diferencia hay entre las etapas de compilación, prueba y despliegue?

La compilación produce artefactos (paquetes, imágenes, modelos compilados); la prueba los verifica (unitarias, de integración, de datos); el despliegue los instala en un entorno y ejecuta los controles posteriores. Separarlas facilita ubicar los fallos.

#### ¿Qué es "shift left" en la calidad de datos?

Detectar los problemas lo antes posible: en el IDE (linters), al hacer commit (hooks de pre-commit), en los pull requests (pruebas de CI, controles de contrato), en lugar de en los dashboards de producción, donde son costosos y visibles.

#### ¿Qué diferencia hay entre una "publicación" (release) y un "despliegue"?

Un despliegue instala una versión en un entorno; una publicación pone la nueva funcionalidad a disposición de los usuarios. Con feature flags o cambios blue-green, se puede desplegar sin publicar y publicar sin volver a desplegar.

#### ¿Por qué los pipelines deben ser deterministas?

Con el mismo código, configuración y entradas, un pipeline determinista produce las mismas salidas, lo que hace posibles las pruebas, la depuración, los backfills y las auditorías. Evita dependencias ocultas de la hora actual, semillas aleatorias o versiones sin fijar.

#### ¿Qué significa "you build it, you run it" para los equipos de datos?

El equipo que construye un pipeline también lo opera: recibe sus alertas, resuelve sus incidentes y mejora su confiabilidad, lo que crea fuertes incentivos para tener buenas pruebas, monitoreo y automatización.

### Control de versiones y flujos de Git

#### ¿Por qué el código de datos debe estar en Git?

El control de versiones da historial (quién cambió qué y por qué), colaboración mediante ramas y pull requests, la posibilidad de revertir, una única fuente de verdad para los despliegues y el disparador del CI/CD.

#### ¿Qué va en un repositorio de datos?

El código de pipelines y transformaciones (Python, SQL, modelos dbt), las pruebas y sus datos de prueba, la configuración por entorno (sin secretos), la infraestructura como código, las definiciones de orquestación (DAG, bundles, especificaciones de jobs), los workflows de CI/CD, la documentación y los contratos de datos.

#### ¿Qué nunca se debe subir al repositorio?

Secretos (contraseñas, claves, tokens), datos personales o sensibles reales, archivos de datos grandes, archivos de entorno local y salidas de compilación. Usa `.gitignore`, escaneo de secretos y hooks de pre-commit para evitar accidentes.

#### ¿Qué es el trunk-based development?

Un flujo en el que los desarrolladores integran cambios pequeños en la rama principal con frecuencia (al menos a diario), usando ramas de funcionalidad de corta vida y feature flags, con la rama principal siempre lista para publicar. Encaja muy bien con CI/CD.

#### ¿Qué es GitFlow y por qué es menos popular hoy?

Un modelo de ramas con ramas `develop` y `main` de larga vida más ramas de funcionalidad, release y hotfix. Añade ceremonia y conflictos de fusión; la mayoría de los equipos que practican CI/CD prefieren el trunk-based development o un flujo simple de ramas de funcionalidad.

#### ¿Qué es un pull request (merge request) y qué debe incluir uno bueno?

Una solicitud para fusionar una rama, con una descripción de qué y por qué, el ticket enlazado, las pruebas hechas, el impacto en los datos (esquemas, backfills, consumidores), capturas o resultados de consultas si aplica, y los controles en verde. Es el lugar de la revisión y la validación automática.

#### ¿Qué deben buscar los revisores en el código de datos?

Que la lógica y los joins sean correctos (grano, fan-out), el manejo de nulos y duplicados, la idempotencia, el rendimiento (filtros de partición, lecturas completas), pruebas que cubran el cambio, cambios de esquema y de contrato, necesidad de backfills, seguridad (sin secretos, permisos adecuados) y legibilidad.

#### ¿Qué son las reglas de protección de ramas?

Ajustes del repositorio que impiden los push directos a las ramas importantes y exigen pull requests, controles en verde, un número de aprobaciones, revisiones de los code owners, ramas actualizadas o commits firmados antes de fusionar.

#### ¿Qué es un archivo CODEOWNERS?

Un archivo que asigna rutas a equipos o personas responsables, a los que se pide revisión automáticamente y cuya aprobación puede ser obligatoria para los cambios en sus áreas, por ejemplo `/models/finance/ @org/finance-data`.

#### ¿Qué es el versionado semántico y aplica a los datos?

Versionar como MAYOR.MENOR.PARCHE, donde las versiones mayores indican cambios que rompen. Aplica a las librerías y también a los productos y contratos de datos: una columna eliminada o un significado cambiado es una versión mayor; una columna opcional nueva, una menor.

#### ¿Qué son los conventional commits?

Una convención para los mensajes de commit (`feat:`, `fix:`, `chore:`, `docs:`, `feat!:` para los cambios que rompen) que hace legible el historial y permite a las herramientas generar changelogs y números de versión automáticamente.

#### ¿Cómo se manejan los hotfixes en trunk-based development?

Se corrige en una rama corta desde main, se fusiona por el pipeline normal (quizá acelerado) y se despliega; si hay una rama de release en producción, se hace cherry-pick de la corrección también allí. Evita parchar producción a mano.

#### ¿Qué es un monorepo frente a un polyrepo para datos?

Un monorepo guarda todos los pipelines, modelos e infraestructura en un repositorio (cambios transversales fáciles, herramientas compartidas, necesita CI por rutas); un polyrepo los divide por dominio o componente (propiedad y acceso claros, coordinación más difícil). Ambos funcionan con un buen CI.

#### ¿Cómo se mantienen cortas las ramas de funcionalidad?

Dividiendo el trabajo en cambios pequeños que se puedan fusionar de forma independiente, fusionando detrás de feature flags o programaciones desactivadas, haciendo rebase con frecuencia sobre main y apuntando a fusionar en uno o dos días.

#### ¿Para qué se usan los tags de Git en los despliegues?

Para marcar los puntos de publicación (`v1.4.0`) que disparan los workflows de publicación, identificar exactamente qué se desplegó y permitir revertir volviendo a desplegar un tag anterior.

#### ¿Cómo se manejan los notebooks en Git?

Guardándolos como archivos fuente (formato `.py` de Databricks, Jupytext) en lugar de JSON con salidas, quitando las salidas antes del commit, y manteniendo la lógica en módulos importables con notebooks delgados, para que los diffs se puedan revisar.

#### ¿Para qué se necesita Git LFS en los repositorios de datos?

Git LFS guarda archivos binarios grandes (pequeños datasets de referencia, datos de prueba, imágenes) fuera del historial normal de Git; los datos grandes de producción no deben estar en Git en absoluto.

### Estrategia de pruebas para datos

#### ¿Cómo es la pirámide de pruebas para los pipelines de datos?

Muchas pruebas unitarias rápidas de la lógica de transformación, menos pruebas de integración de componentes con motores reales (Spark, una base de prueba, dbt contra un esquema de prueba), unas pocas pruebas de extremo a extremo que ejecutan todo el pipeline con datos de muestra, más pruebas de calidad de datos que corren en producción con datos reales.

#### ¿Qué es una prueba unitaria en un pipeline de datos?

Una prueba rápida de una pequeña parte de la lógica con entradas controladas y salidas esperadas, como una función PySpark sobre un DataFrame diminuto, una función de parseo, o una macro o un modelo de dbt con entradas simuladas.

```python
def test_dedupe_keeps_latest(spark):
    df = spark.createDataFrame(
        [(1, "a", "2026-10-01"), (1, "b", "2026-10-02"), (2, "c", "2026-10-01")],
        ["id", "value", "updated_at"])
    result = dedupe_latest(df, key="id", order_col="updated_at")
    assert sorted(result.collect()) == sorted(
        spark.createDataFrame([(1, "b", "2026-10-02"), (2, "c", "2026-10-01")],
                              ["id", "value", "updated_at"]).collect())
```

#### ¿Cómo se estructura el código para que se pueda probar unitariamente?

Separando las funciones de transformación puras (DataFrame entra, DataFrame sale; filas entran, filas salen) de la E/S (leer fuentes, escribir tablas) y de la configuración; inyectando dependencias como rutas y fechas; y manteniendo delgados los notebooks o scripts de entrada.

#### ¿Qué es una prueba de integración de datos?

Una prueba que ejecuta componentes juntos con dependencias reales (o realistas): leer y escribir tablas reales en un esquema de prueba, ejecutar SQL en un sandbox del warehouse o llamar a una API simulada, verificando que las piezas encajan.

#### ¿Qué es una prueba de extremo a extremo de un pipeline?

Ejecutar todo el pipeline (de la ingesta a las tablas finales) sobre un conjunto de datos sintético pequeño y representativo en un entorno aislado, y comprobar las salidas (conteos de filas, valores clave, invariantes). Detecta errores de conexión entre piezas que las pruebas unitarias no ven.

#### ¿Qué son las pruebas de datos y en qué se diferencian de las pruebas de código?

Las pruebas de código verifican que la lógica se comporta como se espera con entradas controladas; las de datos verifican que los datos reales cumplen las expectativas (unicidad, no nulos, valores aceptados, integridad referencial, frescura, volumen). Se necesitan ambas: un código correcto puede producir datos malos a partir de entradas malas.

#### ¿Qué es la gestión de datos de prueba?

Crear y mantener conjuntos de datos para las pruebas: datos sintéticos pequeños para las unitarias, muestras anonimizadas o sintéticas para las de integración y datos parecidos a los de producción (enmascarados) para las de rendimiento, versionados con el código cuando sea posible.

#### ¿Por qué preferir datos sintéticos en CI?

Son seguros (sin datos personales), pequeños (pruebas rápidas), deterministas y pueden incluir a propósito casos límite (nulos, duplicados, registros tardíos, unicode, valores extremos) que serían raros en muestras reales.

#### ¿Qué es una prueba de contrato de datos?

Una prueba que verifica que la salida de un productor cumple el esquema y la semántica acordados en un contrato de datos (columnas, tipos, nulabilidad, valores permitidos), ejecutada en el CI del productor para que los cambios que rompen fallen antes de publicarse.

#### ¿Qué son las pruebas de regresión de los pipelines de datos?

Comparar las salidas de la nueva versión con las de la anterior sobre la misma entrada (conteos de filas, agregados, diferencias fila a fila), para detectar cambios no intencionados; las herramientas incluyen `datacompy`, dbt audit helper y enfoques de data-diff.

#### ¿Qué es una prueba de humo tras el despliegue?

Un control rápido justo después de desplegar de que el sistema funciona: los jobs están registrados, una ejecución pequeña termina bien, las tablas clave se pueden leer, los dashboards cargan. Detecta pronto los errores de configuración y de permisos.

#### ¿Cómo se prueban las transformaciones SQL?

Compilando y analizando el SQL en CI, ejecutando los modelos contra entradas pequeñas sembradas en un esquema de prueba y comparando con las salidas esperadas (pruebas unitarias de dbt), aplicando pruebas de datos sobre los resultados y haciendo linting del SQL en cuanto a estilo y antipatrones.

#### ¿Cómo se prueban los DAG de Airflow?

Cargando todos los DAG con `DagBag` y fallando ante errores de importación, revisando las convenciones (owners, reintentos, etiquetas, sin ciclos), probando unitariamente la lógica Python que usan las tareas y ejecutando pruebas de integración en un Airflow de staging.

#### ¿Qué son las pruebas basadas en propiedades y sirven para datos?

Generar muchas entradas aleatorias que cumplen restricciones y comprobar propiedades que siempre deberían cumplirse (por ejemplo, que la salida de la deduplicación tenga claves únicas y sea un subconjunto de la entrada). Herramientas como Hypothesis encuentran casos límite que las pruebas escritas a mano no ven.

#### ¿Qué son las pruebas de mutación?

Introducir pequeños cambios en el código (mutantes) y comprobar si las pruebas fallan; los mutantes que sobreviven revelan pruebas débiles. Se usan poco en los equipos de datos, pero son útiles para librerías críticas.

#### ¿Cómo se mantienen rápidos los conjuntos de pruebas?

Usando datos de prueba pequeños, compartiendo una SparkSession por sesión de pruebas, marcando las pruebas lentas y ejecutándolas aparte o solo en main, paralelizando con `pytest-xdist`, cacheando dependencias en CI y evitando llamar a servicios reales de la nube en las pruebas unitarias.

#### ¿Qué son los fixtures de pytest y cómo ayudan en las pruebas de datos?

Funciones de preparación reutilizables (una SparkSession, una base temporal, DataFrames de muestra) inyectadas en las pruebas por nombre, con alcances (función, módulo, sesión) para que los recursos costosos como Spark se creen una sola vez.

```python
import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark():
    session = (SparkSession.builder.master("local[2]")
               .config("spark.sql.shuffle.partitions", "2")
               .getOrCreate())
    yield session
    session.stop()
```

#### ¿Cómo se comparan DataFrames en las pruebas?

Con `pyspark.testing.assertDataFrameEqual` (Spark 3.5+) o `chispa` para PySpark, y `pandas.testing.assert_frame_equal` para pandas, con opciones para ignorar el orden de las filas y manejar decimales aproximados.

#### ¿Qué casos límite deben cubrir las pruebas de un pipeline de datos?

Entradas vacías, nulos en claves y valores, duplicados, registros tardíos y desordenados, cambios de esquema (columnas de más o de menos), formatos inválidos, zonas horarias y horario de verano, valores muy grandes, caracteres especiales y reejecuciones sobre la misma entrada (idempotencia).

#### ¿Cómo se prueba la idempotencia?

Ejecutando dos veces el paso del pipeline sobre la misma entrada y comprobando que la salida sea idéntica (mismo número de filas, sin duplicados, mismos agregados).

#### ¿Cómo se prueba el manejo de la evolución del esquema?

Alimentando datos de prueba con una columna añadida, una columna eliminada y un tipo cambiado, y comprobando que el pipeline se comporte según lo diseñado (acepta los cambios aditivos, falla de forma clara o pone en cuarentena los incompatibles).

#### ¿Qué son los "golden files" o pruebas de snapshot?

Salidas esperadas guardadas (CSV, JSON, Parquet) con las que se comparan los resultados de las pruebas; cuando las salidas cambian a propósito, los golden files se actualizan en el mismo pull request, haciendo visibles los cambios en la revisión.

#### ¿Cómo se prueba el rendimiento en CI?

Normalmente no en cada PR, sino con benchmarks periódicos sobre volúmenes representativos, siguiendo el tiempo de ejecución, el tamaño de los shuffles y el costo, y alertando ante regresiones; las reglas de lint pueden detectar barato los antipatrones de rendimiento conocidos.

### Calidad del código y controles estáticos

#### ¿Qué linters se usan en los proyectos de datos?

Ruff (linting y formateo de Python), mypy o pyright (verificación de tipos), SQLFluff (linting y formateo de SQL para muchos dialectos, compatible con dbt), yamllint, shellcheck, hadolint para Dockerfiles y controles propios de cada herramienta (dbt project evaluator, reglas `AIR` de Airflow).

#### ¿Qué es pre-commit?

Un framework que ejecuta hooks configurados (formateadores, linters, escáneres de secretos, controles de archivos grandes) en cada commit local, detectando problemas antes de que lleguen a CI; los mismos hooks pueden correr en CI por coherencia.

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
      - id: ruff-format
  - repo: https://github.com/sqlfluff/sqlfluff
    rev: 3.2.0
    hooks:
      - id: sqlfluff-lint
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.0
    hooks:
      - id: gitleaks
```

#### ¿Por qué imponer el formateo automáticamente?

Acaba con los debates de estilo en las revisiones, hace los diffs más pequeños y legibles, y permite a los revisores concentrarse en la lógica. Formateadores como Ruff y SQLFluff corrigen el formato automáticamente.

#### ¿Qué son las reglas de lint propias para el código de datos?

Controles específicos del proyecto contra antipatrones, como `collect()` sobre DataFrames grandes, UDF de Python donde existen funciones integradas, `SELECT *` en modelos de producción, rutas o credenciales escritas en el código, filtros de partición faltantes o `withColumn` dentro de bucles.

#### ¿Qué es el análisis estático de seguridad?

Herramientas como Bandit (problemas de seguridad en Python), Semgrep (reglas propias), Checkov o tfsec (malas configuraciones de infraestructura) y escáneres de dependencias que encuentran vulnerabilidades y patrones riesgosos antes del despliegue.

#### ¿Qué es la cobertura de código y cómo se debe usar?

El porcentaje de código que ejecutan las pruebas. Es una señal útil de áreas sin probar, pero no un objetivo en sí; apunta a pruebas significativas de la lógica crítica más que a un número, y vigila la tendencia de la cobertura en los archivos modificados.

#### ¿Cómo se revisan los proyectos dbt en CI?

Con `dbt deps`, `dbt parse` o `compile` para detectar errores de sintaxis y de referencias, linting con SQLFluff, el dbt project evaluator para las convenciones, y `dbt build` de los modelos modificados con sus pruebas en un esquema de CI.

#### ¿Por qué añadir anotaciones de tipo al código de datos?

Documentan las interfaces, permiten que los verificadores de tipos detecten errores (tipos de argumentos equivocados, manejo de `None`) antes de ejecutar y mejoran el soporte del IDE, lo que importa en las librerías compartidas por muchos pipelines.

#### ¿Qué es el dbt project evaluator?

Un paquete de dbt que revisa un proyecto contra buenas prácticas (nombres de modelos, capas, referencias directas a fuentes desde los marts, pruebas o documentación faltantes, patrones de fan-out) y puede hacer fallar el CI ante incumplimientos.

#### ¿Cómo se revisan los archivos YAML y de configuración?

Con validación de esquema (JSON Schema para las configuraciones, `databricks bundle validate`, `actionlint` para los workflows de GitHub), yamllint para la sintaxis y el estilo, y pruebas que cargan todos los archivos de configuración que usa el pipeline.

#### ¿Qué es actionlint?

Un verificador estático de los archivos de workflow de GitHub Actions que detecta errores de sintaxis, expresiones inválidas, entradas desconocidas y problemas en los scripts de shell antes de que corran los workflows.

### Entornos y configuración

#### ¿Qué entornos necesita una plataforma de datos?

Al menos desarrollo (sandboxes individuales o compartidos), un entorno de staging o preproducción que refleje producción, y producción. Algunos añaden entornos de pruebas/QA o entornos efímeros por pull request.

#### ¿Por qué separar los entornos por cuenta, workspace o catálogo?

El aislamiento limita el alcance de los errores, permite permisos distintos (los desarrolladores no pueden escribir en producción), separa los costos y hace explícita la promoción.

#### ¿Qué es la paridad de entornos?

Mantener los entornos lo más parecidos posible (mismo código, versiones, configuraciones, plantillas de infraestructura) para que las pruebas en staging predigan el comportamiento en producción; las diferencias deben limitarse a la escala, los datos y las credenciales.

#### ¿Cómo se administra la configuración por entorno?

Con archivos de configuración o variables por entorno (rutas, catálogos, tamaños de cluster, programaciones) inyectados al desplegar, manteniendo idéntico el código; los secretos vienen de un gestor de secretos, nunca de archivos del repositorio.

#### ¿Qué dice el principio twelve-factor sobre la configuración?

Guardar la configuración en el entorno (variables), no en el código, para que el mismo artefacto de compilación corra en todos los entornos con ajustes distintos.

#### ¿Qué son los entornos efímeros?

Entornos de corta vida creados automáticamente para un pull request (un esquema, una rama del catálogo, un clon de tablas, una copia desplegada de los jobs) y destruidos tras el merge, que permiten a los revisores probar los cambios de forma aislada.

#### ¿Cómo se proveen datos de prueba en staging?

Copiando o clonando los datos de producción con enmascaramiento o anonimización de los datos personales, tomando muestras para reducir el costo, usando clones zero-copy (Snowflake, shallow clones de Delta) donde existan, o generando datos sintéticos a escala de producción.

#### ¿Qué es el versionado de datos y por qué sirve en CI/CD?

Versionar los datasets como el código (ramas de lakeFS, Project Nessie para Iceberg, snapshots de Delta e Iceberg, snapshots de dbt) para reproducir ejecuciones, probar cambios sobre ramas aisladas de los datos y revertir escrituras malas.

#### ¿Qué es el patrón write-audit-publish (WAP)?

Escribir los datos nuevos en una ubicación o rama de staging, auditarlos con controles de calidad y solo entonces publicarlos (swap, merge o fast-forward), para que los consumidores nunca vean datos malos. Las ramas de Iceberg, lakeFS y los intercambios de tablas lo implementan.

#### ¿Cómo se nombran los recursos entre entornos?

Con un esquema coherente que incluya el entorno (`sales_prod`, `catalog_dev`, `dbt_ci_pr_123`), derivado de la configuración y no escrito en el código, para que el código nunca apunte por accidente a producción desde dev.

#### ¿Cómo trabajan los desarrolladores sin tocar los datos de producción?

Con esquemas o catálogos personales, targets de desarrollo que leen de producción en solo lectura (o de clones) y escriben solo en dev, datos muestreados o enmascarados, y permisos que impiden escribir en producción con las identidades de los desarrolladores.

#### ¿Qué es la promoción entre entornos?

Mover el mismo artefacto de dev a staging y a producción tras pasar los controles de cada etapa, en lugar de reconstruirlo, con aprobaciones para producción.

#### ¿Debe staging usar datos de producción?

Lo ideal es que staging use datos parecidos a los de producción (clonados, muestreados o enmascarados) para detectar problemas del mundo real, con controles estrictos sobre los datos personales; un staging puramente sintético puede no ver problemas que solo revelan los datos reales.

### Infraestructura como código

#### ¿Qué es la infraestructura como código (IaC)?

Definir los recursos de la nube (almacenamiento, cómputo, redes, permisos, catálogos, jobs) en código declarativo que se versiona, se revisa y se aplica automáticamente, en lugar de crearlos a mano en las consolas.

#### ¿Qué herramientas de IaC son comunes en las plataformas de datos?

Terraform/OpenTofu (multinube), AWS CloudFormation, CDK y SAM, Azure Bicep, Pulumi, y herramientas propias de cada plataforma como los Databricks Asset Bundles, el provider de Terraform de Snowflake y los manifiestos de Kubernetes con Helm.

#### ¿Qué es el flujo plan/apply de Terraform?

`terraform plan` muestra los cambios que se harían; los revisores revisan el plan en el pull request; `terraform apply` lo ejecuta tras la aprobación, normalmente desde CI con estado remoto y bloqueo.

#### ¿Qué es el estado de Terraform y cómo se debe guardar?

Un archivo que relaciona la configuración con los recursos reales. Se guarda de forma remota (S3 con bloqueo, Terraform Cloud, Azure Storage) con cifrado y control de acceso, nunca en Git, y con un estado separado por entorno.

#### ¿Qué es la deriva de configuración?

Las diferencias entre la infraestructura declarada y la realidad, causadas por cambios manuales. Se detecta con ejecuciones programadas de `terraform plan` o servicios de detección de deriva, y se corrige actualizando el código o revirtiendo los cambios manuales.

#### ¿Qué es la infraestructura inmutable?

Reemplazar los componentes por versiones nuevas en lugar de modificarlos en su lugar (imágenes de contenedor nuevas, clusters nuevos), lo que hace predecibles los despliegues y sencillas las reversiones.

#### ¿Cómo se estructura la IaC para varios entornos?

Con módulos reutilizables para los componentes comunes, variables o workspaces por entorno (dev, staging, prod), estado separado por entorno y los mismos módulos promovidos entre entornos.

#### ¿Cómo se revisan con seguridad los cambios de infraestructura?

Publicando el `terraform plan` (o el diff de CDK, el change set de CloudFormation) como comentario del pull request, exigiendo revisiones de los responsables de los recursos afectados, usando controles de políticas (Checkov, OPA/Conftest, Sentinel) y aplicando solo desde CI.

#### ¿Qué es la política como código?

Escribir las reglas de la organización (cifrado obligatorio, sin buckets públicos, etiquetas obligatorias, regiones aprobadas) como código evaluado automáticamente en CI o al desplegar, por ejemplo con Open Policy Agent, Checkov o los servicios de políticas nativos de la nube.

#### ¿Cómo se administran los permisos de la plataforma de datos como código?

Definiendo los roles, permisos y permisos del catálogo en Terraform o en las herramientas de la plataforma (provider de Snowflake, provider de Terraform de Databricks, permisos de Unity Catalog en los bundles), revisados en pull requests, para que los cambios de acceso sean auditables y reversibles.

### Empaquetado y artefactos

#### ¿Qué es un artefacto de compilación en los proyectos de datos?

La salida versionada de una compilación que se despliega: un wheel de Python con el código del pipeline, una imagen Docker, un JAR, un manifiesto de dbt compilado, un bundle o un zip de scripts SQL. Se construye una vez y se despliega el mismo artefacto en todas partes.

#### ¿Por qué "construir una vez, desplegar muchas"?

Reconstruir para cada entorno puede producir artefactos distintos (cambios de dependencias, el momento de la compilación), así que lo probado no es lo desplegado. Construir un artefacto y promoverlo garantiza la coherencia.

#### ¿Cómo se versionan los artefactos?

Con versiones semánticas para las librerías, y SHA de commit o números de compilación para las aplicaciones (`0.2.145+g1a2b3c4`), estampados al compilar para que cada despliegue se pueda rastrear hasta un commit.

#### ¿Dónde se guardan los artefactos?

En repositorios y registros de artefactos: repositorios compatibles con PyPI (CodeArtifact, Artifactory, GitHub Packages), registros de contenedores (ECR, ACR, GHCR), buckets de S3 para scripts, o almacenes de la plataforma (archivos del workspace y volúmenes de Databricks).

#### ¿Cómo se administran las dependencias de Python de forma reproducible?

Fijando las versiones exactas con archivos de bloqueo (`uv.lock`, `poetry.lock`, requirements de `pip-tools`), separando las dependencias de ejecución y de desarrollo, compilando en entornos limpios y actualizando las dependencias de forma deliberada (Dependabot o Renovate con pruebas).

#### ¿Por qué usar contenedores para los pipelines de datos?

Los contenedores empaquetan el código con las dependencias y librerías del sistema exactas, haciendo idénticas las ejecuciones en los computadores de los desarrolladores, en CI y en producción, y encajan con orquestadores como Kubernetes, ECS, el KubernetesPodOperator de Airflow y Cloud Run.

#### ¿Cómo se estampa una versión en un paquete Python en CI?

Derivándola de Git (setuptools-scm, `git describe`) o fijándola explícitamente en CI a partir del número de ejecución y el SHA corto, para que cada artefacto corresponda a un commit; evita reutilizar la misma versión para código distinto.

#### ¿Qué es un SBOM?

Una lista de materiales del software (software bill of materials) con todos los componentes y dependencias (y sus versiones) de un artefacto, generada en CI (Syft, CycloneDX) para seguir vulnerabilidades y licencias.

#### ¿Por qué escanear las imágenes de contenedor en CI?

Las imágenes base y las dependencias contienen vulnerabilidades conocidas; los escáneres (Trivy, Grype, el escaneo del registro) las encuentran antes del despliegue, y las políticas pueden bloquear los problemas críticos.

### Estrategias de despliegue

#### ¿Qué estrategias de despliegue existen?

Recreate (detener lo viejo, iniciar lo nuevo), rolling (reemplazar instancias poco a poco), blue-green (cambiar el tráfico entre dos entornos completos), canary (enviar primero una pequeña parte a la nueva versión), shadow (ejecutar la nueva versión en paralelo sin servir sus resultados) y feature flags (desplegar apagado y activar después).

#### ¿Cómo se aplica el despliegue blue-green a los datos?

Construyendo la nueva versión de las tablas o pipelines junto a las actuales (nuevo esquema, versión de tabla o clon), validándola y luego cambiando a los consumidores de forma atómica (intercambio de vistas, renombrado de tablas, puntero del catálogo), conservando la versión vieja para revertir rápido.

#### ¿Qué es un canary release para los pipelines de datos?

Ejecutar la nueva versión sobre un subconjunto (un país, una partición, una muestra de clientes) o en paralelo con la vieja, comparar salidas y métricas, y ampliarla cuando haya confianza.

#### ¿Qué es el modo shadow?

Ejecutar una nueva versión del pipeline en paralelo sobre entradas reales, escribiendo en tablas aparte que nadie consume, y comparar los resultados con la versión de producción antes de cambiar.

#### ¿Qué son los feature flags en las plataformas de datos?

Interruptores de configuración que activan o desactivan lógica o salidas nuevas sin volver a desplegar, lo que permite un despliegue gradual, desactivar rápido las funciones problemáticas y desacoplar el despliegue de la publicación.

#### ¿Cómo se revierte un despliegue de datos?

Volviendo a desplegar el artefacto de código anterior y, para los datos, restaurando las tablas con viaje en el tiempo o snapshots, devolviendo las vistas a la versión anterior (blue-green) o volviendo a ejecutar la lógica vieja en las particiones afectadas. Planifica la reversión antes de desplegar cambios riesgosos.

#### ¿Por qué los cambios de esquema de base de datos son riesgosos en los despliegues?

Pueden romper el código en ejecución, bloquear tablas, requerir migración de datos y son difíciles de revertir. Usa cambios compatibles hacia atrás (expand and contract), migraciones probadas sobre clones y despliega esquema y código en pasos compatibles.

#### ¿Qué es el patrón expand and contract?

Hacer los cambios de esquema por fases: expandir (añadir la columna o tabla nueva, conservar la vieja), migrar (escribir en ambas, hacer backfill, cambiar a los lectores), contraer (quitar la columna vieja cuando nadie la usa). Cada paso es compatible hacia atrás.

#### ¿Qué son las herramientas de migración de bases de datos?

Herramientas que aplican cambios de esquema versionados y ordenados y llevan registro de cuáles se ejecutaron: Flyway, Liquibase, Alembic (SQLAlchemy), Sqitch, schemachange (Snowflake) y dbt para los objetos que administra la transformación.

#### ¿Cómo se manejan los backfills en los despliegues?

Como parte del plan de publicación: estimar costo y duración, parametrizar los pipelines por rango de fechas, ejecutar en lotes controlados (a menudo fuera de horas pico), validar las salidas y avisar a los consumidores cuando cambian datos históricos.

#### ¿Cómo se despliega un cambio en una tabla muy usada sin interrupción?

Construyendo la nueva versión en paralelo (tabla o versión nueva), validándola, cambiando luego de forma atómica (swap, renombrado o actualización de una vista) y conservando la versión vieja para revertir; evita reescribir en su lugar mientras los consumidores leen.

#### ¿Cómo se despliega un cambio que exige recalcular el historial?

Planificando un backfill: desplegar la nueva lógica escribiendo en una tabla o versión nueva, recalcular el historial por lotes, validar frente a las salidas viejas, cambiar a los consumidores y comunicar las cifras reexpresadas, en lugar de sobrescribir el historial en su lugar sin controles.

#### ¿Qué es un congelamiento de despliegues y cuándo es apropiado?

Un periodo sin despliegues a producción, por ejemplo durante el cierre contable o los picos de ventas, para reducir el riesgo; es mejor hacer los despliegues seguros y rutinarios, y mantener los congelamientos cortos y solo para periodos de alto riesgo real.

#### ¿Cómo se despliegan los cambios de jobs de streaming?

Revisando la compatibilidad del estado, deteniendo el job de forma ordenada (savepoint o checkpoint), desplegando la nueva versión desde el mismo checkpoint si es compatible, o iniciando un job nuevo con un checkpoint nuevo y un plan de backfill; en los streams críticos, ejecutando la versión vieja y la nueva en paralelo.

### GitHub Actions a fondo

#### ¿Qué es GitHub Actions?

La plataforma de CI/CD y automatización de GitHub: workflows definidos en YAML en `.github/workflows/` que se ejecutan ante eventos (push, pull request, programación, disparo manual, releases) en runners alojados por GitHub o propios.

#### ¿Qué son los workflows, jobs y steps?

Un workflow es un proceso automatizado definido en un archivo YAML; contiene jobs que corren en runners, en paralelo por defecto o en orden con `needs`; cada job tiene steps que ejecutan comandos (`run`) o acciones (`uses`).

#### ¿Cómo es un workflow básico de CI para un proyecto de datos en Python?

```yaml
name: ci
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -r requirements-dev.txt
      - run: ruff check . && ruff format --check .
      - run: pytest -q --maxfail=1
```

#### ¿Qué disparadores pueden iniciar un workflow?

`push`, `pull_request` (y `pull_request_target`), `schedule` (cron), `workflow_dispatch` (manual, con entradas), `workflow_call` (reutilizable), `release`, `repository_dispatch` (API externa), `merge_group` (merge queue) y muchos otros eventos del repositorio.

#### ¿Cómo se ejecuta un workflow solo cuando cambian ciertos archivos?

Con filtros de rutas en el disparador, por ejemplo `on: pull_request: paths: ["models/**", "dbt_project.yml"]`, o con un paso que detecta los archivos cambiados y ejecuta jobs de forma condicional, lo que ahorra tiempo de CI en los monorepos.

#### ¿Qué es un runner?

La máquina que ejecuta los jobs: los runners alojados por GitHub (Ubuntu, Windows, macOS, tamaños más grandes y con GPU) son máquinas virtuales nuevas por job; los runners propios (self-hosted) son tus máquinas o pods de Kubernetes, usados para acceder a redes privadas, hardware especial o por costo.

#### ¿Por qué fijar la versión de la imagen del runner?

`ubuntu-latest` cambia cuando GitHub pasa a una imagen nueva, lo que puede romper las compilaciones sin aviso. Fijar `ubuntu-24.04` da compilaciones reproducibles; se actualiza a propósito.

#### ¿Qué es una compilación con matriz?

Ejecutar el mismo job con distintas combinaciones de parámetros en paralelo, por ejemplo varias versiones de Python o varios adaptadores de dbt.

```yaml
jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        python: ["3.11", "3.12"]
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - run: pip install -e ".[dev]" && pytest -q
```

#### ¿Cómo funciona el caché en GitHub Actions?

`actions/cache` (o el caché integrado de `setup-python`, `setup-node`, `setup-java`) guarda directorios como los cachés de pip o Maven con una clave basada en el hash de los archivos de bloqueo, y los restaura en ejecuciones posteriores para acelerar la instalación de dependencias.

#### ¿Qué son los artefactos en GitHub Actions?

Archivos producidos por un job (reportes de pruebas, wheels construidos, el sitio, manifiestos de dbt) subidos con `actions/upload-artifact` y descargables por jobs posteriores o por personas, con un periodo de retención.

#### ¿Cómo se pasan datos entre jobs?

Mediante artefactos para los archivos, y salidas de job para los valores pequeños: un step escribe `nombre=valor` en `$GITHUB_OUTPUT`, el job declara `outputs`, y los jobs dependientes los leen con el contexto `needs`.

#### ¿Qué son los secretos y las variables en GitHub Actions?

Los secretos son valores cifrados (tokens, contraseñas) disponibles para los workflows y enmascarados en los logs; las variables son valores de configuración no sensibles. Ambos se definen a nivel de organización, repositorio o entorno y se referencian con los contextos `secrets` y `vars`.

#### ¿Por qué los valores identificativos deben ser secretos en repositorios públicos?

Los logs de los workflows de los repositorios públicos son públicos, y solo se enmascaran los secretos. Nombres de host, IDs de cuenta, nombres de buckets o correos guardados como variables normales pueden filtrarse en los logs, así que trátalos como secretos cuando el repositorio es público.

#### ¿Qué son los entornos de GitHub?

Destinos de despliegue con nombre (dev, staging, production) con sus propios secretos y variables y reglas de protección: revisores obligatorios, temporizadores de espera, restricciones de ramas e historial de despliegues, que controlan los jobs de CD.

```yaml
jobs:
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-24.04
    environment:
      name: production
      url: https://data.example.com
    steps:
      - run: ./scripts/deploy.sh
```

#### ¿Qué es la autenticación OIDC desde GitHub Actions hacia la nube?

El workflow pide a GitHub un token OpenID Connect de corta duración, y el proveedor de nube (AWS, Azure, GCP) lo intercambia por credenciales temporales de un rol que confía en el repositorio, la rama o el entorno. No se guardan claves de acceso de larga duración.

```yaml
permissions:
  contents: read
  id-token: write
steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: ${{ secrets.AWS_DEPLOY_ROLE_ARN }}
      aws-region: eu-west-1
```

#### ¿Cómo se restringe qué workflows pueden asumir un rol de la nube mediante OIDC?

En la política de confianza del rol, condicionando sobre las claims del token: la audiencia (`sts.amazonaws.com`), el repositorio y la rama o el entorno en `sub` (por ejemplo `repo:org/repo:environment:production`), para que solo los despliegues de producción de ese repositorio puedan asumirlo.

#### ¿Qué es el `GITHUB_TOKEN` y cómo se deben definir sus permisos?

Un token creado automáticamente para cada ejecución, con alcance limitado al repositorio. Define `permissions:` a nivel de workflow o de job con lo mínimo necesario (a menudo `contents: read`), y concede permisos extra como `pull-requests: write` o `id-token: write` solo a los jobs que los necesitan.

#### ¿Qué son los workflows reutilizables?

Workflows disparados con `workflow_call` que otros workflows invocan con `uses: ./.github/workflows/ci.yml` (o desde otro repositorio), pasando entradas y secretos, para definir la lógica de CI una sola vez y reutilizarla, por ejemplo ejecutando todo el CI como barrera dentro del workflow de CD.

#### ¿Qué son las acciones compuestas (composite actions)?

Acciones propias definidas con `runs: using: composite` que agrupan varios pasos (preparación, instalación, configuración) en un solo paso reutilizable, guardadas en el repositorio o en un repositorio compartido.

#### ¿Qué hace `concurrency`?

Agrupa las ejecuciones por una clave y las limita a una a la vez; con `cancel-in-progress: true` una ejecución nueva cancela la anterior (bueno para el CI de los PR), con `false` las nuevas esperan (esencial en los despliegues para que nunca se solapen dos).

```yaml
concurrency:
  group: deploy-production
  cancel-in-progress: false
```

#### ¿Cómo se ejecutan jobs programados en GitHub Actions?

Con `on: schedule: - cron: "0 5 * * *"` (UTC). Es útil para controles nocturnos de deriva, auditorías de dependencias o jobs de datos pequeños, pero no reemplaza a un orquestador de datos: las programaciones pueden retrasarse y se desactivan en repositorios inactivos.

#### ¿Para qué sirve `workflow_dispatch`?

Para disparos manuales con entradas tipadas opcionales, por ejemplo desplegar una versión concreta, ejecutar un backfill para un rango de fechas o iniciar un job de producción tras el despliegue.

#### ¿Cómo se hacen condicionales los jobs?

Con expresiones `if:` en jobs o steps, usando contextos como `github.ref`, `github.event_name`, `needs.<job>.result`, variables (`vars.DEPLOY_AWS == 'true'`) o funciones como `success()`, `failure()` y `always()`.

#### ¿Por qué fijar las acciones de terceros a un SHA de commit?

Las etiquetas como `v4` se pueden mover, y una acción comprometida podría robar secretos. Fijar a un SHA de commit completo (con la versión como comentario) garantiza el código exacto que se ejecuta; Dependabot puede mantener actualizadas las acciones fijadas.

#### ¿Qué diferencia hay entre `pull_request` y `pull_request_target`?

`pull_request` corre en el contexto del commit de merge con un token de solo lectura y sin secretos para los forks, lo que es seguro. `pull_request_target` corre en el contexto del repositorio base con secretos; hacer checkout y ejecutar en él el código de un PR no confiable es un agujero de seguridad conocido.

#### ¿Cómo se añade una aprobación manual antes de producción?

Configurando el entorno de producción con revisores obligatorios; los jobs que referencian ese entorno se pausan hasta que un revisor autorizado aprueba el despliegue en la interfaz de GitHub.

#### ¿Qué es una merge queue?

Una función de GitHub que prueba los pull requests junto con el main más reciente (y entre sí) antes de fusionarlos en orden, evitando el "PR en verde, main roto" cuando se fusionan varios PR casi al mismo tiempo; el CI también debe correr en el evento `merge_group`.

#### ¿Cómo se muestran bien los resultados de las pruebas en GitHub Actions?

Subiendo los reportes JUnit XML como artefactos y publicándolos con una acción de reportes, escribiendo un resumen del job en `$GITHUB_STEP_SUMMARY` (Markdown) o comentando los resultados en el pull request.

#### ¿Para qué usan los equipos de datos los runners más grandes de GitHub y los propios?

Los runners más grandes ayudan con compilaciones pesadas o pruebas de Spark; los runners propios dentro de tu red en la nube pueden llegar a bases de datos o warehouses privados para las pruebas de integración sin exponerlos públicamente, pero hay que endurecerlos y aislarlos (se recomiendan runners efímeros).

#### ¿Cómo se compara GitHub Actions con GitLab CI y Azure DevOps?

Todos definen los pipelines en YAML con etapas o jobs, runners/agentes, variables y secretos, entornos y aprobaciones. GitLab CI usa `.gitlab-ci.yml` con stages y registro integrado; Azure DevOps usa `azure-pipelines.yml` con stages, service connections y una integración estrecha con Azure. Los conceptos se transfieren directamente.

#### ¿Cómo se pasan salidas entre jobs?

```yaml
jobs:
  version:
    runs-on: ubuntu-24.04
    outputs:
      tag: ${{ steps.v.outputs.tag }}
    steps:
      - id: v
        run: echo "tag=0.2.${{ github.run_number }}" >> "$GITHUB_OUTPUT"
  deploy:
    needs: version
    runs-on: ubuntu-24.04
    steps:
      - run: echo "Desplegando ${{ needs.version.outputs.tag }}"
```

#### ¿Cómo se llama a un workflow reutilizable?

```yaml
jobs:
  tests:
    uses: ./.github/workflows/ci.yml
  deploy:
    needs: tests
    runs-on: ubuntu-24.04
    environment: production
    steps:
      - run: echo "desplegar tras pasar el CI"
```

#### ¿Cómo se dispara un despliegue manual con entradas?

```yaml
on:
  workflow_dispatch:
    inputs:
      start_date:
        description: Primera fecha del backfill (AAAA-MM-DD)
        required: true
      run_job:
        type: boolean
        default: false
```

Las entradas quedan disponibles en los jobs y steps mediante el contexto `inputs`.

#### ¿Cómo se definen el shell y el directorio de trabajo por defecto?

Con `defaults: run:` a nivel de workflow o de job, por ejemplo `shell: bash` y `working-directory: ./dbt`, para que todos los steps `run` los usen; en GitHub Actions los steps de bash corren por defecto con `-e` (salir ante errores).

#### ¿Cómo se escribe un resumen del job?

Añadiendo Markdown al archivo de `$GITHUB_STEP_SUMMARY` (por ejemplo una tabla de conteos de filas o un reporte de pruebas), que aparece en la página de resumen de la ejecución.

#### ¿Cómo se añaden timeouts a los jobs?

Con `timeout-minutes` en los jobs (y en los steps), para que un job colgado no consuma minutos de runner durante horas; el timeout por defecto de un job es de 360 minutos.

#### ¿Qué son las expresiones y los contextos en GitHub Actions?

Las expresiones se escriben como `${{ ... }}` en el YAML de los workflows y acceden a contextos como `github` (datos del evento y del repositorio), `env`, `vars`, `secrets`, `matrix`, `needs`, `steps`, `runner` e `inputs`, con funciones como `contains`, `startsWith`, `format`, `hashFiles` y las de estado.

#### ¿Cómo se ejecuta un job solo en la rama main tras un push?

`if: github.ref == 'refs/heads/main' && github.event_name == 'push'`, lo que impide desplegar desde pull requests u otras ramas.

#### ¿Cómo se despliega solo cuando está definida una variable del repositorio?

Condicionando el job con `if: vars.DEPLOY_AWS == 'true'`, para que los jobs de despliegue queden inactivos hasta que esté lista la configuración del entorno, sin hacer fallar el CI mientras tanto.

#### ¿Cómo se publica un comentario en un pull request desde un workflow?

Con la CLI de GitHub (`gh pr comment`) o una acción con el `GITHUB_TOKEN` con permiso `pull-requests: write`, por ejemplo para compartir un plan de Terraform o los resultados del CI de dbt.

#### ¿Cómo se construye y publica una imagen Docker en GitHub Actions?

Con `docker/setup-buildx-action`, `docker/login-action` (hacia ECR, GHCR u otro registro, idealmente con OIDC) y `docker/build-push-action`, etiquetando las imágenes con el SHA del commit y usando caché de capas.

#### ¿Cómo ayudan Dependabot o Renovate al CI/CD?

Abren pull requests para actualizar las dependencias y las GitHub Actions fijadas, que pasan por el CI como cualquier cambio, manteniendo al día la cadena de suministro con actualizaciones probadas en lugar de actualizaciones grandes y riesgosas.

### CI/CD para dbt

#### ¿Qué ejecuta un pipeline de CI para dbt?

Instala las dependencias (`dbt deps`), revisa el estilo SQL (SQLFluff), compila o analiza, construye y prueba los modelos cambiados y sus hijos en un esquema de CI aislado, revisa la documentación y las convenciones, e informa los resultados en el pull request.

#### ¿Qué es el slim CI en dbt?

Construir y probar solo los modelos modificados y sus dependientes, comparando el estado con el manifiesto de producción: `dbt build --select state:modified+ --defer --state prod-artifacts/`, para que el CI sea rápido y barato.

```yaml
- name: Descargar el manifiesto de producción
  run: aws s3 cp s3://dbt-artifacts/prod/manifest.json prod-artifacts/manifest.json
- name: Construir los modelos modificados
  run: dbt build --select state:modified+ --defer --state prod-artifacts --target ci
```

#### ¿Qué hace `--defer`?

Cuando un modelo referencia un modelo anterior no modificado que no se construyó en el esquema de CI, dbt resuelve la referencia hacia la relación de producción, así el CI no tiene que reconstruir todo el proyecto.

#### ¿Cómo se aíslan las ejecuciones de CI de dbt?

Con un target de CI que escribe en un esquema único por pull request (por ejemplo `dbt_ci_pr_123`) y que se borra al terminar la ejecución o al cerrar el PR, para que los PR concurrentes no choquen.

#### ¿Cómo se despliega dbt en producción?

Al fusionar en main, se ejecuta `dbt build` (o un job de dbt Cloud) con el target de producción desde el orquestador, se guardan los artefactos (manifiesto, resultados) para la siguiente comparación de slim CI, se genera la documentación y se alerta ante fallos.

#### ¿Qué son las pruebas unitarias de dbt?

Pruebas (dbt 1.8+) que definen filas de entrada simuladas para los refs de un modelo y la salida esperada, y que se ejecutan sin datos reales, para verificar en CI lógica SQL compleja como los case y las funciones de ventana.

#### ¿Cómo se evita romper a los consumidores con los cambios de dbt?

Con contratos de modelo (nombres y tipos de columnas obligatorios), versiones de modelo para los cambios que rompen, niveles de acceso para los modelos públicos, exposures que documentan los dashboards que dependen de los modelos, y un CI que construye los modelos dependientes (`state:modified+`).

#### ¿Cómo se maneja el `profiles.yml` de dbt en CI?

Subiendo un archivo de perfiles que lee toda la configuración de conexión de variables de entorno (`env_var('DBT_HOST')`), y definiendo esas variables desde los secretos en el workflow; nunca se suben credenciales.

#### ¿Cómo se ejecutan los controles de frescura de las fuentes en dbt?

Con `dbt source freshness` en el job de producción (antes de construir) o de forma programada, fallando o advirtiendo cuando las fuentes son más viejas que los umbrales, lo que evita construir sobre entradas desactualizadas.

#### ¿Cómo se genera y publica la documentación de dbt?

Ejecutando `dbt docs generate` en el pipeline de producción y publicando el sitio estático (S3 con CloudFront, GitHub Pages, dbt Cloud) o enviando los metadatos a un catálogo, para que la documentación corresponda a lo desplegado.

#### ¿Para qué sirve el comando "clone" de dbt en CI?

`dbt clone` crea clones zero-copy (o vistas) de las relaciones de producción en el esquema de CI o de desarrollo, para que los modelos incrementales y las pruebas posteriores corran sobre un estado realista a bajo costo.

### CI/CD para Databricks, Airflow y warehouses

#### ¿Cómo se configura CI/CD para Databricks?

Guardando el código y las definiciones de los Databricks Asset Bundles en Git; en CI, pruebas unitarias con Spark local, linting y `databricks bundle validate`; en CD, despliegue con `databricks bundle deploy -t <target>` como service principal autenticado con OAuth o federación de identidades de carga de trabajo, ejecutando opcionalmente jobs de integración en staging antes de producción.

```yaml
- uses: databricks/setup-cli@main   # fija un SHA de commit en producción
  with:
    version: ${{ vars.DATABRICKS_CLI_VERSION }}
- name: Validar y desplegar el bundle
  env:
    DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
    DATABRICKS_CLIENT_ID: ${{ secrets.DATABRICKS_CLIENT_ID }}
    DATABRICKS_CLIENT_SECRET: ${{ secrets.DATABRICKS_CLIENT_SECRET }}
  run: |
    databricks bundle validate -t prod
    databricks bundle deploy -t prod
```

#### ¿Por qué desplegar los jobs de Databricks como service principal?

Para que los jobs de producción no dependan de la cuenta y los permisos de una persona, el acceso se limite a lo que necesita el pipeline y la propiedad sobreviva a la salida de las personas.

#### ¿Cómo se despliegan los DAG de Airflow con CI/CD?

Ejecutando en CI las pruebas de integridad de los DAG y las unitarias, construyendo una imagen con los DAG y las dependencias fijadas (o sincronizando los archivos de DAG al bucket de MWAA o Composer), desplegando en staging, ejecutando pruebas de humo y promoviendo a producción, con reversión volviendo a desplegar la imagen o el commit anterior.

#### ¿Cómo se administran los cambios de Snowflake con CI/CD?

Los objetos de cuenta (warehouses, roles, permisos, integraciones) con Terraform; los esquemas y tablas con herramientas de migración (schemachange, Flyway) o scripts `CREATE OR ALTER`; las transformaciones con dbt; todo desplegado desde CI por un usuario de servicio con autenticación por par de claves u OAuth, probado primero sobre una base clonada.

#### ¿Cómo se despliegan los jobs de AWS Glue con CI/CD?

Empaquetando el código compartido como wheel, subiendo scripts y wheels a S3 con rutas versionadas, definiendo los jobs, triggers y tablas del catálogo con CloudFormation, CDK o Terraform, y ejecutando las pruebas en local con la imagen Docker de Glue o Spark antes del despliegue.

#### ¿Cómo se prueban en CI los pipelines que dependen de servicios en la nube?

Simulando los servicios en las pruebas unitarias (moto para AWS, LocalStack), usando equivalentes locales (Spark con Delta, contenedores de PostgreSQL, MinIO para S3) en las de integración, y ejecutando unas pocas pruebas contra una cuenta sandbox real en staging.

#### ¿Qué son los service containers en GitHub Actions?

Contenedores Docker que se inician junto a un job (por ejemplo PostgreSQL o Redis) para las pruebas de integración, definidos en `services:` con puertos y health checks.

```yaml
services:
  postgres:
    image: postgres:16
    env:
      POSTGRES_PASSWORD: postgres
    ports: ["5432:5432"]
    options: >-
      --health-cmd "pg_isready -U postgres"
      --health-interval 5s --health-retries 10
```

#### ¿Cómo se prueba el código de Databricks antes de desplegarlo?

Con pruebas unitarias en Spark local (o Databricks Connect), linting de los patrones no admitidos en serverless, `databricks bundle validate --strict`, despliegue en un target de desarrollo o staging con `mode: development` y ejecución de jobs de integración allí.

#### ¿Cómo se ejecuta un job de Databricks desde CI tras desplegar?

Con `databricks bundle run -t <target> <job_key>` (con `--no-wait` si no quieres que el CI espere), o disparándolo con la API de Jobs; en producción, a menudo solo con un disparo manual.

#### ¿Cómo se manejan las Variables y Connections de Airflow en CI/CD?

Manteniendo la configuración no secreta en el código o en variables de entorno de la imagen, y los secretos en un secrets backend; nunca creando a mano las conexiones de producción en la interfaz, para que los entornos sean reproducibles.

#### ¿Cómo se despliegan las transformaciones de BigQuery o Dataform?

Con las release configurations y workflow configurations de Dataform integradas con Git, o con dbt y el adaptador de BigQuery, desplegando desde CI con una cuenta de servicio mediante federación de identidades de carga de trabajo.

### Seguridad de la cadena de entrega

#### ¿Cuáles son los principales riesgos de seguridad en CI/CD?

Secretos filtrados en el código o los logs, credenciales demasiado amplias, acciones o dependencias de terceros comprometidas, código no confiable que corre con secretos (forks, `pull_request_target`), runners propios inseguros y cambios sin revisar que llegan a producción.

#### ¿Qué es el escaneo de secretos?

Detectar secretos en el código y en el historial con herramientas como gitleaks, TruffleHog o el escaneo de secretos y la protección de push integrados de GitHub, bloqueando commits y alertando ante filtraciones para revocar las credenciales.

#### ¿Qué se debe hacer si se sube un secreto al repositorio?

Revocarlo y rotarlo de inmediato (asume que está comprometido) y luego quitarlo del historial si hace falta; borrar el commit no basta, porque los clones y los cachés pueden tenerlo.

#### ¿Qué es la seguridad de la cadena de suministro de software?

Proteger el camino del código fuente a producción: dependencias y acciones fijadas y verificadas, escaneo de vulnerabilidades de las dependencias (Dependabot, pip-audit), SBOM, artefactos firmados y procedencia (SLSA, Sigstore), y sistemas de compilación con el mínimo privilegio.

#### ¿Qué es el mínimo privilegio en CI/CD?

Que cada workflow y job reciba solo los permisos que necesita: tokens de solo lectura por defecto, credenciales de despliegue solo en los jobs de despliegue, secretos con alcance de entorno y roles de nube restringidos a recursos y ramas concretos.

#### ¿Cómo se protege producción de despliegues no autorizados?

Con protección de la rama main, revisiones obligatorias, reglas de protección del entorno con aprobadores, políticas de confianza OIDC restringidas al entorno de producción y logs de auditoría de los despliegues.

#### ¿Cómo se manejan los datos sensibles en los logs de CI?

No imprimiendo nunca secretos ni datos reales; confiando en el enmascarado pero sin fiarse del todo; usando datos sintéticos en las pruebas; revisando los logs de los repositorios públicos; y limitando la retención de los logs.

#### ¿Por qué son riesgosos los runners propios y cómo se aseguran?

Ejecutan código arbitrario de los workflows dentro de tu red; un PR malicioso podría atacar sistemas internos. Usa runners efímeros (un job por runner), nunca ejecutes en ellos código de forks no confiables, aísla las redes y restringe qué repositorios pueden usarlos.

#### ¿Qué es un ataque de "poisoned pipeline execution"?

Un atacante modifica en un pull request la configuración del CI o archivos que ejecuta el CI (scripts, Makefiles) para que el pipeline ejecute código malicioso con acceso a los secretos. Se mitiga con tokens de mínimo privilegio, sin secretos para los PR no confiables y con revisiones obligatorias de los cambios del CI.

#### ¿Cómo se protege la propia configuración del CI?

Exigiendo la revisión de los code owners para `.github/workflows/`, restringiendo quién puede modificar los entornos y los secretos, fijando las acciones y auditando los cambios de los workflows.

### Operación, monitoreo y DataOps

#### ¿Qué debe pasar después de un despliegue?

Pruebas de humo, monitoreo de las ejecuciones de los jobs y de los controles de calidad en la siguiente ejecución, comparación de las métricas clave con las ejecuciones anteriores y notificaciones al equipo; revertir rápido si fallan los controles.

#### ¿Cómo se sabe si un despliegue de datos rompió algo?

Con pruebas de calidad y observabilidad de datos (frescura, volumen, cambios de esquema y de distribución), alertas de fallo de los pipelines, conciliación con las fuentes y dashboards de métricas clave comparadas con su historial reciente.

#### ¿Qué es GitOps?

Usar Git como única fuente de verdad del estado deseado, con agentes automatizados que lo aplican al entorno (Argo CD, Flux para Kubernetes), de modo que cada cambio es un commit y el sistema converge a lo que hay en el repositorio.

#### ¿Cómo se documenta una publicación?

Con las descripciones de los pull requests, un changelog (a menudo generado a partir de conventional commits), notas de publicación para los consumidores que describen el impacto en los datos (columnas nuevas, definiciones cambiadas, backfills) y ADR para las decisiones importantes.

#### ¿Cómo se comunican los cambios de datos a los consumidores?

Con changelogs y notas de publicación, avisos de obsolescencia con plazos, actualizaciones del catálogo, subidas de versión de los contratos y comunicación directa para los cambios que rompen o las reexpresiones del historial.

#### ¿Cómo se mide el éxito de CI/CD en un equipo de datos?

Con las métricas DORA (frecuencia de despliegue, tiempo de entrega, tasa de fallos de los cambios, tiempo de restauración), el número de incidentes de datos causados por cambios, el tiempo dedicado a despliegues manuales y la duración y el costo del CI.

#### ¿Cómo se mantiene rápido el CI a medida que crece el proyecto?

Probando solo lo que cambió (filtros de rutas, slim CI), paralelizando jobs y pruebas, cacheando dependencias, usando datos sintéticos más pequeños, separando las pruebas de integración lentas para que corran en main o de noche, y usando runners más grandes donde se justifique.

#### ¿Cómo se controlan los costos del CI?

Cancelando las ejecuciones superadas, evitando ejecutar jobs pesados en cada commit, cacheando dependencias, usando slim CI contra los warehouses, borrando automáticamente los esquemas de CI, definiendo timeouts en los jobs y vigilando los minutos y el gasto de warehouse por repositorio.

#### ¿Qué es un registro de despliegues y por qué conservarlo?

Un registro de qué versión se desplegó dónde y cuándo, por quién y con qué aprobaciones (despliegues de GitHub, historial de los entornos, notas de publicación), esencial para relacionar los incidentes con los cambios.

#### ¿Cómo se relaciona un incidente de datos con un despliegue?

Comparando la hora de inicio del incidente con el historial de despliegues, revisando qué modelos o jobs cambiaron (diff de Git entre versiones), revisando el linaje de las tablas afectadas y mirando las métricas de calidad antes y después.

#### ¿Qué son las pruebas de caos para los pipelines de datos?

Introducir fallos a propósito en un entorno de pruebas (jobs matados, archivos faltantes, fuentes retrasadas, cambios de esquema) para verificar que los reintentos, las alertas, la idempotencia y los procedimientos de recuperación funcionan como se espera.

### Escenarios

#### Diseña un pipeline de CI/CD para un proyecto dbt sobre Snowflake.

En los pull requests: linting con SQLFluff, `dbt deps`, `dbt build --select state:modified+ --defer` contra un esquema propio del PR con un usuario de servicio de CI, publicación de los resultados y borrado del esquema al final. Al fusionar: despliegue disparando el job de producción (orquestador o dbt Cloud), guardado de los artefactos para la siguiente comparación y publicación de la documentación. Los warehouses y roles se administran con Terraform en el mismo pipeline o en uno aparte.

#### Diseña el CI/CD de un lakehouse PySpark en Databricks y AWS.

CI en los pull requests: escaneo de secretos, Ruff y reglas de lint propias para Spark, pruebas unitarias con Spark local y Delta, prueba de extremo a extremo con datos sintéticos y validación del bundle. CD en main: reutilizar el CI como barrera (workflow reutilizable) y luego desplegar la ingesta en AWS (SAM o Terraform) mediante OIDC y el bundle de Databricks como service principal, ambos en un entorno de producción protegido con concurrency configurado para que los despliegues nunca se solapen.

#### Un despliegue rompió una tabla de producción. ¿Qué debió detectar tu proceso y cómo te recuperas?

Primero recupero: revierto el código, restauro la tabla con viaje en el tiempo o vuelvo a ejecutar la lógica vieja en las particiones afectadas, e informo a los consumidores. Después mejoro el pipeline: añado una prueba del caso que falló, un control de contrato o de esquema, una comparación de regresión en CI, o write-audit-publish para que los datos malos no se expongan.

#### Tu CI tarda 45 minutos y los desarrolladores se lo saltan. ¿Qué haces?

Perfilo el pipeline, paralelizo los jobs independientes, cacheo las dependencias, ejecuto solo las pruebas afectadas (filtros de rutas, slim CI), reduzco los datos de prueba, paso las pruebas de extremo a extremo lentas a la merge queue o a main, y fijo una meta (por ejemplo menos de 10 minutos para los controles de los PR).

#### Los logs de los workflows de un repositorio público muestran el nombre de host de una base de datos. ¿Qué cambias?

Paso el nombre de host y los demás valores identificativos a secretos del entorno para que se enmascaren, roto las credenciales si apareció algo sensible, reviso los logs anteriores y añado un control que impida imprimir la configuración en los logs.

#### ¿Cómo migrarías de despliegues manuales a CI/CD?

Llevando todo a Git (código, configuración, infraestructura), añadiendo CI con linting y pruebas en los pull requests, automatizando el despliegue a un entorno de staging, añadiendo pruebas de humo y aprobaciones, luego automatizando el despliegue a producción con los mismos artefactos y retirando poco a poco el acceso manual a producción.

#### ¿Cómo le explicas el CI/CD de datos a una persona no técnica?

Es una línea automática de control de calidad y de entrega para nuestros pipelines de datos: cada cambio se prueba antes de que pueda afectar los reportes, y los cambios aprobados llegan a producción de la misma forma segura cada vez, para que las cifras sigan siendo confiables mientras las mejoramos rápido.

#### ¿Cómo añadirías controles de calidad de datos a un pipeline de CI/CD existente?

Añadiendo pruebas de datos al proyecto de transformación (unicidad, no nulos, relaciones, valores aceptados), ejecutándolas en CI con datos de prueba y en producción tras cada construcción, bloqueando la publicación (write-audit-publish o fallando el job) ante fallos críticos y alertando a los responsables.

#### Dos equipos despliegan en el mismo workspace de Databricks y se sobrescriben los jobs. ¿Cómo lo corriges?

Usando bundles con nombres y targets distintos por equipo, desplegando con el service principal de cada equipo con permisos limitados a sus recursos, usando el modo de desarrollo para los despliegues personales y separando los despliegues de producción por repositorio y protecciones de entorno.

#### Un `terraform apply` en CI borró un recurso de producción. ¿Cómo evitas que vuelva a pasar?

Exigiendo la revisión del plan antes del apply, añadiendo reglas de ciclo de vida `prevent_destroy` en los recursos críticos, ejecutando controles de políticas que bloqueen el borrado de recursos protegidos, separando el estado y los permisos por entorno, y, de inmediato, restaurando desde los respaldos o volviendo a importar el recurso.
