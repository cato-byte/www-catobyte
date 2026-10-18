## Fiche d'étude AWS Certified Cloud Practitioner

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude AWS Certified Cloud Practitioner : environ 200 questions](../../images/aws_practicioner_guide_title_img.png)

Environ 200 questions avec des réponses courtes, que j'ai utilisées pour préparer l'examen AWS Certified Cloud Practitioner (CLF-C02), obtenu en octobre 2026. Elles suivent les quatre domaines de l'examen : concepts du cloud, sécurité et conformité, technologies et services cloud, et facturation, tarification et support.

La fiche suit un parcours d'apprentissage en quatre étapes. Chaque section est découpée en unités courtes : objectifs d'apprentissage, explication du concept et exemple commenté, puis questions (d'abord de mémorisation, ensuite d'application), un exercice pratique et les points à retenir. Pour **apprendre**, lisez chaque unité du début à la fin. Pour **réviser**, passez en mode révision ou utilisez « Aller aux questions », marquez les réponses à revoir et essayez une révision mixte entre les sections. Les services et les prix évoluent : vérifiez la documentation AWS avant de vous fier à un chiffre.

<!-- QA -->
<!-- stage: Fondamentaux du cloud -->

### Concepts du cloud

<!-- unit: Pourquoi le cloud -->

<!-- goals -->

- Expliquer l'argument économique du cloud computing.
- Relier les six avantages d'AWS à des bénéfices métier concrets.

<!-- concept -->

Gérer son propre centre de données, c'est acheter pour le pic attendu dans plusieurs années, puis payer de la capacité inutilisée jusqu'à l'atteindre. Le cloud inverse cela : on loue de la capacité à la seconde à un fournisseur dont l'échelle rend chaque unité moins chère que ce qu'on pourrait acheter. L'argent passe de l'investissement initial à la dépense d'exploitation.

La vitesse découle du même changement. Quand un serveur est à un appel d'API, tester une idée coûte quelques minutes, et ouvrir un autre continent devient un changement de configuration, pas un chantier.

<!-- example -->

| Question | Sur site | AWS |
|---|---|---|
| Capacité pour le Black Friday | Acheter des serveurs pour le pic | Monter en charge pour la semaine |
| Nouvelle région pour les clients UE | Louer de l'espace, expédier du matériel | Déployer dans eu-west-3 |
| Modèle de coût | CapEx d'avance | OpEx, paiement à l'usage |

#### Qu'est-ce que le cloud computing ?

La fourniture à la demande de ressources informatiques (calcul, stockage, bases de données, réseau, logiciels) via internet, avec une facturation à l'usage. Au lieu d'acheter et d'exploiter des centres de données, on loue de la capacité à un fournisseur et on la libère quand on n'en a plus besoin.

#### Quels sont les six avantages du cloud computing selon AWS ?

1. Remplacer des dépenses fixes (investissement) par des dépenses variables.
2. Profiter d'énormes économies d'échelle.
3. Ne plus deviner la capacité nécessaire.
4. Gagner en rapidité et en agilité.
5. Ne plus dépenser d'argent pour exploiter et entretenir des centres de données.
6. Se déployer dans le monde entier en quelques minutes.

#### Quels sont les avantages d'AWS par rapport à une infrastructure sur site ?

Pas d'achat initial de matériel, on ne paie que ce qu'on utilise, de la capacité en minutes au lieu de mois, une portée mondiale, des services gérés qui suppriment le travail sans valeur ajoutée (correctifs, sauvegardes), sécurité et certifications de conformité intégrées, et la possibilité d'expérimenter à moindre coût et d'arrêter ce qui échoue.

#### Quelle est la différence entre CapEx et OpEx ?

Les dépenses d'investissement (CapEx) sont un investissement initial dans des actifs physiques, comme des serveurs, amortis sur plusieurs années. Les dépenses d'exploitation (OpEx) sont des dépenses courantes en services. Le cloud transforme l'essentiel du CapEx informatique en OpEx.

#### Que signifie « économies d'échelle » dans le cloud ?

AWS achète du matériel, de l'énergie et du réseau à une échelle qu'aucun client n'atteint seul, donc son coût unitaire est plus bas. Une partie de l'économie est répercutée par des baisses de prix, qu'AWS a appliquées de nombreuses fois.

#### Qu'est-ce que l'agilité dans le contexte du cloud ?

La vitesse à laquelle on peut obtenir des ressources et tester de nouvelles idées. Des ressources qui prenaient des semaines à arriver sont disponibles en minutes : le coût et le délai d'une expérimentation chutent fortement.

#### Que signifie « se déployer dans le monde entier en quelques minutes » ?

Qu'on peut déployer une application dans des régions AWS du monde entier en quelques clics ou appels d'API, et offrir une latence plus faible aux utilisateurs sans construire de centres de données dans d'autres pays.

<!-- challenge -->

Le DAF d'une startup demande pourquoi ne pas acheter des serveurs, puisque « louer revient toujours plus cher à la fin ». Donnez deux arguments simples.

<!-- solution -->

Ils paieraient d'avance une capacité qu'ils n'utiliseront peut-être jamais, et se tromper dans un sens ou dans l'autre coûte cher. Avec AWS, ils paient ce qu'ils utilisent, suivent la demande et gardent leur trésorerie ; les savings plans baissent encore les prix quand l'usage devient prévisible.

<!-- takeaways -->

- Le cloud échange un CapEx initial contre un OpEx variable.
- Les économies d'échelle baissent les prix unitaires d'AWS.
- Agilité : ressources en minutes, régions partout dans le monde.

<!-- unit: Modèles de service et de déploiement -->

<!-- goals -->

- Distinguer IaaS, PaaS et SaaS avec des exemples AWS.
- Comparer déploiements cloud, hybrides et sur site.

<!-- concept -->

Les services cloud diffèrent par ce qu'AWS gère pour vous. Avec des services d'infrastructure, vous recevez des machines virtuelles et gérez tout ce qui tourne dessus. Avec des services de plateforme, vous apportez le code et AWS gère les serveurs. Avec le logiciel en service, vous utilisez simplement l'application. Les services managés et serverless sont du côté plateforme : moins à exploiter, moins à contrôler.

Les modèles de déploiement répondent à une autre question : où tournent les choses. Beaucoup d'entreprises combinent cloud et sur site pendant des années de migration.

<!-- example -->

| Vous gérez | IaaS (EC2) | PaaS (Elastic Beanstalk) | SaaS |
|---|---|---|---|
| Code de l'application | Oui | Oui | Non |
| Correctifs du système | Oui | Non | Non |
| Matériel | Non | Non | Non |

#### Quels modèles de déploiement du cloud AWS prend-il en charge ?

- **Cloud (cloud natif) :** tout tourne dans le cloud public.
- **Sur site (cloud privé) :** des ressources dans votre propre centre de données, souvent avec de la virtualisation et des outils de gestion. AWS Outposts apporte l'infrastructure AWS sur site.
- **Hybride :** des ressources cloud reliées à une infrastructure sur site, par exemple pendant une migration ou pour des données qui doivent rester sur place.

#### Que signifient IaaS, PaaS et SaaS ? Donnez des exemples AWS.

- **IaaS (infrastructure en tant que service) :** vous obtenez des machines virtuelles, du stockage et des réseaux, et gérez le système d'exploitation et tout ce qui est au-dessus. Exemple : Amazon EC2.
- **PaaS (plateforme en tant que service) :** le fournisseur gère l'infrastructure et la plateforme, vous déployez du code. Exemple : AWS Elastic Beanstalk.
- **SaaS (logiciel en tant que service) :** une application complète utilisée via internet. Exemples : Amazon WorkMail, Amazon Chime, Amazon QuickSight.

#### Qu'est-ce qu'un service géré ?

Un service dont AWS exploite l'infrastructure et les logiciels sous-jacents (provisionnement, correctifs, sauvegardes, montée en charge), et que vous vous contentez d'utiliser. Amazon RDS est une base de données gérée. Faire tourner une base de données sur EC2 ne l'est pas : tout cela est à votre charge.

#### Que signifie « serverless » ?

Exécuter du code ou utiliser un service sans provisionner ni gérer de serveurs. La capacité s'ajuste automatiquement et on paie l'usage réel. Exemples : AWS Lambda, Amazon S3, Amazon DynamoDB, AWS Fargate, Amazon Athena.

<!-- challenge -->

Une équipe fait tourner PostgreSQL sur EC2 et passe des heures sur les correctifs et sauvegardes. Quel changement de modèle aiderait, et à quoi renoncent-ils ?

<!-- solution -->

Passer à une base managée (Amazon RDS for PostgreSQL), où AWS gère correctifs, sauvegardes et basculement. Ils renoncent à l'accès au système d'exploitation et à une partie des réglages bas niveau.

<!-- takeaways -->

- IaaS, PaaS et SaaS diffèrent par ce que vous gérez.
- Les services managés et serverless transfèrent l'exploitation à AWS.
- L'hybride combine cloud et sur site.

<!-- unit: Élasticité et passage à l'échelle -->

<!-- goals -->

- Distinguer élasticité et scalabilité.
- Choisir entre montée en charge verticale et horizontale.

<!-- concept -->

La scalabilité est la capacité à absorber plus de charge en ajoutant des ressources. L'élasticité ajoute une dimension temporelle : les ressources grandissent et rétrécissent automatiquement avec la demande, pour ne pas payer le pic toute l'année.

La façon de monter en charge compte. Une plus grosse machine est simple mais plafonne et reste un point unique de défaillance. Davantage de machines derrière un répartiteur vont plus loin et survivent aux pannes, mais l'application doit permettre à toute instance de servir toute requête.

<!-- example -->

```text
Vertical:   t3.large ─► m7i.2xlarge         (bigger box, restart, limit)
Horizontal: 2 × m7i.large ─► 8 × m7i.large  (more boxes, load balancer, no limit)
```

#### Qu'est-ce que l'élasticité ?

La capacité d'obtenir des ressources quand on en a besoin et de les libérer quand on n'en a plus besoin, automatiquement, en suivant la demande. Exemple : un groupe Auto Scaling qui ajoute des instances EC2 pendant un pic de trafic et les retire ensuite.

#### Qu'est-ce que la scalabilité ?

La capacité d'un système à absorber une charge croissante en ajoutant des ressources. Le scaling vertical consiste à prendre des ressources plus grosses, le scaling horizontal à en ajouter davantage. L'élasticité est une scalabilité qui redescend aussi automatiquement.

#### Quelle est la différence entre scaling vertical et horizontal ?

Le scaling vertical remplace une ressource par une plus grosse (un type d'instance plus grand). C'est simple, mais il y a un plafond et souvent un redémarrage. Le scaling horizontal ajoute des ressources de même taille derrière un équilibreur de charge. Il n'a pas de limite pratique et améliore la disponibilité.

<!-- challenge -->

Le trafic d'une boutique en ligne triple chaque soir et chute la nuit. Quelle approche suggérez-vous ?

<!-- solution -->

Une montée en charge horizontale avec EC2 Auto Scaling derrière un répartiteur : ajouter des instances le soir, les retirer la nuit. C'est l'élasticité : on ne paie la capacité de pointe que lorsqu'elle sert.

<!-- takeaways -->

- La scalabilité absorbe la croissance ; l'élasticité suit la demande.
- Le vertical est simple mais limité ; l'horizontal va plus loin.
- Les conceptions élastiques évitent de payer une pointe inutilisée.

<!-- unit: Disponibilité et reprise -->

<!-- goals -->

- Définir haute disponibilité, tolérance aux pannes et reprise après sinistre.
- Choisir une stratégie de reprise selon le RTO et le RPO.

<!-- concept -->

Les pannes sont certaines ; la question est leur coût. La haute disponibilité raccourcit l'interruption quand des composants tombent ; la tolérance aux pannes maintient le service sans aucune interruption, plus cher. La reprise après sinistre couvre les gros événements, comme la perte d'une région entière.

Deux nombres encadrent chaque choix : combien de temps on peut être arrêté (RTO) et combien de données on peut perdre (RPO). Plus ils sont bas, plus il faut de ressources en attente, donc le coût monte.

<!-- example -->

| Stratégie | RTO / RPO | Coût |
|---|---|---|
| Sauvegarde et restauration | Heures / heures | $ |
| Pilot light | Dizaines de minutes | $$ |
| Warm standby | Minutes | $$$ |
| Multi-site actif/actif | Proche de zéro | $$$$ |

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

<!-- challenge -->

Un système de paie peut être arrêté 8 heures et perdre au plus 1 heure de données. Quelle stratégie convient, et pourquoi pas une plus chère ?

<!-- solution -->

Sauvegarde et restauration avec des sauvegardes horaires (ou pilot light si les restaurations sont longues) respecte un RTO de 8 heures et un RPO d'1 heure. Warm standby ou multi-site coûteraient bien plus pour une vitesse de reprise inutile au métier.

<!-- takeaways -->

- La haute disponibilité limite l'arrêt ; la tolérance aux pannes l'évite.
- Le RTO est le délai de reprise ; le RPO, la perte de données acceptable.
- Une reprise plus rapide exige plus de ressources en attente.

<!-- unit: Planifier une migration -->

<!-- goals -->

- Décrire l'AWS Cloud Adoption Framework.
- Choisir une stratégie de migration parmi les 7 R.

<!-- concept -->

Passer au cloud est autant un changement organisationnel que technique. Le Cloud Adoption Framework structure le travail en perspectives, du métier et des personnes à la sécurité et l'exploitation, pour que compétences et processus évoluent avec les serveurs.

Pour chaque application, les 7 R donnent les options, de la laisser en l'état à la réécrire. La plupart des entreprises en combinent plusieurs : un rehost rapide pour quitter un centre de données, puis un refactoring là où les fonctions cloud rapportent.

<!-- example -->

| Application | Stratégie |
|---|---|
| Vieil outil de reporting que personne n'utilise | Retire |
| ERP avec une contrainte de licence forte | Retain (pour l'instant) |
| Application web sur VM | Rehost vers EC2 |
| MySQL autogéré | Replatform vers RDS |
| Monolithe qui doit monter en charge | Refactor |

#### Qu'est-ce que l'AWS Cloud Adoption Framework (AWS CAF) ?

Un guide qui aide les organisations à planifier leur transformation vers le cloud. Il regroupe les capacités en six perspectives : Métier, Personnes, Gouvernance (orientées métier) et Plateforme, Sécurité, Opérations (techniques).

#### Que sont les 7 R de la migration ?

Retirer (Retire), Conserver (Retain), Réhéberger (Rehost, « lift and shift »), Relocaliser (Relocate, par exemple VMware Cloud on AWS), Racheter (Repurchase, passer au SaaS), Changer de plateforme (Replatform, « lift, tinker and shift », comme passer à RDS) et Refactoriser ou réarchitecturer (Refactor, reconstruire en natif cloud).

<!-- challenge -->

Une entreprise doit quitter son centre de données dans 6 mois et compte 300 applications. Quelle stratégie pour la plupart, et ensuite ?

<!-- solution -->

Un rehost pour la plupart (lift and shift), le plus rapide, et retire ou retain pour le reste. Après la sortie, refactor ou replatform pour les applications où services managés ou montée en charge apportent un vrai gain.

<!-- takeaways -->

- Le CAF couvre métier, personnes, gouvernance, plateforme, sécurité, exploitation.
- Les 7 R vont de retire à refactor.
- Rehost d'abord, optimiser ensuite : un chemin courant.

### Infrastructure mondiale et Well-Architected Framework

<!-- unit: Régions et zones de disponibilité -->

<!-- goals -->

- Décrire régions, zones de disponibilité et services globaux ou régionaux.
- Choisir une région selon conformité, latence, services et prix.

<!-- concept -->

AWS construit son infrastructure en couches d'isolation. Une région est une zone géographique ; à l'intérieur, les zones de disponibilité sont des centres de données séparés, avec leur propre alimentation et réseau, assez proches pour des liaisons rapides mais assez éloignés pour qu'un événement ne les touche pas tous.

Cette organisation guide la conception : répartir sur plusieurs zones protège d'une panne de centre de données, sur plusieurs régions d'un événement régional. Le choix de la région commence par les exigences légales, puis latence, disponibilité des services et prix.

<!-- example -->

```text
Region eu-west-3 (Paris)
 ├─ AZ eu-west-3a ── app + DB primary
 ├─ AZ eu-west-3b ── app + DB standby
 └─ AZ eu-west-3c ── app
```

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

#### Les services sont-ils mondiaux ou régionaux ?

La plupart sont régionaux : les ressources vivent dans une région. Quelques-uns sont mondiaux : IAM, Route 53, CloudFront, AWS Organizations et WAF pour CloudFront. D'autres, comme les sous-réseaux EC2 et les volumes EBS, sont limités à une zone de disponibilité.

<!-- challenge -->

Une entreprise de santé française veut une faible latence pour ses utilisateurs français et doit garder les données patients en France. Quelle région et quelle organisation proposez-vous ?

<!-- solution -->

Paris (eu-west-3), qui respecte la résidence des données, avec l'application et la base réparties sur au moins deux zones de disponibilité pour la haute disponibilité. Vérifiez que les services nécessaires y sont disponibles.

<!-- takeaways -->

- Les régions contiennent plusieurs zones de disponibilité isolées.
- Répartissez sur les zones pour la disponibilité, sur les régions contre les sinistres.
- La conformité passe en premier dans le choix de région.

<!-- unit: Infrastructure en périphérie et sur site -->

<!-- goals -->

- Expliquer edge locations, Local Zones, Wavelength et Outposts.
- Associer chacun à un besoin de latence ou de localisation.

<!-- concept -->

Tout ne peut pas tourner dans une région. Contenus et réponses DNS sont plus rapides depuis des edge locations proches des utilisateurs. Certaines applications exigent une latence de quelques millisecondes vers une ville ou un réseau 5G, que fournissent Local Zones et Wavelength. D'autres doivent rester dans vos locaux pour des raisons réglementaires ou de latence : Outposts y apporte du matériel AWS.

Chaque option étend les mêmes services et API AWS à un nouvel endroit.

<!-- example -->

| Besoin | Option |
|---|---|
| Mettre en cache des images près des utilisateurs du monde entier | Edge locations (CloudFront) |
| Montage vidéo près de Los Angeles | Local Zone |
| Jeu mobile sur 5G | Wavelength |
| Systèmes d'usine sur place | Outposts |

#### Qu'est-ce qu'un emplacement périphérique (edge location) ?

Un site qui fait tourner les caches CloudFront et le DNS Route 53 (et des services comme Lambda@Edge) près des utilisateurs finaux. Il y a beaucoup plus d'emplacements périphériques que de régions.

#### Qu'est-ce qu'une Local Zone ?

Une extension d'une région placée près d'une grande ville, qui fait tourner certains services (comme EC2 et EBS) pour offrir une latence de quelques millisecondes aux utilisateurs locaux.

#### Qu'est-ce qu'AWS Wavelength ?

Une infrastructure intégrée aux réseaux 5G des opérateurs télécoms, pour que les applications atteignent les appareils mobiles avec une latence très faible.

#### Qu'est-ce qu'AWS Outposts ?

Des baies de matériel gérées par AWS installées dans votre propre centre de données, qui font tourner des services AWS avec les mêmes API et outils. Utilisé pour une faible latence avec des systèmes sur site, le traitement local des données ou la résidence des données.

<!-- challenge -->

Une banque doit garder un système de trading dans son propre centre de données mais veut les API et outils AWS. Quel service convient ?

<!-- solution -->

AWS Outposts : des racks gérés par AWS installés sur site, qui exécutent des services AWS avec les mêmes API, reliés à une région parente.

<!-- takeaways -->

- Les edge locations servent CloudFront et Route 53 près des utilisateurs.
- Local Zones et Wavelength rapprochent le calcul des villes et de la 5G.
- Outposts exécute AWS dans votre centre de données.

<!-- unit: Les piliers Well-Architected -->

<!-- goals -->

- Nommer les six piliers du Well-Architected Framework.
- Résumer ce que chaque pilier exige d'une charge de travail.

<!-- concept -->

Le Well-Architected Framework est une façon structurée de se demander si une charge est bien construite. Il découpe « bien » en six préoccupations souvent contradictoires : l'exploiter sereinement, la sécuriser, la rendre fiable, utiliser les ressources efficacement, dépenser judicieusement et réduire l'impact environnemental.

Leur valeur tient aux arbitrages. Une revue par piliers les rend explicites, par exemple payer plus pour une fiabilité multi-AZ ou accepter moins de performance pour un coût plus bas.

<!-- example -->

| Pilier | Question type |
|---|---|
| Excellence opérationnelle | Comment déployez-vous et tirez-vous les leçons des incidents ? |
| Sécurité | Comment gérez-vous les identités et protégez-vous les données ? |
| Fiabilité | Comment la charge se rétablit-elle après une panne ? |
| Efficacité des performances | Comment choisissez-vous les bonnes ressources ? |
| Optimisation des coûts | Comment savez-vous ce que vous dépensez et pourquoi ? |
| Durabilité | Comment réduisez-vous l'usage des ressources ? |

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

<!-- challenge -->

Une équipe fait tourner sa base de production sur une seule instance sans sauvegarde pour économiser. Quels piliers néglige-t-elle, et quelle est la correction la moins chère ?

<!-- solution -->

Surtout la Fiabilité (point unique de défaillance, aucune reprise) au profit de l'Optimisation des coûts. La correction la moins chère : des sauvegardes automatiques avec restauration à un instant donné ; le Multi-AZ ajoute la disponibilité pour plus cher.

<!-- takeaways -->

- Six piliers : exploitation, sécurité, fiabilité, performance, coût, durabilité.
- Les piliers s'opposent souvent.
- Les revues rendent ces arbitrages explicites.

<!-- unit: Principes de conception -->

<!-- goals -->

- Appliquer « concevoir pour la panne », le couplage faible et les applications sans état.
- Expliquer pourquoi l'infrastructure as code est recommandée.

<!-- concept -->

Quelques principes reviennent dans tous les piliers. Attendez-vous à ce que tout composant tombe, et construisez redondance et reprise automatique. Reliez les composants par des files et des événements pour qu'une partie lente ne bloque pas les autres. Gardez les serveurs d'application sans état pour pouvoir remplacer n'importe lequel.

L'infrastructure as code rend tout cela reproductible : les environnements deviennent des modèles relus et versionnés, et reconstruire après une panne revient à relancer le modèle.

<!-- example -->

```text
Tightly coupled:  web ─► order service ─► payment API (down → orders fail)
Loosely coupled:  web ─► SQS queue ─► order workers ─► payment API (down → orders wait)
```

#### Que signifie « concevoir pour la panne » ?

Partir du principe que tout composant peut tomber en panne, et construire le système pour qu'il continue de fonctionner quand cela arrive : plusieurs AZ, contrôles de santé, remplacement automatique, nouvelles tentatives et composants découplés.

#### Qu'est-ce que le couplage faible, et quels services aident à l'obtenir ?

Concevoir les composants de sorte qu'une panne ou un ralentissement de l'un ne se propage pas aux autres. Les files d'attente (Amazon SQS), les notifications (Amazon SNS), les bus d'événements (Amazon EventBridge) et les équilibreurs de charge permettent aux composants de communiquer sans dépendre directement les uns des autres.

#### Quelle est la différence entre une application sans état et avec état ?

Un composant sans état ne garde aucune donnée de session entre deux requêtes : n'importe quelle instance peut traiter n'importe quelle requête, et on peut ajouter ou retirer des instances librement. L'état est stocké ailleurs (DynamoDB, ElastiCache, S3). Les composants avec état sont plus difficiles à faire monter en charge horizontalement.

#### Qu'est-ce que l'infrastructure as code, et pourquoi le Well-Architected Framework la recommande-t-il ?

Définir l'infrastructure dans des modèles ou du code versionnés (CloudFormation, AWS CDK) plutôt que par des clics manuels dans la console. Les environnements deviennent reproductibles, relisibles et rapides à reconstruire, ce qui sert l'excellence opérationnelle et la fiabilité.

<!-- challenge -->

Les utilisateurs sont déconnectés chaque fois qu'Auto Scaling retire une instance. Quelle est la cause, et la correction ?

<!-- solution -->

Les sessions sont stockées sur les instances : l'application a un état. Déplacez les données de session vers un stockage partagé (ElastiCache ou DynamoDB) pour que toute instance serve tout utilisateur.

<!-- takeaways -->

- Concevoir pour la panne : redondance et reprise automatique.
- Files et événements découplent les composants.
- Serveurs sans état et IaC facilitent les remplacements.

<!-- stage: Sécurité -->

### Sécurité, modèle de responsabilité partagée et IAM

<!-- unit: Responsabilité partagée -->

<!-- goals -->

- Expliquer ce que sécurise AWS et ce que sécurise le client.
- Montrer comment les responsabilités évoluent entre EC2, RDS et S3.

<!-- concept -->

La sécurité sur AWS se partage selon une ligne. AWS sécurise le cloud lui-même : bâtiments, matériel, couche de virtualisation, rouages des services managés. Vous sécurisez ce que vous y mettez : données, identités, configuration et tout ce que vous installez.

L'emplacement de la ligne dépend du service. Plus AWS gère, moins vous en faites, mais données, accès et configuration restent toujours à vous.

<!-- example -->

| Tâche | EC2 | RDS | S3 |
|---|---|---|---|
| Sécurité physique | AWS | AWS | AWS |
| Correctifs du système | Client | AWS | AWS |
| Correctifs du moteur de base | Client | AWS | n/a |
| Données, politiques d'accès, réglages de chiffrement | Client | Client | Client |

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

<!-- challenge -->

Un bucket S3 d'une entreprise est devenu public par erreur et des données ont fuité. Selon le modèle de responsabilité partagée, à qui la faute, et quel contrôle l'aurait évité ?

<!-- solution -->

Au client : la configuration d'accès du bucket relève de sa responsabilité. S3 Block Public Access au niveau du compte (plus des SCP dans Organizations et des règles Config) aurait empêché les buckets de devenir publics.

<!-- takeaways -->

- AWS sécurise « le » cloud ; vous sécurisez ce qui est « dans » le cloud.
- Plus un service est managé, plus AWS en fait.
- Données, identités et configuration restent toujours à vous.

<!-- unit: Utilisateur root et identités IAM -->

<!-- goals -->

- Protéger l'utilisateur root et connaître ses tâches exclusives.
- Choisir entre utilisateurs, groupes et rôles IAM.

<!-- concept -->

Chaque compte démarre avec un utilisateur root qui peut tout faire, y compris fermer le compte. Comme on ne peut pas le limiter, il doit être mis sous clé avec MFA et réservé aux rares tâches qui l'exigent.

L'accès quotidien passe par IAM. Les utilisateurs représentent des personnes ou applications avec des identifiants de longue durée ; les groupes rendent les permissions gérables ; les rôles fournissent des identifiants temporaires à qui est autorisé à les endosser. Les rôles sont le choix le plus sûr, surtout pour les applications.

<!-- example -->

```text
root user        ─► MFA, no access keys, used only for root-only tasks
group: analysts  ─► policy AnalystsReadOnly ◄─ users ana, luis
role: ec2-app    ─► policy AppS3Access      ◄─ assumed by EC2 instances
```

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

<!-- challenge -->

Un développeur stocke des clés d'accès dans un fichier de configuration sur une instance EC2 pour que l'application lise S3. Que recommandez-vous ?

<!-- solution -->

Créer un rôle IAM avec lecture sur le bucket nécessaire, l'attacher à l'instance via un instance profile, retirer les clés du fichier et les désactiver. L'application reçoit automatiquement des identifiants temporaires renouvelés.

<!-- takeaways -->

- Protégez le root avec MFA ; ne l'utilisez pas au quotidien.
- Les groupes gèrent les permissions ; les rôles donnent des identifiants temporaires.
- Les applications sur AWS doivent utiliser des rôles, pas des clés.

<!-- unit: Politiques et évaluation des permissions -->

<!-- goals -->

- Lire une instruction de politique IAM et ses parties.
- Prédire le résultat quand des politiques autorisent et refusent.

<!-- concept -->

Les permissions AWS s'écrivent en politiques JSON qui autorisent ou refusent des actions sur des ressources, éventuellement sous conditions. Les ressources sont désignées par des ARN, ce qui permet à une politique de viser un seul bucket ou une seule table.

L'évaluation suit une règle simple : tout est refusé par défaut, un allow ouvre l'accès et un deny explicite l'emporte toujours. Le moindre privilège consiste à écrire des allow aussi étroits que la tâche l'exige et à ne les élargir qu'en cas de besoin.

<!-- example -->

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject"],
    "Resource": "arn:aws:s3:::sales-reports/*",
    "Condition": {"Bool": {"aws:SecureTransport": "true"}}
  }]
}
```

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

#### Qu'est-ce qu'un ARN ?

Un Amazon Resource Name identifie une ressource de façon unique : `arn:partition:service:region:account-id:resource`, par exemple `arn:aws:s3:::my-bucket`.

<!-- challenge -->

Un utilisateur a une politique de groupe qui autorise `s3:*` sur tous les buckets et une politique personnelle qui refuse `s3:DeleteObject` sur `finance-*`. Peut-il supprimer des objets dans `finance-2026` ?

<!-- solution -->

Non. Le deny explicite l'emporte sur tout allow : les suppressions dans les buckets correspondant à `finance-*` sont refusées, les autres actions S3 restant autorisées.

<!-- takeaways -->

- Les politiques autorisent ou refusent des actions sur des ressources, avec conditions.
- Refus par défaut ; allow accorde ; deny explicite gagne toujours.
- Moindre privilège : commencer étroit, élargir si besoin.

<!-- unit: Identifiants et hygiène du compte -->

<!-- goals -->

- Sécuriser la connexion avec MFA et politiques de mot de passe.
- Auditer les identifiants et les permissions inutilisées.

<!-- concept -->

La plupart des compromissions de comptes commencent par un identifiant volé. Le MFA rend un mot de passe volé insuffisant, les politiques de mot de passe raréfient les mots de passe faibles, et les clés d'accès, qui n'expirent jamais d'elles-mêmes, doivent être peu nombreuses et renouvelées.

L'hygiène, c'est aussi regarder en arrière : qui a encore de vieilles clés, qui a des permissions jamais utilisées. Le credential report et Access Advisor répondent à ces questions pour retirer le superflu.

<!-- example -->

```bash
aws iam generate-credential-report
aws iam get-credential-report --query Content --output text | base64 -d \
  | cut -d, -f1,4,9,11 | column -t -s,      # user, password, key 1 active, key 1 last rotated
```

#### Qu'est-ce que l'authentification multifacteur (MFA), et quels appareils AWS prend-il en charge ?

Un second facteur en plus du mot de passe. AWS prend en charge les clés d'accès (passkeys) et les clés de sécurité FIDO2, les applications d'authentification virtuelles et les jetons TOTP matériels.

#### Que sont les clés d'accès ?

Une paire formée d'un ID de clé d'accès et d'une clé d'accès secrète, utilisée pour signer les requêtes programmatiques (CLI, SDK). Ce sont des identifiants de longue durée : ne les mettez jamais dans le code, renouvelez-les, et préférez les rôles ou IAM Identity Center quand c'est possible.

#### Qu'est-ce qu'une politique de mots de passe dans IAM ?

Des règles du compte pour les mots de passe des utilisateurs IAM : longueur minimale, types de caractères obligatoires, expiration, interdiction de réutilisation.

#### Qu'est-ce que le rapport d'identifiants IAM ?

Un CSV au niveau du compte qui liste tous les utilisateurs et l'état de leurs identifiants : mots de passe, clés d'accès, MFA, dates de dernière utilisation. Utile pour les audits.

#### Qu'est-ce qu'IAM Access Advisor ?

Une vue qui montre à quels services un utilisateur, un groupe ou un rôle a accès et quand il les a utilisés pour la dernière fois. Elle aide à retirer les permissions inutilisées.

<!-- challenge -->

Un audit trouve un utilisateur administrateur qui ne s'est pas connecté depuis un an mais a une clé d'accès active. Que faites-vous ?

<!-- solution -->

Vérifier la dernière utilisation de la clé ; la désactiver, puis supprimer clé et utilisateur s'il n'est plus nécessaire. Utiliser Access Advisor sur les identités restantes pour retirer les permissions inutilisées.

<!-- takeaways -->

- Le MFA bloque la plupart des compromissions par mot de passe.
- Les clés d'accès n'expirent pas ; limitez-les et renouvelez-les.
- Credential reports et Access Advisor montrent quoi retirer.

<!-- unit: Fédération et identifiants temporaires -->

<!-- goals -->

- Donner accès au personnel via IAM Identity Center et la fédération.
- Expliquer comment STS délivre des identifiants temporaires.

<!-- concept -->

Dans les entreprises aux nombreux comptes et collaborateurs, créer des utilisateurs IAM partout ne passe pas à l'échelle et laisse des identifiants traîner après les départs. La fédération permet de se connecter avec l'identité de l'entreprise, et IAM Identity Center la relie à des permission sets sur plusieurs comptes.

En dessous, STS délivre des identifiants de courte durée chaque fois qu'un rôle est endossé. Les identifiants temporaires expirent d'eux-mêmes, d'où leur sécurité supérieure aux clés de longue durée.

<!-- example -->

```bash
aws sso login --profile data-dev                  # corporate sign-in via Identity Center
aws sts get-caller-identity --profile data-dev    # temporary role credentials
```

#### Qu'est-ce qu'AWS IAM Identity Center ?

Le successeur d'AWS Single Sign-On. Il gère de façon centralisée l'accès des collaborateurs à plusieurs comptes AWS et applications métier, avec son propre annuaire ou un fournisseur d'identité externe (Microsoft Entra ID, Okta, Active Directory).

#### Qu'est-ce que la fédération d'identités ?

Permettre aux utilisateurs de se connecter avec une identité existante (annuaire d'entreprise, fournisseur SAML 2.0 ou OIDC) et de recevoir des identifiants AWS temporaires, sans créer d'utilisateurs IAM pour eux.

#### Qu'est-ce qu'AWS STS ?

AWS Security Token Service délivre des identifiants temporaires aux privilèges limités, par exemple quand un rôle est assumé ou qu'un utilisateur fédéré se connecte.

<!-- challenge -->

Une entreprise de 20 comptes AWS crée des utilisateurs IAM dans chacun pour 150 salariés. Que proposez-vous ?

<!-- solution -->

Connecter le fournisseur d'identité de l'entreprise à IAM Identity Center, définir des permission sets par métier et affecter des groupes aux comptes. Puis supprimer les utilisateurs IAM par compte et leurs clés.

<!-- takeaways -->

- Identity Center centralise l'accès du personnel sur tous les comptes.
- La fédération réutilise les identités de l'entreprise.
- Les identifiants STS expirent d'eux-mêmes.

### Services de sécurité et conformité

<!-- unit: Gouvernance multi-comptes -->

<!-- goals -->

- Organiser les comptes avec AWS Organizations et des OU.
- Poser des garde-fous avec les SCP et Control Tower.

<!-- concept -->

Les entreprises utilisent de nombreux comptes pour séparer équipes, environnements et risques. Les gérer un par un ne passe pas à l'échelle : Organizations les regroupe en unités organisationnelles et applique des règles d'en haut.

Les Service Control Policies fixent le maximum de ce que chacun peut faire dans un compte, administrateurs compris : par exemple, personne ne peut sortir des régions approuvées ni désactiver la journalisation. Control Tower en fait une landing zone prête à l'emploi avec garde-fous.

<!-- example -->

```json
{
  "Effect": "Deny",
  "Action": "*",
  "Resource": "*",
  "Condition": {"StringNotEquals": {"aws:RequestedRegion": ["eu-west-1", "eu-west-3"]}}
}
```

#### Qu'est-ce qu'AWS Organizations ?

Un service pour gérer de façon centralisée plusieurs comptes AWS : les regrouper en unités d'organisation (OU), leur appliquer des politiques et consolider la facturation. Un compte de gestion possède l'organisation.

#### Que sont les Service Control Policies (SCP) ?

Des politiques d'AWS Organizations qui fixent les permissions maximales de comptes ou d'OU. Elles n'accordent rien : elles limitent ce que les politiques IAM de ces comptes peuvent autoriser, même pour l'utilisateur racine d'un compte membre.

#### Qu'est-ce qu'AWS Control Tower ?

Un service qui met en place et gouverne un environnement multicompte sécurisé (une landing zone) selon les bonnes pratiques, avec des garde-fous préventifs et de détection et un tableau de bord.

<!-- challenge -->

Une SCP refuse toutes les actions hors de deux régions UE. Un administrateur du compte a toutes les permissions IAM. Peut-il lancer une instance dans us-east-1 ?

<!-- solution -->

Non. Les SCP fixent les permissions maximales du compte : même un administrateur ne peut agir hors des régions autorisées. (Les services globaux peuvent nécessiter des exceptions dans la SCP.)

<!-- takeaways -->

- Organizations regroupe les comptes en OU.
- Les SCP plafonnent ce que toute identité peut faire dans un compte.
- Control Tower met en place une landing zone gouvernée.

<!-- unit: Chiffrement et secrets -->

<!-- goals -->

- Chiffrer les données au repos et en transit avec KMS et ACM.
- Stocker et renouveler des secrets avec Secrets Manager ou Parameter Store.

<!-- concept -->

Le chiffrement protège les données dans deux états. Au repos, des clés gérées dans KMS chiffrent volumes, objets et bases, et l'accès à la clé devient un second contrôle de permission. En transit, des certificats TLS d'ACM protègent le trafic vers les répartiteurs et CloudFront.

Les secrets comme les mots de passe de base ont besoin de leur propre place. Les stocker dans un service managé avec rotation signifie qu'ils ne sont jamais dans le code et changent sans redéploiement.

<!-- example -->

| Besoin | Service |
|---|---|
| Chiffrer S3, EBS, RDS avec des clés que vous contrôlez | KMS |
| HSM dédié pour une conformité stricte | CloudHSM |
| Certificat HTTPS pour un répartiteur | ACM |
| Mot de passe de base avec rotation | Secrets Manager |
| Valeurs de configuration applicative | Parameter Store |

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

<!-- challenge -->

Le mot de passe d'une base se trouve dans le code source de l'application et a été poussé dans un dépôt public. Que faites-vous maintenant, et pour la suite ?

<!-- solution -->

Changer immédiatement le mot de passe et vérifier les logs à la recherche d'abus. Le placer dans Secrets Manager avec rotation automatique, le faire lire à l'exécution via le rôle IAM de l'application et ajouter une détection de secrets au dépôt.

<!-- takeaways -->

- KMS gère les clés de chiffrement ; CloudHSM fournit des HSM dédiés.
- ACM fournit et renouvelle les certificats TLS.
- Secrets Manager stocke et renouvelle les secrets.

<!-- unit: Protéger et détecter -->

<!-- goals -->

- Associer les services de sécurité AWS aux menaces qu'ils couvrent.
- Combiner services de protection, de détection et d'enquête.

<!-- concept -->

Les services de sécurité font trois métiers. Certains protègent en bordure : Shield absorbe les DDoS et WAF filtre les requêtes web malveillantes. D'autres détectent : GuardDuty repère les menaces dans les logs, Inspector les vulnérabilités, Macie les données sensibles mal placées. D'autres aident à réagir : Security Hub rassemble les constats et Detective aide à retracer ce qui s'est passé.

Savoir quel métier fait un service suffit souvent à choisir le bon.

<!-- example -->

| Problème | Service |
|---|---|
| Tentatives d'injection SQL sur une application web | WAF |
| Gros DDoS contre un site | Shield (Advanced pour une protection renforcée) |
| Instance qui contacte une IP malveillante connue | GuardDuty |
| CVE non corrigée dans une image de conteneur | Inspector |
| Numéros de carte dans un bucket S3 | Macie |
| Une vue de tous les constats entre comptes | Security Hub |

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

<!-- challenge -->

GuardDuty signale qu'une instance EC2 mine de la cryptomonnaie. Quel service aide à comprendre comment c'est arrivé, et que faites-vous d'abord ?

<!-- solution -->

Isoler l'instance (security group restrictif, snapshot pour l'analyse) et révoquer ses identifiants. Utiliser Detective pour retracer l'activité et le point d'entrée, et Inspector pour vérifier la vulnérabilité exploitée.

<!-- takeaways -->

- Shield et WAF protègent en bordure.
- GuardDuty, Inspector et Macie détectent menaces, vulnérabilités et données sensibles.
- Security Hub centralise ; Detective enquête.

<!-- unit: Conformité et rapports -->

<!-- goals -->

- Trouver les rapports et accords de conformité d'AWS.
- Connaître les règles des tests d'intrusion et des signalements d'abus.

<!-- concept -->

Les clients héritent d'une partie de leur conformité d'AWS. Les auditeurs veulent la preuve que la part d'AWS est certifiée, et Artifact fournit ces rapports et accords à la demande. Votre part exige toujours vos propres contrôles et preuves.

Tester votre propre sécurité est permis sur de nombreux services sans demande préalable, dans le respect de règles publiées. Quand des ressources AWS sont utilisées contre vous, ou que les vôtres sont détournées, le contact est l'équipe abus.

<!-- example -->

| Besoin | Où |
|---|---|
| Rapport SOC 2 pour un auditeur | AWS Artifact |
| Signer un business associate addendum (HIPAA) | AWS Artifact |
| Test d'intrusion de votre appli web sur EC2 | Permis par la politique, sans approbation |
| Signaler du spam venant d'une IP AWS | AWS Trust & Safety (abus) |

#### Qu'est-ce qu'AWS Artifact ?

Un portail en libre-service qui donne accès aux rapports de conformité d'AWS (SOC, ISO, PCI DSS) et aux accords (comme le Business Associate Addendum pour HIPAA).

#### Qu'est-ce que le programme de conformité d'AWS ?

AWS maintient des certifications et attestations (ISO 27001, SOC 1/2/3, PCI DSS, éligibilité HIPAA, accompagnement RGPD) pour son infrastructure. Les clients héritent des contrôles de l'infrastructure, mais doivent rendre leurs propres charges de travail conformes.

#### Faut-il l'autorisation d'AWS pour réaliser un test d'intrusion ?

Pas pour une liste de services autorisés (EC2, RDS, Lambda, CloudFront et d'autres). Certaines activités restent interdites, comme les attaques DoS, qui nécessitent une procédure d'approbation distincte pour les événements simulés.

#### Qu'est-ce qu'AWS Abuse, et quand le contacter ?

L'équipe d'AWS à qui signaler que des ressources AWS sont utilisées de façon abusive, par exemple pour du spam, du scan de ports, des attaques DoS ou l'hébergement de logiciels malveillants.

<!-- challenge -->

Un auditeur demande la preuve que le centre de données qui héberge votre charge est certifié ISO 27001. Que fournissez-vous, et cela suffit-il pour votre audit ?

<!-- solution -->

Le certificat ISO 27001 d'AWS téléchargé depuis AWS Artifact. Il ne couvre que les responsabilités d'AWS ; vous devez aussi montrer vos propres contrôles (accès, chiffrement, journalisation) sur vos charges.

<!-- takeaways -->

- Artifact fournit les rapports et accords de conformité d'AWS.
- La conformité d'AWS ne couvre que la part d'AWS.
- Le test d'intrusion sur de nombreux services ne demande pas d'approbation.

<!-- stage: Services essentiels -->

### Calcul : EC2, conteneurs et serverless

<!-- unit: Bases d'EC2 -->

<!-- goals -->

- Décrire instances EC2, AMI et familles d'instances.
- Comprendre le stockage d'instance et le cycle de vie.

<!-- concept -->

EC2 loue des serveurs virtuels. On choisit un modèle (une AMI avec système et logiciels), une taille dans une famille optimisée pour le CPU, la mémoire, le stockage ou les accélérateurs, et un script à exécuter au premier démarrage. Les instances se comportent alors comme des serveurs que l'on contrôle.

Le cycle de vie compte pour les coûts et les données. Une instance arrêtée garde ses volumes EBS et ne paie plus le calcul ; une instance résiliée disparaît. Les disques d'instance store sont rapides mais perdent leurs données à l'arrêt.

<!-- example -->

```bash
aws ec2 run-instances --image-id ami-0abcd1234 --instance-type m7i.large \
  --iam-instance-profile Name=web-app \
  --user-data file://install_web.sh
```

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

#### Que sont les données utilisateur (user data) d'EC2 ?

Un script passé au lancement, exécuté au premier démarrage, pour installer des logiciels ou configurer l'instance.

#### Qu'est-ce que le stockage d'instance (instance store) d'EC2 ?

Un stockage en mode bloc temporaire, physiquement attaché au serveur hôte. Il est très rapide, mais ses données sont perdues quand l'instance s'arrête ou est résiliée : il sert aux tampons, aux caches et aux données temporaires.

#### Quelle est la différence entre arrêter et résilier une instance ?

L'arrêter l'éteint : les volumes EBS racine sont conservés, on ne paie que le stockage, et on peut la redémarrer. La résilier la supprime, ainsi que, par défaut, son volume EBS racine.

<!-- challenge -->

Une application d'analytique en mémoire gourmande en RAM tourne sur une instance polyvalente et swappe sans arrêt. Quelle famille suggérez-vous ?

<!-- solution -->

Une famille optimisée mémoire (R ou X), qui offre bien plus de RAM par vCPU. Mesurez d'abord l'usage mémoire pour choisir la taille.

<!-- takeaways -->

- L'AMI est le modèle ; la famille fixe l'équilibre des ressources.
- Arrêter garde l'EBS ; résilier supprime l'instance.
- Les données de l'instance store ne survivent pas à un arrêt.

<!-- unit: Payer EC2 -->

<!-- goals -->

- Comparer On-Demand, Savings Plans, Reserved, Spot et Dedicated.
- Associer une option tarifaire à un profil de charge.

<!-- concept -->

Une même instance peut coûter très différemment selon votre engagement. On-Demand est le prix de la flexibilité. S'engager sur un usage stable pour un ou trois ans avec Savings Plans ou Reserved Instances le réduit nettement. Spot vend la capacité inutilisée avec la plus forte remise, mais AWS peut la reprendre avec deux minutes de préavis.

Le choix tarifaire suit donc la charge : socle stable en engagement, pics en On-Demand, batch interruptible en Spot.

<!-- example -->

| Charge | Tarification |
|---|---|
| Serveurs web 24 h/24 pendant des années | Savings Plan |
| Pics de trafic saisonniers | On-Demand |
| Rendu d'images nocturne, relançable | Spot |
| Licence liée aux cœurs physiques | Dedicated Host |

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

<!-- challenge -->

Une entreprise fait tourner 20 instances toute l'année et en ajoute 30 pendant deux mois chaque hiver. Comment payer ?

<!-- solution -->

Couvrir les 20 instances stables par un Savings Plan (les Compute Savings Plans gardent de la flexibilité) et faire tourner les 30 saisonnières en On-Demand, ou en Spot si la charge tolère les interruptions.

<!-- takeaways -->

- Engagez l'usage stable ; laissez les pics en On-Demand.
- Spot est le moins cher mais interruptible.
- Les Dedicated Hosts servent les licences par cœur et l'isolation.

<!-- unit: Réseau et passage à l'échelle d'EC2 -->

<!-- goals -->

- Contrôler le trafic des instances avec des security groups et y accéder en sécurité.
- Monter en charge et répartir avec Auto Scaling et ELB.

<!-- concept -->

Une instance seule n'est ni joignable en sécurité ni résiliente. Les security groups décident du trafic qui l'atteint, et ils sont stateful : les réponses sont autorisées automatiquement. Session Manager et Instance Connect donnent un accès administrateur sans clés SSH de longue durée.

Résilience et échelle viennent de groupes d'instances : un répartiteur distribue le trafic sur plusieurs zones et cesse d'envoyer vers les cibles malsaines, tandis qu'Auto Scaling remplace les instances en panne et ajuste la capacité à la demande.

<!-- example -->

```text
users ─► Application Load Balancer (AZ a, b)
           └─► Auto Scaling group: min 2, desired 4, max 10 (target CPU 50%)
                 security group: allow 443 from the load balancer only
```

#### Qu'est-ce qu'un groupe de sécurité ?

Un pare-feu virtuel avec état pour les instances (attaché aux interfaces réseau). Il n'a que des règles d'autorisation. Le trafic de retour est autorisé automatiquement, et par défaut tout le trafic entrant est refusé et tout le trafic sortant autorisé.

#### Qu'est-ce qu'une adresse IP Elastic ?

Une adresse IPv4 publique statique que vous allouez à votre compte et pouvez attacher à une instance. Les adresses IPv4 publiques sont facturées à l'heure, attachées ou non.

#### Qu'est-ce qu'EC2 Auto Scaling ?

Un service qui ajoute ou retire des instances EC2 d'un groupe Auto Scaling selon des politiques (suivi de cible, par paliers, planifiées, prédictives), et remplace les instances défaillantes. On définit une capacité minimale, souhaitée et maximale.

#### Qu'est-ce qu'Elastic Load Balancing, et quels en sont les types ?

Un service qui répartit le trafic entre des cibles dans plusieurs AZ et vérifie leur santé.
- **Application Load Balancer :** HTTP/HTTPS, couche 7, routage par chemin et par hôte.
- **Network Load Balancer :** TCP/UDP/TLS, couche 4, très hautes performances et IP statiques.
- **Gateway Load Balancer :** couche 3, pour les appliances réseau tierces comme les pare-feu.

#### Qu'apportent EC2 Instance Connect et Session Manager ?

Des moyens d'accéder aux instances sans gérer de clés SSH. Session Manager (dans Systems Manager) fonctionne même sans ouvrir de port entrant, et journalise les sessions.

<!-- challenge -->

Une application web tourne sur une seule instance avec une Elastic IP. Elle est tombée quand l'instance a lâché. Comment la reconcevez-vous ?

<!-- solution -->

Placer deux instances ou plus dans un groupe Auto Scaling sur deux zones derrière un Application Load Balancer, pointer le DNS vers le répartiteur et abandonner l'Elastic IP. Les instances en panne sont remplacées automatiquement.

<!-- takeaways -->

- Les security groups sont des pare-feu stateful par instance.
- Les répartiteurs distribuent le trafic et vérifient la santé.
- Auto Scaling remplace et ajuste les instances.

<!-- unit: Conteneurs et fonctions -->

<!-- goals -->

- Choisir entre Lambda, ECS, EKS et Fargate.
- Savoir où sont stockées les images de conteneurs.

<!-- concept -->

Conteneurs et fonctions éloignent encore le travail des serveurs. Lambda exécute une fonction par événement et ne facture que pendant l'exécution, idéal pour du travail court et irrégulier. Les conteneurs empaquettent une application avec ses dépendances ; ECS et EKS les planifient et Fargate les exécute sans gérer d'instances.

Le choix dépend de la durée du travail, du contrôle voulu et de la maîtrise de Kubernetes par l'équipe.

<!-- example -->

| Charge | Bon choix |
|---|---|
| Redimensionner une image à son dépôt | Lambda |
| API web en conteneurs, petite équipe | ECS sur Fargate |
| Le standard de l'entreprise est Kubernetes | EKS |
| Stocker et analyser les images | ECR |

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

<!-- challenge -->

Une tâche de traitement de données dure 40 minutes chaque nuit. Un collègue propose Lambda. Est-ce adapté ?

<!-- solution -->

Non : les fonctions Lambda sont limitées à 15 minutes. Exécutez-la comme tâche de conteneur sur ECS avec Fargate (ou AWS Batch), sans cette limite et toujours sans serveur à gérer.

<!-- takeaways -->

- Lambda pour le travail court piloté par événements (15 minutes maximum).
- ECS est plus simple ; EKS, c'est Kubernetes.
- Fargate exécute des conteneurs sans gérer d'instances.

<!-- unit: Plateformes managées -->

<!-- goals -->

- Reconnaître les usages d'Elastic Beanstalk, Lightsail, Batch et App Runner.
- Choisir la plateforme la plus simple qui convient.

<!-- concept -->

Certains services existent surtout pour masquer les décisions d'infrastructure. Elastic Beanstalk déploie du code sur EC2 avec répartition de charge et montée en charge déjà configurées. App Runner fait de même pour conteneurs et code source avec encore moins de réglages. Lightsail propose des serveurs simples à prix fixe pour les petits projets. Batch planifie de très nombreux jobs sur une capacité managée.

Ils échangent contrôle contre vitesse, souvent le bon choix pour les petites équipes.

<!-- example -->

| Besoin | Service |
|---|---|
| Déployer une appli Django sans apprendre les détails d'EC2 | Elastic Beanstalk |
| Exécuter une API web conteneurisée depuis un dépôt | App Runner |
| Petit blog à prix mensuel prévisible | Lightsail |
| 10 000 jobs de simulation | AWS Batch |

#### Qu'est-ce qu'AWS Elastic Beanstalk ?

Une plateforme en tant que service : vous déposez le code de l'application (Java, .NET, Node.js, Python, PHP, Go, Ruby, Docker) et Beanstalk provisionne et gère EC2, l'équilibrage de charge, Auto Scaling et la supervision. Les ressources sous-jacentes restent visibles et configurables.

#### Qu'est-ce qu'Amazon Lightsail ?

Un service simplifié de serveurs privés virtuels, de bases de données et de conteneurs à prix mensuel prévisible, destiné aux sites simples et aux débutants sur AWS.

#### Qu'est-ce qu'AWS Batch ?

Un service qui exécute des traitements par lots à n'importe quelle échelle, en provisionnant de la capacité EC2 ou Fargate (y compris Spot) selon les travaux en file d'attente.

#### Qu'est-ce qu'AWS App Runner ?

Un service entièrement géré qui construit et exécute des applications web et des API à partir de code source ou d'une image de conteneur, avec montée en charge automatique et HTTPS.

<!-- challenge -->

Une startup de deux personnes veut déployer cette semaine une API conteneurisée avec HTTPS et autoscaling, sans expérience d'exploitation. Que suggérez-vous ?

<!-- solution -->

AWS App Runner : pointez-le vers l'image ou le dépôt, il gère build, déploiement, HTTPS, répartition et montée en charge. Revoir ECS plus tard si plus de contrôle devient nécessaire.

<!-- takeaways -->

- Les services de plateforme échangent contrôle contre vitesse.
- Beanstalk et App Runner déploient sans travail d'infrastructure.
- Batch exécute de longues files de jobs sur capacité managée.

### Stockage

<!-- unit: Bases de S3 -->

<!-- goals -->

- Décrire buckets, objets, durabilité et classes de stockage.
- Réduire les coûts de stockage avec classes et règles de cycle de vie.

<!-- concept -->

S3 stocke des objets (fichiers avec métadonnées) dans des buckets, avec une durabilité très élevée car chaque objet est copié sur plusieurs installations. Ce qui varie, c'est la vitesse et la fréquence d'accès nécessaires, et les classes de stockage en fixent le prix : l'accès fréquent coûte plus au gigaoctet stocké, l'archive coûte peu à stocker mais plus, et plus lentement, à récupérer.

Les règles de cycle de vie déplacent les objets entre classes en vieillissant : les données deviennent moins chères automatiquement.

<!-- example -->

```json
{"Rules": [{"ID": "logs", "Status": "Enabled", "Filter": {"Prefix": "logs/"},
  "Transitions": [{"Days": 30, "StorageClass": "STANDARD_IA"},
                  {"Days": 180, "StorageClass": "GLACIER"}],
  "Expiration": {"Days": 730}}]}
```

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

#### Quelles sont la durabilité et la disponibilité de S3 Standard ?

Il est conçu pour une durabilité de 99,999999999 % et une disponibilité de 99,99 %, avec les données stockées sur au moins trois AZ.

#### Quand utiliser S3 One Zone-IA ?

Pour des données peu consultées qu'on peut recréer, comme des copies de sauvegarde secondaires ou des données dérivées, quand la perte d'une AZ est acceptable en échange d'un prix plus bas.

#### Que sont les règles de cycle de vie S3 ?

Des règles qui font passer automatiquement les objets vers des classes de stockage moins chères au-delà d'un certain âge, ou qui les suppriment (expiration).

<!-- challenge -->

Les logs d'une application sont lus souvent pendant une semaine, rarement pendant un an, et doivent être conservés 7 ans pour l'audit. Concevez un cycle de vie.

<!-- solution -->

Les garder en S3 Standard 30 jours, les passer en Standard-IA, puis en Glacier Flexible Retrieval ou Deep Archive après un an, et les faire expirer au bout de 7 ans.

<!-- takeaways -->

- S3 stocke des objets dans des buckets avec 11 neuf de durabilité.
- Les classes échangent vitesse d'accès contre prix.
- Les règles de cycle de vie déplacent et font expirer les données.

<!-- unit: Protéger et servir les données S3 -->

<!-- goals -->

- Protéger les objets avec versionnement, contrôles d'accès, chiffrement et réplication.
- Servir des sites web et accélérer les envois depuis S3.

<!-- concept -->

Les réglages par défaut de S3 sont sûrs (les nouveaux buckets sont privés et chiffrés), et la plupart des incidents viennent de leur modification. Le versionnement protège des écrasements et suppressions, Block Public Access empêche les expositions accidentelles, les politiques limitent qui lit quoi et la réplication garde une copie dans une autre région.

S3 peut aussi servir du contenu directement, pour des sites statiques, souvent derrière CloudFront, et accélérer les envois longue distance via les edge locations.

<!-- example -->

```bash
aws s3api put-bucket-versioning --bucket finance-docs --versioning-configuration Status=Enabled
aws s3api put-public-access-block --bucket finance-docs \
  --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```

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

<!-- challenge -->

Un utilisateur a supprimé un dossier important d'un bucket. Le versionnement était activé. Peut-on le récupérer, et comment ?

<!-- solution -->

Oui. Avec le versionnement, la suppression n'a ajouté que des delete markers. Retirez-les (ou recopiez les versions précédentes), et envisagez MFA delete ou Object Lock pour les buckets critiques.

<!-- takeaways -->

- Le versionnement protège des écrasements et suppressions.
- Block Public Access empêche les expositions accidentelles.
- La réplication copie les objets vers une autre région ou un autre compte.

<!-- unit: Stockage bloc et fichiers -->

<!-- goals -->

- Comparer S3, EBS, EFS et FSx.
- Sauvegarder des volumes EBS avec des snapshots.

<!-- concept -->

Toutes les applications ne peuvent pas utiliser du stockage objet. Bases de données et systèmes d'exploitation ont besoin de stockage bloc, un disque attaché à une instance : c'est EBS, sauvegardé par snapshots incrémentaux. Les applications qui partagent des fichiers entre de nombreux serveurs ont besoin d'un système de fichiers : EFS pour Linux, FSx pour Windows et les systèmes spécialisés.

Le choix suit le mode d'accès : objets par API, disque d'une instance ou fichiers partagés.

<!-- example -->

| Besoin | Service |
|---|---|
| Disque de démarrage et de base pour une instance | EBS |
| Dossier partagé pour 20 serveurs web Linux | EFS |
| Partages Windows avec Active Directory | FSx for Windows File Server |
| Images et sauvegardes accessibles en HTTP | S3 |

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

<!-- challenge -->

Dix serveurs Linux derrière un répartiteur doivent lire et écrire les mêmes fichiers déposés. Quel stockage choisissez-vous ?

<!-- solution -->

Amazon EFS, monté par tous les serveurs en NFS, ou S3 si l'application peut utiliser une API. Un volume EBS ne s'attache qu'à une instance : il ne convient pas à l'accès partagé.

<!-- takeaways -->

- EBS est du stockage bloc pour une instance.
- EFS et FSx sont des systèmes de fichiers partagés.
- S3 est du stockage objet accessible par API.

<!-- unit: Hybride, transfert et sauvegarde -->

<!-- goals -->

- Transférer des données vers AWS en ligne et hors ligne.
- Centraliser les sauvegardes entre services.

<!-- concept -->

Amener des données dans AWS dépend du volume et de la bande passante. Les transferts en ligne avec DataSync conviennent aux volumes continus ou modérés ; quand un transfert réseau prendrait des semaines, les appareils Snow transportent physiquement les données. Certaines applications sur site continuent de tourner et utilisent le stockage cloud via Storage Gateway.

Une fois les charges sur AWS, les sauvegardes doivent être centralisées, avec politiques et audit entre services : c'est le rôle d'AWS Backup.

<!-- example -->

| Situation | Service |
|---|---|
| Archive de 500 To, lien de bureau lent | Snowball |
| Synchronisation quotidienne d'un serveur NFS vers S3 | DataSync |
| Logiciel de sauvegarde sur site écrivant sur des bandes cloud | Storage Gateway (Tape Gateway) |
| Politique de sauvegarde pour RDS, EBS et DynamoDB | AWS Backup |

#### Qu'est-ce qu'AWS Storage Gateway ?

Un service de stockage hybride qui donne aux applications sur site un accès au stockage cloud. Types : S3 File Gateway, FSx File Gateway, Volume Gateway et Tape Gateway (bibliothèque de bandes virtuelle pour les sauvegardes).

#### Qu'est-ce que la famille AWS Snow ?

Des appareils physiques pour transférer hors ligne de grandes quantités de données vers ou depuis AWS, ou traiter des données en périphérie avec peu ou pas de connectivité (appareils AWS Snowball Edge).

#### Qu'est-ce qu'AWS DataSync ?

Un service de transfert de données en ligne qui déplace des données entre un stockage sur site (NFS, SMB, HDFS, stockage objet) et les services de stockage AWS, rapidement et avec vérification.

#### Qu'est-ce qu'AWS Backup ?

Un service central pour automatiser et auditer les sauvegardes de nombreux services : EBS, EC2, RDS, DynamoDB, EFS, FSx, S3 et d'autres, avec des plans de sauvegarde et des copies entre régions ou entre comptes.

<!-- challenge -->

Une entreprise doit transférer 200 To vers AWS par un lien de 100 Mbit/s. Estimez la durée en ligne et proposez une option.

<!-- solution -->

À 100 Mbit/s, 200 To prennent environ 185 jours à pleine vitesse. Utiliser des Snowball Edge pour expédier les données, puis DataSync pour les modifications survenues pendant l'expédition.

<!-- takeaways -->

- DataSync transfère en ligne ; les appareils Snow transportent.
- Storage Gateway relie les applications sur site au stockage cloud.
- AWS Backup centralise les politiques de sauvegarde.

### Bases de données et analytique

<!-- unit: Bases de données relationnelles -->

<!-- goals -->

- Comparer RDS, Aurora et DynamoDB.
- Distinguer Multi-AZ et réplicas en lecture, et utiliser DMS pour migrer.

<!-- concept -->

Les bases relationnelles sur AWS sont managées : RDS exécute des moteurs connus et gère sauvegardes, correctifs et basculement ; Aurora est le moteur cloud natif d'AWS, au stockage répliqué entre zones. DynamoDB est un autre modèle, un magasin clé-valeur qui monte en charge sans serveurs.

Deux fonctions de RDS sont souvent confondues. Le Multi-AZ sert la disponibilité : un standby prend le relais si le primaire tombe. Les réplicas en lecture servent l'échelle : ils absorbent les lectures. DMS migre les bases existantes avec peu d'interruption.

<!-- example -->

| Besoin | Choix |
|---|---|
| Survivre à la panne d'une zone | RDS Multi-AZ |
| Décharger les lectures de reporting | Réplica en lecture |
| Panier d'achat pour des millions d'utilisateurs, accès par clé | DynamoDB |
| Migrer un Oracle sur site vers PostgreSQL | DMS (+ Schema Conversion) |

#### En quoi Amazon RDS diffère-t-il d'Amazon DynamoDB ?

RDS est un service de bases de données relationnelles géré (SQL, schémas, jointures, transactions) qui fait tourner MySQL, PostgreSQL, MariaDB, Oracle, SQL Server ou Db2 sur des instances que vous dimensionnez. DynamoDB est une base NoSQL serverless clé-valeur et documents, avec des performances de quelques millisecondes à toute échelle, sans schéma fixe au-delà des clés et avec une montée en charge automatique.

#### Que gère Amazon RDS pour vous ?

Le provisionnement, les correctifs du système d'exploitation et de la base de données, les sauvegardes automatiques et la restauration à un instant donné, la bascule Multi-AZ, les réplicas en lecture, la supervision et l'extension du stockage. Vous gérez le schéma, les requêtes, les utilisateurs et l'accès réseau.

#### Quelle est la différence entre RDS Multi-AZ et les réplicas en lecture ?

Multi-AZ maintient une ou plusieurs instances de secours synchrones dans une autre AZ pour la haute disponibilité et la bascule automatique. Dans sa configuration classique, elle ne sert pas les lectures. Les réplicas en lecture sont des copies asynchrones pour répartir les lectures, éventuellement dans d'autres régions, et peuvent être promus.

#### Qu'est-ce qu'Amazon Aurora ?

Une base de données relationnelle native cloud compatible MySQL et PostgreSQL. Elle stocke six copies des données sur trois AZ, étend son stockage automatiquement et propose Aurora Serverless pour les charges variables.

#### Qu'est-ce qu'AWS Database Migration Service (DMS) ?

Un service qui migre des bases de données vers AWS avec une interruption minimale, entre moteurs identiques (homogène) ou différents (hétérogène, avec la Schema Conversion Tool), et qui peut répliquer les changements en continu.

<!-- challenge -->

Les rapports ralentissent une base RDS en journée. L'équipe propose d'activer le Multi-AZ. Est-ce la bonne correction ?

<!-- solution -->

Non. Les standbys Multi-AZ ne servent pas de lectures ; ils servent au basculement. Ajoutez un réplica en lecture et dirigez-y les rapports (ou déplacez le reporting vers un entrepôt).

<!-- takeaways -->

- RDS gère des moteurs ; Aurora est cloud natif ; DynamoDB est clé-valeur.
- Multi-AZ = disponibilité ; réplicas = échelle en lecture.
- DMS migre les bases avec un minimum d'interruption.

<!-- unit: Bases de données spécialisées -->

<!-- goals -->

- Associer besoins de cache, documents, graphes, colonnes larges et séries temporelles aux services.
- Savoir quand un magasin en mémoire aide.

<!-- concept -->

L'approche d'AWS, c'est « la bonne base pour chaque usage ». Au lieu de tout forcer en tables, AWS propose des moteurs conçus pour des modes d'accès précis : caches en mémoire pour des lectures en microsecondes, magasins de documents pour le JSON, graphes pour les relations, colonnes larges pour les écritures massives, séries temporelles pour les métriques.

La question à poser : comment l'application lit-elle et écrit-elle ses données ? Le moteur en découle.

<!-- example -->

| Mode d'accès | Service |
|---|---|
| Mettre en cache les pages produit | ElastiCache |
| Magasin principal durable compatible Redis | MemoryDB |
| Documents de type MongoDB | DocumentDB |
| Réseaux de fraude, graphes sociaux | Neptune |
| Charges Cassandra | Keyspaces |
| Relevés de capteurs IoT | Timestream |

#### Qu'est-ce qu'Amazon ElastiCache ?

Un cache en mémoire géré avec Valkey, Redis OSS ou Memcached, utilisé pour réduire la charge de la base de données et servir les lectures fréquentes avec une latence de l'ordre de la microseconde.

#### Qu'est-ce qu'Amazon MemoryDB ?

Une base de données en mémoire durable, compatible Valkey et Redis OSS, utilisable comme base principale grâce à son journal de transactions Multi-AZ.

#### Qu'est-ce qu'Amazon DocumentDB ?

Une base de données documentaire gérée, compatible avec les charges de travail MongoDB.

#### Qu'est-ce qu'Amazon Neptune ?

Une base de données de graphes gérée pour des données très connectées, comme les réseaux sociaux, la détection de fraude et les graphes de connaissances.

#### Qu'est-ce qu'Amazon Keyspaces ?

Une base de données serverless gérée, compatible Apache Cassandra.

#### Qu'est-ce qu'Amazon Timestream ?

Une base de données de séries temporelles gérée pour l'IoT et les métriques opérationnelles.

<!-- challenge -->

Les pages produit d'un site e-commerce interrogent la base à chaque vue et la surchargent. Qu'ajoutez-vous ?

<!-- solution -->

Un cache ElastiCache devant la base : mettre en cache les données produit avec une expiration raisonnable, pour que la plupart des vues n'atteignent jamais la base.

<!-- takeaways -->

- Choisissez la base selon le mode d'accès.
- Les caches réduisent charge et latence de la base.
- Graphes, documents et séries temporelles servent des formes précises.

<!-- unit: Services analytiques -->

<!-- goals -->

- Distinguer OLTP et OLAP et les services de chacun.
- Situer Redshift, Athena, Glue, EMR et Lake Formation dans une plateforme de données.

<!-- concept -->

Les systèmes transactionnels répondent vite à beaucoup de petites questions ; les systèmes analytiques répondent à de grandes questions sur beaucoup d'historique. Les mélanger ralentit les deux : l'analytique part donc sur une plateforme séparée.

Sur AWS, cette plateforme a des pièces interchangeables : S3 comme lake, Glue pour cataloguer et transformer, Lake Formation pour gouverner, Athena pour du SQL serverless sur fichiers, Redshift comme entrepôt pour la BI lourde et EMR pour les frameworks big data.

<!-- example -->

```text
RDS (OLTP) ─► DMS / Glue ─► S3 data lake ─► Athena (ad hoc SQL)
                               │  Glue Data Catalog + Lake Formation
                               └─► Redshift (dashboards)   EMR (Spark)
```

#### Qu'est-ce qu'Amazon Redshift ?

Un entrepôt de données cloud géré, à l'échelle du pétaoctet, pour les requêtes SQL analytiques (OLAP), avec stockage en colonnes, une option serverless et la possibilité d'interroger des données dans S3.

#### Quelle est la différence entre OLTP et OLAP, et quels services AWS conviennent à chacun ?

L'OLTP gère beaucoup de petites lectures et écritures transactionnelles (commandes, paiements) : RDS, Aurora, DynamoDB. L'OLAP exécute de grosses requêtes analytiques sur des données historiques : Redshift, Athena.

#### Qu'est-ce qu'Amazon Athena ?

Un service de requêtes interactives serverless pour analyser des données dans S3 en SQL standard. On paie au volume de données analysé : les formats en colonnes et le partitionnement réduisent le coût.

#### Qu'est-ce qu'AWS Glue ?

Un service d'intégration de données serverless : des crawlers pour découvrir les schémas, le Glue Data Catalog comme référentiel central de métadonnées, et des jobs ETL basés sur Spark.

#### Qu'est-ce qu'Amazon EMR ?

Une plateforme big data gérée pour exécuter Apache Spark, Hive, Presto/Trino, HBase et d'autres frameworks sur EC2, EKS ou en serverless.

#### Qu'est-ce qu'AWS Lake Formation ?

Un service pour construire, sécuriser et gérer un data lake sur S3, avec des permissions centralisées et fines sur les tables du Glue Data Catalog.

<!-- challenge -->

Des analystes veulent lancer ponctuellement du SQL sur trois ans de logs dans S3 sans les charger ailleurs. Quel service convient ?

<!-- solution -->

Amazon Athena avec des tables dans le Glue Data Catalog : les requêtes tournent directement sur S3 et l'on paie les données scannées. Convertir les logs en Parquet garde les coûts bas.

<!-- takeaways -->

- OLTP pour les transactions ; OLAP pour l'analyse.
- Athena interroge S3 ; Redshift sert la BI lourde.
- Glue et Lake Formation cataloguent et gouvernent le lake.

<!-- unit: Streaming, recherche et BI -->

<!-- goals -->

- Reconnaître les usages de Kinesis, OpenSearch et QuickSight.
- Construire un flux simple du temps réel au tableau de bord.

<!-- concept -->

Certaines données n'ont de valeur que fraîches : clics, relevés de capteurs, logs. Kinesis capture et livre ces flux, pour un traitement maison ou directement vers le stockage. OpenSearch indexe textes et logs pour les rechercher et les explorer de façon interactive.

Au bout de la plupart des pipelines se trouve un outil de BI ; QuickSight fournit des tableaux de bord serverless que les métiers peuvent explorer et partager.

<!-- example -->

```text
app clicks ─► Kinesis Data Streams ─► consumers (real-time alerts)
           └► Firehose ─► S3 ─► Athena ─► QuickSight dashboard
app logs   ─► OpenSearch Service (search, log analytics)
```

#### Qu'est-ce qu'Amazon Kinesis ?

Des services pour les données en streaming en temps réel. Kinesis Data Streams capture et stocke des flux pour un traitement sur mesure. Amazon Data Firehose charge des flux vers des destinations comme S3, Redshift ou OpenSearch.

#### Qu'est-ce qu'Amazon OpenSearch Service ?

Un service géré pour les clusters OpenSearch (et l'ancien Elasticsearch), utilisé pour l'analyse de journaux, la recherche plein texte et l'observabilité.

#### Qu'est-ce qu'Amazon QuickSight ?

Un service de business intelligence serverless pour créer des tableaux de bord et des rapports interactifs, avec des analyses fondées sur l'apprentissage automatique et des questions en langage naturel.

<!-- challenge -->

Les ingénieurs du support veulent rechercher par mot-clé dans les logs d'erreurs quelques secondes après chaque erreur. Quel service suggérez-vous ?

<!-- solution -->

Amazon OpenSearch Service, alimenté par les logs (par exemple via Firehose ou des abonnements CloudWatch), avec OpenSearch Dashboards pour la recherche et les visualisations.

<!-- takeaways -->

- Kinesis capture et livre les données en flux.
- OpenSearch sert la recherche et l'analytique de logs.
- QuickSight fournit des tableaux de bord BI serverless.

### Réseau et diffusion de contenu

<!-- unit: Briques d'un VPC -->

<!-- goals -->

- Décrire VPC, blocs CIDR et sous-réseaux.
- Router le trafic avec internet gateways, NAT gateways et bastions.

<!-- concept -->

Un VPC est votre réseau privé dans une région, avec une plage d'adresses que vous choisissez. Les sous-réseaux le découpent par zone et par exposition. Ce qui rend un sous-réseau public n'est pas une case à cocher mais une route vers un internet gateway ; les sous-réseaux privés n'en ont pas, leurs ressources sont donc injoignables depuis Internet.

Les ressources privées doivent tout de même télécharger des mises à jour, ce que permettent les NAT gateways dans un seul sens. L'accès d'administration passe par un bastion durci ou, mieux, par Session Manager.

<!-- example -->

```text
VPC 10.0.0.0/16
 ├─ public subnet  10.0.1.0/24  (AZ a)  route 0.0.0.0/0 → internet gateway   [load balancer, NAT]
 └─ private subnet 10.0.11.0/24 (AZ a)  route 0.0.0.0/0 → NAT gateway        [app servers, DB]
```

#### Qu'est-ce qu'Amazon VPC ?

Virtual Private Cloud est un réseau virtuel isolé logiquement, dans une région, où l'on lance des ressources. On choisit sa plage d'adresses IP et on crée des sous-réseaux, des tables de routage et des passerelles.

#### Qu'est-ce qu'un bloc CIDR ?

Une notation pour une plage d'adresses IP, comme 10.0.0.0/16, utilisée pour définir l'espace d'adressage d'un VPC et de ses sous-réseaux.

#### Quelle est la différence entre un sous-réseau public et un sous-réseau privé ?

Un sous-réseau public a une route vers une passerelle internet : les ressources dotées d'une IP publique sont joignables depuis internet. Un sous-réseau privé n'a pas cette route : ses ressources ne sortent sur internet, le cas échéant, que par une passerelle NAT.

#### Qu'est-ce qu'une passerelle internet ?

Un composant du VPC qui permet la communication entre les ressources du VPC et internet.

#### Qu'est-ce qu'une passerelle NAT ?

Un service géré qui permet aux instances de sous-réseaux privés d'ouvrir des connexions sortantes vers internet (pour des mises à jour, par exemple) tout en bloquant les connexions entrantes non sollicitées.

#### Qu'est-ce qu'un hôte bastion ?

Une instance dans un sous-réseau public qui sert de point d'entrée durci pour accéder en SSH ou RDP aux instances de sous-réseaux privés. Systems Manager Session Manager le remplace souvent.

<!-- challenge -->

Des serveurs de base de données ne doivent pas être joignables depuis Internet mais doivent télécharger les correctifs système. Où les placez-vous, et comment obtiennent-ils les correctifs ?

<!-- solution -->

Dans des sous-réseaux privés sans route vers l'internet gateway, avec une route vers un NAT gateway situé dans un sous-réseau public pour le seul trafic sortant. Mieux encore : VPC endpoints et Systems Manager Patch Manager.

<!-- takeaways -->

- Une route vers un internet gateway rend un sous-réseau public.
- Les NAT gateways n'autorisent que la sortie vers Internet.
- Placez bases et serveurs d'application dans des sous-réseaux privés.

<!-- unit: Sécurité réseau et accès privé -->

<!-- goals -->

- Comparer security groups et network ACL.
- Atteindre les services AWS en privé et journaliser le trafic réseau.

<!-- concept -->

La défense réseau a deux couches. Les security groups protègent chaque ressource et retiennent les connexions : les réponses reviennent automatiquement. Les network ACL protègent des sous-réseaux entiers, évaluent leurs règles dans l'ordre et exigent des règles explicites dans les deux sens. La plupart des conceptions s'appuient sur les security groups et gardent des ACL simples.

Le trafic vers les services AWS n'a pas besoin d'Internet non plus : endpoints et PrivateLink le gardent sur le réseau AWS. Les Flow Logs enregistrent ce qui est réellement passé.

<!-- example -->

| | Security group | Network ACL |
|---|---|---|
| S'applique à | Interface réseau | Sous-réseau |
| État | Stateful | Stateless |
| Règles | Autorisation seule | Autorisation et refus, numérotées |

#### Quelle est la différence entre un groupe de sécurité et une ACL réseau ?

Un groupe de sécurité agit au niveau de l'instance (interface réseau), il est avec état et n'a que des règles d'autorisation. Une ACL réseau agit au niveau du sous-réseau, elle est sans état (le trafic de retour doit être autorisé explicitement), accepte des règles d'autorisation et de refus, et évalue les règles par ordre de numéro.

#### Que sont les VPC Flow Logs ?

Des enregistrements du trafic IP entrant et sortant des interfaces réseau d'un VPC, envoyés vers CloudWatch Logs ou S3 pour le dépannage et l'analyse de sécurité.

#### Qu'est-ce qu'un point de terminaison de VPC (VPC endpoint) ?

Une connexion privée d'un VPC vers des services AWS sans passer par internet. Les points de terminaison de passerelle servent S3 et DynamoDB. Les points de terminaison d'interface (AWS PrivateLink) servent beaucoup d'autres services.

#### Qu'est-ce qu'AWS PrivateLink ?

Une technologie qui expose des services de façon privée entre VPC et comptes via des points de terminaison d'interface, en gardant le trafic sur le réseau AWS.

<!-- challenge -->

Vous devez empêcher une plage d'IP malveillantes d'atteindre toute instance d'un sous-réseau. Security group ou NACL ?

<!-- solution -->

Une network ACL avec une règle de refus pour cette plage, numérotée avant les règles d'autorisation : les security groups ne savent pas refuser, seulement autoriser.

<!-- takeaways -->

- Security groups : stateful, par ressource, autorisation seule.
- NACL : stateless, par sous-réseau, autorisation et refus.
- Les endpoints gardent privé le trafic vers les services AWS.

<!-- unit: Relier des réseaux -->

<!-- goals -->

- Relier des VPC avec le peering et Transit Gateway.
- Relier bureaux et utilisateurs avec VPN et Direct Connect.

<!-- concept -->

Quand une entreprise grandit, les réseaux se multiplient : nombreux VPC, bureaux, centres de données et télétravailleurs. Le peering relie directement deux VPC mais ne se chaîne pas : de nombreux VPC finissent en maillage. Transit Gateway remplace le maillage par un hub.

Pour les liaisons sur site, le VPN est rapide et chiffré via Internet ; Direct Connect est une ligne privée aux performances stables qui demande des semaines de mise en place. Client VPN sert les utilisateurs individuels.

<!-- example -->

| Besoin | Service |
|---|---|
| Deux VPC partagent une base | VPC peering |
| 40 VPC et deux centres de données | Transit Gateway |
| Liaison de bureau cette semaine | Site-to-Site VPN |
| 10 Gbit/s stables vers AWS | Direct Connect |
| Salariés à distance | Client VPN |

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

<!-- challenge -->

Une entreprise a besoin d'une liaison fiable et à haut débit vers AWS, sans pouvoir attendre des mois, et doit rester couverte si la liaison tombe. Que mettez-vous en place ?

<!-- solution -->

Commander Direct Connect pour le débit stable et monter tout de suite un Site-to-Site VPN ; garder le VPN comme chemin de secours une fois Direct Connect en service.

<!-- takeaways -->

- Le peering relie deux VPC ; Transit Gateway en relie beaucoup.
- Le VPN est rapide et chiffré ; Direct Connect, privé et stable.
- Client VPN relie les utilisateurs individuels.

<!-- unit: DNS et diffusion de contenu -->

<!-- goals -->

- Router les utilisateurs avec Route 53 et ses politiques de routage.
- Accélérer les applications avec CloudFront, Global Accelerator et API Gateway.

<!-- concept -->

Les utilisateurs atteignent les applications par des noms et des réseaux que l'on peut façonner. Route 53 répond aux requêtes DNS et peut envoyer les utilisateurs vers le point le plus proche, le plus sain ou selon un poids. CloudFront met le contenu en cache près des utilisateurs pour que la plupart des requêtes n'atteignent jamais vos serveurs. Global Accelerator fait entrer tôt le trafic non cacheable sur le réseau dorsal d'AWS.

API Gateway place devant les API authentification, limitation de débit et surveillance, souvent devant Lambda.

<!-- example -->

| Objectif | Politique Route 53 |
|---|---|
| Envoyer 10 % des utilisateurs vers une nouvelle version | Weighted |
| Basculer vers une région de secours | Failover |
| Servir depuis la région la plus rapide | Latency |
| Servir du contenu français en France | Geolocation |

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

<!-- challenge -->

Un site hébergé dans eu-west-1 est lent pour les utilisateurs en Asie, surtout à cause de grandes images. Qu'ajoutez-vous d'abord ?

<!-- solution -->

Amazon CloudFront devant le site (ou le bucket S3 des images), pour que le contenu soit mis en cache dans des edge locations proches des utilisateurs asiatiques.

<!-- takeaways -->

- Route 53 route selon poids, latence, santé ou localisation.
- CloudFront met le contenu en cache en périphérie.
- API Gateway protège et pilote les API.

<!-- stage: Exploiter et payer -->

### Gestion, gouvernance et outils de développement

<!-- unit: Surveillance et audit -->

<!-- goals -->

- Distinguer CloudWatch, CloudTrail et Config.
- Tracer les requêtes et suivre la santé des services AWS.

<!-- concept -->

Trois questions, trois services. Est-ce que ça va ? CloudWatch collecte métriques et logs et déclenche des alarmes. Qui a fait quoi ? CloudTrail enregistre chaque appel d'API. La configuration est-elle conforme ? Config enregistre la configuration des ressources dans le temps et la compare à des règles.

Pour les applications distribuées, X-Ray suit une requête à travers les services, et le Health Dashboard vous prévient quand AWS lui-même a un problème qui vous touche.

<!-- example -->

| Question | Service |
|---|---|
| CPU au-dessus de 80 % pendant 10 minutes ? | Alarme CloudWatch |
| Qui a supprimé le security group ? | CloudTrail |
| Tous les buckets sont-ils chiffrés ? | Règle Config |
| Quel service ralentit le paiement ? | X-Ray |
| Une panne AWS touche-t-elle ma région ? | Health Dashboard |

#### Qu'est-ce qu'Amazon CloudWatch ?

Un service de supervision et d'observabilité : métriques, alarmes, journaux (CloudWatch Logs), tableaux de bord et événements, pour les ressources AWS et les applications.

#### Qu'est-ce qu'AWS CloudTrail ?

Un service qui enregistre les appels d'API et l'activité du compte (qui a fait quoi, quand, d'où) pour la gouvernance, la conformité et l'audit. Les journaux peuvent être livrés dans S3 et analysés avec CloudTrail Lake.

#### Quelle est la différence entre CloudWatch et CloudTrail ?

CloudWatch supervise les performances et la santé (métriques, journaux, alarmes). CloudTrail audite les actions (appels d'API effectués dans le compte).

#### Qu'est-ce qu'AWS Config ?

Un service qui enregistre la configuration des ressources et ses changements au fil du temps et l'évalue selon des règles, pour l'audit de conformité et le dépannage.

#### Qu'est-ce qu'AWS X-Ray ?

Un service qui trace les requêtes à travers des applications distribuées pour trouver les goulets d'étranglement et les erreurs.

#### Qu'est-ce que l'AWS Health Dashboard ?

Une vue de l'état des services AWS et des événements qui touchent vos propres ressources, comme une maintenance planifiée ou un incident dans vos régions.

<!-- challenge -->

Un security group de production a été ouvert à tout Internet hier soir. Comment trouver qui l'a fait et être alerté la prochaine fois ?

<!-- solution -->

Chercher dans CloudTrail l'appel `AuthorizeSecurityGroupIngress` pour identifier l'auteur et l'heure. Ajouter une règle Config (ou EventBridge) qui signale les security groups ouverts et prévient l'équipe, avec remédiation automatique si souhaité.

<!-- takeaways -->

- CloudWatch : santé. CloudTrail : activité. Config : configuration.
- X-Ray trace les requêtes distribuées.
- Le Health Dashboard signale les problèmes AWS qui vous touchent.

<!-- unit: Gérer et automatiser -->

<!-- goals -->

- Interagir avec AWS par la console, la CLI, les SDK et l'IaC.
- Automatiser infrastructure, exploitation et déploiements.

<!-- concept -->

Tout dans AWS est une API, et console, CLI et SDK ne sont que des façons de l'appeler. Le travail répétable doit passer par du code : CloudFormation et CDK décrivent l'infrastructure, Systems Manager exécute des tâches d'exploitation sur des parcs entiers et les services Code* construisent et déploient le logiciel.

Trusted Advisor boucle la boucle en examinant le compte et en signalant économies, risques et limites.

<!-- example -->

```yaml
# CloudFormation: a versioned, private S3 bucket
Resources:
  ReportsBucket:
    Type: AWS::S3::Bucket
    Properties:
      VersioningConfiguration: {Status: Enabled}
      PublicAccessBlockConfiguration: {BlockPublicAcls: true, BlockPublicPolicy: true,
                                       IgnorePublicAcls: true, RestrictPublicBuckets: true}
```

#### Quelles sont les façons d'interagir avec AWS ?

L'AWS Management Console (web), l'AWS CLI, les SDK pour les langages de programmation, l'infrastructure as code (CloudFormation, CDK) et AWS CloudShell (un terminal dans le navigateur déjà authentifié).

#### Qu'est-ce qu'AWS CloudFormation ?

L'infrastructure as code : on décrit les ressources dans des modèles JSON ou YAML, et CloudFormation les crée, les met à jour et les supprime sous forme de pile, dans le bon ordre.

#### Qu'est-ce que l'AWS Cloud Development Kit (CDK) ?

Un framework pour définir l'infrastructure cloud dans des langages de programmation (TypeScript, Python, Java, C#, Go). Il génère des modèles CloudFormation.

#### Qu'est-ce qu'AWS Systems Manager ?

Un ensemble d'outils d'exploitation pour gérer à grande échelle des serveurs EC2 et sur site : Session Manager, Patch Manager, Run Command, Parameter Store, Automation et inventaire.

#### Que sont AWS CodeCommit, CodeBuild, CodeDeploy et CodePipeline ?

Des outils de CI/CD : CodeBuild compile et teste le code, CodeDeploy automatise les déploiements sur EC2, Lambda, ECS et sur site, CodePipeline orchestre les chaînes de livraison. CodeCommit est un service d'hébergement Git fermé aux nouveaux clients.

#### Qu'est-ce qu'AWS Trusted Advisor ?

Un service qui inspecte votre compte et recommande des améliorations dans cinq catégories : optimisation des coûts, performances, sécurité, tolérance aux pannes et quotas de service. Les plans de support Basic et Developer n'ont que les contrôles essentiels. Business et au-delà ont l'ensemble complet.

<!-- challenge -->

Une équipe crée ses environnements de test en cliquant dans la console, et chacun finit légèrement différent. Que proposez-vous ?

<!-- solution -->

Définir l'environnement dans CloudFormation ou CDK, le stocker dans Git et créer chaque environnement à partir du même modèle avec des paramètres. Déployer les changements par un pipeline plutôt que par la console.

<!-- takeaways -->

- Console, CLI et SDK appellent tous les mêmes API.
- CloudFormation et CDK rendent l'infrastructure reproductible.
- Trusted Advisor contrôle coûts, sécurité, limites et plus.

<!-- unit: Découpler les applications -->

<!-- goals -->

- Choisir entre SQS, SNS et EventBridge.
- Découpler producteurs et consommateurs.

<!-- concept -->

Quand un composant appelle directement un autre, la lenteur de l'un contamine les deux. Les services de messagerie coupent ce lien. Une file garde le travail jusqu'à ce qu'un consommateur soit prêt ; un topic livre chaque message à de nombreux abonnés à la fois ; un bus d'événements route les événements selon leur contenu vers les bonnes cibles, services AWS et SaaS compris.

La différence tient à la livraison : un consommateur par message, tous les abonnés, ou un routage par règles.

<!-- example -->

| Patron | Service |
|---|---|
| Commandes traitées par un groupe de workers | SQS |
| Envoyer une alerte par e-mail, SMS et à une Lambda | SNS |
| Router les événements « commande passée » vers facturation et analytique par règles | EventBridge |

#### Qu'est-ce qu'Amazon SQS ?

Simple Queue Service est une file de messages entièrement gérée qui découple les composants. Les files standard offrent un débit élevé avec une livraison au moins une fois. Les files FIFO garantissent l'ordre et un traitement exactement une fois.

#### Quelle est la différence entre SQS et SNS ?

SQS est une file : les consommateurs récupèrent les messages, chaque message est traité par un seul consommateur. SNS est de la publication/abonnement : un message publié sur un sujet est poussé à tous les abonnés (SQS, Lambda, HTTP, e-mail, SMS). On les combine souvent en éventail (fan-out).

#### Qu'est-ce qu'Amazon EventBridge ?

Un bus d'événements serverless qui achemine les événements des services AWS, d'applications SaaS et de votre propre code vers des cibles selon des règles, et planifie des tâches (EventBridge Scheduler).

<!-- challenge -->

Un service de commandes appelle directement le service d'e-mail ; quand l'e-mail ralentit, le paiement expire. Comment corriger ?

<!-- solution -->

Publier les événements de commande dans une file SQS (ou un topic SNS avec abonnement SQS) et laisser le service d'e-mail les consommer à son rythme. Le paiement se termine dès que le message est stocké.

<!-- takeaways -->

- Les files SQS donnent un consommateur par message.
- SNS diffuse vers de nombreux abonnés.
- EventBridge route les événements par règles.

### Facturation, tarification et support

<!-- unit: Ce qui fait le coût -->

<!-- goals -->

- Citer les principaux facteurs de coût sur AWS.
- Estimer les coûts et bien utiliser l'offre gratuite.

<!-- concept -->

AWS facture surtout trois choses : le temps de calcul, les données stockées et les données qui sortent d'AWS. La plupart des surprises viennent d'en oublier une, comme des instances inactives ou de gros transferts sortants. L'offre gratuite aide à apprendre, dans des limites faciles à dépasser.

Le travail sur les coûts commence avant de construire, par une estimation, et continue ensuite, en supprimant le gaspillage et en engageant l'usage stable.

<!-- example -->

| Facteur de coût | Exemple | Levier |
|---|---|---|
| Calcul | 10 instances 24 h/24 | Bien dimensionner, Savings Plans, arrêter si inactif |
| Stockage | 50 To en S3 Standard | Cycle de vie vers des classes moins chères |
| Transfert sortant | Vidéo servie depuis EC2 | CloudFront, compression |

#### Quels sont les trois facteurs fondamentaux du coût sur AWS ?

Le calcul, le stockage et le transfert de données sortant. Le transfert de données entrant est en général gratuit.

#### Qu'est-ce que l'offre gratuite d'AWS (Free Tier) ?

Des offres pour essayer AWS sans frais dans certaines limites. Elle comprend des offres toujours gratuites (par exemple des requêtes Lambda et du stockage DynamoDB jusqu'à un plafond), des crédits ou offres de 12 mois pour les nouveaux comptes selon le plan du compte, et de courts essais gratuits de certains services. L'usage au-delà des limites est facturé.

#### Qu'est-ce que l'AWS Pricing Calculator ?

Un outil gratuit pour estimer le coût d'une architecture avant de la construire.

#### Comment réduire ses coûts sur AWS ?

Redimensionner les instances, éteindre les ressources inutilisées, utiliser des Savings Plans ou des instances réservées pour les charges stables et Spot pour les charges interruptibles, choisir des classes de stockage moins chères avec des règles de cycle de vie, passer au serverless pour les charges variables, réduire le transfert de données (par exemple avec CloudFront et les points de terminaison de VPC), et suivre les dépenses avec des balises, Budgets et Cost Explorer.

<!-- challenge -->

Le compte Free Tier d'un étudiant a généré une facture de 90 USD. Citez deux causes probables et comment les éviter.

<!-- solution -->

Des ressources hors des limites gratuites (une instance plus grosse, un NAT gateway, une instance RDS restée allumée) ou un usage après la fin des offres de 12 mois. Créer une alerte budgétaire sur un petit montant et supprimer les ressources après les expériences.

<!-- takeaways -->

- Calcul, stockage et transfert sortant font le coût.
- Estimez avec le Pricing Calculator avant de construire.
- L'offre gratuite a des limites ; créez des alertes budgétaires.

<!-- unit: Suivre et maîtriser les dépenses -->

<!-- goals -->

- Analyser et prévoir les dépenses avec Cost Explorer et les exports détaillés.
- Maîtriser et attribuer les coûts avec budgets, tags et facturation consolidée.

<!-- concept -->

On ne maîtrise pas ce qu'on ne voit pas. Cost Explorer montre tendances et prévisions ; les exports détaillés donnent des données ligne à ligne pour vos propres analyses ; les tags attribuent les coûts aux projets et aux équipes. Les budgets ajoutent des alertes, et Compute Optimizer suggère de meilleures tailles selon l'usage réel.

Dans les organisations, la facturation consolidée combine l'usage de tous les comptes, ce qui atteint plus vite les remises de volume et fait profiter toute l'entreprise des engagements.

<!-- example -->

```bash
aws budgets create-budget --account-id 123456789012 --budget '{
  "BudgetName": "data-team-monthly", "BudgetLimit": {"Amount": "5000", "Unit": "USD"},
  "TimeUnit": "MONTHLY", "BudgetType": "COST",
  "CostFilters": {"TagKeyValue": ["user:team$data"]}}'
```

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

<!-- challenge -->

La finance veut le coût AWS mensuel de chaque équipe, mais les équipes partagent des comptes. Que mettez-vous en place ?

<!-- solution -->

Définir un tag `team`, l'exiger sur les ressources (tag policies, SCP ou IaC), l'activer comme cost allocation tag et produire un reporting par tag dans Cost Explorer avec un budget par équipe. Des comptes séparés par équipe sont la solution de plus long terme.

<!-- takeaways -->

- Cost Explorer montre et prévoit les dépenses.
- Tags et comptes attribuent les coûts à leurs propriétaires.
- La facturation consolidée partage les remises entre comptes.

<!-- unit: Support et partenaires -->

<!-- goals -->

- Comparer les plans AWS Support et leur contenu.
- Savoir où trouver de l'aide : re:Post, TAM, Marketplace et partenaires.

<!-- concept -->

L'aide sur AWS se décline par niveaux. Tout le monde a la documentation, la communauté re:Post et les contrôles de base. Les plans payants ajoutent des cas techniques avec des délais de réponse plus courts à mesure que le plan monte, et les niveaux supérieurs ajoutent un Technical Account Manager qui connaît votre environnement.

Au-delà d'AWS, les partenaires et Professional Services fournissent du conseil, et le Marketplace vend des logiciels prêts à tourner sur AWS, facturés via votre compte AWS.

<!-- example -->

| Besoin | Plan ou ressource |
|---|---|
| Apprentissage, pas de production | Basic + re:Post |
| Charge de production, problèmes en heures ouvrées | Developer ou Business |
| Critique pour le métier, réponse rapide 24 h/24 | Business ou Enterprise On-Ramp |
| TAM dédié, systèmes critiques | Enterprise |

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

<!-- challenge -->

Le site de production d'une entreprise tombe à 2 h du matin et elle a le plan Developer. Quel support peut-elle obtenir, et quel plan conviendrait mieux ?

<!-- solution -->

Developer offre un support par e-mail en heures ouvrées pour des conseils généraux, pas pour les cas urgents de production. Business (ou supérieur) ajoute téléphone et chat 24 h/24 avec réponse rapide en cas de production arrêtée.

<!-- takeaways -->

- Les plans diffèrent par délais de réponse et accès.
- Les plans Enterprise incluent un TAM.
- Marketplace et partenaires complètent ce qu'offre AWS.
