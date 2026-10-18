## Fiche d'étude Amazon Athena

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude Amazon Athena : environ 200 questions](../../images/aws_athena_study_guide_title_img.png)

Environ 200 questions d'entretien sur Amazon Athena : le fonctionnement du SQL serverless sur S3, les tables et les SerDe, les partitions et la projection de partitions, les formats de fichiers, les tables Iceberg, `CTAS` et `UNLOAD`, les workgroups et la maîtrise des coûts, l'optimisation des performances, les requêtes fédérées, la sécurité et le dépannage. Les réponses décrivent le service tel qu'il est en 2026. Ouvrez une question pour voir sa réponse, ou utilisez le filtre pour chercher dans toute la fiche.

<!-- QA -->

### Fondamentaux

#### Qu'est-ce qu'Amazon Athena ?

Un service de requêtes interactives serverless qui permet d'analyser des données directement dans Amazon S3 (et d'autres sources via des connecteurs) en SQL standard. Aucune infrastructure à gérer : on définit des tables sur ses données, on lance des requêtes et on paie les données lues ou une capacité réservée.

#### Quel moteur Athena utilise-t-il ?

La version 3 du moteur SQL d'Athena repose sur Trino (anciennement PrestoSQL) avec des améliorations propres à AWS, et le DDL utilise une syntaxe compatible Hive. Athena propose aussi Apache Spark via les notebooks Athena pour les charges PySpark.

#### Quels sont les cas d'usage typiques d'Athena ?

L'analyse ad hoc de data lakes, l'interrogation de journaux (CloudTrail, VPC Flow Logs, ALB, CloudFront, journaux d'accès S3), un ELT léger avec `CTAS` et `INSERT INTO`, l'alimentation d'outils BI comme QuickSight, l'exploration de données avant de construire des pipelines et l'interrogation de tables Iceberg dans un lakehouse.

#### Comment Athena est-il facturé ?

Par défaut, au téraoctet lu (environ 5 USD par To dans de nombreuses régions), avec un minimum de 10 Mo par requête, arrondi au mégaoctet. Les instructions DDL et les requêtes en échec ne sont pas facturées. Les réservations de capacité proposent à la place un prix fixe par DPU-heure. Le stockage et les requêtes S3 ainsi que l'usage du Glue Data Catalog sont facturés à part.

#### Pourquoi le format des données compte-t-il autant pour le coût d'Athena ?

Parce qu'on paie à l'octet lu. Les formats en colonnes et compressés (Parquet, ORC) permettent à Athena de ne lire que les colonnes nécessaires et de sauter des blocs grâce aux statistiques, ce qui réduit souvent les données lues de 90 % ou plus par rapport à du CSV ou du JSON non compressé.

#### Où Athena stocke-t-il les définitions de tables ?

Dans l'AWS Glue Data Catalog (par défaut), dans un Hive metastore externe, ou dans d'autres catalogues enregistrés comme sources de données (connecteurs fédérés, Redshift, catalogues S3 Tables).

#### Où vont les résultats des requêtes ?

Dans un emplacement de résultats S3 (défini par workgroup ou par requête) sous forme de fichier CSV accompagné d'un fichier de métadonnées, ou dans le stockage de résultats géré qu'Athena conserve pour une durée limitée. Les résultats peuvent être chiffrés et devraient avoir une règle de cycle de vie pour expirer les anciens fichiers.

#### Comment Athena se compare-t-il à Amazon Redshift ?

Athena est serverless et interroge les données sur place dans S3, idéal pour les charges ad hoc, intermittentes ou exploratoires, avec un paiement à la requête. Redshift est un entrepôt (provisionné ou serverless) optimisé pour une analytique complexe, fréquente et très concurrente sur des données chargées dans son stockage géré, avec des fonctions comme les vues matérialisées et la gestion des charges. Beaucoup d'architectures utilisent les deux.

#### Comment Athena se compare-t-il à Redshift Spectrum ?

Les deux interrogent des données S3 via le Glue Data Catalog. Spectrum s'exécute depuis un cluster Redshift et permet de joindre les données S3 aux tables Redshift ; Athena est autonome et serverless. Spectrum est utile quand l'entrepôt existe déjà.

#### Comment Athena se compare-t-il à Trino ou Spark sur EMR ?

Athena supprime la gestion de clusters et facture à la requête ou à la capacité, mais offre moins de contrôle sur la configuration et les ressources. EMR convient aux charges très volumineuses et régulières, aux configurations sur mesure ou aux outils au-delà du SQL.

#### Qu'est-ce qu'un workgroup ?

Un moyen de séparer utilisateurs, équipes ou applications : chaque workgroup a son emplacement de résultats, ses réglages de chiffrement, sa version de moteur, ses limites d'usage de données, ses métriques CloudWatch et son historique de requêtes, et IAM peut contrôler qui utilise quel workgroup.

#### Quelles sont les principales interfaces d'Athena ?

L'éditeur de requêtes de la console, la CLI et les SDK AWS (`StartQueryExecution`, `GetQueryExecution`, `GetQueryResults`), les pilotes JDBC et ODBC pour les outils BI et SQL, les notebooks Athena pour Spark, et les intégrations avec QuickSight, Glue, Step Functions et Airflow.

#### Athena est-il ACID ?

Pour les tables de style Hive, non : les requêtes lisent les fichiers présents, et les écritures ajoutent des fichiers sans transaction. Pour les tables Apache Iceberg, oui : Athena prend en charge `INSERT`, `UPDATE`, `DELETE` et `MERGE` ACID avec isolation par snapshots et voyage dans le temps.

#### Quel est le cycle de vie d'une requête dans Athena ?

La requête est soumise (`QUEUED`), planifiée à l'aide des métadonnées du catalogue et de l'élagage des partitions, exécutée en parallèle sur le calcul géré d'Athena en lisant S3 (`RUNNING`), puis se termine en `SUCCEEDED`, `FAILED` ou `CANCELLED`, les résultats étant écrits à l'emplacement prévu.

#### Quelles limites d'Athena faut-il connaître ?

Des quotas par compte sur les requêtes DML et DDL actives simultanément, un timeout de requête (30 minutes par défaut pour le DML, ajustable), la longueur du texte de requête, le nombre de partitions qu'une seule requête peut ajouter, et les débits de requêtes S3 par préfixe qui peuvent brider les lectures très parallèles.

#### Que signifie « schéma à la lecture » (schema on read) dans Athena ?

Le schéma s'applique quand les données sont lues, pas quand elles sont écrites : n'importe quel outil peut écrire les fichiers S3, et la définition de table indique à Athena comment les interpréter à la requête. C'est souple, mais les fichiers défectueux n'apparaissent qu'à l'interrogation, sous forme d'erreurs ou de `NULL`.

#### Que signifie « serverless » pour Athena ?

Il n'y a pas de clusters à dimensionner, démarrer ou patcher : AWS exploite un moteur de requêtes partagé et multi-locataire, alloue les ressources par requête, et vous payez à la requête (ou à la capacité réservée). Rien ne tourne quand vous n'interrogez pas.

#### Quels services AWS alimentent couramment Athena en données ?

Kinesis Data Firehose (flux vers S3), AWS Glue (ETL et catalogue), AWS DMS (réplication de bases vers S3), les services AWS qui écrivent leurs journaux dans S3, S3 Inventory et les applications qui écrivent directement des fichiers.

#### Athena peut-il écrire des données ?

Oui : `CTAS`, `INSERT INTO`, `UNLOAD`, et le DML complet (`UPDATE`, `DELETE`, `MERGE`) sur les tables Iceberg. Sur les tables de style Hive, il ne peut qu'ajouter de nouveaux fichiers.

#### Que sont les versions du moteur Athena, et comment sont-elles mises à jour ?

Athena fait évoluer son moteur par versions (la v3 est l'actuelle) ; les workgroups peuvent choisir les mises à jour automatiques ou une version précise. Une mise à jour peut changer le comportement de fonctions ou la gestion des types : testez les requêtes critiques avant de basculer.

#### Que sont les requêtes enregistrées de l'éditeur Athena ?

Des requêtes nommées enregistrées par workgroup que les utilisateurs peuvent réutiliser et partager, utiles pour les analyses récurrentes, même si le contrôle de version dans Git est préférable pour le SQL de production.

### Tables, DDL et SerDe

#### Comment créer une table dans Athena ?

Avec `CREATE EXTERNAL TABLE`, en indiquant les colonnes, l'emplacement S3, le format ou le SerDe, les colonnes de partition et les propriétés de la table :

```sql
CREATE EXTERNAL TABLE logs.app_events (
  event_id   string,
  user_id    bigint,
  event_type string,
  payload    string,
  event_ts   timestamp
)
PARTITIONED BY (dt string)
STORED AS PARQUET
LOCATION 's3://my-lake/curated/app_events/'
TBLPROPERTIES ('parquet.compression' = 'SNAPPY');
```

#### Pourquoi les tables Athena sont-elles « externes » ?

Athena ne stocke que des métadonnées ; les données restent dans S3. Supprimer une table externe retire la définition mais pas les fichiers (les tables Iceberg sont différentes : les supprimer peut effacer les données).

#### Qu'est-ce qu'un SerDe ?

Un sérialiseur/désérialiseur qui indique à Athena comment lire et écrire un format : `LazySimpleSerDe` pour le texte délimité, `OpenCSVSerDe` pour le CSV avec guillemets, `JsonSerDe` (Hive ou OpenX) pour le JSON, `RegexSerDe` et `GrokSerDe` pour les journaux, et des lecteurs natifs pour Parquet, ORC et Avro.

#### Quand utiliser `OpenCSVSerDe` plutôt que `LazySimpleSerDe` ?

Quand les champs CSV sont entre guillemets et peuvent contenir des virgules. `OpenCSVSerDe` gère les guillemets mais traite toutes les colonnes comme des chaînes sauf conversion explicite, et a des limites sur certains types ; `LazySimpleSerDe` est plus rapide pour les fichiers délimités simples.

#### Comment ignorer la ligne d'en-tête des fichiers CSV ?

Avec la propriété de table `'skip.header.line.count'='1'`.

#### Comment lire du JSON dans Athena ?

Avec un SerDe JSON, un objet JSON par ligne. Le SerDe OpenX propose des options comme `ignore.malformed.json` et un mappage insensible à la casse. Les objets imbriqués deviennent des `struct` et les tableaux des `array`.

```sql
CREATE EXTERNAL TABLE raw.orders_json (
  order_id string,
  customer struct<id:bigint, country:string>,
  items array<struct<sku:string, qty:int, price:double>>
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES ('ignore.malformed.json' = 'true')
LOCATION 's3://my-lake/raw/orders/';
```

#### Comment interroger des tableaux imbriqués ?

Avec `UNNEST` dans un `CROSS JOIN`, qui produit une ligne par élément du tableau :

```sql
SELECT o.order_id, i.sku, i.qty
FROM raw.orders_json o
CROSS JOIN UNNEST(o.items) AS t(i);
```

#### Comment analyser du JSON stocké dans une colonne texte ?

Avec les fonctions JSON comme `json_extract_scalar(payload, '$.customer.id')`, `json_extract`, `json_parse` et `CAST(json_parse(payload) AS map(varchar, json))`.

#### Que se passe-t-il si les données ne correspondent pas au schéma de la table ?

Athena applique le schéma à la lecture : les valeurs incompatibles deviennent en général `NULL` ou provoquent des erreurs comme `HIVE_BAD_DATA` (par exemple une chaîne dans une colonne entière, ou un type de colonne Parquet différent du type de la table).

#### Athena gère-t-il l'évolution du schéma ?

En Parquet, ajouter des colonnes en fin de schéma et lire par nom fonctionne ; renommer ou changer de type est risqué. En CSV, les colonnes sont positionnelles : seul l'ajout en fin est sûr. Les tables Iceberg prennent en charge une vraie évolution de schéma (ajout, suppression, renommage, réordonnancement, élargissement de types).

#### Qu'est-ce qu'une vue dans Athena ?

Une requête enregistrée (`CREATE VIEW`) dans le catalogue, qu'on interroge comme une table. Elle ne stocke pas de données : chaque requête lit les tables sous-jacentes et est facturée en conséquence.

#### Que fait `MSCK REPAIR TABLE` ?

Il parcourt l'emplacement S3 de la table à la recherche de dossiers de partition de style Hive (`cle=valeur`) et ajoute au catalogue les partitions manquantes. Il est lent sur les tables très partitionnées ; mieux vaut ajouter les partitions explicitement ou utiliser la projection de partitions.

#### Que fait `SHOW CREATE TABLE` ?

Il affiche le DDL d'une table, pratique pour copier des définitions entre environnements ou vérifier le SerDe et les propriétés.

#### Comment interroger les journaux des services AWS avec Athena ?

Créer des tables avec le DDL documenté pour chaque type de journal (CloudTrail, VPC Flow Logs, ALB, CloudFront, journaux d'accès S3), idéalement avec une projection de partitions par date et région, puis les interroger en SQL pour enquêter sur les événements de sécurité, le trafic et les erreurs.

#### Comment modifier les colonnes d'une table ?

Avec `ALTER TABLE … ADD COLUMNS`, `REPLACE COLUMNS` ou `CHANGE COLUMN` (le comportement dépend du format), ou en recréant la table. Pour Iceberg, `ALTER TABLE … ADD COLUMNS`, `DROP COLUMN` et `RENAME COLUMN` sont des opérations sûres sur les métadonnées.

#### Comment Athena mappe-t-il les colonnes Parquet : par nom ou par position ?

Par nom, par défaut, pour Parquet : l'ordre des colonnes de la table n'a pas à correspondre à celui des fichiers. Le CSV et les autres formats texte mappent par position.

#### Quels types de données Athena prend-il en charge ?

`boolean`, `tinyint`, `smallint`, `int`, `bigint`, `double`, `float`, `decimal(p,s)`, `char`, `varchar`, `string`, `binary`, `date`, `timestamp`, et les types complexes `array`, `map` et `struct`.

#### Comment lire des fichiers avec un délimiteur personnalisé ?

`ROW FORMAT DELIMITED FIELDS TERMINATED BY '|'` (ou `\t` pour le TSV), avec les options `ESCAPED BY` et `LINES TERMINATED BY` si besoin.

#### Comment interroger des données à l'aide d'une expression régulière ?

Définir une table avec `RegexSerDe` et une propriété `input.regex` dont les groupes de capture correspondent aux colonnes, utile pour des journaux à format fixe ; pour une analyse ponctuelle, utiliser `regexp_extract` sur une seule colonne texte.

#### Comment n'interroger que certains fichiers d'un emplacement ?

Utiliser la pseudo-colonne `"$path"` (le chemin S3 du fichier de chaque ligne) dans une clause `WHERE`, ce qui aide aussi à repérer quel fichier contient des données défectueuses.

```sql
SELECT "$path", count(*) FROM raw.app_events_csv GROUP BY 1 ORDER BY 2 DESC;
```

#### Quelles autres pseudo-colonnes existent ?

`"$path"`, `"$file_size"` et `"$file_modified_time"` décrivent le fichier source de chaque ligne, utiles pour le lignage, le débogage et le traitement incrémental.

### Partitions et projection de partitions

#### Qu'est-ce que le partitionnement dans Athena ?

Organiser les données dans S3 selon les valeurs d'une ou plusieurs colonnes (`s3://bucket/table/dt=2026-10-15/`) et les déclarer comme colonnes de partition, pour que les requêtes qui filtrent dessus ne lisent que les dossiers correspondants.

#### Qu'est-ce que l'élagage de partitions (partition pruning) ?

Le moteur utilise les filtres sur les colonnes de partition pour écarter les partitions qui ne peuvent pas correspondre, ce qui réduit les données lues. Cela ne fonctionne que si le filtre porte sur la colonne de partition elle-même, sans fonction qui empêche son évaluation à la planification.

#### Comment ajouter des partitions ?

`ALTER TABLE t ADD PARTITION (dt='2026-10-15') LOCATION 's3://.../dt=2026-10-15/'`, `MSCK REPAIR TABLE` pour les dossiers de style Hive, un crawler Glue, l'API Glue ou la projection de partitions (sans enregistrement).

#### Qu'est-ce que la projection de partitions ?

Une configuration de table où Athena calcule les valeurs et emplacements des partitions à partir de règles dans les propriétés de la table (plages de dates ou d'entiers, énumérations, valeurs injectées) au lieu de les lire dans le catalogue. Les nouvelles partitions n'ont pas besoin d'être enregistrées et la planification est plus rapide pour les tables très partitionnées.

```sql
ALTER TABLE logs.app_events SET TBLPROPERTIES (
  'projection.enabled' = 'true',
  'projection.dt.type' = 'date',
  'projection.dt.range' = '2024-01-01,NOW',
  'projection.dt.format' = 'yyyy-MM-dd',
  'storage.location.template' = 's3://my-lake/curated/app_events/dt=${dt}/'
);
```

#### Quand la projection de partitions ne convient-elle pas ?

Quand les valeurs de partition sont imprévisibles (par exemple des identifiants clients arbitraires inconnus à l'avance, sauf avec le type `injected` et des filtres obligatoires), quand d'autres moteurs (EMR, Spark) ont aussi besoin des partitions dans le catalogue, ou quand la plupart des partitions projetées n'existent pas (Athena sonderait de nombreux préfixes vides).

#### Qu'est-ce que le type de projection injected ?

Un type de projection où la valeur de partition doit figurer dans la clause `WHERE` de la requête (par exemple `customer_id = '123'`) ; Athena l'utilise pour construire l'emplacement. Il convient aux clés à forte cardinalité toujours utilisées en filtre.

#### Quelle est une bonne stratégie de partitionnement ?

Partitionner selon les colonnes filtrées par la plupart des requêtes (généralement la date), à une granularité qui garde chaque partition suffisamment volumineuse (au moins quelques dizaines de Mo, idéalement plus), et éviter les clés à forte cardinalité qui créent des millions de minuscules partitions.

#### Quelle différence entre chemins de partition de style Hive et non Hive ?

Les chemins de style Hive contiennent `cle=valeur` (`dt=2026-10-15/`), que `MSCK REPAIR` et les crawlers comprennent. Les chemins non Hive (`2026/10/15/`) exigent d'ajouter les partitions explicitement avec un `LOCATION`, ou une projection de partitions avec un modèle d'emplacement.

#### Qu'est-ce que le bucketing dans Athena ?

La répartition des données d'une partition dans un nombre fixe de fichiers selon le hachage d'une colonne (`CLUSTERED BY (user_id) INTO 32 BUCKETS`), qui aide les requêtes filtrant sur cette colonne à sauter des fichiers. On l'utilise surtout avec `CTAS`.

#### Pourquoi un trop grand nombre de partitions nuit-il aux performances ?

La planification doit récupérer et évaluer les métadonnées des partitions, et chaque partition implique souvent des listages S3 séparés et de petits fichiers. Les index de partition Glue ou la projection de partitions réduisent le coût de planification.

#### Comment voir les partitions d'une table ?

`SHOW PARTITIONS table` liste les partitions enregistrées (pas celles projetées), et la console ou l'API Glue montrent les emplacements et schémas des partitions.

#### Comment supprimer des partitions ?

`ALTER TABLE t DROP PARTITION (dt='2026-10-01')` ne supprime que les métadonnées du catalogue ; supprimez les objets S3 séparément si les données doivent disparaître aussi.

#### Peut-on mélanger projection de partitions et partitions du catalogue ?

Quand la projection est activée, Athena ignore les partitions enregistrées dans le catalogue pour cette table et n'utilise que les règles de projection. Les autres moteurs voient toujours les partitions du catalogue.

#### Comment partitionner par date quand les données contiennent des horodatages ?

Dériver à l'écriture une date sous forme de chaîne (ou année/mois/jour) et la stocker en colonne de partition ; avec Iceberg, utiliser le partitionnement caché `day(event_ts)` pour que les requêtes filtrent directement sur l'horodatage.

#### Pourquoi une requête peut-elle ne pas élaguer les partitions alors qu'elle filtre sur la date ?

Le filtre applique peut-être une fonction à la colonne de partition (par exemple `date(dt) = …` sur une colonne texte), compare avec un type qui impose une conversion, ou filtre sur une autre colonne que la clé de partition. Filtrez sur la colonne de partition avec des littéraux du même type.

### Formats de fichiers et organisation des données

#### Quels formats de fichiers Athena prend-il en charge ?

Le CSV/TSV et d'autres textes délimités, JSON, Parquet, ORC, Avro, Ion, les journaux via les SerDe Regex ou Grok, et les formats de table ouverts Iceberg, Hudi (lecture) et Delta Lake (lecture).

#### Pourquoi recommande-t-on Parquet et ORC ?

Ils sont en colonnes (lecture des seules colonnes utiles), compressés par colonne, et stockent des statistiques (min/max par groupe de lignes ou stripe) qui permettent à Athena de sauter des données. Ils prennent aussi en charge la poussée des prédicats, ce qui accélère les requêtes et réduit le coût.

#### Quels codecs de compression conviennent ?

Snappy et ZSTD pour Parquet et ORC (rapides, découpables au sein du format). Pour les fichiers texte, gzip est courant mais non découpable : un gros fichier gzip est lu par un seul worker ; bzip2 est découpable mais lent.

#### Quelle est la taille de fichier idéale pour Athena ?

Environ 128 Mo à 1 Go par fichier. De nombreux petits fichiers (quelques Ko) ajoutent une surcharge par fichier et des coûts de requêtes S3 ; de très gros fichiers non découpables limitent le parallélisme.

#### Comment corriger une table composée de nombreux petits fichiers ?

Les compacter : lancer un `CTAS` ou un `INSERT INTO` qui réécrit les données en fichiers moins nombreux et plus gros (avec bucketing ou un partitionnement maîtrisé), utiliser `OPTIMIZE` sur les tables Iceberg, ou corriger le producteur (lots plus gros, buffering Firehose).

#### En quoi trier les données aide-t-il Athena ?

Quand les données sont triées (ou regroupées) selon une colonne de filtre courante à l'intérieur des fichiers, les statistiques Parquet et ORC ont des plages min/max étroites, ce qui permet de sauter davantage de groupes de lignes.

#### Que signifie la projection en colonnes pour `SELECT *` ?

Avec Parquet ou ORC, sélectionner moins de colonnes lit moins d'octets : un `SELECT *` sur une table large coûte bien plus que la sélection des seules colonnes utiles.

#### Comment convertir du CSV en Parquet avec Athena ?

Avec `CTAS` :

```sql
CREATE TABLE curated.app_events
WITH (
  format = 'PARQUET',
  write_compression = 'ZSTD',
  external_location = 's3://my-lake/curated/app_events/',
  partitioned_by = ARRAY['dt']
) AS
SELECT event_id, user_id, event_type, event_ts, dt
FROM raw.app_events_csv;
```

#### Athena prend-il en charge S3 Express One Zone ou S3 Tables ?

Oui. Athena peut interroger des données dans des directory buckets S3 Express One Zone pour une latence plus faible, et peut interroger et gérer des tables Iceberg dans S3 Tables (table buckets) via leur intégration de catalogue.

#### Qu'est-ce que la poussée des prédicats (predicate pushdown) dans Athena ?

Les filtres sont poussés jusqu'au lecteur de fichiers, qui utilise les statistiques Parquet/ORC pour sauter les groupes de lignes ou stripes dont le min/max ne peut pas correspondre : moins de données sont lues et décompressées.

#### Quelle taille de groupe de lignes est bonne pour Parquet ?

Typiquement de 128 Mo à 512 Mo ; des groupes plus gros compressent bien et réduisent la surcharge, mais des groupes énormes réduisent l'efficacité du saut de données. Des écrivains comme Spark ont des valeurs par défaut raisonnables.

#### La compression réduit-elle les coûts d'Athena ?

Oui. Athena facture les octets compressés lus : des fichiers compressés (et l'encodage en colonnes) réduisent directement le coût, en plus du stockage S3.

#### Quelle différence entre Parquet et ORC pour Athena ?

Les deux sont en colonnes, avec statistiques et compression, et fonctionnent bien. Parquet est le choix le plus courant dans l'écosystème (Spark, valeurs par défaut d'Iceberg) ; ORC a été historiquement privilégié par Hive. Choisissez selon les écrivains et les autres moteurs utilisés.

#### Comment traiter des données qui arrivent en un seul énorme fichier gzip ?

gzip n'étant pas découpable, un seul worker le lit. Découpez le fichier avant ou pendant l'ingestion, recompressez en bzip2 ou, mieux, convertissez en Parquet avec un `CTAS` ou un job Glue.

### Tables Iceberg dans Athena

#### Qu'est-ce qu'Apache Iceberg, et pourquoi l'utiliser avec Athena ?

Un format de table ouvert qui ajoute une couche de métadonnées (snapshots, manifestes) au-dessus de fichiers Parquet, apportant transactions ACID, évolution du schéma et des partitions, partitionnement caché, voyage dans le temps et modifications au niveau ligne efficaces. Athena peut créer, lire et écrire des tables Iceberg enregistrées dans le Glue Data Catalog.

#### Comment créer une table Iceberg dans Athena ?

```sql
CREATE TABLE lake.customers (
  customer_id bigint,
  email       string,
  country     string,
  updated_at  timestamp
)
PARTITIONED BY (country)
LOCATION 's3://my-lake/iceberg/customers/'
TBLPROPERTIES ('table_type' = 'ICEBERG', 'format' = 'parquet');
```

#### Quelles instructions DML Athena prend-il en charge sur Iceberg ?

`INSERT INTO`, `UPDATE`, `DELETE` et `MERGE INTO`, ainsi que `CREATE TABLE AS SELECT` vers Iceberg, et `OPTIMIZE … REWRITE DATA` et `VACUUM` pour la maintenance.

```sql
MERGE INTO lake.customers t
USING staging.customer_changes s ON t.customer_id = s.customer_id
WHEN MATCHED AND s.op = 'D' THEN DELETE
WHEN MATCHED THEN UPDATE SET email = s.email, country = s.country, updated_at = s.updated_at
WHEN NOT MATCHED THEN INSERT (customer_id, email, country, updated_at)
  VALUES (s.customer_id, s.email, s.country, s.updated_at);
```

#### Qu'est-ce que le partitionnement caché d'Iceberg ?

Des partitions définies comme des transformations de colonnes (`day(event_ts)`, `bucket(16, user_id)`, `truncate(10, sku)`) : les requêtes filtrent sur la colonne d'origine (`event_ts`) et Iceberg élague automatiquement les partitions ; les utilisateurs n'ont pas à connaître les colonnes de partition.

#### Comment fonctionne le voyage dans le temps d'Iceberg dans Athena ?

```sql
SELECT * FROM lake.customers FOR TIMESTAMP AS OF TIMESTAMP '2026-10-15 08:00:00 UTC';
SELECT * FROM lake.customers FOR VERSION AS OF 949530903748831860;
```

On peut aussi consulter des tables de métadonnées comme `"customers$snapshots"`, `"customers$history"`, `"customers$files"` et `"customers$partitions"`.

#### Que font `OPTIMIZE` et `VACUUM` sur les tables Iceberg ?

`OPTIMIZE table REWRITE DATA USING BIN_PACK` compacte les petits fichiers et fusionne les fichiers de suppression avec les fichiers de données. `VACUUM` expire les anciens snapshots et supprime les fichiers non référencés (selon les propriétés de rétention), libérant du stockage.

#### Comment fonctionnent les suppressions au niveau ligne d'Iceberg dans Athena ?

Athena écrit des fichiers de suppression positionnels (merge-on-read) qui marquent les lignes supprimées au lieu de réécrire les fichiers de données. Les lectures les fusionnent à la volée : les tables avec beaucoup de suppressions ont besoin d'`OPTIMIZE` réguliers pour rester rapides.

#### Peut-on faire évoluer le partitionnement d'une table Iceberg ?

Oui. On peut changer la spécification de partition (par exemple de mensuelle à quotidienne) sans réécrire les anciennes données ; les anciens fichiers gardent l'ancienne spécification, les nouvelles données utilisent la nouvelle, et les requêtes gèrent les deux.

#### Iceberg ou tables de style Hive dans Athena : comment choisir ?

Iceberg quand il faut des mises à jour, suppressions, upserts (CDC, effacements RGPD), de l'évolution de schéma, des écrivains concurrents ou du voyage dans le temps. Le Parquet de style Hive est plus simple pour des données immuables en ajout seul écrites par d'autres outils. Les nouvelles conceptions de lakehouse choisissent généralement Iceberg.

#### D'autres moteurs peuvent-ils utiliser les mêmes tables Iceberg ?

Oui. Spark sur EMR ou Glue, Trino, Flink, Snowflake, Databricks et d'autres peuvent lire et écrire les mêmes tables Iceberg via le Glue Data Catalog ou un catalogue REST Iceberg, ce qui évite l'enfermement dans un moteur.

#### Quelles propriétés de table comptent pour Iceberg dans Athena ?

`format` (parquet, orc, avro), `write_compression`, `optimize_rewrite_delete_file_threshold`, `vacuum_max_snapshot_age_seconds`, `vacuum_min_snapshots_to_keep` et `vacuum_max_metadata_files_to_keep`, qui contrôlent l'organisation des fichiers et la rétention.

#### Plusieurs écrivains peuvent-ils modifier une table Iceberg en même temps ?

Oui, avec une concurrence optimiste : chaque commit vérifie la version courante de la table, et les commits en conflit échouent et doivent être relancés. Évitez de nombreux écrivains concurrents mettant à jour les mêmes partitions.

#### Comment ajouter une colonne à une table Iceberg ?

`ALTER TABLE lake.customers ADD COLUMNS (segment string)`. Les fichiers existants ne sont pas réécrits ; les anciennes lignes renvoient `NULL` pour la nouvelle colonne.

#### Comment revenir en arrière sur une table Iceberg dans Athena ?

Lire la version précédente avec le voyage dans le temps et la réécrire (par exemple un `CTAS` depuis `FOR VERSION AS OF`), ou utiliser un moteur disposant de procédures de retour arrière (`rollback_to_snapshot` de Spark) sur la même table.

#### Que sont les S3 Tables ?

Des table buckets S3 qui stockent des tables Iceberg avec une maintenance intégrée (compaction, gestion des snapshots) et une intégration de catalogue, qu'Athena peut interroger et écrire comme les autres tables Iceberg.

### CTAS, INSERT et UNLOAD

#### Qu'est-ce que `CTAS` ?

`CREATE TABLE AS SELECT` : crée une nouvelle table à partir des résultats d'une requête, en écrivant dans S3 des fichiers au format, à la compression, au partitionnement et au bucketing choisis. On l'utilise pour convertir des formats, construire des agrégats et matérialiser des transformations.

#### Quelles sont les limites de `CTAS` et `INSERT INTO` ?

Une seule requête peut créer ou alimenter un nombre limité de partitions (100 par requête pour les tables Hive) : les gros backfills exigent plusieurs instructions ou des boucles par plages de partitions. Les tables Iceberg n'ont pas cette limite précise.

#### Que fait `INSERT INTO` sur une table de style Hive ?

Il ajoute de nouveaux fichiers à l'emplacement de la table (et enregistre les nouvelles partitions). Il ne modifie jamais les fichiers existants : le relancer duplique les données, sauf à supprimer d'abord les fichiers de la partition cible.

#### Comment rendre un ELT Athena idempotent ?

Pour les tables Hive, écrire la sortie de chaque exécution dans une partition et supprimer ou écraser cette partition avant de relancer (souvent en écrivant dans un nouvel emplacement puis en changeant l'emplacement de la partition). Pour les tables Iceberg, utiliser `MERGE`, ou `DELETE` plus `INSERT` dans la même logique, ou des schémas d'écrasement avec Iceberg.

#### Que fait `UNLOAD` ?

Il écrit les résultats d'une requête dans S3 au format choisi (Parquet, ORC, Avro, JSON, texte), avec partitionnement et compression optionnels, sans créer de table, ce qui est utile pour exporter vers d'autres systèmes.

```sql
UNLOAD (SELECT * FROM curated.app_events WHERE dt = '2026-10-15')
TO 's3://exports/app_events/dt=2026-10-15/'
WITH (format = 'PARQUET', compression = 'SNAPPY');
```

#### Comment planifier des requêtes Athena ?

Avec EventBridge Scheduler ou Step Functions appelant `StartQueryExecution`, l'`AthenaOperator` d'Airflow, dbt avec l'adaptateur dbt-athena, ou une fonction Lambda planifiée.

#### Peut-on utiliser dbt avec Athena ?

Oui, avec l'adaptateur dbt-athena : les modèles se matérialisent en vues, tables (`CTAS`), modèles incrémentaux (`insert_overwrite` par partition, `append` ou `merge` sur Iceberg) et tables Iceberg, avec Glue comme catalogue.

#### Que sont les instructions préparées et les requêtes paramétrées ?

Des instructions créées avec `PREPARE` (ou passées avec `ExecutionParameters`) contenant des marqueurs `?` remplis à l'exécution, ce qui évite l'injection SQL et permet aux applications de réutiliser le texte des requêtes.

```sql
PREPARE events_by_day FROM
SELECT event_type, count(*) FROM curated.app_events WHERE dt = ? GROUP BY 1;

EXECUTE events_by_day USING '2026-10-15';
```

#### Comment créer une copie vide du schéma d'une table ?

`CREATE TABLE nouvelle_t WITH (...) AS SELECT * FROM t WITH NO DATA`, qui crée la définition de la table sans écrire de lignes.

#### Comment maîtriser le nombre de fichiers produits par un `CTAS` ?

Avec `bucketed_by` et `bucket_count`, qui fixent le nombre de fichiers par partition, ou en réduisant le parallélisme de l'étape finale ; sinon Athena écrit autant de fichiers que les workers en produisent.

#### Un `CTAS` peut-il écrire dans un emplacement S3 existant ?

Non. L'`external_location` doit être vide, ce qui évite d'écraser des données par erreur. Supprimez l'emplacement ou utilisez-en un nouveau pour les relances.

#### Comment exporter les résultats d'une requête en un seul CSV ?

Lancer la requête et télécharger le fichier de résultats depuis l'emplacement de résultats (Athena écrit un CSV par requête), ou utiliser `UNLOAD` avec un format texte ; de très gros résultats peuvent être répartis sur plusieurs fichiers avec `UNLOAD`.

### Optimisation des performances

#### Quels sont les principaux leviers pour rendre les requêtes Athena plus rapides et moins chères ?

Formats en colonnes compressés, partitionnement selon les filtres courants (ou projection), fichiers de 128 Mo à 1 Go, sélection des seules colonnes utiles, filtres sur les colonnes de partition, tri ou bucketing selon les filtres courants, Iceberg avec compaction, statistiques de tables et réutilisation des résultats.

#### Comment voir combien de données une requête a lues ?

Dans la console après exécution, dans les statistiques de `GetQueryExecution` (`DataScannedInBytes`), dans les métriques CloudWatch du workgroup et dans la sortie d'`EXPLAIN ANALYZE` par stage.

#### Que montrent `EXPLAIN` et `EXPLAIN ANALYZE` ?

`EXPLAIN` montre le plan distribué ou logique sans exécuter la requête : lectures, filtres poussés, jointures et leur distribution. `EXPLAIN ANALYZE` exécute la requête et indique les lignes, les données lues et le temps réels par stage, ce qui montre où part le temps.

#### Dans quel ordre placer les tables dans une jointure ?

Le moteur v3 dispose d'un optimiseur basé sur les coûts qui peut réordonner les jointures quand des statistiques existent dans le catalogue Glue. Sans statistiques, placez la plus grande table en premier (à gauche) et les plus petites à droite, car le côté droit est construit en mémoire et distribué aux workers.

#### Quels types de distribution de jointure existent ?

Les jointures broadcast envoient la petite table de droite à tous les workers (rapide si elle est petite) ; les jointures partitionnées répartissent les deux côtés par hachage (nécessaire pour deux grandes tables). L'optimiseur choisit selon les statistiques.

#### Pourquoi un `ORDER BY` sans `LIMIT` nuit-il aux performances ?

Un tri global exige d'envoyer toutes les lignes à un seul worker pour l'ordonnancement final, ce qui est lent et peut échouer avec « exceeded resources ». Ajoutez un `LIMIT` (le top-N est efficace) ou ne triez que le nécessaire.

#### Qu'est-ce que « Query exhausted resources at this scale factor » ?

Une erreur quand une requête a besoin de plus de mémoire que disponible pour une opération (jointures énormes, `GROUP BY` sur de très nombreux groupes, `DISTINCT` sur beaucoup de colonnes, `ORDER BY` de tout, tableaux très volumineux). Solutions : filtrer plus tôt, réduire les colonnes, utiliser des fonctions approximatives, découper la requête, matérialiser des étapes intermédiaires avec `CTAS`, ou utiliser des réservations de capacité.

#### Quand utiliser des fonctions approximatives ?

`approx_distinct`, `approx_percentile` et `approx_most_frequent` renvoient des estimations à faible erreur en utilisant bien moins de mémoire que `count(DISTINCT)` ou les percentiles exacts, ce qui convient aux dashboards et à l'exploration.

#### Qu'est-ce que la réutilisation des résultats de requêtes ?

Une fonction où Athena renvoie les résultats d'une requête précédente si la même requête a été exécutée récemment (dans un âge maximal défini, jusqu'à 7 jours) et que les données n'ont pas changé (pour les tables compatibles), sans relire les données.

#### En quoi les statistiques de tables aident-elles Athena ?

Les statistiques de colonnes stockées dans le catalogue Glue (calculées par Glue) permettent à l'optimiseur basé sur les coûts de choisir l'ordre et la distribution des jointures, ce qui améliore les requêtes complexes sans changer le code.

#### Comment accélérer les recherches `LIKE` sur de grandes colonnes texte ?

Filtrer d'abord sur les partitions, n'utiliser `regexp_like` qu'en cas de besoin, et envisager d'extraire pendant l'ETL les champs recherchés dans des colonnes séparées, ou un service de recherche comme OpenSearch pour du plein texte.

#### Pourquoi le throttling S3 peut-il ralentir les requêtes Athena ?

S3 accepte des débits élevés par préfixe, mais des requêtes sur des millions de petits fichiers dans un même préfixe peuvent recevoir des erreurs `SlowDown` (503). Des fichiers moins nombreux et plus gros, répartis sur plusieurs préfixes (partitions), l'évitent.

#### Que sont les réservations de capacité ?

Une capacité de traitement dédiée achetée en DPU (pour une durée minimale, puis à la minute) et affectée à des workgroups. Les requêtes de ces workgroups s'exécutent sur la capacité réservée, facturée au DPU-heure plutôt qu'au To lu, avec un coût et une concurrence prévisibles.

#### Quand les réservations de capacité valent-elles la peine ?

Quand le volume de requêtes est élevé et régulier (dashboards BI intensifs, nombreux utilisateurs simultanés), quand il faut une concurrence garantie pour des charges critiques, ou quand le coût au To dépasse le prix de la capacité réservée.

#### Pourquoi `count(DISTINCT x)` sur une énorme table échoue-t-il ou est-il lent ?

Il faut garder toutes les valeurs distinctes en mémoire sur l'ensemble des workers. Utilisez `approx_distinct(x)` pour une estimation, ou pré-agrégez les comptes distincts par partition puis combinez-les.

#### Comment les fonctions de fenêtre affectent-elles les performances d'Athena ?

Les fonctions de fenêtre partitionnent et trient les données ; une fenêtre sur toute la table (sans `PARTITION BY`) impose un seul worker. Partitionnez toujours les fenêtres par une clé et filtrez les données d'abord.

#### Quel est l'effet de `UNION` par rapport à `UNION ALL` ?

`UNION` supprime les doublons, ce qui exige une étape d'agrégation supplémentaire ; `UNION ALL` se contente de concaténer. Utilisez `UNION ALL` quand les doublons sont impossibles ou acceptables.

#### Comment optimiser les requêtes sur une combinaison de dimensions très interrogée ?

Précalculer des agrégats dans une table de synthèse (`CTAS` ou `INSERT` planifié), partitionnée par date, et pointer les dashboards vers elle plutôt que vers la table brute.

#### Quel est l'effet de `LIMIT` sur le coût ?

Sur les tables de style Hive, un `LIMIT` sans filtre peut s'arrêter plus tôt mais lire tout de même de nombreux fichiers ; il ne garantit pas un faible coût. Les filtres de partition sont le moyen fiable de limiter la lecture.

#### Quel est l'impact du déséquilibre des données sur les jointures et agrégations Athena ?

Quelques clés concentrant la plupart des lignes surchargent des workers isolés et peuvent provoquer des erreurs « exhausted resources ». Filtrez les clés chaudes (souvent les nulls), traitez-les à part ou utilisez des agrégations approximatives.

### Workgroups, maîtrise des coûts et supervision

#### Comment limiter les coûts par équipe ?

Créer un workgroup par équipe ou application avec une limite de données par requête (qui annule les requêtes dépassant un seuil) et des limites globales par période qui déclenchent des alarmes, imposer les réglages du workgroup pour que les utilisateurs ne puissent pas les surcharger, et taguer les workgroups pour l'imputation des coûts.

#### Que signifie « override client-side settings » pour un workgroup ?

Une fois activé, l'emplacement des résultats, le chiffrement et les autres réglages du workgroup s'appliquent à toutes les requêtes, en ignorant ce que précisent les clients, ce qui impose la gouvernance.

#### Comment superviser l'usage d'Athena ?

Avec les métriques CloudWatch par workgroup (données lues, durée des requêtes, temps d'attente, requêtes en échec), l'historique des requêtes (`ListQueryExecutions`, console), CloudTrail pour les appels d'API, et des rapports de coûts par tags.

#### Combien de temps l'historique des requêtes est-il conservé ?

Athena conserve l'historique des requêtes 45 jours. Pour une rétention ou une analyse plus longue, exportez les détails d'exécution (par exemple via des événements EventBridge ou un job planifié appelant `GetQueryExecution`) vers S3.

#### Comment trouver les requêtes les plus coûteuses ?

Dans l'historique ou les données d'exécution exportées, trier par `DataScannedInBytes` ; puis vérifier si elles filtrent sur les partitions, lisent du CSV ou du JSON, ou sélectionnent trop de colonnes.

#### Comment éviter les requêtes incontrôlées ?

Avec des limites de données par requête dans les workgroups, des timeouts, de la formation sur les filtres de partition, des vues qui imposent un filtre de partition, et des réservations de capacité pour les charges prévisibles.

#### Comment les requêtes S3 influent-elles sur les coûts d'Athena ?

Le prix au To d'Athena n'inclut pas les requêtes GET et LIST de S3, facturées par S3. Des tables composées d'un nombre énorme de petits fichiers peuvent générer des coûts de requêtes importants en plus de la facture Athena.

#### Quelle différence entre une limite par requête et une limite de workgroup ?

Un contrôle par requête annule toute requête qui lit plus que le seuil. Les contrôles de workgroup mesurent le total lu sur une période et déclenchent des alarmes CloudWatch ou des notifications SNS, sans annuler de requêtes.

#### Comment imputer les coûts d'Athena aux équipes ?

Avec des workgroups séparés par équipe, tagués avec des tags d'imputation des coûts, en analysant les coûts dans Cost Explorer par tag ; avec des réservations de capacité, en affectant les workgroups aux réservations par équipe.

#### Comment suivre les échecs de requêtes ?

Avec les métriques CloudWatch de requêtes en échec par workgroup, les événements EventBridge « Athena Query State Change » routés vers des alertes, et l'historique des requêtes avec les messages d'erreur.

### Requêtes fédérées et connecteurs

#### Qu'est-ce qu'Athena Federated Query ?

Une fonction qui permet à Athena d'interroger des données hors de S3, comme DynamoDB, RDS et Aurora (MySQL, PostgreSQL), Redshift, DocumentDB, OpenSearch, CloudWatch Logs, Snowflake, BigQuery et bien d'autres, via des connecteurs de sources de données exécutés en fonctions AWS Lambda (ou en connexions Glue gérées).

#### Comment fonctionnent les connecteurs fédérés ?

La Lambda du connecteur reçoit une partie du plan de requête, lit les données de la source (en poussant filtres et projections quand c'est possible) et les renvoie à Athena au format Apache Arrow, qui les joint et les agrège ensuite avec d'autres données.

#### Quels sont les inconvénients des requêtes fédérées ?

Les performances dépendent de la source et de la Lambda (timeouts, mémoire, concurrence), les requêtes peuvent charger les bases opérationnelles, la poussée de prédicats est limitée pour certaines sources, et on paie Lambda en plus des données lues. Pour un usage fréquent et intensif, répliquez les données dans S3.

#### Comment joindre des données S3 à une table RDS ?

Enregistrer le connecteur RDS comme source de données (par exemple `rds_pg`), puis interroger `SELECT … FROM lake.orders o JOIN rds_pg.public.customers c ON o.customer_id = c.id`, en gardant le côté RDS petit grâce à des filtres.

#### Que sont les fonctions définies par l'utilisateur dans Athena ?

Des fonctions scalaires implémentées dans une fonction Lambda (Java) et appelées avec `USING EXTERNAL FUNCTION`, utilisées pour une logique absente du SQL, comme appeler un service interne ou un déchiffrement personnalisé.

#### Athena peut-il appeler des modèles de machine learning ?

Oui, avec `USING EXTERNAL FUNCTION … SAGEMAKER 'nom-endpoint'`, qui envoie des lignes à un endpoint SageMaker pour faire de l'inférence au sein d'une requête.

#### Comment déployer un connecteur fédéré ?

Depuis la console Athena (création d'une source de données), qui déploie la Lambda du connecteur depuis l'AWS Serverless Application Repository ou utilise des connexions Glue, avec un bucket de spill S3 pour les gros résultats et les bons réglages IAM et VPC.

#### À quoi sert le bucket de spill ?

Un emplacement S3 où le connecteur écrit les données qui dépassent les limites de taille de réponse de Lambda, qu'Athena lit ensuite. Il doit être chiffré et avoir une règle de cycle de vie.

#### Comment interroger DynamoDB avec Athena ?

Avec le connecteur DynamoDB, qui scanne ou interroge la table (en consommant de la capacité de lecture) ; pour de grosses requêtes analytiques, exportez la table vers S3 (export DynamoDB) et interrogez l'export.

#### Peut-on écrire son propre connecteur ?

Oui, avec l'Athena Query Federation SDK (Java), en implémentant les gestionnaires de métadonnées et d'enregistrements pour sa source, déployé en fonction Lambda.

### Sécurité et gouvernance

#### Comment contrôler l'accès à Athena ?

Par des politiques IAM sur les actions Athena et les workgroups, des droits S3 sur les données et les emplacements de résultats, des droits sur le Glue Data Catalog (bases, tables) et, pour un contrôle fin, des droits Lake Formation sur les bases, tables, colonnes, lignes et cellules.

#### Comment Lake Formation fonctionne-t-il avec Athena ?

Athena vérifie les droits Lake Formation de l'appelant et ne renvoie que les colonnes et lignes autorisées, en lisant S3 avec des identifiants temporaires fournis par Lake Formation : les utilisateurs n'ont pas besoin d'accès direct à S3 sur les données.

#### Comment chiffrer les données d'Athena ?

Les données dans S3 peuvent être chiffrées en SSE-S3, SSE-KMS ou KMS côté client ; Athena lit les données chiffrées de façon transparente avec les bons droits KMS. Les résultats peuvent être chiffrés (SSE-S3, SSE-KMS, CSE-KMS) par workgroup, et les données en transit utilisent TLS.

#### Comment restreindre les données S3 qu'un utilisateur peut interroger ?

Accorder l'accès aux tables via Lake Formation (sans droits S3 directs), ou, avec IAM, limiter l'accès S3 à des préfixes précis et l'accès Glue à des bases et tables précises.

#### Comment interroger des données d'un autre compte AWS ?

Via le partage inter-comptes de Lake Formation (resource links), l'accès inter-comptes au catalogue Glue enregistré comme source de données, ou des politiques de bucket donnant au rôle requérant l'accès aux données et à leur clé KMS.

#### Comment auditer l'usage d'Athena ?

CloudTrail enregistre les appels d'API (qui a lancé quelle requête, avec son texte), Lake Formation journalise l'accès aux données, et les journaux d'accès serveur S3 ou les événements de données CloudTrail enregistrent les lectures d'objets.

#### Comment utiliser Athena depuis un réseau privé ?

Via des endpoints VPC d'interface pour Athena (et pour Glue, S3 et KMS selon les besoins), pour que le trafic ne passe pas par Internet ; des politiques d'endpoint peuvent restreindre l'usage.

#### Qu'est-ce qu'un data filter Lake Formation ?

Une définition de sécurité au niveau ligne et cellule pour une table (une expression de filtre de lignes plus des colonnes incluses ou exclues) accordée à des principals ; Athena l'applique à la requête.

#### Comment donner à un outil BI un accès sécurisé à Athena ?

Créer un rôle ou utilisateur IAM dédié (de préférence fédéré via IAM Identity Center ou OAuth pour le pilote), limité à un workgroup, aux tables nécessaires via Lake Formation et à l'emplacement de résultats, et se connecter via le pilote JDBC/ODBC.

#### Comment masquer des colonnes sensibles dans Athena ?

Les exclure via les droits de colonnes Lake Formation, fournir des vues qui les hachent ou les masquent, ou stocker des copies masquées dans une table curée séparée pour un accès large.

### Spark dans Athena et notebooks

#### Qu'est-ce qu'Amazon Athena for Apache Spark ?

Une offre Spark serverless dans Athena qui permet d'exécuter du PySpark et du Spark SQL dans des notebooks ou via des API, avec un démarrage rapide et une facturation au DPU-heure, pour les charges qui demandent plus que du SQL.

#### Quand utiliser Athena Spark plutôt qu'Athena SQL ?

Pour des transformations complexes en Python, la préparation de données pour le machine learning, l'exploration itérative avec des DataFrames ou une logique malcommode en SQL ; le SQL reste plus simple et moins cher pour l'essentiel de l'analytique.

#### Comment les sessions Athena Spark sont-elles facturées ?

Au DPU-heure du calcul de la session, avec un dimensionnement automatique des executors et des délais d'inactivité qui terminent la session.

#### Comment Athena Spark accède-t-il au Data Catalog ?

Les sessions Spark d'Athena utilisent par défaut le Glue Data Catalog : on peut lire et écrire les tables du catalogue (y compris Iceberg) en Spark SQL ou en DataFrames.

#### Quels langages les notebooks Athena prennent-ils en charge ?

PySpark et Spark SQL (avec des commandes magiques), avec des bibliothèques Python courantes disponibles et la possibilité d'en ajouter d'autres à la session.

### Dépannage

#### Une requête renvoie zéro ligne alors que les fichiers existent. Que vérifiez-vous ?

Si les partitions sont enregistrées (ou si la projection est correctement configurée), si le `LOCATION` et le modèle d'emplacement correspondent aux vrais chemins, si le SerDe et les colonnes correspondent au format, et si les fichiers sont dans des sous-dossiers que la table n'inclut pas.

#### Que signifie `HIVE_PARTITION_SCHEMA_MISMATCH` ?

Le schéma d'une partition dans le catalogue diffère de celui de la table (types ou colonnes). Faites hériter aux partitions le schéma de la table (réglage du crawler ou recréation des partitions) et stabilisez la source.

#### Qu'indique généralement `HIVE_CURSOR_ERROR` ?

Un problème de lecture de fichier : fichiers corrompus ou tronqués, format différent de la définition de la table, fichier compressé illisible, ou problèmes de droits ou de KMS sur certains objets.

#### Que signifie `HIVE_BAD_DATA` ?

Une valeur ne peut pas être lue avec le type déclaré, par exemple du texte dans une colonne numérique, un enregistrement JSON mal formé, ou un type Parquet discordant. Corrigez les données, les types de la table, ou utilisez `TRY_CAST` sur des colonnes texte.

#### Pourquoi obtient-on `Access Denied` sur une requête ?

Il manque des droits sur les données S3, l'emplacement des résultats, la clé KMS, les objets du catalogue Glue, les droits Lake Formation ou le workgroup. Le message d'erreur nomme généralement la ressource.

#### Pourquoi une requête sur des horodatages renvoie-t-elle des résultats faux ?

Des horodatages stockés sous forme de chaînes dans des formats différents, une confusion de fuseaux horaires (les timestamps sans fuseau sont souvent interprétés en UTC), ou des encodages de timestamps Parquet différents selon les écrivains. Analysez explicitement avec `from_iso8601_timestamp` ou `parse_datetime` et convertissez les fuseaux avec `AT TIME ZONE`.

#### Une requête est lente mais lit peu de données. Quelle peut en être la cause ?

Le temps de planification sur des tables très partitionnées (utilisez la projection ou les index de partition), de nombreux fichiers minuscules (surcharge par fichier), une source fédérée, l'attente due aux limites de concurrence, ou une opération coûteuse comme une grosse jointure ou un tri global.

#### Les résultats contiennent des doublons après la relance d'un pipeline. Pourquoi ?

Le pipeline a utilisé `INSERT INTO` sur une table Hive sans supprimer la sortie précédente, ou des fichiers ont été écrits deux fois au même emplacement. Rendez les écritures idempotentes (écraser les partitions, `MERGE` Iceberg) et dédupliquez les partitions concernées.

#### Pourquoi `MSCK REPAIR TABLE` n'ajoute-t-il aucune partition ?

Les dossiers ne sont pas de style Hive (`cle=valeur`), les noms de clés ne correspondent pas aux colonnes de partition (la casse compte), l'emplacement est faux, ou la projection de partitions est activée sur la table.

#### Pourquoi des nombres apparaissent-ils en `NULL` depuis une table CSV ?

Les valeurs contiennent des caractères non analysables (séparateurs de milliers, symboles monétaires, guillemets avec `LazySimpleSerDe`, chaînes vides), ou les colonnes sont décalées parce qu'un champ contient le délimiteur. Utilisez `OpenCSVSerDe`, nettoyez les données, ou lisez en texte et appliquez `TRY_CAST`.

#### Pourquoi obtient-on « Query timeout » ?

La requête a dépassé le timeout du workgroup : trop de données lues, une jointure ou un tri lourd, ou une source fédérée lente. Optimisez la requête ou l'organisation des données, matérialisez des étapes intermédiaires ou relevez le quota de timeout.

#### Pourquoi des erreurs « too many open files » ou `SlowDown` S3 ?

Des tables composées d'un nombre énorme de petits fichiers provoquent énormément de requêtes S3 simultanées. Compactez les fichiers et répartissez-les sur plusieurs partitions.

#### Pourquoi une requête sur Iceberg ralentit-elle avec le temps ?

De nombreux petits fichiers et fichiers de suppression s'accumulent avec des écritures fréquentes et des modifications au niveau ligne. Planifiez `OPTIMIZE` et `VACUUM` (ou utilisez la compaction automatique du catalogue Glue ou de S3 Tables).

### Fonctions SQL et modèles de requêtes

#### Comment manipuler les dates et heures dans Athena ?

Avec des fonctions comme `current_date`, `date_add('day', -1, current_date)`, `date_diff('day', a, b)`, `date_trunc('month', ts)`, `date_format(ts, '%Y-%m-%d')`, `from_iso8601_timestamp(s)`, `parse_datetime(s, 'yyyy-MM-dd HH:mm')` et `ts AT TIME ZONE 'Europe/Paris'`.

#### Comment convertir des types en toute sécurité ?

`TRY_CAST(x AS integer)` renvoie `NULL` au lieu d'échouer sur une valeur invalide, et `try()` enveloppe des expressions susceptibles d'échouer. Utilisez-les sur des données texte brutes.

#### Comment dédupliquer des lignes dans Athena ?

Avec `row_number()` par clé ordonné par un horodatage, en gardant la première ligne par clé, dans une sous-requête ou une CTE, car Athena ne prend pas en charge `QUALIFY`.

#### Comment pivoter des données dans Athena ?

Avec une agrégation conditionnelle, faute de mot-clé `PIVOT` : `sum(CASE WHEN month = 1 THEN amount END) AS janv`, ou `map_agg` pour construire une map clé-valeur.

#### Quelles fonctions de tableaux et de maps sont utiles ?

`cardinality`, `contains`, `element_at`, `array_join`, `array_agg`, `filter`, `transform`, `reduce`, `map_keys`, `map_values` et `map_agg`, qui permettent de travailler sur des données imbriquées sans les déplier.

#### Comment calculer un cumul ou une moyenne mobile ?

Avec des fonctions de fenêtre : `sum(amount) OVER (PARTITION BY customer ORDER BY dt ROWS UNBOUNDED PRECEDING)` pour les cumuls et `avg(amount) OVER (ORDER BY dt ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)` pour une moyenne mobile sur 7 lignes.

#### Comment générer une série de dates dans Athena ?

Avec `sequence` et `UNNEST` : `SELECT d FROM UNNEST(sequence(date '2026-01-01', date '2026-12-31', interval '1' day)) AS t(d)`, utile pour combler les trous des séries temporelles.

#### Comment obtenir les N premières lignes par groupe ?

Utiliser `row_number()` ou `rank()` par groupe, ordonné selon la mesure, dans une sous-requête, et filtrer sur le rang dans la requête externe ; `max_by(x, y)` donne la valeur de `x` au maximum de `y` par groupe.

#### À quoi servent `max_by` et `min_by` ?

À renvoyer la valeur d'une colonne sur la ligne où une autre colonne est maximale ou minimale, par exemple le dernier statut de chaque commande : `max_by(status, updated_at)`, sans fonction de fenêtre.

#### Comment faire des requêtes géospatiales dans Athena ?

Avec des fonctions géospatiales comme `ST_Point`, `ST_Contains`, `ST_Distance`, `ST_Within`, `ST_GeometryFromText` et `great_circle_distance`, par exemple pour compter des événements à l'intérieur de polygones.

#### Comment hacher des valeurs pour les pseudonymiser ?

Avec `to_hex(sha256(to_utf8(email)))` (de préférence avec un sel secret ou un HMAC via `hmac_sha256`), ce qui produit des pseudonymes stables qu'on peut encore joindre.

#### Comment écrire une logique SQL réutilisable dans Athena ?

Avec des vues pour la logique partagée, des CTE (`WITH`) pour la lisibilité au sein d'une requête, et des macros dbt quand on utilise dbt-athena.

#### Comment comparer deux tables pour trouver les différences ?

Avec `EXCEPT` dans les deux sens (`SELECT * FROM a EXCEPT SELECT * FROM b`) pour les différences de lignes, ou une jointure externe complète sur la clé en comparant les colonnes, utile pour valider des migrations.

#### Comment échantillonner des données dans Athena ?

`TABLESAMPLE BERNOULLI (1)` lit chaque ligne avec 1 % de probabilité (mais lit toutes les données), et `TABLESAMPLE SYSTEM (1)` échantillonne au niveau du fichier ou du split, ce qui peut réduire les données lues.

#### Comment gérer les valeurs `NULL` dans les agrégations et comparaisons ?

Les agrégations ignorent les `NULL` (sauf `count(*)`) ; les comparaisons avec `NULL` renvoient `NULL` : utilisez `IS NULL`, `coalesce`, `IS DISTINCT FROM` pour comparer en tenant compte des nulls, et méfiez-vous de `NOT IN` sur des colonnes qui contiennent des nulls.

### Mises en situation

#### Concevez une solution d'analyse de journaux peu coûteuse avec Athena.

Livrer les journaux dans S3 avec Firehose (bufferisés, convertis en Parquet, partitionnés par date), définir une table avec projection de partitions par date, créer des vues pour les questions courantes, configurer un workgroup avec des limites de données, et donner l'accès aux analystes via Lake Formation. Ajouter des règles de cycle de vie pour déplacer les anciens journaux vers des classes de stockage moins chères.

#### Votre facture Athena a doublé. Comment enquêtez-vous ?

Je vérifie les données lues par workgroup dans CloudWatch, je trouve les requêtes les plus lourdes en octets dans l'historique, et je cherche de nouveaux dashboards lançant des requêtes non filtrées, des `SELECT *` sur des tables larges, des tables en CSV ou JSON, et des filtres de partition devenus inopérants (par exemple une fonction sur la colonne de partition). Puis je corrige formats et filtres et j'ajoute des limites par requête.

#### Les analystes doivent supprimer les données de certains clients au titre du RGPD. Comment le permettre dans Athena ?

Stocker les données dans des tables Iceberg, lancer `DELETE FROM … WHERE customer_id = …` sur les tables concernées, puis `OPTIMIZE` et `VACUUM` pour supprimer physiquement les anciens fichiers après la période de rétention des snapshots. Avec des tables Hive, il faudrait réécrire des partitions entières.

#### Comment construire un petit pipeline ELT uniquement avec Athena ?

Des tables raw sur les fichiers d'atterrissage, des `CTAS` ou `INSERT INTO` (ou des modèles dbt-athena) pour construire des tables nettoyées en Iceberg ou Parquet, `MERGE` pour les upserts, des contrôles de qualité sous forme de requêtes SQL qui font échouer le pipeline quand elles renvoient des lignes, et Step Functions ou Airflow pour planifier et ordonner les instructions.

#### Un dashboard QuickSight sur Athena est lent et coûteux. Que changez-vous ?

Pré-agréger dans une table de synthèse rafraîchie selon un planning, utiliser SPICE de QuickSight pour mettre les données en cache, s'assurer que le dashboard applique des filtres de partition, convertir les tables sources en Parquet ou Iceberg avec compaction, et envisager des réservations de capacité pour une concurrence prévisible.

#### Une table reçoit 2 millions de petits fichiers JSON par jour. Que recommandez-vous ?

Corriger le producteur pour regrouper les enregistrements (buffering Firehose, écritures plus grosses), ajouter une étape de compaction qui convertit chaque journée en quelques fichiers Parquet (job Glue ou `CTAS`), et interroger la table compactée ; ne garder le JSON brut qu'en archive.

#### Comment interroger le dernier état d'une table qui reçoit des enregistrements CDC ?

Soit maintenir une table Iceberg avec un `MERGE` appliquant les changements (le plus propre), soit, sur une table de changements en ajout seul, utiliser `ROW_NUMBER()` par clé ordonné par horodatage de changement et garder la dernière ligne non supprimée dans une vue.

```sql
SELECT * FROM (
  SELECT *, row_number() OVER (PARTITION BY customer_id ORDER BY change_ts DESC) AS rn
  FROM raw.customer_changes
) WHERE rn = 1 AND op <> 'D';
```

#### Comment expliquer Athena à un interlocuteur métier ?

Il permet à l'équipe de poser des questions en SQL directement sur les fichiers que l'entreprise stocke déjà dans S3, sans monter ni payer de serveurs, en ne payant que les données lues par chaque question.

#### Comment migrer des rapports d'un SQL Server on-premise vers Athena ?

Exporter les tables vers S3 en Parquet (DMS ou exports), définir des tables Glue ou Iceberg, traduire le T-SQL en SQL Trino (fonctions, gestion des dates, `TOP` vers `LIMIT`, pas de `PIVOT`), recréer les vues, valider les résultats en comparant des agrégats, et connecter l'outil BI via le pilote.

#### Une équipe a besoin d'un accès SQL ad hoc à un data lake de 50 To avec un budget serré. Que mettez-vous en place ?

Des droits Lake Formation par domaine, un workgroup par équipe avec limites par requête, des tables Parquet ou Iceberg partitionnées par date, des vues qui imposent un filtre de partition, la réutilisation des résultats, une documentation des tables et des rapports mensuels des octets lus par équipe.

#### Comment construire des dashboards quasi temps réel sur Athena ?

Envoyer les événements avec Firehose vers S3 en Parquet avec des buffers courts, partitionner par date et heure avec projection, construire toutes les quelques minutes de petites tables agrégées avec un `INSERT INTO` planifié ou un `MERGE` dans Iceberg, et pointer les dashboards vers ces agrégats ; pour une latence sous la minute, utiliser un autre stockage comme OpenSearch ou une base de données de streaming.
