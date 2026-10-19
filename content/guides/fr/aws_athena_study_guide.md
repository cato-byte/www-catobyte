## Fiche d'étude Amazon Athena

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude Amazon Athena : environ 200 questions](../../images/aws_athena_study_guide_title_img.png)

Environ 200 questions d'entretien sur Amazon Athena : le fonctionnement du SQL serverless sur S3, les tables et les SerDe, les partitions et la projection de partitions, les formats de fichiers, les tables Iceberg, `CTAS` et `UNLOAD`, les workgroups et la maîtrise des coûts, l'optimisation des performances, les requêtes fédérées, la sécurité et le dépannage. Les réponses décrivent le service tel qu'il est en 2026.

La fiche suit un parcours d'apprentissage en cinq étapes. Chaque section est découpée en unités courtes : objectifs d'apprentissage, explication du concept et exemple commenté, puis questions (d'abord de mémorisation, ensuite d'application), un exercice pratique et les points à retenir. Pour **apprendre**, lisez chaque unité du début à la fin. Pour **réviser**, passez en mode révision ou utilisez « Aller aux questions », marquez les réponses à revoir et essayez une révision mixte entre les sections.

<!-- QA -->
<!-- stage: Fondamentaux -->

### Fondamentaux

<!-- unit: Du SQL serverless sur S3 -->

<!-- goals -->

- Expliquer ce qu'est Athena, quel moteur il utilise et à quoi il sert.
- Décrire le schema on read et ce que le serverless vous épargne.

<!-- concept -->

La plupart des entreprises gardent déjà leurs données brutes en fichiers dans S3. Athena permet de les interroger en SQL sans les charger ailleurs. Deux idées le rendent possible. Le schema on read : une table n'est qu'une description posée sur des fichiers, appliquée à la requête, donc n'importe quel outil peut les écrire. Le serverless : AWS opère un moteur partagé basé sur Trino, sans cluster à dimensionner ni à laisser inactif.

La contrepartie : le moteur n'est jamais plus efficace que les fichiers qu'on lui donne.

<!-- example -->

```sql
-- files written by Firehose; no load step, just a table definition
SELECT status, count(*) AS requests
FROM logs.alb_access
WHERE day = '2026-10-17'
GROUP BY status
ORDER BY requests DESC;
```

#### Qu'est-ce qu'Amazon Athena ?

Un service de requêtes interactives serverless qui permet d'analyser des données directement dans Amazon S3 (et d'autres sources via des connecteurs) en SQL standard. Aucune infrastructure à gérer : on définit des tables sur ses données, on lance des requêtes et on paie les données lues ou une capacité réservée.

#### Quel moteur Athena utilise-t-il ?

La version 3 du moteur SQL d'Athena repose sur Trino (anciennement PrestoSQL) avec des améliorations propres à AWS, et le DDL utilise une syntaxe compatible Hive. Athena propose aussi Apache Spark via les notebooks Athena pour les charges PySpark.

#### Quels sont les cas d'usage typiques d'Athena ?

L'analyse ad hoc de data lakes, l'interrogation de journaux (CloudTrail, VPC Flow Logs, ALB, CloudFront, journaux d'accès S3), un ELT léger avec `CTAS` et `INSERT INTO`, l'alimentation d'outils BI comme QuickSight, l'exploration de données avant de construire des pipelines et l'interrogation de tables Iceberg dans un lakehouse.

#### Que signifie « serverless » pour Athena ?

Il n'y a pas de clusters à dimensionner, démarrer ou patcher : AWS exploite un moteur de requêtes partagé et multi-locataire, alloue les ressources par requête, et vous payez à la requête (ou à la capacité réservée). Rien ne tourne quand vous n'interrogez pas.

#### Que signifie « schéma à la lecture » (schema on read) dans Athena ?

Le schéma s'applique quand les données sont lues, pas quand elles sont écrites : n'importe quel outil peut écrire les fichiers S3, et la définition de table indique à Athena comment les interpréter à la requête. C'est souple, mais les fichiers défectueux n'apparaissent qu'à l'interrogation, sous forme d'erreurs ou de `NULL`.

#### Quels services AWS alimentent couramment Athena en données ?

Kinesis Data Firehose (flux vers S3), AWS Glue (ETL et catalogue), AWS DMS (réplication de bases vers S3), les services AWS qui écrivent leurs journaux dans S3, S3 Inventory et les applications qui écrivent directement des fichiers.

#### Comment expliquer Athena à un interlocuteur métier ?

Il permet à l'équipe de poser des questions en SQL directement sur les fichiers que l'entreprise stocke déjà dans S3, sans monter ni payer de serveurs, en ne payant que les données lues par chaque question.

<!-- challenge -->

Une équipe demande si Athena peut remplacer son job nocturne qui charge des logs S3 dans une base de données pour quelques requêtes hebdomadaires. Que répondez-vous ?

<!-- solution -->

Probablement oui : définissez une table sur les logs et interrogez-les sur place, en ne payant que pendant les requêtes. Convertissez les logs en Parquet partitionné si les requêtes hebdomadaires scannent beaucoup, pour garder un coût bas.

<!-- takeaways -->

- Athena interroge directement des fichiers S3 en SQL.
- Schema on read : les tables décrivent des fichiers ; rien n'est chargé.
- Serverless veut dire sans cluster, mais l'organisation des fichiers compte.

<!-- unit: Tarification et exécution des requêtes -->

<!-- goals -->

- Expliquer la facturation d'Athena et pourquoi le format décide du coût.
- Suivre une requête de sa soumission aux résultats et connaître les limites.

<!-- concept -->

Le prix par défaut d'Athena est à l'octet scanné, ce qui lie le coût à la part de chaque fichier qu'une requête doit lire. Les formats qui permettent de sauter colonnes et groupes de lignes réduisent donc coût et temps. Chaque requête suit le même chemin : file d'attente, planification avec les métadonnées du catalogue, scan parallèle et résultats écrits dans S3.

Des quotas de concurrence et un timeout bornent ce chemin : des requêtes très grosses ou très nombreuses demandent une autre conception, pas seulement de la patience.

<!-- example -->

| Les mêmes 100 Go d'événements | Octets scannés pour 3 colonnes | Coût approx. à 5 USD/To |
|---|---|---|
| CSV non compressé | 100 Go | 0,50 USD |
| Parquet + Snappy | ~4 Go | 0,02 USD |

#### Comment Athena est-il facturé ?

Par défaut, au téraoctet lu (environ 5 USD par To dans de nombreuses régions), avec un minimum de 10 Mo par requête, arrondi au mégaoctet. Les instructions DDL et les requêtes en échec ne sont pas facturées. Les réservations de capacité proposent à la place un prix fixe par DPU-heure. Le stockage et les requêtes S3 ainsi que l'usage du Glue Data Catalog sont facturés à part.

#### Pourquoi le format des données compte-t-il autant pour le coût d'Athena ?

Parce qu'on paie à l'octet lu. Les formats en colonnes et compressés (Parquet, ORC) permettent à Athena de ne lire que les colonnes nécessaires et de sauter des blocs grâce aux statistiques, ce qui réduit souvent les données lues de 90 % ou plus par rapport à du CSV ou du JSON non compressé.

#### Où vont les résultats des requêtes ?

Dans un emplacement de résultats S3 (défini par workgroup ou par requête) sous forme de fichier CSV accompagné d'un fichier de métadonnées, ou dans le stockage de résultats géré qu'Athena conserve pour une durée limitée. Les résultats peuvent être chiffrés et devraient avoir une règle de cycle de vie pour expirer les anciens fichiers.

#### Quel est le cycle de vie d'une requête dans Athena ?

La requête est soumise (`QUEUED`), planifiée à l'aide des métadonnées du catalogue et de l'élagage des partitions, exécutée en parallèle sur le calcul géré d'Athena en lisant S3 (`RUNNING`), puis se termine en `SUCCEEDED`, `FAILED` ou `CANCELLED`, les résultats étant écrits à l'emplacement prévu.

#### Quelles limites d'Athena faut-il connaître ?

Des quotas par compte sur les requêtes DML et DDL actives simultanément, un timeout de requête (30 minutes par défaut pour le DML, ajustable), la longueur du texte de requête, le nombre de partitions qu'une seule requête peut ajouter, et les débits de requêtes S3 par préfixe qui peuvent brider les lectures très parallèles.

<!-- challenge -->

Un tableau de bord lance une requête par minute sur une table CSV de 2 To. Estimez le coût mensuel de scan et citez la première correction.

<!-- solution -->

Environ 2 To × 43 200 requêtes ≈ 86 Po scannés, soit près de 430 000 USD par mois. Convertir en Parquet partitionné et filtrer par date pour que chaque requête scanne des mégaoctets ; puis mettre les résultats en cache ou pré-agréger.

<!-- takeaways -->

- On paie à l'octet scanné : l'organisation, c'est le coût.
- Les requêtes passent par file, planification, scan parallèle et écriture dans S3.
- Quotas et timeouts bornent ce qu'une requête peut faire.

<!-- unit: Athena parmi les services analytiques AWS -->

<!-- goals -->

- Comparer Athena à Redshift, Redshift Spectrum et EMR.
- Choisir le bon moteur pour une charge.

<!-- concept -->

AWS offre plusieurs façons d'exécuter du SQL sur le même lake, qui diffèrent par le propriétaire du calcul et la régularité de la charge. Athena convient aux requêtes intermittentes, ad hoc et exploratoires car on ne paie qu'en interrogeant. Un entrepôt convient à une BI régulière et très concurrente, son calcul étant toujours prêt et optimisé. Des clusters gérés soi-même conviennent aux équipes qui veulent le contrôle total des moteurs et des réglages.

Beaucoup d'architectures en utilisent plusieurs sur un catalogue partagé.

<!-- example -->

| Charge | Bon choix |
|---|---|
| Des analystes explorent des logs quelques fois par jour | Athena |
| 300 utilisateurs de tableaux de bord toute la journée, sub-seconde | Redshift |
| Joindre des tables d'entrepôt à l'historique dans S3 | Redshift Spectrum |
| Jobs Spark maison aux réglages fins | EMR |

#### Comment Athena se compare-t-il à Amazon Redshift ?

Athena est serverless et interroge les données sur place dans S3, idéal pour les charges ad hoc, intermittentes ou exploratoires, avec un paiement à la requête. Redshift est un entrepôt (provisionné ou serverless) optimisé pour une analytique complexe, fréquente et très concurrente sur des données chargées dans son stockage géré, avec des fonctions comme les vues matérialisées et la gestion des charges. Beaucoup d'architectures utilisent les deux.

#### Comment Athena se compare-t-il à Redshift Spectrum ?

Les deux interrogent des données S3 via le Glue Data Catalog. Spectrum s'exécute depuis un cluster Redshift et permet de joindre les données S3 aux tables Redshift ; Athena est autonome et serverless. Spectrum est utile quand l'entrepôt existe déjà.

#### Comment Athena se compare-t-il à Trino ou Spark sur EMR ?

Athena supprime la gestion de clusters et facture à la requête ou à la capacité, mais offre moins de contrôle sur la configuration et les ressources. EMR convient aux charges très volumineuses et régulières, aux configurations sur mesure ou aux outils au-delà du SQL.

<!-- challenge -->

Une entreprise utilise Athena pour tout, dont un outil de BI à 200 utilisateurs simultanés, et bute chaque jour sur les limites de concurrence. Que proposez-vous ?

<!-- solution -->

Déplacer la charge BI régulière vers un entrepôt (Redshift) ou des réservations de capacité Athena, et garder Athena à la demande pour l'ad hoc et l'exploration. Des tables pré-agrégées aident dans les deux cas.

<!-- takeaways -->

- Athena convient aux requêtes intermittentes et ad hoc sur S3.
- Les entrepôts conviennent à la BI régulière et très concurrente.
- EMR convient aux équipes qui veulent le contrôle total.

<!-- unit: Travailler avec Athena -->

<!-- goals -->

- Utiliser workgroups, interfaces et requêtes enregistrées au quotidien.
- Savoir où vivent les métadonnées et ce qu'Athena peut écrire.

<!-- concept -->

Athena ne stocke presque rien lui-même. Les définitions de tables vivent dans le Glue Data Catalog, données et résultats dans S3, la configuration dans les workgroups. Cela explique son comportement : supprimer une table laisse les fichiers, deux moteurs peuvent partager un catalogue et un workgroup décide où vont les résultats et qui paie.

On peut écrire, mais sur les tables de style Hive cela ne fait qu'ajouter des fichiers. Transactions, mises à jour et suppressions exigent un format de table comme Iceberg.

<!-- example -->

```bash
aws athena start-query-execution \
  --work-group analytics \
  --query-string "SELECT count(*) FROM logs.alb_access WHERE day = '2026-10-17'"
```

#### Qu'est-ce qu'un workgroup ?

Un moyen de séparer utilisateurs, équipes ou applications : chaque workgroup a son emplacement de résultats, ses réglages de chiffrement, sa version de moteur, ses limites d'usage de données, ses métriques CloudWatch et son historique de requêtes, et IAM peut contrôler qui utilise quel workgroup.

#### Quelles sont les principales interfaces d'Athena ?

L'éditeur de requêtes de la console, la CLI et les SDK AWS (`StartQueryExecution`, `GetQueryExecution`, `GetQueryResults`), les pilotes JDBC et ODBC pour les outils BI et SQL, les notebooks Athena pour Spark, et les intégrations avec QuickSight, Glue, Step Functions et Airflow.

#### Que sont les requêtes enregistrées de l'éditeur Athena ?

Des requêtes nommées enregistrées par workgroup que les utilisateurs peuvent réutiliser et partager, utiles pour les analyses récurrentes, même si le contrôle de version dans Git est préférable pour le SQL de production.

#### Que sont les versions du moteur Athena, et comment sont-elles mises à jour ?

Athena fait évoluer son moteur par versions (la v3 est l'actuelle) ; les workgroups peuvent choisir les mises à jour automatiques ou une version précise. Une mise à jour peut changer le comportement de fonctions ou la gestion des types : testez les requêtes critiques avant de basculer.

#### Où Athena stocke-t-il les définitions de tables ?

Dans l'AWS Glue Data Catalog (par défaut), dans un Hive metastore externe, ou dans d'autres catalogues enregistrés comme sources de données (connecteurs fédérés, Redshift, catalogues S3 Tables).

#### Athena est-il ACID ?

Pour les tables de style Hive, non : les requêtes lisent les fichiers présents, et les écritures ajoutent des fichiers sans transaction. Pour les tables Apache Iceberg, oui : Athena prend en charge `INSERT`, `UPDATE`, `DELETE` et `MERGE` ACID avec isolation par snapshots et voyage dans le temps.

#### Athena peut-il écrire des données ?

Oui : `CTAS`, `INSERT INTO`, `UNLOAD`, et le DML complet (`UPDATE`, `DELETE`, `MERGE`) sur les tables Iceberg. Sur les tables de style Hive, il ne peut qu'ajouter de nouveaux fichiers.

<!-- challenge -->

Un utilisateur supprime une table par erreur et panique. Qu'est-il arrivé aux données, et comment restaurer la table ?

<!-- solution -->

Les données sont toujours dans S3, car les tables Athena sont externes. Recréez la table à partir de son DDL (par exemple depuis le contrôle de version ou `SHOW CREATE TABLE` dans un autre environnement) et réajoutez les partitions.

<!-- takeaways -->

- Métadonnées dans Glue, données et résultats dans S3, configuration dans les workgroups.
- Supprimer une table externe laisse les fichiers.
- Les écritures ACID exigent des tables Iceberg.

### Tables, DDL et SerDe

<!-- unit: Tables externes et catalogue -->

<!-- goals -->

- Créer et inspecter des tables externes et des vues.
- Choisir les types de données et modifier les colonnes sans risque.

<!-- concept -->

Une table Athena est un contrat entre un emplacement S3 et un schéma. La créer n'écrit que des métadonnées ; les fichiers peuvent déjà exister ou arriver plus tard. Cette séparation rend les tables faciles à créer et recréer, et fait du DDL votre outil principal pour corriger les décalages.

Les vues ajoutent une couche de logique sans stocker de données, utiles pour des définitions partagées, mais chaque requête paie le scan complet des tables sous-jacentes.

<!-- example -->

```sql
CREATE EXTERNAL TABLE sales.orders (
  order_id bigint, customer_id bigint, amount decimal(12,2), created_at timestamp
)
PARTITIONED BY (dt string)
STORED AS PARQUET
LOCATION 's3://lake/sales/orders/';
```

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

#### Que fait `SHOW CREATE TABLE` ?

Il affiche le DDL d'une table, pratique pour copier des définitions entre environnements ou vérifier le SerDe et les propriétés.

#### Qu'est-ce qu'une vue dans Athena ?

Une requête enregistrée (`CREATE VIEW`) dans le catalogue, qu'on interroge comme une table. Elle ne stocke pas de données : chaque requête lit les tables sous-jacentes et est facturée en conséquence.

#### Quels types de données Athena prend-il en charge ?

`boolean`, `tinyint`, `smallint`, `int`, `bigint`, `double`, `float`, `decimal(p,s)`, `char`, `varchar`, `string`, `binary`, `date`, `timestamp`, et les types complexes `array`, `map` et `struct`.

#### Comment modifier les colonnes d'une table ?

Avec `ALTER TABLE … ADD COLUMNS`, `REPLACE COLUMNS` ou `CHANGE COLUMN` (le comportement dépend du format), ou en recréant la table. Pour Iceberg, `ALTER TABLE … ADD COLUMNS`, `DROP COLUMN` et `RENAME COLUMN` sont des opérations sûres sur les métadonnées.

<!-- challenge -->

Les montants sont stockés en `double` et la finance voit des erreurs d'arrondi dans les totaux. Que changez-vous ?

<!-- solution -->

Stocker l'argent en `decimal(p,s)` plutôt qu'en `double`. Recréer la table (ou écrire une nouvelle version Parquet par CTAS avec un cast en decimal), car changer les types sur place au-dessus de fichiers existants n'est pas fiable.

<!-- takeaways -->

- Les tables sont des métadonnées sur des emplacements S3.
- Les vues partagent la logique mais ne stockent rien.
- Utilisez `decimal` pour l'argent.

<!-- unit: Lire des formats texte avec les SerDes -->

<!-- goals -->

- Choisir le bon SerDe pour CSV, fichiers délimités et logs.
- Configurer en-têtes, délimiteurs et parsing par regex.

<!-- concept -->

Les fichiers texte n'ont pas de schéma : Athena a besoin d'instructions pour les découper en colonnes. Un SerDe est cet ensemble d'instructions. Celui par défaut gère vite le texte délimité simple ; d'autres gèrent le CSV avec guillemets, les expressions régulières et des formats de logs précis. Un mauvais choix échoue rarement bruyamment : les valeurs se décalent ou deviennent `NULL`.

Pour les logs des services AWS, AWS publie un DDL prêt à l'emploi, souvent le chemin le plus rapide.

<!-- example -->

```sql
CREATE EXTERNAL TABLE raw.partners (id string, name string, city string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES ('separatorChar' = ',', 'quoteChar' = '"')
LOCATION 's3://landing/partners/'
TBLPROPERTIES ('skip.header.line.count' = '1');
```

#### Qu'est-ce qu'un SerDe ?

Un sérialiseur/désérialiseur qui indique à Athena comment lire et écrire un format : `LazySimpleSerDe` pour le texte délimité, `OpenCSVSerDe` pour le CSV avec guillemets, `JsonSerDe` (Hive ou OpenX) pour le JSON, `RegexSerDe` et `GrokSerDe` pour les journaux, et des lecteurs natifs pour Parquet, ORC et Avro.

#### Quand utiliser `OpenCSVSerDe` plutôt que `LazySimpleSerDe` ?

Quand les champs CSV sont entre guillemets et peuvent contenir des virgules. `OpenCSVSerDe` gère les guillemets mais traite toutes les colonnes comme des chaînes sauf conversion explicite, et a des limites sur certains types ; `LazySimpleSerDe` est plus rapide pour les fichiers délimités simples.

#### Comment ignorer la ligne d'en-tête des fichiers CSV ?

Avec la propriété de table `'skip.header.line.count'='1'`.

#### Comment lire des fichiers avec un délimiteur personnalisé ?

`ROW FORMAT DELIMITED FIELDS TERMINATED BY '|'` (ou `\t` pour le TSV), avec les options `ESCAPED BY` et `LINES TERMINATED BY` si besoin.

#### Comment interroger des données à l'aide d'une expression régulière ?

Définir une table avec `RegexSerDe` et une propriété `input.regex` dont les groupes de capture correspondent aux colonnes, utile pour des journaux à format fixe ; pour une analyse ponctuelle, utiliser `regexp_extract` sur une seule colonne texte.

#### Comment interroger les journaux des services AWS avec Athena ?

Créer des tables avec le DDL documenté pour chaque type de journal (CloudTrail, VPC Flow Logs, ALB, CloudFront, journaux d'accès S3), idéalement avec une projection de partitions par date et région, puis les interroger en SQL pour enquêter sur les événements de sécurité, le trafic et les erreurs.

<!-- challenge -->

Un CSV contient des noms comme `"Pérez, Ana"` et la colonne ville affiche `" Ana"`. Qu'est-ce qui ne va pas, et que changez-vous ?

<!-- solution -->

La table utilise `LazySimpleSerDe`, qui coupe à chaque virgule, y compris entre guillemets. Utilisez `OpenCSVSerDe` avec le caractère de guillemet configuré, puis castez les colonnes non textuelles, car il lit tout en chaînes.

<!-- takeaways -->

- Un SerDe dit à Athena comment parser un format.
- Le CSV avec guillemets exige `OpenCSVSerDe`.
- Un mauvais SerDe décale les valeurs en silence.

<!-- unit: JSON et données imbriquées -->

<!-- goals -->

- Lire des fichiers JSON et du JSON stocké en texte dans Athena.
- Aplatir des tableaux imbriqués avec `UNNEST`.

<!-- concept -->

Les données semi-structurées arrivent sous deux formes : des fichiers avec un objet JSON par ligne, et du JSON stocké comme chaîne dans une autre colonne. Le premier est mappé par un SerDe en colonnes, tableaux et structs compris. Le second reste une chaîne dont on extrait les valeurs à la requête.

Les tableaux transforment une ligne en plusieurs. `UNNEST` le rend explicite, ce qui compte pour des comptages justes : une commande à trois articles devient trois lignes.

<!-- example -->

```sql
SELECT o.order_id, i.sku, i.qty
FROM raw.orders o
CROSS JOIN UNNEST(o.items) AS t(i)
WHERE json_extract_scalar(o.metadata, '$.channel') = 'web';
```

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

<!-- challenge -->

Après un `UNNEST` des articles, le chiffre d'affaires total double. Qu'est-ce qui a mal tourné ?

<!-- solution -->

Le montant de la commande est répété sur chaque ligne d'article, donc le sommer après l'unnest le multiplie. Sommez des valeurs au niveau article (prix × quantité), ou agrégez les montants de commande avant le dépliage.

<!-- takeaways -->

- Les SerDes JSON mappent les objets en colonnes et structs.
- Le JSON en chaîne s'interroge avec les fonctions JSON.
- `UNNEST` multiplie les lignes ; agrégez en conséquence.

<!-- unit: Le schema on read en pratique -->

<!-- goals -->

- Diagnostiquer les décalages entre fichiers et schémas de table.
- Utiliser les pseudo-colonnes pour inspecter les fichiers source.

<!-- concept -->

Le schéma étant appliqué à la lecture, table et fichiers peuvent diverger sans que personne ne le voie, jusqu'à ce qu'une requête renvoie des `NULL` ou échoue. La façon dont Athena apparie les colonnes décide de sa tolérance : Parquet apparie par nom, les formats texte par position, donc ajouter une colonne au milieu casse les tables texte mais pas les tables Parquet.

Quand quelque chose semble bizarre, les pseudo-colonnes indiquent de quel fichier vient chaque ligne.

<!-- example -->

```sql
SELECT "$path", count(*) AS bad_rows
FROM raw.events
WHERE user_id IS NULL
GROUP BY "$path"
ORDER BY bad_rows DESC;
```

#### Que se passe-t-il si les données ne correspondent pas au schéma de la table ?

Athena applique le schéma à la lecture : les valeurs incompatibles deviennent en général `NULL` ou provoquent des erreurs comme `HIVE_BAD_DATA` (par exemple une chaîne dans une colonne entière, ou un type de colonne Parquet différent du type de la table).

#### Athena gère-t-il l'évolution du schéma ?

En Parquet, ajouter des colonnes en fin de schéma et lire par nom fonctionne ; renommer ou changer de type est risqué. En CSV, les colonnes sont positionnelles : seul l'ajout en fin est sûr. Les tables Iceberg prennent en charge une vraie évolution de schéma (ajout, suppression, renommage, réordonnancement, élargissement de types).

#### Comment Athena mappe-t-il les colonnes Parquet : par nom ou par position ?

Par nom, par défaut, pour Parquet : l'ordre des colonnes de la table n'a pas à correspondre à celui des fichiers. Le CSV et les autres formats texte mappent par position.

#### Comment n'interroger que certains fichiers d'un emplacement ?

Utiliser la pseudo-colonne `"$path"` (le chemin S3 du fichier de chaque ligne) dans une clause `WHERE`, ce qui aide aussi à repérer quel fichier contient des données défectueuses.

```sql
SELECT "$path", count(*) FROM raw.app_events_csv GROUP BY 1 ORDER BY 2 DESC;
```

#### Quelles autres pseudo-colonnes existent ?

`"$path"`, `"$file_size"` et `"$file_modified_time"` décrivent le fichier source de chaque ligne, utiles pour le lignage, le débogage et le traitement incrémental.

<!-- challenge -->

Un producteur a ajouté une colonne au milieu de son export CSV. Depuis, plusieurs colonnes contiennent de mauvaises valeurs. Que faites-vous ?

<!-- solution -->

Le CSV apparie par position : toutes les colonnes après la nouvelle se sont décalées. Mettez à jour la définition selon le nouvel ordre pour les nouveaux fichiers, et séparez anciens et nouveaux fichiers dans des tables ou partitions distinctes avec leur schéma, ou convertissez les deux en Parquet.

<!-- takeaways -->

- Les décalages de schéma apparaissent en `NULL` ou en erreurs de parsing.
- Parquet apparie par nom ; les formats texte par position.
- `"$path"` retrouve les fichiers derrière des lignes suspectes.

<!-- stage: Organisation des données -->

### Partitions et projection de partitions

<!-- unit: Partitionnement et élagage -->

<!-- goals -->

- Choisir les colonnes et la granularité de partition.
- Écrire des filtres qui élaguent vraiment les partitions.

<!-- concept -->

Partitionner répartit les fichiers d'une table dans des dossiers selon la valeur d'une colonne : une requête qui filtre sur cette colonne ne lit que les dossiers correspondants. C'est le plus grand levier sur la taille du scan, à condition que les requêtes filtrent directement sur la colonne de partition et que les partitions ne soient ni trop petites ni trop nombreuses.

Trop de partitions minuscules déplacent le coût du scan vers la planification et le listage. Le bucketing complète : il organise les fichiers d'une partition selon une colonne à forte cardinalité.

<!-- example -->

```sql
-- prunes: compares the partition column directly
SELECT count(*) FROM logs.events WHERE dt BETWEEN '2026-10-01' AND '2026-10-07';
-- does not prune: function applied to the partition column
SELECT count(*) FROM logs.events WHERE date(dt) >= date '2026-10-01';
```

#### Qu'est-ce que le partitionnement dans Athena ?

Organiser les données dans S3 selon les valeurs d'une ou plusieurs colonnes (`s3://bucket/table/dt=2026-10-15/`) et les déclarer comme colonnes de partition, pour que les requêtes qui filtrent dessus ne lisent que les dossiers correspondants.

#### Qu'est-ce que l'élagage de partitions (partition pruning) ?

Le moteur utilise les filtres sur les colonnes de partition pour écarter les partitions qui ne peuvent pas correspondre, ce qui réduit les données lues. Cela ne fonctionne que si le filtre porte sur la colonne de partition elle-même, sans fonction qui empêche son évaluation à la planification.

#### Quelle est une bonne stratégie de partitionnement ?

Partitionner selon les colonnes filtrées par la plupart des requêtes (généralement la date), à une granularité qui garde chaque partition suffisamment volumineuse (au moins quelques dizaines de Mo, idéalement plus), et éviter les clés à forte cardinalité qui créent des millions de minuscules partitions.

#### Pourquoi un trop grand nombre de partitions nuit-il aux performances ?

La planification doit récupérer et évaluer les métadonnées des partitions, et chaque partition implique souvent des listages S3 séparés et de petits fichiers. Les index de partition Glue ou la projection de partitions réduisent le coût de planification.

#### Qu'est-ce que le bucketing dans Athena ?

La répartition des données d'une partition dans un nombre fixe de fichiers selon le hachage d'une colonne (`CLUSTERED BY (user_id) INTO 32 BUCKETS`), qui aide les requêtes filtrant sur cette colonne à sauter des fichiers. On l'utilise surtout avec `CTAS`.

#### Comment partitionner par date quand les données contiennent des horodatages ?

Dériver à l'écriture une date sous forme de chaîne (ou année/mois/jour) et la stocker en colonne de partition ; avec Iceberg, utiliser le partitionnement caché `day(event_ts)` pour que les requêtes filtrent directement sur l'horodatage.

#### Pourquoi une requête peut-elle ne pas élaguer les partitions alors qu'elle filtre sur la date ?

Le filtre applique peut-être une fonction à la colonne de partition (par exemple `date(dt) = …` sur une colonne texte), compare avec un type qui impose une conversion, ou filtre sur une autre colonne que la clé de partition. Filtrez sur la colonne de partition avec des littéraux du même type.

<!-- challenge -->

Une table est partitionnée par `customer_id` (2 millions de valeurs) et `dt`. Les requêtes sont lentes même filtrées. Que changez-vous ?

<!-- solution -->

Retirer `customer_id` des colonnes de partition : il crée des millions de partitions minuscules. Partitionner seulement par date et faire du bucketing ou trier par `customer_id` dans les partitions pour que les statistiques des fichiers sautent encore des données.

<!-- takeaways -->

- Partitionnez selon les colonnes les plus filtrées, souvent la date.
- Filtrez directement la colonne de partition pour élaguer.
- Trop de partitions nuisent à la planification ; bucketing pour la forte cardinalité.

<!-- unit: Enregistrer les partitions -->

<!-- goals -->

- Ajouter, lister et supprimer des partitions dans le catalogue.
- Savoir quand `MSCK REPAIR TABLE` fonctionne et quand il échoue.

<!-- concept -->

Les tables classiques ne voient que les partitions connues du catalogue. Les nouveaux dossiers dans S3 sont invisibles tant que personne ne les enregistre, raison la plus fréquente de « les données sont là mais la requête ne renvoie rien ».

La façon d'enregistrer dépend des noms de dossiers. Les chemins de style Hive `key=value` se découvrent automatiquement ; tout le reste demande des emplacements explicites. Supprimer une partition ne touche aussi que les métadonnées : les fichiers restent dans S3.

<!-- example -->

```sql
ALTER TABLE logs.events ADD IF NOT EXISTS
  PARTITION (dt = '2026-10-17') LOCATION 's3://lake/events/dt=2026-10-17/';
SHOW PARTITIONS logs.events;
```

#### Comment ajouter des partitions ?

`ALTER TABLE t ADD PARTITION (dt='2026-10-15') LOCATION 's3://.../dt=2026-10-15/'`, `MSCK REPAIR TABLE` pour les dossiers de style Hive, un crawler Glue, l'API Glue ou la projection de partitions (sans enregistrement).

#### Que fait `MSCK REPAIR TABLE` ?

Il parcourt l'emplacement S3 de la table à la recherche de dossiers de partition de style Hive (`cle=valeur`) et ajoute au catalogue les partitions manquantes. Il est lent sur les tables très partitionnées ; mieux vaut ajouter les partitions explicitement ou utiliser la projection de partitions.

#### Quelle différence entre chemins de partition de style Hive et non Hive ?

Les chemins de style Hive contiennent `cle=valeur` (`dt=2026-10-15/`), que `MSCK REPAIR` et les crawlers comprennent. Les chemins non Hive (`2026/10/15/`) exigent d'ajouter les partitions explicitement avec un `LOCATION`, ou une projection de partitions avec un modèle d'emplacement.

#### Comment voir les partitions d'une table ?

`SHOW PARTITIONS table` liste les partitions enregistrées (pas celles projetées), et la console ou l'API Glue montrent les emplacements et schémas des partitions.

#### Comment supprimer des partitions ?

`ALTER TABLE t DROP PARTITION (dt='2026-10-01')` ne supprime que les métadonnées du catalogue ; supprimez les objets S3 séparément si les données doivent disparaître aussi.

<!-- challenge -->

Un job nocturne lance `MSCK REPAIR TABLE` sur une table de 50 000 partitions et dure maintenant 40 minutes. Que suggérez-vous ?

<!-- solution -->

Arrêter de scanner tout l'emplacement : ajouter explicitement la partition du jour avec `ALTER TABLE ADD PARTITION` dans le job de chargement, ou passer à la partition projection pour ne plus rien enregistrer.

<!-- takeaways -->

- Les partitions non enregistrées sont invisibles aux requêtes.
- `MSCK REPAIR` ne comprend que les chemins de style Hive et scanne tout.
- Supprimer des partitions efface des métadonnées, pas des fichiers.

<!-- unit: Partition projection -->

<!-- goals -->

- Configurer la partition projection pour des partitions prévisibles.
- Reconnaître les cas où la projection ne convient pas.

<!-- concept -->

Enregistrer les partitions est une corvée de maintenance et un coût de planification. La partition projection supprime les deux : au lieu de chercher les partitions dans le catalogue, Athena les calcule à partir de règles dans les propriétés de la table, comme une plage de dates et un modèle de chemin. Les nouvelles données sont interrogeables dès leur arrivée.

Les règles doivent décrire la réalité. La projection convient aux valeurs prévisibles comme les dates et les énumérations connues, et remplace entièrement les partitions du catalogue pour cette table.

<!-- example -->

```sql
ALTER TABLE logs.events SET TBLPROPERTIES (
  'projection.enabled' = 'true',
  'projection.dt.type' = 'date',
  'projection.dt.format' = 'yyyy-MM-dd',
  'projection.dt.range' = '2024-01-01,NOW',
  'storage.location.template' = 's3://lake/events/dt=${dt}/'
);
```

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

#### Peut-on mélanger projection de partitions et partitions du catalogue ?

Quand la projection est activée, Athena ignore les partitions enregistrées dans le catalogue pour cette table et n'utilise que les règles de projection. Les autres moteurs voient toujours les partitions du catalogue.

<!-- challenge -->

Après activation de la projection, les requêtes sur l'an dernier ne renvoient plus rien, alors qu'elles fonctionnaient. Que vérifiez-vous ?

<!-- solution -->

Que la plage de projection couvre l'an dernier et que le modèle d'emplacement et le format correspondent aux vrais chemins. Projection active, les partitions du catalogue sont ignorées : tout décalage masque des données.

<!-- takeaways -->

- La projection calcule les partitions par règles ; rien à enregistrer.
- Elle convient aux valeurs prévisibles comme les dates.
- Projection active, les partitions du catalogue sont ignorées.

### Formats de fichiers et organisation des données

<!-- unit: Formats colonnes -->

<!-- goals -->

- Expliquer pourquoi Parquet et ORC rendent Athena plus rapide et moins cher.
- Convertir des formats bruts en colonnes avec Athena lui-même.

<!-- concept -->

Les formats en lignes comme CSV et JSON obligent le moteur à lire chaque octet pour trouver quelques colonnes. Les formats en colonnes stockent chaque colonne séparément avec des statistiques : une requête ne lit que les colonnes sélectionnées et saute les blocs dont les statistiques ne correspondent pas. D'où des requêtes qui scannent cinquante fois moins d'octets.

La conversion est une requête ponctuelle, et le gain se voit sur chaque requête suivante, pourvu que l'on cesse d'écrire `SELECT *`.

<!-- example -->

```sql
CREATE TABLE curated.events
WITH (format = 'PARQUET', write_compression = 'ZSTD',
      external_location = 's3://lake/curated/events/', partitioned_by = ARRAY['dt'])
AS SELECT event_id, user_id, event_type, ts, dt FROM raw.events_json;
```

#### Quels formats de fichiers Athena prend-il en charge ?

Le CSV/TSV et d'autres textes délimités, JSON, Parquet, ORC, Avro, Ion, les journaux via les SerDe Regex ou Grok, et les formats de table ouverts Iceberg, Hudi (lecture) et Delta Lake (lecture).

#### Pourquoi recommande-t-on Parquet et ORC ?

Ils sont en colonnes (lecture des seules colonnes utiles), compressés par colonne, et stockent des statistiques (min/max par groupe de lignes ou stripe) qui permettent à Athena de sauter des données. Ils prennent aussi en charge la poussée des prédicats, ce qui accélère les requêtes et réduit le coût.

#### Quelle différence entre Parquet et ORC pour Athena ?

Les deux sont en colonnes, avec statistiques et compression, et fonctionnent bien. Parquet est le choix le plus courant dans l'écosystème (Spark, valeurs par défaut d'Iceberg) ; ORC a été historiquement privilégié par Hive. Choisissez selon les écrivains et les autres moteurs utilisés.

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

<!-- challenge -->

Des analystes se plaignent qu'une table Parquet « coûte toujours cher ». La requête principale est `SELECT * FROM events WHERE dt = ...` sur une table de 200 colonnes. Que suggérez-vous ?

<!-- solution -->

Ne sélectionner que les colonnes nécessaires ; avec Parquet, le coût baisse à chaque colonne retirée. Proposer des vues ou des tables curées plus étroites pour les usages courants, et garder le filtre de date pour l'élagage.

<!-- takeaways -->

- Les formats colonnes ne lisent que les colonnes sélectionnées.
- Les statistiques permettent de sauter des blocs.
- `SELECT *` annule l'essentiel de l'économie.

<!-- unit: Compression -->

<!-- goals -->

- Choisir les codecs pour fichiers colonnes et texte.
- Gérer les gros fichiers non découpables.

<!-- concept -->

Athena facture les octets compressés : compresser est une remise directe. Le codec influe aussi sur le parallélisme : dans Parquet ou ORC, tout codec convient car le format découpe le fichier en blocs, mais un seul fichier texte gzip ne peut être lu que par un worker, du début à la fin.

Préférez donc le format colonnes avec Snappy ou ZSTD, et pour le texte, des fichiers de taille modérée.

<!-- example -->

| Fichier | Découpable pour Athena ? |
|---|---|
| Parquet avec ZSTD | Oui (row groups) |
| `.csv.gz` de 20 Go | Non : un seul worker le lit |
| 200 × `.csv.gz` de 100 Mo | En parallèle sur les fichiers |

#### Quels codecs de compression conviennent ?

Snappy et ZSTD pour Parquet et ORC (rapides, découpables au sein du format). Pour les fichiers texte, gzip est courant mais non découpable : un gros fichier gzip est lu par un seul worker ; bzip2 est découpable mais lent.

#### La compression réduit-elle les coûts d'Athena ?

Oui. Athena facture les octets compressés lus : des fichiers compressés (et l'encodage en colonnes) réduisent directement le coût, en plus du stockage S3.

#### Comment traiter des données qui arrivent en un seul énorme fichier gzip ?

gzip n'étant pas découpable, un seul worker le lit. Découpez le fichier avant ou pendant l'ingestion, recompressez en bzip2 ou, mieux, convertissez en Parquet avec un `CTAS` ou un job Glue.

<!-- challenge -->

Un partenaire envoie un `.json.gz` de 30 Go par jour et la requête dessus dépasse le timeout. Que faites-vous ?

<!-- solution -->

Gzip n'est pas découpable : un seul worker le lit. Ajouter une étape d'ingestion (Glue, Lambda ou Firehose) qui le découpe et le convertit en Parquet partitionné avec Snappy ou ZSTD, et interroger la table convertie.

<!-- takeaways -->

- La compression réduit les octets payés.
- Les formats colonnes découpent les fichiers compressés ; le gzip texte non.
- Préférez Snappy ou ZSTD dans Parquet ou ORC.

<!-- unit: Taille et organisation des fichiers -->

<!-- goals -->

- Garder les fichiers dans la bonne plage de taille et corriger les petits fichiers.
- Utiliser tri et statistiques pour que le moteur saute des données.

<!-- concept -->

Chaque fichier a un coût fixe d'ouverture, de listage et de planification : des milliers de fichiers minuscules gaspillent l'essentiel du temps d'une requête. Les très gros fichiers limitent le parallélisme. La plage saine va d'environ 128 Mo à 1 Go, ce qui suppose d'écrire par lots ou de compacter ensuite.

Dans les fichiers, l'ordre compte. Quand les données sont triées par une colonne filtrée, les statistiques min/max de chaque bloc se resserrent et le predicate pushdown saute la plupart des blocs.

<!-- example -->

```sql
-- compact one day of small files into a few sorted Parquet files
INSERT INTO curated.events
SELECT * FROM raw.events WHERE dt = '2026-10-17'
ORDER BY user_id;
```

#### Quelle est la taille de fichier idéale pour Athena ?

Environ 128 Mo à 1 Go par fichier. De nombreux petits fichiers (quelques Ko) ajoutent une surcharge par fichier et des coûts de requêtes S3 ; de très gros fichiers non découpables limitent le parallélisme.

#### Comment corriger une table composée de nombreux petits fichiers ?

Les compacter : lancer un `CTAS` ou un `INSERT INTO` qui réécrit les données en fichiers moins nombreux et plus gros (avec bucketing ou un partitionnement maîtrisé), utiliser `OPTIMIZE` sur les tables Iceberg, ou corriger le producteur (lots plus gros, buffering Firehose).

#### En quoi trier les données aide-t-il Athena ?

Quand les données sont triées (ou regroupées) selon une colonne de filtre courante à l'intérieur des fichiers, les statistiques Parquet et ORC ont des plages min/max étroites, ce qui permet de sauter davantage de groupes de lignes.

#### Qu'est-ce que la poussée des prédicats (predicate pushdown) dans Athena ?

Les filtres sont poussés jusqu'au lecteur de fichiers, qui utilise les statistiques Parquet/ORC pour sauter les groupes de lignes ou stripes dont le min/max ne peut pas correspondre : moins de données sont lues et décompressées.

#### Quelle taille de groupe de lignes est bonne pour Parquet ?

Typiquement de 128 Mo à 512 Mo ; des groupes plus gros compressent bien et réduisent la surcharge, mais des groupes énormes réduisent l'efficacité du saut de données. Des écrivains comme Spark ont des valeurs par défaut raisonnables.

#### Une table reçoit 2 millions de petits fichiers JSON par jour. Que recommandez-vous ?

Corriger le producteur pour regrouper les enregistrements (buffering Firehose, écritures plus grosses), ajouter une étape de compaction qui convertit chaque journée en quelques fichiers Parquet (job Glue ou `CTAS`), et interroger la table compactée ; ne garder le JSON brut qu'en archive.

<!-- challenge -->

Une Lambda écrit un fichier minuscule par événement dans S3. Les requêtes ralentissent et les coûts S3 augmentent. Quels deux changements faites-vous ?

<!-- solution -->

Regrouper chez le producteur : envoyer les événements à Firehose avec un tampon (par exemple 128 Mo ou 5 minutes) et conversion en Parquet. Puis compacter une fois les anciennes données en gros fichiers et supprimer les petits.

<!-- takeaways -->

- Visez des fichiers d'environ 128 Mo à 1 Go.
- Écrivez par lots ou compactez les petits fichiers.
- Des données triées rendent statistiques et pushdown efficaces.

### Tables Iceberg dans Athena

<!-- unit: Iceberg sur Athena -->

<!-- goals -->

- Expliquer ce qu'Iceberg ajoute aux fichiers Parquet.
- Choisir entre tables Iceberg et tables de style Hive.

<!-- concept -->

Les tables de style Hive sont des dossiers de fichiers : simples, mais sans transactions, sans modification de lignes et sans écritures concurrentes sûres. Iceberg ajoute une couche de métadonnées qui enregistre exactement quels fichiers composent chaque version de la table. Chaque écriture devient un commit atomique, d'où découlent mises à jour, time travel et changements de schéma.

Le format étant ouvert, la même table fonctionne dans Spark, Trino, Snowflake et d'autres : Iceberg est le choix par défaut pour les nouvelles tables du lake qui évoluent.

<!-- example -->

```sql
CREATE TABLE lake.customers (
  customer_id bigint, email string, country string, updated_at timestamp
)
PARTITIONED BY (country)
LOCATION 's3://lake/iceberg/customers/'
TBLPROPERTIES ('table_type' = 'ICEBERG', 'format' = 'parquet');
```

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

#### Iceberg ou tables de style Hive dans Athena : comment choisir ?

Iceberg quand il faut des mises à jour, suppressions, upserts (CDC, effacements RGPD), de l'évolution de schéma, des écrivains concurrents ou du voyage dans le temps. Le Parquet de style Hive est plus simple pour des données immuables en ajout seul écrites par d'autres outils. Les nouvelles conceptions de lakehouse choisissent généralement Iceberg.

#### D'autres moteurs peuvent-ils utiliser les mêmes tables Iceberg ?

Oui. Spark sur EMR ou Glue, Trino, Flink, Snowflake, Databricks et d'autres peuvent lire et écrire les mêmes tables Iceberg via le Glue Data Catalog ou un catalogue REST Iceberg, ce qui évite l'enfermement dans un moteur.

#### Que sont les S3 Tables ?

Des table buckets S3 qui stockent des tables Iceberg avec une maintenance intégrée (compaction, gestion des snapshots) et une intégration de catalogue, qu'Athena peut interroger et écrire comme les autres tables Iceberg.

#### Quelles propriétés de table comptent pour Iceberg dans Athena ?

`format` (parquet, orc, avro), `write_compression`, `optimize_rewrite_delete_file_threshold`, `vacuum_max_snapshot_age_seconds`, `vacuum_min_snapshots_to_keep` et `vacuum_max_metadata_files_to_keep`, qui contrôlent l'organisation des fichiers et la rétention.

<!-- challenge -->

Une table de logs en ajout seul est lue uniquement par Athena et ne change jamais. Faut-il la passer en Iceberg ?

<!-- solution -->

Pas forcément. Une table Parquet partitionnée avec projection fonctionne déjà bien. Iceberg apporte de la valeur pour les modifications de lignes, les écrivains concurrents, l'évolution du schéma ou des partitions, ou le time travel. Choisissez-le si ces besoins sont proches.

<!-- takeaways -->

- Iceberg fait de chaque écriture un commit atomique versionné.
- Il permet mises à jour, suppressions, time travel et évolution.
- Le Parquet simple suffit pour des données simples en ajout seul.

<!-- unit: Modifier les données dans Iceberg -->

<!-- goals -->

- Appliquer `UPDATE`, `DELETE` et `MERGE` aux tables Iceberg.
- Gérer le CDC et les suppressions RGPD avec des écrivains concurrents.

<!-- concept -->

Avec Iceberg, les modifications au niveau ligne deviennent du SQL ordinaire. Athena écrit de petits fichiers de suppression qui marquent les lignes effacées au lieu de réécrire les fichiers de données : les écritures restent rapides mais les lectures ralentissent jusqu'à ce qu'une compaction les fusionne.

La concurrence est optimiste : les écrivains ne verrouillent pas, ils vérifient au commit et réessaient en cas de conflit. Cela convient à la plupart des pipelines, tant que deux jobs ne réécrivent pas les mêmes partitions en même temps.

<!-- example -->

```sql
MERGE INTO lake.customers t
USING staging.customer_changes s
ON t.customer_id = s.customer_id
WHEN MATCHED AND s.op = 'D' THEN DELETE
WHEN MATCHED THEN UPDATE SET email = s.email, country = s.country, updated_at = s.updated_at
WHEN NOT MATCHED AND s.op <> 'D' THEN INSERT VALUES (s.customer_id, s.email, s.country, s.updated_at);
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

#### Comment fonctionnent les suppressions au niveau ligne d'Iceberg dans Athena ?

Athena écrit des fichiers de suppression positionnels (merge-on-read) qui marquent les lignes supprimées au lieu de réécrire les fichiers de données. Les lectures les fusionnent à la volée : les tables avec beaucoup de suppressions ont besoin d'`OPTIMIZE` réguliers pour rester rapides.

#### Plusieurs écrivains peuvent-ils modifier une table Iceberg en même temps ?

Oui, avec une concurrence optimiste : chaque commit vérifie la version courante de la table, et les commits en conflit échouent et doivent être relancés. Évitez de nombreux écrivains concurrents mettant à jour les mêmes partitions.

#### Les analystes doivent supprimer les données de certains clients au titre du RGPD. Comment le permettre dans Athena ?

Stocker les données dans des tables Iceberg, lancer `DELETE FROM … WHERE customer_id = …` sur les tables concernées, puis `OPTIMIZE` et `VACUUM` pour supprimer physiquement les anciens fichiers après la période de rétention des snapshots. Avec des tables Hive, il faudrait réécrire des partitions entières.

#### Comment interroger le dernier état d'une table qui reçoit des enregistrements CDC ?

Soit maintenir une table Iceberg avec un `MERGE` appliquant les changements (le plus propre), soit, sur une table de changements en ajout seul, utiliser `ROW_NUMBER()` par clé ordonné par horodatage de changement et garder la dernière ligne non supprimée dans une vue.

```sql
SELECT * FROM (
  SELECT *, row_number() OVER (PARTITION BY customer_id ORDER BY change_ts DESC) AS rn
  FROM raw.customer_changes
) WHERE rn = 1 AND op <> 'D';
```

<!-- challenge -->

Après un `DELETE` RGPD, les données de la personne sont toujours dans des fichiers S3. Pourquoi, et qu'est-ce qui achève la suppression ?

<!-- solution -->

Les fichiers de suppression marquent seulement les lignes ; anciens fichiers de données et snapshots les contiennent encore. Lancez `OPTIMIZE` pour réécrire les fichiers sans ces lignes, puis `VACUUM` pour expirer les anciens snapshots et retirer les fichiers non référencés.

<!-- takeaways -->

- Iceberg prend en charge `UPDATE`, `DELETE` et `MERGE` dans Athena.
- Les suppressions écrivent des fichiers de suppression ; la compaction les applique.
- Les commits concurrents sont vérifiés de façon optimiste.

<!-- unit: Évolution, time travel et maintenance -->

<!-- goals -->

- Faire évoluer schémas et partitionnement sans réécrire les données.
- Utiliser time travel, retours arrière et commandes de maintenance.

<!-- concept -->

Comme Iceberg suit les colonnes par identifiant et les partitions comme transformations de colonnes, la forme de la table peut changer sans toucher aux anciens fichiers. Les requêtes filtrent sur la vraie colonne et les bonnes partitions sont élaguées en coulisse.

Chaque commit laisse un snapshot, d'où un time travel et des retours arrière gratuits jusqu'à ce que la maintenance les expire. C'est l'équilibre à gérer : snapshots et petits fichiers s'accumulent, il faut donc planifier compaction et vacuum.

<!-- example -->

```sql
SELECT count(*) FROM lake.customers FOR TIMESTAMP AS OF TIMESTAMP '2026-10-15 08:00:00 UTC';
OPTIMIZE lake.customers REWRITE DATA USING BIN_PACK;
VACUUM lake.customers;
```

#### Qu'est-ce que le partitionnement caché d'Iceberg ?

Des partitions définies comme des transformations de colonnes (`day(event_ts)`, `bucket(16, user_id)`, `truncate(10, sku)`) : les requêtes filtrent sur la colonne d'origine (`event_ts`) et Iceberg élague automatiquement les partitions ; les utilisateurs n'ont pas à connaître les colonnes de partition.

#### Peut-on faire évoluer le partitionnement d'une table Iceberg ?

Oui. On peut changer la spécification de partition (par exemple de mensuelle à quotidienne) sans réécrire les anciennes données ; les anciens fichiers gardent l'ancienne spécification, les nouvelles données utilisent la nouvelle, et les requêtes gèrent les deux.

#### Comment ajouter une colonne à une table Iceberg ?

`ALTER TABLE lake.customers ADD COLUMNS (segment string)`. Les fichiers existants ne sont pas réécrits ; les anciennes lignes renvoient `NULL` pour la nouvelle colonne.

#### Comment fonctionne le voyage dans le temps d'Iceberg dans Athena ?

```sql
SELECT * FROM lake.customers FOR TIMESTAMP AS OF TIMESTAMP '2026-10-15 08:00:00 UTC';
SELECT * FROM lake.customers FOR VERSION AS OF 949530903748831860;
```

On peut aussi consulter des tables de métadonnées comme `"customers$snapshots"`, `"customers$history"`, `"customers$files"` et `"customers$partitions"`.

#### Comment revenir en arrière sur une table Iceberg dans Athena ?

Lire la version précédente avec le voyage dans le temps et la réécrire (par exemple un `CTAS` depuis `FOR VERSION AS OF`), ou utiliser un moteur disposant de procédures de retour arrière (`rollback_to_snapshot` de Spark) sur la même table.

#### Que font `OPTIMIZE` et `VACUUM` sur les tables Iceberg ?

`OPTIMIZE table REWRITE DATA USING BIN_PACK` compacte les petits fichiers et fusionne les fichiers de suppression avec les fichiers de données. `VACUUM` expire les anciens snapshots et supprime les fichiers non référencés (selon les propriétés de rétention), libérant du stockage.

<!-- challenge -->

Un job défectueux a écrasé la moitié d'une table clients à 09:12. Comment la restaurer avec Athena ?

<!-- solution -->

Interroger la table `FOR TIMESTAMP AS OF` 09:10 pour confirmer le bon état, puis reconstruire la table à partir de cette version (par exemple CTAS vers une nouvelle table puis échange, ou réinsertion des anciennes lignes). À faire avant que `VACUUM` n'expire le snapshot.

<!-- takeaways -->

- Partitionnement caché et identifiants de colonnes sécurisent l'évolution.
- Les snapshots offrent time travel et retour arrière.
- Planifiez `OPTIMIZE` et `VACUUM` pour maîtriser la croissance.

<!-- stage: Construire et interroger -->

### CTAS, INSERT et UNLOAD

<!-- unit: Écrire des tables avec CTAS -->

<!-- goals -->

- Créer des tables par CTAS dans le bon format et la bonne organisation.
- Respecter les limites de CTAS sur partitions, fichiers et emplacements.

<!-- concept -->

CTAS est le principal outil de transformation d'Athena : une instruction exécute une requête et écrit le résultat dans une nouvelle table, en choisissant format, compression, partitionnement et bucketing. On transforme ainsi des fichiers bruts en tables curées sans autre service.

Ses garde-fous façonnent les pipelines. Une requête ne peut écrire qu'un nombre limité de partitions et refuse les emplacements non vides : les gros backfills se font par lots et chaque exécution exige un emplacement neuf ou nettoyé.

<!-- example -->

```sql
CREATE TABLE curated.daily_sales
WITH (format = 'PARQUET', external_location = 's3://lake/curated/daily_sales/v2/',
      partitioned_by = ARRAY['dt'], bucketed_by = ARRAY['store_id'], bucket_count = 8)
AS SELECT store_id, sum(amount) AS revenue, dt
   FROM sales.orders GROUP BY store_id, dt;
```

#### Qu'est-ce que `CTAS` ?

`CREATE TABLE AS SELECT` : crée une nouvelle table à partir des résultats d'une requête, en écrivant dans S3 des fichiers au format, à la compression, au partitionnement et au bucketing choisis. On l'utilise pour convertir des formats, construire des agrégats et matérialiser des transformations.

#### Quelles sont les limites de `CTAS` et `INSERT INTO` ?

Une seule requête peut créer ou alimenter un nombre limité de partitions (100 par requête pour les tables Hive) : les gros backfills exigent plusieurs instructions ou des boucles par plages de partitions. Les tables Iceberg n'ont pas cette limite précise.

#### Comment maîtriser le nombre de fichiers produits par un `CTAS` ?

Avec `bucketed_by` et `bucket_count`, qui fixent le nombre de fichiers par partition, ou en réduisant le parallélisme de l'étape finale ; sinon Athena écrit autant de fichiers que les workers en produisent.

#### Un `CTAS` peut-il écrire dans un emplacement S3 existant ?

Non. L'`external_location` doit être vide, ce qui évite d'écraser des données par erreur. Supprimez l'emplacement ou utilisez-en un nouveau pour les relances.

#### Comment créer une copie vide du schéma d'une table ?

`CREATE TABLE nouvelle_t WITH (...) AS SELECT * FROM t WITH NO DATA`, qui crée la définition de la table sans écrire de lignes.

<!-- challenge -->

Un CTAS sur trois ans de données quotidiennes échoue car il écrit trop de partitions. Comment le charger ?

<!-- solution -->

Créer la table par CTAS pour un premier lot de moins de 100 partitions (par exemple trois mois), puis ajouter le reste avec `INSERT INTO ... SELECT` par lots de même taille, idéalement pilotés par un script.

<!-- takeaways -->

- CTAS écrit le résultat d'une requête dans une nouvelle table formatée.
- Les limites de partitions imposent des chargements par lots.
- CTAS exige un emplacement cible vide.

<!-- unit: ELT idempotent sur Athena -->

<!-- goals -->

- Construire des pipelines relançables avec `INSERT INTO`, CTAS ou dbt.
- Planifier des requêtes Athena avec les services AWS ou Airflow.

<!-- concept -->

Sur les tables de style Hive, `INSERT INTO` ne fait qu'ajouter des fichiers : l'exécuter deux fois double les données. Un pipeline devient relançable quand chaque exécution possède une tranche, en général une partition de date, et la nettoie d'abord. Iceberg supprime le problème avec `MERGE` et l'écrasement, raison pour laquelle beaucoup d'ELT sur Athena utilisent Iceberg pour les couches curées.

L'orchestration consiste juste à appeler l'API selon un calendrier, mais dbt y ajoute tests et dépendances.

<!-- example -->

```bash
# rerun-safe daily load for a Hive-style table
aws s3 rm --recursive s3://lake/curated/orders/dt=2026-10-17/
aws athena start-query-execution --work-group etl --query-string \
 "INSERT INTO curated.orders SELECT ..., dt FROM raw.orders WHERE dt = '2026-10-17'"
```

#### Que fait `INSERT INTO` sur une table de style Hive ?

Il ajoute de nouveaux fichiers à l'emplacement de la table (et enregistre les nouvelles partitions). Il ne modifie jamais les fichiers existants : le relancer duplique les données, sauf à supprimer d'abord les fichiers de la partition cible.

#### Comment rendre un ELT Athena idempotent ?

Pour les tables Hive, écrire la sortie de chaque exécution dans une partition et supprimer ou écraser cette partition avant de relancer (souvent en écrivant dans un nouvel emplacement puis en changeant l'emplacement de la partition). Pour les tables Iceberg, utiliser `MERGE`, ou `DELETE` plus `INSERT` dans la même logique, ou des schémas d'écrasement avec Iceberg.

#### Comment planifier des requêtes Athena ?

Avec EventBridge Scheduler ou Step Functions appelant `StartQueryExecution`, l'`AthenaOperator` d'Airflow, dbt avec l'adaptateur dbt-athena, ou une fonction Lambda planifiée.

#### Peut-on utiliser dbt avec Athena ?

Oui, avec l'adaptateur dbt-athena : les modèles se matérialisent en vues, tables (`CTAS`), modèles incrémentaux (`insert_overwrite` par partition, `append` ou `merge` sur Iceberg) et tables Iceberg, avec Glue comme catalogue.

#### Comment construire un petit pipeline ELT uniquement avec Athena ?

Des tables raw sur les fichiers d'atterrissage, des `CTAS` ou `INSERT INTO` (ou des modèles dbt-athena) pour construire des tables nettoyées en Iceberg ou Parquet, `MERGE` pour les upserts, des contrôles de qualité sous forme de requêtes SQL qui font échouer le pipeline quand elles renvoient des lignes, et Step Functions ou Airflow pour planifier et ordonner les instructions.

<!-- challenge -->

Un modèle incrémental dbt-athena ajoute des lignes à chaque exécution et les relances créent des doublons. Vers quelle stratégie passez-vous ?

<!-- solution -->

`insert_overwrite` sur une partition de date (tables Hive) ou `merge` avec une `unique_key` sur des tables Iceberg. Les deux remplacent les données concernées à la relance au lieu d'ajouter.

<!-- takeaways -->

- `INSERT INTO` ajoute ; relancer duplique.
- Chaque exécution possède une tranche, ou utilisez le `MERGE` d'Iceberg.
- dbt-athena ajoute tests et dépendances à l'ELT sur Athena.

<!-- unit: Exporter et paramétrer -->

<!-- goals -->

- Exporter des résultats de requêtes dans des formats utiles.
- Utiliser des requêtes paramétrées en sécurité dans les applications.

<!-- concept -->

Tout résultat ne doit pas devenir une table. Parfois un autre système a besoin de fichiers, et `UNLOAD` écrit les résultats dans le format choisi sans rien enregistrer. Parfois une personne a besoin d'un seul CSV, que l'emplacement des résultats fournit déjà.

Les applications qui construisent des requêtes à partir d'entrées utilisateur ne doivent jamais concaténer de chaînes ; les paramètres séparent valeurs et SQL et évitent l'injection.

<!-- example -->

```sql
UNLOAD (SELECT * FROM curated.daily_sales WHERE dt = '2026-10-17')
TO 's3://exports/partner_x/2026-10-17/'
WITH (format = 'PARQUET', compression = 'SNAPPY');

PREPARE sales_by_store FROM SELECT * FROM curated.daily_sales WHERE store_id = ?;
EXECUTE sales_by_store USING 42;
```

#### Que fait `UNLOAD` ?

Il écrit les résultats d'une requête dans S3 au format choisi (Parquet, ORC, Avro, JSON, texte), avec partitionnement et compression optionnels, sans créer de table, ce qui est utile pour exporter vers d'autres systèmes.

```sql
UNLOAD (SELECT * FROM curated.app_events WHERE dt = '2026-10-15')
TO 's3://exports/app_events/dt=2026-10-15/'
WITH (format = 'PARQUET', compression = 'SNAPPY');
```

#### Comment exporter les résultats d'une requête en un seul CSV ?

Lancer la requête et télécharger le fichier de résultats depuis l'emplacement de résultats (Athena écrit un CSV par requête), ou utiliser `UNLOAD` avec un format texte ; de très gros résultats peuvent être répartis sur plusieurs fichiers avec `UNLOAD`.

#### Que sont les instructions préparées et les requêtes paramétrées ?

Des instructions créées avec `PREPARE` (ou passées avec `ExecutionParameters`) contenant des marqueurs `?` remplis à l'exécution, ce qui évite l'injection SQL et permet aux applications de réutiliser le texte des requêtes.

```sql
PREPARE events_by_day FROM
SELECT event_type, count(*) FROM curated.app_events WHERE dt = ? GROUP BY 1;

EXECUTE events_by_day USING '2026-10-15';
```

<!-- challenge -->

Une application interne construit le SQL Athena en concaténant un nom de magasin saisi par l'utilisateur. Quel risque, et quelle correction ?

<!-- solution -->

L'injection SQL : un nom forgé pourrait modifier la requête. Utilisez des requêtes paramétrées (`ExecutionParameters` ou prepared statements) et un workgroup et un rôle IAM limités aux tables nécessaires à l'application.

<!-- takeaways -->

- `UNLOAD` exporte des résultats en fichiers sans table.
- Chaque requête écrit aussi un CSV dans l'emplacement des résultats.
- Paramétrez les requêtes construites à partir d'entrées utilisateur.

### Fonctions SQL et modèles de requêtes

<!-- unit: Types, dates et NULL -->

<!-- goals -->

- Gérer correctement dates, conversions et `NULL`.
- Pseudonymiser des identifiants par hachage.

<!-- concept -->

Beaucoup de mauvaises réponses en SQL viennent de trois endroits : des dates au mauvais type ou fuseau, des casts qui échouent sur des valeurs sales, et des `NULL` qui disparaissent en silence des comparaisons. Les données du lake sont souvent sales car jamais validées à l'écriture : les fonctions défensives comptent plus dans Athena que dans un entrepôt.

Le hachage a aussi sa place : un hash déterministe permet de joindre sur un identifiant sans l'exposer.

<!-- example -->

```sql
SELECT
  date_trunc('month', TRY_CAST(order_ts AS timestamp)) AS month,
  count(*) FILTER (WHERE TRY_CAST(amount AS decimal(12,2)) IS NULL) AS bad_amounts,
  to_hex(hmac_sha256(to_utf8(email), to_utf8('salt-from-secrets'))) AS email_key
FROM raw.orders
GROUP BY 1, 3;
```

#### Comment manipuler les dates et heures dans Athena ?

Avec des fonctions comme `current_date`, `date_add('day', -1, current_date)`, `date_diff('day', a, b)`, `date_trunc('month', ts)`, `date_format(ts, '%Y-%m-%d')`, `from_iso8601_timestamp(s)`, `parse_datetime(s, 'yyyy-MM-dd HH:mm')` et `ts AT TIME ZONE 'Europe/Paris'`.

#### Comment convertir des types en toute sécurité ?

`TRY_CAST(x AS integer)` renvoie `NULL` au lieu d'échouer sur une valeur invalide, et `try()` enveloppe des expressions susceptibles d'échouer. Utilisez-les sur des données texte brutes.

#### Comment gérer les valeurs `NULL` dans les agrégations et comparaisons ?

Les agrégations ignorent les `NULL` (sauf `count(*)`) ; les comparaisons avec `NULL` renvoient `NULL` : utilisez `IS NULL`, `coalesce`, `IS DISTINCT FROM` pour comparer en tenant compte des nulls, et méfiez-vous de `NOT IN` sur des colonnes qui contiennent des nulls.

#### Comment hacher des valeurs pour les pseudonymiser ?

Avec `to_hex(sha256(to_utf8(email)))` (de préférence avec un sel secret ou un HMAC via `hmac_sha256`), ce qui produit des pseudonymes stables qu'on peut encore joindre.

<!-- challenge -->

Une requête `WHERE discount <> 10` manque les lignes où la remise est absente. Pourquoi, et comment corriger ?

<!-- solution -->

Les comparaisons avec `NULL` renvoient `NULL` : ces lignes sont exclues. Utilisez `WHERE discount IS NULL OR discount <> 10`, ou `coalesce(discount, 0) <> 10` si absent signifie zéro.

<!-- takeaways -->

- Utilisez `TRY_CAST` sur les données sales du lake.
- Les comparaisons avec `NULL` écartent des lignes en silence.
- Des hachages salés pseudonymisent les identifiants.

<!-- unit: Patrons analytiques -->

<!-- goals -->

- Dédupliquer, classer et calculer des cumuls avec les fonctions de fenêtre.
- Pivoter des données et comparer des tables.

<!-- concept -->

Quelques patrons couvrent la plupart des questions analytiques. Les fonctions de fenêtre répondent aux questions « par groupe » sans écraser les lignes : dernier enregistrement par clé, top N par catégorie, totaux cumulés. L'agrégation conditionnelle remplace le `PIVOT` absent. Les opérations ensemblistes comparent deux versions d'une table.

Connaître le patron compte plus que la syntaxe, car la même forme revient d'un moteur à l'autre.

<!-- example -->

```sql
WITH ranked AS (
  SELECT *, row_number() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) AS rn
  FROM raw.customer_changes
)
SELECT * FROM ranked WHERE rn = 1;      -- latest version per customer
```

#### Comment dédupliquer des lignes dans Athena ?

Avec `row_number()` par clé ordonné par un horodatage, en gardant la première ligne par clé, dans une sous-requête ou une CTE, car Athena ne prend pas en charge `QUALIFY`.

#### Comment obtenir les N premières lignes par groupe ?

Utiliser `row_number()` ou `rank()` par groupe, ordonné selon la mesure, dans une sous-requête, et filtrer sur le rang dans la requête externe ; `max_by(x, y)` donne la valeur de `x` au maximum de `y` par groupe.

#### Comment calculer un cumul ou une moyenne mobile ?

Avec des fonctions de fenêtre : `sum(amount) OVER (PARTITION BY customer ORDER BY dt ROWS UNBOUNDED PRECEDING)` pour les cumuls et `avg(amount) OVER (ORDER BY dt ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)` pour une moyenne mobile sur 7 lignes.

#### À quoi servent `max_by` et `min_by` ?

À renvoyer la valeur d'une colonne sur la ligne où une autre colonne est maximale ou minimale, par exemple le dernier statut de chaque commande : `max_by(status, updated_at)`, sans fonction de fenêtre.

#### Comment pivoter des données dans Athena ?

Avec une agrégation conditionnelle, faute de mot-clé `PIVOT` : `sum(CASE WHEN month = 1 THEN amount END) AS janv`, ou `map_agg` pour construire une map clé-valeur.

#### Comment comparer deux tables pour trouver les différences ?

Avec `EXCEPT` dans les deux sens (`SELECT * FROM a EXCEPT SELECT * FROM b`) pour les différences de lignes, ou une jointure externe complète sur la clé en comparant les colonnes, utile pour valider des migrations.

<!-- challenge -->

Il vous faut le dernier pays de chaque client et sa dépense totale en une requête. Écrivez-en le cœur.

<!-- solution -->

`SELECT customer_id, max_by(country, updated_at) AS country, sum(amount) AS spend FROM orders GROUP BY customer_id`. `max_by` évite une étape de fenêtre séparée pour la dernière valeur.

<!-- takeaways -->

- `row_number()` gère déduplication et top N par groupe.
- L'agrégation conditionnelle pivote les données.
- `EXCEPT` dans les deux sens trouve les différences entre tables.

<!-- unit: Tableaux, séries et fonctions spécialisées -->

<!-- goals -->

- Utiliser les fonctions de tableaux, de maps et de séquences.
- Appliquer les patrons géospatiaux, d'échantillonnage et de réutilisation.

<!-- concept -->

La bibliothèque de fonctions de Trino va bien au-delà du SQL standard, et les données du lake en ont souvent besoin : tableaux et maps issus de JSON, calendriers avec des trous, coordonnées d'applications. Générer une série de dates est une astuce courante pour afficher les jours sans activité au lieu de les omettre.

La réutilisation complète la boîte à outils : les vues partagent la logique entre requêtes et les CTE l'organisent dans une requête.

<!-- example -->

```sql
SELECT d AS day, coalesce(count(o.order_id), 0) AS orders
FROM UNNEST(sequence(date '2026-10-01', date '2026-10-31', interval '1' day)) AS t(d)
LEFT JOIN sales.orders o ON date(o.created_at) = d
GROUP BY d ORDER BY d;
```

#### Quelles fonctions de tableaux et de maps sont utiles ?

`cardinality`, `contains`, `element_at`, `array_join`, `array_agg`, `filter`, `transform`, `reduce`, `map_keys`, `map_values` et `map_agg`, qui permettent de travailler sur des données imbriquées sans les déplier.

#### Comment générer une série de dates dans Athena ?

Avec `sequence` et `UNNEST` : `SELECT d FROM UNNEST(sequence(date '2026-01-01', date '2026-12-31', interval '1' day)) AS t(d)`, utile pour combler les trous des séries temporelles.

#### Comment faire des requêtes géospatiales dans Athena ?

Avec des fonctions géospatiales comme `ST_Point`, `ST_Contains`, `ST_Distance`, `ST_Within`, `ST_GeometryFromText` et `great_circle_distance`, par exemple pour compter des événements à l'intérieur de polygones.

#### Comment échantillonner des données dans Athena ?

`TABLESAMPLE BERNOULLI (1)` lit chaque ligne avec 1 % de probabilité (mais lit toutes les données), et `TABLESAMPLE SYSTEM (1)` échantillonne au niveau du fichier ou du split, ce qui peut réduire les données lues.

#### Comment écrire une logique SQL réutilisable dans Athena ?

Avec des vues pour la logique partagée, des CTE (`WITH`) pour la lisibilité au sein d'une requête, et des macros dbt quand on utilise dbt-athena.

<!-- challenge -->

Un collègue utilise `TABLESAMPLE BERNOULLI (1)` pour réduire le coût d'une requête exploratoire. Cela fonctionne-t-il ?

<!-- solution -->

Cela renvoie environ 1 % des lignes mais scanne toujours toutes les données : le coût ne baisse pas. Filtrez sur les partitions (par exemple un jour) ou utilisez `TABLESAMPLE SYSTEM` si un échantillonnage approximatif par fichiers convient.

<!-- takeaways -->

- Les fonctions de tableaux, maps et JSON gèrent les données imbriquées.
- `sequence` et `UNNEST` comblent les trous des séries de dates.
- L'échantillonnage ne réduit le coût que s'il saute des fichiers.

### Spark dans Athena et notebooks

<!-- unit: Spark serverless dans Athena -->

<!-- goals -->

- Expliquer ce qu'offre Athena pour Apache Spark.
- Choisir entre Athena SQL et Athena Spark.

<!-- concept -->

Certains travaux ne tiennent pas dans une instruction SQL : exploration itérative, bibliothèques Python, préparation pour le machine learning. Athena pour Apache Spark offre la même expérience serverless pour PySpark dans des notebooks, avec un démarrage en secondes sans cluster.

SQL reste le meilleur choix pour les requêtes et rapports ; Spark sert la logique qui demande un langage de programmation.

<!-- example -->

```python
df = spark.read.table("lake.orders").where("dt >= '2026-10-01'")
features = df.groupBy("customer_id").agg(F.count("*").alias("orders"), F.sum("amount").alias("spend"))
features.write.mode("overwrite").saveAsTable("ml.customer_features")
```

#### Qu'est-ce qu'Amazon Athena for Apache Spark ?

Une offre Spark serverless dans Athena qui permet d'exécuter du PySpark et du Spark SQL dans des notebooks ou via des API, avec un démarrage rapide et une facturation au DPU-heure, pour les charges qui demandent plus que du SQL.

#### Quand utiliser Athena Spark plutôt qu'Athena SQL ?

Pour des transformations complexes en Python, la préparation de données pour le machine learning, l'exploration itérative avec des DataFrames ou une logique malcommode en SQL ; le SQL reste plus simple et moins cher pour l'essentiel de l'analytique.

#### Quels langages les notebooks Athena prennent-ils en charge ?

PySpark et Spark SQL (avec des commandes magiques), avec des bibliothèques Python courantes disponibles et la possibilité d'en ajouter d'autres à la session.

<!-- challenge -->

Une data scientist veut préparer des features avec une logique de type pandas sur 300 Go de Parquet. Athena SQL ou Athena Spark ?

<!-- solution -->

Athena Spark : la logique est plus simple en PySpark et les données sont trop volumineuses pour pandas sur une machine. Les résultats peuvent être réécrits en tables du catalogue interrogées par Athena SQL.

<!-- takeaways -->

- Athena Spark exécute PySpark en serverless dans des notebooks.
- SQL pour les requêtes ; Spark pour la logique programmée.
- Les deux partagent le catalogue Glue.

<!-- unit: Sessions, facturation et catalogue -->

<!-- goals -->

- Comprendre comment les sessions Spark sont facturées et terminées.
- Lire et écrire des tables du catalogue depuis des sessions Spark.

<!-- concept -->

Une session Spark garde du calcul tant qu'elle est ouverte : le coût suit la durée de session, pas les octets scannés. Des timeouts d'inactivité terminent automatiquement les sessions, ce qui compte car les notebooks restent facilement ouverts.

Les sessions utilisent le même Glue Data Catalog que SQL : les tables écrites depuis Spark apparaissent dans Athena SQL et les deux styles partagent un lake.

<!-- example -->

| Modèle de facturation | Athena SQL | Athena Spark |
|---|---|---|
| Unité | Octets scannés (ou DPU réservées) | DPU-heures de la session |
| Moteur du coût | Données lues | Durée et taille de la session |

#### Comment les sessions Athena Spark sont-elles facturées ?

Au DPU-heure du calcul de la session, avec un dimensionnement automatique des executors et des délais d'inactivité qui terminent la session.

#### Comment Athena Spark accède-t-il au Data Catalog ?

Les sessions Spark d'Athena utilisent par défaut le Glue Data Catalog : on peut lire et écrire les tables du catalogue (y compris Iceberg) en Spark SQL ou en DataFrames.

<!-- challenge -->

Le coût mensuel d'Athena Spark est élevé, alors que les notebooks ne servent que quelques heures par jour. Que vérifiez-vous ?

<!-- solution -->

Les timeouts d'inactivité des sessions, si les utilisateurs laissent des sessions tourner, et la taille en DPU de chaque session. Réduisez le timeout et apprenez aux utilisateurs à fermer leurs sessions après usage.

<!-- takeaways -->

- Les sessions Spark sont facturées en DPU-heures.
- Les timeouts d'inactivité limitent les sessions oubliées.
- Spark et SQL partagent le catalogue Glue.

<!-- stage: Exploiter Athena -->

### Optimisation des performances

<!-- unit: Mesurer une requête -->

<!-- goals -->

- Mesurer les données scannées et lire les plans de requête.
- Connaître les leviers qui améliorent vitesse et coût.

<!-- concept -->

L'optimisation commence par la mesure. Chaque exécution enregistre les octets scannés et le temps passé en file, en planification et en exécution, et `EXPLAIN ANALYZE` montre où le temps est parti. La plupart des gains viennent d'une courte liste : lire moins (colonnes, partitions, formats), déplacer moins entre workers et éviter les étapes à un seul worker.

Un `LIMIT` n'est pas à lui seul un contrôle de coût ; seul le fait de lire moins l'est.

<!-- example -->

```sql
EXPLAIN ANALYZE
SELECT store_id, sum(amount) FROM sales.orders
WHERE dt = '2026-10-17' GROUP BY store_id;
-- check: input bytes per stage, pruned partitions, time per operator
```

#### Quels sont les principaux leviers pour rendre les requêtes Athena plus rapides et moins chères ?

Formats en colonnes compressés, partitionnement selon les filtres courants (ou projection), fichiers de 128 Mo à 1 Go, sélection des seules colonnes utiles, filtres sur les colonnes de partition, tri ou bucketing selon les filtres courants, Iceberg avec compaction, statistiques de tables et réutilisation des résultats.

#### Comment voir combien de données une requête a lues ?

Dans la console après exécution, dans les statistiques de `GetQueryExecution` (`DataScannedInBytes`), dans les métriques CloudWatch du workgroup et dans la sortie d'`EXPLAIN ANALYZE` par stage.

#### Que montrent `EXPLAIN` et `EXPLAIN ANALYZE` ?

`EXPLAIN` montre le plan distribué ou logique sans exécuter la requête : lectures, filtres poussés, jointures et leur distribution. `EXPLAIN ANALYZE` exécute la requête et indique les lignes, les données lues et le temps réels par stage, ce qui montre où part le temps.

#### Quel est l'effet de `LIMIT` sur le coût ?

Sur les tables de style Hive, un `LIMIT` sans filtre peut s'arrêter plus tôt mais lire tout de même de nombreux fichiers ; il ne garantit pas un faible coût. Les filtres de partition sont le moyen fiable de limiter la lecture.

<!-- challenge -->

Une requête scanne 800 Go alors qu'elle filtre un seul jour. Que cherchez-vous dans `EXPLAIN` ?

<!-- solution -->

Si le filtre de partition apparaît dans le scan (élagage), ou s'il est appliqué après le scan à cause d'une fonction ou d'un décalage de type sur la colonne de partition. Vérifiez aussi que la table est bien partitionnée ou projetée.

<!-- takeaways -->

- Mesurez d'abord octets scannés et temps par étape.
- `EXPLAIN ANALYZE` montre où vont temps et données.
- `LIMIT` ne garantit pas de scanner moins.

<!-- unit: Jointures et distribution des données -->

<!-- goals -->

- Écrire des jointures que l'optimiseur exécute efficacement.
- Gérer le skew et l'absence de statistiques.

<!-- concept -->

Les jointures distribuées diffusent une petite table à chaque worker ou redistribuent les deux côtés par clé. L'optimiseur choisit selon les statistiques ; sans elles, il suit l'ordre d'écriture : la table la plus grosse d'abord, la plus petite en dernier.

Le skew casse les deux stratégies : quand quelques clés concentrent la plupart des lignes, quelques workers reçoivent l'essentiel du travail. Filtrer ou séparer les clés chaudes aide généralement plus que n'importe quel réglage.

<!-- example -->

```sql
-- largest table first, small dimension last (broadcast-friendly)
SELECT f.order_id, d.region
FROM sales.orders f
JOIN ref.stores d ON f.store_id = d.store_id
WHERE f.dt = '2026-10-17';
```

#### Dans quel ordre placer les tables dans une jointure ?

Le moteur v3 dispose d'un optimiseur basé sur les coûts qui peut réordonner les jointures quand des statistiques existent dans le catalogue Glue. Sans statistiques, placez la plus grande table en premier (à gauche) et les plus petites à droite, car le côté droit est construit en mémoire et distribué aux workers.

#### Quels types de distribution de jointure existent ?

Les jointures broadcast envoient la petite table de droite à tous les workers (rapide si elle est petite) ; les jointures partitionnées répartissent les deux côtés par hachage (nécessaire pour deux grandes tables). L'optimiseur choisit selon les statistiques.

#### En quoi les statistiques de tables aident-elles Athena ?

Les statistiques de colonnes stockées dans le catalogue Glue (calculées par Glue) permettent à l'optimiseur basé sur les coûts de choisir l'ordre et la distribution des jointures, ce qui améliore les requêtes complexes sans changer le code.

#### Quel est l'impact du déséquilibre des données sur les jointures et agrégations Athena ?

Quelques clés concentrant la plupart des lignes surchargent des workers isolés et peuvent provoquer des erreurs « exhausted resources ». Filtrez les clés chaudes (souvent les nulls), traitez-les à part ou utilisez des agrégations approximatives.

<!-- challenge -->

Une jointure sur `customer_id` échoue avec « exhausted resources », et 30 % des lignes ont `customer_id = 0` (invités). Que faites-vous ?

<!-- solution -->

Traiter la clé chaude à part : retirer `customer_id = 0` de la jointure et gérer les invités dans une autre branche, puis réunir avec `UNION ALL`. Générer aussi des statistiques de table pour que l'optimiseur choisisse le bon type de jointure.

<!-- takeaways -->

- Mettez les grosses tables en premier sans statistiques.
- Diffusez les petites tables ; redistribuez les grosses.
- Les clés à skew exigent un traitement spécial.

<!-- unit: Opérations gourmandes en mémoire -->

<!-- goals -->

- Reconnaître les opérations qui concentrent le travail sur un worker.
- Remplacer les calculs exacts par des approximations quand c'est acceptable.

<!-- concept -->

Certaines opérations SQL doivent voir toutes les lignes à la fois : tris globaux, comptages distincts exacts, fenêtres sans partition, déduplication d'une union. Dans un moteur distribué, ces étapes concentrent les données sur peu de workers, d'où les erreurs « exhausted resources ».

Les remèdes : ajouter de la structure (partitionner les fenêtres, limiter les tris), accepter l'approximation quand le métier le permet et éviter les déduplications inutiles.

<!-- example -->

```sql
SELECT dt,
       approx_distinct(user_id) AS users,            -- ~2% error, small memory
       approx_percentile(latency_ms, 0.95) AS p95
FROM logs.requests
WHERE dt >= '2026-10-01'
GROUP BY dt;
```

#### Pourquoi un `ORDER BY` sans `LIMIT` nuit-il aux performances ?

Un tri global exige d'envoyer toutes les lignes à un seul worker pour l'ordonnancement final, ce qui est lent et peut échouer avec « exceeded resources ». Ajoutez un `LIMIT` (le top-N est efficace) ou ne triez que le nécessaire.

#### Qu'est-ce que « Query exhausted resources at this scale factor » ?

Une erreur quand une requête a besoin de plus de mémoire que disponible pour une opération (jointures énormes, `GROUP BY` sur de très nombreux groupes, `DISTINCT` sur beaucoup de colonnes, `ORDER BY` de tout, tableaux très volumineux). Solutions : filtrer plus tôt, réduire les colonnes, utiliser des fonctions approximatives, découper la requête, matérialiser des étapes intermédiaires avec `CTAS`, ou utiliser des réservations de capacité.

#### Quand utiliser des fonctions approximatives ?

`approx_distinct`, `approx_percentile` et `approx_most_frequent` renvoient des estimations à faible erreur en utilisant bien moins de mémoire que `count(DISTINCT)` ou les percentiles exacts, ce qui convient aux dashboards et à l'exploration.

#### Pourquoi `count(DISTINCT x)` sur une énorme table échoue-t-il ou est-il lent ?

Il faut garder toutes les valeurs distinctes en mémoire sur l'ensemble des workers. Utilisez `approx_distinct(x)` pour une estimation, ou pré-agrégez les comptes distincts par partition puis combinez-les.

#### Comment les fonctions de fenêtre affectent-elles les performances d'Athena ?

Les fonctions de fenêtre partitionnent et trient les données ; une fenêtre sur toute la table (sans `PARTITION BY`) impose un seul worker. Partitionnez toujours les fenêtres par une clé et filtrez les données d'abord.

#### Quel est l'effet de `UNION` par rapport à `UNION ALL` ?

`UNION` supprime les doublons, ce qui exige une étape d'agrégation supplémentaire ; `UNION ALL` se contente de concaténer. Utilisez `UNION ALL` quand les doublons sont impossibles ou acceptables.

#### Comment accélérer les recherches `LIKE` sur de grandes colonnes texte ?

Filtrer d'abord sur les partitions, n'utiliser `regexp_like` qu'en cas de besoin, et envisager d'extraire pendant l'ETL les champs recherchés dans des colonnes séparées, ou un service de recherche comme OpenSearch pour du plein texte.

<!-- challenge -->

Un rapport quotidien calcule les utilisateurs distincts exacts sur 90 jours et échoue souvent. L'équipe produit n'a besoin que d'une tendance. Que changez-vous ?

<!-- solution -->

Utiliser `approx_distinct(user_id)` par jour, qui demande peu de mémoire avec environ 2 % d'erreur. Si des chiffres exacts deviennent nécessaires, précalculer les ensembles distincts quotidiens dans une table de synthèse.

<!-- takeaways -->

- Tris globaux, distincts exacts et fenêtres sans partition coûtent cher.
- Les fonctions approximatives échangent une petite erreur contre l'échelle.
- Préférez `UNION ALL` sauf besoin de dédupliquer.

<!-- unit: Réutiliser et précalculer les résultats -->

<!-- goals -->

- Réutiliser des résultats récents et précalculer les agrégats fréquents.
- Accélérer les tableaux de bord qui interrogent Athena.

<!-- concept -->

La requête la moins chère est celle qu'on ne lance pas. Les tableaux de bord renvoient sans cesse les mêmes requêtes : mettre en cache les résultats récents et précalculer les agrégats courants économise coût et attente. La réutilisation des résultats couvre les requêtes identiques ; les tables de synthèse couvrent la même question posée de façons un peu différentes.

La question de conception est la fraîcheur : jusqu'à quel âge une réponse reste-t-elle acceptable ?

<!-- example -->

```sql
-- summary table refreshed hourly; the dashboard reads it instead of raw events
INSERT INTO marts.sales_hourly
SELECT date_trunc('hour', created_at) AS hour, store_id, sum(amount) AS revenue
FROM sales.orders WHERE dt = '2026-10-17'
GROUP BY 1, 2;
```

#### Qu'est-ce que la réutilisation des résultats de requêtes ?

Une fonction où Athena renvoie les résultats d'une requête précédente si la même requête a été exécutée récemment (dans un âge maximal défini, jusqu'à 7 jours) et que les données n'ont pas changé (pour les tables compatibles), sans relire les données.

#### Comment optimiser les requêtes sur une combinaison de dimensions très interrogée ?

Précalculer des agrégats dans une table de synthèse (`CTAS` ou `INSERT` planifié), partitionnée par date, et pointer les dashboards vers elle plutôt que vers la table brute.

#### Un dashboard QuickSight sur Athena est lent et coûteux. Que changez-vous ?

Pré-agréger dans une table de synthèse rafraîchie selon un planning, utiliser SPICE de QuickSight pour mettre les données en cache, s'assurer que le dashboard applique des filtres de partition, convertir les tables sources en Parquet ou Iceberg avec compaction, et envisager des réservations de capacité pour une concurrence prévisible.

<!-- challenge -->

Un tableau de bord de 10 graphiques interroge des événements bruts et met 40 secondes à charger. Les données ne changent qu'une fois par heure. Que proposez-vous ?

<!-- solution -->

Construire des tables de synthèse horaires pour les graphiques, les rafraîchir selon un calendrier et y brancher le tableau de bord ; activer la réutilisation des résultats ou le cache de l'outil de BI (SPICE) avec une fraîcheur d'une heure.

<!-- takeaways -->

- La réutilisation renvoie des réponses en cache aux requêtes identiques.
- Les tables de synthèse servent les agrégations répétées à faible coût.
- Décidez d'abord de la fraîcheur, puis du cache.

<!-- unit: Capacité et limites de S3 -->

<!-- goals -->

- Décider quand les réservations de capacité sont rentables.
- Reconnaître le throttling S3 comme une limite de performance.

<!-- concept -->

Athena à la demande partage la capacité avec d'autres clients et facture au scan. Les réservations de capacité achètent un traitement dédié pour des charges régulières, échangeant le paiement par requête contre un coût et une concurrence prévisibles.

Sous le moteur, S3 a ses propres limites par préfixe. Des requêtes sur des millions de petits fichiers peuvent être freinées quelle que soit la capacité de calcul : l'organisation des fichiers est aussi une question de débit.

<!-- example -->

| Situation | Meilleur choix |
|---|---|
| Quelques requêtes ad hoc par jour | À la demande |
| BI toute la journée, des centaines d'utilisateurs | Réservation de capacité |
| Erreurs `SlowDown` sur de nombreux petits fichiers | Compacter, répartir les préfixes |

#### Que sont les réservations de capacité ?

Une capacité de traitement dédiée achetée en DPU (pour une durée minimale, puis à la minute) et affectée à des workgroups. Les requêtes de ces workgroups s'exécutent sur la capacité réservée, facturée au DPU-heure plutôt qu'au To lu, avec un coût et une concurrence prévisibles.

#### Quand les réservations de capacité valent-elles la peine ?

Quand le volume de requêtes est élevé et régulier (dashboards BI intensifs, nombreux utilisateurs simultanés), quand il faut une concurrence garantie pour des charges critiques, ou quand le coût au To dépasse le prix de la capacité réservée.

#### Pourquoi le throttling S3 peut-il ralentir les requêtes Athena ?

S3 accepte des débits élevés par préfixe, mais des requêtes sur des millions de petits fichiers dans un même préfixe peuvent recevoir des erreurs `SlowDown` (503). Des fichiers moins nombreux et plus gros, répartis sur plusieurs préfixes (partitions), l'évitent.

<!-- challenge -->

Votre facture à la demande atteint 30 000 USD par mois, surtout des requêtes BI 8 heures par jour. Comment évaluez-vous une réservation de capacité ?

<!-- solution -->

Estimer les DPU nécessaires à la concurrence de pointe d'après le volume actuel, les chiffrer pour les heures ouvrées et comparer à la dépense à la demande. N'affecter que le workgroup BI à la réservation et garder l'ad hoc à la demande.

<!-- takeaways -->

- Les réservations offrent capacité dédiée et coût prévisible.
- Elles paient pour des charges régulières et volumineuses.
- Beaucoup de petits fichiers peuvent heurter les limites de requêtes S3.

### Workgroups, maîtrise des coûts et supervision

<!-- unit: Les workgroups comme garde-fous -->

<!-- goals -->

- Fixer des limites par requête et par workgroup.
- Imposer des réglages et répartir les coûts par équipe.

<!-- concept -->

Dans un service facturé au scan, une requête négligente peut coûter plus qu'un mois d'usage normal. Les workgroups encadrent ce risque : chaque équipe ou application a ses réglages, son emplacement de résultats et son chiffrement imposés, et des limites qui annulent ou alertent sur les gros scans.

Les workgroups rendent aussi les coûts visibles, car tags et métriques rattachent chaque requête à son propriétaire.

<!-- example -->

```bash
aws athena update-work-group --work-group analysts \
  --configuration-updates 'EnforceWorkGroupConfiguration=true,BytesScannedCutoffPerQuery=107374182400'
# cancels any query scanning more than 100 GB
```

#### Comment limiter les coûts par équipe ?

Créer un workgroup par équipe ou application avec une limite de données par requête (qui annule les requêtes dépassant un seuil) et des limites globales par période qui déclenchent des alarmes, imposer les réglages du workgroup pour que les utilisateurs ne puissent pas les surcharger, et taguer les workgroups pour l'imputation des coûts.

#### Que signifie « override client-side settings » pour un workgroup ?

Une fois activé, l'emplacement des résultats, le chiffrement et les autres réglages du workgroup s'appliquent à toutes les requêtes, en ignorant ce que précisent les clients, ce qui impose la gouvernance.

#### Quelle différence entre une limite par requête et une limite de workgroup ?

Un contrôle par requête annule toute requête qui lit plus que le seuil. Les contrôles de workgroup mesurent le total lu sur une période et déclenchent des alarmes CloudWatch ou des notifications SNS, sans annuler de requêtes.

#### Comment éviter les requêtes incontrôlées ?

Avec des limites de données par requête dans les workgroups, des timeouts, de la formation sur les filtres de partition, des vues qui imposent un filtre de partition, et des réservations de capacité pour les charges prévisibles.

#### Comment imputer les coûts d'Athena aux équipes ?

Avec des workgroups séparés par équipe, tagués avec des tags d'imputation des coûts, en analysant les coûts dans Cost Explorer par tag ; avec des réservations de capacité, en affectant les workgroups aux réservations par équipe.

<!-- challenge -->

La requête d'un stagiaire a scanné 40 To pendant un week-end. Quels garde-fous ajoutez-vous ?

<!-- solution -->

Placer stagiaires et analystes dans un workgroup avec une limite par requête (par exemple 1 To) et une alerte quotidienne, imposer les réglages du workgroup et exiger des filtres de partition via des vues ou de la formation.

<!-- takeaways -->

- Les limites par requête annulent les gros scans.
- Les réglages imposés du workgroup priment sur les clients.
- Des workgroups tagués attribuent les coûts aux équipes.

<!-- unit: Surveiller usage et échecs -->

<!-- goals -->

- Suivre scans, durées et échecs dans le temps.
- Enquêter méthodiquement sur une hausse de coût.

<!-- concept -->

Athena garde l'historique des requêtes 45 jours et les workgroups publient des métriques, mais aucun ne répond seul à « pourquoi les coûts ont-ils changé ? ». Exporter le détail des requêtes permet de trouver les plus chères et leur tendance.

N'oubliez pas les coûts cachés : les requêtes S3 sont facturées à part, si bien que les tables à nombreux petits fichiers coûtent plus que ce que montre la facture Athena.

<!-- example -->

```sql
-- after exporting query executions to a table
SELECT workgroup, query_hash, sum(data_scanned_bytes) / 1e12 AS tb
FROM ops.athena_queries
WHERE day >= current_date - interval '7' day
GROUP BY 1, 2 ORDER BY tb DESC LIMIT 20;
```

#### Comment superviser l'usage d'Athena ?

Avec les métriques CloudWatch par workgroup (données lues, durée des requêtes, temps d'attente, requêtes en échec), l'historique des requêtes (`ListQueryExecutions`, console), CloudTrail pour les appels d'API, et des rapports de coûts par tags.

#### Combien de temps l'historique des requêtes est-il conservé ?

Athena conserve l'historique des requêtes 45 jours. Pour une rétention ou une analyse plus longue, exportez les détails d'exécution (par exemple via des événements EventBridge ou un job planifié appelant `GetQueryExecution`) vers S3.

#### Comment trouver les requêtes les plus coûteuses ?

Dans l'historique ou les données d'exécution exportées, trier par `DataScannedInBytes` ; puis vérifier si elles filtrent sur les partitions, lisent du CSV ou du JSON, ou sélectionnent trop de colonnes.

#### Comment les requêtes S3 influent-elles sur les coûts d'Athena ?

Le prix au To d'Athena n'inclut pas les requêtes GET et LIST de S3, facturées par S3. Des tables composées d'un nombre énorme de petits fichiers peuvent générer des coûts de requêtes importants en plus de la facture Athena.

#### Comment suivre les échecs de requêtes ?

Avec les métriques CloudWatch de requêtes en échec par workgroup, les événements EventBridge « Athena Query State Change » routés vers des alertes, et l'historique des requêtes avec les messages d'erreur.

#### Votre facture Athena a doublé. Comment enquêtez-vous ?

Je vérifie les données lues par workgroup dans CloudWatch, je trouve les requêtes les plus lourdes en octets dans l'historique, et je cherche de nouveaux dashboards lançant des requêtes non filtrées, des `SELECT *` sur des tables larges, des tables en CSV ou JSON, et des filtres de partition devenus inopérants (par exemple une fonction sur la colonne de partition). Puis je corrige formats et filtres et j'ajoute des limites par requête.

<!-- challenge -->

Les coûts ont augmenté de 40 % ce mois-ci sans nouvelle équipe. Citez les trois premiers points à vérifier.

<!-- solution -->

Les requêtes les plus scannées ce mois-ci contre le précédent, les requêtes planifiées nouvelles ou modifiées (souvent la fréquence de rafraîchissement d'un tableau de bord) et les tables dont les filtres de partition n'élaguent plus après un changement de schéma ou d'organisation.

<!-- takeaways -->

- Exportez l'historique des requêtes pour l'analyser à long terme.
- Triez par octets scannés pour trouver les requêtes chères.
- Les coûts de requêtes S3 sont hors de la facture Athena.

### Requêtes fédérées et connecteurs

<!-- unit: Interroger au-delà de S3 -->

<!-- goals -->

- Expliquer comment les requêtes fédérées atteignent bases de données et autres sources.
- Peser leur commodité face aux performances et à la charge.

<!-- concept -->

Les requêtes fédérées permettent à une instruction SQL de joindre des données du lake à des données vivantes en base ou dans d'autres services. Un connecteur Lambda traduit une partie de la requête pour la source, pousse les filtres quand il peut et renvoie des lignes à Athena.

La commodité a un prix : la source travaille vraiment, la Lambda a des limites et des scans analytiques peuvent nuire à une base opérationnelle. La fédération convient aux petites recherches et aux jointures occasionnelles, pas aux gros scans réguliers.

<!-- example -->

```sql
SELECT o.order_id, o.amount, c.segment
FROM lake.orders o
JOIN rds_pg.public.customers c ON o.customer_id = c.id
WHERE o.dt = '2026-10-17';
```

#### Qu'est-ce qu'Athena Federated Query ?

Une fonction qui permet à Athena d'interroger des données hors de S3, comme DynamoDB, RDS et Aurora (MySQL, PostgreSQL), Redshift, DocumentDB, OpenSearch, CloudWatch Logs, Snowflake, BigQuery et bien d'autres, via des connecteurs de sources de données exécutés en fonctions AWS Lambda (ou en connexions Glue gérées).

#### Comment fonctionnent les connecteurs fédérés ?

La Lambda du connecteur reçoit une partie du plan de requête, lit les données de la source (en poussant filtres et projections quand c'est possible) et les renvoie à Athena au format Apache Arrow, qui les joint et les agrège ensuite avec d'autres données.

#### Quels sont les inconvénients des requêtes fédérées ?

Les performances dépendent de la source et de la Lambda (timeouts, mémoire, concurrence), les requêtes peuvent charger les bases opérationnelles, la poussée de prédicats est limitée pour certaines sources, et on paie Lambda en plus des données lues. Pour un usage fréquent et intensif, répliquez les données dans S3.

#### Comment joindre des données S3 à une table RDS ?

Enregistrer le connecteur RDS comme source de données (par exemple `rds_pg`), puis interroger `SELECT … FROM lake.orders o JOIN rds_pg.public.customers c ON o.customer_id = c.id`, en gardant le côté RDS petit grâce à des filtres.

#### Comment interroger DynamoDB avec Athena ?

Avec le connecteur DynamoDB, qui scanne ou interroge la table (en consommant de la capacité de lecture) ; pour de grosses requêtes analytiques, exportez la table vers S3 (export DynamoDB) et interrogez l'export.

<!-- challenge -->

Un rapport quotidien joint une table de 2 To du lake à un scan complet d'une table DynamoDB de production, et l'application ralentit à ce moment. Que changez-vous ?

<!-- solution -->

Cesser de scanner DynamoDB en direct : l'exporter vers S3 (export DynamoDB vers S3 en Parquet ou job quotidien) et joindre la copie exportée. Garder la fédération pour des recherches petites et filtrées.

<!-- takeaways -->

- Les connecteurs tournent dans Lambda et poussent les filtres.
- La fédération est pratique mais charge la source.
- Exportez les grosses sources vers S3 pour l'analytique régulière.

<!-- unit: Connecteurs et fonctions externes -->

<!-- goals -->

- Déployer et exploiter des connecteurs fédérés.
- Appeler des UDF Lambda et des modèles SageMaker depuis SQL.

<!-- concept -->

Connecteurs et fonctions étendent Athena avec du code que vous exécutez. Ce sont des fonctions Lambda, qui héritent de leurs limites : taille de réponse (d'où le spill bucket), timeouts et concurrence. Traitez-les comme tout service : déployez-les en code, avec des rôles au moindre privilège, et surveillez-les.

Les fonctions externes apportent au SQL une logique absente du moteur, du déchiffrement au scoring de modèles, mais chaque ligne traverse un appel réseau.

<!-- example -->

```sql
USING EXTERNAL FUNCTION predict_churn(tenure int, spend double)
  RETURNS double SAGEMAKER 'churn-endpoint'
SELECT customer_id, predict_churn(tenure, spend) AS churn_score
FROM marts.customers WHERE dt = '2026-10-17';
```

#### Comment déployer un connecteur fédéré ?

Depuis la console Athena (création d'une source de données), qui déploie la Lambda du connecteur depuis l'AWS Serverless Application Repository ou utilise des connexions Glue, avec un bucket de spill S3 pour les gros résultats et les bons réglages IAM et VPC.

#### À quoi sert le bucket de spill ?

Un emplacement S3 où le connecteur écrit les données qui dépassent les limites de taille de réponse de Lambda, qu'Athena lit ensuite. Il doit être chiffré et avoir une règle de cycle de vie.

#### Peut-on écrire son propre connecteur ?

Oui, avec l'Athena Query Federation SDK (Java), en implémentant les gestionnaires de métadonnées et d'enregistrements pour sa source, déployé en fonction Lambda.

#### Que sont les fonctions définies par l'utilisateur dans Athena ?

Des fonctions scalaires implémentées dans une fonction Lambda (Java) et appelées avec `USING EXTERNAL FUNCTION`, utilisées pour une logique absente du SQL, comme appeler un service interne ou un déchiffrement personnalisé.

#### Athena peut-il appeler des modèles de machine learning ?

Oui, avec `USING EXTERNAL FUNCTION … SAGEMAKER 'nom-endpoint'`, qui envoie des lignes à un endpoint SageMaker pour faire de l'inférence au sein d'une requête.

<!-- challenge -->

Une requête fédérée échoue avec une erreur de taille de réponse Lambda sur de gros résultats. Que manque-t-il ?

<!-- solution -->

Un spill bucket, ou un dans lequel le connecteur peut écrire. Configurez un emplacement de spill S3 avec une règle de cycle de vie supprimant les anciens objets, et accordez-y l'accès au rôle du connecteur.

<!-- takeaways -->

- Connecteurs et UDF sont des Lambda, avec leurs limites.
- Le spill bucket gère les grosses réponses du connecteur.
- Les fonctions externes ajoutent une logique par ligne, au prix du réseau.

### Sécurité et gouvernance

<!-- unit: Contrôle d'accès avec IAM et Lake Formation -->

<!-- goals -->

- Contrôler qui interroge quelles tables, colonnes et lignes.
- Masquer ou exclure les données sensibles.

<!-- concept -->

Avec IAM seul, l'accès aux tables est en réalité un accès S3 : qui peut lire les fichiers peut lire toute table posée dessus. Lake Formation remonte le contrôle aux tables, colonnes et lignes, et fournit à Athena des identifiants temporaires pour exactement ce que l'utilisateur peut voir. Des règles fines comme « les analystes UE voient les lignes UE sans e-mail » deviennent possibles.

Le masquage ajoute une couche, via colonnes exclues, vues qui masquent ou copies masquées.

<!-- example -->

```sql
-- Lake Formation data filter (defined in LF): row filter + excluded columns
--   table: lake.customers  row filter: country IN ('DE','FR','ES')  exclude: email, phone
SELECT customer_id, country, segment FROM lake.customers;   -- analyst sees only allowed data
```

#### Comment contrôler l'accès à Athena ?

Par des politiques IAM sur les actions Athena et les workgroups, des droits S3 sur les données et les emplacements de résultats, des droits sur le Glue Data Catalog (bases, tables) et, pour un contrôle fin, des droits Lake Formation sur les bases, tables, colonnes, lignes et cellules.

#### Comment Lake Formation fonctionne-t-il avec Athena ?

Athena vérifie les droits Lake Formation de l'appelant et ne renvoie que les colonnes et lignes autorisées, en lisant S3 avec des identifiants temporaires fournis par Lake Formation : les utilisateurs n'ont pas besoin d'accès direct à S3 sur les données.

#### Comment restreindre les données S3 qu'un utilisateur peut interroger ?

Accorder l'accès aux tables via Lake Formation (sans droits S3 directs), ou, avec IAM, limiter l'accès S3 à des préfixes précis et l'accès Glue à des bases et tables précises.

#### Qu'est-ce qu'un data filter Lake Formation ?

Une définition de sécurité au niveau ligne et cellule pour une table (une expression de filtre de lignes plus des colonnes incluses ou exclues) accordée à des principals ; Athena l'applique à la requête.

#### Comment masquer des colonnes sensibles dans Athena ?

Les exclure via les droits de colonnes Lake Formation, fournir des vues qui les hachent ou les masquent, ou stocker des copies masquées dans une table curée séparée pour un accès large.

<!-- challenge -->

Les analystes doivent interroger une table clients sans voir les e-mails, et les analystes allemands seulement les clients allemands. Comment le configurez-vous ?

<!-- solution -->

Enregistrer l'emplacement dans Lake Formation, créer un data filter excluant `email` avec un filtre de lignes `country = 'DE'`, et l'accorder au rôle des analystes allemands. Retirer leur accès S3 direct à l'emplacement de la table.

<!-- takeaways -->

- IAM seul, c'est un accès au niveau fichier.
- Lake Formation accorde tables, colonnes et lignes.
- Les data filters combinent sécurité des lignes et des colonnes.

<!-- unit: Chiffrement, réseau et audit -->

<!-- goals -->

- Chiffrer données et résultats et garder le trafic privé.
- Partager entre comptes et auditer l'usage.

<!-- concept -->

La sécurité couvre aussi le chemin autour des requêtes. Données et résultats doivent être chiffrés avec des clés que vous contrôlez. Le trafic peut rester dans votre réseau grâce aux VPC endpoints. L'accès entre comptes passe par des catalogues partagés plutôt que par des copies.

L'audit boucle la boucle : CloudTrail enregistre qui a exécuté quoi, ce qui compte dès qu'il y a des tables sensibles.

<!-- example -->

```bash
aws athena update-work-group --work-group finance --configuration-updates \
 'ResultConfigurationUpdates={OutputLocation=s3://athena-results-finance/,EncryptionConfiguration={EncryptionOption=SSE_KMS,KmsKey=alias/finance}}'
```

#### Comment chiffrer les données d'Athena ?

Les données dans S3 peuvent être chiffrées en SSE-S3, SSE-KMS ou KMS côté client ; Athena lit les données chiffrées de façon transparente avec les bons droits KMS. Les résultats peuvent être chiffrés (SSE-S3, SSE-KMS, CSE-KMS) par workgroup, et les données en transit utilisent TLS.

#### Comment interroger des données d'un autre compte AWS ?

Via le partage inter-comptes de Lake Formation (resource links), l'accès inter-comptes au catalogue Glue enregistré comme source de données, ou des politiques de bucket donnant au rôle requérant l'accès aux données et à leur clé KMS.

#### Comment auditer l'usage d'Athena ?

CloudTrail enregistre les appels d'API (qui a lancé quelle requête, avec son texte), Lake Formation journalise l'accès aux données, et les journaux d'accès serveur S3 ou les événements de données CloudTrail enregistrent les lectures d'objets.

#### Comment utiliser Athena depuis un réseau privé ?

Via des endpoints VPC d'interface pour Athena (et pour Glue, S3 et KMS selon les besoins), pour que le trafic ne passe pas par Internet ; des politiques d'endpoint peuvent restreindre l'usage.

#### Comment donner à un outil BI un accès sécurisé à Athena ?

Créer un rôle ou utilisateur IAM dédié (de préférence fédéré via IAM Identity Center ou OAuth pour le pilote), limité à un workgroup, aux tables nécessaires via Lake Formation et à l'emplacement de résultats, et se connecter via le pilote JDBC/ODBC.

<!-- challenge -->

Un outil de BI se connecte avec un utilisateur IAM dont les clés n'expirent jamais et qui a des droits d'administrateur. Comment corriger ?

<!-- solution -->

Créer un rôle dédié (ou une identité fédérée via le driver) limité à un workgroup et aux tables nécessaires via Lake Formation, utiliser des identifiants temporaires et supprimer les clés de longue durée.

<!-- takeaways -->

- Chiffrez données et résultats avec KMS.
- Partagez entre comptes par catalogues, pas par copies.
- CloudTrail enregistre qui a lancé chaque requête.

### Dépannage

<!-- unit: Résultats manquants ou faux -->

<!-- goals -->

- Diagnostiquer des requêtes sans lignes, avec des `NULL` ou des doublons.
- Corriger l'enregistrement des partitions et les problèmes de timestamps.

<!-- concept -->

Quand les résultats semblent faux dans Athena, la cause est généralement le contrat entre table et fichiers, pas le SQL. Partitions non enregistrées, emplacement légèrement erroné, SerDe qui ne parse pas les valeurs ou fichiers écrits deux fois produisent des réponses plausibles mais fausses.

Partez des fichiers : listez l'emplacement, vérifiez les partitions, regardez les valeurs brutes avec `"$path"`, puis corrigez la définition ou le pipeline.

<!-- example -->

```sql
SHOW PARTITIONS sales.orders;                 -- is today's partition there?
SELECT "$path", count(*) FROM sales.orders WHERE dt = '2026-10-17' GROUP BY 1;  -- duplicate files?
```

#### Une requête renvoie zéro ligne alors que les fichiers existent. Que vérifiez-vous ?

Si les partitions sont enregistrées (ou si la projection est correctement configurée), si le `LOCATION` et le modèle d'emplacement correspondent aux vrais chemins, si le SerDe et les colonnes correspondent au format, et si les fichiers sont dans des sous-dossiers que la table n'inclut pas.

#### Pourquoi `MSCK REPAIR TABLE` n'ajoute-t-il aucune partition ?

Les dossiers ne sont pas de style Hive (`cle=valeur`), les noms de clés ne correspondent pas aux colonnes de partition (la casse compte), l'emplacement est faux, ou la projection de partitions est activée sur la table.

#### Pourquoi des nombres apparaissent-ils en `NULL` depuis une table CSV ?

Les valeurs contiennent des caractères non analysables (séparateurs de milliers, symboles monétaires, guillemets avec `LazySimpleSerDe`, chaînes vides), ou les colonnes sont décalées parce qu'un champ contient le délimiteur. Utilisez `OpenCSVSerDe`, nettoyez les données, ou lisez en texte et appliquez `TRY_CAST`.

#### Pourquoi une requête sur des horodatages renvoie-t-elle des résultats faux ?

Des horodatages stockés sous forme de chaînes dans des formats différents, une confusion de fuseaux horaires (les timestamps sans fuseau sont souvent interprétés en UTC), ou des encodages de timestamps Parquet différents selon les écrivains. Analysez explicitement avec `from_iso8601_timestamp` ou `parse_datetime` et convertissez les fuseaux avec `AT TIME ZONE`.

#### Les résultats contiennent des doublons après la relance d'un pipeline. Pourquoi ?

Le pipeline a utilisé `INSERT INTO` sur une table Hive sans supprimer la sortie précédente, ou des fichiers ont été écrits deux fois au même emplacement. Rendez les écritures idempotentes (écraser les partitions, `MERGE` Iceberg) et dédupliquez les partitions concernées.

<!-- challenge -->

Les données d'hier sont dans S3 sous `s3://lake/orders/2026/10/17/`, mais `WHERE dt = '2026-10-17'` ne renvoie rien. Cause probable et correction ?

<!-- solution -->

Le chemin n'est pas de style Hive : ni `MSCK REPAIR` ni le catalogue ne connaissent la partition. Ajoutez-la avec `ALTER TABLE ADD PARTITION ... LOCATION`, ou configurez la projection avec un modèle d'emplacement correspondant à `${year}/${month}/${day}`.

<!-- takeaways -->

- Vérifiez partitions et emplacements avant le SQL.
- Les erreurs de parsing deviennent des `NULL` en silence.
- Les doublons signalent souvent des écritures non idempotentes.

<!-- unit: Lire les erreurs Hive -->

<!-- goals -->

- Interpréter les erreurs `HIVE_*` et de permission courantes.
- Localiser le fichier ou l'objet qui les provoque.

<!-- concept -->

Les messages d'erreur d'Athena nomment la couche en échec. Les erreurs de décalage de schéma pointent vers le catalogue, celles de curseur et de données invalides vers les fichiers, et un accès refusé peut venir de cinq couches de permissions. Lire l'erreur d'abord évite de deviner.

La plupart des erreurs au niveau fichier se règlent en trouvant le fichier fautif avec `"$path"` puis en le déplaçant ou en le corrigeant.

<!-- example -->

| Erreur | Regardez |
|---|---|
| `HIVE_PARTITION_SCHEMA_MISMATCH` | schéma de partition vs table dans le catalogue |
| `HIVE_CURSOR_ERROR` | fichier corrompu ou au mauvais format |
| `HIVE_BAD_DATA` | une valeur qui ne correspond pas au type |
| `Access Denied` | S3, bucket de résultats, KMS, Glue, Lake Formation |

#### Que signifie `HIVE_PARTITION_SCHEMA_MISMATCH` ?

Le schéma d'une partition dans le catalogue diffère de celui de la table (types ou colonnes). Faites hériter aux partitions le schéma de la table (réglage du crawler ou recréation des partitions) et stabilisez la source.

#### Qu'indique généralement `HIVE_CURSOR_ERROR` ?

Un problème de lecture de fichier : fichiers corrompus ou tronqués, format différent de la définition de la table, fichier compressé illisible, ou problèmes de droits ou de KMS sur certains objets.

#### Que signifie `HIVE_BAD_DATA` ?

Une valeur ne peut pas être lue avec le type déclaré, par exemple du texte dans une colonne numérique, un enregistrement JSON mal formé, ou un type Parquet discordant. Corrigez les données, les types de la table, ou utilisez `TRY_CAST` sur des colonnes texte.

#### Pourquoi obtient-on `Access Denied` sur une requête ?

Il manque des droits sur les données S3, l'emplacement des résultats, la clé KMS, les objets du catalogue Glue, les droits Lake Formation ou le workgroup. Le message d'erreur nomme généralement la ressource.

<!-- challenge -->

Un utilisateur reçoit `Access Denied` alors qu'il a un accès complet en lecture S3 aux données. Citez trois autres endroits à vérifier.

<!-- solution -->

Le droit d'écriture sur l'emplacement des résultats, le droit de déchiffrement sur la clé KMS des données ou des résultats, et les permissions du catalogue Glue (ou de Lake Formation) sur la base et la table.

<!-- takeaways -->

- L'erreur nomme la couche en échec.
- Utilisez `"$path"` pour trouver les mauvais fichiers.
- L'accès exige S3, résultats, KMS, Glue et Lake Formation.

<!-- unit: Requêtes lentes et en échec -->

<!-- goals -->

- Diagnostiquer des requêtes lentes qui scannent peu.
- Corriger timeouts, throttling et ralentissements Iceberg.

<!-- concept -->

Toute lenteur ne vient pas du scan. Planifier beaucoup de partitions, ouvrir beaucoup de petits fichiers, attendre un throttling S3 ou une source fédérée lente prennent un temps que les métriques d'octets ne montrent pas. Les statistiques d'exécution répartissent le temps entre file, planification et exécution, ce qui désigne le coupable.

Les tables Iceberg ralentissent pour une raison voisine : les écritures fréquentes laissent petits fichiers et fichiers de suppression jusqu'à ce que la maintenance les nettoie.

<!-- example -->

```text
QueryQueueTime:      0.2 s
QueryPlanningTime:  48.7 s   ← partition metadata, not data
EngineExecutionTime: 3.1 s
DataScannedInBytes:  120 MB
```

#### Une requête est lente mais lit peu de données. Quelle peut en être la cause ?

Le temps de planification sur des tables très partitionnées (utilisez la projection ou les index de partition), de nombreux fichiers minuscules (surcharge par fichier), une source fédérée, l'attente due aux limites de concurrence, ou une opération coûteuse comme une grosse jointure ou un tri global.

#### Pourquoi obtient-on « Query timeout » ?

La requête a dépassé le timeout du workgroup : trop de données lues, une jointure ou un tri lourd, ou une source fédérée lente. Optimisez la requête ou l'organisation des données, matérialisez des étapes intermédiaires ou relevez le quota de timeout.

#### Pourquoi des erreurs « too many open files » ou `SlowDown` S3 ?

Des tables composées d'un nombre énorme de petits fichiers provoquent énormément de requêtes S3 simultanées. Compactez les fichiers et répartissez-les sur plusieurs partitions.

#### Pourquoi une requête sur Iceberg ralentit-elle avec le temps ?

De nombreux petits fichiers et fichiers de suppression s'accumulent avec des écritures fréquentes et des modifications au niveau ligne. Planifiez `OPTIMIZE` et `VACUUM` (ou utilisez la compaction automatique du catalogue Glue ou de S3 Tables).

<!-- challenge -->

Une table Iceberg mise à jour toutes les 5 minutes est maintenant dix fois plus lente à interroger que le mois dernier. Que planifiez-vous ?

<!-- solution -->

Un `OPTIMIZE ... REWRITE DATA USING BIN_PACK` régulier pour compacter petits fichiers et fichiers de suppression, et `VACUUM` pour expirer les anciens snapshots, par exemple chaque jour. Envisagez des mises à jour moins fréquentes si la fraîcheur le permet.

<!-- takeaways -->

- Examinez séparément file, planification et exécution.
- Beaucoup de partitions ou de fichiers ralentissent la planification, pas le scan.
- Les tables Iceberg exigent une compaction régulière.

<!-- stage: Tout assembler -->

### Mises en situation

<!-- unit: Concevoir l'analytique de logs et d'événements -->

<!-- goals -->

- Concevoir un chemin peu coûteux et rapide des événements aux requêtes.
- Équilibrer fraîcheur, coût et taille de fichiers.

<!-- concept -->

Les conceptions Athena réussissent ou échouent sur le chemin d'écriture. Les requêtes sont rapides et peu coûteuses quand les données arrivent en fichiers colonnes de bonne taille, partitionnés selon les filtres utilisés et enregistrés sans étape manuelle. Une bonne réponse suit les données du producteur à la requête, nomme un choix à chaque étape, puis explique le compromis fraîcheur-coût : des tampons plus courts donnent des données plus fraîches mais des fichiers plus petits.

<!-- example -->

```text
apps ─► Firehose (buffer 5 min, convert to Parquet, dt/hour prefixes)
     ─► S3 lake ─► table with partition projection
     ─► workgroup with limits ─► dashboards on hourly summary tables
```

#### Concevez une solution d'analyse de journaux peu coûteuse avec Athena.

Livrer les journaux dans S3 avec Firehose (bufferisés, convertis en Parquet, partitionnés par date), définir une table avec projection de partitions par date, créer des vues pour les questions courantes, configurer un workgroup avec des limites de données, et donner l'accès aux analystes via Lake Formation. Ajouter des règles de cycle de vie pour déplacer les anciens journaux vers des classes de stockage moins chères.

#### Comment construire des dashboards quasi temps réel sur Athena ?

Envoyer les événements avec Firehose vers S3 en Parquet avec des buffers courts, partitionner par date et heure avec projection, construire toutes les quelques minutes de petites tables agrégées avec un `INSERT INTO` planifié ou un `MERGE` dans Iceberg, et pointer les dashboards vers ces agrégats ; pour une latence sous la minute, utiliser un autre stockage comme OpenSearch ou une base de données de streaming.

<!-- challenge -->

Le métier veut des tableaux de bord rafraîchis chaque minute au lieu de toutes les 15. Qu'est-ce qui change, et combien cela coûte-t-il ?

<!-- solution -->

Raccourcir le tampon Firehose et rafraîchir plus souvent, ce qui crée beaucoup plus de petits fichiers et de requêtes. Ajouter une compaction (ou Iceberg avec `OPTIMIZE`) et interroger des tables de synthèse ; si une latence d'une minute est vraiment nécessaire, envisager un stockage de streaming plutôt qu'Athena.

<!-- takeaways -->

- Concevez le chemin d'écriture : format, taille, partitions, enregistrement.
- La fraîcheur se paie en taille de fichiers et volume de requêtes.
- Servez les tableaux de bord depuis des synthèses, pas des événements bruts.

<!-- unit: Migrations et libre-service gouverné -->

<!-- goals -->

- Planifier la migration de rapports vers Athena.
- Mettre en place un accès gouverné et budgété à un grand lake.

<!-- concept -->

Amener des utilisateurs sur Athena relève autant du contrôle que du SQL. Une migration exige des données dans de bons formats, des requêtes traduites et une validation en parallèle. Le libre-service exige des garde-fous pour que la liberté ne finisse pas en coûts incontrôlés ou en fuites : permissions par domaine, workgroups limités, tables curées et surveillance. Les deux questions testent si vous voyez Athena comme partie d'une plateforme, pas comme un outil isolé.

<!-- example -->

| Préoccupation | Contrôle |
|---|---|
| Qui voit quoi | Permissions Lake Formation par domaine |
| Combien ils dépensent | Un workgroup par équipe, limite par requête |
| Vitesse et coût des requêtes | Parquet partitionné ou Iceberg, synthèses |
| Ce qui s'est passé | CloudTrail, export de l'historique des requêtes |

#### Comment migrer des rapports d'un SQL Server on-premise vers Athena ?

Exporter les tables vers S3 en Parquet (DMS ou exports), définir des tables Glue ou Iceberg, traduire le T-SQL en SQL Trino (fonctions, gestion des dates, `TOP` vers `LIMIT`, pas de `PIVOT`), recréer les vues, valider les résultats en comparant des agrégats, et connecter l'outil BI via le pilote.

#### Une équipe a besoin d'un accès SQL ad hoc à un data lake de 50 To avec un budget serré. Que mettez-vous en place ?

Des droits Lake Formation par domaine, un workgroup par équipe avec limites par requête, des tables Parquet ou Iceberg partitionnées par date, des vues qui imposent un filtre de partition, la réutilisation des résultats, une documentation des tables et des rapports mensuels des octets lus par équipe.

<!-- challenge -->

Après la migration des rapports, les totaux diffèrent légèrement de SQL Server pour certains jours. Comment trouver la cause ?

<!-- solution -->

Comparez par jour et par clé pour localiser l'écart, puis inspectez les lignes. Causes typiques : fuseaux horaires des timestamps, `double` contre `decimal`, gestion des `NULL` dans les jointures et fonctions T-SQL traduites avec une sémantique différente.

<!-- takeaways -->

- Les migrations exigent formats, traduction et validation.
- Le libre-service exige permissions, limites et données curées.
- Validez en comparant les agrégats par clé et par jour.
