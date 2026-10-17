## Fiche d'étude Databricks

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude Databricks : environ 200 questions](../../images/databricks_study_guide_title_img.png)

Environ 200 questions d'entretien sur Databricks, de l'idée du lakehouse à Delta Lake, Unity Catalog, l'ingestion, les pipelines et jobs Lakeflow, l'optimisation des performances, la sécurité et les coûts. Les réponses décrivent la plateforme telle qu'elle est en 2026 ; Databricks renomme souvent ses produits, les anciens noms sont donc indiqués quand ils restent courants. Ouvrez une question pour voir sa réponse, ou utilisez le filtre pour chercher dans toute la fiche.

<!-- QA -->

### Fondamentaux de la plateforme

#### Qu'est-ce que Databricks ?

Une plateforme cloud de données et d'IA, fondée par les créateurs d'Apache Spark, disponible sur AWS, Azure et Google Cloud. Elle réunit ingénierie des données, analytique SQL, streaming, machine learning et gouvernance sur une seule copie des données, stockée dans des formats ouverts (Delta Lake, Apache Iceberg) dans votre propre stockage cloud.

#### Qu'est-ce qu'un lakehouse ?

Une architecture qui stocke les données dans un stockage objet bon marché, comme un data lake, mais y ajoute des fonctions d'entrepôt de données : transactions ACID, schémas, optimisations proches de l'indexation, gouvernance fine et SQL rapide. Elle évite de garder une copie des données dans un lake pour la data science et une autre dans un entrepôt pour la BI.

#### Quels problèmes du data lake classique le lakehouse résout-il ?

Les data lakes n'avaient pas de transactions (les lecteurs voyaient des données à moitié écrites), pas de contrôle de schéma (les données inutilisables s'accumulaient), des requêtes lentes sur de nombreux petits fichiers, pas de mises à jour ni de suppressions faciles (un problème pour le RGPD) et une gouvernance faible. Delta Lake et Unity Catalog traitent chacun de ces points.

#### Quelle est la différence entre le plan de contrôle et le plan de calcul ?

Le plan de contrôle est géré par Databricks dans son propre compte : l'application web, les notebooks, l'ordonnanceur de jobs, le gestionnaire de clusters et les métadonnées d'Unity Catalog. Le plan de calcul est l'endroit où les données sont traitées. Avec le calcul classique, il tourne dans votre compte cloud (votre VPC) ; avec le calcul serverless, il tourne dans le compte de Databricks, dans la même région. Dans les deux cas, les données au repos restent dans votre stockage.

#### Qu'est-ce qu'un workspace Databricks ?

L'environnement où travaillent les utilisateurs : notebooks, fichiers, dossiers Git, jobs, pipelines, requêtes SQL, dashboards, clusters et expériences. Une entreprise a généralement plusieurs workspaces (par exemple dev, staging et prod), rattachés à un metastore Unity Catalog par région.

#### Qu'est-ce qu'un DBU ?

Une Databricks Unit, l'unité de capacité de traitement que Databricks facture à la seconde. Le tarif du DBU dépend du type de calcul (jobs, all-purpose, SQL, serverless) et de l'offre. Avec le calcul classique, vous payez aussi les machines virtuelles au fournisseur cloud ; en serverless, le prix du DBU inclut l'infrastructure.

#### Pourquoi le calcul de jobs est-il moins cher que le calcul all-purpose ?

Le calcul de jobs est facturé à un tarif de DBU plus bas, car il exécute des traitements planifiés et non interactifs et s'arrête à la fin du job. Les clusters all-purpose servent au développement interactif, sont partagés et restent allumés longtemps, donc Databricks les facture plus cher. Faire tourner la production sur des clusters all-purpose est une erreur de coût classique.

#### Quels langages peut-on utiliser dans Databricks ?

Python, SQL, Scala et R dans les notebooks, ainsi que Java et Scala dans les jobs JAR. On peut mélanger les langages dans un notebook avec les commandes magiques `%sql`, `%python`, `%scala`, `%md` (Markdown) et `%sh` (shell sur le driver).

#### Qu'est-ce qu'un notebook Databricks ?

Un document web composé de cellules qui exécutent du code sur le calcul attaché, avec résultats, graphiques, commentaires, historique des versions et coédition en temps réel. Les notebooks peuvent être planifiés comme tâches d'un job, paramétrés avec des widgets et stockés comme fichiers source dans Git.

#### Que sont les dossiers Git (anciennement Repos) ?

Des dossiers du workspace liés à un dépôt Git (GitHub, GitLab, Azure DevOps, Bitbucket). Ils permettent de cloner, créer des branches, faire des commits, pull et push depuis le workspace, pour que les notebooks et fichiers Python soient versionnés et relus comme n'importe quel code.

#### Qu'est-ce que DBFS, et pourquoi est-il déconseillé aujourd'hui ?

Le Databricks File System, une abstraction historique qui montait le stockage cloud sous des chemins `dbfs:/`, y compris un bucket racine du workspace. Il n'offre pas de gouvernance fine : Databricks recommande désormais les volumes Unity Catalog pour les fichiers et les tables pour les données, et désactive la racine DBFS et les montages dans les nouvelles installations.

#### Qu'est-ce que `dbutils` ?

Une bibliothèque d'utilitaires disponible dans les notebooks et les jobs : `dbutils.fs` pour les fichiers, `dbutils.secrets` pour les secrets, `dbutils.widgets` pour les paramètres, `dbutils.notebook.run` et `dbutils.notebook.exit` pour enchaîner des notebooks, et `dbutils.jobs.taskValues` pour passer de petites valeurs entre les tâches d'un job.

#### Que sont les widgets ?

Les paramètres d'entrée des notebooks (texte, liste déroulante, combobox, sélection multiple). Dans les jobs, les paramètres de la tâche les remplissent. En SQL, on référence les paramètres avec la syntaxe `:nom`.

```python
dbutils.widgets.text("snapshot_date", "2026-10-01")
snapshot = dbutils.widgets.get("snapshot_date")
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

#### Qu'est-ce que Lakeflow ?

Le nom générique, depuis 2025, des produits d'ingénierie des données de Databricks : Lakeflow Connect (connecteurs d'ingestion gérés), Lakeflow Declarative Pipelines (anciennement Delta Live Tables) et Lakeflow Jobs (anciennement Workflows).

#### Qu'est-ce que Mosaic AI ?

L'ensemble des fonctions d'IA et de ML de Databricks : entraînement et fine-tuning de modèles, Model Serving, Vector Search, AI Gateway, frameworks et évaluation d'agents, le tout gouverné par Unity Catalog.

### Delta Lake

#### Qu'est-ce que Delta Lake ?

Un format de stockage open source qui ajoute un journal de transactions à des fichiers Parquet. Il apporte les transactions ACID, le contrôle et l'évolution du schéma, le voyage dans le temps, `MERGE`, `UPDATE` et `DELETE`, ainsi que les lectures et écritures en streaming. C'est le format de table par défaut sur Databricks.

#### Comment fonctionne le journal de transactions de Delta ?

Chaque table possède un dossier `_delta_log/` de fichiers JSON de commit ordonnés (`000…0.json`, `000…1.json`) qui listent les fichiers de données ajoutés et supprimés par chaque transaction, ainsi que les changements de schéma et de métadonnées. Régulièrement, un checkpoint Parquet résume l'état pour que les lecteurs n'aient pas à rejouer tous les commits. Une version de la table est l'ensemble des fichiers valides après un commit donné.

#### Comment Delta garantit-il les propriétés ACID sur un stockage objet ?

Les écrivains créent de nouveaux fichiers Parquet, puis tentent de valider en écrivant de façon atomique l'entrée numérotée suivante du journal. Si deux écrivains sont en concurrence, un seul réussit ; l'autre vérifie s'il y a conflit, puis réessaie ou échoue. Les lecteurs ne voient que les fichiers référencés par des entrées validées, donc jamais d'écriture partielle.

#### Quel contrôle de concurrence Delta utilise-t-il ?

Un contrôle de concurrence optimiste : les transactions ne verrouillent rien, elles vérifient au moment du commit si un commit concurrent a touché les mêmes données. Les ajouts entrent rarement en conflit ; des `UPDATE`/`MERGE` concurrents sur les mêmes fichiers peuvent lever `ConcurrentModificationException`. Le partitionnement, le liquid clustering et la concurrence au niveau ligne (avec les deletion vectors) réduisent les conflits.

#### Qu'est-ce que le contrôle de schéma (schema enforcement) ?

Delta rejette les écritures dont les colonnes ou les types ne correspondent pas au schéma de la table, au lieu de la corrompre silencieusement. Cela protège les consommateurs des chargements défectueux.

#### Comment fonctionne l'évolution du schéma dans Delta ?

Il faut l'autoriser explicitement : `.option("mergeSchema", "true")` sur une écriture ajoute les nouvelles colonnes, et `ALTER TABLE` modifie le schéma. Pour `MERGE`, `WITH SCHEMA EVOLUTION` (ou le réglage de merge automatique) permet d'ajouter de nouvelles colonnes de la source. Le type widening autorise certains changements de type, comme `int` vers `bigint`, sans réécrire les données.

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

#### Que fait `OPTIMIZE` ?

Il compacte les petits fichiers en fichiers plus gros (environ 1 Go par défaut), ce qui accélère les lectures. Avec le Z-ordering ou le liquid clustering, il réécrit aussi les données pour que les valeurs proches se retrouvent dans les mêmes fichiers.

#### Qu'est-ce que le problème des petits fichiers ?

De nombreux fichiers minuscules ralentissent les lectures (chaque fichier a un coût d'ouverture et de métadonnées, et les statistiques sont moins utiles) ainsi que le journal de transactions. Le streaming et les petits ajouts fréquents en sont la cause. Solutions : `OPTIMIZE`, l'auto-compaction et les écritures optimisées, et des lots moins nombreux et plus gros.

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

#### Que sont les deletion vectors ?

Une optimisation du stockage où `DELETE`, `UPDATE` et `MERGE` marquent les lignes comme supprimées dans un petit fichier annexe au lieu de réécrire des fichiers Parquet entiers. Les écritures deviennent beaucoup plus rapides ; les fichiers sont physiquement réécrits plus tard par `OPTIMIZE` ou `REORG TABLE … APPLY (PURGE)`.

#### Qu'est-ce que le Change Data Feed ?

Une option de table (`delta.enableChangeDataFeed = true`) qui enregistre les changements au niveau ligne (insert, update_preimage, update_postimage, delete) avec la version et l'horodatage du commit. Les traitements en aval ne lisent que ce qui a changé :

```sql
SELECT * FROM table_changes('silver.customers', 120);
```

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

#### Quelle est la différence entre un deep clone et un shallow clone ?

Un deep clone copie les fichiers de données et les métadonnées dans une table indépendante. Un shallow clone ne copie que les métadonnées et pointe vers les fichiers de la source : il est instantané et peu coûteux, pratique pour tester des changements sur des données de la taille de la production. Les deux ont leur propre historique à partir du clonage.

#### Quelles contraintes Delta prend-il en charge ?

Les contraintes `NOT NULL` et `CHECK`, qui sont appliquées : une écriture qui les viole échoue. Les clés primaires et étrangères peuvent être déclarées dans Unity Catalog, mais elles sont informatives (non appliquées) et servent aux outils et à l'optimiseur.

#### Que sont les colonnes générées et les colonnes d'identité ?

Une colonne générée est calculée à partir d'autres colonnes (`GENERATED ALWAYS AS (CAST(ts AS DATE))`). Une colonne d'identité (`GENERATED ALWAYS AS IDENTITY`) attribue des nombres uniques et croissants (pas forcément consécutifs), utiles comme clés de substitution.

#### Qu'est-ce qu'UniForm ?

Universal Format : une option des tables Delta qui écrit aussi des métadonnées Iceberg (et Hudi), pour que les moteurs qui lisent Iceberg puissent lire les mêmes fichiers sans copier les données.

#### Quelle est la différence entre une table gérée et une table externe ?

Les données d'une table gérée (managed) vivent dans un stockage contrôlé par Unity Catalog ; supprimer la table supprime les données (après une période de rétention), et Databricks peut l'optimiser automatiquement. Une table externe pointe vers un chemin que vous gérez dans votre propre emplacement de stockage ; la supprimer n'efface que les métadonnées.

#### Que montre `DESCRIBE DETAIL` ?

Le format, l'emplacement, le nombre de fichiers, la taille en octets, les colonnes de partitionnement ou de clustering et les propriétés de la table. C'est une vérification rapide du problème des petits fichiers.

#### Quelle est la différence entre le mode `overwrite` et `replaceWhere` ?

`mode("overwrite")` remplace toute la table (sous forme d'une nouvelle version, donc le voyage dans le temps fonctionne toujours). `replaceWhere` ne remplace que les lignes qui satisfont un prédicat. L'écrasement dynamique de partitions (`partitionOverwriteMode=dynamic`) ne remplace que les partitions présentes dans les nouvelles données.

#### Comment Delta exécute-t-il `UPDATE` et `DELETE` sans deletion vectors ?

Il trouve les fichiers contenant des lignes concernées, les réécrit sans les lignes supprimées (ou avec les valeurs mises à jour) et valide une transaction qui retire les anciens fichiers et ajoute les nouveaux. C'est du copy-on-write : lectures peu coûteuses, écritures coûteuses sur les gros fichiers.

#### Qu'est-ce que `CONVERT TO DELTA` ?

Une commande qui transforme sur place un répertoire Parquet existant en table Delta, en écrivant un journal de transactions au-dessus des fichiers existants, sans copier les données.

#### À quoi servent les propriétés de table dans Delta ?

Ce sont des réglages stockés avec la table, comme `delta.enableChangeDataFeed`, `delta.logRetentionDuration`, `delta.deletedFileRetentionDuration`, `delta.enableDeletionVectors` ou `delta.appendOnly`, ainsi que des métadonnées clé-valeur personnalisées. On les définit avec `TBLPROPERTIES` et on les affiche avec `SHOW TBLPROPERTIES`.

#### Quelle est la différence entre la rétention du journal et celle des fichiers supprimés ?

`delta.logRetentionDuration` (30 jours par défaut) contrôle combien de temps l'historique des commits est conservé ; `delta.deletedFileRetentionDuration` (7 jours par défaut) contrôle combien de temps `VACUUM` garde les fichiers de données non référencés. Le voyage dans le temps a besoin des deux : les entrées du journal et les fichiers de données.

### Unity Catalog et gouvernance

#### Qu'est-ce qu'Unity Catalog ?

La couche de gouvernance unifiée de Databricks pour les actifs de données et d'IA de tous les workspaces : un seul endroit pour définir le contrôle d'accès, l'audit, le lignage, la découverte et le partage des tables, vues, volumes, fonctions et modèles. Il a aussi été publié en open source.

#### Quelle est la hiérarchie des objets d'Unity Catalog ?

Metastore (un par région) → catalogue → schéma (base de données) → tables, vues, vues matérialisées, volumes, fonctions et modèles. Les objets sont désignés par un nom à trois niveaux : `catalogue.schema.table`.

#### Qu'est-ce qu'un volume ?

Un objet Unity Catalog qui gouverne l'accès à des fichiers non tabulaires (CSV, JSON, images, PDF, wheels) dans le stockage cloud, avec des chemins de la forme `/Volumes/catalogue/schema/volume/chemin`. Les volumes gérés vivent dans le stockage géré par Unity Catalog ; les volumes externes pointent vers un chemin de stockage existant.

#### Que sont les storage credentials et les external locations ?

Une storage credential encapsule une identité cloud (un rôle IAM AWS, une identité managée Azure) qui a accès au stockage. Une external location associe un chemin de stockage à une credential, et les droits sur celle-ci contrôlent qui peut y créer des tables ou des volumes externes.

#### Comment accorde-t-on des droits dans Unity Catalog ?

En SQL ou via l'interface, à des utilisateurs, des groupes ou des service principals. Les privilèges se transmettent vers le bas de la hiérarchie, et un utilisateur a besoin de `USE CATALOG` et `USE SCHEMA` sur les niveaux supérieurs pour atteindre un objet.

```sql
GRANT USE CATALOG ON CATALOG prod TO `analysts`;
GRANT USE SCHEMA, SELECT ON SCHEMA prod.gold TO `analysts`;
```

#### Que sont les row filters et les column masks ?

Des fonctions attachées à une table et évaluées au moment de la requête. Un row filter détermine les lignes qu'un utilisateur peut voir (par exemple seulement celles de son pays) ; un column mask renvoie la valeur ou une version masquée selon les groupes de l'utilisateur. Les données restent dans une seule table au lieu de multiples copies filtrées.

#### Que sont les vues dynamiques ?

Des vues qui utilisent des fonctions comme `current_user()` ou `is_account_group_member()` pour filtrer des lignes ou masquer des colonnes. C'était l'approche habituelle avant l'arrivée des row filters et des column masks.

#### Quel lignage Unity Catalog capture-t-il ?

Le lignage au niveau table et colonne des requêtes exécutées sur le calcul Databricks, à travers notebooks, jobs, pipelines et dashboards, visible dans Catalog Explorer et interrogeable dans les tables système. Il répond à « qu'est-ce qui casse si je modifie cette colonne ? » et « d'où vient ce chiffre ? ».

#### Que sont les tables système ?

Des tables en lecture seule du catalogue `system` contenant des données d'exploitation : consommation facturée (`system.billing.usage`), journaux d'audit, lignage des tables, exécutions de jobs, événements de clusters, historique des requêtes, etc. Elles sont la base des tableaux de bord de coûts et de l'audit.

#### Qu'est-ce que l'ancien Hive metastore, et comment migrer depuis celui-ci ?

Le metastore par workspace antérieur à Unity Catalog, avec des droits locaux au workspace. La migration consiste à créer un metastore Unity Catalog, à migrer les tables (`SYNC` pour les tables externes, `CREATE TABLE … AS SELECT` ou deep clone pour les tables gérées) et à passer le code aux noms à trois niveaux. L'outil UCX automatise une grande partie de l'évaluation et de la migration.

#### Qu'est-ce que Delta Sharing ?

Un protocole ouvert pour partager des données vivantes en toute sécurité entre organisations et plateformes, sans les copier. Le fournisseur crée un share de tables, vues ou volumes ; les destinataires le lisent depuis Databricks ou depuis des clients open source (pandas, Spark, outils BI). Le partage entre comptes Databricks utilise les identités Unity Catalog.

#### Qu'est-ce que Lakehouse Federation ?

La fédération de requêtes qui permet à Unity Catalog d'enregistrer des bases externes (PostgreSQL, MySQL, SQL Server, Snowflake, Redshift, BigQuery et d'autres) comme catalogues étrangers, pour les interroger sur place avec gouvernance et lignage, sans d'abord ingérer les données.

#### À quoi servent les tags et les commentaires dans Unity Catalog ?

Les commentaires documentent tables et colonnes (et alimentent les descriptions générées par l'IA et la recherche) ; les tags (paires clé-valeur) classent les objets, par exemple `pii=true`, ce qui peut piloter des politiques, la découverte et les audits.

#### Qu'est-ce qu'un service principal, et pourquoi l'utiliser pour les jobs de production ?

Une identité non humaine destinée à l'automatisation. Les jobs de production et les déploiements CI/CD devraient s'exécuter sous un service principal pour ne pas dépendre du compte et des droits d'une personne, et pour limiter l'accès à ce dont le pipeline a besoin.

#### Comment gère-t-on les secrets dans Databricks ?

Dans des secret scopes (gérés par Databricks ou adossés à Azure Key Vault), lus avec `dbutils.secrets.get(scope, key)`. Les valeurs secrètes sont masquées dans les sorties des notebooks. Pour les ressources cloud, préférez l'accès par identité (instance profiles, storage credentials) aux secrets.

#### Quelle est la différence entre l'administration au niveau du compte et au niveau du workspace ?

Les administrateurs du compte gèrent les identités (utilisateurs, groupes, service principals, souvent synchronisés depuis un fournisseur d'identité via SCIM), les metastores, les workspaces et les réglages globaux. Les administrateurs d'un workspace gèrent les réglages, les politiques de calcul et les accès dans ce workspace.

#### Quelle est la différence entre la propriété et les privilèges ?

Le propriétaire d'un objet (un utilisateur, un groupe ou un service principal) peut accorder des privilèges dessus et le gérer. Les privilèges comme `SELECT`, `MODIFY`, `CREATE TABLE` ou `READ VOLUME` autorisent des actions précises. Faire d'un groupe le propriétaire des objets de production évite de dépendre d'une seule personne.

#### Qu'est-ce que la liaison entre workspaces et catalogues ?

Un réglage qui limite les workspaces pouvant accéder à un catalogue, par exemple pour qu'un catalogue de production ne soit accessible que depuis le workspace de production, même si des utilisateurs ont des droits dessus.

#### Qu'est-ce que l'information schema dans Unity Catalog ?

Un ensemble de vues SQL standard dans chaque catalogue (`information_schema.tables`, `columns`, `table_privileges` et d'autres) qui décrivent les objets et les droits, utiles pour la documentation et les audits.

#### Comment découvrir des données dans Unity Catalog ?

Avec Catalog Explorer et la recherche, qui s'appuient sur les noms, les commentaires, les tags et le lignage, ainsi que sur des signaux de popularité comme les utilisateurs et requêtes fréquents. De bons commentaires et tags améliorent beaucoup la découverte.

### Calcul

#### Quels types de calcul Databricks propose-t-il ?

Des clusters all-purpose pour le travail interactif, du calcul de jobs créé pour une exécution, des SQL warehouses pour le SQL et la BI, du calcul serverless pour les notebooks, jobs et pipelines, et des instance pools pour accélérer le démarrage des clusters classiques.

#### Qu'est-ce que le calcul serverless ?

Du calcul que Databricks provisionne et gère dans son propre compte : il démarre en quelques secondes, s'adapte automatiquement, utilise toujours un runtime récent avec Photon et n'est facturé que pendant qu'il travaille. Vous renoncez au choix des types d'instance et aux réglages Spark, et le code doit être compatible avec Spark Connect.

#### Comment est composé un cluster classique ?

D'un nœud driver qui exécute le programme principal, planifie le travail et collecte les résultats, et de nœuds workers dont les executors traitent les partitions. Un cluster à nœud unique exécute tout sur le driver, ce qui suffit pour de petites données et du ML sur une seule machine.

#### Que sont les modes d'accès ?

Des réglages qui contrôlent l'isolation et la gouvernance sur le calcul classique. Le mode standard (anciennement shared) permet à plusieurs utilisateurs de partager un cluster avec l'isolation d'Unity Catalog, via Spark Connect. Le mode dédié (anciennement single user) attribue le cluster à un utilisateur ou un groupe et prend en charge plus d'API, comme les RDD et certaines bibliothèques de ML.

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

#### Qu'est-ce qu'un SQL warehouse ?

Du calcul dédié aux requêtes SQL de Databricks SQL, des outils de BI et des dashboards. Types : serverless (démarrage rapide, recommandé), pro et classic. Il monte en charge en ajoutant des clusters pour absorber la concurrence et utilise Photon et une gestion intelligente de la charge.

#### Comment dimensionner un SQL warehouse ?

Choisissez une taille (T-shirt size) selon la complexité des requêtes et le volume de données (plus grand signifie des requêtes individuelles plus rapides), et fixez le nombre maximal de clusters pour la concurrence (plus d'utilisateurs simultanés). Surveillez la mise en file d'attente et le spill dans l'historique des requêtes, et configurez l'arrêt automatique.

#### Comment installer des bibliothèques sur un cluster ?

Comme bibliothèques du calcul (PyPI, Maven, wheels depuis des volumes ou des fichiers du workspace), au niveau du notebook avec `%pip install`, ou comme dépendances d'une tâche de job. En serverless, on déclare les dépendances dans la configuration de l'environnement. Figez les versions pour la reproductibilité.

#### Que sont les init scripts ?

Des scripts shell exécutés sur chaque nœud au démarrage, pour installer des paquets système ou configurer l'environnement. Ils doivent être stockés dans des volumes ou des fichiers du workspace, pas dans DBFS, et rester minimes car ils ralentissent le démarrage et compliquent le débogage.

#### Que se passe-t-il quand le driver manque de mémoire ?

Le notebook ou le job échoue ou redémarre. Causes fréquentes : `collect()` ou `toPandas()` sur de gros volumes, broadcast d'une table trop grande, gros objets Python sur le driver, ou trop de tâches suivies en même temps. Gardez les données dans Spark, écrivez les résultats dans des tables et dimensionnez correctement le driver.

#### Où regarder quand un cluster est lent ?

Dans la Spark UI (jobs, stages, durée des tâches, volumes de shuffle, spill, déséquilibre), les métriques du cluster (CPU, mémoire, disque), les journaux du driver et le profil de requête pour le SQL. Comparez la médiane et le maximum des durées de tâches d'un stage pour repérer le déséquilibre (skew).

#### À quoi sert un cluster à nœud unique ?

Au traitement de petites données, au travail avec pandas et scikit-learn et au développement léger. Il n'a pas de workers : Spark tourne en mode local sur le driver, ce qui est peu coûteux mais ne passe pas à l'échelle.

#### À quoi servent les clusters GPU ?

À l'entraînement et à l'inférence de deep learning, et à certaines bibliothèques accélérées par GPU. Ils nécessitent un runtime ML avec les pilotes GPU et coûtent cher, ils doivent donc s'arrêter rapidement.

#### Qu'implique le choix entre mode standard et dédié pour le ML ?

Les bibliothèques de ML qui ont besoin d'un accès direct à la JVM ou au `SparkContext`, ou l'entraînement sur GPU, exigent généralement le mode d'accès dédié ou le serverless avec le bon environnement. Le mode standard convient mieux au travail partagé en SQL et DataFrame.

### Ingestion

#### Quelles options existent pour charger des données dans Databricks ?

Auto Loader pour les fichiers qui arrivent dans le stockage cloud, `COPY INTO` pour des chargements batch idempotents, les connecteurs gérés de Lakeflow Connect (Salesforce, Workday, SQL Server, Google Analytics et d'autres), Structured Streaming depuis Kafka, Kinesis ou Event Hubs, Lakehouse Federation pour interroger sur place, des outils partenaires (Fivetran et d'autres) et le dépôt de fichiers dans des volumes.

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

#### Comment Auto Loader gère-t-il les changements de schéma ?

Il stocke le schéma inféré dans l'emplacement de schéma. Avec le mode par défaut `addNewColumns`, une nouvelle colonne arrête le flux, met à jour le schéma, et le flux reprend après redémarrage. Les données qui ne correspondent pas au schéma (mauvais type, colonne inattendue) vont dans la colonne `_rescued_data` au lieu d'être perdues.

#### Qu'est-ce que la colonne de données récupérées ?

Une colonne de texte JSON (`_rescued_data`) où Auto Loader place les valeurs qu'il n'a pas pu convertir selon le schéma. La surveiller révèle les changements de format en amont.

#### Qu'est-ce que `COPY INTO` ?

Une commande SQL qui charge les fichiers d'un chemin dans une table Delta et qui est idempotente : les fichiers déjà chargés sont ignorés. Elle convient aux chargements batch planifiés de milliers de fichiers ; Auto Loader est préférable pour des millions de fichiers ou une ingestion continue.

```sql
COPY INTO bronze.customers
FROM '/Volumes/raw/landing/customers/'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');
```

#### Que fait `trigger(availableNow=True)` ?

Il fait traiter à une requête de streaming tout ce qui est disponible au démarrage (en plusieurs lots, en respectant les limites de débit), puis l'arrête. On obtient le suivi incrémental du streaming avec le profil de coût d'un job batch planifié.

#### Qu'est-ce qu'un checkpoint de streaming ?

Un emplacement de stockage où une requête de streaming enregistre sa progression (offsets ou fichiers traités) et son état. Il garantit un traitement exactly-once entre les redémarrages. Chaque requête a besoin de son propre checkpoint, et le supprimer fait repartir la requête de zéro.

#### Comment ingérer depuis Kafka ?

Avec la source Kafka de Structured Streaming, qui lit `key`, `value`, `topic`, `partition`, `offset` et `timestamp`. On décode `value` (JSON, Avro avec un schema registry, Protobuf), on écrit les enregistrements bruts en bronze et on garde un checkpoint par requête.

#### Qu'est-ce que la colonne `_metadata` ?

Une colonne cachée disponible à la lecture de fichiers, avec `file_path`, `file_name`, `file_size` et `file_modification_time`. Elle remplace `input_file_name()` (non pris en charge dans Unity Catalog) pour enregistrer le fichier d'origine de chaque ligne.

#### Pourquoi éviter `inferSchema` en production ?

L'inférence demande une lecture supplémentaire des données, peut déduire des types différents selon les fichiers et change silencieusement quand la source change. Déclarez les schémas (contrats de données) pour les chargements de production, ou laissez Auto Loader gérer l'inférence avec des schema hints.

#### Qu'est-ce que Lakeflow Connect ?

Des connecteurs d'ingestion gérés et serverless pour les applications SaaS et les bases de données. Ils gèrent l'extraction incrémentale (souvent en CDC) et déposent les données dans des tables Unity Catalog via un pipeline, sans écrire de code d'extraction.

#### Comment charger les données d'une base relationnelle sans Lakeflow Connect ?

Avec le lecteur JDBC de Spark, en partitionnant la lecture avec `partitionColumn`, `lowerBound`, `upperBound` et `numPartitions` pour l'exécuter en parallèle, et en chargeant de façon incrémentale selon une colonne de watermark (par exemple `updated_at`). Stockez les identifiants dans des secrets.

#### Comment gérer les fichiers qui arrivent en retard ?

Auto Loader prend tout nouveau fichier à son arrivée, quelle que soit sa date, donc le chargement lui-même est sûr. En aval, utilisez `MERGE` sur les clés métier, ou retraitez les dates concernées avec `replaceWhere`, pour que les données tardives corrigent les résultats précédents.

#### Que sont les schema hints d'Auto Loader ?

Des types explicites pour certaines colonnes (`cloudFiles.schemaHints = "amount DECIMAL(18,2), event_ts TIMESTAMP"`) qui priment sur l'inférence, le reste du schéma étant toujours inféré.

#### Qu'est-ce que `read_files` ?

Une fonction SQL de table qui lit des fichiers (CSV, JSON, Parquet, Avro, XML, texte) depuis un chemin ou un volume avec inférence de schéma. Avec `STREAM read_files(...)` dans une streaming table, elle utilise Auto Loader en coulisses.

### Lakeflow Declarative Pipelines

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

#### Quand ne pas utiliser les pipelines déclaratifs ?

Quand vous avez besoin d'un contrôle fin de chaque étape, d'une logique qui ne rentre pas dans le modèle déclaratif (code procédural complexe, appels à des systèmes externes à chaque lot) ou de portabilité vers de simples jobs Spark. Beaucoup d'équipes utilisent des jobs classiques avec Delta et `MERGE` et obtiennent les mêmes résultats avec plus de code.

#### Qu'est-ce qu'un full refresh d'une table de pipeline ?

Vider la table et retraiter toutes les données source depuis le début, y compris la réinitialisation des checkpoints de streaming. C'est nécessaire après des changements de logique qui doivent s'appliquer à l'historique, mais cela peut coûter cher et faire perdre des données si la rétention de la source est plus courte que l'historique.

#### Comment écrire un pipeline déclaratif en Python ?

Avec le module `pipelines` (anciennement `dlt`) : des fonctions décorées renvoient des DataFrames, et les décorateurs déclarent les tables et les expectations.

```python
from pyspark import pipelines as dp

@dp.table(comment="Commandes nettoyées")
@dp.expect_or_drop("valid_amount", "amount >= 0")
def silver_orders():
    return spark.readStream.table("bronze_orders").dropDuplicates(["order_id"])
```

#### Où vivent les tables d'un pipeline ?

Dans le catalogue et le schéma Unity Catalog configurés pour le pipeline (et dans d'autres schémas si on utilise des noms complets). Pour les lecteurs, ce sont des tables Delta ordinaires, mais seul le pipeline devrait y écrire.

#### Qu'est-ce qu'un flow dans un pipeline déclaratif ?

Une unité de traitement qui écrit dans une table cible. Une streaming table peut avoir plusieurs append flows (par exemple un par région source), ce qui permet d'ajouter des sources sans full refresh.

#### Comment un pipeline déclaratif est-il facturé ?

Selon le calcul du pipeline (serverless ou classique) et l'édition du produit (Core, Pro, Advanced) ; les éditions supérieures ajoutent le CDC et les expectations. Les pipelines serverless sont facturés à l'usage et sont l'option par défaut.

### Jobs et orchestration

#### Que sont les Lakeflow Jobs (anciennement Workflows) ?

L'orchestrateur intégré de Databricks. Un job est un DAG de tâches (notebooks, scripts Python, wheels, SQL, dbt, pipelines, JAR, autres jobs) avec dépendances, planifications ou déclencheurs, paramètres, relances, timeouts, notifications et réglages de calcul.

#### Quels types de tâches un job peut-il contenir ?

Notebook, script Python, wheel Python, SQL (requête, fichier, dashboard ou alerte), dbt, pipeline, JAR, Spark Submit, Run Job (un autre job), condition If/else et For each (boucle sur des valeurs).

#### Quels déclencheurs peuvent lancer un job ?

Une planification cron, l'arrivée d'un fichier dans un emplacement de stockage, la mise à jour d'une table (quand une table source change), le mode continu (relance dès la fin), l'API ou la CLI, ou une exécution manuelle.

#### Comment passer des valeurs entre les tâches ?

Les petites valeurs avec les task values (`dbutils.jobs.taskValues.set` dans une tâche et `get` dans une tâche suivante, ou des références dynamiques comme `{{tasks.ingest.values.row_count}}` dans les paramètres). Les données elles-mêmes doivent passer par des tables, pas par des task values.

#### Que sont les paramètres de job et les références de valeurs dynamiques ?

Des paramètres définis au niveau du job, transmis à toutes les tâches et modifiables à chaque exécution. Les références dynamiques comme `{{job.start_time.iso_date}}` ou `{{job.run_id}}` injectent le contexte de l'exécution, utile pour un traitement idempotent piloté par la date.

#### Comment rendre un job Databricks idempotent ?

En écrivant avec `MERGE` ou avec `replaceWhere`/l'écrasement dynamique de partitions pour la date traitée au lieu d'ajouts aveugles, en tirant la date de traitement d'un paramètre plutôt que de l'horloge, en utilisant des checkpoints de streaming pour l'ingestion incrémentale, et en rendant les effets de bord (notifications, exports) rejouables sans risque.

#### Comment ne relancer que la partie d'un job qui a échoué ?

Avec « Repair run », qui relance les tâches en échec et leurs dépendances en aval, en réutilisant les résultats réussis en amont, éventuellement avec de nouveaux paramètres.

#### Quelle est la différence entre le calcul de jobs et l'exécution des tâches sur un cluster partagé ?

Chaque tâche peut utiliser son propre cluster de job, partager un cluster de job avec les autres tâches de la même exécution, utiliser du calcul serverless ou un cluster all-purpose existant. Les clusters de job partagés évitent les démarrages répétés ; le serverless supprime le démarrage.

#### Comment être alerté quand un job échoue ou est lent ?

En configurant des notifications (e-mail, Slack, Teams, PagerDuty, webhooks) au démarrage, au succès, à l'échec et au dépassement de seuils de durée, et en fixant un timeout et un nombre maximal d'exécutions concurrentes. Les tables système sur les exécutions de jobs permettent de construire des tableaux de bord de fiabilité sur la durée.

#### Faut-il orchestrer Databricks avec Airflow ou avec Jobs ?

Jobs suffit quand le flux vit surtout dans Databricks, et c'est moins cher et plus simple. Airflow (ou Dagster, Prefect) a du sens quand le DAG couvre de nombreux systèmes, quand l'entreprise en a fait son standard, ou pour des dépendances complexes entre équipes. Le provider Databricks d'Airflow peut lancer des jobs et attendre leur fin.

#### Que fait la tâche For each ?

Elle exécute une tâche imbriquée une fois par élément d'une liste (par exemple une liste de pays ou de dates), avec une concurrence configurable, pour ne pas devoir définir une tâche par élément.

#### À quoi sert la tâche de condition If/else ?

À créer une branche dans un job selon une valeur, comme une task value ou un paramètre : par exemple, sauter l'étape de publication quand une tâche de qualité signale zéro ligne valide.

#### Comment limiter les exécutions concurrentes d'un job ?

Avec le réglage du nombre maximal d'exécutions concurrentes (généralement 1 pour les jobs qui écrivent dans les mêmes tables) et l'option de file d'attente, pour qu'un nouveau déclenchement attende au lieu d'être ignoré ou exécuté en parallèle.

#### Comment exécuter un job pour le backfill de nombreuses dates ?

En paramétrant le job par date et en le déclenchant pour chaque date (via l'API, la CLI ou une tâche For each sur une liste de dates), en gardant des écritures idempotentes et en limitant la concurrence pour que le backfill n'affame pas la production.

### Spark et performances sur Databricks

#### Comment lire un plan de requête Spark ?

Avec `df.explain(mode="formatted")` ou l'onglet SQL de la Spark UI. On le lit de bas en haut : lectures (vérifiez les filtres poussés et les fichiers écartés), exchanges (shuffles), stratégies de jointure (broadcast, sort-merge) et agrégations. Le profil de requête de Databricks SQL montre la même chose avec les durées.

#### Qu'est-ce que l'Adaptive Query Execution ?

Une fonction de Spark, activée par défaut, qui réoptimise une requête entre les stages grâce aux statistiques d'exécution : elle fusionne les petites partitions de shuffle, transforme les jointures sort-merge en jointures broadcast quand un côté s'avère petit, et découpe les partitions déséquilibrées.

#### Qu'est-ce qu'une jointure broadcast, et quand aide-t-elle ?

Spark envoie une copie de la petite table à chaque executor, de sorte que la grande table est jointe sans être redistribuée. Elle aide quand un côté est assez petit (quelques dizaines de Mo par défaut, plus avec des hints). Diffuser une table trop grande provoque des erreurs de mémoire sur le driver ou les executors.

#### Qu'est-ce que le déséquilibre des données (skew), et comment le corriger ?

Certaines clés ont beaucoup plus de lignes que d'autres, si bien que quelques tâches durent bien plus longtemps que les autres. Solutions : laisser AQE découper les partitions déséquilibrées, diffuser le petit côté, filtrer ou traiter à part les clés chaudes (souvent les nulls), ou saler la clé pour la répartir sur plusieurs partitions.

#### Qu'est-ce que le spill, et pourquoi est-il lent ?

Quand les données d'une tâche ne tiennent pas en mémoire d'exécution, Spark les écrit sur le disque local puis les relit. Cela apparaît dans la Spark UI comme spill (memory) et spill (disk). On le corrige avec des partitions plus nombreuses et plus petites, des workers plus gros ou optimisés pour la mémoire, ou moins de données par tâche.

#### Comment choisir le nombre de partitions de shuffle ?

`spark.sql.shuffle.partitions` vaut 200 par défaut. Avec AQE, fixez un nombre généreux (ou `auto` sur Databricks) et laissez AQE fusionner. Visez des partitions d'environ 100 à 200 Mo après le shuffle ; trop peu provoque du spill, trop crée de la surcharge.

#### Pourquoi les UDF Python sont-elles lentes, et quelles sont les alternatives ?

Chaque ligne est sérialisée entre la JVM et un worker Python, et l'optimiseur ne voit pas l'intérieur de la fonction. Utilisez d'abord les fonctions intégrées, puis les UDF pandas (vectorisées) avec Arrow, ou des UDF SQL. Photon ne peut pas non plus accélérer les UDF Python.

#### Faut-il utiliser `cache()` sur Databricks ?

Avec parcimonie. Le cache aide quand le même DataFrame est réutilisé plusieurs fois dans une session interactive, mais il consomme de la mémoire et n'est pas pris en charge en serverless. Le disk cache (cache automatique sur SSD des fichiers Parquet distants sur certains types d'instance) apporte souvent le gain sans changer le code. Pour réutiliser entre jobs, écrivez une table.

#### Qu'est-ce que le disk cache ?

Un cache automatique, anciennement appelé Delta cache, qui stocke des copies des fichiers Parquet et Delta distants sur les SSD locaux des workers, pour accélérer les lectures répétées des mêmes données. Il est géré de façon transparente.

#### Pourquoi `withColumn` dans une boucle pose-t-il problème ?

Chaque appel ajoute une projection au plan logique, et l'analyse d'un plan très profond devient lente (elle peut prendre des minutes avant de traiter la moindre donnée). Utilisez un seul `select` ou `withColumns` avec un dictionnaire.

#### Qu'est-ce que l'optimisation prédictive ?

Une fonction d'Unity Catalog qui lance automatiquement `OPTIMIZE`, `VACUUM` et la collecte de statistiques sur les tables gérées quand elle en prévoit un bénéfice, pour vous éviter de planifier des jobs de maintenance.

#### Comment réduire le coût d'un job Databricks lourd ?

En utilisant du calcul de jobs ou serverless au lieu de clusters all-purpose, en activant Photon quand il est rentable, en traitant de façon incrémentale plutôt que de tout recalculer, en réduisant les lectures grâce au clustering et aux filtres, en dimensionnant et en autoscalant correctement les clusters, en utilisant des workers spot, en évitant les shuffles inutiles et les UDF Python, et en surveillant `system.billing.usage`.

#### Qu'est-ce que `replaceWhere` ?

Une option d'écriture qui remplace de façon atomique uniquement les lignes qui satisfont un prédicat, généralement une plage de dates, sans toucher au reste de la table. Elle rend idempotent le retraitement d'une période.

```python
(df.write.format("delta").mode("overwrite")
   .option("replaceWhere", "event_date = '2026-10-15'")
   .saveAsTable("silver.events"))
```

#### Comment diagnostiquer un job devenu soudain plus lent ?

En comparant l'exécution lente avec une exécution normale : volumes en entrée, nombre de fichiers (petits fichiers, `OPTIMIZE` manquant), changements de plan (un broadcast devenu sort-merge), déséquilibre dans un stage, spill, taille du cluster ou perte d'instances spot, et changements de code ou de données depuis la dernière bonne exécution.

#### Quelle est la différence entre transformations narrow et wide ?

Les transformations narrow (`filter`, `select`, `withColumn`) calculent chaque partition de sortie à partir d'une seule partition d'entrée, sans déplacer de données. Les transformations wide (`groupBy`, `join`, `distinct`, `orderBy`) exigent un shuffle sur le réseau. L'optimisation des performances porte surtout sur les shuffles.

#### Quelle est la différence entre `repartition` et `coalesce` ?

`repartition(n)` fait un shuffle complet et peut augmenter ou diminuer le nombre de partitions, éventuellement par colonnes. `coalesce(n)` se contente de fusionner des partitions sans shuffle complet : c'est moins coûteux, mais cela ne peut que réduire leur nombre et peut laisser des partitions inégales. `coalesce(1)` fait tout passer par une seule tâche.

#### Pourquoi un `count()` avant chaque étape ralentit-il un job ?

Chaque action déclenche l'exécution complète du plan jusqu'à ce point. Compter pour les logs après chaque transformation recalcule les données encore et encore. Récupérez les métriques du commit Delta (`numOutputRows` dans l'historique) ou calculez-les une seule fois.

#### Que sont les statistiques de colonnes, et pourquoi les calculer ?

`ANALYZE TABLE … COMPUTE STATISTICS FOR ALL COLUMNS` stocke le nombre de lignes et les statistiques des colonnes que l'optimiseur basé sur les coûts utilise pour choisir l'ordre et la stratégie des jointures. L'optimisation prédictive peut les maintenir automatiquement.

#### En quoi l'élagage de fichiers diffère-t-il de l'élagage de partitions ?

L'élagage de partitions (partition pruning) ignore des répertoires entiers selon les colonnes de partitionnement. L'élagage de fichiers (data skipping) ignore des fichiers individuels grâce aux statistiques min/max du journal Delta : il fonctionne sur toute colonne dotée de statistiques et profite du clustering.

### Databricks SQL et analytique

#### Qu'est-ce que Databricks SQL ?

La partie entrepôt SQL de la plateforme : SQL warehouses, éditeur SQL, historique et profils de requêtes, alertes, dashboards et connecteurs pour les outils de BI (Power BI, Tableau, Looker) via JDBC/ODBC.

#### Que sont les dashboards AI/BI et Genie ?

Les dashboards AI/BI sont les tableaux de bord actuels de Databricks, construits sur des SQL warehouses avec une aide de l'IA à la création. Genie est une interface en langage naturel où les utilisateurs métier posent des questions sur des tables sélectionnées et obtiennent des réponses appuyées sur du SQL.

#### Qu'est-ce qu'une vue matérialisée dans Databricks SQL ?

Une vue dont les résultats sont stockés et rafraîchis (selon un planning ou à la demande, de façon incrémentale quand c'est possible). Elle accélère les agrégations coûteuses des dashboards. On la crée avec `CREATE MATERIALIZED VIEW` et elle tourne sur des pipelines serverless.

#### Que sont les alertes SQL ?

Des requêtes planifiées qui comparent un résultat à un seuil et notifient (e-mail, Slack, webhook) quand la condition est remplie, par exemple quand un contrôle de qualité renvoie des lignes.

#### À quoi sert la fédération de requêtes en analytique ?

À joindre des tables Databricks avec des tables encore dans une base opérationnelle ou un autre entrepôt, pour l'exploration ou une migration, sans construire d'abord une ingestion. Pour un usage intensif et répété, ingérer les données est plus rapide et moins cher.

#### Quelle est la différence entre une vue, une vue temporaire et une vue matérialisée ?

Une vue ne stocke que la requête et l'exécute à chaque lecture. Une vue temporaire n'existe que dans la session courante. Une vue matérialisée stocke des résultats précalculés et doit être rafraîchie.

#### Comment les outils de BI se connectent-ils à Databricks ?

Via des pilotes JDBC/ODBC ou des connecteurs natifs (Power BI, Tableau, Looker, Excel) pointant vers un SQL warehouse, avec une authentification OAuth ou par jeton. Unity Catalog applique les droits de l'identité connectée.

#### Qu'est-ce que le cache de résultats de Databricks SQL ?

Un cache des résultats de requêtes sur les SQL warehouses : quand la même requête est relancée et que les tables n'ont pas changé, le résultat est renvoyé sans recalcul.

#### Qu'est-ce qu'une metric view ?

Un objet Unity Catalog qui définit une seule fois en YAML les indicateurs métier (mesures et dimensions) au-dessus d'une table, pour que les dashboards, Genie et les utilisateurs SQL les calculent de façon cohérente.

### Architecture médaillon et modélisation

#### Qu'est-ce que l'architecture médaillon ?

Une façon d'organiser les données du lakehouse en couches : bronze contient les données brutes telles que reçues (en ajout seul, avec des métadonnées de chargement), silver les données nettoyées, harmonisées, dédupliquées et validées, et gold les agrégats métier et modèles dimensionnels prêts pour la BI et le ML. La qualité et la structure augmentent de couche en couche.

#### Pourquoi garder une couche bronze brute ?

Pour pouvoir retraiter l'historique quand la logique change ou qu'on trouve des bugs, auditer ce que la source a réellement envoyé, et découpler l'ingestion de la transformation. Bronze doit être peu coûteux à conserver et fidèle à la source.

#### Que met-on en silver ?

Des colonnes typées et renommées, la déduplication, des valeurs standardisées (dates, codes, adresses), des jointures avec les données de référence, des contrôles de qualité avec mise en quarantaine des lignes défectueuses, et l'historique (SCD de type 2) si besoin. Silver est la version unique et fiable de chaque entité.

#### Que met-on en gold ?

Des données mises en forme pour la consommation : schémas en étoile (faits et dimensions), agrégats, tables de features et produits de données, avec les définitions métier appliquées. Les tables gold sont généralement plus petites et optimisées pour la lecture.

#### Comment implémenter une SCD de type 2 sur Delta ?

Avec `MERGE` : on clôt la ligne courante (on remplit `valid_to` et `is_current = false`) quand les attributs suivis changent, et on insère la nouvelle version. Une astuce courante consiste à fusionner une union des mises à jour avec une clé de merge nulle pour les lignes modifiées, de sorte qu'un seul `MERGE` clôt et insère. Les pipelines déclaratifs le font avec `AUTO CDC … STORED AS SCD TYPE 2`.

#### Comment mettre en quarantaine les enregistrements défectueux ?

En validant les lignes selon des règles en silver, en écrivant les lignes en échec avec leurs motifs dans une table de quarantaine, et en continuant avec les lignes valides. Surveillez le taux de quarantaine et alertez sur les pics. Dans les pipelines déclaratifs, des expectations `DROP ROW` et une requête inverse séparée donnent le même résultat.

#### Faut-il un catalogue par environnement ou par couche ?

Un schéma courant est un catalogue par environnement (`dev`, `staging`, `prod`) avec des schémas par couche (`bronze`, `silver`, `gold`), car les environnements ont besoin de droits et de stockages différents. Certaines équipes préfèrent des catalogues par domaine ou par entité métier. La cohérence compte plus que le choix.

#### Qu'est-ce qu'un produit de données dans le contexte de Databricks ?

Un ensemble de tables (généralement gold) sélectionné, documenté et gouverné, dont une équipe est responsable, avec des contrôles de qualité, une interface claire et un accès accordé via Unity Catalog, éventuellement partagé par Delta Sharing.

#### L'architecture médaillon a-t-elle toujours trois couches ?

Non. C'est une convention, pas une règle. Les petits projets peuvent fusionner silver et gold ; d'autres ajoutent une zone d'atterrissage (landing) avant bronze ou une couche de service (platinum) après gold. L'important est que chaque couche ait un contrat clair.

#### Bronze doit-elle être une table Delta ou des fichiers bruts ?

En général, les fichiers bruts restent dans une zone de landing (ou un volume) et bronze est une table Delta chargée depuis ces fichiers avec un minimum de changements et des métadonnées de chargement. Delta en bronze apporte les transactions, le suivi du schéma et un retraitement rapide ; garder les fichiers d'origine donne une copie exacte pour les audits.

#### Comment modéliser gold pour la BI et le ML à la fois ?

Avec des schémas en étoile (faits à un grain déclaré et dimensions conformes) pour la BI, et des tables de features par entité et par date pour le ML, tous construits à partir des mêmes tables silver pour que les chiffres concordent.

### Machine learning et IA

#### Qu'est-ce que MLflow ?

Une plateforme open source, créée par Databricks, pour le cycle de vie du ML : suivi des expériences (paramètres, métriques, artefacts), packaging des modèles, registre de modèles avec versions et alias, évaluation, et traces pour les applications d'IA générative. Sur Databricks, il est géré et intégré à Unity Catalog.

#### Que signifie enregistrer un modèle dans Unity Catalog ?

Les modèles sont stockés comme objets Unity Catalog (`catalogue.schema.modele`) avec des versions et des alias comme `champion`, gouvernés par les mêmes droits et le même lignage que les tables, et utilisables depuis plusieurs workspaces.

#### Qu'est-ce qu'une table de features ?

Une table Delta avec clé primaire servant à stocker des features de ML dans Unity Catalog. Les jeux d'entraînement sont construits en joignant les tables de features aux étiquettes (avec une jointure point-in-time pour les séries temporelles), et les mêmes features peuvent être servies en ligne pour l'inférence.

#### Qu'est-ce que Model Serving ?

Un service serverless qui expose des modèles (modèles MLflow personnalisés, modèles de fondation, modèles externes) sous forme d'endpoints REST avec autoscaling, supervision et contrôle d'accès.

#### Qu'est-ce que Vector Search ?

Une base vectorielle gérée qui indexe les embeddings d'une table Delta et maintient l'index synchronisé, utilisée pour la génération augmentée par récupération (RAG) et la recherche par similarité.

#### Que sont les fonctions d'IA de Databricks SQL ?

Des fonctions SQL comme `ai_query`, `ai_classify`, `ai_extract`, `ai_summarize` et `ai_translate` qui appellent des modèles depuis le SQL, pour enrichir des tables avec la sortie d'un LLM en batch.

### Sécurité, coûts et exploitation

#### Comment Databricks accède-t-il de façon sécurisée aux données sur AWS S3 ?

Par des rôles IAM : dans Unity Catalog, une storage credential encapsule un rôle IAM qui fait confiance à Databricks, et des external locations donnent accès aux chemins. Les anciennes installations utilisaient des instance profiles attachés aux clusters. Il faut éviter les clés d'accès dans le code.

#### Quelles options de sécurité réseau existent ?

Déployer le calcul classique dans votre propre VPC/VNet, la connectivité privée entre plan de contrôle et plan de calcul (PrivateLink, Private Link), les listes d'IP autorisées, des nœuds sans IP publique, des politiques réseau serverless pour contrôler les sorties, et des clés gérées par le client pour le chiffrement.

#### Comment auditer qui a accédé à quoi ?

Avec les journaux d'audit (disponibles dans la table `system.access.audit`), le lignage d'Unity Catalog et l'historique des requêtes. Ils enregistrent les connexions, les changements de droits, l'accès aux données et les actions sur les jobs.

#### Comment surveiller et maîtriser les dépenses Databricks ?

En taguant clusters, jobs et warehouses par centre de coût, en interrogeant `system.billing.usage` joint aux prix catalogue, en définissant budgets et alertes, en imposant des politiques de cluster (types d'instance, arrêt automatique, nombre maximal de workers), en utilisant le serverless ou le calcul de jobs en production, et en revoyant régulièrement les jobs les plus coûteux.

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

#### Que sont les Databricks Apps ?

Un moyen de construire et d'héberger des applications de données et d'IA (Streamlit, Dash, Gradio, Flask et d'autres) directement dans le workspace, avec authentification et accès aux données gouvernées via Unity Catalog.

#### Qu'est-ce que Lakebase ?

Une base de données opérationnelle gérée, compatible PostgreSQL, intégrée à Databricks et fondée sur Postgres serverless, destinée aux charges transactionnelles à faible latence (applications, service de features) synchronisées avec les tables du lakehouse.

### Mises en situation

#### Concevez un pipeline qui ingère des fichiers CSV quotidiens depuis S3 jusqu'à une table de reporting.

Déposer les fichiers dans S3, les lire avec Auto Loader (trigger `availableNow`) dans une table Delta bronze avec un schéma déclaré et des colonnes `_metadata`, nettoyer, dédupliquer et valider vers silver avec `MERGE`, construire des agrégats gold ou un schéma en étoile, planifier le tout en job avec relances et alertes, le gouverner avec Unity Catalog et le déployer avec un bundle.

#### Un job quotidien écrit des doublons à chaque relance. Que changez-vous ?

Je remplace l'ajout par une écriture idempotente : un `MERGE` sur la clé métier, ou `replaceWhere` sur la date traitée. Je tire la date d'un paramètre du job et j'ajoute un contrôle d'unicité sur la cible.

#### Votre table Delta compte 500 000 petits fichiers. Que faites-vous ?

Je lance `OPTIMIZE` (avec liquid clustering sur les principales colonnes de filtre), j'active les écritures optimisées et l'auto-compaction ou l'optimisation prédictive, puis je corrige la cause : regrouper les micro-ajouts, éviter le surpartitionnement et utiliser des triggers `availableNow` plutôt que des flux minuscules très fréquents. Je lance ensuite `VACUUM` pour supprimer les anciens fichiers.

#### Une jointure entre une table de faits de 2 To et une dimension de 50 Mo est lente. Que vérifiez-vous ?

Si elle est diffusée en broadcast (vérifier le plan ; ajouter un hint de broadcast ou relever le seuil), si la lecture des faits écarte des fichiers (filtres sur des colonnes regroupées), le déséquilibre sur la clé de jointure et le spill. Une dimension de 50 Mo devrait presque toujours être diffusée.

#### Une requête de streaming échoue après un changement de schéma de la source. Comment le gérez-vous ?

Avec Auto Loader en mode `addNewColumns`, je redémarre le flux pour qu'il prenne le nouveau schéma. Pour les changements incompatibles, je mets à jour le schéma cible (ou j'utilise la colonne de données récupérées) et, si la logique a changé, je démarre un nouveau checkpoint avec un plan de backfill clair. J'ajoute une alerte sur les données récupérées.

#### Les analystes ne doivent voir que les lignes de leur pays dans une table partagée. Comment l'implémentez-vous ?

J'attache à la table une fonction de row filter Unity Catalog qui compare l'appartenance de l'utilisateur à des groupes avec la colonne pays. J'accorde `SELECT` aux groupes d'analystes. J'utilise des column masks pour les colonnes sensibles.

#### Comment migreriez-vous un pipeline on-premise basé sur Hive vers Databricks ?

En inventoriant les jobs, les tables et les dépendances ; en copiant les données dans le stockage cloud et en les convertissant en Delta (`CONVERT TO DELTA` pour le Parquet) ; en portant le HiveQL vers Spark SQL (très largement compatible) ; en remplaçant Oozie ou cron par Lakeflow Jobs ou Airflow ; en enregistrant les tables dans Unity Catalog ; et en validant les résultats côte à côte (nombre de lignes, sommes de contrôle, agrégats) avant de basculer les consommateurs.

#### Quelqu'un a supprimé par erreur des colonnes d'une table gold il y a une heure. Comment la récupérez-vous ?

Je cherche dans `DESCRIBE HISTORY` la version précédant le changement et je lance `RESTORE TABLE … TO VERSION AS OF` cette version, ou je fais un `SELECT` dessus pour reconstruire. Ensuite je revois les droits pour que seul le service principal du pipeline puisse modifier les tables gold.

#### Comment réduire le coût du développement pour une équipe de dix ingénieurs ?

Avec des clusters petits ou à nœud unique, encadrés par des politiques et un arrêt automatique court, des notebooks serverless, des échantillons de données de développement partagés ou des shallow clones plutôt que des copies complètes, des tests unitaires locaux pour l'essentiel de la logique, des bundles en mode développement et une alerte budgétaire par équipe.

#### Comment expliquer le lakehouse à un interlocuteur métier ?

Un seul endroit pour toutes les données de l'entreprise, stockées une seule fois dans des formats ouverts dans le propre compte cloud de l'entreprise, où le reporting, la data science et l'IA travaillent sur les mêmes chiffres fiables, avec des droits et des traces d'audit gérés de façon centralisée.

#### Un notebook fonctionne sur votre cluster mais échoue en job serverless. Pourquoi ?

Probablement parce qu'il utilise quelque chose qui n'est pas pris en charge en serverless (Spark Connect) : RDD, `sparkContext`, `cache()`, la plupart des appels à `spark.conf.set`, des init scripts ou des bibliothèques qui ont besoin de la JVM. Réécrivez avec les API DataFrame, déclarez les dépendances dans l'environnement et testez en serverless avant de déployer.

#### Comment partager des tables gold avec une entreprise partenaire qui n'utilise pas Databricks ?

Avec Delta Sharing ouvert : je crée un share contenant les tables, un destinataire avec une credential par jeton, et le partenaire le lit depuis pandas, Spark ou un outil de BI. L'accès peut être révoqué à tout moment et il est audité.

#### La facture mensuelle Databricks a doublé. Comment enquêtez-vous ?

J'interroge `system.billing.usage` par SKU, workspace, job, warehouse et tag, et je compare les mois. Je cherche les clusters all-purpose sans arrêt automatique, les jobs passés sur du calcul all-purpose, les warehouses qui ne s'arrêtent jamais, les full refreshes, les nouvelles charges serverless et les relances incontrôlées.

#### Comment traiter une demande d'effacement RGPD sur un lakehouse Delta ?

Je supprime les lignes de la personne avec `DELETE` ou `MERGE` dans toutes les couches (bronze compris), puis je lance `VACUUM` pour supprimer physiquement les anciens fichiers qui les contenaient, une fois la période de rétention écoulée. Pseudonymiser les identifiants tôt dans le pipeline limite le nombre de tables contenant des données personnelles.
