## Scala Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Scala study guide: about 220 questions](../../images/scala_study_guide_title_img.png)

About 220 questions on Scala for data engineering interviews: the language and its type system, collections and functional programming, contextual abstractions, concurrency, tooling and Java interop, Scala with Apache Spark, and a set of coding problems with solutions. Examples use Scala 3 syntax (3.9 LTS, released in September 2026) unless they involve Spark, which runs on Scala 2.13. The answers follow the official documentation at docs.scala-lang.org.

The guide follows a learning path in six stages. Each section is split into short units: learning goals, a concept explanation and a worked example, then questions (recall first, then application), a practical challenge and key takeaways. To **learn**, read each unit top to bottom. To **review**, switch to review mode or use "Skip to questions", mark answers you want to see again, and try a mixed review across sections.

<!-- QA -->
<!-- stage: Foundations -->

### Scala basics

<!-- unit: Scala and the JVM -->

<!-- goals -->

- Explain what Scala is, how it runs and how Scala 2 and Scala 3 relate.
- Choose a Scala version and run code with the `scala` command.

<!-- concept -->

Scala combines object-oriented and functional programming in one statically typed language that compiles to JVM bytecode. Every value is an object, functions are values, and the compiler infers most types, so code stays concise while type errors are caught before it runs.

Scala 3 redesigned the language in 2021 with cleaner syntax, givens instead of implicits, enums and union types. Releases follow two lines: Scala Next gets new features, while long-term support (LTS) versions get fixes for years. Spark, the main reason data engineers meet Scala, still runs on Scala 2.13.

<!-- example -->

```scala
// hello.scala
@main def hello(name: String): Unit =
  println(s"Hello, $name")
```
```bash
scala run hello.scala -- Ana      # compiles and runs; prints "Hello, Ana"
```

#### What is Scala?

A statically typed language for the JVM that unifies object-oriented and functional programming. Its name comes from "scalable language". It's used for Apache Spark, Kafka's original code base, Pekko and Akka systems, and backend services, and it also compiles to JavaScript (Scala.js) and native code (Scala Native).

#### How does Scala code run?

The compiler turns `.scala` files into JVM `.class` files (Scala 3 also writes `.tasty` files with the typed program tree), and the JVM runs them with its just-in-time compiler. Scala code can call any Java library directly, and Java code can call Scala.

#### What are the main differences between Scala 2 and Scala 3?

Scala 3 adds optional-braces syntax, `given` and `using` instead of implicits, extension methods, enums, union and intersection types, opaque types, top-level definitions, trait parameters and a new macro system based on `inline` and quotes. Most Scala 2.13 code compiles with small changes, and Scala 3 projects can use Scala 2.13 libraries, but Scala 2 macros must be rewritten.

#### What are Scala LTS and Scala Next?

Two release lines. Scala Next ships minor versions with new features (3.10 in October 2026). An LTS version gets at least three years of fixes without language changes: 3.3 was the first, and 3.9, released in September 2026, is the new one that libraries are moving to. Since 3.8, Scala 3 requires JDK 17 or later.

#### Which Scala version does Spark use?

Spark 4 is built for Scala 2.13 only (Spark 3 supported 2.12 and 2.13). There is no official Scala 3 build: Scala 3 can depend on the 2.13 artifacts, but Spark's encoders rely on Scala 2 features, so Spark jobs are written in Scala 2.13 or need community libraries.

#### What is the `scala` command?

Since Scala 3.5, `scala` is the Scala CLI: it compiles, runs, tests and packages single-module projects without a build file (`scala run`, `scala repl`, `scala test`, `scala package`), with dependencies and versions declared in `//> using` directives at the top of a file.

#### What is a `@main` method?

A Scala 3 annotation that turns a top-level method into a program entry point and parses command-line arguments by parameter type. In Scala 2, the entry point is a `def main(args: Array[String]): Unit` in an object, or an object extending `App`.

<!-- challenge -->

A team wants to write a new Spark job in Scala 3 because "it's the current version". What do you advise?

<!-- solution -->

Write the job in Scala 2.13, the version Spark 4 is built and tested for; Scala 3 works with Spark only through workarounds for encoders and libraries. Use Scala 3 for services and libraries outside Spark.

<!-- takeaways -->

- Scala is a statically typed OOP and FP language on the JVM.
- Scala Next adds features; LTS versions get fixes for years.
- Spark jobs use Scala 2.13.

<!-- unit: Values, variables and types -->

<!-- goals -->

- Use `val`, `var` and `lazy val`, and rely on type inference.
- Navigate Scala's type hierarchy, number types and equality.

<!-- concept -->

Scala prefers immutable bindings: a `val` can't be reassigned, a `var` can, and idiomatic code rarely needs `var`. The compiler infers types from the right-hand side, but public methods still declare them for readability and stable APIs.

Every type sits in one hierarchy: `Any` at the top, split into value types (`Int`, `Double`, `Boolean`, `Unit`) and reference types (`AnyRef`, Java's `Object`). `Nothing` sits at the bottom, the type of expressions that never return, such as a thrown exception. `==` calls `equals`, so it compares values, even for strings.

<!-- example -->

```scala
val rate = 0.19                  // Double, inferred
var retries = 0                  // reassignable: use sparingly
lazy val lookup = loadLookup()   // computed on first access, only once
val total: BigDecimal = BigDecimal("19.99") * 3
println("ab" + "c" == "abc")     // true: == compares values
def fail(msg: String): Nothing = throw IllegalStateException(msg)
```

#### What is the difference between `val`, `var` and `lazy val`?

A `val` is assigned once and can't be reassigned (the object it refers to may still be mutable). A `var` can be reassigned. A `lazy val` is computed the first time it's accessed, at most once and thread-safely, which defers expensive work until needed.

#### What is type inference, and when should you still write types?

The compiler deduces types from values and expressions, so `val n = 1` is an `Int`. Write types on public methods and fields (they document the API and keep it stable), on recursive methods (required), on givens, and when the inferred type is too specific, such as a `Some[Int]` where you want `Option[Int]`.

#### What are `Any`, `AnyVal`, `AnyRef`, `Nothing` and `Null`?

`Any` is the supertype of everything. `AnyVal` is the parent of value types (`Int`, `Double`, `Boolean`, `Char`, `Unit`), `AnyRef` the parent of reference types. `Nothing` is a subtype of every type and has no values; it's the type of `throw` and of empty collections such as `Nil`. `Null` is the type of `null`, a subtype of reference types.

#### What is `Unit`?

A type with a single value, `()`, returned by methods that are called for their side effects, like Java's `void`. Because it's a real value, every expression in Scala has a type, even a `println`.

#### What is the difference between `==` and `eq`?

`==` calls `equals`, compares values and handles `null` safely, so `"abc" == "ab" + "c"` is true, unlike in Java. `eq` compares references (whether both names point to the same object) and exists only on `AnyRef`.

#### How do Scala's number types behave?

`Int` (32-bit) and `Long` (64-bit) overflow silently, `Double` is a binary floating-point number, and `BigInt` and `BigDecimal` give arbitrary precision, which money needs. Integer division truncates toward zero (`7 / 2 == 3`, `-7 / 2 == -3`), and underscores make literals readable: `1_000_000`.

<!-- challenge -->

A class computes an expensive lookup table in a `val` field, but most instances never use it, and creating them is slow. What do you change?

<!-- solution -->

Make it a `lazy val`: it's computed on first access, at most once, so instances that never use the table don't pay for it.

<!-- takeaways -->

- Prefer `val`; `lazy val` defers work.
- `Any` is at the top, `Nothing` at the bottom.
- `==` compares values; `eq` compares references.

<!-- unit: Expressions and control structures -->

<!-- goals -->

- Use `if`, `match`, `for` and `try` as expressions.
- Read Scala 3's optional-braces syntax and replace `break` and `continue`.

<!-- concept -->

In Scala almost everything is an expression that returns a value: `if`, `match`, `try` and blocks, whose value is their last expression. That removes temporary variables, and code reads as a definition of the result rather than a series of assignments.

Scala 3 also lets indentation replace braces, with `then` and `do` keywords, the style used in the official documentation. Braces still work, and many codebases, including Spark ones on Scala 2.13, keep them.

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

#### What does "everything is an expression" mean in Scala?

Constructs that are statements in other languages return values: `if`/`else`, `match`, `try`/`catch` and blocks `{ ... }`, whose value is their last expression. You assign their result directly to a `val` instead of mutating a variable in each branch.

#### How does `if`/`else` work as an expression?

`val label = if amount > 0 then "credit" else "debit"`. Both branches determine the result type; without `else` the result is `Unit`. Scala has no ternary operator because `if` already is one.

#### What is the difference between a `for` loop and a `for` comprehension?

`for x <- xs do ...` runs a side effect for each element and returns `Unit`. `for x <- xs yield ...` builds a new collection (or Option, Future...) from the results. Both are translated into method calls (`foreach`, `map`, `flatMap`, `withFilter`).

#### Does Scala have `break` and `continue`?

Not as keywords. Use collection methods that stop early (`find`, `exists`, `takeWhile`), recursion, or, since Scala 3.3, `scala.util.boundary` with `break` to exit a block with a value.

#### What is the optional-braces syntax?

Scala 3 can use indentation to delimit blocks, with `then` after `if` conditions, `do` in loops and optional `end` markers for long blocks. Braces remain valid, and the two styles can be mixed; formatters and the compiler (`-rewrite -indent` or `-no-indent`) convert between them.

#### How does `try`/`catch`/`finally` work in Scala?

It's an expression: `catch` takes pattern-matching cases on exception types, and `finally` runs cleanup without affecting the result. Scala has no checked exceptions. For expected failures, `Try`, `Either` and `Using` are usually clearer than catching exceptions.

<!-- challenge -->

Code like `var status = ""` followed by `if (paid) status = "done" else status = "open"` appears throughout a project. Rewrite it idiomatically.

<!-- solution -->

`val status = if paid then "done" else "open"`: the `if` expression returns the value directly, with no mutable variable and no chance of forgetting a branch.

<!-- takeaways -->

- `if`, `match`, `try` and blocks return values.
- `for ... do` loops; `for ... yield` builds results.
- No `break`: use collection methods or `boundary`.

<!-- unit: Strings and interpolation -->

<!-- goals -->

- Build strings with the `s`, `f` and `raw` interpolators and multiline literals.
- Split, parse and transform strings safely.

<!-- concept -->

Scala strings are Java strings: immutable sequences of characters with all of Java's methods, plus Scala's collection methods such as `map`, `filter` and `reverse`. String interpolation builds text from values: `s` inserts them, `f` formats them printf-style with type checking, and `raw` leaves backslashes alone.

Triple-quoted strings span several lines without escaping, and `stripMargin` removes the indentation up to a `|` so the literal can follow the code's indentation.

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

#### What string interpolators does Scala have?

`s"..."` inserts values (`$name` or `${expr}`), `f"..."` formats them with printf-style specs checked at compile time (`$total%.2f`), and `raw"..."` doesn't process escape sequences. Libraries define their own, such as `sql"..."` in Doobie, which builds parameterized queries.

#### How do multiline strings and `stripMargin` work?

`"""..."""` literals span lines and don't need escaping for quotes or backslashes. `stripMargin` removes leading whitespace up to and including a `|` on each line, so the text can be indented with the surrounding code.

#### How do you build a long string efficiently?

Collect the parts and use `mkString` (`rows.mkString("\n")`, with an optional prefix and suffix), or a `StringBuilder` in a loop. Repeated `+` on strings copies the growing string each time.

#### Reverse a string, and check whether it is a palindrome ignoring case and punctuation.

```scala
def isPalindrome(s: String): Boolean =
  val letters = s.filter(_.isLetterOrDigit).toLowerCase
  letters == letters.reverse
```

#### How do you split and parse strings safely?

`split` takes a regular expression, so special characters such as `|` and `.` must be escaped (`split("\\|")`) or passed as a `Char` (`split('|')`). Use `trim` or `strip` for whitespace, and `toIntOption`, `toDoubleOption` or `toBooleanOption`, which return `None` instead of throwing on bad input.

<!-- challenge -->

`line.split("|")` returns every character separately instead of the fields. Why, and how do you fix it?

<!-- solution -->

`split` takes a regex, and `|` alone means "empty or empty", which matches between every character. Escape it (`line.split("\\|")`) or use the `Char` overload, `line.split('|')`.

<!-- takeaways -->

- `s`, `f` and `raw` interpolate; `f` checks formats.
- Use `mkString` instead of repeated `+`.
- `split` takes a regex; parse with `toIntOption`.

### Methods and functions

<!-- unit: Methods -->

<!-- goals -->

- Define methods with default, named and repeated parameters.
- Use multiple parameter lists and by-name parameters.

<!-- concept -->

Methods are defined with `def` in a class, an object or, in Scala 3, at the top level of a file. Default and named arguments replace most overloads and builders, and repeated parameters accept any number of arguments. A method can have several parameter lists, which helps type inference, lets a block be passed as the last argument, and separates context parameters.

By-name parameters (`=> A`) are evaluated each time they're used inside the method, not before the call, which lets methods take code to run later or not at all, such as a retry helper or a log message.

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

#### What is the difference between a method and a function in Scala?

A method is defined with `def` and belongs to a class, object or file; it isn't a value by itself. A function is an object of a function type such as `Int => Int` that you can store and pass around. Scala converts methods to functions automatically when a function is expected (eta-expansion).

#### What are default and named arguments?

Parameters can have default values (`port: Int = 5432`), and callers can pass arguments by name in any order (`connect("db", ssl = false)`). Together they replace most overloaded methods and builder classes and make call sites self-explanatory.

#### What are repeated parameters?

A parameter typed `Int*` accepts any number of arguments, received as a `Seq[Int]`. To pass an existing collection, spread it: `total(xs*)` in Scala 3, `total(xs: _*)` in Scala 2.

#### What are multiple parameter lists used for?

Type inference flows from one list to the next (`foldLeft(0)(_ + _)` knows the accumulator type from the first list), a single-argument last list can take a block in braces (`retry(3) { ... }`), and context parameters go in a separate `using` list. They also enable currying.

#### What is a by-name parameter?

A parameter declared `op: => A` is not evaluated at the call; the expression is passed unevaluated and runs each time the method uses it. It's how methods like `getOrElse`, `assert` messages or retry helpers receive code to run later, and it avoids computing values that may not be needed.

#### Why must recursive methods declare their return type?

The compiler infers a method's type from its body, but a recursive body depends on the method's own type, so inference can't finish. Declaring the return type breaks the cycle.

<!-- challenge -->

A helper `def debug(msg: String): Unit` is called as `debug(s"rows: ${dump(df)}")`, and the expensive `dump` runs even when debug logging is off. How do you fix it?

<!-- solution -->

Make the parameter by-name, `def debug(msg: => String)`, and evaluate `msg` only when debug logging is enabled; the string, and `dump`, are then never built otherwise.

<!-- takeaways -->

- Defaults and named arguments replace overloads.
- Multiple parameter lists help inference and blocks.
- By-name parameters delay evaluation.

<!-- unit: Functions as values -->

<!-- goals -->

- Write anonymous functions and use higher-order functions.
- Explain closures, eta-expansion, currying and function composition.

<!-- concept -->

Functions are values with types such as `Int => Int`. You pass them to methods like `map`, return them from methods and store them in collections, and short ones can use `_` as a placeholder for their parameters.

A method becomes a function automatically when one is expected (eta-expansion). A function that refers to variables from the scope where it was created captures them, which makes it a closure. Currying splits parameters into separate lists, so fixing the first ones yields a new, more specific function.

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

#### What is an anonymous function?

A function literal without a name: `(x: Int) => x * 2`, or `x => x * 2` when the type is known from context. It's an object of a function type and can be passed directly to higher-order methods.

#### What does the underscore mean in `_ + 1`?

Each `_` stands for the next parameter of an anonymous function: `_ + 1` is `x => x + 1`, and `_ + _` is `(a, b) => a + b`. It only works when each parameter is used once, in order.

#### What is a higher-order function?

A function or method that takes functions as parameters or returns one, such as `map`, `filter`, `foldLeft`, `sortBy` or a `retry` helper. They let you separate what to do with each element from how to iterate.

#### What is a closure?

A function that captures variables from the scope where it was defined, such as `k` in `x => x * k`. It captures variables, not values, so changes to a captured `var` are visible to the function. In Spark, everything a closure captures is serialized and shipped to executors.

#### What is eta-expansion?

The automatic conversion of a method into a function value, as in `nums.filter(isEven)`. Scala 3 does it whenever a method is used where a function is expected; Scala 2 sometimes needed an explicit `isEven _`.

#### What are currying and partial application?

Currying turns a method with several parameters into a chain of single-parameter lists: `def add(a: Int)(b: Int) = a + b`. Applying the first list gives a function waiting for the rest: `val add5 = add(5)` (`add(5) _` in Scala 2). Partial application can also fix any arguments with placeholders: `connect("db.local", _, true)`.

#### What are function types and composition?

`A => B` is shorthand for the trait `Function1[A, B]` (with `Function2` and so on for more parameters). Functions compose: `f andThen g` applies `f` first, `f compose g` applies `g` first, which builds pipelines from small steps.

<!-- challenge -->

Text cleaning is written as nested calls, `stripAccents(lower(trim(s)))`, repeated in many places with steps added or forgotten. How do you make it reusable?

<!-- solution -->

Define each step as a function value (`val trim: String => String = _.trim`, and so on) and compose them once: `val normalize = trim andThen lower andThen stripAccents`. Callers use `normalize(s)`, and the pipeline lives in one place.

<!-- takeaways -->

- Functions are values with types like `A => B`.
- Closures capture variables from their scope.
- Compose small functions with `andThen`.

<!-- unit: Partial functions -->

<!-- goals -->

- Write pattern-matching anonymous functions and partial functions.
- Use `collect` and `lift`.

<!-- concept -->

A block of `case` clauses is an anonymous function that matches its argument against patterns. When the cases don't cover every input, it's a partial function: a `PartialFunction[A, B]` can tell with `isDefinedAt` whether it applies to a value.

Collection methods such as `collect` use that to filter and transform in one step, keeping only the elements the cases match.

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

#### What is a partial function?

A function defined only for some inputs, typed `PartialFunction[A, B]` and usually written as a block of `case` clauses. `isDefinedAt(x)` tells whether it handles `x`; calling it on other inputs throws a `MatchError`.

#### How does `collect` differ from `map` and `filter`?

`collect` takes a partial function and keeps only the elements it's defined for, transformed by it: filter and map in one pass, with pattern matching to extract values. `collectFirst` returns the first result as an `Option`.

#### What does `lift` do?

It turns a `PartialFunction[A, B]` into a total function `A => Option[B]` that returns `None` where the partial function isn't defined, which avoids `MatchError`s.

#### How do you deconstruct tuples in lambdas?

With a case lambda, `pairs.map { case (k, v) => s"$k=$v" }`, which works in Scala 2 and 3. Scala 3 also untuples parameters automatically: `pairs.map((k, v) => s"$k=$v")`.

<!-- challenge -->

Code extracts parsed values with `results.filter(_.isRight).map(_.toOption.get)`. How do you simplify it?

<!-- solution -->

`results.collect { case Right(v) => v }`: one pass, no `.get`, and the pattern makes the intent explicit.

<!-- takeaways -->

- `case` blocks are pattern-matching functions.
- `collect` filters and maps in one step.
- `lift` makes partial functions return Options.

### Domain modeling

<!-- unit: Classes, objects and traits -->

<!-- goals -->

- Define classes, singleton objects and companion objects.
- Compose behavior with traits and understand linearization.

<!-- concept -->

A class declares its constructor parameters in its header; prefix one with `val` to make it a public field. Scala has no `static`: a singleton `object` holds what would be static members, and an object with the same name as a class, its companion, can access the class's private members and usually hosts factory methods.

Traits define interfaces with optional implementations and are mixed into classes. When several traits define the same method, linearization decides the order, and `super` calls go to the next trait in that order.

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

#### How do you define a class with constructor parameters?

Parameters go in the class header, which is the primary constructor; the class body runs as constructor code. A parameter becomes a public field with `val` (or `var`), and stays private to the class otherwise. Extra constructors are written as `def this(...)`. In Scala 3, `new` is optional.

#### What is a singleton object?

An `object` defines a class and its single instance at once, created lazily on first use. It holds utilities, constants and entry points, and replaces Java's static members.

#### What is a companion object?

An object with the same name as a class, in the same file. The class and its companion can access each other's private members; the companion typically holds factory methods (`apply`), constants and given instances for the class.

#### What is a trait, and how does it differ from an abstract class?

A trait defines abstract and concrete members and can be mixed into a class alongside other traits (`extends A with B`, or `extends A, B` in Scala 3). A class extends only one abstract class. Scala 3 traits can take parameters too, so abstract classes are mostly kept for Java interop or when a constructor is essential.

#### What is trait linearization?

The order in which Scala resolves members when several mixed-in traits define them: roughly right to left in the `extends` clause. `super.method()` in a trait calls the next implementation in that order, which allows "stackable" traits that each add behavior around the same method.

#### What do `require` and `assert` do?

`require(cond, msg)` checks a precondition on arguments and throws `IllegalArgumentException`. `assert(cond, msg)` checks an internal invariant and throws `AssertionError`. Both make invalid states fail early with a clear message.

#### What access modifiers does Scala have?

Members are public by default. `private` restricts them to the class and its companion, `protected` to subclasses, and qualified forms such as `private[etl]` open them to a whole package.

<!-- challenge -->

A `DateUtils` class has no state, yet code creates `new DateUtils()` everywhere just to call `parse`. How do you restructure it?

<!-- solution -->

Make it an `object DateUtils` (or top-level functions in a Scala 3 file), so `DateUtils.parse(...)` is called directly without creating instances.

<!-- takeaways -->

- Objects replace static members.
- Companions hold factories and givens.
- Traits mix behavior into classes.

<!-- unit: Case classes, enums and ADTs -->

<!-- goals -->

- Model data with case classes and enums.
- Build algebraic data types with sealed traits and enums.

<!-- concept -->

Case classes are the standard way to model immutable data. The compiler generates a constructor without `new`, field accessors, structural equality and hashing, a readable `toString`, a `copy` method and pattern matching support.

Combined, they form algebraic data types: a sealed trait or a Scala 3 enum lists every possible case, so the compiler warns when a match forgets one. Case classes are product types ("this and that"); enums and sealed hierarchies are sum types ("this or that").

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

#### What does a case class give you?

An `apply` factory (no `new`), public immutable fields, `equals` and `hashCode` based on the fields, a readable `toString`, `copy`, an `unapply` extractor for pattern matching, and serialization. It's the default choice for data records.

#### What does `copy` do?

It creates a new instance with some fields changed and the others kept: `order.copy(status = Status.Paid)`. It's how you "update" immutable data.

#### Why mark case classes `final`?

Extending a case class breaks the generated equality and pattern matching in subtle ways, so the recommended style is `final case class`. Variation belongs in a sealed trait or an enum with several cases.

#### What is a Scala 3 enum?

A type with a fixed set of cases. Simple enums (`case Pending, Paid`) have `values`, `valueOf` and `ordinal`; cases can also take parameters, which makes enums a concise way to write algebraic data types. Scala 2 expressed the same with a sealed trait and case objects.

#### What is an algebraic data type?

A type built from products (a case class combining fields) and sums (a choice between cases). Modeling a payment event as "authorized, captured or failed", each with its own fields, makes invalid combinations impossible to represent.

#### What does `sealed` mean?

A sealed trait or class can only be extended in the same file, so the compiler knows every subtype and can check that a `match` covers them all.

#### What is the difference between a case class and a regular class?

A regular class compares by reference, has no `copy` or extractor, and keeps constructor parameters private unless marked `val`. Use case classes for data, regular classes for objects with identity, behavior and hidden state.

#### What is a case object?

A singleton with case-class features (readable `toString`, pattern matching, serialization), used in Scala 2 for cases without data in a sealed hierarchy, such as `case object Pending extends Status`.

<!-- challenge -->

Order status is a `String` field, and a typo, `"payed"`, reached production data. How can the type system prevent it?

<!-- solution -->

Model the status as an enum (`Pending`, `Paid`, `Refunded`) and convert external strings once at the boundary with a function returning `Option` or `Either`, so invalid values are rejected there and can't exist further in.

<!-- takeaways -->

- Case classes model immutable data.
- Enums and sealed traits list every case.
- Parse strings into types at the boundary.

<!-- unit: Pattern matching -->

<!-- goals -->

- Match on values, types, case classes and collections.
- Use guards, binders and extractors, and rely on exhaustiveness checks.

<!-- concept -->

`match` is a switch that also takes values apart. It checks a value against patterns in order, binding parts of it to names: literals, types, case classes, tuples and lists, with guards for extra conditions.

On sealed types and enums, the compiler checks exhaustiveness and warns about missing cases, so adding a case turns into a list of compiler warnings to fix rather than run-time surprises. Custom extractors (`unapply`) make any type matchable.

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

#### How does pattern matching work in Scala?

`value match { case pattern => result ... }` tries each case in order and evaluates the first that matches, binding variables in the pattern. It's an expression, so it returns the chosen result.

#### What kinds of patterns are there?

Literals (`case 0`), variables and the wildcard `_`, typed patterns (`case s: String`), constructor patterns for case classes, tuples (`case (k, v)`), sequences (`case List(a, b, _*)`, `case x :: rest`), alternatives (`case "FR" | "BE"`) and binders that name a matched part (`case o @ Order(_, _, _, Status.Paid)`).

#### What is a guard?

An `if` condition after a pattern (`case Authorized(id, amt) if amt > 1000`). The case matches only if both the pattern and the condition do.

#### What is exhaustiveness checking?

For matches on sealed traits, enums, `Option` and similar types, the compiler warns when a possible case isn't covered. It's one of the strongest benefits of modeling data with algebraic data types.

#### What is an extractor?

An object with an `unapply` method that decides whether a value matches and what to bind:

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

#### What happens if no case matches?

A `scala.MatchError` is thrown at run time. Exhaustiveness warnings prevent it for sealed types; for open types such as strings, add a final `case _`.

#### Why can't you match on `List[String]` versus `List[Int]`?

Generic type arguments are erased on the JVM, so at run time both are just `List`. The compiler warns that such a pattern is unchecked. Match on the elements instead, or keep the type information with a `ClassTag` or a wrapper type.

<!-- challenge -->

A new `Disputed` case was added to `PaymentEvent`, and a report silently classifies disputes as "other" through a `case _ =>` branch. How do you make the compiler catch such gaps?

<!-- solution -->

Remove the wildcard from matches on sealed types and enums, so the compiler warns that `Disputed` isn't handled, and fail the CI build on warnings (`-Werror`).

<!-- takeaways -->

- `match` tests patterns in order and binds parts.
- Sealed types give exhaustiveness checks.
- Avoid wildcards on matches over your own ADTs.

<!-- stage: Collections and functional programming -->

### Collections

<!-- unit: The collections hierarchy -->

<!-- goals -->

- Distinguish immutable and mutable collections.
- Choose between `List`, `Vector`, `Array`, `Set` and `Map` by access pattern.

<!-- concept -->

Scala collections come in immutable versions, the default, and mutable ones in `scala.collection.mutable`. Immutable collections never change: operations return new collections that share most of their structure with the old one, so they're cheap to create and safe to share between threads.

The main families are sequences, sets and maps. Among sequences, `List` is a linked list that's fast at the head, `Vector` gives fast access and updates anywhere, `Array` is a mutable Java array, and `ArrayBuffer` grows efficiently. Choosing by access pattern matters more than any micro-optimization.

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

#### What is the difference between immutable and mutable collections?

Immutable collections can't change after creation; "adding" returns a new collection. Mutable collections change in place. Immutable ones are the default in Scala because they're safe to share and easier to reason about; mutable ones suit local, performance-sensitive code.

#### When do you use `List` versus `Vector`?

`List` is fast for prepending, head and tail access and recursive pattern matching, but indexing and appending are O(n). `Vector` has effectively constant-time indexing, appending and updating. `Seq(...)` creates a `List`, `IndexedSeq(...)` a `Vector`.

#### What is an `Array` in Scala?

A Java array: fixed size, mutable and stored compactly (primitives unboxed). It's used for interop and performance-sensitive code. `==` on arrays compares references, so compare contents with `sameElements`.

#### How do sets and maps work?

The default `Set` and `Map` are hash-based and unordered; `SortedSet` and `TreeMap` keep keys sorted. `map(key)` throws `NoSuchElementException` for a missing key, while `map.get(key)` returns an `Option` and `getOrElse` a default.

#### What is structural sharing?

Immutable collections reuse unchanged parts of the old collection in the new one: `0 :: xs` points to `xs` instead of copying it, and `Vector.updated` copies only a small path in its internal tree. That's why immutable updates are affordable.

#### What is the complexity of common `List` operations?

`head`, `tail` and prepending (`::`) are O(1). `length`, indexing with `apply`, `last` and appending (`:+`) are O(n), because the list must be traversed.

#### What is `Seq` in Scala 2.13 and 3?

`scala.Seq` is an alias for `scala.collection.immutable.Seq`. In Scala 2.12 it was `scala.collection.Seq`, which could also be mutable, a common source of compile errors when migrating code that passes arrays or buffers as `Seq`.

<!-- challenge -->

A job builds a `List` by appending in a loop, `acc = acc :+ row`, over a million rows, and takes minutes. What do you change?

<!-- solution -->

Each `:+` copies the whole list, making the loop O(n²). Prepend and reverse once at the end, use a `ListBuffer` or a builder, or better, express the loop as a `map` or `filter` over the source.

<!-- takeaways -->

- Immutable collections are the default.
- `List` is fast at the head; `Vector` everywhere.
- Arrays are mutable Java arrays.

<!-- unit: Transforming collections -->

<!-- goals -->

- Apply `map`, `flatMap`, `filter`, folds and grouping.
- Choose the right method for an aggregation.

<!-- concept -->

Collections share a large set of transformation methods. `map` transforms each element, `filter` keeps some, `flatMap` maps and flattens, and folds combine everything into one value. Grouping methods split a collection by key, the in-memory equivalent of SQL's `GROUP BY`.

Chaining these methods replaces most loops with code that states what the result is, and the same vocabulary appears in Spark, `Option`, `Future` and effect libraries.

<!-- example -->

```scala
final case class Sale(country: String, product: String, amount: Double)
val sales = List(Sale("FR", "a", 10), Sale("CO", "b", 5), Sale("FR", "b", 7))

val byCountry = sales.groupMapReduce(_.country)(_.amount)(_ + _)   // Map(FR -> 17.0, CO -> 5.0)
val total = sales.foldLeft(0.0)((acc, s) => acc + s.amount)        // 22.0
val (big, small) = sales.partition(_.amount >= 7)
val top = sales.sortBy(-_.amount).take(2)
```

#### What is the difference between `map` and `flatMap`?

`map` applies a function to each element and keeps the structure: `List(1, 2).map(x => List(x, x))` is `List(List(1, 1), List(2, 2))`. `flatMap` applies a function that returns a collection and flattens the results: `List(1, 1, 2, 2)`.

#### What is the difference between `foldLeft`, `foldRight` and `reduce`?

`foldLeft(init)(op)` combines elements from left to right starting from an initial value, and works on empty collections. `foldRight` goes from right to left. `reduce` uses the first element as the start and throws on an empty collection, so `reduceOption` is safer.

#### How do `groupBy`, `groupMap` and `groupMapReduce` differ?

`groupBy(key)` returns a `Map` from key to the elements with that key. `groupMap(key)(f)` also transforms each element. `groupMapReduce(key)(f)(op)` transforms and combines in one pass, without building intermediate lists: the efficient way to sum or count per key.

#### What do `partition`, `span` and `splitAt` do?

`partition(p)` splits into elements that satisfy `p` and those that don't. `span(p)` splits at the first element that fails `p`. `splitAt(n)` splits at a position. All return a pair of collections.

#### What do `zip`, `zipWithIndex` and `sliding` do?

`zip` pairs elements of two collections (stopping at the shorter), `zipWithIndex` pairs each element with its position, and `sliding(n)` iterates over overlapping windows of `n` elements, useful for moving averages and comparisons with the previous element.

#### How do you sort collections?

`sorted` uses the element type's `Ordering`, `sortBy(f)` sorts by a key, and `sortWith(lt)` takes a comparison. Tuples sort by several keys (`sortBy(s => (s.country, -s.amount))`), and `Ordering.by` and `.reverse` build custom orderings.

#### What do `exists`, `forall`, `find` and `count` do?

`exists(p)` is true if any element satisfies `p`, `forall(p)` if all do (true for an empty collection), `find(p)` returns the first match as an `Option`, and `count(p)` counts matches. The first three stop as soon as the answer is known.

#### Count word frequencies in a text and return the top n.

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

`orders.groupBy(_.customer).map((c, os) => c -> os.map(_.amount).sum)` runs out of memory on 50 million orders. What do you change?

<!-- solution -->

`groupBy` builds a full list of orders per customer before summing. `orders.groupMapReduce(_.customer)(_.amount)(_ + _)` aggregates in one pass, keeping only one running total per customer.

<!-- takeaways -->

- `map` keeps structure; `flatMap` flattens.
- Prefer `foldLeft` and `reduceOption` to `reduce`.
- `groupMapReduce` aggregates per key in one pass.

<!-- unit: Lazy collections and iterators -->

<!-- goals -->

- Avoid intermediate collections with views, iterators and `LazyList`.
- Process large files in constant memory.

<!-- concept -->

Strict collections compute each step fully: `xs.map(f).filter(p).take(10)` builds two complete intermediate collections. A view makes the chain lazy, computing only the elements that are needed. An iterator hands out elements one at a time and can be consumed only once, which suits files and streams. A `LazyList` computes elements on demand, remembers them, and can be infinite.

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

#### What is a view?

A lazy wrapper over a collection (`xs.view`): transformations are recorded and applied element by element only when a result is requested, for example with `toList` or `sum`. It avoids building intermediate collections in long chains.

#### What is the difference between an `Iterator` and an `Iterable`?

An `Iterable` (such as a `List`) can be traversed many times. An `Iterator` yields elements with `hasNext` and `next` and is exhausted after one pass, so calling `size` on it consumes it. Methods like `getLines()` return iterators.

#### What is `LazyList`?

A lazily evaluated, memoized sequence that can be infinite, built with `#::`. It replaced the deprecated `Stream` in Scala 2.13. Holding on to its head keeps every computed element in memory.

#### How do you read a large file line by line?

Iterate over `Source.fromFile(path).getLines()` (or `java.nio.file.Files.lines`) inside `Using`, transforming and folding the iterator without converting it to a list, so only one line is in memory at a time and the file is closed afterwards.

#### How do you process items in batches?

`iterator.grouped(1000)` yields batches of 1,000 elements (the last one may be shorter), and `sliding(n, step)` yields windows. On an iterator, both stay lazy, which suits bulk inserts or API calls in chunks.

<!-- challenge -->

`Source.fromFile(path).getLines().toList.filter(isError)` crashes with `OutOfMemoryError` on a 20 GB log. What do you change?

<!-- solution -->

Keep it an iterator: drop `toList`, filter and count or write results as you go, and wrap the source in `Using` so the file is closed. Memory then stays constant regardless of file size.

<!-- takeaways -->

- Views avoid intermediate collections.
- Iterators are consumed once and stream data.
- Never `toList` a file you can't fit in memory.

<!-- unit: Collection problems -->

<!-- goals -->

- Solve classic coding problems with Scala collections.
- Choose between collection methods, folds and local mutation.

<!-- concept -->

Coding problems in Scala test whether you think in transformations. Most have a short solution with collection methods: deduplicate with `distinct` or a map keyed by ID, two-sum with a map of seen values, intervals with a sort and a fold. Inside a function, local mutation such as a mutable map or builder is fine when it's faster and doesn't escape.

<!-- example -->

```scala
final case class Row(id: String, ts: Long, value: String)

def latestById(rows: Seq[Row]): Iterable[Row] =
  rows.groupMapReduce(_.id)(identity)((a, b) => if a.ts >= b.ts then a else b).values
```

#### Find the two numbers in a sequence that add up to a target (two-sum).

Use a map of values already seen, for O(n):

```scala
def twoSum(nums: Vector[Int], target: Int): Option[(Int, Int)] =
  val seen = collection.mutable.HashMap.empty[Int, Int]   // local mutation, never shared
  nums.indices.iterator.flatMap { i =>
    val hit = seen.get(target - nums(i)).map(j => (j, i))
    seen(nums(i)) = i
    hit
  }.nextOption()
```

#### How do you remove duplicates while keeping order?

`xs.distinct` keeps the first occurrence of each element, and `xs.distinctBy(_.id)` (2.13+) the first occurrence of each key. Both preserve the original order.

#### Merge overlapping intervals.

```scala
def merge(intervals: List[(Int, Int)]): List[(Int, Int)] =
  intervals.sortBy(_._1).foldLeft(List.empty[(Int, Int)]) {
    case ((s0, e0) :: rest, (s, e)) if s <= e0 => (s0, e0.max(e)) :: rest
    case (acc, interval)                       => interval :: acc
  }.reverse
```

#### Group a list of words into anagrams.

```scala
def groupAnagrams(words: List[String]): List[List[String]] =
  words.groupBy(_.sorted).values.toList
```

#### Check whether a string of brackets is balanced.

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

#### Find the first non-repeating character in a string.

```scala
def firstUnique(s: String): Option[Char] =
  val counts = s.groupMapReduce(identity)(_ => 1)(_ + _)
  s.find(c => counts(c) == 1)
```

#### Compute a running total and a 3-item moving average.

```scala
val values = List(3, 5, 2, 8, 6)
val running = values.scanLeft(0)(_ + _).tail                    // List(3, 8, 10, 18, 24)
val moving = values.sliding(3).map(w => w.sum / 3.0).toList     // List(3.33, 5.0, 5.33)
```

<!-- challenge -->

A solution checks `if !result.contains(x)` on a growing `List` for each of a million items, and takes minutes. What do you change?

<!-- solution -->

`contains` on a `List` is O(n), so the loop is O(n²). Track seen items in a `Set` (O(1) membership), or use `distinct`, which does exactly that.

<!-- takeaways -->

- Most problems are a few collection methods.
- Maps and sets turn O(n²) searches into O(n).
- Local mutation is fine when it doesn't escape.

### Functional programming

<!-- unit: Immutability and pure functions -->

<!-- goals -->

- Explain pure functions, referential transparency and side effects.
- Keep side effects at the edges of a program.

<!-- concept -->

A pure function returns the same output for the same input and does nothing else: no mutation, no I/O, no exceptions used for control flow. Pure code is easy to test, reason about, cache and run in parallel, which is why functional programming builds programs from pure functions over immutable data.

Real programs still read files and call APIs. The functional approach pushes these effects to the edges, a "functional core, imperative shell", or describes them as values that run later, as effect libraries do.

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

#### What is functional programming?

A style that builds programs from pure functions and immutable values, treats functions as values, and handles errors and effects explicitly in types. Scala supports it alongside object-oriented programming, and most Scala code mixes both.

#### What is a pure function?

A function whose result depends only on its arguments and that has no observable side effects. `def add(a: Int, b: Int) = a + b` is pure; a function that reads the clock, logs or mutates a field isn't.

#### What is referential transparency?

An expression is referentially transparent if you can replace it with its value without changing the program's behavior. Pure functions give that property, which makes refactoring, caching and reasoning about code safe.

#### What are side effects, and how do you manage them?

Anything a function does besides returning a value: I/O, mutation, exceptions, reading the time or random numbers. Keep them in a thin outer layer, pass inputs such as the current time as parameters, and use effect types such as `IO` when you need to compose them.

#### Why does immutability help with concurrency?

Immutable data can be shared between threads without locks, because no one can change it; race conditions need shared mutable state. It also makes Spark closures and caches safer.

#### Is mutation ever acceptable in Scala?

Yes, when it's local and doesn't escape: a `var` or mutable builder inside a function that returns an immutable result, or a tight loop where performance matters. The function stays pure from the outside.

<!-- challenge -->

A transformation reads `LocalDate.now()` internally, and its tests fail every night around midnight. How do you fix it?

<!-- solution -->

Pass the date (or a `java.time.Clock`) as a parameter, so the function is pure: production code passes today's date, tests pass a fixed one.

<!-- takeaways -->

- Pure functions depend only on their inputs.
- Push effects to the edges.
- Local mutation is fine if it doesn't escape.

<!-- unit: Option, Either and Try -->

<!-- goals -->

- Replace `null` and exceptions with `Option`, `Either` and `Try`.
- Chain results and collect validation errors.

<!-- concept -->

Instead of `null` and thrown exceptions, Scala represents "may be missing" as `Option` (`Some` or `None`), "success or a described failure" as `Either` (`Right` or `Left`), and "a computation that may throw" as `Try` (`Success` or `Failure`). The types make failures visible in signatures, so callers must deal with them.

All three support `map`, `flatMap`, `getOrElse` and for-comprehensions: you chain steps, and the first failure short-circuits the rest.

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

#### What is `Option`, and why use it instead of `null`?

A container that is either `Some(value)` or `None`. The type says a value may be missing, so the compiler makes callers handle it, while `null` is invisible in types and fails later with a `NullPointerException`.

#### How do you get a value out of an `Option` safely?

With `getOrElse(default)`, `fold`, `map` and `flatMap` to keep working inside it, or a `match`. Avoid `.get`, which throws on `None` and brings back the problem `Option` solves.

#### What is `Either`?

A value that is `Left(error)` or `Right(result)`. It's right-biased: `map` and `flatMap` work on the `Right` side and pass a `Left` through, so it's used for operations that can fail with a meaningful error.

#### What is `Try`?

A wrapper for code that may throw: `Try(expr)` gives `Success(value)` or `Failure(exception)`. It's mostly used at boundaries with exception-throwing libraries, then converted with `toOption` or `toEither`.

#### When do you use `Option`, `Either` or `Try`?

`Option` when absence is normal and needs no explanation (a lookup). `Either` when the caller needs to know why something failed (validation, parsing with messages). `Try` to capture exceptions from code you don't control.

#### How do you handle `null` from Java APIs?

Wrap the value at the boundary: `Option(javaValue)` turns `null` into `None`. Scala 3 also has an opt-in explicit-nulls mode in which reference types are non-nullable and Java results are typed `T | Null`.

#### How do you collect all validation errors instead of stopping at the first?

`Either` in a for-comprehension stops at the first `Left`. To keep all of them, validate each item and split results with `partitionMap`, or use an accumulating type such as Cats' `ValidatedNel`:

```scala
val (errors, amounts) = rows.partitionMap(r => parseAmount(r("amount")))
```

<!-- challenge -->

A parser returns `null` for invalid input, and `NullPointerException`s appear in code far from the parser. How do you fix the design?

<!-- solution -->

Return `Option` (or `Either` with an error message) from the parser, so every caller handles the failure where it happens, and the compiler enforces it.

<!-- takeaways -->

- `Option` for missing, `Either` for errors, `Try` for exceptions.
- Chain with `map`, `flatMap` and for-comprehensions.
- Never call `.get` on an `Option`.

<!-- unit: For-comprehensions -->

<!-- goals -->

- Read and write for-comprehensions and their translation.
- Use them with collections, `Option`, `Either` and `Future`.

<!-- concept -->

A for-comprehension is syntax over `flatMap`, `map` and `withFilter`. Each generator (`<-`) is a step, and `yield` builds the result. Because it's only method calls, it works with any type that defines them: collections, `Option`, `Either`, `Try`, `Future` and effect types.

The first generator's type decides the result type, so unrelated types such as `Option` and `Future` can't be mixed in one comprehension without converting them first.

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

#### What is a for-comprehension?

Syntax for sequencing operations on values that support `map` and `flatMap`: generators (`x <- xs`), filters (`if cond`) and value definitions (`y = f(x)`), followed by `yield`. It reads like a sequence of steps.

#### How is a for-comprehension translated?

Every generator but the last becomes a `flatMap`, the last one a `map` with the `yield` expression, and `if` filters become `withFilter`. A comprehension with `do` instead of `yield` becomes `foreach` calls.

#### Can you mix `Option`, `List` and `Future` in one for-comprehension?

Not directly: the steps must share a type that can be flattened together. Convert first (`option.toRight(error)`, `Future.fromTry`, `opt.toList`), or use monad transformers or effect libraries designed to combine them.

#### What did "better fors" change in Scala 3.8?

SIP-62, the default since 3.8, lets a comprehension start with an alias (`x = ...`), translates aliases without building intermediate tuples, and drops the final `map` when `yield` only returns the last bound value. The translation is simpler and cheaper, which matters most for effect types.

#### What is a monad, in practical terms?

A type with `flatMap` and a way to wrap a plain value (`Some(x)`, `List(x)`, `Future.successful(x)`, `IO.pure(x)`) that obeys a few laws. Practically, it's anything you can chain in a for-comprehension, each step depending on the previous one.

<!-- challenge -->

A parsing function nests four `flatMap` calls on `Either` values, and nobody can read it. How do you rewrite it?

<!-- solution -->

As a for-comprehension, one generator per step (`a <- parseA(raw)`, `b <- parseB(a)`, ...) and a `yield` that builds the result. The semantics are identical, and the steps read top to bottom.

<!-- takeaways -->

- `for`/`yield` is `flatMap`, `map` and `withFilter`.
- It works with any type that defines them.
- The first generator decides the result type.

<!-- unit: Recursion and tail calls -->

<!-- goals -->

- Write recursive functions over lists.
- Make recursion stack-safe with `@tailrec` and accumulators.

<!-- concept -->

Recursion mirrors recursive data: a `List` is either empty or a head followed by another list. Each recursive call uses a stack frame, so deep recursion on the JVM throws `StackOverflowError`.

When the recursive call is the last thing a method does (tail position), the Scala compiler turns it into a loop, and `@tailrec` makes compilation fail if it can't. Folds already package most of these loops.

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

#### What is tail recursion?

A recursive call that is the last operation of a method, so nothing remains to do after it returns. `loop(tail, acc + h)` is in tail position; `h + sum(tail)` isn't, because the addition happens after the call.

#### What does `@tailrec` do?

It asks the compiler to verify that a method is tail-recursive and compiled into a loop; compilation fails otherwise. It doesn't enable the optimization (the compiler does it anyway), but it guarantees it.

#### Why doesn't the JVM optimize all tail calls?

The JVM has no general tail-call elimination. Scala optimizes only self-recursive calls in methods that can't be overridden (local, `private` or `final`). Mutually recursive functions need trampolines, such as `scala.util.control.TailCalls`, or an effect library.

#### When should you use a fold instead of explicit recursion?

Whenever the recursion just walks a collection and accumulates a result: `foldLeft` is already a stack-safe loop and states the intent. Explicit recursion is clearer for trees, early exit or several accumulators.

#### Reverse a list recursively.

```scala
import scala.annotation.tailrec

def reverse[A](xs: List[A]): List[A] =
  @tailrec def loop(rest: List[A], acc: List[A]): List[A] = rest match
    case Nil    => acc
    case h :: t => loop(t, h :: acc)
  loop(xs, Nil)
```

<!-- challenge -->

`def count(xs: List[Int]): Int = if xs.isEmpty then 0 else 1 + count(xs.tail)` fails with `StackOverflowError` on 100,000 elements. How do you fix it?

<!-- solution -->

Carry the count in an accumulator so the recursive call is in tail position, and annotate the helper with `@tailrec`; or simply use `xs.size` or a fold.

<!-- takeaways -->

- Each non-tail call uses a stack frame.
- `@tailrec` guarantees a loop.
- Folds replace most explicit recursion.

<!-- stage: Types and abstractions -->

### The type system

<!-- unit: Generics and variance -->

<!-- goals -->

- Write generic classes and methods with type bounds.
- Explain covariance, contravariance and type erasure.

<!-- concept -->

Generics let one definition work for many types while staying type-safe: `List[A]`, `def first[A](xs: List[A]): Option[A]`. Bounds restrict type parameters: `A <: Animal` requires a subtype, `B >: A` a supertype.

Variance says how subtyping of the parameter carries over to the container. Immutable containers are usually covariant (`List[+A]`: a list of cats is a list of animals). Types that consume values are contravariant (`-A`): something that accepts any animal can be used where something accepting cats is needed. Mutable containers must be invariant.

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

#### What are generics in Scala?

Classes, traits and methods with type parameters in square brackets (`class Box[A]`, `def first[A](xs: List[A])`), so the same code works for any type while the compiler still checks every use.

#### What are upper and lower type bounds?

`A <: Upper` restricts `A` to subtypes of `Upper`, so code can use `Upper`'s members. `B >: Lower` restricts `B` to supertypes of `Lower`, typically used to widen a type when adding elements to a covariant collection.

#### What is covariance?

`Container[+A]` means that if `Cat` is a subtype of `Animal`, `Container[Cat]` is a subtype of `Container[Animal]`. It's safe for types that only produce `A` values, such as immutable collections, `Option` and `Future`.

#### What is contravariance?

`Container[-A]` reverses the relation: `Sink[Animal]` is a subtype of `Sink[Cat]`. It fits types that only consume `A`, such as function parameters (`Function1[-A, +B]`), encoders or writers.

#### Why is `Array` invariant while `List` is covariant?

An `Array` is mutable. If `Array[Cat]` were an `Array[Animal]`, you could store a `Dog` in it through the animal view, breaking the cat array. An immutable `List` can't be changed, so treating a list of cats as a list of animals is safe.

#### Why does `:+` on a `List[Cat]` accept a `Dog`?

Its signature is `def :+[B >: A](elem: B): List[B]`: the lower bound lets the compiler widen the element type to a common supertype, so appending a `Dog` to a `List[Cat]` returns a `List[Animal]`.

#### What is type erasure?

On the JVM, generic type arguments disappear at run time: a `List[Int]` and a `List[String]` are both just `List`. Code that needs the runtime class, such as creating an `Array[A]`, asks for a `ClassTag[A]`.

<!-- challenge -->

You declare `class Box[+A](var value: A)`, and the compiler rejects it. Why?

<!-- solution -->

A `var` has a setter that takes an `A`, a contravariant position. If it compiled, a `Box[Cat]` seen as `Box[Animal]` could receive a `Dog`. Make the field a `val` to keep the box covariant, or keep it invariant if it must be mutable.

<!-- takeaways -->

- Bounds restrict type parameters.
- Producers are covariant; consumers contravariant.
- Mutable containers are invariant.

<!-- unit: Union, intersection and opaque types -->

<!-- goals -->

- Use Scala 3 union and intersection types.
- Create zero-cost domain types with opaque types, and use named tuples.

<!-- concept -->

Scala 3 adds types that were awkward to express before. A union `A | B` holds a value of either type, without wrapping it in `Either` or a sealed trait. An intersection `A & B` has the members of both, replacing Scala 2's `A with B`.

An opaque type gives an existing type a new name that only its defining scope can see through: a `CustomerId` is a `String` at run time, but code outside can't mix it up with an `OrderId` or a plain string, and there is no wrapper cost. Named tuples, stable since 3.7, give tuple elements names without declaring a case class.

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

#### What is a union type?

`A | B` is the type of values that are either `A` or `B`, such as `Int | String`. You use the value by matching on its type. Unlike `Either`, there's no wrapper and no left or right meaning, and the order of the types doesn't matter.

#### What is an intersection type?

`A & B` is the type of values that are both `A` and `B`, with the members of both. A parameter typed `Closeable & Flushable` accepts any object implementing both interfaces. It replaces Scala 2's compound types `A with B`.

#### What is an opaque type?

A type alias that is transparent only inside the scope that defines it: `opaque type CustomerId = String`. Outside, it's a distinct type, so it can't be mixed with other strings, but at run time it's just a `String`, with no allocation. Its companion object and extension methods define what you can do with it.

#### How do opaque types compare with value classes?

Scala 2 value classes (`class CustomerId(val value: String) extends AnyVal`) also avoid wrappers, but box the value in many situations: in collections, generics and pattern matching. Opaque types never box, so they replace value classes in Scala 3.

#### What are named tuples?

Tuples whose elements have names: `(rows = 1200, errors = 3)`, with the type `(rows: Int, errors: Int)`. Elements are accessed by name, and a named tuple can be used where a plain tuple is expected. They suit lightweight results without declaring a case class.

#### What is a type alias?

`type Row = Map[String, String]` gives a shorter name to an existing type. It's purely a name: a `Row` and a `Map[String, String]` are interchangeable, unlike an opaque type, which adds type safety.

#### When would you use a union type rather than `Either`?

A union fits when both alternatives are equally valid values, as in a field that is an `Int` or a `String`. `Either` fits when one side is an error, because it carries success or failure meaning and supports `map`, `flatMap` and for-comprehensions.

<!-- challenge -->

Functions take `customerId: String, orderId: String`, and callers keep passing them in the wrong order. How do you prevent it at compile time without run-time cost?

<!-- solution -->

Define `opaque type CustomerId = String` and `opaque type OrderId = String` with smart constructors, and change the signatures. Swapped arguments no longer compile, and both are still plain strings at run time.

<!-- takeaways -->

- `A | B` is either; `A & B` is both.
- Opaque types give type safety without wrappers.
- Named tuples name lightweight results.

### Contextual abstractions

<!-- unit: Givens and using clauses -->

<!-- goals -->

- Pass context with `using` clauses and provide it with `given` instances.
- Import givens, summon them, and map Scala 2 implicits to Scala 3.

<!-- concept -->

Some parameters are context rather than data: an execution context, a configuration, an ordering. Passing them explicitly through every call is noise. Scala 3 lets a method declare them in a `using` clause, and the compiler fills them in from `given` instances in scope, based on their type.

This is Scala 3's redesign of Scala 2 implicits. Givens define instances, `using` clauses consume them, and givens are imported explicitly with `import x.given`, so it's clear where they come from.

<!-- example -->

```scala
final case class Config(env: String, batchSize: Int)

def load(path: String)(using cfg: Config): String =
  s"loading $path in ${cfg.env} with batches of ${cfg.batchSize}"

given Config = Config("dev", 500)
load("s3://lake/orders")                               // Config passed automatically
load("s3://lake/orders")(using Config("prod", 5000))   // or explicitly
```

#### What problem do givens and `using` clauses solve?

They pass contextual values (configuration, execution contexts, type class instances) without writing them at every call site, while keeping the dependency visible in method signatures and resolved at compile time.

#### What is a given instance?

A value declared with `given` that the compiler can supply for a `using` parameter of its type: `given Config = Config("dev", 500)`, or a named one, `given devConfig: Config = ...`. Givens can also depend on other givens.

#### What is a `using` clause?

A parameter list marked `using`, such as `(using cfg: Config)`, whose arguments the compiler fills in from givens in scope. Callers can still pass them explicitly with `(using value)`. Anonymous ones are written `(using Config)` and retrieved with `summon`.

#### How do you import givens?

Wildcard imports (`import a.*`) don't bring givens in. Import them with `import a.given` (all givens) or by type, `import a.{given Ordering[?]}`, which makes their origin explicit.

#### What does `summon` do?

`summon[T]` returns the given instance of type `T` in scope, or fails to compile if there is none. It's Scala 3's equivalent of Scala 2's `implicitly`.

#### How do Scala 2 implicits map to Scala 3?

Implicit values and methods become `given` instances, implicit parameters become `using` clauses, implicit classes become extension methods, and implicit conversions become `given Conversion[A, B]` instances. Scala 3 still accepts Scala 2 implicits, which makes gradual migration possible.

#### Where does the compiler look for givens?

First in the lexical scope: local definitions, enclosing classes and imports. Then in the implicit scope of the type it's looking for, which includes the companion objects of the type and its type arguments. That's why type class instances usually live in companion objects.

<!-- challenge -->

An `ExecutionContext` parameter is passed explicitly through 30 methods of a service. How do you simplify it without global state?

<!-- solution -->

Declare it as `(using ExecutionContext)` in those methods and provide one `given ExecutionContext` at the application's edge (or in tests). Call sites no longer mention it, and each environment can still supply its own.

<!-- takeaways -->

- `using` clauses take context; `given` provides it.
- Import givens explicitly with `import x.given`.
- Instances in companion objects are found automatically.

<!-- unit: Type classes -->

<!-- goals -->

- Define type classes with traits and given instances.
- Use context bounds, derivation and multiversal equality.

<!-- concept -->

A type class adds behavior to types you don't own, without inheritance. A trait describes the behavior (`Show[A]`, `Encoder[A]`), given instances implement it for specific types, and methods require an instance with a context bound. Supporting a new type means writing one more instance, not changing the type.

Libraries use the pattern everywhere: JSON codecs in circe, Spark's encoders, Cats' `Monoid` and `Functor`, and `Ordering` in the standard library. Scala 3 can derive instances automatically with `derives`.

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

#### What is a type class?

A generic trait describing a capability (`Show[A]`, `Ordering[A]`, `Encoder[A]`) plus instances for specific types, provided as givens. Code that needs the capability asks for an instance, so behavior is attached to types from outside, at compile time.

#### How do you define and use a type class in Scala 3?

Write a trait with a type parameter, provide `given` instances for the types you support (usually in the trait's or the type's companion object), and require an instance where you need it with a context bound or a `using` clause. Extension methods in the trait give call sites a natural syntax such as `value.show`.

#### What is a context bound?

`def describe[A: Show](a: A)` is shorthand for a `using` parameter of type `Show[A]`. Since Scala 3.6 the instance can be named in the bound, `[A: Show as s]`; otherwise it's retrieved with `summon[Show[A]]`.

#### What is type class derivation?

`case class Order(...) derives Codec` asks the compiler to generate an instance from the type's structure, using a `derived` method that the type class provides. Libraries such as circe use it to build JSON codecs for case classes and enums.

#### Why use type classes instead of inheritance for things like JSON encoding?

Instances can be added for types you don't own (library or Java classes), a type can have several instances in different contexts, the data classes stay free of serialization code, and a missing instance is a compile error rather than a run-time one.

#### What is `Ordering`?

The standard library's type class for sorting. `sorted`, `max` and `TreeMap` take a given `Ordering`; you build custom ones with `Ordering.by(_.amount)` and reverse them with `.reverse`.

#### What is multiversal equality?

An opt-in Scala 3 feature: with `import scala.language.strictEquality`, `==` compiles only between types that have a `CanEqual` instance, usually derived with `derives CanEqual`. It catches comparisons that are always false, such as a `CustomerId` with an `Int`.

<!-- challenge -->

A team adds `toJson` to 40 case classes through a `JsonSerializable` trait, but can't add it to classes from an external library. What design fixes both problems?

<!-- solution -->

A type class: an `Encoder[A]` with instances derived for the team's case classes (`derives`) and written by hand for the library types. The data classes no longer depend on JSON code, and any type can gain an encoder.

<!-- takeaways -->

- Type classes add behavior from outside a type.
- Context bounds request instances.
- `derives` generates instances from structure.

<!-- unit: Extension methods and conversions -->

<!-- goals -->

- Add methods to existing types with extension methods.
- Use implicit conversions sparingly, with `Conversion` and `into`.

<!-- concept -->

Extension methods add methods to types you can't change, such as `String` or a library class. They're resolved at compile time, cost nothing at run time, and replace Scala 2's implicit classes.

Implicit conversions silently turn one type into another. They made Scala 2 code hard to follow, so Scala 3 restricts them: you define a `given Conversion[A, B]`, and using it requires a language import unless the target is marked with `into`, stable since 3.9, which allows conversions only where an API asks for them.

<!-- example -->

```scala
extension (s: String)
  def toSnakeCase: String = s.replaceAll("([a-z])([A-Z])", "$1_$2").toLowerCase
  def isBlankOrNull: Boolean = s == null || s.isBlank

"orderDate".toSnakeCase          // order_date
```

#### What is an extension method?

A method defined outside a type that can be called as if it were a member: `extension (s: String) def toSnakeCase: String = ...` lets you write `"orderDate".toSnakeCase`. It's visible where it's defined or imported, or when it belongs to a given instance or companion in scope.

#### How did Scala 2 add methods to existing types?

With implicit classes, `implicit class RichString(s: String) { def toSnakeCase = ... }`, the "enrich my library" pattern. The compiler wrapped the value in the class when a missing method was called.

#### What is an implicit conversion, and why is it discouraged?

A rule that converts a value of type `A` to `B` automatically when `B` is expected. It hides what code does, can make wrong code compile, and slows compilation, so Scala 3 requires a `given Conversion[A, B]` and a `scala.language.implicitConversions` import (or `into`) to use one.

#### What does `into` do?

It marks a parameter type, or a whole class, as a target for implicit conversions: `def write(path: into Path)` lets callers pass any value that has a `Conversion` to `Path`, without the language import at call sites. Conversions then happen only where the API author allowed them.

#### How does the compiler find extension methods?

When `x.m` doesn't compile because `x` has no member `m`, the compiler looks for an extension method named `m` in scope (defined or imported), in given instances in scope, and in the implicit scope of `x`'s type, such as its companion object.

<!-- challenge -->

A codebase defines an implicit conversion from `String` to `LocalDate`. A column name passed by mistake where a date was expected compiled and failed at run time. What do you change?

<!-- solution -->

Remove the conversion and parse explicitly, for example with an extension method `"2026-10-22".toLocalDate` returning an `Either`, so the conversion is visible and failures are handled at the call site.

<!-- takeaways -->

- Extension methods add methods without wrappers.
- Conversions need `Conversion` and an opt-in.
- Prefer explicit conversions in application code.

<!-- stage: Engineering practice -->

### Concurrency

<!-- unit: Futures -->

<!-- goals -->

- Run asynchronous work with `Future` and an `ExecutionContext`.
- Compose futures and handle failures, blocking and parallelism limits.

<!-- concept -->

A `Future[A]` is a value that will hold a result, or a failure, later. It's computed on a thread pool provided by an `ExecutionContext`, starts running as soon as it's created, and is combined with `map`, `flatMap` and for-comprehensions instead of waiting.

Blocking a thread to wait for a result (`Await.result`) defeats the purpose, except at the very edge of a program or in tests. Blocking I/O inside a future should be wrapped in `blocking` or run on a dedicated pool, so it doesn't starve the shared one.

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

#### What is a `Future`?

A placeholder for a value computed asynchronously, which eventually completes with `Success(value)` or `Failure(exception)`. It's eager (it starts immediately) and its result is cached once complete.

#### What is an `ExecutionContext`?

The thread pool that runs futures and their callbacks, passed as a context parameter to most `Future` methods. `ExecutionContext.global` suits CPU-bound work; blocking calls need `blocking { ... }` or a separate bounded pool.

#### How do you compose futures?

With `map` and `flatMap` (or a for-comprehension) to chain dependent steps, `zip` to combine independent ones, and `Future.sequence` or `Future.traverse` to turn a collection of futures into a future of a collection.

#### Why do futures in a for-comprehension sometimes run one after the other?

If the futures are created inside the comprehension (`a <- fetchA(); b <- fetchB()`), the second is created only after the first completes. Create independent futures before the comprehension, as in the example, so they run concurrently.

#### Why should you avoid `Await.result`?

It blocks a thread until the future completes, which wastes threads, can deadlock a small pool and hides the asynchronous design. Use it only at the program's edge (a `main` that must wait) or in tests, always with a timeout.

#### How do you handle failures in a `Future`?

A thrown exception completes the future with a `Failure`. Recover with `recover` or `recoverWith`, transform both outcomes with `transform`, provide an alternative with `fallbackTo`, and react with `onComplete`, without throwing again inside callbacks.

#### How do you run many futures with limited parallelism?

`Future.traverse(items)(f)` starts all calls at once, which can overwhelm an API. Process items in batches (`grouped(n)` folded sequentially), run them on a bounded thread pool, or use a streaming or effect library with a parallelism limit, such as Cats Effect's `parTraverseN`.

<!-- challenge -->

A for-comprehension combines three independent API calls returning futures, and the total time is the sum of the three. How do you make it the time of the slowest?

<!-- solution -->

Start the three futures before the comprehension (`val a = callA(); val b = callB(); val c = callC()`) and only combine them inside it, or use `zip`; they then run concurrently.

<!-- takeaways -->

- Futures start eagerly on an `ExecutionContext`.
- Compose; don't block with `Await`.
- Start independent futures before combining them.

<!-- unit: Effects, actors and threads -->

<!-- goals -->

- Explain effect systems such as Cats Effect and ZIO.
- Know actors, virtual threads and safe shared state.

<!-- concept -->

Futures are eager and not referentially transparent: creating one starts work, so a future can't be retried or reused as a description of work. Effect libraries such as Cats Effect and ZIO describe programs as values (`IO`, `ZIO`) that run only when their runtime executes them. Programs then compose, retry and cancel safely, on lightweight fibers with resource safety and structured concurrency built in.

Actors, in Apache Pekko (the open-source fork of Akka), model concurrency as objects exchanging messages, suited to stateful and distributed systems. On JDK 21 and later, virtual threads also make plain blocking code scale.

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

#### What is an effect system?

A library that represents side effects as values describing what to do, such as `IO[A]` in Cats Effect or `ZIO[R, E, A]`, and runs them with a runtime. It adds lazy evaluation, cancellation, retries, resource safety and lightweight concurrency on top of pure functional code.

#### What is the difference between `Future` and `IO`?

A `Future` starts running when created and memoizes its result. An `IO` is a description that does nothing until run, and running it twice does the work twice. That makes `IO` referentially transparent: retries, timeouts and racing are just functions on values.

#### What are fibers?

Lightweight logical threads managed by an effect runtime and scheduled on a small pool of OS threads. Millions can exist at once, they can be cancelled, and blocking calls are moved to a separate pool.

#### What is the actor model, and what is Pekko?

Actors are objects that hold private state and communicate only through asynchronous messages, processing one message at a time, so no locks are needed. Pekko is the Apache fork of Akka, created after Akka moved to a commercial license in 2022.

#### What are virtual threads, and do they matter for Scala?

JDK 21 threads managed by the JVM rather than the OS, cheap enough to create one per task, so blocking code no longer wastes OS threads. Scala can use them directly, and libraries such as Ox build structured, direct-style concurrency on them as an alternative to futures and effect systems.

#### How do you share mutable state safely between threads?

Prefer immutable data and message passing. When state must be shared, use atomic references (`AtomicReference`, Cats Effect's `Ref`), concurrent collections (`TrieMap`, `ConcurrentHashMap`) or `synchronized` blocks, keeping critical sections small.

<!-- challenge -->

A retry helper takes `f: Future[A]` and calls it again on failure, but retries never call the API again. Why, and how do you fix it?

<!-- solution -->

The future started once when it was passed in, and "retrying" just reads the same failed result. Take a way to create it again, `f: () => Future[A]` or a by-name `f: => Future[A]`, or use `IO`, which describes the call and reruns it on each attempt.

<!-- takeaways -->

- `IO` describes work; `Future` already started it.
- Fibers and virtual threads make concurrency cheap.
- Share state through atomics, `Ref` or messages.

### Tooling, Java interop and testing

<!-- unit: Build tools -->

<!-- goals -->

- Structure an sbt build with dependencies, scopes and settings.
- Package Spark jobs, cross-build libraries and know Scala CLI and Mill.

<!-- concept -->

sbt is the most common Scala build tool. `build.sbt` declares the Scala version, dependencies and settings, and sbt compiles incrementally, runs tests and publishes artifacts. Scala library artifacts carry the Scala binary version in their name (`_2.13`, `_3`), which the `%%` operator adds for you.

For scripts and small projects, Scala CLI (the `scala` command) needs no build file, and Mill is a faster alternative build tool. Spark jobs are usually packaged as one JAR, with Spark itself marked `provided` because the cluster supplies it.

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

#### What is sbt?

The standard Scala build tool: it compiles incrementally, resolves dependencies, runs tests, starts a REPL and publishes artifacts. Builds are defined in `build.sbt` with settings and tasks, and extended with plugins (`project/plugins.sbt`).

#### What is the difference between `%` and `%%` in sbt?

`%%` appends the project's Scala binary version to the artifact name (`spark-sql` becomes `spark-sql_2.13`), as needed for Scala libraries. `%` uses the name as is, for Java libraries.

#### What does the `provided` scope mean?

The dependency is available at compile time but not packaged, because the runtime environment supplies it. Spark and Hadoop are `provided` in Spark jobs, which keeps the JAR small and avoids version conflicts with the cluster.

#### How do you build a fat JAR?

With the sbt-assembly plugin, which packages your code and its dependencies into one JAR. Merge strategies resolve duplicate files (for example in `META-INF`), and shading renames conflicting packages, such as an older Jackson or Guava used by a dependency.

#### What is cross-building?

Compiling and publishing a library for several Scala versions: `crossScalaVersions := Seq("2.13.18", "3.3.8")`, then `sbt +test` or `+publish` runs the task for each. Version-specific code goes in `src/main/scala-2.13` or `scala-3` folders.

#### What are Scala CLI and Mill?

Scala CLI, now the `scala` command, runs and packages single-module projects with `//> using` directives in source files instead of a build file. Mill is a build tool with builds written as Scala objects, known for fast, cached builds. Both are alternatives to sbt for different project sizes.

#### Why do Scala versions affect binary compatibility?

Libraries are compiled against one Scala binary version (2.12, 2.13 or 3), and those series aren't binary-compatible with each other, so each library is published once per version. Scala 3 is the exception: it can use most Scala 2.13 artifacts, and Scala 3 minor versions stay backward compatible.

<!-- challenge -->

A Spark job's JAR is 400 MB and fails on the cluster with `NoSuchMethodError` in Jackson classes. What do you change in the build?

<!-- solution -->

Mark Spark and Hadoop as `provided`, so they're no longer packaged, align the remaining dependency versions with the cluster's, and shade the conflicting library in sbt-assembly if a dependency really needs another Jackson version.

<!-- takeaways -->

- `%%` adds the Scala binary version.
- Spark is `provided` in job JARs.
- Assembly builds fat JARs; shading resolves conflicts.

<!-- unit: Java interop -->

<!-- goals -->

- Call Java libraries from Scala and Scala from Java.
- Convert collections and handle nulls, checked exceptions and JDK versions.

<!-- concept -->

Scala runs on the JVM, so any Java library is one dependency away, and calls look like Scala calls. The friction is at the edges: Java collections need converting to Scala ones, Java APIs may return `null`, and Java's checked exceptions aren't tracked by the Scala compiler.

In the other direction, Scala features without a Java equivalent, such as default arguments, givens and companion objects, look odd from Java, so APIs meant for Java callers stay simple.

<!-- example -->

```scala
import scala.jdk.CollectionConverters.*
import java.nio.file.{Files, Paths}

val ids: List[String] = Files.readAllLines(Paths.get("ids.txt")).asScala.toList
val javaList: java.util.List[String] = List("a", "b").asJava
val appHome: Option[String] = Option(System.getenv("APP_HOME"))    // null becomes None
```

#### How do you convert between Java and Scala collections?

Import `scala.jdk.CollectionConverters.*` and call `.asScala` or `.asJava`, which wrap the collection without copying; add `.toList` or `.toMap` for an immutable copy. In Scala 2.12 the import was `scala.collection.JavaConverters._`.

#### How do you deal with `null` from Java code?

Wrap values from Java in `Option(...)` at the boundary, so `null` becomes `None` and the rest of the code works with `Option`. Never let `null` travel into Scala domain code.

#### How are Java's checked exceptions handled?

Scala doesn't distinguish checked exceptions: you aren't forced to catch or declare them. Catch them where you can handle them, or wrap the call in `Try`. Add `@throws[IOException]` to Scala methods that Java code calls, so Java sees the declaration.

#### How do Scala features look from Java?

Objects compile to a class with a static `MODULE$` instance plus static forwarders, traits to interfaces with default methods, default arguments to methods named like `connect$default$2`, and givens to ordinary parameters. Keep APIs meant for Java callers plain.

#### How do Scala functions and Java functional interfaces interoperate?

Scala lambdas convert automatically to Java functional interfaces (single abstract method types) such as `Runnable` or `java.util.function.Function`. `scala.jdk.FunctionConverters` converts function objects explicitly when needed.

#### Which JDK should Scala code run on?

Scala 3.8 and later require JDK 17 or newer; Scala 3.3 LTS, 2.13 and 2.12 still run on JDK 8. In practice teams use an LTS JDK, 17, 21 or 25, matching their platform: Spark 4 requires JDK 17 or later.

<!-- challenge -->

A Java SDK returns a `java.util.Map[String, String]` of tags that is sometimes `null`, and `sdk.tags().asScala.get("env")` throws a `NullPointerException`. Fix it.

<!-- solution -->

Wrap the result first: `Option(sdk.tags()).map(_.asScala.toMap).getOrElse(Map.empty).get("env")`, so a missing map behaves like an empty one.

<!-- takeaways -->

- `asScala`/`asJava` convert collections.
- Wrap Java results in `Option`.
- Scala 3.8+ needs JDK 17.

<!-- unit: Testing -->

<!-- goals -->

- Write tests with ScalaTest or MUnit and property-based tests with ScalaCheck.
- Test Spark code and mock dependencies sensibly.

<!-- concept -->

Scala test frameworks combine a style of test definition with assertions and runners integrated into sbt. ScalaTest offers several styles (`AnyFunSuite`, `AnyFlatSpec`, `AnyWordSpec`); MUnit keeps a small API with clear diffs. Both run with `sbt test` and in IDEs.

Property-based testing with ScalaCheck generates many random inputs and checks that a property holds, shrinking failures to a minimal case. Pure functions make all of this easier: no setup, no mocks, just inputs and outputs.

<!-- example -->

```scala
import munit.FunSuite

class AmountSuite extends FunSuite:
  test("parses amounts with spaces"):
    assertEquals(parseAmount(" 12.50 "), Right(BigDecimal("12.50")))

  test("rejects garbage"):
    assert(parseAmount("abc").isLeft)
```

#### Which testing libraries are common in Scala?

ScalaTest (many styles, rich matchers), MUnit (minimal, fast, good diffs), specs2, ScalaCheck for property-based testing, and effect-aware frameworks such as weaver or ZIO Test for `IO` and `ZIO` code.

#### What is property-based testing?

Stating a property that must hold for all inputs and letting a library generate hundreds of random cases, shrinking any failure to the smallest counterexample:

```scala
import org.scalacheck.Prop.forAll
val reverseTwice = forAll((xs: List[Int]) => xs.reverse.reverse == xs)
```

#### How do you test Spark code in Scala?

Write transformations as functions from `DataFrame` to `DataFrame`, build small inputs with `Seq(...).toDF(...)`, run them on a local `SparkSession` shared by the test suite (`master("local[2]")`), and compare collected results or use a helper library for DataFrame equality.

#### How do you mock dependencies in Scala?

Prefer designing for testability: depend on traits or functions and pass simple fake implementations in tests. For Java-heavy code, Mockito works through mockito-scala, but heavy mocking often signals that effects aren't separated from logic.

#### How do you run a subset of tests with sbt?

`sbt "testOnly *AmountSuite"` runs one suite, `testQuick` reruns failed and changed tests, and the `~` prefix (`~testQuick`) reruns them on every file change.

<!-- challenge -->

Each Spark test suite creates its own `SparkSession`, and the test run takes 15 minutes. How do you speed it up?

<!-- solution -->

Share one local session across suites through a common trait or fixture, run with `local[2]`, set `spark.sql.shuffle.partitions` to a small number and disable the UI; most of the time went into starting sessions and shuffling into 200 partitions.

<!-- takeaways -->

- ScalaTest and MUnit are the common choices.
- ScalaCheck finds edge cases.
- Share one local Spark session in tests.

<!-- unit: Code quality and migration -->

<!-- goals -->

- Keep code consistent with scalafmt, scalafix and compiler warnings.
- Plan a migration from Scala 2.13 to Scala 3.

<!-- concept -->

Formatting and linting are automated in most Scala teams: scalafmt formats code, scalafix applies lint rules and automated rewrites, and compiler warnings such as unused imports or non-exhaustive matches catch real bugs when CI treats them as errors.

Migrating from Scala 2.13 to Scala 3 is mostly source-compatible. The compiler can rewrite old syntax, and Scala 3 code can use Scala 2.13 libraries. The hard parts are Scala 2 macros, which must be rewritten, and dependencies that haven't published for Scala 3.

<!-- example -->

```scala
// build.sbt (Scala 3)
scalacOptions ++= Seq("-deprecation", "-feature", "-Wunused:all", "-Werror")
```
```bash
sbt scalafmtAll "scalafixAll RemoveUnused" test
```

#### What are scalafmt and scalafix?

scalafmt is the standard code formatter, configured in `.scalafmt.conf` and checked in CI. scalafix is a refactoring and linting tool whose rules remove unused imports, enforce conventions and automate migrations.

#### Which compiler options help catch bugs?

`-deprecation` and `-feature` explain warnings, `-Wunused:all` reports unused imports and variables, `-Wvalue-discard` flags discarded non-`Unit` values, and `-Werror` (formerly `-Xfatal-warnings`) turns warnings into errors so they can't accumulate.

#### How do you migrate a project from Scala 2.13 to Scala 3?

Update dependencies to versions published for Scala 3 (or use 2.13 ones with `.cross(CrossVersion.for3Use2_13)`), compile with `-source:3.0-migration -rewrite` to fix syntax automatically, rewrite macros, and cross-build during the transition. Start with leaf modules and libraries, then services.

#### Which Scala 2 features changed or were dropped in Scala 3?

Scala 2 macros, existential types (`forSome`), procedure syntax (`def f() { ... }`), symbol literals, `do`-`while` loops and auto-application of empty parameter lists were dropped. Implicits still work but are superseded by givens, and package objects are deprecated in favor of top-level definitions.

#### What is TASTy?

The typed abstract syntax tree format that Scala 3 stores in `.tasty` files next to the bytecode. It keeps full type information, which lets the compiler consume libraries across Scala 3 versions, supports `inline` and macros, and powers IDE tooling.

<!-- challenge -->

A company has 40 Scala 2.13 services and libraries and wants to move to Scala 3. How do you plan it?

<!-- solution -->

Upgrade shared libraries first and cross-build them for 2.13 and 3, then migrate services one at a time with the migration rewrites, replacing macros and unsupported dependencies. Keep Spark jobs on 2.13, and turn on warnings as errors once each module compiles cleanly.

<!-- takeaways -->

- Automate formatting, linting and warnings in CI.
- Scala 3 can use Scala 2.13 libraries.
- Migrate libraries first; Spark jobs stay on 2.13.

<!-- stage: Scala for data engineering -->

### Scala and Spark

<!-- unit: Spark's Scala API -->

<!-- goals -->

- Explain how Scala relates to Spark and when to choose it over PySpark.
- Create a `SparkSession`, read data and write DataFrame transformations in Scala.

<!-- concept -->

Spark is written in Scala, and its Scala API is the most direct one: no Python processes, typed Datasets checked at compile time, and access to Spark's internal extension points. DataFrame operations compile to the same plans in every language, so PySpark is just as fast for built-in operations; Scala's advantages show in UDFs, typed pipelines, custom connectors and libraries.

The DataFrame API reads almost the same in both languages, with a few Scala-specific symbols such as `$"col"` and `===`.

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

#### Why is Spark associated with Scala?

Spark was written in Scala at UC Berkeley, and its core, its APIs and most of its ecosystem (connectors, Delta Lake's original code base) are Scala. New features appear in the Scala API first, and Spark's internals are Scala classes.

#### Scala or PySpark: how do you choose?

PySpark fits teams that work in Python, use Python libraries (pandas, ML) and stick to built-in functions. Scala fits teams that want compile-time checks, typed Datasets, fast JVM UDFs, custom data sources or Spark extensions. Platform support and the team's skills usually decide.

#### Is a DataFrame query faster in Scala than in PySpark?

Not for built-in operations: both build the same logical plan, which Catalyst optimizes and the JVM executes. Differences appear with UDFs, which in PySpark ship rows to Python workers, and with driver-side code.

#### What does `import spark.implicits._` do?

It brings encoders for primitives, tuples and case classes into scope, the `$"column"` syntax, and `toDF` and `toDS` on local collections, such as `Seq((1, "a")).toDF("id", "name")`.

#### How do you reference columns in Scala Spark?

With `$"amount"`, `col("amount")`, `df("amount")` (useful to disambiguate columns after a join) or a plain string in methods that accept names. The Scala 2 symbol syntax `'amount` is deprecated.

#### Why does Spark Scala use `===` for column equality?

`==` is Scala's object equality and returns a `Boolean`, comparing the `Column` objects themselves. `===` builds an equality expression evaluated per row, and `=!=` its negation.

<!-- challenge -->

`df.filter($"country" == "FR")` doesn't compile in a Scala Spark job. Why, and what's the fix?

<!-- solution -->

`==` compares the `Column` object with a string and returns a `Boolean`, which `filter` doesn't accept. Use `$"country" === "FR"`, which builds a column expression.

<!-- takeaways -->

- Spark's native API is Scala.
- Built-in DataFrame code performs the same in Scala and Python.
- Use `===` and `=!=` for column comparisons.

<!-- unit: Datasets and encoders -->

<!-- goals -->

- Use typed Datasets with case classes and encoders.
- Decide between Datasets and DataFrames.

<!-- concept -->

A `Dataset[T]` is a distributed collection of typed objects: you transform it with ordinary Scala functions over case classes, and the compiler checks field names and types. A DataFrame is `Dataset[Row]`, untyped. Encoders convert between JVM objects and Spark's internal binary format and are derived for case classes and primitives.

Typed lambdas are opaque to the optimizer, though: `ds.filter(_.amount > 0)` deserializes every row into an object, while `ds.filter($"amount" > 0)` can be pushed down to the files. Many teams use case classes at boundaries and column expressions inside.

<!-- example -->

```scala
final case class Order(orderId: Long, customerId: String, amount: Double, country: String)

val ds = spark.read.parquet("s3://lake/silver/orders").as[Order]   // column names must match
val slow = ds.filter(_.amount > 1000)              // typed lambda: no pushdown
val fast = ds.filter($"amount" > 1000)             // column expression: pushdown
val counts = ds.groupByKey(_.country).count()      // Dataset[(String, Long)]
```

#### What is the difference between a DataFrame and a Dataset?

A Dataset is typed: `Dataset[Order]` exposes `Order` objects, and typed operations are checked at compile time. A DataFrame is `Dataset[Row]`, whose columns are checked only when the plan is analyzed at run time. Both run on the same engine.

#### What is an encoder?

An object that converts between a JVM type and Spark's internal row format, knowing the schema. Spark derives encoders for case classes, tuples and primitives through `import spark.implicits._`; other types need `Encoders.kryo` or a conversion.

#### Why can typed Dataset operations be slower?

Lambdas such as `map(o => ...)` or `filter(_.amount > 0)` are black boxes to Catalyst: each row must be deserialized into an object, and filters can't be pushed down to Parquet. Column expressions keep data in the internal format and stay optimizable.

#### How do you convert between DataFrames and Datasets?

`df.as[Order]` gives a Dataset (failing if columns are missing or types don't match), `ds.toDF()` goes back, and `Seq(...).toDS()` or `spark.createDataset` builds one from local data.

#### Can you use Datasets from PySpark?

No. Python is dynamically typed, so PySpark exposes only DataFrames. Typed Datasets exist in Scala and Java.

#### How do you model nullable columns in a case class?

With `Option` fields, such as `amount: Option[Double]`. A primitive field like `Double` can't hold `null`, so a null value in the data fails at run time.

<!-- challenge -->

A job reading `orders.as[Order]` fails at run time with a null error on the `discount` field, which is empty for some rows. What do you change?

<!-- solution -->

Declare the field as `discount: Option[Double]` in the case class, so nulls become `None`, and handle the missing case in the transformation.

<!-- takeaways -->

- Datasets are typed; DataFrames are `Dataset[Row]`.
- Typed lambdas skip optimizer pushdown.
- Nullable columns need `Option` fields.

<!-- unit: UDFs, closures and serialization -->

<!-- goals -->

- Write Scala UDFs and know when to avoid them.
- Fix "Task not serializable" and use broadcast variables and per-partition resources.

<!-- concept -->

Spark ships the functions you write to executors, so everything a closure references must be serializable. Referencing a field or method of an enclosing class captures the whole object, often with something non-serializable inside, such as a database client, and the job fails with "Task not serializable".

Scala UDFs run in the JVM, avoiding PySpark's round trip to Python, but they're still black boxes for the optimizer. Built-in functions remain the first choice, and a broadcast variable sends a lookup table to each executor once instead of with every task.

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

#### Why does "Task not serializable" happen, and how do you fix it?

A closure sent to executors references something that can't be serialized, often because it uses a field or method of an enclosing class, which captures the whole instance. Copy the needed value into a local `val` before the closure, move helpers to an `object`, or create non-serializable resources on the executors.

#### Are Scala UDFs faster than Python UDFs?

Yes: they run inside the executor JVM, without serializing rows to a Python process. They're still opaque to Catalyst, which can't optimize through them or push filters past them, so built-in functions are faster still.

#### What is a broadcast variable?

A read-only value, such as a lookup map, sent once to each executor and cached there (`sparkContext.broadcast(value)`, read with `.value`). Without it, a large value captured by a closure is shipped with every task.

#### What is the difference between a broadcast variable and a broadcast join?

A broadcast variable ships an arbitrary value you use in your own code. A broadcast join is a join strategy for DataFrames, triggered automatically for small tables or with the `broadcast(df)` hint, in which Spark sends the small table to every executor instead of shuffling both sides.

#### What are accumulators?

Shared variables that tasks can only add to, such as counters of bad records, read on the driver. Updates made inside transformations can be applied twice when tasks are retried; only updates inside actions are guaranteed to count once.

#### How do you use a database or HTTP client inside a Spark job?

Create it once per partition with `foreachPartition` or `mapPartitions`, not once per row and not on the driver, and write in batches. The client never needs to be serialized because it's created on the executor.

<!-- challenge -->

A job sends each row to an API in `foreach`, creating an HTTP client per row, and it's very slow. Moving the client to a class field causes "Task not serializable". What's the right structure?

<!-- solution -->

Use `foreachPartition`: create one client per partition on the executor, send rows in batches, and close the client at the end. Nothing non-serializable is captured, and connection overhead is paid once per partition.

<!-- takeaways -->

- Closures must capture only serializable values.
- Prefer built-ins to UDFs, even in Scala.
- Create clients per partition, not per row.

### Data work in Scala

<!-- unit: JSON, configuration and I/O -->

<!-- goals -->

- Parse JSON into case classes and load typed configuration.
- Manage files, HTTP calls, databases and resources safely.

<!-- concept -->

Outside Spark, Scala jobs and services read JSON, configuration and files. JSON libraries derive codecs for case classes from their structure (circe, upickle, jsoniter-scala), so parsing returns typed values or a clear error instead of maps of strings. Configuration in HOCON files is read with Typesafe Config or loaded directly into case classes with PureConfig.

Resources such as files and connections must be closed even when errors happen, which `scala.util.Using` does for anything `AutoCloseable`.

<!-- example -->

```scala
import io.circe.Decoder
import io.circe.parser.decode

final case class Event(id: String, kind: String, amount: Option[BigDecimal]) derives Decoder

val parsed: Either[io.circe.Error, Event] =
  decode[Event]("""{"id":"e1","kind":"purchase","amount":12.5}""")
```

#### How do you parse JSON in Scala?

With a library that derives codecs for case classes: circe (`derives Decoder`, then `decode[Event](json)`), upickle, or jsoniter-scala for high throughput. Decoding returns an `Either` with a precise error path when a field is missing or has the wrong type.

#### How do you read configuration in Scala?

Typesafe Config reads `application.conf` files in HOCON format, with environment overrides such as `url = ${?DB_URL}`. PureConfig loads the configuration straight into case classes and reports every missing or invalid field at once, at start-up.

#### What does `scala.util.Using` do?

It runs a block with a resource and closes it afterwards, even on exceptions, like Java's try-with-resources. `Using(resource)(f)` returns a `Try`, `Using.resource` returns the value directly and throws on failure, and `Using.Manager` handles several resources.

#### How do you work with files and paths?

With `java.nio.file` (`Files`, `Paths`) through Scala, or os-lib for concise scripting (`os.read.lines`, `os.walk`, `os.proc` for subprocesses). `scala.io.Source` is enough for reading simple text files.

#### How do you call a REST API from Scala?

With sttp client (choosing a synchronous, `Future` or effect backend) or requests-scala for scripts: set timeouts, retry transient errors with backoff, and decode JSON responses into case classes.

#### How do you query a database from Scala?

With JDBC directly or through a library: Doobie for Cats Effect code, Slick, ScalikeJDBC or Magnum. Use parameterized queries, a connection pool such as HikariCP, and `Using` or the library's resource handling to close connections.

<!-- challenge -->

A job calls `config.getString("db.url")` deep inside its processing and fails an hour in when the key is missing in production. How do you prevent it?

<!-- solution -->

Load the whole configuration into a case class at start-up (with PureConfig, or by reading every key once) and fail immediately with a list of what is missing; the rest of the code receives the typed settings.

<!-- takeaways -->

- Derive JSON codecs for case classes.
- Load and validate configuration at start-up.
- Close resources with `Using`.

<!-- unit: Performance on the JVM -->

<!-- goals -->

- Avoid boxing and wasteful collection use.
- Measure performance with JMH and understand JIT warm-up and garbage collection.

<!-- concept -->

Scala code runs on the JVM's just-in-time compiler, which optimizes hot code after it has run for a while. That's why micro-benchmarks need warm-up, which JMH handles, and why short-lived jobs pay start-up costs. Garbage collection reclaims short-lived objects cheaply, but very high allocation rates still show up as pauses.

Generic code boxes primitives (a `List[Int]` holds `java.lang.Integer` objects), so hot numeric loops use arrays of primitives. Choosing the right collection and avoiding intermediate ones gives the largest wins; measure before optimizing.

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

#### What is boxing, and when does it happen in Scala?

Wrapping a primitive value in an object (`Int` into `java.lang.Integer`) so it can be used where an object is expected. It happens in generic collections and methods, in `Option[Int]` and in function values, and costs allocation and indirection in hot loops. Arrays of primitives avoid it.

#### How do you benchmark Scala code correctly?

With JMH through the sbt-jmh plugin, which handles JVM warm-up, forking, dead-code elimination and statistics. Timing a single run with `System.nanoTime` mostly measures the interpreter and the JIT compiler, not your code.

#### What is JIT warm-up?

The JVM first interprets bytecode, then compiles frequently executed methods to optimized machine code. Code gets faster after thousands of executions, so the first seconds of a job or benchmark are slower than steady state.

#### How does garbage collection affect Scala programs?

Immutable code allocates many short-lived objects, which generational collectors such as G1 (the default) reclaim cheaply. Problems come from very high allocation rates or large live data sets; heap size (`-Xmx`), collector choice (ZGC for low pauses) and fewer allocations are the levers.

#### Why avoid exceptions for control flow?

Creating an exception captures a stack trace, which is expensive, and hides the failure path from types. Return `Option` or `Either` for expected failures; for unavoidable exception-based control flow, `scala.util.control.NoStackTrace` avoids the stack capture.

<!-- challenge -->

A pricing service is slow, and a profiler shows 40% of CPU time in garbage collection and boxing. The hot loop sums `List[Double]` values through several `map` and `filter` calls. What do you do?

<!-- solution -->

Rewrite the hot path as a single pass over an `Array[Double]` (a `while` loop or one fold over a view), removing intermediate collections and boxing; then confirm the gain with a JMH benchmark and the profiler.

<!-- takeaways -->

- Generic code boxes primitives.
- Benchmark with JMH, after warm-up.
- Remove intermediate collections in hot loops.

<!-- stage: Putting it together -->

### Scenarios

<!-- unit: Designing a Scala data job -->

<!-- goals -->

- Structure a Spark job in Scala for testability and safe reruns.
- Combine typed models, configuration, tests and packaging.

<!-- concept -->

A production Scala job brings the earlier units together: configuration loaded and checked at start-up, case classes at the boundaries, transformations written as pure functions from DataFrame to DataFrame and unit-tested on small data, input and output kept in a thin `main`, and a build that produces one artifact for the cluster. Idempotent writes, which replace a partition instead of appending to it, make reruns safe.

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

#### How do you structure a Spark job in Scala for testability?

Separate pure transformations (`DataFrame => DataFrame` functions in an object) from reading, writing and configuration in `main`. Tests call the transformations on small DataFrames with a shared local session; `main` stays thin enough to need only an integration test.

#### How do you make a Spark job's writes idempotent?

Overwrite exactly the slice the run produces: dynamic partition overwrite for Parquet tables, `replaceWhere` or `MERGE` for Delta and Iceberg tables. Plain `append` duplicates data whenever a run is retried.

#### How do you pass arguments and configuration to a Spark job?

Command-line arguments after the JAR in `spark-submit`, parsed with a library such as scopt or decline; Spark settings with `--conf`; environment-specific values from configuration files or the environment, validated at start-up.

<!-- challenge -->

A daily job writes with `mode("append")`, and a retry after a timeout duplicated a day's revenue. Rewrite its write strategy.

<!-- solution -->

Write with `mode("overwrite")`, partitioned by date, and `partitionOverwriteMode` set to `dynamic`, so a run replaces only its own day's partition (or use `replaceWhere` on a Delta table); reruns then leave the same data.

<!-- takeaways -->

- Pure transformations, thin `main`.
- Overwrite the slice; never blindly append.
- Validate arguments and configuration first.

<!-- unit: Coding exercises in Scala -->

<!-- goals -->

- Solve common coding exercises idiomatically in Scala.
- Explain trade-offs between functional and imperative solutions.

<!-- concept -->

In live coding, interviewers look for correct, idiomatic code first: immutable values, collection methods, pattern matching, and `Option` instead of `null`. State the complexity, start with the clearest version, and switch to local mutation or arrays only when you can explain why it's faster.

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

#### Reverse the order of the words in a sentence.

```scala
def reverseWords(s: String): String = s.trim.split("\\s+").reverse.mkString(" ")
```

#### Find the second largest distinct value in a list.

```scala
def secondLargest(xs: List[Int]): Option[Int] =
  xs.distinct.sorted.reverse.lift(1)
```

This is O(n log n); a single `foldLeft` that tracks the two largest values makes it O(n).

#### Find the length of the longest substring without repeating characters.

```scala
def longestUnique(s: String): Int =
  s.indices.foldLeft((0, 0, Map.empty[Char, Int])) { case ((best, start, last), i) =>
    val newStart = last.get(s(i)).filter(_ >= start).map(_ + 1).getOrElse(start)
    (best.max(i - newStart + 1), newStart, last.updated(s(i), i))
  }._1
```

#### Implement binary search on a sorted array.

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

#### Flatten an arbitrarily nested structure of integers.

Model the nesting with an enum, then recurse:

```scala
enum Nested:
  case Leaf(value: Int)
  case Node(children: List[Nested])

def flatten(n: Nested): List[Int] = n match
  case Nested.Leaf(v)  => List(v)
  case Nested.Node(cs) => cs.flatMap(flatten)
```

<!-- challenge -->

After your FizzBuzz, the interviewer asks for a version that handles n = 100 million without building the whole list in memory. What do you change?

<!-- solution -->

Return an `Iterator[String]` (`(1 to n).iterator.map { ... }`) or a view instead of a `List`, so values are produced on demand and the caller can stream them.

<!-- takeaways -->

- Correct and idiomatic first, then optimize.
- State complexity and trade-offs.
- Use iterators for large or infinite outputs.
