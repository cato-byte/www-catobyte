## Fiche d'étude CI/CD pour les données

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude CI/CD pour les données : environ 200 questions](../../images/cicd_data_study_guide_title_img.png)

Environ 200 questions d'entretien sur la CI/CD et l'automatisation des plateformes de données : workflows Git, stratégies de test des pipelines et des données, qualité du code, environnements, infrastructure as code, stratégies de déploiement, GitHub Actions en profondeur, CI/CD pour dbt, Databricks, Airflow et les entrepôts, sécurité de la chaîne de livraison et exploitation. Les exemples utilisent GitHub Actions, avec des remarques sur GitLab CI et Azure DevOps. Ouvrez une question pour voir sa réponse, ou utilisez le filtre pour chercher dans toute la fiche.

<!-- QA -->

### Fondamentaux

#### Qu'est-ce que la CI/CD ?

L'intégration continue (CI) consiste à fusionner fréquemment les modifications de code dans une branche partagée, avec compilation et tests automatiques à chaque changement. La livraison continue (CD) garde le code toujours déployable et automatise les mises en production dans les environnements ; le déploiement continu va plus loin et déploie automatiquement en production chaque changement qui passe les tests.

#### Pourquoi la CI/CD compte-t-elle pour les équipes data ?

Les pipelines de données sont du logiciel : sans automatisation, les changements sont déployés à la main, cassent des tables de production et sont difficiles à annuler. La CI/CD détecte les erreurs avant qu'elles n'atteignent les consommateurs, rend les déploiements reproductibles et auditables, et permet de faire évoluer les pipelines vite et en sécurité.

#### Qu'est-ce que le DataOps ?

L'application des pratiques DevOps et agiles aux données : gestion de versions, tests automatisés (du code et des données), CI/CD, gestion des environnements, supervision et observabilité, et collaboration entre data engineers, analystes et exploitation, avec pour objectif des données fiables livrées rapidement.

#### En quoi la CI/CD des données diffère-t-elle de celle des applications ?

Les pipelines de données ont un état (tables, historique, schémas) qu'il faut migrer et pas seulement remplacer ; les tests exigent des données représentatives ; la justesse dépend autant des données que du code ; les déploiements peuvent déclencher des recalculs coûteux ; et annuler des données est plus difficile qu'annuler du code.

#### Que faut-il automatiser dans un pipeline de CI/CD data ?

Le linting et le formatage, les tests unitaires, la construction des artefacts (wheels, images, manifestes dbt), la validation statique (compilation SQL, validation des bundles ou DAG), les tests d'intégration et de données sur des données de test, les analyses de sécurité, les changements d'infrastructure, les déploiements dans chaque environnement, les tests de fumée après déploiement et les notifications.

#### Quelle différence entre livraison continue et déploiement continu ?

Avec la livraison continue, chaque changement est déployable et la mise en production est à un clic ou une approbation près. Avec le déploiement continu, chaque changement qui passe le pipeline arrive en production automatiquement, sans étape manuelle.

#### Qu'est-ce que « tout sous forme de code » ?

Définir pipelines, transformations, infrastructure, droits, planifications, règles de qualité et même documentation dans des fichiers versionnés, pour que chaque changement soit relu, testé, reproductible et traçable.

#### Quels sont les avantages des déploiements petits et fréquents ?

Chaque changement est plus facile à relire, tester et comprendre, les échecs sont plus faciles à diagnostiquer et à annuler, et les retours de la production arrivent plus tôt. Les grosses livraisons espacées regroupent de nombreux risques.

#### Qu'est-ce qu'un pipeline de déploiement ?

La séquence automatisée qui mène un commit jusqu'en production : compiler, tester, empaqueter, déployer dans les environnements inférieurs, contrôler, approuver, déployer en production, vérifier. C'est le chemin suivi par chaque changement.

#### Que sont les métriques DORA ?

Quatre mesures de la performance de livraison : fréquence de déploiement, délai de mise en production des changements, taux d'échec des changements et délai de rétablissement du service. Elles s'appliquent aussi aux équipes data et aident à mesurer si la CI/CD améliore la livraison.

#### Quelle différence entre les étapes de compilation, de test et de déploiement ?

La compilation produit des artefacts (paquets, images, modèles compilés) ; le test les vérifie (unitaires, intégration, données) ; le déploiement les installe dans un environnement et exécute les contrôles post-déploiement. Les séparer facilite la localisation des échecs.

#### Qu'est-ce que le « shift left » appliqué à la qualité des données ?

Détecter les problèmes le plus tôt possible : dans l'IDE (linters), au commit (hooks pre-commit), dans les pull requests (tests de CI, contrôles de contrat), plutôt que dans les tableaux de bord de production, où ils coûtent cher et se voient.

#### Quelle différence entre une « livraison » (release) et un « déploiement » ?

Un déploiement installe une version dans un environnement ; une livraison met une nouvelle fonctionnalité à disposition des utilisateurs. Avec des feature flags ou des bascules blue-green, on peut déployer sans livrer et livrer sans redéployer.

#### Pourquoi les pipelines doivent-ils être déterministes ?

Avec le même code, la même configuration et les mêmes entrées, un pipeline déterministe produit les mêmes sorties, ce qui rend possibles les tests, le débogage, les backfills et les audits. Évitez les dépendances cachées à l'heure courante, aux graines aléatoires ou aux versions non figées.

#### Que signifie « you build it, you run it » pour les équipes data ?

L'équipe qui construit un pipeline l'exploite aussi : elle reçoit ses alertes, résout ses incidents et améliore sa fiabilité, ce qui incite fortement à de bons tests, une bonne supervision et l'automatisation.

### Gestion de versions et workflows Git

#### Pourquoi le code data doit-il être dans Git ?

La gestion de versions apporte l'historique (qui a changé quoi et pourquoi), la collaboration par branches et pull requests, la possibilité d'annuler, une source de vérité unique pour les déploiements et le déclencheur de la CI/CD.

#### Que contient un dépôt data ?

Le code des pipelines et des transformations (Python, SQL, modèles dbt), les tests et leurs jeux de données, la configuration par environnement (sans secrets), l'infrastructure as code, les définitions d'orchestration (DAG, bundles, spécifications de jobs), les workflows de CI/CD, la documentation et les contrats de données.

#### Que ne faut-il jamais committer ?

Des secrets (mots de passe, clés, jetons), de vraies données personnelles ou sensibles, de gros fichiers de données, des fichiers d'environnement local et des sorties de compilation. Utilisez `.gitignore`, l'analyse de secrets et des hooks pre-commit pour éviter les accidents.

#### Qu'est-ce que le trunk-based development ?

Un workflow où les développeurs intègrent de petits changements dans la branche principale fréquemment (au moins quotidiennement), avec des branches de fonctionnalité de courte durée et des feature flags, la branche principale restant toujours livrable. Il convient bien à la CI/CD.

#### Qu'est-ce que GitFlow, et pourquoi est-il moins populaire aujourd'hui ?

Un modèle de branches avec des branches `develop` et `main` de longue durée plus des branches de fonctionnalité, de release et de hotfix. Il ajoute de la lourdeur et des conflits de fusion ; la plupart des équipes pratiquant la CI/CD préfèrent le trunk-based development ou un simple flux de branches de fonctionnalité.

#### Qu'est-ce qu'une pull request (merge request), et que doit contenir une bonne PR ?

Une demande de fusion d'une branche, avec une description du quoi et du pourquoi, le ticket lié, les tests effectués, l'impact sur les données (schémas, backfills, consommateurs), des captures ou résultats de requêtes si utile, et des contrôles au vert. C'est le lieu de la revue et de la validation automatique.

#### Que doivent chercher les relecteurs dans du code data ?

La justesse de la logique et des jointures (grain, fan-out), la gestion des nulls et des doublons, l'idempotence, les performances (filtres de partition, lectures complètes), des tests couvrant le changement, les changements de schéma et de contrat, les besoins de backfill, la sécurité (pas de secrets, droits adaptés) et la lisibilité.

#### Que sont les règles de protection de branche ?

Des réglages du dépôt qui empêchent les push directs sur les branches importantes et exigent pull requests, contrôles au vert, un nombre d'approbations, des revues des code owners, des branches à jour ou des commits signés avant la fusion.

#### Qu'est-ce qu'un fichier CODEOWNERS ?

Un fichier qui associe des chemins à des équipes ou personnes responsables, automatiquement sollicitées en revue et dont l'approbation peut être exigée pour les changements de leur périmètre, par exemple `/models/finance/ @org/finance-data`.

#### Qu'est-ce que le versionnage sémantique, et s'applique-t-il aux données ?

Versionner en MAJEURE.MINEURE.CORRECTIF, les versions majeures signalant des changements cassants. Il s'applique aux bibliothèques et aussi aux produits et contrats de données : une colonne supprimée ou un sens modifié est une version majeure, une nouvelle colonne optionnelle une version mineure.

#### Que sont les conventional commits ?

Une convention de messages de commit (`feat:`, `fix:`, `chore:`, `docs:`, `feat!:` pour les changements cassants) qui rend l'historique lisible et permet aux outils de générer automatiquement changelogs et numéros de version.

#### Comment gérer les hotfixes en trunk-based development ?

Corriger sur une branche courte issue de main, fusionner par le pipeline normal (éventuellement accéléré) et déployer ; si une branche de release est en production, y faire aussi un cherry-pick de la correction. Évitez de corriger la production à la main.

#### Monorepo ou polyrepo pour les données ?

Un monorepo regroupe pipelines, modèles et infrastructure dans un seul dépôt (changements transverses faciles, outillage partagé, CI par chemins nécessaire) ; un polyrepo les sépare par domaine ou composant (responsabilités et accès clairs, coordination plus difficile). Les deux fonctionnent avec une bonne CI.

#### Comment garder des branches de fonctionnalité courtes ?

Découper le travail en petits changements fusionnables indépendamment, fusionner derrière des feature flags ou des planifications désactivées, rebaser souvent sur main et viser une fusion en un ou deux jours.

#### À quoi servent les tags Git dans les déploiements ?

À marquer les points de livraison (`v1.4.0`) qui déclenchent les workflows de release, à identifier exactement ce qui a été déployé et à permettre un retour arrière en redéployant un tag précédent.

#### Comment gérer les notebooks dans Git ?

Les stocker comme fichiers source (format `.py` de Databricks, Jupytext) plutôt qu'en JSON avec leurs sorties, supprimer les sorties avant le commit, et garder la logique dans des modules importables avec des notebooks minces, pour des diffs relisibles.

#### À quoi sert Git LFS dans les dépôts data ?

Git LFS stocke les gros fichiers binaires (petits jeux de référence, données de test, images) hors de l'historique Git normal ; les gros volumes de production ne doivent pas du tout être dans Git.

### Stratégie de test pour les données

#### À quoi ressemble la pyramide des tests pour les pipelines de données ?

De nombreux tests unitaires rapides de la logique de transformation, moins de tests d'intégration de composants avec de vrais moteurs (Spark, une base de test, dbt sur un schéma de test), quelques tests de bout en bout exécutant tout le pipeline sur des données d'exemple, plus des tests de qualité des données qui tournent en production sur les données réelles.

#### Qu'est-ce qu'un test unitaire dans un pipeline de données ?

Un test rapide d'un petit morceau de logique avec des entrées maîtrisées et des sorties attendues, comme une fonction PySpark sur un minuscule DataFrame, une fonction d'analyse, ou une macro ou un modèle dbt avec des entrées simulées.

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

#### Comment structurer le code pour qu'il soit testable unitairement ?

Séparer les fonctions de transformation pures (DataFrame en entrée, DataFrame en sortie ; lignes en entrée, lignes en sortie) des entrées-sorties (lecture des sources, écriture des tables) et de la configuration ; injecter les dépendances comme les chemins et les dates ; garder les notebooks ou scripts d'entrée minces.

#### Qu'est-ce qu'un test d'intégration pour les données ?

Un test qui exécute des composants ensemble avec des dépendances réelles (ou réalistes) : lire et écrire de vraies tables dans un schéma de test, exécuter du SQL dans un bac à sable de l'entrepôt, ou appeler une API simulée, pour vérifier que les pièces s'emboîtent.

#### Qu'est-ce qu'un test de bout en bout d'un pipeline ?

L'exécution de tout le pipeline (de l'ingestion aux tables finales) sur un petit jeu de données synthétique représentatif dans un environnement isolé, avec des assertions sur les sorties (nombres de lignes, valeurs clés, invariants). Il détecte des erreurs de câblage que les tests unitaires ne voient pas.

#### Que sont les tests de données, et en quoi diffèrent-ils des tests de code ?

Les tests de code vérifient que la logique se comporte comme prévu sur des entrées maîtrisées ; les tests de données vérifient que les données réelles respectent les attentes (unicité, non-nullité, valeurs acceptées, intégrité référentielle, fraîcheur, volume). Les deux sont nécessaires : un code correct peut produire des données fausses à partir d'entrées fausses.

#### Qu'est-ce que la gestion des données de test ?

La création et la maintenance de jeux de données pour les tests : petits jeux synthétiques pour les tests unitaires, échantillons anonymisés ou synthétiques pour les tests d'intégration, et données proches de la production (masquées) pour les tests de performance, versionnés avec le code quand c'est possible.

#### Pourquoi privilégier des données synthétiques en CI ?

Elles sont sûres (pas de données personnelles), petites (tests rapides), déterministes, et peuvent inclure délibérément des cas limites (nulls, doublons, enregistrements tardifs, unicode, valeurs extrêmes) rares dans de vrais échantillons.

#### Qu'est-ce qu'un test de contrat de données ?

Un test qui vérifie que la sortie d'un producteur respecte le schéma et la sémantique convenus dans un contrat de données (colonnes, types, nullabilité, valeurs autorisées), exécuté dans la CI du producteur pour que les changements cassants échouent avant la livraison.

#### Qu'est-ce que le test de non-régression des pipelines de données ?

Comparer les sorties de la nouvelle version à celles de la précédente sur la même entrée (nombres de lignes, agrégats, différences ligne à ligne), pour détecter les changements involontaires ; les outils incluent `datacompy`, dbt audit helper et les approches de data-diff.

#### Qu'est-ce qu'un test de fumée après déploiement ?

Une vérification rapide, juste après le déploiement, que le système fonctionne : les jobs sont enregistrés, une petite exécution réussit, les tables clés sont lisibles, les tableaux de bord se chargent. Il détecte tôt les erreurs de configuration et de droits.

#### Comment tester les transformations SQL ?

Compiler et analyser le SQL en CI, exécuter les modèles sur de petites entrées amorcées dans un schéma de test et comparer aux sorties attendues (tests unitaires dbt), appliquer des tests de données sur les résultats, et linter le SQL pour le style et les anti-modèles.

#### Comment tester des DAG Airflow ?

Charger tous les DAG avec `DagBag` et échouer en cas d'erreur d'import, vérifier les conventions (owners, relances, tags, absence de cycle), tester unitairement la logique Python utilisée par les tâches, et lancer des tests d'intégration dans un Airflow de staging.

#### Qu'est-ce que le test par propriétés, et est-il utile pour les données ?

Générer de nombreuses entrées aléatoires respectant des contraintes et vérifier des propriétés toujours vraies (par exemple, la sortie d'une déduplication a des clés uniques et est un sous-ensemble de l'entrée). Des outils comme Hypothesis trouvent des cas limites que les tests écrits à la main ratent.

#### Qu'est-ce que le test par mutation ?

Introduire de petites modifications dans le code (mutants) et vérifier si les tests échouent ; les mutants survivants révèlent des tests faibles. Peu utilisé dans les équipes data, il est utile pour les bibliothèques critiques.

#### Comment garder des suites de tests rapides ?

Utiliser de petits jeux de données, partager une SparkSession par session de tests, marquer les tests lents et les lancer séparément ou seulement sur main, paralléliser avec `pytest-xdist`, mettre en cache les dépendances en CI et éviter d'appeler de vrais services cloud dans les tests unitaires.

#### Que sont les fixtures pytest, et en quoi aident-elles pour les tests de données ?

Des fonctions de préparation réutilisables (une SparkSession, une base temporaire, des DataFrames d'exemple) injectées dans les tests par leur nom, avec des portées (fonction, module, session) pour que les ressources coûteuses comme Spark ne soient créées qu'une fois.

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

#### Comment comparer des DataFrames dans les tests ?

Avec `pyspark.testing.assertDataFrameEqual` (Spark 3.5+) ou `chispa` pour PySpark, `pandas.testing.assert_frame_equal` pour pandas, avec des options pour ignorer l'ordre des lignes et tolérer les flottants approchés.

#### Quels cas limites les tests d'un pipeline de données doivent-ils couvrir ?

Entrées vides, nulls dans les clés et les valeurs, doublons, enregistrements tardifs et désordonnés, changements de schéma (colonnes en plus ou en moins), formats invalides, fuseaux horaires et changements d'heure, valeurs très grandes, caractères spéciaux, et relances sur la même entrée (idempotence).

#### Comment tester l'idempotence ?

Exécuter deux fois l'étape du pipeline sur la même entrée et vérifier que la sortie est identique (même nombre de lignes, pas de doublons, mêmes agrégats).

#### Comment tester la gestion de l'évolution du schéma ?

Fournir des jeux de test avec une colonne ajoutée, une colonne supprimée et un type modifié, et vérifier que le pipeline se comporte comme prévu (accepte les changements additifs, échoue clairement ou met en quarantaine les changements incompatibles).

#### Que sont les « golden files » ou tests par snapshot ?

Des sorties attendues stockées (CSV, JSON, Parquet) auxquelles on compare les résultats des tests ; quand les sorties changent volontairement, les golden files sont mis à jour dans la même pull request, ce qui rend les changements visibles en revue.

#### Comment tester les performances en CI ?

En général pas à chaque PR, mais par des benchmarks périodiques sur des volumes représentatifs, en suivant durée, volumes de shuffle et coût, avec des alertes en cas de régression ; des règles de lint peuvent détecter à moindre coût les anti-modèles de performance connus.

### Qualité du code et contrôles statiques

#### Quels linters utilise-t-on dans les projets data ?

Ruff (linting et formatage Python), mypy ou pyright (vérification de types), SQLFluff (linting et formatage SQL pour de nombreux dialectes, compatible dbt), yamllint, shellcheck, hadolint pour les Dockerfiles et des contrôles propres aux outils (dbt project evaluator, règles `AIR` d'Airflow).

#### Qu'est-ce que pre-commit ?

Un framework qui exécute des hooks configurés (formateurs, linters, détecteurs de secrets, contrôles de gros fichiers) à chaque commit local, détectant les problèmes avant la CI ; les mêmes hooks peuvent tourner en CI par cohérence.

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

#### Pourquoi imposer le formatage automatiquement ?

Cela met fin aux débats de style en revue, rend les diffs plus petits et lisibles, et permet aux relecteurs de se concentrer sur la logique. Des formateurs comme Ruff et SQLFluff corrigent le formatage automatiquement.

#### Que sont les règles de lint personnalisées pour le code data ?

Des contrôles propres au projet contre des anti-modèles, comme `collect()` sur de gros DataFrames, des UDF Python là où des fonctions natives existent, `SELECT *` dans des modèles de production, des chemins ou identifiants codés en dur, des filtres de partition manquants ou `withColumn` dans des boucles.

#### Qu'est-ce que l'analyse statique de sécurité ?

Des outils comme Bandit (problèmes de sécurité Python), Semgrep (règles personnalisées), Checkov ou tfsec (mauvaises configurations d'infrastructure) et des analyseurs de dépendances qui trouvent vulnérabilités et motifs risqués avant le déploiement.

#### Qu'est-ce que la couverture de code, et comment l'utiliser ?

Le pourcentage de code exécuté par les tests. C'est un signal utile des zones non testées mais pas un objectif en soi ; visez des tests significatifs de la logique critique plutôt qu'un chiffre, et suivez la tendance sur les fichiers modifiés.

#### Comment vérifier les projets dbt en CI ?

Avec `dbt deps`, `dbt parse` ou `compile` pour détecter les erreurs de syntaxe et de références, le linting SQLFluff, le dbt project evaluator pour les conventions, et `dbt build` des modèles modifiés avec leurs tests dans un schéma de CI.

#### Pourquoi ajouter des annotations de type au code data ?

Elles documentent les interfaces, permettent aux vérificateurs de types de détecter des erreurs (mauvais types d'arguments, gestion de `None`) avant l'exécution et améliorent l'IDE, ce qui compte pour les bibliothèques partagées par de nombreux pipelines.

#### Qu'est-ce que le dbt project evaluator ?

Un paquet dbt qui vérifie un projet au regard des bonnes pratiques (nommage des modèles, couches, références directes aux sources depuis les marts, tests ou documentation manquants, motifs de fan-out) et peut faire échouer la CI en cas d'écart.

#### Comment vérifier les fichiers YAML et de configuration ?

Par la validation de schéma (JSON Schema pour les configurations, `databricks bundle validate`, `actionlint` pour les workflows GitHub), yamllint pour la syntaxe et le style, et des tests qui chargent tous les fichiers de configuration utilisés par le pipeline.

#### Qu'est-ce qu'actionlint ?

Un vérificateur statique des fichiers de workflow GitHub Actions qui détecte erreurs de syntaxe, expressions invalides, entrées inconnues et problèmes de scripts shell avant l'exécution des workflows.

### Environnements et configuration

#### De quels environnements une plateforme de données a-t-elle besoin ?

Au minimum du développement (bacs à sable individuels ou partagés), un environnement de staging ou de préproduction reflétant la production, et la production. Certains ajoutent des environnements de test/recette ou des environnements éphémères par pull request.

#### Pourquoi séparer les environnements par compte, workspace ou catalogue ?

L'isolement limite la portée des erreurs, permet des droits différents (les développeurs ne peuvent pas écrire en production), sépare les coûts et rend la promotion explicite.

#### Qu'est-ce que la parité des environnements ?

Garder les environnements aussi semblables que possible (même code, versions, configurations, modèles d'infrastructure) pour que les tests en staging prédisent le comportement en production ; les différences doivent se limiter à l'échelle, aux données et aux identifiants.

#### Comment gérer la configuration par environnement ?

Avec des fichiers de configuration ou des variables par environnement (chemins, catalogues, tailles de cluster, planifications) injectés au déploiement, le code restant identique ; les secrets viennent d'un gestionnaire de secrets, jamais de fichiers du dépôt.

#### Que dit le principe twelve-factor sur la configuration ?

Stocker la configuration dans l'environnement (variables), pas dans le code, pour que le même artefact de compilation tourne dans tous les environnements avec des réglages différents.

#### Que sont les environnements éphémères ?

Des environnements de courte durée créés automatiquement pour une pull request (un schéma, une branche du catalogue, un clone de tables, une copie déployée des jobs) et détruits après la fusion, qui permettent aux relecteurs de tester les changements de façon isolée.

#### Comment fournir des données de test en staging ?

Copier ou cloner les données de production en masquant ou anonymisant les données personnelles, échantillonner pour réduire le coût, utiliser des clones zero-copy (Snowflake, shallow clones Delta) quand ils existent, ou générer des données synthétiques à l'échelle de la production.

#### Qu'est-ce que le versionnage des données, et pourquoi est-il utile en CI/CD ?

Versionner les jeux de données comme le code (branches lakeFS, Project Nessie pour Iceberg, snapshots Delta et Iceberg, snapshots dbt) pour reproduire des exécutions, tester des changements sur des branches isolées des données et annuler des écritures fautives.

#### Qu'est-ce que le modèle write-audit-publish (WAP) ?

Écrire les nouvelles données dans un emplacement ou une branche de staging, les auditer avec des contrôles de qualité, puis seulement les publier (swap, merge ou fast-forward), pour que les consommateurs ne voient jamais de données fausses. Les branches Iceberg, lakeFS et les échanges de tables le mettent en œuvre.

#### Comment nommer les ressources d'un environnement à l'autre ?

Avec un schéma cohérent qui inclut l'environnement (`sales_prod`, `catalog_dev`, `dbt_ci_pr_123`), dérivé de la configuration plutôt que codé en dur, pour que le code ne pointe jamais par accident vers la production depuis le dev.

#### Comment les développeurs travaillent-ils sans toucher aux données de production ?

Avec des schémas ou catalogues personnels, des cibles de développement qui lisent la production en lecture seule (ou des clones) et n'écrivent qu'en dev, des données échantillonnées ou masquées, et des droits qui interdisent l'écriture en production aux identités des développeurs.

#### Qu'est-ce que la promotion entre environnements ?

Faire passer le même artefact du dev au staging puis à la production après la réussite des contrôles à chaque étape, au lieu de le reconstruire, avec des approbations pour la production.

#### Le staging doit-il utiliser des données de production ?

Idéalement, le staging utilise des données proches de la production (clonées, échantillonnées ou masquées) pour détecter les problèmes du monde réel, avec un contrôle strict des données personnelles ; un staging purement synthétique peut manquer des problèmes que seules les données réelles révèlent.

### Infrastructure as code

#### Qu'est-ce que l'infrastructure as code (IaC) ?

La définition des ressources cloud (stockage, calcul, réseaux, droits, catalogues, jobs) dans du code déclaratif versionné, relu et appliqué automatiquement, plutôt que leur création à la main dans les consoles.

#### Quels outils d'IaC sont courants pour les plateformes de données ?

Terraform/OpenTofu (multi-cloud), AWS CloudFormation, CDK et SAM, Azure Bicep, Pulumi, et des outils propres aux plateformes comme les Databricks Asset Bundles, le provider Terraform de Snowflake et les manifestes Kubernetes avec Helm.

#### Qu'est-ce que le workflow plan/apply de Terraform ?

`terraform plan` montre les changements qui seraient faits ; les relecteurs vérifient le plan dans la pull request ; `terraform apply` l'exécute après approbation, généralement depuis la CI avec un état distant et un verrouillage.

#### Qu'est-ce que l'état Terraform, et comment le stocker ?

Un fichier qui relie la configuration aux ressources réelles. Stockez-le à distance (S3 avec verrouillage, Terraform Cloud, Azure Storage) avec chiffrement et contrôle d'accès, jamais dans Git, et séparez l'état par environnement.

#### Qu'est-ce que la dérive de configuration ?

Des écarts entre l'infrastructure déclarée et la réalité, causés par des modifications manuelles. On la détecte avec des `terraform plan` planifiés ou des services de détection de dérive, et on la corrige en mettant à jour le code ou en annulant les modifications manuelles.

#### Qu'est-ce que l'infrastructure immuable ?

Remplacer les composants par de nouvelles versions au lieu de les modifier sur place (nouvelles images de conteneur, nouveaux clusters), ce qui rend les déploiements prévisibles et les retours arrière simples.

#### Comment structurer l'IaC pour plusieurs environnements ?

Des modules réutilisables pour les composants communs, des variables ou workspaces par environnement (dev, staging, prod), un état séparé par environnement et les mêmes modules promus d'un environnement à l'autre.

#### Comment relire en sécurité les changements d'infrastructure ?

Publier le `terraform plan` (ou le diff CDK, le change set CloudFormation) en commentaire de la pull request, exiger la revue des responsables des ressources concernées, utiliser des contrôles de politiques (Checkov, OPA/Conftest, Sentinel), et n'appliquer que depuis la CI.

#### Qu'est-ce que la politique sous forme de code (policy as code) ?

L'écriture des règles de l'organisation (chiffrement obligatoire, pas de bucket public, tags obligatoires, régions autorisées) sous forme de code évalué automatiquement en CI ou au déploiement, par exemple avec Open Policy Agent, Checkov ou les services de politiques natifs du cloud.

#### Comment gérer les droits de la plateforme de données sous forme de code ?

Définir rôles, droits et permissions du catalogue dans Terraform ou les outils des plateformes (provider Snowflake, provider Terraform de Databricks, droits Unity Catalog dans les bundles), relus en pull request, pour que les changements d'accès soient auditables et réversibles.

### Empaquetage et artefacts

#### Qu'est-ce qu'un artefact de compilation dans les projets data ?

La sortie versionnée d'une compilation qui est déployée : un wheel Python avec le code du pipeline, une image Docker, un JAR, un manifeste dbt compilé, un bundle ou un zip de scripts SQL. On compile une fois et on déploie le même artefact partout.

#### Pourquoi « compiler une fois, déployer plusieurs fois » ?

Recompiler pour chaque environnement peut produire des artefacts différents (changements de dépendances, moment de compilation), si bien que ce qui a été testé n'est pas ce qui est déployé. Compiler un artefact et le promouvoir garantit la cohérence.

#### Comment versionner les artefacts ?

Avec des versions sémantiques pour les bibliothèques, et des SHA de commit ou des numéros de build pour les applications (`0.2.145+g1a2b3c4`), apposés à la compilation pour que chaque déploiement soit traçable jusqu'à un commit.

#### Où stocker les artefacts ?

Dans des dépôts et registres d'artefacts : dépôts compatibles PyPI (CodeArtifact, Artifactory, GitHub Packages), registres de conteneurs (ECR, ACR, GHCR), buckets S3 pour les scripts, ou stockages de la plateforme (fichiers du workspace et volumes Databricks).

#### Comment gérer les dépendances Python de façon reproductible ?

Figer les versions exactes avec des fichiers de verrouillage (`uv.lock`, `poetry.lock`, requirements de `pip-tools`), séparer les dépendances d'exécution et de développement, compiler dans des environnements propres, et mettre à jour délibérément (Dependabot ou Renovate avec des tests).

#### Pourquoi utiliser des conteneurs pour les pipelines de données ?

Les conteneurs embarquent le code avec les dépendances et bibliothèques système exactes, rendant les exécutions identiques sur les postes, en CI et en production, et s'intègrent aux orchestrateurs comme Kubernetes, ECS, le KubernetesPodOperator d'Airflow et Cloud Run.

#### Comment apposer une version sur un paquet Python en CI ?

La dériver de Git (setuptools-scm, `git describe`) ou la fixer explicitement en CI à partir du numéro d'exécution et du SHA court, pour que chaque artefact corresponde à un commit ; évitez de réutiliser la même version pour du code différent.

#### Qu'est-ce qu'un SBOM ?

Une nomenclature logicielle (software bill of materials) qui liste tous les composants et dépendances (avec leurs versions) d'un artefact, générée en CI (Syft, CycloneDX) pour suivre vulnérabilités et licences.

#### Pourquoi analyser les images de conteneur en CI ?

Les images de base et les dépendances contiennent des vulnérabilités connues ; les analyseurs (Trivy, Grype, analyse du registre) les trouvent avant le déploiement, et des politiques peuvent bloquer les problèmes critiques.

### Stratégies de déploiement

#### Quelles stratégies de déploiement existent ?

Recreate (arrêter l'ancien, démarrer le nouveau), rolling (remplacer progressivement les instances), blue-green (basculer le trafic entre deux environnements complets), canary (envoyer d'abord une petite part vers la nouvelle version), shadow (faire tourner la nouvelle version en parallèle sans servir ses résultats) et feature flags (déployer désactivé, activer plus tard).

#### Comment le déploiement blue-green s'applique-t-il aux données ?

Construire la nouvelle version des tables ou pipelines à côté des actuelles (nouveau schéma, nouvelle version de table ou clone), la valider, puis basculer les consommateurs de façon atomique (échange de vues, renommage de tables, pointeur du catalogue), en gardant l'ancienne version pour un retour arrière rapide.

#### Qu'est-ce qu'une livraison canary pour les pipelines de données ?

Exécuter la nouvelle version sur un sous-ensemble (un pays, une partition, un échantillon de clients) ou en parallèle de l'ancienne, comparer sorties et indicateurs, puis élargir une fois la confiance acquise.

#### Qu'est-ce que le mode shadow ?

Faire tourner une nouvelle version d'un pipeline en parallèle sur des entrées réelles, en écrivant dans des tables séparées que personne ne consomme, et comparer les résultats avec la version de production avant de basculer.

#### Que sont les feature flags dans les plateformes de données ?

Des interrupteurs de configuration qui activent ou désactivent une nouvelle logique ou de nouvelles sorties sans redéployer, permettant un déploiement progressif, la désactivation rapide d'une fonction problématique et le découplage entre déploiement et mise à disposition.

#### Comment annuler un déploiement data ?

Redéployer l'artefact de code précédent et, pour les données, restaurer les tables avec le voyage dans le temps ou des snapshots, rebasculer les vues sur la version précédente (blue-green) ou relancer l'ancienne logique sur les partitions concernées. Planifiez le retour arrière avant de déployer des changements risqués.

#### Pourquoi les changements de schéma de base sont-ils risqués lors des déploiements ?

Ils peuvent casser le code en cours d'exécution, verrouiller des tables, exiger une migration de données et sont difficiles à annuler. Utilisez des changements rétrocompatibles (expand and contract), des migrations testées sur des clones, et déployez schéma et code par étapes compatibles.

#### Qu'est-ce que le modèle expand and contract ?

Faire les changements de schéma par phases : étendre (ajouter la nouvelle colonne ou table, garder l'ancienne), migrer (écrire dans les deux, faire le backfill, basculer les lecteurs), contracter (supprimer l'ancienne colonne quand plus personne ne l'utilise). Chaque étape est rétrocompatible.

#### Que sont les outils de migration de bases de données ?

Des outils qui appliquent des changements de schéma versionnés et ordonnés en gardant trace de ceux déjà exécutés : Flyway, Liquibase, Alembic (SQLAlchemy), Sqitch, schemachange (Snowflake), et dbt pour les objets gérés par la transformation.

#### Comment gérer les backfills lors des déploiements ?

Les intégrer au plan de livraison : estimer coût et durée, paramétrer les pipelines par plage de dates, exécuter par lots maîtrisés (souvent hors pointe), valider les sorties et prévenir les consommateurs quand des données historiques changent.

#### Comment déployer un changement sur une table très utilisée sans interruption ?

Construire la nouvelle version en parallèle (nouvelle table ou version), la valider, puis basculer atomiquement (swap, renommage ou mise à jour d'une vue), en gardant l'ancienne version pour un retour arrière ; évitez les réécritures sur place pendant que les consommateurs lisent.

#### Comment déployer un changement qui impose de recalculer l'historique ?

Planifier un backfill : déployer la nouvelle logique en écrivant dans une nouvelle table ou version, recalculer l'historique par lots, valider par rapport aux anciennes sorties, basculer les consommateurs et communiquer les chiffres retraités, plutôt que d'écraser l'historique sur place sans contrôle.

#### Qu'est-ce qu'un gel des déploiements, et quand est-il approprié ?

Une période sans déploiement en production, par exemple pendant la clôture comptable ou les pics de ventes, pour réduire le risque ; mieux vaut rendre les déploiements sûrs et routiniers, et garder les gels courts et réservés aux périodes réellement à risque.

#### Comment déployer des changements sur des jobs de streaming ?

Vérifier la compatibilité de l'état, arrêter proprement le job (savepoint ou checkpoint), déployer la nouvelle version depuis le même checkpoint si elle est compatible, ou démarrer un nouveau job avec un nouveau checkpoint et un plan de backfill ; pour les flux critiques, faire tourner ancienne et nouvelle version en parallèle.

### GitHub Actions en profondeur

#### Qu'est-ce que GitHub Actions ?

La plateforme de CI/CD et d'automatisation de GitHub : des workflows définis en YAML dans `.github/workflows/` s'exécutent sur des événements (push, pull request, planification, déclenchement manuel, releases) sur des runners hébergés par GitHub ou auto-hébergés.

#### Que sont les workflows, jobs et steps ?

Un workflow est un processus automatisé défini dans un fichier YAML ; il contient des jobs qui tournent sur des runners, en parallèle par défaut ou dans l'ordre avec `needs` ; chaque job a des steps qui exécutent des commandes (`run`) ou des actions (`uses`).

#### À quoi ressemble un workflow de CI de base pour un projet data Python ?

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

#### Quels déclencheurs peuvent lancer un workflow ?

`push`, `pull_request` (et `pull_request_target`), `schedule` (cron), `workflow_dispatch` (manuel, avec des entrées), `workflow_call` (réutilisable), `release`, `repository_dispatch` (API externe), `merge_group` (merge queue) et de nombreux autres événements du dépôt.

#### Comment lancer un workflow seulement quand certains fichiers changent ?

Avec des filtres de chemins sur le déclencheur, par exemple `on: pull_request: paths: ["models/**", "dbt_project.yml"]`, ou une étape qui détecte les fichiers modifiés et exécute des jobs conditionnellement, ce qui fait gagner du temps de CI dans les monorepos.

#### Qu'est-ce qu'un runner ?

La machine qui exécute les jobs : les runners hébergés par GitHub (Ubuntu, Windows, macOS, tailles plus grandes et GPU) sont des VM neuves par job ; les runners auto-hébergés sont vos propres machines ou pods Kubernetes, utilisés pour accéder à des réseaux privés, du matériel particulier ou pour le coût.

#### Pourquoi figer la version de l'image du runner ?

`ubuntu-latest` change quand GitHub passe à une nouvelle image, ce qui peut casser les builds sans prévenir. Figer `ubuntu-24.04` donne des builds reproductibles ; on met à jour délibérément.

#### Qu'est-ce qu'un build en matrice ?

Exécuter le même job avec différentes combinaisons de paramètres en parallèle, par exemple plusieurs versions de Python ou plusieurs adaptateurs dbt.

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

#### Comment fonctionne le cache dans GitHub Actions ?

`actions/cache` (ou le cache intégré de `setup-python`, `setup-node`, `setup-java`) conserve des répertoires comme les caches pip ou Maven avec une clé fondée sur le hachage des fichiers de verrouillage, et les restaure dans les exécutions suivantes pour accélérer l'installation des dépendances.

#### Que sont les artefacts dans GitHub Actions ?

Des fichiers produits par un job (rapports de tests, wheels construits, le site, manifestes dbt) téléversés avec `actions/upload-artifact` et téléchargeables par les jobs suivants ou par des personnes, avec une durée de rétention.

#### Comment les jobs se transmettent-ils des données ?

Par des artefacts pour les fichiers, et par des sorties de job pour les petites valeurs : une étape écrit `nom=valeur` dans `$GITHUB_OUTPUT`, le job déclare des `outputs`, et les jobs dépendants les lisent via le contexte `needs`.

#### Que sont les secrets et les variables dans GitHub Actions ?

Les secrets sont des valeurs chiffrées (jetons, mots de passe) disponibles pour les workflows et masquées dans les journaux ; les variables sont des valeurs de configuration non sensibles. Les deux se définissent au niveau de l'organisation, du dépôt ou de l'environnement et se référencent via les contextes `secrets` et `vars`.

#### Pourquoi les valeurs identifiantes doivent-elles être des secrets dans les dépôts publics ?

Les journaux des workflows des dépôts publics sont publics, et seuls les secrets sont masqués. Noms d'hôte, identifiants de compte, noms de buckets ou e-mails stockés en simples variables peuvent fuiter dans les journaux : traitez-les comme des secrets quand le dépôt est public.

#### Que sont les environnements GitHub ?

Des cibles de déploiement nommées (dev, staging, production) avec leurs propres secrets et variables et des règles de protection : relecteurs obligatoires, temporisations, restrictions de branches et historique des déploiements, qui conditionnent les jobs de CD.

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

#### Qu'est-ce que l'authentification OIDC de GitHub Actions vers le cloud ?

Le workflow demande à GitHub un jeton OpenID Connect de courte durée, que le fournisseur cloud (AWS, Azure, GCP) échange contre des identifiants temporaires pour un rôle qui fait confiance au dépôt, à la branche ou à l'environnement. Aucune clé d'accès de longue durée n'est stockée.

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

#### Comment restreindre les workflows autorisés à assumer un rôle cloud via OIDC ?

Dans la politique de confiance du rôle, en posant des conditions sur les claims du jeton : l'audience (`sts.amazonaws.com`), le dépôt et la référence ou l'environnement dans `sub` (par exemple `repo:org/repo:environment:production`), pour que seuls les déploiements de production de ce dépôt puissent l'assumer.

#### Qu'est-ce que le `GITHUB_TOKEN`, et comment régler ses droits ?

Un jeton créé automatiquement pour chaque exécution, limité au dépôt. Fixez `permissions:` au niveau du workflow ou du job au strict nécessaire (souvent `contents: read`), et n'accordez des droits supplémentaires comme `pull-requests: write` ou `id-token: write` qu'aux jobs qui en ont besoin.

#### Que sont les workflows réutilisables ?

Des workflows déclenchés par `workflow_call` que d'autres workflows invoquent avec `uses: ./.github/workflows/ci.yml` (ou depuis un autre dépôt), en passant des entrées et des secrets, pour définir une seule fois la logique de CI et la réutiliser, par exemple en exécutant toute la CI comme barrière dans le workflow de CD.

#### Que sont les actions composites ?

Des actions personnalisées définies avec `runs: using: composite` qui regroupent plusieurs étapes (préparation, installation, configuration) en une seule étape réutilisable, stockées dans le dépôt ou un dépôt partagé.

#### Que fait `concurrency` ?

Il regroupe les exécutions par une clé et les limite à une à la fois ; avec `cancel-in-progress: true`, une nouvelle exécution annule l'ancienne (bien pour la CI des PR), avec `false` les nouvelles attendent (indispensable pour les déploiements, afin que deux ne se chevauchent jamais).

```yaml
concurrency:
  group: deploy-production
  cancel-in-progress: false
```

#### Comment lancer des jobs planifiés dans GitHub Actions ?

Avec `on: schedule: - cron: "0 5 * * *"` (UTC). C'est pratique pour des contrôles nocturnes de dérive, des audits de dépendances ou de petits jobs data, mais cela ne remplace pas un orchestrateur : les planifications peuvent être retardées et sont désactivées sur les dépôts inactifs.

#### À quoi sert `workflow_dispatch` ?

Aux déclenchements manuels avec des entrées typées optionnelles, par exemple déployer une version précise, lancer un backfill sur une plage de dates ou démarrer un job de production après le déploiement.

#### Comment rendre des jobs conditionnels ?

Avec des expressions `if:` sur les jobs ou les étapes, en utilisant des contextes comme `github.ref`, `github.event_name`, `needs.<job>.result`, des variables (`vars.DEPLOY_AWS == 'true'`) ou des fonctions comme `success()`, `failure()` et `always()`.

#### Pourquoi figer les actions tierces sur un SHA de commit ?

Les tags comme `v4` peuvent être déplacés, et une action compromise pourrait exfiltrer des secrets. Figer sur un SHA complet (avec la version en commentaire) garantit le code exact exécuté ; Dependabot peut maintenir ces actions à jour.

#### Quelle différence entre `pull_request` et `pull_request_target` ?

`pull_request` s'exécute dans le contexte du commit de fusion avec un jeton en lecture seule et sans secrets pour les forks, ce qui est sûr. `pull_request_target` s'exécute dans le contexte du dépôt de base avec les secrets ; y récupérer et exécuter le code d'une PR non fiable est une faille bien connue.

#### Comment ajouter une approbation manuelle avant la production ?

Configurer l'environnement de production avec des relecteurs obligatoires ; les jobs qui référencent cet environnement se mettent en pause jusqu'à ce qu'un relecteur habilité approuve le déploiement dans l'interface de GitHub.

#### Qu'est-ce qu'une merge queue ?

Une fonction de GitHub qui teste les pull requests avec le main le plus récent (et entre elles) avant de les fusionner dans l'ordre, évitant le « PR au vert, main cassé » quand plusieurs PR fusionnent à peu d'intervalle ; la CI doit aussi tourner sur l'événement `merge_group`.

#### Comment bien afficher les résultats des tests dans GitHub Actions ?

Téléverser les rapports JUnit XML en artefacts et les publier avec une action de rapport, écrire un résumé du job dans `$GITHUB_STEP_SUMMARY` (Markdown), ou commenter les résultats dans la pull request.

#### À quoi servent les grands runners GitHub et les runners auto-hébergés pour les équipes data ?

Les grands runners aident pour les builds lourds ou les tests Spark ; les runners auto-hébergés dans votre réseau cloud peuvent atteindre des bases ou entrepôts privés pour les tests d'intégration sans les exposer publiquement, mais il faut les durcir et les isoler (les runners éphémères sont recommandés).

#### Comment GitHub Actions se compare-t-il à GitLab CI et Azure DevOps ?

Tous définissent des pipelines en YAML avec étapes ou jobs, runners/agents, variables et secrets, environnements et approbations. GitLab CI utilise `.gitlab-ci.yml` avec des stages et un registre intégré ; Azure DevOps utilise `azure-pipelines.yml` avec des stages, des service connections et une intégration étroite à Azure. Les concepts se transposent directement.

#### Comment passer des sorties entre jobs ?

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
      - run: echo "Déploiement de ${{ needs.version.outputs.tag }}"
```

#### Comment appeler un workflow réutilisable ?

```yaml
jobs:
  tests:
    uses: ./.github/workflows/ci.yml
  deploy:
    needs: tests
    runs-on: ubuntu-24.04
    environment: production
    steps:
      - run: echo "déployer après la réussite de la CI"
```

#### Comment déclencher un déploiement manuel avec des entrées ?

```yaml
on:
  workflow_dispatch:
    inputs:
      start_date:
        description: Première date du backfill (AAAA-MM-JJ)
        required: true
      run_job:
        type: boolean
        default: false
```

Les entrées sont ensuite disponibles via le contexte `inputs` dans les jobs et les étapes.

#### Comment définir le shell et le répertoire de travail par défaut ?

Avec `defaults: run:` au niveau du workflow ou du job, par exemple `shell: bash` et `working-directory: ./dbt`, pour que toutes les étapes `run` les utilisent ; dans GitHub Actions, les étapes bash s'exécutent par défaut avec `-e` (arrêt en cas d'erreur).

#### Comment écrire un résumé de job ?

En ajoutant du Markdown au fichier `$GITHUB_STEP_SUMMARY` (par exemple un tableau de nombres de lignes ou un rapport de tests), qui apparaît sur la page de synthèse de l'exécution.

#### Comment ajouter des timeouts aux jobs ?

Avec `timeout-minutes` sur les jobs (et les étapes), pour qu'un job bloqué ne consomme pas des minutes de runner pendant des heures ; le timeout par défaut d'un job est de 360 minutes.

#### Que sont les expressions et contextes dans GitHub Actions ?

Les expressions s'écrivent `${{ ... }}` dans le YAML des workflows et accèdent à des contextes comme `github` (données de l'événement et du dépôt), `env`, `vars`, `secrets`, `matrix`, `needs`, `steps`, `runner` et `inputs`, avec des fonctions comme `contains`, `startsWith`, `format`, `hashFiles` et les fonctions de statut.

#### Comment n'exécuter un job que sur la branche main après un push ?

`if: github.ref == 'refs/heads/main' && github.event_name == 'push'`, ce qui empêche de déployer depuis des pull requests ou d'autres branches.

#### Comment ne déployer que si une variable du dépôt est définie ?

Conditionner le job avec `if: vars.DEPLOY_AWS == 'true'`, pour que les jobs de déploiement restent inactifs tant que la configuration de l'environnement n'est pas prête, sans faire échouer la CI entre-temps.

#### Comment publier un commentaire sur une pull request depuis un workflow ?

Avec la CLI GitHub (`gh pr comment`) ou une action utilisant le `GITHUB_TOKEN` doté du droit `pull-requests: write`, par exemple pour partager un plan Terraform ou les résultats de la CI dbt.

#### Comment construire et publier une image Docker dans GitHub Actions ?

Avec `docker/setup-buildx-action`, `docker/login-action` (vers ECR, GHCR ou un autre registre, idéalement via OIDC) et `docker/build-push-action`, en taguant les images avec le SHA du commit et en utilisant le cache de couches.

#### Comment Dependabot ou Renovate aident-ils la CI/CD ?

Ils ouvrent des pull requests pour mettre à jour les dépendances et les GitHub Actions figées, qui passent par la CI comme tout changement, gardant la chaîne d'approvisionnement à jour par des mises à jour testées plutôt que de grosses mises à jour risquées.

### CI/CD pour dbt

#### Que lance un pipeline de CI pour dbt ?

Il installe les dépendances (`dbt deps`), vérifie le style SQL (SQLFluff), compile ou analyse, construit et teste les modèles modifiés et leurs descendants dans un schéma de CI isolé, vérifie la documentation et les conventions, et publie les résultats dans la pull request.

#### Qu'est-ce que la slim CI dans dbt ?

Construire et tester uniquement les modèles modifiés et leurs dépendances aval, en comparant l'état avec le manifeste de production : `dbt build --select state:modified+ --defer --state prod-artifacts/`, pour une CI rapide et peu coûteuse.

```yaml
- name: Télécharger le manifeste de production
  run: aws s3 cp s3://dbt-artifacts/prod/manifest.json prod-artifacts/manifest.json
- name: Construire les modèles modifiés
  run: dbt build --select state:modified+ --defer --state prod-artifacts --target ci
```

#### Que fait `--defer` ?

Quand un modèle référence un modèle amont non modifié qui n'a pas été construit dans le schéma de CI, dbt résout la référence vers la relation de production, si bien que la CI n'a pas à reconstruire tout le projet.

#### Comment isoler les exécutions de CI dbt ?

Avec une cible de CI qui écrit dans un schéma propre à chaque pull request (par exemple `dbt_ci_pr_123`), supprimé à la fin de l'exécution ou à la fermeture de la PR, pour que des PR simultanées n'entrent pas en collision.

#### Comment déployer dbt en production ?

À la fusion sur main, lancer `dbt build` (ou un job dbt Cloud) avec la cible de production depuis l'orchestrateur, conserver les artefacts (manifeste, résultats) pour la prochaine comparaison de slim CI, générer la documentation et alerter en cas d'échec.

#### Que sont les tests unitaires dbt ?

Des tests (dbt 1.8+) qui définissent des lignes d'entrée simulées pour les refs d'un modèle et la sortie attendue, exécutés sans données réelles, pour vérifier en CI une logique SQL complexe comme les case et les fonctions de fenêtre.

#### Comment éviter de casser les consommateurs avec des changements dbt ?

Avec les contrats de modèle (noms et types de colonnes imposés), les versions de modèle pour les changements cassants, les niveaux d'accès pour les modèles publics, les exposures documentant les tableaux de bord dépendants, et une CI qui construit les modèles aval (`state:modified+`).

#### Comment gérer le `profiles.yml` de dbt en CI ?

Committer un fichier de profils qui lit tous les réglages de connexion dans des variables d'environnement (`env_var('DBT_HOST')`), et définir ces variables depuis les secrets dans le workflow ; ne jamais committer d'identifiants.

#### Comment lancer les contrôles de fraîcheur des sources dbt ?

Avec `dbt source freshness` dans le job de production (avant la construction) ou selon un planning, en échouant ou en avertissant quand les sources dépassent les seuils, ce qui évite de construire sur des entrées périmées.

#### Comment générer et publier la documentation dbt ?

Lancer `dbt docs generate` dans le pipeline de production et publier le site statique (S3 avec CloudFront, GitHub Pages, dbt Cloud) ou pousser les métadonnées vers un catalogue, pour que la documentation corresponde à ce qui est déployé.

#### À quoi sert la commande « clone » de dbt en CI ?

`dbt clone` crée des clones zero-copy (ou des vues) des relations de production dans le schéma de CI ou de dev, pour que les modèles incrémentaux et les tests aval s'exécutent sur un état réaliste à faible coût.

### CI/CD pour Databricks, Airflow et les entrepôts

#### Comment mettre en place la CI/CD pour Databricks ?

Garder le code et les définitions des Databricks Asset Bundles dans Git ; en CI, tests unitaires sur Spark local, linting et `databricks bundle validate` ; en CD, déploiement avec `databricks bundle deploy -t <cible>` sous un service principal authentifié par OAuth ou fédération d'identité de charge de travail, avec éventuellement des jobs d'intégration en staging avant la production.

```yaml
- uses: databricks/setup-cli@main   # figer sur un SHA de commit en production
  with:
    version: ${{ vars.DATABRICKS_CLI_VERSION }}
- name: Valider et déployer le bundle
  env:
    DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
    DATABRICKS_CLIENT_ID: ${{ secrets.DATABRICKS_CLIENT_ID }}
    DATABRICKS_CLIENT_SECRET: ${{ secrets.DATABRICKS_CLIENT_SECRET }}
  run: |
    databricks bundle validate -t prod
    databricks bundle deploy -t prod
```

#### Pourquoi déployer les jobs Databricks sous un service principal ?

Pour que les jobs de production ne dépendent pas du compte et des droits d'une personne, que l'accès soit limité aux besoins du pipeline et que la propriété survive aux départs.

#### Comment déployer des DAG Airflow via la CI/CD ?

Lancer en CI les tests d'intégrité des DAG et les tests unitaires, construire une image avec les DAG et les dépendances figées (ou synchroniser les fichiers de DAG vers le bucket de MWAA ou Composer), déployer en staging, lancer des tests de fumée, puis promouvoir en production, le retour arrière consistant à redéployer l'image ou le commit précédent.

#### Comment gérer les changements Snowflake via la CI/CD ?

Les objets de compte (warehouses, rôles, droits, intégrations) avec Terraform ; les schémas et tables avec des outils de migration (schemachange, Flyway) ou des scripts `CREATE OR ALTER` ; les transformations avec dbt ; le tout déployé depuis la CI par un utilisateur de service authentifié par paire de clés ou OAuth, et testé d'abord sur une base clonée.

#### Comment déployer des jobs AWS Glue via la CI/CD ?

Empaqueter le code partagé en wheel, téléverser scripts et wheels dans S3 sous des chemins versionnés, définir jobs, triggers et tables du catalogue avec CloudFormation, CDK ou Terraform, et lancer les tests en local avec l'image Docker de Glue ou Spark avant le déploiement.

#### Comment tester en CI des pipelines qui dépendent de services cloud ?

Simuler les services dans les tests unitaires (moto pour AWS, LocalStack), utiliser des équivalents locaux (Spark avec Delta, conteneurs PostgreSQL, MinIO pour S3) pour les tests d'intégration, et lancer quelques tests contre un vrai compte bac à sable en staging.

#### Que sont les service containers dans GitHub Actions ?

Des conteneurs Docker démarrés à côté d'un job (par exemple PostgreSQL ou Redis) pour les tests d'intégration, définis sous `services:` avec ports et contrôles de santé.

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

#### Comment tester le code Databricks avant de le déployer ?

Tests unitaires sur Spark local (ou Databricks Connect), linting des motifs non pris en charge en serverless, `databricks bundle validate --strict`, déploiement sur une cible de développement ou de staging en `mode: development`, et exécution de jobs d'intégration à cet endroit.

#### Comment lancer un job Databricks depuis la CI après le déploiement ?

`databricks bundle run -t <cible> <job_key>` (avec `--no-wait` si l'on ne veut pas que la CI attende), ou via l'API Jobs ; pour la production, souvent uniquement sur déclenchement manuel.

#### Comment gérer les Variables et Connections Airflow en CI/CD ?

Garder la configuration non secrète dans le code ou dans des variables d'environnement de l'image, et les secrets dans un secrets backend ; ne jamais créer à la main les connexions de production dans l'interface, pour que les environnements soient reproductibles.

#### Comment déployer les transformations BigQuery ou Dataform ?

Avec les release configurations et workflow configurations de Dataform intégrées à Git, ou avec dbt et l'adaptateur BigQuery, en déployant depuis la CI avec un compte de service via la fédération d'identité de charge de travail.

### Sécurité de la chaîne de livraison

#### Quels sont les principaux risques de sécurité en CI/CD ?

Des secrets divulgués dans le code ou les journaux, des identifiants trop larges, des actions ou dépendances tierces compromises, du code non fiable exécuté avec des secrets (forks, `pull_request_target`), des runners auto-hébergés mal sécurisés, et des changements non relus qui atteignent la production.

#### Qu'est-ce que l'analyse de secrets ?

La détection de secrets dans le code et l'historique avec des outils comme gitleaks, TruffleHog ou l'analyse de secrets et la protection des push intégrées à GitHub, qui bloquent les commits et alertent en cas de fuite pour révoquer les identifiants.

#### Que faire si un secret est committé ?

Le révoquer et le renouveler immédiatement (considérez-le comme compromis), puis le retirer de l'historique si nécessaire ; supprimer le commit ne suffit pas, car des clones et des caches peuvent l'avoir conservé.

#### Qu'est-ce que la sécurité de la chaîne d'approvisionnement logicielle ?

La protection du chemin entre le code source et la production : dépendances et actions figées et vérifiées, analyse des vulnérabilités des dépendances (Dependabot, pip-audit), SBOM, artefacts signés et provenance (SLSA, Sigstore), et systèmes de build au moindre privilège.

#### Qu'est-ce que le moindre privilège en CI/CD ?

Chaque workflow et job ne reçoit que les droits nécessaires : jetons en lecture seule par défaut, identifiants de déploiement seulement dans les jobs de déploiement, secrets limités à l'environnement, et rôles cloud restreints à des ressources et branches précises.

#### Comment protéger la production des déploiements non autorisés ?

Protection de la branche main, revues obligatoires, règles de protection d'environnement avec approbateurs, politiques de confiance OIDC restreintes à l'environnement de production, et journaux d'audit des déploiements.

#### Comment gérer les données sensibles dans les journaux de CI ?

Ne jamais afficher de secrets ni de données réelles ; s'appuyer sur le masquage sans s'y fier totalement ; utiliser des données synthétiques dans les tests ; relire les journaux des dépôts publics ; et limiter la rétention des journaux.

#### Pourquoi les runners auto-hébergés sont-ils risqués, et comment les sécuriser ?

Ils exécutent du code de workflow arbitraire dans votre réseau ; une PR malveillante pourrait attaquer des systèmes internes. Utilisez des runners éphémères (un job par runner), n'y exécutez jamais de code de fork non fiable, isolez les réseaux et restreignez les dépôts autorisés à les utiliser.

#### Qu'est-ce qu'une attaque « poisoned pipeline execution » ?

Un attaquant modifie dans une pull request la configuration de CI ou des fichiers exécutés par la CI (scripts, Makefiles) pour que le pipeline exécute du code malveillant avec accès aux secrets. On l'atténue avec des jetons au moindre privilège, pas de secrets pour les PR non fiables et une revue obligatoire des changements de CI.

#### Comment protéger la configuration de CI elle-même ?

Exiger la revue des code owners pour `.github/workflows/`, restreindre qui peut modifier les environnements et les secrets, figer les actions et auditer les changements de workflows.

### Exploitation, supervision et DataOps

#### Que doit-il se passer après un déploiement ?

Des tests de fumée, la surveillance des exécutions de jobs et des contrôles de qualité à l'exécution suivante, la comparaison des indicateurs clés avec les exécutions précédentes et la notification de l'équipe ; revenir en arrière rapidement si les contrôles échouent.

#### Comment savoir si un déploiement data a cassé quelque chose ?

Avec des tests de qualité et l'observabilité des données (fraîcheur, volume, changements de schéma et de distribution), des alertes d'échec des pipelines, des rapprochements avec les sources et des tableaux de bord d'indicateurs clés comparés à leur historique récent.

#### Qu'est-ce que le GitOps ?

Utiliser Git comme source unique de vérité de l'état souhaité, avec des agents automatisés qui l'appliquent à l'environnement (Argo CD, Flux pour Kubernetes), de sorte que chaque changement soit un commit et que le système converge vers le contenu du dépôt.

#### Comment documenter une livraison ?

Avec les descriptions des pull requests, un changelog (souvent généré à partir des conventional commits), des notes de version pour les consommateurs décrivant l'impact sur les données (nouvelles colonnes, définitions modifiées, backfills) et des ADR pour les décisions importantes.

#### Comment communiquer les changements de données aux consommateurs ?

Par des changelogs et notes de version, des avis de dépréciation avec un calendrier, des mises à jour du catalogue, des montées de version des contrats, et une communication directe pour les changements cassants ou les retraitements de l'historique.

#### Comment mesurer le succès de la CI/CD dans une équipe data ?

Avec les métriques DORA (fréquence de déploiement, délai, taux d'échec des changements, délai de rétablissement), le nombre d'incidents de données causés par des changements, le temps passé en déploiements manuels, et la durée et le coût de la CI.

#### Comment garder une CI rapide à mesure que le projet grandit ?

Ne tester que ce qui a changé (filtres de chemins, slim CI), paralléliser jobs et tests, mettre en cache les dépendances, réduire les données synthétiques, déplacer les tests d'intégration lents sur main ou la nuit, et utiliser de plus grands runners quand c'est justifié.

#### Comment maîtriser les coûts de la CI ?

Annuler les exécutions obsolètes, éviter de lancer des jobs lourds à chaque commit, mettre en cache les dépendances, utiliser la slim CI sur les entrepôts, supprimer automatiquement les schémas de CI, fixer des timeouts sur les jobs, et surveiller minutes et dépenses d'entrepôt par dépôt.

#### Qu'est-ce qu'un journal des déploiements, et pourquoi le tenir ?

Un registre de la version déployée où et quand, par qui et avec quelles approbations (déploiements GitHub, historique des environnements, notes de version), indispensable pour relier les incidents aux changements.

#### Comment relier un incident de données à un déploiement ?

Comparer l'heure de début de l'incident à l'historique des déploiements, vérifier quels modèles ou jobs ont changé (diff Git entre versions), examiner le lignage des tables touchées et regarder les indicateurs de qualité avant et après.

#### Qu'est-ce que le chaos testing pour les pipelines de données ?

Introduire volontairement des pannes dans un environnement de test (jobs tués, fichiers manquants, sources en retard, changements de schéma) pour vérifier que relances, alertes, idempotence et procédures de reprise fonctionnent comme prévu.

### Mises en situation

#### Concevez un pipeline de CI/CD pour un projet dbt sur Snowflake.

Sur les pull requests : linting SQLFluff, `dbt deps`, `dbt build --select state:modified+ --defer` dans un schéma propre à la PR avec un utilisateur de service de CI, publication des résultats, suppression du schéma à la fin. À la fusion : déploiement en déclenchant le job de production (orchestrateur ou dbt Cloud), conservation des artefacts pour la comparaison suivante, publication de la documentation. Les warehouses et rôles sont gérés avec Terraform dans le même pipeline ou un pipeline séparé.

#### Concevez la CI/CD d'un lakehouse PySpark sur Databricks et AWS.

CI sur les pull requests : analyse de secrets, Ruff et règles de lint Spark maison, tests unitaires sur Spark local avec Delta, test de bout en bout sur données synthétiques, validation du bundle. CD sur main : réutiliser la CI comme barrière (workflow réutilisable), puis déployer l'ingestion AWS (SAM ou Terraform) via OIDC et le bundle Databricks sous un service principal, les deux dans un environnement de production protégé avec une concurrency réglée pour que les déploiements ne se chevauchent jamais.

#### Un déploiement a cassé une table de production. Qu'aurait dû détecter votre processus, et comment rétablir ?

D'abord rétablir : annuler le code, restaurer la table avec le voyage dans le temps ou relancer l'ancienne logique sur les partitions concernées, et prévenir les consommateurs. Ensuite améliorer le pipeline : ajouter un test pour le cas d'échec, un contrôle de contrat ou de schéma, une comparaison de non-régression en CI, ou le write-audit-publish pour ne pas exposer de données fausses.

#### Votre CI prend 45 minutes et les développeurs la contournent. Que faites-vous ?

Profiler le pipeline, paralléliser les jobs indépendants, mettre en cache les dépendances, ne lancer que les tests concernés (filtres de chemins, slim CI), réduire les données de test, déplacer les tests de bout en bout lents dans la merge queue ou sur main, et fixer un objectif (par exemple moins de 10 minutes pour les contrôles de PR).

#### Les journaux des workflows d'un dépôt public affichent le nom d'hôte d'une base de données. Que changez-vous ?

Passer le nom d'hôte et les autres valeurs identifiantes en secrets d'environnement pour qu'ils soient masqués, renouveler les identifiants si quelque chose de sensible est apparu, relire les journaux passés, et ajouter un contrôle empêchant d'afficher la configuration dans les journaux.

#### Comment passer de déploiements manuels à la CI/CD ?

Tout mettre dans Git (code, configuration, infrastructure), ajouter une CI avec linting et tests sur les pull requests, automatiser le déploiement vers un environnement de staging, ajouter tests de fumée et approbations, puis automatiser le déploiement en production avec les mêmes artefacts, et retirer progressivement l'accès manuel à la production.

#### Comment expliquer la CI/CD des données à un interlocuteur non technique ?

C'est une chaîne automatique de contrôle qualité et de livraison pour nos pipelines de données : chaque changement est testé avant de pouvoir toucher les rapports, et les changements approuvés arrivent en production toujours de la même façon sûre, pour que les chiffres restent fiables pendant que nous les améliorons rapidement.

#### Comment ajouter des barrières de qualité des données à un pipeline de CI/CD existant ?

Ajouter des tests de données au projet de transformation (unicité, non-nullité, relations, valeurs acceptées), les lancer en CI sur des données de test et en production après chaque construction, bloquer la publication (write-audit-publish ou échec du job) en cas d'échec critique, et alerter les responsables.

#### Deux équipes déploient dans le même workspace Databricks et écrasent mutuellement leurs jobs. Comment corriger ?

Utiliser des bundles aux noms et cibles distincts par équipe, déployer sous le service principal de chaque équipe avec des droits limités à ses ressources, utiliser le mode développement pour les déploiements personnels, et séparer les déploiements de production par dépôt et protections d'environnement.

#### Un `terraform apply` en CI a supprimé une ressource de production. Comment éviter que cela se reproduise ?

Exiger la revue du plan avant l'apply, ajouter des règles de cycle de vie `prevent_destroy` sur les ressources critiques, lancer des contrôles de politiques qui bloquent la suppression des ressources protégées, séparer état et droits par environnement, et, dans l'immédiat, restaurer depuis les sauvegardes ou réimporter la ressource.
