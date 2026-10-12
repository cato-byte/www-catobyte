---
title: Lakehouse des registres d'entreprises européens
summary: Intégration des registres d'entreprises ouverts de six pays européens dans un lakehouse Data Vault 2.0 sur Databricks et AWS, avec des tables gold nettoyées et géocodées.
started: 2026-07
updated: 2026-10-12
status: in_progress
stack: [PySpark, Databricks Serverless, Delta Lake, AWS Lambda, Amazon S3, AWS Location Service, Data Vault 2.0]
cover: images/projects/eu-company-registry.png
cover_alt: Six registres nationaux d'entreprises traversant les couches landing, bronze, staging, vault et gold
repo: https://github.com/cato-byte/eu-company-registry-lakehouse
---

## En bref

<ul class="stats"><li><strong>6</strong><span>registres nationaux (FR, IE, UK, NO, EE, ES)</span></li><li><strong>5</strong><span>couches de pipeline, de landing à gold</span></li><li><strong>6</strong><span>entités Data Vault : hubs, link, satellites</span></li><li><strong>2</strong><span>tables gold pour l'analytique</span></li></ul>

## Le problème

La plupart des pays européens publient leur registre d'entreprises en open data, mais chacun à sa façon. Les formats vont du CSV au JSON compressé, les délimiteurs de la virgule au point-virgule. Les noms de colonnes sont en français, en norvégien ou en estonien, et les dates, formes juridiques et codes de statut ont chacun leurs conventions. Les identifiants ne sont uniques qu'à l'intérieur de leur propre pays.

L'objectif du projet est un modèle unique et interrogeable des entreprises de six pays. On doit pouvoir demander « combien d'entreprises actives par secteur et par pays ? » ou les placer sur une carte, sans connaître la structure de chaque registre.

## Sources de données

| Pays | Registre | Producteur | Format | Clé métier |
|---|---|---|---|---|
| France | Base SIRENE, établissements | INSEE via data.gouv.fr | CSV (zip) | SIRET, à défaut SIREN |
| Irlande | Registre des sociétés | Companies Registration Office (CRO) | CSV | Numéro de société |
| Royaume-Uni | Basic Company Data | Companies House | CSV (zip) | Numéro de société |
| Norvège | Enhetsregisteret | Brønnøysund Register Centre | JSON (gzip) | Organisasjonsnummer |
| Estonie | Registre du commerce, données de base | Centre des registres et des systèmes d'information (RIK) | CSV (zip, délimité par `;`) | Code d'immatriculation |
| Espagne | Établissements de Navarre | Open data du Gouvernement de Navarre | CSV | NIF (DNI/CIF) |

<div class="callout"><p><strong>Une réalité des données, pas un bug :</strong> l'Espagne ne propose pas de téléchargement gratuit en masse de son registre national, la partie espagnole provient donc du portail open data régional de Navarre. La France et la Navarre publient par ailleurs des <em>établissements</em> (sites) plutôt que des personnes morales, si bien que leur granularité diffère de celle des quatre autres sources. Le modèle en tient compte au lieu de le masquer.</p></div>

## Architecture

<ol class="pipeline"><li><strong>Ingestion</strong><span>Une seule Lambda générique télécharge chaque registre, le décompresse et dépose les fichiers bruts dans S3, partitionnés par pays.</span><span class="tool">AWS Lambda · S3</span></li><li><strong>Bronze</strong><span>Les fichiers sont lus avec des schémas explicites et stockés 1:1 en tables Delta.</span><span class="tool">PySpark · Delta Lake</span></li><li><strong>Staging</strong><span>Chaque source est mappée vers un modèle canonique, nettoyée et dotée de ses clés de hachage Data Vault.</span><span class="tool">PySpark</span></li><li><strong>Raw Vault</strong><span>Hubs, links et satellites intègrent les six pays dans un seul modèle.</span><span class="tool">Data Vault 2.0 · Delta</span></li><li><strong>Gold</strong><span>État le plus récent de chaque entreprise, géocodage incrémental, plus une dimension et une table de faits analytiques.</span><span class="tool">PySpark · AWS Location Service</span></li><li><strong>Restitution</strong><span>Carte et tableau de bord sur les tables gold. Un prototype est en cours de développement.</span><span class="tool">Leaflet · JavaScript</span></li></ol>

Tout s'exécute sur le **calcul serverless de Databricks sur AWS**, en lecture et écriture sur S3. Aucun cluster à dimensionner ni à maintenir allumé pour un traitement batch lancé ponctuellement.

## Choix clés et leurs raisons

1. **Une seule fonction d'ingestion pilotée par configuration.** Une unique Lambda gère tous les pays. Chaque source est une petite requête JSON (URL, pays, fichier cible) : ajouter un pays revient à ajouter un fichier de configuration, pas du code. Les téléchargements sont écrits sur disque par blocs de 64 Ko, ce qui garde la mémoire stable même pour des registres de plusieurs gigaoctets, et les archives ZIP sont détectées et extraites à la volée.
2. **Des schémas explicites, stockés à côté des données.** Chaque source a un schéma Spark `StructType` en JSON, donc rien ne repose sur `inferSchema`. On évite une lecture complète supplémentaire de gros fichiers, on obtient les mêmes types à chaque exécution, et toute dérive de schéma fait échouer la couche bronze de façon visible au lieu de corrompre silencieusement les tables en aval.
3. **Un stockage Delta Lake en couches.** Landing conserve les fichiers intacts, et bronze, staging, vault et gold sont des tables Delta. Chaque couche peut être reconstruite à partir de la précédente, et quand une valeur semble fausse je peux retrouver la couche exacte où elle a changé.
4. **Un modèle de staging canonique.** Les six sources sont mappées vers les mêmes 14 colonnes métier (identifiant, nom, forme juridique, statut, secteur, effectifs, adresse…) plus des colonnes de lignage (`source_country`, `record_source`, `load_timestamp`). La logique propre à chaque source tient dans un seul `select` par pays, et tout ce qui suit le staging est indépendant du pays.
5. **Des clés métier limitées au pays.** Les identifiants nationaux ne sont uniques qu'au sein de leur registre. Un numéro de société britannique peut coïncider avec un numéro irlandais, c'est pourquoi la clé de hachage combine le pays *et* l'identifiant.
6. **Data Vault 2.0 pour l'intégration.** Six sources aux attributs et rythmes de changement différents se rangent naturellement en hubs (clés métier), links (relations) et satellites (attributs descriptifs avec `hash_diff`). Une nouvelle source ajoute des lignes, pas une migration de schéma.
7. **Le géocodage comme satellite incrémental.** Appeler une API de géocodage est la seule étape du pipeline qui coûte de l'argent par enregistrement. Les nouvelles adresses sont repérées par une jointure `left_anti` sur les coordonnées déjà stockées, géocodées via AWS Location Service (avec OpenStreetMap en secours), puis ajoutées à un satellite. Aucune adresse n'est géocodée deux fois.

```python
# Clés Data Vault limitées au pays, générées dans la couche staging
.withColumn("hk_company", md5(concat_ws("||", col("source_country"), col("national_id"))))
.withColumn("hk_location", md5(concat_ws("||",
    coalesce(col("address_line"), lit("")),
    coalesce(col("postal_code"), lit("")),
    col("source_country"),
)))
```

## Nettoyage des données

| Problème dans les données sources | Exemple | Règle appliquée |
|---|---|---|
| Quatre formats de date différents | `2024-03-01`, `01/03/2024`, `01.03.2024` | Chaque motif essayé tour à tour avec `coalesce(to_date(...))` |
| Données parasites dans les adresses | URL, e-mails, téléphones, coordonnées | Un filtre regex les remplace par `NULL` |
| Effectifs publiés en tranches | `de 20 a 49` | Milieu de la tranche (34,5), pour pouvoir les additionner |
| Statut publié en booléens | `konkurs`, `underAvvikling` en Norvège | Converti en `BANKRUPT`, `LIQUIDATION`, `ACTIVE` |
| Champs décalés par des délimiteurs parasites | Lignes estoniennes avec `;` dans la clé | Découpage puis récupération de la clé et du nom |
| Clés métier absentes ou factices | vide, `NONE` | Écartées *avant* le hachage |
| Casse et espaces incohérents | noms, villes | Espaces supprimés, passage en majuscules |

## Modèle Data Vault

<div class="vault"><div class="vault-entity vault-hub"><p class="kind">Hub</p><p class="name">hub_company</p><p class="cols">hk_company · national_id · source_country</p></div><div class="vault-entity vault-link"><p class="kind">Link</p><p class="name">link_company_location</p><p class="cols">hk_link · hk_company · hk_location</p></div><div class="vault-entity vault-hub"><p class="kind">Hub</p><p class="name">hub_location</p><p class="cols">hk_location · address_line · postal_code · city</p></div><div class="vault-entity vault-sat"><p class="kind">Satellite</p><p class="name">sat_company_profile</p><p class="cols">nom · forme juridique · statut · date d'immatriculation · TVA</p></div><div class="vault-entity vault-sat"><p class="kind">Satellite</p><p class="name">sat_company_metrics</p><p class="cols">code d'activité · libellé · effectifs</p></div><div class="vault-entity vault-sat"><p class="kind">Satellite</p><p class="name">sat_location_geocodes</p><p class="cols">latitude · longitude · source du géocodage</p></div></div>

Le profil et les indicateurs sont dans des satellites séparés car ils évoluent à des rythmes différents. Le nom et le statut d'une entreprise changent rarement, alors que les effectifs sont mis à jour chaque année.

## Déduplication

Les doublons apparaissent à plusieurs niveaux, et chacun est traité là où il se produit :

- **Au sein d'un registre :** les hubs sont dédoublonnés sur leur clé de hachage, si bien qu'une entreprise n'apparaît qu'une fois même si la source la répète.
- **Entre chargements :** les satellites conservent toutes les versions. La couche gold retient la plus récente pour chaque entreprise grâce à une fenêtre point-in-time (`row_number()` sur `load_timestamp`).
- **Entre entreprises partageant une adresse :** `hub_location` a pour clé l'adresse normalisée, donc un immeuble de bureaux partagé par cinquante entreprises n'est stocké et géocodé qu'une fois.
- **Démultiplication dans les jointures :** gold conserve une seule localisation courante par entreprise, de sorte que les jointures ne multiplient jamais les lignes.

```python
# Point-in-time : dernier enregistrement satellite par entreprise
latest = Window.partitionBy("hk_company").orderBy(col("load_timestamp").desc())
latest_profile = (
    sat_profile.withColumn("rn", row_number().over(latest))
    .filter(col("rn") == 1)
    .drop("rn")
)
```

## Tables gold

**`dim_companies`** : une ligne par entreprise, avec son profil, ses indicateurs, son adresse et ses coordonnées actuels.

| Colonne | Description |
|---|---|
| `company_key` | Clé de hachage du vault (pays + identifiant national) |
| `national_id`, `source_country`, `record_source` | Identité et lignage |
| `company_name`, `legal_form_code`, `company_status`, `registration_date` | Profil le plus récent |
| `industry_code`, `employee_count` | Indicateurs les plus récents |
| `address_line`, `postal_code`, `city`, `latitude`, `longitude` | Localisation actuelle, géocodée |

**`fact_country_industry_metrics`** : un agrégat par `source_country`, `industry_code` et `company_status`, avec `total_companies` et `total_employees`. Il alimente directement les tableaux de bord sans parcourir des millions de lignes.

<!-- bars: companies_by_country.csv -->

<!-- table: fact_country_industry_metrics_sample.csv -->

## Prochaines étapes

- **Des chargements qui conservent l'historique.** Les tables du vault sont aujourd'hui reconstruites à chaque exécution. L'étape suivante : des satellites en insertion seule avec un `MERGE` sur `hash_diff`, pour garder chaque évolution d'un registre dans le temps.
- **Des référentiels communs.** Ramener les codes de statut de toutes les sources à un seul jeu de valeurs, et agréger les codes d'activité aux sections NACE Rév. 2. SIC 2007 (Royaume-Uni), NAF (France), SN2007 (Norvège) et CNAE-2009 (Espagne) dérivent tous de la NACE et peuvent donc être alignés.
- **Résolution d'entités transfrontalière.** Rapprocher un même groupe présent dans plusieurs pays par correspondance approximative du nom et de l'adresse, car seuls certains registres publient le numéro de TVA.
- **Industrialisation.** Des contrôles de qualité des données sur chaque couche, une orchestration en job Databricks et l'infrastructure AWS décrite en code avec Terraform.
- **Tableau de bord.** Finaliser la carte Leaflet et les filtres sur les tables gold.
