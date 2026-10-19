## Fiche d'étude AWS Glue

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude AWS Glue : environ 200 questions](../../images/aws_glue_study_guide_title_img.png)

Environ 200 questions d'entretien sur AWS Glue : le Data Catalog, les crawlers, les jobs ETL Spark, les DynamicFrames, les job bookmarks, les workers et les coûts, le streaming, la qualité des données, l'orchestration, la sécurité avec Lake Formation et l'optimisation des performances. Les réponses décrivent le service tel qu'il est en 2026.

La fiche suit un parcours d'apprentissage en quatre étapes. Chaque section est découpée en unités courtes : objectifs d'apprentissage, explication du concept et exemple commenté, puis questions (d'abord de mémorisation, ensuite d'application), un exercice pratique et les points à retenir. Pour **apprendre**, lisez chaque unité du début à la fin. Pour **réviser**, passez en mode révision ou utilisez « Aller aux questions », marquez les réponses à revoir et essayez une révision mixte entre les sections.

<!-- QA -->
<!-- stage: Fondamentaux -->

### Fondamentaux

<!-- unit: Ce qu'est Glue -->

<!-- goals -->

- Expliquer ce que fait AWS Glue et quels sont ses composants.
- Situer Glue dans un data lake AWS, pour l'ETL et l'ELT.

<!-- concept -->

Un data lake a besoin de deux choses en plus du stockage : une description partagée de ce que sont les données, et des jobs qui transforment les fichiers bruts en tables utiles. Glue fournit les deux. Son catalogue est l'inventaire que lisent Athena, Redshift et EMR ; ses crawlers le remplissent ; ses jobs Spark serverless font la transformation.

« Serverless » signifie ici que l'on choisit une taille et que l'on paie à la seconde, sans cluster allumé en permanence. Cela convient au batch qui tourne quelques fois par jour et reste inactif entre-temps.

<!-- example -->

```text
sources ─► S3 raw ─► Glue job (Spark) ─► S3 curated (Parquet/Iceberg)
                │                               │
                └──────► Glue Data Catalog ◄────┘ ◄── Athena, Redshift, EMR
```

#### Qu'est-ce qu'AWS Glue ?

Un service serverless d'intégration de données sur AWS pour découvrir, préparer, déplacer et intégrer des données. Ses principaux éléments sont le Glue Data Catalog (un référentiel central de métadonnées), les crawlers (découverte de schémas), les jobs ETL (Apache Spark ou Python), Glue Studio (conception visuelle), Data Quality, DataBrew (préparation visuelle des données) et les workflows pour l'orchestration.

#### Que signifie « serverless » pour Glue ?

Vous ne provisionnez ni ne gérez de clusters : vous choisissez un type et un nombre de workers (ou laissez l'autoscaling décider), Glue démarre l'environnement pour l'exécution du job, et vous ne payez que la durée d'exécution, à la seconde.

#### Quels sont les principaux cas d'usage de Glue ?

Construire des data lakes sur S3 (cataloguer et transformer les données brutes en Parquet ou Iceberg), l'ETL vers Redshift ou d'autres bases, préparer des données pour Athena et le machine learning, l'ingestion CDC et streaming, et fournir un catalogue de métadonnées partagé pour Athena, EMR, Redshift Spectrum et Lake Formation.

#### Quels sont les principaux composants d'AWS Glue, en une phrase chacun ?

Le Data Catalog stocke les métadonnées ; les crawlers découvrent les schémas ; les jobs ETL transforment les données avec Spark ou Python ; les triggers et workflows orchestrent ; Glue Studio permet la conception visuelle ; Data Quality valide les données ; DataBrew prépare les données visuellement ; le Schema Registry gouverne les schémas de streaming.

#### Comment Glue s'intègre-t-il dans l'architecture data lake d'AWS ?

Les données arrivent dans S3 (depuis DMS, Kinesis, AppFlow, des dépôts), les crawlers ou les jobs les enregistrent dans le Data Catalog, les jobs Glue les nettoient et les convertissent en zones curées (Parquet ou Iceberg), Lake Formation gouverne l'accès, et Athena, Redshift, EMR, QuickSight et SageMaker les consomment.

#### Qu'est-ce que l'ETL par rapport à l'ELT dans le contexte de Glue ?

En ETL, les jobs Glue transforment les données avant de les charger dans la cible (par exemple nettoyer et convertir en Parquet avant Redshift). En ELT, les données brutes sont chargées d'abord et transformées dans la cible (SQL Redshift, dbt sur Athena). Glue sert souvent au « E » et au « L » de l'ELT, ou au « T » dans un lakehouse.

#### Comment expliquer AWS Glue à un interlocuteur non technique ?

C'est le service d'AWS qui tient l'inventaire des données de l'entreprise, et qui nettoie et déplace ces données pour les mettre en forme pour les rapports et les analyses, sans avoir à gérer de serveurs.

<!-- challenge -->

Une équipe écrit des scripts Python sur une instance EC2 qui convertissent chaque nuit des CSV en Parquet. Qu'apporterait Glue, et que leur resterait-il à concevoir ?

<!-- solution -->

Glue supprimerait le serveur, ferait passer la conversion à l'échelle avec Spark, enregistrerait les tables dans le catalogue et suivrait les exécutions. L'équipe décide toujours du partitionnement, de la taille des fichiers, de la logique incrémentale, des calendriers et des règles de qualité.

<!-- takeaways -->

- Glue combine catalogue, crawlers et jobs Spark serverless.
- Athena, Redshift et EMR partagent le catalogue.
- Le serverless convient au batch entrecoupé de périodes d'inactivité.

<!-- unit: Glue parmi les services AWS -->

<!-- goals -->

- Comparer Glue avec EMR, Lambda, DataBrew et d'autres plateformes.
- Choisir un service de traitement pour une charge.

<!-- concept -->

AWS propose plusieurs façons d'exécuter des transformations, qui diffèrent surtout par ce que l'on gère et par la taille du travail. Lambda traite de petits fichiers déclenchés par des événements. Glue traite l'ETL batch avec Spark sans clusters. EMR traite les charges qui exigent un contrôle total ou de nombreux moteurs open source. DataBrew offre aux analystes un outil visuel.

Le catalogue Glue est sous la plupart d'entre eux : on peut changer de moteur sans déplacer les métadonnées.

<!-- example -->

| Charge | Bon choix |
|---|---|
| Transformer chaque fichier de 2 Mo à son arrivée | Lambda |
| CSV nocturne de 500 Go vers Parquet | Glue |
| Spark longue durée avec réglages maison et tuning Hudi | EMR |
| Un analyste nettoie visuellement un jeu de type tableur | DataBrew |

#### Comment Glue se compare-t-il à Amazon EMR ?

Glue est serverless et centré sur l'ETL avec Spark, avec catalogue, bookmarks et qualité intégrés ; on échange du contrôle contre de la simplicité. EMR (sur EC2, EKS ou Serverless) donne le contrôle total de Spark, Hadoop, Hive, Trino et d'autres frameworks, de leurs versions et de leur réglage, et revient souvent moins cher pour des charges importantes et régulières.

#### Comment Glue se compare-t-il à AWS Lambda pour l'ETL ?

Lambda convient aux petites transformations événementielles (un fichier de quelques Mo), avec une limite de 15 minutes et une mémoire limitée. Glue convient au traitement distribué plus lourd avec Spark, aux exécutions longues et aux gros volumes.

#### Qu'est-ce qu'AWS Glue DataBrew ?

Un outil visuel de préparation des données doté de plus de 250 transformations intégrées, utilisé par les analystes pour nettoyer et normaliser des données sans code. Les transformations sont enregistrées en recettes et exécutées en jobs sur des données S3, avec du profilage.

#### Quel lien entre Glue et SageMaker Lakehouse/Unified Studio ?

Le Glue Data Catalog est la base de métadonnées de SageMaker Lakehouse, et les fonctions d'intégration de Glue (jobs ETL, ETL visuel, connexions, zero-ETL) sont disponibles dans SageMaker Unified Studio, l'environnement unifié d'AWS pour les données, l'analytique et l'IA.

#### Comment choisir entre Glue, EMR Serverless et Databricks pour une nouvelle plateforme de données sur AWS ?

Glue pour de l'ETL serverless étroitement intégré au catalogue AWS et à Lake Formation ; EMR Serverless pour du Spark/Hive open source avec plus de contrôle et souvent un coût moindre à grande échelle ; Databricks pour une plateforme lakehouse unifiée avec notebooks collaboratifs, Delta, Unity Catalog et ML. Les compétences de l'équipe, les exigences de gouvernance et les modèles de coût tranchent.

<!-- challenge -->

Une Lambda qui convertit les fichiers déposés dépasse désormais son timeout car certains fichiers font 3 Go. Que recommandez-vous ?

<!-- solution -->

Déplacer le traitement des gros fichiers vers un job Glue (déclenché par EventBridge ou un calendrier), sans limite de 15 minutes et qui passe à l'échelle avec Spark. Garder Lambda pour les petits fichiers ou pour lancer le job Glue.

<!-- takeaways -->

- Lambda pour les petits événements ; Glue pour l'ETL batch Spark ; EMR pour le contrôle.
- DataBrew sert visuellement les analystes.
- Le catalogue Glue est partagé entre moteurs.

<!-- unit: Facturation, versions et limites -->

<!-- goals -->

- Expliquer les DPU et estimer la facturation des jobs Glue.
- Choisir les versions de Glue et connaître les principaux quotas.

<!-- concept -->

Le prix de Glue est simple : capacité multipliée par le temps. Une DPU est une quantité fixe de CPU et de mémoire, payée à la seconde pendant l'exécution d'un job. Le coût dépend donc du bon dimensionnement et d'une fin rapide, pas directement du volume de données.

Chaque version de Glue embarque une version de Spark et de Python, ce qui influe sur la vitesse, le démarrage et les fonctions disponibles. Catalogues régionaux, quotas de service et outils de développement complètent le tableau.

<!-- example -->

```text
10 G.1X workers × 1 DPU × 0.25 h × 0.44 USD/DPU-hour ≈ 1.10 USD per run
same job on Glue 5.0, 40% faster          ≈ 0.66 USD per run
```

#### Qu'est-ce qu'un DPU ?

Une Data Processing Unit : 4 vCPU et 16 Go de mémoire. Glue facture les jobs ETL, les crawlers et les sessions interactives en DPU-heures, à la seconde.

#### Comment un job Glue est-il facturé ?

Au DPU-heure, à la seconde, avec un minimum d'une minute pour les jobs Spark depuis Glue 2.0. Le coût vaut nombre de DPU × durée × prix du DPU-heure (environ 0,44 USD dans de nombreuses régions, moins en Flex). Les jobs Python shell facturent 1/16 ou 1 DPU.

#### Que sont les versions de Glue, et pourquoi comptent-elles ?

Chaque version de Glue embarque une version de Spark, Python et Java et des connecteurs : par exemple Glue 4.0 utilise Spark 3.3 et Python 3.10, et Glue 5.0 Spark 3.5 et Python 3.11. Les versions récentes démarrent et s'exécutent plus vite et prennent en charge des formats de table plus récents. Les anciennes perdent leur support : les mises à jour font partie de la maintenance.

#### Quels quotas de service Glue faut-il connaître ?

Les limites d'exécutions de jobs simultanées par compte, de DPU maximum par job, de nombre de jobs, triggers, crawlers, bases, tables et partitions par table. La plupart sont ajustables via Service Quotas ; les grands data lakes atteignent d'abord les limites de partitions et de concurrence.

#### Dans quelles régions Glue est-il disponible, et le catalogue est-il régional ?

Glue est disponible dans la plupart des régions AWS, et le Data Catalog est régional : chaque région a son propre catalogue par compte. L'accès inter-régions exige de répliquer les métadonnées ou d'utiliser des resource links Lake Formation.

#### Qu'est-ce que Glue Studio ?

L'interface console pour créer, exécuter et superviser des jobs Glue : un éditeur visuel où l'on construit l'ETL sous forme de graphe de sources, transformations et cibles (qui génère du code PySpark), un éditeur de scripts, un éditeur de notebooks et des tableaux de bord de supervision.

#### Qu'est-ce qu'un development endpoint, et qu'est-ce qui l'a remplacé ?

Un ancien environnement toujours allumé pour développer des scripts Glue depuis des notebooks, facturé tant qu'il tournait. Les sessions interactives et les notebooks de Glue Studio l'ont remplacé, à la demande, facturés à la seconde avec des délais d'inactivité.

<!-- challenge -->

Un job sous Glue 2.0 tourne 40 minutes sur 20 workers G.1X chaque heure. Citez deux changements susceptibles de réduire son coût.

<!-- solution -->

Passer à la dernière version de Glue (Spark plus récent, exécution et démarrage plus rapides) et activer l'auto scaling pour réduire les workers quand les étapes en demandent moins. Puis vérifier si les exécutions horaires pourraient être incrémentales.

<!-- takeaways -->

- On paie DPU × temps, à la seconde.
- Les versions récentes de Glue sont souvent plus rapides et moins chères.
- Le catalogue est régional ; les quotas limitent la concurrence.

### Data Catalog

<!-- unit: Bases de données et tables -->

<!-- goals -->

- Décrire ce que stocke le Data Catalog et comment les tables y arrivent.
- Utiliser les propriétés de table et comprendre le sens de « externe ».

<!-- concept -->

Le Data Catalog est un metastore : il stocke des descriptions de données, jamais les données. Les bases regroupent des tables, et chaque table enregistre un emplacement, un schéma, un format et des propriétés qui indiquent aux moteurs comment lire les fichiers. Tous les services analytiques lisant les mêmes entrées, une propriété erronée casse les requêtes partout.

Les tables peuvent naître de crawlers, de DDL, de jobs ou d'infrastructure as code. Pour vos propres pipelines, les définitions explicites sont plus prévisibles que la découverte.

<!-- example -->

```python
glue.create_table(DatabaseName="curated", TableInput={
    "Name": "orders",
    "StorageDescriptor": {
        "Columns": [{"Name": "order_id", "Type": "bigint"}, {"Name": "amount", "Type": "decimal(12,2)"}],
        "Location": "s3://lake/curated/orders/",
        "InputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
        "SerdeInfo": {"SerializationLibrary": "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"}},
    "PartitionKeys": [{"Name": "dt", "Type": "string"}],
    "Parameters": {"classification": "parquet"}})
```

#### Qu'est-ce que le Glue Data Catalog ?

Un référentiel de métadonnées géré, compatible avec le Hive metastore, par compte et par région. Il stocke des bases de données, des tables (schéma, emplacement, format, partitions, statistiques), des connexions et des fonctions définies par l'utilisateur. Athena, EMR, Redshift Spectrum, les jobs Glue et bien d'autres services l'utilisent pour savoir où sont les données et comment les lire.

#### Qu'est-ce qu'une base de données Glue ?

Un conteneur logique de tables dans le Data Catalog. Elle ne stocke pas de données ; elle regroupe des définitions de tables, et Lake Formation permet d'accorder des droits au niveau de la base.

#### Qu'est-ce qu'une table Glue ?

Des métadonnées qui décrivent des données : noms et types des colonnes, emplacement S3 (ou source JDBC), format (SerDe et formats d'entrée et de sortie), clés de partition et propriétés de la table. Les données restent dans S3 ou dans la base source.

#### Comment les tables arrivent-elles dans le Data Catalog ?

Par des crawlers, par création manuelle (console, `CREATE EXTERNAL TABLE` dans Athena, CloudFormation, Terraform, l'API), par des jobs Glue qui créent ou mettent à jour les tables en écrivant (`enableUpdateCatalog`), ou par des services comme les blueprints de Lake Formation et les intégrations zero-ETL.

#### Quelle différence entre une table externe et une governed table ?

Dans le Data Catalog, toutes les tables sur S3 sont externes (le catalogue ne contient que les métadonnées ; supprimer la table ne supprime pas les données). Les governed tables étaient un type de table Lake Formation avec transactions ACID, aujourd'hui retiré au profit des tables Apache Iceberg.

#### À quoi servent les propriétés de table comme `classification` et `compressionType` ?

Elles indiquent aux moteurs et à Glue comment interpréter les données : `classification` (csv, json, parquet) est fixée par les crawlers et utilisée par les jobs Glue, tandis que les paramètres du SerDe et la compression indiquent à Athena ou Hive comment lire les fichiers.

#### Qu'est-ce qu'une fonction définie par l'utilisateur dans le Data Catalog ?

Les métadonnées d'une UDF Hive (nom de classe et emplacement du JAR) stockées dans le catalogue pour que des moteurs comme Hive sur EMR puissent l'utiliser ; c'est surtout utile pour les charges compatibles Hive.

<!-- challenge -->

Quelqu'un supprime une table du catalogue « pour faire le ménage » et les requêtes Athena échouent. Les données sont-elles perdues ? Comment restaurer la table ?

<!-- solution -->

Non, les tables sur S3 sont externes : les fichiers sont toujours là. Recréez la table depuis sa définition en code (ou une version du catalogue, ou le DDL Athena), puis réenregistrez les partitions ou relancez le crawler.

<!-- takeaways -->

- Le catalogue stocke des métadonnées ; les données restent dans S3.
- Tous les moteurs lisent les mêmes entrées de table.
- Définissez explicitement en code les tables de vos pipelines.

<!-- unit: Partitions et statistiques -->

<!-- goals -->

- Enregistrer des partitions et les garder cohérentes avec la table.
- Accélérer la planification avec index de partitions et statistiques de colonnes.

<!-- concept -->

Les partitions sont aussi des entrées du catalogue, une par dossier, chacune avec son emplacement et son schéma. Deux conséquences : les moteurs ne sautent que les partitions enregistrées, et les partitions peuvent diverger de la table quand on met à jour l'une sans l'autre.

Quand les partitions se multiplient, même les lister devient lent. Les index de partitions laissent le catalogue filtrer côté serveur, et les statistiques de colonnes aident les optimiseurs à planifier les jointures.

<!-- example -->

```python
glue.batch_create_partition(DatabaseName="curated", TableName="orders",
    PartitionInputList=[{"Values": ["2026-10-17"],
        "StorageDescriptor": {**table_sd, "Location": "s3://lake/curated/orders/dt=2026-10-17/"}}])
```

#### Qu'est-ce qu'une partition dans le Data Catalog ?

Un sous-ensemble des données d'une table défini par des valeurs de clés de partition (par exemple `year=2026/month=10/day=15`), chacun avec son propre emplacement S3. Les moteurs de requête ne lisent que les partitions qui correspondent aux filtres, ce qui réduit coût et durée.

#### Comment enregistre-t-on les nouvelles partitions ?

Par un crawler, par `MSCK REPAIR TABLE` ou `ALTER TABLE ADD PARTITION` dans Athena, par l'API `BatchCreatePartition`, par des jobs Glue qui écrivent avec mise à jour du catalogue, ou en s'en passant grâce à la projection de partitions d'Athena.

#### Que sont les index de partition ?

Des index sur les clés de partition des tables du catalogue qui en ont beaucoup, pour que les appels `GetPartitions` filtrés répondent vite au lieu de parcourir toutes les partitions. Ils accélèrent la planification des requêtes Athena et Glue sur des tables à des dizaines de milliers de partitions.

#### Que sont les statistiques de colonnes du Data Catalog ?

Des statistiques (nombre de valeurs distinctes, nulls, min/max, longueur moyenne) calculées par Glue pour les colonnes des tables et stockées dans le catalogue, qu'Athena et Redshift Spectrum utilisent pour l'optimisation basée sur les coûts, comme le réordonnancement des jointures.

#### Les requêtes Athena sur la table Glue échouent avec `HIVE_PARTITION_SCHEMA_MISMATCH`. Pourquoi ?

Certaines partitions ont été enregistrées avec un schéma différent de celui de la table (un crawler a mis à jour une partition après un changement de la source). Je fais hériter aux partitions le schéma de la table (réglage du crawler « update all new and existing partitions with metadata from the table »), je corrige ou réécris les partitions divergentes et je stabilise le schéma de la source.

<!-- challenge -->

Une table de 300 000 partitions met 40 secondes à se planifier dans Athena, même pour un jour. Qu'ajoutez-vous ?

<!-- solution -->

Un index de partitions sur la clé de date, pour que `GetPartitions` filtre côté serveur, ou passer la table en partition projection. Vérifiez aussi si la granularité est plus fine que ce que les requêtes demandent.

<!-- takeaways -->

- Les partitions sont des entrées du catalogue avec leur propre schéma.
- Des schémas de partition décalés cassent les requêtes.
- Index de partitions et statistiques accélèrent la planification.

<!-- unit: Formats, connections et schémas -->

<!-- goals -->

- Connaître les formats de table et connections pris en charge par le catalogue.
- Versionner les schémas des tables et des flux.

<!-- concept -->

Le catalogue décrit plus que des dossiers. Il enregistre des formats de table ouverts comme Iceberg, dont les métadonnées suivent les fichiers, et peut les entretenir en compactant automatiquement. Il stocke des connections aux bases pour que jobs et crawlers n'embarquent ni URL ni identifiants.

Les schémas changent : le catalogue garde des versions de tables, et le Schema Registry versionne les schémas des données de streaming avec des règles de compatibilité qui bloquent les changements cassants.

<!-- example -->

```python
# connection referencing a secret instead of a password
glue.create_connection(ConnectionInput={
    "Name": "orders_pg", "ConnectionType": "JDBC",
    "ConnectionProperties": {"JDBC_CONNECTION_URL": "jdbc:postgresql://db:5432/shop",
                             "SECRET_ID": "prod/orders_pg"}})
```

#### Quels formats de table le Data Catalog prend-il en charge ?

Les tables de style Hive en Parquet, ORC, Avro, JSON, CSV et d'autres formats, et les formats de table ouverts Apache Iceberg, Apache Hudi et Delta Lake. Iceberg est le plus profondément intégré aux services AWS.

#### Que sont les optimisations du catalogue pour les tables Iceberg ?

La maintenance gérée des tables Iceberg du Data Catalog : compaction automatique des petits fichiers, rétention des snapshots (expiration des anciens) et suppression des fichiers orphelins, configurées par table et exécutées par Glue sans jobs maison.

#### Qu'est-ce qu'une connexion Glue ?

Un objet du catalogue qui stocke les propriétés de connexion à un stockage de données : URL JDBC, identifiants (de préférence un secret Secrets Manager), VPC, sous-réseau et groupes de sécurité, ou propriétés pour Kafka, MongoDB, Snowflake, BigQuery et d'autres connecteurs natifs. Les jobs et crawlers y font référence.

#### Qu'est-ce que le Glue Schema Registry ?

Un service pour stocker, versionner et valider des schémas (Avro, JSON Schema, Protobuf) de données en streaming, avec des règles de compatibilité (backward, forward, full). Les producteurs et consommateurs utilisant Kafka, MSK, Kinesis ou Lambda sérialisent et valident les enregistrements selon les schémas enregistrés.

#### Comment versionner les schémas de tables dans le Data Catalog ?

Le catalogue conserve automatiquement des versions d'une table quand elle est mise à jour (jusqu'à une limite), ce qui permet de voir et comparer les anciens schémas avec `GetTableVersions`. Les tables Iceberg conservent aussi l'historique du schéma dans leurs propres métadonnées.

<!-- challenge -->

Un producteur Kafka a changé un champ de `int` en `string` et cassé trois consommateurs. Quelle fonction de Glue l'aurait évité ?

<!-- solution -->

Le Glue Schema Registry avec un mode de compatibilité comme `BACKWARD` : le sérialiseur du producteur aurait rejeté la version incompatible avant l'envoi du moindre message.

<!-- takeaways -->

- Le catalogue enregistre tables de style Hive et formats ouverts.
- Les connections sortent URL et secrets du code.
- Versions de tables et Schema Registry suivent les changements de schéma.

<!-- unit: Partager et gérer le catalogue -->

<!-- goals -->

- Partager des catalogues entre comptes et les interroger par programme.
- Garder un catalogue propre et comprendre son coût.

<!-- concept -->

Dans les organisations multi-comptes, un catalogue sert souvent de nombreuses équipes. Le partage passe par Lake Formation et les resource links, qui font apparaître localement des tables distantes sans copier de métadonnées, et chaque appel d'API peut désigner le catalogue visé.

Un catalogue partagé demande de l'entretien : conventions de nommage par couche, tables définies en code et suppression des tables laissées par des crawlers ou des expériences. Le problème est rarement la facture ; c'est la confusion.

<!-- example -->

```python
paginator = boto3.client("glue").get_paginator("get_tables")
for page in paginator.paginate(CatalogId="111122223333", DatabaseName="curated"):
    for t in page["TableList"]:
        print(t["Name"], t["StorageDescriptor"]["Location"])
```

#### Plusieurs comptes AWS peuvent-ils partager un Data Catalog ?

Oui. L'accès peut être accordé entre comptes par des politiques de ressources sur le catalogue ou, plus souvent, par des droits inter-comptes Lake Formation (souvent via AWS RAM), pour qu'un compte central de gouvernance partage bases et tables avec les comptes consommateurs.

#### Qu'est-ce que le catalog ID ?

L'identifiant du compte AWS propriétaire d'un Data Catalog. Les API et les requêtes peuvent référencer le catalogue d'un autre compte par son identifiant quand l'accès inter-comptes est accordé.

#### Qu'est-ce qu'un resource link ?

Un objet Lake Formation qui pointe vers une base ou une table partagée depuis un autre compte ou une autre région, pour que les utilisateurs l'interrogent comme si elle était locale dans leur catalogue.

#### Comment interroger le Data Catalog par programme ?

Avec l'API Glue (`GetDatabases`, `GetTables`, `GetPartitions`, `SearchTables`) via boto3 ou la CLI, ou en SQL via les vues `information_schema` d'Athena.

#### Comment le Data Catalog est-il facturé ?

Le premier million d'objets stockés et le premier million de requêtes par mois sont gratuits ; au-delà on paie par tranche de 100 000 objets et par million de requêtes. Le calcul des statistiques et les optimisations Iceberg sont facturés à part en DPU-heures.

#### Comment garder un Data Catalog propre ?

Définir des conventions de nommage par couche (`raw_`, `curated_`), gérer les tables sous forme de code, supprimer les tables créées par des crawls accidentels, documenter tables et colonnes avec des descriptions, appliquer des LF-Tags pour la classification et surveiller les tables inutilisées.

<!-- challenge -->

La base `raw` compte 2 000 tables, dont la moitié créées par des crawlers sur des dossiers de test. Les analystes ne trouvent plus rien. Que faites-vous ?

<!-- solution -->

Inventorier les tables via l'API (emplacement, dernière mise à jour), supprimer celles qui pointent vers des tests ou des emplacements absents, restreindre la portée des crawlers, adopter des conventions par couche et gérer les tables curées en code avec descriptions.

<!-- takeaways -->

- Partagez les catalogues via Lake Formation et les resource links.
- Le catalog ID permet aux API de viser d'autres comptes.
- Un catalogue propre exige conventions et responsables.

### Crawlers

<!-- unit: Fonctionnement des crawlers -->

<!-- goals -->

- Expliquer comment les crawlers infèrent les schémas et regroupent les fichiers en tables.
- Savoir ce que les crawlers peuvent lire, du CSV au JDBC et à Iceberg.

<!-- concept -->

Un crawler examine un échantillon de données et devine. Les classifiers reconnaissent format et schéma, la structure des dossiers suggère tables et partitions, et le résultat est écrit dans le catalogue. Bien deviner exige des données cohérentes : même format, mêmes colonnes, dossiers prévisibles.

Les formats texte sont là où l'on se trompe le plus, car types et en-têtes s'infèrent à partir des valeurs. Les sources autodescriptives (Parquet, Iceberg, schémas de bases) donnent des résultats bien plus fiables.

<!-- example -->

```text
s3://landing/orders/dt=2026-10-16/part-0.csv   ┐
s3://landing/orders/dt=2026-10-17/part-0.csv   ┘─► table "orders", partition key "dt"
s3://landing/orders/backup_old/orders.json      ─► a second table: different format
```

#### Qu'est-ce qu'un crawler ?

Un composant Glue qui se connecte à un stockage de données (S3, bases JDBC, DynamoDB, MongoDB, Delta, Iceberg, Hudi), échantillonne les données, infère schémas et partitions grâce aux classifiers, et crée ou met à jour des tables dans le Data Catalog. Il peut s'exécuter à la demande ou selon un planning.

#### Qu'est-ce qu'un classifier ?

La logique qui reconnaît un format de données et son schéma. Glue fournit des classifiers intégrés (CSV, JSON, Parquet, Avro, ORC, XML, journaux et d'autres), et l'on peut en ajouter avec des motifs grok, des balises XML, des chemins JSON ou des réglages CSV.

#### Comment un crawler décide-t-il du nombre de tables à créer ?

Il regroupe dans une table les fichiers aux schémas compatibles sous un préfixe commun, en s'appuyant sur l'arborescence pour détecter les partitions. Si les schémas diffèrent trop, il crée plusieurs tables. L'option « create a single schema for each S3 path » impose une table par chemin inclus.

#### Comment les crawlers infèrent-ils les types des fichiers CSV ?

En échantillonnant les premières lignes et en choisissant des types adaptés ; si une colonne mélange les valeurs (des nombres avec quelques vides ou du texte), le crawler peut choisir `string`, ou un type que des lignes ultérieures contredisent. Définissez explicitement les tables CSV pour des types prévisibles.

#### Comment les crawlers gèrent-ils les en-têtes CSV ?

Le classifier CSV intégré devine si la première ligne est un en-tête en vérifiant si elle diffère des lignes de données. Quand il se trompe, un classifier CSV personnalisé avec un réglage d'en-tête explicite corrige le problème.

#### Les crawlers peuvent-ils créer des tables Iceberg ou Delta ?

Oui. Les crawlers peuvent enregistrer des tables Delta Lake, Iceberg et Hudi existantes sur S3 en lisant leurs métadonnées, et créer des tables de catalogue qui pointent vers le format de table (nativement ou via des manifestes, selon la configuration).

#### Un crawler peut-il parcourir une base JDBC ?

Oui. Via une connexion Glue, il lit les définitions de tables de bases comme MySQL, PostgreSQL, Oracle et SQL Server avec un chemin d'inclusion comme `mydb/%`, et crée des tables de catalogue que les jobs peuvent lire.

<!-- challenge -->

Un crawler a typé une colonne `zip_code` en `bigint`, perdant les zéros initiaux. Comment corriger définitivement ?

<!-- solution -->

Fixer le schéma vous-même : définir la table en code avec `zip_code` en `string` et configurer le crawler pour ne pas mettre à jour les schémas (ou ne plus l'utiliser pour cette table). Un classifier personnalisé aux types explicites est une autre option.

<!-- takeaways -->

- Les crawlers infèrent les schémas par échantillonnage ; la cohérence aide.
- Les formats texte donnent les pires inférences.
- Les formats autodescriptifs se crawlent de façon fiable.

<!-- unit: Configurer les crawlers -->

<!-- goals -->

- Configurer changements de schéma, re-crawl et portée.
- Rendre les crawls incrémentaux et pilotés par événements.

<!-- concept -->

Un crawler qui rescanne tout et réécrit les schémas à chaque exécution est lent, coûteux et risqué. Ses réglages contrôlent trois choses : ce qu'il regarde (chemins, exclusions, niveau de table, taille d'échantillon), la fréquence à laquelle il relit les anciens dossiers (recrawl policy, événements S3) et ce qu'il a le droit de changer (schema change policy).

La configuration la plus sûre ne lit que les nouvelles données et journalise les changements de schéma au lieu de les appliquer.

<!-- example -->

```json
{
  "Targets": {"S3Targets": [{"Path": "s3://landing/orders/", "Exclusions": ["**/_temporary/**", "**.crc"]}]},
  "RecrawlPolicy": {"RecrawlBehavior": "CRAWL_NEW_FOLDERS_ONLY"},
  "SchemaChangePolicy": {"UpdateBehavior": "LOG", "DeleteBehavior": "LOG"},
  "Configuration": "{\"Version\":1.0,\"Grouping\":{\"TableLevelConfiguration\":3}}"
}
```

#### Qu'est-ce que la politique de changement de schéma d'un crawler ?

Les réglages de ce qu'il faut faire quand le schéma change ou que des objets sont supprimés : mettre à jour la table ou seulement journaliser les changements, et supprimer, déprécier ou ignorer les tables et partitions disparues. En production, on journalise souvent les changements plutôt que de mettre à jour automatiquement, pour éviter les surprises.

#### Que sont les crawls incrémentaux ?

Des exécutions qui ne traitent que les dossiers ajoutés depuis la dernière (et, en mode événements S3, uniquement les objets modifiés d'après une file SQS), ce qui est bien plus rapide et moins cher sur des data lakes volumineux et en croissance.

#### Qu'est-ce que le mode événements S3 des crawlers ?

Un mode où le crawler lit les notifications d'événements S3 depuis une file SQS pour savoir exactement quels objets ont changé, au lieu de lister tout le préfixe.

#### Qu'est-ce que la « recrawl policy » ?

Le réglage qui décide si l'on recrawle tous les dossiers à chaque exécution, seulement les nouveaux dossiers depuis le dernier crawl (incrémental), ou si l'on utilise les événements S3.

#### Que sont les motifs d'exclusion ?

Des motifs glob qui indiquent au crawler les fichiers ou dossiers à ignorer, comme `**/_temporary/**`, `**.crc` ou `**/_SUCCESS`, ce qui évite les tables parasites et fait gagner du temps.

#### Comment limiter le périmètre d'un crawler ?

Avec des chemins d'inclusion précis, des motifs d'exclusion, une taille d'échantillon par dossier (pour S3), le réglage du niveau de table (profondeur de dossier à laquelle les tables sont créées) et des crawlers séparés par source.

#### Que signifie « table level » dans la configuration d'un crawler ?

La profondeur de dossier à laquelle le crawler crée les tables. La fixer évite qu'il crée des tables au mauvais niveau, par exemple en traitant chaque dossier de partition comme une table distincte.

<!-- challenge -->

Un crawler sur un bucket vieux de 5 ans tourne une heure chaque nuit pour trouver un seul nouveau dossier. Que changez-vous ?

<!-- solution -->

Régler la recrawl policy sur les nouveaux dossiers seulement, ou passer en S3 event mode avec une file SQS pour ne lire que les objets modifiés. Mieux encore, enregistrer la partition du jour depuis le job de chargement et se passer du crawler.

<!-- takeaways -->

- Les réglages de portée contrôlent ce que lit le crawler.
- Les modes incrémental et événementiel évitent les rescans complets.
- Journalisez les changements de schéma au lieu de les appliquer aveuglément.

<!-- unit: Quand utiliser un crawler -->

<!-- goals -->

- Reconnaître les problèmes courants des crawlers et leurs causes.
- Décider quand utiliser un crawler et quand définir les tables soi-même.

<!-- concept -->

Les crawlers sont un outil de découverte. Ils excellent sur des données que l'on ne contrôle pas et que l'on veut explorer vite. Dans vos propres pipelines, vous connaissez déjà schéma et partitions : laisser un crawler les deviner ajoute coût, délai et le risque qu'une mauvaise inférence modifie des tables de production.

La plupart des problèmes de crawlers viennent d'entrées incohérentes : formats ou schémas mélangés sous un préfixe, fichiers parasites ou profondeur de dossiers inattendue.

<!-- example -->

| Situation | Usage |
|---|---|
| Explorer le bucket S3 d'un fournisseur | Crawler |
| Votre job Glue écrit des partitions quotidiennes | Le job met à jour le catalogue |
| Table Iceberg écrite par Spark | Catalogue via l'écrivain, sans crawler |

#### Quels sont les problèmes fréquents des crawlers ?

Trop de tables créées à cause de schémas ou d'arborescences incohérents, des types mal inférés depuis des échantillons CSV, des erreurs `HIVE_PARTITION_SCHEMA_MISMATCH` quand les partitions ont des schémas différents, du coût et du temps sur d'énormes préfixes, et des changements de schéma silencieux qui cassent les requêtes en aval.

#### Faut-il toujours utiliser des crawlers ?

Non. Les crawlers sont pratiques pour la découverte et pour les sources qu'on ne maîtrise pas. Pour ses propres pipelines, définir les tables explicitement (infrastructure as code) et enregistrer les partitions depuis les jobs, ou utiliser la projection de partitions, donne des schémas prévisibles et aucun coût de crawler.

#### Comment les crawlers sont-ils facturés ?

Au DPU-heure pendant leur exécution, à la seconde avec une durée minimale par exécution. Parcourir des millions de petits fichiers peut coûter cher ; utilisez des motifs d'inclusion et d'exclusion, l'échantillonnage et les crawls incrémentaux.

#### Un crawler crée des dizaines de tables au lieu d'une. Qu'est-ce qui ne va pas ?

Les fichiers sous le préfixe ont des schémas ou des arborescences incohérents (colonnes supplémentaires, formats différents, fichiers égarés). Corriger l'organisation de la source, ajouter des motifs d'exclusion, utiliser « create a single schema for each S3 path », ou définir la table explicitement au lieu de crawler.

<!-- challenge -->

Votre job Glue écrit du Parquet dans S3 et un crawler passe ensuite pour mettre la table à jour. Parfois les requêtes cassent après un changement de type par le crawler. Que proposez-vous ?

<!-- solution -->

Retirer le crawler du pipeline : faire écrire le job avec mise à jour du catalogue activée (ou appeler `BatchCreatePartition`) sur une table définie en code. Les changements de schéma deviennent délibérés, via la revue de code.

<!-- takeaways -->

- Les crawlers servent à découvrir, pas aux pipelines maison.
- Des entrées incohérentes créent trop de tables.
- Laissez les jobs enregistrer leur propre sortie.

<!-- stage: Construire des jobs -->

### Jobs ETL Glue

<!-- unit: Anatomie d'un job Glue -->

<!-- goals -->

- Lire et écrire la structure d'un job PySpark Glue.
- Suivre une exécution à travers ses états, identifiants et logs.

<!-- concept -->

Un job Spark Glue est une application Spark entourée d'une fine couche Glue. Le contexte Glue ajoute des lecteurs et écrivains qui connaissent le catalogue ; l'objet job garde un état entre les exécutions, sur lequel reposent les bookmarks. Le reste est du PySpark ordinaire.

Chaque exécution reçoit un identifiant et passe par des états que l'on peut surveiller et auxquels on peut réagir. Logs et métriques arrivent dans CloudWatch, organisés par exécution.

<!-- example -->

```python
import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

args = getResolvedOptions(sys.argv, ["JOB_NAME", "process_date"])
glue = GlueContext(SparkContext.getOrCreate())
job = Job(glue); job.init(args["JOB_NAME"], args)
df = glue.spark_session.read.parquet(f"s3://lake/raw/orders/dt={args['process_date']}/")
df.write.mode("overwrite").parquet(f"s3://lake/curated/orders/dt={args['process_date']}/")
job.commit()
```

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

#### Quels sont les états d'exécution d'un job ?

`STARTING`, `RUNNING`, `STOPPING`, `STOPPED`, `SUCCEEDED`, `FAILED`, `TIMEOUT`, `ERROR` et `WAITING`. EventBridge reçoit les événements de changement d'état pour les alertes et l'orchestration.

#### À quoi sert l'identifiant d'exécution d'un job Glue ?

Il identifie une exécution pour la supervision, les journaux, le rembobinage des bookmarks et les relances, et peut être reporté dans les sorties (par exemple en colonne) pour le lignage.

#### Que deviennent les journaux d'un job Glue ?

Les journaux du driver et des executors vont dans CloudWatch Logs (`/aws-glue/jobs/output` et `/aws-glue/jobs/error`) ; la journalisation continue les transmet pendant l'exécution. Utilisez `glue.get_logger()` pour des messages structurés.

<!-- challenge -->

Un job oublie d'appeler `job.commit()`. Les bookmarks sont activés. Que se passe-t-il à l'exécution suivante ?

<!-- solution -->

Le bookmark n'avance jamais : chaque exécution retraite les mêmes données comme si elles étaient nouvelles, ce qui peut créer des doublons en aval. Ajoutez `job.commit()` à la fin d'un traitement réussi.

<!-- takeaways -->

- Un job Glue, c'est Spark plus un contexte Glue et un état de job.
- `job.commit()` enregistre l'état du bookmark après succès.
- Les run IDs relient états, logs et métriques.

<!-- unit: Paramètres, bibliothèques et accès au catalogue -->

<!-- goals -->

- Passer des arguments et ajouter des dépendances Python ou Java aux jobs.
- Utiliser Spark SQL sur le catalogue Glue.

<!-- concept -->

Le même script doit tourner pour n'importe quelle date ou environnement : tout ce qui varie arrive en arguments du job. Les dépendances arrivent de même : paquets Python et JAR sont désignés dans les paramètres et installés au démarrage, ce qui garde les scripts portables mais allonge le démarrage pour de grosses installations.

Activer le catalogue comme metastore de Spark permet d'utiliser du SQL simple sur les tables du catalogue, que beaucoup d'équipes trouvent plus clair que les API propres à Glue.

<!-- example -->

```text
--process_date                 2026-10-17
--additional-python-modules    pydantic==2.9.2,s3://artifacts/libs/etl_lib-1.4.0-py3-none-any.whl
--extra-jars                   s3://artifacts/jars/postgresql-42.7.4.jar
--enable-glue-datacatalog      true
```

#### Comment passer des paramètres à un job Glue ?

Sous forme d'arguments du job (`--target_path s3://...`) définis dans le job ou surchargés au démarrage, lus avec `getResolvedOptions`. Des arguments spéciaux configurent Glue lui-même, comme `--job-bookmark-option`, `--enable-metrics`, `--additional-python-modules` ou `--conf`.

#### Comment ajouter des bibliothèques Python à un job Glue ?

Avec `--additional-python-modules` (installation depuis PyPI ou des wheels dans S3 au démarrage), `--extra-py-files` (fichiers zip ou py dans S3), ou en empaquetant les dépendances dans un wheel. Pour des jobs sans accès Internet, hébergez les wheels dans S3 ou utilisez un dépôt privé via un endpoint VPC.

#### Comment ajouter des dépendances JAR ?

Avec `--extra-jars` pointant vers des fichiers JAR dans S3, pour des pilotes JDBC ou des bibliothèques Spark non incluses dans la version de Glue.

#### Que fait `--enable-glue-datacatalog` ?

Il configure Spark dans le job pour utiliser le Glue Data Catalog comme Hive metastore, de sorte que `spark.sql("SELECT * FROM raw.orders")` et `saveAsTable` fonctionnent sur les tables du catalogue.

#### Comment utiliser Spark SQL dans un job Glue ?

Convertir en DataFrame, enregistrer une vue temporaire et lancer `spark.sql()`. Avec le Data Catalog activé comme Hive metastore (`--enable-glue-datacatalog`), on peut interroger directement les tables du catalogue par `base.table`.

<!-- challenge -->

Un job installe 15 paquets PyPI au démarrage et échoue parfois quand PyPI est lent. Comment le fiabiliser ?

<!-- solution -->

Construire en CI une wheel (ou un lot de wheels) aux versions figées, la stocker dans S3 et la référencer dans `--additional-python-modules`. Le démarrage ne dépend plus de PyPI et les versions restent fixes.

<!-- takeaways -->

- Les arguments font servir un script à chaque exécution.
- Les dépendances arrivent par les paramètres au démarrage.
- Le catalogue peut servir de metastore à Spark.

<!-- unit: Options d'exécution -->

<!-- goals -->

- Choisir entre Spark, Python shell, Flex et auto scaling.
- Régler délibérément timeouts, relances et concurrence.

<!-- concept -->

Tous les jobs n'ont pas besoin d'un cluster Spark, et tous les jobs Spark n'ont pas besoin de démarrer tout de suite. Les jobs Python shell traitent les tâches légères à bas coût ; Flex exécute du Spark non urgent sur de la capacité disponible avec remise ; l'auto scaling dimensionne le cluster par étape.

Les valeurs par défaut sont risquées. Un timeout de 48 heures laisse un job bloqué brûler de l'argent deux jours, et les relances d'un job non idempotent dupliquent les données. Réglez-les délibérément, avec le nombre d'exécutions qui peuvent se chevaucher.

<!-- example -->

```python
glue.create_job(Name="orders_daily", Role=ROLE, GlueVersion="5.0",
    Command={"Name": "glueetl", "ScriptLocation": "s3://artifacts/jobs/orders_daily.py"},
    WorkerType="G.1X", NumberOfWorkers=10, ExecutionClass="FLEX",
    Timeout=60, MaxRetries=1, ExecutionProperty={"MaxConcurrentRuns": 1},
    DefaultArguments={"--enable-auto-scaling": "true", "--TempDir": "s3://glue-temp/orders/"})
```

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

#### À quoi sert le répertoire temporaire (`--TempDir`) ?

Un emplacement S3 où Glue écrit des données intermédiaires, par exemple lors d'un chargement dans Redshift ou pour le shuffle dans certaines configurations. Il doit avoir une règle de cycle de vie qui supprime les anciens fichiers.

<!-- challenge -->

Un job de rapport nocturne doit seulement finir avant 08:00 et dure 30 minutes. Comment réduire son coût sans toucher au code ?

<!-- solution -->

L'exécuter avec la classe d'exécution Flex, qui utilise la capacité disponible à moindre prix ; un démarrage éventuellement plus lent n'a pas d'importance vu l'échéance. Fixez aussi un timeout raisonnable et activez l'auto scaling.

<!-- takeaways -->

- Python shell pour le léger ; Flex pour le Spark non urgent.
- Ne gardez jamais le timeout par défaut de 48 heures.
- Relancez seulement les jobs idempotents ; limitez les exécutions concurrentes.

<!-- unit: Développer des jobs -->

<!-- goals -->

- Développer des jobs Glue en interactif et en local.
- Choisir entre éditeur visuel et scripts.

<!-- concept -->

Attendre une minute à chaque essai tue la productivité. Les sessions interactives donnent une session Spark dans un notebook ou un IDE, facturée seulement tant qu'elle est ouverte ; les images Docker de Glue permettent d'exécuter jobs et tests sur son portable avec les mêmes bibliothèques.

L'éditeur visuel accélère les jobs simples et aide les non-développeurs, mais la logique complexe, la réutilisation et les tests sont plus simples dans des scripts versionnés dans Git.

<!-- example -->

```bash
docker run -it -v ~/.aws:/home/hadoop/.aws -v $PWD:/home/hadoop/workspace \
  public.ecr.aws/glue/aws-glue-libs:5 \
  spark-submit workspace/jobs/orders_daily.py --JOB_NAME local --process_date 2026-10-17
```

#### Que sont les sessions interactives Glue ?

Des sessions Spark à la demande, utilisées depuis des notebooks Jupyter, les notebooks de Glue Studio ou votre IDE pour développer et déboguer du code Glue de façon interactive, facturées à la seconde avec un délai d'inactivité.

#### Comment développer des jobs Glue en local ?

Avec les images Docker officielles de Glue (qui contiennent les bibliothèques Glue et le Spark d'une version donnée), en exécutant scripts et pytest en local, ou avec des sessions interactives depuis un notebook local. La logique PySpark pure peut aussi être testée avec une SparkSession locale.

#### Quelle est la différence entre l'éditeur de scripts Spark et l'éditeur visuel ?

L'éditeur visuel construit les jobs comme un graphe de nœuds et génère le code ; il est rapide pour l'ETL standard et accessible aux analystes. L'éditeur de scripts donne le contrôle total du code PySpark ou Scala. Beaucoup d'équipes commencent en visuel puis passent au code géré dans Git.

<!-- challenge -->

Une équipe construit tous ses jobs dans l'éditeur visuel et se retrouve avec 40 jobs à la logique copiée. Que proposez-vous ?

<!-- solution -->

Déplacer la logique partagée dans un paquet Python testé, écrire les nouveaux jobs comme des scripts qui l'importent et garder l'éditeur visuel pour les prototypes. Stocker scripts et définitions dans Git et les déployer en code.

<!-- takeaways -->

- Les sessions interactives donnent un retour rapide dans les notebooks.
- Les images Docker de Glue exécutent jobs et tests en local.
- Les scripts dans Git passent mieux à l'échelle que les jobs visuels.

<!-- unit: Sources et destinations -->

<!-- goals -->

- Lire des bases de données en parallèle et écrire vers entrepôts et formats de table.
- Gérer JSON imbriqué et enregistrements invalides à la lecture.

<!-- concept -->

La plupart des problèmes de jobs commencent aux bords. Une lecture de base non partitionnée tourne sur un seul executor, quel que soit le nombre de workers payés. Une écriture vers un entrepôt passe par un staging S3 et exige des permissions des deux côtés. Les formats de table ouverts doivent être activés explicitement.

Les fichiers ont leurs propres soucis : structures imbriquées à aplatir et enregistrements mal formés à mettre en quarantaine plutôt que de faire échouer le job ou de les perdre.

<!-- example -->

```python
df = (spark.read.format("jdbc")
      .option("url", url).option("dbtable", "public.orders")
      .option("partitionColumn", "order_id").option("lowerBound", 1)
      .option("upperBound", 50_000_000).option("numPartitions", 16)
      .load())                               # 16 parallel reads instead of 1
```

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

#### Comment lire DynamoDB dans Glue ?

Avec le connecteur DynamoDB : soit directement (consomme de la capacité de lecture, contrôlée par `dynamodb.throughput.read.percent`), soit via l'export DynamoDB vers S3 (`dynamodb.export`), qui ne consomme pas de capacité de la table et est préférable pour les grandes tables.

#### Comment les jobs Glue se connectent-ils à Snowflake, BigQuery ou d'autres sources hors AWS ?

Via les connecteurs natifs de Glue pour de nombreuses sources (Snowflake, BigQuery, Teradata, SAP HANA, MongoDB et des applications SaaS), via des connecteurs AWS Marketplace, ou en JDBC avec un pilote personnalisé et une connexion Glue.

#### Comment lire du JSON imbriqué dans Glue ?

Le lire en DynamicFrame ou en DataFrame (schéma inféré ou déclaré), puis l'aplatir avec des `select` de champs imbriqués, `explode` pour les tableaux, ou `Relationalize` de Glue pour une sortie entièrement relationnelle.

#### Comment gérer les enregistrements défectueux à la lecture de fichiers ?

Pour les lecteurs Spark, avec `mode` (`PERMISSIVE` avec une colonne d'enregistrements corrompus, `DROPMALFORMED`, `FAILFAST`) ou `badRecordsPath` quand c'est pris en charge ; pour les DynamicFrames, les erreurs sont capturées par enregistrement et consultables avec `errorsAsDynamicFrame()`, avec des seuils fixés par `stageThreshold` et `totalThreshold`.

<!-- challenge -->

Un job qui lit une table PostgreSQL de 200 Go utilise 20 workers mais dure 3 heures, avec un seul executor actif. Qu'est-ce qui ne va pas ?

<!-- solution -->

La lecture JDBC n'est pas partitionnée : une seule connexion lit tout. Ajoutez `partitionColumn`, des bornes et `numPartitions` (ou `hashfield`/`hashpartitions` pour les DynamicFrames) sur une colonne numérique indexée, dans la limite de ce que supporte la base.

<!-- takeaways -->

- Partitionnez les lectures JDBC, sinon elles tournent sur un executor.
- Activez les formats de table avec `--datalake-formats`.
- Mettez les enregistrements invalides en quarantaine au lieu de les perdre.

### DynamicFrames et transformations

<!-- unit: DynamicFrames et DataFrames -->

<!-- goals -->

- Expliquer l'apport des DynamicFrames et quand passer aux DataFrames.
- Écrire des DynamicFrames avec mise à jour du catalogue et bookmarks.

<!-- concept -->

Les DynamicFrames ont été conçus pour des sources désordonnées : chaque enregistrement porte son propre schéma, si bien que des types incohérents n'arrêtent pas la lecture. Les DataFrames supposent un schéma unique et obtiennent en échange tout l'optimiseur Spark. La plupart des jobs utilisent les deux : DynamicFrames aux bords, où catalogue et bookmarks comptent, DataFrames pour la logique au milieu.

Les noms `transformation_ctx` relient chaque étape à l'état du bookmark : ils doivent être stables et uniques.

<!-- example -->

```python
dyf = glue.create_dynamic_frame.from_catalog(database="raw", table_name="orders",
                                             transformation_ctx="src_orders")
df = dyf.toDF().where("status = 'paid'")            # DataFrame logic
out = DynamicFrame.fromDF(df, glue, "out_orders")
sink = glue.getSink(connection_type="s3", path="s3://lake/curated/orders/",
                    enableUpdateCatalog=True, partitionKeys=["dt"])
sink.setFormat("glueparquet"); sink.setCatalogInfo("curated", "orders"); sink.writeFrame(out)
```

#### Qu'est-ce qu'un DynamicFrame ?

La structure de données distribuée de Glue, proche d'un DataFrame Spark mais où chaque enregistrement est autodescriptif : il n'a pas besoin d'un schéma fixe à l'avance. Il gère les données incohérentes (un champ tantôt chaîne, tantôt entier) grâce aux types « choice ».

#### Quelle est la différence entre un DynamicFrame et un DataFrame ?

Un DataFrame a un schéma unique pour tout le jeu de données et bénéficie de tout l'optimiseur et de l'API Spark SQL. Un DynamicFrame calcule le schéma par enregistrement, prend en charge les types choice, les transformations propres à Glue, les bookmarks et l'intégration au catalogue. On convertit avec `toDF()` et `DynamicFrame.fromDF()`, et la plupart des équipes transforment en DataFrame.

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

<!-- challenge -->

Après un refactoring, les bookmarks ne fonctionnent plus et chaque exécution relit tout. Les lectures semblent identiques. Que vérifiez-vous ?

<!-- solution -->

Si les valeurs de `transformation_ctx` ont changé ou disparu : l'état du bookmark est stocké par nom de contexte. Restaurez les noms d'origine (ou réinitialisez volontairement le bookmark) et vérifiez que `job.commit()` s'exécute toujours.

<!-- takeaways -->

- Les DynamicFrames tolèrent des schémas incohérents.
- Les DataFrames apportent l'optimiseur et une API plus riche.
- Des `transformation_ctx` stables préservent les bookmarks.

<!-- unit: Transformations souples sur le schéma -->

<!-- goals -->

- Résoudre les types mixtes et mapper les colonnes avec les transformations Glue.
- Aplatir les données imbriquées et survivre aux nouvelles colonnes.

<!-- concept -->

Les sources tiennent rarement leurs promesses. Une colonne numérique hier contient du texte aujourd'hui ; un champ JSON plat devient imbriqué ; un fournisseur ajoute des colonnes sans prévenir. Les transformations souples de Glue gèrent cela au bord : décider du sort des types mixtes, mapper et caster explicitement les colonnes, aplatir l'imbrication en tables.

Le principe : absorber le changement à l'étape brut vers propre et garder un schéma curé stable et explicite.

<!-- example -->

```python
dyf = dyf.resolveChoice(specs=[("price", "cast:double")])
dyf = ApplyMapping.apply(frame=dyf, mappings=[
    ("id", "string", "order_id", "bigint"),
    ("price", "double", "amount", "decimal(12,2)"),
    ("ts", "string", "created_at", "timestamp")])
```

#### Qu'est-ce qu'un type choice, et comment fonctionne `ResolveChoice` ?

Quand une colonne contient des valeurs de types différents, un DynamicFrame garde un type choice (par exemple `choice<int,string>`). `ResolveChoice` le résout avec `cast:long`, `make_cols` (sépare en `col_int` et `col_string`), `make_struct` ou `project:string`.

```python
resolved = dyf.resolveChoice(specs=[("amount", "cast:double"), ("id", "cast:long")])
```

#### Que fait `ApplyMapping` ?

Il renomme des colonnes, convertit des types et sélectionne des champs en une étape, à partir d'une liste de tuples `(source, type_source, cible, type_cible)` ; c'est ainsi que fonctionne le nœud de mapping de Glue Studio.

#### Que fait `Relationalize` ?

Il aplatit du JSON imbriqué en un ensemble de tables relationnelles : les structures imbriquées deviennent des colonnes et les tableaux des tables séparées reliées par des clés générées, prêtes à charger dans une base relationnelle.

#### Que fait `Unbox` ?

Il analyse une colonne texte contenant du JSON (ou du CSV) et la transforme en structure, pour que les champs imbriqués deviennent des colonnes accessibles.

#### Un système source ajoute des colonnes sans prévenir. Comment garder le pipeline Glue en marche ?

Lire en tenant compte de l'évolution du schéma : DynamicFrames ou schémas permissifs en raw, sélection explicite des colonnes dans les sorties curées, alerte sur les nouvelles colonnes (mode journalisation seule du crawler ou contrôle de schéma), et évolution de schéma Iceberg pour ajouter les colonnes de façon délibérée.

<!-- challenge -->

Une source envoie `amount` en nombre, mais certains jours en texte avec un symbole monétaire. La table curée doit rester en `decimal`. Que faites-vous ?

<!-- solution -->

Résoudre le choix en castant d'abord en chaîne, retirer les caractères non numériques, caster en decimal avec une sémantique de type `try_cast`, et envoyer les lignes encore en échec vers un emplacement de quarantaine avec alerte.

<!-- takeaways -->

- Les choice types notent les types mixtes ; `ResolveChoice` tranche.
- `ApplyMapping` renomme, caste et sélectionne en une étape.
- Absorbez les changements du brut vers le propre ; gardez le curé stable.

<!-- unit: Transformations intégrées -->

<!-- goals -->

- Utiliser les transformations intégrées pour filtrer, joindre et découper.
- Dédupliquer et ajouter des colonnes d'audit.

<!-- concept -->

Glue fournit des transformations qui reprennent des opérations SQL courantes, surtout pour l'éditeur visuel et les jobs en DynamicFrames uniquement. En code, les opérations DataFrame équivalentes sont souvent plus claires et plus rapides : les intégrées comptent surtout pour lire des jobs générés.

Deux habitudes valent quelle que soit l'API : dédupliquer sur une clé métier avec une règle claire de ligne gagnante, et marquer chaque ligne de sa provenance et de son heure d'arrivée.

<!-- example -->

```python
from pyspark.sql import functions as F, Window
w = Window.partitionBy("order_id").orderBy(F.col("updated_at").desc())
clean = (df.withColumn("rn", F.row_number().over(w)).where("rn = 1").drop("rn")
           .withColumn("ingested_at", F.current_timestamp())
           .withColumn("source_file", F.input_file_name()))
```

#### Quelles autres transformations intégrées Glue propose-t-il ?

`DropFields`, `SelectFields`, `RenameField`, `Filter`, `Map`, `Join`, `SplitFields`, `SplitRows`, `Unbox` (analyse de chaînes JSON), `DropNullFields`, `FillMissingValues`, `FindMatches` (déduplication par ML) et, dans Glue Studio, des transformations comme `Aggregate`, `Pivot`, `Derived column`, `Identify sensitive data` et `Evaluate data quality`.

#### Comment filtrer un DynamicFrame ?

Avec `Filter.apply(frame=dyf, f=lambda row: row["status"] == "paid")` ou `dyf.filter(...)`, même si convertir en DataFrame et utiliser `filter("status = 'paid'")` est généralement plus rapide car Spark peut l'optimiser.

#### Comment joindre des DynamicFrames ?

Avec `Join.apply(dyf1, dyf2, "key1", "key2")`, qui fait une jointure par égalité ; pour d'autres types de jointures ou conditions, convertir en DataFrames.

#### Que fait `SplitFields` ?

Il sépare un DynamicFrame en deux collections par colonnes, par exemple pour isoler les colonnes de données personnelles du reste et les écrire à des emplacements différents.

#### Comment dédupliquer dans un job Glue ?

Convertir en DataFrame et utiliser `dropDuplicates(["key"])` ou une fonction de fenêtre avec `row_number()` ordonnée par un horodatage de mise à jour, en gardant l'enregistrement le plus récent par clé.

#### Comment ajouter des colonnes d'audit dans un job Glue ?

Ajouter des colonnes comme `ingested_at` (`current_timestamp()`), `source_file` (`input_file_name()` ou les métadonnées du fichier), `job_run_id` et `process_date`, pour que chaque ligne soit traçable jusqu'à l'exécution et au fichier qui l'ont produite.

<!-- challenge -->

Une équipe aval demande de quel fichier vient chaque ligne curée, après qu'un mauvais fichier a corrompu un rapport. Qu'ajoutez-vous, et où ?

<!-- solution -->

Ajouter en colonnes `source_file` (via `input_file_name()` ou les métadonnées du fichier), `ingested_at` et l'identifiant d'exécution du job à l'étape brut vers propre, et les propager aux tables curées. Les mauvaises lignes se tracent et se retirent alors par fichier.

<!-- takeaways -->

- Les intégrées reprennent le SQL ; le code DataFrame est souvent plus clair.
- Dédupliquez sur une clé avec une règle explicite de ligne gagnante.
- Les colonnes d'audit relient les données à leur source.

<!-- unit: Appariement d'enregistrements par ML -->

<!-- goals -->

- Expliquer ce que fait FindMatches et quand il convient.
- L'entraîner et l'utiliser pour dédupliquer sans clé commune.

<!-- concept -->

La déduplication exacte exige une clé. Quand des enregistrements décrivent le même client différemment selon les systèmes (orthographe, champs manquants, noms inversés), les règles ne finissent jamais. FindMatches apprend ce que « le même » signifie à partir d'exemples que vous étiquetez, puis regroupe les enregistrements en correspondances.

Sa qualité dépend des étiquettes : quelques centaines de paires bien choisies lui en apprennent plus que des milliers de cas faciles.

<!-- example -->

```text
1. Create a FindMatches transform on customers (primary key: source_id)
2. Generate a labeling file, mark pairs as match / no match, upload it
3. Check estimated precision/recall; tune toward precision or recall
4. Use the transform in a job: output adds match_id per group
```

#### Qu'est-ce que FindMatches ?

Une transformation de machine learning qui identifie des enregistrements en double ou correspondants sans clé commune (par exemple le même client orthographié différemment), entraînée à partir d'exemples étiquetés.

#### Vous devez dédupliquer des fiches clients sans clé commune entre deux systèmes. Quel outil Glue peut aider ?

La transformation ML FindMatches : étiqueter des exemples de paires correspondantes et non correspondantes, entraîner la transformation et l'exécuter dans un job pour attribuer des identifiants de correspondance, puis fusionner les enregistrements par identifiant avec des règles métier.

<!-- challenge -->

Après FindMatches, les ventes remarquent deux clients différents fusionnés en un seul. Quel réglage ajustez-vous, et que faites-vous d'autre ?

<!-- solution -->

Orienter la transformation vers la précision plutôt que le rappel, pour ne fusionner que les correspondances sûres. Ajouter des exemples étiquetés de clients proches mais différents, réentraîner et revoir un échantillon de groupes fusionnés avant publication.

<!-- takeaways -->

- FindMatches apprend l'appariement à partir de paires étiquetées.
- Étiquetez les cas difficiles, pas les faciles.
- Arbitrez précision et rappel selon l'usage.

### Job bookmarks et traitement incrémental

<!-- unit: Fonctionnement des job bookmarks -->

<!-- goals -->

- Activer, suspendre, réinitialiser et rembobiner les bookmarks.
- Connaître leurs limites avec les fichiers, JDBC et Iceberg.

<!-- concept -->

Les bookmarks permettent à un job de se souvenir de ce qu'il a déjà traité. Pour les fichiers, l'état repose sur chemins et dates de modification ; pour les bases, sur les colonnes clés choisies. L'état n'avance que lorsqu'une exécution réussit son commit : un échec ne saute jamais de données.

Pratiques mais implicites, ils peuvent être trompés par des fichiers écrasés, des contextes renommés ou une source partagée, et ne s'appliquent pas aux sources Iceberg. Sachez les réinitialiser avant d'en avoir besoin.

<!-- example -->

```bash
aws glue start-job-run --job-name orders_daily \
  --arguments '{"--job-bookmark-option": "job-bookmark-enable"}'
aws glue reset-job-bookmark --job-name orders_daily --run-id jr_0a1b2c   # rewind to a run
```

#### Que sont les job bookmarks ?

Une fonction de Glue qui conserve un état entre les exécutions pour que chacune ne traite que les nouvelles données : pour les sources S3, les fichiers (par date de modification) déjà traités ; pour les sources JDBC, les valeurs maximales des colonnes clés du bookmark.

#### Comment activer et piloter les job bookmarks ?

Avec `--job-bookmark-option` : `job-bookmark-enable`, `job-bookmark-disable` ou `job-bookmark-pause` (traite depuis le dernier bookmark sans le mettre à jour). La source doit avoir un `transformation_ctx` et le script doit appeler `job.commit()`.

#### Comment réinitialiser ou rembobiner un bookmark ?

Avec la console ou l'API `ResetJobBookmark`, qui fait tout retraiter à l'exécution suivante ; on peut aussi revenir à l'identifiant d'une exécution précédente pour retraiter à partir de ce point.

#### Qu'arrive-t-il aux bookmarks si un job échoue ?

Les bookmarks ne sont mis à jour par `job.commit()` qu'en cas de succès : une exécution en échec laisse le bookmark en place et la suivante retraite les mêmes données. D'où la nécessité d'écritures idempotentes.

#### Deux jobs différents peuvent-ils partager un bookmark ?

Non. Les bookmarks sont propres à chaque job (et à chaque `transformation_ctx`). Deux jobs lisant la même source gardent des états indépendants.

#### Comment fonctionnent les bookmarks JDBC ?

On indique des `jobBookmarkKeys` (colonnes comme un identifiant croissant ou `updated_at`) et un ordre de tri ; le job lit les lignes dont les valeurs dépassent le dernier maximum stocké. Les mises à jour de lignes aux clés anciennes sont manquées : cela convient aux tables en ajout seul ou aux horodatages monotones.

#### Quelles sont les limites des job bookmarks ?

Ils suivent les fichiers par date de modification : des fichiers écrasés sous le même nom peuvent être manqués ou retraités ; les bookmarks JDBC exigent des colonnes clés croissantes et ne voient pas les mises à jour d'anciennes lignes ; ils ne fonctionnent qu'avec certaines sources et certains formats ; et ils ne rendent pas les écritures idempotentes, donc un échec après l'écriture et avant le `commit` fait retraiter des données.

#### Les job bookmarks fonctionnent-ils avec des tables Iceberg en source ?

Pas de la même manière ; pour des sources Iceberg, on traite de façon incrémentale avec les fonctions propres à Iceberg, comme la lecture des changements entre snapshots (lectures incrémentales ou vues de changelog), en mémorisant l'identifiant du dernier snapshot traité.

<!-- challenge -->

Un bug a corrompu la sortie des trois dernières exécutions. Les bookmarks sont actifs. Comment retraiter seulement ces exécutions ?

<!-- solution -->

Corriger le code, supprimer ou écraser la sortie des trois exécutions, puis rembobiner le bookmark à l'exécution précédant la première mauvaise avec `ResetJobBookmark` et un run ID. L'exécution suivante retraite tout depuis ce point.

<!-- takeaways -->

- Les bookmarks suivent fichiers ou clés traités par job.
- Ils n'avancent qu'en cas de commit réussi.
- Connaissez leurs limites : fichiers écrasés, Iceberg, contextes renommés.

<!-- unit: Incrémental sans bookmarks -->

<!-- goals -->

- Traiter des plages de dates explicites avec des prédicats.
- Rendre les jobs idempotents et gérer les données tardives.

<!-- concept -->

Beaucoup d'équipes préfèrent des incréments explicites aux bookmarks : l'orchestrateur passe une date, le job lit cette partition avec un pushdown predicate et écrase la sortie de cette partition. L'exécution devient une fonction pure de son argument, ce qui simplifie relances, backfills et données tardives.

Les prédicats comptent aussi pour les performances : poussés au catalogue, ils évitent au job de lister des partitions qu'il ne lira jamais.

<!-- example -->

```python
dyf = glue.create_dynamic_frame.from_catalog(
    database="raw", table_name="orders",
    push_down_predicate=f"dt = '{args['process_date']}'",
    additional_options={"catalogPartitionPredicate": f"dt = '{args['process_date']}'"})
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
dyf.toDF().write.mode("overwrite").partitionBy("dt").parquet("s3://lake/curated/orders/")
```

#### Comment rendre un job Glue idempotent ?

En écrivant la sortie de la partition traitée par écrasement (écrasement dynamique de partitions) ou en utilisant `MERGE` sur une table Iceberg, plutôt que d'ajouter aveuglément ; en tirant la période traitée d'un paramètre ; et en considérant les bookmarks comme une optimisation, pas comme la seule garantie.

#### Qu'est-ce que le pushdown predicate dans Glue ?

Un filtre sur les colonnes de partition passé à la lecture depuis le catalogue (`push_down_predicate="order_date >= '2026-10-01'"`) pour que Glue ne liste et ne lise que les partitions correspondantes au lieu de toute la table.

#### Qu'est-ce que `catalogPartitionPredicate` ?

Un filtre de partitions côté serveur, évalué par le Data Catalog à l'aide des index de partition, qui réduit le nombre de partitions que Glue doit récupérer du catalogue pour les tables très partitionnées. Il se combine avec `push_down_predicate`.

#### Comment ne traiter que les données de la veille sans bookmarks ?

Passer la date en argument du job (depuis l'ordonnanceur), lire avec un pushdown predicate sur la partition de date, et écraser la partition de sortie de cette date. C'est explicite, reproductible, et cela facilite les backfills.

#### Comment corriger les « données tardives » dans un pipeline Glue quotidien ?

Traiter une fenêtre glissante (par exemple les trois derniers jours) à chaque exécution avec écrasement de partitions ou `MERGE`, pour que les enregistrements tardifs mettent à jour les bonnes partitions, en gardant la fenêtre paramétrable pour des corrections plus larges.

<!-- challenge -->

Un job écrase toute la table curée à chaque exécution avec les seules données du jour, effaçant l'historique. Quel réglage manque ?

<!-- solution -->

L'écrasement dynamique de partitions : régler `spark.sql.sources.partitionOverwriteMode=dynamic` (et écrire avec `partitionBy`) pour ne remplacer que les partitions présentes dans la sortie, ou écrire directement dans le chemin de la partition.

<!-- takeaways -->

- Passez des dates explicites ; lisez avec des pushdown predicates.
- N'écrasez que les partitions propres à l'exécution.
- Des fenêtres glissantes absorbent les données tardives.

### ETL en streaming

<!-- unit: Les jobs de streaming Glue -->

<!-- goals -->

- Décrire les jobs de streaming Glue, leurs sources et leurs schémas.
- Choisir entre Glue streaming, Firehose et Flink.

<!-- concept -->

Un job de streaming est un job Spark qui ne finit jamais : il lit un flux en micro-lots et écrit chaque lot quelque part, généralement S3 ou un format de table. Comme il tourne en continu, chaque heure est payée : il ne vaut la peine que si la fraîcheur compte vraiment et si les transformations exigent Spark.

La livraison simple relève de Firehose ; le traitement d'événements complexe à faible latence, de Flink. Glue streaming se situe entre les deux.

<!-- example -->

| Besoin | Choix |
|---|---|
| Livrer des événements vers S3 en Parquet, sans logique | Firehose |
| Joindre le flux aux données du lake, écrire de l'Iceberg chaque minute | Glue streaming |
| Fenêtres sub-seconde, état complexe | Managed Service for Apache Flink |

#### Que sont les jobs de streaming Glue ?

Des jobs Spark Structured Streaming de longue durée qui lisent depuis Kinesis Data Streams, Amazon MSK ou Kafka autogéré, transforment les enregistrements en micro-lots et écrivent dans S3, des formats de data lake, des bases ou d'autres flux.

#### Quelles sources le streaming Glue peut-il lire ?

Amazon Kinesis Data Streams, Amazon MSK, Apache Kafka autogéré et (via des connecteurs) d'autres systèmes de streaming. Les sorties incluent S3, les tables Iceberg/Hudi/Delta, les bases JDBC et d'autres flux.

#### Comment un job de streaming Glue gère-t-il les schémas ?

À partir d'une table du Data Catalog qui décrit le flux, du Glue Schema Registry, ou en inférant le schéma depuis les données. Les enregistrements non conformes peuvent être traités avec des types choice ou envoyés vers un chemin d'erreurs.

#### Quand choisir le streaming Glue plutôt que Kinesis Data Firehose ou Managed Service for Apache Flink ?

Firehose pour une livraison simple vers S3, Redshift ou OpenSearch avec peu de transformation et sans code. Managed Flink pour du traitement de flux avec état et faible latence, avec une logique complexe en temps d'événement. Le streaming Glue quand l'équipe utilise déjà Spark, a besoin d'ETL en micro-lots vers un data lake et veut partager le code avec les jobs batch.

#### Comment les jobs de streaming Glue sont-ils facturés ?

Au DPU-heure tant qu'ils tournent, c'est-à-dire en continu ; les workers G.025X réduisent le coût pour les flux à faible volume. L'autoscaling aide face à un trafic variable.

<!-- challenge -->

Une équipe fait tourner un job de streaming Glue 24 h/24 juste pour écrire des événements Kinesis bruts dans S3 en Parquet. Que suggérez-vous ?

<!-- solution -->

Utiliser Kinesis Data Firehose avec conversion Parquet et partitionnement dynamique : pas de code, pas de cluster allumé toute la journée et un coût plus bas. Garder Glue pour les transformations batch ultérieures.

<!-- takeaways -->

- Les jobs de streaming sont des micro-lots Spark toujours actifs.
- Chaque heure d'exécution est payée.
- Firehose pour la livraison simple ; Flink pour le complexe à faible latence.

<!-- unit: Exploiter des flux de façon fiable -->

<!-- goals -->

- Régler fenêtres et checkpoints pour un streaming fiable.
- Gérer petits fichiers, mises à jour de code et événements tardifs.

<!-- concept -->

La fiabilité en streaming vient du checkpoint : il enregistre ce qui a été lu et l'état existant, pour qu'un job redémarré reprenne exactement là où il s'est arrêté. Tout le reste découle de sa protection. Les changements de code doivent rester compatibles avec lui, et la sortie doit tolérer qu'un lot soit écrit deux fois.

La taille de fenêtre est l'arbitrage principal : plus courte, les données sont plus fraîches mais les fichiers plus nombreux et plus petits, à compacter ensuite.

<!-- example -->

```python
glue.forEachBatch(frame=stream_df,
    batch_function=write_batch,
    options={"windowSize": "120 seconds",
             "checkpointLocation": "s3://glue-checkpoints/orders_stream/"})
```

#### Qu'est-ce que la taille de fenêtre dans le streaming Glue ?

L'intervalle de chaque micro-lot (`windowSize`, par exemple 100 secondes) dans `forEachBatch`. Des fenêtres plus grandes réduisent les petits fichiers et la surcharge ; des fenêtres plus petites réduisent la latence.

#### Où un job de streaming conserve-t-il sa progression ?

Dans un emplacement de checkpoint sur S3, qui stocke les offsets et l'état pour que le job reprenne là où il s'est arrêté après un redémarrage ou une mise à jour.

#### Comment éviter les petits fichiers produits par les jobs de streaming ?

Utiliser des fenêtres plus grandes, écrire dans des tables Iceberg ou Hudi et les compacter (ou s'appuyer sur la compaction du catalogue pour Iceberg), ou lancer un job de compaction séparé.

#### Comment mettre à jour le code d'un job de streaming en cours ?

Arrêter le job et démarrer la nouvelle version avec le même emplacement de checkpoint, tant que les changements sont compatibles avec l'état stocké ; des changements incompatibles exigent un nouveau checkpoint et un plan pour rejouer ou ignorer des données.

#### Comment gérer les événements tardifs dans le streaming Glue ?

Avec les fenêtres en temps d'événement et les watermarks de Spark Structured Streaming pour les agrégations, ou en écrivant les événements dans des partitions par date d'événement et en laissant les jobs en aval retraiter les partitions récentes.

<!-- challenge -->

Après un déploiement, un job de streaming relit le flux depuis le début et duplique une journée de données. Que s'est-il passé ?

<!-- solution -->

La nouvelle version a utilisé un autre emplacement de checkpoint (ou un vide) et n'avait donc aucune trace de sa progression. Déployez avec le même chemin de checkpoint et rendez la destination idempotente (par exemple `MERGE` dans Iceberg sur l'identifiant d'événement) pour que les relectures ne dupliquent pas.

<!-- takeaways -->

- Le checkpoint garde la progression ; ne le perdez jamais.
- Fenêtres plus larges et compaction combattent les petits fichiers.
- Des destinations idempotentes sécurisent les relectures.

<!-- stage: Exécuter en production -->

### Workers, performances et coûts

<!-- unit: Dimensionner les workers -->

<!-- goals -->

- Choisir types et nombre de workers pour un job.
- Estimer le coût d'un job avant de le lancer.

<!-- concept -->

Dimensionner, c'est choisir entre plus de workers et des workers plus gros. Plus de workers ajoutent du parallélisme, utile quand les données se répartissent bien. Des workers plus gros ou à forte mémoire aident quand les tâches individuelles ont besoin de mémoire, comme dans les grosses jointures ou les lignes larges. L'auto scaling gère les jobs dont les étapes demandent des quantités différentes.

Comme le coût est workers × temps, un cluster plus gros qui finit bien plus tôt peut coûter autant, voire moins.

<!-- example -->

```text
G.1X × 20 workers × 0.5 h = 10 DPU-h  ≈ 4.40 USD
G.2X × 10 workers × 0.3 h =  6 DPU-h  ≈ 2.64 USD   (no spill, faster)
```

#### Quels types de workers Glue propose-t-il ?

G.1X (1 DPU : 4 vCPU, 16 Go), G.2X (2 DPU), G.4X (4 DPU), G.8X (8 DPU) et des types plus grands sur les versions récentes, G.025X (0,25 DPU, pour le streaming à faible volume) et des types R optimisés pour la mémoire. Les workers plus gros conviennent aux transformations gourmandes en mémoire ; davantage de workers conviennent au travail parallèle.

#### Comment choisir le nombre de workers ?

Partir du volume et de la complexité des données, activer l'autoscaling avec un maximum raisonnable, et regarder les métriques du job : si les executors sont inactifs, réduire ; si les stages déversent ou si les tâches attendent, augmenter ou prendre des workers plus gros. Mesurer le coût par exécution.

#### Quand utiliser des workers G.2X ou plus gros plutôt que davantage de G.1X ?

Quand les executors manquent de mémoire (grosses jointures, lignes larges, grosses agrégations, transformations ML) ou déversent beaucoup. Si les tâches sont petites et nombreuses, davantage de petits workers donnent le même parallélisme au même prix.

#### Que sont les workers de type R (optimisés mémoire) ?

Des types de workers avec plus de mémoire par CPU, pour les jobs limités par la mémoire plutôt que par le CPU, comme de grosses jointures broadcast ou la mise en cache.

#### Que nécessite `--enable-auto-scaling` ?

Glue 3.0 ou plus, un nombre maximal de workers et une charge qui varie d'un stage à l'autre. Glue ajuste alors les executors selon les tâches en attente.

#### Comment estimer le coût d'un job Glue ?

Workers × DPU par worker × durée en heures × prix du DPU-heure. Par exemple 10 workers G.1X pendant 15 minutes font 10 × 1 × 0,25 = 2,5 DPU-heures, environ 1,10 USD à 0,44 USD le DPU-heure. Avec l'autoscaling, regardez les DPU-secondes réelles dans le détail de l'exécution.

<!-- challenge -->

Les executors d'un job riche en jointures meurent par manque de mémoire sur 40 workers G.1X. Ajouter des workers n'a rien changé. Que tentez-vous ?

<!-- solution -->

Passer à des workers G.2X (ou de type R) pour donner plus de mémoire à chaque executor, avec moins de workers. Vérifier aussi les clés à skew et la possibilité de diffuser un petit côté, car une clé chaude échoue quel que soit le nombre de workers.

<!-- takeaways -->

- Plus de workers = parallélisme ; workers plus gros = mémoire.
- L'auto scaling convient aux jobs aux étapes inégales.
- Coût = workers × DPU × temps ; plus rapide peut coûter moins.

<!-- unit: Diagnostiquer les jobs lents -->

<!-- goals -->

- Utiliser la Spark UI et les métriques d'observabilité pour trouver les goulots.
- Enquêter sur un job devenu soudain lent.

<!-- concept -->

Un job Glue lent est un job Spark lent : les outils sont les mêmes. Trouvez l'étape la plus lente, puis demandez-vous si elle lit trop, déplace trop, fait du spill ou attend une tâche. Glue ajoute des métriques par job et par executor et une Spark UI construite à partir des event logs.

Quand un job ralentit soudain, comparez les exécutions avant de lire le code : taille d'entrée, nombre de fichiers, prédicats qui ne s'appliquent plus et configuration modifiée expliquent la plupart des régressions.

<!-- example -->

```text
--enable-metrics                 true
--enable-observability-metrics   true
--enable-spark-ui                true
--spark-event-logs-path          s3://glue-sparkui/orders_daily/
```

#### Comment diagnostiquer un job Glue lent ?

Activer les métriques du job, les métriques d'observabilité et la Spark UI (event logs dans S3), puis examiner la durée des stages, les tâches déséquilibrées, les volumes de shuffle et le spill, l'utilisation des executors et le nombre de fichiers en entrée. Job run insights pointe la ligne en échec et les causes fréquentes.

#### Qu'est-ce que la Spark UI de Glue ?

Une vue du Spark history server sur les event logs d'une exécution (activée avec `--enable-spark-ui` et un chemin de journaux S3), disponible dans la console Glue, pour analyser stages, tâches, stockage et plans SQL.

#### Que sont les métriques d'observabilité de Glue ?

Des métriques CloudWatch au niveau du job, du stage et de l'executor (CPU, mémoire, disque, shuffle, déséquilibre, utilisation des workers, débit) qui aident à repérer les goulots d'étranglement et à dimensionner les jobs.

#### Un job Glue qui prenait 10 minutes en prend maintenant 2 heures. Comment enquêtez-vous ?

Je compare le volume et le nombre de fichiers en entrée, je vérifie si le pushdown predicate ou les bookmarks ont cessé de fonctionner (tout est retraité), je cherche du déséquilibre ou du spill dans la Spark UI, je contrôle le nombre de workers et l'autoscaling, et je cherche une jointure modifiée ou un broadcast perdu.

<!-- challenge -->

La Spark UI montre une tâche sur 200 dans une étape qui tourne 50 minutes quand les autres prennent 20 secondes. De quoi s'agit-il et que tentez-vous ?

<!-- solution -->

D'un skew : une clé concentre la plupart des lignes. Vérifiez la distribution de la clé, comptez sur la gestion du skew par AQE, diffusez le petit côté si possible ou appliquez un salting à la clé chaude. Filtrer des clés parasites comme `NULL` suffit souvent.

<!-- takeaways -->

- Trouvez l'étape la plus lente, puis la cause.
- Comparez les exécutions : entrée, fichiers, prédicats, réglages.
- Une longue tâche isolée dans une étape signale presque toujours un skew.

<!-- unit: Shuffles, skew et mémoire -->

<!-- goals -->

- Utiliser AQE et la configuration Spark pour réduire les problèmes de shuffle.
- Corriger les erreurs de disque et de mémoire liées aux shuffles.

<!-- concept -->

Les shuffles déplacent les données entre workers pour les jointures et agrégations, et causent l'essentiel des échecs de mémoire et de disque. Adaptive Query Execution règle beaucoup de problèmes à l'exécution, en fusionnant les petites partitions, en passant aux broadcast joins et en découpant les partitions déséquilibrées.

Quand un shuffle est simplement plus gros que les disques des workers, on lui donne plus de place (workers plus gros, shuffle vers S3) ou on le réduit (filtrer tôt, sélectionner moins de colonnes, pré-agréger).

<!-- example -->

```text
--conf spark.sql.adaptive.enabled=true
--conf spark.sql.shuffle.partitions=400
--write-shuffle-files-to-s3 true
```

#### Comment l'Adaptive Query Execution de Spark aide-t-elle dans Glue ?

Activée par défaut depuis Glue 4.0, elle fusionne les petites partitions de shuffle, convertit les jointures en broadcast quand un côté est petit et découpe les partitions déséquilibrées, ce qui améliore les performances sans réglage manuel.

#### Comment traiter le déséquilibre des données dans un job Glue ?

Comme dans Spark : s'appuyer sur l'Adaptive Query Execution (activée sur les versions récentes de Glue), diffuser les petites tables, isoler ou saler les clés chaudes, et repérer les tâches retardataires dans la Spark UI.

#### Comment passer une configuration Spark à un job Glue ?

Avec le paramètre `--conf` (par exemple `--conf spark.sql.shuffle.partitions=400`), en sachant que certains réglages sont gérés par Glue et ne peuvent pas être modifiés.

#### Qu'est-ce que l'option de shuffle sur S3 de Glue ?

Une option (`--write-shuffle-files-to-s3`) qui écrit les données de shuffle de Spark dans S3 au lieu du disque local, évitant les erreurs « no space left on device » sur les jobs très shuffle, au prix d'un peu de vitesse.

#### Votre job Glue échoue avec « No space left on device ». Que faites-vous ?

Le job déverse ou redistribue plus que le disque local ne peut contenir. J'utilise des workers plus gros (plus de disque par executor), j'active l'option de shuffle sur S3, je réduis les données avant les shuffles (filtrer et sélectionner plus tôt), je corrige le déséquilibre et j'augmente les partitions pour que chaque tâche traite moins de données.

<!-- challenge -->

Un job agrège 2 To mais n'a besoin que de 5 colonnes sur 80. Il échoue avec des erreurs de disque. Quels deux changements en premier ?

<!-- solution -->

Sélectionner les 5 colonnes et appliquer les filtres avant l'agrégation, pour que le shuffle transporte bien moins de données. S'il y a encore du spill, utiliser des workers plus gros ou activer le shuffle vers S3.

<!-- takeaways -->

- AQE gère taille des partitions, broadcast et skew à l'exécution.
- Réduisez d'abord les shuffles : filtrez et sélectionnez tôt.
- Workers plus gros ou shuffle S3 donnent de la place aux shuffles.

<!-- unit: Organisation de la sortie -->

<!-- goals -->

- Écrire fichiers et partitions que l'aval lit à moindre coût.
- Corriger les petits fichiers en sortie de Glue.

<!-- concept -->

La sortie d'un job Glue est l'entrée de quelqu'un d'autre. Athena facture à l'octet scanné et planifie par fichier et partition : la façon dont un job écrit décide du coût des requêtes pendant des mois. L'objectif : formats colonnes, partitions raisonnables et fichiers de quelques centaines de mégaoctets.

Spark produit en général un fichier par tâche et par partition : sans étape de repartition, la sortie peut exploser en milliers de fichiers minuscules.

<!-- example -->

```python
(df.repartition("dt")                       # one task per date → few files per partition
   .write.mode("overwrite")
   .option("compression", "zstd")
   .partitionBy("dt")
   .parquet("s3://lake/curated/events/"))
```

#### Qu'est-ce que le problème des petits fichiers dans Glue, et comment le traiter ?

Lire de nombreux petits fichiers crée beaucoup de tâches et de requêtes S3 et ralentit les jobs. Glue peut regrouper les fichiers à la lecture (`groupFiles: inPartition`, `groupSize`), et il faut écrire des fichiers moins nombreux et plus gros (repartition avant l'écriture, de 128 Mo à 1 Go par fichier) ou compacter les tables Iceberg.

```python
dyf = glue.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://lake/raw/clicks/"], "recurse": True,
                        "groupFiles": "inPartition", "groupSize": "134217728"},
    format="json")
```

#### Comment écrire la sortie avec un nombre de fichiers maîtrisé ?

Faire un repartition ou un coalesce avant l'écriture (`df.repartition(20, "order_date")`), ou régler `spark.sql.files.maxRecordsPerFile`, pour que chaque partition contienne quelques gros fichiers au lieu de centaines de petits.

#### Pourquoi convertir le CSV ou le JSON brut en Parquet ?

Parquet est en colonnes et compressé : Athena, Redshift Spectrum et Spark ne lisent que les colonnes utiles, sautent des groupes de lignes grâce aux statistiques et lisent beaucoup moins de données, ce qui réduit durée et coût.

#### Qu'est-ce qui rend les fichiers Parquet efficaces pour les requêtes ultérieures ?

L'organisation en colonnes, la compression (Snappy ou ZSTD), les statistiques par groupe de lignes pour les sauter, des tailles de fichiers raisonnables (quelques centaines de Mo) et le tri ou le partitionnement selon les colonnes de filtre courantes.

#### Comment la stratégie de partitionnement influe-t-elle sur Glue et Athena ?

Partitionnez selon les colonnes utilisées par la plupart des filtres (généralement la date), avec un nombre modéré de partitions contenant chacune assez de données ; trop fin (par heure et par client) crée des millions de partitions minuscules et une planification lente, trop grossier impose de grosses lectures.

#### Un job Glue écrit des milliers de minuscules fichiers Parquet par jour. Comment corriger ?

Faire un repartition par la colonne de partition avant l'écriture pour que chaque partition ait peu de fichiers, augmenter la taille des lots (traiter une journée plutôt que toutes les quelques minutes) et, avec Iceberg, activer la compaction du catalogue ou lancer `rewrite_data_files`.

#### Les analystes trouvent coûteuses les requêtes Athena sur les tables Glue. Que changez-vous dans les jobs Glue ?

Écrire du Parquet ou de l'Iceberg au lieu de CSV/JSON, compresser, partitionner selon les filtres courants, produire des fichiers moins nombreux et plus gros, calculer des statistiques de colonnes, et éventuellement créer des tables agrégées pour les dashboards fréquents.

<!-- challenge -->

Un job écrit une table partitionnée par `dt` et `customer_id` et produit 400 000 fichiers par jour. Que changez-vous ?

<!-- solution -->

Partitionner seulement par `dt`, faire un repartition par `dt` avant l'écriture pour que chaque jour ait quelques gros fichiers, et trier ou faire du bucketing par `customer_id` à l'intérieur. Compacter une fois les données existantes.

<!-- takeaways -->

- L'organisation de la sortie décide du coût des requêtes en aval.
- Faites un repartition avant d'écrire pour maîtriser les fichiers.
- Partitionnez selon les filtres courants, pas les clés à forte cardinalité.

<!-- unit: Coût et démarrage -->

<!-- goals -->

- Appliquer les principaux leviers pour réduire les coûts Glue.
- Réduire le temps de démarrage des jobs.

<!-- concept -->

Réduire les coûts Glue, c'est surtout cesser de payer l'inactivité et le gaspillage : version la plus récente, auto scaling qui retire les workers en trop, Flex quand l'échéance le permet, traitements incrémentaux plutôt que rechargements complets, timeouts contre les jobs incontrôlés.

Le démarrage compte pour les petits jobs fréquents, où l'attente peut dépasser le travail. Les versions récentes démarrent plus vite, et les grosses installations de dépendances ralentissent chaque exécution.

<!-- example -->

| Levier | Effet typique |
|---|---|
| Passer à la dernière version de Glue | Démarrage et exécution plus rapides |
| Auto scaling | Moins de workers inactifs |
| Exécution Flex | Prix plus bas pour les jobs non urgents |
| Incrémental plutôt que rechargement complet | Moins de données traitées |

#### Comment réduire les coûts de Glue ?

Utiliser la dernière version de Glue (démarrage et exécution plus rapides), activer l'autoscaling, utiliser Flex pour les jobs non urgents, dimensionner correctement les workers, fixer des timeouts, traiter de façon incrémentale par partitions ou bookmarks, ne lire que les partitions et colonnes utiles, éviter les crawlers quand les tables peuvent être définies en code, et arrêter les endpoints de développement et les sessions inactives.

#### Pourquoi les jobs Glue mettent-ils du temps à démarrer, et comment réduire ce délai ?

Glue provisionne l'environnement à chaque exécution. Depuis Glue 2.0, le démarrage prend de quelques secondes à environ une minute ; Flex peut être plus long. On le réduit avec des versions récentes, moins de modules installés au démarrage (wheels préconstruits), et en évitant de multiplier de minuscules jobs qui pourraient n'en faire qu'un.

<!-- challenge -->

Un job tourne toutes les 5 minutes pour 40 secondes de travail et coûte plus que prévu. Pourquoi, et que changez-vous ?

<!-- solution -->

Chaque exécution paie un minimum et le temps de démarrage : le surcoût domine. Regrouper le travail en moins d'exécutions (par exemple toutes les 30 minutes), utiliser un job Python shell si Spark n'est pas nécessaire, ou passer à une conception streaming ou Lambda.

<!-- takeaways -->

- Payez le travail, pas l'inactivité : auto scaling, Flex, timeouts.
- Traitez des incréments, pas des rechargements complets.
- Les petits jobs fréquents gaspillent en démarrages.

### Qualité des données et données sensibles

<!-- unit: Règles de Data Quality -->

<!-- goals -->

- Écrire des règles DQDL, y compris composites et référentielles.
- Obtenir des recommandations de règles à partir de profils de données.

<!-- concept -->

Glue Data Quality transforme les attentes sur les données en règles exécutables à chaque chargement : volumes, complétude, unicité, valeurs autorisées, relations. Les écrire en DQDL les garde déclaratives et relisibles, comme du code.

Partir de zéro est difficile : les recommandations profilent une table et proposent des règles. Traitez-les comme un brouillon : gardez celles qui expriment de vraies attentes métier et resserrez les seuils au fil du temps.

<!-- example -->

```text
Rules = [
  RowCount > 1000,
  IsComplete "order_id", IsUnique "order_id",
  ColumnValues "status" in ["paid", "refunded", "cancelled"],
  (ColumnValues "amount" > 0) or (ColumnValues "status" = "refunded"),
  ReferentialIntegrity "customer_id" "customers.customer_id" = 1.0
]
```

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

#### Que sont les règles composites en DQDL ?

Des règles combinées avec `and` et `or`, par exemple `(ColumnValues "status" = "paid") and (ColumnValues "amount" > 0)`, pour exprimer des conditions portant sur plusieurs colonnes.

#### Comment vérifier l'intégrité référentielle avec Glue Data Quality ?

Avec des règles comme `ReferentialIntegrity`, qui compare une colonne à la colonne clé d'un autre jeu de données, ou `DatasetMatch` pour comparer deux jeux, en passant le jeu de référence comme source additionnelle.

#### Comment obtenir des recommandations de règles dans Glue Data Quality ?

Lancer une tâche de recommandation sur une table du catalogue : Glue profile les données et propose des règles DQDL (complétude, unicité, plages de valeurs, valeurs autorisées) qu'on revoit et modifie avant de les utiliser.

<!-- challenge -->

Une recommandation propose `ColumnValues "country" in [...]` avec les 12 pays actuels. L'acceptez-vous telle quelle ?

<!-- solution -->

Pas aveuglément : un nouveau marché ferait échouer le job. Confirmez la liste avec le métier, ou remplacez-la par un contrôle sur une table de référence, et décidez si une nouvelle valeur doit faire échouer le chargement ou seulement avertir.

<!-- takeaways -->

- Les règles DQDL déclarent les attentes en code.
- Règles composites et référentielles expriment la logique métier.
- Les recommandations sont un brouillon de départ.

<!-- unit: Agir sur la qualité et les données sensibles -->

<!-- goals -->

- Router, stocker et alerter sur les résultats de qualité.
- Détecter et traiter les données sensibles dans les pipelines.

<!-- concept -->

Une règle qui échoue en silence n'est que décoration. Les résultats de qualité doivent avoir des conséquences : les lignes en échec vont en quarantaine, les exécutions en échec cessent de publier et les responsables sont prévenus. La détection d'anomalies ajoute des contrôles que personne n'a écrits, en signalant les valeurs qui s'écartent de l'historique.

Les données sensibles posent un problème voisin : avant qu'elles atteignent les couches curées, la détection peut trouver les PII et les masquer, les hacher ou les retirer.

<!-- example -->

```python
dq = EvaluateDataQuality().process_rows(frame=orders, ruleset=RULES,
        publishing_options={"dataQualityEvaluationContext": "orders_dq",
                            "enableDataQualityCloudWatchMetrics": True})
rows = SelectFromCollection.apply(dfc=dq, key="rowLevelOutcomes")
passed = rows.filter(lambda r: r["DataQualityEvaluationResult"] == "Passed")
failed = rows.filter(lambda r: r["DataQualityEvaluationResult"] == "Failed")   # → quarantine
```

#### Comment agir sur les résultats de qualité dans un job ?

Utiliser la transformation Evaluate Data Quality, puis aiguiller les lignes : garder celles qui passent, écrire celles qui échouent dans un emplacement de quarantaine, et faire échouer le job ou envoyer une alerte EventBridge quand le score global passe sous un seuil.

#### Qu'est-ce que la détection d'anomalies de qualité ?

Glue apprend des statistiques au fil des exécutions (nombre de lignes, valeurs distinctes, distributions) et signale les valeurs inhabituelles même sans seuils explicites, ce qui détecte des problèmes comme une chute soudaine de volume.

#### Comment recevoir des alertes en cas d'échec de qualité ?

Glue publie les résultats de qualité dans EventBridge et CloudWatch ; des règles peuvent envoyer des notifications via SNS ou déclencher des processus de correction.

#### Où sont stockés les résultats de qualité ?

Dans l'historique de la console Glue, dans des métriques CloudWatch, sous forme d'événements EventBridge et, en option, écrits dans S3 par le job, où on peut les interroger avec Athena pour suivre les tendances.

#### Qu'est-ce que la détection de données sensibles dans Glue ?

Une transformation qui recherche des données personnelles comme les noms, e-mails, numéros de téléphone, cartes bancaires et identifiants nationaux (avec des détecteurs par pays), et peut masquer, hacher ou signaler ce qu'elle trouve, ce qui aide à respecter le RGPD.

<!-- challenge -->

Un jour, les volumes quotidiens ont chuté de 60 %, mais aucune règle n'a échoué car le seuil était `RowCount > 1000`. Qu'ajoutez-vous ?

<!-- solution -->

Activer la détection d'anomalies sur le volume (ou une règle comparant à la moyenne récente) et alerter les responsables via EventBridge. Les minimums statiques ne voient pas les fortes baisses relatives.

<!-- takeaways -->

- Mettez les lignes en échec en quarantaine ; bloquez les mauvaises publications.
- La détection d'anomalies attrape les dérives que les règles statiques manquent.
- Détectez et masquez les PII avant les couches curées.

### Orchestration

<!-- unit: Triggers et workflows -->

<!-- goals -->

- Construire des pipelines avec triggers et workflows Glue.
- Partager un état dans un workflow et reprendre après échec.

<!-- concept -->

Glue a sa propre orchestration légère. Les triggers lancent jobs et crawlers selon un calendrier, à la demande ou quand d'autres terminent ; les workflows les regroupent en un graphe avec une exécution et des propriétés partagées. Pour des pipelines entièrement dans Glue, cela évite un service de plus.

Les limites apparaissent quand les pipelines grandissent : branchements, relances entre services et backfills sont plus simples dans un orchestrateur généraliste.

<!-- example -->

```text
workflow orders_daily
  scheduled trigger 05:00 ─► job extract_orders
  conditional trigger (extract SUCCEEDED AND ...) ─► job build_curated
  conditional trigger (build SUCCEEDED) ─► job publish_marts
```

#### Que sont les triggers Glue ?

Des objets qui démarrent jobs et crawlers : planifiés (cron), conditionnels (quand d'autres jobs ou crawlers atteignent un état comme `SUCCEEDED`), à la demande, ou fondés sur des événements EventBridge (par exemple des lots d'événements S3).

#### Qu'est-ce qu'un workflow Glue ?

Un conteneur pour un graphe de triggers, crawlers et jobs représentant un pipeline ETL, avec une vue visuelle des exécutions, des propriétés d'exécution partagées (paramètres clé-valeur) et la possibilité de reprendre depuis une étape en échec.

#### Qu'est-ce que le prédicat d'un trigger conditionnel ?

La liste des jobs ou crawlers et des états qu'il surveille, avec une logique `AND` (toutes les conditions) ou `ANY` (une seule), par exemple « démarrer le job B quand le job A et le crawler C ont réussi ».

#### Que sont les propriétés d'exécution d'un workflow ?

Des paires clé-valeur partagées par tous les jobs d'une exécution de workflow, lues et mises à jour avec `get_workflow_run_properties` et `put_workflow_run_properties`, pour transmettre des valeurs comme une date de traitement d'une étape à l'autre.

#### Comment reprendre un workflow en échec ?

Dans la console ou l'API Glue (`ResumeWorkflowRun`), en sélectionnant les nœuds en échec à relancer après correction ; les nœuds terminés ne sont pas relancés.

<!-- challenge -->

Un workflow a échoué à son troisième job après deux heures pour les deux premiers. Comment continuer sans les relancer ?

<!-- solution -->

Corriger la cause, puis reprendre l'exécution du workflow (`ResumeWorkflowRun`) en sélectionnant le nœud en échec, pour que seuls lui et ses nœuds aval tournent avec les mêmes propriétés d'exécution.

<!-- takeaways -->

- Les triggers lancent les jobs selon calendrier, demande ou conditions.
- Les workflows regroupent les triggers et partagent des propriétés.
- Reprenez les nœuds en échec au lieu de tout relancer.

<!-- unit: Orchestrateurs externes et événements -->

<!-- goals -->

- Lancer des jobs Glue depuis Step Functions, Airflow et EventBridge.
- Transmettre les dates de traitement depuis l'orchestrateur.

<!-- concept -->

La plupart des plateformes orchestrent plus que Glue : Lambda, EMR, Athena, dbt, notifications. Un orchestrateur généraliste lance les jobs Glue, les attend et décide de la suite, le job n'ayant besoin que de ses arguments.

Les démarrages événementiels complètent le tableau : un fichier déposé dans S3 peut lancer un workflow ou un job via EventBridge, pour des pipelines qui réagissent aux données plutôt qu'à l'horloge.

<!-- example -->

```json
{
  "Type": "Task",
  "Resource": "arn:aws:states:::glue:startJobRun.sync",
  "Parameters": {"JobName": "orders_daily",
                 "Arguments": {"--process_date.$": "$.process_date"}},
  "Retry": [{"ErrorEquals": ["Glue.ConcurrentRunsExceededException"], "MaxAttempts": 3}],
  "Next": "PublishMarts"
}
```

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

#### EventBridge peut-il démarrer directement un job Glue ?

EventBridge peut cibler nativement des workflows Glue ; pour un job isolé, le schéma courant est EventBridge vers Step Functions ou vers une Lambda qui appelle `StartJobRun`.

#### Comment passer la date de traitement d'un orchestrateur à un job Glue ?

En argument du job dans `StartJobRun` (`--process_date=2026-10-16`), calculé par l'orchestrateur à partir de la date logique du planning, jamais à partir de l'horloge du job lui-même.

<!-- challenge -->

Un pipeline doit enchaîner Glue, une requête Athena et une notification Lambda, avec un autre chemin en cas d'échec. Workflow Glue ou Step Functions ?

<!-- solution -->

Step Functions : il appelle nativement Glue (`.sync`), Athena et Lambda, avec relances et branches catch pour le chemin d'échec. Les workflows Glue n'orchestrent que des jobs et crawlers Glue.

<!-- takeaways -->

- Prenez un orchestrateur généraliste quand le pipeline traverse des services.
- Les intégrations `.sync` attendent la fin des jobs Glue.
- Passez les dates en arguments depuis l'orchestrateur.

### Sécurité et gouvernance

<!-- unit: Identité des jobs et accès réseau -->

<!-- goals -->

- Donner aux jobs Glue des rôles au moindre privilège et des identifiants sûrs.
- Atteindre des bases privées sans exposer les jobs à Internet.

<!-- concept -->

Un job Glue agit avec les permissions de son rôle IAM : le rôle est la frontière de sécurité. Il ne doit atteindre que les buckets, clés et secrets nécessaires au job. Les identifiants de base de données vont dans Secrets Manager, référencés par des connections.

L'accès réseau est la seconde frontière. Les jobs qui lisent des bases privées tournent dans votre VPC via une connection et, sans NAT gateway, ne peuvent pas joindre Internet, avec des endpoints pour les services AWS utilisés.

<!-- example -->

```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": ["arn:aws:s3:::lake/raw/orders/*", "arn:aws:s3:::lake/curated/orders/*"]
}
```

#### De quels droits IAM un job Glue a-t-il besoin ?

Un job s'exécute avec un rôle IAM que Glue assume. Il lui faut les droits de `AWSGlueServiceRole` (ou équivalents), l'accès aux chemins S3 qu'il lit et écrit, à l'emplacement du script, au répertoire temporaire, aux clés KMS, aux secrets Secrets Manager des connexions et à CloudWatch Logs.

#### Comment restreindre un job Glue à certains préfixes S3 ?

Donner à son rôle IAM une politique n'autorisant que les préfixes de bucket et les clés KMS nécessaires et, avec Lake Formation, n'accorder que les tables nécessaires ; évitez les droits larges du type `s3:*`.

#### Comment éviter de coder en dur des identifiants dans les scripts Glue ?

Stocker les identifiants dans AWS Secrets Manager et référencer le secret dans la connexion Glue, ou le lire dans le script avec boto3 ; utiliser des rôles IAM pour les ressources AWS.

#### Comment les jobs Glue accèdent-ils aux bases situées dans un VPC ?

Via une connexion Glue avec VPC, sous-réseau et groupes de sécurité : Glue crée des interfaces réseau élastiques dans le sous-réseau. Celui-ci a besoin de routes vers la base et, pour accéder à S3, d'un endpoint passerelle S3 (ou d'un NAT pour Internet).

#### Comment empêcher les jobs Glue d'accéder à Internet ?

Les exécuter avec une connexion VPC dans des sous-réseaux privés sans NAT gateway, utiliser des endpoints VPC pour S3, Glue, CloudWatch, KMS et Secrets Manager, et héberger les dépendances Python dans S3 ou un dépôt privé.

<!-- challenge -->

Un job Glue ne parvient pas à se connecter à une base RDS dans un sous-réseau privé et expire. Que vérifiez-vous ?

<!-- solution -->

Que le job utilise une connection Glue avec le bon VPC, sous-réseau et security group ; que le security group s'autorise lui-même (auto-référence) et que la base l'accepte sur le port ; et que le sous-réseau dispose d'endpoints ou d'un NAT vers S3 et Secrets Manager.

<!-- takeaways -->

- Le rôle du job est la frontière de sécurité ; gardez-le étroit.
- Gardez les identifiants dans Secrets Manager.
- Les connections VPC atteignent les bases privées ; sans NAT, pas d'Internet.

<!-- unit: Lake Formation et accès fin -->

<!-- goals -->

- Expliquer comment Lake Formation gouverne les tables du catalogue Glue.
- Utiliser les LF-Tags et l'accès fin dans les jobs Spark.

<!-- concept -->

Les politiques IAM sur S3 contrôlent des fichiers, pas des tables. Lake Formation ajoute des permissions par table, colonne, ligne et cellule sur les objets du catalogue, et fournit aux moteurs des identifiants temporaires pour exactement ce qui est autorisé. Les LF-Tags le font passer à l'échelle : on classe tables et colonnes une fois et on accorde par tag.

Avec les versions récentes de Glue, les jobs Spark appliquent les mêmes permissions fines : la gouvernance ne s'arrête pas aux moteurs SQL.

<!-- example -->

```text
LF-Tag classification=pii on columns customers.email, customers.phone
Grant  analysts: SELECT on tables tagged domain=sales, excluding classification=pii
Grant  etl-role: SELECT, INSERT on domain=sales (all columns)
```

#### Comment Lake Formation fonctionne-t-il avec Glue ?

Lake Formation ajoute des droits fins (au niveau base, table, colonne, ligne et cellule, et un contrôle d'accès par tags avec les LF-Tags) au-dessus du Data Catalog. Des services comme Athena, Redshift Spectrum, EMR et Glue (5.0+) appliquent ces droits à la lecture des données.

#### Que sont les LF-Tags ?

Des tags Lake Formation (paires clé-valeur comme `domain=sales`, `classification=pii`) attachés aux bases, tables et colonnes ; les droits s'accordent sur des expressions de tags, ce qui passe mieux à l'échelle que des droits table par table.

#### Qu'est-ce que le contrôle d'accès fin pour les jobs Spark Glue ?

Avec Glue 5.0 et Lake Formation, les jobs Spark peuvent appliquer les droits au niveau table, colonne, ligne et cellule définis dans Lake Formation, pour que le rôle du job ne voie que les données autorisées.

<!-- challenge -->

Chaque mois, une nouvelle table contenant des e-mails clients apparaît, et chaque fois quelqu'un oublie de restreindre la colonne e-mail. Comment l'automatiser ?

<!-- solution -->

Utiliser les LF-Tags : accorder aux analystes par tag `domain` en excluant `classification=pii`, et taguer les nouvelles tables et colonnes PII à leur création (dans le modèle de table en code). Les nouvelles tables héritent alors du bon accès.

<!-- takeaways -->

- Lake Formation gouverne tables, colonnes, lignes et cellules.
- Les LF-Tags accordent par classification à grande échelle.
- Les jobs Spark Glue récents appliquent les permissions fines.

<!-- unit: Chiffrement et audit -->

<!-- goals -->

- Chiffrer sortie, logs et bookmarks avec les security configurations.
- Auditer l'activité de Glue et du catalogue.

<!-- concept -->

Glue écrit à plusieurs endroits en plus de votre sortie : logs, bookmarks, fichiers temporaires. Une security configuration les chiffre tous de façon cohérente avec vos clés KMS, sans dépendre de la mémoire de chaque développeur.

L'audit répond à « qui a changé ou lu quoi » : CloudTrail enregistre les appels d'API sur les jobs et le catalogue, et Lake Formation journalise l'accès aux données.

<!-- example -->

```python
glue.create_security_configuration(Name="lake-kms", EncryptionConfiguration={
    "S3Encryption": [{"S3EncryptionMode": "SSE-KMS", "KmsKeyArn": KEY}],
    "CloudWatchEncryption": {"CloudWatchEncryptionMode": "SSE-KMS", "KmsKeyArn": KEY},
    "JobBookmarksEncryption": {"JobBookmarksEncryptionMode": "CSE-KMS", "KmsKeyArn": KEY}})
```

#### Comment chiffrer les données avec Glue ?

Avec des configurations de sécurité qui activent le chiffrement des sorties S3 (SSE-S3 ou SSE-KMS), de CloudWatch Logs et des job bookmarks ; le chiffrement du catalogue avec KMS ; et des mots de passe de connexion stockés dans Secrets Manager ou chiffrés dans le catalogue.

#### Qu'est-ce qu'une configuration de sécurité Glue ?

Un ensemble nommé de réglages de chiffrement (mode de chiffrement S3 et clé KMS, chiffrement de CloudWatch Logs, chiffrement des job bookmarks) attaché aux jobs, crawlers et endpoints de développement.

#### Comment auditer l'activité Glue ?

CloudTrail journalise les appels d'API Glue (modifications de jobs et du catalogue), CloudWatch Logs conserve la sortie des jobs, Lake Formation fournit des traces d'audit des accès aux données et AWS Config peut suivre la configuration des ressources.

<!-- challenge -->

Un auditeur demande qui a modifié le schéma de la table `payments` le mois dernier. Où cherchez-vous ?

<!-- solution -->

Dans les événements CloudTrail `UpdateTable` sur cette table (utilisateur ou rôle et heure), et dans les versions de table du catalogue pour voir ce qui a changé. Si c'était un crawler, ses logs montrent l'exécution.

<!-- takeaways -->

- Les security configurations chiffrent sortie, logs et bookmarks.
- CloudTrail enregistre les changements de jobs et de catalogue.
- Les versions de table montrent l'évolution d'un schéma.

### Exploitation, CI/CD et intégration

<!-- unit: Jobs en code -->

<!-- goals -->

- Structurer, tester, versionner et déployer les jobs Glue en code.
- Exécuter un même job en dev, staging et prod.

<!-- concept -->

Un job Glue, c'est un script plus une définition : rôle, workers, arguments. Les traiter tous deux en code rend les environnements reproductibles : le même script tourne partout avec d'autres paramètres, et les outils d'infrastructure créent les jobs.

Les tests suivent le schéma habituel : logique dans des fonctions qui prennent et renvoient des DataFrames, testées en local avec pytest, tandis que le script du job ne fait que brancher entrées et sorties. Des chemins de scripts versionnés rendent les retours arrière triviaux.

<!-- example -->

```text
repo/
  jobs/orders_daily.py          # thin entry script
  src/etl_lib/transforms.py     # logic, built as a wheel
  tests/test_transforms.py
  infra/glue_jobs.tf            # job definitions per environment
```

#### Comment déployer des jobs Glue sous forme de code ?

Garder scripts et définitions de jobs dans Git, déployer avec CloudFormation, CDK, Terraform ou SAM : téléverser les scripts dans S3 et créer jobs, triggers, crawlers, connexions et tables du catalogue. Un pipeline de CI lance les tests, empaquette les bibliothèques en wheels et déploie dans chaque environnement.

#### Comment structurer le dépôt d'un projet Glue ?

Séparer les scripts d'entrée des jobs, un paquet Python partagé contenant la logique de transformation (construit en wheel), les tests, l'infrastructure as code (CDK, Terraform ou CloudFormation), les jeux de règles de qualité et la configuration par environnement.

#### Comment versionner les scripts Glue ?

Les garder dans Git et déployer des copies versionnées dans S3 (par exemple avec le SHA du commit dans le chemin), pour que chaque définition de job pointe vers une version connue du script et qu'un retour arrière consiste à repointer vers la précédente.

#### Comment tester la logique des jobs Glue ?

Placer la logique de transformation dans des fonctions qui prennent et renvoient des DataFrames, les tester avec pytest sur une SparkSession locale ou l'image Docker de Glue, tester le job de bout en bout sur des données d'exemple dans un compte de dev, et ajouter des règles de qualité pour les contrôles à l'exécution.

#### Comment passer un job Glue à une version plus récente ?

Changer la version de Glue dans une copie de dev, lancer les tests et comparer sorties et durées, lire les notes de migration (changements de Spark, Python et bibliothèques), vérifier connecteurs et JAR, puis promouvoir via la CI.

#### Comment exécuter le même job Glue en dev, staging et prod ?

Un seul script paramétré pour les chemins, bases et connexions, déployé par infrastructure as code pour chaque environnement (idéalement dans des comptes séparés), avec des arguments de job et des rôles IAM propres à chaque environnement, promu via la CI après les tests.

<!-- challenge -->

Un développeur a modifié dans la console le script d'un job de production pour corriger un bug. Une semaine plus tard, un déploiement a écrasé la correction. Comment l'éviter ?

<!-- solution -->

Faire de Git et de la CI le seul chemin vers la production : déployer scripts et définitions en infrastructure as code, retirer les droits d'édition console en prod et intégrer la correction au dépôt avec un test.

<!-- takeaways -->

- Scripts et définitions de jobs vont tous deux dans Git.
- Un script paramétré sert tous les environnements.
- Testez la logique comme de simples fonctions DataFrame.

<!-- unit: Surveillance et échecs -->

<!-- goals -->

- Surveiller la santé et la durée des jobs en production.
- Gérer les échecs avec relances, alertes et réexécutions.

<!-- concept -->

En production, les signaux importants sont simples : le job a-t-il échoué, expiré, duré bien plus que d'habitude ? Les événements d'état vont dans EventBridge et les métriques dans CloudWatch, qui couvrent ensemble alertes et tableaux de bord.

La gestion des échecs dépend de l'idempotence. Quand un job peut être relancé sans risque, relances et réexécutions sont de la routine ; sinon, chaque échec devient un nettoyage manuel.

<!-- example -->

```json
{
  "source": ["aws.glue"],
  "detail-type": ["Glue Job State Change"],
  "detail": {"state": ["FAILED", "TIMEOUT", "ERROR"]}
}
```

#### Comment superviser les jobs Glue en production ?

Avec les métriques et alarmes CloudWatch (échecs, durée, consommation de DPU), les événements EventBridge de changement d'état envoyés vers SNS ou Slack, job run insights pour les erreurs, et des tableaux de bord des durées et coûts des jobs dans le temps.

#### Comment gérer les échecs de jobs ?

Des relances pour les erreurs transitoires (uniquement pour des jobs idempotents), des alertes sur les états `FAILED` et `TIMEOUT`, une procédure de relance paramétrée pour la période en échec, et des chemins de quarantaine ou dead-letter pour les données défectueuses.

#### Comment alerter sur des jobs Glue trop longs ?

Fixer le timeout du job, ajouter une alarme CloudWatch sur le temps écoulé ou la métrique `glue.driver.aggregate.elapsedTime`, ou faire alerter l'orchestrateur quand une étape dépasse sa durée attendue.

<!-- challenge -->

Un job qui dure d'habitude 20 minutes a tourné 9 heures avant que quelqu'un s'en aperçoive. Quels deux contrôles manquaient ?

<!-- solution -->

Un timeout réaliste (par exemple 60 minutes) pour qu'il échoue au lieu de continuer, et une alarme sur la durée écoulée ou une règle EventBridge sur `TIMEOUT` qui prévient le responsable.

<!-- takeaways -->

- Les événements d'état EventBridge déclenchent les alertes d'échec.
- Fixez des timeouts et alertez sur les durées inhabituelles.
- Des jobs idempotents sécurisent relances et réexécutions.

<!-- unit: Glue dans l'écosystème AWS -->

<!-- goals -->

- Relier Glue à Athena, DMS, Redshift et EMR.
- Savoir quand zero-ETL, les connecteurs SaaS ou Amazon Q aident.

<!-- concept -->

Glue travaille rarement seul. DMS amène les changements des bases dans S3, Glue les applique aux tables du lake, Athena et Redshift interrogent le résultat et EMR lit le même catalogue. Les intégrations managées suppriment de plus en plus d'étapes entières : zero-ETL réplique des sources sans jobs et les connecteurs SaaS extraient depuis les applications métier.

Connaître ces liens répond souvent à « faut-il construire un job pour ça ? ».

<!-- example -->

```sql
-- Redshift reading Glue catalog tables directly
CREATE EXTERNAL SCHEMA lake FROM DATA CATALOG
DATABASE 'curated' IAM_ROLE 'arn:aws:iam::123456789012:role/redshift-spectrum';
SELECT count(*) FROM lake.orders WHERE dt = '2026-10-17';
```

#### Comment Glue et Athena fonctionnent-ils ensemble ?

Glue catalogue et transforme les données ; Athena interroge les tables du catalogue en SQL. Les jobs Glue convertissent souvent les données brutes en Parquet ou Iceberg partitionnés pour que les requêtes Athena soient rapides et peu coûteuses.

#### Comment Glue et AWS DMS fonctionnent-ils ensemble ?

DMS réplique des bases (chargement complet et CDC) dans S3 sous forme de fichiers avec indicateurs d'opération ; des jobs Glue appliquent ensuite les changements aux tables curées, typiquement avec `MERGE` sur des tables Iceberg ou Hudi.

#### Comment partager des tables Glue avec Amazon Redshift ?

Créer dans Redshift un schéma externe pointant vers une base Glue (`CREATE EXTERNAL SCHEMA ... FROM DATA CATALOG`), puis interroger les tables avec Redshift Spectrum, ou utiliser l'accès au Data Catalog monté automatiquement dans Redshift.

#### Comment EMR utilise-t-il le Glue Data Catalog ?

Les clusters EMR et EMR Serverless peuvent être configurés pour utiliser le Glue Data Catalog comme Hive metastore, de sorte que Spark, Hive, Presto et Trino sur EMR partagent les mêmes définitions de tables qu'Athena et Glue.

#### Qu'est-ce que le zero-ETL dans le contexte de Glue ?

Des intégrations gérées qui répliquent des données depuis des sources (applications SaaS comme Salesforce, SAP ou ServiceNow, et bases AWS comme DynamoDB) vers des cibles comme les tables de SageMaker Lakehouse ou Redshift sans construire de pipelines ETL, en les maintenant synchronisées.

#### À quoi servent AWS Glue for SAP et les autres connecteurs SaaS ?

À extraire les données d'applications d'entreprise (SAP OData, Salesforce, ServiceNow, Zendesk et d'autres) via des connecteurs gérés vers des jobs Glue ou des intégrations zero-ETL, sans écrire de code d'API.

#### Qu'est-ce qu'Amazon Q data integration dans Glue ?

Un assistant d'IA générative qui crée des jobs et transformations ETL Glue à partir de descriptions en langage naturel et aide à dépanner les jobs ; il existe aussi une mise à niveau assistée par l'IA des scripts Spark vers des versions plus récentes de Glue.

<!-- challenge -->

Une équipe prévoit un job Glue maison pour copier chaque nuit des objets Salesforce vers S3. Que vérifieriez-vous d'abord ?

<!-- solution -->

S'il existe une voie managée : le connecteur Salesforce de Glue ou une intégration zero-ETL peuvent répliquer les objets sans code d'extraction maison, en gérant pagination, limites d'API et changements incrémentaux.

<!-- takeaways -->

- DMS réplique ; Glue applique ; Athena et Redshift interrogent.
- Un seul catalogue sert Athena, Redshift et EMR.
- Vérifiez zero-ETL et les connecteurs avant de construire des jobs.

<!-- stage: Tout assembler -->

### Mises en situation

<!-- unit: Concevoir des pipelines de lake -->

<!-- goals -->

- Concevoir de bout en bout des pipelines batch et CDC sur Glue.
- Justifier chaque choix dans une réponse d'entretien.

<!-- concept -->

Les questions de conception testent votre capacité à relier les sections : comment arrivent les données, comment elles sont enregistrées, comment les jobs ne traitent que le nouveau, comment la sortie est organisée pour les requêtes, comment la qualité est contrôlée et comment le tout est orchestré. Suivez les données, nommez un choix par étape, puis dites ce qui se passe à la relance. Pour le CDC, ajoutez comment les changements sont appliqués, là où des formats comme Iceberg prennent tout leur sens.

<!-- example -->

```text
RDS ─► DMS (full load + CDC, Parquet with op column) ─► S3 raw
     ─► Glue job: dedupe per key, MERGE INTO Iceberg ─► curated.customers
     ─► Data Quality ruleset ─► Athena / Redshift
```

#### Concevez un pipeline qui transforme des dépôts CSV quotidiens dans S3 en jeu de données partitionné et interrogeable.

Déposer les CSV sous un préfixe raw daté, lancer un job Spark Glue (déclenché par EventBridge ou un planning) qui lit les fichiers du jour avec un schéma défini, nettoie et convertit les types, écrit en Parquet ou Iceberg partitionné par date dans un préfixe curé, met à jour le catalogue et exécute des règles de qualité. Athena ou Redshift Spectrum interrogent la table curée ; Lake Formation contrôle l'accès.

#### Comment charger le CDC d'une base RDS PostgreSQL dans un lakehouse avec Glue ?

Utiliser DMS pour le chargement complet et le CDC vers S3 (Parquet avec une colonne d'opération), ou une intégration zero-ETL si elle existe. Un job Glue lit les nouveaux fichiers de changements (bookmarks ou partitions par date), déduplique par clé en gardant le dernier changement et exécute `MERGE INTO` sur une table Iceberg enregistrée dans le Data Catalog. La compaction et l'expiration des snapshots la maintiennent en bonne santé.

<!-- challenge -->

Dans la conception CDC, DMS livre parfois deux fois le même changement. Comment votre pipeline reste-t-il juste ?

<!-- solution -->

Dédupliquer chaque lot sur clé primaire plus séquence de changement (ou horodatage), garder le dernier changement par clé et l'appliquer avec `MERGE` : rejouer un changement déjà appliqué ne modifie pas la table.

<!-- takeaways -->

- Suivez les données : arriver, enregistrer, traiter, organiser, contrôler, orchestrer.
- Rendez chaque étape idempotente.
- Le CDC exige des changements ordonnés, dédupliqués et un `MERGE`.

<!-- unit: Migrer un ETL historique -->

<!-- goals -->

- Planifier une migration de SSIS ou Informatica vers Glue.
- Valider les jobs migrés avant de basculer les consommateurs.

<!-- concept -->

Les outils d'ETL historiques cachent beaucoup de logique dans des mappings visuels, des lookups et des dépendances d'ordonnanceur. Une migration réussit quand cette logique devient explicite : inventorier jobs et dépendances, reconstruire les sources en connections, réécrire les transformations en Spark avec tests et remplacer l'ordonnanceur. Faire tourner l'ancien et le nouveau en parallèle et comparer les sorties crée la confiance nécessaire à la bascule.

<!-- example -->

| Historique | Équivalent Glue |
|---|---|
| Connection manager | Connection Glue + Secrets Manager |
| Data flow avec lookups | Job Spark avec jointures |
| Ordonnanceur SQL Agent / Informatica | Step Functions, Airflow ou workflows Glue |
| Variables de package | Arguments du job |

#### Comment migrer des jobs SSIS ou Informatica on-premise vers Glue ?

Inventorier les jobs et leurs dépendances, recréer les sources sous forme de connexions Glue, réécrire les transformations en PySpark (ou en jobs visuels), stocker les données de référence dans S3 ou le catalogue, orchestrer avec Step Functions ou Airflow, et valider les sorties côte à côte avant de basculer.

<!-- challenge -->

En exécution parallèle, le nouveau job produit 0,5 % de lignes de moins que le package SSIS. Comment trouver pourquoi ?

<!-- solution -->

Comparer les sorties par clé pour trouver les lignes manquantes et remonter leur origine : causes typiques, des jointures internes au lieu de left joins sur les lookups, des différences de casse ou d'espaces dans les clés, la gestion des `NULL` et des filtres de date différents.

<!-- takeaways -->

- Rendez explicite et testée la logique historique cachée.
- Remplacez délibérément ordonnanceurs et connections.
- Faites tourner en parallèle et comparez avant la bascule.
