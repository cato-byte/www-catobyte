## Fiche d'étude AWS Glue

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude AWS Glue : environ 200 questions](../../images/aws_glue_study_guide_title_img.png)

Environ 200 questions d'entretien sur AWS Glue : le Data Catalog, les crawlers, les jobs ETL Spark, les DynamicFrames, les job bookmarks, les workers et les coûts, le streaming, la qualité des données, l'orchestration, la sécurité avec Lake Formation et l'optimisation des performances. Les réponses décrivent le service tel qu'il est en 2026. Ouvrez une question pour voir sa réponse, ou utilisez le filtre pour chercher dans toute la fiche.

<!-- QA -->

### Fondamentaux

#### Qu'est-ce qu'AWS Glue ?

Un service serverless d'intégration de données sur AWS pour découvrir, préparer, déplacer et intégrer des données. Ses principaux éléments sont le Glue Data Catalog (un référentiel central de métadonnées), les crawlers (découverte de schémas), les jobs ETL (Apache Spark ou Python), Glue Studio (conception visuelle), Data Quality, DataBrew (préparation visuelle des données) et les workflows pour l'orchestration.

#### Que signifie « serverless » pour Glue ?

Vous ne provisionnez ni ne gérez de clusters : vous choisissez un type et un nombre de workers (ou laissez l'autoscaling décider), Glue démarre l'environnement pour l'exécution du job, et vous ne payez que la durée d'exécution, à la seconde.

#### Quels sont les principaux cas d'usage de Glue ?

Construire des data lakes sur S3 (cataloguer et transformer les données brutes en Parquet ou Iceberg), l'ETL vers Redshift ou d'autres bases, préparer des données pour Athena et le machine learning, l'ingestion CDC et streaming, et fournir un catalogue de métadonnées partagé pour Athena, EMR, Redshift Spectrum et Lake Formation.

#### Qu'est-ce que le Glue Data Catalog ?

Un référentiel de métadonnées géré, compatible avec le Hive metastore, par compte et par région. Il stocke des bases de données, des tables (schéma, emplacement, format, partitions, statistiques), des connexions et des fonctions définies par l'utilisateur. Athena, EMR, Redshift Spectrum, les jobs Glue et bien d'autres services l'utilisent pour savoir où sont les données et comment les lire.

#### Qu'est-ce qu'une base de données Glue ?

Un conteneur logique de tables dans le Data Catalog. Elle ne stocke pas de données ; elle regroupe des définitions de tables, et Lake Formation permet d'accorder des droits au niveau de la base.

#### Qu'est-ce qu'une table Glue ?

Des métadonnées qui décrivent des données : noms et types des colonnes, emplacement S3 (ou source JDBC), format (SerDe et formats d'entrée et de sortie), clés de partition et propriétés de la table. Les données restent dans S3 ou dans la base source.

#### Comment Glue se compare-t-il à Amazon EMR ?

Glue est serverless et centré sur l'ETL avec Spark, avec catalogue, bookmarks et qualité intégrés ; on échange du contrôle contre de la simplicité. EMR (sur EC2, EKS ou Serverless) donne le contrôle total de Spark, Hadoop, Hive, Trino et d'autres frameworks, de leurs versions et de leur réglage, et revient souvent moins cher pour des charges importantes et régulières.

#### Comment Glue se compare-t-il à AWS Lambda pour l'ETL ?

Lambda convient aux petites transformations événementielles (un fichier de quelques Mo), avec une limite de 15 minutes et une mémoire limitée. Glue convient au traitement distribué plus lourd avec Spark, aux exécutions longues et aux gros volumes.

#### Qu'est-ce qu'un DPU ?

Une Data Processing Unit : 4 vCPU et 16 Go de mémoire. Glue facture les jobs ETL, les crawlers et les sessions interactives en DPU-heures, à la seconde.

#### Comment un job Glue est-il facturé ?

Au DPU-heure, à la seconde, avec un minimum d'une minute pour les jobs Spark depuis Glue 2.0. Le coût vaut nombre de DPU × durée × prix du DPU-heure (environ 0,44 USD dans de nombreuses régions, moins en Flex). Les jobs Python shell facturent 1/16 ou 1 DPU.

#### Que sont les versions de Glue, et pourquoi comptent-elles ?

Chaque version de Glue embarque une version de Spark, Python et Java et des connecteurs : par exemple Glue 4.0 utilise Spark 3.3 et Python 3.10, et Glue 5.0 Spark 3.5 et Python 3.11. Les versions récentes démarrent et s'exécutent plus vite et prennent en charge des formats de table plus récents. Les anciennes perdent leur support : les mises à jour font partie de la maintenance.

#### Qu'est-ce que Glue Studio ?

L'interface console pour créer, exécuter et superviser des jobs Glue : un éditeur visuel où l'on construit l'ETL sous forme de graphe de sources, transformations et cibles (qui génère du code PySpark), un éditeur de scripts, un éditeur de notebooks et des tableaux de bord de supervision.

#### Qu'est-ce qu'AWS Glue DataBrew ?

Un outil visuel de préparation des données doté de plus de 250 transformations intégrées, utilisé par les analystes pour nettoyer et normaliser des données sans code. Les transformations sont enregistrées en recettes et exécutées en jobs sur des données S3, avec du profilage.

#### Comment Glue s'intègre-t-il dans l'architecture data lake d'AWS ?

Les données arrivent dans S3 (depuis DMS, Kinesis, AppFlow, des dépôts), les crawlers ou les jobs les enregistrent dans le Data Catalog, les jobs Glue les nettoient et les convertissent en zones curées (Parquet ou Iceberg), Lake Formation gouverne l'accès, et Athena, Redshift, EMR, QuickSight et SageMaker les consomment.

#### Quel lien entre Glue et SageMaker Lakehouse/Unified Studio ?

Le Glue Data Catalog est la base de métadonnées de SageMaker Lakehouse, et les fonctions d'intégration de Glue (jobs ETL, ETL visuel, connexions, zero-ETL) sont disponibles dans SageMaker Unified Studio, l'environnement unifié d'AWS pour les données, l'analytique et l'IA.

#### Quels sont les principaux composants d'AWS Glue, en une phrase chacun ?

Le Data Catalog stocke les métadonnées ; les crawlers découvrent les schémas ; les jobs ETL transforment les données avec Spark ou Python ; les triggers et workflows orchestrent ; Glue Studio permet la conception visuelle ; Data Quality valide les données ; DataBrew prépare les données visuellement ; le Schema Registry gouverne les schémas de streaming.

#### Qu'est-ce que l'ETL par rapport à l'ELT dans le contexte de Glue ?

En ETL, les jobs Glue transforment les données avant de les charger dans la cible (par exemple nettoyer et convertir en Parquet avant Redshift). En ELT, les données brutes sont chargées d'abord et transformées dans la cible (SQL Redshift, dbt sur Athena). Glue sert souvent au « E » et au « L » de l'ELT, ou au « T » dans un lakehouse.

#### Quels quotas de service Glue faut-il connaître ?

Les limites d'exécutions de jobs simultanées par compte, de DPU maximum par job, de nombre de jobs, triggers, crawlers, bases, tables et partitions par table. La plupart sont ajustables via Service Quotas ; les grands data lakes atteignent d'abord les limites de partitions et de concurrence.

#### Dans quelles régions Glue est-il disponible, et le catalogue est-il régional ?

Glue est disponible dans la plupart des régions AWS, et le Data Catalog est régional : chaque région a son propre catalogue par compte. L'accès inter-régions exige de répliquer les métadonnées ou d'utiliser des resource links Lake Formation.

#### Qu'est-ce qu'un development endpoint, et qu'est-ce qui l'a remplacé ?

Un ancien environnement toujours allumé pour développer des scripts Glue depuis des notebooks, facturé tant qu'il tournait. Les sessions interactives et les notebooks de Glue Studio l'ont remplacé, à la demande, facturés à la seconde avec des délais d'inactivité.

### Data Catalog

#### Comment les tables arrivent-elles dans le Data Catalog ?

Par des crawlers, par création manuelle (console, `CREATE EXTERNAL TABLE` dans Athena, CloudFormation, Terraform, l'API), par des jobs Glue qui créent ou mettent à jour les tables en écrivant (`enableUpdateCatalog`), ou par des services comme les blueprints de Lake Formation et les intégrations zero-ETL.

#### Qu'est-ce qu'une partition dans le Data Catalog ?

Un sous-ensemble des données d'une table défini par des valeurs de clés de partition (par exemple `year=2026/month=10/day=15`), chacun avec son propre emplacement S3. Les moteurs de requête ne lisent que les partitions qui correspondent aux filtres, ce qui réduit coût et durée.

#### Comment enregistre-t-on les nouvelles partitions ?

Par un crawler, par `MSCK REPAIR TABLE` ou `ALTER TABLE ADD PARTITION` dans Athena, par l'API `BatchCreatePartition`, par des jobs Glue qui écrivent avec mise à jour du catalogue, ou en s'en passant grâce à la projection de partitions d'Athena.

#### Que sont les index de partition ?

Des index sur les clés de partition des tables du catalogue qui en ont beaucoup, pour que les appels `GetPartitions` filtrés répondent vite au lieu de parcourir toutes les partitions. Ils accélèrent la planification des requêtes Athena et Glue sur des tables à des dizaines de milliers de partitions.

#### Que sont les statistiques de colonnes du Data Catalog ?

Des statistiques (nombre de valeurs distinctes, nulls, min/max, longueur moyenne) calculées par Glue pour les colonnes des tables et stockées dans le catalogue, qu'Athena et Redshift Spectrum utilisent pour l'optimisation basée sur les coûts, comme le réordonnancement des jointures.

#### Qu'est-ce qu'une connexion Glue ?

Un objet du catalogue qui stocke les propriétés de connexion à un stockage de données : URL JDBC, identifiants (de préférence un secret Secrets Manager), VPC, sous-réseau et groupes de sécurité, ou propriétés pour Kafka, MongoDB, Snowflake, BigQuery et d'autres connecteurs natifs. Les jobs et crawlers y font référence.

#### Quels formats de table le Data Catalog prend-il en charge ?

Les tables de style Hive en Parquet, ORC, Avro, JSON, CSV et d'autres formats, et les formats de table ouverts Apache Iceberg, Apache Hudi et Delta Lake. Iceberg est le plus profondément intégré aux services AWS.

#### Que sont les optimisations du catalogue pour les tables Iceberg ?

La maintenance gérée des tables Iceberg du Data Catalog : compaction automatique des petits fichiers, rétention des snapshots (expiration des anciens) et suppression des fichiers orphelins, configurées par table et exécutées par Glue sans jobs maison.

#### Plusieurs comptes AWS peuvent-ils partager un Data Catalog ?

Oui. L'accès peut être accordé entre comptes par des politiques de ressources sur le catalogue ou, plus souvent, par des droits inter-comptes Lake Formation (souvent via AWS RAM), pour qu'un compte central de gouvernance partage bases et tables avec les comptes consommateurs.

#### Qu'est-ce que le catalog ID ?

L'identifiant du compte AWS propriétaire d'un Data Catalog. Les API et les requêtes peuvent référencer le catalogue d'un autre compte par son identifiant quand l'accès inter-comptes est accordé.

#### Comment versionner les schémas de tables dans le Data Catalog ?

Le catalogue conserve automatiquement des versions d'une table quand elle est mise à jour (jusqu'à une limite), ce qui permet de voir et comparer les anciens schémas avec `GetTableVersions`. Les tables Iceberg conservent aussi l'historique du schéma dans leurs propres métadonnées.

#### Qu'est-ce que le Glue Schema Registry ?

Un service pour stocker, versionner et valider des schémas (Avro, JSON Schema, Protobuf) de données en streaming, avec des règles de compatibilité (backward, forward, full). Les producteurs et consommateurs utilisant Kafka, MSK, Kinesis ou Lambda sérialisent et valident les enregistrements selon les schémas enregistrés.

#### Qu'est-ce qu'un resource link ?

Un objet Lake Formation qui pointe vers une base ou une table partagée depuis un autre compte ou une autre région, pour que les utilisateurs l'interrogent comme si elle était locale dans leur catalogue.

#### Quelle différence entre une table externe et une governed table ?

Dans le Data Catalog, toutes les tables sur S3 sont externes (le catalogue ne contient que les métadonnées ; supprimer la table ne supprime pas les données). Les governed tables étaient un type de table Lake Formation avec transactions ACID, aujourd'hui retiré au profit des tables Apache Iceberg.

#### Comment interroger le Data Catalog par programme ?

Avec l'API Glue (`GetDatabases`, `GetTables`, `GetPartitions`, `SearchTables`) via boto3 ou la CLI, ou en SQL via les vues `information_schema` d'Athena.

#### Comment le Data Catalog est-il facturé ?

Le premier million d'objets stockés et le premier million de requêtes par mois sont gratuits ; au-delà on paie par tranche de 100 000 objets et par million de requêtes. Le calcul des statistiques et les optimisations Iceberg sont facturés à part en DPU-heures.

#### À quoi servent les propriétés de table comme `classification` et `compressionType` ?

Elles indiquent aux moteurs et à Glue comment interpréter les données : `classification` (csv, json, parquet) est fixée par les crawlers et utilisée par les jobs Glue, tandis que les paramètres du SerDe et la compression indiquent à Athena ou Hive comment lire les fichiers.

#### Qu'est-ce qu'une fonction définie par l'utilisateur dans le Data Catalog ?

Les métadonnées d'une UDF Hive (nom de classe et emplacement du JAR) stockées dans le catalogue pour que des moteurs comme Hive sur EMR puissent l'utiliser ; c'est surtout utile pour les charges compatibles Hive.

#### Comment garder un Data Catalog propre ?

Définir des conventions de nommage par couche (`raw_`, `curated_`), gérer les tables sous forme de code, supprimer les tables créées par des crawls accidentels, documenter tables et colonnes avec des descriptions, appliquer des LF-Tags pour la classification et surveiller les tables inutilisées.

### Crawlers

#### Qu'est-ce qu'un crawler ?

Un composant Glue qui se connecte à un stockage de données (S3, bases JDBC, DynamoDB, MongoDB, Delta, Iceberg, Hudi), échantillonne les données, infère schémas et partitions grâce aux classifiers, et crée ou met à jour des tables dans le Data Catalog. Il peut s'exécuter à la demande ou selon un planning.

#### Qu'est-ce qu'un classifier ?

La logique qui reconnaît un format de données et son schéma. Glue fournit des classifiers intégrés (CSV, JSON, Parquet, Avro, ORC, XML, journaux et d'autres), et l'on peut en ajouter avec des motifs grok, des balises XML, des chemins JSON ou des réglages CSV.

#### Comment un crawler décide-t-il du nombre de tables à créer ?

Il regroupe dans une table les fichiers aux schémas compatibles sous un préfixe commun, en s'appuyant sur l'arborescence pour détecter les partitions. Si les schémas diffèrent trop, il crée plusieurs tables. L'option « create a single schema for each S3 path » impose une table par chemin inclus.

#### Qu'est-ce que la politique de changement de schéma d'un crawler ?

Les réglages de ce qu'il faut faire quand le schéma change ou que des objets sont supprimés : mettre à jour la table ou seulement journaliser les changements, et supprimer, déprécier ou ignorer les tables et partitions disparues. En production, on journalise souvent les changements plutôt que de mettre à jour automatiquement, pour éviter les surprises.

#### Que sont les crawls incrémentaux ?

Des exécutions qui ne traitent que les dossiers ajoutés depuis la dernière (et, en mode événements S3, uniquement les objets modifiés d'après une file SQS), ce qui est bien plus rapide et moins cher sur des data lakes volumineux et en croissance.

#### Qu'est-ce que le mode événements S3 des crawlers ?

Un mode où le crawler lit les notifications d'événements S3 depuis une file SQS pour savoir exactement quels objets ont changé, au lieu de lister tout le préfixe.

#### Quels sont les problèmes fréquents des crawlers ?

Trop de tables créées à cause de schémas ou d'arborescences incohérents, des types mal inférés depuis des échantillons CSV, des erreurs `HIVE_PARTITION_SCHEMA_MISMATCH` quand les partitions ont des schémas différents, du coût et du temps sur d'énormes préfixes, et des changements de schéma silencieux qui cassent les requêtes en aval.

#### Faut-il toujours utiliser des crawlers ?

Non. Les crawlers sont pratiques pour la découverte et pour les sources qu'on ne maîtrise pas. Pour ses propres pipelines, définir les tables explicitement (infrastructure as code) et enregistrer les partitions depuis les jobs, ou utiliser la projection de partitions, donne des schémas prévisibles et aucun coût de crawler.

#### Comment les crawlers sont-ils facturés ?

Au DPU-heure pendant leur exécution, à la seconde avec une durée minimale par exécution. Parcourir des millions de petits fichiers peut coûter cher ; utilisez des motifs d'inclusion et d'exclusion, l'échantillonnage et les crawls incrémentaux.

#### Que sont les motifs d'exclusion ?

Des motifs glob qui indiquent au crawler les fichiers ou dossiers à ignorer, comme `**/_temporary/**`, `**.crc` ou `**/_SUCCESS`, ce qui évite les tables parasites et fait gagner du temps.

#### Un crawler peut-il parcourir une base JDBC ?

Oui. Via une connexion Glue, il lit les définitions de tables de bases comme MySQL, PostgreSQL, Oracle et SQL Server avec un chemin d'inclusion comme `mydb/%`, et crée des tables de catalogue que les jobs peuvent lire.

#### Comment les crawlers infèrent-ils les types des fichiers CSV ?

En échantillonnant les premières lignes et en choisissant des types adaptés ; si une colonne mélange les valeurs (des nombres avec quelques vides ou du texte), le crawler peut choisir `string`, ou un type que des lignes ultérieures contredisent. Définissez explicitement les tables CSV pour des types prévisibles.

#### Comment les crawlers gèrent-ils les en-têtes CSV ?

Le classifier CSV intégré devine si la première ligne est un en-tête en vérifiant si elle diffère des lignes de données. Quand il se trompe, un classifier CSV personnalisé avec un réglage d'en-tête explicite corrige le problème.

#### Les crawlers peuvent-ils créer des tables Iceberg ou Delta ?

Oui. Les crawlers peuvent enregistrer des tables Delta Lake, Iceberg et Hudi existantes sur S3 en lisant leurs métadonnées, et créer des tables de catalogue qui pointent vers le format de table (nativement ou via des manifestes, selon la configuration).

#### Qu'est-ce que la « recrawl policy » ?

Le réglage qui décide si l'on recrawle tous les dossiers à chaque exécution, seulement les nouveaux dossiers depuis le dernier crawl (incrémental), ou si l'on utilise les événements S3.

#### Comment limiter le périmètre d'un crawler ?

Avec des chemins d'inclusion précis, des motifs d'exclusion, une taille d'échantillon par dossier (pour S3), le réglage du niveau de table (profondeur de dossier à laquelle les tables sont créées) et des crawlers séparés par source.

#### Que signifie « table level » dans la configuration d'un crawler ?

La profondeur de dossier à laquelle le crawler crée les tables. La fixer évite qu'il crée des tables au mauvais niveau, par exemple en traitant chaque dossier de partition comme une table distincte.

### Jobs ETL Glue

#### Quels types de jobs Glue propose-t-il ?

Les jobs Spark (ETL batch en PySpark ou Scala), les jobs Spark streaming (traitement continu depuis Kinesis, Kafka ou MSK) et les jobs Python shell (scripts Python mono-nœud pour de petites tâches).

#### À quoi ressemble un job Glue PySpark de base ?

```python
import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

args = getResolvedOptions(sys.argv, ["JOB_NAME", "target_path"])
glue = GlueContext(SparkContext.getOrCreate())
spark = glue.spark_session
job = Job(glue)
job.init(args["JOB_NAME"], args)

orders = glue.create_dynamic_frame.from_catalog(
    database="raw", table_name="orders", transformation_ctx="orders")
df = orders.toDF().filter("status = 'paid'")
df.write.mode("append").partitionBy("order_date").parquet(args["target_path"])

job.commit()
```

#### Qu'est-ce que `GlueContext` ?

Une enveloppe autour du `SparkContext` qui ajoute les fonctions de Glue : lecture et écriture de DynamicFrames depuis le catalogue, S3 et les connexions, job bookmarks et options propres à Glue.

#### Que font `job.init()` et `job.commit()` ?

`init` initialise l'état du job, et `commit` enregistre l'état des job bookmarks à la fin d'une exécution réussie. Sans `commit`, les bookmarks n'avancent pas et l'exécution suivante retraite les mêmes données.

#### Comment passer des paramètres à un job Glue ?

Sous forme d'arguments du job (`--target_path s3://...`) définis dans le job ou surchargés au démarrage, lus avec `getResolvedOptions`. Des arguments spéciaux configurent Glue lui-même, comme `--job-bookmark-option`, `--enable-metrics`, `--additional-python-modules` ou `--conf`.

#### Comment ajouter des bibliothèques Python à un job Glue ?

Avec `--additional-python-modules` (installation depuis PyPI ou des wheels dans S3 au démarrage), `--extra-py-files` (fichiers zip ou py dans S3), ou en empaquetant les dépendances dans un wheel. Pour des jobs sans accès Internet, hébergez les wheels dans S3 ou utilisez un dépôt privé via un endpoint VPC.

#### Comment ajouter des dépendances JAR ?

Avec `--extra-jars` pointant vers des fichiers JAR dans S3, pour des pilotes JDBC ou des bibliothèques Spark non incluses dans la version de Glue.

#### À quoi sert un job Python shell ?

Aux tâches légères qui n'ont pas besoin de Spark : appeler des API, exécuter du SQL sur Redshift ou Athena, déplacer de petits fichiers, déclencher d'autres services. Il tourne sur 1/16 ou 1 DPU avec Python et des bibliothèques courantes comme pandas et boto3.

#### Qu'est-ce que l'exécution Flex de Glue ?

Une classe d'exécution qui utilise de la capacité inutilisée à prix réduit, avec des démarrages éventuellement plus longs et sans garantie de démarrage immédiat. Elle convient aux charges non urgentes comme le batch de nuit, les tests et les backfills.

#### Qu'est-ce que l'autoscaling des jobs Glue ?

Avec l'autoscaling activé (Glue 3.0+), Glue ajoute et retire des workers pendant l'exécution selon la charge, jusqu'au maximum fixé, pour ne pas payer de workers inactifs dans les étapes peu parallèles.

#### Que sont les timeouts et les relances d'un job ?

`Timeout` arrête un job après un certain nombre de minutes (48 heures par défaut pour les jobs batch, ce qui est risqué ; fixez une valeur réaliste). `MaxRetries` relance automatiquement les jobs en échec ; ne l'utilisez que si le job est idempotent.

#### Qu'est-ce que la concurrence maximale d'un job ?

Le nombre d'exécutions simultanées autorisées pour un même job (1 par défaut). Si une exécution est encore active, les nouvelles demandes de démarrage échouent avec `ConcurrentRunsExceededException`, sauf si on l'augmente.

#### Comment écrire dans Redshift depuis un job Glue ?

Via une connexion Redshift, en écrivant un DynamicFrame avec `glue.write_dynamic_frame.from_jdbc_conf` (Glue dépose les données dans S3 et lance `COPY`), ou avec le connecteur Spark pour Redshift. `preactions` et `postactions` exécutent du SQL avant et après, par exemple un `TRUNCATE` d'une table de staging puis un `MERGE` dans la cible.

#### Comment lire une base JDBC en parallèle ?

Avec les options `hashfield`/`hashpartitions` des DynamicFrames, ou `partitionColumn`, `lowerBound`, `upperBound` et `numPartitions` sur le lecteur JDBC de Spark, pour que plusieurs tâches lisent des plages en même temps au lieu d'une seule connexion qui lit tout.

#### Les jobs Glue peuvent-ils écrire des tables Iceberg, Hudi ou Delta ?

Oui. Fixez `--datalake-formats` à `iceberg`, `hudi` ou `delta` (avec les réglages Spark correspondants) et utilisez Spark SQL ou les API DataFrame, y compris `MERGE INTO`, avec le Glue Data Catalog comme catalogue.

```python
spark.sql("""
MERGE INTO glue_catalog.curated.customers t
USING updates s ON t.customer_id = s.customer_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
""")
```

#### À quoi sert le répertoire temporaire (`--TempDir`) ?

Un emplacement S3 où Glue écrit des données intermédiaires, par exemple lors d'un chargement dans Redshift ou pour le shuffle dans certaines configurations. Il doit avoir une règle de cycle de vie qui supprime les anciens fichiers.

#### Que sont les sessions interactives Glue ?

Des sessions Spark à la demande, utilisées depuis des notebooks Jupyter, les notebooks de Glue Studio ou votre IDE pour développer et déboguer du code Glue de façon interactive, facturées à la seconde avec un délai d'inactivité.

#### Comment développer des jobs Glue en local ?

Avec les images Docker officielles de Glue (qui contiennent les bibliothèques Glue et le Spark d'une version donnée), en exécutant scripts et pytest en local, ou avec des sessions interactives depuis un notebook local. La logique PySpark pure peut aussi être testée avec une SparkSession locale.

#### Quelle est la différence entre l'éditeur de scripts Spark et l'éditeur visuel ?

L'éditeur visuel construit les jobs comme un graphe de nœuds et génère le code ; il est rapide pour l'ETL standard et accessible aux analystes. L'éditeur de scripts donne le contrôle total du code PySpark ou Scala. Beaucoup d'équipes commencent en visuel puis passent au code géré dans Git.

#### Comment utiliser Spark SQL dans un job Glue ?

Convertir en DataFrame, enregistrer une vue temporaire et lancer `spark.sql()`. Avec le Data Catalog activé comme Hive metastore (`--enable-glue-datacatalog`), on peut interroger directement les tables du catalogue par `base.table`.

#### Que fait `--enable-glue-datacatalog` ?

Il configure Spark dans le job pour utiliser le Glue Data Catalog comme Hive metastore, de sorte que `spark.sql("SELECT * FROM raw.orders")` et `saveAsTable` fonctionnent sur les tables du catalogue.

#### Comment lire du JSON imbriqué dans Glue ?

Le lire en DynamicFrame ou en DataFrame (schéma inféré ou déclaré), puis l'aplatir avec des `select` de champs imbriqués, `explode` pour les tableaux, ou `Relationalize` de Glue pour une sortie entièrement relationnelle.

#### Comment gérer les enregistrements défectueux à la lecture de fichiers ?

Pour les lecteurs Spark, avec `mode` (`PERMISSIVE` avec une colonne d'enregistrements corrompus, `DROPMALFORMED`, `FAILFAST`) ou `badRecordsPath` quand c'est pris en charge ; pour les DynamicFrames, les erreurs sont capturées par enregistrement et consultables avec `errorsAsDynamicFrame()`, avec des seuils fixés par `stageThreshold` et `totalThreshold`.

#### Comment écrire la sortie avec un nombre de fichiers maîtrisé ?

Faire un repartition ou un coalesce avant l'écriture (`df.repartition(20, "order_date")`), ou régler `spark.sql.files.maxRecordsPerFile`, pour que chaque partition contienne quelques gros fichiers au lieu de centaines de petits.

#### À quoi sert l'identifiant d'exécution d'un job Glue ?

Il identifie une exécution pour la supervision, les journaux, le rembobinage des bookmarks et les relances, et peut être reporté dans les sorties (par exemple en colonne) pour le lignage.

#### Comment lire DynamoDB dans Glue ?

Avec le connecteur DynamoDB : soit directement (consomme de la capacité de lecture, contrôlée par `dynamodb.throughput.read.percent`), soit via l'export DynamoDB vers S3 (`dynamodb.export`), qui ne consomme pas de capacité de la table et est préférable pour les grandes tables.

#### Comment les jobs Glue se connectent-ils à Snowflake, BigQuery ou d'autres sources hors AWS ?

Via les connecteurs natifs de Glue pour de nombreuses sources (Snowflake, BigQuery, Teradata, SAP HANA, MongoDB et des applications SaaS), via des connecteurs AWS Marketplace, ou en JDBC avec un pilote personnalisé et une connexion Glue.

#### Quels sont les états d'exécution d'un job ?

`STARTING`, `RUNNING`, `STOPPING`, `STOPPED`, `SUCCEEDED`, `FAILED`, `TIMEOUT`, `ERROR` et `WAITING`. EventBridge reçoit les événements de changement d'état pour les alertes et l'orchestration.

#### Que deviennent les journaux d'un job Glue ?

Les journaux du driver et des executors vont dans CloudWatch Logs (`/aws-glue/jobs/output` et `/aws-glue/jobs/error`) ; la journalisation continue les transmet pendant l'exécution. Utilisez `glue.get_logger()` pour des messages structurés.

### DynamicFrames et transformations

#### Qu'est-ce qu'un DynamicFrame ?

La structure de données distribuée de Glue, proche d'un DataFrame Spark mais où chaque enregistrement est autodescriptif : il n'a pas besoin d'un schéma fixe à l'avance. Il gère les données incohérentes (un champ tantôt chaîne, tantôt entier) grâce aux types « choice ».

#### Quelle est la différence entre un DynamicFrame et un DataFrame ?

Un DataFrame a un schéma unique pour tout le jeu de données et bénéficie de tout l'optimiseur et de l'API Spark SQL. Un DynamicFrame calcule le schéma par enregistrement, prend en charge les types choice, les transformations propres à Glue, les bookmarks et l'intégration au catalogue. On convertit avec `toDF()` et `DynamicFrame.fromDF()`, et la plupart des équipes transforment en DataFrame.

#### Qu'est-ce qu'un type choice, et comment fonctionne `ResolveChoice` ?

Quand une colonne contient des valeurs de types différents, un DynamicFrame garde un type choice (par exemple `choice<int,string>`). `ResolveChoice` le résout avec `cast:long`, `make_cols` (sépare en `col_int` et `col_string`), `make_struct` ou `project:string`.

```python
resolved = dyf.resolveChoice(specs=[("amount", "cast:double"), ("id", "cast:long")])
```

#### Que fait `ApplyMapping` ?

Il renomme des colonnes, convertit des types et sélectionne des champs en une étape, à partir d'une liste de tuples `(source, type_source, cible, type_cible)` ; c'est ainsi que fonctionne le nœud de mapping de Glue Studio.

#### Que fait `Relationalize` ?

Il aplatit du JSON imbriqué en un ensemble de tables relationnelles : les structures imbriquées deviennent des colonnes et les tableaux des tables séparées reliées par des clés générées, prêtes à charger dans une base relationnelle.

#### Quelles autres transformations intégrées Glue propose-t-il ?

`DropFields`, `SelectFields`, `RenameField`, `Filter`, `Map`, `Join`, `SplitFields`, `SplitRows`, `Unbox` (analyse de chaînes JSON), `DropNullFields`, `FillMissingValues`, `FindMatches` (déduplication par ML) et, dans Glue Studio, des transformations comme `Aggregate`, `Pivot`, `Derived column`, `Identify sensitive data` et `Evaluate data quality`.

#### Qu'est-ce que FindMatches ?

Une transformation de machine learning qui identifie des enregistrements en double ou correspondants sans clé commune (par exemple le même client orthographié différemment), entraînée à partir d'exemples étiquetés.

#### Pourquoi beaucoup d'équipes convertissent-elles tôt les DynamicFrames en DataFrames ?

Les DataFrames ont une API plus riche, l'optimiseur Catalyst, de meilleures performances pour la plupart des transformations et sont portables vers d'autres environnements Spark. Les DynamicFrames servent surtout à la lecture (catalogue, bookmarks, résolution des choices) et à l'écriture (mise à jour du catalogue, connecteurs).

#### Comment écrire un DynamicFrame en mettant à jour le catalogue ?

```python
sink = glue.getSink(connection_type="s3", path="s3://lake/curated/orders/",
                    enableUpdateCatalog=True, updateBehavior="UPDATE_IN_DATABASE",
                    partitionKeys=["order_date"])
sink.setFormat("glueparquet")
sink.setCatalogInfo(catalogDatabase="curated", catalogTableName="orders")
sink.writeFrame(dyf)
```

#### Qu'est-ce que le format `glueparquet` ?

Un écrivain Parquet optimisé par Glue pour les DynamicFrames, qui calcule le schéma pendant l'écriture et évite une lecture supplémentaire des données, ce qui accélère l'écriture de gros volumes.

#### Qu'est-ce que `transformation_ctx` ?

Un nom unique pour chaque source et transformation d'un job, utilisé par les job bookmarks pour stocker leur état. Sans lui sur une source, les bookmarks ne fonctionnent pas pour cette source.

#### Comment filtrer un DynamicFrame ?

Avec `Filter.apply(frame=dyf, f=lambda row: row["status"] == "paid")` ou `dyf.filter(...)`, même si convertir en DataFrame et utiliser `filter("status = 'paid'")` est généralement plus rapide car Spark peut l'optimiser.

#### Comment joindre des DynamicFrames ?

Avec `Join.apply(dyf1, dyf2, "key1", "key2")`, qui fait une jointure par égalité ; pour d'autres types de jointures ou conditions, convertir en DataFrames.

#### Que fait `Unbox` ?

Il analyse une colonne texte contenant du JSON (ou du CSV) et la transforme en structure, pour que les champs imbriqués deviennent des colonnes accessibles.

#### Que fait `SplitFields` ?

Il sépare un DynamicFrame en deux collections par colonnes, par exemple pour isoler les colonnes de données personnelles du reste et les écrire à des emplacements différents.

#### Comment dédupliquer dans un job Glue ?

Convertir en DataFrame et utiliser `dropDuplicates(["key"])` ou une fonction de fenêtre avec `row_number()` ordonnée par un horodatage de mise à jour, en gardant l'enregistrement le plus récent par clé.

#### Comment ajouter des colonnes d'audit dans un job Glue ?

Ajouter des colonnes comme `ingested_at` (`current_timestamp()`), `source_file` (`input_file_name()` ou les métadonnées du fichier), `job_run_id` et `process_date`, pour que chaque ligne soit traçable jusqu'à l'exécution et au fichier qui l'ont produite.

### Job bookmarks et traitement incrémental

#### Que sont les job bookmarks ?

Une fonction de Glue qui conserve un état entre les exécutions pour que chacune ne traite que les nouvelles données : pour les sources S3, les fichiers (par date de modification) déjà traités ; pour les sources JDBC, les valeurs maximales des colonnes clés du bookmark.

#### Comment activer et piloter les job bookmarks ?

Avec `--job-bookmark-option` : `job-bookmark-enable`, `job-bookmark-disable` ou `job-bookmark-pause` (traite depuis le dernier bookmark sans le mettre à jour). La source doit avoir un `transformation_ctx` et le script doit appeler `job.commit()`.

#### Comment réinitialiser ou rembobiner un bookmark ?

Avec la console ou l'API `ResetJobBookmark`, qui fait tout retraiter à l'exécution suivante ; on peut aussi revenir à l'identifiant d'une exécution précédente pour retraiter à partir de ce point.

#### Quelles sont les limites des job bookmarks ?

Ils suivent les fichiers par date de modification : des fichiers écrasés sous le même nom peuvent être manqués ou retraités ; les bookmarks JDBC exigent des colonnes clés croissantes et ne voient pas les mises à jour d'anciennes lignes ; ils ne fonctionnent qu'avec certaines sources et certains formats ; et ils ne rendent pas les écritures idempotentes, donc un échec après l'écriture et avant le `commit` fait retraiter des données.

#### Comment rendre un job Glue idempotent ?

En écrivant la sortie de la partition traitée par écrasement (écrasement dynamique de partitions) ou en utilisant `MERGE` sur une table Iceberg, plutôt que d'ajouter aveuglément ; en tirant la période traitée d'un paramètre ; et en considérant les bookmarks comme une optimisation, pas comme la seule garantie.

#### Qu'est-ce que le pushdown predicate dans Glue ?

Un filtre sur les colonnes de partition passé à la lecture depuis le catalogue (`push_down_predicate="order_date >= '2026-10-01'"`) pour que Glue ne liste et ne lise que les partitions correspondantes au lieu de toute la table.

#### Qu'est-ce que `catalogPartitionPredicate` ?

Un filtre de partitions côté serveur, évalué par le Data Catalog à l'aide des index de partition, qui réduit le nombre de partitions que Glue doit récupérer du catalogue pour les tables très partitionnées. Il se combine avec `push_down_predicate`.

#### Comment ne traiter que les données de la veille sans bookmarks ?

Passer la date en argument du job (depuis l'ordonnanceur), lire avec un pushdown predicate sur la partition de date, et écraser la partition de sortie de cette date. C'est explicite, reproductible, et cela facilite les backfills.

#### Les job bookmarks fonctionnent-ils avec des tables Iceberg en source ?

Pas de la même manière ; pour des sources Iceberg, on traite de façon incrémentale avec les fonctions propres à Iceberg, comme la lecture des changements entre snapshots (lectures incrémentales ou vues de changelog), en mémorisant l'identifiant du dernier snapshot traité.

#### Qu'arrive-t-il aux bookmarks si un job échoue ?

Les bookmarks ne sont mis à jour par `job.commit()` qu'en cas de succès : une exécution en échec laisse le bookmark en place et la suivante retraite les mêmes données. D'où la nécessité d'écritures idempotentes.

#### Deux jobs différents peuvent-ils partager un bookmark ?

Non. Les bookmarks sont propres à chaque job (et à chaque `transformation_ctx`). Deux jobs lisant la même source gardent des états indépendants.

#### Comment fonctionnent les bookmarks JDBC ?

On indique des `jobBookmarkKeys` (colonnes comme un identifiant croissant ou `updated_at`) et un ordre de tri ; le job lit les lignes dont les valeurs dépassent le dernier maximum stocké. Les mises à jour de lignes aux clés anciennes sont manquées : cela convient aux tables en ajout seul ou aux horodatages monotones.

### Workers, performances et coûts

#### Quels types de workers Glue propose-t-il ?

G.1X (1 DPU : 4 vCPU, 16 Go), G.2X (2 DPU), G.4X (4 DPU), G.8X (8 DPU) et des types plus grands sur les versions récentes, G.025X (0,25 DPU, pour le streaming à faible volume) et des types R optimisés pour la mémoire. Les workers plus gros conviennent aux transformations gourmandes en mémoire ; davantage de workers conviennent au travail parallèle.

#### Comment choisir le nombre de workers ?

Partir du volume et de la complexité des données, activer l'autoscaling avec un maximum raisonnable, et regarder les métriques du job : si les executors sont inactifs, réduire ; si les stages déversent ou si les tâches attendent, augmenter ou prendre des workers plus gros. Mesurer le coût par exécution.

#### Comment diagnostiquer un job Glue lent ?

Activer les métriques du job, les métriques d'observabilité et la Spark UI (event logs dans S3), puis examiner la durée des stages, les tâches déséquilibrées, les volumes de shuffle et le spill, l'utilisation des executors et le nombre de fichiers en entrée. Job run insights pointe la ligne en échec et les causes fréquentes.

#### Qu'est-ce que le problème des petits fichiers dans Glue, et comment le traiter ?

Lire de nombreux petits fichiers crée beaucoup de tâches et de requêtes S3 et ralentit les jobs. Glue peut regrouper les fichiers à la lecture (`groupFiles: inPartition`, `groupSize`), et il faut écrire des fichiers moins nombreux et plus gros (repartition avant l'écriture, de 128 Mo à 1 Go par fichier) ou compacter les tables Iceberg.

```python
dyf = glue.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://lake/raw/clicks/"], "recurse": True,
                        "groupFiles": "inPartition", "groupSize": "134217728"},
    format="json")
```

#### Pourquoi convertir le CSV ou le JSON brut en Parquet ?

Parquet est en colonnes et compressé : Athena, Redshift Spectrum et Spark ne lisent que les colonnes utiles, sautent des groupes de lignes grâce aux statistiques et lisent beaucoup moins de données, ce qui réduit durée et coût.

#### Comment traiter le déséquilibre des données dans un job Glue ?

Comme dans Spark : s'appuyer sur l'Adaptive Query Execution (activée sur les versions récentes de Glue), diffuser les petites tables, isoler ou saler les clés chaudes, et repérer les tâches retardataires dans la Spark UI.

#### Comment réduire les coûts de Glue ?

Utiliser la dernière version de Glue (démarrage et exécution plus rapides), activer l'autoscaling, utiliser Flex pour les jobs non urgents, dimensionner correctement les workers, fixer des timeouts, traiter de façon incrémentale par partitions ou bookmarks, ne lire que les partitions et colonnes utiles, éviter les crawlers quand les tables peuvent être définies en code, et arrêter les endpoints de développement et les sessions inactives.

#### Qu'est-ce que la Spark UI de Glue ?

Une vue du Spark history server sur les event logs d'une exécution (activée avec `--enable-spark-ui` et un chemin de journaux S3), disponible dans la console Glue, pour analyser stages, tâches, stockage et plans SQL.

#### Que sont les métriques d'observabilité de Glue ?

Des métriques CloudWatch au niveau du job, du stage et de l'executor (CPU, mémoire, disque, shuffle, déséquilibre, utilisation des workers, débit) qui aident à repérer les goulots d'étranglement et à dimensionner les jobs.

#### Que nécessite `--enable-auto-scaling` ?

Glue 3.0 ou plus, un nombre maximal de workers et une charge qui varie d'un stage à l'autre. Glue ajuste alors les executors selon les tâches en attente.

#### Qu'est-ce que l'option de shuffle sur S3 de Glue ?

Une option (`--write-shuffle-files-to-s3`) qui écrit les données de shuffle de Spark dans S3 au lieu du disque local, évitant les erreurs « no space left on device » sur les jobs très shuffle, au prix d'un peu de vitesse.

#### Quand utiliser des workers G.2X ou plus gros plutôt que davantage de G.1X ?

Quand les executors manquent de mémoire (grosses jointures, lignes larges, grosses agrégations, transformations ML) ou déversent beaucoup. Si les tâches sont petites et nombreuses, davantage de petits workers donnent le même parallélisme au même prix.

#### Que sont les workers de type R (optimisés mémoire) ?

Des types de workers avec plus de mémoire par CPU, pour les jobs limités par la mémoire plutôt que par le CPU, comme de grosses jointures broadcast ou la mise en cache.

#### Comment estimer le coût d'un job Glue ?

Workers × DPU par worker × durée en heures × prix du DPU-heure. Par exemple 10 workers G.1X pendant 15 minutes font 10 × 1 × 0,25 = 2,5 DPU-heures, environ 1,10 USD à 0,44 USD le DPU-heure. Avec l'autoscaling, regardez les DPU-secondes réelles dans le détail de l'exécution.

#### Pourquoi les jobs Glue mettent-ils du temps à démarrer, et comment réduire ce délai ?

Glue provisionne l'environnement à chaque exécution. Depuis Glue 2.0, le démarrage prend de quelques secondes à environ une minute ; Flex peut être plus long. On le réduit avec des versions récentes, moins de modules installés au démarrage (wheels préconstruits), et en évitant de multiplier de minuscules jobs qui pourraient n'en faire qu'un.

#### Comment l'Adaptive Query Execution de Spark aide-t-elle dans Glue ?

Activée par défaut depuis Glue 4.0, elle fusionne les petites partitions de shuffle, convertit les jointures en broadcast quand un côté est petit et découpe les partitions déséquilibrées, ce qui améliore les performances sans réglage manuel.

#### Comment passer une configuration Spark à un job Glue ?

Avec le paramètre `--conf` (par exemple `--conf spark.sql.shuffle.partitions=400`), en sachant que certains réglages sont gérés par Glue et ne peuvent pas être modifiés.

#### Qu'est-ce qui rend les fichiers Parquet efficaces pour les requêtes ultérieures ?

L'organisation en colonnes, la compression (Snappy ou ZSTD), les statistiques par groupe de lignes pour les sauter, des tailles de fichiers raisonnables (quelques centaines de Mo) et le tri ou le partitionnement selon les colonnes de filtre courantes.

#### Comment la stratégie de partitionnement influe-t-elle sur Glue et Athena ?

Partitionnez selon les colonnes utilisées par la plupart des filtres (généralement la date), avec un nombre modéré de partitions contenant chacune assez de données ; trop fin (par heure et par client) crée des millions de partitions minuscules et une planification lente, trop grossier impose de grosses lectures.

### ETL en streaming

#### Que sont les jobs de streaming Glue ?

Des jobs Spark Structured Streaming de longue durée qui lisent depuis Kinesis Data Streams, Amazon MSK ou Kafka autogéré, transforment les enregistrements en micro-lots et écrivent dans S3, des formats de data lake, des bases ou d'autres flux.

#### Comment un job de streaming Glue gère-t-il les schémas ?

À partir d'une table du Data Catalog qui décrit le flux, du Glue Schema Registry, ou en inférant le schéma depuis les données. Les enregistrements non conformes peuvent être traités avec des types choice ou envoyés vers un chemin d'erreurs.

#### Qu'est-ce que la taille de fenêtre dans le streaming Glue ?

L'intervalle de chaque micro-lot (`windowSize`, par exemple 100 secondes) dans `forEachBatch`. Des fenêtres plus grandes réduisent les petits fichiers et la surcharge ; des fenêtres plus petites réduisent la latence.

#### Où un job de streaming conserve-t-il sa progression ?

Dans un emplacement de checkpoint sur S3, qui stocke les offsets et l'état pour que le job reprenne là où il s'est arrêté après un redémarrage ou une mise à jour.

#### Quand choisir le streaming Glue plutôt que Kinesis Data Firehose ou Managed Service for Apache Flink ?

Firehose pour une livraison simple vers S3, Redshift ou OpenSearch avec peu de transformation et sans code. Managed Flink pour du traitement de flux avec état et faible latence, avec une logique complexe en temps d'événement. Le streaming Glue quand l'équipe utilise déjà Spark, a besoin d'ETL en micro-lots vers un data lake et veut partager le code avec les jobs batch.

#### Comment éviter les petits fichiers produits par les jobs de streaming ?

Utiliser des fenêtres plus grandes, écrire dans des tables Iceberg ou Hudi et les compacter (ou s'appuyer sur la compaction du catalogue pour Iceberg), ou lancer un job de compaction séparé.

#### Quelles sources le streaming Glue peut-il lire ?

Amazon Kinesis Data Streams, Amazon MSK, Apache Kafka autogéré et (via des connecteurs) d'autres systèmes de streaming. Les sorties incluent S3, les tables Iceberg/Hudi/Delta, les bases JDBC et d'autres flux.

#### Comment les jobs de streaming Glue sont-ils facturés ?

Au DPU-heure tant qu'ils tournent, c'est-à-dire en continu ; les workers G.025X réduisent le coût pour les flux à faible volume. L'autoscaling aide face à un trafic variable.

#### Comment mettre à jour le code d'un job de streaming en cours ?

Arrêter le job et démarrer la nouvelle version avec le même emplacement de checkpoint, tant que les changements sont compatibles avec l'état stocké ; des changements incompatibles exigent un nouveau checkpoint et un plan pour rejouer ou ignorer des données.

#### Comment gérer les événements tardifs dans le streaming Glue ?

Avec les fenêtres en temps d'événement et les watermarks de Spark Structured Streaming pour les agrégations, ou en écrivant les événements dans des partitions par date d'événement et en laissant les jobs en aval retraiter les partitions récentes.

### Qualité des données et données sensibles

#### Qu'est-ce qu'AWS Glue Data Quality ?

Une fonction fondée sur la bibliothèque open source Deequ pour mesurer et superviser la qualité des données avec des règles écrites en DQDL (Data Quality Definition Language), exécutées dans des jobs Glue ou sur des tables du catalogue, avec recommandations, scores, détection d'anomalies et alertes.

#### À quoi ressemble un jeu de règles DQDL ?

```
Rules = [
    RowCount > 1000,
    IsComplete "order_id",
    IsUnique "order_id",
    ColumnValues "status" in ["paid", "refunded", "cancelled"],
    ColumnValues "amount" >= 0,
    Freshness "updated_at" <= 24 hours
]
```

#### Comment agir sur les résultats de qualité dans un job ?

Utiliser la transformation Evaluate Data Quality, puis aiguiller les lignes : garder celles qui passent, écrire celles qui échouent dans un emplacement de quarantaine, et faire échouer le job ou envoyer une alerte EventBridge quand le score global passe sous un seuil.

#### Qu'est-ce que la détection d'anomalies de qualité ?

Glue apprend des statistiques au fil des exécutions (nombre de lignes, valeurs distinctes, distributions) et signale les valeurs inhabituelles même sans seuils explicites, ce qui détecte des problèmes comme une chute soudaine de volume.

#### Qu'est-ce que la détection de données sensibles dans Glue ?

Une transformation qui recherche des données personnelles comme les noms, e-mails, numéros de téléphone, cartes bancaires et identifiants nationaux (avec des détecteurs par pays), et peut masquer, hacher ou signaler ce qu'elle trouve, ce qui aide à respecter le RGPD.

#### Comment recevoir des alertes en cas d'échec de qualité ?

Glue publie les résultats de qualité dans EventBridge et CloudWatch ; des règles peuvent envoyer des notifications via SNS ou déclencher des processus de correction.

#### Comment obtenir des recommandations de règles dans Glue Data Quality ?

Lancer une tâche de recommandation sur une table du catalogue : Glue profile les données et propose des règles DQDL (complétude, unicité, plages de valeurs, valeurs autorisées) qu'on revoit et modifie avant de les utiliser.

#### Que sont les règles composites en DQDL ?

Des règles combinées avec `and` et `or`, par exemple `(ColumnValues "status" = "paid") and (ColumnValues "amount" > 0)`, pour exprimer des conditions portant sur plusieurs colonnes.

#### Où sont stockés les résultats de qualité ?

Dans l'historique de la console Glue, dans des métriques CloudWatch, sous forme d'événements EventBridge et, en option, écrits dans S3 par le job, où on peut les interroger avec Athena pour suivre les tendances.

#### Comment vérifier l'intégrité référentielle avec Glue Data Quality ?

Avec des règles comme `ReferentialIntegrity`, qui compare une colonne à la colonne clé d'un autre jeu de données, ou `DatasetMatch` pour comparer deux jeux, en passant le jeu de référence comme source additionnelle.

### Orchestration

#### Que sont les triggers Glue ?

Des objets qui démarrent jobs et crawlers : planifiés (cron), conditionnels (quand d'autres jobs ou crawlers atteignent un état comme `SUCCEEDED`), à la demande, ou fondés sur des événements EventBridge (par exemple des lots d'événements S3).

#### Qu'est-ce qu'un workflow Glue ?

Un conteneur pour un graphe de triggers, crawlers et jobs représentant un pipeline ETL, avec une vue visuelle des exécutions, des propriétés d'exécution partagées (paramètres clé-valeur) et la possibilité de reprendre depuis une étape en échec.

#### Quand utiliser Step Functions ou Airflow plutôt que les workflows Glue ?

Quand le pipeline fait intervenir de nombreux services AWS (Lambda, EMR, Athena, SageMaker), exige des branchements complexes, des relances et une gestion d'erreurs, ou s'étend à d'autres systèmes. Step Functions s'intègre nativement à Glue (`startJobRun.sync`) ; Airflow (ou MWAA) dispose d'opérateurs Glue.

#### Comment déclencher un job Glue à l'arrivée d'un fichier dans S3 ?

Avec une règle EventBridge sur les événements S3 « Object Created » ciblant un workflow Glue (avec regroupement par nombre d'événements ou fenêtre de temps), avec des notifications S3 vers une Lambda qui appelle `StartJobRun`, ou avec une règle EventBridge qui démarre une machine à états Step Functions.

#### Comment démarrer un job Glue depuis Step Functions et attendre sa fin ?

```json
{
  "Type": "Task",
  "Resource": "arn:aws:states:::glue:startJobRun.sync",
  "Parameters": {
    "JobName": "curate-orders",
    "Arguments": { "--process_date.$": "$.date" }
  },
  "Retry": [{ "ErrorEquals": ["States.ALL"], "MaxAttempts": 2, "BackoffRate": 2 }],
  "Next": "RunAthenaChecks"
}
```

#### Que sont les propriétés d'exécution d'un workflow ?

Des paires clé-valeur partagées par tous les jobs d'une exécution de workflow, lues et mises à jour avec `get_workflow_run_properties` et `put_workflow_run_properties`, pour transmettre des valeurs comme une date de traitement d'une étape à l'autre.

#### Qu'est-ce que le prédicat d'un trigger conditionnel ?

La liste des jobs ou crawlers et des états qu'il surveille, avec une logique `AND` (toutes les conditions) ou `ANY` (une seule), par exemple « démarrer le job B quand le job A et le crawler C ont réussi ».

#### EventBridge peut-il démarrer directement un job Glue ?

EventBridge peut cibler nativement des workflows Glue ; pour un job isolé, le schéma courant est EventBridge vers Step Functions ou vers une Lambda qui appelle `StartJobRun`.

#### Comment reprendre un workflow en échec ?

Dans la console ou l'API Glue (`ResumeWorkflowRun`), en sélectionnant les nœuds en échec à relancer après correction ; les nœuds terminés ne sont pas relancés.

#### Comment passer la date de traitement d'un orchestrateur à un job Glue ?

En argument du job dans `StartJobRun` (`--process_date=2026-10-16`), calculé par l'orchestrateur à partir de la date logique du planning, jamais à partir de l'horloge du job lui-même.

### Sécurité et gouvernance

#### De quels droits IAM un job Glue a-t-il besoin ?

Un job s'exécute avec un rôle IAM que Glue assume. Il lui faut les droits de `AWSGlueServiceRole` (ou équivalents), l'accès aux chemins S3 qu'il lit et écrit, à l'emplacement du script, au répertoire temporaire, aux clés KMS, aux secrets Secrets Manager des connexions et à CloudWatch Logs.

#### Comment Lake Formation fonctionne-t-il avec Glue ?

Lake Formation ajoute des droits fins (au niveau base, table, colonne, ligne et cellule, et un contrôle d'accès par tags avec les LF-Tags) au-dessus du Data Catalog. Des services comme Athena, Redshift Spectrum, EMR et Glue (5.0+) appliquent ces droits à la lecture des données.

#### Que sont les LF-Tags ?

Des tags Lake Formation (paires clé-valeur comme `domain=sales`, `classification=pii`) attachés aux bases, tables et colonnes ; les droits s'accordent sur des expressions de tags, ce qui passe mieux à l'échelle que des droits table par table.

#### Comment les jobs Glue accèdent-ils aux bases situées dans un VPC ?

Via une connexion Glue avec VPC, sous-réseau et groupes de sécurité : Glue crée des interfaces réseau élastiques dans le sous-réseau. Celui-ci a besoin de routes vers la base et, pour accéder à S3, d'un endpoint passerelle S3 (ou d'un NAT pour Internet).

#### Comment chiffrer les données avec Glue ?

Avec des configurations de sécurité qui activent le chiffrement des sorties S3 (SSE-S3 ou SSE-KMS), de CloudWatch Logs et des job bookmarks ; le chiffrement du catalogue avec KMS ; et des mots de passe de connexion stockés dans Secrets Manager ou chiffrés dans le catalogue.

#### Comment éviter de coder en dur des identifiants dans les scripts Glue ?

Stocker les identifiants dans AWS Secrets Manager et référencer le secret dans la connexion Glue, ou le lire dans le script avec boto3 ; utiliser des rôles IAM pour les ressources AWS.

#### Comment auditer l'activité Glue ?

CloudTrail journalise les appels d'API Glue (modifications de jobs et du catalogue), CloudWatch Logs conserve la sortie des jobs, Lake Formation fournit des traces d'audit des accès aux données et AWS Config peut suivre la configuration des ressources.

#### Qu'est-ce qu'une configuration de sécurité Glue ?

Un ensemble nommé de réglages de chiffrement (mode de chiffrement S3 et clé KMS, chiffrement de CloudWatch Logs, chiffrement des job bookmarks) attaché aux jobs, crawlers et endpoints de développement.

#### Comment restreindre un job Glue à certains préfixes S3 ?

Donner à son rôle IAM une politique n'autorisant que les préfixes de bucket et les clés KMS nécessaires et, avec Lake Formation, n'accorder que les tables nécessaires ; évitez les droits larges du type `s3:*`.

#### Comment empêcher les jobs Glue d'accéder à Internet ?

Les exécuter avec une connexion VPC dans des sous-réseaux privés sans NAT gateway, utiliser des endpoints VPC pour S3, Glue, CloudWatch, KMS et Secrets Manager, et héberger les dépendances Python dans S3 ou un dépôt privé.

#### Qu'est-ce que le contrôle d'accès fin pour les jobs Spark Glue ?

Avec Glue 5.0 et Lake Formation, les jobs Spark peuvent appliquer les droits au niveau table, colonne, ligne et cellule définis dans Lake Formation, pour que le rôle du job ne voie que les données autorisées.

### Exploitation, CI/CD et intégration

#### Comment déployer des jobs Glue sous forme de code ?

Garder scripts et définitions de jobs dans Git, déployer avec CloudFormation, CDK, Terraform ou SAM : téléverser les scripts dans S3 et créer jobs, triggers, crawlers, connexions et tables du catalogue. Un pipeline de CI lance les tests, empaquette les bibliothèques en wheels et déploie dans chaque environnement.

#### Comment tester la logique des jobs Glue ?

Placer la logique de transformation dans des fonctions qui prennent et renvoient des DataFrames, les tester avec pytest sur une SparkSession locale ou l'image Docker de Glue, tester le job de bout en bout sur des données d'exemple dans un compte de dev, et ajouter des règles de qualité pour les contrôles à l'exécution.

#### Comment superviser les jobs Glue en production ?

Avec les métriques et alarmes CloudWatch (échecs, durée, consommation de DPU), les événements EventBridge de changement d'état envoyés vers SNS ou Slack, job run insights pour les erreurs, et des tableaux de bord des durées et coûts des jobs dans le temps.

#### Comment gérer les échecs de jobs ?

Des relances pour les erreurs transitoires (uniquement pour des jobs idempotents), des alertes sur les états `FAILED` et `TIMEOUT`, une procédure de relance paramétrée pour la période en échec, et des chemins de quarantaine ou dead-letter pour les données défectueuses.

#### Qu'est-ce que le zero-ETL dans le contexte de Glue ?

Des intégrations gérées qui répliquent des données depuis des sources (applications SaaS comme Salesforce, SAP ou ServiceNow, et bases AWS comme DynamoDB) vers des cibles comme les tables de SageMaker Lakehouse ou Redshift sans construire de pipelines ETL, en les maintenant synchronisées.

#### Qu'est-ce qu'Amazon Q data integration dans Glue ?

Un assistant d'IA générative qui crée des jobs et transformations ETL Glue à partir de descriptions en langage naturel et aide à dépanner les jobs ; il existe aussi une mise à niveau assistée par l'IA des scripts Spark vers des versions plus récentes de Glue.

#### Comment Glue et Athena fonctionnent-ils ensemble ?

Glue catalogue et transforme les données ; Athena interroge les tables du catalogue en SQL. Les jobs Glue convertissent souvent les données brutes en Parquet ou Iceberg partitionnés pour que les requêtes Athena soient rapides et peu coûteuses.

#### Comment Glue et AWS DMS fonctionnent-ils ensemble ?

DMS réplique des bases (chargement complet et CDC) dans S3 sous forme de fichiers avec indicateurs d'opération ; des jobs Glue appliquent ensuite les changements aux tables curées, typiquement avec `MERGE` sur des tables Iceberg ou Hudi.

#### Comment passer un job Glue à une version plus récente ?

Changer la version de Glue dans une copie de dev, lancer les tests et comparer sorties et durées, lire les notes de migration (changements de Spark, Python et bibliothèques), vérifier connecteurs et JAR, puis promouvoir via la CI.

#### Comment structurer le dépôt d'un projet Glue ?

Séparer les scripts d'entrée des jobs, un paquet Python partagé contenant la logique de transformation (construit en wheel), les tests, l'infrastructure as code (CDK, Terraform ou CloudFormation), les jeux de règles de qualité et la configuration par environnement.

#### Comment versionner les scripts Glue ?

Les garder dans Git et déployer des copies versionnées dans S3 (par exemple avec le SHA du commit dans le chemin), pour que chaque définition de job pointe vers une version connue du script et qu'un retour arrière consiste à repointer vers la précédente.

#### Comment alerter sur des jobs Glue trop longs ?

Fixer le timeout du job, ajouter une alarme CloudWatch sur le temps écoulé ou la métrique `glue.driver.aggregate.elapsedTime`, ou faire alerter l'orchestrateur quand une étape dépasse sa durée attendue.

#### Comment partager des tables Glue avec Amazon Redshift ?

Créer dans Redshift un schéma externe pointant vers une base Glue (`CREATE EXTERNAL SCHEMA ... FROM DATA CATALOG`), puis interroger les tables avec Redshift Spectrum, ou utiliser l'accès au Data Catalog monté automatiquement dans Redshift.

#### Comment EMR utilise-t-il le Glue Data Catalog ?

Les clusters EMR et EMR Serverless peuvent être configurés pour utiliser le Glue Data Catalog comme Hive metastore, de sorte que Spark, Hive, Presto et Trino sur EMR partagent les mêmes définitions de tables qu'Athena et Glue.

#### À quoi servent AWS Glue for SAP et les autres connecteurs SaaS ?

À extraire les données d'applications d'entreprise (SAP OData, Salesforce, ServiceNow, Zendesk et d'autres) via des connecteurs gérés vers des jobs Glue ou des intégrations zero-ETL, sans écrire de code d'API.

### Mises en situation

#### Concevez un pipeline qui transforme des dépôts CSV quotidiens dans S3 en jeu de données partitionné et interrogeable.

Déposer les CSV sous un préfixe raw daté, lancer un job Spark Glue (déclenché par EventBridge ou un planning) qui lit les fichiers du jour avec un schéma défini, nettoie et convertit les types, écrit en Parquet ou Iceberg partitionné par date dans un préfixe curé, met à jour le catalogue et exécute des règles de qualité. Athena ou Redshift Spectrum interrogent la table curée ; Lake Formation contrôle l'accès.

#### Un crawler crée des dizaines de tables au lieu d'une. Qu'est-ce qui ne va pas ?

Les fichiers sous le préfixe ont des schémas ou des arborescences incohérents (colonnes supplémentaires, formats différents, fichiers égarés). Corriger l'organisation de la source, ajouter des motifs d'exclusion, utiliser « create a single schema for each S3 path », ou définir la table explicitement au lieu de crawler.

#### Un job Glue qui prenait 10 minutes en prend maintenant 2 heures. Comment enquêtez-vous ?

Je compare le volume et le nombre de fichiers en entrée, je vérifie si le pushdown predicate ou les bookmarks ont cessé de fonctionner (tout est retraité), je cherche du déséquilibre ou du spill dans la Spark UI, je contrôle le nombre de workers et l'autoscaling, et je cherche une jointure modifiée ou un broadcast perdu.

#### Votre job Glue échoue avec « No space left on device ». Que faites-vous ?

Le job déverse ou redistribue plus que le disque local ne peut contenir. J'utilise des workers plus gros (plus de disque par executor), j'active l'option de shuffle sur S3, je réduis les données avant les shuffles (filtrer et sélectionner plus tôt), je corrige le déséquilibre et j'augmente les partitions pour que chaque tâche traite moins de données.

#### Les requêtes Athena sur la table Glue échouent avec `HIVE_PARTITION_SCHEMA_MISMATCH`. Pourquoi ?

Certaines partitions ont été enregistrées avec un schéma différent de celui de la table (un crawler a mis à jour une partition après un changement de la source). Je fais hériter aux partitions le schéma de la table (réglage du crawler « update all new and existing partitions with metadata from the table »), je corrige ou réécris les partitions divergentes et je stabilise le schéma de la source.

#### Comment charger le CDC d'une base RDS PostgreSQL dans un lakehouse avec Glue ?

Utiliser DMS pour le chargement complet et le CDC vers S3 (Parquet avec une colonne d'opération), ou une intégration zero-ETL si elle existe. Un job Glue lit les nouveaux fichiers de changements (bookmarks ou partitions par date), déduplique par clé en gardant le dernier changement et exécute `MERGE INTO` sur une table Iceberg enregistrée dans le Data Catalog. La compaction et l'expiration des snapshots la maintiennent en bonne santé.

#### Comment exécuter le même job Glue en dev, staging et prod ?

Un seul script paramétré pour les chemins, bases et connexions, déployé par infrastructure as code pour chaque environnement (idéalement dans des comptes séparés), avec des arguments de job et des rôles IAM propres à chaque environnement, promu via la CI après les tests.

#### Comment expliquer AWS Glue à un interlocuteur non technique ?

C'est le service d'AWS qui tient l'inventaire des données de l'entreprise, et qui nettoie et déplace ces données pour les mettre en forme pour les rapports et les analyses, sans avoir à gérer de serveurs.

#### Vous devez dédupliquer des fiches clients sans clé commune entre deux systèmes. Quel outil Glue peut aider ?

La transformation ML FindMatches : étiqueter des exemples de paires correspondantes et non correspondantes, entraîner la transformation et l'exécuter dans un job pour attribuer des identifiants de correspondance, puis fusionner les enregistrements par identifiant avec des règles métier.

#### Un job Glue écrit des milliers de minuscules fichiers Parquet par jour. Comment corriger ?

Faire un repartition par la colonne de partition avant l'écriture pour que chaque partition ait peu de fichiers, augmenter la taille des lots (traiter une journée plutôt que toutes les quelques minutes) et, avec Iceberg, activer la compaction du catalogue ou lancer `rewrite_data_files`.

#### Comment migrer des jobs SSIS ou Informatica on-premise vers Glue ?

Inventorier les jobs et leurs dépendances, recréer les sources sous forme de connexions Glue, réécrire les transformations en PySpark (ou en jobs visuels), stocker les données de référence dans S3 ou le catalogue, orchestrer avec Step Functions ou Airflow, et valider les sorties côte à côte avant de basculer.

#### Les analystes trouvent coûteuses les requêtes Athena sur les tables Glue. Que changez-vous dans les jobs Glue ?

Écrire du Parquet ou de l'Iceberg au lieu de CSV/JSON, compresser, partitionner selon les filtres courants, produire des fichiers moins nombreux et plus gros, calculer des statistiques de colonnes, et éventuellement créer des tables agrégées pour les dashboards fréquents.

#### Un système source ajoute des colonnes sans prévenir. Comment garder le pipeline Glue en marche ?

Lire en tenant compte de l'évolution du schéma : DynamicFrames ou schémas permissifs en raw, sélection explicite des colonnes dans les sorties curées, alerte sur les nouvelles colonnes (mode journalisation seule du crawler ou contrôle de schéma), et évolution de schéma Iceberg pour ajouter les colonnes de façon délibérée.

#### Comment corriger les « données tardives » dans un pipeline Glue quotidien ?

Traiter une fenêtre glissante (par exemple les trois derniers jours) à chaque exécution avec écrasement de partitions ou `MERGE`, pour que les enregistrements tardifs mettent à jour les bonnes partitions, en gardant la fenêtre paramétrable pour des corrections plus larges.

#### Comment choisir entre Glue, EMR Serverless et Databricks pour une nouvelle plateforme de données sur AWS ?

Glue pour de l'ETL serverless étroitement intégré au catalogue AWS et à Lake Formation ; EMR Serverless pour du Spark/Hive open source avec plus de contrôle et souvent un coût moindre à grande échelle ; Databricks pour une plateforme lakehouse unifiée avec notebooks collaboratifs, Delta, Unity Catalog et ML. Les compétences de l'équipe, les exigences de gouvernance et les modèles de coût tranchent.
