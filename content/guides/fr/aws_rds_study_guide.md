## Fiche d'étude Amazon RDS

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude Amazon RDS : environ 200 questions](../../images/aws_rds_study_guide_title_img.png)

Environ 200 questions d'entretien sur Amazon RDS et Aurora : moteurs, choix d'instance et de stockage, haute disponibilité avec Multi-AZ, réplicas en lecture, sauvegardes et restaurations, sécurité, supervision, performances, montée en charge, coûts, migrations, et la façon dont les data engineers extraient les données de RDS par CDC, exports et zero-ETL. Les réponses décrivent le service tel qu'il est en 2026.

La fiche suit un parcours d'apprentissage en six étapes. Chaque section est découpée en unités courtes : objectifs d'apprentissage, explication du concept et exemple commenté, puis questions (d'abord de mémorisation, ensuite d'application), un exercice pratique et les points à retenir. Pour **apprendre**, lisez chaque unité du début à la fin. Pour **réviser**, passez en mode révision ou utilisez « Aller aux questions », marquez les réponses à revoir et essayez une révision mixte entre les sections.

<!-- QA -->
<!-- stage: Fondamentaux -->

### Fondamentaux

<!-- unit: Ce que gère RDS -->

<!-- goals -->

- Expliquer ce qu'est Amazon RDS et quels moteurs il exécute.
- Répartir les responsabilités entre AWS et vous.

<!-- concept -->

Bien exploiter une base de données demande un travail de routine constant : installer, corriger, sauvegarder, remplacer le matériel en panne, monter des standbys. RDS transforme cette routine en réglages. Vous choisissez un moteur et une taille, et AWS exploite le serveur sous-jacent.

Ce qui reste de votre côté, c'est tout ce qui dépend de vos données et de votre application : conception du schéma, requêtes, index, utilisateurs et permissions, accès réseau, et les choix de sauvegarde et de disponibilité. Managé ne veut dire ni optimisé ni sécurisé par défaut.

<!-- example -->

| Tâche | Autogéré sur EC2 | RDS |
|---|---|---|
| Correctifs du système et du moteur | Vous | AWS (dans votre fenêtre de maintenance) |
| Sauvegardes et restauration à un instant donné | Vous | AWS (vous fixez la rétention) |
| Standby et basculement | Vous | AWS (si Multi-AZ) |
| Schéma, index, requêtes, utilisateurs | Vous | Vous |

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

<!-- challenge -->

Une équipe est passée à RDS et a cessé de penser à sa base. Six mois plus tard, les requêtes sont lentes et une table a été supprimée par erreur. Lequel de ces points relevait de sa responsabilité ?

<!-- solution -->

Les deux. La performance des requêtes (index, conception des requêtes) et la protection des données contre les erreurs humaines (permissions, deletion protection, rétention des sauvegardes et restaurations testées) relèvent du client sur RDS.

<!-- takeaways -->

- RDS automatise infrastructure, correctifs, sauvegardes et basculement.
- Schéma, requêtes, utilisateurs et accès restent à vous.
- Managé n'est pas synonyme d'optimisé ou de sécurisé.

<!-- unit: RDS, EC2 et variantes -->

<!-- goals -->

- Décider quand RDS est le bon choix et quand il ne l'est pas.
- Connaître RDS Custom et RDS on Outposts.

<!-- concept -->

RDS échange du contrôle contre moins de travail. On ne peut pas se connecter au serveur, installer des extensions arbitraires ni utiliser des versions inhabituelles. Pour la plupart des applications, l'échange est bon ; pour certaines bases historiques ou spécialisées, non.

AWS comble l'entre-deux : RDS Custom donne accès au système pour Oracle et SQL Server en gardant l'automatisation, et RDS on Outposts exécute le service dans votre propre centre de données. Gérer la base soi-même sur EC2 reste l'option de contrôle total, avec tout le travail qu'elle implique.

<!-- example -->

| Exigence | Option |
|---|---|
| Application PostgreSQL standard | RDS |
| Oracle avec un agent fournisseur sur le système | RDS Custom |
| Base à faible latence dans une usine | RDS on Outposts |
| Moteur non pris en charge ou configuration exotique | EC2, autogéré |

#### Quand RDS n'est-il pas le bon choix ?

Quand il faut un accès au système d'exploitation ou des extensions non prises en charge (envisagez RDS Custom ou EC2), un moteur que RDS ne propose pas, une échelle extrême au-delà d'un seul écrivain (envisagez Aurora DSQL, DynamoDB ou du sharding), ou des charges analytiques sur des téraoctets qui conviennent mieux à un entrepôt de données ou un lakehouse.

#### Quelle est la différence entre RDS et une base de données sur EC2 ?

Sur EC2, vous avez un contrôle total (système d'exploitation, toute version, toute configuration) mais vous gérez tout : installation, correctifs, sauvegardes, réplication, basculement et supervision. RDS supprime ce travail d'exploitation au prix de quelques restrictions (pas d'accès au système, privilèges superutilisateur limités, seuls les paramètres pris en charge).

#### Qu'est-ce que RDS Custom ?

Une variante de RDS pour Oracle et SQL Server qui donne accès au système d'exploitation et permet de personnaliser la base (pour des applications historiques nécessitant des correctifs ou logiciels précis), tandis qu'AWS automatise toujours les sauvegardes et une partie de la gestion.

#### Qu'est-ce qu'un DB subnet group ?

Un ensemble de sous-réseaux (dans au moins deux zones de disponibilité) d'un VPC où RDS peut placer les instances. Il est nécessaire pour créer une instance dans un VPC et pour le Multi-AZ.

<!-- challenge -->

L'application SQL Server d'un éditeur exige d'installer un agent de supervision sur le système du serveur de base. Quelle option convient, et que fournit encore AWS ?

<!-- solution -->

RDS Custom for SQL Server : il permet l'accès système pour l'agent, et AWS automatise toujours sauvegardes, supervision et une partie de la maintenance. RDS classique ne permet pas l'accès au système.

<!-- takeaways -->

- RDS échange l'accès système contre l'automatisation.
- RDS Custom ajoute l'accès système pour Oracle et SQL Server.
- EC2 donne un contrôle total et une responsabilité totale.

<!-- unit: Instances et classes -->

<!-- goals -->

- Décrire les DB instances et choisir une classe d'instance.
- Utiliser sans risque l'arrêt, la deletion protection et les tags.

<!-- concept -->

Une DB instance est l'unité que l'on paie et exploite : du calcul issu d'une classe d'instance plus le stockage attaché. Les classes forment des familles, des burstables pour une charge légère ou variable aux classes optimisées mémoire pour la plupart des bases de production, où tenir les données en mémoire décide de la performance.

Autour de l'instance, quelques réglages évitent les accidents et coûts courants : deletion protection, arrêt des instances de développement inactives (avec une limite de durée) et tags pour responsables et coûts.

<!-- example -->

```bash
aws rds create-db-instance --db-instance-identifier orders-prod \
  --engine postgres --db-instance-class db.r7g.large --allocated-storage 200 \
  --storage-type gp3 --multi-az --deletion-protection \
  --tags Key=team,Value=orders Key=env,Value=prod
```

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

<!-- challenge -->

Les bases de développement sont arrêtées le vendredi pour économiser, mais le samedi suivant elles tournent de nouveau. Pourquoi, et que faites-vous ?

<!-- solution -->

RDS redémarre les instances arrêtées après 7 jours. Planifiez un arrêt/démarrage quotidien (EventBridge Scheduler ou Instance Scheduler) par tag, ou utilisez Aurora Serverless v2 ou des snapshots pour les environnements peu utilisés.

<!-- takeaways -->

- Une instance, c'est une classe plus du stockage.
- Les classes optimisées mémoire servent la plupart des bases de production.
- Deletion protection et tags évitent accidents et coûts inconnus.

<!-- unit: Configuration et maintenance -->

<!-- goals -->

- Configurer les moteurs avec parameter groups et option groups.
- Planifier la maintenance et créer les instances en code.

<!-- concept -->

On ne peut pas modifier de fichiers de configuration sur RDS : les réglages du moteur vivent dans des parameter groups et les fonctions optionnelles dans des option groups. Utiliser des groupes personnalisés dès le premier jour compte, car les groupes par défaut ne se modifient pas et en changer plus tard peut exiger un redémarrage.

La maintenance est planifiée dans une fenêtre hebdomadaire que vous choisissez. Définir instances, groupes et fenêtres en code rend les environnements cohérents et les changements relisibles.

<!-- example -->

```bash
aws rds create-db-parameter-group --db-parameter-group-name pg16-orders \
  --db-parameter-group-family postgres16 --description "orders prod"
aws rds modify-db-parameter-group --db-parameter-group-name pg16-orders \
  --parameters "ParameterName=log_min_duration_statement,ParameterValue=500,ApplyMethod=immediate"
```

#### Qu'est-ce que la protection contre la suppression ?

Un réglage qui empêche la suppression d'une instance ou d'un cluster tant qu'il n'est pas désactivé, protégeant les bases de production d'une suppression accidentelle.

#### Qu'est-ce que le modèle de responsabilité partagée pour RDS ?

AWS est responsable de l'infrastructure, du système d'exploitation, des correctifs du logiciel de base, des sauvegardes et des mécanismes de réplication. Vous êtes responsable de l'accès réseau (groupes de sécurité), des choix de chiffrement, des utilisateurs et privilèges de la base, de la conception du schéma et des requêtes, des paramètres et de la protection des identifiants.

#### Comment vous connecter depuis votre ordinateur à une instance RDS dans un sous-réseau privé ?

Via un bastion ou, mieux, la redirection de port d'AWS Systems Manager Session Manager vers une instance du VPC, un VPN client, ou une machine EC2 dans le VPC ; jamais en rendant la base publique.

#### Que signifie « publicly accessible » pour une instance RDS ?

L'instance reçoit une IP publique et son endpoint la résout depuis l'extérieur du VPC : elle est joignable depuis Internet si les groupes de sécurité le permettent. Les bases de production doivent garder ce réglage désactivé.

<!-- challenge -->

Vous devez modifier un paramètre statique (`shared_buffers`) sur une instance de production qui utilise le parameter group par défaut. Quelles étapes ?

<!-- solution -->

Créer un parameter group personnalisé, y fixer la valeur, l'attacher à l'instance et redémarrer (de préférence dans la fenêtre de maintenance), car les paramètres statiques ne s'appliquent qu'après redémarrage.

<!-- takeaways -->

- Les parameter groups portent les réglages ; les option groups, les fonctions.
- Utilisez des groupes personnalisés dès le départ.
- Choisissez une fenêtre de maintenance et gérez tout en code.

<!-- unit: Réseau et connectivité -->

<!-- goals -->

- Placer RDS dans un VPC avec subnet groups et endpoints.
- Se connecter en sécurité à des instances privées.

<!-- concept -->

Une instance RDS vit dans votre VPC, dans des sous-réseaux choisis via un subnet group couvrant au moins deux zones. Les applications se connectent par un endpoint, un nom DNS qui continue de fonctionner quand RDS déplace l'instance lors d'un basculement.

Les bases de production vont dans des sous-réseaux privés sans accès public. Les personnes qui doivent s'y connecter passent par le port forwarding de Session Manager ou un bastion plutôt que d'ouvrir la base à Internet.

<!-- example -->

```bash
aws ssm start-session --target i-0bastion123 \
  --document-name AWS-StartPortForwardingSessionToRemoteHost \
  --parameters '{"host":["orders-prod.abc123.eu-west-1.rds.amazonaws.com"],"portNumber":["5432"],"localPortNumber":["5432"]}'
psql -h localhost -U analyst orders
```

#### Comment créer des instances RDS de façon reproductible ?

Avec l'infrastructure as code (CloudFormation, CDK, Terraform), en définissant subnet groups, parameter groups, groupes de sécurité, clés KMS, secrets et l'instance, pour que les environnements soient cohérents et les changements relus.

#### À quoi servent les tags RDS ?

À l'imputation des coûts, au contrôle d'accès (conditions IAM sur les tags), à l'automatisation (par exemple arrêter la nuit les instances taguées `env=dev`) et à l'identification des responsables.

#### Qu'est-ce que RDS on Outposts ?

RDS exécuté sur du matériel AWS Outposts dans votre propre centre de données, pour les charges qui exigent une faible latence vers des systèmes on-premise ou la résidence des données, géré avec les mêmes API.

#### Quels types de stockage RDS propose-t-il ?

Le SSD généraliste gp3 (base de 3 000 IOPS et 125 Mio/s, IOPS et débit configurables indépendamment de la taille), gp2 (IOPS liées à la taille avec crédits de rafale), les IOPS provisionnées io1 et io2 Block Express (IOPS élevées et constantes, faible latence) et l'ancien stockage magnétique.

<!-- challenge -->

Une application se connecte à RDS par l'IP de l'instance et casse après chaque basculement. Que devrait-elle utiliser ?

<!-- solution -->

Le nom DNS de l'endpoint RDS. Lors du basculement, RDS redirige l'endpoint vers le nouveau primaire ; les IP changent. Gardez aussi un cache DNS court dans l'application.

<!-- takeaways -->

- Les subnet groups couvrent au moins deux zones.
- Connectez-vous toujours par l'endpoint, jamais par IP.
- Gardez les bases de production privées ; passez par des tunnels.

### Stockage

<!-- unit: Types de stockage et IOPS -->

<!-- goals -->

- Choisir entre stockage gp3, gp2 et io1/io2.
- Lire les métriques d'IOPS et de file pour dimensionner le stockage.

<!-- concept -->

Les bases de données sont souvent limitées par la vitesse de lecture et d'écriture des blocs, pas par le CPU. Les types de stockage RDS diffèrent par la façon de fixer cette vitesse : gp3 offre une base réglable indépendamment de la taille, l'ancien gp2 lie la vitesse à la taille avec des crédits de rafale, et io1/io2 garantissent des IOPS à faible latence pour les charges exigeantes.

Les métriques disent dans quel cas vous êtes : une file et une latence élevées signifient que le disque ne suit pas.

<!-- example -->

```text
ReadIOPS + WriteIOPS at peak:  5,200
gp3 baseline:                  3,000  → raise gp3 IOPS to ~6,000
DiskQueueDepth:                 35    (was 2)  → storage is the bottleneck
```

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

<!-- challenge -->

Une base gp2 de 100 Go est rapide le matin et lente chaque après-midi pendant les chargements batch. Que se passe-t-il, et que changez-vous ?

<!-- solution -->

La base de gp2 est de 300 IOPS pour 100 Go ; les chargements épuisent les crédits de rafale et la performance retombe à la base. Passer en gp3 (base de 3 000 IOPS, réglable) ou en io2 si la latence doit être constante.

<!-- takeaways -->

- gp3 découple IOPS et taille ; gp2 dépend des rafales.
- io1/io2 garantissent les IOPS pour les charges exigeantes.
- Une file élevée signale que le stockage est le goulot.

<!-- unit: Faire grandir et modifier le stockage -->

<!-- goals -->

- Éviter la saturation du stockage avec le storage autoscaling.
- Savoir ce que les modifications de stockage peuvent faire ou non.

<!-- concept -->

Manquer d'espace bloque les écritures, d'où le storage autoscaling jusqu'à un maximum que vous fixez. Grandir est facile ; réduire, non : le stockage alloué ne peut qu'augmenter, et le diminuer suppose de déplacer les données vers une nouvelle instance.

Les changements de taille ou de type se font en général en ligne, mais l'instance passe par une phase d'optimisation et un délai s'impose avant le changement suivant. Planifiez les modifications de stockage au lieu de les faire en plein incident.

<!-- example -->

```bash
aws rds modify-db-instance --db-instance-identifier orders-prod \
  --max-allocated-storage 1000 --apply-immediately     # enable autoscaling up to 1 TB
```

#### Comment gp3 se compare-t-il à io2 pour RDS ?

gp3 offre une base de 3 000 IOPS et 125 Mio/s, configurable jusqu'à des limites plus élevées moyennant un surcoût, à un prix au Go plus bas. io2 Block Express offre des IOPS plus élevées et plus constantes et une latence plus faible avec une meilleure durabilité, pour les charges les plus exigeantes.

#### Qu'indique `DiskQueueDepth` ?

Le nombre de requêtes d'E/S en attente du disque. Une file constamment élevée avec une latence élevée signifie que le stockage ne suit pas ; envisagez plus d'IOPS, de meilleures requêtes ou du cache.

#### Quel est l'impact d'une modification du stockage sur une instance en service ?

Augmenter le stockage ou changer de type se fait généralement en ligne, mais l'instance peut passer des heures en état « storage-optimization », pendant lequel aucune autre modification du stockage n'est possible ; les performances peuvent être légèrement affectées.

#### Comment estimer les IOPS nécessaires ?

À partir des métriques actuelles (`ReadIOPS` + `WriteIOPS` en pointe) ou, pour une nouvelle charge, des transactions par seconde attendues et des E/S par transaction, avec de la marge ; puis tester sous charge avant la production.

#### Qu'est-ce qu'un déploiement Multi-AZ d'instance ?

RDS maintient une réplique standby synchrone de la primaire dans une autre zone de disponibilité. Si la primaire tombe (matériel, panne de la zone, défaillance du stockage) ou lors de certaines maintenances, RDS bascule automatiquement sur la standby, généralement en une à deux minutes. La standby ne sert pas de lectures.

<!-- challenge -->

Une équipe a alloué 4 To « par sécurité » à une base qui en utilise 300 Go. Peut-elle réduire, et comment ?

<!-- solution -->

Pas sur place. Créer une nouvelle instance avec moins de stockage et l'autoscaling activé, migrer les données (dump et restore, DMS ou réplication), basculer l'application, puis supprimer l'ancienne instance.

<!-- takeaways -->

- Le storage autoscaling évite les pannes « storage-full ».
- Le stockage alloué peut grandir mais pas diminuer.
- Les modifications déclenchent optimisation et délais.

<!-- stage: Disponibilité et protection des données -->

### Haute disponibilité et Multi-AZ

<!-- unit: Déploiements Multi-AZ -->

<!-- goals -->

- Expliquer les déploiements Multi-AZ d'instance et de cluster.
- Décrire le fonctionnement du basculement et les RPO et RTO obtenus.

<!-- concept -->

Le Multi-AZ protège contre la perte d'un serveur ou d'une zone de disponibilité entière. RDS garde un standby dans une autre zone avec une réplication synchrone : chaque écriture validée existe aux deux endroits. Quand le primaire tombe, le standby est promu et l'endpoint pointe vers lui.

Dans la variante instance, le standby est invisible et ne fait qu'attendre. La variante cluster a deux standbys lisibles et bascule plus vite. Dans les deux cas, le RPO est quasi nul et la reprise prend une à deux minutes.

<!-- example -->

```text
AZ a: primary  ── synchronous replication ──►  AZ b: standby
         ▲
endpoint orders-prod.xxxx.rds.amazonaws.com  (DNS flips to b on failover)
```

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

<!-- challenge -->

Le métier exige « aucune perte de données et moins de 5 minutes d'arrêt » si une zone tombe. Le Multi-AZ le permet-il ?

<!-- solution -->

Oui. La réplication synchrone donne un RPO quasi nul, et le basculement se termine en général en une à deux minutes (plus vite avec les Multi-AZ DB clusters), dans l'objectif des 5 minutes.

<!-- takeaways -->

- Le Multi-AZ garde un standby synchrone dans une autre zone.
- Le basculement promeut le standby et redirige l'endpoint.
- RPO ≈ 0 ; RTO d'environ 1 à 2 minutes.

<!-- unit: Vivre avec le basculement -->

<!-- goals -->

- Préparer les applications au basculement et le tester.
- Savoir contre quoi le Multi-AZ ne protège pas.

<!-- concept -->

Le basculement n'est que la moitié de l'histoire ; l'application doit se reconnecter. Des clients qui gardent longtemps le DNS en cache, tiennent des connexions sans relance ou codent des IP en dur transforment un basculement d'une minute en longue panne. Un basculement forcé en test le révèle avant que cela compte.

Le Multi-AZ a aussi des limites nettes. Dans le schéma classique, le standby ne sert pas de lectures : ce n'est pas du passage à l'échelle. Il réplique fidèlement les erreurs : ce n'est pas une sauvegarde. Les sinistres régionaux demandent un plan de reprise distinct.

<!-- example -->

```bash
aws rds reboot-db-instance --db-instance-identifier orders-prod --force-failover
# then watch: app errors, reconnect time, connection pool behavior
```

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

#### Qu'est-ce qu'un réplica en lecture ?

Une copie d'une instance source maintenue à jour par réplication asynchrone, utilisée pour décharger le trafic de lecture (rapports, analytique, API très lues). Il a son propre endpoint et peut être dans la même région ou une autre.

<!-- challenge -->

Après un basculement de test, la base revient en 60 secondes, mais l'application Java échoue encore pendant 15 minutes. Cause probable ?

<!-- solution -->

La JVM met le DNS en cache (parfois indéfiniment) et se connecte toujours à l'IP de l'ancien primaire. Fixez un TTL DNS court dans la JVM, ajoutez des relances et envisagez l'AWS Advanced JDBC Wrapper pour détecter plus vite le basculement.

<!-- takeaways -->

- Les applications doivent se reconnecter vite ; testez-le.
- Le Multi-AZ n'est ni montée en charge des lectures ni sauvegarde.
- Haute disponibilité n'est pas reprise après sinistre.

### Réplicas en lecture

<!-- unit: Réplicas et retard -->

<!-- goals -->

- Expliquer réplicas en lecture, retard de réplication et lectures périmées.
- Router les lectures vers les réplicas sans risque.

<!-- concept -->

Les réplicas en lecture copient les changements du primaire de façon asynchrone, ce qui leur permet de servir des lectures sans ralentir les écritures. Le prix, c'est le retard : un réplica a toujours un peu de retard, parfois beaucoup, et relire sa propre écriture juste après peut échouer.

Cela façonne leur usage. Les requêtes de lecture qui tolèrent un léger retard vont aux réplicas ; tout ce qui doit voir la dernière écriture va au primaire.

<!-- example -->

```python
WRITER = "orders-prod.xxxx.rds.amazonaws.com"
READER = "orders-replica-1.xxxx.rds.amazonaws.com"

def get_order_after_payment(order_id):
    return query(WRITER, "SELECT * FROM orders WHERE id = %s", order_id)  # must be fresh

def list_catalog():
    return query(READER, "SELECT * FROM products WHERE active")             # lag is fine
```

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

<!-- challenge -->

Après avoir déplacé les lectures vers un réplica, les utilisateurs ne voient parfois pas le commentaire qu'ils viennent de publier. Comment corriger sans abandonner les réplicas ?

<!-- solution -->

Envoyer au primaire les lectures qui suivent une écriture de l'utilisateur lui-même (read-your-writes), par exemple quelques secondes après l'écriture ou pour la session de cet utilisateur, et garder les autres lectures sur le réplica.

<!-- takeaways -->

- Les réplicas répliquent de façon asynchrone et ont du retard.
- Routez au primaire les lectures qui exigent la fraîcheur.
- Les réplicas exigent des sauvegardes automatiques sur la source.

<!-- unit: Topologies de réplicas -->

<!-- goals -->

- Utiliser des réplicas entre régions, en Multi-AZ et en copies différées.
- Promouvoir des réplicas et savoir comment ils réagissent au basculement.

<!-- concept -->

Les réplicas font plus que monter en charge les lectures. Dans une autre région, ils rapprochent les données des utilisateurs et fournissent une copie de reprise à promouvoir. En Multi-AZ eux-mêmes, ils survivent aux pannes de zone. Différés, ils gardent une fenêtre où les erreurs du primaire ne sont pas encore arrivées.

La promotion est une porte à sens unique : le réplica devient une base indépendante et la réplication s'arrête.

<!-- example -->

```bash
aws rds create-db-instance-read-replica --db-instance-identifier orders-dr \
  --source-db-instance-identifier arn:aws:rds:eu-west-1:123456789012:db:orders-prod \
  --region eu-central-1 --kms-key-id alias/rds-dr
# during a regional disaster:
aws rds promote-read-replica --db-instance-identifier orders-dr --region eu-central-1
```

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

<!-- challenge -->

Quelqu'un a lancé un `UPDATE` sans `WHERE` sur MySQL il y a 10 minutes. Un réplica différé d'une heure existe. Comment peut-il aider ?

<!-- solution -->

Arrêter la réplication sur le réplica différé avant qu'il n'applique l'instruction fautive, appliquer les changements jusqu'à juste avant, puis recopier les lignes correctes vers le primaire (ou promouvoir le réplica si nécessaire).

<!-- takeaways -->

- Les réplicas inter-régions servent les lectures lointaines et la reprise.
- La promotion rend le réplica indépendant ; la réplication s'arrête.
- Les réplicas différés laissent une fenêtre pour réparer les erreurs.

<!-- unit: Réplicas pour l'analytique -->

<!-- goals -->

- Décharger rapports et extractions sur des réplicas.
- Gérer le retard causé par de lourdes écritures sur le primaire.

<!-- concept -->

Analytique et transactions se disputent les mêmes CPU, mémoire et I/O. Un réplica dimensionné pour le reporting sort les requêtes lourdes du primaire pour que les clients ne les sentent pas.

Mais les réplicas partagent la charge d'écriture du primaire : chaque changement doit être rejoué. De gros lots d'écritures ou de longues transactions sur le primaire se traduisent en retard sur le réplica, et de longues requêtes sur le réplica peuvent retarder encore le rejeu.

<!-- example -->

```sql
-- on the primary: break one huge update into batches
UPDATE orders SET status = 'archived'
WHERE id IN (SELECT id FROM orders WHERE created_at < '2024-01-01' AND status <> 'archived' LIMIT 10000);
-- repeat until 0 rows; replicas apply each small transaction quickly
```

#### Que sont les sauvegardes automatiques ?

Des snapshots quotidiens de l'instance plus les journaux de transactions capturés toutes les quelques minutes, conservés pendant une période configurable (1 à 35 jours ; 0 les désactive), qui permettent la restauration à un instant donné dans la fenêtre de rétention.

#### Qu'est-ce que la restauration à un instant donné (PITR) ?

Restaurer la base à n'importe quelle seconde de la période de rétention (jusqu'à environ cinq minutes avant maintenant), ce qui crée une nouvelle instance avec un nouvel endpoint. C'est l'outil principal pour se remettre de modifications accidentelles.

#### Que sont les snapshots manuels ?

Des snapshots lancés par l'utilisateur, conservés jusqu'à leur suppression, indépendamment de la rétention des sauvegardes automatiques. On les utilise avant des changements risqués, pour la conservation longue et pour copier ou partager des bases.

<!-- challenge -->

Les analystes ont besoin des données de la veille à 07:00, mais le retard du réplica atteint trois heures pendant le batch nocturne. Citez deux changements.

<!-- solution -->

Découper les grosses transactions du batch en plus petites (et les programmer plus tôt), et donner au réplica assez d'I/O et de CPU pour rejouer les changements. Si la fraîcheur à la minute n'est pas nécessaire, un export quotidien de snapshot vers S3 évite le problème.

<!-- takeaways -->

- Les réplicas sortent l'analytique du primaire.
- Les grosses transactions du primaire créent du retard.
- Pour l'analytique quotidienne, exports ou lake peuvent mieux convenir.

### Sauvegardes et restauration

<!-- unit: Sauvegardes automatiques et restauration à un instant donné -->

<!-- goals -->

- Expliquer les sauvegardes automatiques et la restauration à un instant donné.
- Récupérer d'une suppression accidentelle et comprendre les restaurations.

<!-- concept -->

Les sauvegardes automatiques combinent un snapshot quotidien et des journaux de transactions enregistrés toutes les quelques minutes, ce qui permet à RDS de reconstruire la base à n'importe quelle seconde de la période de rétention. C'est la principale protection contre les erreurs humaines, puisque les réplicas copient aussi les erreurs.

Les restaurations n'écrasent jamais : elles créent une nouvelle instance, qui démarre vite mais charge ses données à la demande depuis S3, d'où des premières requêtes lentes. Récupérer quelques lignes, c'est restaurer à côté de la production et les recopier.

<!-- example -->

```bash
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier orders-prod \
  --target-db-instance-identifier orders-restore-0930 \
  --restore-time 2026-10-17T09:29:00Z
pg_dump -h orders-restore-0930... -t public.invoices --data-only | psql -h orders-prod...
```

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

<!-- challenge -->

Une instance restaurée pour un test de sinistre répond très lentement pendant la première heure. Y a-t-il un problème ?

<!-- solution -->

Non, c'est le lazy loading : les blocs sont récupérés depuis S3 au premier accès. Préchauffez-la en lisant les tables importantes (par exemple scans complets ou `pg_prewarm`) avant d'envoyer le vrai trafic.

<!-- takeaways -->

- Les sauvegardes automatiques permettent de restaurer toute seconde de la rétention.
- Les restaurations créent de nouvelles instances.
- Le stockage restauré se charge à la demande ; préchauffez-le.

<!-- unit: Snapshots et rétention -->

<!-- goals -->

- Gérer snapshots manuels, copies et rétention longue.
- Protéger les sauvegardes entre régions et comptes.

<!-- concept -->

Les sauvegardes automatiques expirent avec leur rétention ; les snapshots manuels restent jusqu'à leur suppression. Les besoins de long terme et de conformité reposent donc sur des snapshots, idéalement gérés par AWS Backup avec politiques, coffres et verrous qui empêchent leur suppression.

Une sauvegarde dans le même compte et la même région partage leur sort : des copies vers une autre région ou un autre compte protègent des pannes régionales et des comptes compromis. Supprimer une instance est le moment de décider quoi garder.

<!-- example -->

```bash
aws rds copy-db-snapshot \
  --source-db-snapshot-identifier arn:aws:rds:eu-west-1:123456789012:snapshot:orders-2026-10 \
  --target-db-snapshot-identifier orders-2026-10-dr --kms-key-id alias/rds-dr \
  --region eu-central-1
```

#### Qu'est-ce que le chargement différé (lazy loading) après une restauration ?

Quand une instance est restaurée depuis un snapshot, ses blocs de stockage sont récupérés depuis S3 au premier accès : les lectures initiales ont une latence plus élevée. Lancer des lectures complètes des tables après la restauration préchauffe le stockage.

#### Comment conserver des sauvegardes sept ans pour la conformité ?

Avec AWS Backup et un plan de rétention long avec vault lock, ou en copiant régulièrement des snapshots manuels ; les sauvegardes automatiques plafonnent à 35 jours. L'export vers S3 avec des règles de cycle de vie peut aussi servir à l'archivage.

#### Peut-on restaurer une seule table depuis une sauvegarde ?

Pas directement. Restaurez toute l'instance dans une nouvelle (à un instant donné), puis faites un dump de la table voulue et importez-la en production.

#### Qu'est-ce que la réplication inter-régions des sauvegardes automatiques ?

Une fonction qui copie les sauvegardes automatiques et les journaux de transactions vers une autre région, pour pouvoir faire une restauration à un instant donné dans la région de secours.

#### Comment contrôler l'accès réseau à RDS ?

Placer les instances dans des sous-réseaux privés, désactiver l'accès public, et utiliser des groupes de sécurité VPC qui n'autorisent que les groupes de sécurité de l'application ou des plages CIDR précises sur le port de la base. L'accès depuis l'on-premise passe par VPN ou Direct Connect.

#### Comment les données sont-elles chiffrées au repos dans RDS ?

Avec des clés AWS KMS (gérées par AWS ou par le client), qui couvrent le stockage, les sauvegardes automatiques, les snapshots, les réplicas en lecture et les journaux. Le chiffrement se choisit à la création.

#### Comment chiffrer une instance RDS existante non chiffrée ?

Prendre un snapshot, le copier avec chiffrement activé à l'aide d'une clé KMS et restaurer une nouvelle instance depuis la copie chiffrée ; puis basculer les applications. Les réplicas d'une instance non chiffrée ne peuvent pas être chiffrés directement.

<!-- challenge -->

Un ransomware a supprimé l'instance et ses snapshots via un compte administrateur compromis. Quelle conception aurait sauvé les données ?

<!-- solution -->

Des copies des sauvegardes dans un compte séparé (et une autre région) avec un vault lock AWS Backup, pour que même un administrateur du compte de production ne puisse pas les supprimer. À combiner avec moindre privilège et MFA sur les rôles d'administration.

<!-- takeaways -->

- Snapshots manuels et AWS Backup servent la rétention longue.
- Copiez les sauvegardes vers une autre région et un autre compte.
- Les vault locks protègent les sauvegardes de la suppression.

### Sécurité

<!-- unit: Accès réseau -->

<!-- goals -->

- Restreindre l'accès réseau à RDS avec sous-réseaux et security groups.
- Connecter Lambda et corriger les instances publiquement accessibles.

<!-- concept -->

La première couche de sécurité, c'est l'accessibilité. Des bases dans des sous-réseaux privés sans accès public ne sont joignables que depuis le réseau, et les security groups restreignent encore à des groupes d'applications précis plutôt qu'à des plages d'IP.

Référencer des security groups plutôt que des adresses garde les règles justes quand instances et fonctions montent en charge et changent d'IP.

<!-- example -->

```text
sg-app     (attached to ECS tasks and Lambda)
sg-db      inbound: TCP 5432 from sg-app   ← no CIDR ranges, no 0.0.0.0/0
RDS:       private subnets, PubliclyAccessible = false
```

#### Comment les données sont-elles chiffrées en transit ?

Par des connexions SSL/TLS utilisant le bundle d'autorités de certification RDS. On peut imposer TLS avec des paramètres comme `rds.force_ssl` (PostgreSQL, SQL Server) ou `require_secure_transport` (MySQL). Il faut renouveler les certificats quand RDS change ses autorités.

#### Qu'est-ce que l'authentification IAM à la base de données ?

Pour MySQL, MariaDB et PostgreSQL (et Aurora), les utilisateurs s'authentifient avec un jeton de courte durée généré à partir d'identifiants IAM au lieu d'un mot de passe : l'accès se contrôle par des politiques IAM et aucun mot de passe de base n'est stocké dans les applications.

#### Comment gérer les mots de passe de la base ?

Avec Secrets Manager, idéalement avec des mots de passe de l'utilisateur maître gérés par RDS (RDS crée et fait tourner le secret), en faisant tourner automatiquement les secrets des utilisateurs applicatifs, et sans jamais coder d'identifiants en dur.

<!-- challenge -->

Le security group d'une base autorise `0.0.0.0/0` sur le port 3306 « temporairement » pour un prestataire. Par quoi le remplacez-vous ?

<!-- solution -->

Supprimer la règle, garder l'instance privée et donner accès au prestataire via le port forwarding de Session Manager (ou un client VPN) avec une identité IAM, pour un accès authentifié et journalisé.

<!-- takeaways -->

- D'abord sous-réseaux privés et pas d'accès public.
- Les security groups doivent référencer d'autres security groups.
- Donnez l'accès par tunnels, pas par ports ouverts.

<!-- unit: Chiffrement -->

<!-- goals -->

- Chiffrer les données RDS au repos et en transit.
- Chiffrer les instances existantes et imposer le chiffrement par politique.

<!-- concept -->

Le chiffrement au repos avec KMS couvre stockage, sauvegardes, snapshots et réplicas, et ne se choisit qu'à la création d'une instance. Chiffrer une base existante suppose donc de copier un snapshot avec chiffrement et de le restaurer.

Le chiffrement en transit repose sur TLS, que l'on peut exiger par paramètres. Des politiques rendent le chiffrement obligatoire, et des clés gérées par le client sont nécessaires pour partager des snapshots chiffrés entre comptes.

<!-- example -->

```bash
aws rds copy-db-snapshot --source-db-snapshot-identifier orders-plain \
  --target-db-snapshot-identifier orders-encrypted --kms-key-id alias/rds-prod
aws rds restore-db-instance-from-db-snapshot --db-instance-identifier orders-prod-enc \
  --db-snapshot-identifier orders-encrypted
# PostgreSQL: rds.force_ssl = 1 in the parameter group
```

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

<!-- challenge -->

Vous devez partager un snapshot chiffré avec un compte d'analytique, mais la copie échoue. Qu'est-ce qui ne va pas ?

<!-- solution -->

Le snapshot est chiffré avec la clé gérée par AWS pour RDS, qui ne se partage pas. Copiez-le avec une clé KMS gérée par le client, accordez à l'autre compte l'usage de cette clé, puis partagez le snapshot.

<!-- takeaways -->

- Le chiffrement au repos se choisit à la création ; copiez pour le changer.
- Exigez TLS par les paramètres du moteur.
- Les snapshots chiffrés partagés exigent des clés gérées par le client.

<!-- unit: Authentification et utilisateurs de base -->

<!-- goals -->

- Choisir entre mots de passe, authentification IAM et Kerberos.
- Concevoir des utilisateurs de base au moindre privilège.

<!-- concept -->

Qui se connecte compte autant que d'où. Les mots de passe doivent vivre dans Secrets Manager avec rotation, idéalement gérée par RDS lui-même. L'authentification IAM remplace les mots de passe par des jetons de courte durée liés à des rôles IAM ; Kerberos rattache les connexions à un annuaire d'entreprise.

Dans la base, l'utilisateur maître sert uniquement à l'administration. Chaque application reçoit son propre utilisateur avec les seuls privilèges nécessaires, ce qui limite les dégâts et donne du sens aux journaux d'audit.

<!-- example -->

```sql
CREATE ROLE orders_app LOGIN;
GRANT CONNECT ON DATABASE shop TO orders_app;
GRANT USAGE ON SCHEMA orders TO orders_app;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA orders TO orders_app;
GRANT rds_iam TO orders_app;           -- PostgreSQL: allow IAM token authentication
```

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

<!-- challenge -->

Trois services et cinq analystes utilisent tous l'utilisateur maître. Que changez-vous d'abord ?

<!-- solution -->

Créer un utilisateur par service et par groupe d'analystes avec les seuls privilèges nécessaires (lecture seule pour les analystes), stocker les identifiants dans Secrets Manager ou utiliser l'authentification IAM, puis changer le mot de passe maître et restreindre son usage.

<!-- takeaways -->

- Stockez et renouvelez les mots de passe avec Secrets Manager.
- IAM et Kerberos remplacent les mots de passe statiques.
- Un utilisateur au moindre privilège par application.

<!-- unit: Audit et garde-fous -->

<!-- goals -->

- Auditer l'activité de la base et les changements par API.
- Empêcher les modifications risquées des ressources RDS.

<!-- concept -->

Deux types d'activité sont à surveiller. Dans le moteur, journaux d'audit et activity streams enregistrent qui a lu ou modifié les données. Autour, CloudTrail enregistre qui a modifié instances, snapshots et réglages.

Les garde-fous arrêtent les erreurs avant toute enquête : politiques IAM qui limitent qui peut modifier ou supprimer les bases de production, deletion protection et rôles ou comptes séparés pour la production.

<!-- example -->

```json
{
  "Effect": "Deny",
  "Action": ["rds:DeleteDBInstance", "rds:ModifyDBInstance"],
  "Resource": "arn:aws:rds:*:*:db:*",
  "Condition": {"StringEquals": {"aws:ResourceTag/env": "prod"},
                "StringNotEquals": {"aws:PrincipalTag/role": "dba"}}
}
```

#### Quelles métriques CloudWatch sont les plus importantes pour RDS ?

`CPUUtilization`, `FreeableMemory`, `FreeStorageSpace`, `ReadIOPS`/`WriteIOPS`, `ReadLatency`/`WriteLatency`, `DiskQueueDepth`, `DatabaseConnections`, `ReplicaLag`, `SwapUsage` et, pour les classes extensibles, `CPUCreditBalance`.

#### Qu'est-ce qu'Enhanced Monitoring ?

Des métriques au niveau du système d'exploitation (CPU et mémoire par processus, système de fichiers, swap, E/S disque) collectées par un agent jusqu'à chaque seconde et envoyées dans CloudWatch Logs, qui aident à trouver des causes invisibles dans les métriques standard.

#### Qu'est-ce que Performance Insights / Database Insights ?

Un outil de performance qui montre la charge de la base (sessions actives moyennes) ventilée par événements d'attente, requêtes SQL, utilisateurs et hôtes, pour voir quelles requêtes génèrent la charge et pourquoi. Il fait désormais partie de CloudWatch Database Insights, qui ajoute en mode avancé des vues sur toute la flotte et une rétention plus longue.

#### Comment trouver les requêtes lentes dans RDS ?

Activer les journaux de requêtes lentes (`slow_query_log` et `long_query_time` pour MySQL, `log_min_duration_statement` pour PostgreSQL), utiliser `pg_stat_statements` ou le Performance Schema, et analyser le top SQL de Database Insights ; puis lancer `EXPLAIN` pour corriger plans et index.

<!-- challenge -->

Un développeur a redimensionné une base de production en pleine journée, provoquant une panne. Quels contrôles l'empêchent ?

<!-- solution -->

Une politique IAM refusant `rds:ModifyDBInstance` sur les instances taguées prod sauf pour un rôle de DBA, des changements déployés par IaC avec revue, et des modifications planifiées dans la fenêtre de maintenance au lieu d'être appliquées immédiatement.

<!-- takeaways -->

- Journaux d'audit et activity streams tracent l'accès aux données.
- CloudTrail trace les changements des ressources RDS.
- Garde-fous IAM et IaC empêchent les changements risqués.

<!-- stage: Exploiter RDS -->

### Supervision et performances

<!-- unit: Métriques, journaux et événements -->

<!-- goals -->

- Savoir quelles métriques, outils et journaux surveiller sur RDS.
- Configurer alertes et notifications d'événements.

<!-- concept -->

RDS offre trois niveaux de visibilité. Les métriques CloudWatch montrent les signes vitaux de l'instance. Enhanced Monitoring montre le système sous-jacent, par processus. Performance Insights montre ce qui occupe la base, réparti par attentes et requêtes, et c'est généralement là qu'est la réponse.

Journaux et événements complètent le tableau : les slow query logs montrent les instructions coûteuses et les notifications d'événements signalent basculements, redémarrages et alertes de stockage au moment où ils surviennent.

<!-- example -->

| Métrique | Inquiétez-vous quand |
|---|---|
| `CPUUtilization` | durablement > 80 % |
| `FreeableMemory` | basse et `SwapUsage` en hausse |
| `FreeStorageSpace` | sous 15 % |
| `DatabaseConnections` | proche de `max_connections` |
| `ReadLatency` / `WriteLatency` | en hausse avec `DiskQueueDepth` |
| `ReplicaLag` | au-delà de ce que tolèrent les lecteurs |

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

<!-- challenge -->

Le CPU d'une base est à 95 % et l'équipe prévoit de doubler la taille de l'instance. Que vérifiez-vous d'abord ?

<!-- solution -->

Performance Insights : quelles requêtes et quels événements d'attente composent la charge. Souvent, quelques requêtes sans index ou avec de mauvais plans dominent ; les corriger coûte moins qu'une instance plus grosse.

<!-- takeaways -->

- Métriques pour les signes vitaux, Enhanced Monitoring pour le système, Insights pour la charge.
- Les slow query logs trouvent les instructions coûteuses.
- Alertez sur CPU, mémoire, stockage, connexions, latence et retard.

<!-- unit: Diagnostiquer la charge -->

<!-- goals -->

- Trouver les causes d'un CPU élevé et d'une mémoire faible.
- Repérer requêtes lentes et attentes de verrous.

<!-- concept -->

La charge d'une base a peu de causes profondes : des requêtes qui travaillent trop, trop de sessions simultanées, pas assez de mémoire pour l'ensemble de travail, et des sessions qui s'attendent mutuellement. Les outils désignent laquelle. Performance Insights montre requêtes et attentes principales ; slow logs et statistiques de requêtes montrent les instructions les plus coûteuses ; les métriques mémoire disent si le cache suffit.

Corriger la cause, en général une requête ou un index, vaut mieux qu'ajouter du matériel.

<!-- example -->

```sql
-- PostgreSQL: top statements by total time
SELECT left(query, 80) AS query, calls, round(total_exec_time) AS total_ms, round(mean_exec_time) AS mean_ms
FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 10;
```

#### Comment régler MySQL sur RDS ?

Dimensionner `innodb_buffer_pool_size` (environ 75 % de la mémoire par défaut), revoir `max_connections`, utiliser des index et plans adaptés, surveiller le journal des requêtes lentes, et éviter les transactions longues qui font grossir les undo logs.

#### Pourquoi l'autovacuum est-il important sur RDS PostgreSQL ?

Le MVCC de PostgreSQL laisse des tuples morts après les mises à jour et suppressions ; l'autovacuum les récupère et évite le bouclage des identifiants de transaction. S'il prend du retard, les tables gonflent et, au pire, la base refuse les écritures pour éviter le bouclage. Réglez-le pour les grosses tables actives.

#### Qu'est-ce que `FreeableMemory`, et quand faut-il s'en inquiéter ?

La RAM disponible sur l'instance. Peu de mémoire libre avec un `SwapUsage` en hausse signifie que la charge ne tient pas (buffer pool, connexions, tris) ; augmentez la taille ou réduisez la consommation mémoire.

#### Comment les verrous apparaissent-ils dans les outils de performance RDS ?

Sous forme d'événements d'attente (par exemple `Lock:transactionid` ou `Lock:relation` pour PostgreSQL, `synch/cond/innodb/row_lock_wait` pour MySQL) dans Database Insights ; des requêtes sur `pg_locks` avec `pg_stat_activity` montrent qui bloque qui.

<!-- challenge -->

Performance Insights montre l'essentiel de la charge en attentes `Lock:transactionid` sur PostgreSQL. Qu'est-ce que cela signifie, et que cherchez-vous ?

<!-- solution -->

Des sessions attendent le commit ou le rollback d'autres transactions, généralement sur les mêmes lignes. Cherchez les sessions longues ou idle in transaction qui tiennent des verrous (`pg_stat_activity`, `pg_locks`), et raccourcissez ou réordonnez les transactions concernées.

<!-- takeaways -->

- L'essentiel de la charge vient de requêtes coûteuses ou de trop de sessions.
- `pg_stat_statements` et les slow logs classent les requêtes coûteuses.
- Les attentes de verrous désignent des transactions longues ou en conflit.

<!-- unit: Connexions et RDS Proxy -->

<!-- goals -->

- Diagnostiquer l'épuisement des connexions.
- Utiliser RDS Proxy pour de nombreux clients de courte durée.

<!-- concept -->

Chaque connexion coûte de la mémoire, et les moteurs ont un maximum. Les applications sans pool, et surtout les fonctions serverless qui montent à des centaines de copies, peuvent l'épuiser en quelques secondes lors d'un pic.

RDS Proxy se place entre clients et base et partage un petit pool de connexions entre de nombreux clients. Il accélère aussi le basculement et s'intègre à IAM et Secrets Manager, ce qui en fait la correction par défaut des architectures riches en Lambda.

<!-- example -->

```text
800 Lambda invocations ─► RDS Proxy (pool: 80 connections) ─► RDS (max_connections 200)
without proxy:          800 direct connections ─► "too many connections"
```

#### Comment trouver les index inutilisés dans PostgreSQL sur RDS ?

Interroger `pg_stat_user_indexes` pour les index avec `idx_scan = 0` sur une longue période (hors contraintes), et les supprimer après vérification, car ils coûtent en performances d'écriture et en stockage.

#### Comment identifier les transactions longues dans PostgreSQL ?

Interroger `pg_stat_activity` pour les sessions avec un `xact_start` ancien, surtout en `idle in transaction` ; elles bloquent le vacuum et causent du bloat. Fixez `idle_in_transaction_session_timeout` pour protéger la base.

#### Quels journaux RDS peut-il publier dans CloudWatch Logs ?

Journaux d'erreurs, de requêtes lentes, généraux (MySQL), les journaux PostgreSQL (dont la sortie de `log_min_duration_statement` et de `pgaudit`), journaux d'audit, de mise à jour et de l'agent, selon le moteur et les réglages.

#### Comment alerter sur les problèmes RDS ?

Alarmes CloudWatch sur le CPU, le stockage libre, la mémoire libre, les connexions, le retard des réplicas, les latences de lecture et d'écriture et le solde de rafale ; règles EventBridge sur les événements RDS (basculement, stockage plein, maintenance) ; et détection d'anomalies dans Database Insights.

#### Comment faire monter une instance RDS en charge verticalement ?

Modifier la classe d'instance (par exemple de `db.r6g.large` à `db.r6g.2xlarge`), immédiatement ou dans la fenêtre de maintenance. Cela implique une brève interruption, raccourcie par le Multi-AZ (la standby est modifiée d'abord, puis basculement).

<!-- challenge -->

Passer `max_connections` de 500 à 5 000 a arrêté les erreurs, mais la base est devenue plus lente. Pourquoi ?

<!-- solution -->

Chaque connexion consomme mémoire et CPU d'ordonnancement : des milliers de connexions compriment le cache et ajoutent de la contention. Gardez une limite modérée et mutualisez les connexions (dans l'application ou avec RDS Proxy).

<!-- takeaways -->

- Les clients sans pool et serverless épuisent les connexions.
- RDS Proxy mutualise et partage les connexions.
- Augmenter `max_connections` n'est pas une correction.

<!-- unit: Optimiser le moteur -->

<!-- goals -->

- Régler les paramètres de PostgreSQL et MySQL sur RDS.
- Entretenir PostgreSQL : autovacuum, index et transactions.

<!-- concept -->

Les valeurs par défaut sont des suppositions prudentes, pas des réglages optimisés. Les paramètres mémoire décident de la part des données en cache ; ceux de journalisation, de ce que vous pouvez voir ; et sous PostgreSQL, l'autovacuum décide si les lignes mortes sont nettoyées avant que les tables gonflent.

Beaucoup de problèmes PostgreSQL viennent de ce qui freine ce nettoyage : transactions longues ou inactives, replication slots abandonnés et index inutilisés qui ralentissent chaque écriture. Les vérifier régulièrement fait partie de l'exploitation du moteur.

<!-- example -->

```sql
-- sessions holding back vacuum and locks
SELECT pid, state, now() - xact_start AS age, left(query, 60)
FROM pg_stat_activity
WHERE xact_start < now() - interval '15 minutes'
ORDER BY xact_start;
```

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

<!-- challenge -->

Une table PostgreSQL très mise à jour est passée de 5 Go à 60 Go alors que le nombre de lignes est stable. Que vérifiez-vous et changez-vous ?

<!-- solution -->

Du bloat par tuples morts : vérifiez `n_dead_tup` et l'activité de l'autovacuum, cherchez transactions longues ou slots inactifs qui bloquent le nettoyage, réglez l'autovacuum de cette table (scale factor plus bas) et reconstruisez-la une fois (par exemple `pg_repack`).

<!-- takeaways -->

- Réglez mémoire et journalisation dans des groupes personnalisés.
- L'autovacuum doit suivre le rythme des updates et deletes.
- Transactions longues et vieux slots bloquent le nettoyage.

### Montée en charge

<!-- unit: Monter en charge verticalement et horizontalement -->

<!-- goals -->

- Faire évoluer RDS verticalement et étendre les lectures horizontalement.
- Reconnaître quand les écritures exigent une autre conception.

<!-- concept -->

Les bases relationnelles étendent les lectures plus facilement que les écritures. Les lectures se répartissent sur réplicas et caches ; toutes les écritures passent par un primaire. Face à la pression d'écriture, la première étape est donc une instance plus grosse, puis des écritures moins coûteuses, et seulement ensuite des changements structurels comme découper la base par domaine ou passer à un moteur qui étend les écritures horizontalement.

Découper est autant un choix d'organisation que technique : des bases séparées conviennent à des responsables et charges séparés.

<!-- example -->

| Pression | Premier geste | Ensuite |
|---|---|---|
| CPU dû aux lectures | Réplicas en lecture, cache | Optimiser les requêtes |
| CPU dû aux écritures | Classe d'instance plus grande | Écritures par lots, moins d'index, découpage par domaine |
| Une table énorme | Partitionnement | Archiver les anciennes données |

#### Comment le cache aide-t-il une base RDS ?

ElastiCache (Redis ou Memcached) ou des caches applicatifs servent depuis la mémoire les lectures répétées (sessions, catalogues produits, résultats calculés), réduisant la charge et la latence de la base. La stratégie d'invalidation est la partie difficile.

#### Quand faut-il découper une base en plusieurs ?

Quand des domaines ou services ont des charges, des besoins de montée en charge ou des responsables indépendants, quand les pics d'une charge affectent les autres, ou selon le principe microservices d'une base par service.

#### Qu'est-ce qu'Amazon Aurora ?

Une base relationnelle compatible MySQL et PostgreSQL conçue pour le cloud, avec une couche de stockage distribuée et tolérante aux pannes partagée par l'écrivain et les réplicas. Elle offre un débit supérieur aux moteurs standard, un basculement plus rapide et un stockage qui croît automatiquement.

#### Comment fonctionne le stockage d'Aurora ?

Les données sont stockées dans un volume de cluster répliqué six fois sur trois zones de disponibilité, en segments de 10 Go. Les écritures exigent quatre copies sur six et les lectures trois sur six : le cluster tolère la perte d'une zone plus une autre copie. Le stockage croît automatiquement jusqu'à 128 Tio.

<!-- challenge -->

Les écritures d'une base ont doublé après une nouvelle fonctionnalité, et la plus grande classe d'instance approche de sa limite. Quelles options restent ?

<!-- solution -->

Réduire le coût des écritures (inserts par lots, suppression des index inutilisés, éviter l'amplification d'écriture), déplacer les données de la fonctionnalité vers leur propre base ou un magasin spécialisé comme DynamoDB, ou passer à un moteur à écritures horizontales (par exemple Aurora Limitless).

<!-- takeaways -->

- Les lectures s'étendent horizontalement ; les écritures passent par un primaire.
- Montez d'abord en taille, puis allégez les écritures.
- Découpez les bases selon domaines et responsables.

<!-- unit: Limites cachées et soulagements -->

<!-- goals -->

- Reconnaître les limites du CPU burstable et des plafonds d'I/O d'instance.
- Soulager la charge par cache, partitionnement et changements de stockage.

<!-- concept -->

Certains ralentissements viennent de limites peu visibles. Les instances burstables vont vite jusqu'à épuisement de leurs crédits CPU. Chaque classe d'instance plafonne l'I/O qu'elle peut pousser : un stockage avec plus d'IOPS que la classe n'en permet n'apporte rien.

D'autres soulagements ne touchent pas l'instance : les caches absorbent les lectures répétées, et partitionner les grosses tables permet aux requêtes et à la maintenance de travailler sur de plus petits morceaux.

<!-- example -->

```sql
-- PostgreSQL declarative partitioning by month
CREATE TABLE events (id bigint, created_at timestamptz NOT NULL, payload jsonb)
PARTITION BY RANGE (created_at);
CREATE TABLE events_2026_10 PARTITION OF events
  FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
```

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

<!-- challenge -->

Une `db.t3.medium` tourne bien pendant des semaines, puis devient très lente chaque jour dès 14:00. Le CPU affiche 20 %. Que se passe-t-il ?

<!-- solution -->

L'instance a épuisé ses crédits CPU et est bridée à sa base, environ 20 % pour cette classe. Passer à une classe non burstable (par exemple `db.m7g`) ou activer le mode unlimited si la charge soutenue est normale.

<!-- takeaways -->

- Les classes burstables sont bridées quand les crédits s'épuisent.
- Les classes d'instance plafonnent l'I/O, quel que soit le stockage.
- Caches et partitionnement soulagent sans instances plus grosses.

### Aurora

<!-- unit: Ce que coûte RDS -->

<!-- goals -->

- Identifier les facteurs de coût d'un déploiement RDS.
- Tenir compte du Multi-AZ, des sauvegardes et du transfert de données.

<!-- concept -->

Une facture RDS compte peu de lignes : heures d'instance, stockage et sa performance, sauvegardes au-delà de la part gratuite, transfert de données. Les choix de disponibilité multiplient la ligne de calcul : le Multi-AZ fait tourner une deuxième instance et chaque réplica en est une de plus.

Le transfert de données s'oublie facilement. La réplication Multi-AZ est gratuite, mais les applications qui parlent à une base dans une autre zone paient le trafic inter-zones.

<!-- example -->

```text
db.r7g.large single-AZ        ~ 1 × instance price
db.r7g.large Multi-AZ         ~ 2 × instance price
+ 2 read replicas             ~ 4 × instance price
+ gp3 storage, extra IOPS, backups beyond DB size, cross-AZ app traffic
```

#### Qu'est-ce qu'Aurora Backtrack ?

Une fonction d'Aurora MySQL qui ramène le cluster sur place à un instant antérieur dans une fenêtre configurée, sans restauration de sauvegarde, utile pour annuler rapidement une erreur.

#### Que sont Aurora Standard et Aurora I/O-Optimized ?

Deux configurations de stockage : Standard facture les requêtes d'E/S séparément (moins cher avec peu d'E/S), I/O-Optimized inclut les E/S dans un prix de stockage et d'instance plus élevé (moins cher quand les E/S dépassent environ un quart du coût de la base).

#### Qu'est-ce que l'intégration zero-ETL d'Aurora avec Redshift ?

Une intégration gérée qui réplique les données d'Aurora (et de certains moteurs RDS) dans Amazon Redshift en quasi temps réel sans construire de pipelines, pour faire de l'analytique dans Redshift sur des données opérationnelles fraîches.

#### Qu'est-ce que Babelfish for Aurora PostgreSQL ?

Une capacité qui permet à Aurora PostgreSQL de comprendre le T-SQL et le protocole TDS de SQL Server, pour que des applications écrites pour SQL Server fonctionnent avec moins de modifications de code.

<!-- challenge -->

La facture RDS montre des coûts élevés de stockage de sauvegarde pour une base de 500 Go. Causes probables ?

<!-- solution -->

Une rétention longue avec beaucoup de changements (journaux et snapshots quotidiens s'additionnent), de nombreux snapshots manuels jamais supprimés et des copies conservées dans d'autres régions. Revoir la rétention, supprimer les snapshots manuels obsolètes et confier les copies longues à AWS Backup avec règles de cycle de vie.

<!-- takeaways -->

- Calcul, stockage, sauvegardes et transfert font le coût.
- Le Multi-AZ double à peu près le calcul.
- Le trafic applicatif inter-zones est facturé.

<!-- unit: Économiser sur RDS -->

<!-- goals -->

- Bien dimensionner les instances et s'engager avec des Reserved Instances.
- Réduire le coût des bases de développement et inactives.

<!-- concept -->

Les économies viennent de trois gestes : la bonne taille, payer moins ce qui tourne en permanence, cesser de payer ce qui n'a pas besoin de tourner. Plusieurs semaines de métriques révèlent les instances surdimensionnées ; les Reserved Instances réduisent le prix des instances de production stables ; les classes Graviton coûtent moins pour le même travail.

Les bases de développement sont le gain facile : plus petites, single-AZ, arrêtées hors heures ouvrées, ou remplacées par une capacité serverless.

<!-- example -->

| Base | Changement | Effet |
|---|---|---|
| Prod, 24 h/24, stable | Reserved Instance 3 ans, Graviton | Forte remise |
| Prod, CPU à 10 % depuis des mois | Une taille en dessous | Moitié moins de calcul |
| Dev | Single-AZ, arrêt nuits et week-ends | ~70 % de moins |

#### Qu'est-ce que la Data API d'Aurora ?

Une API HTTP pour exécuter du SQL sur Aurora (Serverless v2 et provisionné) sans gérer de connexions ni de pilotes, pratique pour Lambda et les autres applications serverless.

#### Qu'est-ce qu'Aurora DSQL ?

Une base SQL distribuée et serverless compatible PostgreSQL, conçue pour des applications actif-actif multi-régions, qui monte en charge horizontalement en lecture et en écriture avec une cohérence forte. Elle diffère d'Aurora standard et a quelques limites fonctionnelles par rapport à PostgreSQL.

#### Quand choisir Aurora plutôt que RDS pour PostgreSQL ou MySQL ?

Quand il faut un débit plus élevé, un basculement plus rapide, de nombreux réplicas à faible retard, une réplication mondiale, du clonage rapide ou une montée en charge serverless. RDS standard peut être moins cher pour des charges petites ou régulières et prend parfois en charge plus tôt certaines fonctions ou versions du moteur.

#### Que sont les endpoints personnalisés d'Aurora ?

Des endpoints qui pointent vers un sous-ensemble choisi des instances d'un cluster, par exemple des réplicas plus gros pour les requêtes analytiques et de plus petits pour les lectures applicatives.

<!-- challenge -->

Dix bases de développement tournent en Multi-AZ 24 h/24 avec la même classe que la production. Estimez les principaux leviers.

<!-- solution -->

Les passer en single-AZ (environ la moitié), sur des classes plus petites ou burstables, et planifier un arrêt/démarrage limité aux heures ouvrées (environ 70 % de temps en moins). Ensemble, plus de 80 % d'économies sont réalistes.

<!-- takeaways -->

- Dimensionnez d'après des semaines de métriques.
- Réservez les instances stables ; préférez Graviton.
- Bases de dev : petites, single-AZ, planifiées.

<!-- stage: Moteurs et fonctions -->

### Moteurs et fonctions

<!-- unit: Architecture d'Aurora -->

<!-- goals -->

- Expliquer comment le stockage partagé d'Aurora change la disponibilité.
- Décrire clusters, niveaux de basculement et sauvegardes.

<!-- concept -->

Aurora sépare calcul et stockage. Les instances n'ont pas de disques propres ; elles partagent un volume de cluster qui garde six copies sur trois zones et se répare seul. Les réplicas lisent le même stockage : leur retard est de quelques millisecondes et ils peuvent prendre le relais sans copier de données.

Le stockage assurant la durabilité, le basculement est plus rapide qu'en Multi-AZ classique, les sauvegardes sont continues sans impact sur la performance, et les niveaux de basculement décident quel réplica est promu en premier.

<!-- example -->

```text
writer (AZ a)   reader tier-0 (AZ b)   reader tier-1 (AZ c)
      │                 │                     │
      └──────── shared cluster volume: 6 copies across 3 AZs ────────┘
```

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

<!-- challenge -->

Un cluster Aurora a un gros lecteur pour l'analytique et un petit. Après un basculement, le petit est devenu l'écrivain et la production a ralenti. Comment l'éviter ?

<!-- solution -->

Fixer les niveaux de basculement : donner le niveau 0 à un lecteur de la taille de l'écrivain pour qu'il soit promu en premier, et placer les lecteurs d'analytique ou petits dans des niveaux de moindre priorité.

<!-- takeaways -->

- Les instances Aurora partagent un volume répliqué six fois.
- Les réplicas ont quelques millisecondes de retard et basculent vite.
- Les niveaux de basculement décident qui devient écrivain.

<!-- unit: Endpoints et lectures à l'échelle -->

<!-- goals -->

- Router le trafic avec les endpoints de cluster, de lecture et personnalisés.
- Accélérer les lectures avec parallel query et Optimized Reads.

<!-- concept -->

Un cluster Aurora expose plusieurs endpoints. Celui du cluster suit l'écrivain ; celui de lecture répartit les nouvelles connexions entre réplicas ; les endpoints personnalisés ciblent des instances choisies, par exemple de gros lecteurs pour le reporting.

La répartition se fait par connexion via le DNS, pas par requête : des pools de longue durée peuvent rester collés à un réplica. Des fonctions comme parallel query et Optimized Reads poussent certaines charges au-delà de simples réplicas.

<!-- example -->

```bash
aws rds create-db-cluster-endpoint --db-cluster-identifier orders-aurora \
  --db-cluster-endpoint-identifier reporting --endpoint-type READER \
  --static-members orders-reader-xl-1 orders-reader-xl-2
```

#### Peut-on mélanger Aurora Serverless v2 et des instances provisionnées ?

Oui. Un cluster peut avoir un écrivain provisionné et des lecteurs Serverless v2 (ou l'inverse), ce qui est utile avec un trafic de lecture variable.

#### Quelles extensions PostgreSQL sont utiles sur RDS ?

`pg_stat_statements` (statistiques de requêtes), `PostGIS` (géospatial), `pgvector` (recherche vectorielle), `pg_partman` (gestion des partitions), `pg_cron` (jobs planifiés), `aws_s3` (import/export avec S3), `pgaudit`, `pg_repack` et `postgres_fdw`. Seules les extensions prises en charge peuvent être installées.

#### Comment charger des données depuis S3 dans RDS PostgreSQL ?

Avec l'extension `aws_s3` : `SELECT aws_s3.table_import_from_s3('table', 'col1,col2', '(format csv, header true)', aws_commons.create_s3_uri('bucket', 'fichier.csv', 'eu-west-1'));`, avec un rôle IAM associé à l'instance.

#### Qu'est-ce qu'un déploiement Blue/Green ?

Une fonction (MySQL, MariaDB, PostgreSQL, Aurora) qui crée une copie de préproduction (green) synchronisée avec la production (blue) par réplication logique, permet de la mettre à jour ou de la modifier, puis bascule en environ une minute avec des garde-fous, en conservant les mêmes endpoints.

<!-- challenge -->

Il y a trois réplicas, mais l'un reçoit presque tout le trafic de lecture. L'application utilise un pool de connexions ouvert au démarrage. Pourquoi ?

<!-- solution -->

L'endpoint de lecture répartit à la connexion via le DNS : les connexions du pool sont presque toutes tombées sur un réplica et y restent. Recyclez périodiquement les connexions, utilisez un wrapper de driver qui répartit entre lecteurs ou des endpoints personnalisés.

<!-- takeaways -->

- Endpoints de cluster, de lecture et personnalisés routent le trafic.
- La répartition des lectures se fait par connexion, pas par requête.
- Parallel query et Optimized Reads aident des charges précises.

<!-- unit: Options de capacité et de stockage -->

<!-- goals -->

- Choisir entre clusters provisionnés, Serverless v2 et mixtes.
- Choisir le stockage Standard ou I/O-Optimized, et connaître Limitless et DSQL.

<!-- concept -->

Aurora propose plusieurs façons de payer la capacité. Les instances provisionnées conviennent à une charge stable ; Serverless v2 ajuste la capacité par petits pas selon la demande, et les deux se mélangent dans un cluster. Le stockage a deux modes de facturation : payer chaque I/O, ou payer plus cher le stockage sans frais d'I/O, gagnant pour les charges intensives en I/O.

Pour étendre les écritures au-delà d'une instance, Limitless répartit les tables PostgreSQL en shards, et DSQL offre une base SQL distribuée et serverless sur plusieurs régions.

<!-- example -->

| Charge | Choix |
|---|---|
| OLTP stable, 24 h/24 | Provisionné |
| Charge en pics ou dev/test | Serverless v2 |
| Coût d'I/O > ~25 % de la facture | I/O-Optimized |
| Écritures au-delà d'une instance | Limitless Database |

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

<!-- challenge -->

La facture d'un cluster Aurora est à 60 % des frais d'I/O. Que changez-vous, et comment confirmer le gain ?

<!-- solution -->

Passer le cluster en Aurora I/O-Optimized, qui supprime les frais d'I/O contre un prix d'instance et de stockage plus élevé. Comparez les coûts d'I/O, d'instance et de stockage des derniers mois aux tarifs I/O-Optimized avant de changer ; c'est rentable quand l'I/O domine.

<!-- takeaways -->

- Provisionné pour le stable ; Serverless v2 pour le variable.
- I/O-Optimized gagne quand l'I/O domine la facture.
- Limitless et DSQL visent l'extension des écritures et le multi-région.

<!-- unit: Bases globales, clonage et Backtrack -->

<!-- goals -->

- Utiliser Aurora Global Database pour les lectures inter-régions et la reprise.
- Créer des clones rapides et revenir en arrière avec Backtrack.

<!-- concept -->

La couche de stockage d'Aurora rend bon marché ce qui coûte cher ailleurs. Global Database réplique au niveau du stockage vers d'autres régions avec environ une seconde de retard : une région distante peut servir des lectures et prendre le relais en cas de sinistre.

Le clonage crée un nouveau cluster qui partage les pages de la source jusqu'à leur modification : une copie complète apparaît en minutes et coûte peu. Backtrack, pour Aurora MySQL, ramène un cluster sur place à un instant antérieur.

<!-- example -->

```bash
aws rds restore-db-cluster-to-point-in-time --source-db-cluster-identifier orders-aurora \
  --db-cluster-identifier orders-clone-qa --restore-type copy-on-write --use-latest-restorable-time
```

#### Quelles options de licence existent pour Oracle et SQL Server sur RDS ?

License Included (licence incluse dans le prix horaire) ou Bring Your Own License pour Oracle ; SQL Server est généralement en License Included, avec le choix de l'édition (Express, Web, Standard, Enterprise).

#### Comment utiliser `pgvector` sur RDS PostgreSQL ?

Installer l'extension, créer des colonnes `vector` pour les embeddings et les indexer avec des index HNSW ou IVFFlat pour la recherche par similarité, ce qui permet la génération augmentée par récupération sans base vectorielle séparée.

#### À quoi sert la réplication logique sur RDS PostgreSQL ?

À répliquer des tables choisies vers une autre base PostgreSQL (mises à jour, migrations, découpage de bases ou alimentation de l'analytique), au CDC vers des systèmes externes et aux déploiements Blue/Green.

<!-- challenge -->

La QA a besoin chaque matin d'une copie complète d'une base de production de 3 To, mais les restaurations prennent des heures. Qu'utilisez-vous ?

<!-- solution -->

Le clonage rapide d'Aurora (copy-on-write) : le clone est prêt en minutes et ne stocke que les pages modifiées. Supprimez-le et recréez-le chaque matin, en masquant les données sensibles si la QA ne doit pas les voir.

<!-- takeaways -->

- Global Database réplique entre régions avec ~1 s de retard.
- Les clones partagent le stockage jusqu'aux modifications.
- Backtrack ramène Aurora MySQL en arrière sur place.

<!-- unit: Intégrations et choix d'Aurora -->

<!-- goals -->

- Utiliser zero-ETL, Babelfish et la Data API.
- Décider quand Aurora vaut mieux que RDS.

<!-- concept -->

Aurora ajoute des intégrations qui suppriment des pans entiers de plomberie. Zero-ETL réplique les données vers Redshift en continu sans pipeline. Babelfish permet aux applications SQL Server de parler à PostgreSQL. La Data API exécute du SQL en HTTP sans gérer de connexions.

Préférer Aurora à RDS standard dépend du besoin : basculement plus rapide, nombreux réplicas à faible retard, réplication globale, clonage ou ces intégrations. Pour de petites bases stables, RDS standard coûte souvent moins.

<!-- example -->

| Besoin | Fonction Aurora |
|---|---|
| Analytique dans Redshift sans ETL | Intégration zero-ETL |
| Migrer progressivement une appli SQL Server vers PostgreSQL | Babelfish |
| Interroger depuis Lambda sans pool de connexions | Data API |

#### Quels sont les atouts de MySQL 8.0+ sur RDS pour le travail sur les données ?

Fonctions de fenêtre, CTE (y compris récursives), fonctions JSON, index invisibles, `ADD COLUMN` instantané pour beaucoup de changements et de meilleures statistiques d'optimiseur, qui facilitent les requêtes analytiques et les changements de schéma.

#### Comment mener des migrations de schéma sûres sur de grosses tables ?

Utiliser des opérations compatibles avec le travail en ligne (DDL instantané de MySQL 8, `CREATE INDEX CONCURRENTLY` de PostgreSQL), des outils comme `gh-ost` ou `pt-online-schema-change` pour MySQL, des déploiements Blue/Green, et mesurer la durée de la migration sur un clone.

#### Qu'est-ce qui fait les coûts de RDS ?

Les heures d'instance (par classe ; le Multi-AZ double le calcul), le stockage (par type et taille, plus les IOPS provisionnées), le stockage de sauvegarde au-delà du volume gratuit, le transfert de données sortant et entre zones ou régions, les frais d'Extended Support, et des fonctions comme RDS Proxy et le mode avancé de Database Insights.

#### Comment réduire les coûts de RDS ?

Dimensionner les instances d'après les métriques, utiliser les classes Graviton, acheter des Reserved Instances pour les charges régulières, préférer gp3 à un io1 surprovisionné, arrêter la nuit les instances hors production, nettoyer les anciens snapshots, utiliser Aurora Serverless v2 ou I/O-Optimized quand ils conviennent, et décharger les lectures vers des caches.

<!-- challenge -->

Une équipe exploite une base PostgreSQL de 50 Go à faible trafic et demande à passer sur Aurora « parce que c'est mieux ». Que demandez-vous avant d'accepter ?

<!-- solution -->

Quel problème cela résout : temps de basculement, réplicas, lectures globales, clonage ou intégrations. Si rien de cela ne compte, RDS for PostgreSQL standard est sans doute moins cher et plus simple ; sinon, comparez les coûts en incluant l'I/O.

<!-- takeaways -->

- Zero-ETL alimente Redshift sans pipeline.
- Babelfish et la Data API facilitent l'intégration.
- Choisissez Aurora pour des besoins précis, pas par défaut.

### Coûts

<!-- unit: Extensions PostgreSQL -->

<!-- goals -->

- Utiliser des extensions PostgreSQL courantes sur RDS.
- Charger depuis S3, planifier des jobs et répliquer logiquement des tables.

<!-- concept -->

Les extensions font de PostgreSQL une plateforme : statistiques de requêtes, données géospatiales, recherche vectorielle, jobs planifiés et import direct depuis S3. RDS prend en charge une liste choisie, qui couvre l'essentiel des besoins sans accès système.

La réplication logique est l'autre brique : elle transmet les changements de tables choisies vers une autre base, ce sur quoi reposent mises à niveau, migrations et CDC.

<!-- example -->

```sql
CREATE EXTENSION IF NOT EXISTS aws_s3 CASCADE;
SELECT aws_s3.table_import_from_s3('staging.orders', '', '(format csv, header true)',
       aws_commons.create_s3_uri('landing-bucket', 'orders/2026-10-17.csv', 'eu-west-1'));
CREATE EXTENSION IF NOT EXISTS pg_cron;
SELECT cron.schedule('refresh-mv', '0 * * * *', 'REFRESH MATERIALIZED VIEW CONCURRENTLY marts.sales_hourly');
```

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

<!-- challenge -->

Une application a besoin d'une recherche par similarité sur 2 millions d'embeddings produits et utilise déjà RDS PostgreSQL. Faut-il une base vectorielle séparée ?

<!-- solution -->

Sans doute pas à cette taille : installez `pgvector`, stockez les embeddings dans une colonne `vector` et créez un index HNSW. N'envisagez un magasin vectoriel séparé que si les exigences de latence ou d'échelle dépassent PostgreSQL.

<!-- takeaways -->

- Les extensions ajoutent statistiques, géospatial, vecteurs et planification.
- `aws_s3` charge les fichiers directement depuis S3.
- La réplication logique transmet des tables choisies.

<!-- unit: Mises à niveau et changements sûrs -->

<!-- goals -->

- Planifier les mises à niveau mineures et majeures du moteur.
- Utiliser les déploiements Blue/Green et les changements de schéma en ligne.

<!-- concept -->

Les moteurs vieillissent : les versions arrivent en fin de support, et y rester coûte des frais d'Extended Support ou expose à des mises à niveau forcées. Les versions mineures peuvent s'appliquer automatiquement ; les majeures demandent des tests car extensions, paramètres et plans de requête changent.

Les déploiements Blue/Green sécurisent mises à niveau et gros changements : une copie synchronisée est modifiée et testée pendant que la production tourne, et la bascule prend environ une minute. Les changements de schéma sur de grosses tables demandent des opérations en ligne pour la même raison.

<!-- example -->

```bash
aws rds create-blue-green-deployment --blue-green-deployment-name orders-pg16 \
  --source arn:aws:rds:eu-west-1:123456789012:db:orders-prod \
  --target-engine-version 16.4 --target-db-parameter-group-name pg16-orders
# test green, then:
aws rds switchover-blue-green-deployment --blue-green-deployment-identifier bgd-abc123
```

#### Comment économiser sur les bases de développement ?

Utiliser des instances petites ou extensibles, en mono-AZ, les arrêter hors des heures de travail, utiliser Aurora Serverless v2 avec un minimum bas, restaurer depuis des snapshots partagés plutôt que de garder de nombreuses copies, et supprimer les environnements inutilisés.

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

<!-- challenge -->

Ajouter un index sur une table PostgreSQL de 400 Go a bloqué les écritures 20 minutes en production. Comment aurait-il fallu procéder ?

<!-- solution -->

Avec `CREATE INDEX CONCURRENTLY`, qui construit sans bloquer les écritures (plus lent, et impossible dans une transaction). Tester d'abord la durée sur un clone et l'exécuter à faible trafic.

<!-- takeaways -->

- Planifiez les majeures ; testez sur une copie restaurée.
- Blue/Green bascule en environ une minute.
- Utilisez du DDL en ligne sur les grosses tables.

<!-- unit: Moteurs commerciaux et MySQL -->

<!-- goals -->

- Connaître les limites et licences de SQL Server et Oracle sur RDS.
- Utiliser les fonctions modernes de MySQL pour le travail sur les données.

<!-- concept -->

Les moteurs commerciaux sur RDS ajoutent deux considérations. Certains privilèges et fonctions sont restreints car AWS gère le serveur : certaines tâches d'administration passent par des procédures propres à RDS. La licence peut être incluse dans le prix horaire ou apportée depuis des accords existants, ce qui change fortement le coût.

MySQL 8 a comblé beaucoup de lacunes du SQL analytique, avec fonctions de fenêtre, CTE et JSON, ce qui compte quand les équipes data l'interrogent directement.

<!-- example -->

```sql
-- MySQL 8: latest order per customer with a window function
SELECT * FROM (
  SELECT o.*, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC) AS rn
  FROM orders o
) t WHERE rn = 1;
```

#### Comment extraire de grosses tables de RDS sans pénaliser la production ?

Lire depuis un réplica ou un clone/une restauration récente, exporter des snapshots vers S3 en Parquet, extraire de façon incrémentale par une colonne updated-at ou par CDC plutôt que tout extraire, paralléliser par plages de clés dans certaines limites, et planifier hors des heures de pointe.

#### Qu'est-ce que l'export de snapshot vers S3 ?

Une fonction RDS qui exporte les données d'un snapshot vers S3 au format Parquet, partitionnées par table, sans impact sur la base en service, prêtes à être cataloguées par Glue et interrogées par Athena.

#### Comment les jobs Glue lisent-ils RDS ?

Via une connexion JDBC Glue dans le VPC de la base (avec accès sous-réseau et groupe de sécurité), en lisant les tables en parallèle grâce aux options de partitionnement, avec les identifiants dans Secrets Manager ; bookmarks ou colonne de watermark assurent les chargements incrémentaux.

<!-- challenge -->

Une équipe qui migre SQL Server vers RDS compte sur `sysadmin` pour ses scripts de maintenance. Que lui dites-vous ?

<!-- solution -->

RDS n'accorde pas `sysadmin`. Réécrivez les scripts avec les privilèges de l'utilisateur maître et les procédures RDS (par exemple `rds_backup_database` pour les sauvegardes natives), ou envisagez RDS Custom si le contrôle système est indispensable.

<!-- takeaways -->

- Les moteurs commerciaux ont des privilèges restreints sur RDS.
- License Included ou BYOL change le coût.
- MySQL 8 apporte fonctions de fenêtre, CTE et JSON.

<!-- stage: Ingénierie des données sur RDS -->

### Migration et data engineering

<!-- unit: Clés et normalisation -->

<!-- goals -->

- Choisir les clés primaires des tables OLTP.
- Expliquer pourquoi la normalisation compte pour les données transactionnelles.

<!-- concept -->

Les bases transactionnelles sont optimisées pour de nombreux petits changements corrects. La normalisation y contribue en stockant chaque fait une seule fois : une mise à jour touche une ligne. Les clés primaires donnent à chaque ligne une identité stable, dont dépendent jointures, réplication et outils de CDC.

Concevoir les clés est un arbitrage : les clés de substitution sont stables et compactes, les naturelles ont du sens, et les entiers s'indexent mieux que des UUID aléatoires, même si les UUID se génèrent plus facilement n'importe où.

<!-- example -->

```sql
CREATE TABLE customers (
  customer_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,   -- surrogate
  email       text NOT NULL UNIQUE,                               -- natural key, enforced
  created_at  timestamptz NOT NULL DEFAULT now(),
  updated_at  timestamptz NOT NULL DEFAULT now()
);
```

#### Comment charger efficacement des données dans RDS ?

Avec le chargement en masse (`COPY` pour PostgreSQL, `LOAD DATA` pour MySQL, l'extension `aws_s3`), des insertions par lots, en désactivant ou différant la création des index secondaires lors des chargements initiaux, en augmentant temporairement `maintenance_work_mem`, et en évitant les insertions ligne à ligne à travers le réseau.

#### Faut-il lancer de l'analytique directement sur l'instance RDS de production ?

En général non. Les requêtes analytiques concurrencent le trafic OLTP pour le CPU, la mémoire et les E/S. Utilisez un réplica pour le reporting léger et, pour une analytique plus lourde, déplacez les données vers un entrepôt ou un lakehouse via CDC, exports ou zero-ETL.

#### Quelle est la différence entre OLTP et OLAP, et où se situe RDS ?

L'OLTP traite de nombreuses petites transactions (insertions, mises à jour, recherches ponctuelles) avec une cohérence forte ; l'OLAP traite de grosses lectures et agrégations sur l'historique. RDS est fait pour l'OLTP ; l'OLAP relève de Redshift, Snowflake, Databricks ou Athena sur un data lake.

#### Qu'est-ce que DMS Schema Conversion ?

Une fonction gérée de DMS (qui succède dans bien des cas au Schema Conversion Tool de bureau) qui évalue et convertit schémas et code entre moteurs, en signalant les éléments nécessitant un travail manuel.

<!-- challenge -->

Une table historique n'a pas de clé primaire, et le CDC de DMS ne parvient pas à appliquer les updates sur la cible. Que faites-vous ?

<!-- solution -->

Ajouter une clé primaire (une colonne unique existante ou une nouvelle colonne identity) et relancer la tâche. Sans clé, les outils de CDC ne peuvent pas identifier la ligne visée par un update ou un delete.

<!-- takeaways -->

- Chaque table a besoin d'une clé primaire.
- Clés de substitution stables ; imposez les naturelles par contraintes uniques.
- La normalisation garde les updates OLTP petits et cohérents.

<!-- unit: Index et concurrence -->

<!-- goals -->

- Concevoir des index, y compris composites, et en peser le coût.
- Comprendre les niveaux d'isolation et éviter les deadlocks.

<!-- concept -->

Les index échangent coût d'écriture et stockage contre des lectures plus rapides. Un index composite aide les requêtes qui filtrent sur ses premières colonnes : l'ordre des colonnes suit la façon dont filtrent les requêtes. Trop d'index ralentissent chaque insert et update.

La concurrence ajoute une couche : les niveaux d'isolation décident de ce qu'une transaction voit des changements des autres, et des ordres de verrouillage contradictoires créent des deadlocks. Des transactions courtes et un ordre d'accès cohérent évitent la plupart des problèmes.

<!-- example -->

```sql
CREATE INDEX idx_orders_customer_created ON orders (customer_id, created_at);
-- uses the index:      WHERE customer_id = 42 AND created_at >= '2026-10-01'
-- uses it partially:   WHERE customer_id = 42
-- cannot use it well:  WHERE created_at >= '2026-10-01'
```

#### Comment DMS gère-t-il les grosses tables lors du chargement complet ?

Par un chargement parallèle par partitions ou plages d'une colonne, des réglages pour les objets volumineux (LOB) et des mappages de tables pour sélectionner et transformer ; les très grosses migrations peuvent combiner un export natif en masse et le CDC DMS à partir d'une position connue.

#### Comment valider une migration ?

Validation des données DMS (comparaison ligne à ligne), comptages de lignes et sommes de contrôle par table, comparaison d'agrégats (sommes, min/max par plages de clés), tests applicatifs sur la cible et une période de fonctionnement en parallèle.

#### Quels sont les pièges courants du CDC depuis des bases relationnelles ?

Des tables sans clé primaire (impossible d'appliquer les mises à jour), une rétention de journaux insuffisante, de grosses transactions qui créent du retard, des changements de schéma non propagés, des écarts de types (horodatages, décimaux) et des suppressions non traitées en aval.

#### Comment envoyer les changements RDS vers Kafka ?

Avec Debezium sur Kafka Connect (ou Amazon MSK Connect) lisant le binlog ou la réplication logique, qui produit un topic par table avec les événements de changement, ou avec DMS ciblant Kinesis ou MSK.

<!-- challenge -->

Deux jobs mettent à jour la même table de comptes et tombent parfois en deadlock. L'un procède par ordre d'identifiant, l'autre par ordre de nom. Que changez-vous ?

<!-- solution -->

Faire mettre à jour les lignes dans le même ordre par les deux (par exemple par clé primaire), garder les transactions courtes et ajouter une logique de relance pour le rare deadlock restant.

<!-- takeaways -->

- Les index accélèrent les lectures et ralentissent les écritures.
- L'ordre d'un index composite suit les filtres des requêtes.
- Un ordre de verrouillage cohérent et des transactions courtes évitent les deadlocks.

<!-- unit: Des tables adaptées aux pipelines -->

<!-- goals -->

- Concevoir des tables qui permettent extraction incrémentale et audit.
- Rendre les suppressions visibles pour l'aval.

<!-- concept -->

Les tables sont lues par d'autres que l'application. Les pipelines de données doivent savoir ce qui a changé depuis la dernière fois, et l'audit quand. Des colonnes d'horodatage tenues à jour à chaque changement rendent l'extraction incrémentale possible.

Les suppressions sont le cas difficile : une ligne supprimée disparaît, et un pipeline qui lit les changements par horodatage ne la voit jamais. Les soft deletes, ou le CDC, rendent les suppressions visibles.

<!-- example -->

```sql
ALTER TABLE orders ADD COLUMN deleted_at timestamptz;
-- trigger keeps updated_at current on every UPDATE
CREATE TRIGGER orders_touch BEFORE UPDATE ON orders
FOR EACH ROW EXECUTE FUNCTION set_updated_at();
```

#### Comment amener les données RDS dans un data lake ?

Des chargements complets par export de snapshot vers S3 ou chargement complet DMS, puis les changements incrémentaux par CDC DMS vers S3 (Parquet avec des colonnes d'opération) ou zero-ETL ; on applique les changements à des tables Iceberg/Delta avec `MERGE` et on catalogue le tout dans Glue.

#### Qu'est-ce qu'une extraction incrémentale par watermark, et quels en sont les risques ?

Sélectionner les lignes dont `updated_at` dépasse la dernière valeur extraite. Elle manque les suppressions, les lignes modifiées sans mise à jour de l'horodatage et les lignes validées tardivement avec un horodatage antérieur ; utilisez une fenêtre de recouvrement et des rapprochements réguliers, ou le CDC.

<!-- challenge -->

Un pipeline incrémental s'appuie sur `updated_at`, mais l'entrepôt affiche encore des commandes supprimées dans l'application. Pourquoi, et quelles sont deux corrections ?

<!-- solution -->

Les hard deletes ne laissent aucune ligne à extraire. Soit utiliser des soft deletes (`deleted_at`) pour que les suppressions soient des updates, soit capturer les changements par CDC (DMS ou Debezium) pour recevoir des événements de suppression.

<!-- takeaways -->

- `created_at` et `updated_at` permettent les chargements incrémentaux.
- Les hard deletes sont invisibles à l'extraction par horodatage.
- Soft deletes ou CDC propagent les suppressions.

### SQL et conception de bases sur RDS

<!-- unit: Migrer vers RDS -->

<!-- goals -->

- Choisir une méthode de migration pour des moteurs identiques ou différents.
- Utiliser DMS et Schema Conversion, et valider le résultat.

<!-- concept -->

La façon de migrer dépend de deux questions : le moteur est-il le même, et quelle interruption est acceptable ? Même moteur et fenêtre de maintenance permettent dump et restore natifs. Une interruption minimale exige une réplication continue : un chargement complet suivi d'une capture des changements jusqu'à la bascule.

Changer de moteur ajoute la conversion du schéma et du code, que les outils n'automatisent qu'en partie. Toute migration se termine par une validation, car « ça a tourné » ne veut pas dire « les données concordent ».

<!-- example -->

```text
1. Schema Conversion: Oracle schema → PostgreSQL (review stored procedures by hand)
2. DMS full load (parallel by table partitions) + CDC
3. DMS data validation, row counts, checksums per table
4. Cutover: stop writes, wait for CDC lag 0, switch connection strings
```

#### Comment éviter de verrouiller les tables de production lors d'une extraction ?

Utiliser des snapshots ou des réplicas, lire avec un isolement par snapshot cohérent sans verrou (MVCC de PostgreSQL, lectures cohérentes InnoDB), éviter `SELECT … FOR UPDATE` et les transactions longues, et paginer par clé.

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

<!-- challenge -->

La validation montre de petites différences numériques entre Oracle et PostgreSQL sur quelques colonnes. Cause probable ?

<!-- solution -->

Le mappage des types : un `NUMBER` Oracle sans précision a été mappé vers un type flottant, ou des fonctions converties arrondissent différemment. Mappez ces colonnes en `numeric` avec la bonne précision et rechargez-les.

<!-- takeaways -->

- Même moteur : outils natifs ; interruption minimale : réplication.
- Changer de moteur exige de convertir schéma et code.
- Validez toujours les données après la migration.

<!-- unit: Capture des changements -->

<!-- goals -->

- Activer le CDC sur RDS MySQL et PostgreSQL.
- Éviter les pièges courants du CDC, dont les replication slots.

<!-- concept -->

Le CDC lit le journal de changements de la base, qui enregistre chaque insert, update et delete sans interroger les tables. Chaque moteur l'expose à sa façon : MySQL via le binlog, PostgreSQL via des replication slots logiques. Les deux demandent configuration et rétention suffisante du journal.

Le risque est la dépendance créée. Si un consommateur s'arrête, PostgreSQL garde le WAL de son slot jusqu'à remplir le disque, et clés manquantes ou transactions énormes cassent les pipelines. Le CDC se surveille comme tout système de production.

<!-- example -->

```text
MySQL:      binlog_format = ROW, binlog_row_image = FULL,
            CALL mysql.rds_set_configuration('binlog retention hours', 24);
PostgreSQL: rds.logical_replication = 1, then a slot per consumer
            alert on: pg_replication_slots.active = false, retained WAL size
```

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

<!-- challenge -->

Un connecteur Debezium est resté arrêté une semaine pour maintenance, et le disque PostgreSQL s'est rempli. Que s'est-il passé, et comment l'éviter ?

<!-- solution -->

Le replication slot du connecteur a continué à retenir du WAL pendant son inactivité. Alertez sur les slots inactifs et la taille du WAL retenu, supprimez les slots inutiles et, sur les versions récentes de PostgreSQL, fixez `max_slot_wal_keep_size` comme limite de sécurité.

<!-- takeaways -->

- Le CDC lit le binlog ou le WAL, pas les tables.
- Les slots PostgreSQL inactifs retiennent le WAL jusqu'à saturation.
- Clés, rétention et surveillance fiabilisent le CDC.

<!-- unit: Extraire pour l'analytique -->

<!-- goals -->

- Garder l'analytique hors du primaire de production.
- Extraire sans verrous, par snapshots, réplicas ou exports.

<!-- concept -->

Les bases OLTP servent les clients ; l'analytique ne doit pas leur faire concurrence. L'extraction la plus sûre lit ailleurs que sur le primaire : un réplica, un clone ou un snapshot exporté vers S3 en Parquet. Quand il faut lire le primaire, des lectures sur snapshot cohérent évitent de bloquer les écrivains.

L'extraction incrémentale par horodatage est simple mais a des trous : elle manque les suppressions et les lignes dont l'horodatage n'est pas mis à jour, et des commits tardifs peuvent passer derrière le watermark.

<!-- example -->

```bash
aws rds start-export-task --export-task-identifier orders-2026-10-17 \
  --source-arn arn:aws:rds:eu-west-1:123456789012:snapshot:rds:orders-prod-2026-10-17-03-10 \
  --s3-bucket-name lake-raw --s3-prefix rds/orders/ \
  --iam-role-arn arn:aws:iam::123456789012:role/rds-export --kms-key-id alias/lake
```

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

<!-- challenge -->

Un job d'extraction sélectionne `WHERE updated_at > last_watermark` et perd parfois des lignes. Citez deux causes et une approche plus robuste.

<!-- solution -->

Des transactions validées après la prise du watermark mais portant un `updated_at` antérieur, et des updates qui ne touchent pas `updated_at` (ou des hard deletes). Utiliser une fenêtre de recouvrement avec déduplication, ou passer au CDC.

<!-- takeaways -->

- Extrayez depuis réplicas, clones ou exports de snapshot.
- L'export de snapshot écrit du Parquet dans S3 sans charger la base.
- Les watermarks manquent suppressions et commits tardifs.

<!-- unit: Déplacer les données vers et depuis le lake -->

<!-- goals -->

- Lire RDS depuis Glue et charger efficacement des données dans RDS.
- Alimenter un data lake depuis RDS par chargements complets et incrémentaux.

<!-- concept -->

Les données circulent dans les deux sens entre RDS et le lake. Depuis RDS, un chargement complet amorce le lake et le CDC le tient à jour, Glue ou Spark appliquant les changements aux tables du lake. Vers RDS, le chargement en masse bat de plusieurs ordres de grandeur les inserts ligne à ligne.

Les jobs Glue atteignent RDS via des connections dans le VPC, et les lectures parallèles comptent pour les grosses tables.

<!-- example -->

```sql
-- PostgreSQL bulk load: far faster than INSERT per row
COPY staging.products (sku, name, price) FROM STDIN WITH (FORMAT csv, HEADER true);
-- then upsert into the final table
INSERT INTO products SELECT * FROM staging.products
ON CONFLICT (sku) DO UPDATE SET name = EXCLUDED.name, price = EXCLUDED.price;
```

#### Comment expliquer RDS à un interlocuteur non technique ?

C'est AWS qui exploite nos bases de données pour nous : il les tient à jour, sauvegardées et disponibles même si un serveur tombe, pour que l'équipe se concentre sur les données et l'application plutôt que sur la maintenance des machines.

#### Une API fondée sur Lambda sature la base de connexions lors des pics de trafic. Quelle est votre correction ?

Placer RDS Proxy entre Lambda et la base avec authentification IAM, fixer une concurrence réservée sur la fonction pour plafonner le parallélisme, réutiliser les connexions entre invocations, et envisager de mettre en cache les lectures les plus fréquentes.

#### Le retard d'un réplica de reporting atteint des heures pendant les batchs nocturnes. Que faites-vous ?

Je trouve les écritures lourdes sur la primaire (jobs batch, grosses transactions) et je les découpe en transactions plus petites, j'augmente la classe d'instance et les IOPS du réplica, j'évite sur le réplica les requêtes longues qui entrent en conflit avec le rejeu (`max_standby_streaming_delay` pour PostgreSQL), et j'envisage une copie analytique séparée.

<!-- challenge -->

Un job nocturne insère 5 millions de lignes dans RDS une par une et dure 6 heures. Que changez-vous ?

<!-- solution -->

Charger en masse : écrire un fichier et utiliser `COPY` (ou `aws_s3.table_import_from_s3` / `LOAD DATA`) vers une table de staging, puis un seul upsert ensembliste. Retirer ou différer les index non essentiels pendant le chargement si besoin.

<!-- takeaways -->

- Chargement complet plus CDC tiennent le lake à jour.
- Glue lit RDS via des connections VPC.
- Le chargement en masse bat les inserts ligne à ligne.

<!-- stage: Tout assembler -->

### Mises en situation

<!-- unit: Concevoir pour la disponibilité et la reprise -->

<!-- goals -->

- Concevoir une base de production pour la disponibilité, la sécurité et la reprise.
- Ajouter un plan de reprise après sinistre inter-régions.

<!-- concept -->

Les questions de conception testent votre capacité à combiner les pièces. Une bonne réponse couvre placement (sous-réseaux privés sur plusieurs zones), disponibilité (Multi-AZ), protection (sauvegardes avec restaurations testées, chiffrement, deletion protection), accès (utilisateurs au moindre privilège, secrets), observabilité (métriques, journaux, alarmes) et croissance. Elle sépare ensuite haute disponibilité et reprise après sinistre, avec un RTO et un RPO pour chacune.

<!-- example -->

| Couche | Choix |
|---|---|
| Disponibilité | Multi-AZ DB cluster (ou Aurora) |
| Protection | PITR de 14 jours, copies AWS Backup dans un autre compte et une autre région |
| Accès | Sous-réseaux privés, SG depuis le SG de l'appli, Secrets Manager, RDS Proxy |
| Observabilité | Database Insights, alarmes, notifications d'événements |
| Reprise | Réplica inter-régions (ou Aurora Global Database), runbook |

#### Votre équipe doit passer de PostgreSQL 13 à 16 avec une interruption minimale. Comment le planifier ?

Vérifier la compatibilité des extensions et des paramètres, tester la mise à jour sur un snapshot restauré avec les tests applicatifs, puis utiliser un déploiement Blue/Green : créer l'environnement green, le mettre à jour, le laisser se synchroniser, valider et basculer dans une courte fenêtre, en gardant le blue comme retour arrière jusqu'à être confiant.

#### Une revue de sécurité découvre une instance RDS accessible publiquement. Que changez-vous ?

Désactiver l'accès public, la déplacer dans des sous-réseaux privés, restreindre les groupes de sécurité aux sources applicatives, imposer TLS, faire tourner les identifiants, examiner les journaux à la recherche d'accès suspects, et ajouter des garde-fous (règle Config, SCP) pour éviter la récidive.

<!-- challenge -->

Le métier fixe un RTO d'1 heure et un RPO de 5 minutes pour un sinistre régional. Un réplica en lecture inter-régions suffit-il, et que faut-il d'autre ?

<!-- solution -->

En général oui : le retard du réplica est de quelques secondes et la promotion prend quelques minutes. Il faut aussi un runbook testé, une infrastructure prête dans la région de reprise (appli, secrets, basculement DNS) et des exercices réguliers.

<!-- takeaways -->

- Combinez placement, disponibilité, protection, accès et observabilité.
- Donnez séparément RTO et RPO pour HA et reprise.
- Une reprise ne compte que si elle est testée.

<!-- unit: Des données de production fraîches pour l'analytique -->

<!-- goals -->

- Fournir aux analystes des copies fraîches de la production en sécurité.
- Arbitrer fraîcheur, coût, isolation et confidentialité.

<!-- concept -->

Les analystes veulent les données de production, et la production veut qu'on la laisse tranquille. La question de conception : comment leur donner une copie récente, isolée des clients, abordable et sûre. Les options vont des réplicas (frais, mais qui chargent la réplication du primaire) aux clones ou restaurations quotidiens (isolés, vieux d'un jour) jusqu'aux exports vers le lake (peu coûteux, interrogeables par d'autres moteurs). La confidentialité décide si le masquage fait partie de la copie.

<!-- example -->

| Option | Fraîcheur | Isolation | Remarques |
|---|---|---|---|
| Réplica en lecture | Secondes | Partage la réplication | Bien pour des tableaux de bord en direct |
| Clone Aurora quotidien | Quotidienne | Totale | Rapide à créer, on paie les modifications |
| Export de snapshot vers S3 | Quotidienne | Totale | Parquet pour Athena ou Spark |

#### Comment mettre en place un plan de reprise après sinistre inter-régions pour une base RDS MySQL ?

Créer un réplica en lecture inter-régions (ou Aurora Global Database pour Aurora), répliquer les sauvegardes automatiques ou copier les snapshots vers la région de secours, scripter la promotion et les changements DNS, garder l'infrastructure applicative prête dans la région de secours, et tester régulièrement le basculement au regard du RPO et du RTO.

<!-- challenge -->

La copie contient e-mails et téléphones de clients que les analystes ne doivent pas voir. À quel endroit de votre conception les retirez-vous ?

<!-- solution -->

Les masquer pendant la construction de la copie : une étape de masquage sur le clone avant d'ouvrir l'accès, ou exclure et hacher ces colonnes à l'export vers le lake (avec des permissions de colonne Lake Formation en seconde couche).

<!-- takeaways -->

- Adaptez fraîcheur et isolation au besoin analytique.
- Clones et exports isolent l'analytique de la production.
- Masquez les données personnelles avant tout accès.
