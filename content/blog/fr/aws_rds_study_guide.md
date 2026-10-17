## Fiche d'étude Amazon RDS

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude Amazon RDS : environ 200 questions](../../images/aws_rds_study_guide_title_img.png)

Environ 200 questions d'entretien sur Amazon RDS et Aurora : moteurs, choix d'instance et de stockage, haute disponibilité avec Multi-AZ, réplicas en lecture, sauvegardes et restaurations, sécurité, supervision, performances, montée en charge, coûts, migrations, et la façon dont les data engineers extraient les données de RDS par CDC, exports et zero-ETL. Les réponses décrivent le service tel qu'il est en 2026. Ouvrez une question pour voir sa réponse, ou utilisez le filtre pour chercher dans toute la fiche.

<!-- QA -->

### Fondamentaux

#### Qu'est-ce qu'Amazon RDS ?

Amazon Relational Database Service : un service géré pour exécuter des bases de données relationnelles sur AWS. AWS prend en charge le provisionnement, les correctifs, les sauvegardes, la supervision, le basculement et le stockage, tandis que vous choisissez le moteur, la taille d'instance et la configuration, et gérez les schémas, les requêtes et les utilisateurs.

#### Quels moteurs de base de données RDS prend-il en charge ?

MySQL, PostgreSQL, MariaDB, Oracle, Microsoft SQL Server et IBM Db2, ainsi qu'Amazon Aurora (compatible MySQL et PostgreSQL), qui fait partie de la famille RDS mais possède sa propre architecture de stockage.

#### Que gère AWS dans RDS, et que gérez-vous encore ?

AWS gère le matériel, l'installation et les correctifs du système d'exploitation, l'installation du logiciel de base de données et ses versions mineures, les sauvegardes automatiques, le stockage, la réplication et le basculement Multi-AZ, et les métriques de supervision. Vous gérez la conception de la base, les requêtes et les index, les utilisateurs et privilèges, le réglage des paramètres, les règles des groupes de sécurité, les choix de capacité et la gestion des connexions applicatives.

#### Qu'est-ce qu'une instance de base de données (DB instance) ?

Un environnement de base de données isolé dans le cloud : une classe d'instance de calcul (CPU et mémoire) avec du stockage associé, qui exécute une version d'un moteur et est accessible via un endpoint (nom DNS et port).

#### Qu'est-ce qu'une classe d'instance ?

La capacité de calcul et de mémoire d'une instance : à performances extensibles (burstable, `db.t4g`, `db.t3`) pour les charges légères ou variables, généralistes (`db.m*`) et optimisées mémoire (`db.r*`, `db.x*`) pour les bases de production. Les classes Graviton (suffixe `g`) offrent généralement un meilleur rapport prix-performance.

#### Quand RDS n'est-il pas le bon choix ?

Quand il faut un accès au système d'exploitation ou des extensions non prises en charge (envisagez RDS Custom ou EC2), un moteur que RDS ne propose pas, une échelle extrême au-delà d'un seul écrivain (envisagez Aurora DSQL, DynamoDB ou du sharding), ou des charges analytiques sur des téraoctets qui conviennent mieux à un entrepôt de données ou un lakehouse.

#### Quelle est la différence entre RDS et une base de données sur EC2 ?

Sur EC2, vous avez un contrôle total (système d'exploitation, toute version, toute configuration) mais vous gérez tout : installation, correctifs, sauvegardes, réplication, basculement et supervision. RDS supprime ce travail d'exploitation au prix de quelques restrictions (pas d'accès au système, privilèges superutilisateur limités, seuls les paramètres pris en charge).

#### Qu'est-ce que RDS Custom ?

Une variante de RDS pour Oracle et SQL Server qui donne accès au système d'exploitation et permet de personnaliser la base (pour des applications historiques nécessitant des correctifs ou logiciels précis), tandis qu'AWS automatise toujours les sauvegardes et une partie de la gestion.

#### Qu'est-ce qu'un DB subnet group ?

Un ensemble de sous-réseaux (dans au moins deux zones de disponibilité) d'un VPC où RDS peut placer les instances. Il est nécessaire pour créer une instance dans un VPC et pour le Multi-AZ.

#### Qu'est-ce qu'un endpoint RDS ?

Le nom DNS et le port que les applications utilisent pour se connecter. Il reste le même lors d'un basculement (l'enregistrement DNS pointe vers la nouvelle primaire) : les applications doivent toujours passer par l'endpoint, jamais par une adresse IP.

#### Que sont les parameter groups ?

Des conteneurs de réglages du moteur (par exemple `max_connections`, `work_mem`, `innodb_buffer_pool_size`, `log_min_duration_statement`) appliqués aux instances. Les groupes par défaut ne sont pas modifiables ; on crée des groupes personnalisés. Les paramètres dynamiques s'appliquent immédiatement, les statiques exigent un redémarrage.

#### Que sont les option groups ?

Des conteneurs de fonctions optionnelles de certains moteurs, comme le Transparent Data Encryption d'Oracle, la sauvegarde native de SQL Server vers S3 ou le plugin memcached de MySQL.

#### Qu'est-ce que la fenêtre de maintenance ?

Une plage horaire hebdomadaire pendant laquelle AWS applique la maintenance en attente, comme les correctifs du système, les mises à jour mineures obligatoires ou les modifications d'instance reportées. Avec le Multi-AZ, la maintenance est appliquée d'abord à la standby puis un basculement a lieu, pour réduire l'interruption.

#### Peut-on arrêter une instance RDS ?

Oui, pour 7 jours au maximum d'affilée ; ensuite AWS la redémarre automatiquement pour appliquer la maintenance. À l'arrêt, on paie le stockage et les sauvegardes mais pas les heures d'instance. Les clusters Aurora peuvent être arrêtés de la même façon.

#### Qu'est-ce que la protection contre la suppression ?

Un réglage qui empêche la suppression d'une instance ou d'un cluster tant qu'il n'est pas désactivé, protégeant les bases de production d'une suppression accidentelle.

#### Qu'est-ce que le modèle de responsabilité partagée pour RDS ?

AWS est responsable de l'infrastructure, du système d'exploitation, des correctifs du logiciel de base, des sauvegardes et des mécanismes de réplication. Vous êtes responsable de l'accès réseau (groupes de sécurité), des choix de chiffrement, des utilisateurs et privilèges de la base, de la conception du schéma et des requêtes, des paramètres et de la protection des identifiants.

#### Comment vous connecter depuis votre ordinateur à une instance RDS dans un sous-réseau privé ?

Via un bastion ou, mieux, la redirection de port d'AWS Systems Manager Session Manager vers une instance du VPC, un VPN client, ou une machine EC2 dans le VPC ; jamais en rendant la base publique.

#### Que signifie « publicly accessible » pour une instance RDS ?

L'instance reçoit une IP publique et son endpoint la résout depuis l'extérieur du VPC : elle est joignable depuis Internet si les groupes de sécurité le permettent. Les bases de production doivent garder ce réglage désactivé.

#### Comment créer des instances RDS de façon reproductible ?

Avec l'infrastructure as code (CloudFormation, CDK, Terraform), en définissant subnet groups, parameter groups, groupes de sécurité, clés KMS, secrets et l'instance, pour que les environnements soient cohérents et les changements relus.

#### À quoi servent les tags RDS ?

À l'imputation des coûts, au contrôle d'accès (conditions IAM sur les tags), à l'automatisation (par exemple arrêter la nuit les instances taguées `env=dev`) et à l'identification des responsables.

#### Qu'est-ce que RDS on Outposts ?

RDS exécuté sur du matériel AWS Outposts dans votre propre centre de données, pour les charges qui exigent une faible latence vers des systèmes on-premise ou la résidence des données, géré avec les mêmes API.

### Stockage

#### Quels types de stockage RDS propose-t-il ?

Le SSD généraliste gp3 (base de 3 000 IOPS et 125 Mio/s, IOPS et débit configurables indépendamment de la taille), gp2 (IOPS liées à la taille avec crédits de rafale), les IOPS provisionnées io1 et io2 Block Express (IOPS élevées et constantes, faible latence) et l'ancien stockage magnétique.

#### Quand choisir les IOPS provisionnées ?

Pour des charges de production intensives en E/S qui exigent une latence faible et constante et beaucoup d'IOPS (OLTP très actif, gros volumes d'écriture), quand les limites configurables de gp3 ne suffisent pas ou que la prévisibilité compte plus que le coût.

#### Qu'est-ce que l'autoscaling du stockage ?

Un réglage qui augmente automatiquement le stockage alloué quand l'espace libre baisse, jusqu'à un maximum défini, pour éviter les pannes dues à un disque plein. Le stockage ne peut pas être réduit ensuite.

#### Peut-on réduire le stockage alloué dans RDS ?

Pas directement. Pour réduire, il faut créer une nouvelle instance avec moins de stockage et migrer les données (dump et restauration, DMS ou réplication logique), ou utiliser les déploiements Blue/Green quand ils sont pris en charge.

#### Pourquoi les performances gp2 peuvent-elles chuter soudainement ?

Les petits volumes gp2 dépendent de crédits de rafale au-delà de leurs IOPS de base (3 IOPS par Go). Quand les crédits sont épuisés, les performances retombent à la base. gp3 évite ce problème avec une base fixe indépendante de la taille.

#### Quel est le stockage maximal d'une instance RDS ?

Jusqu'à 64 Tio pour la plupart des moteurs (moins pour certaines configurations SQL Server). Le stockage d'Aurora croît automatiquement jusqu'à 128 Tio par cluster.

#### Que signifie l'état « storage-full » ?

L'instance n'a plus de stockage et n'accepte plus d'écritures. Activez l'autoscaling du stockage, alertez sur `FreeStorageSpace` et nettoyez les grosses tables, les journaux ou les fichiers temporaires.

#### Comment gp3 se compare-t-il à io2 pour RDS ?

gp3 offre une base de 3 000 IOPS et 125 Mio/s, configurable jusqu'à des limites plus élevées moyennant un surcoût, à un prix au Go plus bas. io2 Block Express offre des IOPS plus élevées et plus constantes et une latence plus faible avec une meilleure durabilité, pour les charges les plus exigeantes.

#### Qu'indique `DiskQueueDepth` ?

Le nombre de requêtes d'E/S en attente du disque. Une file constamment élevée avec une latence élevée signifie que le stockage ne suit pas ; envisagez plus d'IOPS, de meilleures requêtes ou du cache.

#### Quel est l'impact d'une modification du stockage sur une instance en service ?

Augmenter le stockage ou changer de type se fait généralement en ligne, mais l'instance peut passer des heures en état « storage-optimization », pendant lequel aucune autre modification du stockage n'est possible ; les performances peuvent être légèrement affectées.

#### Comment estimer les IOPS nécessaires ?

À partir des métriques actuelles (`ReadIOPS` + `WriteIOPS` en pointe) ou, pour une nouvelle charge, des transactions par seconde attendues et des E/S par transaction, avec de la marge ; puis tester sous charge avant la production.

### Haute disponibilité et Multi-AZ

#### Qu'est-ce qu'un déploiement Multi-AZ d'instance ?

RDS maintient une réplique standby synchrone de la primaire dans une autre zone de disponibilité. Si la primaire tombe (matériel, panne de la zone, défaillance du stockage) ou lors de certaines maintenances, RDS bascule automatiquement sur la standby, généralement en une à deux minutes. La standby ne sert pas de lectures.

#### Qu'est-ce qu'un déploiement Multi-AZ de cluster ?

Un déploiement (pour MySQL et PostgreSQL) avec un écrivain et deux instances standby lisibles dans trois zones, en réplication semi-synchrone. Le basculement est plus rapide (généralement moins de 35 secondes) et les standby peuvent servir des lectures via un endpoint de lecture.

#### Comment fonctionne le basculement Multi-AZ ?

RDS détecte la panne, promeut la standby et met à jour l'enregistrement DNS de l'endpoint pour qu'il pointe vers elle. Les applications doivent se reconnecter ; les pools de connexions doivent gérer les déconnexions et respecter le TTL DNS.

#### Quels événements déclenchent un basculement automatique ?

La perte de l'instance primaire ou de sa zone, une panne réseau ou de stockage sur la primaire, les changements de type d'instance, les correctifs du système et certaines maintenances du moteur, et un redémarrage manuel avec basculement.

#### Le Multi-AZ est-il une solution de montée en charge ?

Non. Dans un déploiement Multi-AZ d'instance, la standby ne sert pas de trafic ; elle sert à la disponibilité et à la durabilité. Pour monter en charge en lecture, utilisez des réplicas en lecture (ou les standby lisibles des clusters Multi-AZ, ou les réplicas Aurora).

#### Comment tester un basculement ?

En redémarrant l'instance avec l'option « reboot with failover » et en observant le comportement de l'application, le temps de reconnexion et les erreurs. Le faire régulièrement valide la résilience de l'application.

#### Le Multi-AZ protège-t-il contre la corruption de données ou les suppressions accidentelles ?

Non. La réplication copie toutes les modifications, y compris les mauvaises, vers la standby. Les sauvegardes, la restauration à un instant donné et les snapshots protègent contre les erreurs logiques.

#### Quelle est la différence entre haute disponibilité et reprise après sinistre pour RDS ?

La haute disponibilité (Multi-AZ) maintient la base en service quand une zone ou une instance tombe dans une région. La reprise après sinistre couvre la perte d'une région ou de données : réplicas en lecture inter-régions, copies inter-régions de snapshots, AWS Backup et Aurora Global Database, avec un RPO et un RTO définis.

#### Comment les applications doivent-elles gérer un basculement ?

Utiliser l'endpoint (jamais d'IP), un cache DNS court (par exemple le TTL DNS de la JVM), des relances avec backoff sur les erreurs de connexion, des pools qui valident les connexions, et envisager RDS Proxy ou les pilotes AWS qui détectent plus vite le basculement.

#### Que sont les AWS Advanced JDBC/Python wrappers ?

Des surcouches de pilotes qui connaissent la topologie de RDS et d'Aurora, détectent les basculements plus vite que les mises à jour DNS et se reconnectent au nouvel écrivain, réduisant l'interruption perçue par les applications.

#### Peut-on choisir la zone de la standby ?

RDS choisit la zone de la standby dans le subnet group ; vous choisissez la zone de la primaire. Le subnet group doit contenir des sous-réseaux dans au moins deux zones (trois pour les clusters Multi-AZ).

#### Quels RPO et RTO le Multi-AZ apporte-t-il ?

Pour les déploiements Multi-AZ d'instance, le RPO est quasiment nul (réplication synchrone) et le RTO est généralement d'une à deux minutes ; pour les clusters Multi-AZ, le RTO est en général inférieur à une minute.

### Réplicas en lecture

#### Qu'est-ce qu'un réplica en lecture ?

Une copie d'une instance source maintenue à jour par réplication asynchrone, utilisée pour décharger le trafic de lecture (rapports, analytique, API très lues). Il a son propre endpoint et peut être dans la même région ou une autre.

#### Combien de réplicas en lecture peut-on créer ?

Jusqu'à 15 pour MySQL, MariaDB et PostgreSQL, et moins pour Oracle et SQL Server ; Aurora accepte jusqu'à 15 Aurora Replicas par cluster. Pour certains moteurs, les réplicas peuvent eux-mêmes avoir des réplicas.

#### Qu'est-ce que le retard de réplication (replica lag) ?

Le délai entre une écriture sur la source et sa visibilité sur le réplica, suivi par la métrique `ReplicaLag`. Les écritures lourdes, les transactions longues, les réplicas sous-dimensionnés et la distance réseau (inter-régions) l'augmentent.

#### Pourquoi lire sur un réplica peut-il renvoyer des données périmées ?

Parce que la réplication est asynchrone : une lecture juste après une écriture peut ne pas la voir. Les applications qui doivent lire leurs propres écritures doivent lire sur la primaire pour ce cas.

#### Peut-on promouvoir un réplica en lecture ?

Oui. La promotion en fait une instance autonome qui accepte les écritures et rompt la réplication. On l'utilise pour la reprise après sinistre, les migrations ou la séparation d'une base.

#### À quoi servent les réplicas en lecture inter-régions ?

À servir des lectures près des utilisateurs d'une autre région, à la reprise après sinistre (promotion si la région primaire tombe) et à la migration d'une base vers une autre région.

#### Un réplica en lecture peut-il être Multi-AZ ?

Oui, pour les moteurs compatibles un réplica peut lui-même être configuré en Multi-AZ, ce qui améliore sa disponibilité (utile s'il peut être promu pour la reprise après sinistre).

#### Les réplicas en lecture exigent-ils des sauvegardes automatiques sur la source ?

Oui. Pour la plupart des moteurs, les sauvegardes automatiques doivent être activées sur l'instance source (rétention supérieure à zéro) pour créer des réplicas.

#### Comment utiliser les réplicas en lecture pour l'analytique sans pénaliser la production ?

En dirigeant les jobs de reporting et d'extraction vers un réplica dimensionné pour les requêtes analytiques, afin que les lectures longues n'entrent pas en concurrence avec le trafic OLTP de la primaire ; on surveille le retard pour que les rapports sachent à quel point les données sont fraîches.

#### Peut-on écrire sur un réplica en lecture ?

Normalement non : les réplicas sont en lecture seule. Pour MySQL, on peut passer `read_only = 0` sur un réplica dans des cas particuliers comme l'ajout d'index pour le reporting, mais les écritures peuvent casser la réplication et sont déconseillées.

#### Comment diriger les lectures vers les réplicas ?

Dans l'application (sources de données séparées en lecture et en écriture), via un proxy ou un pilote qui sépare lectures et écritures, ou avec l'endpoint de lecture d'Aurora, qui répartit les connexions entre réplicas.

#### Qu'arrive-t-il aux réplicas quand la source bascule en Multi-AZ ?

Les réplicas suivent automatiquement la nouvelle primaire après un basculement Multi-AZ, car l'endpoint source et le flux de réplication reprennent depuis la standby.

#### Qu'est-ce qu'un réplica différé ?

Un réplica (MySQL, MariaDB) configuré pour appliquer les changements avec un retard, par exemple une heure, afin de pouvoir se remettre d'une erreur en le promouvant avant que le mauvais changement ne soit appliqué.

### Sauvegardes et restauration

#### Que sont les sauvegardes automatiques ?

Des snapshots quotidiens de l'instance plus les journaux de transactions capturés toutes les quelques minutes, conservés pendant une période configurable (1 à 35 jours ; 0 les désactive), qui permettent la restauration à un instant donné dans la fenêtre de rétention.

#### Qu'est-ce que la restauration à un instant donné (PITR) ?

Restaurer la base à n'importe quelle seconde de la période de rétention (jusqu'à environ cinq minutes avant maintenant), ce qui crée une nouvelle instance avec un nouvel endpoint. C'est l'outil principal pour se remettre de modifications accidentelles.

#### Que sont les snapshots manuels ?

Des snapshots lancés par l'utilisateur, conservés jusqu'à leur suppression, indépendamment de la rétention des sauvegardes automatiques. On les utilise avant des changements risqués, pour la conservation longue et pour copier ou partager des bases.

#### Peut-on restaurer un snapshot dans l'instance existante ?

Non. Une restauration crée toujours une nouvelle instance. On pointe ensuite les applications vers le nouvel endpoint (ou on renomme les instances pour réutiliser l'ancien nom d'endpoint).

#### Comment copier les sauvegardes vers une autre région ou un autre compte ?

Copier les snapshots vers une autre région (copie inter-régions, éventuellement automatisée par AWS Backup ou par la réplication inter-régions des sauvegardes automatiques) et partager les snapshots avec d'autres comptes (les snapshots chiffrés exigent de partager la clé KMS).

#### Quel est le rôle d'AWS Backup avec RDS ?

AWS Backup centralise les politiques de sauvegarde entre services : planifications, rétention, copies inter-régions et inter-comptes, vault locks pour l'immuabilité, et rapports de conformité pour RDS et Aurora.

#### Que deviennent les sauvegardes automatiques à la suppression d'une instance ?

On peut les conserver (jusqu'à expiration de leur rétention) et prendre un snapshot final. Sans snapshot final ni sauvegardes conservées, les données sont perdues ; la protection contre la suppression et les snapshots finaux évitent les erreurs.

#### Les sauvegardes affectent-elles les performances ?

Avec le Multi-AZ, les sauvegardes sont prises sur la standby : la primaire n'est pas affectée. Sur les instances mono-AZ, les E/S peuvent être brièvement suspendues pendant le snapshot, ce qui peut affecter les performances.

#### Comment exporter les données RDS vers S3 pour l'analytique ?

Exporter un snapshot vers S3 (RDS écrit les tables en fichiers Parquet, interrogeables par Athena ou Glue), ou faire ses propres exports (l'extension `aws_s3` de PostgreSQL, `SELECT INTO OUTFILE S3` dans Aurora MySQL, ou des jobs Glue/DMS).

#### Combien de temps prend une restauration ?

Cela dépend de la taille et de l'activité de la base : créer l'instance depuis le snapshot est rapide, mais les données sont chargées à la demande depuis S3, donc les premières requêtes peuvent être lentes tant que les blocs n'ont pas été lus (il peut falloir « préchauffer » les restaurations critiques).

#### Qu'est-ce que le chargement différé (lazy loading) après une restauration ?

Quand une instance est restaurée depuis un snapshot, ses blocs de stockage sont récupérés depuis S3 au premier accès : les lectures initiales ont une latence plus élevée. Lancer des lectures complètes des tables après la restauration préchauffe le stockage.

#### Comment conserver des sauvegardes sept ans pour la conformité ?

Avec AWS Backup et un plan de rétention long avec vault lock, ou en copiant régulièrement des snapshots manuels ; les sauvegardes automatiques plafonnent à 35 jours. L'export vers S3 avec des règles de cycle de vie peut aussi servir à l'archivage.

#### Peut-on restaurer une seule table depuis une sauvegarde ?

Pas directement. Restaurez toute l'instance dans une nouvelle (à un instant donné), puis faites un dump de la table voulue et importez-la en production.

#### Qu'est-ce que la réplication inter-régions des sauvegardes automatiques ?

Une fonction qui copie les sauvegardes automatiques et les journaux de transactions vers une autre région, pour pouvoir faire une restauration à un instant donné dans la région de secours.

### Sécurité

#### Comment contrôler l'accès réseau à RDS ?

Placer les instances dans des sous-réseaux privés, désactiver l'accès public, et utiliser des groupes de sécurité VPC qui n'autorisent que les groupes de sécurité de l'application ou des plages CIDR précises sur le port de la base. L'accès depuis l'on-premise passe par VPN ou Direct Connect.

#### Comment les données sont-elles chiffrées au repos dans RDS ?

Avec des clés AWS KMS (gérées par AWS ou par le client), qui couvrent le stockage, les sauvegardes automatiques, les snapshots, les réplicas en lecture et les journaux. Le chiffrement se choisit à la création.

#### Comment chiffrer une instance RDS existante non chiffrée ?

Prendre un snapshot, le copier avec chiffrement activé à l'aide d'une clé KMS et restaurer une nouvelle instance depuis la copie chiffrée ; puis basculer les applications. Les réplicas d'une instance non chiffrée ne peuvent pas être chiffrés directement.

#### Comment les données sont-elles chiffrées en transit ?

Par des connexions SSL/TLS utilisant le bundle d'autorités de certification RDS. On peut imposer TLS avec des paramètres comme `rds.force_ssl` (PostgreSQL, SQL Server) ou `require_secure_transport` (MySQL). Il faut renouveler les certificats quand RDS change ses autorités.

#### Qu'est-ce que l'authentification IAM à la base de données ?

Pour MySQL, MariaDB et PostgreSQL (et Aurora), les utilisateurs s'authentifient avec un jeton de courte durée généré à partir d'identifiants IAM au lieu d'un mot de passe : l'accès se contrôle par des politiques IAM et aucun mot de passe de base n'est stocké dans les applications.

#### Comment gérer les mots de passe de la base ?

Avec Secrets Manager, idéalement avec des mots de passe de l'utilisateur maître gérés par RDS (RDS crée et fait tourner le secret), en faisant tourner automatiquement les secrets des utilisateurs applicatifs, et sans jamais coder d'identifiants en dur.

#### Quels privilèges l'utilisateur maître possède-t-il ?

Des privilèges d'administration étendus dans les limites du moteur (par exemple `rds_superuser` dans PostgreSQL), mais pas de superutilisateur complet ni d'accès au système. Créez des utilisateurs séparés avec le moindre privilège pour les applications et les pipelines.

#### Comment auditer l'activité de la base ?

Avec les journaux du moteur (`pgaudit` pour PostgreSQL, le plugin d'audit MySQL, l'audit SQL Server, l'audit unifié Oracle) publiés dans CloudWatch Logs, CloudTrail pour les appels d'API RDS, et les Database Activity Streams pour une activité quasi temps réel envoyée vers Kinesis (pour les outils de conformité).

#### Que sont les Database Activity Streams ?

Une fonction (pour Aurora et certains moteurs RDS) qui pousse un flux temps réel de l'activité de la base vers Kinesis Data Streams, chiffré avec KMS et hors du contrôle des DBA, pour la supervision et la conformité.

#### Comment protéger RDS des modifications humaines accidentelles ?

IAM au moindre privilège sur les API RDS, protection contre la suppression, comptes ou rôles séparés pour la production, gestion des changements par infrastructure as code, et audits de qui peut modifier instances et parameter groups.

#### Comment restreindre les utilisateurs IAM autorisés à créer ou modifier des instances RDS ?

Avec des politiques IAM sur les actions RDS (`rds:CreateDBInstance`, `rds:ModifyDBInstance`, `rds:DeleteDBInstance`), des conditions sur les tags, et des service control policies dans AWS Organizations comme garde-fous, par exemple pour imposer le chiffrement.

#### Comment empêcher la création de bases non chiffrées ?

Avec une SCP ou une condition IAM `rds:StorageEncrypted = true` sur les actions de création, des règles AWS Config (`rds-storage-encrypted`) pour détecter les écarts, et des valeurs par défaut dans l'infrastructure as code.

#### Qu'est-ce que l'authentification Kerberos sur RDS ?

L'intégration avec AWS Managed Microsoft AD (ou un AD autogéré via une relation d'approbation) pour que les utilisateurs se connectent à SQL Server, Oracle, PostgreSQL ou MySQL avec leurs identifiants d'annuaire et une gestion centralisée des comptes.

#### Comment limiter l'accès réseau de Lambda à RDS ?

Exécuter Lambda dans le VPC avec son propre groupe de sécurité, n'autoriser que ce groupe sur le port de la base, et utiliser RDS Proxy avec authentification IAM pour ne pas stocker de mots de passe dans la fonction.

#### Comment partager un snapshot chiffré avec un autre compte ?

Utiliser une clé KMS gérée par le client (les snapshots chiffrés avec la clé gérée par AWS ne peuvent pas être partagés), donner à l'autre compte l'accès à la clé et partager le snapshot ; l'autre compte le copie avec sa propre clé.

#### Quelle bonne pratique pour les utilisateurs de base applicatifs ?

Un utilisateur par application ou service avec uniquement les privilèges nécessaires (souvent `SELECT`, `INSERT`, `UPDATE`, `DELETE` au niveau du schéma, sans DDL), des utilisateurs en lecture seule séparés pour le reporting, et le DDL confié aux outils de migration avec un autre utilisateur.

### Supervision et performances

#### Quelles métriques CloudWatch sont les plus importantes pour RDS ?

`CPUUtilization`, `FreeableMemory`, `FreeStorageSpace`, `ReadIOPS`/`WriteIOPS`, `ReadLatency`/`WriteLatency`, `DiskQueueDepth`, `DatabaseConnections`, `ReplicaLag`, `SwapUsage` et, pour les classes extensibles, `CPUCreditBalance`.

#### Qu'est-ce qu'Enhanced Monitoring ?

Des métriques au niveau du système d'exploitation (CPU et mémoire par processus, système de fichiers, swap, E/S disque) collectées par un agent jusqu'à chaque seconde et envoyées dans CloudWatch Logs, qui aident à trouver des causes invisibles dans les métriques standard.

#### Qu'est-ce que Performance Insights / Database Insights ?

Un outil de performance qui montre la charge de la base (sessions actives moyennes) ventilée par événements d'attente, requêtes SQL, utilisateurs et hôtes, pour voir quelles requêtes génèrent la charge et pourquoi. Il fait désormais partie de CloudWatch Database Insights, qui ajoute en mode avancé des vues sur toute la flotte et une rétention plus longue.

#### Comment trouver les requêtes lentes dans RDS ?

Activer les journaux de requêtes lentes (`slow_query_log` et `long_query_time` pour MySQL, `log_min_duration_statement` pour PostgreSQL), utiliser `pg_stat_statements` ou le Performance Schema, et analyser le top SQL de Database Insights ; puis lancer `EXPLAIN` pour corriger plans et index.

#### Que sont les notifications d'événements RDS ?

Des notifications envoyées via EventBridge ou SNS pour des événements comme les basculements, redémarrages, stockage faible, sauvegardes, changements de configuration et maintenance, utilisées pour l'alerte et l'automatisation.

#### Qu'est-ce qui provoque un CPU élevé sur une instance RDS ?

Des requêtes inefficaces (index manquants, lectures complètes, mauvais plans), trop de connexions simultanées, des rapports lourds sur la primaire, de la contention de verrous ou une instance sous-dimensionnée. Trouvez d'abord le top SQL, puis optimisez ou augmentez la taille.

#### Qu'est-ce qui provoque un manque de connexions ?

Des applications sans pool qui ouvrent de nombreuses connexions (les fonctions serverless sont un cas classique), des fuites de connexions, un `max_connections` faible pour la mémoire de l'instance, ou un pic de trafic. Utilisez un pool (RDS Proxy, PgBouncer) et corrigez les fuites.

#### Qu'est-ce que RDS Proxy ?

Un proxy de base de données géré qui mutualise et partage les connexions entre les applications et RDS ou Aurora, réduit le coût d'ouverture des connexions (surtout depuis Lambda), accélère le basculement en conservant les connexions clientes et en les redirigeant, et prend en charge l'authentification IAM et Secrets Manager.

#### Quand utiliser RDS Proxy ?

Avec Lambda ou d'autres clients très concurrents et éphémères, des applications qui ouvrent beaucoup de connexions, ou pour un basculement plus rapide et plus transparent. Il ajoute un coût et un peu de latence, et certaines fonctions de session (pinning) réduisent son intérêt.

#### Comment régler PostgreSQL sur RDS ?

Ajuster les paramètres dans un parameter group personnalisé (`shared_buffers`, `work_mem`, `maintenance_work_mem`, `effective_cache_size`, réglages d'autovacuum, `max_connections`), garder les statistiques à jour, ajouter les bons index, surveiller le bloat et les transactions longues, et utiliser `pg_stat_statements`.

#### Comment régler MySQL sur RDS ?

Dimensionner `innodb_buffer_pool_size` (environ 75 % de la mémoire par défaut), revoir `max_connections`, utiliser des index et plans adaptés, surveiller le journal des requêtes lentes, et éviter les transactions longues qui font grossir les undo logs.

#### Pourquoi l'autovacuum est-il important sur RDS PostgreSQL ?

Le MVCC de PostgreSQL laisse des tuples morts après les mises à jour et suppressions ; l'autovacuum les récupère et évite le bouclage des identifiants de transaction. S'il prend du retard, les tables gonflent et, au pire, la base refuse les écritures pour éviter le bouclage. Réglez-le pour les grosses tables actives.

#### Qu'est-ce que `FreeableMemory`, et quand faut-il s'en inquiéter ?

La RAM disponible sur l'instance. Peu de mémoire libre avec un `SwapUsage` en hausse signifie que la charge ne tient pas (buffer pool, connexions, tris) ; augmentez la taille ou réduisez la consommation mémoire.

#### Comment les verrous apparaissent-ils dans les outils de performance RDS ?

Sous forme d'événements d'attente (par exemple `Lock:transactionid` ou `Lock:relation` pour PostgreSQL, `synch/cond/innodb/row_lock_wait` pour MySQL) dans Database Insights ; des requêtes sur `pg_locks` avec `pg_stat_activity` montrent qui bloque qui.

#### Comment trouver les index inutilisés dans PostgreSQL sur RDS ?

Interroger `pg_stat_user_indexes` pour les index avec `idx_scan = 0` sur une longue période (hors contraintes), et les supprimer après vérification, car ils coûtent en performances d'écriture et en stockage.

#### Comment identifier les transactions longues dans PostgreSQL ?

Interroger `pg_stat_activity` pour les sessions avec un `xact_start` ancien, surtout en `idle in transaction` ; elles bloquent le vacuum et causent du bloat. Fixez `idle_in_transaction_session_timeout` pour protéger la base.

#### Quels journaux RDS peut-il publier dans CloudWatch Logs ?

Journaux d'erreurs, de requêtes lentes, généraux (MySQL), les journaux PostgreSQL (dont la sortie de `log_min_duration_statement` et de `pgaudit`), journaux d'audit, de mise à jour et de l'agent, selon le moteur et les réglages.

#### Comment alerter sur les problèmes RDS ?

Alarmes CloudWatch sur le CPU, le stockage libre, la mémoire libre, les connexions, le retard des réplicas, les latences de lecture et d'écriture et le solde de rafale ; règles EventBridge sur les événements RDS (basculement, stockage plein, maintenance) ; et détection d'anomalies dans Database Insights.

### Montée en charge

#### Comment faire monter une instance RDS en charge verticalement ?

Modifier la classe d'instance (par exemple de `db.r6g.large` à `db.r6g.2xlarge`), immédiatement ou dans la fenêtre de maintenance. Cela implique une brève interruption, raccourcie par le Multi-AZ (la standby est modifiée d'abord, puis basculement).

#### Comment monter en charge en lecture ?

Ajouter des réplicas en lecture (ou des Aurora Replicas) et y diriger le trafic en lecture seule, mettre en cache les lectures fréquentes avec ElastiCache, et utiliser les standby lisibles des clusters Multi-AZ.

#### Comment monter en charge en écriture au-delà d'une seule instance ?

Augmenter la taille de l'instance, optimiser les écritures (lots, moins d'index, partitionnement), déplacer une partie de la charge vers d'autres bases (DynamoDB pour les accès clé-valeur), ou répartir les données (sharding) entre instances au niveau applicatif. Aurora Limitless Database (PostgreSQL) et Aurora DSQL offrent des options gérées de montée en charge horizontale.

#### Qu'est-ce que le partitionnement de tables, et aide-t-il sur RDS ?

Découper de grosses tables en partitions (partitionnement déclaratif PostgreSQL, partitionnement MySQL) par plage ou par liste, ce qui accélère les requêtes filtrant sur la clé de partition et rend l'archivage peu coûteux (supprimer une partition plutôt que des lignes).

#### Comment se comportent les instances extensibles sous une charge soutenue ?

Les instances `db.t*` accumulent des crédits CPU au repos et les dépensent sous charge ; avec un CPU élevé soutenu, elles épuisent leurs crédits et sont bridées (mode standard) ou facturent davantage (mode illimité). Elles ne conviennent pas aux charges de production régulières.

#### Comment augmenter les performances du stockage sans changer d'instance ?

Avec gp3, augmenter IOPS et débit indépendamment ; avec io1/io2, augmenter les IOPS provisionnées ; vérifier que la bande passante EBS de la classe d'instance n'est pas le goulot d'étranglement.

#### Quelles limites d'instance peuvent plafonner les E/S ?

Chaque classe d'instance a une bande passante EBS et des IOPS maximales ; une petite classe ne peut pas exploiter des IOPS provisionnées très élevées. Choisissez une classe dont les limites correspondent à la configuration du stockage.

#### Comment le cache aide-t-il une base RDS ?

ElastiCache (Redis ou Memcached) ou des caches applicatifs servent depuis la mémoire les lectures répétées (sessions, catalogues produits, résultats calculés), réduisant la charge et la latence de la base. La stratégie d'invalidation est la partie difficile.

#### Quand faut-il découper une base en plusieurs ?

Quand des domaines ou services ont des charges, des besoins de montée en charge ou des responsables indépendants, quand les pics d'une charge affectent les autres, ou selon le principe microservices d'une base par service.

### Aurora

#### Qu'est-ce qu'Amazon Aurora ?

Une base relationnelle compatible MySQL et PostgreSQL conçue pour le cloud, avec une couche de stockage distribuée et tolérante aux pannes partagée par l'écrivain et les réplicas. Elle offre un débit supérieur aux moteurs standard, un basculement plus rapide et un stockage qui croît automatiquement.

#### Comment fonctionne le stockage d'Aurora ?

Les données sont stockées dans un volume de cluster répliqué six fois sur trois zones de disponibilité, en segments de 10 Go. Les écritures exigent quatre copies sur six et les lectures trois sur six : le cluster tolère la perte d'une zone plus une autre copie. Le stockage croît automatiquement jusqu'à 128 Tio.

#### Qu'est-ce qu'un cluster Aurora ?

Une instance écrivain (primaire) et jusqu'à 15 Aurora Replicas partageant le même volume, avec un endpoint de cluster (écrivain), un endpoint de lecture (réparti entre les réplicas) et des endpoints personnalisés optionnels pour des sous-ensembles d'instances.

#### En quoi le basculement Aurora diffère-t-il du Multi-AZ de RDS ?

Un Aurora Replica peut être promu parce qu'il partage le même stockage : il n'y a pas de données à rattraper et le basculement prend généralement 30 secondes ou moins. Le retard des réplicas est en général de quelques millisecondes.

#### Qu'est-ce qu'Aurora Serverless v2 ?

Un mode de capacité où les instances Aurora ajustent automatiquement leur capacité, par fines unités appelées Aurora Capacity Units (ACU), selon la charge, entre un minimum et un maximum, et peuvent descendre à zéro dans certaines configurations. Il convient aux charges variables ou imprévisibles.

#### Qu'est-ce qu'Aurora Global Database ?

Une configuration avec une région primaire et plusieurs régions secondaires, répliquées au niveau du stockage avec généralement moins d'une seconde de retard. Les secondaires servent des lectures locales et peuvent être promues en cas de panne régionale (basculement géré ou switchover).

#### Qu'est-ce que le clonage rapide d'Aurora ?

La création d'un nouveau cluster qui partage les pages de stockage de la source en copy-on-write : le clone se crée vite et seules les pages modifiées consomment du nouveau stockage. Idéal pour les tests, l'analytique sur une copie ou le rafraîchissement de la préproduction.

#### Qu'est-ce qu'Aurora Backtrack ?

Une fonction d'Aurora MySQL qui ramène le cluster sur place à un instant antérieur dans une fenêtre configurée, sans restauration de sauvegarde, utile pour annuler rapidement une erreur.

#### Que sont Aurora Standard et Aurora I/O-Optimized ?

Deux configurations de stockage : Standard facture les requêtes d'E/S séparément (moins cher avec peu d'E/S), I/O-Optimized inclut les E/S dans un prix de stockage et d'instance plus élevé (moins cher quand les E/S dépassent environ un quart du coût de la base).

#### Qu'est-ce que l'intégration zero-ETL d'Aurora avec Redshift ?

Une intégration gérée qui réplique les données d'Aurora (et de certains moteurs RDS) dans Amazon Redshift en quasi temps réel sans construire de pipelines, pour faire de l'analytique dans Redshift sur des données opérationnelles fraîches.

#### Qu'est-ce que Babelfish for Aurora PostgreSQL ?

Une capacité qui permet à Aurora PostgreSQL de comprendre le T-SQL et le protocole TDS de SQL Server, pour que des applications écrites pour SQL Server fonctionnent avec moins de modifications de code.

#### Qu'est-ce que la Data API d'Aurora ?

Une API HTTP pour exécuter du SQL sur Aurora (Serverless v2 et provisionné) sans gérer de connexions ni de pilotes, pratique pour Lambda et les autres applications serverless.

#### Qu'est-ce qu'Aurora DSQL ?

Une base SQL distribuée et serverless compatible PostgreSQL, conçue pour des applications actif-actif multi-régions, qui monte en charge horizontalement en lecture et en écriture avec une cohérence forte. Elle diffère d'Aurora standard et a quelques limites fonctionnelles par rapport à PostgreSQL.

#### Quand choisir Aurora plutôt que RDS pour PostgreSQL ou MySQL ?

Quand il faut un débit plus élevé, un basculement plus rapide, de nombreux réplicas à faible retard, une réplication mondiale, du clonage rapide ou une montée en charge serverless. RDS standard peut être moins cher pour des charges petites ou régulières et prend parfois en charge plus tôt certaines fonctions ou versions du moteur.

#### Que sont les endpoints personnalisés d'Aurora ?

Des endpoints qui pointent vers un sous-ensemble choisi des instances d'un cluster, par exemple des réplicas plus gros pour les requêtes analytiques et de plus petits pour les lectures applicatives.

#### Quelle est la limite de l'endpoint de lecture d'Aurora ?

Il répartit les nouvelles connexions entre réplicas via le DNS, pas les requêtes individuelles ; les connexions longues restent sur un réplica, d'où une charge parfois déséquilibrée. Des pools qui recyclent périodiquement les connexions ou des proxies aident.

#### Qu'est-ce qu'Aurora parallel query ?

Une fonction d'Aurora MySQL qui pousse une partie des requêtes analytiques (filtres, agrégations) vers la couche de stockage, sur des milliers de nœuds, ce qui accélère certaines requêtes analytiques sur de grosses tables sans entrepôt séparé.

#### Que sont les Aurora Optimized Reads ?

Une fonction des instances dotées de stockage NVMe local, qui l'utilise comme cache hiérarchisé et pour les objets temporaires, améliorant la latence des charges en lecture dont les données dépassent la mémoire et des requêtes avec de grosses tables temporaires.

#### Comment Aurora gère-t-il les sauvegardes ?

En continu et de façon incrémentale vers S3, sans impact sur les performances, avec restauration à un instant donné dans la période de rétention (1 à 35 jours) ; les snapshots sont au niveau du cluster.

#### Qu'est-ce qu'Aurora Limitless Database ?

Une capacité d'Aurora PostgreSQL qui monte en charge horizontalement en écriture en répartissant (sharding) les tables sur plusieurs instances derrière un seul endpoint, pour des charges au-delà de la capacité d'un écrivain.

#### Qu'est-ce que la priorité de basculement (tier) d'Aurora ?

Un réglage (tier 0 à 15) sur chaque réplica qui détermine lequel est promu en premier lors d'un basculement ; à rang égal, le choix se fait selon la taille.

#### Peut-on mélanger Aurora Serverless v2 et des instances provisionnées ?

Oui. Un cluster peut avoir un écrivain provisionné et des lecteurs Serverless v2 (ou l'inverse), ce qui est utile avec un trafic de lecture variable.

### Moteurs et fonctions

#### Quelles extensions PostgreSQL sont utiles sur RDS ?

`pg_stat_statements` (statistiques de requêtes), `PostGIS` (géospatial), `pgvector` (recherche vectorielle), `pg_partman` (gestion des partitions), `pg_cron` (jobs planifiés), `aws_s3` (import/export avec S3), `pgaudit`, `pg_repack` et `postgres_fdw`. Seules les extensions prises en charge peuvent être installées.

#### Comment charger des données depuis S3 dans RDS PostgreSQL ?

Avec l'extension `aws_s3` : `SELECT aws_s3.table_import_from_s3('table', 'col1,col2', '(format csv, header true)', aws_commons.create_s3_uri('bucket', 'fichier.csv', 'eu-west-1'));`, avec un rôle IAM associé à l'instance.

#### Qu'est-ce qu'un déploiement Blue/Green ?

Une fonction (MySQL, MariaDB, PostgreSQL, Aurora) qui crée une copie de préproduction (green) synchronisée avec la production (blue) par réplication logique, permet de la mettre à jour ou de la modifier, puis bascule en environ une minute avec des garde-fous, en conservant les mêmes endpoints.

#### Comment mettre à jour la version majeure d'un moteur RDS ?

Tester la mise à jour sur une restauration de snapshot, vérifier la compatibilité des extensions et des paramètres, puis mettre à jour sur place (avec interruption) ou utiliser un déploiement Blue/Green pour une interruption minimale. Prenez un snapshot avant la mise à jour.

#### Que sont les mises à jour automatiques de version mineure ?

Une option où RDS applique automatiquement les versions mineures du moteur (corrections de bugs et de sécurité) pendant la fenêtre de maintenance. La plupart des équipes l'activent, parfois après des tests dans les environnements inférieurs.

#### Qu'est-ce que RDS Extended Support ?

Une offre payante qui continue de fournir les correctifs critiques des versions majeures après leur fin de vie communautaire, ce qui donne du temps pour mettre à jour. Les instances sur ces versions y sont inscrites automatiquement si elles ne sont pas mises à jour.

#### Comment planifier des jobs dans RDS PostgreSQL ?

Avec `pg_cron` pour des jobs SQL à l'intérieur de la base, ou depuis l'extérieur avec EventBridge Scheduler, Lambda ou un orchestrateur. Le batch lourd est souvent mieux placé hors de la base OLTP.

#### Quelles sont les restrictions de SQL Server sur RDS ?

Pas de rôle `sysadmin`, des fonctions limitées dans certaines éditions, des procédures spécifiques pour la sauvegarde et la restauration natives (via S3), des limites sur le nombre de bases par instance et sur la taille du stockage ; RDS Custom for SQL Server en lève certaines.

#### Quelles options de licence existent pour Oracle et SQL Server sur RDS ?

License Included (licence incluse dans le prix horaire) ou Bring Your Own License pour Oracle ; SQL Server est généralement en License Included, avec le choix de l'édition (Express, Web, Standard, Enterprise).

#### Comment utiliser `pgvector` sur RDS PostgreSQL ?

Installer l'extension, créer des colonnes `vector` pour les embeddings et les indexer avec des index HNSW ou IVFFlat pour la recherche par similarité, ce qui permet la génération augmentée par récupération sans base vectorielle séparée.

#### À quoi sert la réplication logique sur RDS PostgreSQL ?

À répliquer des tables choisies vers une autre base PostgreSQL (mises à jour, migrations, découpage de bases ou alimentation de l'analytique), au CDC vers des systèmes externes et aux déploiements Blue/Green.

#### Quels sont les atouts de MySQL 8.0+ sur RDS pour le travail sur les données ?

Fonctions de fenêtre, CTE (y compris récursives), fonctions JSON, index invisibles, `ADD COLUMN` instantané pour beaucoup de changements et de meilleures statistiques d'optimiseur, qui facilitent les requêtes analytiques et les changements de schéma.

#### Comment mener des migrations de schéma sûres sur de grosses tables ?

Utiliser des opérations compatibles avec le travail en ligne (DDL instantané de MySQL 8, `CREATE INDEX CONCURRENTLY` de PostgreSQL), des outils comme `gh-ost` ou `pt-online-schema-change` pour MySQL, des déploiements Blue/Green, et mesurer la durée de la migration sur un clone.

### Coûts

#### Qu'est-ce qui fait les coûts de RDS ?

Les heures d'instance (par classe ; le Multi-AZ double le calcul), le stockage (par type et taille, plus les IOPS provisionnées), le stockage de sauvegarde au-delà du volume gratuit, le transfert de données sortant et entre zones ou régions, les frais d'Extended Support, et des fonctions comme RDS Proxy et le mode avancé de Database Insights.

#### Comment réduire les coûts de RDS ?

Dimensionner les instances d'après les métriques, utiliser les classes Graviton, acheter des Reserved Instances pour les charges régulières, préférer gp3 à un io1 surprovisionné, arrêter la nuit les instances hors production, nettoyer les anciens snapshots, utiliser Aurora Serverless v2 ou I/O-Optimized quand ils conviennent, et décharger les lectures vers des caches.

#### Combien coûte le Multi-AZ ?

Environ le double du coût de l'instance, car une instance standby tourne dans une autre zone, plus le stockage répliqué. C'est généralement justifié en production ; les environnements hors production tournent souvent en mono-AZ.

#### Que sont les Reserved Instances pour RDS ?

Un engagement d'un ou trois ans sur une famille de classes d'instance dans une région, en échange d'une remise importante par rapport au prix à la demande, avec une flexibilité de taille au sein d'une famille pour la plupart des moteurs.

#### Comment trouver les instances RDS inactives ou surdimensionnées ?

Avec les métriques CloudWatch (CPU, connexions, IOPS) sur plusieurs semaines, les recommandations d'AWS Compute Optimizer pour RDS, les contrôles Trusted Advisor sur les instances inactives et les rapports de coûts par tag.

#### Combien coûte le stockage des sauvegardes ?

Le stockage de sauvegarde jusqu'à la taille du stockage provisionné de la région est inclus ; au-delà, et pour les snapshots manuels conservés longtemps, on paie au Go-mois. Les vieux snapshots manuels sont un coût caché fréquent.

#### Comment les coûts de transfert entre zones affectent-ils RDS ?

La réplication Multi-AZ n'est pas facturée, mais le trafic applicatif entre une instance dans une zone et des clients dans une autre, ainsi que la réplication inter-régions, entraînent des frais de transfert.

#### Comment économiser sur les bases de développement ?

Utiliser des instances petites ou extensibles, en mono-AZ, les arrêter hors des heures de travail, utiliser Aurora Serverless v2 avec un minimum bas, restaurer depuis des snapshots partagés plutôt que de garder de nombreuses copies, et supprimer les environnements inutilisés.

### Migration et data engineering

#### Comment migrer une base vers RDS ?

Pour un même moteur : dump et restauration natifs (`pg_dump`/`pg_restore`, `mysqldump`, sauvegarde SQL Server vers S3 puis restauration), ou réplication de la source vers RDS pour une interruption minimale. Pour des moteurs différents ou une réplication continue : AWS DMS, avec le Schema Conversion Tool (ou DMS Schema Conversion) pour traduire le schéma.

#### Qu'est-ce qu'AWS DMS ?

Database Migration Service : il réplique les données d'une base source vers une cible (une autre base, S3, Redshift, Kinesis et d'autres) avec un chargement complet puis une capture continue des changements (CDC), sur des instances de réplication ou DMS Serverless.

#### Comment capturer les changements (CDC) de RDS MySQL ?

Activer le binary log avec `binlog_format = ROW` (et l'image complète des lignes), garder une rétention suffisante (`mysql.rds_set_configuration('binlog retention hours', 24)`), et lire les changements avec DMS, Debezium ou une intégration zero-ETL.

#### Comment capturer les changements de RDS PostgreSQL ?

Activer la réplication logique (`rds.logical_replication = 1`), créer un slot de réplication et une publication, et consommer avec DMS, Debezium (plugin pgoutput) ou zero-ETL. Surveillez les slots : un slot non consommé retient le WAL et peut remplir le disque.

#### Pourquoi les slots de réplication sont-ils dangereux sur PostgreSQL ?

Un slot oblige PostgreSQL à conserver le WAL jusqu'à ce que le consommateur l'acquitte. Si un consommateur CDC s'arrête, le WAL s'accumule (`TransactionLogsDiskUsage` augmente) jusqu'à remplir le stockage et arrêter la base. Alertez sur le retard des slots et supprimez les slots abandonnés.

#### Comment extraire de grosses tables de RDS sans pénaliser la production ?

Lire depuis un réplica ou un clone/une restauration récente, exporter des snapshots vers S3 en Parquet, extraire de façon incrémentale par une colonne updated-at ou par CDC plutôt que tout extraire, paralléliser par plages de clés dans certaines limites, et planifier hors des heures de pointe.

#### Qu'est-ce que l'export de snapshot vers S3 ?

Une fonction RDS qui exporte les données d'un snapshot vers S3 au format Parquet, partitionnées par table, sans impact sur la base en service, prêtes à être cataloguées par Glue et interrogées par Athena.

#### Comment les jobs Glue lisent-ils RDS ?

Via une connexion JDBC Glue dans le VPC de la base (avec accès sous-réseau et groupe de sécurité), en lisant les tables en parallèle grâce aux options de partitionnement, avec les identifiants dans Secrets Manager ; bookmarks ou colonne de watermark assurent les chargements incrémentaux.

#### Comment charger efficacement des données dans RDS ?

Avec le chargement en masse (`COPY` pour PostgreSQL, `LOAD DATA` pour MySQL, l'extension `aws_s3`), des insertions par lots, en désactivant ou différant la création des index secondaires lors des chargements initiaux, en augmentant temporairement `maintenance_work_mem`, et en évitant les insertions ligne à ligne à travers le réseau.

#### Faut-il lancer de l'analytique directement sur l'instance RDS de production ?

En général non. Les requêtes analytiques concurrencent le trafic OLTP pour le CPU, la mémoire et les E/S. Utilisez un réplica pour le reporting léger et, pour une analytique plus lourde, déplacez les données vers un entrepôt ou un lakehouse via CDC, exports ou zero-ETL.

#### Quelle est la différence entre OLTP et OLAP, et où se situe RDS ?

L'OLTP traite de nombreuses petites transactions (insertions, mises à jour, recherches ponctuelles) avec une cohérence forte ; l'OLAP traite de grosses lectures et agrégations sur l'historique. RDS est fait pour l'OLTP ; l'OLAP relève de Redshift, Snowflake, Databricks ou Athena sur un data lake.

#### Qu'est-ce que DMS Schema Conversion ?

Une fonction gérée de DMS (qui succède dans bien des cas au Schema Conversion Tool de bureau) qui évalue et convertit schémas et code entre moteurs, en signalant les éléments nécessitant un travail manuel.

#### Comment DMS gère-t-il les grosses tables lors du chargement complet ?

Par un chargement parallèle par partitions ou plages d'une colonne, des réglages pour les objets volumineux (LOB) et des mappages de tables pour sélectionner et transformer ; les très grosses migrations peuvent combiner un export natif en masse et le CDC DMS à partir d'une position connue.

#### Comment valider une migration ?

Validation des données DMS (comparaison ligne à ligne), comptages de lignes et sommes de contrôle par table, comparaison d'agrégats (sommes, min/max par plages de clés), tests applicatifs sur la cible et une période de fonctionnement en parallèle.

#### Quels sont les pièges courants du CDC depuis des bases relationnelles ?

Des tables sans clé primaire (impossible d'appliquer les mises à jour), une rétention de journaux insuffisante, de grosses transactions qui créent du retard, des changements de schéma non propagés, des écarts de types (horodatages, décimaux) et des suppressions non traitées en aval.

#### Comment envoyer les changements RDS vers Kafka ?

Avec Debezium sur Kafka Connect (ou Amazon MSK Connect) lisant le binlog ou la réplication logique, qui produit un topic par table avec les événements de changement, ou avec DMS ciblant Kinesis ou MSK.

#### Comment amener les données RDS dans un data lake ?

Des chargements complets par export de snapshot vers S3 ou chargement complet DMS, puis les changements incrémentaux par CDC DMS vers S3 (Parquet avec des colonnes d'opération) ou zero-ETL ; on applique les changements à des tables Iceberg/Delta avec `MERGE` et on catalogue le tout dans Glue.

#### Qu'est-ce qu'une extraction incrémentale par watermark, et quels en sont les risques ?

Sélectionner les lignes dont `updated_at` dépasse la dernière valeur extraite. Elle manque les suppressions, les lignes modifiées sans mise à jour de l'horodatage et les lignes validées tardivement avec un horodatage antérieur ; utilisez une fenêtre de recouvrement et des rapprochements réguliers, ou le CDC.

#### Comment éviter de verrouiller les tables de production lors d'une extraction ?

Utiliser des snapshots ou des réplicas, lire avec un isolement par snapshot cohérent sans verrou (MVCC de PostgreSQL, lectures cohérentes InnoDB), éviter `SELECT … FOR UPDATE` et les transactions longues, et paginer par clé.

### SQL et conception de bases sur RDS

#### Pourquoi les clés primaires sont-elles si importantes sur les tables RDS ?

Elles garantissent l'identité des lignes, de nombreux outils de réplication et de CDC en ont besoin pour appliquer mises à jour et suppressions, et dans InnoDB elles définissent l'organisation physique de la table. Chaque table devrait en avoir une.

#### Clés naturelles ou clés de substitution ?

Les clés de substitution (auto-incrément, identity ou UUID) sont stables et compactes ; les clés naturelles (e-mail, numéro d'identité) peuvent changer et sont souvent sensibles. Utilisez des clés primaires de substitution avec des contraintes d'unicité sur les clés naturelles.

#### UUID ou entiers comme clés primaires ?

Les entiers sont plus petits et gardent des insertions séquentielles (bon pour les index B-tree et l'organisation InnoDB). Les UUID aléatoires dispersent les insertions et gonflent les index ; les UUID ordonnés dans le temps (UUIDv7) assurent l'unicité entre systèmes avec une meilleure localité.

#### Qu'est-ce que la normalisation, et pourquoi compte-t-elle en OLTP ?

Organiser les tables pour que chaque fait ne soit stocké qu'une fois (formes normales), ce qui évite les anomalies de mise à jour et garde des transactions petites et cohérentes. Les bases OLTP sont généralement normalisées jusqu'à la troisième forme normale ; l'analytique dénormalise ensuite.

#### Comment les index accélèrent-ils les requêtes, et que coûtent-ils ?

Les index B-tree permettent de trouver des lignes par clé sans parcourir la table et aident les tris et jointures ; chaque index ralentit les écritures et consomme du stockage, donc indexez les colonnes des filtres, jointures et tris fréquents, pas tout.

#### Qu'est-ce qu'un index composite, et pourquoi l'ordre des colonnes compte-t-il ?

Un index sur plusieurs colonnes utilisé de gauche à droite : un index sur `(customer_id, created_at)` sert pour les filtres sur `customer_id` et sur `customer_id` avec une plage sur `created_at`, mais pas sur `created_at` seul.

#### Quels niveaux d'isolation les moteurs RDS utilisent-ils par défaut ?

PostgreSQL utilise read committed par défaut ; InnoDB de MySQL utilise repeatable read. Les comprendre compte pour la cohérence des extractions et le comportement en concurrence.

#### Comment éviter les interblocages (deadlocks) ?

Accéder aux tables et lignes dans un ordre cohérent, garder des transactions courtes, indexer les clés étrangères et colonnes de filtre pour verrouiller moins de lignes, et relancer les transactions qui échouent pour interblocage.

#### Que sont les suppressions logiques (soft deletes), et pourquoi comptent-elles pour les pipelines ?

Marquer des lignes comme supprimées (`deleted_at`) au lieu de les effacer. Elles rendent les suppressions visibles pour l'extraction incrémentale, mais les applications et pipelines doivent les filtrer de façon cohérente.

#### Pourquoi ajouter des colonnes `created_at` et `updated_at` à chaque table ?

Elles servent à l'audit, à l'extraction incrémentale, au débogage et aux contrôles de qualité ; `updated_at` doit être maintenue à chaque modification par l'application ou un trigger.

### Mises en situation

#### Concevez une base PostgreSQL hautement disponible pour une application de production.

RDS for PostgreSQL (ou Aurora PostgreSQL) dans des sous-réseaux privés sur plusieurs zones avec Multi-AZ (ou un cluster Multi-AZ), chiffrement avec une clé KMS gérée par le client, TLS imposé, secrets gérés par RDS avec rotation, RDS Proxy pour le pooling, sauvegardes automatiques avec 14 à 35 jours de rétention plus des copies AWS Backup dans une autre région, Database Insights, alarmes sur les métriques clés et protection contre la suppression, le tout en infrastructure as code.

#### L'équipe applicative signale des erreurs intermittentes « too many connections ». Que faites-vous ?

Je compare `DatabaseConnections` à `max_connections`, je trouve les clients qui ouvrent trop de connexions (Lambda sans pool, pools sans limite, fuites), j'introduis RDS Proxy ou un pool applicatif aux limites raisonnables, je ferme les connexions inactives, et j'augmente la taille de l'instance si la mémoire permet plus de connexions.

#### Un rapport nocturne ralentit la base de production. Comment corriger ?

Je déplace le rapport vers un réplica en lecture (ou un clone), j'optimise ses requêtes et index, ou je déplace les données vers un stockage analytique par CDC. S'il doit rester, je le planifie hors des heures de pointe et je limite ses ressources.

#### Quelqu'un a supprimé des lignes d'une table importante il y a 30 minutes. Comment les récupérer ?

Je fais une restauration à un instant donné vers une nouvelle instance juste avant la suppression, j'en extrais les lignes supprimées et je les réinsère en production (ou je bascule si c'est pertinent). Puis je revois les privilèges et j'ajoute des garde-fous.

#### Vous devez migrer une base Oracle de 2 To vers Aurora PostgreSQL avec une interruption minimale. Comment ?

J'évalue avec le Schema Conversion Tool, je convertis le schéma et le code (PL/SQL vers PL/pgSQL), je lance le chargement complet DMS plus le CDC pour garder la cible synchronisée, je valide les données (validation DMS, comptages, sommes de contrôle) et le comportement applicatif, puis je bascule pendant une courte fenêtre : arrêt des écritures, rattrapage du CDC et changement des connexions.

#### L'usage disque de RDS PostgreSQL ne cesse d'augmenter alors que les données ne changent pas. Pourquoi ?

Causes possibles : un slot de réplication logique inactif qui retient le WAL, du bloat de tables et d'index dû à un autovacuum en retard, de gros fichiers temporaires issus de requêtes lourdes, ou une longue rétention des journaux. Je vérifie `pg_replication_slots`, les estimations de bloat, `TransactionLogsDiskUsage` et la configuration des journaux.

#### Comment donner chaque jour à l'équipe analytique des copies fraîches des données de production ?

Avec le clonage rapide d'Aurora ou des restaurations de snapshots pour créer une copie séparée chaque jour (masquée si nécessaire), l'export de snapshots vers S3 en Parquet pour Athena, ou une intégration zero-ETL vers Redshift pour une analytique quasi temps réel sans toucher à la production.

#### Comment expliquer RDS à un interlocuteur non technique ?

C'est AWS qui exploite nos bases de données pour nous : il les tient à jour, sauvegardées et disponibles même si un serveur tombe, pour que l'équipe se concentre sur les données et l'application plutôt que sur la maintenance des machines.

#### Une API fondée sur Lambda sature la base de connexions lors des pics de trafic. Quelle est votre correction ?

Placer RDS Proxy entre Lambda et la base avec authentification IAM, fixer une concurrence réservée sur la fonction pour plafonner le parallélisme, réutiliser les connexions entre invocations, et envisager de mettre en cache les lectures les plus fréquentes.

#### Le retard d'un réplica de reporting atteint des heures pendant les batchs nocturnes. Que faites-vous ?

Je trouve les écritures lourdes sur la primaire (jobs batch, grosses transactions) et je les découpe en transactions plus petites, j'augmente la classe d'instance et les IOPS du réplica, j'évite sur le réplica les requêtes longues qui entrent en conflit avec le rejeu (`max_standby_streaming_delay` pour PostgreSQL), et j'envisage une copie analytique séparée.

#### Votre équipe doit passer de PostgreSQL 13 à 16 avec une interruption minimale. Comment le planifier ?

Vérifier la compatibilité des extensions et des paramètres, tester la mise à jour sur un snapshot restauré avec les tests applicatifs, puis utiliser un déploiement Blue/Green : créer l'environnement green, le mettre à jour, le laisser se synchroniser, valider et basculer dans une courte fenêtre, en gardant le blue comme retour arrière jusqu'à être confiant.

#### Une revue de sécurité découvre une instance RDS accessible publiquement. Que changez-vous ?

Désactiver l'accès public, la déplacer dans des sous-réseaux privés, restreindre les groupes de sécurité aux sources applicatives, imposer TLS, faire tourner les identifiants, examiner les journaux à la recherche d'accès suspects, et ajouter des garde-fous (règle Config, SCP) pour éviter la récidive.

#### Comment mettre en place un plan de reprise après sinistre inter-régions pour une base RDS MySQL ?

Créer un réplica en lecture inter-régions (ou Aurora Global Database pour Aurora), répliquer les sauvegardes automatiques ou copier les snapshots vers la région de secours, scripter la promotion et les changements DNS, garder l'infrastructure applicative prête dans la région de secours, et tester régulièrement le basculement au regard du RPO et du RTO.
