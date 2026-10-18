## Fiche d'étude dbt

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude dbt : environ 200 questions](../../images/dbt_study_guide_title_img.png)

Environ 200 questions d'entretien sur dbt (data build tool), des bases aux modèles incrémentaux, snapshots, tests, déploiement et performances. Les réponses suivent les conventions de dbt Core 1.x. Ouvrez une question pour voir sa réponse, ou utilisez le filtre pour chercher dans toute la fiche.

<!-- QA -->

### Fondamentaux

#### Qu'est-ce que dbt ?

dbt (data build tool) est un framework de transformation : on écrit des requêtes `SELECT` sous forme de modèles, et dbt les compile avec Jinja, déduit leurs dépendances et les exécute dans l'entrepôt de données sous forme de tables ou de vues. Il apporte aux transformations SQL les pratiques du génie logiciel (gestion de versions, tests, documentation, modularité, CI/CD). dbt est le « T » de l'ELT.

#### Quels sont les cas d'usage courants de dbt ?

Construire un entrepôt de données ou un lakehouse couche par couche (staging, intermédiaire, marts), nettoyer et normaliser des données brutes, construire des modèles dimensionnels pour la BI, historiser des données à évolution lente avec des snapshots, tester la qualité des données, documenter les jeux de données avec leur lignage, et définir des indicateurs métier partagés dans la couche sémantique.

#### En quoi dbt diffère-t-il des outils ETL traditionnels ?

Les outils ETL traditionnels extraient, transforment dans leur propre moteur puis chargent, souvent via une interface graphique. dbt ne fait que transformer, dans l'entrepôt qui contient déjà les données chargées (ELT), avec du SQL dans des fichiers texte. Tout est du code : versionné dans Git, relu, testé et déployé comme un logiciel. L'extraction et le chargement sont confiés à d'autres outils (Fivetran, Airbyte, pipelines maison).

#### Comment dbt se compare-t-il à Apache Spark ?

Spark est un moteur de traitement distribué qu'on programme en Python, Scala ou SQL, et dont on gère les jobs et les clusters. dbt n'est pas un moteur : il génère du SQL et l'envoie à un moteur (Snowflake, BigQuery, Redshift, Databricks, Postgres, et Spark lui-même via les adaptateurs dbt-spark ou dbt-databricks). Ils sont complémentaires : dbt peut orchestrer des transformations SQL exécutées par Spark, tandis que les traitements complexes non SQL restent en code Spark.

#### Que signifie ELT, et pourquoi dbt s'y prête-t-il ?

Extract, Load, Transform : les données brutes sont d'abord chargées dans l'entrepôt, puis transformées sur place. Les entrepôts modernes sont peu coûteux en stockage et puissants en calcul : transformer en SQL là où se trouvent déjà les données est plus simple et passe à l'échelle. dbt structure cette étape de transformation.

#### Quelle est la différence entre dbt Core et dbt Cloud ?

dbt Core est l'outil en ligne de commande open source (Apache 2.0) : on l'installe, on l'exécute et on l'orchestre soi-même. dbt Cloud (aujourd'hui intégré à la dbt platform) est le service commercial géré : un IDE web, un planificateur de jobs, la CI, la documentation hébergée, la couche sémantique, des alertes et le contrôle d'accès. Les deux exécutent le même code de projet.

#### Qu'est-ce qu'un adaptateur dbt ?

Un plugin qui permet à dbt de dialoguer avec une plateforme de données donnée, en traduisant les opérations génériques de dbt dans le dialecte SQL de cette plateforme : dbt-postgres, dbt-snowflake, dbt-bigquery, dbt-redshift, dbt-databricks, dbt-spark et de nombreux adaptateurs communautaires.

#### Qu'est-ce qu'un modèle dbt ?

Un fichier `.sql` du dossier `models/` qui contient une requête `SELECT`. dbt l'enveloppe dans le DDL nécessaire pour créer une vue, une table ou un autre objet portant le nom du fichier. Des modèles Python (`.py`) sont aussi pris en charge sur certaines plateformes.

#### Qu'est-ce que le DAG dans le contexte de dbt ?

Le graphe orienté acyclique des dépendances entre modèles, sources, seeds et snapshots, construit à partir des appels à `ref()` et `source()`. dbt s'en sert pour exécuter les nœuds dans le bon ordre (et en parallèle quand c'est possible), pour sélectionner des parties du projet et pour dessiner le lignage dans la documentation.

#### Quelles sont les difficultés de dbt ?

Il ne couvre que la transformation : il faut d'autres outils pour l'ingestion et l'orchestration. Les gros projets peuvent devenir lents à compiler et difficiles à parcourir sans conventions. Les modèles incrémentaux et les snapshots demandent une conception soignée. Jinja peut rendre le SQL illisible s'il est surutilisé. Les performances dépendent toujours de l'entrepôt et du SQL écrit, et les coûts peuvent grimper si les full refresh sont trop fréquents.

#### Quels problèmes dbt résout-il par rapport aux procédures stockées et aux scripts ?

Les dépendances sont explicites et résolues automatiquement, le code est modulaire et réutilisable grâce à `ref` et aux macros, les tests et la documentation vivent à côté du code, on change d'environnement par la configuration et non en modifiant le code, et tout est versionné et relisible.

#### Quelles sont les commandes dbt les plus courantes ?

`dbt run` (construire les modèles), `dbt test` (exécuter les tests), `dbt build` (run, test, snapshot et seed dans l'ordre du DAG), `dbt seed`, `dbt snapshot`, `dbt compile`, `dbt docs generate` / `dbt docs serve`, `dbt debug`, `dbt deps`, `dbt clean`, `dbt ls`, `dbt source freshness` et `dbt run-operation`.

#### Que fait `dbt build` ?

Il exécute les seeds, les modèles, les snapshots et les tests dans l'ordre du DAG. Si un test échoue sur un nœud, les nœuds qui en dépendent sont ignorés, pour que des données erronées ne se propagent pas.

#### À quoi sert `dbt debug` ?

Il vérifie l'installation, `dbt_project.yml`, `profiles.yml` et la connexion à l'entrepôt. C'est la première commande à lancer quand rien ne fonctionne.

#### Quelle est la différence entre `dbt run` et `dbt compile` ?

`dbt compile` rend le Jinja et écrit le SQL obtenu dans `target/compiled/` sans rien exécuter. `dbt run` compile et exécute, et écrit les requêtes exécutées (avec leur DDL) dans `target/run/`.

#### Dans quels langages peut-on écrire des modèles dbt ?

En SQL (avec Jinja) partout, et en Python sur Snowflake (Snowpark), Databricks et BigQuery (Dataproc). Les modèles Python renvoient un DataFrame et servent pour la logique difficile à exprimer en SQL.

#### Qu'est-ce qu'un modèle Python dans dbt ?

Un fichier `.py` qui définit `model(dbt, session)` et renvoie un DataFrame. Il peut référencer d'autres modèles avec `dbt.ref()` et est matérialisé en table ou en modèle incrémental.

```python
def model(dbt, session):
    dbt.config(materialized="table")
    orders = dbt.ref("stg_orders")
    return orders.groupBy("customer_id").count()
```

#### Qu'est-ce que dbt Fusion ?

Un nouveau moteur dbt écrit en Rust, présenté en 2025, qui analyse et compile les projets beaucoup plus vite et comprend le SQL sémantiquement (lignage au niveau des colonnes, détection des erreurs avant qu'elles n'atteignent l'entrepôt). Il fait tourner l'extension dbt pour VS Code et la dbt platform.

#### Qu'est-ce que la couche sémantique de dbt ?

Une couche, fondée sur MetricFlow, où les indicateurs (chiffre d'affaires, utilisateurs actifs) sont définis une seule fois en YAML au-dessus de modèles sémantiques, puis interrogés de façon cohérente par la BI et d'autres outils via des API, pour que chaque outil calcule l'indicateur de la même façon.

#### Que signifie « modélisation de données modulaire » dans dbt ?

Découper les transformations en petits modèles réutilisables avec une seule responsabilité chacun (staging par source, logique intermédiaire, marts finaux), reliés par `ref`, au lieu de grosses requêtes monolithiques.

### Projets et configuration

#### Qu'est-ce qu'un projet dbt ?

Un répertoire qui contient un fichier `dbt_project.yml`, ainsi que des modèles, tests, macros, seeds, snapshots, analyses et de la documentation. C'est l'unité que dbt compile et exécute, en général un dépôt Git.

#### Quelle est la structure d'un projet ?

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
```

#### Que contient `dbt_project.yml` ?

Le nom et la version du projet, le `profile` à utiliser, les chemins (models, seeds, macros…), les `vars` et les configurations par défaut de chaque dossier, comme `+materialized: table` pour tous les marts ou `+schema: staging`.

#### Qu'est-ce que `profiles.yml` ?

Le fichier (par défaut dans `~/.dbt/`) qui contient les informations de connexion de chaque profil et target : type d'adaptateur, hôte, base de données, schéma, identifiants et threads. Il reste hors du dépôt du projet car il contient des secrets. Les valeurs peuvent venir de variables d'environnement avec `env_var()`.

#### Qu'est-ce qu'un target dans dbt ?

Une configuration de connexion nommée au sein d'un profil, comme `dev` et `prod`. On la choisit avec `--target`, et les modèles peuvent varier selon `target.name`.

#### Que sont les threads dans dbt ?

Le nombre maximal de modèles que dbt exécute en même temps. Les branches indépendantes du DAG s'exécutent en parallèle jusqu'à cette limite.

#### Comment configure-t-on un modèle ?

À trois endroits, du plus précis au moins précis : un bloc `{{ config(...) }}` dans le fichier du modèle, un bloc `config:` dans les propriétés YAML du modèle et les réglages par dossier dans `dbt_project.yml`. Le plus précis l'emporte.

```sql
{{ config(materialized='table', schema='marts', tags=['daily']) }}
select * from {{ ref('int_orders') }}
```

#### Quelle est la différence entre configs et properties ?

Les configs contrôlent la façon dont dbt construit un nœud (matérialisation, schéma, tags, hooks). Les properties le décrivent (description, colonnes, tests, documentation). Les properties vivent dans des fichiers YAML. Les configs peuvent être en YAML, dans le fichier du modèle ou dans `dbt_project.yml`.

#### À quoi servent les tags ?

À étiqueter des nœuds pour les sélectionner dans les commandes, par exemple `dbt run --select tag:daily`, ou les regrouper dans des jobs.

#### Comment fonctionne la sélection de nœuds ?

Avec `--select` et `--exclude`, à partir de noms, de chemins, de tags, de `source:`, `state:`, `resource_type:` et d'opérateurs de graphe : `+model` sélectionne le modèle et ses parents, `model+` le modèle et ses enfants, `@model` le modèle, ses enfants et leurs parents.

```bash
dbt build --select +fct_orders          # fct_orders et tout ce qui est en amont
dbt run --select staging.stripe         # un dossier
dbt test --select source:stripe+        # tests d'une source et de tout ce qui en dépend
```

#### Que sont les packages, et comment les installer ?

Des projets dbt réutilisables (macros, modèles, tests) comme `dbt_utils`, `dbt_expectations` ou `codegen`. On les liste dans `packages.yml` (ou `dependencies.yml`) et on lance `dbt deps`.

#### Qu'est-ce que `dbt_utils` ?

Le package le plus utilisé, avec des tests génériques (`unique_combination_of_columns`, `expression_is_true`, `accepted_range`) et des macros (`generate_surrogate_key`, `star`, `date_spine`, `pivot`, `union_relations`).

#### Que sont les variables (`vars`) dans dbt ?

Des valeurs définies dans `dbt_project.yml` ou passées en ligne de commande (`--vars '{start_date: 2026-01-01}'`) et lues avec `{{ var('start_date') }}`.

#### Comment utilise-t-on les variables d'environnement dans dbt ?

Avec `{{ env_var('DBT_PASSWORD') }}`, éventuellement avec une valeur par défaut. On s'en sert surtout dans `profiles.yml` pour les identifiants, et les variables préfixées `DBT_ENV_SECRET_` sont masquées dans les journaux.

#### Comment dbt choisit-il le schéma dans lequel un modèle est construit ?

Grâce à la macro `generate_schema_name`. Par défaut, un schéma personnalisé est ajouté au schéma du target (`dbt_alice_marts` en dev, `analytics_marts` en prod). Beaucoup de projets redéfinissent la macro pour utiliser le schéma personnalisé tel quel en production.

#### Qu'est-ce que la macro `generate_schema_name`, et pourquoi la redéfinir ?

Elle calcule le schéma de chaque nœud. La redéfinir permet, par exemple, d'utiliser des noms de schéma exacts en production tout en gardant un préfixe personnel en développement, pour que les développeurs ne s'écrasent pas mutuellement.

#### Que sont les analyses dans dbt ?

Des fichiers SQL du dossier `analyses/` qui sont compilés (Jinja et `ref` résolus) mais jamais exécutés par `dbt run`. Utiles pour des requêtes ponctuelles qui profitent des références de dbt.

#### Que fait `dbt clean` ?

Il supprime les dossiers listés dans `clean-targets` (en général `target/` et `dbt_packages/`).

#### Que sont l'accès aux modèles et les groupes ?

Des fonctions de gouvernance. L'`access` d'un modèle peut être `private` (référençable seulement dans son groupe), `protected` (dans le projet, la valeur par défaut) ou `public` (depuis d'autres projets). Les groupes attribuent la responsabilité d'un ensemble de modèles.

#### Que sont les versions de modèles ?

Un moyen de publier une nouvelle version d'un modèle public (`fct_orders_v2`) pendant que les consommateurs continuent d'utiliser l'ancienne jusqu'à leur migration, avec `ref('fct_orders', v=1)`.

### Sources et seeds

#### Que sont les sources dans dbt ?

Des déclarations, en YAML, des tables brutes chargées dans l'entrepôt par d'autres outils. Les modèles les lisent avec `{{ source('stripe', 'payments') }}` au lieu de noms de tables écrits en dur, ce qui enregistre le lignage, permet des tests et de la documentation sur les données brutes et active les contrôles de fraîcheur.

```yaml
sources:
  - name: stripe
    database: raw
    schema: stripe
    tables:
      - name: payments
        loaded_at_field: _loaded_at
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
```

#### Pourquoi utiliser `source()` plutôt que d'écrire le nom de la table ?

L'emplacement de la table est défini à un seul endroit, le lignage commence à la source dans le DAG, les sources peuvent être sélectionnées (`source:stripe+`) et `dbt source freshness` peut les contrôler.

#### Qu'est-ce que la fraîcheur des sources (source freshness) ?

Un contrôle, lancé avec `dbt source freshness`, qui compare le maximum de `loaded_at_field` à l'heure actuelle et avertit ou échoue quand les données sont plus anciennes que les seuils configurés.

#### Peut-on tester les sources ?

Oui, on déclare des tests génériques sur les colonnes des sources exactement comme sur les modèles, ce qui détecte les problèmes des données brutes avant qu'ils n'atteignent les modèles.

#### Qu'est-ce qu'un modèle de staging ?

La première couche au-dessus d'une source : un modèle par table source, avec des transformations légères (renommage, conversion de types, nettoyage de base, dédoublonnage). Tout ce qui suit référence les modèles de staging, pas directement les sources.

#### Pourquoi seuls les modèles de staging devraient-ils référencer les sources ?

Pour que chaque table brute soit nettoyée une seule fois, à un seul endroit. Si la source change, seul son modèle de staging doit être modifié.

#### Qu'est-ce qu'un seed ?

Un fichier CSV du dossier `seeds/` que `dbt seed` charge dans l'entrepôt sous forme de table. Les modèles le référencent avec `ref()` comme n'importe quel modèle.

#### Quand utiliser des seeds, et quand ne pas le faire ?

Pour de petites données de référence statiques, qui changent rarement et ont leur place dans la gestion de versions : codes pays, tables de correspondance, jeux de test. Pas pour des données volumineuses ou qui changent souvent, ni pour des données qui devraient venir d'un système source.

#### Comment fixer les types de colonnes d'un seed ?

Avec `column_types` dans la configuration du seed, sinon dbt les infère :

```yaml
seeds:
  my_project:
    country_codes:
      +column_types:
        code: varchar(2)
```

#### Comment recharger un seed dont les colonnes ont changé ?

Avec `dbt seed --full-refresh`, qui supprime et recrée la table au lieu de la vider puis d'insérer.

#### dbt peut-il travailler avec différentes sources de données et différents entrepôts ?

dbt travaille avec une plateforme de données par target, via son adaptateur, et transforme des données déjà présentes sur cette plateforme. Il n'extrait pas depuis les systèmes sources. Les plateformes capables d'interroger des données externes (tables externes Snowflake, requêtes fédérées BigQuery, catalogues Databricks et Trino) permettent à dbt de transformer des données de plusieurs origines via l'entrepôt.

#### Quelle est la différence entre `ref()` et `source()` ?

`ref()` pointe vers un autre nœud dbt (modèle, seed, snapshot) et crée une dépendance que le DAG utilise pour ordonner les exécutions. `source()` pointe vers des données brutes chargées hors de dbt. Les deux se résolvent en nom de table complet pour le target courant.

#### En quoi `ref()` se résout-il selon l'environnement ?

En la relation dans la base et le schéma du target courant : le même code construit dans le schéma d'un développeur en dev et dans les schémas de production en prod.

#### Qu'est-ce que l'organisation en couches « staging, intermediate, marts » ?

Une structure courante : staging nettoie chaque source, intermediate contient des jointures et une logique métier réutilisables, les marts sont les tables de faits et de dimensions finales (ou des tables larges) consommées par la BI et les analystes.

#### À quoi sert `dbt source freshness` en production ?

À détecter une ingestion cassée ou en retard avant que les modèles ne tournent sur des données périmées, souvent en première étape d'un job planifié.

### Modèles et matérialisations

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
- **materialized_view** : une vue matérialisée de la base, là où elle est prise en charge.
Les snapshots et les seeds sont des types de ressources distincts, avec leur propre comportement.

#### Quand utiliser une vue plutôt qu'une table ?

Les vues sont peu coûteuses à construire et toujours à jour : elles conviennent au staging et aux transformations légères. Les tables sont plus rapides à interroger : elles conviennent aux marts utilisés par la BI et aux modèles coûteux à calculer ou très interrogés.

#### Quand utiliser un modèle ephemeral ?

Pour une logique légère et réutilisable qu'on ne veut pas voir comme un objet distinct dans l'entrepôt. Les multiplier complique le débogage, car on ne peut pas les interroger directement.

#### Comment créer une matérialisation personnalisée dans dbt ?

Avec un bloc `{% materialization name, adapter='default' %}` dans un fichier de macros. En général, il récupère la relation cible, exécute les pre-hooks, construit le SQL avec `{% call statement('main') %}`, gère les relations existantes, exécute les post-hooks et renvoie `{'relations': [target_relation]}`. Les matérialisations personnalisées sont rares : les matérialisations intégrées et les stratégies incrémentales couvrent presque tous les besoins.

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

#### Que sont les hooks ?

Du SQL exécuté à des moments précis : `pre-hook` et `post-hook` autour d'un modèle, `on-run-start` et `on-run-end` autour de toute l'invocation. Usages : accorder des privilèges, créer des index ou journaliser les exécutions.

#### Que sont le pre-hook et le post-hook ?

Un `pre-hook` exécute du SQL juste avant la construction d'un modèle, un `post-hook` juste après, dans la même exécution. Par exemple :

```sql
{{ config(post_hook="grant select on {{ this }} to role reporter") }}
```

#### À quoi fait référence `{{ this }}` ?

À la relation (base.schéma.table) du modèle en cours de construction. On l'utilise dans les hooks et dans les modèles incrémentaux pour interroger la table existante.

#### Que sont les contrats de modèle ?

Une configuration `contract: {enforced: true}` avec des noms et types de colonnes déclarés (et des contraintes là où elles sont prises en charge). dbt vérifie que la sortie du modèle correspond avant de le construire, ce qui protège les consommateurs des changements de schéma.

#### Que sont les contraintes (constraints) dans dbt ?

Des déclarations comme `not_null`, `unique`, `primary_key`, `foreign_key` et `check` sur des modèles sous contrat. dbt les ajoute au DDL quand la plateforme les applique. Beaucoup d'entrepôts n'enregistrent certaines que comme métadonnées : les tests restent nécessaires.

#### Quelle est la différence entre `dbt run --full-refresh` et une exécution normale ?

`--full-refresh` supprime et reconstruit entièrement les modèles incrémentaux et recharge les seeds, au lieu de ne traiter que les nouvelles données.

#### Que fait l'option `--defer` ?

Avec `--state` pointant vers les artefacts de production, elle fait résoudre `ref()` vers les relations de production pour les modèles que vous n'avez pas construits dans votre environnement : on peut exécuter un modèle en dev sans reconstruire tous ses parents.

#### Qu'est-ce que `dbt clone` ?

Une commande qui crée des copies (clones sans copie de données quand c'est possible, sinon des vues) des modèles de production dans un autre environnement, à partir de l'état de production. Elle accélère la CI et la préparation des environnements de développement.

#### Qu'est-ce que `dbt show` ?

Une commande pour prévisualiser le résultat d'un modèle ou d'une requête sans le matérialiser : `dbt show --select stg_orders --limit 10`.

#### Qu'est-ce que `dbt retry` ?

Elle relance uniquement les nœuds qui ont échoué ou ont été ignorés lors de l'invocation précédente.

#### Comment traiter l'erreur « relation does not exist » dans dbt ?

Causes fréquentes : une table référencée n'a jamais été construite dans le target courant (lancez le parent ou utilisez `--defer`), le nom de table est écrit en dur au lieu d'utiliser `ref`/`source` (la dépendance n'est donc pas connue et l'ordre est faux), la définition de la source pointe vers la mauvaise base ou le mauvais schéma, l'utilisateur n'a pas le droit de voir l'objet, ou l'identifiant a un problème de guillemets ou de casse. Lancer `dbt compile` et lire le SQL dans `target/compiled/` montre en général quel nom est faux.

#### Qu'est-ce que le rafraîchissement des données (data refresh) ?

Mettre à jour les tables de l'entrepôt pour qu'elles reflètent les dernières données sources : un `dbt build` planifié qui reconstruit les tables, traite les nouvelles lignes des modèles incrémentaux et capture les changements dans les snapshots. Sa fréquence dépend de la fraîcheur attendue par les consommateurs et du rythme de chargement des sources.

#### Qu'est-ce qu'un modèle désactivé ?

Un modèle avec `enabled: false`. dbt l'ignore, ce qui est utile pour des modèles propres à une plateforme ou en cours de développement.

#### Qu'est-ce que la configuration `alias` ?

Elle fixe le nom de la relation dans l'entrepôt indépendamment du nom du fichier du modèle.

### Jinja et macros

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

#### Que sont les macros dans dbt, et comment les exécuter ?

Des morceaux de Jinja réutilisables (qui génèrent souvent du SQL), définis avec `{% macro name(args) %}...{% endmacro %}` dans le dossier `macros/`. On les appelle dans des modèles, des tests ou des hooks avec `{{ name(args) }}`, ou on les exécute directement avec `dbt run-operation name --args '{...}'`.

#### Quelle est la différence entre `{{ }}`, `{% %}` et `{# #}` ?

`{{ }}` affiche une expression, `{% %}` exécute une instruction (if, for, set, macro, call), et `{# #}` est un commentaire qui n'apparaît pas dans le SQL compilé.

#### Que fait le `-` dans `{%-` ou `-%}` ?

Il supprime les espaces avant ou après la balise, pour garder un SQL compilé propre.

#### Comment écrire une macro avec un argument par défaut ?

```sql
{% macro cents_to_euros(column, scale=2) %}
    round({{ column }} / 100.0, {{ scale }})
{% endmacro %}
```

Appelée avec `{{ cents_to_euros('amount') }}`.

#### Que fait `run_query` ?

Elle exécute une requête pendant la compilation et renvoie le résultat sous forme de table agate, par exemple pour construire une liste de valeurs distinctes utilisée dans une boucle. Elle ne renvoie des données qu'à l'exécution, d'où la garde habituelle `{% if execute %}`.

#### Qu'est-ce que la variable `execute` ?

Un booléen qui vaut false pendant l'analyse du projet et true quand dbt exécute réellement les nœuds. Le code qui interroge la base doit être placé dans `{% if execute %}`, car la base n'est pas interrogée pendant l'analyse.

#### Qu'est-ce qu'`adapter.dispatch` ?

Un mécanisme pour implémenter une macro différemment selon la base, afin que les packages fonctionnent avec plusieurs adaptateurs : dbt choisit `snowflake__my_macro`, `bigquery__my_macro` ou `default__my_macro` selon l'adaptateur.

#### Qu'est-ce que la variable `target` dans Jinja ?

Des informations sur la connexion courante : `target.name`, `target.schema`, `target.type`, `target.threads`. On s'en sert souvent pour limiter les données en développement :

```sql
{% if target.name == 'dev' %} where created_at >= dateadd(day, -3, current_date) {% endif %}
```

#### Comment définir une variable dans un modèle ?

Avec `{% set %}`, par exemple `{% set payment_methods = ['card', 'paypal'] %}`, puis on l'utilise dans des boucles ou des expressions.

#### À quoi sert `log()` dans les macros ?

À afficher des messages dans la console ou le fichier de journal pendant la compilation, pour déboguer : `{{ log("value: " ~ my_var, info=true) }}`.

#### Qu'est-ce que l'objet `config` dans Jinja ?

Il lit la configuration d'un modèle à l'intérieur des macros, par exemple `config.get('unique_key')`.

#### Que sont les variables de contexte `graph` et `model` ?

`graph` expose le projet analysé (tous les nœuds et leurs métadonnées), et `model` le nœud courant, que les macros peuvent inspecter, par exemple pour générer de la documentation ou des audits.

#### À quoi sert `dbt run-operation` ?

À exécuter une macro en dehors de la construction, pour des tâches d'administration : accorder des droits, supprimer d'anciens schémas, charger des données ou générer du code avec le package `codegen`.

#### Qu'est-ce que le package `codegen` ?

Un package de macros qui génèrent le YAML et le SQL répétitifs, comme les définitions de sources à partir d'un schéma ou un modèle de staging à partir d'une table source.

#### Comment redéfinir une macro intégrée de dbt ?

En définissant une macro du même nom dans le projet, par exemple `generate_schema_name` ou `generate_alias_name`. La version du projet a priorité sur celle fournie par dbt.

#### Que fait `return()` dans une macro ?

Il renvoie un objet Python (liste, dictionnaire, nombre) au lieu de texte rendu, pour qu'une autre macro puisse utiliser la valeur.

#### Que sont les filtres Jinja ? Donnez des exemples.

Des fonctions appliquées avec `|`, comme `{{ name | upper }}`, `{{ columns | join(', ') }}` ou `{{ value | default('n/a') }}`.

#### Comment éviter de trop complexifier le code avec Jinja ?

Écrire d'abord du SQL simple, n'extraire une macro que lorsque la logique se répète ou doit varier selon l'adaptateur, documenter les arguments des macros, et vérifier que le SQL compilé reste lisible.

#### Qu'est-ce que la macro `star` de dbt_utils ?

`{{ dbt_utils.star(ref('model'), except=['col']) }}` génère la liste des colonnes d'une relation, moins certaines, pour éviter `select *` sans saisir chaque colonne.

### Tests et qualité des données

#### Quels sont les deux types de tests dans dbt ?

Les **tests de données** vérifient les données dans l'entrepôt : tests génériques (réutilisables, paramétrés, déclarés en YAML) et tests singuliers (requêtes SQL ponctuelles dans `tests/`). Les **tests unitaires**, ajoutés dans dbt 1.8, vérifient la logique SQL d'un modèle sur de petites entrées simulées avant de l'exécuter sur de vraies données.

#### Quels types de tests peut-on exécuter dans dbt ?

Les quatre tests génériques intégrés (`unique`, `not_null`, `accepted_values`, `relationships`), des tests génériques de packages (`dbt_utils`, `dbt_expectations`) ou maison, des tests SQL singuliers, des tests unitaires, des contrôles de fraîcheur des sources et des contrats de modèle.

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
              values: ['placed', 'shipped', 'returned']
      - name: customer_id
        data_tests:
          - relationships:
              to: ref('dim_customers')
              field: customer_id
```

dbt transforme chacun en une requête qui renvoie les lignes en échec. Le test réussit quand la requête ne renvoie aucune ligne.

#### Qu'est-ce qu'un test singulier ?

Un fichier `.sql` du dossier `tests/` qui sélectionne les lignes qui violent une règle. Il échoue s'il renvoie au moins une ligne :

```sql
-- tests/assert_no_negative_amounts.sql
select * from {{ ref('fct_orders') }} where amount < 0
```

#### Comment écrire un test générique personnalisé ?

Avec un bloc `{% test name(model, column_name) %}` qui renvoie les lignes en échec, puis on l'utilise en YAML comme un test intégré :

```sql
{% test is_positive(model, column_name) %}
select * from {{ model }} where {{ column_name }} <= 0
{% endtest %}
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

#### Quelle est la différence entre un test unitaire et un test de données ?

Un test unitaire vérifie le code sur des entrées fixes et s'exécute avant la construction du modèle, en général en CI. Un test de données vérifie les vraies données après la construction du modèle, à chaque exécution.

#### Qu'est-ce que la sévérité d'un test ?

Un réglage `severity: warn` ou `error` (par défaut). Avec des seuils `warn_if` et `error_if` comme `">10"`, un test peut avertir pour quelques échecs et n'échouer qu'au-delà d'une limite.

#### Comment conserver les échecs des tests ?

Avec `--store-failures` ou `store_failures: true`, dbt enregistre les lignes en échec dans une table d'un schéma d'audit, pour les examiner après l'exécution.

#### Que fait la configuration `where` d'un test ?

Elle limite le test à un sous-ensemble de lignes, par exemple les données récentes : `config: {where: "order_date >= current_date - 7"}`.

#### Qu'est-ce que `dbt_expectations` ?

Un package de tests génériques inspiré de Great Expectations : plages de valeurs, expressions régulières, nombre de lignes, distributions, types de colonnes, etc.

#### Comment vérifier qu'une combinaison de colonnes est unique ?

Avec `dbt_utils.unique_combination_of_columns` :

```yaml
data_tests:
  - dbt_utils.unique_combination_of_columns:
      combination_of_columns: [order_id, line_number]
```

#### Que faut-il tester au minimum sur chaque modèle ?

La clé primaire avec `unique` et `not_null`, les clés étrangères des jointures importantes avec `relationships`, et les colonnes catégorielles avec `accepted_values`. Ajoutez des règles métier là où une erreur coûterait cher.

#### Que signifie « tester à la source » ?

Placer des tests sur les sources et les modèles de staging, pour détecter les problèmes des données brutes à l'entrée plutôt que de les découvrir dans un tableau de bord.

#### Comment éviter la lassitude face aux alertes des tests dbt ?

Utiliser la sévérité `warn` et des seuils pour les contrôles non critiques, tester ce qui compte pour les consommateurs, supprimer les tests qui ne détectent jamais rien d'utile, et envoyer les erreurs à leurs responsables.

#### Comment dbt garantit-il la qualité des données tout au long du pipeline ?

Par des tests à chaque couche, la fraîcheur des sources, des contrats sur les modèles publics, `dbt build` qui ignore les modèles en aval quand un test échoue, et une CI qui exécute les modèles modifiés et leurs tests avant la fusion.

#### Quelle est la différence entre `dbt test` et `dbt build` pour les tests ?

`dbt test` exécute les tests sur des modèles déjà construits. `dbt build` alterne construction et tests dans l'ordre du DAG : un test en échec empêche la construction de ses enfants.

#### Comment comparer le nombre de lignes d'un modèle à celui d'un autre ?

Avec un test de package comme `dbt_utils.equal_rowcount` ou `dbt_expectations.expect_table_row_count_to_equal_other_table`, ou un test singulier qui compare les comptes.

#### Comment vérifier qu'une valeur est dans une plage ?

Avec `dbt_utils.accepted_range` (`min_value`, `max_value`) ou `dbt_expectations.expect_column_values_to_be_between`.

#### Qu'est-ce qu'un test de récence ?

Un test comme `dbt_utils.recency` qui échoue quand l'horodatage le plus récent d'un modèle est plus ancien qu'un seuil, et repère ainsi les modèles qui ne reçoivent plus de données.

### Modèles incrémentaux

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

True seulement si le modèle est incrémental, que la table cible existe déjà et que l'exécution n'est pas un `--full-refresh`.

#### Qu'est-ce que `unique_key` dans un modèle incrémental ?

La colonne (ou la liste de colonnes) qui identifie une ligne. Avec elle, les lignes déjà présentes sont mises à jour au lieu d'être dupliquées, selon la stratégie.

#### Quelles stratégies incrémentales existe-t-il ?

Selon l'adaptateur : `append` (insertion seule), `merge` (upsert sur `unique_key`), `delete+insert` (suppression des clés correspondantes puis insertion), `insert_overwrite` (remplacement de partitions entières, BigQuery et Spark) et `microbatch` (traitement par lots temporels).

#### Comment dbt gère-t-il le chargement incrémental des données des systèmes sources ?

dbt n'extrait pas des systèmes sources : il traite des données déjà chargées dans l'entrepôt. Les modèles incrémentaux ne sélectionnent que les lignes plus récentes que les dernières traitées (via un horodatage ou un identifiant), puis les fusionnent ou les ajoutent. Des outils de chargement comme Fivetran ou Airbyte apportent les données de façon incrémentale, et dbt les transforme de façon incrémentale.

#### Qu'est-ce que la stratégie microbatch ?

Ajoutée dans dbt 1.9, elle traite les données en lots temporels indépendants (par exemple un par jour) selon une colonne `event_time` : les lots peuvent être relancés, exécutés en parallèle ou recalculés avec `--event-time-start` et `--event-time-end`.

#### Comment gérer les données qui arrivent en retard dans un modèle incrémental ?

Avec une fenêtre de retraitement plutôt qu'un « supérieur à » strict : retraiter les derniers jours, et s'appuyer sur `unique_key` avec `merge` pour mettre à jour les lignes déjà chargées.

```sql
{% if is_incremental() %}
where event_time >= (select dateadd(day, -3, max(event_time)) from {{ this }})
{% endif %}
```

#### Que fait `on_schema_change` ?

Il définit ce qui se passe quand les colonnes d'un modèle incrémental changent : `ignore` (par défaut), `fail`, `append_new_columns` ou `sync_all_columns`.

#### Quand faut-il faire un full refresh d'un modèle incrémental ?

Quand la logique change d'une manière qui affecte les lignes historiques, quand les colonnes changent d'une façon que `on_schema_change` ne gère pas, ou pour réparer des données. Certaines tables sont protégées par `full_refresh: false` car les reconstruire coûte trop cher.

#### Quels sont les risques des modèles incrémentaux ?

Des doublons si `unique_key` manque ou est fausse, des lignes manquées si le filtre oublie les données tardives, un écart avec une reconstruction complète si la logique change, et des tests plus complexes. Un full refresh périodique dans un environnement inférieur aide à détecter les écarts.

#### Quelle est la différence entre `merge` et `delete+insert` ?

`merge` met à jour les lignes correspondantes et insère les nouvelles en une seule requête. `delete+insert` supprime les lignes existantes ayant les mêmes clés, puis insère le nouveau lot. Utile là où merge est lent ou non pris en charge.

#### Qu'est-ce qu'`insert_overwrite`, et quand est-ce efficace ?

Il remplace des partitions entières (par exemple les jours présents dans le nouveau lot) au lieu de fusionner ligne par ligne. Efficace sur les tables partitionnées de BigQuery, Spark et Databricks quand les données arrivent par partition.

#### Que fait `incremental_predicates` ?

Il ajoute des conditions au merge, par exemple limiter la lecture de la table cible aux partitions récentes, ce qui réduit le coût sur les grosses tables.

#### Un modèle incrémental peut-il se référencer lui-même ?

Oui, via `{{ this }}` dans le bloc `is_incremental()`, en général pour lire l'horodatage maximal actuel.

#### Comment bien tester un modèle incrémental ?

Tester l'unicité de la clé primaire (les doublons sont le bug classique), comparer avec un full refresh dans un environnement inférieur, et écrire des tests unitaires qui forcent `is_incremental` à true et à false.

#### Qu'est-ce qu'un modèle incrémental « append-only » ?

Un modèle avec la stratégie `append` et sans `unique_key` : les lignes sont seulement insérées. Il convient aux journaux d'événements immuables.

#### Comment le partitionnement ou le clustering interagissent-ils avec les modèles incrémentaux ?

Partitionner ou regrouper la table cible sur la colonne du filtre (en général une date) fait lire moins de données au filtre incrémental comme au merge : c'est de là que vient l'essentiel du gain.

#### Pourquoi un modèle incrémental peut-il ralentir avec le temps ?

Le merge doit parcourir une table cible toujours plus grande. Les incremental predicates, l'élagage des partitions, le clustering, ou les stratégies `insert_overwrite` et `microbatch` gardent chaque exécution bornée.

#### Comment recalculer l'historique (backfill) d'un modèle incrémental ?

Avec `--full-refresh`, ou pour les modèles microbatch avec `--event-time-start` et `--event-time-end` pour retraiter une période, ou en l'exécutant avec une variable qui change la fenêtre du filtre.

#### Quelle est la différence entre un modèle incrémental et un snapshot ?

Un modèle incrémental garde le dernier état (ou ajoute des événements), et sa logique est la vôtre. Un snapshot garde l'historique complet des changements d'enregistrements modifiables, sous forme de lignes SCD de type 2 avec des dates de validité.

### Snapshots

#### Qu'est-ce qu'un snapshot ?

Une ressource dbt qui enregistre les changements d'une table modifiable au fil du temps (Slowly Changing Dimension de type 2). À chaque exécution, il compare les lignes actuelles de la source à la table du snapshot, ferme les lignes modifiées en fixant `dbt_valid_to` et insère leur nouvelle version avec `dbt_valid_from`.

#### Comment définit-on un snapshot ?

Dans les versions récentes de dbt, en YAML (les anciens projets utilisent un bloc `{% snapshot %}` dans `snapshots/`) :

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

`timestamp` : une ligne a changé si sa colonne `updated_at` est plus récente. Fiable et efficace quand la source maintient cette colonne. `check` : une ligne a changé si l'une des `check_cols` listées (ou toutes les colonnes) diffère. Utilisée quand il n'y a pas d'horodatage fiable.

#### Quelles colonnes dbt ajoute-t-il à un snapshot ?

`dbt_scd_id`, `dbt_updated_at`, `dbt_valid_from` et `dbt_valid_to` (NULL pour la version courante, sauf si `dbt_valid_to_current` est configuré).

#### Comment les snapshots gèrent-ils les lignes supprimées de la source ?

Par défaut, ils ne les gèrent pas. Avec `hard_deletes: invalidate` (anciennement `invalidate_hard_deletes`), les lignes supprimées reçoivent leur `dbt_valid_to`. Avec `hard_deletes: new_record`, une nouvelle ligne marque explicitement la suppression.

#### Pourquoi les snapshots doivent-ils lire des sources plutôt que des modèles transformés ?

Les snapshots capturent un historique qu'on ne peut pas recréer après coup. Photographier les données brutes avec un minimum de logique garantit qu'un bug dans le code de transformation ne corrompt pas l'historique, et qu'on peut relancer les transformations par-dessus.

#### À quelle fréquence exécuter les snapshots ?

Aussi souvent que nécessaire pour capturer les changements : les changements qui surviennent puis s'annulent entre deux exécutions sont perdus. Beaucoup d'équipes les exécutent toutes les heures ou tous les jours, avant les modèles qui les utilisent.

#### Comment interroger la version courante de chaque enregistrement d'un snapshot ?

`where dbt_valid_to is null` (ou la valeur courante configurée).

#### Comment obtenir l'état d'un enregistrement à une date donnée ?

```sql
select * from {{ ref('customers_snapshot') }}
where '2026-06-30' >= dbt_valid_from
  and ('2026-06-30' < dbt_valid_to or dbt_valid_to is null)
```

#### Peut-on faire un full refresh d'un snapshot ?

Non. dbt ne reconstruit jamais les snapshots, car l'historique serait perdu. Pour en modifier un, on migre la table à la main ou on démarre un nouveau snapshot.

#### Que se passe-t-il si la `unique_key` n'est pas unique dans la source ?

Le snapshot produit des versions dupliquées ou incohérentes. Testez l'unicité sur la source et dédoublonnez en amont si besoin.

#### Quand utiliser la stratégie `check` avec `check_cols: all` ?

Quand la source n'a pas d'`updated_at` fiable et que tout changement de colonne compte. Elle est plus coûteuse, car toutes les colonnes sont comparées.

#### En quoi les snapshots diffèrent-ils du time travel de Delta Lake ou de l'entrepôt ?

Le time travel de l'entrepôt conserve les versions passées d'une table pendant une durée de rétention limitée, pour la récupération. Les snapshots construisent une table d'historique permanente et interrogeable au niveau de la ligne, conçue pour l'analyse.

#### Qu'est-ce qu'une SCD de type 2, et comment les snapshots dbt l'implémentent-ils ?

Une dimension à évolution lente qui conserve une nouvelle ligne pour chaque version d'un enregistrement, avec des dates de validité. Les snapshots dbt sont exactement cela : une ligne par version, `dbt_valid_from` et `dbt_valid_to` bornant sa validité.

#### Comment construire une dimension historisée à partir d'un snapshot ?

Sélectionner depuis le snapshot dans un modèle, renommer `dbt_valid_from` et `dbt_valid_to` en noms plus parlants, ajouter une clé de substitution par version et un indicateur `is_current`, puis joindre les faits sur la clé naturelle et la date du fait comprise dans la période de validité.

### Documentation, lignage et couche sémantique

#### Comment dbt génère-t-il la documentation ?

`dbt docs generate` construit un site statique à partir du projet (descriptions, colonnes, tests, SQL) et des métadonnées de l'entrepôt (types de colonnes, nombre de lignes). `dbt docs serve` le sert en local. Il inclut un graphe de lignage interactif.

#### Où écrit-on les descriptions ?

Dans des fichiers de propriétés YAML à côté des modèles (`description:` sur les modèles et les colonnes), ou dans des blocs `{% docs %}` de fichiers `.md` référencés avec `{{ doc('name') }}` pour les textes longs.

#### Qu'est-ce que `persist_docs` ?

Une configuration qui écrit les descriptions des modèles et des colonnes dans l'entrepôt sous forme de commentaires de tables et de colonnes, pour qu'elles soient visibles dans d'autres outils.

#### Que sont les exposures ?

Des déclarations YAML des usages en aval des modèles dbt (tableaux de bord, modèles de ML, applications) avec leurs responsables, pour que le lignage montre ce qui dépend de chaque modèle.

#### Que fait `dbt ls` ?

Il liste les nœuds correspondant à une sélection sans les exécuter, ce qui est utile pour vérifier les sélecteurs.

#### Qu'est-ce que l'artefact `manifest.json` ?

Un fichier JSON du dossier `target/` qui décrit tout le projet (nœuds, configurations, dépendances). Il sert à la comparaison d'états (`state:modified`), à la documentation et aux outils externes.

#### Qu'est-ce que `run_results.json` ?

Un artefact qui contient le résultat, la durée et le statut de chaque nœud de la dernière invocation, utilisé pour la supervision et par `dbt retry`.

#### Quelle est l'architecture de la couche sémantique de dbt ?

Des modèles sémantiques sont définis en YAML au-dessus des modèles dbt, en déclarant des entités (clés de jointure), des dimensions et des mesures. Les indicateurs sont définis à partir de ces mesures. MetricFlow transforme une demande d'indicateur (indicateur, dimensions, filtres, granularité) en SQL optimisé pour l'entrepôt, et la dbt platform l'expose via des API et des intégrations avec les outils de BI.

#### Qu'est-ce qu'un modèle sémantique ?

Une définition YAML liée à un modèle dbt qui décrit ses entités, dimensions et mesures, pour que MetricFlow sache comment l'agréger et le joindre.

#### Quels types d'indicateurs existent dans la couche sémantique ?

Simples (une mesure), ratios, cumulatifs (totaux cumulés ou fenêtres), dérivés (expressions sur d'autres indicateurs) et de conversion.

#### Pourquoi définir les indicateurs dans dbt plutôt que dans l'outil de BI ?

Pour que la définition existe une seule fois, dans la gestion de versions, avec des tests et une revue, et que chaque outil donne le même chiffre pour « chiffre d'affaires » ou « utilisateurs actifs ».

#### Qu'est-ce que le lignage au niveau des colonnes ?

Un lignage qui montre quelles colonnes amont alimentent chaque colonne, et pas seulement quels modèles dépendent de quels autres. La dbt platform et dbt Fusion le fournissent.

#### À quoi servent les artefacts dbt pour l'observabilité ?

Des outils analysent `manifest.json` et `run_results.json` pour suivre la durée des exécutions, les échecs de tests et la fraîcheur dans le temps, et le package `dbt_artifacts` les charge dans l'entrepôt pour les analyser.

#### Que sont les champs meta ?

Un dictionnaire libre `meta:` sur les nœuds et les colonnes, par exemple pour noter les responsables, les indicateurs de données personnelles ou les engagements de service, que les outils et les macros peuvent lire.

#### Comment documenter un test ou une macro ?

Les tests et les macros peuvent avoir des propriétés `description` en YAML, qui apparaissent dans la documentation générée.

### Déploiement, environnements, CI/CD et orchestration

#### Comment gérer les déploiements de dbt sur plusieurs environnements (dev, staging, production) ?

Avec une seule base de code et plusieurs targets (ou environnements de la dbt platform) pointant vers des schémas ou des bases séparés : chaque développeur construit dans un schéma dev personnel, la CI dans un schéma temporaire, et des jobs planifiés construisent la production. Les différences entre environnements viennent de `profiles.yml`, des variables d'environnement et de `target.name`, jamais de modifications du code. Les changements n'arrivent en production que par pull request et CI.

#### Comment gérer la gestion de versions de dbt quand plusieurs personnes travaillent ensemble ?

Git avec des branches de fonctionnalité et des pull requests, la revue de code, une CI qui construit et teste les modèles modifiés à chaque pull request, un guide de style et un linter (SQLFluff), des responsables clairs pour chaque modèle, des changements petits et ciblés, et un schéma dev personnel par développeur pour que personne n'écrase les tables d'un autre.

#### Qu'est-ce que Slim CI ?

N'exécuter en CI que les modèles modifiés et leurs dépendants, par comparaison avec les artefacts de production : `dbt build --select state:modified+ --defer --state prod-artifacts/`. Les parents inchangés sont lus en production au lieu d'être reconstruits.

#### Que sélectionne `state:modified` ?

Les nœuds dont le SQL, la configuration ou les propriétés diffèrent du manifest fourni avec `--state`. Combiné avec `+`, il inclut leurs enfants.

#### Citez trois avantages de l'intégration de dbt avec Airflow.

1. Les exécutions dbt sont orchestrées avec le reste du pipeline (attendre l'ingestion, transformer, puis rafraîchir les tableaux de bord ou entraîner des modèles).
2. Les relances, les alertes, les SLA, les recalculs d'historique et la planification viennent d'Airflow.
3. Avec des outils comme Astronomer Cosmos, chaque modèle dbt devient une tâche Airflow, ce qui donne une visibilité fine et permet de ne relancer que les modèles en échec.

#### Comment intégrer dbt dans un pipeline de données existant ?

Commencer par déclarer les tables brutes existantes comme sources, puis reproduire les transformations actuelles en modèles de staging et de marts, un domaine à la fois, en comparant les résultats avec les tables historiques (par exemple avec `audit_helper`). Ajouter tests et documentation, lancer dbt depuis l'orchestrateur existant après l'ingestion, basculer les consommateurs vers les nouvelles tables et retirer progressivement les anciens scripts.

#### Comment planifier dbt en production avec dbt Core ?

Avec un orchestrateur (Airflow, Dagster, Prefect, cron, GitHub Actions, Databricks Workflows) qui lance `dbt build` (ou les commandes choisies) dans un conteneur ou un environnement virtuel avec les identifiants de production.

#### À quoi ressemble un job de production typique ?

`dbt deps`, `dbt source freshness`, `dbt build` (seeds, snapshots, modèles et tests dans l'ordre), puis `dbt docs generate`, avec des alertes en cas d'échec et les artefacts conservés pour la comparaison suivante en CI.

#### Comment déployer dbt sur la dbt platform (dbt Cloud) ?

Créer des environnements de déploiement avec leurs identifiants, définir des jobs (commandes, planification ou déclencheurs, modèles sélectionnés), activer des jobs de CI sur les pull requests, et utiliser l'enchaînement de jobs ou des déclenchements par API pour lancer dbt après l'ingestion.

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

#### Comment superviser et diagnostiquer les problèmes dans dbt ?

Lire la sortie de la console et `logs/dbt.log`, lire le SQL compilé dans `target/compiled` et `target/run`, examiner `run_results.json` pour les échecs et les durées, conserver les échecs de tests, utiliser `dbt retry` après correction, et suivre l'historique et la durée des exécutions dans l'orchestrateur ou la dbt platform. Des alertes sur les échecs de jobs et la fraîcheur des sources détectent les problèmes tôt.

#### Comment déboguer ses modèles dbt ?

Lancer `dbt compile` et exécuter le SQL compilé directement dans l'entrepôt, prévisualiser avec `dbt show`, isoler les CTE pas à pas, utiliser `{{ log() }}` dans Jinja, exécuter avec `--debug` pour des journaux complets, et vérifier les données amont avec des tests.

#### Comment dbt compile-t-il les requêtes ?

dbt analyse le projet et construit le DAG, puis pour chaque nœud il rend le Jinja : il résout `ref`, `source`, `var`, `config` et les appels de macros en SQL simple pour le target courant. Le `SELECT` compilé est écrit dans `target/compiled/`. À l'exécution, la matérialisation l'enveloppe dans du DDL/DML (`create table as`, `merge`) et l'envoie à l'entrepôt via l'adaptateur.

#### Qu'est-ce que SQLFluff ?

Un linter et formateur SQL avec un mode de templating dbt, utilisé en CI et dans des hooks pre-commit pour imposer un style SQL homogène.

#### Comment exécuter dbt dans un conteneur Docker ?

Utiliser une image avec dbt Core et l'adaptateur installés, monter ou copier le projet, passer les identifiants par variables d'environnement et lancer des commandes comme `dbt build --target prod`.

#### Qu'est-ce que dbt Mesh ?

Un modèle d'organisation pour les grandes structures où plusieurs projets dbt référencent les modèles publics les uns des autres (`ref` entre projets), avec des contrats, des versions et des contrôles d'accès, pour que chaque domaine gère son projet de façon indépendante.

#### Comment lancer dbt à la fin de l'ingestion ?

Via l'orchestrateur (une dépendance entre tâches ou un capteur), les déclenchements par API ou l'enchaînement de jobs de la dbt platform, ou l'intégration de l'outil d'ingestion (par exemple Fivetran qui déclenche un job dbt).

#### Qu'est-ce qu'un déploiement bleu-vert avec dbt ?

Construire la production dans un nouveau schéma ou une nouvelle base, la tester, puis la basculer de façon atomique (renommage de schémas ou permutation de vues), pour que les consommateurs ne voient jamais de données à moitié construites.

### Performances, entrepôts et dépannage

#### Comment optimiser les performances des transformations dbt sur de gros volumes ?

Matérialiser en tables les modèles coûteux et utiliser des modèles incrémentaux pour les grosses tables de faits, filtrer et agréger tôt, éviter `select *` et les jointures inutiles, partitionner et regrouper les grosses tables sur les colonnes de filtre, utiliser les fonctions natives de l'entrepôt (clés de clustering, clés de tri), limiter les données en développement, et étudier les profils de requêtes et les durées de `run_results.json` pour trouver les modèles les plus lents.

#### Citez des techniques d'optimisation de dbt sur Snowflake.

Utiliser des tables transitoires pour les modèles intermédiaires (pas de coût de stockage Fail-safe), appliquer du clustering aux très grosses tables sur les colonnes de filtre courantes, dimensionner les warehouses par job (et séparer ceux de dbt et de la BI), utiliser `merge` ou `delete+insert` avec des incremental predicates, s'appuyer sur le clonage sans copie pour la dev et la CI (`dbt clone`), définir un `query_tag` pour attribuer les coûts, et activer la suspension automatique des warehouses.

#### Comment comparer dbt et BigQuery ?

Ce ne sont pas des alternatives : BigQuery est un entrepôt de données serverless qui stocke et traite les données, tandis que dbt est un framework de transformation qui génère du SQL et l'exécute dans BigQuery (via dbt-bigquery). Les requêtes planifiées de BigQuery ou Dataform couvrent un terrain proche de dbt, mais dbt apporte la portabilité entre plateformes, un large écosystème de packages et une grande communauté. Sur BigQuery, dbt prend en charge le partitionnement, le clustering et `insert_overwrite`.

#### Comment accélérer globalement les exécutions dbt ?

Augmenter les `threads` dans les limites de l'entrepôt, supprimer les modèles inutiles, transformer en vues les tables peu interrogées (ou l'inverse pour les vues lourdes), utiliser des modèles incrémentaux, n'exécuter que ce qui a changé (`state:modified+`) en CI, et séparer les jobs selon leurs besoins de fraîcheur.

#### Pourquoi une longue chaîne de vues peut-elle être lente ?

Chaque requête sur la vue finale exécute toute la chaîne de SQL sous-jacente. Matérialiser en tables les modèles intermédiaires clés évite de répéter les calculs.

#### Comment trouver les modèles les plus lents ?

Via les durées de `run_results.json`, la vue des durées de modèles de la dbt platform, ou l'historique des requêtes de l'entrepôt filtré par le `query_tag` de dbt.

#### Quel est l'impact sur les coûts des vues, des tables et des modèles incrémentaux ?

Les vues coûtent du calcul à chaque interrogation. Les tables coûtent du calcul à chaque construction, plus le stockage. Les modèles incrémentaux coûtent peu par exécution mais demandent du soin pour rester justes.

#### Qu'est-ce qui provoque un « fan-out » dans les modèles dbt, et comment le détecter ?

Joindre sur une clé non unique d'un côté multiplie les lignes et gonfle les sommes. Des tests d'unicité sur les clés de jointure et sur la granularité de chaque modèle le détectent.

#### Comment limiter les données en développement pour gagner du temps et de l'argent ?

Filtrer par date ou échantillonner quand `target.name == 'dev'`, utiliser `--defer` pour réutiliser les parents de production, ou utiliser des clones sans copie.

#### Que faire de dépendances entre modèles qui forment un cycle ?

dbt refuse les cycles. Restructurer la logique, en général en extrayant la partie commune dans un modèle amont référencé par les deux modèles.

#### Que se passe-t-il quand un modèle échoue au milieu d'une exécution ?

Ses modèles en aval sont ignorés, les branches indépendantes continuent, et l'exécution signale l'échec. Corriger puis lancer `dbt retry`, ou relancer le modèle en échec et ses enfants avec `model+`.

#### Comment gérer les changements de schéma des sources ?

Les détecter avec des tests et des contrats, utiliser des listes de colonnes explicites en staging plutôt que `select *`, configurer `on_schema_change` pour les modèles incrémentaux, et adapter les modèles de staging à un seul endroit.

#### Comment traiter des lignes en double venant d'une source ?

Les dédoublonner dans le modèle de staging, en général avec une fonction de fenêtrage qui garde la ligne la plus récente par clé, puis tester l'unicité :

```sql
select *
from {{ source('crm', 'customers') }}
qualify row_number() over (partition by customer_id order by updated_at desc) = 1
```

#### Comment superviser et diagnostiquer les problèmes de dbt en production ?

Des alertes sur les échecs de jobs et les erreurs de tests, le suivi de l'évolution des échecs de tests et des durées d'exécution, le contrôle de la fraîcheur des sources avant l'exécution, la conservation des artefacts pour comparaison, et une procédure d'astreinte documentée (examiner les journaux et le SQL compilé, relancer avec `dbt retry`, informer les consommateurs des incidents de données).

#### Que vérifier quand un job dbt prend soudain deux fois plus de temps ?

La croissance des volumes dans les sources, un modèle qui a changé de matérialisation ou perdu son filtre incrémental, un full refresh lancé par erreur, la taille du warehouse ou la file d'attente, une nouvelle jointure qui multiplie les lignes, et l'absence d'élagage des partitions.
