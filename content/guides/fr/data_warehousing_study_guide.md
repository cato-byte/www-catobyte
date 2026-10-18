## Fiche d'étude Data Warehousing

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude data warehousing : environ 200 questions](../../images/data_warehousing_study_guide_title_img.png)

Environ 200 questions d'entretien sur l'entreposage de données : concepts clés, modélisation dimensionnelle avec faits et dimensions, dimensions à évolution lente, modes de chargement, qualité des données, architectures et moteurs d'entrepôt, performances, entrepôts cloud, BI et couche sémantique, avec des exemples SQL. Les réponses sont indépendantes des outils autant que possible, avec des remarques pour Snowflake, Redshift, BigQuery et Databricks. Ouvrez une question pour voir sa réponse, ou utilisez le filtre pour chercher dans toute la fiche.

<!-- QA -->

### Concepts clés

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

#### Qu'est-ce que la latence dans le contexte d'un entrepôt ?

Le délai entre un événement dans un système source et sa disponibilité dans les rapports : batch quotidien (heures), micro-batch (minutes) ou streaming (secondes). La bonne latence dépend des décisions métier, pas de la technologie.

#### Que sont les SLA d'un entrepôt de données ?

Des engagements comme « le mart des ventes est rafraîchi avant 7 h, heure locale, les jours ouvrés » ou « 99 % des chargements réussissent », avec supervision et communication en cas de manquement. Ils transforment les pipelines en produits sur lesquels les consommateurs peuvent compter.

### Bases de la modélisation dimensionnelle

#### Qu'est-ce que la modélisation dimensionnelle ?

La technique de Ralph Kimball pour concevoir des schémas analytiques autour des processus métier : des faits (mesures d'événements) entourés de dimensions (contexte descriptif). Elle privilégie la compréhension et les performances des requêtes plutôt que la normalisation.

#### Quelles sont les quatre étapes de la conception dimensionnelle selon Kimball ?

1) Choisir le processus métier (par exemple la prise de commande). 2) Déclarer le grain (ce que représente une ligne de faits). 3) Identifier les dimensions (qui, quoi, où, quand, pourquoi, comment). 4) Identifier les faits (mesures numériques à ce grain).

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

#### Pourquoi ne pas joindre directement deux tables de faits ?

Leurs grains diffèrent généralement, et les jointures directes produisent des fan-outs et des doubles comptes. Agrégez d'abord chaque fait au grain dimensionnel commun, puis combinez.

#### Qu'est-ce qu'une dimension heure de la journée ?

Une dimension séparée avec une ligne par minute ou seconde de la journée (heure, minute, tranche horaire), utilisée quand l'analyse par heure compte, ce qui garde la dimension date petite.

#### Comment nommer tables et colonnes dans un modèle dimensionnel ?

De façon cohérente et en langage métier : préfixes `fct_` et `dim_` (ou `fact_`/`dim_`), noms au singulier, `_key` pour les clés de substitution, `_id` pour les clés naturelles, unités explicites (`amount_eur`), et pas de jargon des systèmes sources dans les couches de présentation.

### Les faits en détail

#### Quels sont les trois types de tables de faits ?

Les faits transactionnels (une ligne par événement, comme une ligne de commande), les faits en photo périodique (une ligne par entité et par période, comme le solde d'un compte par jour) et les faits en photo cumulative (une ligne par instance de processus, mise à jour à chaque jalon, comme une commande de sa création à sa livraison).

#### Quand utiliser une table de faits en photo périodique ?

Pour mesurer des niveaux ou des états à intervalles réguliers (stocks, soldes, abonnements actifs par mois), quand additionner les transactions serait coûteux ou quand l'état ne se déduit pas des événements.

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

#### Comment gérer des faits de grains différents ?

Les placer dans des tables de faits séparées ; mélanger les grains (montants d'en-tête et de lignes de commande dans une même table) provoque des doubles comptes. Ne répartissez les valeurs d'en-tête sur les lignes que si une règle métier le justifie.

#### Quelle est la clé primaire d'une table de faits ?

Souvent la combinaison de ses clés de dimension et des dimensions dégénérées au grain déclaré, ou une clé de substitution de fait par commodité. Vérifier l'unicité au grain par un test est essentiel.

#### Que sont les tables de faits agrégées ?

Des versions résumées des faits atomiques à un grain plus grossier (ventes par mois et par catégorie) qui accélèrent les requêtes courantes. Elles doivent rester cohérentes avec la table atomique, et les outils BI ou les couches sémantiques peuvent y rediriger les requêtes.

#### Qu'est-ce qu'une table de faits consolidée ?

Une table de faits qui combine des faits de plusieurs processus au même grain (montants réels et budgétés par mois, compte et centre de coût), pratique pour comparer le réel au budget.

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

#### Quand utiliser une photo périodique plutôt que de déduire l'état des transactions ?

Quand calculer l'état à partir de toutes les transactions historiques est coûteux ou complexe (soldes, niveaux de stock, tickets ouverts), ou quand les systèmes sources fournissent des états mais pas d'historique complet des événements.

### Les dimensions en détail

#### Qu'est-ce qu'une dimension à rôles multiples (role-playing) ?

Une dimension physique utilisée plusieurs fois dans une table de faits avec des sens différents, typiquement la dimension date comme date de commande, d'expédition et de livraison, exposée via des vues ou des alias.

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

#### Qu'est-ce que la ligne « membre inconnu » ?

Une ligne spéciale de dimension (souvent de clé de substitution `-1` ou `0`) utilisée quand la dimension d'un fait est manquante ou pas encore connue, pour que les faits ne disparaissent pas dans les jointures internes et que le problème soit visible dans les rapports.

#### Qu'est-ce qu'une dimension réduite (shrunken) ?

Un sous-ensemble des lignes ou colonnes d'une dimension utilisé pour des faits agrégés à un grain supérieur, comme une dimension mois dérivée de la dimension date ou une dimension catégorie dérivée des produits.

#### Qu'est-ce qu'une dimension à évolution lente ?

Une dimension dont les attributs changent dans le temps de façon imprévisible (un client déménage, un produit change de catégorie), ce qui exige une politique pour savoir si et comment conserver l'historique.

#### Qu'est-ce qu'une dimension statique ?

Une dimension dont le contenu ne vient pas d'une source et change rarement, comme la dimension date, les tables de codes de statut ou les devises, générée une fois ou maintenue manuellement.

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

#### Qu'est-ce qu'une « vue courante » d'une dimension SCD2 ?

Une vue filtrant `is_current = true` qui donne une ligne par clé naturelle avec les attributs du jour, utilisée par les analystes qui n'ont pas besoin de l'historique et pour un reporting de type 1.

### Dimensions à évolution lente

#### Quels sont les types de SCD ?

Type 0 : ne change jamais (on garde l'original). Type 1 : écrasement, pas d'historique. Type 2 : une nouvelle ligne par changement avec dates de validité. Type 3 : une colonne « valeur précédente ». Type 4 : l'historique dans une table séparée (mini-dimension ou table d'historique). Type 6 : hybride des types 1, 2 et 3 (colonnes de valeur courante sur toutes les lignes plus lignes d'historique). Type 7 : double clé pour joindre aux lignes courantes ou historiques.

#### Comment fonctionne la SCD de type 2 ?

Quand un attribut suivi change, la ligne courante est clôturée (date de fin renseignée, indicateur courant à faux) et une nouvelle ligne est insérée avec une nouvelle clé de substitution, les nouvelles valeurs, une date de début et une date de fin ouverte. Les faits référencent la clé de substitution valide à leur date.

| customer_key | customer_id | city     | valid_from | valid_to   | is_current |
|---|---|---|---|---|---|
| 101 | C-42 | Lyon       | 2024-01-01 | 2026-03-31 | false |
| 187 | C-42 | Bordeaux   | 2026-04-01 | 9999-12-31 | true  |

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

#### Comment gérer un changement de dimension appris tardivement ?

Si l'on apprend aujourd'hui qu'un changement a eu lieu le mois dernier, on insère la version avec sa vraie date de début, on ajuste la date de fin de la ligne précédente et, éventuellement, on rattache à la nouvelle clé les faits survenus après le changement ; c'est pourquoi certaines équipes préfèrent les jointures temporelles au moment de la requête.

#### Qu'est-ce qu'un hash diff, et pourquoi l'utiliser ?

Un hachage (MD5, SHA) des attributs suivis concaténés, stocké sur chaque ligne, pour que la détection des changements soit une seule comparaison au lieu de comparer de nombreuses colonnes, avec une gestion sûre des nulls.

#### Comment les snapshots dbt implémentent-ils la SCD2 ?

La configuration du snapshot définit la clé unique et une stratégie (`timestamp` avec une colonne de mise à jour, ou `check` qui compare des colonnes) ; chaque exécution compare la source à la table de snapshot, clôture et insère des lignes, et ajoute `dbt_valid_from` et `dbt_valid_to`.

#### Comment tester une dimension SCD2 ?

Vérifier que chaque clé naturelle a exactement une ligne courante, que les périodes de validité ne se chevauchent pas et ne laissent pas de trous, que `valid_from < valid_to`, que les clés de substitution sont uniques et que les clés de substitution des faits existent dans la dimension.

#### Qu'est-ce qu'une SCD2 à l'horodatage par rapport à une granularité journalière ?

Certaines dimensions suivent les changements à la précision de l'horodatage (plusieurs changements par jour), d'autres au jour (dernière valeur de la journée). Choisissez selon la façon dont les faits sont rapprochés ; la granularité journalière est plus simple et suffit généralement.

#### Peut-on rattacher des faits à de nouvelles versions de dimension ?

Normalement non : les faits gardent la version valide au moment où ils ont eu lieu. Pour un reporting « à la date d'aujourd'hui », joignez par la clé naturelle à la ligne courante ou utilisez les colonnes de valeur courante du type 6.

### Alimentation de l'entrepôt

#### Qu'est-ce qu'un chargement complet par rapport à un chargement incrémental ?

Un chargement complet recharge toutes les données à chaque exécution (simple, coûteux, adapté aux petites tables). Un chargement incrémental ne traite que les données nouvelles ou modifiées depuis la dernière exécution (par horodatage, séquence ou CDC), ce qui est indispensable pour les grosses tables.

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

### Qualité des données

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

### Architectures d'entrepôt

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

#### Quel lien entre l'architecture médaillon et l'entreposage ?

C'est un modèle en couches du lakehouse (bronze brut, silver nettoyé et harmonisé, gold prêt pour le métier) qui correspond aux couches staging, intégration et présentation ; gold contient souvent des schémas en étoile à la Kimball.

#### Qu'est-ce qu'une couche sémantique ?

Une couche qui définit une seule fois les indicateurs, dimensions et relations métier (couche sémantique de dbt, LookML, Cube, modèles sémantiques Power BI, AtScale, metric views) pour que tous les outils calculent le « chiffre d'affaires » de la même façon.

#### Qu'est-ce qu'un cube OLAP ?

Une structure multidimensionnelle qui précalcule des agrégats selon les dimensions pour des analyses rapides. Le MOLAP stocke les cubes dans un stockage spécialisé (SSAS), le ROLAP interroge des tables relationnelles et l'HOLAP mélange les deux. Les entrepôts cloud en colonnes ont réduit le besoin de cubes physiques.

#### Qu'est-ce qu'un entrepôt virtuel ou la virtualisation des données ?

L'interrogation sur place de données de plusieurs sources via une couche de virtualisation (Denodo, Trino, requêtes fédérées) sans les consolider physiquement. C'est rapide pour intégrer, mais les performances et l'historique sont limités.

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

#### Que sont les tables point-in-time (PIT) en Data Vault ?

Des tables auxiliaires qui stockent, pour chaque clé de hub et chaque date de photo, les dates de chargement des satellites correspondants, ce qui accélère la reconstitution de l'état d'une entité à une date donnée pour les dimensions.

### Moteurs et stockage

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

### Performances

#### Comment rendre rapide une requête sur un schéma en étoile ?

Filtrer sur les colonnes de partitionnement ou de clustering (date), joindre les faits à de petites dimensions (broadcast), ne sélectionner que les colonnes utiles, pré-agréger les requêtes courantes, tenir les statistiques à jour et éviter les fonctions sur les colonnes filtrées.

#### Qu'est-ce qui provoque un « fan-out » ou un double comptage dans les jointures ?

Joindre un fait à une table qui a plusieurs lignes par clé (plusieurs-à-plusieurs ou mauvais grain), de sorte que chaque ligne de fait est dupliquée et que les sommes gonflent. Vérifiez la cardinalité des jointures et imposez l'unicité des clés de dimension.

#### Comment accélérer `COUNT(DISTINCT)` sur de gros volumes ?

Utiliser des fonctions approximatives (HyperLogLog : `APPROX_COUNT_DISTINCT`), pré-agréger des ensembles distincts par période, ou maintenir des comptes distincts dans des tables agrégées quand des valeurs exactes sont nécessaires.

#### Pourquoi des tables larges dénormalisées peuvent-elles être rapides dans un moteur en colonnes ?

Parce que seules les colonnes référencées par la requête sont lues : une table large ne coûte pas plus à interroger qu'une étroite de même nombre de lignes, et elle évite des jointures. Les coûts sont le stockage, la maintenance et le risque d'incohérence.

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

#### Comment éviter des `SELECT DISTINCT` coûteux dans les modèles ?

Chercher pourquoi les doublons apparaissent (une jointure au mauvais grain) et corriger la jointure plutôt que de la masquer avec `DISTINCT`, coûteux et qui cache des problèmes de données.

#### Comment tester les performances de l'entrepôt avant la mise en production ?

Rejouer des requêtes représentatives et la concurrence sur des données de taille réelle, mesurer la latence et le coût par requête, vérifier l'élagage et les jointures dans les plans, et ajuster l'organisation, les agrégats et le dimensionnement.

#### Comment les modèles incrémentaux réduisent-ils les coûts de l'entrepôt ?

En ne transformant à chaque exécution que les données nouvelles ou modifiées au lieu de reconstruire des tables entières, ce qui réduit fortement le calcul sur les gros faits ; ils exigent une gestion soignée des données tardives et des backfills.

### Entrepôts cloud

#### Quels sont les principaux entrepôts cloud ?

Snowflake, Google BigQuery, Amazon Redshift (provisionné et Serverless), les entrepôts Azure Synapse et Microsoft Fabric, et Databricks SQL sur le lakehouse. Ils diffèrent par leur architecture, leurs modèles de prix et leur intégration à l'écosystème.

#### Comment fonctionne BigQuery et comment est-il facturé ?

BigQuery est serverless : stockage dans un format en colonnes (Capacitor) sur Colossus, calcul alloué en slots par Dremel. Il est facturé à la demande au To lu ou à la capacité (éditions avec slots réservés ou en autoscaling), plus le stockage.

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

#### Comment BigQuery gère-t-il le partitionnement et le clustering ?

Les tables peuvent être partitionnées par une colonne date/horodatage, par temps d'ingestion ou par plage d'entiers, et regroupées sur jusqu'à quatre colonnes ; les requêtes filtrant dessus lisent moins d'octets, ce qui réduit directement le coût à la demande.

#### Qu'est-ce que Redshift Spectrum ?

Une fonction qui permet à Redshift d'interroger des données S3 via des tables externes du Glue Data Catalog, en joignant les données du lake aux tables de l'entrepôt, facturée à l'octet lu.

#### Qu'est-ce que l'entrepôt de Microsoft Fabric ?

Une plateforme analytique SaaS où entrepôts et lakehouses stockent les données au format Delta dans OneLake, interrogées en T-SQL et en Spark et servies à Power BI en mode Direct Lake.

#### Qu'est-ce que Databricks SQL en tant qu'entrepôt ?

Des SQL warehouses sur le lakehouse Databricks qui interrogent des tables Delta gouvernées par Unity Catalog, avec Photon, du calcul serverless et des connecteurs BI, offrant les fonctions d'un entrepôt sur un stockage ouvert.

### BI et consommation

#### Qu'est-ce qui rend un modèle de données adapté à la BI ?

Des schémas en étoile aux noms clairs, des définitions métier documentées, des dimensions conformes, des grains corrects, des clés de substitution cachées aux utilisateurs, une gestion cohérente des dates et une couche sémantique pour les indicateurs.

#### Quelle différence entre un rapport et un tableau de bord ?

Un rapport présente des données détaillées, souvent tabulaires et paginées, pour l'analyse ou des besoins réglementaires. Un tableau de bord résume visuellement les indicateurs clés pour un suivi en un coup d'œil, avec exploration.

#### Qu'est-ce que la BI en libre-service, et quels sont ses risques ?

Des utilisateurs métier qui construisent leurs propres analyses à partir de jeux de données gouvernés. Risques : définitions d'indicateurs incohérentes, logique dupliquée, extraits et coûts non maîtrisés. Une couche sémantique, des jeux de données certifiés et de la formation les réduisent.

#### Qu'est-ce que la sécurité au niveau ligne dans la BI et les entrepôts ?

Restreindre les lignes visibles par chaque utilisateur selon son identité (région, département), dans l'entrepôt (row access policies, vues sécurisées) ou dans la couche BI, pour qu'un même jeu de données serve de nombreux publics en toute sécurité.

#### Comment documenter un entrepôt ?

Avec des descriptions de tables et de colonnes dans le catalogue (dbt docs, Unity Catalog, Glue, DataHub), un glossaire métier pour les indicateurs, des graphes de lignage, les responsables et les SLA, et des exemples de requêtes correctes.

#### Qu'est-ce qu'un jeu de données certifié ?

Un jeu de données marqué comme fiable après revue (définitions, tests, responsable), mis en avant dans les outils BI et les catalogues pour que les utilisateurs le préfèrent aux copies personnelles ou expérimentales.

#### Qu'est-ce que le reverse ETL ?

Le renvoi de données de l'entrepôt (segments, scores, indicateurs) vers des outils opérationnels comme les CRM, les plateformes marketing ou de support, pour que les équipes métier agissent sur des données modélisées (Hightouch, Census, jobs maison).

#### Comment choisir entre requêtes en direct et extraits dans les outils BI ?

Les requêtes en direct donnent des données fraîches et une sécurité centralisée mais dépendent des performances et du coût de l'entrepôt ; les extraits (extraits Tableau, import Power BI, SPICE) sont rapides et peu coûteux par requête mais périmés et dupliqués. On choisit par tableau de bord selon le besoin de fraîcheur et l'usage.

### Gouvernance et sécurité

#### Comment sécuriser un entrepôt de données ?

Rôles au moindre privilège (rôles d'accès accordés à des rôles fonctionnels), SSO et MFA, restrictions réseau, chiffrement au repos et en transit, masquage des colonnes sensibles, sécurité au niveau ligne, audit des accès et environnements séparés pour le développement et la production.

#### Comment traiter les données personnelles dans un entrepôt ?

Les classifier et les taguer, minimiser ce qui est chargé, pseudonymiser ou tokeniser tôt les identifiants, masquer pour la plupart des utilisateurs, restreindre l'accès brut, appliquer des politiques de rétention et traiter les demandes d'effacement (RGPD) avec des processus documentés.

#### Qu'est-ce que le lignage des données, et pourquoi compte-t-il ?

La trace de l'origine des données et de leurs transformations, au niveau table et colonne. Il sert à l'analyse d'impact avant un changement, au débogage de chiffres faux, aux audits et à la confiance.

#### Qu'est-ce qu'un catalogue de données ?

Un inventaire consultable des jeux de données avec descriptions, responsables, schémas, tags, lignage, état de qualité et usage, qui aide à trouver et comprendre les données (DataHub, Collibra, Alation, Unity Catalog, Glue Data Catalog).

#### Que sont les politiques de rétention des données ?

Des règles fixant la durée de conservation de chaque jeu de données (pour des raisons légales, métier et de coût), mises en œuvre par la suppression de partitions, des règles de cycle de vie, les réglages de Time Travel et l'archivage, et documentées pour la conformité.

### SQL pour l'analytique

#### Que sont les fonctions de fenêtre, et pourquoi sont-elles essentielles en entreposage ?

Des fonctions qui calculent des valeurs sur un ensemble de lignes liées à la ligne courante sans les regrouper (`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`, `SUM() OVER`). Elles servent à dédupliquer, calculer des cumuls, comparer des périodes et reconstituer des sessions.

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

#### Qu'est-ce qu'une requête d'analyse de cohortes ?

Affecter chaque client à une cohorte (mois du premier achat), puis compter les clients actifs ou le chiffre d'affaires par cohorte et par mois depuis le premier achat, souvent pivoté en triangle de rétention.

#### Comment calculer une médiane ou un percentile ?

Avec `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x)` dans de nombreux moteurs, `MEDIAN()` dans Snowflake, ou `APPROX_PERCENTILE`/`APPROX_QUANTILES` pour de gros volumes.

#### Que sont `GROUPING SETS`, `ROLLUP` et `CUBE` ?

Des extensions de `GROUP BY` qui calculent plusieurs niveaux d'agrégation en une requête : `ROLLUP(year, month)` donne les totaux par mois, par année et le total général ; `CUBE` toutes les combinaisons ; `GROUPING SETS` liste les combinaisons exactes.

#### Qu'est-ce qu'une CTE, et quand l'utiliser ?

Une common table expression (`WITH nom AS (...)`) nomme une sous-requête pour la lisibilité et la réutilisation dans une requête ; les CTE récursives parcourent des hiérarchies. Elles facilitent la relecture du SQL complexe de l'entrepôt.

#### Comment éviter les erreurs de division par zéro ?

Utiliser `NULLIF(denominateur, 0)` pour obtenir `NULL` au lieu d'une erreur, ou des fonctions de division sûre (`SAFE_DIVIDE` dans BigQuery, `DIV0` dans Snowflake).

#### Quelle différence entre `WHERE` et `HAVING` ?

`WHERE` filtre les lignes avant l'agrégation ; `HAVING` filtre les groupes après l'agrégation. Filtrer tôt avec `WHERE` coûte moins cher.

#### Comment gérer les NULL dans les jointures et agrégations ?

`NULL` n'est égal à rien, donc les lignes à clé `NULL` ne se joignent pas (utilisez des membres inconnus ou `IS NOT DISTINCT FROM`) ; les agrégats ignorent les `NULL` sauf `COUNT(*)` ; utilisez `COALESCE` pour les valeurs par défaut à l'affichage.

#### Comment pivoter des lignes en colonnes en SQL ?

Avec une agrégation conditionnelle (`SUM(CASE WHEN channel = 'web' THEN amount END) AS web_amount`), portable entre moteurs, ou `PIVOT` quand il est pris en charge (Snowflake, SQL Server, BigQuery, Databricks).

### Mises en situation

#### Concevez un data mart des ventes pour une entreprise de e-commerce.

Processus métier : lignes de commande. Grain : une ligne par ligne de commande. Dimensions : date (commande, expédition), client (SCD2 sur segment et région), produit (SCD2 sur catégorie), magasin ou canal, promotion et une junk dimension pour les indicateurs ; dimension dégénérée le numéro de commande. Faits : quantité, montant brut, remise, montant net, coût, taxes. Ajouter ensuite un fait des retours et une photo quotidienne des stocks partageant les dimensions conformes.

#### La finance et les ventes rapportent des chiffres d'affaires différents. Comment résoudre le problème ?

Recenser la définition de chaque équipe (brut ou net, date de réservation ou d'expédition, conversion de devises, remboursements, annulations), suivre les deux chiffres jusqu'aux sources grâce au lignage, convenir d'une définition unique avec les responsables métier, l'implémenter une seule fois dans la couche sémantique ou un fait conforme, et retirer la logique divergente.

#### Le chargement quotidien d'une table de faits crée parfois des doublons. Comment corriger ?

Rendre le chargement idempotent (`MERGE` sur la clé du grain ou delete-insert de la fenêtre de chargement), dédupliquer le staging par clé naturelle, ajouter un test d'unicité au grain qui bloque la publication, et vérifier si l'extraction source a des fenêtres qui se chevauchent.

#### Une dimension doit historiser les changements de segment client, mais l'adresse change tous les jours. Que faites-vous ?

Suivre le segment en SCD2 dans la dimension client ; placer l'adresse dans une dimension ou mini-dimension séparée, ou la garder en type 1 si son historique n'est pas utile à l'analyse, pour éviter l'explosion quotidienne des lignes.

#### Comment migrer un entrepôt on-premise vers le cloud ?

Inventorier sources, jobs ETL, rapports et utilisateurs ; choisir la plateforme et l'architecture cibles ; migrer l'historique en masse ; reconstruire les pipelines en ELT (souvent avec dbt) plutôt qu'un simple « lift-and-shift » quand cela apporte de la valeur ; redéfinir sécurité et gouvernance ; valider par des rapports de rapprochement ; faire tourner en parallèle ; basculer les rapports par vagues ; décommissionner l'ancien système.

#### Les requêtes sur une table de faits de 5 ans ont ralenti avec la croissance des données. Que vérifiez-vous ?

Si les requêtes filtrent sur la colonne de partitionnement ou de clustering, la dégradation de l'organisation des données (profondeur de clustering, petits fichiers), les statistiques manquantes, de nouvelles jointures qui démultiplient les lignes, des requêtes BI sans filtre de date, et si des tables agrégées ou des vues matérialisées serviraient les usages courants.

#### Comment expliquer un entrepôt de données à un interlocuteur métier ?

C'est l'historique fiable et organisé des données de l'entreprise : les informations de tous les systèmes réunies, nettoyées et décrites une seule fois, pour que chacun réponde aux questions métier avec les mêmes chiffres.

#### Comment modéliser les abonnements d'une entreprise SaaS ?

Une dimension abonnement (offre, période de facturation, statut en SCD2), un fait transactionnel pour les événements d'abonnement (souscription, montée en gamme, descente, résiliation) et un fait en photo périodique mensuelle avec le MRR par client et par offre, permettant l'analyse du churn, de l'expansion et des cohortes.

#### Les analystes ne trouvent pas les bonnes tables. Que faites-vous ?

Organiser les schémas par couche et par domaine, documenter modèles et colonnes, certifier les jeux de données clés, publier un catalogue avec recherche et lignage, déprécier puis supprimer les tables historiques, et proposer une couche sémantique avec des indicateurs nommés en langage métier.

#### Comment concevoir l'entrepôt d'une entreprise qui acquiert souvent d'autres sociétés ?

Une couche d'intégration résiliente aux nouvelles sources (Data Vault ou un cœur bien structuré avec des tables de correspondance des sources), des dimensions conformes avec rapprochement des données de référence entre sociétés, des codes de système source sur chaque ligne, et des marts capables d'inclure ou d'exclure les entités acquises.
