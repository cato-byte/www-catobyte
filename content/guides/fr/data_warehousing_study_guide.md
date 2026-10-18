## Fiche d'étude Data Warehousing

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude data warehousing : environ 200 questions](../../images/data_warehousing_study_guide_title_img.png)

Environ 200 questions d'entretien sur l'entreposage de données : concepts clés, modélisation dimensionnelle avec faits et dimensions, dimensions à évolution lente, modes de chargement, qualité des données, architectures et moteurs d'entrepôt, performances, entrepôts cloud, BI et couche sémantique, avec des exemples SQL. Les réponses sont indépendantes des outils autant que possible, avec des remarques pour Snowflake, Redshift, BigQuery et Databricks.

La fiche suit un parcours d'apprentissage en six étapes. Chaque section est découpée en unités courtes : objectifs d'apprentissage, explication du concept et exemple commenté, puis questions (d'abord de mémorisation, ensuite d'application), un exercice pratique et les points à retenir. Pour **apprendre**, lisez chaque unité du début à la fin. Pour **réviser**, passez en mode révision ou utilisez « Aller aux questions », marquez les réponses à revoir et essayez une révision mixte entre les sections.

<!-- QA -->
<!-- stage: Fondamentaux -->

### Concepts clés

<!-- unit: Ce qu'est un entrepôt -->

<!-- goals -->

- Expliquer ce qu'est un data warehouse et ce qui le distingue d'une base opérationnelle.
- Décrire qui utilise un entrepôt et pourquoi l'analytique a besoin de son propre système.

<!-- concept -->

Les systèmes opérationnels sont faits pour faire tourner l'entreprise : prendre une commande, mettre à jour un stock, enregistrer un paiement, des milliers de fois par minute. Leur demander « comment les ventes ont-elles évolué par région sur trois ans ? » est lent pour eux et pénible pour vous, car les données sont dispersées, écrasées à chaque changement et modélisées pour l'écriture, pas la lecture.
L'entrepôt répond à ce décalage : un lieu où les données de nombreux systèmes sont intégrées, historisées et organisées par sujets métier pour une analyse rapide et cohérente.

<!-- example -->

| Question | Base OLTP | Data warehouse |
|---|---|---|
| Requête type | Récupérer la commande 98123 | CA par mois et région, 3 ans |
| Données | État courant, un système | Historique, systèmes intégrés |
| Modèle | Normalisé pour l'écriture | Dimensionnel pour la lecture |
| Utilisateurs | Applications | Analystes, BI, data science |

#### Qu'est-ce qu'un entrepôt de données (data warehouse) ?

Un référentiel central de données intégrées et historisées issues de nombreuses sources, organisé pour l'analyse et le reporting plutôt que pour les transactions. Définition classique de Bill Inmon : orienté sujet, intégré, historisé et non volatil.

#### Que signifient « orienté sujet, intégré, historisé et non volatil » ?

Orienté sujet : organisé autour des sujets métier (clients, ventes, produits) plutôt que des applications. Intégré : noms, codes et unités cohérents entre les sources. Historisé : conserve l'historique pour analyser les évolutions. Non volatil : les données sont chargées puis lues, pas modifiées sur place par des transactions.

#### Quelle est la différence entre OLTP et OLAP ?

Les systèmes OLTP (traitement transactionnel en ligne) font tourner l'activité : nombreuses petites lectures et écritures concurrentes, schémas normalisés, état courant. Les systèmes OLAP (traitement analytique en ligne) analysent l'activité : grosses lectures et agrégations sur l'historique, schémas dénormalisés ou dimensionnels, surtout des lectures.

#### Pourquoi ne pas faire l'analytique directement sur la base opérationnelle ?

Les requêtes analytiques sont lourdes et ralentiraient l'application ; les schémas opérationnels sont normalisés et difficiles à interroger ; il faut combiner et nettoyer les données de plusieurs systèmes ; l'historique est souvent écrasé dans les systèmes OLTP ; et le contrôle d'accès des analystes diffère de celui de l'application.

#### Qu'est-ce qu'un data mart ?

Un sous-ensemble de l'entrepôt centré sur un domaine ou un département (ventes, finance, marketing), souvent un ensemble de schémas en étoile construits pour un groupe d'utilisateurs précis.

#### Quelle différence entre un data mart dépendant et indépendant ?

Un data mart dépendant est construit à partir de l'entrepôt d'entreprise et partage donc ses définitions avec les autres marts. Un mart indépendant est alimenté directement par les sources : plus rapide à construire, mais il produit des chiffres incohérents entre départements.

#### Qu'est-ce qu'un operational data store (ODS) ?

Un stockage intégré et quasi temps réel des données opérationnelles courantes de plusieurs systèmes, utilisé pour le reporting opérationnel et comme zone intermédiaire. Contrairement à un entrepôt, il conserve peu d'historique et est mis à jour fréquemment.

<!-- challenge -->

Une entreprise lance ses rapports mensuels directement sur la base de l'ERP la nuit. Citez deux problèmes qu'un entrepôt résoudrait.

<!-- solution -->

Les rapports ne concurrenceraient plus l'ERP pour les ressources et n'exigeraient plus de fenêtres nocturnes, et l'historique serait conservé (l'ERP écrase des changements comme la région d'un client). Un entrepôt intègre aussi le CRM et d'autres sources que l'ERP n'a pas.

<!-- takeaways -->

- Les entrepôts intègrent l'historique de nombreux systèmes.
- L'OLTP fait tourner l'entreprise ; l'OLAP l'analyse.
- L'analytique a besoin de son propre système et modèle.

<!-- unit: Couches et composants -->

<!-- goals -->

- Décrire les couches d'un entrepôt et le rôle du staging.
- Comparer ETL et ELT et expliquer les métadonnées de l'entrepôt.

<!-- concept -->

Les données traversent un entrepôt par étapes, chacune avec son rôle. Le staging conserve les extractions source presque telles qu'elles sont arrivées, pour relancer et auditer les chargements. Une couche d'intégration nettoie, harmonise et historise. Les marts de présentation mettent les données en forme pour les consommateurs.
Transformer avant de charger (ETL) ou dans l'entrepôt (ELT) dépend surtout de l'endroit où le calcul coûte le moins ; les entrepôts cloud ont fait de l'ELT la norme. Les métadonnées relient les couches en consignant ce que signifie chaque table et d'où elle vient.

<!-- example -->

```text
sources ─► staging (raw extracts, load metadata)
        ─► core / integration (clean, conformed, historized)
        ─► marts (stars per business process) ─► BI, data science
```

#### Quelle est la différence entre un entrepôt de données et un data lake ?

Un entrepôt stocke des données structurées, modélisées et curées avec un schéma défini à l'écriture, optimisées pour l'analytique SQL. Un data lake stocke des données brutes de tout format (structurées, semi-structurées, non structurées) à bas coût dans un stockage objet, avec un schéma à la lecture, pour la data science et les usages futurs.

#### Qu'est-ce qu'un lakehouse ?

Une architecture qui ajoute les capacités d'un entrepôt (transactions ACID, schémas, gouvernance, SQL rapide) au stockage d'un data lake grâce à des formats de table ouverts comme Delta Lake et Iceberg, pour qu'une seule copie des données serve la BI, la data science et le ML.

#### Quelles sont les couches typiques d'un entrepôt de données ?

Le staging (copies brutes des données sources), une couche d'intégration ou cœur (données nettoyées, harmonisées et historisées ; normalisées ou en Data Vault) et une couche de présentation (marts dimensionnels pour la BI). Les stacks modernes les appellent raw/bronze, staging/silver et marts/gold.

#### Quel est le rôle de la zone de staging ?

Une zone d'atterrissage où les extractions sources sont stockées avec un minimum de modifications, pour pouvoir relancer, retraiter et auditer les chargements sans resolliciter les sources, et pour que les transformations ne s'exécutent pas sur les systèmes opérationnels.

#### Que sont les métadonnées dans un entrepôt ?

Des données sur les données : métadonnées techniques (schémas, types, lignage, heures de chargement), métier (définitions, responsables, glossaire) et opérationnelles (exécutions de jobs, nombres de lignes, erreurs). Elles alimentent les catalogues, l'analyse d'impact et la confiance.

<!-- challenge -->

Une équipe transforme les données dans le script d'extraction et ne charge que les tables finales. Un bug de transformation est découvert. Pourquoi la reprise est-elle difficile, et quelle couche manque ?

<!-- solution -->

Sans couche de staging, les extractions brutes ne sont pas conservées : la logique corrigée ne peut pas être rejouée sur les données d'origine, et les sources ont pu changer depuis. Garder les données source en staging (ou une persistent staging area) et transformer à partir de là.

<!-- takeaways -->

- Staging, intégration et marts ont chacun leur rôle.
- L'ELT transforme dans l'entrepôt ; l'ETL avant.
- Les métadonnées expliquent sens et origine.

<!-- unit: Marts, ODS, lacs et appliances -->

<!-- goals -->

- Distinguer data marts, ODS, data lakes et lakehouses.
- Connaître marts dépendants et indépendants, et les appliances d'entrepôt.

<!-- concept -->

Autour de l'entrepôt gravitent des stockages aux rôles différents. Les data marts se concentrent sur un service ou un processus ; construits depuis un entrepôt commun, ils concordent, construits indépendamment, ils divergent. Un ODS intègre les données opérationnelles courantes pour un usage quasi temps réel. Un data lake stocke à bas coût des données brutes de tout format ; un lakehouse y ajoute des fonctions d'entrepôt.
Les appliances étaient la façon d'exploiter un entrepôt sur site, aujourd'hui largement remplacées par des services cloud.

<!-- example -->

| Stockage | Rôle | Données |
|---|---|---|
| Data mart | Analyse des ventes | Modélisées, un sujet |
| ODS | Écrans du service client | Courantes, intégrées |
| Data lake | Données brutes et ML | Tout format, historique |
| Lakehouse | BI et ML sur une copie | Tables ouvertes avec ACID |

#### Qu'est-ce qu'une source unique de vérité ?

L'objectif que chaque indicateur et chaque entité métier ait une seule définition convenue et un seul jeu de données de référence, pour que les rapports des différents départements concordent. Les dimensions conformes, une couche sémantique et la gouvernance y contribuent.

#### Quelle est la différence entre ETL et ELT ?

L'ETL extrait les données, les transforme dans un moteur séparé, puis les charge dans l'entrepôt. L'ELT charge d'abord les données brutes dans l'entrepôt et les transforme sur place en SQL (souvent avec dbt), en profitant de son calcul élastique. Les entrepôts cloud ont fait de l'ELT la norme.

#### Qui sont les principaux utilisateurs d'un entrepôt de données ?

Les analystes métier et développeurs BI (rapports, tableaux de bord), les data scientists (données d'entraînement, exploration), les équipes finance et opérations (reporting réglementaire et de gestion), les dirigeants (KPI) et, de plus en plus, des applications et des agents IA via des API et des couches sémantiques.

#### Qu'est-ce qu'une appliance d'entrepôt de données ?

Un système matériel et logiciel pré-intégré pour l'entreposage (Teradata, Netezza, Exadata), vendu comme un équipement. Les entrepôts cloud ont largement remplacé les appliances par des services élastiques.

#### Quels sont les principaux composants d'une architecture d'entrepôt ?

Les systèmes sources, les outils d'ingestion et d'ETL/ELT, les couches de stockage (staging, cœur, marts), le moteur de requêtes, une couche sémantique ou d'indicateurs, les outils BI et d'analyse, l'orchestration, la qualité et l'observabilité des données, le catalogue et la gouvernance, et la sécurité.

#### Quelle différence entre un entrepôt de données et une base de données ?

Une base de données est tout stockage organisé de données ; un entrepôt de données est un usage particulier de la technologie des bases, conçu pour des données analytiques, intégrées et historisées, généralement en stockage colonnes et avec des modèles dimensionnels ou en couches.

<!-- challenge -->

Le marketing et la finance ont chacun construit leur mart indépendant depuis les systèmes source, et leurs nombres de clients ne concordent jamais. Que proposez-vous ?

<!-- solution -->

Construire les deux marts depuis une couche d'intégration commune, avec une dimension client conforme et une seule définition de « client », pour en faire des marts dépendants qui concordent par construction.

<!-- takeaways -->

- Un mart sert un sujet ; les marts dépendants concordent.
- Un ODS sert les besoins opérationnels courants.
- Lacs et lakehouses complètent ou remplacent les entrepôts.

<!-- unit: Confiance et ponctualité -->

<!-- goals -->

- Expliquer la source unique de vérité et comment l'atteindre.
- Définir les attentes de latence et les SLA de l'entrepôt.

<!-- concept -->

Un entrepôt n'a de valeur que si on lui fait confiance : une définition et une source par métrique, livrées quand on en a besoin. Les chiffres contradictoires viennent généralement de définitions différentes plutôt que de bugs : brut contre net, date de réservation contre date d'expédition.
La ponctualité est l'autre moitié de la confiance. La latence est le délai avant qu'un événement apparaisse dans les rapports ; les SLA la rendent explicite pour que les consommateurs sachent quand les données sont complètes.

<!-- example -->

| Métrique | Définition (convenue) | SLA |
|---|---|---|
| CA net | Brut − remboursements − remises, par date de commande, EUR | À jour avant 07:00 heure locale, jours ouvrés |
| Client actif | Commande dans les 90 derniers jours | Quotidien |

#### Qu'est-ce que la latence dans le contexte d'un entrepôt ?

Le délai entre un événement dans un système source et sa disponibilité dans les rapports : batch quotidien (heures), micro-batch (minutes) ou streaming (secondes). La bonne latence dépend des décisions métier, pas de la technologie.

#### Que sont les SLA d'un entrepôt de données ?

Des engagements comme « le mart des ventes est rafraîchi avant 7 h, heure locale, les jours ouvrés » ou « 99 % des chargements réussissent », avec supervision et communication en cas de manquement. Ils transforment les pipelines en produits sur lesquels les consommateurs peuvent compter.

#### Qu'est-ce que la modélisation dimensionnelle ?

La technique de Ralph Kimball pour concevoir des schémas analytiques autour des processus métier : des faits (mesures d'événements) entourés de dimensions (contexte descriptif). Elle privilégie la compréhension et les performances des requêtes plutôt que la normalisation.

#### Quelles sont les quatre étapes de la conception dimensionnelle selon Kimball ?

1) Choisir le processus métier (par exemple la prise de commande). 2) Déclarer le grain (ce que représente une ligne de faits). 3) Identifier les dimensions (qui, quoi, où, quand, pourquoi, comment). 4) Identifier les faits (mesures numériques à ce grain).

<!-- challenge -->

Les ventes publient le CA par date de réservation, la finance par date de facture, et les deux ont raison pour leur usage. Comment garder une source unique de vérité ?

<!-- solution -->

Définir explicitement les deux métriques sous des noms distincts (CA réservé, CA facturé), les documenter dans le glossaire, calculer chacune une fois dans des modèles certifiés et afficher les deux là où c'est pertinent.

<!-- takeaways -->

- Les conflits viennent des définitions, pas des bugs.
- Une définition et une source par métrique.
- Les SLA rendent explicites les attentes de fraîcheur.

### Bases de la modélisation dimensionnelle

<!-- unit: Inmon et Kimball -->

<!-- goals -->

- Comparer les approches d'Inmon et de Kimball.
- Décrire les architectures hub-and-spoke et fédérées.

<!-- concept -->

Les deux écoles classiques divergent sur l'endroit de l'intégration. Inmon construit d'abord un entrepôt d'entreprise normalisé et en dérive les marts : intégration forte, démarrage plus lent. Kimball construit des marts dimensionnels par processus métier et les intègre par des dimensions conformes : valeur plus rapide, discipline requise.
La forme organisationnelle suit : le hub-and-spoke place un entrepôt central au milieu ; les modèles fédérés laissent chaque unité garder le sien, reliés par des standards communs.

<!-- example -->

```text
Inmon:   sources ─► EDW (3NF) ─► marts (sales, finance, HR)
Kimball: sources ─► staging ─► star schemas per process, sharing dim_customer, dim_date
```

#### Qu'est-ce que le grain d'une table de faits ?

La définition précise de ce que représente une ligne, par exemple « une ligne par ligne de commande » ou « une ligne par compte et par jour ». Il se déclare avant de choisir dimensions et faits, et toutes les lignes doivent partager le même grain.

#### Pourquoi modéliser au grain le plus fin possible ?

Les données atomiques permettent de répondre à n'importe quelle question par agrégation, y compris aux questions imprévues ; des faits agrégés ne peuvent pas être détaillés. Les agrégats peuvent être ajoutés ensuite pour les performances.

#### Qu'est-ce qu'une table de faits ?

Une table de mesures d'un processus métier, avec des clés étrangères vers les dimensions et des faits numériques (quantité, montant, durée). Elle est généralement étroite et très longue.

#### Qu'est-ce qu'une table de dimension ?

Une table qui décrit le contexte des faits : attributs servant à filtrer, regrouper et libeller (nom, segment et ville du client ; catégorie et marque du produit ; date, mois, indicateur de jour férié). Elle est généralement large et relativement courte.

#### Qu'est-ce qu'un schéma en étoile ?

Une table de faits au centre reliée directement à des tables de dimension dénormalisées, formant une étoile. Il est simple à comprendre, nécessite peu de jointures et fonctionne bien dans les outils BI et les moteurs en colonnes.

```sql
SELECT d.year_month, p.category, SUM(f.net_amount) AS revenue
FROM fct_order_lines f
JOIN dim_date d    ON f.order_date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
WHERE d.year = 2026
GROUP BY d.year_month, p.category;
```

<!-- challenge -->

Une entreprise a besoin de tableaux de bord des ventes dans deux mois, d'autres services suivront. Par quelle approche commencez-vous, et quelle discipline protège l'avenir ?

<!-- solution -->

Kimball : livrer vite l'étoile des ventes, mais construire les dimensions (client, produit, date) conformes dès le premier jour et planifier avec une bus matrix, pour que les marts suivants les réutilisent.

<!-- takeaways -->

- Inmon intègre d'abord ; Kimball livre d'abord des marts.
- Les dimensions conformes gardent les marts Kimball intégrés.
- L'organisation oriente vers hub-and-spoke ou fédéré.

<!-- unit: Data Vault -->

<!-- goals -->

- Décrire hubs, links, satellites et couches du vault dans Data Vault.
- Décider quand Data Vault convient, y compris en cas d'acquisitions fréquentes.

<!-- concept -->

Data Vault est conçu pour le changement. Il sépare clés métier (hubs), relations (links) et historique descriptif (satellites) : une nouvelle source ajoute de nouveaux satellites au lieu de remanier les tables existantes. Tout est en insertion seule avec métadonnées de chargement, ce qui donne un historique d'audit complet.
Le prix, c'est la complexité : beaucoup de tables et de jointures, d'où le besoin de marts et de tables d'aide comme les PIT pour la consommation. Il est rentable avec de nombreuses sources changeantes et de fortes exigences d'audit.

<!-- example -->

```text
raw vault:      hub_customer, sat_customer_crm, sat_customer_billing, link_customer_order
business vault: sat_customer_segment (derived rules)
helpers:        pit_customer (keys of latest satellite rows per snapshot date)
marts:          dim_customer, fct_orders
```

#### Qu'est-ce qu'un schéma en flocon (snowflake) ?

Un schéma en étoile dont les dimensions sont normalisées en plusieurs tables liées (produit → sous-catégorie → catégorie). Il économise un peu de stockage et évite la redondance, mais ajoute des jointures et de la complexité ; Kimball recommande en général d'aplatir les dimensions.

#### Qu'est-ce qu'une clé de substitution (surrogate key) ?

Une clé entière (ou un hachage) sans signification, générée dans l'entrepôt pour identifier une ligne de dimension, indépendante des clés des systèmes sources. Elle permet l'historique (plusieurs lignes par clé naturelle), l'intégration de plusieurs sources et la protection contre les changements de clés sources.

#### Qu'est-ce qu'une clé naturelle (métier) ?

L'identifiant du système source ou du métier (numéro client, SKU, IBAN). Elle est conservée comme attribut de la dimension, à côté de la clé de substitution, pour retracer les lignes jusqu'aux sources.

#### Pourquoi utiliser des clés de substitution plutôt que naturelles dans les faits ?

Les clés naturelles peuvent changer, être réutilisées, entrer en collision entre sources ou être de longues chaînes. Les clés de substitution permettent l'historique SCD de type 2 (les faits pointent vers la version valide à leur date), gardent les faits compacts et autorisent des lignes spéciales comme « inconnu ».

#### Qu'est-ce qu'une dimension conforme ?

Une dimension partagée avec les mêmes clés, attributs et sens entre plusieurs tables de faits et marts (un seul `dim_customer`, un seul `dim_date`), pour pouvoir comparer et combiner les indicateurs de processus différents (drill-across).

#### Qu'est-ce que la bus matrix de l'entrepôt d'entreprise ?

Une grille de planification avec les processus métier en lignes et les dimensions conformes en colonnes, indiquant quelles dimensions chaque processus utilise. Elle guide le développement incrémental de marts qui s'intègrent par les dimensions conformes.

<!-- challenge -->

Après chaque acquisition, le modèle central doit être repensé pour intégrer les données clients de la nouvelle société. Qu'est-ce que Data Vault changerait ?

<!-- solution -->

Les nouvelles sources se chargent dans de nouveaux satellites (et links) rattachés au hub client existant par clés métier ou correspondance ; les tables existantes restent intactes. Les marts combinent ensuite les satellites selon des règles métier convenues.

<!-- takeaways -->

- Hubs, links et satellites séparent clés, relations et historique.
- Les nouvelles sources ajoutent des tables sans remanier les anciennes.
- Marts et tables PIT rendent les vaults utilisables.

<!-- unit: Restitution et architectures alternatives -->

<!-- goals -->

- Situer l'architecture médaillon et les couches sémantiques dans l'entreposage.
- Connaître cubes OLAP, virtualisation et entrepôts temps réel.

<!-- concept -->

Les plateformes modernes gardent les idées de l'entrepôt en changeant la technologie. Les couches médaillon d'un lakehouse correspondent au staging, à l'intégration et aux marts. Les couches sémantiques définissent les métriques une fois pour tous les outils BI, comme le faisaient les cubes OLAP avec des agrégats précalculés.
Deux alternatives échangent le stockage contre autre chose : la virtualisation interroge les sources sur place sans copier, et les entrepôts temps réel ingèrent en continu pour que les rapports aient quelques minutes et non un jour.

<!-- example -->

| Classique | Équivalent moderne |
|---|---|
| Staging | Bronze |
| Couche d'intégration | Silver |
| Data marts | Gold |
| Cube OLAP | Couche sémantique + moteur colonnaire |

#### Qu'est-ce que la dimension date, et pourquoi est-elle importante ?

Une dimension avec une ligne par jour et des attributs comme le jour de la semaine, le mois, le trimestre, les périodes fiscales, les jours fériés et les indicateurs de jour ouvré. Elle rend l'analyse temporelle simple et cohérente et évite une logique de dates complexe dans chaque requête.

#### Pourquoi la clé de la dimension date est-elle souvent au format AAAAMMJJ ?

Un entier comme `20261015` est lisible, se trie correctement, rend l'élagage des partitions intuitif et peut se dériver d'une date sans recherche ; c'est une exception courante aux clés de substitution sans signification.

#### Quelles questions aident à identifier les dimensions ?

Qui (client, employé), quoi (produit, service), où (magasin, région, canal), quand (date, heure), pourquoi (promotion, code motif) et comment (moyen de paiement, mode d'expédition), tels qu'ils apparaissent dans les événements du processus métier.

#### Une table de faits doit-elle avoir des contraintes de clé étrangère ?

Logiquement oui : chaque fait doit référencer une ligne de dimension existante (ou le membre inconnu). Physiquement, beaucoup d'entrepôts n'appliquent pas les contraintes pour les performances de chargement : l'intégrité référentielle est vérifiée par des tests.

#### Qu'est-ce que le drill-across ?

Combiner dans un rapport des mesures de différentes tables de faits (ventes et retours) en interrogeant chacune séparément à un grain commun de dimensions conformes, puis en joignant les résultats, plutôt qu'en joignant directement les faits.

<!-- challenge -->

Trois outils BI calculent la « marge brute » de trois façons différentes. Quelle brique d'architecture corrige cela ?

<!-- solution -->

Une couche sémantique (ou de métriques) qui définit une fois la marge brute, avec sa formule et ses dimensions, consommée par les trois outils, pour que chaque rapport utilise le même calcul.

<!-- takeaways -->

- Les couches médaillon reflètent les couches classiques de l'entrepôt.
- Les couches sémantiques définissent les métriques une fois pour tous.
- Virtualisation et streaming échangent des copies contre de la fraîcheur.

<!-- stage: Modélisation dimensionnelle -->

### Les faits en détail

<!-- unit: Concevoir un modèle dimensionnel -->

<!-- goals -->

- Appliquer les quatre étapes de conception de Kimball.
- Déclarer le grain et choisir les dimensions à partir des questions métier.

<!-- concept -->

La conception dimensionnelle part d'un processus métier, pas des tables source. Une fois le processus choisi, la décision la plus importante est le grain : ce que signifie exactement une ligne. Tout le reste en découle. Les dimensions sont le qui, quoi, où et quand qui décrivent chaque ligne ; les faits sont les nombres mesurés à ce grain.
Choisir le grain le plus fin garde le modèle utile pour des questions que personne n'a encore posées : on peut construire n'importe quelle synthèse à partir du détail, pas l'inverse.

<!-- example -->

```text
1. Process:    order taking
2. Grain:      one row per order line
3. Dimensions: date, customer, product, store, promotion
4. Facts:      quantity, gross_amount, discount_amount, net_amount
```

#### Pourquoi ne pas joindre directement deux tables de faits ?

Leurs grains diffèrent généralement, et les jointures directes produisent des fan-outs et des doubles comptes. Agrégez d'abord chaque fait au grain dimensionnel commun, puis combinez.

#### Qu'est-ce qu'une dimension heure de la journée ?

Une dimension séparée avec une ligne par minute ou seconde de la journée (heure, minute, tranche horaire), utilisée quand l'analyse par heure compte, ce qui garde la dimension date petite.

#### Comment nommer tables et colonnes dans un modèle dimensionnel ?

De façon cohérente et en langage métier : préfixes `fct_` et `dim_` (ou `fact_`/`dim_`), noms au singulier, `_key` pour les clés de substitution, `_id` pour les clés naturelles, unités explicites (`amount_eur`), et pas de jargon des systèmes sources dans les couches de présentation.

#### Quels sont les trois types de tables de faits ?

Les faits transactionnels (une ligne par événement, comme une ligne de commande), les faits en photo périodique (une ligne par entité et par période, comme le solde d'un compte par jour) et les faits en photo cumulative (une ligne par instance de processus, mise à jour à chaque jalon, comme une commande de sa création à sa livraison).

#### Quand utiliser une table de faits en photo périodique ?

Pour mesurer des niveaux ou des états à intervalles réguliers (stocks, soldes, abonnements actifs par mois), quand additionner les transactions serait coûteux ou quand l'état ne se déduit pas des événements.

<!-- challenge -->

Une partie prenante demande une table des « ventes quotidiennes par magasin ». Quel grain construisez-vous, et pourquoi ?

<!-- solution -->

Le grain atomique, une ligne par ligne de commande, avec le quotidien par magasin en agrégat ou en vue par-dessus. La table atomique répond aussi aux questions sur produits, clients et promotions qui suivront.

<!-- takeaways -->

- Partez d'un processus métier.
- Déclarez le grain avant tout.
- Le grain atomique répond aux questions futures.

<!-- unit: Faits, dimensions et schémas -->

<!-- goals -->

- Distinguer tables de faits et tables de dimensions.
- Comparer schémas en étoile et en flocon, et nommer clairement les objets.

<!-- concept -->

Un modèle dimensionnel a deux sortes de tables. Les tables de faits sont longues et étroites : clés plus mesures, une ligne par événement au grain. Les tables de dimensions sont larges et courtes : attributs descriptifs pour filtrer et regrouper.
Disposer les dimensions directement autour du fait donne une étoile, simple pour les utilisateurs et rapide sur les moteurs colonnaires. Normaliser les dimensions en sous-tables donne un flocon, qui économise peu d'espace et ajoute des jointures. Des noms métier clairs complètent un modèle utilisable sans aide.

<!-- example -->

```text
             dim_date
                │
dim_customer ─ fct_order_lines ─ dim_product
                │
             dim_store
```

#### Qu'est-ce qu'une table de faits en photo cumulative ?

Une table de faits avec une ligne par instance d'un processus ayant un début et une fin définis (préparation de commande, demande de prêt, sinistre), avec plusieurs clés de date pour les jalons et des mesures de délai entre eux ; les lignes sont mises à jour à mesure que les jalons surviennent.

#### Qu'est-ce qu'une table de faits sans fait (factless) ?

Une table de faits ne contenant que des clés de dimension et aucune mesure numérique, qui enregistre qu'un événement a eu lieu (un étudiant a assisté à un cours) ou une couverture (quels produits étaient en promotion dans quels magasins), comptée avec `COUNT(*)`.

#### Que sont les faits additifs, semi-additifs et non additifs ?

Les faits additifs s'additionnent sur toutes les dimensions (montant des ventes). Les semi-additifs s'additionnent sur certaines dimensions mais pas sur le temps (solde : on additionne entre comptes, on fait une moyenne ou on prend le dernier dans le temps). Les non additifs ne s'additionnent pas (ratios, pourcentages, prix unitaires) ; stockez plutôt leurs composantes.

#### Comment stocker des ratios comme le pourcentage de marge ?

Stocker les composantes additives (chiffre d'affaires et coût) dans la table de faits et calculer le ratio à la requête (`SUM(revenue - cost) / SUM(revenue)`), car faire la moyenne de pourcentages donne des résultats faux.

#### Qu'est-ce qu'une dimension dégénérée ?

Une clé de dimension stockée dans la table de faits sans table de dimension propre, typiquement un identifiant de transaction comme un numéro de commande ou de facture, utilisé pour regrouper les lignes et pour le drill-through.

<!-- challenge -->

Une dimension produit a été éclatée en tables produit, sous-catégorie, catégorie et département. Les analystes se plaignent des jointures. Que faites-vous ?

<!-- solution -->

Aplatir la hiérarchie dans la dimension produit (catégorie et département en colonnes). Le coût de stockage est négligeable sur un moteur colonnaire, et les requêtes n'ont plus besoin que d'une jointure au lieu de quatre.

<!-- takeaways -->

- Les faits portent les mesures ; les dimensions, le contexte.
- L'étoile est plus simple et souvent plus rapide que le flocon.
- Des noms métier rendent les modèles utilisables.

<!-- unit: Clés -->

<!-- goals -->

- Expliquer clés de substitution et clés naturelles, et pourquoi les faits utilisent les premières.
- Décider comment garantir l'intégrité référentielle.

<!-- concept -->

Les systèmes source identifient les choses par des clés naturelles, qui peuvent changer, être réutilisées ou entrer en collision quand on fusionne des sources. L'entrepôt émet ses propres clés de substitution pour les lignes de dimension, ce qui permet aussi à une clé naturelle d'avoir plusieurs versions historiques.
Les faits pointent vers les dimensions par ces clés de substitution. Chaque fait doit référencer une ligne de dimension existante : les chargements recherchent les clés et se rabattent sur un membre inconnu plutôt que de laisser des orphelins.

<!-- example -->

```text
dim_customer
customer_key | customer_number | segment | valid_from | valid_to
1001         | C-552           | SMB     | 2024-01-01 | 2026-03-31
1874         | C-552           | Mid     | 2026-04-01 | 9999-12-31
fct_orders.customer_key → 1001 for 2025 orders, 1874 for 2026 orders
```

#### Comment gérer des faits de grains différents ?

Les placer dans des tables de faits séparées ; mélanger les grains (montants d'en-tête et de lignes de commande dans une même table) provoque des doubles comptes. Ne répartissez les valeurs d'en-tête sur les lignes que si une règle métier le justifie.

#### Quelle est la clé primaire d'une table de faits ?

Souvent la combinaison de ses clés de dimension et des dimensions dégénérées au grain déclaré, ou une clé de substitution de fait par commodité. Vérifier l'unicité au grain par un test est essentiel.

#### Que sont les tables de faits agrégées ?

Des versions résumées des faits atomiques à un grain plus grossier (ventes par mois et par catégorie) qui accélèrent les requêtes courantes. Elles doivent rester cohérentes avec la table atomique, et les outils BI ou les couches sémantiques peuvent y rediriger les requêtes.

#### Qu'est-ce qu'une table de faits consolidée ?

Une table de faits qui combine des faits de plusieurs processus au même grain (montants réels et budgétés par mois, compte et centre de coût), pratique pour comparer le réel au budget.

<!-- challenge -->

Deux sociétés acquises ont chacune un client `C-100`, deux personnes différentes. Les faits indexés par numéro client les mélangent désormais. Que changez-vous ?

<!-- solution -->

Émettre des clés de substitution dans la dimension client et garder la clé naturelle avec une colonne de système source (`source`, `customer_number`) comme clé métier. Les faits référencent la clé de substitution.

<!-- takeaways -->

- Les clés de substitution sont stables et indépendantes des sources.
- Les clés naturelles restent des attributs avec leur source.
- Les faits doivent toujours référencer une ligne de dimension.

<!-- unit: Dimensions partagées et temporelles -->

<!-- goals -->

- Construire des dimensions conformes et planifier avec une bus matrix.
- Concevoir les dimensions date et heure de la journée.

<!-- concept -->

Dans un entrepôt Kimball, l'intégration passe par des dimensions conformes : les mêmes tables client, produit et date partagées par tous les faits. La bus matrix planifie cela en croisant les processus métier avec les dimensions qu'ils utilisent, et montre quelles dimensions construire d'abord.
La dimension date est la plus partagée de toutes. Elle porte les attributs calendaires et fiscaux pour qu'aucun rapport ne les recalcule. L'heure de la journée, si nécessaire, est une petite dimension séparée.

<!-- example -->

| Processus \ Dimension | Date | Client | Produit | Magasin | Employé |
|---|---|---|---|---|---|
| Commandes | X | X | X | X | |
| Retours | X | X | X | X | |
| Stocks | X | | X | X | |
| Paie | X | | | X | X |

#### Que sont les faits arrivant en retard ?

Des lignes de faits qui arrivent après leur date d'événement (transactions différées). Il faut les charger avec les versions de dimension valides à la date de l'événement, et non les versions courantes, en recherchant les lignes SCD2 avec cette date.

#### Comment modéliser les devises dans les tables de faits ?

Stocker les montants dans la devise de la transaction avec une clé de devise, ainsi que les montants convertis dans une devise de reporting au taux valide à la date de la transaction (depuis une table de taux), pour que les rapports puissent afficher les deux.

#### Comment modéliser les annulations et les retours ?

Soit en lignes négatives dans le même fait transactionnel (sommes simples), soit dans un fait des retours séparé avec son propre grain et ses motifs ; les photos cumulatives peuvent suivre les changements de statut des commandes.

#### Qu'est-ce que la « dimension d'audit » d'une table de faits ?

Une dimension ou un ensemble de colonnes décrivant comment chaque ligne de fait a été chargée (identifiant de lot, horodatage de chargement, fichier source, statut de qualité), utile pour le débogage et le lignage.

#### Quelle taille peuvent atteindre les tables de faits, et comment les gérer ?

Des milliards de lignes sont courants. On les gère par partitionnement par date, clustering sur les filtres courants, compression, chargements incrémentaux, politiques de rétention et agrégats pour les requêtes fréquentes.

<!-- challenge -->

Chaque rapport calcule les trimestres fiscaux avec son propre CASE, et deux divergent. Qu'ajoutez-vous ?

<!-- solution -->

Des attributs fiscaux (année, trimestre, semaine fiscale) dans la dimension date, calculés une fois et joints par tous les faits, pour que les rapports utilisent le même calendrier.

<!-- takeaways -->

- Les dimensions conformes intègrent les marts.
- La bus matrix planifie les dimensions partagées.
- La dimension date centralise la logique calendaire.

<!-- unit: Combiner des faits -->

<!-- goals -->

- Combiner correctement des mesures issues de plusieurs tables de faits.
- Expliquer pourquoi les jointures directes entre faits comptent en double.

<!-- concept -->

Des processus différents produisent des tables de faits différentes, souvent à des grains différents : commandes par ligne, retours par ligne de retour, objectifs par mois. Les joindre directement multiplie les lignes partout où les clés se répètent, et gonfle les totaux.
La méthode sûre est le drill-across : agréger d'abord chaque fait sur un ensemble commun de dimensions conformes, puis combiner les résultats. Ce sont les dimensions conformes qui le permettent.

<!-- example -->

```sql
WITH s AS (SELECT date_key, product_key, SUM(net_amount) AS sales   FROM fct_order_lines GROUP BY 1, 2),
     r AS (SELECT date_key, product_key, SUM(refund_amount) AS returns FROM fct_returns     GROUP BY 1, 2)
SELECT COALESCE(s.date_key, r.date_key) AS date_key, COALESCE(s.product_key, r.product_key) AS product_key,
       s.sales, r.returns
FROM s FULL OUTER JOIN r ON s.date_key = r.date_key AND s.product_key = r.product_key;
```

#### Quand utiliser une photo périodique plutôt que de déduire l'état des transactions ?

Quand calculer l'état à partir de toutes les transactions historiques est coûteux ou complexe (soldes, niveaux de stock, tickets ouverts), ou quand les systèmes sources fournissent des états mais pas d'historique complet des événements.

#### Qu'est-ce qu'une dimension à rôles multiples (role-playing) ?

Une dimension physique utilisée plusieurs fois dans une table de faits avec des sens différents, typiquement la dimension date comme date de commande, d'expédition et de livraison, exposée via des vues ou des alias.

<!-- challenge -->

Un rapport joint `fct_orders` à `fct_shipments` sur `order_id`, et le CA dépasse de 40 % celui de la finance. Pourquoi ?

<!-- solution -->

Les commandes à plusieurs expéditions répètent leur CA une fois par ligne d'expédition. Agréger d'abord chaque fait à la commande (ou aux dimensions partagées), puis joindre les résultats agrégés.

<!-- takeaways -->

- Des faits de grains différents se multiplient en jointure.
- Le drill-across agrège d'abord, combine ensuite.
- Les dimensions conformes rendent le drill-across possible.

### Les dimensions en détail

<!-- unit: Types de tables de faits -->

<!-- goals -->

- Choisir entre faits transactionnels, periodic snapshot et accumulating snapshot.
- Utiliser des factless facts et décider quand un snapshot vaut mieux qu'une dérivation.

<!-- concept -->

Les processus métier mesurent des choses différentes. Les événements (une ligne de commande) conviennent aux faits transactionnels, une ligne par événement. Les niveaux et états (un stock, un solde de compte) conviennent aux periodic snapshots, une ligne par période. Les processus à jalons (commande passée, payée, expédiée, livrée) conviennent aux accumulating snapshots, une ligne par instance mise à jour au fil de l'avancement.
Certains faits n'ont aucune mesure : ils enregistrent seulement que quelque chose s'est produit ou aurait pu se produire.

<!-- example -->

| Processus | Type de fait | Grain |
|---|---|---|
| Ventes | Transactionnel | Ligne de commande |
| Stocks | Periodic snapshot | Produit × magasin × jour |
| Traitement des commandes | Accumulating snapshot | Commande, avec dates de jalons |
| Présence en cours | Factless | Étudiant × cours × date |

#### Qu'est-ce qu'une junk dimension ?

Une dimension qui regroupe plusieurs indicateurs et drapeaux de faible cardinalité (moyen de paiement, emballage cadeau, canal) dans une table de leurs combinaisons, pour éviter de nombreuses minuscules dimensions ou des tables de faits trop larges.

#### Qu'est-ce qu'une mini-dimension ?

Une dimension séparée pour les attributs qui changent vite d'une grosse dimension (tranche d'âge, de revenu ou de score de crédit du client), pour que la dimension principale n'explose pas en lignes SCD2 ; la table de faits référence les deux.

#### Qu'est-ce qu'une dimension outrigger ?

Une dimension référencée par une autre dimension plutôt que par la table de faits (par exemple la date du premier achat d'un client pointant vers la dimension date). Elle est admise avec parcimonie ; trop nombreuses, elles deviennent un flocon.

#### Qu'est-ce qu'une table de pont (bridge) ?

Une table qui résout les relations plusieurs-à-plusieurs entre faits et dimensions, comme des comptes à plusieurs titulaires ou plusieurs diagnostics par visite hospitalière, souvent avec des coefficients de pondération pour ne pas compter deux fois les montants.

#### Comment modéliser les hiérarchies dans les dimensions ?

Les hiérarchies de profondeur fixe (catégorie → sous-catégorie → produit) en colonnes aplaties dans la dimension. Les hiérarchies irrégulières ou de profondeur variable (organigrammes, nomenclatures) avec des clés parent-enfant et une table de pont contenant toutes les paires ancêtre-descendant pour faciliter les cumuls.

<!-- challenge -->

Le métier demande : « combien de temps prend chaque étape du traitement des commandes, et où bloquent-elles ? ». Quel type de fait convient ?

<!-- solution -->

Un accumulating snapshot avec une ligne par commande, une clé de date par jalon (passée, payée, expédiée, livrée) et des mesures de délai entre eux, mis à jour à chaque jalon.

<!-- takeaways -->

- Événements : faits transactionnels. Niveaux : periodic snapshots.
- Processus à jalons : accumulating snapshots.
- Les factless facts enregistrent occurrences ou couverture.

<!-- unit: Mesures et additivité -->

<!-- goals -->

- Classer les faits en additifs, semi-additifs ou non additifs.
- Stocker correctement ratios, devises, annulations et retours.

<!-- concept -->

La façon dont une mesure s'additionne décide de son stockage. Les montants s'additionnent partout ; les soldes s'additionnent entre comptes mais pas entre jours ; ratios et pourcentages ne s'additionnent pas. Stocker les composantes additives et calculer les ratios à la requête garde chaque agrégation juste.
Deux cas métier courants suivent la même logique : les devises, qui exigent montant d'origine et montant converti, et les annulations et retours, qui doivent réduire les totaux d'une façon qui s'additionne encore.

<!-- example -->

```sql
-- margin % computed from additive parts, correct at any level
SELECT category, SUM(revenue) AS revenue, SUM(cost) AS cost,
       (SUM(revenue) - SUM(cost)) / NULLIF(SUM(revenue), 0) AS margin_pct
FROM fct_sales JOIN dim_product USING (product_key)
GROUP BY category;
```

#### Qu'est-ce que la ligne « membre inconnu » ?

Une ligne spéciale de dimension (souvent de clé de substitution `-1` ou `0`) utilisée quand la dimension d'un fait est manquante ou pas encore connue, pour que les faits ne disparaissent pas dans les jointures internes et que le problème soit visible dans les rapports.

#### Qu'est-ce qu'une dimension réduite (shrunken) ?

Un sous-ensemble des lignes ou colonnes d'une dimension utilisé pour des faits agrégés à un grain supérieur, comme une dimension mois dérivée de la dimension date ou une dimension catégorie dérivée des produits.

#### Qu'est-ce qu'une dimension à évolution lente ?

Une dimension dont les attributs changent dans le temps de façon imprévisible (un client déménage, un produit change de catégorie), ce qui exige une politique pour savoir si et comment conserver l'historique.

#### Qu'est-ce qu'une dimension statique ?

Une dimension dont le contenu ne vient pas d'une source et change rarement, comme la dimension date, les tables de codes de statut ou les devises, générée une fois ou maintenue manuellement.

<!-- challenge -->

Un tableau de bord fait la moyenne d'une colonne stockée `margin_pct` sur les produits et affiche une marge que le directeur financier conteste. Qu'est-ce qui ne va pas ?

<!-- solution -->

Le pourcentage de marge n'est pas additif ; faire la moyenne de ratios ignore le poids du CA. Stocker CA et coût, et calculer la marge à partir de leurs sommes au niveau choisi.

<!-- takeaways -->

- L'additivité décide de l'agrégation des mesures.
- Stockez les composantes ; calculez les ratios à la requête.
- Gardez montants en devise d'origine et convertis.

<!-- unit: Grain, clés et dimensions dégénérées -->

<!-- goals -->

- Garder un grain par table de faits et définir sa clé.
- Utiliser dimensions dégénérées et d'audit, et charger les faits tardifs.

<!-- concept -->

Le grain d'une table de faits est une promesse que chaque ligne doit tenir. Mélanger montants d'en-tête et montants de ligne de commande dans une table fausse les sommes. Les identifiants comme le numéro de commande restent dans le fait comme dimensions dégénérées, sans table propre, et forment avec les clés de dimension la clé du fait.
Les faits doivent aussi s'expliquer : des colonnes d'audit enregistrent comment chaque ligne a été chargée, et les faits tardifs doivent arriver dans la bonne période avec les versions de dimension valides au moment où ils se sont produits.

<!-- example -->

```text
fct_order_lines
  order_number (degenerate), line_number, date_key, customer_key, product_key,
  quantity, net_amount,
  batch_id, loaded_at, source_system          ← audit
key: (order_number, line_number)
```

#### Qu'est-ce qu'un attribut « type 1 » dans une dimension mixte ?

Les dimensions peuvent mélanger les politiques par attribut : certaines colonnes sont écrasées (type 1, corrections), d'autres historisées (type 2, changements significatifs). On décide attribut par attribut avec les utilisateurs métier.

#### Comment gérer des données clients venant de plusieurs systèmes ?

Rapprocher et fusionner les enregistrements dans une dimension client conforme avec une clé maître (issue de la gestion des données de référence ou de règles de rapprochement sur e-mails, identifiants, noms), conserver les clés sources comme attributs ou dans une table de correspondance, et définir des règles de survivance pour les attributs en conflit.

#### Qu'est-ce que la gestion des données de référence (MDM) ?

Des processus et outils qui créent et maintiennent une version unique et faisant autorité des entités clés (clients, produits, fournisseurs) entre systèmes, et qui alimentent les dimensions conformes.

#### Qu'est-ce qu'un « attribut conforme » ?

Un attribut ayant le même nom, le même sens et les mêmes valeurs autorisées partout où il apparaît, comme un code pays standard ou une liste de catégories produit, permettant un filtrage cohérent entre marts.

#### Comment gérer des attributs multivalués comme les centres d'intérêt d'un client ?

Avec une table de pont entre la dimension et une dimension de groupe ou d'attribut, ou en stockant une colonne tableau quand le moteur le permet et que les requêtes peuvent la déplier ; évitez d'encoder plusieurs valeurs dans une chaîne séparée par des virgules.

<!-- challenge -->

Les frais de port sont connus par commande, mais la table de faits est au grain ligne de commande. Les analystes les additionnent et obtiennent des totaux gonflés. Quelles options avez-vous ?

<!-- solution -->

Garder les frais de port dans un fait séparé au grain commande, ou les répartir sur les lignes (par exemple au prorata du montant) pour qu'ils s'additionnent correctement au grain ligne. Ne jamais répéter la valeur de la commande sur chaque ligne.

<!-- takeaways -->

- Un grain par table de faits.
- Les dimensions dégénérées gardent les ID de transaction dans le fait.
- Colonnes d'audit et gestion des faits tardifs rendent les faits fiables.

<!-- unit: Faits volumineux et agrégés -->

<!-- goals -->

- Gérer des tables de faits de plusieurs milliards de lignes.
- Utiliser des tables de faits agrégées et consolidées.

<!-- concept -->

Les tables de faits grandissent sans fin. Partitionner par date et regrouper sur les filtres courants fait lire aux requêtes une petite partie seulement, et les chargements incrémentaux gardent le traitement proportionnel aux nouvelles données.
Les agrégats échangent stockage contre vitesse : une copie résumée à un grain plus grossier répond vite aux questions fréquentes, tant qu'elle est reconstruite depuis les faits atomiques. Les faits consolidés vont dans l'autre sens et combinent des processus à un grain commun, comme réalisé et budget par mois, pour faciliter la comparaison.

<!-- example -->

```sql
CREATE TABLE agg_sales_month_category AS
SELECT d.year_month, p.category, SUM(f.net_amount) AS net_amount, SUM(f.quantity) AS quantity
FROM fct_order_lines f
JOIN dim_date d USING (date_key) JOIN dim_product p USING (product_key)
GROUP BY 1, 2;
```

#### Qu'est-ce qu'une « vue courante » d'une dimension SCD2 ?

Une vue filtrant `is_current = true` qui donne une ligne par clé naturelle avec les attributs du jour, utilisée par les analystes qui n'ont pas besoin de l'historique et pour un reporting de type 1.

#### Quels sont les types de SCD ?

Type 0 : ne change jamais (on garde l'original). Type 1 : écrasement, pas d'historique. Type 2 : une nouvelle ligne par changement avec dates de validité. Type 3 : une colonne « valeur précédente ». Type 4 : l'historique dans une table séparée (mini-dimension ou table d'historique). Type 6 : hybride des types 1, 2 et 3 (colonnes de valeur courante sur toutes les lignes plus lignes d'historique). Type 7 : double clé pour joindre aux lignes courantes ou historiques.

#### Comment fonctionne la SCD de type 2 ?

Quand un attribut suivi change, la ligne courante est clôturée (date de fin renseignée, indicateur courant à faux) et une nouvelle ligne est insérée avec une nouvelle clé de substitution, les nouvelles valeurs, une date de début et une date de fin ouverte. Les faits référencent la clé de substitution valide à leur date.

| customer_key | customer_id | city     | valid_from | valid_to   | is_current |
|---|---|---|---|---|---|
| 101 | C-42 | Lyon       | 2024-01-01 | 2026-03-31 | false |
| 187 | C-42 | Bordeaux   | 2026-04-01 | 9999-12-31 | true  |

<!-- challenge -->

La finance compare les ventes réelles mensuelles au budget, qui n'existe que par mois et catégorie. Comment modéliser ?

<!-- solution -->

Un fait consolidé au grain mois × catégorie avec des colonnes réalisé (agrégé depuis les ventes atomiques) et budget, utilisant des dimensions date et produit conformes (une dimension produit réduite au niveau catégorie).

<!-- takeaways -->

- Partitionnez et regroupez les gros faits ; chargez en incrémental.
- Les agrégats accélèrent les questions fréquentes.
- Les faits consolidés comparent des processus à un grain commun.

### Dimensions à évolution lente

<!-- unit: Dimensions spécialisées -->

<!-- goals -->

- Utiliser les dimensions role-playing, junk, mini, outrigger, réduites et statiques.
- Séparer les attributs qui changent vite de ceux qui changent lentement.

<!-- concept -->

Les vrais modèles ont besoin de quelques motifs au-delà de la dimension de base. Une dimension date peut jouer plusieurs rôles dans un fait. Les indicateurs épars se regroupent dans une junk dimension au lieu d'encombrer le fait. Les attributs qui changent trop vite pour être historisés dans une grosse dimension passent dans une mini-dimension. Certaines dimensions en référencent d'autres, sont des versions réduites pour les agrégats ou sont générées plutôt que chargées.
Chaque motif vise à garder le fait étroit et les dimensions gérables.

<!-- example -->

```text
fct_orders: order_date_key, ship_date_key, delivery_date_key → dim_date (role-playing)
            order_flags_key → dim_order_flags (gift_wrap, express, coupon_used) (junk)
            customer_key → dim_customer (SCD2: segment)
            customer_profile_key → dim_customer_profile (age band, income band) (mini)
```

#### Comment implémenter une SCD de type 2 en SQL ?

Détecter les lignes modifiées en comparant un hachage des attributs suivis entre le staging et les lignes courantes de la dimension, clôturer les lignes modifiées et insérer les nouvelles versions (ainsi que les nouvelles clés). Beaucoup de plateformes le font en un seul `MERGE` avec l'astuce de l'union, ou avec des outils comme les snapshots dbt.

```sql
-- 1) clôturer les lignes dont les attributs suivis ont changé
UPDATE dim_customer d
SET valid_to = CURRENT_DATE - 1, is_current = false
FROM stg_customer s
WHERE d.customer_id = s.customer_id AND d.is_current
  AND d.attr_hash <> s.attr_hash;

-- 2) insérer les nouvelles versions et les nouveaux clients
INSERT INTO dim_customer (customer_id, city, segment, attr_hash, valid_from, valid_to, is_current)
SELECT s.customer_id, s.city, s.segment, s.attr_hash, CURRENT_DATE, DATE '9999-12-31', true
FROM stg_customer s
LEFT JOIN dim_customer d ON d.customer_id = s.customer_id AND d.is_current
WHERE d.customer_id IS NULL;
```

#### Pourquoi une date de fin à 9999-12-31 plutôt que NULL ?

Elle simplifie les requêtes « valide à la date X » avec `BETWEEN` et évite de gérer les `NULL` dans les jointures ; certaines équipes préfèrent `NULL` plus un indicateur courant. L'important est d'être cohérent.

#### Comment joindre des faits à une dimension SCD2 à une date donnée ?

Au chargement des faits, chercher la ligne de dimension dont la période de validité contient la date de l'événement : `ON f.customer_id = d.customer_id AND f.event_date >= d.valid_from AND f.event_date < d.valid_to`, et stocker cette clé de substitution dans le fait.

#### Qu'est-ce que la SCD de type 1, et quand convient-elle ?

L'écrasement des attributs par les nouvelles valeurs, sans historique. Elle convient aux corrections (une faute de frappe) et aux attributs dont l'historique n'importe pas pour l'analyse.

#### Qu'est-ce que la SCD de type 3, et pourquoi est-elle rare ?

L'ajout d'une colonne contenant la valeur précédente (`previous_region`) pour comparer l'affectation actuelle et la précédente. Elle ne garde qu'un niveau d'historique, d'où un usage limité à des analyses de réorganisation.

#### Qu'est-ce que la SCD de type 6 ?

Un hybride où la dimension conserve des lignes d'historique de type 2 et aussi des colonnes « courantes » de type 1 mises à jour sur toutes les lignes de la même clé naturelle, pour rapporter les faits à la fois tels qu'ils étaient et avec les valeurs d'aujourd'hui.

#### Quels problèmes la SCD2 pose-t-elle sur les grosses dimensions ?

L'explosion du nombre de lignes quand les attributs changent souvent, des jointures plus lentes et une logique temporelle complexe. Parades : ne suivre que les attributs significatifs, déplacer les attributs volatils dans des mini-dimensions et utiliser des comparaisons par hachage pour détecter les changements.

<!-- challenge -->

Une table de faits a 12 colonnes d'indicateurs oui/non rarement utilisées qui alourdissent la table. Que faites-vous ?

<!-- solution -->

Créer une junk dimension avec une ligne par combinaison d'indicateurs observée, remplacer les 12 colonnes par une clé et garder les indicateurs disponibles comme attributs descriptifs.

<!-- takeaways -->

- Le role-playing réutilise une dimension pour plusieurs sens.
- Les junk dimensions absorbent les indicateurs divers.
- Les mini-dimensions isolent les attributs qui changent vite.

<!-- unit: Hiérarchies et plusieurs-à-plusieurs -->

<!-- goals -->

- Modéliser hiérarchies fixes et irrégulières.
- Résoudre les relations plusieurs-à-plusieurs avec des tables de pont.

<!-- concept -->

Les dimensions contiennent souvent des hiérarchies. Les hiérarchies fixes, aux niveaux connus, s'aplatissent en colonnes. Les irrégulières ou récursives, comme les organigrammes, demandent plus de structure, souvent un pont qui liste chaque paire ancêtre-descendant.
Les relations plusieurs-à-plusieurs, comme des comptes à plusieurs titulaires ou des clients aux intérêts multiples, exigent aussi des ponts. Des poids sur les lignes du pont permettent de répartir les mesures sans double comptage.

<!-- example -->

```text
bridge_account_holder (account_key, customer_key, weight)
  A1, C1, 0.5
  A1, C2, 0.5
fct_balances.account_key → bridge → dim_customer   (SUM(balance * weight) per customer)
```

#### Comment gérer un changement de dimension appris tardivement ?

Si l'on apprend aujourd'hui qu'un changement a eu lieu le mois dernier, on insère la version avec sa vraie date de début, on ajuste la date de fin de la ligne précédente et, éventuellement, on rattache à la nouvelle clé les faits survenus après le changement ; c'est pourquoi certaines équipes préfèrent les jointures temporelles au moment de la requête.

#### Qu'est-ce qu'un hash diff, et pourquoi l'utiliser ?

Un hachage (MD5, SHA) des attributs suivis concaténés, stocké sur chaque ligne, pour que la détection des changements soit une seule comparaison au lieu de comparer de nombreuses colonnes, avec une gestion sûre des nulls.

#### Comment les snapshots dbt implémentent-ils la SCD2 ?

La configuration du snapshot définit la clé unique et une stratégie (`timestamp` avec une colonne de mise à jour, ou `check` qui compare des colonnes) ; chaque exécution compare la source à la table de snapshot, clôture et insère des lignes, et ajoute `dbt_valid_from` et `dbt_valid_to`.

<!-- challenge -->

Les comptes joints ont deux titulaires, et le solde par client compte deux fois chaque solde joint. Comment publier un résultat juste ?

<!-- solution -->

Utiliser un pont avec des poids de répartition (0,5 chacun, ou selon la quote-part) et sommer solde × poids par client. N'afficher des totaux non pondérés que dans les rapports qui demandent explicitement « l'exposition par titulaire ».

<!-- takeaways -->

- Aplatissez les hiérarchies fixes ; pontez les irrégulières.
- Les ponts résolvent les relations plusieurs-à-plusieurs.
- Les poids évitent le double comptage.

<!-- unit: Intégrer et harmoniser les dimensions -->

<!-- goals -->

- Fusionner les données clients de plusieurs systèmes en une dimension.
- Utiliser membres inconnus, MDM et attributs conformes.

<!-- concept -->

Une dimension client construite depuis CRM, facturation et support doit décider quels enregistrements décrivent le même client et quelles valeurs l'emportent. La gestion des données maîtres fournit le rapprochement et un golden record ; sans elle, l'entrepôt en fait lui-même une version plus simple.
Deux petites conventions gardent le résultat utilisable : une ligne de membre inconnu pour les faits dont la dimension manque, pour que rien ne disparaisse des jointures, et des attributs conformes qui signifient la même chose partout.

<!-- example -->

```text
dim_customer
customer_key | master_id | crm_id | billing_id | segment | country
-1           | -1        | n/a    | n/a        | Unknown | Unknown   ← unknown member
1874         | M-552     | C-552  | B-9917     | Mid     | ES
```

#### Comment tester une dimension SCD2 ?

Vérifier que chaque clé naturelle a exactement une ligne courante, que les périodes de validité ne se chevauchent pas et ne laissent pas de trous, que `valid_from < valid_to`, que les clés de substitution sont uniques et que les clés de substitution des faits existent dans la dimension.

#### Qu'est-ce qu'une SCD2 à l'horodatage par rapport à une granularité journalière ?

Certaines dimensions suivent les changements à la précision de l'horodatage (plusieurs changements par jour), d'autres au jour (dernière valeur de la journée). Choisissez selon la façon dont les faits sont rapprochés ; la granularité journalière est plus simple et suffit généralement.

#### Peut-on rattacher des faits à de nouvelles versions de dimension ?

Normalement non : les faits gardent la version valide au moment où ils ont eu lieu. Pour un reporting « à la date d'aujourd'hui », joignez par la clé naturelle à la ligne courante ou utilisez les colonnes de valeur courante du type 6.

#### Qu'est-ce qu'un chargement complet par rapport à un chargement incrémental ?

Un chargement complet recharge toutes les données à chaque exécution (simple, coûteux, adapté aux petites tables). Un chargement incrémental ne traite que les données nouvelles ou modifiées depuis la dernière exécution (par horodatage, séquence ou CDC), ce qui est indispensable pour les grosses tables.

<!-- challenge -->

5 % des ventes n'ont pas de client correspondant car la synchro CRM a du retard. Les rapports par client perdent silencieusement ces ventes. Corrigez.

<!-- solution -->

Rattacher les faits sans correspondance au membre inconnu (ou créer des inferred members avec la clé naturelle) pour garder des totaux complets, et mettre à jour la clé quand le client arrive. Surveiller la part de clés inconnues.

<!-- takeaways -->

- Fusionnez les sources en une dimension client conforme.
- Les membres inconnus évitent la disparition des faits.
- Les attributs conformes ont partout le même sens.

### Alimentation de l'entrepôt

<!-- unit: Types de SCD -->

<!-- goals -->

- Expliquer les SCD de type 0, 1, 2, 3 et 6.
- Choisir une politique de changement par attribut.

<!-- concept -->

Les attributs de dimension changent : les clients déménagent, les produits sont reclassés. Chaque attribut exige une décision : les rapports doivent-ils voir l'historique ou seulement la valeur courante ? Le type 1 écrase, donc tout l'historique suit la valeur du jour. Le type 2 garde des versions, donc les faits restent liés à ce qui était vrai au moment où ils se sont produits. Le type 3 garde une valeur précédente ; le type 6 combine historique et colonnes courantes.
Le choix se fait par attribut, donc la plupart des dimensions mêlent les politiques.

<!-- example -->

| Attribut | Politique | Pourquoi |
|---|---|---|
| Correction d'orthographe du nom | Type 1 | Correction, pas besoin d'historique |
| Segment client | Type 2 | Les ventes doivent rester sur l'ancien segment |
| Région précédente (réorganisation ponctuelle) | Type 3 | Comparer ancienne et nouvelle |
| Date de naissance | Type 0 | Ne change jamais |

#### Qu'est-ce que la capture des changements (CDC) ?

La capture des insertions, mises à jour et suppressions d'une base source, typiquement en lisant son journal de transactions (binlog, WAL, redo log) avec des outils comme Debezium, DMS, GoldenGate ou Fivetran, puis leur application dans l'entrepôt.

#### Pourquoi préfère-t-on le CDC fondé sur les journaux à l'extraction par horodatage ?

Il capture tous les changements, y compris les suppressions, ne dépend pas de la bonne mise à jour de `updated_at` par les applications, charge peu la source et préserve l'ordre des changements.

#### Comment charger une dimension ?

Extraire et nettoyer les enregistrements sources, dédupliquer par clé naturelle, générer ou retrouver les clés de substitution, appliquer la politique SCD par attribut, ajouter le membre inconnu, et lancer des tests d'unicité des clés naturelles courantes.

#### Comment charger une table de faits ?

Extraire les transactions au grain déclaré, retrouver les clés de substitution des dimensions (à la date pour la SCD2, membre inconnu si absent), calculer les mesures dérivées, et insérer ou fusionner de façon idempotente dans la table de faits, généralement partitionnée par date.

#### Dans quel ordre alimente-t-on un entrepôt ?

D'abord les dimensions, puis les faits, pour que les faits trouvent leurs clés de substitution. Les membres de dimension arrivant en retard sont gérés par des membres inférés ou des lignes inconnues, corrigés ensuite.

#### Qu'est-ce qu'un membre inféré ?

Une ligne de dimension provisoire créée quand un fait arrive avec une clé naturelle encore absente de la dimension, avec la clé naturelle et des attributs par défaut, mise à jour quand les vraies données arrivent.

<!-- challenge -->

Les responsables commerciaux veulent les ventes de l'an dernier par la région du client à l'époque, mais aussi par sa région actuelle. Quelle approche SCD permet les deux ?

<!-- solution -->

Le type 2 sur la région pour les versions historiques, plus une colonne de type 1 `current_region` sur chaque version (type 6), pour regrouper selon l'une ou l'autre.

<!-- takeaways -->

- Choisissez une politique de changement par attribut.
- Le type 2 garde l'historique ; le type 1 écrase.
- Le type 6 offre ensemble vue historique et vue courante.

<!-- unit: Implémenter le type 2 -->

<!-- goals -->

- Implémenter un SCD2 avec SQL, hash diffs et snapshots dbt.
- Choisir dates de validité, indicateurs de version courante et granularité.

<!-- concept -->

Un chargement SCD2 compare les enregistrements entrants aux versions courantes. Quand des attributs suivis changent, il clôt la ligne courante et insère une nouvelle ligne avec une nouvelle clé de substitution. Hacher les attributs suivis ramène la détection de changement à une seule comparaison.
Des conventions simplifient les requêtes : une date de fin lointaine plutôt que `NULL`, un indicateur de version courante et une vue des lignes courantes. Suivre la validité au jour ou à l'horodatage dépend de la fréquence des changements.

<!-- example -->

```sql
-- close changed current rows
UPDATE dim_customer d SET valid_to = s.change_date - 1, is_current = false
FROM stg_customer s
WHERE d.customer_number = s.customer_number AND d.is_current AND d.hash_diff <> s.hash_diff;
-- insert new versions
INSERT INTO dim_customer (customer_number, segment, region, hash_diff, valid_from, valid_to, is_current)
SELECT s.customer_number, s.segment, s.region, s.hash_diff, s.change_date, DATE '9999-12-31', true
FROM stg_customer s
LEFT JOIN dim_customer d ON d.customer_number = s.customer_number AND d.is_current
WHERE d.customer_number IS NULL OR d.hash_diff <> s.hash_diff;
```

#### Comment rendre les chargements de l'entrepôt idempotents ?

Traiter des plages de dates explicites, supprimer et réinsérer les partitions concernées ou utiliser `MERGE` sur les clés, éviter les ajouts aveugles, utiliser des clés de substitution déterministes ou des recherches stables, et concevoir les jobs pour qu'une relance produise le même résultat.

#### Qu'est-ce qu'un upsert, et comment le faire ?

Insérer les nouvelles lignes et mettre à jour les existantes en une seule opération, typiquement avec `MERGE` (Snowflake, BigQuery, Databricks, SQL Server, Postgres 15+) ou `INSERT … ON CONFLICT DO UPDATE` (PostgreSQL).

```sql
MERGE INTO fct_orders t
USING stg_orders s ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET status = s.status, amount = s.amount, updated_at = s.updated_at
WHEN NOT MATCHED THEN INSERT (order_id, customer_key, status, amount, updated_at)
  VALUES (s.order_id, s.customer_key, s.status, s.amount, s.updated_at);
```

#### Comment gérer les suppressions dans les sources ?

Avec les événements de suppression du CDC ou en comparant des extractions complètes pour trouver les clés disparues ; puis supprimer physiquement, ou supprimer logiquement avec un indicateur `is_deleted` et la date de suppression pour garder l'historique, selon les besoins métier et de conformité.

#### Qu'est-ce qu'un watermark dans un chargement incrémental ?

La valeur d'horodatage ou de séquence la plus élevée traitée lors de la dernière exécution, stockée dans une table de contrôle et utilisée pour sélectionner les nouvelles lignes la fois suivante ; utilisez une fenêtre de recouvrement pour attraper les lignes validées tardivement, puis dédupliquez.

#### Qu'est-ce qu'un backfill ?

Le retraitement de périodes passées, par exemple après une correction de bug ou l'ajout d'une colonne. Les pipelines doivent accepter des plages de dates en paramètre et écrire de façon idempotente pour que les backfills soient sûrs.

#### Que sont les contrôles de rapprochement ?

Des comparaisons entre la source et l'entrepôt (nombres de lignes, sommes de montants, clés distinctes par jour) pour prouver que les chargements sont complets et corrects, souvent lancées automatiquement après chaque chargement.

#### Qu'est-ce qu'une table de contrôle en ETL ?

Une table qui stocke les métadonnées de chaque exécution d'un pipeline : watermarks, identifiants de lot, heures de début et de fin, nombres de lignes, statut et erreurs, utilisée pour le chargement incrémental, les relances et la supervision.

<!-- challenge -->

Une dimension SCD2 crée chaque jour une nouvelle version pour la plupart des clients, alors que rien de visible ne change. Quelle est la cause probable ?

<!-- solution -->

Le hash inclut un attribut qui change chaque jour (un `last_login` ou un horodatage de chargement) ou des valeurs non normalisées (espaces finaux, casse). Ne hacher que les attributs métier suivis, normalisés ; passer les volatils en type 1 ou dans une table séparée.

<!-- takeaways -->

- Le SCD2 clôt les anciennes lignes et insère de nouvelles versions.
- Les hash diffs rendent la détection de changement bon marché.
- Dates de fin lointaines et indicateurs courants simplifient les requêtes.

<!-- unit: Utiliser et maintenir un SCD2 -->

<!-- goals -->

- Retrouver la bonne version de dimension lors du chargement des faits.
- Gérer changements tardifs, grosses dimensions et tests.

<!-- concept -->

L'historique n'est utile que si les faits pointent vers la bonne version. Les chargements de faits cherchent la version dont la plage de validité contient la date de l'événement ; le reporting « à aujourd'hui » passe par la vue courante plutôt que de réécrire les faits.
Avec le temps, le SCD2 apporte ses propres problèmes : changements qui arrivent en retard et doivent être insérés dans le passé, dimensions qui grossissent trop vite, et erreurs subtiles comme des plages qui se chevauchent. Des tests sur la structure de la dimension en attrapent la plupart.

<!-- example -->

```sql
-- each natural key: exactly one current row, no overlapping ranges
SELECT customer_number FROM dim_customer GROUP BY 1 HAVING SUM(CASE WHEN is_current THEN 1 ELSE 0 END) <> 1;
SELECT a.customer_number FROM dim_customer a JOIN dim_customer b
  ON a.customer_number = b.customer_number AND a.customer_key < b.customer_key
 AND a.valid_from <= b.valid_to AND b.valid_from <= a.valid_to;
```

#### Quelle différence entre ingestion push et pull ?

Pull : l'entrepôt extrait des sources selon un planning (requêtes, API). Push : les sources envoient les données sous forme d'événements ou de fichiers (flux CDC, webhooks, dépôts de fichiers). Le push réduit la latence et la charge sur les sources ; le pull est plus simple à piloter.

#### Comment charger des données d'applications SaaS ?

Avec des connecteurs gérés (Fivetran, Airbyte, Lakeflow Connect, AppFlow) ou une extraction API maison qui gère la pagination, les limites de débit, les curseurs incrémentaux et les changements de schéma, en déposant le JSON brut avant de modéliser.

#### À quoi servent les outils ELT comme dbt ?

À écrire les transformations sous forme de modèles SQL versionnés avec dépendances, tests, documentation et environnements, compilés et exécutés dans l'entrepôt, en apportant les pratiques du génie logiciel à la couche de transformation.

#### Comment gérer les changements de schéma dans les sources ?

Les détecter (contrôles de schéma, contrats, alertes), déposer les données brutes de façon souple (`VARIANT`, JSON, évolution de schéma), sélectionner explicitement les colonnes en staging, décider au cas par cas de propager ou non le changement, et communiquer les changements cassants.

#### Qu'est-ce que le chargement en micro-batch ?

Charger de petits lots toutes les quelques minutes (au lieu d'une fois par jour), en équilibrant latence et efficacité ; Snowpipe, Auto Loader, les déclencheurs de Structured Streaming et des jobs `MERGE` planifiés le mettent en œuvre.

<!-- challenge -->

Vous apprenez aujourd'hui qu'un client a changé de segment le 1er mars, mais vous avez déjà chargé les ventes de mars sur l'ancienne version. Que faites-vous ?

<!-- solution -->

Insérer la nouvelle version avec valid_from au 1er mars, clore l'ancienne au 28 février et repointer les faits de mars de ce client vers la nouvelle clé de substitution. Consigner la correction.

<!-- takeaways -->

- Les faits se lient à la version valide à la date de l'événement.
- Les changements tardifs peuvent imposer de repointer des faits.
- Testez une seule ligne courante et aucun chevauchement.

<!-- stage: Construire l'entrepôt -->

### Qualité des données

<!-- unit: Chargements complets, incrémentaux et CDC -->

<!-- goals -->

- Choisir entre extraction complète, incrémentale et CDC.
- Suivre l'avancement avec des watermarks et des tables de contrôle.

<!-- concept -->

Tout recharger chaque nuit est simple, jusqu'au jour où ça ne l'est plus : les volumes grandissent et les fenêtres rétrécissent. Les chargements incrémentaux ne prennent que ce qui a changé depuis la dernière fois, suivi par un watermark stocké dans une table de contrôle. L'extraction par horodatage dépend des sources qui mettent à jour leurs horodatages ; le CDC sur journal lit chaque changement, suppressions comprises, sans toucher aux tables.
Qui initie le transfert, l'entrepôt qui tire ou la source qui pousse, décide où vivent la planification et la gestion des échecs.

<!-- example -->

```sql
SELECT * FROM src.orders
WHERE updated_at > (SELECT last_watermark FROM etl_control WHERE pipeline = 'orders')
  AND updated_at <= :run_started_at;
UPDATE etl_control SET last_watermark = :run_started_at WHERE pipeline = 'orders';
```

#### Quelles sont les dimensions de la qualité des données ?

Complétude (pas de données manquantes), exactitude (valeurs correctes), cohérence (mêmes valeurs entre systèmes), validité (respect des formats et règles), unicité (pas de doublons), fraîcheur (données assez récentes) et intégrité (les relations sont respectées).

#### Quels tests chaque table de l'entrepôt devrait-elle avoir ?

Unicité et non-nullité de la clé primaire au grain, intégrité référentielle des faits vers les dimensions, valeurs acceptées pour les codes de statut, fraîcheur du dernier chargement, seuils ou anomalies sur le nombre de lignes, et rapprochement avec les sources pour les tables critiques.

#### Où doivent s'exécuter les contrôles de qualité ?

À l'ingestion (contrôles de schéma et de format), après les transformations (règles métier et intégrité) et avant la publication aux consommateurs (barrières qui empêchent les données fausses d'atteindre les tableaux de bord), en conservant les résultats pour suivre les tendances.

#### Que doit-il se passer quand un contrôle de qualité échoue ?

Cela dépend de la gravité : bloquer la publication et alerter le responsable pour les contrôles critiques, mettre en quarantaine les lignes fautives et continuer pour les problèmes au niveau ligne, ou avertir et enregistrer pour les problèmes mineurs. Les consommateurs doivent être informés quand les données sont en retard ou fausses.

#### Quels outils utilise-t-on pour la qualité des données d'un entrepôt ?

Les tests et paquets dbt (dbt_utils, dbt_expectations), Great Expectations, Soda, Monte Carlo et d'autres outils d'observabilité, les expectations de Databricks, les data metric functions de Snowflake et des contrôles SQL maison dans les orchestrateurs.

#### Qu'est-ce que l'observabilité des données ?

La supervision des systèmes de données en termes de fraîcheur, de volume, de changements de schéma, de changements de distribution et de lignage, souvent avec une détection automatique d'anomalies, pour découvrir les incidents de données avant les utilisateurs.

<!-- challenge -->

Un chargement incrémental sur `updated_at` ne supprime jamais les commandes effacées dans la source. Quelles options avez-vous ?

<!-- solution -->

Passer au CDC sur journal pour recevoir les événements de suppression, ou comparer périodiquement la liste complète des clés avec la source pour détecter les clés manquantes, puis les marquer supprimées (soft delete) dans l'entrepôt.

<!-- takeaways -->

- L'incrémental passe à l'échelle ; le complet est simple.
- Watermarks et tables de contrôle suivent l'avancement.
- Le CDC sur journal capture aussi les suppressions.

<!-- unit: Charger dimensions et faits -->

<!-- goals -->

- Charger dimensions et faits dans le bon ordre, avec recherche de clés.
- Gérer les inferred members et les suppressions à la source.

<!-- concept -->

L'ordre compte : les dimensions se chargent d'abord pour que les faits trouvent leurs clés de substitution. Les chargements de dimensions nettoient et dédupliquent par clé naturelle, puis appliquent les politiques de changement. Les chargements de faits recherchent les clés de chaque dimension, dans la version valide à la date de l'événement.
Quand un fait référence un client que l'entrepôt n'a pas encore vu, un inferred member permet de charger le fait et sera complété plus tard. Les suppressions à la source exigent aussi une politique : suppression physique ou indicateur de suppression.

<!-- example -->

```text
1. load dim_date (static), dim_product, dim_customer (SCD2)
2. load fct_order_lines:
   customer_key ← lookup(customer_number, order_date)  or inferred member if missing
   product_key  ← lookup(sku, order_date)              or -1 (unknown)
```

#### Qu'est-ce qu'un contrat de données ?

Un accord entre un producteur de données et ses consommateurs sur le schéma, la sémantique, la qualité et les SLA d'un jeu de données, appliqué dans la CI et les pipelines pour détecter tôt les changements cassants.

#### Qu'est-ce qu'un SLA de qualité des données ?

Un engagement sur une qualité mesurable (par exemple « moins de 0,1 % de commandes sans client », « données de moins de 2 heures »), supervisé automatiquement et communiqué aux consommateurs.

#### Comment quantifier l'impact métier de données de mauvaise qualité ?

En rattachant les incidents aux décisions touchées (factures erronées, objectifs mal mesurés), au temps passé à corriger et à la confiance perdue ; cela aide à prioriser les investissements qualité sur les jeux de données critiques.

#### Que sont les contrôles de détection d'anomalies ?

Des contrôles statistiques qui comparent les indicateurs du jour (nombres de lignes, sommes, taux de nulls) aux tendances historiques et signalent les écarts inhabituels même sans seuil explicite.

#### Quel est le rôle d'un data steward ?

Un responsable côté métier chargé des définitions, des règles de qualité et de la résolution des problèmes d'un domaine de données, en lien avec les data engineers qui implémentent les contrôles.

<!-- challenge -->

Des commandes de nouveaux clients arrivent quelques heures avant que le CRM n'envoie leurs informations, et ces commandes gardent définitivement la clé inconnue. Que changez-vous ?

<!-- solution -->

Créer des inferred members : insérer une ligne client provisoire avec la clé naturelle quand un fait référence un client inconnu, puis la mettre à jour (type 1) à l'arrivée des données CRM. Les faits ont la bonne clé dès le départ.

<!-- takeaways -->

- Chargez les dimensions avant les faits.
- Recherchez les clés à la date de l'événement.
- Les inferred members gèrent les faits arrivés en avance.

<!-- unit: Chargements idempotents et rejouables -->

<!-- goals -->

- Rendre les chargements idempotents avec MERGE ou delete-insert.
- Lancer des backfills et rapprocher les résultats des sources.

<!-- concept -->

Tout chargement sera relancé un jour : après un échec, une correction ou des données tardives. Un chargement ne se relance sans risque que si deux exécutions donnent le même résultat, ce qui suppose de remplacer sa tranche de données plutôt que d'ajouter. Un `MERGE` sur la clé du grain ou la suppression puis réinsertion de la fenêtre de chargement le permet.
Les backfills réutilisent la même logique sur des périodes passées, et des contrôles de rapprochement comparent les totaux à la source pour prouver le résultat.

<!-- example -->

```sql
MERGE INTO fct_order_lines t
USING stg_order_lines s
ON t.order_number = s.order_number AND t.line_number = s.line_number
WHEN MATCHED THEN UPDATE SET quantity = s.quantity, net_amount = s.net_amount, loaded_at = s.loaded_at
WHEN NOT MATCHED THEN INSERT (order_number, line_number, date_key, customer_key, product_key, quantity, net_amount, loaded_at)
VALUES (s.order_number, s.line_number, s.date_key, s.customer_key, s.product_key, s.quantity, s.net_amount, s.loaded_at);
```

#### Qu'est-ce que l'approche d'Inmon ?

Une approche descendante : construire un entrepôt d'entreprise normalisé (3FN) comme cœur intégré (la Corporate Information Factory), puis en dériver des data marts dépendants pour les départements. Elle privilégie l'intégration et la cohérence mais met plus de temps à apporter de la valeur.

#### Qu'est-ce que l'approche de Kimball ?

Une approche ascendante : construire des data marts dimensionnels par processus métier, intégrés par les dimensions conformes et la bus matrix, en apportant de la valeur de façon incrémentale. L'union des marts constitue l'entrepôt.

#### Inmon ou Kimball : comment choisir ?

Kimball pour livrer plus vite des modèles compréhensibles par le métier ; Inmon (ou Data Vault) pour un cœur fortement intégré et auditable dans des entreprises complexes aux nombreuses sources. Beaucoup d'organisations les combinent : un cœur normalisé ou Data Vault avec des marts Kimball au-dessus.

#### Qu'est-ce que Data Vault ?

Une méthode de modélisation de Dan Linstedt pour la couche d'intégration : des hubs (clés métier), des links (relations entre hubs) et des satellites (attributs descriptifs historisés). Elle fonctionne en insertion seule, est auditable et s'adapte bien aux changements des sources, avec des marts construits au-dessus pour la consommation.

#### Quels sont les avantages et inconvénients de Data Vault ?

Avantages : auditabilité, historique complet, chargement parallèle, résilience aux changements de sources, ajout facile de sources. Inconvénients : beaucoup de tables et de jointures, inutilisable directement par les analystes (il faut des marts), plus complexe à implémenter et à interroger sans automatisation.

<!-- challenge -->

Après un backfill de mars, le CA de mars dans l'entrepôt est inférieur de 0,4 % à celui du système source. Comment trouver l'écart ?

<!-- solution -->

Rapprocher par jour, puis par clé : comparer nombres et sommes quotidiens avec la source, et pour les jours en écart, trouver les clés source absentes de l'entrepôt (filtres, recherches de clé échouées, enregistrements tardifs).

<!-- takeaways -->

- Les chargements idempotents remplacent leur tranche de données.
- Les backfills réutilisent la même logique sur le passé.
- Rapprochez nombres et sommes avec les sources.

<!-- unit: Sources et outils -->

<!-- goals -->

- Charger des données SaaS et utiliser dbt pour les transformations.
- Gérer les changements de schéma source et le chargement en micro-batch.

<!-- concept -->

La plupart des entrepôts chargent aujourd'hui depuis des dizaines d'outils SaaS et de bases. Les connecteurs managés gèrent API et pagination ; dbt gère les transformations sous forme de SQL versionné avec tests et dépendances. Ensemble, ils couvrent l'essentiel de l'ELT.
Les sources changent pourtant en dessous : des colonnes apparaissent, des types changent. Déposer le brut avec souplesse, détecter les changements de schéma et alerter transforme ces surprises en travail planifié. Les micro-batches ramènent la latence à quelques minutes quand le quotidien ne suffit pas.

<!-- example -->

```text
Fivetran/Airbyte ─► raw schema (auto-added columns, alerts on change)
dbt: staging models (rename, cast) ─► core ─► marts, tests on each
schedule: every 15 minutes for orders, daily for finance
```

#### Quel lien entre l'architecture médaillon et l'entreposage ?

C'est un modèle en couches du lakehouse (bronze brut, silver nettoyé et harmonisé, gold prêt pour le métier) qui correspond aux couches staging, intégration et présentation ; gold contient souvent des schémas en étoile à la Kimball.

#### Qu'est-ce qu'une couche sémantique ?

Une couche qui définit une seule fois les indicateurs, dimensions et relations métier (couche sémantique de dbt, LookML, Cube, modèles sémantiques Power BI, AtScale, metric views) pour que tous les outils calculent le « chiffre d'affaires » de la même façon.

#### Qu'est-ce qu'un cube OLAP ?

Une structure multidimensionnelle qui précalcule des agrégats selon les dimensions pour des analyses rapides. Le MOLAP stocke les cubes dans un stockage spécialisé (SSAS), le ROLAP interroge des tables relationnelles et l'HOLAP mélange les deux. Les entrepôts cloud en colonnes ont réduit le besoin de cubes physiques.

#### Qu'est-ce qu'un entrepôt virtuel ou la virtualisation des données ?

L'interrogation sur place de données de plusieurs sources via une couche de virtualisation (Denodo, Trino, requêtes fédérées) sans les consolider physiquement. C'est rapide pour intégrer, mais les performances et l'historique sont limités.

<!-- challenge -->

Un connecteur ajoute automatiquement une colonne à la table brute, et un modèle aval en `SELECT *` casse l'outil BI. Comment rendre le pipeline robuste ?

<!-- solution -->

Sélectionner des colonnes explicites dans les modèles de staging au lieu de `SELECT *`, imposer des contrats sur les marts et alerter sur les changements de schéma du brut, pour ajouter les nouvelles colonnes délibérément.

<!-- takeaways -->

- Les connecteurs chargent le SaaS ; dbt le transforme.
- Déposez avec souplesse, sélectionnez explicitement.
- Les micro-batches ramènent la latence à quelques minutes.

### Architectures d'entrepôt

<!-- unit: Définir et tester la qualité -->

<!-- goals -->

- Nommer les dimensions de la qualité des données et les tests que toute table exige.
- Décider où s'exécutent les contrôles et ce qui se passe en cas d'échec.

<!-- concept -->

La qualité a plusieurs dimensions (complétude, exactitude, cohérence, ponctualité, validité, unicité), et chaque table a besoin de tests pour celles qui la concernent. Certains s'appliquent partout : unicité de la clé au grain, clés non nulles, intégrité référentielle des faits vers les dimensions.
L'endroit où s'exécutent les contrôles décide de ce qu'ils attrapent : à l'ingestion pour le format, après transformation pour les règles, avant publication comme barrière. La sévérité décide de la réponse, du blocage avec alerte à l'avertissement journalisé.

<!-- example -->

```yaml
models:
  - name: fct_order_lines
    tests:
      - dbt_utils.unique_combination_of_columns: {combination_of_columns: [order_number, line_number]}
    columns:
      - name: customer_key
        tests: [not_null, {relationships: {to: ref('dim_customer'), field: customer_key}}]
      - name: net_amount
        tests: [{dbt_utils.accepted_range: {min_value: -100000, max_value: 100000}}]
```

#### Qu'est-ce qu'un entrepôt temps réel ou en streaming ?

Un entrepôt alimenté en continu (Snowpipe Streaming, streaming BigQuery, connecteurs Kafka, CDC) avec des transformations à faible latence (dynamic tables, vues matérialisées, streaming tables), pour une analytique opérationnelle qui a besoin de données en quelques secondes ou minutes.

#### Qu'est-ce qu'une architecture hub-and-spoke ?

Un entrepôt d'entreprise central (hub) qui alimente des data marts départementaux (spokes), la topologie classique de style Inmon.

#### Qu'est-ce qu'une architecture fédérée ?

Plusieurs entrepôts ou marts tenus par différentes entités métier, intégrés par des standards partagés, des dimensions conformes ou de la virtualisation plutôt que par un stockage central unique ; elle rejoint les idées du data mesh.

#### Qu'est-ce qu'une « persistent staging area » ?

Une couche de staging qui conserve toutes les extractions historiques (souvent en insertion seule avec horodatage de chargement) au lieu d'être vidée à chaque exécution, ce qui permet de reconstruire les couches aval sans réextraire des sources.

#### Que sont le « raw vault » et le « business vault » en Data Vault ?

Le raw vault stocke les données sources telles quelles dans des hubs, links et satellites ; le business vault ajoute des structures dérivées appliquant des règles métier (satellites calculés, tables point-in-time et bridge) pour simplifier la construction des marts.

<!-- challenge -->

Un test d'unicité sur une table de faits échoue à 06:00. Les tableaux de bord se rafraîchissent à 07:00. Que doit faire le pipeline ?

<!-- solution -->

Bloquer la publication du mart concerné (en gardant visibles les données de la veille), alerter le propriétaire avec les clés en échec et signaler les tableaux de bord comme périmés. Publier des doublons induirait les utilisateurs en erreur.

<!-- takeaways -->

- Testez clés, nulls et relations sur chaque table.
- Contrôlez à l'ingestion, à la transformation et à la publication.
- La sévérité décide : bloquer, mettre en quarantaine ou avertir.

<!-- unit: Supervision et responsabilité -->

<!-- goals -->

- Surveiller la qualité avec observabilité, détection d'anomalies et SLA.
- Attribuer les responsabilités avec contrats et stewards.

<!-- concept -->

Les tests attrapent ce que quelqu'un a prévu ; la supervision attrape le reste. L'observabilité surveille fraîcheur, volume, schéma et distributions, et la détection d'anomalies compare aujourd'hui à l'historique pour signaler des changements brusques qu'aucune règle ne décrivait.
La qualité est aussi un accord entre personnes. Les contrats fixent ce que promettent les producteurs, les SLA des cibles mesurables, les stewards portent définitions et corrections, et chiffrer le coût des mauvaises données justifie l'effort.

<!-- example -->

| Signal | Contrôle |
|---|---|
| Fraîcheur | `max(loaded_at)` à moins de 2 h du planning |
| Volume | Nombre de lignes à ±20 % de la moyenne sur 7 jours |
| Distribution | Taux de nulls de `customer_key` < 0,1 % |
| Schéma | Colonne ajoutée/supprimée à la source → alerte |

#### Que sont les tables point-in-time (PIT) en Data Vault ?

Des tables auxiliaires qui stockent, pour chaque clé de hub et chaque date de photo, les dates de chargement des satellites correspondants, ce qui accélère la reconstitution de l'état d'une entité à une date donnée pour les dimensions.

#### Qu'est-ce que le MPP ?

Le massively parallel processing : une base répartit les données sur de nombreux nœuds, chacun avec son CPU, sa mémoire et son stockage (ou cache), exécute les requêtes en parallèle et combine les résultats. Redshift, Teradata, Synapse et Vertica sont MPP ; Snowflake et BigQuery en sont des variantes cloud.

#### Pourquoi les bases analytiques sont-elles en colonnes ?

Les requêtes analytiques lisent quelques colonnes de nombreuses lignes ; stocker chaque colonne de façon contiguë permet de ne lire que les colonnes utiles, de très bien compresser des valeurs similaires et de les traiter en exécution vectorisée.

#### Quelle différence entre stockage par lignes et par colonnes ?

Le stockage par lignes regroupe toutes les colonnes d'une ligne, efficace pour lire et écrire des enregistrements complets (OLTP). Le stockage en colonnes regroupe les valeurs de chaque colonne, efficace pour les lectures et agrégations sur peu de colonnes (OLAP).

#### Qu'est-ce qu'une clé de distribution (Redshift, Synapse) ?

La colonne utilisée pour répartir les lignes entre les nœuds. Distribuer deux grosses tables sur leur clé de jointure colocalise les lignes correspondantes et évite la redistribution lors des jointures ; les petites dimensions peuvent être répliquées (`ALL`) sur chaque nœud ; `EVEN` ou `AUTO` répartissent uniformément.

#### Qu'est-ce qu'une sort key (Redshift) ou clé de clustering ?

Un ordre des données dans le stockage pour que les filtres sur plage puissent sauter des blocs grâce aux métadonnées min/max (zone maps). Équivalents : clés de clustering Snowflake, clustering BigQuery, liquid clustering ou Z-order de Delta.

<!-- challenge -->

Tous les tests passent, mais les ventes d'hier sont deux fois plus faibles que d'habitude car le flux d'un magasin a échoué silencieusement. Quel contrôle l'aurait détecté ?

<!-- solution -->

Un contrôle d'anomalie sur le volume ou le CA par magasin (ou par source) par rapport à l'historique récent, qui alerte quand un segment chute fortement même si les totaux restent plausibles.

<!-- takeaways -->

- L'observabilité attrape ce que les tests n'avaient pas prévu.
- Contrats et SLA font de la qualité un accord.
- Les stewards portent définitions et corrections.

### Moteurs et stockage

<!-- unit: Fonctions de fenêtrage -->

<!-- goals -->

- Utiliser les fonctions de fenêtrage pour cumuls, classements et déduplication.
- Calculer la croissance d'une période sur l'autre.

<!-- concept -->

Les fonctions de fenêtrage calculent sur des lignes liées sans les regrouper, d'où leur omniprésence en entreposage. La partition définit le groupe, l'ordre la séquence, et le frame les lignes prises en compte. Grâce à elles, cumuls, classements, sélection de la dernière ligne et comparaisons avec la période précédente tiennent en une expression.
Les fonctions de classement ne diffèrent que par les ex æquo, un détail qui change les résultats quand des valeurs se répètent.

<!-- example -->

```sql
WITH monthly AS (
  SELECT d.year_month, SUM(f.net_amount) AS revenue
  FROM fct_order_lines f JOIN dim_date d USING (date_key)
  GROUP BY 1
)
SELECT year_month, revenue,
       revenue / NULLIF(LAG(revenue) OVER (ORDER BY year_month), 0) - 1 AS mom_growth
FROM monthly;
```

#### Qu'est-ce que le partitionnement dans un entrepôt ?

Le découpage d'une grosse table selon une colonne (généralement la date) pour que les requêtes filtrant dessus ne lisent que les partitions pertinentes et que la maintenance (supprimer d'anciennes données, recharger un jour) soit peu coûteuse. BigQuery utilise un partitionnement explicite ; Snowflake des micro-partitions automatiques.

#### Que sont les zone maps ou statistiques min/max ?

Des métadonnées qui stockent les valeurs minimale et maximale par bloc ou fichier, utilisées pour sauter les blocs qui ne peuvent pas correspondre à un filtre. Des données triées ou regroupées selon la colonne filtrée les rendent efficaces.

#### Qu'est-ce qu'une vue matérialisée ?

Le résultat stocké d'une requête, rafraîchi automatiquement ou périodiquement. Elle accélère les agrégations ou jointures répétées ; le moteur peut l'utiliser de façon transparente. Sa maintenance coûte du calcul.

#### Qu'est-ce que la gestion des charges de travail (workload management) ?

Le contrôle du partage des ressources entre requêtes : files, priorités, limites de concurrence, clusters ou warehouses séparés pour l'ETL et la BI, et timeouts, pour que les traitements lourds n'affament pas les utilisateurs interactifs.

#### Qu'est-ce que la séparation du stockage et du calcul ?

Stocker les données dans un stockage partagé (stockage objet) et exécuter dessus des clusters de calcul indépendants et élastiques, pour dimensionner et payer chacun séparément et isoler les charges. Snowflake, BigQuery, Databricks et Redshift RA3/Serverless suivent ce modèle.

<!-- challenge -->

Vous avez besoin des 3 meilleurs produits en CA de chaque catégorie, ex æquo à la troisième place compris. Quelle fonction utilisez-vous ?

<!-- solution -->

`RANK()` ou `DENSE_RANK()` sur le CA partitionné par catégorie, filtré sur rang ≤ 3. `ROW_NUMBER()` départagerait arbitrairement les ex æquo.

<!-- takeaways -->

- Les fenêtres calculent sur des lignes liées sans les regrouper.
- `LAG` et les frames donnent croissance et cumuls.
- Les fonctions de classement diffèrent sur les ex æquo.

<!-- unit: Motifs analytiques -->

<!-- goals -->

- Écrire des requêtes de cohortes, de rétention et d'activité consécutive.
- Calculer percentiles, agrégats multiniveaux et pivots.

<!-- concept -->

La plupart des demandes analytiques sont des variantes de quelques motifs. Les cohortes regroupent les clients selon leur date de début et les suivent dans le temps. Les questions d'activité consécutive comparent chaque période à la précédente. Les percentiles décrivent mieux les distributions que les moyennes. Agrégats multiniveaux et pivots mettent en forme les résultats pour les rapports.
Reconnaître le motif derrière une question fait l'essentiel du travail ; le SQL suit.

<!-- example -->

```sql
WITH firsts AS (
  SELECT customer_key, MIN(order_month) AS cohort FROM customer_months GROUP BY 1
)
SELECT f.cohort, m.order_month, COUNT(DISTINCT m.customer_key) AS active
FROM customer_months m JOIN firsts f USING (customer_key)
GROUP BY 1, 2 ORDER BY 1, 2;
```

#### Qu'est-ce que l'exécution vectorisée ?

Le traitement de lots de valeurs de colonnes en une fois avec des boucles efficaces pour le CPU et des instructions SIMD, au lieu de ligne par ligne, ce qui accélère fortement les lectures, filtres et agrégations des moteurs en colonnes.

#### Que sont les caches de résultats ?

Des stockages de résultats de requêtes précédentes renvoyés instantanément quand la même requête est relancée sur des données inchangées (cache de résultats Snowflake, résultats en cache BigQuery), ce qui économise du calcul pour les tableaux de bord.

#### Quel rôle jouent les statistiques dans l'optimisation des requêtes ?

Les nombres de lignes, valeurs distinctes, min/max et histogrammes permettent à l'optimiseur d'estimer les cardinalités et de choisir l'ordre et la stratégie des jointures ; des statistiques périmées donnent de mauvais plans.

#### Qu'est-ce que l'encodage de compression dans les stockages en colonnes ?

Des techniques comme l'encodage par dictionnaire, run-length, delta et bit-packing qui réduisent les colonnes aux valeurs répétées ou ordonnées ; des données triées se compressent mieux.

#### Quelle différence entre scale up et scale out dans les entrepôts ?

Le scale up donne plus de ressources à une requête (warehouse plus gros, plus de slots) pour qu'elle finisse plus vite ; le scale out ajoute des clusters pour servir plus de requêtes simultanées. Choisissez selon que le problème est la latence d'une requête ou la concurrence.

<!-- challenge -->

Un rapport a besoin du CA par année, par année et trimestre, et d'un total général dans un seul résultat. Comment l'écrire sans trois requêtes ?

<!-- solution -->

`GROUP BY ROLLUP(year, quarter)`, qui renvoie des sous-totaux par année, des lignes par trimestre et un total général ; utiliser `GROUPING()` pour étiqueter les lignes de sous-total.

<!-- takeaways -->

- Les cohortes suivent les clients depuis leur première activité.
- Les percentiles décrivent mieux les données asymétriques que les moyennes.
- `ROLLUP`, `CUBE` et les pivots mettent en forme les rapports.

<!-- unit: Écrire du SQL juste -->

<!-- goals -->

- Structurer les requêtes avec des CTE et filtrer au bon endroit.
- Éviter les erreurs dues à la division par zéro et aux NULL.

<!-- concept -->

Les mauvais chiffres dans les rapports viennent généralement de petites erreurs SQL, pas d'une logique complexe. Filtrer après l'agrégation au lieu d'avant, diviser par zéro ou oublier que `NULL` n'est jamais égal à rien changent silencieusement les résultats.
Une structure lisible est la meilleure défense : les CTE nomment chaque étape pour que les relecteurs suivent la logique, et traiter explicitement `NULL` et zéro transforme des hypothèses cachées en décisions visibles.

<!-- example -->

```sql
WITH paid AS (
  SELECT customer_key, net_amount FROM fct_order_lines WHERE status = 'paid'   -- row filter: WHERE
)
SELECT customer_key, SUM(net_amount) AS revenue,
       SUM(net_amount) / NULLIF(COUNT(*), 0) AS avg_line
FROM paid
GROUP BY customer_key
HAVING SUM(net_amount) > 1000;                                               -- group filter: HAVING
```

#### Comment rendre rapide une requête sur un schéma en étoile ?

Filtrer sur les colonnes de partitionnement ou de clustering (date), joindre les faits à de petites dimensions (broadcast), ne sélectionner que les colonnes utiles, pré-agréger les requêtes courantes, tenir les statistiques à jour et éviter les fonctions sur les colonnes filtrées.

#### Qu'est-ce qui provoque un « fan-out » ou un double comptage dans les jointures ?

Joindre un fait à une table qui a plusieurs lignes par clé (plusieurs-à-plusieurs ou mauvais grain), de sorte que chaque ligne de fait est dupliquée et que les sommes gonflent. Vérifiez la cardinalité des jointures et imposez l'unicité des clés de dimension.

#### Comment accélérer `COUNT(DISTINCT)` sur de gros volumes ?

Utiliser des fonctions approximatives (HyperLogLog : `APPROX_COUNT_DISTINCT`), pré-agréger des ensembles distincts par période, ou maintenir des comptes distincts dans des tables agrégées quand des valeurs exactes sont nécessaires.

#### Pourquoi des tables larges dénormalisées peuvent-elles être rapides dans un moteur en colonnes ?

Parce que seules les colonnes référencées par la requête sont lues : une table large ne coûte pas plus à interroger qu'une étroite de même nombre de lignes, et elle évite des jointures. Les coûts sont le stockage, la maintenance et le risque d'incohérence.

<!-- challenge -->

Une jointure sur `promotion_id` élimine toutes les ventes sans promotion, et le CA paraît faible. Que s'est-il passé, et comment corriger dans le modèle ?

<!-- solution -->

Les ventes ont des ID de promotion `NULL`, et `NULL` ne correspond jamais dans une jointure : une jointure interne les élimine. Rattacher les promotions manquantes à un membre inconnu/sans promotion dans le fait (ou utiliser une jointure externe gauche).

<!-- takeaways -->

- Les CTE rendent chaque étape lisible.
- `NULLIF` évite la division par zéro.
- Les clés `NULL` ne joignent pas ; utilisez des membres inconnus.

<!-- stage: Plateformes et performance -->

### Performances

<!-- unit: MPP et stockage colonnaire -->

<!-- goals -->

- Expliquer le MPP et pourquoi les moteurs analytiques stockent par colonne.
- Décrire encodages de compression et exécution vectorisée.

<!-- concept -->

Les moteurs analytiques sont faits pour un type de travail : parcourir beaucoup de lignes mais peu de colonnes. Stocker chaque colonne d'un bloc fait qu'une requête ne lit que ce qu'elle utilise, et des valeurs similaires côte à côte se compressent extrêmement bien. Traiter les valeurs par lots avec des boucles adaptées au processeur accélère chaque parcours.
Le traitement massivement parallèle ajoute l'échelle : les données sont réparties entre des nœuds qui traitent leur part en même temps, donc ajouter des nœuds ajoute de la vitesse.

<!-- example -->

| Disposition | Lire `SUM(amount)` sur 1 Md de lignes × 50 colonnes |
|---|---|
| Stockage en lignes | Lit les 50 colonnes |
| Stockage en colonnes | Lit 1 colonne, compressée ~10× |

#### Qu'est-ce que l'élagage (pruning), et comment le vérifier ?

Sauter les partitions, fichiers ou blocs qui ne peuvent pas correspondre aux filtres d'une requête. On le vérifie dans les profils ou plans de requête (partitions lues sur le total, octets lus) et on corrige filtres ou organisation des données quand il n'a pas lieu.

#### Comment optimiser un tableau de bord lent ?

Trouver les requêtes lentes, vérifier l'élagage et les jointures, ajouter des agrégats ou des vues matérialisées au grain du tableau de bord, utiliser les extraits ou le cache de l'outil BI, limiter les plages de dates par défaut et retirer les visuels inutiles qui déclenchent chacun des requêtes.

#### Quel est l'impact des types de données sur les performances de l'entrepôt ?

Des types plus petits (entiers plutôt que chaînes pour les clés, `DATE` plutôt que `TIMESTAMP` quand cela suffit, `DECIMAL` de précision adaptée) se compressent mieux et se comparent plus vite ; joindre sur des types différents impose des conversions et empêche des optimisations.

#### Comment gérer de très grosses dimensions (des centaines de millions de lignes) ?

Partitionner ou regrouper par plages de clés naturelles, limiter le renouvellement SCD2 avec des mini-dimensions, éviter les attributs inutiles, utiliser des clés de substitution entières, et se demander si la « dimension » n'est pas en réalité une entité proche d'un fait.

#### Qu'est-ce qu'un agrégat « couvrant » ?

Une table agrégée contenant toutes les colonnes dont une requête fréquente a besoin au bon grain, pour que la requête ne touche jamais la table de faits atomique.

<!-- challenge -->

Une équipe stocke une colonne de statut en longues chaînes comme « ORDER_STATUS_SHIPPED ». Est-ce important dans un entrepôt colonnaire ?

<!-- solution -->

Moins que dans un stockage en lignes, car l'encodage par dictionnaire compresse bien les valeurs répétées. Des codes courts ou de petits entiers réduisent toutefois mémoire et coût de comparaison ; garder les libellés dans une dimension.

<!-- takeaways -->

- Le stockage colonnaire ne lit que les colonnes utiles.
- Les encodages compressent fortement les valeurs répétées.
- Le MPP répartit le travail entre nœuds.

<!-- unit: Disposition des données -->

<!-- goals -->

- Utiliser clés de distribution, clés de tri, clustering et partitionnement.
- Expliquer comment zone maps et statistiques aident l'optimiseur.

<!-- concept -->

L'emplacement des données décide de ce qu'une requête doit lire et déplacer. Partitionner et trier permet au moteur d'ignorer les blocs dont les min/max ne peuvent satisfaire un filtre. La distribution décide quel nœud détient quelles lignes, pour que les jointures sur la clé de distribution se fassent sans déplacer de données.
Les statistiques indiquent à l'optimiseur la taille des tables et la répartition des valeurs, ce qui pilote l'ordre et la stratégie de jointure. Des statistiques périmées produisent de mauvais plans sur de bonnes données.

<!-- example -->

```sql
-- Redshift
CREATE TABLE fct_order_lines (...)
DISTKEY (customer_key)
SORTKEY (date_key);
-- Snowflake / BigQuery equivalent idea: CLUSTER BY (date_key)
```

#### Comment éviter des `SELECT DISTINCT` coûteux dans les modèles ?

Chercher pourquoi les doublons apparaissent (une jointure au mauvais grain) et corriger la jointure plutôt que de la masquer avec `DISTINCT`, coûteux et qui cache des problèmes de données.

#### Comment tester les performances de l'entrepôt avant la mise en production ?

Rejouer des requêtes représentatives et la concurrence sur des données de taille réelle, mesurer la latence et le coût par requête, vérifier l'élagage et les jointures dans les plans, et ajuster l'organisation, les agrégats et le dimensionnement.

#### Comment les modèles incrémentaux réduisent-ils les coûts de l'entrepôt ?

En ne transformant à chaque exécution que les données nouvelles ou modifiées au lieu de reconstruire des tables entières, ce qui réduit fortement le calcul sur les gros faits ; ils exigent une gestion soignée des données tardives et des backfills.

#### Quels sont les principaux entrepôts cloud ?

Snowflake, Google BigQuery, Amazon Redshift (provisionné et Serverless), les entrepôts Azure Synapse et Microsoft Fabric, et Databricks SQL sur le lakehouse. Ils diffèrent par leur architecture, leurs modèles de prix et leur intégration à l'écosystème.

#### Comment fonctionne BigQuery et comment est-il facturé ?

BigQuery est serverless : stockage dans un format en colonnes (Capacitor) sur Colossus, calcul alloué en slots par Dremel. Il est facturé à la demande au To lu ou à la capacité (éditions avec slots réservés ou en autoscaling), plus le stockage.

<!-- challenge -->

Une requête qui filtre une journée d'une table de faits de 3 ans lit 80 % de ses blocs. Que vérifiez-vous ?

<!-- solution -->

Si la table est triée, regroupée ou partitionnée par date, et si le filtre porte directement sur cette colonne (pas via une fonction). Vérifier la profondeur de clustering ou l'état vacuum/sort si les données ont été chargées dans le désordre.

<!-- takeaways -->

- Tri et partitionnement permettent d'ignorer des blocs.
- Les clés de distribution colocalisent les données jointes.
- Des statistiques fraîches donnent de bons plans.

<!-- unit: Calcul et concurrence -->

<!-- goals -->

- Séparer stockage et calcul et gérer les charges de travail.
- Utiliser vues matérialisées, caches de résultats et options de montée en charge.

<!-- concept -->

Les entrepôts cloud séparent stockage et calcul : plusieurs clusters indépendants peuvent lire les mêmes données. Cela change la gestion de la charge : un calcul séparé par charge empêche l'ETL de ralentir les tableaux de bord, ajouter des clusters sert plus d'utilisateurs, et agrandir un cluster accélère une requête isolée.
Cache et précalcul réduisent encore le travail : les caches de résultats répondent instantanément aux requêtes répétées, et les vues matérialisées gardent prêts les résultats coûteux.

<!-- example -->

| Problème | Levier |
|---|---|
| L'ETL ralentit les tableaux de bord à 08:00 | Calcul séparé par charge |
| Une requête lourde est lente | Agrandir |
| 200 utilisateurs en file à 09:00 | Multiplier (multi-cluster) |
| Même requête de tableau de bord 500×/jour | Cache de résultats / vue matérialisée |

#### Comment fonctionne Amazon Redshift ?

Un entrepôt MPP avec un nœud leader et des nœuds de calcul ; les nœuds RA3 séparent le stockage géré (adossé à S3) du calcul, Serverless est facturé au RPU-heure, et ses fonctions incluent les clés de distribution et de tri (avec réglage automatique), les vues matérialisées, Spectrum pour les données S3, le partage de données et les intégrations zero-ETL.

#### Comment les entrepôts cloud facturent-ils, et qu'est-ce qui fait les coûts ?

Le calcul (crédits, slots, RPU, DBU) domine généralement, puis le stockage, le transfert de données et les fonctions serverless. Les coûts augmentent avec les requêtes inefficaces, le calcul toujours allumé, les rafraîchissements complets et de nombreux utilisateurs lançant des requêtes non filtrées ; gouvernance et supervision sont indispensables.

#### Comment choisir un entrepôt cloud ?

En tenant compte du cloud et de l'écosystème existants, des profils de charge (réguliers ou en pics, concurrence), des compétences, des besoins de gouvernance, des formats ouverts et de la stratégie lakehouse, de l'adéquation du modèle de prix, des besoins de partage et de la tolérance à la dépendance envers un fournisseur. Faites un prototype avec de vraies requêtes avant de vous engager.

#### Qu'est-ce que le partage de données zero-copy ?

Le partage de données vivantes entre comptes ou organisations sans les copier (Secure Data Sharing de Snowflake, Analytics Hub de BigQuery, data sharing de Redshift, Delta Sharing), pour que les consommateurs interrogent les données du fournisseur avec leur propre calcul.

#### Quelles conséquences ont les formats de table ouverts pour les entrepôts ?

Iceberg et Delta permettent à plusieurs moteurs (entrepôt, Spark, Trino) de travailler sur les mêmes données en stockage objet, réduisant la dépendance et les copies. Les entrepôts les lisent et les écrivent de plus en plus nativement.

<!-- challenge -->

Les tableaux de bord du matin attendent derrière l'ETL nocturne qui finit en retard. L'entrepôt n'a qu'un cluster. Que proposez-vous ?

<!-- solution -->

Donner à l'ETL et à la BI des calculs séparés (warehouses ou files avec workload management), pour que la BI n'attende jamais l'ETL. Traiter ensuite le retard de l'ETL séparément.

<!-- takeaways -->

- Séparer stockage et calcul permet d'isoler les charges.
- Agrandir pour une requête ; multiplier pour la concurrence.
- Caches et vues matérialisées évitent le travail répété.

### Entrepôts cloud

<!-- unit: Requêtes en étoile rapides -->

<!-- goals -->

- Faire élaguer et joindre efficacement les requêtes sur schéma en étoile.
- Choisir types de données et tables larges pour la vitesse.

<!-- concept -->

Les requêtes en étoile rapides partagent un profil : elles filtrent sur des colonnes partitionnées ou regroupées, joignent un gros fait à de petites dimensions et lisent peu de colonnes. Vérifier l'élagage dans le profil de requête est la première étape dès que quelque chose est lent.
Sur un moteur colonnaire, les tables larges dénormalisées peuvent être rapides, car les colonnes inutilisées ne coûtent rien. Des types compacts aident partout : clés et dates plus petites se parcourent, se joignent et se compressent mieux.

<!-- example -->

```text
Query profile: fct_order_lines
  partitions scanned: 31 of 1,826   ✔ pruning on date_key
  bytes scanned: 4.2 GB
  join: broadcast dim_product (12 MB) ✔
```

#### Comment BigQuery gère-t-il le partitionnement et le clustering ?

Les tables peuvent être partitionnées par une colonne date/horodatage, par temps d'ingestion ou par plage d'entiers, et regroupées sur jusqu'à quatre colonnes ; les requêtes filtrant dessus lisent moins d'octets, ce qui réduit directement le coût à la demande.

#### Qu'est-ce que Redshift Spectrum ?

Une fonction qui permet à Redshift d'interroger des données S3 via des tables externes du Glue Data Catalog, en joignant les données du lake aux tables de l'entrepôt, facturée à l'octet lu.

#### Qu'est-ce que l'entrepôt de Microsoft Fabric ?

Une plateforme analytique SaaS où entrepôts et lakehouses stockent les données au format Delta dans OneLake, interrogées en T-SQL et en Spark et servies à Power BI en mode Direct Lake.

#### Qu'est-ce que Databricks SQL en tant qu'entrepôt ?

Des SQL warehouses sur le lakehouse Databricks qui interrogent des tables Delta gouvernées par Unity Catalog, avec Photon, du calcul serverless et des connecteurs BI, offrant les fonctions d'un entrepôt sur un stockage ouvert.

#### Qu'est-ce qui rend un modèle de données adapté à la BI ?

Des schémas en étoile aux noms clairs, des définitions métier documentées, des dimensions conformes, des grains corrects, des clés de substitution cachées aux utilisateurs, une gestion cohérente des dates et une couche sémantique pour les indicateurs.

<!-- challenge -->

Les clés de jointure sont des UUID de 36 caractères, et les jointures sur un fait de 2 milliards de lignes sont lentes. Que changez-vous ?

<!-- solution -->

Utiliser des clés de substitution entières dans faits et dimensions (garder l'UUID comme attribut de clé naturelle). Jointures et comparaisons d'entiers coûtent bien moins et se compressent mieux.

<!-- takeaways -->

- Vérifiez d'abord l'élagage quand une requête est lente.
- Joignez les gros faits à de petites dimensions.
- Les types compacts allègent parcours et jointures.

<!-- unit: Jointures et comptages distincts -->

<!-- goals -->

- Reconnaître et corriger le fan-out et les DISTINCT inutiles.
- Accélérer comptages distincts et très grandes dimensions.

<!-- concept -->

Deux habitudes rendent les requêtes à la fois lentes et fausses. Joindre au mauvais grain multiplie les lignes, et ajouter `DISTINCT` pour masquer les doublons double le coût sans traiter la cause. Corriger la jointure est la vraie solution.
Les comptages distincts sur d'énormes volumes sont coûteux par nature ; les fonctions approximatives ou des ensembles pré-agrégés les rendent abordables. Les très grandes dimensions demandent le même soin que les faits : clustering, moins de versions et jointures sur des clés compactes.

<!-- example -->

```sql
SELECT date_key, APPROX_COUNT_DISTINCT(customer_key) AS customers   -- HyperLogLog, ~1–2% error
FROM fct_page_views
WHERE date_key BETWEEN 20261001 AND 20261031
GROUP BY date_key;
```

#### Quelle différence entre un rapport et un tableau de bord ?

Un rapport présente des données détaillées, souvent tabulaires et paginées, pour l'analyse ou des besoins réglementaires. Un tableau de bord résume visuellement les indicateurs clés pour un suivi en un coup d'œil, avec exploration.

#### Qu'est-ce que la BI en libre-service, et quels sont ses risques ?

Des utilisateurs métier qui construisent leurs propres analyses à partir de jeux de données gouvernés. Risques : définitions d'indicateurs incohérentes, logique dupliquée, extraits et coûts non maîtrisés. Une couche sémantique, des jeux de données certifiés et de la formation les réduisent.

#### Qu'est-ce que la sécurité au niveau ligne dans la BI et les entrepôts ?

Restreindre les lignes visibles par chaque utilisateur selon son identité (région, département), dans l'entrepôt (row access policies, vues sécurisées) ou dans la couche BI, pour qu'un même jeu de données serve de nombreux publics en toute sécurité.

#### Comment documenter un entrepôt ?

Avec des descriptions de tables et de colonnes dans le catalogue (dbt docs, Unity Catalog, Glue, DataHub), un glossaire métier pour les indicateurs, des graphes de lignage, les responsables et les SLA, et des exemples de requêtes correctes.

<!-- challenge -->

Un modèle se termine par `SELECT DISTINCT *` « pour supprimer les doublons » et prend 40 minutes. Que faites-vous ?

<!-- solution -->

Trouver quelle jointure introduit les doublons (une table à plusieurs lignes par clé), corriger le grain de la jointure (agréger ou filtrer cette table d'abord), ajouter un test d'unicité sur la clé de sortie et retirer le `DISTINCT`.

<!-- takeaways -->

- Le fan-out vient d'une jointure au mauvais grain.
- Corrigez les jointures au lieu de masquer avec `DISTINCT`.
- Les distincts approximatifs passent à très grande échelle.

<!-- unit: Tableaux de bord et coût -->

<!-- goals -->

- Accélérer les tableaux de bord lents avec agrégats et tables couvrantes.
- Tester la performance avant la mise en service et réduire les coûts avec des modèles incrémentaux.

<!-- concept -->

Les tableaux de bord répètent les mêmes questions : leur optimisation consiste à ne pas recalculer les réponses, avec des agrégats ou vues matérialisées au grain dont les graphiques ont besoin, et des tables couvrantes qui contiennent exactement les colonnes d'une requête fréquente.
Coût et vitesse vont généralement de pair. Les modèles incrémentaux ne transforment que les nouvelles données, et tester avec des volumes et une concurrence réalistes avant le lancement évite de découvrir les limites devant les utilisateurs.

<!-- example -->

```text
dashboard "Sales overview": 9 charts
  before: each chart scans fct_order_lines (1.4 B rows) → 25 s
  after:  agg_sales_day_store_category (3 M rows), refreshed hourly → 1.5 s
```

#### Qu'est-ce qu'un jeu de données certifié ?

Un jeu de données marqué comme fiable après revue (définitions, tests, responsable), mis en avant dans les outils BI et les catalogues pour que les utilisateurs le préfèrent aux copies personnelles ou expérimentales.

#### Qu'est-ce que le reverse ETL ?

Le renvoi de données de l'entrepôt (segments, scores, indicateurs) vers des outils opérationnels comme les CRM, les plateformes marketing ou de support, pour que les équipes métier agissent sur des données modélisées (Hightouch, Census, jobs maison).

#### Comment choisir entre requêtes en direct et extraits dans les outils BI ?

Les requêtes en direct donnent des données fraîches et une sécurité centralisée mais dépendent des performances et du coût de l'entrepôt ; les extraits (extraits Tableau, import Power BI, SPICE) sont rapides et peu coûteux par requête mais périmés et dupliqués. On choisit par tableau de bord selon le besoin de fraîcheur et l'usage.

#### Comment sécuriser un entrepôt de données ?

Rôles au moindre privilège (rôles d'accès accordés à des rôles fonctionnels), SSO et MFA, restrictions réseau, chiffrement au repos et en transit, masquage des colonnes sensibles, sécurité au niveau ligne, audit des accès et environnements séparés pour le développement et la production.

<!-- challenge -->

Un projet dbt reconstruit ses 300 modèles toutes les heures, et les coûts de l'entrepôt ont triplé. Que changez-vous d'abord ?

<!-- solution -->

Rendre incrémentaux les gros modèles de faits (ne traiter que les lignes nouvelles ou modifiées), reconstruire moins souvent les petits modèles et n'exécuter chaque heure que les modèles dont les tableaux de bord ont besoin à l'heure.

<!-- takeaways -->

- Précalculez ce que les tableaux de bord demandent sans cesse.
- Testez avec des données et une concurrence réalistes.
- Les modèles incrémentaux réduisent coût et temps.

### BI et consommation

<!-- unit: Le paysage des entrepôts cloud -->

<!-- goals -->

- Décrire les principaux entrepôts cloud et leur fonctionnement.
- Comparer BigQuery, Redshift, Fabric et Databricks SQL.

<!-- concept -->

Les entrepôts cloud partagent les mêmes idées de fond, stockage colonnaire, MPP et calcul séparé, mais diffèrent par ce que vous gérez et par la façon de payer. BigQuery est entièrement serverless. Redshift propose des clusters et un mode serverless. Fabric et Databricks SQL bâtissent des entrepôts sur des formats de lac ouverts.
Connaître l'architecture de chacun explique ses leviers d'optimisation et sa tarification.

<!-- example -->

| Entrepôt | Modèle de calcul | Stockage |
|---|---|---|
| Snowflake | Virtual warehouses (crédits) | Managé, micro-partitions |
| BigQuery | Slots (à la demande ou réservés) | Colonnaire managé |
| Redshift | Clusters RA3 ou RPU Serverless | Stockage managé + S3 |
| Fabric | Unités de capacité | Delta dans OneLake |
| Databricks SQL | SQL warehouses (DBU) | Delta / Iceberg via Unity Catalog |

#### Comment traiter les données personnelles dans un entrepôt ?

Les classifier et les taguer, minimiser ce qui est chargé, pseudonymiser ou tokeniser tôt les identifiants, masquer pour la plupart des utilisateurs, restreindre l'accès brut, appliquer des politiques de rétention et traiter les demandes d'effacement (RGPD) avec des processus documentés.

#### Qu'est-ce que le lignage des données, et pourquoi compte-t-il ?

La trace de l'origine des données et de leurs transformations, au niveau table et colonne. Il sert à l'analyse d'impact avant un changement, au débogage de chiffres faux, aux audits et à la confiance.

#### Qu'est-ce qu'un catalogue de données ?

Un inventaire consultable des jeux de données avec descriptions, responsables, schémas, tags, lignage, état de qualité et usage, qui aide à trouver et comprendre les données (DataHub, Collibra, Alation, Unity Catalog, Glue Data Catalog).

#### Que sont les politiques de rétention des données ?

Des règles fixant la durée de conservation de chaque jeu de données (pour des raisons légales, métier et de coût), mises en œuvre par la suppression de partitions, des règles de cycle de vie, les réglages de Time Travel et l'archivage, et documentées pour la conformité.

#### Que sont les fonctions de fenêtre, et pourquoi sont-elles essentielles en entreposage ?

Des fonctions qui calculent des valeurs sur un ensemble de lignes liées à la ligne courante sans les regrouper (`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`, `SUM() OVER`). Elles servent à dédupliquer, calculer des cumuls, comparer des périodes et reconstituer des sessions.

<!-- challenge -->

Une équipe qui passe de Redshift à BigQuery demande où définir les clés de distribution et de tri. Que lui répondez-vous ?

<!-- solution -->

BigQuery n'a pas de clés de distribution ; il gère le placement. Les équivalents sont le partitionnement (souvent par date) et le clustering sur les colonnes de filtre courantes, plus le contrôle des octets lus, puisque la tarification à la demande facture les données lues.

<!-- takeaways -->

- Tous partagent stockage colonnaire et MPP.
- Ils diffèrent par la gestion et la tarification.
- Les leviers d'optimisation suivent chaque architecture.

<!-- unit: Choisir et payer un entrepôt -->

<!-- goals -->

- Comprendre les coûts des entrepôts cloud et choisir une plateforme.
- Utiliser le partitionnement BigQuery et Redshift Spectrum, et planifier les migrations.

<!-- concept -->

Le calcul domine la facture d'un entrepôt, et chaque plateforme le mesure différemment : crédits, slots, RPU ou DBU. Les coûts suivent les habitudes plus que les tarifs : clusters inactifs, reconstructions complètes, parcours sans filtre.
Choisir une plateforme part du contexte : le cloud utilisé, la forme des charges, les compétences, l'écosystème et la gouvernance. Y migrer est un projet d'inventaire, de traduction et de validation, pas une simple copie.

<!-- example -->

```sql
-- BigQuery: partition and cluster to cut bytes scanned
CREATE TABLE sales.fct_order_lines
PARTITION BY order_date
CLUSTER BY customer_key, product_key
AS SELECT * FROM staging.order_lines;
```

#### Comment calculer la croissance d'un mois sur l'autre ?

```sql
WITH monthly AS (
  SELECT d.year_month, SUM(f.net_amount) AS revenue
  FROM fct_order_lines f JOIN dim_date d ON f.order_date_key = d.date_key
  GROUP BY d.year_month
)
SELECT year_month, revenue,
       revenue / NULLIF(LAG(revenue) OVER (ORDER BY year_month), 0) - 1 AS mom_growth
FROM monthly;
```

#### Comment calculer un cumul ?

`SUM(amount) OVER (PARTITION BY customer_key ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`.

#### Comment dédupliquer en gardant la ligne la plus récente par clé ?

```sql
SELECT * FROM (
  SELECT s.*, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) AS rn
  FROM stg_customers s
) WHERE rn = 1;
```

Les moteurs dotés de `QUALIFY` (Snowflake, BigQuery, Databricks) permettent de filtrer directement sur la fenêtre.

#### Quelle différence entre `RANK`, `DENSE_RANK` et `ROW_NUMBER` ?

`ROW_NUMBER` donne des numéros séquentiels uniques ; `RANK` donne le même rang aux ex æquo et saute les rangs suivants (1, 1, 3) ; `DENSE_RANK` donne le même rang aux ex æquo sans trous (1, 1, 2).

#### Comment trouver les clients actifs plusieurs mois consécutifs ?

Calculer les mois d'activité de chaque client puis utiliser `LAG` pour comparer au mois précédent, ou la technique « gaps and islands » (indice du mois moins numéro de ligne) pour regrouper les séries consécutives.

<!-- challenge -->

Après la migration vers le cloud, la facture mensuelle est le double de l'estimation. Citez trois causes probables.

<!-- solution -->

Du calcul laissé allumé (sans auto-suspend), des jobs qui reconstruisent des tables entières au lieu de chargements incrémentaux, et des requêtes qui parcourent des tables non partitionnées ou non regroupées. Une quatrième : des requêtes BI en direct sans cache.

<!-- takeaways -->

- Le calcul domine ; les habitudes font le coût.
- Choisissez selon le contexte, les charges et les compétences.
- Une migration exige inventaire, traduction et validation.

<!-- unit: Données ouvertes et partage -->

<!-- goals -->

- Partager des données en direct sans copie.
- Expliquer ce que les formats de table ouverts changent pour les entrepôts.

<!-- concept -->

Copier des données pour les partager crée des doublons périmés et des failles de sécurité. Le partage zero-copy donne à d'autres comptes ou entreprises un accès en direct et en lecture seule aux mêmes données, gouverné par leur propriétaire.
Les formats de table ouverts poussent l'idée plus loin : entrepôts, Spark et autres moteurs lisent et écrivent les mêmes tables Iceberg ou Delta dans votre stockage, et l'entrepôt devient un moteur parmi d'autres plutôt qu'un stockage fermé.

<!-- example -->

```text
producer account: share sales.daily_revenue → partner account (read-only, live)
open tables: Iceberg in S3 ◄── Snowflake, Spark, Trino all read the same files
```

#### Qu'est-ce qu'une requête d'analyse de cohortes ?

Affecter chaque client à une cohorte (mois du premier achat), puis compter les clients actifs ou le chiffre d'affaires par cohorte et par mois depuis le premier achat, souvent pivoté en triangle de rétention.

#### Comment calculer une médiane ou un percentile ?

Avec `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x)` dans de nombreux moteurs, `MEDIAN()` dans Snowflake, ou `APPROX_PERCENTILE`/`APPROX_QUANTILES` pour de gros volumes.

<!-- challenge -->

Un partenaire reçoit chaque nuit un export CSV de 20 tables, souvent avec un jour de retard et parfois incomplet. Que proposez-vous ?

<!-- solution -->

Partager les tables préparées via le partage zero-copy de l'entrepôt (ou Delta Sharing / Iceberg via un catalogue), pour que le partenaire interroge des données en direct avec des permissions que vous contrôlez, sans transfert de fichiers.

<!-- takeaways -->

- Le partage zero-copy remplace les exports.
- Les formats ouverts permettent à plusieurs moteurs de partager des tables.
- L'entrepôt devient un moteur parmi d'autres.

<!-- stage: Restituer et gouverner -->

### Gouvernance et sécurité

<!-- unit: Modèles prêts pour la BI -->

<!-- goals -->

- Rendre les modèles de données adaptés aux outils et utilisateurs BI.
- Choisir entre rapports, tableaux de bord, requêtes en direct et extraits.

<!-- concept -->

Un modèle est prêt pour la BI quand un utilisateur métier peut construire un graphique juste sans rien demander à personne : noms clairs, mesures documentées, dimensions conformes et relations correctes. Les schémas en étoile s'intègrent naturellement aux outils BI.
La façon dont les données atteignent l'outil compte aussi. Les requêtes en direct gardent les données fraîches et la sécurité centralisée ; les extraits apportent la vitesse et soulagent l'entrepôt. Rapports et tableaux de bord servent des besoins différents, et le reverse ETL pousse les résultats dans les outils opérationnels où les gens travaillent déjà.

<!-- example -->

| Besoin | Choix |
|---|---|
| Liste réglementaire mensuelle | Rapport paginé |
| Suivi quotidien des KPI | Tableau de bord |
| Données qui changent toutes les quelques minutes | Requête en direct |
| 500 lecteurs, données quotidiennes | Extrait / cache |
| Les commerciaux ont besoin de scores dans le CRM | Reverse ETL |

#### Que sont `GROUPING SETS`, `ROLLUP` et `CUBE` ?

Des extensions de `GROUP BY` qui calculent plusieurs niveaux d'agrégation en une requête : `ROLLUP(year, month)` donne les totaux par mois, par année et le total général ; `CUBE` toutes les combinaisons ; `GROUPING SETS` liste les combinaisons exactes.

#### Qu'est-ce qu'une CTE, et quand l'utiliser ?

Une common table expression (`WITH nom AS (...)`) nomme une sous-requête pour la lisibilité et la réutilisation dans une requête ; les CTE récursives parcourent des hiérarchies. Elles facilitent la relecture du SQL complexe de l'entrepôt.

#### Comment éviter les erreurs de division par zéro ?

Utiliser `NULLIF(denominateur, 0)` pour obtenir `NULL` au lieu d'une erreur, ou des fonctions de division sûre (`SAFE_DIVIDE` dans BigQuery, `DIV0` dans Snowflake).

#### Quelle différence entre `WHERE` et `HAVING` ?

`WHERE` filtre les lignes avant l'agrégation ; `HAVING` filtre les groupes après l'agrégation. Filtrer tôt avec `WHERE` coûte moins cher.

<!-- challenge -->

Un tableau de bord consulté par 400 personnes par jour lance des requêtes en direct sur l'entrepôt à chaque ouverture, alors que les données changent une fois par jour. Que changez-vous ?

<!-- solution -->

Utiliser un extrait ou un jeu de données en cache rafraîchi après le chargement quotidien, pour que les lecteurs interrogent le cache et que l'entrepôt n'exécute les requêtes qu'une fois.

<!-- takeaways -->

- Noms clairs et étoiles rendent les modèles adaptés à la BI.
- Requêtes en direct pour la fraîcheur ; extraits pour la vitesse.
- Le reverse ETL livre les données dans les outils opérationnels.

<!-- unit: Self-service encadré -->

<!-- goals -->

- Permettre la BI en self-service tout en gardant des chiffres cohérents.
- Sécuriser les lignes, documenter les modèles et certifier les jeux de données.

<!-- concept -->

Le self-service permet aux utilisateurs métier de répondre eux-mêmes à leurs questions, ce qui passe bien mieux à l'échelle qu'une file de demandes. Sans garde-fous, il produit des métriques contradictoires et des données exposées. Les garde-fous : des jeux de données gouvernés et certifiés aux définitions documentées, une sécurité au niveau ligne qui suit l'utilisateur, et une documentation là où l'on regarde.
La certification est le signal dont les utilisateurs ont besoin : ce jeu est relu, testé et a un propriétaire.

<!-- example -->

```sql
-- row-level security (Snowflake row access policy)
CREATE ROW ACCESS POLICY region_rls AS (region STRING) RETURNS BOOLEAN ->
  EXISTS (SELECT 1 FROM security.user_regions u
          WHERE u.user_name = CURRENT_USER() AND u.region = region);
ALTER TABLE marts.fct_sales ADD ROW ACCESS POLICY region_rls ON (region);
```

#### Comment gérer les NULL dans les jointures et agrégations ?

`NULL` n'est égal à rien, donc les lignes à clé `NULL` ne se joignent pas (utilisez des membres inconnus ou `IS NOT DISTINCT FROM`) ; les agrégats ignorent les `NULL` sauf `COUNT(*)` ; utilisez `COALESCE` pour les valeurs par défaut à l'affichage.

#### Comment pivoter des lignes en colonnes en SQL ?

Avec une agrégation conditionnelle (`SUM(CASE WHEN channel = 'web' THEN amount END) AS web_amount`), portable entre moteurs, ou `PIVOT` quand il est pris en charge (Snowflake, SQL Server, BigQuery, Databricks).

#### Concevez un data mart des ventes pour une entreprise de e-commerce.

Processus métier : lignes de commande. Grain : une ligne par ligne de commande. Dimensions : date (commande, expédition), client (SCD2 sur segment et région), produit (SCD2 sur catégorie), magasin ou canal, promotion et une junk dimension pour les indicateurs ; dimension dégénérée le numéro de commande. Faits : quantité, montant brut, remise, montant net, coût, taxes. Ajouter ensuite un fait des retours et une photo quotidienne des stocks partageant les dimensions conformes.

#### La finance et les ventes rapportent des chiffres d'affaires différents. Comment résoudre le problème ?

Recenser la définition de chaque équipe (brut ou net, date de réservation ou d'expédition, conversion de devises, remboursements, annulations), suivre les deux chiffres jusqu'aux sources grâce au lignage, convenir d'une définition unique avec les responsables métier, l'implémenter une seule fois dans la couche sémantique ou un fait conforme, et retirer la logique divergente.

<!-- challenge -->

Les responsables régionaux ne doivent voir que les ventes de leur région dans tous les outils, pas seulement dans un tableau de bord. Où l'implémentez-vous ?

<!-- solution -->

Dans l'entrepôt, avec une row access policy (ou des vues sécurisées) pilotée par une table de correspondance utilisateur-région, pour que chaque outil qui interroge les données reçoive la même restriction. Les seuls filtres de l'outil se contournent facilement.

<!-- takeaways -->

- Le self-service exige des jeux gouvernés et certifiés.
- La sécurité au niveau ligne se place dans l'entrepôt.
- Documentez les définitions là où les utilisateurs regardent.

### SQL pour l'analytique

<!-- unit: Sécuriser les données de l'entrepôt -->

<!-- goals -->

- Sécuriser un entrepôt avec rôles, contrôles réseau et chiffrement.
- Gérer les données personnelles et fixer des politiques de rétention.

<!-- concept -->

La sécurité de l'entrepôt suit le moindre privilège : les rôles d'accès portent les privilèges sur les objets, les rôles fonctionnels les regroupent par métier, et les utilisateurs reçoivent des rôles fonctionnels via SSO. Restrictions réseau et chiffrement ajoutent des couches autour.
Les données personnelles exigent un traitement propre : les classifier et les taguer, ne charger que le nécessaire, pseudonymiser tôt et les masquer pour la plupart des utilisateurs. Les politiques de rétention décident combien de temps chaque jeu reste, pour des raisons légales et de coût.

<!-- example -->

```text
access roles:     sales_read, sales_write, pii_read
functional roles: analyst_sales = sales_read
                  data_engineer = sales_read + sales_write
users ← functional roles via SSO groups; pii_read only for a few
```

#### Le chargement quotidien d'une table de faits crée parfois des doublons. Comment corriger ?

Rendre le chargement idempotent (`MERGE` sur la clé du grain ou delete-insert de la fenêtre de chargement), dédupliquer le staging par clé naturelle, ajouter un test d'unicité au grain qui bloque la publication, et vérifier si l'extraction source a des fenêtres qui se chevauchent.

#### Une dimension doit historiser les changements de segment client, mais l'adresse change tous les jours. Que faites-vous ?

Suivre le segment en SCD2 dans la dimension client ; placer l'adresse dans une dimension ou mini-dimension séparée, ou la garder en type 1 si son historique n'est pas utile à l'analyse, pour éviter l'explosion quotidienne des lignes.

#### Comment migrer un entrepôt on-premise vers le cloud ?

Inventorier sources, jobs ETL, rapports et utilisateurs ; choisir la plateforme et l'architecture cibles ; migrer l'historique en masse ; reconstruire les pipelines en ELT (souvent avec dbt) plutôt qu'un simple « lift-and-shift » quand cela apporte de la valeur ; redéfinir sécurité et gouvernance ; valider par des rapports de rapprochement ; faire tourner en parallèle ; basculer les rapports par vagues ; décommissionner l'ancien système.

<!-- challenge -->

Tout analyste peut interroger les e-mails et numéros de téléphone bruts des clients. Que changez-vous sans casser leur travail ?

<!-- solution -->

Appliquer des politiques de masquage aux colonnes PII (visibles seulement d'un rôle privilégié), proposer des clés pseudonymisées pour jointures et comptages, et revoir qui a vraiment besoin des valeurs brutes.

<!-- takeaways -->

- Moindre privilège via rôles d'accès et fonctionnels.
- Classifiez, minimisez et masquez les données personnelles.
- Les politiques de rétention limitent risque légal et coût.

<!-- unit: Lignage et découverte -->

<!-- goals -->

- Utiliser lignage et catalogues pour rendre les données compréhensibles.
- Aider les analystes à trouver les bonnes tables.

<!-- concept -->

Quand un entrepôt grandit, trouver la bonne table devient le goulot. Un catalogue rend les jeux de données cherchables, avec descriptions, propriétaires et signaux de qualité ; le lignage montre d'où vient chaque table et ce qui en dépend, ce qui crée la confiance et soutient l'analyse d'impact.
L'organisation aide autant que l'outillage : schémas par couche et domaine, jeux certifiés et moins de tables quasi dupliquées.

<!-- example -->

```text
search "revenue" →
  marts.fct_revenue        ✔ certified · owner: finance-data · refreshed 06:40 · used by 34 dashboards
  sandbox.revenue_test_v2  ✘ uncertified · owner: a.lopez · last used 4 months ago
```

#### Les requêtes sur une table de faits de 5 ans ont ralenti avec la croissance des données. Que vérifiez-vous ?

Si les requêtes filtrent sur la colonne de partitionnement ou de clustering, la dégradation de l'organisation des données (profondeur de clustering, petits fichiers), les statistiques manquantes, de nouvelles jointures qui démultiplient les lignes, des requêtes BI sans filtre de date, et si des tables agrégées ou des vues matérialisées serviraient les usages courants.

#### Comment expliquer un entrepôt de données à un interlocuteur métier ?

C'est l'historique fiable et organisé des données de l'entreprise : les informations de tous les systèmes réunies, nettoyées et décrites une seule fois, pour que chacun réponde aux questions métier avec les mêmes chiffres.

#### Comment modéliser les abonnements d'une entreprise SaaS ?

Une dimension abonnement (offre, période de facturation, statut en SCD2), un fait transactionnel pour les événements d'abonnement (souscription, montée en gamme, descente, résiliation) et un fait en photo périodique mensuelle avec le MRR par client et par offre, permettant l'analyse du churn, de l'expansion et des cohortes.

<!-- challenge -->

Les analystes utilisent encore une ancienne table de CA non maintenue parce qu'elle apparaît en premier dans la recherche. Que faites-vous ?

<!-- solution -->

Certifier la table maintenue et marquer l'ancienne comme dépréciée dans le catalogue, la rediriger ou la remplacer par une vue sur la nouvelle, prévenir ses utilisateurs repérés dans les journaux de requêtes, puis la supprimer.

<!-- takeaways -->

- Les catalogues rendent les données trouvables et fiables.
- Le lignage soutient confiance et analyse d'impact.
- Certifiez les bonnes tables ; dépréciez les autres.

<!-- stage: Tout assembler -->

### Mises en situation

<!-- unit: Concevoir un mart des ventes -->

<!-- goals -->

- Concevoir de bout en bout un mart dimensionnel des ventes.
- Justifier les choix de grain, faits, dimensions et SCD.

<!-- concept -->

Une question de conception de data mart vérifie que vous savez appliquer la méthode sous pression. Commencez par le processus métier et le grain, listez les dimensions avec leurs politiques de changement, définissez les faits et leur additivité, puis couvrez chargement, qualité et usage par les utilisateurs. Dire ce que vous feriez des retours, des devises et des données tardives montre une expérience au-delà du manuel.

<!-- example -->

```text
process: order taking   grain: order line
dims: date (order, ship roles), customer (SCD2 segment), product (SCD2 category),
      store, promotion, junk flags
facts: quantity, gross, discount, net (additive), returns as negative lines
load: incremental MERGE on (order_number, line_number); tests on keys and relationships
```

#### Les analystes ne trouvent pas les bonnes tables. Que faites-vous ?

Organiser les schémas par couche et par domaine, documenter modèles et colonnes, certifier les jeux de données clés, publier un catalogue avec recherche et lignage, déprécier puis supprimer les tables historiques, et proposer une couche sémantique avec des indicateurs nommés en langage métier.

<!-- challenge -->

Le métier ajoute : « nous voulons aussi savoir quels produits les clients ont consultés sans les acheter. » Comment votre conception change-t-elle ?

<!-- solution -->

Ajouter un fait séparé pour les consultations produit (une ligne par événement de consultation, factless ou avec durée de visite), partageant les dimensions conformes client, produit et date, et le comparer aux ventes par drill-across.

<!-- takeaways -->

- Partez du processus et du grain, puis dimensions et faits.
- Traitez explicitement retours, devises et données tardives.
- Un nouveau processus, c'est un nouveau fait sur des dimensions conformes.

<!-- unit: Modéliser des abonnements -->

<!-- goals -->

- Modéliser une activité d'abonnement avec les bons types de faits.
- Calculer revenu récurrent et churn à partir du modèle.

<!-- concept -->

Les abonnements mêlent événements et états. Souscriptions, montées en gamme et résiliations sont des événements ; le revenu récurrent mensuel et le statut actif sont des états à un instant donné. Un bon modèle capture les deux : des faits transactionnels pour les changements et un periodic snapshot pour l'état mensuel, avec l'abonnement en dimension à évolution lente. Des métriques comme le MRR, le churn et l'expansion deviennent alors des requêtes simples plutôt que des reconstructions complexes.

<!-- example -->

```text
dim_subscription (plan, billing_period, status; SCD2)
fct_subscription_events (date, subscription, event_type, mrr_delta)
fct_subscription_monthly (month, subscription, customer, mrr, is_active)   ← periodic snapshot
churned MRR(month) = SUM(mrr) last month for subscriptions inactive this month
```

#### Comment concevoir l'entrepôt d'une entreprise qui acquiert souvent d'autres sociétés ?

Une couche d'intégration résiliente aux nouvelles sources (Data Vault ou un cœur bien structuré avec des tables de correspondance des sources), des dimensions conformes avec rapprochement des données de référence entre sociétés, des codes de système source sur chaque ligne, et des marts capables d'inclure ou d'exclure les entités acquises.

<!-- challenge -->

La finance veut le MRR tel que publié à chaque fin de mois, même si des corrections ultérieures modifient l'historique. Comment le permettre ?

<!-- solution -->

Rendre le snapshot mensuel immuable une fois le mois clos (ajouter une version corrigée du snapshot au lieu d'écraser), pour disposer du MRR « tel que publié » et « tel que corrigé ».

<!-- takeaways -->

- Événements en faits transactionnels ; états en snapshots.
- MRR et churn se lisent directement dans le snapshot.
- Figez les périodes closes quand les chiffres publiés comptent.
