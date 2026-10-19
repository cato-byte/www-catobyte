## Fiche d'étude PostgreSQL

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude PostgreSQL : environ 200 questions](../../images/postgres_study_guide_title_img.png)

Environ 200 questions sur PostgreSQL et le SQL pour les entretiens de data engineer : architecture, types de données, requêtes, fonctions de fenêtrage, index, transactions et MVCC, optimisation des performances, modélisation des données, administration et fonctionnalités avancées comme JSONB et le partitionnement. Les exemples ciblent PostgreSQL 16 et 17.

La fiche suit un parcours d'apprentissage en quatre étapes. Chaque section est découpée en unités courtes : objectifs d'apprentissage, explication du concept et exemple commenté, puis questions (d'abord de mémorisation, ensuite d'application), un exercice pratique et les points à retenir. Pour **apprendre**, lisez chaque unité du début à la fin. Pour **réviser**, passez en mode révision ou utilisez « Aller aux questions », marquez les réponses à revoir et essayez une révision mixte entre les sections.

<!-- QA -->
<!-- stage: Fondamentaux -->

### Bases et architecture

<!-- unit: Architecture de PostgreSQL -->

<!-- goals -->

- Décrire le modèle de processus, le WAL et les checkpoints de PostgreSQL.
- Expliquer ACID et pourquoi les connexions coûtent cher.

<!-- concept -->

La conception de PostgreSQL explique une grande partie de son comportement. Chaque connexion cliente reçoit son propre processus système, ce qui est robuste mais coûte de la mémoire : des milliers de connexions directes font mal, et le pooling devient nécessaire.
La durabilité vient du write-ahead log : chaque changement est écrit d'abord dans le journal, puis dans les fichiers de données. Après un crash, rejouer le journal restaure le travail validé. Les checkpoints écrivent régulièrement les pages modifiées pour que le journal nécessaire à la reprise reste court. Ensemble, ils fournissent les garanties ACID.

<!-- example -->

```text
client ──► postmaster ──fork──► backend process (one per connection)
UPDATE ──► WAL record (fsync on COMMIT) ──► shared_buffers page (dirty)
checkpoint ──► dirty pages flushed to data files ──► old WAL recyclable
```

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

<!-- challenge -->

Un serveur perd l'alimentation en pleine transaction. Au redémarrage, les transactions validées sont-elles présentes et les autres disparues ? Pourquoi ?

<!-- solution -->

Oui. Le WAL des transactions validées a été écrit sur disque avant le retour de `COMMIT`, donc la reprise les rejoue ; les changements non validés n'ont pas d'enregistrement de commit et sont écartés.

<!-- takeaways -->

- Un processus par connexion : utilisez un pool.
- WAL d'abord, fichiers ensuite : la durabilité est garantie.
- Les checkpoints bornent le temps de reprise.

<!-- unit: Bases, schémas et tables -->

<!-- goals -->

- Naviguer entre clusters, bases, schémas et tables avec psql.
- Créer bases et tables avec clés primaires et comprendre le search path.

<!-- concept -->

PostgreSQL organise les objets en couches. Une instance contient des bases, isolées les unes des autres ; chaque base contient des schémas, espaces de noms pour les tables et autres objets. Les noms non qualifiés sont résolus par le search path, ce qui explique bien des surprises « table introuvable ».
Tout ce qui concerne ces objets, tables, colonnes, index et permissions, est lui-même stocké dans des tables du catalogue système interrogeables. psql est l'outil quotidien pour explorer tout cela.

<!-- example -->

```sql
CREATE DATABASE shop OWNER app_owner ENCODING 'UTF8';
\c shop
CREATE SCHEMA sales;
CREATE TABLE sales.company (
  company_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  country_code char(2) NOT NULL,
  business_id text NOT NULL,
  UNIQUE (country_code, business_id)
);
\dt sales.*
```

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

<!-- challenge -->

`SELECT * FROM orders` échoue avec « relation does not exist », mais la table est visible dans un outil graphique. Que vérifiez-vous ?

<!-- solution -->

Le schéma et le search path : la table vit sans doute dans un autre schéma (par exemple `sales.orders`) absent du `search_path`, ou dans une autre base. Qualifier le nom ou ajuster le search path.

<!-- takeaways -->

- Les instances contiennent des bases ; les bases, des schémas.
- Le search path résout les noms non qualifiés.
- Le catalogue système décrit chaque objet.

<!-- unit: Au-delà des tables -->

<!-- goals -->

- Utiliser séquences, colonnes identity, vues et vues matérialisées.
- Choisir entre DELETE, TRUNCATE et DROP.

<!-- concept -->

Les tables sont entourées d'objets auxiliaires. Les séquences génèrent des nombres pour les clés, et les colonnes identity sont la façon moderne et standard de les rattacher. Les vues stockent des requêtes, recalculées à chaque lecture ; les vues matérialisées stockent des résultats, rafraîchis sur demande.
Supprimer des données passe par trois outils aux effets très différents : effacer des lignes une à une, vider toute la table instantanément, ou supprimer la table elle-même.

<!-- example -->

| Opération | Supprime | Vitesse | WHERE ? | Laisse des tuples morts |
|---|---|---|---|---|
| `DELETE` | Lignes choisies | Ligne par ligne | Oui | Oui |
| `TRUNCATE` | Toutes les lignes | Instantanée | Non | Non |
| `DROP TABLE` | La table elle-même | Instantanée | Non | n/a |

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

<!-- challenge -->

Un job nocturne vide une table de staging de 50 millions de lignes avec `DELETE FROM staging`, et la table ne cesse de grossir sur disque. Que changez-vous ?

<!-- solution -->

Utiliser `TRUNCATE staging`, qui supprime toutes les lignes instantanément sans laisser de tuples morts. `DELETE` marque les lignes comme mortes et compte sur vacuum pour récupérer l'espace.

<!-- takeaways -->

- Les colonnes identity sont la façon standard de générer des clés.
- Les vues recalculent ; les vues matérialisées stockent.
- TRUNCATE vide une table sans tuples morts.

<!-- unit: Stockage physique -->

<!-- goals -->

- Expliquer comment PostgreSQL stocke les grandes valeurs avec TOAST.
- Utiliser des tablespaces pour placer les données sur différents disques.

<!-- concept -->

Les lignes vivent dans des pages de taille fixe : les très grandes valeurs exigent un traitement particulier. TOAST les compresse et, si elles restent grandes, les déplace dans une table annexe, ce qui garde la table principale compacte et rapide à parcourir quand ces colonnes ne sont pas lues.
Les tablespaces associent des objets à des répertoires sur disque, pour placer certaines tables ou index sur un stockage plus rapide ou plus grand. En service managé, ils sont rarement utiles.

<!-- example -->

```sql
SELECT pg_size_pretty(pg_relation_size('documents'))        AS main,
       pg_size_pretty(pg_total_relation_size('documents'))  AS total;   -- includes TOAST and indexes
CREATE TABLESPACE fast_ssd LOCATION '/mnt/nvme/pg';
ALTER INDEX orders_created_idx SET TABLESPACE fast_ssd;
```

#### Qu'est-ce qu'un tablespace ?

Un répertoire sur disque où PostgreSQL peut stocker des objets, ce qui permet de placer certaines tables ou certains index sur un autre stockage.

#### Qu'est-ce que le catalogue système ?

Les tables de `pg_catalog` (comme `pg_class`, `pg_attribute`, `pg_index`) qui décrivent tous les objets, ainsi que les vues standard d'`information_schema`.

<!-- challenge -->

Une table `documents` est petite sur disque, mais `pg_total_relation_size` affiche 400 Go. Où est l'espace, et cela ralentit-il les requêtes qui ne lisent pas le contenu ?

<!-- solution -->

Surtout dans la table TOAST qui contient les grandes valeurs de `content`. Les requêtes qui ne sélectionnent pas cette colonne ne lisent pas TOAST et restent rapides.

<!-- takeaways -->

- TOAST compresse et déporte les grandes valeurs.
- Les requêtes qui ne lisent pas ces colonnes ignorent TOAST.
- Les tablespaces placent les objets sur le stockage choisi.

### Types de données et DDL

<!-- unit: Choisir les types de données -->

<!-- goals -->

- Choisir correctement types numériques, texte, date et heure.
- Arbitrer entre timestamp et timestamptz, et générer des UUID.

<!-- concept -->

Les types sont des règles : ils décident quelles valeurs sont valides, comment elles se comparent et quelle place elles prennent. Décimaux exacts pour l'argent, entiers pour les comptes et les clés, texte sans limite arbitraire. Le temps est le piège classique : `timestamptz` enregistre un instant, tandis que `timestamp` enregistre une heure d'horloge sans fuseau, ambiguë dès que les systèmes couvrent plusieurs fuseaux.
Les UUID sont utiles quand les clés doivent être générées hors de la base.

<!-- example -->

```sql
CREATE TABLE payment (
  payment_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  amount numeric(12,2) NOT NULL,          -- exact money
  currency char(3) NOT NULL,
  paid_at timestamptz NOT NULL,           -- an instant
  is_refund boolean NOT NULL DEFAULT false,
  note text
);
```

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

<!-- challenge -->

Les totaux de montants en `double precision` sont faux d'un centime dans les rapports financiers. Quel type utiliser, et pourquoi ?

<!-- solution -->

`numeric(p, s)`, qui stocke des décimaux exacts. Les types à virgule flottante approchent les valeurs en binaire : la somme de nombreux montants accumule des erreurs d'arrondi.

<!-- takeaways -->

- `numeric` pour l'argent ; entiers pour clés et comptes.
- `timestamptz` pour les instants.
- `text` convient ; limitez la longueur seulement si c'est une règle.

<!-- unit: Types riches -->

<!-- goals -->

- Utiliser tableaux, plages, enums et domaines.
- Calculer des valeurs avec des colonnes générées.

<!-- concept -->

Les types de PostgreSQL vont au-delà des bases du SQL. Les tableaux stockent des listes dans une colonne ; les plages représentent des intervalles et peuvent empêcher les chevauchements ; les enums fixent un ensemble de valeurs ; les domaines attachent des contraintes à un type réutilisable. Les colonnes générées calculent automatiquement des valeurs à partir d'autres colonnes.
Chacun économise du code ailleurs, mais chacun sacrifie aussi de la souplesse : les enums se réduisent mal, et les tableaux ne remplacent pas des tables liées quand les éléments ont leurs propres attributs.

<!-- example -->

```sql
CREATE DOMAIN email AS text CHECK (VALUE ~* '^[^@\s]+@[^@\s]+$');
CREATE TABLE booking (
  room_id int,
  during tstzrange NOT NULL,
  tags text[] DEFAULT '{}',
  guest_email email,
  nights int GENERATED ALWAYS AS (upper(during)::date - lower(during)::date) STORED,
  EXCLUDE USING gist (room_id WITH =, during WITH &&)   -- no double bookings (btree_gist)
);
```

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

<!-- challenge -->

Les catégories de produits sont stockées en enum, et le métier renomme et supprime des catégories chaque trimestre. Un enum est-il un bon choix ?

<!-- solution -->

Non. Les valeurs d'un enum s'ajoutent facilement mais se renomment, se réordonnent ou se suppriment mal. Utiliser une table de référence avec clé étrangère, qui permet changements, descriptions et historique.

<!-- takeaways -->

- Tableaux, plages, enums et domaines encodent des règles dans les types.
- Les contraintes d'exclusion sur plages empêchent les chevauchements.
- Utilisez des tables de référence pour les valeurs qui changent.

<!-- unit: Contraintes et clés -->

<!-- goals -->

- Utiliser les principaux types de contraintes, dont les clés étrangères.
- Choisir le comportement ON DELETE et indexer les clés étrangères.

<!-- concept -->

Les contraintes permettent à la base de refuser les mauvaises données au lieu de faire confiance à chaque application. Clés et unicité empêchent les doublons, les checks imposent des règles, les exclusions empêchent les chevauchements, et les clés étrangères garantissent l'existence des références.
Les clés étrangères demandent deux décisions : ce qui arrive aux enfants quand un parent est supprimé, et un index sur la colonne référençante, que PostgreSQL ne crée pas pour vous. Sans lui, les suppressions côté parent parcourent la table enfant.

<!-- example -->

```sql
CREATE TABLE order_line (
  order_id bigint NOT NULL REFERENCES orders (order_id) ON DELETE CASCADE,
  line_no int NOT NULL,
  qty int NOT NULL CHECK (qty > 0),
  PRIMARY KEY (order_id, line_no)
);
CREATE INDEX ON order_line (order_id);   -- often covered by the PK; needed if it doesn't lead
```

#### Les colonnes de clé étrangère sont-elles indexées automatiquement ?

Non. PostgreSQL indexe la clé référencée (celle du parent) mais pas la colonne qui référence. Indexez les colonnes de clé étrangère utilisées dans les jointures ou vérifiées lors des suppressions sur le parent.

#### Qu'est-ce qu'une colonne générée ?

Une colonne calculée à partir d'autres colonnes : `total numeric GENERATED ALWAYS AS (price * qty) STORED`. PostgreSQL la calcule à l'écriture.

#### Qu'est-ce qu'un domaine ?

Un type de données assorti de contraintes, réutilisable dans plusieurs tables : `CREATE DOMAIN postcode_fr AS text CHECK (VALUE ~ '^\d{5}$')`.

<!-- challenge -->

Supprimer un client prend 30 secondes. La table `orders` référence customers par une clé étrangère. Quelle est la cause probable ?

<!-- solution -->

`orders.customer_id` n'est pas indexée : chaque suppression parcourt toute la table des commandes pour vérifier les références. Créer un index sur la colonne de la clé étrangère.

<!-- takeaways -->

- Les contraintes imposent les règles dans la base.
- Choisissez délibérément le comportement ON DELETE.
- Indexez vous-même les colonnes de clés étrangères.

<!-- unit: Modifier les tables en sécurité -->

<!-- goals -->

- Ajouter colonnes et contraintes à de grosses tables sans longs verrous.
- Utiliser à bon escient tables temporaires et unlogged.

<!-- concept -->

Sur une table très sollicitée, la façon de changer le schéma compte autant que le changement. Certains changements sont instantanés ; d'autres réécrivent la table ou la parcourent en tenant un verrou qui bloque tout le monde. Ajouter une colonne avec une valeur par défaut constante est désormais instantané, et une contrainte peut être ajoutée non validée, puis validée sans bloquer les écritures.
Les tables temporaires et unlogged échangent durabilité contre vitesse, ce qui convient aux données de travail et de staging.

<!-- example -->

```sql
ALTER TABLE orders ADD COLUMN channel text DEFAULT 'web';          -- instant
ALTER TABLE orders ADD CONSTRAINT orders_amount_pos CHECK (amount >= 0) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT orders_amount_pos;          -- scans without blocking writes
CREATE UNLOGGED TABLE staging_orders (LIKE orders);                -- fast, not crash-safe
```

#### Comment ajouter une colonne à une grosse table sans risque ?

`ALTER TABLE t ADD COLUMN c type` est instantané, même avec une valeur par défaut constante (depuis PostgreSQL 11). Les valeurs par défaut volatiles, les changements de type qui réécrivent la table et l'ajout de `NOT NULL` avec une passe de validation demandent plus de précautions.

#### Comment ajouter une contrainte sans bloquer la table longtemps ?

L'ajouter en `NOT VALID` (appliquée aux nouvelles lignes seulement), puis lancer `ALTER TABLE ... VALIDATE CONSTRAINT`, qui prend un verrou plus faible pendant la vérification des lignes existantes.

#### Qu'est-ce qu'une table temporaire ?

Une table visible seulement par la session courante et supprimée à sa fin (ou à la validation avec `ON COMMIT DROP`). Utile pour des résultats intermédiaires.

#### Qu'est-ce qu'une table unlogged ?

Une table dont les modifications ne sont pas écrites dans le WAL. Les écritures sont bien plus rapides, mais la table est vidée après une panne et n'est pas répliquée. Utile pour des données de staging qu'on peut recharger.

<!-- challenge -->

Une migration ajoute une clé étrangère à une table de 500 millions de lignes et bloque les écritures pendant 20 minutes. Comment aurait-il fallu l'écrire ?

<!-- solution -->

Ajouter la clé étrangère avec `NOT VALID` (rapide, appliquée aux nouvelles lignes), puis lancer séparément `VALIDATE CONSTRAINT`, qui vérifie les lignes existantes avec un verrou plus faible ne bloquant pas les écritures.

<!-- takeaways -->

- Certains DDL sont instantanés ; d'autres réécrivent ou bloquent.
- Utilisez `NOT VALID` puis `VALIDATE` pour les contraintes.
- Les tables unlogged sont rapides mais pas sûres en cas de crash.

<!-- unit: Travailler avec NULL -->

<!-- goals -->

- Expliquer le comportement de NULL dans les comparaisons.
- Utiliser COALESCE et NULLIF.

<!-- concept -->

`NULL` signifie inconnu, et l'inconnu se propage : comparer quoi que ce soit à `NULL` donne inconnu, que les filtres traitent comme faux. C'est pourquoi `= NULL` ne correspond jamais et pourquoi des lignes disparaissent silencieusement des `WHERE` qui l'oublient.
Deux fonctions couvrent la plupart des cas : l'une remplace les valeurs manquantes par une valeur par défaut, l'autre transforme une valeur précise en `NULL`, ce qui évite des erreurs comme la division par zéro.

<!-- example -->

```sql
SELECT count(*) FROM customer WHERE phone = NULL;     -- always 0
SELECT count(*) FROM customer WHERE phone IS NULL;    -- correct
SELECT COALESCE(nickname, first_name, 'unknown') AS display_name FROM customer;
SELECT revenue / NULLIF(orders, 0) AS avg_order FROM daily_stats;
```

#### Que signifie `NULL`, et comment se comporte-t-il dans les comparaisons ?

Une valeur inconnue ou absente. Toute comparaison avec `NULL` renvoie `NULL` (et non vrai) : il faut utiliser `IS NULL` / `IS NOT NULL`, et `IS DISTINCT FROM` pour des comparaisons sûres vis-à-vis des nulls.

#### Que fait `COALESCE` ?

Elle renvoie le premier argument non nul : `COALESCE(nickname, first_name, 'unknown')`.

#### Qu'est-ce que `NULLIF` ?

`NULLIF(a, b)` renvoie `NULL` si `a = b`, sinon `a`. Pratique pour éviter la division par zéro : `x / NULLIF(y, 0)`.

<!-- challenge -->

`WHERE status <> 'cancelled'` renvoie moins de lignes que prévu. Certaines lignes ont `status` à NULL. Comment les inclure ?

<!-- solution -->

`WHERE status IS DISTINCT FROM 'cancelled'` (ou `status <> 'cancelled' OR status IS NULL`), car `NULL <> 'cancelled'` est inconnu et filtré.

<!-- takeaways -->

- Les comparaisons avec NULL sont inconnues.
- Utilisez `IS NULL` et `IS DISTINCT FROM`.
- `COALESCE` donne un défaut ; `NULLIF` évite la division par zéro.

<!-- stage: Interroger -->

### Requêtes : jointures, sous-requêtes et CTE

<!-- unit: Jointures -->

<!-- goals -->

- Choisir le bon type de jointure et placer correctement les conditions.
- Écrire semi-jointures, anti-jointures et jointures LATERAL.

<!-- concept -->

Les jointures combinent des tables, et de petits détails changent les résultats. Dans une jointure gauche, une condition dans `ON` décide quelles lignes de droite correspondent tout en gardant chaque ligne de gauche ; la même condition dans `WHERE` filtre ensuite et transforme silencieusement la jointure en jointure interne.
Les questions « a une correspondance » et « n'en a pas » sont des semi- et anti-jointures, mieux écrites avec `EXISTS` et `NOT EXISTS`. LATERAL laisse une sous-requête utiliser les colonnes des tables précédentes, par exemple pour récupérer les trois dernières commandes par client.

<!-- example -->

```sql
-- customers with no orders in 2026 (anti-join)
SELECT c.*
FROM customer c
WHERE NOT EXISTS (
  SELECT 1 FROM orders o
  WHERE o.customer_id = c.customer_id AND o.ordered_at >= '2026-01-01'
);
```

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

<!-- challenge -->

`SELECT * FROM customer WHERE customer_id NOT IN (SELECT customer_id FROM orders)` ne renvoie aucune ligne, alors que certains clients n'ont pas de commande. Pourquoi ?

<!-- solution -->

`orders.customer_id` contient un `NULL` : `NOT IN` compare alors à un inconnu et ne renvoie rien. Utiliser `NOT EXISTS`, insensible aux NULL.

<!-- takeaways -->

- Les conditions `ON` apparient ; les conditions `WHERE` filtrent.
- Utilisez `EXISTS` / `NOT EXISTS` pour semi- et anti-jointures.
- Les sous-requêtes LATERAL utilisent les colonnes des tables précédentes.

<!-- unit: Sous-requêtes, CTE et opérations ensemblistes -->

<!-- goals -->

- Structurer les requêtes avec des CTE, y compris récursives.
- Utiliser correctement sous-requêtes corrélées et opérations ensemblistes.

<!-- concept -->

Les questions complexes se lisent mieux par étapes. Les CTE nomment chaque étape ; les CTE récursives parcourent des hiérarchies comme des organigrammes ou génèrent des séquences. Les sous-requêtes corrélées font référence à la ligne externe et sont souvent réécrites en jointures par le planificateur.
Les opérations ensemblistes combinent des résultats verticalement : union supprime les doublons à un certain coût, union all se contente d'ajouter, et intersect et except comparent deux résultats, pratique pour vérifier des écarts.

<!-- example -->

```sql
WITH RECURSIVE chain AS (
  SELECT employee_id, manager_id, name, 1 AS depth FROM employee WHERE employee_id = 42
  UNION ALL
  SELECT e.employee_id, e.manager_id, e.name, c.depth + 1
  FROM employee e JOIN chain c ON e.employee_id = c.manager_id
)
SELECT * FROM chain;            -- employee 42 and every manager above
```

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

<!-- challenge -->

Comment vérifier qu'une requête réécrite renvoie exactement les mêmes lignes que l'ancienne ?

<!-- solution -->

Exécuter `(old EXCEPT new)` et `(new EXCEPT old)` ; les deux doivent être vides. Pour les doublons, comparer avec `EXCEPT ALL` ou des comptages par ligne.

<!-- takeaways -->

- Les CTE rendent les étapes lisibles ; les récursives parcourent des hiérarchies.
- `UNION ALL` sauf besoin de dédupliquer.
- `EXCEPT` dans les deux sens compare deux résultats.

<!-- unit: Comment s'exécute un SELECT -->

<!-- goals -->

- Expliquer l'ordre logique d'un SELECT.
- Utiliser HAVING, DISTINCT ON, la pagination par clé et generate_series.

<!-- concept -->

Le SQL s'écrit de haut en bas mais s'évalue dans un autre ordre : les lignes sont rassemblées et filtrées, groupées, filtrées à nouveau, fenêtrées, projetées, dédupliquées, triées et limitées. Cet ordre explique pourquoi les alias ne s'utilisent pas dans `WHERE` et pourquoi on ne peut filtrer une fonction de fenêtrage sans sous-requête.
Certaines fonctions de PostgreSQL s'appuient dessus : `DISTINCT ON` garde une ligne par groupe selon le tri, la pagination par clé évite de lire les lignes sautées, et `generate_series` comble les dates manquantes.

<!-- example -->

```sql
-- latest order per customer
SELECT DISTINCT ON (customer_id) customer_id, order_id, ordered_at
FROM orders
ORDER BY customer_id, ordered_at DESC;

-- next page after the last seen row (keyset)
SELECT * FROM orders WHERE (ordered_at, order_id) < ('2026-10-17 09:00', 98123)
ORDER BY ordered_at DESC, order_id DESC LIMIT 50;
```

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

<!-- challenge -->

Une API pagine les commandes avec `OFFSET 200000 LIMIT 50` et les pages profondes tombent en timeout. Que changez-vous ?

<!-- solution -->

Passer à la pagination par clé : retenir la clé de tri de la dernière ligne (par exemple `ordered_at, order_id`) et filtrer `WHERE (ordered_at, order_id) < (...)` avec un index adapté, pour que chaque page ne lise que 50 lignes.

<!-- takeaways -->

- Ordre d'évaluation : FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY.
- `DISTINCT ON` garde une ligne par groupe.
- La pagination par clé reste rapide sur les pages profondes.

<!-- unit: Écrire des données -->

<!-- goals -->

- Faire des upserts avec ON CONFLICT et MERGE, et renvoyer les lignes touchées.
- Trouver et supprimer les lignes en double.

<!-- concept -->

Les écritures dépendent souvent de l'existant. `INSERT ... ON CONFLICT` insère ou met à jour en une instruction atomique, en détectant les conflits par une contrainte d'unicité. `MERGE` gère des cas plus riches, suppressions comprises, à partir d'une source de changements. `RETURNING` renvoie les lignes touchées et évite une requête de plus.
Les doublons sont le problème inverse : les trouver en groupant sur la clé voulue, supprimer tous sauf un par groupe, puis ajouter la contrainte d'unicité qui aurait dû les empêcher.

<!-- example -->

```sql
INSERT INTO company (country_code, business_id, name)
VALUES ('FR', '123456789', 'Acme')
ON CONFLICT (country_code, business_id)
DO UPDATE SET name = EXCLUDED.name
RETURNING company_id, (xmax = 0) AS inserted;
```

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

<!-- challenge -->

Un upsert avec `ON CONFLICT (email)` échoue avec « there is no unique or exclusion constraint matching ». Que manque-t-il ?

<!-- solution -->

Une contrainte ou un index unique sur `email`. `ON CONFLICT` en a besoin pour détecter les conflits ; le créer (après suppression des doublons existants).

<!-- takeaways -->

- `ON CONFLICT` fait un upsert atomique sur une clé unique.
- `MERGE` applique insertions, mises à jour et suppressions depuis une source.
- Supprimez les doublons, puis ajoutez la contrainte manquante.

### Agrégation et fonctions de fenêtrage

<!-- unit: Agrégats -->

<!-- goals -->

- Utiliser les agrégats courants et la clause FILTER.
- Produire des totaux multiniveaux et des pivots.

<!-- concept -->

L'agrégation résume des lignes, et quelques détails décident si le résumé est juste. Compter les lignes, les valeurs non nulles et les valeurs distinctes donne trois nombres différents. Des filtres à l'intérieur d'un agrégat calculent plusieurs totaux conditionnels en une passe.
Les grouping sets produisent sous-totaux et total général en une requête, et l'agrégation conditionnelle pivote les lignes en colonnes, la façon habituelle de produire en SQL des résultats en forme de rapport.

<!-- example -->

```sql
SELECT country_code,
       count(*)                                  AS orders,
       count(DISTINCT customer_id)               AS customers,
       sum(amount) FILTER (WHERE status = 'paid') AS paid_amount,
       string_agg(DISTINCT channel, ', ' ORDER BY channel) AS channels
FROM orders
GROUP BY ROLLUP (country_code);
```

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

<!-- challenge -->

Un rapport a besoin du CA par pays pour 2024, 2025 et 2026 en trois colonnes. Écrivez-en le cœur.

<!-- solution -->

`SELECT country_code, sum(amount) FILTER (WHERE extract(year FROM ordered_at) = 2024) AS y2024, ... 2025 ..., ... 2026 ... FROM orders GROUP BY country_code`.

<!-- takeaways -->

- `count(*)`, `count(col)` et `count(DISTINCT col)` diffèrent.
- `FILTER` donne des agrégats conditionnels.
- `ROLLUP` ajoute des sous-totaux ; `FILTER` pivote.

<!-- unit: Bases des fonctions de fenêtrage -->

<!-- goals -->

- Expliquer les fonctions de fenêtrage et de classement.
- Obtenir le top N par groupe et comparer aux lignes précédentes.

<!-- concept -->

Les fonctions de fenêtrage calculent sur des lignes liées tout en gardant chaque ligne dans le résultat. La fenêtre se définit par une partition (quelles lignes vont ensemble) et un ordre (leur séquence). Classer au sein d'un groupe, comparer à la ligne précédente ou numéroter les lignes tient alors en une expression.
Comme les fenêtres sont calculées après `WHERE`, filtrer sur leurs résultats exige une requête externe. Les fenêtres nommées évitent de répéter de longues définitions.

<!-- example -->

```sql
SELECT * FROM (
  SELECT product_id, category, revenue,
         rank() OVER w AS rnk,
         revenue - lag(revenue) OVER w AS diff_to_previous
  FROM product_revenue
  WINDOW w AS (PARTITION BY category ORDER BY revenue DESC)
) t
WHERE rnk <= 3;
```

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

<!-- challenge -->

Quelqu'un écrit `WHERE row_number() OVER (...) = 1` et obtient une erreur. Comment corriger ?

<!-- solution -->

Les fonctions de fenêtrage s'exécutent après `WHERE` : calculer le numéro de ligne dans une sous-requête ou une CTE et filtrer dans la requête externe (ou utiliser `DISTINCT ON` pour la première ligne par groupe).

<!-- takeaways -->

- Les fenêtres calculent sur des partitions sans regrouper les lignes.
- Les fonctions de classement diffèrent sur les ex æquo.
- Filtrez les résultats de fenêtre dans une requête externe.

<!-- unit: Frames et calculs cumulés -->

<!-- goals -->

- Définir des frames de fenêtre avec ROWS et RANGE.
- Calculer cumuls, moyennes mobiles et croissance par période.

<!-- concept -->

Les fenêtres ordonnées ont un frame : les lignes autour de la ligne courante que voit la fonction. Le frame par défaut va du début à la ligne courante, ce qui fait fonctionner les cumuls mais explique aussi les surprises de `last_value`.
Choisir entre compter des lignes et couvrir une plage de valeurs compte en présence de trous ou d'ex æquo : un frame de sept lignes et un frame de sept jours diffèrent dès qu'il manque des jours.

<!-- example -->

```sql
SELECT day, amount,
       sum(amount) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
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

<!-- challenge -->

`last_value(price) OVER (PARTITION BY product ORDER BY changed_at)` renvoie le prix de chaque ligne au lieu du dernier. Pourquoi, et comment corriger ?

<!-- solution -->

Le frame par défaut s'arrête à la ligne courante : la « dernière » valeur est donc la valeur courante. Utiliser `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`, ou `first_value` avec un tri décroissant.

<!-- takeaways -->

- Les frames définissent les lignes vues par une fonction de fenêtrage.
- `ROWS` compte des lignes ; `RANGE` couvre des plages de valeurs.
- Le frame par défaut s'arrête à la ligne courante.

<!-- unit: Distributions et séquences -->

<!-- goals -->

- Calculer percentiles, tranches et parts du total.
- Résoudre des problèmes de gaps and islands.

<!-- concept -->

Les moyennes cachent les distributions. Médianes et percentiles décrivent honnêtement les données asymétriques, les tranches répartissent les lignes en quartiles ou déciles, et une fenêtre sur tout le résultat transforme des comptages en parts du total.
Les séquences d'événements posent un autre classique : trouver des séries consécutives, comme les jours d'activité d'affilée d'un utilisateur. Soustraire un numéro de ligne à la date donne à chaque série une clé constante : c'est le cœur de la technique gaps and islands.

<!-- example -->

```sql
WITH d AS (
  SELECT user_id, day, day - (row_number() OVER (PARTITION BY user_id ORDER BY day))::int AS grp
  FROM (SELECT DISTINCT user_id, day FROM activity) a
)
SELECT user_id, min(day) AS start_day, max(day) AS end_day, count(*) AS streak
FROM d GROUP BY user_id, grp
ORDER BY streak DESC;
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

<!-- challenge -->

Le panier moyen est de 120, mais la plupart des commandes tournent autour de 40. Comment mieux décrire la commande typique en une requête ?

<!-- solution -->

Utiliser `percentile_cont(0.5) WITHIN GROUP (ORDER BY amount)` pour la médiane, plus p90 et p99, qui révèlent que quelques grosses commandes gonflent la moyenne.

<!-- takeaways -->

- Médianes et percentiles décrivent les données asymétriques.
- `sum(...) OVER ()` donne des parts du total.
- Gaps and islands : date moins numéro de ligne regroupe les séries.

<!-- stage: Performance -->

### Index

<!-- unit: Types d'index -->

<!-- goals -->

- Choisir entre index B-tree, hash, GIN, GiST, BRIN et uniques.
- Expliquer le fonctionnement des B-trees et le rôle de CLUSTER.

<!-- concept -->

Un index est une structure séparée qui permet à PostgreSQL de trouver des lignes sans lire toute la table. Chaque type convient à un genre de question : B-trees pour l'égalité, les plages et le tri ; GIN pour les questions « contient » sur tableaux, JSON et texte ; GiST pour les données géométriques et de plages ; BRIN pour d'énormes tables dont les valeurs suivent l'ordre physique.
Les index uniques imposent aussi des règles. PostgreSQL ne garde jamais les tables triées physiquement ; `CLUSTER` réordonne une fois, puis l'ordre se dégrade.

<!-- example -->

| Requête | Index |
|---|---|
| `WHERE email = ?`, `ORDER BY created_at` | B-tree |
| `WHERE tags @> '{sale}'`, JSONB `@>` | GIN |
| `WHERE during && tstzrange(...)` | GiST |
| `WHERE logged_at > now() - interval '1 day'` sur 5 To en ajout seul | BRIN |

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

<!-- challenge -->

Une table de journaux de 3 To en ajout seul est interrogée par plage de temps. Un B-tree sur `logged_at` fait 90 Go. Quelle alternative envisagez-vous ?

<!-- solution -->

Un index BRIN sur `logged_at` : les lignes étant ajoutées dans l'ordre du temps, BRIN stocke min/max par plage de blocs et ne pèse que quelques Mo tout en élaguant l'essentiel de la table.

<!-- takeaways -->

- Choisissez le type d'index selon la forme de la requête.
- B-tree par défaut ; GIN et GiST pour les types complexes.
- BRIN est minuscule pour d'énormes tables naturellement ordonnées.

<!-- unit: Concevoir les index -->

<!-- goals -->

- Concevoir des index composites, partiels, sur expression et couvrants.
- Obtenir des index-only scans et éviter les index redondants.

<!-- concept -->

De bons index correspondent à la façon dont les requêtes filtrent et trient. Dans un index composite, les colonnes s'utilisent de gauche à droite : colonnes d'égalité d'abord, colonnes de plage en dernier ; un index composite rend généralement redondant un index sur sa première colonne.
Les index peuvent être plus étroits ou plus riches qu'une colonne : les index partiels ne couvrent que les lignes demandées, les index sur expression couvrent des valeurs calculées, et les colonnes incluses laissent l'index répondre seul à une requête, si la visibility map le permet.

<!-- example -->

```sql
CREATE INDEX ON orders (customer_id, ordered_at);                     -- composite
CREATE INDEX ON orders (ordered_at) WHERE status = 'pending';         -- partial
CREATE INDEX ON customer (lower(email));                              -- expression
CREATE INDEX ON orders (customer_id) INCLUDE (amount);                -- covering
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

<!-- challenge -->

Les requêtes filtrent `WHERE status = 'pending' AND ordered_at > now() - interval '1 day'` ; 99 % des commandes ne sont pas en attente. Quel index convient le mieux ?

<!-- solution -->

Un index partiel `ON orders (ordered_at) WHERE status = 'pending'` : il ne contient que les lignes en attente, il est donc petit et correspond exactement à la requête.

<!-- takeaways -->

- Ordre composite : égalités d'abord, plages en dernier.
- Index partiels et sur expression ciblent des requêtes précises.
- Les index couvrants permettent les index-only scans.

<!-- unit: Index pour données particulières -->

<!-- goals -->

- Indexer des documents JSONB et des recherches de sous-chaînes.
- Comprendre les pending lists de GIN.

<!-- concept -->

Certaines requêtes ne peuvent pas utiliser des B-trees ordinaires. Chercher dans des documents JSON, tester une inclusion ou trouver un texte n'importe où dans une chaîne exige des index inversés. GIN indexe chaque clé ou trigramme pour transformer ces recherches en parcours d'index.
GIN coûte cher à mettre à jour : il tamponne les nouvelles entrées dans une pending list et les fusionne plus tard. Les écritures vont plus vite, mais les lectures peuvent être irrégulières jusqu'à la fusion.

<!-- example -->

```sql
CREATE INDEX ON events USING gin (payload jsonb_path_ops);    -- payload @> '{"type":"click"}'
CREATE INDEX ON events ((payload->>'user_id'));               -- equality on one key
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX ON company USING gin (name gin_trgm_ops);        -- name ILIKE '%acme%'
```

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

<!-- challenge -->

Des recherches `name ILIKE '%dupont%'` sur 20 millions d'entreprises prennent 8 secondes. Qu'ajoutez-vous ?

<!-- solution -->

Un index GIN de trigrammes (`pg_trgm`, `gin_trgm_ops`) sur `name`, qui prend en charge `LIKE`/`ILIKE` avec joker initial.

<!-- takeaways -->

- GIN indexe clés et trigrammes pour inclusion et sous-chaînes.
- Les index sur expression couvrent une clé JSON précise.
- GIN tamponne les écritures dans une pending list.

<!-- unit: Coût et entretien des index -->

<!-- goals -->

- Peser le coût des index et comprendre pourquoi ils sont ignorés.
- Créer, reconstruire, trouver et mesurer les index en sécurité.

<!-- concept -->

Les index ne sont pas gratuits : chacun ralentit chaque écriture et prend de la place, et un index inutilisé n'est que du coût. Le planificateur ignore aussi les index quand un parcours coûte moins, quand les statistiques le trompent ou quand la requête enveloppe la colonne dans une fonction.
L'entretien en découle : construire les index sans bloquer les écritures, reconstruire de même les index gonflés, chercher les index manquants dans les statistiques de parcours et les requêtes lentes, et supprimer ceux que personne n'utilise.

<!-- example -->

```sql
CREATE INDEX CONCURRENTLY orders_customer_idx ON orders (customer_id);
REINDEX INDEX CONCURRENTLY orders_customer_idx;
SELECT relname, seq_scan, seq_tup_read, idx_scan FROM pg_stat_user_tables ORDER BY seq_tup_read DESC LIMIT 10;
SELECT pg_size_pretty(pg_indexes_size('orders'));
```

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

<!-- challenge -->

Une table a 14 index, et les insertions sont devenues lentes. Comment décider lesquels supprimer ?

<!-- solution -->

Vérifier `pg_stat_user_indexes.idx_scan` sur une période représentative (hors index uniques et de contraintes), repérer les doublons et les préfixes d'index composites, et supprimer les inutilisés en notant de quoi les recréer si besoin.

<!-- takeaways -->

- Chaque index ralentit les écritures et prend de la place.
- Construisez et reconstruisez les index en concurrent.
- Trouvez index manquants et inutilisés grâce aux statistiques.

### Transactions, MVCC et concurrence

<!-- unit: Transactions et MVCC -->

<!-- goals -->

- Expliquer transactions, MVCC et tuples morts.
- Utiliser à bon escient savepoints, HOT updates et commit asynchrone.

<!-- concept -->

PostgreSQL laisse lecteurs et écrivains travailler en même temps en gardant plusieurs versions des lignes. Une mise à jour écrit une nouvelle version ; les transactions voient la version qui correspond à leur snapshot. Personne n'attend les lecteurs, mais les anciennes versions s'accumulent en tuples morts jusqu'à ce que vacuum les supprime.
Certaines optimisations réduisent ce coût : les mises à jour qui ne touchent pas de colonne indexée peuvent rester dans la même page sans modifier les index. Les savepoints permettent un rollback partiel, et assouplir la durabilité du commit échange une petite fenêtre de perte contre de la vitesse.

<!-- example -->

```sql
BEGIN;
UPDATE account SET balance = balance - 100 WHERE account_id = 1;
SAVEPOINT before_fee;
UPDATE account SET balance = balance - 2 WHERE account_id = 1;
ROLLBACK TO before_fee;         -- undo only the fee
COMMIT;
```

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

<!-- challenge -->

Une table mise à jour en permanence ne cesse de grossir, ses index aussi, alors que le nombre de lignes ne change pas. Quel détail du MVCC pouvez-vous exploiter pour limiter la croissance des index ?

<!-- solution -->

Activer les HOT updates : éviter d'indexer les colonnes souvent modifiées et baisser le `fillfactor` pour que les nouvelles versions tiennent dans la même page, ce qui permet aux mises à jour d'éviter les changements d'index.

<!-- takeaways -->

- Le MVCC garde des versions pour que les lecteurs ne bloquent pas les écrivains.
- Les tuples morts exigent vacuum.
- Les HOT updates évitent les changements d'index.

<!-- unit: Isolation et anomalies -->

<!-- goals -->

- Comparer les niveaux d'isolation de PostgreSQL et les anomalies qu'ils évitent.
- Éviter les mises à jour perdues par verrouillage ou contrôle optimiste.

<!-- concept -->

L'isolation décide de ce qu'une transaction voit des autres transactions simultanées. Read Committed, le niveau par défaut, donne à chaque instruction un snapshot neuf. Repeatable Read garde un snapshot pour toute la transaction. Serializable fait se comporter les transactions concurrentes comme si elles s'exécutaient l'une après l'autre, en annulant celles qui ne le peuvent pas.
Le bug classique au niveau par défaut est la mise à jour perdue : deux sessions lisent, modifient et écrivent la même valeur. Mises à jour atomiques, verrous de ligne ou contrôles de version l'empêchent.

<!-- example -->

```sql
-- optimistic locking: fail if someone else changed the row
UPDATE product SET price = 19.90, version = version + 1
WHERE product_id = 7 AND version = 12;
-- 0 rows updated → reload and retry
```

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

<!-- challenge -->

Deux agents du support modifient en même temps la même note client, et une modification disparaît. Quelle approche choisissez-vous pour une application web ?

<!-- solution -->

Le verrouillage optimiste : garder une colonne `version`, mettre à jour avec `WHERE version = :read_version` et afficher un message de conflit si aucune ligne n'a été modifiée, plutôt que de tenir des verrous pendant que l'utilisateur réfléchit.

<!-- takeaways -->

- Read Committed par défaut ; Serializable pour une justesse stricte.
- Les mises à jour perdues viennent du lire-modifier-écrire.
- Utilisez mises à jour atomiques, verrous de ligne ou contrôles de version.

<!-- unit: Verrous -->

<!-- goals -->

- Utiliser verrous de ligne, SKIP LOCKED et advisory locks.
- Comprendre les interblocages et les conflits de verrous du DDL.

<!-- concept -->

La plupart de la concurrence dans PostgreSQL se passe de verrous explicites, mais certains motifs en ont besoin. Verrouiller des lignes sélectionnées les réserve jusqu'au commit ; ignorer les lignes déjà verrouillées permet à de nombreux workers de tirer des tâches d'une même table de file ; les advisory locks coordonnent des tâches applicatives.
Les verrous apportent deux risques : les interblocages, quand des transactions s'attendent mutuellement, et le DDL qui prend des verrous exclusifs et met toutes les autres requêtes en file derrière lui.

<!-- example -->

```sql
-- job queue worker
BEGIN;
SELECT job_id, payload FROM job
WHERE status = 'ready'
ORDER BY created_at
LIMIT 1
FOR UPDATE SKIP LOCKED;
-- process, then
UPDATE job SET status = 'done' WHERE job_id = :id;
COMMIT;
```

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

<!-- challenge -->

Une migration lance `ALTER TABLE orders ADD COLUMN ...` et toute l'application se fige, alors que le changement lui-même est instantané. Pourquoi ?

<!-- solution -->

L'`ALTER` attend un verrou `ACCESS EXCLUSIVE` derrière une requête longue, et chaque nouvelle requête fait la queue derrière l'`ALTER`. Définir `lock_timeout` dans les migrations et relancer, et éviter de les exécuter pendant de longues transactions.

<!-- takeaways -->

- `FOR UPDATE SKIP LOCKED` sert à construire des files de tâches.
- PostgreSQL détecte et casse les interblocages.
- Un DDL en attente de verrou bloque tout ; utilisez `lock_timeout`.

<!-- unit: Vacuum et maintenance -->

<!-- goals -->

- Expliquer VACUUM, VACUUM FULL, autovacuum et ANALYZE.
- Éviter le bloat dû aux longues transactions et le wraparound des ID de transaction.

<!-- concept -->

Les restes du MVCC doivent être nettoyés. Vacuum rend réutilisable l'espace des tuples morts, met à jour la visibility map et gèle les anciennes lignes ; autovacuum le fait automatiquement au fil des changements, en plus de collecter les statistiques. Vacuum full réécrit la table pour la réduire, sous verrou exclusif.
Deux choses mettent vacuum en échec : les longues transactions, dont les vieux snapshots gardent les tuples morts en vie, et les tables négligées qui approchent du wraparound des ID de transaction, ce qui force un vacuum d'urgence.

<!-- example -->

```sql
SELECT relname, n_dead_tup, last_autovacuum, last_autoanalyze
FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 10;
ALTER TABLE events SET (autovacuum_vacuum_scale_factor = 0.02);   -- vacuum big tables more often
SELECT datname, age(datfrozenxid) FROM pg_database ORDER BY 2 DESC;
```

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

<!-- challenge -->

Une grosse table gonfle alors qu'autovacuum tourne. `pg_stat_activity` montre une session « idle in transaction » depuis deux jours. Quel est le lien ?

<!-- solution -->

La transaction ouverte détient un vieux snapshot : vacuum ne peut pas supprimer les tuples morts plus récents. Terminer la session, définir `idle_in_transaction_session_timeout` et corriger l'application.

<!-- takeaways -->

- Vacuum récupère l'espace ; vacuum full réduit sous verrou.
- Réglez autovacuum table par table pour les tables actives.
- Les longues transactions bloquent le nettoyage et exposent au wraparound.

### Performances et planification des requêtes

<!-- unit: Lire les plans d'exécution -->

<!-- goals -->

- Lire la sortie d'EXPLAIN et d'EXPLAIN ANALYZE.
- Reconnaître types de parcours, algorithmes de jointure et effet de LIMIT.

<!-- concept -->

Le planificateur transforme chaque requête en arbre d'opérations et choisit le moins coûteux selon ses estimations. `EXPLAIN` montre cet arbre ; `EXPLAIN ANALYZE` l'exécute et ajoute lignes et temps réels. Comparer lignes estimées et réelles est l'habitude la plus utile : de grands écarts signalent de mauvaises statistiques et, presque toujours, de mauvais plans.
Les types de nœuds racontent l'histoire : comment les tables sont lues, comment elles sont jointes, et si un `LIMIT` permet d'arrêter tôt grâce à un index adapté.

<!-- example -->

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT o.* FROM orders o JOIN customer c USING (customer_id)
WHERE c.country_code = 'FR' AND o.ordered_at >= '2026-10-01';
-- look for: rows=estimated vs actual, Seq Scan on big tables, Sort spilling, loops
```

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

<!-- challenge -->

Un plan estime 10 lignes pour un filtre mais en obtient 2 millions, et choisit un nested loop qui dure des minutes. Que faites-vous ?

<!-- solution -->

Corriger l'estimation : lancer `ANALYZE`, augmenter les statistiques des colonnes déséquilibrées ou ajouter des statistiques étendues pour les colonnes corrélées, pour que le planificateur choisisse un hash join. Revérifier ensuite le plan.

<!-- takeaways -->

- `EXPLAIN ANALYZE` montre lignes et temps réels.
- Les écarts d'estimation signalent un problème de statistiques.
- Les jointures sont nested loop, hash ou merge.

<!-- unit: Statistiques et estimations -->

<!-- goals -->

- Garder justes les statistiques du planificateur, y compris étendues.
- Diagnostiquer les requêtes devenues soudain lentes.

<!-- concept -->

Le planificateur ne vaut que ce qu'il sait. Les statistiques échantillonnent les valeurs de chaque colonne ; périmées, trop grossières pour des données déséquilibrées ou aveugles aux corrélations entre colonnes, elles faussent les estimations, et les plans suivent. Envelopper une colonne indexée dans une fonction la cache aussi à l'index et aux statistiques.
Quand une requête rapide devient lente, la cause est généralement l'une de celles-ci : un plan changé, des statistiques périmées, plus de données, du bloat ou une nouvelle contention.

<!-- example -->

```sql
-- correlated columns: city implies country
CREATE STATISTICS addr_stats (dependencies) ON country_code, city FROM address;
ALTER TABLE orders ALTER COLUMN status SET STATISTICS 1000;
ANALYZE address; ANALYZE orders;
-- sargable rewrite:
-- WHERE date(created_at) = '2026-10-15'  →  WHERE created_at >= '2026-10-15' AND created_at < '2026-10-16'
```

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

<!-- challenge -->

Une requête qui filtre `WHERE country_code = 'FR' AND city = 'Paris'` estime 50 lignes mais en renvoie 400 000. Pourquoi, et comment corriger ?

<!-- solution -->

Le planificateur multiplie les deux sélectivités comme si elles étaient indépendantes, alors que la ville implique le pays. Créer des statistiques étendues (dependencies) sur les deux colonnes et analyser.

<!-- takeaways -->

- Les statistiques pilotent les estimations ; gardez-les fraîches.
- Les statistiques étendues capturent les corrélations entre colonnes.
- Gardez des filtres sargables : pas de fonction sur une colonne indexée.

<!-- unit: Mémoire, parallélisme et JIT -->

<!-- goals -->

- Régler work_mem et les principaux paramètres mémoire.
- Comprendre les requêtes parallèles et la compilation JIT.

<!-- concept -->

Les paramètres mémoire décident de la part du travail qui reste en RAM. `shared_buffers` est le cache propre de PostgreSQL ; `work_mem` s'applique par opération, si bien qu'une requête complexe avec de nombreux tris sur de nombreuses connexions peut le multiplier. Trop bas, les tris débordent sur disque ; trop haut, le serveur manque de mémoire.
Pour les grosses requêtes analytiques, des workers parallèles se partagent parcours et jointures, et le JIT compile les expressions en code machine, ce qui aide les requêtes longues et pénalise les courtes.

<!-- example -->

```text
shared_buffers = 16GB            # ~25% of 64 GB RAM
effective_cache_size = 48GB      # planner hint: OS cache + shared_buffers
work_mem = 32MB                  # per sort/hash node, per connection
maintenance_work_mem = 2GB       # VACUUM, CREATE INDEX
max_parallel_workers_per_gather = 4
```

#### Pourquoi une fonction appliquée à une colonne indexée peut-elle empêcher l'utilisation de l'index ?

L'index stocke les valeurs brutes de la colonne : `WHERE date(created_at) = '2026-10-15'` ne peut donc pas utiliser un index sur `created_at`. Réécrivez-le en intervalle (`created_at >= '2026-10-15' AND created_at < '2026-10-16'`) ou créez un index d'expression.

#### Que sont les statistiques étendues ?

`CREATE STATISTICS` permet au planificateur de connaître les corrélations entre colonnes (dépendances, nombres de valeurs distinctes, combinaisons de valeurs les plus fréquentes), ce qui améliore les estimations des filtres sur plusieurs colonnes corrélées, comme la ville et le code postal.

#### Que contrôle `default_statistics_target` ?

Le nombre de valeurs d'échantillon et de tranches d'histogramme qu'`ANALYZE` conserve par colonne. L'augmenter pour les colonnes à distribution déséquilibrée améliore les estimations, au prix d'un temps de planification plus long.

#### Comment charger rapidement de gros volumes de données ?

Utiliser `COPY` plutôt que des insertions ligne à ligne, charger dans une seule transaction, créer index et clés étrangères après le chargement, envisager des tables de staging unlogged, augmenter `maintenance_work_mem` pour la création d'index, et lancer `ANALYZE` ensuite.

<!-- challenge -->

`EXPLAIN ANALYZE` affiche « Sort Method: external merge Disk: 2GB » pour un rapport nocturne. Que changez-vous ?

<!-- solution -->

Augmenter `work_mem` pour cette session ou ce rôle (`SET work_mem = '512MB'` avant le rapport), pas globalement, pour que le tri tienne en mémoire sans risquer la consommation de toutes les connexions.

<!-- takeaways -->

- `shared_buffers` met en cache ; `work_mem` s'applique par opération.
- Augmentez `work_mem` par session pour les gros tris.
- Requêtes parallèles et JIT aident les longues requêtes analytiques.

<!-- unit: Trouver et arrêter les requêtes lentes -->

<!-- goals -->

- Trouver les requêtes coûteuses et en cours avec pg_stat_statements et pg_stat_activity.
- Arrêter les requêtes incontrôlées et détecter le bloat des tables.

<!-- concept -->

Deux vues répondent à la plupart des questions de performance. `pg_stat_statements` agrège l'historique par forme de requête et montre lesquelles coûtent le plus de temps au total. `pg_stat_activity` montre ce qui tourne en ce moment, depuis combien de temps et ce que cela attend.
Quand quelque chose bloque, on peut annuler la requête ou terminer la session. Le bloat, l'espace occupé par les tuples morts, est le problème à combustion lente derrière des parcours de plus en plus lents.

<!-- example -->

```sql
SELECT pid, now() - query_start AS duration, state, wait_event_type, left(query, 80)
FROM pg_stat_activity
WHERE state <> 'idle' ORDER BY duration DESC;
SELECT pg_cancel_backend(12345);     -- cancel the query
SELECT pg_terminate_backend(12345);  -- close the connection
```

#### Qu'est-ce que la commande `COPY` ?

Le moyen le plus rapide de charger ou d'exporter en masse des données entre des tables et des fichiers ou des flux : `COPY company FROM '/data/company.csv' WITH (FORMAT csv, HEADER)`. Depuis un client, utilisez le `\copy` de psql ou la prise en charge de COPY du pilote. PostgreSQL 17 peut ignorer les lignes mal formées avec `ON_ERROR ignore`.

#### Qu'est-ce que le pooling de connexions, et pourquoi utiliser PgBouncer ?

Réutiliser un petit nombre de connexions à la base pour de nombreux clients. PgBouncer se place entre les applications et PostgreSQL, en mode session, transaction ou instruction, et réduit le coût de chaque connexion.

#### Qu'est-ce que la requête parallèle ?

PostgreSQL peut répartir les parcours séquentiels, les jointures et les agrégations sur plusieurs processus workers, selon `max_parallel_workers_per_gather` et la taille de la table.

#### Qu'est-ce que la compilation JIT dans PostgreSQL ?

La compilation à la volée (avec LLVM) des expressions des longues requêtes analytiques. Elle accélère les calculs lourds mais ajoute un surcoût aux requêtes courtes. Elle est contrôlée par `jit` et des seuils de coût.

<!-- challenge -->

La base est lente, mais aucune requête ne semble durer longtemps. Où cherchez-vous la cause ?

<!-- solution -->

Dans `pg_stat_statements` trié par temps d'exécution total : souvent, une requête rapide appelée des millions de fois domine la charge. L'optimiser, la mettre en cache ou réduire la fréquence de ses appels.

<!-- takeaways -->

- `pg_stat_statements` classe les requêtes par coût total.
- `pg_stat_activity` montre ce qui tourne maintenant.
- Annulez d'abord les requêtes ; terminez les sessions si besoin.

<!-- unit: Connexions et chargement en masse -->

<!-- goals -->

- Mutualiser les connexions avec PgBouncer.
- Charger rapidement de gros volumes avec COPY.

<!-- concept -->

Deux problèmes de performance courants se situent hors des plans de requête. Trop de connexions gaspillent mémoire et CPU en gestion de processus : un pooler comme PgBouncer laisse des milliers de clients partager quelques dizaines de connexions serveur.
Charger ligne par ligne gaspille allers-retours et surcoût par instruction. `COPY` transmet les données en bloc, et charger avant de créer les index, dans une seule transaction, est encore plus rapide.

<!-- example -->

```bash
psql -c "\copy staging.orders (order_id, customer_id, amount, ordered_at) FROM 'orders.csv' WITH (FORMAT csv, HEADER true)"
```
```ini
; pgbouncer.ini
pool_mode = transaction
default_pool_size = 40
max_client_conn = 2000
```

#### Comment `LIMIT` interagit-il avec `ORDER BY` et les index ?

Avec un index correspondant à l'`ORDER BY`, PostgreSQL ne lit que les premières lignes nécessaires. Sans index, il doit tout trier (par un heapsort top-N) avant d'appliquer la limite.

#### Qu'est-ce que le gonflement (bloat) des tables, et comment le détecter ?

De l'espace gaspillé par des tuples morts que le vacuum n'a pas récupérés ou que le système d'exploitation n'a pas repris. On le détecte avec `pgstattuple`, des requêtes d'estimation du gonflement, ou des tables qui grossissent plus vite que leur nombre de lignes.

#### Que vérifier en premier quand une requête devient soudain lente ?

Son plan (`EXPLAIN ANALYZE`) comparé à l'ancien, la fraîcheur des statistiques (dernier analyze), l'évolution des volumes, les verrous et attentes dans `pg_stat_activity`, le gonflement, et si des paramètres ou un nouvel index ont changé le plan.

<!-- challenge -->

Un script Python insère 10 millions de lignes avec un `INSERT` par ligne et prend 3 heures. Que changez-vous ?

<!-- solution -->

Utiliser `COPY` (par exemple `cursor.copy_expert` ou le `copy` de psycopg) vers une table de staging, dans une transaction, puis faire un upsert ensembliste vers la cible. Comptez quelques minutes au lieu de plusieurs heures.

<!-- takeaways -->

- Mutualisez les connexions ; n'en ouvrez pas des milliers.
- `COPY` est la voie rapide pour les chargements en masse.
- Chargez d'abord, indexez ensuite, en une transaction.

<!-- stage: Conception et exploitation -->

### Modélisation des données, normalisation et OLAP

<!-- unit: Normalisation -->

<!-- goals -->

- Expliquer 1NF, 2NF, 3NF et BCNF.
- Décider quand la dénormalisation se justifie, OLTP contre OLAP.

<!-- concept -->

La normalisation stocke chaque fait une fois pour que les mises à jour ne laissent pas de contradictions : pas de groupes répétés, pas d'attributs dépendant d'une partie de la clé, pas d'attributs dépendant d'autres attributs non clés. C'est la bonne forme pour les systèmes transactionnels, où la justesse de nombreuses petites écritures prime.
L'analytique inverse les priorités : les lectures dominent, et une redondance délibérée, comme des tables pré-jointes ou pré-agrégées, rend les requêtes plus simples et plus rapides.

<!-- example -->

```text
Not 3NF: orders(order_id, customer_id, customer_city, amount)   ← city depends on customer
3NF:     orders(order_id, customer_id, amount)
         customer(customer_id, city)
```

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

<!-- challenge -->

Une table stocke la ville du client sur chaque commande, et après un déménagement, anciennes et nouvelles commandes affichent des villes différentes. Est-ce un bug ?

<!-- solution -->

Dans un modèle OLTP, oui : la ville dépend du client, elle va donc dans la table des clients (3NF). Dans un modèle analytique, stocker la ville au moment de la commande peut être un historique voulu, mais cela doit alors être explicite.

<!-- takeaways -->

- Les formes normales éliminent redondance et anomalies de mise à jour.
- L'OLTP privilégie la normalisation ; l'OLAP tolère la redondance.
- Dénormalisez délibérément, pour les lectures.

<!-- unit: Bases dimensionnelles -->

<!-- goals -->

- Décrire les opérations OLAP et les schémas en étoile et en flocon.
- Déclarer le grain et le type d'une table de faits.

<!-- concept -->

Les modèles analytiques s'organisent autour des questions : les faits portent les mesures, les dimensions le contexte selon lequel on découpe. Les opérations OLAP, forer, agréger, découper et pivoter, sont des façons de parcourir cette structure.
Une étoile garde les dimensions plates autour du fait, un flocon les normalise. La décision la plus importante est le grain, ce que signifie une ligne de fait, qui décide ensuite du type de fait : événements, snapshots périodiques ou processus cumulatifs.

<!-- example -->

```text
fct_sales (grain: one order line)
  date_key, customer_key, product_key, store_key, quantity, net_amount
dim_date, dim_customer, dim_product, dim_store  (star)
```

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

<!-- challenge -->

Une équipe a besoin des soldes de comptes en fin de mois. Doit-elle sommer les faits de transactions à la volée ou stocker autre chose ?

<!-- solution -->

Stocker un fait de periodic snapshot (une ligne par compte et par mois avec le solde). Les soldes sont semi-additifs et coûteux à reconstruire à partir de toutes les transactions historiques.

<!-- takeaways -->

- Les faits mesurent ; les dimensions décrivent.
- L'étoile est plus simple que le flocon.
- Le grain décide du type de fait.

<!-- unit: Clés et dimensions -->

<!-- goals -->

- Utiliser clés de substitution et clés naturelles dans un entrepôt.
- Construire des dimensions junk, dégénérées, conformes et date.

<!-- concept -->

Les entrepôts émettent leurs propres clés de substitution pour les lignes de dimension et gardent les clés naturelles des sources comme attributs. Cela isole le modèle des changements des sources et permet à une entité d'avoir des versions historiques.
Quelques motifs de dimension reviennent : junk dimensions pour les indicateurs épars, dimensions dégénérées pour les identifiants gardés dans le fait, dimensions conformes partagées entre marts, et une dimension date qui porte une seule fois la logique calendaire.

<!-- example -->

```sql
INSERT INTO dim_date (date_key, day, month, quarter, is_weekend)
SELECT to_char(d, 'YYYYMMDD')::int, d::date, extract(month FROM d), extract(quarter FROM d),
       extract(isodow FROM d) IN (6, 7)
FROM generate_series('2020-01-01'::date, '2030-12-31', interval '1 day') AS d;
```

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

<!-- challenge -->

Les rapports regroupent par trimestre avec `extract(quarter ...)` partout, mais l'exercice fiscal de l'entreprise commence en avril. Comment corriger une fois pour toutes ?

<!-- solution -->

Ajouter des attributs fiscaux (année fiscale, trimestre fiscal) à la dimension date, calculés une fois, et faire joindre les rapports à celle-ci au lieu de calculer eux-mêmes les trimestres.

<!-- takeaways -->

- Les clés de substitution isolent l'entrepôt des sources.
- Dimensions junk, dégénérées et conformes répondent à des besoins récurrents.
- Une dimension date centralise la logique calendaire.

<!-- unit: Historique et architectures -->

<!-- goals -->

- Implémenter des dimensions à évolution lente dans PostgreSQL.
- Situer PostgreSQL face au Data Vault, au médaillon et aux moteurs analytiques.

<!-- concept -->

Les dimensions changent, et les dimensions à évolution lente de type 2 gardent l'historique en clôturant la version courante et en insérant une nouvelle, idéalement dans une seule transaction pour que les lecteurs ne voient jamais de trou.
PostgreSQL convient bien comme petit entrepôt ou couche de restitution, mais il n'est pas colonnaire : avec des téraoctets de parcours, des entrepôts dédiés ou des lakehouses conviennent mieux. Des méthodologies comme le Data Vault et les couches médaillon s'appliquent dans les deux cas.

<!-- example -->

```sql
BEGIN;
UPDATE dim_customer SET valid_to = now(), is_current = false
WHERE customer_id = 552 AND is_current;
INSERT INTO dim_customer (customer_id, segment, valid_from, valid_to, is_current)
VALUES (552, 'Mid', now(), 'infinity', true);
COMMIT;
```

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

<!-- challenge -->

Une base de reporting PostgreSQL contient désormais 6 To, et les tableaux de bord qui parcourent des mois de données prennent des minutes. Que suggérez-vous ?

<!-- solution -->

À court terme, partitionner et pré-agréger, mais prévoir de déplacer l'analytique à gros parcours vers un entrepôt colonnaire ou un lakehouse, en gardant PostgreSQL pour les charges opérationnelles et les petites restitutions.

<!-- takeaways -->

- Le SCD2 clôt et insère les versions dans une transaction.
- PostgreSQL convient aux petits entrepôts et couches de restitution.
- Les gros parcours relèvent des moteurs colonnaires.

### Administration, sécurité, sauvegarde et réplication

<!-- unit: Rôles et accès -->

<!-- goals -->

- Gérer rôles, accès en lecture seule et sécurité au niveau ligne.
- Configurer l'authentification et prévenir l'injection SQL.

<!-- concept -->

Dans PostgreSQL, utilisateurs et groupes sont tous des rôles, et les privilèges passent par l'appartenance aux rôles. Lire un schéma exige usage sur le schéma, select sur les tables et des privilèges par défaut pour les tables créées plus tard. La sécurité au niveau ligne restreint encore l'accès, ligne par ligne.
Qui peut se connecter est décidé par des règles par hôte et un hachage robuste des mots de passe. Dans les applications, les requêtes paramétrées empêchent les saisies utilisateur de devenir du SQL.

<!-- example -->

```sql
CREATE ROLE reporting NOLOGIN;
GRANT USAGE ON SCHEMA analytics TO reporting;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO reporting;
ALTER DEFAULT PRIVILEGES IN SCHEMA analytics GRANT SELECT ON TABLES TO reporting;
CREATE ROLE ana LOGIN PASSWORD '...' IN ROLE reporting;
```

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

<!-- challenge -->

Un rôle en lecture seule fonctionne pour les tables existantes, mais les analystes perdent l'accès à chaque nouvelle table. Que manque-t-il ?

<!-- solution -->

Des privilèges par défaut : `ALTER DEFAULT PRIVILEGES ... GRANT SELECT ON TABLES TO reporting` pour le rôle qui crée les tables, afin que les futures tables soient accordées automatiquement.

<!-- takeaways -->

- Les rôles sont utilisateurs et groupes ; accordez par appartenance.
- Les privilèges par défaut couvrent les futures tables.
- La RLS restreint les lignes ; les paramètres préviennent l'injection.

<!-- unit: Sauvegardes et restauration -->

<!-- goals -->

- Comparer sauvegardes logiques et physiques.
- Sauvegarder avec pg_dump et restaurer à un instant donné.

<!-- concept -->

Il existe deux sortes de sauvegardes. Les logiques exportent objets et données en SQL ou en archives : portables entre versions, sélectives, mais lentes pour les grosses bases. Les physiques copient les fichiers de données et, avec le WAL archivé, permettent de rejouer les changements jusqu'à n'importe quel instant.
Cette seconde capacité, la restauration à un instant donné, est ce qui vous sauve d'erreurs comme une mauvaise suppression à 10:42 : restaurer la sauvegarde de base et arrêter le rejeu à 10:41.

<!-- example -->

```bash
pg_dump -Fc -d shop -f shop.dump
pg_restore -d shop_restore -j 4 shop.dump
# PITR: restore base backup, then in postgresql.conf
#   restore_command = 'cp /archive/%f %p'
#   recovery_target_time = '2026-10-17 10:41:00+02'
```

#### Quelle est la différence entre sauvegardes logiques et physiques ?

Les sauvegardes logiques (`pg_dump`, `pg_dumpall`) exportent des fichiers SQL ou d'archive contenant les objets et les données. Elles sont portables entre versions et restaurables de façon sélective, mais lentes pour les grosses bases. Les sauvegardes physiques (`pg_basebackup`, pgBackRest) copient les fichiers de données et le WAL. Elles sont rapides pour les grosses bases et permettent la restauration à un instant donné.

#### Comment sauvegarder et restaurer une seule base avec pg_dump ?

```bash
pg_dump -Fc -d mydb -f mydb.dump          # format custom, compressé
pg_restore -d newdb -j 4 mydb.dump        # restauration en parallèle
```

#### Qu'est-ce que la restauration à un instant donné (PITR) ?

Restaurer une sauvegarde de base puis rejouer le WAL archivé jusqu'à un instant choisi, par exemple juste avant un `DELETE` accidentel.

<!-- challenge -->

Une base de 4 To est sauvegardée chaque nuit avec `pg_dump`, qui prend 9 heures, et la restauration serait plus longue encore. Que changez-vous ?

<!-- solution -->

Passer à des sauvegardes physiques (pgBackRest ou les snapshots du service managé) avec archivage continu du WAL, pour des restaurations rapides et à un instant donné ; garder `pg_dump` pour les exports sélectifs.

<!-- takeaways -->

- Les sauvegardes logiques sont portables ; les physiques, rapides.
- L'archivage du WAL permet la restauration à un instant donné.
- Testez les restaurations, pas seulement les sauvegardes.

<!-- unit: Réplication et CDC -->

<!-- goals -->

- Comparer réplication streaming et logique, synchrone et asynchrone.
- Utiliser CDC et replication slots en sécurité, et bâtir la haute disponibilité.

<!-- concept -->

La réplication streaming envoie le WAL à des standbys qui le rejouent, gardant des copies exactes pour le basculement et la montée en charge des lectures. Les réplicas asynchrones peuvent avoir du retard ; les synchrones font attendre la confirmation aux commits, échangeant latence contre absence de perte.
La réplication logique fonctionne par table et entre versions, et les outils de CDC s'appuient sur le même décodage pour envoyer les changements vers Kafka ou un lac. Les replication slots conservent le WAL jusqu'à sa lecture, ce qui remplit les disques si un consommateur disparaît. La HA ajoute un gestionnaire de basculement.

<!-- example -->

```sql
-- publisher
CREATE PUBLICATION orders_pub FOR TABLE orders, order_line;
-- subscriber
CREATE SUBSCRIPTION orders_sub CONNECTION 'host=primary dbname=shop user=repl' PUBLICATION orders_pub;
-- watch slots
SELECT slot_name, active, pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS retained
FROM pg_replication_slots;
```

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

<!-- challenge -->

Après un basculement vers un standby asynchrone, les dernières secondes de commandes manquent. Comment l'éviter, et à quel coût ?

<!-- solution -->

La réplication synchrone vers au moins un standby (`synchronous_standby_names`), pour que les commits attendent la confirmation du standby. Le coût : une latence de commit plus élevée et une dépendance à la disponibilité du standby.

<!-- takeaways -->

- Le streaming copie tout ; la réplication logique copie des tables.
- La réplication synchrone évite la perte au prix de la latence.
- Surveillez les slots ; un slot inactif retient le WAL.

<!-- unit: Exploiter un serveur -->

<!-- goals -->

- Mettre à niveau les versions majeures et superviser un serveur PostgreSQL.
- Utiliser le taux de cache, statement_timeout et les services managés.

<!-- concept -->

Exploiter PostgreSQL, c'est surveiller quelques signaux et planifier quelques événements. Signaux : connexions, débit de transactions, taux de succès du cache, requêtes lentes, verrous, retard de réplication, bloat et âge avant wraparound. Événements : les mises à niveau majeures, qui exigent des tests et une méthode adaptée à la taille et à l'interruption tolérée.
Des garde-fous comme les statement timeouts arrêtent les requêtes incontrôlées par rôle. Les services managés reprennent une grande part de la routine, mais l'optimisation et la conception restent à vous.

<!-- example -->

```sql
SELECT round(100.0 * sum(blks_hit) / nullif(sum(blks_hit) + sum(blks_read), 0), 2) AS cache_hit_pct
FROM pg_stat_database;
ALTER ROLE reporting SET statement_timeout = '5min';
```

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

<!-- challenge -->

Les requêtes ad hoc des analystes tournent parfois des heures et ralentissent l'application. Quel garde-fou ajoutez-vous sans toucher à l'application ?

<!-- solution -->

Définir `statement_timeout` sur le rôle des analystes (par exemple 5 minutes), pas globalement, et les orienter vers un réplica en lecture s'ils ont besoin de requêtes plus longues.

<!-- takeaways -->

- Surveillez connexions, cache, requêtes lentes, verrous et retard.
- Planifiez les mises à niveau majeures avec des tests.
- Définissez les timeouts par rôle.

### Fonctionnalités avancées

<!-- unit: JSON dans PostgreSQL -->

<!-- goals -->

- Choisir entre json et jsonb et interroger des documents.
- Décider quand stocker du JSONB plutôt que des colonnes.

<!-- concept -->

PostgreSQL stocke nativement des documents. `jsonb` analyse une fois vers une forme binaire indexable et efficace à interroger ; `json` garde le texte exact. Les opérateurs extraient des valeurs, testent l'inclusion et suivent des chemins, et des fonctions ensemblistes transforment les tableaux en lignes pour les jointures.
Le JSONB est idéal pour des attributs épars ou variables et des payloads bruts. Les champs sur lesquels chaque requête filtre, joint ou agrège méritent généralement de vraies colonnes, avec types et contraintes.

<!-- example -->

```sql
SELECT e.event_id,
       e.payload->>'type'                 AS type,
       (item->>'qty')::int                AS qty
FROM events e,
     jsonb_array_elements(e.payload->'items') AS item
WHERE e.payload @> '{"channel": "web"}';
```

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

<!-- challenge -->

Chaque rapport filtre et agrège sur `payload->>'country'`, stocké dans une colonne JSONB, et les requêtes sont lentes. Que changez-vous ?

<!-- solution -->

Promouvoir `country` en vraie colonne (générée depuis le JSON ou remplie à l'écriture) avec un index, puisque chaque requête l'utilise ; garder le reste en JSONB.

<!-- takeaways -->

- Utilisez `jsonb` pour l'indexation et les requêtes rapides.
- Les opérateurs extraient, testent l'inclusion et suivent des chemins.
- Promouvez en colonnes les champs très utilisés.

<!-- unit: Code côté serveur -->

<!-- goals -->

- Écrire fonctions, procédures et triggers en PL/pgSQL.
- Choisir la volatilité des fonctions et utiliser LISTEN/NOTIFY.

<!-- concept -->

Certaines logiques ont leur place à côté des données : tenir `updated_at` à jour, imposer des règles complexes, prévenir des écouteurs de changements. Les fonctions et triggers PL/pgSQL s'en chargent. Les fonctions renvoient des valeurs et s'exécutent dans la transaction de l'appelant ; les procédures peuvent gérer elles-mêmes les transactions.
Les étiquettes de volatilité disent au planificateur ce qu'une fonction peut faire, ce qui influe sur le cache et sur la possibilité d'appuyer un index. LISTEN/NOTIFY offre une messagerie légère entre sessions.

<!-- example -->

```sql
CREATE FUNCTION touch_updated_at() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at := now();
  RETURN NEW;
END $$;
CREATE TRIGGER orders_touch BEFORE UPDATE ON orders
FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
```

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

<!-- challenge -->

Un index sur l'expression `my_normalize(name)` échoue avec « functions in index expression must be marked IMMUTABLE ». Qu'est-ce que cela signifie ?

<!-- solution -->

Les valeurs d'index ne doivent jamais changer pour une même entrée : la fonction doit être déclarée `IMMUTABLE`. Ne la marquer ainsi que si elle l'est vraiment (aucune dépendance à des réglages, à l'heure ou à des tables) ; sinon, utiliser une colonne générée.

<!-- takeaways -->

- Les fonctions renvoient des valeurs ; les procédures peuvent valider.
- Les triggers exécutent une logique sur les changements de lignes.
- Les étiquettes de volatilité doivent être exactes.

<!-- unit: Partitionnement -->

<!-- goals -->

- Partitionner des tables par plage, liste ou hash.
- Décider quand le partitionnement vaut la peine.

<!-- concept -->

Le partitionnement découpe une table logique en nombreuses tables physiques selon une clé, généralement le temps. Les requêtes qui filtrent sur la clé ne touchent que les partitions utiles, et les anciennes données se suppriment instantanément en détachant une partition au lieu d'effacer des millions de lignes.
Il ajoute un surcoût de planification et des règles sur les clés et les index : il est rentable pour les grandes tables avec une clé d'élagage naturelle et un cycle de vie, pas pour toute grosse table.

<!-- example -->

```sql
CREATE TABLE events (event_id bigint, occurred_at timestamptz NOT NULL, payload jsonb)
PARTITION BY RANGE (occurred_at);
CREATE TABLE events_2026_10 PARTITION OF events
  FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
ALTER TABLE events DETACH PARTITION events_2024_10;   -- then DROP: instant retention
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

<!-- challenge -->

Une table d'événements de 2 milliards de lignes exige 13 mois de rétention, et le `DELETE` nocturne des anciennes lignes prend des heures et gonfle la table. Que proposez-vous ?

<!-- solution -->

Partitionner par mois sur `occurred_at` et supprimer (ou détacher et archiver) la plus ancienne partition chaque mois, ce qui est instantané et ne laisse aucun tuple mort.

<!-- takeaways -->

- Les partitions élaguent par clé et simplifient la rétention.
- Supprimer une partition remplace les suppressions massives.
- Ne partitionnez que les tables qui en profitent.

<!-- unit: Extensions -->

<!-- goals -->

- Utiliser des extensions courantes comme pg_stat_statements, PostGIS et pgvector.
- Interroger des données externes avec des foreign data wrappers et chercher du texte.

<!-- concept -->

Les extensions sont la façon dont PostgreSQL grandit : une commande ajoute types, fonctions, index ou intégrations. Certaines sont quasi standard, comme les statistiques de requêtes ; d'autres font de PostgreSQL une base géospatiale, un stockage vectoriel ou une passerelle vers d'autres systèmes.
La recherche plein texte est intégrée, avec racinisation selon la langue et classement, souvent suffisante pour éviter un moteur de recherche séparé pour des besoins modérés.

<!-- example -->

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE doc_chunk (id bigint PRIMARY KEY, body text, embedding vector(1536));
CREATE INDEX ON doc_chunk USING hnsw (embedding vector_cosine_ops);
SELECT id, body FROM doc_chunk ORDER BY embedding <=> :query_embedding LIMIT 5;
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

<!-- challenge -->

Une application de support doit « chercher des articles par mots, classés, en espagnol », et l'équipe prévoit d'ajouter Elasticsearch. Que peut offrir PostgreSQL d'abord ?

<!-- solution -->

La recherche plein texte intégrée : une colonne `tsvector` avec la configuration `spanish`, un index GIN et un tri par `ts_rank`. Ne passer à un moteur de recherche que si le réglage de pertinence ou l'échelle le dépassent.

<!-- takeaways -->

- Les extensions ajoutent types, index et intégrations.
- PostGIS, pgvector et les FDW couvrent les besoins spécialisés.
- La recherche plein texte intégrée couvre de nombreux besoins.

<!-- unit: Fonctions pratiques -->

<!-- goals -->

- Utiliser les fonctions de date et d'heure courantes.
- Générer rapidement des données de test en SQL.

<!-- concept -->

Un petit ensemble de fonctions couvre l'essentiel du travail sur les dates : heure courante, troncature à une période, extraction de parties, ajout d'intervalles et calcul d'âges. Les utiliser dans la base garde cohérente la logique de fuseaux et de calendrier.
La même boîte à outils génère des données de test réalistes : des séries de nombres ou de dates combinées à des fonctions aléatoires produisent des millions de lignes en quelques secondes, idéal pour tester requêtes et index.

<!-- example -->

```sql
INSERT INTO orders (customer_id, amount, ordered_at)
SELECT (random() * 10000)::int + 1,
       round((random() * 200)::numeric, 2),
       now() - random() * interval '365 days'
FROM generate_series(1, 1000000);
SELECT date_trunc('month', ordered_at) AS month, count(*) FROM orders GROUP BY 1 ORDER BY 1;
```

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

<!-- challenge -->

Vous devez vérifier si un nouvel index aide une requête sur 10 millions de commandes, mais l'environnement de dev compte 500 lignes. Comment tester de façon réaliste en quelques minutes ?

<!-- solution -->

Générer 10 millions de lignes avec `generate_series` et des valeurs aléatoires aux distributions réalistes, lancer `ANALYZE`, puis comparer `EXPLAIN ANALYZE` avec et sans l'index.

<!-- takeaways -->

- `date_trunc`, `extract`, intervalles et `age` couvrent l'essentiel des dates.
- `generate_series` et `random()` créent vite des données de test.
- Testez la performance sur des volumes réalistes.
