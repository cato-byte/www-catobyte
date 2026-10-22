## Guía de estudio de Scala

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Guía de estudio de Scala: unas 220 preguntas](../../images/scala_study_guide_title_img.png)

Unas 220 preguntas de Scala para entrevistas de ingeniería de datos: el lenguaje y su sistema de tipos, las colecciones y la programación funcional, las abstracciones contextuales, la concurrencia, las herramientas y la interoperabilidad con Java, Scala con Apache Spark, y una serie de problemas de programación con sus soluciones. Los ejemplos usan la sintaxis de Scala 3 (3.9 LTS, publicada en septiembre de 2026), salvo los de Spark, que corre sobre Scala 2.13. Las respuestas siguen la documentación oficial de docs.scala-lang.org.

La guía sigue una ruta de aprendizaje en seis etapas. Cada sección se divide en unidades cortas: objetivos de aprendizaje, una explicación del concepto y un ejemplo resuelto, luego preguntas (primero de memoria, después de aplicación), un reto práctico e ideas clave. Para **aprender**, lee cada unidad de principio a fin. Para **repasar**, cambia al modo repaso o usa "Ir a las preguntas", marca las respuestas que quieras volver a ver y prueba un repaso mixto entre secciones.

<!-- QA -->
<!-- stage: Fundamentos -->

### Bases de Scala

<!-- unit: Scala y la JVM -->

<!-- goals -->

- Explicar qué es Scala, cómo se ejecuta y cómo se relacionan Scala 2 y Scala 3.
- Elegir una versión de Scala y ejecutar código con el comando `scala`.

<!-- concept -->

Scala combina la programación orientada a objetos y la funcional en un lenguaje de tipado estático que compila a bytecode de la JVM. Todo valor es un objeto, las funciones son valores y el compilador infiere la mayoría de los tipos, así que el código es conciso y los errores de tipo aparecen antes de ejecutarlo.

Scala 3 rediseñó el lenguaje en 2021 con una sintaxis más limpia, givens en lugar de implicits, enums y tipos unión. Las versiones siguen dos líneas: Scala Next recibe funcionalidades nuevas y las versiones de soporte extendido (LTS) reciben correcciones durante años. Spark, la principal razón por la que los ingenieros de datos se encuentran con Scala, sigue corriendo sobre Scala 2.13.

<!-- example -->

```scala
// hello.scala
@main def hello(name: String): Unit =
  println(s"Hello, $name")
```
```bash
scala run hello.scala -- Ana      # compiles and runs; prints "Hello, Ana"
```

#### ¿Qué es Scala?

Un lenguaje de tipado estático para la JVM que une la programación orientada a objetos y la funcional. Su nombre viene de "scalable language". Se usa en Apache Spark, en el código original de Kafka, en sistemas con Pekko y Akka y en servicios backend, y también compila a JavaScript (Scala.js) y a código nativo (Scala Native).

#### ¿Cómo se ejecuta el código Scala?

El compilador convierte los archivos `.scala` en archivos `.class` de la JVM (Scala 3 también escribe archivos `.tasty` con el árbol tipado del programa), y la JVM los ejecuta con su compilador just-in-time. El código Scala puede llamar directamente cualquier biblioteca Java, y Java puede llamar a Scala.

#### ¿Cuáles son las principales diferencias entre Scala 2 y Scala 3?

Scala 3 añade la sintaxis con llaves opcionales, `given` y `using` en lugar de implicits, métodos de extensión, enums, tipos unión e intersección, tipos opacos, definiciones de nivel superior, parámetros en traits y un nuevo sistema de macros basado en `inline` y quotes. La mayoría del código Scala 2.13 compila con pocos cambios, y los proyectos Scala 3 pueden usar bibliotecas de Scala 2.13, pero las macros de Scala 2 hay que reescribirlas.

#### ¿Qué son Scala LTS y Scala Next?

Dos líneas de versiones. Scala Next publica versiones menores con funcionalidades nuevas (3.10 en octubre de 2026). Una versión LTS recibe al menos tres años de correcciones sin cambios en el lenguaje: 3.3 fue la primera, y 3.9, publicada en septiembre de 2026, es la nueva hacia la que migran las bibliotecas. Desde 3.8, Scala 3 requiere JDK 17 o posterior.

#### ¿Qué versión de Scala usa Spark?

Spark 4 se compila solo para Scala 2.13 (Spark 3 soportaba 2.12 y 2.13). No hay una versión oficial para Scala 3: Scala 3 puede depender de los artefactos 2.13, pero los encoders de Spark dependen de funcionalidades de Scala 2, así que los jobs de Spark se escriben en Scala 2.13 o necesitan bibliotecas de la comunidad.

#### ¿Qué es el comando `scala`?

Desde Scala 3.5, `scala` es la Scala CLI: compila, ejecuta, prueba y empaqueta proyectos de un solo módulo sin archivo de build (`scala run`, `scala repl`, `scala test`, `scala package`), con las dependencias y versiones declaradas en directivas `//> using` al inicio de un archivo.

#### ¿Qué es un método `@main`?

Una anotación de Scala 3 que convierte un método de nivel superior en el punto de entrada de un programa y analiza los argumentos de la línea de comandos según el tipo de cada parámetro. En Scala 2, el punto de entrada es un `def main(args: Array[String]): Unit` dentro de un object, o un object que extiende `App`.

<!-- challenge -->

Un equipo quiere escribir un job nuevo de Spark en Scala 3 porque "es la versión actual". ¿Qué le recomiendas?

<!-- solution -->

Escribir el job en Scala 2.13, la versión para la que Spark 4 se compila y se prueba; Scala 3 solo funciona con Spark mediante soluciones alternativas para los encoders y las bibliotecas. Usar Scala 3 para servicios y bibliotecas fuera de Spark.

<!-- takeaways -->

- Scala es un lenguaje POO y funcional de tipado estático sobre la JVM.
- Scala Next añade funcionalidades; las versiones LTS reciben correcciones durante años.
- Los jobs de Spark usan Scala 2.13.

<!-- unit: Valores, variables y tipos -->

<!-- goals -->

- Usar `val`, `var` y `lazy val`, y apoyarse en la inferencia de tipos.
- Recorrer la jerarquía de tipos de Scala, los tipos numéricos y la igualdad.

<!-- concept -->

Scala prefiere los enlaces inmutables: un `val` no se puede reasignar, un `var` sí, y el código idiomático rara vez necesita `var`. El compilador infiere los tipos a partir del lado derecho, pero los métodos públicos siguen declarándolos para que sean legibles y la API sea estable.

Todos los tipos están en una sola jerarquía: `Any` arriba, dividido en tipos de valor (`Int`, `Double`, `Boolean`, `Unit`) y tipos de referencia (`AnyRef`, el `Object` de Java). `Nothing` está abajo, el tipo de las expresiones que nunca retornan, como una excepción lanzada. `==` llama a `equals`, así que compara valores, incluso con cadenas.

<!-- example -->

```scala
val rate = 0.19                  // Double, inferred
var retries = 0                  // reassignable: use sparingly
lazy val lookup = loadLookup()   // computed on first access, only once
val total: BigDecimal = BigDecimal("19.99") * 3
println("ab" + "c" == "abc")     // true: == compares values
def fail(msg: String): Nothing = throw IllegalStateException(msg)
```

#### ¿Cuál es la diferencia entre `val`, `var` y `lazy val`?

Un `val` se asigna una vez y no se puede reasignar (el objeto al que apunta puede seguir siendo mutable). Un `var` se puede reasignar. Un `lazy val` se calcula la primera vez que se accede a él, como máximo una vez y de forma segura entre hilos, lo que aplaza el trabajo costoso hasta que hace falta.

#### ¿Qué es la inferencia de tipos y cuándo conviene escribir los tipos igual?

El compilador deduce los tipos a partir de valores y expresiones, así que `val n = 1` es un `Int`. Escribe los tipos en métodos y campos públicos (documentan la API y la mantienen estable), en métodos recursivos (obligatorio), en los givens y cuando el tipo inferido es demasiado específico, como un `Some[Int]` donde quieres un `Option[Int]`.

#### ¿Qué son `Any`, `AnyVal`, `AnyRef`, `Nothing` y `Null`?

`Any` es el supertipo de todo. `AnyVal` es el padre de los tipos de valor (`Int`, `Double`, `Boolean`, `Char`, `Unit`) y `AnyRef` el de los tipos de referencia. `Nothing` es subtipo de todos los tipos y no tiene valores; es el tipo de `throw` y de colecciones vacías como `Nil`. `Null` es el tipo de `null`, subtipo de los tipos de referencia.

#### ¿Qué es `Unit`?

Un tipo con un único valor, `()`, que devuelven los métodos que se llaman por sus efectos secundarios, como el `void` de Java. Como es un valor real, toda expresión en Scala tiene un tipo, incluso un `println`.

#### ¿Cuál es la diferencia entre `==` y `eq`?

`==` llama a `equals`, compara valores y maneja `null` sin fallar, así que `"abc" == "ab" + "c"` es verdadero, a diferencia de Java. `eq` compara referencias (si ambos nombres apuntan al mismo objeto) y solo existe en `AnyRef`.

#### ¿Cómo se comportan los tipos numéricos de Scala?

`Int` (32 bits) y `Long` (64 bits) se desbordan sin avisar, `Double` es un número de punto flotante binario, y `BigInt` y `BigDecimal` dan precisión arbitraria, que es lo que necesita el dinero. La división entera trunca hacia cero (`7 / 2 == 3`, `-7 / 2 == -3`), y los guiones bajos hacen legibles los literales: `1_000_000`.

<!-- challenge -->

Una clase calcula una tabla de búsqueda costosa en un campo `val`, pero la mayoría de las instancias nunca la usan, y crearlas es lento. ¿Qué cambias?

<!-- solution -->

Conviértelo en `lazy val`: se calcula en el primer acceso, como máximo una vez, así que las instancias que nunca usan la tabla no pagan por ella.

<!-- takeaways -->

- Prefiere `val`; `lazy val` aplaza el trabajo.
- `Any` está arriba, `Nothing` abajo.
- `==` compara valores; `eq` compara referencias.

<!-- unit: Expresiones y estructuras de control -->

<!-- goals -->

- Usar `if`, `match`, `for` y `try` como expresiones.
- Leer la sintaxis de llaves opcionales de Scala 3 y reemplazar `break` y `continue`.

<!-- concept -->

En Scala casi todo es una expresión que devuelve un valor: `if`, `match`, `try` y los bloques, cuyo valor es su última expresión. Eso elimina variables temporales, y el código se lee como la definición del resultado en lugar de una serie de asignaciones.

Scala 3 también permite que la indentación reemplace las llaves, con las palabras clave `then` y `do`, el estilo de la documentación oficial. Las llaves siguen funcionando, y muchos proyectos, incluidos los de Spark en Scala 2.13, las mantienen.

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

#### ¿Qué significa que "todo es una expresión" en Scala?

Construcciones que en otros lenguajes son sentencias devuelven valores: `if`/`else`, `match`, `try`/`catch` y los bloques `{ ... }`, cuyo valor es su última expresión. Asignas su resultado directamente a un `val` en lugar de modificar una variable en cada rama.

#### ¿Cómo funciona `if`/`else` como expresión?

`val label = if amount > 0 then "credit" else "debit"`. Ambas ramas determinan el tipo del resultado; sin `else`, el resultado es `Unit`. Scala no tiene operador ternario porque `if` ya cumple ese papel.

#### ¿Cuál es la diferencia entre un bucle `for` y una comprensión `for`?

`for x <- xs do ...` ejecuta un efecto secundario por elemento y devuelve `Unit`. `for x <- xs yield ...` construye una colección nueva (o un Option, un Future...) con los resultados. Ambos se traducen en llamadas a métodos (`foreach`, `map`, `flatMap`, `withFilter`).

#### ¿Tiene Scala `break` y `continue`?

No como palabras clave. Usa métodos de colección que se detienen antes (`find`, `exists`, `takeWhile`), recursión o, desde Scala 3.3, `scala.util.boundary` con `break` para salir de un bloque con un valor.

#### ¿Qué es la sintaxis de llaves opcionales?

Scala 3 puede usar la indentación para delimitar bloques, con `then` después de las condiciones de `if`, `do` en los bucles y marcadores `end` opcionales para bloques largos. Las llaves siguen siendo válidas y ambos estilos se pueden mezclar; los formateadores y el compilador (`-rewrite -indent` o `-no-indent`) convierten de uno a otro.

#### ¿Cómo funciona `try`/`catch`/`finally` en Scala?

Es una expresión: `catch` recibe casos de pattern matching sobre tipos de excepción, y `finally` hace la limpieza sin afectar el resultado. Scala no tiene excepciones comprobadas. Para fallos esperados, `Try`, `Either` y `Using` suelen ser más claros que capturar excepciones.

<!-- challenge -->

Código como `var status = ""` seguido de `if (paid) status = "done" else status = "open"` aparece en todo un proyecto. Reescríbelo de forma idiomática.

<!-- solution -->

`val status = if paid then "done" else "open"`: la expresión `if` devuelve el valor directamente, sin variable mutable y sin riesgo de olvidar una rama.

<!-- takeaways -->

- `if`, `match`, `try` y los bloques devuelven valores.
- `for ... do` recorre; `for ... yield` construye resultados.
- No hay `break`: usa métodos de colección o `boundary`.

<!-- unit: Cadenas e interpolación -->

<!-- goals -->

- Construir cadenas con los interpoladores `s`, `f` y `raw` y con literales multilínea.
- Dividir, convertir y transformar cadenas de forma segura.

<!-- concept -->

Las cadenas de Scala son cadenas de Java: secuencias inmutables de caracteres con todos los métodos de Java, más los métodos de colección de Scala como `map`, `filter` y `reverse`. La interpolación construye texto a partir de valores: `s` los inserta, `f` les da formato al estilo printf con comprobación de tipos, y `raw` deja las barras invertidas tal cual.

Las cadenas con triple comilla ocupan varias líneas sin escapar nada, y `stripMargin` quita la indentación hasta un `|` para que el literal siga la indentación del código.

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

#### ¿Qué interpoladores de cadenas tiene Scala?

`s"..."` inserta valores (`$name` o `${expr}`), `f"..."` les da formato con especificaciones al estilo printf comprobadas en compilación (`$total%.2f`), y `raw"..."` no procesa las secuencias de escape. Las bibliotecas definen los suyos, como `sql"..."` en Doobie, que construye consultas parametrizadas.

#### ¿Cómo funcionan las cadenas multilínea y `stripMargin`?

Los literales `"""..."""` ocupan varias líneas y no necesitan escapar comillas ni barras invertidas. `stripMargin` elimina en cada línea los espacios iniciales hasta un `|` inclusive, así que el texto puede indentarse junto con el código que lo rodea.

#### ¿Cómo construyes una cadena larga de forma eficiente?

Reúne las partes y usa `mkString` (`rows.mkString("\n")`, con prefijo y sufijo opcionales), o un `StringBuilder` dentro de un bucle. Repetir `+` sobre cadenas copia la cadena creciente cada vez.

#### Invierte una cadena y comprueba si es un palíndromo, ignorando mayúsculas y puntuación.

```scala
def isPalindrome(s: String): Boolean =
  val letters = s.filter(_.isLetterOrDigit).toLowerCase
  letters == letters.reverse
```

#### ¿Cómo divides y conviertes cadenas de forma segura?

`split` recibe una expresión regular, así que los caracteres especiales como `|` y `.` se deben escapar (`split("\\|")`) o pasar como `Char` (`split('|')`). Usa `trim` o `strip` para los espacios, y `toIntOption`, `toDoubleOption` o `toBooleanOption`, que devuelven `None` en lugar de lanzar una excepción con una entrada inválida.

<!-- challenge -->

`line.split("|")` devuelve cada carácter por separado en lugar de los campos. ¿Por qué y cómo lo corriges?

<!-- solution -->

`split` recibe una regex, y `|` solo significa "vacío o vacío", que coincide entre cada carácter. Escápalo (`line.split("\\|")`) o usa la sobrecarga con `Char`, `line.split('|')`.

<!-- takeaways -->

- `s`, `f` y `raw` interpolan; `f` comprueba los formatos.
- Usa `mkString` en lugar de `+` repetido.
- `split` recibe una regex; convierte con `toIntOption`.

### Métodos y funciones

<!-- unit: Métodos -->

<!-- goals -->

- Definir métodos con parámetros por defecto, con nombre y repetidos.
- Usar varias listas de parámetros y parámetros por nombre (by-name).

<!-- concept -->

Los métodos se definen con `def` en una clase, un object o, en Scala 3, en el nivel superior de un archivo. Los argumentos por defecto y con nombre reemplazan la mayoría de las sobrecargas y los builders, y los parámetros repetidos aceptan cualquier número de argumentos. Un método puede tener varias listas de parámetros, lo que ayuda a la inferencia de tipos, permite pasar un bloque como último argumento y separa los parámetros de contexto.

Los parámetros by-name (`=> A`) se evalúan cada vez que se usan dentro del método, no antes de la llamada, lo que permite recibir código para ejecutarlo más tarde o nunca, como en un helper de reintentos o un mensaje de log.

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

#### ¿Cuál es la diferencia entre un método y una función en Scala?

Un método se define con `def` y pertenece a una clase, un object o un archivo; no es un valor por sí mismo. Una función es un objeto de un tipo función como `Int => Int` que puedes guardar y pasar. Scala convierte automáticamente los métodos en funciones cuando se espera una función (eta-expansion).

#### ¿Qué son los argumentos por defecto y con nombre?

Los parámetros pueden tener valores por defecto (`port: Int = 5432`), y quien llama puede pasar los argumentos por nombre en cualquier orden (`connect("db", ssl = false)`). Juntos reemplazan la mayoría de los métodos sobrecargados y las clases builder, y hacen que las llamadas se expliquen solas.

#### ¿Qué son los parámetros repetidos?

Un parámetro de tipo `Int*` acepta cualquier número de argumentos, que recibe como un `Seq[Int]`. Para pasar una colección existente, se expande: `total(xs*)` en Scala 3, `total(xs: _*)` en Scala 2.

#### ¿Para qué sirven varias listas de parámetros?

La inferencia de tipos avanza de una lista a la siguiente (`foldLeft(0)(_ + _)` conoce el tipo del acumulador por la primera lista), una última lista de un solo argumento puede recibir un bloque entre llaves (`retry(3) { ... }`), y los parámetros de contexto van en una lista `using` aparte. También permiten el currying.

#### ¿Qué es un parámetro by-name?

Un parámetro declarado `op: => A` no se evalúa en la llamada; la expresión se pasa sin evaluar y se ejecuta cada vez que el método la usa. Así reciben código para más tarde métodos como `getOrElse`, los mensajes de `assert` o los helpers de reintentos, y se evita calcular valores que quizá no hagan falta.

#### ¿Por qué los métodos recursivos deben declarar su tipo de retorno?

El compilador infiere el tipo de un método a partir de su cuerpo, pero un cuerpo recursivo depende del propio tipo del método, así que la inferencia no puede terminar. Declarar el tipo de retorno rompe el ciclo.

<!-- challenge -->

Un helper `def debug(msg: String): Unit` se llama como `debug(s"rows: ${dump(df)}")`, y el costoso `dump` se ejecuta aunque el log de depuración esté apagado. ¿Cómo lo corriges?

<!-- solution -->

Haz que el parámetro sea by-name, `def debug(msg: => String)`, y evalúa `msg` solo cuando el log de depuración esté activo; si no, la cadena, y `dump`, nunca se construyen.

<!-- takeaways -->

- Los argumentos por defecto y con nombre reemplazan las sobrecargas.
- Varias listas de parámetros ayudan a la inferencia y a pasar bloques.
- Los parámetros by-name aplazan la evaluación.

<!-- unit: Funciones como valores -->

<!-- goals -->

- Escribir funciones anónimas y usar funciones de orden superior.
- Explicar closures, eta-expansion, currying y composición de funciones.

<!-- concept -->

Las funciones son valores con tipos como `Int => Int`. Las pasas a métodos como `map`, las devuelves desde métodos y las guardas en colecciones, y las cortas pueden usar `_` en lugar de sus parámetros.

Un método se convierte en función automáticamente cuando se espera una (eta-expansion). Una función que usa variables del ámbito donde se creó las captura, y eso la convierte en un closure. El currying separa los parámetros en listas distintas, así que fijar las primeras produce una función nueva, más específica.

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

#### ¿Qué es una función anónima?

Un literal de función sin nombre: `(x: Int) => x * 2`, o `x => x * 2` cuando el tipo se conoce por el contexto. Es un objeto de un tipo función y se puede pasar directamente a métodos de orden superior.

#### ¿Qué significa el guion bajo en `_ + 1`?

Cada `_` representa el siguiente parámetro de una función anónima: `_ + 1` es `x => x + 1`, y `_ + _` es `(a, b) => a + b`. Solo funciona cuando cada parámetro se usa una vez y en orden.

#### ¿Qué es una función de orden superior?

Una función o método que recibe funciones como parámetros o devuelve una, como `map`, `filter`, `foldLeft`, `sortBy` o un helper `retry`. Permiten separar qué hacer con cada elemento de cómo recorrerlos.

#### ¿Qué es un closure?

Una función que captura variables del ámbito donde se definió, como `k` en `x => x * k`. Captura variables, no valores, así que los cambios en un `var` capturado son visibles para la función. En Spark, todo lo que captura un closure se serializa y se envía a los executors.

#### ¿Qué es la eta-expansion?

La conversión automática de un método en un valor función, como en `nums.filter(isEven)`. Scala 3 la hace siempre que un método se usa donde se espera una función; Scala 2 a veces necesitaba un `isEven _` explícito.

#### ¿Qué son el currying y la aplicación parcial?

El currying convierte un método con varios parámetros en una cadena de listas de un parámetro: `def add(a: Int)(b: Int) = a + b`. Aplicar la primera lista da una función que espera el resto: `val add5 = add(5)` (`add(5) _` en Scala 2). La aplicación parcial también puede fijar cualquier argumento con marcadores: `connect("db.local", _, true)`.

#### ¿Qué son los tipos función y la composición?

`A => B` es una abreviatura del trait `Function1[A, B]` (con `Function2` y siguientes para más parámetros). Las funciones se componen: `f andThen g` aplica primero `f`, `f compose g` aplica primero `g`, lo que construye pipelines a partir de pasos pequeños.

<!-- challenge -->

La limpieza de texto está escrita como llamadas anidadas, `stripAccents(lower(trim(s)))`, repetidas en muchos lugares con pasos añadidos u olvidados. ¿Cómo la haces reutilizable?

<!-- solution -->

Define cada paso como un valor función (`val trim: String => String = _.trim`, etc.) y compónlos una sola vez: `val normalize = trim andThen lower andThen stripAccents`. Quien la necesite llama a `normalize(s)`, y el pipeline vive en un solo lugar.

<!-- takeaways -->

- Las funciones son valores con tipos como `A => B`.
- Los closures capturan variables de su ámbito.
- Compón funciones pequeñas con `andThen`.

<!-- unit: Funciones parciales -->

<!-- goals -->

- Escribir funciones anónimas con pattern matching y funciones parciales.
- Usar `collect` y `lift`.

<!-- concept -->

Un bloque de cláusulas `case` es una función anónima que compara su argumento con patrones. Cuando los casos no cubren todas las entradas, es una función parcial: un `PartialFunction[A, B]` puede decir con `isDefinedAt` si se aplica a un valor.

Métodos de colección como `collect` lo aprovechan para filtrar y transformar en un solo paso, conservando solo los elementos que coinciden con los casos.

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

#### ¿Qué es una función parcial?

Una función definida solo para algunas entradas, de tipo `PartialFunction[A, B]` y escrita normalmente como un bloque de cláusulas `case`. `isDefinedAt(x)` dice si maneja `x`; llamarla con otras entradas lanza un `MatchError`.

#### ¿En qué se diferencia `collect` de `map` y `filter`?

`collect` recibe una función parcial y conserva solo los elementos para los que está definida, transformados por ella: filtra y transforma en una pasada, con pattern matching para extraer valores. `collectFirst` devuelve el primer resultado como un `Option`.

#### ¿Qué hace `lift`?

Convierte un `PartialFunction[A, B]` en una función total `A => Option[B]` que devuelve `None` donde la función parcial no está definida, lo que evita los `MatchError`.

#### ¿Cómo descompones tuplas en lambdas?

Con una lambda de casos, `pairs.map { case (k, v) => s"$k=$v" }`, que funciona en Scala 2 y 3. Scala 3 además destupla los parámetros automáticamente: `pairs.map((k, v) => s"$k=$v")`.

<!-- challenge -->

Un código extrae valores ya convertidos con `results.filter(_.isRight).map(_.toOption.get)`. ¿Cómo lo simplificas?

<!-- solution -->

`results.collect { case Right(v) => v }`: una pasada, sin `.get`, y el patrón deja clara la intención.

<!-- takeaways -->

- Los bloques `case` son funciones con pattern matching.
- `collect` filtra y transforma en un paso.
- `lift` hace que las funciones parciales devuelvan Options.

### Modelado del dominio

<!-- unit: Clases, objects y traits -->

<!-- goals -->

- Definir clases, objects singleton y objects compañeros.
- Componer comportamiento con traits y entender la linealización.

<!-- concept -->

Una clase declara los parámetros de su constructor en el encabezado; con `val` delante, un parámetro se vuelve un campo público. Scala no tiene `static`: un `object` singleton contiene lo que serían miembros estáticos, y un object con el mismo nombre que una clase, su compañero, puede acceder a los miembros privados de la clase y suele alojar los métodos de fábrica.

Los traits definen interfaces con implementaciones opcionales y se mezclan en las clases. Cuando varios traits definen el mismo método, la linealización decide el orden, y las llamadas a `super` van al siguiente trait en ese orden.

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

#### ¿Cómo defines una clase con parámetros de constructor?

Los parámetros van en el encabezado de la clase, que es el constructor primario; el cuerpo de la clase se ejecuta como código del constructor. Un parámetro se vuelve campo público con `val` (o `var`) y, si no, queda privado a la clase. Los constructores adicionales se escriben como `def this(...)`. En Scala 3, `new` es opcional.

#### ¿Qué es un object singleton?

Un `object` define a la vez una clase y su única instancia, creada de forma perezosa en el primer uso. Contiene utilidades, constantes y puntos de entrada, y reemplaza los miembros estáticos de Java.

#### ¿Qué es un object compañero?

Un object con el mismo nombre que una clase, en el mismo archivo. La clase y su compañero pueden acceder a los miembros privados del otro; el compañero suele contener métodos de fábrica (`apply`), constantes e instancias given para la clase.

#### ¿Qué es un trait y en qué se diferencia de una clase abstracta?

Un trait define miembros abstractos y concretos y se puede mezclar en una clase junto con otros traits (`extends A with B`, o `extends A, B` en Scala 3). Una clase extiende una sola clase abstracta. En Scala 3 los traits también aceptan parámetros, así que las clases abstractas se usan sobre todo por interoperabilidad con Java o cuando un constructor es imprescindible.

#### ¿Qué es la linealización de traits?

El orden en que Scala resuelve los miembros cuando varios traits mezclados los definen: aproximadamente de derecha a izquierda en la cláusula `extends`. `super.method()` dentro de un trait llama a la siguiente implementación en ese orden, lo que permite traits "apilables" que añaden comportamiento alrededor del mismo método.

#### ¿Qué hacen `require` y `assert`?

`require(cond, msg)` comprueba una precondición sobre los argumentos y lanza `IllegalArgumentException`. `assert(cond, msg)` comprueba un invariante interno y lanza `AssertionError`. Ambos hacen que los estados inválidos fallen pronto y con un mensaje claro.

#### ¿Qué modificadores de acceso tiene Scala?

Los miembros son públicos por defecto. `private` los limita a la clase y su compañero, `protected` a las subclases, y formas calificadas como `private[etl]` los abren a todo un paquete.

<!-- challenge -->

Una clase `DateUtils` no tiene estado, pero el código crea `new DateUtils()` en todas partes solo para llamar a `parse`. ¿Cómo la reestructuras?

<!-- solution -->

Conviértela en un `object DateUtils` (o en funciones de nivel superior en un archivo Scala 3), para llamar directamente a `DateUtils.parse(...)` sin crear instancias.

<!-- takeaways -->

- Los objects reemplazan los miembros estáticos.
- Los compañeros contienen fábricas y givens.
- Los traits mezclan comportamiento en las clases.

<!-- unit: Case classes, enums y ADTs -->

<!-- goals -->

- Modelar datos con case classes y enums.
- Construir tipos de datos algebraicos con sealed traits y enums.

<!-- concept -->

Las case classes son la forma estándar de modelar datos inmutables. El compilador genera un constructor sin `new`, accesores para los campos, igualdad estructural y hash, un `toString` legible, un método `copy` y soporte para pattern matching.

Combinadas, forman tipos de datos algebraicos: un sealed trait o un enum de Scala 3 enumera todos los casos posibles, así que el compilador avisa cuando a un match le falta uno. Las case classes son tipos producto ("esto y aquello"); los enums y las jerarquías selladas son tipos suma ("esto o aquello").

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

#### ¿Qué te da una case class?

Una fábrica `apply` (sin `new`), campos públicos inmutables, `equals` y `hashCode` basados en los campos, un `toString` legible, `copy`, un extractor `unapply` para pattern matching y serialización. Es la opción por defecto para registros de datos.

#### ¿Qué hace `copy`?

Crea una instancia nueva con algunos campos cambiados y el resto igual: `order.copy(status = Status.Paid)`. Es la forma de "actualizar" datos inmutables.

#### ¿Por qué marcar las case classes como `final`?

Extender una case class rompe de forma sutil la igualdad y el pattern matching generados, así que el estilo recomendado es `final case class`. Las variantes van en un sealed trait o en un enum con varios casos.

#### ¿Qué es un enum de Scala 3?

Un tipo con un conjunto fijo de casos. Los enums simples (`case Pending, Paid`) tienen `values`, `valueOf` y `ordinal`; los casos también pueden recibir parámetros, lo que hace de los enums una forma concisa de escribir tipos de datos algebraicos. Scala 2 expresaba lo mismo con un sealed trait y case objects.

#### ¿Qué es un tipo de datos algebraico?

Un tipo construido con productos (una case class que combina campos) y sumas (una elección entre casos). Modelar un evento de pago como "autorizado, capturado o fallido", cada uno con sus propios campos, hace imposible representar combinaciones inválidas.

#### ¿Qué significa `sealed`?

Un trait o clase sellado solo se puede extender en el mismo archivo, así que el compilador conoce todos los subtipos y puede comprobar que un `match` los cubra todos.

#### ¿Cuál es la diferencia entre una case class y una clase normal?

Una clase normal compara por referencia, no tiene `copy` ni extractor y mantiene privados los parámetros del constructor si no se marcan con `val`. Usa case classes para datos y clases normales para objetos con identidad, comportamiento y estado oculto.

#### ¿Qué es un case object?

Un singleton con las características de una case class (`toString` legible, pattern matching, serialización), usado en Scala 2 para los casos sin datos de una jerarquía sellada, como `case object Pending extends Status`.

<!-- challenge -->

El estado de un pedido es un campo `String`, y un error de tipeo, `"payed"`, llegó a los datos de producción. ¿Cómo puede evitarlo el sistema de tipos?

<!-- solution -->

Modela el estado como un enum (`Pending`, `Paid`, `Refunded`) y convierte las cadenas externas una sola vez en la frontera con una función que devuelva `Option` o `Either`, para que los valores inválidos se rechacen ahí y no puedan existir más adentro.

<!-- takeaways -->

- Las case classes modelan datos inmutables.
- Los enums y sealed traits enumeran todos los casos.
- Convierte las cadenas en tipos en la frontera.

<!-- unit: Pattern matching -->

<!-- goals -->

- Hacer match sobre valores, tipos, case classes y colecciones.
- Usar guardas, binders y extractores, y apoyarse en la comprobación de exhaustividad.

<!-- concept -->

`match` es un switch que además descompone valores. Compara un valor con patrones en orden y asocia partes de él a nombres: literales, tipos, case classes, tuplas y listas, con guardas para condiciones adicionales.

Con tipos sellados y enums, el compilador comprueba la exhaustividad y avisa de los casos que faltan, así que añadir un caso se convierte en una lista de advertencias del compilador por corregir en lugar de sorpresas en ejecución. Los extractores propios (`unapply`) permiten hacer match sobre cualquier tipo.

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

#### ¿Cómo funciona el pattern matching en Scala?

`value match { case pattern => result ... }` prueba cada caso en orden y evalúa el primero que coincide, asociando las variables del patrón. Es una expresión, así que devuelve el resultado elegido.

#### ¿Qué tipos de patrones existen?

Literales (`case 0`), variables y el comodín `_`, patrones con tipo (`case s: String`), patrones de constructor para case classes, tuplas (`case (k, v)`), secuencias (`case List(a, b, _*)`, `case x :: rest`), alternativas (`case "FR" | "BE"`) y binders que dan nombre a una parte coincidente (`case o @ Order(_, _, _, Status.Paid)`).

#### ¿Qué es una guarda?

Una condición `if` después de un patrón (`case Authorized(id, amt) if amt > 1000`). El caso coincide solo si se cumplen el patrón y la condición.

#### ¿Qué es la comprobación de exhaustividad?

En los match sobre sealed traits, enums, `Option` y tipos similares, el compilador avisa cuando un caso posible no está cubierto. Es uno de los mayores beneficios de modelar los datos con tipos algebraicos.

#### ¿Qué es un extractor?

Un objeto con un método `unapply` que decide si un valor coincide y qué asociar:

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

#### ¿Qué pasa si ningún caso coincide?

Se lanza un `scala.MatchError` en tiempo de ejecución. Las advertencias de exhaustividad lo evitan con los tipos sellados; para tipos abiertos como las cadenas, añade un `case _` final.

#### ¿Por qué no puedes distinguir con un match entre `List[String]` y `List[Int]`?

Los argumentos de tipo genéricos se borran en la JVM, así que en ejecución ambos son solo `List`. El compilador avisa de que ese patrón no se puede comprobar. Haz match sobre los elementos, o conserva la información de tipo con un `ClassTag` o un tipo envoltorio.

<!-- challenge -->

Se añadió un caso `Disputed` a `PaymentEvent`, y un reporte clasifica las disputas como "otro" sin avisar, a través de una rama `case _ =>`. ¿Cómo haces que el compilador detecte estos huecos?

<!-- solution -->

Quita el comodín de los match sobre tipos sellados y enums, para que el compilador avise de que `Disputed` no se maneja, y haz que el build de CI falle con advertencias (`-Werror`).

<!-- takeaways -->

- `match` prueba patrones en orden y asocia partes.
- Los tipos sellados dan comprobación de exhaustividad.
- Evita los comodines en los match sobre tus propios ADTs.

<!-- stage: Colecciones y programación funcional -->

### Colecciones

<!-- unit: La jerarquía de colecciones -->

<!-- goals -->

- Distinguir las colecciones inmutables de las mutables.
- Elegir entre `List`, `Vector`, `Array`, `Set` y `Map` según el patrón de acceso.

<!-- concept -->

Las colecciones de Scala vienen en versiones inmutables, las de por defecto, y mutables, en `scala.collection.mutable`. Las inmutables nunca cambian: las operaciones devuelven colecciones nuevas que comparten la mayor parte de su estructura con la anterior, así que son baratas de crear y seguras de compartir entre hilos.

Las familias principales son secuencias, conjuntos y mapas. Entre las secuencias, `List` es una lista enlazada rápida en la cabeza, `Vector` da acceso y actualizaciones rápidas en cualquier posición, `Array` es un arreglo mutable de Java y `ArrayBuffer` crece de forma eficiente. Elegir según el patrón de acceso importa más que cualquier microoptimización.

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

#### ¿Cuál es la diferencia entre colecciones inmutables y mutables?

Las colecciones inmutables no pueden cambiar después de crearse; "añadir" devuelve una colección nueva. Las mutables cambian en el lugar. Las inmutables son las de por defecto en Scala porque son seguras de compartir y más fáciles de razonar; las mutables sirven para código local y sensible al rendimiento.

#### ¿Cuándo usas `List` y cuándo `Vector`?

`List` es rápida para anteponer elementos, acceder a la cabeza y la cola y hacer pattern matching recursivo, pero indexar y añadir al final son O(n). `Vector` indexa, añade al final y actualiza en tiempo prácticamente constante. `Seq(...)` crea una `List`, `IndexedSeq(...)` un `Vector`.

#### ¿Qué es un `Array` en Scala?

Un arreglo de Java: tamaño fijo, mutable y almacenado de forma compacta (los primitivos sin boxing). Se usa para interoperabilidad y código sensible al rendimiento. `==` sobre arreglos compara referencias, así que compara su contenido con `sameElements`.

#### ¿Cómo funcionan los sets y los maps?

Los `Set` y `Map` por defecto se basan en hash y no tienen orden; `SortedSet` y `TreeMap` mantienen las claves ordenadas. `map(key)` lanza `NoSuchElementException` si falta la clave, mientras que `map.get(key)` devuelve un `Option` y `getOrElse` un valor por defecto.

#### ¿Qué es la compartición estructural?

Las colecciones inmutables reutilizan en la nueva colección las partes sin cambios de la anterior: `0 :: xs` apunta a `xs` en lugar de copiarla, y `Vector.updated` copia solo un camino corto de su árbol interno. Por eso las actualizaciones inmutables son asequibles.

#### ¿Cuál es la complejidad de las operaciones comunes de `List`?

`head`, `tail` y anteponer (`::`) son O(1). `length`, indexar con `apply`, `last` y añadir al final (`:+`) son O(n), porque hay que recorrer la lista.

#### ¿Qué es `Seq` en Scala 2.13 y 3?

`scala.Seq` es un alias de `scala.collection.immutable.Seq`. En Scala 2.12 era `scala.collection.Seq`, que también podía ser mutable, una fuente común de errores de compilación al migrar código que pasa arreglos o buffers como `Seq`.

<!-- challenge -->

Un job construye una `List` añadiendo al final dentro de un bucle, `acc = acc :+ row`, sobre un millón de filas, y tarda minutos. ¿Qué cambias?

<!-- solution -->

Cada `:+` copia toda la lista, lo que hace el bucle O(n²). Antepón y invierte una sola vez al final, usa un `ListBuffer` o un builder o, mejor, expresa el bucle como un `map` o `filter` sobre la fuente.

<!-- takeaways -->

- Las colecciones inmutables son las de por defecto.
- `List` es rápida en la cabeza; `Vector` en todas partes.
- Los arreglos son arreglos mutables de Java.

<!-- unit: Transformar colecciones -->

<!-- goals -->

- Aplicar `map`, `flatMap`, `filter`, folds y agrupaciones.
- Elegir el método adecuado para una agregación.

<!-- concept -->

Las colecciones comparten un gran conjunto de métodos de transformación. `map` transforma cada elemento, `filter` conserva algunos, `flatMap` transforma y aplana, y los folds combinan todo en un solo valor. Los métodos de agrupación dividen una colección por clave, el equivalente en memoria del `GROUP BY` de SQL.

Encadenar estos métodos reemplaza la mayoría de los bucles con código que dice cuál es el resultado, y el mismo vocabulario aparece en Spark, `Option`, `Future` y las bibliotecas de efectos.

<!-- example -->

```scala
final case class Sale(country: String, product: String, amount: Double)
val sales = List(Sale("FR", "a", 10), Sale("CO", "b", 5), Sale("FR", "b", 7))

val byCountry = sales.groupMapReduce(_.country)(_.amount)(_ + _)   // Map(FR -> 17.0, CO -> 5.0)
val total = sales.foldLeft(0.0)((acc, s) => acc + s.amount)        // 22.0
val (big, small) = sales.partition(_.amount >= 7)
val top = sales.sortBy(-_.amount).take(2)
```

#### ¿Cuál es la diferencia entre `map` y `flatMap`?

`map` aplica una función a cada elemento y conserva la estructura: `List(1, 2).map(x => List(x, x))` es `List(List(1, 1), List(2, 2))`. `flatMap` aplica una función que devuelve una colección y aplana los resultados: `List(1, 1, 2, 2)`.

#### ¿Cuál es la diferencia entre `foldLeft`, `foldRight` y `reduce`?

`foldLeft(init)(op)` combina los elementos de izquierda a derecha a partir de un valor inicial, y funciona con colecciones vacías. `foldRight` va de derecha a izquierda. `reduce` usa el primer elemento como inicio y falla con una colección vacía, así que `reduceOption` es más seguro.

#### ¿En qué se diferencian `groupBy`, `groupMap` y `groupMapReduce`?

`groupBy(key)` devuelve un `Map` de cada clave a los elementos con esa clave. `groupMap(key)(f)` además transforma cada elemento. `groupMapReduce(key)(f)(op)` transforma y combina en una sola pasada, sin construir listas intermedias: la forma eficiente de sumar o contar por clave.

#### ¿Qué hacen `partition`, `span` y `splitAt`?

`partition(p)` separa los elementos que cumplen `p` de los que no. `span(p)` corta en el primer elemento que no cumple `p`. `splitAt(n)` corta en una posición. Las tres devuelven un par de colecciones.

#### ¿Qué hacen `zip`, `zipWithIndex` y `sliding`?

`zip` empareja los elementos de dos colecciones (y se detiene en la más corta), `zipWithIndex` empareja cada elemento con su posición, y `sliding(n)` recorre ventanas superpuestas de `n` elementos, útiles para promedios móviles y comparaciones con el elemento anterior.

#### ¿Cómo ordenas colecciones?

`sorted` usa el `Ordering` del tipo de los elementos, `sortBy(f)` ordena por una clave y `sortWith(lt)` recibe una comparación. Las tuplas ordenan por varias claves (`sortBy(s => (s.country, -s.amount))`), y `Ordering.by` y `.reverse` construyen ordenamientos a medida.

#### ¿Qué hacen `exists`, `forall`, `find` y `count`?

`exists(p)` es verdadero si algún elemento cumple `p`, `forall(p)` si todos lo cumplen (verdadero con una colección vacía), `find(p)` devuelve la primera coincidencia como un `Option` y `count(p)` cuenta las coincidencias. Los tres primeros se detienen en cuanto conocen la respuesta.

#### Cuenta la frecuencia de las palabras de un texto y devuelve las n más frecuentes.

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

`orders.groupBy(_.customer).map((c, os) => c -> os.map(_.amount).sum)` se queda sin memoria con 50 millones de pedidos. ¿Qué cambias?

<!-- solution -->

`groupBy` construye una lista completa de pedidos por cliente antes de sumar. `orders.groupMapReduce(_.customer)(_.amount)(_ + _)` agrega en una sola pasada y conserva solo un total acumulado por cliente.

<!-- takeaways -->

- `map` conserva la estructura; `flatMap` aplana.
- Prefiere `foldLeft` y `reduceOption` a `reduce`.
- `groupMapReduce` agrega por clave en una pasada.

<!-- unit: Colecciones perezosas e iteradores -->

<!-- goals -->

- Evitar colecciones intermedias con views, iteradores y `LazyList`.
- Procesar archivos grandes con memoria constante.

<!-- concept -->

Las colecciones estrictas calculan cada paso por completo: `xs.map(f).filter(p).take(10)` construye dos colecciones intermedias completas. Una view hace perezosa la cadena y calcula solo los elementos necesarios. Un iterador entrega los elementos de uno en uno y solo se puede recorrer una vez, lo que sirve para archivos y flujos. Una `LazyList` calcula los elementos a demanda, los recuerda y puede ser infinita.

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

#### ¿Qué es una view?

Un envoltorio perezoso sobre una colección (`xs.view`): las transformaciones se registran y se aplican elemento por elemento solo cuando se pide un resultado, por ejemplo con `toList` o `sum`. Evita construir colecciones intermedias en cadenas largas.

#### ¿Cuál es la diferencia entre un `Iterator` y un `Iterable`?

Un `Iterable` (como una `List`) se puede recorrer muchas veces. Un `Iterator` entrega elementos con `hasNext` y `next` y se agota tras una pasada, así que llamar a `size` sobre él lo consume. Métodos como `getLines()` devuelven iteradores.

#### ¿Qué es `LazyList`?

Una secuencia perezosa y memorizada que puede ser infinita, construida con `#::`. Reemplazó al obsoleto `Stream` en Scala 2.13. Conservar una referencia a su cabeza mantiene en memoria todos los elementos ya calculados.

#### ¿Cómo lees un archivo grande línea por línea?

Recorre `Source.fromFile(path).getLines()` (o `java.nio.file.Files.lines`) dentro de `Using`, transformando y plegando el iterador sin convertirlo en lista, así que solo hay una línea en memoria a la vez y el archivo se cierra al final.

#### ¿Cómo procesas elementos por lotes?

`iterator.grouped(1000)` entrega lotes de 1.000 elementos (el último puede ser más corto), y `sliding(n, step)` entrega ventanas. Sobre un iterador, ambos siguen siendo perezosos, lo que sirve para inserciones masivas o llamadas a APIs por bloques.

<!-- challenge -->

`Source.fromFile(path).getLines().toList.filter(isError)` falla con `OutOfMemoryError` sobre un log de 20 GB. ¿Qué cambias?

<!-- solution -->

Mantenlo como iterador: quita `toList`, filtra y cuenta o escribe los resultados sobre la marcha, y envuelve la fuente en `Using` para que el archivo se cierre. Así la memoria se mantiene constante sin importar el tamaño del archivo.

<!-- takeaways -->

- Las views evitan colecciones intermedias.
- Los iteradores se consumen una vez y procesan datos en flujo.
- Nunca hagas `toList` de un archivo que no cabe en memoria.

<!-- unit: Problemas con colecciones -->

<!-- goals -->

- Resolver problemas clásicos de programación con colecciones de Scala.
- Elegir entre métodos de colección, folds y mutación local.

<!-- concept -->

Los problemas de programación en Scala evalúan si piensas en transformaciones. La mayoría tiene una solución corta con métodos de colección: deduplicar con `distinct` o un mapa por ID, two-sum con un mapa de valores vistos, intervalos con un ordenamiento y un fold. Dentro de una función, la mutación local, como un mapa mutable o un builder, está bien cuando es más rápida y no se escapa.

<!-- example -->

```scala
final case class Row(id: String, ts: Long, value: String)

def latestById(rows: Seq[Row]): Iterable[Row] =
  rows.groupMapReduce(_.id)(identity)((a, b) => if a.ts >= b.ts then a else b).values
```

#### Encuentra los dos números de una secuencia que suman un objetivo (two-sum).

Usa un mapa de los valores ya vistos, en O(n):

```scala
def twoSum(nums: Vector[Int], target: Int): Option[(Int, Int)] =
  val seen = collection.mutable.HashMap.empty[Int, Int]   // local mutation, never shared
  nums.indices.iterator.flatMap { i =>
    val hit = seen.get(target - nums(i)).map(j => (j, i))
    seen(nums(i)) = i
    hit
  }.nextOption()
```

#### ¿Cómo quitas duplicados conservando el orden?

`xs.distinct` conserva la primera aparición de cada elemento, y `xs.distinctBy(_.id)` (2.13+) la primera de cada clave. Ambos mantienen el orden original.

#### Fusiona intervalos superpuestos.

```scala
def merge(intervals: List[(Int, Int)]): List[(Int, Int)] =
  intervals.sortBy(_._1).foldLeft(List.empty[(Int, Int)]) {
    case ((s0, e0) :: rest, (s, e)) if s <= e0 => (s0, e0.max(e)) :: rest
    case (acc, interval)                       => interval :: acc
  }.reverse
```

#### Agrupa una lista de palabras en anagramas.

```scala
def groupAnagrams(words: List[String]): List[List[String]] =
  words.groupBy(_.sorted).values.toList
```

#### Comprueba si una cadena de paréntesis está balanceada.

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

#### Encuentra el primer carácter que no se repite en una cadena.

```scala
def firstUnique(s: String): Option[Char] =
  val counts = s.groupMapReduce(identity)(_ => 1)(_ + _)
  s.find(c => counts(c) == 1)
```

#### Calcula un total acumulado y un promedio móvil de 3 elementos.

```scala
val values = List(3, 5, 2, 8, 6)
val running = values.scanLeft(0)(_ + _).tail                    // List(3, 8, 10, 18, 24)
val moving = values.sliding(3).map(w => w.sum / 3.0).toList     // List(3.33, 5.0, 5.33)
```

<!-- challenge -->

Una solución comprueba `if !result.contains(x)` sobre una `List` que crece, para cada uno de un millón de elementos, y tarda minutos. ¿Qué cambias?

<!-- solution -->

`contains` sobre una `List` es O(n), así que el bucle es O(n²). Lleva los elementos vistos en un `Set` (pertenencia en O(1)), o usa `distinct`, que hace exactamente eso.

<!-- takeaways -->

- La mayoría de los problemas son unos pocos métodos de colección.
- Los mapas y sets convierten búsquedas O(n²) en O(n).
- La mutación local está bien si no se escapa.

### Programación funcional

<!-- unit: Inmutabilidad y funciones puras -->

<!-- goals -->

- Explicar las funciones puras, la transparencia referencial y los efectos secundarios.
- Mantener los efectos secundarios en los bordes de un programa.

<!-- concept -->

Una función pura devuelve la misma salida para la misma entrada y no hace nada más: no muta, no hace E/S, no usa excepciones para el control de flujo. El código puro es fácil de probar, de razonar, de cachear y de ejecutar en paralelo, y por eso la programación funcional construye programas con funciones puras sobre datos inmutables.

Los programas reales igual leen archivos y llaman a APIs. El enfoque funcional empuja esos efectos a los bordes, un "núcleo funcional con una capa imperativa", o los describe como valores que se ejecutan después, como hacen las bibliotecas de efectos.

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

#### ¿Qué es la programación funcional?

Un estilo que construye programas con funciones puras y valores inmutables, trata las funciones como valores y maneja los errores y efectos de forma explícita en los tipos. Scala la soporta junto a la programación orientada a objetos, y la mayoría del código Scala mezcla ambas.

#### ¿Qué es una función pura?

Una función cuyo resultado depende solo de sus argumentos y que no tiene efectos secundarios observables. `def add(a: Int, b: Int) = a + b` es pura; una función que lee el reloj, escribe logs o modifica un campo no lo es.

#### ¿Qué es la transparencia referencial?

Una expresión es referencialmente transparente si puedes reemplazarla por su valor sin cambiar el comportamiento del programa. Las funciones puras dan esa propiedad, que hace seguros el refactoring, el cacheo y el razonamiento sobre el código.

#### ¿Qué son los efectos secundarios y cómo los manejas?

Todo lo que hace una función además de devolver un valor: E/S, mutación, excepciones, leer la hora o números aleatorios. Mantenlos en una capa exterior delgada, pasa entradas como la hora actual como parámetros y usa tipos de efecto como `IO` cuando necesites componerlos.

#### ¿Por qué la inmutabilidad ayuda con la concurrencia?

Los datos inmutables se pueden compartir entre hilos sin locks, porque nadie puede cambiarlos; las condiciones de carrera necesitan estado mutable compartido. También hace más seguros los closures de Spark y las cachés.

#### ¿Es aceptable la mutación alguna vez en Scala?

Sí, cuando es local y no se escapa: un `var` o un builder mutable dentro de una función que devuelve un resultado inmutable, o un bucle ajustado donde el rendimiento importa. La función sigue siendo pura vista desde fuera.

<!-- challenge -->

Una transformación lee `LocalDate.now()` internamente, y sus tests fallan cada noche cerca de la medianoche. ¿Cómo lo corriges?

<!-- solution -->

Pasa la fecha (o un `java.time.Clock`) como parámetro, para que la función sea pura: el código de producción pasa la fecha de hoy y los tests una fija.

<!-- takeaways -->

- Las funciones puras dependen solo de sus entradas.
- Empuja los efectos a los bordes.
- La mutación local está bien si no se escapa.

<!-- unit: Option, Either y Try -->

<!-- goals -->

- Reemplazar `null` y las excepciones con `Option`, `Either` y `Try`.
- Encadenar resultados y reunir errores de validación.

<!-- concept -->

En lugar de `null` y excepciones lanzadas, Scala representa "puede faltar" como `Option` (`Some` o `None`), "éxito o un fallo descrito" como `Either` (`Right` o `Left`) y "un cálculo que puede lanzar una excepción" como `Try` (`Success` o `Failure`). Los tipos hacen visibles los fallos en las firmas, así que quien llama debe ocuparse de ellos.

Los tres soportan `map`, `flatMap`, `getOrElse` y las comprensiones `for`: encadenas pasos, y el primer fallo interrumpe el resto.

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

#### ¿Qué es `Option` y por qué usarlo en lugar de `null`?

Un contenedor que es `Some(value)` o `None`. El tipo dice que un valor puede faltar, así que el compilador obliga a quien llama a manejarlo, mientras que `null` es invisible en los tipos y falla más tarde con un `NullPointerException`.

#### ¿Cómo sacas un valor de un `Option` de forma segura?

Con `getOrElse(default)`, `fold`, `map` y `flatMap` para seguir trabajando dentro de él, o con un `match`. Evita `.get`, que lanza una excepción con `None` y trae de vuelta el problema que `Option` resuelve.

#### ¿Qué es `Either`?

Un valor que es `Left(error)` o `Right(result)`. Está sesgado a la derecha: `map` y `flatMap` trabajan sobre el lado `Right` y dejan pasar un `Left`, así que se usa para operaciones que pueden fallar con un error significativo.

#### ¿Qué es `Try`?

Un envoltorio para código que puede lanzar una excepción: `Try(expr)` da `Success(value)` o `Failure(exception)`. Se usa sobre todo en la frontera con bibliotecas que lanzan excepciones, y luego se convierte con `toOption` o `toEither`.

#### ¿Cuándo usas `Option`, `Either` o `Try`?

`Option` cuando la ausencia es normal y no necesita explicación (una búsqueda). `Either` cuando quien llama necesita saber por qué algo falló (validación, conversión con mensajes). `Try` para capturar excepciones de código que no controlas.

#### ¿Cómo manejas el `null` que viene de APIs Java?

Envuelve el valor en la frontera: `Option(javaValue)` convierte `null` en `None`. Scala 3 también tiene un modo opcional de nulls explícitos en el que los tipos de referencia no aceptan null y los resultados de Java tienen tipo `T | Null`.

#### ¿Cómo reúnes todos los errores de validación en lugar de detenerte en el primero?

`Either` en una comprensión `for` se detiene en el primer `Left`. Para conservarlos todos, valida cada elemento y separa los resultados con `partitionMap`, o usa un tipo acumulador como `ValidatedNel` de Cats:

```scala
val (errors, amounts) = rows.partitionMap(r => parseAmount(r("amount")))
```

<!-- challenge -->

Un parser devuelve `null` con entradas inválidas, y aparecen `NullPointerException` en código lejos del parser. ¿Cómo corriges el diseño?

<!-- solution -->

Devuelve `Option` (o `Either` con un mensaje de error) desde el parser, para que cada llamada maneje el fallo donde ocurre y el compilador lo exija.

<!-- takeaways -->

- `Option` para lo que falta, `Either` para errores, `Try` para excepciones.
- Encadena con `map`, `flatMap` y comprensiones `for`.
- Nunca llames a `.get` sobre un `Option`.

<!-- unit: Comprensiones for -->

<!-- goals -->

- Leer y escribir comprensiones `for` y su traducción.
- Usarlas con colecciones, `Option`, `Either` y `Future`.

<!-- concept -->

Una comprensión `for` es sintaxis sobre `flatMap`, `map` y `withFilter`. Cada generador (`<-`) es un paso, y `yield` construye el resultado. Como son solo llamadas a métodos, funciona con cualquier tipo que los defina: colecciones, `Option`, `Either`, `Try`, `Future` y tipos de efecto.

El tipo del primer generador decide el tipo del resultado, así que tipos no relacionados como `Option` y `Future` no se pueden mezclar en una misma comprensión sin convertirlos antes.

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

#### ¿Qué es una comprensión `for`?

Sintaxis para encadenar operaciones sobre valores que soportan `map` y `flatMap`: generadores (`x <- xs`), filtros (`if cond`) y definiciones de valores (`y = f(x)`), seguidos de `yield`. Se lee como una secuencia de pasos.

#### ¿Cómo se traduce una comprensión `for`?

Cada generador salvo el último se convierte en un `flatMap`, el último en un `map` con la expresión del `yield`, y los filtros `if` en `withFilter`. Una comprensión con `do` en lugar de `yield` se convierte en llamadas a `foreach`.

#### ¿Puedes mezclar `Option`, `List` y `Future` en una comprensión `for`?

No directamente: los pasos deben compartir un tipo que se pueda aplanar. Convierte antes (`option.toRight(error)`, `Future.fromTry`, `opt.toList`), o usa monad transformers o bibliotecas de efectos pensadas para combinarlos.

#### ¿Qué cambió "better fors" en Scala 3.8?

La SIP-62, activa por defecto desde 3.8, permite que una comprensión empiece con un alias (`x = ...`), traduce los alias sin construir tuplas intermedias y elimina el `map` final cuando `yield` solo devuelve el último valor asociado. La traducción es más simple y más barata, lo que importa sobre todo con tipos de efecto.

#### ¿Qué es una mónada, en términos prácticos?

Un tipo con `flatMap` y una forma de envolver un valor simple (`Some(x)`, `List(x)`, `Future.successful(x)`, `IO.pure(x)`) que cumple unas pocas leyes. En la práctica, es cualquier cosa que puedes encadenar en una comprensión `for`, donde cada paso depende del anterior.

<!-- challenge -->

Una función de conversión anida cuatro llamadas a `flatMap` sobre valores `Either`, y nadie la entiende. ¿Cómo la reescribes?

<!-- solution -->

Como una comprensión `for`, con un generador por paso (`a <- parseA(raw)`, `b <- parseB(a)`, ...) y un `yield` que construye el resultado. La semántica es idéntica y los pasos se leen de arriba abajo.

<!-- takeaways -->

- `for`/`yield` es `flatMap`, `map` y `withFilter`.
- Funciona con cualquier tipo que los defina.
- El primer generador decide el tipo del resultado.

<!-- unit: Recursión y llamadas de cola -->

<!-- goals -->

- Escribir funciones recursivas sobre listas.
- Hacer la recursión segura para la pila con `@tailrec` y acumuladores.

<!-- concept -->

La recursión refleja los datos recursivos: una `List` está vacía o es una cabeza seguida de otra lista. Cada llamada recursiva usa un marco de la pila, así que la recursión profunda en la JVM lanza `StackOverflowError`.

Cuando la llamada recursiva es lo último que hace un método (posición de cola), el compilador de Scala la convierte en un bucle, y `@tailrec` hace fallar la compilación si no puede. Los folds ya empaquetan la mayoría de estos bucles.

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

#### ¿Qué es la recursión de cola?

Una llamada recursiva que es la última operación de un método, así que no queda nada por hacer cuando retorna. `loop(tail, acc + h)` está en posición de cola; `h + sum(tail)` no, porque la suma ocurre después de la llamada.

#### ¿Qué hace `@tailrec`?

Le pide al compilador que verifique que un método es recursivo de cola y se compila como un bucle; si no, la compilación falla. No activa la optimización (el compilador la hace de todas formas), pero la garantiza.

#### ¿Por qué la JVM no optimiza todas las llamadas de cola?

La JVM no tiene eliminación general de llamadas de cola. Scala solo optimiza las llamadas recursivas a sí mismo en métodos que no se pueden sobrescribir (locales, `private` o `final`). Las funciones mutuamente recursivas necesitan trampolines, como `scala.util.control.TailCalls`, o una biblioteca de efectos.

#### ¿Cuándo conviene usar un fold en lugar de recursión explícita?

Siempre que la recursión solo recorre una colección y acumula un resultado: `foldLeft` ya es un bucle seguro para la pila y expresa la intención. La recursión explícita es más clara para árboles, salidas tempranas o varios acumuladores.

#### Invierte una lista de forma recursiva.

```scala
import scala.annotation.tailrec

def reverse[A](xs: List[A]): List[A] =
  @tailrec def loop(rest: List[A], acc: List[A]): List[A] = rest match
    case Nil    => acc
    case h :: t => loop(t, h :: acc)
  loop(xs, Nil)
```

<!-- challenge -->

`def count(xs: List[Int]): Int = if xs.isEmpty then 0 else 1 + count(xs.tail)` falla con `StackOverflowError` con 100.000 elementos. ¿Cómo lo corriges?

<!-- solution -->

Lleva la cuenta en un acumulador para que la llamada recursiva quede en posición de cola, y anota el helper con `@tailrec`; o simplemente usa `xs.size` o un fold.

<!-- takeaways -->

- Cada llamada que no es de cola usa un marco de la pila.
- `@tailrec` garantiza un bucle.
- Los folds reemplazan la mayoría de la recursión explícita.

<!-- stage: Tipos y abstracciones -->

### El sistema de tipos

<!-- unit: Genéricos y varianza -->

<!-- goals -->

- Escribir clases y métodos genéricos con cotas de tipo.
- Explicar la covarianza, la contravarianza y el borrado de tipos.

<!-- concept -->

Los genéricos permiten que una definición funcione con muchos tipos sin perder la seguridad de tipos: `List[A]`, `def first[A](xs: List[A]): Option[A]`. Las cotas restringen los parámetros de tipo: `A <: Animal` exige un subtipo, `B >: A` un supertipo.

La varianza dice cómo se traslada el subtipado del parámetro al contenedor. Los contenedores inmutables suelen ser covariantes (`List[+A]`: una lista de gatos es una lista de animales). Los tipos que consumen valores son contravariantes (`-A`): algo que acepta cualquier animal sirve donde se necesita algo que acepte gatos. Los contenedores mutables deben ser invariantes.

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

#### ¿Qué son los genéricos en Scala?

Clases, traits y métodos con parámetros de tipo entre corchetes (`class Box[A]`, `def first[A](xs: List[A])`), para que el mismo código funcione con cualquier tipo mientras el compilador sigue comprobando cada uso.

#### ¿Qué son las cotas superiores e inferiores de tipo?

`A <: Upper` restringe `A` a subtipos de `Upper`, así que el código puede usar los miembros de `Upper`. `B >: Lower` restringe `B` a supertipos de `Lower`, y se usa normalmente para ampliar un tipo al añadir elementos a una colección covariante.

#### ¿Qué es la covarianza?

`Container[+A]` significa que si `Cat` es subtipo de `Animal`, `Container[Cat]` es subtipo de `Container[Animal]`. Es segura para tipos que solo producen valores `A`, como las colecciones inmutables, `Option` y `Future`.

#### ¿Qué es la contravarianza?

`Container[-A]` invierte la relación: `Sink[Animal]` es subtipo de `Sink[Cat]`. Encaja con tipos que solo consumen `A`, como los parámetros de las funciones (`Function1[-A, +B]`), los encoders o los writers.

#### ¿Por qué `Array` es invariante mientras que `List` es covariante?

Un `Array` es mutable. Si un `Array[Cat]` fuera un `Array[Animal]`, podrías guardar un `Dog` a través de la vista de animales y romper el arreglo de gatos. Una `List` inmutable no se puede cambiar, así que tratar una lista de gatos como una lista de animales es seguro.

#### ¿Por qué `:+` sobre una `List[Cat]` acepta un `Dog`?

Su firma es `def :+[B >: A](elem: B): List[B]`: la cota inferior permite al compilador ampliar el tipo de los elementos a un supertipo común, así que añadir un `Dog` a una `List[Cat]` devuelve una `List[Animal]`.

#### ¿Qué es el borrado de tipos?

En la JVM, los argumentos de tipo genéricos desaparecen en ejecución: una `List[Int]` y una `List[String]` son ambas solo `List`. El código que necesita la clase en ejecución, como para crear un `Array[A]`, pide un `ClassTag[A]`.

<!-- challenge -->

Declaras `class Box[+A](var value: A)` y el compilador lo rechaza. ¿Por qué?

<!-- solution -->

Un `var` tiene un setter que recibe un `A`, una posición contravariante. Si compilara, un `Box[Cat]` visto como `Box[Animal]` podría recibir un `Dog`. Haz que el campo sea `val` para mantener la caja covariante, o déjala invariante si debe ser mutable.

<!-- takeaways -->

- Las cotas restringen los parámetros de tipo.
- Los productores son covariantes; los consumidores, contravariantes.
- Los contenedores mutables son invariantes.

<!-- unit: Tipos unión, intersección y opacos -->

<!-- goals -->

- Usar los tipos unión e intersección de Scala 3.
- Crear tipos de dominio sin costo con tipos opacos, y usar tuplas con nombre.

<!-- concept -->

Scala 3 añade tipos que antes eran difíciles de expresar. Una unión `A | B` contiene un valor de cualquiera de los dos tipos, sin envolverlo en `Either` ni en un sealed trait. Una intersección `A & B` tiene los miembros de ambos y reemplaza el `A with B` de Scala 2.

Un tipo opaco da un nombre nuevo a un tipo existente que solo su ámbito de definición puede ver por dentro: un `CustomerId` es un `String` en ejecución, pero el código de fuera no puede confundirlo con un `OrderId` ni con una cadena cualquiera, y no hay costo de envoltorio. Las tuplas con nombre, estables desde 3.7, dan nombre a los elementos de una tupla sin declarar una case class.

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

#### ¿Qué es un tipo unión?

`A | B` es el tipo de los valores que son `A` o `B`, como `Int | String`. Usas el valor haciendo match sobre su tipo. A diferencia de `Either`, no hay envoltorio ni significado de izquierda o derecha, y el orden de los tipos no importa.

#### ¿Qué es un tipo intersección?

`A & B` es el tipo de los valores que son a la vez `A` y `B`, con los miembros de ambos. Un parámetro de tipo `Closeable & Flushable` acepta cualquier objeto que implemente las dos interfaces. Reemplaza los tipos compuestos `A with B` de Scala 2.

#### ¿Qué es un tipo opaco?

Un alias de tipo que solo es transparente dentro del ámbito que lo define: `opaque type CustomerId = String`. Fuera, es un tipo distinto, así que no se puede mezclar con otras cadenas, pero en ejecución es solo un `String`, sin asignación de memoria. Su object compañero y sus métodos de extensión definen qué se puede hacer con él.

#### ¿Cómo se comparan los tipos opacos con las value classes?

Las value classes de Scala 2 (`class CustomerId(val value: String) extends AnyVal`) también evitan envoltorios, pero hacen boxing del valor en muchas situaciones: en colecciones, genéricos y pattern matching. Los tipos opacos nunca hacen boxing, así que reemplazan a las value classes en Scala 3.

#### ¿Qué son las tuplas con nombre?

Tuplas cuyos elementos tienen nombre: `(rows = 1200, errors = 3)`, de tipo `(rows: Int, errors: Int)`. Los elementos se acceden por nombre, y una tupla con nombre se puede usar donde se espera una tupla normal. Sirven para resultados ligeros sin declarar una case class.

#### ¿Qué es un alias de tipo?

`type Row = Map[String, String]` da un nombre más corto a un tipo existente. Es solo un nombre: un `Row` y un `Map[String, String]` son intercambiables, a diferencia de un tipo opaco, que añade seguridad de tipos.

#### ¿Cuándo usarías un tipo unión en lugar de `Either`?

Una unión encaja cuando las dos alternativas son valores igual de válidos, como un campo que es un `Int` o un `String`. `Either` encaja cuando un lado es un error, porque lleva el significado de éxito o fallo y soporta `map`, `flatMap` y comprensiones `for`.

<!-- challenge -->

Varias funciones reciben `customerId: String, orderId: String`, y quienes las llaman los pasan en el orden equivocado una y otra vez. ¿Cómo lo evitas en compilación sin costo en ejecución?

<!-- solution -->

Define `opaque type CustomerId = String` y `opaque type OrderId = String` con constructores inteligentes y cambia las firmas. Los argumentos intercambiados dejan de compilar, y ambos siguen siendo cadenas simples en ejecución.

<!-- takeaways -->

- `A | B` es uno u otro; `A & B` es ambos.
- Los tipos opacos dan seguridad de tipos sin envoltorios.
- Las tuplas con nombre nombran resultados ligeros.

### Abstracciones contextuales

<!-- unit: Givens y cláusulas using -->

<!-- goals -->

- Pasar contexto con cláusulas `using` y proveerlo con instancias `given`.
- Importar givens, obtenerlos con `summon` y traducir los implicits de Scala 2 a Scala 3.

<!-- concept -->

Algunos parámetros son contexto más que datos: un execution context, una configuración, un ordenamiento. Pasarlos explícitamente en cada llamada es ruido. Scala 3 permite que un método los declare en una cláusula `using`, y el compilador los completa con instancias `given` en el ámbito, según su tipo.

Es el rediseño en Scala 3 de los implicits de Scala 2. Los givens definen instancias, las cláusulas `using` las consumen, y los givens se importan explícitamente con `import x.given`, así que queda claro de dónde vienen.

<!-- example -->

```scala
final case class Config(env: String, batchSize: Int)

def load(path: String)(using cfg: Config): String =
  s"loading $path in ${cfg.env} with batches of ${cfg.batchSize}"

given Config = Config("dev", 500)
load("s3://lake/orders")                               // Config passed automatically
load("s3://lake/orders")(using Config("prod", 5000))   // or explicitly
```

#### ¿Qué problema resuelven los givens y las cláusulas `using`?

Pasan valores de contexto (configuración, execution contexts, instancias de type classes) sin escribirlos en cada llamada, mientras la dependencia sigue visible en las firmas de los métodos y se resuelve en compilación.

#### ¿Qué es una instancia given?

Un valor declarado con `given` que el compilador puede aportar a un parámetro `using` de su tipo: `given Config = Config("dev", 500)`, o uno con nombre, `given devConfig: Config = ...`. Los givens también pueden depender de otros givens.

#### ¿Qué es una cláusula `using`?

Una lista de parámetros marcada con `using`, como `(using cfg: Config)`, cuyos argumentos completa el compilador con los givens del ámbito. Quien llama puede pasarlos igual de forma explícita con `(using value)`. Los anónimos se escriben `(using Config)` y se obtienen con `summon`.

#### ¿Cómo importas givens?

Los imports con comodín (`import a.*`) no traen givens. Se importan con `import a.given` (todos los givens) o por tipo, `import a.{given Ordering[?]}`, lo que deja explícito su origen.

#### ¿Qué hace `summon`?

`summon[T]` devuelve la instancia given de tipo `T` en el ámbito, o no compila si no hay ninguna. Es el equivalente en Scala 3 del `implicitly` de Scala 2.

#### ¿Cómo se traducen los implicits de Scala 2 a Scala 3?

Los valores y métodos implícitos se vuelven instancias `given`, los parámetros implícitos cláusulas `using`, las clases implícitas métodos de extensión y las conversiones implícitas instancias `given Conversion[A, B]`. Scala 3 sigue aceptando los implicits de Scala 2, lo que permite migrar de forma gradual.

#### ¿Dónde busca givens el compilador?

Primero en el ámbito léxico: definiciones locales, clases que lo rodean e imports. Luego en el ámbito implícito del tipo que busca, que incluye los objects compañeros del tipo y de sus argumentos de tipo. Por eso las instancias de type classes suelen vivir en objects compañeros.

<!-- challenge -->

Un parámetro `ExecutionContext` se pasa explícitamente por 30 métodos de un servicio. ¿Cómo lo simplificas sin estado global?

<!-- solution -->

Decláralo como `(using ExecutionContext)` en esos métodos y provee un único `given ExecutionContext` en el borde de la aplicación (o en los tests). Las llamadas ya no lo mencionan, y cada entorno puede seguir aportando el suyo.

<!-- takeaways -->

- Las cláusulas `using` reciben contexto; `given` lo provee.
- Importa los givens explícitamente con `import x.given`.
- Las instancias en objects compañeros se encuentran solas.

<!-- unit: Type classes -->

<!-- goals -->

- Definir type classes con traits e instancias given.
- Usar context bounds, derivación e igualdad multiversal.

<!-- concept -->

Una type class añade comportamiento a tipos que no son tuyos, sin herencia. Un trait describe el comportamiento (`Show[A]`, `Encoder[A]`), las instancias given lo implementan para tipos concretos, y los métodos piden una instancia con un context bound. Soportar un tipo nuevo significa escribir una instancia más, no cambiar el tipo.

Las bibliotecas usan el patrón en todas partes: los codecs JSON de circe, los encoders de Spark, `Monoid` y `Functor` de Cats y `Ordering` en la biblioteca estándar. Scala 3 puede derivar instancias automáticamente con `derives`.

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

#### ¿Qué es una type class?

Un trait genérico que describe una capacidad (`Show[A]`, `Ordering[A]`, `Encoder[A]`) más instancias para tipos concretos, provistas como givens. El código que necesita la capacidad pide una instancia, así que el comportamiento se añade a los tipos desde fuera, en compilación.

#### ¿Cómo defines y usas una type class en Scala 3?

Escribe un trait con un parámetro de tipo, provee instancias `given` para los tipos que soportas (normalmente en el object compañero del trait o del tipo) y pide una instancia donde la necesitas con un context bound o una cláusula `using`. Los métodos de extensión dentro del trait dan a las llamadas una sintaxis natural como `value.show`.

#### ¿Qué es un context bound?

`def describe[A: Show](a: A)` es una abreviatura de un parámetro `using` de tipo `Show[A]`. Desde Scala 3.6 la instancia se puede nombrar en la cota, `[A: Show as s]`; si no, se obtiene con `summon[Show[A]]`.

#### ¿Qué es la derivación de type classes?

`case class Order(...) derives Codec` le pide al compilador generar una instancia a partir de la estructura del tipo, usando un método `derived` que provee la type class. Bibliotecas como circe lo usan para construir codecs JSON para case classes y enums.

#### ¿Por qué usar type classes en lugar de herencia para cosas como la serialización a JSON?

Se pueden añadir instancias para tipos que no son tuyos (de bibliotecas o de Java), un tipo puede tener varias instancias en distintos contextos, las clases de datos quedan libres de código de serialización y una instancia que falta es un error de compilación, no de ejecución.

#### ¿Qué es `Ordering`?

La type class de la biblioteca estándar para ordenar. `sorted`, `max` y `TreeMap` reciben un `Ordering` given; construyes los tuyos con `Ordering.by(_.amount)` y los inviertes con `.reverse`.

#### ¿Qué es la igualdad multiversal?

Una funcionalidad opcional de Scala 3: con `import scala.language.strictEquality`, `==` solo compila entre tipos que tienen una instancia `CanEqual`, normalmente derivada con `derives CanEqual`. Detecta comparaciones que siempre son falsas, como un `CustomerId` con un `Int`.

<!-- challenge -->

Un equipo añade `toJson` a 40 case classes mediante un trait `JsonSerializable`, pero no puede añadirlo a clases de una biblioteca externa. ¿Qué diseño resuelve ambos problemas?

<!-- solution -->

Una type class: un `Encoder[A]` con instancias derivadas para las case classes del equipo (`derives`) y escritas a mano para los tipos de la biblioteca. Las clases de datos dejan de depender del código JSON, y cualquier tipo puede tener un encoder.

<!-- takeaways -->

- Las type classes añaden comportamiento desde fuera de un tipo.
- Los context bounds piden instancias.
- `derives` genera instancias a partir de la estructura.

<!-- unit: Métodos de extensión y conversiones -->

<!-- goals -->

- Añadir métodos a tipos existentes con métodos de extensión.
- Usar las conversiones implícitas con moderación, con `Conversion` e `into`.

<!-- concept -->

Los métodos de extensión añaden métodos a tipos que no puedes cambiar, como `String` o una clase de una biblioteca. Se resuelven en compilación, no cuestan nada en ejecución y reemplazan las clases implícitas de Scala 2.

Las conversiones implícitas transforman un tipo en otro sin avisar. Hacían difícil seguir el código Scala 2, así que Scala 3 las restringe: defines un `given Conversion[A, B]`, y usarlo requiere un import de lenguaje salvo que el destino esté marcado con `into`, estable desde 3.9, que permite conversiones solo donde una API las pide.

<!-- example -->

```scala
extension (s: String)
  def toSnakeCase: String = s.replaceAll("([a-z])([A-Z])", "$1_$2").toLowerCase
  def isBlankOrNull: Boolean = s == null || s.isBlank

"orderDate".toSnakeCase          // order_date
```

#### ¿Qué es un método de extensión?

Un método definido fuera de un tipo que se puede llamar como si fuera un miembro: `extension (s: String) def toSnakeCase: String = ...` permite escribir `"orderDate".toSnakeCase`. Es visible donde se define o se importa, o cuando pertenece a una instancia given o un compañero en el ámbito.

#### ¿Cómo añadía Scala 2 métodos a tipos existentes?

Con clases implícitas, `implicit class RichString(s: String) { def toSnakeCase = ... }`, el patrón "enrich my library". El compilador envolvía el valor en la clase cuando se llamaba a un método inexistente.

#### ¿Qué es una conversión implícita y por qué se desaconseja?

Una regla que convierte automáticamente un valor de tipo `A` en `B` cuando se espera un `B`. Oculta lo que hace el código, puede hacer que compile código incorrecto y hace más lenta la compilación, así que Scala 3 exige un `given Conversion[A, B]` y un import de `scala.language.implicitConversions` (o `into`) para usar una.

#### ¿Qué hace `into`?

Marca un tipo de parámetro, o una clase entera, como destino de conversiones implícitas: `def write(path: into Path)` permite pasar cualquier valor que tenga una `Conversion` a `Path`, sin el import de lenguaje en las llamadas. Así las conversiones ocurren solo donde el autor de la API las permitió.

#### ¿Cómo encuentra el compilador los métodos de extensión?

Cuando `x.m` no compila porque `x` no tiene un miembro `m`, el compilador busca un método de extensión llamado `m` en el ámbito (definido o importado), en las instancias given del ámbito y en el ámbito implícito del tipo de `x`, como su object compañero.

<!-- challenge -->

Un código define una conversión implícita de `String` a `LocalDate`. Un nombre de columna pasado por error donde se esperaba una fecha compiló y falló en ejecución. ¿Qué cambias?

<!-- solution -->

Quita la conversión y convierte de forma explícita, por ejemplo con un método de extensión `"2026-10-22".toLocalDate` que devuelva un `Either`, para que la conversión sea visible y los fallos se manejen en la llamada.

<!-- takeaways -->

- Los métodos de extensión añaden métodos sin envoltorios.
- Las conversiones necesitan `Conversion` y activarse explícitamente.
- Prefiere conversiones explícitas en el código de aplicación.

<!-- stage: Práctica de ingeniería -->

### Concurrencia

<!-- unit: Futures -->

<!-- goals -->

- Ejecutar trabajo asíncrono con `Future` y un `ExecutionContext`.
- Componer futures y manejar fallos, bloqueos y límites de paralelismo.

<!-- concept -->

Un `Future[A]` es un valor que más adelante tendrá un resultado o un fallo. Se calcula en un pool de hilos que provee un `ExecutionContext`, empieza a correr en cuanto se crea y se combina con `map`, `flatMap` y comprensiones `for` en lugar de esperar.

Bloquear un hilo para esperar un resultado (`Await.result`) va contra la idea, salvo en el borde mismo de un programa o en los tests. La E/S bloqueante dentro de un future debe envolverse en `blocking` o correr en un pool dedicado, para no dejar sin hilos al compartido.

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

#### ¿Qué es un `Future`?

Un marcador de posición para un valor calculado de forma asíncrona, que termina con `Success(value)` o `Failure(exception)`. Es impaciente (eager: empieza de inmediato) y su resultado queda guardado una vez completo.

#### ¿Qué es un `ExecutionContext`?

El pool de hilos que ejecuta los futures y sus callbacks, que la mayoría de los métodos de `Future` recibe como parámetro de contexto. `ExecutionContext.global` sirve para trabajo de CPU; las llamadas bloqueantes necesitan `blocking { ... }` o un pool aparte y acotado.

#### ¿Cómo compones futures?

Con `map` y `flatMap` (o una comprensión `for`) para encadenar pasos dependientes, `zip` para combinar pasos independientes, y `Future.sequence` o `Future.traverse` para convertir una colección de futures en un future de una colección.

#### ¿Por qué los futures de una comprensión `for` a veces corren uno tras otro?

Si los futures se crean dentro de la comprensión (`a <- fetchA(); b <- fetchB()`), el segundo se crea solo cuando el primero termina. Crea los futures independientes antes de la comprensión, como en el ejemplo, para que corran en paralelo.

#### ¿Por qué evitar `Await.result`?

Bloquea un hilo hasta que el future termina, lo que desperdicia hilos, puede bloquear por completo un pool pequeño y oculta el diseño asíncrono. Úsalo solo en el borde del programa (un `main` que debe esperar) o en tests, siempre con un timeout.

#### ¿Cómo manejas los fallos de un `Future`?

Una excepción lanzada completa el future con un `Failure`. Recupéralo con `recover` o `recoverWith`, transforma ambos resultados con `transform`, ofrece una alternativa con `fallbackTo` y reacciona con `onComplete`, sin volver a lanzar excepciones dentro de los callbacks.

#### ¿Cómo ejecutas muchos futures con paralelismo limitado?

`Future.traverse(items)(f)` lanza todas las llamadas a la vez, lo que puede saturar una API. Procesa los elementos por lotes (`grouped(n)` plegados en secuencia), ejecútalos en un pool de hilos acotado o usa una biblioteca de streaming o de efectos con límite de paralelismo, como `parTraverseN` de Cats Effect.

<!-- challenge -->

Una comprensión `for` combina tres llamadas independientes a APIs que devuelven futures, y el tiempo total es la suma de las tres. ¿Cómo haces que sea el tiempo de la más lenta?

<!-- solution -->

Lanza los tres futures antes de la comprensión (`val a = callA(); val b = callB(); val c = callC()`) y solo combínalos dentro de ella, o usa `zip`; así corren en paralelo.

<!-- takeaways -->

- Los futures empiezan de inmediato en un `ExecutionContext`.
- Compón; no bloquees con `Await`.
- Lanza los futures independientes antes de combinarlos.

<!-- unit: Efectos, actores e hilos -->

<!-- goals -->

- Explicar los sistemas de efectos como Cats Effect y ZIO.
- Conocer los actores, los hilos virtuales y el estado compartido seguro.

<!-- concept -->

Los futures son impacientes y no son referencialmente transparentes: crear uno inicia el trabajo, así que un future no se puede reintentar ni reutilizar como descripción de un trabajo. Las bibliotecas de efectos como Cats Effect y ZIO describen los programas como valores (`IO`, `ZIO`) que solo corren cuando su runtime los ejecuta. Así los programas se componen, se reintentan y se cancelan de forma segura, sobre fibras ligeras, con seguridad de recursos y concurrencia estructurada incluidas.

Los actores, en Apache Pekko (el fork open source de Akka), modelan la concurrencia como objetos que intercambian mensajes, adecuados para sistemas con estado y distribuidos. Desde JDK 21, los hilos virtuales también hacen escalar el código bloqueante simple.

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

#### ¿Qué es un sistema de efectos?

Una biblioteca que representa los efectos secundarios como valores que describen qué hacer, como `IO[A]` en Cats Effect o `ZIO[R, E, A]`, y los ejecuta con un runtime. Añade evaluación perezosa, cancelación, reintentos, seguridad de recursos y concurrencia ligera sobre código funcional puro.

#### ¿Cuál es la diferencia entre `Future` e `IO`?

Un `Future` empieza a correr al crearse y memoriza su resultado. Un `IO` es una descripción que no hace nada hasta ejecutarse, y ejecutarlo dos veces hace el trabajo dos veces. Eso hace que `IO` sea referencialmente transparente: los reintentos, los timeouts y las carreras son simples funciones sobre valores.

#### ¿Qué son las fibras?

Hilos lógicos ligeros que gestiona un runtime de efectos y que se planifican sobre un pool pequeño de hilos del sistema operativo. Pueden existir millones a la vez, se pueden cancelar, y las llamadas bloqueantes se mueven a un pool aparte.

#### ¿Qué es el modelo de actores y qué es Pekko?

Los actores son objetos que guardan un estado privado y se comunican solo mediante mensajes asíncronos, procesando un mensaje a la vez, así que no necesitan locks. Pekko es el fork de Apache de Akka, creado después de que Akka pasara a una licencia comercial en 2022.

#### ¿Qué son los hilos virtuales y le importan a Scala?

Hilos de JDK 21 gestionados por la JVM en lugar del sistema operativo, tan baratos que se puede crear uno por tarea, así que el código bloqueante ya no desperdicia hilos del sistema. Scala puede usarlos directamente, y bibliotecas como Ox construyen sobre ellos una concurrencia estructurada en estilo directo, como alternativa a los futures y los sistemas de efectos.

#### ¿Cómo compartes estado mutable de forma segura entre hilos?

Prefiere datos inmutables y paso de mensajes. Cuando el estado se debe compartir, usa referencias atómicas (`AtomicReference`, el `Ref` de Cats Effect), colecciones concurrentes (`TrieMap`, `ConcurrentHashMap`) o bloques `synchronized`, con secciones críticas pequeñas.

<!-- challenge -->

Un helper de reintentos recibe `f: Future[A]` y lo vuelve a llamar si falla, pero los reintentos nunca vuelven a llamar a la API. ¿Por qué y cómo lo corriges?

<!-- solution -->

El future empezó una sola vez al pasarse como argumento, y "reintentar" solo lee el mismo resultado fallido. Recibe una forma de crearlo de nuevo, `f: () => Future[A]` o un by-name `f: => Future[A]`, o usa `IO`, que describe la llamada y la vuelve a ejecutar en cada intento.

<!-- takeaways -->

- `IO` describe el trabajo; `Future` ya lo empezó.
- Las fibras y los hilos virtuales abaratan la concurrencia.
- Comparte estado con atómicos, `Ref` o mensajes.

### Herramientas, interoperabilidad con Java y tests

<!-- unit: Herramientas de build -->

<!-- goals -->

- Estructurar un build de sbt con dependencias, ámbitos y ajustes.
- Empaquetar jobs de Spark, compilar bibliotecas para varias versiones y conocer Scala CLI y Mill.

<!-- concept -->

sbt es la herramienta de build más común de Scala. `build.sbt` declara la versión de Scala, las dependencias y los ajustes, y sbt compila de forma incremental, ejecuta los tests y publica artefactos. Los artefactos de bibliotecas Scala llevan la versión binaria de Scala en su nombre (`_2.13`, `_3`), que el operador `%%` añade por ti.

Para scripts y proyectos pequeños, Scala CLI (el comando `scala`) no necesita archivo de build, y Mill es una herramienta de build alternativa más rápida. Los jobs de Spark se suelen empaquetar en un solo JAR, con Spark marcado como `provided` porque el clúster lo aporta.

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

#### ¿Qué es sbt?

La herramienta de build estándar de Scala: compila de forma incremental, resuelve dependencias, ejecuta tests, abre un REPL y publica artefactos. Los builds se definen en `build.sbt` con ajustes y tareas, y se extienden con plugins (`project/plugins.sbt`).

#### ¿Cuál es la diferencia entre `%` y `%%` en sbt?

`%%` añade al nombre del artefacto la versión binaria de Scala del proyecto (`spark-sql` se vuelve `spark-sql_2.13`), como necesitan las bibliotecas Scala. `%` usa el nombre tal cual, para bibliotecas Java.

#### ¿Qué significa el ámbito `provided`?

La dependencia está disponible en compilación pero no se empaqueta, porque el entorno de ejecución la aporta. Spark y Hadoop son `provided` en los jobs de Spark, lo que mantiene pequeño el JAR y evita conflictos de versiones con el clúster.

#### ¿Cómo construyes un fat JAR?

Con el plugin sbt-assembly, que empaqueta tu código y sus dependencias en un solo JAR. Las estrategias de fusión resuelven archivos duplicados (por ejemplo en `META-INF`), y el shading renombra paquetes en conflicto, como una versión antigua de Jackson o Guava que usa una dependencia.

#### ¿Qué es el cross-building?

Compilar y publicar una biblioteca para varias versiones de Scala: `crossScalaVersions := Seq("2.13.18", "3.3.8")`, y luego `sbt +test` o `+publish` ejecuta la tarea para cada una. El código específico de una versión va en carpetas `src/main/scala-2.13` o `scala-3`.

#### ¿Qué son Scala CLI y Mill?

Scala CLI, ahora el comando `scala`, ejecuta y empaqueta proyectos de un solo módulo con directivas `//> using` en los archivos fuente en lugar de un archivo de build. Mill es una herramienta de build cuyos builds se escriben como objects de Scala, conocida por sus builds rápidos y en caché. Ambos son alternativas a sbt para proyectos de distintos tamaños.

#### ¿Por qué las versiones de Scala afectan la compatibilidad binaria?

Las bibliotecas se compilan para una versión binaria de Scala (2.12, 2.13 o 3), y esas series no son compatibles entre sí a nivel binario, así que cada biblioteca se publica una vez por versión. Scala 3 es la excepción: puede usar la mayoría de los artefactos de Scala 2.13, y sus versiones menores siguen siendo compatibles hacia atrás.

<!-- challenge -->

El JAR de un job de Spark pesa 400 MB y falla en el clúster con `NoSuchMethodError` en clases de Jackson. ¿Qué cambias en el build?

<!-- solution -->

Marca Spark y Hadoop como `provided`, para que dejen de empaquetarse, alinea las versiones de las demás dependencias con las del clúster, y haz shading de la biblioteca en conflicto en sbt-assembly si una dependencia de verdad necesita otra versión de Jackson.

<!-- takeaways -->

- `%%` añade la versión binaria de Scala.
- Spark es `provided` en los JAR de los jobs.
- Assembly construye fat JARs; el shading resuelve conflictos.

<!-- unit: Interoperabilidad con Java -->

<!-- goals -->

- Llamar bibliotecas Java desde Scala y Scala desde Java.
- Convertir colecciones y manejar nulls, excepciones comprobadas y versiones del JDK.

<!-- concept -->

Scala corre sobre la JVM, así que cualquier biblioteca Java está a una dependencia de distancia, y las llamadas se ven como llamadas Scala. La fricción está en los bordes: las colecciones de Java se deben convertir a colecciones de Scala, las APIs de Java pueden devolver `null` y el compilador de Scala no sigue las excepciones comprobadas de Java.

En la otra dirección, las funcionalidades de Scala sin equivalente en Java, como los argumentos por defecto, los givens y los objects compañeros, se ven raras desde Java, así que las APIs pensadas para llamadas desde Java se mantienen simples.

<!-- example -->

```scala
import scala.jdk.CollectionConverters.*
import java.nio.file.{Files, Paths}

val ids: List[String] = Files.readAllLines(Paths.get("ids.txt")).asScala.toList
val javaList: java.util.List[String] = List("a", "b").asJava
val appHome: Option[String] = Option(System.getenv("APP_HOME"))    // null becomes None
```

#### ¿Cómo conviertes entre colecciones de Java y de Scala?

Importa `scala.jdk.CollectionConverters.*` y llama a `.asScala` o `.asJava`, que envuelven la colección sin copiarla; añade `.toList` o `.toMap` para una copia inmutable. En Scala 2.12 el import era `scala.collection.JavaConverters._`.

#### ¿Cómo manejas el `null` que viene de código Java?

Envuelve los valores de Java en `Option(...)` en la frontera, para que `null` se vuelva `None` y el resto del código trabaje con `Option`. Nunca dejes que `null` entre al código de dominio en Scala.

#### ¿Cómo se manejan las excepciones comprobadas de Java?

Scala no distingue las excepciones comprobadas: no te obliga a capturarlas ni a declararlas. Captúralas donde puedas manejarlas, o envuelve la llamada en `Try`. Añade `@throws[IOException]` a los métodos Scala que llama código Java, para que Java vea la declaración.

#### ¿Cómo se ven las funcionalidades de Scala desde Java?

Los objects se compilan como una clase con una instancia estática `MODULE$` más reenvíos estáticos, los traits como interfaces con métodos por defecto, los argumentos por defecto como métodos con nombres como `connect$default$2` y los givens como parámetros normales. Mantén simples las APIs pensadas para llamadas desde Java.

#### ¿Cómo interoperan las funciones de Scala y las interfaces funcionales de Java?

Las lambdas de Scala se convierten automáticamente en interfaces funcionales de Java (tipos con un único método abstracto) como `Runnable` o `java.util.function.Function`. `scala.jdk.FunctionConverters` convierte objetos función de forma explícita cuando hace falta.

#### ¿Sobre qué JDK debería correr el código Scala?

Scala 3.8 y posteriores requieren JDK 17 o más reciente; Scala 3.3 LTS, 2.13 y 2.12 siguen corriendo en JDK 8. En la práctica los equipos usan un JDK LTS, 17, 21 o 25, según su plataforma: Spark 4 requiere JDK 17 o posterior.

<!-- challenge -->

Un SDK de Java devuelve un `java.util.Map[String, String]` de etiquetas que a veces es `null`, y `sdk.tags().asScala.get("env")` lanza un `NullPointerException`. Corrígelo.

<!-- solution -->

Envuelve primero el resultado: `Option(sdk.tags()).map(_.asScala.toMap).getOrElse(Map.empty).get("env")`, para que un mapa ausente se comporte como uno vacío.

<!-- takeaways -->

- `asScala`/`asJava` convierten colecciones.
- Envuelve en `Option` los resultados de Java.
- Scala 3.8+ necesita JDK 17.

<!-- unit: Tests -->

<!-- goals -->

- Escribir tests con ScalaTest o MUnit y tests basados en propiedades con ScalaCheck.
- Probar código Spark y simular dependencias con sensatez.

<!-- concept -->

Los frameworks de tests de Scala combinan un estilo de definición de tests con aserciones y ejecutores integrados en sbt. ScalaTest ofrece varios estilos (`AnyFunSuite`, `AnyFlatSpec`, `AnyWordSpec`); MUnit mantiene una API pequeña con diffs claros. Ambos se ejecutan con `sbt test` y en los IDEs.

Los tests basados en propiedades con ScalaCheck generan muchas entradas aleatorias y comprueban que una propiedad se cumpla, reduciendo los fallos a un caso mínimo. Las funciones puras facilitan todo esto: sin preparación, sin mocks, solo entradas y salidas.

<!-- example -->

```scala
import munit.FunSuite

class AmountSuite extends FunSuite:
  test("parses amounts with spaces"):
    assertEquals(parseAmount(" 12.50 "), Right(BigDecimal("12.50")))

  test("rejects garbage"):
    assert(parseAmount("abc").isLeft)
```

#### ¿Qué bibliotecas de tests son comunes en Scala?

ScalaTest (muchos estilos, matchers completos), MUnit (mínima, rápida, buenos diffs), specs2, ScalaCheck para tests basados en propiedades y frameworks adaptados a efectos como weaver o ZIO Test para código con `IO` y `ZIO`.

#### ¿Qué son los tests basados en propiedades?

Enunciar una propiedad que debe cumplirse para todas las entradas y dejar que una biblioteca genere cientos de casos aleatorios, reduciendo cualquier fallo al contraejemplo más pequeño:

```scala
import org.scalacheck.Prop.forAll
val reverseTwice = forAll((xs: List[Int]) => xs.reverse.reverse == xs)
```

#### ¿Cómo pruebas código Spark en Scala?

Escribe las transformaciones como funciones de `DataFrame` a `DataFrame`, construye entradas pequeñas con `Seq(...).toDF(...)`, ejecútalas en una `SparkSession` local compartida por la suite (`master("local[2]")`) y compara los resultados recogidos o usa una biblioteca auxiliar para la igualdad de DataFrames.

#### ¿Cómo simulas dependencias en Scala?

Prefiere diseñar para que el código sea fácil de probar: depende de traits o funciones y pasa implementaciones falsas simples en los tests. Para código muy orientado a Java, Mockito funciona mediante mockito-scala, pero usar muchos mocks suele indicar que los efectos no están separados de la lógica.

#### ¿Cómo ejecutas un subconjunto de tests con sbt?

`sbt "testOnly *AmountSuite"` ejecuta una suite, `testQuick` vuelve a ejecutar los tests fallidos y los modificados, y el prefijo `~` (`~testQuick`) los vuelve a ejecutar con cada cambio de archivo.

<!-- challenge -->

Cada suite de tests de Spark crea su propia `SparkSession`, y la ejecución de los tests tarda 15 minutos. ¿Cómo la aceleras?

<!-- solution -->

Comparte una sola sesión local entre suites mediante un trait o fixture común, ejecuta con `local[2]`, pon `spark.sql.shuffle.partitions` en un número pequeño y desactiva la interfaz web; la mayor parte del tiempo se iba en iniciar sesiones y en hacer shuffle a 200 particiones.

<!-- takeaways -->

- ScalaTest y MUnit son las opciones comunes.
- ScalaCheck encuentra casos límite.
- Comparte una sola sesión local de Spark en los tests.

<!-- unit: Calidad de código y migración -->

<!-- goals -->

- Mantener el código consistente con scalafmt, scalafix y las advertencias del compilador.
- Planificar una migración de Scala 2.13 a Scala 3.

<!-- concept -->

El formateo y el linting están automatizados en la mayoría de los equipos Scala: scalafmt formatea el código, scalafix aplica reglas de lint y reescrituras automáticas, y las advertencias del compilador, como imports sin usar o match no exhaustivos, detectan errores reales cuando la CI las trata como errores.

Migrar de Scala 2.13 a Scala 3 es en gran parte compatible a nivel de código fuente. El compilador puede reescribir la sintaxis antigua, y el código Scala 3 puede usar bibliotecas de Scala 2.13. Las partes difíciles son las macros de Scala 2, que hay que reescribir, y las dependencias que no han publicado versiones para Scala 3.

<!-- example -->

```scala
// build.sbt (Scala 3)
scalacOptions ++= Seq("-deprecation", "-feature", "-Wunused:all", "-Werror")
```
```bash
sbt scalafmtAll "scalafixAll RemoveUnused" test
```

#### ¿Qué son scalafmt y scalafix?

scalafmt es el formateador de código estándar, configurado en `.scalafmt.conf` y verificado en CI. scalafix es una herramienta de refactoring y linting cuyas reglas quitan imports sin usar, imponen convenciones y automatizan migraciones.

#### ¿Qué opciones del compilador ayudan a detectar errores?

`-deprecation` y `-feature` explican las advertencias, `-Wunused:all` informa de imports y variables sin usar, `-Wvalue-discard` señala valores no `Unit` descartados, y `-Werror` (antes `-Xfatal-warnings`) convierte las advertencias en errores para que no se acumulen.

#### ¿Cómo migras un proyecto de Scala 2.13 a Scala 3?

Actualiza las dependencias a versiones publicadas para Scala 3 (o usa las de 2.13 con `.cross(CrossVersion.for3Use2_13)`), compila con `-source:3.0-migration -rewrite` para corregir la sintaxis automáticamente, reescribe las macros y compila para ambas versiones durante la transición. Empieza por los módulos hoja y las bibliotecas, y después los servicios.

#### ¿Qué funcionalidades de Scala 2 cambiaron o desaparecieron en Scala 3?

Se eliminaron las macros de Scala 2, los tipos existenciales (`forSome`), la sintaxis de procedimiento (`def f() { ... }`), los literales de símbolo, los bucles `do`-`while` y la auto-aplicación de listas de parámetros vacías. Los implicits siguen funcionando pero los reemplazan los givens, y los package objects están obsoletos en favor de las definiciones de nivel superior.

#### ¿Qué es TASTy?

El formato de árbol de sintaxis abstracta tipado que Scala 3 guarda en archivos `.tasty` junto al bytecode. Conserva toda la información de tipos, lo que permite al compilador usar bibliotecas entre versiones de Scala 3, soporta `inline` y las macros, y alimenta las herramientas de los IDEs.

<!-- challenge -->

Una empresa tiene 40 servicios y bibliotecas en Scala 2.13 y quiere pasar a Scala 3. ¿Cómo lo planificas?

<!-- solution -->

Actualiza primero las bibliotecas compartidas y compílalas para 2.13 y 3, luego migra los servicios de a uno con las reescrituras de migración, reemplazando las macros y las dependencias sin soporte. Deja los jobs de Spark en 2.13, y activa las advertencias como errores cuando cada módulo compile limpio.

<!-- takeaways -->

- Automatiza el formateo, el linting y las advertencias en CI.
- Scala 3 puede usar bibliotecas de Scala 2.13.
- Migra primero las bibliotecas; los jobs de Spark se quedan en 2.13.

<!-- stage: Scala para ingeniería de datos -->

### Scala y Spark

<!-- unit: La API de Spark en Scala -->

<!-- goals -->

- Explicar la relación entre Scala y Spark y cuándo elegirla frente a PySpark.
- Crear una `SparkSession`, leer datos y escribir transformaciones de DataFrames en Scala.

<!-- concept -->

Spark está escrito en Scala, y su API de Scala es la más directa: sin procesos Python, Datasets tipados comprobados en compilación y acceso a los puntos de extensión internos de Spark. Las operaciones con DataFrames compilan a los mismos planes en cualquier lenguaje, así que PySpark es igual de rápido con las operaciones integradas; las ventajas de Scala aparecen en las UDF, los pipelines tipados, los conectores propios y las bibliotecas.

La API de DataFrames se lee casi igual en ambos lenguajes, con unos pocos símbolos propios de Scala como `$"col"` y `===`.

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

#### ¿Por qué Spark se asocia con Scala?

Spark se escribió en Scala en UC Berkeley, y su núcleo, sus APIs y la mayor parte de su ecosistema (conectores, el código original de Delta Lake) son Scala. Las funcionalidades nuevas aparecen primero en la API de Scala, y los internos de Spark son clases Scala.

#### Scala o PySpark: ¿cómo eliges?

PySpark encaja con equipos que trabajan en Python, usan bibliotecas de Python (pandas, ML) y se limitan a las funciones integradas. Scala encaja con equipos que quieren comprobaciones en compilación, Datasets tipados, UDF rápidas en la JVM, fuentes de datos propias o extensiones de Spark. El soporte de la plataforma y las habilidades del equipo suelen decidir.

#### ¿Una consulta con DataFrames es más rápida en Scala que en PySpark?

No con las operaciones integradas: ambos construyen el mismo plan lógico, que Catalyst optimiza y la JVM ejecuta. Las diferencias aparecen con las UDF, que en PySpark envían las filas a trabajadores Python, y con el código del lado del driver.

#### ¿Qué hace `import spark.implicits._`?

Trae al ámbito los encoders para primitivos, tuplas y case classes, la sintaxis `$"column"` y `toDF` y `toDS` sobre colecciones locales, como `Seq((1, "a")).toDF("id", "name")`.

#### ¿Cómo haces referencia a columnas en Spark con Scala?

Con `$"amount"`, `col("amount")`, `df("amount")` (útil para desambiguar columnas después de un join) o una cadena simple en los métodos que aceptan nombres. La sintaxis de símbolo de Scala 2, `'amount`, está obsoleta.

#### ¿Por qué Spark en Scala usa `===` para la igualdad entre columnas?

`==` es la igualdad de objetos de Scala y devuelve un `Boolean`, comparando los propios objetos `Column`. `===` construye una expresión de igualdad que se evalúa por fila, y `=!=` su negación.

<!-- challenge -->

`df.filter($"country" == "FR")` no compila en un job de Spark en Scala. ¿Por qué y cuál es la corrección?

<!-- solution -->

`==` compara el objeto `Column` con una cadena y devuelve un `Boolean`, que `filter` no acepta. Usa `$"country" === "FR"`, que construye una expresión de columna.

<!-- takeaways -->

- La API nativa de Spark es Scala.
- El código con DataFrames integrados rinde igual en Scala y en Python.
- Usa `===` y `=!=` para comparar columnas.

<!-- unit: Datasets y encoders -->

<!-- goals -->

- Usar Datasets tipados con case classes y encoders.
- Decidir entre Datasets y DataFrames.

<!-- concept -->

Un `Dataset[T]` es una colección distribuida de objetos tipados: lo transformas con funciones Scala normales sobre case classes, y el compilador comprueba los nombres y tipos de los campos. Un DataFrame es un `Dataset[Row]`, sin tipos. Los encoders convierten entre objetos de la JVM y el formato binario interno de Spark, y se derivan para case classes y primitivos.

Eso sí, las lambdas tipadas son opacas para el optimizador: `ds.filter(_.amount > 0)` deserializa cada fila en un objeto, mientras que `ds.filter($"amount" > 0)` puede empujarse hasta los archivos. Muchos equipos usan case classes en los bordes y expresiones de columna por dentro.

<!-- example -->

```scala
final case class Order(orderId: Long, customerId: String, amount: Double, country: String)

val ds = spark.read.parquet("s3://lake/silver/orders").as[Order]   // column names must match
val slow = ds.filter(_.amount > 1000)              // typed lambda: no pushdown
val fast = ds.filter($"amount" > 1000)             // column expression: pushdown
val counts = ds.groupByKey(_.country).count()      // Dataset[(String, Long)]
```

#### ¿Cuál es la diferencia entre un DataFrame y un Dataset?

Un Dataset tiene tipo: `Dataset[Order]` expone objetos `Order`, y las operaciones tipadas se comprueban en compilación. Un DataFrame es un `Dataset[Row]`, cuyas columnas solo se comprueban cuando se analiza el plan en ejecución. Ambos corren sobre el mismo motor.

#### ¿Qué es un encoder?

Un objeto que convierte entre un tipo de la JVM y el formato interno de filas de Spark, y que conoce el esquema. Spark deriva encoders para case classes, tuplas y primitivos mediante `import spark.implicits._`; otros tipos necesitan `Encoders.kryo` o una conversión.

#### ¿Por qué las operaciones tipadas con Datasets pueden ser más lentas?

Las lambdas como `map(o => ...)` o `filter(_.amount > 0)` son cajas negras para Catalyst: cada fila se debe deserializar en un objeto, y los filtros no se pueden empujar hasta Parquet. Las expresiones de columna mantienen los datos en el formato interno y siguen siendo optimizables.

#### ¿Cómo conviertes entre DataFrames y Datasets?

`df.as[Order]` da un Dataset (y falla si faltan columnas o los tipos no coinciden), `ds.toDF()` vuelve atrás, y `Seq(...).toDS()` o `spark.createDataset` construyen uno a partir de datos locales.

#### ¿Puedes usar Datasets desde PySpark?

No. Python es de tipado dinámico, así que PySpark solo expone DataFrames. Los Datasets tipados existen en Scala y Java.

#### ¿Cómo modelas columnas que aceptan null en una case class?

Con campos `Option`, como `amount: Option[Double]`. Un campo primitivo como `Double` no puede contener `null`, así que un valor nulo en los datos falla en ejecución.

<!-- challenge -->

Un job que lee `orders.as[Order]` falla en ejecución con un error de null en el campo `discount`, que está vacío en algunas filas. ¿Qué cambias?

<!-- solution -->

Declara el campo como `discount: Option[Double]` en la case class, para que los nulls se vuelvan `None`, y maneja el caso ausente en la transformación.

<!-- takeaways -->

- Los Datasets tienen tipo; los DataFrames son `Dataset[Row]`.
- Las lambdas tipadas se saltan el pushdown del optimizador.
- Las columnas que aceptan null necesitan campos `Option`.

<!-- unit: UDF, closures y serialización -->

<!-- goals -->

- Escribir UDF en Scala y saber cuándo evitarlas.
- Corregir "Task not serializable" y usar variables broadcast y recursos por partición.

<!-- concept -->

Spark envía a los executors las funciones que escribes, así que todo lo que referencia un closure debe ser serializable. Usar un campo o método de una clase que lo rodea captura el objeto entero, que a menudo contiene algo no serializable, como un cliente de base de datos, y el job falla con "Task not serializable".

Las UDF de Scala corren en la JVM y evitan el viaje de ida y vuelta a Python de PySpark, pero siguen siendo cajas negras para el optimizador. Las funciones integradas siguen siendo la primera opción, y una variable broadcast envía una tabla de búsqueda a cada executor una sola vez en lugar de con cada tarea.

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

#### ¿Por qué ocurre "Task not serializable" y cómo lo corriges?

Un closure enviado a los executors referencia algo que no se puede serializar, a menudo porque usa un campo o método de una clase que lo rodea, lo que captura toda la instancia. Copia el valor necesario en un `val` local antes del closure, mueve los helpers a un `object` o crea los recursos no serializables en los executors.

#### ¿Las UDF de Scala son más rápidas que las de Python?

Sí: corren dentro de la JVM del executor, sin serializar filas hacia un proceso Python. Siguen siendo opacas para Catalyst, que no puede optimizar a través de ellas ni empujar filtros más allá, así que las funciones integradas son aún más rápidas.

#### ¿Qué es una variable broadcast?

Un valor de solo lectura, como un mapa de búsqueda, que se envía una vez a cada executor y queda en caché ahí (`sparkContext.broadcast(value)`, leído con `.value`). Sin ella, un valor grande capturado por un closure viaja con cada tarea.

#### ¿Cuál es la diferencia entre una variable broadcast y un broadcast join?

Una variable broadcast envía un valor cualquiera que usas en tu propio código. Un broadcast join es una estrategia de join para DataFrames, activada automáticamente con tablas pequeñas o con la pista `broadcast(df)`, en la que Spark envía la tabla pequeña a cada executor en lugar de hacer shuffle de ambos lados.

#### ¿Qué son los acumuladores?

Variables compartidas a las que las tareas solo pueden sumar, como contadores de registros erróneos, leídas en el driver. Las actualizaciones hechas dentro de transformaciones pueden aplicarse dos veces cuando se reintentan tareas; solo las actualizaciones dentro de acciones cuentan una sola vez con garantía.

#### ¿Cómo usas un cliente de base de datos o HTTP dentro de un job de Spark?

Créalo una vez por partición con `foreachPartition` o `mapPartitions`, no una vez por fila ni en el driver, y escribe por lotes. El cliente nunca necesita serializarse porque se crea en el executor.

<!-- challenge -->

Un job envía cada fila a una API dentro de `foreach`, creando un cliente HTTP por fila, y es muy lento. Mover el cliente a un campo de la clase provoca "Task not serializable". ¿Cuál es la estructura correcta?

<!-- solution -->

Usa `foreachPartition`: crea un cliente por partición en el executor, envía las filas por lotes y cierra el cliente al final. No se captura nada no serializable, y el costo de conexión se paga una vez por partición.

<!-- takeaways -->

- Los closures solo deben capturar valores serializables.
- Prefiere funciones integradas a UDF, incluso en Scala.
- Crea los clientes por partición, no por fila.

### Trabajo con datos en Scala

<!-- unit: JSON, configuración y E/S -->

<!-- goals -->

- Convertir JSON en case classes y cargar configuración tipada.
- Manejar con seguridad archivos, llamadas HTTP, bases de datos y recursos.

<!-- concept -->

Fuera de Spark, los jobs y servicios en Scala leen JSON, configuración y archivos. Las bibliotecas JSON derivan codecs para case classes a partir de su estructura (circe, upickle, jsoniter-scala), así que la conversión devuelve valores tipados o un error claro en lugar de mapas de cadenas. La configuración en archivos HOCON se lee con Typesafe Config o se carga directamente en case classes con PureConfig.

Los recursos como archivos y conexiones deben cerrarse incluso cuando hay errores, y `scala.util.Using` lo hace para cualquier `AutoCloseable`.

<!-- example -->

```scala
import io.circe.Decoder
import io.circe.parser.decode

final case class Event(id: String, kind: String, amount: Option[BigDecimal]) derives Decoder

val parsed: Either[io.circe.Error, Event] =
  decode[Event]("""{"id":"e1","kind":"purchase","amount":12.5}""")
```

#### ¿Cómo conviertes JSON en Scala?

Con una biblioteca que derive codecs para case classes: circe (`derives Decoder`, luego `decode[Event](json)`), upickle o jsoniter-scala para alto rendimiento. La decodificación devuelve un `Either` con la ruta exacta del error cuando falta un campo o tiene el tipo equivocado.

#### ¿Cómo lees la configuración en Scala?

Typesafe Config lee archivos `application.conf` en formato HOCON, con valores que se pueden sobrescribir desde el entorno, como `url = ${?DB_URL}`. PureConfig carga la configuración directamente en case classes e informa de todos los campos ausentes o inválidos a la vez, al arrancar.

#### ¿Qué hace `scala.util.Using`?

Ejecuta un bloque con un recurso y lo cierra después, incluso con excepciones, como el try-with-resources de Java. `Using(resource)(f)` devuelve un `Try`, `Using.resource` devuelve el valor directamente y lanza la excepción si falla, y `Using.Manager` maneja varios recursos.

#### ¿Cómo trabajas con archivos y rutas?

Con `java.nio.file` (`Files`, `Paths`) desde Scala, u os-lib para scripts concisos (`os.read.lines`, `os.walk`, `os.proc` para subprocesos). `scala.io.Source` basta para leer archivos de texto simples.

#### ¿Cómo llamas a una API REST desde Scala?

Con sttp client (eligiendo un backend síncrono, de `Future` o de efectos) o requests-scala para scripts: define timeouts, reintenta los errores transitorios con backoff y decodifica las respuestas JSON en case classes.

#### ¿Cómo consultas una base de datos desde Scala?

Con JDBC directamente o mediante una biblioteca: Doobie para código con Cats Effect, Slick, ScalikeJDBC o Magnum. Usa consultas parametrizadas, un pool de conexiones como HikariCP, y `Using` o el manejo de recursos de la biblioteca para cerrar las conexiones.

<!-- challenge -->

Un job llama a `config.getString("db.url")` en lo profundo de su procesamiento y falla a la hora cuando la clave falta en producción. ¿Cómo lo evitas?

<!-- solution -->

Carga toda la configuración en una case class al arrancar (con PureConfig, o leyendo cada clave una vez) y falla de inmediato con la lista de lo que falta; el resto del código recibe la configuración tipada.

<!-- takeaways -->

- Deriva codecs JSON para las case classes.
- Carga y valida la configuración al arrancar.
- Cierra los recursos con `Using`.

<!-- unit: Rendimiento en la JVM -->

<!-- goals -->

- Evitar el boxing y el uso derrochador de colecciones.
- Medir el rendimiento con JMH y entender el calentamiento del JIT y la recolección de basura.

<!-- concept -->

El código Scala corre sobre el compilador just-in-time de la JVM, que optimiza el código caliente después de que ha corrido un tiempo. Por eso los microbenchmarks necesitan calentamiento, que JMH maneja, y los jobs de corta duración pagan costos de arranque. La recolección de basura recupera los objetos de vida corta con poco costo, pero tasas de asignación muy altas igual se notan como pausas.

El código genérico hace boxing de los primitivos (una `List[Int]` contiene objetos `java.lang.Integer`), así que los bucles numéricos calientes usan arreglos de primitivos. Elegir la colección adecuada y evitar las intermedias da las mayores ganancias; mide antes de optimizar.

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

#### ¿Qué es el boxing y cuándo ocurre en Scala?

Envolver un valor primitivo en un objeto (`Int` en `java.lang.Integer`) para usarlo donde se espera un objeto. Ocurre en colecciones y métodos genéricos, en `Option[Int]` y en los valores función, y cuesta asignaciones e indirección en los bucles calientes. Los arreglos de primitivos lo evitan.

#### ¿Cómo haces benchmarks correctos de código Scala?

Con JMH mediante el plugin sbt-jmh, que maneja el calentamiento de la JVM, los forks, la eliminación de código muerto y las estadísticas. Medir una sola ejecución con `System.nanoTime` mide sobre todo el intérprete y el compilador JIT, no tu código.

#### ¿Qué es el calentamiento del JIT?

La JVM primero interpreta el bytecode y luego compila a código máquina optimizado los métodos que se ejecutan con frecuencia. El código se vuelve más rápido tras miles de ejecuciones, así que los primeros segundos de un job o de un benchmark son más lentos que el régimen estable.

#### ¿Cómo afecta la recolección de basura a los programas Scala?

El código inmutable asigna muchos objetos de vida corta, que los recolectores generacionales como G1 (el de por defecto) recuperan con poco costo. Los problemas vienen de tasas de asignación muy altas o de grandes volúmenes de datos vivos; el tamaño del heap (`-Xmx`), la elección del recolector (ZGC para pausas cortas) y menos asignaciones son las palancas.

#### ¿Por qué evitar las excepciones para el control de flujo?

Crear una excepción captura una traza de pila, lo cual es costoso, y oculta el camino de fallo en los tipos. Devuelve `Option` o `Either` para los fallos esperados; para un control de flujo con excepciones inevitable, `scala.util.control.NoStackTrace` evita capturar la pila.

<!-- challenge -->

Un servicio de precios es lento, y un profiler muestra el 40 % del tiempo de CPU en recolección de basura y boxing. El bucle caliente suma valores de una `List[Double]` a través de varias llamadas a `map` y `filter`. ¿Qué haces?

<!-- solution -->

Reescribe el camino caliente como una sola pasada sobre un `Array[Double]` (un bucle `while` o un único fold sobre una view), eliminando las colecciones intermedias y el boxing; luego confirma la mejora con un benchmark JMH y el profiler.

<!-- takeaways -->

- El código genérico hace boxing de los primitivos.
- Haz benchmarks con JMH, tras el calentamiento.
- Quita las colecciones intermedias de los bucles calientes.

<!-- stage: Juntarlo todo -->

### Escenarios

<!-- unit: Diseñar un job de datos en Scala -->

<!-- goals -->

- Estructurar un job de Spark en Scala para que sea fácil de probar y seguro de reejecutar.
- Combinar modelos tipados, configuración, tests y empaquetado.

<!-- concept -->

Un job Scala de producción reúne las unidades anteriores: configuración cargada y comprobada al arrancar, case classes en los bordes, transformaciones escritas como funciones puras de DataFrame a DataFrame y probadas sobre datos pequeños, la entrada y salida en un `main` delgado, y un build que produce un solo artefacto para el clúster. Las escrituras idempotentes, que reemplazan una partición en lugar de añadirle datos, hacen seguras las reejecuciones.

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

#### ¿Cómo estructuras un job de Spark en Scala para que sea fácil de probar?

Separa las transformaciones puras (funciones `DataFrame => DataFrame` en un object) de la lectura, la escritura y la configuración en `main`. Los tests llaman a las transformaciones con DataFrames pequeños y una sesión local compartida; `main` queda tan delgado que solo necesita un test de integración.

#### ¿Cómo haces idempotentes las escrituras de un job de Spark?

Sobrescribe exactamente la porción que produce la ejecución: sobrescritura dinámica de particiones para tablas Parquet, `replaceWhere` o `MERGE` para tablas Delta e Iceberg. Un `append` simple duplica datos cada vez que se reintenta una ejecución.

#### ¿Cómo pasas argumentos y configuración a un job de Spark?

Argumentos de línea de comandos después del JAR en `spark-submit`, analizados con una biblioteca como scopt o decline; ajustes de Spark con `--conf`; valores propios de cada entorno desde archivos de configuración o el entorno, validados al arrancar.

<!-- challenge -->

Un job diario escribe con `mode("append")`, y un reintento tras un timeout duplicó los ingresos de un día. Reescribe su estrategia de escritura.

<!-- solution -->

Escribe con `mode("overwrite")`, particionado por fecha y con `partitionOverwriteMode` en `dynamic`, para que una ejecución reemplace solo la partición de su propio día (o usa `replaceWhere` sobre una tabla Delta); así las reejecuciones dejan los mismos datos.

<!-- takeaways -->

- Transformaciones puras, `main` delgado.
- Sobrescribe la porción; nunca añadas a ciegas.
- Valida primero los argumentos y la configuración.

<!-- unit: Ejercicios de programación en Scala -->

<!-- goals -->

- Resolver ejercicios de programación comunes de forma idiomática en Scala.
- Explicar las ventajas y desventajas de las soluciones funcionales e imperativas.

<!-- concept -->

En la programación en vivo, los entrevistadores buscan primero código correcto e idiomático: valores inmutables, métodos de colección, pattern matching y `Option` en lugar de `null`. Di la complejidad, empieza por la versión más clara y pasa a la mutación local o a los arreglos solo cuando puedas explicar por qué es más rápido.

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

#### Invierte el orden de las palabras de una frase.

```scala
def reverseWords(s: String): String = s.trim.split("\\s+").reverse.mkString(" ")
```

#### Encuentra el segundo valor distinto más grande de una lista.

```scala
def secondLargest(xs: List[Int]): Option[Int] =
  xs.distinct.sorted.reverse.lift(1)
```

Esto es O(n log n); un solo `foldLeft` que lleve los dos valores más grandes lo deja en O(n).

#### Encuentra la longitud de la subcadena más larga sin caracteres repetidos.

```scala
def longestUnique(s: String): Int =
  s.indices.foldLeft((0, 0, Map.empty[Char, Int])) { case ((best, start, last), i) =>
    val newStart = last.get(s(i)).filter(_ >= start).map(_ + 1).getOrElse(start)
    (best.max(i - newStart + 1), newStart, last.updated(s(i), i))
  }._1
```

#### Implementa una búsqueda binaria sobre un arreglo ordenado.

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

#### Aplana una estructura de enteros anidada a cualquier profundidad.

Modela el anidamiento con un enum y luego recorre de forma recursiva:

```scala
enum Nested:
  case Leaf(value: Int)
  case Node(children: List[Nested])

def flatten(n: Nested): List[Int] = n match
  case Nested.Leaf(v)  => List(v)
  case Nested.Node(cs) => cs.flatMap(flatten)
```

<!-- challenge -->

Después de tu FizzBuzz, el entrevistador pide una versión que maneje n = 100 millones sin construir la lista completa en memoria. ¿Qué cambias?

<!-- solution -->

Devuelve un `Iterator[String]` (`(1 to n).iterator.map { ... }`) o una view en lugar de una `List`, para que los valores se produzcan a demanda y quien llama pueda procesarlos en flujo.

<!-- takeaways -->

- Primero correcto e idiomático; después optimiza.
- Di la complejidad y las ventajas y desventajas.
- Usa iteradores para salidas grandes o infinitas.
