## Guía de estudio de CI/CD para datos

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de CI/CD para datos: unas 200 preguntas](../../images/cicd_data_study_guide_title_img.png)

Unas 200 preguntas tipo entrevista sobre CI/CD y automatización para plataformas de datos: flujos de Git, estrategias de pruebas de pipelines y datos, calidad del código, entornos, infraestructura como código, patrones de despliegue, GitHub Actions a fondo, CI/CD para dbt, Databricks, Airflow y warehouses, seguridad de la cadena de entrega y operación. Los ejemplos usan GitHub Actions, con notas sobre GitLab CI y Azure DevOps.

La guía sigue una ruta de aprendizaje en seis etapas. Cada sección se divide en unidades cortas: objetivos de aprendizaje, una explicación del concepto y un ejemplo resuelto, luego preguntas (primero de memoria, después de aplicación), un reto práctico e ideas clave. Para **aprender**, lee cada unidad de principio a fin. Para **repasar**, cambia al modo repaso o usa "Ir a las preguntas", marca las respuestas que quieras volver a ver y prueba un repaso mixto entre secciones.

<!-- QA -->
<!-- stage: Fundamentos -->

### Fundamentos

<!-- unit: CI/CD y DataOps -->

<!-- goals -->

- Explicar qué son CI/CD y DataOps y por qué los equipos de datos los necesitan.
- Describir qué hace distinto el CI/CD para datos frente a aplicaciones.

<!-- concept -->

Los pipelines de datos son software y fallan igual: un error en un join, un cambio sin probar, un deploy manual un viernes. CI/CD vuelve cada cambio una rutina: se integra seguido, se revisa automáticamente y se entrega siempre igual. DataOps lleva ese hábito a los datos, con pruebas y monitoreo sobre lo que producen los pipelines.
La dificultad extra es el estado. Una aplicación se reemplaza; una tabla con cinco años de historia hay que migrarla, recalcularla y mantenerla consistente para quienes la consumen.

<!-- example -->

| Paso | A mano | Con CI/CD |
|---|---|---|
| Cambiar un modelo de dbt | Editar en prod y rezar | PR, CI lo construye y lo prueba |
| Desplegar | Copiar archivos al servidor | El pipeline despliega un artefacto versionado |
| Saber qué se rompió | Preguntar por ahí | Historial de Git y log de despliegues |

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

<!-- challenge -->

Un equipo dice "nuestro SQL es simple, no necesitamos CI". Da dos fallas concretas que CI atraparía en un proyecto solo de SQL.

<!-- solution -->

Un modelo que referencia una columna renombrada (se atrapa compilando y construyendo en un esquema de CI) y un join que duplica filas (se atrapa con una prueba de unicidad sobre la llave de salida). Sin CI, ambas llegarían a los dashboards.

<!-- takeaways -->

- CI/CD hace los cambios pequeños, revisados y repetibles.
- DataOps agrega pruebas y monitoreo de los datos mismos.
- Los datos tienen estado: los cambios exigen migraciones y backfills.

<!-- unit: Pipelines y etapas -->

<!-- goals -->

- Describir las etapas de un pipeline de despliegue y qué automatiza cada una.
- Distinguir continuous delivery, continuous deployment y releases.

<!-- concept -->

Un pipeline de despliegue es una línea de ensamblaje del commit a producción. Build produce artefactos, test los verifica y deploy instala esos mismos artefactos en cada ambiente, uno tras otro. Cada etapa es una compuerta: una falla detiene la línea antes de que el daño se propague.
Hasta dónde automatizar es una decisión. Continuous delivery mantiene cada cambio listo para desplegar; continuous deployment lo despliega solo. Los releases, cuando los usuarios ven el cambio, se pueden separar de los despliegues con flags.

<!-- example -->

```text
commit ─► lint + unit tests ─► build wheel/image/manifest ─► deploy staging
       ─► integration + data tests ─► [approval] ─► deploy prod ─► smoke test
```

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

<!-- challenge -->

Un nuevo modelo de ingresos debe salir esta semana, pero solo activarse para finanzas a fin de mes. ¿Cómo separas despliegue y release?

<!-- solution -->

Despliega el modelo ya, detrás de un flag o en una tabla nueva que los dashboards aún no usan, valídalo en producción y a fin de mes cambia el dashboard de finanzas hacia él (activando el flag o cambiando la vista).

<!-- takeaways -->

- Los pipelines construyen, prueban y despliegan los mismos artefactos.
- Delivery deja los cambios desplegables; deployment los despliega solo.
- Los releases se pueden separar de los despliegues.

<!-- unit: Principios de entrega -->

<!-- goals -->

- Aplicar todo como código, cambios pequeños y calidad shift-left.
- Medir la entrega con métricas DORA y ownership.

<!-- concept -->

Unos pocos principios explican por qué funciona CI/CD. Todo lo que define la plataforma vive en código, así que se puede revisar y reconstruir. Los cambios son pequeños, fáciles de entender y deshacer. Los problemas se atrapan lo antes posible, donde son más baratos. Los pipelines son deterministas: repetir da el mismo resultado.
El ownership y la medición lo mantienen honesto: quien construye un pipeline lo opera, y las métricas DORA muestran si la entrega es más rápida y segura.

<!-- example -->

| Métrica DORA | Equipo de datos sano |
|---|---|
| Frecuencia de despliegue | Varias veces por semana |
| Lead time de cambios | De horas a un día |
| Tasa de fallas por cambio | Menos del 15 % |
| Tiempo de recuperación | Menos de una hora |

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

#### ¿Por qué el código de datos debe estar en Git?

El control de versiones da historial (quién cambió qué y por qué), colaboración mediante ramas y pull requests, la posibilidad de revertir, una única fuente de verdad para los despliegues y el disparador del CI/CD.

<!-- challenge -->

Un equipo despliega una vez al mes un lote de 40 cambios, y cada release trae incidentes. ¿Qué dos cambios ayudan más?

<!-- solution -->

Desplegar cambios pequeños de forma continua (trunk-based, pipeline automatizado) para que cada release sea pequeño y diagnosticable, y adelantar pruebas y chequeos automáticos (shift left) para que lleguen menos defectos a producción.

<!-- takeaways -->

- Todo como código hace las plataformas revisables y reconstruibles.
- Cambios pequeños y frecuentes reducen el riesgo.
- Las métricas DORA miden velocidad y estabilidad.

### Control de versiones y flujos de Git

<!-- unit: Qué va en Git -->

<!-- goals -->

- Decidir qué pertenece a un repositorio de datos y qué nunca.
- Versionar bien notebooks y archivos grandes.

<!-- concept -->

Git es la fuente de verdad de todo lo que define un pipeline: código, SQL, configuración, pruebas, infraestructura y documentación. Lo que no está en Git no se puede revisar, reproducir ni revertir.
Algunas cosas deben quedar por fuera: secretos, datos personales reales, datasets grandes y archivos generados. Los notebooks y binarios necesitan manejo especial, porque sus formatos por defecto producen diffs ilegibles o inflan el repositorio.

<!-- example -->

```gitignore
.env
*.parquet
data/
target/            # dbt build output
.venv/
**/.ipynb_checkpoints/
```

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

<!-- challenge -->

Un científico de datos hace commit de notebooks con celdas de salida que contienen registros de clientes. ¿Qué implementas?

<!-- solution -->

Quitar las salidas automáticamente (nbstripout o un hook de pre-commit), guardar los notebooks como archivos fuente (Jupytext o `.py` de Databricks), borrar los datos filtrados del historial y tratarlo como un incidente de datos.

<!-- takeaways -->

- Código, SQL, config, pruebas e infraestructura van en Git.
- Secretos, datos personales y archivos grandes nunca.
- Guarda notebooks como fuente; usa LFS para binarios necesarios.

<!-- unit: Flujos de ramas -->

<!-- goals -->

- Comparar trunk-based development y GitFlow.
- Mantener ramas cortas y manejar hotfixes y la estructura del repo.

<!-- concept -->

La estrategia de ramas decide cuánto tiempo viven separados los cambios. Las ramas largas se alejan de main, y fusionarlas se vuelve un proyecto aparte. Trunk-based development mantiene las ramas uno o dos días y fusiona piezas pequeñas seguido; por eso encaja con CI/CD.
Las ramas cortas necesitan técnicas para el trabajo sin terminar, como flags y caminos de código desactivados, y una ruta clara para arreglos urgentes. La estructura del repositorio es una decisión relacionada: un repo para todo o uno por componente.

<!-- example -->

```text
main ──●──●──●──●──●──●──   (always deployable)
        \  /    \ /
  feat/orders-dedupe   fix/null-country   (hours to 2 days each)
```

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

<!-- challenge -->

Un desarrollador lleva tres semanas en una rama que reescribe el pipeline de clientes, y fusionarla ahora genera conflictos por todas partes. ¿Cómo debió organizarse?

<!-- solution -->

En pasos pequeños y fusionables: agregar el pipeline nuevo junto al viejo, detrás de un flag o escribiendo en una tabla nueva, fusionar cada parte a main cuando esté lista, luego cambiar a los consumidores y borrar el código viejo.

<!-- takeaways -->

- Trunk-based development fusiona cambios pequeños a diario.
- Flags y caminos paralelos mantienen fusionable el trabajo sin terminar.
- Los hotfixes pasan por main y el pipeline normal.

<!-- unit: Revisiones y protecciones -->

<!-- goals -->

- Escribir y revisar pull requests de código de datos.
- Exigir revisiones con branch protection y CODEOWNERS.

<!-- concept -->

Los pull requests son donde una segunda persona ve un cambio antes de producción. En código de datos, una buena revisión va más allá del estilo: grano y fan-out en joins, manejo de nulos y duplicados, idempotencia, rendimiento e impacto en los consumidores.
La configuración del repositorio hace obligatorias las revisiones: las ramas protegidas exigen chequeos aprobados y aprobaciones, y los code owners se agregan solos para las rutas que conocen.

<!-- example -->

```text
# .github/CODEOWNERS
/models/finance/        @acme/finance-data
/infra/                 @acme/platform
/.github/workflows/     @acme/platform
```

#### ¿Cómo se manejan los hotfixes en trunk-based development?

Se corrige en una rama corta desde main, se fusiona por el pipeline normal (quizá acelerado) y se despliega; si hay una rama de release en producción, se hace cherry-pick de la corrección también allí. Evita parchar producción a mano.

#### ¿Qué es un monorepo frente a un polyrepo para datos?

Un monorepo guarda todos los pipelines, modelos e infraestructura en un repositorio (cambios transversales fáciles, herramientas compartidas, necesita CI por rutas); un polyrepo los divide por dominio o componente (propiedad y acceso claros, coordinación más difícil). Ambos funcionan con un buen CI.

#### ¿Cómo se mantienen cortas las ramas de funcionalidad?

Dividiendo el trabajo en cambios pequeños que se puedan fusionar de forma independiente, fusionando detrás de feature flags o programaciones desactivadas, haciendo rebase con frecuencia sobre main y apuntando a fusionar en uno o dos días.

#### ¿Para qué se usan los tags de Git en los despliegues?

Para marcar los puntos de publicación (`v1.4.0`) que disparan los workflows de publicación, identificar exactamente qué se desplegó y permitir revertir volviendo a desplegar un tag anterior.

<!-- challenge -->

Un PR cambia un join de `customer_id` a `email` y todas las pruebas pasan. ¿Qué preguntaría un buen revisor?

<!-- solution -->

Si `email` es único por cliente (si no, el join se abre y duplica filas), cómo se manejan nulos y diferencias de mayúsculas, y qué modelos y dashboards cambian aguas abajo. Pedir una prueba de unicidad sobre la salida.

<!-- takeaways -->

- Revisa joins, grano, nulos, idempotencia e impacto.
- Branch protection hace obligatorios chequeos y aprobaciones.
- CODEOWNERS dirige las revisiones a las personas indicadas.

<!-- unit: Versiones e historial -->

<!-- goals -->

- Aplicar versionado semántico a código y contratos de datos.
- Usar conventional commits y tags en los releases.

<!-- concept -->

Las versiones comunican qué significa un cambio. El versionado semántico lo dice en tres números: un major rompe algo, un minor agrega, un patch corrige. Aplica a librerías y también a contratos de datos: renombrar una columna es un cambio major para los consumidores.
Los mensajes de commit y los tags lo automatizan. Los conventional commits codifican el tipo de cambio, así las herramientas calculan la siguiente versión y el changelog, y los tags marcan exactamente qué se liberó.

<!-- example -->

```text
fix(orders): exclude test customers from revenue      → 2.3.1
feat(orders): add refund_amount column                → 2.4.0
feat!(orders): rename amount to gross_amount          → 3.0.0
git tag v3.0.0 && git push origin v3.0.0              # triggers the release workflow
```

#### ¿Cómo se manejan los notebooks en Git?

Guardándolos como archivos fuente (formato `.py` de Databricks, Jupytext) en lugar de JSON con salidas, quitando las salidas antes del commit, y manteniendo la lógica en módulos importables con notebooks delgados, para que los diffs se puedan revisar.

#### ¿Para qué se necesita Git LFS en los repositorios de datos?

Git LFS guarda archivos binarios grandes (pequeños datasets de referencia, datos de prueba, imágenes) fuera del historial normal de Git; los datos grandes de producción no deben estar en Git en absoluto.

#### ¿Cómo es la pirámide de pruebas para los pipelines de datos?

Muchas pruebas unitarias rápidas de la lógica de transformación, menos pruebas de integración de componentes con motores reales (Spark, una base de prueba, dbt contra un esquema de prueba), unas pocas pruebas de extremo a extremo que ejecutan todo el pipeline con datos de muestra, más pruebas de calidad de datos que corren en producción con datos reales.

<!-- challenge -->

Un equipo renombra una columna de una tabla compartida como "arreglo menor". Se rompen tres dashboards. ¿Cómo habría ayudado el versionado?

<!-- solution -->

Tratando la tabla como contrato, renombrar es un cambio major: publícalo como nueva versión (o columna nueva) junto a la vieja, anuncia una fecha de deprecación y quita el nombre viejo solo cuando los consumidores migren.

<!-- takeaways -->

- MAJOR.MINOR.PATCH indica cambios que rompen, agregan y corrigen.
- Los contratos de datos también merecen versiones.
- Conventional commits y tags automatizan los releases.

<!-- stage: Calidad -->

### Estrategia de pruebas para datos

<!-- unit: La pirámide de pruebas -->

<!-- goals -->

- Describir pruebas unitarias, de integración, end-to-end y smoke para pipelines.
- Estructurar el código para que la lógica sea probable unitariamente.

<!-- concept -->

Las pruebas cambian velocidad por realismo. Las unitarias revisan pequeñas piezas de lógica en milisegundos; las de integración, componentes contra dependencias reales; las end-to-end corren todo el pipeline con pocos datos; las smoke confirman que un despliegue funciona. Una suite sana tiene muchas de las primeras y pocas de las últimas.
Las pruebas unitarias solo son baratas si la lógica está separada de la I/O. Funciones que reciben y devuelven DataFrames se prueban sin clúster ni warehouse.

<!-- example -->

```python
def add_net_amount(df):                         # pure: DataFrame in, DataFrame out
    return df.withColumn("net", F.col("gross") - F.coalesce(F.col("discount"), F.lit(0)))

def test_add_net_amount(spark):
    df = spark.createDataFrame([(100, 10), (50, None)], "gross int, discount int")
    assert [r.net for r in add_net_amount(df).collect()] == [90, 50]
```

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

<!-- challenge -->

Las únicas pruebas de un pipeline corren el job completo en un clúster de staging y tardan 50 minutos. ¿Cómo rebalanceas la suite?

<!-- solution -->

Extrae la lógica de transformación a funciones puras y cúbrelas con pruebas unitarias rápidas en Spark local, deja unas pocas pruebas de integración para la I/O y corre el job end-to-end completo cada noche o antes de releases, no en cada PR.

<!-- takeaways -->

- Muchas pruebas unitarias rápidas, pocas lentas y realistas.
- Separa la lógica pura de la I/O para probarla barato.
- Las smoke tests confirman que cada despliegue funciona.

<!-- unit: Pruebas de código frente a pruebas de datos -->

<!-- goals -->

- Distinguir pruebas de lógica de pruebas de datos.
- Agregar compuertas de contrato, regresión y calidad de datos a la entrega.

<!-- concept -->

Las pruebas de código preguntan "¿la lógica hace lo que quise con entradas que elegí?". Las de datos preguntan "¿lo que llegó de verdad es lo que esperamos?". Ambas hacen falta: un código perfecto igual falla con una fuente que cambió anoche.
Las pruebas de contrato están entre equipos y verifican que un productor siga entregando el esquema acordado. Las de regresión comparan la salida de una versión nueva con la anterior. Las compuertas de calidad frenan la publicación cuando fallan las expectativas.

<!-- example -->

```yaml
# dbt data tests on the output of a model
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests: [unique, not_null]
      - name: status
        tests:
          - accepted_values: {values: [placed, shipped, returned]}
```

#### ¿Por qué preferir datos sintéticos en CI?

Son seguros (sin datos personales), pequeños (pruebas rápidas), deterministas y pueden incluir a propósito casos límite (nulos, duplicados, registros tardíos, unicode, valores extremos) que serían raros en muestras reales.

#### ¿Qué es una prueba de contrato de datos?

Una prueba que verifica que la salida de un productor cumple el esquema y la semántica acordados en un contrato de datos (columnas, tipos, nulabilidad, valores permitidos), ejecutada en el CI del productor para que los cambios que rompen fallen antes de publicarse.

#### ¿Qué son las pruebas de regresión de los pipelines de datos?

Comparar las salidas de la nueva versión con las de la anterior sobre la misma entrada (conteos de filas, agregados, diferencias fila a fila), para detectar cambios no intencionados; las herramientas incluyen `datacompy`, dbt audit helper y enfoques de data-diff.

#### ¿Qué es una prueba de humo tras el despliegue?

Un control rápido justo después de desplegar de que el sistema funciona: los jobs están registrados, una ejecución pequeña termina bien, las tablas clave se pueden leer, los dashboards cargan. Detecta pronto los errores de configuración y de permisos.

<!-- challenge -->

Un refactor de un modelo de ingresos pasa todas las pruebas unitarias. ¿Cómo verificas que no cambió los resultados?

<!-- solution -->

Haz una comparación de regresión: construye la versión nueva en un esquema de CI o staging con las mismas entradas y compara conteos, agregados y un diff por llave contra producción. Investiga cualquier diferencia antes de fusionar.

<!-- takeaways -->

- Las pruebas de código revisan lógica; las de datos, datos reales.
- Los contratos protegen a los consumidores de cambios del productor.
- Los diffs de regresión atrapan cambios no intencionales.

<!-- unit: Datos de prueba y herramientas -->

<!-- goals -->

- Manejar datos de prueba, prefiriendo fixtures sintéticos en CI.
- Usar fixtures de pytest, comparaciones de DataFrames y golden files.

<!-- concept -->

Las pruebas son tan buenas como sus entradas. Datasets sintéticos pequeños, diseñados alrededor de casos borde, son rápidos, deterministas y sin datos personales; por eso son lo estándar en CI. Las muestras parecidas a producción, enmascaradas, van en staging.
Las herramientas mantienen las pruebas cortas: los fixtures comparten preparación como una sesión de Spark, los helpers de comparación dan diffs legibles y los golden files guardan salidas esperadas para casos grandes. La velocidad importa, porque las suites lentas se saltan.

<!-- example -->

```python
import pytest
from pyspark.testing import assertDataFrameEqual

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[2]").getOrCreate()

def test_dedupe(spark):
    actual = dedupe(spark.read.json("tests/fixtures/orders_dupes.json"))
    expected = spark.read.json("tests/golden/orders_deduped.json")
    assertDataFrameEqual(actual, expected)
```

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

<!-- challenge -->

Cada prueba crea su propia SparkSession y la suite tarda 12 minutos para 80 pruebas. ¿Cuál es el arreglo más rápido?

<!-- solution -->

Compartir una SparkSession por sesión de pruebas con un fixture de pytest con scope de sesión, y bajar `spark.sql.shuffle.partitions` para datos diminutos. El costo de arranque ocurre una sola vez.

<!-- takeaways -->

- Los fixtures sintéticos son seguros, pequeños y deterministas.
- Comparte la preparación costosa con fixtures.
- Los golden files guardan salidas esperadas para casos grandes.

<!-- unit: Qué probar en un pipeline -->

<!-- goals -->

- Cubrir casos borde, idempotencia y evolución de esquema.
- Probar transformaciones SQL y DAGs de Airflow.

<!-- concept -->

Los pipelines rara vez fallan en el camino feliz. Fallan con entradas vacías, nulos en llaves, duplicados, registros tardíos, una columna nueva o una re-ejecución que agrega dos veces. Las pruebas que alimentan esos casos a propósito atrapan con anticipación la mayoría de incidentes.
Cada herramienta tiene sus puntos de entrada: los modelos SQL se construyen sobre entradas sembradas, los DAGs se cargan e inspeccionan, y la idempotencia se prueba corriendo un paso dos veces.

<!-- example -->

```python
def test_load_is_idempotent(spark, tmp_path):
    load_day(spark, "tests/fixtures/day.json", tmp_path, day="2026-10-17")
    first = spark.read.parquet(str(tmp_path)).count()
    load_day(spark, "tests/fixtures/day.json", tmp_path, day="2026-10-17")
    assert spark.read.parquet(str(tmp_path)).count() == first
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

<!-- challenge -->

Una fuente agregó una columna y el pipeline botó en silencio otra columna por un select posicional. ¿Qué prueba lo habría atrapado?

<!-- solution -->

Una prueba de evolución de esquema: alimentar un fixture con una columna extra en el medio y verificar que el esquema y los valores de salida no cambien. Luego corregir el código para seleccionar por nombre.

<!-- takeaways -->

- Prueba entradas vacías, nulas, duplicadas, tardías y cambiadas.
- Corre los pasos dos veces para demostrar idempotencia.
- Construye SQL sobre seeds; carga DAGs con `DagBag`.

<!-- unit: Técnicas avanzadas de pruebas -->

<!-- goals -->

- Usar pruebas basadas en propiedades y de mutación donde valgan la pena.
- Seguir el rendimiento sin frenar cada PR.

<!-- concept -->

Las pruebas por ejemplos solo revisan casos que alguien pensó. Las pruebas basadas en propiedades generan muchas entradas y verifican reglas que siempre deben cumplirse, como "deduplicar nunca aumenta las filas". Las pruebas de mutación evalúan las pruebas mismas: rompen el código a propósito y miran si algo falla.
El rendimiento tiene su propio ritmo: los benchmarks con volúmenes realistas son muy lentos para cada PR, pero corridos con regularidad muestran regresiones antes que los usuarios.

<!-- example -->

```python
from hypothesis import given, strategies as st

@given(st.lists(st.tuples(st.integers(1, 5), st.integers())))
def test_dedupe_never_adds_rows(rows):
    assert len(dedupe_by_key(rows)) <= len(rows)
```

#### ¿Cómo se prueba el rendimiento en CI?

Normalmente no en cada PR, sino con benchmarks periódicos sobre volúmenes representativos, siguiendo el tiempo de ejecución, el tamaño de los shuffles y el costo, y alertando ante regresiones; las reglas de lint pueden detectar barato los antipatrones de rendimiento conocidos.

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

<!-- challenge -->

Un equipo tiene 95 % de cobertura y aun así siguen llegando bugs a producción. ¿Cómo ayudarían las pruebas de mutación?

<!-- solution -->

Muestran si las pruebas de verdad revisan el comportamiento: si los mutantes (condiciones invertidas, constantes cambiadas) sobreviven, esas pruebas ejecutan código sin verificar lo correcto. Refuerza las aserciones donde sobreviven mutantes.

<!-- takeaways -->

- Las pruebas de propiedades revisan invariantes con entradas generadas.
- Las pruebas de mutación miden qué tan fuertes son las pruebas.
- Mide el rendimiento con un calendario, no por PR.

### Calidad del código y controles estáticos

<!-- unit: Linters y formato -->

<!-- goals -->

- Configurar linters, formateadores y chequeo de tipos para código de datos.
- Correrlos temprano con pre-commit y reglas propias.

<!-- concept -->

Los chequeos estáticos encuentran problemas sin ejecutar nada. Los formateadores acaban las discusiones de estilo; los linters atrapan bugs y malos patrones; los chequeadores de tipos encuentran argumentos equivocados y manejo de `None`. Correrlos en cada commit mantiene las revisiones enfocadas en la lógica.
A los equipos de datos también les sirven reglas propias: un chequeo que marque `collect()` sobre DataFrames grandes o `SELECT *` en modelos codifica lecciones aprendidas a las malas.

<!-- example -->

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks: [{id: ruff, args: [--fix]}, {id: ruff-format}]
  - repo: https://github.com/sqlfluff/sqlfluff
    rev: 3.2.0
    hooks: [{id: sqlfluff-lint}]
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.0
    hooks: [{id: gitleaks}]
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

<!-- challenge -->

Las revisiones de código siempre terminan en debates sobre estilo de SQL. ¿Qué introduces?

<!-- solution -->

Un formateador y linter de SQL (SQLFluff) con una configuración acordada, corriendo en pre-commit y exigido en CI. El estilo se vuelve automático y las revisiones se enfocan en la lógica.

<!-- takeaways -->

- Formateadores, linters y tipos atrapan problemas temprano.
- Pre-commit los corre antes de que el código salga del portátil.
- Las reglas propias codifican lecciones del equipo.

<!-- unit: Chequeos más allá del estilo -->

<!-- goals -->

- Agregar análisis de seguridad y cobertura a CI.
- Validar proyectos dbt, YAML y archivos de workflow.

<!-- concept -->

El análisis estático también cubre seguridad y estructura. Los escáneres de seguridad señalan código riesgoso y definiciones de infraestructura inseguras. La cobertura muestra zonas sin probar, como señal y no como meta.
La configuración merece chequeos tanto como el código: los proyectos dbt se pueden parsear y evaluar contra convenciones, el YAML validar contra esquemas y los archivos de workflow de CI pasar por un linter antes de correr.

<!-- example -->

```yaml
- run: dbt deps && dbt parse
- run: sqlfluff lint models/
- run: checkov -d infra/
- run: actionlint
- run: pytest --cov=src --cov-report=xml
```

#### ¿Por qué añadir anotaciones de tipo al código de datos?

Documentan las interfaces, permiten que los verificadores de tipos detecten errores (tipos de argumentos equivocados, manejo de `None`) antes de ejecutar y mejoran el soporte del IDE, lo que importa en las librerías compartidas por muchos pipelines.

#### ¿Qué es el dbt project evaluator?

Un paquete de dbt que revisa un proyecto contra buenas prácticas (nombres de modelos, capas, referencias directas a fuentes desde los marts, pruebas o documentación faltantes, patrones de fan-out) y puede hacer fallar el CI ante incumplimientos.

#### ¿Cómo se revisan los archivos YAML y de configuración?

Con validación de esquema (JSON Schema para las configuraciones, `databricks bundle validate`, `actionlint` para los workflows de GitHub), yamllint para la sintaxis y el estilo, y pruebas que cargan todos los archivos de configuración que usa el pipeline.

#### ¿Qué es actionlint?

Un verificador estático de los archivos de workflow de GitHub Actions que detecta errores de sintaxis, expresiones inválidas, entradas desconocidas y problemas en los scripts de shell antes de que corran los workflows.

#### ¿Qué entornos necesita una plataforma de datos?

Al menos desarrollo (sandboxes individuales o compartidos), un entorno de staging o preproducción que refleje producción, y producción. Algunos añaden entornos de pruebas/QA o entornos efímeros por pull request.

#### ¿Por qué separar los entornos por cuenta, workspace o catálogo?

El aislamiento limita el alcance de los errores, permite permisos distintos (los desarrolladores no pueden escribir en producción), separa los costos y hace explícita la promoción.

<!-- challenge -->

Un gerente quiere exigir 90 % de cobertura en todos los PRs. ¿Qué le aconsejas?

<!-- solution -->

Usar la cobertura para encontrar código crítico sin probar y evitar caídas grandes, no como meta rígida: un número alto con aserciones débiles da falsa tranquilidad. Exigir pruebas para la lógica nueva y revisar su calidad.

<!-- takeaways -->

- Los escáneres de seguridad revisan código e infraestructura.
- La cobertura es una señal, no una meta.
- Valida dbt, YAML y workflows en CI.

<!-- stage: Plataforma -->

### Entornos y configuración

<!-- unit: Ambientes y aislamiento -->

<!-- goals -->

- Definir los ambientes que necesita una plataforma de datos y cómo aislarlos.
- Promover artefactos entre ambientes con nombres consistentes.

<!-- concept -->

Los ambientes dan a los cambios un camino seguro a producción. Desarrollo es para construir, staging para comprobar, producción para los consumidores. El aislamiento, por cuenta, workspace o catálogo, evita que un error en uno llegue a los otros y permite permisos distintos.
La paridad le da sentido a staging: entre más se parezca a producción, más significa una prueba aprobada. Y la promoción mueve el mismo artefacto por cada ambiente en lugar de reconstruirlo.

<!-- example -->

```text
dev:     catalog dev_sales,  workspace dev,  role developer (read prod)
staging: catalog stg_sales,  workspace stg,  role ci-deployer
prod:    catalog sales,      workspace prod, role prod-deployer (no humans)
artifact etl-2.4.1.whl  ──► dev ──► staging ──► prod
```

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

<!-- challenge -->

Staging usa otra versión de Spark y clústeres más pequeños que producción, y siguen apareciendo bugs solo en producción. ¿Qué cambias?

<!-- solution -->

Alinear staging con producción: mismas versiones de runtime, configuración y código de infraestructura, con tamaños menores solo donde no cambien el comportamiento. Despliega ambos desde el mismo IaC con variables por ambiente.

<!-- takeaways -->

- Dev, staging y prod dan a los cambios un camino seguro.
- Aísla ambientes por cuenta, workspace o catálogo.
- Paridad y promoción hacen confiables los resultados de staging.

<!-- unit: Configuración por ambiente -->

<!-- goals -->

- Sacar la configuración del código con variables y archivos por ambiente.
- Usar ambientes efímeros para los pull requests.

<!-- concept -->

El mismo artefacto debe correr en todas partes, así que lo que cambia entre ambientes, como rutas, catálogos, tamaños y endpoints, sale de la configuración, no del código. La regla twelve-factor la pone en el ambiente, con los secretos en un gestor de secretos.
Los ambientes efímeros llevan la idea más lejos: cada pull request recibe su propio esquema o workspace de corta vida, creado y destruido automáticamente, para que las pruebas nunca choquen.

<!-- example -->

```yaml
# databricks.yml targets
targets:
  dev:     {variables: {catalog: dev_sales,  workers: 2}}
  staging: {variables: {catalog: stg_sales,  workers: 4}}
  prod:    {variables: {catalog: sales,      workers: 16}}
```

#### ¿Qué es el versionado de datos y por qué sirve en CI/CD?

Versionar los datasets como el código (ramas de lakeFS, Project Nessie para Iceberg, snapshots de Delta e Iceberg, snapshots de dbt) para reproducir ejecuciones, probar cambios sobre ramas aisladas de los datos y revertir escrituras malas.

#### ¿Qué es el patrón write-audit-publish (WAP)?

Escribir los datos nuevos en una ubicación o rama de staging, auditarlos con controles de calidad y solo entonces publicarlos (swap, merge o fast-forward), para que los consumidores nunca vean datos malos. Las ramas de Iceberg, lakeFS y los intercambios de tablas lo implementan.

#### ¿Cómo se nombran los recursos entre entornos?

Con un esquema coherente que incluya el entorno (`sales_prod`, `catalog_dev`, `dbt_ci_pr_123`), derivado de la configuración y no escrito en el código, para que el código nunca apunte por accidente a producción desde dev.

<!-- challenge -->

Dos PRs corren CI al mismo tiempo y sus pruebas se sobrescriben las tablas en un esquema de CI compartido. ¿Qué cambias?

<!-- solution -->

Dar a cada PR su propio esquema (por ejemplo `ci_pr_123`), creado al inicio de la ejecución y eliminado al cerrar el PR, con el nombre pasado como configuración.

<!-- takeaways -->

- La configuración varía; el artefacto no.
- Config en el ambiente, secretos en un vault.
- Los ambientes efímeros aíslan cada PR.

<!-- unit: Datos fuera de producción -->

<!-- goals -->

- Dar datos realistas y seguros a staging y desarrollo.
- Usar versionado de datos y write-audit-publish.

<!-- concept -->

El código se copia libremente entre ambientes; los datos no. Staging necesita datos parecidos a producción para atrapar problemas reales, pero copiar datos personales a todas partes es un riesgo. La respuesta usual es clonar o muestrear con enmascaramiento, y acceso de solo lectura a producción para desarrollo donde la política lo permita.
El versionado de datos y write-audit-publish llevan ideas de CI a los datos: escribe los datos nuevos en una rama o área de staging, revísalos y publícalos de forma atómica.

<!-- example -->

```text
write:   INSERT INTO sales.orders_staging  (or Iceberg branch "audit")
audit:   row counts, uniqueness, freshness, reconciliation
publish: swap/fast-forward into sales.orders only if checks pass
```

#### ¿Cómo trabajan los desarrolladores sin tocar los datos de producción?

Con esquemas o catálogos personales, targets de desarrollo que leen de producción en solo lectura (o de clones) y escriben solo en dev, datos muestreados o enmascarados, y permisos que impiden escribir en producción con las identidades de los desarrolladores.

#### ¿Qué es la promoción entre entornos?

Mover el mismo artefacto de dev a staging y a producción tras pasar los controles de cada etapa, en lugar de reconstruirlo, con aprobaciones para producción.

#### ¿Debe staging usar datos de producción?

Lo ideal es que staging use datos parecidos a los de producción (clonados, muestreados o enmascarados) para detectar problemas del mundo real, con controles estrictos sobre los datos personales; un staging puramente sintético puede no ver problemas que solo revelan los datos reales.

#### ¿Qué es la infraestructura como código (IaC)?

Definir los recursos de la nube (almacenamiento, cómputo, redes, permisos, catálogos, jobs) en código declarativo que se versiona, se revisa y se aplica automáticamente, en lugar de crearlos a mano en las consolas.

#### ¿Qué herramientas de IaC son comunes en las plataformas de datos?

Terraform/OpenTofu (multinube), AWS CloudFormation, CDK y SAM, Azure Bicep, Pulumi, y herramientas propias de cada plataforma como los Databricks Asset Bundles, el provider de Terraform de Snowflake y los manifiestos de Kubernetes con Helm.

<!-- challenge -->

Una carga nocturna publicó una vez medio día de datos en los dashboards antes de fallar, y los directivos vieron cifras erróneas. ¿Qué patrón lo evita?

<!-- solution -->

Write-audit-publish: cargar en una tabla o rama de staging, correr chequeos de calidad y publicar con un swap atómico solo si pasan, para que los consumidores vean los datos viejos o los nuevos completos.

<!-- takeaways -->

- Staging necesita datos parecidos a producción y enmascarados.
- Desarrollo lee producción en solo lectura o trabaja con muestras.
- WAP publica datos solo después de pasar los chequeos.

### Infraestructura como código

<!-- unit: Declarar la infraestructura -->

<!-- goals -->

- Explicar la infraestructura como código y sus herramientas principales.
- Estructurar IaC para varios ambientes, incluidos los permisos.

<!-- concept -->

Crear recursos a punta de clics no deja registro ni se puede repetir. La infraestructura como código declara buckets, clústeres, catálogos, jobs y permisos en archivos, así los ambientes se construyen siempre igual y los cambios pasan por revisión.
Una buena estructura lo hace manejable: módulos reutilizables para piezas comunes, variables por ambiente y reemplazo inmutable en lugar de parchar recursos en sitio. Los permisos también van en código, porque son lo que más rápido se desvía.

<!-- example -->

```hcl
module "lake" {
  source      = "./modules/lake"
  environment = var.environment          # dev, staging, prod
  buckets     = ["raw", "curated"]
}

resource "databricks_grants" "sales" {
  catalog = "sales"
  grant { principal = "analysts"  privileges = ["USE_CATALOG", "SELECT"] }
}
```

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

<!-- challenge -->

Los permisos del warehouse se otorgaron a mano durante años y nadie sabe quién tiene acceso a qué. ¿Cómo pasas a código?

<!-- solution -->

Exporta los grants actuales, modélalos como roles en IaC, revisa y quita lo innecesario, importa los objetos existentes al state y desde ahí cambia grants solo con pull requests. Detecta el drift con un calendario.

<!-- takeaways -->

- IaC hace la infraestructura revisable y repetible.
- Módulos más variables por ambiente la mantienen manejable.
- Los permisos también van en código.

<!-- unit: Plan, state y drift -->

<!-- goals -->

- Revisar cambios de infraestructura con plan y apply.
- Manejar el state, detectar drift y aplicar políticas.

<!-- concept -->

Las herramientas de IaC comparan lo que declara el código con lo que existe, registrado en el state, y calculan un plan. Revisar ese plan es la principal medida de seguridad: muestra qué se creará, cambiará o destruirá antes de que pase.
El state se guarda remoto y con bloqueo, y los cambios manuales generan drift que el siguiente apply puede revertir. La política como código agrega reglas automáticas a la revisión humana, como prohibir buckets públicos o borrar recursos protegidos.

<!-- example -->

```hcl
resource "aws_s3_bucket" "raw" {
  bucket = "acme-lake-raw-prod"
  lifecycle { prevent_destroy = true }
}
```
```bash
terraform plan -out=tfplan && terraform show -no-color tfplan > plan.txt   # posted to the PR
```

#### ¿Cómo se revisan con seguridad los cambios de infraestructura?

Publicando el `terraform plan` (o el diff de CDK, el change set de CloudFormation) como comentario del pull request, exigiendo revisiones de los responsables de los recursos afectados, usando controles de políticas (Checkov, OPA/Conftest, Sentinel) y aplicando solo desde CI.

#### ¿Qué es la política como código?

Escribir las reglas de la organización (cifrado obligatorio, sin buckets públicos, etiquetas obligatorias, regiones aprobadas) como código evaluado automáticamente en CI o al desplegar, por ejemplo con Open Policy Agent, Checkov o los servicios de políticas nativos de la nube.

#### ¿Cómo se administran los permisos de la plataforma de datos como código?

Definiendo los roles, permisos y permisos del catálogo en Terraform o en las herramientas de la plataforma (provider de Snowflake, provider de Terraform de Databricks, permisos de Unity Catalog en los bundles), revisados en pull requests, para que los cambios de acceso sean auditables y reversibles.

#### ¿Qué es un artefacto de compilación en los proyectos de datos?

La salida versionada de una compilación que se despliega: un wheel de Python con el código del pipeline, una imagen Docker, un JAR, un manifiesto de dbt compilado, un bundle o un zip de scripts SQL. Se construye una vez y se despliega el mismo artefacto en todas partes.

#### ¿Por qué "construir una vez, desplegar muchas"?

Reconstruir para cada entorno puede producir artefactos distintos (cambios de dependencias, el momento de la compilación), así que lo probado no es lo desplegado. Construir un artefacto y promoverlo garantiza la coherencia.

#### ¿Cómo se versionan los artefactos?

Con versiones semánticas para las librerías, y SHA de commit o números de compilación para las aplicaciones (`0.2.145+g1a2b3c4`), estampados al compilar para que cada despliegue se pueda rastrear hasta un commit.

<!-- challenge -->

Alguien cambió el tamaño de un clúster de producción en la consola. ¿Qué pasa en el siguiente apply de Terraform y cuál debería ser el proceso?

<!-- solution -->

Terraform ve el drift y devuelve el tamaño al valor del código. El cambio debió hacerse en código con un PR; corre `terraform plan` programado para detectar drift y alertar.

<!-- takeaways -->

- Revisa el plan antes de cada apply.
- Mantén el state remoto y con bloqueo.
- Detecta drift; aplica reglas con política como código.

### Empaquetado y artefactos

<!-- unit: Artefactos y versiones -->

<!-- goals -->

- Construir artefactos versionados una vez y desplegarlos en todas partes.
- Guardar artefactos en registros y estampar versiones en CI.

<!-- concept -->

Un artefacto es exactamente lo que se despliega: un wheel, una imagen, un proyecto dbt compilado. Construirlo una vez y promover los mismos bytes por cada ambiente garantiza que lo probado es lo que corre en producción.
Las versiones atan los artefactos al código fuente: versiones semánticas para librerías, SHAs de commit para aplicaciones, ambas derivadas automáticamente en CI. Los registros las guardan para redesplegar cualquier versión.

<!-- example -->

```bash
python -m build                                   # version from setuptools-scm: 2.4.1
twine upload --repository codeartifact dist/*
docker build -t $ECR/etl:$(git rev-parse --short HEAD) . && docker push $ECR/etl:$(git rev-parse --short HEAD)
```

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

<!-- challenge -->

Producción se comporta distinto de staging aunque "el código es el mismo". Cada ambiente reconstruye la imagen al desplegar. ¿Por qué es un problema?

<!-- solution -->

Cada reconstrucción puede traer otras versiones de dependencias o imágenes base, así que staging y prod corren artefactos distintos. Construye la imagen una vez en CI, etiquétala con el SHA del commit y despliega ese mismo tag en todas partes.

<!-- takeaways -->

- Los artefactos son las unidades desplegables.
- Construye una vez; promueve el mismo artefacto.
- Versiona desde Git y guarda en registros.

<!-- unit: Dependencias y contenedores -->

<!-- goals -->

- Hacer reproducibles las dependencias de Python con lock files.
- Empaquetar con contenedores y escanearlos con SBOMs.

<!-- concept -->

Las dependencias sin fijar hacen que los builds se desvíen: el mismo código instala otras librerías el mes siguiente. Los lock files fijan versiones exactas, incluidas las transitivas, para que un build sea reproducible.
Los contenedores extienden eso a todo el runtime, incluidas las librerías del sistema operativo. El costo es responder por lo que hay adentro: las imágenes base traen vulnerabilidades, así que se escanean y un SBOM registra cada componente.

<!-- example -->

```dockerfile
FROM python:3.12.7-slim
COPY uv.lock pyproject.toml ./
RUN pip install uv && uv sync --frozen --no-dev
COPY src/ ./src/
```
```bash
trivy image --severity HIGH,CRITICAL --exit-code 1 $ECR/etl:abc123
```

#### ¿Por qué escanear las imágenes de contenedor en CI?

Las imágenes base y las dependencias contienen vulnerabilidades conocidas; los escáneres (Trivy, Grype, el escaneo del registro) las encuentran antes del despliegue, y las políticas pueden bloquear los problemas críticos.

#### ¿Qué estrategias de despliegue existen?

Recreate (detener lo viejo, iniciar lo nuevo), rolling (reemplazar instancias poco a poco), blue-green (cambiar el tráfico entre dos entornos completos), canary (enviar primero una pequeña parte a la nueva versión), shadow (ejecutar la nueva versión en paralelo sin servir sus resultados) y feature flags (desplegar apagado y activar después).

#### ¿Cómo se aplica el despliegue blue-green a los datos?

Construyendo la nueva versión de las tablas o pipelines junto a las actuales (nuevo esquema, versión de tabla o clon), validándola y luego cambiando a los consumidores de forma atómica (intercambio de vistas, renombrado de tablas, puntero del catálogo), conservando la versión vieja para revertir rápido.

#### ¿Qué es un canary release para los pipelines de datos?

Ejecutar la nueva versión sobre un subconjunto (un país, una partición, una muestra de clientes) o en paralelo con la vieja, comparar salidas y métricas, y ampliarla cuando haya confianza.

<!-- challenge -->

Un job nocturno se rompió porque una dependencia sacó una versión major durante la noche. Nada cambió en el repo. ¿Qué cambias?

<!-- solution -->

Fija todas las dependencias con un lock file e instala desde él (`--frozen`), y deja que Dependabot o Renovate propongan actualizaciones como PRs que pasen por CI.

<!-- takeaways -->

- Los lock files hacen reproducibles las instalaciones.
- Los contenedores fijan todo el runtime.
- Escanea imágenes y mantén SBOMs.

<!-- stage: Entrega -->

### Estrategias de despliegue

<!-- unit: Estrategias para código y datos -->

<!-- goals -->

- Aplicar despliegues blue-green, canary y shadow a pipelines.
- Usar feature flags para controlar lógica nueva.

<!-- concept -->

Las estrategias de despliegue reducen el riesgo de un cambio limitando quién lo ve hasta que esté probado. En datos, las mismas ideas aplican a tablas: construir la versión nueva junto a la vieja y cambiar (blue-green), correrla primero sobre una porción (canary) o correrla con entradas reales sin que los consumidores la vean (shadow).
Los feature flags dan el mismo control dentro del código: la lógica nueva se despliega pero queda apagada hasta que alguien la active.

<!-- example -->

```sql
-- blue-green for a table: build v2, validate, then switch the view consumers use
CREATE TABLE marts.revenue_v2 AS SELECT ...;
-- validation queries comparing v1 and v2 ...
CREATE OR REPLACE VIEW marts.revenue AS SELECT * FROM marts.revenue_v2;
```

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

<!-- challenge -->

Un nuevo modelo de atribución va a cambiar las cifras de marketing. ¿Cómo lo liberas sin sorprender al negocio?

<!-- solution -->

Córrelo en modo shadow unas semanas, escribiendo en tablas separadas, y compara con el modelo actual. Comparte las diferencias con los interesados y cambia con un flag o una vista en una fecha acordada.

<!-- takeaways -->

- Blue-green, canary y shadow limitan la exposición.
- En datos, construye tablas nuevas junto a las viejas.
- Los feature flags separan desplegar de activar.

<!-- unit: Cambios de esquema -->

<!-- goals -->

- Hacer cambios de esquema sin romper código en ejecución ni consumidores.
- Usar expand-and-contract y herramientas de migración.

<!-- concept -->

Los cambios de esquema son lo más riesgoso de los despliegues de datos: los jobs en curso esperan la forma vieja, los consumidores leen la tabla directamente y algunos cambios bloquean tablas o son difíciles de deshacer. Hacerlos en un solo paso obliga a que todos los lectores y escritores cambien al mismo tiempo.
Expand-and-contract divide el cambio: agrega la forma nueva, migra escritores y lectores, y luego quita la vieja. Las herramientas de migración aplican cambios ordenados y registrados para que todos los ambientes queden iguales.

<!-- example -->

```text
1. expand:   ADD COLUMN gross_amount; write both amount and gross_amount
2. migrate:  backfill gross_amount; move readers to gross_amount
3. contract: stop writing amount; DROP COLUMN amount (after deprecation date)
```

#### ¿Qué son las herramientas de migración de bases de datos?

Herramientas que aplican cambios de esquema versionados y ordenados y llevan registro de cuáles se ejecutaron: Flyway, Liquibase, Alembic (SQLAlchemy), Sqitch, schemachange (Snowflake) y dbt para los objetos que administra la transformación.

#### ¿Cómo se manejan los backfills en los despliegues?

Como parte del plan de publicación: estimar costo y duración, parametrizar los pipelines por rango de fechas, ejecutar en lotes controlados (a menudo fuera de horas pico), validar las salidas y avisar a los consumidores cuando cambian datos históricos.

#### ¿Cómo se despliega un cambio en una tabla muy usada sin interrupción?

Construyendo la nueva versión en paralelo (tabla o versión nueva), validándola, cambiando luego de forma atómica (swap, renombrado o actualización de una vista) y conservando la versión vieja para revertir; evita reescribir en su lugar mientras los consumidores leen.

#### ¿Cómo se despliega un cambio que exige recalcular el historial?

Planificando un backfill: desplegar la nueva lógica escribiendo en una tabla o versión nueva, recalcular el historial por lotes, validar frente a las salidas viejas, cambiar a los consumidores y comunicar las cifras reexpresadas, en lugar de sobrescribir el historial en su lugar sin controles.

<!-- challenge -->

Debes renombrar `cust_id` a `customer_id` en una tabla que leen 12 dashboards. Planéalo.

<!-- solution -->

Agrega `customer_id` y llénalo junto con `cust_id` (o exponlo con una vista), anuncia la deprecación, migra los dashboards, monitorea que ya nadie consulte `cust_id` y luego bórralo.

<!-- takeaways -->

- Los cambios de esquema rompen código en curso y consumidores.
- Expande, migra y luego contrae.
- Las herramientas de migración mantienen esquemas consistentes entre ambientes.

<!-- unit: Rollbacks, backfills y congelamientos -->

<!-- goals -->

- Revertir código y datos después de un mal despliegue.
- Planear backfills, congelamientos y despliegues de streaming.

<!-- concept -->

Revertir código es fácil: redespliegas el artefacto anterior. Revertir datos no: las tablas ya contienen lo que escribió la versión mala. Los planes necesitan ambos, con time travel, snapshots o una re-ejecución de la lógica anterior.
Los cambios que exigen recalcular la historia son despliegues con costo y calendario. Los congelamientos protegen periodos críticos, y los jobs de streaming agregan estado que debe sobrevivir a la actualización.

<!-- example -->

```sql
-- data rollback on Delta / Iceberg after a bad deploy at 09:40
RESTORE TABLE marts.revenue TO TIMESTAMP AS OF '2026-10-17 09:30:00';
```

#### ¿Qué es un congelamiento de despliegues y cuándo es apropiado?

Un periodo sin despliegues a producción, por ejemplo durante el cierre contable o los picos de ventas, para reducir el riesgo; es mejor hacer los despliegues seguros y rutinarios, y mantener los congelamientos cortos y solo para periodos de alto riesgo real.

#### ¿Cómo se despliegan los cambios de jobs de streaming?

Revisando la compatibilidad del estado, deteniendo el job de forma ordenada (savepoint o checkpoint), desplegando la nueva versión desde el mismo checkpoint si es compatible, o iniciando un job nuevo con un checkpoint nuevo y un plan de backfill; en los streams críticos, ejecutando la versión vieja y la nueva en paralelo.

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

<!-- challenge -->

Un cambio de lógica exige recalcular tres años de una tabla de 4 TB. ¿Cómo lo despliegas sin afectar a los consumidores?

<!-- solution -->

Despliega la lógica nueva escribiendo en una nueva versión de la tabla, haz el backfill por lotes con concurrencia limitada y un estimado de costo, valida contra la tabla vieja, cambia a los consumidores de forma atómica (vista o swap) y conserva la versión vieja un tiempo.

<!-- takeaways -->

- Planea el rollback de datos, no solo el de código.
- Los backfills son releases con costo y calendario.
- Los despliegues de streaming deben preservar el estado.

### GitHub Actions a fondo

<!-- unit: Workflows, jobs y triggers -->

<!-- goals -->

- Leer y escribir workflows de GitHub Actions con jobs y steps.
- Elegir triggers, incluidos calendarios, filtros de rutas e inputs manuales.

<!-- concept -->

Un workflow es un archivo YAML que dice cuándo correr y qué hacer. Los triggers deciden el cuándo: pushes, pull requests, calendarios, ejecuciones manuales con inputs. Los jobs corren en paralelo en máquinas separadas salvo que dependan entre sí; los steps corren en orden dentro de un job.
Los filtros de rutas mantienen enfocados los workflows, para que un cambio de documentación no corra la suite de pruebas de Spark.

<!-- example -->

```yaml
name: ci
on:
  pull_request:
    paths: ["src/**", "tests/**", "pyproject.toml"]
  workflow_dispatch:
    inputs:
      start_date: {description: "First date to backfill (YYYY-MM-DD)", required: true}
permissions: {contents: read}
jobs:
  test:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12", cache: pip}
      - run: pip install -e .[dev] && pytest -q
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

<!-- challenge -->

Un monorepo tiene modelos dbt y jobs de Python, y cada PR corre ambas suites (30 minutos). ¿Cómo lo aceleras?

<!-- solution -->

Divide en dos workflows (o jobs) con filtros de rutas: los chequeos de dbt corren con cambios en `models/` y las pruebas de Python en `src/` y `tests/`. Archivos compartidos como la config de CI disparan ambos.

<!-- takeaways -->

- Los workflows definen triggers; los jobs corren en paralelo; los steps en orden.
- Los filtros de rutas corren solo los chequeos relevantes.
- `workflow_dispatch` agrega ejecuciones manuales con inputs.

<!-- unit: Runners, caché y artefactos -->

<!-- goals -->

- Elegir runners y fijar sus imágenes.
- Acelerar jobs con caché y matrices, y pasar archivos y valores entre jobs.

<!-- concept -->

Cada job corre en un runner nuevo, lo que es seguro pero olvida todo entre ejecuciones. La caché restaura dependencias para no instalar desde cero; los artefactos llevan archivos de un job a otro; los outputs llevan valores pequeños. Las matrices corren el mismo job en varias versiones en paralelo.
Los runners mismos son una decisión: las imágenes hospedadas cambian con el tiempo, así que fijar una versión evita roturas sorpresa, y hay runners más grandes o self-hosted para trabajo pesado.

<!-- example -->

```yaml
jobs:
  build:
    runs-on: ubuntu-24.04
    outputs: {version: "${{ steps.v.outputs.version }}"}
    steps:
      - uses: actions/checkout@v4
      - id: v
        run: echo "version=$(git describe --tags)" >> "$GITHUB_OUTPUT"
      - run: python -m build
      - uses: actions/upload-artifact@v4
        with: {name: dist, path: dist/}
  deploy:
    needs: build
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/download-artifact@v4
        with: {name: dist}
      - run: echo "deploying ${{ needs.build.outputs.version }}"
```

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

<!-- challenge -->

El job de deploy reconstruye el wheel que el job de pruebas ya construyó, y a veces despliega una versión un poco distinta. Arréglalo.

<!-- solution -->

Construye una vez en un job de build, sube el wheel como artefacto, corre las pruebas contra él y haz que el job de deploy descargue ese mismo artefacto (y el output de versión) en lugar de reconstruir.

<!-- takeaways -->

- Los runners arrancan limpios; caché y artefactos trasladan cosas.
- Los outputs pasan valores pequeños entre jobs.
- Fija las imágenes de runner; usa runners grandes o self-hosted para trabajo pesado.

<!-- unit: Secretos, ambientes y OIDC -->

<!-- goals -->

- Guardar secretos y variables de forma segura, también en repositorios públicos.
- Desplegar con ambientes, aprobaciones y OIDC en lugar de llaves de larga vida.

<!-- concept -->

Los workflows necesitan credenciales, y cómo se las das decide tu exposición. Los secretos están cifrados y se enmascaran en los logs; las variables no, así que en repositorios públicos todo lo identificable va en secretos. Los ambientes limitan los secretos a un destino y pueden exigir aprobación antes de que corra un job.
OIDC elimina por completo las llaves de nube guardadas: el workflow prueba su identidad con un token de corta vida y el rol de nube confía solo en repositorios, ramas o ambientes específicos. El `GITHUB_TOKEN` debe tener los permisos mínimos.

<!-- example -->

```yaml
permissions: {id-token: write, contents: read}
jobs:
  deploy:
    environment: production          # required reviewers, prod-only secrets
    runs-on: ubuntu-24.04
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_DEPLOY_ROLE_ARN }}
          aws-region: eu-west-1
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

<!-- challenge -->

Un repositorio guarda como secreto una access key de AWS con permisos de admin para los despliegues. ¿Con qué la reemplazas?

<!-- solution -->

Un rol de IAM asumido con GitHub OIDC, con una trust policy limitada a este repositorio y al ambiente de producción (claim `sub`), y permisos limitados a lo que necesita el despliegue. Luego borra la access key.

<!-- takeaways -->

- Los secretos se enmascaran; las variables son visibles.
- Los ambientes limitan secretos y agregan aprobaciones.
- OIDC reemplaza llaves guardadas por tokens de corta vida.

<!-- unit: Control de flujo y reutilización -->

<!-- goals -->

- Controlar cuándo corren los jobs con condiciones, concurrencia y timeouts.
- Reutilizar lógica con reusable workflows y composite actions.

<!-- concept -->

Cuando los pipelines crecen aparecen dos necesidades: decidir con precisión cuándo corre algo y no copiar el mismo YAML en diez repositorios. Las condiciones usan expresiones sobre contextos como la rama o el evento; la concurrencia evita que dos despliegues compitan; los timeouts evitan que jobs colgados quemen minutos.
La reutilización viene en dos tamaños: las composite actions agrupan steps y los reusable workflows agrupan jobs completos que otros workflows llaman.

<!-- example -->

```yaml
concurrency: {group: deploy-prod, cancel-in-progress: false}
jobs:
  tests:
    uses: ./.github/workflows/ci.yml
  deploy:
    needs: tests
    if: github.ref == 'refs/heads/main' && github.event_name == 'push' && vars.DEPLOY_AWS == 'true'
    timeout-minutes: 30
    runs-on: ubuntu-24.04
    steps:
      - uses: ./.github/actions/setup-project      # composite action
      - run: make deploy
```

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

<!-- challenge -->

Dos merges con un minuto de diferencia arrancan dos despliegues a producción que corren a la vez y dejan las definiciones de jobs en un estado mezclado. ¿Qué agregas?

<!-- solution -->

Un grupo de `concurrency` para los despliegues a producción sin `cancel-in-progress` (para que hagan fila en vez de solaparse), más un timeout para que un despliegue trabado no bloquee la fila para siempre.

<!-- takeaways -->

- Condiciones y contextos deciden cuándo corren los jobs.
- Los grupos de concurrencia evitan despliegues en competencia.
- Reutiliza con composite actions y reusable workflows.

<!-- unit: Seguridad, feedback y ecosistema -->

<!-- goals -->

- Proteger los workflows de código no confiable y dependencias cambiantes.
- Dar feedback claro a los revisores y mantener las dependencias al día.

<!-- concept -->

Los workflows ejecutan código, a veces de desconocidos. Las acciones de terceros pueden cambiar bajo un tag, y los triggers que corren con secretos sobre pull requests de forks se pueden abusar. Fijar acciones a commits y elegir bien los triggers cierra esas brechas; las merge queues aseguran que lo que llega a main se probó con main.
Un buen feedback hace que la gente siga usando CI: reportes de pruebas, resúmenes y comentarios en PRs ponen los resultados donde se miran. Los bots de dependencias y otros sistemas de CI siguen las mismas ideas.

<!-- example -->

```yaml
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683   # v4.2.2, pinned
- run: |
    echo "### dbt build" >> "$GITHUB_STEP_SUMMARY"
    echo "| models | tests | failures |" >> "$GITHUB_STEP_SUMMARY"
    echo "| 42 | 180 | 0 |" >> "$GITHUB_STEP_SUMMARY"
- run: gh pr comment "$PR" --body-file plan.txt
  env: {GH_TOKEN: "${{ github.token }}", PR: "${{ github.event.number }}"}
```

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

<!-- challenge -->

Un workflow usa `pull_request_target` y hace checkout del código del PR para correr pruebas con secretos de despliegue disponibles. ¿Cuál es el riesgo y qué haces?

<!-- solution -->

El PR de un fork puede cambiar el código de pruebas para exfiltrar secretos, porque `pull_request_target` corre con secretos. Usa `pull_request` para código no confiable (sin secretos) y deja los jobs con secretos para ramas confiables o después de aprobación.

<!-- takeaways -->

- Fija acciones a SHAs; cuidado con `pull_request_target`.
- Las merge queues prueban los cambios contra el main más reciente.
- Resúmenes, reportes y comentarios hacen visibles los resultados de CI.

### CI/CD para dbt

<!-- unit: CI de dbt -->

<!-- goals -->

- Construir un pipeline de CI para dbt con slim CI y defer.
- Aislar las ejecuciones de CI y sacar la configuración de conexión del código.

<!-- concept -->

Construir todos los modelos dbt en cada PR se vuelve lento y caro a medida que crecen los proyectos. Slim CI construye solo lo que cambió y lo que depende de ello, comparando con el manifest de producción. Defer llena los huecos leyendo de producción los modelos upstream sin cambios en lugar de reconstruirlos.
Cada PR escribe en su propio esquema, y el profile lee todos los datos de conexión de variables de ambiente, así el mismo proyecto corre en CI y en producción sin editarlo.

<!-- example -->

```bash
dbt deps
sqlfluff lint models/
dbt build --select state:modified+ --defer --state prod-artifacts/ --target ci
# profiles.yml: schema: "dbt_ci_pr_{{ env_var('PR_NUMBER') }}", password: "{{ env_var('DBT_PASSWORD') }}"
```

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

<!-- challenge -->

Slim CI falla porque un modelo modificado referencia un modelo upstream que no existe en el esquema de CI. ¿Qué falta?

<!-- solution -->

`--defer` con el manifest de producción (`--state`), para que las referencias a modelos sin cambios resuelvan a relaciones de producción. Otra opción: hacer `dbt clone` de los modelos upstream necesarios al esquema de CI primero.

<!-- takeaways -->

- Slim CI construye los modelos modificados y sus hijos.
- Defer lee los padres sin cambios desde producción.
- Un esquema por PR; credenciales desde variables de ambiente.

<!-- unit: Desplegar dbt con seguridad -->

<!-- goals -->

- Desplegar dbt a producción con pruebas, frescura y docs.
- Proteger a los consumidores con unit tests, contratos y versiones.

<!-- concept -->

Las ejecuciones de dbt en producción construyen modelos y corren pruebas en orden de dependencia, así una prueba fallida frena que datos malos fluyan aguas abajo. Los chequeos de frescura de fuentes aseguran primero que las entradas estén al día, y los docs se regeneran con cada release.
La seguridad de los consumidores viene de tres funciones: los unit tests revisan la lógica sobre filas simuladas, los contratos imponen nombres y tipos de columnas, y las versiones dejan que un cambio que rompe conviva con la forma vieja hasta que los consumidores migren.

<!-- example -->

```yaml
models:
  - name: fct_orders
    config: {contract: {enforced: true}}
    columns:
      - {name: order_id, data_type: bigint, constraints: [{type: not_null}]}
      - {name: gross_amount, data_type: numeric(12,2)}
unit_tests:
  - name: test_refunds_are_negative
    model: fct_orders
    given: [{input: ref('stg_orders'), rows: [{order_id: 1, type: refund, amount: 10}]}]
    expect: {rows: [{order_id: 1, gross_amount: -10}]}
```

#### ¿Para qué sirve el comando "clone" de dbt en CI?

`dbt clone` crea clones zero-copy (o vistas) de las relaciones de producción en el esquema de CI o de desarrollo, para que los modelos incrementales y las pruebas posteriores corran sobre un estado realista a bajo costo.

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

<!-- challenge -->

Un PR cambia el tipo de una columna en un modelo que usa una herramienta de BI, y el dashboard se rompe tras el despliegue. ¿Qué lo habría frenado?

<!-- solution -->

Un contrato de modelo exigido: CI fallaría al cambiar el tipo de la columna. Para un cambio intencional, publica una nueva versión del modelo y deja que los consumidores migren antes de quitar la vieja.

<!-- takeaways -->

- `dbt build` corre modelos y pruebas en orden.
- La frescura protege las entradas; los docs salen con cada release.
- Unit tests, contratos y versiones protegen a los consumidores.

### CI/CD para Databricks, Airflow y warehouses

<!-- unit: Databricks -->

<!-- goals -->

- Configurar CI/CD para Databricks con Asset Bundles y service principals.
- Probar, desplegar y correr jobs desde CI sin que los equipos choquen.

<!-- concept -->

Los Databricks Asset Bundles describen jobs, pipelines y su configuración en archivos junto al código, con targets por ambiente. CI los valida y prueba; CD los despliega como un service principal, así producción nunca depende de la cuenta de una persona.
Los bundles también resuelven el ownership: cada bundle tiene un nombre y una ruta de despliegue, así dos equipos que despliegan en un mismo workspace no se sobrescriben los jobs.

<!-- example -->

```bash
databricks bundle validate -t staging
pytest tests/unit
databricks bundle deploy -t staging          # as the staging service principal
databricks bundle run -t staging smoke_test_job
databricks bundle deploy -t prod             # after approval
```

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

<!-- challenge -->

Los jobs de producción fallan después de que se fue de la empresa el ingeniero que los creó. ¿Qué salió mal y cómo lo arreglas?

<!-- solution -->

Los jobs corrían con la identidad de esa persona, que se desactivó. Redespliégalos con bundles usando un service principal como owner e identidad run-as, con los permisos otorgados al principal, no a personas.

<!-- takeaways -->

- Los bundles mantienen los recursos de Databricks en código con targets.
- Despliega y corre como service principals.
- Nombres y rutas distintos de bundle evitan choques.

<!-- unit: Airflow, Glue y warehouses -->

<!-- goals -->

- Desplegar DAGs de Airflow y jobs de Glue con CI/CD.
- Manejar cambios de Snowflake y BigQuery como código.

<!-- concept -->

Cada plataforma tiene su mecánica de despliegue, pero el patrón se repite: probar en CI, construir un artefacto versionado, desplegarlo con infraestructura como código y dejar los secretos fuera del artefacto. En Airflow es una imagen con DAGs; en Glue, scripts y wheels en rutas versionadas de S3; en warehouses, objetos repartidos entre IaC para lo de nivel de cuenta y herramientas de migración o dbt para los esquemas.
Configuración y secretos siguen la misma regla en todas partes: configuración del ambiente, secretos de un gestor.

<!-- example -->

| Plataforma | Artefacto | Se despliega con |
|---|---|---|
| Airflow | Imagen con DAGs y providers fijados | Helm / sync de S3 en MWAA |
| Glue | Script + wheel en `s3://artifacts/<sha>/` | Terraform / CDK |
| Snowflake | Roles, warehouses; esquemas | Terraform; dbt o schemachange |
| BigQuery | Release de Dataform | Release configurations |

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

<!-- challenge -->

Las conexiones de Airflow se crean a mano en la UI de cada ambiente, y staging apunta a producción por error. ¿Qué cambias?

<!-- solution -->

Define las conexiones por ambiente en un secrets backend (o variables de ambiente) manejado como código, con nombres iguales entre ambientes y valores distintos. Quita las conexiones creadas en la UI.

<!-- takeaways -->

- El mismo patrón en todas partes: probar, construir, desplegar como código.
- Versiona los artefactos por commit.
- Configuración del ambiente, secretos de un gestor.

<!-- unit: Probar contra servicios de nube -->

<!-- goals -->

- Probar código que depende de servicios de nube sin acceso a producción.
- Usar service containers para pruebas de integración.

<!-- concept -->

El código que llama a S3, Glue o una base de datos es difícil de probar en CI sin tocar sistemas reales. Las capas ayudan: simula el servicio en pruebas unitarias, usa equivalentes locales como LocalStack o un contenedor de PostgreSQL para integración, y deja unas pocas pruebas contra una cuenta sandbox real.
Los service containers en CI levantan esas dependencias junto al job, así las pruebas de integración corren en cada PR sin nada que limpiar.

<!-- example -->

```yaml
jobs:
  integration:
    runs-on: ubuntu-24.04
    services:
      postgres:
        image: postgres:16
        env: {POSTGRES_PASSWORD: test}
        ports: ["5432:5432"]
        options: --health-cmd "pg_isready" --health-interval 5s
    steps:
      - uses: actions/checkout@v4
      - run: pytest tests/integration --db-url postgresql://postgres:test@localhost:5432/postgres
```

#### ¿Cómo se protege producción de despliegues no autorizados?

Con protección de la rama main, revisiones obligatorias, reglas de protección del entorno con aprobadores, políticas de confianza OIDC restringidas al entorno de producción y logs de auditoría de los despliegues.

#### ¿Cómo se manejan los datos sensibles en los logs de CI?

No imprimiendo nunca secretos ni datos reales; confiando en el enmascarado pero sin fiarse del todo; usando datos sintéticos en las pruebas; revisando los logs de los repositorios públicos; y limitando la retención de los logs.

<!-- challenge -->

Las pruebas de integración escriben en un bucket S3 real de una cuenta dev compartida y a veces se borran archivos entre sí. ¿Qué cambias?

<!-- solution -->

Usa moto o LocalStack para la mayoría de pruebas de S3, y para las pocas con el servicio real, un prefijo único por ejecución de CI con limpieza automática (y una regla de lifecycle de respaldo).

<!-- takeaways -->

- Simula en pruebas unitarias; usa equivalentes locales para integración.
- Los service containers corren dependencias junto al job.
- Aísla por ejecución las pruebas con servicios reales.

<!-- stage: Operar con seguridad -->

### Seguridad de la cadena de entrega

<!-- unit: Secretos y filtraciones -->

<!-- goals -->

- Identificar los principales riesgos de seguridad de CI/CD.
- Escanear secretos y responder cuando uno se filtra.

<!-- concept -->

Un pipeline de entrega tiene las llaves de producción, y eso lo vuelve un objetivo. La falla más común es simple: un secreto en el código, el historial o los logs. El escaneo atrapa la mayoría antes de que salgan del portátil.
Cuando uno se filtra igual, sacarlo de Git no basta, porque ya puede haber copias. Primero revoca y rota, luego limpia y verifica si se usó.

<!-- example -->

```bash
gitleaks detect --source . --log-opts="--all"     # scan the full history
# leaked key? 1) revoke/rotate  2) check CloudTrail for use  3) purge history  4) add a pre-commit hook
```

#### ¿Por qué son riesgosos los runners propios y cómo se aseguran?

Ejecutan código arbitrario de los workflows dentro de tu red; un PR malicioso podría atacar sistemas internos. Usa runners efímeros (un job por runner), nunca ejecutes en ellos código de forks no confiables, aísla las redes y restringe qué repositorios pueden usarlos.

#### ¿Qué es un ataque de "poisoned pipeline execution"?

Un atacante modifica en un pull request la configuración del CI o archivos que ejecuta el CI (scripts, Makefiles) para que el pipeline ejecute código malicioso con acceso a los secretos. Se mitiga con tokens de mínimo privilegio, sin secretos para los PR no confiables y con revisiones obligatorias de los cambios del CI.

#### ¿Cómo se protege la propia configuración del CI?

Exigiendo la revisión de los code owners para `.github/workflows/`, restringiendo quién puede modificar los entornos y los secretos, fijando las acciones y auditando los cambios de los workflows.

#### ¿Qué debe pasar después de un despliegue?

Pruebas de humo, monitoreo de las ejecuciones de los jobs y de los controles de calidad en la siguiente ejecución, comparación de las métricas clave con las ejecuciones anteriores y notificaciones al equipo; revertir rápido si fallan los controles.

<!-- challenge -->

Un desarrollador subió una contraseña de base de datos a una rama e hizo force-push para quitarla una hora después. ¿Está cerrado el asunto?

<!-- solution -->

No. Asume que está comprometida: rota la contraseña, revisa los logs de la base por accesos y verifica si forks, cachés o logs de CI la capturaron. Agrega escaneo de secretos en pre-commit y push protection.

<!-- takeaways -->

- Los secretos filtrados son el riesgo de CI/CD más común.
- Escanea código e historial de forma continua.
- Rota primero; borrar el commit no basta.

<!-- unit: Cadena de suministro y mínimo privilegio -->

<!-- goals -->

- Aplicar mínimo privilegio y controles de cadena de suministro a CI/CD.
- Proteger la configuración de CI y los runners del abuso.

<!-- concept -->

Todo en lo que confía el pipeline puede ser una entrada: dependencias, acciones de terceros, runners y la configuración de CI misma. Los ataques de poisoned pipeline cambian archivos que CI ejecuta, así un pull request malicioso puede correr código con los permisos del pipeline.
El mínimo privilegio limita el daño: tokens de solo lectura por defecto, permisos de despliegue solo en los jobs de deploy, producción alcanzable solo desde ramas protegidas con aprobaciones. Los runners self-hosted necesitan aislamiento extra porque viven dentro de tu red.

<!-- example -->

```text
default GITHUB_TOKEN:       contents: read
deploy job:                 id-token: write, environment: production (approvers)
cloud role trust:           repo:acme/lake:environment:production only
.github/workflows/**:       CODEOWNERS = platform team
self-hosted runners:        ephemeral, no access from fork PRs
```

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

<!-- challenge -->

Cualquier desarrollador puede editar archivos de workflow, y el rol del job de deploy puede desplegar a producción desde cualquier rama. Nombra tres controles para agregar.

<!-- solution -->

Revisión de CODEOWNERS para `.github/workflows/`, una trust policy de OIDC restringida al ambiente de producción en main, y protección del ambiente con revisores obligatorios. Tokens por defecto de solo lectura.

<!-- takeaways -->

- Dependencias, acciones, runners y config de CI son superficie de ataque.
- Mínimo privilegio por job y por ambiente.
- Protege los archivos de workflow con code owners.

### Operación, monitoreo y DataOps

<!-- unit: Después del despliegue -->

<!-- goals -->

- Verificar que un despliegue no rompió los datos.
- Correlacionar incidentes con despliegues y practicar fallas.

<!-- concept -->

Un pipeline en verde solo dice que el código se desplegó. Si los datos siguen bien se ve después: en los chequeos de calidad de la siguiente ejecución, la frescura, los volúmenes y los dashboards que usa la gente. Mirar esas señales tras cada despliegue cierra el ciclo.
Cuando algo se rompe, un log de despliegues responde la primera pregunta, qué cambió, y el chaos testing en staging muestra cómo se comportan los pipelines ante fallas antes de que pase de verdad.

<!-- example -->

```text
deploy 14:02  etl v2.4.1 (PR #318, approved by @ana)
14:05  smoke test: job registered, 1-day run OK
06:10  next run: row count -38% vs 7-day avg  ← alert
→ diff v2.4.0..v2.4.1 shows a changed join in orders_enriched
```

#### ¿Cómo se controlan los costos del CI?

Cancelando las ejecuciones superadas, evitando ejecutar jobs pesados en cada commit, cacheando dependencias, usando slim CI contra los warehouses, borrando automáticamente los esquemas de CI, definiendo timeouts en los jobs y vigilando los minutos y el gasto de warehouse por repositorio.

#### ¿Qué es un registro de despliegues y por qué conservarlo?

Un registro de qué versión se desplegó dónde y cuándo, por quién y con qué aprobaciones (despliegues de GitHub, historial de los entornos, notas de publicación), esencial para relacionar los incidentes con los cambios.

#### ¿Cómo se relaciona un incidente de datos con un despliegue?

Comparando la hora de inicio del incidente con el historial de despliegues, revisando qué modelos o jobs cambiaron (diff de Git entre versiones), revisando el linaje de las tablas afectadas y mirando las métricas de calidad antes y después.

#### ¿Qué son las pruebas de caos para los pipelines de datos?

Introducir fallos a propósito en un entorno de pruebas (jobs matados, archivos faltantes, fuentes retrasadas, cambios de esquema) para verificar que los reintentos, las alertas, la idempotencia y los procedimientos de recuperación funcionan como se espera.

#### Diseña un pipeline de CI/CD para un proyecto dbt sobre Snowflake.

En los pull requests: linting con SQLFluff, `dbt deps`, `dbt build --select state:modified+ --defer` contra un esquema propio del PR con un usuario de servicio de CI, publicación de los resultados y borrado del esquema al final. Al fusionar: despliegue disparando el job de producción (orquestador o dbt Cloud), guardado de los artefactos para la siguiente comparación y publicación de la documentación. Los warehouses y roles se administran con Terraform en el mismo pipeline o en uno aparte.

<!-- challenge -->

Los ingresos cayeron 20 % en un dashboard esta mañana. ¿Cómo verificas si lo causó un despliegue?

<!-- solution -->

Compara la hora de inicio de la caída con el log de despliegues, lista los modelos y jobs que cambiaron en esos despliegues (diff de Git), revisa el linaje desde ellos hasta el modelo de ingresos y corre la versión anterior con las mismas entradas para comparar.

<!-- takeaways -->

- Vigila la calidad de los datos tras cada despliegue.
- Un log de despliegues responde "¿qué cambió?".
- Practica fallas en staging con chaos tests.

<!-- unit: Releases y comunicación -->

<!-- goals -->

- Documentar releases y comunicar cambios de datos a los consumidores.
- Aplicar GitOps y medir el éxito de la entrega.

<!-- concept -->

Los consumidores no leen tus pull requests, así que los cambios deben llegarles en sus términos: qué cambia, cuándo y qué deben hacer. Changelogs, notas de release y avisos de deprecación con fechas lo logran, generados desde los mensajes de commit cuando se pueda.
GitOps hace de Git el registro de lo que debe estar desplegado, con agentes que lo aplican. El éxito no se mide solo en frecuencia de despliegue, sino en menos incidentes y recuperación más rápida.

<!-- example -->

```markdown
## Release 3.0.0 – 2026-10-20
- **Breaking:** `fct_orders.amount` renamed to `gross_amount`. Old name available until 2026-11-30.
- Added `refund_amount` (nullable).
- Fixed: test customers excluded from revenue.
```

#### Diseña el CI/CD de un lakehouse PySpark en Databricks y AWS.

CI en los pull requests: escaneo de secretos, Ruff y reglas de lint propias para Spark, pruebas unitarias con Spark local y Delta, prueba de extremo a extremo con datos sintéticos y validación del bundle. CD en main: reutilizar el CI como barrera (workflow reutilizable) y luego desplegar la ingesta en AWS (SAM o Terraform) mediante OIDC y el bundle de Databricks como service principal, ambos en un entorno de producción protegido con concurrency configurado para que los despliegues nunca se solapen.

#### Un despliegue rompió una tabla de producción. ¿Qué debió detectar tu proceso y cómo te recuperas?

Primero recupero: revierto el código, restauro la tabla con viaje en el tiempo o vuelvo a ejecutar la lógica vieja en las particiones afectadas, e informo a los consumidores. Después mejoro el pipeline: añado una prueba del caso que falló, un control de contrato o de esquema, una comparación de regresión en CI, o write-audit-publish para que los datos malos no se expongan.

#### Tu CI tarda 45 minutos y los desarrolladores se lo saltan. ¿Qué haces?

Perfilo el pipeline, paralelizo los jobs independientes, cacheo las dependencias, ejecuto solo las pruebas afectadas (filtros de rutas, slim CI), reduzco los datos de prueba, paso las pruebas de extremo a extremo lentas a la merge queue o a main, y fijo una meta (por ejemplo menos de 10 minutos para los controles de los PR).

#### Los logs de los workflows de un repositorio público muestran el nombre de host de una base de datos. ¿Qué cambias?

Paso el nombre de host y los demás valores identificativos a secretos del entorno para que se enmascaren, roto las credenciales si apareció algo sensible, reviso los logs anteriores y añado un control que impida imprimir la configuración en los logs.

<!-- challenge -->

Los analistas siguen llevándose sorpresas con cambios de columnas. ¿Qué proceso liviano introduces?

<!-- solution -->

Genera un changelog desde conventional commits en cada release, publícalo en el catálogo de datos y en un canal que sigan los analistas, y anuncia los cambios que rompen con un periodo de deprecación antes de quitarlos.

<!-- takeaways -->

- Changelogs y notas traducen los cambios para los consumidores.
- Las deprecaciones necesitan fechas y alternativas.
- Mide velocidad y estabilidad de la entrega.

<!-- unit: CI rápido y económico -->

<!-- goals -->

- Mantener CI rápido a medida que crece un proyecto.
- Controlar los costos de CI sin quitar chequeos.

<!-- concept -->

CI solo funciona si la gente lo usa. Cuando tarda demasiado, los desarrolladores agrupan cambios, se saltan chequeos o fusionan por fuera, y la red de seguridad desaparece. La velocidad viene de hacer menos trabajo por ejecución: solo lo que cambió, en paralelo, con dependencias en caché.
Los mismos movimientos bajan el costo, junto con cancelar ejecuciones reemplazadas y dejar los jobs pesados para merges o calendarios.

<!-- example -->

```yaml
concurrency: {group: "ci-${{ github.ref }}", cancel-in-progress: true}
jobs:
  unit:   {runs-on: ubuntu-24.04, steps: [...]}        # every PR
  dbt:    {if: "contains(needs.changes.outputs.paths, 'models')", ...}
  e2e:    {if: "github.event_name == 'schedule'", ...}  # nightly only
```

#### ¿Cómo migrarías de despliegues manuales a CI/CD?

Llevando todo a Git (código, configuración, infraestructura), añadiendo CI con linting y pruebas en los pull requests, automatizando el despliegue a un entorno de staging, añadiendo pruebas de humo y aprobaciones, luego automatizando el despliegue a producción con los mismos artefactos y retirando poco a poco el acceso manual a producción.

#### ¿Cómo le explicas el CI/CD de datos a una persona no técnica?

Es una línea automática de control de calidad y de entrega para nuestros pipelines de datos: cada cambio se prueba antes de que pueda afectar los reportes, y los cambios aprobados llegan a producción de la misma forma segura cada vez, para que las cifras sigan siendo confiables mientras las mejoramos rápido.

#### ¿Cómo añadirías controles de calidad de datos a un pipeline de CI/CD existente?

Añadiendo pruebas de datos al proyecto de transformación (unicidad, no nulos, relaciones, valores aceptados), ejecutándolas en CI con datos de prueba y en producción tras cada construcción, bloqueando la publicación (write-audit-publish o fallando el job) ante fallos críticos y alertando a los responsables.

<!-- challenge -->

Los costos de CI se duplicaron cuando creció el equipo. La mayoría de minutos vienen de ejecuciones sobre commits que se vuelven a subir minutos después. ¿Qué cambias primero?

<!-- solution -->

Agrega un grupo de `concurrency` por rama con `cancel-in-progress: true`, para que los pushes nuevos cancelen la ejecución vieja. Luego cachea dependencias y corre las suites pesadas solo cuando cambien las rutas relevantes.

<!-- takeaways -->

- Un CI lento se esquiva; la velocidad es seguridad.
- Corre solo lo que cambió, en paralelo, con caché.
- Cancela ejecuciones reemplazadas para ahorrar.

<!-- stage: Juntarlo todo -->

### Escenarios

<!-- unit: Recuperarse de un mal despliegue -->

<!-- goals -->

- Recuperar una tabla de producción tras un mal despliegue.
- Identificar qué brechas del proceso dejaron pasar el cambio.

<!-- concept -->

Las preguntas de incidentes evalúan dos cosas: si restauras el servicio con calma y si aprendes de ello. Primero la recuperación: revertir el código, restaurar o recalcular los datos, avisar a los consumidores. Luego la revisión mira el pipeline: qué prueba, revisión o compuerta debió frenar esto y cómo agregarla. Las revisiones sin culpables se enfocan en el sistema, no en la persona.

<!-- example -->

```text
1. Stop the bleeding: pause downstream jobs, notify consumers
2. Roll back code (previous artifact); restore table (time travel) or rerun old logic
3. Verify: row counts, key metrics vs before the deploy
4. Review: missing regression test? missing data test? review skipped?
5. Add the check to CI; document in the postmortem
```

#### Dos equipos despliegan en el mismo workspace de Databricks y se sobrescriben los jobs. ¿Cómo lo corriges?

Usando bundles con nombres y targets distintos por equipo, desplegando con el service principal de cada equipo con permisos limitados a sus recursos, usando el modo de desarrollo para los despliegues personales y separando los despliegues de producción por repositorio y protecciones de entorno.

<!-- challenge -->

El postmortem muestra que el bug se habría atrapado comparando las salidas antes y después del cambio. ¿Cómo haces esa comparación parte de cada PR relevante?

<!-- solution -->

Agrega a CI un paso de regresión para los modelos cambiados: constrúyelos en el esquema del PR con las mismas entradas y compara agregados clave y conteos contra producción, publicando el resultado como comentario del PR y fallando ante diferencias inesperadas.

<!-- takeaways -->

- Primero recupera: código, datos, comunicación.
- Busca la compuerta que faltó, no a quién culpar.
- Convierte cada lección en un chequeo automático.

<!-- unit: Pasar de entregas manuales a automatizadas -->

<!-- goals -->

- Planear una migración de despliegues manuales a CI/CD.
- Ordenar los pasos para que el valor llegue pronto.

<!-- concept -->

Los equipos rara vez pasan de despliegues manuales a CI/CD completo en un paso, y no deberían intentarlo. El camino es incremental: primero todo a Git, luego chequeos que corran en cada cambio, después despliegue automático a un ambiente no productivo y por último a producción con aprobaciones. Cada paso vale por sí solo y genera confianza para el siguiente.

<!-- example -->

| Paso | Resultado |
|---|---|
| 1. Todo en Git | Historial, revisiones, ningún script perdido |
| 2. CI: lint + pruebas unitarias | Menos cambios rotos |
| 3. Despliegue automático a staging | Despliegues repetibles |
| 4. Despliegue a prod con aprobación | Nada de copiar a mano, rastro de auditoría |
| 5. Pruebas de datos y monitoreo | Problemas atrapados antes que los usuarios |

#### Un `terraform apply` en CI borró un recurso de producción. ¿Cómo evitas que vuelva a pasar?

Exigiendo la revisión del plan antes del apply, añadiendo reglas de ciclo de vida `prevent_destroy` en los recursos críticos, ejecutando controles de políticas que bloqueen el borrado de recursos protegidos, separando el estado y los permisos por entorno, y, de inmediato, restaurando desde los respaldos o volviendo a importar el recurso.

<!-- challenge -->

Algunos ingenieros temen que la automatización los frene. ¿Cómo muestras valor en las primeras dos semanas?

<!-- solution -->

Empieza por lo que hoy les quita tiempo: pon los scripts en Git con un CI básico que corra linting y unas pruebas en minutos, y automatiza un despliegue doloroso. Muestra el tiempo ahorrado y el primer bug que atrapó CI.

<!-- takeaways -->

- Migra por pasos: Git, CI, despliegues a staging, despliegues a prod.
- Cada paso debe valer por sí solo.
- Muestra logros tempranos para generar confianza.
