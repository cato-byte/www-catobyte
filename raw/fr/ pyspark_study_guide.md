## Guide d'etude Pyspark

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Image créée par ChatGPT, OpenAI. 11 octobre 2025 ](../../images/pyspark_study_guide_title_img.webp)


### Index
[Jointures Broadcast vs Jointures Skewed](#what-are-broadcast-joins)
[Concepts clés de Spark](#key-spark-concepts)

<a name="key-spark-concepts"></a>
### Concepts clés de Spark

- Transformation : Méthode sur un dataframe qui renvoie un autre dataframe.
- Action : Méthode sur un dataframe qui renvoie une valeur.
- Catalyst Optimizer : Mécanisme Spark qui évalue toutes les transformations à exécuter et détermine la méthode la plus efficace pour les exécuter ensemble.

<a name="diff-spark-concepts"></a>
### Quelle est la différence entre SparkContext, SparkSession et SQLContext ?

Ils constituent tous trois des points d'entrée pour interagir avec le moteur de traitement :

- SparkContext : Point d'entrée d'origine de Spark. Conçu pour lancer l'application, établir une connexion au cluster et gérer les opérations sur les RDD. Se concentre sur les opérations personnalisées des RDD.
- SparkSession : Point d'entrée moderne pour Spark, unifiant les différents points d'entrée et donnant accès à SparkSQL et aux DataFrames.
- SQLContext : Point d'entrée pour SparkSQL. Spark SQL est un module Spark pour le traitement de données structurées. Il fournit une abstraction appelée DataFrames et peut agir comme un moteur SQL distribué.

```python
depuis pyspark.sql import SparkSession

spark = SparkSession.builder.appName("MyOtherApp").getOrCreate()
df = spark.createDataFrame([('Rosa María Casas del Campo',16,'Planeta Rica','Colombia','Null'),('Hideo Kojima',63,'Setagaya','Japón')],['name','age','city_of_birth','country_of_birth'])
df.show()
spark.stop()
```

### Différences entre l'instanciation de SparkContext et SparkSession

La configuration de SparkContext implique de configurer directement le Spark Master ou d'utiliser SparkConf pour une configuration détaillée.

```python
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster('local[0]').setAppName('MiAplicacion')
sc = SparkContext(conf = conf)
print(sc.applicationId)
sc.stop()
```

La session Spark utilise un modèle de builder.

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder\
.appName('ProcesadorDeDatos')\
.config('spark.executor.memory','1g')
.getOrCreate()
print(spark.sparkContext.applicationId)
spark.stop()
```
### Prise en charge des RDD : SparkContext vs. Spark Session

SparkContext gère directement les RDD, tandis que SpárkSession intègre un SparkContext qui gère ces interactions.

```python
from pyspark import SparkConf, SparkContext

sc = SparkContext('local[0]','MyRDDApp')
rdd = sc.parallelize(['A','B','C'])
print(rdd.collect())
sc.stop()
```
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("RDDSparkSession").getOrCreate()
sc = spark.SparkContext
rdd = sc.parallelize([1,2,3])
print(rdd.collect())
sc.stop()
```

### Prise en charge des DataFrames : SparkContext vs. Spark Session

SparkContext ne prend pas en charge les DataFrames, seule SparkSession le fait.

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DataFrames").getOrCreate()
df = spark.createDataFrame([('AWS Redshift',2013),('Apache Spark', 2009)],['product','year_of_release'])
df_recent_releases = df.filter(df.year_of_release > 2010)
df_recent_releases.show()
spark.close()
```

### Différence entre transformation large et transformation étroite dans Pyspark

Dans Spark, les transformations étroites sont celles qui ne nécessitent pas de brassage. Cela améliore les performances car les opérations peuvent être traitées individuellement dans leurs propres partitions. Voici quelques-unes de ces opérations : filter, map et union. Les jointures ne peuvent être une fonction étroite que si l'ensemble de données est partitionné par la clé de jointure.

À l'inverse, les opérations qui nécessitent un brassage entre les workers sont appelées partitions larges. Elles pénalisent les performances en termes de temps d'exécution, mais sont parfois inévitables. Les jointures, groupbykey et reduceByKey sont des opérations qui nécessitent un brassage des données.

### Évaluation paresseuse dans Spark

L'évaluation paresseuse est une fonctionnalité de Spark qui empêche l'exécution des transformations tant qu'une action n'est pas exécutée. Grâce à Catalyst, elle recherche la méthode la plus efficace pour combiner les transformations.

### Pyspark est plus rapide que Python pur

Cela dépend de la taille de l'ensemble de données. Pyspark est généralement plus rapide que Python car il peut répartir la charge de travail sur différents nœuds et traiter les données en parallèle. Cependant, il existe…

### Problème pratique 1

Soit le fichier CSV suivant :
```
user_id;product_id;amount;city
1;101;12500.0;Bogota
2;102;9000.0;Carthagène
1;103;3000.0;Bogota
4;104;12500.0;Medellin
5;101;6250.0;Bogota
2;102;9000.0;Medellin
```
- Charger le fichier CSV dans un DataFrame
- Calculer le montant total par utilisateur
- Calculer le montant moyen des transactions par ville
- Filtrer uniquement les villes dont le montant moyen des transactions est supérieur à 8000
- Afficher les résultats sous forme de deux DataFrames : total_per_user et city_avg
- Mettre en cache l'un des DataFrames.

```python
depuis pyspark.sql importer SparkSession
depuispyspark.sql.types import StringType, DoubleType, StructType, IntegerType
from pyspark.sql.functions import col,avg

spark = SparkSession.builder.getOrCreate()

schema = StructType() \
.add("user_id",IntegerType(),True) \
.add("product_id",IntegerType(),True) \
.add("amount",DoubleType(),True) \
.add("city",StringType(),True)

df_products = spark.read.options(header=True,delimiter=";",schema=schema).csv('chemin/vers/fichier')

total_par_utilisateur = df_products.groupBy('user').sum('amount')

filtered_avg_city = df_products.groupBy('ville').agg(moyenne('montant').alias(montant_moyenne)).filter(col('montant_moyenne' > 8000)

filtered_moyenne_ville.cache()
```

### Problème pratique 2

Soit les fichiers CSV suivants :

```csv
ID_utilisateur;nom
1;'Wilmer'
2;'Jayson'
```
```
ID_utilisateur;ID_produit;montant
1;101;12500.0
1;102;8900.0
2;103;3000.0
2;101;5000.0
```

Charger les dataframes
Joindre les dataframes pour obtenir les noms d'utilisateur et les montants des transactions
Calculer le total dépensé par utilisateur
Trier par ordre décroissant du montant total

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, sort

spark = SparkSession.builder.getOrCreate()
df_user = spark.read.options(header=True,delimiter=";",inferSchema=True).csv("chemin/vers/fichier")
df_transactions = spark.read.options(header=True,delimiter=";",inferSchema=True).csv("chemin/vers/fichier")

df_user_transactions = df_user.join(df_transactions,df_user.user_id == df_transactions.user_id,"inner")
df_total_per_user = df_user_transactions.groupBy(col("name")).agg(sum("amount")).sort(col("amount").desc

```

### Problème pratique 3

Considérons le dataframe suivant :

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

sales_df = spark.createDataFrame([
("2024-01-01", "A", 10),
("2024-01-02", "A", 15),
("2024-01-03", "A", 7),
("2024-01-01", "B", 20),
("2024-01-02", "B", 5)
], ["date", "store", "revenue"])

```

- Calculer le chiffre d'affaires cumulé au fil du temps Pour chaque magasin
- Différences quotidiennes dans Spark

```python

from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import sum as _sum,

windowSpec = Window.partitionBy("store").orderBy("date")

spark = SparkSession.builder.getOrCreate()

window_revenue = sales_df.withColumn("window_sum" ,̣_sum("revenue").over(windowSpec)) \
.withColumn("day_to_day_diff" ,col("revenue") - lag("revenue").over(windowSpec))

window_revenue .show()

spark.stop()

```

### Quelle est la différence entre cache et persist ?

Le cache enregistre le RDD ou le dataframe dans Mémoire uniquement. La méthode persist permet de la stocker au niveau défini par l'utilisateur : MÉMOIRE_SEULEMENT, MÉMOIRE_ET_DISQUE, DISQUE_SEULEMENT, etc.

### Qu'est-ce qu'un shuffle et pourquoi est-il coûteux ?

Un shuffle implique que les nœuds doivent envoyer des données à travers le cluster pour effectuer des opérations. Ces opérations sont appelées opérations étendues, et la transmission de toutes ces données entraîne une surcharge en termes de temps et d'utilisation des ressources. Dans les cas extrêmes, cela peut entraîner l'échec d'une tâche.

### Quel est le rôle de l'optimiseur Catalyst ?

L'optimiseur Catalyst examine le plan d'exécution du DAG et propose un ordre spécifique pour appliquer les transformations, afin d'optimiser l'utilisation des ressources. Disponible uniquement pour les dataframes et les jeux de données.

### Nommez deux façons de réduire le shuffle dans les opérations dans Spark.

La première consiste à utiliser des transformations étroites autant que possible. La seconde est une diffusion dans les jointures pour les tables de petite taille.

### Comment déboguer une tâche qui prend beaucoup plus de temps que Attendu ?

Je commencerais par examiner le plan d'exécution (df.explain() ou interface Spark) pour identifier les étapes ou transformations qui déclenchent des remaniements ou des analyses importants.

- Vérifier si les transformations peuvent être réorganisées ou combinées pour une meilleure efficacité.
- Mettre en cache ou conserver les résultats intermédiaires pour éviter les recalculs.
- Augmenter la mémoire ou les exécuteurs si la tâche manque de ressources.
- Rechercher les asymétries de données (tailles de partition inégales).
- Utiliser l'interface Spark ou les journaux pour identifier les étapes lentes et tester les optimisations progressivement.

### Expliquez l'exécution d'une tâche Spark dès l'appel d'une action. Comment le DAG est-il construit ? Qu'est-ce qu'une étape ? Que sont les tâches ? Comment sont-elles distribuées ?

Une fois qu'une action est appelée, Catalyst crée un graphe depuis l'action, en analysant la transformation précédente jusqu'à son arrivée aux jeux de données sources. Une tâche Spark est divisée en étapes, qui constituent à leur tour un ensemble de tâches. Il existe des étapes étroites et des étapes larges. Les étapes étroites signifient qu'aucun remaniement n'est nécessaire et que toutes les Les transformations sont effectuées dans chaque worker. En revanche, dans les étapes larges, les données sont remaniées entre les partitions.

### Quelle est la différence entre map(), flatMap() et mapPartitions() ?

Dans map, une fonction est appliquée à chaque élément du RDD.
Dans flatmap, une colonne produit une ou plusieurs colonnes.
Dans mapPartitions, une fonction est appliquée à une partition entière plutôt qu'à chaque élément.Par exemple, si nous voulions obtenir la moyenne d'une partition,

Exemples :
map

```python
rdd = sc.parallelize([1, 2, 3, 4])
squared_rdd = rdd.map(lambda x: x**2)
squared_rdd.collect()

# sortie
[1, 4, 9, 16]
```

mapPartitions
```python
rdd = sc.parallelize([1, 2, 3, 4], 2)
def sum_partition(iterator):
yield sum(iterator)

sum_rdd = rdd.mapPartitions(sum_partition)
sum_rdd.collect()

# sortie
[3, 7]
```

flatMap

```python
rdd = sc.parallelize(["hello world", "how are you"])

# définir une fonction pour diviser chaque ligne en mots
def split_line(line):
return line.split(" ")

flat_rdd = rdd.flatMap(split_line)
flat_rdd.collect()

# sortie
['hello', 'world', 'how', 'are', 'you']
```

<a name="what-are-broadcast-joins"></a>

### Que sont les jointures broadcast et les jointures asymétriques ? Quand les utiliser ? Quels sont les symptômes d'une jointure asymétrique ? Comment la détecter et la limiter ?

Une jointure broadcast est utilisée lorsqu'une table est trop petite pour être jointe à une table plus grande. Il est donc judicieux de la diffuser aux autres nœuds pour une jointure plus efficace. Une jointure asymétrique se produit lorsque la clé de jointure n'est pas répartie uniformément, ce qui crée une surcharge dans certaines partitions et une charge insuffisante dans d'autres. Un signe d'une jointure biaisée est que les partitions contiennent très peu ou trop d'éléments. Vous pouvez utiliser le salage pour atténuer une jointure biaisée. Exemples :

diffusion
```python
depuis pyspark.sql, importer SparkSession
depuis pyspark.sql.functions, importer col
depuis pyspark.sql.functions, importer lit, rand, floor,concat

spark = SparkSession.builder.getOrCreate()

données = [
('A', 100),
('A', 200),
('A', 300),
('B', 10),
('C', 20)
]

df = spark.createDataFrame(données, ['clé','valeur'])

```
salage biaisé

```python

# Nombre de sels
num_salts = 3

# Ajouter un sel aléatoire à la clé
df_salted = df.withColumn(
"salt", floor(rand() * num_salts)
).withColumn(
"salted_key", concat(col("key"), lit("_"), col("salt"))
)

df_salted.show()

```

### À quoi servent le repartitionnement et la coalescence ?

- Le repartitionnement : redistribue l'ensemble du dataframe et le divise en n partitions. Il permet de répartir les données entre les nœuds de calcul.
- La coalescence : réduit le nombre de partitions à n. Elle répartit les données, réduisant ainsi le nombre de données réparties dans le cluster.