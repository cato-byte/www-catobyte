## Fiche d'étude Snowflake

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude Snowflake : environ 200 questions](../../images/snowflake_study_guide_title_img.png)

Environ 200 questions d'entretien sur Snowflake, de son architecture aux virtual warehouses, aux micro-partitions, au chargement, aux données semi-structurées, aux streams et tasks, aux dynamic tables, à la sécurité, au partage de données, aux performances et à la maîtrise des coûts. Les réponses décrivent la plateforme telle qu'elle est en 2026. Ouvrez une question pour voir sa réponse, ou utilisez le filtre pour chercher dans toute la fiche.

<!-- QA -->

### Architecture

#### Qu'est-ce que Snowflake ?

Une plateforme de données cloud fournie en service entièrement géré sur AWS, Azure et Google Cloud. D'abord entrepôt de données SQL, elle couvre aujourd'hui aussi les data lakes (tables Iceberg), l'ingénierie des données, le partage de données, les applications et l'IA. Il n'y a ni matériel ni logiciel à installer, régler ou patcher.

#### Quelles sont les trois couches de l'architecture de Snowflake ?

Le stockage (données stockées en micro-partitions compressées et en colonnes dans le stockage objet cloud), le traitement des requêtes (les virtual warehouses : des clusters de calcul indépendants) et les services cloud (authentification, métadonnées, optimisation des requêtes, contrôle d'accès, transactions et gestion de l'infrastructure).

#### Que signifie la « séparation du stockage et du calcul » dans Snowflake ?

Les données sont stockées une seule fois dans un stockage central, et autant de virtual warehouses que nécessaire peuvent les lire indépendamment. On dimensionne et on paie séparément calcul et stockage, et les charges (chargement, BI, data science) ne se disputent pas les mêmes ressources.

#### Pourquoi dit-on que Snowflake est un hybride entre shared-disk et shared-nothing ?

Comme en shared-disk, tous les nœuds de calcul voient une copie centrale unique des données. Comme en shared-nothing (MPP), chaque warehouse traite sa part des données sur ses propres nœuds avec un cache local, ce qui donne des performances qui passent à l'échelle.

#### Qu'est-ce qu'un virtual warehouse ?

Un cluster de calcul nommé qui exécute les requêtes et le DML et charge les données. Il a une taille, peut être suspendu et repris, et ne consomme des crédits que lorsqu'il tourne.

#### Que fait la couche de services cloud ?

Elle coordonne tout : authentification et contrôle d'accès, magasin de métadonnées (tables, statistiques des micro-partitions, historique), analyse et optimisation des requêtes, gestion des transactions, cache de résultats et sécurité. Elle n'est facturée que si son usage dépasse 10 % du calcul quotidien des warehouses.

#### Que sont un compte et une organisation Snowflake ?

Un compte est un déploiement Snowflake dans une région d'un cloud, avec ses propres utilisateurs, bases et warehouses, accessible par une URL. Une organisation regroupe plusieurs comptes d'un même client pour la facturation, la réplication et la gestion des comptes (via ORGADMIN).

#### Quelle est la hiérarchie des objets dans Snowflake ?

Organisation → compte → base de données → schéma → objets (tables, vues, stages, file formats, séquences, streams, tasks, pipes, fonctions, procédures). Les warehouses, utilisateurs, rôles, resource monitors et intégrations sont des objets de niveau compte.

#### Quelles éditions Snowflake propose-t-il ?

Standard ; Enterprise (ajoute les warehouses multi-cluster, le Time Travel jusqu'à 90 jours, les vues matérialisées, les politiques de masquage et d'accès aux lignes, la search optimization) ; Business Critical (ajoute une sécurité et une conformité renforcées comme HIPAA et PCI, Tri-Secret Secure, la connectivité privée et le failover) ; et Virtual Private Snowflake (un environnement totalement isolé).

#### Qu'est-ce qu'un crédit ?

L'unité de facturation du calcul. Un warehouse consomme des crédits à la seconde (avec un minimum de 60 secondes à chaque reprise) selon sa taille. Les fonctions serverless (Snowpipe, clustering automatique, search optimization, tasks serverless) consomment aussi des crédits. Le stockage est facturé à part, par To et par mois.

#### Quel lien entre la taille des warehouses et les crédits ?

Chaque palier double le calcul et le tarif en crédits : X-Small consomme 1 crédit par heure, Small 2, Medium 4, Large 8, et ainsi de suite jusqu'à 6X-Large. Une requête qui se parallélise bien s'exécute environ deux fois plus vite au palier suivant : le coût peut rester similaire tandis que la latence baisse.

#### Quels fournisseurs cloud et régions peut-on utiliser ?

AWS, Azure et Google Cloud, dans de nombreuses régions. Un compte vit dans une région d'un cloud ; la réplication et le partage de données entre régions et clouds relient les comptes.

#### Comment se connecter à Snowflake ?

Via Snowsight (l'interface web), la Snowflake CLI et SnowSQL, les pilotes (JDBC, ODBC, connecteur Python, Go, Node.js, .NET, connecteurs Spark et Kafka), l'API REST SQL et les outils partenaires (BI, ETL, dbt).

#### Qu'est-ce que Snowsight ?

L'interface web de Snowflake pour écrire des worksheets SQL et Python, des notebooks et des dashboards, explorer les données, surveiller les requêtes et les coûts, et administrer le compte.

#### Qu'est-ce que Snowflake Horizon ?

Les capacités intégrées de gouvernance et de catalogue de Snowflake : contrôle d'accès, classification des données sensibles, politiques de masquage et d'accès aux lignes, tags, lignage, supervision de la qualité des données, audit et découverte, appliqués aux tables, aux tables Iceberg et aux données partagées.

#### Quelle est la différence entre Snowflake et un entrepôt MPP traditionnel comme Teradata ou Redshift (provisionné) ?

Les entrepôts MPP traditionnels couplent stockage et calcul sur les mêmes nœuds : monter en charge implique de redistribuer les données, et toutes les charges partagent un cluster. Snowflake garde le stockage centralisé et permet de démarrer des warehouses indépendants en quelques secondes, sans index, clés de distribution ni vacuum à gérer.

#### Quel est le rôle de l'URL et du localisateur du compte ?

L'identifiant de compte (nom de l'organisation plus nom du compte, ou l'ancien localisateur avec la région) forme l'URL à laquelle se connectent les clients, par exemple `myorg-myaccount.snowflakecomputing.com`.

#### Qu'est-ce que le contexte d'une session Snowflake ?

Le rôle, le warehouse, la base et le schéma courants d'une session (`USE ROLE`, `USE WAREHOUSE`, `USE DATABASE`, `USE SCHEMA`). Les requêtes s'exécutent avec les privilèges du rôle courant sur le warehouse courant, et les noms non qualifiés se résolvent dans la base et le schéma courants.

### Stockage et micro-partitions

#### Qu'est-ce qu'une micro-partition ?

L'unité physique de stockage d'une table Snowflake : un fichier immuable de 50 à 500 Mo de données non compressées (bien moins une fois compressé), stocké en colonnes. Snowflake les crée automatiquement au chargement, dans l'ordre d'arrivée des données.

#### Quelles métadonnées Snowflake conserve-t-il par micro-partition ?

La plage de valeurs (min et max) de chaque colonne, le nombre de valeurs distinctes, le nombre de nulls et d'autres statistiques. L'optimiseur s'en sert pour écarter les micro-partitions qui ne peuvent pas contenir de lignes correspondantes.

#### Qu'est-ce que le pruning ?

Le fait d'écarter des micro-partitions pendant une lecture parce que leurs métadonnées montrent qu'elles ne peuvent pas satisfaire le filtre. Un bon pruning est la principale raison pour laquelle des requêtes sur d'énormes tables peuvent être rapides. Il apparaît dans le query profile sous la forme « partitions scanned » face à « partitions total ».

#### Pourquoi les micro-partitions sont-elles immuables, et que fait un update ?

L'immutabilité simplifie la concurrence, le Time Travel et le clonage. Un `UPDATE` ou un `DELETE` écrit de nouvelles micro-partitions contenant les lignes modifiées et marque les anciennes comme non courantes ; les anciennes sont conservées pour le Time Travel et le Fail-safe.

#### Qu'est-ce que le clustering des données dans Snowflake ?

La mesure dans laquelle les lignes ayant des valeurs proches pour une colonne se trouvent dans les mêmes micro-partitions. Des données chargées par ordre de date sont naturellement bien regroupées par date. Le clustering se dégrade quand le DML disperse les valeurs sur de nombreuses partitions.

#### Qu'est-ce qu'une clé de clustering ?

Une ou plusieurs colonnes ou expressions déclarées sur une grande table (`CLUSTER BY (event_date, customer_id)`) pour que le service Automatic Clustering réorganise les micro-partitions en arrière-plan et garde ensemble les valeurs proches, ce qui améliore le pruning des filtres sur ces colonnes.

#### Quand définir une clé de clustering ?

Sur de très grandes tables (plusieurs téraoctets) dont les requêtes filtrent sur des colonnes non regroupées naturellement et dont le query profile montre un pruning médiocre. Le clustering coûte des crédits de reclustering : il ne vaut pas la peine pour des tables petites ou souvent réécrites entièrement.

#### Comment vérifier la qualité du clustering d'une table ?

Avec `SYSTEM$CLUSTERING_INFORMATION('table', '(col)')`, qui indique la profondeur moyenne et le chevauchement des micro-partitions. Une profondeur plus faible signifie un meilleur clustering.

#### Comment les données sont-elles compressées dans Snowflake ?

Automatiquement, colonne par colonne, avec le meilleur encodage pour les données. On ne choisit pas la compression ; le stockage est facturé sur la taille compressée.

#### Quels types de tables existent dans Snowflake ?

Les tables permanentes (Time Travel et 7 jours de Fail-safe), transitoires (Time Travel de 0 ou 1 jour, sans Fail-safe, moins chères pour des données reconstructibles), temporaires (n'existent que pendant la session), externes (lisent des fichiers d'un stage), les tables Iceberg, les tables hybrides (orientées ligne, pour les charges transactionnelles) et les dynamic tables.

#### Que sont les tables Iceberg dans Snowflake ?

Des tables stockées au format Apache Iceberg dans votre propre stockage cloud (un external volume). Avec Snowflake comme catalogue, elles se comportent presque comme des tables natives ; avec un catalogue externe (AWS Glue, Snowflake Open Catalog/Apache Polaris et d'autres), Snowflake peut les lire et, dans certains cas, les écrire. D'autres moteurs (Spark, Trino) peuvent travailler sur les mêmes données.

#### Que sont les tables hybrides ?

Des tables optimisées pour des lectures et écritures de lignes uniques à faible latence et forte concurrence, avec des clés primaires et des index appliqués, qu'on peut joindre à des tables analytiques dans la même requête. Elles visent les charges transactionnelles légères (Unistore).

#### Qu'est-ce qu'une table externe ?

Une table en lecture seule dont les données restent dans des fichiers d'un stage externe (S3, GCS, Azure). Snowflake stocke des métadonnées au niveau fichier, et l'on interroge les fichiers en SQL. Elle est plus lente que les tables natives ; on lui préfère généralement les tables Iceberg aujourd'hui.

#### Comment le stockage est-il facturé ?

Sur la moyenne mensuelle des octets compressés des tables, des données de Time Travel et de Fail-safe et des fichiers en stage, à un tarif par To qui dépend du mode (capacité ou à la demande) et de la région.

#### Que fait `ALTER TABLE … SUSPEND RECLUSTER` ?

Il met en pause le clustering automatique d'une table et arrête les coûts de reclustering, par exemple pendant un gros backfill ; `RESUME RECLUSTER` le réactive.

#### Quelle différence entre le clustering naturel d'une colonne et une clé de clustering ?

Le clustering naturel découle de l'ordre de chargement et ne coûte rien ; une clé de clustering demande à Snowflake de maintenir un ordre par reclustering en arrière-plan, ce qui coûte des crédits mais garde un bon pruning malgré le DML.

#### Comment voir le stockage utilisé par le Time Travel et le Fail-safe ?

Dans `ACCOUNT_USAGE.TABLE_STORAGE_METRICS`, qui indique par table les octets actifs, ceux du Time Travel, ceux du Fail-safe et ceux retenus pour des clones.

### Virtual warehouses et calcul

#### Que se passe-t-il quand un warehouse est suspendu ?

Il cesse de consommer des crédits et son cache local est vidé. Avec l'auto-resume, la requête suivante le relance en une ou deux secondes.

#### Que sont l'auto-suspend et l'auto-resume ?

Des réglages qui suspendent un warehouse après un certain nombre de secondes d'inactivité et le reprennent automatiquement à l'arrivée d'une requête. Un auto-suspend court (par exemple 60 secondes) économise des crédits sur des charges intermittentes ; un plus long garde le cache chaud pour la BI.

#### Qu'est-ce qu'un warehouse multi-cluster ?

Une fonction Enterprise où un warehouse peut faire tourner plusieurs clusters de même taille, entre un minimum et un maximum, pour absorber la concurrence. Des clusters supplémentaires démarrent quand des requêtes attendent et s'arrêtent quand la charge baisse.

#### Quelle est la différence entre scale up et scale out ?

Le scale up (un warehouse plus gros) accélère les requêtes complexes individuelles et réduit le spilling. Le scale out (plus de clusters dans un warehouse multi-cluster) sert davantage d'utilisateurs simultanés sans file d'attente ; il n'accélère pas une requête individuelle.

#### Quelles sont les politiques de scaling multi-cluster ?

Standard (démarre vite des clusters pour éviter l'attente, privilégie la performance) et Economy (ne démarre un cluster que s'il y a assez de charge pour l'occuper plusieurs minutes, privilégie le coût).

#### Comment séparer les charges de travail dans Snowflake ?

Avec des warehouses distincts par charge (ingestion, transformation, BI, data science, ad hoc), chacun dimensionné et suspendu de façon adaptée, pour qu'ils ne se disputent jamais le calcul et que leurs coûts soient visibles séparément.

#### Qu'est-ce que la mise en file d'attente des requêtes, et comment la réduire ?

Les requêtes attendent quand un warehouse atteint sa limite de concurrence (`MAX_CONCURRENCY_LEVEL`, 8 par défaut). Solutions : warehouses multi-cluster, warehouses séparés par charge, requêtes plus rapides ou warehouse plus gros.

#### Qu'est-ce qu'un warehouse optimisé Snowpark ?

Un warehouse doté de beaucoup plus de mémoire par nœud, pour les charges Snowpark gourmandes en mémoire comme l'entraînement de ML ou le traitement par de grosses UDF.

#### Qu'est-ce que le Query Acceleration Service ?

Une fonction serverless qui délègue des parties des lectures et filtres volumineux des requêtes éligibles à un calcul partagé, pour que les requêtes atypiques se terminent plus vite sans redimensionner tout le warehouse. On l'active par warehouse avec une limite de facteur d'échelle.

#### Que sont les warehouses standard Gen2 ?

Une nouvelle génération de warehouses standard, avec du matériel plus rapide et des améliorations du moteur, surtout pour le DML et les grosses lectures, facturés à un tarif en crédits un peu plus élevé. On les choisit warehouse par warehouse.

#### Qu'est-ce que le timeout d'instruction ?

`STATEMENT_TIMEOUT_IN_SECONDS`, défini sur un warehouse, un utilisateur ou une session, annule les requêtes qui dépassent la limite. Il évite qu'une requête incontrôlée ne brûle des crédits pendant des heures.

#### Une requête en cours profite-t-elle d'un warehouse redimensionné ?

Le redimensionnement s'applique aux nouvelles requêtes ; celles en cours se terminent avec les ressources existantes. Un scale up provisionne de nouvelles ressources en arrière-plan, dont profitent les requêtes en attente et nouvelles dès qu'elles sont prêtes.

#### Que contrôle `MAX_CONCURRENCY_LEVEL` ?

Le nombre d'instructions SQL simultanées qu'un cluster de warehouse exécute avant de mettre les autres en attente. Le baisser donne plus de ressources à chaque requête ; l'augmenter permet plus de requêtes en parallèle au risque de ralentir chacune.

#### Comment choisir la taille initiale d'un warehouse ?

Commencer petit (X-Small ou Small) pour le développement et les chargements simples, tester des requêtes représentatives, et n'augmenter la taille que si les requêtes déversent, durent trop ou ne tiennent pas l'objectif. Mesurer le coût par exécution, pas seulement la durée.

### Caches

#### Quels caches Snowflake possède-t-il ?

Le cache de résultats (dans la couche services : résultats réutilisés pendant 24 heures si la requête et les données n'ont pas changé), le cache du warehouse (données de micro-partitions sur le SSD local du warehouse tant qu'il tourne) et le cache de métadonnées (statistiques qui répondent à certaines requêtes comme `COUNT(*)` ou `MIN` sans warehouse).

#### Quand le cache de résultats est-il utilisé ?

Quand le même texte de requête est relancé, que les données n'ont pas changé, que l'utilisateur a les droits nécessaires et que la requête n'utilise pas de fonctions non déterministes comme `CURRENT_TIMESTAMP()`. Chaque réutilisation prolonge la rétention, jusqu'à 31 jours. Il ne coûte aucun calcul.

#### Quel lien entre le cache du warehouse et l'auto-suspend ?

La suspension vide le cache local : les requêtes suivantes lisent depuis le stockage distant et sont plus lentes. Pour des dashboards qui interrogent sans cesse les mêmes données, un auto-suspend plus long peut être plus rapide sans coûter beaucoup plus.

#### Comment désactiver le cache de résultats pour des tests ?

`ALTER SESSION SET USE_CACHED_RESULT = FALSE;` pour que les requêtes de benchmark s'exécutent vraiment.

#### Le cache de résultats fonctionne-t-il entre utilisateurs ?

Oui, si le rôle de l'autre utilisateur a les droits nécessaires sur les objets et que le texte de la requête est identique ; les résultats ne sont pas liés à l'utilisateur d'origine.

#### Pourquoi une requête répétée peut-elle ne pas utiliser le cache de résultats ?

Les données ont changé, le texte diffère (parfois même par les espaces ou la casse), elle utilise des fonctions non déterministes, des fonctions externes ou certaines fonctions de table, le résultat a dépassé sa rétention, ou le cache est désactivé dans la session.

### Chargement des données

#### Quelles sont les façons de charger des données dans Snowflake ?

Le chargement en masse avec `COPY INTO` depuis des stages, le chargement continu avec Snowpipe (fichiers) et Snowpipe Streaming (lignes), le connecteur Kafka, Openflow et les outils ETL/ELT partenaires, les instructions `INSERT`, les tables externes et Iceberg pour interroger sur place, et le partage de données pour les données d'autres comptes.

#### Qu'est-ce qu'un stage ?

Un emplacement pour les fichiers à charger ou décharger. Les stages internes sont dans Snowflake : stage utilisateur (`@~`), stage de table (`@%table`) et stages nommés. Les stages externes pointent vers des conteneurs S3, GCS ou Azure, généralement via une storage integration.

#### Qu'est-ce qu'une storage integration ?

Un objet de compte qui contient une identité cloud (sur AWS, un rôle IAM que Snowflake assume) et les emplacements autorisés, pour que les stages externes accèdent aux buckets sans stocker d'identifiants dans le SQL.

```sql
CREATE STORAGE INTEGRATION s3_lake
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/snowflake-lake'
  STORAGE_ALLOWED_LOCATIONS = ('s3://my-lake/raw/');

CREATE STAGE raw_stage URL = 's3://my-lake/raw/' STORAGE_INTEGRATION = s3_lake;
```

#### Qu'est-ce qu'un objet file format ?

Une définition nommée de la façon de lire les fichiers : type (CSV, JSON, Avro, ORC, Parquet, XML), délimiteurs, gestion de l'en-tête, chaînes nulles, compression, formats de date. Les stages et les instructions `COPY` y font référence.

#### Comment fonctionne `COPY INTO <table>` ?

Il charge en parallèle les fichiers d'un stage dans une table, avec un file format, des options de gestion d'erreurs et des transformations dans un `SELECT`. Il conserve 64 jours de métadonnées de chargement par table : les fichiers déjà chargés sont ignorés par défaut.

```sql
COPY INTO raw.orders
FROM @raw_stage/orders/
FILE_FORMAT = (TYPE = 'PARQUET')
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
ON_ERROR = 'ABORT_STATEMENT';
```

#### Quelles options `ON_ERROR` existent pour `COPY` ?

`ABORT_STATEMENT` (par défaut pour les chargements en masse), `CONTINUE` (ignore les lignes en erreur), `SKIP_FILE`, `SKIP_FILE_<n>` ou `SKIP_FILE_<n>%` (ignore un fichier avec trop d'erreurs). Utilisez `VALIDATION_MODE = RETURN_ERRORS` pour tester un chargement sans charger, et la fonction `VALIDATE` pour voir les erreurs d'un chargement précédent.

#### Quelle est la taille de fichier idéale pour le chargement ?

Environ 100 à 250 Mo compressés par fichier. De nombreux petits fichiers ajoutent de la surcharge ; un seul énorme fichier ne peut pas être chargé en parallèle. Découpez les gros fichiers et regroupez les petits.

#### Qu'est-ce que Snowpipe ?

Un service serverless qui charge des fichiers en continu à mesure qu'ils arrivent dans un stage, via une instruction `COPY` définie dans un pipe. Avec l'auto-ingest, ce sont les notifications d'événements cloud (événements S3 via SQS, Event Grid, Pub/Sub) qui le déclenchent ; sinon on appelle son API REST. La latence est généralement d'environ une minute.

```sql
CREATE PIPE raw.orders_pipe AUTO_INGEST = TRUE AS
COPY INTO raw.orders FROM @raw_stage/orders/ FILE_FORMAT = (TYPE = 'JSON');
```

#### Comment Snowpipe est-il facturé, et pourquoi la taille des fichiers compte-t-elle ?

Au calcul serverless plus une petite surcharge par fichier (dans la tarification récente, un montant fixe par Go ingéré). Avec de très petits fichiers, la surcharge domine : les producteurs devraient regrouper les données en fichiers de taille raisonnable, idéalement envoyés environ toutes les minutes plutôt qu'à chaque événement.

#### Qu'est-ce que Snowpipe Streaming ?

Une API (via le SDK Java ou Python, le connecteur Kafka ou Openflow) qui écrit des lignes directement dans les tables avec quelques secondes de latence, sans passer par des fichiers en stage. Elle convient aux flux d'événements ; son architecture haute performance est facturée au volume de données.

#### Comment décharger des données de Snowflake ?

Avec `COPY INTO @stage/chemin/ FROM (SELECT ...)`, qui écrit des fichiers CSV, JSON ou Parquet dans un stage interne ou externe, avec des options de partitionnement (`PARTITION BY`), de taille de fichier et d'en-têtes. `GET` télécharge ensuite les fichiers des stages internes.

#### Que sont `PUT` et `GET` ?

Des commandes client (SnowSQL, CLI, pilotes) pour téléverser des fichiers locaux dans un stage interne (`PUT`, qui les compresse et les chiffre) et les télécharger depuis celui-ci (`GET`).

#### Qu'est-ce que la détection de schéma avec `INFER_SCHEMA` ?

Une fonction qui lit des fichiers Parquet, Avro, ORC, JSON ou CSV en stage et renvoie les noms et types de colonnes ; combinée à `CREATE TABLE … USING TEMPLATE`, elle crée une table d'après la structure des fichiers. Les tables peuvent aussi activer l'évolution de schéma pour ajouter les nouvelles colonnes pendant les chargements.

#### Qu'est-ce que l'option `FORCE` de `COPY` ?

`FORCE = TRUE` recharge les fichiers même si les métadonnées indiquent qu'ils ont déjà été chargés, ce qui peut créer des doublons ; on l'utilise volontairement pour recharger après avoir vidé une table.

#### Comment `COPY` traite-t-il les fichiers de plus de 64 jours ?

Les métadonnées de chargement expirent au bout de 64 jours : pour les fichiers plus anciens, Snowflake peut ignorer s'ils ont été chargés. `LOAD_UNCERTAIN_FILES = TRUE` les charge quand même ; pour éviter l'ambiguïté, déplacez ou supprimez les fichiers une fois chargés, ou utilisez Snowpipe, qui garde 14 jours d'historique par pipe.

#### Comment transformer les données pendant le `COPY` ?

Avec un `SELECT` sur les fichiers du stage dans l'instruction `COPY` : réordonner ou omettre des colonnes, convertir des types, utiliser les positions `$1`, `$2` ou `$1:champ` pour le semi-structuré, et ajouter `METADATA$FILENAME` ou `METADATA$FILE_ROW_NUMBER` pour le lignage.

#### Comment interroger des fichiers en stage sans les charger ?

`SELECT $1, $2, METADATA$FILENAME FROM @stage/chemin (FILE_FORMAT => 'my_csv')`, pratique pour inspecter les fichiers avant de les charger.

#### Qu'est-ce qu'Openflow ?

Le service d'intégration de données géré de Snowflake, fondé sur Apache NiFi, avec des connecteurs pour les bases de données, applications SaaS et flux, déployé dans Snowflake ou dans votre propre cloud (bring your own cloud), pour ingérer des données structurées et non structurées.

#### Comment charger une base relationnelle en CDC dans Snowflake ?

Avec un outil de CDC (connecteurs Openflow, Debezium avec Kafka et le connecteur Kafka de Snowflake, Fivetran, AWS DMS écrivant dans S3 plus Snowpipe) qui dépose les événements de changement dans des tables raw, puis un `MERGE` depuis un stream ou une dynamic table pour les appliquer à la table d'état courant.

### Données semi-structurées

#### Qu'est-ce que le type `VARIANT` ?

Un type qui peut contenir n'importe quelle valeur de type JSON (objet, tableau, chaîne, nombre, booléen, null) jusqu'à une taille limite. Snowflake stocke en interne sous forme colonne les clés fréquentes, donc les requêtes sur celles-ci peuvent faire du pruning et rester rapides.

#### Comment interroger du JSON stocké dans un `VARIANT` ?

Avec la notation de chemin et des conversions :

```sql
SELECT payload:customer.id::NUMBER       AS customer_id,
       payload:items[0]:sku::STRING       AS first_sku
FROM raw.events
WHERE payload:type::STRING = 'purchase';
```

#### Que fait `FLATTEN` ?

Une fonction de table qui déplie un tableau ou un objet en une ligne par élément, utilisée avec `LATERAL` pour désimbriquer les données.

```sql
SELECT e.payload:order_id::STRING AS order_id, i.value:sku::STRING AS sku
FROM raw.events e, LATERAL FLATTEN(input => e.payload:items) i;
```

#### Que sont les types `OBJECT` et `ARRAY` ?

Des types semi-structurés pour les objets clé-valeur et les tableaux. Des fonctions comme `OBJECT_CONSTRUCT`, `ARRAY_AGG`, `ARRAY_CONTAINS` et `PARSE_JSON` les construisent et les inspectent. Les versions structurées (`OBJECT(name STRING, age NUMBER)`, `ARRAY(NUMBER)`) imposent le type des éléments.

#### Faut-il garder le JSON en `VARIANT` ou l'aplatir en colonnes ?

Gardez le JSON brut en `VARIANT` dans la couche d'atterrissage pour la souplesse et la traçabilité, puis extrayez les champs souvent interrogés en colonnes typées dans les couches nettoyées : les colonnes typées sont plus simples à utiliser, documenter et gouverner, et leur pruning est prévisible.

#### Comment gérer un champ JSON tantôt texte, tantôt nombre ?

En convertissant de façon défensive avec `TRY_CAST` ou `TRY_TO_NUMBER`, qui renvoient `NULL` au lieu d'échouer, et en vérifiant le type avec `TYPEOF()` pour mettre en quarantaine les valeurs inattendues.

#### Comment convertir des lignes relationnelles en JSON ?

Avec `OBJECT_CONSTRUCT(*)` ou `OBJECT_CONSTRUCT('id', id, 'name', name)` par ligne, et `ARRAY_AGG` pour regrouper des lignes en tableaux, utile pour exporter des documents imbriqués ou alimenter des API.

#### En quoi une clé absente diffère-t-elle d'un null JSON ?

Une clé absente renvoie le `NULL` SQL ; une valeur JSON `null` est un null de `VARIANT`, différent du `NULL` SQL (`IS_NULL_VALUE()` le teste). La conversion avec `::STRING` transforme le null JSON en `NULL` SQL.

#### Comment charger des colonnes Parquet directement dans des colonnes de table ?

Avec `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE` dans `COPY`, qui associe les colonnes du fichier à celles de la table par nom, ou en sélectionnant explicitement `$1:nom_colonne::type`.

### Fonctions SQL

#### Qu'est-ce que `QUALIFY` ?

Une clause qui filtre sur les résultats des fonctions de fenêtre, comme `HAVING` pour les agrégats. C'est la manière idiomatique de dédupliquer :

```sql
SELECT *
FROM raw.customers
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1;
```

#### Que fait `MERGE` dans Snowflake ?

Il insère, met à jour ou supprime des lignes d'une table cible selon une jointure avec une source, en une seule instruction atomique, typiquement pour les upserts et le CDC.

```sql
MERGE INTO dw.customers t
USING staging.customers s ON t.customer_id = s.customer_id
WHEN MATCHED AND s.is_deleted THEN DELETE
WHEN MATCHED THEN UPDATE SET t.email = s.email, t.updated_at = s.updated_at
WHEN NOT MATCHED THEN INSERT (customer_id, email, updated_at)
  VALUES (s.customer_id, s.email, s.updated_at);
```

#### Snowflake applique-t-il les clés primaires et étrangères ?

Sur les tables standard, seul `NOT NULL` est appliqué. Les contraintes de clé primaire, d'unicité et de clé étrangère sont informatives : elles documentent le modèle et peuvent aider les outils de BI et l'optimiseur (avec `RELY`), mais n'empêchent pas les doublons. Les tables hybrides, elles, les appliquent.

#### Que sont les séquences et les colonnes d'identité ?

Les séquences génèrent des nombres uniques (`seq.NEXTVAL`), pas forcément sans trous. Les colonnes `AUTOINCREMENT`/`IDENTITY` utilisent une séquence en interne. Beaucoup de modèles d'entrepôt préfèrent des clés de substitution par hachage, déterministes d'un chargement à l'autre.

#### À quoi sert `SAMPLE` ?

À lire une fraction aléatoire d'une table (`SELECT * FROM t SAMPLE (1)` pour 1 % des lignes, ou `SAMPLE BLOCK` par micro-partitions), pratique pour explorer et tester rapidement sur de grosses tables.

#### Que sont les fonctions définies par l'utilisateur dans Snowflake ?

Des fonctions scalaires ou de table écrites en SQL, JavaScript, Python, Java ou Scala. Les UDF Python s'exécutent dans un bac à sable sécurisé avec des paquets d'Anaconda ou des fichiers téléversés. Les UDF Python vectorisées traitent des lots avec pandas pour de meilleures performances.

#### Que sont les procédures stockées dans Snowflake ?

Des procédures écrites en Snowflake Scripting (SQL), JavaScript, Python, Java ou Scala, utilisées pour la logique procédurale et l'administration. Elles s'exécutent avec les droits du propriétaire (par défaut) ou de l'appelant.

#### Qu'est-ce que Snowflake Scripting ?

Une extension procédurale du SQL avec variables, `IF`, boucles, curseurs, gestion des exceptions et `RETURN`, utilisable dans les procédures stockées et les blocs anonymes.

#### Comment fonctionnent les transactions dans Snowflake ?

ACID, avec le niveau d'isolation read committed. Chaque instruction est validée automatiquement, sauf à l'intérieur d'un `BEGIN … COMMIT` explicite. Le DDL valide implicitement. Du DML concurrent sur la même table peut être bloqué par des verrous jusqu'à la fin de l'autre transaction.

#### Que fait `UNDROP` ?

Il restaure une table, un schéma ou une base supprimés récemment grâce au Time Travel, tant que l'on est dans la période de rétention.

#### Que fait `SWAP WITH` ?

`ALTER TABLE a SWAP WITH b` échange atomiquement les noms de deux tables, une façon courante de publier une table reconstruite sans interruption pour les lecteurs.

#### Qu'est-ce que `CREATE OR ALTER` ?

Une instruction qui crée un objet s'il n'existe pas, ou le modifie pour qu'il corresponde à la définition s'il existe, en conservant données et droits, utile pour des déploiements déclaratifs de tables et d'autres objets.

#### À quoi servent `PIVOT` et `UNPIVOT` ?

À faire pivoter des lignes en colonnes (par exemple les mois en colonnes) et des colonnes en lignes. `PIVOT` accepte des listes de valeurs dynamiques avec `ANY` dans les versions récentes.

#### Que fait `MATCH_RECOGNIZE` ?

De la reconnaissance de motifs sur des lignes ordonnées (par exemple une séquence d'événements dans une session, comme vue → panier → achat), qui renvoie les correspondances avec des mesures, sans écrire d'auto-jointures complexes.

### Time Travel, Fail-safe et clonage

#### Qu'est-ce que le Time Travel ?

L'accès aux données historiques modifiées ou supprimées, pendant une période de rétention : 1 jour par défaut, configurable jusqu'à 90 jours en Enterprise pour les tables permanentes. On peut interroger, cloner ou restaurer les données à un instant, un décalage ou une instruction donnés.

```sql
SELECT * FROM orders AT (OFFSET => -3600);
SELECT * FROM orders BEFORE (STATEMENT => '01b2c3d4-...');
CREATE TABLE orders_restored CLONE orders AT (TIMESTAMP => '2026-10-15 08:00'::TIMESTAMP_LTZ);
```

#### Qu'est-ce que le Fail-safe ?

Une période de 7 jours après le Time Travel pendant laquelle Snowflake peut récupérer les données des tables permanentes en cas de sinistre. Seul le support Snowflake y a accès ; on ne peut pas l'interroger. Il coûte du stockage, c'est pourquoi les tables transitoires (sans Fail-safe) sont moins chères.

#### Comment régler la rétention du Time Travel ?

Avec `DATA_RETENTION_TIME_IN_DAYS` au niveau du compte, de la base, du schéma ou de la table. Une rétention longue sur des tables très souvent modifiées augmente nettement les coûts de stockage.

#### Qu'est-ce que le clonage zero-copy ?

La création instantanée d'une copie d'une table, d'un schéma ou d'une base avec `CLONE`, sans copier de données : le clone partage les micro-partitions de l'original et seules les modifications ultérieures consomment du stockage. On l'utilise pour les environnements de dev et de test, les sauvegardes avant un changement risqué et les instantanés à une date donnée.

#### Qu'hérite un clone ?

Les données et la structure, et pour les bases et schémas, les objets enfants. Les droits sur l'objet source lui-même ne sont pas copiés sauf avec `COPY GRANTS` ; les droits sur les objets enfants sont clonés. Les pipes pointant vers des stages internes, et quelques autres objets, ne sont pas clonés.

#### Comment donner à un développeur une copie complète des données de production à moindre coût ?

En clonant la base de production dans une base de dev (instantanément, sans stockage supplémentaire tant qu'il n'y a pas de modifications), en appliquant des politiques de masquage ou une couche de vues sécurisées si les données sont sensibles, et en donnant au développeur un rôle sur le clone.

#### Qu'advient-il du Time Travel si l'on supprime puis recrée une table du même nom ?

La nouvelle table est distincte ; la table supprimée reste dans le Time Travel et ne peut être restaurée avec `UNDROP` qu'après avoir renommé la nouvelle, car les noms doivent être uniques.

#### Peut-on cloner à partir d'un instant passé ?

Oui : `CREATE TABLE t_clone CLONE t AT (TIMESTAMP => ...)` ou `BEFORE (STATEMENT => ...)`, dans la limite de la période de rétention. C'est une façon courante de se remettre d'un mauvais changement tout en gardant la table courante pour comparer.

### Streams, tasks et dynamic tables

#### Qu'est-ce qu'un stream ?

Un objet qui enregistre les modifications (insertions, mises à jour, suppressions) faites sur une table, une vue ou une table externe depuis sa dernière consommation, et les expose avec les colonnes `METADATA$ACTION`, `METADATA$ISUPDATE` et `METADATA$ROW_ID`. Le consommer dans une transaction DML fait avancer son offset.

#### Quels types de streams existent ?

Standard (toutes les modifications, compensées entre elles), append-only (uniquement les insertions, moins cher, pour les tables en insertion seule) et insert-only pour les tables externes et Iceberg.

#### Qu'est-ce qu'une task ?

Une unité planifiée ou déclenchée qui exécute une instruction SQL, un appel de procédure ou du Snowflake Scripting, sur un warehouse ou du calcul serverless. Les tasks peuvent être chaînées en DAG avec `AFTER` et ne s'exécuter que quand un stream contient des données grâce à `WHEN SYSTEM$STREAM_HAS_DATA(...)`.

```sql
CREATE TASK load_orders
  WAREHOUSE = transform_wh
  SCHEDULE = '15 MINUTE'
  WHEN SYSTEM$STREAM_HAS_DATA('raw.orders_stream')
AS
  INSERT INTO dw.orders SELECT * FROM raw.orders_stream WHERE METADATA$ACTION = 'INSERT';

ALTER TASK load_orders RESUME;
```

#### Qu'est-ce qu'une task serverless ?

Une task sans warehouse spécifié, dont Snowflake gère la taille de calcul d'après les exécutions précédentes. Elle convient aux petites tâches fréquentes, car il n'y a pas de facturation minimale de warehouse.

#### Qu'est-ce qu'une triggered task ?

Une task sans planning qui s'exécute quand son stream reçoit de nouvelles données, réagissant vite aux changements sans scrutation à intervalle fixe.

#### Qu'est-ce qu'une dynamic table ?

Une table définie par une requête et un retard cible (`TARGET_LAG = '10 minutes'`), que Snowflake maintient à jour automatiquement, de façon incrémentale quand c'est possible. Elle remplace de nombreux pipelines streams-et-tasks par du SQL déclaratif.

```sql
CREATE DYNAMIC TABLE dw.daily_sales
  TARGET_LAG = '30 minutes'
  WAREHOUSE = transform_wh
AS
SELECT order_date, SUM(amount) AS sales FROM dw.orders GROUP BY order_date;
```

#### Dynamic tables, vues matérialisées ou streams et tasks : comment choisir ?

Les dynamic tables pour des pipelines déclaratifs avec jointures et agrégations à la fraîcheur voulue. Les vues matérialisées pour accélérer des requêtes répétées sur une seule table (sans jointure), toujours à jour. Les streams et tasks pour une logique procédurale, une gestion personnalisée du `MERGE` ou des effets de bord.

#### Quelle est la différence entre rafraîchissement incrémental et complet des dynamic tables ?

Le rafraîchissement incrémental ne traite que les changements des sources depuis le dernier rafraîchissement ; le complet recalcule toute la requête. Snowflake choisit l'incrémental quand la requête le permet ; certaines constructions (certaines fonctions non déterministes, certains motifs de fenêtrage) imposent des rafraîchissements complets, plus coûteux.

#### Qu'est-ce qu'une vue matérialisée dans Snowflake ?

Le résultat précalculé d'une requête sur une seule table, maintenu automatiquement et de façon transparente par un service d'arrière-plan (Enterprise). L'optimiseur peut l'utiliser même quand on interroge la table de base. La maintenance coûte des crédits : on la réserve aux requêtes coûteuses et fréquentes sur des tables qui changent peu.

#### Qu'arrive-t-il à un stream non consommé pendant longtemps ?

Il peut devenir obsolète (stale) quand son offset sort de la période de rétention de la table source (Snowflake prolonge la rétention jusqu'à 14 jours pour l'éviter sur les tables ayant des streams). Un stream obsolète doit être recréé, et un rechargement complet des changements peut être nécessaire.

#### Comment superviser les tasks ?

Avec `TASK_HISTORY` (fonction de table de l'information schema et vue account usage), la vue du graphe de tasks dans Snowsight, les notifications d'erreur via une notification integration, et `SYSTEM$TASK_DEPENDENTS_ENABLE` pour reprendre des graphes entiers.

#### Qu'est-ce qu'une finalizer task ?

Une task attachée à la racine d'un graphe de tasks qui s'exécute après toutes les autres, qu'elles aient réussi ou échoué, pour le nettoyage ou les notifications.

#### Peut-on chaîner des dynamic tables ?

Oui. Une dynamic table peut lire d'autres dynamic tables et former un pipeline ; `TARGET_LAG = DOWNSTREAM` signifie qu'une table ne se rafraîchit qu'en fonction des besoins des tables qui en dépendent.

### Sécurité et contrôle d'accès

#### Comment fonctionne le contrôle d'accès dans Snowflake ?

Par un contrôle d'accès basé sur les rôles (RBAC) combiné à un contrôle discrétionnaire : les privilèges sont accordés aux rôles, les rôles aux utilisateurs et à d'autres rôles, et chaque objet a un rôle propriétaire qui le contrôle.

#### Quels sont les rôles définis par le système ?

ORGADMIN (organisation), ACCOUNTADMIN (rôle le plus élevé du compte ; à utiliser avec parcimonie), SECURITYADMIN (gère les droits et peut gérer utilisateurs et rôles), USERADMIN (crée utilisateurs et rôles), SYSADMIN (crée warehouses et bases ; les rôles personnalisés devraient lui être rattachés) et PUBLIC (accordé à tous).

#### À quoi ressemble une bonne hiérarchie de rôles ?

Des rôles d'accès qui portent les privilèges sur les objets (par exemple `SALES_READ`, `SALES_WRITE`), des rôles fonctionnels représentant des métiers ou des équipes (`ANALYST`, `DATA_ENGINEER`) auxquels on accorde les rôles d'accès, et des rôles fonctionnels rattachés à SYSADMIN pour que les administrateurs puissent tout gérer. Les comptes de service ont leurs propres rôles fonctionnels.

#### Que sont les future grants ?

Des droits appliqués automatiquement aux objets créés plus tard dans un schéma ou une base : `GRANT SELECT ON FUTURE TABLES IN SCHEMA sales.marts TO ROLE sales_read;`. Ils évitent les droits manquants sur les nouvelles tables.

#### Que sont les rôles de base de données ?

Des rôles limités à une base, utilisés pour gérer les accès à l'intérieur de celle-ci et surtout pour partager des accès fins via le partage de données.

#### Que sont les schémas à accès géré ?

Des schémas où seul le propriétaire du schéma (ou les rôles ayant `MANAGE GRANTS`) peut accorder des privilèges sur les objets, et non les propriétaires des objets, ce qui centralise le contrôle d'accès.

#### Qu'est-ce qu'une politique de masquage ?

Un objet de niveau schéma qui réécrit la valeur d'une colonne au moment de la requête selon le contexte, typiquement le rôle : les analystes voient `***@***` tandis qu'un rôle privilégié voit le vrai e-mail. On l'attache directement aux colonnes ou via des tags (Enterprise).

```sql
CREATE MASKING POLICY mask_email AS (val STRING) RETURNS STRING ->
  CASE WHEN IS_ROLE_IN_SESSION('PII_READER') THEN val ELSE '***MASKED***' END;

ALTER TABLE crm.customers MODIFY COLUMN email SET MASKING POLICY mask_email;
```

#### Qu'est-ce qu'une row access policy ?

Une politique qui indique si une ligne est visible dans le contexte courant, attachée à une table ou une vue, souvent avec une table de correspondance entre rôles et régions autorisées. Elle filtre les lignes de façon transparente pour toutes les requêtes.

#### Qu'est-ce que le masquage par tags ?

Le fait d'attacher une politique de masquage à un tag, pour que toutes les colonnes portant ce tag (par exemple `pii = 'email'`) soient masquées automatiquement, y compris les nouvelles colonnes dès qu'on les tague.

#### Qu'est-ce que la classification des données ?

Une fonction qui analyse les colonnes pour détecter les données sensibles (e-mails, noms, numéros de téléphone, identifiants nationaux) et propose ou applique des tags système, qui peuvent ensuite piloter des politiques de masquage.

#### Comment les utilisateurs s'authentifient-ils dans Snowflake ?

Par mot de passe plus MFA (que Snowflake rend obligatoire pour les connexions par mot de passe), SSO via des fournisseurs d'identité SAML 2.0 (Okta, Entra ID), OAuth (Snowflake ou externe), authentification par paire de clés pour les services, fédération d'identité de charge de travail et jetons d'accès programmatique. Les utilisateurs de service devraient utiliser des paires de clés ou OAuth, pas des mots de passe.

#### Que sont les network policies ?

Des règles qui autorisent ou bloquent des adresses IP clientes (et des network rules pour les endpoints privés) au niveau du compte ou de l'utilisateur, pour que seuls les réseaux de l'entreprise ou certains services puissent se connecter.

#### Comment les données sont-elles chiffrées dans Snowflake ?

Toujours au repos (AES-256) et en transit (TLS), avec un modèle de clés hiérarchique et une rotation automatique. Business Critical ajoute Tri-Secret Secure, qui combine une clé gérée par le client avec la clé de Snowflake.

#### Que sont les vues et UDF sécurisées ?

Des vues et fonctions dont la définition est masquée aux non-propriétaires et qui désactivent certaines optimisations susceptibles de laisser fuiter des données via le comportement des requêtes. Elles sont obligatoires pour les objets d'un share.

#### À quoi sert la vue access history ?

`SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY` enregistre les colonnes lues et écrites par chaque requête, ce qui aide l'audit, le lignage et la détection des données inutilisées.

#### Quelle est la différence entre `OWNERSHIP` et les autres privilèges ?

Le rôle propriétaire d'un objet en a le contrôle total, y compris accorder des privilèges dessus et le supprimer. Les autres privilèges (`SELECT`, `INSERT`, `USAGE`, `MONITOR`, `OPERATE`) autorisent des actions précises. La propriété se transfère avec `GRANT OWNERSHIP`.

#### Pourquoi ACCOUNTADMIN ne doit-il être le rôle par défaut de personne ?

Il a un pouvoir illimité : une erreur ou une session compromise est catastrophique. Accordez-le à quelques administrateurs avec MFA, ne l'utilisez jamais pour le travail quotidien ni pour des comptes de service, et créez les objets avec SYSADMIN ou des rôles personnalisés.

#### Que sont les rôles secondaires ?

`USE SECONDARY ROLES ALL` permet à une session d'utiliser pour ses requêtes les privilèges de tous les rôles accordés (le rôle principal reste propriétaire des objets créés), ce qui simplifie le travail des utilisateurs qui ont plusieurs rôles.

#### Que sont les external access integrations ?

Des objets qui autorisent les UDF et procédures à appeler des endpoints réseau externes, contrôlés par des network rules listant les hôtes autorisés et par des objets secret pour les identifiants.

### Partage de données et collaboration

#### Qu'est-ce que le Secure Data Sharing ?

Le partage de données vivantes en lecture seule d'un compte à un autre sans copie : le fournisseur crée un share contenant bases, schémas, tables et vues sécurisées, et le consommateur crée une base à partir de celui-ci. Le consommateur paie le calcul qu'il utilise ; le fournisseur paie le stockage.

#### Peut-on partager avec quelqu'un qui n'a pas de compte Snowflake ?

Oui, via un reader account que le fournisseur crée et paie, avec des capacités limitées.

#### Comment fonctionne le partage entre régions ou clouds ?

Les données doivent être répliquées vers un compte de la région du consommateur, ou partagées via des listings avec l'auto-fulfillment inter-cloud, qui réplique les données automatiquement.

#### Qu'est-ce que la Snowflake Marketplace ?

Un catalogue de listings où les fournisseurs publient des jeux de données gratuits ou payants, des services de données et des Native Apps que les consommateurs obtiennent directement dans leurs comptes.

#### Que sont les data clean rooms ?

Des environnements où plusieurs parties combinent leurs données pour les analyser (par exemple le recouvrement d'audiences) selon des politiques qui n'autorisent que des requêtes approuvées et des résultats agrégés, sans s'exposer mutuellement les enregistrements bruts.

#### Qu'est-ce qu'une Native App ?

Une application packagée avec du code et des données qu'un fournisseur distribue via la Marketplace et qui s'exécute dans le compte du consommateur, de sorte que les données du consommateur n'en sortent pas.

#### Que ne peut-on pas faire, en tant que consommateur, avec des données partagées ?

Les modifier, les cloner ou les repartager (sauf réglages précis du fournisseur), et le Time Travel n'est pas disponible sur les objets partagés. On peut les interroger, les joindre à ses données et créer des vues dessus.

#### Qu'est-ce qu'un listing ?

Une offre packagée d'un share ou d'une Native App avec des métadonnées, des conditions et des statistiques d'usage, publiée de façon privée à des comptes choisis ou publiquement sur la Marketplace.

### Snowpark, Python et IA

#### Qu'est-ce que Snowpark ?

Un ensemble de bibliothèques et d'environnements d'exécution pour traiter les données dans Snowflake en Python, Java ou Scala. Les opérations DataFrame sont traduites en SQL et exécutées sur un warehouse : les données ne quittent pas Snowflake.

```python
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, sum as sum_

session = Session.builder.configs(connection_params).create()
daily = (session.table("dw.orders")
         .filter(col("status") == "paid")
         .group_by("order_date")
         .agg(sum_("amount").alias("sales")))
daily.write.save_as_table("dw.daily_sales", mode="overwrite")
```

#### Qu'est-ce que l'API pandas on Snowflake ?

Une API compatible pandas (Snowpark pandas, via Modin) qui exécute du code pandas sur le calcul Snowflake, pour que la syntaxe pandas familière passe à l'échelle de grandes tables.

#### Que sont les Snowflake Notebooks ?

Des notebooks dans Snowsight qui mêlent cellules SQL, Python et Markdown et s'exécutent sur un warehouse ou sur du calcul en conteneurs, pour l'exploration, l'ingénierie des données et le ML.

#### Qu'est-ce que Snowpark Container Services ?

Un environnement de conteneurs géré dans Snowflake pour exécuter n'importe quelle application, service ou modèle de ML conteneurisé (y compris sur GPU) près des données, sous la sécurité de Snowflake.

#### Qu'est-ce que Snowflake Cortex ?

La couche d'IA de Snowflake : des fonctions LLM appelables en SQL (`AI_COMPLETE`, `AI_CLASSIFY`, `AI_EXTRACT`, `AI_SENTIMENT`, résumé, traduction), Cortex Search pour la recherche, Cortex Analyst pour les questions en langage naturel sur des modèles sémantiques, et des agents.

#### Qu'est-ce que Streamlit in Snowflake ?

Un moyen de construire et d'héberger des applications de données Streamlit directement dans Snowflake, exécutées avec la gouvernance du compte et partagées via des rôles.

#### Qu'est-ce que l'écosystème ML de Snowflake ?

Snowflake ML comprend un feature store, un registre de modèles, l'entraînement et l'inférence distribués sur warehouses ou conteneurs et l'observabilité ML, pour construire et servir les modèles là où sont les données.

#### Quand utiliser Snowpark plutôt que SQL ?

Pour une logique plus simple en Python (règles complexes de texte ou métier, ingénierie de features pour le ML, réutilisation de bibliothèques Python), pour du code de transformation testable unitairement, ou pour des équipes plus à l'aise avec les DataFrames. Pour des transformations simples, SQL est souvent plus simple et aussi rapide.

#### Comment les paquets Python arrivent-ils dans Snowflake ?

Depuis le canal Anaconda de Snowflake (listés dans `PACKAGES`), depuis des wheels ou zips téléversés dans un stage (`IMPORTS`), ou via des dépôts d'artefacts qui récupèrent des paquets de PyPI.

### Performances

#### Comment savoir pourquoi une requête est lente ?

Ouvrez le Query Profile : regardez les opérateurs les plus coûteux, les partitions lues par rapport au total (pruning), les octets déversés (spill) en stockage local et distant, les jointures qui explosent (beaucoup plus de lignes en sortie qu'en entrée) et le temps d'attente. `GET_QUERY_OPERATOR_STATS` fournit les mêmes données en SQL.

#### Qu'est-ce que le spilling, et comment le corriger ?

Quand un warehouse manque de mémoire pour une opération, il déverse sur le disque local puis sur le stockage distant, bien plus lent. On le corrige avec un warehouse plus gros, en traitant moins de données (meilleurs filtres, pré-agrégation) ou en découpant la requête.

#### Qu'est-ce qui provoque une « jointure qui explose » ?

Une jointure sur une clé non unique, ou des conditions de jointure manquantes, de sorte que chaque ligne correspond à de nombreuses autres et que la sortie se multiplie. Vérifiez l'unicité des clés et que chaque jointure a sa condition complète.

#### Comment améliorer le pruning ?

En filtrant sur des colonnes corrélées à l'ordre de chargement (les dates), en ajoutant une clé de clustering sur les grandes tables filtrées par d'autres colonnes, en évitant d'envelopper les colonnes de filtre dans des fonctions qui empêchent le pruning, et en filtrant le plus tôt possible.

#### Qu'est-ce que le Search Optimization Service ?

Une fonction Enterprise qui construit un chemin d'accès de recherche persistant pour une table, afin que les recherches ponctuelles et les filtres sélectifs (égalité, `IN`, recherches de sous-chaînes et regex, champs `VARIANT`, géo) puissent écarter la plupart des micro-partitions. Elle coûte du stockage et des crédits de maintenance.

#### Pourquoi éviter `SELECT *` dans Snowflake ?

Le stockage est en colonnes : ne lire que les colonnes utiles réduit énormément les données lues. `SELECT *` sur des tables larges lit toutes les colonnes et ralentit les requêtes et les extractions BI.

#### Comment accélérer de nombreuses petites instructions `INSERT` ?

En ne les faisant pas : Snowflake est optimisé pour les opérations ensemblistes. Regroupez les lignes en fichiers et utilisez `COPY`, Snowpipe Streaming pour des lignes continues, ou des insertions en grandes instructions multi-lignes.

#### Un `ORDER BY` dans un `CREATE TABLE AS` est-il utile ?

Oui, pour le chargement initial de grandes tables : trier par les principales colonnes de filtre produit dès le départ des micro-partitions bien regroupées, ce qui améliore le pruning sans payer le clustering automatique.

#### Quelles erreurs fréquentes rendent Snowflake lent ?

Du DML ligne à ligne en boucle, `SELECT *`, des fonctions sur les colonnes de filtre, des jointures entre types différents, d'énormes listes `IN`, des warehouses trop petits qui déversent, des warehouses trop gros pour des requêtes triviales (coût) et des vues complexes empilées sur de nombreux niveaux.

#### Que montre `EXPLAIN` dans Snowflake ?

Le plan logique d'une requête sans l'exécuter : opérateurs, ordre des jointures et partitions à lire (d'après les métadonnées), utile pour vérifier le pruning avant de lancer une requête coûteuse.

#### Comment accélérer une requête `DISTINCT` sur d'énormes volumes ?

En vérifiant si la déduplication est vraiment nécessaire (souvent une jointure a multiplié les lignes), en dédupliquant plus tôt et sur moins de colonnes, en utilisant `APPROX_COUNT_DISTINCT` (HyperLogLog) quand une estimation suffit, et un warehouse plus gros s'il y a du spill.

#### À quoi servent les fonctions approximatives ?

`APPROX_COUNT_DISTINCT`, `APPROX_PERCENTILE` et `APPROX_TOP_K` donnent des estimations avec une faible erreur en utilisant bien moins de mémoire et de temps, ce qui convient aux dashboards et à l'exploration sur de très grosses tables.

### Maîtrise des coûts

#### Qu'est-ce qui fait les coûts de Snowflake ?

Le calcul des warehouses (de loin le poste principal pour la plupart des clients), les fonctions serverless (Snowpipe, clustering, vues matérialisées, search optimization, tasks, fonctions d'IA), le stockage (y compris Time Travel et Fail-safe), les services cloud au-delà de 10 % du calcul, et le transfert de données hors de la région.

#### Qu'est-ce qu'un resource monitor ?

Un objet qui suit la consommation de crédits de warehouses ou du compte sur une période et peut notifier, suspendre après la fin des requêtes en cours, ou suspendre immédiatement quand des seuils sont atteints.

```sql
CREATE RESOURCE MONITOR monthly_bi WITH CREDIT_QUOTA = 500
  FREQUENCY = MONTHLY START_TIMESTAMP = IMMEDIATELY
  TRIGGERS ON 80 PERCENT DO NOTIFY
           ON 100 PERCENT DO SUSPEND;
ALTER WAREHOUSE bi_wh SET RESOURCE_MONITOR = monthly_bi;
```

#### Comment voir où partent les crédits ?

Avec `SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY`, `QUERY_HISTORY` (avec `QUERY_ATTRIBUTION_HISTORY` pour le coût par requête), `METERING_DAILY_HISTORY` pour les fonctions serverless, les pages de gestion des coûts de Snowsight, les budgets, et les tags d'objets ou de requêtes pour l'attribution.

#### Que sont les query tags ?

Un paramètre de session (`ALTER SESSION SET QUERY_TAG = 'dbt:daily_sales'`) stocké avec chaque requête dans l'historique, utilisé pour attribuer les coûts et retrouver les requêtes par job, outil ou équipe.

#### Que sont les budgets dans Snowflake ?

Des plafonds de dépense pour le compte ou des groupes d'objets, avec des notifications quand la dépense projetée dépasse le plafond, pour aider les équipes à suivre les coûts serverless et des warehouses.

#### Comment réduire les coûts des warehouses ?

Dimensionner chaque warehouse selon sa charge, utiliser un auto-suspend court, éviter les warehouses toujours allumés, regrouper les petits jobs sur des warehouses partagés, utiliser le multi-cluster en politique Economy là où l'attente est acceptable, fixer des timeouts, optimiser les requêtes les plus coûteuses et utiliser des resource monitors.

#### Comment réduire les coûts de stockage ?

Utiliser des tables transitoires pour le staging et les données reconstructibles, raccourcir le Time Travel des tables très modifiées, supprimer les tables inutilisées et les clones qui ont divergé, nettoyer les anciens fichiers des stages, et éviter de garder de multiples copies complètes au lieu de clones.

#### Un warehouse plus gros est-il toujours plus cher ?

Pas forcément. Si une requête se parallélise bien, doubler la taille divise la durée par deux pour un tarif doublé : le coût est similaire et le résultat arrive plus tôt. C'est plus cher quand les requêtes sont petites ou ne se parallélisent pas.

#### Pourquoi un warehouse qui exécute une requête d'une seconde chaque minute coûte-t-il cher ?

Chaque reprise facture au moins 60 secondes, et l'auto-suspend le garde allumé pendant le temps d'inactivité configuré après chaque requête. Une requête par minute peut le laisser allumé en permanence. Regroupez ces requêtes, utilisez des tasks serverless ou un seul petit warehouse partagé.

#### Comment fonctionne l'ajustement des services cloud ?

L'usage des services cloud est gratuit jusqu'à 10 % du calcul quotidien des warehouses ; seul l'excédent est facturé. Les opérations lourdes en métadonnées (beaucoup de requêtes minuscules, commandes `SHOW`, clones fréquents) peuvent le dépasser.

### Exploitation et protection des données

#### Quelle est la différence entre `ACCOUNT_USAGE` et `INFORMATION_SCHEMA` ?

Les vues `SNOWFLAKE.ACCOUNT_USAGE` couvrent tout le compte, gardent un an d'historique et incluent les objets supprimés, mais ont de la latence (de quelques minutes à quelques heures). Les vues et fonctions de table de l'`INFORMATION_SCHEMA` sont par base, en temps réel, avec un historique plus court (7 à 14 jours pour l'historique des requêtes).

#### Qu'est-ce que la réplication de bases ?

La copie de bases (et, avec les groupes de réplication, d'autres objets comme les utilisateurs, rôles, warehouses et intégrations) vers des comptes d'autres régions ou clouds, rafraîchie selon un planning, pour la reprise après sinistre, le partage de données ou les migrations.

#### Que sont les failover groups et le client redirect ?

Les failover groups (Business Critical) permettent de promouvoir un compte secondaire en primaire pour les objets répliqués pendant une panne. Le client redirect utilise une URL de connexion qu'on peut basculer vers le nouveau primaire, pour que les applications se reconnectent sans changer leur configuration.

#### Comment gérer les objets Snowflake sous forme de code ?

Avec Terraform (le provider Snowflake) pour les objets de compte comme les warehouses, rôles, droits, bases et intégrations ; dbt ou schemachange pour les changements de schéma et les transformations ; et la Snowflake CLI ou `EXECUTE IMMEDIATE FROM` avec des dépôts Git dans Snowflake pour déployer des fichiers SQL.

#### Qu'est-ce qu'un objet Git repository dans Snowflake ?

Une intégration qui clone un dépôt Git dans Snowflake pour y exécuter des fichiers SQL et Python, les référencer dans des notebooks et des procédures, et déployer depuis une branche ou un tag.

#### Comment alerter sur des problèmes de données dans Snowflake ?

Avec les alerts (conditions planifiées qui déclenchent une action comme l'envoi d'un e-mail ou d'une notification webhook), les data metric functions (supervision de la qualité des données Horizon : nulls, doublons, fraîcheur, métriques personnalisées) et les notifications d'échec des tasks.

#### Que sont les data metric functions ?

Des fonctions (système, comme `NULL_COUNT`, `DUPLICATE_COUNT`, `FRESHNESS`, ou personnalisées) attachées à des tables et exécutées selon un planning, dont les résultats sont conservés pour suivre la qualité des données dans le temps.

#### Qu'est-ce que l'event table ?

Une table spéciale qui collecte les journaux, traces et métriques émis par les UDF, procédures, Native Apps et Snowpark Container Services, pour superviser le code applicatif qui tourne dans Snowflake.

#### Comment sauvegarder les données Snowflake ?

Le Time Travel et le Fail-safe couvrent les erreurs récentes et les sinistres ; pour une protection plus longue, utilisez des clones zero-copy planifiés, des sauvegardes (ensembles de copies immuables à un instant donné, là où c'est disponible), la réplication vers une autre région, ou le déchargement vers un stockage cloud.

#### Comment déployer du SQL en sécurité ?

Versionner le SQL dans Git, déployer depuis la CI avec un utilisateur de service (paire de clés ou OAuth), utiliser `CREATE OR ALTER` ou des outils de migration (schemachange, dbt, Terraform), tester d'abord sur une base clonée, et garder des scripts de retour arrière ou s'appuyer sur le Time Travel et les clones.

### Modélisation et intégration

#### La modélisation en étoile est-elle toujours utile dans Snowflake ?

Oui. Snowflake gère bien les jointures et le stockage est bon marché, mais les schémas en étoile rendent toujours l'analytique plus simple, cohérente et rapide pour les outils de BI. Beaucoup d'équipes adoptent une approche en couches : raw, staging, intermédiaire et marts avec faits et dimensions, souvent construits avec dbt.

#### Faut-il normaliser ou dénormaliser dans Snowflake ?

Normaliser là où l'intégrité et la réutilisation comptent (entités centrales), dénormaliser pour la consommation (marts larges, une grande table pour des dashboards précis). Le stockage en colonnes rend les tables larges peu coûteuses à interroger quand on ne lit que quelques colonnes.

#### Comment dbt fonctionne-t-il avec Snowflake ?

dbt compile les modèles en SQL et les exécute sur un warehouse Snowflake via l'adaptateur dbt-snowflake, qui prend en charge les tables, vues, modèles incrémentaux (`merge`, `delete+insert`, `append`, `microbatch`), dynamic tables, tables transitoires, query tags et réglages de clustering.

#### Comment Spark et Snowflake s'intègrent-ils ?

Via le connecteur Spark, qui lit et écrit les tables Snowflake avec poussée des requêtes (pushdown), ou en partageant des tables Iceberg via un catalogue pour que Spark et Snowflake travaillent sur les mêmes fichiers.

#### Comment implémenter une SCD de type 2 dans Snowflake ?

Avec un `MERGE` qui clôt les lignes courantes modifiées et insère les nouvelles versions (souvent deux instructions ou l'astuce de l'union), avec des streams et des tasks pour le traitement incrémental, ou avec les snapshots dbt, qui le gèrent automatiquement.

#### Qu'est-ce que l'approche « one big table », et quand convient-elle ?

Une table large et dénormalisée contenant tout ce dont un cas d'usage a besoin, rapide à interroger dans un moteur en colonnes et simple pour la BI. Elle convient à des cas d'usage stables et précis ; pour l'analytique générale, les schémas en étoile restent plus souples et cohérents.

#### Comment modéliser des données de référence à évolution lente partagées par de nombreux marts ?

Sous forme de dimensions conformes portées par un seul modèle, avec clés de substitution et historique SCD si besoin, référencées par tous les marts pour que tous les rapports utilisent les mêmes définitions.

### Mises en situation

#### Concevez un pipeline d'ingestion d'événements S3 vers des tables de reporting Snowflake.

Une storage integration et un stage externe sur le préfixe S3, un Snowpipe en auto-ingest à partir des notifications d'événements S3 vers une table raw typée ou en `VARIANT`, un stream sur la table raw, et des dynamic tables (ou des tasks avec `MERGE`) qui construisent les tables nettoyées et agrégées à la fraîcheur requise. J'ajoute des data metric functions, des alertes et des resource monitors, et je gère le tout sous forme de code.

#### Un warehouse de dashboards sature chaque lundi à 9 h. Que faites-vous ?

J'en fais un warehouse multi-cluster avec assez de clusters maximum (politique Standard pour les utilisateurs interactifs), je regarde si les requêtes lentes peuvent être optimisées ou servies par des agrégats, et je sépare les autres charges qui utilisent le même warehouse à ce moment-là.

#### Une requête lit 98 % des partitions d'une table de 5 To alors qu'elle filtre sur `customer_id`. Comment corriger ?

La table n'est pas regroupée par `customer_id`. Pour des recherches ponctuelles, j'active la search optimization sur cette colonne ; pour des filtres par plage fréquents, j'ajoute une clé de clustering (éventuellement combinée à la date) ; sinon je revois la requête ou je crée une table pré-agrégée.

#### Quelqu'un a lancé `DELETE FROM orders` sans `WHERE` il y a une heure. Comment récupérer ?

Avec le Time Travel : je réinsère les lignes depuis `orders AT (OFFSET => -3600)` ou `BEFORE (STATEMENT => '<query id>')`, ou je clone la table à cet instant et je l'échange avec `ALTER TABLE … SWAP WITH`. Ensuite je restreins les droits de suppression sur les tables de production.

#### Les coûts ont augmenté de 40 % ce mois-ci. Comment enquêtez-vous ?

Je compare `WAREHOUSE_METERING_HISTORY` et la consommation serverless par service et par warehouse, je repère les warehouses et query tags en hausse, j'examine `QUERY_ATTRIBUTION_HISTORY` pour les requêtes les plus coûteuses, et je cherche des warehouses qui ne se suspendent plus, de nouvelles dynamic tables au lag très court, du reclustering sur des tables très modifiées ou des rafraîchissements complets.

#### Les analystes de chaque pays ne doivent voir que leurs lignes et pas les e-mails. Comment ?

Une row access policy sur les tables avec une table de correspondance entre rôles et pays, et une politique de masquage (ou un masquage par tags) sur les colonnes e-mail qui ne révèle les valeurs qu'à un rôle privilégié. Les analystes reçoivent des rôles fonctionnels associés à leur pays.

#### Comment migrer un entrepôt de données on-premise vers Snowflake ?

Inventorier les objets, les charges et les dépendances ; traduire le DDL et le SQL (SnowConvert aide) ; transférer l'historique via le stockage cloud et `COPY` ; mettre en place le chargement incrémental ; reconstruire les transformations (souvent en dbt) ; recréer la sécurité avec rôles et politiques ; valider par comptages de lignes, sommes de contrôle et comparaisons de rapports ; faire tourner les deux en parallèle avant la bascule ; puis optimiser warehouses et coûts.

#### Une équipe veut traiter 2 To de logs JSON par jour. Comment les charger et les modéliser ?

Déposer dans S3 des fichiers compressés d'environ 100 à 250 Mo, les charger avec Snowpipe ou un `COPY` planifié dans une colonne `VARIANT` d'une table raw transitoire, extraire les champs courants en colonnes typées dans une table nettoyée regroupée par date d'événement, et agréger dans des marts. Garder les données raw peu de temps si elles peuvent être rechargées depuis S3.

#### Comment expliquer la valeur de Snowflake à un interlocuteur métier ?

Un seul endroit gouverné pour les données de l'entreprise, qui passe instantanément à l'échelle pour n'importe quel nombre d'utilisateurs, ne coûte rien quand il ne sert pas, et permet aux équipes de partager et d'analyser les mêmes chiffres sans gérer de serveurs.

#### Un `MERGE` nocturne sur une table de 3 To prend des heures. Que vérifiez-vous ?

Si la cible est élaguée (ajouter un filtre de date ou de plage de clés dans la clause `ON`, regrouper par la clé de merge), si la source contient des doublons ou est bien plus grosse que les changements, la taille du warehouse et le spill, et si une approche incrémentale (streams, `delete+insert` sur les partitions récentes) convient mieux.

#### Un Snowpipe charge parfois des lignes en double. Pourquoi, et que faites-vous ?

Les mêmes données sont arrivées dans des fichiers différents (relances du producteur, fichiers renommés), ou des fichiers ont été rechargés avec `FORCE`. Je fais écrire aux producteurs des noms de fichiers déterministes, je déduplique en aval sur une clé métier avec `QUALIFY` et je garde la couche raw en ajout seul, avec les métadonnées de fichier pour la traçabilité.

#### Comment donner à un partenaire l'accès à un jeu de données choisi sans le copier ?

Je crée des vues sécurisées sur les tables choisies, je les mets dans un share (ou un listing privé) et j'ajoute le compte du partenaire comme consommateur ; s'il n'a pas de compte Snowflake, je crée un reader account. J'utilise des row access policies ou des vues séparées pour limiter ce qu'il voit.
