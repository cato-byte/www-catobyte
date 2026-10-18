## Fiche d'étude Hadoop

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude Hadoop : environ 200 questions](../../images/hadoop_study_guide_title_img.png)

Environ 200 questions d'entretien sur Apache Hadoop et son écosystème : HDFS, YARN, MapReduce, formats de fichiers, Hive, HBase, ZooKeeper, outils d'ingestion, sécurité, exploitation et passage au stockage objet dans le cloud. Hadoop n'est plus le choix par défaut des nouvelles plateformes, mais beaucoup d'entreprises l'utilisent encore, et ses idées (localité des données, stockage distribué, gestion des ressources) sont à la base de Spark et du lakehouse.

La fiche suit un parcours d'apprentissage en six étapes. Chaque section est découpée en unités courtes : objectifs d'apprentissage, explication du concept et exemple commenté, puis questions (d'abord de mémorisation, ensuite d'application), un exercice pratique et les points à retenir. Pour **apprendre**, lisez chaque unité du début à la fin. Pour **réviser**, passez en mode révision ou utilisez « Aller aux questions », marquez les réponses à revoir et essayez une révision mixte entre les sections.

<!-- QA -->
<!-- stage: Fondamentaux -->

### Fondamentaux

<!-- unit: Pourquoi Hadoop existe -->

<!-- goals -->

- Expliquer le problème résolu par Hadoop et son origine.
- Décrire ses principes : localité des données, matériel standard, débit.

<!-- concept -->

Au début des années 2000, les entreprises du web avaient plus de données qu'aucune machine ne pouvait en stocker ou traiter, et les gros serveurs spécialisés coûtaient trop cher. La réponse de Google, décrite dans deux articles, fut de répartir données et calcul sur de nombreuses machines bon marché et de laisser le logiciel gérer les pannes inévitables.
Hadoop en est la version open source. Son astuce centrale : amener le calcul là où sont déjà les données, car envoyer du code coûte peu et envoyer des téraoctets beaucoup. Il vise les gros jobs batch, pas les requêtes rapides.

<!-- example -->

```text
Classic approach:  data ──network──► one big server ──► result
Hadoop:            code ──► node 1 (block A)  node 2 (block B)  node 3 (block C)
                            process locally, in parallel, combine results
```

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

<!-- challenge -->

Un manager demande pourquoi une requête Hadoop met 40 secondes à compter 10 lignes alors que la base de données répond instantanément. Que lui expliquez-vous ?

<!-- solution -->

Hadoop est conçu pour le débit sur d'énormes volumes : chaque job paie des coûts de planification et de démarrage qui dominent pour les petites requêtes. Il est efficace pour parcourir des téraoctets, pas pour de petites recherches interactives, qu'une base ou un moteur à faible latence doit servir.

<!-- takeaways -->

- Hadoop répartit données et travail sur de nombreuses machines bon marché.
- Il amène le calcul aux données.
- Il vise le débit batch, pas la latence.

<!-- unit: Versions, distributions et écosystème -->

<!-- goals -->

- Distinguer Hadoop 1, 2 et 3 et les principales distributions.
- Décrire Hadoop Common, l'abstraction FileSystem et les fichiers de configuration clés.

<!-- concept -->

Hadoop est passé d'un système MapReduce à usage unique à une plateforme. La version 2 a séparé la gestion des ressources (YARN) du traitement, pour que des moteurs comme Spark et Tez partagent un cluster ; la version 3 a ajouté l'erasure coding et davantage de NameNodes. Des éditeurs l'ont packagé en distributions avec outils d'administration, et des dizaines de projets ont poussé autour.
En dessous, des bibliothèques communes et une abstraction de système de fichiers permettent au même code de lire HDFS, des disques locaux ou du stockage objet, configuré par quelques fichiers XML.

<!-- example -->

```xml
<!-- core-site.xml -->
<property>
  <name>fs.defaultFS</name>
  <value>hdfs://prod-nameservice</value>
</property>
<!-- hdfs-site.xml -->
<property>
  <name>dfs.replication</name>
  <value>3</value>
</property>
```

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

<!-- challenge -->

Une équipe sous Hadoop 1 veut exécuter Spark sur le même cluster. Que faut-il changer, et pourquoi ?

<!-- solution -->

Il faut Hadoop 2 ou plus : YARN sépare la gestion des ressources de MapReduce, pour que Spark demande des conteneurs à côté d'autres moteurs. Le JobTracker de Hadoop 1 n'exécute que MapReduce.

<!-- takeaways -->

- Hadoop 2 a introduit YARN ; Hadoop 3, l'erasure coding.
- L'écosystème s'est construit autour d'un cluster partagé.
- L'API FileSystem abstrait HDFS, le local et le stockage objet.

<!-- unit: Comment on utilise Hadoop -->

<!-- goals -->

- Décrire le modèle write-once de HDFS, le schema on read et la montée en charge horizontale.
- Connaître les charges typiques et le rôle des edge nodes.

<!-- concept -->

Les clusters Hadoop servaient de data lake d'entreprise : les fichiers arrivent une fois, sont lus de nombreuses fois par des jobs batch et ne reçoivent un schéma que lorsqu'un job ou une table les interprète. Ce modèle convient aux journaux, à l'ETL et à l'analytique de type entrepôt, et passe à l'échelle en ajoutant des nœuds ordinaires.
Les utilisateurs ne se connectent pas aux nœuds de travail. Ils travaillent depuis des edge nodes dotés des outils clients et de la configuration, ce qui garde le cluster propre et sûr.

<!-- example -->

```text
edge node (hdfs, hive, spark-submit clients)
   │ submits jobs / reads files
   ▼
master nodes: NameNode, ResourceManager
worker nodes: DataNode + NodeManager on every machine (storage and compute together)
```

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

<!-- challenge -->

Une application doit mettre à jour des enregistrements individuels d'un fichier de nombreuses fois par jour. HDFS convient-il ?

<!-- solution -->

Non. HDFS est write once, read many : il permet l'ajout mais pas la mise à jour aléatoire. Utiliser une base de données (ou HBase pour l'accès par clé à grande échelle), ou réécrire les données par lots.

<!-- takeaways -->

- Les fichiers HDFS s'écrivent une fois et se lisent souvent.
- Le schéma s'applique à la lecture.
- Les clusters grandissent par ajout de nœuds ; on travaille depuis des edge nodes.

<!-- unit: Hadoop aujourd'hui -->

<!-- goals -->

- Expliquer pourquoi les nouveaux projets choisissent rarement Hadoop.
- Expliquer pourquoi connaître Hadoop reste utile.

<!-- concept -->

Le stockage objet cloud a changé l'économie. Stockage et calcul n'ont plus à cohabiter sur les mêmes machines : chacun passe à l'échelle et se paie séparément, et les services managés suppriment l'exploitation de cluster qu'exige Hadoop. La plupart des nouvelles plateformes partent de là.
Pourtant, de nombreuses banques, opérateurs télécoms et grandes entreprises exploitent encore de gros clusters Hadoop, et les outils modernes ont hérité de ses idées : Spark, le metastore Hive, Parquet et le partitionnement viennent de ce monde. Connaître Hadoop aide à exploiter, migrer et comprendre ce qui l'a remplacé.

<!-- example -->

| Composant Hadoop | Successeur moderne |
|---|---|
| HDFS | S3, ADLS, GCS |
| YARN | Kubernetes, calcul serverless |
| MapReduce | Spark, Flink |
| Tables Hive | Tables Iceberg / Delta |

#### Pourquoi Hadoop privilégie-t-il le débit plutôt que la latence ?

Il a été conçu pour parcourir de gros volumes en batch, où le temps total de traitement compte plus que le temps de réponse de chaque requête ; HDFS lit de gros blocs séquentiellement et les jobs MapReduce mettent plusieurs secondes à démarrer.

#### Qu'est-ce que HDFS ?

Le Hadoop Distributed File System : un système de fichiers distribué et tolérant aux pannes qui découpe les fichiers en gros blocs et stocke des réplicas de chaque bloc sur des machines différentes, offrant un accès à haut débit à de gros volumes.

<!-- challenge -->

En entretien, on vous demande pourquoi apprendre Hadoop en 2026. Répondez en deux phrases.

<!-- solution -->

De nombreuses grandes entreprises exploitent encore des clusters Hadoop qu'il faut maintenir et migrer, et ses concepts (stockage distribué, localité des données, partitionnement, metastore) sous-tendent les lakehouses et Spark d'aujourd'hui.

<!-- takeaways -->

- Le cloud a séparé stockage et calcul.
- De nombreux clusters restent à exploiter et migrer.
- Les outils modernes héritent des idées de Hadoop.

<!-- stage: Stockage distribué -->

### Architecture HDFS

<!-- unit: NameNode et DataNodes -->

<!-- goals -->

- Décrire les composants de HDFS et ce que chacun stocke.
- Expliquer heartbeats, block reports et safe mode.

<!-- concept -->

HDFS sépare savoir et stocker. Le NameNode sait : l'arborescence, les permissions, quels blocs forment chaque fichier et où ils se trouvent, le tout en mémoire. Les DataNodes stockent : les blocs comme simples fichiers sur disques locaux, servant directement lectures et écritures aux clients.
Les deux côtés restent synchronisés par des messages constants. Les heartbeats montrent qu'un DataNode est vivant ; les block reports disent au NameNode ce qu'il détient. Au démarrage, le NameNode attend en safe mode, en lecture seule, que suffisamment de blocs soient déclarés.

<!-- example -->

```text
NameNode (memory):  /data/orders/part-0.parquet → blocks b1, b2
                    b1 → dn1, dn4, dn7     b2 → dn2, dn4, dn9
DataNode dn4 disk:  /hadoop/dfs/data/current/.../blk_b1, blk_b2
```

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

<!-- challenge -->

Après un redémarrage du NameNode, les écritures échouent pendant 10 minutes avec une erreur « safe mode ». Quelque chose est-il cassé ?

<!-- solution -->

Probablement pas. Le NameNode reste en safe mode jusqu'à ce qu'assez de DataNodes aient déclaré leurs blocs ; sur un gros cluster, cela prend des minutes. Vérifier `hdfs dfsadmin -safemode get` et le pourcentage de blocs déclarés ; ne forcer la sortie que si des blocs manquent vraiment.

<!-- takeaways -->

- Le NameNode porte les métadonnées ; les DataNodes, les blocs.
- Heartbeats et block reports les synchronisent.
- Le safe mode protège les données pendant la déclaration des blocs.

<!-- unit: Blocs et réplication -->

<!-- goals -->

- Expliquer les gros blocs, la réplication et le placement par rack.
- Comparer réplication et erasure coding.

<!-- concept -->

HDFS découpe les fichiers en gros blocs, typiquement 128 Mo, pour que le NameNode suive peu d'objets et que les disques lisent en longues séquences. Chaque bloc est copié, trois fois par défaut, et le placement tient compte des racks : les copies se répartissent pour qu'une panne de rack ne perde pas de données.
Trois copies, c'est payer trois fois le stockage. L'erasure coding stocke plutôt les données avec de la parité, à la manière du RAID, ramenant le surcoût à environ la moitié, au prix de plus de CPU et de réseau. Il convient aux données froides.

<!-- example -->

| Schéma | Surcoût de stockage | Résiste à |
|---|---|---|
| Réplication ×3 | 200 % | 2 copies perdues |
| Erasure coding RS-6-3 | 50 % | 3 cellules perdues sur 9 |

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

<!-- challenge -->

Un cluster stocke 2 Po de journaux de plus d'un an, lus quelques fois par trimestre. Comment réduire leur coût de stockage ?

<!-- solution -->

Appliquer une politique d'erasure coding (par exemple RS-6-3) aux répertoires de vieux journaux, faisant passer le surcoût de 200 % à 50 %. Garder les données chaudes répliquées pour la performance en lecture.

<!-- takeaways -->

- Les gros blocs gardent métadonnées réduites et lectures efficaces.
- Les répliques se répartissent entre racks.
- L'erasure coding économise de l'espace sur les données froides.

<!-- unit: Durabilité des métadonnées -->

<!-- goals -->

- Expliquer le fsimage et le journal edits.
- Décrire les rôles du Secondary NameNode et des JournalNodes.

<!-- concept -->

Le NameNode garde les métadonnées en mémoire pour la vitesse : il lui faut donc un enregistrement durable sur disque. Il utilise deux fichiers : un checkpoint complet de l'espace de noms (fsimage) et un journal de chaque changement depuis (edits). Au redémarrage, il charge le checkpoint et rejoue le journal.
Si le journal grossit sans fin, les redémarrages durent sans fin. Un assistant fusionne régulièrement le journal dans le checkpoint. En haute disponibilité, un petit quorum de JournalNodes stocke le journal partagé, pour qu'un NameNode standby suive chaque changement.

<!-- example -->

```text
fsimage_0000000000041000      (namespace at transaction 41000)
edits_0000000000041001-...    (every change since)
checkpoint: fsimage + edits → new fsimage, edits truncated
```

#### Pourquoi le NameNode est-il un goulot d'étranglement pour la montée en charge ?

Toutes les métadonnées résident dans sa mémoire : environ 150 octets par fichier, répertoire et bloc. Des centaines de millions d'objets exigent beaucoup de heap, et chaque opération de métadonnées passe par lui. La fédération, les observer NameNodes et la chasse aux petits fichiers aident.

#### Qu'est-ce que l'erasure coding dans HDFS ?

Une politique de stockage de Hadoop 3 qui stocke les données avec de la parité (par exemple Reed-Solomon 6+3) au lieu de trois copies complètes, offrant une tolérance aux pannes comparable avec 50 % de surcoût de stockage au lieu de 200 %. Les lectures et la reconstruction coûtent plus de CPU et de réseau : on la réserve aux données froides.

#### Que sont les fichiers `fsimage` et `edits` ?

`fsimage` est un point de contrôle de tout l'espace de noms à un instant donné ; `edits` est le journal de toutes les modifications depuis ce point. Au démarrage, le NameNode charge le `fsimage` puis rejoue les edits.

<!-- challenge -->

Un redémarrage du NameNode prend deux heures. Les journaux montrent qu'il rejoue un énorme fichier edits. Qu'est-ce qui n'allait pas ?

<!-- solution -->

Le checkpointing s'était arrêté : le Secondary ou Standby NameNode ne fusionnait plus les edits dans le fsimage. Réparer le processus de checkpoint et surveiller le temps écoulé depuis le dernier.

<!-- takeaways -->

- fsimage est un checkpoint ; edits journalise les changements depuis.
- Les checkpoints gardent les redémarrages rapides.
- Les JournalNodes partagent le journal edits en HA.

<!-- unit: Haute disponibilité et passage à l'échelle du NameNode -->

<!-- goals -->

- Expliquer NameNode HA, fencing, observers et fédération.
- Reconnaître et gérer les limites mémoire du NameNode.

<!-- concept -->

Le NameNode était le point unique de défaillance de Hadoop et sa limite d'échelle. La haute disponibilité ajoute des NameNodes standby qui suivent le journal edits partagé et prennent le relais quand l'actif tombe ; le fencing garantit que l'ancien actif ne peut plus écrire. Les clients doivent s'adresser au nameservice logique, pas à un hôte.
L'échelle est un problème de mémoire : chaque fichier et bloc coûte du heap au NameNode. La fédération répartit l'espace de noms entre plusieurs NameNodes, les observers absorbent la charge de lecture, et des fichiers moins nombreux et plus gros réduisent la pression.

<!-- example -->

```xml
<property><name>dfs.nameservices</name><value>prod-nameservice</value></property>
<property><name>dfs.ha.namenodes.prod-nameservice</name><value>nn1,nn2</value></property>
<!-- clients use hdfs://prod-nameservice/... never hdfs://nn1-host:8020/... -->
```

#### Que sont les JournalNodes ?

Un petit quorum de démons (généralement trois ou cinq) qui stockent le journal d'edits partagé des NameNodes en HA ; le NameNode actif écrit sur une majorité, et les standby lisent depuis eux pour rester synchronisés.

#### Qu'est-ce que le fencing dans la HA du NameNode ?

Des mécanismes qui garantissent qu'un ancien NameNode actif ne puisse plus modifier l'espace de noms après un basculement (par exemple tuer son processus ou faire accepter par les JournalNodes les écritures d'une seule époque d'écrivain), pour éviter le split brain.

#### Comment HDFS gère-t-il un fichier plus petit qu'un bloc ?

Il n'utilise que l'espace disque nécessaire ; un fichier de 1 Mo ne consomme pas 128 Mo. Mais il coûte toujours un objet de métadonnées complet dans le NameNode, ce qui est le vrai problème des petits fichiers.

#### Qu'est-ce que l'espace de noms HDFS ?

La hiérarchie de répertoires et de fichiers, avec droits, propriétaires, quotas et dates de modification, maintenue par le NameNode, comparable à l'arborescence d'un système de fichiers classique.

#### Comment se déroule une écriture HDFS ?

Le client demande au NameNode de créer le fichier ; pour chaque bloc, le NameNode renvoie une liste de DataNodes. Le client envoie les données par paquets au premier DataNode, qui les transmet au deuxième, qui les transmet au troisième (un pipeline). Les acquittements remontent, et le fichier devient visible une fois fermé.

#### Comment se déroule une lecture HDFS ?

Le client demande au NameNode l'emplacement des blocs du fichier, puis lit chaque bloc directement depuis le DataNode le plus proche qui en possède un réplica, en vérifiant les sommes de contrôle ; si un DataNode tombe, il passe à un autre réplica.

#### Comment HDFS détecte-t-il les données corrompues ?

Chaque bloc a des sommes de contrôle calculées à l'écriture ; les clients les vérifient à la lecture, et les DataNodes exécutent un scanner de blocs en arrière-plan. Les réplicas corrompus sont signalés au NameNode, qui re-réplique à partir d'une copie saine.

<!-- challenge -->

L'usage du heap du NameNode croît de 5 % par mois, surtout à cause de millions de minuscules fichiers. Outre l'ajout de mémoire, que faites-vous ?

<!-- solution -->

S'attaquer au nombre de fichiers : compacter les petits fichiers en gros (ou les archiver), corriger les jobs qui les produisent, poser des quotas de noms sur les répertoires, et envisager la fédération si l'espace de noms continue de croître.

<!-- takeaways -->

- NameNodes standby et fencing assurent la HA.
- Les clients doivent utiliser le nameservice HA.
- La mémoire du NameNode suit le nombre de fichiers et de blocs.

### Exploitation de HDFS

<!-- unit: Lectures, écritures et intégrité -->

<!-- goals -->

- Décrire comment HDFS lit et écrit les données.
- Expliquer checksums, short-circuit reads et WebHDFS.

<!-- concept -->

Les données ne transitent jamais par le NameNode. Pour écrire, un client lui demande où placer un bloc, puis envoie les données à un pipeline de DataNodes qui les relaient et accusent réception. Pour lire, le client obtient l'emplacement des blocs et lit directement depuis le DataNode le plus proche.
L'intégrité est vérifiée partout : les checksums sont calculés à l'écriture et contrôlés à la lecture, si bien que la corruption est détectée et servie depuis une autre réplique. Les lecteurs locaux peuvent éviter le réseau, et les clients distants utiliser une API REST.

<!-- example -->

```text
write: client ──► dn1 ──► dn4 ──► dn7   (pipeline, acks flow back)
read:  client ──► NameNode: "where is b1?" ──► dn4 (closest) ──► data
```

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

<!-- challenge -->

Un disque corrompt silencieusement quelques blocs. Les utilisateurs reçoivent-ils de mauvaises données ? Que se passe-t-il ?

<!-- solution -->

Non. Les checksums échouent à la lecture : le client lit une autre réplique et signale la corrompue ; le NameNode planifie une nouvelle copie saine. Les block scanners des DataNodes détectent aussi la corruption de façon proactive.

<!-- takeaways -->

- Les données circulent directement entre clients et DataNodes.
- Les écritures passent par un pipeline de réplication.
- Les checksums détectent et contournent la corruption.

<!-- unit: Commandes HDFS du quotidien -->

<!-- goals -->

- Déplacer et inspecter des données avec les commandes `hdfs dfs`.
- Vérifier santé et capacité avec `fsck` et `dfsadmin`.

<!-- concept -->

L'essentiel du travail HDFS quotidien tient en quelques commandes proches de celles d'Unix : lister, copier, déplacer, mesurer des tailles. L'administration ajoute des contrôles de santé : `fsck` signale par chemin les blocs manquants, corrompus ou sous-répliqués, et `dfsadmin` montre la capacité et l'état des nœuds du cluster.
Changer la réplication de données existantes est aussi une commande, utile pour renforcer la protection des données critiques ou l'alléger sur l'espace temporaire.

<!-- example -->

```bash
hdfs dfs -mkdir -p /data/raw/orders/dt=2026-10-17
hdfs dfs -put orders.csv /data/raw/orders/dt=2026-10-17/
hdfs dfs -du -h /data/raw | sort -h | tail
hdfs dfs -count -q /data/raw/orders
hdfs fsck /data/raw/orders -files -blocks | tail
hdfs dfsadmin -report | head -20
```

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

<!-- challenge -->

Un utilisateur affirme qu'un jeu de données critique « est peut-être endommagé ». Quelles commandes lancez-vous, et que cherchez-vous ?

<!-- solution -->

`hdfs fsck <path> -files -blocks -locations` pour les blocs manquants, corrompus ou sous-répliqués, et `hdfs dfsadmin -report` pour les DataNodes morts. Si des blocs manquent sans réplique vivante, restaurer depuis un snapshot ou une sauvegarde.

<!-- takeaways -->

- `hdfs dfs` couvre les opérations sur fichiers.
- `fsck` vérifie la santé des blocs par chemin.
- `dfsadmin -report` montre capacité et nœuds du cluster.

<!-- unit: Pannes de nœuds et maintenance -->

<!-- goals -->

- Expliquer ce qui se passe quand un DataNode tombe.
- Équilibrer, décommissionner et tolérer les pannes de disque en sécurité.

<!-- concept -->

Dans un grand cluster, un disque ou un nœud est toujours en train de tomber. Quand un DataNode cesse d'envoyer des heartbeats, le NameNode re-réplique ses blocs depuis les copies survivantes ; des blocs temporairement sous-répliqués sont normaux. Les nœuds peuvent aussi tolérer quelques disques en panne au lieu de s'arrêter.
Le travail planifié utilise les mêmes mécanismes en douceur : le décommissionnement copie les blocs d'un nœud ailleurs avant son retrait, et le balancer égalise l'usage des disques après l'ajout de nœuds.

<!-- example -->

```bash
echo "dn12.prod" >> /etc/hadoop/conf/dfs.exclude
hdfs dfsadmin -refreshNodes          # dn12 → "Decommission in progress"
hdfs dfsadmin -report | grep -A3 dn12
hdfs balancer -threshold 10          # after adding new nodes
```

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

<!-- challenge -->

Vous devez retirer trois DataNodes pour remplacer du matériel sans risquer de données. Quelles étapes suivez-vous ?

<!-- solution -->

Les décommissionner via le fichier d'exclusion et `-refreshNodes`, attendre qu'ils apparaissent « Decommissioned » (tous les blocs copiés ailleurs), puis les arrêter. Lancer le balancer à l'arrivée du nouveau matériel.

<!-- takeaways -->

- Le NameNode re-réplique les blocs des nœuds morts.
- Décommissionnez avant de retirer un nœud.
- Le balancer égalise l'usage des disques.

<!-- unit: Protéger et organiser les données -->

<!-- goals -->

- Utiliser corbeille, snapshots et quotas pour protéger les données.
- Placer les données avec des storage policies et les copier avec `distcp`.

<!-- concept -->

HDFS offre plusieurs filets de sécurité contre les erreurs. La corbeille garde un temps les fichiers supprimés ; les snapshots conservent des vues en lecture seule de répertoires à un instant donné pour un coût quasi nul ; les quotas empêchent une équipe de remplir le cluster.
Les storage policies placent les données sur le bon support, SSD pour le chaud ou disques d'archive pour le froid, et `distcp` copie de gros volumes entre clusters ou vers le stockage objet avec un job parallèle.

<!-- example -->

```bash
hdfs dfsadmin -allowSnapshot /data/finance
hdfs dfs -createSnapshot /data/finance before-reload-2026-10-17
hdfs dfsadmin -setSpaceQuota 50t /data/marketing
hadoop distcp -update hdfs://prod/data/finance s3a://backup-bucket/finance
```

#### Que montre `hdfs dfs -count` ?

Le nombre de répertoires, de fichiers et d'octets sous un chemin, et avec `-q` les quotas de noms et d'espace, utile pour trouver les répertoires contenant trop de petits fichiers.

#### Qu'est-ce que WebHDFS ?

Une API REST d'HDFS sur HTTP qui permet à des clients dans n'importe quel langage de lire, écrire et gérer des fichiers sans les bibliothèques Hadoop ; HttpFS en fournit une version passerelle.

#### Qu'est-ce que YARN ?

Yet Another Resource Negotiator : le gestionnaire de ressources du cluster Hadoop. Il alloue CPU et mémoire sous forme de conteneurs aux applications (MapReduce, Spark, Tez, Flink), en séparant la gestion des ressources du moteur de traitement.

#### Quels sont les principaux composants de YARN ?

Le ResourceManager (ordonnanceur et gestionnaire d'applications du cluster), les NodeManagers (agents par nœud qui lancent et surveillent les conteneurs), les ApplicationMasters (un par application, qui négocient les ressources et coordonnent les tâches) et les conteneurs (lots alloués de mémoire et de vcores).

#### Que se passe-t-il quand on soumet une application à YARN ?

Le client la soumet au ResourceManager, qui démarre l'ApplicationMaster dans un conteneur sur un nœud. L'ApplicationMaster demande des conteneurs pour les tâches en tenant compte de la localité des données ; les NodeManagers les lancent ; l'ApplicationMaster suit l'avancement et signale la fin.

<!-- challenge -->

Avant un rechargement risqué d'un répertoire finance, comment garantir un retour arrière en quelques minutes ?

<!-- solution -->

Prendre un snapshot HDFS du répertoire avant le rechargement. En cas de problème, recopier les fichiers depuis le chemin `.snapshot` (les snapshots sont bon marché et instantanés à créer).

<!-- takeaways -->

- Corbeille et snapshots protègent des erreurs.
- Les quotas protègent la capacité partagée.
- `distcp` copie de gros volumes en parallèle.

<!-- unit: Le problème des petits fichiers -->

<!-- goals -->

- Expliquer pourquoi les petits fichiers nuisent à HDFS et aux jobs qui le lisent.
- Corriger et prévenir leur prolifération.

<!-- concept -->

Chaque fichier, même minuscule, coûte de la mémoire au NameNode et généralement une tâche à la lecture. Des millions de petits fichiers épuisent donc le NameNode et font passer aux jobs plus de temps à démarrer des tâches qu'à traiter des données.
Ils viennent généralement de jobs de streaming ou trop parallèles qui écrivent un fichier par tâche. Le remède est à la source, écrire moins de fichiers plus gros, plus une compaction régulière de l'existant.

<!-- example -->

```text
50,000 files × 200 KB  = 10 GB  → 50,000 NameNode objects, 50,000 map tasks
80 files × 128 MB      = 10 GB  → 80 objects, 80 tasks
```

#### Quels ordonnanceurs YARN propose-t-il ?

L'ordonnanceur FIFO (premier arrivé, premier servi), le Capacity Scheduler (files hiérarchiques avec capacités garanties et élasticité, par défaut dans la plupart des distributions) et le Fair Scheduler (partage équitable des ressources entre applications et files en cours).

#### Comment fonctionne le Capacity Scheduler ?

Les files sont configurées avec des pourcentages garantis de la capacité du cluster (par exemple `etl` 50 %, `analytics` 30 %, `adhoc` 20 %), peuvent emprunter la capacité inutilisée jusqu'à un maximum, ont des limites par utilisateur et peuvent préempter des conteneurs pour rendre la capacité garantie.

<!-- challenge -->

Un job de streaming écrit un fichier par partition chaque minute. Comment stopper la croissance sans perdre en fraîcheur ?

<!-- solution -->

Garder les fichiers minute dans une zone d'atterrissage et lancer une compaction horaire ou quotidienne qui les réécrit en quelques gros fichiers (ou utiliser un format de table avec compaction), puis supprimer les originaux.

<!-- takeaways -->

- Les petits fichiers coûtent mémoire NameNode et surcharge de tâches.
- Écrivez moins de fichiers plus gros à la source.
- Compactez l'existant.

### YARN

<!-- unit: Choisir un format de fichier -->

<!-- goals -->

- Comparer texte, SequenceFile, Avro, Parquet et ORC.
- Expliquer la divisibilité et quand utiliser Avro ou Parquet.

<!-- concept -->

Les formats de fichier décident du travail d'un job avant tout calcul. Le texte est universel mais volumineux et non typé. SequenceFiles et Avro stockent des lignes en binaire, Avro embarquant son schéma pour évoluer sans risque, ce qui convient aux messages et à l'ingestion. Les formats colonnaires conviennent à l'analytique.
La divisibilité décide du parallélisme : un format lisible en morceaux indépendants permet à de nombreuses tâches de se partager un gros fichier. Il existe des contournements pour les petits fichiers comme les archives, mais ils ne remplacent pas une meilleure écriture.

<!-- example -->

| Besoin | Format |
|---|---|
| Ingérer des événements Kafka au schéma évolutif | Avro |
| Tables analytiques interrogées par colonne | Parquet ou ORC |
| Données clé-valeur intermédiaires MapReduce | SequenceFile |
| Archiver des millions de minuscules fichiers | HAR |

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

<!-- challenge -->

Les événements bruts arrivent en Avro, et les analystes interrogent trois colonnes d'un jeu de 200. Quelle organisation proposez-vous ?

<!-- solution -->

Garder Avro pour l'ingestion brute (évolution de schéma, enregistrements complets), et convertir en Parquet ou ORC partitionné pour les tables analytiques, pour que les requêtes ne lisent que les colonnes utiles.

<!-- takeaways -->

- Avro pour les lignes et l'évolution de schéma ; colonnaire pour l'analytique.
- Les formats divisibles permettent des lectures parallèles.
- Les archives aident sans corriger la source des petits fichiers.

<!-- unit: Formats colonnaires et compression -->

<!-- goals -->

- Décrire comment Parquet et ORC organisent les données.
- Choisir les codecs de compression, y compris pour la sortie intermédiaire.

<!-- concept -->

Parquet et ORC regroupent tous deux les lignes en gros blocs (row groups ou stripes) et stockent chaque colonne séparément à l'intérieur, avec des statistiques permettant d'ignorer des blocs. ORC a grandi avec Hive et ajoute des index légers ; Parquet est le plus largement supporté par les moteurs.
La compression multiplie le gain, mais le codec compte : les codecs rapides comme Snappy conviennent aux données chaudes et intermédiaires, les plus forts économisent davantage d'espace, et les codecs non divisibles sur du texte brut limitent le parallélisme.

<!-- example -->

```properties
# compress map output to cut shuffle I/O
mapreduce.map.output.compress=true
mapreduce.map.output.compress.codec=org.apache.hadoop.io.compress.SnappyCodec
```

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

<!-- challenge -->

Un job lit un unique fichier `.csv.gz` de 40 Go avec une seule tâche map. Pourquoi, et comment corriger ?

<!-- solution -->

Gzip n'est pas divisible : une seule tâche doit lire tout le fichier. Découper l'entrée avant compression, utiliser un codec divisible (bzip2) ou, mieux, convertir en Parquet ou ORC avec Snappy ou ZSTD.

<!-- takeaways -->

- Parquet et ORC stockent les colonnes par blocs avec statistiques.
- Codecs rapides pour le chaud et l'intermédiaire.
- Le texte compressé non divisible limite le parallélisme.

<!-- stage: Calcul sur le cluster -->

### MapReduce

<!-- unit: Architecture de YARN -->

<!-- goals -->

- Décrire les composants de YARN et le cycle de vie d'une application.
- Inspecter, gérer et rendre le ResourceManager hautement disponible.

<!-- concept -->

YARN a fait de Hadoop une plateforme partagée. Le ResourceManager possède la capacité du cluster ; les NodeManagers proposent le CPU et la mémoire de chaque nœud sous forme de conteneurs ; chaque application a son propre ApplicationMaster qui négocie les conteneurs et suit ses tâches. MapReduce, Spark et Tez tournent ainsi côte à côte.
Le ResourceManager étant central, il tourne avec un standby, et un timeline service conserve l'historique une fois les applications terminées.

<!-- example -->

```bash
yarn application -list -appStates RUNNING
yarn application -status application_1729150000000_0042
yarn logs -applicationId application_1729150000000_0042 | less
yarn application -kill application_1729150000000_0042
```

#### Comment empêcher un utilisateur d'occuper tout le cluster ?

Avec les limites des files de l'ordonnanceur : capacité maximale par file, facteurs de limite par utilisateur, nombre maximal d'applications par utilisateur et par file, et listes de contrôle d'accès sur les files.

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

<!-- challenge -->

Une requête Hive incontrôlée accapare l'essentiel du cluster. Comment la trouver et l'arrêter en ligne de commande ?

<!-- solution -->

Lister les applications en cours avec `yarn application -list`, l'identifier par utilisateur, file et ressources, l'examiner avec `-status` et l'arrêter avec `yarn application -kill <id>`. Revoir ensuite les limites des files.

<!-- takeaways -->

- Le ResourceManager alloue ; les NodeManagers exécutent les conteneurs.
- Chaque application a son ApplicationMaster.
- Le ResourceManager tourne avec un standby pour la HA.

<!-- unit: Ordonnanceurs et files -->

<!-- goals -->

- Comparer les ordonnanceurs YARN et configurer des files de capacité.
- Utiliser préemption, node labels et limites par utilisateur.

<!-- concept -->

Un cluster partagé a besoin de règles d'attribution. Le Capacity Scheduler divise le cluster en files aux parts garanties qui peuvent emprunter la capacité inutilisée. Quand une file a besoin de récupérer sa garantie, la préemption reprend des conteneurs aux emprunteurs.
D'autres contrôles affinent les règles : les node labels orientent le travail vers du matériel spécifique, et les limites par utilisateur empêchent une personne d'occuper toute une file.

<!-- example -->

```xml
<property><name>yarn.scheduler.capacity.root.queues</name><value>etl,analytics,adhoc</value></property>
<property><name>yarn.scheduler.capacity.root.etl.capacity</name><value>50</value></property>
<property><name>yarn.scheduler.capacity.root.analytics.capacity</name><value>35</value></property>
<property><name>yarn.scheduler.capacity.root.adhoc.capacity</name><value>15</value></property>
<property><name>yarn.scheduler.capacity.root.adhoc.maximum-capacity</name><value>30</value></property>
```

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

<!-- challenge -->

Les requêtes ad hoc empruntent toute la capacité libre la nuit, et l'ETL de 05:00 les attend. Que configurez-vous ?

<!-- solution -->

Activer la préemption pour que la file ETL récupère sa part garantie, et plafonner la capacité maximale de la file ad hoc ainsi que les limites par utilisateur.

<!-- takeaways -->

- Les files garantissent des parts et empruntent l'inutilisé.
- La préemption restitue les garanties.
- Labels et limites par utilisateur affinent l'allocation.

<!-- unit: Conteneurs et ressources -->

<!-- goals -->

- Configurer la taille des conteneurs et comprendre les arrêts pour mémoire.
- Expliquer vcores, DominantResourceCalculator et shared cache.

<!-- concept -->

Chaque tâche tourne dans un conteneur doté d'une taille mémoire et CPU. Les nœuds annoncent ce qu'ils offrent, l'ordonnanceur impose minimums et maximums, et le NodeManager tue tout conteneur qui dépasse sa mémoire. La plupart des erreurs « killed by YARN » signifient que le conteneur était trop petit pour le heap plus les besoins hors heap.
Par défaut, seule la mémoire compte pour placer les conteneurs ; le dominant resource calculator ajoute le CPU pour que les jobs gourmands en CPU ne surchargent pas les nœuds. Mettre en cache les fichiers d'application entre jobs accélère le démarrage.

<!-- example -->

```properties
yarn.nodemanager.resource.memory-mb=114688      # 112 GB offered per node
yarn.nodemanager.resource.cpu-vcores=30
yarn.scheduler.minimum-allocation-mb=1024
yarn.scheduler.maximum-allocation-mb=32768
```

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

<!-- challenge -->

Les nœuds affichent 90 % de mémoire allouée mais 300 % de charge CPU, et les jobs rampent. Quel réglage vérifiez-vous ?

<!-- solution -->

Le resource calculator : par défaut, seule la mémoire est prise en compte, si bien que trop de conteneurs gourmands en CPU atterrissent sur un nœud. Passer au DominantResourceCalculator et fixer des vcores réalistes par conteneur.

<!-- takeaways -->

- Les conteneurs ont des tailles mémoire et CPU limitées.
- Dépasser la mémoire fait tuer le conteneur.
- Le DominantResourceCalculator planifie aussi le CPU.

### Formats de fichiers et compression

<!-- unit: Le modèle MapReduce -->

<!-- goals -->

- Expliquer map, shuffle et reduce avec le comptage de mots.
- Écrire des jobs en Java ou d'autres langages et savoir pourquoi Spark a remplacé MapReduce.

<!-- concept -->

MapReduce découpe un calcul en deux fonctions simples. Map transforme chaque enregistrement en paires clé-valeur ; le framework regroupe toutes les valeurs par clé ; reduce combine les valeurs de chaque clé en un résultat. Comme les deux fonctions travaillent sur des morceaux indépendants, le framework peut en exécuter des milliers en parallèle et relancer celles qui échouent.
La faiblesse du modèle : chaque étape écrit sur disque, et les pipelines multi-étapes deviennent des chaînes de jobs lents. Spark a gardé l'idée en conservant les données en mémoire entre étapes.

<!-- example -->

```text
input:  "to be or not to be"
map:    (to,1) (be,1) (or,1) (not,1) (to,1) (be,1)
shuffle: be→[1,1]  not→[1]  or→[1]  to→[1,1]
reduce: (be,2) (not,1) (or,1) (to,2)
```

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

<!-- challenge -->

Un pipeline de cinq jobs MapReduce tourne trois heures, surtout à écrire et lire des données intermédiaires. Que changerait un passage à Spark ?

<!-- solution -->

Spark exécute les cinq étapes en une application avec un DAG d'étapes, gardant les données intermédiaires en mémoire (ou sur disque local seulement aux shuffles) au lieu d'écrire dans HDFS entre les jobs, ce qui réduit généralement fortement la durée.

<!-- takeaways -->

- Map émet des paires clé-valeur ; reduce combine par clé.
- Parallélisme et relances viennent de tâches indépendantes.
- Le disque entre étapes rendait MapReduce lent pour les pipelines.

<!-- unit: Entrées et sorties -->

<!-- goals -->

- Expliquer InputSplits, RecordReaders et formats d'entrée/sortie.
- Gérer de nombreuses petites entrées et des commits de sortie atomiques.

<!-- concept -->

Avant qu'un mapper voie un enregistrement, le framework décide comment diviser l'entrée (des splits, généralement un par bloc) et comment transformer les octets en enregistrements (un RecordReader du format d'entrée). En sortie, un format de sortie écrit les résultats et un committer les fait apparaître d'un coup, pour que personne ne voie la moitié de la sortie d'un job.
De nombreux petits fichiers d'entrée donneraient de nombreux minuscules splits ; les combiner en splits moins nombreux garde un nombre de tâches raisonnable.

<!-- example -->

```java
job.setInputFormatClass(CombineTextInputFormat.class);
CombineTextInputFormat.setMaxInputSplitSize(job, 256L * 1024 * 1024);   // pack small files
job.setOutputFormatClass(TextOutputFormat.class);
```

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

<!-- challenge -->

Un job sur 20 000 fichiers de 100 Ko lance 20 000 tâches map et tourne lentement. Que changez-vous ?

<!-- solution -->

Utiliser `CombineFileInputFormat` (ou `CombineTextInputFormat`) pour regrouper les petits fichiers en splits de quelques centaines de Mo, afin que quelques dizaines de tâches fassent le travail. À terme, compacter les fichiers.

<!-- takeaways -->

- Les splits divisent l'entrée ; les RecordReaders produisent les enregistrements.
- Regroupez les petits fichiers en splits plus gros.
- Les committers rendent la sortie visible de façon atomique.

<!-- unit: Shuffle, combiners et partitioners -->

<!-- goals -->

- Expliquer le shuffle et le tri, et comment les combiners le réduisent.
- Contrôler partitionnement, nombre de reducers et tris secondaires.

<!-- concept -->

Le shuffle concentre l'essentiel de l'effort de MapReduce : la sortie des maps est partitionnée par clé, triée, écrite sur disque puis récupérée par les reducers via le réseau. Tout ce qui le réduit aide. Un combiner pré-agrège côté map, et bien moins de données voyagent.
Le partitionnement décide quel reducer reçoit chaque clé, et le nombre de reducers fixe le parallélisme. Des partitioners personnalisés répartissent les clés déséquilibrées ; un tri secondaire livre les valeurs au reducer déjà ordonnées.

<!-- example -->

```java
job.setMapperClass(WordMapper.class);
job.setCombinerClass(SumReducer.class);   // safe: sum is associative and commutative
job.setReducerClass(SumReducer.class);
job.setNumReduceTasks(40);
```

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

<!-- challenge -->

Un job calcule une moyenne par clé, et quelqu'un ajoute le reducer comme combiner. Les résultats sont faux. Pourquoi ?

<!-- solution -->

La moyenne n'est pas associative : faire la moyenne de moyennes partielles ignore les effectifs. Émettre (somme, compte) depuis le combiner et calculer somme/compte dans le reducer.

<!-- takeaways -->

- Le shuffle domine le coût de MapReduce.
- Les combiners réduisent la sortie map si la fonction est associative.
- Partitioners et nombre de reducers contrôlent le parallélisme.

<!-- unit: Bien exécuter les jobs -->

<!-- goals -->

- Utiliser counters, distributed cache et exécution spéculative.
- Joindre des jeux de données et dimensionner correctement les tâches.

<!-- concept -->

Quelques outils rendent les jobs observables et efficaces. Les counters rapportent ce qui s'est passé, comme les enregistrements mal formés ou les octets déversés sur disque. Le distributed cache envoie de petits fichiers de référence à chaque tâche, ce qui permet des jointures côté map avec de petites tables ; les gros jeux exigent des jointures côté reduce.
L'exécution spéculative combat les nœuds lents en lançant des doublons des tâches à la traîne. La taille des tâches compte aussi : des tâches qui finissent en quelques secondes passent l'essentiel de leur temps à démarrer.

<!-- example -->

```java
context.getCounter("quality", "MALFORMED_RECORDS").increment(1);
job.addCacheFile(new URI("/ref/country_codes.csv#countries"));  // map-side join lookup
```

#### Comment choisir entre Avro et Parquet ?

Avro pour les écritures par lignes, le streaming et les messages dont on lit les enregistrements complets et dont le schéma évolue souvent ; Parquet pour l'analytique où les requêtes lisent quelques colonnes de nombreuses lignes.

#### Qu'est-ce qu'Apache Hive ?

Un système d'entrepôt de données sur Hadoop qui permet d'interroger des données dans HDFS (et dans un stockage objet) avec un dialecte SQL (HiveQL). Les requêtes sont compilées en jobs MapReduce, Tez ou Spark, et les métadonnées des tables sont stockées dans le Hive Metastore.

#### Qu'est-ce que le Hive Metastore ?

Un service adossé à une base relationnelle (MySQL, PostgreSQL) qui stocke les définitions de tables, colonnes, partitions, emplacements et formats. Hive, Spark, Impala, Presto/Trino et d'autres l'utilisent, et l'AWS Glue Data Catalog lui est compatible.

#### Quelle différence entre tables gérées et externes dans Hive ?

Hive possède les données des tables gérées : supprimer la table supprime les fichiers. Les tables externes pointent vers des données gérées ailleurs : les supprimer n'efface que les métadonnées. Les tables externes sont courantes dans les data lakes partagés.

#### Que sont les partitions dans Hive ?

Des sous-répertoires par valeur de colonne (`/sales/dt=2026-10-15/`) ; les requêtes qui filtrent sur les colonnes de partition ne lisent que les répertoires correspondants. Le partitionnement dynamique crée les partitions à partir des résultats d'une requête.

<!-- challenge -->

Un job joint 2 To de transactions à une table de pays de 20 Mo par une jointure côté reduce, et le shuffle est énorme. Que changez-vous ?

<!-- solution -->

Utiliser une jointure côté map : distribuer la table des pays via le distributed cache, la charger en mémoire dans chaque mapper et joindre là, pour que les 2 To ne passent jamais par le shuffle.

<!-- takeaways -->

- Les counters rendent les jobs observables.
- Les petites tables se joignent côté map via le cache.
- Exécution spéculative et taille des tâches combattent la lenteur.

### Hive

<!-- unit: Spark sur YARN -->

<!-- goals -->

- Exécuter Spark sur YARN avec les données HDFS et le Hive Metastore.
- Choisir entre les modes de déploiement client et cluster.

<!-- concept -->

Spark tourne sur les clusters Hadoop comme une application YARN parmi d'autres : les executors sont des conteneurs, les données viennent de HDFS via l'API de système de fichiers de Hadoop, et les définitions de tables viennent du Hive Metastore. Cette réutilisation explique pourquoi Spark s'est imposé si facilement sur les clusters Hadoop.
L'emplacement du driver est le choix principal. En mode client, il tourne sur la machine qui soumet, pratique pour le travail interactif ; en mode cluster, il tourne dans YARN, ce dont ont besoin les jobs de production.

<!-- example -->

```bash
spark-submit \
  --master yarn --deploy-mode cluster --queue etl \
  --num-executors 20 --executor-cores 4 --executor-memory 12g \
  --conf spark.executor.memoryOverhead=2g \
  daily_orders.py --date 2026-10-17
```

#### Qu'est-ce que le bucketing dans Hive ?

La répartition des données d'une table ou d'une partition dans un nombre fixe de fichiers selon le hachage d'une colonne, ce qui permet un échantillonnage efficace et des bucket map joins quand les tables sont « bucketées » sur la clé de jointure.

#### Quels moteurs d'exécution Hive peut-il utiliser ?

MapReduce (historique, déprécié), Apache Tez (basé sur des DAG, défaut habituel de Hive 2/3) et Spark (Hive on Spark). Hive LLAP ajoute des démons persistants avec cache pour les requêtes interactives.

#### Que sont les tables ACID de Hive ?

Des tables ORC transactionnelles (les tables gérées de Hive 3) qui prennent en charge `INSERT`, `UPDATE`, `DELETE` et `MERGE` avec isolation par snapshot, grâce à des fichiers delta fusionnés par des compactions (mineures et majeures).

#### Qu'est-ce que l'optimiseur basé sur les coûts de Hive ?

Une optimisation fondée sur Apache Calcite qui utilise les statistiques de tables et de colonnes (`ANALYZE TABLE … COMPUTE STATISTICS`) pour choisir l'ordre et la stratégie des jointures ; sans statistiques, les plans peuvent être médiocres.

<!-- challenge -->

Un job Spark nocturne soumis depuis un edge node échoue chaque fois que quelqu'un redémarre ce edge node. Pourquoi, et que changez-vous ?

<!-- solution -->

Il tourne en mode client : le driver vit sur le edge node et meurt avec lui. Le soumettre en mode cluster pour que le driver tourne dans un conteneur YARN, indépendant de la machine cliente.

<!-- takeaways -->

- Spark sur YARN réutilise HDFS et le Hive Metastore.
- Mode client pour l'interactif ; mode cluster pour la production.
- Les executors sont des conteneurs YARN.

<!-- unit: Dimensionner Spark sur YARN -->

<!-- goals -->

- Dimensionner les executors et utiliser la dynamic allocation avec l'external shuffle service.
- Corriger les conteneurs tués pour dépassement de mémoire.

<!-- concept -->

Dimensionner les executors arbitre entre parallélisme et mémoire. Environ quatre ou cinq cœurs par executor gardent un bon débit HDFS ; la mémoire doit couvrir le heap plus le surcoût des workers Python, des buffers et des données hors heap, sinon YARN tue le conteneur.
La dynamic allocation fait varier le nombre d'executors avec la charge, ce qui ne marche que si les fichiers de shuffle survivent à la suppression d'executors : c'est le rôle de l'external shuffle service de chaque NodeManager.

<!-- example -->

```properties
spark.dynamicAllocation.enabled=true
spark.shuffle.service.enabled=true
spark.dynamicAllocation.minExecutors=2
spark.dynamicAllocation.maxExecutors=60
spark.executor.memoryOverhead=3g      # PySpark UDFs need off-heap room
```

#### Qu'est-ce qu'une map join dans Hive ?

Une jointure où la petite table est chargée en mémoire sur chaque mapper (broadcast), évitant le shuffle ; Hive convertit automatiquement les jointures quand la petite table est sous un seuil de taille (`hive.auto.convert.join`).

#### Comment charger des données dans des tables Hive ?

`LOAD DATA INPATH` (déplace les fichiers dans l'emplacement de la table), `INSERT INTO/OVERWRITE … SELECT`, `CREATE TABLE AS SELECT`, ou en écrivant directement des fichiers à l'emplacement d'une table externe puis en ajoutant les partitions.

#### Qu'est-ce que `MSCK REPAIR TABLE` ?

Une commande qui parcourt l'emplacement de la table à la recherche de répertoires de partition non enregistrés dans le metastore et les ajoute.

#### Que sont les SerDe dans Hive ?

Des sérialiseurs/désérialiseurs qui définissent comment les lignes sont lues et écrites : `LazySimpleSerDe` pour le texte délimité, `OpenCSVSerde`, des SerDe JSON, `RegexSerDe`, et la prise en charge intégrée d'ORC, Parquet et Avro.

<!-- challenge -->

Un job PySpark avec des UDF Python perd sans cesse des executors avec « killed by YARN for exceeding memory limits », alors que le heap JVM semble correct. Que changez-vous ?

<!-- solution -->

Augmenter `spark.executor.memoryOverhead` (les workers Python tournent hors heap), ou réduire les cœurs par executor pour que moins de workers Python se le partagent ; remplacer les UDF par des fonctions intégrées quand c'est possible.

<!-- takeaways -->

- ~4–5 cœurs par executor ; dimensionnez heap plus surcoût.
- La dynamic allocation exige l'external shuffle service.
- L'usage hors heap cause la plupart des arrêts mémoire YARN.

<!-- stage: L'écosystème -->

### HBase

<!-- unit: Hive et son metastore -->

<!-- goals -->

- Expliquer ce qu'est Hive, son metastore et ses moteurs d'exécution.
- Se connecter avec HiveServer2 et Beeline, et savoir en quoi HiveQL diffère du SQL.

<!-- concept -->

Hive a rendu Hadoop utilisable par quiconque connaissait le SQL. Les requêtes sont traduites en jobs sur un moteur d'exécution, autrefois MapReduce, aujourd'hui Tez ou Spark, et tournent sur des fichiers HDFS. Le metastore contient ce qui transforme des fichiers en tables : schémas, emplacements, partitions et formats.
Ce metastore a survécu au moteur de Hive lui-même : Spark, Trino et Impala l'utilisent tous. Les clients se connectent via HiveServer2, généralement avec Beeline ou des outils JDBC.

<!-- example -->

```bash
beeline -u "jdbc:hive2://hs2.prod:10000/default;principal=hive/_HOST@CORP.COM" \
  -e "SELECT dt, count(*) FROM sales.orders WHERE dt >= '2026-10-01' GROUP BY dt"
```

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

<!-- challenge -->

Une équipe veut que Spark et Trino voient les mêmes tables que Hive. Que partagent-ils ?

<!-- solution -->

Le Hive Metastore : configurer Spark (`enableHiveSupport` / réglages de catalogue) et le connecteur Hive de Trino pour utiliser le même metastore, afin que tous les moteurs voient les mêmes définitions de tables et partitions.

<!-- takeaways -->

- Hive traduit le SQL en jobs distribués.
- Le metastore fait des fichiers des tables pour de nombreux moteurs.
- HiveServer2 et Beeline sont les points d'entrée clients.

<!-- unit: Tables, partitions et buckets -->

<!-- goals -->

- Distinguer tables managed et external.
- Utiliser correctement partitions, buckets et insertions en partitions dynamiques.

<!-- concept -->

Les tables Hive sont des répertoires, et leur organisation pilote la performance. Les tables managed appartiennent à Hive : les supprimer efface les données ; les tables external pointent seulement vers des données appartenant à d'autres. Les partitions sont des sous-répertoires par valeur de colonne, qui laissent les requêtes ignorer tout sauf les dossiers utiles, à condition de filtrer directement sur la colonne de partition.
Les buckets découpent les données d'une partition en un nombre fixe de fichiers par hash, utile aux jointures et à l'échantillonnage. Les partitions dynamiques naissent des données et exigent des limites.

<!-- example -->

```sql
SET hive.exec.dynamic.partition.mode=nonstrict;
INSERT OVERWRITE TABLE sales.orders PARTITION (dt)
SELECT order_id, customer_id, amount, to_date(created_at) AS dt
FROM staging.orders_raw
WHERE created_at >= '2026-10-15';
```

#### Comment calcule-t-on des statistiques dans Hive ?

`ANALYZE TABLE t PARTITION (dt) COMPUTE STATISTICS` pour les statistiques de table et de partition, et `… FOR COLUMNS` pour celles des colonnes, utilisées par l'optimiseur basé sur les coûts ; `hive.stats.autogather` collecte les statistiques de base à l'insertion.

#### Qu'est-ce que l'insertion avec partitions dynamiques, et que faut-il surveiller ?

`INSERT OVERWRITE TABLE t PARTITION (dt) SELECT …, dt FROM src` crée les partitions à partir des valeurs des données. Des limites (`hive.exec.max.dynamic.partitions`) évitent de créer des milliers de partitions par accident, et de nombreuses partitions avec peu de lignes produisent de petits fichiers.

#### Qu'est-ce que HBase ?

Une base NoSQL distribuée orientée familles de colonnes, inspirée de Google Bigtable, qui tourne sur HDFS. Elle offre des lectures et écritures aléatoires en temps réel sur des milliards de lignes par clé de ligne, avec une cohérence forte par ligne.

#### Quel est le modèle de données de HBase ?

Des tables de lignes triées par clé ; chaque ligne a des familles de colonnes (définies à la création de la table), chaque famille contient un nombre quelconque de colonnes (qualifiers), et chaque cellule conserve des versions identifiées par horodatage. Les colonnes clairsemées ne coûtent rien.

#### Quels sont les principaux composants de HBase ?

Le HMaster (attribue les régions, gère les changements de schéma et l'équilibrage), les RegionServers (servent lectures et écritures des régions), les régions (plages contiguës de clés d'une table) et ZooKeeper (coordination et localisation de la table meta).

#### Comment se déroule une écriture HBase ?

Le RegionServer ajoute la modification au write-ahead log (WAL) dans HDFS pour la durabilité, puis l'écrit dans la MemStore en mémoire. Quand la MemStore est pleine, elle est vidée dans un HFile immuable sur HDFS.

<!-- challenge -->

Quelqu'un supprime une table Hive managed en pensant n'effacer que la définition. Qu'est-il advenu des données, et comment définir les données partagées ?

<!-- solution -->

Les fichiers de données ont été supprimés avec la table (sauf si la corbeille ou un snapshot les sauve). Les données partagées avec d'autres outils ou équipes doivent être en tables external, pour que la suppression de la définition laisse les fichiers intacts.

<!-- takeaways -->

- Les tables managed possèdent les données ; les external y pointent.
- Le pruning n'opère que si le filtre porte directement sur la colonne.
- Limitez les partitions dynamiques pour éviter les explosions.

<!-- unit: Charger et lire des données -->

<!-- goals -->

- Charger des données dans des tables Hive et lire des formats avec des SerDes.
- Utiliser LATERAL VIEW explode et les clauses de tri de Hive.

<!-- concept -->

Les données entrent dans Hive de quelques façons : déplacer des fichiers dans le répertoire d'une table, insérer des résultats de requête, ou définir une table external sur des fichiers existants. Les SerDes décident comment les octets deviennent des colonnes, du texte délimité au JSON ou à l'ORC.
HiveQL a aussi son vocabulaire pour les données distribuées : éclater des tableaux en lignes, et quatre clauses de tri qui diffèrent selon que l'ordre est global, par reducer, ou porte seulement sur quel reducer reçoit quelles lignes.

<!-- example -->

```sql
SELECT o.order_id, item.sku, item.qty
FROM sales.orders o
LATERAL VIEW explode(o.items) t AS item
WHERE o.dt = '2026-10-17'
DISTRIBUTE BY o.order_id SORT BY o.order_id;
```

#### Que sont les compactions dans HBase ?

Des processus d'arrière-plan qui fusionnent les HFiles : les compactions mineures fusionnent quelques petits fichiers ; les majeures réécrivent tous les fichiers d'un store en un seul en supprimant les cellules effacées et expirées. Les compactions majeures sont lourdes en E/S et souvent planifiées hors pointe.

#### Pourquoi la conception de la clé de ligne est-elle si importante dans HBase ?

Tout accès se fait par clé, et les lignes sont triées et découpées en régions par clé. Des clés croissantes (horodatages, séquences) envoient toutes les écritures vers une seule région (hotspotting). Utilisez le salage, le hachage ou l'inversion de champs, et concevez les clés selon les principaux modes d'accès.

#### Quand choisir HBase plutôt que Hive ?

HBase pour des lectures et écritures aléatoires à faible latence par clé (profils utilisateurs, recherches de séries temporelles, compteurs) ; Hive pour l'analytique SQL batch sur de grosses lectures.

#### Qu'est-ce qu'Apache Phoenix ?

Une couche SQL au-dessus de HBase qui compile le SQL en scans HBase, avec des index secondaires et un accès JDBC.

<!-- challenge -->

Une requête avec `ORDER BY` sur un milliard de lignes tourne des heures sur un seul reducer. La sortie doit seulement être triée au sein de chaque client. Qu'utilisez-vous ?

<!-- solution -->

`DISTRIBUTE BY customer_id SORT BY customer_id, event_time` : les lignes de chaque client vont au même reducer et y sont triées, en parallèle, sans tri global sur un seul reducer.

<!-- takeaways -->

- Chargez en déplaçant des fichiers, en insérant ou via des tables external.
- Les SerDes associent le contenu des fichiers aux colonnes.
- `ORDER BY` est global ; `SORT BY` et `DISTRIBUTE BY` passent à l'échelle.

<!-- unit: Performance de Hive et ACID -->

<!-- goals -->

- Accélérer Hive avec statistiques, CBO, map joins et vectorisation.
- Expliquer les tables ACID de Hive.

<!-- concept -->

L'optimiseur de Hive doit connaître la taille des tables et la distribution des valeurs pour bien planifier les jointures : les statistiques sont donc le socle de la performance. Avec elles, les petites tables deviennent des map joins diffusés à chaque tâche, ce qui évite les shuffles. La vectorisation traite les lignes par lots et exploite bien mieux le processeur.
Les tables ACID ont ajouté mises à jour et suppressions à Hive via des fichiers delta et la compaction, premier pas vers ce que les formats de table comme Iceberg offrent désormais partout.

<!-- example -->

```sql
ANALYZE TABLE sales.orders PARTITION (dt) COMPUTE STATISTICS;
ANALYZE TABLE sales.orders PARTITION (dt) COMPUTE STATISTICS FOR COLUMNS;
SET hive.cbo.enable=true;
SET hive.auto.convert.join=true;
SET hive.vectorized.execution.enabled=true;
```

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

<!-- challenge -->

Une jointure entre un gros fait et une dimension de 50 Mo fait un shuffle des deux côtés. Les statistiques n'ont jamais été calculées. Que faites-vous ?

<!-- solution -->

Calculer les statistiques de tables et de colonnes pour que l'optimiseur sache que la dimension est petite, et activer la conversion automatique en map join ; la dimension est alors diffusée et le fait n'est pas mélangé.

<!-- takeaways -->

- Les statistiques pilotent l'optimiseur par coûts.
- Les map joins diffusent les petites tables.
- Les tables ACID ajoutent mises à jour et suppressions par deltas.

### Autres outils de l'écosystème

<!-- unit: Le modèle de données HBase -->

<!-- goals -->

- Décrire le modèle de données de HBase et les column families.
- Choisir entre HBase et Hive, et connaître Apache Phoenix.

<!-- concept -->

HBase répond à une autre question que Hive : non pas « parcourir tout » mais « donne-moi cette ligne maintenant ». Ses tables sont des maps triées de row key vers column families puis cellules versionnées, conçues pour des lectures et écritures rapides par clé à très grande échelle.
Les column families sont stockées séparément : elles doivent être peu nombreuses et regrouper des données lues ensemble. Phoenix ajoute du SQL par-dessus pour les équipes qui veulent requêtes et index secondaires sans l'API brute.

<!-- example -->

```text
row key: user#00042
  cf "profile": name="Ana", city="Bogotá"
  cf "activity": last_login@t3="2026-10-17T09:01", last_login@t2="2026-10-16T21:40"
```

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

<!-- challenge -->

Une application a besoin du dernier profil de n'importe lequel de 500 millions d'utilisateurs en moins de 10 ms, tandis que les analystes veulent des agrégats hebdomadaires. Quel stockage sert quel besoin ?

<!-- solution -->

HBase (row key = ID utilisateur) pour les accès par clé à faible latence ; Hive (ou Spark sur Parquet) pour les agrégats hebdomadaires, alimentés par les mêmes données.

<!-- takeaways -->

- HBase est un stockage trié par clé aux cellules versionnées.
- Gardez peu de column families.
- HBase pour l'accès par clé ; Hive pour les parcours.

<!-- unit: Fonctionnement interne de HBase -->

<!-- goals -->

- Décrire les composants de HBase et son chemin d'écriture.
- Expliquer compactions, découpage de régions, bloom filters et TTL.

<!-- concept -->

HBase écrit vite car il ne réécrit jamais de fichiers sur place. Une écriture va dans un journal pour la durabilité et en mémoire ; la mémoire est vidée dans des fichiers immuables. Avec le temps, ces fichiers s'accumulent : les compactions les fusionnent et éliminent les données supprimées ou expirées.
Les tables sont découpées en régions par plage de clés, servies par des RegionServers et redécoupées en grandissant. Les bloom filters permettent aux lectures d'ignorer les fichiers qui ne peuvent contenir une ligne, et les TTL font expirer automatiquement les anciennes cellules.

<!-- example -->

```text
put(row) → WAL on HDFS → MemStore (memory) → flush → HFile
minor compaction: merge a few HFiles
major compaction: rewrite all HFiles of a store, drop deletes and expired cells
```

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

<!-- challenge -->

La latence de lecture explose chaque dimanche à 02:00 sur un cluster HBase. Quelle cause probable, et quelle correction ?

<!-- solution -->

Des major compactions planifiées réécrivent tous les store files et concurrencent les lectures. Désactiver les major compactions périodiques et les lancer à la main ou bridées pendant des créneaux calmes, table par table.

<!-- takeaways -->

- Les écritures vont dans le WAL et le MemStore, puis en HFiles.
- Les compactions fusionnent les fichiers et purgent l'ancien.
- Les régions se découpent par plage de clés en grandissant.

<!-- unit: Concevoir pour l'accès -->

<!-- goals -->

- Concevoir des row keys qui évitent les points chauds.
- Lire HBase efficacement avec gets, scans et filtres.

<!-- concept -->

Dans HBase, la row key est à la fois l'index, le partitionnement et l'ordre de tri. Une clé croissante dans le temps, comme un horodatage, envoie toutes les écritures vers la dernière région : un point chaud. Saler, hacher ou inverser les clés répartit les écritures, au prix de parcours par plage plus difficiles.
Les lectures suivent la même logique : récupérer une ligne par clé, parcourir des plages avec clés de début et de fin, et limiter colonnes et versions au nécessaire.

<!-- example -->

```text
bad:  20261017T090112#sensor42      → all writes hit the newest region
good: 7#sensor42#20261017T090112    → salt (hash(sensor) % 16) spreads writes
scan: start=7#sensor42#20261017  stop=7#sensor42#20261018
```

#### Qu'est-ce qu'Apache Ozone ?

Un stockage objet distribué et scalable pour Hadoop avec une API compatible S3, conçu pour dépasser les limites d'HDFS sur les petits fichiers et l'espace de noms tout en restant compatible avec les applications Hadoop.

#### Comment se fait l'authentification dans Hadoop ?

Avec Kerberos : utilisateurs et services obtiennent des tickets auprès d'un Key Distribution Center, que les services Hadoop vérifient. Sans Kerberos (mode « simple »), Hadoop fait confiance au nom d'utilisateur déclaré par le client, ce qui n'est pas sûr.

<!-- challenge -->

Une table IoT indexée par horodatage n'écrit que sur un seul RegionServer pendant que les autres restent inactifs. Repensez la clé.

<!-- solution -->

Préfixer la clé par un sel ou l'ID de l'appareil (par exemple `hash(device) % N # device # timestamp`), pour répartir les écritures entre régions tout en gardant les parcours d'un appareil sous forme de plages.

<!-- takeaways -->

- La row key décide de la distribution et de l'accès.
- Les clés monotones créent des points chauds d'écriture.
- Utilisez gets et scans bornés avec filtres.

### Sécurité et gouvernance

<!-- unit: Coordination et orchestration -->

<!-- goals -->

- Expliquer le rôle de ZooKeeper dans la coordination des services Hadoop.
- Décrire Oozie, Ambari et Livy.

<!-- concept -->

Les services distribués doivent se mettre d'accord : qui est le maître actif, quels nœuds sont vivants, quelle est la configuration en vigueur. ZooKeeper fournit cet état partagé petit et fiable, et de nombreux composants Hadoop en dépendent pour le basculement.
Autour du cluster, d'autres outils gèrent le travail et l'exploitation : Oozie planifie des workflows de jobs Hadoop, Ambari installe et supervise les services, et Livy permet aux applications de soumettre des jobs Spark via REST.

<!-- example -->

```text
ZooKeeper ensemble (3 or 5 nodes)
 ├─ NameNode HA: ZKFC elects the active NameNode
 ├─ ResourceManager HA leader election
 └─ HBase: active HMaster, RegionServer membership
```

#### Que sont les delegation tokens ?

Des jetons émis par les services (NameNode, ResourceManager) après une authentification Kerberos, transmis aux tâches exécutées sur le cluster pour qu'elles accèdent à HDFS sans disposer elles-mêmes d'identifiants Kerberos.

#### Comment gère-t-on les droits HDFS ?

Avec des droits de type POSIX propriétaire/groupe/autres sur fichiers et répertoires, plus des ACL pour un contrôle plus fin. Les politiques fines et centralisées sont généralement gérées avec Apache Ranger.

#### Qu'est-ce qu'Apache Ranger ?

Un framework de sécurité centralisé pour Hadoop qui définit et audite des politiques d'accès (chemins HDFS, bases, tables et colonnes Hive, filtres de lignes et masquage, HBase, Kafka) avec des plugins qui les appliquent dans chaque service.

#### Qu'est-ce qu'Apache Atlas ?

Un service de métadonnées et de gouvernance qui fournit catalogue de données, lignage, classification (tags comme PII) et intégration avec Ranger pour des politiques fondées sur les tags.

<!-- challenge -->

Pourquoi un ensemble ZooKeeper compte-t-il trois ou cinq nœuds, jamais deux ou quatre ?

<!-- solution -->

Il lui faut une majorité (quorum) pour fonctionner. Trois nœuds tolèrent une panne et cinq en tolèrent deux ; quatre n'en tolère qu'une, comme trois, et deux aucune : les nombres pairs ajoutent du coût sans résilience.

<!-- takeaways -->

- ZooKeeper fournit coordination et élection de leader.
- Oozie planifie les workflows Hadoop.
- Ambari administre les clusters ; Livy soumet Spark en REST.

<!-- unit: Outils d'ingestion -->

<!-- goals -->

- Décrire le rôle de Sqoop, Flume et Kafka dans les architectures Hadoop.
- Choisir une voie d'ingestion pour bases de données, journaux et événements.

<!-- concept -->

Les données arrivaient dans Hadoop par des outils spécialisés. Sqoop transférait des tables entre bases relationnelles et HDFS avec des jobs parallèles. Flume collectait des lignes de journaux sur de nombreux serveurs et les livrait par lots. Kafka est devenu le tampon durable entre producteurs et tout l'aval.
Sqoop et Flume sont retirés ou rarement choisis aujourd'hui, remplacés par Spark JDBC, des outils de CDC et des connecteurs Kafka, mais leurs motifs demeurent.

<!-- example -->

| Source | Outil classique | Équivalent moderne |
|---|---|---|
| Tables de bases relationnelles | Sqoop | Spark JDBC, CDC (Debezium) |
| Fichiers journaux de serveurs | Flume | Kafka + connecteurs, Fluent Bit |
| Flux d'événements | Kafka | Kafka |

#### Qu'est-ce qu'Apache Knox ?

Une passerelle qui offre un point d'entrée unique et sécurisé (API REST, interfaces) aux services Hadoop pour les utilisateurs hors du cluster, en gérant l'authentification et le SSL.

#### Comment les données sont-elles chiffrées dans Hadoop ?

En transit avec le chiffrement RPC, TLS pour les interfaces web et le chiffrement du transfert de données ; au repos avec le chiffrement transparent HDFS par zones de chiffrement dont les clés sont gérées par le Hadoop Key Management Server (KMS).

#### Qu'est-ce qu'un keytab ?

Un fichier contenant les clés d'un principal Kerberos, utilisé par les services et les jobs batch pour s'authentifier sans mot de passe ; les keytabs doivent être protégés comme des mots de passe.

<!-- challenge -->

Un cluster importe encore une base chaque nuit avec Sqoop, qui n'est plus maintenu. Par quoi le remplacez-vous ?

<!-- solution -->

Un job Spark JDBC qui lit en parallèle par plages de clés (ou un outil de CDC pour les changements incrémentaux), écrit des partitions Parquet ou ORC, et est planifié par l'orchestrateur existant.

<!-- takeaways -->

- Sqoop déplaçait les bases ; Flume, les journaux.
- Kafka découple producteurs et consommateurs.
- Les stacks modernes utilisent Spark JDBC, CDC et connecteurs.

<!-- unit: Moteurs de traitement et de requête -->

<!-- goals -->

- Comparer Pig, Tez, Impala et Trino avec Spark.
- Décrire la place de Spark et d'Ozone sur les clusters Hadoop.

<!-- concept -->

Les moteurs sur Hadoop ont évolué pour réduire la surcharge de MapReduce. Pig offrait un langage de scripts compilé en jobs. Tez exécutait une requête entière comme un seul graphe au lieu de jobs chaînés. Impala et Trino utilisaient des démons permanents pour du SQL interactif sans démarrage de job. Spark a tout généralisé avec le traitement en mémoire.
Le stockage a évolué aussi : Ozone apporte aux clusters Hadoop un stockage objet avec API S3, ce qui allège les limites des petits fichiers et du NameNode.

<!-- example -->

| Moteur | Style | Usage type |
|---|---|---|
| Pig (retiré) | Scripts de flux de données | ETL historique |
| Hive sur Tez | SQL en DAG | SQL batch |
| Impala / Trino | Démons MPP | SQL interactif |
| Spark | DAG, en mémoire | ETL, ML, SQL |

#### Qu'est-ce que l'usurpation contrôlée (proxy users) dans Hadoop ?

Une configuration qui permet à un service de confiance (HiveServer2, Livy, Oozie) d'agir au nom des utilisateurs finaux, pour que les droits et les audits reflètent l'utilisateur réel et non le compte de service.

#### Comment auditer les accès dans Hadoop ?

Les journaux d'audit HDFS du NameNode enregistrent chaque accès aux fichiers ; Ranger collecte les événements d'audit de tous ses plugins dans Solr ou HDFS, et Atlas enregistre le lignage.

#### Comment dimensionner un cluster Hadoop ?

À partir du volume de données (taille brute × facteur de réplication × croissance, plus l'espace temporaire), des besoins de traitement (CPU et mémoire pour les jobs simultanés) et des objectifs de débit ; en gardant de la marge pour les pannes et le rééquilibrage (on garde souvent les disques sous 70 à 80 %).

#### Quelles sont les causes fréquentes de jobs Hadoop lents ?

Le déséquilibre des données (quelques reducers avec la plupart des clés), trop de petits fichiers, un parallélisme insuffisant ou excessif, des déversements sur disque dus à des tampons mémoire trop petits, des entrées compressées non découpables, l'absence de localité et la contention dans les files YARN.

#### Comment régler la mémoire de MapReduce ?

Fixer `mapreduce.map.memory.mb` et `mapreduce.reduce.memory.mb` pour la taille des conteneurs et `-Xmx` dans `mapreduce.map.java.opts` à environ 80 % du conteneur, et ajuster `mapreduce.task.io.sort.mb` pour réduire les déversements.

<!-- challenge -->

Les analystes se plaignent que chaque requête Hive met 30 secondes à démarrer, même les plus simples. Que leur proposez-vous ?

<!-- solution -->

Un moteur interactif à démons permanents (Impala ou Trino) sur le même metastore et les mêmes fichiers, pour les requêtes ad hoc ; garder Hive sur Tez ou Spark pour les gros jobs batch.

<!-- takeaways -->

- Tez exécute une requête comme un seul DAG.
- Impala et Trino servent le SQL interactif.
- Ozone ajoute un stockage objet de type S3 à Hadoop.

<!-- stage: Exploiter Hadoop -->

### Exploitation et performances

<!-- unit: Authentification Kerberos -->

<!-- goals -->

- Expliquer l'authentification Kerberos, les keytabs et les delegation tokens.
- Configurer l'usurpation d'identité pour les services de confiance.

<!-- concept -->

Par défaut, Hadoop croit le nom d'utilisateur annoncé par le client, ce qui n'offre aucune sécurité. Kerberos corrige cela : utilisateurs et services prouvent leur identité avec des tickets d'une autorité centrale. Les jobs batch s'authentifient avec des fichiers keytab plutôt qu'avec des mots de passe.
Les jobs distribués ajoutent une difficulté : des milliers de tâches ne peuvent pas contacter chacune le serveur Kerberos, donc les services distribuent des delegation tokens après la première authentification. Des services de confiance comme HiveServer2 agissent au nom des utilisateurs par usurpation d'identité.

<!-- example -->

```bash
kinit -kt /etc/security/keytabs/etl.keytab etl@CORP.COM
klist
hdfs dfs -ls /data/finance
```

#### Comment traiter le déséquilibre des données dans les jobs Hadoop ?

Avec des combiners, des partitioners personnalisés, le salage des clés chaudes, des jointures côté map pour les petites tables, les optimisations de skew join de Hive (`hive.optimize.skewjoin`) ou une pré-agrégation.

#### Comment superviser un cluster Hadoop ?

Avec les interfaces web du NameNode et du ResourceManager, les métriques JMX, Cloudera Manager (ou historiquement Ambari), des exporteurs Prometheus et Grafana, et des alertes sur la capacité HDFS, les nœuds morts ou lents, les blocs sous-répliqués, le heap du NameNode, la latence RPC et l'usage des files.

#### Comment mettre à jour un cluster Hadoop ?

Planifier avec les notes de version et des vérifications de compatibilité, sauvegarder les métadonnées du NameNode, utiliser les mises à jour progressives (rolling) quand c'est possible (NameNodes en HA, DataNodes un par un), tester les jobs sur un cluster de préproduction et garder la possibilité de revenir en arrière jusqu'à la finalisation.

#### Comment sauvegarder HDFS ?

Avec des snapshots pour les erreurs utilisateur, `distcp` vers un autre cluster ou un stockage objet pour la reprise après sinistre, et des sauvegardes des métadonnées du NameNode (`fsimage` et edits). La réplication interne au cluster n'est pas une sauvegarde.

<!-- challenge -->

Un job nocturne échoue après des mois sans souci, avec « GSS initiate failed ». Que vérifiez-vous ?

<!-- solution -->

Les identifiants Kerberos : la validité du keytab (mot de passe ou version de clé changés), l'expiration du ticket avant renouvellement, et le décalage d'horloge entre le nœud et le KDC.

<!-- takeaways -->

- Kerberos prouve les identités par des tickets.
- Les keytabs authentifient jobs batch et services.
- Delegation tokens et proxy users font passer l'authentification à l'échelle.

<!-- unit: Autorisation, chiffrement et audit -->

<!-- goals -->

- Gérer les permissions avec les ACL HDFS et Ranger.
- Chiffrer les données et auditer les accès avec Atlas, Knox et les journaux d'audit.

<!-- concept -->

Une fois les identités connues, il faut décider des accès. Permissions et ACL HDFS fonctionnent par fichier et répertoire ; Ranger centralise les politiques pour HDFS, Hive, HBase et d'autres, y compris masquage de colonnes et filtrage de lignes, avec audit de chaque décision.
Autour se placent le chiffrement en transit et au repos, une passerelle qui masque les endpoints du cluster aux utilisateurs, et un catalogue de gouvernance avec lignage et classifications capables de piloter les politiques.

<!-- example -->

```text
Ranger policy "finance_read":
  resource: Hive db=finance, table=*, column=*
  allow: group finance-analysts → SELECT
  mask: column=iban → partial mask (show last 4)
Atlas tag PII on finance.customers.iban → tag-based policy applies everywhere
```

#### Quel est l'impact du garbage collector de la JVM sur les services Hadoop ?

De longues pauses de GC sur le NameNode ou les RegionServers les rendent muets, provoquant timeouts, basculements ou heartbeats manqués. Dimensionnez soigneusement les heaps, utilisez des collecteurs modernes (G1) et surveillez les journaux de GC.

#### Comment trouver les jobs qui consomment le plus de ressources du cluster ?

L'interface et les API du ResourceManager YARN (mémoire-secondes et vcore-secondes par application), les métriques des files, les history servers Spark et MapReduce, et les rapports d'usage des outils de gestion.

#### Comment nettoyer un cluster qui manque d'espace ?

Repérer les répertoires volumineux et anciens (`hdfs dfs -du -h`), vider la corbeille, supprimer les données temporaires obsolètes et les vieux snapshots, réduire la réplication des données froides ou appliquer l'erasure coding, compresser ou convertir en formats en colonnes, et ajouter de la capacité si nécessaire.

#### À quoi sert `mapreduce.job.reduce.slowstart.completedmaps` ?

Il fixe la fraction de maps qui doivent être terminés avant que les reducers commencent à récupérer les sorties ; démarrer les reducers trop tôt gaspille des slots en attente, trop tard retarde le shuffle.

#### Comment HDFS se compare-t-il à Amazon S3 ?

HDFS couple stockage et calcul sur les mêmes nœuds, offre la localité des données et une cohérence forte, et exige de gérer un cluster. S3 est un stockage objet géré, scalable indépendamment, moins cher et très durable, accessible par le réseau ; il est aujourd'hui lui aussi fortement cohérent. La plupart des data lakes cloud utilisent le stockage objet plutôt que HDFS.

#### Qu'est-ce que le connecteur S3A ?

Le connecteur de système de fichiers Hadoop (`s3a://`) qui permet à Hadoop, Hive et Spark de lire et écrire S3 comme un système de fichiers, avec des optimisations pour les envois multipart, des committers qui évitent les renommages lents et des fournisseurs d'identifiants.

<!-- challenge -->

Les auditeurs demandent qui a lu une table Hive sensible au cours des 90 derniers jours. D'où vient la réponse ?

<!-- solution -->

Des journaux d'audit Ranger pour la table Hive (utilisateur, heure, action, décision de politique), complétés par les journaux d'audit du NameNode HDFS pour les lectures directes de fichiers à son emplacement.

<!-- takeaways -->

- Ranger centralise politiques, masquage et audit.
- Atlas classifie les données et suit le lignage.
- Chiffrez en transit et au repos ; Knox protège l'accès au cluster.

### Hadoop et le cloud

<!-- unit: Dimensionnement et supervision -->

<!-- goals -->

- Dimensionner un cluster Hadoop selon les données et la charge.
- Surveiller services, jobs et santé des JVM.

<!-- concept -->

Le dimensionnement part des données : volume brut × réplication × croissance, plus de la place pour les données temporaires. Le calcul découle des charges et de leurs échéances. Un cluster sous-dimensionné échoue par manque de capacité ; un cluster surdimensionné gaspille de l'argent, et sur site le matériel met des mois à arriver.
La supervision couvre les deux niveaux : les services, comme le heap du NameNode, les blocs manquants et les pauses de garbage collection, et les jobs, comme l'usage des ressources par file et par application.

<!-- example -->

```text
raw data 400 TB × 3 replicas = 1.2 PB
+ 25% temporary/shuffle space    = 1.5 PB
+ 30% yearly growth, 2 years     ≈ 2.5 PB raw disk
```

#### Pourquoi les renommages posent-ils problème sur un stockage objet ?

Les stockages objet n'ont pas de vrais répertoires ; un « renommage » est une copie suivie d'une suppression de chaque objet, ce qui est lent et non atomique. Les committers de sortie Hadoop qui reposent sur des renommages sont lents ou dangereux sur S3 ; on utilise les committers S3A (magic, staging) ou des formats de table (Iceberg, Delta).

#### Qu'est-ce qu'Amazon EMR ?

Une plateforme big data gérée sur AWS qui exécute Hadoop, Spark, Hive, HBase, Presto/Trino, Flink et d'autres sur EC2, EKS ou en serverless, avec S3 (EMRFS/S3A) comme stockage principal et le Glue Data Catalog comme metastore, en clusters éphémères ou persistants.

#### Qu'est-ce qu'un cluster éphémère ?

Un cluster créé pour un job ou un pipeline puis arrêté, les données étant conservées dans un stockage objet. On évite de payer des clusters inactifs et les environnements deviennent reproductibles.

#### Comment migrer un data lake Hadoop vers le cloud ?

Inventorier données, jobs et dépendances ; copier les données vers le stockage objet avec `distcp` ou des services de transfert ; convertir les tables en formats ouverts (Parquet, puis Iceberg ou Delta) ; passer le metastore à un catalogue géré (Glue, Unity Catalog) ; porter les jobs Hive et MapReduce vers Spark ou des moteurs SQL ; remplacer Oozie par Airflow ; recréer la sécurité avec l'IAM cloud et les droits du catalogue ; et valider les résultats en parallèle avant de décommissionner.

<!-- challenge -->

Le NameNode ne répond plus pendant 30 secondes plusieurs fois par jour, suivi de basculements. Que regardez-vous ?

<!-- solution -->

Les journaux de garbage collection de la JVM et l'usage du heap : de longues pauses de full GC sur un gros heap. Ajuster le collecteur et la taille du heap, réduire les métadonnées (moins de petits fichiers) et surveiller les durées de pause GC.

<!-- takeaways -->

- Dimensionnez par données × réplication × croissance.
- Surveillez services et jobs séparément.
- Les longues pauses GC déstabilisent les services maîtres.

<!-- unit: Jobs lents et déséquilibre -->

<!-- goals -->

- Diagnostiquer les jobs Hadoop lents et régler la mémoire MapReduce.
- Gérer le déséquilibre des données et le démarrage des reducers.

<!-- concept -->

Les jobs lents ont généralement peu de causes : des clés déséquilibrées qui surchargent un reducer, trop de petits fichiers, de mauvais réglages mémoire, ou la contention avec d'autres charges dans les mêmes files. Comparer les durées des tâches désigne la cause : une tâche longue signale un déséquilibre, des milliers de minuscules tâches des petits fichiers, des tâches tuées un problème de mémoire.
Le moment où démarrent les reducers compte aussi : les lancer tôt fait se chevaucher le travail mais peut immobiliser des conteneurs pendant que les maps se terminent.

<!-- example -->

```properties
mapreduce.map.memory.mb=4096
mapreduce.map.java.opts=-Xmx3276m          # ~80% of the container
mapreduce.reduce.memory.mb=8192
mapreduce.reduce.java.opts=-Xmx6553m
mapreduce.job.reduce.slowstart.completedmaps=0.80
```

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

<!-- challenge -->

199 reducers d'un job finissent en 5 minutes et un seul tourne 2 heures. Que se passe-t-il, et quelles sont deux corrections ?

<!-- solution -->

Un déséquilibre des données : une clé concentre la plupart des enregistrements. Utiliser un combiner pour la réduire, saler la clé chaude sur plusieurs reducers puis fusionner, ou traiter la clé chaude à part (par exemple par une jointure côté map).

<!-- takeaways -->

- Une tâche longue : déséquilibre ; des milliers de minuscules : petits fichiers.
- Dimensionnez le heap à environ 80 % du conteneur.
- Le slowstart arbitre entre reducers précoces et conteneurs inactifs.

<!-- unit: Capacité, sauvegardes et mises à niveau -->

<!-- goals -->

- Libérer de l'espace et protéger les données HDFS par des sauvegardes.
- Planifier des mises à niveau de cluster sûres.

<!-- concept -->

Manquer d'espace est une urgence lente : les écritures commencent à échouer dans tout le cluster. Les remèdes : nettoyer tout de suite (corbeille, données temporaires, réplication des données froides) et fixer des règles ensuite (quotas, rétention, archivage vers un stockage moins cher).
Les sauvegardes suivent la même logique qu'ailleurs : snapshots pour les erreurs d'utilisateurs, copies vers un autre cluster ou le stockage objet pour les sinistres. Les mises à niveau se planifient comme des migrations, avec sauvegarde des métadonnées, rolling upgrades quand c'est possible et retour arrière testé.

<!-- example -->

```bash
hdfs dfs -du -h / | sort -h | tail -20          # biggest directories
hdfs dfs -expunge                               # empty trash
hdfs dfs -setrep -w 2 /data/archive/2023        # less replication on cold data
hadoop distcp /data/finance s3a://dr-bucket/finance   # disaster copy
```

#### En quoi les coûts diffèrent-ils entre Hadoop on-premise et data lakes cloud ?

Les clusters on-premise ont des coûts fixes élevés (matériel, centres de données, équipes) et sont dimensionnés pour les pics ; les lakes cloud ont un stockage et un calcul payés à l'usage qui peuvent descendre à zéro, mais exigent une gouvernance des coûts pour éviter les dérives.

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

<!-- challenge -->

Un administrateur a supprimé par erreur un répertoire de production avec `-skipTrash`. Quelles protections auraient pu le sauver ?

<!-- solution -->

Un snapshot HDFS du répertoire (restauration depuis `.snapshot`), ou une sauvegarde `distcp` récente ailleurs. Restreindre aussi l'usage de `-skipTrash` et l'accès en écriture à la production aux comptes de service.

<!-- takeaways -->

- Nettoyez tout de suite ; imposez quotas et rétention ensuite.
- Snapshots pour les erreurs ; copies pour les sinistres.
- Mettez à niveau avec sauvegardes et plan de retour arrière.

### Spark sur Hadoop

<!-- unit: HDFS face au stockage objet -->

<!-- goals -->

- Comparer HDFS et S3, et expliquer le connecteur S3A et EMRFS.
- Expliquer pourquoi les renommages posent problème sur le stockage objet.

<!-- concept -->

HDFS couple stockage et calcul : la localité des données est rapide, mais on fait grandir les deux ensemble et on paie la capacité inutilisée. Le stockage objet les sépare : quasi illimité, bon marché et durable, accessible par le réseau depuis autant de clusters qu'on veut.
Les outils Hadoop y accèdent via des connecteurs, mais un stockage objet n'est pas un système de fichiers. Renommer un répertoire, ce que font les jobs Hadoop pour valider leur sortie, devient une copie suivie d'une suppression lente de chaque objet : il faut des committers conçus pour le stockage objet.

<!-- example -->

| | HDFS | S3 |
|---|---|---|
| Passage à l'échelle | Stockage + calcul ensemble | Indépendant |
| Renommage | Changement atomique de métadonnées | Copie + suppression par objet |
| Durabilité | Réplication ×3 | 11 neuf, géré |
| Modèle de coût | Matériel, toujours allumé | Au Go-mois |

#### Qu'est-ce que l'allocation dynamique de Spark sur YARN ?

Une fonction où Spark demande et libère des executors selon les tâches en attente, pour que les executors inactifs rendent leurs ressources à YARN ; elle nécessite le service de shuffle externe (ou le suivi du shuffle) pour que les fichiers de shuffle survivent à la suppression des executors.

#### Qu'est-ce que le service de shuffle externe ?

Un service exécuté dans chaque NodeManager qui sert les fichiers de shuffle écrits par les executors, pour que ceux-ci puissent être supprimés (allocation dynamique) ou tomber en panne sans perdre leur sortie de shuffle.

#### Comment choisir la taille des executors sur YARN ?

Équilibrer cœurs et mémoire : environ 4 à 5 cœurs par executor pour un bon débit HDFS, une mémoire par cœur adaptée à la charge, de l'overhead pour les besoins hors heap, et des ressources laissées au NodeManager et au système sur chaque nœud.

#### Le NameNode manque de mémoire heap. Que faites-vous ?

À court terme, j'augmente le heap et je redémarre pendant une fenêtre de maintenance (avec la HA, je bascule). À long terme, je réduis le nombre d'objets : trouver et compacter les petits fichiers, supprimer les données inutilisées et les vieux snapshots, utiliser des fichiers HAR, et envisager la fédération ou des observer NameNodes.

<!-- challenge -->

Un job Spark qui écrit sur S3 passe 20 minutes en « committing » après la fin des tâches. Pourquoi, et que changez-vous ?

<!-- solution -->

Le file output committer par défaut renomme la sortie temporaire, ce qui sur S3 signifie copie plus suppression par fichier. Utiliser un committer optimisé pour S3 (les committers magic/directory de S3A ou le committer optimisé d'EMR), ou écrire dans un format de table.

<!-- takeaways -->

- Le stockage objet sépare stockage et calcul.
- S3A et EMRFS relient les outils Hadoop à S3.
- Les renommages sont lents sur le stockage objet ; utilisez des committers adaptés.

<!-- unit: Clusters managés et éphémères -->

<!-- goals -->

- Décrire EMR, Dataproc et HDInsight ainsi que les clusters éphémères.
- Comparer les coûts avec Hadoop sur site et Hadoop sur Kubernetes.

<!-- concept -->

Les services managés exploitent pour vous l'écosystème Hadoop sur des machines cloud, et changent l'usage des clusters. Au lieu d'un cluster permanent dimensionné pour le pic, on peut démarrer un cluster pour un job, lire et écrire dans le stockage objet, puis l'éteindre, en ne payant que pendant son exécution.
Les coûts passent ainsi du matériel fixe à l'usage. Certaines briques tournent désormais sur Kubernetes, notamment Spark, Trino et le metastore.

<!-- example -->

```bash
aws emr create-cluster --name nightly-etl --release-label emr-7.3.0 \
  --applications Name=Spark Name=Hive --instance-type m7g.2xlarge --instance-count 10 \
  --steps Type=Spark,Name=etl,Args=[s3://code/etl.py,--date,2026-10-17] \
  --auto-terminate
```

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

<!-- challenge -->

Un cluster cloud tourne 24 h/24 mais ne traite des jobs que 4 heures par nuit. Comment réduire les coûts ?

<!-- solution -->

Garder les données dans le stockage objet et passer à des clusters éphémères démarrés pour les jobs nocturnes puis arrêtés (ou un autoscaling proche de zéro), avec des instances spot pour les nœuds de tâches.

<!-- takeaways -->

- Les services managés exploitent les outils Hadoop dans le cloud.
- Les clusters éphémères ne coûtent que pendant les jobs.
- Les coûts passent du matériel fixe à l'usage.

<!-- unit: Au-delà de Hadoop -->

<!-- goals -->

- Faire correspondre les composants Hadoop à leurs remplaçants modernes.
- Expliquer en quoi les formats de table ouverts améliorent les tables Hive.

<!-- concept -->

La plupart des briques Hadoop ont des successeurs de l'ère cloud : le stockage objet pour HDFS, Kubernetes ou le serverless pour YARN, Spark pour MapReduce. Les tables Hive évoluent en formats de table ouverts qui ajoutent transactions, évolution de schéma et time travel sur les mêmes fichiers Parquet, corrigeant les problèmes de listage de partitions et de cohérence de Hive.
Migrer un lac Hadoop consiste donc moins à copier des fichiers qu'à choisir le successeur adapté à chaque charge.

<!-- example -->

```sql
-- Spark: migrate a Hive Parquet table to Iceberg in place
CALL spark_catalog.system.migrate('sales.orders');
-- or snapshot it first to test without touching the original
CALL spark_catalog.system.snapshot('sales.orders', 'sales.orders_iceberg_test');
```

#### Un job écrit 50 000 petits fichiers par jour dans HDFS. Quelle est votre correction ?

Faire un repartition ou un coalesce avant l'écriture pour produire des fichiers proches de la taille de bloc, lancer des jobs de compaction périodiques sur les anciennes partitions, envisager un format de table qui compacte, et alerter sur le nombre de fichiers par répertoire.

#### Les utilisateurs se plaignent que le cluster Hive est lent chaque matin à 9 h. Que vérifiez-vous ?

La configuration et la contention des files (ETL qui déborde sur les heures ouvrées), de grosses requêtes ad hoc sans filtre de partition, la charge de HiveServer2 et du metastore, des statistiques manquantes, et le besoin éventuel de LLAP ou de capacité supplémentaire pour les utilisateurs interactifs.

#### HDFS est plein à 90 % et continue de croître. Que faites-vous à court et à long terme ?

À court terme : supprimer les données temporaires et la corbeille, réduire la réplication des données froides, imposer des quotas. À long terme : hiérarchiser les données (erasure coding, stockage archive), déplacer les données froides vers un stockage objet, compresser et convertir en formats en colonnes, appliquer des politiques de rétention et planifier la capacité.

<!-- challenge -->

Une table Hive compte 200 000 partitions, et la planification des requêtes prend des minutes à les lister. En quoi un format de table ouvert aiderait-il ?

<!-- solution -->

Iceberg (ou Delta) garde les métadonnées de fichiers et de partitions dans ses propres manifests avec statistiques : la planification lit des fichiers de métadonnées au lieu de lister répertoires et metastore, et élague les fichiers par statistiques.

<!-- takeaways -->

- Stockage objet, Kubernetes et Spark remplacent HDFS, YARN et MapReduce.
- Les formats de table ouverts améliorent les tables Hive.
- Migrer, c'est choisir un successeur par charge.

<!-- stage: Tout assembler -->

### Mises en situation

<!-- unit: Ingérer une base de données dans le lac -->

<!-- goals -->

- Concevoir une ingestion relationnelle quotidienne vers un lac Hadoop.
- Combiner extraction parallèle, formats, partitions et tables.

<!-- concept -->

Les questions d'ingestion vérifient votre capacité à relier stockage, calcul et métadonnées. Une bonne réponse extrait efficacement sans pénaliser la source, écrit des fichiers colonnaires de bonne taille dans des partitions par date, les enregistre comme tables et rend les relances sûres. Elle couvre ensuite contrôles et planification, et se demande si le CDC serait préférable aux extractions complètes.

<!-- example -->

```text
Spark JDBC (16 parallel reads by id range) ─► Parquet, dt=2026-10-17, ~256 MB files
  ─► INSERT OVERWRITE partition (idempotent) ─► Hive Metastore table
  ─► row-count check vs source ─► Oozie/Airflow schedule, alerts
```

#### Vous devez migrer 500 tables Hive vers un lakehouse dans le cloud. Comment le planifier ?

Classer les tables par taille, usage et dépendances ; copier les données avec `distcp` vers le stockage objet ; convertir en Iceberg ou Delta (procédures de migration sur place ou `CTAS`) ; les enregistrer dans le nouveau catalogue ; traduire les jobs HiveQL en Spark SQL ou dbt ; migrer par vagues et par domaine en validant comptages et sommes de contrôle, et garder l'ancien cluster en lecture seule jusqu'à la bascule des consommateurs.

<!-- challenge -->

La table source atteint 2 milliards de lignes et l'extraction complète quotidienne ne tient plus dans la fenêtre. Que changez-vous ?

<!-- solution -->

Passer à l'extraction incrémentale : CDC depuis le journal de la base (ou extractions par `updated_at` avec recouvrement), en appliquant les changements à un format de table avec `MERGE`, plus un rapprochement complet périodique.

<!-- takeaways -->

- Extrayez en parallèle sans surcharger la source.
- Écrivez des fichiers colonnaires bien dimensionnés en partitions.
- Rendez les chargements idempotents ; envisagez le CDC quand les volumes croissent.

<!-- unit: Migrer des tables Hive vers un lakehouse -->

<!-- goals -->

- Planifier la migration de centaines de tables Hive vers le cloud.
- Ordonner copie, conversion, validation et bascule.

<!-- concept -->

Migrer un parc Hive est un programme, pas un job de copie. Les tables diffèrent par taille, usage et dépendances : le plan les classe, déplace les données par vagues, convertit vers le format et le catalogue cibles, porte les jobs et valide les résultats avant de basculer les consommateurs. Retirer en chemin les tables inutilisées réduit le travail.

<!-- example -->

| Vague | Tables | Approche |
|---|---|---|
| 0 | Inutilisées (aucune lecture en 90 jours) | Archiver, ne pas migrer |
| 1 | Petites, peu de consommateurs | Copier + convertir, validation rapide |
| 2 | Grosses, critiques | distcp, Iceberg/Delta, exécution en parallèle |
| 3 | Dépendances complexes | Porter les jobs, basculer ensemble |

#### Un basculement du NameNode survient et certains jobs échouent. Pourquoi, et comment l'éviter ?

Les clients configurés avec l'adresse d'un seul NameNode au lieu du nameservice HA échouent ; les jobs en pleine opération de métadonnées peuvent recevoir des erreurs. Utilisez le nameservice logique (`hdfs://nameservice1`) avec des proxies de basculement côté client, et des relances dans les applications.

<!-- challenge -->

Pendant l'exécution en parallèle, une table migrée affiche 0,1 % de lignes en moins que Hive sur certaines partitions. Comment trouver la cause ?

<!-- solution -->

Comparer par partition, puis par clé, pour trouver les lignes manquantes ; causes typiques : fichiers écrits après la copie (resynchroniser avec `distcp -update`), différences de fuseau horaire dans les valeurs de partition, et enregistrements rejetés par le parsing du nouveau job.

<!-- takeaways -->

- Classez les tables ; migrez par vagues.
- Retirez les tables inutilisées au lieu de les déplacer.
- Exécutez en parallèle et rapprochez avant la bascule.
