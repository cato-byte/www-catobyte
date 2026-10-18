## Fiche d'étude Snowflake

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude Snowflake : environ 200 questions](../../images/snowflake_study_guide_title_img.png)

Environ 200 questions d'entretien sur Snowflake, de son architecture aux virtual warehouses, aux micro-partitions, au chargement, aux données semi-structurées, aux streams et tasks, aux dynamic tables, à la sécurité, au partage de données, aux performances et à la maîtrise des coûts. Les réponses décrivent la plateforme telle qu'elle est en 2026.

La fiche suit un parcours d'apprentissage en six étapes. Chaque section est découpée en unités courtes : objectifs d'apprentissage, explication du concept et exemple commenté, puis questions (d'abord de mémorisation, ensuite d'application), un exercice pratique et les points à retenir. Pour **apprendre**, lisez chaque unité du début à la fin. Pour **réviser**, passez en mode révision ou utilisez « Aller aux questions », marquez les réponses à revoir et essayez une révision mixte entre les sections.

<!-- QA -->
<!-- stage: Fondamentaux -->

### Architecture

<!-- unit: Les trois couches de Snowflake -->

<!-- goals -->

- Décrire les couches stockage, calcul et services cloud de Snowflake.
- Expliquer la séparation stockage/calcul et ce qui la distingue du MPP classique.

<!-- concept -->

Les entrepôts classiques lient les données aux machines qui les traitent : toutes les charges se disputent le même cluster et passer à l'échelle impose de déplacer des données. Snowflake découpe le problème en trois. Les données vivent une seule fois dans un stockage cloud central. Des clusters de calcul indépendants, les virtual warehouses, les lisent sans se gêner. Une couche de services gère tout ce qui entoure les requêtes : sécurité, métadonnées, optimisation et transactions.
Résultat : un entrepôt sans réglage physique, où l'on dimensionne le calcul par charge et ne paie que pendant son exécution.

<!-- example -->

```text
cloud services: auth · metadata · optimizer · transactions
      │
compute:   WH_LOAD (M)    WH_TRANSFORM (L)    WH_BI (S, multi-cluster)
      │            │                │                 │
storage:   one copy of the data in micro-partitions on S3 / Azure Blob / GCS
```

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

<!-- challenge -->

Les chargements nocturnes ralentissent les tableaux de bord du matin sur l'entrepôt actuel de l'entreprise. Comment l'architecture de Snowflake y répondrait-elle ?

<!-- solution -->

En donnant au chargement et à la BI des virtual warehouses séparés : tous deux lisent et écrivent le même stockage, mais avec un calcul indépendant, et les chargements ne concurrencent plus les requêtes des tableaux de bord.

<!-- takeaways -->

- Stockage, calcul et services sont des couches séparées.
- Plusieurs warehouses partagent une seule copie des données.
- Le calcul se dimensionne par charge et se paie pendant l'exécution.

<!-- unit: Comptes et objets -->

<!-- goals -->

- Naviguer entre organisations, comptes, bases, schémas et éditions.
- Utiliser identifiants de compte, régions et contextes de session.

<!-- concept -->

Tout dans Snowflake s'inscrit dans une hiérarchie : une organisation contient des comptes, chaque compte vit dans une région cloud et contient des bases, qui contiennent des schémas, qui contiennent tables, vues, stages et autres objets. Warehouses, utilisateurs et rôles vivent au niveau du compte.
Les éditions décident des fonctionnalités d'un compte, et une session s'exécute toujours dans un contexte : rôle, warehouse, base et schéma courants, ce qui explique la plupart des surprises « object does not exist ».

<!-- example -->

```sql
USE ROLE transformer;
USE WAREHOUSE wh_transform;
USE SCHEMA analytics.marts;
SELECT CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_ROLE(), CURRENT_WAREHOUSE();
```

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

<!-- challenge -->

Une requête échoue avec « Object does not exist or not authorized », alors qu'un collègue voit la table. Que vérifiez-vous d'abord ?

<!-- solution -->

Le contexte de session et le rôle : le rôle courant manque peut-être de privilèges, ou le contexte base/schéma diffère. Vérifier `CURRENT_ROLE()`, utiliser le nom entièrement qualifié et contrôler les grants.

<!-- takeaways -->

- Organisation → compte → base → schéma → objets.
- Chaque compte vit dans une région cloud.
- Rôle, warehouse, base et schéma forment le contexte de session.

<!-- unit: Crédits et warehouses -->

<!-- goals -->

- Expliquer virtual warehouses et crédits.
- Relier la taille des warehouses à la consommation de crédits.

<!-- concept -->

Un virtual warehouse est du calcul qu'on allume et éteint. Tant qu'il tourne, il consomme des crédits, facturés à la seconde après une première minute. Chaque taille double à la fois la puissance et le débit de crédits : le prix horaire d'un gros warehouse est élevé, mais une requête qui se parallélise bien finit deux fois plus vite pour à peu près le même coût.
Le dimensionnement devient donc une décision de vitesse plus que de coût, tant que les warehouses se suspendent quand ils sont inactifs.

<!-- example -->

| Taille | Crédits/heure | Requête qui se parallélise bien |
|---|---|---|
| X-Small | 1 | 16 min → 0,27 crédit |
| Small | 2 | 8 min → 0,27 crédit |
| Medium | 4 | 4 min → 0,27 crédit |
| Large | 8 | 2 min → 0,27 crédit |

#### Qu'est-ce que Snowsight ?

L'interface web de Snowflake pour écrire des worksheets SQL et Python, des notebooks et des dashboards, explorer les données, surveiller les requêtes et les coûts, et administrer le compte.

#### Qu'est-ce que Snowflake Horizon ?

Les capacités intégrées de gouvernance et de catalogue de Snowflake : contrôle d'accès, classification des données sensibles, politiques de masquage et d'accès aux lignes, tags, lignage, supervision de la qualité des données, audit et découverte, appliqués aux tables, aux tables Iceberg et aux données partagées.

#### Quelle est la différence entre Snowflake et un entrepôt MPP traditionnel comme Teradata ou Redshift (provisionné) ?

Les entrepôts MPP traditionnels couplent stockage et calcul sur les mêmes nœuds : monter en charge implique de redistribuer les données, et toutes les charges partagent un cluster. Snowflake garde le stockage centralisé et permet de démarrer des warehouses indépendants en quelques secondes, sans index, clés de distribution ni vacuum à gérer.

<!-- challenge -->

Une transformation prend 40 minutes sur un warehouse Small. L'équipe craint qu'un Large quadruple le coût. Que lui expliquez-vous ?

<!-- solution -->

Si la requête se parallélise, un Large (4× le débit) finit en environ un quart du temps : les crédits restent proches et les résultats arrivent plus vite. Le tester et comparer les crédits dans l'historique des requêtes.

<!-- takeaways -->

- Les warehouses consomment des crédits à la seconde quand ils tournent.
- Chaque taille double puissance et prix.
- Plus gros peut être plus rapide pour un coût similaire.

<!-- unit: Outils et gouvernance -->

<!-- goals -->

- Se connecter à Snowflake avec Snowsight, le CLI et les drivers.
- Décrire les fonctions de gouvernance de Snowflake Horizon.

<!-- concept -->

On accède à Snowflake par de nombreuses portes : l'interface web Snowsight pour worksheets, notebooks et tableaux de bord ; des outils en ligne de commande pour les scripts et déploiements ; des drivers et connecteurs pour applications, outils BI et pipelines.
La gouvernance est intégrée à la plateforme sous le nom Horizon : contrôle d'accès, classification, politiques, lignage et audit, pour que sécurité et découverte ne dépendent pas d'un outil séparé.

<!-- example -->

```bash
snow connection test --connection prod
snow sql -q "SELECT count(*) FROM analytics.marts.fct_orders" --connection prod
```
```python
import snowflake.connector
conn = snowflake.connector.connect(account="myorg-prod", user="etl_svc",
                                   authenticator="SNOWFLAKE_JWT", private_key_file="rsa_key.p8")
```

#### Quel est le rôle de l'URL et du localisateur du compte ?

L'identifiant de compte (nom de l'organisation plus nom du compte, ou l'ancien localisateur avec la région) forme l'URL à laquelle se connectent les clients, par exemple `myorg-myaccount.snowflakecomputing.com`.

#### Qu'est-ce que le contexte d'une session Snowflake ?

Le rôle, le warehouse, la base et le schéma courants d'une session (`USE ROLE`, `USE WAREHOUSE`, `USE DATABASE`, `USE SCHEMA`). Les requêtes s'exécutent avec les privilèges du rôle courant sur le warehouse courant, et les noms non qualifiés se résolvent dans la base et le schéma courants.

#### Qu'est-ce qu'une micro-partition ?

L'unité physique de stockage d'une table Snowflake : un fichier immuable de 50 à 500 Mo de données non compressées (bien moins une fois compressé), stocké en colonnes. Snowflake les crée automatiquement au chargement, dans l'ordre d'arrivée des données.

<!-- challenge -->

Un pipeline se connecte avec un nom d'utilisateur et un mot de passe stockés dans un fichier de configuration. Quelle méthode d'authentification un utilisateur de service devrait-il utiliser ?

<!-- solution -->

L'authentification par key pair (ou OAuth/workload identity), avec la clé privée dans un gestionnaire de secrets : aucun mot de passe stocké ni invite MFA pour l'automatisation.

<!-- takeaways -->

- Snowsight, CLI et drivers couvrent tous les accès.
- Les utilisateurs de service utilisent key pairs ou OAuth.
- Horizon intègre la gouvernance à la plateforme.

### Stockage et micro-partitions

<!-- unit: Micro-partitions et élagage -->

<!-- goals -->

- Expliquer les micro-partitions, leurs métadonnées et leur compression.
- Décrire l'élagage et l'effet des mises à jour sur un stockage immuable.

<!-- concept -->

Snowflake stocke les tables sous forme de nombreux petits fichiers immuables, les micro-partitions, chacune contenant une tranche de lignes stockée par colonne et compressée automatiquement. Pour chacune, il enregistre des métadonnées comme les valeurs minimale et maximale de chaque colonne.
Ces métadonnées rendent les requêtes rapides sans index : un filtre sur une colonne permet d'ignorer toute micro-partition dont la plage ne peut pas correspondre. Les fichiers ne changeant jamais, mises à jour et suppressions écrivent de nouvelles micro-partitions, ce qui rend aussi bon marché Time Travel et clonage.

<!-- example -->

```text
orders: 12,000 micro-partitions
WHERE order_date = '2026-10-17'
  micro-partition 0001: order_date 2024-01-01..2024-01-03 → skip
  ...
  micro-partition 11,880: order_date 2026-10-16..2026-10-17 → scan
Query Profile: partitions scanned 14 of 12,000
```

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

<!-- challenge -->

Une requête sur une table de 2 To filtre sur `order_date` et parcourt 14 partitions sur 12 000. Une autre filtre sur `customer_id` et en parcourt 11 500. Pourquoi cette différence ?

<!-- solution -->

Les données ont été chargées dans l'ordre des dates : chaque micro-partition couvre une plage de dates étroite et l'élagage fonctionne ; les ID clients sont répartis sur toutes les partitions, leurs plages min/max se chevauchent et presque rien n'est ignoré.

<!-- takeaways -->

- Les tables sont des micro-partitions immuables et compressées.
- Les métadonnées min/max permettent l'élagage.
- Les mises à jour écrivent de nouvelles micro-partitions.

<!-- unit: Clustering -->

<!-- goals -->

- Expliquer le clustering naturel et les clustering keys.
- Décider quand regrouper, vérifier le clustering et maîtriser son coût.

<!-- concept -->

L'élagage ne fonctionne que si les valeurs similaires se trouvent dans les mêmes micro-partitions. Des données chargées dans l'ordre du temps sont naturellement regroupées par date, sans coût. Pour d'autres colonnes de filtre sur de très grandes tables, une clustering key demande à Snowflake de réorganiser les données en arrière-plan, ce qui coûte des crédits tant que la table change.
Le clustering est donc un arbitrage : rentable sur des tables de plusieurs téraoctets avec des filtres sélectifs fréquents, inutile sur des tables petites ou rarement interrogées.

<!-- example -->

```sql
ALTER TABLE events CLUSTER BY (event_date, customer_id);
SELECT SYSTEM$CLUSTERING_INFORMATION('events', '(event_date, customer_id)');
-- average_depth falling toward 1–2 means good clustering
ALTER TABLE events SUSPEND RECLUSTER;   -- pause during a big backfill
```

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

<!-- challenge -->

Une équipe ajoute des clustering keys à toutes les tables de plus de 1 Go, et les crédits d'automatic clustering s'envolent. Que conseillez-vous ?

<!-- solution -->

Retirer les clés des tables petites ou peu filtrées (le clustering naturel et les parcours complets y coûtent peu) et ne les garder que sur les très grandes tables aux filtres sélectifs fréquents, en vérifiant le gain dans les query profiles.

<!-- takeaways -->

- Le clustering naturel issu de l'ordre de chargement est gratuit.
- Les clustering keys réorganisent les données, à un coût.
- Ne regroupez que les grandes tables souvent filtrées.

<!-- unit: Types de tables et coût du stockage -->

<!-- goals -->

- Choisir entre tables permanentes, transient, temporaires, Iceberg, hybrides et externes.
- Comprendre la facturation du stockage, du Time Travel et du Fail-safe.

<!-- concept -->

Les types de tables arbitrent entre protection, emplacement et adéquation à la charge. Les tables permanentes ont Time Travel et Fail-safe ; les tables transient et temporaires n'ont pas de Fail-safe, ce qui économise du stockage pour des données reconstructibles. Les tables Iceberg gardent les données au format ouvert dans votre stockage ; les tables hybrides servent des opérations rapides par ligne ; les tables externes lisent les fichiers sur place.
Le stockage est facturé en octets compressés, historique du Time Travel et du Fail-safe compris, qui peut dépasser les données actives sur des tables qui changent sans cesse.

<!-- example -->

```sql
CREATE TRANSIENT TABLE staging.orders_raw (...) DATA_RETENTION_TIME_IN_DAYS = 0;
SELECT table_name, active_bytes, time_travel_bytes, failsafe_bytes
FROM snowflake.account_usage.table_storage_metrics
ORDER BY failsafe_bytes DESC LIMIT 10;
```

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

#### Que se passe-t-il quand un warehouse est suspendu ?

Il cesse de consommer des crédits et son cache local est vidé. Avec l'auto-resume, la requête suivante le relance en une ou deux secondes.

<!-- challenge -->

Une table de staging est entièrement rechargée toutes les heures, et son stockage Fail-safe vaut dix fois sa taille active. Que changez-vous ?

<!-- solution -->

En faire une table transient avec un Time Travel court (ou nul) : elle est reconstructible, n'a pas besoin de Fail-safe, et les réécritures horaires cessent d'accumuler du stockage historique.

<!-- takeaways -->

- Les tables permanentes ont Time Travel et Fail-safe.
- Les tables transient conviennent aux données reconstructibles.
- Iceberg, hybrides et externes répondent à des besoins précis.

### Virtual warehouses et calcul

<!-- unit: Cycle de vie des warehouses -->

<!-- goals -->

- Configurer auto-suspend, auto-resume et statement timeouts.
- Choisir une taille initiale et comprendre le redimensionnement.

<!-- concept -->

Les warehouses ne coûtent que lorsqu'ils tournent : leurs réglages de cycle de vie comptent plus que leur taille. L'auto-suspend les arrête après une courte inactivité ; l'auto-resume les relance à l'arrivée d'une requête. La suspension vide aussi le cache local, si bien que des délais très courts peuvent ralentir les requêtes répétées.
Dimensionner est une expérience : partir petit, mesurer des requêtes représentatives et ajuster. Redimensionner concerne les nouvelles requêtes ; celles en cours finissent là où elles ont commencé. Les timeouts arrêtent les requêtes incontrôlées avant qu'elles ne brûlent des crédits.

<!-- example -->

```sql
CREATE WAREHOUSE wh_transform
  WAREHOUSE_SIZE = 'SMALL'
  AUTO_SUSPEND = 60          -- seconds
  AUTO_RESUME = TRUE
  STATEMENT_TIMEOUT_IN_SECONDS = 3600
  INITIALLY_SUSPENDED = TRUE;
```

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

<!-- challenge -->

Un warehouse de développement tourne 24 h/24 avec l'auto-suspend désactivé. Que changez-vous, et quel est le compromis ?

<!-- solution -->

Activer l'auto-suspend (par exemple 60 à 300 secondes) et l'auto-resume. Le compromis : quelques secondes de reprise et un cache froid après inactivité, bien moins cher que payer des heures d'inactivité.

<!-- takeaways -->

- Auto-suspend et auto-resume maîtrisent le coût d'inactivité.
- Partez petit, mesurez, redimensionnez.
- Les timeouts arrêtent les requêtes incontrôlées.

<!-- unit: Montée en charge et concurrence -->

<!-- goals -->

- Choisir entre agrandir et multiplier avec les warehouses multi-cluster.
- Réduire les files d'attente et séparer les charges.

<!-- concept -->

Deux problèmes se ressemblent mais appellent des remèdes différents. Une seule requête lourde et lente a besoin d'un warehouse plus grand : plus de mémoire, moins de débordement. De nombreuses requêtes concurrentes en attente ont besoin de plus de clusters de même taille : un warehouse multi-cluster en ajoute quand les files s'allongent et en retire quand la charge baisse.
Mais d'abord, des warehouses séparés par charge, pour que chargements, transformations et tableaux de bord ne se concurrencent pas du tout.

<!-- example -->

```sql
ALTER WAREHOUSE wh_bi SET
  WAREHOUSE_SIZE = 'SMALL'
  MIN_CLUSTER_COUNT = 1
  MAX_CLUSTER_COUNT = 4
  SCALING_POLICY = 'STANDARD';   -- start clusters quickly to avoid queuing
```

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

<!-- challenge -->

Un warehouse BI montre de longues files d'attente aux heures de pointe, et quelqu'un propose de passer de Small à X-Large. Est-ce la meilleure solution ?

<!-- solution -->

Probablement pas : l'attente vient de la concurrence, il faut donc multiplier avec un warehouse multi-cluster (politique Standard) à taille égale. N'agrandir que si les requêtes individuelles sont lentes ou débordent.

<!-- takeaways -->

- Agrandir pour les requêtes lourdes ; multiplier pour la concurrence.
- Les warehouses multi-cluster ajoutent des clusters selon la charge.
- Séparez les warehouses par charge.

<!-- unit: Calcul spécialisé -->

<!-- goals -->

- Connaître les warehouses Snowpark-optimized et Gen2.
- Utiliser le Query Acceleration Service pour des gros parcours ponctuels.

<!-- concept -->

Les warehouses standard conviennent à la plupart du SQL, mais certaines charges exigent un autre matériel. Les warehouses Snowpark-optimized offrent beaucoup plus de mémoire par nœud pour Python et le ML. Les nouvelles générations apportent un matériel plus rapide et des améliorations du moteur, surtout pour les pipelines riches en DML.
Le Query Acceleration Service adopte une autre approche : au lieu d'un plus gros warehouse pour des parcours énormes occasionnels, il prête du calcul serverless aux parties des requêtes éligibles qui en ont besoin.

<!-- example -->

```sql
CREATE WAREHOUSE wh_ml WAREHOUSE_SIZE = 'MEDIUM' WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED';
ALTER WAREHOUSE wh_adhoc SET ENABLE_QUERY_ACCELERATION = TRUE
                            QUERY_ACCELERATION_MAX_SCALE_FACTOR = 8;
```

#### Comment choisir la taille initiale d'un warehouse ?

Commencer petit (X-Small ou Small) pour le développement et les chargements simples, tester des requêtes représentatives, et n'augmenter la taille que si les requêtes déversent, durent trop ou ne tiennent pas l'objectif. Mesurer le coût par exécution, pas seulement la durée.

#### Quels caches Snowflake possède-t-il ?

Le cache de résultats (dans la couche services : résultats réutilisés pendant 24 heures si la requête et les données n'ont pas changé), le cache du warehouse (données de micro-partitions sur le SSD local du warehouse tant qu'il tourne) et le cache de métadonnées (statistiques qui répondent à certaines requêtes comme `COUNT(*)` ou `MIN` sans warehouse).

#### Quand le cache de résultats est-il utilisé ?

Quand le même texte de requête est relancé, que les données n'ont pas changé, que l'utilisateur a les droits nécessaires et que la requête n'utilise pas de fonctions non déterministes comme `CURRENT_TIMESTAMP()`. Chaque réutilisation prolonge la rétention, jusqu'à 31 jours. Il ne coûte aucun calcul.

<!-- challenge -->

Un warehouse ad hoc est en Small, mais quelques requêtes d'analystes parcourent des milliards de lignes et durent une heure. Agrandir pour tout le monde gaspille des crédits. Qu'est-ce qui peut aider ?

<!-- solution -->

Activer le Query Acceleration Service sur ce warehouse : les gros parcours éligibles reçoivent du calcul serverless supplémentaire pour leurs parties lourdes, tandis que les requêtes normales tournent comme d'habitude.

<!-- takeaways -->

- Les warehouses Snowpark-optimized ajoutent de la mémoire.
- Les warehouses Gen2 accélèrent de nombreux pipelines.
- L'accélération aide les gros parcours ponctuels.

### Caches

<!-- unit: Les caches de Snowflake -->

<!-- goals -->

- Décrire les caches de résultats, de warehouse et de métadonnées.
- Arbitrer entre cache du warehouse et auto-suspend.

<!-- concept -->

Trois caches rendent le travail répété bon marché. Le cache de résultats renvoie pendant un jour le résultat de requêtes identiques sans utiliser de warehouse. Chaque warehouse garde sur disque local les données lues récemment, pour que les parcours répétés évitent le stockage distant. Le cache de métadonnées répond instantanément à des questions comme le nombre de lignes.
Le cache du warehouse ne vit que tant que le warehouse tourne : le moment de suspension arbitre entre coût et données chaudes pour les tableaux de bord.

<!-- example -->

| Cache | Où | Durée de vie | Warehouse requis ? |
|---|---|---|---|
| Résultats | Services cloud | 24 h (renouvelé à la réutilisation, max 31 jours) | Non |
| Warehouse (disque local) | Nœuds de calcul | Jusqu'à la suspension | Oui |
| Métadonnées | Services cloud | Toujours | Non (pour `COUNT(*)`, min/max) |

#### Quel lien entre le cache du warehouse et l'auto-suspend ?

La suspension vide le cache local : les requêtes suivantes lisent depuis le stockage distant et sont plus lentes. Pour des dashboards qui interrogent sans cesse les mêmes données, un auto-suspend plus long peut être plus rapide sans coûter beaucoup plus.

#### Comment désactiver le cache de résultats pour des tests ?

`ALTER SESSION SET USE_CACHED_RESULT = FALSE;` pour que les requêtes de benchmark s'exécutent vraiment.

<!-- challenge -->

Un warehouse BI avec un auto-suspend de 60 secondes rend lent le premier tableau de bord de chaque session. Qu'envisagez-vous ?

<!-- solution -->

Un auto-suspend plus long pendant les heures ouvrées (par exemple 5 à 10 minutes) garde le cache local chaud entre utilisateurs ; peser les crédits d'inactivité supplémentaires face à des tableaux de bord plus rapides.

<!-- takeaways -->

- Les caches de résultats, de warehouse et de métadonnées évitent le travail répété.
- Le cache du warehouse disparaît à la suspension.
- Réglez la suspension pour la BI qui dépend du cache.

<!-- unit: Le cache de résultats -->

<!-- goals -->

- Expliquer quand le cache de résultats sert, et entre quels utilisateurs.
- Le désactiver pour les benchmarks et diagnostiquer les échecs.

<!-- concept -->

Le cache de résultats est la requête la moins chère : zéro crédit. Il s'applique quand le même texte de requête est relancé, que les données n'ont pas changé et que le rôle peut les lire, même pour un autre utilisateur. De petites différences le cassent : données modifiées, texte différent, fonctions non déterministes ou certains réglages de session.
Les benchmarks doivent le désactiver, sinon ils mesurent le cache plutôt que la requête.

<!-- example -->

```sql
ALTER SESSION SET USE_CACHED_RESULT = FALSE;   -- benchmark the real query
SELECT region, SUM(amount) FROM sales.fct_orders WHERE order_date >= '2026-10-01' GROUP BY 1;
-- Query Profile shows "QUERY RESULT REUSE" when the cache was hit
```

#### Le cache de résultats fonctionne-t-il entre utilisateurs ?

Oui, si le rôle de l'autre utilisateur a les droits nécessaires sur les objets et que le texte de la requête est identique ; les résultats ne sont pas liés à l'utilisateur d'origine.

#### Pourquoi une requête répétée peut-elle ne pas utiliser le cache de résultats ?

Les données ont changé, le texte diffère (parfois même par les espaces ou la casse), elle utilise des fonctions non déterministes, des fonctions externes ou certaines fonctions de table, le résultat a dépassé sa rétention, ou le cache est désactivé dans la session.

#### Quelles sont les façons de charger des données dans Snowflake ?

Le chargement en masse avec `COPY INTO` depuis des stages, le chargement continu avec Snowpipe (fichiers) et Snowpipe Streaming (lignes), le connecteur Kafka, Openflow et les outils ETL/ELT partenaires, les instructions `INSERT`, les tables externes et Iceberg pour interroger sur place, et le partage de données pour les données d'autres comptes.

#### Qu'est-ce qu'un stage ?

Un emplacement pour les fichiers à charger ou décharger. Les stages internes sont dans Snowflake : stage utilisateur (`@~`), stage de table (`@%table`) et stages nommés. Les stages externes pointent vers des conteneurs S3, GCS ou Azure, généralement via une storage integration.

<!-- challenge -->

Une requête de tableau de bord qui utilise `CURRENT_TIMESTAMP()` dans son filtre ne profite jamais du cache de résultats. Pourquoi, et comment corriger ?

<!-- solution -->

Les fonctions non déterministes rendent chaque exécution différente : les résultats ne peuvent pas être réutilisés. Les remplacer par un paramètre de date fixe fourni par l'outil BI (par exemple la date du rapport) pour que les exécutions identiques partagent les résultats.

<!-- takeaways -->

- Requête identique, données inchangées, rôle autorisé : cache utilisé.
- Les fonctions non déterministes empêchent la réutilisation.
- Désactivez le cache pour les benchmarks.

<!-- stage: Faire entrer les données -->

### Chargement des données

<!-- unit: Stages, intégrations et formats de fichiers -->

<!-- goals -->

- Mettre en place stages, storage integrations et file formats.
- Téléverser, inspecter et inférer le schéma des fichiers en stage.

<!-- concept -->

Le chargement commence par l'emplacement des fichiers. Un stage pointe vers des fichiers, dans Snowflake ou dans votre stockage cloud ; une storage integration permet à Snowflake d'accéder à ce stockage via un rôle cloud plutôt qu'avec des clés ; un file format indique comment analyser les fichiers.
Avant de charger, on peut interroger directement les fichiers en stage et inférer leur schéma, ce qui accélère l'examen des nouvelles sources.

<!-- example -->

```sql
CREATE STORAGE INTEGRATION s3_lake TYPE = EXTERNAL_STAGE STORAGE_PROVIDER = 'S3'
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/snowflake-lake' ENABLED = TRUE
  STORAGE_ALLOWED_LOCATIONS = ('s3://lake/landing/');
CREATE FILE FORMAT ff_csv TYPE = CSV FIELD_DELIMITER = ';' SKIP_HEADER = 1 NULL_IF = ('', 'NULL');
CREATE STAGE landing URL = 's3://lake/landing/' STORAGE_INTEGRATION = s3_lake FILE_FORMAT = ff_csv;
SELECT $1, $2, METADATA$FILENAME FROM @landing/orders/ LIMIT 10;
```

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

<!-- challenge -->

Un stage a été créé avec des clés d'accès AWS intégrées à sa définition. Par quoi le remplacez-vous ?

<!-- solution -->

Une storage integration qui utilise un rôle IAM de confiance pour Snowflake, limitée aux emplacements autorisés, puis recréer le stage dessus ; supprimer ensuite les clés.

<!-- takeaways -->

- Les stages pointent vers des fichiers ; les file formats les décrivent.
- Les storage integrations remplacent les clés intégrées.
- Interrogez et inférez les fichiers en stage avant de charger.

<!-- unit: Chargement en masse avec COPY -->

<!-- goals -->

- Charger des fichiers avec COPY INTO, gestion des erreurs et transformations.
- Dimensionner les fichiers, comprendre les métadonnées de chargement et exporter des données.

<!-- concept -->

`COPY INTO` charge en parallèle des fichiers en stage dans une table, un fichier par thread : la taille des fichiers fixe la vitesse. De nombreux minuscules fichiers gaspillent du surcoût, et un énorme fichier ne peut pas être découpé. Snowflake retient pendant 64 jours quels fichiers il a chargés, et les relances les ignorent sauf si on force.
Les erreurs exigent une politique : abandonner, ignorer des lignes ou ignorer des fichiers. Des transformations simples peuvent avoir lieu pendant le chargement, et la même commande, en sens inverse, exporte des résultats de requête vers des fichiers.

<!-- example -->

```sql
COPY INTO raw.orders (order_id, customer_id, amount, source_file)
FROM (SELECT $1::NUMBER, $2::NUMBER, $3::NUMBER(12,2), METADATA$FILENAME FROM @landing/orders/)
ON_ERROR = 'CONTINUE';
SELECT * FROM TABLE(VALIDATE(raw.orders, JOB_ID => '_last'));   -- rejected rows
COPY INTO @exports/orders/ FROM (SELECT * FROM marts.fct_orders) FILE_FORMAT = (TYPE = PARQUET);
```

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

<!-- challenge -->

Un `COPY` quotidien d'un unique fichier gzip de 40 Go prend une heure, même sur un warehouse Large. Que changez-vous ?

<!-- solution -->

Découper l'entrée en fichiers d'environ 100–250 Mo compressés (chez le producteur ou par une étape de prétraitement), pour que `COPY` charge de nombreux fichiers en parallèle sur les threads du warehouse.

<!-- takeaways -->

- `COPY` parallélise par fichier ; visez ~100–250 Mo.
- Les métadonnées ignorent pendant 64 jours les fichiers déjà chargés.
- Choisissez délibérément une politique `ON_ERROR`.

<!-- unit: Chargement continu -->

<!-- goals -->

- Charger des fichiers en continu avec Snowpipe et des lignes avec Snowpipe Streaming.
- Ingérer des données CDC et éviter les chargements en double.

<!-- concept -->

Quand les données arrivent toute la journée, attendre un `COPY` nocturne ajoute de la latence. Snowpipe exécute le même `COPY` en serverless à l'arrivée de chaque fichier, prévenu par des événements cloud ; les petits fichiers augmentent son surcoût par fichier. Snowpipe Streaming se passe de fichiers et écrit des lignes depuis Kafka ou des SDK avec quelques secondes de latence.
Les changements de bases arrivent généralement via des outils CDC dans des tables brutes, puis sont appliqués avec `MERGE`. Les doublons viennent des producteurs qui renvoient des données, pas de Snowpipe : les pipelines dédupliquent en aval.

<!-- example -->

```sql
CREATE PIPE raw.orders_pipe AUTO_INGEST = TRUE AS
COPY INTO raw.orders FROM @landing/orders/ FILE_FORMAT = ff_csv;
SHOW PIPES;                                      -- notification_channel → configure S3 events to SQS
SELECT SYSTEM$PIPE_STATUS('raw.orders_pipe');
```

#### Comment interroger des fichiers en stage sans les charger ?

`SELECT $1, $2, METADATA$FILENAME FROM @stage/chemin (FILE_FORMAT => 'my_csv')`, pratique pour inspecter les fichiers avant de les charger.

#### Qu'est-ce qu'Openflow ?

Le service d'intégration de données géré de Snowflake, fondé sur Apache NiFi, avec des connecteurs pour les bases de données, applications SaaS et flux, déployé dans Snowflake ou dans votre propre cloud (bring your own cloud), pour ingérer des données structurées et non structurées.

#### Comment charger une base relationnelle en CDC dans Snowflake ?

Avec un outil de CDC (connecteurs Openflow, Debezium avec Kafka et le connecteur Kafka de Snowflake, Fivetran, AWS DMS écrivant dans S3 plus Snowpipe) qui dépose les événements de changement dans des tables raw, puis un `MERGE` depuis un stream ou une dynamic table pour les appliquer à la table d'état courant.

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

<!-- challenge -->

Un producteur écrit un minuscule fichier par événement, et les coûts de Snowpipe croissent plus vite que le volume de données. Que changez-vous ?

<!-- solution -->

Regrouper les fichiers chez le producteur (par exemple le buffering de Firehose à ~100 Mo ou quelques minutes), ou passer à Snowpipe Streaming pour une ingestion par lignes, sans surcoût par fichier.

<!-- takeaways -->

- Snowpipe charge les fichiers à leur arrivée.
- Snowpipe Streaming écrit des lignes à faible latence.
- Dédupliquez en aval ; les producteurs renvoient des données.

### Données semi-structurées

<!-- unit: VARIANT et requêtes par chemin -->

<!-- goals -->

- Stocker du JSON en VARIANT et l'interroger par chemins et conversions.
- Gérer les types mixtes et la différence entre clé absente et null JSON.

<!-- concept -->

Les données semi-structurées arrivent telles quelles dans des colonnes `VARIANT`, que Snowflake stocke en interne sous forme colonnaire : les requêtes sur les chemins courants restent rapides. On navigue avec une notation de chemin et on convertit en types SQL à la lecture.
Deux subtilités comptent pour la justesse : un champ qui arrive tantôt comme nombre, tantôt comme chaîne exige des conversions défensives, et une clé absente est un `NULL` SQL alors qu'un `null` JSON est un null `VARIANT`, qui se comporte différemment dans les comparaisons.

<!-- example -->

```sql
SELECT payload:order_id::NUMBER                 AS order_id,
       payload:customer.city::STRING            AS city,
       TRY_TO_NUMBER(payload:amount::STRING)    AS amount,     -- tolerate "12.50" or 12.5
       IS_NULL_VALUE(payload:coupon)            AS coupon_is_json_null
FROM raw.events_json;
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

<!-- challenge -->

`WHERE payload:discount IS NULL` rate les lignes où le JSON contient `"discount": null`. Pourquoi, et comment les inclure ?

<!-- solution -->

Un null JSON est un null `VARIANT`, pas un `NULL` SQL. Convertir d'abord (`payload:discount::NUMBER IS NULL`) ou tester les deux avec `IS_NULL_VALUE(payload:discount)`.

<!-- takeaways -->

- `VARIANT` stocke le JSON efficacement.
- Naviguez par chemins ; convertissez à la lecture.
- Clé absente ≠ null JSON.

<!-- unit: Aplatir et modéliser le JSON -->

<!-- goals -->

- Développer des tableaux avec FLATTEN et construire du JSON à partir de lignes.
- Décider quoi garder en VARIANT et quoi extraire, et charger du Parquet par nom de colonne.

<!-- concept -->

Les tableaux contenus dans du JSON deviennent des lignes avec `FLATTEN`, une par élément, rattachées à leur parent par une jointure latérale. Dans l'autre sens, construire du JSON à partir de lignes sert aux API et aux exports.
Le choix de modélisation se fait par couches : garder le JSON brut en `VARIANT` pour la souplesse et l'audit, et extraire les champs stables et très utilisés en colonnes typées dans des tables préparées, où types, contraintes et élagage fonctionnent le mieux. Des fichiers colonnaires peuvent se charger directement dans les colonnes correspondantes.

<!-- example -->

```sql
SELECT o.payload:order_id::NUMBER AS order_id,
       i.value:sku::STRING        AS sku,
       i.value:qty::NUMBER        AS qty
FROM raw.orders_json o,
     LATERAL FLATTEN(input => o.payload:items) i;

COPY INTO raw.orders FROM @landing/orders_parquet/
FILE_FORMAT = (TYPE = PARQUET) MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
```

#### Comment charger des colonnes Parquet directement dans des colonnes de table ?

Avec `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE` dans `COPY`, qui associe les colonnes du fichier à celles de la table par nom, ou en sélectionnant explicitement `$1:nom_colonne::type`.

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

<!-- challenge -->

Chaque requête de tableau de bord extrait les mêmes dix champs d'une énorme colonne `VARIANT`. Que changez-vous ?

<!-- solution -->

Extraire ces champs en colonnes typées dans une table préparée (ou une dynamic table) rafraîchie depuis le brut, pour que les requêtes lisent des colonnes étroites et typées avec un meilleur élagage ; garder le `VARIANT` brut pour l'audit et les nouveaux champs.

<!-- takeaways -->

- `FLATTEN` transforme les tableaux en lignes.
- Gardez le JSON brut ; extrayez les champs stables en colonnes.
- `MATCH_BY_COLUMN_NAME` charge les fichiers colonnaires par nom.

<!-- stage: Transformer les données -->

### Fonctions SQL

<!-- unit: Interroger et modifier les données -->

<!-- goals -->

- Utiliser QUALIFY, MERGE, PIVOT, SAMPLE et MATCH_RECOGNIZE.
- Écrire déduplications et upserts de façon idiomatique.

<!-- concept -->

Le SQL de Snowflake offre des raccourcis pour des motifs que les analystes écrivent chaque jour. `QUALIFY` filtre sur des résultats de fenêtre sans sous-requête, la façon la plus nette de garder la dernière ligne par clé. `MERGE` applique insertions, mises à jour et suppressions depuis une source en une instruction. Les pivots font pivoter les données pour les rapports, l'échantillonnage lit une fraction pour explorer, et le pattern matching trouve des séquences d'événements.

<!-- example -->

```sql
MERGE INTO silver.customers t
USING (
  SELECT * FROM raw.customer_changes
  QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1
) s
ON t.customer_id = s.customer_id
WHEN MATCHED AND s.op = 'D' THEN DELETE
WHEN MATCHED THEN UPDATE SET email = s.email, segment = s.segment, updated_at = s.updated_at
WHEN NOT MATCHED AND s.op <> 'D' THEN INSERT (customer_id, email, segment, updated_at)
  VALUES (s.customer_id, s.email, s.segment, s.updated_at);
```

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

<!-- challenge -->

Un `MERGE` échoue avec « Duplicate row detected during DML action ». Qu'est-ce qui ne va pas dans la source, et comment corriger ?

<!-- solution -->

Plusieurs lignes source correspondent à la même ligne cible. Dédupliquer d'abord la source en gardant une ligne par clé (par exemple avec `QUALIFY ROW_NUMBER() ... = 1`).

<!-- takeaways -->

- `QUALIFY` filtre les résultats de fenêtre.
- `MERGE` fait upserts et suppressions en une instruction.
- Dédupliquez par clé les sources de MERGE.

<!-- unit: Clés, séquences et transactions -->

<!-- goals -->

- Comprendre quelles contraintes Snowflake applique.
- Utiliser correctement séquences, colonnes identity et transactions.

<!-- concept -->

Snowflake accepte les déclarations de clés primaires, uniques et étrangères, mais n'applique que `NOT NULL` sur les tables standard. Les autres documentent l'intention et aident les outils et l'optimiseur : l'unicité doit être garantie et testée par les pipelines.
Séquences et colonnes identity génèrent des nombres uniques, pas sans trous. Les instructions sont validées automatiquement sauf si elles sont enveloppées dans une transaction explicite, exécutée en isolation read committed.

<!-- example -->

```sql
CREATE TABLE dim_customer (
  customer_key NUMBER IDENTITY(1,1),
  customer_id NUMBER NOT NULL,          -- enforced
  email STRING,
  PRIMARY KEY (customer_key)            -- declared, not enforced
);
SELECT customer_id, COUNT(*) FROM dim_customer GROUP BY 1 HAVING COUNT(*) > 1;   -- test it yourself
```

#### Comment fonctionnent les transactions dans Snowflake ?

ACID, avec le niveau d'isolation read committed. Chaque instruction est validée automatiquement, sauf à l'intérieur d'un `BEGIN … COMMIT` explicite. Le DDL valide implicitement. Du DML concurrent sur la même table peut être bloqué par des verrous jusqu'à la fin de l'autre transaction.

#### Que fait `UNDROP` ?

Il restaure une table, un schéma ou une base supprimés récemment grâce au Time Travel, tant que l'on est dans la période de rétention.

#### Que fait `SWAP WITH` ?

`ALTER TABLE a SWAP WITH b` échange atomiquement les noms de deux tables, une façon courante de publier une table reconstruite sans interruption pour les lecteurs.

<!-- challenge -->

Une équipe compte sur une clé primaire déclarée pour empêcher les doublons, et des doublons apparaissent après une relance. Qu'est-ce qui n'allait pas, et qu'ajoutez-vous ?

<!-- solution -->

Les clés primaires ne sont pas appliquées sur les tables standard. Rendre les chargements idempotents (`MERGE` sur la clé ou delete-insert par lot) et ajouter un test d'unicité (test dbt ou data metric function).

<!-- takeaways -->

- Seul `NOT NULL` est appliqué sur les tables standard.
- Les séquences sont uniques, pas sans trous.
- Garantissez et testez l'unicité dans les pipelines.

<!-- unit: Code procédural -->

<!-- goals -->

- Écrire UDF, procédures stockées et Snowflake Scripting.
- Choisir langages et cas d'usage pour chacun.

<!-- concept -->

Quand le SQL seul ne suffit pas, Snowflake exécute du code à côté des données. Les UDF renvoient des valeurs ou des tables et s'appellent depuis les requêtes ; les procédures stockées enchaînent des instructions avec contrôle de flux, pour l'administration ou une logique en plusieurs étapes. Les deux s'écrivent en SQL, Python, Java, Scala ou JavaScript.
Snowflake Scripting apporte variables, boucles et gestion d'erreurs au SQL lui-même, souvent suffisant pour des procédures sans autre langage.

<!-- example -->

```sql
CREATE OR REPLACE PROCEDURE ops.drop_old_dev_schemas(days INT)
RETURNS STRING LANGUAGE SQL AS
$$
DECLARE c CURSOR FOR SELECT schema_name FROM dev.information_schema.schemata
                     WHERE created < DATEADD(day, -:days, CURRENT_TIMESTAMP());
        n INT DEFAULT 0;
BEGIN
  FOR r IN c DO
    EXECUTE IMMEDIATE 'DROP SCHEMA dev.' || r.schema_name; n := n + 1;
  END FOR;
  RETURN n || ' schemas dropped';
END;
$$;
```

#### Qu'est-ce que `CREATE OR ALTER` ?

Une instruction qui crée un objet s'il n'existe pas, ou le modifie pour qu'il corresponde à la définition s'il existe, en conservant données et droits, utile pour des déploiements déclaratifs de tables et d'autres objets.

#### À quoi servent `PIVOT` et `UNPIVOT` ?

À faire pivoter des lignes en colonnes (par exemple les mois en colonnes) et des colonnes en lignes. `PIVOT` accepte des listes de valeurs dynamiques avec `ANY` dans les versions récentes.

#### Que fait `MATCH_RECOGNIZE` ?

De la reconnaissance de motifs sur des lignes ordonnées (par exemple une séquence d'événements dans une session, comme vue → panier → achat), qui renvoie les correspondances avec des mesures, sans écrire d'auto-jointures complexes.

<!-- challenge -->

Une UDF Python est appelée sur 2 milliards de lignes pour appliquer une règle fiscale simple, et la requête est lente. Que suggérez-vous ?

<!-- solution -->

Exprimer la règle en SQL (`CASE` et arithmétique) pour qu'elle s'exécute nativement, ou utiliser une UDF Python vectorisée si Python est vraiment nécessaire. Le Python ligne par ligne ajoute un surcoût de sérialisation.

<!-- takeaways -->

- Les UDF renvoient des valeurs ; les procédures enchaînent des étapes.
- Plusieurs langages sont pris en charge.
- Préférez le SQL quand il peut exprimer la logique.

<!-- unit: Gérer les objets -->

<!-- goals -->

- Récupérer des objets supprimés avec UNDROP et publier de façon atomique avec SWAP.
- Garder des définitions déclaratives avec CREATE OR ALTER.

<!-- concept -->

Quelques commandes sécurisent la gestion des objets. `UNDROP` restaure depuis le Time Travel une table, un schéma ou une base récemment supprimés. `SWAP WITH` échange deux tables de façon atomique : une table reconstruite remplace l'ancienne sans que les consommateurs voient jamais un état à moitié chargé.
`CREATE OR ALTER` apporte des définitions déclaratives : décrire l'objet voulu, et Snowflake le crée ou l'ajuste sans supprimer de données.

<!-- example -->

```sql
CREATE OR REPLACE TABLE marts.fct_revenue_new AS SELECT ...;
-- validate fct_revenue_new ...
ALTER TABLE marts.fct_revenue SWAP WITH marts.fct_revenue_new;   -- atomic publish
DROP TABLE marts.fct_revenue_new;
UNDROP TABLE marts.fct_revenue_old;                              -- if needed
```

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

<!-- challenge -->

Un job nocturne reconstruit sur place un gros mart, et les tableaux de bord affichent des données vides ou partielles pendant 20 minutes. Comment corriger ?

<!-- solution -->

Construire la nouvelle version dans une table séparée, la valider, puis publier de façon atomique avec `ALTER TABLE ... SWAP WITH` ; les tableaux de bord voient soit l'ancienne table, soit la nouvelle complète.

<!-- takeaways -->

- `UNDROP` restaure les objets supprimés.
- `SWAP WITH` publie les tables reconstruites de façon atomique.
- `CREATE OR ALTER` garde des définitions déclaratives.

### Time Travel, Fail-safe et clonage

<!-- unit: Streams -->

<!-- goals -->

- Suivre les changements de tables avec des streams.
- Choisir les types de streams et éviter les streams périmés.

<!-- concept -->

Un stream est un signet sur l'historique des changements d'une table. L'interroger renvoie les lignes insérées, modifiées ou supprimées depuis sa dernière consommation, et le consommer dans une instruction DML fait avancer le signet. Toute table devient ainsi un flux de changements pour le traitement incrémental.
Les streams append-only coûtent moins quand seules les insertions comptent. Un stream non consommé au-delà de la rétention de la table devient stale et doit être recréé.

<!-- example -->

```sql
CREATE STREAM raw.orders_changes ON TABLE raw.orders;
INSERT INTO silver.orders_log
SELECT order_id, amount, METADATA$ACTION, METADATA$ISUPDATE, CURRENT_TIMESTAMP()
FROM raw.orders_changes;          -- consuming the stream advances its offset
```

#### Qu'est-ce que le clonage zero-copy ?

La création instantanée d'une copie d'une table, d'un schéma ou d'une base avec `CLONE`, sans copier de données : le clone partage les micro-partitions de l'original et seules les modifications ultérieures consomment du stockage. On l'utilise pour les environnements de dev et de test, les sauvegardes avant un changement risqué et les instantanés à une date donnée.

#### Qu'hérite un clone ?

Les données et la structure, et pour les bases et schémas, les objets enfants. Les droits sur l'objet source lui-même ne sont pas copiés sauf avec `COPY GRANTS` ; les droits sur les objets enfants sont clonés. Les pipes pointant vers des stages internes, et quelques autres objets, ne sont pas clonés.

#### Comment donner à un développeur une copie complète des données de production à moindre coût ?

En clonant la base de production dans une base de dev (instantanément, sans stockage supplémentaire tant qu'il n'y a pas de modifications), en appliquant des politiques de masquage ou une couche de vues sécurisées si les données sont sensibles, et en donnant au développeur un rôle sur le clone.

<!-- challenge -->

Un stream sur une table de staging n'a pas été consommé pendant deux semaines de vacances, et il est désormais signalé comme stale. Pourquoi, et comment l'éviter ?

<!-- solution -->

Son offset est sorti de la rétention des données de la table : les changements ne peuvent plus être reconstitués. Le recréer et recharger ; consommer régulièrement les streams (une task planifiée) ou allonger la rétention des tables dont ils dépendent.

<!-- takeaways -->

- Les streams renvoient les changements depuis la dernière consommation.
- Consommer en DML fait avancer l'offset.
- Un stream non consommé périme après la rétention.

<!-- unit: Tasks -->

<!-- goals -->

- Planifier du SQL avec des tasks, serverless tasks et triggered tasks.
- Construire et superviser des graphes de tasks avec finalizers.

<!-- concept -->

Les tasks exécutent du SQL ou des procédures selon un planning, après d'autres tasks, ou quand un stream a de nouvelles données. Chaînées en graphes, elles forment des pipelines dans Snowflake sans orchestrateur externe. Les serverless tasks laissent Snowflake dimensionner le calcul automatiquement.
Comme tout pipeline, les graphes de tasks exigent supervision et nettoyage : l'historique montre exécutions et échecs, et une finalizer task s'exécute à la fin quoi qu'il arrive, pour notifier ou nettoyer.

<!-- example -->

```sql
CREATE TASK silver.apply_orders
  WAREHOUSE = wh_transform
  WHEN SYSTEM$STREAM_HAS_DATA('raw.orders_changes')
AS
  MERGE INTO silver.orders t USING raw.orders_changes s ON t.order_id = s.order_id
  WHEN MATCHED THEN UPDATE SET amount = s.amount
  WHEN NOT MATCHED THEN INSERT (order_id, amount) VALUES (s.order_id, s.amount);
ALTER TASK silver.apply_orders RESUME;
```

#### Qu'advient-il du Time Travel si l'on supprime puis recrée une table du même nom ?

La nouvelle table est distincte ; la table supprimée reste dans le Time Travel et ne peut être restaurée avec `UNDROP` qu'après avoir renommé la nouvelle, car les noms doivent être uniques.

#### Peut-on cloner à partir d'un instant passé ?

Oui : `CREATE TABLE t_clone CLONE t AT (TIMESTAMP => ...)` ou `BEFORE (STATEMENT => ...)`, dans la limite de la période de rétention. C'est une façon courante de se remettre d'un mauvais changement tout en gardant la table courante pour comparer.

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

<!-- challenge -->

Une task planifiée chaque minute vérifie un stream et ne trouve presque jamais rien, pourtant le warehouse se suspend rarement. Que changez-vous ?

<!-- solution -->

En faire une triggered task (sans planning, exécutée seulement quand le stream a des données) ou garder la condition `WHEN SYSTEM$STREAM_HAS_DATA`, qui saute les exécutions sans relancer le warehouse ; envisager les serverless tasks.

<!-- takeaways -->

- Les tasks s'exécutent par planning, après d'autres, ou sur nouvelles données.
- Les serverless tasks dimensionnent seules le calcul.
- Surveillez l'historique ; les finalizers nettoient.

<!-- unit: Dynamic tables et vues matérialisées -->

<!-- goals -->

- Construire des pipelines déclaratifs avec des dynamic tables et un target lag.
- Choisir entre dynamic tables, vues matérialisées et streams avec tasks.

<!-- concept -->

Les dynamic tables font des pipelines des définitions : on écrit la requête et un objectif de fraîcheur, et Snowflake tient la table à jour, en incrémental quand c'est possible. Des dynamic tables chaînées forment un pipeline dont les étapes amont se rafraîchissent aussi souvent que l'aval l'exige.
Les vues matérialisées résolvent un problème plus étroit : accélérer de façon transparente les requêtes sur une seule table. Streams et tasks restent l'outil du contrôle total, comme une logique procédurale ou des effets de bord.

<!-- example -->

```sql
CREATE DYNAMIC TABLE marts.daily_revenue
  TARGET_LAG = '15 minutes'
  WAREHOUSE = wh_transform
  REFRESH_MODE = INCREMENTAL
AS
SELECT order_date, region, SUM(amount) AS revenue
FROM silver.orders
GROUP BY order_date, region;
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

<!-- challenge -->

Une dynamic table fait toujours des rafraîchissements complets et coûte cher. Que vérifiez-vous ?

<!-- solution -->

Si sa requête utilise des constructions qui empêchent le rafraîchissement incrémental (certaines fonctions non déterministes, jointures ou motifs de fenêtre) ; vérifier le refresh mode indiqué, simplifier la requête ou la découper en dynamic tables chaînées rafraîchissables en incrémental.

<!-- takeaways -->

- Dynamic table : une requête plus un target lag.
- Le rafraîchissement incrémental ne traite que les changements.
- Les vues matérialisées accélèrent les requêtes d'une table.

### Streams, tasks et dynamic tables

<!-- unit: Snowpark pour le code -->

<!-- goals -->

- Traiter les données dans Snowflake avec Snowpark et pandas on Snowflake.
- Gérer les paquets Python et utiliser les notebooks.

<!-- concept -->

Snowpark permet d'écrire du code DataFrame en Python, Java ou Scala qui se compile en SQL et s'exécute dans Snowflake : les données ne quittent jamais la plateforme. Pour une logique malcommode en SQL, comme des règles métier complexes ou du feature engineering, c'est souvent plus clair.
pandas on Snowflake exécute de la même façon, à l'échelle, du code pandas familier. Les paquets viennent d'un canal sélectionné ou de vos propres téléversements, et les notebooks mêlent SQL et Python sur les mêmes données.

<!-- example -->

```python
from snowflake.snowpark import Session, functions as F
session = Session.builder.configs(conn_params).create()
orders = session.table("silver.orders")
features = (orders.group_by("customer_id")
                  .agg(F.count("order_id").alias("orders"), F.sum("amount").alias("spend")))
features.write.mode("overwrite").save_as_table("ml.customer_features")
```

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

<!-- challenge -->

Un data scientist exporte 200 Go de Snowflake vers son portable pour calculer des features en pandas. Que suggérez-vous ?

<!-- solution -->

Exécuter la même logique dans Snowflake avec Snowpark (ou pandas on Snowflake), pour que le calcul se fasse à côté des données sur un warehouse, et réécrire les features dans une table.

<!-- takeaways -->

- Les DataFrames Snowpark s'exécutent dans Snowflake.
- pandas on Snowflake fait passer pandas à l'échelle.
- Les données n'ont pas à quitter la plateforme.

<!-- unit: Applications, conteneurs et IA -->

<!-- goals -->

- Décrire Snowpark Container Services, Streamlit in Snowflake et Snowflake ML.
- Utiliser les fonctions Cortex AI depuis SQL.

<!-- concept -->

Snowflake multiplie les façons d'exécuter des applications là où sont les données. Container Services héberge n'importe quel service ou modèle conteneurisé ; les applications Streamlit tournent dans le compte avec ses permissions ; Snowflake ML fournit features, registre et outils d'entraînement.
Cortex apporte les grands modèles de langage au SQL : classification, extraction, résumé et complétion sous forme de fonctions, gouvernées comme toute requête.

<!-- example -->

```sql
SELECT ticket_id,
       AI_CLASSIFY(body, ['billing', 'bug', 'feature request']):labels[0]::STRING AS category,
       AI_COMPLETE('claude-sonnet-4-5', 'Summarize in one sentence: ' || body)  AS summary
FROM support.tickets
WHERE created_at >= DATEADD(day, -1, CURRENT_TIMESTAMP());
```

#### Comment fonctionne le contrôle d'accès dans Snowflake ?

Par un contrôle d'accès basé sur les rôles (RBAC) combiné à un contrôle discrétionnaire : les privilèges sont accordés aux rôles, les rôles aux utilisateurs et à d'autres rôles, et chaque objet a un rôle propriétaire qui le contrôle.

#### Quels sont les rôles définis par le système ?

ORGADMIN (organisation), ACCOUNTADMIN (rôle le plus élevé du compte ; à utiliser avec parcimonie), SECURITYADMIN (gère les droits et peut gérer utilisateurs et rôles), USERADMIN (crée utilisateurs et rôles), SYSADMIN (crée warehouses et bases ; les rôles personnalisés devraient lui être rattachés) et PUBLIC (accordé à tous).

#### À quoi ressemble une bonne hiérarchie de rôles ?

Des rôles d'accès qui portent les privilèges sur les objets (par exemple `SALES_READ`, `SALES_WRITE`), des rôles fonctionnels représentant des métiers ou des équipes (`ANALYST`, `DATA_ENGINEER`) auxquels on accorde les rôles d'accès, et des rôles fonctionnels rattachés à SYSADMIN pour que les administrateurs puissent tout gérer. Les comptes de service ont leurs propres rôles fonctionnels.

#### Que sont les future grants ?

Des droits appliqués automatiquement aux objets créés plus tard dans un schéma ou une base : `GRANT SELECT ON FUTURE TABLES IN SCHEMA sales.marts TO ROLE sales_read;`. Ils évitent les droits manquants sur les nouvelles tables.

<!-- challenge -->

Le support veut que chaque nouveau ticket soit étiqueté par thème toutes les heures, et l'équipe prévoit un service de ML séparé. Quoi de plus simple ?

<!-- solution -->

Une task planifiée (ou une dynamic table) qui applique en SQL une fonction Cortex comme `AI_CLASSIFY` aux nouveaux tickets, gouvernée par les permissions Snowflake, sans service séparé à héberger.

<!-- takeaways -->

- Container Services héberge tout service dans Snowflake.
- Les applications Streamlit héritent de la gouvernance du compte.
- Cortex expose les LLM comme fonctions SQL.

### Sécurité et contrôle d'accès

<!-- unit: Modéliser dans Snowflake -->

<!-- goals -->

- Appliquer schémas en étoile, normalisation et tables larges dans Snowflake.
- Implémenter le SCD de type 2 et des données de référence conformes.

<!-- concept -->

La puissance de Snowflake ne rend pas la modélisation obsolète. Stockage colonnaire et jointures rapides font bien tourner les schémas en étoile et rendent peu coûteuses les colonnes inutilisées des tables larges, mais des modèles clairs gardent les données compréhensibles et cohérentes. Normaliser là où intégrité et réutilisation comptent, dénormaliser pour la consommation.
L'historique et les données de référence partagées exigent la même discipline qu'ailleurs : SCD de type 2 avec `MERGE`, et dimensions conformes portées par un seul modèle.

<!-- example -->

```sql
MERGE INTO dim_customer d
USING stg_customer s ON d.customer_id = s.customer_id AND d.is_current
WHEN MATCHED AND d.hash_diff <> s.hash_diff
  THEN UPDATE SET valid_to = s.loaded_at, is_current = FALSE;
INSERT INTO dim_customer (customer_id, segment, hash_diff, valid_from, valid_to, is_current)
SELECT s.customer_id, s.segment, s.hash_diff, s.loaded_at, '9999-12-31', TRUE
FROM stg_customer s
LEFT JOIN dim_customer d ON d.customer_id = s.customer_id AND d.is_current
WHERE d.customer_id IS NULL;
```

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

<!-- challenge -->

Chaque équipe de mart a construit sa propre table clients avec des règles de segment légèrement différentes. Comment consolider ?

<!-- solution -->

Créer une `dim_customer` conforme portée par un seul modèle (avec historique SCD si besoin et règles de segment convenues), faire référencer ses clés de substitution par tous les marts, et déprécier les copies locales.

<!-- takeaways -->

- Les schémas en étoile aident toujours compréhension et cohérence.
- Normalisez pour l'intégrité ; dénormalisez pour la consommation.
- SCD2 avec `MERGE` ; dimensions partagées conformes.

<!-- unit: Outils autour de Snowflake -->

<!-- goals -->

- Expliquer comment dbt fonctionne sur Snowflake.
- Intégrer Spark à Snowflake.

<!-- concept -->

La plupart des plateformes Snowflake l'associent à d'autres outils. dbt est la couche de transformation courante : les modèles se compilent en SQL exécuté sur un warehouse Snowflake, avec des configs propres à Snowflake pour le clustering, les tables transient et le warehouse par modèle.
Spark s'intègre via un connecteur qui lit et écrit les tables Snowflake en poussant filtres et requêtes vers Snowflake, ce qui convient aux équipes qui traitent une partie des données dans Spark et les servent depuis Snowflake.

<!-- example -->

```sql
-- dbt model config for Snowflake
{{ config(materialized='incremental', unique_key='order_id',
          cluster_by=['order_date'], transient=false, snowflake_warehouse='wh_transform_l') }}
select * from {{ ref('stg_orders') }}
{% if is_incremental() %} where order_date >= dateadd(day, -3, current_date) {% endif %}
```

#### Qu'est-ce que la classification des données ?

Une fonction qui analyse les colonnes pour détecter les données sensibles (e-mails, noms, numéros de téléphone, identifiants nationaux) et propose ou applique des tags système, qui peuvent ensuite piloter des politiques de masquage.

#### Comment les utilisateurs s'authentifient-ils dans Snowflake ?

Par mot de passe plus MFA (que Snowflake rend obligatoire pour les connexions par mot de passe), SSO via des fournisseurs d'identité SAML 2.0 (Okta, Entra ID), OAuth (Snowflake ou externe), authentification par paire de clés pour les services, fédération d'identité de charge de travail et jetons d'accès programmatique. Les utilisateurs de service devraient utiliser des paires de clés ou OAuth, pas des mots de passe.

<!-- challenge -->

Un modèle dbt lourd a besoin d'un warehouse Large, mais le reste tourne bien en Small. Comment éviter de tout exécuter en Large ?

<!-- solution -->

Définir `snowflake_warehouse` dans la config de ce modèle vers le warehouse Large et garder le défaut du projet en Small : seul le modèle lourd utilise le calcul plus gros.

<!-- takeaways -->

- dbt compile les modèles en SQL exécuté sur Snowflake.
- Des configs propres à Snowflake règlent chaque modèle.
- Le connecteur Spark lit et écrit avec pushdown.

<!-- stage: Protéger et partager les données -->

### Partage de données et collaboration

<!-- unit: Time Travel et Fail-safe -->

<!-- goals -->

- Interroger et restaurer des données passées avec Time Travel.
- Expliquer le Fail-safe et fixer les durées de rétention.

<!-- concept -->

Les micro-partitions étant immuables, Snowflake peut garder d'anciennes versions à faible coût. Le Time Travel permet d'interroger une table telle qu'elle était, de la restaurer ou de l'annuler-supprimer pendant une période de rétention que vous fixez. Ensuite, le Fail-safe garde les tables permanentes récupérables une semaine de plus, mais seul le support Snowflake peut l'utiliser, en cas de sinistre.
La rétention est un levier de coût : une longue rétention sur des tables qui changent sans cesse multiplie le stockage.

<!-- example -->

```sql
SELECT COUNT(*) FROM sales.orders AT (OFFSET => -3600);                  -- an hour ago
INSERT INTO sales.orders
SELECT * FROM sales.orders BEFORE (STATEMENT => '01b8a0e3-0002-...');      -- before the bad DELETE
ALTER TABLE sales.orders SET DATA_RETENTION_TIME_IN_DAYS = 14;
```

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

<!-- challenge -->

Une table a été supprimée puis recréée sous le même nom, et `UNDROP TABLE orders` échoue désormais. Pourquoi, et comment restaurer l'ancienne ?

<!-- solution -->

Un objet de ce nom existe, donc `UNDROP` ne peut pas restaurer par-dessus. Renommer d'abord la nouvelle table (`ALTER TABLE orders RENAME TO orders_new`), puis `UNDROP TABLE orders`.

<!-- takeaways -->

- Le Time Travel interroge et restaure le passé.
- Le Fail-safe est un filet de sinistre réservé au support.
- La rétention coûte du stockage sur les tables très changeantes.

<!-- unit: Clonage zero-copy -->

<!-- goals -->

- Cloner instantanément tables, schémas et bases.
- Comprendre ce dont héritent les clones et cloner à un instant donné.

<!-- concept -->

Le clonage crée une copie complète en pointant vers les mêmes micro-partitions au lieu de les copier. C'est instantané et ne coûte aucun stockage tant que la copie ou l'original ne changent pas. Des environnements de développement et de test en taille réelle deviennent ainsi rapides et bon marché.
Les clones héritent des données et de la structure, et au niveau base ou schéma de leurs objets enfants, mais pas de tous les privilèges ; combinés au Time Travel, ils peuvent capturer une table telle qu'elle était avant un problème.

<!-- example -->

```sql
CREATE DATABASE analytics_dev CLONE analytics;                                 -- instant
CREATE TABLE sales.orders_before_fix CLONE sales.orders AT (TIMESTAMP => '2026-10-17 08:00:00'::TIMESTAMP_TZ);
GRANT USAGE ON DATABASE analytics_dev TO ROLE developer;
```

#### Pourquoi ACCOUNTADMIN ne doit-il être le rôle par défaut de personne ?

Il a un pouvoir illimité : une erreur ou une session compromise est catastrophique. Accordez-le à quelques administrateurs avec MFA, ne l'utilisez jamais pour le travail quotidien ni pour des comptes de service, et créez les objets avec SYSADMIN ou des rôles personnalisés.

#### Que sont les rôles secondaires ?

`USE SECONDARY ROLES ALL` permet à une session d'utiliser pour ses requêtes les privilèges de tous les rôles accordés (le rôle principal reste propriétaire des objets créés), ce qui simplifie le travail des utilisateurs qui ont plusieurs rôles.

#### Que sont les external access integrations ?

Des objets qui autorisent les UDF et procédures à appeler des endpoints réseau externes, contrôlés par des network rules listant les hôtes autorisés et par des objets secret pour les identifiants.

#### Qu'est-ce que le Secure Data Sharing ?

Le partage de données vivantes en lecture seule d'un compte à un autre sans copie : le fournisseur crée un share contenant bases, schémas, tables et vues sécurisées, et le consommateur crée une base à partir de celui-ci. Le consommateur paie le calcul qu'il utilise ; le fournisseur paie le stockage.

<!-- challenge -->

Les développeurs reçoivent chaque semaine un clone de la production, mais il contient des e-mails clients qu'ils ne devraient pas voir. Qu'ajoutez-vous ?

<!-- solution -->

Des politiques de masquage (idéalement par tag) sur les colonnes PII, ne révélant les valeurs qu'aux rôles privilégiés ; les clones conservent les politiques, donc les développeurs voient des données masquées. Autre option : masquer dans une étape après le clonage.

<!-- takeaways -->

- Les clones partagent les micro-partitions : instantanés et bon marché.
- Ils ne divergent qu'à mesure que les données changent.
- Clonez à un horodatage pour capturer un état passé.

### Snowpark, Python et IA

<!-- unit: RBAC et conception des rôles -->

<!-- goals -->

- Expliquer le contrôle d'accès par rôles de Snowflake et les rôles système.
- Concevoir une hiérarchie de rôles et utiliser avec prudence ownership, ACCOUNTADMIN et rôles secondaires.

<!-- concept -->

Dans Snowflake, les privilèges vont aux rôles, les rôles aux utilisateurs, et les rôles peuvent contenir d'autres rôles. Chaque objet a un rôle propriétaire au contrôle total. Les rôles système répartissent l'administration : un pour la sécurité, un pour les utilisateurs, un pour tout. Utiliser chaque jour le rôle le plus élevé fait de chaque erreur un désastre potentiel.
Une conception propre sépare les rôles d'accès, qui portent les privilèges sur les objets, des rôles fonctionnels, qui représentent des métiers et reçoivent les rôles d'accès. Les rôles secondaires permettent à une session d'utiliser tous ses rôles à la fois.

<!-- example -->

```sql
CREATE ROLE sales_read;   GRANT USAGE ON DATABASE sales TO ROLE sales_read;
GRANT USAGE ON SCHEMA sales.marts TO ROLE sales_read;
GRANT SELECT ON ALL TABLES IN SCHEMA sales.marts TO ROLE sales_read;
CREATE ROLE analyst_sales; GRANT ROLE sales_read TO ROLE analyst_sales;
GRANT ROLE analyst_sales TO ROLE sysadmin;     -- keep the hierarchy connected
GRANT ROLE analyst_sales TO USER ana;
```

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

<!-- challenge -->

Dix analystes ont ACCOUNTADMIN comme rôle par défaut « pour éviter les erreurs de permission ». Que changez-vous ?

<!-- solution -->

Créer des rôles fonctionnels dotés des seuls rôles d'accès nécessaires, en faire les rôles par défaut, réserver ACCOUNTADMIN à deux ou trois administrateurs avec MFA, et corriger les grants manquants plutôt que d'élever les privilèges.

<!-- takeaways -->

- Privilèges → rôles → utilisateurs ; les rôles s'imbriquent.
- Séparez rôles d'accès et rôles fonctionnels.
- Gardez ACCOUNTADMIN rare et protégé.

<!-- unit: Grants à l'échelle -->

<!-- goals -->

- Utiliser future grants et database roles.
- Centraliser le contrôle des grants avec des managed access schemas.

<!-- concept -->

Accorder objet par objet ne tient plus dès qu'apparaissent de nouvelles tables. Les future grants appliquent automatiquement des privilèges aux objets créés ensuite dans un schéma ou une base. Les database roles limitent l'accès au sein d'une base, et c'est aussi ainsi qu'un accès fin accompagne les shares.
Les managed access schemas centralisent le droit d'accorder : les propriétaires d'objets ne peuvent plus distribuer l'accès eux-mêmes, seul le propriétaire du schéma ou un rôle gérant les grants le peut.

<!-- example -->

```sql
GRANT SELECT ON FUTURE TABLES IN SCHEMA sales.marts TO ROLE sales_read;
CREATE DATABASE ROLE sales.reader;
GRANT SELECT ON ALL TABLES IN SCHEMA sales.marts TO DATABASE ROLE sales.reader;
CREATE SCHEMA sales.restricted WITH MANAGED ACCESS;
```

#### Qu'est-ce qu'un listing ?

Une offre packagée d'un share ou d'une Native App avec des métadonnées, des conditions et des statistiques d'usage, publiée de façon privée à des comptes choisis ou publiquement sur la Marketplace.

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

<!-- challenge -->

Chaque nouvelle table d'un schéma exige un ticket pour donner l'accès aux analystes. Que mettez-vous en place ?

<!-- solution -->

Des future grants sur le schéma (`GRANT SELECT ON FUTURE TABLES IN SCHEMA ... TO ROLE ...`), pour que les nouvelles tables soient lisibles automatiquement par le rôle d'accès, gérés en code.

<!-- takeaways -->

- Les future grants couvrent les objets créés ensuite.
- Les database roles limitent l'accès dans une base.
- Les managed access schemas centralisent l'octroi.

<!-- unit: Protection des colonnes et des lignes -->

<!-- goals -->

- Protéger les colonnes par des politiques de masquage, y compris par tags, et les lignes par des row access policies.
- Classifier les données sensibles et utiliser des secure views.

<!-- concept -->

Les grants au niveau table sont trop grossiers pour les données personnelles. Les politiques de masquage réécrivent les valeurs de colonne à la requête selon qui interroge ; les row access policies décident des lignes visibles par chaque rôle. Rattacher les politiques de masquage à des tags fait passer la protection à l'échelle : une colonne taguée PII est masquée partout.
La classification trouve automatiquement les colonnes sensibles, et les secure views et fonctions cachent leur définition aux consommateurs, ce qui compte pour le partage.

<!-- example -->

```sql
CREATE MASKING POLICY gov.mask_email AS (v STRING) RETURNS STRING ->
  CASE WHEN IS_ROLE_IN_SESSION('PII_READER') THEN v ELSE REGEXP_REPLACE(v, '.+@', '***@') END;
ALTER TAG gov.pii SET MASKING POLICY gov.mask_email;
CREATE ROW ACCESS POLICY gov.by_country AS (country STRING) RETURNS BOOLEAN ->
  EXISTS (SELECT 1 FROM gov.role_countries r
          WHERE r.country = country AND IS_ROLE_IN_SESSION(r.role_name));
ALTER TABLE sales.customers ADD ROW ACCESS POLICY gov.by_country ON (country);
```

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

<!-- challenge -->

De nouvelles tables avec des e-mails apparaissent sans cesse, et à chaque fois quelqu'un oublie d'ajouter une politique de masquage. Comment automatiser la protection ?

<!-- solution -->

Utiliser le masquage par tag : rattacher la politique à un tag `pii`, lancer la classification (ou taguer dans les modèles de tables) pour que les colonnes e-mail reçoivent le tag, et chaque colonne taguée est masquée sans travail table par table.

<!-- takeaways -->

- Les politiques de masquage protègent les colonnes à la requête.
- Les row access policies filtrent les lignes par rôle.
- Tags et classification font passer la protection à l'échelle.

<!-- unit: Authentification, réseau et audit -->

<!-- goals -->

- Sécuriser connexion, accès réseau et appels externes.
- Expliquer le chiffrement et auditer les accès avec l'access history.

<!-- concept -->

Autour des données, Snowflake contrôle qui entre et ce qui sort. Les utilisateurs se connectent avec MFA, SSO ou key pairs ; les network policies limitent la provenance des connexions ; les external access integrations contrôlent les points de terminaison externes que le code peut appeler.
Le chiffrement est toujours actif, au repos et en transit. L'access history enregistre les colonnes lues et écrites par chaque requête, ce qui répond précisément aux questions d'audit et de lignage.

<!-- example -->

```sql
CREATE NETWORK POLICY corp_only ALLOWED_IP_LIST = ('203.0.113.0/24');
ALTER USER etl_svc SET NETWORK_POLICY = corp_only;
SELECT query_start_time, user_name, direct_objects_accessed
FROM snowflake.account_usage.access_history
WHERE ARRAY_CONTAINS('SALES.PUBLIC.CUSTOMERS'::VARIANT,
      TRANSFORM(base_objects_accessed, o -> o:objectName))
ORDER BY query_start_time DESC LIMIT 20;
```

#### Comment les paquets Python arrivent-ils dans Snowflake ?

Depuis le canal Anaconda de Snowflake (listés dans `PACKAGES`), depuis des wheels ou zips téléversés dans un stage (`IMPORTS`), ou via des dépôts d'artefacts qui récupèrent des paquets de PyPI.

#### Comment savoir pourquoi une requête est lente ?

Ouvrez le Query Profile : regardez les opérateurs les plus coûteux, les partitions lues par rapport au total (pruning), les octets déversés (spill) en stockage local et distant, les jointures qui explosent (beaucoup plus de lignes en sortie qu'en entrée) et le temps d'attente. `GET_QUERY_OPERATOR_STATS` fournit les mêmes données en SQL.

#### Qu'est-ce que le spilling, et comment le corriger ?

Quand un warehouse manque de mémoire pour une opération, il déverse sur le disque local puis sur le stockage distant, bien plus lent. On le corrige avec un warehouse plus gros, en traitant moins de données (meilleurs filtres, pré-agrégation) ou en découpant la requête.

#### Qu'est-ce qui provoque une « jointure qui explose » ?

Une jointure sur une clé non unique, ou des conditions de jointure manquantes, de sorte que chaque ligne correspond à de nombreuses autres et que la sortie se multiplie. Vérifiez l'unicité des clés et que chaque jointure a sa condition complète.

#### Comment améliorer le pruning ?

En filtrant sur des colonnes corrélées à l'ordre de chargement (les dates), en ajoutant une clé de clustering sur les grandes tables filtrées par d'autres colonnes, en évitant d'envelopper les colonnes de filtre dans des fonctions qui empêchent le pruning, et en filtrant le plus tôt possible.

<!-- challenge -->

Les auditeurs demandent qui a lu la colonne `customers.national_id` le trimestre dernier. Où cherchez-vous ?

<!-- solution -->

Dans `ACCOUNT_USAGE.ACCESS_HISTORY`, qui liste les colonnes accédées par chaque requête (objets de base et directs), filtrée sur cette colonne et cette période, jointe à l'historique des requêtes pour le détail.

<!-- takeaways -->

- MFA, SSO et key pairs pour l'authentification.
- Network policies et intégrations contrôlent le trafic.
- L'access history enregistre les accès par colonne.

### Performances

<!-- unit: Secure Data Sharing -->

<!-- goals -->

- Partager des données en direct avec d'autres comptes et des utilisateurs sans Snowflake.
- Partager entre régions et comprendre les limites des consommateurs.

<!-- concept -->

Partager dans Snowflake signifie accorder un accès, pas envoyer des fichiers. Le fournisseur ajoute des objets à un share ; le consommateur le monte comme base en lecture seule et interroge les données en direct avec son propre calcul. Ni copies, ni exports, ni versions périmées.
Les partenaires sans Snowflake peuvent utiliser des reader accounts payés par le fournisseur. Les consommateurs d'autres régions ont besoin de réplication ou de listings qui s'en chargent. Les consommateurs peuvent interroger mais pas modifier les données partagées.

<!-- example -->

```sql
CREATE SECURE VIEW share_db.partner.v_sales AS
  SELECT order_date, region, product, revenue FROM marts.fct_sales WHERE partner_id = 42;
CREATE SHARE partner_42;
GRANT USAGE ON DATABASE share_db TO SHARE partner_42;
GRANT USAGE ON SCHEMA share_db.partner TO SHARE partner_42;
GRANT SELECT ON VIEW share_db.partner.v_sales TO SHARE partner_42;
ALTER SHARE partner_42 ADD ACCOUNTS = partnerorg.partner_account;
```

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

<!-- challenge -->

Un partenaire dans une autre région cloud a besoin de vos ventes quotidiennes. Un share direct échoue. Que faites-vous ?

<!-- solution -->

Répliquer la base vers un compte dans la région du partenaire et partager depuis celui-ci, ou publier un listing privé avec cross-cloud auto-fulfillment, qui gère la réplication.

<!-- takeaways -->

- Les shares donnent un accès en direct, en lecture seule, sans copie.
- Les reader accounts servent les partenaires sans Snowflake.
- Le partage entre régions exige réplication ou listings.

<!-- unit: Marketplace, clean rooms et applications -->

<!-- goals -->

- Décrire les listings et le Snowflake Marketplace.
- Expliquer les data clean rooms et les Native Apps.

<!-- concept -->

Le partage passe à l'échelle du produit. Les listings emballent des shares avec descriptions, conditions et statistiques d'usage, publiés en privé ou sur le Marketplace. Les clean rooms permettent à plusieurs parties d'analyser des données combinées tout en contrôlant ce qui peut être révélé, comme le recouvrement d'audiences sans exposer les listes de clients.
Les Native Apps vont le plus loin : elles distribuent ensemble code et données qui s'exécutent dans le compte du consommateur.

<!-- example -->

| Besoin | Mécanisme |
|---|---|
| Proposer des données météo à tout client | Listing sur le Marketplace |
| Partager un jeu de données avec un partenaire, sous conditions | Listing privé |
| Mesurer le recouvrement d'audience avec un annonceur | Data clean room |
| Livrer une application analytique qui tourne chez les clients | Native App |

#### Que montre `EXPLAIN` dans Snowflake ?

Le plan logique d'une requête sans l'exécuter : opérateurs, ordre des jointures et partitions à lire (d'après les métadonnées), utile pour vérifier le pruning avant de lancer une requête coûteuse.

#### Comment accélérer une requête `DISTINCT` sur d'énormes volumes ?

En vérifiant si la déduplication est vraiment nécessaire (souvent une jointure a multiplié les lignes), en dédupliquant plus tôt et sur moins de colonnes, en utilisant `APPROX_COUNT_DISTINCT` (HyperLogLog) quand une estimation suffit, et un warehouse plus gros s'il y a du spill.

#### À quoi servent les fonctions approximatives ?

`APPROX_COUNT_DISTINCT`, `APPROX_PERCENTILE` et `APPROX_TOP_K` donnent des estimations avec une faible erreur en utilisant bien moins de mémoire et de temps, ce qui convient aux dashboards et à l'exploration sur de très grosses tables.

#### Qu'est-ce qui fait les coûts de Snowflake ?

Le calcul des warehouses (de loin le poste principal pour la plupart des clients), les fonctions serverless (Snowpipe, clustering, vues matérialisées, search optimization, tasks, fonctions d'IA), le stockage (y compris Time Travel et Fail-safe), les services cloud au-delà de 10 % du calcul, et le transfert de données hors de la région.

<!-- challenge -->

Un distributeur et une marque veulent savoir combien de clients ils partagent, sans que l'un voie la liste de clients de l'autre. Qu'est-ce qui convient ?

<!-- solution -->

Une data clean room : chaque partie apporte des identifiants hachés, et seules des requêtes agrégées approuvées (comptes de recouvrement au-dessus d'un seuil) peuvent s'exécuter, sans révéler aucun enregistrement individuel.

<!-- takeaways -->

- Les listings font des shares des produits.
- Les clean rooms permettent l'analyse conjointe sous contrôle.
- Les Native Apps livrent code et données aux consommateurs.

<!-- stage: Exploiter Snowflake -->

### Maîtrise des coûts

<!-- unit: Lire le Query Profile -->

<!-- goals -->

- Diagnostiquer les requêtes lentes avec le Query Profile et EXPLAIN.
- Corriger débordements, jointures qui explosent et DISTINCT coûteux.

<!-- concept -->

Le Query Profile montre où une requête passe son temps et ses données : opérateurs les plus coûteux, partitions parcourues sur le total, octets débordés et lignes produites à chaque étape. La plupart des problèmes s'y voient d'un coup d'œil.
Trois motifs reviennent : le débordement quand la mémoire manque, l'explosion des jointures quand une clé n'est pas unique et que les lignes se multiplient, et un `DISTINCT` qui masque des doublons créés par une mauvaise jointure.

<!-- example -->

```text
Query Profile (most expensive nodes)
  Join [id = id]           48%   rows in: 2 M × 3 M   rows out: 1.8 B   ← exploding join
  TableScan ORDERS         31%   partitions 11,500 / 12,000             ← poor pruning
  Aggregate                12%   bytes spilled to local storage: 85 GB ← memory
```

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

<!-- challenge -->

La jointure d'une requête produit 600 fois plus de lignes que sa plus grosse entrée. Que vérifiez-vous, et comment corriger ?

<!-- solution -->

Les clés de jointure : un côté n'est pas unique sur la clé (ou une condition manque), et les lignes se multiplient. Corriger le grain de la jointure (dédupliquer ou agréger ce côté d'abord, ajouter la condition manquante) et retirer tout `DISTINCT` qui le masque.

<!-- takeaways -->

- Commencez par les nœuds les plus coûteux du Query Profile.
- Un débordement exige plus de mémoire ou moins de données.
- Les jointures qui explosent viennent de clés non uniques.

<!-- unit: Élagage et recherche -->

<!-- goals -->

- Améliorer l'élagage avec filtres, clustering et chargements triés.
- Utiliser le Search Optimization Service pour les recherches ponctuelles.

<!-- concept -->

L'essentiel de la performance de Snowflake vient de lire moins. Les filtres sur des colonnes qui suivent l'ordre de chargement, généralement des dates, élaguent bien ; les filtres enveloppés dans des fonctions ou sur des colonnes non regroupées, non. Clustering keys et chargement trié selon les principales colonnes de filtre améliorent l'élagage des grandes tables.
Pour chercher une aiguille dans une botte de foin par ID ou chaîne, search optimization construit un chemin d'accès qui trouve les rares micro-partitions concernées sans réorganiser la table.

<!-- example -->

```sql
-- prunes poorly: function on the filter column
SELECT * FROM events WHERE TO_DATE(event_ts) = '2026-10-17';
-- prunes well: range on the raw column
SELECT * FROM events WHERE event_ts >= '2026-10-17' AND event_ts < '2026-10-18';
ALTER TABLE events ADD SEARCH OPTIMIZATION ON EQUALITY(customer_id);
```

#### Comment réduire les coûts de stockage ?

Utiliser des tables transitoires pour le staging et les données reconstructibles, raccourcir le Time Travel des tables très modifiées, supprimer les tables inutilisées et les clones qui ont divergé, nettoyer les anciens fichiers des stages, et éviter de garder de multiples copies complètes au lieu de clones.

#### Un warehouse plus gros est-il toujours plus cher ?

Pas forcément. Si une requête se parallélise bien, doubler la taille divise la durée par deux pour un tarif doublé : le coût est similaire et le résultat arrive plus tôt. C'est plus cher quand les requêtes sont petites ou ne se parallélisent pas.

#### Pourquoi un warehouse qui exécute une requête d'une seconde chaque minute coûte-t-il cher ?

Chaque reprise facture au moins 60 secondes, et l'auto-suspend le garde allumé pendant le temps d'inactivité configuré après chaque requête. Une requête par minute peut le laisser allumé en permanence. Regroupez ces requêtes, utilisez des tasks serverless ou un seul petit warehouse partagé.

#### Comment fonctionne l'ajustement des services cloud ?

L'usage des services cloud est gratuit jusqu'à 10 % du calcul quotidien des warehouses ; seul l'excédent est facturé. Les opérations lourdes en métadonnées (beaucoup de requêtes minuscules, commandes `SHOW`, clones fréquents) peuvent le dépasser.

<!-- challenge -->

Le support recherche des clients individuels par `email` dans une table d'événements de 4 To, et chaque recherche en parcourt l'essentiel. Qu'ajoutez-vous ?

<!-- solution -->

Search optimization sur la colonne `email` (égalité), qui permet aux recherches ponctuelles d'ignorer presque toutes les micro-partitions ; regrouper par e-mail coûterait cher et aiderait peu les autres requêtes.

<!-- takeaways -->

- Filtrez les colonnes brutes, pas des fonctions de celles-ci.
- Regroupez ou triez les grandes tables par filtres principaux.
- Search optimization sert les recherches ponctuelles.

<!-- unit: Écrire des charges efficaces -->

<!-- goals -->

- Éviter les anti-patterns courants comme SELECT * et le DML ligne par ligne.
- Accélérer les gros MERGE et utiliser les fonctions approchées.

<!-- concept -->

Snowflake récompense le travail ensembliste et pénalise les habitudes des bases orientées lignes. Lire toutes les colonnes de tables larges gaspille la disposition colonnaire ; insérer les lignes une à une crée une multitude de minuscules micro-partitions ; joindre sur des types incompatibles empêche l'élagage.
Les gros merges demandent la même attention : borner la cible par des plages de dates ou de clés permet à Snowflake d'élaguer l'essentiel de la table. Les fonctions approchées échangent une erreur infime contre d'énormes économies sur comptages distincts et percentiles.

<!-- example -->

```sql
MERGE INTO sales.orders t
USING staging.orders_delta s
ON  t.order_id = s.order_id
AND t.order_date >= DATEADD(day, -7, CURRENT_DATE())     -- prune the 3 TB target
WHEN MATCHED THEN UPDATE SET amount = s.amount
WHEN NOT MATCHED THEN INSERT (order_id, order_date, amount) VALUES (s.order_id, s.order_date, s.amount);
SELECT APPROX_COUNT_DISTINCT(user_id) FROM events WHERE event_date >= '2026-10-01';
```

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

<!-- challenge -->

Une application insère 50 000 lignes par minute avec des `INSERT` ligne par ligne, et les requêtes sur la table ralentissent. Que changez-vous ?

<!-- solution -->

Regrouper les lignes : écrire des fichiers de micro-lots et charger avec `COPY`/Snowpipe, ou utiliser Snowpipe Streaming. Les insertions ligne par ligne créent de nombreuses minuscules micro-partitions et gaspillent du calcul par instruction.

<!-- takeaways -->

- Ne sélectionnez que les colonnes utiles.
- Regroupez les écritures ; évitez le DML ligne par ligne.
- Élaguez les cibles de MERGE par des conditions de plage.

### Exploitation et protection des données

<!-- unit: Ce qui fait le coût -->

<!-- goals -->

- Identifier les principaux leviers de coût de Snowflake.
- Raisonner sur taille des warehouses, minimums de reprise et facturation des cloud services.

<!-- concept -->

Pour la plupart des comptes, le calcul des warehouses fait la facture. Viennent ensuite les fonctions serverless, le stockage et le transfert de données. Le coût de calcul dépend moins de la taille que du temps de fonctionnement : un warehouse plus gros qui finit plus vite peut coûter autant, tandis qu'un petit maintenu éveillé par de fréquentes requêtes minuscules coûte bien plus que son travail.
Deux détails de facturation expliquent bien des surprises : chaque reprise facture au moins une minute, et les cloud services ne sont gratuits que jusqu'à une part du calcul quotidien.

<!-- example -->

```text
query: 1 s, every minute, X-Small, auto-suspend 600 s
→ warehouse never suspends: 24 h × 1 credit/h = 24 credits/day for ~24 min of actual work
fix: batch the checks, use a serverless task, or a shared warehouse already running
```

#### Comment alerter sur des problèmes de données dans Snowflake ?

Avec les alerts (conditions planifiées qui déclenchent une action comme l'envoi d'un e-mail ou d'une notification webhook), les data metric functions (supervision de la qualité des données Horizon : nulls, doublons, fraîcheur, métriques personnalisées) et les notifications d'échec des tasks.

#### Que sont les data metric functions ?

Des fonctions (système, comme `NULL_COUNT`, `DUPLICATE_COUNT`, `FRESHNESS`, ou personnalisées) attachées à des tables et exécutées selon un planning, dont les résultats sont conservés pour suivre la qualité des données dans le temps.

#### Qu'est-ce que l'event table ?

Une table spéciale qui collecte les journaux, traces et métriques émis par les UDF, procédures, Native Apps et Snowpark Container Services, pour superviser le code applicatif qui tourne dans Snowflake.

#### Comment sauvegarder les données Snowflake ?

Le Time Travel et le Fail-safe couvrent les erreurs récentes et les sinistres ; pour une protection plus longue, utilisez des clones zero-copy planifiés, des sauvegardes (ensembles de copies immuables à un instant donné, là où c'est disponible), la réplication vers une autre région, ou le déchargement vers un stockage cloud.

<!-- challenge -->

Un script de supervision lance une requête d'une seconde toutes les deux minutes sur son propre warehouse. Comment réduire son coût ?

<!-- solution -->

L'exécuter sur un warehouse déjà allumé, réduire sa fréquence, utiliser une serverless task ou une alerte, ou fixer un auto-suspend très court ; un warehouse dédié paie minimums et inactivité pour quelques secondes de travail.

<!-- takeaways -->

- Le temps de warehouse domine le coût.
- Plus gros et plus rapide peut coûter autant.
- Des requêtes minuscules fréquentes gardent les warehouses éveillés.

<!-- unit: Suivre et maîtriser les dépenses -->

<!-- goals -->

- Suivre la consommation de crédits par warehouse, requête et tag.
- Maîtriser les dépenses avec resource monitors et budgets.

<!-- concept -->

La maîtrise des coûts commence par l'attribution. Les vues account usage montrent les crédits par warehouse et par service serverless ; l'historique des requêtes, avec des query tags, relie les dépenses aux jobs, équipes et outils. Resource monitors et budgets ajoutent des limites : notifier, puis suspendre les warehouses quand les quotas sont atteints.
Quand les coûts bondissent, les mêmes données disent pourquoi : quel warehouse, quel service, quelles requêtes ont changé.

<!-- example -->

```sql
ALTER SESSION SET QUERY_TAG = 'dbt:marts_daily';
SELECT warehouse_name, SUM(credits_used) AS credits
FROM snowflake.account_usage.warehouse_metering_history
WHERE start_time >= DATEADD(month, -1, CURRENT_DATE())
GROUP BY 1 ORDER BY 2 DESC;
CREATE RESOURCE MONITOR rm_bi WITH CREDIT_QUOTA = 500
  TRIGGERS ON 80 PERCENT DO NOTIFY ON 100 PERCENT DO SUSPEND;
ALTER WAREHOUSE wh_bi SET RESOURCE_MONITOR = rm_bi;
```

#### Comment déployer du SQL en sécurité ?

Versionner le SQL dans Git, déployer depuis la CI avec un utilisateur de service (paire de clés ou OAuth), utiliser `CREATE OR ALTER` ou des outils de migration (schemachange, dbt, Terraform), tester d'abord sur une base clonée, et garder des scripts de retour arrière ou s'appuyer sur le Time Travel et les clones.

#### La modélisation en étoile est-elle toujours utile dans Snowflake ?

Oui. Snowflake gère bien les jointures et le stockage est bon marché, mais les schémas en étoile rendent toujours l'analytique plus simple, cohérente et rapide pour les outils de BI. Beaucoup d'équipes adoptent une approche en couches : raw, staging, intermédiaire et marts avec faits et dimensions, souvent construits avec dbt.

#### Faut-il normaliser ou dénormaliser dans Snowflake ?

Normaliser là où l'intégrité et la réutilisation comptent (entités centrales), dénormaliser pour la consommation (marts larges, une grande table pour des dashboards précis). Le stockage en colonnes rend les tables larges peu coûteuses à interroger quand on ne lit que quelques colonnes.

#### Comment dbt fonctionne-t-il avec Snowflake ?

dbt compile les modèles en SQL et les exécute sur un warehouse Snowflake via l'adaptateur dbt-snowflake, qui prend en charge les tables, vues, modèles incrémentaux (`merge`, `delete+insert`, `append`, `microbatch`), dynamic tables, tables transitoires, query tags et réglages de clustering.

#### Comment Spark et Snowflake s'intègrent-ils ?

Via le connecteur Spark, qui lit et écrit les tables Snowflake avec poussée des requêtes (pushdown), ou en partageant des tables Iceberg via un catalogue pour que Spark et Snowflake travaillent sur les mêmes fichiers.

<!-- challenge -->

La finance veut le coût Snowflake mensuel par équipe, mais les équipes partagent des warehouses. Comment l'attribuer ?

<!-- solution -->

Définir des query tags par équipe ou outil (dbt, BI, notebooks), puis répartir les crédits des warehouses selon la part de temps d'exécution de chaque tag dans l'historique des requêtes (`QUERY_ATTRIBUTION_HISTORY` si disponible), avec des warehouses séparés pour les plus grosses équipes.

<!-- takeaways -->

- Attribuez les crédits par warehouse, requête et tag.
- Resource monitors et budgets imposent des limites.
- Les vues d'usage expliquent les hausses de coût.

<!-- unit: Réduire les coûts -->

<!-- goals -->

- Réduire le coût des warehouses par dimensionnement, suspension et conception des charges.
- Réduire le coût du stockage par types de tables et rétention.

<!-- concept -->

Les économies de calcul consistent à ne pas payer l'inactivité ni le gaspillage : dimensionner par charge, suspendre vite, regrouper les petites charges, traiter en incrémental au lieu de reconstruire, et laisser jouer le cache.
Les économies de stockage portent plus sur l'historique que sur les données : tables transient pour les données reconstructibles, Time Travel plus court sur les tables très changeantes, et suppression des tables inutilisées et des vieux clones qui ont divergé.

<!-- example -->

| Levier | Économie typique |
|---|---|
| Auto-suspend de 60 s sur les warehouses ETL | Heures d'inactivité supprimées |
| Modèles incrémentaux au lieu de reconstructions complètes | L'essentiel du calcul de transformation |
| Tables de staging transient | Stockage Fail-safe |
| Rétention d'1 jour sur les tables très changeantes | Stockage Time Travel |

#### Comment implémenter une SCD de type 2 dans Snowflake ?

Avec un `MERGE` qui clôt les lignes courantes modifiées et insère les nouvelles versions (souvent deux instructions ou l'astuce de l'union), avec des streams et des tasks pour le traitement incrémental, ou avec les snapshots dbt, qui le gèrent automatiquement.

#### Qu'est-ce que l'approche « one big table », et quand convient-elle ?

Une table large et dénormalisée contenant tout ce dont un cas d'usage a besoin, rapide à interroger dans un moteur en colonnes et simple pour la BI. Elle convient à des cas d'usage stables et précis ; pour l'analytique générale, les schémas en étoile restent plus souples et cohérents.

<!-- challenge -->

Les coûts de stockage ont doublé alors que les données actives n'ont augmenté que de 10 %. Que vérifiez-vous ?

<!-- solution -->

Les octets Time Travel et Fail-safe par table (`TABLE_STORAGE_METRICS`) : tables très changeantes à longue rétention, tables de staging permanentes, et clones dont les données ont divergé. Réduire la rétention et passer en transient les tables reconstructibles.

<!-- takeaways -->

- Payez le travail, pas l'inactivité : dimensionnez, suspendez, regroupez.
- Traitez en incrémental.
- L'historique domine souvent le coût du stockage.

### Modélisation et intégration

<!-- unit: Supervision et qualité des données -->

<!-- goals -->

- Choisir entre ACCOUNT_USAGE et INFORMATION_SCHEMA.
- Surveiller la qualité des données avec alertes, data metric functions et event table.

<!-- concept -->

Deux familles de vues décrivent un compte : `INFORMATION_SCHEMA`, par base, en temps réel mais avec peu d'historique ; `ACCOUNT_USAGE`, pour tout le compte, un an d'historique avec un certain délai. Les requêtes de supervision choisissent selon la fraîcheur et la portée.
La qualité des données se pilote aussi dans Snowflake : les data metric functions mesurent fraîcheur, nulls ou doublons selon un planning, les alertes évaluent des conditions et notifient, et l'event table collecte les journaux du code exécuté dans le compte.

<!-- example -->

```sql
ALTER TABLE sales.orders SET DATA_METRIC_SCHEDULE = '60 MINUTE';
ALTER TABLE sales.orders ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.DUPLICATE_COUNT ON (order_id);
CREATE ALERT ops.orders_stale
  WAREHOUSE = wh_ops SCHEDULE = '30 MINUTE'
  IF (EXISTS (SELECT 1 FROM sales.orders HAVING MAX(loaded_at) < DATEADD(hour, -2, CURRENT_TIMESTAMP())))
  THEN CALL SYSTEM$SEND_EMAIL('ops_email', 'data@example.com', 'orders stale', 'No load in 2 hours');
```

#### Comment modéliser des données de référence à évolution lente partagées par de nombreux marts ?

Sous forme de dimensions conformes portées par un seul modèle, avec clés de substitution et historique SCD si besoin, référencées par tous les marts pour que tous les rapports utilisent les mêmes définitions.

#### Concevez un pipeline d'ingestion d'événements S3 vers des tables de reporting Snowflake.

Une storage integration et un stage externe sur le préfixe S3, un Snowpipe en auto-ingest à partir des notifications d'événements S3 vers une table raw typée ou en `VARIANT`, un stream sur la table raw, et des dynamic tables (ou des tasks avec `MERGE`) qui construisent les tables nettoyées et agrégées à la fraîcheur requise. J'ajoute des data metric functions, des alertes et des resource monitors, et je gère le tout sous forme de code.

#### Un warehouse de dashboards sature chaque lundi à 9 h. Que faites-vous ?

J'en fais un warehouse multi-cluster avec assez de clusters maximum (politique Standard pour les utilisateurs interactifs), je regarde si les requêtes lentes peuvent être optimisées ou servies par des agrégats, et je sépare les autres charges qui utilisent le même warehouse à ce moment-là.

#### Une requête lit 98 % des partitions d'une table de 5 To alors qu'elle filtre sur `customer_id`. Comment corriger ?

La table n'est pas regroupée par `customer_id`. Pour des recherches ponctuelles, j'active la search optimization sur cette colonne ; pour des filtres par plage fréquents, j'ajoute une clé de clustering (éventuellement combinée à la date) ; sinon je revois la requête ou je crée une table pré-agrégée.

<!-- challenge -->

Un tableau de bord des coûts construit sur `ACCOUNT_USAGE` n'affiche pas les requêtes de la dernière heure. Est-il cassé ?

<!-- solution -->

Non : les vues `ACCOUNT_USAGE` ont une latence (souvent jusqu'à quelques heures). Pour des contrôles quasi temps réel, utiliser les fonctions de table d'`INFORMATION_SCHEMA`, en acceptant leur historique plus court et leur portée par base.

<!-- takeaways -->

- `ACCOUNT_USAGE` : tout le compte, long historique, en différé.
- `INFORMATION_SCHEMA` : par base, en temps réel.
- DMF et alertes surveillent la qualité dans Snowflake.

<!-- unit: Réplication et sauvegardes -->

<!-- goals -->

- Répliquer des bases et basculer entre comptes.
- Prévoir des sauvegardes au-delà du Time Travel et du Fail-safe.

<!-- concept -->

Snowflake protège déjà contre les pannes matérielles et de zone, et le Time Travel couvre les erreurs récentes. Les pannes régionales et la protection à long terme exigent davantage. La réplication copie des bases, et avec les replication groups aussi utilisateurs, rôles et warehouses, vers des comptes d'autres régions ou clouds ; failover groups et client redirect permettent aux applications de passer sur le secondaire.
Pour les sauvegardes, clones, copies répliquées et exports vers votre propre stockage couvrent ce que les rétentions ne couvrent pas.

<!-- example -->

```sql
CREATE FAILOVER GROUP fg_prod
  OBJECT_TYPES = DATABASES, ROLES, USERS, WAREHOUSES
  ALLOWED_DATABASES = analytics, sales
  ALLOWED_ACCOUNTS = myorg.prod_dr
  REPLICATION_SCHEDULE = '10 MINUTE';
-- in the DR account, during a disaster:
ALTER FAILOVER GROUP fg_prod PRIMARY;
```

#### Quelqu'un a lancé `DELETE FROM orders` sans `WHERE` il y a une heure. Comment récupérer ?

Avec le Time Travel : je réinsère les lignes depuis `orders AT (OFFSET => -3600)` ou `BEFORE (STATEMENT => '<query id>')`, ou je clone la table à cet instant et je l'échange avec `ALTER TABLE … SWAP WITH`. Ensuite je restreins les droits de suppression sur les tables de production.

#### Les coûts ont augmenté de 40 % ce mois-ci. Comment enquêtez-vous ?

Je compare `WAREHOUSE_METERING_HISTORY` et la consommation serverless par service et par warehouse, je repère les warehouses et query tags en hausse, j'examine `QUERY_ATTRIBUTION_HISTORY` pour les requêtes les plus coûteuses, et je cherche des warehouses qui ne se suspendent plus, de nouvelles dynamic tables au lag très court, du reclustering sur des tables très modifiées ou des rafraîchissements complets.

#### Les analystes de chaque pays ne doivent voir que leurs lignes et pas les e-mails. Comment ?

Une row access policy sur les tables avec une table de correspondance entre rôles et pays, et une politique de masquage (ou un masquage par tags) sur les colonnes e-mail qui ne révèle les valeurs qu'à un rôle privilégié. Les analystes reçoivent des rôles fonctionnels associés à leur pays.

<!-- challenge -->

La conformité exige une copie mensuelle des tables financières conservée 7 ans. Le Time Travel plafonne à 90 jours. Que faites-vous ?

<!-- solution -->

Garder des clones zero-copy mensuels (nommés par mois) du schéma finance, ou exporter des snapshots mensuels en Parquet vers votre propre stockage avec object lock ; gérer la rétention en code.

<!-- takeaways -->

- La réplication copie bases et objets de compte.
- Failover groups et client redirect permettent la reprise.
- Les sauvegardes long terme exigent clones ou exports.

<!-- unit: Les objets en code -->

<!-- goals -->

- Gérer les objets Snowflake avec Terraform, l'intégration Git et du SQL déclaratif.
- Déployer des changements SQL en sécurité via la CI.

<!-- concept -->

Créer des objets à coups de clics ne passe pas à l'échelle et s'audite mal. Les objets de niveau compte comme warehouses, rôles et grants conviennent à Terraform ; les objets de base, à dbt, aux outils de migration ou à des scripts `CREATE OR ALTER` déclaratifs. Un objet Git repository permet à Snowflake de lire le code directement depuis votre dépôt.
Les déploiements suivent alors la pratique logicielle : changements relus dans Git, appliqués par la CI avec un utilisateur de service, testés sur un environnement cloné avant la production.

<!-- example -->

```hcl
resource "snowflake_warehouse" "transform" {
  name           = "WH_TRANSFORM"
  warehouse_size = "SMALL"
  auto_suspend   = 60
  auto_resume    = true
}
resource "snowflake_grant_account_role" "analyst_to_sysadmin" {
  role_name        = "ANALYST_SALES"
  parent_role_name = "SYSADMIN"
}
```

#### Comment migrer un entrepôt de données on-premise vers Snowflake ?

Inventorier les objets, les charges et les dépendances ; traduire le DDL et le SQL (SnowConvert aide) ; transférer l'historique via le stockage cloud et `COPY` ; mettre en place le chargement incrémental ; reconstruire les transformations (souvent en dbt) ; recréer la sécurité avec rôles et politiques ; valider par comptages de lignes, sommes de contrôle et comparaisons de rapports ; faire tourner les deux en parallèle avant la bascule ; puis optimiser warehouses et coûts.

#### Une équipe veut traiter 2 To de logs JSON par jour. Comment les charger et les modéliser ?

Déposer dans S3 des fichiers compressés d'environ 100 à 250 Mo, les charger avec Snowpipe ou un `COPY` planifié dans une colonne `VARIANT` d'une table raw transitoire, extraire les champs courants en colonnes typées dans une table nettoyée regroupée par date d'événement, et agréger dans des marts. Garder les données raw peu de temps si elles peuvent être rechargées depuis S3.

#### Comment expliquer la valeur de Snowflake à un interlocuteur métier ?

Un seul endroit gouverné pour les données de l'entreprise, qui passe instantanément à l'échelle pour n'importe quel nombre d'utilisateurs, ne coûte rien quand il ne sert pas, et permet aux équipes de partager et d'analyser les mêmes chiffres sans gérer de serveurs.

<!-- challenge -->

Warehouses et grants diffèrent entre dev et prod parce que des personnes les ont modifiés à la main. Comment les reprendre en main ?

<!-- solution -->

Importer les objets existants dans le state Terraform, les définir en code avec des variables par environnement, relire le plan et n'appliquer que via la CI ; retirer les droits de modification manuelle aux administrateurs hors procédure d'urgence.

<!-- takeaways -->

- Terraform pour les objets de compte ; dbt ou migrations pour les objets de base.
- Déployez via la CI avec des utilisateurs de service.
- Testez d'abord les changements sur des clones.

<!-- stage: Tout assembler -->

### Mises en situation

<!-- unit: Concevoir des pipelines d'ingestion -->

<!-- goals -->

- Concevoir des pipelines du stockage cloud et des journaux jusqu'aux tables de reporting.
- Combiner chargement, semi-structuré, transformation et supervision.

<!-- concept -->

Les questions de conception d'ingestion relient les sections. Une bonne réponse suit les fichiers : comment Snowflake y accède, comment et à quelle fréquence ils sont chargés, où atterrissent les données brutes, comment elles sont dédupliquées, typées et modélisées, comment les transformations restent incrémentales et ce qui est surveillé. Citer les choix de coût, taille des fichiers, warehouse par charge, rafraîchissements incrémentaux, montre une expérience de production.

<!-- example -->

```text
S3 (Firehose, ~128 MB gz) ─► storage integration + stage ─► Snowpipe (auto-ingest)
  ─► raw.events (VARIANT + metadata) ─► dynamic table silver.events (typed, deduped, lag 15 min)
  ─► gold marts (dbt or dynamic tables) ─► BI warehouse (multi-cluster)
  monitoring: pipe status, DMFs freshness/duplicates, alerts, resource monitor
```

#### Un `MERGE` nocturne sur une table de 3 To prend des heures. Que vérifiez-vous ?

Si la cible est élaguée (ajouter un filtre de date ou de plage de clés dans la clause `ON`, regrouper par la clé de merge), si la source contient des doublons ou est bien plus grosse que les changements, la taille du warehouse et le spill, et si une approche incrémentale (streams, `delete+insert` sur les partitions récentes) convient mieux.

#### Un Snowpipe charge parfois des lignes en double. Pourquoi, et que faites-vous ?

Les mêmes données sont arrivées dans des fichiers différents (relances du producteur, fichiers renommés), ou des fichiers ont été rechargés avec `FORCE`. Je fais écrire aux producteurs des noms de fichiers déterministes, je déduplique en aval sur une clé métier avec `QUALIFY` et je garde la couche raw en ajout seul, avec les métadonnées de fichier pour la traçabilité.

<!-- challenge -->

L'équipe source prévient que des fichiers peuvent être renvoyés après des échecs. Où votre conception gère-t-elle les doublons ?

<!-- solution -->

Garder le brut tel que chargé (avec nom de fichier et heure de chargement), puis dédupliquer en silver sur l'ID d'événement en gardant le plus récent par heure de chargement (`QUALIFY ROW_NUMBER() ... = 1`), pour que les fichiers renvoyés ne créent pas de lignes métier en double.

<!-- takeaways -->

- Suivez les fichiers du stockage aux rapports.
- Le brut garde tout ; le silver déduplique et type.
- Concevez pour les renvois, le coût et la supervision.

<!-- unit: Migrer vers Snowflake -->

<!-- goals -->

- Planifier la migration d'un entrepôt sur site.
- Ordonner traduction, déplacement des données, validation et bascule.

<!-- concept -->

Les migrations d'entrepôt échouent sur des surprises : dépendances oubliées, SQL traduit avec une autre sémantique, consommateurs que personne n'a listés. Un bon plan inventorie objets, jobs et utilisateurs, traduit DDL et SQL avec outils et relecture, déplace l'historique une fois puis les changements en incrémental, et fait tourner ancien et nouveau en parallèle en comparant les résultats avant de basculer les consommateurs. Repenser la conception, pas seulement la copier, apporte l'essentiel de la valeur.

<!-- example -->

| Phase | Activités |
|---|---|
| Évaluer | Inventaire des tables, jobs, rapports, utilisateurs ; statistiques d'usage |
| Traduire | DDL et SQL (SnowConvert), procédures, types de données |
| Déplacer | Chargement historique en masse via stages ; CDC pour les changements |
| Valider | Nombres de lignes, sommes de contrôle, comparaison des rapports |
| Basculer | Repointer BI et jobs ; retirer l'ancien système |

#### Comment donner à un partenaire l'accès à un jeu de données choisi sans le copier ?

Je crée des vues sécurisées sur les tables choisies, je les mets dans un share (ou un listing privé) et j'ajoute le compte du partenaire comme consommateur ; s'il n'a pas de compte Snowflake, je crée un reader account. J'utilise des row access policies ou des vues séparées pour limiter ce qu'il voit.

<!-- challenge -->

Après la migration, quelques rapports mensuels diffèrent de l'ancien système de petits montants. Quelles sont les causes probables ?

<!-- solution -->

Différences de types et d'arrondi (précision numérique, flottant contre décimal), gestion des fuseaux horaires des timestamps, sémantique de NULL dans jointures et agrégats, et fonctions SQL traduites avec un comportement différent. Comparer par jour et par clé pour localiser.

<!-- takeaways -->

- Inventoriez avant de déplacer quoi que ce soit.
- Traduisez et relisez la sémantique du SQL.
- Validez en parallèle avant la bascule.
