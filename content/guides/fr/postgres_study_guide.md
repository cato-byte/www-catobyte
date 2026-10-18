## Fiche d'étude PostgreSQL

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude PostgreSQL : environ 200 questions](../../images/postgres_study_guide_title_img.png)

Environ 200 questions sur PostgreSQL et le SQL pour les entretiens de data engineer : architecture, types de données, requêtes, fonctions de fenêtrage, index, transactions et MVCC, optimisation des performances, modélisation des données, administration et fonctionnalités avancées comme JSONB et le partitionnement. Les exemples ciblent PostgreSQL 16 et 17. Ouvrez une question pour voir sa réponse, ou utilisez le filtre pour chercher dans toute la fiche.

<!-- QA -->

### Bases et architecture

#### Qu'est-ce que PostgreSQL ?

Un système de gestion de bases de données objet-relationnel open source, reconnu pour son respect des standards, sa fiabilité et son extensibilité. Il prend en charge les transactions ACID, le MVCC, des types de données riches (JSONB, tableaux, intervalles), le SQL avancé (fonctions de fenêtrage, CTE), les extensions et plusieurs types d'index.

#### Que signifie ACID ?

Les propriétés que doivent avoir les transactions d'une base de données, essentielles dans les systèmes OLTP, pour garder des données valides malgré les erreurs et les pannes :

- **Atomicité :** une transaction est une unité qui réussit entièrement ou n'a aucun effet.
- **Cohérence :** une transaction fait passer la base d'un état valide à un autre, en respectant les contraintes.
- **Isolation :** les transactions concurrentes n'interfèrent pas entre elles : le résultat est comme si elles s'étaient exécutées dans un certain ordre, selon le niveau d'isolation.
- **Durabilité :** une fois validée, une transaction survit aux pannes (dans PostgreSQL, grâce au journal d'écriture anticipée, le WAL).

#### Quelle est l'architecture des processus de PostgreSQL ?

Un processus postmaster accepte les connexions et crée un processus backend par connexion cliente. Des processus d'arrière-plan gèrent l'écriture (background writer, checkpointer), l'écriture du WAL, l'autovacuum, les statistiques et la réplication. Tous partagent de la mémoire, comme `shared_buffers`.

#### Pourquoi le modèle « un processus par connexion » est-il important ?

Chaque connexion coûte de la mémoire et un processus : des milliers de connexions directes dégradent les performances. Les applications utilisent un pool de connexions comme PgBouncer ou celui du pilote.

#### Qu'est-ce que le write-ahead log (WAL) ?

Un journal où chaque modification est enregistrée avant que les fichiers de données soient modifiés. Après une panne, PostgreSQL rejoue le WAL pour retrouver un état cohérent. Le WAL alimente aussi la réplication et la restauration à un instant donné.

#### Qu'est-ce qu'un checkpoint ?

Le moment où toutes les pages modifiées en mémoire sont écrites dans les fichiers de données, ce qui rend le WAL antérieur inutile pour la reprise après panne. Sa fréquence dépend de `checkpoint_timeout` et `max_wal_size`.

#### Quelle est la différence entre une base de données, un schéma et une table ?

Un cluster (instance) contient des bases de données. Une base contient des schémas (des espaces de noms comme `public`). Un schéma contient des tables, des vues, des fonctions et d'autres objets. Une connexion se fait à une base, et peut interroger plusieurs de ses schémas.

#### Comment créer une nouvelle base de données dans PostgreSQL ?

```sql
CREATE DATABASE my_database OWNER app_owner ENCODING 'UTF8';
```

Depuis le terminal, `createdb my_database` fait la même chose.

#### Comment créer une table dans PostgreSQL ?

```sql
CREATE TABLE company (
    company_id   bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    country_code char(2)      NOT NULL,
    business_id  text         NOT NULL,
    name         text,
    created_on   date,
    employees    integer CHECK (employees >= 0),
    UNIQUE (country_code, business_id)
);
```

#### Qu'est-ce qu'une clé primaire dans Postgres ?

Une contrainte qui identifie chaque ligne de façon unique : ses colonnes sont `NOT NULL` et uniques, et PostgreSQL crée un index B-tree unique pour l'appliquer. Une table a au plus une clé primaire, qui peut porter sur plusieurs colonnes.

#### Qu'est-ce que psql ?

Le client interactif en ligne de commande de PostgreSQL. Méta-commandes utiles : `\l` liste les bases, `\c` se connecte, `\dt` liste les tables, `\d table` en décrit une, `\di` liste les index, `\x` active l'affichage étendu, `\timing` affiche la durée des requêtes.

#### Qu'est-ce que le search path ?

La liste ordonnée des schémas où PostgreSQL cherche les noms d'objets non qualifiés (`SHOW search_path`). Par défaut, `"$user", public`.

#### Quelle est la différence entre `DELETE`, `TRUNCATE` et `DROP` ?

`DELETE` supprime les lignes une par une, accepte une clause `WHERE`, déclenche les triggers et laisse des tuples morts pour le vacuum. `TRUNCATE` vide toute la table rapidement en remplaçant ses fichiers. `DROP` supprime la table elle-même. Dans PostgreSQL, les trois sont transactionnels.

#### Qu'est-ce qu'une séquence ?

Un objet de la base qui génère des nombres croissants, utilisé pour les clés de substitution. Les colonnes `GENERATED ... AS IDENTITY` (standard SQL) et les anciens types `serial` utilisent des séquences. Les séquences ne sont pas transactionnelles : les insertions annulées laissent des trous.

#### Quelle est la différence entre `serial` et les colonnes identity ?

Les deux génèrent automatiquement des entiers à partir d'une séquence. Les colonnes identity sont du SQL standard, lient plus proprement la séquence à la colonne et, avec `GENERATED ALWAYS`, empêchent les valeurs manuelles accidentelles. Elles sont à privilégier pour les nouvelles tables.

#### Qu'est-ce qu'une vue ?

Une requête enregistrée qu'on interroge comme une table. Elle ne contient pas de données et sa requête s'exécute à chaque accès. Les vues simples peuvent être modifiables.

#### Qu'est-ce qu'une vue matérialisée ?

Une vue dont le résultat est stocké sur disque et rafraîchi explicitement avec `REFRESH MATERIALIZED VIEW`. Avec un index unique, `REFRESH ... CONCURRENTLY` la rafraîchit sans bloquer les lecteurs.

#### Qu'est-ce que TOAST ?

The Oversized-Attribute Storage Technique : les valeurs volumineuses (au-delà d'environ 2 ko) sont compressées et/ou stockées hors de la ligne dans une table séparée, de façon transparente pour les requêtes.

#### Qu'est-ce qu'un tablespace ?

Un répertoire sur disque où PostgreSQL peut stocker des objets, ce qui permet de placer certaines tables ou certains index sur un autre stockage.

#### Qu'est-ce que le catalogue système ?

Les tables de `pg_catalog` (comme `pg_class`, `pg_attribute`, `pg_index`) qui décrivent tous les objets, ainsi que les vues standard d'`information_schema`.

### Types de données et DDL

#### Quels types numériques PostgreSQL propose-t-il, et quand utiliser chacun ?

`smallint`, `integer`, `bigint` pour les nombres entiers. `numeric(p, s)` pour les décimaux exacts comme les montants. `real` et `double precision` pour les valeurs à virgule flottante approchées. Évitez les float pour l'argent.

#### Quelle est la différence entre `char(n)`, `varchar(n)` et `text` ?

`char(n)` complète par des espaces jusqu'à une longueur fixe. `varchar(n)` limite la longueur. `text` n'a pas de limite. Leurs performances sont identiques dans PostgreSQL : `text` (avec une contrainte `CHECK` si une limite est nécessaire) est le choix courant.

#### Quels sont les types de date et d'heure ?

`date`, `time`, `timestamp` (sans fuseau horaire), `timestamptz` (avec fuseau horaire) et `interval`. `timestamptz` stocke un instant absolu en UTC et le convertit à l'affichage selon le `TimeZone` de la session.

#### Faut-il utiliser `timestamp` ou `timestamptz` ?

`timestamptz` pour les événements survenus à un instant donné : il évite les ambiguïtés entre fuseaux horaires et changements d'heure. `timestamp` seulement pour des valeurs d'« heure locale » non liées à un fuseau.

#### Qu'est-ce que le type `boolean` ?

`true`, `false` ou `NULL`, avec en entrée `'t'`, `'yes'`, `'1'`, `'on'` et leurs contraires.

#### Qu'est-ce que le type `uuid`, et comment générer des UUID ?

Un type d'identifiant sur 128 bits. `gen_random_uuid()` est intégré et génère des UUID de version 4. PostgreSQL 18 ajoute `uuidv7()` pour des UUID ordonnés dans le temps, qui s'indexent mieux.

#### Que sont les tableaux dans PostgreSQL ?

Tout type peut être un tableau : `text[]`, `integer[]`. On les interroge avec `ANY`, `@>` (contient), `unnest()` pour les transformer en lignes, et on les indexe avec GIN.

#### Que sont les types intervalle (range) ?

Des types qui représentent un intervalle de valeurs, comme `daterange`, `tstzrange`, `int4range`, avec des opérateurs de chevauchement (`&&`) et d'inclusion (`@>`). Utiles pour les périodes de validité et les réservations.

#### Qu'est-ce qu'un type enum ?

Un type avec une liste fixe et ordonnée de valeurs : `CREATE TYPE status AS ENUM ('active', 'closed')`. Ajouter des valeurs est facile, en retirer ne l'est pas : les tables de référence sont souvent plus souples.

#### Quels sont les principaux types de contraintes ?

`NOT NULL`, `UNIQUE`, `PRIMARY KEY`, `FOREIGN KEY`, `CHECK` et `EXCLUDE` (par exemple, pas deux réservations qui se chevauchent pour la même salle).

#### Qu'est-ce qu'une clé étrangère, et que font les options `ON DELETE` ?

Une contrainte qui exige que les valeurs d'une colonne existent dans la clé d'une table référencée. `ON DELETE CASCADE` supprime les lignes enfants avec le parent, `SET NULL` vide la référence, `RESTRICT` ou `NO ACTION` empêchent la suppression.

#### Les colonnes de clé étrangère sont-elles indexées automatiquement ?

Non. PostgreSQL indexe la clé référencée (celle du parent) mais pas la colonne qui référence. Indexez les colonnes de clé étrangère utilisées dans les jointures ou vérifiées lors des suppressions sur le parent.

#### Qu'est-ce qu'une colonne générée ?

Une colonne calculée à partir d'autres colonnes : `total numeric GENERATED ALWAYS AS (price * qty) STORED`. PostgreSQL la calcule à l'écriture.

#### Qu'est-ce qu'un domaine ?

Un type de données assorti de contraintes, réutilisable dans plusieurs tables : `CREATE DOMAIN postcode_fr AS text CHECK (VALUE ~ '^\d{5}$')`.

#### Comment ajouter une colonne à une grosse table sans risque ?

`ALTER TABLE t ADD COLUMN c type` est instantané, même avec une valeur par défaut constante (depuis PostgreSQL 11). Les valeurs par défaut volatiles, les changements de type qui réécrivent la table et l'ajout de `NOT NULL` avec une passe de validation demandent plus de précautions.

#### Comment ajouter une contrainte sans bloquer la table longtemps ?

L'ajouter en `NOT VALID` (appliquée aux nouvelles lignes seulement), puis lancer `ALTER TABLE ... VALIDATE CONSTRAINT`, qui prend un verrou plus faible pendant la vérification des lignes existantes.

#### Qu'est-ce qu'une table temporaire ?

Une table visible seulement par la session courante et supprimée à sa fin (ou à la validation avec `ON COMMIT DROP`). Utile pour des résultats intermédiaires.

#### Qu'est-ce qu'une table unlogged ?

Une table dont les modifications ne sont pas écrites dans le WAL. Les écritures sont bien plus rapides, mais la table est vidée après une panne et n'est pas répliquée. Utile pour des données de staging qu'on peut recharger.

#### Que signifie `NULL`, et comment se comporte-t-il dans les comparaisons ?

Une valeur inconnue ou absente. Toute comparaison avec `NULL` renvoie `NULL` (et non vrai) : il faut utiliser `IS NULL` / `IS NOT NULL`, et `IS DISTINCT FROM` pour des comparaisons sûres vis-à-vis des nulls.

#### Que fait `COALESCE` ?

Elle renvoie le premier argument non nul : `COALESCE(nickname, first_name, 'unknown')`.

#### Qu'est-ce que `NULLIF` ?

`NULLIF(a, b)` renvoie `NULL` si `a = b`, sinon `a`. Pratique pour éviter la division par zéro : `x / NULLIF(y, 0)`.

### Requêtes : jointures, sous-requêtes et CTE

#### Quels sont les différents types de jointures ?

`INNER JOIN` (lignes correspondantes seulement), `LEFT JOIN` (toutes les lignes de gauche et les correspondances), `RIGHT JOIN`, `FULL OUTER JOIN` (toutes les lignes des deux côtés) et `CROSS JOIN` (toutes les combinaisons). Il existe aussi les auto-jointures et les jointures `LATERAL`.

#### Quelle est la différence entre `WHERE` et `ON` dans une jointure externe gauche ?

Une condition dans `ON` décide quelles lignes de droite correspondent, et les lignes de gauche sont conservées quoi qu'il arrive. La même condition dans `WHERE` filtre le résultat de la jointure, ce qui peut supprimer des lignes de gauche et transformer en pratique la jointure gauche en jointure interne.

#### Qu'est-ce qu'une semi-jointure et une anti-jointure ?

Une semi-jointure renvoie les lignes de A qui ont une correspondance dans B (`WHERE EXISTS (...)`) sans dupliquer A. Une anti-jointure renvoie les lignes de A sans correspondance dans B (`WHERE NOT EXISTS (...)` ou une jointure gauche avec `IS NULL`).

#### Pourquoi préférer `NOT EXISTS` à `NOT IN` avec une sous-requête ?

Si la sous-requête renvoie un seul `NULL`, `NOT IN` ne renvoie aucune ligne, car la comparaison avec `NULL` est inconnue. `NOT EXISTS` se comporte comme attendu et se planifie bien en anti-jointure.

#### Qu'est-ce qu'une CTE ?

Une Common Table Expression, introduite par `WITH`, donne un nom à une sous-requête pour la lisibilité et la réutilisation au sein d'une requête. Depuis PostgreSQL 12, les CTE non récursives sont intégrées à la requête quand c'est possible. `MATERIALIZED` et `NOT MATERIALIZED` forcent le choix.

#### Qu'est-ce qu'une CTE récursive ?

Une CTE qui se référence elle-même pour parcourir des hiérarchies ou générer des séries :

```sql
WITH RECURSIVE tree AS (
    SELECT id, parent_id, name, 1 AS depth FROM category WHERE parent_id IS NULL
    UNION ALL
    SELECT c.id, c.parent_id, c.name, t.depth + 1
    FROM category c JOIN tree t ON c.parent_id = t.id
)
SELECT * FROM tree;
```

#### Qu'est-ce qu'une sous-requête corrélée ?

Une sous-requête qui référence des colonnes de la requête externe : elle est donc logiquement évaluée pour chaque ligne externe. Le planificateur peut souvent la transformer en jointure.

#### Qu'est-ce qu'une jointure `LATERAL` ?

Une jointure où la sous-requête de droite peut référencer des colonnes des tables situées à sa gauche. Utilisée pour le « top N par groupe » :

```sql
SELECT c.name, o.*
FROM customer c
CROSS JOIN LATERAL (
    SELECT * FROM orders o WHERE o.customer_id = c.id ORDER BY created_at DESC LIMIT 3
) o;
```

#### Quelle est la différence entre `UNION` et `UNION ALL` ?

`UNION` supprime les doublons, ce qui demande un tri ou un hachage. `UNION ALL` garde toutes les lignes et est plus rapide. Utilisez `UNION ALL` sauf si vous avez besoin du dédoublonnage.

#### Que font `INTERSECT` et `EXCEPT` ?

`INTERSECT` renvoie les lignes présentes dans les deux requêtes, `EXCEPT` celles de la première absentes de la seconde, les deux sans doublons sauf avec `ALL`.

#### Quel est l'ordre logique d'exécution d'un SELECT ?

`FROM` et les jointures, `WHERE`, `GROUP BY`, `HAVING`, les fonctions de fenêtrage, `SELECT`, `DISTINCT`, `ORDER BY`, `LIMIT`/`OFFSET`. C'est pourquoi les alias définis dans le `SELECT` ne sont pas utilisables dans le `WHERE`.

#### Quelle est la différence entre `WHERE` et `HAVING` ?

`WHERE` filtre les lignes avant le regroupement. `HAVING` filtre les groupes après l'agrégation : il peut donc utiliser des résultats d'agrégats comme `HAVING count(*) > 10`.

#### Que fait `DISTINCT ON` ?

Une extension PostgreSQL qui garde la première ligne de chaque groupe, selon l'`ORDER BY` :

```sql
SELECT DISTINCT ON (customer_id) customer_id, order_id, created_at
FROM orders
ORDER BY customer_id, created_at DESC;   -- dernière commande de chaque client
```

#### Qu'est-ce qu'un upsert dans PostgreSQL ?

`INSERT ... ON CONFLICT` insère une ligne ou, si elle viole une contrainte d'unicité, la met à jour (ou ne fait rien) :

```sql
INSERT INTO company (country_code, business_id, name)
VALUES ('FR', '732829320', 'ACME')
ON CONFLICT (country_code, business_id) DO UPDATE SET name = EXCLUDED.name;
```

#### Qu'est-ce que l'instruction `MERGE` ?

Une instruction SQL standard (PostgreSQL 15+) qui insère, met à jour ou supprime des lignes d'une cible selon une jointure avec une source, en une seule requête. PostgreSQL 17 ajoute `RETURNING` et `WHEN NOT MATCHED BY SOURCE`.

#### Que fait `RETURNING` ?

Il renvoie des colonnes des lignes touchées par `INSERT`, `UPDATE` ou `DELETE`, ce qui évite une seconde requête : `INSERT ... RETURNING id`.

#### Comment paginer efficacement ?

`OFFSET` ralentit à mesure que le décalage augmente, car les lignes sautées sont quand même lues. La pagination par clé (keyset) est plus rapide : `WHERE (created_at, id) < ($1, $2) ORDER BY created_at DESC, id DESC LIMIT 50`, avec un index sur ces colonnes.

#### Comment trouver des lignes en double ?

```sql
SELECT country_code, business_id, count(*)
FROM company
GROUP BY country_code, business_id
HAVING count(*) > 1;
```

#### Comment supprimer les doublons en gardant une ligne par clé ?

```sql
DELETE FROM company c
USING (
    SELECT ctid, row_number() OVER (PARTITION BY country_code, business_id ORDER BY company_id) AS rn
    FROM company
) d
WHERE c.ctid = d.ctid AND d.rn > 1;
```

#### Qu'est-ce que `generate_series` ?

Une fonction qui renvoie un ensemble de lignes avec une série de nombres ou d'horodatages, utilisée pour construire des calendriers et combler des trous : `SELECT generate_series('2026-01-01'::date, '2026-12-31', interval '1 day')`.

### Agrégation et fonctions de fenêtrage

#### Quelles sont les fonctions d'agrégation les plus utilisées ?

`count`, `sum`, `avg`, `min`, `max`, `string_agg`, `array_agg`, `bool_and`, `bool_or`, `json_agg`, et des fonctions statistiques comme `stddev` et `percentile_cont`.

#### Quelle est la différence entre `count(*)`, `count(col)` et `count(DISTINCT col)` ?

`count(*)` compte les lignes. `count(col)` compte les valeurs non nulles de `col`. `count(DISTINCT col)` compte les valeurs distinctes non nulles.

#### Que fait la clause `FILTER` ?

Elle restreint les lignes vues par un agrégat, une alternative plus propre à un `CASE` dans les agrégats :

```sql
SELECT country_code,
       count(*) AS total,
       count(*) FILTER (WHERE status = 'ACTIVE') AS active
FROM company GROUP BY country_code;
```

#### Que sont `GROUPING SETS`, `ROLLUP` et `CUBE` ?

Des moyens de calculer plusieurs regroupements en une requête. `ROLLUP (country, city)` produit les totaux par ville, par pays et le total général. `CUBE` produit toutes les combinaisons. `GROUPING SETS` liste exactement les regroupements voulus.

#### Qu'est-ce qu'une fonction de fenêtrage ?

Une fonction calculée sur un ensemble de lignes liées à la ligne courante (sa fenêtre), sans regrouper les lignes comme `GROUP BY` :

```sql
SELECT country_code, name, revenue,
       rank() OVER (PARTITION BY country_code ORDER BY revenue DESC) AS rank_in_country
FROM company;
```

#### Quelle est la différence entre `row_number`, `rank` et `dense_rank` ?

En cas d'égalité : `row_number` donne des numéros uniques (1, 2, 3), `rank` donne le même rang puis saute (1, 1, 3), `dense_rank` donne le même rang sans trou (1, 1, 2).

#### Comment obtenir les N premières lignes de chaque groupe ?

En numérotant les lignes par groupe et en filtrant dans une requête externe (les fonctions de fenêtrage ne sont pas autorisées dans le `WHERE`) :

```sql
SELECT * FROM (
    SELECT *, row_number() OVER (PARTITION BY country_code ORDER BY employees DESC) AS rn
    FROM company
) t WHERE rn <= 3;
```

#### Que font `lag` et `lead` ?

Elles renvoient une valeur d'une ligne précédente ou suivante dans la fenêtre, par exemple pour calculer l'évolution par rapport au mois précédent : `revenue - lag(revenue) OVER (ORDER BY month)`.

#### Comment calculer un total cumulé ?

```sql
SELECT day, amount,
       sum(amount) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM sales;
```

#### Qu'est-ce que le cadre d'une fenêtre, et quelle est la différence entre `ROWS` et `RANGE` ?

Le sous-ensemble de la partition utilisé pour le calcul de chaque ligne. `ROWS` compte des lignes physiques (par exemple les trois lignes précédentes). `RANGE` utilise des écarts de valeur sur la colonne de l'`ORDER BY` : les lignes de même valeur sont incluses ensemble. Le cadre par défaut avec `ORDER BY` est `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`.

#### Comment calculer une moyenne mobile sur 7 jours ?

```sql
SELECT day,
       avg(amount) OVER (ORDER BY day RANGE BETWEEN interval '6 days' PRECEDING AND CURRENT ROW) AS avg_7d
FROM daily_sales;
```

#### Que font `first_value`, `last_value` et `nth_value` ?

Elles renvoient la première, la dernière ou la n-ième valeur du cadre. `last_value` surprend souvent car le cadre par défaut s'arrête à la ligne courante : précisez `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.

#### Que font `ntile` et `percent_rank` ?

`ntile(4)` répartit les lignes ordonnées en 4 groupes (quartiles). `percent_rank()` donne à chaque ligne son rang relatif entre 0 et 1.

#### Comment calculer un pourcentage du total avec une fonction de fenêtrage ?

```sql
SELECT country_code, count(*) AS n,
       round(100.0 * count(*) / sum(count(*)) OVER (), 1) AS pct
FROM company GROUP BY country_code;
```

#### Comment calculer une médiane dans PostgreSQL ?

Avec l'agrégat d'ensemble ordonné `percentile_cont(0.5) WITHIN GROUP (ORDER BY value)`. `percentile_disc` renvoie une valeur réelle de l'ensemble.

#### Qu'est-ce que le problème des « îlots et trous », et comment le résoudre ?

Trouver des séquences consécutives (îlots) dans une suite. Une méthode classique soustrait un `row_number()` à la valeur ordonnée : les lignes d'un même îlot partagent la différence, sur laquelle on regroupe ensuite.

```sql
SELECT user_id, min(day) AS start_day, max(day) AS end_day
FROM (
    SELECT user_id, day, day - (row_number() OVER (PARTITION BY user_id ORDER BY day))::int AS grp
    FROM logins
) t
GROUP BY user_id, grp;
```

#### Comment transformer des lignes en colonnes (pivot) ?

Avec une agrégation conditionnelle :

```sql
SELECT country_code,
       sum(amount) FILTER (WHERE year = 2025) AS y2025,
       sum(amount) FILTER (WHERE year = 2026) AS y2026
FROM revenue GROUP BY country_code;
```

La fonction `crosstab` de l'extension `tablefunc` est une alternative.

#### Que fait `string_agg` ?

Elle concatène des valeurs avec un séparateur, éventuellement dans un ordre donné : `string_agg(name, ', ' ORDER BY name)`.

#### Qu'est-ce que la clause `WINDOW` ?

Un moyen de nommer une définition de fenêtre et de la réutiliser dans plusieurs fonctions : `... OVER w ... WINDOW w AS (PARTITION BY country ORDER BY day)`.

#### Comment calculer une croissance d'une année sur l'autre ?

```sql
SELECT year, revenue,
       round(100.0 * (revenue - lag(revenue) OVER (ORDER BY year)) / lag(revenue) OVER (ORDER BY year), 1) AS yoy_pct
FROM yearly_revenue;
```

### Index

#### Quels types d'index PostgreSQL propose-t-il, et quand utiliser chacun ?

- **B-tree** (par défaut) : recherches d'égalité et d'intervalle (`=`, `<`, `>`, `BETWEEN`, `ORDER BY`, `LIKE 'abc%'` avec préfixe) sur des données ordonnables.
- **Hash :** égalité seulement. Rarement meilleur qu'un B-tree, mais compact pour les valeurs longues.
- **GIN** (index inversé généralisé) : valeurs composées de plusieurs éléments, comme les tableaux, le JSONB et les vecteurs de recherche plein texte, pour les requêtes de type « contient ».
- **GiST** (arbre de recherche généralisé) : données géométriques, intervalles, recherche plein texte et recherche du plus proche voisin (avec PostGIS, par exemple).
- **SP-GiST :** données partitionnées dans l'espace, comme des quadtrees, des adresses IP ou des numéros de téléphone.
- **BRIN** (index par plages de blocs) : très grosses tables dont les valeurs suivent l'ordre physique, comme une colonne d'horodatage dans une table en ajout seul. Minuscule et peu coûteux à maintenir.

#### Comment fonctionne un index B-tree ?

C'est un arbre équilibré de clés triées avec des pointeurs vers les lignes de la table. Les recherches lisent quelques pages (temps logarithmique), et l'ordre trié rend efficaces les parcours d'intervalle et l'`ORDER BY`.

#### Qu'est-ce qu'un index composite (multicolonne), et l'ordre des colonnes compte-t-il ?

Un index sur plusieurs colonnes. L'ordre compte : un index sur `(country_code, created_on)` sert pour les filtres sur `country_code` seul ou sur les deux, mais pas efficacement sur `created_on` seul. Placez d'abord les colonnes d'égalité, puis celle d'intervalle ou de tri.

#### Qu'est-ce qu'un index partiel ?

Un index sur un sous-ensemble de lignes, défini par une clause `WHERE`. Il est plus petit et plus rapide quand les requêtes ciblent ce sous-ensemble :

```sql
CREATE INDEX ON company (country_code) WHERE status = 'ACTIVE';
```

#### Qu'est-ce qu'un index d'expression ?

Un index sur le résultat d'une expression, utilisé quand les requêtes filtrent sur cette même expression :

```sql
CREATE INDEX ON customer (lower(email));
SELECT * FROM customer WHERE lower(email) = 'a@b.com';
```

#### Qu'est-ce qu'un index couvrant, et que fait `INCLUDE` ?

Un index qui contient toutes les colonnes dont une requête a besoin, pour qu'elle puisse répondre par un index-only scan sans lire la table. `INCLUDE (col)` ajoute à l'index des colonnes non clés dans ce but.

#### Qu'est-ce qu'un index-only scan, et de quoi a-t-il besoin ?

Un parcours qui répond à une requête avec le seul index. Il faut un index couvrant et des pages marquées entièrement visibles dans la visibility map, maintenue par le vacuum.

#### Quels sont les coûts des index ?

Ils occupent de l'espace disque et ralentissent `INSERT`, `UPDATE` et `DELETE`, car chaque index doit être maintenu. Les index inutilisés ne sont qu'un coût : repérez-les avec `pg_stat_user_indexes` (`idx_scan = 0`).

#### Pourquoi PostgreSQL pourrait-il ne pas utiliser un index ?

La requête renvoie une grande partie de la table (un parcours séquentiel coûte moins cher), les statistiques sont périmées, une fonction ou une conversion de type est appliquée à la colonne indexée, le filtre commence par un joker (`LIKE '%abc'`), l'ordre des colonnes ne correspond pas à un index composite, ou la table est petite.

#### Comment créer un index sans bloquer les écritures ?

`CREATE INDEX CONCURRENTLY`, qui construit l'index sans verrou bloquant les insertions et mises à jour. C'est plus long et impossible dans un bloc de transaction. En cas d'échec, il laisse un index invalide à supprimer.

#### Qu'est-ce qu'un index unique, et quel est son lien avec une contrainte d'unicité ?

Un index qui refuse les clés en double. Une contrainte `UNIQUE` est implémentée par un index unique. Par défaut, plusieurs `NULL` sont acceptés, sauf si l'index est déclaré `NULLS NOT DISTINCT` (PostgreSQL 15+).

#### Comment indexer une colonne JSONB ?

Un index GIN sur toute la colonne pour les requêtes d'inclusion et d'existence de clé (`@>`, `?`), avec `jsonb_path_ops` pour un index plus petit qui ne gère que `@>`, ou un index d'expression B-tree sur une clé extraite :

```sql
CREATE INDEX ON events USING gin (payload jsonb_path_ops);
CREATE INDEX ON events ((payload->>'user_id'));
```

#### Comment accélérer les recherches `LIKE '%text%'` ?

Avec un index de trigrammes de l'extension `pg_trgm` : `CREATE INDEX ON company USING gin (name gin_trgm_ops)`. Il accélère aussi les recherches par similarité.

#### Qu'est-ce que le gonflement (bloat) des index, et comment le corriger ?

Les index accumulent de l'espace vide après beaucoup de mises à jour et de suppressions. `REINDEX CONCURRENTLY` les reconstruit en ligne. La déduplication des B-tree (PostgreSQL 13+) réduit le gonflement dû aux doublons.

#### Quand un index BRIN est-il le bon choix ?

Pour les très grosses tables où une colonne suit l'ordre physique, comme un horodatage dans un journal en ajout seul. Un index BRIN stocke le minimum et le maximum par plage de blocs : il est minuscule et permet aux requêtes de sauter la plupart des blocs.

#### Quelle est la différence entre un index cluster d'autres bases et `CLUSTER` dans PostgreSQL ?

PostgreSQL n'a pas de tables organisées en permanence selon un index. `CLUSTER` réordonne physiquement une table une fois selon un index, mais les nouvelles lignes ne restent pas dans l'ordre : il faut le relancer.

#### Comment repérer les index manquants ?

En cherchant de gros parcours séquentiels dans `pg_stat_user_tables` (`seq_scan`, `seq_tup_read`), les requêtes lentes dans `pg_stat_statements`, et les parcours séquentiels avec des filtres sélectifs dans les plans `EXPLAIN`.

#### Un index sur `(a, b)` rend-il redondant un index sur `(a)` ?

Le plus souvent oui : l'index composite sert les requêtes sur `a` seul. Un index séparé sur `a` peut être un peu plus petit et rapide, mais en vaut rarement le coût de maintenance.

#### Que sont le `fastupdate` et les listes en attente des index GIN ?

Les index GIN accumulent les nouvelles entrées dans une liste en attente pour accélérer les insertions, intégrée plus tard à l'index principal par le vacuum ou quand la liste est pleine. De grosses listes en attente peuvent ralentir les recherches.

#### Comment voir la taille d'une table et de ses index ?

```sql
SELECT pg_size_pretty(pg_total_relation_size('company')) AS total,
       pg_size_pretty(pg_relation_size('company'))       AS table_only,
       pg_size_pretty(pg_indexes_size('company'))        AS indexes;
```

### Transactions, MVCC et concurrence

#### Qu'est-ce qu'une transaction dans PostgreSQL ?

Un groupe d'instructions entre `BEGIN` et `COMMIT` (ou `ROLLBACK`) exécuté de façon atomique. Chaque instruction hors transaction explicite s'exécute dans sa propre transaction (autocommit).

#### Qu'est-ce que le MVCC ?

Le contrôle de concurrence multiversion : un `UPDATE` écrit une nouvelle version de la ligne au lieu de l'écraser, et chaque transaction voit un instantané des données validées. Les lecteurs ne bloquent pas les écrivains, et les écrivains ne bloquent pas les lecteurs.

#### Que sont les tuples morts ?

Les anciennes versions de lignes laissées par les mises à jour et suppressions, qu'aucune transaction ne peut plus voir. Elles occupent de la place jusqu'à ce que `VACUUM` la récupère.

#### Quels sont les niveaux d'isolation des transactions dans PostgreSQL ?

- **Read Committed** (par défaut) : chaque instruction voit les données validées avant son début.
- **Repeatable Read :** toute la transaction voit un seul instantané, pris à sa première instruction. Les mises à jour concurrentes en conflit provoquent des erreurs de sérialisation.
- **Serializable :** comme Repeatable Read, avec en plus la détection des anomalies (isolation par instantané sérialisable), pour que le résultat corresponde à un ordre séquentiel. Les applications doivent relancer en cas d'échec de sérialisation.

Read Uncommitted est accepté mais se comporte comme Read Committed.

#### Quelles anomalies les niveaux d'isolation empêchent-ils ?

Les lectures sales (impossibles dans PostgreSQL), les lectures non répétables (empêchées à partir de Repeatable Read), les lectures fantômes (empêchées aussi par le Repeatable Read de PostgreSQL) et les anomalies de sérialisation comme le write skew (empêchées seulement par Serializable).

#### Qu'est-ce qu'un interblocage (deadlock), et comment PostgreSQL le gère-t-il ?

Deux transactions attendent chacune un verrou détenu par l'autre. PostgreSQL le détecte après `deadlock_timeout` et annule l'une des transactions avec une erreur. On l'évite en verrouillant les lignes dans un ordre cohérent et en gardant des transactions courtes.

#### Qu'est-ce que `SELECT ... FOR UPDATE` ?

Il verrouille les lignes sélectionnées contre les mises à jour ou suppressions concurrentes jusqu'à la fin de la transaction, pour pouvoir les lire puis les modifier sans risque. `FOR SHARE` permet aux autres lecteurs de les verrouiller aussi.

#### Que fait `SKIP LOCKED`, et à quoi sert-il ?

Il ignore les lignes déjà verrouillées par d'autres au lieu d'attendre, ce qui permet de construire facilement des files de tâches :

```sql
SELECT id FROM jobs WHERE status = 'pending'
ORDER BY id LIMIT 10 FOR UPDATE SKIP LOCKED;
```

#### Que sont les verrous consultatifs (advisory locks) ?

Des verrous définis par l'application sur des nombres arbitraires (`pg_advisory_lock(42)`), gérés par PostgreSQL mais non liés à des lignes. Ils servent à garantir qu'un seul worker exécute une tâche à la fois.

#### Qu'est-ce qu'un savepoint ?

Un point au sein d'une transaction vers lequel on peut revenir sans annuler toute la transaction : `SAVEPOINT s1; ... ROLLBACK TO SAVEPOINT s1;`.

#### Pourquoi les transactions longues sont-elles néfastes ?

Elles conservent un instantané : le vacuum ne peut pas supprimer les tuples morts plus récents que lui, ce qui crée du gonflement. Elles peuvent aussi détenir des verrous qui bloquent le DDL et d'autres écritures. Les sessions « idle in transaction » sont une cause fréquente, limitée par `idle_in_transaction_session_timeout`.

#### Qu'est-ce que le problème de la mise à jour perdue, et comment l'éviter ?

Deux transactions lisent une valeur, la modifient, et la seconde écriture écrase la première. On l'évite avec une mise à jour atomique (`SET qty = qty - 1`), `SELECT ... FOR UPDATE`, un verrouillage optimiste avec une colonne de version, ou Repeatable Read avec relances.

#### Qu'est-ce que le verrouillage optimiste ?

Détecter les conflits au moment de l'écriture plutôt que verrouiller : chaque ligne a une version, et une mise à jour ne réussit que si la version n'a pas changé (`UPDATE ... SET ..., version = version + 1 WHERE id = $1 AND version = $2`).

#### Quels verrous prend le DDL, et pourquoi un `ALTER TABLE` peut-il tout bloquer ?

Beaucoup de formes d'`ALTER TABLE` prennent un verrou `ACCESS EXCLUSIVE`, incompatible avec tous les autres, y compris les lectures. S'il attend derrière une longue requête, toutes les nouvelles requêtes s'accumulent derrière lui. Utilisez `lock_timeout` et relancez.

#### Qu'est-ce que le rebouclage (wraparound) des identifiants de transaction ?

Les identifiants de transaction sont sur 32 bits et finissent par reboucler. Le vacuum doit « geler » les anciennes lignes avant que cela n'arrive, sinon PostgreSQL cesse d'accepter les écritures pour protéger les données. L'autovacuum lance automatiquement des vacuums anti-rebouclage, et surveiller `age(datfrozenxid)` permet de détecter les problèmes tôt.

#### Que fait `VACUUM`, et en quoi diffère-t-il de `VACUUM FULL` ?

`VACUUM` rend réutilisable l'espace des tuples morts, met à jour la visibility map et gèle les anciennes lignes, sans bloquer lectures ni écritures. `VACUUM FULL` réécrit la table pour rendre l'espace au système d'exploitation, mais prend un verrou exclusif. `pg_repack` fait la même chose en ligne.

#### Qu'est-ce que l'autovacuum ?

Un processus d'arrière-plan qui lance `VACUUM` et `ANALYZE` sur les tables quand assez de lignes ont changé, selon des seuils et facteurs d'échelle réglables par table.

#### Que fait `ANALYZE` ?

Il échantillonne les tables et met à jour les statistiques (`pg_statistic`) que le planificateur utilise pour estimer le nombre de lignes et choisir les plans.

#### Qu'est-ce qu'une mise à jour HOT (heap-only tuple) ?

Une optimisation où une mise à jour qui ne modifie pas de colonne indexée, et qui tient dans la même page, crée la nouvelle version sans mettre à jour les index. Un `fillfactor` plus bas laisse de la place pour les mises à jour HOT sur les tables très modifiées.

#### Quelle est la différence entre `COMMIT` et `synchronous_commit = off` ?

Par défaut, `COMMIT` attend que le WAL soit écrit sur disque, ce qui garantit la durabilité. Avec `synchronous_commit = off`, les commits reviennent plus vite et une panne peut perdre les dernières transactions, sans corrompre les données.

### Performances et planification des requêtes

#### Que montre `EXPLAIN`, et en quoi `EXPLAIN ANALYZE` est-il différent ?

`EXPLAIN` montre le plan choisi par le planificateur, avec les coûts et nombres de lignes estimés. `EXPLAIN ANALYZE` exécute la requête et ajoute les durées et nombres de lignes réels. Ajoutez `BUFFERS` pour voir les pages lues en cache ou sur disque.

```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM company WHERE country_code = 'FR';
```

#### Que faut-il regarder dans un plan d'exécution ?

De gros écarts entre lignes estimées et réelles (statistiques faussées), des parcours séquentiels sur de grosses tables avec des filtres sélectifs, des boucles imbriquées sur beaucoup de lignes, des tris ou hachages qui débordent sur disque, et les nœuds où se concentre le temps.

#### Quels sont les principaux types de parcours ?

Le parcours séquentiel (lit toute la table), l'index scan (suit l'index puis lit les lignes de la table), l'index-only scan (avec l'index seul) et le bitmap index/heap scan (rassemble les emplacements correspondants d'un ou plusieurs index, puis lit les pages dans l'ordre physique).

#### Quels sont les trois algorithmes de jointure ?

- **Nested loop :** pour chaque ligne externe, cherche les lignes internes. Bon quand un côté est petit et l'autre indexé.
- **Hash join :** construit une table de hachage sur la plus petite entrée. Bon pour de grosses jointures d'égalité non triées.
- **Merge join :** les deux entrées triées sur la clé de jointure. Bon pour de grosses entrées déjà triées ou indexées.

#### Qu'est-ce que `work_mem`, et pourquoi est-ce important ?

La mémoire que chaque opération de tri ou de hachage peut utiliser avant de déborder sur disque. Trop basse, elle provoque des tris lents sur disque. Trop haute, elle fait courir un risque de manque de mémoire, car une seule requête peut l'utiliser plusieurs fois.

#### Quels sont les principaux paramètres mémoire à régler ?

`shared_buffers` (le cache de PostgreSQL, souvent environ 25 % de la RAM), `effective_cache_size` (indication au planificateur du cache total, souvent 50 à 75 % de la RAM), `work_mem` (par opération) et `maintenance_work_mem` (vacuum, création d'index).

#### Qu'est-ce que `pg_stat_statements` ?

Une extension qui enregistre les statistiques d'exécution de chaque requête normalisée : appels, temps total et moyen, lignes, accès au cache. C'est le premier endroit où chercher les requêtes lentes ou fréquentes.

#### Comment trouver les requêtes lentes en cours d'exécution ?

```sql
SELECT pid, now() - query_start AS duration, state, wait_event_type, query
FROM pg_stat_activity
WHERE state <> 'idle'
ORDER BY duration DESC;
```

#### Comment arrêter une requête qui s'emballe ?

`SELECT pg_cancel_backend(pid)` annule la requête en cours. `pg_terminate_backend(pid)` ferme toute la connexion. `statement_timeout` évite dès le départ les requêtes qui s'emballent.

#### Pourquoi une fonction appliquée à une colonne indexée peut-elle empêcher l'utilisation de l'index ?

L'index stocke les valeurs brutes de la colonne : `WHERE date(created_at) = '2026-10-15'` ne peut donc pas utiliser un index sur `created_at`. Réécrivez-le en intervalle (`created_at >= '2026-10-15' AND created_at < '2026-10-16'`) ou créez un index d'expression.

#### Que sont les statistiques étendues ?

`CREATE STATISTICS` permet au planificateur de connaître les corrélations entre colonnes (dépendances, nombres de valeurs distinctes, combinaisons de valeurs les plus fréquentes), ce qui améliore les estimations des filtres sur plusieurs colonnes corrélées, comme la ville et le code postal.

#### Que contrôle `default_statistics_target` ?

Le nombre de valeurs d'échantillon et de tranches d'histogramme qu'`ANALYZE` conserve par colonne. L'augmenter pour les colonnes à distribution déséquilibrée améliore les estimations, au prix d'un temps de planification plus long.

#### Comment charger rapidement de gros volumes de données ?

Utiliser `COPY` plutôt que des insertions ligne à ligne, charger dans une seule transaction, créer index et clés étrangères après le chargement, envisager des tables de staging unlogged, augmenter `maintenance_work_mem` pour la création d'index, et lancer `ANALYZE` ensuite.

#### Qu'est-ce que la commande `COPY` ?

Le moyen le plus rapide de charger ou d'exporter en masse des données entre des tables et des fichiers ou des flux : `COPY company FROM '/data/company.csv' WITH (FORMAT csv, HEADER)`. Depuis un client, utilisez le `\copy` de psql ou la prise en charge de COPY du pilote. PostgreSQL 17 peut ignorer les lignes mal formées avec `ON_ERROR ignore`.

#### Qu'est-ce que le pooling de connexions, et pourquoi utiliser PgBouncer ?

Réutiliser un petit nombre de connexions à la base pour de nombreux clients. PgBouncer se place entre les applications et PostgreSQL, en mode session, transaction ou instruction, et réduit le coût de chaque connexion.

#### Qu'est-ce que la requête parallèle ?

PostgreSQL peut répartir les parcours séquentiels, les jointures et les agrégations sur plusieurs processus workers, selon `max_parallel_workers_per_gather` et la taille de la table.

#### Qu'est-ce que la compilation JIT dans PostgreSQL ?

La compilation à la volée (avec LLVM) des expressions des longues requêtes analytiques. Elle accélère les calculs lourds mais ajoute un surcoût aux requêtes courtes. Elle est contrôlée par `jit` et des seuils de coût.

#### Comment `LIMIT` interagit-il avec `ORDER BY` et les index ?

Avec un index correspondant à l'`ORDER BY`, PostgreSQL ne lit que les premières lignes nécessaires. Sans index, il doit tout trier (par un heapsort top-N) avant d'appliquer la limite.

#### Qu'est-ce que le gonflement (bloat) des tables, et comment le détecter ?

De l'espace gaspillé par des tuples morts que le vacuum n'a pas récupérés ou que le système d'exploitation n'a pas repris. On le détecte avec `pgstattuple`, des requêtes d'estimation du gonflement, ou des tables qui grossissent plus vite que leur nombre de lignes.

#### Que vérifier en premier quand une requête devient soudain lente ?

Son plan (`EXPLAIN ANALYZE`) comparé à l'ancien, la fraîcheur des statistiques (dernier analyze), l'évolution des volumes, les verrous et attentes dans `pg_stat_activity`, le gonflement, et si des paramètres ou un nouvel index ont changé le plan.

### Modélisation des données, normalisation et OLAP

#### Citez les trois principales formes normales.

- **Première forme normale (1FN) :** chaque colonne contient des valeurs atomiques, sans groupes répétés ni listes dans une colonne, et chaque ligne est unique.
- **Deuxième forme normale (2FN) :** 1FN, et chaque colonne non clé dépend de toute la clé primaire, pas seulement d'une partie d'une clé composite.
- **Troisième forme normale (3FN) :** 2FN, et les colonnes non clés ne dépendent que de la clé, pas d'autres colonnes non clés (pas de dépendance transitive).

#### Qu'est-ce que la FNBC ?

La forme normale de Boyce-Codd, une 3FN plus stricte : tout déterminant (un ensemble de colonnes qui détermine une autre colonne) doit être une clé candidate.

#### Qu'est-ce que la dénormalisation, et quand est-elle justifiée ?

Ajouter délibérément de la redondance (colonnes dupliquées, tables pré-jointes ou pré-agrégées) pour accélérer les lectures, en analytique et reporting, où les requêtes dominent et où les données sont chargées par lots maîtrisés.

#### Quelle est la différence entre OLTP et OLAP ?

L'OLTP (traitement transactionnel en ligne) gère beaucoup de lectures et écritures courtes sur des données actuelles, avec des schémas normalisés et un stockage en lignes. L'OLAP (traitement analytique en ligne) exécute des requêtes complexes sur de gros volumes de données historiques, avec des schémas dénormalisés (en étoile) et un stockage en colonnes.

#### Quelles sont les principales opérations OLAP dans un système OLAP ?

Les opérations OLAP s'appliquent à un modèle multidimensionnel où les données sont représentées sous forme de cubes. Il existe cinq opérations analytiques de base :

- **Drill down (forage) :** descendre à un niveau plus détaillé d'une hiérarchie, par exemple année → trimestre → mois.
- **Roll up (agrégation) :** l'inverse du drill down, agréger à un niveau supérieur, par exemple ville → pays ou mois → trimestre.
- **Slice (tranche) :** fixer une dimension sur une seule valeur pour obtenir un sous-cube avec une dimension de moins, par exemple uniquement le T1.
- **Dice (découpe) :** filtrer sur deux dimensions ou plus pour obtenir un sous-cube plus petit, par exemple lieu = Bogotá et produit = café.
- **Pivot (rotation) :** faire pivoter le cube pour échanger les dimensions sur les axes et voir les données sous un autre angle.

#### Qu'est-ce qu'un schéma en étoile ?

Un modèle dimensionnel avec une table de faits centrale (mesures et clés étrangères) entourée de tables de dimensions (attributs descriptifs). Simple à interroger et rapide pour l'analytique.

#### Qu'est-ce qu'un schéma en flocon ?

Un schéma en étoile dont les dimensions sont normalisées en plusieurs tables liées (produit → catégorie → rayon). Il économise de l'espace mais demande plus de jointures.

#### Qu'est-ce que la granularité d'une table de faits ?

Ce que représente exactement une ligne (une ligne de commande, un solde quotidien par compte). La déclarer en premier est l'étape la plus importante de la conception dimensionnelle.

#### Quels sont les types de tables de faits ?

Les faits transactionnels (une ligne par événement), les instantanés périodiques (une ligne par entité et par période, comme les soldes de fin de mois) et les instantanés cumulatifs (une ligne par instance de processus, mise à jour à chaque étape).

#### Que sont les dimensions à évolution lente (SCD) ?

Des façons de gérer les changements d'attributs des dimensions. Le type 1 écrase, donc aucun historique n'est conservé. Le type 2 ajoute une ligne par version, avec des dates de validité et un indicateur de version courante. Le type 3 garde la valeur précédente dans une colonne supplémentaire. Les types 4 et 6 combinent ces approches.

#### Comment implémenter une SCD de type 2 dans PostgreSQL ?

Fermer la version courante et insérer la nouvelle dans une seule transaction :

```sql
BEGIN;
UPDATE dim_customer SET valid_to = now(), is_current = false
WHERE customer_id = $1 AND is_current AND row_hash <> $2;
INSERT INTO dim_customer (customer_id, name, city, row_hash, valid_from, valid_to, is_current)
SELECT $1, $3, $4, $2, now(), NULL, true
WHERE NOT EXISTS (SELECT 1 FROM dim_customer WHERE customer_id = $1 AND is_current);
COMMIT;
```

#### Qu'est-ce qu'une clé de substitution, et pourquoi l'utiliser dans un entrepôt ?

Une clé générée sans signification (identity ou hachage) à la place de la clé naturelle de la source. Elle isole l'entrepôt des changements de clé de la source, permet plusieurs versions d'un enregistrement (SCD2) et rend les jointures efficaces.

#### Qu'est-ce qu'une clé naturelle ?

Une clé qui a un sens pour le métier ou le système source, comme un SIRET ou une adresse e-mail. Elle doit être conservée comme attribut même quand on utilise une clé de substitution.

#### Qu'est-ce qu'une dimension fourre-tout (junk dimension) ?

Une dimension qui regroupe plusieurs indicateurs et drapeaux à faible cardinalité (type de paiement, is_promo) dans une table, au lieu d'encombrer la table de faits.

#### Qu'est-ce qu'une dimension dégénérée ?

Une clé de dimension stockée dans la table de faits sans table de dimension propre, comme un numéro de facture.

#### Qu'est-ce qu'une dimension conforme ?

Une dimension partagée, avec le même sens et les mêmes clés, entre plusieurs tables de faits ou data marts (date, client), pour pouvoir combiner les résultats.

#### Qu'est-ce qu'une dimension date, et pourquoi en construire une ?

Une table avec une ligne par jour et des attributs (jour de la semaine, mois, trimestre, jours fériés, périodes fiscales). Elle rend les filtres et regroupements calendaires simples et cohérents :

```sql
SELECT d::date AS day, extract(isodow FROM d) AS weekday, extract(quarter FROM d) AS quarter
FROM generate_series('2020-01-01'::date, '2030-12-31', interval '1 day') AS d;
```

#### Qu'est-ce que la modélisation Data Vault ?

Une méthode de modélisation pour intégrer de nombreuses sources avec un historique complet : hubs (clés métier), links (relations) et satellites (attributs descriptifs avec dates de chargement). Elle favorise l'auditabilité et le chargement en parallèle, et alimente en général des schémas en étoile pour le reporting.

#### Quand ne pas utiliser PostgreSQL pour l'analytique ?

Quand les données atteignent de nombreux téraoctets ou que les requêtes parcourent régulièrement d'énormes volumes : les entrepôts en colonnes ou les lakehouses (Redshift, BigQuery, Snowflake, Databricks) passent mieux à l'échelle. Des extensions comme Citus ou le stockage en colonnes, ou DuckDB pour l'analyse locale, peuvent d'abord repousser les limites de PostgreSQL.

#### Qu'est-ce que l'architecture médaillon, et quelle place y occupe une base relationnelle ?

Une organisation en couches d'un lakehouse : bronze (brut), silver (nettoyé et conformé) et gold (agrégats et modèles métier). Une base relationnelle comme PostgreSQL est souvent un système source, ou une couche de service pour les données gold utilisées par les applications.

### Administration, sécurité, sauvegarde et réplication

#### Que sont les rôles dans PostgreSQL ?

Les rôles sont à la fois des utilisateurs et des groupes : un rôle avec `LOGIN` est un utilisateur, et des rôles peuvent être accordés à d'autres rôles pour qu'ils héritent de leurs privilèges.

#### Comment accorder un accès en lecture seule à un schéma ?

```sql
CREATE ROLE reporting NOLOGIN;
GRANT USAGE ON SCHEMA analytics TO reporting;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO reporting;
ALTER DEFAULT PRIVILEGES IN SCHEMA analytics GRANT SELECT ON TABLES TO reporting;
GRANT reporting TO alice;
```

PostgreSQL 14+ dispose aussi du rôle prédéfini `pg_read_all_data`.

#### Qu'est-ce que la sécurité au niveau des lignes (RLS) ?

Des politiques qui restreignent les lignes que chaque rôle peut voir ou modifier :

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders USING (tenant_id = current_setting('app.tenant_id')::int);
```

#### Qu'est-ce que `pg_hba.conf` ?

Le fichier d'authentification par hôte : des règles qui indiquent quels utilisateurs peuvent se connecter à quelles bases, depuis quelles adresses et avec quelle méthode (`scram-sha-256`, `cert`, `peer`). `trust` ne doit jamais être utilisé hors tests locaux.

#### Comment stocker et vérifier les mots de passe ?

Avec `scram-sha-256` (la valeur par défaut depuis PostgreSQL 14) plutôt que md5, des connexions chiffrées en TLS, et les identifiants applicatifs conservés dans un gestionnaire de secrets.

#### Comment empêcher l'injection SQL ?

Utiliser des requêtes paramétrées (des marqueurs liés par le pilote) au lieu de concaténer des chaînes. Dans le SQL dynamique au sein de fonctions, utiliser `format()` avec `%I` pour les identifiants et `%L` pour les littéraux, ou `EXECUTE ... USING`.

#### Quelle est la différence entre sauvegardes logiques et physiques ?

Les sauvegardes logiques (`pg_dump`, `pg_dumpall`) exportent des fichiers SQL ou d'archive contenant les objets et les données. Elles sont portables entre versions et restaurables de façon sélective, mais lentes pour les grosses bases. Les sauvegardes physiques (`pg_basebackup`, pgBackRest) copient les fichiers de données et le WAL. Elles sont rapides pour les grosses bases et permettent la restauration à un instant donné.

#### Comment sauvegarder et restaurer une seule base avec pg_dump ?

```bash
pg_dump -Fc -d mydb -f mydb.dump          # format custom, compressé
pg_restore -d newdb -j 4 mydb.dump        # restauration en parallèle
```

#### Qu'est-ce que la restauration à un instant donné (PITR) ?

Restaurer une sauvegarde de base puis rejouer le WAL archivé jusqu'à un instant choisi, par exemple juste avant un `DELETE` accidentel.

#### Qu'est-ce que la réplication en streaming ?

Un serveur de secours reçoit et rejoue en continu le WAL du primaire, et en garde une copie identique octet pour octet. Il peut servir des requêtes en lecture seule (hot standby) et être promu si le primaire tombe.

#### Quelle est la différence entre réplication synchrone et asynchrone ?

En réplication asynchrone, les commits n'attendent pas les secours : une bascule peut perdre les dernières transactions. En réplication synchrone, les commits attendent la confirmation d'un ou plusieurs secours : aucune donnée n'est perdue, au prix d'une latence de commit plus élevée.

#### Qu'est-ce que la réplication logique ?

La réplication des changements de lignes par table, via des publications et des abonnements. Elle fonctionne entre versions majeures et permet de répliquer un sous-ensemble de tables, ce qui est utile pour les montées de version, la consolidation et la capture des changements.

#### Qu'est-ce que la capture des changements de données (CDC) avec PostgreSQL ?

Diffuser en flux les changements au niveau des lignes depuis le WAL grâce au décodage logique, souvent avec Debezium et Kafka, pour que les systèmes en aval (data lakes, index de recherche) reçoivent insertions, mises à jour et suppressions quasiment en temps réel.

#### Qu'est-ce qu'un slot de réplication, et quel est le risque ?

Un slot oblige le primaire à conserver le WAL jusqu'à ce qu'un consommateur l'ait reçu. Si le consommateur s'arrête, le WAL s'accumule et peut remplir le disque : il faut surveiller `pg_replication_slots`.

#### Comment passer à une nouvelle version majeure de PostgreSQL ?

Avec `pg_upgrade` (rapide, sur place, avec `--link` ou `--clone`), un dump puis une restauration (simple mais lent), ou la réplication logique vers un nouveau cluster pour une interruption quasi nulle.

#### Avec quoi construit-on en général la haute disponibilité de PostgreSQL ?

La réplication en streaming plus un gestionnaire de bascule comme Patroni (avec etcd ou Consul), ou un service géré (Amazon RDS ou Aurora, Cloud SQL, Azure Database for PostgreSQL) qui gère la bascule.

#### Que faut-il superviser sur un serveur PostgreSQL ?

Les connexions, le débit de transactions, le taux de succès du cache, les requêtes lentes (`pg_stat_statements`), les verrous et attentes, le retard de réplication, l'activité de l'autovacuum et le gonflement, l'âge des identifiants de transaction, l'espace disque et la croissance du WAL, les checkpoints et les entrées-sorties.

#### Qu'est-ce que le taux de succès du cache, et comment le calculer ?

La part des lectures de blocs servies depuis `shared_buffers`. Pour une charge OLTP, il doit en général dépasser 99 % :

```sql
SELECT round(100.0 * sum(blks_hit) / nullif(sum(blks_hit) + sum(blks_read), 0), 2)
FROM pg_stat_database;
```

#### Qu'est-ce que `statement_timeout`, et où le fixer ?

La durée maximale d'une instruction avant annulation. Fixez-la par rôle ou par application (par exemple 30 secondes pour une application web) pour protéger le serveur des requêtes qui s'emballent.

#### Que gère Amazon RDS for PostgreSQL pour vous ?

Le provisionnement, les sauvegardes automatiques et la PITR, les correctifs de versions mineures, la bascule Multi-AZ, les réplicas en lecture, la supervision et l'extension du stockage. Vous restez responsable du schéma, des requêtes, des utilisateurs, des paramètres et de l'accès réseau, et vous n'avez ni accès superutilisateur ni accès au système d'exploitation.

### Fonctionnalités avancées

#### Quelle est la différence entre `json` et `jsonb` ?

`json` stocke le texte d'entrée exact et l'analyse à chaque accès. `jsonb` stocke une forme binaire décomposée, supprime les espaces et les clés en double, est plus rapide à interroger et peut être indexé. `jsonb` est le choix habituel.

#### Quels sont les principaux opérateurs JSONB ?

`->` renvoie une valeur JSON, `->>` renvoie du texte, `#>` et `#>>` suivent un chemin, `@>` teste l'inclusion, `?` teste l'existence d'une clé, `||` concatène et `-` supprime une clé.

```sql
SELECT payload->>'user_id' AS user_id
FROM events
WHERE payload @> '{"type": "click"}';
```

#### Qu'est-ce que SQL/JSON path dans PostgreSQL ?

Un langage de requête pour le JSON (`jsonb_path_query`, `@?`, `@@`). PostgreSQL 17 ajoute les fonctions standard `JSON_TABLE`, `JSON_VALUE` et `JSON_QUERY` pour transformer du JSON en lignes relationnelles.

#### Comment transformer un tableau JSON en lignes ?

```sql
SELECT e.id, item->>'sku' AS sku, (item->>'qty')::int AS qty
FROM orders e, jsonb_array_elements(e.payload->'items') AS item;
```

#### Quand stocker des données en JSONB plutôt qu'en colonnes ?

Pour des attributs semi-structurés ou clairsemés qui varient d'une ligne à l'autre, ou des charges utiles brutes conservées pour référence. Les colonnes sont meilleures pour les champs sur lesquels on filtre, joint ou agrège régulièrement, car elles ont de vrais types, des contraintes et des statistiques.

#### Qu'est-ce que la recherche plein texte dans PostgreSQL ?

Rechercher dans des documents avec `tsvector` (lexèmes normalisés) et `tsquery`, avec une racinisation propre à chaque langue, un classement par pertinence (`ts_rank`) et des index GIN :

```sql
SELECT * FROM article
WHERE to_tsvector('english', body) @@ websearch_to_tsquery('english', 'data pipeline');
```

#### Qu'est-ce qu'une fonction PL/pgSQL ?

Une fonction écrite dans le langage procédural de PostgreSQL, avec variables, boucles, conditions et gestion des exceptions, exécutée dans le serveur.

#### Quelle est la différence entre une fonction et une procédure ?

Les fonctions renvoient une valeur, sont appelées dans des requêtes et s'exécutent dans la transaction de l'appelant. Les procédures (PostgreSQL 11+) sont invoquées par `CALL`, ne renvoient rien (ou des paramètres de sortie) et peuvent faire `COMMIT` et `ROLLBACK` à l'intérieur, ce qui convient aux traitements de maintenance par lots.

#### Que sont les catégories de volatilité des fonctions ?

`IMMUTABLE` (même résultat pour les mêmes arguments, toujours : nécessaire pour les index d'expression), `STABLE` (constante au sein d'une instruction) et `VOLATILE` (peut changer à chaque appel, la valeur par défaut). Bien les déclarer permet au planificateur d'optimiser.

#### Qu'est-ce qu'un trigger ?

Une fonction exécutée automatiquement avant ou après un `INSERT`, `UPDATE`, `DELETE` ou `TRUNCATE`, par ligne ou par instruction. Utilisé pour les journaux d'audit, la maintenance de colonnes dérivées ou des règles complexes. Les triggers cachent de la logique : utilisez-les avec parcimonie.

#### Comment tenir à jour une colonne `updated_at` avec un trigger ?

```sql
CREATE FUNCTION touch_updated_at() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at := now();
    RETURN NEW;
END $$;

CREATE TRIGGER company_touch BEFORE UPDATE ON company
FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
```

#### Que sont les extensions ? Citez-en quelques-unes d'utiles.

Des paquets qui ajoutent des fonctionnalités avec `CREATE EXTENSION` : `pg_stat_statements` (statistiques de requêtes), `pg_trgm` (similarité et index de trigrammes), `postgis` (géospatial), `pgcrypto`, `uuid-ossp`, `postgres_fdw`, `pg_partman` (gestion des partitions), `pgvector` (recherche de similarité vectorielle), `timescaledb` (séries temporelles), `citus` (distribution).

#### Qu'est-ce que le partitionnement de tables ?

Découper une grosse table en partitions par `RANGE`, `LIST` ou `HASH` d'une clé, derrière une table parente. Les requêtes qui filtrent sur la clé ne lisent que les partitions utiles (élagage des partitions), et les anciennes données peuvent être supprimées instantanément en détachant ou supprimant une partition.

```sql
CREATE TABLE events (id bigint, created_at timestamptz NOT NULL, payload jsonb)
PARTITION BY RANGE (created_at);
CREATE TABLE events_2026_10 PARTITION OF events
FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
```

#### Quand le partitionnement vaut-il la peine ?

Pour de très grosses tables avec une clé naturelle d'élagage (en général le temps) et un cycle de vie qui supprime ou archive les anciennes données. Il ajoute de la complexité : les clés primaires doivent inclure la clé de partitionnement, et trop de partitions ralentissent la planification.

#### Qu'est-ce que PostGIS ?

L'extension spatiale de PostgreSQL : types geometry et geography, fonctions spatiales (distance, intersection, zones tampons), index GiST et transformations de systèmes de coordonnées. C'est la référence des bases de données spatiales open source.

#### Qu'est-ce qu'un foreign data wrapper (FDW) ?

Une extension qui permet à PostgreSQL d'interroger des sources de données externes comme des tables locales : `postgres_fdw` (autres serveurs PostgreSQL), `file_fdw` (fichiers), et d'autres pour MySQL, Oracle, S3 ou Parquet.

#### Qu'est-ce que pgvector ?

Une extension qui ajoute un type `vector` et la recherche de similarité (cosinus, L2, produit scalaire) avec des index HNSW et IVFFlat. Utilisée pour stocker des embeddings pour la recherche sémantique et la génération augmentée par récupération.

#### Que fait `LISTEN` / `NOTIFY` ?

Un mécanisme intégré de publication/abonnement : une session envoie `NOTIFY channel, 'payload'` et toutes les sessions qui ont lancé `LISTEN channel` le reçoivent après le commit. Utile pour une invalidation de cache légère ou réveiller des traitements.

#### Quelles sont les fonctions de date les plus courantes ?

`now()` et `current_date`, `date_trunc('month', ts)`, `extract(year FROM ts)`, `age(a, b)`, l'arithmétique d'intervalles (`ts + interval '7 days'`), `to_char(ts, 'YYYY-MM')` et `make_date(y, m, d)`.

#### Comment générer rapidement des données de test dans PostgreSQL ?

Avec `generate_series` et des fonctions aléatoires :

```sql
INSERT INTO company (country_code, business_id, name, employees)
SELECT (ARRAY['FR','GB','IE','NO'])[1 + floor(random() * 4)::int],
       lpad(i::text, 9, '0'),
       'Company ' || i,
       floor(random() * 500)::int
FROM generate_series(1, 1000000) AS i;
```
