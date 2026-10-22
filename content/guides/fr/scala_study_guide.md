## Fiche d'étude Scala

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude Scala : environ 220 questions](../../images/scala_study_guide_title_img.png)

Environ 220 questions Scala pour les entretiens de data engineer : le langage et son système de types, les collections et la programmation fonctionnelle, les abstractions contextuelles, la concurrence, l'outillage et l'interopérabilité avec Java, Scala avec Apache Spark, et une série d'exercices de code avec leurs solutions. Les exemples utilisent la syntaxe de Scala 3 (3.9 LTS, sortie en septembre 2026), sauf ceux qui concernent Spark, qui tourne sur Scala 2.13. Les réponses suivent la documentation officielle de docs.scala-lang.org.

La fiche suit un parcours d'apprentissage en six étapes. Chaque section est découpée en unités courtes : objectifs d'apprentissage, explication du concept et exemple commenté, puis questions (d'abord de mémorisation, ensuite d'application), un exercice pratique et les points à retenir. Pour **apprendre**, lisez chaque unité du début à la fin. Pour **réviser**, passez en mode révision ou utilisez « Aller aux questions », marquez les réponses à revoir et essayez une révision mixte entre les sections.

<!-- QA -->
<!-- stage: Fondamentaux -->

### Les bases de Scala

<!-- unit: Scala et la JVM -->

<!-- goals -->

- Expliquer ce qu'est Scala, comment il s'exécute et le lien entre Scala 2 et Scala 3.
- Choisir une version de Scala et exécuter du code avec la commande `scala`.

<!-- concept -->

Scala réunit la programmation orientée objet et la programmation fonctionnelle dans un langage à typage statique compilé en bytecode JVM. Toute valeur est un objet, les fonctions sont des valeurs et le compilateur infère la plupart des types : le code reste concis et les erreurs de type apparaissent avant l'exécution.

Scala 3 a repensé le langage en 2021, avec une syntaxe plus propre, les givens à la place des implicits, les enums et les types union. Les versions suivent deux lignes : Scala Next reçoit les nouveautés, tandis que les versions à support long (LTS) reçoivent des correctifs pendant des années. Spark, principale raison pour laquelle les data engineers rencontrent Scala, tourne toujours sur Scala 2.13.

<!-- example -->

```scala
// hello.scala
@main def hello(name: String): Unit =
  println(s"Hello, $name")
```
```bash
scala run hello.scala -- Ana      # compiles and runs; prints "Hello, Ana"
```

#### Qu'est-ce que Scala ?

Un langage à typage statique pour la JVM qui unit programmation orientée objet et programmation fonctionnelle. Son nom vient de « scalable language ». On l'utilise pour Apache Spark, le code d'origine de Kafka, les systèmes Pekko et Akka et des services backend, et il compile aussi vers JavaScript (Scala.js) et en code natif (Scala Native).

#### Comment le code Scala s'exécute-t-il ?

Le compilateur transforme les fichiers `.scala` en fichiers `.class` pour la JVM (Scala 3 écrit aussi des fichiers `.tasty` contenant l'arbre typé du programme), et la JVM les exécute avec son compilateur just-in-time. Le code Scala peut appeler directement n'importe quelle bibliothèque Java, et Java peut appeler Scala.

#### Quelles sont les principales différences entre Scala 2 et Scala 3 ?

Scala 3 ajoute la syntaxe à accolades optionnelles, `given` et `using` à la place des implicits, les méthodes d'extension, les enums, les types union et intersection, les types opaques, les définitions de premier niveau, les paramètres de traits et un nouveau système de macros fondé sur `inline` et les quotes. La plupart du code Scala 2.13 compile avec peu de changements, et les projets Scala 3 peuvent utiliser des bibliothèques Scala 2.13, mais les macros Scala 2 doivent être réécrites.

#### Que sont Scala LTS et Scala Next ?

Deux lignes de versions. Scala Next publie des versions mineures avec des nouveautés (3.10 en octobre 2026). Une version LTS reçoit au moins trois ans de correctifs sans changement du langage : 3.3 fut la première, et 3.9, sortie en septembre 2026, est la nouvelle vers laquelle migrent les bibliothèques. Depuis 3.8, Scala 3 exige le JDK 17 ou plus récent.

#### Quelle version de Scala Spark utilise-t-il ?

Spark 4 est compilé uniquement pour Scala 2.13 (Spark 3 prenait en charge 2.12 et 2.13). Il n'existe pas de version officielle pour Scala 3 : Scala 3 peut dépendre des artefacts 2.13, mais les encoders de Spark reposent sur des fonctionnalités de Scala 2, si bien que les jobs Spark s'écrivent en Scala 2.13 ou nécessitent des bibliothèques communautaires.

#### Qu'est-ce que la commande `scala` ?

Depuis Scala 3.5, `scala` est la Scala CLI : elle compile, exécute, teste et package des projets à un seul module sans fichier de build (`scala run`, `scala repl`, `scala test`, `scala package`), les dépendances et versions étant déclarées par des directives `//> using` en tête de fichier.

#### Qu'est-ce qu'une méthode `@main` ?

Une annotation Scala 3 qui fait d'une méthode de premier niveau le point d'entrée d'un programme et analyse les arguments de la ligne de commande selon le type de chaque paramètre. En Scala 2, le point d'entrée est un `def main(args: Array[String]): Unit` dans un object, ou un object qui étend `App`.

<!-- challenge -->

Une équipe veut écrire un nouveau job Spark en Scala 3 parce que « c'est la version actuelle ». Que lui conseillez-vous ?

<!-- solution -->

Écrire le job en Scala 2.13, la version pour laquelle Spark 4 est compilé et testé ; Scala 3 ne fonctionne avec Spark qu'au prix de contournements pour les encoders et les bibliothèques. Utiliser Scala 3 pour les services et bibliothèques hors Spark.

<!-- takeaways -->

- Scala est un langage objet et fonctionnel à typage statique sur la JVM.
- Scala Next ajoute des nouveautés ; les versions LTS reçoivent des correctifs pendant des années.
- Les jobs Spark utilisent Scala 2.13.

<!-- unit: Valeurs, variables et types -->

<!-- goals -->

- Utiliser `val`, `var` et `lazy val`, et s'appuyer sur l'inférence de types.
- Parcourir la hiérarchie des types de Scala, les types numériques et l'égalité.

<!-- concept -->

Scala privilégie les liaisons immuables : une `val` ne peut pas être réaffectée, une `var` si, et le code idiomatique a rarement besoin de `var`. Le compilateur infère les types à partir du membre droit, mais les méthodes publiques continuent de les déclarer pour la lisibilité et la stabilité de l'API.

Tous les types tiennent dans une seule hiérarchie : `Any` en haut, divisé entre types valeur (`Int`, `Double`, `Boolean`, `Unit`) et types référence (`AnyRef`, l'`Object` de Java). `Nothing` est tout en bas, le type des expressions qui ne retournent jamais, comme une exception levée. `==` appelle `equals` : il compare des valeurs, même pour les chaînes.

<!-- example -->

```scala
val rate = 0.19                  // Double, inferred
var retries = 0                  // reassignable: use sparingly
lazy val lookup = loadLookup()   // computed on first access, only once
val total: BigDecimal = BigDecimal("19.99") * 3
println("ab" + "c" == "abc")     // true: == compares values
def fail(msg: String): Nothing = throw IllegalStateException(msg)
```

#### Quelle est la différence entre `val`, `var` et `lazy val` ?

Une `val` est affectée une fois et ne peut pas être réaffectée (l'objet qu'elle désigne peut rester mutable). Une `var` peut être réaffectée. Une `lazy val` est calculée au premier accès, au plus une fois et de façon thread-safe, ce qui reporte un travail coûteux jusqu'au moment où il est nécessaire.

#### Qu'est-ce que l'inférence de types, et quand écrire les types malgré tout ?

Le compilateur déduit les types des valeurs et des expressions : `val n = 1` est un `Int`. Écrivez les types sur les méthodes et champs publics (ils documentent l'API et la stabilisent), sur les méthodes récursives (obligatoire), sur les givens, et quand le type inféré est trop précis, comme un `Some[Int]` là où vous voulez un `Option[Int]`.

#### Que sont `Any`, `AnyVal`, `AnyRef`, `Nothing` et `Null` ?

`Any` est le supertype de tout. `AnyVal` est le parent des types valeur (`Int`, `Double`, `Boolean`, `Char`, `Unit`), `AnyRef` celui des types référence. `Nothing` est un sous-type de tous les types et n'a aucune valeur ; c'est le type de `throw` et des collections vides comme `Nil`. `Null` est le type de `null`, sous-type des types référence.

#### Qu'est-ce que `Unit` ?

Un type à une seule valeur, `()`, renvoyé par les méthodes appelées pour leurs effets de bord, comme le `void` de Java. Comme c'est une vraie valeur, toute expression a un type en Scala, même un `println`.

#### Quelle est la différence entre `==` et `eq` ?

`==` appelle `equals`, compare les valeurs et gère `null` sans erreur : `"abc" == "ab" + "c"` est vrai, contrairement à Java. `eq` compare les références (les deux noms désignent-ils le même objet ?) et n'existe que sur `AnyRef`.

#### Comment se comportent les types numériques de Scala ?

`Int` (32 bits) et `Long` (64 bits) débordent silencieusement, `Double` est un nombre à virgule flottante binaire, et `BigInt` et `BigDecimal` offrent une précision arbitraire, nécessaire pour l'argent. La division entière tronque vers zéro (`7 / 2 == 3`, `-7 / 2 == -3`), et les tirets bas rendent les littéraux lisibles : `1_000_000`.

<!-- challenge -->

Une classe calcule une table de correspondance coûteuse dans un champ `val`, mais la plupart des instances ne l'utilisent jamais, et leur création est lente. Que changez-vous ?

<!-- solution -->

En faire une `lazy val` : elle est calculée au premier accès, au plus une fois, et les instances qui n'utilisent jamais la table ne paient rien.

<!-- takeaways -->

- Préférez `val` ; `lazy val` reporte le travail.
- `Any` est en haut, `Nothing` en bas.
- `==` compare des valeurs ; `eq` des références.

<!-- unit: Expressions et structures de contrôle -->

<!-- goals -->

- Utiliser `if`, `match`, `for` et `try` comme expressions.
- Lire la syntaxe à accolades optionnelles de Scala 3 et remplacer `break` et `continue`.

<!-- concept -->

En Scala, presque tout est une expression qui renvoie une valeur : `if`, `match`, `try` et les blocs, dont la valeur est leur dernière expression. Les variables temporaires disparaissent, et le code se lit comme la définition du résultat plutôt que comme une suite d'affectations.

Scala 3 permet aussi de remplacer les accolades par l'indentation, avec les mots-clés `then` et `do`, le style de la documentation officielle. Les accolades fonctionnent toujours, et beaucoup de projets, dont ceux en Spark sur Scala 2.13, les conservent.

<!-- example -->

```scala
val raw = "42"
val n: Int =
  try raw.toInt
  catch case _: NumberFormatException => 0

val size = if n >= 100 then "large" else "small"

for i <- 1 to 3 do println(i)                 // loop: returns Unit
val squares = for i <- 1 to 3 yield i * i     // Vector(1, 4, 9)
```

#### Que signifie « tout est une expression » en Scala ?

Des constructions qui sont des instructions dans d'autres langages renvoient des valeurs : `if`/`else`, `match`, `try`/`catch` et les blocs `{ ... }`, dont la valeur est leur dernière expression. On affecte directement leur résultat à une `val` au lieu de modifier une variable dans chaque branche.

#### Comment `if`/`else` fonctionne-t-il comme expression ?

`val label = if amount > 0 then "credit" else "debit"`. Les deux branches déterminent le type du résultat ; sans `else`, le résultat est `Unit`. Scala n'a pas d'opérateur ternaire, puisque `if` en joue déjà le rôle.

#### Quelle est la différence entre une boucle `for` et une compréhension `for` ?

`for x <- xs do ...` exécute un effet de bord par élément et renvoie `Unit`. `for x <- xs yield ...` construit une nouvelle collection (ou un Option, un Future...) à partir des résultats. Les deux sont traduites en appels de méthodes (`foreach`, `map`, `flatMap`, `withFilter`).

#### Scala a-t-il `break` et `continue` ?

Pas comme mots-clés. On utilise des méthodes de collection qui s'arrêtent tôt (`find`, `exists`, `takeWhile`), la récursion ou, depuis Scala 3.3, `scala.util.boundary` avec `break` pour sortir d'un bloc avec une valeur.

#### Qu'est-ce que la syntaxe à accolades optionnelles ?

Scala 3 peut délimiter les blocs par l'indentation, avec `then` après les conditions de `if`, `do` dans les boucles et des marqueurs `end` facultatifs pour les longs blocs. Les accolades restent valides et les deux styles peuvent se mélanger ; les formateurs et le compilateur (`-rewrite -indent` ou `-no-indent`) passent de l'un à l'autre.

#### Comment `try`/`catch`/`finally` fonctionne-t-il en Scala ?

C'est une expression : `catch` reçoit des cas de pattern matching sur les types d'exception, et `finally` fait le nettoyage sans changer le résultat. Scala n'a pas d'exceptions vérifiées. Pour les échecs attendus, `Try`, `Either` et `Using` sont en général plus clairs que l'interception d'exceptions.

<!-- challenge -->

Du code comme `var status = ""` suivi de `if (paid) status = "done" else status = "open"` apparaît dans tout un projet. Réécrivez-le de façon idiomatique.

<!-- solution -->

`val status = if paid then "done" else "open"` : l'expression `if` renvoie directement la valeur, sans variable mutable et sans risque d'oublier une branche.

<!-- takeaways -->

- `if`, `match`, `try` et les blocs renvoient des valeurs.
- `for ... do` boucle ; `for ... yield` construit un résultat.
- Pas de `break` : méthodes de collection ou `boundary`.

<!-- unit: Chaînes et interpolation -->

<!-- goals -->

- Construire des chaînes avec les interpolateurs `s`, `f` et `raw` et les littéraux multilignes.
- Découper, convertir et transformer des chaînes en sécurité.

<!-- concept -->

Les chaînes Scala sont des chaînes Java : des séquences immuables de caractères avec toutes les méthodes de Java, plus les méthodes de collection de Scala comme `map`, `filter` et `reverse`. L'interpolation construit du texte à partir de valeurs : `s` les insère, `f` les formate à la manière de printf avec vérification des types, et `raw` laisse les barres obliques inverses intactes.

Les chaînes entre triples guillemets s'étendent sur plusieurs lignes sans échappement, et `stripMargin` retire l'indentation jusqu'à un `|` pour que le littéral suive l'indentation du code.

<!-- example -->

```scala
val name = "Ana"; val total = 1234.5
println(s"Hello, $name: ${total * 2}")   // Hello, Ana: 2469.0
println(f"$name%-6s|$total%10.2f|")      // Ana   |   1234.50|
println(raw"C:\data\new")                // backslashes kept
val report =
  """Daily load
    |  rows: 1200
    |  errors: 0""".stripMargin
```

#### Quels interpolateurs de chaînes Scala propose-t-il ?

`s"..."` insère des valeurs (`$name` ou `${expr}`), `f"..."` les formate avec des spécifications de type printf vérifiées à la compilation (`$total%.2f`), et `raw"..."` ne traite pas les séquences d'échappement. Les bibliothèques définissent les leurs, comme `sql"..."` dans Doobie, qui construit des requêtes paramétrées.

#### Comment fonctionnent les chaînes multilignes et `stripMargin` ?

Les littéraux `"""..."""` s'étendent sur plusieurs lignes sans échapper guillemets ni barres obliques inverses. `stripMargin` retire sur chaque ligne les espaces de tête jusqu'à un `|` inclus, si bien que le texte peut s'indenter avec le code qui l'entoure.

#### Comment construire efficacement une longue chaîne ?

Rassemblez les morceaux et utilisez `mkString` (`rows.mkString("\n")`, avec préfixe et suffixe facultatifs), ou un `StringBuilder` dans une boucle. Répéter `+` sur des chaînes recopie à chaque fois la chaîne qui grandit.

#### Inversez une chaîne et vérifiez si c'est un palindrome, en ignorant la casse et la ponctuation.

```scala
def isPalindrome(s: String): Boolean =
  val letters = s.filter(_.isLetterOrDigit).toLowerCase
  letters == letters.reverse
```

#### Comment découper et convertir des chaînes en sécurité ?

`split` prend une expression régulière : les caractères spéciaux comme `|` et `.` doivent être échappés (`split("\\|")`) ou passés comme `Char` (`split('|')`). Utilisez `trim` ou `strip` pour les espaces, et `toIntOption`, `toDoubleOption` ou `toBooleanOption`, qui renvoient `None` au lieu de lever une exception sur une entrée invalide.

<!-- challenge -->

`line.split("|")` renvoie chaque caractère séparément au lieu des champs. Pourquoi, et comment corriger ?

<!-- solution -->

`split` prend une regex, et `|` seul signifie « vide ou vide », qui correspond entre chaque caractère. Échappez-le (`line.split("\\|")`) ou utilisez la surcharge avec `Char`, `line.split('|')`.

<!-- takeaways -->

- `s`, `f` et `raw` interpolent ; `f` vérifie les formats.
- Utilisez `mkString` plutôt que des `+` répétés.
- `split` prend une regex ; convertissez avec `toIntOption`.

### Méthodes et fonctions

<!-- unit: Méthodes -->

<!-- goals -->

- Définir des méthodes avec des paramètres par défaut, nommés et répétés.
- Utiliser plusieurs listes de paramètres et des paramètres par nom (by-name).

<!-- concept -->

Les méthodes se définissent avec `def` dans une classe, un object ou, en Scala 3, au premier niveau d'un fichier. Les arguments par défaut et nommés remplacent la plupart des surcharges et des builders, et les paramètres répétés acceptent un nombre quelconque d'arguments. Une méthode peut avoir plusieurs listes de paramètres, ce qui aide l'inférence de types, permet de passer un bloc en dernier argument et sépare les paramètres de contexte.

Les paramètres by-name (`=> A`) sont évalués à chaque utilisation dans la méthode, pas avant l'appel : la méthode reçoit du code à exécuter plus tard, ou jamais, comme dans un helper de relance ou un message de log.

<!-- example -->

```scala
def connect(host: String, port: Int = 5432, ssl: Boolean = true): String =
  s"$host:$port ssl=$ssl"
connect("db.local", ssl = false)              // named and default arguments

def total(xs: Int*): Int = xs.sum
total(1, 2, 3)
total(List(4, 5)*)                            // pass a collection (Scala 2: xs: _*)

def retry[A](times: Int)(op: => A): A =
  try op
  catch case _: Exception if times > 1 => retry(times - 1)(op)

val page = retry(3) { fetchPage(url) }        // the block runs on each attempt
```

#### Quelle est la différence entre une méthode et une fonction en Scala ?

Une méthode se définit avec `def` et appartient à une classe, un object ou un fichier ; ce n'est pas une valeur en soi. Une fonction est un objet d'un type fonction comme `Int => Int`, qu'on peut stocker et transmettre. Scala convertit automatiquement les méthodes en fonctions quand une fonction est attendue (eta-expansion).

#### Que sont les arguments par défaut et nommés ?

Les paramètres peuvent avoir des valeurs par défaut (`port: Int = 5432`), et l'appelant peut passer les arguments par nom, dans n'importe quel ordre (`connect("db", ssl = false)`). Ensemble, ils remplacent la plupart des méthodes surchargées et des classes builder, et rendent les appels explicites.

#### Que sont les paramètres répétés ?

Un paramètre de type `Int*` accepte un nombre quelconque d'arguments, reçus sous forme de `Seq[Int]`. Pour passer une collection existante, on la déplie : `total(xs*)` en Scala 3, `total(xs: _*)` en Scala 2.

#### À quoi servent plusieurs listes de paramètres ?

L'inférence de types passe d'une liste à la suivante (`foldLeft(0)(_ + _)` connaît le type de l'accumulateur grâce à la première liste), une dernière liste à un seul argument peut recevoir un bloc entre accolades (`retry(3) { ... }`), et les paramètres de contexte vont dans une liste `using` séparée. Elles permettent aussi la curryfication.

#### Qu'est-ce qu'un paramètre by-name ?

Un paramètre déclaré `op: => A` n'est pas évalué à l'appel ; l'expression est transmise non évaluée et s'exécute à chaque utilisation dans la méthode. C'est ainsi que `getOrElse`, les messages d'`assert` ou les helpers de relance reçoivent du code à exécuter plus tard, sans calculer des valeurs peut-être inutiles.

#### Pourquoi les méthodes récursives doivent-elles déclarer leur type de retour ?

Le compilateur infère le type d'une méthode à partir de son corps, mais un corps récursif dépend du type de la méthode elle-même : l'inférence ne peut pas aboutir. Déclarer le type de retour brise ce cycle.

<!-- challenge -->

Un helper `def debug(msg: String): Unit` est appelé ainsi : `debug(s"rows: ${dump(df)}")`, et le coûteux `dump` s'exécute même quand les logs de debug sont désactivés. Comment corriger ?

<!-- solution -->

Passer le paramètre en by-name, `def debug(msg: => String)`, et n'évaluer `msg` que si les logs de debug sont actifs ; sinon la chaîne, et `dump`, ne sont jamais construits.

<!-- takeaways -->

- Arguments par défaut et nommés remplacent les surcharges.
- Plusieurs listes de paramètres aident l'inférence et les blocs.
- Les paramètres by-name reportent l'évaluation.

<!-- unit: Les fonctions comme valeurs -->

<!-- goals -->

- Écrire des fonctions anonymes et utiliser des fonctions d'ordre supérieur.
- Expliquer closures, eta-expansion, curryfication et composition de fonctions.

<!-- concept -->

Les fonctions sont des valeurs avec des types comme `Int => Int`. On les passe à des méthodes comme `map`, on les renvoie depuis des méthodes et on les stocke dans des collections, et les plus courtes peuvent utiliser `_` à la place de leurs paramètres.

Une méthode devient automatiquement une fonction quand une fonction est attendue (eta-expansion). Une fonction qui utilise des variables de la portée où elle a été créée les capture, ce qui en fait une closure. La curryfication répartit les paramètres en listes séparées : fixer les premières produit une nouvelle fonction, plus spécifique.

<!-- example -->

```scala
val double: Int => Int = x => x * 2
val nums = List(1, 2, 3)
nums.map(double)                   // List(2, 4, 6)
nums.map(_ + 1)                    // placeholder syntax
def isEven(n: Int) = n % 2 == 0
nums.filter(isEven)                // method used as a function

def multiplier(k: Int): Int => Int = x => x * k   // returns a closure over k
val triple = multiplier(3)
triple(5)                          // 15
```

#### Qu'est-ce qu'une fonction anonyme ?

Un littéral de fonction sans nom : `(x: Int) => x * 2`, ou `x => x * 2` quand le contexte donne le type. C'est un objet d'un type fonction, qu'on peut passer directement à des méthodes d'ordre supérieur.

#### Que signifie le tiret bas dans `_ + 1` ?

Chaque `_` représente le paramètre suivant d'une fonction anonyme : `_ + 1` est `x => x + 1`, et `_ + _` est `(a, b) => a + b`. Cela ne fonctionne que si chaque paramètre est utilisé une fois, dans l'ordre.

#### Qu'est-ce qu'une fonction d'ordre supérieur ?

Une fonction ou méthode qui prend des fonctions en paramètres ou en renvoie une, comme `map`, `filter`, `foldLeft`, `sortBy` ou un helper `retry`. Elles séparent ce qu'on fait de chaque élément de la façon de les parcourir.

#### Qu'est-ce qu'une closure ?

Une fonction qui capture des variables de la portée où elle a été définie, comme `k` dans `x => x * k`. Elle capture des variables, pas des valeurs : les modifications d'une `var` capturée sont visibles par la fonction. Dans Spark, tout ce qu'une closure capture est sérialisé et envoyé aux executors.

#### Qu'est-ce que l'eta-expansion ?

La conversion automatique d'une méthode en valeur fonction, comme dans `nums.filter(isEven)`. Scala 3 la fait chaque fois qu'une méthode est utilisée là où une fonction est attendue ; Scala 2 demandait parfois un `isEven _` explicite.

#### Que sont la curryfication et l'application partielle ?

La curryfication transforme une méthode à plusieurs paramètres en une chaîne de listes à un paramètre : `def add(a: Int)(b: Int) = a + b`. Appliquer la première liste donne une fonction qui attend le reste : `val add5 = add(5)` (`add(5) _` en Scala 2). L'application partielle peut aussi fixer n'importe quels arguments avec des marqueurs : `connect("db.local", _, true)`.

#### Que sont les types fonction et la composition ?

`A => B` est un raccourci pour le trait `Function1[A, B]` (avec `Function2` et suivants pour plus de paramètres). Les fonctions se composent : `f andThen g` applique d'abord `f`, `f compose g` d'abord `g`, ce qui construit des pipelines à partir de petites étapes.

<!-- challenge -->

Le nettoyage de texte est écrit en appels imbriqués, `stripAccents(lower(trim(s)))`, répétés à de nombreux endroits avec des étapes ajoutées ou oubliées. Comment le rendre réutilisable ?

<!-- solution -->

Définir chaque étape comme une valeur fonction (`val trim: String => String = _.trim`, etc.) et les composer une seule fois : `val normalize = trim andThen lower andThen stripAccents`. Les appelants utilisent `normalize(s)`, et le pipeline vit à un seul endroit.

<!-- takeaways -->

- Les fonctions sont des valeurs de types comme `A => B`.
- Les closures capturent des variables de leur portée.
- Composez de petites fonctions avec `andThen`.

<!-- unit: Fonctions partielles -->

<!-- goals -->

- Écrire des fonctions anonymes à pattern matching et des fonctions partielles.
- Utiliser `collect` et `lift`.

<!-- concept -->

Un bloc de clauses `case` est une fonction anonyme qui confronte son argument à des motifs. Quand les cas ne couvrent pas toutes les entrées, c'est une fonction partielle : un `PartialFunction[A, B]` peut dire avec `isDefinedAt` s'il s'applique à une valeur.

Des méthodes de collection comme `collect` s'en servent pour filtrer et transformer en une seule étape, en ne gardant que les éléments qui correspondent aux cas.

<!-- example -->

```scala
val events = List(("click", 3), ("view", 10), ("click", 5))
events.collect { case ("click", n) => n }             // List(3, 5)

val parse: PartialFunction[String, Int] = {
  case s if s.nonEmpty && s.forall(_.isDigit) => s.toInt
}
parse.isDefinedAt("42")                                // true
parse.lift("abc")                                      // None
```

#### Qu'est-ce qu'une fonction partielle ?

Une fonction définie seulement pour certaines entrées, de type `PartialFunction[A, B]` et généralement écrite comme un bloc de clauses `case`. `isDefinedAt(x)` indique si elle gère `x` ; l'appeler sur d'autres entrées lève un `MatchError`.

#### En quoi `collect` diffère-t-il de `map` et `filter` ?

`collect` prend une fonction partielle et ne garde que les éléments pour lesquels elle est définie, transformés par elle : filtrage et transformation en une passe, avec du pattern matching pour extraire des valeurs. `collectFirst` renvoie le premier résultat sous forme d'`Option`.

#### Que fait `lift` ?

Elle transforme un `PartialFunction[A, B]` en fonction totale `A => Option[B]` qui renvoie `None` là où la fonction partielle n'est pas définie, ce qui évite les `MatchError`.

#### Comment décomposer des tuples dans des lambdas ?

Avec une lambda à cas, `pairs.map { case (k, v) => s"$k=$v" }`, qui fonctionne en Scala 2 et 3. Scala 3 décompose aussi automatiquement les paramètres : `pairs.map((k, v) => s"$k=$v")`.

<!-- challenge -->

Un code extrait des valeurs converties avec `results.filter(_.isRight).map(_.toOption.get)`. Comment le simplifier ?

<!-- solution -->

`results.collect { case Right(v) => v }` : une seule passe, pas de `.get`, et le motif rend l'intention explicite.

<!-- takeaways -->

- Les blocs `case` sont des fonctions à pattern matching.
- `collect` filtre et transforme en une étape.
- `lift` fait renvoyer des Options aux fonctions partielles.

### Modélisation du domaine

<!-- unit: Classes, objects et traits -->

<!-- goals -->

- Définir des classes, des objects singletons et des objects compagnons.
- Composer des comportements avec les traits et comprendre la linéarisation.

<!-- concept -->

Une classe déclare les paramètres de son constructeur dans son en-tête ; précédé de `val`, un paramètre devient un champ public. Scala n'a pas de `static` : un `object` singleton contient ce qui serait des membres statiques, et un object qui porte le même nom qu'une classe, son compagnon, peut accéder aux membres privés de la classe et héberge en général les méthodes de fabrique.

Les traits définissent des interfaces avec des implémentations facultatives et se mélangent aux classes. Quand plusieurs traits définissent la même méthode, la linéarisation fixe l'ordre, et les appels à `super` vont au trait suivant dans cet ordre.

<!-- example -->

```scala
class Account(val id: String, private var balance: BigDecimal):
  def deposit(amount: BigDecimal): Unit =
    require(amount > 0, "amount must be positive")
    balance += amount
  def current: BigDecimal = balance

object Account:
  def open(id: String): Account = Account(id, BigDecimal(0))   // factory

trait Logging:
  def log(msg: String): Unit = println(s"[${getClass.getSimpleName}] $msg")

class Loader extends Logging:
  def run(): Unit = log("loading")
```

#### Comment définir une classe avec des paramètres de constructeur ?

Les paramètres vont dans l'en-tête de la classe, qui est le constructeur primaire ; le corps de la classe s'exécute comme code du constructeur. Un paramètre devient un champ public avec `val` (ou `var`) et reste privé à la classe sinon. Les constructeurs supplémentaires s'écrivent `def this(...)`. En Scala 3, `new` est facultatif.

#### Qu'est-ce qu'un object singleton ?

Un `object` définit à la fois une classe et son unique instance, créée paresseusement à la première utilisation. Il contient des utilitaires, des constantes et des points d'entrée, et remplace les membres statiques de Java.

#### Qu'est-ce qu'un object compagnon ?

Un object qui porte le même nom qu'une classe, dans le même fichier. La classe et son compagnon accèdent mutuellement à leurs membres privés ; le compagnon contient en général les méthodes de fabrique (`apply`), les constantes et les instances given de la classe.

#### Qu'est-ce qu'un trait, et en quoi diffère-t-il d'une classe abstraite ?

Un trait définit des membres abstraits et concrets et peut être mélangé à une classe avec d'autres traits (`extends A with B`, ou `extends A, B` en Scala 3). Une classe n'étend qu'une seule classe abstraite. En Scala 3, les traits acceptent aussi des paramètres : les classes abstraites servent surtout à l'interopérabilité avec Java ou quand un constructeur est indispensable.

#### Qu'est-ce que la linéarisation des traits ?

L'ordre dans lequel Scala résout les membres quand plusieurs traits mélangés les définissent : à peu près de droite à gauche dans la clause `extends`. `super.method()` dans un trait appelle l'implémentation suivante dans cet ordre, ce qui permet des traits « empilables » qui ajoutent chacun un comportement autour de la même méthode.

#### Que font `require` et `assert` ?

`require(cond, msg)` vérifie une précondition sur les arguments et lève `IllegalArgumentException`. `assert(cond, msg)` vérifie un invariant interne et lève `AssertionError`. Les deux font échouer tôt les états invalides, avec un message clair.

#### Quels modificateurs d'accès Scala propose-t-il ?

Les membres sont publics par défaut. `private` les limite à la classe et à son compagnon, `protected` aux sous-classes, et des formes qualifiées comme `private[etl]` les ouvrent à tout un package.

<!-- challenge -->

Une classe `DateUtils` n'a aucun état, mais le code crée des `new DateUtils()` partout juste pour appeler `parse`. Comment la restructurer ?

<!-- solution -->

En faire un `object DateUtils` (ou des fonctions de premier niveau dans un fichier Scala 3), pour appeler directement `DateUtils.parse(...)` sans créer d'instances.

<!-- takeaways -->

- Les objects remplacent les membres statiques.
- Les compagnons contiennent fabriques et givens.
- Les traits mélangent des comportements aux classes.

<!-- unit: Case classes, enums et ADT -->

<!-- goals -->

- Modéliser des données avec des case classes et des enums.
- Construire des types de données algébriques avec des sealed traits et des enums.

<!-- concept -->

Les case classes sont la façon standard de modéliser des données immuables. Le compilateur génère un constructeur sans `new`, des accesseurs pour les champs, une égalité et un hachage structurels, un `toString` lisible, une méthode `copy` et la prise en charge du pattern matching.

Combinées, elles forment des types de données algébriques : un sealed trait ou un enum Scala 3 énumère tous les cas possibles, et le compilateur avertit quand un match en oublie un. Les case classes sont des types produit (« ceci et cela ») ; les enums et hiérarchies scellées sont des types somme (« ceci ou cela »).

<!-- example -->

```scala
enum Status:
  case Pending, Paid, Refunded

final case class Order(id: Long, customer: String, amount: BigDecimal, status: Status)

enum PaymentEvent:
  case Authorized(orderId: Long, amount: BigDecimal)
  case Captured(orderId: Long)
  case Failed(orderId: Long, reason: String)

val o = Order(1, "ana", BigDecimal("19.99"), Status.Pending)
val paid = o.copy(status = Status.Paid)       // new instance; o is unchanged
```

#### Qu'apporte une case class ?

Une fabrique `apply` (sans `new`), des champs publics immuables, `equals` et `hashCode` fondés sur les champs, un `toString` lisible, `copy`, un extracteur `unapply` pour le pattern matching et la sérialisation. C'est le choix par défaut pour des enregistrements de données.

#### Que fait `copy` ?

Elle crée une nouvelle instance avec certains champs modifiés et les autres conservés : `order.copy(status = Status.Paid)`. C'est ainsi qu'on « met à jour » des données immuables.

#### Pourquoi déclarer les case classes `final` ?

Étendre une case class casse subtilement l'égalité et le pattern matching générés : le style recommandé est `final case class`. Les variantes vont dans un sealed trait ou un enum à plusieurs cas.

#### Qu'est-ce qu'un enum Scala 3 ?

Un type avec un ensemble fixe de cas. Les enums simples (`case Pending, Paid`) ont `values`, `valueOf` et `ordinal` ; les cas peuvent aussi prendre des paramètres, ce qui fait des enums une façon concise d'écrire des types de données algébriques. Scala 2 exprimait la même chose avec un sealed trait et des case objects.

#### Qu'est-ce qu'un type de données algébrique ?

Un type construit à partir de produits (une case class qui combine des champs) et de sommes (un choix entre des cas). Modéliser un événement de paiement comme « autorisé, capturé ou échoué », chacun avec ses champs, rend les combinaisons invalides impossibles à représenter.

#### Que signifie `sealed` ?

Un trait ou une classe scellé ne peut être étendu que dans le même fichier : le compilateur connaît tous les sous-types et peut vérifier qu'un `match` les couvre tous.

#### Quelle est la différence entre une case class et une classe ordinaire ?

Une classe ordinaire compare par référence, n'a ni `copy` ni extracteur, et garde privés les paramètres du constructeur non marqués `val`. Utilisez des case classes pour les données, des classes ordinaires pour les objets avec une identité, un comportement et un état caché.

#### Qu'est-ce qu'un case object ?

Un singleton doté des fonctionnalités d'une case class (`toString` lisible, pattern matching, sérialisation), utilisé en Scala 2 pour les cas sans données d'une hiérarchie scellée, comme `case object Pending extends Status`.

<!-- challenge -->

Le statut d'une commande est un champ `String`, et une faute de frappe, `"payed"`, a atteint les données de production. Comment le système de types peut-il l'empêcher ?

<!-- solution -->

Modéliser le statut comme un enum (`Pending`, `Paid`, `Refunded`) et convertir les chaînes externes une seule fois, à la frontière, avec une fonction qui renvoie `Option` ou `Either` : les valeurs invalides sont rejetées là et ne peuvent pas exister plus loin.

<!-- takeaways -->

- Les case classes modélisent des données immuables.
- Enums et sealed traits énumèrent tous les cas.
- Convertissez les chaînes en types à la frontière.

<!-- unit: Pattern matching -->

<!-- goals -->

- Faire du match sur des valeurs, des types, des case classes et des collections.
- Utiliser gardes, binders et extracteurs, et s'appuyer sur la vérification d'exhaustivité.

<!-- concept -->

`match` est un switch qui décompose aussi les valeurs. Il confronte une valeur à des motifs, dans l'ordre, en liant des parties de celle-ci à des noms : littéraux, types, case classes, tuples et listes, avec des gardes pour les conditions supplémentaires.

Sur les types scellés et les enums, le compilateur vérifie l'exhaustivité et signale les cas manquants : ajouter un cas produit une liste d'avertissements à corriger plutôt que des surprises à l'exécution. Des extracteurs personnalisés (`unapply`) rendent n'importe quel type « matchable ».

<!-- example -->

```scala
def describe(e: PaymentEvent): String = e match
  case PaymentEvent.Authorized(id, amt) if amt > 1000 => s"large authorization on $id"
  case PaymentEvent.Authorized(id, _)                 => s"authorized $id"
  case PaymentEvent.Captured(id)                      => s"captured $id"
  case PaymentEvent.Failed(id, reason)                => s"failed $id: $reason"

def summary(xs: List[Int]): String = xs match
  case Nil       => "empty"
  case x :: Nil  => s"one: $x"
  case x :: rest => s"$x and ${rest.size} more"
```

#### Comment fonctionne le pattern matching en Scala ?

`value match { case pattern => result ... }` essaie chaque cas dans l'ordre et évalue le premier qui correspond, en liant les variables du motif. C'est une expression, qui renvoie donc le résultat choisi.

#### Quels types de motifs existe-t-il ?

Les littéraux (`case 0`), les variables et le joker `_`, les motifs typés (`case s: String`), les motifs de constructeur pour les case classes, les tuples (`case (k, v)`), les séquences (`case List(a, b, _*)`, `case x :: rest`), les alternatives (`case "FR" | "BE"`) et les binders qui nomment une partie reconnue (`case o @ Order(_, _, _, Status.Paid)`).

#### Qu'est-ce qu'une garde ?

Une condition `if` après un motif (`case Authorized(id, amt) if amt > 1000`). Le cas ne correspond que si le motif et la condition sont satisfaits.

#### Qu'est-ce que la vérification d'exhaustivité ?

Pour les match sur des sealed traits, des enums, `Option` et types similaires, le compilateur avertit quand un cas possible n'est pas couvert. C'est l'un des plus grands bénéfices de la modélisation par types algébriques.

#### Qu'est-ce qu'un extracteur ?

Un objet doté d'une méthode `unapply` qui décide si une valeur correspond et ce qu'il faut lier :

```scala
object Email:
  def unapply(s: String): Option[(String, String)] =
    s.split("@") match
      case Array(user, domain) => Some((user, domain))
      case _                   => None

"ana@example.com" match
  case Email(user, domain) => s"$user at $domain"
  case _                   => "not an email"
```

#### Que se passe-t-il si aucun cas ne correspond ?

Un `scala.MatchError` est levé à l'exécution. Les avertissements d'exhaustivité l'évitent pour les types scellés ; pour les types ouverts comme les chaînes, ajoutez un `case _` final.

#### Pourquoi ne peut-on pas distinguer `List[String]` de `List[Int]` dans un match ?

Les arguments de types génériques sont effacés sur la JVM : à l'exécution, les deux ne sont que des `List`. Le compilateur avertit que ce motif n'est pas vérifiable. Faites le match sur les éléments, ou conservez l'information de type avec un `ClassTag` ou un type enveloppe.

<!-- challenge -->

Un cas `Disputed` a été ajouté à `PaymentEvent`, et un rapport classe silencieusement les litiges en « autre » via une branche `case _ =>`. Comment faire détecter ces trous par le compilateur ?

<!-- solution -->

Retirer le joker des match sur les types scellés et les enums, pour que le compilateur signale que `Disputed` n'est pas géré, et faire échouer le build de CI sur les avertissements (`-Werror`).

<!-- takeaways -->

- `match` teste les motifs dans l'ordre et lie des parties.
- Les types scellés apportent la vérification d'exhaustivité.
- Évitez les jokers dans les match sur vos propres ADT.

<!-- stage: Collections et programmation fonctionnelle -->

### Collections

<!-- unit: La hiérarchie des collections -->

<!-- goals -->

- Distinguer collections immuables et mutables.
- Choisir entre `List`, `Vector`, `Array`, `Set` et `Map` selon le mode d'accès.

<!-- concept -->

Les collections Scala existent en versions immuables, celles par défaut, et mutables, dans `scala.collection.mutable`. Les collections immuables ne changent jamais : les opérations renvoient de nouvelles collections qui partagent l'essentiel de leur structure avec l'ancienne, ce qui les rend peu coûteuses à créer et sûres à partager entre threads.

Les grandes familles sont les séquences, les ensembles et les maps. Parmi les séquences, `List` est une liste chaînée rapide en tête, `Vector` offre des accès et mises à jour rapides partout, `Array` est un tableau Java mutable et `ArrayBuffer` grandit efficacement. Choisir selon le mode d'accès compte plus que toute micro-optimisation.

<!-- example -->

```scala
val xs = List(1, 2, 3)
val ys = 0 :: xs                       // O(1) prepend, shares xs
val v  = Vector(1, 2, 3).updated(1, 20) // Vector(1, 20, 3)
val m  = Map("FR" -> 10, "CO" -> 7)
val m2 = m + ("AR" -> 3)               // new map; m unchanged
m.getOrElse("DE", 0)                   // 0

import scala.collection.mutable
val buf = mutable.ArrayBuffer.empty[Int]
buf += 4                               // changes buf in place
```

#### Quelle est la différence entre collections immuables et mutables ?

Les collections immuables ne peuvent pas changer après leur création ; « ajouter » renvoie une nouvelle collection. Les mutables changent sur place. Les immuables sont la norme en Scala, car elles sont sûres à partager et plus simples à raisonner ; les mutables conviennent au code local sensible aux performances.

#### Quand utiliser `List` plutôt que `Vector` ?

`List` est rapide pour ajouter en tête, accéder à la tête et à la queue et faire du pattern matching récursif, mais l'accès par indice et l'ajout en fin sont en O(n). `Vector` accède par indice, ajoute en fin et met à jour en temps quasi constant. `Seq(...)` crée une `List`, `IndexedSeq(...)` un `Vector`.

#### Qu'est-ce qu'un `Array` en Scala ?

Un tableau Java : taille fixe, mutable et stockage compact (primitifs sans boxing). On l'utilise pour l'interopérabilité et le code sensible aux performances. `==` sur des tableaux compare les références : comparez leur contenu avec `sameElements`.

#### Comment fonctionnent les sets et les maps ?

`Set` et `Map` par défaut reposent sur un hachage et ne sont pas ordonnés ; `SortedSet` et `TreeMap` gardent les clés triées. `map(key)` lève `NoSuchElementException` si la clé manque, tandis que `map.get(key)` renvoie un `Option` et `getOrElse` une valeur par défaut.

#### Qu'est-ce que le partage structurel ?

Les collections immuables réutilisent dans la nouvelle collection les parties inchangées de l'ancienne : `0 :: xs` pointe vers `xs` au lieu de la copier, et `Vector.updated` ne copie qu'un court chemin de son arbre interne. C'est ce qui rend les mises à jour immuables abordables.

#### Quelle est la complexité des opérations courantes sur `List` ?

`head`, `tail` et l'ajout en tête (`::`) sont en O(1). `length`, l'accès par indice avec `apply`, `last` et l'ajout en fin (`:+`) sont en O(n), car il faut parcourir la liste.

#### Qu'est-ce que `Seq` en Scala 2.13 et 3 ?

`scala.Seq` est un alias de `scala.collection.immutable.Seq`. En Scala 2.12, c'était `scala.collection.Seq`, qui pouvait aussi être mutable, source fréquente d'erreurs de compilation lors de la migration de code qui passe des tableaux ou des buffers comme `Seq`.

<!-- challenge -->

Un job construit une `List` en ajoutant en fin dans une boucle, `acc = acc :+ row`, sur un million de lignes, et prend des minutes. Que changez-vous ?

<!-- solution -->

Chaque `:+` recopie toute la liste, ce qui rend la boucle O(n²). Ajoutez en tête puis inversez une fois à la fin, utilisez un `ListBuffer` ou un builder, ou mieux, exprimez la boucle comme un `map` ou un `filter` sur la source.

<!-- takeaways -->

- Les collections immuables sont la norme.
- `List` est rapide en tête ; `Vector` partout.
- Les tableaux sont des tableaux Java mutables.

<!-- unit: Transformer des collections -->

<!-- goals -->

- Appliquer `map`, `flatMap`, `filter`, les folds et les regroupements.
- Choisir la bonne méthode pour une agrégation.

<!-- concept -->

Les collections partagent un large ensemble de méthodes de transformation. `map` transforme chaque élément, `filter` en garde certains, `flatMap` transforme et aplatit, et les folds combinent tout en une seule valeur. Les méthodes de regroupement découpent une collection par clé, l'équivalent en mémoire du `GROUP BY` de SQL.

Enchaîner ces méthodes remplace la plupart des boucles par du code qui dit ce qu'est le résultat, et le même vocabulaire se retrouve dans Spark, `Option`, `Future` et les bibliothèques d'effets.

<!-- example -->

```scala
final case class Sale(country: String, product: String, amount: Double)
val sales = List(Sale("FR", "a", 10), Sale("CO", "b", 5), Sale("FR", "b", 7))

val byCountry = sales.groupMapReduce(_.country)(_.amount)(_ + _)   // Map(FR -> 17.0, CO -> 5.0)
val total = sales.foldLeft(0.0)((acc, s) => acc + s.amount)        // 22.0
val (big, small) = sales.partition(_.amount >= 7)
val top = sales.sortBy(-_.amount).take(2)
```

#### Quelle est la différence entre `map` et `flatMap` ?

`map` applique une fonction à chaque élément et conserve la structure : `List(1, 2).map(x => List(x, x))` donne `List(List(1, 1), List(2, 2))`. `flatMap` applique une fonction qui renvoie une collection et aplatit les résultats : `List(1, 1, 2, 2)`.

#### Quelle est la différence entre `foldLeft`, `foldRight` et `reduce` ?

`foldLeft(init)(op)` combine les éléments de gauche à droite à partir d'une valeur initiale et fonctionne sur une collection vide. `foldRight` va de droite à gauche. `reduce` part du premier élément et échoue sur une collection vide : `reduceOption` est plus sûr.

#### En quoi `groupBy`, `groupMap` et `groupMapReduce` diffèrent-ils ?

`groupBy(key)` renvoie une `Map` de chaque clé vers les éléments qui la portent. `groupMap(key)(f)` transforme aussi chaque élément. `groupMapReduce(key)(f)(op)` transforme et combine en une seule passe, sans construire de listes intermédiaires : la façon efficace de sommer ou compter par clé.

#### Que font `partition`, `span` et `splitAt` ?

`partition(p)` sépare les éléments qui satisfont `p` de ceux qui ne le satisfont pas. `span(p)` coupe au premier élément qui échoue `p`. `splitAt(n)` coupe à une position. Toutes renvoient une paire de collections.

#### Que font `zip`, `zipWithIndex` et `sliding` ?

`zip` associe les éléments de deux collections (en s'arrêtant à la plus courte), `zipWithIndex` associe chaque élément à sa position, et `sliding(n)` parcourt des fenêtres chevauchantes de `n` éléments, utiles pour les moyennes mobiles et les comparaisons avec l'élément précédent.

#### Comment trier des collections ?

`sorted` utilise l'`Ordering` du type des éléments, `sortBy(f)` trie selon une clé et `sortWith(lt)` prend une comparaison. Les tuples trient sur plusieurs clés (`sortBy(s => (s.country, -s.amount))`), et `Ordering.by` et `.reverse` construisent des ordres personnalisés.

#### Que font `exists`, `forall`, `find` et `count` ?

`exists(p)` est vrai si un élément satisfait `p`, `forall(p)` si tous le font (vrai pour une collection vide), `find(p)` renvoie la première correspondance sous forme d'`Option` et `count(p)` compte les correspondances. Les trois premières s'arrêtent dès que la réponse est connue.

#### Comptez la fréquence des mots d'un texte et renvoyez les n plus fréquents.

```scala
def topWords(text: String, n: Int): List[(String, Int)] =
  text.toLowerCase
    .split("\\W+").toList
    .filter(_.nonEmpty)
    .groupMapReduce(identity)(_ => 1)(_ + _)
    .toList
    .sortBy((word, count) => (-count, word))
    .take(n)
```

<!-- challenge -->

`orders.groupBy(_.customer).map((c, os) => c -> os.map(_.amount).sum)` manque de mémoire sur 50 millions de commandes. Que changez-vous ?

<!-- solution -->

`groupBy` construit une liste complète de commandes par client avant de sommer. `orders.groupMapReduce(_.customer)(_.amount)(_ + _)` agrège en une passe et ne garde qu'un total courant par client.

<!-- takeaways -->

- `map` conserve la structure ; `flatMap` aplatit.
- Préférez `foldLeft` et `reduceOption` à `reduce`.
- `groupMapReduce` agrège par clé en une passe.

<!-- unit: Collections paresseuses et itérateurs -->

<!-- goals -->

- Éviter les collections intermédiaires avec les views, les itérateurs et `LazyList`.
- Traiter de gros fichiers à mémoire constante.

<!-- concept -->

Les collections strictes calculent chaque étape en entier : `xs.map(f).filter(p).take(10)` construit deux collections intermédiaires complètes. Une view rend la chaîne paresseuse et ne calcule que les éléments nécessaires. Un itérateur délivre les éléments un par un et ne se parcourt qu'une fois, ce qui convient aux fichiers et aux flux. Une `LazyList` calcule les éléments à la demande, les mémorise et peut être infinie.

<!-- example -->

```scala
import scala.io.Source
import scala.util.Using

val firstErrors: List[String] = Using.resource(Source.fromFile("app.log")) { src =>
  src.getLines().filter(_.contains("ERROR")).take(5).toList
}

val firstHits = (1 to 1_000_000).view.map(_ * 3).filter(_ % 7 == 0).take(3).toList
val fibs: LazyList[BigInt] = BigInt(0) #:: BigInt(1) #:: fibs.zip(fibs.tail).map((a, b) => a + b)
fibs.take(10).toList                  // List(0, 1, 1, 2, 3, 5, 8, 13, 21, 34)
```

#### Qu'est-ce qu'une view ?

Une enveloppe paresseuse sur une collection (`xs.view`) : les transformations sont enregistrées et appliquées élément par élément seulement quand un résultat est demandé, par exemple avec `toList` ou `sum`. Elle évite de construire des collections intermédiaires dans les longues chaînes.

#### Quelle est la différence entre un `Iterator` et un `Iterable` ?

Un `Iterable` (comme une `List`) peut être parcouru plusieurs fois. Un `Iterator` délivre des éléments avec `hasNext` et `next` et s'épuise après une passe : appeler `size` dessus le consomme. Des méthodes comme `getLines()` renvoient des itérateurs.

#### Qu'est-ce que `LazyList` ?

Une séquence paresseuse et mémoïsée qui peut être infinie, construite avec `#::`. Elle a remplacé le `Stream` déprécié en Scala 2.13. Garder une référence vers sa tête conserve en mémoire tous les éléments déjà calculés.

#### Comment lire un gros fichier ligne par ligne ?

Parcourez `Source.fromFile(path).getLines()` (ou `java.nio.file.Files.lines`) dans un `Using`, en transformant et en repliant l'itérateur sans le convertir en liste : une seule ligne est en mémoire à la fois et le fichier est fermé à la fin.

#### Comment traiter des éléments par lots ?

`iterator.grouped(1000)` délivre des lots de 1 000 éléments (le dernier peut être plus court), et `sliding(n, step)` des fenêtres. Sur un itérateur, les deux restent paresseux, ce qui convient aux insertions en masse ou aux appels d'API par paquets.

<!-- challenge -->

`Source.fromFile(path).getLines().toList.filter(isError)` plante avec `OutOfMemoryError` sur un log de 20 Go. Que changez-vous ?

<!-- solution -->

Garder un itérateur : supprimer `toList`, filtrer et compter ou écrire les résultats au fil de l'eau, et envelopper la source dans `Using` pour fermer le fichier. La mémoire reste alors constante, quelle que soit la taille du fichier.

<!-- takeaways -->

- Les views évitent les collections intermédiaires.
- Les itérateurs se consomment une fois et traitent les données en flux.
- Ne faites jamais `toList` d'un fichier qui ne tient pas en mémoire.

<!-- unit: Exercices sur les collections -->

<!-- goals -->

- Résoudre des exercices de code classiques avec les collections Scala.
- Choisir entre méthodes de collection, folds et mutation locale.

<!-- concept -->

Les exercices de code en Scala vérifient que vous pensez en transformations. La plupart ont une solution courte avec des méthodes de collection : dédoublonner avec `distinct` ou une map indexée par ID, two-sum avec une map des valeurs vues, intervalles avec un tri et un fold. Dans une fonction, une mutation locale comme une map mutable ou un builder est acceptable quand elle est plus rapide et ne s'échappe pas.

<!-- example -->

```scala
final case class Row(id: String, ts: Long, value: String)

def latestById(rows: Seq[Row]): Iterable[Row] =
  rows.groupMapReduce(_.id)(identity)((a, b) => if a.ts >= b.ts then a else b).values
```

#### Trouvez les deux nombres d'une séquence dont la somme vaut une cible (two-sum).

Utilisez une map des valeurs déjà vues, en O(n) :

```scala
def twoSum(nums: Vector[Int], target: Int): Option[(Int, Int)] =
  val seen = collection.mutable.HashMap.empty[Int, Int]   // local mutation, never shared
  nums.indices.iterator.flatMap { i =>
    val hit = seen.get(target - nums(i)).map(j => (j, i))
    seen(nums(i)) = i
    hit
  }.nextOption()
```

#### Comment supprimer les doublons en conservant l'ordre ?

`xs.distinct` garde la première occurrence de chaque élément, et `xs.distinctBy(_.id)` (2.13+) la première de chaque clé. Les deux conservent l'ordre d'origine.

#### Fusionnez des intervalles qui se chevauchent.

```scala
def merge(intervals: List[(Int, Int)]): List[(Int, Int)] =
  intervals.sortBy(_._1).foldLeft(List.empty[(Int, Int)]) {
    case ((s0, e0) :: rest, (s, e)) if s <= e0 => (s0, e0.max(e)) :: rest
    case (acc, interval)                       => interval :: acc
  }.reverse
```

#### Regroupez une liste de mots en anagrammes.

```scala
def groupAnagrams(words: List[String]): List[List[String]] =
  words.groupBy(_.sorted).values.toList
```

#### Vérifiez si une chaîne de parenthèses est équilibrée.

```scala
def balanced(s: String): Boolean =
  val pairs = Map(')' -> '(', ']' -> '[', '}' -> '{')
  s.foldLeft(Option(List.empty[Char])) {
    case (Some(stack), c) if "([{".contains(c)                  => Some(c :: stack)
    case (Some(top :: rest), c) if pairs.get(c).contains(top) => Some(rest)
    case (Some(_), c) if pairs.contains(c)                      => None
    case (acc, _)                                               => acc
  }.contains(Nil)
```

#### Trouvez le premier caractère non répété d'une chaîne.

```scala
def firstUnique(s: String): Option[Char] =
  val counts = s.groupMapReduce(identity)(_ => 1)(_ + _)
  s.find(c => counts(c) == 1)
```

#### Calculez un total cumulé et une moyenne mobile sur 3 éléments.

```scala
val values = List(3, 5, 2, 8, 6)
val running = values.scanLeft(0)(_ + _).tail                    // List(3, 8, 10, 18, 24)
val moving = values.sliding(3).map(w => w.sum / 3.0).toList     // List(3.33, 5.0, 5.33)
```

<!-- challenge -->

Une solution teste `if !result.contains(x)` sur une `List` qui grandit, pour chacun d'un million d'éléments, et prend des minutes. Que changez-vous ?

<!-- solution -->

`contains` sur une `List` est en O(n), donc la boucle est en O(n²). Mémorisez les éléments vus dans un `Set` (appartenance en O(1)), ou utilisez `distinct`, qui fait exactement cela.

<!-- takeaways -->

- La plupart des exercices tiennent en quelques méthodes de collection.
- Maps et sets transforment des recherches O(n²) en O(n).
- La mutation locale est acceptable si elle ne s'échappe pas.

### Programmation fonctionnelle

<!-- unit: Immuabilité et fonctions pures -->

<!-- goals -->

- Expliquer fonctions pures, transparence référentielle et effets de bord.
- Garder les effets de bord en bordure du programme.

<!-- concept -->

Une fonction pure renvoie la même sortie pour la même entrée et ne fait rien d'autre : pas de mutation, pas d'E/S, pas d'exceptions comme flux de contrôle. Le code pur est facile à tester, à raisonner, à mettre en cache et à exécuter en parallèle : c'est pourquoi la programmation fonctionnelle construit les programmes à partir de fonctions pures sur des données immuables.

Les vrais programmes lisent pourtant des fichiers et appellent des API. L'approche fonctionnelle repousse ces effets en bordure, un « cœur fonctionnel, coque impérative », ou les décrit comme des valeurs exécutées plus tard, comme le font les bibliothèques d'effets.

<!-- example -->

```scala
// impure: depends on the clock and mutates shared state
var processed = 0
def stampImpure(o: Order): String =
  processed += 1
  s"${o.id}@${System.currentTimeMillis}"

// pure: everything it needs comes in as parameters
def stamp(o: Order, now: Long): String = s"${o.id}@$now"
```

#### Qu'est-ce que la programmation fonctionnelle ?

Un style qui construit les programmes à partir de fonctions pures et de valeurs immuables, traite les fonctions comme des valeurs et gère explicitement erreurs et effets dans les types. Scala la prend en charge à côté de la programmation orientée objet, et la plupart du code Scala mêle les deux.

#### Qu'est-ce qu'une fonction pure ?

Une fonction dont le résultat ne dépend que de ses arguments et qui n'a pas d'effet de bord observable. `def add(a: Int, b: Int) = a + b` est pure ; une fonction qui lit l'horloge, écrit des logs ou modifie un champ ne l'est pas.

#### Qu'est-ce que la transparence référentielle ?

Une expression est référentiellement transparente si on peut la remplacer par sa valeur sans changer le comportement du programme. Les fonctions pures ont cette propriété, qui sécurise le refactoring, la mise en cache et le raisonnement sur le code.

#### Que sont les effets de bord, et comment les gérer ?

Tout ce que fait une fonction en plus de renvoyer une valeur : E/S, mutation, exceptions, lecture de l'heure ou de nombres aléatoires. Gardez-les dans une fine couche externe, passez en paramètre des entrées comme l'heure courante, et utilisez des types d'effet comme `IO` quand il faut les composer.

#### Pourquoi l'immuabilité aide-t-elle la concurrence ?

Des données immuables se partagent entre threads sans verrous, puisque personne ne peut les modifier ; les conditions de course exigent un état mutable partagé. Elle rend aussi plus sûrs les closures Spark et les caches.

#### La mutation est-elle parfois acceptable en Scala ?

Oui, quand elle est locale et ne s'échappe pas : une `var` ou un builder mutable dans une fonction qui renvoie un résultat immuable, ou une boucle serrée où les performances comptent. Vue de l'extérieur, la fonction reste pure.

<!-- challenge -->

Une transformation lit `LocalDate.now()` en interne, et ses tests échouent chaque nuit vers minuit. Comment corriger ?

<!-- solution -->

Passer la date (ou une `java.time.Clock`) en paramètre pour que la fonction soit pure : le code de production passe la date du jour, les tests une date fixe.

<!-- takeaways -->

- Les fonctions pures ne dépendent que de leurs entrées.
- Repoussez les effets en bordure.
- La mutation locale est acceptable si elle ne s'échappe pas.

<!-- unit: Option, Either et Try -->

<!-- goals -->

- Remplacer `null` et les exceptions par `Option`, `Either` et `Try`.
- Enchaîner des résultats et rassembler les erreurs de validation.

<!-- concept -->

Au lieu de `null` et d'exceptions levées, Scala représente « peut manquer » par `Option` (`Some` ou `None`), « succès ou échec expliqué » par `Either` (`Right` ou `Left`) et « un calcul qui peut lever une exception » par `Try` (`Success` ou `Failure`). Les types rendent les échecs visibles dans les signatures, et l'appelant doit s'en occuper.

Tous trois prennent en charge `map`, `flatMap`, `getOrElse` et les compréhensions `for` : on enchaîne des étapes, et le premier échec court-circuite le reste.

<!-- example -->

```scala
import scala.util.Try

def parseAmount(raw: String): Either[String, BigDecimal] =
  Try(BigDecimal(raw.trim)).toEither.left.map(_ => s"bad amount: '$raw'")

def findCustomer(id: String): Option[Customer] = customers.get(id)

val invoice: Either[String, Invoice] = for
  amount   <- parseAmount(row("amount"))
  customer <- findCustomer(row("customer")).toRight(s"unknown customer ${row("customer")}")
yield Invoice(customer, amount)
```

#### Qu'est-ce qu'`Option`, et pourquoi l'utiliser plutôt que `null` ?

Un conteneur qui vaut `Some(value)` ou `None`. Le type dit qu'une valeur peut manquer, et le compilateur oblige l'appelant à le gérer, tandis que `null` est invisible dans les types et échoue plus tard avec une `NullPointerException`.

#### Comment extraire une valeur d'un `Option` en sécurité ?

Avec `getOrElse(default)`, `fold`, `map` et `flatMap` pour continuer à travailler à l'intérieur, ou un `match`. Évitez `.get`, qui lève une exception sur `None` et ramène le problème qu'`Option` résout.

#### Qu'est-ce qu'`Either` ?

Une valeur qui vaut `Left(error)` ou `Right(result)`. Il est biaisé à droite : `map` et `flatMap` agissent sur le côté `Right` et laissent passer un `Left`. On l'utilise pour les opérations qui peuvent échouer avec une erreur explicite.

#### Qu'est-ce que `Try` ?

Une enveloppe pour du code qui peut lever une exception : `Try(expr)` donne `Success(value)` ou `Failure(exception)`. On l'utilise surtout à la frontière avec des bibliothèques qui lèvent des exceptions, puis on convertit avec `toOption` ou `toEither`.

#### Quand utiliser `Option`, `Either` ou `Try` ?

`Option` quand l'absence est normale et n'a pas besoin d'explication (une recherche). `Either` quand l'appelant doit savoir pourquoi cela a échoué (validation, conversion avec messages). `Try` pour capturer les exceptions d'un code que vous ne contrôlez pas.

#### Comment gérer le `null` venant des API Java ?

Enveloppez la valeur à la frontière : `Option(javaValue)` transforme `null` en `None`. Scala 3 propose aussi un mode facultatif de nulls explicites, où les types référence n'acceptent pas null et où les résultats Java sont typés `T | Null`.

#### Comment rassembler toutes les erreurs de validation au lieu de s'arrêter à la première ?

`Either` dans une compréhension `for` s'arrête au premier `Left`. Pour toutes les garder, validez chaque élément et séparez les résultats avec `partitionMap`, ou utilisez un type accumulateur comme `ValidatedNel` de Cats :

```scala
val (errors, amounts) = rows.partitionMap(r => parseAmount(r("amount")))
```

<!-- challenge -->

Un parser renvoie `null` sur une entrée invalide, et des `NullPointerException` apparaissent loin du parser. Comment corriger la conception ?

<!-- solution -->

Renvoyer `Option` (ou `Either` avec un message d'erreur) depuis le parser, pour que chaque appel gère l'échec là où il se produit, sous le contrôle du compilateur.

<!-- takeaways -->

- `Option` pour l'absence, `Either` pour les erreurs, `Try` pour les exceptions.
- Enchaînez avec `map`, `flatMap` et les compréhensions `for`.
- N'appelez jamais `.get` sur un `Option`.

<!-- unit: Compréhensions for -->

<!-- goals -->

- Lire et écrire des compréhensions `for` et leur traduction.
- Les utiliser avec les collections, `Option`, `Either` et `Future`.

<!-- concept -->

Une compréhension `for` est une syntaxe au-dessus de `flatMap`, `map` et `withFilter`. Chaque générateur (`<-`) est une étape, et `yield` construit le résultat. Comme ce ne sont que des appels de méthodes, elle fonctionne avec tout type qui les définit : collections, `Option`, `Either`, `Try`, `Future` et types d'effet.

Le type du premier générateur détermine le type du résultat : des types sans rapport comme `Option` et `Future` ne se mélangent pas dans une même compréhension sans conversion préalable.

<!-- example -->

```scala
val pairs = for
  x <- List(1, 2, 3)
  if x % 2 == 1
  y <- List("a", "b")
yield (x, y)
// List((1,a), (1,b), (3,a), (3,b)), the same as:
List(1, 2, 3).withFilter(_ % 2 == 1).flatMap(x => List("a", "b").map(y => (x, y)))
```

#### Qu'est-ce qu'une compréhension `for` ?

Une syntaxe pour enchaîner des opérations sur des valeurs qui prennent en charge `map` et `flatMap` : générateurs (`x <- xs`), filtres (`if cond`) et définitions de valeurs (`y = f(x)`), suivis de `yield`. Elle se lit comme une suite d'étapes.

#### Comment une compréhension `for` est-elle traduite ?

Chaque générateur sauf le dernier devient un `flatMap`, le dernier un `map` avec l'expression du `yield`, et les filtres `if` deviennent `withFilter`. Une compréhension avec `do` au lieu de `yield` devient des appels à `foreach`.

#### Peut-on mélanger `Option`, `List` et `Future` dans une compréhension `for` ?

Pas directement : les étapes doivent partager un type qu'on peut aplatir. Convertissez d'abord (`option.toRight(error)`, `Future.fromTry`, `opt.toList`), ou utilisez des monad transformers ou des bibliothèques d'effets conçues pour les combiner.

#### Qu'a changé « better fors » dans Scala 3.8 ?

La SIP-62, activée par défaut depuis 3.8, permet à une compréhension de commencer par un alias (`x = ...`), traduit les alias sans construire de tuples intermédiaires et supprime le `map` final quand `yield` ne renvoie que la dernière valeur liée. La traduction est plus simple et moins coûteuse, ce qui compte surtout pour les types d'effet.

#### Qu'est-ce qu'une monade, concrètement ?

Un type doté de `flatMap` et d'un moyen d'envelopper une valeur simple (`Some(x)`, `List(x)`, `Future.successful(x)`, `IO.pure(x)`) qui respecte quelques lois. En pratique, c'est tout ce qu'on peut enchaîner dans une compréhension `for`, chaque étape dépendant de la précédente.

<!-- challenge -->

Une fonction de conversion imbrique quatre appels à `flatMap` sur des valeurs `Either`, et personne n'arrive à la lire. Comment la réécrire ?

<!-- solution -->

En compréhension `for`, avec un générateur par étape (`a <- parseA(raw)`, `b <- parseB(a)`, ...) et un `yield` qui construit le résultat. La sémantique est identique, et les étapes se lisent de haut en bas.

<!-- takeaways -->

- `for`/`yield`, c'est `flatMap`, `map` et `withFilter`.
- Elle fonctionne avec tout type qui les définit.
- Le premier générateur détermine le type du résultat.

<!-- unit: Récursion et appels terminaux -->

<!-- goals -->

- Écrire des fonctions récursives sur des listes.
- Rendre la récursion sûre pour la pile avec `@tailrec` et des accumulateurs.

<!-- concept -->

La récursion reflète les données récursives : une `List` est vide ou c'est une tête suivie d'une autre liste. Chaque appel récursif utilise un cadre de pile : une récursion profonde sur la JVM lève `StackOverflowError`.

Quand l'appel récursif est la dernière action d'une méthode (position terminale), le compilateur Scala le transforme en boucle, et `@tailrec` fait échouer la compilation s'il ne le peut pas. Les folds empaquettent déjà la plupart de ces boucles.

<!-- example -->

```scala
import scala.annotation.tailrec

def sum(xs: List[Long]): Long =
  @tailrec
  def loop(rest: List[Long], acc: Long): Long = rest match
    case Nil       => acc
    case h :: tail => loop(tail, acc + h)
  loop(xs, 0L)
```

#### Qu'est-ce que la récursion terminale ?

Un appel récursif qui est la dernière opération d'une méthode : il ne reste rien à faire à son retour. `loop(tail, acc + h)` est en position terminale ; `h + sum(tail)` ne l'est pas, car l'addition a lieu après l'appel.

#### Que fait `@tailrec` ?

Elle demande au compilateur de vérifier qu'une méthode est récursive terminale et compilée en boucle ; sinon la compilation échoue. Elle n'active pas l'optimisation (le compilateur la fait de toute façon), mais la garantit.

#### Pourquoi la JVM n'optimise-t-elle pas tous les appels terminaux ?

La JVM n'a pas d'élimination générale des appels terminaux. Scala n'optimise que les appels d'une méthode à elle-même, dans des méthodes non redéfinissables (locales, `private` ou `final`). Les fonctions mutuellement récursives ont besoin de trampolines, comme `scala.util.control.TailCalls`, ou d'une bibliothèque d'effets.

#### Quand utiliser un fold plutôt qu'une récursion explicite ?

Chaque fois que la récursion ne fait que parcourir une collection en accumulant un résultat : `foldLeft` est déjà une boucle sûre pour la pile et exprime l'intention. La récursion explicite est plus claire pour les arbres, les sorties anticipées ou plusieurs accumulateurs.

#### Inversez une liste de façon récursive.

```scala
import scala.annotation.tailrec

def reverse[A](xs: List[A]): List[A] =
  @tailrec def loop(rest: List[A], acc: List[A]): List[A] = rest match
    case Nil    => acc
    case h :: t => loop(t, h :: acc)
  loop(xs, Nil)
```

<!-- challenge -->

`def count(xs: List[Int]): Int = if xs.isEmpty then 0 else 1 + count(xs.tail)` échoue avec `StackOverflowError` sur 100 000 éléments. Comment corriger ?

<!-- solution -->

Porter le compte dans un accumulateur pour que l'appel récursif soit en position terminale, et annoter le helper avec `@tailrec` ; ou simplement utiliser `xs.size` ou un fold.

<!-- takeaways -->

- Chaque appel non terminal utilise un cadre de pile.
- `@tailrec` garantit une boucle.
- Les folds remplacent la plupart des récursions explicites.

<!-- stage: Types et abstractions -->

### Le système de types

<!-- unit: Génériques et variance -->

<!-- goals -->

- Écrire des classes et méthodes génériques avec des bornes de type.
- Expliquer la covariance, la contravariance et l'effacement de types.

<!-- concept -->

Les génériques permettent à une définition de fonctionner pour de nombreux types tout en restant sûre : `List[A]`, `def first[A](xs: List[A]): Option[A]`. Les bornes restreignent les paramètres de type : `A <: Animal` exige un sous-type, `B >: A` un supertype.

La variance indique comment le sous-typage du paramètre se reporte sur le conteneur. Les conteneurs immuables sont en général covariants (`List[+A]` : une liste de chats est une liste d'animaux). Les types qui consomment des valeurs sont contravariants (`-A`) : ce qui accepte n'importe quel animal convient là où il faut accepter des chats. Les conteneurs mutables doivent être invariants.

<!-- example -->

```scala
sealed trait Animal { def name: String }
final case class Cat(name: String) extends Animal
final case class Dog(name: String) extends Animal

val cats: List[Cat] = List(Cat("Tom"))
val animals: List[Animal] = cats                    // OK: List is covariant
val mixed: List[Animal] = cats :+ Dog("Rex")        // OK, via a lower bound

trait Sink[-A]:                                     // contravariant: consumes A
  def write(a: A): Unit
val animalSink: Sink[Animal] = a => println(a.name)
val catSink: Sink[Cat] = animalSink                 // OK
```

#### Que sont les génériques en Scala ?

Des classes, traits et méthodes avec des paramètres de type entre crochets (`class Box[A]`, `def first[A](xs: List[A])`), pour que le même code fonctionne avec n'importe quel type tandis que le compilateur vérifie chaque utilisation.

#### Que sont les bornes supérieures et inférieures de type ?

`A <: Upper` restreint `A` aux sous-types de `Upper`, si bien que le code peut utiliser les membres de `Upper`. `B >: Lower` restreint `B` aux supertypes de `Lower`, en général pour élargir un type quand on ajoute des éléments à une collection covariante.

#### Qu'est-ce que la covariance ?

`Container[+A]` signifie que si `Cat` est un sous-type d'`Animal`, `Container[Cat]` est un sous-type de `Container[Animal]`. C'est sûr pour les types qui ne font que produire des valeurs `A`, comme les collections immuables, `Option` et `Future`.

#### Qu'est-ce que la contravariance ?

`Container[-A]` inverse la relation : `Sink[Animal]` est un sous-type de `Sink[Cat]`. Elle convient aux types qui ne font que consommer des `A`, comme les paramètres de fonctions (`Function1[-A, +B]`), les encoders ou les writers.

#### Pourquoi `Array` est-il invariant alors que `List` est covariant ?

Un `Array` est mutable. Si un `Array[Cat]` était un `Array[Animal]`, on pourrait y ranger un `Dog` via la vue « animaux » et casser le tableau de chats. Une `List` immuable ne peut pas changer : traiter une liste de chats comme une liste d'animaux est sûr.

#### Pourquoi `:+` sur une `List[Cat]` accepte-t-il un `Dog` ?

Sa signature est `def :+[B >: A](elem: B): List[B]` : la borne inférieure permet au compilateur d'élargir le type des éléments à un supertype commun, si bien qu'ajouter un `Dog` à une `List[Cat]` renvoie une `List[Animal]`.

#### Qu'est-ce que l'effacement de types ?

Sur la JVM, les arguments de types génériques disparaissent à l'exécution : une `List[Int]` et une `List[String]` ne sont toutes deux que des `List`. Le code qui a besoin de la classe à l'exécution, par exemple pour créer un `Array[A]`, demande un `ClassTag[A]`.

<!-- challenge -->

Vous déclarez `class Box[+A](var value: A)`, et le compilateur refuse. Pourquoi ?

<!-- solution -->

Une `var` a un setter qui reçoit un `A`, une position contravariante. Si cela compilait, une `Box[Cat]` vue comme `Box[Animal]` pourrait recevoir un `Dog`. Faites du champ une `val` pour garder la boîte covariante, ou laissez-la invariante si elle doit être mutable.

<!-- takeaways -->

- Les bornes restreignent les paramètres de type.
- Producteurs covariants ; consommateurs contravariants.
- Les conteneurs mutables sont invariants.

<!-- unit: Types union, intersection et opaques -->

<!-- goals -->

- Utiliser les types union et intersection de Scala 3.
- Créer des types métier sans coût avec les types opaques, et utiliser les tuples nommés.

<!-- concept -->

Scala 3 ajoute des types auparavant difficiles à exprimer. Une union `A | B` contient une valeur de l'un ou l'autre type, sans l'envelopper dans un `Either` ou un sealed trait. Une intersection `A & B` possède les membres des deux et remplace le `A with B` de Scala 2.

Un type opaque donne un nouveau nom à un type existant que seule sa portée de définition voit en transparence : un `CustomerId` est un `String` à l'exécution, mais le code extérieur ne peut pas le confondre avec un `OrderId` ou une chaîne quelconque, et il n'y a aucun coût d'enveloppe. Les tuples nommés, stables depuis 3.7, nomment les éléments d'un tuple sans déclarer de case class.

<!-- example -->

```scala
object ids:
  opaque type CustomerId = String
  object CustomerId:
    def apply(s: String): CustomerId = s
  extension (id: CustomerId) def value: String = id

import ids.*
def load(id: CustomerId): Unit = ()
load(CustomerId("c-42"))           // compiles
// load("c-42")                    // doesn't compile: a String is not a CustomerId

def parse(raw: String): Int | String = raw.toIntOption.getOrElse(raw)

val stats = (rows = 1200, errors = 3)    // named tuple
stats.rows                               // 1200
```

#### Qu'est-ce qu'un type union ?

`A | B` est le type des valeurs qui sont soit `A`, soit `B`, comme `Int | String`. On utilise la valeur en faisant un match sur son type. Contrairement à `Either`, il n'y a ni enveloppe ni sens gauche/droite, et l'ordre des types n'importe pas.

#### Qu'est-ce qu'un type intersection ?

`A & B` est le type des valeurs qui sont à la fois `A` et `B`, avec les membres des deux. Un paramètre de type `Closeable & Flushable` accepte tout objet qui implémente les deux interfaces. Il remplace les types composés `A with B` de Scala 2.

#### Qu'est-ce qu'un type opaque ?

Un alias de type transparent uniquement dans la portée qui le définit : `opaque type CustomerId = String`. À l'extérieur, c'est un type distinct qu'on ne peut pas mélanger avec d'autres chaînes, mais à l'exécution ce n'est qu'un `String`, sans allocation. Son object compagnon et ses méthodes d'extension définissent ce qu'on peut en faire.

#### Comment les types opaques se comparent-ils aux value classes ?

Les value classes de Scala 2 (`class CustomerId(val value: String) extends AnyVal`) évitent aussi les enveloppes, mais font du boxing dans de nombreux cas : collections, génériques et pattern matching. Les types opaques ne font jamais de boxing et remplacent donc les value classes en Scala 3.

#### Que sont les tuples nommés ?

Des tuples dont les éléments ont des noms : `(rows = 1200, errors = 3)`, de type `(rows: Int, errors: Int)`. On accède aux éléments par leur nom, et un tuple nommé peut s'utiliser là où un tuple ordinaire est attendu. Ils conviennent aux résultats légers sans déclarer de case class.

#### Qu'est-ce qu'un alias de type ?

`type Row = Map[String, String]` donne un nom plus court à un type existant. Ce n'est qu'un nom : un `Row` et une `Map[String, String]` sont interchangeables, contrairement à un type opaque, qui ajoute la sûreté de typage.

#### Quand utiliser un type union plutôt qu'`Either` ?

Une union convient quand les deux possibilités sont des valeurs également valides, comme un champ qui est un `Int` ou un `String`. `Either` convient quand un côté est une erreur, car il porte le sens succès/échec et prend en charge `map`, `flatMap` et les compréhensions `for`.

<!-- challenge -->

Des fonctions prennent `customerId: String, orderId: String`, et les appelants les inversent régulièrement. Comment l'empêcher à la compilation, sans coût à l'exécution ?

<!-- solution -->

Définir `opaque type CustomerId = String` et `opaque type OrderId = String` avec des constructeurs intelligents, et changer les signatures. Les arguments inversés ne compilent plus, et les deux restent de simples chaînes à l'exécution.

<!-- takeaways -->

- `A | B` est l'un ou l'autre ; `A & B` les deux.
- Les types opaques apportent la sûreté sans enveloppe.
- Les tuples nommés nomment des résultats légers.

### Abstractions contextuelles

<!-- unit: Givens et clauses using -->

<!-- goals -->

- Passer un contexte avec des clauses `using` et le fournir avec des instances `given`.
- Importer des givens, les invoquer et transposer les implicits de Scala 2 en Scala 3.

<!-- concept -->

Certains paramètres relèvent du contexte plutôt que des données : un execution context, une configuration, un ordre de tri. Les passer explicitement à chaque appel est du bruit. Scala 3 permet à une méthode de les déclarer dans une clause `using`, et le compilateur les remplit avec les instances `given` présentes dans la portée, selon leur type.

C'est la refonte en Scala 3 des implicits de Scala 2. Les givens définissent des instances, les clauses `using` les consomment, et les givens s'importent explicitement avec `import x.given` : on sait d'où ils viennent.

<!-- example -->

```scala
final case class Config(env: String, batchSize: Int)

def load(path: String)(using cfg: Config): String =
  s"loading $path in ${cfg.env} with batches of ${cfg.batchSize}"

given Config = Config("dev", 500)
load("s3://lake/orders")                               // Config passed automatically
load("s3://lake/orders")(using Config("prod", 5000))   // or explicitly
```

#### Quel problème résolvent les givens et les clauses `using` ?

Ils transmettent des valeurs de contexte (configuration, execution contexts, instances de type classes) sans les écrire à chaque appel, tout en gardant la dépendance visible dans les signatures et résolue à la compilation.

#### Qu'est-ce qu'une instance given ?

Une valeur déclarée avec `given` que le compilateur peut fournir à un paramètre `using` de son type : `given Config = Config("dev", 500)`, ou une instance nommée, `given devConfig: Config = ...`. Les givens peuvent aussi dépendre d'autres givens.

#### Qu'est-ce qu'une clause `using` ?

Une liste de paramètres marquée `using`, comme `(using cfg: Config)`, dont le compilateur remplit les arguments avec les givens de la portée. L'appelant peut toujours les passer explicitement avec `(using value)`. Les paramètres anonymes s'écrivent `(using Config)` et se récupèrent avec `summon`.

#### Comment importer des givens ?

Les imports avec joker (`import a.*`) n'importent pas les givens. On les importe avec `import a.given` (tous les givens) ou par type, `import a.{given Ordering[?]}`, ce qui rend leur origine explicite.

#### Que fait `summon` ?

`summon[T]` renvoie l'instance given de type `T` présente dans la portée, ou ne compile pas s'il n'y en a pas. C'est l'équivalent Scala 3 du `implicitly` de Scala 2.

#### Comment les implicits de Scala 2 se transposent-ils en Scala 3 ?

Les valeurs et méthodes implicites deviennent des instances `given`, les paramètres implicites des clauses `using`, les classes implicites des méthodes d'extension et les conversions implicites des instances `given Conversion[A, B]`. Scala 3 accepte toujours les implicits de Scala 2, ce qui permet une migration progressive.

#### Où le compilateur cherche-t-il les givens ?

D'abord dans la portée lexicale : définitions locales, classes englobantes et imports. Ensuite dans la portée implicite du type recherché, qui comprend les objects compagnons du type et de ses arguments de type. C'est pourquoi les instances de type classes vivent en général dans des objects compagnons.

<!-- challenge -->

Un paramètre `ExecutionContext` est passé explicitement à travers 30 méthodes d'un service. Comment simplifier sans état global ?

<!-- solution -->

Le déclarer comme `(using ExecutionContext)` dans ces méthodes et fournir un seul `given ExecutionContext` en bordure de l'application (ou dans les tests). Les appels ne le mentionnent plus, et chaque environnement peut toujours fournir le sien.

<!-- takeaways -->

- Les clauses `using` reçoivent le contexte ; `given` le fournit.
- Importez les givens explicitement avec `import x.given`.
- Les instances des objects compagnons sont trouvées automatiquement.

<!-- unit: Type classes -->

<!-- goals -->

- Définir des type classes avec des traits et des instances given.
- Utiliser les context bounds, la dérivation et l'égalité multiverselle.

<!-- concept -->

Une type class ajoute un comportement à des types qui ne vous appartiennent pas, sans héritage. Un trait décrit le comportement (`Show[A]`, `Encoder[A]`), des instances given l'implémentent pour des types précis, et les méthodes réclament une instance avec un context bound. Prendre en charge un nouveau type, c'est écrire une instance de plus, pas modifier le type.

Les bibliothèques utilisent ce patron partout : les codecs JSON de circe, les encoders de Spark, `Monoid` et `Functor` de Cats, et `Ordering` dans la bibliothèque standard. Scala 3 peut dériver des instances automatiquement avec `derives`.

<!-- example -->

```scala
trait Show[A]:
  def show(a: A): String

object Show:
  given Show[Int] = n => s"Int($n)"
  given [A](using s: Show[A]): Show[List[A]] =
    as => as.map(s.show).mkString("[", ", ", "]")

def describe[A: Show](a: A): String = summon[Show[A]].show(a)
describe(List(1, 2))                     // [Int(1), Int(2)]
```

#### Qu'est-ce qu'une type class ?

Un trait générique qui décrit une capacité (`Show[A]`, `Ordering[A]`, `Encoder[A]`), plus des instances pour des types précis, fournies comme givens. Le code qui a besoin de la capacité réclame une instance : le comportement s'ajoute aux types de l'extérieur, à la compilation.

#### Comment définir et utiliser une type class en Scala 3 ?

Écrivez un trait avec un paramètre de type, fournissez des instances `given` pour les types pris en charge (en général dans l'object compagnon du trait ou du type), et réclamez une instance là où vous en avez besoin avec un context bound ou une clause `using`. Des méthodes d'extension dans le trait offrent aux appels une syntaxe naturelle comme `value.show`.

#### Qu'est-ce qu'un context bound ?

`def describe[A: Show](a: A)` est un raccourci pour un paramètre `using` de type `Show[A]`. Depuis Scala 3.6, l'instance peut être nommée dans la borne, `[A: Show as s]` ; sinon on la récupère avec `summon[Show[A]]`.

#### Qu'est-ce que la dérivation de type classes ?

`case class Order(...) derives Codec` demande au compilateur de générer une instance à partir de la structure du type, via une méthode `derived` fournie par la type class. Des bibliothèques comme circe s'en servent pour construire des codecs JSON pour les case classes et les enums.

#### Pourquoi préférer les type classes à l'héritage pour, par exemple, l'encodage JSON ?

On peut ajouter des instances pour des types qui ne nous appartiennent pas (bibliothèques ou classes Java), un type peut avoir plusieurs instances selon le contexte, les classes de données restent libres de code de sérialisation, et une instance manquante est une erreur de compilation plutôt que d'exécution.

#### Qu'est-ce qu'`Ordering` ?

La type class de tri de la bibliothèque standard. `sorted`, `max` et `TreeMap` reçoivent un `Ordering` given ; on construit les siens avec `Ordering.by(_.amount)` et on les inverse avec `.reverse`.

#### Qu'est-ce que l'égalité multiverselle ?

Une fonctionnalité facultative de Scala 3 : avec `import scala.language.strictEquality`, `==` ne compile qu'entre types disposant d'une instance `CanEqual`, en général dérivée avec `derives CanEqual`. Elle détecte les comparaisons toujours fausses, comme un `CustomerId` avec un `Int`.

<!-- challenge -->

Une équipe ajoute `toJson` à 40 case classes via un trait `JsonSerializable`, mais ne peut pas l'ajouter à des classes d'une bibliothèque externe. Quelle conception résout les deux problèmes ?

<!-- solution -->

Une type class : un `Encoder[A]` avec des instances dérivées pour les case classes de l'équipe (`derives`) et écrites à la main pour les types de la bibliothèque. Les classes de données ne dépendent plus du code JSON, et n'importe quel type peut avoir un encoder.

<!-- takeaways -->

- Les type classes ajoutent un comportement de l'extérieur.
- Les context bounds réclament des instances.
- `derives` génère des instances à partir de la structure.

<!-- unit: Méthodes d'extension et conversions -->

<!-- goals -->

- Ajouter des méthodes à des types existants avec les méthodes d'extension.
- Utiliser les conversions implicites avec parcimonie, avec `Conversion` et `into`.

<!-- concept -->

Les méthodes d'extension ajoutent des méthodes à des types qu'on ne peut pas modifier, comme `String` ou une classe de bibliothèque. Elles sont résolues à la compilation, ne coûtent rien à l'exécution et remplacent les classes implicites de Scala 2.

Les conversions implicites transforment silencieusement un type en un autre. Elles rendaient le code Scala 2 difficile à suivre, alors Scala 3 les restreint : on définit un `given Conversion[A, B]`, et son utilisation exige un import de langage, sauf si la cible est marquée `into`, stable depuis 3.9, qui n'autorise les conversions que là où une API les demande.

<!-- example -->

```scala
extension (s: String)
  def toSnakeCase: String = s.replaceAll("([a-z])([A-Z])", "$1_$2").toLowerCase
  def isBlankOrNull: Boolean = s == null || s.isBlank

"orderDate".toSnakeCase          // order_date
```

#### Qu'est-ce qu'une méthode d'extension ?

Une méthode définie hors d'un type qu'on peut appeler comme un membre : `extension (s: String) def toSnakeCase: String = ...` permet d'écrire `"orderDate".toSnakeCase`. Elle est visible là où elle est définie ou importée, ou quand elle appartient à une instance given ou à un compagnon dans la portée.

#### Comment Scala 2 ajoutait-il des méthodes à des types existants ?

Avec des classes implicites, `implicit class RichString(s: String) { def toSnakeCase = ... }`, le patron « enrich my library ». Le compilateur enveloppait la valeur dans la classe quand on appelait une méthode absente.

#### Qu'est-ce qu'une conversion implicite, et pourquoi la déconseille-t-on ?

Une règle qui convertit automatiquement une valeur de type `A` en `B` quand un `B` est attendu. Elle masque ce que fait le code, peut faire compiler du code faux et ralentit la compilation : Scala 3 exige un `given Conversion[A, B]` et un import de `scala.language.implicitConversions` (ou `into`) pour en utiliser une.

#### Que fait `into` ?

Il marque un type de paramètre, ou toute une classe, comme cible de conversions implicites : `def write(path: into Path)` permet de passer toute valeur qui a une `Conversion` vers `Path`, sans import de langage côté appelant. Les conversions n'ont alors lieu que là où l'auteur de l'API les a autorisées.

#### Comment le compilateur trouve-t-il les méthodes d'extension ?

Quand `x.m` ne compile pas parce que `x` n'a pas de membre `m`, le compilateur cherche une méthode d'extension nommée `m` dans la portée (définie ou importée), dans les instances given de la portée et dans la portée implicite du type de `x`, comme son object compagnon.

<!-- challenge -->

Un code définit une conversion implicite de `String` vers `LocalDate`. Un nom de colonne passé par erreur à la place d'une date a compilé, puis échoué à l'exécution. Que changez-vous ?

<!-- solution -->

Supprimer la conversion et convertir explicitement, par exemple avec une méthode d'extension `"2026-10-22".toLocalDate` qui renvoie un `Either` : la conversion est visible et les échecs se gèrent à l'appel.

<!-- takeaways -->

- Les méthodes d'extension ajoutent des méthodes sans enveloppe.
- Les conversions exigent `Conversion` et une activation explicite.
- Préférez les conversions explicites dans le code applicatif.

<!-- stage: Pratique de l'ingénierie -->

### Concurrence

<!-- unit: Futures -->

<!-- goals -->

- Exécuter du travail asynchrone avec `Future` et un `ExecutionContext`.
- Composer des futures et gérer échecs, blocages et limites de parallélisme.

<!-- concept -->

Un `Future[A]` est une valeur qui contiendra plus tard un résultat, ou un échec. Il est calculé sur un pool de threads fourni par un `ExecutionContext`, démarre dès sa création et se combine avec `map`, `flatMap` et les compréhensions `for` au lieu d'attendre.

Bloquer un thread pour attendre un résultat (`Await.result`) va à l'encontre de l'idée, sauf tout au bord d'un programme ou dans les tests. Les E/S bloquantes dans un future doivent être enveloppées dans `blocking` ou tourner sur un pool dédié, pour ne pas affamer le pool partagé.

<!-- example -->

```scala
import scala.concurrent.{Future, ExecutionContext}
import ExecutionContext.Implicits.global

def fetchOrders(day: String): Future[List[Order]] = Future(api.orders(day))
def fetchRate(day: String): Future[BigDecimal] = Future(api.eurRate(day))

val ordersF = fetchOrders("2026-10-22")       // both start now, in parallel
val rateF   = fetchRate("2026-10-22")
val totalF: Future[BigDecimal] = for
  orders <- ordersF
  rate   <- rateF
yield orders.map(_.amount).sum * rate
```

#### Qu'est-ce qu'un `Future` ?

Un emplacement pour une valeur calculée de façon asynchrone, qui finit par valoir `Success(value)` ou `Failure(exception)`. Il est impatient (eager : il démarre immédiatement) et son résultat est conservé une fois terminé.

#### Qu'est-ce qu'un `ExecutionContext` ?

Le pool de threads qui exécute les futures et leurs callbacks, que la plupart des méthodes de `Future` reçoivent comme paramètre de contexte. `ExecutionContext.global` convient au travail CPU ; les appels bloquants ont besoin de `blocking { ... }` ou d'un pool séparé et borné.

#### Comment composer des futures ?

Avec `map` et `flatMap` (ou une compréhension `for`) pour enchaîner des étapes dépendantes, `zip` pour combiner des étapes indépendantes, et `Future.sequence` ou `Future.traverse` pour transformer une collection de futures en future d'une collection.

#### Pourquoi les futures d'une compréhension `for` s'exécutent-ils parfois l'un après l'autre ?

Si les futures sont créés dans la compréhension (`a <- fetchA(); b <- fetchB()`), le second n'est créé qu'une fois le premier terminé. Créez les futures indépendants avant la compréhension, comme dans l'exemple, pour qu'ils s'exécutent en parallèle.

#### Pourquoi éviter `Await.result` ?

Il bloque un thread jusqu'à la fin du future, ce qui gaspille des threads, peut interbloquer un petit pool et masque la conception asynchrone. Ne l'utilisez qu'au bord du programme (un `main` qui doit attendre) ou dans les tests, toujours avec un timeout.

#### Comment gérer les échecs d'un `Future` ?

Une exception levée termine le future en `Failure`. On récupère avec `recover` ou `recoverWith`, on transforme les deux issues avec `transform`, on fournit une alternative avec `fallbackTo` et on réagit avec `onComplete`, sans relancer d'exception dans les callbacks.

#### Comment exécuter de nombreux futures avec un parallélisme limité ?

`Future.traverse(items)(f)` lance tous les appels d'un coup, ce qui peut saturer une API. Traitez les éléments par lots (`grouped(n)` enchaînés séquentiellement), exécutez-les sur un pool de threads borné, ou utilisez une bibliothèque de streaming ou d'effets avec limite de parallélisme, comme `parTraverseN` de Cats Effect.

<!-- challenge -->

Une compréhension `for` combine trois appels d'API indépendants qui renvoient des futures, et le temps total est la somme des trois. Comment le ramener au temps du plus lent ?

<!-- solution -->

Lancer les trois futures avant la compréhension (`val a = callA(); val b = callB(); val c = callC()`) et ne faire que les combiner dedans, ou utiliser `zip` ; ils s'exécutent alors en parallèle.

<!-- takeaways -->

- Les futures démarrent aussitôt sur un `ExecutionContext`.
- Composez ; ne bloquez pas avec `Await`.
- Lancez les futures indépendants avant de les combiner.

<!-- unit: Effets, acteurs et threads -->

<!-- goals -->

- Expliquer les systèmes d'effets comme Cats Effect et ZIO.
- Connaître les acteurs, les threads virtuels et le partage d'état sûr.

<!-- concept -->

Les futures sont impatients et non référentiellement transparents : créer un future lance le travail, si bien qu'on ne peut ni le relancer ni le réutiliser comme description d'un travail. Les bibliothèques d'effets comme Cats Effect et ZIO décrivent les programmes comme des valeurs (`IO`, `ZIO`) qui ne s'exécutent que lorsque leur runtime les lance. Les programmes se composent, se relancent et s'annulent alors en sécurité, sur des fibres légères, avec gestion sûre des ressources et concurrence structurée intégrées.

Les acteurs, dans Apache Pekko (le fork open source d'Akka), modélisent la concurrence comme des objets qui échangent des messages, adaptés aux systèmes avec état et distribués. Depuis le JDK 21, les threads virtuels permettent aussi au code bloquant ordinaire de passer à l'échelle.

<!-- example -->

```scala
import cats.effect.{IO, IOApp}
import scala.concurrent.duration.*

object Crawl extends IOApp.Simple:
  def fetch(id: Int): IO[String] = IO.blocking(s"page $id")

  val run: IO[Unit] =
    IO.parTraverseN(4)(List.range(1, 21))(fetch)     // at most 4 at a time
      .timeout(30.seconds)
      .flatMap(pages => IO.println(s"${pages.size} pages"))
```

#### Qu'est-ce qu'un système d'effets ?

Une bibliothèque qui représente les effets de bord comme des valeurs décrivant ce qu'il faut faire, comme `IO[A]` dans Cats Effect ou `ZIO[R, E, A]`, et les exécute avec un runtime. Elle ajoute évaluation paresseuse, annulation, relances, gestion sûre des ressources et concurrence légère à du code fonctionnel pur.

#### Quelle est la différence entre `Future` et `IO` ?

Un `Future` démarre à sa création et mémorise son résultat. Un `IO` est une description qui ne fait rien tant qu'on ne l'exécute pas, et l'exécuter deux fois fait le travail deux fois. Cela rend `IO` référentiellement transparent : relances, timeouts et courses sont de simples fonctions sur des valeurs.

#### Que sont les fibres ?

Des threads logiques légers gérés par un runtime d'effets et planifiés sur un petit pool de threads système. Il peut en exister des millions à la fois, elles sont annulables, et les appels bloquants sont déplacés vers un pool séparé.

#### Qu'est-ce que le modèle d'acteurs, et qu'est-ce que Pekko ?

Les acteurs sont des objets qui détiennent un état privé et ne communiquent que par messages asynchrones, en traitant un message à la fois : pas besoin de verrous. Pekko est le fork Apache d'Akka, créé après le passage d'Akka sous licence commerciale en 2022.

#### Que sont les threads virtuels, et comptent-ils pour Scala ?

Des threads du JDK 21 gérés par la JVM plutôt que par le système, assez peu coûteux pour en créer un par tâche : le code bloquant ne gaspille plus de threads système. Scala peut les utiliser directement, et des bibliothèques comme Ox construisent dessus une concurrence structurée en style direct, alternative aux futures et aux systèmes d'effets.

#### Comment partager un état mutable entre threads en sécurité ?

Privilégiez les données immuables et le passage de messages. Quand un état doit être partagé, utilisez des références atomiques (`AtomicReference`, le `Ref` de Cats Effect), des collections concurrentes (`TrieMap`, `ConcurrentHashMap`) ou des blocs `synchronized`, avec des sections critiques courtes.

<!-- challenge -->

Un helper de relance reçoit `f: Future[A]` et le rappelle en cas d'échec, mais les relances ne rappellent jamais l'API. Pourquoi, et comment corriger ?

<!-- solution -->

Le future a démarré une seule fois en étant passé en argument, et « relancer » relit le même résultat en échec. Recevez de quoi le recréer, `f: () => Future[A]` ou un by-name `f: => Future[A]`, ou utilisez `IO`, qui décrit l'appel et le réexécute à chaque tentative.

<!-- takeaways -->

- `IO` décrit le travail ; `Future` l'a déjà lancé.
- Fibres et threads virtuels rendent la concurrence bon marché.
- Partagez l'état via atomiques, `Ref` ou messages.

### Outillage, interopérabilité Java et tests

<!-- unit: Outils de build -->

<!-- goals -->

- Structurer un build sbt avec dépendances, portées et paramètres.
- Packager des jobs Spark, compiler des bibliothèques pour plusieurs versions et connaître Scala CLI et Mill.

<!-- concept -->

sbt est l'outil de build Scala le plus répandu. `build.sbt` déclare la version de Scala, les dépendances et les paramètres, et sbt compile de façon incrémentale, lance les tests et publie des artefacts. Les artefacts des bibliothèques Scala portent la version binaire de Scala dans leur nom (`_2.13`, `_3`), que l'opérateur `%%` ajoute pour vous.

Pour les scripts et petits projets, Scala CLI (la commande `scala`) se passe de fichier de build, et Mill est un outil de build alternatif plus rapide. Les jobs Spark sont en général packagés en un seul JAR, Spark étant marqué `provided` puisque le cluster le fournit.

<!-- example -->

```scala
// build.sbt
ThisBuild / scalaVersion := "2.13.18"

lazy val etl = (project in file("."))
  .settings(
    name := "orders-etl",
    libraryDependencies ++= Seq(
      "org.apache.spark" %% "spark-sql" % "4.2.0" % "provided",
      "org.scalatest"    %% "scalatest" % "3.2.19" % Test
    )
  )
```

#### Qu'est-ce que sbt ?

L'outil de build standard de Scala : il compile de façon incrémentale, résout les dépendances, lance les tests, ouvre un REPL et publie des artefacts. Les builds se définissent dans `build.sbt` avec des paramètres et des tâches, et s'étendent avec des plugins (`project/plugins.sbt`).

#### Quelle est la différence entre `%` et `%%` dans sbt ?

`%%` ajoute au nom de l'artefact la version binaire de Scala du projet (`spark-sql` devient `spark-sql_2.13`), comme l'exigent les bibliothèques Scala. `%` utilise le nom tel quel, pour les bibliothèques Java.

#### Que signifie la portée `provided` ?

La dépendance est disponible à la compilation mais n'est pas packagée, car l'environnement d'exécution la fournit. Spark et Hadoop sont `provided` dans les jobs Spark, ce qui garde le JAR léger et évite les conflits de versions avec le cluster.

#### Comment construire un fat JAR ?

Avec le plugin sbt-assembly, qui package votre code et ses dépendances dans un seul JAR. Des stratégies de fusion résolvent les fichiers en double (par exemple dans `META-INF`), et le shading renomme les packages en conflit, comme une ancienne version de Jackson ou Guava utilisée par une dépendance.

#### Qu'est-ce que le cross-building ?

Compiler et publier une bibliothèque pour plusieurs versions de Scala : `crossScalaVersions := Seq("2.13.18", "3.3.8")`, puis `sbt +test` ou `+publish` exécute la tâche pour chacune. Le code propre à une version va dans des dossiers `src/main/scala-2.13` ou `scala-3`.

#### Que sont Scala CLI et Mill ?

Scala CLI, désormais la commande `scala`, exécute et package des projets à un seul module avec des directives `//> using` dans les fichiers source au lieu d'un fichier de build. Mill est un outil de build dont les builds s'écrivent comme des objects Scala, connu pour ses builds rapides et mis en cache. Les deux sont des alternatives à sbt selon la taille du projet.

#### Pourquoi les versions de Scala influent-elles sur la compatibilité binaire ?

Les bibliothèques sont compilées pour une version binaire de Scala (2.12, 2.13 ou 3), et ces séries ne sont pas compatibles binairement entre elles : chaque bibliothèque est publiée une fois par version. Scala 3 fait exception : il peut utiliser la plupart des artefacts Scala 2.13, et ses versions mineures restent rétrocompatibles.

<!-- challenge -->

Le JAR d'un job Spark pèse 400 Mo et échoue sur le cluster avec `NoSuchMethodError` dans des classes Jackson. Que changez-vous dans le build ?

<!-- solution -->

Marquer Spark et Hadoop comme `provided` pour qu'ils ne soient plus packagés, aligner les versions des autres dépendances sur celles du cluster, et appliquer le shading à la bibliothèque en conflit dans sbt-assembly si une dépendance a vraiment besoin d'une autre version de Jackson.

<!-- takeaways -->

- `%%` ajoute la version binaire de Scala.
- Spark est `provided` dans les JAR des jobs.
- Assembly construit des fat JARs ; le shading résout les conflits.

<!-- unit: Interopérabilité avec Java -->

<!-- goals -->

- Appeler des bibliothèques Java depuis Scala et Scala depuis Java.
- Convertir les collections et gérer nulls, exceptions vérifiées et versions du JDK.

<!-- concept -->

Scala tourne sur la JVM : toute bibliothèque Java est à une dépendance près, et les appels ressemblent à des appels Scala. Les frictions sont aux frontières : les collections Java doivent être converties en collections Scala, les API Java peuvent renvoyer `null`, et le compilateur Scala ne suit pas les exceptions vérifiées de Java.

Dans l'autre sens, les fonctionnalités Scala sans équivalent Java, comme les arguments par défaut, les givens et les objects compagnons, paraissent étranges depuis Java : les API destinées à des appelants Java restent simples.

<!-- example -->

```scala
import scala.jdk.CollectionConverters.*
import java.nio.file.{Files, Paths}

val ids: List[String] = Files.readAllLines(Paths.get("ids.txt")).asScala.toList
val javaList: java.util.List[String] = List("a", "b").asJava
val appHome: Option[String] = Option(System.getenv("APP_HOME"))    // null becomes None
```

#### Comment convertir entre collections Java et Scala ?

Importez `scala.jdk.CollectionConverters.*` et appelez `.asScala` ou `.asJava`, qui enveloppent la collection sans la copier ; ajoutez `.toList` ou `.toMap` pour une copie immuable. En Scala 2.12, l'import était `scala.collection.JavaConverters._`.

#### Comment gérer le `null` venant du code Java ?

Enveloppez les valeurs Java dans `Option(...)` à la frontière : `null` devient `None` et le reste du code travaille avec `Option`. Ne laissez jamais `null` circuler dans le code métier Scala.

#### Comment les exceptions vérifiées de Java sont-elles gérées ?

Scala ne distingue pas les exceptions vérifiées : rien n'oblige à les intercepter ou à les déclarer. Interceptez-les là où vous pouvez les traiter, ou enveloppez l'appel dans `Try`. Ajoutez `@throws[IOException]` aux méthodes Scala appelées depuis Java, pour que Java voie la déclaration.

#### À quoi ressemblent les fonctionnalités Scala vues de Java ?

Les objects deviennent une classe avec une instance statique `MODULE$` plus des redirections statiques, les traits des interfaces avec méthodes par défaut, les arguments par défaut des méthodes nommées comme `connect$default$2`, et les givens des paramètres ordinaires. Gardez simples les API destinées aux appelants Java.

#### Comment les fonctions Scala et les interfaces fonctionnelles Java interagissent-elles ?

Les lambdas Scala se convertissent automatiquement en interfaces fonctionnelles Java (types à une seule méthode abstraite) comme `Runnable` ou `java.util.function.Function`. `scala.jdk.FunctionConverters` convertit explicitement des objets fonction si nécessaire.

#### Sur quel JDK le code Scala doit-il tourner ?

Scala 3.8 et ultérieurs exigent le JDK 17 ou plus récent ; Scala 3.3 LTS, 2.13 et 2.12 tournent encore sur le JDK 8. En pratique, les équipes utilisent un JDK LTS, 17, 21 ou 25, selon leur plateforme : Spark 4 exige le JDK 17 ou ultérieur.

<!-- challenge -->

Un SDK Java renvoie une `java.util.Map[String, String]` de tags parfois `null`, et `sdk.tags().asScala.get("env")` lève une `NullPointerException`. Corrigez.

<!-- solution -->

Envelopper d'abord le résultat : `Option(sdk.tags()).map(_.asScala.toMap).getOrElse(Map.empty).get("env")`, pour qu'une map absente se comporte comme une map vide.

<!-- takeaways -->

- `asScala`/`asJava` convertissent les collections.
- Enveloppez les résultats Java dans `Option`.
- Scala 3.8+ exige le JDK 17.

<!-- unit: Tests -->

<!-- goals -->

- Écrire des tests avec ScalaTest ou MUnit et des tests de propriétés avec ScalaCheck.
- Tester du code Spark et simuler les dépendances avec discernement.

<!-- concept -->

Les frameworks de test Scala associent un style de définition des tests à des assertions et à des exécuteurs intégrés à sbt. ScalaTest propose plusieurs styles (`AnyFunSuite`, `AnyFlatSpec`, `AnyWordSpec`) ; MUnit garde une API réduite avec des diffs clairs. Les deux s'exécutent avec `sbt test` et dans les IDE.

Les tests de propriétés avec ScalaCheck génèrent de nombreuses entrées aléatoires et vérifient qu'une propriété tient, en réduisant les échecs à un cas minimal. Les fonctions pures facilitent tout cela : pas de mise en place, pas de mocks, juste des entrées et des sorties.

<!-- example -->

```scala
import munit.FunSuite

class AmountSuite extends FunSuite:
  test("parses amounts with spaces"):
    assertEquals(parseAmount(" 12.50 "), Right(BigDecimal("12.50")))

  test("rejects garbage"):
    assert(parseAmount("abc").isLeft)
```

#### Quelles bibliothèques de test sont courantes en Scala ?

ScalaTest (nombreux styles, matchers riches), MUnit (minimal, rapide, bons diffs), specs2, ScalaCheck pour les tests de propriétés, et des frameworks adaptés aux effets comme weaver ou ZIO Test pour le code `IO` et `ZIO`.

#### Qu'est-ce que le test de propriétés ?

Énoncer une propriété qui doit tenir pour toutes les entrées et laisser une bibliothèque générer des centaines de cas aléatoires, en réduisant tout échec au plus petit contre-exemple :

```scala
import org.scalacheck.Prop.forAll
val reverseTwice = forAll((xs: List[Int]) => xs.reverse.reverse == xs)
```

#### Comment tester du code Spark en Scala ?

Écrivez les transformations comme des fonctions de `DataFrame` vers `DataFrame`, construisez de petites entrées avec `Seq(...).toDF(...)`, exécutez-les sur une `SparkSession` locale partagée par la suite (`master("local[2]")`), et comparez les résultats collectés ou utilisez une bibliothèque d'aide pour l'égalité de DataFrames.

#### Comment simuler des dépendances en Scala ?

Concevez plutôt pour la testabilité : dépendez de traits ou de fonctions et passez de simples implémentations factices dans les tests. Pour du code très orienté Java, Mockito fonctionne via mockito-scala, mais un usage intensif de mocks signale souvent que les effets ne sont pas séparés de la logique.

#### Comment exécuter une partie des tests avec sbt ?

`sbt "testOnly *AmountSuite"` exécute une suite, `testQuick` relance les tests en échec et modifiés, et le préfixe `~` (`~testQuick`) les relance à chaque modification de fichier.

<!-- challenge -->

Chaque suite de tests Spark crée sa propre `SparkSession`, et l'exécution des tests prend 15 minutes. Comment l'accélérer ?

<!-- solution -->

Partager une seule session locale entre les suites via un trait ou une fixture commune, exécuter avec `local[2]`, régler `spark.sql.shuffle.partitions` sur un petit nombre et désactiver l'interface web ; l'essentiel du temps partait dans le démarrage des sessions et le shuffle vers 200 partitions.

<!-- takeaways -->

- ScalaTest et MUnit sont les choix courants.
- ScalaCheck trouve les cas limites.
- Partagez une seule session Spark locale dans les tests.

<!-- unit: Qualité du code et migration -->

<!-- goals -->

- Garder un code cohérent avec scalafmt, scalafix et les avertissements du compilateur.
- Planifier une migration de Scala 2.13 vers Scala 3.

<!-- concept -->

Le formatage et le linting sont automatisés dans la plupart des équipes Scala : scalafmt formate le code, scalafix applique des règles de lint et des réécritures automatiques, et les avertissements du compilateur, comme les imports inutilisés ou les match non exhaustifs, détectent de vrais bugs quand la CI les traite comme des erreurs.

La migration de Scala 2.13 vers Scala 3 est en grande partie compatible au niveau du source. Le compilateur peut réécrire l'ancienne syntaxe, et le code Scala 3 peut utiliser des bibliothèques Scala 2.13. Les difficultés sont les macros Scala 2, à réécrire, et les dépendances qui n'ont pas publié de version pour Scala 3.

<!-- example -->

```scala
// build.sbt (Scala 3)
scalacOptions ++= Seq("-deprecation", "-feature", "-Wunused:all", "-Werror")
```
```bash
sbt scalafmtAll "scalafixAll RemoveUnused" test
```

#### Que sont scalafmt et scalafix ?

scalafmt est le formateur de code standard, configuré dans `.scalafmt.conf` et vérifié en CI. scalafix est un outil de refactoring et de linting dont les règles suppriment les imports inutilisés, imposent des conventions et automatisent les migrations.

#### Quelles options du compilateur aident à détecter les bugs ?

`-deprecation` et `-feature` détaillent les avertissements, `-Wunused:all` signale les imports et variables inutilisés, `-Wvalue-discard` les valeurs non `Unit` ignorées, et `-Werror` (anciennement `-Xfatal-warnings`) transforme les avertissements en erreurs pour qu'ils ne s'accumulent pas.

#### Comment migrer un projet de Scala 2.13 vers Scala 3 ?

Mettez les dépendances à jour vers des versions publiées pour Scala 3 (ou utilisez celles de 2.13 avec `.cross(CrossVersion.for3Use2_13)`), compilez avec `-source:3.0-migration -rewrite` pour corriger automatiquement la syntaxe, réécrivez les macros et compilez pour les deux versions pendant la transition. Commencez par les modules feuilles et les bibliothèques, puis les services.

#### Quelles fonctionnalités de Scala 2 ont changé ou disparu en Scala 3 ?

Les macros Scala 2, les types existentiels (`forSome`), la syntaxe de procédure (`def f() { ... }`), les littéraux de symbole, les boucles `do`-`while` et l'auto-application des listes de paramètres vides ont disparu. Les implicits fonctionnent toujours mais sont remplacés par les givens, et les package objects sont dépréciés au profit des définitions de premier niveau.

#### Qu'est-ce que TASTy ?

Le format d'arbre syntaxique abstrait typé que Scala 3 stocke dans des fichiers `.tasty` à côté du bytecode. Il conserve toute l'information de type, ce qui permet au compilateur d'utiliser des bibliothèques d'une version de Scala 3 à l'autre, prend en charge `inline` et les macros, et alimente l'outillage des IDE.

<!-- challenge -->

Une entreprise a 40 services et bibliothèques en Scala 2.13 et veut passer à Scala 3. Comment planifier la migration ?

<!-- solution -->

Mettre d'abord à jour les bibliothèques partagées et les compiler pour 2.13 et 3, puis migrer les services un par un avec les réécritures de migration, en remplaçant les macros et les dépendances non prises en charge. Garder les jobs Spark en 2.13, et activer les avertissements comme erreurs dès que chaque module compile proprement.

<!-- takeaways -->

- Automatisez formatage, linting et avertissements en CI.
- Scala 3 peut utiliser des bibliothèques Scala 2.13.
- Migrez d'abord les bibliothèques ; les jobs Spark restent en 2.13.

<!-- stage: Scala pour le data engineering -->

### Scala et Spark

<!-- unit: L'API Scala de Spark -->

<!-- goals -->

- Expliquer le lien entre Scala et Spark et quand le préférer à PySpark.
- Créer une `SparkSession`, lire des données et écrire des transformations de DataFrames en Scala.

<!-- concept -->

Spark est écrit en Scala, et son API Scala est la plus directe : pas de processus Python, des Datasets typés vérifiés à la compilation et l'accès aux points d'extension internes de Spark. Les opérations sur DataFrames se compilent en plans identiques dans tous les langages : PySpark est donc aussi rapide pour les opérations intégrées, et les avantages de Scala apparaissent dans les UDF, les pipelines typés, les connecteurs sur mesure et les bibliothèques.

L'API DataFrame se lit presque à l'identique dans les deux langages, à quelques symboles propres à Scala près, comme `$"col"` et `===`.

<!-- example -->

```scala
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

val spark = SparkSession.builder().appName("orders-daily").getOrCreate()
import spark.implicits._

val daily = spark.read.parquet("s3://lake/silver/orders")
  .filter($"status" === "paid")
  .groupBy($"order_date", $"country")
  .agg(sum($"amount").as("revenue"), countDistinct($"customer_id").as("customers"))

daily.write.mode("overwrite").partitionBy("order_date").parquet("s3://lake/gold/daily_revenue")
```

#### Pourquoi associe-t-on Spark à Scala ?

Spark a été écrit en Scala à UC Berkeley, et son cœur, ses API et l'essentiel de son écosystème (connecteurs, code d'origine de Delta Lake) sont en Scala. Les nouveautés apparaissent d'abord dans l'API Scala, et les internes de Spark sont des classes Scala.

#### Scala ou PySpark : comment choisir ?

PySpark convient aux équipes qui travaillent en Python, utilisent des bibliothèques Python (pandas, ML) et s'en tiennent aux fonctions intégrées. Scala convient aux équipes qui veulent des vérifications à la compilation, des Datasets typés, des UDF rapides dans la JVM, des sources de données sur mesure ou des extensions de Spark. Le support de la plateforme et les compétences de l'équipe tranchent en général.

#### Une requête DataFrame est-elle plus rapide en Scala qu'en PySpark ?

Pas pour les opérations intégrées : les deux construisent le même plan logique, que Catalyst optimise et que la JVM exécute. Les différences apparaissent avec les UDF, qui en PySpark envoient les lignes à des workers Python, et avec le code côté driver.

#### Que fait `import spark.implicits._` ?

Il met dans la portée les encoders pour les primitifs, les tuples et les case classes, la syntaxe `$"column"`, et `toDF` et `toDS` sur les collections locales, comme `Seq((1, "a")).toDF("id", "name")`.

#### Comment désigner des colonnes en Spark Scala ?

Avec `$"amount"`, `col("amount")`, `df("amount")` (utile pour lever l'ambiguïté après une jointure) ou une simple chaîne dans les méthodes qui acceptent des noms. La syntaxe de symbole de Scala 2, `'amount`, est dépréciée.

#### Pourquoi Spark Scala utilise-t-il `===` pour l'égalité de colonnes ?

`==` est l'égalité d'objets de Scala et renvoie un `Boolean`, en comparant les objets `Column` eux-mêmes. `===` construit une expression d'égalité évaluée ligne par ligne, et `=!=` sa négation.

<!-- challenge -->

`df.filter($"country" == "FR")` ne compile pas dans un job Spark en Scala. Pourquoi, et quelle est la correction ?

<!-- solution -->

`==` compare l'objet `Column` à une chaîne et renvoie un `Boolean`, que `filter` n'accepte pas. Utilisez `$"country" === "FR"`, qui construit une expression de colonne.

<!-- takeaways -->

- L'API native de Spark est en Scala.
- Le code DataFrame intégré performe pareil en Scala et en Python.
- Utilisez `===` et `=!=` pour comparer des colonnes.

<!-- unit: Datasets et encoders -->

<!-- goals -->

- Utiliser des Datasets typés avec des case classes et des encoders.
- Choisir entre Datasets et DataFrames.

<!-- concept -->

Un `Dataset[T]` est une collection distribuée d'objets typés : on le transforme avec des fonctions Scala ordinaires sur des case classes, et le compilateur vérifie noms et types des champs. Un DataFrame est un `Dataset[Row]`, non typé. Les encoders convertissent entre objets JVM et format binaire interne de Spark, et sont dérivés pour les case classes et les primitifs.

Les lambdas typées sont cependant opaques pour l'optimiseur : `ds.filter(_.amount > 0)` désérialise chaque ligne en objet, tandis que `ds.filter($"amount" > 0)` peut être poussé jusqu'aux fichiers. Beaucoup d'équipes utilisent des case classes aux frontières et des expressions de colonnes à l'intérieur.

<!-- example -->

```scala
final case class Order(orderId: Long, customerId: String, amount: Double, country: String)

val ds = spark.read.parquet("s3://lake/silver/orders").as[Order]   // column names must match
val slow = ds.filter(_.amount > 1000)              // typed lambda: no pushdown
val fast = ds.filter($"amount" > 1000)             // column expression: pushdown
val counts = ds.groupByKey(_.country).count()      // Dataset[(String, Long)]
```

#### Quelle est la différence entre un DataFrame et un Dataset ?

Un Dataset est typé : `Dataset[Order]` expose des objets `Order`, et les opérations typées sont vérifiées à la compilation. Un DataFrame est un `Dataset[Row]`, dont les colonnes ne sont vérifiées qu'à l'analyse du plan, à l'exécution. Les deux tournent sur le même moteur.

#### Qu'est-ce qu'un encoder ?

Un objet qui convertit entre un type JVM et le format de lignes interne de Spark, en connaissant le schéma. Spark dérive des encoders pour les case classes, les tuples et les primitifs via `import spark.implicits._` ; les autres types nécessitent `Encoders.kryo` ou une conversion.

#### Pourquoi les opérations typées sur les Datasets peuvent-elles être plus lentes ?

Les lambdas comme `map(o => ...)` ou `filter(_.amount > 0)` sont des boîtes noires pour Catalyst : chaque ligne doit être désérialisée en objet, et les filtres ne peuvent pas être poussés jusqu'à Parquet. Les expressions de colonnes gardent les données au format interne et restent optimisables.

#### Comment passer d'un DataFrame à un Dataset et inversement ?

`df.as[Order]` donne un Dataset (et échoue si des colonnes manquent ou si les types ne correspondent pas), `ds.toDF()` fait le chemin inverse, et `Seq(...).toDS()` ou `spark.createDataset` en construisent un à partir de données locales.

#### Peut-on utiliser des Datasets depuis PySpark ?

Non. Python est typé dynamiquement, si bien que PySpark n'expose que des DataFrames. Les Datasets typés existent en Scala et en Java.

#### Comment modéliser des colonnes nullables dans une case class ?

Avec des champs `Option`, comme `amount: Option[Double]`. Un champ primitif comme `Double` ne peut pas contenir `null` : une valeur nulle dans les données échoue à l'exécution.

<!-- challenge -->

Un job qui lit `orders.as[Order]` échoue à l'exécution avec une erreur de null sur le champ `discount`, vide pour certaines lignes. Que changez-vous ?

<!-- solution -->

Déclarer le champ `discount: Option[Double]` dans la case class, pour que les nulls deviennent `None`, et traiter le cas absent dans la transformation.

<!-- takeaways -->

- Les Datasets sont typés ; les DataFrames sont des `Dataset[Row]`.
- Les lambdas typées échappent au pushdown de l'optimiseur.
- Les colonnes nullables exigent des champs `Option`.

<!-- unit: UDF, closures et sérialisation -->

<!-- goals -->

- Écrire des UDF Scala et savoir quand les éviter.
- Corriger « Task not serializable » et utiliser variables broadcast et ressources par partition.

<!-- concept -->

Spark envoie aux executors les fonctions que vous écrivez : tout ce qu'une closure référence doit être sérialisable. Utiliser un champ ou une méthode d'une classe englobante capture l'objet entier, qui contient souvent quelque chose de non sérialisable, comme un client de base de données, et le job échoue avec « Task not serializable ».

Les UDF Scala tournent dans la JVM et évitent l'aller-retour vers Python de PySpark, mais restent des boîtes noires pour l'optimiseur. Les fonctions intégrées restent le premier choix, et une variable broadcast envoie une table de correspondance à chaque executor une seule fois au lieu de l'envoyer avec chaque tâche.

<!-- example -->

```scala
import org.apache.spark.sql.functions._

object Clean {
  def email(s: String): String = Option(s).map(_.trim.toLowerCase).orNull
}
val cleanEmail = udf((s: String) => Clean.email(s))
val viaUdf = customers.withColumn("email", cleanEmail(col("email")))
val viaBuiltins = customers.withColumn("email", lower(trim(col("email"))))   // preferred

val rates = spark.sparkContext.broadcast(Map("EUR" -> 1.0, "COP" -> 0.00023))
```

#### Pourquoi « Task not serializable » se produit-il, et comment corriger ?

Une closure envoyée aux executors référence quelque chose qui ne se sérialise pas, souvent parce qu'elle utilise un champ ou une méthode d'une classe englobante, ce qui capture toute l'instance. Copiez la valeur utile dans une `val` locale avant la closure, déplacez les helpers dans un `object`, ou créez les ressources non sérialisables sur les executors.

#### Les UDF Scala sont-elles plus rapides que les UDF Python ?

Oui : elles s'exécutent dans la JVM de l'executor, sans sérialiser les lignes vers un processus Python. Elles restent opaques pour Catalyst, qui ne peut ni optimiser à travers elles ni pousser les filtres au-delà : les fonctions intégrées sont encore plus rapides.

#### Qu'est-ce qu'une variable broadcast ?

Une valeur en lecture seule, comme une map de correspondance, envoyée une fois à chaque executor et mise en cache sur place (`sparkContext.broadcast(value)`, lue avec `.value`). Sans elle, une grosse valeur capturée par une closure voyage avec chaque tâche.

#### Quelle est la différence entre une variable broadcast et une broadcast join ?

Une variable broadcast transporte une valeur quelconque que vous utilisez dans votre code. Une broadcast join est une stratégie de jointure pour DataFrames, déclenchée automatiquement pour les petites tables ou avec l'indication `broadcast(df)`, dans laquelle Spark envoie la petite table à chaque executor au lieu de faire un shuffle des deux côtés.

#### Que sont les accumulateurs ?

Des variables partagées auxquelles les tâches ne peuvent qu'ajouter, comme des compteurs d'enregistrements erronés, lues sur le driver. Les mises à jour faites dans des transformations peuvent être appliquées deux fois quand des tâches sont relancées ; seules celles faites dans des actions ne comptent qu'une fois de façon garantie.

#### Comment utiliser un client de base de données ou HTTP dans un job Spark ?

Créez-le une fois par partition avec `foreachPartition` ou `mapPartitions`, ni par ligne ni sur le driver, et écrivez par lots. Le client n'a jamais besoin d'être sérialisé puisqu'il est créé sur l'executor.

<!-- challenge -->

Un job envoie chaque ligne à une API dans un `foreach`, en créant un client HTTP par ligne, et il est très lent. Déplacer le client dans un champ de la classe provoque « Task not serializable ». Quelle est la bonne structure ?

<!-- solution -->

Utiliser `foreachPartition` : créer un client par partition sur l'executor, envoyer les lignes par lots et fermer le client à la fin. Rien de non sérialisable n'est capturé, et le coût de connexion n'est payé qu'une fois par partition.

<!-- takeaways -->

- Les closures ne doivent capturer que des valeurs sérialisables.
- Préférez les fonctions intégrées aux UDF, même en Scala.
- Créez les clients par partition, pas par ligne.

### Travailler les données en Scala

<!-- unit: JSON, configuration et E/S -->

<!-- goals -->

- Convertir du JSON en case classes et charger une configuration typée.
- Gérer en sécurité fichiers, appels HTTP, bases de données et ressources.

<!-- concept -->

Hors de Spark, les jobs et services Scala lisent du JSON, de la configuration et des fichiers. Les bibliothèques JSON dérivent des codecs pour les case classes à partir de leur structure (circe, upickle, jsoniter-scala) : la conversion renvoie des valeurs typées ou une erreur claire au lieu de maps de chaînes. La configuration en fichiers HOCON se lit avec Typesafe Config ou se charge directement dans des case classes avec PureConfig.

Les ressources comme les fichiers et les connexions doivent être fermées même en cas d'erreur, ce que fait `scala.util.Using` pour tout `AutoCloseable`.

<!-- example -->

```scala
import io.circe.Decoder
import io.circe.parser.decode

final case class Event(id: String, kind: String, amount: Option[BigDecimal]) derives Decoder

val parsed: Either[io.circe.Error, Event] =
  decode[Event]("""{"id":"e1","kind":"purchase","amount":12.5}""")
```

#### Comment convertir du JSON en Scala ?

Avec une bibliothèque qui dérive des codecs pour les case classes : circe (`derives Decoder`, puis `decode[Event](json)`), upickle, ou jsoniter-scala pour le haut débit. Le décodage renvoie un `Either` avec le chemin précis de l'erreur quand un champ manque ou a le mauvais type.

#### Comment lire la configuration en Scala ?

Typesafe Config lit des fichiers `application.conf` au format HOCON, avec des surcharges par l'environnement comme `url = ${?DB_URL}`. PureConfig charge la configuration directement dans des case classes et signale d'un coup, au démarrage, tous les champs manquants ou invalides.

#### Que fait `scala.util.Using` ?

Il exécute un bloc avec une ressource et la ferme ensuite, même en cas d'exception, comme le try-with-resources de Java. `Using(resource)(f)` renvoie un `Try`, `Using.resource` renvoie directement la valeur et lève l'exception en cas d'échec, et `Using.Manager` gère plusieurs ressources.

#### Comment travailler avec des fichiers et des chemins ?

Avec `java.nio.file` (`Files`, `Paths`) depuis Scala, ou os-lib pour des scripts concis (`os.read.lines`, `os.walk`, `os.proc` pour les sous-processus). `scala.io.Source` suffit pour lire de simples fichiers texte.

#### Comment appeler une API REST depuis Scala ?

Avec sttp client (en choisissant un backend synchrone, `Future` ou à effets) ou requests-scala pour les scripts : fixez des timeouts, relancez les erreurs transitoires avec backoff et décodez les réponses JSON en case classes.

#### Comment interroger une base de données depuis Scala ?

Avec JDBC directement ou via une bibliothèque : Doobie pour le code Cats Effect, Slick, ScalikeJDBC ou Magnum. Utilisez des requêtes paramétrées, un pool de connexions comme HikariCP, et `Using` ou la gestion de ressources de la bibliothèque pour fermer les connexions.

<!-- challenge -->

Un job appelle `config.getString("db.url")` au cœur de son traitement et échoue au bout d'une heure quand la clé manque en production. Comment l'éviter ?

<!-- solution -->

Charger toute la configuration dans une case class au démarrage (avec PureConfig, ou en lisant chaque clé une fois) et échouer immédiatement avec la liste de ce qui manque ; le reste du code reçoit la configuration typée.

<!-- takeaways -->

- Dérivez des codecs JSON pour les case classes.
- Chargez et validez la configuration au démarrage.
- Fermez les ressources avec `Using`.

<!-- unit: Performances sur la JVM -->

<!-- goals -->

- Éviter le boxing et l'usage dispendieux des collections.
- Mesurer les performances avec JMH et comprendre le préchauffage du JIT et le ramasse-miettes.

<!-- concept -->

Le code Scala tourne sur le compilateur just-in-time de la JVM, qui optimise le code chaud après un certain temps d'exécution. C'est pourquoi les micro-benchmarks ont besoin d'un préchauffage, que JMH gère, et pourquoi les jobs courts paient un coût de démarrage. Le ramasse-miettes récupère à faible coût les objets à courte durée de vie, mais des taux d'allocation très élevés se traduisent quand même par des pauses.

Le code générique fait du boxing des primitifs (une `List[Int]` contient des objets `java.lang.Integer`) : les boucles numériques chaudes utilisent des tableaux de primitifs. Choisir la bonne collection et éviter les collections intermédiaires apporte les plus gros gains ; mesurez avant d'optimiser.

<!-- example -->

```scala
// boxes every element and builds two intermediate lists
val slow = values.map(_ * 2).filter(_ > 10).sum

// one pass over a primitive array, no allocation
val arr: Array[Double] = values.toArray
var i = 0
var acc = 0.0
while i < arr.length do
  val v = arr(i) * 2
  if v > 10 then acc += v
  i += 1
```

#### Qu'est-ce que le boxing, et quand se produit-il en Scala ?

Envelopper une valeur primitive dans un objet (`Int` en `java.lang.Integer`) pour l'utiliser là où un objet est attendu. Il se produit dans les collections et méthodes génériques, dans `Option[Int]` et dans les valeurs fonction, et coûte allocations et indirections dans les boucles chaudes. Les tableaux de primitifs l'évitent.

#### Comment faire un benchmark correct de code Scala ?

Avec JMH via le plugin sbt-jmh, qui gère le préchauffage de la JVM, les forks, l'élimination de code mort et les statistiques. Chronométrer une seule exécution avec `System.nanoTime` mesure surtout l'interpréteur et le compilateur JIT, pas votre code.

#### Qu'est-ce que le préchauffage du JIT ?

La JVM interprète d'abord le bytecode, puis compile en code machine optimisé les méthodes souvent exécutées. Le code accélère après des milliers d'exécutions : les premières secondes d'un job ou d'un benchmark sont plus lentes que le régime établi.

#### Comment le ramasse-miettes affecte-t-il les programmes Scala ?

Le code immuable alloue beaucoup d'objets à courte durée de vie, que les collecteurs générationnels comme G1 (par défaut) récupèrent à faible coût. Les problèmes viennent de taux d'allocation très élevés ou de gros volumes de données vivantes ; la taille du heap (`-Xmx`), le choix du collecteur (ZGC pour des pauses courtes) et moins d'allocations sont les leviers.

#### Pourquoi éviter les exceptions comme flux de contrôle ?

Créer une exception capture une trace de pile, ce qui coûte cher, et cache le chemin d'échec aux types. Renvoyez `Option` ou `Either` pour les échecs attendus ; pour un flux de contrôle par exceptions inévitable, `scala.util.control.NoStackTrace` évite la capture de la pile.

<!-- challenge -->

Un service de tarification est lent, et un profileur montre 40 % du temps CPU dans le ramasse-miettes et le boxing. La boucle chaude somme des valeurs d'une `List[Double]` via plusieurs `map` et `filter`. Que faites-vous ?

<!-- solution -->

Réécrire le chemin chaud en une seule passe sur un `Array[Double]` (une boucle `while` ou un unique fold sur une view), en supprimant les collections intermédiaires et le boxing ; puis confirmer le gain avec un benchmark JMH et le profileur.

<!-- takeaways -->

- Le code générique fait du boxing des primitifs.
- Benchmarkez avec JMH, après préchauffage.
- Supprimez les collections intermédiaires des boucles chaudes.

<!-- stage: Tout assembler -->

### Scénarios

<!-- unit: Concevoir un job de données en Scala -->

<!-- goals -->

- Structurer un job Spark en Scala pour qu'il soit testable et sûr à relancer.
- Combiner modèles typés, configuration, tests et packaging.

<!-- concept -->

Un job Scala de production réunit les unités précédentes : configuration chargée et vérifiée au démarrage, case classes aux frontières, transformations écrites comme des fonctions pures de DataFrame vers DataFrame et testées sur de petites données, entrées et sorties dans un `main` mince, et un build qui produit un seul artefact pour le cluster. Les écritures idempotentes, qui remplacent une partition au lieu d'y ajouter des données, rendent les relances sûres.

<!-- example -->

```scala
object DailyRevenueJob {
  def transform(orders: DataFrame, day: String): DataFrame =
    orders.filter(col("order_date") === day && col("status") === "paid")
      .groupBy("country").agg(sum("amount").as("revenue"))
      .withColumn("order_date", lit(day))

  def main(args: Array[String]): Unit = {
    val Array(input, output, day) = args
    val spark = SparkSession.builder().appName("daily-revenue").getOrCreate()
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
    transform(spark.read.parquet(input), day)
      .write.mode("overwrite").partitionBy("order_date").parquet(output)
  }
}
```

#### Comment structurer un job Spark en Scala pour le rendre testable ?

Séparer les transformations pures (fonctions `DataFrame => DataFrame` dans un object) de la lecture, de l'écriture et de la configuration dans `main`. Les tests appellent les transformations sur de petits DataFrames avec une session locale partagée ; `main` reste assez mince pour ne demander qu'un test d'intégration.

#### Comment rendre idempotentes les écritures d'un job Spark ?

Écraser exactement la tranche que produit l'exécution : écrasement dynamique de partitions pour les tables Parquet, `replaceWhere` ou `MERGE` pour les tables Delta et Iceberg. Un simple `append` duplique les données à chaque relance.

#### Comment passer arguments et configuration à un job Spark ?

Des arguments de ligne de commande après le JAR dans `spark-submit`, analysés avec une bibliothèque comme scopt ou decline ; les paramètres Spark avec `--conf` ; les valeurs propres à chaque environnement depuis des fichiers de configuration ou l'environnement, validées au démarrage.

<!-- challenge -->

Un job quotidien écrit avec `mode("append")`, et une relance après un timeout a doublé le chiffre d'affaires d'une journée. Réécrivez sa stratégie d'écriture.

<!-- solution -->

Écrire avec `mode("overwrite")`, partitionné par date et avec `partitionOverwriteMode` à `dynamic`, pour qu'une exécution ne remplace que la partition de sa journée (ou utiliser `replaceWhere` sur une table Delta) ; les relances laissent alors les mêmes données.

<!-- takeaways -->

- Transformations pures, `main` mince.
- Écrasez la tranche ; n'ajoutez jamais à l'aveugle.
- Validez d'abord arguments et configuration.

<!-- unit: Exercices de code en Scala -->

<!-- goals -->

- Résoudre des exercices de code courants de façon idiomatique en Scala.
- Expliquer les compromis entre solutions fonctionnelles et impératives.

<!-- concept -->

En live coding, les recruteurs cherchent d'abord un code correct et idiomatique : valeurs immuables, méthodes de collection, pattern matching et `Option` au lieu de `null`. Annoncez la complexité, commencez par la version la plus claire et ne passez à la mutation locale ou aux tableaux que si vous pouvez expliquer pourquoi c'est plus rapide.

<!-- example -->

```scala
def fizzBuzz(n: Int): List[String] =
  (1 to n).map {
    case i if i % 15 == 0 => "FizzBuzz"
    case i if i % 3 == 0  => "Fizz"
    case i if i % 5 == 0  => "Buzz"
    case i                => i.toString
  }.toList
```

#### Inversez l'ordre des mots d'une phrase.

```scala
def reverseWords(s: String): String = s.trim.split("\\s+").reverse.mkString(" ")
```

#### Trouvez la deuxième plus grande valeur distincte d'une liste.

```scala
def secondLargest(xs: List[Int]): Option[Int] =
  xs.distinct.sorted.reverse.lift(1)
```

C'est du O(n log n) ; un seul `foldLeft` qui suit les deux plus grandes valeurs le ramène à O(n).

#### Trouvez la longueur de la plus longue sous-chaîne sans caractère répété.

```scala
def longestUnique(s: String): Int =
  s.indices.foldLeft((0, 0, Map.empty[Char, Int])) { case ((best, start, last), i) =>
    val newStart = last.get(s(i)).filter(_ >= start).map(_ + 1).getOrElse(start)
    (best.max(i - newStart + 1), newStart, last.updated(s(i), i))
  }._1
```

#### Implémentez une recherche dichotomique sur un tableau trié.

```scala
import scala.annotation.tailrec

def binarySearch(xs: Array[Int], target: Int): Option[Int] =
  @tailrec def go(lo: Int, hi: Int): Option[Int] =
    if lo > hi then None
    else
      val mid = lo + (hi - lo) / 2
      if xs(mid) == target then Some(mid)
      else if xs(mid) < target then go(mid + 1, hi)
      else go(lo, mid - 1)
  go(0, xs.length - 1)
```

#### Aplatissez une structure d'entiers imbriquée à une profondeur quelconque.

Modélisez l'imbrication avec un enum, puis parcourez récursivement :

```scala
enum Nested:
  case Leaf(value: Int)
  case Node(children: List[Nested])

def flatten(n: Nested): List[Int] = n match
  case Nested.Leaf(v)  => List(v)
  case Nested.Node(cs) => cs.flatMap(flatten)
```

<!-- challenge -->

Après votre FizzBuzz, le recruteur demande une version qui gère n = 100 millions sans construire toute la liste en mémoire. Que changez-vous ?

<!-- solution -->

Renvoyer un `Iterator[String]` (`(1 to n).iterator.map { ... }`) ou une view au lieu d'une `List`, pour que les valeurs soient produites à la demande et que l'appelant puisse les traiter en flux.

<!-- takeaways -->

- D'abord correct et idiomatique, puis optimisé.
- Annoncez complexité et compromis.
- Utilisez des itérateurs pour les sorties grandes ou infinies.
