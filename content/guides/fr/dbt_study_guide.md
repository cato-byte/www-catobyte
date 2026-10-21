## Fiche d'étude dbt

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude dbt : environ 200 questions](../../images/dbt_study_guide_title_img.png)

Environ 200 questions d'entretien sur dbt (data build tool), des bases aux modèles incrémentaux, snapshots, tests, déploiement et performances. Les réponses suivent le dbt actuel : v2, le moteur en Rust installé par défaut, et les conventions YAML communes à dbt v1.10 et versions ultérieures. Quand dbt v1 se comporte différemment, la réponse le précise.

La fiche suit un parcours d'apprentissage en quatre étapes. Chaque section est découpée en unités courtes : objectifs d'apprentissage, explication du concept et exemple commenté, puis questions (d'abord de mémorisation, ensuite d'application), un exercice pratique et les points à retenir. Pour **apprendre**, lisez chaque unité du début à la fin. Pour **réviser**, passez en mode révision ou utilisez « Aller aux questions », marquez les réponses à revoir et essayez une révision mixte entre les sections.

<!-- QA -->
<!-- stage: Fondamentaux -->

### Fondamentaux

<!-- unit: Ce qu'est dbt -->

<!-- goals -->

- Expliquer ce que fait dbt et sa place dans l'ELT.
- Comparer dbt aux outils ETL et aux procédures stockées, limites comprises.

<!-- concept -->

Une fois les données brutes chargées dans un entrepôt, il faut les transformer en tables propres et fiables. Pendant des années, cela voulait dire des procédures stockées et des scripts lancés dans un ordre fixe que seul leur auteur comprenait. dbt les remplace par un framework : chaque transformation est un `SELECT` dans un fichier, les dépendances sont déclarées dans le code, et dbt construit tout dans le bon ordre au sein de l'entrepôt.

Les pratiques logicielles suivent : gestion de versions, tests, documentation et revues. Ce que dbt ne fait pas : charger les données ou se planifier lui-même.

<!-- example -->

```sql
-- models/marts/fct_orders.sql
select
    o.order_id,
    o.customer_id,
    o.ordered_at,
    sum(p.amount) as amount
from {{ ref('stg_shop__orders') }} o
left join {{ ref('stg_shop__payments') }} p using (order_id)
group by 1, 2, 3
```

#### Qu'est-ce que dbt ?

dbt (data build tool) est un framework de transformation : on écrit des requêtes `SELECT` sous forme de modèles, et dbt les compile avec Jinja, déduit leurs dépendances et les exécute dans l'entrepôt de données sous forme de tables ou de vues. Il apporte aux transformations SQL les pratiques du génie logiciel (gestion de versions, tests, documentation, modularité, CI/CD). dbt est le « T » de l'ELT.

#### Quels sont les cas d'usage courants de dbt ?

Construire un entrepôt de données ou un lakehouse couche par couche (staging, intermédiaire, marts), nettoyer et normaliser des données brutes, construire des modèles dimensionnels pour la BI, historiser des données à évolution lente avec des snapshots, tester la qualité des données, documenter les jeux de données avec leur lignage, et définir des indicateurs métier partagés dans la couche sémantique.

#### En quoi dbt diffère-t-il des outils ETL traditionnels ?

Les outils ETL traditionnels extraient, transforment dans leur propre moteur puis chargent, souvent via une interface graphique. dbt ne fait que transformer, dans l'entrepôt qui contient déjà les données chargées (ELT), avec du SQL dans des fichiers texte. Tout est du code : versionné dans Git, relu, testé et déployé comme un logiciel. L'extraction et le chargement sont confiés à d'autres outils (Fivetran, Airbyte, pipelines maison).

#### Que signifie ELT, et pourquoi dbt s'y prête-t-il ?

Extract, Load, Transform : les données brutes sont d'abord chargées dans l'entrepôt, puis transformées sur place. Les entrepôts modernes sont peu coûteux en stockage et puissants en calcul : transformer en SQL là où se trouvent déjà les données est plus simple et passe à l'échelle. dbt structure cette étape de transformation.

#### Quels problèmes dbt résout-il par rapport aux procédures stockées et aux scripts ?

Les dépendances sont explicites et résolues automatiquement, le code est modulaire et réutilisable grâce à `ref` et aux macros, les tests et la documentation vivent à côté du code, on change d'environnement par la configuration et non en modifiant le code, et tout est versionné et relisible.

#### Quelles sont les difficultés de dbt ?

Il ne couvre que la transformation : il faut d'autres outils pour l'ingestion et l'orchestration. Les gros projets peuvent devenir lents à compiler et difficiles à parcourir sans conventions. Les modèles incrémentaux et les snapshots demandent une conception soignée. Jinja peut rendre le SQL illisible s'il est surutilisé. Les performances dépendent toujours de l'entrepôt et du SQL écrit, et les coûts peuvent grimper si les full refresh sont trop fréquents.

<!-- challenge -->

Une équipe a 80 procédures stockées lancées par un ordonnanceur dans un ordre maintenu à la main. Citez deux améliorations concrètes qu'apporterait dbt et une chose dont elle aurait encore besoin.

<!-- solution -->

dbt déduirait l'ordre d'exécution des dépendances `ref()` et ajouterait tests et documentation à côté du code dans Git. Il lui faudrait encore l'ingestion vers l'entrepôt et un orchestrateur ou ordonnanceur pour lancer dbt.

<!-- takeaways -->

- dbt transforme des `SELECT` en tables et vues gérées.
- Dépendances, tests et doc vivent avec le code.
- L'ingestion et l'orchestration restent hors de dbt.

<!-- unit: dbt dans l'écosystème -->

<!-- goals -->

- Comparer dbt à Spark et distinguer dbt auto-hébergé de la plateforme dbt.
- Expliquer adapters, dbt v1 et v2, analyse statique et Semantic Layer.

<!-- concept -->

dbt n'est pas un moteur de requêtes. Il génère du SQL (ou du Python) et l'envoie à une plateforme de données via un adapter : c'est l'entrepôt qui fait le travail. C'est pourquoi il s'associe aux plateformes basées sur Spark au lieu de les concurrencer.

Vous pouvez exécuter dbt vous-même en ligne de commande ou utiliser la plateforme dbt managée, qui ajoute IDE, planification et fonctions hébergées. Le moteur dbt existe en deux générations : v1, le CLI Python d'origine, et v2, une réécriture en Rust (d'abord appelée dbt Fusion) qui est aujourd'hui l'installation par défaut. v2 exécute le même code de projet, mais comprend en plus le SQL qu'il compile.

<!-- example -->

| Composant | Rôle |
|---|---|
| dbt v2 | Moteur par défaut, écrit en Rust : parsing rapide, compréhension du SQL, `dbt lint` |
| dbt v1 | Moteur Python d'origine (anciennement dbt Core), toujours maintenu |
| Plateforme dbt (anciennement dbt Cloud) | Studio IDE, jobs, CI, Catalog, API Semantic Layer |
| Adapter | Dialogue avec Snowflake, BigQuery, Databricks, Redshift... |

#### Comment dbt se compare-t-il à Apache Spark ?

Spark est un moteur de traitement distribué qu'on programme en Python, Scala ou SQL, et dont on gère les jobs et les clusters. dbt n'est pas un moteur : il génère du SQL et l'envoie à un moteur (Snowflake, BigQuery, Redshift, Databricks, Postgres, et Spark lui-même via les adaptateurs dbt-spark ou dbt-databricks). Ils sont complémentaires : dbt peut orchestrer des transformations SQL exécutées par Spark, tandis que les traitements complexes non SQL restent en code Spark.

#### Quelle est la différence entre dbt auto-hébergé et la dbt platform ?

dbt auto-hébergé est l'outil en ligne de commande que l'on installe (`pip install dbt` ou un installeur natif), exécute et orchestre soi-même ; c'est ce qu'on appelait dbt Core. La dbt platform (anciennement dbt Cloud) est le service commercial géré : Studio IDE, planificateur de jobs, jobs de CI, Catalog pour la documentation et le lignage, les API de la couche sémantique, des alertes et le contrôle d'accès. Les deux exécutent le même code de projet, et la plateforme prend en charge les deux versions du moteur.

#### Que sont dbt v1 et dbt v2 ?

Les deux générations du moteur dbt. dbt v1 est l'implémentation Python d'origine (les versions 1.x de dbt Core). dbt v2 est une réécriture en Rust, sortie d'abord sous le nom dbt Fusion, et c'est aujourd'hui ce qu'installe `pip install dbt`. Les projets se transposent, mais v2 est plus strict : configs mal orthographiées, clés YAML inconnues, macros inexistantes et variables non définies échouent dès l'analyse du projet au lieu d'être ignorées ou d'échouer plus tard. En échange, v2 analyse beaucoup plus vite et ajoute l'analyse statique, le lignage au niveau des colonnes, un linter intégré (`dbt lint`), des contrôles du projet (`dbt check`) et un serveur de langage pour l'extension VS Code. Les deux générations produisent des artefacts compatibles et peuvent donc cohabiter pendant une migration.

#### Qu'est-ce que l'analyse statique dans dbt v2 ?

Après avoir rendu le Jinja, v2 transforme le SQL de chaque modèle en plan logique sans interroger l'entrepôt. Il détecte ainsi les erreurs SQL avant toute exécution. La config `static_analysis` règle son niveau d'exigence. `baseline`, la valeur par défaut, signale les problèmes comme des avertissements. `strict` résout les types de colonnes sur tout le DAG et échoue avant l'exécution ; il est nécessaire pour le lignage au niveau des colonnes. dbt v1 ne fait que rendre les templates : les erreurs SQL apparaissent quand l'entrepôt exécute la requête.

#### Qu'est-ce qu'un adaptateur dbt ?

Un plugin qui permet à dbt de dialoguer avec une plateforme de données donnée, en traduisant les opérations génériques de dbt dans le dialecte SQL de cette plateforme : Snowflake, BigQuery, Databricks, Redshift, Postgres, Spark et de nombreux adaptateurs communautaires. Dans dbt v1, ce sont des packages Python (`dbt-snowflake`, `dbt-bigquery`...). Dans dbt v2, ils se connectent via des drivers ADBC que dbt télécharge à la première utilisation, si bien que dbt est distribué sous forme d'un binaire unique.

#### Qu'est-ce que la couche sémantique de dbt ?

Une couche, fondée sur MetricFlow, où les indicateurs (chiffre d'affaires, utilisateurs actifs) sont définis une seule fois en YAML au-dessus des modèles dbt, puis interrogés de façon cohérente par la BI et d'autres outils via des API, pour que chaque outil calcule l'indicateur de la même façon.

<!-- challenge -->

Une équipe sur Databricks demande s'il faut utiliser dbt ou Spark pour les transformations. Que répondez-vous ?

<!-- solution -->

Les deux : dbt peut exécuter des modèles SQL (et Python) sur Databricks via l'adapter, Spark les exécutant. Utiliser dbt pour une modélisation orientée SQL avec tests et lignage ; des jobs Spark directs pour les traitements complexes riches en code.

<!-- takeaways -->

- dbt génère le code ; la plateforme l'exécute.
- dbt v2 (Rust) est le moteur par défaut ; v1 est le moteur Python d'origine.
- La plateforme dbt ajoute des fonctions managées au-dessus de l'un ou l'autre moteur.

<!-- unit: Modèles et DAG -->

<!-- goals -->

- Décrire les modèles dbt et le DAG construit à partir de leurs références.
- Choisir entre modèles SQL et Python et concevoir des couches modulaires.

<!-- concept -->

Un modèle, c'est un fichier avec un `SELECT`. Quand il référence un autre modèle avec `ref()`, dbt enregistre une arête, et l'ensemble des arêtes forme un DAG qui décide l'ordre de construction et ce qui peut tourner en parallèle.

La modularité devient bon marché : de petits modèles à responsabilité unique, réutilisés par de nombreux modèles en aval. Les modèles Python servent aux rares transformations que le SQL gère mal, tout en restant dans le même DAG.

<!-- example -->

```python
# models/ml/customer_features.py
def model(dbt, session):
    orders = dbt.ref("fct_orders").to_pandas()
    feats = orders.groupby("customer_id").agg(orders=("order_id", "count"), spend=("amount", "sum"))
    return feats.reset_index()
```

#### Qu'est-ce qu'un modèle dbt ?

Un fichier `.sql` du dossier `models/` qui contient une requête `SELECT`. dbt l'enveloppe dans le DDL nécessaire pour créer une vue, une table ou un autre objet portant le nom du fichier. Des modèles Python (`.py`) sont aussi pris en charge sur certaines plateformes.

#### Qu'est-ce que le DAG dans le contexte de dbt ?

Le graphe orienté acyclique des dépendances entre modèles, sources, seeds et snapshots, construit à partir des appels à `ref()` et `source()`. dbt s'en sert pour exécuter les nœuds dans le bon ordre (et en parallèle quand c'est possible), pour sélectionner des parties du projet et pour dessiner le lignage dans la documentation.

#### Que signifie « modélisation de données modulaire » dans dbt ?

Découper les transformations en petits modèles réutilisables avec une seule responsabilité chacun (staging par source, logique intermédiaire, marts finaux), reliés par `ref`, au lieu de grosses requêtes monolithiques.

#### Dans quels langages peut-on écrire des modèles dbt ?

En SQL (avec Jinja) partout, et en Python sur Snowflake (Snowpark), Databricks (PySpark) et BigQuery (BigQuery DataFrames ou Dataproc). Le code Python s'exécute sur la plateforme de données, pas sur la machine qui lance dbt. Les modèles Python renvoient un DataFrame et servent pour la logique difficile à exprimer en SQL.

#### Qu'est-ce qu'un modèle Python dans dbt ?

Un fichier `.py` qui définit `model(dbt, session)` et renvoie un DataFrame. Il peut référencer d'autres modèles avec `dbt.ref()` et est matérialisé en table ou en modèle incrémental ; les vues et les modèles ephemeral ne sont pas possibles en Python, et un modèle Python ne peut pas référencer un modèle ephemeral.

```python
def model(dbt, session):
    dbt.config(materialized="table")
    orders = dbt.ref("stg_orders")
    return orders.groupBy("customer_id").count()
```

<!-- challenge -->

Cinq modèles de mart répètent la même jointure de 40 lignes entre commandes et paiements. Comment les restructurer ?

<!-- solution -->

Extraire la jointure dans un modèle intermédiaire (par exemple `int_orders_with_payments`) que les cinq marts référencent avec `ref()`. La logique existe une fois, et le DAG montre la dépendance partagée.

<!-- takeaways -->

- Un modèle est un `SELECT` dans un fichier.
- `ref()` construit le DAG et l'ordre d'exécution.
- Les petits modèles à but unique se réutilisent facilement.

<!-- unit: Commandes essentielles -->

<!-- goals -->

- Utiliser les commandes dbt les plus courantes.
- Expliquer ce que font `dbt build`, `dbt debug` et `dbt compile`.

<!-- concept -->

Une poignée de commandes couvre le travail quotidien. Run construit les modèles ; test les vérifie ; build fait les deux, plus seeds et snapshots, dans l'ordre du DAG, et saute ce qui dépend d'un échec. Compile produit le SQL sans l'exécuter : c'est ainsi qu'on voit ce que dbt enverra vraiment. Debug vérifie la configuration et la connexion.

Savoir quelle commande utiliser fait gagner du temps et évite de construire sur des données cassées.

<!-- example -->

```bash
dbt debug                           # config and connection OK?
dbt compile --select fct_orders     # see rendered SQL in target/compiled
dbt build --select +fct_orders      # build and test fct_orders and its parents
```

#### Quelles sont les commandes dbt les plus courantes ?

`dbt run` (construire les modèles), `dbt test` (exécuter les tests), `dbt build` (seeds, modèles, snapshots et tests dans l'ordre du DAG), `dbt seed`, `dbt snapshot`, `dbt compile`, `dbt show`, `dbt retry`, `dbt docs generate` / `dbt docs serve`, `dbt debug`, `dbt deps`, `dbt clean`, `dbt ls`, `dbt run-operation` et `dbt source freshness`. dbt v2 ajoute `dbt freshness` (sources et modèles), `dbt check` (standards du projet) et `dbt lint` (style SQL).

#### Que fait `dbt build` ?

Il exécute les seeds, les modèles, les snapshots et leurs tests dans l'ordre du DAG, en testant chaque nœud juste après sa construction. Si un test de sévérité `error` échoue, les nœuds qui en dépendent sont ignorés, pour que des données erronées ne se propagent pas. Dans dbt v2, `dbt build` exécute aussi d'abord tous les tests unitaires et évalue les contrôles du projet avant tout travail dans l'entrepôt.

#### À quoi sert `dbt debug` ?

Il vérifie l'installation, `dbt_project.yml`, `profiles.yml`, les dépendances requises comme `git` et la connexion à l'entrepôt. C'est la première commande à lancer quand rien ne fonctionne.

#### Quelle est la différence entre `dbt run` et `dbt compile` ?

`dbt compile` rend le Jinja et écrit le SQL obtenu dans `target/compiled/` sans rien construire. Il se connecte tout de même à l'entrepôt quand des modèles ont besoin d'introspection (par exemple `run_query`). `dbt run` compile et exécute, et écrit les requêtes exécutées (avec leur DDL) dans `target/run/`.

<!-- challenge -->

Un job de production lance `dbt run` puis `dbt test`. Un modèle de staging cassé a produit des doublons, et tous les modèles en aval ont été reconstruits dessus avant l'échec des tests. Que changez-vous ?

<!-- solution -->

Utiliser `dbt build`, qui teste chaque nœud juste après l'avoir construit et saute ses enfants quand un test échoue, pour que les mauvaises données ne se propagent pas.

<!-- takeaways -->

- `build` = run + test + seed + snapshot dans l'ordre du DAG.
- `compile` montre le SQL sans l'exécuter.
- `debug` vérifie configuration et connexion.

### Projets et configuration

<!-- unit: Fichiers de projet et de connexion -->

<!-- goals -->

- Décrire `dbt_project.yml`, `profiles.yml`, targets et threads.
- Garder les identifiants dans des variables d'environnement.

<!-- concept -->

Un projet dbt a deux types de configuration. Le fichier de projet voyage avec le code : nom, chemins, configurations par défaut par dossier. Le profile reste avec la personne ou la machine qui exécute dbt : quelle plateforme, quels identifiants, quelle target comme `dev` ou `prod`.

Cette séparation permet à un même code de construire dans de nombreux environnements. Les variables d'environnement la complètent en gardant les secrets hors de tous les fichiers.

<!-- example -->

```yaml
# profiles.yml
shop:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('DBT_USER') }}"
      password: "{{ env_var('DBT_PASSWORD') }}"
      database: analytics_dev
      schema: "dbt_{{ env_var('USER') }}"
      threads: 8
```

#### Qu'est-ce qu'un projet dbt ?

Un répertoire qui contient un fichier `dbt_project.yml`, ainsi que des modèles, tests, macros, seeds, snapshots, analyses et de la documentation. C'est l'unité que dbt compile et exécute, en général un dépôt Git.

#### Que contient `dbt_project.yml` ?

Le nom et la version du projet, le `profile` à utiliser, les chemins (models, seeds, macros…), les `vars` et les configurations par défaut de chaque dossier, comme `+materialized: table` pour tous les marts ou `+schema: staging`.

#### Qu'est-ce que `profiles.yml` ?

Le fichier qui contient les informations de connexion de chaque profil et target : type d'adaptateur, hôte, base de données, schéma, identifiants et threads. dbt le cherche dans le dossier indiqué par `--profiles-dir` ou `DBT_PROFILES_DIR`, puis dans le dossier du projet, puis dans `~/.dbt/`. Il contient des secrets de connexion : on le garde hors du dépôt, ou on versionne une version qui lit chaque secret avec `env_var()`.

#### Qu'est-ce qu'un target dans dbt ?

Une configuration de connexion nommée au sein d'un profil, comme `dev` et `prod`. On la choisit avec `--target`, et les modèles peuvent varier selon `target.name`.

#### Que sont les threads dans dbt ?

Le nombre maximal de nœuds que dbt construit en même temps. Les branches indépendantes du DAG s'exécutent en parallèle jusqu'à cette limite. dbt v2 gère lui-même le parallélisme sur Snowflake et Databricks, où `threads` ne sert que de plafond, et traite `threads: 0` (ou l'absence de valeur) comme « optimiser automatiquement » sur BigQuery et Redshift.

#### Comment utilise-t-on les variables d'environnement dans dbt ?

Avec `{{ env_var('DBT_PASSWORD') }}`, éventuellement avec une valeur par défaut : `{{ env_var('DBT_SCHEMA', 'dbt_dev') }}`. On s'en sert surtout dans `profiles.yml` pour les identifiants. Les variables préfixées `DBT_ENV_SECRET_` sont masquées dans les journaux et ne peuvent être utilisées que dans `profiles.yml` et `packages.yml`, pas dans les modèles.

<!-- challenge -->

Un développeur a commité `profiles.yml` avec un mot de passe de production. Que changez-vous ?

<!-- solution -->

Changer le mot de passe, le retirer de l'historique du dépôt et réécrire le profile pour lire les identifiants avec `env_var()`. En CI et en production, les injecter depuis un gestionnaire de secrets.

<!-- takeaways -->

- `dbt_project.yml` voyage avec le code.
- `profiles.yml` contient connexions et targets par environnement.
- Les identifiants viennent des variables d'environnement.

<!-- unit: Configurer les nœuds -->

<!-- goals -->

- Configurer les modèles au niveau fichier, YAML et projet.
- Sélectionner des nœuds avec tags, selectors et variables.

<!-- concept -->

La configuration va du général au particulier : valeurs par défaut par dossier dans le projet, surchargées en YAML, puis à nouveau dans le fichier du modèle. Les configs changent la façon dont dbt construit ; les properties décrivent. Garder cette distinction claire évite la plupart des questions du type « pourquoi mon réglage ne s'est-il pas appliqué ? ».

La sélection permet d'agir sur une partie du DAG : par nom, chemin, tag, état ou opérateurs de graphe. Les variables font se comporter le même code différemment selon l'exécution.

<!-- example -->

```bash
dbt build --select tag:daily
dbt build --select +fct_orders+          # parents, the model, children
dbt run --select path:models/marts --exclude tag:deprecated
dbt run --vars '{start_date: "2026-10-01"}'
```

#### Comment configure-t-on un modèle ?

À trois endroits, du plus précis au moins précis : un bloc `{{ config(...) }}` dans le fichier du modèle, un bloc `config:` dans les propriétés YAML du modèle et les réglages par dossier dans `dbt_project.yml`. Le plus précis l'emporte.

```sql
{{ config(materialized='table', schema='marts', tags=['daily']) }}
select * from {{ ref('int_orders') }}
```

#### Quelle est la différence entre configs et properties ?

Les configs contrôlent la façon dont dbt construit et gère un nœud (matérialisation, schéma, tags, meta, hooks, access). Les properties le décrivent (description, colonnes, tests, documentation). Les properties vivent dans des fichiers YAML. Les configs peuvent être en YAML sous une clé `config:`, dans le fichier du modèle ou dans `dbt_project.yml`, et se transmettent du général au particulier. Depuis dbt v1.10, des configs comme `tags`, `meta` et `access` vont sous `config:` en YAML, et dbt v2 les refuse au premier niveau. Seules les configs servent à la sélection, avec `--select config.materialized:incremental`.

#### À quoi servent les tags ?

À étiqueter des nœuds pour les sélectionner dans les commandes, par exemple `dbt run --select tag:daily`, ou les regrouper dans des jobs.

#### Comment fonctionne la sélection de nœuds ?

Avec `--select` et `--exclude`, à partir de noms, de chemins, de tags, de `source:`, `state:`, `resource_type:` et d'opérateurs de graphe : `+model` sélectionne le modèle et ses parents, `model+` le modèle et ses enfants, `@model` le modèle, ses enfants et leurs parents.

```bash
dbt build --select +fct_orders          # fct_orders et tout ce qui est en amont
dbt run --select staging.stripe         # un dossier
dbt test --select source:stripe+        # tests d'une source et de tout ce qui en dépend
```

#### Que sont les variables (`vars`) dans dbt ?

Des valeurs définies dans `dbt_project.yml` ou passées en ligne de commande (`--vars '{start_date: 2026-01-01}'`) et lues avec `{{ var('start_date') }}`, éventuellement avec une valeur par défaut : `{{ var('start_date', '2020-01-01') }}`. Les valeurs de la ligne de commande l'emportent sur le fichier du projet. Une variable sans valeur ni valeur par défaut est une erreur (dès l'analyse du projet dans dbt v2).

<!-- challenge -->

Tous les marts doivent être des tables, sauf un gros modèle qui doit être incrémental. Où placez-vous chaque config ?

<!-- solution -->

Mettre `+materialized: table` pour le dossier des marts dans `dbt_project.yml`, et surcharger avec `{{ config(materialized='incremental', unique_key=...) }}` dans le fichier du gros modèle, qui l'emporte.

<!-- takeaways -->

- Les configs descendent en cascade du projet au YAML puis au fichier.
- Les configs changent les builds ; les properties décrivent les nœuds.
- La sélection cible des parties du DAG.

<!-- unit: Structure et schémas -->

<!-- goals -->

- Organiser un projet en dossiers et en couches.
- Contrôler les noms de schémas avec `generate_schema_name`.

<!-- concept -->

Une structure de dossiers cohérente dit à chacun où vont les choses : staging par source, intermediate pour la logique partagée, marts par domaine métier. Les configs par dossier appliquent ensuite matérialisations et schémas à des couches entières.

Par défaut, dbt ajoute le schéma personnalisé au schéma de la target, ce qui empêche les développeurs d'écrire dans les schémas de production. Les équipes surchargent souvent la macro pour que la production ait des noms propres tout en isolant le développement. Analyses et commandes de nettoyage complètent l'organisation du projet.

<!-- example -->

```sql
-- macros/generate_schema_name.sql
{% macro generate_schema_name(custom_schema_name, node) -%}
  {%- if target.name == 'prod' and custom_schema_name is not none -%}
    {{ custom_schema_name | trim }}
  {%- else -%}
    {{ target.schema }}{% if custom_schema_name %}_{{ custom_schema_name | trim }}{% endif %}
  {%- endif -%}
{%- endmacro %}
```

#### Comment un projet dbt est-il généralement structuré ?

L'organisation recommandée :

```
dbt_project.yml
models/
  staging/<source>/      modèles stg_ : un par table source, nettoyage léger
  intermediate/          modèles int_ : jointures et logique métier
  marts/                 modèles fct_ et dim_ consommés par les utilisateurs
seeds/        petites données de référence en CSV
snapshots/    historique SCD de type 2
macros/       Jinja réutilisable
tests/        tests de données singuliers
analyses/     SQL compilé mais non exécuté
functions/    fonctions définies par l'utilisateur (UDF)
checks/       standards du projet vérifiés par dbt check (dbt v2)
```

#### Comment dbt choisit-il le schéma dans lequel un modèle est construit ?

Grâce à la macro `generate_schema_name`. Par défaut, un schéma personnalisé est ajouté au schéma du target (`dbt_alice_marts` en dev, `analytics_marts` en prod). Beaucoup de projets redéfinissent la macro pour utiliser le schéma personnalisé tel quel en production.

#### Qu'est-ce que la macro `generate_schema_name`, et pourquoi la redéfinir ?

Elle calcule le schéma de chaque nœud. La redéfinir permet, par exemple, d'utiliser des noms de schéma exacts en production tout en gardant un préfixe personnel en développement, pour que les développeurs ne s'écrasent pas mutuellement.

#### Que sont les analyses dans dbt ?

Des fichiers SQL du dossier `analyses/` qui sont compilés (Jinja et `ref` résolus) mais jamais exécutés par `dbt run`. Utiles pour des requêtes ponctuelles qui profitent des références de dbt.

#### Que fait `dbt clean` ?

Il supprime les dossiers listés dans `clean-targets` (en général `target/` et `dbt_packages/`). dbt v2 refuse de supprimer quoi que ce soit hors du dossier du projet ou dans des chemins de ressources comme `models/`.

<!-- challenge -->

Les modèles de production atterrissent dans des schémas comme `analytics_marts` au lieu de `marts`, et les analystes trouvent ces noms déroutants. Que changez-vous sans gêner les développeurs ?

<!-- solution -->

Surcharger `generate_schema_name` pour qu'avec la target prod le schéma personnalisé soit utilisé tel quel (`marts`), les autres targets gardant la forme préfixée (`dbt_ana_marts`) pour rester isolées.

<!-- takeaways -->

- Organisez par couche : staging, intermediate, marts.
- Par défaut, dbt ajoute les schémas personnalisés à celui de la target.
- Surchargez le nommage pour des noms de production propres.

<!-- unit: Packages et gouvernance -->

<!-- goals -->

- Installer et utiliser des packages comme `dbt_utils`.
- Gouverner les modèles publics avec access, groups et versions.

<!-- concept -->

Les packages sont des projets dbt que vous importez : tests, macros et modèles déjà écrits et éprouvés par d'autres. La plupart des projets commencent avec `dbt_utils` pour les tests et utilitaires courants.

Quand les projets grandissent et servent d'autres équipes, les modèles deviennent des interfaces. Niveaux d'accès et groupes décident qui peut référencer quoi, et les versions permettent de livrer un changement cassant comme nouvelle version pendant que les consommateurs migrent à leur rythme.

<!-- example -->

```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: [">=1.3.0", "<2.0.0"]
# models/marts/_marts.yml
models:
  - name: fct_orders
    config:
      access: public
      group: finance
    latest_version: 2
    versions: [{v: 1}, {v: 2}]
```

#### Que sont les packages, et comment les installer ?

Des projets dbt réutilisables (macros, modèles, tests) comme `dbt_utils`, `dbt_expectations` ou `codegen`. On les liste dans `packages.yml` et on lance `dbt deps`, qui les installe dans `dbt_packages/` et fige les versions résolues dans `package-lock.yml`. `dependencies.yml` peut contenir à la fois des packages et des dépendances entre projets (dbt Mesh), mais dbt v1 n'y rend pas le Jinja : les packages privés qui ont besoin d'un jeton tiré d'une variable d'environnement restent dans `packages.yml`.

#### Qu'est-ce que `dbt_utils` ?

Le package le plus utilisé, avec des tests génériques (`unique_combination_of_columns`, `expression_is_true`, `accepted_range`) et des macros (`generate_surrogate_key`, `star`, `date_spine`, `pivot`, `union_relations`).

#### Que sont l'accès aux modèles et les groupes ?

Des fonctions de gouvernance. La config `access` d'un modèle peut être `private` (référençable seulement dans son groupe), `protected` (dans le projet ou quand il est installé comme package ; la valeur par défaut) ou `public` (aussi depuis d'autres projets). Les groupes rassemblent des modèles liés sous un même responsable. dbt Labs recommande `private` pour les nouveaux modèles qui ne sont pas conçus pour être partagés.

#### Que sont les versions de modèles ?

Un moyen de publier un changement cassant d'un modèle public sous forme de nouvelle version, pendant que les consommateurs continuent d'utiliser l'ancienne jusqu'à leur migration. Chaque version vit dans son propre fichier (`fct_orders_v1.sql`, `fct_orders_v2.sql`). `ref('fct_orders', v=1)` fixe une version, et un simple `ref('fct_orders')` se résout en `latest_version`. Les anciennes versions peuvent recevoir une `deprecation_date` pour avertir les consommateurs.

<!-- challenge -->

Une autre équipe référence directement vos modèles intermédiaires, et chaque refactoring les casse. Comment poser des limites ?

<!-- solution -->

Placer vos modèles dans un group, marquer les modèles intermédiaires `private` (ou `protected`) et n'exposer en `public`, avec contrats, que les marts dont elle a besoin. Les changements cassants passent ensuite par des versions de modèle.

<!-- takeaways -->

- Les packages apportent tests et macros prêts à l'emploi.
- Access et groups définissent les interfaces des modèles.
- Les versions font cohabiter les changements cassants.

<!-- stage: Construire des modèles -->

### Sources et seeds

<!-- unit: Sources et fraîcheur -->

<!-- goals -->

- Déclarer des sources et les référencer avec `source()`.
- Tester les sources et vérifier leur fraîcheur.

<!-- concept -->

Les tables brutes chargées par d'autres outils sont les entrées de dbt. Les déclarer comme sources place leur emplacement en un seul endroit, fait partir le lignage du bon point et permet de les tester avant de construire quoi que ce soit dessus.

Les contrôles de fraîcheur répondent à une question que les tests ne posent pas : de nouvelles données sont-elles arrivées ? Les lancer en premier en production évite que les modèles se reconstruisent silencieusement sur des données périmées.

<!-- example -->

```yaml
sources:
  - name: shop
    database: raw
    schema: shop
    config:
      loaded_at_field: _loaded_at
      freshness:
        warn_after: {count: 6, period: hour}
        error_after: {count: 24, period: hour}
    tables:
      - name: orders
        columns:
          - name: id
            data_tests: [unique, not_null]
```

#### Que sont les sources dans dbt ?

Des déclarations, en YAML, des tables brutes chargées dans l'entrepôt par d'autres outils. Les modèles les lisent avec `{{ source('stripe', 'payments') }}` au lieu de noms de tables écrits en dur, ce qui enregistre le lignage, permet des tests et de la documentation sur les données brutes et active les contrôles de fraîcheur.

```yaml
sources:
  - name: stripe
    database: raw
    schema: stripe
    tables:
      - name: payments
        config:
          loaded_at_field: _loaded_at
          freshness:
            warn_after: {count: 12, period: hour}
            error_after: {count: 24, period: hour}
```

#### Pourquoi utiliser `source()` plutôt que d'écrire le nom de la table ?

L'emplacement de la table est défini à un seul endroit, le lignage commence à la source dans le DAG, les sources peuvent être sélectionnées (`source:stripe+`) et `dbt source freshness` peut les contrôler.

#### Qu'est-ce que la fraîcheur des sources (source freshness) ?

Un contrôle qui compare le chargement le plus récent d'une source à l'heure actuelle et avertit ou échoue quand les données sont plus anciennes que les seuils `warn_after` et `error_after`. dbt lit le maximum de `loaded_at_field` (ou le résultat d'une `loaded_at_query` personnalisée), ou utilise les métadonnées de l'entrepôt quand aucun des deux n'est défini et que la plateforme le permet. Depuis dbt v1.10, `freshness` et `loaded_at_field` vont sous `config:`, au niveau de la source comme valeurs par défaut ou par table pour les remplacer.

#### Peut-on tester les sources ?

Oui, on déclare des tests génériques sur les colonnes des sources exactement comme sur les modèles, ce qui détecte les problèmes des données brutes avant qu'ils n'atteignent les modèles.

#### À quoi sert `dbt source freshness` en production ?

À détecter une ingestion cassée ou en retard avant que les modèles ne tournent sur des données périmées, souvent en première étape d'un job planifié. Ses résultats sont écrits dans `target/sources.json`.

#### Qu'est-ce que la fraîcheur des modèles, et que fait `dbt freshness` ?

dbt v2 étend la fraîcheur aux modèles : on définit `warn_after` et `error_after` (et un `loaded_at_field` ou `loaded_at_query`) dans la config d'un modèle, et `dbt freshness` vérifie en une seule commande toutes les sources et tous les modèles dont la fraîcheur est configurée, puis écrit `target/freshness.json`. `dbt source freshness` fonctionne toujours, mais ne vérifie que les sources. La fraîcheur des modèles est utile sur les modèles que les consommateurs interrogent directement, où « le job a réussi » ne prouve pas que les données sont récentes.

#### Quelle est la différence entre `ref()` et `source()` ?

`ref()` pointe vers un autre nœud dbt (modèle, seed, snapshot) et crée une dépendance que le DAG utilise pour ordonner les exécutions. `source()` pointe vers des données brutes chargées hors de dbt. Les deux se résolvent en nom de table complet pour le target courant.

<!-- challenge -->

Un job d'ingestion a échoué pendant deux jours, et les tableaux de bord affichaient des chiffres plats sans que personne ne le remarque. Quelle fonction de dbt l'aurait détecté ?

<!-- solution -->

La source freshness sur les tables brutes avec des seuils `error_after`, lancée en première étape du job de production (avec alerte en cas d'échec), pour que le job s'arrête et que l'équipe soit prévenue.

<!-- takeaways -->

- Les sources déclarent les entrées brutes en un seul endroit.
- `source()` pour les tables brutes ; `ref()` pour les nœuds dbt.
- Les contrôles de fraîcheur repèrent une ingestion en retard ou cassée.

<!-- unit: Staging et couches -->

<!-- goals -->

- Écrire les modèles de staging comme seuls consommateurs des sources.
- Expliquer les couches staging, intermediate et marts entre environnements.

<!-- concept -->

Les modèles de staging sont le point d'entrée propre : un par table source, avec renommages, casts et nettoyage léger, sans jointure ni logique métier. Si seul le staging lit les sources, un changement de source ne touche qu'un fichier.

Les couches s'appuient là-dessus : les modèles intermédiaires portent jointures et logique réutilisables, les marts servent les consommateurs. Comme `ref()` se résout selon la target courante, les mêmes couches se construisent dans le schéma d'un développeur ou en production sans changer le code.

<!-- example -->

```sql
-- models/staging/shop/stg_shop__orders.sql
select
    id::bigint            as order_id,
    customer_id::bigint   as customer_id,
    lower(status)         as status,
    created_at::timestamp as ordered_at
from {{ source('shop', 'orders') }}
```

#### Qu'est-ce qu'un modèle de staging ?

La première couche au-dessus d'une source : un modèle par table source, avec des transformations légères (renommage, conversion de types, nettoyage de base, dédoublonnage). Tout ce qui suit référence les modèles de staging, pas directement les sources.

#### Pourquoi seuls les modèles de staging devraient-ils référencer les sources ?

Pour que chaque table brute soit nettoyée une seule fois, à un seul endroit. Si la source change, seul son modèle de staging doit être modifié.

#### Qu'est-ce que l'organisation en couches « staging, intermediate, marts » ?

Une structure courante : staging nettoie chaque source, intermediate contient des jointures et une logique métier réutilisables, les marts sont les tables de faits et de dimensions finales (ou des tables larges) consommées par la BI et les analystes.

#### En quoi `ref()` se résout-il selon l'environnement ?

En la relation dans la base et le schéma du target courant : le même code construit dans le schéma d'un développeur en dev et dans les schémas de production en prod.

#### dbt peut-il travailler avec différentes sources de données et différents entrepôts ?

dbt travaille avec une plateforme de données par target, via son adaptateur, et transforme des données déjà présentes sur cette plateforme. Il n'extrait pas depuis les systèmes sources. Les plateformes capables d'interroger des données externes (tables externes Snowflake, requêtes fédérées BigQuery, catalogues Databricks et Trino) permettent à dbt de transformer des données de plusieurs origines via l'entrepôt.

<!-- challenge -->

Une source renomme `created_at` en `created_ts`, et neuf modèles cassent. Comment des couches auraient-elles limité les dégâts ?

<!-- solution -->

Si seul `stg_shop__orders` lisait la source, la correction tiendrait en une ligne (`created_ts as ordered_at`) ; tous les modèles en aval utilisent le nom de colonne du staging et restent inchangés.

<!-- takeaways -->

- Staging : un modèle par table source, nettoyage léger seulement.
- Seul le staging lit les sources.
- `ref()` se résout par target : les couches marchent partout.

<!-- unit: Seeds -->

<!-- goals -->

- Décider quand les seeds conviennent ou non.
- Fixer les types de colonnes des seeds et recharger ceux qui changent.

<!-- concept -->

Les seeds chargent dans l'entrepôt de petits fichiers CSV du dépôt. Ils sont idéaux pour les données de référence statiques qui ont leur place dans la gestion de versions, comme les codes pays ou les tables de correspondance, relues comme du code.

Ils ne conviennent pas à ce qui est volumineux, sensible ou change souvent ; cela relève de l'ingestion. Les types doivent être fixés explicitement, car l'inférence devine, et les changements de colonnes exigent un full refresh.

<!-- example -->

```yaml
seeds:
  shop:
    country_codes:
      +column_types:
        iso_code: varchar(2)
        dial_code: varchar(6)
```
```bash
dbt seed --select country_codes --full-refresh
```

#### Qu'est-ce qu'un seed ?

Un fichier CSV du dossier `seeds/` que `dbt seed` charge dans l'entrepôt sous forme de table. Les modèles le référencent avec `ref()` comme n'importe quel modèle.

#### Quand utiliser des seeds, et quand ne pas le faire ?

Pour de petites données de référence statiques, qui changent rarement et ont leur place dans la gestion de versions : codes pays, tables de correspondance, jeux de test. Pas pour des données volumineuses ou qui changent souvent, ni pour des données qui devraient venir d'un système source.

#### Comment fixer les types de colonnes d'un seed ?

Avec la config `column_types`, dans `dbt_project.yml` ou dans les propriétés YAML du seed ; sinon dbt infère chaque type à partir des valeurs :

```yaml
seeds:
  my_project:
    country_codes:
      +column_types:
        code: varchar(2)
```

#### Comment recharger un seed dont les colonnes ont changé ?

Avec `dbt seed --full-refresh`, qui supprime et recrée la table au lieu de la vider puis d'insérer.

<!-- challenge -->

Une équipe charge en seed un export quotidien de 300 Mo de prix produits. Que suggérez-vous ?

<!-- solution -->

Le déplacer dans la couche d'ingestion (un chargeur ou connecteur vers une table brute déclarée comme source). Les seeds servent aux petites données de référence statiques versionnées dans Git, pas aux flux quotidiens.

<!-- takeaways -->

- Les seeds chargent de petits CSV statiques depuis Git.
- Fixez explicitement les types de colonnes.
- Des colonnes modifiées exigent `--full-refresh`.

### Modèles et matérialisations

<!-- unit: Construire des modèles et matérialisations -->

<!-- goals -->

- Créer des modèles et laisser `ref()` gérer les dépendances.
- Choisir entre les matérialisations view, table, ephemeral et incremental.

<!-- concept -->

Écrire un modèle, c'est écrire une requête ; la matérialisation décide ce que dbt en fait. Une vue ne stocke rien et recalcule à chaque lecture. Une table stocke les résultats et recalcule à chaque build. Les modèles ephemeral sont insérés comme CTE dans leurs enfants. Les incrémentaux n'ajoutent que les nouvelles données à chaque exécution.

Le choix arbitre entre coût de build, coût de requête et fraîcheur, et un projet les utilise généralement toutes selon la couche. Quand aucune ne convient, des matérialisations personnalisées sont possibles, mais rarement nécessaires.

<!-- example -->

| Couche | Matérialisation type | Pourquoi |
|---|---|---|
| Staging | View | Bon marché, toujours à jour |
| Intermediate | Ephemeral ou view | Logique réutilisée, pas d'objet en plus |
| Marts | Table | Rapide pour la BI |
| Gros faits | Incremental | Ne traite que les nouvelles lignes |

#### Comment crée-t-on un modèle dbt ?

On crée un fichier `.sql` sous `models/` contenant un `SELECT` qui référence les nœuds amont avec `ref` ou `source`, on ajoute éventuellement un bloc `config` et une entrée YAML avec description et tests, puis on lance `dbt run --select my_model`.

```sql
-- models/staging/stripe/stg_stripe__payments.sql
select
    id as payment_id,
    order_id,
    amount / 100.0 as amount_eur,
    created::date as payment_date
from {{ source('stripe', 'payments') }}
where status = 'succeeded'
```

#### Comment dbt gère-t-il les dépendances entre modèles ?

Grâce à `ref()`. Quand un modèle appelle `{{ ref('stg_orders') }}`, dbt enregistre l'arête dans le DAG, construit d'abord `stg_orders` et remplace l'appel par le bon nom de table. On ne déclare jamais soi-même l'ordre d'exécution.

#### Quels sont les types de matérialisation dans dbt ?

- **view** (par défaut) : une vue est créée, rien n'est stocké et la requête s'exécute à la lecture.
- **table** : le résultat est stocké et reconstruit à chaque exécution.
- **incremental** : lors des exécutions suivantes, seules les lignes nouvelles ou modifiées sont insérées ou fusionnées.
- **ephemeral** : rien n'est construit, le modèle est intégré en CTE dans les modèles en aval.
- **materialized_view** : une vue matérialisée de la base, rafraîchie par la plateforme elle-même, là où elle est prise en charge. L'équivalent sur Snowflake est la matérialisation `dynamic_table`, propre à son adaptateur.

Les snapshots et les seeds sont des types de ressources distincts, avec leur propre comportement.

#### Quand utiliser une vue plutôt qu'une table ?

Les vues sont peu coûteuses à construire et toujours à jour : elles conviennent au staging et aux transformations légères. Les tables sont plus rapides à interroger : elles conviennent aux marts utilisés par la BI et aux modèles coûteux à calculer ou très interrogés.

#### Quand utiliser un modèle ephemeral ?

Pour une logique légère et réutilisable qu'on ne veut pas voir comme un objet distinct dans l'entrepôt. Les multiplier complique le débogage, car on ne peut pas les interroger directement.

#### Comment créer une matérialisation personnalisée dans dbt ?

Avec un bloc `{% materialization name, adapter='default' %}` dans un fichier de macros. En général, il récupère la relation cible, exécute les pre-hooks, construit le SQL avec `{% call statement('main') %}`, gère les relations existantes, exécute les post-hooks et renvoie `{'relations': [target_relation]}`. Les matérialisations personnalisées sont rares : les matérialisations intégrées et les stratégies incrémentales couvrent presque tous les besoins.

<!-- challenge -->

Un tableau de bord interroge un mart construit en vue sur quatre autres vues, et chaque rafraîchissement prend deux minutes. Que changez-vous ?

<!-- solution -->

Matérialiser le mart en table (et peut-être un modèle intermédiaire coûteux), pour que le travail ait lieu une fois par build et non à chaque requête du tableau de bord.

<!-- takeaways -->

- La matérialisation décide du stockage d'un modèle.
- Les vues sont bon marché à construire ; les tables, à lire.
- Choisissez selon la couche et l'usage.

<!-- unit: Marts, nommage et grain -->

<!-- goals -->

- Concevoir des marts de faits et de dimensions au grain déclaré.
- Appliquer conventions de nommage, clés de substitution, alias et modèles désactivés.

<!-- concept -->

Les marts sont les modèles qu'utilisent les gens : ils suivent la conception dimensionnelle, avec des faits à un grain déclaré et des dimensions pour le contexte. Énoncer le grain dans la description et le tester par un test d'unicité attrape le bug de modélisation le plus courant, une jointure qui multiplie les lignes.

Les conventions rendent un projet navigable : préfixes par couche, clés de substitution générées de façon cohérente, alias quand le nom dans l'entrepôt doit différer du fichier, et modèles désactivés pour du code qui ne doit pas tourner sur une plateforme.

<!-- example -->

```sql
-- models/marts/fct_order_lines.sql   grain: one row per order line
select
    {{ dbt_utils.generate_surrogate_key(['order_id', 'line_number']) }} as order_line_key,
    order_id, line_number, product_id, quantity, net_amount
from {{ ref('int_order_lines_enriched') }}
```

#### Qu'est-ce qu'un modèle mart ?

Un modèle final construit pour les consommateurs, en général une table de faits (`fct_orders`) ou de dimension (`dim_customers`), ou une table large dénormalisée pour une équipe donnée.

#### Quelles conventions de nommage sont courantes dans dbt ?

`stg_<source>__<table>` pour le staging, `int_<entité>_<verbe>` pour l'intermédiaire, `fct_` et `dim_` pour les marts, des noms d'entité au pluriel, le snake_case, et un modèle par fichier portant le nom de la relation.

#### Quelle est la différence entre un modèle de faits et un modèle de dimension ?

Un modèle de faits contient des événements ou des mesures à une granularité déclarée (commandes, paiements), avec des clés étrangères et des mesures numériques. Une dimension contient les attributs descriptifs des entités (clients, produits) qui servent à filtrer et regrouper les faits.

#### Comment générer une clé de substitution dans dbt ?

Avec `dbt_utils.generate_surrogate_key`, qui calcule le hachage de la concaténation des colonnes (en traitant les NULL de façon cohérente) :

```sql
select
    {{ dbt_utils.generate_surrogate_key(['order_id', 'line_number']) }} as order_line_key,
    *
from {{ ref('stg_order_lines') }}
```

#### Qu'est-ce que la granularité d'un modèle, et pourquoi est-elle importante ?

Ce que représente une ligne (une commande, une ligne de commande, un client par jour). La déclarer, et la vérifier par un test d'unicité, évite les doublons et les agrégations fausses en aval.

#### Qu'est-ce que la configuration `alias` ?

Elle fixe le nom de la relation dans l'entrepôt indépendamment du nom du fichier du modèle.

#### Qu'est-ce qu'un modèle désactivé ?

Un modèle avec `enabled: false`. dbt l'ignore, ce qui est utile pour des modèles propres à une plateforme ou en cours de développement.

<!-- challenge -->

`fct_orders` compte soudain plus de lignes qu'il n'y a de commandes. Quel test l'aurait détecté, et quelle en est la cause habituelle ?

<!-- solution -->

Un test `unique` sur `order_id` (le grain déclaré). La cause habituelle est une jointure avec une table à plusieurs lignes par commande, comme paiements ou expéditions, sans l'avoir agrégée au préalable.

<!-- takeaways -->

- Les marts sont des faits et dimensions au grain déclaré.
- Testez le grain par un test d'unicité.
- Noms et clés cohérents rendent le projet navigable.

<!-- unit: Hooks, contrats et contraintes -->

<!-- goals -->

- Exécuter du SQL autour des modèles avec des hooks et `{{ this }}`.
- Imposer des schémas avec contrats de modèle et contraintes.

<!-- concept -->

Les hooks exécutent du SQL supplémentaire avant ou après un modèle ou une exécution entière : grants, insertions d'audit, commandes de maintenance. `{{ this }}` désigne la relation du modèle lui-même, dont ont besoin les hooks et la logique incrémentale.

Les contrats vont dans l'autre sens : au lieu d'ajouter des actions, ils ajoutent des garanties. Avec un contrat imposé, colonnes et types du modèle doivent correspondre à la déclaration, si bien qu'un refactoring ne peut pas changer en silence l'interface dont dépendent les consommateurs. Les contraintes ajoutent des règles au niveau de la base là où la plateforme les supporte.

<!-- example -->

```yaml
models:
  - name: dim_customer
    config:
      contract: {enforced: true}
      post_hook: "grant select on {{ this }} to role reporting"
    columns:
      - name: customer_id
        data_type: bigint
        constraints: [{type: not_null}, {type: primary_key}]
      - name: segment
        data_type: varchar
```

#### Que sont les hooks ?

Du SQL exécuté à des moments précis : `pre-hook` et `post-hook` autour d'un modèle, `on-run-start` et `on-run-end` autour de toute l'invocation. Usages : accorder des privilèges, créer des index ou journaliser les exécutions.

#### Que sont les pre-hooks et les post-hooks ?

Un `pre-hook` exécute du SQL juste avant la construction d'un modèle, un `post-hook` juste après, dans la même exécution. Par exemple :

```sql
{{ config(post_hook="grant select on {{ this }} to role reporter") }}
```

#### À quoi fait référence `{{ this }}` ?

À la relation (base.schéma.table) du modèle en cours de construction. On l'utilise dans les hooks et dans les modèles incrémentaux pour interroger la table existante.

#### Que sont les contrats de modèle ?

Une configuration `contract: {enforced: true}` avec le nom et le type de chaque colonne déclarés (et des contraintes là où elles sont prises en charge). Avant la construction, dbt fait une vérification préalable : la requête du modèle doit renvoyer exactement ces colonnes et ces types, dans n'importe quel ordre, sinon la construction échoue. Cela protège les consommateurs des changements de schéma. Les contrats s'appliquent aux modèles SQL matérialisés en tables, en vues (noms et types seulement, sans contraintes) ou en modèles incrémentaux avec `on_schema_change` à `append_new_columns` ou `fail`.

#### Que sont les contraintes (constraints) dans dbt ?

Des déclarations comme `not_null`, `unique`, `primary_key`, `foreign_key` et `check` sur des modèles sous contrat. dbt les ajoute au DDL du `create table` là où la plateforme les prend en charge. Le support varie : la plupart des plateformes analytiques appliquent `not_null`, mais n'enregistrent les clés primaires, les clés étrangères et `unique` que comme métadonnées (la `primary_key` de Snowflake, par exemple) : les tests restent nécessaires pour l'unicité et les relations.

<!-- challenge -->

Un développeur fait passer une colonne de `bigint` à `varchar` dans un modèle public, et une application en aval casse une semaine plus tard. Qu'est-ce qui l'aurait arrêté au build ?

<!-- solution -->

Un contrat de modèle imposé déclarant `bigint` pour cette colonne : le build échoue quand le type produit ne correspond pas, avant que quoi que ce soit n'atteigne la production.

<!-- takeaways -->

- Les hooks exécutent du SQL avant ou après modèles et exécutions.
- `{{ this }}` est la relation du modèle lui-même.
- Les contrats font des noms et types de colonnes une interface imposée.

<!-- unit: Exécuter les modèles et dépanner -->

<!-- goals -->

- Utiliser full refresh, defer, clone, show et retry.
- Corriger « relation does not exist » et planifier les rafraîchissements de données.

<!-- concept -->

Le travail quotidien demande plus que `run`. Le full refresh reconstruit les modèles incrémentaux de zéro. Defer et clone permettent de ne construire que ce que vous avez modifié, en lisant le reste depuis la production. Show prévisualise les résultats sans construire ; retry ne relance que ce qui a échoué.

Beaucoup d'erreurs viennent des environnements plutôt que du SQL : un parent jamais construit dans votre schéma, une faute de frappe dans une source, des permissions manquantes. Connaître ces outils les résout généralement en quelques minutes.

<!-- example -->

```bash
dbt build --select state:modified+ --defer --state prod-artifacts/   # build only my changes
dbt show --select fct_orders --limit 10                              # preview
dbt retry                                                            # rerun failed nodes only
```

#### Quelle est la différence entre `dbt run --full-refresh` et une exécution normale ?

`--full-refresh` reconstruit entièrement les modèles incrémentaux et supprime puis recharge les seeds, au lieu de ne traiter que les nouvelles données. Les modèles avec `full_refresh: false` l'ignorent, et les snapshots l'ignorent toujours et s'exécutent normalement.

#### Que fait l'option `--defer` ?

Avec `--state` pointant vers les artefacts de production, elle fait résoudre `ref()` vers les relations de production pour les modèles que vous n'avez pas construits dans votre environnement : on peut exécuter un modèle en dev sans reconstruire tous ses parents.

#### Qu'est-ce que `dbt clone` ?

Une commande qui copie les nœuds sélectionnés depuis un état enregistré (par exemple les artefacts de production passés avec `--state`) vers le target courant. Sur les plateformes qui proposent le clonage sans copie (Snowflake, Databricks, BigQuery), elle crée des clones des tables ; ailleurs, elle crée des vues qui pointent vers l'original. Elle accélère la préparation des environnements de développement et de CI et sert aux déploiements bleu-vert.

#### Qu'est-ce que `dbt show` ?

Une commande qui compile un modèle, un test ou une analyse (ou une requête en ligne avec `--inline`), l'exécute et affiche un aperçu des résultats sans rien matérialiser : `dbt show --select stg_orders --limit 10`.

#### Qu'est-ce que `dbt retry` ?

Elle relance l'invocation précédente à partir du point d'échec : les nœuds qui ont échoué ou ont été ignorés, avec les mêmes options. Si la commande précédente a échoué avant l'exécution du moindre nœud (par exemple sur une erreur de connexion), il n'y a rien à relancer.

#### Comment traiter l'erreur « relation does not exist » dans dbt ?

Causes fréquentes : une table référencée n'a jamais été construite dans le target courant (lancez le parent ou utilisez `--defer`), le nom de table est écrit en dur au lieu d'utiliser `ref`/`source` (la dépendance n'est donc pas connue et l'ordre est faux), la définition de la source pointe vers la mauvaise base ou le mauvais schéma, l'utilisateur n'a pas le droit de voir l'objet, ou l'identifiant a un problème de guillemets ou de casse. Lancer `dbt compile` et lire le SQL dans `target/compiled/` montre en général quel nom est faux.

#### Qu'est-ce qu'un rafraîchissement des données (data refresh) ?

Mettre à jour les tables de l'entrepôt pour qu'elles reflètent les dernières données sources : un `dbt build` planifié qui reconstruit les tables, traite les nouvelles lignes des modèles incrémentaux et capture les changements dans les snapshots. Sa fréquence dépend de la fraîcheur attendue par les consommateurs et du rythme de chargement des sources.

<!-- challenge -->

Un développeur modifie un mart et lance `dbt run --select my_mart` dans son schéma de dev. Cela échoue avec « relation does not exist » pour un modèle parent. Donnez deux façons de corriger.

<!-- solution -->

Construire aussi les parents (`--select +my_mart`), ou utiliser `--defer --state` avec les artefacts de production pour que les parents non construits se résolvent vers les relations de production (ou les copier en dev avec `dbt clone`).

<!-- takeaways -->

- Le full refresh reconstruit les modèles incrémentaux.
- Defer et clone réutilisent la production pour les parents inchangés.
- Show prévisualise ; retry relance les échecs.

### Jinja et macros

<!-- unit: Bases de Jinja -->

<!-- goals -->

- Utiliser expressions, instructions, variables et filtres Jinja dans les modèles.
- Adapter le SQL à la target et garder le SQL compilé propre.

<!-- concept -->

Jinja fait des fichiers SQL des modèles de texte. Les expressions insèrent des valeurs, les instructions ajoutent boucles et conditions, et les commentaires disparaissent à la compilation. Avec variables et filtres, du SQL répétitif, comme une colonne par moyen de paiement, devient une boucle sur une liste.

La variable `target` permet d'adapter le code à l'environnement, par exemple en échantillonnant les données en développement. Le contrôle des espaces garde le SQL compilé lisible, ce qui compte car c'est lui que l'on débogue.

<!-- example -->

```sql
{% set methods = ['card', 'paypal', 'bank_transfer'] %}
select
    order_id,
    {%- for m in methods %}
    sum(case when method = '{{ m }}' then amount end) as {{ m }}_amount{{ "," if not loop.last }}
    {%- endfor %}
from {{ ref('stg_shop__payments') }}
{% if target.name == 'dev' %} where created_at >= current_date - 30 {% endif %}
group by 1
```

#### Comment utiliser Jinja pour améliorer son code SQL ?

Jinja ajoute du contrôle de flux et de la réutilisation : des boucles pour générer des colonnes répétitives, des blocs `if` pour la logique propre à un environnement, des variables pour les valeurs configurables et des macros pour partager de la logique entre modèles. Restez lisible : quand Jinja domine un modèle, une macro ou une autre conception est souvent préférable.

```sql
select
    order_id,
    {% for method in ['card', 'paypal', 'transfer'] %}
    sum(case when payment_method = '{{ method }}' then amount else 0 end) as {{ method }}_amount
    {%- if not loop.last %},{% endif %}
    {% endfor %}
from {{ ref('stg_payments') }}
group by 1
```

#### Quelle est la différence entre `{{ }}`, `{% %}` et `{# #}` ?

`{{ }}` affiche une expression, `{% %}` exécute une instruction (if, for, set, macro, call), et `{# #}` est un commentaire qui n'apparaît pas dans le SQL compilé.

#### Que fait le `-` dans `{%-` ou `-%}` ?

Il supprime les espaces avant ou après la balise, pour garder un SQL compilé propre.

#### Comment définir une variable dans un modèle ?

Avec `{% set %}`, par exemple `{% set payment_methods = ['card', 'paypal'] %}`, puis on l'utilise dans des boucles ou des expressions.

#### Que sont les filtres Jinja ? Donnez des exemples.

Des fonctions appliquées avec `|`, comme `{{ name | upper }}`, `{{ columns | join(', ') }}` ou `{{ value | default('n/a') }}`.

#### Qu'est-ce que la variable `target` dans Jinja ?

Des informations sur la connexion courante : `target.name`, `target.schema`, `target.type`, `target.threads`. On s'en sert souvent pour limiter les données en développement :

```sql
{% if target.name == 'dev' %} where created_at >= dateadd(day, -3, current_date) {% endif %}
```

<!-- challenge -->

Un modèle a 12 lignes `case when` presque identiques, une par pays, et un nouveau pays implique de modifier le SQL. Comment le piloter par les données ?

<!-- solution -->

Lire la liste des pays depuis une variable, un seed ou `run_query` et la parcourir avec `{% for %}` pour générer les colonnes. Un nouveau pays ne change alors que la liste.

<!-- takeaways -->

- Jinja ajoute boucles, conditions et variables au SQL.
- `target` adapte le code à l'environnement.
- Le contrôle des espaces garde le SQL compilé lisible.

<!-- unit: Écrire des macros -->

<!-- goals -->

- Écrire des macros avec arguments, valeurs par défaut et valeurs de retour.
- Lancer des macros en opérations, les déboguer avec `log()` et savoir quand une UDF convient mieux.

<!-- concept -->

Les macros sont des fonctions pour le SQL : une logique écrite une fois et appelée depuis de nombreux modèles. Elles prennent des arguments avec valeurs par défaut, peuvent lire la config d'un modèle et peuvent renvoyer des valeurs plutôt que du texte quand une autre macro a besoin de données et non de SQL.

Certaines macros ne tournent jamais pendant un build. Run-operation les appelle directement pour des tâches d'administration, comme accorder des permissions ou nettoyer d'anciens schémas, et la journalisation aide à suivre ce qu'elles font. Quand la logique doit aussi pouvoir être appelée hors de dbt, le meilleur outil est une fonction définie par l'utilisateur que dbt crée dans l'entrepôt.

<!-- example -->

```sql
-- macros/cents_to_currency.sql
{% macro cents_to_currency(column, scale=2) %}
    round({{ column }} / 100.0, {{ scale }})
{% endmacro %}

-- usage in a model
select order_id, {{ cents_to_currency('amount_cents') }} as amount from {{ ref('stg_shop__payments') }}
```

#### Que sont les macros dans dbt, et comment les exécuter ?

Des morceaux de Jinja réutilisables (qui génèrent souvent du SQL), définis avec `{% macro name(args) %}...{% endmacro %}` dans le dossier `macros/`. On les appelle dans des modèles, des tests ou des hooks avec `{{ name(args) }}`, ou on les exécute directement avec `dbt run-operation name --args '{...}'`.

#### Comment écrire une macro avec un argument par défaut ?

```sql
{% macro cents_to_euros(column, scale=2) %}
    round({{ column }} / 100.0, {{ scale }})
{% endmacro %}
```

Appelée avec `{{ cents_to_euros('amount') }}`.

#### Que fait `return()` dans une macro ?

Il renvoie un objet Python (liste, dictionnaire, nombre) au lieu de texte rendu, pour qu'une autre macro puisse utiliser la valeur.

#### À quoi sert `log()` dans les macros ?

À afficher des messages dans la console ou le fichier de journal pendant la compilation, pour déboguer : `{{ log("value: " ~ my_var, info=true) }}`.

#### Qu'est-ce que l'objet `config` dans Jinja ?

Il lit la configuration d'un modèle à l'intérieur des macros et des matérialisations : `config.get('unique_key')` renvoie une valeur ou une valeur par défaut, et `config.require('unique_key')` échoue si elle manque. Les clés personnalisées rangées dans `meta` se lisent avec `config.meta_get('owner')` ou `config.meta_require('owner')`, pas avec `config.get`.

#### À quoi sert `dbt run-operation` ?

À exécuter une macro en dehors de la construction, pour des tâches d'administration : accorder des droits, supprimer d'anciens schémas, charger des données ou générer du code avec le package `codegen`.

#### Quand utiliser une fonction définie par l'utilisateur (UDF) plutôt qu'une macro ?

Une macro génère du texte SQL à la compilation et n'existe que dans dbt. Une UDF, définie dans un fichier SQL ou Python sous `functions/` et appelée avec `{{ function('name') }}`, est créée comme une vraie fonction dans l'entrepôt avant les modèles qui l'utilisent : les outils de BI et les notebooks peuvent donc l'appeler aussi. Utilisez une UDF pour une logique réutilisable ligne par ligne qui doit être partagée hors de dbt ; utilisez une macro pour générer du SQL, l'adapter à chaque plateforme ou produire du DDL. Les UDF nécessitent dbt v1.11+ ou v2 sur des plateformes comme Snowflake, BigQuery, Databricks et Redshift.

<!-- challenge -->

Chaque mois, quelqu'un supprime à la main les schémas de développement de plus de 30 jours. Comment l'automatiser avec dbt ?

<!-- solution -->

Écrire une macro qui interroge l'information schema pour trouver les schémas de dev, filtre par âge ou motif de nom et les supprime, puis planifier `dbt run-operation drop_old_dev_schemas` dans l'orchestrateur.

<!-- takeaways -->

- Les macros sont des fonctions réutilisables qui génèrent du SQL.
- `return()` passe des données entre macros.
- `run-operation` lance des macros hors des builds.

<!-- unit: Introspection à la compilation -->

<!-- goals -->

- Interroger l'entrepôt et le graphe du projet pendant la compilation.
- Écrire des macros spécifiques à un adapter et surcharger les macros intégrées.

<!-- concept -->

Certains SQL ne peuvent s'écrire qu'une fois une information connue : les valeurs distinctes d'une colonne, les colonnes d'une table, la plateforme utilisée. dbt peut interroger l'entrepôt pendant la compilation et lire son propre graphe de projet, mais seulement quand il exécute réellement, pas pendant le parsing du projet.

Le dispatch choisit l'implémentation d'une macro selon la plateforme, ce qui permet aux packages de fonctionner partout, et toute macro intégrée peut être surchargée en en définissant une du même nom.

<!-- example -->

```sql
{% set statuses_query %}select distinct status from {{ ref('stg_shop__orders') }}{% endset %}
{% if execute %}
  {% set statuses = run_query(statuses_query).columns[0].values() %}
{% else %}
  {% set statuses = [] %}
{% endif %}
```

#### Que fait `run_query` ?

Elle exécute une requête pendant la compilation et renvoie le résultat sous forme de table agate, par exemple pour construire une liste de valeurs distinctes utilisée dans une boucle. Elle ne renvoie des données qu'à l'exécution, d'où la garde habituelle `{% if execute %}`.

#### Qu'est-ce que la variable `execute` ?

Un booléen qui vaut false pendant que dbt analyse le projet et true quand il compile ou exécute les nœuds. Le code qui dépend de résultats de requêtes doit être placé dans `{% if execute %}`, car pendant l'analyse les requêtes ne renvoient rien et les relations référencées peuvent ne pas encore exister.

#### Que sont les variables de contexte `graph` et `model` ?

`graph` expose le projet analysé (tous les nœuds et leurs métadonnées), et `model` le nœud courant, que les macros peuvent inspecter, par exemple pour générer de la documentation ou des audits.

#### Qu'est-ce qu'`adapter.dispatch` ?

Un mécanisme pour implémenter une macro différemment selon la base, afin que les packages fonctionnent avec plusieurs adaptateurs : dbt choisit `snowflake__my_macro`, `bigquery__my_macro` ou `default__my_macro` selon l'adaptateur.

#### Comment redéfinir une macro intégrée de dbt ?

En définissant une macro du même nom dans le projet, par exemple `generate_schema_name` ou `generate_alias_name`. La version du projet a priorité sur celle fournie par dbt.

<!-- challenge -->

Un modèle utilisant `run_query` échoue pendant `dbt parse` avec une erreur de relation manquante. Pourquoi, et quelle est la correction ?

<!-- solution -->

Le Jinja est aussi rendu pendant le parsing, quand les relations peuvent ne pas exister et que les résultats des requêtes ne sont pas disponibles. Encadrer le `run_query` par `{% if execute %}` et fournir sinon une valeur par défaut.

<!-- takeaways -->

- `run_query` lit l'entrepôt à la compilation.
- Protégez les requêtes avec `execute`.
- Dispatch et surcharges adaptent les macros par plateforme.

<!-- unit: Packages et sobriété -->

<!-- goals -->

- Utiliser des macros utilitaires comme `codegen` et `dbt_utils.star`.
- Éviter la sur-ingénierie en Jinja.

<!-- concept -->

Les macros toutes faites évitent beaucoup de saisie : générer le YAML des sources et les modèles de staging, lister les colonnes sauf quelques-unes. Elles méritent d'être connues avant d'écrire les vôtres.

Le risque inverse est bien réel. Un SQL très templatisé est difficile à lire, relire et déboguer, car le code visible n'est pas celui qui s'exécute. Du SQL simple d'abord, une macro seulement quand la logique se répète vraiment ou doit varier selon la plateforme : c'est ce qui garde un projet maintenable.

<!-- example -->

```bash
dbt run-operation generate_source --args '{"schema_name": "shop", "generate_columns": true}'
```
```sql
select {{ dbt_utils.star(from=ref('stg_shop__customers'), except=['_loaded_at', 'raw_payload']) }}
from {{ ref('stg_shop__customers') }}
```

#### Qu'est-ce que le package `codegen` ?

Un package de macros qui génèrent le YAML et le SQL répétitifs, comme les définitions de sources à partir d'un schéma ou un modèle de staging à partir d'une table source.

#### Qu'est-ce que la macro `star` de dbt_utils ?

`{{ dbt_utils.star(ref('model'), except=['col']) }}` génère la liste des colonnes d'une relation, moins certaines, pour éviter `select *` sans saisir chaque colonne.

#### Comment éviter de trop complexifier le code avec Jinja ?

Écrire d'abord du SQL simple, n'extraire une macro que lorsque la logique se répète ou doit varier selon l'adaptateur, documenter les arguments des macros, et vérifier que le SQL compilé reste lisible.

<!-- challenge -->

Un collègue a écrit une macro qui génère des modèles entiers depuis des métadonnées YAML, et personne d'autre ne sait les déboguer. Que suggérez-vous ?

<!-- solution -->

Réserver la génération aux modèles vraiment répétitifs et mécaniques (si besoin) et écrire la logique métier en modèles SQL simples. Documenter tout générateur restant et rendre le SQL compilé facile à inspecter.

<!-- takeaways -->

- `codegen` écrit le code répétitif ; `star` liste les colonnes.
- Préférez le SQL simple ; macros pour la logique répétée.
- Un SQL compilé lisible compte pour déboguer.

<!-- stage: Qualité et historique -->

### Tests et qualité des données

<!-- unit: Tests de données -->

<!-- goals -->

- Utiliser des tests de données génériques, singuliers et génériques personnalisés.
- Tester l'unicité sur des combinaisons de colonnes.

<!-- concept -->

Un test de données est une requête qui renvoie les lignes violant une règle ; aucune ligne signifie succès. Les tests génériques sont des règles réutilisables appliquées en YAML, comme l'unicité ou les valeurs acceptées. Les tests singuliers sont des fichiers SQL ponctuels pour des règles trop spécifiques pour être réutilisées. Quand une règle revient à plusieurs endroits, un test générique personnalisé la rend réutilisable.

Comme les tests s'exécutent sur les vraies données de l'entrepôt, ils détectent les problèmes des sources autant que ceux du code.

<!-- example -->

```yaml
models:
  - name: fct_order_lines
    data_tests:
      - dbt_utils.unique_combination_of_columns:
          arguments:
            combination_of_columns: [order_id, line_number]
    columns:
      - name: status
        data_tests:
          - accepted_values:
              arguments: {values: [placed, shipped, returned]}
      - name: customer_id
        data_tests:
          - relationships:
              arguments: {to: ref('dim_customer'), field: customer_id}
```

#### Quels sont les deux types de tests dans dbt ?

Les **tests de données** vérifient les données dans l'entrepôt : tests génériques (réutilisables, paramétrés, déclarés en YAML) et tests singuliers (requêtes SQL ponctuelles dans `tests/`). Les **tests unitaires**, ajoutés dans dbt 1.8, vérifient la logique SQL d'un modèle sur de petites entrées simulées avant de l'exécuter sur de vraies données.

#### Quels types de tests peut-on exécuter dans dbt ?

Les quatre tests génériques intégrés (`unique`, `not_null`, `accepted_values`, `relationships`), des tests génériques de packages (`dbt_utils`, `dbt_expectations`) ou maison, des tests SQL singuliers et des tests unitaires. Garde-fous associés : la fraîcheur des sources et des modèles, les contrats de modèle et, dans dbt v2, les checks sur les métadonnées du projet.

#### Comment fonctionnent les tests génériques intégrés ?

```yaml
models:
  - name: fct_orders
    columns:
      - name: order_id
        data_tests: [unique, not_null]
      - name: status
        data_tests:
          - accepted_values:
              arguments:
                values: ['placed', 'shipped', 'returned']
      - name: customer_id
        data_tests:
          - relationships:
              arguments:
                to: ref('dim_customers')
                field: customer_id
```

dbt transforme chacun en une requête qui renvoie les lignes en échec. Le test réussit quand la requête ne renvoie aucune ligne. Les paramètres du test vont sous `arguments:` et les options comme `severity` sous `config:` ; les anciens projets placent les paramètres directement sous le nom du test, une syntaxe dépréciée depuis dbt v1.10.

#### Qu'est-ce qu'un test singulier ?

Un fichier `.sql` du dossier `tests/` qui sélectionne les lignes qui violent une règle. Il échoue s'il renvoie au moins une ligne :

```sql
-- tests/assert_no_negative_amounts.sql
select * from {{ ref('fct_orders') }} where amount < 0
```

#### Comment écrire un test générique personnalisé ?

Avec un bloc `{% test name(model, column_name) %}`, généralement dans `tests/generic/` ou `macros/`, qui renvoie les lignes en échec. Les paramètres supplémentaires deviennent des arguments en YAML, où l'on utilise le test comme un test intégré :

```sql
{% test is_positive(model, column_name) %}
select * from {{ model }} where {{ column_name }} <= 0
{% endtest %}
```

#### Comment vérifier qu'une combinaison de colonnes est unique ?

Avec `dbt_utils.unique_combination_of_columns` :

```yaml
data_tests:
  - dbt_utils.unique_combination_of_columns:
      arguments:
        combination_of_columns: [order_id, line_number]
```

<!-- challenge -->

Plusieurs modèles ont besoin de la règle « le montant ne peut être négatif que pour un remboursement ». Comment éviter de copier cinq fois un test singulier ?

<!-- solution -->

Écrire un test générique personnalisé (par exemple `non_negative_unless_refund(model, column_name)`) qui renvoie les lignes en infraction, et l'appliquer en YAML à la colonne montant de chaque modèle.

<!-- takeaways -->

- Les tests de données renvoient les lignes qui violent une règle.
- Les génériques se réutilisent ; les singuliers sont spécifiques.
- Les règles répétées deviennent des tests génériques personnalisés.

<!-- unit: Unit tests et packages de tests -->

<!-- goals -->

- Écrire des unit tests et les distinguer des tests de données.
- Utiliser des tests de packages pour plages, récence et nombres de lignes.

<!-- concept -->

Les tests de données vérifient les données présentes à un instant donné ; les unit tests vérifient la logique sur des entrées choisies. Un unit test fournit des lignes fixes pour les parents d'un modèle et la sortie attendue : des cas limites comme remboursements ou nulls sont testés avant même que le modèle tourne sur de vraies données.

Les packages étendent les tests de données avec des contrôles courants : valeurs dans une plage, données récentes, nombres de lignes concordants entre modèles. Ils couvrent la plupart des besoins sans SQL personnalisé.

<!-- example -->

```yaml
unit_tests:
  - name: refunds_reduce_net_amount
    model: fct_order_lines
    given:
      - input: ref('int_order_lines_enriched')
        rows:
          - {order_id: 1, line_number: 1, type: sale,   amount: 100}
          - {order_id: 1, line_number: 2, type: refund, amount: 30}
    expect:
      rows:
        - {order_id: 1, line_number: 1, net_amount: 100}
        - {order_id: 1, line_number: 2, net_amount: -30}
```

#### Qu'est-ce qu'un test unitaire dans dbt ?

Une définition YAML qui fournit des lignes d'entrée fixes pour les parents d'un modèle et la sortie attendue, pour que dbt vérifie la logique de transformation (cas limites, instructions case, fonctions de fenêtrage) sans vraies données :

```yaml
unit_tests:
  - name: test_is_valid_email
    model: dim_customers
    given:
      - input: ref('stg_customers')
        rows:
          - {customer_id: 1, email: a@b.com}
          - {customer_id: 2, email: not-an-email}
    expect:
      rows:
        - {customer_id: 1, is_valid_email: true}
        - {customer_id: 2, is_valid_email: false}
```

Les lignes peuvent être écrites en `dict` (par défaut), `csv` ou `sql`, en ligne ou dans des fichiers de fixtures, et seules les colonnes utiles au test ont besoin de valeurs. `overrides` permet de fixer des macros et des variables, par exemple `is_incremental: true` pour tester la branche incrémentale.

#### Quelle est la différence entre un test unitaire et un test de données ?

Un test unitaire vérifie le code sur des entrées fixes et s'exécute avant la construction du modèle. Comme ses entrées ne changent pas, dbt Labs recommande de n'exécuter les tests unitaires qu'en développement et en CI, et de les exclure des jobs de production. Un test de données vérifie les vraies données après la construction du modèle, à chaque exécution. Pour l'instant, les tests unitaires ne prennent en charge que les modèles SQL, et chaque `ref` ou `source` utilisé par le modèle doit être fourni en entrée.

#### Qu'est-ce que `dbt_expectations` ?

Un package de tests génériques inspiré de Great Expectations : plages de valeurs, expressions régulières, nombre de lignes, distributions, types de colonnes, etc.

#### Comment comparer le nombre de lignes d'un modèle à celui d'un autre ?

Avec un test de package comme `dbt_utils.equal_rowcount` ou `dbt_expectations.expect_table_row_count_to_equal_other_table`, ou un test singulier qui compare les comptes.

#### Comment vérifier qu'une valeur est dans une plage ?

Avec `dbt_utils.accepted_range` (`min_value`, `max_value`) ou `dbt_expectations.expect_column_values_to_be_between`.

#### Qu'est-ce qu'un test de récence ?

Un test comme `dbt_utils.recency` qui échoue quand l'horodatage le plus récent d'un modèle est plus ancien qu'un seuil, et repère ainsi les modèles qui ne reçoivent plus de données.

<!-- challenge -->

Un calcul de remise complexe passe tous les tests de données, mais une combinaison rare de coupons est mal calculée en production. Quel type de test l'aurait détecté ?

<!-- solution -->

Un unit test avec des lignes d'entrée fictives couvrant cette combinaison de coupons et la remise attendue. Les tests de données ne voient que les combinaisons présentes dans les données au moment du test.

<!-- takeaways -->

- Les unit tests vérifient la logique sur des entrées choisies.
- Les tests de données vérifient les vraies données.
- Les packages ajoutent tests de plage, de récence et de comptage.

<!-- unit: Configurer les tests -->

<!-- goals -->

- Fixer sévérité, seuils et filtres sur les tests.
- Conserver les échecs et éviter la lassitude face aux alertes.

<!-- concept -->

Tous les tests échoués ne se valent pas. Sévérité et seuils distinguent « tout arrêter » de « à regarder » : quelques lignes fautives peuvent déclencher un avertissement et un millier une erreur. Un filtre `where` limite un test aux données récentes, ce qui le garde rapide et pertinent.

Conserver les échecs transforme un test rouge en quelque chose d'analysable. Sans ces réglages, les équipes se noient dans les alertes et finissent par les ignorer, ce qui est pire que d'avoir moins de tests.

<!-- example -->

```yaml
columns:
  - name: email
    data_tests:
      - not_null:
          config:
            severity: error
            warn_if: ">0"
            error_if: ">100"
            where: "created_at >= current_date - 7"
            store_failures: true
```

#### Qu'est-ce que la sévérité d'un test ?

Un réglage `severity: warn` ou `error` (par défaut). Avec des seuils `warn_if` et `error_if` comme `">10"`, un test peut avertir pour quelques échecs et n'échouer qu'au-delà d'une limite.

#### Comment conserver les échecs des tests ?

Avec `--store-failures` ou `store_failures: true`, dbt enregistre les lignes en échec de chaque test dans une table d'un schéma d'audit (par défaut, le schéma du target suffixé par `_dbt_test__audit`), pour les examiner après l'exécution. `store_failures_as` choisit `table`, `view` ou `ephemeral` (ne rien conserver).

#### Que fait la configuration `where` d'un test ?

Elle limite le test à un sous-ensemble de lignes, par exemple les données récentes : `config: {where: "order_date >= current_date - 7"}`.

#### Comment éviter la lassitude face aux alertes des tests dbt ?

Utiliser la sévérité `warn` et des seuils pour les contrôles non critiques, tester ce qui compte pour les consommateurs, supprimer les tests qui ne détectent jamais rien d'utile, et envoyer les erreurs à leurs responsables.

<!-- challenge -->

Une équipe reçoit 40 avertissements de tests chaque matin et ne les lit plus. Que faites-vous ?

<!-- solution -->

Revoir chaque test : corriger les vrais problèmes, supprimer les tests qui ne protègent pas les consommateurs, fixer des seuils pour que les avertissements aient un sens, faire des tests critiques des erreurs bloquantes et router les alertes vers les propriétaires.

<!-- takeaways -->

- Sévérité et seuils graduent les échecs.
- `where` garde les tests ciblés et rapides.
- Peu d'alertes utiles valent mieux que beaucoup d'ignorées.

<!-- unit: Une stratégie de tests -->

<!-- goals -->

- Définir les tests minimaux nécessaires à chaque modèle.
- Tester à la source, utiliser `dbt build` pour arrêter les mauvaises données et faire respecter les standards du projet avec des checks.

<!-- concept -->

Une bonne stratégie place les tests là où ils protègent le plus. À l'entrée, les tests sur les sources et le staging détectent les problèmes de données brutes avant qu'ils ne se propagent. Sur chaque modèle, les clés primaires sont uniques et non nulles, et les clés étrangères importantes existent. Sur les modèles publics, les contrats protègent les consommateurs.

`dbt build` relie le tout : chaque modèle est testé juste après sa construction, et les enfants d'un modèle en échec sont sautés. Dans dbt v2, les checks ajoutent une couche au-dessus des données, qui fait respecter des standards comme les descriptions et les responsables avant toute exécution.

<!-- example -->

| Couche | Minimum |
|---|---|
| Sources | Fraîcheur, clé non nulle, unique si attendu |
| Staging | Clé primaire unique + non nulle |
| Marts | Unicité du grain, relations, valeurs acceptées, contrats |

#### Que faut-il tester au minimum sur chaque modèle ?

La clé primaire avec `unique` et `not_null`, les clés étrangères des jointures importantes avec `relationships`, et les colonnes catégorielles avec `accepted_values`. Ajoutez des règles métier là où une erreur coûterait cher.

#### Que signifie « tester à la source » ?

Placer des tests sur les sources et les modèles de staging, pour détecter les problèmes des données brutes à l'entrée plutôt que de les découvrir dans un tableau de bord.

#### Comment dbt garantit-il la qualité des données tout au long du pipeline ?

Par des tests à chaque couche, la fraîcheur des sources, des contrats sur les modèles publics, `dbt build` qui ignore les modèles en aval quand un test échoue, et une CI qui exécute les modèles modifiés et leurs tests avant la fusion.

#### Quelle est la différence entre `dbt test` et `dbt build` pour les tests ?

`dbt test` exécute les tests sur des modèles déjà construits. `dbt build` alterne construction et tests dans l'ordre du DAG : un test en échec empêche la construction de ses enfants.

#### Que sont les checks dans dbt v2 ?

Des règles sur le projet lui-même plutôt que sur les données : chaque modèle a une description, chaque modèle public a un responsable, les noms suivent les conventions. Un check est un fichier SQL dans `checks/`, écrit en SQL DuckDB sur le dbt Information Schema (`{{ info_schema('models') }}`), et il échoue quand il renvoie des lignes, comme un test de données. Les checks s'exécutent en local sans connexion à l'entrepôt, à la demande avec `dbt check` et automatiquement au début de chaque `dbt build`.

```sql
-- checks/all_models_have_descriptions.sql
select unique_id from {{ info_schema('models') }} where description = ''
```

<!-- challenge -->

Des doublons d'une source ont atteint trois marts avant que quiconque ne s'en aperçoive. Où aurait dû se trouver le premier test ?

<!-- solution -->

Sur la source ou son modèle de staging : un test d'unicité sur la clé source échouerait à l'entrée, et avec `dbt build` les marts seraient sautés au lieu d'être reconstruits sur des doublons.

<!-- takeaways -->

- Testez les clés de chaque modèle.
- Attrapez les problèmes bruts aux sources et au staging.
- `dbt build` empêche la propagation des mauvaises données.

### Modèles incrémentaux

<!-- unit: Fonctionnement des modèles incrémentaux -->

<!-- goals -->

- Construire des modèles incrémentaux avec `is_incremental()` et `unique_key`.
- Savoir quand les utiliser et comment ils lisent leur propre table.

<!-- concept -->

Reconstruire une table d'un milliard de lignes à chaque exécution gaspille temps et argent quand seules les lignes du jour sont nouvelles. Un modèle incrémental construit la table complète une fois, puis aux exécutions suivantes ne traite que les lignes nouvelles ou modifiées et les ajoute à la table existante.

Le modèle décide de ce qui est nouveau en filtrant dans un bloc `is_incremental()`, généralement par rapport à l'horodatage maximal déjà présent dans `{{ this }}`. Un `unique_key` transforme les insertions en upserts.

<!-- example -->

```sql
{{ config(materialized='incremental', unique_key='event_id') }}
select event_id, user_id, event_type, occurred_at
from {{ ref('stg_app__events') }}
{% if is_incremental() %}
where occurred_at > (select max(occurred_at) from {{ this }})
{% endif %}
```

#### Comment créer des modèles incrémentaux dans dbt, et quand les utiliser ?

On fixe `materialized='incremental'` et on filtre les nouvelles lignes avec `is_incremental()`. La première exécution construit toute la table, les suivantes ne traitent que les lignes plus récentes que celles déjà présentes. À utiliser pour les grosses tables alimentées surtout par ajout (événements, journaux, transactions), où tout reconstruire à chaque exécution est trop lent ou trop cher.

```sql
{{ config(materialized='incremental', unique_key='event_id') }}

select * from {{ ref('stg_events') }}
{% if is_incremental() %}
where event_time > (select max(event_time) from {{ this }})
{% endif %}
```

#### Que renvoie `is_incremental()` ?

True seulement si le modèle est matérialisé en incrémental, que la table cible existe déjà et que l'exécution n'est pas un full refresh. Le SQL du modèle doit être valide que la fonction renvoie true ou false.

#### Qu'est-ce que `unique_key` dans un modèle incrémental ?

La colonne (ou la liste de colonnes) qui identifie une ligne. Avec elle, les lignes déjà présentes sont mises à jour au lieu d'être dupliquées, selon la stratégie.

#### Comment dbt gère-t-il le chargement incrémental des données des systèmes sources ?

dbt n'extrait pas des systèmes sources : il traite des données déjà chargées dans l'entrepôt. Les modèles incrémentaux ne sélectionnent que les lignes plus récentes que les dernières traitées (via un horodatage ou un identifiant), puis les fusionnent ou les ajoutent. Des outils de chargement comme Fivetran ou Airbyte apportent les données de façon incrémentale, et dbt les transforme de façon incrémentale.

#### Un modèle incrémental peut-il se référencer lui-même ?

Oui, via `{{ this }}` dans le bloc `is_incremental()`, en général pour lire l'horodatage maximal actuel.

#### Qu'est-ce qu'un modèle incrémental « append-only » ?

Un modèle qui utilise la stratégie `append`, ou un modèle sans `unique_key` : les nouvelles lignes sont insérées et les lignes existantes ne sont jamais mises à jour. Il convient aux journaux d'événements immuables et c'est la stratégie la moins coûteuse, mais retraiter les mêmes lignes crée des doublons.

<!-- challenge -->

Un modèle incrémental n'a pas de `unique_key`, et la source renvoie parfois des commandes mises à jour. Que se passe-t-il, et que changez-vous ?

<!-- solution -->

Les commandes mises à jour sont ajoutées à nouveau, créant des doublons. Ajouter `unique_key='order_id'` (avec une stratégie merge ou delete+insert) pour que les lignes existantes soient mises à jour.

<!-- takeaways -->

- Après le premier build, l'incrémental ne traite que le nouveau.
- `is_incremental()` protège le filtre.
- `unique_key` transforme les ajouts en upserts.

<!-- unit: Stratégies incrémentales -->

<!-- goals -->

- Choisir entre append, merge, delete+insert, insert_overwrite et microbatch.
- Accélérer les merges avec prédicats et partitionnement.

<!-- concept -->

La façon de combiner les nouvelles lignes avec la table s'appelle la stratégie. Append insère simplement. Merge fait un upsert sur la clé. Delete+insert supprime d'abord les lignes correspondantes, parfois plus rapide sur de gros lots. Insert_overwrite remplace des partitions entières sur des plateformes comme BigQuery et Databricks, très efficace quand les données arrivent par jour. Microbatch découpe le travail en lots temporels indépendants, relançables et rattrapables un par un, sans filtre à écrire.

Les grosses cibles ont besoin d'aide : prédicats et partitionnement limitent la part de la table existante que parcourt chaque merge.

<!-- example -->

```sql
{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='order_id',
    incremental_predicates=["DBT_INTERNAL_DEST.ordered_at >= dateadd(day, -7, current_date)"],
    cluster_by=['ordered_at']
) }}
```

#### Quelles stratégies incrémentales existe-t-il ?

Selon l'adaptateur : `append` (insertion seule), `merge` (upsert sur `unique_key`), `delete+insert` (suppression des clés correspondantes puis insertion), `insert_overwrite` (remplacement de partitions entières sur BigQuery, Spark, Databricks et Athena) et `microbatch` (traitement par lots temporels). Certains adaptateurs ajoutent les leurs, comme `replace_where` sur Databricks. BigQuery ne prend en charge ni `append` ni `delete+insert`.

#### Quelle est la différence entre `merge` et `delete+insert` ?

`merge` met à jour les lignes correspondantes et insère les nouvelles en une seule requête. `delete+insert` supprime les lignes existantes ayant les mêmes clés, puis insère le nouveau lot. Utile là où merge est lent ou non pris en charge.

#### Qu'est-ce qu'`insert_overwrite`, et quand est-ce efficace ?

Il remplace des partitions entières (par exemple les jours présents dans le nouveau lot) au lieu de fusionner ligne par ligne. Efficace sur les tables partitionnées de BigQuery, Spark et Databricks quand les données arrivent par partition. Sur Snowflake, qui n'a pas de partitions, `insert_overwrite` remplace la table entière.

#### Que fait `incremental_predicates` ?

Il ajoute des conditions au merge, par exemple limiter la lecture de la table cible aux partitions récentes, ce qui réduit le coût sur les grosses tables.

#### Qu'est-ce que la stratégie microbatch ?

Ajoutée dans dbt 1.9, elle traite les données en lots temporels indépendants selon une colonne `event_time`. On n'écrit pas de filtre `is_incremental()` : dbt filtre sur la plage du lot chaque parent qui déclare aussi `event_time`. `batch_size` fixe la granularité (`hour`, `day`, `month` ou `year`), `begin` la date de départ pour la première construction ou une reconstruction complète, et `lookback` le nombre de lots précédents à retraiter pour les données tardives. Les lots peuvent être relancés un par un, exécutés en parallèle ou recalculés avec `--event-time-start` et `--event-time-end`.

```sql
{{ config(materialized='incremental', incremental_strategy='microbatch',
          event_time='occurred_at', begin='2024-01-01', batch_size='day', lookback=3) }}
select * from {{ ref('stg_app__events') }}   -- filtered per batch automatically
```

#### Comment le partitionnement ou le clustering interagissent-ils avec les modèles incrémentaux ?

Partitionner ou regrouper la table cible sur la colonne du filtre (en général une date) fait lire moins de données au filtre incrémental comme au merge : c'est de là que vient l'essentiel du gain.

<!-- challenge -->

Une table BigQuery partitionnée par jour reçoit une journée complète d'événements à chaque exécution. Le merge est lent et coûteux. Quelle stratégie convient mieux ?

<!-- solution -->

`insert_overwrite` avec la table partitionnée par date : chaque exécution remplace les partitions des jours concernés au lieu de fusionner ligne à ligne, ce qui coûte moins et est naturellement idempotent.

<!-- takeaways -->

- Stratégies : append, merge, delete+insert, insert_overwrite, microbatch.
- L'écrasement par partition est efficace pour des données quotidiennes.
- Prédicats et partitionnement limitent le parcours du merge.

<!-- unit: Garder les modèles incrémentaux justes -->

<!-- goals -->

- Gérer données tardives, changements de schéma et full refresh.
- Tester les modèles incrémentaux et faire des backfills.

<!-- concept -->

Les modèles incrémentaux échangent simplicité contre vitesse, et cela se voit dans les cas limites. Un filtre strict « plus récent que le max » rate les lignes tardives ; une fenêtre de lookback retraite les derniers jours pour les rattraper. Les changements de colonnes exigent une politique. Les changements de logique exigent un full refresh ou un backfill, car les lignes existantes ont été construites avec l'ancienne logique.

Les tests comptent plus que pour les tables : les clés en double sont le bug classique, et comparer de temps en temps avec une reconstruction complète prouve que les incréments s'additionnent toujours.

<!-- example -->

```sql
{% if is_incremental() %}
-- 3-day lookback catches late events; unique_key de-duplicates the overlap
where occurred_at >= (select dateadd(day, -3, max(occurred_at)) from {{ this }})
{% endif %}
```

#### Comment gérer les données qui arrivent en retard dans un modèle incrémental ?

Avec une fenêtre de retraitement plutôt qu'un « supérieur à » strict : retraiter les derniers jours, et s'appuyer sur `unique_key` avec `merge` pour mettre à jour les lignes déjà chargées.

```sql
{% if is_incremental() %}
where event_time >= (select dateadd(day, -3, max(event_time)) from {{ this }})
{% endif %}
```

#### Que fait `on_schema_change` ?

Il définit ce qui se passe quand les colonnes d'un modèle incrémental changent : `ignore` (par défaut : les nouvelles colonnes ne sont pas ajoutées), `fail`, `append_new_columns` (ajoute les nouvelles colonnes, garde les colonnes supprimées) ou `sync_all_columns` (ajoute les nouvelles, supprime celles qui ont disparu, changements de type compris). Aucune option ne remplit les anciennes lignes dans les nouvelles colonnes ; il faut pour cela un full refresh. Seules les colonnes de premier niveau sont suivies, pas les champs imbriqués.

#### Quand faut-il faire un full refresh d'un modèle incrémental ?

Quand la logique change d'une manière qui affecte les lignes historiques, quand les colonnes changent d'une façon que `on_schema_change` ne gère pas, ou pour réparer des données. Certaines tables sont protégées par `full_refresh: false` car les reconstruire coûte trop cher.

#### Quels sont les risques des modèles incrémentaux ?

Des doublons si `unique_key` manque ou est fausse, des lignes manquées si le filtre oublie les données tardives, un écart avec une reconstruction complète si la logique change, et des tests plus complexes. Un full refresh périodique dans un environnement inférieur aide à détecter les écarts.

#### Comment bien tester un modèle incrémental ?

Tester l'unicité de la clé primaire (les doublons sont le bug classique), comparer avec un full refresh dans un environnement inférieur, et écrire des tests unitaires qui forcent `is_incremental` à true et à false.

#### Comment recalculer l'historique (backfill) d'un modèle incrémental ?

Avec `--full-refresh`, ou pour les modèles microbatch avec `--event-time-start` et `--event-time-end` pour retraiter une période, ou en l'exécutant avec une variable qui change la fenêtre du filtre.

<!-- challenge -->

Vous changez le calcul de `net_amount` dans un modèle incrémental. Les nouvelles lignes sont justes, mais celles de l'an dernier utilisent toujours l'ancienne formule. Que faites-vous ?

<!-- solution -->

Reconstruire l'historique : lancer avec `--full-refresh` (ou un backfill microbatch sur la plage concernée). Les exécutions incrémentales ne revisitent jamais les anciennes lignes, donc un changement de logique impose de les retraiter.

<!-- takeaways -->

- Utilisez des fenêtres de lookback pour les données tardives.
- Un changement de logique exige full refresh ou backfill.
- Testez les doublons de clés ; comparez à des reconstructions complètes.

<!-- unit: Les modèles incrémentaux dans la durée -->

<!-- goals -->

- Expliquer pourquoi les modèles incrémentaux ralentissent et comment y remédier.
- Choisir entre modèles incrémentaux et snapshots.

<!-- concept -->

Un modèle incrémental rapide au lancement peut devenir lent un an plus tard, car chaque merge parcourt une cible qui ne cesse de grossir. Limiter le parcours avec prédicats, partitionnement ou clustering garde le coût proportionnel aux nouvelles données.

Modèles incrémentaux et snapshots « ajoutent avec le temps », mais répondent à des questions différentes. Les incrémentaux gardent le dernier état ou le flux d'événements selon votre logique ; les snapshots enregistrent comment les lignes modifiables de la source ont changé.

<!-- example -->

| Besoin | Utiliser |
|---|---|
| Ajouter efficacement des événements de clic | Incrémental (append) |
| Garder les commandes courantes, mises à jour sur place | Incrémental (merge) |
| Historique des changements d'offre de chaque client | Snapshot |

#### Pourquoi un modèle incrémental peut-il ralentir avec le temps ?

Le merge doit parcourir une table cible toujours plus grande. Les incremental predicates, l'élagage des partitions, le clustering, ou les stratégies `insert_overwrite` et `microbatch` gardent chaque exécution bornée.

#### Quelle est la différence entre un modèle incrémental et un snapshot ?

Un modèle incrémental garde le dernier état (ou ajoute des événements), et sa logique est la vôtre. Un snapshot garde l'historique complet des changements d'enregistrements modifiables, sous forme de lignes SCD de type 2 avec des dates de validité. Les deux se combinent bien : un modèle de staging incrémental garde des exécutions peu coûteuses, et un snapshot sur la source conserve l'historique quand le métier doit savoir à quoi ressemblait une ligne dans le passé.

<!-- challenge -->

La durée d'un modèle incrémental en merge est passée de 2 à 25 minutes en un an, alors que le volume quotidien est stable. Que faites-vous ?

<!-- solution -->

Limiter le parcours de la cible : ajouter des `incremental_predicates` sur une plage de dates récente et partitionner ou regrouper la table sur cette date, pour que le merge ne touche que les données récentes.

<!-- takeaways -->

- Les merges sans limite ralentissent quand les tables grossissent.
- Prédicats et clustering gardent les merges bon marché.
- L'incrémental garde l'état ; les snapshots, l'historique.

### Snapshots

<!-- unit: Capturer l'historique avec les snapshots -->

<!-- goals -->

- Définir des snapshots avec la stratégie timestamp ou check.
- Expliquer les colonnes ajoutées par dbt et comment les snapshots implémentent le SCD2.

<!-- concept -->

Les tables source écrasent souvent les lignes : l'offre d'un client change et l'ancienne valeur disparaît. Les snapshots enregistrent ces changements. Chaque exécution compare la source à la dernière version enregistrée et, en cas de changement, clôt l'ancienne version et en insère une nouvelle : c'est exactement une dimension à évolution lente de type 2.

Détecter le changement, c'est la stratégie : une colonne updated-at fiable est la moins coûteuse ; sans elle, comparer certaines colonnes ou toutes fonctionne pour un coût plus élevé.

<!-- example -->

```yaml
# snapshots/customers_snapshot.yml
snapshots:
  - name: customers_snapshot
    relation: source('crm', 'customers')
    config:
      unique_key: customer_id
      strategy: timestamp
      updated_at: updated_at
      hard_deletes: invalidate
```

#### Qu'est-ce qu'un snapshot ?

Une ressource dbt qui enregistre les changements d'une table modifiable au fil du temps (Slowly Changing Dimension de type 2). À chaque exécution, il compare les lignes actuelles de la source à la table du snapshot, ferme les lignes modifiées en fixant `dbt_valid_to` et insère leur nouvelle version avec `dbt_valid_from`.

#### Comment définit-on un snapshot ?

Depuis dbt 1.9, dans un fichier YAML qui nomme la relation à historiser et sa configuration (les anciens projets utilisent un bloc `{% snapshot %}` avec un `select` dans `snapshots/`, qui fonctionne toujours mais reste la forme historique) :

```yaml
snapshots:
  - name: customers_snapshot
    relation: source('crm', 'customers')
    config:
      schema: snapshots
      unique_key: customer_id
      strategy: timestamp
      updated_at: updated_at
```

#### Quelles stratégies de snapshot existe-t-il ?

`timestamp` (recommandée) : une ligne a changé si sa colonne `updated_at` est plus récente. Fiable et efficace quand la source maintient cette colonne. `check` : une ligne a changé si l'une des `check_cols` listées (ou toutes les colonnes) diffère. Utilisée quand il n'y a pas d'horodatage fiable.

#### Quelles colonnes dbt ajoute-t-il à un snapshot ?

`dbt_scd_id` (une clé unique par version), `dbt_updated_at`, `dbt_valid_from` et `dbt_valid_to` (NULL pour la version courante, sauf si `dbt_valid_to_current` fixe une valeur comme `9999-12-31`). Avec `hard_deletes: new_record`, dbt ajoute aussi `dbt_is_deleted`. Les noms peuvent être changés avec `snapshot_meta_column_names`.

#### Quand utiliser la stratégie `check` avec `check_cols: all` ?

Quand la source n'a pas d'`updated_at` fiable et que tout changement de colonne compte. Elle est plus coûteuse, car toutes les colonnes sont comparées, et les nouvelles colonnes de la source modifient ce qui compte comme un changement. La documentation recommande de lister explicitement les colonnes utiles, ou de comparer une seule colonne de hachage construite à partir d'elles.

#### Qu'est-ce qu'une SCD de type 2, et comment les snapshots dbt l'implémentent-ils ?

Une dimension à évolution lente qui conserve une nouvelle ligne pour chaque version d'un enregistrement, avec des dates de validité. Les snapshots dbt sont exactement cela : une ligne par version, `dbt_valid_from` et `dbt_valid_to` bornant sa validité.

<!-- challenge -->

Une table source n'a pas de colonne `updated_at`, mais les changements de `plan` et `status` comptent. Comment configurez-vous le snapshot ?

<!-- solution -->

Utiliser la stratégie `check` avec `check_cols: ['plan', 'status']`, pour que dbt compare ces colonnes à chaque exécution et enregistre une nouvelle version quand elles changent.

<!-- takeaways -->

- Les snapshots enregistrent les changements de lignes modifiables (SCD2).
- Timestamp est la moins coûteuse ; check marche sans horodatage.
- dbt ajoute des colonnes de validité et d'ID.

<!-- unit: Exécuter les snapshots en sécurité -->

<!-- goals -->

- Gérer suppressions, problèmes de clé et fréquence d'exécution.
- Expliquer pourquoi les snapshots ne se reconstruisent pas et en quoi ils diffèrent du time travel.

<!-- concept -->

Les snapshots sont la seule partie d'un projet dbt qui ne se régénère pas : un changement non capturé est perdu. Cela dicte toutes leurs règles. Lire les sources brutes, pour que l'historique reflète la réalité et non votre logique actuelle. Les exécuter assez souvent pour attraper les changements qui s'annulent. S'assurer que la clé est unique, sinon les versions se mélangent.

Les suppressions exigent un traitement explicite, et le time travel de l'entrepôt ne les remplace pas : sa rétention est courte et il sert à la reprise, pas à l'historique.

<!-- example -->

| Règle | Pourquoi |
|---|---|
| Snapshotter les sources, pas les marts | Un changement de logique réécrirait l'historique |
| Tester l'unicité de la clé source | Les doublons corrompent les versions |
| Exécuter au moins aussi souvent que les changements comptent | Les changements manqués sont perdus |
| Ne jamais supprimer la table du snapshot | Le full refresh ne s'applique pas ; l'historique ne se reconstruit pas |

#### Comment les snapshots gèrent-ils les lignes supprimées de la source ?

Par défaut (`hard_deletes: ignore`), ils ne les gèrent pas : la dernière version d'une ligne supprimée reste courante. Avec `hard_deletes: invalidate` (anciennement `invalidate_hard_deletes: true`), les lignes supprimées reçoivent leur `dbt_valid_to`. Avec `hard_deletes: new_record`, dbt insère une nouvelle ligne avec `dbt_is_deleted = True`, et une ligne qui réapparaît reçoit une nouvelle version avec `dbt_is_deleted = False`.

#### Pourquoi les snapshots doivent-ils lire des sources plutôt que des modèles transformés ?

Les snapshots capturent un historique qu'on ne peut pas recréer après coup. Photographier les données brutes avec un minimum de logique garantit qu'un bug dans le code de transformation ne corrompt pas l'historique, et qu'on peut relancer les transformations par-dessus.

#### À quelle fréquence exécuter les snapshots ?

Aussi souvent que nécessaire pour capturer les changements : les changements qui surviennent puis s'annulent entre deux exécutions sont perdus. Beaucoup d'équipes les exécutent toutes les heures ou tous les jours, avant les modèles qui les utilisent.

#### Que se passe-t-il si la `unique_key` n'est pas unique dans la source ?

Le snapshot produit des versions dupliquées ou incohérentes. Testez l'unicité sur la source et dédoublonnez en amont si besoin.

#### Peut-on faire un full refresh d'un snapshot ?

Non. Les snapshots ignorent à la fois l'option `--full-refresh` et la config `full_refresh` : un `dbt build --full-refresh` les exécute normalement, car supprimer la table ferait perdre un historique impossible à recréer. Pour en modifier un, on migre la table à la main ou on démarre un nouveau snapshot.

#### En quoi les snapshots diffèrent-ils du time travel de Delta Lake ou de l'entrepôt ?

Le time travel de l'entrepôt conserve les versions passées d'une table pendant une durée de rétention limitée, pour la récupération. Les snapshots construisent une table d'historique permanente et interrogeable au niveau de la ligne, conçue pour l'analyse.

<!-- challenge -->

Un snapshot tourne chaque jour, mais des clients changent parfois d'offre puis reviennent en arrière en quelques heures. Le métier veut voir ces changements. Que changez-vous ?

<!-- solution -->

Exécuter le snapshot plus souvent (par exemple toutes les heures), ou capturer les changements en amont par CDC. Un snapshot quotidien ne voit que l'état au moment de l'exécution : les changements éphémères sont manqués.

<!-- takeaways -->

- Les snapshots ne se reconstruisent pas ; protégez-les.
- Snapshottez des sources brutes à clés uniques.
- Traitez explicitement les suppressions ; le time travel n'est pas un historique.

<!-- unit: Interroger les snapshots -->

<!-- goals -->

- Interroger les versions courantes et à une date donnée d'un snapshot.
- Construire une dimension historisée sur un snapshot.

<!-- concept -->

Un snapshot est de l'historique brut, et comme toute donnée brute il se consomme mieux via un modèle. Les versions courantes sont les lignes dont la validité n'est pas terminée ; une vue à date choisit la version dont la plage contient cette date.

Un modèle de dimension par-dessus renomme les colonnes de validité, ajoute un indicateur de version courante et une clé de substitution, et offre aux faits une cible de jointure propre.

<!-- example -->

```sql
-- models/marts/dim_customer.sql
select
    {{ dbt_utils.generate_surrogate_key(['customer_id', 'dbt_valid_from']) }} as customer_key,
    customer_id, plan, status,
    dbt_valid_from as valid_from,
    coalesce(dbt_valid_to, '9999-12-31'::timestamp) as valid_to,
    dbt_valid_to is null as is_current
from {{ ref('customers_snapshot') }}
```

#### Comment interroger la version courante de chaque enregistrement d'un snapshot ?

`where dbt_valid_to is null` (ou la valeur courante configurée).

#### Comment obtenir l'état d'un enregistrement à une date donnée ?

```sql
select * from {{ ref('customers_snapshot') }}
where '2026-06-30' >= dbt_valid_from
  and ('2026-06-30' < dbt_valid_to or dbt_valid_to is null)
```

#### Comment construire une dimension historisée à partir d'un snapshot ?

Sélectionner depuis le snapshot dans un modèle, renommer `dbt_valid_from` et `dbt_valid_to` en noms plus parlants, ajouter une clé de substitution par version et un indicateur `is_current`, puis joindre les faits sur la clé naturelle et la date du fait comprise dans la période de validité.

<!-- challenge -->

La finance demande l'offre de chaque client au 30 juin. Écrivez le filtre.

<!-- solution -->

`where '2026-06-30' >= dbt_valid_from and ('2026-06-30' < dbt_valid_to or dbt_valid_to is null)` sur le snapshot (ou l'équivalent sur `valid_from`/`valid_to` dans la dimension).

<!-- takeaways -->

- Les lignes courantes n'ont pas de fin de validité.
- Les requêtes à date filtrent sur la plage de validité.
- Construisez des dimensions sur les snapshots.

<!-- stage: Production -->

### Documentation, lignage et couche sémantique

<!-- unit: Documenter les projets -->

<!-- goals -->

- Rédiger des descriptions et générer le site de documentation.
- Utiliser persist_docs, champs meta et exposures.

<!-- concept -->

La documentation dbt vit à côté du code : descriptions en YAML pour les modèles et colonnes, textes plus longs dans des doc blocks. Le site de documentation les combine avec le DAG et les tests, pour que le lecteur voie ce que signifie une table et d'où elle vient.

La documentation va plus loin quand elle sort de dbt : persister les descriptions dans l'entrepôt les affiche dans les outils BI, les champs meta enregistrent propriétaires et sensibilité, et les exposures déclarent quels tableaux de bord dépendent de quels modèles.

<!-- example -->

```yaml
exposures:
  - name: revenue_dashboard
    type: dashboard
    owner: {name: Finance Data, email: finance-data@example.com}
    depends_on: [ref('fct_revenue'), ref('dim_customer')]
models:
  - name: fct_revenue
    description: "One row per invoice line. Net of refunds and discounts, in EUR."
    config:
      meta: {owner: finance-data, contains_pii: false}
      persist_docs: {relation: true, columns: true}
```

#### Comment dbt génère-t-il la documentation ?

`dbt docs generate` construit un site statique à partir du projet (descriptions, colonnes, tests, SQL) et des métadonnées de l'entrepôt (types de colonnes, nombre de lignes), et `dbt docs serve` le sert en local, avec un graphe de lignage interactif. Dans dbt v2, docs v2 stocke les métadonnées en fichiers Parquet que le navigateur interroge avec DuckDB-WASM : le site tient la charge sur les gros projets, peut être hébergé sur n'importe quel hébergement statique et affiche le lignage au niveau des colonnes quand il est construit avec `--static-analysis strict`. Sur la dbt platform, ce sont les jobs qui tiennent Catalog à jour.

#### Où écrit-on les descriptions ?

Dans des fichiers de propriétés YAML à côté des modèles (`description:` sur les modèles et les colonnes), ou dans des blocs `{% docs %}` de fichiers `.md` référencés avec `{{ doc('name') }}` pour les textes longs.

#### Qu'est-ce que `persist_docs` ?

Une configuration qui écrit les descriptions des modèles et des colonnes dans l'entrepôt sous forme de commentaires de tables et de colonnes, pour qu'elles soient visibles dans d'autres outils.

#### Comment documenter un test ou une macro ?

Les macros se documentent en YAML sous une clé `macros:`, avec une description et leurs arguments. Les tests de données acceptent une `description` là où ils sont appliqués, et les tests singuliers peuvent être documentés dans un fichier de propriétés sous `data_tests:`. Ces descriptions apparaissent dans la documentation générée.

#### Que sont les champs meta ?

Un dictionnaire libre `meta`, défini sous `config:` sur les nœuds et les colonnes, par exemple pour noter les responsables, les indicateurs de données personnelles ou les engagements de service. Les outils externes le lisent dans le manifest, et les macros avec `config.meta_get()`.

#### Que sont les exposures ?

Des déclarations YAML des usages en aval des modèles dbt (tableaux de bord, modèles de ML, applications) avec leurs responsables, pour que le lignage montre ce qui dépend de chaque modèle.

<!-- challenge -->

Avant de modifier `fct_revenue`, un ingénieur veut savoir quels tableaux de bord seront touchés. Comment le projet répond-il ?

<!-- solution -->

Avec des exposures déclarées pour les tableaux de bord : le DAG montre quelles exposures dépendent de `fct_revenue`, avec leurs propriétaires, et `dbt ls --select fct_revenue+` les liste.

<!-- takeaways -->

- Les descriptions vivent en YAML à côté des modèles.
- `persist_docs` les pousse dans l'entrepôt.
- Les exposures relient les modèles à leurs consommateurs.

<!-- unit: Artefacts et lignage -->

<!-- goals -->

- Utiliser les artefacts dbt pour lignage, supervision et vérifications de sélection.
- Expliquer le lignage au niveau colonne.

<!-- concept -->

Chaque invocation de dbt écrit des artefacts : un manifest qui décrit tout le projet et des run results avec le résultat et la durée de chaque nœud. De nombreux outils reposent dessus : comparaison d'état en CI, tableaux de bord d'observabilité, catalogues et graphes de lignage.

Le lignage au niveau modèle montre quelles tables dépendent de quelles autres ; le lignage au niveau colonne va plus loin et remonte chaque colonne jusqu'à ses sources, ce qui répond précisément à « qu'est-ce qui casse si je supprime cette colonne ? ».

<!-- example -->

```bash
dbt ls --select state:modified+ --state prod-artifacts/    # check a selection before running
jq '.results[] | {node: .unique_id, s: .execution_time}' target/run_results.json | head
```

#### Que fait `dbt ls` ?

Il liste les nœuds correspondant à une sélection sans les exécuter, ce qui est utile pour vérifier les sélecteurs.

#### Qu'est-ce que l'artefact `manifest.json` ?

Un fichier JSON du dossier `target/` qui décrit tout le projet (nœuds, configurations, dépendances). Il sert à la comparaison d'états (`state:modified`), à la documentation et aux outils externes.

#### Qu'est-ce que `run_results.json` ?

Un artefact qui contient le résultat, la durée et le statut de chaque nœud de la dernière invocation, utilisé pour la supervision et par `dbt retry`.

#### À quoi servent les artefacts dbt pour l'observabilité ?

Des outils analysent `manifest.json` et `run_results.json` pour suivre la durée des exécutions, les échecs de tests et la fraîcheur dans le temps, et le package `dbt_artifacts` les charge dans l'entrepôt pour les analyser. dbt v2 peut aussi écrire le dbt Information Schema (`--generate-info-schema`) : des tables Parquet versionnées qui décrivent chaque ressource, et que les checks et `dbt show --info` interrogent directement.

#### Qu'est-ce que le lignage au niveau des colonnes ?

Un lignage qui montre quelles colonnes amont alimentent chaque colonne, et pas seulement quels modèles dépendent de quels autres, pour voir précisément ce qu'affecte le renommage ou la suppression d'une colonne. dbt Catalog l'affiche sur la dbt platform, et dbt v2 le calcule en local quand on compile ou construit avec `--static-analysis strict`.

<!-- challenge -->

Vous voulez un rapport hebdomadaire des dix modèles les plus lents et des tests qui échouent le plus. D'où viennent les données ?

<!-- solution -->

Du `run_results.json` de chaque exécution de production (durée et statut par nœud), joint au `manifest.json` pour les métadonnées des modèles, chargé dans une table et agrégé par semaine.

<!-- takeaways -->

- `manifest.json` décrit le projet ; `run_results.json`, l'exécution.
- Les artefacts alimentent CI, observabilité et catalogues.
- Le lignage colonne remonte l'origine de chaque colonne.

<!-- unit: La couche sémantique -->

<!-- goals -->

- Décrire semantic models, entités, dimensions et types de métriques.
- Expliquer pourquoi les métriques ont leur place dans dbt plutôt que dans les outils BI.

<!-- concept -->

Quand chaque outil BI définit lui-même le « chiffre d'affaires », les chiffres divergent. La couche sémantique définit les métriques une fois dans dbt, au-dessus des modèles : un semantic model marque les colonnes d'un modèle comme entités pour les jointures et dimensions pour découper, les métriques simples agrègent une colonne, et les autres types de métriques combinent des métriques en définitions métier.

Les outils interrogent alors la métrique par son nom, et MetricFlow génère le SQL correct avec les bonnes jointures, le bon grain et les bons filtres : chaque consommateur obtient la même réponse.

<!-- example -->

```yaml
models:
  - name: fct_orders
    semantic_model: {enabled: true}
    agg_time_dimension: ordered_at
    columns:
      - name: order_id
        entity: {type: primary, name: order}
      - name: customer_id
        entity: {type: foreign, name: customer}
      - name: ordered_at
        granularity: day
        dimension: {type: time}
    metrics:
      - name: revenue
        type: simple
        agg: sum
        expr: net_amount
```

#### Quelle est l'architecture de la couche sémantique de dbt ?

Des modèles sémantiques sont déclarés au-dessus des modèles dbt et marquent des entités (clés de jointure) et des dimensions. Les indicateurs sont définis à partir d'eux. MetricFlow transforme une demande d'indicateurs (indicateurs, dimensions, filtres, granularité) en SQL pour l'entrepôt, en s'appuyant sur les entités pour trouver les jointures, et la dbt platform l'expose via des API (JDBC, GraphQL, SDK Python) et des intégrations avec les outils de BI et les tableurs.

#### Qu'est-ce qu'un modèle sémantique ?

Des métadonnées attachées à un modèle dbt qui indiquent à MetricFlow comment le joindre et l'agréger. Dans la spécification actuelle (dbt v1.12+ et v2), il s'active dans le YAML du modèle avec `semantic_model:`, les entités et dimensions se définissent sur les colonnes et les métriques simples sont listées à côté. Les anciens projets utilisent un bloc `semantic_models:` séparé, au premier niveau, avec des `measures`, dépréciées au profit des métriques simples.

#### Quels types d'indicateurs existent dans la couche sémantique ?

Simples (une agrégation d'une colonne, comme `sum` ou `count_distinct`), ratios (un indicateur divisé par un autre), cumulatifs (totaux cumulés ou fenêtres), dérivés (une expression sur d'autres indicateurs) et de conversion (le taux auquel une entité passe d'un événement à un autre). Les métriques simples vivent avec leur modèle sémantique ; les autres se définissent sous une clé `metrics:` de premier niveau.

#### Pourquoi définir les indicateurs dans dbt plutôt que dans l'outil de BI ?

Pour que la définition existe une seule fois, dans la gestion de versions, avec des tests et une revue, et que chaque outil donne le même chiffre pour « chiffre d'affaires » ou « utilisateurs actifs ».

<!-- challenge -->

L'outil BI du marketing et le tableur de la finance affichent un « panier moyen » différent. Comment la couche sémantique corrigerait-elle cela ?

<!-- solution -->

Définir une fois le panier moyen comme métrique de ratio (numérateur `revenue`, dénominateur `orders`) dans dbt, relue dans Git, et faire interroger cette métrique par les deux outils via l'API de la couche sémantique au lieu de la calculer eux-mêmes.

<!-- takeaways -->

- Les semantic models déclarent entités et dimensions ; les métriques simples agrègent des colonnes.
- Les métriques sont définies une fois, sous gestion de versions.
- Tous les outils interrogent les mêmes définitions.

### Déploiement, environnements, CI/CD et orchestration

<!-- unit: Environnements, gestion de versions et CI -->

<!-- goals -->

- Gérer dev, staging et production avec un seul code.
- Lancer le Slim CI avec `state:modified`, déployer en sécurité et expliquer ce qu'apporte dbt State.

<!-- concept -->

dbt rend les environnements bon marché : un seul code, plusieurs targets, chacune écrivant dans ses propres schémas. Les développeurs construisent dans des schémas personnels, la CI dans un schéma par pull request, la production en production.

Le Slim CI compare le projet aux artefacts de production et ne construit que les modèles modifiés et leurs enfants, en faisant defer vers la production pour le reste. dbt State pousse la même idée plus loin et décide, par nœud et par exécution, si une reconstruction est vraiment nécessaire. Pour les changements sensibles, construire une nouvelle version complète à côté de l'ancienne et basculer de façon atomique donne un déploiement blue-green.

<!-- example -->

```bash
# CI for a pull request
dbt deps
dbt build --select state:modified+ --defer --state prod-artifacts/ --target ci
```

#### Comment gérer les déploiements de dbt sur plusieurs environnements (dev, staging, production) ?

Avec une seule base de code et plusieurs targets (ou environnements de la dbt platform) pointant vers des schémas ou des bases séparés : chaque développeur construit dans un schéma dev personnel, la CI dans un schéma temporaire, et des jobs planifiés construisent la production. Les différences entre environnements viennent de `profiles.yml`, des variables d'environnement et de `target.name`, jamais de modifications du code. Les changements n'arrivent en production que par pull request et CI.

#### Comment gérer la gestion de versions de dbt quand plusieurs personnes travaillent ensemble ?

Git avec des branches de fonctionnalité et des pull requests, la revue de code, une CI qui construit et teste les modèles modifiés à chaque pull request, un guide de style et un linter (SQLFluff), des responsables clairs pour chaque modèle, des changements petits et ciblés, et un schéma dev personnel par développeur pour que personne n'écrase les tables d'un autre.

#### Qu'est-ce que Slim CI ?

N'exécuter en CI que les modèles modifiés et leurs dépendants, par comparaison avec les artefacts de production : `dbt build --select state:modified+ --defer --state prod-artifacts/`. Les parents inchangés sont lus en production au lieu d'être reconstruits. Les jobs de CI de la dbt platform le font automatiquement et construisent dans un schéma temporaire par pull request.

#### Que sélectionne `state:modified` ?

Les nœuds dont le SQL, la configuration ou les propriétés diffèrent du manifest fourni avec `--state`. Combiné avec `+`, il inclut leurs enfants. Des sous-sélecteurs l'affinent, comme `state:modified.body` ou `state:modified.configs`, et `state:new` ne sélectionne que les nœuds absents du manifest de comparaison.

#### Qu'est-ce que dbt State ?

Un service géré de dbt Labs (il exige une connexion à la dbt platform et se facture à l'usage) qui décide, nœud par nœud, si une construction est nécessaire. Il compare la logique et les données amont de chaque nœud aux constructions précédentes dans tous les environnements, puis ignore le nœud si rien n'a changé, clone un objet identique et à jour depuis un autre schéma, ou le construit normalement en faisant defer des parents non sélectionnés. Il fonctionne avec dbt v1, v2 et les orchestrateurs externes, ignore les changements sans effet sur la logique comme les commentaires et les espaces, et utilise `lag_tolerance` pour ne pas reconstruire un modèle plus souvent que nécessaire. `dbt state explain` montre pourquoi chaque nœud a été ignoré, cloné ou construit. Il remplace l'orchestration fondée sur l'état (state-aware orchestration) que proposait auparavant la plateforme.

#### Qu'est-ce qu'un déploiement bleu-vert avec dbt ?

Construire la production dans un nouveau schéma ou une nouvelle base, la tester, puis la basculer de façon atomique (renommage de schémas ou permutation de vues), pour que les consommateurs ne voient jamais de données à moitié construites.

<!-- challenge -->

La CI construit tout le projet de 600 modèles à chaque pull request et prend 50 minutes. Que changez-vous ?

<!-- solution -->

Passer au Slim CI : télécharger le manifest de production, construire `state:modified+` avec `--defer` et utiliser un schéma par PR. Une PR typique construit alors quelques modèles en quelques minutes.

<!-- takeaways -->

- Un code, plusieurs targets et schémas.
- Le Slim CI ne construit que ce qui a changé.
- Le blue-green met en place un build entièrement testé.

<!-- unit: Orchestrer dbt -->

<!-- goals -->

- Planifier dbt auto-hébergé avec un orchestrateur ou utiliser la plateforme dbt.
- Concevoir un job de production qui s'exécute après l'ingestion.

<!-- concept -->

dbt ne se planifie pas lui-même. Quand on héberge dbt soi-même, un orchestrateur l'exécute, idéalement au sein d'un pipeline plus large : attendre l'ingestion, vérifier la fraîcheur, construire et tester, puis prévenir l'aval. La plateforme dbt intègre jobs et déclencheurs, avec des API pour les orchestrateurs.

Un job de production type suit partout les mêmes étapes, et exécuter dbt dans un conteneur le rend reproductible où qu'il tourne.

<!-- example -->

```bash
# typical production job
dbt deps
dbt source freshness
dbt build --target prod
dbt docs generate
# then: upload artifacts, alert on failure, trigger downstream
```

#### Citez trois avantages de l'intégration de dbt avec Airflow.

1. Les exécutions dbt sont orchestrées avec le reste du pipeline (attendre l'ingestion, transformer, puis rafraîchir les tableaux de bord ou entraîner des modèles).
2. Les relances, les alertes, les SLA, les recalculs d'historique et la planification viennent d'Airflow.
3. Avec des outils comme Astronomer Cosmos, chaque modèle dbt devient une tâche Airflow, ce qui donne une visibilité fine et permet de ne relancer que les modèles en échec.

#### Comment planifier dbt auto-hébergé en production ?

Avec un orchestrateur (Airflow, Dagster, Prefect, cron, GitHub Actions, Databricks Lakeflow Jobs) qui lance `dbt build` (ou les commandes choisies) dans un conteneur ou un environnement virtuel avec les identifiants de production.

#### À quoi ressemble un job de production typique ?

`dbt deps`, `dbt source freshness` (ou `dbt freshness` dans dbt v2), `dbt build` (seeds, snapshots, modèles et tests dans l'ordre), puis `dbt docs generate`, avec des alertes en cas d'échec et les artefacts conservés pour la comparaison suivante en CI.

#### Comment déployer dbt sur la dbt platform ?

Créer des environnements de déploiement avec leurs identifiants et leur version de dbt (release track), puis définir les jobs : jobs de déploiement avec commandes, planification ou déclencheurs et modèles sélectionnés ; jobs de CI exécutés sur chaque pull request ; et jobs de merge exécutés après la fusion d'une pull request. Utiliser l'enchaînement de jobs ou l'API d'administration pour lancer dbt après l'ingestion.

#### Comment lancer dbt à la fin de l'ingestion ?

Via l'orchestrateur (une dépendance entre tâches ou un capteur), les déclenchements par API ou l'enchaînement de jobs de la dbt platform, ou l'intégration de l'outil d'ingestion (par exemple Fivetran qui déclenche un job dbt).

#### Comment exécuter dbt dans un conteneur Docker ?

Utiliser une image où dbt est installé (avec dbt v1, plus le package de l'adaptateur ; dbt v2 est un binaire unique qui télécharge le driver de l'adaptateur à la première exécution, donc à mettre en cache ou à intégrer à l'image), monter ou copier le projet, passer les identifiants par variables d'environnement et lancer des commandes comme `dbt build --target prod`.

<!-- challenge -->

dbt tourne à 06:00 par cron, mais l'ingestion finit parfois à 06:30 : les marts sont construits sur les données de la veille. Que changez-vous ?

<!-- solution -->

Déclencher dbt depuis l'orchestrateur à la fin de l'ingestion (dépendance de tâches, sensor ou appel d'API), et garder la source freshness en première étape pour qu'un chargement tardif échoue bruyamment au lieu de construire des données périmées.

<!-- takeaways -->

- Un orchestrateur ou la plateforme dbt exécute dbt.
- Lancez dbt à la fin de l'ingestion, pas à heure fixe.
- Jobs de production : deps, freshness, build, docs.

<!-- unit: Sécurité -->

<!-- goals -->

- Exécuter dbt avec des identifiants au moindre privilège.
- Appliquer les grants en code.

<!-- concept -->

dbt n'ajoute aucun accès aux données : il exécute du SQL avec les permissions de ses identifiants, dans l'entrepôt. La sécurité se résume donc à ces identifiants, un utilisateur de service dédié par environnement avec seulement les privilèges nécessaires, et à garder les secrets hors du dépôt.

Les grants peuvent vivre avec les modèles : les permissions sont relues et appliquées à chaque build au lieu d'être accordées à la main.

<!-- example -->

```yaml
models:
  shop:
    marts:
      +grants:
        select: ['reporting', 'analyst']
    staging:
      +grants:
        select: []          # no direct access for consumers
```

#### Quelles mesures de sécurité dbt offre-t-il pour l'accès aux données et leur transformation ?

dbt s'exécute avec les droits d'entrepôt des identifiants qu'il utilise : des comptes de service au moindre privilège par environnement sont le principal contrôle. Il propose aussi la configuration `grants` pour gérer les privilèges des objets construits, des secrets dans des variables d'environnement (masqués avec le préfixe `DBT_ENV_SECRET_`), des niveaux d'accès aux modèles et des contrats. La dbt platform ajoute le SSO, le contrôle d'accès par rôles, des journaux d'audit et des restrictions par IP.

#### Comment dbt garantit-il la sécurité des données ?

dbt ne stocke ni ne déplace les données : les transformations s'exécutent dans l'entrepôt, donc les données restent sous les contrôles d'accès, le chiffrement et la gouvernance de l'entrepôt. dbt ne détient que des identifiants de connexion, qui doivent être des secrets aux privilèges minimaux.

#### Que fait la configuration `grants` ?

Elle déclare des privilèges, que dbt applique après la construction d'un modèle :

```yaml
models:
  +grants:
    select: ['reporter', 'analyst']
```

<!-- challenge -->

Le job dbt de production tourne avec un compte administrateur personnel. Que changez-vous ?

<!-- solution -->

Créer un utilisateur de service pour la production avec des privilèges limités aux bases et schémas nécessaires, stocker ses identifiants dans le gestionnaire de secrets de l'orchestrateur, et gérer l'accès des consommateurs avec `grants` dans le projet.

<!-- takeaways -->

- dbt a exactement l'accès de ses identifiants.
- Utilisez des utilisateurs de service au moindre privilège par environnement.
- Déclarez les grants en code avec `grants`.

<!-- unit: Débogage, outillage et adoption -->

<!-- goals -->

- Déboguer les modèles et comprendre comment dbt compile les requêtes.
- Introduire dbt dans des pipelines existants et passer à l'échelle avec dbt Mesh.

<!-- concept -->

L'essentiel du débogage dbt commence par le SQL compilé : ce que dbt a réellement envoyé à l'entrepôt, exécutable directement. Journaux, artefacts et historique des requêtes de l'entrepôt complètent le tableau. Le linting avec SQLFluff garde le code assez homogène pour être lu rapidement.

Adopter dbt part rarement de zéro : les tables existantes deviennent des sources, les transformations existantes sont reconstruites modèle par modèle et comparées. À plus grande échelle, plusieurs projets référencent les modèles publics des autres via dbt Mesh.

<!-- example -->

```bash
dbt compile --select fct_orders && cat target/compiled/shop/models/marts/fct_orders.sql
dbt --debug run --select fct_orders        # verbose logs
sqlfluff lint models/marts/fct_orders.sql
```

#### Comment superviser et diagnostiquer les problèmes dans dbt ?

Lire la sortie de la console et `logs/dbt.log`, lire le SQL compilé dans `target/compiled` et `target/run`, examiner `run_results.json` pour les échecs et les durées, conserver les échecs de tests, utiliser `dbt retry` après correction, et suivre l'historique et la durée des exécutions dans l'orchestrateur ou la dbt platform. Des alertes sur les échecs de jobs et la fraîcheur des sources détectent les problèmes tôt.

#### Comment déboguer ses modèles dbt ?

Lancer `dbt compile` et exécuter le SQL compilé directement dans l'entrepôt, prévisualiser avec `dbt show`, isoler les CTE pas à pas, utiliser `{{ log() }}` dans Jinja, exécuter avec `--debug` pour des journaux complets, et vérifier les données amont avec des tests.

#### Comment dbt compile-t-il les requêtes ?

dbt analyse le projet et construit le DAG, puis pour chaque nœud il rend le Jinja : il résout `ref`, `source`, `var`, `config` et les appels de macros en SQL simple pour le target courant. Le `SELECT` compilé est écrit dans `target/compiled/`. dbt v2 ajoute ensuite l'analyse statique : il transforme ce SQL en plan logique pour détecter les erreurs et suivre le lignage des colonnes sans interroger l'entrepôt. À l'exécution, la matérialisation enveloppe la requête dans du DDL/DML (`create table as`, `merge`) et l'envoie à l'entrepôt via l'adaptateur.

#### Qu'est-ce que SQLFluff, et que fait `dbt lint` ?

SQLFluff est un linter et formateur SQL avec un mode de templating dbt, utilisé en CI et dans des hooks pre-commit pour imposer un style SQL homogène. dbt v2 inclut `dbt lint`, un linter intégré beaucoup plus rapide qui lit la même configuration `.sqlfluff` et les mêmes codes de règles, et corrige les violations avec `--fix`. Ses résultats peuvent légèrement différer de ceux de SQLFluff.

#### Comment intégrer dbt dans un pipeline de données existant ?

Commencer par déclarer les tables brutes existantes comme sources, puis reproduire les transformations actuelles en modèles de staging et de marts, un domaine à la fois, en comparant les résultats avec les tables historiques (par exemple avec `audit_helper`). Ajouter tests et documentation, lancer dbt depuis l'orchestrateur existant après l'ingestion, basculer les consommateurs vers les nouvelles tables et retirer progressivement les anciens scripts.

#### Qu'est-ce que dbt Mesh ?

Un modèle d'organisation pour les grandes structures où plusieurs projets dbt référencent les modèles publics les uns des autres avec un `ref('project', 'model')` entre projets, avec des groupes, des contrats, des versions et des contrôles d'accès, pour que chaque domaine gère son projet de façon indépendante. Les références entre projets sont une fonction des offres Enterprise de la dbt platform, et Catalog affiche le lignage entre les projets.

<!-- challenge -->

Un modèle renvoie des totaux faux, et le Jinja empêche de voir pourquoi. Quelle est votre première étape ?

<!-- solution -->

Le compiler et exécuter le SQL compilé directement dans l'entrepôt, puis interroger chaque CTE séparément pour trouver où les chiffres divergent. Corriger la logique et ajouter un unit test pour ce cas.

<!-- takeaways -->

- Déboguez le SQL compilé, pas le template.
- Adoptez dbt en déclarant les tables existantes comme sources.
- dbt Mesh relie plusieurs projets par des modèles publics.

### Performances, entrepôts et dépannage

<!-- unit: Des exécutions plus rapides et moins chères -->

<!-- goals -->

- Accélérer les projets dbt avec matérialisations, threads et modèles incrémentaux.
- Trouver les modèles lents et réduire les coûts, y compris sur Snowflake.

<!-- concept -->

La durée d'un projet dbt est la somme de ses requêtes : l'optimisation relève surtout de l'entrepôt. Matérialiser ce qui est souvent interrogé, rendre incrémentaux les gros faits, éviter les longues chaînes de vues qui recalculent tout, et exécuter en parallèle les modèles indépendants avec assez de threads.

Mesurer avant de changer : les durées d'exécution montrent les modèles les plus lents, et le modèle de coût des vues, tables et incrémentaux explique où va l'argent. Le développement peut coûter encore moins avec des échantillons et un defer vers la production.

<!-- example -->

| Matérialisation | Coût de build | Coût de requête |
|---|---|---|
| View | ~0 | Requête complète à chaque lecture |
| Table | Requête complète à chaque build | Faible |
| Incremental | Nouvelles données seulement | Faible |

#### Comment optimiser les performances des transformations dbt sur de gros volumes ?

Matérialiser en tables les modèles coûteux et utiliser des modèles incrémentaux pour les grosses tables de faits, filtrer et agréger tôt, éviter `select *` et les jointures inutiles, partitionner et regrouper les grosses tables sur les colonnes de filtre, utiliser les fonctions natives de l'entrepôt (clés de clustering, clés de tri), limiter les données en développement, et étudier les profils de requêtes et les durées de `run_results.json` pour trouver les modèles les plus lents.

#### Quelles techniques d'optimisation aident à exécuter dbt sur Snowflake ?

Utiliser des tables transitoires pour les modèles intermédiaires (pas de coût de stockage Fail-safe), appliquer du clustering aux très grosses tables sur les colonnes de filtre courantes, dimensionner les warehouses par job (et séparer ceux de dbt et de la BI), utiliser `merge` ou `delete+insert` avec des incremental predicates, s'appuyer sur le clonage sans copie pour la dev et la CI (`dbt clone`), définir un `query_tag` pour attribuer les coûts, et activer la suspension automatique des warehouses.

#### Comment accélérer globalement les exécutions dbt ?

Augmenter les `threads` dans les limites de l'entrepôt (dbt v2 ajuste lui-même le parallélisme sur la plupart des plateformes), supprimer les modèles inutiles, transformer en vues les tables peu interrogées (ou l'inverse pour les vues lourdes), utiliser des modèles incrémentaux, n'exécuter que ce qui a changé (`state:modified+`) en CI, et séparer les jobs selon leurs besoins de fraîcheur.

#### Comment trouver les modèles les plus lents ?

Via les durées de `run_results.json`, la vue des durées de modèles de la dbt platform, ou l'historique des requêtes de l'entrepôt filtré par le `query_tag` de dbt.

#### Quel est l'impact sur les coûts des vues, des tables et des modèles incrémentaux ?

Les vues coûtent du calcul à chaque interrogation. Les tables coûtent du calcul à chaque construction, plus le stockage. Les modèles incrémentaux coûtent peu par exécution mais demandent du soin pour rester justes.

#### Pourquoi une longue chaîne de vues peut-elle être lente ?

Chaque requête sur la vue finale exécute toute la chaîne de SQL sous-jacente. Matérialiser en tables les modèles intermédiaires clés évite de répéter les calculs.

#### Comment limiter les données en développement pour gagner du temps et de l'argent ?

Filtrer par date quand `target.name == 'dev'`, utiliser `--defer` pour réutiliser les parents de production, ou utiliser des clones sans copie. dbt propose aussi deux options intégrées pour `run` et `build` : `--sample="3 days"` restreint à une fenêtre de temps récente chaque `ref` et `source` qui a un `event_time`, et `--empty` les limite à zéro ligne, ce qui vérifie presque sans coût que le SQL s'exécute et crée les bonnes colonnes (utile en CI).

#### Comment comparer dbt et BigQuery ?

Ce ne sont pas des alternatives : BigQuery est un entrepôt de données serverless qui stocke et traite les données, tandis que dbt est un framework de transformation qui génère du SQL et l'exécute dans BigQuery (via dbt-bigquery). Les requêtes planifiées de BigQuery ou Dataform couvrent un terrain proche de dbt, mais dbt apporte la portabilité entre plateformes, un large écosystème de packages et une grande communauté. Sur BigQuery, dbt prend en charge le partitionnement, le clustering et `insert_overwrite`.

<!-- challenge -->

Une exécution nocturne prend 3 heures, mais l'entrepôt montre de longues périodes d'inactivité entre les requêtes. Quel réglage vérifiez-vous d'abord ?

<!-- solution -->

`threads` : s'ils sont trop peu nombreux, les modèles indépendants font la queue. Augmenter les threads dans les limites de concurrence de l'entrepôt, puis examiner le chemin critique du DAG pour trouver les modèles lents.

<!-- takeaways -->

- Matérialisez les modèles très utilisés ; incrémentalisez les gros faits.
- Mesurez avec les durées d'exécution avant d'optimiser.
- Développez sur échantillons avec defer vers la production.

<!-- unit: Problèmes de justesse -->

<!-- goals -->

- Détecter fan-out, doublons et cycles dans les modèles dbt.
- Gérer les changements de schéma des sources.

<!-- concept -->

Certains problèmes produisent des chiffres faux plutôt que des erreurs. Les jointures sur des clés non uniques multiplient les lignes ; les sources qui renvoient des enregistrements créent des doublons ; des colonnes source qui changent cassent des modèles ou font perdre des données en silence. Tests d'unicité et listes de colonnes explicites en détectent la plupart tôt.

Les cycles sont le seul problème que dbt refuse catégoriquement : si deux modèles ont besoin l'un de l'autre, la logique partagée doit aller dans un troisième modèle en amont des deux.

<!-- example -->

```sql
-- staging: keep the latest row per key
select * from {{ source('shop', 'orders') }}
qualify row_number() over (partition by id order by _loaded_at desc) = 1
```

#### Qu'est-ce qui provoque un « fan-out » dans les modèles dbt, et comment le détecter ?

Joindre sur une clé non unique d'un côté multiplie les lignes et gonfle les sommes. Des tests d'unicité sur les clés de jointure et sur la granularité de chaque modèle le détectent.

#### Que faire de dépendances entre modèles qui forment un cycle ?

dbt refuse les cycles. Restructurer la logique, en général en extrayant la partie commune dans un modèle amont référencé par les deux modèles.

#### Comment traiter des lignes en double venant d'une source ?

Les dédoublonner dans le modèle de staging, en général avec une fonction de fenêtrage qui garde la ligne la plus récente par clé, puis tester l'unicité :

```sql
select *
from {{ source('crm', 'customers') }}
qualify row_number() over (partition by customer_id order by updated_at desc) = 1
```

#### Comment gérer les changements de schéma des sources ?

Les détecter avec des tests et des contrats, utiliser des listes de colonnes explicites en staging plutôt que `select *`, configurer `on_schema_change` pour les modèles incrémentaux, et adapter les modèles de staging à un seul endroit.

<!-- challenge -->

Le modèle A fait un ref sur B pour les segments clients, et B a maintenant besoin des totaux de commandes de A. dbt signale un cycle. Comment restructurer ?

<!-- solution -->

Déplacer la logique partagée dans un nouveau modèle en amont (par exemple `int_customer_orders` avec les totaux de commandes par client) que A et B référencent tous deux, supprimant la dépendance mutuelle.

<!-- takeaways -->

- Le fan-out vient de clés de jointure non uniques.
- Dédupliquez les sources au staging.
- Cassez les cycles avec un modèle partagé en amont.

<!-- unit: Dépannage en production -->

<!-- goals -->

- Comprendre ce qui se passe quand un modèle échoue en cours d'exécution.
- Superviser les exécutions de production et analyser les ralentissements.

<!-- concept -->

En production, le DAG contient les échecs : un modèle en échec saute ses enfants tandis que les branches indépendantes se terminent. Après correction, ne relancer que la partie en échec évite de tout reconstruire.

La supervision transforme les exécutions en tendances : échecs, résultats de tests et durées dans le temps. Quand un job prend soudain deux fois plus de temps, la cause est généralement la croissance des données, un filtre incrémental perdu, une matérialisation modifiée ou de la contention dans l'entrepôt, et comparer les exécutions désigne laquelle.

<!-- example -->

```text
run 2026-10-16: 41 min   run 2026-10-17: 88 min
slowest node change: fct_events 6 min → 52 min
manifest diff: fct_events materialized 'incremental' → 'table' (PR #212)
```

#### Que se passe-t-il quand un modèle échoue au milieu d'une exécution ?

Ses modèles en aval sont ignorés, les branches indépendantes continuent, et l'exécution signale l'échec. Corriger puis lancer `dbt retry`, ou relancer le modèle en échec et ses enfants avec `model+`.

#### Comment superviser et diagnostiquer les problèmes de dbt en production ?

Des alertes sur les échecs de jobs et les erreurs de tests, le suivi de l'évolution des échecs de tests et des durées d'exécution, le contrôle de la fraîcheur des sources avant l'exécution, la conservation des artefacts pour comparaison, et une procédure d'astreinte documentée (examiner les journaux et le SQL compilé, relancer avec `dbt retry`, informer les consommateurs des incidents de données).

#### Que vérifier quand un job dbt prend soudain deux fois plus de temps ?

La croissance des volumes dans les sources, un modèle qui a changé de matérialisation ou perdu son filtre incrémental, un full refresh lancé par erreur, la taille du warehouse ou la file d'attente, une nouvelle jointure qui multiplie les lignes, et l'absence d'élagage des partitions.

<!-- challenge -->

Une exécution de production a échoué sur un mart à 05:00. Après correction du SQL, comment terminer rapidement l'exécution ?

<!-- solution -->

Déployer la correction et lancer `dbt retry` (ou `dbt build --select <failed_model>+`), qui reconstruit le modèle en échec et ses enfants sautés sans relancer tout ce qui a réussi.

<!-- takeaways -->

- Un échec saute les enfants ; les branches indépendantes continuent.
- `dbt retry` reprend à partir des échecs.
- Comparez les durées pour expliquer les ralentissements.
