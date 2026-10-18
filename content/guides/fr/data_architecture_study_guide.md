## Fiche d'étude Architecture des données

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude architecture des données : environ 200 questions](../../images/data_architecture_study_guide_title_img.png)

Environ 200 questions d'entretien sur l'architecture des données : principes, choix de stockage et de bases de données, compromis des systèmes distribués, approches de modélisation (Inmon, Kimball, Data Vault), lakes, lakehouses et architecture médaillon, architectures batch et streaming (Lambda, Kappa), microservices et données événementielles, data mesh et data fabric, gouvernance, sécurité, fiabilité, coûts et architecture pour l'IA. Elle complète la fiche data warehousing, qui approfondit la modélisation dimensionnelle. Ouvrez une question pour voir sa réponse, ou utilisez le filtre pour chercher dans toute la fiche.

<!-- QA -->

### Principes

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

#### Que sont les exigences fonctionnelles et non fonctionnelles en architecture des données ?

Fonctionnelles : quelles données, transformations, indicateurs et sorties sont nécessaires. Non fonctionnelles : latence, fraîcheur, volume, scalabilité, disponibilité, durabilité, sécurité, conformité, coût et maintenabilité, qui déterminent souvent les choix technologiques.

#### Qu'est-ce qu'un architecture decision record (ADR) ?

Un court document qui consigne une décision importante : contexte, options étudiées, décision, conséquences et statut. Les ADR rendent le raisonnement visible et évitent de rouvrir sans cesse les débats ; ils sont stockés avec le code.

#### Qu'est-ce que la dette technique dans les plateformes de données ?

Des raccourcis qui rendent les évolutions coûteuses : pipelines non documentés, logique dupliquée, configuration codée en dur, tests absents, tables sans responsable, correctifs rapides en production. Elle s'accumule silencieusement et se manifeste par des incidents, des livraisons lentes et une défiance envers les chiffres.

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

#### Qu'est-ce que le coût total de possession (TCO) ?

Le coût complet d'une solution dans la durée : licences ou consommation cloud, infrastructure, personnes pour la construire et l'exploiter, formation, migration, support et coût des interruptions, et pas seulement le prix par unité de calcul.

#### Qu'est-ce que l'« architecture évolutive » ?

Concevoir les systèmes pour qu'ils changent de façon incrémentale avec des garde-fous (fitness functions comme des tests sur la latence, le coût ou le couplage), en privilégiant les décisions réversibles et les petits pas plutôt que de grandes conceptions initiales.

#### Pourquoi les données brutes doivent-elles être immuables ?

Des données brutes immuables permettent de retraiter l'historique quand la logique change ou que des bugs sont corrigés, d'auditer ce que les sources ont envoyé et de reconstruire les couches aval ; les modifications ont lieu dans les couches suivantes, ce qui garde le système récupérable.

#### Qu'est-ce que le principe de « responsabilité unique » appliqué aux pipelines ?

Chaque pipeline ou modèle doit avoir un objectif clair (ingérer une source, harmoniser une entité, construire un indicateur), ce qui le rend plus facile à tester, à attribuer, à réutiliser et à modifier sans effet de bord.

### Stockage et bases de données

#### Quels types de bases de données existent ?

Relationnelles (PostgreSQL, MySQL, Oracle), clé-valeur (DynamoDB, Redis), documentaires (MongoDB, Couchbase), orientées colonnes larges (Cassandra, HBase, Bigtable), orientées graphes (Neo4j, Neptune), séries temporelles (TimescaleDB, InfluxDB), moteurs de recherche (Elasticsearch, OpenSearch), vectorielles (pgvector, Pinecone, vecteurs OpenSearch) et stockages analytiques en colonnes (entrepôts, ClickHouse, Druid).

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

#### Quelles différences entre stockage bloc, fichier et objet ?

Le stockage bloc fournit des volumes bruts pour une machine (EBS), idéal pour les bases de données ; le stockage fichier des systèmes de fichiers hiérarchiques partagés (NFS, EFS) ; le stockage objet des objets plats accessibles en HTTP à très grande échelle (S3), idéal pour les data lakes.

#### Que sont les niveaux (tiers) de stockage ?

Des classes de stockage de coût et de rapidité d'accès différents (chaud, tiède, froid, archive ; S3 Standard, Infrequent Access, Glacier). Les politiques de cycle de vie déplacent les données vieillissantes vers les niveaux moins chers.

#### Que sont les formats de fichiers par lignes et en colonnes ?

Les formats par lignes (CSV, JSON, Avro) stockent les enregistrements ensemble, efficaces pour écrire et lire des enregistrements complets ; les formats en colonnes (Parquet, ORC) stockent les colonnes ensemble avec des statistiques, efficaces pour l'analytique qui lit peu de colonnes de nombreuses lignes.

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

#### Quand utiliser un moteur de recherche comme OpenSearch ?

Pour la recherche plein texte avec pertinence, correspondance approximative, facettes et analyse de journaux, généralement comme index secondaire alimenté depuis le système de référence et non comme base principale.

### Fondamentaux des systèmes distribués

#### Qu'est-ce que le théorème CAP ?

Dans un système distribué subissant une partition réseau, il faut choisir entre cohérence (chaque lecture voit la dernière écriture) et disponibilité (chaque requête reçoit une réponse). Sans partition, les deux sont possibles ; CAP porte sur le comportement en cas de panne.

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

#### Qu'est-ce qu'un point chaud (hotspot), et comment l'éviter ?

Une partition ou un nœud qui reçoit une charge disproportionnée à cause d'une clé biaisée (un utilisateur très populaire, un horodatage croissant). On l'évite avec de meilleures clés, du salage, du hachage ou en découpant les clés chaudes.

#### Qu'est-ce que le protocole de validation en deux phases, et pourquoi l'évite-t-on ?

Un protocole où un coordinateur demande à tous les participants de se préparer puis de valider, garantissant l'atomicité entre systèmes. On l'évite à grande échelle car il bloque en cas de panne, ajoute de la latence et couple la disponibilité de tous les participants ; on préfère les sagas et l'outbox.

#### Qu'est-ce qu'un quorum ?

Le nombre minimal de nœuds qui doivent acquitter une lecture ou une écriture pour qu'elle réussisse (par exemple une majorité). Si le quorum de lecture plus celui d'écriture dépasse le nombre de répliques, les lectures voient la dernière écriture.

#### Qu'est-ce que le décalage d'horloge, et pourquoi compte-t-il ?

Les horloges des différentes machines divergent : on ne peut pas se fier aux horodatages de systèmes différents pour un ordre exact. Pour ordonner les changements, utilisez des horloges logiques, des numéros de séquence ou les positions du journal du système source.

#### Quelle différence entre latence et débit ?

La latence est la durée d'une opération ; le débit est le nombre d'opérations terminées par unité de temps. Les systèmes batch optimisent le débit ; les systèmes interactifs et de streaming se soucient de la latence ; améliorer l'un peut dégrader l'autre.

### Approches de modélisation

#### Quelles approches de modélisation utilise-t-on en architecture des données ?

Des modèles normalisés (3FN) pour l'intégration et l'OLTP, dimensionnels (Kimball) pour l'analytique, Data Vault pour des couches d'intégration auditables, des tables larges dénormalisées (one big table) pour des usages précis, et des modèles anchor ou ensemble dans des cas de niche.

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

#### Comment modéliser des données semi-structurées dans une plateforme analytique ?

Les déposer brutes (JSON, `VARIANT`, colonnes struct), extraire dans les couches suivantes les champs stables et fréquemment utilisés en colonnes typées, garder le reste imbriqué pour la souplesse, et documenter les schémas par des contrats ou un registre.

#### Qu'est-ce qu'un modèle « conforme » entre domaines ?

Des définitions partagées de clés et d'entités (client, produit, date) utilisées par les produits de données de tous les domaines, pour que l'analyse inter-domaines fonctionne ; dans un mesh, elles sont souvent publiées comme produits de données de référence.

#### Comment choisir le grain d'un produit de données ?

À partir des questions des consommateurs et des événements atomiques de la source : choisir le grain le plus fin qui soit stable et utile, le documenter explicitement et proposer les agrégats comme produits séparés.

### Data lakes, lakehouses et médaillon

#### Qu'est-ce qu'un data lake ?

Un référentiel centralisé en stockage objet contenant des données brutes et traitées de tout format et à toute échelle, avec un stockage bon marché et un schéma à la lecture, utilisé pour l'analytique, la data science et comme source des entrepôts.

#### Qu'est-ce qu'un data swamp ?

Un data lake devenu inutilisable : données non documentées, non gouvernées, dupliquées, de qualité et de propriété inconnues. Catalogues, responsables, contrôles de qualité, zones et politiques de cycle de vie l'évitent.

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

#### À quoi sert le « voyage dans le temps » d'un point de vue architectural ?

À reproduire des rapports à une date, auditer, comprendre ce qui a changé, récupérer d'écritures erronées et comparer des versions, à condition que les politiques de rétention conservent assez d'historique.

### Architectures batch et streaming

#### Quelle différence entre traitement batch et streaming ?

Le batch traite des jeux de données bornés à intervalles (horaires, quotidiens) avec un fort débit et une logique plus simple ; le streaming traite en continu des flux d'événements sans fin avec une faible latence, ce qui exige gestion d'état, prise en compte du temps de l'événement et tolérance aux pannes.

#### Qu'est-ce que l'architecture Lambda ?

L'architecture de Nathan Marz avec une couche batch (recalcule des vues exactes à partir de tout l'historique), une couche de vitesse (traite les données récentes en temps réel) et une couche de service qui fusionne les deux. Elle apporte exactitude et faible latence mais duplique la logique dans deux chemins de code.

#### Qu'est-ce que l'architecture Kappa ?

La simplification de Jay Kreps : un chemin unique de traitement en streaming où tout est flux ; le retraitement se fait en rejouant le journal (Kafka) dans une nouvelle version du job. Elle supprime la logique dupliquée mais exige un journal durable et rejouable et un streaming robuste.

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

### Microservices et données événementielles

#### Comment les microservices changent-ils l'architecture des données ?

Chaque service possède ses données et sa base (une base par service) et communique par API et événements plutôt que par tables partagées. Cela améliore l'autonomie et la montée en charge, mais disperse les données et exige des modèles d'intégration pour l'analytique et les requêtes inter-services.

#### Qu'est-ce que le modèle « une base par service » ?

Chaque microservice a une base privée à laquelle lui seul accède ; les autres services utilisent son API ou ses événements. Cela évite un couplage fort via des schémas partagés.

#### Pourquoi une base partagée est-elle un anti-modèle avec les microservices ?

Les services deviennent couplés par le schéma : le changement d'une équipe en casse d'autres, les déploiements doivent être coordonnés et la responsabilité devient floue, ce qui fait perdre le principal intérêt des microservices.

#### Comment faire de l'analytique entre microservices ?

Capturer les données de chaque service (CDC de sa base ou ses événements de domaine) dans un lake ou un entrepôt, les modéliser de façon centrale ou par domaine, et servir l'analytique depuis là, plutôt que d'interroger directement les bases des services.

#### Qu'est-ce que l'architecture orientée événements ?

Des systèmes qui communiquent en produisant des événements et en y réagissant (des faits sur quelque chose qui s'est produit : `OrderPlaced`, `PaymentFailed`) via un broker, plutôt que par des appels synchrones, ce qui apporte couplage faible, scalabilité et piste d'audit naturelle.

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

#### Quelle différence entre chorégraphie et orchestration ?

Dans la chorégraphie, les services réagissent aux événements des autres sans coordinateur central (couplage faible, flux global plus difficile à voir) ; dans l'orchestration, un coordinateur dit aux services quoi faire (flux clair, dépendance centrale). Les pipelines de données utilisent surtout l'orchestration (Airflow) ; les sagas de microservices l'une ou l'autre.

### Data mesh et data fabric

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

#### Que sont les « métadonnées actives » ?

Des métadonnées qui déclenchent des automatismes plutôt que de simplement documenter : des tags qui appliquent un masquage, un lignage qui alerte sur les changements en amont, des statistiques d'usage qui suggèrent une dépréciation, des indicateurs de qualité qui bloquent la publication.

### Intégration et ingestion

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

#### Qu'est-ce qu'un contrat de livraison avec des fournisseurs de données externes ?

Un accord sur les formats de fichiers, le nommage, le calendrier de livraison, les signaux de complétude (manifestes ou fichiers `_SUCCESS`), l'encodage, le préavis de changement de schéma et la gestion des erreurs, qui évite la plupart des incidents d'ingestion de fichiers.

### Gouvernance, métadonnées et qualité

#### Qu'est-ce que la gouvernance des données ?

Le cadre de rôles, politiques, standards et processus qui garantit que les données sont exactes, sécurisées, conformes, comprises et utilisées à bon escient, incluant la responsabilité, l'intendance (stewardship), la classification, l'accès, la qualité et le cycle de vie.

#### Que sont les data owners et les data stewards ?

Les data owners rendent compte d'un domaine de données (décisions d'accès, définitions, objectifs de qualité) ; les data stewards gèrent au quotidien les définitions, les problèmes de qualité et les métadonnées, avec les ingénieurs qui mettent en œuvre les contrôles.

#### Qu'est-ce que la gestion des métadonnées ?

La collecte et la gestion des métadonnées techniques, métier et opérationnelles (schémas, définitions, lignage, qualité, usage) pour permettre la découverte, l'analyse d'impact, la gouvernance et l'automatisation ; les « métadonnées actives » s'en servent pour déclencher des actions.

#### Qu'est-ce que le lignage des données, et comment le capte-t-on ?

Le cheminement des données des sources aux consommateurs à travers les transformations. On le capte en analysant le SQL et les jobs (dbt, Unity Catalog, événements OpenLineage d'Airflow et de Spark), et on l'affiche au niveau table et colonne pour l'analyse d'impact et les audits.

#### Qu'est-ce qu'OpenLineage ?

Un standard ouvert pour les événements de lignage émis par les orchestrateurs et moteurs (Airflow, Spark, dbt, Flink), décrivant jobs, exécutions et jeux de données en entrée et en sortie, collectés par des backends comme Marquez ou des catalogues.

#### Qu'est-ce que la classification des données ?

L'étiquetage des données par sensibilité (public, interne, confidentiel, restreint) et par type (données personnelles, financières, de santé), souvent automatisé par des scanners, pour piloter les politiques d'accès, le masquage, la rétention et la conformité.

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

#### Comment éviter les jeux de données en double ?

Rendre découvrables les jeux existants (catalogue, recherche), certifier ceux qui font autorité, exiger un responsable et une revue pour tout nouveau jeu publié, surveiller l'usage et déprécier les copies.

### Sécurité et conformité

#### Quelles sont les couches de la sécurité des données ?

La gestion des identités et des accès (authentification, autorisation au moindre privilège), l'isolement réseau, le chiffrement au repos et en transit, la gestion des clés, le masquage et la tokenisation, la sécurité au niveau ligne et colonne, l'audit et la supervision, et des pratiques de développement sécurisé.

#### Quelle différence entre RBAC et ABAC ?

Le contrôle d'accès par rôles accorde des droits à des rôles attribués aux utilisateurs ; le contrôle par attributs évalue dans les politiques des attributs des utilisateurs, des ressources et du contexte (département, classification, localisation), ce qui passe mieux à l'échelle pour des règles fines (par exemple les politiques par tags).

#### Quelle différence entre pseudonymisation et anonymisation ?

La pseudonymisation remplace les identifiants par des jetons ou des hachages qu'on peut relier à nouveau avec des informations supplémentaires (ce sont toujours des données personnelles au sens du RGPD) ; l'anonymisation empêche de façon irréversible l'identification (ce ne sont plus des données personnelles), ce qui est difficile à obtenir en pratique.

#### Qu'est-ce que la tokenisation ?

Le remplacement de valeurs sensibles (numéros de carte, identifiants nationaux) par des jetons non sensibles, la correspondance étant conservée dans un coffre sécurisé, pour que la plupart des systèmes ne manipulent jamais les vraies valeurs.

#### Comment le RGPD affecte-t-il l'architecture des données ?

Il exige une base légale et la limitation des finalités, la minimisation des données, des durées de conservation limitées, la sécurité, des registres de traitement et la prise en charge des droits des personnes (accès, rectification, effacement), ce qui suppose de savoir où se trouvent les données personnelles (lignage, catalogue) et de pouvoir les supprimer dans toutes les couches.

#### Comment mettre en œuvre le droit à l'effacement dans un lakehouse ?

Savoir où se trouvent les données de chaque personne, utiliser des formats de table qui prennent en charge les suppressions (Delta, Iceberg), supprimer dans toutes les couches, faire un vacuum des anciens fichiers après la rétention, éviter de propager largement les identifiants bruts (pseudonymiser tôt), et documenter le processus et ses délais.

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

### Fiabilité, exploitation et coûts

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

#### Quels sont les principaux postes de coût des plateformes de données ?

Le calcul des transformations et des requêtes (surtout les clusters toujours allumés et les recalculs complets), les requêtes inefficaces sur de gros volumes, la duplication des données entre couches et outils, les sorties de données et transferts inter-régions, et les données inutilisées conservées indéfiniment.

#### Comment rendre une plateforme économe dès sa conception ?

Traitement incrémental, partitionnement et clustering pour l'élagage, calcul serverless ou en autoscaling avec arrêt automatique, stockage hiérarchisé et rétention, absence de copies inutiles, latence adaptée au besoin métier, et visibilité des coûts par équipe.

#### Quel est le rôle de l'infrastructure as code dans l'architecture des données ?

Définir les plateformes (stockage, calcul, droits, catalogues, jobs) de façon déclarative dans du code (Terraform, CloudFormation, Bicep, bundles) pour que les environnements soient reproductibles, relus et auditables, et que les dérives soient détectables.

#### Qu'est-ce qu'un incident de données, et comment le gérer ?

Tout événement où les données sont fausses, en retard ou indisponibles pour les consommateurs. On le gère comme un incident logiciel : détecter, évaluer l'impact, informer les consommateurs, atténuer (suspendre la publication, revenir en arrière), corriger la cause racine et rédiger un post-mortem sans recherche de coupable, avec des actions.

#### Qu'est-ce que la planification de capacité pour les plateformes de données ?

Prévoir la croissance des volumes, des utilisateurs et des charges pour que stockage, calcul et concurrence restent suffisants et que les budgets soient prêts, à partir des tendances de supervision et des plans métier.

#### Comment définir l'architecture des politiques de rétention ?

Classer les jeux de données selon les besoins légaux et métier, définir la rétention par couche (le raw peut être gardé plus longtemps pour le retraitement, ou moins pour la confidentialité), la mettre en œuvre par des règles de cycle de vie, la suppression de partitions et la rétention du format de table, et documenter les exceptions.

### Architecture des données pour l'IA et le ML

#### De quoi une plateforme de ML a-t-elle besoin côté architecture des données ?

De données d'entraînement fiables et versionnées, de features exactes à la date (point-in-time), de la réutilisation des features entre entraînement et service, d'un lignage des données aux modèles, du suivi des expériences, d'un registre de modèles et de la surveillance de la dérive des données et des prédictions.

#### Qu'est-ce qu'un feature store ?

Un système qui stocke, documente et sert les features de ML de façon cohérente pour l'entraînement (offline, historique, exact à la date) et l'inférence (online, faible latence), évitant l'écart entre entraînement et service et l'ingénierie de features dupliquée.

#### Qu'est-ce que l'exactitude à la date (point-in-time correctness) ?

Lors de la construction des données d'entraînement, les features ne doivent utiliser que l'information disponible au moment de l'événement de chaque étiquette, pour éviter la fuite de données futures ; les feature stores joignent les features à la date de chaque événement.

#### Qu'est-ce que l'écart entre entraînement et service (training-serving skew) ?

Des différences dans le calcul des features pour l'entraînement et pour l'inférence (code, sources ou moment différents), qui dégradent les performances du modèle en production. Des définitions de features partagées et les feature stores le réduisent.

#### Qu'est-ce qu'une base vectorielle, et où se situe-t-elle ?

Un stockage optimisé pour la recherche par similarité sur des embeddings (pgvector, OpenSearch, Pinecone, Weaviate, Databricks Vector Search), utilisé pour la recherche sémantique, les recommandations et la génération augmentée par récupération.

#### Quelle est l'architecture de données d'une application RAG ?

Ingérer des documents, les découper en fragments, calculer des embeddings, les stocker avec leurs métadonnées dans un index vectoriel, récupérer les fragments pertinents à la requête (souvent combinés à une recherche par mots-clés et à des filtres de droits) et les transmettre à un LLM, avec des pipelines qui maintiennent l'index frais et gouverné.

#### Comment les enjeux de gouvernance changent-ils avec l'IA ?

Il faut tracer quelles données ont entraîné quels modèles, respecter les droits lors de la récupération (un utilisateur ne doit pas voir via un LLM des documents auxquels il n'aurait pas accès directement), gérer les données personnelles dans les prompts et les données d'entraînement, et évaluer les réponses ; les catalogues gouvernent de plus en plus modèles et features aux côtés des tables.

#### Qu'est-ce que le MLOps ?

Des pratiques et outils pour développer, déployer et exploiter des modèles de ML de façon fiable : données et code versionnés, pipelines d'entraînement reproductibles, registre de modèles, tests et déploiements automatisés, supervision des performances et de la dérive, et réentraînement.

#### Quelle différence entre dérive des données et dérive de concept ?

La dérive des données est un changement de la distribution des entrées (l'âge des clients évolue) ; la dérive de concept est un changement de la relation entre entrées et cible (ce qui prédit le churn change). Les deux exigent une supervision et éventuellement un réentraînement.

#### Comment gérer les données non structurées pour l'IA ?

Les stocker en stockage objet avec leurs métadonnées dans un catalogue (volumes), tracer le lignage des documents vers les fragments et les embeddings, appliquer contrôles d'accès et classification, et construire des pipelines qui mettent à jour les index quand les documents changent ou sont supprimés.

### Cloud et architectures de référence

#### À quoi ressemble une architecture de données typique sur AWS ?

Des sources ingérées avec DMS, Kinesis/MSK, AppFlow ou Glue vers S3 ; Glue Data Catalog et Lake Formation pour la gouvernance ; traitement avec Glue, EMR ou Databricks ; tables Iceberg ou Delta ; Athena et Redshift pour le SQL ; QuickSight pour la BI ; SageMaker pour le ML ; Step Functions, MWAA ou EventBridge pour l'orchestration ; le tout défini avec CloudFormation, CDK ou Terraform.

#### À quoi ressemble une architecture de données typique sur Azure ?

Ingestion avec Data Factory ou les pipelines Fabric et Event Hubs vers ADLS Gen2/OneLake ; traitement avec Databricks ou Spark de Fabric ; tables Delta ; entrepôts Synapse/Fabric ou Databricks SQL ; Power BI ; Purview pour la gouvernance ; Entra ID pour l'identité.

#### À quoi ressemble une architecture de données typique sur Google Cloud ?

Ingestion avec Pub/Sub, Datastream (CDC) et Dataflow vers Cloud Storage et BigQuery ; traitement avec Dataflow, Dataproc ou le SQL BigQuery (souvent avec dbt ou Dataform) ; Dataplex pour la gouvernance ; Looker pour la BI ; Vertex AI pour le ML.

#### Qu'est-ce que le multi-cloud, et quand en vaut-il la peine ?

L'usage de plusieurs fournisseurs cloud. Il peut réduire la dépendance, répondre à des exigences clients ou réglementaires, ou tirer parti des meilleurs services de chacun, mais il multiplie compétences, outillage, réseau et coûts de sortie. La plupart des organisations gagnent davantage avec un cloud principal et des formats portables.

#### Qu'est-ce qu'une architecture hybride ?

La combinaison de systèmes on-premise et de services cloud, courante pendant les migrations ou pour les données réglementées ; elle exige une connectivité sécurisée (VPN, Direct Connect, ExpressRoute), une identité et une gouvernance cohérentes et des mouvements de données maîtrisés.

#### Quelles stratégies de migration existe-t-il pour les plateformes de données ?

Rehost (lift and shift), replatform (passer à des équivalents gérés avec peu de changements), refactor (repenser pour des services cloud natifs et l'ELT), retirer les actifs inutilisés et conserver ce qui doit rester. Les migrations de données les combinent généralement, par vagues et par domaine avec une validation en parallèle.

#### Qu'est-ce qu'une landing zone dans l'architecture cloud ?

Un environnement multi-comptes (ou multi-abonnements) préconfiguré et sécurisé, avec identité, réseau, journalisation, garde-fous de sécurité et structure de comptes, sur lequel les plateformes de données sont déployées de manière cohérente.

#### Comment organiser les comptes ou projets d'une plateforme de données ?

Séparer les environnements (dev, staging, prod) et souvent les domaines dans des comptes ou projets distincts pour limiter l'impact des incidents, voir les coûts et appliquer le moindre privilège, les services partagés (catalogue, réseau, journalisation) étant gérés de façon centrale.

### Mises en situation

#### Concevez une plateforme de données pour une entreprise de e-commerce de taille moyenne.

Ingérer la base des commandes en CDC, les événements web via un flux (Kafka ou Kinesis) et les outils SaaS (CRM, marketing) avec des connecteurs vers le stockage objet ; organiser des couches médaillon avec des tables Iceberg ou Delta dans un catalogue ; transformer avec dbt ou Spark en dimensions conformes et en faits ; servir la BI depuis un entrepôt ou un moteur SQL de lakehouse avec une couche sémantique ; ajouter du reverse ETL pour les segments marketing ; orchestrer avec Airflow ou des jobs natifs ; appliquer gouvernance, tests de qualité, observabilité et tags de coût ; tout définir sous forme de code avec CI/CD.

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

#### Une startup vous demande de concevoir sa première plateforme de données. Que recommandez-vous ?

La garder simple et gérée : un service d'entrepôt ou de lakehouse cloud, des connecteurs gérés pour les sources SaaS, du CDC ou des réplicas pour la base du produit, dbt pour les transformations avec des tests, un seul orchestrateur, un outil BI avec une couche sémantique, une gouvernance de base et des alertes de coût, le tout sous forme de code. N'ajouter streaming, mesh ou composants maison que quand le besoin apparaît.

#### Votre entreprise en a racheté une autre avec un cloud et une plateforme différents. Comment intégrer les données ?

Partir des questions auxquelles la direction doit répondre, cartographier les entités et indicateurs clés, répliquer les données nécessaires dans la plateforme principale par CDC ou exports (ou les partager via des formats ouverts), construire des dimensions conformes avec rapprochement des données de référence, et planifier à plus long terme la consolidation des plateformes selon les coûts et les capacités.

#### La direction veut « tout en temps réel ». Comment répondez-vous ?

Demander quelles décisions changent avec des données plus fraîches et quelle latence chacune exige, estimer coûts et complexité de chaque niveau (secondes, minutes, heures), livrer du temps réel là où la valeur métier le justifie, et garder le reste en batch ou micro-batch, moins coûteux.
