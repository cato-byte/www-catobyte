## Fiche d'étude CI/CD pour les données

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude CI/CD pour les données : environ 200 questions](../../images/cicd_data_study_guide_title_img.png)

Environ 200 questions d'entretien sur la CI/CD et l'automatisation des plateformes de données : workflows Git, stratégies de test des pipelines et des données, qualité du code, environnements, infrastructure as code, stratégies de déploiement, GitHub Actions en profondeur, CI/CD pour dbt, Databricks, Airflow et les entrepôts, sécurité de la chaîne de livraison et exploitation. Les exemples utilisent GitHub Actions, avec des remarques sur GitLab CI et Azure DevOps.

La fiche suit un parcours d'apprentissage en six étapes. Chaque section est découpée en unités courtes : objectifs d'apprentissage, explication du concept et exemple commenté, puis questions (d'abord de mémorisation, ensuite d'application), un exercice pratique et les points à retenir. Pour **apprendre**, lisez chaque unité du début à la fin. Pour **réviser**, passez en mode révision ou utilisez « Aller aux questions », marquez les réponses à revoir et essayez une révision mixte entre les sections.

<!-- QA -->
<!-- stage: Fondamentaux -->

### Fondamentaux

<!-- unit: CI/CD et DataOps -->

<!-- goals -->

- Expliquer le CI/CD et le DataOps, et pourquoi les équipes data en ont besoin.
- Décrire ce qui distingue le CI/CD pour les données de celui des applications.

<!-- concept -->

Les pipelines de données sont du logiciel et cassent de la même façon : une faute dans une jointure, un changement non testé, un déploiement manuel un vendredi. Le CI/CD fait de chaque changement une routine : intégré souvent, vérifié automatiquement, livré toujours de la même manière. Le DataOps étend cette habitude aux données, avec tests et supervision de ce que produisent les pipelines.
La difficulté en plus, c'est l'état. Une application se remplace ; une table avec cinq ans d'historique doit être migrée, recalculée et rester cohérente pour ses consommateurs.

<!-- example -->

| Étape | À la main | Avec CI/CD |
|---|---|---|
| Modifier un modèle dbt | Éditer en prod et espérer | PR, la CI le construit et le teste |
| Déployer | Copier des fichiers sur le serveur | Le pipeline déploie un artefact versionné |
| Savoir ce qui a cassé | Demander autour de soi | Historique Git et journal des déploiements |

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

<!-- challenge -->

Une équipe affirme : « notre SQL est simple, pas besoin de CI ». Donnez deux défaillances concrètes que la CI détecterait dans un projet purement SQL.

<!-- solution -->

Un modèle qui référence une colonne renommée (détecté en compilant et construisant dans un schéma de CI), et une jointure qui duplique des lignes (détectée par un test d'unicité sur la clé de sortie). Sans CI, les deux atteindraient les tableaux de bord.

<!-- takeaways -->

- Le CI/CD rend les changements petits, vérifiés et répétables.
- Le DataOps ajoute tests et supervision des données elles-mêmes.
- Les données ont un état : migrations et backfills sont nécessaires.

<!-- unit: Pipelines et étapes -->

<!-- goals -->

- Décrire les étapes d'un pipeline de déploiement et ce que chacune automatise.
- Distinguer continuous delivery, continuous deployment et releases.

<!-- concept -->

Un pipeline de déploiement est une chaîne de montage du commit à la production. Le build produit des artefacts, le test les vérifie, et le deploy installe ces mêmes artefacts dans chaque environnement tour à tour. Chaque étape est une barrière : un échec arrête la chaîne avant que les dégâts ne s'étendent.
Le degré d'automatisation est un choix. La continuous delivery garde chaque changement prêt à déployer ; le continuous deployment le livre automatiquement. Les releases, quand les utilisateurs voient le changement, peuvent être découplées des déploiements avec des flags.

<!-- example -->

```text
commit ─► lint + unit tests ─► build wheel/image/manifest ─► deploy staging
       ─► integration + data tests ─► [approval] ─► deploy prod ─► smoke test
```

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

<!-- challenge -->

Un nouveau modèle de revenus doit être livré cette semaine mais n'être activé pour la finance qu'en fin de mois. Comment séparer déploiement et release ?

<!-- solution -->

Déployer le modèle maintenant derrière un flag ou dans une nouvelle table que les tableaux de bord n'utilisent pas encore, le valider en production, puis basculer le tableau de bord finance dessus en fin de mois (flag ou vue).

<!-- takeaways -->

- Les pipelines construisent, testent et déploient les mêmes artefacts.
- La delivery garde les changements déployables ; le deployment les livre seul.
- Les releases peuvent être découplées des déploiements.

<!-- unit: Principes de livraison -->

<!-- goals -->

- Appliquer tout-en-code, petits changements et qualité shift-left.
- Mesurer la livraison avec les métriques DORA et la responsabilité.

<!-- concept -->

Quelques principes expliquent pourquoi le CI/CD fonctionne. Tout ce qui définit la plateforme vit dans du code, donc peut être relu et reconstruit. Les changements sont petits, faciles à comprendre et à annuler. Les problèmes sont détectés au plus tôt, là où ils coûtent le moins. Les pipelines sont déterministes : relancer donne le même résultat.
Responsabilité et mesure gardent le cap : l'équipe qui construit un pipeline l'exploite, et les métriques DORA montrent si la livraison devient plus rapide et plus sûre.

<!-- example -->

| Métrique DORA | Équipe data en bonne santé |
|---|---|
| Fréquence de déploiement | Plusieurs fois par semaine |
| Délai des changements | De quelques heures à un jour |
| Taux d'échec des changements | Sous 15 % |
| Temps de rétablissement | Moins d'une heure |

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

#### Pourquoi le code data doit-il être dans Git ?

La gestion de versions apporte l'historique (qui a changé quoi et pourquoi), la collaboration par branches et pull requests, la possibilité d'annuler, une source de vérité unique pour les déploiements et le déclencheur de la CI/CD.

<!-- challenge -->

Une équipe déploie une fois par mois un lot de 40 changements, et chaque release provoque des incidents. Quels deux changements aident le plus ?

<!-- solution -->

Déployer de petits changements en continu (trunk-based, pipeline automatisé) pour que chaque release soit petite et diagnosticable, et avancer tests et vérifications automatiques (shift left) pour que moins de défauts atteignent la production.

<!-- takeaways -->

- Le tout-en-code rend les plateformes relisibles et reconstructibles.
- Des changements petits et fréquents réduisent le risque.
- Les métriques DORA suivent vitesse et stabilité.

### Gestion de versions et workflows Git

<!-- unit: Ce qui va dans Git -->

<!-- goals -->

- Décider ce qui appartient à un dépôt data et ce qui n'y va jamais.
- Versionner correctement notebooks et gros fichiers.

<!-- concept -->

Git est la source de vérité de tout ce qui définit un pipeline : code, SQL, configuration, tests, infrastructure et documentation. Ce qui n'est pas dans Git ne peut être ni relu, ni reproduit, ni annulé.
Certaines choses doivent rester dehors : secrets, données personnelles réelles, gros jeux de données et fichiers générés. Notebooks et binaires demandent un traitement particulier, car leurs formats par défaut produisent des diffs illisibles ou gonflent le dépôt.

<!-- example -->

```gitignore
.env
*.parquet
data/
target/            # dbt build output
.venv/
**/.ipynb_checkpoints/
```

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

<!-- challenge -->

Un data scientist commite des notebooks dont les cellules de sortie contiennent des enregistrements clients. Que mettez-vous en place ?

<!-- solution -->

Supprimer automatiquement les sorties (nbstripout ou un hook pre-commit), stocker les notebooks comme fichiers source (Jupytext ou `.py` Databricks), retirer les données fuitées de l'historique et traiter l'événement comme un incident de données.

<!-- takeaways -->

- Code, SQL, config, tests et infrastructure vont dans Git.
- Secrets, données personnelles et gros fichiers jamais.
- Notebooks en source ; LFS pour les binaires nécessaires.

<!-- unit: Workflows de branches -->

<!-- goals -->

- Comparer trunk-based development et GitFlow.
- Garder des branches courtes et gérer hotfixes et organisation du dépôt.

<!-- concept -->

La stratégie de branches décide combien de temps les changements vivent séparés. Les branches longues s'éloignent de main, et les fusionner devient un projet à part entière. Le trunk-based development limite les branches à un ou deux jours et fusionne souvent de petits morceaux, d'où son affinité avec le CI/CD.
Les branches courtes exigent des techniques pour le travail inachevé, comme flags et chemins de code désactivés, et une voie claire pour les correctifs urgents. L'organisation du dépôt est un choix lié : un dépôt pour tout ou un par composant.

<!-- example -->

```text
main ──●──●──●──●──●──●──   (always deployable)
        \  /    \ /
  feat/orders-dedupe   fix/null-country   (hours to 2 days each)
```

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

<!-- challenge -->

Un développeur travaille depuis trois semaines sur une branche qui réécrit le pipeline clients, et la fusion provoque des conflits partout. Comment aurait-il fallu s'organiser ?

<!-- solution -->

Par petites étapes fusionnables : ajouter le nouveau pipeline à côté de l'ancien, derrière un flag ou en écrivant dans une nouvelle table, fusionner chaque partie dans main quand elle est prête, puis basculer les consommateurs et supprimer l'ancien code.

<!-- takeaways -->

- Le trunk-based development fusionne de petits changements chaque jour.
- Flags et chemins parallèles gardent le travail inachevé fusionnable.
- Les hotfixes passent par main et le pipeline normal.

<!-- unit: Revues et protections -->

<!-- goals -->

- Rédiger et relire des pull requests de code data.
- Imposer les revues avec la protection de branches et CODEOWNERS.

<!-- concept -->

La pull request est l'endroit où une deuxième personne voit un changement avant la production. Pour du code data, une bonne revue dépasse le style : grain et fan-out des jointures, gestion des nulls et doublons, idempotence, performance et impact sur les consommateurs.
Les réglages du dépôt rendent les revues obligatoires : les branches protégées exigent vérifications réussies et approbations, et les code owners sont ajoutés automatiquement sur les chemins qu'ils connaissent.

<!-- example -->

```text
# .github/CODEOWNERS
/models/finance/        @acme/finance-data
/infra/                 @acme/platform
/.github/workflows/     @acme/platform
```

#### Comment gérer les hotfixes en trunk-based development ?

Corriger sur une branche courte issue de main, fusionner par le pipeline normal (éventuellement accéléré) et déployer ; si une branche de release est en production, y faire aussi un cherry-pick de la correction. Évitez de corriger la production à la main.

#### Monorepo ou polyrepo pour les données ?

Un monorepo regroupe pipelines, modèles et infrastructure dans un seul dépôt (changements transverses faciles, outillage partagé, CI par chemins nécessaire) ; un polyrepo les sépare par domaine ou composant (responsabilités et accès clairs, coordination plus difficile). Les deux fonctionnent avec une bonne CI.

#### Comment garder des branches de fonctionnalité courtes ?

Découper le travail en petits changements fusionnables indépendamment, fusionner derrière des feature flags ou des planifications désactivées, rebaser souvent sur main et viser une fusion en un ou deux jours.

#### À quoi servent les tags Git dans les déploiements ?

À marquer les points de livraison (`v1.4.0`) qui déclenchent les workflows de release, à identifier exactement ce qui a été déployé et à permettre un retour arrière en redéployant un tag précédent.

<!-- challenge -->

Une PR fait passer une jointure de `customer_id` à `email` et tous les tests passent. Que demanderait un bon relecteur ?

<!-- solution -->

Si `email` est unique par client (sinon la jointure se démultiplie et duplique des lignes), comment sont gérés nulls et différences de casse, et quels modèles et tableaux de bord en aval changent. Demander un test d'unicité sur la sortie.

<!-- takeaways -->

- Relisez jointures, grain, nulls, idempotence et impact.
- La protection de branches rend vérifications et approbations obligatoires.
- CODEOWNERS oriente les revues vers les bonnes personnes.

<!-- unit: Versions et historique -->

<!-- goals -->

- Appliquer le versionnage sémantique au code et aux contrats de données.
- Utiliser conventional commits et tags dans les releases.

<!-- concept -->

Les versions disent ce que signifie un changement. Le versionnage sémantique le dit en trois nombres : un major casse quelque chose, un minor ajoute, un patch corrige. Cela vaut pour les bibliothèques, et aussi pour les contrats de données : renommer une colonne est un changement major pour les consommateurs.
Messages de commit et tags l'automatisent. Les conventional commits codent le type de changement, pour que les outils calculent la version suivante et le changelog, et les tags marquent exactement ce qui a été livré.

<!-- example -->

```text
fix(orders): exclude test customers from revenue      → 2.3.1
feat(orders): add refund_amount column                → 2.4.0
feat!(orders): rename amount to gross_amount          → 3.0.0
git tag v3.0.0 && git push origin v3.0.0              # triggers the release workflow
```

#### Comment gérer les notebooks dans Git ?

Les stocker comme fichiers source (format `.py` de Databricks, Jupytext) plutôt qu'en JSON avec leurs sorties, supprimer les sorties avant le commit, et garder la logique dans des modules importables avec des notebooks minces, pour des diffs relisibles.

#### À quoi sert Git LFS dans les dépôts data ?

Git LFS stocke les gros fichiers binaires (petits jeux de référence, données de test, images) hors de l'historique Git normal ; les gros volumes de production ne doivent pas du tout être dans Git.

#### À quoi ressemble la pyramide des tests pour les pipelines de données ?

De nombreux tests unitaires rapides de la logique de transformation, moins de tests d'intégration de composants avec de vrais moteurs (Spark, une base de test, dbt sur un schéma de test), quelques tests de bout en bout exécutant tout le pipeline sur des données d'exemple, plus des tests de qualité des données qui tournent en production sur les données réelles.

<!-- challenge -->

Une équipe renomme une colonne d'une table partagée comme « petite correction ». Trois tableaux de bord cassent. En quoi le versionnage aurait-il aidé ?

<!-- solution -->

Si la table est un contrat, le renommage est un changement major : le publier comme nouvelle version (ou nouvelle colonne) à côté de l'ancienne, annoncer une date de dépréciation et retirer l'ancien nom seulement après la migration des consommateurs.

<!-- takeaways -->

- MAJOR.MINOR.PATCH signale rupture, ajout et correction.
- Les contrats de données méritent aussi des versions.
- Conventional commits et tags automatisent les releases.

<!-- stage: Qualité -->

### Stratégie de test pour les données

<!-- unit: La pyramide des tests -->

<!-- goals -->

- Décrire tests unitaires, d'intégration, end-to-end et smoke pour les pipelines.
- Structurer le code pour que la logique soit testable unitairement.

<!-- concept -->

Les tests échangent vitesse contre réalisme. Les tests unitaires vérifient de petits bouts de logique en millisecondes ; les tests d'intégration, des composants face à de vraies dépendances ; les tests end-to-end exécutent tout le pipeline sur peu de données ; les smoke tests confirment qu'un déploiement fonctionne. Une suite saine compte beaucoup des premiers et peu des derniers.
Les tests unitaires ne sont bon marché que si la logique est séparée des I/O. Des fonctions qui prennent et renvoient des DataFrames se testent sans cluster ni entrepôt.

<!-- example -->

```python
def add_net_amount(df):                         # pure: DataFrame in, DataFrame out
    return df.withColumn("net", F.col("gross") - F.coalesce(F.col("discount"), F.lit(0)))

def test_add_net_amount(spark):
    df = spark.createDataFrame([(100, 10), (50, None)], "gross int, discount int")
    assert [r.net for r in add_net_amount(df).collect()] == [90, 50]
```

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

<!-- challenge -->

Les seuls tests d'un pipeline exécutent tout le job sur un cluster de staging et prennent 50 minutes. Comment rééquilibrer la suite ?

<!-- solution -->

Extraire la logique de transformation en fonctions pures couvertes par des tests unitaires rapides sur Spark local, garder quelques tests d'intégration pour les I/O, et lancer le job end-to-end complet chaque nuit ou avant les releases plutôt qu'à chaque PR.

<!-- takeaways -->

- Beaucoup de tests unitaires rapides, peu de tests lents et réalistes.
- Séparez logique pure et I/O pour tester à moindre coût.
- Les smoke tests confirment chaque déploiement.

<!-- unit: Tests de code et tests de données -->

<!-- goals -->

- Distinguer tests de logique et tests de données.
- Ajouter à la livraison des barrières de contrat, de régression et de qualité.

<!-- concept -->

Les tests de code demandent : « la logique fait-elle ce que je voulais sur des entrées choisies ? ». Les tests de données : « ce qui est réellement arrivé correspond-il à nos attentes ? ». Il faut les deux : un code parfait échoue quand même sur une source qui a changé dans la nuit.
Les tests de contrat se placent entre équipes et vérifient qu'un producteur livre toujours le schéma convenu. Les tests de régression comparent la sortie d'une nouvelle version à l'ancienne. Les barrières de qualité bloquent la publication quand les attentes échouent.

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

#### Pourquoi privilégier des données synthétiques en CI ?

Elles sont sûres (pas de données personnelles), petites (tests rapides), déterministes, et peuvent inclure délibérément des cas limites (nulls, doublons, enregistrements tardifs, unicode, valeurs extrêmes) rares dans de vrais échantillons.

#### Qu'est-ce qu'un test de contrat de données ?

Un test qui vérifie que la sortie d'un producteur respecte le schéma et la sémantique convenus dans un contrat de données (colonnes, types, nullabilité, valeurs autorisées), exécuté dans la CI du producteur pour que les changements cassants échouent avant la livraison.

#### Qu'est-ce que le test de non-régression des pipelines de données ?

Comparer les sorties de la nouvelle version à celles de la précédente sur la même entrée (nombres de lignes, agrégats, différences ligne à ligne), pour détecter les changements involontaires ; les outils incluent `datacompy`, dbt audit helper et les approches de data-diff.

#### Qu'est-ce qu'un test de fumée après déploiement ?

Une vérification rapide, juste après le déploiement, que le système fonctionne : les jobs sont enregistrés, une petite exécution réussit, les tables clés sont lisibles, les tableaux de bord se chargent. Il détecte tôt les erreurs de configuration et de droits.

<!-- challenge -->

Un refactoring d'un modèle de revenus passe tous les tests unitaires. Comment vérifier qu'il n'a pas changé les résultats ?

<!-- solution -->

Faire une comparaison de régression : construire la nouvelle version dans un schéma de CI ou de staging sur les mêmes entrées et comparer à la production nombres de lignes, agrégats et diff ligne à ligne par clé. Examiner tout écart avant de fusionner.

<!-- takeaways -->

- Les tests de code vérifient la logique ; ceux de données, les vraies données.
- Les contrats protègent les consommateurs des changements des producteurs.
- Les diffs de régression détectent les changements involontaires.

<!-- unit: Données de test et outillage -->

<!-- goals -->

- Gérer les données de test en privilégiant des fixtures synthétiques en CI.
- Utiliser fixtures pytest, comparaisons de DataFrames et golden files.

<!-- concept -->

Les tests ne valent que ce que valent leurs entrées. De petits jeux synthétiques conçus autour des cas limites sont rapides, déterministes et sans données personnelles : c'est le choix par défaut en CI. Les échantillons proches de la production, masqués, vont en staging.
L'outillage garde les tests courts : les fixtures partagent la préparation comme une session Spark, les helpers de comparaison donnent des diffs lisibles, et les golden files stockent les sorties attendues des cas plus gros. La vitesse compte, car on saute les suites lentes.

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

<!-- challenge -->

Chaque test crée sa propre SparkSession et la suite met 12 minutes pour 80 tests. Quelle est la correction la plus rapide ?

<!-- solution -->

Partager une SparkSession par session de tests via une fixture pytest de scope session, et baisser `spark.sql.shuffle.partitions` pour les très petites données. Le coût de démarrage n'est payé qu'une fois.

<!-- takeaways -->

- Les fixtures synthétiques sont sûres, petites et déterministes.
- Partagez la préparation coûteuse avec des fixtures.
- Les golden files stockent les sorties attendues des gros cas.

<!-- unit: Que tester dans un pipeline -->

<!-- goals -->

- Couvrir cas limites, idempotence et évolution de schéma.
- Tester les transformations SQL et les DAGs Airflow.

<!-- concept -->

Les pipelines échouent rarement sur le cas nominal. Ils échouent sur des entrées vides, des nulls dans les clés, des doublons, des enregistrements tardifs, une nouvelle colonne ou une relance qui ajoute deux fois. Des tests qui fournissent volontairement ces cas détectent à l'avance la plupart des incidents.
Chaque outil a ses points d'entrée : les modèles SQL se construisent sur des entrées seedées, les DAGs se chargent et s'inspectent, et l'idempotence se teste en exécutant une étape deux fois.

<!-- example -->

```python
def test_load_is_idempotent(spark, tmp_path):
    load_day(spark, "tests/fixtures/day.json", tmp_path, day="2026-10-17")
    first = spark.read.parquet(str(tmp_path)).count()
    load_day(spark, "tests/fixtures/day.json", tmp_path, day="2026-10-17")
    assert spark.read.parquet(str(tmp_path)).count() == first
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

<!-- challenge -->

Une source a ajouté une colonne et le pipeline a silencieusement perdu une autre colonne à cause d'un select positionnel. Quel test l'aurait détecté ?

<!-- solution -->

Un test d'évolution de schéma : fournir une fixture avec une colonne supplémentaire insérée au milieu et vérifier que le schéma et les valeurs de sortie ne changent pas. Puis corriger le code pour sélectionner par nom.

<!-- takeaways -->

- Testez entrées vides, nulles, en double, tardives et modifiées.
- Exécutez les étapes deux fois pour prouver l'idempotence.
- Construisez le SQL sur des seeds ; chargez les DAGs avec `DagBag`.

<!-- unit: Techniques de test avancées -->

<!-- goals -->

- Utiliser tests par propriétés et tests de mutation quand ils sont rentables.
- Suivre la performance sans ralentir chaque PR.

<!-- concept -->

Les tests par exemples ne vérifient que les cas auxquels quelqu'un a pensé. Les tests par propriétés génèrent de nombreuses entrées et vérifient des règles toujours vraies, comme « la déduplication n'augmente jamais le nombre de lignes ». Les tests de mutation évaluent les tests eux-mêmes en cassant volontairement le code pour voir si quelque chose échoue.
La performance a son propre rythme : les benchmarks sur volumes réalistes sont trop lents pour chaque PR, mais lancés régulièrement ils révèlent les régressions avant les utilisateurs.

<!-- example -->

```python
from hypothesis import given, strategies as st

@given(st.lists(st.tuples(st.integers(1, 5), st.integers())))
def test_dedupe_never_adds_rows(rows):
    assert len(dedupe_by_key(rows)) <= len(rows)
```

#### Comment tester les performances en CI ?

En général pas à chaque PR, mais par des benchmarks périodiques sur des volumes représentatifs, en suivant durée, volumes de shuffle et coût, avec des alertes en cas de régression ; des règles de lint peuvent détecter à moindre coût les anti-modèles de performance connus.

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

<!-- challenge -->

Une équipe a 95 % de couverture, pourtant des bugs continuent d'atteindre la production. En quoi les tests de mutation aideraient-ils ?

<!-- solution -->

Ils montrent si les tests vérifient vraiment le comportement : si des mutants (conditions inversées, constantes changées) survivent, ces tests exécutent du code sans vérifier ce qu'il faut. Renforcer les assertions là où des mutants survivent.

<!-- takeaways -->

- Les tests par propriétés vérifient des invariants sur des entrées générées.
- Les tests de mutation mesurent la solidité des tests.
- Mesurez la performance selon un calendrier, pas par PR.

### Qualité du code et contrôles statiques

<!-- unit: Linters et formatage -->

<!-- goals -->

- Mettre en place linters, formateurs et vérification de types pour le code data.
- Les lancer tôt avec pre-commit et des règles maison.

<!-- concept -->

Les vérifications statiques trouvent des problèmes sans rien exécuter. Les formateurs mettent fin aux débats de style ; les linters attrapent bugs et mauvais motifs ; les vérificateurs de types trouvent arguments erronés et gestion de `None`. Les lancer à chaque commit recentre les revues sur la logique.
Les équipes data gagnent aussi à avoir des règles maison : une vérification qui signale `collect()` sur de gros DataFrames ou `SELECT *` dans les modèles encode des leçons apprises à la dure.

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

<!-- challenge -->

Les revues de code tournent sans cesse au débat sur le style SQL. Qu'introduisez-vous ?

<!-- solution -->

Un formateur et linter SQL (SQLFluff) avec une configuration convenue, lancé en pre-commit et imposé en CI. Le style devient automatique et les revues se concentrent sur la logique.

<!-- takeaways -->

- Formateurs, linters et types détectent tôt les problèmes.
- Pre-commit les lance avant que le code ne quitte le poste.
- Les règles maison encodent les leçons de l'équipe.

<!-- unit: Vérifications au-delà du style -->

<!-- goals -->

- Ajouter analyse de sécurité et couverture à la CI.
- Valider projets dbt, YAML et fichiers de workflow.

<!-- concept -->

L'analyse statique couvre aussi sécurité et structure. Les scanners de sécurité signalent le code risqué et les définitions d'infrastructure non sûres. La couverture montre les zones non testées, comme signal et non comme objectif.
La configuration mérite autant de vérifications que le code : les projets dbt peuvent être analysés et évalués selon des conventions, le YAML validé contre des schémas et les fichiers de workflow CI passés au linter avant de s'exécuter.

<!-- example -->

```yaml
- run: dbt deps && dbt parse
- run: sqlfluff lint models/
- run: checkov -d infra/
- run: actionlint
- run: pytest --cov=src --cov-report=xml
```

#### Pourquoi ajouter des annotations de type au code data ?

Elles documentent les interfaces, permettent aux vérificateurs de types de détecter des erreurs (mauvais types d'arguments, gestion de `None`) avant l'exécution et améliorent l'IDE, ce qui compte pour les bibliothèques partagées par de nombreux pipelines.

#### Qu'est-ce que le dbt project evaluator ?

Un paquet dbt qui vérifie un projet au regard des bonnes pratiques (nommage des modèles, couches, références directes aux sources depuis les marts, tests ou documentation manquants, motifs de fan-out) et peut faire échouer la CI en cas d'écart.

#### Comment vérifier les fichiers YAML et de configuration ?

Par la validation de schéma (JSON Schema pour les configurations, `databricks bundle validate`, `actionlint` pour les workflows GitHub), yamllint pour la syntaxe et le style, et des tests qui chargent tous les fichiers de configuration utilisés par le pipeline.

#### Qu'est-ce qu'actionlint ?

Un vérificateur statique des fichiers de workflow GitHub Actions qui détecte erreurs de syntaxe, expressions invalides, entrées inconnues et problèmes de scripts shell avant l'exécution des workflows.

#### De quels environnements une plateforme de données a-t-elle besoin ?

Au minimum du développement (bacs à sable individuels ou partagés), un environnement de staging ou de préproduction reflétant la production, et la production. Certains ajoutent des environnements de test/recette ou des environnements éphémères par pull request.

#### Pourquoi séparer les environnements par compte, workspace ou catalogue ?

L'isolement limite la portée des erreurs, permet des droits différents (les développeurs ne peuvent pas écrire en production), sépare les coûts et rend la promotion explicite.

<!-- challenge -->

Un manager veut exiger 90 % de couverture sur toutes les PR. Que lui conseillez-vous ?

<!-- solution -->

Utiliser la couverture pour trouver le code critique non testé et éviter les fortes baisses, pas comme objectif strict : un chiffre élevé avec des assertions faibles rassure à tort. Exiger des tests pour la nouvelle logique et en relire la qualité.

<!-- takeaways -->

- Les scanners de sécurité vérifient code et infrastructure.
- La couverture est un signal, pas un objectif.
- Validez dbt, YAML et workflows en CI.

<!-- stage: Plateforme -->

### Environnements et configuration

<!-- unit: Environnements et isolation -->

<!-- goals -->

- Définir les environnements nécessaires à une plateforme data et leur isolation.
- Promouvoir les artefacts entre environnements avec un nommage cohérent.

<!-- concept -->

Les environnements offrent aux changements un chemin sûr vers la production. Le développement sert à construire, le staging à prouver, la production aux consommateurs. L'isolation, par compte, workspace ou catalogue, empêche qu'une erreur dans l'un atteigne les autres et permet des permissions différentes.
La parité donne son sens au staging : plus il ressemble à la production, plus un test réussi signifie quelque chose. Et la promotion fait passer le même artefact par chaque environnement au lieu de le reconstruire.

<!-- example -->

```text
dev:     catalog dev_sales,  workspace dev,  role developer (read prod)
staging: catalog stg_sales,  workspace stg,  role ci-deployer
prod:    catalog sales,      workspace prod, role prod-deployer (no humans)
artifact etl-2.4.1.whl  ──► dev ──► staging ──► prod
```

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

<!-- challenge -->

Le staging utilise une autre version de Spark et des clusters plus petits que la production, et des bugs n'apparaissent qu'en production. Que changez-vous ?

<!-- solution -->

Aligner le staging sur la production : mêmes versions de runtime, configuration et code d'infrastructure, avec des tailles réduites seulement là où elles ne changent pas le comportement. Déployer les deux depuis le même IaC avec des variables par environnement.

<!-- takeaways -->

- Dev, staging et prod offrent un chemin sûr aux changements.
- Isolez les environnements par compte, workspace ou catalogue.
- Parité et promotion rendent fiables les résultats du staging.

<!-- unit: Configuration par environnement -->

<!-- goals -->

- Sortir la configuration du code avec variables et fichiers par environnement.
- Utiliser des environnements éphémères pour les pull requests.

<!-- concept -->

Le même artefact doit tourner partout : ce qui diffère entre environnements, comme chemins, catalogues, tailles et endpoints, vient de la configuration, pas du code. La règle twelve-factor la place dans l'environnement, avec les secrets dans un gestionnaire de secrets.
Les environnements éphémères vont plus loin : chaque pull request reçoit son propre schéma ou workspace de courte durée, créé et détruit automatiquement, pour que les tests ne se marchent jamais dessus.

<!-- example -->

```yaml
# databricks.yml targets
targets:
  dev:     {variables: {catalog: dev_sales,  workers: 2}}
  staging: {variables: {catalog: stg_sales,  workers: 4}}
  prod:    {variables: {catalog: sales,      workers: 16}}
```

#### Qu'est-ce que le versionnage des données, et pourquoi est-il utile en CI/CD ?

Versionner les jeux de données comme le code (branches lakeFS, Project Nessie pour Iceberg, snapshots Delta et Iceberg, snapshots dbt) pour reproduire des exécutions, tester des changements sur des branches isolées des données et annuler des écritures fautives.

#### Qu'est-ce que le modèle write-audit-publish (WAP) ?

Écrire les nouvelles données dans un emplacement ou une branche de staging, les auditer avec des contrôles de qualité, puis seulement les publier (swap, merge ou fast-forward), pour que les consommateurs ne voient jamais de données fausses. Les branches Iceberg, lakeFS et les échanges de tables le mettent en œuvre.

#### Comment nommer les ressources d'un environnement à l'autre ?

Avec un schéma cohérent qui inclut l'environnement (`sales_prod`, `catalog_dev`, `dbt_ci_pr_123`), dérivé de la configuration plutôt que codé en dur, pour que le code ne pointe jamais par accident vers la production depuis le dev.

<!-- challenge -->

Deux PR lancent la CI en même temps et leurs tests écrasent mutuellement leurs tables dans un schéma de CI partagé. Que changez-vous ?

<!-- solution -->

Donner à chaque PR son propre schéma (par exemple `ci_pr_123`), créé au début de l'exécution et supprimé à la fermeture de la PR, avec le nom passé en configuration.

<!-- takeaways -->

- La configuration varie ; l'artefact non.
- Config dans l'environnement, secrets dans un coffre.
- Les environnements éphémères isolent chaque PR.

<!-- unit: Données hors production -->

<!-- goals -->

- Fournir des données réalistes et sûres au staging et au développement.
- Utiliser le versionnage des données et le write-audit-publish.

<!-- concept -->

Le code se copie librement entre environnements ; les données, non. Le staging a besoin de données proches de la production pour détecter de vrais problèmes, mais copier partout des données personnelles est un risque. La réponse habituelle : cloner ou échantillonner avec masquage, et un accès en lecture seule à la production pour le développement là où la politique l'autorise.
Le versionnage des données et le write-audit-publish appliquent la logique de la CI aux données : écrire dans une branche ou zone de staging, vérifier, puis publier de façon atomique.

<!-- example -->

```text
write:   INSERT INTO sales.orders_staging  (or Iceberg branch "audit")
audit:   row counts, uniqueness, freshness, reconciliation
publish: swap/fast-forward into sales.orders only if checks pass
```

#### Comment les développeurs travaillent-ils sans toucher aux données de production ?

Avec des schémas ou catalogues personnels, des cibles de développement qui lisent la production en lecture seule (ou des clones) et n'écrivent qu'en dev, des données échantillonnées ou masquées, et des droits qui interdisent l'écriture en production aux identités des développeurs.

#### Qu'est-ce que la promotion entre environnements ?

Faire passer le même artefact du dev au staging puis à la production après la réussite des contrôles à chaque étape, au lieu de le reconstruire, avec des approbations pour la production.

#### Le staging doit-il utiliser des données de production ?

Idéalement, le staging utilise des données proches de la production (clonées, échantillonnées ou masquées) pour détecter les problèmes du monde réel, avec un contrôle strict des données personnelles ; un staging purement synthétique peut manquer des problèmes que seules les données réelles révèlent.

#### Qu'est-ce que l'infrastructure as code (IaC) ?

La définition des ressources cloud (stockage, calcul, réseaux, droits, catalogues, jobs) dans du code déclaratif versionné, relu et appliqué automatiquement, plutôt que leur création à la main dans les consoles.

#### Quels outils d'IaC sont courants pour les plateformes de données ?

Terraform/OpenTofu (multi-cloud), AWS CloudFormation, CDK et SAM, Azure Bicep, Pulumi, et des outils propres aux plateformes comme les Databricks Asset Bundles, le provider Terraform de Snowflake et les manifestes Kubernetes avec Helm.

<!-- challenge -->

Un chargement nocturne a un jour publié une demi-journée de données dans les tableaux de bord avant d'échouer, et la direction a vu de faux chiffres. Quel motif l'empêche ?

<!-- solution -->

Le write-audit-publish : charger dans une table ou branche de staging, lancer les contrôles qualité et publier par un swap atomique seulement s'ils passent, pour que les consommateurs voient soit les anciennes données, soit les nouvelles complètes.

<!-- takeaways -->

- Le staging a besoin de données proches de la prod et masquées.
- Le développement lit la prod en lecture seule ou des échantillons.
- Le WAP ne publie qu'après les contrôles.

### Infrastructure as code

<!-- unit: Déclarer l'infrastructure -->

<!-- goals -->

- Expliquer l'infrastructure as code et ses principaux outils.
- Structurer l'IaC pour plusieurs environnements, permissions comprises.

<!-- concept -->

Créer des ressources à coups de clics ne laisse aucune trace et ne se répète pas. L'infrastructure as code déclare buckets, clusters, catalogues, jobs et permissions dans des fichiers : les environnements sont construits de la même façon à chaque fois et les changements passent en revue.
Une bonne structure garde cela gérable : modules réutilisables pour les pièces communes, variables par environnement, et remplacement immuable plutôt que correctifs sur place. Les permissions vont aussi dans le code, car ce sont elles qui dérivent le plus vite.

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

<!-- challenge -->

Les permissions de l'entrepôt ont été accordées à la main pendant des années, et personne ne sait qui a accès à quoi. Comment passer au code ?

<!-- solution -->

Exporter les grants actuels, les modéliser en rôles dans l'IaC, revoir et retirer l'inutile, importer les objets existants dans le state, puis ne modifier les grants que par pull requests. Détecter la dérive selon un calendrier.

<!-- takeaways -->

- L'IaC rend l'infrastructure relisible et reproductible.
- Modules et variables par environnement la gardent gérable.
- Les permissions vont aussi dans le code.

<!-- unit: Plan, state et dérive -->

<!-- goals -->

- Relire les changements d'infrastructure avec plan et apply.
- Gérer le state, détecter la dérive et appliquer des politiques.

<!-- concept -->

Les outils d'IaC comparent ce que le code déclare à ce qui existe, enregistré dans le state, et calculent un plan. Relire ce plan est la principale vérification de sécurité : il montre ce qui sera créé, modifié ou détruit avant que rien ne se passe.
Le state doit être stocké à distance avec verrouillage, et les changements manuels créent une dérive que le prochain apply peut annuler. La policy as code ajoute des règles automatiques à la revue humaine, comme interdire les buckets publics ou la suppression de ressources protégées.

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

#### Comment relire en sécurité les changements d'infrastructure ?

Publier le `terraform plan` (ou le diff CDK, le change set CloudFormation) en commentaire de la pull request, exiger la revue des responsables des ressources concernées, utiliser des contrôles de politiques (Checkov, OPA/Conftest, Sentinel), et n'appliquer que depuis la CI.

#### Qu'est-ce que la politique sous forme de code (policy as code) ?

L'écriture des règles de l'organisation (chiffrement obligatoire, pas de bucket public, tags obligatoires, régions autorisées) sous forme de code évalué automatiquement en CI ou au déploiement, par exemple avec Open Policy Agent, Checkov ou les services de politiques natifs du cloud.

#### Comment gérer les droits de la plateforme de données sous forme de code ?

Définir rôles, droits et permissions du catalogue dans Terraform ou les outils des plateformes (provider Snowflake, provider Terraform de Databricks, droits Unity Catalog dans les bundles), relus en pull request, pour que les changements d'accès soient auditables et réversibles.

#### Qu'est-ce qu'un artefact de compilation dans les projets data ?

La sortie versionnée d'une compilation qui est déployée : un wheel Python avec le code du pipeline, une image Docker, un JAR, un manifeste dbt compilé, un bundle ou un zip de scripts SQL. On compile une fois et on déploie le même artefact partout.

#### Pourquoi « compiler une fois, déployer plusieurs fois » ?

Recompiler pour chaque environnement peut produire des artefacts différents (changements de dépendances, moment de compilation), si bien que ce qui a été testé n'est pas ce qui est déployé. Compiler un artefact et le promouvoir garantit la cohérence.

#### Comment versionner les artefacts ?

Avec des versions sémantiques pour les bibliothèques, et des SHA de commit ou des numéros de build pour les applications (`0.2.145+g1a2b3c4`), apposés à la compilation pour que chaque déploiement soit traçable jusqu'à un commit.

<!-- challenge -->

Quelqu'un a modifié la taille d'un cluster de production dans la console. Que se passe-t-il au prochain apply Terraform, et quel devrait être le processus ?

<!-- solution -->

Terraform détecte la dérive et ramène la taille à la valeur du code. Le changement doit passer par le code via une PR ; lancer un `terraform plan` planifié pour détecter la dérive et alerter.

<!-- takeaways -->

- Relisez le plan avant chaque apply.
- Gardez le state distant et verrouillé.
- Détectez la dérive ; imposez les règles en policy as code.

### Empaquetage et artefacts

<!-- unit: Artefacts et versions -->

<!-- goals -->

- Construire une fois des artefacts versionnés et les déployer partout.
- Stocker les artefacts dans des registres et estampiller les versions en CI.

<!-- concept -->

Un artefact est exactement ce qui est déployé : un wheel, une image, un projet dbt compilé. Le construire une fois et promouvoir les mêmes octets dans chaque environnement garantit que ce qui a été testé est ce qui tourne en production.
Les versions relient les artefacts au code source : versions sémantiques pour les bibliothèques, SHA de commit pour les applications, toutes deux calculées automatiquement en CI. Les registres les conservent pour redéployer n'importe quelle version.

<!-- example -->

```bash
python -m build                                   # version from setuptools-scm: 2.4.1
twine upload --repository codeartifact dist/*
docker build -t $ECR/etl:$(git rev-parse --short HEAD) . && docker push $ECR/etl:$(git rev-parse --short HEAD)
```

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

<!-- challenge -->

La production se comporte autrement que le staging alors que « le code est le même ». Chaque environnement reconstruit l'image au déploiement. Pourquoi est-ce un problème ?

<!-- solution -->

Chaque reconstruction peut tirer d'autres versions de dépendances ou d'images de base : staging et prod exécutent des artefacts différents. Construire l'image une fois en CI, la taguer avec le SHA du commit et déployer ce même tag partout.

<!-- takeaways -->

- Les artefacts sont les unités déployables.
- Construisez une fois ; promouvez le même artefact.
- Versionnez depuis Git et stockez dans des registres.

<!-- unit: Dépendances et conteneurs -->

<!-- goals -->

- Rendre les dépendances Python reproductibles avec des lock files.
- Empaqueter avec des conteneurs et les analyser avec des SBOM.

<!-- concept -->

Des dépendances non figées font dériver les builds : le même code installe d'autres bibliothèques le mois suivant. Les lock files fixent des versions exactes, transitives comprises, pour qu'un build soit reproductible.
Les conteneurs étendent cela à tout le runtime, bibliothèques système comprises. Le prix, c'est d'être responsable de ce qu'ils contiennent : les images de base embarquent des vulnérabilités, donc on les scanne et un SBOM recense chaque composant.

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

#### Pourquoi analyser les images de conteneur en CI ?

Les images de base et les dépendances contiennent des vulnérabilités connues ; les analyseurs (Trivy, Grype, analyse du registre) les trouvent avant le déploiement, et des politiques peuvent bloquer les problèmes critiques.

#### Quelles stratégies de déploiement existent ?

Recreate (arrêter l'ancien, démarrer le nouveau), rolling (remplacer progressivement les instances), blue-green (basculer le trafic entre deux environnements complets), canary (envoyer d'abord une petite part vers la nouvelle version), shadow (faire tourner la nouvelle version en parallèle sans servir ses résultats) et feature flags (déployer désactivé, activer plus tard).

#### Comment le déploiement blue-green s'applique-t-il aux données ?

Construire la nouvelle version des tables ou pipelines à côté des actuelles (nouveau schéma, nouvelle version de table ou clone), la valider, puis basculer les consommateurs de façon atomique (échange de vues, renommage de tables, pointeur du catalogue), en gardant l'ancienne version pour un retour arrière rapide.

#### Qu'est-ce qu'une livraison canary pour les pipelines de données ?

Exécuter la nouvelle version sur un sous-ensemble (un pays, une partition, un échantillon de clients) ou en parallèle de l'ancienne, comparer sorties et indicateurs, puis élargir une fois la confiance acquise.

<!-- challenge -->

Un job nocturne a cassé parce qu'une dépendance a publié une nouvelle version majeure dans la nuit. Rien n'a changé dans le dépôt. Que changez-vous ?

<!-- solution -->

Figer toutes les dépendances avec un lock file et installer depuis celui-ci (`--frozen`), et laisser Dependabot ou Renovate proposer les mises à jour en PR qui passent par la CI.

<!-- takeaways -->

- Les lock files rendent les installations reproductibles.
- Les conteneurs figent tout le runtime.
- Scannez les images et tenez des SBOM.

<!-- stage: Livraison -->

### Stratégies de déploiement

<!-- unit: Stratégies pour le code et les données -->

<!-- goals -->

- Appliquer les déploiements blue-green, canary et shadow aux pipelines.
- Utiliser des feature flags pour contrôler la nouvelle logique.

<!-- concept -->

Les stratégies de déploiement réduisent le risque d'un changement en limitant qui le voit tant qu'il n'est pas éprouvé. Pour les données, les mêmes idées s'appliquent aux tables : construire la nouvelle version à côté de l'ancienne et basculer (blue-green), l'exécuter d'abord sur une tranche (canary), ou sur de vraies entrées sans que les consommateurs la voient (shadow).
Les feature flags offrent le même contrôle dans le code : la nouvelle logique est déployée mais inactive jusqu'à ce que quelqu'un l'active.

<!-- example -->

```sql
-- blue-green for a table: build v2, validate, then switch the view consumers use
CREATE TABLE marts.revenue_v2 AS SELECT ...;
-- validation queries comparing v1 and v2 ...
CREATE OR REPLACE VIEW marts.revenue AS SELECT * FROM marts.revenue_v2;
```

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

<!-- challenge -->

Un nouveau modèle d'attribution va modifier les chiffres marketing. Comment le livrer sans surprendre le métier ?

<!-- solution -->

L'exécuter en mode shadow pendant quelques semaines, en écrivant dans des tables séparées, et comparer avec le modèle actuel. Partager les écarts avec les parties prenantes, puis basculer avec un flag ou une vue à une date convenue.

<!-- takeaways -->

- Blue-green, canary et shadow limitent l'exposition.
- Pour les données, construisez les nouvelles tables à côté des anciennes.
- Les feature flags découplent déploiement et activation.

<!-- unit: Changements de schéma -->

<!-- goals -->

- Changer un schéma sans casser le code en cours ni les consommateurs.
- Utiliser expand-and-contract et les outils de migration.

<!-- concept -->

Les changements de schéma sont la partie la plus risquée des déploiements data : les jobs en cours attendent l'ancienne forme, les consommateurs lisent directement la table, et certains changements verrouillent les tables ou sont difficiles à annuler. Les faire en une étape force tous les lecteurs et écrivains à changer au même moment.
L'expand-and-contract découpe le changement : ajouter la nouvelle forme, migrer écrivains et lecteurs, puis retirer l'ancienne. Les outils de migration appliquent des changements ordonnés et suivis pour que chaque environnement aboutisse au même état.

<!-- example -->

```text
1. expand:   ADD COLUMN gross_amount; write both amount and gross_amount
2. migrate:  backfill gross_amount; move readers to gross_amount
3. contract: stop writing amount; DROP COLUMN amount (after deprecation date)
```

#### Que sont les outils de migration de bases de données ?

Des outils qui appliquent des changements de schéma versionnés et ordonnés en gardant trace de ceux déjà exécutés : Flyway, Liquibase, Alembic (SQLAlchemy), Sqitch, schemachange (Snowflake), et dbt pour les objets gérés par la transformation.

#### Comment gérer les backfills lors des déploiements ?

Les intégrer au plan de livraison : estimer coût et durée, paramétrer les pipelines par plage de dates, exécuter par lots maîtrisés (souvent hors pointe), valider les sorties et prévenir les consommateurs quand des données historiques changent.

#### Comment déployer un changement sur une table très utilisée sans interruption ?

Construire la nouvelle version en parallèle (nouvelle table ou version), la valider, puis basculer atomiquement (swap, renommage ou mise à jour d'une vue), en gardant l'ancienne version pour un retour arrière ; évitez les réécritures sur place pendant que les consommateurs lisent.

#### Comment déployer un changement qui impose de recalculer l'historique ?

Planifier un backfill : déployer la nouvelle logique en écrivant dans une nouvelle table ou version, recalculer l'historique par lots, valider par rapport aux anciennes sorties, basculer les consommateurs et communiquer les chiffres retraités, plutôt que d'écraser l'historique sur place sans contrôle.

<!-- challenge -->

Vous devez renommer `cust_id` en `customer_id` dans une table lue par 12 tableaux de bord. Planifiez-le.

<!-- solution -->

Ajouter `customer_id` et le remplir en parallèle de `cust_id` (ou l'exposer via une vue), annoncer la dépréciation, migrer les tableaux de bord, vérifier que `cust_id` n'est plus interrogé, puis le supprimer.

<!-- takeaways -->

- Les changements de schéma cassent code en cours et consommateurs.
- Étendre, migrer, puis contracter.
- Les outils de migration alignent les schémas entre environnements.

<!-- unit: Rollbacks, backfills et gels -->

<!-- goals -->

- Annuler code et données après un mauvais déploiement.
- Planifier backfills, gels et déploiements de streaming.

<!-- concept -->

Annuler du code est facile : redéployer l'artefact précédent. Annuler des données ne l'est pas : les tables contiennent déjà ce que la mauvaise version a écrit. Les plans doivent couvrir les deux, avec time travel, snapshots ou réexécution de l'ancienne logique.
Les changements qui exigent de recalculer l'historique sont des déploiements avec un coût et un calendrier. Les gels protègent les périodes critiques, et les jobs de streaming ajoutent un état qui doit survivre à la mise à jour.

<!-- example -->

```sql
-- data rollback on Delta / Iceberg after a bad deploy at 09:40
RESTORE TABLE marts.revenue TO TIMESTAMP AS OF '2026-10-17 09:30:00';
```

#### Qu'est-ce qu'un gel des déploiements, et quand est-il approprié ?

Une période sans déploiement en production, par exemple pendant la clôture comptable ou les pics de ventes, pour réduire le risque ; mieux vaut rendre les déploiements sûrs et routiniers, et garder les gels courts et réservés aux périodes réellement à risque.

#### Comment déployer des changements sur des jobs de streaming ?

Vérifier la compatibilité de l'état, arrêter proprement le job (savepoint ou checkpoint), déployer la nouvelle version depuis le même checkpoint si elle est compatible, ou démarrer un nouveau job avec un nouveau checkpoint et un plan de backfill ; pour les flux critiques, faire tourner ancienne et nouvelle version en parallèle.

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

<!-- challenge -->

Un changement de logique impose de recalculer trois ans d'une table de 4 To. Comment le déployer sans perturber les consommateurs ?

<!-- solution -->

Déployer la nouvelle logique dans une nouvelle version de la table, faire le backfill par lots avec concurrence limitée et estimation de coût, valider contre l'ancienne table, puis basculer les consommateurs de façon atomique (vue ou swap) et garder l'ancienne version un moment.

<!-- takeaways -->

- Prévoyez le rollback des données, pas seulement du code.
- Les backfills sont des releases avec coût et calendrier.
- Les déploiements de streaming doivent préserver l'état.

### GitHub Actions en profondeur

<!-- unit: Workflows, jobs et déclencheurs -->

<!-- goals -->

- Lire et écrire des workflows GitHub Actions avec jobs et steps.
- Choisir les déclencheurs : planifications, filtres de chemins, entrées manuelles.

<!-- concept -->

Un workflow est un fichier YAML qui dit quand s'exécuter et quoi faire. Les déclencheurs décident du quand : pushes, pull requests, planifications, exécutions manuelles avec entrées. Les jobs tournent en parallèle sur des machines séparées sauf s'ils dépendent l'un de l'autre ; les steps s'exécutent dans l'ordre au sein d'un job.
Les filtres de chemins gardent les workflows ciblés, pour qu'un changement de documentation ne lance pas la suite de tests Spark.

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

<!-- challenge -->

Un monorepo contient des modèles dbt et des jobs Python, et chaque PR lance les deux suites (30 minutes). Comment accélérer ?

<!-- solution -->

Séparer en deux workflows (ou jobs) avec filtres de chemins : les vérifications dbt sur les changements dans `models/`, les tests Python sur `src/` et `tests/`. Les fichiers partagés comme la config de CI déclenchent les deux.

<!-- takeaways -->

- Les workflows définissent les déclencheurs ; jobs en parallèle ; steps dans l'ordre.
- Les filtres de chemins ne lancent que les vérifications utiles.
- `workflow_dispatch` ajoute des exécutions manuelles avec entrées.

<!-- unit: Runners, cache et artefacts -->

<!-- goals -->

- Choisir les runners et figer leurs images.
- Accélérer les jobs avec cache et matrices, et passer fichiers et valeurs entre jobs.

<!-- concept -->

Chaque job tourne sur un runner neuf : c'est sûr, mais tout est oublié entre deux exécutions. Le cache restaure les dépendances pour ne pas tout réinstaller ; les artefacts transportent des fichiers d'un job à l'autre ; les outputs, de petites valeurs. Les matrices exécutent le même job sur plusieurs versions en parallèle.
Les runners eux-mêmes sont un choix : les images hébergées évoluent, donc figer une version évite les casses surprises, et il existe des runners plus grands ou self-hosted pour le travail lourd.

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

<!-- challenge -->

Le job de déploiement reconstruit le wheel déjà construit par le job de test, et déploie parfois une version légèrement différente. Corrigez-le.

<!-- solution -->

Construire une fois dans un job de build, téléverser le wheel comme artefact, lancer les tests dessus, et faire télécharger ce même artefact (et l'output de version) par le job de déploiement au lieu de reconstruire.

<!-- takeaways -->

- Les runners repartent de zéro ; cache et artefacts transmettent.
- Les outputs passent de petites valeurs entre jobs.
- Figez les images ; runners plus grands ou self-hosted pour le lourd.

<!-- unit: Secrets, environnements et OIDC -->

<!-- goals -->

- Stocker secrets et variables en sécurité, y compris dans les dépôts publics.
- Déployer avec environnements, approbations et OIDC plutôt qu'avec des clés durables.

<!-- concept -->

Les workflows ont besoin d'identifiants, et la façon de les fournir détermine votre exposition. Les secrets sont chiffrés et masqués dans les journaux ; les variables non, donc dans un dépôt public tout ce qui identifie va dans des secrets. Les environnements limitent les secrets à une cible et peuvent exiger une approbation avant l'exécution d'un job.
OIDC supprime toute clé cloud stockée : le workflow prouve son identité avec un jeton de courte durée, et le rôle cloud ne fait confiance qu'à des dépôts, branches ou environnements précis. Le `GITHUB_TOKEN` doit recevoir les permissions les plus étroites possibles.

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

<!-- challenge -->

Un dépôt stocke comme secret une clé d'accès AWS avec droits administrateur pour les déploiements. Par quoi la remplacez-vous ?

<!-- solution -->

Un rôle IAM assumé via GitHub OIDC, avec une trust policy limitée à ce dépôt et à l'environnement de production (claim `sub`), et des permissions limitées au besoin du déploiement. Puis supprimer la clé d'accès.

<!-- takeaways -->

- Les secrets sont masqués ; les variables sont visibles.
- Les environnements limitent les secrets et ajoutent des approbations.
- OIDC remplace les clés stockées par des jetons de courte durée.

<!-- unit: Contrôle du flux et réutilisation -->

<!-- goals -->

- Contrôler quand les jobs s'exécutent avec conditions, concurrence et timeouts.
- Réutiliser la logique avec reusable workflows et composite actions.

<!-- concept -->

Quand les pipelines grandissent, deux besoins apparaissent : décider précisément quand quelque chose s'exécute, et ne pas copier le même YAML dans dix dépôts. Les conditions utilisent des expressions sur des contextes comme la branche ou l'événement ; la concurrence empêche deux déploiements de se télescoper ; les timeouts empêchent les jobs bloqués de brûler des minutes.
La réutilisation existe en deux tailles : les composite actions regroupent des steps, les reusable workflows des jobs entiers appelés par d'autres workflows.

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

<!-- challenge -->

Deux merges à une minute d'écart lancent deux déploiements en production simultanés qui laissent les définitions de jobs dans un état mélangé. Qu'ajoutez-vous ?

<!-- solution -->

Un groupe `concurrency` pour les déploiements de production sans `cancel-in-progress` (pour qu'ils fassent la queue au lieu de se chevaucher), plus un timeout pour qu'un déploiement bloqué ne bloque pas la file indéfiniment.

<!-- takeaways -->

- Conditions et contextes décident quand les jobs s'exécutent.
- Les groupes de concurrence évitent les déploiements simultanés.
- Réutilisez avec composite actions et reusable workflows.

<!-- unit: Sécurité, retours et écosystème -->

<!-- goals -->

- Protéger les workflows du code non fiable et des dépendances mouvantes.
- Donner des retours clairs aux relecteurs et tenir les dépendances à jour.

<!-- concept -->

Les workflows exécutent du code, parfois venu d'inconnus. Les actions tierces peuvent changer sous un tag, et les déclencheurs qui tournent avec des secrets sur des pull requests de forks peuvent être détournés. Figer les actions sur des commits et bien choisir les déclencheurs ferme ces brèches ; les merge queues garantissent que ce qui arrive dans main a été testé avec main.
De bons retours entretiennent l'usage de la CI : rapports de tests, résumés et commentaires de PR placent les résultats là où l'on regarde. Les bots de dépendances et les autres systèmes de CI suivent les mêmes idées.

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

<!-- challenge -->

Un workflow utilise `pull_request_target` et fait un checkout du code de la PR pour lancer des tests avec les secrets de déploiement disponibles. Quel est le risque, et que faites-vous ?

<!-- solution -->

La PR d'un fork peut modifier le code de test pour exfiltrer des secrets, puisque `pull_request_target` s'exécute avec les secrets. Utiliser `pull_request` pour le code non fiable (sans secrets), et réserver les jobs à secrets aux branches de confiance ou après approbation.

<!-- takeaways -->

- Figez les actions sur des SHA ; prudence avec `pull_request_target`.
- Les merge queues testent les changements contre le dernier main.
- Résumés, rapports et commentaires rendent la CI visible.

### CI/CD pour dbt

<!-- unit: CI pour dbt -->

<!-- goals -->

- Construire un pipeline de CI pour dbt avec slim CI et defer.
- Isoler les exécutions de CI et sortir les paramètres de connexion du code.

<!-- concept -->

Construire tous les modèles dbt à chaque PR devient lent et coûteux quand les projets grandissent. Le slim CI ne construit que ce qui a changé et ce qui en dépend, en comparant au manifest de production. Le defer comble les trous en lisant depuis la production les modèles amont inchangés au lieu de les reconstruire.
Chaque PR écrit dans son propre schéma, et le profile lit toutes les informations de connexion dans des variables d'environnement : le même projet tourne en CI et en production sans modification.

<!-- example -->

```bash
dbt deps
sqlfluff lint models/
dbt build --select state:modified+ --defer --state prod-artifacts/ --target ci
# profiles.yml: schema: "dbt_ci_pr_{{ env_var('PR_NUMBER') }}", password: "{{ env_var('DBT_PASSWORD') }}"
```

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

<!-- challenge -->

Le slim CI échoue car un modèle modifié référence un modèle amont absent du schéma de CI. Que manque-t-il ?

<!-- solution -->

`--defer` avec le manifest de production (`--state`), pour que les références aux modèles non modifiés pointent vers les relations de production. Autre option : `dbt clone` des modèles amont nécessaires dans le schéma de CI au préalable.

<!-- takeaways -->

- Le slim CI construit les modèles modifiés et leurs enfants.
- Le defer lit les parents inchangés en production.
- Un schéma par PR ; identifiants via variables d'environnement.

<!-- unit: Déployer dbt en sécurité -->

<!-- goals -->

- Déployer dbt en production avec tests, fraîcheur et documentation.
- Protéger les consommateurs avec unit tests, contrats et versions.

<!-- concept -->

En production, dbt construit les modèles et exécute les tests dans l'ordre des dépendances : un test échoué empêche les mauvaises données de couler en aval. Les vérifications de fraîcheur des sources s'assurent d'abord que les entrées sont à jour, et la documentation est régénérée à chaque release.
La sécurité des consommateurs repose sur trois fonctions : les unit tests vérifient la logique sur des lignes fictives, les contrats imposent noms et types de colonnes, et les versions laissent un changement cassant cohabiter avec l'ancienne forme le temps que les consommateurs migrent.

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

#### À quoi sert la commande « clone » de dbt en CI ?

`dbt clone` crée des clones zero-copy (ou des vues) des relations de production dans le schéma de CI ou de dev, pour que les modèles incrémentaux et les tests aval s'exécutent sur un état réaliste à faible coût.

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

<!-- challenge -->

Une PR change le type d'une colonne d'un modèle utilisé par un outil BI, et le tableau de bord casse après déploiement. Qu'est-ce qui l'aurait empêché ?

<!-- solution -->

Un contrat de modèle imposé : la CI échouerait au changement de type. Pour un changement voulu, publier une nouvelle version du modèle et laisser les consommateurs migrer avant de retirer l'ancienne.

<!-- takeaways -->

- `dbt build` exécute modèles et tests dans l'ordre.
- La fraîcheur protège les entrées ; la doc part avec chaque release.
- Unit tests, contrats et versions protègent les consommateurs.

### CI/CD pour Databricks, Airflow et les entrepôts

<!-- unit: Databricks -->

<!-- goals -->

- Mettre en place le CI/CD pour Databricks avec Asset Bundles et service principals.
- Tester, déployer et exécuter des jobs depuis la CI sans collisions entre équipes.

<!-- concept -->

Les Databricks Asset Bundles décrivent jobs, pipelines et leurs réglages dans des fichiers à côté du code, avec des targets par environnement. La CI les valide et les teste ; le CD les déploie en tant que service principal, pour que la production ne dépende jamais du compte d'une personne.
Les bundles règlent aussi la question de la propriété : chaque bundle a un nom et un chemin de déploiement, donc deux équipes qui déploient dans un même workspace n'écrasent pas leurs jobs respectifs.

<!-- example -->

```bash
databricks bundle validate -t staging
pytest tests/unit
databricks bundle deploy -t staging          # as the staging service principal
databricks bundle run -t staging smoke_test_job
databricks bundle deploy -t prod             # after approval
```

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

<!-- challenge -->

Des jobs de production échouent depuis le départ de l'ingénieur qui les avait créés. Qu'est-ce qui n'allait pas, et comment corriger ?

<!-- solution -->

Les jobs tournaient sous l'identité de cette personne, désactivée depuis. Les redéployer via des bundles avec un service principal comme propriétaire et identité run-as, les permissions étant accordées au principal et non à des personnes.

<!-- takeaways -->

- Les bundles gardent les ressources Databricks en code avec des targets.
- Déployez et exécutez en tant que service principals.
- Des noms et chemins de bundle distincts évitent les collisions.

<!-- unit: Airflow, Glue et entrepôts -->

<!-- goals -->

- Déployer des DAGs Airflow et des jobs Glue par CI/CD.
- Gérer en code les changements Snowflake et BigQuery.

<!-- concept -->

Chaque plateforme a sa mécanique de déploiement, mais le motif se répète : tester en CI, construire un artefact versionné, le déployer en infrastructure as code, garder les secrets hors de l'artefact. Pour Airflow, une image avec les DAGs ; pour Glue, scripts et wheels dans des chemins S3 versionnés ; pour les entrepôts, des objets répartis entre IaC pour le niveau compte et outils de migration ou dbt pour les schémas.
Configuration et secrets suivent partout la même règle : configuration depuis l'environnement, secrets depuis un gestionnaire.

<!-- example -->

| Plateforme | Artefact | Déployé avec |
|---|---|---|
| Airflow | Image avec DAGs et providers figés | Helm / synchro S3 MWAA |
| Glue | Script + wheel dans `s3://artifacts/<sha>/` | Terraform / CDK |
| Snowflake | Rôles, warehouses ; schémas | Terraform ; dbt ou schemachange |
| BigQuery | Release Dataform | Release configurations |

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

<!-- challenge -->

Les connexions Airflow sont créées à la main dans l'UI de chaque environnement, et le staging pointe par erreur vers la production. Que changez-vous ?

<!-- solution -->

Définir les connexions par environnement dans un secrets backend (ou des variables d'environnement) géré en code, avec des noms identiques entre environnements et des valeurs différentes. Supprimer les connexions créées dans l'UI.

<!-- takeaways -->

- Partout le même motif : tester, construire, déployer en code.
- Versionnez les artefacts par commit.
- Configuration depuis l'environnement, secrets depuis un gestionnaire.

<!-- unit: Tester face aux services cloud -->

<!-- goals -->

- Tester du code dépendant de services cloud sans accès à la production.
- Utiliser des service containers pour les tests d'intégration.

<!-- concept -->

Le code qui appelle S3, Glue ou une base de données est difficile à tester en CI sans toucher de vrais systèmes. Les couches aident : simuler le service dans les tests unitaires, utiliser des équivalents locaux comme LocalStack ou un conteneur PostgreSQL pour l'intégration, et garder quelques tests contre un vrai compte sandbox.
Les service containers en CI démarrent ces dépendances à côté du job : les tests d'intégration tournent à chaque PR sans rien à nettoyer.

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

#### Comment protéger la production des déploiements non autorisés ?

Protection de la branche main, revues obligatoires, règles de protection d'environnement avec approbateurs, politiques de confiance OIDC restreintes à l'environnement de production, et journaux d'audit des déploiements.

#### Comment gérer les données sensibles dans les journaux de CI ?

Ne jamais afficher de secrets ni de données réelles ; s'appuyer sur le masquage sans s'y fier totalement ; utiliser des données synthétiques dans les tests ; relire les journaux des dépôts publics ; et limiter la rétention des journaux.

<!-- challenge -->

Les tests d'intégration écrivent dans un vrai bucket S3 d'un compte dev partagé et suppriment parfois les fichiers les uns des autres. Que changez-vous ?

<!-- solution -->

Utiliser moto ou LocalStack pour la plupart des tests S3, et pour les quelques tests sur le vrai service, un préfixe unique par exécution de CI avec nettoyage automatique (et une règle de lifecycle en secours).

<!-- takeaways -->

- Simulez en tests unitaires ; équivalents locaux pour l'intégration.
- Les service containers démarrent les dépendances à côté du job.
- Isolez par exécution les tests sur de vrais services.

<!-- stage: Exploiter en sécurité -->

### Sécurité de la chaîne de livraison

<!-- unit: Secrets et fuites -->

<!-- goals -->

- Identifier les principaux risques de sécurité du CI/CD.
- Scanner les secrets et réagir quand l'un fuit.

<!-- concept -->

Un pipeline de livraison détient les clés de la production, ce qui en fait une cible. La défaillance la plus fréquente est simple : un secret dans le code, l'historique ou les journaux. Le scan en attrape la plupart avant qu'ils ne quittent le poste.
Quand l'un fuit malgré tout, le retirer de Git ne suffit pas, car des copies peuvent déjà exister. Révoquer et renouveler d'abord, puis nettoyer et vérifier s'il a été utilisé.

<!-- example -->

```bash
gitleaks detect --source . --log-opts="--all"     # scan the full history
# leaked key? 1) revoke/rotate  2) check CloudTrail for use  3) purge history  4) add a pre-commit hook
```

#### Pourquoi les runners auto-hébergés sont-ils risqués, et comment les sécuriser ?

Ils exécutent du code de workflow arbitraire dans votre réseau ; une PR malveillante pourrait attaquer des systèmes internes. Utilisez des runners éphémères (un job par runner), n'y exécutez jamais de code de fork non fiable, isolez les réseaux et restreignez les dépôts autorisés à les utiliser.

#### Qu'est-ce qu'une attaque « poisoned pipeline execution » ?

Un attaquant modifie dans une pull request la configuration de CI ou des fichiers exécutés par la CI (scripts, Makefiles) pour que le pipeline exécute du code malveillant avec accès aux secrets. On l'atténue avec des jetons au moindre privilège, pas de secrets pour les PR non fiables et une revue obligatoire des changements de CI.

#### Comment protéger la configuration de CI elle-même ?

Exiger la revue des code owners pour `.github/workflows/`, restreindre qui peut modifier les environnements et les secrets, figer les actions et auditer les changements de workflows.

#### Que doit-il se passer après un déploiement ?

Des tests de fumée, la surveillance des exécutions de jobs et des contrôles de qualité à l'exécution suivante, la comparaison des indicateurs clés avec les exécutions précédentes et la notification de l'équipe ; revenir en arrière rapidement si les contrôles échouent.

<!-- challenge -->

Un développeur a poussé un mot de passe de base de données sur une branche, puis fait un force-push pour le retirer une heure plus tard. L'affaire est-elle close ?

<!-- solution -->

Non. Le considérer comme compromis : changer le mot de passe, vérifier les accès dans les journaux de la base, et vérifier si forks, caches ou journaux de CI l'ont capturé. Ajouter le scan de secrets en pre-commit et la push protection.

<!-- takeaways -->

- Les secrets fuités sont le risque CI/CD le plus courant.
- Scannez code et historique en continu.
- Renouvelez d'abord ; supprimer le commit ne suffit pas.

<!-- unit: Chaîne d'approvisionnement et moindre privilège -->

<!-- goals -->

- Appliquer moindre privilège et contrôles de chaîne d'approvisionnement au CI/CD.
- Protéger la configuration de CI et les runners contre les abus.

<!-- concept -->

Tout ce à quoi le pipeline fait confiance peut servir de porte d'entrée : dépendances, actions tierces, runners et la configuration de CI elle-même. Les attaques de poisoned pipeline modifient des fichiers que la CI exécute : une pull request malveillante peut lancer du code avec les permissions du pipeline.
Le moindre privilège limite les dégâts : jetons en lecture seule par défaut, permissions de déploiement seulement dans les jobs de déploiement, production accessible uniquement depuis des branches protégées avec approbations. Les runners self-hosted exigent une isolation renforcée car ils vivent dans votre réseau.

<!-- example -->

```text
default GITHUB_TOKEN:       contents: read
deploy job:                 id-token: write, environment: production (approvers)
cloud role trust:           repo:acme/lake:environment:production only
.github/workflows/**:       CODEOWNERS = platform team
self-hosted runners:        ephemeral, no access from fork PRs
```

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

<!-- challenge -->

N'importe quel développeur peut modifier les fichiers de workflow, et le rôle du job de déploiement peut déployer en production depuis n'importe quelle branche. Citez trois contrôles à ajouter.

<!-- solution -->

Une revue CODEOWNERS pour `.github/workflows/`, une trust policy OIDC restreinte à l'environnement de production sur main, et une protection d'environnement avec relecteurs obligatoires. Jetons par défaut en lecture seule.

<!-- takeaways -->

- Dépendances, actions, runners et config de CI sont des surfaces d'attaque.
- Moindre privilège par job et par environnement.
- Protégez les fichiers de workflow avec des code owners.

### Exploitation, supervision et DataOps

<!-- unit: Après le déploiement -->

<!-- goals -->

- Vérifier qu'un déploiement n'a pas cassé les données.
- Relier incidents et déploiements, et s'exercer aux pannes.

<!-- concept -->

Un pipeline au vert dit seulement que le code a été déployé. Que les données soient toujours justes se voit plus tard : dans les contrôles qualité de l'exécution suivante, la fraîcheur, les volumes et les tableaux de bord utilisés. Surveiller ces signaux après chaque déploiement boucle la boucle.
Quand quelque chose casse, un journal des déploiements répond à la première question, ce qui a changé, et le chaos testing en staging montre comment les pipelines réagissent aux pannes avant qu'elles n'arrivent pour de vrai.

<!-- example -->

```text
deploy 14:02  etl v2.4.1 (PR #318, approved by @ana)
14:05  smoke test: job registered, 1-day run OK
06:10  next run: row count -38% vs 7-day avg  ← alert
→ diff v2.4.0..v2.4.1 shows a changed join in orders_enriched
```

#### Comment maîtriser les coûts de la CI ?

Annuler les exécutions obsolètes, éviter de lancer des jobs lourds à chaque commit, mettre en cache les dépendances, utiliser la slim CI sur les entrepôts, supprimer automatiquement les schémas de CI, fixer des timeouts sur les jobs, et surveiller minutes et dépenses d'entrepôt par dépôt.

#### Qu'est-ce qu'un journal des déploiements, et pourquoi le tenir ?

Un registre de la version déployée où et quand, par qui et avec quelles approbations (déploiements GitHub, historique des environnements, notes de version), indispensable pour relier les incidents aux changements.

#### Comment relier un incident de données à un déploiement ?

Comparer l'heure de début de l'incident à l'historique des déploiements, vérifier quels modèles ou jobs ont changé (diff Git entre versions), examiner le lignage des tables touchées et regarder les indicateurs de qualité avant et après.

#### Qu'est-ce que le chaos testing pour les pipelines de données ?

Introduire volontairement des pannes dans un environnement de test (jobs tués, fichiers manquants, sources en retard, changements de schéma) pour vérifier que relances, alertes, idempotence et procédures de reprise fonctionnent comme prévu.

#### Concevez un pipeline de CI/CD pour un projet dbt sur Snowflake.

Sur les pull requests : linting SQLFluff, `dbt deps`, `dbt build --select state:modified+ --defer` dans un schéma propre à la PR avec un utilisateur de service de CI, publication des résultats, suppression du schéma à la fin. À la fusion : déploiement en déclenchant le job de production (orchestrateur ou dbt Cloud), conservation des artefacts pour la comparaison suivante, publication de la documentation. Les warehouses et rôles sont gérés avec Terraform dans le même pipeline ou un pipeline séparé.

<!-- challenge -->

Le chiffre d'affaires a chuté de 20 % sur un tableau de bord ce matin. Comment vérifier si un déploiement en est la cause ?

<!-- solution -->

Comparer l'heure de début de la baisse au journal des déploiements, lister les modèles et jobs modifiés dans ces déploiements (diff Git), suivre le lignage jusqu'au modèle de revenus et exécuter la version précédente sur les mêmes entrées pour comparer.

<!-- takeaways -->

- Surveillez la qualité des données après chaque déploiement.
- Un journal des déploiements répond à « qu'est-ce qui a changé ? ».
- Exercez-vous aux pannes en staging avec des chaos tests.

<!-- unit: Releases et communication -->

<!-- goals -->

- Documenter les releases et communiquer les changements de données aux consommateurs.
- Appliquer le GitOps et mesurer le succès de la livraison.

<!-- concept -->

Les consommateurs ne lisent pas vos pull requests : les changements doivent leur parvenir dans leurs termes, quoi, quand et ce qu'ils doivent faire. Changelogs, notes de release et avis de dépréciation datés y répondent, générés depuis les messages de commit quand c'est possible.
Le GitOps fait de Git le registre de ce qui doit être déployé, avec des agents qui l'appliquent. Le succès se mesure non seulement en fréquence de déploiement, mais en incidents moins nombreux et rétablissement plus rapide.

<!-- example -->

```markdown
## Release 3.0.0 – 2026-10-20
- **Breaking:** `fct_orders.amount` renamed to `gross_amount`. Old name available until 2026-11-30.
- Added `refund_amount` (nullable).
- Fixed: test customers excluded from revenue.
```

#### Concevez la CI/CD d'un lakehouse PySpark sur Databricks et AWS.

CI sur les pull requests : analyse de secrets, Ruff et règles de lint Spark maison, tests unitaires sur Spark local avec Delta, test de bout en bout sur données synthétiques, validation du bundle. CD sur main : réutiliser la CI comme barrière (workflow réutilisable), puis déployer l'ingestion AWS (SAM ou Terraform) via OIDC et le bundle Databricks sous un service principal, les deux dans un environnement de production protégé avec une concurrency réglée pour que les déploiements ne se chevauchent jamais.

#### Un déploiement a cassé une table de production. Qu'aurait dû détecter votre processus, et comment rétablir ?

D'abord rétablir : annuler le code, restaurer la table avec le voyage dans le temps ou relancer l'ancienne logique sur les partitions concernées, et prévenir les consommateurs. Ensuite améliorer le pipeline : ajouter un test pour le cas d'échec, un contrôle de contrat ou de schéma, une comparaison de non-régression en CI, ou le write-audit-publish pour ne pas exposer de données fausses.

#### Votre CI prend 45 minutes et les développeurs la contournent. Que faites-vous ?

Profiler le pipeline, paralléliser les jobs indépendants, mettre en cache les dépendances, ne lancer que les tests concernés (filtres de chemins, slim CI), réduire les données de test, déplacer les tests de bout en bout lents dans la merge queue ou sur main, et fixer un objectif (par exemple moins de 10 minutes pour les contrôles de PR).

#### Les journaux des workflows d'un dépôt public affichent le nom d'hôte d'une base de données. Que changez-vous ?

Passer le nom d'hôte et les autres valeurs identifiantes en secrets d'environnement pour qu'ils soient masqués, renouveler les identifiants si quelque chose de sensible est apparu, relire les journaux passés, et ajouter un contrôle empêchant d'afficher la configuration dans les journaux.

<!-- challenge -->

Les analystes sont sans cesse surpris par des changements de colonnes. Quel processus léger introduisez-vous ?

<!-- solution -->

Générer un changelog depuis les conventional commits à chaque release, le publier dans le catalogue de données et sur un canal suivi par les analystes, et annoncer les changements cassants avec une période de dépréciation avant retrait.

<!-- takeaways -->

- Changelogs et notes traduisent les changements pour les consommateurs.
- Les dépréciations exigent dates et alternatives.
- Mesurez vitesse et stabilité de la livraison.

<!-- unit: Une CI rapide et économique -->

<!-- goals -->

- Garder une CI rapide quand un projet grandit.
- Maîtriser les coûts de CI sans supprimer de vérifications.

<!-- concept -->

La CI ne fonctionne que si on l'utilise. Quand elle est trop lente, les développeurs regroupent les changements, sautent des vérifications ou fusionnent en la contournant, et le filet de sécurité disparaît. La vitesse vient de moins de travail par exécution : seulement ce qui a changé, en parallèle, avec dépendances en cache.
Les mêmes gestes baissent le coût, avec l'annulation des exécutions dépassées et des jobs lourds réservés aux merges ou aux planifications.

<!-- example -->

```yaml
concurrency: {group: "ci-${{ github.ref }}", cancel-in-progress: true}
jobs:
  unit:   {runs-on: ubuntu-24.04, steps: [...]}        # every PR
  dbt:    {if: "contains(needs.changes.outputs.paths, 'models')", ...}
  e2e:    {if: "github.event_name == 'schedule'", ...}  # nightly only
```

#### Comment passer de déploiements manuels à la CI/CD ?

Tout mettre dans Git (code, configuration, infrastructure), ajouter une CI avec linting et tests sur les pull requests, automatiser le déploiement vers un environnement de staging, ajouter tests de fumée et approbations, puis automatiser le déploiement en production avec les mêmes artefacts, et retirer progressivement l'accès manuel à la production.

#### Comment expliquer la CI/CD des données à un interlocuteur non technique ?

C'est une chaîne automatique de contrôle qualité et de livraison pour nos pipelines de données : chaque changement est testé avant de pouvoir toucher les rapports, et les changements approuvés arrivent en production toujours de la même façon sûre, pour que les chiffres restent fiables pendant que nous les améliorons rapidement.

#### Comment ajouter des barrières de qualité des données à un pipeline de CI/CD existant ?

Ajouter des tests de données au projet de transformation (unicité, non-nullité, relations, valeurs acceptées), les lancer en CI sur des données de test et en production après chaque construction, bloquer la publication (write-audit-publish ou échec du job) en cas d'échec critique, et alerter les responsables.

<!-- challenge -->

Les coûts de CI ont doublé avec la croissance de l'équipe. La plupart des minutes viennent d'exécutions sur des commits repoussés quelques minutes plus tard. Que changez-vous d'abord ?

<!-- solution -->

Ajouter un groupe `concurrency` par branche avec `cancel-in-progress: true`, pour que chaque nouveau push annule l'exécution périmée. Puis mettre les dépendances en cache et ne lancer les suites lourdes que si les chemins concernés changent.

<!-- takeaways -->

- Une CI lente est contournée ; la vitesse, c'est la sécurité.
- N'exécutez que ce qui a changé, en parallèle, avec cache.
- Annulez les exécutions dépassées pour économiser.

<!-- stage: Tout assembler -->

### Mises en situation

<!-- unit: Se remettre d'un mauvais déploiement -->

<!-- goals -->

- Restaurer une table de production après un mauvais déploiement.
- Identifier les failles du processus qui ont laissé passer le changement.

<!-- concept -->

Les questions d'incident testent deux choses : rétablir le service calmement, et en tirer des leçons. La reprise d'abord : annuler le code, restaurer ou recalculer les données, prévenir les consommateurs. Ensuite la revue examine le pipeline : quel test, quelle revue ou quelle barrière aurait dû arrêter cela, et comment l'ajouter. Les revues sans reproche portent sur le système, pas sur la personne.

<!-- example -->

```text
1. Stop the bleeding: pause downstream jobs, notify consumers
2. Roll back code (previous artifact); restore table (time travel) or rerun old logic
3. Verify: row counts, key metrics vs before the deploy
4. Review: missing regression test? missing data test? review skipped?
5. Add the check to CI; document in the postmortem
```

#### Deux équipes déploient dans le même workspace Databricks et écrasent mutuellement leurs jobs. Comment corriger ?

Utiliser des bundles aux noms et cibles distincts par équipe, déployer sous le service principal de chaque équipe avec des droits limités à ses ressources, utiliser le mode développement pour les déploiements personnels, et séparer les déploiements de production par dépôt et protections d'environnement.

<!-- challenge -->

Le postmortem montre que le bug aurait été détecté en comparant les sorties avant et après le changement. Comment intégrer cette comparaison à chaque PR concernée ?

<!-- solution -->

Ajouter à la CI une étape de régression pour les modèles modifiés : les construire dans le schéma de la PR sur les mêmes entrées et comparer agrégats clés et nombres de lignes à la production, publier le résultat en commentaire de PR et échouer sur les écarts inattendus.

<!-- takeaways -->

- Rétablir d'abord : code, données, communication.
- Cherchez la barrière manquante, pas un coupable.
- Transformez chaque leçon en vérification automatique.

<!-- unit: Passer d'une livraison manuelle à automatisée -->

<!-- goals -->

- Planifier la migration de déploiements manuels vers le CI/CD.
- Ordonner les étapes pour que la valeur arrive tôt.

<!-- concept -->

Les équipes passent rarement des déploiements manuels au CI/CD complet en une étape, et elles ne devraient pas essayer. Le chemin est progressif : d'abord tout mettre dans Git, puis ajouter des vérifications à chaque changement, puis automatiser le déploiement vers un environnement hors production, et enfin vers la production avec approbations. Chaque étape rapporte par elle-même et crée la confiance pour la suivante.

<!-- example -->

| Étape | Résultat |
|---|---|
| 1. Tout dans Git | Historique, revues, aucun script perdu |
| 2. CI : lint + tests unitaires | Moins de changements cassés |
| 3. Déploiement automatique en staging | Déploiements reproductibles |
| 4. Déploiement en prod avec approbation | Plus de copie manuelle, piste d'audit |
| 5. Tests de données et supervision | Problèmes détectés avant les utilisateurs |

#### Un `terraform apply` en CI a supprimé une ressource de production. Comment éviter que cela se reproduise ?

Exiger la revue du plan avant l'apply, ajouter des règles de cycle de vie `prevent_destroy` sur les ressources critiques, lancer des contrôles de politiques qui bloquent la suppression des ressources protégées, séparer état et droits par environnement, et, dans l'immédiat, restaurer depuis les sauvegardes ou réimporter la ressource.

<!-- challenge -->

Certains ingénieurs craignent que l'automatisation les ralentisse. Comment montrer de la valeur dès les deux premières semaines ?

<!-- solution -->

Commencer par ce qui leur coûte du temps aujourd'hui : mettre les scripts dans Git avec une CI de base qui lance linting et quelques tests en quelques minutes, et automatiser un déploiement pénible. Montrer le temps gagné et le premier bug détecté par la CI.

<!-- takeaways -->

- Migrez par étapes : Git, CI, déploiements staging, puis prod.
- Chaque étape doit rapporter par elle-même.
- Montrez des gains rapides pour créer la confiance.
