## CI/CD y automatización para datos: lo que importa, con ejemplos de GitHub Actions

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![CI/CD y automatización para pipelines de datos](../../images/cicd_automation_for_data_title_img.png)

*Artículo técnico*

## Por qué los equipos de datos necesitan CI/CD

Hace diez años, desplegar un pipeline de datos solía significar copiar un script a un servidor, editar una línea de cron y cruzar los dedos. He visto arreglos de emergencia escritos directamente en producción, jobs que funcionaban en un entorno y no en otro, y lunes por la mañana dedicados a averiguar cuál de los cambios del viernes rompió los dashboards. Nada de eso es un problema de herramientas. Es lo que pasa cuando los cambios llegan a producción sin un camino repetible y automatizado.

CI/CD le da a cada cambio el mismo camino: se versiona, se revisa, se prueba automáticamente, lo despliega una máquina con los mismos pasos cada vez y queda trazable después. Para los equipos de datos trae los mismos beneficios que para los equipos de aplicaciones (menos incidentes, entregas más rápidas, reversiones fáciles), pero los datos añaden consideraciones propias. Este artículo cubre lo que creo que más importa y luego muestra workflows concretos de GitHub Actions, varios tomados de los pipelines detrás de este sitio y de mi [lakehouse de registros mercantiles europeos](../projects/eu-company-registry.html).

## Qué hace distinto el CI/CD de datos

Cuatro diferencias condicionan todo lo demás:

1. **Los pipelines tienen estado.** Desplegar código nuevo no reemplaza las tablas que escribió. Un cambio de esquema necesita una migración; un cambio de lógica puede necesitar un backfill; un despliegue malo puede exigir restaurar datos, no solo revertir el código.
2. **La corrección depende de los datos, no solo del código.** Las pruebas con datos de prueba demuestran la lógica. Solo los controles de calidad sobre datos reales demuestran que el archivo del mes que viene es sensato. El CI/CD tiene que incluir ambas cosas.
3. **Los despliegues pueden salir caros.** Un cambio en un modelo central puede disparar el recálculo completo de años de historial. El costo y el momento forman parte del plan de publicación.
4. **Intervienen varios sistemas.** Una plataforma de datos típica abarca un repositorio de código, una cuenta en la nube, una plataforma de cómputo (Databricks, Snowflake, Glue) y un orquestador. Cada uno necesita credenciales, y ninguno debería guardar los secretos de otro.

## Las consideraciones que importan

### Versionarlo todo

El código, los modelos SQL, las definiciones de orquestación (DAG, Databricks Asset Bundles, especificaciones de jobs), la infraestructura (Terraform, CloudFormation, SAM), los permisos, las reglas de calidad de datos y los workflows de CI van en Git. Si algo solo se puede cambiar haciendo clic en una consola, no se puede revisar, probar ni revertir. Los datos reales y los secretos son las dos cosas que nunca entran.

### Probar por capas, y que las capas rápidas sean de verdad rápidas

El linting y las pruebas unitarias deben correr en segundos; una ejecución de extremo a extremo con datos sintéticos, en minutos; los controles de calidad en producción, en cada ejecución. Si los controles de un pull request tardan 45 minutos, los desarrolladores encontrarán cómo saltárselos. Escribí en detalle sobre las capas de pruebas en [Pruebas y rendimiento en pipelines de big data](testing_and_performance_big_data.html).

### Separar entornos y promover el mismo artefacto

Al menos desarrollo, un entorno de staging o preproducción y producción, idealmente en cuentas, workspaces o catálogos separados, para que un error en dev no pueda tocar los datos de producción. Se construye una vez (un wheel, una imagen, un bundle), se estampa con el commit y se promueve ese mismo artefacto. La configuración cambia por entorno; el código no.

### Identidad, no claves

La mayor mejora de seguridad en CI/CD de los últimos años es la **federación de identidades de carga de trabajo (OIDC)**. En lugar de guardar claves de acceso a la nube de larga duración como secretos del repositorio, el workflow pide a GitHub un token de corta duración y lo intercambia por credenciales temporales de un rol que solo confía en ese repositorio y ese entorno. Nada que filtrar, nada que rotar. Databricks, Snowflake (par de claves u OAuth) y las grandes nubes admiten identidades de máquina; despliega como service principal, nunca como una persona.

### Hacer que los despliegues se puedan repetir sin riesgo

Los despliegues se reintentan, se vuelven a ejecutar y a veces se disparan dos veces. La infraestructura como código es declarativa (aplicarla dos veces no cambia nada), los bundles y jobs se actualizan en su lugar, y los propios pipelines deben ser idempotentes (`MERGE` o sobrescritura por partición, nunca appends a ciegas). Nunca dejes que dos despliegues al mismo entorno corran a la vez.

### Planificar los cambios de datos, no solo los de código

En cada pull request, pregúntate: ¿cambia esto un esquema del que dependen los consumidores? ¿Exige reprocesar el historial? Usa cambios de esquema compatibles hacia atrás (añadir, migrar y luego quitar: *expand and contract*), contratos de datos verificados en CI, modelos versionados para los cambios que rompen y un plan de backfill explícito con su costo y su momento. El patrón write-audit-publish (escribir los datos nuevos en una ubicación de staging, revisarlos y luego intercambiarlos) mantiene los datos malos lejos de los consumidores.

### Poner una barrera antes de producción, pero ligera

Una aprobación obligatoria antes de producción es un seguro barato en las plataformas de datos, donde un despliegue malo puede corromper tablas que leen los consumidores. Mantén automático todo lo anterior a la barrera, para que la aprobación sea un vistazo rápido a un pipeline en verde y no una lista de verificación manual.

### Vigilar lo que pasa después del despliegue

El CI/CD no termina en "el despliegue terminó bien". Las pruebas de humo, los resultados de calidad de la siguiente ejecución, el monitoreo de frescura y volumen, y las alertas de duración te dicen si el cambio funciona de verdad con datos reales.

### Cuidado con los repositorios públicos

Si el repositorio es público, también lo son los logs de sus workflows. GitHub enmascara los secretos en los logs, pero no las variables normales. Los nombres de host, nombres de buckets, IDs de cuenta y correos deberían guardarse como **secretos** de un entorno protegido, aunque no sean contraseñas, para que nunca aparezcan en un log público. Escanea en CI todo el historial en busca de secretos, no solo los commits nuevos.

## GitHub Actions en cinco minutos

Los workflows son archivos YAML en `.github/workflows/`. Cada workflow se dispara con eventos (`push`, `pull_request`, `schedule`, `workflow_dispatch` para ejecuciones manuales, `workflow_call` para que otros workflows lo reutilicen) y contiene **jobs** que corren en máquinas virtuales nuevas (runners). Los jobs corren en paralelo salvo que uno `needs` otro; cada job es una lista de **steps** que ejecutan comandos de shell o **acciones** reutilizables. Los **entornos** (por ejemplo `production`) tienen sus propios secretos y variables y pueden exigir revisores antes de que empiece un job dirigido a ellos. Con eso basta para leer los ejemplos.

## Ejemplo 1: CI para un proyecto PySpark

Esta es la forma del CI en el repositorio de mi lakehouse. Corre en cada pull request y se reutiliza como primera etapa del workflow de despliegue:

```yaml
name: ci

on:
  pull_request:
  workflow_call:      # cd.yml lo ejecuta como barrera antes de cualquier despliegue
  workflow_dispatch:

permissions:
  contents: read      # mínimo privilegio por defecto

jobs:
  checks:
    runs-on: ubuntu-24.04
    timeout-minutes: 40
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0              # historial completo, para el escaneo de secretos

      - name: Escaneo de secretos (todo el historial)
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip

      - uses: actions/setup-java@v4   # Spark necesita una JVM
        with:
          distribution: temurin
          java-version: "17"

      - name: Instalar
        run: pip install -e ".[local,dev]"

      - name: Lint (ruff + antipatrones de PySpark + datos sensibles)
        run: |
          ruff check src tests tools
          python tools/spark_lint.py src
          git ls-files | xargs python tools/check_sensitive.py

      - name: Pruebas unitarias
        run: pytest tests -m "not e2e" --cov=registry_lakehouse --cov-report=term-missing

      - name: Pipeline de extremo a extremo con datos sintéticos
        run: pytest tests -m e2e
```

Algunas decisiones que vale la pena destacar:

- **`permissions: contents: read`** arriba: el `GITHUB_TOKEN` generado automáticamente tiene acceso de solo lectura salvo que un job pida más de forma explícita.
- **El escaneo de secretos lee todo el historial**, porque una clave subida y luego borrada sigue estando en el repositorio.
- **Las reglas de lint propias** codifican lecciones aprendidas: nada de `collect()` sobre datos sin acotar, nada de UDF de Python, nada que se rompa en el serverless de Databricks, nada de rutas de bucket escritas en el código.
- **Las pruebas unitarias y la ejecución de extremo a extremo son pasos separados**, así un fallo te dice de inmediato qué capa se rompió.
- **`workflow_call`** permite que el workflow de despliegue reutilice exactamente este archivo en lugar de duplicarlo.

## Ejemplo 2: despliegue continuo en AWS y Databricks

El workflow de despliegue corre en cada push a `main`. Reutiliza el CI como barrera y luego despliega dos sistemas independientes, cada uno solo tras una aprobación manual en el entorno `production`:

```yaml
# push a main ──► ci (todas las pruebas) ──► [aprobación de producción] ──► ingesta en AWS (SAM)
#                                                                    └──► job de Databricks (bundle)
name: cd

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      run_job:
        description: Iniciar una ejecución de producción justo después de desplegar
        type: boolean
        default: false

concurrency:
  group: deploy-production
  cancel-in-progress: false      # nunca interrumpir un despliegue a medias

permissions:
  contents: read

jobs:
  tests:
    uses: ./.github/workflows/ci.yml

  aws:
    needs: tests
    if: vars.DEPLOY_AWS == 'true'          # se activa cuando existe la configuración de AWS
    runs-on: ubuntu-24.04
    environment: production
    permissions:
      contents: read
      id-token: write                      # permite GitHub OIDC -> rol de AWS
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/setup-sam@v2
        with:
          use-installer: true
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_DEPLOY_ROLE_ARN }}
          aws-region: ${{ vars.AWS_REGION }}
      - name: Construir y desplegar
        run: |
          sam build -t infra/template.yaml
          sam deploy --stack-name eu-registry-ingestion --resolve-s3 \
            --capabilities CAPABILITY_IAM \
            --no-confirm-changeset --no-fail-on-empty-changeset \
            --parameter-overrides "BucketName=${{ secrets.LANDING_BUCKET }}"

  databricks:
    needs: tests
    if: vars.DEPLOY_DATABRICKS == 'true'
    runs-on: ubuntu-24.04
    environment: production
    env:
      DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
      DATABRICKS_CLIENT_ID: ${{ secrets.DATABRICKS_CLIENT_ID }}
      DATABRICKS_CLIENT_SECRET: ${{ secrets.DATABRICKS_CLIENT_SECRET }}
    steps:
      - uses: actions/checkout@v4
      - uses: databricks/setup-cli@main      # fija un SHA de commit en producción
      - name: Estampar una versión única del wheel
        run: python tools/set_version.py "0.2.${{ github.run_number }}+g${GITHUB_SHA::7}"
      - name: Validar contra el workspace
        run: databricks bundle validate -t prod --strict
      - name: Desplegar
        run: databricks bundle deploy -t prod
      - name: Iniciar una ejecución (opcional)
        if: github.event_name == 'workflow_dispatch' && inputs.run_job
        run: databricks bundle run -t prod registry_lakehouse --no-wait
```

Lo que este workflow hace bien, y por qué:

- **El CI es la barrera.** `uses: ./.github/workflows/ci.yml` ejecuta las mismas pruebas que los pull requests; nada se despliega si fallan.
- **`concurrency` con `cancel-in-progress: false`** pone en cola los despliegues en lugar de correr dos a la vez o matar uno a medias.
- **No hay claves de AWS en ningún lado.** `id-token: write` permite al job pedir un token OIDC; `configure-aws-credentials` lo intercambia por un rol de corta duración. La política de confianza del rol solo acepta tokens del entorno `production` de este repositorio.
- **Databricks se despliega como service principal** con OAuth máquina a máquina. El bundle define como código el job, su programación, sus alertas y sus permisos.
- **Cada artefacto es trazable.** La versión del wheel contiene el número de ejecución y el SHA corto del commit.
- **Las variables del repositorio controlan cada despliegue** (`vars.DEPLOY_AWS == 'true'`), así el workflow sigue en verde mientras un entorno de destino todavía no está configurado.
- **Los valores identificativos son secretos**, porque el repositorio es público y solo los secretos se enmascaran en los logs.
- **Iniciar una ejecución de producción es una decisión aparte y manual** mediante las entradas de `workflow_dispatch`.

Del lado de AWS, la política de confianza del rol es lo que hace seguro el OIDC. Lo importante es la condición sobre el subject del token:

```json
{
  "Effect": "Allow",
  "Principal": { "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com" },
  "Action": "sts:AssumeRoleWithWebIdentity",
  "Condition": {
    "StringEquals": {
      "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
      "token.actions.githubusercontent.com:sub": "repo:my-org/my-repo:environment:production"
    }
  }
}
```

## Ejemplo 3: slim CI para dbt

En un proyecto dbt, reconstruirlo todo en cada pull request es lento y caro. El slim CI construye solo los modelos que modificó el pull request, más todo lo que depende de ellos, en un esquema único por pull request, resolviendo hacia producción las referencias que no cambiaron:

```yaml
name: dbt-ci
on:
  pull_request:
    paths: ["models/**", "macros/**", "seeds/**", "dbt_project.yml", "packages.yml"]

permissions:
  contents: read
  id-token: write

concurrency:
  group: dbt-ci-${{ github.event.pull_request.number }}
  cancel-in-progress: true          # un push nuevo reemplaza la ejecución anterior

jobs:
  build:
    runs-on: ubuntu-24.04
    environment: ci
    env:
      DBT_TARGET_SCHEMA: dbt_ci_pr_${{ github.event.pull_request.number }}
      SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
      SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_CI_USER }}
      SNOWFLAKE_PRIVATE_KEY: ${{ secrets.SNOWFLAKE_CI_PRIVATE_KEY }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -r requirements.txt
      - run: dbt deps
      - name: Lint de SQL
        run: sqlfluff lint models
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.ARTIFACTS_READ_ROLE_ARN }}
          aws-region: eu-west-1
      - name: Traer el manifiesto de producción
        run: aws s3 cp s3://my-dbt-artifacts/prod/manifest.json prod-artifacts/manifest.json
      - name: Construir y probar los modelos modificados y sus hijos
        run: dbt build --select state:modified+ --defer --state prod-artifacts --target ci
      - name: Borrar el esquema del pull request
        if: always()
        run: dbt run-operation drop_schema --args "{schema: $DBT_TARGET_SCHEMA}"
```

El perfil lee la configuración de conexión de variables de entorno (`env_var('SNOWFLAKE_ACCOUNT')`, etc.), así no hay credenciales en el repositorio. `drop_schema` es una pequeña macro del proyecto; borrar el esquema con `if: always()` mantiene limpio el warehouse aunque falle la construcción. Al fusionar, corre el job de producción y sube su nuevo `manifest.json`, que se convierte en el punto de comparación del siguiente pull request.

## Ejemplo 4: plan de Terraform en los pull requests, apply en main

Los cambios de infraestructura merecen la misma revisión que el código. El plan va al pull request; el apply solo ocurre desde `main`, detrás del entorno de producción:

```yaml
name: infra
on:
  pull_request:
    paths: ["infra/**"]
  push:
    branches: [main]
    paths: ["infra/**"]

permissions:
  contents: read
  id-token: write
  pull-requests: write          # para comentar el plan

jobs:
  terraform:
    runs-on: ubuntu-24.04
    environment: ${{ github.event_name == 'push' && 'production' || 'plan' }}
    defaults:
      run:
        working-directory: infra
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.TERRAFORM_ROLE_ARN }}
          aws-region: eu-west-1
      - run: terraform init -input=false
      - run: terraform plan -input=false -out=tfplan -no-color | tee plan.txt
      - name: Comentar el plan en el pull request
        if: github.event_name == 'pull_request'
        run: gh pr comment ${{ github.event.pull_request.number }} --body-file plan.txt
        env:
          GH_TOKEN: ${{ github.token }}
      - name: Aplicar
        if: github.event_name == 'push'
        run: terraform apply -input=false tfplan
```

Aquí es mejor tener dos roles que uno: un rol de solo lectura para los planes de los pull requests y un rol que puede cambiar recursos, en el que solo confía el entorno de producción. Añade reglas de ciclo de vida `prevent_destroy` a los recursos que nunca deben borrarse por accidente.

## Ejemplo 5: un sitio estático cuyos datos nunca se vuelven a desplegar

Este sitio se despliega con un workflow pequeño: cada push ejecuta las pruebas (que construyen todo el sitio y revisan enlaces, traducciones y metadatos), y los push a `master` despliegan en S3 y CloudFront mediante OIDC. Hay un detalle propio de los productos de datos: el pipeline de registros escribe su JSON directamente en el bucket del sitio, así que el script de despliegue **excluye la ruta de los datos**. Publicar datos nuevos nunca requiere desplegar el sitio, y desplegar el sitio nunca sobrescribe la salida del pipeline.

```yaml
jobs:
  test:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip
      - run: pip install -r requirements-dev.txt
      - run: pytest -q            # construye el sitio y revisa enlaces, metadatos y traducciones

  deploy:
    needs: test
    if: github.ref == 'refs/heads/master' && github.event_name != 'pull_request'
    runs-on: ubuntu-24.04
    environment:
      name: production
      url: https://www.catobyte.co
    concurrency:
      group: production
      cancel-in-progress: false
    permissions:
      contents: read
      id-token: write
    env:
      BUCKET: ${{ vars.S3_BUCKET }}
      DISTRIBUTION_ID: ${{ vars.CLOUDFRONT_DISTRIBUTION_ID }}
      PYTHON: python
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip
      - run: pip install -r requirements-dev.txt
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.AWS_DEPLOY_ROLE_ARN }}
          aws-region: ${{ vars.AWS_REGION }}
      # prueba, construye, sincroniza con S3 con --exclude "*/projects/*/data/*" e invalida CloudFront
      - run: ./scripts/deploy.sh
```

## Ejemplo 6: backfills manuales con entradas

Los backfills no deberían depender del portátil de nadie. Un `workflow_dispatch` con entradas tipadas da una forma revisada y registrada de reprocesar un periodo:

```yaml
name: backfill
on:
  workflow_dispatch:
    inputs:
      start_date:
        description: Primera fecha a reprocesar (AAAA-MM-DD)
        required: true
      end_date:
        description: Última fecha a reprocesar (AAAA-MM-DD)
        required: true

jobs:
  backfill:
    runs-on: ubuntu-24.04
    environment: production          # la misma aprobación que un despliegue
    env:
      DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
      DATABRICKS_CLIENT_ID: ${{ secrets.DATABRICKS_CLIENT_ID }}
      DATABRICKS_CLIENT_SECRET: ${{ secrets.DATABRICKS_CLIENT_SECRET }}
    steps:
      - uses: actions/checkout@v4
      - uses: databricks/setup-cli@main
      - name: Ejecutar el job de backfill para el periodo pedido
        run: |
          databricks bundle run -t prod backfill_job \
            --params start_date=${{ inputs.start_date }},end_date=${{ inputs.end_date }}
```

El propio pipeline debe aceptar rangos de fechas y escribir de forma idempotente; el workflow solo hace que ejecutarlo sea seguro, auditable y aprobado.

## Lista de endurecimiento para GitHub Actions

- Define `permissions:` de forma explícita; por defecto `contents: read`, y concede más por job.
- Usa OIDC para el acceso a la nube; restringe la confianza del rol al repositorio y al entorno.
- Guarda los secretos de despliegue en **entornos** con revisores obligatorios y restricciones de ramas.
- En los repositorios públicos, guarda los valores identificativos (hosts, buckets, IDs de cuenta, correos) como secretos para que se enmascaren.
- Fija las acciones de terceros a un SHA de commit completo en los workflows de producción, y deja que Dependabot las actualice.
- Nunca hagas checkout ni ejecutes el código de un pull request en workflows `pull_request_target`.
- Usa `concurrency` para que los despliegues nunca se solapen.
- Añade `timeout-minutes` a los jobs para que un paso colgado no pueda correr seis horas.
- Fija la imagen del runner (`ubuntu-24.04`) para compilaciones reproducibles.
- Escanea todo el historial en busca de secretos y exige la revisión de los code owners para `.github/workflows/`.

## Errores comunes

- **Un CI que solo hace linting.** Sin pruebas unitarias y de extremo a extremo, el CI da una falsa sensación de seguridad.
- **Desplegar reconstruyendo para cada entorno.** Lo que probaste no es lo que desplegaste.
- **Claves de nube de larga duración en los secretos.** Se filtran, se comparten y nadie las rota.
- **Tratar los cambios de esquema como cambios de código.** Borrar una columna que usan los consumidores los rompe, por muy verde que esté el pipeline.
- **No tener un plan para revertir los datos.** Revertir el código no deshace lo escrito en las tablas; antes de desplegar, ten claro cómo vas a restaurar (viaje en el tiempo, snapshots, versión anterior de la tabla).
- **Pasos manuales "solo por esta vez".** Cada cambio manual en producción es una deriva que el siguiente despliegue puede sobrescribir.

El CI/CD de datos no se trata del YAML. Se trata de que cada cambio siga el mismo camino, para que la plataforma pueda cambiar rápido sin que las cifras cambien por accidente. Empieza poco a poco: pon todo en Git, añade un job de CI que ejecute tus pruebas en cada pull request, y luego automatiza un despliegue con OIDC y una aprobación. Cada paso se paga solo la primera vez que detecta un problema antes que tus usuarios.
