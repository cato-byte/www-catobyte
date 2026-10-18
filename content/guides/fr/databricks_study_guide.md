## Fiche d'étude Databricks

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude Databricks : environ 200 questions](../../images/databricks_study_guide_title_img.png)

Environ 200 questions d'entretien sur Databricks, de l'idée du lakehouse à Delta Lake, Unity Catalog, l'ingestion, les pipelines et jobs Lakeflow, l'optimisation des performances, la sécurité et les coûts. Les réponses décrivent la plateforme telle qu'elle est en 2026 ; Databricks renomme souvent ses produits, les anciens noms sont donc indiqués quand ils restent courants.

La fiche suit un parcours d'apprentissage en six étapes. Chaque section est découpée en unités courtes : objectifs d'apprentissage, explication du concept et exemple commenté, puis questions (d'abord de mémorisation, ensuite d'application), un exercice pratique et les points à retenir. Pour **apprendre**, lisez chaque unité du début à la fin. Pour **réviser**, passez en mode révision ou utilisez « Aller aux questions », marquez les réponses à revoir et essayez une révision mixte entre les sections.

<!-- QA -->
<!-- stage: Fondamentaux -->

### Fondamentaux de la plateforme

<!-- unit: L'idée du lakehouse -->

<!-- goals -->

- Expliquer ce qu'est un lakehouse et quels problèmes du data lake il résout.
- Situer les familles de produits Databricks (Lakeflow, Mosaic AI) dans ce schéma.

<!-- concept -->

Les entreprises gardaient deux copies : un data lake bon marché pour la data science et un entrepôt coûteux pour la BI. Le lake n'avait ni transactions, ni schémas, ni mises à jour simples ; l'entrepôt enfermait les données dans un format propriétaire. Un lakehouse garde une seule copie en formats ouverts sur du stockage objet et y ajoute les fonctions d'un entrepôt : Delta Lake apporte les transactions, Unity Catalog la gouvernance, Spark, Photon et les SQL warehouses la vitesse.

Databricks vend cette plateforme, en familles : Lakeflow pour l'ingénierie, Databricks SQL pour l'analytique et Mosaic AI pour le ML.

<!-- example -->

| Besoin | Lake classique | Entrepôt | Lakehouse |
|---|---|---|---|
| Stockage bon marché, format ouvert | Oui | Non | Oui |
| Transactions ACID, `UPDATE`/`DELETE` | Non | Oui | Oui (Delta) |
| Permissions fines | Faibles | Oui | Oui (Unity Catalog) |
| Une seule copie pour la BI et le ML | Non | Non | Oui |

#### Qu'est-ce que Databricks ?

Une plateforme cloud de données et d'IA, fondée par les créateurs d'Apache Spark, disponible sur AWS, Azure et Google Cloud. Elle réunit ingénierie des données, analytique SQL, streaming, machine learning et gouvernance sur une seule copie des données, stockée dans des formats ouverts (Delta Lake, Apache Iceberg) dans votre propre stockage cloud.

#### Qu'est-ce qu'un lakehouse ?

Une architecture qui stocke les données dans un stockage objet bon marché, comme un data lake, mais y ajoute des fonctions d'entrepôt de données : transactions ACID, schémas, optimisations proches de l'indexation, gouvernance fine et SQL rapide. Elle évite de garder une copie des données dans un lake pour la data science et une autre dans un entrepôt pour la BI.

#### Quels problèmes du data lake classique le lakehouse résout-il ?

Les data lakes n'avaient pas de transactions (les lecteurs voyaient des données à moitié écrites), pas de contrôle de schéma (les données inutilisables s'accumulaient), des requêtes lentes sur de nombreux petits fichiers, pas de mises à jour ni de suppressions faciles (un problème pour le RGPD) et une gouvernance faible. Delta Lake et Unity Catalog traitent chacun de ces points.

#### Qu'est-ce que Lakeflow ?

Le nom générique, depuis 2025, des produits d'ingénierie des données de Databricks : Lakeflow Connect (connecteurs d'ingestion gérés), Lakeflow Declarative Pipelines (anciennement Delta Live Tables) et Lakeflow Jobs (anciennement Workflows).

#### Qu'est-ce que Mosaic AI ?

L'ensemble des fonctions d'IA et de ML de Databricks : entraînement et fine-tuning de modèles, Model Serving, Vector Search, AI Gateway, frameworks et évaluation d'agents, le tout gouverné par Unity Catalog.

#### Comment expliquer le lakehouse à un interlocuteur métier ?

Un seul endroit pour toutes les données de l'entreprise, stockées une seule fois dans des formats ouverts dans le propre compte cloud de l'entreprise, où le reporting, la data science et l'IA travaillent sur les mêmes chiffres fiables, avec des droits et des traces d'audit gérés de façon centralisée.

<!-- challenge -->

Votre responsable demande pourquoi l'équipe devrait cesser d'exporter chaque nuit des CSV du lake vers un entrepôt séparé. Écrivez-lui trois phrases : ce qui change, ce qu'on y gagne et un risque.

<!-- solution -->

Rapports et modèles liraient les mêmes tables Delta : la copie nocturne et ses délais disparaissent. Les chiffres concordent entre BI et data science, et permissions et audit sont au même endroit. Le risque est l'effort de migration : il faut rebrancher et valider les rapports avant d'éteindre l'ancien entrepôt.

<!-- takeaways -->

- Un lakehouse, c'est une copie des données en formats ouverts avec les fonctions d'un entrepôt.
- Delta Lake règle transactions et schémas ; Unity Catalog, la gouvernance.
- Lakeflow (ingénierie), Databricks SQL (analytique) et Mosaic AI (ML) sont les familles de produits.

<!-- unit: Plan de contrôle, workspaces et facturation -->

<!-- goals -->

- Dire où Databricks exécute votre code et où restent vos données.
- Expliquer pourquoi les DBU rendent le calcul de jobs moins cher que l'all-purpose.

<!-- concept -->

Databricks se divise en deux plans. Le plan de contrôle, dans le compte Databricks, héberge l'application web, les notebooks, l'ordonnanceur et les métadonnées. Le plan de calcul traite les données : dans votre compte cloud pour les clusters classiques, dans celui de Databricks pour le serverless. Les données au repos restent toujours dans votre stockage.

Le traitement est facturé en DBU à la seconde, à un tarif qui dépend du type de calcul : les clusters all-purpose interactifs coûtent plus que le calcul de jobs, qui ne vit que le temps d'une exécution.

<!-- example -->

```text
 Control plane (Databricks)        Compute plane
 ┌──────────────────────────┐      ┌─────────────────────────────┐
 │ web app, notebooks, jobs │ ───► │ classic: VMs in YOUR account│
 │ scheduler, UC metadata   │      │ serverless: Databricks acct │
 └──────────────────────────┘      └──────────────┬──────────────┘
                                                  ▼
                                   your S3 / ADLS / GCS storage
```

#### Quelle est la différence entre le plan de contrôle et le plan de calcul ?

Le plan de contrôle est géré par Databricks dans son propre compte : l'application web, les notebooks, l'ordonnanceur de jobs, le gestionnaire de clusters et les métadonnées d'Unity Catalog. Le plan de calcul est l'endroit où les données sont traitées. Avec le calcul classique, il tourne dans votre compte cloud (votre VPC) ; avec le calcul serverless, il tourne dans le compte de Databricks, dans la même région. Dans les deux cas, les données au repos restent dans votre stockage.

#### Qu'est-ce qu'un workspace Databricks ?

L'environnement où travaillent les utilisateurs : notebooks, fichiers, dossiers Git, jobs, pipelines, requêtes SQL, dashboards, clusters et expériences. Une entreprise a généralement plusieurs workspaces (par exemple dev, staging et prod), rattachés à un metastore Unity Catalog par région.

#### Qu'est-ce qu'un DBU ?

Une Databricks Unit, l'unité de capacité de traitement que Databricks facture à la seconde. Le tarif du DBU dépend du type de calcul (jobs, all-purpose, SQL, serverless) et de l'offre. Avec le calcul classique, vous payez aussi les machines virtuelles au fournisseur cloud ; en serverless, le prix du DBU inclut l'infrastructure.

#### Pourquoi le calcul de jobs est-il moins cher que le calcul all-purpose ?

Le calcul de jobs est facturé à un tarif de DBU plus bas, car il exécute des traitements planifiés et non interactifs et s'arrête à la fin du job. Les clusters all-purpose servent au développement interactif, sont partagés et restent allumés longtemps, donc Databricks les facture plus cher. Faire tourner la production sur des clusters all-purpose est une erreur de coût classique.

<!-- challenge -->

Un job de production nocturne tourne sur le cluster all-purpose partagé de l'équipe et dure une heure. Citez deux changements qui réduisent son coût sans toucher au code.

<!-- solution -->

L'exécuter sur du calcul de jobs (ou des jobs serverless) au lieu du cluster all-purpose : le tarif DBU baisse et la facturation s'arrête avec l'exécution. Puis dimensionner le cluster du job (ou utiliser des workers spot) d'après ses métriques.

<!-- takeaways -->

- Le plan de contrôle appartient à Databricks ; les données au repos restent dans votre stockage.
- Les DBU sont facturés à la seconde, à un tarif qui dépend du type de calcul.
- La production va sur du calcul de jobs ou serverless, pas sur des clusters all-purpose.

<!-- unit: Travailler dans le workspace -->

<!-- goals -->

- Utiliser notebooks, widgets et `dbutils` au quotidien.
- Expliquer pourquoi les dossiers Git et les volumes remplacent d'anciennes pratiques.

<!-- concept -->

L'essentiel du développement se fait dans des notebooks : des cellules Python, SQL, Scala ou R exécutées sur le calcul attaché. Les widgets transforment un notebook en tâche de job paramétrée, et `dbutils` donne accès aux fichiers, secrets, paramètres et valeurs de tâches.

Deux vieilles habitudes disparaissent. Le code doit vivre dans des dossiers Git, relu et versionné comme tout dépôt. Les fichiers doivent vivre dans des volumes Unity Catalog plutôt que dans DBFS, dont les chemins n'ont pas de permissions fines.

<!-- example -->

Un notebook qui fonctionne en interactif comme en tâche planifiée :
```python
dbutils.widgets.text("snapshot_date", "2026-10-01")    # default for interactive runs
snapshot = dbutils.widgets.get("snapshot_date")          # the job overrides it
df = spark.read.json(f"/Volumes/raw/landing/orders/{snapshot}/")
```

#### Quels langages peut-on utiliser dans Databricks ?

Python, SQL, Scala et R dans les notebooks, ainsi que Java et Scala dans les jobs JAR. On peut mélanger les langages dans un notebook avec les commandes magiques `%sql`, `%python`, `%scala`, `%md` (Markdown) et `%sh` (shell sur le driver).

#### Qu'est-ce qu'un notebook Databricks ?

Un document web composé de cellules qui exécutent du code sur le calcul attaché, avec résultats, graphiques, commentaires, historique des versions et coédition en temps réel. Les notebooks peuvent être planifiés comme tâches d'un job, paramétrés avec des widgets et stockés comme fichiers source dans Git.

#### Que sont les widgets ?

Les paramètres d'entrée des notebooks (texte, liste déroulante, combobox, sélection multiple). Dans les jobs, les paramètres de la tâche les remplissent. En SQL, on référence les paramètres avec la syntaxe `:nom`.

```python
dbutils.widgets.text("snapshot_date", "2026-10-01")
snapshot = dbutils.widgets.get("snapshot_date")
```

#### Qu'est-ce que `dbutils` ?

Une bibliothèque d'utilitaires disponible dans les notebooks et les jobs : `dbutils.fs` pour les fichiers, `dbutils.secrets` pour les secrets, `dbutils.widgets` pour les paramètres, `dbutils.notebook.run` et `dbutils.notebook.exit` pour enchaîner des notebooks, et `dbutils.jobs.taskValues` pour passer de petites valeurs entre les tâches d'un job.

#### Que sont les dossiers Git (anciennement Repos) ?

Des dossiers du workspace liés à un dépôt Git (GitHub, GitLab, Azure DevOps, Bitbucket). Ils permettent de cloner, créer des branches, faire des commits, pull et push depuis le workspace, pour que les notebooks et fichiers Python soient versionnés et relus comme n'importe quel code.

#### Qu'est-ce que DBFS, et pourquoi est-il déconseillé aujourd'hui ?

Le Databricks File System, une abstraction historique qui montait le stockage cloud sous des chemins `dbfs:/`, y compris un bucket racine du workspace. Il n'offre pas de gouvernance fine : Databricks recommande désormais les volumes Unity Catalog pour les fichiers et les tables pour les données, et désactive la racine DBFS et les montages dans les nouvelles installations.

<!-- challenge -->

Un collègue garde des identifiants dans une cellule de notebook et lit des fichiers depuis `dbfs:/mnt/raw`. Quels deux changements proposez-vous ?

<!-- solution -->

Déplacer les identifiants dans un secret scope lu avec `dbutils.secrets.get` (ou mieux, une storage credential pour ne plus avoir de secret) et remplacer le mount par un chemin de volume Unity Catalog sous `/Volumes/...`, afin que l'accès soit gouverné et audité.

<!-- takeaways -->

- Les widgets rendent un même notebook utilisable en interactif et en tâche de job.
- Le code va dans des dossiers Git, les fichiers dans des volumes, pas dans DBFS.
- `dbutils` couvre fichiers, secrets, widgets et valeurs de tâches.

<!-- unit: Runtime, Photon et développement à distance -->

<!-- goals -->

- Décrire le contenu d'un Databricks Runtime et ce qu'accélère Photon.
- Expliquer pourquoi Spark Connect limite certaines API et comment développer depuis un IDE.

<!-- concept -->

Chaque cluster exécute un Databricks Runtime : Spark plus Delta, des connecteurs et des optimisations, en versions LTS que l'on peut figer. Photon, un moteur vectorisé en C++, accélère en dessous le travail SQL et DataFrame.

Le calcul récent parle à Spark via Spark Connect : le client envoie un plan logique à un serveur distant. Cela rend possibles le serverless et le développement depuis un IDE (Databricks Connect, la CLI), mais le code qui touche la JVM, les RDD ou `SparkContext` n'y fonctionne plus.

<!-- example -->

```python
# Works everywhere, including serverless (plain DataFrame API):
df.groupBy("country").count()

# Fails on Spark Connect (serverless, standard access mode):
spark.sparkContext.parallelize([1, 2, 3])
```

#### Qu'est-ce que le Databricks Runtime ?

L'image logicielle versionnée qu'exécutent les clusters : Apache Spark plus Delta Lake, Photon, des bibliothèques, des connecteurs et des améliorations de performance. Les versions LTS (support à long terme) sont maintenues environ trois ans. Le runtime ML ajoute des bibliothèques de machine learning.

#### Qu'est-ce que Photon ?

Un moteur de requêtes vectorisé écrit en C++ qui exécute nativement les opérations Spark SQL et DataFrame, au lieu de les exécuter dans la JVM. Il accélère les lectures, jointures, agrégations et écritures, surtout sur Delta et Parquet. Il est activé par défaut sur les SQL warehouses et en serverless, et optionnel (à un tarif de DBU plus élevé) sur les clusters.

#### Qu'est-ce que Spark Connect, et pourquoi est-ce important sur Databricks ?

Un protocole client-serveur où le client construit un plan logique non résolu et l'envoie à un serveur Spark distant. Le calcul serverless et les clusters partagés (mode d'accès standard) l'utilisent : le code qui touche directement le `SparkContext`, les RDD ou la JVM n'y fonctionne pas. Le code DataFrame et SQL fonctionne sans changement.

#### Qu'est-ce que la CLI Databricks ?

Un outil en ligne de commande pour gérer les workspaces depuis un terminal ou la CI : fichiers, jobs, clusters, secrets, objets Unity Catalog et surtout les Databricks Asset Bundles (`databricks bundle validate|deploy|run`). Elle s'authentifie en OAuth (utilisateur ou service principal) ou avec des jetons.

#### Qu'est-ce que Databricks Connect ?

Une bibliothèque qui permet d'exécuter du code Spark depuis votre IDE ou un processus Python local sur le calcul Databricks, via Spark Connect. Vous développez et déboguez en local pendant que les opérations DataFrame s'exécutent sur le cluster ou en serverless.

<!-- challenge -->

Vous voulez déboguer pas à pas une transformation dans votre IDE pendant que les données restent dans Databricks. Que mettez-vous en place ?

<!-- solution -->

Installer Databricks Connect correspondant au runtime du cluster (ou utiliser le serverless), s'authentifier avec la CLI (`databricks auth login`) et exécuter le code en local : les opérations DataFrame s'exécutent à distance via Spark Connect, le Python dans votre débogueur.

<!-- takeaways -->

- Le runtime est l'image versionnée : figez une LTS en production.
- Photon accélère SQL et DataFrames, pas les UDF Python.
- Spark Connect permet le serverless et l'IDE mais interdit RDD et accès JVM.

### Calcul

<!-- unit: Types de calcul et serverless -->

<!-- goals -->

- Choisir entre calcul all-purpose, de jobs, SQL warehouse et serverless.
- Expliquer ce à quoi on renonce avec le serverless.

<!-- concept -->

Databricks adapte le calcul à la charge. Les clusters all-purpose servent le développement interactif, le calcul de jobs vit le temps d'une exécution et les SQL warehouses servent le SQL et la BI. Leurs versions serverless démarrent en secondes et ne facturent que pendant le travail.

Le serverless échange contrôle contre confort : pas de choix d'instances ni de la plupart des réglages Spark, et le code doit être compatible Spark Connect. Un SQL warehouse se dimensionne autrement : la taille fixe la vitesse d'une requête, le nombre de clusters la concurrence.

<!-- example -->

| Charge | Bon choix |
|---|---|
| Explorer des données dans un notebook | All-purpose (avec auto-terminaison) ou notebook serverless |
| Job ETL nocturne | Calcul de jobs ou jobs serverless |
| Tableaux de bord et outils de BI | SQL warehouse serverless |
| Bibliothèque qui a besoin de la JVM | Cluster classique, mode d'accès dédié |

#### Quels types de calcul Databricks propose-t-il ?

Des clusters all-purpose pour le travail interactif, du calcul de jobs créé pour une exécution, des SQL warehouses pour le SQL et la BI, du calcul serverless pour les notebooks, jobs et pipelines, et des instance pools pour accélérer le démarrage des clusters classiques.

#### Qu'est-ce que le calcul serverless ?

Du calcul que Databricks provisionne et gère dans son propre compte : il démarre en quelques secondes, s'adapte automatiquement, utilise toujours un runtime récent avec Photon et n'est facturé que pendant qu'il travaille. Vous renoncez au choix des types d'instance et aux réglages Spark, et le code doit être compatible avec Spark Connect.

#### Qu'est-ce qu'un SQL warehouse ?

Du calcul dédié aux requêtes SQL de Databricks SQL, des outils de BI et des dashboards. Types : serverless (démarrage rapide, recommandé), pro et classic. Il monte en charge en ajoutant des clusters pour absorber la concurrence et utilise Photon et une gestion intelligente de la charge.

#### Comment dimensionner un SQL warehouse ?

Choisissez une taille (T-shirt size) selon la complexité des requêtes et le volume de données (plus grand signifie des requêtes individuelles plus rapides), et fixez le nombre maximal de clusters pour la concurrence (plus d'utilisateurs simultanés). Surveillez la mise en file d'attente et le spill dans l'historique des requêtes, et configurez l'arrêt automatique.

#### Un notebook fonctionne sur votre cluster mais échoue en job serverless. Pourquoi ?

Probablement parce qu'il utilise quelque chose qui n'est pas pris en charge en serverless (Spark Connect) : RDD, `sparkContext`, `cache()`, la plupart des appels à `spark.conf.set`, des init scripts ou des bibliothèques qui ont besoin de la JVM. Réécrivez avec les API DataFrame, déclarez les dépendances dans l'environnement et testez en serverless avant de déployer.

<!-- challenge -->

Le lundi matin, un tableau de bord est lent car 40 analystes l'ouvrent en même temps ; chaque requête seule est rapide. Quel réglage du warehouse changez-vous ?

<!-- solution -->

Augmenter le nombre maximal de clusters (passage à l'échelle horizontal pour la concurrence), pas la taille, car les requêtes seules sont déjà rapides. Vérifiez la mise en file dans l'historique des requêtes.

<!-- takeaways -->

- Adaptez le calcul à la charge : interactive, planifiée ou SQL.
- Le serverless démarre vite et facture à l'usage, mais exige du code compatible Spark Connect.
- Taille du warehouse = vitesse par requête ; nombre de clusters = concurrence.

<!-- unit: Clusters classiques et modes d'accès -->

<!-- goals -->

- Décrire le driver et les workers d'un cluster classique.
- Choisir le mode d'accès standard ou dédié pour une charge.

<!-- concept -->

Un cluster classique a un driver, qui exécute votre programme et planifie le travail, et des workers dont les executors traitent les partitions en parallèle. Un cluster mono-nœud met tout sur le driver, suffisant pour de petites données ou du pandas.

Le mode d'accès décide du partage. Le mode standard permet à plusieurs utilisateurs de le partager en sécurité sous Unity Catalog, au prix des restrictions de Spark Connect. Le mode dédié appartient à un utilisateur ou un groupe et accepte plus d'API, ce qu'exigent certaines bibliothèques de ML et le travail sur GPU.

<!-- example -->

```text
 driver  ── plans stages, collects results (keep big data off it)
   ├── worker 1: executor ── tasks on partitions 1..n
   ├── worker 2: executor ── tasks on partitions n+1..m
   └── worker 3: executor ── ...
```

#### Comment est composé un cluster classique ?

D'un nœud driver qui exécute le programme principal, planifie le travail et collecte les résultats, et de nœuds workers dont les executors traitent les partitions. Un cluster à nœud unique exécute tout sur le driver, ce qui suffit pour de petites données et du ML sur une seule machine.

#### À quoi sert un cluster à nœud unique ?

Au traitement de petites données, au travail avec pandas et scikit-learn et au développement léger. Il n'a pas de workers : Spark tourne en mode local sur le driver, ce qui est peu coûteux mais ne passe pas à l'échelle.

#### Que sont les modes d'accès ?

Des réglages qui contrôlent l'isolation et la gouvernance sur le calcul classique. Le mode standard (anciennement shared) permet à plusieurs utilisateurs de partager un cluster avec l'isolation d'Unity Catalog, via Spark Connect. Le mode dédié (anciennement single user) attribue le cluster à un utilisateur ou un groupe et prend en charge plus d'API, comme les RDD et certaines bibliothèques de ML.

#### Qu'implique le choix entre mode standard et dédié pour le ML ?

Les bibliothèques de ML qui ont besoin d'un accès direct à la JVM ou au `SparkContext`, ou l'entraînement sur GPU, exigent généralement le mode d'accès dédié ou le serverless avec le bon environnement. Le mode standard convient mieux au travail partagé en SQL et DataFrame.

#### À quoi servent les clusters GPU ?

À l'entraînement et à l'inférence de deep learning, et à certaines bibliothèques accélérées par GPU. Ils nécessitent un runtime ML avec les pilotes GPU et coûtent cher, ils doivent donc s'arrêter rapidement.

<!-- challenge -->

Le script d'entraînement d'une data scientist appelle `spark.sparkContext` et échoue sur le cluster partagé de l'équipe. Que proposez-vous ?

<!-- solution -->

Lui donner un cluster dédié (utilisateur unique), ou un environnement serverless qui prend en charge sa bibliothèque, pour l'entraînement. Le cluster partagé en mode standard reste pour le SQL et les DataFrames.

<!-- takeaways -->

- Le driver planifie et collecte ; les workers traitent.
- Le mode standard sert au partage sous Unity Catalog ; le dédié accepte plus d'API.
- Les clusters mono-nœud sont économiques ; les clusters GPU doivent s'arrêter vite.

<!-- unit: Passage à l'échelle et maîtrise des coûts -->

<!-- goals -->

- Configurer avec discernement autoscaling, auto-terminaison, pools et instances spot.
- Utiliser des politiques de cluster pour encadrer le calcul d'une équipe.

<!-- concept -->

L'essentiel de l'argent gaspillé vient de clusters trop gros ou qui ne s'arrêtent jamais. L'autoscaling ajoute et retire des workers selon la charge, l'auto-terminaison arrête les clusters inactifs et les pools gardent des VM prêtes pour démarrer plus vite. Les instances spot réduisent fortement le coût des workers tolérants aux pannes, tant que le driver reste à la demande.

Les politiques de cluster en font des valeurs par défaut : les administrateurs limitent types et tailles, imposent l'auto-terminaison et exigent des tags de coût.

<!-- example -->

Un extrait de politique que tout cluster de développement doit respecter :
```json
{
  "autotermination_minutes": {"type": "range", "maxValue": 30, "defaultValue": 20},
  "num_workers": {"type": "range", "maxValue": 4},
  "custom_tags.team": {"type": "fixed", "value": "data-eng"}
}
```

#### Comment fonctionne l'autoscaling ?

Vous fixez un nombre minimal et maximal de workers ; Databricks ajoute des workers quand des tâches attendent et en retire quand ils sont inactifs. L'autoscaling convient aux charges interactives et variables ; les clusters de taille fixe peuvent être plus prévisibles pour des jobs batch réguliers. Les charges de streaming devraient utiliser l'autoscaling amélioré des pipelines.

#### Qu'est-ce que l'arrêt automatique ?

Un réglage qui éteint un cluster all-purpose inactif après un certain nombre de minutes. Le laisser désactivé est l'une des causes les plus fréquentes de dépenses inutiles.

#### Que sont les instance pools ?

Un ensemble de machines virtuelles inactives et prêtes à l'emploi dans lequel les clusters puisent, pour réduire le démarrage de plusieurs minutes à quelques secondes. Les instances inactives d'un pool coûtent chez le fournisseur cloud, mais pas en DBU.

#### Faut-il utiliser des instances spot ?

Pour les workers des jobs batch tolérants aux pannes, oui : elles sont beaucoup moins chères et Spark relance les tâches si une instance est reprise. Gardez le driver à la demande, car le perdre fait échouer le job, et autorisez un repli vers des instances à la demande.

#### Que sont les politiques de cluster ?

Des règles définies par les administrateurs qui encadrent la création de clusters : types d'instance autorisés, taille maximale, tags obligatoires, arrêt automatique, versions du runtime. Elles maîtrisent les coûts et standardisent les configurations.

#### Comment réduire le coût du développement pour une équipe de dix ingénieurs ?

Avec des clusters petits ou à nœud unique, encadrés par des politiques et un arrêt automatique court, des notebooks serverless, des échantillons de données de développement partagés ou des shallow clones plutôt que des copies complètes, des tests unitaires locaux pour l'essentiel de la logique, des bundles en mode développement et une alerte budgétaire par équipe.

<!-- challenge -->

Les dépenses de développement d'une équipe ont doublé après l'arrivée de cinq ingénieurs. Citez trois contrôles à mettre en place cette semaine.

<!-- solution -->

Une politique de cluster avec de petites tailles maximales et une auto-terminaison de 20 à 30 minutes, des notebooks serverless ou un pool partagé pour démarrer vite, et une alerte budgétaire sur le tag de coût de l'équipe. À plus long terme, des tests unitaires locaux.

<!-- takeaways -->

- Les clusters inactifs ou surdimensionnés sont le principal gaspillage ; l'auto-terminaison règle le premier.
- Spot pour les workers, à la demande pour le driver.
- Les politiques font des bons réglages la norme.

<!-- unit: Bibliothèques et dépannage -->

<!-- goals -->

- Installer des dépendances de façon reproductible sur clusters et serverless.
- Trouver la cause d'un cluster lent ou en échec.

<!-- concept -->

Les dépendances peuvent être attachées au cluster, installées par notebook avec `%pip` ou déclarées par tâche de job ; le serverless utilise une spécification d'environnement. Figez les versions pour qu'une relance le mois suivant se comporte pareil. Les init scripts s'exécutent au démarrage pour la configuration système, mais ralentissent le démarrage et sont difficiles à déboguer.

En cas de panne, le driver est le suspect habituel des plantages (il manque de mémoire quand on y rapatrie des données), et la Spark UI est l'endroit où chercher la lenteur : durée des stages, tâches déséquilibrées, taille des shuffles et spill.

<!-- example -->

```python
# Pulls 50 million rows into driver memory: likely out-of-memory
pdf = spark.table("silver.events").toPandas()

# Keeps the work distributed and the result small
spark.table("silver.events").groupBy("event_date").count().toPandas()
```

#### Comment installer des bibliothèques sur un cluster ?

Comme bibliothèques du calcul (PyPI, Maven, wheels depuis des volumes ou des fichiers du workspace), au niveau du notebook avec `%pip install`, ou comme dépendances d'une tâche de job. En serverless, on déclare les dépendances dans la configuration de l'environnement. Figez les versions pour la reproductibilité.

#### Que sont les init scripts ?

Des scripts shell exécutés sur chaque nœud au démarrage, pour installer des paquets système ou configurer l'environnement. Ils doivent être stockés dans des volumes ou des fichiers du workspace, pas dans DBFS, et rester minimes car ils ralentissent le démarrage et compliquent le débogage.

#### Que se passe-t-il quand le driver manque de mémoire ?

Le notebook ou le job échoue ou redémarre. Causes fréquentes : `collect()` ou `toPandas()` sur de gros volumes, broadcast d'une table trop grande, gros objets Python sur le driver, ou trop de tâches suivies en même temps. Gardez les données dans Spark, écrivez les résultats dans des tables et dimensionnez correctement le driver.

#### Où regarder quand un cluster est lent ?

Dans la Spark UI (jobs, stages, durée des tâches, volumes de shuffle, spill, déséquilibre), les métriques du cluster (CPU, mémoire, disque), les journaux du driver et le profil de requête pour le SQL. Comparez la médiane et le maximum des durées de tâches d'un stage pour repérer le déséquilibre (skew).

<!-- challenge -->

Un job échoue tous les quelques jours avec « driver not responding ». La dernière cellule appelle `collect()` sur le résultat pour l'envoyer par e-mail. Que changez-vous ?

<!-- solution -->

Écrire le résultat dans une table (ou un fichier dans un volume) et envoyer un lien ou un petit résumé au lieu de collecter toutes les lignes. Si un résumé est nécessaire, l'agréger d'abord dans Spark pour que seules quelques lignes atteignent le driver.

<!-- takeaways -->

- Figez les versions des bibliothèques ; limitez les init scripts.
- `collect()` et `toPandas()` sur de gros volumes sont les tueurs habituels du driver.
- Comparez durée médiane et maximale des tâches dans la Spark UI.

### Delta Lake

<!-- unit: Journal de transactions et ACID -->

<!-- goals -->

- Expliquer comment un dossier de fichiers Parquet plus un journal devient une table transactionnelle.
- Distinguer tables managées et externes.

<!-- concept -->

Une table Delta, ce sont des fichiers Parquet plus un dossier `_delta_log/`. Chaque commit est un fichier JSON numéroté listant les fichiers ajoutés et retirés ; la table en version N est l'ensemble des fichiers valides après le commit N. Les écrivains écrivent d'abord leurs fichiers puis tentent de créer l'entrée suivante du journal, opération atomique : les lecteurs ne voient jamais de données à moitié écrites.

Il n'y a pas de verrous : la concurrence est optimiste et les conflits apparaissent au commit. Le propriétaire de l'emplacement décide si la table est managée ou externe.

<!-- example -->

```text
sales/
├── part-0001.parquet   added in v0
├── part-0002.parquet   added in v1
├── part-0003.parquet   added in v2 (replaces 0001)
└── _delta_log/
    ├── 00000000000000000000.json   add 0001
    ├── 00000000000000000001.json   add 0002
    └── 00000000000000000002.json   remove 0001, add 0003
Version 2 = {0002, 0003}
```

#### Qu'est-ce que Delta Lake ?

Un format de stockage open source qui ajoute un journal de transactions à des fichiers Parquet. Il apporte les transactions ACID, le contrôle et l'évolution du schéma, le voyage dans le temps, `MERGE`, `UPDATE` et `DELETE`, ainsi que les lectures et écritures en streaming. C'est le format de table par défaut sur Databricks.

#### Comment fonctionne le journal de transactions de Delta ?

Chaque table possède un dossier `_delta_log/` de fichiers JSON de commit ordonnés (`000…0.json`, `000…1.json`) qui listent les fichiers de données ajoutés et supprimés par chaque transaction, ainsi que les changements de schéma et de métadonnées. Régulièrement, un checkpoint Parquet résume l'état pour que les lecteurs n'aient pas à rejouer tous les commits. Une version de la table est l'ensemble des fichiers valides après un commit donné.

#### Comment Delta garantit-il les propriétés ACID sur un stockage objet ?

Les écrivains créent de nouveaux fichiers Parquet, puis tentent de valider en écrivant de façon atomique l'entrée numérotée suivante du journal. Si deux écrivains sont en concurrence, un seul réussit ; l'autre vérifie s'il y a conflit, puis réessaie ou échoue. Les lecteurs ne voient que les fichiers référencés par des entrées validées, donc jamais d'écriture partielle.

#### Quel contrôle de concurrence Delta utilise-t-il ?

Un contrôle de concurrence optimiste : les transactions ne verrouillent rien, elles vérifient au moment du commit si un commit concurrent a touché les mêmes données. Les ajouts entrent rarement en conflit ; des `UPDATE`/`MERGE` concurrents sur les mêmes fichiers peuvent lever `ConcurrentModificationException`. Le partitionnement, le liquid clustering et la concurrence au niveau ligne (avec les deletion vectors) réduisent les conflits.

#### Quelle est la différence entre une table gérée et une table externe ?

Les données d'une table gérée (managed) vivent dans un stockage contrôlé par Unity Catalog ; supprimer la table supprime les données (après une période de rétention), et Databricks peut l'optimiser automatiquement. Une table externe pointe vers un chemin que vous gérez dans votre propre emplacement de stockage ; la supprimer n'efface que les métadonnées.

#### Que montre `DESCRIBE DETAIL` ?

Le format, l'emplacement, le nombre de fichiers, la taille en octets, les colonnes de partitionnement ou de clustering et les propriétés de la table. C'est une vérification rapide du problème des petits fichiers.

#### Qu'est-ce que `CONVERT TO DELTA` ?

Une commande qui transforme sur place un répertoire Parquet existant en table Delta, en écrivant un journal de transactions au-dessus des fichiers existants, sans copier les données.

<!-- challenge -->

Deux jobs font un `MERGE` sur la même table en même temps et l'un échoue avec `ConcurrentModificationException`. Donnez deux façons de l'éviter.

<!-- solution -->

Sérialiser les écrivains (un seul job, ou une exécution concurrente maximum avec file), ou leur faire toucher des fichiers différents : regrouper ou partitionner selon la colonne qui sépare leurs données et l'inclure dans la condition du `MERGE`. Les deletion vectors permettent aussi une concurrence au niveau ligne.

<!-- takeaways -->

- Une version Delta est l'ensemble des fichiers listés par le journal jusqu'à ce commit.
- Le commit atomique du journal apporte l'ACID sur du stockage objet.
- La concurrence est optimiste : les conflits apparaissent au commit, pas sous forme de verrous.

<!-- unit: Schémas et contraintes -->

<!-- goals -->

- Expliquer l'application du schéma et comment autoriser délibérément son évolution.
- Utiliser contraintes, colonnes générées et identity, et propriétés de table.

<!-- concept -->

Delta rejette les écritures qui ne correspondent pas au schéma de la table : c'est l'enforcement, qui protège les lecteurs en aval. Quand le schéma doit changer, on l'autorise explicitement : `mergeSchema` sur une écriture, `ALTER TABLE` ou l'évolution de schéma dans `MERGE`.

Au-delà des types, les tables portent des règles et des métadonnées : contraintes `NOT NULL` et `CHECK` (appliquées), colonnes générées et identity, et propriétés qui activent des fonctions comme Change Data Feed. UniForm ajoute des métadonnées Iceberg pour que d'autres moteurs lisent les mêmes fichiers.

<!-- example -->

```sql
CREATE TABLE silver.orders (
  order_id   BIGINT GENERATED ALWAYS AS IDENTITY,
  ordered_at TIMESTAMP NOT NULL,
  order_date DATE GENERATED ALWAYS AS (CAST(ordered_at AS DATE)),
  amount     DECIMAL(18,2),
  CONSTRAINT positive_amount CHECK (amount >= 0)
) TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true');
```

#### Qu'est-ce que le contrôle de schéma (schema enforcement) ?

Delta rejette les écritures dont les colonnes ou les types ne correspondent pas au schéma de la table, au lieu de la corrompre silencieusement. Cela protège les consommateurs des chargements défectueux.

#### Comment fonctionne l'évolution du schéma dans Delta ?

Il faut l'autoriser explicitement : `.option("mergeSchema", "true")` sur une écriture ajoute les nouvelles colonnes, et `ALTER TABLE` modifie le schéma. Pour `MERGE`, `WITH SCHEMA EVOLUTION` (ou le réglage de merge automatique) permet d'ajouter de nouvelles colonnes de la source. Le type widening autorise certains changements de type, comme `int` vers `bigint`, sans réécrire les données.

#### Quelles contraintes Delta prend-il en charge ?

Les contraintes `NOT NULL` et `CHECK`, qui sont appliquées : une écriture qui les viole échoue. Les clés primaires et étrangères peuvent être déclarées dans Unity Catalog, mais elles sont informatives (non appliquées) et servent aux outils et à l'optimiseur.

#### Que sont les colonnes générées et les colonnes d'identité ?

Une colonne générée est calculée à partir d'autres colonnes (`GENERATED ALWAYS AS (CAST(ts AS DATE))`). Une colonne d'identité (`GENERATED ALWAYS AS IDENTITY`) attribue des nombres uniques et croissants (pas forcément consécutifs), utiles comme clés de substitution.

#### À quoi servent les propriétés de table dans Delta ?

Ce sont des réglages stockés avec la table, comme `delta.enableChangeDataFeed`, `delta.logRetentionDuration`, `delta.deletedFileRetentionDuration`, `delta.enableDeletionVectors` ou `delta.appendOnly`, ainsi que des métadonnées clé-valeur personnalisées. On les définit avec `TBLPROPERTIES` et on les affiche avec `SHOW TBLPROPERTIES`.

#### Qu'est-ce qu'UniForm ?

Universal Format : une option des tables Delta qui écrit aussi des métadonnées Iceberg (et Hudi), pour que les moteurs qui lisent Iceberg puissent lire les mêmes fichiers sans copier les données.

<!-- challenge -->

Une source ajoute une colonne `discount` et l'append nocturne dans `silver.orders` échoue désormais. Faut-il activer `mergeSchema` en permanence ?

<!-- solution -->

Pas aveuglément. Ajoutez la colonne volontairement (`ALTER TABLE ... ADD COLUMN discount ...` ou une écriture ponctuelle avec `mergeSchema`) après avoir vérifié son sens et son type. Une évolution automatique permanente laisse n'importe quelle erreur en amont remodeler une table silver de confiance.

<!-- takeaways -->

- L'enforcement est la règle ; l'évolution doit être un choix délibéré.
- `CHECK` et `NOT NULL` sont appliqués ; clés primaires et étrangères sont informatives.
- Les propriétés de table activent ou désactivent CDF et la rétention.

<!-- unit: Time travel, restore et rétention -->

<!-- goals -->

- Interroger et restaurer d'anciennes versions d'une table.
- Expliquer comment `VACUUM` et la rétention limitent le time travel.

<!-- concept -->

Comme les anciens fichiers restent dans le stockage jusqu'à leur suppression, chaque version Delta peut être relue : c'est le time travel, et `RESTORE` rend une ancienne version courante par un nouveau commit. Les clones copient une table à un instant donné, entièrement (deep) ou en métadonnées seules (shallow).

Le time travel n'est pas un stockage gratuit éternel. `VACUUM` supprime les fichiers non référencés plus anciens que la rétention (7 jours par défaut), et le journal garde 30 jours d'historique. Une fois les fichiers supprimés, les versions qui en dépendaient ne sont plus lisibles.

<!-- example -->

```sql
DESCRIBE HISTORY gold.revenue;                 -- find the bad commit, say v57
SELECT * FROM gold.revenue VERSION AS OF 56;   -- check the good version
RESTORE TABLE gold.revenue TO VERSION AS OF 56;
```

#### Qu'est-ce que le voyage dans le temps (time travel) ?

Interroger une version antérieure d'une table par numéro de version ou par horodatage, grâce au journal de transactions :

```sql
SELECT * FROM sales VERSION AS OF 42;
SELECT * FROM sales TIMESTAMP AS OF '2026-10-01';
DESCRIBE HISTORY sales;
```

C'est utile pour les audits, reproduire un rapport, comparer des versions et récupérer d'une écriture erronée. Cela ne fonctionne que tant que les anciens fichiers n'ont pas été supprimés par `VACUUM`.

#### Comment annuler une écriture erronée dans Delta ?

`RESTORE TABLE sales TO VERSION AS OF 41` (ou `TIMESTAMP AS OF`). La commande crée un nouveau commit qui pointe de nouveau vers les anciens fichiers, l'historique est donc conservé.

#### Que fait `VACUUM` ?

Il supprime les fichiers de données qui ne sont plus référencés par la version courante et qui sont plus anciens que le seuil de rétention (7 jours par défaut). Il économise du stockage mais limite le voyage dans le temps à la période de rétention. Descendre le seuil sous la durée de la plus longue lecture ou écriture peut casser des requêtes concurrentes.

#### Quelle est la différence entre la rétention du journal et celle des fichiers supprimés ?

`delta.logRetentionDuration` (30 jours par défaut) contrôle combien de temps l'historique des commits est conservé ; `delta.deletedFileRetentionDuration` (7 jours par défaut) contrôle combien de temps `VACUUM` garde les fichiers de données non référencés. Le voyage dans le temps a besoin des deux : les entrées du journal et les fichiers de données.

#### Quelle est la différence entre un deep clone et un shallow clone ?

Un deep clone copie les fichiers de données et les métadonnées dans une table indépendante. Un shallow clone ne copie que les métadonnées et pointe vers les fichiers de la source : il est instantané et peu coûteux, pratique pour tester des changements sur des données de la taille de la production. Les deux ont leur propre historique à partir du clonage.

#### Quelqu'un a supprimé par erreur des colonnes d'une table gold il y a une heure. Comment la récupérez-vous ?

Je cherche dans `DESCRIBE HISTORY` la version précédant le changement et je lance `RESTORE TABLE … TO VERSION AS OF` cette version, ou je fais un `SELECT` dessus pour reconstruire. Ensuite je revois les droits pour que seul le service principal du pipeline puisse modifier les tables gold.

<!-- challenge -->

L'audit vous demande de reproduire un rapport exactement tel qu'il était il y a 60 jours. Avec la configuration par défaut, est-ce possible ? Que changeriez-vous ?

<!-- solution -->

Probablement pas : les fichiers supprimés disparaissent après 7 jours et le journal garde 30 jours. À l'avenir, augmentez `delta.logRetentionDuration` et `delta.deletedFileRetentionDuration` sur cette table, ou figez les données du rapport (deep clone ou table datée) à chaque publication.

<!-- takeaways -->

- Le time travel lit d'anciennes versions ; `RESTORE` en rend une courante.
- `VACUUM` et la rétention définissent jusqu'où remonter.
- Les shallow clones sont des copies instantanées pour tester sur des données réelles.

<!-- unit: Modifier les données : MERGE, UPDATE et DELETE -->

<!-- goals -->

- Écrire un `MERGE` correct et corriger ses erreurs courantes.
- Expliquer copy-on-write, deletion vectors et Change Data Feed.

<!-- concept -->

Les fichiers Parquet sont immuables : modifier une ligne implique d'écrire de nouveaux fichiers. Sans deletion vectors, `UPDATE`, `DELETE` et `MERGE` réécrivent chaque fichier contenant une ligne touchée (copy-on-write). Les deletion vectors marquent plutôt les lignes supprimées dans un petit fichier annexe et réécrivent plus tard.

`MERGE` est l'outil central des upserts, du CDC et de la déduplication. Ses deux problèmes habituels : des sources ambiguës (plusieurs lignes par clé) et des scans lents de toute la cible. Pour remplacer une tranche entière, `replaceWhere` est plus simple. Change Data Feed permet à l'aval de ne lire que les lignes modifiées.

<!-- example -->

Dédupliquer la source, puis fusionner :
```sql
MERGE INTO silver.customers t
USING (
  SELECT * FROM updates
  QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1
) s
ON t.customer_id = s.customer_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

#### Comment Delta exécute-t-il `UPDATE` et `DELETE` sans deletion vectors ?

Il trouve les fichiers contenant des lignes concernées, les réécrit sans les lignes supprimées (ou avec les valeurs mises à jour) et valide une transaction qui retire les anciens fichiers et ajoute les nouveaux. C'est du copy-on-write : lectures peu coûteuses, écritures coûteuses sur les gros fichiers.

#### Que sont les deletion vectors ?

Une optimisation du stockage où `DELETE`, `UPDATE` et `MERGE` marquent les lignes comme supprimées dans un petit fichier annexe au lieu de réécrire des fichiers Parquet entiers. Les écritures deviennent beaucoup plus rapides ; les fichiers sont physiquement réécrits plus tard par `OPTIMIZE` ou `REORG TABLE … APPLY (PURGE)`.

#### Comment fonctionne `MERGE` dans Delta ?

`MERGE INTO` fait un upsert d'une source dans une cible selon une condition de jointure, avec des clauses pour les lignes qui correspondent et celles qui ne correspondent pas. C'est la base du CDC, de la déduplication et de la logique SCD.

```sql
MERGE INTO silver.customers t
USING updates s ON t.customer_id = s.customer_id
WHEN MATCHED AND s.op = 'DELETE' THEN DELETE
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

#### Pourquoi `MERGE` échoue-t-il avec « multiple source rows matched » ?

Parce que deux lignes source ou plus correspondent à la même ligne cible, ce qui rendrait le résultat ambigu. Il faut d'abord dédupliquer la source, par exemple en gardant la ligne la plus récente par clé avec `ROW_NUMBER()`.

#### Comment accélérer un `MERGE` lent ?

En ajoutant des filtres qui permettent à Delta d'écarter des fichiers de la cible (par exemple une plage de dates dans la clause `ON`), en regroupant la cible par la clé de merge, en dédupliquant et en réduisant la source, en activant les deletion vectors, et en évitant de fusionner tout l'historique quand seules les données récentes changent.

#### Quelle est la différence entre le mode `overwrite` et `replaceWhere` ?

`mode("overwrite")` remplace toute la table (sous forme d'une nouvelle version, donc le voyage dans le temps fonctionne toujours). `replaceWhere` ne remplace que les lignes qui satisfont un prédicat. L'écrasement dynamique de partitions (`partitionOverwriteMode=dynamic`) ne remplace que les partitions présentes dans les nouvelles données.

#### Qu'est-ce que le Change Data Feed ?

Une option de table (`delta.enableChangeDataFeed = true`) qui enregistre les changements au niveau ligne (insert, update_preimage, update_postimage, delete) avec la version et l'horodatage du commit. Les traitements en aval ne lisent que ce qui a changé :

```sql
SELECT * FROM table_changes('silver.customers', 120);
```

#### Comment traiter une demande d'effacement RGPD sur un lakehouse Delta ?

Je supprime les lignes de la personne avec `DELETE` ou `MERGE` dans toutes les couches (bronze compris), puis je lance `VACUUM` pour supprimer physiquement les anciens fichiers qui les contenaient, une fois la période de rétention écoulée. Pseudonymiser les identifiants tôt dans le pipeline limite le nombre de tables contenant des données personnelles.

<!-- challenge -->

Un `MERGE` quotidien de 50 000 lignes modifiées dans une table de 3 milliards de lignes prend 40 minutes. Les changements portent toujours sur les 3 derniers jours. Que tentez-vous d'abord ?

<!-- solution -->

Ajouter la plage de dates à la condition `ON` (par exemple `t.event_date >= current_date() - 3`) pour que Delta élague la plupart des fichiers cibles, et regrouper la table par date et clé. Activer les deletion vectors pour ne pas réécrire entièrement les fichiers concernés.

<!-- takeaways -->

- Sans deletion vectors, toute modification de ligne réécrit des fichiers entiers.
- Dédupliquez la source du `MERGE` ; élaguez la cible avec des conditions en plus.
- CDF ne fournit à l'aval que les lignes modifiées.

<!-- unit: Organisation des fichiers et data skipping -->

<!-- goals -->

- Diagnostiquer et corriger le problème des petits fichiers.
- Préférer le liquid clustering au partitionnement et au Z-ordering pour les nouvelles tables.

<!-- concept -->

La vitesse dépend des fichiers ouverts et sautés. `OPTIMIZE`, les optimized writes et l'auto compaction regroupent les petits fichiers. Delta conserve des statistiques min/max par fichier, si bien qu'un filtre saute les fichiers hors plage ; il faut que les valeurs proches soient groupées.

Le clustering les y place. Le partitionnement découpe par répertoire et ne convient qu'aux tables énormes sur des colonnes peu cardinales. Le Z-ordering doit être relancé. Le liquid clustering (`CLUSTER BY`) regroupe de façon incrémentale, permet de changer de clés et est désormais le choix par défaut.

<!-- example -->

```sql
DESCRIBE DETAIL silver.events;            -- numFiles: 480000, sizeInBytes: 200 GB → ~400 KB per file
ALTER TABLE silver.events CLUSTER BY (event_date, user_id);
OPTIMIZE silver.events;                   -- compacts and clusters
```

#### Qu'est-ce que le problème des petits fichiers ?

De nombreux fichiers minuscules ralentissent les lectures (chaque fichier a un coût d'ouverture et de métadonnées, et les statistiques sont moins utiles) ainsi que le journal de transactions. Le streaming et les petits ajouts fréquents en sont la cause. Solutions : `OPTIMIZE`, l'auto-compaction et les écritures optimisées, et des lots moins nombreux et plus gros.

#### Que fait `OPTIMIZE` ?

Il compacte les petits fichiers en fichiers plus gros (environ 1 Go par défaut), ce qui accélère les lectures. Avec le Z-ordering ou le liquid clustering, il réécrit aussi les données pour que les valeurs proches se retrouvent dans les mêmes fichiers.

#### Que sont les écritures optimisées et l'auto-compaction ?

Les écritures optimisées redistribuent les données avant l'écriture pour que chaque partition produise moins de fichiers, plus gros. L'auto-compaction lance un petit `OPTIMIZE` après une écriture quand une table compte beaucoup de petits fichiers. Les deux sont activées par défaut pour de nombreuses opérations sur les runtimes récents et en serverless.

#### Qu'est-ce que le data skipping ?

Delta stocke les valeurs minimale et maximale et le nombre de nulls des premières colonnes de chaque fichier (32 par défaut). Quand une requête filtre sur ces colonnes, les fichiers dont les plages ne peuvent pas correspondre sont ignorés sans être lus. Cela fonctionne mieux quand les données sont regroupées selon les colonnes filtrées.

#### Qu'est-ce que le Z-ordering ?

Une technique de regroupement multidimensionnel lancée avec `OPTIMIZE table ZORDER BY (col1, col2)`. Elle place dans les mêmes fichiers les valeurs proches de plusieurs colonnes pour améliorer le data skipping. Il faut la relancer à mesure que les données arrivent, et elle est remplacée par le liquid clustering.

#### Qu'est-ce que le liquid clustering ?

Une méthode de regroupement déclarée sur la table avec `CLUSTER BY (cols)` qui remplace à la fois le partitionnement et le Z-ordering. Elle regroupe les données de façon incrémentale pendant `OPTIMIZE`, les clés peuvent changer sans réécrire la table, et `CLUSTER BY AUTO` laisse Databricks choisir les clés d'après l'historique des requêtes. C'est l'organisation recommandée pour les nouvelles tables.

```sql
CREATE TABLE events (event_date DATE, user_id BIGINT, payload STRING)
CLUSTER BY (event_date, user_id);
```

#### Quand faut-il encore partitionner une table Delta ?

Rarement, maintenant que le liquid clustering existe. Le partitionnement n'aide que pour les très grandes tables (au-delà d'environ 1 To) sur une colonne de faible cardinalité filtrée par presque toutes les requêtes, avec au moins 1 Go par partition. Trop partitionner crée le problème des petits fichiers.

#### Votre table Delta compte 500 000 petits fichiers. Que faites-vous ?

Je lance `OPTIMIZE` (avec liquid clustering sur les principales colonnes de filtre), j'active les écritures optimisées et l'auto-compaction ou l'optimisation prédictive, puis je corrige la cause : regrouper les micro-ajouts, éviter le surpartitionnement et utiliser des triggers `availableNow` plutôt que des flux minuscules très fréquents. Je lance ensuite `VACUUM` pour supprimer les anciens fichiers.

<!-- challenge -->

Une table partitionnée par `customer_id` (200 000 clients) est lente pour toutes les requêtes. Que s'est-il passé et que faites-vous ?

<!-- solution -->

Le partitionnement à forte cardinalité a créé des centaines de milliers de petits répertoires et fichiers. Recréez la table sans partitions, avec `CLUSTER BY (customer_id)` (plus la date si les requêtes filtrent dessus), lancez `OPTIMIZE`, puis `VACUUM` sur les anciens fichiers.

<!-- takeaways -->

- Visez peu de gros fichiers ; `DESCRIBE DETAIL` donne le nombre de fichiers.
- Le data skipping exige des données regroupées.
- Liquid clustering pour les nouvelles tables ; partitionnez seulement les tables énormes sur des colonnes peu cardinales.

<!-- stage: Construire des pipelines -->

### Ingestion

<!-- unit: Choisir une voie d'ingestion -->

<!-- goals -->

- Choisir le bon outil pour fichiers, bases de données, sources SaaS et flux.
- Charger une table relationnelle en parallèle et de façon incrémentale.

<!-- concept -->

La façon dont les données arrivent décide de l'outil. Les fichiers déposés dans le stockage passent par Auto Loader (ou `COPY INTO` pour des lots modestes, ou `read_files` en SQL). Applications SaaS et bases de données peuvent utiliser les connecteurs managés de Lakeflow Connect ; sinon une lecture JDBC suffit. Les flux d'événements viennent de Kafka ou équivalent via Structured Streaming.

Quelle que soit la source, le schéma est le même : déposer les données brutes en bronze, de façon incrémentale, avec assez de métadonnées pour savoir d'où vient chaque ligne.

<!-- example -->

| Source | Premier choix |
|---|---|
| Fichiers dans S3 / ADLS / volumes | Auto Loader (`cloudFiles`) |
| Quelques milliers de fichiers par lot, SQL seulement | `COPY INTO` |
| Salesforce, SQL Server, Workday... | Lakeflow Connect |
| PostgreSQL sans connecteur | Spark JDBC, partitionné, par watermark |
| Kafka, Kinesis, Event Hubs | Structured Streaming |

#### Quelles options existent pour charger des données dans Databricks ?

Auto Loader pour les fichiers qui arrivent dans le stockage cloud, `COPY INTO` pour des chargements batch idempotents, les connecteurs gérés de Lakeflow Connect (Salesforce, Workday, SQL Server, Google Analytics et d'autres), Structured Streaming depuis Kafka, Kinesis ou Event Hubs, Lakehouse Federation pour interroger sur place, des outils partenaires (Fivetran et d'autres) et le dépôt de fichiers dans des volumes.

#### Qu'est-ce que Lakeflow Connect ?

Des connecteurs d'ingestion gérés et serverless pour les applications SaaS et les bases de données. Ils gèrent l'extraction incrémentale (souvent en CDC) et déposent les données dans des tables Unity Catalog via un pipeline, sans écrire de code d'extraction.

#### Comment charger les données d'une base relationnelle sans Lakeflow Connect ?

Avec le lecteur JDBC de Spark, en partitionnant la lecture avec `partitionColumn`, `lowerBound`, `upperBound` et `numPartitions` pour l'exécuter en parallèle, et en chargeant de façon incrémentale selon une colonne de watermark (par exemple `updated_at`). Stockez les identifiants dans des secrets.

#### Comment ingérer depuis Kafka ?

Avec la source Kafka de Structured Streaming, qui lit `key`, `value`, `topic`, `partition`, `offset` et `timestamp`. On décode `value` (JSON, Avro avec un schema registry, Protobuf), on écrit les enregistrements bruts en bronze et on garde un checkpoint par requête.

#### Qu'est-ce que `COPY INTO` ?

Une commande SQL qui charge les fichiers d'un chemin dans une table Delta et qui est idempotente : les fichiers déjà chargés sont ignorés. Elle convient aux chargements batch planifiés de milliers de fichiers ; Auto Loader est préférable pour des millions de fichiers ou une ingestion continue.

```sql
COPY INTO bronze.customers
FROM '/Volumes/raw/landing/customers/'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');
```

#### Qu'est-ce que `read_files` ?

Une fonction SQL de table qui lit des fichiers (CSV, JSON, Parquet, Avro, XML, texte) depuis un chemin ou un volume avec inférence de schéma. Avec `STREAM read_files(...)` dans une streaming table, elle utilise Auto Loader en coulisses.

<!-- challenge -->

Vous devez charger chaque nuit une table PostgreSQL de 400 millions de lignes, dont environ 1 % change. Esquissez la lecture.

<!-- solution -->

Lire seulement les lignes dont `updated_at` dépasse le dernier watermark chargé (stocké dans une table de contrôle ou pris sur le maximum de la cible), avec une lecture JDBC partitionnée sur une clé numérique (`partitionColumn`, bornes, `numPartitions`). Faire un `MERGE` du résultat par clé primaire. Les suppressions demandent une autre voie, comme le CDC ou une comparaison périodique des clés.

<!-- takeaways -->

- Choisissez l'outil selon l'arrivée des données : fichiers, bases, SaaS ou flux.
- Chargez de façon incrémentale ; les rechargements complets ne passent pas à l'échelle.
- Bronze garde les données brutes et leur provenance.

<!-- unit: Auto Loader et le suivi du streaming -->

<!-- goals -->

- Expliquer comment Auto Loader charge chaque fichier exactement une fois.
- Exécuter une ingestion en streaming selon un calendrier batch avec `availableNow`.

<!-- concept -->

Auto Loader est une source de streaming qui découvre les nouveaux fichiers, en listant le répertoire ou via des notifications du stockage. Il enregistre les fichiers traités dans le checkpoint du flux : un redémarrage ne charge jamais deux fois un fichier, et les fichiers tardifs sont tout de même pris.

Streaming ne veut pas dire toujours allumé. Avec `trigger(availableNow=True)`, la requête traite tout ce qui est nouveau puis s'arrête : le suivi du streaming au coût d'un job planifié. La colonne cachée `_metadata` indique de quel fichier vient chaque ligne.

<!-- example -->

```python
(spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("cloudFiles.schemaLocation", "/Volumes/raw/_schemas/orders")
    .load("/Volumes/raw/landing/orders/")
    .select("*", "_metadata.file_path", "_metadata.file_modification_time")
  .writeStream
    .option("checkpointLocation", "/Volumes/raw/_checkpoints/orders")
    .trigger(availableNow=True)          # run as a daily batch
    .toTable("bronze.orders"))
```

#### Qu'est-ce qu'Auto Loader ?

Une source Structured Streaming (`cloudFiles`) qui traite de façon incrémentale et efficace les nouveaux fichiers à mesure qu'ils arrivent dans le stockage cloud. Elle enregistre dans son checkpoint les fichiers déjà traités, donc chaque fichier est chargé exactement une fois, et elle peut inférer et faire évoluer le schéma.

```python
(spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/Volumes/raw/_schemas/orders")
    .load("/Volumes/raw/landing/orders/")
  .writeStream
    .option("checkpointLocation", "/Volumes/raw/_checkpoints/orders")
    .trigger(availableNow=True)
    .toTable("bronze.orders"))
```

#### Quels sont les modes de détection de fichiers d'Auto Loader ?

Le listage de répertoires, qui liste le chemin d'entrée pour trouver les nouveaux fichiers (simple, suffisant pour des volumes modérés), et la notification de fichiers, qui s'abonne aux événements du stockage via une file (SQS/SNS, Event Grid) et passe à l'échelle de millions de fichiers. Les installations récentes peuvent utiliser les managed file events des external locations.

#### Qu'est-ce qu'un checkpoint de streaming ?

Un emplacement de stockage où une requête de streaming enregistre sa progression (offsets ou fichiers traités) et son état. Il garantit un traitement exactly-once entre les redémarrages. Chaque requête a besoin de son propre checkpoint, et le supprimer fait repartir la requête de zéro.

#### Que fait `trigger(availableNow=True)` ?

Il fait traiter à une requête de streaming tout ce qui est disponible au démarrage (en plusieurs lots, en respectant les limites de débit), puis l'arrête. On obtient le suivi incrémental du streaming avec le profil de coût d'un job batch planifié.

#### Qu'est-ce que la colonne `_metadata` ?

Une colonne cachée disponible à la lecture de fichiers, avec `file_path`, `file_name`, `file_size` et `file_modification_time`. Elle remplace `input_file_name()` (non pris en charge dans Unity Catalog) pour enregistrer le fichier d'origine de chaque ligne.

#### Comment gérer les fichiers qui arrivent en retard ?

Auto Loader prend tout nouveau fichier à son arrivée, quelle que soit sa date, donc le chargement lui-même est sûr. En aval, utilisez `MERGE` sur les clés métier, ou retraitez les dates concernées avec `replaceWhere`, pour que les données tardives corrigent les résultats précédents.

<!-- challenge -->

Quelqu'un supprime le dossier de checkpoint d'un flux d'ingestion bronze « pour faire le ménage ». Que se passe-t-il à l'exécution suivante et comment récupérer ?

<!-- solution -->

Le flux repart de zéro et recharge tous les fichiers du chemin d'arrivée, ce qui duplique bronze. Restaurez la table bronze à la version précédant l'exécution (ou dédupliquez par chemin de fichier), puis laissez le nouveau checkpoint continuer. Protégez les checkpoints par des permissions.

<!-- takeaways -->

- Le checkpoint rend l'ingestion exactly-once ; ne le partagez ni ne le supprimez jamais.
- `availableNow` donne le suivi du streaming avec un calendrier batch.
- Enregistrez `_metadata.file_path` pour la traçabilité.

<!-- unit: Inférence et dérive de schéma -->

<!-- goals -->

- Contrôler l'inférence de schéma dans les chargements de production.
- Gérer colonnes nouvelles ou mal formées sans perdre de données.

<!-- concept -->

Les sources changent sans prévenir. Inférer le schéma à chaque exécution est lent et instable : les chargements de production déclarent un schéma ou laissent Auto Loader le gérer. Il stocke le schéma inféré, s'arrête quand une nouvelle colonne apparaît et repart avec le schéma enrichi après redémarrage.

Les schema hints figent les types importants, et les valeurs qui ne collent pas vont dans `_rescued_data` au lieu d'être perdues. Surveiller cette colonne alerte tôt d'un changement de la source.

<!-- example -->

```python
.option("cloudFiles.schemaHints", "amount DECIMAL(18,2), event_ts TIMESTAMP")
.option("cloudFiles.schemaEvolutionMode", "addNewColumns")
# Later: SELECT count(*) FROM bronze.orders WHERE _rescued_data IS NOT NULL
```

#### Pourquoi éviter `inferSchema` en production ?

L'inférence demande une lecture supplémentaire des données, peut déduire des types différents selon les fichiers et change silencieusement quand la source change. Déclarez les schémas (contrats de données) pour les chargements de production, ou laissez Auto Loader gérer l'inférence avec des schema hints.

#### Comment Auto Loader gère-t-il les changements de schéma ?

Il stocke le schéma inféré dans l'emplacement de schéma. Avec le mode par défaut `addNewColumns`, une nouvelle colonne arrête le flux, met à jour le schéma, et le flux reprend après redémarrage. Les données qui ne correspondent pas au schéma (mauvais type, colonne inattendue) vont dans la colonne `_rescued_data` au lieu d'être perdues.

#### Qu'est-ce que la colonne de données récupérées ?

Une colonne de texte JSON (`_rescued_data`) où Auto Loader place les valeurs qu'il n'a pas pu convertir selon le schéma. La surveiller révèle les changements de format en amont.

#### Que sont les schema hints d'Auto Loader ?

Des types explicites pour certaines colonnes (`cloudFiles.schemaHints = "amount DECIMAL(18,2), event_ts TIMESTAMP"`) qui priment sur l'inférence, le reste du schéma étant toujours inféré.

#### Une requête de streaming échoue après un changement de schéma de la source. Comment le gérez-vous ?

Avec Auto Loader en mode `addNewColumns`, je redémarre le flux pour qu'il prenne le nouveau schéma. Pour les changements incompatibles, je mets à jour le schéma cible (ou j'utilise la colonne de données récupérées) et, si la logique a changé, je démarre un nouveau checkpoint avec un plan de backfill clair. J'ajoute une alerte sur les données récupérées.

<!-- challenge -->

Après une mise à jour du fournisseur, `amount` arrive en `"12,50"` (virgule décimale) dans certains fichiers. Que se passe-t-il avec un type `DECIMAL` fixé par hint, et comment le remarquer ?

<!-- solution -->

Ces valeurs ne se convertissent pas : `amount` est nul et la valeur brute part dans `_rescued_data`. Une alerte sur la part de lignes avec données sauvées le détecte ; corrigez ensuite la conversion en silver (remplacer la virgule, caster) et retraitez les fichiers concernés.

<!-- takeaways -->

- Déclarez ou indiquez les types importants ; ne comptez pas sur l'inférence.
- `addNewColumns` s'arrête, fait évoluer le schéma et repart après redémarrage.
- Surveillez `_rescued_data` pour repérer les changements en amont.

### Architecture médaillon et modélisation

<!-- unit: Les couches et leurs contrats -->

<!-- goals -->

- Décrire ce qui va en bronze, silver et gold.
- Justifier une couche brute et adapter les couches au projet.

<!-- concept -->

L'architecture médaillon organise un lakehouse en couches de qualité croissante. Bronze garde ce que la source a envoyé, pour retraiter et auditer. Silver est la version nettoyée, dédupliquée et validée de chaque entité, celle à laquelle tous se fient. Gold met les données en forme pour leur usage : schémas en étoile, agrégats et features.

La valeur est dans les contrats entre couches, pas dans le chiffre trois. Les petits projets fusionnent des couches ; d'autres ajoutent une zone d'arrivée ou une couche de service.

<!-- example -->

| Couche | Table d'exemple | Contrat |
|---|---|---|
| Bronze | `bronze.orders` | Lignes brutes + `file_path`, heure de chargement ; append seulement |
| Silver | `silver.orders` | Typée, une ligne par `order_id`, lignes en erreur en quarantaine |
| Gold | `gold.fct_daily_sales` | Grain : une ligne par jour et magasin ; définitions métier appliquées |

#### Qu'est-ce que l'architecture médaillon ?

Une façon d'organiser les données du lakehouse en couches : bronze contient les données brutes telles que reçues (en ajout seul, avec des métadonnées de chargement), silver les données nettoyées, harmonisées, dédupliquées et validées, et gold les agrégats métier et modèles dimensionnels prêts pour la BI et le ML. La qualité et la structure augmentent de couche en couche.

#### Pourquoi garder une couche bronze brute ?

Pour pouvoir retraiter l'historique quand la logique change ou qu'on trouve des bugs, auditer ce que la source a réellement envoyé, et découpler l'ingestion de la transformation. Bronze doit être peu coûteux à conserver et fidèle à la source.

#### Bronze doit-elle être une table Delta ou des fichiers bruts ?

En général, les fichiers bruts restent dans une zone de landing (ou un volume) et bronze est une table Delta chargée depuis ces fichiers avec un minimum de changements et des métadonnées de chargement. Delta en bronze apporte les transactions, le suivi du schéma et un retraitement rapide ; garder les fichiers d'origine donne une copie exacte pour les audits.

#### Que met-on en silver ?

Des colonnes typées et renommées, la déduplication, des valeurs standardisées (dates, codes, adresses), des jointures avec les données de référence, des contrôles de qualité avec mise en quarantaine des lignes défectueuses, et l'historique (SCD de type 2) si besoin. Silver est la version unique et fiable de chaque entité.

#### Que met-on en gold ?

Des données mises en forme pour la consommation : schémas en étoile (faits et dimensions), agrégats, tables de features et produits de données, avec les définitions métier appliquées. Les tables gold sont généralement plus petites et optimisées pour la lecture.

#### L'architecture médaillon a-t-elle toujours trois couches ?

Non. C'est une convention, pas une règle. Les petits projets peuvent fusionner silver et gold ; d'autres ajoutent une zone d'atterrissage (landing) avant bronze ou une couche de service (platinum) après gold. L'important est que chaque couche ait un contrat clair.

<!-- challenge -->

Un collègue propose de nettoyer les données au chargement et de se passer de bronze « pour économiser du stockage ». Que perdez-vous ?

<!-- solution -->

La possibilité de retraiter l'historique quand la logique de nettoyage change ou contient un bug, et la preuve de ce que la source a réellement envoyé. Le stockage bronze coûte peu comparé à une nouvelle extraction de données que la source n'a peut-être plus.

<!-- takeaways -->

- Bronze est fidèle, silver est fiable, gold est façonné pour l'usage.
- Chaque couche est un contrat sur le grain, la qualité et les responsables.
- Adaptez le nombre de couches ; gardez les contrats.

<!-- unit: Patrons de modélisation -->

<!-- goals -->

- Mettre en œuvre une SCD de type 2 et la quarantaine d'enregistrements sur Delta.
- Organiser catalogues et tables gold pour la BI et le ML.

<!-- concept -->

C'est en silver que l'on gère l'historique et la qualité. La SCD de type 2 garde chaque version d'une entité avec des dates de validité, maintenues par un seul `MERGE`. La quarantaine envoie les lignes en échec, avec leurs motifs, vers une table à part pour que le pipeline continue et que quelqu'un corrige la source.

Gold sert ensuite deux publics à partir du même silver : schémas en étoile pour la BI, tables de features pour le ML. Les catalogues séparent souvent les environnements et les schémas les couches, si bien que les permissions suivent l'environnement.

<!-- example -->

Lignes SCD de type 2 pour un client :
| customer_id | city | valid_from | valid_to | is_current |
|---|---|---|---|---|
| 42 | Bogotá | 2024-01-10 | 2026-03-02 | false |
| 42 | Medellín | 2026-03-02 | null | true |

#### Comment implémenter une SCD de type 2 sur Delta ?

Avec `MERGE` : on clôt la ligne courante (on remplit `valid_to` et `is_current = false`) quand les attributs suivis changent, et on insère la nouvelle version. Une astuce courante consiste à fusionner une union des mises à jour avec une clé de merge nulle pour les lignes modifiées, de sorte qu'un seul `MERGE` clôt et insère. Les pipelines déclaratifs le font avec `AUTO CDC … STORED AS SCD TYPE 2`.

#### Comment mettre en quarantaine les enregistrements défectueux ?

En validant les lignes selon des règles en silver, en écrivant les lignes en échec avec leurs motifs dans une table de quarantaine, et en continuant avec les lignes valides. Surveillez le taux de quarantaine et alertez sur les pics. Dans les pipelines déclaratifs, des expectations `DROP ROW` et une requête inverse séparée donnent le même résultat.

#### Faut-il un catalogue par environnement ou par couche ?

Un schéma courant est un catalogue par environnement (`dev`, `staging`, `prod`) avec des schémas par couche (`bronze`, `silver`, `gold`), car les environnements ont besoin de droits et de stockages différents. Certaines équipes préfèrent des catalogues par domaine ou par entité métier. La cohérence compte plus que le choix.

#### Qu'est-ce qu'un produit de données dans le contexte de Databricks ?

Un ensemble de tables (généralement gold) sélectionné, documenté et gouverné, dont une équipe est responsable, avec des contrôles de qualité, une interface claire et un accès accordé via Unity Catalog, éventuellement partagé par Delta Sharing.

#### Comment modéliser gold pour la BI et le ML à la fois ?

Avec des schémas en étoile (faits à un grain déclaré et dimensions conformes) pour la BI, et des tables de features par entité et par date pour le ML, tous construits à partir des mêmes tables silver pour que les chiffres concordent.

<!-- challenge -->

La finance publie le chiffre d'affaires par région client et veut que les chiffres de l'an dernier restent inchangés quand des clients déménagent. Quel type de dimension utilisez-vous et comment la table de faits s'y joint-elle ?

<!-- solution -->

Une SCD de type 2 sur la dimension client, avec une clé de substitution par version. La table de faits stocke la clé valide au moment de la vente (ou joint sur la clé naturelle avec `sale_date BETWEEN valid_from AND valid_to`), donc les anciennes ventes gardent leur ancienne région.

<!-- takeaways -->

- La SCD2 garde l'historique avec des plages de validité ; un `MERGE` suffit à la maintenir.
- Mettez les lignes en erreur en quarantaine avec leur motif au lieu d'échouer ou de les perdre.
- Construisez le gold BI et ML depuis le même silver pour que les chiffres concordent.

### Lakeflow Declarative Pipelines

<!-- unit: Le modèle déclaratif -->

<!-- goals -->

- Expliquer ce qu'un pipeline déclaratif gère pour vous.
- Choisir entre streaming table et vue matérialisée.

<!-- concept -->

Dans un pipeline déclaratif, on définit les tables voulues et les requêtes qui les produisent ; le moteur déduit l'ordre, les exécute, relance les échecs et gère le calcul. Plus de code d'orchestration ni de checkpoints à écrire.

Deux types de datasets couvrent l'essentiel. Une streaming table traite chaque ligne d'entrée une fois, idéale pour l'ingestion et les données en append. Une vue matérialisée se recalcule (de façon incrémentale si possible) pour toujours correspondre à ses sources, idéale pour jointures et agrégats. Les flows permettent à plusieurs sources d'alimenter une table.

<!-- example -->

```sql
CREATE OR REFRESH STREAMING TABLE silver_orders
AS SELECT * FROM STREAM bronze_orders WHERE order_id IS NOT NULL;

CREATE OR REFRESH MATERIALIZED VIEW gold_sales_by_day
AS SELECT order_date, sum(amount) AS sales FROM silver_orders GROUP BY order_date;
```

#### Que sont les Lakeflow Declarative Pipelines (anciennement Delta Live Tables) ?

Un framework déclaratif où vous définissez les tables et les requêtes qui les produisent, en SQL ou en Python, et où Databricks déduit les dépendances, orchestre l'exécution, gère l'infrastructure, relance les échecs et applique les attentes de qualité des données. Le moteur a été donné à Apache Spark sous le nom de Spark Declarative Pipelines.

#### Quelle est la différence entre une streaming table et une vue matérialisée ?

Une streaming table traite chaque ligne d'entrée une seule fois, en ajoutant ou en mettant à jour de façon incrémentale, ce qui convient à l'ingestion et aux données en ajout seul. Une vue matérialisée stocke le résultat d'une requête et est rafraîchie (de façon incrémentale quand c'est possible) pour toujours refléter ses sources, ce qui convient aux agrégations et jointures sur des données qui changent.

```sql
CREATE OR REFRESH STREAMING TABLE bronze_orders
AS SELECT * FROM STREAM read_files('/Volumes/raw/landing/orders/', format => 'json');

CREATE OR REFRESH MATERIALIZED VIEW gold_daily_sales
AS SELECT order_date, sum(amount) AS sales FROM silver_orders GROUP BY order_date;
```

#### Comment écrire un pipeline déclaratif en Python ?

Avec le module `pipelines` (anciennement `dlt`) : des fonctions décorées renvoient des DataFrames, et les décorateurs déclarent les tables et les expectations.

```python
from pyspark import pipelines as dp

@dp.table(comment="Commandes nettoyées")
@dp.expect_or_drop("valid_amount", "amount >= 0")
def silver_orders():
    return spark.readStream.table("bronze_orders").dropDuplicates(["order_id"])
```

#### Qu'est-ce qu'un flow dans un pipeline déclaratif ?

Une unité de traitement qui écrit dans une table cible. Une streaming table peut avoir plusieurs append flows (par exemple un par région source), ce qui permet d'ajouter des sources sans full refresh.

#### Où vivent les tables d'un pipeline ?

Dans le catalogue et le schéma Unity Catalog configurés pour le pipeline (et dans d'autres schémas si on utilise des noms complets). Pour les lecteurs, ce sont des tables Delta ordinaires, mais seul le pipeline devrait y écrire.

#### Quand ne pas utiliser les pipelines déclaratifs ?

Quand vous avez besoin d'un contrôle fin de chaque étape, d'une logique qui ne rentre pas dans le modèle déclaratif (code procédural complexe, appels à des systèmes externes à chaque lot) ou de portabilité vers de simples jobs Spark. Beaucoup d'équipes utilisent des jobs classiques avec Delta et `MERGE` et obtiennent les mêmes résultats avec plus de code.

<!-- challenge -->

Les commandes arrivent en append ; les remboursements modifient d'anciennes commandes. Il vous faut le chiffre d'affaires quotidien net des remboursements. Quelles tables sont des streaming tables, et laquelle est une vue matérialisée ?

<!-- solution -->

Ingérer commandes et remboursements en streaming tables (chaque événement traité une fois). Calculer le chiffre d'affaires net quotidien en vue matérialisée joignant les deux, car un remboursement modifie le résultat d'un jour passé, ce qu'une vue matérialisée recalcule et qu'une streaming table ne ferait pas.

<!-- takeaways -->

- Déclarez tables et requêtes ; le moteur gère ordre, relances et calcul.
- Les streaming tables traitent chaque ligne une fois ; les vues matérialisées restent justes quand les sources changent.
- Utilisez des flows pour ajouter des sources sans refresh complet.

<!-- unit: Qualité, CDC et exploitation des pipelines -->

<!-- goals -->

- Ajouter expectations et gestion du CDC à un pipeline.
- Exécuter, surveiller et rafraîchir un pipeline en sécurité.

<!-- concept -->

Les expectations déclarent des règles de qualité sur une table, avec une politique pour les violations : les enregistrer, écarter la ligne ou faire échouer la mise à jour. `AUTO CDC` applique un flux de changements avec clés et séquence, gère les événements désordonnés et l'historique SCD de type 2 sans code `MERGE`.

En exploitation, le mode triggered s'exécute puis s'arrête ; le mode continu reste actif. Le mode développement itère vite, l'event log enregistre tout et un full refresh reconstruit une table de zéro, puissant mais coûteux et risqué si la source ne garde plus son historique.

<!-- example -->

```sql
CREATE OR REFRESH STREAMING TABLE silver_customers;

CREATE FLOW customers_cdc AS AUTO CDC INTO silver_customers
FROM STREAM bronze_customer_changes
KEYS (customer_id)
SEQUENCE BY change_ts
APPLY AS DELETE WHEN op = 'D'
STORED AS SCD TYPE 2;
```

#### Que sont les expectations ?

Des règles de qualité des données déclarées sur une table du pipeline. Chaque ligne est vérifiée, et la politique décide de ce qui se passe en cas de violation : garder la ligne et l'enregistrer (`EXPECT`), la supprimer (`ON VIOLATION DROP ROW`) ou faire échouer la mise à jour (`ON VIOLATION FAIL UPDATE`). Les métriques sont visibles dans l'interface du pipeline et dans l'event log.

```sql
CONSTRAINT valid_amount EXPECT (amount >= 0) ON VIOLATION DROP ROW
```

#### Comment gère-t-on le CDC dans les pipelines déclaratifs ?

Avec `AUTO CDC` (anciennement `APPLY CHANGES INTO`), qui applique un flux de changements à une table cible à l'aide d'une clé et d'une colonne de séquencement, gère les événements désordonnés et les suppressions, et peut conserver l'historique en SCD de type 1 ou 2 sans écrire de logique `MERGE`.

#### Quelle est la différence entre le mode triggered et le mode continu d'un pipeline ?

Le mode triggered traite les données disponibles puis s'arrête (moins cher, pour des planifications batch). Le mode continu garde le pipeline actif pour traiter les données avec une faible latence.

#### Qu'est-ce que le mode développement d'un pipeline ?

Un mode qui réutilise le cluster entre les mises à jour et désactive les relances, pour itérer vite et voir les erreurs immédiatement. Le mode production redémarre le cluster en cas d'erreur récupérable et relance.

#### Qu'est-ce que l'event log du pipeline ?

Une table Delta qui enregistre tous les événements d'un pipeline : mises à jour, progression des flows, métriques de qualité, lignage et erreurs. On l'interroge pour construire des tableaux de bord de supervision et de qualité des données.

#### Qu'est-ce qu'un full refresh d'une table de pipeline ?

Vider la table et retraiter toutes les données source depuis le début, y compris la réinitialisation des checkpoints de streaming. C'est nécessaire après des changements de logique qui doivent s'appliquer à l'historique, mais cela peut coûter cher et faire perdre des données si la rétention de la source est plus courte que l'historique.

#### Comment un pipeline déclaratif est-il facturé ?

Selon le calcul du pipeline (serverless ou classique) et l'édition du produit (Core, Pro, Advanced) ; les éditions supérieures ajoutent le CDC et les expectations. Les pipelines serverless sont facturés à l'usage et sont l'option par défaut.

<!-- challenge -->

Un collègue veut lancer un full refresh de la table bronze à cause d'une correction de parsing. Le topic Kafka source garde 7 jours. Contre quoi le mettez-vous en garde ?

<!-- solution -->

Un full refresh vide la table et relit la source depuis le début, mais Kafka n'a que 7 jours : l'historique plus ancien serait perdu. Corrigez plutôt le parsing en silver, ou retraitez seulement le récent, et gardez bronze (ou les fichiers bruts) comme copie long terme.

<!-- takeaways -->

- Les expectations rendent les règles de qualité visibles et applicables.
- `AUTO CDC` remplace le `MERGE` écrit à la main pour les flux de changements.
- Un full refresh relit les sources ; vérifiez d'abord leur rétention.

### Jobs et orchestration

<!-- unit: Jobs, tâches et déclencheurs -->

<!-- goals -->

- Construire un job comme DAG de tâches avec le bon calcul et le bon déclencheur.
- Décider quand Lakeflow Jobs suffit et quand utiliser Airflow.

<!-- concept -->

Un job est un DAG de tâches : notebooks, scripts, SQL, dbt, pipelines ou autres jobs, chacune avec dépendances, calcul, relances et timeouts. Les déclencheurs le lancent selon un calendrier, à l'arrivée de fichiers ou à la mise à jour d'une table source. Les tâches de contrôle ajoutent des boucles (For each) et des branches (If/else).

Si le flux vit surtout dans Databricks, Jobs est plus simple et moins cher qu'un orchestrateur externe. Airflow se justifie quand le DAG traverse de nombreux systèmes.

<!-- example -->

```text
ingest_orders ─┐
               ├─► build_silver ─► check_quality ─► if rows > 0 ─► publish_gold
ingest_stores ─┘                                      └── else ──► notify
```

#### Que sont les Lakeflow Jobs (anciennement Workflows) ?

L'orchestrateur intégré de Databricks. Un job est un DAG de tâches (notebooks, scripts Python, wheels, SQL, dbt, pipelines, JAR, autres jobs) avec dépendances, planifications ou déclencheurs, paramètres, relances, timeouts, notifications et réglages de calcul.

#### Quels types de tâches un job peut-il contenir ?

Notebook, script Python, wheel Python, SQL (requête, fichier, dashboard ou alerte), dbt, pipeline, JAR, Spark Submit, Run Job (un autre job), condition If/else et For each (boucle sur des valeurs).

#### Quels déclencheurs peuvent lancer un job ?

Une planification cron, l'arrivée d'un fichier dans un emplacement de stockage, la mise à jour d'une table (quand une table source change), le mode continu (relance dès la fin), l'API ou la CLI, ou une exécution manuelle.

#### Quelle est la différence entre le calcul de jobs et l'exécution des tâches sur un cluster partagé ?

Chaque tâche peut utiliser son propre cluster de job, partager un cluster de job avec les autres tâches de la même exécution, utiliser du calcul serverless ou un cluster all-purpose existant. Les clusters de job partagés évitent les démarrages répétés ; le serverless supprime le démarrage.

#### Que fait la tâche For each ?

Elle exécute une tâche imbriquée une fois par élément d'une liste (par exemple une liste de pays ou de dates), avec une concurrence configurable, pour ne pas devoir définir une tâche par élément.

#### À quoi sert la tâche de condition If/else ?

À créer une branche dans un job selon une valeur, comme une task value ou un paramètre : par exemple, sauter l'étape de publication quand une tâche de qualité signale zéro ligne valide.

#### Faut-il orchestrer Databricks avec Airflow ou avec Jobs ?

Jobs suffit quand le flux vit surtout dans Databricks, et c'est moins cher et plus simple. Airflow (ou Dagster, Prefect) a du sens quand le DAG couvre de nombreux systèmes, quand l'entreprise en a fait son standard, ou pour des dépendances complexes entre équipes. Le provider Databricks d'Airflow peut lancer des jobs et attendre leur fin.

<!-- challenge -->

Un job doit tourner à chaque modification de la table `silver.orders` de l'équipe amont, mais pas plus d'une fois toutes les 30 minutes. Comment le déclenchez-vous ?

<!-- solution -->

Avec un déclencheur sur mise à jour de table pour `silver.orders` et un délai minimal de 30 minutes entre déclenchements (ou une attente après le dernier changement), et au plus une exécution concurrente avec file.

<!-- takeaways -->

- Un job est un DAG de tâches avec leur calcul, leurs relances et leurs timeouts.
- Déclenchez par calendrier, arrivée de fichiers ou mise à jour de tables.
- Jobs pour les flux centrés sur Databricks ; Airflow pour ceux qui traversent les systèmes.

<!-- unit: Exécutions fiables : paramètres, idempotence et backfills -->

<!-- goals -->

- Rendre un job sûr à relancer et à rejouer sur le passé.
- Passer des paramètres et de petites valeurs entre tâches.

<!-- concept -->

Un job fiable donne le même résultat qu'il tourne une ou trois fois. Cela suppose des écritures qui remplacent ou fusionnent au lieu d'ajouter, et une date de traitement venant d'un paramètre plutôt que de l'horloge. Des références dynamiques comme `{{job.start_time.iso_date}}` fournissent ce contexte.

Avec des tâches idempotentes, la reprise est simple : réparer une exécution pour ne relancer que les tâches en échec, limiter la concurrence pour éviter les chevauchements, et faire un backfill en bouclant sur les dates.

<!-- example -->

```python
# Task parameter: process_date = {{job.start_time.iso_date}}
process_date = dbutils.widgets.get("process_date")
(daily_df.write.mode("overwrite")
   .option("replaceWhere", f"event_date = '{process_date}'")   # rerun-safe
   .saveAsTable("silver.events"))
dbutils.jobs.taskValues.set("row_count", daily_df.count())
```

#### Que sont les paramètres de job et les références de valeurs dynamiques ?

Des paramètres définis au niveau du job, transmis à toutes les tâches et modifiables à chaque exécution. Les références dynamiques comme `{{job.start_time.iso_date}}` ou `{{job.run_id}}` injectent le contexte de l'exécution, utile pour un traitement idempotent piloté par la date.

#### Comment passer des valeurs entre les tâches ?

Les petites valeurs avec les task values (`dbutils.jobs.taskValues.set` dans une tâche et `get` dans une tâche suivante, ou des références dynamiques comme `{{tasks.ingest.values.row_count}}` dans les paramètres). Les données elles-mêmes doivent passer par des tables, pas par des task values.

#### Comment rendre un job Databricks idempotent ?

En écrivant avec `MERGE` ou avec `replaceWhere`/l'écrasement dynamique de partitions pour la date traitée au lieu d'ajouts aveugles, en tirant la date de traitement d'un paramètre plutôt que de l'horloge, en utilisant des checkpoints de streaming pour l'ingestion incrémentale, et en rendant les effets de bord (notifications, exports) rejouables sans risque.

#### Comment ne relancer que la partie d'un job qui a échoué ?

Avec « Repair run », qui relance les tâches en échec et leurs dépendances en aval, en réutilisant les résultats réussis en amont, éventuellement avec de nouveaux paramètres.

#### Comment limiter les exécutions concurrentes d'un job ?

Avec le réglage du nombre maximal d'exécutions concurrentes (généralement 1 pour les jobs qui écrivent dans les mêmes tables) et l'option de file d'attente, pour qu'un nouveau déclenchement attende au lieu d'être ignoré ou exécuté en parallèle.

#### Comment être alerté quand un job échoue ou est lent ?

En configurant des notifications (e-mail, Slack, Teams, PagerDuty, webhooks) au démarrage, au succès, à l'échec et au dépassement de seuils de durée, et en fixant un timeout et un nombre maximal d'exécutions concurrentes. Les tables système sur les exécutions de jobs permettent de construire des tableaux de bord de fiabilité sur la durée.

#### Comment exécuter un job pour le backfill de nombreuses dates ?

En paramétrant le job par date et en le déclenchant pour chaque date (via l'API, la CLI ou une tâche For each sur une liste de dates), en gardant des écritures idempotentes et en limitant la concurrence pour que le backfill n'affame pas la production.

#### Un job quotidien écrit des doublons à chaque relance. Que changez-vous ?

Je remplace l'ajout par une écriture idempotente : un `MERGE` sur la clé métier, ou `replaceWhere` sur la date traitée. Je tire la date d'un paramètre du job et j'ajoute un contrôle d'unicité sur la cible.

<!-- challenge -->

Vous devez rejouer 2 ans de données quotidiennes avec un job qui traite normalement un jour. Comment le faire sans perturber la production ?

<!-- solution -->

Vérifier que le job est idempotent par date, puis lancer une tâche For each (ou des appels API) sur les 730 dates avec une concurrence limitée, sur un calcul de jobs séparé, éventuellement hors heures ouvrées. Contrôler ensuite les volumes par date.

<!-- takeaways -->

- Les écritures idempotentes (`MERGE`, `replaceWhere`) sécurisent les relances.
- Prenez la date de traitement d'un paramètre, jamais de l'horloge.
- La réparation ne relance que ce qui a échoué.

<!-- stage: Gouverner les données -->

### Unity Catalog et gouvernance

<!-- unit: Modèle d'objets et stockage -->

<!-- goals -->

- Nommer la hiérarchie d'Unity Catalog et désigner les objets par un nom à trois niveaux.
- Expliquer comment storage credentials, external locations et volumes gouvernent les fichiers.

<!-- concept -->

Unity Catalog est une couche de gouvernance unique pour tous les workspaces d'une région. Tout s'inscrit dans une hiérarchie : metastore, catalogue, schéma, puis tables, vues, volumes, fonctions et modèles, désignés par `catalog.schema.object`.

L'accès au stockage cloud est aussi gouverné. Une storage credential enveloppe une identité cloud, une external location l'associe à un chemin et les volumes exposent des fichiers sous des chemins gouvernés. Les anciens workspaces ont encore un metastore Hive, à migrer vers Unity Catalog.

<!-- example -->

```text
metastore (eu-west-1)
└── catalog: prod
    ├── schema: bronze ── table: orders
    ├── schema: gold   ── table: fct_sales, view: v_sales_eu
    └── schema: raw    ── volume: landing  → /Volumes/prod/raw/landing/
```

#### Qu'est-ce qu'Unity Catalog ?

La couche de gouvernance unifiée de Databricks pour les actifs de données et d'IA de tous les workspaces : un seul endroit pour définir le contrôle d'accès, l'audit, le lignage, la découverte et le partage des tables, vues, volumes, fonctions et modèles. Il a aussi été publié en open source.

#### Quelle est la hiérarchie des objets d'Unity Catalog ?

Metastore (un par région) → catalogue → schéma (base de données) → tables, vues, vues matérialisées, volumes, fonctions et modèles. Les objets sont désignés par un nom à trois niveaux : `catalogue.schema.table`.

#### Qu'est-ce qu'un volume ?

Un objet Unity Catalog qui gouverne l'accès à des fichiers non tabulaires (CSV, JSON, images, PDF, wheels) dans le stockage cloud, avec des chemins de la forme `/Volumes/catalogue/schema/volume/chemin`. Les volumes gérés vivent dans le stockage géré par Unity Catalog ; les volumes externes pointent vers un chemin de stockage existant.

#### Que sont les storage credentials et les external locations ?

Une storage credential encapsule une identité cloud (un rôle IAM AWS, une identité managée Azure) qui a accès au stockage. Une external location associe un chemin de stockage à une credential, et les droits sur celle-ci contrôlent qui peut y créer des tables ou des volumes externes.

#### Qu'est-ce que l'information schema dans Unity Catalog ?

Un ensemble de vues SQL standard dans chaque catalogue (`information_schema.tables`, `columns`, `table_privileges` et d'autres) qui décrivent les objets et les droits, utiles pour la documentation et les audits.

#### Qu'est-ce que l'ancien Hive metastore, et comment migrer depuis celui-ci ?

Le metastore par workspace antérieur à Unity Catalog, avec des droits locaux au workspace. La migration consiste à créer un metastore Unity Catalog, à migrer les tables (`SYNC` pour les tables externes, `CREATE TABLE … AS SELECT` ou deep clone pour les tables gérées) et à passer le code aux noms à trois niveaux. L'outil UCX automatise une grande partie de l'évaluation et de la migration.

<!-- challenge -->

Un notebook lit `hive_metastore.sales.orders` et écrit des fichiers dans `dbfs:/mnt/exports`. Listez les étapes de sa migration.

<!-- solution -->

Faire passer la table dans Unity Catalog (`SYNC` si elle est externe, deep clone ou CTAS si elle est managée), modifier le code vers le nom à trois niveaux comme `prod.sales.orders`, remplacer le mount par un volume adossé à une external location et accorder les privilèges nécessaires au service principal du job.

<!-- takeaways -->

- Tout objet a un nom à trois niveaux : `catalog.schema.object`.
- Storage credentials et external locations gouvernent l'accès aux chemins.
- Les volumes remplacent les mounts DBFS pour les fichiers.

<!-- unit: Identités et permissions -->

<!-- goals -->

- Accorder des privilèges en tenant compte de l'héritage et de la propriété.
- Exécuter la production avec des service principals et gérer les secrets en sécurité.

<!-- concept -->

Les privilèges sont accordés à des utilisateurs, groupes ou service principals et descendent la hiérarchie, mais l'utilisateur a aussi besoin de `USE CATALOG` et `USE SCHEMA` sur les parents. Les propriétaires peuvent accorder et administrer ; les objets de production doivent appartenir à des groupes, pas à des personnes.

L'automatisation tourne sous un service principal. Les secrets vivent dans des secret scopes, mais l'accès au stockage par identité est encore mieux. Les admins de compte gèrent identités et metastores ; ceux de workspace, un workspace ; le binding limite quels workspaces voient un catalogue.

<!-- example -->

```sql
GRANT USE CATALOG ON CATALOG prod TO `analysts`;
GRANT USE SCHEMA, SELECT ON SCHEMA prod.gold TO `analysts`;
ALTER TABLE prod.gold.fct_sales OWNER TO `data-platform`;
```

#### Comment accorde-t-on des droits dans Unity Catalog ?

En SQL ou via l'interface, à des utilisateurs, des groupes ou des service principals. Les privilèges se transmettent vers le bas de la hiérarchie, et un utilisateur a besoin de `USE CATALOG` et `USE SCHEMA` sur les niveaux supérieurs pour atteindre un objet.

```sql
GRANT USE CATALOG ON CATALOG prod TO `analysts`;
GRANT USE SCHEMA, SELECT ON SCHEMA prod.gold TO `analysts`;
```

#### Quelle est la différence entre la propriété et les privilèges ?

Le propriétaire d'un objet (un utilisateur, un groupe ou un service principal) peut accorder des privilèges dessus et le gérer. Les privilèges comme `SELECT`, `MODIFY`, `CREATE TABLE` ou `READ VOLUME` autorisent des actions précises. Faire d'un groupe le propriétaire des objets de production évite de dépendre d'une seule personne.

#### Quelle est la différence entre l'administration au niveau du compte et au niveau du workspace ?

Les administrateurs du compte gèrent les identités (utilisateurs, groupes, service principals, souvent synchronisés depuis un fournisseur d'identité via SCIM), les metastores, les workspaces et les réglages globaux. Les administrateurs d'un workspace gèrent les réglages, les politiques de calcul et les accès dans ce workspace.

#### Qu'est-ce qu'un service principal, et pourquoi l'utiliser pour les jobs de production ?

Une identité non humaine destinée à l'automatisation. Les jobs de production et les déploiements CI/CD devraient s'exécuter sous un service principal pour ne pas dépendre du compte et des droits d'une personne, et pour limiter l'accès à ce dont le pipeline a besoin.

#### Comment gère-t-on les secrets dans Databricks ?

Dans des secret scopes (gérés par Databricks ou adossés à Azure Key Vault), lus avec `dbutils.secrets.get(scope, key)`. Les valeurs secrètes sont masquées dans les sorties des notebooks. Pour les ressources cloud, préférez l'accès par identité (instance profiles, storage credentials) aux secrets.

#### Qu'est-ce que la liaison entre workspaces et catalogues ?

Un réglage qui limite les workspaces pouvant accéder à un catalogue, par exemple pour qu'un catalogue de production ne soit accessible que depuis le workspace de production, même si des utilisateurs ont des droits dessus.

<!-- challenge -->

Une analyste a `SELECT` sur `prod.gold.fct_sales` mais reçoit « permission denied ». Quelle est la cause probable ?

<!-- solution -->

Il lui manque `USE CATALOG` sur `prod` ou `USE SCHEMA` sur `prod.gold` ; `SELECT` seul ne suffit pas. Autre possibilité : le catalogue n'est lié qu'à d'autres workspaces.

<!-- takeaways -->

- Les droits s'héritent, mais `USE CATALOG` et `USE SCHEMA` restent nécessaires.
- Des groupes possèdent la production ; des service principals exécutent les jobs.
- Préférez l'accès par identité aux secrets.

<!-- unit: Accès fin -->

<!-- goals -->

- Restreindre lignes et colonnes sans copier les tables.
- Comparer row filters et column masks aux vues dynamiques.

<!-- concept -->

Les droits au niveau table sont souvent trop grossiers : une équipe ne doit voir que son pays, une autre que des e-mails masqués. Row filters et column masks sont des fonctions attachées à la table et évaluées à la requête pour l'utilisateur courant : une seule table, plusieurs vues. Les vues dynamiques obtiennent le même résultat avec `current_user()` ou des tests de groupe, et étaient l'approche habituelle auparavant.

<!-- example -->

```sql
CREATE FUNCTION gov.country_filter(country STRING)
RETURN is_account_group_member('admins')
    OR is_account_group_member(concat('analysts_', lower(country)));

ALTER TABLE prod.gold.sales SET ROW FILTER gov.country_filter ON (country);
```

#### Que sont les row filters et les column masks ?

Des fonctions attachées à une table et évaluées au moment de la requête. Un row filter détermine les lignes qu'un utilisateur peut voir (par exemple seulement celles de son pays) ; un column mask renvoie la valeur ou une version masquée selon les groupes de l'utilisateur. Les données restent dans une seule table au lieu de multiples copies filtrées.

#### Que sont les vues dynamiques ?

Des vues qui utilisent des fonctions comme `current_user()` ou `is_account_group_member()` pour filtrer des lignes ou masquer des colonnes. C'était l'approche habituelle avant l'arrivée des row filters et des column masks.

#### Les analystes ne doivent voir que les lignes de leur pays dans une table partagée. Comment l'implémentez-vous ?

J'attache à la table une fonction de row filter Unity Catalog qui compare l'appartenance de l'utilisateur à des groupes avec la colonne pays. J'accorde `SELECT` aux groupes d'analystes. J'utilise des column masks pour les colonnes sensibles.

<!-- challenge -->

Les agents du support doivent voir les lignes clients mais seulement les quatre derniers chiffres du téléphone ; l'équipe fraude doit voir le numéro complet. Écrivez l'idée du masque.

<!-- solution -->

Une fonction de column mask sur `phone` : si l'utilisateur est dans le groupe fraude, renvoyer la valeur ; sinon `concat('***', right(phone, 4))`. On l'attache avec `ALTER TABLE ... ALTER COLUMN phone SET MASK`.

<!-- takeaways -->

- Row filters et column masks s'exécutent par utilisateur à la requête.
- Une table avec des politiques vaut mieux que plusieurs copies filtrées.
- Basez les politiques sur des groupes, pas sur des individus.

<!-- unit: Découverte, lignage et partage -->

<!-- goals -->

- Utiliser lignage, tables système, tags et commentaires pour comprendre les données.
- Partager ou interroger des données entre organisations et systèmes sans les copier.

<!-- concept -->

Gouverner, c'est aussi savoir ce qui existe et comment tout est relié. Unity Catalog enregistre automatiquement le lignage au niveau table et colonne, les tables système exposent usage, audit et facturation en SQL, et commentaires et tags rendent les données trouvables et classables.

Les données doivent souvent franchir des frontières. Delta Sharing donne à d'autres organisations un accès en direct et en lecture seule sans copie ; Lakehouse Federation interroge des bases externes sur place.

<!-- example -->

```sql
-- Who reads the table we want to change?
SELECT DISTINCT entity_type, entity_id, created_by
FROM system.access.table_lineage
WHERE source_table_full_name = 'prod.silver.customers'
  AND event_date >= current_date() - 30;
```

#### Quel lignage Unity Catalog capture-t-il ?

Le lignage au niveau table et colonne des requêtes exécutées sur le calcul Databricks, à travers notebooks, jobs, pipelines et dashboards, visible dans Catalog Explorer et interrogeable dans les tables système. Il répond à « qu'est-ce qui casse si je modifie cette colonne ? » et « d'où vient ce chiffre ? ».

#### Que sont les tables système ?

Des tables en lecture seule du catalogue `system` contenant des données d'exploitation : consommation facturée (`system.billing.usage`), journaux d'audit, lignage des tables, exécutions de jobs, événements de clusters, historique des requêtes, etc. Elles sont la base des tableaux de bord de coûts et de l'audit.

#### À quoi servent les tags et les commentaires dans Unity Catalog ?

Les commentaires documentent tables et colonnes (et alimentent les descriptions générées par l'IA et la recherche) ; les tags (paires clé-valeur) classent les objets, par exemple `pii=true`, ce qui peut piloter des politiques, la découverte et les audits.

#### Comment découvrir des données dans Unity Catalog ?

Avec Catalog Explorer et la recherche, qui s'appuient sur les noms, les commentaires, les tags et le lignage, ainsi que sur des signaux de popularité comme les utilisateurs et requêtes fréquents. De bons commentaires et tags améliorent beaucoup la découverte.

#### Qu'est-ce que Delta Sharing ?

Un protocole ouvert pour partager des données vivantes en toute sécurité entre organisations et plateformes, sans les copier. Le fournisseur crée un share de tables, vues ou volumes ; les destinataires le lisent depuis Databricks ou depuis des clients open source (pandas, Spark, outils BI). Le partage entre comptes Databricks utilise les identités Unity Catalog.

#### Qu'est-ce que Lakehouse Federation ?

La fédération de requêtes qui permet à Unity Catalog d'enregistrer des bases externes (PostgreSQL, MySQL, SQL Server, Snowflake, Redshift, BigQuery et d'autres) comme catalogues étrangers, pour les interroger sur place avec gouvernance et lignage, sans d'abord ingérer les données.

#### Comment partager des tables gold avec une entreprise partenaire qui n'utilise pas Databricks ?

Avec Delta Sharing ouvert : je crée un share contenant les tables, un destinataire avec une credential par jeton, et le partenaire le lit depuis pandas, Spark ou un outil de BI. L'accès peut être révoqué à tout moment et il est audité.

<!-- challenge -->

Vous comptez renommer une colonne de `silver.customers`. Comment savoir ce qui va casser et qui prévenir ?

<!-- solution -->

Consulter le lignage par colonne dans Catalog Explorer (ou `system.access.column_lineage`) pour les tables, jobs, tableaux de bord et notebooks en aval, et l'historique des requêtes ou l'audit pour les lecteurs directs. Prévenir les propriétaires et envisager de garder l'ancien nom dans une vue pendant la transition.

<!-- takeaways -->

- Le lignage répond à « qu'est-ce qui casse si je change ceci ? ».
- Les tables système transforment usage, audit et facturation en SQL.
- Delta Sharing partage sans copie ; Federation interroge sans ingérer.

<!-- stage: Exploiter efficacement -->

### Spark et performances sur Databricks

<!-- unit: Plans et shuffles -->

<!-- goals -->

- Lire un plan de requête et repérer les étapes coûteuses.
- Expliquer shuffles, AQE et nombre de partitions.

<!-- concept -->

Spark transforme votre code en plan de stages séparés par des shuffles, quand les données traversent le réseau pour une jointure, un `groupBy` ou un `distinct`. Les étapes narrow sont bon marché ; les shuffles dominent le coût. Le travail de performance commence donc par lire le plan de bas en haut : ce qui est scanné, ce qui est poussé vers la source, où sont les exchanges et quelle stratégie de jointure est utilisée.

Adaptive Query Execution ajuste le plan à l'exécution, fusionnant les petites partitions et changeant les jointures. Reste à bien choisir les partitions et `repartition` ou `coalesce`.

<!-- example -->

```text
== Physical Plan (simplified, read bottom-up) ==
HashAggregate(keys=[country])
+- Exchange hashpartitioning(country, 200)          ← shuffle
   +- HashAggregate(keys=[country])                 ← partial aggregation
      +- Scan delta silver.orders
         PushedFilters: [order_date >= 2026-10-01]   ← pruning works
```

#### Quelle est la différence entre transformations narrow et wide ?

Les transformations narrow (`filter`, `select`, `withColumn`) calculent chaque partition de sortie à partir d'une seule partition d'entrée, sans déplacer de données. Les transformations wide (`groupBy`, `join`, `distinct`, `orderBy`) exigent un shuffle sur le réseau. L'optimisation des performances porte surtout sur les shuffles.

#### Comment lire un plan de requête Spark ?

Avec `df.explain(mode="formatted")` ou l'onglet SQL de la Spark UI. On le lit de bas en haut : lectures (vérifiez les filtres poussés et les fichiers écartés), exchanges (shuffles), stratégies de jointure (broadcast, sort-merge) et agrégations. Le profil de requête de Databricks SQL montre la même chose avec les durées.

#### Qu'est-ce que l'Adaptive Query Execution ?

Une fonction de Spark, activée par défaut, qui réoptimise une requête entre les stages grâce aux statistiques d'exécution : elle fusionne les petites partitions de shuffle, transforme les jointures sort-merge en jointures broadcast quand un côté s'avère petit, et découpe les partitions déséquilibrées.

#### Comment choisir le nombre de partitions de shuffle ?

`spark.sql.shuffle.partitions` vaut 200 par défaut. Avec AQE, fixez un nombre généreux (ou `auto` sur Databricks) et laissez AQE fusionner. Visez des partitions d'environ 100 à 200 Mo après le shuffle ; trop peu provoque du spill, trop crée de la surcharge.

#### Quelle est la différence entre `repartition` et `coalesce` ?

`repartition(n)` fait un shuffle complet et peut augmenter ou diminuer le nombre de partitions, éventuellement par colonnes. `coalesce(n)` se contente de fusionner des partitions sans shuffle complet : c'est moins coûteux, mais cela ne peut que réduire leur nombre et peut laisser des partitions inégales. `coalesce(1)` fait tout passer par une seule tâche.

<!-- challenge -->

Un job se termine par `.coalesce(1).write...` pour produire un seul fichier, et le dernier stage dure 25 minutes sur un cluster de 40 nœuds. Pourquoi, et que faites-vous ?

<!-- solution -->

`coalesce(1)` fait passer tout le calcul final par une seule tâche : 39 nœuds attendent. Écrivez normalement et laissez les consommateurs lire la table, ou, si un fichier unique est vraiment nécessaire, écrivez un petit résultat agrégé ou utilisez `repartition(1)` après le travail lourd pour garder les stages précédents parallèles.

<!-- takeaways -->

- Les shuffles sont le coût principal ; cherchez les exchanges dans le plan.
- AQE ajuste partitions et jointures à l'exécution.
- `coalesce` fusionne sans shuffle mais peut tuer le parallélisme.

<!-- unit: Jointures, skew et spill -->

<!-- goals -->

- Choisir les broadcast joins et corriger le skew.
- Reconnaître le spill et ses remèdes.

<!-- concept -->

Les jointures sont là où les jobs lents font le plus mal. Si un côté est petit, le diffuser (broadcast) évite de déplacer le gros côté. Si les clés sont mal réparties, quelques tâches reçoivent presque tout (skew) et le stage les attend. Si les données d'une tâche ne tiennent pas en mémoire, Spark les déverse sur disque (spill).

Les trois se voient dans la Spark UI : stratégie de jointure dans le plan, durée médiane contre maximale des tâches, colonnes de spill.

<!-- example -->

```python
from pyspark.sql.functions import broadcast
facts.join(broadcast(dim_store), "store_id")      # 50 MB dimension: no shuffle of facts
```
Résumé de stage qui signale un skew : tâche médiane 8 s, tâche maximale 14 min.

#### Qu'est-ce qu'une jointure broadcast, et quand aide-t-elle ?

Spark envoie une copie de la petite table à chaque executor, de sorte que la grande table est jointe sans être redistribuée. Elle aide quand un côté est assez petit (quelques dizaines de Mo par défaut, plus avec des hints). Diffuser une table trop grande provoque des erreurs de mémoire sur le driver ou les executors.

#### Qu'est-ce que le déséquilibre des données (skew), et comment le corriger ?

Certaines clés ont beaucoup plus de lignes que d'autres, si bien que quelques tâches durent bien plus longtemps que les autres. Solutions : laisser AQE découper les partitions déséquilibrées, diffuser le petit côté, filtrer ou traiter à part les clés chaudes (souvent les nulls), ou saler la clé pour la répartir sur plusieurs partitions.

#### Qu'est-ce que le spill, et pourquoi est-il lent ?

Quand les données d'une tâche ne tiennent pas en mémoire d'exécution, Spark les écrit sur le disque local puis les relit. Cela apparaît dans la Spark UI comme spill (memory) et spill (disk). On le corrige avec des partitions plus nombreuses et plus petites, des workers plus gros ou optimisés pour la mémoire, ou moins de données par tâche.

#### Une jointure entre une table de faits de 2 To et une dimension de 50 Mo est lente. Que vérifiez-vous ?

Si elle est diffusée en broadcast (vérifier le plan ; ajouter un hint de broadcast ou relever le seuil), si la lecture des faits écarte des fichiers (filtres sur des colonnes regroupées), le déséquilibre sur la clé de jointure et le spill. Une dimension de 50 Mo devrait presque toujours être diffusée.

#### Comment diagnostiquer un job devenu soudain plus lent ?

En comparant l'exécution lente avec une exécution normale : volumes en entrée, nombre de fichiers (petits fichiers, `OPTIMIZE` manquant), changements de plan (un broadcast devenu sort-merge), déséquilibre dans un stage, spill, taille du cluster ou perte d'instances spot, et changements de code ou de données depuis la dernière bonne exécution.

<!-- challenge -->

Une jointure sur `customer_id` a une tâche qui tourne 20 minutes quand les autres finissent en secondes. La clé la plus fréquente est `NULL`. Que faites-vous ?

<!-- solution -->

Les lignes à clé nulle ne peuvent jamais correspondre dans une jointure interne : filtrez-les avant la jointure (ou traitez-les à part pour une jointure externe). S'il reste d'autres clés chaudes, comptez sur la gestion du skew par AQE ou appliquez un salting.

<!-- takeaways -->

- Diffusez les petites dimensions ; vérifiez-le dans le plan.
- Le skew se voit comme une longue traîne de durées ; les nulls sont une clé chaude fréquente.
- Le spill signifie trop de données par tâche : plus de partitions ou plus de mémoire.

<!-- unit: Écrire du code efficace -->

<!-- goals -->

- Éviter les patrons de code qui ralentissent Spark.
- N'utiliser le cache que là où il aide.

<!-- concept -->

Une partie de la lenteur vient du code, pas des données. Les UDF Python font transiter chaque ligne entre la JVM et Python et cachent la logique à l'optimiseur ; les fonctions natives sont bien plus rapides. Construire un plan avec `withColumn` en boucle ralentit l'analyse, et appeler `count()` après chaque étape recalcule tout à chaque fois.

Le cache n'est pas un remède général : sur Databricks, le disk cache accélère déjà les lectures répétées, le serverless ne prend pas en charge `cache()` et la réutilisation entre jobs passe par une table.

<!-- example -->

```python
# Slow: Python UDF, row by row
@udf("string")
def clean(s): return s.strip().upper()
df.withColumn("code", clean("code"))

# Fast: built-in functions, optimized and Photon-friendly
from pyspark.sql import functions as F
df.withColumn("code", F.upper(F.trim("code")))
```

#### Pourquoi les UDF Python sont-elles lentes, et quelles sont les alternatives ?

Chaque ligne est sérialisée entre la JVM et un worker Python, et l'optimiseur ne voit pas l'intérieur de la fonction. Utilisez d'abord les fonctions intégrées, puis les UDF pandas (vectorisées) avec Arrow, ou des UDF SQL. Photon ne peut pas non plus accélérer les UDF Python.

#### Pourquoi `withColumn` dans une boucle pose-t-il problème ?

Chaque appel ajoute une projection au plan logique, et l'analyse d'un plan très profond devient lente (elle peut prendre des minutes avant de traiter la moindre donnée). Utilisez un seul `select` ou `withColumns` avec un dictionnaire.

#### Pourquoi un `count()` avant chaque étape ralentit-il un job ?

Chaque action déclenche l'exécution complète du plan jusqu'à ce point. Compter pour les logs après chaque transformation recalcule les données encore et encore. Récupérez les métriques du commit Delta (`numOutputRows` dans l'historique) ou calculez-les une seule fois.

#### Faut-il utiliser `cache()` sur Databricks ?

Avec parcimonie. Le cache aide quand le même DataFrame est réutilisé plusieurs fois dans une session interactive, mais il consomme de la mémoire et n'est pas pris en charge en serverless. Le disk cache (cache automatique sur SSD des fichiers Parquet distants sur certains types d'instance) apporte souvent le gain sans changer le code. Pour réutiliser entre jobs, écrivez une table.

#### Qu'est-ce que le disk cache ?

Un cache automatique, anciennement appelé Delta cache, qui stocke des copies des fichiers Parquet et Delta distants sur les SSD locaux des workers, pour accélérer les lectures répétées des mêmes données. Il est géré de façon transparente.

<!-- challenge -->

Un notebook renomme 300 colonnes avec une boucle `for` de `withColumnRenamed` et met 6 minutes avant de lancer le moindre job. Corrigez-le.

<!-- solution -->

Construire toutes les expressions d'un coup et appliquer un seul `select` : `df.select([F.col(c).alias(new_names[c]) for c in df.columns])`, ou `withColumnsRenamed` avec un dictionnaire. Le plan reste peu profond et l'analyse prend quelques secondes.

<!-- takeaways -->

- Préférez les fonctions natives aux UDF Python.
- Construisez les transformations larges en un seul `select`, pas en boucle.
- Cachez rarement ; écrivez des tables pour réutiliser entre jobs.

<!-- unit: Élagage, statistiques et coût des jobs -->

<!-- goals -->

- Faire lire moins de données aux requêtes grâce à l'élagage et aux statistiques.
- Réduire le coût d'un job lourd.

<!-- concept -->

Les données les moins chères sont celles qu'on ne lit pas. L'élagage de partitions saute des répertoires, celui de fichiers saute des fichiers grâce aux statistiques Delta ; les deux exigent des filtres alignés sur l'organisation de la table. Les statistiques de colonnes aident l'optimiseur à choisir les jointures, et l'optimisation prédictive entretient organisation et statistiques des tables managées.

Le coût en découle : traitement incrémental plutôt que recalcul complet, lectures élaguées, bon type et bonne taille de calcul, et suivi via les tables de facturation.

<!-- example -->

```sql
-- Prunes files: filter on the clustering column
SELECT sum(amount) FROM silver.events WHERE event_date = '2026-10-15';
-- Can't prune: function applied to the column
SELECT sum(amount) FROM silver.events WHERE date_format(event_date, 'yyyy-MM') = '2026-10';
```

#### En quoi l'élagage de fichiers diffère-t-il de l'élagage de partitions ?

L'élagage de partitions (partition pruning) ignore des répertoires entiers selon les colonnes de partitionnement. L'élagage de fichiers (data skipping) ignore des fichiers individuels grâce aux statistiques min/max du journal Delta : il fonctionne sur toute colonne dotée de statistiques et profite du clustering.

#### Que sont les statistiques de colonnes, et pourquoi les calculer ?

`ANALYZE TABLE … COMPUTE STATISTICS FOR ALL COLUMNS` stocke le nombre de lignes et les statistiques des colonnes que l'optimiseur basé sur les coûts utilise pour choisir l'ordre et la stratégie des jointures. L'optimisation prédictive peut les maintenir automatiquement.

#### Qu'est-ce que l'optimisation prédictive ?

Une fonction d'Unity Catalog qui lance automatiquement `OPTIMIZE`, `VACUUM` et la collecte de statistiques sur les tables gérées quand elle en prévoit un bénéfice, pour vous éviter de planifier des jobs de maintenance.

#### Qu'est-ce que `replaceWhere` ?

Une option d'écriture qui remplace de façon atomique uniquement les lignes qui satisfont un prédicat, généralement une plage de dates, sans toucher au reste de la table. Elle rend idempotent le retraitement d'une période.

```python
(df.write.format("delta").mode("overwrite")
   .option("replaceWhere", "event_date = '2026-10-15'")
   .saveAsTable("silver.events"))
```

#### Comment réduire le coût d'un job Databricks lourd ?

En utilisant du calcul de jobs ou serverless au lieu de clusters all-purpose, en activant Photon quand il est rentable, en traitant de façon incrémentale plutôt que de tout recalculer, en réduisant les lectures grâce au clustering et aux filtres, en dimensionnant et en autoscalant correctement les clusters, en utilisant des workers spot, en évitant les shuffles inutiles et les UDF Python, et en surveillant `system.billing.usage`.

<!-- challenge -->

Un job quotidien recalcule chaque nuit trois ans de ventes dans une table gold, alors que seules les données de la veille changent. Esquissez une conception moins chère.

<!-- solution -->

Ne traiter que la plage modifiée : lire les nouvelles lignes silver (CDF ou filtre de date), recalculer les jours touchés et écrire avec `replaceWhere` sur ces dates (ou un `MERGE`). L'exécuter sur du calcul de jobs ou serverless et garder la table gold regroupée par date.

<!-- takeaways -->

- Pour élaguer, les filtres doivent suivre l'organisation, sans fonction sur la colonne.
- L'optimisation prédictive entretient les tables managées pour vous.
- Le traitement incrémental est le premier levier de coût.

### Sécurité, coûts et exploitation

<!-- unit: Sécurité et audit -->

<!-- goals -->

- Décrire l'accès sécurisé au stockage cloud et les options réseau.
- Retrouver qui a accédé à quoi.

<!-- concept -->

La sécurité sur Databricks repose sur des identités, pas sur des clés. L'accès au stockage passe par des rôles IAM enveloppés dans des storage credentials, jamais par des clés d'accès dans le code. Le réseau peut être verrouillé avec votre propre VPC, une connectivité privée, des listes d'IP et des politiques de sortie pour le serverless.

Tout est tracé : journaux d'audit dans `system.access.audit`, historique des requêtes et lignage disent qui a fait quoi et quand.

<!-- example -->

```sql
SELECT event_time, user_identity.email, action_name, request_params.full_name_arg
FROM system.access.audit
WHERE service_name = 'unityCatalog'
  AND request_params.full_name_arg = 'prod.silver.customers'
  AND event_date >= current_date() - 7;
```

#### Comment Databricks accède-t-il de façon sécurisée aux données sur AWS S3 ?

Par des rôles IAM : dans Unity Catalog, une storage credential encapsule un rôle IAM qui fait confiance à Databricks, et des external locations donnent accès aux chemins. Les anciennes installations utilisaient des instance profiles attachés aux clusters. Il faut éviter les clés d'accès dans le code.

#### Quelles options de sécurité réseau existent ?

Déployer le calcul classique dans votre propre VPC/VNet, la connectivité privée entre plan de contrôle et plan de calcul (PrivateLink, Private Link), les listes d'IP autorisées, des nœuds sans IP publique, des politiques réseau serverless pour contrôler les sorties, et des clés gérées par le client pour le chiffrement.

#### Comment auditer qui a accédé à quoi ?

Avec les journaux d'audit (disponibles dans la table `system.access.audit`), le lignage d'Unity Catalog et l'historique des requêtes. Ils enregistrent les connexions, les changements de droits, l'accès aux données et les actions sur les jobs.

<!-- challenge -->

Une revue de sécurité trouve une clé d'accès AWS écrite en dur dans un notebook. Par quoi la remplacez-vous, et que faites-vous d'autre ?

<!-- solution -->

La remplacer par une storage credential Unity Catalog (rôle IAM) et une external location ou un volume pour le chemin, sans clé. Désactiver la clé exposée, vérifier l'audit et CloudTrail à la recherche d'abus, et analyser les autres notebooks et dépôts.

<!-- takeaways -->

- Accédez au stockage par rôles et storage credentials, jamais par des clés dans le code.
- Réseau privé et contrôles de sortie limitent l'exposition.
- Les journaux d'audit sont des tables système interrogeables.

<!-- unit: Surveiller la facture -->

<!-- goals -->

- Décomposer les dépenses Databricks et en trouver les causes.
- Attribuer les coûts aux équipes avec tags et tables système.

<!-- concept -->

Les dépenses se lisent dans `system.billing.usage` : DBU par SKU, workspace, job, warehouse et tag, à joindre aux prix catalogue. Les tags sur le calcul permettent d'attribuer les coûts aux équipes. Les coupables sont toujours les mêmes : clusters qui ne s'arrêtent jamais, production sur du calcul all-purpose, recalculs complets et relances incontrôlées.

<!-- example -->

```sql
SELECT usage_metadata.job_id, sku_name, sum(usage_quantity) AS dbus
FROM system.billing.usage
WHERE usage_date >= date_trunc('month', current_date())
GROUP BY ALL ORDER BY dbus DESC LIMIT 10;
```

#### Comment surveiller et maîtriser les dépenses Databricks ?

En taguant clusters, jobs et warehouses par centre de coût, en interrogeant `system.billing.usage` joint aux prix catalogue, en définissant budgets et alertes, en imposant des politiques de cluster (types d'instance, arrêt automatique, nombre maximal de workers), en utilisant le serverless ou le calcul de jobs en production, et en revoyant régulièrement les jobs les plus coûteux.

#### La facture mensuelle Databricks a doublé. Comment enquêtez-vous ?

J'interroge `system.billing.usage` par SKU, workspace, job, warehouse et tag, et je compare les mois. Je cherche les clusters all-purpose sans arrêt automatique, les jobs passés sur du calcul all-purpose, les warehouses qui ne s'arrêtent jamais, les full refreshes, les nouvelles charges serverless et les relances incontrôlées.

<!-- challenge -->

Écrivez les deux premières requêtes que vous lancez quand la finance demande pourquoi le mois dernier a coûté 40 % de plus.

<!-- solution -->

D'abord les DBU (ou le coût) par SKU ce mois-ci contre le mois précédent, pour voir quel produit a augmenté. Ensuite, dans ce SKU, les jobs, warehouses ou clusters les plus consommateurs sur les deux mois, pour trouver la charge qui a changé.

<!-- takeaways -->

- `system.billing.usage` est la source de vérité des dépenses.
- Les tags rendent les coûts attribuables aux équipes et projets.
- Comparez d'abord par SKU, puis par charge.

<!-- unit: Déployer avec des bundles et la CI/CD -->

<!-- goals -->

- Décrire un projet Databricks sous forme de code avec les Asset Bundles.
- Mettre en place tests et déploiement par CI/CD.

<!-- concept -->

Les pipelines de production se déploient, ils ne s'assemblent pas à la souris. Les Databricks Asset Bundles décrivent jobs, pipelines et réglages en YAML à côté du code, avec une cible par environnement. Les cibles de développement préfixent les ressources par utilisateur et mettent les calendriers en pause ; celles de production tournent sous un service principal.

Un pipeline de CI valide ensuite le bundle, lance des tests unitaires sur des fonctions de transformation pures, déploie en staging pour les tests d'intégration et promeut en production après approbation.

<!-- example -->

```text
pull request ──► lint + pytest (local Spark) ──► bundle validate
merge to main ──► deploy -t staging ──► integration run ──► approval ──► deploy -t prod
```

#### Que sont les Databricks Asset Bundles ?

Une façon de décrire les ressources Databricks (jobs, pipelines, dashboards, modèles, droits) en YAML à côté du code dans Git, avec des targets pour chaque environnement. La CLI les valide, les déploie et les exécute, ce qui rend les projets Databricks déployables en CI/CD.

```yaml
bundle:
  name: sales_pipeline
targets:
  dev:
    mode: development
    default: true
  prod:
    mode: production
resources:
  jobs:
    daily_sales:
      name: daily_sales
      tasks:
        - task_key: build
          notebook_task:
            notebook_path: ./src/build_sales.py
```

#### Que change `mode: development` dans un target de bundle ?

Il préfixe les ressources déployées avec le nom de l'utilisateur, met en pause les planifications et les déclencheurs, et déploie dans un dossier propre à l'utilisateur, pour que plusieurs développeurs puissent déployer le même bundle sans se gêner. `mode: production` vérifie que le déploiement s'exécute sous un service principal (ou une identité fixée) et n'utilise pas ces raccourcis.

#### Comment mettre en place la CI/CD pour Databricks ?

En gardant le code et les définitions du bundle dans Git, en lançant les tests unitaires (avec Spark en local ou Databricks Connect) et le linting sur les pull requests, en validant le bundle, en déployant sur un target de staging pour lancer les tests d'intégration, puis en déployant en production après approbation, le tout sous un service principal authentifié par OAuth ou par fédération d'identité de charge de travail.

#### Comment tester du code PySpark destiné à Databricks ?

En isolant les transformations dans des fonctions pures qui prennent et renvoient des DataFrames, en les testant avec pytest sur une SparkSession locale et de petits jeux de données (comparés avec `assertDataFrameEqual`), en ajoutant des tests de bout en bout sur des données synthétiques, et en lançant des contrôles de qualité (expectations, contraintes) dans le pipeline lui-même.

<!-- challenge -->

Deux développeurs déploient le même bundle dans le workspace de développement et écrasent mutuellement leur job. Que manque-t-il ?

<!-- solution -->

La cible de développement doit utiliser `mode: development`, qui préfixe les ressources du nom de chaque utilisateur et déploie dans un dossier par utilisateur : leurs copies ne se heurtent plus.

<!-- takeaways -->

- Les bundles gardent jobs et pipelines en code, par environnement.
- Le mode développement isole le déploiement de chaque développeur.
- Testez les fonctions pures en local ; déployez en staging avant la production.

<!-- stage: Servir et appliquer -->

### Databricks SQL et analytique

<!-- unit: Entrepôt de données et BI -->

<!-- goals -->

- Expliquer comment les outils de BI interrogent Databricks et ce qui les accélère.
- Choisir entre vues, vues matérialisées et fédération.

<!-- concept -->

Databricks SQL fait du lakehouse un entrepôt pour les analystes : les SQL warehouses exécutent les requêtes de l'éditeur, des tableaux de bord et des outils de BI via JDBC/ODBC, avec les permissions Unity Catalog de chaque utilisateur. Les requêtes répétées profitent du cache de résultats.

La façon d'exposer les données influe sur le coût : une vue réexécute sa requête à chaque fois, une vue matérialisée stocke les résultats et se rafraîchit, et la fédération interroge une base externe sur place, bien pour explorer mais lente en usage intensif.

<!-- example -->

```sql
CREATE MATERIALIZED VIEW gold.mv_sales_by_month
SCHEDULE CRON '0 0 6 * * ?'
AS SELECT date_trunc('month', order_date) AS month, region, sum(amount) AS sales
FROM silver.orders GROUP BY ALL;
```

#### Qu'est-ce que Databricks SQL ?

La partie entrepôt SQL de la plateforme : SQL warehouses, éditeur SQL, historique et profils de requêtes, alertes, dashboards et connecteurs pour les outils de BI (Power BI, Tableau, Looker) via JDBC/ODBC.

#### Comment les outils de BI se connectent-ils à Databricks ?

Via des pilotes JDBC/ODBC ou des connecteurs natifs (Power BI, Tableau, Looker, Excel) pointant vers un SQL warehouse, avec une authentification OAuth ou par jeton. Unity Catalog applique les droits de l'identité connectée.

#### Qu'est-ce que le cache de résultats de Databricks SQL ?

Un cache des résultats de requêtes sur les SQL warehouses : quand la même requête est relancée et que les tables n'ont pas changé, le résultat est renvoyé sans recalcul.

#### Quelle est la différence entre une vue, une vue temporaire et une vue matérialisée ?

Une vue ne stocke que la requête et l'exécute à chaque lecture. Une vue temporaire n'existe que dans la session courante. Une vue matérialisée stocke des résultats précalculés et doit être rafraîchie.

#### Qu'est-ce qu'une vue matérialisée dans Databricks SQL ?

Une vue dont les résultats sont stockés et rafraîchis (selon un planning ou à la demande, de façon incrémentale quand c'est possible). Elle accélère les agrégations coûteuses des dashboards. On la crée avec `CREATE MATERIALIZED VIEW` et elle tourne sur des pipelines serverless.

#### À quoi sert la fédération de requêtes en analytique ?

À joindre des tables Databricks avec des tables encore dans une base opérationnelle ou un autre entrepôt, pour l'exploration ou une migration, sans construire d'abord une ingestion. Pour un usage intensif et répété, ingérer les données est plus rapide et moins cher.

<!-- challenge -->

Un rapport Power BI lance une agrégation lourde sur 2 milliards de lignes à chaque ouverture ; les données changent une fois par jour. Que changez-vous ?

<!-- solution -->

Précalculer l'agrégation en vue matérialisée (ou table gold) rafraîchie après le chargement quotidien et y brancher le rapport. Les requêtes lisent alors une petite table, et le cache de résultats aide aux ouvertures répétées.

<!-- takeaways -->

- Les outils de BI se connectent aux SQL warehouses avec les permissions Unity Catalog de chaque utilisateur.
- Les vues matérialisées précalculent les agrégations coûteuses.
- La fédération sert à explorer ; ingérez pour un usage intensif et répété.

<!-- unit: Tableaux de bord, métriques et applications -->

<!-- goals -->

- Décrire tableaux de bord, Genie, metric views et alertes.
- Savoir quand Databricks Apps et Lakebase conviennent.

<!-- concept -->

Au-dessus des warehouses, Databricks propose des tableaux de bord AI/BI, Genie pour les questions en langage naturel et des alertes SQL qui préviennent selon des conditions. Les metric views définissent les mesures une fois pour que tous les outils calculent le « chiffre d'affaires » de la même façon.

Pour les applications interactives, Databricks Apps héberge des applications web dans le workspace, et Lakebase fournit une base compatible Postgres pour des besoins transactionnels à faible latence que les tables analytiques servent mal.

<!-- example -->

Une alerte de qualité : planifiez cette requête toutes les heures et prévenez quand `bad_rows > 0`.
```sql
SELECT count(*) AS bad_rows FROM silver.orders
WHERE amount < 0 AND order_date = current_date();
```

#### Que sont les dashboards AI/BI et Genie ?

Les dashboards AI/BI sont les tableaux de bord actuels de Databricks, construits sur des SQL warehouses avec une aide de l'IA à la création. Genie est une interface en langage naturel où les utilisateurs métier posent des questions sur des tables sélectionnées et obtiennent des réponses appuyées sur du SQL.

#### Qu'est-ce qu'une metric view ?

Un objet Unity Catalog qui définit une seule fois en YAML les indicateurs métier (mesures et dimensions) au-dessus d'une table, pour que les dashboards, Genie et les utilisateurs SQL les calculent de façon cohérente.

#### Que sont les alertes SQL ?

Des requêtes planifiées qui comparent un résultat à un seuil et notifient (e-mail, Slack, webhook) quand la condition est remplie, par exemple quand un contrôle de qualité renvoie des lignes.

#### Que sont les Databricks Apps ?

Un moyen de construire et d'héberger des applications de données et d'IA (Streamlit, Dash, Gradio, Flask et d'autres) directement dans le workspace, avec authentification et accès aux données gouvernées via Unity Catalog.

#### Qu'est-ce que Lakebase ?

Une base de données opérationnelle gérée, compatible PostgreSQL, intégrée à Databricks et fondée sur Postgres serverless, destinée aux charges transactionnelles à faible latence (applications, service de features) synchronisées avec les tables du lakehouse.

<!-- challenge -->

Trois tableaux de bord affichent trois chiffres différents de « clients actifs ». Comment régler le problème durablement ?

<!-- solution -->

S'accorder sur une définition avec les responsables métier, la définir une fois en metric view (ou table gold documentée) et reconstruire les tableaux de bord dessus, pour que la définition ne puisse plus diverger.

<!-- takeaways -->

- Définissez les métriques métier une fois, dans une metric view.
- Les alertes SQL transforment des requêtes en surveillance.
- Apps et Lakebase répondent aux besoins interactifs et transactionnels.

### Machine learning et IA

<!-- unit: Modèles et features -->

<!-- goals -->

- Décrire le cycle de vie ML sur Databricks avec MLflow et Unity Catalog.
- Expliquer pourquoi les tables de features gardent entraînement et inférence cohérents.

<!-- concept -->

Un modèle ne vaut que par son historique. MLflow enregistre chaque entraînement (paramètres, métriques, artefacts) pour comparer les essais et empaqueter le meilleur. L'enregistrer dans Unity Catalog en fait un objet gouverné avec versions, alias comme `champion`, permissions et lignage jusqu'aux tables d'entraînement.

Les features exigent la même rigueur. Une table de features indexée par entité et par temps est calculée une fois et réutilisée : jeux d'entraînement et prédictions en direct lisent les mêmes définitions au lieu de deux copies de la logique.

<!-- example -->

```python
import mlflow
mlflow.set_registry_uri("databricks-uc")
with mlflow.start_run():
    model = train(features_df)
    mlflow.sklearn.log_model(model, "model", registered_model_name="ml.churn.churn_model")
```

#### Qu'est-ce que MLflow ?

Une plateforme open source, créée par Databricks, pour le cycle de vie du ML : suivi des expériences (paramètres, métriques, artefacts), packaging des modèles, registre de modèles avec versions et alias, évaluation, et traces pour les applications d'IA générative. Sur Databricks, il est géré et intégré à Unity Catalog.

#### Que signifie enregistrer un modèle dans Unity Catalog ?

Les modèles sont stockés comme objets Unity Catalog (`catalogue.schema.modele`) avec des versions et des alias comme `champion`, gouvernés par les mêmes droits et le même lignage que les tables, et utilisables depuis plusieurs workspaces.

#### Qu'est-ce qu'une table de features ?

Une table Delta avec clé primaire servant à stocker des features de ML dans Unity Catalog. Les jeux d'entraînement sont construits en joignant les tables de features aux étiquettes (avec une jointure point-in-time pour les séries temporelles), et les mêmes features peuvent être servies en ligne pour l'inférence.

<!-- challenge -->

Un modèle entraîné le trimestre dernier est moins bon en production qu'en test. Ses features sont calculées par un code différent pour l'entraînement et le service. Que changez-vous ?

<!-- solution -->

Déplacer les features dans des tables de features construites une fois depuis silver, utiliser des jointures point-in-time pour les jeux d'entraînement et servir les mêmes features en ligne, pour que entraînement et inférence ne divergent plus. Puis réentraîner et comparer les versions dans MLflow.

<!-- takeaways -->

- MLflow suit les entraînements ; Unity Catalog versionne et gouverne les modèles.
- Des alias comme `champion` découplent les consommateurs des numéros de version.
- Les tables de features alignent entraînement et service sur une définition.

<!-- unit: Service de modèles et IA en SQL -->

<!-- goals -->

- Choisir entre Model Serving, Vector Search et AI functions.
- Associer chaque option aux charges en ligne, de recherche ou batch.

<!-- concept -->

Une fois un modèle enregistré, la question est de savoir comment il rencontre les données. Les applications en ligne exigent des réponses rapides : le modèle se place derrière un endpoint REST. Les applications à génération augmentée doivent d'abord trouver les documents pertinents : un index sur une table Delta garde les embeddings synchronisés avec la source. L'enrichissement batch n'a besoin ni de l'un ni de l'autre : les analystes appellent un modèle dans une requête SQL et le warehouse gère le volume. Les trois restent sous les permissions Unity Catalog.

<!-- example -->

```sql
SELECT ticket_id,
       ai_classify(body, ARRAY('billing', 'bug', 'feature request')) AS category
FROM silver.support_tickets
WHERE created_date = current_date();
```

#### Qu'est-ce que Model Serving ?

Un service serverless qui expose des modèles (modèles MLflow personnalisés, modèles de fondation, modèles externes) sous forme d'endpoints REST avec autoscaling, supervision et contrôle d'accès.

#### Qu'est-ce que Vector Search ?

Une base vectorielle gérée qui indexe les embeddings d'une table Delta et maintient l'index synchronisé, utilisée pour la génération augmentée par récupération (RAG) et la recherche par similarité.

#### Que sont les fonctions d'IA de Databricks SQL ?

Des fonctions SQL comme `ai_query`, `ai_classify`, `ai_extract`, `ai_summarize` et `ai_translate` qui appellent des modèles depuis le SQL, pour enrichir des tables avec la sortie d'un LLM en batch.

<!-- challenge -->

Le support veut que chaque nouveau ticket soit classé par catégorie chaque matin, et un chatbot qui réponde à partir des articles du centre d'aide. Quelle option pour chaque besoin ?

<!-- solution -->

Le classement est du batch : une requête SQL planifiée avec `ai_classify` sur les nouveaux tickets. Le chatbot a besoin de recherche : un index Vector Search sur la table d'articles, avec le LLM derrière un endpoint Model Serving qui utilise les passages retrouvés comme contexte.

<!-- takeaways -->

- Model Serving répond aux requêtes en ligne via des endpoints REST.
- Vector Search indexe des tables Delta pour la recherche.
- Les AI functions amènent les modèles dans le SQL batch.

<!-- stage: Tout assembler -->

### Mises en situation

<!-- unit: Concevoir un pipeline de bout en bout -->

<!-- goals -->

- Combiner ingestion, couches médaillon, jobs et gouvernance dans une conception.
- Justifier chaque choix dans une réponse d'entretien.

<!-- concept -->

Les questions de conception testent votre capacité à relier les sections, pas à les réciter. Une bonne réponse suit les données : comment arrivent les fichiers, comment ils deviennent une table fiable, comment ils sont rafraîchis, qui peut les lire et comment le code arrive en production. Nommez un outil par étape et dites pourquoi il convient, comme des lectures incrémentales pour des dossiers qui grossissent ou un `MERGE` pour des corrections tardives. Terminez par la gestion des échecs : relances, alertes et effet d'une relance.

<!-- example -->

```text
S3 landing ─► Auto Loader ─► bronze (raw + _metadata)
                                │ dedupe, validate, MERGE
                                ▼
                             silver ─► gold aggregates ─► dashboard
 job: daily trigger, retries, alerts · UC grants · bundle deploys dev → prod
```

#### Concevez un pipeline qui ingère des fichiers CSV quotidiens depuis S3 jusqu'à une table de reporting.

Déposer les fichiers dans S3, les lire avec Auto Loader (trigger `availableNow`) dans une table Delta bronze avec un schéma déclaré et des colonnes `_metadata`, nettoyer, dédupliquer et valider vers silver avec `MERGE`, construire des agrégats gold ou un schéma en étoile, planifier le tout en job avec relances et alertes, le gouverner avec Unity Catalog et le déployer avec un bundle.

<!-- challenge -->

Le même pipeline doit maintenant accepter des fichiers corrigés pour des jours passés. Qu'est-ce qui change dans votre conception ?

<!-- solution -->

Auto Loader prend toujours chaque nouveau fichier une fois. Silver fait un `MERGE` sur la clé métier où le `updated_at` le plus récent l'emporte : les corrections remplacent les anciennes lignes au lieu de les dupliquer. Les agrégats gold des dates concernées sont recalculés, par exemple avec `replaceWhere` sur ces dates.

<!-- takeaways -->

- Suivez les données de l'arrivée aux consommateurs, un outil par étape.
- Rendez chaque couche idempotente pour sécuriser relances et corrections.
- Terminez par planification, surveillance, gouvernance et déploiement.

<!-- unit: Migrer vers Databricks -->

<!-- goals -->

- Planifier une migration depuis une pile Hive sur site.
- Valider les résultats avant de basculer les consommateurs.

<!-- concept -->

Les migrations échouent moins sur la technologie que sur l'enchaînement. Commencez par un inventaire, car les dépendances cachées (un script cron, un rapport qui lit une table brute) font échouer les bascules. Données et code se déplacent séparément : les tables passent en Delta, les requêtes sont portées en Spark SQL et les ordonnanceurs remplacés. Faire tourner l'ancien et le nouveau en parallèle et comparer les sorties crée la confiance nécessaire pour basculer les consommateurs et retirer l'ancien système.

<!-- example -->

```sql
-- Parquet table copied to cloud storage: convert in place
CONVERT TO DELTA parquet.`s3://lake/legacy/orders` PARTITIONED BY (order_date DATE);
-- then compare with the legacy output
SELECT count(*), sum(amount) FROM main.sales.orders WHERE order_date = '2026-09-30';
```

#### Comment migreriez-vous un pipeline on-premise basé sur Hive vers Databricks ?

En inventoriant les jobs, les tables et les dépendances ; en copiant les données dans le stockage cloud et en les convertissant en Delta (`CONVERT TO DELTA` pour le Parquet) ; en portant le HiveQL vers Spark SQL (très largement compatible) ; en remplaçant Oozie ou cron par Lakeflow Jobs ou Airflow ; en enregistrant les tables dans Unity Catalog ; et en validant les résultats côte à côte (nombre de lignes, sommes de contrôle, agrégats) avant de basculer les consommateurs.

<!-- challenge -->

Les volumes de lignes concordent entre l'ancien et le nouveau pipeline, mais les totaux de chiffre d'affaires diffèrent de 0,3 %. Comment trouver la cause ?

<!-- solution -->

Comparez les agrégats par jour et par clé pour localiser l'écart, puis comparez les lignes concernées. Causes habituelles : decimal contre double, fuseaux horaires des timestamps, gestion des NULL dans les jointures et doublons résolus différemment. Corrigez la règle, relancez et comparez à nouveau.

<!-- takeaways -->

- Inventoriez jobs, tables et consommateurs avant de déplacer quoi que ce soit.
- Convertissez les données en Delta, portez le HiveQL, remplacez l'ordonnanceur.
- Faites tourner en parallèle et comparez avant la bascule.
