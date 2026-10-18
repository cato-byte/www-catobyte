## Fiche d'étude Hadoop

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude Hadoop : environ 200 questions](../../images/hadoop_study_guide_title_img.png)

Environ 200 questions d'entretien sur Apache Hadoop et son écosystème : HDFS, YARN, MapReduce, formats de fichiers, Hive, HBase, ZooKeeper, outils d'ingestion, sécurité, exploitation et passage au stockage objet dans le cloud. Hadoop n'est plus le choix par défaut des nouvelles plateformes, mais beaucoup d'entreprises l'utilisent encore, et ses idées (localité des données, stockage distribué, gestion des ressources) sont à la base de Spark et du lakehouse. Ouvrez une question pour voir sa réponse, ou utilisez le filtre pour chercher dans toute la fiche.

<!-- QA -->

### Fondamentaux

#### Qu'est-ce qu'Apache Hadoop ?

Un framework open source pour stocker et traiter de très grands volumes de données sur des clusters de machines standard. Ses modules centraux sont HDFS (stockage distribué), YARN (gestion des ressources), MapReduce (un modèle de traitement batch) et Hadoop Common (bibliothèques partagées).

#### Quel problème Hadoop a-t-il résolu ?

Stocker et traiter des données trop volumineuses pour une seule machine, à moindre coût, en répartissant données et calculs sur de nombreux serveurs bon marché et en tolérant les pannes matérielles de façon logicielle plutôt qu'en achetant du matériel spécialisé et coûteux.

#### D'où vient Hadoop ?

Des articles de Google sur le Google File System (2003) et MapReduce (2004). Doug Cutting et Mike Cafarella ont implémenté ces idées pour le projet de recherche Nutch ; Yahoo! a beaucoup investi, et Hadoop est devenu un projet Apache de premier niveau en 2008.

#### Quels sont les principes de conception de Hadoop ?

Déplacer le calcul vers les données (localité), supposer que le matériel tombe en panne et le gérer en logiciel (réplication, relance des tâches), monter en charge horizontalement avec des machines standard, privilégier le débit plutôt que la latence, et stocker les données en écriture unique, lectures multiples.

#### Qu'est-ce que la localité des données ?

Planifier les tâches sur les nœuds (ou racks) qui contiennent déjà les blocs qu'elles lisent, pour que les données ne transitent pas par le réseau. C'était crucial quand le réseau était le goulot d'étranglement.

#### Quels sont les fichiers de configuration principaux de Hadoop ?

`core-site.xml` (réglages communs comme le système de fichiers par défaut `fs.defaultFS`), `hdfs-site.xml` (réglages HDFS comme la réplication et les répertoires du NameNode), `yarn-site.xml` (ResourceManager et NodeManager) et `mapred-site.xml` (réglages MapReduce).

#### Quelle différence entre Hadoop 1, 2 et 3 ?

Hadoop 1 combinait la gestion des ressources et MapReduce dans le modèle JobTracker/TaskTracker. Hadoop 2 a introduit YARN, qui sépare la gestion des ressources pour accueillir d'autres moteurs, ainsi que la haute disponibilité du NameNode. Hadoop 3 a ajouté l'erasure coding, plus de deux NameNodes, l'exigence de Java 8+, le timeline service v2 de YARN et d'autres améliorations.

#### Quelles sont les principales distributions Hadoop ?

Historiquement Cloudera, Hortonworks (fusionnée avec Cloudera en 2019) et MapR (rachetée par HPE). Aujourd'hui Cloudera Data Platform est la principale distribution commerciale, et les services cloud (Amazon EMR, Google Dataproc, Azure HDInsight) proposent des écosystèmes Hadoop gérés.

#### Qu'est-ce que l'écosystème Hadoop ?

L'ensemble des projets construits autour de Hadoop : Hive (SQL), HBase (NoSQL), Pig (scripts), Spark (traitement rapide), Kafka (streaming), ZooKeeper (coordination), Oozie (workflows), Sqoop et Flume (ingestion), Ranger et Atlas (sécurité et gouvernance), Impala et Presto/Trino (SQL interactif), entre autres.

#### Pourquoi Hadoop est-il moins utilisé aujourd'hui pour les nouveaux projets ?

Le stockage objet cloud (S3, ADLS, GCS) sépare stockage et calcul de façon plus économique et élastique, Spark a remplacé MapReduce pour le traitement, et les entrepôts et lakehouses gérés (Snowflake, Databricks, BigQuery) suppriment l'exploitation de clusters. Les clusters Hadoop sont complexes à exploiter et à régler.

#### Est-il encore utile d'apprendre Hadoop ?

Oui, pour maintenir et migrer les clusters existants (fréquents dans les banques, les télécoms et les grandes entreprises), et parce que ses concepts — systèmes de fichiers distribués, blocs, réplication, localité des données, gestionnaires de ressources, partitionnement, shuffle — expliquent le fonctionnement de Spark, de Hive et des lakehouses modernes.

#### Qu'est-ce qu'un cluster de matériel standard (commodity) ?

Un cluster de serveurs standard et relativement bon marché avec des disques locaux, par opposition à des machines haut de gamme spécialisées ou à des SAN. Hadoop s'attend à ce que des nœuds tombent en panne et le compense.

#### Que signifie « écriture unique, lectures multiples » dans HDFS ?

Les fichiers sont écrits une fois puis surtout lus ; HDFS accepte l'ajout en fin de fichier mais pas les mises à jour aléatoires au milieu. Cela simplifie la cohérence et favorise l'analytique batch.

#### Comment Hadoop monte-t-il en charge ?

Horizontalement : on ajoute des DataNodes pour le stockage et des NodeManagers pour le calcul ; HDFS rééquilibre les données et YARN utilise la nouvelle capacité. La mémoire du NameNode limite le nombre de fichiers, ce que résout la fédération.

#### Qu'est-ce que Hadoop Common ?

Les bibliothèques et utilitaires partagés utilisés par les autres modules Hadoop : abstractions de système de fichiers, RPC, sérialisation, configuration, sécurité et outils en ligne de commande.

#### Qu'est-ce que l'abstraction `FileSystem` de Hadoop ?

Une API Java qui permet aux applications Hadoop de travailler avec différents systèmes de stockage via une interface unique, avec des implémentations pour HDFS (`hdfs://`), les fichiers locaux (`file://`), S3 (`s3a://`), Azure (`abfs://`), Google Cloud Storage (`gs://`) et d'autres.

#### Quelles charges typiques tournent sur les clusters Hadoop ?

L'ETL batch, le traitement de journaux, l'entreposage de données avec Hive, la préparation de features de machine learning avec Spark, l'indexation pour la recherche et le stockage de données brutes dans un data lake central.

#### Que signifie « schéma à la lecture » dans Hadoop ?

Les données sont stockées en fichiers sans imposer de schéma à l'écriture ; un schéma (par exemple une définition de table Hive) est appliqué à la lecture. L'ingestion devient souple, mais la validation est reportée sur les consommateurs.

#### Que sont les edge nodes ?

Des machines passerelles avec les bibliothèques clientes et la configuration Hadoop mais sans rôle de DataNode ni de NodeManager, d'où les utilisateurs soumettent des jobs, lancent des outils en ligne de commande et hébergent des applications clientes sans toucher aux nœuds de travail.

#### Pourquoi Hadoop privilégie-t-il le débit plutôt que la latence ?

Il a été conçu pour parcourir de gros volumes en batch, où le temps total de traitement compte plus que le temps de réponse de chaque requête ; HDFS lit de gros blocs séquentiellement et les jobs MapReduce mettent plusieurs secondes à démarrer.

### Architecture HDFS

#### Qu'est-ce que HDFS ?

Le Hadoop Distributed File System : un système de fichiers distribué et tolérant aux pannes qui découpe les fichiers en gros blocs et stocke des réplicas de chaque bloc sur des machines différentes, offrant un accès à haut débit à de gros volumes.

#### Quels sont les principaux composants de HDFS ?

Le NameNode (maître qui détient l'espace de noms et l'emplacement des blocs), les DataNodes (travailleurs qui stockent les blocs sur disques locaux) et, en haute disponibilité, un NameNode standby, des JournalNodes et des ZooKeeper Failover Controllers.

#### Que stocke le NameNode ?

L'espace de noms du système de fichiers (répertoires, fichiers, droits, blocs composant chaque fichier) en mémoire, persisté sous forme d'un point de contrôle `fsimage` et d'un journal `edits`. L'emplacement des blocs n'est pas persisté ; il provient des block reports des DataNodes.

#### Que fait un DataNode ?

Il stocke les blocs sous forme de fichiers sur ses disques locaux, sert les requêtes de lecture et d'écriture des clients, envoie des heartbeats et des block reports au NameNode, et réplique des blocs vers d'autres DataNodes sur instruction.

#### Quelle est la taille de bloc par défaut, et pourquoi est-elle si grande ?

128 Mo dans Hadoop 2 et 3 (64 Mo dans Hadoop 1). De gros blocs réduisent les métadonnées du NameNode, minimisent le temps de positionnement par rapport au temps de transfert et donnent à chaque tâche map une quantité de données significative.

#### Qu'est-ce que le facteur de réplication ?

Le nombre de copies de chaque bloc, 3 par défaut (`dfs.replication`), configurable par fichier. Plus de réplicas signifie plus de durabilité et de parallélisme en lecture, mais plus de stockage.

#### Qu'est-ce que la connaissance des racks (rack awareness) ?

Le NameNode sait dans quel rack se trouve chaque DataNode (via un script de topologie) et place les réplicas pour survivre à la perte d'un rack : par défaut le premier réplica sur le nœud de l'écrivain, le deuxième sur un nœud d'un autre rack et le troisième sur un autre nœud de ce second rack.

#### Qu'est-ce que le Secondary NameNode ?

Un assistant qui fusionne périodiquement le journal `edits` dans le `fsimage` (checkpointing) pour que le journal ne grossisse pas indéfiniment et que les redémarrages du NameNode soient plus rapides. Malgré son nom, ce n'est pas un standby et il ne peut pas prendre le relais en cas de panne.

#### Comment fonctionne la haute disponibilité du NameNode ?

Deux NameNodes (ou plus avec Hadoop 3) tournent : un actif, les autres en standby. Ils partagent le journal d'edits via un quorum de JournalNodes ; les DataNodes rendent compte à tous. Les ZooKeeper Failover Controllers surveillent la santé et déclenchent le basculement automatique, avec un fencing pour éviter deux NameNodes actifs (split brain).

#### Qu'est-ce que la fédération HDFS ?

Plusieurs NameNodes indépendants, chacun gérant une partie de l'espace de noms (par exemple `/user` et `/data`), partageant les mêmes DataNodes. Elle fait monter l'espace de noms en charge au-delà de la mémoire d'un NameNode et isole les charges. ViewFs ou la fédération par routeurs offrent une vue unifiée.

#### Qu'est-ce que l'Observer NameNode ?

Un NameNode en lecture seule (Hadoop 3) qui sert les lectures avec un état cohérent, déchargeant le NameNode actif dans les clusters à fort trafic de lecture de métadonnées.

#### Que sont les heartbeats et les block reports ?

Les DataNodes envoient un heartbeat toutes les quelques secondes pour signaler qu'ils sont vivants, et périodiquement un block report complet listant leurs blocs. Si les heartbeats cessent une dizaine de minutes, le NameNode déclare le nœud mort et re-réplique ses blocs.

#### Qu'est-ce que le safe mode ?

Un état en lecture seule dans lequel entre le NameNode au démarrage pendant qu'il charge l'espace de noms et attend que les DataNodes déclarent assez de réplicas. Il en sort automatiquement une fois un seuil de blocs atteint, ou un administrateur peut l'en faire sortir.

#### Pourquoi le NameNode est-il un goulot d'étranglement pour la montée en charge ?

Toutes les métadonnées résident dans sa mémoire : environ 150 octets par fichier, répertoire et bloc. Des centaines de millions d'objets exigent beaucoup de heap, et chaque opération de métadonnées passe par lui. La fédération, les observer NameNodes et la chasse aux petits fichiers aident.

#### Qu'est-ce que l'erasure coding dans HDFS ?

Une politique de stockage de Hadoop 3 qui stocke les données avec de la parité (par exemple Reed-Solomon 6+3) au lieu de trois copies complètes, offrant une tolérance aux pannes comparable avec 50 % de surcoût de stockage au lieu de 200 %. Les lectures et la reconstruction coûtent plus de CPU et de réseau : on la réserve aux données froides.

#### Que sont les fichiers `fsimage` et `edits` ?

`fsimage` est un point de contrôle de tout l'espace de noms à un instant donné ; `edits` est le journal de toutes les modifications depuis ce point. Au démarrage, le NameNode charge le `fsimage` puis rejoue les edits.

#### Que sont les JournalNodes ?

Un petit quorum de démons (généralement trois ou cinq) qui stockent le journal d'edits partagé des NameNodes en HA ; le NameNode actif écrit sur une majorité, et les standby lisent depuis eux pour rester synchronisés.

#### Qu'est-ce que le fencing dans la HA du NameNode ?

Des mécanismes qui garantissent qu'un ancien NameNode actif ne puisse plus modifier l'espace de noms après un basculement (par exemple tuer son processus ou faire accepter par les JournalNodes les écritures d'une seule époque d'écrivain), pour éviter le split brain.

#### Comment HDFS gère-t-il un fichier plus petit qu'un bloc ?

Il n'utilise que l'espace disque nécessaire ; un fichier de 1 Mo ne consomme pas 128 Mo. Mais il coûte toujours un objet de métadonnées complet dans le NameNode, ce qui est le vrai problème des petits fichiers.

#### Qu'est-ce que l'espace de noms HDFS ?

La hiérarchie de répertoires et de fichiers, avec droits, propriétaires, quotas et dates de modification, maintenue par le NameNode, comparable à l'arborescence d'un système de fichiers classique.

### Exploitation de HDFS

#### Comment se déroule une écriture HDFS ?

Le client demande au NameNode de créer le fichier ; pour chaque bloc, le NameNode renvoie une liste de DataNodes. Le client envoie les données par paquets au premier DataNode, qui les transmet au deuxième, qui les transmet au troisième (un pipeline). Les acquittements remontent, et le fichier devient visible une fois fermé.

#### Comment se déroule une lecture HDFS ?

Le client demande au NameNode l'emplacement des blocs du fichier, puis lit chaque bloc directement depuis le DataNode le plus proche qui en possède un réplica, en vérifiant les sommes de contrôle ; si un DataNode tombe, il passe à un autre réplica.

#### Comment HDFS détecte-t-il les données corrompues ?

Chaque bloc a des sommes de contrôle calculées à l'écriture ; les clients les vérifient à la lecture, et les DataNodes exécutent un scanner de blocs en arrière-plan. Les réplicas corrompus sont signalés au NameNode, qui re-réplique à partir d'une copie saine.

#### Que se passe-t-il quand un DataNode meurt ?

Le NameNode ne reçoit plus ses heartbeats, le déclare mort après un délai et planifie la re-réplication de ses blocs à partir des réplicas restants pour rétablir le facteur de réplication.

#### Qu'est-ce que le balancer HDFS ?

Un outil qui déplace des blocs entre DataNodes pour équilibrer l'utilisation des disques dans le cluster, généralement après l'ajout de nœuds. Le disk balancer équilibre l'utilisation entre les disques d'un même DataNode.

#### Comment retirer (decommission) un DataNode ?

L'ajouter au fichier d'exclusion et rafraîchir le NameNode (`hdfs dfsadmin -refreshNodes`) ; le NameNode re-réplique ses blocs ailleurs et, une fois le retrait terminé, le nœud peut être enlevé sans risque.

#### Quelles sont les commandes `hdfs dfs` courantes ?

```bash
hdfs dfs -ls /data/raw
hdfs dfs -mkdir -p /data/raw/orders/dt=2026-10-15
hdfs dfs -put orders.csv /data/raw/orders/dt=2026-10-15/
hdfs dfs -get /data/curated/report.parquet .
hdfs dfs -du -h /data
hdfs dfs -rm -r -skipTrash /tmp/old
hdfs dfs -setrep -w 2 /data/archive
```

#### Que fait `hdfs fsck` ?

Il vérifie la santé des fichiers et des blocs : blocs manquants, corrompus, sous-répliqués ou mal répliqués, et peut lister l'emplacement des blocs (`hdfs fsck /chemin -files -blocks -locations`). Il ne lit que les métadonnées et ne corrige rien lui-même.

#### Que montre `hdfs dfsadmin -report` ?

La capacité du cluster, l'espace utilisé et libre, et l'état de chaque DataNode (vivant, mort, en retrait), utile pour un contrôle de santé rapide.

#### Qu'est-ce que la corbeille HDFS ?

Quand elle est activée (`fs.trash.interval`), les fichiers supprimés vont dans un dossier `.Trash` du répertoire de l'utilisateur et sont définitivement supprimés après l'intervalle, ce qui protège des suppressions accidentelles. `-skipTrash` la contourne.

#### Que sont les snapshots HDFS ?

Des copies en lecture seule d'un répertoire à un instant donné (activées par répertoire par un administrateur), peu coûteuses car elles n'enregistrent que les changements ; on les utilise pour se remettre d'erreurs utilisateur et pour des sauvegardes cohérentes.

#### Que sont les quotas HDFS ?

Des quotas de noms (nombre maximal de fichiers et répertoires) et d'espace (octets maximaux, réplicas compris) définis par répertoire, pour éviter qu'une équipe épuise le cluster.

#### Qu'est-ce que `distcp` ?

Un outil qui copie de gros volumes de données entre clusters HDFS ou entre HDFS et un stockage objet, en utilisant MapReduce pour copier en parallèle, avec des options de mise à jour incrémentale et de conservation des attributs.

#### Que sont les politiques de stockage HDFS ?

Des règles qui placent les réplicas sur différents types de stockage (DISK, SSD, ARCHIVE, RAM_DISK) selon la « température » : Hot, Warm, Cold, All_SSD, One_SSD et Lazy_Persist. L'outil mover déplace les données existantes pour respecter une politique.

#### Qu'est-ce que la lecture locale short-circuit ?

Quand le client tourne sur le même nœud que le DataNode qui détient un bloc, il lit le fichier directement sur le disque local via un descripteur partagé, sans passer par le chemin réseau du DataNode, ce qui accélère les lectures.

#### Qu'est-ce que le problème des petits fichiers dans HDFS ?

Des millions de fichiers bien plus petits que la taille de bloc consomment la mémoire du NameNode (chaque fichier et bloc est un objet), ralentissent les listages et créent de nombreuses tâches minuscules. Solutions : compacter les fichiers (`INSERT OVERWRITE` Hive, repartition Spark), utiliser des formats conteneurs (SequenceFile, Parquet, ORC), ou archiver en fichiers HAR.

#### Comment changer le facteur de réplication de données existantes ?

Avec `hdfs dfs -setrep -w <n> <chemin>`, qui modifie la réplication des fichiers et attend que les réplicas soient ajoutés ou supprimés.

#### Que contrôle `dfs.datanode.failed.volumes.tolerated` ?

Le nombre de pannes de disque qu'un DataNode tolère avant de s'arrêter ; zéro par défaut, mais les gros nœuds à nombreux disques sont souvent configurés pour continuer avec un ou deux disques en panne.

#### Comment déplacer des données entre HDFS et le système de fichiers local ?

`hdfs dfs -put`/`-copyFromLocal` pour téléverser, `hdfs dfs -get`/`-copyToLocal` pour télécharger, et `hdfs dfs -getmerge` pour concaténer un répertoire de fichiers de parties en un seul fichier local.

#### Que montre `hdfs dfs -count` ?

Le nombre de répertoires, de fichiers et d'octets sous un chemin, et avec `-q` les quotas de noms et d'espace, utile pour trouver les répertoires contenant trop de petits fichiers.

#### Qu'est-ce que WebHDFS ?

Une API REST d'HDFS sur HTTP qui permet à des clients dans n'importe quel langage de lire, écrire et gérer des fichiers sans les bibliothèques Hadoop ; HttpFS en fournit une version passerelle.

### YARN

#### Qu'est-ce que YARN ?

Yet Another Resource Negotiator : le gestionnaire de ressources du cluster Hadoop. Il alloue CPU et mémoire sous forme de conteneurs aux applications (MapReduce, Spark, Tez, Flink), en séparant la gestion des ressources du moteur de traitement.

#### Quels sont les principaux composants de YARN ?

Le ResourceManager (ordonnanceur et gestionnaire d'applications du cluster), les NodeManagers (agents par nœud qui lancent et surveillent les conteneurs), les ApplicationMasters (un par application, qui négocient les ressources et coordonnent les tâches) et les conteneurs (lots alloués de mémoire et de vcores).

#### Que se passe-t-il quand on soumet une application à YARN ?

Le client la soumet au ResourceManager, qui démarre l'ApplicationMaster dans un conteneur sur un nœud. L'ApplicationMaster demande des conteneurs pour les tâches en tenant compte de la localité des données ; les NodeManagers les lancent ; l'ApplicationMaster suit l'avancement et signale la fin.

#### Quels ordonnanceurs YARN propose-t-il ?

L'ordonnanceur FIFO (premier arrivé, premier servi), le Capacity Scheduler (files hiérarchiques avec capacités garanties et élasticité, par défaut dans la plupart des distributions) et le Fair Scheduler (partage équitable des ressources entre applications et files en cours).

#### Comment fonctionne le Capacity Scheduler ?

Les files sont configurées avec des pourcentages garantis de la capacité du cluster (par exemple `etl` 50 %, `analytics` 30 %, `adhoc` 20 %), peuvent emprunter la capacité inutilisée jusqu'à un maximum, ont des limites par utilisateur et peuvent préempter des conteneurs pour rendre la capacité garantie.

#### Qu'est-ce que la préemption dans YARN ?

Quand une file est sous sa part garantie et que d'autres en utilisent plus, l'ordonnanceur peut tuer des conteneurs des applications en surconsommation pour libérer des ressources et respecter les garanties.

#### Comment configure-t-on la taille des conteneurs ?

Avec `yarn.nodemanager.resource.memory-mb` et `.cpu-vcores` (ressources offertes par un nœud), `yarn.scheduler.minimum-allocation-mb` et `maximum-allocation-mb` (tailles de conteneur autorisées), et les demandes de chaque application (par exemple `mapreduce.map.memory.mb` ou la mémoire des executors Spark plus l'overhead).

#### Que se passe-t-il quand un conteneur dépasse sa mémoire ?

Le NodeManager le tue (« Container killed by YARN for exceeding memory limits ») et la tâche est relancée. On corrige en augmentant la mémoire ou l'overhead du conteneur, ou en réduisant la mémoire par tâche (plus de partitions, moins de cache).

#### Que sont les node labels dans YARN ?

Des étiquettes qui partitionnent les nœuds (par exemple `gpu` ou `high-memory`), pour restreindre files et applications à des groupes de nœuds précis.

#### Comment fonctionne la haute disponibilité du ResourceManager ?

Un ResourceManager actif et un standby se coordonnent via ZooKeeper ; l'état est conservé dans un state store pour que le standby prenne le relais et que les applications en cours continuent (redémarrage conservant le travail).

#### Qu'est-ce que le YARN Timeline Service ?

Un service qui stocke et sert l'historique des applications et de leurs tâches (heures de début, durées, compteurs) pour la supervision et le débogage après leur fin. Spark a son propre History Server.

#### Comment inspecter et tuer des applications YARN ?

```bash
yarn application -list -appStates RUNNING
yarn application -status application_1729000000000_0042
yarn logs -applicationId application_1729000000000_0042 | less
yarn application -kill application_1729000000000_0042
```

#### Quelle différence entre les modes client et cluster de Spark sur YARN ?

En mode client, le driver Spark tourne sur la machine qui a soumis le job (un edge node), utile pour le travail interactif ; en mode cluster, le driver tourne dans le conteneur de l'ApplicationMaster sur le cluster, mieux adapté aux jobs de production qui doivent survivre à la déconnexion du client.

#### Que sont les vcores ?

Des cœurs CPU virtuels annoncés par les NodeManagers, une unité abstraite que YARN utilise pour planifier le CPU ; la rigueur de son application dépend du calculateur de ressources et de la configuration des cgroups.

#### Qu'est-ce que le DominantResourceCalculator ?

Un calculateur de ressources YARN qui tient compte de la mémoire et du CPU lors de la planification (la ressource dominante de chaque demande), au lieu de celui par défaut qui ne regarde que la mémoire.

#### Qu'est-ce que le shared cache de YARN ?

Une fonction qui met en cache les ressources des applications (JAR, fichiers) sur les nœuds d'une application à l'autre, réduisant le temps et la bande passante passés à rapatrier encore et encore les mêmes dépendances.

#### Comment empêcher un utilisateur d'occuper tout le cluster ?

Avec les limites des files de l'ordonnanceur : capacité maximale par file, facteurs de limite par utilisateur, nombre maximal d'applications par utilisateur et par file, et listes de contrôle d'accès sur les files.

### MapReduce

#### Qu'est-ce que MapReduce ?

Un modèle de programmation et un moteur d'exécution pour le traitement batch : une fonction map transforme les enregistrements d'entrée en paires clé-valeur intermédiaires, le framework regroupe toutes les valeurs par clé (shuffle et tri), et une fonction reduce agrège les valeurs de chaque clé en résultats.

#### Expliquez le comptage de mots en MapReduce.

Le mapper lit les lignes et émet `(mot, 1)` pour chaque mot. Le shuffle regroupe les paires par mot. Le reducer reçoit `(mot, [1, 1, 1, …])` et émet `(mot, somme)`. Un combiner peut additionner localement après le map pour réduire les données du shuffle.

#### Qu'est-ce qu'un InputSplit ?

Un morceau logique de l'entrée attribué à une tâche map, correspondant généralement à un bloc HDFS. Le nombre de splits détermine le nombre de tâches map.

#### Qu'est-ce qu'un RecordReader ?

Le composant qui lit un InputSplit et le transforme en enregistrements clé-valeur pour le mapper ; par exemple `LineRecordReader` donne (décalage en octets, ligne).

#### Que se passe-t-il pendant le shuffle et le tri ?

Les sorties des maps sont partitionnées par clé, triées et déversées sur disque local ; les reducers récupèrent leurs partitions auprès de tous les mappers via le réseau, les fusionnent en ordre et fournissent les clés regroupées à la fonction reduce. C'est généralement la phase la plus coûteuse.

#### Qu'est-ce qu'un combiner ?

Un « mini-reducer » optionnel exécuté sur la sortie du map avant le shuffle pour pré-agréger les valeurs par clé et réduire les transferts réseau. Il doit pouvoir s'appliquer zéro, une ou plusieurs fois sans changer le résultat (opérations associatives et commutatives comme la somme ou le max).

#### Qu'est-ce qu'un partitioner ?

La fonction qui décide quel reducer reçoit chaque clé, par défaut `hash(clé) % nbReducers`. Des partitioners personnalisés contrôlent la distribution, par exemple pour éviter le déséquilibre ou regrouper des clés liées.

#### Comment choisir le nombre de reducers ?

Assez pour paralléliser le travail de reduce en gardant une entrée raisonnable par reducer, typiquement autour de 0,95 ou 1,75 fois les slots de reduce ou selon la taille de la sortie ; zéro reducer donne un job map seul.

#### Qu'est-ce que l'exécution spéculative ?

Quand certaines tâches sont bien plus lentes que les autres (retardataires), le framework lance des tentatives en double sur d'autres nœuds et garde celle qui finit la première. Elle aide face à du matériel lent mais gaspille des ressources, et doit être désactivée en cas d'effets de bord non idempotents.

#### Que sont les compteurs (counters) ?

Des nombres nommés que les tâches incrémentent (intégrés, comme les enregistrements lus, octets écrits ou enregistrements déversés, et personnalisés, comme « lignes invalides »), agrégés sur tout le job pour la supervision et la validation.

#### Qu'est-ce que le distributed cache ?

Un mécanisme pour envoyer des fichiers en lecture seule (tables de correspondance, JAR, configuration) à chaque nœud qui exécute des tâches d'un job, afin que les tâches les lisent localement.

#### Comment faire une jointure en MapReduce ?

Une jointure côté reduce étiquette les enregistrements des deux jeux, les émet par clé de jointure et joint dans le reducer (générale, mais tout passe par le shuffle). Une jointure côté map charge le petit jeu en mémoire via le distributed cache et joint dans le mapper (rapide, mais un côté doit tenir en mémoire).

#### Pourquoi Spark a-t-il remplacé MapReduce pour la plupart des charges ?

MapReduce écrit les résultats intermédiaires sur disque entre chaque étape et exprime les pipelines complexes comme des chaînes de jobs, ce qui est lent et verbeux. Spark garde les données en mémoire entre les étapes, optimise des DAG entiers et propose des API de haut niveau (SQL, DataFrames) dans plusieurs langages.

#### Qu'est-ce que Hadoop Streaming ?

Un utilitaire qui permet d'écrire mappers et reducers dans n'importe quel langage lisant stdin et écrivant stdout (Python, bash), Hadoop gérant la distribution ; il était populaire avant PySpark.

#### À quoi sert un job map seul ?

Aux transformations qui n'ont pas besoin de regroupement, comme le filtrage, la conversion de format ou l'analyse de journaux, avec zéro reducer pour que la sortie du mapper soit écrite directement.

#### Quelles sont les classes principales d'un job MapReduce en Java ?

Une sous-classe de `Mapper` avec une méthode `map()`, une sous-classe de `Reducer` avec `reduce()`, et un driver qui configure le `Job` (formats et chemins d'entrée et de sortie, types de clés et de valeurs, nombre de reducers) et le soumet.

#### Que sont InputFormat et OutputFormat ?

`InputFormat` définit comment l'entrée est découpée et lue (`TextInputFormat`, `SequenceFileInputFormat`, `KeyValueTextInputFormat`, `CombineFileInputFormat` pour de nombreux petits fichiers) ; `OutputFormat` définit comment les résultats sont écrits (`TextOutputFormat`, `SequenceFileOutputFormat`).

#### À quoi sert `CombineFileInputFormat` ?

À regrouper de nombreux petits fichiers dans moins de splits, pour qu'un job sur des milliers de petits fichiers ne lance pas des milliers de minuscules tâches map.

#### Quel est le rôle de l'OutputCommitter ?

Il rend la sortie d'un job atomique : les tâches écrivent dans des répertoires temporaires et le committer déplace les résultats vers l'emplacement final quand le job réussit, pour que les tentatives en échec ou spéculatives ne laissent pas de sorties partielles.

#### Qu'est-ce qu'un secondary sort ?

Une technique pour que les valeurs arrivent au reducer triées selon un champ secondaire, à l'aide d'une clé composite, d'un partitioner personnalisé sur la clé naturelle et d'un comparateur de regroupement.

#### Pourquoi les tâches map devraient-elles durer au moins une minute environ ?

Démarrer une tâche a un coût (lancement de la JVM, planification) ; des tâches très courtes passent plus de temps à démarrer qu'à traiter. Des splits plus gros ou des petits fichiers regroupés rendent les tâches efficaces.

### Formats de fichiers et compression

#### Quels formats de fichiers sont courants dans Hadoop ?

Le texte (CSV, JSON), SequenceFile (clé-valeur binaire), Avro (par lignes avec schéma intégré, bon pour l'ingestion et l'évolution de schéma), Parquet et ORC (en colonnes, compressés, avec statistiques, les meilleurs pour l'analytique).

#### Qu'est-ce qu'un format découpable (splittable), et pourquoi est-ce important ?

Un format que différentes tâches peuvent lire par morceaux indépendants. Le texte brut, SequenceFile, Avro, Parquet et ORC sont découpables ; un fichier texte compressé en gzip ne l'est pas, donc une seule tâche doit le lire en entier, ce qui limite le parallélisme.

#### Quels codecs de compression utilise-t-on dans Hadoop ?

Snappy et LZ4 (rapides, compression modérée), gzip/Deflate (meilleure compression, plus lents, non découpables pour le texte), bzip2 (découpable, lent), LZO (découpable avec un index) et ZSTD (bon taux et bonne vitesse). Dans Parquet et ORC, la compression se fait par bloc : les fichiers restent découpables.

#### Pourquoi ORC est-il associé à Hive ?

ORC (Optimized Row Columnar) a été créé pour Hive : stockage en colonnes avec index légers, statistiques et filtres de Bloom, et prise en charge des tables ACID de Hive. Parquet est plus répandu dans les autres moteurs.

#### Quel est l'avantage d'Avro pour les pipelines de données ?

Le schéma est stocké avec les données et prend en charge l'évolution (ajout de champs avec valeur par défaut, renommage via des alias), et son format compact par lignes convient au streaming et à l'ingestion, souvent avec un schema registry dans Kafka.

#### Qu'est-ce qu'un SequenceFile ?

Un fichier binaire plat de paires clé-valeur, découpable et compressible, utilisé comme sortie intermédiaire de MapReduce et pour regrouper de nombreux petits fichiers dans un conteneur.

#### Que sont les fichiers HAR ?

Les Hadoop Archives : un moyen de regrouper de nombreux petits fichiers dans une archive unique (un index plus des fichiers de parties) pour réduire les objets du NameNode tout en gardant les fichiers accessibles via un chemin `har://`.

#### Comment Parquet organise-t-il les données ?

Les fichiers contiennent des groupes de lignes ; chaque groupe stocke des tronçons de colonnes, découpés en pages encodées et compressées ; le pied de fichier contient le schéma et les statistiques (min/max, nombre de nulls) par groupe et colonne, ce qui permet l'élagage de colonnes et la poussée des prédicats.

#### Comment ORC organise-t-il les données ?

Les fichiers sont découpés en stripes (typiquement 64 à 256 Mo) contenant des flux par colonne, des index légers toutes les 10 000 lignes (min/max), des filtres de Bloom optionnels et un pied avec les statistiques par stripe, ce qui permet aux moteurs de sauter stripes et groupes de lignes.

#### Faut-il compresser la sortie intermédiaire de MapReduce ?

Généralement oui, avec un codec rapide comme Snappy ou LZ4 (`mapreduce.map.output.compress`), car cela réduit les E/S disque et réseau pendant le shuffle pour un faible coût CPU.

#### Comment choisir entre Avro et Parquet ?

Avro pour les écritures par lignes, le streaming et les messages dont on lit les enregistrements complets et dont le schéma évolue souvent ; Parquet pour l'analytique où les requêtes lisent quelques colonnes de nombreuses lignes.

### Hive

#### Qu'est-ce qu'Apache Hive ?

Un système d'entrepôt de données sur Hadoop qui permet d'interroger des données dans HDFS (et dans un stockage objet) avec un dialecte SQL (HiveQL). Les requêtes sont compilées en jobs MapReduce, Tez ou Spark, et les métadonnées des tables sont stockées dans le Hive Metastore.

#### Qu'est-ce que le Hive Metastore ?

Un service adossé à une base relationnelle (MySQL, PostgreSQL) qui stocke les définitions de tables, colonnes, partitions, emplacements et formats. Hive, Spark, Impala, Presto/Trino et d'autres l'utilisent, et l'AWS Glue Data Catalog lui est compatible.

#### Quelle différence entre tables gérées et externes dans Hive ?

Hive possède les données des tables gérées : supprimer la table supprime les fichiers. Les tables externes pointent vers des données gérées ailleurs : les supprimer n'efface que les métadonnées. Les tables externes sont courantes dans les data lakes partagés.

#### Que sont les partitions dans Hive ?

Des sous-répertoires par valeur de colonne (`/sales/dt=2026-10-15/`) ; les requêtes qui filtrent sur les colonnes de partition ne lisent que les répertoires correspondants. Le partitionnement dynamique crée les partitions à partir des résultats d'une requête.

#### Qu'est-ce que le bucketing dans Hive ?

La répartition des données d'une table ou d'une partition dans un nombre fixe de fichiers selon le hachage d'une colonne, ce qui permet un échantillonnage efficace et des bucket map joins quand les tables sont « bucketées » sur la clé de jointure.

#### Quels moteurs d'exécution Hive peut-il utiliser ?

MapReduce (historique, déprécié), Apache Tez (basé sur des DAG, défaut habituel de Hive 2/3) et Spark (Hive on Spark). Hive LLAP ajoute des démons persistants avec cache pour les requêtes interactives.

#### Que sont les tables ACID de Hive ?

Des tables ORC transactionnelles (les tables gérées de Hive 3) qui prennent en charge `INSERT`, `UPDATE`, `DELETE` et `MERGE` avec isolation par snapshot, grâce à des fichiers delta fusionnés par des compactions (mineures et majeures).

#### Qu'est-ce que l'optimiseur basé sur les coûts de Hive ?

Une optimisation fondée sur Apache Calcite qui utilise les statistiques de tables et de colonnes (`ANALYZE TABLE … COMPUTE STATISTICS`) pour choisir l'ordre et la stratégie des jointures ; sans statistiques, les plans peuvent être médiocres.

#### Qu'est-ce qu'une map join dans Hive ?

Une jointure où la petite table est chargée en mémoire sur chaque mapper (broadcast), évitant le shuffle ; Hive convertit automatiquement les jointures quand la petite table est sous un seuil de taille (`hive.auto.convert.join`).

#### Comment charger des données dans des tables Hive ?

`LOAD DATA INPATH` (déplace les fichiers dans l'emplacement de la table), `INSERT INTO/OVERWRITE … SELECT`, `CREATE TABLE AS SELECT`, ou en écrivant directement des fichiers à l'emplacement d'une table externe puis en ajoutant les partitions.

#### Qu'est-ce que `MSCK REPAIR TABLE` ?

Une commande qui parcourt l'emplacement de la table à la recherche de répertoires de partition non enregistrés dans le metastore et les ajoute.

#### Que sont les SerDe dans Hive ?

Des sérialiseurs/désérialiseurs qui définissent comment les lignes sont lues et écrites : `LazySimpleSerDe` pour le texte délimité, `OpenCSVSerde`, des SerDe JSON, `RegexSerDe`, et la prise en charge intégrée d'ORC, Parquet et Avro.

#### En quoi HiveQL diffère-t-il du SQL standard ?

HiveQL est presque du SQL, mais avec des fonctions propres à Hadoop (partitions, buckets, `LATERAL VIEW explode`, SerDe, `INSERT OVERWRITE DIRECTORY`), des transactions et sous-requêtes historiquement limitées, et une sémantique de schéma à la lecture.

#### Qu'est-ce que HiveServer2 ?

Le service qui accepte les connexions clientes (JDBC/ODBC, Beeline) et exécute les requêtes HiveQL avec authentification, concurrence et sécurité, remplaçant l'ancienne CLI Hive pour l'accès multi-utilisateurs.

#### Qu'est-ce que Beeline ?

Le client JDBC en ligne de commande pour HiveServer2, utilisé pour lancer requêtes et scripts sur Hive avec la bonne authentification.

#### Qu'est-ce que `LATERAL VIEW explode` ?

Une construction Hive qui transforme des colonnes de type tableau ou map en plusieurs lignes, comparable à `UNNEST` dans d'autres dialectes SQL.

```sql
SELECT o.order_id, item
FROM orders o
LATERAL VIEW explode(o.items) t AS item;
```

#### Quelle différence entre `ORDER BY`, `SORT BY`, `DISTRIBUTE BY` et `CLUSTER BY` dans Hive ?

`ORDER BY` produit un ordre total via un seul reducer ; `SORT BY` trie au sein de chaque reducer ; `DISTRIBUTE BY` contrôle quel reducer reçoit chaque clé ; `CLUSTER BY` combine `DISTRIBUTE BY` et `SORT BY` sur les mêmes colonnes.

#### Qu'est-ce que la vectorisation de Hive ?

Le traitement de lots de lignes (généralement 1 024) à la fois avec des opérations en colonnes plutôt que ligne par ligne, ce qui accélère les lectures, filtres et agrégations sur des données ORC.

#### Comment calcule-t-on des statistiques dans Hive ?

`ANALYZE TABLE t PARTITION (dt) COMPUTE STATISTICS` pour les statistiques de table et de partition, et `… FOR COLUMNS` pour celles des colonnes, utilisées par l'optimiseur basé sur les coûts ; `hive.stats.autogather` collecte les statistiques de base à l'insertion.

#### Qu'est-ce que l'insertion avec partitions dynamiques, et que faut-il surveiller ?

`INSERT OVERWRITE TABLE t PARTITION (dt) SELECT …, dt FROM src` crée les partitions à partir des valeurs des données. Des limites (`hive.exec.max.dynamic.partitions`) évitent de créer des milliers de partitions par accident, et de nombreuses partitions avec peu de lignes produisent de petits fichiers.

### HBase

#### Qu'est-ce que HBase ?

Une base NoSQL distribuée orientée familles de colonnes, inspirée de Google Bigtable, qui tourne sur HDFS. Elle offre des lectures et écritures aléatoires en temps réel sur des milliards de lignes par clé de ligne, avec une cohérence forte par ligne.

#### Quel est le modèle de données de HBase ?

Des tables de lignes triées par clé ; chaque ligne a des familles de colonnes (définies à la création de la table), chaque famille contient un nombre quelconque de colonnes (qualifiers), et chaque cellule conserve des versions identifiées par horodatage. Les colonnes clairsemées ne coûtent rien.

#### Quels sont les principaux composants de HBase ?

Le HMaster (attribue les régions, gère les changements de schéma et l'équilibrage), les RegionServers (servent lectures et écritures des régions), les régions (plages contiguës de clés d'une table) et ZooKeeper (coordination et localisation de la table meta).

#### Comment se déroule une écriture HBase ?

Le RegionServer ajoute la modification au write-ahead log (WAL) dans HDFS pour la durabilité, puis l'écrit dans la MemStore en mémoire. Quand la MemStore est pleine, elle est vidée dans un HFile immuable sur HDFS.

#### Que sont les compactions dans HBase ?

Des processus d'arrière-plan qui fusionnent les HFiles : les compactions mineures fusionnent quelques petits fichiers ; les majeures réécrivent tous les fichiers d'un store en un seul en supprimant les cellules effacées et expirées. Les compactions majeures sont lourdes en E/S et souvent planifiées hors pointe.

#### Pourquoi la conception de la clé de ligne est-elle si importante dans HBase ?

Tout accès se fait par clé, et les lignes sont triées et découpées en régions par clé. Des clés croissantes (horodatages, séquences) envoient toutes les écritures vers une seule région (hotspotting). Utilisez le salage, le hachage ou l'inversion de champs, et concevez les clés selon les principaux modes d'accès.

#### Quand choisir HBase plutôt que Hive ?

HBase pour des lectures et écritures aléatoires à faible latence par clé (profils utilisateurs, recherches de séries temporelles, compteurs) ; Hive pour l'analytique SQL batch sur de grosses lectures.

#### Qu'est-ce qu'Apache Phoenix ?

Une couche SQL au-dessus de HBase qui compile le SQL en scans HBase, avec des index secondaires et un accès JDBC.

#### Qu'est-ce que le découpage d'une région (region split) ?

Quand une région dépasse une taille configurée, le RegionServer la découpe en deux régions sur une clé médiane, et le HMaster peut les déplacer pour équilibrer la charge. Pré-découper les tables évite les points chauds initiaux.

#### Qu'est-ce qu'une famille de colonnes, et pourquoi en avoir peu ?

Un groupe de colonnes stockées ensemble dans les mêmes fichiers avec des réglages communs (compression, versions, TTL). Chaque famille a sa propre MemStore et ses fichiers : de nombreuses familles multiplient les vidages et compactions ; deux ou trois est typique.

#### Comment lire efficacement dans HBase ?

Utiliser `Get` pour des lignes isolées par clé et `Scan` avec des clés de début et de fin pour les plages, ajouter des filtres pour réduire les données renvoyées, régler caching et batching des scans, et éviter les scans complets sur les chemins sensibles à la latence.

#### Qu'est-ce qu'un filtre de Bloom dans HBase ?

Une structure par fichier de store qui indique si une ligne (ou ligne et colonne) pourrait exister dans le fichier, ce qui permet aux lectures de sauter les fichiers qui ne la contiennent certainement pas et réduit les lectures disque des gets aléatoires.

#### Qu'est-ce qu'un TTL dans HBase ?

Une durée de vie définie par famille de colonnes ; les cellules plus anciennes que le TTL sont supprimées lors des compactions, utile pour les séries temporelles et les caches.

### Autres outils de l'écosystème

#### Qu'est-ce que ZooKeeper ?

Un service de coordination centralisé offrant un stockage clé-valeur hiérarchique (znodes), des watches et du consensus (protocole ZAB). Les composants Hadoop l'utilisent pour l'élection de leader (HA du NameNode et du ResourceManager), la configuration et la découverte de services ; les anciennes versions de Kafka l'utilisaient aussi.

#### Qu'était Apache Pig ?

Un langage de flux de données de haut niveau (Pig Latin) qui compilait des scripts en jobs MapReduce ou Tez, populaire pour l'ETL avant la maturité de Spark et Hive ; il est rarement utilisé pour de nouveaux travaux.

#### Qu'était Apache Sqoop ?

Un outil de transfert de données entre bases relationnelles et Hadoop (import vers HDFS/Hive, export retour) par des tâches MapReduce parallèles. Il a été retiré dans l'Apache Attic en 2021 ; Spark JDBC, des outils de type DMS et des outils de CDC l'ont remplacé.

#### Qu'est-ce qu'Apache Flume ?

Un service pour collecter, agréger et déplacer de gros volumes de journaux depuis de nombreuses sources vers HDFS ou HBase, avec des sources, des canaux et des sinks. Kafka l'a largement remplacé.

#### Qu'est-ce qu'Apache Oozie ?

Un ordonnanceur de workflows pour les jobs Hadoop (MapReduce, Hive, Pig, Sqoop, shell) définis en XML, avec des coordinateurs pour les déclenchements temporels et par données. La plupart des équipes sont passées à Airflow ou à d'autres orchestrateurs.

#### Que sont Impala et Presto/Trino ?

Des moteurs SQL MPP qui interrogent directement les données de HDFS et du stockage objet avec des démons persistants, offrant une latence interactive par rapport à Hive sur MapReduce. Trino (anciennement PrestoSQL) est très utilisé et sous-tend Amazon Athena.

#### Comment Spark tourne-t-il sur un cluster Hadoop ?

Spark tourne sur YARN (driver en mode client ou cluster, executors dans des conteneurs YARN), lit et écrit HDFS, utilise le Hive Metastore pour les tables et profite de la localité des données.

#### Quel est le rôle de Kafka dans les architectures Hadoop ?

Un journal de messages durable et scalable qui ingère des flux (événements, CDC) et découple producteurs et consommateurs ; les données sont ensuite écrites dans HDFS ou un stockage objet par Kafka Connect, Spark Streaming ou Flink.

#### Qu'est-ce qu'Apache Tez ?

Un framework d'exécution en DAG sur YARN qui exécute les jobs Hive et Pig comme un seul graphe de tâches, évitant les écritures disque par étape et les coûts de démarrage de MapReduce.

#### Qu'est-ce qu'Apache Ambari ?

Un outil web pour provisionner, gérer et superviser les clusters Hadoop (installation des services, configuration, alertes), surtout utilisé avec les distributions Hortonworks ; Cloudera Manager joue le même rôle chez Cloudera.

#### Qu'est-ce qu'Apache Livy ?

Un service REST pour soumettre des jobs et des sessions interactives Spark à un cluster, utilisé par les notebooks et les applications qui ne peuvent pas exécuter eux-mêmes un driver Spark.

#### Qu'est-ce qu'Apache Ozone ?

Un stockage objet distribué et scalable pour Hadoop avec une API compatible S3, conçu pour dépasser les limites d'HDFS sur les petits fichiers et l'espace de noms tout en restant compatible avec les applications Hadoop.

### Sécurité et gouvernance

#### Comment se fait l'authentification dans Hadoop ?

Avec Kerberos : utilisateurs et services obtiennent des tickets auprès d'un Key Distribution Center, que les services Hadoop vérifient. Sans Kerberos (mode « simple »), Hadoop fait confiance au nom d'utilisateur déclaré par le client, ce qui n'est pas sûr.

#### Que sont les delegation tokens ?

Des jetons émis par les services (NameNode, ResourceManager) après une authentification Kerberos, transmis aux tâches exécutées sur le cluster pour qu'elles accèdent à HDFS sans disposer elles-mêmes d'identifiants Kerberos.

#### Comment gère-t-on les droits HDFS ?

Avec des droits de type POSIX propriétaire/groupe/autres sur fichiers et répertoires, plus des ACL pour un contrôle plus fin. Les politiques fines et centralisées sont généralement gérées avec Apache Ranger.

#### Qu'est-ce qu'Apache Ranger ?

Un framework de sécurité centralisé pour Hadoop qui définit et audite des politiques d'accès (chemins HDFS, bases, tables et colonnes Hive, filtres de lignes et masquage, HBase, Kafka) avec des plugins qui les appliquent dans chaque service.

#### Qu'est-ce qu'Apache Atlas ?

Un service de métadonnées et de gouvernance qui fournit catalogue de données, lignage, classification (tags comme PII) et intégration avec Ranger pour des politiques fondées sur les tags.

#### Qu'est-ce qu'Apache Knox ?

Une passerelle qui offre un point d'entrée unique et sécurisé (API REST, interfaces) aux services Hadoop pour les utilisateurs hors du cluster, en gérant l'authentification et le SSL.

#### Comment les données sont-elles chiffrées dans Hadoop ?

En transit avec le chiffrement RPC, TLS pour les interfaces web et le chiffrement du transfert de données ; au repos avec le chiffrement transparent HDFS par zones de chiffrement dont les clés sont gérées par le Hadoop Key Management Server (KMS).

#### Qu'est-ce qu'un keytab ?

Un fichier contenant les clés d'un principal Kerberos, utilisé par les services et les jobs batch pour s'authentifier sans mot de passe ; les keytabs doivent être protégés comme des mots de passe.

#### Qu'est-ce que l'usurpation contrôlée (proxy users) dans Hadoop ?

Une configuration qui permet à un service de confiance (HiveServer2, Livy, Oozie) d'agir au nom des utilisateurs finaux, pour que les droits et les audits reflètent l'utilisateur réel et non le compte de service.

#### Comment auditer les accès dans Hadoop ?

Les journaux d'audit HDFS du NameNode enregistrent chaque accès aux fichiers ; Ranger collecte les événements d'audit de tous ses plugins dans Solr ou HDFS, et Atlas enregistre le lignage.

### Exploitation et performances

#### Comment dimensionner un cluster Hadoop ?

À partir du volume de données (taille brute × facteur de réplication × croissance, plus l'espace temporaire), des besoins de traitement (CPU et mémoire pour les jobs simultanés) et des objectifs de débit ; en gardant de la marge pour les pannes et le rééquilibrage (on garde souvent les disques sous 70 à 80 %).

#### Quelles sont les causes fréquentes de jobs Hadoop lents ?

Le déséquilibre des données (quelques reducers avec la plupart des clés), trop de petits fichiers, un parallélisme insuffisant ou excessif, des déversements sur disque dus à des tampons mémoire trop petits, des entrées compressées non découpables, l'absence de localité et la contention dans les files YARN.

#### Comment régler la mémoire de MapReduce ?

Fixer `mapreduce.map.memory.mb` et `mapreduce.reduce.memory.mb` pour la taille des conteneurs et `-Xmx` dans `mapreduce.map.java.opts` à environ 80 % du conteneur, et ajuster `mapreduce.task.io.sort.mb` pour réduire les déversements.

#### Comment traiter le déséquilibre des données dans les jobs Hadoop ?

Avec des combiners, des partitioners personnalisés, le salage des clés chaudes, des jointures côté map pour les petites tables, les optimisations de skew join de Hive (`hive.optimize.skewjoin`) ou une pré-agrégation.

#### Comment superviser un cluster Hadoop ?

Avec les interfaces web du NameNode et du ResourceManager, les métriques JMX, Cloudera Manager (ou historiquement Ambari), des exporteurs Prometheus et Grafana, et des alertes sur la capacité HDFS, les nœuds morts ou lents, les blocs sous-répliqués, le heap du NameNode, la latence RPC et l'usage des files.

#### Comment mettre à jour un cluster Hadoop ?

Planifier avec les notes de version et des vérifications de compatibilité, sauvegarder les métadonnées du NameNode, utiliser les mises à jour progressives (rolling) quand c'est possible (NameNodes en HA, DataNodes un par un), tester les jobs sur un cluster de préproduction et garder la possibilité de revenir en arrière jusqu'à la finalisation.

#### Comment sauvegarder HDFS ?

Avec des snapshots pour les erreurs utilisateur, `distcp` vers un autre cluster ou un stockage objet pour la reprise après sinistre, et des sauvegardes des métadonnées du NameNode (`fsimage` et edits). La réplication interne au cluster n'est pas une sauvegarde.

#### Quel est l'impact du garbage collector de la JVM sur les services Hadoop ?

De longues pauses de GC sur le NameNode ou les RegionServers les rendent muets, provoquant timeouts, basculements ou heartbeats manqués. Dimensionnez soigneusement les heaps, utilisez des collecteurs modernes (G1) et surveillez les journaux de GC.

#### Comment trouver les jobs qui consomment le plus de ressources du cluster ?

L'interface et les API du ResourceManager YARN (mémoire-secondes et vcore-secondes par application), les métriques des files, les history servers Spark et MapReduce, et les rapports d'usage des outils de gestion.

#### Comment nettoyer un cluster qui manque d'espace ?

Repérer les répertoires volumineux et anciens (`hdfs dfs -du -h`), vider la corbeille, supprimer les données temporaires obsolètes et les vieux snapshots, réduire la réplication des données froides ou appliquer l'erasure coding, compresser ou convertir en formats en colonnes, et ajouter de la capacité si nécessaire.

#### À quoi sert `mapreduce.job.reduce.slowstart.completedmaps` ?

Il fixe la fraction de maps qui doivent être terminés avant que les reducers commencent à récupérer les sorties ; démarrer les reducers trop tôt gaspille des slots en attente, trop tard retarde le shuffle.

### Hadoop et le cloud

#### Comment HDFS se compare-t-il à Amazon S3 ?

HDFS couple stockage et calcul sur les mêmes nœuds, offre la localité des données et une cohérence forte, et exige de gérer un cluster. S3 est un stockage objet géré, scalable indépendamment, moins cher et très durable, accessible par le réseau ; il est aujourd'hui lui aussi fortement cohérent. La plupart des data lakes cloud utilisent le stockage objet plutôt que HDFS.

#### Qu'est-ce que le connecteur S3A ?

Le connecteur de système de fichiers Hadoop (`s3a://`) qui permet à Hadoop, Hive et Spark de lire et écrire S3 comme un système de fichiers, avec des optimisations pour les envois multipart, des committers qui évitent les renommages lents et des fournisseurs d'identifiants.

#### Pourquoi les renommages posent-ils problème sur un stockage objet ?

Les stockages objet n'ont pas de vrais répertoires ; un « renommage » est une copie suivie d'une suppression de chaque objet, ce qui est lent et non atomique. Les committers de sortie Hadoop qui reposent sur des renommages sont lents ou dangereux sur S3 ; on utilise les committers S3A (magic, staging) ou des formats de table (Iceberg, Delta).

#### Qu'est-ce qu'Amazon EMR ?

Une plateforme big data gérée sur AWS qui exécute Hadoop, Spark, Hive, HBase, Presto/Trino, Flink et d'autres sur EC2, EKS ou en serverless, avec S3 (EMRFS/S3A) comme stockage principal et le Glue Data Catalog comme metastore, en clusters éphémères ou persistants.

#### Qu'est-ce qu'un cluster éphémère ?

Un cluster créé pour un job ou un pipeline puis arrêté, les données étant conservées dans un stockage objet. On évite de payer des clusters inactifs et les environnements deviennent reproductibles.

#### Comment migrer un data lake Hadoop vers le cloud ?

Inventorier données, jobs et dépendances ; copier les données vers le stockage objet avec `distcp` ou des services de transfert ; convertir les tables en formats ouverts (Parquet, puis Iceberg ou Delta) ; passer le metastore à un catalogue géré (Glue, Unity Catalog) ; porter les jobs Hive et MapReduce vers Spark ou des moteurs SQL ; remplacer Oozie par Airflow ; recréer la sécurité avec l'IAM cloud et les droits du catalogue ; et valider les résultats en parallèle avant de décommissionner.

#### Qu'est-ce qui a remplacé les composants Hadoop dans les stacks modernes ?

HDFS → stockage objet (S3, ADLS, GCS) ; YARN → Kubernetes ou calcul serverless géré ; MapReduce → Spark, Flink, moteurs SQL ; Hive Metastore → Glue, Unity Catalog, Polaris et d'autres catalogues ; tables Hive → Iceberg, Delta, Hudi ; Oozie → Airflow, Dagster ; Ranger/Atlas → gouvernance native du cloud (Lake Formation, Unity Catalog).

#### Que sont les formats de table ouverts, et quel lien avec les tables Hive ?

Iceberg, Delta Lake et Hudi ajoutent une couche de métadonnées transactionnelle au-dessus de fichiers Parquet, résolvant les problèmes des tables Hive (pas d'ACID sur stockage objet, listage lent des partitions, écritures concurrentes risquées, évolution de schéma pénible). Ce sont les successeurs modernes des tables de style Hive.

#### Qu'est-ce qu'EMRFS ?

L'implémentation par Amazon EMR du système de fichiers Hadoop pour S3, avec des fonctions comme la vue cohérente (historiquement), le chiffrement et le mappage de rôles IAM ; les versions récentes d'EMR prennent aussi en charge S3A.

#### Peut-on faire tourner Hadoop sur Kubernetes ?

En partie : Spark et Flink tournent nativement sur Kubernetes, le Hive Metastore et Trino tournent comme services, et le stockage passe sur des stockages objet. Faire tourner HDFS et YARN sur Kubernetes est possible mais en vaut rarement la complexité.

#### Que sont Google Dataproc et Azure HDInsight ?

Des services Hadoop et Spark gérés sur Google Cloud et Azure, comparables à EMR, qui créent des clusters en quelques minutes avec un stockage objet (GCS, ADLS) comme stockage principal. Azure oriente de plus en plus les nouveaux projets vers Fabric et Databricks.

#### En quoi les coûts diffèrent-ils entre Hadoop on-premise et data lakes cloud ?

Les clusters on-premise ont des coûts fixes élevés (matériel, centres de données, équipes) et sont dimensionnés pour les pics ; les lakes cloud ont un stockage et un calcul payés à l'usage qui peuvent descendre à zéro, mais exigent une gouvernance des coûts pour éviter les dérives.

### Spark sur Hadoop

#### Comment Spark lit-il les données d'HDFS ?

Via l'API `FileSystem` de Hadoop et les input formats : chaque bloc HDFS (ou plage de groupes de lignes Parquet) devient une partition, et YARN planifie les executors avec des préférences de localité proches des blocs.

#### Comment Spark utilise-t-il le Hive Metastore ?

Avec `enableHiveSupport()` (ou la configuration du catalogue), Spark lit dans le metastore les définitions de tables, partitions et emplacements : `spark.table("db.table")` et Spark SQL fonctionnent sur des tables Hive, et Spark peut créer des tables visibles par Hive.

#### Comment soumettre un job Spark à YARN ?

```bash
spark-submit \
  --master yarn --deploy-mode cluster \
  --queue etl \
  --num-executors 20 --executor-cores 4 --executor-memory 8g \
  --conf spark.executor.memoryOverhead=1g \
  --conf spark.sql.shuffle.partitions=400 \
  jobs/curate_orders.py --date 2026-10-15
```

#### Qu'est-ce que l'allocation dynamique de Spark sur YARN ?

Une fonction où Spark demande et libère des executors selon les tâches en attente, pour que les executors inactifs rendent leurs ressources à YARN ; elle nécessite le service de shuffle externe (ou le suivi du shuffle) pour que les fichiers de shuffle survivent à la suppression des executors.

#### Qu'est-ce que le service de shuffle externe ?

Un service exécuté dans chaque NodeManager qui sert les fichiers de shuffle écrits par les executors, pour que ceux-ci puissent être supprimés (allocation dynamique) ou tomber en panne sans perdre leur sortie de shuffle.

#### Comment choisir la taille des executors sur YARN ?

Équilibrer cœurs et mémoire : environ 4 à 5 cœurs par executor pour un bon débit HDFS, une mémoire par cœur adaptée à la charge, de l'overhead pour les besoins hors heap, et des ressources laissées au NodeManager et au système sur chaque nœud.

### Mises en situation

#### Le NameNode manque de mémoire heap. Que faites-vous ?

À court terme, j'augmente le heap et je redémarre pendant une fenêtre de maintenance (avec la HA, je bascule). À long terme, je réduis le nombre d'objets : trouver et compacter les petits fichiers, supprimer les données inutilisées et les vieux snapshots, utiliser des fichiers HAR, et envisager la fédération ou des observer NameNodes.

#### Une requête Hive sur une table partitionnée lit toute la table. Pourquoi ?

Le filtre ne porte pas sur la colonne de partition, l'enveloppe dans une fonction, la compare à un autre type, ou les partitions ne sont pas enregistrées et la requête retombe sur l'emplacement de la table. Je vérifie le plan avec `EXPLAIN` et je corrige filtres ou partitions.

#### Un job Spark sur YARN échoue à répétition avec des conteneurs tués pour dépassement de mémoire. Comment corriger ?

Augmenter `spark.executor.memoryOverhead` (mémoire hors heap pour les workers Python et les tampons), réduire les cœurs par executor, augmenter les partitions pour réduire les données par tâche, éviter les gros collects et le cache, et vérifier le déséquilibre.

#### De nombreux blocs sous-répliqués apparaissent après la panne d'un nœud. Est-ce un problème ?

Temporairement, c'est attendu : le NameNode re-réplique les blocs du nœud mort. Surveillez la progression ; si cela persiste, vérifiez le manque de capacité, les contraintes de racks, des problèmes de retrait ou une limitation réseau (`dfs.namenode.replication.max-streams`).

#### Comment ingérer un extrait quotidien d'une base relationnelle dans un data lake Hadoop ?

Extraire avec Spark JDBC (en parallèle par plages de clés) ou un outil de CDC, écrire en Parquet ou ORC dans un répertoire d'atterrissage daté, enregistrer les partitions dans le metastore, transformer vers des tables curées avec Hive ou Spark, lancer des contrôles de qualité et orchestrer avec Airflow ou Oozie.

#### Comment expliquer Hadoop à un interlocuteur non technique ?

C'est une façon de stocker et de traiter d'énormes volumes de données en les répartissant sur de nombreux ordinateurs ordinaires qui travaillent ensemble, de sorte que le système continue de fonctionner même si certaines machines tombent en panne.

#### Un job écrit 50 000 petits fichiers par jour dans HDFS. Quelle est votre correction ?

Faire un repartition ou un coalesce avant l'écriture pour produire des fichiers proches de la taille de bloc, lancer des jobs de compaction périodiques sur les anciennes partitions, envisager un format de table qui compacte, et alerter sur le nombre de fichiers par répertoire.

#### Les utilisateurs se plaignent que le cluster Hive est lent chaque matin à 9 h. Que vérifiez-vous ?

La configuration et la contention des files (ETL qui déborde sur les heures ouvrées), de grosses requêtes ad hoc sans filtre de partition, la charge de HiveServer2 et du metastore, des statistiques manquantes, et le besoin éventuel de LLAP ou de capacité supplémentaire pour les utilisateurs interactifs.

#### HDFS est plein à 90 % et continue de croître. Que faites-vous à court et à long terme ?

À court terme : supprimer les données temporaires et la corbeille, réduire la réplication des données froides, imposer des quotas. À long terme : hiérarchiser les données (erasure coding, stockage archive), déplacer les données froides vers un stockage objet, compresser et convertir en formats en colonnes, appliquer des politiques de rétention et planifier la capacité.

#### Vous devez migrer 500 tables Hive vers un lakehouse dans le cloud. Comment le planifier ?

Classer les tables par taille, usage et dépendances ; copier les données avec `distcp` vers le stockage objet ; convertir en Iceberg ou Delta (procédures de migration sur place ou `CTAS`) ; les enregistrer dans le nouveau catalogue ; traduire les jobs HiveQL en Spark SQL ou dbt ; migrer par vagues et par domaine en validant comptages et sommes de contrôle, et garder l'ancien cluster en lecture seule jusqu'à la bascule des consommateurs.

#### Un basculement du NameNode survient et certains jobs échouent. Pourquoi, et comment l'éviter ?

Les clients configurés avec l'adresse d'un seul NameNode au lieu du nameservice HA échouent ; les jobs en pleine opération de métadonnées peuvent recevoir des erreurs. Utilisez le nameservice logique (`hdfs://nameservice1`) avec des proxies de basculement côté client, et des relances dans les applications.
