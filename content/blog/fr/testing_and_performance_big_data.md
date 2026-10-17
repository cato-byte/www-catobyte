## Tests et performances des pipelines big data

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Tests et performances des pipelines big data](../../images/testing_and_performance_big_data_title_img.png)

*Article technique*

## Deux questions auxquelles tout pipeline doit répondre

Un pipeline de données doit répondre à deux questions avant qu'on puisse lui faire confiance en production. Est-il **juste** : produit-il les bonnes données, à chaque fois, y compris face aux entrées étranges qu'envoient les vraies sources ? Et est-il **assez rapide et peu coûteux** : se termine-t-il dans sa fenêtre, pour un coût acceptable par le métier, à mesure que les données grossissent ?

Les équipes les traitent souvent séparément : la justesse serait l'affaire des analystes, les performances celle de l'équipe plateforme. Les deux sont liées. Optimiser un pipeline sans tests revient à parier, car chaque changement de performance (une nouvelle stratégie de jointure, un autre partitionnement, un chargement incrémental au lieu d'une reconstruction complète) est une occasion de modifier les résultats en silence. Et des tests qui ne tournent pas rapidement sur un portable ne seront jamais lancés.

Cet article présente ma façon d'aborder les deux, avec des exemples PySpark et Delta Lake. Plusieurs viennent de mon [lakehouse des registres d'entreprises européens](../projects/eu-company-registry.html), qui compte environ 200 tests et tourne de bout en bout sur un portable avant que quoi que ce soit n'atteigne Databricks.

## Partie 1 : prouver que le pipeline est juste

### Pourquoi tester du big data est différent

Tester une API web et tester un pipeline de données partagent des principes, mais les données ajoutent quatre complications :

- **L'entrée est la moitié du programme.** Un code correct peut produire des données fausses à partir d'une source qui a changé de format, décalé une colonne ou envoyé un demi-fichier. Les tests de code ne suffisent pas ; il faut aussi tester les données.
- **L'état compte.** Les pipelines écrivent des tables historisées. On ne corrige pas un bug en redéployant ; il faut aussi réparer les données qu'il a écrites.
- **L'échelle cache des problèmes.** Une jointure qui fonctionne sur 1 000 lignes peut exploser sur 50 millions à cause d'une seule clé chaude. Certaines pannes n'apparaissent qu'avec le volume.
- **Exécuter pour de vrai coûte cher.** « Déployer et voir » sur un cluster coûte de l'argent et des minutes à chaque essai ; la boucle de retour doit donc être locale.

Une bonne stratégie comporte donc plusieurs couches, chacune détectant une classe de problèmes différente.

| Couche | Ce qu'elle détecte | Où elle tourne |
|---|---|---|
| Contrôles statiques | Anti-modèles, API non prises en charge, secrets | Pre-commit et CI, quelques secondes |
| Tests unitaires | Logique erronée d'analyse, de nettoyage, de règles métier | Portable et CI, quelques secondes |
| Tests de bout en bout sur données synthétiques | Erreurs de câblage entre étapes, idempotence, historique | Portable et CI, quelques minutes |
| Contrôles de qualité des données | Données réelles fausses ou inattendues | Production, à chaque exécution |
| Non-régression et rapprochement | Changements involontaires des résultats, chargements incomplets | CI sur échantillons, production après les chargements |
| Contrôles de performance | Plans et durées qui se dégradent | CI (contrôle des plans), benchmarks périodiques |

### Concevoir pour tester

L'habitude la plus utile est de **séparer les transformations des entrées-sorties**. Une fonction qui prend un DataFrame et renvoie un DataFrame se teste avec dix lignes ; une cellule de notebook qui lit S3, transforme et écrit une table ne se teste qu'en exécutant le tout.

```python
from pyspark.sql import DataFrame, functions as F
from pyspark.sql.window import Window

def latest_per_key(df: DataFrame, key: str, order_col: str) -> DataFrame:
    """Garde la ligne la plus récente par clé."""
    w = Window.partitionBy(key).orderBy(F.col(order_col).desc())
    return df.withColumn("_rn", F.row_number().over(w)).filter("_rn = 1").drop("_rn")
```

Les points d'entrée (jobs, notebooks, handlers Lambda) restent minces : ils lisent la configuration, appellent ces fonctions et écrivent les résultats. Chemins, dates et noms de tables sont des paramètres, jamais des constantes enfouies dans le code.

### Tests unitaires avec une SparkSession locale

Une fixture de portée session fournit à tous les tests la même petite instance Spark, ce qui garde la suite rapide :

```python
import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark():
    session = (SparkSession.builder.master("local[2]")
               .config("spark.sql.shuffle.partitions", "2")
               .config("spark.sql.ansi.enabled", "true")   # même comportement qu'en production
               .getOrCreate())
    yield session
    session.stop()

def test_latest_per_key_keeps_newest(spark):
    from pyspark.testing import assertDataFrameEqual
    df = spark.createDataFrame(
        [(1, "old", "2026-10-01"), (1, "new", "2026-10-02"), (2, "only", "2026-10-01")],
        ["id", "value", "updated_at"])
    expected = spark.createDataFrame(
        [(1, "new", "2026-10-02"), (2, "only", "2026-10-01")],
        ["id", "value", "updated_at"])
    assertDataFrameEqual(latest_per_key(df, "id", "updated_at"), expected)
```

Deux détails comptent. Configurez la session locale comme la production (ici le mode ANSI, qui fait échouer les conversions invalides au lieu de renvoyer silencieusement null), sinon les tests passeront en local et échoueront sur le cluster. Et gardez peu de partitions de shuffle ; la valeur par défaut de 200 rend les petits tests lents.

Pour les fonctions au niveau colonne (analyse de dates, nettoyage de codes postaux, validation d'identifiants), j'utilise un helper qui évalue une expression de colonne sur une liste d'entrées **en un seul job Spark**, pour qu'un test de cinquante cas ne lance pas cinquante jobs :

```python
def eval_col(spark, fn, values):
    """eval_col(spark, parse_int, ["5.0", "x"]) -> [5, None]"""
    df = spark.createDataFrame([(v,) for v in values], "value string")
    return [row[0] for row in df.select(fn(F.col("value"))).collect()]

def test_parse_postcode(spark):
    assert eval_col(spark, clean_postcode, [" 75001", "75-001", "", None]) == ["75001", "75001", None, None]
```

### Tests par propriétés pour les parseurs

Les exemples écrits à la main couvrent les cas auxquels on a pensé. Le test par propriétés (avec Hypothesis) génère des centaines d'entrées et vérifie des propriétés toujours vraies : une sortie dédupliquée a des clés uniques ; un identifiant nettoyé est soit valide soit null, jamais entre les deux ; analyser puis formater une valeur redonne la même valeur. Il est particulièrement efficace pour trouver les cas limites des parseurs de texte désordonné.

### Des jeux synthétiques qui ressemblent aux vrais

Les données réelles ne peuvent pas aller dans un dépôt public, et ne devraient de toute façon pas aller en CI. La solution : **des jeux synthétiques qui reproduisent les bizarreries des vrais fichiers** — mêmes noms et ordre de colonnes, mêmes encodages et séparateurs, mêmes particularités (dates dans trois formats, identifiants avec espaces, lignes incomplètes, un tableau JSON au lieu de NDJSON). Dans le projet de registres, les jeux de test sont générés à partir de la forme des vrais fichiers avec de nouveaux identifiants qui passent toujours leurs chiffres de contrôle, ce qui exerce la logique de validation de façon réaliste.

### Tests de bout en bout : tout le pipeline sur un portable

Le test auquel je tiens le plus exécute toutes les étapes, des fichiers d'atterrissage jusqu'à la sortie publiée, sur ces jeux de test :

```python
@pytest.mark.e2e
def test_pipeline_end_to_end(spark, tmp_path):
    settings = Settings(landing_root=copy_fixtures(tmp_path), snapshot_date=date(2026, 7, 31),
                        publish_root=tmp_path / "publish")
    run_bronze(spark, settings)
    run_silver(spark, settings)
    run_gold(spark, settings)
    run_publish(spark, settings)

    silver = spark.table("silver.companies")
    assert silver.filter("is_current").groupBy("company_key").count().filter("count > 1").count() == 0
    assert (tmp_path / "publish" / "summary.json").exists()
```

Il prend quelques minutes et ne coûte rien. Il détecte les erreurs que les tests unitaires ne voient pas : une étape qui lit une colonne renommée par l'étape précédente, une table écrite dans le mauvais schéma, une condition de merge qui duplique les lignes courantes. Dans mon projet, c'est littéralement « le test qui remplace le fait de lancer sur Databricks pour voir ».

### Tester explicitement l'idempotence et l'historique

Les pipelines sont relancés en permanence : relances après échec, backfills, déclenchements doublés par accident. Un pipeline qui ajoute aveuglément dupliquera les données à chaque relance. Faites de l'idempotence un test, pas un espoir :

```python
def test_rerun_on_same_input_changes_nothing(spark, settings):
    run_silver(spark, settings)
    version_before = spark.sql("DESCRIBE HISTORY silver.companies").first()["version"]
    run_silver(spark, settings)   # mêmes fichiers en entrée
    version_after = spark.sql("DESCRIBE HISTORY silver.companies").first()["version"]
    assert version_after == version_before   # aucune nouvelle version de table n'a été écrite
```

Pour les tables historisées (SCD de type 2), testez le cycle de vie : une nouvelle entité a une ligne ouverte ; un changement clôt l'ancienne version et en ouvre une nouvelle ; une entité qui disparaît est clôturée ; une photo plus ancienne est refusée au lieu de réécrire l'historique à rebours.

### Contrôles de qualité des données en production

Les tests sur des jeux de test prouvent le code ; ils ne prouvent pas que le fichier du mois prochain sera sain. C'est le rôle des contrôles de qualité exécutés sur les données réelles à chaque exécution. Une conception simple et efficace donne à chaque règle une **sévérité** :

- **Avertissement :** la ligne est conservée, comptée et signalée.
- **Erreur :** la ligne part dans une table de quarantaine avec les règles échouées, et le traitement continue avec le reste.
- **Seuil d'arrêt :** si trop de lignes échouent à une règle, l'exécution s'arrête. Quand 1 % des identifiants échouent soudain à leur chiffre de contrôle, le problème est structurel (colonnes décalées, nouveau format), et charger le reste serait pire que s'arrêter.

Toutes les règles peuvent être évaluées en une seule passe sur les données :

```python
RULES = {
    # nom : (sévérité, condition qui doit être vraie)
    "id_present":    ("error",   F.col("company_id").isNotNull()),
    "known_country": ("error",   F.col("country_code").isin("FR", "IE", "GB", "NO", "EE", "ES")),
    "has_postcode":  ("warning", F.col("postcode").isNotNull()),
}

failures = df.select(
    F.count("*").alias("rows"),
    *[F.sum(F.when(F.coalesce(cond, F.lit(False)), 0).otherwise(1)).alias(name)
      for name, (_, cond) in RULES.items()],
).first()
```

Ajoutez aussi des contrôles de volume. Dans le pipeline de registres, une photo comptant moins de 80 % des lignes de la précédente arrête l'exécution : c'est à ça que ressemble un téléchargement tronqué, et il est bien moins coûteux de s'arrêter que de publier une carte à laquelle il manque un cinquième d'un pays.

Les contraintes au niveau des tables sont la dernière ligne de défense. Les contraintes `CHECK` de Delta Lake (statuts valides, `valid_to >= valid_from`, lignes courantes avec une date de fin ouverte) rendent impossible l'écriture d'un état invalide par une régression du code, car l'écriture elle-même échoue.

### Non-régression et rapprochement

Quand vous changez la logique, comparez les sorties. Sur les jeux de test en CI, comparez les résultats de la nouvelle version à ceux de la précédente (nombres de lignes, agrégats clés, différences ligne à ligne sur un échantillon). En production, rapprochez avec les sources après chaque chargement : lignes par photo, clés distinctes, sommes de montants. Le rapprochement transforme « je pense que le chargement est complet » en preuve.

## Partie 2 : le rendre rapide et abordable

### Mesurer avant d'optimiser

La plupart des pipelines lents le sont pour une ou deux raisons, et deviner fait perdre des jours. Regardez :

- **La Spark UI :** quel stage prend le temps, comment se répartissent les durées de ses tâches (une longue traîne signifie un déséquilibre), les volumes lus et écrits en shuffle, et le spill sur disque.
- **Le plan physique** (`df.explain(mode="formatted")`) : les filtres sont-ils poussés jusqu'à la lecture, des fichiers sont-ils écartés, quelle stratégie de jointure a été choisie, y a-t-il un `CartesianProduct` inattendu ou une évaluation Python ?
- **Le coût par exécution**, pas seulement la durée. Sur Databricks, `system.billing.usage` donne les DBU réels de chaque exécution ; dans mon projet, une petite tâche `cost_report` les enregistre après chaque exécution pour calibrer les estimations sur la réalité.

### Où part généralement le temps

D'après mon expérience, à peu près dans cet ordre :

1. **Lire trop de données.** Des lectures complètes au lieu de lectures élaguées, du CSV ou du JSON au lieu d'un format en colonnes, des milliers de petits fichiers.
2. **Les shuffles.** Des jointures et agrégations qui déplacent de gros volumes sur le réseau.
3. **Le déséquilibre (skew).** Quelques clés (souvent `null` ou une valeur par défaut) concentrent la plupart des lignes : quelques tâches tournent une heure pendant que les autres finissent en secondes.
4. **Le spill.** Des partitions trop grosses pour la mémoire de l'executor, écrites sur disque puis relues.
5. **Python au niveau ligne.** Des UDF qui sérialisent chaque ligne entre la JVM et Python.
6. **Les goulots du driver.** `collect()` ou `toPandas()` sur de gros volumes, ou des plans de requête gigantesques.

### Organisation des données : lire moins

L'octet le moins cher est celui qu'on ne lit jamais.

- Les **formats en colonnes** (Parquet, ou Delta et Iceberg par-dessus) permettent aux moteurs de ne lire que les colonnes utiles et de sauter des groupes de lignes grâce aux statistiques min/max.
- Des **tailles de fichiers** d'environ 128 Mo à 1 Go gardent faible le coût par fichier. Le streaming et les petits ajouts fréquents créent de petits fichiers ; la compaction (`OPTIMIZE`) les corrige.
- **Partitionner ou regrouper** selon les colonnes filtrées par la plupart des requêtes. Sur Delta, le liquid clustering (`CLUSTER BY`) a largement remplacé le partitionnement manuel et le Z-ordering ; ne partitionnez que les très grosses tables, sur une colonne de faible cardinalité utilisée par presque toutes les requêtes, sinon vous recréerez le problème des petits fichiers.
- **Des filtres qui élaguent.** Un filtre n'élague que s'il porte directement sur la colonne stockée. `WHERE to_date(event_ts) = '2026-10-15'` peut tout lire ; `WHERE event_date = '2026-10-15'` sur une colonne regroupée ou partitionnée, non.

### Jointures : diffuser le petit, traiter le déséquilibre

Quand un côté d'une jointure est petit (une dimension, une table de correspondance), diffusez-le pour ne pas redistribuer le gros côté :

```python
from pyspark.sql.functions import broadcast
enriched = facts.join(broadcast(dim_country), "country_code", "left")
```

L'Adaptive Query Execution (activée par défaut dans les Spark récents) convertit les jointures en broadcast quand un côté s'avère petit à l'exécution, fusionne les petites partitions de shuffle et découpe les partitions déséquilibrées. Laissez-la travailler et gardez ses réglages activés.

Pour un déséquilibre qu'AQE ne corrige pas, traitez à part les clés chaudes ou **salez-les** : répartissez une clé chaude sur plusieurs sous-clés artificielles côté gros jeu, et répliquez le petit côté en conséquence.

```python
SALTS = 16
big = big.withColumn("salt", (F.rand() * SALTS).cast("int"))
small = small.crossJoin(spark.range(SALTS).withColumnRenamed("id", "salt"))  # petit côté seulement
joined = big.join(small, ["key", "salt"])
```

Souvent, la vraie correction est en amont : une clé de jointure `null` qui aurait dû être filtrée ou rattachée à un membre « inconnu » avant la jointure.

### Des pratiques à bannir du code

Certains anti-modèles sont si fréquents et si coûteux qu'il vaut la peine de les détecter automatiquement plutôt qu'en revue. Dans le projet de registres, un petit linter fondé sur l'AST tourne en pre-commit, en CI et dans la suite de tests, et signale entre autres :

| Pratique | Pourquoi elle coûte |
|---|---|
| `collect()` / `toPandas()` sur des données non bornées | Ramène tout sur le driver |
| UDF Python | Sérialisation ligne à ligne, invisible pour l'optimiseur ; des fonctions natives existent presque toujours |
| `withColumn` dans une boucle | Le plan grossit de façon quadratique ; utilisez `withColumns` ou un seul `select` |
| `crossJoin` | Produit cartésien, presque toujours un bug |
| `repartition(1)` / `coalesce(1)` | Fait passer toutes les données par une seule tâche |
| `inferSchema` | Lecture complète supplémentaire, types instables ; déclarez les schémas |
| `cache()` / `persist()` en serverless | Non pris en charge ; écrivez plutôt une table intermédiaire |

Chaque alerte peut être neutralisée sur une ligne avec une justification écrite, ce qui garde des règles strictes sans bloquer les exceptions légitimes.

### Tester le plan, pas seulement le résultat

On ne peut pas lancer des benchmarks au volume de production à chaque pull request, mais on peut vérifier la **forme du plan de requête** sur les jeux de test, à moindre coût et de façon déterministe :

```python
import contextlib, io

def plan_of(df) -> str:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        df.explain(mode="formatted")
    return buffer.getvalue()

def test_gold_plan_is_safe(spark, silver_fixture):
    plan = plan_of(build_gold(silver_fixture))
    assert "BatchEvalPython" not in plan and "ArrowEvalPython" not in plan   # pas d'UDF Python
    assert "CartesianProduct" not in plan                                     # pas de produit cartésien accidentel
    assert len(plan.splitlines()) < 400                                       # la taille du plan reste bornée
```

Ces tests détectent une régression de performance au moment où elle est écrite, bien avant que quelqu'un remarque qu'un job prend deux fois plus de temps.

### Ne traiter que ce qui a changé

Les plus grosses économies viennent rarement du réglage d'une jointure. Elles viennent du fait de **ne pas faire le travail** :

- Charger de façon incrémentale (Auto Loader, `COPY INTO`, CDC, watermarks) au lieu de relire tous les fichiers.
- Écrire avec `MERGE` ou `replaceWhere` sur la période concernée au lieu de reconstruire des tables entières.
- Sauter les étapes dont les entrées n'ont pas changé. La première tâche du job de registres compare les derniers fichiers d'atterrissage, le référentiel géographique et les résultats de géocodage à ce qui a été traité la dernière fois ; si rien n'a changé, une tâche de condition termine immédiatement l'exécution, et si seule la France a changé, seule la France est retraitée. Un test vérifie qu'une relance sur les mêmes fichiers n'écrit aucune nouvelle version de table ni aucun fichier publié.

### Dimensionner le calcul

Adaptez le calcul à la charge : serverless ou clusters de job pour les pipelines planifiés (jamais de clusters interactifs), autoscaling dans des limites raisonnables, instances spot pour les workers batch tolérants aux pannes, arrêt automatique partout. Plus gros n'est pas toujours plus cher : si un job se parallélise bien, doubler le cluster divise la durée par deux pour le même coût. Sinon, vous payez des cœurs inactifs, et la frise des executors dans la Spark UI le montrera.

### Suivre les performances dans le temps

Les performances se dégradent progressivement à mesure que les données grossissent. Conservez un historique de la durée, de la taille d'entrée, du volume de shuffle et du coût par exécution, et alertez quand une exécution dure bien plus que sa moyenne récente. Dans les jobs Databricks, une alerte de durée sous le timeout ferme prévient avant que le job n'échoue.

## Une liste de contrôle pour chaque pipeline

**Justesse**

- Les transformations sont des fonctions pures avec des tests unitaires, exécutés sur une session locale configurée comme la production.
- Les jeux synthétiques reproduisent les bizarreries des vraies sources ; aucune donnée personnelle réelle dans le dépôt.
- Un test de bout en bout exécute tout le pipeline sur les jeux de test en quelques minutes.
- L'idempotence des relances est testée ; la logique d'historique (SCD2) est testée sur tout son cycle de vie.
- Les règles de qualité ont des sévérités, une quarantaine et des seuils d'arrêt ; les baisses de volume arrêtent l'exécution.
- Des contraintes de table imposent les invariants ; les résultats sont rapprochés des sources.

**Performances et coût**

- Formats en colonnes, tailles de fichiers saines, clustering sur les filtres courants, filtres qui élaguent.
- Petites tables diffusées, déséquilibre traité, AQE activée.
- Anti-modèles bloqués par un linter ; plans de requête vérifiés dans les tests.
- Seules les données modifiées sont traitées ; les étapes inchangées sont sautées.
- Le calcul est adapté à la charge ; le coût par exécution est mesuré et suivi.

Tests et performances sont une même discipline vue sous deux angles : savoir exactement ce que fait votre pipeline, pour pouvoir le modifier en confiance. Une suite qui tourne en quelques minutes sur un portable est ce qui rend l'optimisation sûre ; les mesures sont ce qui vous dit où elle en vaut la peine.
