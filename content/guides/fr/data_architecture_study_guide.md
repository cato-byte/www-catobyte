## Fiche d'étude Architecture des données

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude architecture des données : environ 200 questions](../../images/data_architecture_study_guide_title_img.png)

Environ 200 questions d'entretien sur l'architecture des données : principes, choix de stockage et de bases de données, compromis des systèmes distribués, approches de modélisation (Inmon, Kimball, Data Vault), lakes, lakehouses et architecture médaillon, architectures batch et streaming (Lambda, Kappa), microservices et données événementielles, data mesh et data fabric, gouvernance, sécurité, fiabilité, coûts et architecture pour l'IA. Elle complète la fiche data warehousing, qui approfondit la modélisation dimensionnelle.

La fiche suit un parcours d'apprentissage en six étapes. Chaque section est découpée en unités courtes : objectifs d'apprentissage, explication du concept et exemple commenté, puis questions (d'abord de mémorisation, ensuite d'application), un exercice pratique et les points à retenir. Pour **apprendre**, lisez chaque unité du début à la fin. Pour **réviser**, passez en mode révision ou utilisez « Aller aux questions », marquez les réponses à revoir et essayez une révision mixte entre les sections.

<!-- QA -->
<!-- stage: Fondamentaux -->

### Principes

<!-- unit: Ce qu'est l'architecture de données -->

<!-- goals -->

- Expliquer ce que couvre l'architecture de données et ce que fait un architecte data.
- Nommer les couches d'une plateforme de données moderne.

<!-- concept -->

Toute entreprise a déjà une architecture de données, conçue ou non : les données viennent de quelque part, sont stockées quelque part, changent de forme et parviennent aux gens. L'architecture de données en est la version délibérée : un plan de structures, de standards et de choix technologiques qui permet à de nombreuses équipes de construire sans se contredire.
Les ingénieurs construisent des pipelines dans ce plan ; les architectes en décident la forme, en pesant exigences, coût et changement sur des années plutôt que des sprints.

<!-- example -->

```text
sources ─► ingestion (batch, CDC, streams) ─► storage (lake, warehouse)
        ─► processing (transform, model) ─► serving (BI, APIs, ML, reverse ETL)
        across all layers: governance, security, metadata, observability
```

#### Qu'est-ce que l'architecture des données ?

L'ensemble des décisions, modèles, politiques et standards qui définissent comment les données sont collectées, stockées, intégrées, traitées, gouvernées et consommées dans une organisation, ainsi que les systèmes qui les mettent en œuvre.

#### Que fait un architecte de données ?

Il traduit les besoins métier en structures et plateformes de données : il choisit technologies et modèles d'architecture, conçoit modèles et flux, définit les standards de qualité, de sécurité et de gouvernance, documente les décisions et guide les équipes pour que les systèmes s'emboîtent et évoluent sans être sans cesse refaits.

#### Quelles sont les principales couches d'une architecture de données moderne ?

Les sources, l'ingestion (batch, CDC, streaming), le stockage (lake, entrepôt, stockages opérationnels), le traitement et la transformation, la mise à disposition (BI, API, features de ML, reverse ETL), plus l'orchestration, la gouvernance, la sécurité, l'observabilité et les métadonnées de façon transversale.

#### Quels sont de bons principes d'architecture des données ?

Traiter les données comme des produits avec des responsables ; concevoir pour le changement (couplage faible, contrats) ; une source de vérité unique par entité ; conserver les données brutes de façon immuable et retraiter quand la logique change ; sécuriser et gouverner par défaut ; tout automatiser sous forme de code ; optimiser pour les questions réellement posées ; et préférer des composants simples et gérés quand ils répondent aux exigences.

#### Quelle différence entre modèles de données conceptuel, logique et physique ?

Les modèles conceptuels montrent les entités métier et leurs relations aux parties prenantes ; les modèles logiques ajoutent attributs, clés et normalisation sans détail technologique ; les modèles physiques les implémentent dans une base précise avec types, index, partitions et choix de stockage.

<!-- challenge -->

Un manager demande pourquoi l'entreprise a besoin d'un architecte data alors qu'elle a déjà cinq data engineers. Donnez deux réponses en termes métier.

<!-- solution -->

Sans plan commun, chaque ingénieur résout les problèmes à sa façon : coûts, données dupliquées et chiffres contradictoires augmentent. Un architecte fixe des standards et prend les décisions technologiques de long terme pour que la plateforme reste abordable et fiable en grandissant.

<!-- takeaways -->

- L'architecture de données est le plan ; l'ingénierie construit dedans.
- Couches : sources, ingestion, stockage, traitement, restitution.
- Gouvernance, sécurité et métadonnées traversent toutes les couches.

<!-- unit: Exigences et modèles -->

<!-- goals -->

- Recueillir les exigences fonctionnelles et non fonctionnelles.
- Utiliser modèles conceptuels, logiques et physiques, et consigner les décisions en ADR.

<!-- concept -->

Une bonne architecture part de questions, pas d'outils. Les exigences fonctionnelles disent quelles données et quelles sorties il faut ; les non fonctionnelles (fraîcheur, volume, disponibilité, coût, conformité) décident généralement la conception, car deux systèmes produisant le même rapport peuvent coûter cent fois plus l'un que l'autre.
Les modèles traduisent les exigences par niveaux, des entités métier pour les parties prenantes aux tables exactes pour les ingénieurs. Les registres de décisions conservent le raisonnement, pour que l'équipe suivante sache pourquoi, pas seulement quoi.

<!-- example -->

```markdown
# ADR-014: Use Iceberg for curated lake tables
Context: Athena, Spark and Snowflake must read the same tables.
Options: Delta, Iceberg, plain Parquet.
Decision: Iceberg (broadest multi-engine support, catalog integration).
Consequences: compaction jobs required; team training on Iceberg maintenance.
```

#### Que sont les exigences fonctionnelles et non fonctionnelles en architecture des données ?

Fonctionnelles : quelles données, transformations, indicateurs et sorties sont nécessaires. Non fonctionnelles : latence, fraîcheur, volume, scalabilité, disponibilité, durabilité, sécurité, conformité, coût et maintenabilité, qui déterminent souvent les choix technologiques.

#### Qu'est-ce qu'un architecture decision record (ADR) ?

Un court document qui consigne une décision importante : contexte, options étudiées, décision, conséquences et statut. Les ADR rendent le raisonnement visible et évitent de rouvrir sans cesse les débats ; ils sont stockés avec le code.

#### Qu'est-ce que la dette technique dans les plateformes de données ?

Des raccourcis qui rendent les évolutions coûteuses : pipelines non documentés, logique dupliquée, configuration codée en dur, tests absents, tables sans responsable, correctifs rapides en production. Elle s'accumule silencieusement et se manifeste par des incidents, des livraisons lentes et une défiance envers les chiffres.

<!-- challenge -->

Les parties prenantes demandent des « tableaux de bord des ventes en temps réel ». Quelles questions non fonctionnelles posez-vous avant de concevoir quoi que ce soit ?

<!-- solution -->

Quelle fraîcheur suffit (secondes, minutes, heure), combien d'utilisateurs, quelles décisions changent avec des données plus fraîches, quel coût est acceptable et quels besoins de disponibilité. Les réponses tranchent entre streaming et batch fréquent.

<!-- takeaways -->

- Les exigences non fonctionnelles pilotent conception et coût.
- Modèles conceptuels, logiques et physiques servent des lecteurs différents.
- Les ADR conservent le raisonnement des décisions.

<!-- unit: Principes de conception -->

<!-- goals -->

- Appliquer les principes clés : données comme produit, données brutes immuables, responsabilité unique.
- Concevoir pour le changement et gérer la dette technique.

<!-- concept -->

Quelques principes font durer les plateformes. Les jeux de données avec propriétaires et garanties inspirent confiance et sont réutilisés. Garder les données brutes inchangées permet de retraiter quand la logique change ou qu'un bug apparaît. Les pipelines à tâche unique sont plus faciles à tester et à remplacer.
Le fil conducteur, c'est le changement : exigences, sources et outils vont changer. Les architectures qui l'assument, avec couplage faible, contrats et vérifications automatiques, absorbent le changement ; les autres accumulent une dette qui ralentit chaque projet futur.

<!-- example -->

| Principe | Pratique |
|---|---|
| Données comme produit | Propriétaire, schéma, SLA, doc par jeu de données |
| Brut immuable | Zone d'atterrissage en ajout seul ; ne jamais modifier les fichiers source |
| Responsabilité unique | Un pipeline par source ; un modèle par concept |
| Évolutive | Contrats et tests comme fitness functions |

#### Que signifie « construire ou acheter » pour les plateformes de données ?

Choisir entre développer des composants maison (plus de contrôle, plus de maintenance) et utiliser des services gérés ou des éditeurs (plus rapide, moins de contrôle, coût récurrent, dépendance). La plupart des équipes achètent les capacités standard (stockage, entrepôt, connecteurs) et construisent ce qui les différencie.

#### Qu'est-ce que la dépendance envers un fournisseur (vendor lock-in), et comment la limiter ?

La dépendance aux formats ou API propriétaires d'un fournisseur, qui rend un changement coûteux. On la limite avec des formats ouverts (Parquet, Iceberg, Delta), du SQL standard, l'infrastructure as code, des abstractions là où elles sont peu coûteuses et des plans de sortie pour les composants critiques, en acceptant une certaine dépendance là où la valeur est forte.

#### Que sont les « données en tant que produit » ?

Gérer les jeux de données comme des produits : un responsable clair, un objectif et un schéma documentés, des garanties de qualité et des SLA, la découvrabilité, le versionnage et les retours des consommateurs. C'est une idée centrale du data mesh, utile dans toute architecture.

#### Quels sont les compromis entre centralisation et décentralisation ?

Les plateformes et équipes centrales apportent cohérence, économies d'échelle et gouvernance forte, mais deviennent des goulots d'étranglement. La responsabilité décentralisée par domaine accélère la livraison et rapproche l'expertise des données, au risque d'incohérences et d'efforts dupliqués ; une gouvernance fédérée équilibre les deux.

#### Quelle différence entre architecture des données et ingénierie des données ?

L'architecture des données définit le plan : structures, standards, choix technologiques et manière dont les composants s'assemblent. L'ingénierie des données construit et exploite les pipelines et plateformes qui le mettent en œuvre. En pratique les rôles se recouvrent, et les ingénieurs seniors prennent de nombreuses décisions d'architecture.

#### Comment évaluer une nouvelle technologie pour la plateforme ?

Partir des exigences, comparer quelques options selon des critères (adéquation, performances, coût, compétences, écosystème, support, sécurité, dépendance), faire une preuve de concept sur de vraies charges, considérer le coût total de possession et le coût de sortie, et consigner la décision dans un ADR.

<!-- challenge -->

Une équipe écrase les fichiers source bruts après nettoyage pour économiser du stockage. Six mois plus tard, on découvre un bug dans la logique de nettoyage. Quelle conséquence, et quelle correction ?

<!-- solution -->

L'historique ne peut plus être retraité, car les entrées d'origine ont disparu. Garder les données brutes immuables (peu coûteux avec les classes de stockage et règles de lifecycle) et écrire les données nettoyées dans une couche séparée.

<!-- takeaways -->

- Les jeux de données ont besoin de propriétaires et de garanties.
- Le brut immuable permet retraitement et audit.
- Concevez pour le changement ; suivez et remboursez la dette.

<!-- unit: Choisir une technologie -->

<!-- goals -->

- Arbitrer entre construire et acheter, et limiter la dépendance au fournisseur.
- Évaluer les technologies selon l'adéquation et le coût total de possession.

<!-- concept -->

Les choix technologiques sont des paris de long terme. Les services managés échangent du contrôle contre de la vitesse ; formats ouverts et interfaces standard gardent la possibilité de changer plus tard. Centraliser apporte la cohérence, décentraliser la vitesse, et la plupart des organisations ont besoin des deux.
Comparer les options au seul prix de licence est trompeur. Le coût total inclut les personnes pour l'exploiter, les migrations et le coût d'être coincé : les évaluations doivent tester de vraies charges selon des critères explicites.

<!-- example -->

| Critère | Option A (managée) | Option B (OSS auto-hébergé) |
|---|---|---|
| Délai avant première valeur | Semaines | Mois |
| Coût d'exploitation (personnes) | Faible | Élevé |
| Dépendance | Moyenne (les formats ouverts aident) | Faible |
| TCO sur 3 ans | ... | ... |

#### Qu'est-ce que le coût total de possession (TCO) ?

Le coût complet d'une solution dans la durée : licences ou consommation cloud, infrastructure, personnes pour la construire et l'exploiter, formation, migration, support et coût des interruptions, et pas seulement le prix par unité de calcul.

#### Qu'est-ce que l'« architecture évolutive » ?

Concevoir les systèmes pour qu'ils changent de façon incrémentale avec des garde-fous (fitness functions comme des tests sur la latence, le coût ou le couplage), en privilégiant les décisions réversibles et les petits pas plutôt que de grandes conceptions initiales.

#### Pourquoi les données brutes doivent-elles être immuables ?

Des données brutes immuables permettent de retraiter l'historique quand la logique change ou que des bugs sont corrigés, d'auditer ce que les sources ont envoyé et de reconstruire les couches aval ; les modifications ont lieu dans les couches suivantes, ce qui garde le système récupérable.

#### Qu'est-ce que le principe de « responsabilité unique » appliqué aux pipelines ?

Chaque pipeline ou modèle doit avoir un objectif clair (ingérer une source, harmoniser une entité, construire un indicateur), ce qui le rend plus facile à tester, à attribuer, à réutiliser et à modifier sans effet de bord.

#### Quels types de bases de données existent ?

Relationnelles (PostgreSQL, MySQL, Oracle), clé-valeur (DynamoDB, Redis), documentaires (MongoDB, Couchbase), orientées colonnes larges (Cassandra, HBase, Bigtable), orientées graphes (Neo4j, Neptune), séries temporelles (TimescaleDB, InfluxDB), moteurs de recherche (Elasticsearch, OpenSearch), vectorielles (pgvector, Pinecone, vecteurs OpenSearch) et stockages analytiques en colonnes (entrepôts, ClickHouse, Druid).

<!-- challenge -->

Une équipe veut auto-héberger une plateforme de streaming open source parce que « c'est gratuit ». Que lui demandez-vous d'inclure dans la comparaison ?

<!-- solution -->

Le coût humain de l'exploitation 24 h/24 (mises à jour, montée en charge, astreinte), l'infrastructure, la sécurité et le support, face au prix d'un service managé sur trois ans. Inclure le coût d'opportunité des ingénieurs qui ne construisent pas de produits de données.

<!-- takeaways -->

- Achetez pour la vitesse, construisez pour vous différencier.
- Formats ouverts et standards limitent la dépendance.
- Comparez le coût total de possession, pas les licences.

### Stockage et bases de données

<!-- unit: Choisir une base de données -->

<!-- goals -->

- Associer bases relationnelles, documentaires, clé-valeur, wide-column et graphes aux charges.
- Expliquer la persistance polyglotte et son coût.

<!-- concept -->

Les bases de données diffèrent par les questions auxquelles elles répondent à bas coût. Les relationnelles gèrent des requêtes flexibles sur des données liées, avec transactions. Les documentaires gardent ensemble des enregistrements imbriqués et autonomes. Les clé-valeur répondent à « donne-moi cette clé » à très grande échelle. Les wide-column absorbent des écritures massives par partition. Les graphes suivent des relations.
Choisir selon le motif d'accès plutôt que par habitude mène à plusieurs bases dans un même système, ce qui fonctionne si quelqu'un est responsable de l'intégration et de la cohérence entre elles.

<!-- example -->

| Motif d'accès | Base |
|---|---|
| Commandes avec jointures et transactions | PostgreSQL |
| Catalogue produits aux attributs imbriqués | Documents MongoDB / DynamoDB |
| Lecture de session par ID, des millions/s | Redis / DynamoDB |
| Écritures de capteurs par appareil et date | Cassandra |
| « Amis d'amis » ou réseaux de fraude | Neo4j / Neptune |

#### Quand choisir une base relationnelle ?

Quand les données sont structurées avec des relations, exigent des transactions ACID, des requêtes flexibles avec jointures et une cohérence forte : commandes, paiements, comptes, stocks. C'est le choix par défaut de la plupart des systèmes opérationnels.

#### Quand choisir une base documentaire ?

Quand les enregistrements sont autonomes, imbriqués et de schéma souple (catalogues produits, contenus, profils utilisateurs), accédés surtout par clé ou par des requêtes simples, et que les équipes veulent faire évoluer le schéma rapidement.

#### Quand choisir un stockage clé-valeur ?

Pour des accès très rapides par clé à grande échelle (sessions, caches, préférences utilisateur, paniers), avec des modes d'accès simples et une latence prévisible.

#### Quand choisir un stockage orienté colonnes larges ?

Pour des volumes d'écriture massifs et de gros jeux de données accédés par clé de partition selon des requêtes connues, comme les séries temporelles, l'IoT, la messagerie et les journaux d'événements (Cassandra, Bigtable, HBase).

#### Quand choisir une base orientée graphes ?

Quand les relations sont l'objet principal de l'analyse : réseaux de fraude, réseaux sociaux, recommandations, topologies réseau, graphes de connaissances, avec des requêtes qui parcourent de nombreux sauts.

#### Qu'est-ce que la persistance polyglotte ?

Utiliser différentes technologies de stockage selon les besoins au sein d'un même système (PostgreSQL pour les commandes, Redis pour les sessions, Elasticsearch pour la recherche, S3 pour les fichiers), en acceptant plus de complexité d'exploitation pour une meilleure adéquation à chaque usage.

#### Qu'est-ce que le stockage objet, et pourquoi est-il central dans les plateformes modernes ?

Le stockage d'objets immuables dans des buckets accessibles par clé via HTTP (S3, ADLS, GCS) : quasiment illimité, très durable, bon marché et découplé du calcul. Les data lakes et lakehouses reposent dessus, les formats de table y ajoutant des fonctions de base de données.

<!-- challenge -->

Une équipe stocke profils, commandes et paiements dans MongoDB et peine désormais avec les rapports qui les croisent et avec la cohérence. Que suggérez-vous ?

<!-- solution -->

Garder MongoDB là où les documents conviennent (profils), déplacer commandes et paiements, qui exigent jointures et transactions, vers une base relationnelle, et répliquer l'ensemble dans la plateforme analytique pour le reporting.

<!-- takeaways -->

- Choisissez la base selon le motif d'accès.
- Relationnel pour jointures et transactions ; les autres pour des formes précises.
- La persistance polyglotte exige une intégration avec un responsable.

<!-- unit: Bases spécialisées -->

<!-- goals -->

- Savoir quand conviennent séries temporelles et moteurs de recherche.
- Distinguer OLTP, OLAP et HTAP.

<!-- concept -->

Certaines charges sont si courantes qu'elles ont leurs propres moteurs. Les bases de séries temporelles gèrent des mesures horodatées à haute fréquence et des requêtes sur des plages de temps. Les moteurs de recherche classent le texte par pertinence et gèrent correspondance approximative et facettes.
La séparation la plus large oppose transactions et analyse : l'OLTP sert de nombreuses petites lectures et écritures, l'OLAP de grands parcours et agrégations. Les systèmes HTAP tentent les deux dans un moteur, ce qui aide l'analytique opérationnelle mais remplace rarement une plateforme analytique dédiée.

<!-- example -->

| Charge | Type de moteur |
|---|---|
| Métriques CPU toutes les 10 s de 5 000 hôtes | Séries temporelles |
| Recherche produit avec fautes de frappe et filtres | Moteur de recherche |
| Paiement et mises à jour de stock | OLTP |
| Chiffre d'affaires mensuel par région et canal | OLAP |

#### Quelles différences entre stockage bloc, fichier et objet ?

Le stockage bloc fournit des volumes bruts pour une machine (EBS), idéal pour les bases de données ; le stockage fichier des systèmes de fichiers hiérarchiques partagés (NFS, EFS) ; le stockage objet des objets plats accessibles en HTTP à très grande échelle (S3), idéal pour les data lakes.

#### Que sont les niveaux (tiers) de stockage ?

Des classes de stockage de coût et de rapidité d'accès différents (chaud, tiède, froid, archive ; S3 Standard, Infrequent Access, Glacier). Les politiques de cycle de vie déplacent les données vieillissantes vers les niveaux moins chers.

#### Que sont les formats de fichiers par lignes et en colonnes ?

Les formats par lignes (CSV, JSON, Avro) stockent les enregistrements ensemble, efficaces pour écrire et lire des enregistrements complets ; les formats en colonnes (Parquet, ORC) stockent les colonnes ensemble avec des statistiques, efficaces pour l'analytique qui lit peu de colonnes de nombreuses lignes.

<!-- challenge -->

Une équipe e-commerce implémente la recherche produit avec `LIKE '%term%'` sur PostgreSQL : c'est lent et les fautes de frappe échappent. Que proposez-vous ?

<!-- solution -->

Indexer les produits dans un moteur de recherche (OpenSearch ou Elasticsearch) alimenté depuis la base par CDC ou événements, et servir la recherche depuis celui-ci avec pertinence, correspondance approximative et facettes. PostgreSQL reste la source de vérité.

<!-- takeaways -->

- Les séries temporelles gèrent les mesures horodatées.
- Les moteurs de recherche classent et rapprochent le texte.
- OLTP et OLAP exigent des moteurs différents ; le HTAP les mêle.

<!-- unit: Couches de stockage et formats -->

<!-- goals -->

- Expliquer le stockage objet, ses classes et les formats de fichiers.
- Comparer les formats de table ouverts et le rôle du catalogue.

<!-- concept -->

Les plateformes modernes reposent sur le stockage objet : peu coûteux, durable, quasi illimité et lisible par n'importe quel moteur. Au-dessus, les formats de fichiers décident de l'efficacité de lecture ; les formats colonnaires permettent aux requêtes analytiques d'ignorer ce dont elles n'ont pas besoin.
Les formats de table ouverts ajoutent les fonctions de base de données manquantes, transactions, évolution de schéma et time travel, sous forme de métadonnées sur ces fichiers. Un catalogue indique ensuite aux moteurs quelles tables existent et qui peut les lire : c'est ce qui transforme des fichiers en plateforme partagée.

<!-- example -->

```text
catalog (Unity / Glue / Polaris)  ─ tables, schemas, permissions
table format (Iceberg / Delta)    ─ snapshots, transactions, schema
file format (Parquet)             ─ columnar, compressed, statistics
object storage (S3 / ADLS / GCS)  ─ cheap, durable, tiered
```

#### Que sont les formats de table ouverts ?

Des spécifications (Apache Iceberg, Delta Lake, Apache Hudi) qui ajoutent une couche de métadonnées transactionnelle au-dessus de fichiers Parquet en stockage objet, offrant écritures ACID, évolution du schéma, voyage dans le temps, évolution du partitionnement et mises à jour efficaces, lisibles par de nombreux moteurs.

#### Iceberg, Delta ou Hudi : comment choisir ?

Delta est natif dans Databricks et très utilisé avec Spark ; Iceberg a le support multi-moteurs le plus large (Snowflake, Athena, Trino, Spark, Flink) et un catalogue REST ouvert ; Hudi se concentre sur les upserts en streaming et le traitement incrémental. Choisissez selon vos moteurs, votre catalogue et votre gouvernance ; les fonctions d'interopérabilité (UniForm, XTable) réduisent les écarts.

#### Quel est le rôle d'un catalogue de données dans l'architecture de stockage ?

Il enregistre les tables existantes, l'emplacement de leurs fichiers, leurs schémas et leurs droits, pour que les moteurs trouvent et gouvernent les données : Hive Metastore, AWS Glue, Unity Catalog, Polaris et les catalogues REST Iceberg.

#### Quelle différence entre OLTP, OLAP et HTAP ?

L'OLTP traite les transactions, l'OLAP l'analytique, et les systèmes HTAP (traitement hybride transactionnel/analytique) (TiDB, SingleStore, AlloyDB, Unistore) tentent de servir les deux sur des données fraîches, utiles pour l'analytique opérationnelle à échelle limitée.

#### Comment choisir une stratégie de clés primaires à grande échelle ?

Considérer l'unicité entre systèmes, l'ordre pour la localité des index et l'exposition : les entiers auto-incrémentés sont compacts mais exigent une coordination centrale ; les UUIDv4 sont uniques mondialement mais aléatoires ; les UUIDv7 et ULID sont uniques et ordonnés dans le temps ; les clés naturelles restent des attributs.

#### Qu'est-ce qu'un index, et quels types comptent pour un architecte de données ?

Une structure qui accélère les recherches au prix des écritures et du stockage : B-tree (plages, égalité), hachage (égalité), GIN/inversés (texte intégral, tableaux, JSON), BRIN (tables énormes naturellement ordonnées), bitmap (faible cardinalité dans les entrepôts) et index vectoriels (HNSW, IVF) pour la recherche par similarité.

#### À quoi sert une base de séries temporelles ?

À des mesures horodatées à fort débit d'ingestion (métriques, IoT, supervision) avec des requêtes sur des plages de temps, du sous-échantillonnage et des politiques de rétention ; elles compressent efficacement les séries et offrent des fonctions spécialisées.

<!-- challenge -->

Trois moteurs (Spark, Trino et un entrepôt) doivent lire et écrire les mêmes tables. Quels choix de stockage le permettent ?

<!-- solution -->

Du stockage objet avec des fichiers Parquet, un format de table ouvert largement supporté par plusieurs moteurs (souvent Iceberg), et un catalogue partagé que les trois moteurs utilisent pour métadonnées et permissions.

<!-- takeaways -->

- Le stockage objet est le socle de la plateforme.
- Les formats colonnaires rendent l'analytique bon marché.
- Les formats de table ajoutent les transactions ; les catalogues partagent les tables.

<!-- unit: Clés et index -->

<!-- goals -->

- Choisir une stratégie de clé primaire pour l'échelle et l'intégration.
- Savoir quels types d'index comptent.

<!-- concept -->

Les clés survivent aux systèmes qui les créent. Une clé unique seulement dans une base entre en collision quand on fusionne des données de plusieurs ; une clé qui révèle un sens ou une séquence divulgue de l'information. À grande échelle, l'ordre compte aussi : les clés séquentielles gardent les index compacts, les aléatoires dispersent les écritures.
Les index sont l'autre moitié : chaque type convient à une forme de requête, et chaque index ralentit les écritures.

<!-- example -->

| Besoin | Choix |
|---|---|
| Unique entre services, générée n'importe où | UUIDv7 (ordonné dans le temps) |
| Compacte, une seule base | bigint identity |
| Requêtes par plage et égalité | Index B-tree |
| JSON ou tableau contient | Index GIN |
| Énormes tables en ajout seul, par date | BRIN / clustering |

#### Quand utiliser un moteur de recherche comme OpenSearch ?

Pour la recherche plein texte avec pertinence, correspondance approximative, facettes et analyse de journaux, généralement comme index secondaire alimenté depuis le système de référence et non comme base principale.

#### Qu'est-ce que le théorème CAP ?

Dans un système distribué subissant une partition réseau, il faut choisir entre cohérence (chaque lecture voit la dernière écriture) et disponibilité (chaque requête reçoit une réponse). Sans partition, les deux sont possibles ; CAP porte sur le comportement en cas de panne.

<!-- challenge -->

Après la fusion des tables clients de deux entreprises, les ID entrent en collision car les deux utilisaient des entiers auto-incrémentés. Comment l'éviter à l'avenir ?

<!-- solution -->

Introduire une clé globale (par exemple un UUIDv7 ou une clé de substitution préfixée par la source) dans le modèle intégré, garder les ID d'origine comme attributs de source et les relier par une table de correspondance de clés.

<!-- takeaways -->

- Les clés doivent être uniques entre systèmes appelés à fusionner.
- Les clés ordonnées gardent les index efficaces.
- Chaque type d'index sert une forme de requête et coûte en écriture.

### Fondamentaux des systèmes distribués

<!-- unit: Compromis face aux pannes -->

<!-- goals -->

- Expliquer CAP, PACELC, ACID et BASE.
- Comparer les modèles de cohérence, de forte à éventuelle.

<!-- concept -->

Dès que les données vivent sur plusieurs machines, les réseaux tombent et les machines divergent. CAP dit que pendant une partition, un système doit choisir entre répondre et répondre juste ; PACELC ajoute que même sans panne, il faut choisir entre vitesse et cohérence.
ACID et BASE décrivent deux attitudes face à ce choix : transactions strictes, ou disponibilité avec accord éventuel. Entre les deux existent des compromis utiles, comme garantir que l'utilisateur voie ses propres écritures, qui suffisent souvent au produit sans le coût d'une cohérence totale.

<!-- example -->

| Cas d'usage | Modèle acceptable |
|---|---|
| Virement bancaire | Cohérence forte (ACID) |
| Compteur de likes d'un post | Cohérence éventuelle |
| L'utilisateur modifie son profil et recharge | Read-your-writes |
| Fil de commentaires | Cohérence causale |

#### Qu'est-ce que PACELC ?

Une extension de CAP : en cas de Partition, choisir Disponibilité ou Cohérence ; sinon (Else, fonctionnement normal), choisir Latence ou Cohérence. Elle explique pourquoi de nombreux systèmes sacrifient la cohérence à la latence même sans panne.

#### Qu'est-ce qu'ACID ?

Atomicité (tout ou rien), Cohérence (les contraintes sont respectées), Isolation (les transactions concurrentes n'interfèrent pas) et Durabilité (les données validées survivent aux pannes) : les garanties des transactions relationnelles.

#### Qu'est-ce que BASE ?

Basically Available, Soft state, Eventual consistency : un modèle privilégié par certains systèmes NoSQL distribués qui favorisent la disponibilité et la tolérance aux partitions, les données convergeant vers la cohérence avec le temps.

#### Qu'est-ce que la cohérence à terme ?

Si aucune nouvelle mise à jour n'a lieu, toutes les répliques finissent par renvoyer la même valeur ; entre-temps, les lectures peuvent renvoyer des données périmées. Les applications doivent tolérer des écarts temporaires.

#### Quels modèles de cohérence existent en plus de la cohérence forte et à terme ?

Lire ses propres écritures (un client voit ce qu'il a écrit), lectures monotones (pas de retour en arrière), cohérence causale (les opérations causalement liées sont vues dans l'ordre), obsolescence bornée (lectures avec au plus X secondes de retard) et cohérence de session.

#### Qu'est-ce que le partitionnement (sharding) ?

Répartir les données entre nœuds selon une clé (hachage ou plage) pour faire monter stockage et charge en charge horizontalement. Une bonne clé répartit les données uniformément et garde ensemble les données liées ; une mauvaise crée des points chauds.

<!-- challenge -->

Un service de panier doit rester disponible pendant des problèmes réseau entre régions. Quel modèle de cohérence convient, et que doit gérer la conception ?

<!-- solution -->

La disponibilité avec cohérence éventuelle (souvent read-your-writes par utilisateur). La conception doit fusionner les mises à jour conflictuelles du panier, par exemple en gardant les ajouts sous forme d'ensemble et en résolvant les suppressions par horodatage ou version vectors.

<!-- takeaways -->

- Pendant une partition : disponibilité ou cohérence.
- PACELC ajoute le compromis de latence en fonctionnement normal.
- Les modèles intermédiaires couvrent souvent le besoin à moindre coût.

<!-- unit: Partitionnement et réplication -->

<!-- goals -->

- Expliquer partitionnement, réplication, consensus et quorums.
- Éviter points chauds et transactions distribuées.

<!-- concept -->

Les bases distribuées passent à l'échelle en répartissant les données entre nœuds (partitionnement) et survivent aux pannes en les copiant (réplication). Chacune apporte son problème. Partitionner sur une clé déséquilibrée envoie l'essentiel du trafic vers un nœud. Répliquer pose la question de la bonne copie, tranchée par des protocoles de consensus et des quorums.
Coordonner une transaction entre nombreux nœuds ou systèmes avec un two-phase commit est possible mais lent et fragile : les conceptions modernes préfèrent des transactions locales et une coordination asynchrone.

<!-- example -->

```text
N = 3 replicas, W = 2 write acks, R = 2 read acks
W + R > N  →  every read overlaps the latest write (strongly consistent reads)
hot key "celebrity_123" → add a suffix 0–9 and spread it over 10 partitions
```

#### Qu'est-ce que la réplication, et quels en sont les types ?

Conserver des copies des données sur plusieurs nœuds pour la disponibilité et la montée en charge en lecture. La réplication synchrone attend les répliques (cohérence plus forte, latence plus élevée) ; l'asynchrone répond avant leur confirmation (latence plus faible, perte possible lors d'un basculement). Les topologies incluent leader-suiveur, multi-leader et sans leader.

#### Qu'est-ce qu'un algorithme de consensus ?

Un protocole (Raft, Paxos, ZAB) qui permet à des nœuds distribués de s'accorder sur une valeur ou un leader malgré des pannes, utilisé pour les métadonnées, la coordination et les journaux répliqués dans des systèmes comme Kafka (KRaft), etcd et ZooKeeper.

#### Qu'est-ce que l'idempotence, et pourquoi est-elle vitale dans les systèmes de données ?

Une opération est idempotente si l'exécuter plusieurs fois a le même effet qu'une seule. Les relances sont inévitables dans les systèmes distribués : des écritures idempotentes (upserts, écrasement par partition, clés de déduplication) évitent doublons et corruption.

#### Que sont les sémantiques de livraison en messagerie ?

At-most-once (peut perdre des messages), at-least-once (peut en dupliquer) et exactly-once (l'effet de chaque message se produit une fois). L'exactly-once signifie généralement une livraison at-least-once plus un traitement idempotent ou transactionnel.

#### Qu'est-ce que la contre-pression (backpressure) ?

Un mécanisme par lequel un consommateur plus lent signale aux producteurs de ralentir (ou par lequel des tampons absorbent les pics), évitant la surcharge et l'épuisement mémoire dans les pipelines de streaming.

#### Quelle différence entre montée en charge horizontale et verticale ?

La montée en charge verticale ajoute des ressources à une machine (plus simple, limitée) ; l'horizontale ajoute des machines (quasi illimitée, exige partitionnement et coordination). Les plateformes de données reposent sur la montée en charge horizontale pour le stockage et le calcul.

<!-- challenge -->

Une table partitionnée par `country` a une partition qui porte 70 % de la charge. Que changez-vous ?

<!-- solution -->

Partitionner sur une clé de plus forte cardinalité (par exemple un hash de `customer_id`), ou des clés composites qui découpent davantage le grand pays, pour répartir la charge. Garder `country` comme filtre ou index secondaire.

<!-- takeaways -->

- Le partitionnement fait passer à l'échelle ; la réplication protège.
- Quorums et consensus décident quelle copie l'emporte.
- Évitez clés déséquilibrées et transactions distribuées.

<!-- unit: Déplacer les données de façon fiable -->

<!-- goals -->

- Sécuriser les mouvements de données avec idempotence et sémantiques de livraison.
- Gérer la backpressure et le décalage d'horloges.

<!-- concept -->

Déplacer des données entre systèmes implique des relances, et les relances impliquent des doublons. La plupart des messageries garantissent une livraison at-least-once : la justesse vient de consommateurs idempotents, qui produisent le même résultat quand un message arrive deux fois.
Deux réalités de plus façonnent la conception : les consommateurs peuvent être plus lents que les producteurs, d'où backpressure ou tampons, et les horloges de machines différentes divergent, donc ordonner par horodatage entre systèmes demande de la prudence.

<!-- example -->

```sql
-- idempotent sink: replaying an event changes nothing
MERGE INTO payments t
USING incoming s ON t.event_id = s.event_id
WHEN NOT MATCHED THEN INSERT *;
```

#### Qu'est-ce qu'un point chaud (hotspot), et comment l'éviter ?

Une partition ou un nœud qui reçoit une charge disproportionnée à cause d'une clé biaisée (un utilisateur très populaire, un horodatage croissant). On l'évite avec de meilleures clés, du salage, du hachage ou en découpant les clés chaudes.

#### Qu'est-ce que le protocole de validation en deux phases, et pourquoi l'évite-t-on ?

Un protocole où un coordinateur demande à tous les participants de se préparer puis de valider, garantissant l'atomicité entre systèmes. On l'évite à grande échelle car il bloque en cas de panne, ajoute de la latence et couple la disponibilité de tous les participants ; on préfère les sagas et l'outbox.

#### Qu'est-ce qu'un quorum ?

Le nombre minimal de nœuds qui doivent acquitter une lecture ou une écriture pour qu'elle réussisse (par exemple une majorité). Si le quorum de lecture plus celui d'écriture dépasse le nombre de répliques, les lectures voient la dernière écriture.

#### Qu'est-ce que le décalage d'horloge, et pourquoi compte-t-il ?

Les horloges des différentes machines divergent : on ne peut pas se fier aux horodatages de systèmes différents pour un ordre exact. Pour ordonner les changements, utilisez des horloges logiques, des numéros de séquence ou les positions du journal du système source.

<!-- challenge -->

Un consommateur traite des événements de paiement en at-least-once et compte parfois deux fois le chiffre d'affaires. Corrigez sans changer de broker.

<!-- solution -->

Donner à chaque événement un ID unique et rendre la cible idempotente : upsert ou `MERGE` sur l'ID d'événement (ou une table des ID traités), pour que les événements relivrés ne créent pas de nouvelles lignes.

<!-- takeaways -->

- La livraison at-least-once exige des consommateurs idempotents.
- La backpressure empêche les producteurs rapides de submerger les consommateurs.
- N'ordonnez pas les événements entre machines par l'horloge seule.

<!-- unit: Montée en charge et performance -->

<!-- goals -->

- Choisir entre montée en charge verticale et horizontale.
- Distinguer latence et débit.

<!-- concept -->

Agrandir une seule machine est le geste le plus simple, jusqu'à un plafond ou un saut de prix. Répartir sur de nombreuses machines lève le plafond mais apporte les problèmes distribués : partitionnement, réplication et coordination.
La performance a deux axes qui tirent en sens opposés : la latence est la vitesse d'une requête, le débit le nombre de requêtes terminées par seconde. Le traitement par lots augmente à la fois débit et latence ; les systèmes temps réel sacrifient le débit à la latence.

<!-- example -->

| Conception | Latence | Débit |
|---|---|---|
| Insertion ligne par ligne | Faible par ligne | Faible |
| Lots de 10 000 lignes | Plus élevée par ligne | Élevé |
| Stream en micro-lots d'1 s | Secondes | Moyen |

#### Quelle différence entre latence et débit ?

La latence est la durée d'une opération ; le débit est le nombre d'opérations terminées par unité de temps. Les systèmes batch optimisent le débit ; les systèmes interactifs et de streaming se soucient de la latence ; améliorer l'un peut dégrader l'autre.

#### Quelles approches de modélisation utilise-t-on en architecture des données ?

Des modèles normalisés (3FN) pour l'intégration et l'OLTP, dimensionnels (Kimball) pour l'analytique, Data Vault pour des couches d'intégration auditables, des tables larges dénormalisées (one big table) pour des usages précis, et des modèles anchor ou ensemble dans des cas de niche.

<!-- challenge -->

Un job nocturne qui charge 100 millions de lignes une par une prend 9 heures. Quel compromis changez-vous ?

<!-- solution -->

Privilégier le débit sur la latence par ligne : charger par gros lots ou avec des commandes de masse (`COPY`), en parallèle par partition. Le temps total s'effondre car le coût par ligne disparaît.

<!-- takeaways -->

- Agrandissez pour la simplicité ; répartissez au-delà des limites.
- Latence et débit s'échangent l'un contre l'autre.
- Le traitement par lots augmente le débit.

<!-- stage: Modélisation et motifs de stockage -->

### Approches de modélisation

<!-- unit: Approches de modélisation -->

<!-- goals -->

- Comparer modélisation normalisée, dimensionnelle et autres approches.
- Choisir entre schema-on-write et schema-on-read.

<!-- concept -->

Les modèles encodent ce que signifient les données. Les modèles normalisés stockent chaque fait une fois et conviennent à l'intégration et aux transactions ; les modèles dimensionnels organisent faits et contexte pour une analyse rapide et compréhensible. Les modèles canoniques donnent aux systèmes un langage commun ; des techniques très normalisées comme l'anchor modeling privilégient le changement sur la simplicité.
Le moment où le schéma est imposé compte aussi : à l'écriture, il attrape tôt les erreurs ; à la lecture, il garde de la souplesse pour les données brutes et exploratoires. La plupart des plateformes font les deux, à des couches différentes.

<!-- example -->

| Couche | Approche |
|---|---|
| Brut | Schema-on-read, tel que livré |
| Intégration | 3NF ou Data Vault |
| Consommation | Dimensionnel (schémas en étoile) ou tables larges |

#### Qu'est-ce que la troisième forme normale, et pourquoi l'utiliser ?

Un niveau de normalisation où chaque attribut non clé ne dépend que de la clé, ce qui évite la redondance et les anomalies de mise à jour. Elle convient aux systèmes transactionnels et aux couches d'intégration de style Inmon.

#### Qu'est-ce que l'architecture d'Inmon ?

La Corporate Information Factory de Bill Inmon : un entrepôt d'entreprise en 3FN comme version unique, intégrée et orientée sujet de la vérité, qui alimente des data marts dépendants pour les départements. Descendante, l'intégration d'abord.

#### Qu'est-ce que l'architecture de Kimball ?

La bus architecture de Ralph Kimball : des data marts dimensionnels par processus métier, intégrés par les dimensions conformes et la bus matrix, construits de façon incrémentale. Ascendante, la valeur métier d'abord.

#### Qu'est-ce que Data Vault 2.0 ?

Une méthodologie pour la couche d'intégration avec des hubs (clés métier uniques), des links (relations) et des satellites (attributs descriptifs dans le temps), plus des clés de hachage pour le chargement parallèle, un historique en insertion seule et des standards pour le business vault et les information marts. Conçue pour l'agilité et l'auditabilité avec de nombreuses sources changeantes.

#### Que sont les hubs, links et satellites ?

Les hubs stockent les clés métier (numéro client) avec des métadonnées de chargement ; les links stockent les relations entre hubs (client-commande) ; les satellites stockent les attributs et leur historique pour un hub ou un link, découpés par source ou par fréquence de changement.

<!-- challenge -->

Les analystes interrogent directement un modèle d'intégration en 3NF et écrivent des jointures sur 12 tables pour chaque rapport. Qu'ajoutez-vous ?

<!-- solution -->

Une couche de consommation dimensionnelle : tables de faits par processus métier avec dimensions conformes (ou tables larges pour des usages précis), construites depuis le modèle d'intégration, pour que les rapports n'aient besoin que de peu de jointures prévisibles.

<!-- takeaways -->

- Normalisé pour l'intégration ; dimensionnel pour l'analyse.
- Imposez le schéma à l'écriture là où les erreurs coûtent cher.
- Chaque couche peut suivre une approche différente.

<!-- unit: Inmon, Kimball et Data Vault -->

<!-- goals -->

- Décrire les méthodologies Inmon, Kimball et Data Vault.
- Les combiner dans une plateforme moderne en couches.

<!-- concept -->

Les débats classiques portent sur l'endroit où se fait l'intégration. Inmon intègre d'abord dans un entrepôt d'entreprise normalisé et en tire les data marts. Kimball intègre via des dimensions partagées entre marts par processus. Data Vault sépare clés, relations et historique en hubs, links et satellites, pour ajouter de nouvelles sources sans remodéliser.
En pratique, ce sont des couches plutôt que des rivaux : un vault ou une couche normalisée pour l'intégration et l'audit, des marts dimensionnels pour la consommation.

<!-- example -->

```text
hub_customer       (customer_hk, customer_number, load_ts, source)
link_order_customer (link_hk, order_hk, customer_hk, load_ts, source)
sat_customer_details (customer_hk, load_ts, name, segment, hash_diff)
      └─► dim_customer (Kimball, SCD2) ─► fct_orders
```

#### Quand Data Vault est-il un bon choix ?

Dans les entreprises aux nombreuses sources changeantes, avec de fortes exigences d'audit (finance, assurance, secteurs réglementés) et un besoin de chargement parallèle et d'historique complet. C'est excessif pour des plateformes petites ou à source unique.

#### Qu'est-ce que l'approche « one big table » (OBT) ?

Une seule table large et dénormalisée par cas d'usage contenant tout le nécessaire, rapide dans les moteurs en colonnes et simple pour les outils, au prix d'une logique et d'un stockage dupliqués entre tables. Elle est souvent construite au-dessus de modèles dimensionnels.

#### Comment Kimball, Inmon et Data Vault s'articulent-ils en pratique ?

Une organisation moderne courante : atterrissage brut, une couche d'intégration (normalisée ou Data Vault) qui historise et intègre les sources, puis des schémas en étoile Kimball ou des OBT pour la consommation, souvent alignés sur bronze, silver et gold.

#### Qu'est-ce que le schéma à l'écriture par rapport au schéma à la lecture ?

Le schéma à l'écriture valide et structure les données au chargement (entrepôts), ce qui détecte tôt les erreurs. Le schéma à la lecture stocke les données brutes et applique la structure à la requête (lakes), ce qui est souple mais reporte les problèmes sur les consommateurs. Les lakehouses combinent les deux selon la couche.

#### Qu'est-ce qu'un modèle de données canonique ?

Une représentation partagée et indépendante des applications des entités et événements clés, utilisée pour l'intégration entre systèmes, afin que chaque système se mappe sur le modèle canonique plutôt que sur tous les autres systèmes.

#### Qu'est-ce que l'anchor modeling ?

Une technique très normalisée (6FN) où chaque attribut est stocké dans sa propre table avec son historique, ce qui permet une évolution non destructive du schéma ; rare en pratique, elle a influencé certaines idées de Data Vault.

<!-- challenge -->

Une entreprise de 20 personnes avec trois sources envisage Data Vault « par bonne pratique ». Que conseillez-vous ?

<!-- solution -->

Probablement pas : Data Vault est rentable avec de nombreuses sources changeantes et de fortes exigences d'audit. Avec trois sources, une couche de staging et des marts dimensionnels sont plus simples et plus rapides à livrer ; réexaminer si les sources se multiplient.

<!-- takeaways -->

- Inmon intègre d'abord ; Kimball par dimensions conformes.
- Data Vault sépare clés, relations et historique.
- Combinez-les en couches si nécessaire.

<!-- unit: Façonner les modèles analytiques -->

<!-- goals -->

- Choisir le grain et la forme des jeux de données analytiques.
- Modéliser les données semi-structurées et harmoniser les définitions entre domaines.

<!-- concept -->

Deux décisions façonnent chaque jeu de données analytique. Le grain, ce que représente une ligne, détermine les questions possibles ; choisir le grain le plus fin dont les consommateurs ont besoin laisse des options ouvertes. La forme décide de la facilité d'usage : schémas en étoile pour la souplesse, une table large pour un usage précis.
Entre domaines, la cohérence compte plus que la forme. Des clés et définitions conformes font que « chiffre d'affaires » signifie la même chose dans le rapport de chaque service.

<!-- example -->

```text
grain: one row per order line
fct_order_lines(order_line_id, order_id, product_id, customer_id, date_id, quantity, net_amount)
conformed: dim_customer, dim_product, dim_date shared by sales, finance and marketing
```

#### Comment modéliser des données semi-structurées dans une plateforme analytique ?

Les déposer brutes (JSON, `VARIANT`, colonnes struct), extraire dans les couches suivantes les champs stables et fréquemment utilisés en colonnes typées, garder le reste imbriqué pour la souplesse, et documenter les schémas par des contrats ou un registre.

#### Qu'est-ce qu'un modèle « conforme » entre domaines ?

Des définitions partagées de clés et d'entités (client, produit, date) utilisées par les produits de données de tous les domaines, pour que l'analyse inter-domaines fonctionne ; dans un mesh, elles sont souvent publiées comme produits de données de référence.

#### Comment choisir le grain d'un produit de données ?

À partir des questions des consommateurs et des événements atomiques de la source : choisir le grain le plus fin qui soit stable et utile, le documenter explicitement et proposer les agrégats comme produits séparés.

#### Qu'est-ce qu'un data lake ?

Un référentiel centralisé en stockage objet contenant des données brutes et traitées de tout format et à toute échelle, avec un stockage bon marché et un schéma à la lecture, utilisé pour l'analytique, la data science et comme source des entrepôts.

#### Qu'est-ce qu'un data swamp ?

Un data lake devenu inutilisable : données non documentées, non gouvernées, dupliquées, de qualité et de propriété inconnues. Catalogues, responsables, contrôles de qualité, zones et politiques de cycle de vie l'évitent.

<!-- challenge -->

Une équipe construit une table de synthèse quotidienne comme unique source du chiffre d'affaires. La finance a maintenant besoin du chiffre par ligne de commande. Qu'est-ce qui n'allait pas, et comment corriger ?

<!-- solution -->

Le grain choisi était trop grossier. Construire le fait au grain atomique (ligne de commande) et en dériver la synthèse quotidienne, pour répondre aux nouvelles questions sans revenir aux sources.

<!-- takeaways -->

- Choisissez le grain le plus fin dont les consommateurs ont besoin.
- Tables larges pour des usages précis ; étoiles pour la souplesse.
- Des définitions conformes font concorder les chiffres.

### Data lakes, lakehouses et médaillon

<!-- unit: Lacs, zones et marécages -->

<!-- goals -->

- Décrire les data lakes et leurs zones.
- Prévenir un data swamp et en sortir.

<!-- concept -->

Un data lake conserve à bas coût des données de tout format dans le stockage objet, généralement en zones allant du brut au curé. Sa souplesse est aussi son risque : sans propriétaires, catalogues ni standards, il se remplit de copies non documentées jusqu'à ce que plus personne ne fasse confiance à rien, un marécage.
Les remèdes sont autant organisationnels que techniques : inventaire, propriétaires, zones aux règles claires, un catalogue et des politiques de cycle de vie qui suppriment ce que personne n'utilise.

<!-- example -->

```text
s3://lake/landing/   files as delivered (immutable, short retention after processing)
s3://lake/raw/       standardized format, all history
s3://lake/curated/   validated, modeled, owned and documented
s3://lake/sandbox/   per-user experiments, auto-expire after 30 days
```

#### Quelles zones un data lake comporte-t-il généralement ?

Atterrissage/raw (tel que reçu), nettoyée/standardisée (validée, typée, dédupliquée), curée/consommation (jeux de données prêts pour le métier), plus des zones bac à sable pour l'exploration et des zones d'archive pour les données froides.

#### Qu'est-ce qu'un lakehouse ?

Une architecture qui apporte au stockage du lake les fonctions d'un entrepôt (transactions ACID, contrôle de schéma, gouvernance, performances) grâce aux formats de table ouverts et aux catalogues, pour qu'une seule copie des données serve la BI, le ML et l'ingénierie des données avec plusieurs moteurs.

#### Qu'est-ce que l'architecture médaillon ?

Un modèle de couches du lakehouse : bronze stocke les données brutes telles qu'ingérées (en ajout seul, avec métadonnées), silver les données nettoyées, harmonisées, dédupliquées et historisées, et gold les agrégats métier et modèles dimensionnels prêts à la consommation.

#### Quels sont les avantages de l'architecture médaillon ?

Des responsabilités claires par couche, la possibilité de retraiter à partir des données brutes, une amélioration progressive de la qualité, un débogage facilité (on inspecte chaque couche) et un emplacement naturel pour les barrières de qualité entre couches.

#### Quelles sont les erreurs courantes avec l'architecture médaillon ?

Traiter les couches comme des copies obligatoires même quand elles n'apportent rien, mettre de la logique métier en bronze, laisser les consommateurs lire bronze ou silver directement, des contrats flous entre couches, et copier les données entre couches sans traitement incrémental (coût).

<!-- challenge -->

Le lac compte 8 000 dossiers et personne ne sait lesquels sont utilisés. Donnez les trois premières étapes d'un nettoyage.

<!-- solution -->

Utiliser les journaux d'accès et les métadonnées du catalogue pour savoir ce qui est lu et par qui, attribuer des propriétaires aux jeux utilisés et les enregistrer au catalogue, puis archiver ou supprimer les données inutilisées après avoir annoncé une échéance.

<!-- takeaways -->

- Les lacs stockent tout à bas coût ; les zones structurent.
- Les marécages naissent de l'absence de propriétaires et de métadonnées.
- On en sort par inventaire, propriétaires, catalogue et cycle de vie.

<!-- unit: Lakehouse et médaillon -->

<!-- goals -->

- Expliquer le lakehouse et les couches médaillon.
- Choisir entre lakehouse et entrepôt, et éviter les erreurs courantes du médaillon.

<!-- concept -->

Un lakehouse ajoute au lac des fonctions d'entrepôt (transactions, schémas, gouvernance) grâce aux formats de table et à un catalogue, pour que BI et ML partagent une seule copie des données. Le médaillon en est l'organisation habituelle : bronze tel que reçu, silver nettoyé et conforme, gold prêt à consommer.
Les couches sont un moyen, pas une règle. Copier des données à travers des couches qui n'apportent rien gaspille de l'argent, et mettre de la logique métier en bronze trahit son rôle. Lakehouse ou entrepôt : cela dépend des charges, des compétences et des formats.

<!-- example -->

| Couche | Contrat |
|---|---|
| Bronze | Ajout seul, schéma source, métadonnées d'ingestion |
| Silver | Typé, dédupliqué, clés conformes |
| Gold | Faits, dimensions et agrégats prêts pour le métier |

#### Quel lien entre le médaillon, Kimball et Data Vault ?

Ils sont complémentaires : le médaillon décrit des couches de raffinement ; Data Vault peut être la technique de modélisation en silver ; les schémas en étoile de Kimball sont typiques en gold. Le médaillon est une convention de couches, pas une méthode de modélisation.

#### Lakehouse ou entrepôt : comment décider ?

Un entrepôt (Snowflake, BigQuery, Redshift) est le plus simple pour une BI centrée sur le SQL avec des données structurées. Un lakehouse convient quand il faut des formats ouverts, plusieurs moteurs, de gros volumes semi-structurés ou non structurés, du ML et du streaming sur les mêmes données, ou éviter les copies. Beaucoup d'organisations combinent les deux, et la frontière s'estompe.

#### Quel est le rôle d'un catalogue de données dans un lakehouse ?

C'est le plan de contrôle : registre des tables, schémas, droits, lignage, tags et découverte entre moteurs (Unity Catalog, Glue avec Lake Formation, Polaris), qui transforme des fichiers en tables gouvernées.

#### Quelle différence entre une « zone d'atterrissage » et bronze ?

La zone d'atterrissage conserve les fichiers exactement tels que livrés (CSV, JSON, exports) pour la traçabilité ; bronze est la première représentation en table de ces données avec un minimum de changements plus les métadonnées d'ingestion, interrogeable et gouvernée.

#### Combien de couches un lakehouse doit-il avoir ?

Autant qu'il en apporte une valeur claire : typiquement raw/bronze, nettoyée/silver et consommation/gold, parfois une zone d'atterrissage avant et une couche de service ou sémantique après. Des couches supplémentaires sans contrat propre ne font qu'ajouter du coût.

#### Qu'est-ce que la compaction, et pourquoi les lakehouses en ont-ils besoin ?

La réécriture de nombreux petits fichiers en fichiers moins nombreux et plus gros (et la fusion des fichiers de suppression), qui garde les lectures rapides et les métadonnées compactes. Le streaming et les upserts fréquents la rendent nécessaire ; elle peut être planifiée ou automatique.

#### Comment gérer l'évolution du schéma dans un lakehouse ?

Accepter automatiquement les changements additifs (nouvelles colonnes nullables) en bronze, revoir et appliquer volontairement les changements en silver et gold avec les fonctions du format de table (ajout, renommage, élargissement), et utiliser contrats et alertes pour les changements cassants.

<!-- challenge -->

Une équipe crée des copies bronze, silver et gold d'une petite table de référence qui ne change jamais. Est-ce une bonne pratique ?

<!-- solution -->

Non. Les couches doivent apporter de la valeur ; une table de référence statique peut être chargée une fois en silver (ou gold) et utilisée directement. Garder le fichier brut pour la traçabilité.

<!-- takeaways -->

- Les lakehouses ajoutent au lac des fonctions d'entrepôt.
- Bronze, silver et gold ont des contrats différents.
- N'utilisez une couche que si elle apporte de la valeur.

<!-- unit: Exploiter un lakehouse -->

<!-- goals -->

- Utiliser le catalogue comme plan de contrôle du lakehouse.
- Planifier compaction, évolution de schéma et time travel.

<!-- concept -->

Un lakehouse ne vaut que par son entretien. Le catalogue enregistre tables, permissions et lignage : il devient le plan de contrôle. Les écritures fréquentes créent petits fichiers et fichiers de suppression, donc la compaction est une maintenance de routine. Les schémas évoluent, donc chaque couche a besoin d'une politique : permissive en bronze, contrôlée en silver et gold.
Le time travel fait de l'historique des tables un outil d'audit, de reproduction et de reprise, dans les limites de rétention fixées par la maintenance.

<!-- example -->

```sql
OPTIMIZE silver.orders;                                 -- compaction (Delta)
SELECT * FROM gold.revenue TIMESTAMP AS OF '2026-09-30'; -- reproduce month-end report
ALTER TABLE bronze.events ADD COLUMNS (device_type STRING); -- additive change
```

#### À quoi sert le « voyage dans le temps » d'un point de vue architectural ?

À reproduire des rapports à une date, auditer, comprendre ce qui a changé, récupérer d'écritures erronées et comparer des versions, à condition que les politiques de rétention conservent assez d'historique.

#### Quelle différence entre traitement batch et streaming ?

Le batch traite des jeux de données bornés à intervalles (horaires, quotidiens) avec un fort débit et une logique plus simple ; le streaming traite en continu des flux d'événements sans fin avec une faible latence, ce qui exige gestion d'état, prise en compte du temps de l'événement et tolérance aux pannes.

#### Qu'est-ce que l'architecture Lambda ?

L'architecture de Nathan Marz avec une couche batch (recalcule des vues exactes à partir de tout l'historique), une couche de vitesse (traite les données récentes en temps réel) et une couche de service qui fusionne les deux. Elle apporte exactitude et faible latence mais duplique la logique dans deux chemins de code.

#### Qu'est-ce que l'architecture Kappa ?

La simplification de Jay Kreps : un chemin unique de traitement en streaming où tout est flux ; le retraitement se fait en rejouant le journal (Kafka) dans une nouvelle version du job. Elle supprime la logique dupliquée mais exige un journal durable et rejouable et un streaming robuste.

<!-- challenge -->

Un auditeur demande le chiffre d'affaires exact publié par l'entreprise le 30 septembre, alors que les données ont été corrigées depuis. Comment l'architecture aide-t-elle ?

<!-- solution -->

Avec le time travel sur la table gold (rétention couvrant cette date), on l'interroge telle qu'elle était à l'instant de la publication. Pour le long terme, figer les chiffres publiés dans une table immuable, car la rétention du time travel est limitée.

<!-- takeaways -->

- Le catalogue est le plan de contrôle du lakehouse.
- La compaction garde les lectures rapides.
- Le time travel aide l'audit dans la limite de sa rétention.

<!-- stage: Déplacer les données -->

### Architectures batch et streaming

<!-- unit: Batch, streaming et leurs architectures -->

<!-- goals -->

- Comparer traitement batch, micro-batch et streaming.
- Expliquer Lambda et Kappa et décider quand le temps réel est nécessaire.

<!-- concept -->

Batch et streaming diffèrent par le moment du calcul, pas par son contenu. Le batch traite des données bornées selon un calendrier, simplement et à bas coût. Le streaming traite les événements à leur arrivée, pour des décisions qui perdent leur valeur en quelques minutes.
Lambda faisait tourner les deux chemins en parallèle ; Kappa utilisait des streams pour tout. Les moteurs modernes brouillent la frontière en exécutant le même code en batch ou en stream. La vraie question est la latence métier : la plupart des tableaux de bord se contentent de l'heure, et le temps réel coûte plus cher.

<!-- example -->

| Cas d'usage | Latence requise | Approche |
|---|---|---|
| Contrôle de fraude sur un paiement par carte | < 1 s | Streaming |
| Stock affiché sur le site | Minutes | Micro-batch ou streaming |
| Tableau de bord CA de la direction | Heures | Batch |

#### Lambda ou Kappa : laquelle utilise-t-on aujourd'hui ?

La Lambda pure est rare car maintenir deux bases de code coûte cher. Les plateformes modernes utilisent des moteurs unifiés (Spark Structured Streaming, Flink, Beam) et des formats de table qui acceptent batch et streaming sur les mêmes tables, plus proche de Kappa, avec des backfills batch si nécessaire.

#### Qu'est-ce que le temps de l'événement par rapport au temps de traitement ?

Le temps de l'événement est le moment où quelque chose s'est produit à la source ; le temps de traitement est le moment où le système le traite. Une analytique correcte a généralement besoin du temps de l'événement, car les événements arrivent en retard et dans le désordre.

#### Que sont les fenêtres en traitement de flux ?

Des regroupements temporels d'événements pour les agréger : tumbling (fixes, sans chevauchement), sliding ou hopping (chevauchantes) et fenêtres de session (des périodes d'inactivité délimitent les sessions).

#### Qu'est-ce qu'un watermark en streaming ?

Un seuil de temps d'événement jusqu'auquel le système considère avoir vu tous les événements, ce qui permet de fermer les fenêtres et de nettoyer l'état ; les événements plus tardifs que le watermark sont ignorés ou traités à part.

#### Quel est le rôle d'Apache Kafka dans l'architecture des données ?

Un journal d'événements distribué, durable et rejouable : il découple producteurs et consommateurs, absorbe les pics, permet à plusieurs consommateurs de lire les mêmes données à leur rythme, et sert de colonne vertébrale au streaming, au CDC et aux systèmes événementiels.

#### Que sont les topics, partitions et groupes de consommateurs Kafka ?

Un topic est un flux nommé d'enregistrements ; il est découpé en partitions (journaux ordonnés et répliqués) pour le parallélisme ; un groupe de consommateurs répartit les partitions entre ses membres, chaque partition étant lue par un seul consommateur du groupe, ce qui donne une consommation scalable avec un ordre par partition.

#### Comment l'ordre est-il garanti dans Kafka ?

Uniquement au sein d'une partition. Les enregistrements de même clé vont dans la même partition, donc l'ordre par clé est préservé ; l'ordre global entre partitions n'est pas garanti.

<!-- challenge -->

Un product manager demande un tableau de bord en temps réel des utilisateurs actifs hebdomadaires. Que proposez-vous ?

<!-- solution -->

Demander quelle décision en dépend. Les utilisateurs actifs hebdomadaires évoluent lentement : un batch horaire ou quotidien suffit et coûte bien moins. Réserver le streaming aux métriques qui déclenchent une action immédiate.

<!-- takeaways -->

- Le batch est simple et bon marché ; le streaming sert l'urgent.
- Les moteurs unifiés remplacent les chemins séparés de Lambda.
- Alignez la latence sur la valeur métier.

<!-- unit: Le temps dans les streams -->

<!-- goals -->

- Distinguer event time et processing time.
- Utiliser correctement fenêtres, watermarks et état.

<!-- concept -->

Les événements arrivent en retard et dans le désordre : un processeur de streams doit choisir à quelle horloge se fier. L'event time, quand la chose s'est produite, donne des résultats justes ; le processing time, quand elle est arrivée, est plus simple mais faux dès que les délais varient.
Les fenêtres regroupent les événements en event time, les watermarks décident combien de temps attendre les retardataires, et l'état mémorise les résultats partiels entre-temps. Joindre des données de référence pose une autre question de temps : quelle version de la référence s'appliquait au moment de l'événement.

<!-- example -->

```python
(events
 .withWatermark("event_time", "10 minutes")           # wait up to 10 min for late events
 .groupBy(F.window("event_time", "5 minutes"), "store_id")
 .agg(F.sum("amount").alias("revenue")))
```

#### Qu'est-ce qu'un schema registry ?

Un service qui stocke des schémas versionnés (Avro, Protobuf, JSON Schema) pour les topics et applique des règles de compatibilité, pour que les producteurs ne publient pas de changements cassants et que les consommateurs désérialisent de façon fiable.

#### Quels moteurs de traitement de flux existent ?

Apache Flink (faible latence, avec état, temps d'événement), Spark Structured Streaming (micro-batch et continu, intégré à Spark), Kafka Streams et ksqlDB (bibliothèque et SQL sur Kafka), Apache Beam (modèle portable, exécuté sur Dataflow) et des services gérés (Kinesis Data Analytics/Managed Flink, Confluent, Databricks).

#### Quand le temps réel est-il vraiment nécessaire ?

Quand les décisions ou actions perdent leur valeur en quelques secondes ou minutes : détection de fraude, alertes opérationnelles, personnalisation, supervision IoT, tarification dynamique. Beaucoup de tableaux de bord n'en ont pas besoin ; le batch ou le micro-batch est moins cher et plus simple.

#### Qu'est-ce qu'une base de données de streaming ou un stockage OLAP temps réel ?

Des systèmes conçus pour ingérer des flux et servir des requêtes analytiques à faible latence sur des données fraîches (Apache Druid, Apache Pinot, ClickHouse, Materialize, RisingWave), utilisés pour l'analytique exposée aux utilisateurs et les tableaux de bord opérationnels.

#### Qu'est-ce que le micro-batch ?

Le traitement d'un flux comme une suite de petits lots (de quelques secondes à quelques minutes), comme le fait par défaut Spark Structured Streaming. Il simplifie la tolérance aux pannes et réutilise la logique batch, avec une latence un peu plus élevée qu'un traitement événement par événement.

<!-- challenge -->

Les événements d'une application mobile peuvent arriver des heures en retard quand les téléphones sont hors ligne. Le chiffre d'affaires par fenêtre de 5 minutes ne cesse de changer dans le tableau de bord. Comment concevoir ?

<!-- solution -->

Agréger en event time avec un watermark qui borne le retard pour la vue en direct, et recalculer les chiffres définitifs dans un job batch (ou par upserts) qui inclut les événements tardifs. Signaler les fenêtres récentes comme provisoires.

<!-- takeaways -->

- Utilisez l'event time pour des résultats justes.
- Les watermarks bornent l'attente des données tardives.
- L'état garde les résultats partiels ; les jointures de référence exigent des versions.

<!-- unit: Kafka comme colonne vertébrale -->

<!-- goals -->

- Expliquer topics, partitions, consumer groups et ordre dans Kafka.
- Utiliser schema registries, traitement exactly-once et rejeu.

<!-- concept -->

Kafka est un journal durable et rejouable. Les producteurs ajoutent des événements ; un nombre quelconque de consumer groups les lisent à leur rythme ; les données restent pendant une période de rétention, ou indéfiniment avec le tiered storage. Ce découplage explique pourquoi il devient souvent la colonne vertébrale entre systèmes.
Ses garanties sont précises : ordre seulement au sein d'une partition, donc les clés choisissent la partition ; exactly-once seulement dans les transactions Kafka ; compatibilité seulement si les schémas sont imposés. Rejouer depuis le journal est la façon standard de retraiter.

<!-- example -->

```text
topic orders (6 partitions, key = customer_id)
  → all events of one customer in order, on one partition
consumer group "billing"   reads every event once (split across its consumers)
consumer group "analytics" reads every event independently
```

#### Qu'est-ce que le traitement de flux avec état ?

Un traitement qui conserve des informations d'un événement à l'autre (comptages par fenêtre, état de session, jointures entre flux, déduplication), ce qui exige des stockages d'état tolérants aux pannes et des checkpoints ; Flink et Spark gèrent l'état par snapshots.

#### Comment joindre des flux à des données de référence ?

Diffuser (broadcast) les données de référence à évolution lente vers les processeurs de flux et les rafraîchir périodiquement, joindre à un flux de changements (tables temporelles ou versionnées), ou interroger un stockage rapide (Redis, DynamoDB) avec cache.

#### Qu'est-ce que le traitement exactly-once dans Kafka ?

Des producteurs idempotents plus des transactions qui écrivent atomiquement les enregistrements de sortie et valident les offsets consommateurs, pour que les effets d'un cycle lecture-traitement-écriture n'aient lieu qu'une fois même avec des relances, dans des pipelines Kafka vers Kafka.

#### Comment retraiter des données dans une architecture de streaming ?

Rejouer depuis le journal (rétention ou stockage hiérarchisé de Kafka) dans une nouvelle version du job écrivant dans de nouvelles tables, valider, puis basculer les consommateurs ; ou faire un backfill depuis les tables du lakehouse avec un job batch utilisant la même logique.

#### Que sont le stockage hiérarchisé et la rétention infinie dans Kafka ?

Le déchargement des segments de journal anciens vers un stockage objet, pour que les topics gardent de longs historiques à moindre coût, permettant des rejeux et des retraitements de type Kappa sans disques énormes sur les brokers.

#### Comment les microservices changent-ils l'architecture des données ?

Chaque service possède ses données et sa base (une base par service) et communique par API et événements plutôt que par tables partagées. Cela améliore l'autonomie et la montée en charge, mais disperse les données et exige des modèles d'intégration pour l'analytique et les requêtes inter-services.

#### Qu'est-ce que le modèle « une base par service » ?

Chaque microservice a une base privée à laquelle lui seul accède ; les autres services utilisent son API ou ses événements. Cela évite un couplage fort via des schémas partagés.

<!-- challenge -->

Les événements de statut de commande (créée, payée, expédiée) arrivent parfois dans le désordre chez un consommateur. Le topic a 12 partitions et pas de clé. Que changez-vous ?

<!-- solution -->

Produire avec `order_id` comme clé, pour que tous les événements d'une commande aillent dans la même partition et restent ordonnés. Les consommateurs doivent aussi tolérer les doublons et utiliser un numéro de séquence par sécurité.

<!-- takeaways -->

- Kafka est un journal durable et rejouable.
- L'ordre vaut par partition ; les clés choisissent la partition.
- Schema registries et rejeu gardent les streams évolutifs.

<!-- unit: Moteurs de streaming et restitution -->

<!-- goals -->

- Comparer moteurs de traitement de streams et bases de restitution temps réel.
- Ajouter du scoring temps réel à une plateforme batch.

<!-- concept -->

Traiter et restituer sont deux choix distincts. Des moteurs comme Flink, Spark Structured Streaming et Kafka Streams calculent sur des streams et diffèrent surtout par la latence, la gestion de l'état et les compétences requises. Servir des résultats frais aux utilisateurs exige une base conçue pour des requêtes à faible latence sur des données récentes, ce que les entrepôts ordinaires ne sont pas.
Ajouter du temps réel à une plateforme batch signifie généralement un chemin parallèle pour les rares cas qui en ont besoin, en réutilisant les mêmes définitions.

<!-- example -->

```text
payments ─► Kafka ─► Flink: features (txn count 5 min, amount vs avg)
                         └─► model endpoint ─► decision < 200 ms
                         └─► feature log ─► lake (training, audit)
```

#### Pourquoi une base partagée est-elle un anti-modèle avec les microservices ?

Les services deviennent couplés par le schéma : le changement d'une équipe en casse d'autres, les déploiements doivent être coordonnés et la responsabilité devient floue, ce qui fait perdre le principal intérêt des microservices.

#### Comment faire de l'analytique entre microservices ?

Capturer les données de chaque service (CDC de sa base ou ses événements de domaine) dans un lake ou un entrepôt, les modéliser de façon centrale ou par domaine, et servir l'analytique depuis là, plutôt que d'interroger directement les bases des services.

#### Qu'est-ce que l'architecture orientée événements ?

Des systèmes qui communiquent en produisant des événements et en y réagissant (des faits sur quelque chose qui s'est produit : `OrderPlaced`, `PaymentFailed`) via un broker, plutôt que par des appels synchrones, ce qui apporte couplage faible, scalabilité et piste d'audit naturelle.

<!-- challenge -->

Les features de fraude en temps réel et celles de l'entraînement du modèle sont calculées par du code différent et ne concordent pas. Comment corriger ?

<!-- solution -->

Calculer les features une seule fois (mêmes définitions) et journaliser dans le lac les valeurs utilisées pour chaque décision ; entraîner sur ces features journalisées ou utiliser un feature store qui sert les mêmes définitions en ligne et hors ligne.

<!-- takeaways -->

- Les moteurs diffèrent par latence, état et compétences.
- La restitution temps réel exige des bases à faible latence.
- N'ajoutez du temps réel que là où il faut, avec des définitions partagées.

### Microservices et données événementielles

<!-- unit: Propriété des données dans les microservices -->

<!-- goals -->

- Expliquer database-per-service et pourquoi les bases partagées échouent.
- Faire de l'analytique entre services sans dépendre de leurs internes.

<!-- concept -->

Les microservices découpent les systèmes pour que les équipes évoluent indépendamment, ce qui ne marche que si chaque service possède ses données. Une base partagée couple tout le monde à un schéma ; le changement d'une équipe casse les autres.
La même logique vaut pour l'analytique. Lire les tables internes des services fait de l'équipe data un consommateur caché de chaque changement de schéma. Contrats, événements publiés ou flux CDC aux formes convenues laissent les services évoluer tandis que l'analytique continue de fonctionner.

<!-- example -->

```text
orders-service ─ its own DB ─► publishes OrderPlaced v2 (contract) ─► Kafka ─► lake
payments-service ─ its own DB ─► CDC on the outbox table only     ─► Kafka ─► lake
data team reads contracts, not internal tables
```

#### Quelle différence entre événements, commandes et messages ?

Une commande demande à quelqu'un de faire quelque chose (`ShipOrder`) et peut être refusée ; un événement constate que quelque chose s'est produit (`OrderShipped`) et est immuable ; le message est l'enveloppe générique qui transporte l'un ou l'autre.

#### Qu'est-ce que l'event sourcing ?

Stocker l'état d'une entité sous la forme de la séquence d'événements qui l'ont modifié, plutôt que son état courant ; l'état courant se reconstruit en rejouant les événements. Cela donne un journal d'audit complet et le voyage dans le temps, mais complique les requêtes et l'évolution du schéma.

#### Qu'est-ce que CQRS ?

Command Query Responsibility Segregation : séparer le modèle d'écriture (commandes, validation) des modèles de lecture (vues optimisées pour les requêtes), souvent mis à jour de façon asynchrone à partir d'événements. Cela fait monter en charge lectures et écritures indépendamment et va bien avec l'event sourcing.

#### Qu'est-ce que le modèle transactional outbox ?

Un service écrit sa modification métier et un enregistrement d'événement dans une table outbox au sein de la même transaction ; un processus séparé (souvent du CDC) publie les enregistrements de l'outbox dans le broker. Cela évite le problème de la double écriture (mettre à jour la base et publier un événement séparément).

#### Qu'est-ce que le problème de la double écriture ?

Quand un service écrit dans sa base et publie un événement en deux opérations séparées, l'une peut réussir et l'autre échouer, laissant les systèmes incohérents. L'outbox ou la publication par CDC le résolvent.

#### Qu'est-ce que le modèle saga ?

Une façon d'exécuter des transactions métier couvrant plusieurs services comme une séquence de transactions locales avec des actions compensatoires en cas d'échec, coordonnées par chorégraphie (événements) ou orchestration (un coordinateur), au lieu de commits distribués en deux phases.

<!-- challenge -->

Les pipelines de l'équipe data cassent chaque fois qu'un service renomme une colonne. Quel accord proposez-vous aux équipes de services ?

<!-- solution -->

Chaque service publie des événements d'intégration ou une vue exposée par CDC avec un contrat versionné, enregistré dans un schema registry avec contrôles de compatibilité. Les tables internes changent librement ; les changements de contrat passent par le versionnage.

<!-- takeaways -->

- Chaque service possède ses données.
- Les bases partagées couplent les équipes.
- L'analytique doit consommer des contrats, pas des internes.

<!-- unit: Événements et commandes -->

<!-- goals -->

- Distinguer événements, commandes et messages.
- Concevoir et versionner des événements dont d'autres peuvent dépendre.

<!-- concept -->

Les systèmes orientés événements communiquent des faits. Une commande demande à un service de faire quelque chose et peut être refusée ; un événement affirme que quelque chose s'est déjà produit et ne se discute pas. Les faits font une bonne intégration, car on peut ajouter des consommateurs sans modifier le producteur.
Cela fait des événements des interfaces publiques. Il leur faut des noms clairs, des ID, des horodatages et des schémas, un choix entre transporter les données ou des références, et des règles de versionnage qui préservent les anciens consommateurs.

<!-- example -->

```json
{
  "event_id": "0192f0c3-7a1e-7b3c-9d4e-5f6a7b8c9d0e",
  "event_type": "OrderPlaced",
  "schema_version": 2,
  "occurred_at": "2026-10-17T09:41:12Z",
  "order_id": 98123,
  "customer_id": 552,
  "total_amount": "129.90",
  "currency": "EUR"
}
```

#### Quel est le rôle du CDC dans l'intégration des données de microservices ?

Le CDC lit le journal de la base de chaque service et publie les changements sous forme d'événements sans modifier les services, alimentant l'analytique et d'autres services ; c'est plus simple que d'ajouter des événements à du code historique, mais cela expose les schémas internes sauf à utiliser une outbox ou un contrat.

#### Quelle différence entre événements de domaine et événements d'intégration ?

Les événements de domaine sont internes au modèle d'un service ; les événements d'intégration sont des contrats publiés pour les autres services et l'analytique, stables et versionnés, volontairement découplés des schémas internes.

#### Quel est le rôle d'une API gateway dans l'accès aux données ?

Un point d'entrée unique pour les requêtes clientes qui route vers les services et gère authentification, limitation de débit et agrégation. Pour les produits de données, des API ou des couches GraphQL exposent des données curées aux applications.

#### Comment concevoir les événements ?

Nommés au passé, avec un schéma clair, un identifiant d'événement, des horodatages (de l'événement et de publication), la clé de l'entité, une version et assez de données pour les consommateurs (événements riches) ou une référence pour récupérer les détails (événements légers), et une évolution compatible.

#### Quelle différence entre événements légers et riches ?

Les événements légers ne portent que des identifiants et le type de changement, si bien que les consommateurs doivent rappeler pour obtenir les détails (couplage, charge sur le producteur) ; les événements riches (event-carried state transfer) portent tout l'état nécessaire, permettant des consommateurs autonomes au prix de messages plus gros et d'une attention accrue au schéma.

#### Comment versionner les schémas d'événements ?

Avec un schema registry et des règles de compatibilité, en ajoutant des champs optionnels plutôt qu'en changeant les sens, en introduisant de nouveaux types ou versions d'événements pour les changements cassants, et en conservant les anciennes versions jusqu'à la migration de tous les consommateurs.

<!-- challenge -->

Une équipe veut renommer `total` en `total_amount` dans un événement consommé par six services. Comment le faire sans risque ?

<!-- solution -->

Ajouter `total_amount` comme nouveau champ optionnel tout en envoyant encore `total`, enregistrer le schéma rétrocompatible, migrer les consommateurs, puis retirer `total` dans une nouvelle version majeure après une période de dépréciation.

<!-- takeaways -->

- Les commandes demandent ; les événements constatent des faits.
- Les événements d'intégration sont des contrats publics.
- Versionnez les événements avec des règles de compatibilité.

<!-- unit: Cohérence entre services -->

<!-- goals -->

- Éviter le problème de double écriture avec le motif outbox et le CDC.
- Coordonner des processus multi-services avec sagas, event sourcing et CQRS.

<!-- concept -->

Sans transactions partagées, garder des services cohérents devient un problème de conception. Écrire dans une base puis publier un événement séparément peut perdre l'un des deux ; le motif outbox écrit les deux dans une transaction locale et publie ensuite, souvent par CDC.
Les processus plus longs deviennent des sagas d'étapes locales avec compensations. L'event sourcing stocke l'état comme son historique d'événements, et le CQRS sépare modèles d'écriture et de lecture ; tous deux servent quand l'audit ou la performance de lecture justifient leur complexité.

<!-- example -->

```sql
BEGIN;
UPDATE orders SET status = 'paid' WHERE order_id = 98123;
INSERT INTO outbox (event_id, type, payload) VALUES (gen_random_uuid(), 'OrderPaid', '{"order_id":98123}');
COMMIT;
-- CDC (Debezium) publishes outbox rows to Kafka
```

#### Quelle différence entre chorégraphie et orchestration ?

Dans la chorégraphie, les services réagissent aux événements des autres sans coordinateur central (couplage faible, flux global plus difficile à voir) ; dans l'orchestration, un coordinateur dit aux services quoi faire (flux clair, dépendance centrale). Les pipelines de données utilisent surtout l'orchestration (Airflow) ; les sagas de microservices l'une ou l'autre.

#### Qu'est-ce que le data mesh ?

L'approche socio-technique de Zhamak Dehghani fondée sur quatre principes : responsabilité des données orientée domaine, données en tant que produit, plateforme de données en libre-service et gouvernance computationnelle fédérée. Elle décentralise la responsabilité des données vers les domaines qui les connaissent.

#### Quel problème le data mesh cherche-t-il à résoudre ?

Des équipes data centrales devenues goulots d'étranglement entre de nombreux domaines sources et de nombreux consommateurs, perdant le contexte métier et passant mal à l'échelle quand l'organisation grandit.

#### Qu'est-ce qu'un produit de données dans le data mesh ?

Un jeu de données d'un domaine exposé à la consommation, avec un responsable, une interface (tables, API, événements), une documentation, des garanties de qualité et de SLA, la découvrabilité, la sécurité et le versionnage, construit sur la plateforme partagée.

#### Qu'est-ce que la gouvernance computationnelle fédérée ?

Une gouvernance où les standards globaux (interopérabilité, sécurité, confidentialité, indicateurs de qualité) sont décidés par une fédération de représentants des domaines et de la plateforme et appliqués automatiquement par la plateforme (politiques sous forme de code), les domaines décidant localement dans ce cadre.

#### Quel est le rôle de l'équipe plateforme dans un data mesh ?

Fournir une infrastructure en libre-service (stockage, calcul, pipelines, catalogue, contrôle d'accès, observabilité, modèles) pour que les équipes de domaine construisent des produits de données sans expertise approfondie de la plateforme.

#### Quand le data mesh est-il inadapté ?

Dans les petites organisations, avec peu de domaines, une faible maturité data ou sans capacité dans les domaines pour porter des produits de données. Sans investissement dans la plateforme et la gouvernance, le mesh devient un ensemble de données fragmentées et incohérentes.

<!-- challenge -->

Un service de commandes met à jour sa base puis publie un événement dans Kafka. Après un crash, l'événement manque parfois. Quel motif corrige cela ?

<!-- solution -->

Le transactional outbox : écrire l'événement dans une table outbox dans la même transaction que la mise à jour de la commande, puis le publier depuis l'outbox (par CDC ou un relais), pour que les deux aient lieu ou aucun.

<!-- takeaways -->

- Des écritures séparées en base et dans le broker peuvent diverger.
- Le motif outbox les rend atomiques.
- Les sagas coordonnent ; event sourcing et CQRS servent des besoins précis.

### Data mesh et data fabric

<!-- unit: Motifs d'intégration -->

<!-- goals -->

- Comparer ETL, ELT, CDC, événements, virtualisation et reverse ETL.
- Choisir un motif d'intégration par source.

<!-- concept -->

Il n'existe qu'une poignée de façons de déplacer des données, et chaque source mérite la bonne. Les extractions batch conviennent aux sources qui changent peu ou n'offrent rien d'autre. Le CDC capture chaque changement des bases avec peu d'impact. Les événements conviennent aux systèmes qui publient déjà des faits. La virtualisation évite de copier quand les requêtes sont rares. Le reverse ETL renvoie des données modélisées dans les outils opérationnels.
L'ELT est devenu la norme parce que stockage et moteurs cloud ont rendu bon marché de charger d'abord et de transformer là où les données arrivent.

<!-- example -->

| Source | Motif |
|---|---|
| PostgreSQL de production | CDC |
| CRM SaaS | Connecteur managé, incrémental |
| Dépôt CSV d'un partenaire | Ingestion batch de fichiers |
| Microservice avec événements métier | Flux d'événements |
| Scores clients renvoyés au CRM | Reverse ETL |

#### Qu'est-ce qu'une data fabric ?

Une architecture qui utilise les métadonnées, les graphes de connaissances, l'automatisation et la virtualisation pour intégrer des données de sources distribuées et présenter une couche d'accès unifiée et gouvernée, en mettant l'accent sur la technologie (métadonnées actives) plutôt que sur l'organisation.

#### Quelle différence entre data mesh et data fabric ?

Le data mesh est d'abord organisationnel (qui possède les données, logique produit), avec de la décentralisation ; la data fabric est d'abord technologique (intégration par les métadonnées et l'automatisation), souvent centralisée. On peut les combiner.

#### Comment démarrer une démarche de data mesh ?

Choisir un ou deux domaines motivés avec des consommateurs clairs, construire une plateforme en libre-service minimale (modèles, catalogue, contrôle d'accès, qualité), définir quelques standards globaux, livrer des produits de données de bout en bout, mesurer l'adoption, puis étendre.

#### Comment les produits de données restent-ils interopérables dans un mesh ?

Grâce à des standards globaux : identifiants et données de référence partagés, conventions de nommage et de métadonnées, formats et méthodes d'accès communs, indicateurs de qualité, et un catalogue central pour la découverte.

#### Quels indicateurs montrent qu'un data mesh fonctionne ?

Le délai de livraison de nouveaux produits de données, le nombre de produits ayant des consommateurs actifs, le respect des SLO de qualité, la baisse des demandes adressées à l'équipe centrale, la réutilisation entre domaines et la satisfaction des consommateurs.

<!-- challenge -->

Une équipe lance chaque nuit un export complet d'une base de production de 2 To qui dure 6 heures et ralentit l'application. Que proposez-vous ?

<!-- solution -->

Passer au CDC : un snapshot initial suivi de la capture des changements depuis le journal de la base, qui ne charge que les changements avec peu d'impact sur la source et donne des données plus fraîches.

<!-- takeaways -->

- Choisissez le motif d'intégration par source.
- L'ELT charge d'abord et transforme dans la plateforme.
- Le reverse ETL boucle vers les outils opérationnels.

<!-- unit: Ingérer de façon fiable -->

<!-- goals -->

- Ingérer depuis API, fichiers et fournisseurs avec des contrats.
- Gérer les données tardives et passer l'ingestion à l'échelle par les métadonnées.

<!-- concept -->

L'ingestion est l'endroit où les problèmes des systèmes externes deviennent les vôtres : limites de débit, fichiers manquants, schémas modifiés, enregistrements tardifs. Les contrats fixent les attentes à l'avance : schémas, calendriers de livraison, signaux de complétude et qui appeler. Des chargements idempotents par upsert absorbent données tardives et répétées.
Quand les sources se multiplient, un pipeline par source ne passe plus à l'échelle. Un composant générique et testé, configuré par des métadonnées, ingère chaque nouvelle source avec une entrée de configuration au lieu de nouveau code.

<!-- example -->

```yaml
# sources.yaml driving one generic ingestion job
- name: crm_accounts
  type: api
  endpoint: /v2/accounts
  incremental_key: updated_at
  primary_key: id
  schedule: hourly
- name: partner_sales
  type: s3_files
  path: s3://landing/partner/sales/
  format: csv
  completeness_marker: _SUCCESS
```

#### Que sont les « métadonnées actives » ?

Des métadonnées qui déclenchent des automatismes plutôt que de simplement documenter : des tags qui appliquent un masquage, un lignage qui alerte sur les changements en amont, des statistiques d'usage qui suggèrent une dépréciation, des indicateurs de qualité qui bloquent la publication.

#### Quels sont les principaux modèles d'intégration de données ?

L'ETL/ELT batch, la capture des changements (CDC), le streaming d'événements, l'intégration par API, la virtualisation/fédération de données, les transferts de fichiers et le reverse ETL pour renvoyer des données curées vers les outils opérationnels.

#### Qu'est-ce que l'ELT, et pourquoi est-il devenu dominant ?

Charger d'abord les données brutes dans un stockage cloud ou un entrepôt élastique et les transformer sur place en SQL (souvent avec dbt). Le stockage bon marché et le calcul élastique l'ont rendu plus simple et plus souple que la transformation avant chargement.

#### Qu'est-ce que la virtualisation des données ?

Interroger les données là où elles se trouvent via une couche logique (Denodo, Trino, requêtes fédérées) sans les copier. C'est rapide à mettre en place et évite la duplication, mais les performances, l'historique et la charge sur les sources sont des limites.

#### Qu'est-ce que le reverse ETL ?

La synchronisation de données modélisées de l'entrepôt vers des systèmes opérationnels (CRM, marketing, outils de support) pour que les équipes métier agissent sur l'analytique, bouclant la boucle entre analyse et opérations.

#### Que faut-il prendre en compte pour ingérer depuis des API ?

L'authentification, la pagination, les limites de débit et les relances avec backoff, l'extraction incrémentale (curseurs, updated-since), la dérive de schéma, l'idempotence, la conservation des réponses brutes pour le retraitement, et la surveillance des changements silencieux de l'API.

<!-- challenge -->

Un partenaire dépose parfois un demi-fichier, et le pipeline le charge avant l'arrivée du reste. Que convenez-vous avec lui, et que changez-vous ?

<!-- solution -->

Convenir d'un signal de complétude dans le contrat de dépôt (un manifest ou un fichier `_SUCCESS` écrit en dernier, avec les nombres de lignes), et ne démarrer le pipeline que lorsqu'il est présent et que les comptes concordent.

<!-- takeaways -->

- Les contrats fixent les attentes avec les producteurs.
- Les upserts idempotents absorbent données tardives et répétées.
- L'ingestion pilotée par métadonnées passe à l'échelle.

<!-- stage: Organiser et gouverner -->

### Intégration et ingestion

<!-- unit: Principes du data mesh -->

<!-- goals -->

- Expliquer les quatre principes du data mesh et le problème qu'il traite.
- Décrire produits de données, gouvernance fédérée et équipe plateforme.

<!-- concept -->

Les équipes data centrales deviennent des goulots quand de nombreux domaines produisent des données et que de nombreux consommateurs en ont besoin. Le data mesh confie la propriété aux domaines qui connaissent les données, leur demande de les publier comme produits avec garanties, leur fournit une plateforme self-service pour ne pas reconstruire l'infrastructure chacun, et maintient des standards globaux par une gouvernance fédérée.
C'est davantage un changement organisationnel que technique : le plus dur est de donner aux domaines les compétences, les incitations et la capacité d'assumer leurs données.

<!-- example -->

| Principe | En pratique |
|---|---|
| Propriété par domaine | L'équipe paiements possède les données de paiement |
| Données comme produit | `payments.transactions` avec SLA, doc, propriétaire |
| Plateforme self-service | Modèles de pipelines, catalogue, accès |
| Gouvernance fédérée | Règles globales sur ID, PII, métriques de qualité |

#### Qu'est-ce qu'un contrat de données dans l'intégration ?

Un accord explicite et versionné sur le schéma, la sémantique, la qualité et les SLA d'un jeu de données ou d'un événement entre producteur et consommateurs, validé en CI et à l'exécution, qui rend visibles les changements cassants avant qu'ils ne cassent les pipelines.

#### Comment gérer les données tardives et désordonnées dans l'intégration ?

Utiliser les horodatages d'événement, admettre des fenêtres de retard, concevoir des upserts et des écritures idempotentes, retraiter les partitions récentes et suivre la complétude des données pour que les consommateurs sachent quand une période est définitive.

#### Comment choisir entre CDC, extractions batch et événements pour une source ?

Le CDC pour les bases qu'on ne peut pas modifier et dont on veut tous les changements avec une faible latence et peu d'impact ; les extractions batch pour des données petites ou peu changeantes et les sources sans accès au journal ; les événements quand on maîtrise l'application et qu'on veut une sémantique métier.

#### Que sont les connecteurs gérés, et quand ont-ils du sens ?

Des services comme Fivetran, Airbyte Cloud, Lakeflow Connect ou AppFlow qui extraient des applications SaaS et des bases avec des connecteurs maintenus et une gestion du schéma. Ils font gagner du temps d'ingénierie sur les sources standard, pour un coût au volume ; le code maison se justifie pour des sources inhabituelles ou des volumes énormes.

#### Comment concevoir l'ingestion pour de nombreuses sources similaires ?

Avec des pipelines pilotés par les métadonnées : un composant d'ingestion générique et testé, configuré par source (connexion, tables, clés, planning) depuis une table ou des fichiers de configuration, plutôt qu'un pipeline écrit à la main par source.

<!-- challenge -->

Une entreprise annonce « nous faisons du data mesh » en renommant les tables en `<domain>_*`. Que manque-t-il ?

<!-- solution -->

La propriété et la capacité dans les domaines, des garanties produit (SLA, documentation, qualité), une plateforme self-service et des standards globaux appliqués automatiquement. Renommer ne change rien à qui est responsable.

<!-- takeaways -->

- Le mesh confie la propriété aux domaines.
- Les produits de données ont propriétaires et garanties.
- Plateforme et gouvernance fédérée le rendent viable.

<!-- unit: Adopter un data mesh -->

<!-- goals -->

- Décider si le data mesh convient à une organisation.
- Commencer petit et mesurer si cela fonctionne.

<!-- concept -->

Le data mesh résout un problème d'échelle et d'organisation : les petites entreprises ou les domaines peu matures en subissent souvent les coûts sans les bénéfices. Là où il convient, mieux vaut commencer petit : un ou deux domaines motivés avec de vrais consommateurs, une plateforme minimale et des standards qui grandissent avec l'expérience.
L'interopérabilité empêche un mesh de devenir une collection de silos : identifiants, conventions et contrats partagés. Les métriques montrent si cela marche, en vitesse de livraison, adoption par les consommateurs et qualité.

<!-- example -->

| Métrique | Signal |
|---|---|
| Délai pour un nouveau produit de données | Passe de mois à semaines |
| Produits avec consommateurs actifs | En hausse |
| SLO de qualité respectés | Au-dessus de 95 % |
| Demandes à l'équipe centrale | En baisse |

#### Qu'est-ce qu'un contrat de livraison avec des fournisseurs de données externes ?

Un accord sur les formats de fichiers, le nommage, le calendrier de livraison, les signaux de complétude (manifestes ou fichiers `_SUCCESS`), l'encodage, le préavis de changement de schéma et la gestion des erreurs, qui évite la plupart des incidents d'ingestion de fichiers.

#### Qu'est-ce que la gouvernance des données ?

Le cadre de rôles, politiques, standards et processus qui garantit que les données sont exactes, sécurisées, conformes, comprises et utilisées à bon escient, incluant la responsabilité, l'intendance (stewardship), la classification, l'accès, la qualité et le cycle de vie.

#### Que sont les data owners et les data stewards ?

Les data owners rendent compte d'un domaine de données (décisions d'accès, définitions, objectifs de qualité) ; les data stewards gèrent au quotidien les définitions, les problèmes de qualité et les métadonnées, avec les ingénieurs qui mettent en œuvre les contrôles.

#### Qu'est-ce que la gestion des métadonnées ?

La collecte et la gestion des métadonnées techniques, métier et opérationnelles (schémas, définitions, lignage, qualité, usage) pour permettre la découverte, l'analyse d'impact, la gouvernance et l'automatisation ; les « métadonnées actives » s'en servent pour déclencher des actions.

<!-- challenge -->

Deux domaines publient des données clients avec des ID différents, et les joindre est impossible. Quel principe du mesh a échoué, et comment corriger ?

<!-- solution -->

La gouvernance fédérée sur l'interopérabilité : définir un identifiant client global (ou un service de correspondance) comme standard que chaque produit doit exposer, imposé par des contrôles de la plateforme.

<!-- takeaways -->

- Le mesh convient aux grandes organisations multi-domaines.
- Commencez par quelques domaines et de vrais consommateurs.
- Des identifiants globaux rendent les produits interopérables.

<!-- unit: Data fabric et métadonnées actives -->

<!-- goals -->

- Expliquer le data fabric et ce qui le distingue du data mesh.
- Utiliser les métadonnées actives pour automatiser la gouvernance.

<!-- concept -->

Le data fabric aborde le même problème d'intégration par la technologie : métadonnées riches, automatisation et virtualisation relient les données là où elles vivent, avec moins d'accent sur leur propriétaire. Le mesh demande qui est responsable ; le fabric, comment rendre les données trouvables et utilisables automatiquement. Les deux peuvent coexister.
Le fil commun, ce sont les métadonnées actives : tags et lignage qui ne se contentent pas de documenter mais agissent, en appliquant un masquage, en routant des alertes ou en recommandant des jeux de données.

<!-- example -->

```text
column customers.email tagged pii=true
  → masking policy applied automatically for non-privileged roles
  → lineage propagates the tag to downstream copies
  → quality alert routed to the owner listed in the catalog
```

#### Qu'est-ce que le lignage des données, et comment le capte-t-on ?

Le cheminement des données des sources aux consommateurs à travers les transformations. On le capte en analysant le SQL et les jobs (dbt, Unity Catalog, événements OpenLineage d'Airflow et de Spark), et on l'affiche au niveau table et colonne pour l'analyse d'impact et les audits.

#### Qu'est-ce qu'OpenLineage ?

Un standard ouvert pour les événements de lignage émis par les orchestrateurs et moteurs (Airflow, Spark, dbt, Flink), décrivant jobs, exécutions et jeux de données en entrée et en sortie, collectés par des backends comme Marquez ou des catalogues.

#### Qu'est-ce que la classification des données ?

L'étiquetage des données par sensibilité (public, interne, confidentiel, restreint) et par type (données personnelles, financières, de santé), souvent automatisé par des scanners, pour piloter les politiques d'accès, le masquage, la rétention et la conformité.

<!-- challenge -->

De nouvelles tables contenant des données personnelles apparaissent sans masquage. Comment les métadonnées actives aident-elles ?

<!-- solution -->

Classer les colonnes automatiquement (scanners ou règles de nommage) et leur poser des tags, puis lier masquage et politiques d'accès aux tags, pour que toute nouvelle colonne taguée soit protégée sans effort manuel. Propager les tags par le lignage.

<!-- takeaways -->

- Le fabric automatise l'intégration par les métadonnées.
- Le mesh est organisationnel ; le fabric technologique.
- Les métadonnées actives transforment les tags en politiques appliquées.

### Gouvernance, métadonnées et qualité

<!-- unit: Rôles, politiques et définitions -->

<!-- goals -->

- Définir rôles, politiques et maturité de la gouvernance.
- Utiliser un glossaire métier et éviter les jeux de données en double.

<!-- concept -->

La gouvernance répond à « qui décide ? » pour les données : qui peut y accéder, ce que signifient les termes, quelle qualité est acceptable. Les propriétaires sont responsables, les stewards entretiennent définitions et qualité au quotidien. Sans ces rôles, chaque question devient une réunion.
Des définitions convenues évitent l'échec le plus visible : deux rapports avec des chiffres différents pour la même métrique. Un glossaire les consigne, et des jeux certifiés et faciles à trouver empêchent les équipes de créer leurs propres copies.

<!-- example -->

| Terme | Définition | Propriétaire |
|---|---|---|
| Client actif | A passé commande dans les 90 derniers jours | Sales ops |
| Chiffre d'affaires net | Brut moins remboursements, remises et taxes | Finance |

#### Qu'est-ce que la gestion des données de référence (MDM) ?

La création d'un enregistrement unique et fiable des entités clés (client, produit, fournisseur) entre systèmes par des règles de rapprochement, de fusion et de survivance, diffusé vers les systèmes opérationnels et analytiques.

#### Que sont les données de référence (reference data) ?

Des listes de codes et classifications relativement statiques utilisées par de nombreux systèmes (codes pays, devises, codes d'activité, valeurs de statut) ; les gérer de façon centrale évite des codes incohérents.

#### Comment intégrer la qualité des données dans une architecture ?

Définir des dimensions de qualité et des SLA par produit de données, valider à l'ingestion (schémas, contrats), tester les transformations (unicité, intégrité, règles métier), bloquer la publication en cas d'échec, surveiller anomalies et fraîcheur, mettre en quarantaine les enregistrements fautifs et désigner des responsables pour résoudre les problèmes.

#### Comment mesurer la maturité de la gouvernance des données ?

Par la couverture des responsabilités, les définitions documentées, la classification des données sensibles, les politiques d'accès sous forme de code, le lignage, les SLO de qualité, les processus d'incident, et la fréquence à laquelle les consommateurs trouvent les données et leur font confiance sans avoir à demander autour d'eux.

#### Qu'est-ce qu'un glossaire métier ?

Une liste soignée de termes métier et de leurs définitions convenues (client actif, chiffre d'affaires net, churn), liés aux jeux de données et indicateurs du catalogue, qui aligne les équipes sur le sens.

<!-- challenge -->

Le marketing et la finance présentent au conseil des chiffres différents de « clients actifs ». Quelle étape de gouvernance règle cela ?

<!-- solution -->

Faire convenir aux propriétaires métier d'une définition dans le glossaire, l'implémenter une fois dans un modèle certifié, faire pointer les deux rapports dessus et nommer différemment toute variante.

<!-- takeaways -->

- La gouvernance confie les décisions aux propriétaires et stewards.
- Un glossaire fixe les définitions partagées.
- Des jeux certifiés et trouvables évitent les copies.

<!-- unit: Métadonnées et lignage -->

<!-- goals -->

- Gérer les métadonnées techniques, métier et opérationnelles.
- Capturer le lignage et classifier les données.

<!-- concept -->

Les métadonnées transforment un tas de tables en quelque chose d'utilisable : ce qui existe, ce que cela signifie, qui en est propriétaire, quelle fraîcheur et quelle origine. Le lignage, la carte des sources aux consommateurs en passant par les transformations, répond aux questions d'impact avant un changement et de cause racine après un incident.
Le lignage se capture au mieux automatiquement depuis les outils qui déplacent les données. La classification ajoute des niveaux de sensibilité, qui pilotent les politiques d'accès.

<!-- example -->

```text
crm.accounts ─► bronze.accounts ─► silver.customers ─► gold.dim_customer
                                                    └► gold.churn_features ─► churn model
change silver.customers.segment → impact: 2 gold tables, 1 model, 4 dashboards
```

#### Comment éviter les jeux de données en double ?

Rendre découvrables les jeux existants (catalogue, recherche), certifier ceux qui font autorité, exiger un responsable et une revue pour tout nouveau jeu publié, surveiller l'usage et déprécier les copies.

#### Quelles sont les couches de la sécurité des données ?

La gestion des identités et des accès (authentification, autorisation au moindre privilège), l'isolement réseau, le chiffrement au repos et en transit, la gestion des clés, le masquage et la tokenisation, la sécurité au niveau ligne et colonne, l'audit et la supervision, et des pratiques de développement sécurisé.

#### Quelle différence entre RBAC et ABAC ?

Le contrôle d'accès par rôles accorde des droits à des rôles attribués aux utilisateurs ; le contrôle par attributs évalue dans les politiques des attributs des utilisateurs, des ressources et du contexte (département, classification, localisation), ce qui passe mieux à l'échelle pour des règles fines (par exemple les politiques par tags).

#### Quelle différence entre pseudonymisation et anonymisation ?

La pseudonymisation remplace les identifiants par des jetons ou des hachages qu'on peut relier à nouveau avec des informations supplémentaires (ce sont toujours des données personnelles au sens du RGPD) ; l'anonymisation empêche de façon irréversible l'identification (ce ne sont plus des données personnelles), ce qui est difficile à obtenir en pratique.

<!-- challenge -->

Avant de supprimer une colonne en silver, un ingénieur demande ce qui pourrait casser. Comment l'architecture répond-elle ?

<!-- solution -->

Le lignage au niveau colonne dans le catalogue (capturé automatiquement via OpenLineage ou l'analyse des requêtes) liste les tables, modèles et tableaux de bord en aval qui l'utilisent, avec les propriétaires à prévenir.

<!-- takeaways -->

- Les métadonnées rendent les données trouvables et compréhensibles.
- Le lignage répond aux questions d'impact et de cause racine.
- La classification pilote accès et protection.

<!-- unit: Données de référence et qualité -->

<!-- goals -->

- Gérer les données maîtres et de référence.
- Intégrer la qualité des données à l'architecture.

<!-- concept -->

Les entités clés comme client et produit apparaissent dans de nombreux systèmes, chacun avec sa version. La gestion des données maîtres crée un enregistrement de confiance et y rattache les autres ; les données de référence, comme les codes pays ou devises, ont besoin de la même source unique.
La qualité fonctionne de la même façon à chaque couche : définir ce qui est « bon » par produit de données, valider tôt à l'ingestion, tester les transformations, surveiller les sorties et mettre en quarantaine ce qui échoue plutôt que de le publier.

<!-- example -->

| Couche | Contrôle qualité |
|---|---|
| Ingestion | Validation du schéma et du contrat |
| Silver | Unicité, nulls, intégrité référentielle |
| Gold | Règles métier, rapprochement avec les totaux source |
| Supervision | Fraîcheur, volume, changements de distribution |

#### Qu'est-ce que la tokenisation ?

Le remplacement de valeurs sensibles (numéros de carte, identifiants nationaux) par des jetons non sensibles, la correspondance étant conservée dans un coffre sécurisé, pour que la plupart des systèmes ne manipulent jamais les vraies valeurs.

#### Comment le RGPD affecte-t-il l'architecture des données ?

Il exige une base légale et la limitation des finalités, la minimisation des données, des durées de conservation limitées, la sécurité, des registres de traitement et la prise en charge des droits des personnes (accès, rectification, effacement), ce qui suppose de savoir où se trouvent les données personnelles (lignage, catalogue) et de pouvoir les supprimer dans toutes les couches.

#### Comment mettre en œuvre le droit à l'effacement dans un lakehouse ?

Savoir où se trouvent les données de chaque personne, utiliser des formats de table qui prennent en charge les suppressions (Delta, Iceberg), supprimer dans toutes les couches, faire un vacuum des anciens fichiers après la rétention, éviter de propager largement les identifiants bruts (pseudonymiser tôt), et documenter le processus et ses délais.

<!-- challenge -->

Le même client apparaît trois fois avec des noms légèrement différents dans le CRM, la facturation et le support. Comment donner un seul client à l'analytique ?

<!-- solution -->

Créer un client maître avec des règles de rapprochement (ou du matching par ML) entre sources, attribuer un ID de référence, garder une table de correspondance vers les ID source et construire `dim_customer` à partir de l'enregistrement maître.

<!-- takeaways -->

- Le MDM crée un enregistrement de confiance par entité.
- Les données de référence exigent une source unique.
- Validez à chaque couche ; mettez les échecs en quarantaine.

### Sécurité et conformité

<!-- unit: Accès et protection -->

<!-- goals -->

- Superposer les couches de sécurité, de l'identité à la supervision.
- Choisir entre RBAC et ABAC et appliquer le zero trust.

<!-- concept -->

La sécurité des données fonctionne par couches, pour qu'une défaillance n'expose pas tout : identité et moindre privilège, isolation réseau, chiffrement, accès fin aux lignes et colonnes, gestion des secrets et supervision. Chaque couche suppose que les autres peuvent céder.
Quand les plateformes grandissent, le contrôle par rôles devient une jungle. Le contrôle par attributs accorde l'accès selon des tags et des attributs utilisateur, et passe mieux à l'échelle. Le zero trust cesse de considérer l'emplacement réseau comme une raison de faire confiance.

<!-- example -->

```text
RBAC: role finance_analyst → SELECT on finance.*
ABAC: allow SELECT where table.domain IN user.domains
      AND (column.pii = false OR user.clearance = 'pii')
```

#### Qu'est-ce que la résidence des données ?

Des exigences imposant que certaines données soient stockées et traitées dans des juridictions précises, ce qui influe sur le choix des régions, la réplication, l'emplacement des sauvegardes et les services utilisables.

#### Qu'est-ce que le zero trust appliqué aux plateformes de données ?

Ne jamais accorder de confiance sur la base de l'emplacement réseau : chaque accès est authentifié, autorisé au moindre privilège et audité, avec des identifiants de courte durée, des identités de charge de travail et une vérification continue.

#### Comment gérer les secrets dans les plateformes de données ?

Les stocker dans un gestionnaire de secrets (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault, secret scopes Databricks), préférer les identités de charge de travail et les identifiants de courte durée aux clés statiques, les faire tourner automatiquement et ne jamais les committer dans Git.

#### Qu'est-ce que la prévention des fuites de données (DLP) ?

Des outils et politiques qui détectent et bloquent la sortie de données sensibles hors des périmètres autorisés (e-mails, exports, buckets publics), souvent en recherchant des motifs comme des numéros de carte ou d'identité.

#### Comment partager des données avec des partenaires externes en sécurité ?

Partager des jeux curés et minimaux via des mécanismes gouvernés (Delta Sharing, shares Snowflake, accès présignés avec expiration) plutôt que des exports de fichiers, appliquer des restrictions de lignes et de colonnes, encadrer l'usage par contrat et auditer les accès.

<!-- challenge -->

L'entrepôt compte 400 rôles, souvent redondants, et les revues d'accès prennent des semaines. Que proposez-vous ?

<!-- solution -->

Passer au contrôle par attributs : taguer tables et colonnes (domaine, sensibilité), donner des attributs aux utilisateurs (équipe, habilitation) et écrire quelques politiques sur les tags. Garder un petit ensemble de rôles fonctionnels.

<!-- takeaways -->

- Superposez identité, réseau, chiffrement, accès et supervision.
- L'ABAC passe mieux à l'échelle que des centaines de rôles.
- Le zero trust authentifie chaque accès.

<!-- unit: Confidentialité et conformité -->

<!-- goals -->

- Appliquer pseudonymisation, anonymisation et tokenisation.
- Concevoir pour le RGPD, l'effacement, la résidence et le partage sécurisé.

<!-- concept -->

Le droit de la vie privée façonne l'architecture. Collecter seulement le nécessaire, le conserver seulement le temps nécessaire, et savoir où vivent les données de chaque personne. La pseudonymisation réduit l'exposition mais reste une donnée personnelle ; seule une vraie anonymisation échappe à la réglementation, et elle est plus difficile qu'il n'y paraît.
Des droits comme l'effacement exigent un support technique : formats de table capables de supprimer des lignes, carte de l'emplacement des identifiants et processus qui nettoient aussi sauvegardes et copies. Résidence et partage externe ajoutent des règles sur la destination des données.

<!-- example -->

```sql
-- erasure request on a lakehouse (Delta/Iceberg)
DELETE FROM silver.customers WHERE customer_id = 552;
DELETE FROM silver.orders    WHERE customer_id = 552;
-- then remove old file versions after retention
VACUUM silver.customers; VACUUM silver.orders;
```

#### Que sont les SLA, SLO et SLI pour les données ?

Les SLI sont des indicateurs mesurés (fraîcheur, complétude, taux de réussite des pipelines) ; les SLO sont des objectifs sur ces indicateurs (données prêtes à 7 h 99 % des jours) ; les SLA sont des engagements envers les consommateurs avec des conséquences. Ils rendent la fiabilité des données mesurable.

#### Qu'est-ce que l'observabilité des données ?

La supervision de la fraîcheur, du volume, du schéma, de la distribution et du lignage des données (pas seulement de l'état des jobs) pour détecter vite les incidents et en trouver la cause, souvent avec une détection automatique d'anomalies.

#### Comment concevoir des pipelines qui supportent les pannes ?

En partant du principe qu'il y aura des pannes : étapes idempotentes et relançables, relances avec backoff pour les erreurs transitoires, checkpoints pour les flux, files dead-letter pour les enregistrements invalides, alertes avec runbooks, et capacité à faire un backfill de périodes précises.

#### Qu'est-ce qu'une file dead-letter ?

Un endroit où sont envoyés, avec les informations d'erreur, les messages ou enregistrements impossibles à traiter (format invalide, validation échouée), pour que le pipeline continue et que les échecs puissent être examinés et rejoués plus tard.

#### Que sont le RPO et le RTO ?

Recovery point objective : la perte de données acceptable (temps entre le dernier état récupérable et la panne). Recovery time objective : la durée acceptable de la reprise. Ils déterminent la fréquence des sauvegardes, la réplication et la conception de la reprise après sinistre.

#### Qu'est-ce que le FinOps pour les plateformes de données ?

La pratique collaborative de gestion des coûts data dans le cloud : visibilité (tags, coût par pipeline et par équipe), optimisation (dimensionnement, arrêt automatique, niveaux de stockage, optimisation des requêtes, traitement incrémental) et gouvernance (budgets, alertes, responsabilisation).

<!-- challenge -->

Les tables analytiques stockent les e-mails des clients à 40 endroits. Chaque demande d'effacement prend une semaine. Comment repenser l'architecture ?

<!-- solution -->

Pseudonymiser tôt : remplacer les e-mails par un jeton en silver, garder la correspondance dans une seule table protégée et laisser les tables en aval utiliser le jeton. L'effacement supprime alors la correspondance et les quelques sources brutes, rendant les jetons impossibles à relier.

<!-- takeaways -->

- Les données pseudonymisées restent des données personnelles.
- L'effacement exige des formats supprimables et une carte des identifiants.
- Résidence et partage contraignent les flux de données.

<!-- stage: Exploiter et faire évoluer -->

### Fiabilité, exploitation et coûts

<!-- unit: Niveaux de service et observabilité -->

<!-- goals -->

- Définir SLI, SLO et SLA pour les produits de données.
- Surveiller les données par l'observabilité et gérer les incidents.

<!-- concept -->

Les utilisateurs se moquent de savoir si un job a réussi ; ce qui compte, c'est que les données soient fraîches, complètes et justes. Les niveaux de service rendent cela mesurable : des indicateurs comme la fraîcheur, des objectifs chiffrés et des engagements promis aux consommateurs.
L'observabilité des données surveille les données elles-mêmes et détecte les défaillances silencieuses que des jobs au vert masquent. Quand quelque chose tourne mal, la gestion d'incidents, avec sévérité, communication et postmortems, traite les données comme tout service de production.

<!-- example -->

| SLI | SLO |
|---|---|
| Fraîcheur de `gold.revenue` | Mise à jour avant 07:00 99 % des jours |
| Complétude | Nombre de lignes à ±5 % de la moyenne sur 7 jours |
| Succès du pipeline | 99,5 % des exécutions quotidiennes |

#### Quels sont les principaux postes de coût des plateformes de données ?

Le calcul des transformations et des requêtes (surtout les clusters toujours allumés et les recalculs complets), les requêtes inefficaces sur de gros volumes, la duplication des données entre couches et outils, les sorties de données et transferts inter-régions, et les données inutilisées conservées indéfiniment.

#### Comment rendre une plateforme économe dès sa conception ?

Traitement incrémental, partitionnement et clustering pour l'élagage, calcul serverless ou en autoscaling avec arrêt automatique, stockage hiérarchisé et rétention, absence de copies inutiles, latence adaptée au besoin métier, et visibilité des coûts par équipe.

#### Quel est le rôle de l'infrastructure as code dans l'architecture des données ?

Définir les plateformes (stockage, calcul, droits, catalogues, jobs) de façon déclarative dans du code (Terraform, CloudFormation, Bicep, bundles) pour que les environnements soient reproductibles, relus et auditables, et que les dérives soient détectables.

#### Qu'est-ce qu'un incident de données, et comment le gérer ?

Tout événement où les données sont fausses, en retard ou indisponibles pour les consommateurs. On le gère comme un incident logiciel : détecter, évaluer l'impact, informer les consommateurs, atténuer (suspendre la publication, revenir en arrière), corriger la cause racine et rédiger un post-mortem sans recherche de coupable, avec des actions.

<!-- challenge -->

Tous les jobs sont au vert, pourtant un tableau de bord a affiché zéro vente pour une région toute la matinée. Quel contrôle d'observabilité l'aurait détecté ?

<!-- solution -->

Un contrôle de volume ou de distribution sur la sortie (lignes par région comparées à l'historique), qui alerte quand un segment tombe à zéro, quel que soit le statut du job.

<!-- takeaways -->

- Mesurez ce que ressentent les utilisateurs : fraîcheur, complétude, justesse.
- L'observabilité surveille les données, pas seulement les jobs.
- Traitez les incidents data comme des incidents logiciels.

<!-- unit: Concevoir pour la panne -->

<!-- goals -->

- Concevoir des pipelines qui échouent proprement et se rétablissent.
- Utiliser dead-letter queues, IaC et planification de capacité.

<!-- concept -->

Les pannes arriveront ; la conception décide si elles sont de la routine ou des crises. Des étapes idempotentes et redémarrables se relancent simplement. Les enregistrements défectueux vont dans une dead-letter queue au lieu de tout arrêter. L'infrastructure en code peut être recréée. La planification de capacité évite que la croissance tourne à la panne.
L'objectif : qu'aucun fichier, nœud ou déploiement défectueux ne fasse tomber la plateforme ou perdre des données.

<!-- example -->

```text
stream ─► parse/validate ─┬─► valid  ─► silver
                          └─► invalid ─► dead-letter topic (with error, source, offset)
                                         └─► alert + reprocess after fix
```

#### Qu'est-ce que la planification de capacité pour les plateformes de données ?

Prévoir la croissance des volumes, des utilisateurs et des charges pour que stockage, calcul et concurrence restent suffisants et que les budgets soient prêts, à partir des tendances de supervision et des plans métier.

#### Comment définir l'architecture des politiques de rétention ?

Classer les jeux de données selon les besoins légaux et métier, définir la rétention par couche (le raw peut être gardé plus longtemps pour le retraitement, ou moins pour la confidentialité), la mettre en œuvre par des règles de cycle de vie, la suppression de partitions et la rétention du format de table, et documenter les exceptions.

#### De quoi une plateforme de ML a-t-elle besoin côté architecture des données ?

De données d'entraînement fiables et versionnées, de features exactes à la date (point-in-time), de la réutilisation des features entre entraînement et service, d'un lignage des données aux modèles, du suivi des expériences, d'un registre de modèles et de la surveillance de la dérive des données et des prédictions.

#### Qu'est-ce qu'un feature store ?

Un système qui stocke, documente et sert les features de ML de façon cohérente pour l'entraînement (offline, historique, exact à la date) et l'inférence (online, faible latence), évitant l'écart entre entraînement et service et l'ingénierie de features dupliquée.

<!-- challenge -->

Un seul enregistrement mal formé dans un fichier quotidien fait échouer tout le chargement et bloque tous les rapports. Comment le repenser ?

<!-- solution -->

Valider par enregistrement : envoyer les lignes invalides vers une table de quarantaine ou un emplacement dead-letter avec l'erreur, charger les lignes valides et alerter si les invalides dépassent un seuil. Retraiter la quarantaine après correction.

<!-- takeaways -->

- Des étapes idempotentes et redémarrables sécurisent les relances.
- Les dead-letter queues isolent les enregistrements défectueux.
- IaC et planification de capacité évitent les pannes auto-infligées.

<!-- unit: Coût et rétention -->

<!-- goals -->

- Identifier les leviers de coût et concevoir des plateformes économes.
- Appliquer le FinOps et des politiques de rétention.

<!-- concept -->

Les plateformes de données dépensent surtout en calcul : clusters toujours allumés, recalculs complets et requêtes inefficaces. Le stockage est bon marché à l'octet mais grandit sans fin si la rétention ne dit pas le contraire. Les conceptions économes traitent en incrémental, élaguent par partitionnement, descendent à zéro au repos et ne gardent les données que tant qu'elles servent ou que la loi l'exige.
Le FinOps rend le coût visible aux équipes qui le génèrent, pour que l'efficacité devienne une habitude partagée plutôt qu'un nettoyage annuel.

<!-- example -->

| Couche | Rétention |
|---|---|
| Fichiers d'atterrissage | 30 jours après traitement |
| Bronze | 7 ans (légal), stockage froid après 1 an |
| Agrégats gold | Tant qu'ils servent |
| Bac à sable | 30 jours, suppression automatique |

#### Qu'est-ce que l'exactitude à la date (point-in-time correctness) ?

Lors de la construction des données d'entraînement, les features ne doivent utiliser que l'information disponible au moment de l'événement de chaque étiquette, pour éviter la fuite de données futures ; les feature stores joignent les features à la date de chaque événement.

#### Qu'est-ce que l'écart entre entraînement et service (training-serving skew) ?

Des différences dans le calcul des features pour l'entraînement et pour l'inférence (code, sources ou moment différents), qui dégradent les performances du modèle en production. Des définitions de features partagées et les feature stores le réduisent.

#### Qu'est-ce qu'une base vectorielle, et où se situe-t-elle ?

Un stockage optimisé pour la recherche par similarité sur des embeddings (pgvector, OpenSearch, Pinecone, Weaviate, Databricks Vector Search), utilisé pour la recherche sémantique, les recommandations et la génération augmentée par récupération.

#### Quelle est l'architecture de données d'une application RAG ?

Ingérer des documents, les découper en fragments, calculer des embeddings, les stocker avec leurs métadonnées dans un index vectoriel, récupérer les fragments pertinents à la requête (souvent combinés à une recherche par mots-clés et à des filtres de droits) et les transmettre à un LLM, avec des pipelines qui maintiennent l'index frais et gouverné.

<!-- challenge -->

Les coûts cloud ont crû de 60 % en un an, surtout à cause de quelques pipelines qui reconstruisent des tables entières chaque nuit. Que changez-vous ?

<!-- solution -->

Les rendre incrémentaux (ne traiter que les partitions nouvelles ou modifiées avec `MERGE`), ajouter l'élagage de partitions, redimensionner ou autoscaler le calcul, et montrer à chaque équipe son coût par produit de données.

<!-- takeaways -->

- Le calcul domine le coût ; l'incrémental bat la reconstruction.
- Concevez pour l'élagage et le passage à zéro.
- Les politiques de rétention maîtrisent la croissance du stockage.

### Architecture des données pour l'IA et le ML

<!-- unit: Des données pour le machine learning -->

<!-- goals -->

- Décrire les besoins des plateformes ML : features, données point-in-time et MLOps.
- Prévenir le training-serving skew et surveiller la dérive.

<!-- concept -->

Les modèles ne valent que leurs données d'entraînement, et le ML ajoute des exigences que la BI n'a pas. Les jeux d'entraînement ne doivent utiliser que l'information disponible au moment de la prédiction, sinon les modèles brillent en test et échouent en production. Les features doivent être calculées de la même façon pour l'entraînement et le service.
Un feature store répond aux deux, et le MLOps encadre le cycle de vie : données et modèles versionnés, réentraînement automatisé et surveillance de la dérive des entrées ou des relations.

<!-- example -->

```text
label: churned on 2026-06-01
features must come from data known on 2026-05-31:
  orders_last_90d   ✔ computed from orders before 2026-05-31
  support_tickets   ✘ includes the cancellation ticket of 2026-06-02 → leakage
```

#### Comment les enjeux de gouvernance changent-ils avec l'IA ?

Il faut tracer quelles données ont entraîné quels modèles, respecter les droits lors de la récupération (un utilisateur ne doit pas voir via un LLM des documents auxquels il n'aurait pas accès directement), gérer les données personnelles dans les prompts et les données d'entraînement, et évaluer les réponses ; les catalogues gouvernent de plus en plus modèles et features aux côtés des tables.

#### Qu'est-ce que le MLOps ?

Des pratiques et outils pour développer, déployer et exploiter des modèles de ML de façon fiable : données et code versionnés, pipelines d'entraînement reproductibles, registre de modèles, tests et déploiements automatisés, supervision des performances et de la dérive, et réentraînement.

#### Quelle différence entre dérive des données et dérive de concept ?

La dérive des données est un changement de la distribution des entrées (l'âge des clients évolue) ; la dérive de concept est un changement de la relation entre entrées et cible (ce qui prédit le churn change). Les deux exigent une supervision et éventuellement un réentraînement.

#### Comment gérer les données non structurées pour l'IA ?

Les stocker en stockage objet avec leurs métadonnées dans un catalogue (volumes), tracer le lignage des documents vers les fragments et les embeddings, appliquer contrôles d'accès et classification, et construire des pipelines qui mettent à jour les index quand les documents changent ou sont supprimés.

#### À quoi ressemble une architecture de données typique sur AWS ?

Des sources ingérées avec DMS, Kinesis/MSK, AppFlow ou Glue vers S3 ; Glue Data Catalog et Lake Formation pour la gouvernance ; traitement avec Glue, EMR ou Databricks ; tables Iceberg ou Delta ; Athena et Redshift pour le SQL ; QuickSight pour la BI ; SageMaker pour le ML ; Step Functions, MWAA ou EventBridge pour l'orchestration ; le tout défini avec CloudFormation, CDK ou Terraform.

#### À quoi ressemble une architecture de données typique sur Azure ?

Ingestion avec Data Factory ou les pipelines Fabric et Event Hubs vers ADLS Gen2/OneLake ; traitement avec Databricks ou Spark de Fabric ; tables Delta ; entrepôts Synapse/Fabric ou Databricks SQL ; Power BI ; Purview pour la gouvernance ; Entra ID pour l'identité.

<!-- challenge -->

Un modèle de churn affiche 97 % de précision en test et 70 % en production. Que soupçonnez-vous d'abord ?

<!-- solution -->

Une fuite due à des données d'entraînement non correctes dans le temps (features utilisant une information postérieure à la date de prédiction), ou un training-serving skew dans le calcul des features. Reconstruire le jeu d'entraînement avec des jointures point-in-time et comparer les valeurs des features.

<!-- takeaways -->

- Les données d'entraînement doivent être correctes dans le temps.
- Calculez les features une fois pour l'entraînement et le service.
- Surveillez la dérive des données et des concepts.

<!-- unit: Des données pour l'IA générative -->

<!-- goals -->

- Situer bases vectorielles et pipelines RAG dans l'architecture.
- Gouverner les données non structurées utilisées par l'IA.

<!-- concept -->

Les applications d'IA générative récupèrent des documents pertinents et les transmettent à un modèle. Cela fait des fichiers non structurés des produits de données : ils exigent ingestion, découpage, embeddings, métadonnées et un index vectoriel synchronisé avec la source.
La gouvernance suit les données. Un système de recherche doit respecter les mêmes permissions que les documents, et les équipes doivent savoir quelles données ont alimenté quel modèle ou quelle réponse.

<!-- example -->

```text
docs (S3 / SharePoint) ─► parse + chunk ─► embeddings ─► vector index (with ACL metadata)
user question ─► retrieve top-k allowed chunks ─► LLM ─► answer with sources
lineage: answer → chunks → documents → owners
```

#### À quoi ressemble une architecture de données typique sur Google Cloud ?

Ingestion avec Pub/Sub, Datastream (CDC) et Dataflow vers Cloud Storage et BigQuery ; traitement avec Dataflow, Dataproc ou le SQL BigQuery (souvent avec dbt ou Dataform) ; Dataplex pour la gouvernance ; Looker pour la BI ; Vertex AI pour le ML.

#### Qu'est-ce que le multi-cloud, et quand en vaut-il la peine ?

L'usage de plusieurs fournisseurs cloud. Il peut réduire la dépendance, répondre à des exigences clients ou réglementaires, ou tirer parti des meilleurs services de chacun, mais il multiplie compétences, outillage, réseau et coûts de sortie. La plupart des organisations gagnent davantage avec un cloud principal et des formats portables.

#### Qu'est-ce qu'une architecture hybride ?

La combinaison de systèmes on-premise et de services cloud, courante pendant les migrations ou pour les données réglementées ; elle exige une connectivité sécurisée (VPN, Direct Connect, ExpressRoute), une identité et une gouvernance cohérentes et des mouvements de données maîtrisés.

#### Quelles stratégies de migration existe-t-il pour les plateformes de données ?

Rehost (lift and shift), replatform (passer à des équivalents gérés avec peu de changements), refactor (repenser pour des services cloud natifs et l'ELT), retirer les actifs inutilisés et conserver ce qui doit rester. Les migrations de données les combinent généralement, par vagues et par domaine avec une validation en parallèle.

<!-- challenge -->

Un assistant interne répond aux questions des employés à partir des documents de l'entreprise, et quelqu'un obtient une réponse citant des fichiers RH qu'il ne peut pas ouvrir. Qu'est-ce qui n'allait pas ?

<!-- solution -->

La recherche ignorait les permissions des documents. Stocker des métadonnées de contrôle d'accès avec chaque chunk et filtrer la recherche selon l'identité de l'utilisateur, pour que le modèle ne voie que les chunks lisibles par celui-ci.

<!-- takeaways -->

- Le RAG fait des documents des produits de données gouvernés.
- Gardez les index vectoriels synchronisés avec les sources.
- La recherche doit appliquer les permissions des sources.

### Cloud et architectures de référence

<!-- unit: Architectures de référence -->

<!-- goals -->

- Esquisser des architectures de données types sur AWS, Azure et Google Cloud.
- Faire correspondre les services équivalents entre clouds.

<!-- concept -->

Les trois grands clouds offrent les mêmes briques sous des noms différents : services d'ingestion, stockage objet, catalogue, moteurs de traitement, entrepôt et BI. Connaître le motif compte plus que la liste des produits, car la forme se répète : déposer les données dans le stockage objet ou un entrepôt, les cataloguer et les gouverner, les transformer, les restituer.
Les différences tiennent à la profondeur d'intégration et aux choix par défaut, comme le degré de fusion entre entrepôt et lac.

<!-- example -->

| Couche | AWS | Azure | Google Cloud |
|---|---|---|---|
| Ingestion | DMS, Kinesis, Glue | Data Factory, Event Hubs | Datastream, Pub/Sub |
| Stockage | S3 | ADLS / OneLake | Cloud Storage |
| Catalogue | Glue + Lake Formation | Purview / Unity | Dataplex |
| Entrepôt | Redshift | Fabric / Synapse | BigQuery |

#### Qu'est-ce qu'une landing zone dans l'architecture cloud ?

Un environnement multi-comptes (ou multi-abonnements) préconfiguré et sécurisé, avec identité, réseau, journalisation, garde-fous de sécurité et structure de comptes, sur lequel les plateformes de données sont déployées de manière cohérente.

#### Comment organiser les comptes ou projets d'une plateforme de données ?

Séparer les environnements (dev, staging, prod) et souvent les domaines dans des comptes ou projets distincts pour limiter l'impact des incidents, voir les coûts et appliquer le moindre privilège, les services partagés (catalogue, réseau, journalisation) étant gérés de façon centrale.

#### Concevez une plateforme de données pour une entreprise de e-commerce de taille moyenne.

Ingérer la base des commandes en CDC, les événements web via un flux (Kafka ou Kinesis) et les outils SaaS (CRM, marketing) avec des connecteurs vers le stockage objet ; organiser des couches médaillon avec des tables Iceberg ou Delta dans un catalogue ; transformer avec dbt ou Spark en dimensions conformes et en faits ; servir la BI depuis un entrepôt ou un moteur SQL de lakehouse avec une couche sémantique ; ajouter du reverse ETL pour les segments marketing ; orchestrer avec Airflow ou des jobs natifs ; appliquer gouvernance, tests de qualité, observabilité et tags de coût ; tout définir sous forme de code avec CI/CD.

<!-- challenge -->

Un recruteur vous demande de concevoir sur un cloud que vous n'avez jamais utilisé. Comment répondre de façon convaincante ?

<!-- solution -->

Décrire d'abord les couches et les exigences (ingestion, stockage, catalogue, traitement, restitution, gouvernance), puis associer chacune au service équivalent de ce cloud, en précisant où vous vérifieriez les détails. Le motif montre le jugement plus que les noms de produits.

<!-- takeaways -->

- Tous les clouds offrent les mêmes couches.
- Apprenez le motif, puis associez les services.
- La profondeur d'intégration varie selon le cloud.

<!-- unit: Multi-cloud, hybride et migration -->

<!-- goals -->

- Décider quand le multi-cloud ou l'hybride en valent la peine.
- Planifier les migrations et organiser les comptes cloud d'une plateforme data.

<!-- concept -->

Le multi-cloud évoque la liberté mais double compétences, outillage et travail d'intégration ; il se justifie pour des raisons précises comme la réglementation, les acquisitions ou les exigences clients. Les configurations hybrides sont courantes pendant les migrations et pour les systèmes qui doivent rester sur site.
Les migrations suivent le spectre connu, du rehosting à la reconstruction. En dessous, une landing zone avec des comptes séparés par environnement et par domaine pose dès le premier jour des frontières de sécurité et de coût.

<!-- example -->

```text
organization
 ├─ security (logs, audit)
 ├─ shared-network
 ├─ data-dev / data-staging / data-prod
 └─ domain-payments-prod, domain-marketing-prod (mesh-style)
```

#### Une entreprise a dix départements qui construisent chacun leurs rapports avec des chiffres contradictoires. Que proposez-vous ?

Identifier les processus métier et indicateurs clés, créer des dimensions conformes et des faits certifiés portés par des équipes responsables, mettre en place une couche sémantique pour les définitions d'indicateurs, établir responsabilité et intendance des données, retirer progressivement la logique dupliquée, et communiquer un catalogue de jeux de données certifiés.

#### Vous devez ajouter un scoring de fraude en temps réel à une plateforme orientée batch. Comment ?

Diffuser les transactions depuis la source (CDC ou événements) vers un broker, calculer les features avec un moteur de flux en s'appuyant sur un feature store online (définitions partagées avec l'entraînement batch), appeler le modèle pour un scoring en millisecondes, réécrire les décisions sous forme d'événements, et tout déposer dans le lakehouse pour l'analyse et le réentraînement.

#### Les équipes microservices se plaignent que l'équipe data casse dès qu'elles modifient leurs bases. Que changez-vous ?

Arrêter de lire directement les tables internes : convenir de contrats de données, faire publier par les services des événements d'intégration (via une outbox) ou des vues CDC curées, valider les contrats dans la CI des services, versionner les changements cassants et confier aux domaines la responsabilité de leurs produits de données publiés.

#### Votre data lake est devenu un marécage. Comment le récupérer ?

Inventorier les jeux de données avec leur usage et leurs responsables, définir des zones et des règles de nommage, enregistrer les données utiles dans un catalogue avec descriptions et tags, ajouter des contrôles de qualité, convertir les jeux clés en formats de table, archiver ou supprimer les données inutilisées par des politiques de cycle de vie, et rendre la responsabilité obligatoire pour tout nouveau jeu de données.

#### Comment expliquer l'architecture des données à un interlocuteur non technique ?

C'est le plan d'urbanisme des données de l'entreprise : d'où viennent les données, où elles sont stockées, comment elles circulent et sont nettoyées, qui en est responsable et quelles règles les gardent sûres et fiables, pour que les équipes puissent construire dessus sans chaos.

<!-- challenge -->

La direction veut exécuter chaque charge sur deux clouds « pour éviter la dépendance ». Que conseillez-vous ?

<!-- solution -->

Expliquer le coût : compétences, outillage et intégration en double, et services au plus petit dénominateur commun. Limiter plutôt la dépendance avec formats ouverts et outils portables, et n'utiliser un second cloud que là où une exigence concrète le justifie.

<!-- takeaways -->

- Le multi-cloud a de vrais coûts ; réservez-le à des raisons concrètes.
- L'hybride est courant pendant les migrations.
- Une landing zone fixe tôt les frontières des comptes.

<!-- stage: Tout assembler -->

### Mises en situation

<!-- unit: Concevoir une plateforme de zéro -->

<!-- goals -->

- Concevoir une plateforme de données de bout en bout pour une entreprise donnée.
- Adapter la conception à la taille et à la maturité de l'entreprise.

<!-- concept -->

Les questions de conception testent le jugement, pas des listes d'outils. Une bonne réponse part des questions métier et des contraintes, puis parcourt les couches : comment chaque source est ingérée, où et dans quels formats les données sont stockées, comment elles sont modélisées, restituées, gouvernées, sécurisées et surveillées. Elle adapte ensuite la conception à l'entreprise : une startup a besoin de simplicité managée, une entreprise moyenne de structure, et toutes deux d'un chemin pour grandir.

<!-- example -->

| Couche | Startup | E-commerce de taille moyenne |
|---|---|---|
| Ingestion | Connecteurs managés | CDC, flux d'événements, connecteurs |
| Stockage | Entrepôt cloud | Lakehouse ou entrepôt + lac |
| Modélisation | dbt, quelques marts | Médaillon + marts dimensionnels |
| Gouvernance | Rôles de base, doc | Catalogue, propriétaires, classification |

#### Une startup vous demande de concevoir sa première plateforme de données. Que recommandez-vous ?

La garder simple et gérée : un service d'entrepôt ou de lakehouse cloud, des connecteurs gérés pour les sources SaaS, du CDC ou des réplicas pour la base du produit, dbt pour les transformations avec des tests, un seul orchestrateur, un outil BI avec une couche sémantique, une gouvernance de base et des alertes de coût, le tout sous forme de code. N'ajouter streaming, mesh ou composants maison que quand le besoin apparaît.

#### Votre entreprise en a racheté une autre avec un cloud et une plateforme différents. Comment intégrer les données ?

Partir des questions auxquelles la direction doit répondre, cartographier les entités et indicateurs clés, répliquer les données nécessaires dans la plateforme principale par CDC ou exports (ou les partager via des formats ouverts), construire des dimensions conformes avec rapprochement des données de référence, et planifier à plus long terme la consolidation des plateformes selon les coûts et les capacités.

<!-- challenge -->

La startup de votre conception double chaque année. Que changeriez-vous la troisième année, et que garderiez-vous ?

<!-- solution -->

Garder l'entrepôt, dbt et les connecteurs managés. Ajouter un catalogue avec propriétaires, des contrats de données avec les équipes produit, du CDC pour la base principale, un suivi des coûts, et éventuellement un lac pour les données brutes et le ML à mesure que les volumes croissent.

<!-- takeaways -->

- Partez des questions et contraintes, puis parcourez les couches.
- Adaptez la conception à la taille et à la maturité.
- Laissez un chemin pour grandir sans tout reconstruire.

<!-- unit: Intégrer après une acquisition -->

<!-- goals -->

- Planifier l'intégration des données entre les plateformes de deux entreprises.
- Privilégier les questions métier sur la consolidation des plateformes.

<!-- concept -->

Après une acquisition, la direction veut des chiffres consolidés bien avant que les plateformes puissent fusionner. La voie pratique : partir des questions auxquelles il faut répondre, faire correspondre les entités et métriques clés entre les entreprises, et répliquer les données nécessaires dans une seule plateforme. La consolidation des plateformes vient plus tard, une fois les définitions alignées et les résultats visibles pour le métier.

<!-- example -->

```text
week 1–4:  agree on 10 key metrics and their definitions; map customer, product, revenue
week 4–8:  replicate needed tables from company B into A's platform; build combined marts
month 3+:  plan migration of B's pipelines; retire duplicate tools
```

#### La direction veut « tout en temps réel ». Comment répondez-vous ?

Demander quelles décisions changent avec des données plus fraîches et quelle latence chacune exige, estimer coûts et complexité de chaque niveau (secondes, minutes, heures), livrer du temps réel là où la valeur métier le justifie, et garder le reste en batch ou micro-batch, moins coûteux.

<!-- challenge -->

Les deux entreprises définissent « client » différemment : l'une compte des comptes, l'autre des personnes. Comment produire un nombre de clients consolidé ?

<!-- solution -->

Convenir d'une définition avec les propriétaires métier (ou publier les deux clairement libellées), y rattacher les enregistrements de chaque entreprise via une table de correspondance de clés, et documenter la règle dans le glossaire avant de publier les chiffres consolidés.

<!-- takeaways -->

- Partez des questions auxquelles la direction doit répondre.
- Faites correspondre entités et métriques avant de déplacer les plateformes.
- Consolidez les plateformes une fois les définitions alignées.
