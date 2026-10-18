## Fiche d'étude PySpark

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude PySpark : environ 200 questions](../../images/pyspark_study_guide_title_img.png)

Environ 200 questions sur PySpark pour les entretiens de data engineer : l'architecture de Spark, SparkSession et les RDD, les DataFrames et les fonctions de colonnes, les agrégations, les jointures, les fonctions de fenêtrage, Spark SQL, la lecture et l'écriture des données, le partitionnement et les shuffles, l'optimiseur Catalyst et AQE, l'optimisation des performances, les UDF et pandas, Structured Streaming, les tests et des exercices pratiques. Les exemples ciblent Spark 3.5 et 4.x. Ouvrez une question pour voir sa réponse, ou utilisez le filtre pour chercher dans toute la fiche.

<!-- QA -->

### Fondamentaux et architecture de Spark

#### Qu'est-ce qu'Apache Spark ?

Un moteur de traitement distribué pour les données à grande échelle. Il découpe les données en partitions et les traite en parallèle sur un cluster, en gardant les résultats intermédiaires en mémoire quand c'est possible. Il propose des API en Python (PySpark), Scala, Java, R et SQL, et des bibliothèques pour le SQL, le streaming et le machine learning.

#### Qu'est-ce que PySpark ?

L'API Python de Spark. Votre code Python construit un plan de requête ; le travail réel s'exécute dans le moteur Spark, basé sur la JVM. Seules les UDF Python et les fonctions pandas s'exécutent dans des processus worker Python, c'est pourquoi les fonctions intégrées sont plus rapides que du code Python.

#### Quels sont les concepts clés de Spark par lesquels commence tout entretien ?

- **Transformation :** une opération sur un DataFrame ou un RDD qui renvoie un nouveau DataFrame ou RDD (`filter`, `select`, `join`). Elle est paresseuse.
- **Action :** une opération qui renvoie une valeur au driver ou écrit des données (`count`, `collect`, `show`, `write`). Elle déclenche l'exécution.
- **Optimiseur Catalyst :** le composant qui analyse toutes les transformations demandées et détermine la manière la plus efficace de les exécuter ensemble.

#### Qu'est-ce que l'évaluation paresseuse (lazy evaluation) ?

Les transformations ne sont pas exécutées quand vous les appelez ; Spark les enregistre seulement dans un plan logique. Quand une action est appelée, Catalyst analyse toute la chaîne de transformations et construit un plan d'exécution optimisé. Spark peut ainsi combiner des étapes, pousser les filtres jusqu'à la source et ignorer les colonnes inutiles.

#### Que sont le driver et les executors ?

Le **driver** exécute votre programme, construit le plan, le découpe en jobs, stages et tâches, et planifie les tâches. Les **executors** sont des processus JVM sur les nœuds worker qui exécutent les tâches, conservent les données en cache et rendent compte au driver. Une application Spark a un driver et de nombreux executors.

#### Qu'est-ce qu'un gestionnaire de cluster (cluster manager) ?

Le système qui alloue les ressources (CPU, mémoire) aux executors de Spark : Spark standalone, Hadoop YARN ou Kubernetes. Le support de Mesos a été déprécié puis supprimé dans Spark 4.0. Les plateformes gérées (Databricks, EMR, Dataproc, Glue) s'en chargent pour vous.

#### Quelle est la différence entre les modes de déploiement client et cluster ?

En **mode client**, le driver s'exécute sur la machine qui a soumis l'application (pratique pour le travail interactif ; l'application s'arrête si cette machine se déconnecte). En **mode cluster**, le driver s'exécute dans le cluster, ce qui est le bon choix pour les jobs de production.

#### Que sont les jobs, les stages et les tâches ?

Chaque action crée un **job**. Le job est découpé en **stages** aux frontières de shuffle : les opérations d'un même stage peuvent s'exécuter sans déplacer de données entre executors. Chaque stage exécute une **tâche** par partition, et les tâches sont l'unité de travail envoyée aux executors.

#### Que se passe-t-il à partir du moment où une action est appelée ?

1. Catalyst transforme les transformations en plan logique, l'optimise et choisit un plan physique.
2. Le DAG scheduler parcourt le plan depuis l'action jusqu'aux sources et le découpe en stages là où un shuffle est nécessaire.
3. Chaque stage devient un ensemble de tâches, une par partition.
4. Le task scheduler envoie les tâches aux executors, de préférence à ceux qui détiennent déjà les données (localité des données).
5. Les stages s'exécutent dans l'ordre ; un stage qui dépend d'un shuffle attend que le stage précédent ait écrit ses fichiers de shuffle.

#### Qu'est-ce que le DAG ?

Le graphe orienté acyclique des opérations que Spark construit à partir de vos transformations. Le scheduler l'utilise pour déterminer les stages, les dépendances et ce qui peut s'exécuter en parallèle, ainsi que pour recalculer les partitions perdues après une panne.

#### Quelle est la différence entre transformations narrow et wide ?

Les transformations **narrow** calculent chaque partition de sortie à partir d'une seule partition d'entrée, donc aucune donnée ne circule entre executors : `filter`, `select`, `map`, `union`, `withColumn`. Les transformations **wide** ont besoin de données de nombreuses partitions, ce qui exige un shuffle : `groupBy`, `join` (sauf broadcast), `distinct`, `orderBy`, `repartition`, `reduceByKey`. Elles sont plus coûteuses, mais souvent inévitables.

#### Qu'est-ce qu'une partition ?

Un morceau des données traité par une seule tâche. Le parallélisme est égal au nombre de partitions traitées en même temps, limité par le nombre total de cœurs des executors. Trop peu de partitions gaspillent des cœurs ; trop de partitions ajoutent du coût de planification et de petits fichiers.

#### Qu'est-ce que la localité des données ?

Spark essaie d'exécuter une tâche là où se trouvent déjà ses données : dans la mémoire du même executor (`PROCESS_LOCAL`), sur le même nœud (`NODE_LOCAL`), dans le même rack, ou n'importe où. Avec le stockage objet dans le cloud, les données sont toujours distantes, donc la localité compte moins qu'avec HDFS.

#### Comment Spark assure-t-il la tolérance aux pannes ?

Grâce au lignage : Spark sait comment chaque partition a été calculée, donc si un executor tombe, il ne recalcule que les partitions perdues depuis leurs sources ou depuis les fichiers de shuffle. Les tâches en échec sont relancées (`spark.task.maxFailures`, 4 par défaut) et des stages peuvent être soumis à nouveau.

#### PySpark est-il plus rapide que Python pur ?

Cela dépend de la taille des données. PySpark est généralement plus rapide sur de gros volumes, car il répartit le travail sur de nombreux nœuds et traite les partitions en parallèle. Pour de petites données qui tiennent facilement sur une machine, Python, pandas ou Polars sont souvent plus rapides, car Spark ajoute un coût de planification, de sérialisation et de JVM.

#### Quand ne faut-il pas utiliser Spark ?

Pour de petits volumes (jusqu'à quelques gigaoctets), des recherches de faible latence sur une seule ligne, des charges transactionnelles (OLTP) ou des jobs simples qu'une base de données sait faire. Un moteur mono-nœud comme DuckDB ou Polars est souvent plus simple et plus rapide pour des données qui tiennent sur une machine.

#### Qu'est-ce que Spark Connect ?

Une architecture client-serveur introduite dans Spark 3.4. Un client léger envoie des plans de requête non résolus à un serveur Spark distant via gRPC, si bien que les applications n'ont pas besoin de JVM ni de s'exécuter sur le cluster. Il est utilisé par Databricks serverless et les clusters partagés ; certaines API de bas niveau, comme les RDD et `SparkContext`, n'y sont pas disponibles.

#### Qu'est-ce qui a changé dans Spark 4.0 et qui compte pour PySpark ?

Le mode ANSI SQL est activé par défaut (les conversions invalides et les dépassements lèvent des erreurs au lieu de renvoyer null), il existe un type `VARIANT` pour les données semi-structurées, une API Python pour les sources de données, des améliorations de Spark Connect, et le support de Mesos a été supprimé. Le code qui comptait sur des nulls silencieux lors de conversions invalides peut devoir être modifié.

#### Qu'est-ce que le moteur Tungsten ?

La couche d'exécution de Spark qui gère la mémoire hors du tas de la JVM dans un format binaire compact et génère du bytecode JVM pour des stages entiers d'une requête (génération de code whole-stage). Elle réduit le ramasse-miettes et la charge CPU, et c'est l'une des raisons pour lesquelles les DataFrames sont plus rapides que les RDD.

### SparkSession, SparkContext et configuration

#### Quelle est la différence entre SparkContext, SparkSession et SQLContext ?

Ce sont trois points d'entrée vers le moteur :

- **SparkContext :** le point d'entrée d'origine. Il se connecte au cluster et gère les opérations sur les RDD.
- **SparkSession :** le point d'entrée moderne et unifié (depuis Spark 2.0) pour les DataFrames et Spark SQL. Il contient un SparkContext, donc les opérations sur les RDD restent possibles via `spark.sparkContext`.
- **SQLContext** (et HiveContext) : des points d'entrée historiques remplacés par SparkSession.

```python
from pyspark import SparkContext

sc = SparkContext("local", "MyApp")
rdd = sc.parallelize(["A", "B", "C", "D"])
print(rdd.map(lambda c: ord(c)).collect())   # [65, 66, 67, 68]
sc.stop()
```

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("MyOtherApp").getOrCreate()
df = spark.createDataFrame(
    [("Rosa María Casas del Campo", 16, "Planeta Rica", "Colombia"),
     ("Hideo Kojima", 63, "Setagaya", "Japón")],
    ["name", "age", "city_of_birth", "country_of_birth"],
)
df.show()
spark.stop()
```

#### Comment créer un SparkContext et une SparkSession ?

Un SparkContext prend une URL de master et un nom d'application, ou un `SparkConf` pour une configuration détaillée. Une SparkSession utilise le modèle builder.

```python
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local[*]").setAppName("MiAplicacion")
sc = SparkContext(conf=conf)
print(sc.applicationId)
sc.stop()
```

```python
from pyspark.sql import SparkSession

spark = (SparkSession.builder
         .appName("ProcesadorDeDatos")
         .config("spark.executor.memory", "1g")
         .getOrCreate())
print(spark.sparkContext.applicationId)
spark.stop()
```

`local[*]` utilise tous les cœurs locaux, `local[4]` en utilise quatre ; `local[0]` n'est pas valide.

#### Comment travailler avec des RDD depuis une SparkSession ?

Via son SparkContext intégré, `spark.sparkContext`. À la fin, arrêtez la session, pas le contexte.

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("RDDSparkSession").getOrCreate()
sc = spark.sparkContext
rdd = sc.parallelize([1, 2, 3])
print(rdd.collect())
spark.stop()
```

#### SparkContext prend-il en charge les DataFrames ?

Non. Les DataFrames nécessitent une SparkSession (ou l'ancien SQLContext). Un SparkContext seul ne travaille qu'avec des RDD.

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DataFrames").getOrCreate()
df = spark.createDataFrame([("AWS Redshift", 2013), ("Apache Spark", 2009)],
                           ["product", "year_of_release"])
df.filter(df.year_of_release > 2010).show()
spark.stop()
```

#### Que fait getOrCreate() ?

Il renvoie la SparkSession active s'il en existe une, ou en crée une nouvelle. Dans les notebooks et sur Databricks, une session nommée `spark` existe déjà, donc `getOrCreate()` la renvoie et la plupart des options du builder sont ignorées.

#### Comment définir et lire la configuration ?

À la construction avec `.config(clé, valeur)`, à la soumission avec `--conf clé=valeur`, ou à l'exécution pour les options SQL avec `spark.conf.set("spark.sql.shuffle.partitions", "64")`. Lisez une valeur avec `spark.conf.get(clé)`. Les options de niveau cluster, comme la mémoire des executors, ne peuvent plus être modifiées une fois l'application démarrée.

#### Quelles sont les options les plus importantes de spark-submit ?

`--master`, `--deploy-mode`, `--executor-memory`, `--executor-cores`, `--num-executors` (ou l'allocation dynamique), `--driver-memory`, `--conf`, `--py-files` (dépendances en zip ou wheel), `--packages` (coordonnées Maven, comme des connecteurs) et `--files`.

```bash
spark-submit --master yarn --deploy-mode cluster \
  --executor-memory 8g --executor-cores 4 \
  --conf spark.sql.shuffle.partitions=400 \
  --py-files deps.zip main.py --date 2026-10-17
```

#### Comment envoyer les dépendances Python aux executors ?

Avec `--py-files` (zips, eggs ou wheels), en construisant un environnement virtuel empaqueté (venv-pack, conda-pack) passé avec `--archives`, ou en installant les bibliothèques sur le cluster (bibliothèques Databricks, bootstrap actions EMR, image Docker personnalisée sur Kubernetes). Chaque executor a besoin des mêmes versions que le driver.

#### Qu'est-ce que l'allocation dynamique (dynamic allocation) ?

Une fonctionnalité qui ajoute des executors quand des tâches attendent et supprime ceux qui sont inactifs (`spark.dynamicAllocation.enabled`). Elle nécessite un moyen de garder les fichiers de shuffle disponibles quand des executors sont supprimés : le service de shuffle externe ou le suivi du shuffle. Elle économise des ressources sur les clusters partagés.

#### Comment dimensionner les executors ?

Un point de départ courant est de 4 à 5 cœurs par executor avec assez de mémoire pour les tâches de ces cœurs (par exemple 4 cœurs avec 16 à 32 Go). Les très gros executors subissent de longues pauses de ramasse-miettes ; les très petits ne peuvent pas contenir les tables diffusées et gaspillent le surcoût par executor. Ajustez selon le spill et le temps de GC affichés dans la Spark UI.

#### Comment changer le niveau de logs ?

Avec `spark.sparkContext.setLogLevel("WARN")` à l'exécution, ou via le fichier de configuration log4j2 du cluster. Réduire le bruit rend les logs du driver plus lisibles dans les notebooks.

### RDD et sérialisation

#### Qu'est-ce qu'un RDD ?

Un Resilient Distributed Dataset : une collection d'objets immuable et partitionnée, qui peut être traitée en parallèle et reconstruite à partir de son lignage. C'est l'API de bas niveau de Spark ; les DataFrames sont construits par-dessus.

#### Quand utiliser encore des RDD ?

Rarement dans du nouveau code : pour un contrôle fin du partitionnement, pour traiter des données non structurées qui ne rentrent pas dans un schéma, ou avec du code existant. Les DataFrames sont plus rapides car Catalyst et Tungsten peuvent les optimiser, et en Python les opérations sur RDD sérialisent chaque enregistrement entre la JVM et Python. Les RDD ne sont pas disponibles avec Spark Connect.

#### Quelle est la différence entre map(), flatMap() et mapPartitions() ?

- `map` applique une fonction à chaque élément et renvoie un élément par entrée.
- `flatMap` applique une fonction qui renvoie une séquence pour chaque élément et aplatit les résultats.
- `mapPartitions` applique une fonction à une partition entière (un itérateur), ce qui est utile pour une préparation coûteuse, comme ouvrir une connexion une seule fois par partition.

```python
rdd = sc.parallelize([1, 2, 3, 4])
rdd.map(lambda x: x ** 2).collect()                 # [1, 4, 9, 16]

lines = sc.parallelize(["hello world", "how are you"])
lines.flatMap(lambda line: line.split(" ")).collect()
# ['hello', 'world', 'how', 'are', 'you']

def sum_partition(iterator):
    yield sum(iterator)

sc.parallelize([1, 2, 3, 4], 2).mapPartitions(sum_partition).collect()   # [3, 7]
```

#### Quelle est la différence entre reduceByKey et groupByKey ?

`reduceByKey` combine les valeurs de chaque clé dans chaque partition avant le shuffle (une combinaison côté map), donc beaucoup moins de données circulent. `groupByKey` envoie toutes les valeurs dans le shuffle puis les regroupe, ce qui consomme plus de réseau et de mémoire et peut échouer avec des clés déséquilibrées. Préférez `reduceByKey` ou `aggregateByKey`, ou mieux, les agrégations de DataFrame.

#### Comment compter des mots avec des RDD ?

```python
counts = (sc.textFile("path/to/text")
            .flatMap(lambda line: line.lower().split())
            .map(lambda word: (word, 1))
            .reduceByKey(lambda a, b: a + b)
            .sortBy(lambda pair: pair[1], ascending=False))
counts.take(10)
```

#### Que sont les variables broadcast ?

Des valeurs en lecture seule envoyées une fois à chaque executor au lieu d'accompagner chaque tâche, comme un dictionnaire de correspondance. On les crée avec `sc.broadcast(valeur)` et on lit `.value` dans les fonctions. Pour les jointures de DataFrames, utilisez plutôt l'indication de jointure `broadcast()`.

#### Que sont les accumulateurs ?

Des variables auxquelles les tâches peuvent seulement ajouter et que seul le driver peut lire, utilisées comme compteurs, par exemple du nombre de lignes mal formées. Les mises à jour faites dans des transformations peuvent être appliquées plusieurs fois si une tâche est relancée ; seules celles faites dans des actions sont garanties une seule fois.

#### Que sont la sérialisation et la désérialisation, et pourquoi Spark en a-t-il besoin ?

La **sérialisation** transforme un objet en flux d'octets pour l'envoyer sur le réseau ou le stocker de façon compacte ; la **désérialisation** reconstruit l'objet à partir de ces octets. Spark a besoin des deux pour envoyer fonctions et données du driver aux executors, déplacer les données pendant les shuffles et mettre des données en cache sous forme sérialisée.

#### Quels sérialiseurs Spark utilise-t-il ?

Côté JVM, Spark utilise par défaut le **sérialiseur Java** pour les RDD d'objets JVM, et le **sérialiseur Kryo**, plus rapide et plus compact, peut être activé (`spark.serializer=org.apache.spark.serializer.KryoSerializer`), éventuellement avec des classes enregistrées. Les DataFrames ne dépendent d'aucun des deux pour leurs données : Tungsten stocke les lignes dans son propre format binaire. En PySpark, les objets et fonctions Python sont sérialisés avec **pickle** (cloudpickle pour les fonctions), et **Apache Arrow** sert à déplacer des données en colonnes entre la JVM et pandas.

```python
from pyspark.sql import SparkSession

spark = (SparkSession.builder.appName("Kryo app")
         .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
         .getOrCreate())
```

#### Peut-on choisir le sérialiseur des RDD Python ?

Oui. Le défaut est un sérialiseur pickle par lots ; `MarshalSerializer` est plus rapide mais prend en charge moins de types. Les classes personnalisées doivent être sérialisables avec pickle et importables sur les executors (définies dans un module envoyé avec `--py-files`, pas seulement dans une cellule de notebook).

```python
from pyspark import SparkContext
from pyspark.serializers import MarshalSerializer

sc = SparkContext("local[*]", "MarshalApp", serializer=MarshalSerializer())
rdd = sc.parallelize([
    {"name": "Daniel Noboa", "home": {"city": "Quito"}},
    {"name": "Nayib Bukele", "home": {"city": "San Salvador"}},
])
print(rdd.map(lambda person: person["home"]["city"]).collect())
sc.stop()
```

#### Que signifie « Task not serializable » ou une erreur de pickle ?

Une fonction envoyée aux executors fait référence à quelque chose qui ne peut pas être sérialisé, comme une SparkSession, une connexion à une base de données, un verrou ou un fichier ouvert. Créez ces objets dans la fonction (ou par partition avec `mapPartitions`/`foreachPartition`) au lieu de les capturer depuis le driver.

#### Quelle est la différence entre coalesce et repartition sur les RDD ?

La même que pour les DataFrames : `repartition(n)` fait un shuffle complet et peut augmenter ou réduire le nombre de partitions ; `coalesce(n)` fusionne des partitions existantes sans shuffle complet et ne peut que le réduire.

#### Comment passer des RDD aux DataFrames et inversement ?

`df.rdd` renvoie un RDD d'objets `Row` ; `spark.createDataFrame(rdd, schema)` ou `rdd.toDF(["col1", "col2"])` construit un DataFrame. Convertir en RDD en Python sérialise chaque ligne vers Python, évitez-le donc dans les parties critiques.

### DataFrames et schémas

#### Qu'est-ce qu'un DataFrame ?

Une collection distribuée de lignes avec des colonnes nommées et typées, comme une table. Il est immuable : chaque transformation renvoie un nouveau DataFrame. Comme Spark connaît le schéma et les opérations, Catalyst peut optimiser le code des DataFrames, contrairement aux fonctions opaques des RDD.

#### Quelle est la différence entre un DataFrame et un Dataset ?

Un Dataset est une version typée du DataFrame disponible en Scala et en Java. Dans ces langages, un DataFrame est un `Dataset[Row]`. Python n'a que des DataFrames, car il n'est pas typé statiquement.

#### Comment créer un DataFrame ?

À partir d'une liste de tuples ou d'objets `Row` avec `spark.createDataFrame`, d'un DataFrame pandas, d'un RDD, d'un fichier ou d'une table avec `spark.read`, ou en SQL via `spark.sql`.

```python
from pyspark.sql import Row

df1 = spark.createDataFrame([(1, "Bogotá"), (2, "Medellín")], ["id", "city"])
df2 = spark.createDataFrame([Row(id=1, city="Cali")])
df3 = spark.range(0, 1000)          # une seule colonne "id"
```

#### Comment définir un schéma explicite ?

Avec un `StructType` de `StructField`, ou avec une chaîne DDL. Les schémas explicites sont plus rapides que l'inférence et détectent tôt les changements de format.

```python
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

schema = StructType([
    StructField("user_id", IntegerType(), nullable=False),
    StructField("city", StringType()),
    StructField("amount", DoubleType()),
])
ddl_schema = "user_id INT, city STRING, amount DOUBLE"
```

#### Pourquoi éviter inferSchema en production ?

L'inférence relit les données (entièrement pour un CSV, ou un échantillon), ce qui est lent sur de gros fichiers. Elle peut aussi déduire des types différents selon les jours (une colonne d'identifiants lue comme entier jusqu'à l'arrivée d'une valeur contenant une lettre), si bien que les jobs échouent ou changent sans prévenir. Déclarez le schéma.

#### Comment inspecter un DataFrame ?

`printSchema()` pour l'arbre du schéma, `df.schema` et `df.dtypes` dans le code, `show(n, truncate=False)` pour les lignes, `df.columns` pour les noms, `describe()` ou `summary()` pour des statistiques de base, et `explain()` pour le plan de requête.

#### Qu'est-ce qu'un Row ?

Un objet représentant un enregistrement, dont les champs sont accessibles par nom (`row.city` ou `row["city"]`) ou par position. `collect()` et `take()` renvoient des listes de `Row` ; `row.asDict()` en convertit un en dictionnaire.

#### Quels types complexes Spark prend-il en charge ?

`ArrayType`, `MapType` et `StructType` (enregistrements imbriqués), qui peuvent s'imbriquer les uns dans les autres, plus `VARIANT` dans Spark 4 pour les données semi-structurées. On accède aux champs d'un struct avec la notation pointée (`col("address.city")`), aux tableaux avec `col("tags")[0]` ou `element_at`, et aux maps avec `col("attrs")["key"]`.

#### Comment traiter du JSON imbriqué ?

Lisez-le avec un schéma, sélectionnez les champs imbriqués avec la notation pointée, aplatissez les tableaux avec `explode`, et analysez les chaînes JSON d'une colonne avec `from_json`.

```python
from pyspark.sql import functions as F

orders = spark.read.schema(order_schema).json("path/to/orders")
flat = (orders
        .select("order_id", "customer.name", F.explode("items").alias("item"))
        .select("order_id", "name", "item.sku", "item.qty"))
```

#### Quelle est la différence entre explode et explode_outer ?

`explode` produit une ligne par élément du tableau et supprime les lignes dont le tableau est null ou vide. `explode_outer` conserve ces lignes avec un élément null. `posexplode` renvoie aussi la position de l'élément.

#### Quelle différence entre l'immuabilité des DataFrames et les variables Python ?

Les DataFrames ne changent jamais ; les transformations en renvoient de nouveaux. Réaffecter `df = df.filter(...)` fait seulement pointer la variable vers un nouveau plan. C'est pourquoi appeler `df.withColumn(...)` sans affecter le résultat ne fait rien.

#### Comment renommer des colonnes ?

Avec `withColumnRenamed(ancien, nouveau)`, `withColumnsRenamed({ancien: nouveau})` (Spark 3.4), `select(col(ancien).alias(nouveau))` ou `toDF(*nouveaux_noms)` pour toutes les renommer d'un coup.

#### Comment ajouter ou remplacer plusieurs colonnes efficacement ?

Utilisez un seul `select` ou `withColumns({...})` (Spark 3.3) au lieu d'appeler `withColumn` dans une boucle. Chaque `withColumn` ajoute une projection au plan, et des centaines d'entre elles rendent l'analyse et l'optimisation très lentes.

```python
df = df.withColumns({
    "amount_cop": F.col("amount") * F.col("fx_rate"),
    "load_date": F.current_date(),
})
```

#### Comment supprimer des colonnes et des lignes en double ?

`drop("col1", "col2")` supprime des colonnes. `distinct()` supprime les lignes identiques sur toutes les colonnes ; `dropDuplicates(["id"])` garde une ligne par clé, mais la ligne conservée n'est pas définie. Pour en garder une précise (par exemple la plus récente), utilisez une fonction de fenêtrage.

#### Comment vérifier si un DataFrame est vide ?

Avec `df.isEmpty()` (Spark 3.3) ou `len(df.head(1)) == 0`. Évitez `df.count() == 0`, qui parcourt toutes les données.

#### Quelle est la différence entre collect, take, head, show et toPandas ?

`collect()` ramène toutes les lignes au driver ; `take(n)` et `head(n)` ramènent les n premières ; `show(n)` les affiche ; `toPandas()` ramène tout dans un DataFrame pandas (via Arrow s'il est activé). Tout, sauf de petits `take`/`show`, peut épuiser la mémoire du driver sur de gros volumes.

#### Comment passer de Spark à pandas et inversement ?

Avec `spark.createDataFrame(pandas_df)` et `df.toPandas()`. Activez Arrow (`spark.sql.execution.arrow.pyspark.enabled=true`, la valeur par défaut dans les runtimes Databricks récents) pour rendre les deux conversions beaucoup plus rapides. Ne convertissez que des données qui tiennent dans la mémoire du driver.

#### Qu'est-ce que l'API pandas sur Spark ?

`pyspark.pandas`, une API compatible avec pandas qui s'exécute sur Spark (anciennement Koalas). Elle aide à migrer du code pandas vers de gros volumes, même si certaines opérations se comportent différemment (gestion de l'index, ordre) et peuvent être plus lentes que PySpark natif.

#### Comment échantillonner des données ?

`df.sample(fraction=0.1, seed=42)` pour un échantillon aléatoire (de taille approximative), `df.limit(n)` pour les premières lignes (non aléatoires), et `df.randomSplit([0.8, 0.2], seed=42)` pour séparer entraînement et test.

### Colonnes et fonctions intégrées

#### De quelles façons peut-on référencer une colonne ?

`F.col("name")`, `df["name"]`, `df.name` et, dans de nombreuses fonctions, la simple chaîne `"name"`. `df.name` échoue avec des noms qui coïncident avec des méthodes du DataFrame ou qui contiennent des espaces ; `F.col` est la forme la plus cohérente. Utilisez des accents graves pour les noms avec points ou espaces : ``F.col("`order.id`")``.

#### Pourquoi importer les fonctions sous le nom F ?

`from pyspark.sql import functions as F` évite de masquer des fonctions intégrées de Python comme `sum`, `min`, `max`, `round` et `filter`. Importer `sum` directement depuis `pyspark.sql.functions` remplace silencieusement le `sum` de Python, une source classique d'erreurs déroutantes.

#### Comment filtrer des lignes ?

Avec `filter` ou son alias `where`, à l'aide d'expressions de colonnes ou d'une chaîne SQL. Combinez les conditions avec `&`, `|` et `~`, en mettant chaque condition entre parenthèses.

```python
df.filter((F.col("amount") > 8000) & (F.col("city") == "Bogotá"))
df.where("amount > 8000 AND city = 'Bogotá'")
df.filter(~F.col("city").isin("Cali", "Pasto"))
```

#### Comment écrire une logique conditionnelle ?

Avec `F.when(...).when(...).otherwise(...)`, l'équivalent du `CASE WHEN` SQL. Sans `otherwise`, les lignes qui ne correspondent à aucune condition reçoivent null.

```python
df = df.withColumn(
    "size",
    F.when(F.col("amount") >= 10000, "large")
     .when(F.col("amount") >= 5000, "medium")
     .otherwise("small"),
)
```

#### Comment Spark traite-t-il les nulls dans les comparaisons ?

Une comparaison avec null renvoie null, que `filter` traite comme faux. `col == None` ne fonctionne pas ; utilisez `isNull()`/`isNotNull()`. Pour une égalité qui considère null égal à null, utilisez `eqNullSafe` ou l'opérateur SQL `<=>`.

#### Comment remplacer ou compléter les nulls ?

Avec `df.na.fill({"city": "unknown", "amount": 0})` ou `fillna`, `F.coalesce(col1, col2, F.lit(valeur_par_défaut))` pour la première valeur non nulle, et `df.na.drop(subset=["id"])` pour supprimer les lignes avec des nulls dans certaines colonnes.

#### Que fait lit() ?

Elle transforme une constante Python en expression de colonne, par exemple `F.lit(0)` ou `F.lit("COP")`. Beaucoup de fonctions acceptent des valeurs simples, mais `lit` est nécessaire quand une colonne est attendue, comme dans `withColumn("currency", F.lit("COP"))`.

#### Comment convertir des types ?

Avec `F.col("amount").cast("double")` ou `.cast(DoubleType())`. Sans mode ANSI, une conversion invalide renvoie null ; avec le mode ANSI (activé par défaut dans Spark 4), elle lève une erreur. `try_cast` (Spark 4, et `TRY_CAST` en SQL) renvoie explicitement null pour les valeurs invalides.

#### Qu'est-ce que le mode ANSI et pourquoi compte-t-il ?

`spark.sql.ansi.enabled` fait suivre à Spark le SQL standard : les dépassements, divisions par zéro et conversions invalides lèvent des erreurs au lieu de renvoyer null. Il est activé par défaut dans Spark 4.0. Il détecte tôt les mauvaises données, mais du code écrit pour l'ancien comportement peut échouer : testez avec le même réglage qu'en production.

#### Quelles sont les fonctions de chaînes les plus utiles ?

`lower`, `upper`, `trim`, `lpad`/`rpad`, `substring`, `concat`/`concat_ws`, `split`, `regexp_extract`, `regexp_replace`, `like`/`rlike`, `length`, `initcap` et `format_string`.

```python
df = df.withColumn("postcode", F.regexp_replace(F.trim("postcode"), r"[^0-9]", ""))
df = df.withColumn("full_name", F.concat_ws(" ", "first_name", "last_name"))
```

#### Comment analyser et formater des dates ?

Avec `to_date(col, "dd/MM/yyyy")`, `to_timestamp`, `date_format(col, "yyyy-MM")`, `date_trunc("month", ts)`, `datediff`, `months_between`, `add_months`, `date_add`, `year`/`month`/`dayofweek`, `current_date` et `current_timestamp`. Les motifs suivent le `DateTimeFormatter` de Java (`yyyy`, `MM`, `dd`, `HH`, `mm`).

#### Comment Spark gère-t-il les fuseaux horaires ?

Les timestamps sont stockés comme des instants UTC et affichés dans le fuseau de la session (`spark.sql.session.timeZone`). Définissez-le explicitement (par exemple `UTC`) pour que les résultats ne dépendent pas du réglage par défaut du cluster. Spark 3.4 a ajouté `TIMESTAMP_NTZ` pour les timestamps sans fuseau horaire.

#### Comment travailler avec des tableaux ?

Avec `array`, `array_contains`, `size`, `element_at`, `array_distinct`, `array_union`, `array_join`, `sort_array`, `explode`, `collect_list` et les fonctions d'ordre supérieur : `transform`, `filter`, `exists`, `aggregate`.

```python
df.withColumn("prices_with_tax", F.transform("prices", lambda p: p * 1.19))
df.withColumn("big_items", F.filter("items", lambda i: i["qty"] > 10))
```

#### Comment travailler avec des chaînes JSON dans une colonne ?

`from_json(col, schema)` les analyse en struct ou en map, `to_json` les resérialise, `get_json_object(col, "$.a.b")` extrait une valeur par chemin, et `schema_of_json` déduit un schéma à partir d'une chaîne d'exemple.

#### Qu'est-ce que monotonically_increasing_id() ?

Une fonction qui génère des identifiants uniques de 64 bits par ligne. Ils sont croissants au sein d'une partition, mais pas consécutifs (le numéro de partition est encodé dans les bits de poids fort). Pour des numéros consécutifs, utilisez `row_number()` sur une fenêtre, ce qui nécessite un tri.

#### Comment générer un hash ou une clé de substitution ?

Avec `F.sha2(F.concat_ws("||", *cols), 256)`, `md5` ou `xxhash64`. Les clés de hachage sont déterministes : la même clé métier reçoit toujours la même clé de substitution, ce qui est utile pour les chargements incrémentaux et pour comparer des enregistrements afin de détecter les changements.

#### Comment faire un pivot et un unpivot ?

`groupBy("store").pivot("month").sum("revenue")` transforme les valeurs de mois en colonnes ; passer la liste des valeurs (`pivot("month", ["01", "02"])`) évite une passe supplémentaire pour les trouver. `unpivot` (aussi appelé `melt`, Spark 3.4) retransforme les colonnes en lignes.

#### Que fait expr() ?

Elle transforme une expression SQL en colonne : `F.expr("amount * fx_rate")` ou `df.selectExpr("id", "upper(city) AS city")`. C'est pratique pour les fonctions qui n'existent qu'en SQL et pour les transformations pilotées par configuration.

#### Comment arrondir et formater des nombres ?

Avec `round(col, 2)` (arrondi au supérieur sur .5), `bround` (arrondi bancaire), `format_number(col, 2)` pour l'affichage, et `DecimalType(p, s)` pour des montants exacts, car `double` est un type à virgule flottante.

### Agrégations et regroupements

#### Comment agréger un DataFrame ?

Avec `groupBy(...).agg(...)` et des fonctions d'agrégation, en nommant chaque résultat avec `alias`.

```python
summary = (df.groupBy("city")
             .agg(F.count("*").alias("orders"),
                  F.sum("amount").alias("revenue"),
                  F.avg("amount").alias("avg_amount"),
                  F.countDistinct("user_id").alias("customers")))
```

#### Quelle est la différence entre count("*"), count(col) et countDistinct ?

`count("*")` compte les lignes ; `count(col)` compte les valeurs non nulles d'une colonne ; `countDistinct(col)` compte les valeurs distinctes non nulles et nécessite un shuffle par valeur. Sur de gros volumes, `approx_count_distinct(col, rsd=0.02)` utilise HyperLogLog et coûte beaucoup moins cher.

#### Quelle est la différence entre collect_list et collect_set ?

Les deux rassemblent des valeurs dans un tableau par groupe : `collect_list` garde les doublons, `collect_set` les supprime. Aucune ne garantit l'ordre. Pour obtenir une liste ordonnée, rassemblez des structs et triez le tableau, ou utilisez une fonction de fenêtrage.

#### Pourquoi first() et last() ne sont-ils pas fiables dans les agrégations ?

Sans ordre explicite, la ligne « première » dépend de la façon dont les données ont été partitionnées et déplacées, donc les résultats peuvent changer d'une exécution à l'autre. Utilisez `max_by`/`min_by` (Spark 3.3), par exemple `F.max_by("status", "updated_at")`, ou une fenêtre avec `row_number()`.

#### Comment filtrer sur un agrégat (HAVING en SQL) ?

Agrégez d'abord, puis filtrez le résultat.

```python
(df.groupBy("city")
   .agg(F.avg("amount").alias("avg_amount"))
   .filter(F.col("avg_amount") > 8000))
```

#### Que font rollup et cube ?

`rollup("country", "city")` ajoute des sous-totaux pour chaque niveau de la hiérarchie plus un total général ; `cube` ajoute des sous-totaux pour chaque combinaison des colonnes. `grouping()` et `grouping_id()` distinguent les vrais nulls des lignes de sous-total.

#### Comment calculer des percentiles et des médianes ?

`percentile_approx(col, 0.5)` (aussi `approx_percentile`) est rapide et fonctionne sur de gros volumes ; `percentile` et `median` (Spark 3.4) sont exacts mais plus coûteux.

#### Comment Spark exécute-t-il physiquement une agrégation ?

En général en deux phases : une agrégation partielle dans chaque partition (comme une combinaison côté map), un shuffle par clé de regroupement, puis une agrégation finale. C'est pourquoi les agrégations déplacent bien moins de données que les lignes brutes, sauf si presque toutes les clés sont uniques.

#### Comment compter les lignes par groupe en gardant les colonnes d'origine ?

Avec une fonction de fenêtrage : `F.count("*").over(Window.partitionBy("city"))` ajoute le comptage à chaque ligne, sans réduire le DataFrame comme le fait `groupBy`.

### Jointures

#### Quels types de jointure Spark prend-il en charge ?

`inner`, `left` (`left_outer`), `right`, `full` (`outer`), `left_semi` (les lignes de gauche qui ont une correspondance, avec seulement les colonnes de gauche), `left_anti` (les lignes de gauche sans correspondance) et `cross`.

```python
orders.join(customers, on="customer_id", how="left")
orders.join(blocked, on="customer_id", how="left_anti")    # commandes des clients non bloqués
```

#### Comment éviter les noms de colonnes en double après une jointure ?

Joignez sur un nom de colonne ou une liste de noms (`on="user_id"`), ce qui ne garde qu'une colonne de clé. Avec une expression (`df1.user_id == df2.user_id`), les deux colonnes subsistent et sélectionner `user_id` ensuite échoue pour ambiguïté. Donnez des alias aux DataFrames ou supprimez la colonne d'un des côtés.

#### Quelles stratégies de jointure Spark peut-il choisir ?

- **Broadcast hash join :** le petit côté est copié sur chaque executor ; pas de shuffle du gros côté.
- **Shuffle hash join :** les deux côtés passent par un shuffle sur la clé et le plus petit est haché dans chaque partition.
- **Sort-merge join :** les deux côtés passent par un shuffle, sont triés par clé puis fusionnés. C'est le choix par défaut pour les grandes tables.
- **Broadcast nested loop join et produit cartésien :** pour les jointures sans égalité et les jointures croisées. Ils sont coûteux.

#### Qu'est-ce qu'un broadcast join et quand l'utiliser ?

Quand un côté est assez petit pour tenir dans la mémoire d'un executor (une dimension ou une table de correspondance), Spark en envoie une copie à chaque executor et le gros côté est joint sur place, sans shuffle. Spark le fait automatiquement sous `spark.sql.autoBroadcastJoinThreshold` (10 Mo par défaut), et AQE peut basculer vers cette stratégie à l'exécution. Vous pouvez le forcer avec une indication.

```python
from pyspark.sql.functions import broadcast

large_df = spark.createDataFrame([("A", 1000), ("B", 2000), ("C", 3000), ("D", 4000)], ["key", "amount"])
small_df = spark.createDataFrame([("A", "Apple"), ("B", "Banana"), ("C", "Cherry")], ["key", "fruit"])

large_df.join(broadcast(small_df), "key", "inner").show()
```

#### Quels sont les risques du broadcast ?

Si la « petite » table est en réalité grande, la diffusion peut épuiser la mémoire du driver ou des executors, car la table est rassemblée sur le driver puis copiée sur chaque executor. Des délais d'attente de broadcast (`spark.sql.broadcastTimeout`) peuvent aussi survenir. Ne diffusez que des tables dont vous savez qu'elles resteront petites.

#### Qu'est-ce qu'une jointure déséquilibrée (skewed join) et quels en sont les symptômes ?

Une jointure où quelques valeurs de clé concentrent une grande part des lignes, si bien que les tâches qui traitent ces clés reçoivent bien plus de données que les autres. Symptômes : un stage où la plupart des tâches finissent en quelques secondes et quelques-unes durent des minutes ou des heures, beaucoup de spill sur ces tâches et des erreurs de mémoire. Le résumé des tâches de la Spark UI (durée maximale très supérieure à la médiane) le montre.

#### Comment atténuer le déséquilibre ?

- Laissez AQE découper les partitions déséquilibrées (`spark.sql.adaptive.skewJoin.enabled`, activé par défaut).
- Diffusez l'autre côté s'il est petit.
- Filtrez ou traitez à part les clés chaudes, souvent des nulls ou des valeurs par défaut comme `-1` ou `"unknown"`.
- **Salez** la clé : ajoutez un suffixe aléatoire côté gros jeu et répliquez le petit côté pour chaque suffixe.

```python
from pyspark.sql import functions as F

num_salts = 8
large_salted = large_df.withColumn("salt", (F.rand() * num_salts).cast("int"))
small_salted = small_df.crossJoin(spark.range(num_salts).withColumnRenamed("id", "salt"))
joined = large_salted.join(small_salted, ["key", "salt"]).drop("salt")
```

#### Pourquoi les clés nulles posent-elles problème dans les jointures ?

Null n'est jamais égal à null dans une condition de jointure, donc les clés nulles ne correspondent à rien, mais elles atterrissent toutes dans la même partition pendant le shuffle, ce qui crée du déséquilibre. Filtrez-les avant la jointure (et réintégrez-les par union si vous en avez besoin dans une jointure gauche) ou remplacez-les par la clé d'un membre « inconnu ».

#### Comment faire une jointure sans égalité ou par intervalle ?

Avec une condition comme `events.ts.between(periods.start, periods.end)`. Sans condition d'égalité, Spark utilise un broadcast nested loop join ou un produit cartésien, lents sur de gros volumes. Ajoutez une condition d'égalité quand c'est possible (par exemple sur un jour) ou diffusez le petit côté.

#### À quoi servent les indications (hints) de jointure ?

Elles indiquent à l'optimiseur quelle stratégie utiliser : `broadcast`, `merge` (sort-merge), `shuffle_hash` et `shuffle_replicate_nl`, via `df.hint("merge")` ou `/*+ BROADCAST(t) */` en SQL. Utilisez-les quand les statistiques manquent ou sont fausses, et vérifiez-les après une mise à jour de Spark.

#### Qu'est-ce qu'une semi-jointure et quand est-elle préférable à une jointure interne ?

Une jointure `left_semi` renvoie les lignes de gauche qui ont au moins une correspondance, sans ajouter de colonnes de droite ni dupliquer les lignes en cas de correspondances multiples. C'est la version DataFrame de `WHERE EXISTS`, plus efficace qu'une jointure interne suivie d'un `distinct`.

#### Qu'est-ce que le bucketing ?

Écrire une table découpée à l'avance en un nombre fixe de buckets selon une clé (`bucketBy(64, "customer_id").saveAsTable(...)`). Les jointures et agrégations entre tables bucketées de la même façon sur la clé peuvent éviter le shuffle. Cela ne fonctionne qu'avec des tables enregistrées dans le metastore, et sur les tables Delta le liquid clustering l'a largement remplacé.

#### Comment joindre efficacement de nombreux petits DataFrames ?

Diffusez-les, joignez-les du plus sélectif au moins sélectif et assurez-vous que les filtres s'appliquent avant les jointures. Si vous joignez la même grande table encore et encore dans une boucle, restructurez la logique en une seule jointure ou une union.

### Fonctions de fenêtrage

#### Qu'est-ce qu'une fonction de fenêtrage ?

Une fonction qui calcule une valeur pour chaque ligne à partir d'un groupe de lignes liées (la fenêtre) sans les réduire, contrairement à `groupBy`. Une fenêtre se définit avec `Window.partitionBy(...)`, généralement `orderBy(...)` et éventuellement un cadre.

#### Quelle est la différence entre row_number, rank et dense_rank ?

Pour des valeurs à égalité dans l'ordre : `row_number` donne des numéros uniques et consécutifs (les égalités sont départagées arbitrairement), `rank` donne le même numéro aux égalités et laisse des trous (1, 1, 3), et `dense_rank` donne le même numéro aux égalités sans trous (1, 1, 2).

#### Comment garder l'enregistrement le plus récent par clé ?

Numérotez les lignes de chaque clé par timestamp décroissant et gardez la première. Ajoutez une colonne de départage à l'ordre pour que le résultat soit déterministe.

```python
from pyspark.sql import Window, functions as F

w = Window.partitionBy("customer_id").orderBy(F.col("updated_at").desc(), F.col("event_id").desc())
latest = (df.withColumn("rn", F.row_number().over(w))
            .filter("rn = 1")
            .drop("rn"))
```

#### Comment obtenir les N premiers par groupe ?

Avec le même modèle et `rn <= N`. Utilisez `dense_rank` au lieu de `row_number` si toutes les égalités à la limite doivent être incluses.

#### Que font lag et lead ?

Ils renvoient la valeur d'une ligne précédente (`lag`) ou suivante (`lead`) selon l'ordre de la fenêtre, avec un décalage et une valeur par défaut optionnels. On les utilise pour les différences entre lignes consécutives, la détection de changements et la construction de périodes de validité.

#### Comment calculer un total cumulé et une différence d'un jour à l'autre ?

```python
from pyspark.sql import Window, functions as F

sales_df = spark.createDataFrame([
    ("2024-01-01", "A", 10), ("2024-01-02", "A", 15), ("2024-01-03", "A", 7),
    ("2024-01-01", "B", 20), ("2024-01-02", "B", 5),
], ["date", "store", "revenue"])

w = Window.partitionBy("store").orderBy("date")
result = (sales_df
          .withColumn("running_revenue", F.sum("revenue").over(w))
          .withColumn("day_to_day_diff", F.col("revenue") - F.lag("revenue").over(w)))
result.show()
```

La première ligne de chaque magasin a une différence nulle, car il n'y a pas de ligne précédente.

#### Qu'est-ce que le cadre d'une fenêtre ?

L'ensemble des lignes, relatif à la ligne courante, qu'utilise un agrégat : `rowsBetween(début, fin)` compte des lignes physiques et `rangeBetween(début, fin)` utilise les valeurs de la colonne d'ordre. Utilisez `Window.unboundedPreceding`, `Window.currentRow` et `Window.unboundedFollowing` comme bornes.

#### Quel est le cadre par défaut, et pourquoi surprend-il ?

Avec `orderBy`, le cadre par défaut est `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. En cas d'égalités dans la colonne d'ordre, toutes les lignes à égalité sont incluses, si bien qu'une somme « cumulée » peut faire des sauts. Et `last()` sur le cadre par défaut renvoie la ligne courante, pas la dernière ligne de la partition. Sans `orderBy`, le cadre est la partition entière.

#### Comment calculer une moyenne mobile sur 7 jours ?

Triez sur une version numérique de la date et utilisez un cadre par intervalle, pour que les jours manquants soient correctement pris en compte.

```python
w = (Window.partitionBy("store")
           .orderBy(F.col("date").cast("timestamp").cast("long"))
           .rangeBetween(-6 * 86400, 0))
df.withColumn("avg_7d", F.avg("revenue").over(w))
```

#### Que font ntile et percent_rank ?

`ntile(n)` répartit les lignes triées en n groupes de taille proche (des quartiles avec 4) ; `percent_rank` donne le rang relatif de chaque ligne entre 0 et 1 ; `cume_dist` donne la proportion de lignes dont la valeur est inférieure ou égale à la valeur courante.

#### Comment détecter des sessions ou des écarts entre événements ?

Utilisez `lag` pour obtenir l'heure de l'événement précédent, marquez une nouvelle session quand l'écart dépasse un seuil, et faites la somme cumulée des marques pour obtenir le numéro de session.

```python
w = Window.partitionBy("user_id").orderBy("event_ts")
sessions = (events
    .withColumn("prev_ts", F.lag("event_ts").over(w))
    .withColumn("new_session",
                (F.col("prev_ts").isNull() |
                 (F.col("event_ts").cast("long") - F.col("prev_ts").cast("long") > 1800)).cast("int"))
    .withColumn("session_id", F.sum("new_session").over(w)))
```

#### Pourquoi les fonctions de fenêtrage peuvent-elles coûter cher ?

Chaque `partitionBy` différent exige un shuffle et un tri. Une fenêtre sans `partitionBy` regroupe toutes les données dans une seule partition, ce qui est lent et peut épuiser la mémoire ; Spark émet un avertissement dans ce cas. Réutilisez la même spécification de fenêtre pour plusieurs colonnes afin que Spark ne trie qu'une fois.

### Spark SQL et le catalogue

#### Comment exécuter du SQL sur un DataFrame ?

Enregistrez-le comme vue temporaire et interrogez-le avec `spark.sql`. Le résultat est un DataFrame, on peut donc mélanger librement SQL et l'API DataFrame ; les deux sont compilés vers le même plan.

```python
df.createOrReplaceTempView("sales")
top = spark.sql("""
    SELECT city, SUM(amount) AS revenue
    FROM sales
    GROUP BY city
    ORDER BY revenue DESC
""")
```

#### Quelle est la différence entre une vue temporaire et une vue temporaire globale ?

Une vue temporaire n'existe que dans la SparkSession qui l'a créée. Une vue temporaire globale est partagée entre les sessions d'une même application et vit dans la base `global_temp` (`SELECT * FROM global_temp.my_view`). Aucune ne survit à la fin de l'application.

#### Comment passer des paramètres à spark.sql en toute sécurité ?

Utilisez les requêtes paramétrées (Spark 3.4+), pas le formatage de chaînes, pour éviter l'injection SQL et les erreurs de guillemets.

```python
spark.sql("SELECT * FROM sales WHERE city = :city AND amount > :min",
          args={"city": "Bogotá", "min": 8000})
```

#### Quelle est la différence entre tables gérées et tables externes ?

Pour une table gérée, Spark (ou le catalogue) contrôle les métadonnées et les données, et `DROP TABLE` supprime les fichiers. Pour une table externe, vous indiquez l'emplacement, et la supprimer n'efface que les métadonnées. Avec Unity Catalog, les tables gérées bénéficient aussi de fonctionnalités de maintenance automatique.

#### Qu'est-ce que le catalogue ?

La couche de métadonnées qui recense les bases (schémas), tables, vues et fonctions : le metastore Hive, l'AWS Glue Data Catalog ou Unity Catalog. En PySpark, `spark.catalog` permet de lister les tables, de vérifier leur existence (`spark.catalog.tableExists`), de mettre des tables en cache et de rafraîchir les métadonnées.

#### Comment écrire dans une table plutôt que dans un chemin ?

Avec `df.write.mode("overwrite").saveAsTable("analytics.sales")`, ou `insertInto` pour une table existante (qui associe les colonnes par position et non par nom, source fréquente de bugs). Avec Delta Lake, vous pouvez aussi utiliser `MERGE INTO` en SQL.

#### Que fait REFRESH TABLE ?

Elle invalide les métadonnées et la liste des fichiers que Spark garde en cache pour une table, ce qui est nécessaire quand un autre processus que Spark a modifié les fichiers. Sans cela, vous pouvez voir des erreurs « fichier introuvable » ou des données périmées.

#### Peut-on définir des fonctions SQL réutilisables ?

Oui. Enregistrez des fonctions Python comme UDF avec `spark.udf.register` pour les appeler depuis SQL, ou créez des fonctions SQL avec `CREATE FUNCTION ... RETURN ...`, qui restent dans le moteur et sont plus rapides que les UDF Python.

#### Que sont les expressions de table communes (CTE) en Spark SQL ?

Des blocs `WITH nom AS (...)` qui rendent lisibles les requêtes complexes. Spark les intègre dans le plan ; une CTE référencée plusieurs fois peut être calculée plusieurs fois si l'optimiseur ne la réutilise pas, donc mettez en cache ou matérialisez les plus lourdes si nécessaire.

### Lecture et écriture des données

#### Comment lire correctement un fichier CSV ?

Déclarez le schéma et les options dont le fichier a besoin.

```python
df = (spark.read
      .schema("user_id INT, product_id INT, amount DOUBLE, city STRING")
      .option("header", True)
      .option("delimiter", ";")
      .option("encoding", "UTF-8")
      .option("mode", "PERMISSIVE")
      .csv("path/to/files/"))
```

Notez que le schéma se passe dans `.schema()`, pas dans `.options()`.

#### Quels sont les modes de lecture CSV/JSON ?

`PERMISSIVE` (par défaut) met à null les champs mal formés et peut conserver la ligne brute dans la colonne désignée par `columnNameOfCorruptRecord` ; `DROPMALFORMED` supprime silencieusement les lignes invalides ; `FAILFAST` lève une erreur dès la première ligne invalide. En production, préférez le mode permissif avec une colonne d'enregistrements corrompus et mettez explicitement les lignes invalides en quarantaine.

#### Quels formats de fichiers Spark prend-il en charge ?

En natif : Parquet, ORC, JSON, CSV, texte, Avro (via un module fourni), fichiers binaires et sources JDBC. Les formats de table comme Delta Lake, Apache Iceberg et Apache Hudi ajoutent des transactions au-dessus de Parquet. Parquet ou un format de table devrait être le choix par défaut pour l'analytique.

#### Pourquoi Parquet est-il le format privilégié ?

Il est en colonnes et compressé, stocke le schéma et conserve des statistiques min/max par groupe de lignes. Spark peut ne lire que les colonnes utiles (column pruning) et sauter les groupes de lignes qui ne peuvent pas satisfaire un filtre (predicate pushdown), ce qui lit bien moins de données que du CSV ou du JSON.

#### Quels sont les modes d'écriture ?

`append` ajoute des données, `overwrite` les remplace, `ignore` ne fait rien si des données existent, et `error`/`errorifexists` (par défaut) échoue si des données existent. Avec `overwrite` sur une table partitionnée, le réglage du mode d'écrasement décide de ce qui est remplacé.

#### Qu'est-ce que l'écrasement dynamique des partitions ?

Avec `spark.sql.sources.partitionOverwriteMode=dynamic`, un overwrite ne remplace que les partitions présentes dans le DataFrame écrit, au lieu de toute la table. C'est la manière sûre de retraiter un jour ou un pays. Avec Delta, l'équivalent est `replaceWhere`.

```python
(df.write.mode("overwrite")
   .option("partitionOverwriteMode", "dynamic")
   .partitionBy("ingest_date")
   .parquet("s3://bucket/sales/"))
```

#### Que fait partitionBy à l'écriture ?

Il crée un répertoire par valeur des colonnes indiquées (`country=CO/`, `country=PE/`). Les requêtes qui filtrent sur ces colonnes ne lisent que les répertoires correspondants (partition pruning). Utilisez-le sur des colonnes de faible cardinalité filtrées dans la plupart des requêtes, comme une date ; partitionner sur une colonne de forte cardinalité crée des millions de petits fichiers.

#### Qu'est-ce que le problème des petits fichiers ?

De nombreux petits fichiers (bien en dessous de 128 Mo) ralentissent les lectures, car chaque fichier a un coût de listage, d'ouverture et de lecture des métadonnées, et ils créent de nombreuses tâches minuscules. Les causes : un partitionnement excessif, de nombreuses partitions écrites par tâche et des ajouts petits et fréquents. On le corrige en repartitionnant avant d'écrire, en compactant (`OPTIMIZE` avec Delta) et en choisissant de meilleures colonnes de partition.

#### Comment contrôler le nombre et la taille des fichiers de sortie ?

Repartitionnez ou appliquez coalesce avant d'écrire (`df.repartition(16)` ou `df.repartition("country")`), définissez `maxRecordsPerFile`, ou laissez le format de table s'en charger (écritures optimisées et compaction automatique de Delta). Avec AQE, les partitions de shuffle sont fusionnées automatiquement, ce qui aide aussi.

#### Comment ne lire que les nouveaux fichiers de façon incrémentale ?

Avec Structured Streaming sur une source de fichiers (ou Auto Loader sur Databricks) et un checkpoint, qui mémorise les fichiers traités ; avec `trigger(availableNow=True)`, il s'exécute comme un job batch. Les alternatives : conserver un repère de la dernière date traitée ou utiliser le change data feed d'un format de table.

#### Comment lire depuis une base de données relationnelle ?

Avec la source JDBC. Définissez `partitionColumn`, `lowerBound`, `upperBound` et `numPartitions` pour lire en parallèle ; sinon, une seule tâche lit toute la table. Poussez les filtres vers la base avec une requête (option `query`) et gardez les identifiants dans un gestionnaire de secrets.

```python
df = (spark.read.format("jdbc")
      .option("url", jdbc_url)
      .option("dbtable", "public.orders")
      .option("user", user).option("password", password)
      .option("partitionColumn", "order_id")
      .option("lowerBound", 1).option("upperBound", 50_000_000)
      .option("numPartitions", 16)
      .load())
```

#### Qu'est-ce que l'évolution de schéma et comment la gérer ?

Les changements du schéma dans le temps, comme l'ajout de colonnes. Les lecteurs Parquet peuvent fusionner les schémas (`mergeSchema`), mais c'est coûteux. Les formats de table la gèrent explicitement : Delta ajoute des colonnes avec `mergeSchema` à l'écriture ou l'évolution de schéma dans `MERGE`. Les renommages et changements de type nécessitent des migrations explicites.

#### Que fait input_file_name() ?

Elle renvoie le chemin du fichier d'où provient chaque ligne (avec Unity Catalog, utilisez plutôt la colonne `_metadata.file_path`). C'est utile pour le lignage et le débogage, par exemple pour remonter d'une ligne invalide jusqu'à son fichier d'origine.

#### Pourquoi utiliser un format de table comme Delta Lake plutôt que du Parquet simple ?

Les dossiers Parquet simples n'ont pas de transactions : un job en échec peut laisser des données à moitié écrites, des écritures concurrentes peuvent corrompre les résultats, et les mises à jour ou suppressions obligent à réécrire des fichiers à la main. Delta, Iceberg et Hudi ajoutent transactions ACID, `MERGE`, voyage dans le temps, contrôle du schéma et compaction au-dessus de Parquet.

#### Comment faire un upsert dans une table Delta depuis PySpark ?

```python
from delta.tables import DeltaTable

target = DeltaTable.forName(spark, "silver.customers")
(target.alias("t")
   .merge(updates.alias("s"), "t.customer_id = s.customer_id")
   .whenMatchedUpdateAll()
   .whenNotMatchedInsertAll()
   .execute())
```

Dédupliquez d'abord la source par clé : un `MERGE` échoue si plusieurs lignes source correspondent à la même ligne cible.

### Partitionnement, shuffles et mémoire

#### Qu'est-ce qu'un shuffle et pourquoi coûte-t-il cher ?

Un shuffle redistribue les données dans le cluster pour que les lignes de même clé se retrouvent dans la même partition. Chaque tâche écrit sa sortie sur le disque local en blocs par partition cible, et les tâches du stage suivant récupèrent ces blocs par le réseau. Il coûte des E/S disque, du transfert réseau, de la sérialisation et de la mémoire, et dans les cas extrêmes il fait échouer les jobs. C'est souvent la partie la plus coûteuse d'un job.

#### Comment réduire les shuffles ?

- Utilisez des transformations narrow quand c'est possible et filtrez et sélectionnez les colonnes tôt.
- Diffusez les petites tables dans les jointures.
- Agrégez avant de joindre quand c'est possible.
- Évitez les `repartition`, `distinct` et `orderBy` inutiles.
- Réutilisez le partitionnement : des données bucketées ou co-partitionnées peuvent éviter des shuffles.
- Utilisez `reduceByKey` au lieu de `groupByKey` avec les RDD.

#### Que contrôle spark.sql.shuffle.partitions ?

Le nombre de partitions après un shuffle dans les opérations sur DataFrames (200 par défaut). Trop pour de petites données crée des tâches minuscules ; trop peu pour de gros volumes crée d'énormes partitions qui débordent sur disque. AQE fusionne automatiquement les partitions après le shuffle, donc une valeur de départ plus élevée est généralement sans risque.

#### Que font repartition et coalesce ?

- **`repartition(n)`** ou `repartition(n, "col")` fait un shuffle complet et produit n partitions de taille proche (par hachage des colonnes si elles sont données). Il peut augmenter ou réduire le nombre de partitions.
- **`coalesce(n)`** fusionne des partitions existantes sans shuffle complet, il ne peut donc que les réduire. Il est moins coûteux, mais peut laisser des partitions inégales et réduire le parallélisme du stage précédent.

#### Quand utiliser repartitionByRange ?

Quand il faut ranger les données par plages d'une colonne, par exemple avant d'écrire des fichiers qui couvrent chacun une plage de dates ou d'identifiants, ce qui améliore le saut de données. Il échantillonne les données pour choisir les bornes des plages.

#### Combien de partitions produit une lecture de fichiers ?

À peu près la taille totale divisée par `spark.sql.files.maxPartitionBytes` (128 Mo par défaut), ajustée par `spark.sql.files.openCostInBytes`, qui regroupe les petits fichiers. Un fichier non découpable (comme un CSV compressé en gzip) devient toujours une seule partition, quelle que soit sa taille.

#### Comment la mémoire d'un executor est-elle répartie ?

Le tas de la JVM moins 300 Mo réservés est découpé ainsi : `spark.memory.fraction` (0,6) est une mémoire unifiée partagée entre l'exécution (shuffles, jointures, tris, agrégations) et le stockage (cache), le stockage pouvant être évincé jusqu'à `spark.memory.storageFraction` (0,5). Le reste est la mémoire utilisateur. Hors du tas se trouve la mémoire d'overhead (`spark.executor.memoryOverhead`, 10 % ou au moins 384 Mo), qui couvre aussi les processus worker Python.

#### Pourquoi des jobs PySpark échouent-ils parfois sur la mémoire du conteneur alors que le tas va bien ?

Les workers Python s'exécutent hors du tas de la JVM, dans la zone d'overhead. Des UDF Python lourdes, des pandas UDF avec de gros lots ou `toPandas` sur les executors peuvent la dépasser, et YARN ou Kubernetes tue le conteneur. Augmentez `spark.executor.memoryOverhead` ou définissez `spark.executor.pyspark.memory`, et réduisez la taille des lots Arrow.

#### Qu'est-ce que le spill ?

Quand la mémoire d'exécution ne suffit pas pour un shuffle, un tri ou une agrégation, Spark écrit des données intermédiaires sur disque et les relit plus tard. La Spark UI l'affiche comme « spill (memory) » et « spill (disk) ». Le spill ralentit fortement les tâches ; réduisez-le avec des partitions plus nombreuses et plus petites, plus de mémoire par cœur ou moins de données par tâche.

#### Qu'est-ce qui provoque un OutOfMemoryError sur le driver ?

Rassembler de gros résultats (`collect`, `toPandas`), diffuser une table trop grande, des plans de requête énormes (des milliers de colonnes ou d'appels à `withColumn` dans des boucles) et le suivi d'un très grand nombre de tâches ou de fichiers. Évitez de ramener des données au driver et gardez des plans compacts.

#### Qu'est-ce qui provoque un OutOfMemoryError sur les executors ?

Des partitions déséquilibrées, trop peu de partitions pour le volume de données, de grandes lignes ou de grands tableaux (d'énormes résultats de `collect_list`), trop de cœurs par executor partageant la mémoire et des UDF Python gourmandes en mémoire. Regardez les métriques des tâches du stage en échec pour savoir si c'est une seule tâche (déséquilibre) ou toutes (dimensionnement).

#### Quelle est la différence entre cache et persist ?

`cache()` stocke les données avec le niveau de stockage par défaut : `MEMORY_ONLY` pour les RDD, mémoire et disque pour les DataFrames. `persist(niveau)` permet de choisir le niveau : `MEMORY_ONLY`, `MEMORY_AND_DISK`, `DISK_ONLY`, et des variantes sérialisées et répliquées. Les deux sont paresseux : les données sont mises en cache la première fois qu'une action les calcule. Libérez-les avec `unpersist()`.

#### Quand la mise en cache en vaut-elle la peine ?

Quand le même DataFrame sert à plusieurs actions et coûte cher à recalculer, par exemple après une jointure coûteuse utilisée par trois sorties différentes. Elle ne vaut pas la peine pour des données utilisées une seule fois ou peu coûteuses à lire, et elle prend de la mémoire à l'exécution. Sur Databricks serverless, `cache()` et `persist()` ne sont pas pris en charge ; écrivez plutôt une table intermédiaire.

#### Quelle est la différence entre cache et checkpoint ?

Le cache conserve les données mais aussi tout le lignage, donc les partitions perdues sont recalculées. `checkpoint()` écrit les données sur un stockage fiable et coupe le lignage, ce qui aide pour les plans très longs (algorithmes itératifs, boucles). `localCheckpoint()` coupe le lignage en utilisant le stockage des executors, plus rapide mais non tolérant aux pannes.

### Catalyst, AQE et plans de requête

#### Quel est le rôle de l'optimiseur Catalyst ?

Catalyst transforme le code DataFrame et SQL en un plan d'exécution efficace. Il applique des règles comme le predicate pushdown, le column pruning, le constant folding et le réordonnancement des jointures, puis choisit les opérateurs physiques (par exemple la stratégie de jointure). Il fonctionne avec les DataFrames, les Datasets et le SQL, pas avec les RDD, dont les fonctions lui sont opaques.

#### Quelles sont les phases de Catalyst ?

1. **Analyse :** résout les noms et types des colonnes et des tables à partir du catalogue (du plan logique non résolu au plan logique).
2. **Optimisation logique :** applique des réécritures fondées sur des règles.
3. **Planification physique :** génère des plans physiques candidats et en choisit un, en s'appuyant sur les statistiques si elles existent.
4. **Génération de code :** la génération de code whole-stage compile des parties du plan en bytecode JVM.

#### Que sont le predicate pushdown et le column pruning ?

Le **predicate pushdown** déplace les filtres au plus près de la source de données, si bien que Parquet peut sauter des groupes de lignes et les sources JDBC peuvent filtrer dans la base. Le **column pruning** ne lit que les colonnes utilisées par la requête. Les deux sont automatiques, sauf si quelque chose les bloque, comme un filtre enveloppé dans une UDF Python.

#### Qu'est-ce qu'Adaptive Query Execution (AQE) ?

Une couche d'optimisation, activée par défaut depuis Spark 3.2, qui replanifie les requêtes à l'exécution à partir de statistiques réelles issues des stages de shuffle terminés. Elle fusionne les petites partitions de shuffle, transforme des sort-merge joins en broadcast joins quand un côté s'avère petit, et découpe les partitions déséquilibrées dans les jointures.

#### Qu'est-ce que le dynamic partition pruning ?

Quand une table de faits partitionnée est jointe à une dimension filtrée, Spark utilise à l'exécution le résultat du filtre de la dimension pour élaguer les partitions de la table de faits, qui ne lit alors que les partitions correspondantes. Il est activé par défaut et très efficace pour les requêtes sur schéma en étoile.

#### Comment lire un plan de requête ?

Avec `df.explain()` ou `df.explain(mode="formatted")` (aussi `extended`, `cost` et `codegen`). Lisez le plan physique de bas en haut : les lectures (cherchez `PushedFilters`, `PartitionFilters` et `ReadSchema`), les nœuds `Exchange` (shuffles), les types de jointure (`BroadcastHashJoin`, `SortMergeJoin`) et `BatchEvalPython`/`ArrowEvalPython` (UDF Python).

#### Que signifie un Exchange dans le plan ?

Un shuffle (`Exchange hashpartitioning`, `rangepartitioning`) ou une diffusion (`BroadcastExchange`). Compter les nœuds `Exchange` est un moyen rapide d'estimer combien de shuffles fait une requête.

#### Qu'est-ce que la génération de code whole-stage ?

Tungsten regroupe plusieurs opérateurs d'un stage (lecture, filtre, projection, agrégation) en une seule fonction Java générée, supprimant les appels virtuels et les objets intermédiaires. Dans le plan, les opérateurs préfixés par `*` ou les blocs numérotés `WholeStageCodegen` bénéficient de la génération de code.

#### Qu'est-ce que l'optimiseur fondé sur les coûts ?

Une partie optionnelle de Catalyst qui utilise des statistiques sur les tables et les colonnes (nombre de lignes, valeurs distinctes, histogrammes) pour choisir l'ordre et la stratégie des jointures. Il nécessite des statistiques collectées avec `ANALYZE TABLE ... COMPUTE STATISTICS FOR COLUMNS` et tenues à jour.

#### Pourquoi une longue chaîne de transformations peut-elle ralentir un job avant même son démarrage ?

Catalyst analyse et optimise tout le plan, et des plans très grands (des centaines d'appels à `withColumn`, des boucles qui font des unions ou des jointures répétées) peuvent prendre des minutes à optimiser ou faire déborder la pile du driver. Regroupez les projections dans un seul `select`, et coupez les longues boucles avec des checkpoints ou des tables intermédiaires.

### Optimisation des performances et débogage

#### Comment déboguer un job qui prend beaucoup plus de temps que prévu ?

Commencez par mesurer, pas par deviner :

- Ouvrez la Spark UI et trouvez le stage qui prend le temps.
- Regardez son résumé de tâches : si la durée maximale est très au-dessus de la médiane, c'est un déséquilibre ; si toutes les tâches sont lentes, c'est le dimensionnement ou le volume de données.
- Regardez les volumes lus et écrits en shuffle et le spill.
- Lisez le plan physique (`explain`) pour voir si les filtres sont poussés à la source, quelles stratégies de jointure ont été choisies et si des UDF Python interviennent.
- Corrigez le plus gros problème, mesurez à nouveau et ne changez qu'une chose à la fois.

#### Que montre la Spark UI ?

Les onglets **Jobs** et **Stages** (durées, résumés de tâches, métriques de shuffle et de spill), **Storage** (données en cache), **Environment** (configuration), **Executors** (mémoire, temps de GC, tâches en échec) et **SQL / DataFrame** (le plan exécuté avec le nombre de lignes par opérateur). Pour les applications terminées, utilisez le Spark History Server.

#### Quelles sont les causes les plus fréquentes de jobs Spark lents ?

À peu près dans cet ordre : lire trop de données (pas d'élagage, CSV/JSON au lieu de Parquet, nombreux petits fichiers), des shuffles inutiles ou volumineux, le déséquilibre des données, le spill dû à des partitions trop grosses pour la mémoire, les UDF Python, la collecte de données sur le driver, et trop peu ou trop de partitions.

#### Quelles mauvaises pratiques PySpark faut-il éviter ?

- `collect()` ou `toPandas()` sur des données non bornées.
- Des UDF Python là où une fonction intégrée existe.
- `withColumn` dans une boucle au lieu de `withColumns` ou d'un seul `select`.
- Des `crossJoin` accidentels ou des jointures sans condition.
- `repartition(1)`/`coalesce(1)` sur de gros volumes, qui fait passer tout par une seule tâche.
- `inferSchema` sur de grosses entrées de production.
- Appeler `count()` juste pour journaliser un nombre, ce qui déclenche un job complet supplémentaire.
- Réutiliser un DataFrame coûteux dans plusieurs actions sans le mettre en cache ni le matérialiser.

#### Pourquoi count() est-il parfois lent, et quand faut-il l'éviter ?

`count()` est une action : il exécute tout le plan jusqu'à ce point. L'appeler pour journaliser après chaque étape recalcule tout plusieurs fois. Comptez une seule fois sur des données matérialisées, utilisez les métriques de l'écriture (historique de la table, Spark UI) ou acceptez des comptages approximatifs.

#### Comment choisir le nombre de partitions de shuffle ?

Visez des partitions d'environ 100 à 200 Mo après le shuffle et au moins deux à trois fois plus de partitions que de cœurs au total. Avec AQE activé, choisissez un nombre de départ généreux (ou `spark.sql.adaptive.coalescePartitions.initialPartitionNum`) et laissez AQE fusionner les petites.

#### Qu'est-ce que l'exécution spéculative ?

Avec `spark.speculation=true`, Spark lance des copies de secours des tâches beaucoup plus lentes que les autres du même stage et garde celle qui termine la première. Cela aide face à des nœuds lents, pas face au déséquilibre, car une tâche déséquilibrée est lente sur n'importe quel nœud. Les sorties doivent être idempotentes.

#### Comment faire profiter les filtres et les jointures de l'organisation des données ?

Partitionnez ou regroupez (clustering) les tables selon les colonnes filtrées par la plupart des requêtes, et filtrez directement sur les colonnes stockées. Un filtre comme `to_date(event_ts) = '2026-10-15'` peut ne rien élaguer ; `event_date = '2026-10-15'` sur une colonne de partition ou de clustering, si. Gardez des tailles de fichiers saines grâce à la compaction.

#### Comment réduire le temps de ramasse-miettes ?

Utilisez des DataFrames plutôt que des RDD d'objets Python, évitez les executors très gros (au-delà d'environ 64 Go de tas), utilisez G1GC (le défaut des versions récentes de Java), mettez en cache sous forme sérialisée si vous cachez beaucoup, et réduisez le nombre d'objets créés dans les UDF. L'onglet Executors affiche le temps de GC par executor.

#### Que faire d'un job qui traite beaucoup plus de données que nécessaire ?

Traitez de façon incrémentale : ne lisez que les nouveaux fichiers (streaming avec `availableNow`, Auto Loader), n'écrivez que les partitions concernées (`replaceWhere`, écrasement dynamique), ne fusionnez que les lignes modifiées, et sautez les étapes dont les entrées n'ont pas changé. Les données les moins chères sont celles qu'on ne traite pas.

#### Quel est l'effet de trop nombreuses colonnes ou de lignes très larges ?

Les lignes larges augmentent la mémoire par ligne, la taille des shuffles et la complexité du plan. Sélectionnez tôt les seules colonnes utiles, évitez de transporter de grandes colonnes texte ou binaires à travers les jointures, et découpez les tables très larges si la plupart des requêtes n'utilisent que quelques colonnes.

#### Comment trouver quelle partie de votre code a produit un stage lent ?

Dans l'onglet SQL / DataFrame, le plan exécuté relie les opérateurs aux stages. Nommez vos jobs avec `spark.sparkContext.setJobDescription("load silver companies")` (ou `setJobGroup`), pour que l'onglet Jobs indique à quelle étape appartient chaque job.

#### Pourquoi la première exécution d'un job est-elle plus lente que les suivantes ?

À cause du préchauffage de la JVM, du chargement des classes, de la génération de code, de la mise à l'échelle automatique du cluster et des caches froids (le cache de fichiers du système d'exploitation et, sur Databricks, le cache disque). Mesurez les performances sur plusieurs exécutions et sur un volume de données réaliste.

### UDF, pandas et Arrow

#### Qu'est-ce qu'une UDF et pourquoi une UDF Python est-elle lente ?

Une fonction définie par l'utilisateur applique du code Python personnalisé à chaque ligne. Chaque ligne doit être sérialisée de la JVM vers un worker Python, traitée par l'interpréteur Python, puis resérialisée en retour. Catalyst ne voit pas son contenu, il ne peut donc ni l'optimiser ni pousser des filtres à travers elle. Les fonctions intégrées s'exécutent dans la JVM et sont généralement bien plus rapides.

```python
from pyspark.sql import functions as F
from pyspark.sql.types import StringType

@F.udf(returnType=StringType())
def clean_city(city):
    return city.strip().title() if city else None

# La version intégrée est plus rapide et fait la même chose :
df.withColumn("city", F.initcap(F.trim("city")))
```

#### Qu'est-ce qu'une pandas UDF ?

Une UDF vectorisée (`@pandas_udf`) qui reçoit des Series ou des DataFrames pandas par lots transférés avec Apache Arrow, au lieu d'une ligne à la fois. Elle est bien plus rapide qu'une UDF ligne par ligne, et vous pouvez y utiliser des opérations vectorisées pandas et NumPy.

```python
import pandas as pd
from pyspark.sql.functions import pandas_udf

@pandas_udf("double")
def to_cop(amount: pd.Series, rate: pd.Series) -> pd.Series:
    return amount * rate

df.withColumn("amount_cop", to_cop("amount", "fx_rate"))
```

#### Que sont les UDF Python optimisées avec Arrow ?

Depuis Spark 3.5, les UDF Python classiques peuvent utiliser Arrow pour la sérialisation (`@udf(useArrow=True)` ou `spark.sql.execution.pythonUDF.arrow.enabled`). La fonction traite toujours une ligne à la fois, mais le transfert des données est plus rapide.

#### Que font applyInPandas et mapInPandas ?

`groupBy(...).applyInPandas(func, schema)` exécute une fonction pandas sur chaque groupe sous forme de DataFrame pandas (chaque groupe doit tenir en mémoire). `mapInPandas(func, schema)` exécute une fonction sur un itérateur de DataFrames pandas par partition, par exemple pour appliquer un modèle de machine learning par lots.

#### Qu'est-ce qu'une UDTF Python ?

Une fonction de table définie par l'utilisateur (Spark 3.5) qui renvoie plusieurs lignes par entrée, définie comme une classe Python avec une méthode `eval` qui produit des lignes. Elle sert à analyser ou à développer des enregistrements d'une manière que `explode` ne peut pas exprimer.

#### Comment éviter les UDF ?

Cherchez d'abord dans `pyspark.sql.functions` : les fonctions de chaînes, de dates, de regex, de tableaux, de maps, JSON et d'ordre supérieur couvrent la plupart des besoins. Combinez-les avec `when`, `expr` et des expressions SQL. Utilisez une pandas UDF si vous avez vraiment besoin de bibliothèques Python, et une UDF ligne par ligne seulement en dernier recours.

#### Pourquoi les UDF doivent-elles gérer None ?

Les colonnes peuvent contenir des nulls, que les fonctions Python reçoivent sous la forme `None`. Une UDF qui appelle `city.strip()` sans vérification fait échouer tout le job au premier null. Déclarez aussi le bon type de retour : une incohérence renvoie null sans prévenir.

#### Comment utiliser un modèle de machine learning dans PySpark ?

Diffusez le modèle, ou chargez-le une fois par partition, et appliquez-le avec une pandas UDF ou `mapInPandas` pour vectoriser les prédictions. `spark_udf` de MLflow transforme un modèle enregistré en UDF Spark.

#### Quand faut-il plutôt convertir en pandas ?

Quand les données sont déjà petites après agrégation (par exemple quelques milliers de lignes pour un graphique ou un rapport) et que vous avez besoin de fonctionnalités propres à pandas. Agrégez d'abord dans Spark, puis appelez `toPandas()` sur le petit résultat.

### Structured Streaming

#### Qu'est-ce que Structured Streaming ?

L'API de traitement de flux de Spark, qui traite un flux comme une table non bornée qui grandit avec le temps. Vous écrivez les mêmes opérations sur DataFrame qu'en batch, et Spark les exécute de façon incrémentale en micro-lots, en conservant l'état et la progression dans un checkpoint.

#### Quels sont les composants principaux d'une requête de streaming ?

Une source (`readStream` depuis Kafka, des fichiers, Delta ou Auto Loader), des transformations, une destination (`writeStream` vers Delta, Kafka, des fichiers ou `foreachBatch`), un trigger, un mode de sortie et un emplacement de checkpoint.

```python
query = (spark.readStream.format("kafka")
         .option("kafka.bootstrap.servers", brokers)
         .option("subscribe", "orders")
         .load()
         .select(F.from_json(F.col("value").cast("string"), order_schema).alias("o"))
         .select("o.*")
         .writeStream
         .format("delta")
         .option("checkpointLocation", "s3://bucket/checkpoints/orders")
         .trigger(processingTime="1 minute")
         .toTable("bronze.orders"))
```

#### Quels triggers sont disponibles ?

Par défaut, les micro-lots s'enchaînent le plus vite possible ; `processingTime="1 minute"` les exécute à intervalle fixe ; `availableNow=True` traite tout ce qui est disponible en plusieurs lots puis s'arrête, ce qui est idéal pour des jobs incrémentaux planifiés ; `once=True` est déprécié au profit d'`availableNow`. Le mode continu existe, mais il est expérimental et limité.

#### Quels sont les modes de sortie ?

`append` n'écrit que les nouvelles lignes (le défaut ; les agrégations nécessitent un watermark), `update` écrit les lignes modifiées depuis le dernier trigger, et `complete` réécrit tout le résultat à chaque fois (seulement pour les agrégations, et réaliste seulement pour de petits résultats).

#### À quoi sert le checkpoint ?

Il stocke les offsets traités et l'état des opérations avec état, si bien qu'une requête redémarrée reprend là où elle s'était arrêtée sans perdre ni dupliquer de données. Chaque requête a besoin de son propre emplacement de checkpoint, et certains changements de requête (comme modifier les agrégations) sont incompatibles avec un checkpoint existant.

#### Qu'est-ce qu'un watermark ?

Un seuil sur le temps de l'événement qui indique à Spark le retard maximal des données (`withWatermark("event_ts", "10 minutes")`). Spark s'en sert pour finaliser les agrégations par fenêtre et supprimer l'ancien état. Sans watermark, l'état des agrégations et des jointures entre flux grossit indéfiniment.

#### Comment agréger par fenêtres de temps dans un flux ?

Regroupez par une `window` (fixe ou glissante) sur la colonne de temps de l'événement, avec un watermark.

```python
counts = (events
          .withWatermark("event_ts", "10 minutes")
          .groupBy(F.window("event_ts", "5 minutes"), "store")
          .count())
```

#### Que fait foreachBatch ?

Il vous fournit chaque micro-lot comme un DataFrame ordinaire avec un identifiant de lot, pour utiliser des API batch que les destinations de streaming ne prennent pas en charge : `MERGE` dans Delta, écriture vers plusieurs destinations, ou appels à des systèmes externes. Rendez la fonction idempotente, par exemple grâce à l'identifiant du lot, car un lot peut être réexécuté après une panne.

```python
def upsert(batch_df, batch_id):
    (DeltaTable.forName(spark, "silver.orders").alias("t")
       .merge(batch_df.alias("s"), "t.order_id = s.order_id")
       .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())

stream.writeStream.foreachBatch(upsert).option("checkpointLocation", ckpt).start()
```

#### Quelles garanties Structured Streaming offre-t-il ?

Un traitement exactly-once de bout en bout quand la source peut être relue (Kafka, fichiers) et que la destination est idempotente ou transactionnelle (Delta, destinations fichiers, `foreachBatch` idempotent). Avec des destinations non idempotentes (appel d'une API), vous obtenez du at-least-once.

#### Comment dédupliquer un flux ?

Avec `dropDuplicates(["event_id"])` et un watermark, pour que l'état des identifiants déjà vus puisse être supprimé après un certain temps, ou avec `dropDuplicatesWithinWatermark` (Spark 3.5). Sans watermark, l'ensemble des clés vues grossit sans limite.

#### Comment joindre des flux ?

Les jointures entre un flux et des données statiques (enrichir des événements avec une table de dimension) sont simples et sans état. Les jointures entre deux flux nécessitent des watermarks des deux côtés et une condition temporelle, pour que Spark sache combien de temps conserver l'état de chaque côté.

#### Comment surveiller une requête de streaming ?

`query.status`, `query.lastProgress` et `query.recentProgress` indiquent le débit d'entrée, le débit de traitement, la durée des lots et la taille de l'état. L'onglet Structured Streaming de la Spark UI les affiche en graphiques, et `StreamingQueryListener` envoie les métriques aux outils de supervision. Alertez quand le débit de traitement reste inférieur au débit d'entrée.

### Tests et bonnes pratiques

#### Comment structurer du code PySpark pour le rendre testable ?

Écrivez les transformations comme des fonctions qui prennent et renvoient des DataFrames, sans lire ni écrire à l'intérieur. Gardez des jobs minces : ils lisent les entrées, appellent les fonctions et écrivent les résultats. Chemins, dates et noms de tables sont des paramètres, pas des constantes.

```python
def latest_per_key(df, key, order_col):
    w = Window.partitionBy(key).orderBy(F.col(order_col).desc())
    return df.withColumn("_rn", F.row_number().over(w)).filter("_rn = 1").drop("_rn")
```

#### Comment écrire des tests unitaires pour du code PySpark ?

Avec pytest et une fixture de SparkSession locale de portée session, de petits DataFrames en mémoire et les fonctions de comparaison de `pyspark.testing` (Spark 3.5) : `assertDataFrameEqual` et `assertSchemaEqual`.

```python
import pytest
from pyspark.sql import SparkSession
from pyspark.testing import assertDataFrameEqual

@pytest.fixture(scope="session")
def spark():
    session = (SparkSession.builder.master("local[2]")
               .config("spark.sql.shuffle.partitions", "2")
               .getOrCreate())
    yield session
    session.stop()

def test_latest_per_key(spark):
    df = spark.createDataFrame([(1, "old", 1), (1, "new", 2)], ["id", "v", "ts"])
    expected = spark.createDataFrame([(1, "new", 2)], ["id", "v", "ts"])
    assertDataFrameEqual(latest_per_key(df, "id", "ts"), expected)
```

#### Pourquoi mettre une valeur basse pour spark.sql.shuffle.partitions dans les tests ?

Avec la valeur par défaut de 200, chaque petit test qui fait un shuffle crée 200 tâches minuscules, ce qui ralentit la suite de tests. Deux à quatre partitions suffisent pour de petites données.

#### Que doivent couvrir les tests au-delà des tests unitaires ?

Une exécution de bout en bout de tout le pipeline sur de petits fichiers synthétiques, l'idempotence (relancer sur la même entrée ne change rien), les cas limites comme les nulls, les entrées vides, les doublons et les lignes mal formées, et des contrôles de qualité des données sur les données réelles en production.

#### Comment rendre les jobs idempotents ?

Écrivez avec `overwrite` de partitions précises, `replaceWhere` ou `MERGE` au lieu d'un `append` aveugle, dérivez les sorties uniquement des entrées (pas de `current_date()` qui décide quoi traiter, sauf s'il s'agit d'un paramètre) et utilisez des clés déterministes. Une relance après une panne doit produire exactement le même résultat.

#### Quelles sont les bonnes conventions de code pour PySpark ?

Importez les fonctions sous le nom `F`, préférez les expressions de colonnes aux chaînes pour construire la logique, utilisez des schémas explicites, enchaînez les transformations entre parenthèses plutôt qu'avec des barres obliques inverses, donnez des alias lisibles aux agrégations, évitez `select("*")` avant d'écrire, et gardez les règles métier dans des fonctions nommées et testées.

#### Comment journaliser des informations utiles sans ralentir le job ?

Journalisez sur le driver : paramètres, chemins d'entrée, décisions de plan et durées. Évitez les actions uniquement destinées aux logs ; utilisez les métriques d'écriture, l'historique de la table ou un seul comptage de la sortie finale. Utilisez `setJobDescription` pour que les logs et la Spark UI concordent.

#### Comment gérer les enregistrements invalides en production ?

Lisez en mode permissif avec une colonne d'enregistrements corrompus, validez les lignes avec des règles explicites, envoyez les échecs dans une table de quarantaine avec leur motif, et arrêtez le job si la part de lignes invalides dépasse un seuil. Les suppressions silencieuses (`DROPMALFORMED`) masquent les problèmes.

### Exercices pratiques

#### Exercice 1 : agrégations

Soit ce fichier CSV :

```csv
user_id;product_id;amount;city
1;101;12500.0;Bogota
2;102;9000.0;Cartagena
1;103;3000.0;Bogota
4;104;12500.0;Medellin
5;101;6250.0;Bogota
2;102;9000.0;Medellin
```

- Chargez le CSV dans un DataFrame.
- Calculez le montant total par utilisateur.
- Calculez le montant moyen des transactions par ville.
- Ne gardez que les villes où le montant moyen des transactions dépasse 8000.
- Renvoyez les résultats sous forme de deux DataFrames, `total_per_user` et `city_avg`, et mettez l'un d'eux en cache.

```python
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.getOrCreate()

df_sales = (spark.read
            .schema("user_id INT, product_id INT, amount DOUBLE, city STRING")
            .options(header=True, delimiter=";")
            .csv("path/to/file"))

total_per_user = df_sales.groupBy("user_id").agg(F.sum("amount").alias("total_amount"))

city_avg = (df_sales.groupBy("city")
            .agg(F.avg("amount").alias("avg_amount"))
            .filter(F.col("avg_amount") > 8000))

city_avg.cache()
city_avg.show()     # la première action remplit le cache
```

#### Exercice 2 : jointures

Soit ces deux fichiers :

```csv
user_id;name
1;Wilmer
2;Jayson
```

```csv
user_id;product_id;amount
1;101;12500.0
1;102;8900.0
2;103;3000.0
2;101;5000.0
```

- Chargez les deux DataFrames.
- Joignez-les pour obtenir les noms des utilisateurs et les montants des transactions.
- Calculez le total dépensé par utilisateur.
- Triez par montant total, en ordre décroissant.

```python
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.getOrCreate()
df_users = spark.read.schema("user_id INT, name STRING").options(header=True, delimiter=";").csv("path/to/users")
df_transactions = (spark.read
                   .schema("user_id INT, product_id INT, amount DOUBLE")
                   .options(header=True, delimiter=";")
                   .csv("path/to/transactions"))

df_total_per_user = (df_users.join(df_transactions, on="user_id", how="inner")
                     .groupBy("user_id", "name")
                     .agg(F.sum("amount").alias("total_amount"))
                     .orderBy(F.col("total_amount").desc()))
```

Joindre sur `"user_id"` ne garde qu'une colonne de clé, et regrouper par `user_id` en plus de `name` évite de fusionner deux utilisateurs différents portant le même nom.

#### Exercice 3 : fonctions de fenêtrage

Avec le DataFrame `sales_df` de la section sur les fonctions de fenêtrage (date, store, revenue), calculez le chiffre d'affaires cumulé dans le temps de chaque magasin et l'écart avec le jour précédent.

```python
from pyspark.sql import Window, functions as F

w = Window.partitionBy("store").orderBy("date")
window_revenue = (sales_df
                  .withColumn("cumulative_revenue", F.sum("revenue").over(w))
                  .withColumn("day_to_day_diff", F.col("revenue") - F.lag("revenue").over(w)))
window_revenue.show()
```

#### Exercice 4 : dédoublonnage

Une table `customers_raw` reçoit chaque modification d'un client, avec `customer_id`, `email`, `updated_at` et `ingested_at`. Construisez une table avec exactement une ligne par client : la version la plus récente, en utilisant `ingested_at` pour départager.

```python
w = Window.partitionBy("customer_id").orderBy(F.col("updated_at").desc(), F.col("ingested_at").desc())
customers = (spark.table("customers_raw")
             .withColumn("rn", F.row_number().over(w))
             .filter("rn = 1")
             .drop("rn"))
```

#### Exercice 5 : meilleurs produits par ville

À partir des ventes de l'exercice 1, renvoyez les deux produits au chiffre d'affaires le plus élevé dans chaque ville, égalités comprises.

```python
revenue = df_sales.groupBy("city", "product_id").agg(F.sum("amount").alias("revenue"))
w = Window.partitionBy("city").orderBy(F.col("revenue").desc())
top2 = revenue.withColumn("rank", F.dense_rank().over(w)).filter("rank <= 2")
```

#### Exercice 6 : aplatir du JSON imbriqué

Chaque commande est un document JSON avec un `order_id`, un struct `customer` (`id`, `city`) et un tableau `items` de structs (`sku`, `qty`, `price`). Produisez une ligne par article avec l'identifiant de la commande, la ville du client et le total de la ligne.

```python
order_schema = """
    order_id STRING,
    customer STRUCT<id: STRING, city: STRING>,
    items ARRAY<STRUCT<sku: STRING, qty: INT, price: DOUBLE>>
"""
lines = (spark.read.schema(order_schema).json("path/to/orders")
         .select("order_id", F.col("customer.city").alias("city"), F.explode("items").alias("item"))
         .select("order_id", "city", "item.sku",
                 (F.col("item.qty") * F.col("item.price")).alias("line_total")))
```

Utilisez `explode_outer` si les commandes sans article doivent aussi apparaître.

#### Exercice 7 : trouver ce qui a changé entre deux photos

Vous recevez chaque mois une photo complète d'un registre. Comparez la photo de ce mois avec celle du mois précédent (toutes deux avec `company_id`, `name`, `status`) et classez chaque entreprise comme nouvelle, supprimée, modifiée ou inchangée.

```python
cols = ["name", "status"]
prev = previous.withColumn("h_prev", F.sha2(F.concat_ws("||", *cols), 256)).select("company_id", "h_prev")
curr = current.withColumn("h_curr", F.sha2(F.concat_ws("||", *cols), 256)).select("company_id", "h_curr")

changes = (curr.join(prev, "company_id", "full")
           .withColumn("change",
                       F.when(F.col("h_prev").isNull(), "new")
                        .when(F.col("h_curr").isNull(), "removed")
                        .when(F.col("h_prev") != F.col("h_curr"), "changed")
                        .otherwise("unchanged")))
```

`concat_ws` ignore les nulls, donc un passage de null à une chaîne vide passe inaperçu. Entourez les colonnes de `coalesce(col, lit("<null>"))` si cette distinction compte.
