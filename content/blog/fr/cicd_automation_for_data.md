## CI/CD et automatisation pour les données : l'essentiel, avec des exemples GitHub Actions

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![CI/CD et automatisation des pipelines de données](../../images/cicd_automation_for_data_title_img.png)

*Article technique*

## Pourquoi les équipes data ont besoin de CI/CD

Il y a dix ans, déployer un pipeline de données revenait souvent à copier un script sur un serveur, modifier une ligne de cron et croiser les doigts. J'ai vu des correctifs d'urgence tapés directement en production, des jobs qui fonctionnaient dans un environnement et pas dans un autre, et des lundis matin passés à chercher lequel des changements du vendredi avait cassé les tableaux de bord. Rien de tout cela n'est un problème d'outillage. C'est ce qui arrive quand les changements atteignent la production sans chemin reproductible et automatisé.

La CI/CD donne le même chemin à chaque changement : il est versionné, relu, testé automatiquement, déployé par une machine avec les mêmes étapes à chaque fois, et traçable ensuite. Pour les équipes data, elle apporte les mêmes bénéfices que pour les équipes applicatives (moins d'incidents, livraison plus rapide, retours arrière faciles), mais les données ajoutent leurs propres considérations. Cet article présente ce qui me semble le plus important, puis montre des workflows GitHub Actions concrets, dont plusieurs sont tirés des pipelines derrière ce site et de mon [lakehouse des registres d'entreprises européens](../projects/eu-company-registry.html).

## Ce qui rend la CI/CD des données différente

Quatre différences conditionnent tout le reste :

1. **Les pipelines ont un état.** Déployer du nouveau code ne remplace pas les tables qu'il a écrites. Un changement de schéma demande une migration ; un changement de logique peut demander un backfill ; un mauvais déploiement peut exiger de restaurer des données, pas seulement de revenir à l'ancien code.
2. **La justesse dépend des données, pas seulement du code.** Les tests sur jeux de test prouvent la logique. Seuls les contrôles de qualité sur les données réelles prouvent que le fichier du mois prochain est sain. La CI/CD doit inclure les deux.
3. **Les déploiements peuvent coûter cher.** Modifier un modèle central peut déclencher le recalcul de plusieurs années d'historique. Le coût et le calendrier font partie du plan de mise en production.
4. **Plusieurs systèmes sont impliqués.** Une plateforme data typique couvre un dépôt de code, un compte cloud, une plateforme de calcul (Databricks, Snowflake, Glue) et un orchestrateur. Chacun a besoin d'identifiants, et aucun ne devrait détenir les secrets d'un autre.

## Les considérations qui comptent

### Tout versionner

Le code, les modèles SQL, les définitions d'orchestration (DAG, Databricks Asset Bundles, spécifications de jobs), l'infrastructure (Terraform, CloudFormation, SAM), les permissions, les règles de qualité et les workflows de CI ont tous leur place dans Git. Si quelque chose ne peut être modifié qu'en cliquant dans une console, il ne peut être ni relu, ni testé, ni annulé. Les données réelles et les secrets sont les deux seules choses qui n'y entrent jamais.

### Tester par couches, et rendre les couches rapides vraiment rapides

Le lint et les tests unitaires devraient tourner en quelques secondes ; une exécution de bout en bout sur des données synthétiques en quelques minutes ; les contrôles de qualité en production à chaque exécution. Si les vérifications d'une pull request prennent 45 minutes, les développeurs trouveront des moyens de les contourner. J'ai décrit ces couches de tests en détail dans [Tests et performances des pipelines big data](testing_and_performance_big_data.html).

### Séparer les environnements, promouvoir le même artefact

Au minimum un environnement de développement, un de staging ou préproduction, et la production, idéalement dans des comptes, espaces de travail ou catalogues distincts, pour qu'une erreur en dev ne puisse pas toucher les données de production. Construisez une fois (un wheel, une image, un bundle), marquez-le avec le commit et promouvez ce même artefact. La configuration change selon l'environnement ; le code, non.

### Des identités, pas des clés

La plus grande amélioration de sécurité de la CI/CD ces dernières années est la **fédération d'identité des workloads (OIDC)**. Au lieu de stocker des clés d'accès cloud à longue durée de vie comme secrets du dépôt, le workflow demande un jeton éphémère à GitHub et l'échange contre les identifiants temporaires d'un rôle qui ne fait confiance qu'à ce dépôt et à cet environnement. Rien à faire fuiter, rien à renouveler. Databricks, Snowflake (paire de clés ou OAuth) et les grands clouds prennent tous en charge les identités machine ; déployez avec des principaux de service, jamais au nom d'une personne.

### Rendre les déploiements sûrs à répéter

Les déploiements sont relancés, réexécutés et parfois déclenchés deux fois. L'infrastructure as code est déclarative (l'appliquer deux fois ne change rien), les bundles et les jobs sont mis à jour en place, et les pipelines eux-mêmes doivent être idempotents (`MERGE` ou écrasement par partition, jamais d'ajouts aveugles). Ne laissez jamais deux déploiements vers le même environnement tourner en même temps.

### Planifier les changements de données, pas seulement de code

Pour chaque pull request, demandez-vous : ce changement modifie-t-il un schéma dont dépendent des consommateurs ? Demande-t-il de retraiter l'historique ? Utilisez des changements de schéma rétrocompatibles (ajouter, migrer, puis supprimer : *expand and contract*), des contrats de données vérifiés en CI, des modèles versionnés pour les changements cassants, et un plan de backfill explicite avec coût et calendrier. Le write-audit-publish (écrire les nouvelles données dans un emplacement intermédiaire, les vérifier, puis basculer) tient les mauvaises données à l'écart des consommateurs.

### Protéger la production, mais avec une barrière légère

Une approbation obligatoire avant la production est une assurance bon marché pour les plateformes de données, où un seul mauvais déploiement peut corrompre des tables lues par les consommateurs. Automatisez tout ce qui précède la barrière, pour que l'approbation soit un coup d'œil rapide à un pipeline vert, pas une liste de contrôle manuelle.

### Surveiller ce qui se passe après le déploiement

La CI/CD ne s'arrête pas à « déploiement réussi ». Les smoke tests, les résultats de qualité de l'exécution suivante, la surveillance de la fraîcheur et des volumes, et les alertes de durée vous disent si le changement fonctionne vraiment avec les données réelles.

### Prudence avec les dépôts publics

Si le dépôt est public, ses journaux de workflow le sont aussi. GitHub masque les secrets dans les journaux, mais pas les variables simples. Noms d'hôtes, noms de buckets, identifiants de compte et adresses e-mail devraient être stockés comme **secrets** d'un environnement protégé, même s'ils ne sont pas des mots de passe, pour n'apparaître jamais dans un journal public. Recherchez les secrets dans tout l'historique en CI, pas seulement dans les nouveaux commits.

## GitHub Actions en cinq minutes

Les workflows sont des fichiers YAML dans `.github/workflows/`. Chaque workflow est déclenché par des événements (`push`, `pull_request`, `schedule`, `workflow_dispatch` pour les exécutions manuelles, `workflow_call` pour être réutilisé par d'autres workflows) et contient des **jobs** qui tournent sur des machines virtuelles neuves (runners). Les jobs s'exécutent en parallèle sauf si l'un `needs` un autre ; chaque job est une liste de **steps** qui exécutent des commandes shell ou des **actions** réutilisables. Les **environments** (par exemple `production`) ont leurs propres secrets et variables et peuvent exiger des relecteurs avant le démarrage d'un job qui les cible. Cela suffit pour lire les exemples ci-dessous.

## Exemple 1 : CI d'un projet PySpark

Voici la forme de la CI de mon dépôt lakehouse. Elle tourne sur chaque pull request et sert de première étape au workflow de déploiement :

```yaml
name: ci

on:
  pull_request:
  workflow_call:      # cd.yml l'exécute comme barrière avant tout déploiement
  workflow_dispatch:

permissions:
  contents: read      # moindre privilège par défaut

jobs:
  checks:
    runs-on: ubuntu-24.04
    timeout-minutes: 40
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0              # historique complet, pour la recherche de secrets

      - name: Secret scan (full history)
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip

      - uses: actions/setup-java@v4   # Spark a besoin d'une JVM
        with:
          distribution: temurin
          java-version: "17"

      - name: Install
        run: pip install -e ".[local,dev]"

      - name: Lint (ruff + PySpark anti-patterns + sensitive data)
        run: |
          ruff check src tests tools
          python tools/spark_lint.py src
          git ls-files | xargs python tools/check_sensitive.py

      - name: Unit tests
        run: pytest tests -m "not e2e" --cov=registry_lakehouse --cov-report=term-missing

      - name: End-to-end pipeline on synthetic fixtures
        run: pytest tests -m e2e
```

Quelques choix à noter :

- **`permissions: contents: read`** en tête : le `GITHUB_TOKEN` généré automatiquement n'a qu'un accès en lecture, sauf si un job en demande explicitement davantage.
- **La recherche de secrets lit tout l'historique**, car une clé commitée puis supprimée est toujours dans le dépôt.
- **Des règles de lint maison** codifient les leçons apprises : pas de `collect()` sur des données non bornées, pas d'UDF Python, rien qui casse sur Databricks serverless, pas de chemins de buckets en dur.
- **Les tests unitaires et l'exécution de bout en bout sont des étapes séparées**, si bien qu'un échec indique immédiatement quelle couche a cassé.
- **`workflow_call`** permet au workflow de déploiement de réutiliser exactement ce fichier au lieu de le dupliquer.

## Exemple 2 : déploiement continu vers AWS et Databricks

Le workflow de déploiement tourne à chaque push sur `main`. Il réutilise la CI comme barrière, puis déploie deux systèmes indépendants, chacun seulement après une approbation manuelle dans l'environnement `production` :

```yaml
# push sur main ──► ci (tous les tests) ──► [approbation production] ──► ingestion AWS (SAM)
#                                                                  └──► job Databricks (bundle)
name: cd

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      run_job:
        description: Start a production run right after deploying
        type: boolean
        default: false

concurrency:
  group: deploy-production
  cancel-in-progress: false      # ne jamais interrompre un déploiement en cours

permissions:
  contents: read

jobs:
  tests:
    uses: ./.github/workflows/ci.yml

  aws:
    needs: tests
    if: vars.DEPLOY_AWS == 'true'          # activé une fois la configuration AWS en place
    runs-on: ubuntu-24.04
    environment: production
    permissions:
      contents: read
      id-token: write                      # autorise GitHub OIDC -> rôle AWS
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/setup-sam@v2
        with:
          use-installer: true
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_DEPLOY_ROLE_ARN }}
          aws-region: ${{ vars.AWS_REGION }}
      - name: Build and deploy
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
      - uses: databricks/setup-cli@main      # épingler sur un SHA de commit en production
      - name: Stamp a unique wheel version
        run: python tools/set_version.py "0.2.${{ github.run_number }}+g${GITHUB_SHA::7}"
      - name: Validate against the workspace
        run: databricks bundle validate -t prod --strict
      - name: Deploy
        run: databricks bundle deploy -t prod
      - name: Start a run (optional)
        if: github.event_name == 'workflow_dispatch' && inputs.run_job
        run: databricks bundle run -t prod registry_lakehouse --no-wait
```

Ce que ce workflow fait bien, et pourquoi :

- **La CI est la barrière.** `uses: ./.github/workflows/ci.yml` exécute les mêmes tests que les pull requests ; rien n'est déployé s'ils échouent.
- **`concurrency` avec `cancel-in-progress: false`** met les déploiements en file d'attente au lieu d'en exécuter deux à la fois ou d'en interrompre un en cours.
- **Aucune clé AWS nulle part.** `id-token: write` permet au job de demander un jeton OIDC ; `configure-aws-credentials` l'échange contre un rôle temporaire. La politique de confiance du rôle n'accepte que les jetons de l'environnement `production` de ce dépôt.
- **Databricks est déployé par un principal de service** via OAuth machine à machine. Le bundle définit le job, sa planification, ses alertes et ses permissions sous forme de code.
- **Chaque artefact est traçable.** La version du wheel contient le numéro d'exécution et le SHA court du commit.
- **Des variables du dépôt activent chaque déploiement** (`vars.DEPLOY_AWS == 'true'`), si bien que le workflow reste vert tant qu'un environnement cible n'est pas encore configuré.
- **Les valeurs identifiantes sont des secrets**, car le dépôt est public et seuls les secrets sont masqués dans les journaux.
- **Lancer une exécution en production est une décision séparée et manuelle**, via les inputs de `workflow_dispatch`.

Côté AWS, c'est la politique de confiance du rôle qui rend l'OIDC sûr. La partie importante est la condition sur le sujet du jeton :

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

## Exemple 3 : slim CI pour dbt

Dans un projet dbt, tout reconstruire à chaque pull request est lent et coûteux. La slim CI ne construit que les modèles modifiés par la pull request et tout ce qui en dépend en aval, dans un schéma propre à la pull request, en renvoyant les références inchangées vers la production :

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
  cancel-in-progress: true          # un nouveau push remplace l'exécution précédente

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
      - name: Lint SQL
        run: sqlfluff lint models
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.ARTIFACTS_READ_ROLE_ARN }}
          aws-region: eu-west-1
      - name: Fetch the production manifest
        run: aws s3 cp s3://my-dbt-artifacts/prod/manifest.json prod-artifacts/manifest.json
      - name: Build and test modified models and their children
        run: dbt build --select state:modified+ --defer --state prod-artifacts --target ci
      - name: Drop the pull request schema
        if: always()
        run: dbt run-operation drop_schema --args "{schema: $DBT_TARGET_SCHEMA}"
```

Le profil lit ses paramètres de connexion dans des variables d'environnement (`env_var('SNOWFLAKE_ACCOUNT')`, etc.), si bien qu'aucun identifiant ne vit dans le dépôt. `drop_schema` est une petite macro du projet ; supprimer le schéma avec `if: always()` garde l'entrepôt propre même quand le build échoue. Au merge, le job de production s'exécute et téléverse son nouveau `manifest.json`, qui devient le point de comparaison de la pull request suivante.

## Exemple 4 : plan Terraform sur les pull requests, apply sur main

Les changements d'infrastructure méritent la même relecture que le code. Le plan est publié dans la pull request ; l'apply n'a lieu que depuis `main`, derrière l'environnement de production :

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
  pull-requests: write          # pour commenter le plan

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
      - name: Comment the plan on the pull request
        if: github.event_name == 'pull_request'
        run: gh pr comment ${{ github.event.pull_request.number }} --body-file plan.txt
        env:
          GH_TOKEN: ${{ github.token }}
      - name: Apply
        if: github.event_name == 'push'
        run: terraform apply -input=false tfplan
```

Deux rôles valent mieux qu'un ici : un rôle en lecture seule pour les plans des pull requests, et un rôle capable de modifier les ressources, auquel on ne fait confiance que depuis l'environnement de production. Ajoutez des règles de cycle de vie `prevent_destroy` sur les ressources qui ne doivent jamais être supprimées par accident.

## Exemple 5 : un site statique dont les données ne sont jamais redéployées

Ce site est déployé par un petit workflow : chaque push exécute les tests (qui construisent tout le site et vérifient liens, traductions et métadonnées), et les pushs sur `master` déploient vers S3 et CloudFront via OIDC. Un détail est propre aux produits de données : le pipeline des registres écrit ses JSON directement dans le bucket du site, donc le script de déploiement **exclut le chemin des données**. Publier de nouvelles données ne demande jamais de déployer le site, et un déploiement du site n'écrase jamais la sortie du pipeline.

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
      - run: pytest -q            # construit le site, vérifie liens, métadonnées, traductions

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
      # tests, build, synchronisation S3 avec --exclude "*/projects/*/data/*", puis invalidation CloudFront
      - run: ./scripts/deploy.sh
```

## Exemple 6 : backfills manuels avec des inputs

Un backfill ne devrait pas dépendre du portable de quelqu'un. Un `workflow_dispatch` avec des inputs typés offre un moyen relu et journalisé de retraiter une période :

```yaml
name: backfill
on:
  workflow_dispatch:
    inputs:
      start_date:
        description: First date to reprocess (YYYY-MM-DD)
        required: true
      end_date:
        description: Last date to reprocess (YYYY-MM-DD)
        required: true

jobs:
  backfill:
    runs-on: ubuntu-24.04
    environment: production          # même approbation qu'un déploiement
    env:
      DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
      DATABRICKS_CLIENT_ID: ${{ secrets.DATABRICKS_CLIENT_ID }}
      DATABRICKS_CLIENT_SECRET: ${{ secrets.DATABRICKS_CLIENT_SECRET }}
    steps:
      - uses: actions/checkout@v4
      - uses: databricks/setup-cli@main
      - name: Run the backfill job for the requested period
        run: |
          databricks bundle run -t prod backfill_job \
            --params start_date=${{ inputs.start_date }},end_date=${{ inputs.end_date }}
```

Le pipeline lui-même doit accepter des plages de dates et écrire de façon idempotente ; le workflow ne fait que rendre son exécution sûre, auditable et approuvée.

## Liste de durcissement pour GitHub Actions

- Définissez `permissions:` explicitement ; `contents: read` par défaut, et accordez davantage job par job.
- Utilisez l'OIDC pour l'accès au cloud ; limitez la confiance du rôle au dépôt et à l'environnement.
- Stockez les secrets de déploiement dans des **environments** avec relecteurs obligatoires et restrictions de branches.
- Dans les dépôts publics, stockez les valeurs identifiantes (hôtes, buckets, identifiants de compte, e-mails) comme secrets pour qu'elles soient masquées.
- Épinglez les actions tierces sur un SHA de commit complet dans les workflows de production, et laissez Dependabot les mettre à jour.
- Ne récupérez et n'exécutez jamais le code d'une pull request dans un workflow `pull_request_target`.
- Utilisez `concurrency` pour que les déploiements ne se chevauchent jamais.
- Ajoutez `timeout-minutes` aux jobs pour qu'une étape bloquée ne tourne pas six heures.
- Épinglez l'image du runner (`ubuntu-24.04`) pour des builds reproductibles.
- Recherchez les secrets dans tout l'historique, et exigez la relecture d'un code owner pour `.github/workflows/`.

## Pièges courants

- **Une CI qui ne fait que du lint.** Sans tests unitaires et de bout en bout, la CI donne un faux sentiment de sécurité.
- **Déployer en reconstruisant pour chaque environnement.** Ce que vous avez testé n'est pas ce que vous avez déployé.
- **Des clés cloud à longue durée de vie dans les secrets.** Elles fuient, elles sont partagées et personne ne les renouvelle.
- **Traiter les changements de schéma comme des changements de code.** Supprimer une colonne utilisée par des consommateurs les casse, aussi vert que soit le pipeline.
- **Aucun plan de retour arrière des données.** Revenir à l'ancien code ne désécrit pas les tables ; sachez comment vous restaurerez (voyage dans le temps, snapshots, version précédente de la table) avant de déployer.
- **Des étapes manuelles « juste pour cette fois ».** Chaque changement manuel en production est une dérive que le prochain déploiement risque d'écraser.

La CI/CD des données ne se résume pas au YAML. Il s'agit de faire suivre le même chemin à chaque changement, pour que la plateforme puisse évoluer vite sans que les chiffres changent par accident. Commencez petit : mettez tout dans Git, ajoutez un job de CI qui exécute vos tests sur chaque pull request, puis automatisez un déploiement avec OIDC et une approbation. Chaque étape est rentabilisée dès la première fois qu'elle détecte un problème avant vos utilisateurs.
