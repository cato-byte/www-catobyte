## Modèles d'architecture des données : Kimball, microservices, médaillon et plus

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Modèles d'architecture des données : de Kimball au lakehouse](../../images/data_architecture_patterns_title_img.png)

*Article technique*

## Il n'existe pas de meilleure architecture

Tous les quelques ans, on annonce une nouvelle architecture de données censée remplacer toutes les autres. Inmon a été remplacé par Kimball, l'entrepôt par le data lake, le lake par le lakehouse, l'équipe centrale par le data mesh. En pratique, aucune n'a disparu. La plupart des plateformes que j'ai vues mélangent trois ou quatre de ces idées, parfois volontairement, souvent par accident.

La façon utile de les penser, c'est comme des réponses à des questions précises. Comment intégrer vingt systèmes qui décrivent différemment le même client ? Comment rendre les chiffres faciles pour les analystes ? Comment garder une piste d'audit de chaque changement ? Comment sortir les données de trente microservices sans se coupler à leurs bases ? Comment servir à la fois un rapport nocturne et un modèle de fraude qui doit répondre en 200 millisecondes ? Chaque modèle présenté ici est une bonne réponse à l'une de ces questions et une mauvaise réponse à d'autres.

Je passe en revue les modèles que je rencontre le plus souvent, ce que chacun optimise, où il atteint ses limites et comment ils se combinent. J'utiliserai mon [lakehouse des registres d'entreprises européens](../projects/eu-company-registry.html) comme exemple concret quand c'est utile, y compris une décision sur laquelle je suis revenu.

## Inmon : intégrer d'abord

La Corporate Information Factory de Bill Inmon place au centre un **entrepôt d'entreprise en troisième forme normale**. Toutes les sources sont intégrées dans un modèle unique, normalisé et orienté sujet (client, compte, produit), qui constitue la version unique de la vérité. Les data marts des départements en sont ensuite dérivés.

```
sources ──► staging ──► entrepôt d'entreprise (3FN, intégré, historisé) ──► data marts dépendants ──► BI
```

**Ce qu'il optimise :** la cohérence. Comme tous les marts proviennent du même cœur intégré, la finance et les ventes ne peuvent pas diverger sur ce qu'est un client.

**Où il pèche :** le délai avant de livrer de la valeur. Concevoir un modèle normalisé à l'échelle de l'entreprise prend des mois avant le premier rapport, et chaque nouvelle source oblige à modifier un modèle central dont dépendent de nombreuses équipes. Les modèles normalisés sont en outre difficiles à interroger directement pour les analystes.

On voit encore des cœurs de style Inmon dans les banques et les assurances, et son idée centrale survit dans toute architecture qui possède une couche « intégration » ou « silver ».

## Kimball : modéliser pour les questions

Ralph Kimball a pris le chemin inverse : partir des **processus métier** (prise de commande, facturation, expéditions) et construire des **modèles dimensionnels** que les analystes comprennent. Une table de faits enregistre des mesures à un grain déclaré, entourée de tables de dimension portant le contexte descriptif. C'est le schéma en étoile.

```sql
-- Une ligne par ligne de commande (le grain), jointe à des dimensions conformes
SELECT d.year_month, c.segment, p.category, SUM(f.net_amount) AS revenue
FROM fct_order_lines f
JOIN dim_date d     ON f.order_date_key = d.date_key
JOIN dim_customer c ON f.customer_key   = c.customer_key
JOIN dim_product p  ON f.product_key    = p.product_key
WHERE d.year = 2026
GROUP BY d.year_month, c.segment, p.category;
```

Les marts s'intègrent par des **dimensions conformes** : un seul `dim_customer` et un seul `dim_date` partagés par toutes les tables de faits, planifiés avec la bus matrix. L'historique vit dans les **dimensions à évolution lente**, généralement de type 2 : quand un client change de segment, l'ancienne ligne est clôturée et une nouvelle version insérée, si bien que les ventes de l'an dernier restent attribuées au segment de l'an dernier.

**Ce qu'il optimise :** la facilité d'usage et les performances des requêtes. Les schémas en étoile sont simples à expliquer, les outils BI les comprennent et les moteurs en colonnes les exécutent vite.

**Où il pèche :** l'intégration de sources désordonnées et qui se recouvrent. Kimball suppose qu'on peut conformer les dimensions ; quand vingt systèmes ne s'accordent pas sur les clients, ce travail de conformation doit se faire quelque part, et le modèle dimensionnel n'est pas le meilleur endroit pour conserver l'historique brut et auditable de chaque source.

Kimball n'est pas dépassé. Presque toutes les couches « gold » que j'ai vues dans un lakehouse sont des ensembles de schémas en étoile, même quand personne ne les appelle ainsi. La couche gold de mon projet de registres est une étoile de Kimball : une dimension entreprises, une dimension secteurs et des tables agrégées, avec une couverture par pays explicite.

## Data Vault : intégrer et auditer à grande échelle

Le Data Vault de Dan Linstedt vise la couche d'intégration quand il y a beaucoup de sources changeantes et de fortes exigences d'audit. Il découpe le modèle en trois types de tables :

- Les **hubs** stockent les clés métier uniques (un numéro de client) avec la date de chargement et la source.
- Les **links** stockent les relations entre hubs (le client a passé une commande).
- Les **satellites** stockent les attributs descriptifs et leur historique, un satellite par source ou par fréquence de changement.

Tout est en insertion seule, avec des clés de hachage pour paralléliser les chargements, et entièrement traçable jusqu'à la source. Des marts de consommation sont construits au-dessus, souvent des étoiles de Kimball, parfois avec des tables auxiliaires point-in-time et bridge.

**Ce qu'il optimise :** l'agilité et l'auditabilité. Ajouter une source revient à ajouter des satellites, pas à repenser des tables. Les régulateurs peuvent voir exactement ce que chaque système a dit et quand.

**Où il pèche :** la complexité et le coût des requêtes. Une question simple devient une jointure entre hubs, links et plusieurs satellites, si bien que personne n'interroge directement le vault ; il faut toujours une couche de présentation. Sans automatisation (paquets dbt, générateurs de code), le nombre de tables grimpe vite.

J'ai travaillé sur une plateforme Data Vault chez Corum L'Épargne, et la première version de mon lakehouse de registres était aussi un modèle Data Vault 2.0. Je l'ai remplacé volontairement, et le raisonnement illustre bien le fait de choisir un modèle à partir du problème plutôt que par habitude :

> Le Data Vault est rentable quand plusieurs systèmes décrivent les mêmes clés métier. Dans le projet de registres, aucune clé n'est jamais partagée : un SIRET français et un numéro d'entreprise britannique ne désignent jamais la même société. Chaque hub était une copie renommée de la colonne d'identifiant d'un registre, et chaque requête devenait une jointure à cinq ou six tables, chaque shuffle facturé en calcul serverless. Les registres publient des photos complètes, donc l'historique correspond exactement à ce que produit un merge SCD de type 2, et Delta Lake fournit déjà une piste d'audit (voyage dans le temps, `RESTORE`, Change Data Feed).

J'ai conservé les idées du Data Vault qui méritaient leur place : clés de hachage, `hash_diff` pour détecter les changements, colonnes de source et de lignage, et historique brut en insertion seule en bronze. C'est souvent la bonne issue : reprendre les techniques et laisser de côté la méthodologie complète quand son principal avantage ne s'applique pas.

## Data lakes et lakehouse

Le data lake répondait à une autre question : où tout mettre, à bas coût, y compris les données qu'on ne comprend pas encore ? Le stockage objet (S3, ADLS, GCS) conserve des fichiers bruts de tout format pour une fraction du coût d'un entrepôt, le schéma étant appliqué à la lecture.

Les lakes ont apporté un stockage bon marché et de la souplesse, mais aussi beaucoup de **data swamps** : pas de transactions (les lecteurs voyaient des données à moitié écrites), pas de contrôle de schéma, des requêtes lentes sur des millions de petits fichiers, pas de mises à jour ni de suppressions fiables (un vrai problème pour le RGPD) et une gouvernance faible.

Le **lakehouse** corrige cela avec les formats de table ouverts, **Delta Lake, Apache Iceberg et Apache Hudi**, qui ajoutent un journal de transactions au-dessus de fichiers Parquet : écritures ACID, contrôle et évolution du schéma, voyage dans le temps, `MERGE`, `UPDATE` et `DELETE`. Un catalogue (Unity Catalog, AWS Glue avec Lake Formation, Polaris) transforme les fichiers en tables gouvernées, et plusieurs moteurs (Spark, Databricks SQL, Snowflake, Athena, Trino) peuvent lire les mêmes données.

**Ce qu'il optimise :** une seule copie des données pour la BI, la data science et le machine learning, dans des formats ouverts, avec des garanties proches de celles d'un entrepôt.

**Où il pèche :** il faut toujours concevoir les couches, maintenir les tables (compaction, vacuum, clustering) et gouverner l'accès. Un lakehouse sans discipline de modélisation n'est qu'un marécage plus rapide.

## Médaillon : des couches de raffinement

L'architecture médaillon est la convention de couches du lakehouse :

| Couche | Contenu | Règles typiques |
|---|---|---|
| **Bronze** | Les données brutes telles que reçues, plus des métadonnées de chargement | Insertion seule, transformation minimale, tout reste rejouable |
| **Silver** | Des entités nettoyées, typées, dédupliquées, harmonisées et historisées | Contrôles de qualité, quarantaine, SCD de type 2, une version fiable de chaque entité |
| **Gold** | Des modèles prêts pour le métier : schémas en étoile, agrégats, tables de features | Définitions métier appliquées, optimisé pour la lecture |

Il est important de voir ce qu'est le médaillon et ce qu'il n'est pas. C'est une **convention de couches de raffinement**, pas une technique de modélisation. Silver peut être normalisé, en Data Vault ou simplement composé de tables d'entités propres ; gold est généralement du Kimball. Le médaillon dit où vont les choses, pas comment les modéliser.

Dans mon lakehouse de registres, les couches se présentent ainsi :

```
landing (S3, fichiers bruts par ingest_date)
   │  contrôle de dérive du schéma par rapport à un contrat
   ▼
bronze  toutes les colonnes en STRING + lignage, insertion seule, une table par registre
   │  analyse par source, règles de qualité, quarantaine
   ▼
silver  un modèle canonique des entreprises, MERGE SCD de type 2 par pays et par photo
   │  modélisation dimensionnelle
   ▼
gold    étoile de Kimball (dimensions entreprises et secteurs) + tables agrégées
```

Deux choix méritent d'être copiés. Bronze stocke toutes les colonnes en texte : une valeur invalide ne peut jamais faire échouer un chargement, et silver peut toujours être relancé avec une meilleure analyse. Et silver impose ses propres invariants par des contraintes (statuts valides, `valid_to >= valid_from`, lignes courantes ouvertes), si bien qu'une régression du code ne peut pas écrire un état invalide.

Les erreurs que je vois le plus souvent avec le médaillon : traiter les trois couches comme des copies obligatoires même quand une couche n'apporte rien ; laisser les tableaux de bord lire bronze ou silver directement ; mettre de la logique métier en bronze ; copier des tables entières entre couches à chaque exécution au lieu de traiter de façon incrémentale ; et n'avoir aucun contrat explicite sur ce que garantit chaque couche.

## Microservices et données

Les microservices ont changé l'architecture des données par l'autre bout. Chaque service possède sa base (**une base par service**) et expose ses données par des API et des événements, jamais par des tables partagées. C'est bon pour l'autonomie et la vitesse de déploiement. C'est un défi pour l'analytique, car les données que l'entreprise veut analyser se retrouvent dispersées dans des dizaines de bases privées.

Le raccourci tentant consiste à brancher l'entrepôt sur la base de chaque service et à lire ses tables. Ça marche un mois, puis une équipe renomme une colonne et le pipeline de nuit casse. Les schémas internes sont des détails d'implémentation ; les lire couple la plateforme de données aux entrailles de chaque service.

Les modèles qui fonctionnent :

- La **capture des changements (CDC)** lit le journal de transactions de chaque base (avec Debezium, AWS DMS ou un connecteur géré) et diffuse insertions, mises à jour et suppressions vers Kafka ou le lakehouse, sans toucher au code du service. C'est le moyen le plus rapide de sortir les données des systèmes existants, mais il expose toujours les schémas internes, sauf si un contrat est convenu.
- Les **événements d'intégration** sont des faits métier (`OrderPlaced`, `PaymentFailed`) que les services publient délibérément sous forme de contrats versionnés, séparés de leur modèle de domaine interne. Ils sont plus stables que le CDC et portent un sens métier.
- La **transactional outbox** résout le problème de la double écriture : si un service écrit dans sa base puis publie un événement, l'un peut réussir et l'autre échouer. À la place, le service écrit l'événement dans une table outbox au sein de la même transaction, et le CDC publie les lignes de l'outbox dans le broker.

```
┌──────────── service des commandes ──────────┐
│  BEGIN                                      │
│    INSERT INTO orders ...                   │
│    INSERT INTO outbox (event: OrderPlaced)  │
│  COMMIT                                     │
└───────────────────┬─────────────────────────┘
                    │ le CDC lit les lignes de l'outbox
                    ▼
              topic Kafka : orders.events ──► autres services
                    │
                    ▼
              lakehouse bronze ──► silver ──► gold
```

Deux modèles apparentés apparaissent dans les systèmes événementiels. L'**event sourcing** stocke une entité sous la forme de la suite d'événements qui l'ont modifiée et reconstruit l'état en les rejouant, ce qui donne une piste d'audit parfaite mais complique les requêtes. **CQRS** sépare le modèle d'écriture des modèles de lecture, mis à jour de façon asynchrone à partir des événements, pour faire monter en charge lectures et écritures indépendamment. Pour les transactions qui couvrent plusieurs services, les **sagas** remplacent la validation distribuée en deux phases par une suite de transactions locales avec des actions compensatoires.

Pour un data engineer, la règle pratique est simple : **consommer des contrats publiés (événements ou vues CDC curées), pas des tables internes**, et valider ces contrats dans la CI des producteurs pour que les changements cassants échouent avant d'être livrés.

## Lambda et Kappa : batch et streaming

Quand la faible latence est entrée en jeu, deux architectures se sont affrontées.

L'**architecture Lambda** a deux chemins : une couche batch qui recalcule des vues exactes à partir de tout l'historique, et une couche de vitesse qui traite les événements récents en temps réel, une couche de service fusionnant les deux. Elle offre exactitude et fraîcheur, au prix d'une même logique écrite et maintenue deux fois.

L'**architecture Kappa** garde un seul chemin : tout est flux, stocké dans un journal durable et rejouable (Kafka). Pour corriger un bug ou changer la logique, on rejoue le journal dans une nouvelle version du job. Une seule base de code, mais il faut un traitement de flux solide et une longue rétention.

Aujourd'hui, la Lambda pure est rare. Les moteurs unifiés (Spark Structured Streaming, Flink, Apache Beam) et les formats de table qui acceptent écritures en streaming et en batch sur les mêmes tables rendent pratique une conception de type Kappa, avec des backfills batch depuis le lakehouse au besoin. Avant de choisir l'une ou l'autre, posez la question qui fait économiser le plus : **quelles décisions changent vraiment si les données ont quelques secondes au lieu de quelques heures ?** La détection de fraude et les alertes opérationnelles, oui. La plupart des tableaux de bord, non.

## Data mesh et data fabric

Le **data mesh**, proposé par Zhamak Dehghani, est d'abord une réponse organisationnelle. Les équipes data centrales deviennent des goulots d'étranglement entre de nombreux domaines sources et de nombreux consommateurs ; le mesh transfère donc la responsabilité aux domaines, selon quatre principes : responsabilité par domaine, **données en tant que produit** (avec un responsable, documentées, assorties de garanties de qualité et de SLA), **plateforme en libre-service** et **gouvernance computationnelle fédérée** (des règles globales appliquées automatiquement par la plateforme).

Il fonctionne quand les domaines ont la capacité et la motivation de porter des produits de données et qu'une vraie plateforme existe en dessous. Sans cela, le mesh produit des données fragmentées et incohérentes sous un nom à la mode. Beaucoup d'organisations adoptent la partie la plus utile, des produits de données avec des responsables et des contrats, sans décentralisation complète.

La **data fabric** en est le pendant technologique : métadonnées actives, graphes de connaissances, automatisation et virtualisation pour intégrer des données distribuées derrière une couche d'accès gouvernée. Le mesh demande « à qui est-ce ? » ; la fabric demande « comment tout relier automatiquement ? ». Les deux peuvent coexister.

## Comment les modèles s'articulent

Dans une plateforme moderne, ces modèles sont les couches d'une même conception, pas des concurrents. Une combinaison typique ressemble à ceci :

```
 sources opérationnelles        ingestion                 lakehouse (médaillon)                  consommation
 ───────────────────────   ──────────────────────   ─────────────────────────────────   ──────────────────────
 bases des microservices ──► CDC / événements outbox ─┐
 applications SaaS       ──► connecteurs gérés ───────┼──►  bronze  brut, insertion seule
 fichiers et API         ──► extractions batch ───────┘         │
                                                                ▼
                                                        silver  intégré et historisé    ──► features ML
                                                                │  (normalisé, Data Vault
                                                                │   ou entités SCD2 propres)
                                                                ▼
                                                        gold    étoiles Kimball, agrégats ──► BI, couche sémantique,
                                                                                              reverse ETL, API
          gouvernance sur toutes les couches : catalogue, lignage, contrats, contrôles de qualité, politiques d'accès
```

Les modèles issus des microservices gouvernent la façon dont les données sortent des applications. Le médaillon organise le lakehouse. L'idée d'intégration d'Inmon ou le Data Vault vivent en silver. Kimball vit en gold. Les chemins de streaming alimentent bronze en continu quand la latence compte. Le mesh décide qui possède chaque produit de données en cours de route.

## Comment choisir

Partez des contraintes, pas du schéma le plus récent. Ces questions réduisent vite les options :

| Si votre situation est… | Privilégiez… |
|---|---|
| Peu de sources, les analystes ont vite besoin de chiffres | Des marts Kimball sur un entrepôt cloud ou un lakehouse ; évitez les couches d'intégration lourdes |
| De nombreuses sources qui se recouvrent, de forts besoins d'audit ou réglementaires | Data Vault (ou un cœur normalisé) en silver, Kimball en gold |
| Données structurées, semi-structurées et non structurées, ML et BI sur les mêmes données | Un lakehouse avec formats de table ouverts et couches médaillon |
| Les données viennent de microservices que vous ne maîtrisez pas | Événements d'intégration et outbox quand c'est possible, CDC ailleurs, contrats dans la CI |
| Les décisions perdent leur valeur en quelques secondes | Un chemin streaming (Kafka plus Flink ou Spark streaming) qui alimente les mêmes tables que le batch |
| Une équipe centrale fait goulot et les domaines sont matures | Des produits de données avec responsables et contrats ; un mesh complet seulement avec une vraie plateforme |
| Petite équipe, budget limité | La stack gérée la plus simple qui fonctionne : entrepôt, dbt, un orchestrateur, des tests |

Quelques principes valent quel que soit votre choix :

- **Gardez les données brutes immuables** pour pouvoir retraiter quand la logique change ou que des bugs sont corrigés.
- **Modélisez les couches de consommation pour les questions réellement posées**, au grain le plus fin que vous pouvez vous permettre.
- **Rendez les contrats explicites** entre producteurs, couches et consommateurs.
- **Écrivez la décision.** Un architecture decision record d'une page, avec le contexte, les options et la raison du choix, est ce qui permet de revenir sereinement sur une décision plus tard, comme je l'ai fait avec le Data Vault.

La meilleure architecture est celle que votre équipe peut expliquer, exploiter et faire évoluer. Les modèles sont des outils ; tout l'art consiste à savoir quel problème chacun résout.
