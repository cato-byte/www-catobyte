## Fiche d'étude AWS Certified Cloud Practitioner

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude AWS Certified Cloud Practitioner : environ 200 questions](../../images/aws_practicioner_guide_title_img.png)

Environ 200 questions avec des réponses courtes, que j'ai utilisées pour préparer l'examen AWS Certified Cloud Practitioner (CLF-C02), obtenu en octobre 2026. Elles suivent les quatre domaines de l'examen : concepts du cloud, sécurité et conformité, technologies et services cloud, et facturation, tarification et support. Ouvrez une question pour voir sa réponse, ou utilisez le filtre pour chercher dans toute la fiche. Les services et les prix évoluent : vérifiez la documentation AWS avant de vous fier à un chiffre.

<!-- QA -->

### Concepts du cloud

#### Qu'est-ce que le cloud computing ?

La fourniture à la demande de ressources informatiques (calcul, stockage, bases de données, réseau, logiciels) via internet, avec une facturation à l'usage. Au lieu d'acheter et d'exploiter des centres de données, on loue de la capacité à un fournisseur et on la libère quand on n'en a plus besoin.

#### Quels sont les six avantages du cloud computing selon AWS ?

1. Remplacer des dépenses fixes (investissement) par des dépenses variables.
2. Profiter d'énormes économies d'échelle.
3. Ne plus deviner la capacité nécessaire.
4. Gagner en rapidité et en agilité.
5. Ne plus dépenser d'argent pour exploiter et entretenir des centres de données.
6. Se déployer dans le monde entier en quelques minutes.

#### Quels modèles de déploiement du cloud AWS prend-il en charge ?

- **Cloud (cloud natif) :** tout tourne dans le cloud public.
- **Sur site (cloud privé) :** des ressources dans votre propre centre de données, souvent avec de la virtualisation et des outils de gestion. AWS Outposts apporte l'infrastructure AWS sur site.
- **Hybride :** des ressources cloud reliées à une infrastructure sur site, par exemple pendant une migration ou pour des données qui doivent rester sur place.

#### Que signifient IaaS, PaaS et SaaS ? Donnez des exemples AWS.

- **IaaS (infrastructure en tant que service) :** vous obtenez des machines virtuelles, du stockage et des réseaux, et gérez le système d'exploitation et tout ce qui est au-dessus. Exemple : Amazon EC2.
- **PaaS (plateforme en tant que service) :** le fournisseur gère l'infrastructure et la plateforme, vous déployez du code. Exemple : AWS Elastic Beanstalk.
- **SaaS (logiciel en tant que service) :** une application complète utilisée via internet. Exemples : Amazon WorkMail, Amazon Chime, Amazon QuickSight.

#### Qu'est-ce que l'élasticité ?

La capacité d'obtenir des ressources quand on en a besoin et de les libérer quand on n'en a plus besoin, automatiquement, en suivant la demande. Exemple : un groupe Auto Scaling qui ajoute des instances EC2 pendant un pic de trafic et les retire ensuite.

#### Qu'est-ce que la scalabilité ?

La capacité d'un système à absorber une charge croissante en ajoutant des ressources. Le scaling vertical consiste à prendre des ressources plus grosses, le scaling horizontal à en ajouter davantage. L'élasticité est une scalabilité qui redescend aussi automatiquement.

#### Quelle est la différence entre scaling vertical et horizontal ?

Le scaling vertical remplace une ressource par une plus grosse (un type d'instance plus grand). C'est simple, mais il y a un plafond et souvent un redémarrage. Le scaling horizontal ajoute des ressources de même taille derrière un équilibreur de charge. Il n'a pas de limite pratique et améliore la disponibilité.

#### Quels sont les avantages d'AWS par rapport à une infrastructure sur site ?

Pas d'achat initial de matériel, on ne paie que ce qu'on utilise, de la capacité en minutes au lieu de mois, une portée mondiale, des services gérés qui suppriment le travail sans valeur ajoutée (correctifs, sauvegardes), sécurité et certifications de conformité intégrées, et la possibilité d'expérimenter à moindre coût et d'arrêter ce qui échoue.

#### Quelle est la différence entre CapEx et OpEx ?

Les dépenses d'investissement (CapEx) sont un investissement initial dans des actifs physiques, comme des serveurs, amortis sur plusieurs années. Les dépenses d'exploitation (OpEx) sont des dépenses courantes en services. Le cloud transforme l'essentiel du CapEx informatique en OpEx.

#### Que signifie « économies d'échelle » dans le cloud ?

AWS achète du matériel, de l'énergie et du réseau à une échelle qu'aucun client n'atteint seul, donc son coût unitaire est plus bas. Une partie de l'économie est répercutée par des baisses de prix, qu'AWS a appliquées de nombreuses fois.

#### Qu'est-ce que la haute disponibilité ?

La capacité d'un système à continuer de fonctionner avec un temps d'arrêt minimal quand des composants tombent en panne. Sur AWS, cela signifie généralement fonctionner sur plusieurs zones de disponibilité, pour que la perte d'un centre de données n'arrête pas l'application.

#### Qu'est-ce que la tolérance aux pannes ?

La capacité à continuer de fonctionner sans interruption quand un composant tombe en panne, généralement grâce à des composants redondants qui prennent le relais automatiquement. C'est une propriété plus forte que la haute disponibilité, qui peut accepter une courte interruption.

#### Qu'est-ce que la reprise après sinistre, et que sont le RTO et le RPO ?

La reprise après sinistre (DR) est l'ensemble des plans permettant de restaurer une charge de travail après une panne majeure. Le RTO (Recovery Time Objective) est la durée d'interruption maximale acceptable. Le RPO (Recovery Point Objective) est la perte de données maximale acceptable, mesurée en temps.

#### Quelles sont les quatre stratégies de reprise après sinistre sur AWS, de la moins chère à la plus rapide ?

1. **Sauvegarde et restauration :** les données sont sauvegardées, l'infrastructure est créée après le sinistre. RTO de plusieurs heures.
2. **Veilleuse (pilot light) :** un noyau minimal (par exemple une base de données répliquée) tourne en permanence, le reste est démarré à la demande.
3. **Veille à chaud (warm standby) :** une copie réduite mais entièrement fonctionnelle tourne et est agrandie lors de la bascule.
4. **Multisite actif/actif :** une production complète dans deux régions ou plus. RTO quasi nul, coût maximal.

#### Qu'est-ce que l'agilité dans le contexte du cloud ?

La vitesse à laquelle on peut obtenir des ressources et tester de nouvelles idées. Des ressources qui prenaient des semaines à arriver sont disponibles en minutes : le coût et le délai d'une expérimentation chutent fortement.

#### Que signifie « se déployer dans le monde entier en quelques minutes » ?

Qu'on peut déployer une application dans des régions AWS du monde entier en quelques clics ou appels d'API, et offrir une latence plus faible aux utilisateurs sans construire de centres de données dans d'autres pays.

#### Qu'est-ce qu'un service géré ?

Un service dont AWS exploite l'infrastructure et les logiciels sous-jacents (provisionnement, correctifs, sauvegardes, montée en charge), et que vous vous contentez d'utiliser. Amazon RDS est une base de données gérée. Faire tourner une base de données sur EC2 ne l'est pas : tout cela est à votre charge.

#### Que signifie « serverless » ?

Exécuter du code ou utiliser un service sans provisionner ni gérer de serveurs. La capacité s'ajuste automatiquement et on paie l'usage réel. Exemples : AWS Lambda, Amazon S3, Amazon DynamoDB, AWS Fargate, Amazon Athena.

#### Qu'est-ce que l'AWS Cloud Adoption Framework (AWS CAF) ?

Un guide qui aide les organisations à planifier leur transformation vers le cloud. Il regroupe les capacités en six perspectives : Métier, Personnes, Gouvernance (orientées métier) et Plateforme, Sécurité, Opérations (techniques).

#### Que sont les 7 R de la migration ?

Retirer (Retire), Conserver (Retain), Réhéberger (Rehost, « lift and shift »), Relocaliser (Relocate, par exemple VMware Cloud on AWS), Racheter (Repurchase, passer au SaaS), Changer de plateforme (Replatform, « lift, tinker and shift », comme passer à RDS) et Refactoriser ou réarchitecturer (Refactor, reconstruire en natif cloud).

### Infrastructure mondiale et Well-Architected Framework

#### Comment l'infrastructure mondiale d'AWS est-elle structurée ?

En régions (zones géographiques distinctes), chacune composée de plusieurs zones de disponibilité (groupes isolés de centres de données). Les emplacements périphériques (edge locations) et les caches périphériques régionaux servent CloudFront et Route 53 au plus près des utilisateurs. Les Local Zones, les Wavelength Zones et Outposts rapprochent AWS des utilisateurs ou de leurs locaux.

#### Quelle est la différence entre une région AWS et une zone de disponibilité ?

Une région est une zone géographique, comme eu-west-3 (Paris), qui contient plusieurs zones de disponibilité. Une zone de disponibilité (AZ) est un ou plusieurs centres de données avec alimentation, réseau et connectivité redondants, physiquement séparés des autres AZ de la région mais reliés à elles par un réseau à faible latence.

#### Combien de zones de disponibilité une région compte-t-elle ?

Au moins trois pour la plupart des régions (les nouvelles régions sont construites avec trois AZ ou plus). Déployer sur au moins deux AZ est la base de la haute disponibilité.

#### Quels sont les quatre critères pour choisir une région ?

1. **Conformité et résidence des données :** la loi peut imposer que les données restent dans un pays.
2. **Proximité des utilisateurs :** latence plus faible.
3. **Disponibilité des services :** tous les services ou fonctionnalités ne sont pas présents dans toutes les régions.
4. **Prix :** un même service peut coûter différemment selon la région.

#### Qu'est-ce qu'un emplacement périphérique (edge location) ?

Un site qui fait tourner les caches CloudFront et le DNS Route 53 (et des services comme Lambda@Edge) près des utilisateurs finaux. Il y a beaucoup plus d'emplacements périphériques que de régions.

#### Qu'est-ce qu'une Local Zone ?

Une extension d'une région placée près d'une grande ville, qui fait tourner certains services (comme EC2 et EBS) pour offrir une latence de quelques millisecondes aux utilisateurs locaux.

#### Qu'est-ce qu'AWS Wavelength ?

Une infrastructure intégrée aux réseaux 5G des opérateurs télécoms, pour que les applications atteignent les appareils mobiles avec une latence très faible.

#### Qu'est-ce qu'AWS Outposts ?

Des baies de matériel gérées par AWS installées dans votre propre centre de données, qui font tourner des services AWS avec les mêmes API et outils. Utilisé pour une faible latence avec des systèmes sur site, le traitement local des données ou la résidence des données.

#### Les services sont-ils mondiaux ou régionaux ?

La plupart sont régionaux : les ressources vivent dans une région. Quelques-uns sont mondiaux : IAM, Route 53, CloudFront, AWS Organizations et WAF pour CloudFront. D'autres, comme les sous-réseaux EC2 et les volumes EBS, sont limités à une zone de disponibilité.

#### Qu'est-ce que l'AWS Well-Architected Framework ?

Un ensemble de bonnes pratiques et de questions pour concevoir et évaluer des charges de travail sur AWS, organisé en six piliers. L'outil Well-Architected Tool de la console mène une revue structurée d'une charge de travail.

#### Quels sont les six piliers du Well-Architected Framework ?

Excellence opérationnelle, Sécurité, Fiabilité, Efficacité des performances, Optimisation des coûts et Durabilité.

#### Sur quoi porte le pilier Excellence opérationnelle ?

Exploiter et superviser les systèmes et améliorer continuellement les processus : opérations sous forme de code, changements petits et réversibles, apprendre des pannes et les anticiper.

#### Sur quoi porte le pilier Sécurité ?

Protéger les données, les systèmes et les actifs : une base d'identités solide, la traçabilité, la sécurité à chaque couche, des contrôles automatisés, le chiffrement en transit et au repos, et la préparation aux incidents de sécurité.

#### Sur quoi porte le pilier Fiabilité ?

Qu'une charge de travail remplisse sa fonction correctement et de façon constante : reprise automatique après une panne, tests des procédures de reprise, scaling horizontal et gestion des changements par l'automatisation.

#### Sur quoi porte le pilier Efficacité des performances ?

Utiliser les ressources efficacement à mesure que la demande et les technologies évoluent : choisir les bons types de ressources, utiliser des services gérés et serverless, se déployer mondialement en minutes et expérimenter souvent.

#### Sur quoi porte le pilier Optimisation des coûts ?

Apporter de la valeur au prix le plus bas : ne payer que ce qu'on utilise, mesurer l'efficacité, ne pas dépenser pour du travail sans valeur ajoutée, analyser et attribuer les dépenses.

#### Sur quoi porte le pilier Durabilité ?

Réduire l'impact environnemental des charges de travail : comprendre son impact, maximiser l'utilisation, utiliser des services gérés et du matériel plus efficace, et réduire les ressources nécessaires aux utilisateurs.

#### Que signifie « concevoir pour la panne » ?

Partir du principe que tout composant peut tomber en panne, et construire le système pour qu'il continue de fonctionner quand cela arrive : plusieurs AZ, contrôles de santé, remplacement automatique, nouvelles tentatives et composants découplés.

#### Qu'est-ce que le couplage faible, et quels services aident à l'obtenir ?

Concevoir les composants de sorte qu'une panne ou un ralentissement de l'un ne se propage pas aux autres. Les files d'attente (Amazon SQS), les notifications (Amazon SNS), les bus d'événements (Amazon EventBridge) et les équilibreurs de charge permettent aux composants de communiquer sans dépendre directement les uns des autres.

#### Quelle est la différence entre une application sans état et avec état ?

Un composant sans état ne garde aucune donnée de session entre deux requêtes : n'importe quelle instance peut traiter n'importe quelle requête, et on peut ajouter ou retirer des instances librement. L'état est stocké ailleurs (DynamoDB, ElastiCache, S3). Les composants avec état sont plus difficiles à faire monter en charge horizontalement.

#### Qu'est-ce que l'infrastructure as code, et pourquoi le Well-Architected Framework la recommande-t-il ?

Définir l'infrastructure dans des modèles ou du code versionnés (CloudFormation, AWS CDK) plutôt que par des clics manuels dans la console. Les environnements deviennent reproductibles, relisibles et rapides à reconstruire, ce qui sert l'excellence opérationnelle et la fiabilité.

### Sécurité, modèle de responsabilité partagée et IAM

#### Qu'est-ce que le modèle de responsabilité partagée d'AWS ?

La sécurité est partagée entre AWS et le client. AWS est responsable de la sécurité **du** cloud (matériel, infrastructure mondiale, locaux, couche de virtualisation, logiciels des services gérés). Le client est responsable de la sécurité **dans** le cloud (données, identités et permissions, systèmes d'exploitation et applications qu'il exécute, configuration réseau et pare-feu, choix de chiffrement).

#### Comment le modèle de responsabilité partagée évolue-t-il entre EC2, RDS et S3 ?

Plus le service est géré, moins le client en a la charge. Sur EC2, vous appliquez les correctifs du système d'exploitation invité et des logiciels. Sur RDS, AWS corrige le système d'exploitation et le moteur de base de données, et vous gérez les utilisateurs, l'accès réseau et les données. Sur S3, vous gérez les données, les politiques d'accès et le chiffrement.

#### Qui est responsable des correctifs du système d'exploitation d'une instance EC2 ?

Le client. AWS corrige l'hyperviseur et les serveurs physiques. Des outils comme AWS Systems Manager Patch Manager aident à automatiser les correctifs du système invité.

#### Qui est responsable de la sécurité physique des centres de données ?

AWS. Les clients n'ont jamais accès physiquement aux centres de données d'AWS.

#### Quelles responsabilités sont partagées par les deux ?

La gestion des correctifs (AWS corrige l'infrastructure, le client ses systèmes invités et ses applications), la gestion de la configuration, et la sensibilisation et la formation (chacun forme son propre personnel).

#### Qu'est-ce qu'AWS Identity and Access Management (IAM) ?

Le service mondial qui contrôle qui peut se connecter à un compte AWS (authentification) et ce qu'il peut faire (autorisation). Il gère utilisateurs, groupes, rôles et politiques, sans coût supplémentaire.

#### Qu'est-ce que l'utilisateur racine, et comment le protéger ?

L'identité créée avec le compte, avec un accès illimité à tout, y compris la facturation et la fermeture du compte. Protégez-le avec un mot de passe robuste et le MFA, supprimez ses clés d'accès et ne l'utilisez que pour les rares tâches qui l'exigent.

#### Quelles tâches seul l'utilisateur racine peut-il effectuer ?

Par exemple : modifier l'adresse e-mail ou le nom du compte, fermer le compte, changer de plan AWS Support, restaurer les permissions IAM quand le seul administrateur s'est bloqué lui-même, et certains réglages de facturation.

#### Qu'est-ce qu'un utilisateur IAM ?

Une identité qui représente une personne ou une application, avec des identifiants de longue durée : un mot de passe pour la console et/ou des clés d'accès pour l'API. AWS recommande, pour les personnes, des identifiants fédérés ou temporaires plutôt que des utilisateurs IAM quand c'est possible.

#### Qu'est-ce qu'un groupe IAM ?

Un ensemble d'utilisateurs IAM. Les politiques attachées au groupe s'appliquent à tous ses membres, ce qui simplifie la gestion des permissions. Les groupes ne peuvent pas être imbriqués et ne sont pas des identités.

#### Qu'est-ce qu'un rôle IAM ?

Une identité dotée de permissions mais sans identifiants de longue durée. Une entité de confiance (un service AWS comme EC2 ou Lambda, un utilisateur, un autre compte ou une identité fédérée) assume le rôle et reçoit des identifiants temporaires d'AWS STS.

#### Pourquoi une instance EC2 doit-elle utiliser un rôle plutôt que des clés d'accès ?

Des clés stockées sur l'instance peuvent fuiter et doivent être renouvelées à la main. Un rôle fournit des identifiants temporaires renouvelés automatiquement via les métadonnées de l'instance, sans rien de secret sur le disque.

#### Qu'est-ce qu'une politique IAM ?

Un document JSON qui autorise ou refuse des actions sur des ressources, sous des conditions facultatives. Les politiques basées sur l'identité s'attachent aux utilisateurs, groupes ou rôles. Les politiques basées sur les ressources (comme les politiques de compartiment S3) s'attachent aux ressources.

#### Que contient une instruction de politique IAM ?

`Effect` (Allow ou Deny), `Action` (par exemple `s3:GetObject`), `Resource` (un ARN) et, en option, `Condition` (par exemple une IP source ou un MFA obligatoire). Les politiques basées sur les ressources ont aussi un `Principal`.

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject"],
    "Resource": "arn:aws:s3:::my-bucket/reports/*"
  }]
}
```

#### Comment IAM évalue-t-il les permissions quand des politiques se contredisent ?

Tout est refusé par défaut. Un Allow explicite accorde l'accès, mais un Deny explicite où que ce soit l'emporte toujours sur n'importe quel Allow.

#### Qu'est-ce que le principe du moindre privilège ?

N'accorder que les permissions nécessaires à une tâche, et rien de plus. Commencez petit et ajoutez des permissions au besoin. IAM Access Analyzer peut générer des politiques à partir de l'activité réelle.

#### Qu'est-ce que l'authentification multifacteur (MFA), et quels appareils AWS prend-il en charge ?

Un second facteur en plus du mot de passe. AWS prend en charge les clés d'accès (passkeys) et les clés de sécurité FIDO2, les applications d'authentification virtuelles et les jetons TOTP matériels.

#### Que sont les clés d'accès ?

Une paire formée d'un ID de clé d'accès et d'une clé d'accès secrète, utilisée pour signer les requêtes programmatiques (CLI, SDK). Ce sont des identifiants de longue durée : ne les mettez jamais dans le code, renouvelez-les, et préférez les rôles ou IAM Identity Center quand c'est possible.

#### Qu'est-ce qu'AWS IAM Identity Center ?

Le successeur d'AWS Single Sign-On. Il gère de façon centralisée l'accès des collaborateurs à plusieurs comptes AWS et applications métier, avec son propre annuaire ou un fournisseur d'identité externe (Microsoft Entra ID, Okta, Active Directory).

#### Qu'est-ce que la fédération d'identités ?

Permettre aux utilisateurs de se connecter avec une identité existante (annuaire d'entreprise, fournisseur SAML 2.0 ou OIDC) et de recevoir des identifiants AWS temporaires, sans créer d'utilisateurs IAM pour eux.

#### Qu'est-ce qu'AWS STS ?

AWS Security Token Service délivre des identifiants temporaires aux privilèges limités, par exemple quand un rôle est assumé ou qu'un utilisateur fédéré se connecte.

#### Qu'est-ce que le rapport d'identifiants IAM ?

Un CSV au niveau du compte qui liste tous les utilisateurs et l'état de leurs identifiants : mots de passe, clés d'accès, MFA, dates de dernière utilisation. Utile pour les audits.

#### Qu'est-ce qu'IAM Access Advisor ?

Une vue qui montre à quels services un utilisateur, un groupe ou un rôle a accès et quand il les a utilisés pour la dernière fois. Elle aide à retirer les permissions inutilisées.

#### Qu'est-ce qu'un ARN ?

Un Amazon Resource Name identifie une ressource de façon unique : `arn:partition:service:region:account-id:resource`, par exemple `arn:aws:s3:::my-bucket`.

#### Qu'est-ce qu'une politique de mots de passe dans IAM ?

Des règles du compte pour les mots de passe des utilisateurs IAM : longueur minimale, types de caractères obligatoires, expiration, interdiction de réutilisation.

### Services de sécurité et conformité

#### Qu'est-ce qu'AWS Organizations ?

Un service pour gérer de façon centralisée plusieurs comptes AWS : les regrouper en unités d'organisation (OU), leur appliquer des politiques et consolider la facturation. Un compte de gestion possède l'organisation.

#### Que sont les Service Control Policies (SCP) ?

Des politiques d'AWS Organizations qui fixent les permissions maximales de comptes ou d'OU. Elles n'accordent rien : elles limitent ce que les politiques IAM de ces comptes peuvent autoriser, même pour l'utilisateur racine d'un compte membre.

#### Qu'est-ce qu'AWS Control Tower ?

Un service qui met en place et gouverne un environnement multicompte sécurisé (une landing zone) selon les bonnes pratiques, avec des garde-fous préventifs et de détection et un tableau de bord.

#### Qu'est-ce qu'AWS Key Management Service (KMS) ?

Un service géré pour créer et contrôler des clés de chiffrement et les utiliser pour chiffrer des données. Il est intégré à la plupart des services AWS et journalise l'utilisation des clés dans CloudTrail.

#### Quelle est la différence entre AWS KMS et AWS CloudHSM ?

KMS est un service géré mutualisé dont AWS exploite les modules de sécurité matériels. CloudHSM vous fournit des HSM dédiés, à locataire unique, que vous contrôlez, pour des exigences de conformité strictes.

#### Quelle est la différence entre chiffrement au repos et en transit ?

Au repos, il protège les données stockées (objets S3, volumes EBS, fichiers de base de données), généralement avec des clés KMS. En transit, il protège les données qui circulent sur le réseau, généralement avec TLS.

#### Qu'est-ce qu'AWS Certificate Manager (ACM) ?

Un service qui émet, gère et renouvelle des certificats SSL/TLS à utiliser avec des services AWS comme Elastic Load Balancing, CloudFront et API Gateway. Les certificats publics sont gratuits.

#### Qu'est-ce qu'AWS Secrets Manager ?

Un service pour stocker, récupérer et renouveler automatiquement des secrets comme les mots de passe de base de données et les clés d'API, pour qu'ils ne soient pas écrits en dur dans les applications.

#### Quelle est la différence entre Secrets Manager et Systems Manager Parameter Store ?

Les deux stockent de la configuration et des secrets. Secrets Manager ajoute la rotation automatique intégrée et le partage entre comptes, avec un coût par secret. Le niveau standard de Parameter Store est gratuit et convient aux valeurs de configuration et aux secrets simples sans rotation.

#### Qu'est-ce qu'AWS Shield ?

Une protection gérée contre les attaques DDoS. Shield Standard est automatique et gratuit pour tous les clients face aux attaques courantes des couches réseau et transport. Shield Advanced est payant et ajoute une protection contre les attaques plus importantes, un accès 24 h/24 et 7 j/7 à la Shield Response Team et une protection des coûts.

#### Qu'est-ce qu'AWS WAF ?

Un pare-feu applicatif web qui filtre les requêtes HTTP(S) vers CloudFront, Application Load Balancer, API Gateway et AppSync avec des règles (listes d'IP, limites de débit, motifs d'injection SQL et de cross-site scripting, groupes de règles gérés).

#### Qu'est-ce qu'Amazon GuardDuty ?

Un service intelligent de détection des menaces qui analyse en continu les événements CloudTrail, les VPC Flow Logs et les journaux DNS (et en option d'autres sources) par apprentissage automatique et renseignement sur les menaces, pour repérer une activité suspecte comme des identifiants compromis ou du minage de cryptomonnaies.

#### Qu'est-ce qu'Amazon Inspector ?

Un service automatisé de gestion des vulnérabilités qui analyse les instances EC2, les images de conteneurs dans ECR et les fonctions Lambda à la recherche de vulnérabilités logicielles et d'expositions réseau non voulues.

#### Qu'est-ce qu'Amazon Macie ?

Un service qui utilise l'apprentissage automatique et la reconnaissance de motifs pour découvrir et protéger les données sensibles, comme les données personnelles, dans Amazon S3.

#### Qu'est-ce qu'AWS Security Hub ?

Une vue centrale des alertes de sécurité et de l'état de conformité de plusieurs comptes. Il agrège les résultats de GuardDuty, Inspector, Macie et d'outils partenaires, et exécute des contrôles automatiques selon des référentiels comme les benchmarks CIS.

#### Qu'est-ce qu'Amazon Detective ?

Un service qui analyse et visualise les données de sécurité pour enquêter sur la cause racine d'une alerte ou d'une activité suspecte.

#### Qu'est-ce qu'AWS Artifact ?

Un portail en libre-service qui donne accès aux rapports de conformité d'AWS (SOC, ISO, PCI DSS) et aux accords (comme le Business Associate Addendum pour HIPAA).

#### Qu'est-ce que le programme de conformité d'AWS ?

AWS maintient des certifications et attestations (ISO 27001, SOC 1/2/3, PCI DSS, éligibilité HIPAA, accompagnement RGPD) pour son infrastructure. Les clients héritent des contrôles de l'infrastructure, mais doivent rendre leurs propres charges de travail conformes.

#### Faut-il l'autorisation d'AWS pour réaliser un test d'intrusion ?

Pas pour une liste de services autorisés (EC2, RDS, Lambda, CloudFront et d'autres). Certaines activités restent interdites, comme les attaques DoS, qui nécessitent une procédure d'approbation distincte pour les événements simulés.

#### Qu'est-ce qu'AWS Abuse, et quand le contacter ?

L'équipe d'AWS à qui signaler que des ressources AWS sont utilisées de façon abusive, par exemple pour du spam, du scan de ports, des attaques DoS ou l'hébergement de logiciels malveillants.

### Calcul : EC2, conteneurs et serverless

#### Qu'est-ce qu'Amazon EC2 et quelles sont ses principales fonctionnalités ?

Elastic Compute Cloud fournit des serveurs virtuels redimensionnables (instances). Fonctionnalités principales : de nombreux types d'instances, le choix du système d'exploitation via les AMI, plusieurs modèles de tarification, le stockage EBS et le stockage d'instance, les groupes de sécurité, Auto Scaling, les adresses IP Elastic et le placement dans n'importe quelle AZ.

#### Qu'est-ce qu'une AMI ?

Une Amazon Machine Image est un modèle qui contient le système d'exploitation, les logiciels et la configuration utilisés pour lancer des instances. On peut utiliser des AMI d'AWS, du Marketplace, de la communauté ou les siennes.

#### Quelles sont les familles d'instances EC2 ?

- **Usage général** (M, T) : CPU, mémoire et réseau équilibrés.
- **Optimisées pour le calcul** (C) : processeurs haute performance, pour le traitement par lots, le jeu vidéo, la modélisation scientifique.
- **Optimisées pour la mémoire** (R, X) : de grands jeux de données en mémoire.
- **Calcul accéléré** (P, G, Inf, Trn) : GPU ou puces spécialisées pour l'apprentissage automatique et le graphisme.
- **Optimisées pour le stockage** (I, D) : lectures et écritures séquentielles intensives sur stockage local, pour les entrepôts de données et l'OLTP.

#### Que sont les instances T et la performance en rafale ?

Les instances T fournissent un niveau de CPU de base et accumulent des crédits CPU au repos, qu'elles dépensent pour dépasser ce niveau. Elles conviennent aux charges à CPU moyen faible avec des pics occasionnels.

#### Quelles sont les options de tarification d'EC2 ?

- **À la demande :** paiement à la seconde ou à l'heure, sans engagement.
- **Savings Plans :** engagement sur une dépense horaire pendant 1 ou 3 ans, jusqu'à environ 72 % de remise.
- **Instances réservées :** engagement sur une configuration d'instance pendant 1 ou 3 ans.
- **Instances Spot :** capacité inutilisée jusqu'à 90 % moins chère, interruptible avec un préavis de deux minutes.
- **Hôtes dédiés :** un serveur physique pour vous, pour les licences et la conformité.
- **Instances dédiées :** des instances sur du matériel non partagé avec d'autres comptes.
- **Réservations de capacité :** réserver de la capacité dans une AZ, au prix à la demande.

#### Quand utiliser des instances Spot ?

Pour des charges flexibles, tolérantes aux pannes et interruptibles : traitements par lots, traitement de données, builds CI, serveurs web sans état. Jamais pour une base de données qui ne peut pas s'arrêter.

#### Quelle est la différence entre Compute Savings Plans et EC2 Instance Savings Plans ?

Les Compute Savings Plans s'appliquent à toute famille, taille, région et système d'exploitation, ainsi qu'à Fargate et Lambda. Les EC2 Instance Savings Plans sont liés à une famille d'instances dans une région, mais offrent une remise plus forte.

#### Quand a-t-on besoin d'un hôte dédié ?

Quand des licences logicielles sont liées aux cœurs ou sockets physiques (apporter sa propre licence), ou quand la conformité exige la visibilité et le contrôle du serveur physique.

#### Qu'est-ce qu'un groupe de sécurité ?

Un pare-feu virtuel avec état pour les instances (attaché aux interfaces réseau). Il n'a que des règles d'autorisation. Le trafic de retour est autorisé automatiquement, et par défaut tout le trafic entrant est refusé et tout le trafic sortant autorisé.

#### Qu'est-ce qu'EC2 Auto Scaling ?

Un service qui ajoute ou retire des instances EC2 d'un groupe Auto Scaling selon des politiques (suivi de cible, par paliers, planifiées, prédictives), et remplace les instances défaillantes. On définit une capacité minimale, souhaitée et maximale.

#### Qu'est-ce qu'Elastic Load Balancing, et quels en sont les types ?

Un service qui répartit le trafic entre des cibles dans plusieurs AZ et vérifie leur santé.
- **Application Load Balancer :** HTTP/HTTPS, couche 7, routage par chemin et par hôte.
- **Network Load Balancer :** TCP/UDP/TLS, couche 4, très hautes performances et IP statiques.
- **Gateway Load Balancer :** couche 3, pour les appliances réseau tierces comme les pare-feu.

#### Qu'est-ce qu'une adresse IP Elastic ?

Une adresse IPv4 publique statique que vous allouez à votre compte et pouvez attacher à une instance. Les adresses IPv4 publiques sont facturées à l'heure, attachées ou non.

#### Que sont les données utilisateur (user data) d'EC2 ?

Un script passé au lancement, exécuté au premier démarrage, pour installer des logiciels ou configurer l'instance.

#### Qu'est-ce qu'AWS Lambda ?

Un service de calcul serverless qui exécute votre fonction en réponse à des événements (un appel d'API, un fichier dans S3, un message, une planification). On paie par requête et par durée à la milliseconde. Une invocation dure au maximum 15 minutes.

#### Quand choisir Lambda plutôt qu'EC2 ?

Pour des charges événementielles, courtes, variables ou imprévisibles, sans vouloir gérer de serveurs. EC2 convient aux processus de longue durée, aux besoins particuliers de système d'exploitation ou à une charge élevée et constante.

#### Quelle est la différence entre Amazon ECS et Amazon EKS ?

Les deux orchestrent des conteneurs. ECS est l'orchestrateur propre à AWS, plus simple. EKS est du Kubernetes géré, pour les équipes qui utilisent l'outillage Kubernetes ou ont besoin de portabilité.

#### Qu'est-ce qu'AWS Fargate ?

Un moteur de calcul serverless pour conteneurs qui fonctionne avec ECS et EKS. On définit le CPU et la mémoire par tâche ou par pod, et AWS les exécute sans serveur à gérer.

#### Qu'est-ce qu'Amazon ECR ?

Elastic Container Registry, un registre géré pour stocker, analyser et partager des images de conteneurs Docker et OCI.

#### Qu'est-ce qu'AWS Elastic Beanstalk ?

Une plateforme en tant que service : vous déposez le code de l'application (Java, .NET, Node.js, Python, PHP, Go, Ruby, Docker) et Beanstalk provisionne et gère EC2, l'équilibrage de charge, Auto Scaling et la supervision. Les ressources sous-jacentes restent visibles et configurables.

#### Qu'est-ce qu'Amazon Lightsail ?

Un service simplifié de serveurs privés virtuels, de bases de données et de conteneurs à prix mensuel prévisible, destiné aux sites simples et aux débutants sur AWS.

#### Qu'est-ce qu'AWS Batch ?

Un service qui exécute des traitements par lots à n'importe quelle échelle, en provisionnant de la capacité EC2 ou Fargate (y compris Spot) selon les travaux en file d'attente.

#### Qu'est-ce qu'AWS App Runner ?

Un service entièrement géré qui construit et exécute des applications web et des API à partir de code source ou d'une image de conteneur, avec montée en charge automatique et HTTPS.

#### Qu'est-ce que le stockage d'instance (instance store) d'EC2 ?

Un stockage en mode bloc temporaire, physiquement attaché au serveur hôte. Il est très rapide, mais ses données sont perdues quand l'instance s'arrête ou est résiliée : il sert aux tampons, aux caches et aux données temporaires.

#### Qu'apportent EC2 Instance Connect et Session Manager ?

Des moyens d'accéder aux instances sans gérer de clés SSH. Session Manager (dans Systems Manager) fonctionne même sans ouvrir de port entrant, et journalise les sessions.

#### Quelle est la différence entre arrêter et résilier une instance ?

L'arrêter l'éteint : les volumes EBS racine sont conservés, on ne paie que le stockage, et on peut la redémarrer. La résilier la supprime, ainsi que, par défaut, son volume EBS racine.

### Stockage

#### Qu'est-ce qu'Amazon S3 et quelles classes de stockage propose-t-il ?

Simple Storage Service est un stockage d'objets d'une durabilité de 11 neuf (99,999999999 %), où les données sont stockées sous forme d'objets dans des compartiments (buckets). Classes de stockage :
- **S3 Standard :** données consultées fréquemment.
- **S3 Intelligent-Tiering :** déplace automatiquement les objets entre niveaux quand les profils d'accès sont inconnus ou changent.
- **S3 Standard-IA :** accès peu fréquent, récupération en millisecondes, avec frais de récupération.
- **S3 One Zone-IA :** accès peu fréquent stocké dans une seule AZ, moins cher et moins résilient.
- **S3 Express One Zone :** latence de quelques millisecondes pour les données les plus sensibles aux performances.
- **S3 Glacier Instant Retrieval :** archive consultée environ une fois par trimestre, récupération en millisecondes.
- **S3 Glacier Flexible Retrieval :** archive, récupération en minutes ou en heures.
- **S3 Glacier Deep Archive :** la moins chère, récupération en 12 à 48 heures.

#### Que sont un compartiment et un objet S3 ?

Un compartiment (bucket) est un conteneur d'objets au nom unique au niveau mondial, créé dans une région. Un objet est un fichier et ses métadonnées, identifié par une clé, jusqu'à 5 To.

#### Que sont les règles de cycle de vie S3 ?

Des règles qui font passer automatiquement les objets vers des classes de stockage moins chères au-delà d'un certain âge, ou qui les suppriment (expiration).

#### Qu'est-ce que la gestion des versions S3 ?

Une option du compartiment qui conserve chaque version d'un objet, pour pouvoir restaurer des objets écrasés ou supprimés.

#### Comment contrôler l'accès à S3 ?

Avec des politiques IAM, des politiques de compartiment, des points d'accès, des ACL (désactivées par défaut aujourd'hui) et Block Public Access, qui empêche l'accès public au niveau du compartiment ou du compte. Les URL présignées donnent un accès temporaire à un objet.

#### Comment les données S3 sont-elles chiffrées ?

Tous les nouveaux objets sont chiffrés au repos par défaut avec des clés gérées par S3 (SSE-S3). On peut choisir des clés KMS (SSE-KMS), des clés fournies par le client (SSE-C) ou chiffrer côté client avant l'envoi.

#### Qu'est-ce que la réplication S3 ?

La copie automatique et asynchrone d'objets vers un autre compartiment dans une autre région (Cross-Region Replication) ou la même région (Same-Region Replication). Elle nécessite la gestion des versions.

#### Qu'est-ce que l'hébergement de site web statique sur S3 ?

Servir un site composé de fichiers statiques (HTML, CSS, JS, images) directement depuis un compartiment, généralement derrière CloudFront pour le HTTPS et le cache.

#### Qu'est-ce que S3 Transfer Acceleration ?

Des envois plus rapides sur de longues distances, en les faisant passer par les emplacements périphériques de CloudFront et le réseau dorsal d'AWS.

#### Qu'est-ce qu'Amazon EBS ?

Elastic Block Store fournit des volumes en mode bloc via le réseau pour les instances EC2, qui persistent indépendamment de la vie de l'instance. Un volume vit dans une AZ et y est répliqué. Types : gp3 (SSD usage général), io2 (SSD à IOPS provisionnées), st1 (HDD optimisé débit) et sc1 (HDD froid).

#### Que sont les instantanés EBS ?

Des sauvegardes incrémentielles à un instant donné de volumes EBS, stockées dans S3 (géré par AWS). Ils peuvent être copiés dans d'autres régions et servir à créer de nouveaux volumes.

#### Qu'est-ce qu'Amazon EFS ?

Elastic File System est un système de fichiers NFS géré pour Linux qui grandit et rétrécit automatiquement et peut être monté simultanément par de nombreuses instances sur plusieurs AZ.

#### Quelle est la différence entre S3, EBS et EFS ?

S3 est un stockage d'objets accessible par API, pratiquement illimité, pour n'importe quel nombre de clients. EBS est un stockage en mode bloc attaché (en général) à une instance dans une AZ, comme un disque. EFS est un système de fichiers partagé entre de nombreuses instances Linux sur plusieurs AZ.

#### Qu'est-ce qu'Amazon FSx ?

Des systèmes de fichiers tiers entièrement gérés : FSx for Windows File Server (SMB), FSx for Lustre (calcul haute performance), FSx for NetApp ONTAP et FSx for OpenZFS.

#### Qu'est-ce qu'AWS Storage Gateway ?

Un service de stockage hybride qui donne aux applications sur site un accès au stockage cloud. Types : S3 File Gateway, FSx File Gateway, Volume Gateway et Tape Gateway (bibliothèque de bandes virtuelle pour les sauvegardes).

#### Qu'est-ce que la famille AWS Snow ?

Des appareils physiques pour transférer hors ligne de grandes quantités de données vers ou depuis AWS, ou traiter des données en périphérie avec peu ou pas de connectivité (appareils AWS Snowball Edge).

#### Qu'est-ce qu'AWS Backup ?

Un service central pour automatiser et auditer les sauvegardes de nombreux services : EBS, EC2, RDS, DynamoDB, EFS, FSx, S3 et d'autres, avec des plans de sauvegarde et des copies entre régions ou entre comptes.

#### Qu'est-ce qu'AWS DataSync ?

Un service de transfert de données en ligne qui déplace des données entre un stockage sur site (NFS, SMB, HDFS, stockage objet) et les services de stockage AWS, rapidement et avec vérification.

#### Quelles sont la durabilité et la disponibilité de S3 Standard ?

Il est conçu pour une durabilité de 99,999999999 % et une disponibilité de 99,99 %, avec les données stockées sur au moins trois AZ.

#### Quand utiliser S3 One Zone-IA ?

Pour des données peu consultées qu'on peut recréer, comme des copies de sauvegarde secondaires ou des données dérivées, quand la perte d'une AZ est acceptable en échange d'un prix plus bas.

### Bases de données et analytique

#### En quoi Amazon RDS diffère-t-il d'Amazon DynamoDB ?

RDS est un service de bases de données relationnelles géré (SQL, schémas, jointures, transactions) qui fait tourner MySQL, PostgreSQL, MariaDB, Oracle, SQL Server ou Db2 sur des instances que vous dimensionnez. DynamoDB est une base NoSQL serverless clé-valeur et documents, avec des performances de quelques millisecondes à toute échelle, sans schéma fixe au-delà des clés et avec une montée en charge automatique.

#### Que gère Amazon RDS pour vous ?

Le provisionnement, les correctifs du système d'exploitation et de la base de données, les sauvegardes automatiques et la restauration à un instant donné, la bascule Multi-AZ, les réplicas en lecture, la supervision et l'extension du stockage. Vous gérez le schéma, les requêtes, les utilisateurs et l'accès réseau.

#### Quelle est la différence entre RDS Multi-AZ et les réplicas en lecture ?

Multi-AZ maintient une ou plusieurs instances de secours synchrones dans une autre AZ pour la haute disponibilité et la bascule automatique. Dans sa configuration classique, elle ne sert pas les lectures. Les réplicas en lecture sont des copies asynchrones pour répartir les lectures, éventuellement dans d'autres régions, et peuvent être promus.

#### Qu'est-ce qu'Amazon Aurora ?

Une base de données relationnelle native cloud compatible MySQL et PostgreSQL. Elle stocke six copies des données sur trois AZ, étend son stockage automatiquement et propose Aurora Serverless pour les charges variables.

#### Qu'est-ce qu'Amazon ElastiCache ?

Un cache en mémoire géré avec Valkey, Redis OSS ou Memcached, utilisé pour réduire la charge de la base de données et servir les lectures fréquentes avec une latence de l'ordre de la microseconde.

#### Qu'est-ce qu'Amazon MemoryDB ?

Une base de données en mémoire durable, compatible Valkey et Redis OSS, utilisable comme base principale grâce à son journal de transactions Multi-AZ.

#### Qu'est-ce qu'Amazon Redshift ?

Un entrepôt de données cloud géré, à l'échelle du pétaoctet, pour les requêtes SQL analytiques (OLAP), avec stockage en colonnes, une option serverless et la possibilité d'interroger des données dans S3.

#### Quelle est la différence entre OLTP et OLAP, et quels services AWS conviennent à chacun ?

L'OLTP gère beaucoup de petites lectures et écritures transactionnelles (commandes, paiements) : RDS, Aurora, DynamoDB. L'OLAP exécute de grosses requêtes analytiques sur des données historiques : Redshift, Athena.

#### Qu'est-ce qu'Amazon DocumentDB ?

Une base de données documentaire gérée, compatible avec les charges de travail MongoDB.

#### Qu'est-ce qu'Amazon Neptune ?

Une base de données de graphes gérée pour des données très connectées, comme les réseaux sociaux, la détection de fraude et les graphes de connaissances.

#### Qu'est-ce qu'Amazon Keyspaces ?

Une base de données serverless gérée, compatible Apache Cassandra.

#### Qu'est-ce qu'Amazon Timestream ?

Une base de données de séries temporelles gérée pour l'IoT et les métriques opérationnelles.

#### Qu'est-ce qu'AWS Database Migration Service (DMS) ?

Un service qui migre des bases de données vers AWS avec une interruption minimale, entre moteurs identiques (homogène) ou différents (hétérogène, avec la Schema Conversion Tool), et qui peut répliquer les changements en continu.

#### Qu'est-ce qu'Amazon Athena ?

Un service de requêtes interactives serverless pour analyser des données dans S3 en SQL standard. On paie au volume de données analysé : les formats en colonnes et le partitionnement réduisent le coût.

#### Qu'est-ce qu'AWS Glue ?

Un service d'intégration de données serverless : des crawlers pour découvrir les schémas, le Glue Data Catalog comme référentiel central de métadonnées, et des jobs ETL basés sur Spark.

#### Qu'est-ce qu'Amazon EMR ?

Une plateforme big data gérée pour exécuter Apache Spark, Hive, Presto/Trino, HBase et d'autres frameworks sur EC2, EKS ou en serverless.

#### Qu'est-ce qu'Amazon Kinesis ?

Des services pour les données en streaming en temps réel. Kinesis Data Streams capture et stocke des flux pour un traitement sur mesure. Amazon Data Firehose charge des flux vers des destinations comme S3, Redshift ou OpenSearch.

#### Qu'est-ce qu'Amazon QuickSight ?

Un service de business intelligence serverless pour créer des tableaux de bord et des rapports interactifs, avec des analyses fondées sur l'apprentissage automatique et des questions en langage naturel.

#### Qu'est-ce qu'Amazon OpenSearch Service ?

Un service géré pour les clusters OpenSearch (et l'ancien Elasticsearch), utilisé pour l'analyse de journaux, la recherche plein texte et l'observabilité.

#### Qu'est-ce qu'AWS Lake Formation ?

Un service pour construire, sécuriser et gérer un data lake sur S3, avec des permissions centralisées et fines sur les tables du Glue Data Catalog.

### Réseau et diffusion de contenu

#### Qu'est-ce qu'Amazon VPC ?

Virtual Private Cloud est un réseau virtuel isolé logiquement, dans une région, où l'on lance des ressources. On choisit sa plage d'adresses IP et on crée des sous-réseaux, des tables de routage et des passerelles.

#### Quelle est la différence entre un sous-réseau public et un sous-réseau privé ?

Un sous-réseau public a une route vers une passerelle internet : les ressources dotées d'une IP publique sont joignables depuis internet. Un sous-réseau privé n'a pas cette route : ses ressources ne sortent sur internet, le cas échéant, que par une passerelle NAT.

#### Qu'est-ce qu'une passerelle internet ?

Un composant du VPC qui permet la communication entre les ressources du VPC et internet.

#### Qu'est-ce qu'une passerelle NAT ?

Un service géré qui permet aux instances de sous-réseaux privés d'ouvrir des connexions sortantes vers internet (pour des mises à jour, par exemple) tout en bloquant les connexions entrantes non sollicitées.

#### Quelle est la différence entre un groupe de sécurité et une ACL réseau ?

Un groupe de sécurité agit au niveau de l'instance (interface réseau), il est avec état et n'a que des règles d'autorisation. Une ACL réseau agit au niveau du sous-réseau, elle est sans état (le trafic de retour doit être autorisé explicitement), accepte des règles d'autorisation et de refus, et évalue les règles par ordre de numéro.

#### Qu'est-ce que l'appairage de VPC (VPC peering) ?

Une connexion réseau privée entre deux VPC (d'un même compte ou de comptes ou régions différents). Elle n'est pas transitive.

#### Qu'est-ce qu'AWS Transit Gateway ?

Un concentrateur qui relie de nombreux VPC et réseaux sur site par une seule passerelle, au lieu de maillages complexes d'appairages.

#### Qu'est-ce qu'AWS Site-to-Site VPN ?

Une connexion IPsec chiffrée entre un réseau sur site et un VPC via internet. Rapide à mettre en place, mais ses performances dépendent d'internet.

#### Qu'est-ce qu'AWS Direct Connect ?

Une connexion réseau privée et dédiée entre vos locaux et AWS. Elle offre une bande passante et une latence constantes et peut réduire les coûts de transfert, mais sa mise en place prend des semaines. Elle n'est pas chiffrée par défaut.

#### Qu'est-ce qu'AWS Client VPN ?

Un service VPN géré qui permet à des utilisateurs individuels de se connecter de façon sécurisée à AWS et aux réseaux sur site depuis leurs appareils.

#### Qu'est-ce qu'un point de terminaison de VPC (VPC endpoint) ?

Une connexion privée d'un VPC vers des services AWS sans passer par internet. Les points de terminaison de passerelle servent S3 et DynamoDB. Les points de terminaison d'interface (AWS PrivateLink) servent beaucoup d'autres services.

#### Qu'est-ce qu'AWS PrivateLink ?

Une technologie qui expose des services de façon privée entre VPC et comptes via des points de terminaison d'interface, en gardant le trafic sur le réseau AWS.

#### Que sont les VPC Flow Logs ?

Des enregistrements du trafic IP entrant et sortant des interfaces réseau d'un VPC, envoyés vers CloudWatch Logs ou S3 pour le dépannage et l'analyse de sécurité.

#### Qu'est-ce qu'Amazon Route 53 ?

Un service DNS hautement disponible et un registraire de noms de domaine, avec des contrôles de santé et des politiques de routage.

#### Quelles sont les politiques de routage de Route 53 ?

Simple, pondérée, fondée sur la latence, basculement, géolocalisation, géoproximité, fondée sur l'IP et réponse à valeurs multiples.

#### Qu'est-ce qu'Amazon CloudFront ?

Un réseau de diffusion de contenu qui met en cache le contenu dans des emplacements périphériques proches des utilisateurs, ce qui réduit la latence. Il fonctionne avec des origines comme S3, des équilibreurs de charge ou tout serveur HTTP, prend en charge le HTTPS et s'intègre à WAF et Shield.

#### Qu'est-ce qu'AWS Global Accelerator ?

Un service qui fait passer le trafic des utilisateurs par le réseau mondial d'AWS via deux adresses IP anycast statiques, ce qui améliore les performances et la disponibilité des applications TCP/UDP multirégions. Contrairement à CloudFront, il ne met rien en cache.

#### Qu'est-ce qu'Amazon API Gateway ?

Un service géré pour créer, publier, sécuriser et superviser des API REST, HTTP et WebSocket, souvent devant des fonctions Lambda.

#### Qu'est-ce qu'un bloc CIDR ?

Une notation pour une plage d'adresses IP, comme 10.0.0.0/16, utilisée pour définir l'espace d'adressage d'un VPC et de ses sous-réseaux.

#### Qu'est-ce qu'un hôte bastion ?

Une instance dans un sous-réseau public qui sert de point d'entrée durci pour accéder en SSH ou RDP aux instances de sous-réseaux privés. Systems Manager Session Manager le remplace souvent.

### Gestion, gouvernance et outils de développement

#### Qu'est-ce qu'Amazon CloudWatch ?

Un service de supervision et d'observabilité : métriques, alarmes, journaux (CloudWatch Logs), tableaux de bord et événements, pour les ressources AWS et les applications.

#### Qu'est-ce qu'AWS CloudTrail ?

Un service qui enregistre les appels d'API et l'activité du compte (qui a fait quoi, quand, d'où) pour la gouvernance, la conformité et l'audit. Les journaux peuvent être livrés dans S3 et analysés avec CloudTrail Lake.

#### Quelle est la différence entre CloudWatch et CloudTrail ?

CloudWatch supervise les performances et la santé (métriques, journaux, alarmes). CloudTrail audite les actions (appels d'API effectués dans le compte).

#### Qu'est-ce qu'AWS Config ?

Un service qui enregistre la configuration des ressources et ses changements au fil du temps et l'évalue selon des règles, pour l'audit de conformité et le dépannage.

#### Qu'est-ce qu'AWS Systems Manager ?

Un ensemble d'outils d'exploitation pour gérer à grande échelle des serveurs EC2 et sur site : Session Manager, Patch Manager, Run Command, Parameter Store, Automation et inventaire.

#### Qu'est-ce qu'AWS CloudFormation ?

L'infrastructure as code : on décrit les ressources dans des modèles JSON ou YAML, et CloudFormation les crée, les met à jour et les supprime sous forme de pile, dans le bon ordre.

#### Qu'est-ce que l'AWS Cloud Development Kit (CDK) ?

Un framework pour définir l'infrastructure cloud dans des langages de programmation (TypeScript, Python, Java, C#, Go). Il génère des modèles CloudFormation.

#### Qu'est-ce qu'AWS Trusted Advisor ?

Un service qui inspecte votre compte et recommande des améliorations dans cinq catégories : optimisation des coûts, performances, sécurité, tolérance aux pannes et quotas de service. Les plans de support Basic et Developer n'ont que les contrôles essentiels. Business et au-delà ont l'ensemble complet.

#### Qu'est-ce que l'AWS Health Dashboard ?

Une vue de l'état des services AWS et des événements qui touchent vos propres ressources, comme une maintenance planifiée ou un incident dans vos régions.

#### Quelles sont les façons d'interagir avec AWS ?

L'AWS Management Console (web), l'AWS CLI, les SDK pour les langages de programmation, l'infrastructure as code (CloudFormation, CDK) et AWS CloudShell (un terminal dans le navigateur déjà authentifié).

#### Que sont AWS CodeCommit, CodeBuild, CodeDeploy et CodePipeline ?

Des outils de CI/CD : CodeBuild compile et teste le code, CodeDeploy automatise les déploiements sur EC2, Lambda, ECS et sur site, CodePipeline orchestre les chaînes de livraison. CodeCommit est un service d'hébergement Git fermé aux nouveaux clients.

#### Qu'est-ce qu'AWS X-Ray ?

Un service qui trace les requêtes à travers des applications distribuées pour trouver les goulets d'étranglement et les erreurs.

#### Qu'est-ce qu'Amazon SQS ?

Simple Queue Service est une file de messages entièrement gérée qui découple les composants. Les files standard offrent un débit élevé avec une livraison au moins une fois. Les files FIFO garantissent l'ordre et un traitement exactement une fois.

#### Quelle est la différence entre SQS et SNS ?

SQS est une file : les consommateurs récupèrent les messages, chaque message est traité par un seul consommateur. SNS est de la publication/abonnement : un message publié sur un sujet est poussé à tous les abonnés (SQS, Lambda, HTTP, e-mail, SMS). On les combine souvent en éventail (fan-out).

#### Qu'est-ce qu'Amazon EventBridge ?

Un bus d'événements serverless qui achemine les événements des services AWS, d'applications SaaS et de votre propre code vers des cibles selon des règles, et planifie des tâches (EventBridge Scheduler).

### Facturation, tarification et support

#### Quels sont les trois facteurs fondamentaux du coût sur AWS ?

Le calcul, le stockage et le transfert de données sortant. Le transfert de données entrant est en général gratuit.

#### Qu'est-ce que l'offre gratuite d'AWS (Free Tier) ?

Des offres pour essayer AWS sans frais dans certaines limites. Elle comprend des offres toujours gratuites (par exemple des requêtes Lambda et du stockage DynamoDB jusqu'à un plafond), des crédits ou offres de 12 mois pour les nouveaux comptes selon le plan du compte, et de courts essais gratuits de certains services. L'usage au-delà des limites est facturé.

#### Qu'est-ce que l'AWS Pricing Calculator ?

Un outil gratuit pour estimer le coût d'une architecture avant de la construire.

#### Qu'est-ce qu'AWS Cost Explorer ?

Un outil pour visualiser, analyser et prévoir les coûts et l'usage dans le temps, avec des filtres par service, compte ou balise, et des recommandations de Savings Plans et de redimensionnement.

#### Qu'est-ce qu'AWS Budgets ?

Un service pour définir des budgets de coût, d'usage ou de réservations et recevoir des alertes (ou déclencher des actions) quand la dépense réelle ou prévue dépasse un seuil.

#### Qu'est-ce que l'AWS Cost and Usage Report, désormais Data Exports ?

Les données de facturation les plus détaillées, livrées dans S3 à la granularité horaire ou quotidienne, pour les analyser avec Athena, QuickSight ou d'autres outils.

#### Que sont les balises de répartition des coûts ?

Des balises (paires clé-valeur comme `project=lakehouse`) activées dans la console de facturation pour regrouper et filtrer les coûts par balise dans Cost Explorer et les rapports.

#### Qu'est-ce que la facturation consolidée d'AWS Organizations ?

Une seule facture pour tous les comptes d'une organisation, payée par le compte de gestion. L'usage est cumulé pour les remises sur volume, et les remises des instances réservées et des Savings Plans peuvent être partagées entre comptes.

#### Qu'est-ce qu'AWS Compute Optimizer ?

Un service qui applique l'apprentissage automatique aux métriques d'utilisation pour recommander les types d'instances EC2, groupes Auto Scaling, volumes EBS, fonctions Lambda et configurations ECS sur Fargate optimaux.

#### Quels sont les plans AWS Support ?

- **Basic :** gratuit. Documentation, forums, AWS re:Post, Health Dashboard et contrôles essentiels de Trusted Advisor.
- **Developer :** accès par e-mail aux ingénieurs du support aux heures ouvrées, pour les tests et le développement.
- **Business :** support 24 h/24 et 7 j/7 par téléphone, chat et e-mail, Trusted Advisor complet, réponse rapide si un système de production est en panne.
- **Enterprise On-Ramp :** ajoute un pool de Technical Account Managers et une réponse plus rapide pour les systèmes critiques.
- **Enterprise :** un Technical Account Manager dédié, la réponse la plus rapide en cas de panne d'un système critique et un service de conciergerie pour la facturation.

Vérifiez la page AWS Support pour les noms et délais de réponse actuels, qu'AWS révise régulièrement.

#### Qu'est-ce qu'un Technical Account Manager (TAM) ?

Un interlocuteur technique AWS dédié aux clients Enterprise, qui apporte des conseils proactifs sur l'architecture, l'exploitation et les bonnes pratiques.

#### Qu'est-ce qu'AWS re:Post ?

Un site communautaire de questions-réponses, modéré avec des experts AWS, qui a remplacé les forums AWS.

#### Qu'est-ce qu'AWS Marketplace ?

Un catalogue numérique sélectionné de logiciels, données et services tiers fonctionnant sur AWS, achetables et facturés via votre compte AWS.

#### Que sont AWS Professional Services et l'AWS Partner Network ?

AWS Professional Services est l'équipe de conseil d'AWS. L'AWS Partner Network (APN) est la communauté mondiale de partenaires conseil et technologiques qui aident les clients à construire sur AWS.

#### Comment réduire ses coûts sur AWS ?

Redimensionner les instances, éteindre les ressources inutilisées, utiliser des Savings Plans ou des instances réservées pour les charges stables et Spot pour les charges interruptibles, choisir des classes de stockage moins chères avec des règles de cycle de vie, passer au serverless pour les charges variables, réduire le transfert de données (par exemple avec CloudFront et les points de terminaison de VPC), et suivre les dépenses avec des balises, Budgets et Cost Explorer.
